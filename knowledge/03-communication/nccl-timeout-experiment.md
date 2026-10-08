---
id: communication.nccl-timeout-experiment
title: NCCL 超时验证实验设计
type: experiment
domain: communication
status: draft
platforms: [nvidia]
source_refs:
  - src.nvidia.nccl-user-guide-2.27.5
  - src.nvidia.nccl-tests-b4d5beeb
  - src.pytorch.processgroupnccl-env-2.8
updated_at: "2026-09-30"
summary: 在隔离 GPU/NIC 资源中设计 ProcessGroupNCCL 进度观测、RAS/trace 与 nccl-tests 基线对照，预注册注入和恢复判据。
related_ids:
  - communication.nccl-timeout-triage
  - communication.nccl-timeout-source-case
  - communication.collectives-and-rank-progress
  - communication.bandwidth-baselines
  - reliability.evidence-and-hypotheses
applicability:
  environment_refs: []
  notes: "尚未选择实际 GPU、driver/CUDA/NCCL/PyTorch、容器、NIC/fabric 或 nccl-tests 构建；执行前逐项核对 NCCL RAS（2.24+）与 PyTorch 观测变量的版本可用性。"
verification:
  status: not_verified
  evidence_refs: []
  notes: "当前只有实验设计；未分配 GPU/网络资源，未运行 nccl-tests、NCCL RAS、ProcessGroupNCCL 工作负载或故障注入，未产生性能、正确性、日志或恢复结果。"
---

# NCCL 超时验证实验设计

## 问题与假设

本设计验证“collective timeout 是由 rank 进度分叉、上游阻塞、设备故障、transport 故障还是等待预算不足所解释”。它不以“让 timeout 消失”为唯一目标，而要求每个结果能映射到同一 process group 中的 rank、sequence、collective、设备和路径。

预注册假设：

- **N1：缺 rank 或错序。** 某 rank 没有进入、进入不同 `SeqNum/OpType`，或多个 process group 的全局调用次序不一致。
- **N2：上游控制流阻塞。** 某 rank 停在数据、checkpoint、CPU/Python、CUDA kernel 或异常分支，NCCL 是等待者。
- **N3：GPU/driver 先失败。** Xid、CUDA fatal 或设备丢失早于 collective timeout。
- **N4：NCCL transport/网络先失败。** socket/IB/async/link 错误早于 timeout，并与实际接口/NIC/rail 路径一致。
- **N5：等待预算不足。** 所有 rank 以一致契约持续前进，正常完成时间分布稳定超过框架 timeout。

每个假设都必须允许“无法判断”。一次 watchdog abort、一次 RAS `MISMATCH` 或一次低带宽不能自动通过任何假设。

## 环境与输入

执行前填写并冻结以下清单：

| 类别 | 必填字段 |
| --- | --- |
| GPU/节点 | GPU 型号/数量/UUID、driver、NVLink/NVSwitch/PCIe/NUMA 拓扑、独占节点或切分边界 |
| 软件 | CUDA runtime、NCCL、PyTorch/框架、容器 digest、宿主 OS/内核、nccl-tests commit/构建身份 |
| 网络 | NIC/端口/固件、IB/RoCE/EFA 或 socket、MTU/GID/rail/交换路径、rank→GPU→NIC 映射 |
| communicator | process group 成员/创建顺序、global/group/local rank、collective、root、dtype/count/shape 契约 |
| 工作负载 | 最小 collective 或最小训练阶段、输入/模型/数据身份、stream、超时配置和结果正确性检查 |
| 观测 | watchdog 字段、NCCL debug 文件命名、RAS 可用性、PyTorch trace/dump 配置、GPU/driver/NIC 事件 |
| 资源 | GPU/HBM、CPU/内存、PCIe/NVLink/NIC/fabric、端口、日志空间、最长时长、温度/功耗边界 |

本设计引用的 RAS 页面属于 NCCL 2.27.5，并说明 RAS 自 2.24 起可用；PyTorch 变量页属于 2.8。目标版本不满足时，对应观测项记为“不适用”，不能用相似变量名替代。

## 实验设计

### A. 无注入的正确性与进度基线

选择一个明确 collective 和 process group，固定消息大小、数据类型、root/规约、rank 映射、接口路径、warm-up/iterations 和同步口径。建立两类基线：

1. **框架基线**：记录每个 rank 的 sequence/op、last enqueued/completed（若版本提供）、阶段和结果检查。
2. **通信工具基线**：使用固定 `src.nvidia.nccl-tests-b4d5beeb` 对应的源码身份，按[集合通信带宽基线](bandwidth-baselines.md)记录工具版本、精确 payload、in/out-of-place、rank 布局、计时和 correctness check。

nccl-tests 基线只能证明工具在该环境和输入下的 collective/transport 行为。它不能复现 DeepSpeed 等框架控制流，也不能把 `busbw` 直接当物理链路利用率。

### B. 被动观测对照

先增加观测，不改变 transport：

- NCCL 2.27.5 中为每个 host/PID 使用唯一 debug 文件，限制 `NCCL_DEBUG`/subsystem 级别和时间窗口；
- NCCL ≥2.24 且环境实际启用 RAS 时，保存 job/process/communicator 查询；重复观察 `MISMATCH` 是否持续不变，区分暂时进度差异与 stuck；
- PyTorch 2.8 且预先配置 ring buffer 时，保存 dump-on-timeout、desync/timing/stack 字段及其配置；
- 同步采集 GPU/driver 与 NIC/link 被动事件，所有记录使用同一 run id 和时钟说明。

如果观测本身显著改变时延、产生磁盘压力或引入 hang，停止并将该 run 标为“观测干扰”，不与基线混合。

### C. 控制流/次序单变量对照

在一次性、无业务的最小程序中，固定 transport 和设备，只改变一个 process group/collective 次序条件。可以设计以下受控情形，但不在正文提供生产可复制命令：

- 所有 rank 同序进入同一 collective；
- 审核后的某 rank 故意不进入目标 collective；
- 两个 process group 在一个 rank 的提交次序与其他 rank 不同；
- 某 rank 先执行一个可控的上游延迟，但最终仍进入相同 collective。

这些都是故障注入，必须有 launcher 回收、硬性运行时限和全进程清理。预期观测是 sequence/op/rank 时间线如何变化，不是追求让作业长时间 hang。

### D. transport 路径对照

只有 B 阶段已有接口/transport 证据时，才单变量比较经过批准的路径。`NCCL_SOCKET_IFNAME`、IB HCA/GID/timeout、socket retry 等设置会改变运行行为；不能一次修改多项再把结果归因于网络。

不在共享 fabric 上做丢包、拔链路、交换机或 NIC 故障注入。需要这类实验时，应另建网络实验计划，限定端口、rail、流量、租户隔离和网络恢复负责人。

### E. GPU/driver 对照

只有出现早于 timeout 的 Xid/CUDA/device 证据时，才在隔离资源中设计设备替换或 rank 映射对照。主动 GPU 压测、复位或诊断不是本实验默认步骤；其资源、型号/版本支持和恢复要求另按设备流程审核。

## 前置条件与运行影响

| 条件 | 要求与影响 |
| --- | --- |
| 隔离 | 调度器独占 GPU/节点和必要 NIC/rail；专用端口、进程组和日志目录；不与训练、推理、存储或其他通信基准共享目标路径 |
| 权限 | 运行程序、访问 RAS 端口、读取 GPU/NIC 状态、attach 进程和修改环境变量分别授权；文档本身不授予权限 |
| 日志 | TRACE、CPP stack 和 flight-recorder dump 可增加 CPU、内存、I/O 和磁盘占用；预设容量、保留期和自动停止点 |
| 通信负载 | nccl-tests 会消耗 GPU、HBM、PCIe/NVLink 与网络带宽；不得在共享业务窗口运行 |
| 配置 | 每轮只改一个预注册变量，保存原值和回滚；debug、接口选择和 timeout 变更在轮次结束后撤销 |
| 故障注入 | 仅限可回收的短时隔离进程；设硬性 timeout 和外部 launcher；不操作共享交换机或生产 GPU |

停止判据：首个不可恢复 Xid/CUDA error、持续 transport/link 错误、correctness check 失败、进程无法回收、共享网络受影响、观测超过容量，或超出时长、温度、功耗、带宽预算。停止后不立即开启下一轮，先保存全 rank 证据并确认恢复。

## 执行与记录方法

1. 审核环境、版本适用性、资源所有者、隔离、风险、执行授权、停止和恢复负责人；缺一项则保持 `not_run`。
2. 建立无注入框架与 nccl-tests 正确性基线。结果检查未通过、rank 缺失或 transport 已报错时，不进入故障注入。
3. 按 B→C→D→E 的证据需求逐层执行。每个 run 只改变一个变量，保存配置 diff、全 rank sequence/op、trace/RAS、设备/网络事件、退出状态和正确性结果。
4. 每轮撤销调试与路径覆盖，清理全部 process group、RAS listener、测试进程和临时端口，再重复无注入基线。
5. 若恢复基线不能通过，停止实验并保持资源隔离；记录偏差，不用下一轮结果覆盖。

本节是实验记录规范，不表示已执行，也不授权任何命令、配置修改或故障注入。

## 通过、失败与无法判断的判据

| 结论 | 预注册判据 |
| --- | --- |
| 支持 N1 | 预设缺 rank/错序使同一 communicator 出现可重复的 sequence/op 分叉和等待；恢复同序后无注入基线及结果检查恢复 |
| 支持 N2 | 同一上游阶段稳定先阻塞一个 rank，移除该单变量后 collective 共同进度恢复，且无更早设备/transport 错误 |
| 支持 N3 | 独立 Xid/CUDA/device 事件稳定早于 timeout、映射到同一 GPU/rank，并在设备或 rank 映射单变量对照中改变结果 |
| 支持 N4 | NCCL transport/link 事件稳定早于 timeout、与实际 NIC/rail 对应，并在获批路径对照中出现/消失 |
| 支持 N5 | 全 rank 契约/sequence 一致且持续进展，完成时间分布稳定超过原预算；调整后完成且 correctness 通过、无错误只是延迟 |
| 实验失败 | 基线错误、控制变量漂移、日志覆盖、隔离破坏、资源超限、进程回收或恢复失败 |
| 无法判断 | 缺少 communicator/rank/时钟/trace/设备/网络证据，版本不支持观测，样本不足或多变量同时变化 |

不以单次 RAS `RUNNING/MISMATCH`、单次 nccl-tests `#wrong 0`、一次没有 timeout 或调大 timeout 后任务延长作为通过。

## 实际结果与证据

尚未执行。没有环境档案、run id、日志、RAS/trace、nccl-tests 输出、设备/网络测量或恢复证据。执行后只有在真实证据可定位时才能填写；当前 `verification.status` 保持 `not_verified`。

## 局限、来源与后续问题

- [NCCL 2.27.5 Environment Variables](https://docs.nvidia.com/deeplearning/nccl/archives/nccl_2275/user-guide/docs/env.html)与[RAS](https://docs.nvidia.com/deeplearning/nccl/archives/nccl_2275/user-guide/docs/troubleshooting/ras.html)：用于观测、版本边界和行为改变说明。
- [PyTorch 2.8 ProcessGroupNCCL Variables](https://docs.pytorch.org/docs/2.8/torch_nccl_environment_variables.html)：用于 trace/dump/desync/timing/monitoring 的设计；不外推到旧版。
- [NVIDIA nccl-tests 固定 commit](https://github.com/NVIDIA/nccl-tests/tree/b4d5beebca8a76cf01335f724d154b9b9d394d96)：用于工具身份和基线字段；未构建或运行。
- 局限：本设计不验证任意 PyTorch/NCCL/CUDA/driver 组合，不给出通用 timeout 或带宽阈值，也不覆盖生产 fabric 和设备破坏性故障注入。
- 待确认：目标硬件/软件/容器、NIC/fabric、RAS/flight-recorder 可用性、日志容量、批准的注入范围、外部 launcher 与恢复负责人。
