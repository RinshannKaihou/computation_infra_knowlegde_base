---
id: training.slow-rank-triage
title: 慢 rank 诊断指南
type: procedure
domain: training
status: draft
platforms: [generic]
source_refs:
  - src.pytorch.processgroupnccl-env-2.8
  - src.pytorch.distributed-2.8
  - src.nvidia.nccl-user-guide-2.27.5
  - src.pytorch.profiler-2.6
  - src.nvidia.dcgm-exporter-metrics-latest-2026-09-30
  - src.nvidia.dcgm-field-identifiers-latest-2026-09-30
updated_at: "2026-10-08"
summary: 定位分布式训练中“谁先慢、慢在哪个阶段”：用 rank 进度证据区分从未进入、进入未完成与完成但未加入下一步，再按数据、计算、通信、设备、主机与观测假象分支归因。
related_ids:
  - communication.collectives-and-rank-progress
  - data-storage.data-starvation-triage
  - communication.bandwidth-degradation-triage
  - hardware.health-evidence
  - hardware.power-thermal-evidence
  - reliability.evidence-and-hypotheses
applicability:
  environment_refs: []
  notes: "流程以 PyTorch 2.8（固定 v2.8.0 源码）与 NCCL 2.27.5 归档文档为可核对样板，DCGM latest 页为可变来源；NPU（HCCL/TorchNPU）侧的等价观测能力未核对，目标环境需另行固定版本与工具。"
verification:
  status: source_checked
  evidence_refs:
    - src.pytorch.processgroupnccl-env-2.8
    - src.pytorch.distributed-2.8
    - src.nvidia.nccl-user-guide-2.27.5
  notes: "已核对 PyTorch 2.8 desync/flight recorder/heartbeat/DEBUG 的文档与固定源码语义、NCCL 2.27.5 RAS 页；未运行分布式作业、开启调试开关或采集真实 trace。"
---

# 慢 rank 诊断指南

## 目标与触发条件

集合通信的训练里，一步的耗时由最慢的 rank 决定：其他 rank 在集合点上等待，表现为整体吞吐下降或周期性抖动。本流程回答两个问题：**谁先慢**（找到落后的 rank），**慢在哪个阶段**（数据、计算、通信、设备、主机，还是测量假象）。

触发信号：step 时间变长或波动、通信超时报告（参考 [HCCL](../03-communication/hccl-timeout-triage.md)/[NCCL 超时](../03-communication/nccl-timeout-triage.md) 流程）、监控显示部分设备利用率低。注意：其他 rank 在集合点上的等待是**后果**，只有最早变慢的那个 rank 的局部证据才能指向根因；rank 进度与集合语义见[集合通信与 rank 进度](../03-communication/collectives-and-rank-progress.md)。

## 适用范围与前置条件

可核对证据固定为 **PyTorch 2.8**（文档 + v2.8.0 源码）与 **NCCL 2.27.5** 归档文档；DCGM 指标页为 latest 可变来源（观察日期 2026-09-30）。NPU 侧（HCCL、TorchNPU、MindCluster）的等价慢 rank 观测能力**未核对**——HCCL 超时文档侧重超时分支，desync/flight recorder 等价物是否存在于目标 CANN 版本标为 `unknown`。

进入排查前固定：框架与通信库版本、rank↔进程↔设备↔节点映射、并行布局、是否允许开启调试开关（多数观测开关有性能开销，见各步骤）。

## 需要的证据

| 证据 | 采集范围或定位 | 用途 | 缺失时如何处理 |
|---|---|---|---|
| rank 进度对比 | desync 报告、flight recorder dump、NCCL RAS、超时日志 | 区分“从未进入”“进入未完成”“完成未加入下一步” | 无进度证据时不能把等待归给任一 rank |
| rank 级阶段时间线 | DDP `TORCH_DISTRIBUTED_DEBUG=DETAIL` 统计、每 rank profiler trace | 定位慢在 forward/backward/通信哪一段 | profiler 只有单进程文件，跨 rank 对齐需自行组织（2.6 文档无聚合视图） |
| 数据供给证据 | 见[数据饥饿流程](../04-data-storage/data-starvation-triage.md) | 慢 rank 的数据支路 | 慢 rank 先慢，其他 rank 的“输入等待”是后果 |
| 通信证据 | 见[带宽退化流程](../03-communication/bandwidth-degradation-triage.md)、NCCL_DEBUG_SUBSYS | 通信支路 | 注意口径限定 |
| 设备侧证据 | DCGM 时钟/温度/violation/PCIe replay 等字段 | 设备降速支路 | exporter 默认不导出降频信号，见步骤 5 |
| 主机侧证据 | CPU/内存/GC/存储等待 | 主机阻塞支路 | 主机总 CPU 不足以定位 |

## 步骤与判断分支

| 步骤 | 检查或动作 | 运行影响 | 预期证据与解释 | 下一步 |
|---|---|---|---|---|
| 1 | 对照 NCCL RAS 的 communicator 计数与状态：`ncclras` 连接 localhost:28028，读取 `STATUS`/`VERBOSE STATUS`，同时检查 INCOMPLETE/TIMEOUT/DEAD 等响应完整性。MISMATCH 的成员只在离群组规模 ≤25% 总数且 ≤10 时默认展开；verbose 放宽为 <50% 且取消成员数限制。活跃通信期间计数差异可能是正常瞬态，重复查询不推进也只提示待调查（[RAS Sample Output](https://docs.nvidia.com/deeplearning/nccl/archives/nccl_2275/user-guide/docs/troubleshooting/ras.html#sample-output)） | 只读，RAS 走带外 TCP | 持续差异提供候选 rank；无差异、未展开或响应不完整均不能证明全体变慢，计算/数据阶段落后时 collective 计数可能仍相同 | 有候选进步骤 2；未定时仍补步骤 2–4 的各 rank 阶段时间线；只有阶段证据支持全体变慢，才转[带宽退化](../03-communication/bandwidth-degradation-triage.md)或共享资源排查 |
| 2 | 定位落后 rank 与最后进度：PyTorch 2.8 的 `TORCH_NCCL_DESYNC_DEBUG` 在 watchdog 超时时输出 desync 报告（文档页说明其用于定位 collective desync 的肇事 rank；[文档](https://docs.pytorch.org/docs/2.8/torch_nccl_environment_variables.html)），固定源码的分析逻辑区分三类：从未进入 collective（"never joined any collectives"）、进入但未完成（"joined but didn't finish collective #N"）、完成 #N 但未加入 #N+1（[TraceUtils.h L78–118](https://github.com/pytorch/pytorch/blob/ba56102387ef21a3b04b357e5b183d48f0afefc7/torch/csrc/distributed/c10d/TraceUtils.h#L78-L118)）。或比对 flight recorder dump（按 rank 分文件）各 rank 最后一条 entry 的 seq | 开启调试变量有开销；desync 默认关闭，且开启时若 `TORCH_NCCL_ASYNC_ERROR_HANDLING=0`，源码会**强制把 async error handling 改回开启**并日志提示（[ProcessGroupNCCL.cpp L990–997](https://github.com/pytorch/pytorch/blob/ba56102387ef21a3b04b357e5b183d48f0afefc7/torch/csrc/distributed/c10d/ProcessGroupNCCL.cpp#L990-L997)）；依赖各 rank 向 Store 写 trace key，Store 不可达时报告失败 | 得到落后 rank 及其未完成的 collective | 进步骤 3 |
| 3 | 判读 flight recorder 的时间戳语义：entry 的 `time_discovered_started/completed_ns` 是 **CPU 侧发现时刻**（源码注释明示 "will always be after it actually started"），不是设备真实起止；input/output sizes 与 dtypes 可用于核对失配 | 只读分析 | 用 seq 判断进度可信；用时间差做精细归因时注意 CPU/设备错位 | 进步骤 4 |
| 4 | 阶段归因（DDP 路径）：`TORCH_DISTRIBUTED_DEBUG=DETAIL` 输出**按 rank 分行**的 Avg forward/backward compute、Avg backward comm、comm/comp overlap 统计（[distributed.html #torch-distributed-debug](https://docs.pytorch.org/docs/2.8/distributed.html#torch-distributed-debug)），可直接横向对比慢在哪个阶段；DETAIL 影响性能，仅调试用。需要单点深入时取该 rank 的 profiler trace（2.6 文档仅说明 `tensorboard_trace_handler` 的 `worker_name` 按 `[hostname]_[pid]` 区分，**没有多进程聚合视图**，跨 rank 对齐自行按文件组织） | DETAIL 有性能影响；profiler 增加开销 | 统计指向 compute → 步骤 5 计算/设备支路；指向 comm → 通信支路；指向 backward 前等待 → 数据/上游支路 | 按指向分支 |
| 5 | 计算/设备支路：先查该 rank 的数据供给（[数据饥饿流程](../04-data-storage/data-starvation-triage.md)，慢 rank 先慢、他人等待是后果）；再查设备侧：DCGM 的 SM/MEM 时钟、温度、功耗、violation 计数器（降速证据）、PCIe replay（链路质量）——**exporter 默认不导出 violation 与 clock events 字段，需显式开启**；字段语义见[供电散热证据](../01-hardware/power-thermal-evidence.md) | 只读 | 时钟降档/violation 增量与慢的时间窗口对齐 → 设备降速支路 | 设备正常回步骤 4 其他分支 |
| 6 | 通信支路：`NCCL_DEBUG_SUBSYS=COLL` 打印 collective 调用日志，对类型/大小失配导致的 hang 有用（[distributed.html](https://docs.pytorch.org/docs/2.8/distributed.html)）；带宽类退化按[带宽退化流程](../03-communication/bandwidth-degradation-triage.md)的口径/配置/链路三分支 | 日志量增加 | 失配证据直接指向控制流；口径问题按带宽流程排除 | 排除后保留未知 |
| 7 | 主机阻塞支路：worker 崩溃/FD 耗尽/GC/存储等待（数据流程步骤 4–5）；heartbeat 类问题：PyTorch 2.8 的 `TORCH_NCCL_ENABLE_MONITORING` 监控 **watchdog 线程本身**卡死（典型为 CUDA API 死锁），默认超 `TORCH_NCCL_HEARTBEAT_TIMEOUT_SEC`（480s）abort——注意 2.8 的变量名不是 `TORCH_NCCL_HEARTBEAT_MONITOR`；源码报错文案自认可误报 | 只读为主 | watchdog 卡死与 work 超时是不同机制，证据在监控线程日志 | 按机制分支 |
| 8 | 汇总：每个结论回链到具体 rank、阶段与证据 | 无 | 慢 rank、阶段、证据三者闭合 | 满足完成判据后结束 |

## 停止条件与恢复安排

- `TORCH_DISTRIBUTED_DEBUG=DETAIL`、desync、flight recorder、profiler 都改变运行开销与行为：在生产作业上启用需授权与窗口，验证后恢复。
- `monitored_barrier` **仅支持 GLOO backend**，NCCL 训练中使用需另建 GLOO 组，不能在 NCCL 组上直接调用。
- 发现设备侧降速证据（violation 增量、时钟降档）时转入设备调查，不直接重启作业；thermal/power 的证据边界见[供电散热证据](../01-hardware/power-thermal-evidence.md)。

## 完成判据

以下任一结果可以结束本轮诊断：

1. 定位到具体落后 rank 及其变慢阶段（数据/计算/通信/设备/主机之一），该 rank 的局部证据与其他 rank 的等待时间线一致；
2. 证明是观测口径问题（CPU 侧时间戳、利用率采样、profiler 单文件误读），修正后“慢”消失；
3. 证明是全体性变慢而非个别 rank，转入对应专项（带宽、负载、共享资源）；
4. 证据不足，但已记录缺失的 rank 进度、时间线或设备证据，结论保持 `unknown`。

“重启后暂时正常”不单独满足完成判据。

## 来源与验证记录

- [PyTorch 2.8 NCCL 环境变量文档](https://docs.pytorch.org/docs/2.8/torch_nccl_environment_variables.html)与固定 v2.8.0 源码（`ProcessGroupNCCL.cpp`、`TraceUtils.h`、`FlightRecorder.hpp`）：desync 报告、flight recorder、heartbeat monitoring 的语义与限定。
- [PyTorch 2.8 distributed 文档](https://docs.pytorch.org/docs/2.8/distributed.html)：TORCH_DISTRIBUTED_DEBUG、monitored_barrier、NCCL_DEBUG_SUBSYS。
- [NCCL 2.27.5 RAS](https://docs.nvidia.com/deeplearning/nccl/archives/nccl_2275/user-guide/docs/troubleshooting/ras.html)：MISMATCH 离群组语义、瞬态限定、ncclras 客户端。
- [DCGM exporter 指标页](https://docs.nvidia.com/datacenter/dcgm/latest/reference/dcgm-exporter-metrics.html)与[字段定义页](https://docs.nvidia.com/datacenter/dcgm/latest/dcgm-api/dcgm-api-field-ids.html)（latest 可变，2026-09-30 观察）：设备侧字段与默认导出边界。
- [torch.profiler 2.6](https://docs.pytorch.org/docs/2.6/profiler.html)：分布式场景仅 worker_name 区分的边界。
- 逐条主张与证据定位见[第十批慢 rank 来源记录](../../docs/research/batch-10-slow-rank-sources.md)。
- 当前验证范围：来源核对；未运行分布式作业或开启调试开关。
- 待确认：NPU（HCCL/TorchNPU/MindCluster）侧的等价慢 rank 观测能力；flight recorder 默认值两处口径（PG 2000 vs FR 0）的实际生效路径；RAS 判读的查询次数/间隔阈值（官方未定义）。
