---
id: communication.nccl-timeout-triage
title: NCCL 超时诊断指南
type: procedure
domain: communication
status: draft
platforms: [nvidia]
source_refs:
  - src.nvidia.nccl-user-guide-2.27.5
  - src.pytorch.distributed-2.8
  - src.pytorch.processgroupnccl-env-2.8
updated_at: "2026-10-22"
summary: 首屏提供现象、证据、判断分支与下一项检查，下层保留机制、版本条件与精确来源。从 ProcessGroupNCCL watchdog 或 NCCL hang 回溯同一 communicator 的 rank/sequence 进度，再独立验证上游控制流、GPU、网络与等待预算。
related_ids:
  - communication.collectives-and-rank-progress
  - communication.bandwidth-baselines
  - reliability.evidence-and-hypotheses
  - software-stack.nvidia-documented-profile
applicability:
  environment_refs: []
  notes: "NCCL 诊断机制以 2.27.5 为来源基线，ProcessGroupNCCL 变量以 PyTorch 2.8 为来源基线；目标环境若为其他版本，必须逐项核对变量、RAS、日志字段与默认行为。"
verification:
  status: source_checked
  evidence_refs:
    - src.nvidia.nccl-user-guide-2.27.5
    - src.pytorch.distributed-2.8
    - src.pytorch.processgroupnccl-env-2.8
  notes: "已核对 NCCL 2.27.5 environment、troubleshooting 与 RAS 页面，以及 PyTorch 2.8 distributed/ProcessGroupNCCL 变量页；2026-10-22 定向重核 init_process_group(timeout) 的后端默认值与显式配置边界（IQ-01）。未在 GPU、网络或集群上执行日志采集、RAS 查询、配置修改、通信测试或故障注入。 2026-10-22 增加快速分流与详细依据两层，文档检查记录见 docs/research/triage-guide-usability-2026-10-22.md；未新增现场验证。"
---

# NCCL 超时诊断指南

## 快速分流：先找下一项检查

适用资料基线：NCCL 2.27.5 / PyTorch 2.8；目标版本另核。先记作业 attempt、进程组（group）及 rank→PID/GPU/节点映射；**SeqNum 只在同一 group 内比较**。

| 现象 | 先要哪些证据 | 当前可走的判断分支 | 下一项检查 |
|---|---|---|---|
| 多个 rank 同序号超时，缺一个 rank 的日志 | 全 rank 日志完整性、group 映射 | 参与者未到达或日志缺失；故障数未知 | 补缺失 rank 的前序日志、进程位置及最后完成点；见[步骤 1–3](#步骤与判断分支) |
| 同 group 对齐轨迹后仍有错序/契约冲突 | 最后共同成功点、调用次序、数据量 | 控制流分叉候选；瞬时进度差不足以定性 | 核对同一逻辑操作及首次分叉前的阶段；见[步骤 4A](#步骤与判断分支) |
| watchdog 前已有 CUDA/Xid/device 错误 | 首错时间、rank↔GPU 身份 | 设备/执行支路候选，尚不能确定硬件根因 | 核对事件先后与同设备记录；见[步骤 4B](#步骤与判断分支) |
| 同窗有 NCCL WARN、IB/socket/link 事件 | 实际接口/NIC/rail 与网络事件 | transport 支路候选 | 对齐首错时间与通信路径；见[步骤 4C](#步骤与判断分支) |
| 各 rank 已入队同一操作，仍不完成 | completed 记录、栈、既有 trace/RAS | 入队不证明 GPU 已执行或网络是根因 | 查完成点与上游执行；RAS 仅在已可用时辅助，见[观测边界](#nccl-2275-的观测边界) |
| 怀疑正常操作只是超过等待预算 | 全 rank 契约/持续进展、正常耗时基线、实际 timeout | 预算不足待验证；没有基线则 unknown | 先读初始化配置与 watchdog timeout，满足[步骤 7](#步骤与判断分支)前提后才评估变更 |

**本轮分流的出口**：写出“候选＋支持/反证＋缺失证据＋下一项检查”。缺日志、0% 利用率、timeout 延长或一次跑完，都不能单独确认根因。主动动作的停止条件与恢复要求见[下文](#停止条件与恢复安排)。

## 详细诊断与依据

按需展开：[证据字段](#需要的证据) · [完整分支](#步骤与判断分支) · [PyTorch 观测条件](#pytorch-28-的观测边界) · [完成判据](#完成判据) · [精确来源](#来源与验证记录)。以下保留机制、版本条件与证据范围。

### 目标与触发条件

本流程用于解释 PyTorch ProcessGroupNCCL watchdog timeout、NCCL collective 长时间无完成，或作业在 collective 周围 hang 的事件。目标是把错误行中的 rank、communicator/process group、`SeqNum`、`OpType` 和等待时间放回全 rank 时间线，找到第一个没有进入同一 collective、进入不同操作、上游失败或遇到独立设备/transport 错误的实体。

watchdog timeout 表明等待超过框架预算。它不能单独回答故障发生在控制流、GPU/CUDA、NCCL transport、网络还是等待配置。NCCL 与 HCCL 面对相似的“参与者必须共同前进”问题，但日志字段、RAS、环境变量和 transport 参数各自独立；本流程不使用 HCCL 的错误码、命令或参数。

### 适用范围与前置条件

主要来源分为两层：

- [NCCL 2.27.5 User Guide](https://docs.nvidia.com/deeplearning/nccl/archives/nccl_2275/user-guide/docs/)：NCCL debug、接口/IB 参数、troubleshooting 与 2.24 起的 RAS。
- [PyTorch 2.8 ProcessGroupNCCL Environment Variables](https://docs.pytorch.org/docs/2.8/torch_nccl_environment_variables.html)：watchdog/monitoring、trace buffer、dump-on-timeout、desync debug 和 timing 等框架层观测。

两者不是任意环境的配套声明。特别是 PyTorch 容器 25.01 的文档基线为 PyTorch 2.6.0a0/NCCL 2.25.1；不能直接假定所有 2.27.5 或 PyTorch 2.8 字段存在。进入流程前需固定：

- PyTorch/框架、NCCL、CUDA runtime、driver 和容器 digest/包身份；
- GPU、节点、NIC/fabric、rank 到进程/GPU/节点/NIC 的映射；
- process group/communicator 的成员、创建顺序和 group 内 rank；
- 作业阶段、collective、tensor 元素数/类型、stream 与等待预算；
- 节点时钟、日志文件唯一性、磁盘预算和已有操作授权。

### 需要的证据

| 证据 | 采集范围或定位 | 用途 | 缺失时如何处理 |
| --- | --- | --- | --- |
| 版本与制品 | 每节点/容器的 PyTorch、NCCL、CUDA、driver、框架、镜像 digest | 判断变量、RAS、日志格式与已知限制是否适用 | 版本未知时不设置版本特定变量 |
| communicator/rank 映射 | global/group/local rank 到 PID、GPU、节点、NIC；group 创建顺序 | 限定 `SeqNum` 的比较范围 | 不跨 process group 比较相同序号 |
| watchdog 行 | rank、`SeqNum`、`OpType`、Numel、configured/elapsed timeout、last enqueued/completed（若版本有） | 定位各 rank 等待的逻辑操作 | 保留原字段，不把旧版日志补成新版格式 |
| 全 rank 前序日志/trace | 从共同成功点前到进程退出后 | 找第一分叉、缺 rank、错序或更早异常 | 只有多数 rank 的 timeout 时，把缺失 rank 标为待补采 |
| 进程与上游阶段 | 数据加载、checkpoint、Python/C++ 栈、CUDA kernel、OOM、异常与 launcher | 区分“没调用 collective”和“NCCL 未完成” | GPU 利用率只能作为线索，不能替代栈和事件 |
| GPU/driver | Xid、CUDA fatal、设备丢失、ECC/健康事件及采集状态 | 验证设备支路 | timeout 后的清理错误单独记录为后果候选 |
| transport/网络 | NCCL WARN、socket/IB error、async event、link、NIC/交换路径、接口选择 | 验证 NCCL/网络支路 | 没有同时段独立事件时不下网络根因结论 |
| RAS/flight recorder | 仅在目标版本支持且已预先启用时，保存查询/dump 身份和窗口 | 辅助识别 mismatch、missing process、卡住位置 | 功能不存在或未预置时，不在事故中临时假造历史数据 |

### 步骤与判断分支

| 步骤 | 检查或动作 | 运行影响 | 预期证据与解释 | 下一步 |
| --- | --- | --- | --- | --- |
| 1 | 记录版本、制品、作业阶段、process group、rank/GPU/NIC 映射和当前配置 | 只读；保留进程会占资源，应由现场决定是否终止 | 获得序号与实体的解释边界 | 身份不完整先补齐，不先改 transport |
| 2 | 从 watchdog 行建立 `(group, rank, SeqNum, OpType, Numel, timeout)` 表 | 只读 | 看哪些 rank 在同一操作，哪些缺席或处于别的序号/操作 | 对缺失/不一致 rank 回看前序日志 |
| 3 | 对齐全 rank 的最后共同成功、last enqueued/completed 和最早异常 | 读日志/trace；高详细度 trace 可能增加 I/O，仅使用既有证据 | 找到第一分叉或证明各 rank 仍同序进展 | 进入控制流、设备或 transport 分支 |
| 4A | 缺 rank/错序时，检查该 rank 的数据、计算、checkpoint、Python/C++ 栈、CUDA kernel 和进程状态 | 只读或受控 attach；attach 需现场权限且会有开销，本页不提供命令 | 找到为什么没有在正确时间调用同一 collective | 在上层修复和验证；不以网络参数掩盖 |
| 4B | 有 CUDA/Xid/device 线索时，确认它是否早于 timeout 且映射到同一 rank/GPU | 被动查询；主动诊断另行隔离 | 独立设备事件支持设备首因 | 转设备流程并保存通信级联证据 |
| 4C | 有 NCCL WARN/socket/IB/link 线索时，核对实际接口、NIC/rail 和同时段网络事件 | 网络查询可能需额外权限；不在本流程注入故障 | transport 事件与路径、时间和 rank 对齐才支持网络支路 | 进入网络专项对照；不符则回到进度 |
| 5 | 目标 NCCL ≥2.24 且 RAS 已可用时，查询 job/process/communicator 状态并重复观察 | 官方称 RAS 为低开销，但仍需端口、组件和授权；查询本身不能代替日志 | `MISMATCH` 若持续不变推动 stuck 假设；持续变化可能只是负载不均；`INCOMPLETE` 指向缺进程/连接 | 与 rank 日志交叉验证，不把状态词当根因 |
| 6 | 目标为 PyTorch 2.8 且观测已预配置时，检查 trace/dump/desync/timing | ring buffer、CPP stack 和 dump 会增加内存、日志与时延 | 获得 culprit-rank 候选和 collective 轨迹 | 用源代码/业务阶段验证候选，不直接定责 |
| 7 | 仅在所有 rank 契约一致、仍持续进展且正常耗时分布超过等待预算时评估 timeout | 调整会延迟失败和占用资源；需单变量、回滚和结果校验 | 证明的是等待预算是否合适，不是网络或库已修复 | 完成任务并校验结果，或恢复原值 |
| 8 | 汇总支持、反证和未知项 | 无运行影响 | 结论可回链到 group/rank/sequence/实体/时间 | 满足完成判据后结束 |

#### NCCL 2.27.5 的观测边界

[Environment Variables](https://docs.nvidia.com/deeplearning/nccl/archives/nccl_2275/user-guide/docs/env.html)说明：

- `NCCL_DEBUG` 控制日志级别；`NCCL_DEBUG_FILE` 的文件名应包含 `%h`（hostname）和 `%p`（PID）等唯一身份，否则文件可能被覆盖；`NCCL_DEBUG_SUBSYS` 限定子系统。
- 文档把一组 debug 变量标成不应长期留在生产脚本中的参数，因为可能造成次优行为、崩溃或 hang。排障完成后要按记录撤销。
- `NCCL_SOCKET_IFNAME` 会绕过自动接口选择。设置它是在改变通信路径，不是只读观测；没有接口/拓扑证据时不要试探性批量修改。
- `NCCL_SOCKET_RETRY_CNT` 与 `NCCL_SOCKET_RETRY_SLEEP_MSEC` 自 2.24 起，只描述 socket 建连失败重试。
- `NCCL_IB_TIMEOUT` 控制 InfiniBand verbs local-ack timeout，取值依网络规模；它独立于 PyTorch 进程组的 collective timeout。[PyTorch 2.8 `init_process_group(timeout)`](https://docs.pytorch.org/docs/2.8/distributed.html#torch.distributed.init_process_group) 的 NCCL 后端默认值为 **10 分钟**，其他后端默认 30 分钟；应用可以显式覆盖。调查时读取实际进程组初始化配置与 watchdog 日志中的 timeout，不把默认值或历史案例的 30 分钟当作现场预算。

[NCCL RAS](https://docs.nvidia.com/deeplearning/nccl/archives/nccl_2275/user-guide/docs/troubleshooting/ras.html)自 2.24 起提供运行中查询。官方程序 `ncclras` 及其 `-h`、`-p`、`-v`、`-t` 选项只能在目标版本确实安装该组件、默认或指定端口获准访问时使用。本页不提供一个假定所有环境都可执行的命令行。

#### PyTorch 2.8 的观测边界

[ProcessGroupNCCL 变量页](https://docs.pytorch.org/docs/2.8/torch_nccl_environment_variables.html)明确：

- `TORCH_NCCL_DUMP_ON_TIMEOUT` 依赖 `TORCH_NCCL_TRACE_BUFFER_SIZE > 0`；没有预置 ring buffer 就不会凭空产生历史轨迹。
- `TORCH_NCCL_DESYNC_DEBUG` 帮助识别 desync 的 culprit rank，是调查提示而不是根因裁决。
- `TORCH_NCCL_ENABLE_TIMING`、`TORCH_NCCL_TRACE_CPP_STACK` 和 dump 文件会增加观测开销，应限制窗口和容量。
- `TORCH_NCCL_ENABLE_MONITORING` 与 heartbeat timeout 在 watchdog 无进展时中止进程，作用是避免作业长期占资源；进程被 abort 不表示 heartbeat 是首因。
- `TORCH_NCCL_ASYNC_ERROR_HANDLING` 不同值改变 communicator/process 的清理方式。只有核对目标版本默认值、数据一致性和恢复策略后才可调整。

旧版 PyTorch 或其他框架必须查自己的文档。不得为了整理旧案例而补写当时没有的 flight-recorder 证据。

### 停止条件与恢复安排

出现以下任一情况时停止主动复现或配置调整：

- Xid、CUDA fatal、设备丢失、进程异常退出或结果可能不一致；
- 持续 socket/IB/link 故障，或调查开始影响共享 fabric；
- communicator/rank 身份、日志时钟或文件唯一性无法保证；
- trace/debug 超出批准的内存、磁盘、时长或性能影响；
- 需要改接口、IB 参数、重启、主动测试或故障注入，但尚无隔离与授权。

恢复时撤销临时 debug/trace/接口/timeout 变量，停止 RAS listener 或测试进程，清理 communicator，确认 GPU/driver/NIC 被动状态可读，并在无注入条件下通过一次结果正确性基线。恢复运行不等于根因或计算正确性已经验证。

### 完成判据

本轮调查在以下任一状态结束：

1. 同一 process group 内找到第一个缺席、进入不同 `SeqNum/OpType` 或在上游阶段停住的 rank，并能解释等待者；
2. 找到早于 watchdog timeout、与 rank/GPU/通信路径一致的独立 device 或 transport 事件；
3. 固定版本、rank 映射和工作负载后，单变量对照稳定改变预注册的 sequence/进度或 timeout 观测，并通过结果检查；
4. 证据仍不足，但已明确缺少哪些 rank 日志、trace、栈、版本、拓扑或设备/网络事件，结论保持 `unknown`。

`ncclras` 能连接、debug 文件生成、timeout 变长、进程退出为 0 或一次作业跑完，都不单独构成完成。

### 来源与验证记录

- [NCCL 2.27.5 Environment Variables](https://docs.nvidia.com/deeplearning/nccl/archives/nccl_2275/user-guide/docs/env.html)、[Troubleshooting](https://docs.nvidia.com/deeplearning/nccl/archives/nccl_2275/user-guide/docs/troubleshooting.html)与[RAS](https://docs.nvidia.com/deeplearning/nccl/archives/nccl_2275/user-guide/docs/troubleshooting/ras.html)：核对 debug、接口/IB 参数、系统支路和 2.24+ RAS。
- [PyTorch 2.8 distributed](https://docs.pytorch.org/docs/2.8/distributed.html)与[ProcessGroupNCCL 变量页](https://docs.pytorch.org/docs/2.8/torch_nccl_environment_variables.html)：核对 process group/collective 背景和框架层观测字段。
- 当前验证范围：来源核对；没有目标 GPU、网络、作业日志或执行结果。
