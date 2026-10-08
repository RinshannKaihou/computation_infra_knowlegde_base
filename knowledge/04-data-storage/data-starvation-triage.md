---
id: data-storage.data-starvation-triage
title: 训练数据加载饥饿诊断指南
type: procedure
domain: data-storage
status: draft
platforms: [generic]
source_refs:
  - src.pytorch.data-loader-2.6
  - src.pytorch.dataloader-source-v2.6.0
  - src.pytorch.profiler-2.6
  - src.pytorch.cuda-semantics-2.6
  - src.mlcommons.storage-rules-v2.0
updated_at: "2026-09-30"
summary: 把“训练在等数据”定位到存储、CPU 处理、组 batch、主机队列、设备传输或训练消费中的首个边界；以 PyTorch 2.6 DataLoader 与 profiler 为可核对实现样板，区分配置错误、worker 硬失败和真实供给不足。
related_ids:
  - data-storage.training-data-path
  - reliability.evidence-and-hypotheses
  - hardware.resource-topology
  - training.parallelism-and-state
applicability:
  environment_refs: []
  notes: "流程以 PyTorch 2.6 的 DataLoader 文档与固定 v2.6.0 源码为证据样板；目标环境的框架、存储实现、CPU/NUMA/设备拓扑与版本仍需补齐，其他框架的同名概念不能照搬参数语义。"
verification:
  status: source_checked
  evidence_refs:
    - src.pytorch.data-loader-2.6
    - src.pytorch.dataloader-source-v2.6.0
    - src.pytorch.profiler-2.6
  notes: "已核对 PyTorch 2.6 data.html 参数语义、v2.6.0 固定 dataloader.py 的 worker 错误/超时/prefetch/record_function 实现和 profiler.html 的观测能力；未在真实环境执行训练、profiling 或变更验证。"
---

# 训练数据加载饥饿诊断指南

## 目标与触发条件

本流程回答“训练为什么在等数据，等待位于哪一段”。典型触发：step 时间变长或波动、设备利用率采样间歇走低、训练日志中取 batch 等待增加。这些症状不直接等于存储慢——等待可能发生在存储、缓存、CPU 解码、组 batch、主机队列、设备传输或训练消费本身，分层框架见[训练数据供给路径与等待](training-data-path.md)。

目标是找到**首个不能按时完成的边界**，并用它上下游同时成立的证据支持结论；不是把任一上游阶段的耗时总和当作根因。

## 适用范围与前置条件

本流程是 generic 诊断结构；可核对的实现证据固定为 **PyTorch 2.6** 的 DataLoader 文档与 v2.6.0 源码（commit `1eba9b3aa3c43f86f4a2c807ac8e12c4a7767340`）。其他框架、其他 PyTorch 版本、NPU 后端传输语义需按各自版本资料另行核对。进入排查前至少固定：

- 框架与 DataLoader 配置：`num_workers`、`prefetch_factor`、`persistent_workers`、`timeout`、`pin_memory`、`in_order`、数据集类型（map-style / iterable-style）；
- 训练作业身份、rank 映射、数据格式与访问模式、存储类型（本地/共享/对象）与缓存层；
- 同一时钟口径下的训练步时间线采集手段（profiler 或等价的步骤计时）；
- 是否为生产作业，以及是否有采集、重启 worker 配置或修改训练参数的授权。

## 需要的证据

| 证据 | 采集范围或定位 | 用途 | 缺失时如何处理 |
|---|---|---|---|
| DataLoader 配置与版本 | 训练入口参数、框架版本 | 决定哪些语义适用（如 prefetch_factor 默认值随 num_workers 变化） | 配置未知时只做症状描述，不套默认语义 |
| 取 batch 等待的直接证据 | profiler trace 或训练循环计时；PyTorch 中 DataLoader 迭代的 record_function 区间 | 确认等待确实在取 batch，而不是计算/通信空档 | 没有直接证据时不能进入数据路径归因 |
| worker 进程状态与错误 | 主进程异常文本、worker 退出码、系统日志 | 区分“worker 死了”与“worker 慢” | 只有训练侧超时报错时保留两种候选 |
| 存储后端指标 | 同窗口的字节/IOPS/延迟/排队/重试 | 验证存储支路 | 应用等待但无后端请求证据时不能定为存储 |
| 主机 CPU/内存/FD | worker 进程的 CPU 时间、内存增长、FD 用量 | 验证 CPU 处理与资源耗尽支路 | 主机总 CPU 百分比不足以区分单核/锁竞争 |
| 队列与预取深度 | **下一顺位 batch 是否就绪**、可交付队列为空的持续时间 | 区分瓶颈在供给上游还是下游背压 | 只看平均深度会掩盖短暂耗尽；PyTorch 默认按序返回，缓冲占用高不等于可交付（见步骤 5） |
| 设备传输与消费时间线 | 设备侧事件、步骤边界 | 区分传输瓶颈与训练自身空档 | 无设备时间线时不排除计算/通信支路 |

## 步骤与判断分支

| 步骤 | 检查或动作 | 运行影响 | 预期证据与解释 | 下一步 |
|---|---|---|---|---|
| 1 | 冻结窗口：记录环境、DataLoader 配置、异常 step 区间与受影响 rank | 只读 | 获得可复核的版本与配置身份 | 配置缺失先补齐，不先调参 |
| 2 | 确认等待在取 batch：PyTorch 2.6 的 profiler 中，DataLoader 每次 `__next__` 被包在 record_function 区间 `enumerate(DataLoader)#_MultiProcessingDataLoaderIter.__next__`（或 SingleProcess 变体）里，可在 trace/key_averages 中直接观测 | profiling 增加运行与存储开销；`record_shapes=True` 会临时持有 tensor 引用 | 该区间占关键路径才支持“数据等待”；否则转向计算/通信排查 | 确认后进入步骤 3；未确认则转向[训练全流程](../00-overview/training-lifecycle.md)定位真实空档 |
| 3 | 核对 worker 模型配置是否本身有误：`num_workers=0` 表示主进程加载、会阻塞计算；`prefetch_factor` 是每 worker 预取 batch 数（`num_workers>0` 时默认 2，合计预取 `2*num_workers`）；`persistent_workers=True` 让 worker 跨 epoch 存活；`in_order=False` 不保证 FIFO 且可能倾斜数据分布 | 只读核对 | 配置与预期不符是独立修复项，不需要先找存储原因 | 修正配置后回到基线比较；配置合理则进入步骤 4 |
| 4 | 区分硬失败与慢：PyTorch v2.6.0 主进程在 worker 本应存活却不存活时抛 `RuntimeError("DataLoader worker (pid(s) …) exited unexpectedly")`；`timeout>0` 时收集 batch 超时抛 `RuntimeError("DataLoader timed out after … seconds")`；pin memory 线程死亡抛 `RuntimeError("Pin memory thread exited unexpectedly")`；Linux 上 FD 耗尽抛 `RuntimeError("Too many open files. Communication with the workers is no longer possible…")`；worker 内 dataset/collate 异常被包装传回主进程 reraise | 只读日志 | 任一硬错误直接指向对应支路（worker 崩溃原因、timeout 配置、FD 上限、数据/变换缺陷） | 命中硬错误则修复对应支路；无硬错误进入步骤 5 |
| 5 | 慢而无错：按[数据路径](training-data-path.md)的阶段表定位首个边界——**下一顺位 batch 未就绪**且与输入等待重合，瓶颈在供给上游；注意 PyTorch 2.6 默认按序返回，乱序先完成的结果会等待队首（dataloader.py L1449–1480），不能把中间缓冲占用读作消费侧已满；可交付队列长期满才指向消费者或更下游；再结合存储后端延迟、worker 产出率、CPU 处理耗时分别验证存储/缓存/解码/组 batch 支路 | 采集指标通常低影响；主动压测不在本流程 | 某阶段耗时先升高、其下游随后等待，支持该阶段为瓶颈 | 定位后进入步骤 6 的受控对照 |
| 6 | 受控对照：一次只改一个因素（worker 数、prefetch_factor、persistent_workers、pin_memory、缓存、数据格式），比较同窗口的取 batch 等待、吞吐与资源代价 | 改变训练运行参数；需授权与回滚计划 | 单变量改变稳定移动等待位置，支持该支路 | 不满足判据则保留未知，不叠加多个变更 |
| 7 | 汇总事实、推断、反证和未知项 | 无 | 每个结论能回链到阶段、窗口与实体 | 满足完成判据后结束 |

关键版本语义补充（PyTorch 2.6 文档与固定源码）：

- `timeout=0` 的具体含义文档未写；固定源码显示 0 为禁用超时，主进程按 5 秒周期（`MP_STATUS_CHECK_INTERVAL`）循环收数并检查 worker 存活；`num_workers=0` 下设正 timeout 会触发断言（文档未写）。引用时区分“文档语义”与“源码行为”（[dataloader.py L1389–1422](https://github.com/pytorch/pytorch/blob/1eba9b3aa3c43f86f4a2c807ac8e12c4a7767340/torch/utils/data/dataloader.py#L1389-L1422)、[L743](https://github.com/pytorch/pytorch/blob/1eba9b3aa3c43f86f4a2c807ac8e12c4a7767340/torch/utils/data/dataloader.py#L743)、[`_utils/__init__.py` L20](https://github.com/pytorch/pytorch/blob/1eba9b3aa3c43f86f4a2c807ac8e12c4a7767340/torch/utils/data/_utils/__init__.py#L20)）。
- worker 崩溃错误与 SIGCHLD/手动检查机制见 [dataloader.py L1238–1266](https://github.com/pytorch/pytorch/blob/1eba9b3aa3c43f86f4a2c807ac8e12c4a7767340/torch/utils/data/dataloader.py#L1238-L1266)；FD 耗尽错误与缓解建议（`ulimit -n` 或 `set_sharing_strategy('file_system')`）见 [L1280–1320](https://github.com/pytorch/pytorch/blob/1eba9b3aa3c43f86f4a2c807ac8e12c4a7767340/torch/utils/data/dataloader.py#L1280-L1320)，仅 Linux 语境。
- record_function 区间名见 [dataloader.py L680、L703–704](https://github.com/pytorch/pytorch/blob/1eba9b3aa3c43f86f4a2c807ac8e12c4a7767340/torch/utils/data/dataloader.py#L680-L704)；profiler 的 activities、schedule（wait/warmup/active/repeat）、on_trace_ready、export_chrome_trace（只导出最后一个 cycle）、key_averages、profile_memory 语义见 [torch.profiler 文档](https://docs.pytorch.org/docs/2.6/profiler.html)。
- profiler 文档的 `ProfilerActivity` 枚举含 `PrivateUse1`，但页面没有 NPU 字样或任何 PrivateUse1 使用说明；NPU 侧的 profiling 能力（如 torch_npu 的 profiler）本文未核对，不能假设与 CUDA 路径一致。
- `pin_memory=True` 的“加速主机到设备传输”是 CUDA 语境语义；固定源码中空 `pin_memory_device` 默认走 CUDA 可用性判断（[dataloader.py L657–669](https://github.com/pytorch/pytorch/blob/1eba9b3aa3c43f86f4a2c807ac8e12c4a7767340/torch/utils/data/dataloader.py#L657-L669)）。NPU 的内存注册与异步传输语义需按 TorchNPU/CANN 对应版本核对，见[昇腾 NPU 内存与 OOM 证据](../02-software-stack/ascend-memory-oom-evidence.md)的版本边界。

## 停止条件与恢复安排

出现以下任一情况时停止主动试探，先保存证据：

- worker 反复崩溃、FD 或主机内存接近耗尽，继续运行会影响同机其他任务；
- 需要修改生产训练的 worker 数、缓存或数据格式，但尚无变更授权与回滚计划；
- 指标口径、时钟或 rank 映射无法保持一致，继续采集只会产生不可比较证据。

做过配置变更的，记录原值与生效时点；验证完成后恢复基线配置，并确认恢复后等待位置与吞吐回到变更前水平或新基线已建立。一次“重启后暂时不卡”不构成完成。

## 完成判据

以下任一结果可以结束本轮诊断：

1. 找到首个不能按时完成的阶段边界（存储/缓存/解码/组 batch/队列/传输/消费之一），并有其上游已就绪、下游随后等待的同时窗口证据；
2. 定位到硬失败支路（worker 崩溃、收集超时、FD 耗尽、pin memory 线程退出、数据/变换异常）并修复后，同窗口取 batch 等待消除且吞吐恢复；
3. 单变量对照稳定改变了预定义的等待或吞吐观测；
4. 证据不足，但已明确记录缺失的版本、窗口、队列或后端证据，结论保持 `unknown`。

“命令成功”“worker 数调大后好像快了”或“利用率回升”均不单独满足完成判据；需要同窗口的等待位置与吞吐证据。

## 来源与验证记录

- [torch.utils.data — PyTorch 2.6](https://docs.pytorch.org/docs/2.6/data.html)：num_workers、prefetch_factor、persistent_workers、timeout、pin_memory、in_order 的文档语义；worker 内存放大 Warning（worker 消耗约等于父进程被访问对象的 CPU 内存，建议非引用计数表示）。
- [PyTorch v2.6.0 固定 dataloader.py](https://github.com/pytorch/pytorch/blob/1eba9b3aa3c43f86f4a2c807ac8e12c4a7767340/torch/utils/data/dataloader.py)：worker 崩溃、超时分支、FD 耗尽、record_function 区间名等文档未覆盖的源码行为。
- [torch.profiler — PyTorch 2.6](https://docs.pytorch.org/docs/2.6/profiler.html)：观测能力与边界（含 PrivateUse1 无说明、export_chrome_trace 只导出最后一个 cycle）。
- [PyTorch 2.6 CUDA semantics](https://docs.pytorch.org/docs/2.6/notes/cuda.html)：仅 pin_memory/non_blocking 的 CUDA 语境对照。
- [MLPerf Storage v2.0 规则](https://github.com/mlcommons/storage/blob/7e71ca162d8f9e7ae4b5b698d7d79b0883817f25/Submission_guidelines.md)：其 AU 用模拟计算且不含预处理与设备传输——不能用该基准的存储结论替代本流程的端到端饥饿判断。
- 逐条主张与证据定位见[第八批数据加载来源记录](../../docs/research/batch-08-dataloader-sources.md)。
- 当前验证范围：来源核对；没有目标环境的训练、profiling 或变更执行记录。
