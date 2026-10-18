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
  - src.kernel.docs-nfs-v6.16
  - src.nfs-utils.nfs-5-man7
  - src.nfs-utils.exports-5-man7
  - src.ietf.rfc-8881
  - src.ceph.docs-rgw-s3-squid
  - src.ceph.docs-health-checks-squid
  - src.lustre.ops-manual-2x
  - src.kernel.admin-guide-ext4-v6.16
updated_at: "2026-10-18"
summary: 把 checkpoint 保存/恢复慢定位到状态收集、staging 拷贝、后台写入、内核 writeback/fsync、存储后端或读路径；以 PyTorch 2.6 DCP 与 MindIO ACP 为固定样板；NFS/RGW/Lustre 后端支路按各自版本化参考分列入口，RDMA 保留证据缺口。
related_ids:
  - data-storage.checkpoint-durability
  - training.checkpoint-state-consistency
  - data-storage.training-data-path
  - reliability.evidence-and-hypotheses
  - data-storage.local-and-shared-storage
  - data-storage.object-and-parallel-storage
  - data-storage.artifact-transfer-and-publication
  - data-storage.checkpoint-integrity-evidence
  - data-storage.storage-workload-baselines
  - data-storage.storage-client-backend-recovery
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
  notes: "已核对 DCP async_save/staging/writer/reader 实现、Linux vm.rst 的 dirty/writeback 语义、MindIO ACP 接口文档与 MLPerf checkpointing 规则；未执行保存、恢复或存储压测。2026-10-18（T04-08 补交）复用登记版本化后端来源（内核 v6.16 NFS、nfs(5)/exports(5)、RFC 8881、Squid RGW S3 与健康检查、Lustre 2.x 手册、admin-guide/ext4），新增后端支路入口节并收窄缺口声明；本轮未重取上游页面，新增条目以 T04-02/03/06/07 已核对口径与初审及定向复核（B21-C35–C59）修订为准；未运行任何工具。"
---

# Checkpoint 慢写与恢复 I/O 诊断指南

## 目标与触发条件

触发：checkpoint 保存耗时变长或阻塞训练、恢复（读取）慢、保存期间训练步出现周期性停顿。本流程把“慢”定位到具体阶段：**状态收集 → staging（设备到主机/主机内存拷贝，默认实现下在主线程）→ 后台写入（含序列化）→ 内核页缓存与 fsync → 存储后端 →（恢复侧）读与反序列化**。各层的完成语义见[Checkpoint 写入与持久化边界](checkpoint-durability.md)；恢复后状态正确性属 [06](../06-training/checkpoint-state-consistency.md)，不在本文范围。

## 适用范围与前置条件

证据样板：PyTorch 2.6 DCP（文档 + v2.6.0 固定源码）、MindCluster v26.1.1 的 MindIO ACP、Linux kernel v6.16 的 vm 文档（固定 commit）、MLPerf Storage v2.0。进入排查前固定：框架与 writer/stager 实现及版本、`sync_files`/`thread_count`/`single_file_per_rank`/staging 配置、同步或异步保存、存储后端类型、内核 dirty 参数、每次保存的数据量与分片数。

**缺口声明（2026-10-18 更新）**：NFS、Ceph RGW、Lustre 的后端语义已有版本化参考，支路入口见「后端支路入口」节；仍无已核对来源的支路只能按现场证据处理，包括：RDMA 传输行为、NFS/RGW 传输选项层行为（如 rsize/wsize/proto、RGW HTTP 前端）、RGW 性能计数器/官方负载基准与日志端点、NFS 客户端 mountstats、Lustre 计数器其余含义与精确小版本（完整清单见[来源记录](../../docs/research/batch-21-t04-08-sources.md)）；DCP 2.6 的 `dcp_logger` 只有方法级总耗时，没有分阶段计时，阶段拆分需自行打点。

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

## 后端支路入口与同窗计时对齐

步骤 5 定位到后端/读侧支路后，按实现进入各自入口；以下只列入口与边界，不给跨后端的统一调参命令。语义细节按各实现的版本化参考核对（NFS/ext4 见[本地与共享存储](local-and-shared-storage.md)，RGW/Lustre 见[对象与并行存储](object-and-parallel-storage.md)，恢复流程见[存储客户端、后端异常与恢复验证](storage-client-backend-recovery.md)）；Lustre 条目限 LTS 2.15.x 及以前引入的特性（见[对象与并行存储 §1](object-and-parallel-storage.md)）。

| 实现 | 写路径慢/失败的特征入口 | 读侧与缓存 | 元数据 vs 数据瓶颈 | 争用观察点 | 空间压力 |
|---|---|---|---|---|---|
| 本地 ext4 | commit 窗口（默认 5 s）内元数据变更可丢；`data=` 三模式与 `barrier` 决定写入路径（[admin-guide/ext4](https://www.kernel.org/doc/html/v6.16/admin-guide/ext4.html)）；步骤 4 的内核 writeback 节流适用 | 页缓存污染读测量（见步骤 5）；冷基线方法见[本地与共享存储 §5](local-and-shared-storage.md) | 默认内部日志时数据与日志同一设备；外部日志设备（`journal_dev`/`journal_path`）例外（[admin-guide/ext4](https://www.kernel.org/doc/html/v6.16/admin-guide/ext4.html)） | 同机其他负载共用设备，按现场计数器 | inode/空间耗尽无已核对来源（unknown） |
| NFSv4.1 | 客户端 fsync/close 慢可能在对端：WRITE 可带 UNSTABLE4，须 COMMIT＋比对 write verifier（[RFC 8881 §18.32](https://datatracker.ietf.org/doc/html/rfc8881#section-18.32)/[§18.3](https://datatracker.ietf.org/doc/html/rfc8881#section-18.3)）；导出 `async` 允许落盘前应答——违反 NFS 协议，异常重启可丢数据/损坏（[exports(5)](https://man7.org/linux/man-pages/man5/exports.5.html)），Checkpoint 发布要求导出 `sync`（见[本地与共享存储 §3/§4](local-and-shared-storage.md)）；grace 期服务器须以 NFS4ERR_GRACE 拒绝 READ/WRITE 与非 reclaim 锁请求，除非能保证安全（[§8.4.2.1](https://datatracker.ietf.org/doc/html/rfc8881#section-8.4.2.1)）；`hard`/`soft` 超时行为见 [nfs(5)](https://man7.org/linux/man-pages/man5/nfs.5.html) | CTO/缓存窗口见[本地与共享存储 §3](local-and-shared-storage.md)（v3 语境叙述，v4 unknown 沿用）；冷/热基线见[同页 §5](local-and-shared-storage.md)（本机 drop_caches；属性/目录项缓存与 v4 委托是否随之失效 unknown；服务器侧 unknown） | pNFS（[RFC 8881 §12](https://datatracker.ietf.org/doc/html/rfc8881#section-12)，OPTIONAL）在协议层分离 metadata server 与 storage devices，客户端 pNFS 范围 unknown（见[本地与共享存储 §3](local-and-shared-storage.md)）；非 pNFS 部署由同一服务器处理元数据与数据操作 | 服务器侧统计 [knfsd-stats](https://www.kernel.org/doc/html/v6.16/filesystems/nfs/knfsd-stats.html)（线程池饱和信号，无请求字节/延迟） | 服务器侧空间证据 unknown |
| Ceph RGW（S3） | multipart 上传中断按 upload-id 列举残留分片；upload-id 不匹配返 404 NoSuchUpload；Complete 前后的可见性与列举一致性 unknown（见[对象与并行存储 §2](object-and-parallel-storage.md)）；已登记来源内没有 RGW 逐操作计数器，暂按客户端计时＋网络/后端证据判定 | 读/条件请求条目见同页 §2；`GET /?usage` 为用量统计、非性能计数器；冷/热基线入口 unknown | bucket 索引 resharding 条目见同页 §1，细节 unknown | 争用观察入口 unknown（`GET /?usage` 非性能计数器） | 池满 OSD_FULL/NEARFULL/POOL_FULL（[health-checks](https://docs.ceph.com/en/squid/rados/operations/health-checks/)） |
| Lustre 2.x | 写带宽受条带布局影响（手册 §19.2 Striping Considerations；布局设/查用 `lfs setstripe`/`getstripe`，§19.3/§19.4）；`BAD WRITE CHECKSUM` 日志为 32-bit 传输校验、ldiskfs 无持久校验（§23.5.1）；校验和不匹配时客户端 re-read/re-write 至多五次（§23.5.1），初始建联超时见 Ch.35.3.8 | 页缓存/客户端缓存语义以手册为准（细分 unknown）；冷/热基线入口 unknown | MDT 元数据瓶颈与 OST 数据带宽瓶颈分开观测（§1.2.2）；Jobstats（Ch.12）/brw_stats（Ch.39）入口 | 同文件多写锁争用（§34.10）；Jobstats 按作业操作计数（Ch.12） | Full OST 禁建与数据迁移（§23.1）；`lfs df` |

同窗计时对齐例子（保存路径，固定实现锚点，均未执行）：同一时钟口径下同窗采集——①主线程与后台的分界（`async_save` 语境；同步 `save` 全程在调用线程执行，无 staging 与后台段之分，保存调用点停顿即全部）：状态收集与 staging 拷贝在主线程（staging 阻塞语义见步骤 2）；序列化在后台 save 内执行（自 [state_dict_saver.py L234](https://github.com/pytorch/pytorch/blob/1eba9b3aa3c43f86f4a2c807ac8e12c4a7767340/torch/distributed/checkpoint/state_dict_saver.py#L234) 提交；写线程侧见 [filesystem.py L263](https://github.com/pytorch/pytorch/blob/1eba9b3aa3c43f86f4a2c807ac8e12c4a7767340/torch/distributed/checkpoint/filesystem.py#L263)、planner 侧见 [default_planner.py L148](https://github.com/pytorch/pytorch/blob/1eba9b3aa3c43f86f4a2c807ac8e12c4a7767340/torch/distributed/checkpoint/default_planner.py#L148)）；保存调用点停顿区间与后台完成分别打点；②后台：DCP 后台写 Future 的完成时间，或 MindIO `flush()` 返回点（步骤 6）；③内核层：同窗 dirty/writeback 计数与节流迹象（步骤 4）；④后端：同窗后端入口，各实现给出的量不同——knfsd-stats 只有服务器线程池排队/唤醒计数（饱和信号），Ceph health 为状态检查，两者都没有请求字节/延迟；Lustre Jobstats/brw_stats 给操作计数与 I/O 时间分布；NFS/RGW 的后端逐操作字节/延迟无已登记来源（unknown）；⑤读侧（恢复慢时）：读带宽、反序列化耗时与 H2D 传输分开计时（区分见步骤 5），并标注缓存冷/热状态。**异步重叠不能简单相加**：默认 `BlockingAsyncStager` 下 staging 在主线程阻塞完成、先于后台 save（[state_dict_saver.py L229–248](https://github.com/pytorch/pytorch/blob/1eba9b3aa3c43f86f4a2c807ac8e12c4a7767340/torch/distributed/checkpoint/state_dict_saver.py#L229-L248)），与后台 save 重叠的是后续训练步；只有自定义 stager 把 staging 做成非阻塞、且 `should_synchronize_after_execute=False`（协议默认 True；为 True 时 saver 在返回 Future 前调用 `synchronize_staging()`）时，staging 才可能与前/反向计算重叠（协议 docstring 的重叠例子正是如此，[staging.py L37/L72/L116](https://github.com/pytorch/pytorch/blob/1eba9b3aa3c43f86f4a2c807ac8e12c4a7767340/torch/distributed/checkpoint/staging.py#L37-L116)）；内核 writeback 与应用写的重叠同理。各阶段耗时之和可以大于 wall-clock；判定用关键路径——主线程停顿区间与 Future/flush 完成点，分段耗时用于定位候选，不累加定罪。DCP `dcp_logger` 仅方法级总耗时（见缺口声明），分阶段须自行打点；fio 的 slat/clat 拆分只用于独立基线工具（见[存储负载基线 §4](storage-workload-baselines.md)），不是保存路径内的计时来源。

定位后的接续：独立基线与隔离/争用/冷热对照口径见[存储负载、容量与长尾基线口径](storage-workload-baselines.md)；后端异常的定位链、repair/remount/回放分支与恢复完成判据见[存储客户端、后端异常与恢复验证](storage-client-backend-recovery.md)；制品暂存/提交/读回验证协议见[模型制品与 Checkpoint 的传输、发布和读回](artifact-transfer-and-publication.md)；RDMA 传输行为仍无已核对来源（unknown）。

## 停止条件与恢复安排

- 不为提速直接关闭 `sync_files`、调大 dirty 参数或改用 NFS 导出 `async`：前者牺牲故障一致性，dirty 参数改变整机写行为，导出 `async` 违反 NFS 协议且异常重启可丢数据/损坏（[exports(5)](https://man7.org/linux/man-pages/man5/exports.5.html)；Checkpoint 发布要求导出 `sync`，见[本地与共享存储 §4](local-and-shared-storage.md)）；任何内核/配置变更需授权与回滚计划。
- 保存期间频繁失败或后端报错时先保存证据（配置、时间线、后端日志），再决定是否重试；不完整的 checkpoint 产物按[持久化边界](checkpoint-durability.md)的提交语义处理，不直接删改。
- 压测类验证（如 MLPerf 流程）需在隔离环境执行；其规则的清缓存、fsync 强制与“无需真实加速器”边界不等同于本环境的训练保存验证。

## 完成判据

以下任一结果可以结束本轮诊断：

1. 慢被定位到具体阶段（staging 拷贝/序列化/集合同步点/写线程/fsync/内核节流/后端/读路径之一），且有该阶段与相邻阶段同时窗口的证据；
2. 证明是测量口径问题（页缓存热读、方法级总耗时误当分阶段、训练停顿误当后台慢）；
3. 单变量配置变更（thread_count、staging 缓存、保存并发窗口）稳定改变保存耗时，且完成语义未降级；
4. 证据不足，但已记录缺失的阶段计时、内核计数或后端证据，结论保持 `unknown`。

“保存成功”不单独满足完成判据；“变快了”需要说明变的是哪个阶段。定位到后端支路或做过受控对照时，完成记录还须同时包含：制品身份（保存 ID、清单与哈希，见[完整性证据](checkpoint-integrity-evidence.md)与[传输发布](artifact-transfer-and-publication.md)）、作业进展（保存后训练 step 恢复；恢复场景的首批/持续窗口）、完整性（读回校验结论）、时延/吞吐与资源代价（对照前后同窗）。

## 来源与验证记录

- [PyTorch 2.6 DCP 文档](https://docs.pytorch.org/docs/2.6/distributed.checkpoint.html)与固定 v2.6.0 源码：async_save 的 staging 位置、CPU 后端要求、集合点、writer/reader 参数与已知性能陷阱。
- [Linux kernel v6.16 vm.rst（固定 commit）](https://github.com/torvalds/linux/blob/038d61fd642278bab63ee8ef722c50d10ab01e8f/Documentation/admin-guide/sysctl/vm.rst)：dirty/writeback 与写者节流；[fsync(2)（man-pages 6.19）](https://man7.org/linux/man-pages/man2/fsync.2.html)。
- [MindIO ACP 接口文档（MindCluster v26.1.1 固定 commit）](https://github.com/Ascend/mind-cluster/tree/44385c13d7b1d87def35f1604e8be4d16de6ca4e/component/mindio)：save/multi_save/flush/register_checker/load 与环境变量。
- [MLPerf Storage v2.0 规则](https://github.com/mlcommons/storage/blob/7e71ca162d8f9e7ae4b5b698d7d79b0883817f25/Submission_guidelines.md)：checkpointing 负载的清缓存、fsync 与测量边界。
- 2026-10-18（T04-08 补交）加法：后端支路入口节复用已登记版本化来源——[Linux v6.16 NFS 内核文档](https://www.kernel.org/doc/html/v6.16/filesystems/nfs/index.html)、[nfs(5)](https://man7.org/linux/man-pages/man5/nfs.5.html) 与 [exports(5)](https://man7.org/linux/man-pages/man5/exports.5.html)、[RFC 8881](https://datatracker.ietf.org/doc/html/rfc8881)（§18.3/§18.32/§8.4.2.1/§12）、[Ceph Squid RGW S3](https://docs.ceph.com/en/squid/radosgw/s3/) 与 [health-checks](https://docs.ceph.com/en/squid/rados/operations/health-checks/)、[Lustre 2.x 手册](https://doc.lustre.org/lustre_manual.xhtml)、[admin-guide/ext4](https://www.kernel.org/doc/html/v6.16/admin-guide/ext4.html)；逐条 revision/许可与未覆盖范围见[第二十一批 T04-08 来源记录](../../docs/research/batch-21-t04-08-sources.md)。本轮未重取上游页面、未运行任何工具或压测。
- [PyTorch 异步保存教程](https://docs.pytorch.org/tutorials/recipes/distributed_async_checkpoint_recipe.html)（动态页，2026-09-30 观察）：仅限定引用其 2.6 适用部分（CPU buffer、staging 阻塞、单异步请求建议）；页面已并入 2.9 的 DefaultStager 内容，不能当作 2.6 功能。
- 逐条主张与证据定位见[第十批 checkpoint I/O 来源记录](../../docs/research/batch-10-checkpoint-io-sources.md)。
- 当前验证范围：来源核对；未执行保存、恢复或存储压测。
- 待确认：RDMA 传输证据；NFS/RGW 传输选项层行为（如 rsize/wsize/proto、RGW HTTP 前端）；RGW 性能计数器/官方负载基准与日志端点；NFS 客户端 mountstats；Lustre 计数器其余含义与精确小版本；DCP loader 集合调用行号；MindIO memfs 实现与性能数据；目标存储的实测基线（未执行）。
