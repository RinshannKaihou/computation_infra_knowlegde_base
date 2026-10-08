---
id: data-storage.checkpoint-slow-io-triage
title: Checkpoint 慢写与恢复 I/O 诊断指南
type: procedure
domain: data-storage
status: draft
platforms: [generic]
source_refs:
  - src.pytorch.dcp-2.6
  - src.kernel.docs-sysctl-vm-v6.16
  - src.linux-man-pages.fsync-6.19
  - src.ascend.mindio-acp-v26.1.1
  - src.mlcommons.storage-rules-v2.0
  - src.pytorch.tutorial-async-checkpoint-2026-09-30
updated_at: "2026-10-08"
summary: 把 checkpoint 保存/恢复慢定位到状态收集、staging 拷贝、后台写入、内核 writeback/fsync、存储后端或读路径；以 PyTorch 2.6 DCP 与 MindIO ACP 为固定样板，保留网络存储证据缺口。
related_ids:
  - data-storage.checkpoint-durability
  - training.checkpoint-state-consistency
  - data-storage.training-data-path
  - reliability.evidence-and-hypotheses
applicability:
  environment_refs: []
  notes: "流程以 PyTorch 2.6 DCP（固定 v2.6.0 源码）与 MindCluster v26.1.1 MindIO ACP 为证据样板；目标环境的框架版本、writer/stager 配置、存储实现与内核参数需另行固定。"
verification:
  status: source_checked
  evidence_refs:
    - src.pytorch.dcp-2.6
    - src.kernel.docs-sysctl-vm-v6.16
    - src.ascend.mindio-acp-v26.1.1
    - src.mlcommons.storage-rules-v2.0
  notes: "已核对 DCP async_save/staging/writer/reader 实现、Linux vm.rst 的 dirty/writeback 语义、MindIO ACP 接口文档与 MLPerf checkpointing 规则；未执行保存、恢复或存储压测。"
---

# Checkpoint 慢写与恢复 I/O 诊断指南

## 目标与触发条件

触发：checkpoint 保存耗时变长或阻塞训练、恢复（读取）慢、保存期间训练步出现周期性停顿。本流程把“慢”定位到具体阶段：**状态收集与序列化 → staging（设备到主机/主机内存拷贝）→ 后台写入 → 内核页缓存与 fsync → 存储后端 →（恢复侧）读与反序列化**。各层的完成语义见[Checkpoint 写入与持久化边界](checkpoint-durability.md)；恢复后状态正确性属 [06](../06-training/checkpoint-state-consistency.md)，不在本文范围。

## 适用范围与前置条件

证据样板：PyTorch 2.6 DCP（文档 + v2.6.0 固定源码）、MindCluster v26.1.1 的 MindIO ACP、Linux kernel v6.16 的 vm 文档（固定 commit）、MLPerf Storage v2.0。进入排查前固定：框架与 writer/stager 实现及版本、`sync_files`/`thread_count`/`single_file_per_rank`/staging 配置、同步或异步保存、存储后端类型、内核 dirty 参数、每次保存的数据量与分片数。

**缺口声明**：网络文件系统、RDMA、对象存储的传输行为暂无已核对来源，相关支路只能按现场证据处理；DCP 2.6 的 `dcp_logger` 只有方法级总耗时，没有分阶段计时，阶段拆分需自行打点。

## 需要的证据

| 证据 | 采集范围或定位 | 用途 | 缺失时如何处理 |
|---|---|---|---|
| 保存配置与身份 | writer/stager 实现与参数、保存 ID、数据量 | 决定哪些机制适用 | 配置未知时只做症状描述 |
| 阶段时间线 | 训练循环中保存点的停顿位置、后台任务完成时间、dcp_logger 事件（仅方法级） | 区分主线程阻塞与后台慢 | 无分阶段计时则用训练侧打点补齐 |
| staging 证据 | staging 期间主线程停顿、CPU 内存增长（BlockingAsyncStager 全量 CPU 复制；cache_staged_state_dict 的 pinned 常驻） | staging 支路 | 见步骤 2 的版本语义 |
| 内核层证据 | dirty/writeback 计数、写者节流迹象 | 页缓存/writeback 支路 | 与后端指标对齐才有意义 |
| 存储后端证据 | 后端带宽/延迟/错误，同窗口 | 后端支路 | 应用慢但后端空闲时不能定为存储 |
| 读侧证据 | 读带宽、缓存冷/热、反序列化时间 | 恢复慢支路 | 页缓存会污染读测量（见步骤 5） |

## 步骤与判断分支

| 步骤 | 检查或动作 | 运行影响 | 预期证据与解释 | 下一步 |
|---|---|---|---|---|
| 1 | 固定保存路径与配置：同步 `save` 还是 `async_save`；writer 是 `FileSystemWriter`（继承 `BlockingAsyncStager`）还是自定义 stager；`sync_files`（默认 True，每文件写后 fsync）、`thread_count`（默认 1）、`single_file_per_rank`、`cache_staged_state_dict` | 只读 | 配置决定慢的可能位置 | 进步骤 2 |
| 2 | 区分主线程阻塞与后台慢（PyTorch 2.6 语义）：`async_save` 的 **staging 在主线程内执行**（[state_dict_saver.py L228–242](https://github.com/pytorch/pytorch/blob/1eba9b3aa3c43f86f4a2c807ac8e12c4a7767340/torch/distributed/checkpoint/state_dict_saver.py#L228-L242)）——默认 `BlockingAsyncStager` 把整个 state_dict 复制到 CPU RAM，大模型时这次拷贝会阻塞训练循环；`async_save` 还要求进程组含 CPU 后端（否则 assert）。后台 `save` 内部有两次集合通信同步点（plan 的 reduce_scatter 与 write 的 all_reduce，[L273–334](https://github.com/pytorch/pytorch/blob/1eba9b3aa3c43f86f4a2c807ac8e12c4a7767340/torch/distributed/checkpoint/state_dict_saver.py#L273-L334)），**慢 rank 会拖到这两个集合点** | 只读分析 | 停顿集中在保存调用期间 → staging/主线程支路；训练步正常但完成时间晚 → 后台/集合点支路 | 按分支进 3/4/5 |
| 3 | 写路径分支：`thread_count>1` 时分桶并发写，但源码 TODO 明确多线程与 `_OverlappingCpuLoader` 组合会 “significant performance degredation”（原文拼写如此，与 CUDA stream syncs 相关），重叠 D2H 装载仅在 `thread_count==1` 且 `inflight_threshhold>0` 时启用（[filesystem.py L290–302](https://github.com/pytorch/pytorch/blob/1eba9b3aa3c43f86f4a2c807ac8e12c4a7767340/torch/distributed/checkpoint/filesystem.py#L290-L302)）；`sync_files=True` 时**每文件写后 fsync**（[L331–334](https://github.com/pytorch/pytorch/blob/1eba9b3aa3c43f86f4a2c807ac8e12c4a7767340/torch/distributed/checkpoint/filesystem.py#L331-L334)）——fsync 等待设备确认，慢后端上这是显式的耗时来源，但关闭它牺牲的是故障一致性（同文件 L466 明确提醒，见[持久化边界](checkpoint-durability.md)），不是免费的提速 | 只读 | 慢在 fsync/写入 → 进步骤 4；慢在序列化/拷贝 → 回到步骤 2 | 按分支 |
| 4 | 内核层：write 返回不等于落盘。`dirty_background_ratio/bytes` 是触发后台 writeback 的阈值；`dirty_ratio/bytes` 是写者自身参与 writeout 的阈值；老化脏页还受 `dirty_expire_centisecs` 与周期唤醒 `dirty_writeback_centisecs` 管理（[vm.rst L165–242，kernel v6.16 固定 commit](https://github.com/torvalds/linux/blob/038d61fd642278bab63ee8ef722c50d10ab01e8f/Documentation/admin-guide/sysctl/vm.rst#L165-L242)）。阈值不是唯一写回条件，显式 fsync 的语义与错误边界见 [fsync(2)](https://man7.org/linux/man-pages/man2/fsync.2.html) | 只读计数器 | 节流迹象与保存窗口对齐 → 定位到 writeback/写者节流等待；后端消化速度不足也可导致脏页积累，不能据此排除存储后端，这是本库的归因边界判断 | 进步骤 5，对照同窗口后端吞吐、延迟和错误；缺少后端证据时根因保持 `unknown` |
| 5 | 后端与读侧：后端带宽/延迟与保存窗口对齐；读恢复慢的测量注意页缓存污染——MLPerf Storage v2.0 的 checkpointing 规则强制“checkpoint 每客户端大小 < 3× 客户端内存则必须 drop_caches 后再测读”（[Submission_guidelines §2.2.2.1](https://github.com/mlcommons/storage/blob/7e71ca162d8f9e7ae4b5b698d7d79b0883817f25/Submission_guidelines.md)），并强制写路径 fsync（L182–184）。读侧 PyTorch 2.6 的 `FileSystemReader` **无并发参数、逐文件串行读**（源码 TODO 注明无 offset 排序与缓存，[filesystem.py L617–674](https://github.com/pytorch/pytorch/blob/1eba9b3aa3c43f86f4a2c807ac8e12c4a7767340/torch/distributed/checkpoint/filesystem.py#L617-L674)），`torch.load` 到 CPU 后 `copy_` 进目标张量（含 H2D）——恢复慢时先区分读、反序列化与 H2D | 只读 | 后端慢/读路径慢被区分 | 进步骤 6 |
| 6 | MindIO ACP 分支（昇腾栈）：`save(open_way='memfs')` 的返回值区分失败/原生 torch.save/memfs/fopen（[save接口.md](https://github.com/Ascend/mind-cluster/blob/44385c13d7b1d87def35f1604e8be4d16de6ca4e/component/mindio/acp/doc/Interface_description/save%E6%8E%A5%E5%8F%A3.md)）；内存暂存到后端持久化的完成信号是 `flush()`——等待后台异步刷盘全部成功，返回 0/1，**无超时与部分失败语义**（[flush接口.md](https://github.com/Ascend/mind-cluster/blob/44385c13d7b1d87def35f1604e8be4d16de6ca4e/component/mindio/acp/doc/Interface_description/flush%E6%8E%A5%E5%8F%A3.md)）。memfs 的内部实现与性能数据未公开核对；ACP 无性能/并发调节环境变量 | 只读 | “保存返回快但 flush 慢”说明慢在后端异步写入 | 与步骤 4/5 对齐后端证据 |
| 7 | 汇总：阶段、证据、反例与未知 | 无 | 结论回链到阶段与配置 | 满足完成判据后结束 |

## 停止条件与恢复安排

- 不为提速直接关闭 `sync_files` 或调大 dirty 参数：前者牺牲故障一致性，后者改变整机写行为；任何内核/配置变更需授权与回滚计划。
- 保存期间频繁失败或后端报错时先保存证据（配置、时间线、后端日志），再决定是否重试；不完整的 checkpoint 产物按[持久化边界](checkpoint-durability.md)的提交语义处理，不直接删改。
- 压测类验证（如 MLPerf 流程）需在隔离环境执行；其规则的清缓存、fsync 强制与“无需真实加速器”边界不等同于本环境的训练保存验证。

## 完成判据

以下任一结果可以结束本轮诊断：

1. 慢被定位到具体阶段（staging 拷贝/序列化/集合同步点/写线程/fsync/内核节流/后端/读路径之一），且有该阶段与相邻阶段同时窗口的证据；
2. 证明是测量口径问题（页缓存热读、方法级总耗时误当分阶段、训练停顿误当后台慢）；
3. 单变量配置变更（thread_count、staging 缓存、保存并发窗口）稳定改变保存耗时，且完成语义未降级；
4. 证据不足，但已记录缺失的阶段计时、内核计数或后端证据，结论保持 `unknown`。

“保存成功”不单独满足完成判据；“变快了”需要说明变的是哪个阶段。

## 来源与验证记录

- [PyTorch 2.6 DCP 文档](https://docs.pytorch.org/docs/2.6/distributed.checkpoint.html)与固定 v2.6.0 源码：async_save 的 staging 位置、CPU 后端要求、集合点、writer/reader 参数与已知性能陷阱。
- [Linux kernel v6.16 vm.rst（固定 commit）](https://github.com/torvalds/linux/blob/038d61fd642278bab63ee8ef722c50d10ab01e8f/Documentation/admin-guide/sysctl/vm.rst)：dirty/writeback 与写者节流；[fsync(2)（man-pages 6.19）](https://man7.org/linux/man-pages/man2/fsync.2.html)。
- [MindIO ACP 接口文档（MindCluster v26.1.1 固定 commit）](https://github.com/Ascend/mind-cluster/tree/44385c13d7b1d87def35f1604e8be4d16de6ca4e/component/mindio)：save/multi_save/flush/register_checker/load 与环境变量。
- [MLPerf Storage v2.0 规则](https://github.com/mlcommons/storage/blob/7e71ca162d8f9e7ae4b5b698d7d79b0883817f25/Submission_guidelines.md)：checkpointing 负载的清缓存、fsync 与测量边界。
- [PyTorch 异步保存教程](https://docs.pytorch.org/tutorials/recipes/distributed_async_checkpoint_recipe.html)（动态页，2026-09-30 观察）：仅限定引用其 2.6 适用部分（CPU buffer、staging 阻塞、单异步请求建议）；页面已并入 2.9 的 DefaultStager 内容，不能当作 2.6 功能。
- 逐条主张与证据定位见[第十批 checkpoint I/O 来源记录](../../docs/research/batch-10-checkpoint-io-sources.md)。
- 当前验证范围：来源核对；未执行保存、恢复或存储压测。
- 待确认：网络文件系统/RDMA/对象存储的传输证据；DCP loader 集合调用行号；MindIO memfs 实现与性能数据；目标存储的实测基线。
