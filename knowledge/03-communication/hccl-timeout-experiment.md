---
id: communication.hccl-timeout-experiment
title: HCCL 超时验证实验设计
type: experiment
domain: communication
status: draft
platforms: [ascend]
source_refs:
  - src.huawei.hccl-user-guide-cann-8.1-rc1-alpha001
  - src.ascend.cann-hccl-2d685b08
updated_at: "2026-09-30"
summary: 在隔离 NPU 资源中设计 rank 进度、group 次序和设备/网络证据的单变量对照，不把预期结果写成实测结论。
related_ids:
  - communication.hccl-timeout-triage
  - communication.hccl-timeout-source-case
  - communication.collectives-and-rank-progress
  - communication.bandwidth-baselines
  - reliability.evidence-and-hypotheses
applicability:
  environment_refs: []
  notes: "尚未选择实际 NPU、CANN/HCCL、HCCL Test、框架、容器或网络环境；执行前必须取得与目标版本配套的测试文档并建立独占资源和恢复方案。"
verification:
  status: not_verified
  evidence_refs: []
  notes: "当前只有实验设计；未分配 NPU/网络资源，未运行 HCCL Test、工作负载或故障注入，未产生延迟、带宽、错误码、日志或恢复结果。"
---

# HCCL 超时验证实验设计

## 问题与假设

本实验设计回答两个可以被证伪的问题：

1. 在固定软件、rank 映射、输入和 group 创建顺序后，超时是否由某个 rank 没有进入同一 collective 或不同 group 的操作次序分叉所解释？
2. 若所有 rank 的操作契约和进度一致，是否存在早于 timeout、可独立复现的设备或通信路径异常？

预注册的候选假设为：

- **H1：rank/次序分叉。** 某 rank 未到达、进入另一 collective，或两个 group 在各 rank 的提交次序不同。
- **H2：上游阶段阻塞。** 某 rank 在数据、计算、checkpoint、编译/图捕获或长 kernel 中停留，通信只是等待者。
- **H3：设备/runtime 先失败。** NPU、AICore/AIV 或 runtime 错误早于 collective timeout。
- **H4：网络/链路先失败。** CQE、link 或丢包事件早于 timeout，并与受影响 rank 的路径一致。
- **H5：等待预算不足。** 所有 rank 仍按同一次序取得进展，但正常完成时间稳定超过目标版本的等待预算。

任何一次超时都可能同时出现多个后果。实验只有在时间和实体映射上分离首因与级联事件，才能推动某一假设。

## 环境与输入

执行前建立不可变实验清单，未知项不允许用“默认”代替：

| 类别 | 必填字段 |
| --- | --- |
| NPU/节点 | 型号、数量、设备身份、固件/驱动、HCCS/PCIe/网口/NUMA 拓扑、独占范围 |
| 软件 | CANN/HCCL、torch_npu/框架、HCCL Test 的发行版或 commit、容器 digest、宿主 OS/内核 |
| rank | 节点/进程/global/group/local rank 到 NPU 和网口的映射；group 成员与创建顺序 |
| 工作负载 | 最小 collective 或最小模型阶段、输入身份、collective/数据类型/元素数、图模式与并行配置 |
| 时间 | 节点时钟同步状态、统一时区、run id、开始/结束时间和最长运行窗口 |
| 观测 | 各 rank 日志路径与保留期、设备/runtime 事件、网络/CQE/link 证据和日志容量预算 |
| 配置 | timeout 原值及来源、所有 HCCL/框架变量、只允许的单变量及回滚值 |

`src.ascend.cann-hccl-2d685b08` 只是固定源码快照，仓库 README 自身提示 master 与 CANN 版本可能不配套。实际执行不能仅凭该 commit 选择二进制；必须取得与目标 CANN/HCCL 相匹配的 HCCL Test 发行物和说明。

## 实验设计

实验分四层，每层先恢复无注入基线，上一层证据不足才进入下一层。

### A. 无注入的共同进度基线

- 选择最小参与 rank 集合和一个明确 collective；固定 group、rank 映射、数据类型、元素数与输入。
- 运行预先确定的重复次数，分别记录各 rank 最后成功、提交、等待与完成的操作，以及设备和链路被动状态。
- 基线必须通过工具/工作负载定义的结果检查；仅记录性能而没有正确性结果的运行不得作为正常基线。
- 保存完成时间分布，不从单次运行定义统一 timeout 或带宽阈值。

### B. 工作负载阶段对照

在配置和输入固定时，只改变一个可能阻塞 rank 的阶段条件，例如是否进入目标图捕获/编译阶段。对照观察：

- 共同进度点是否移动；
- 是否总是同一 rank/group 首先分叉；
- 设备/runtime 或网络错误是否仍早于分叉；
- 无该阶段时结果检查与基线是否恢复。

若必须同时改变两个开关，只能把结果归因于“组合变化”，不能拆成两个单变量结论。

### C. group/次序对照

在一次性隔离作业中，显式定义一个 group 与两个 group 的对照，固定创建次序和成员。只有在审核后的测试程序中才能设计“某 rank 不进入”或“不同 rank 交换 group 操作次序”的故障注入；正文不提供可复制的生产注入命令。

预期观测不是“必须超时”，而是每个 rank 的 group、操作和相对序号是否如设计分叉，以及其他 rank 的等待能否由该分叉解释。若程序没有暴露可靠序号，就用带 run id 的前/后事件点建立等价时间线。

### D. 设备/网络独立对照

只有被动证据已指向特定 NPU 或路径时，才另建专项实验。设备压力诊断、链路故障注入、交换机变更和共享 RoCE/HCCS 操作不属于本设计的默认步骤；它们需要独立风险评审、资源隔离、厂商适用性和恢复验证。

若只是验证健康基线，可在无业务资源上选择目标版本支持的被动查询和低风险测试。HCCL timeout 与设备/网络证据必须按时间、rank 与路径对齐，不能用一次“健康”或一次“FAIL”覆盖所有子系统。

## 前置条件与运行影响

| 条件 | 要求与影响 |
| --- | --- |
| 隔离 | 调度器独占测试节点/NPU；专用端口、日志目录和 rank group；不得与训练、推理或其他通信作业共享目标 NPU/网口 |
| 资源预算 | 预先批准 NPU/HBM、CPU、主机内存、HCCS/RoCE 带宽、端口、功耗/温度、日志空间和最长运行时间 |
| 正确性 | 输入和期望输出可确定；每次运行保存 check 状态，错误或跳过检查的结果不进入性能分布 |
| 观测成本 | debug/trace 会增加日志、CPU/I/O 和时延；限定窗口、级别、唯一文件和停止容量 |
| 配置变更 | 每次只改一个预注册变量；保存原值、生效范围和回滚步骤；不把增大 timeout 或关闭特性作为默认修复 |
| 故障注入 | 仅限一次性、无业务作业；launcher 必须能回收全部进程；不触碰共享交换网络或生产设备 |

停止判据：首个不可恢复 NPU/runtime 错误、持续 link/CQE 异常、结果检查失败、影响隔离边界、rank 身份丢失，或超出时间、温度、功耗、带宽与日志预算。任何停止都先保存当前 run id 和全 rank 证据，再按批准方案清理。

## 执行与记录方法

1. 审核环境清单、资源所有者、隔离状态、风险、停止/恢复判据和执行授权；任一缺失则记录 `not_run`。
2. 验证 rank 到 NPU/节点/网口映射和时钟，建立无注入正确性基线；没有合格基线不进入注入。
3. 按 A→B→C→D 顺序执行获批的单变量对照。每个 run 使用唯一身份，保存全 rank 的操作进度、最早错误、设备与网络事件、退出状态和结果检查。
4. 每轮后恢复原配置并重复一次无注入基线。若基线不能恢复，停止后续实验并保持资源隔离。
5. 记录任何偏离设计的情况；不得删除不符合预期的运行，也不得用预期值填充缺失观测。

本节是记录规范，不表示本库已执行这些步骤，也不提供执行授权。

## 通过、失败与无法判断的判据

| 结论 | 预注册判据 |
| --- | --- |
| 支持 H1 | 同一 group 中可重复出现预设的缺 rank/错序，其他 rank 的等待在时间和操作上由其解释；恢复相同次序后无注入基线恢复 |
| 支持 H2 | 某上游阶段总是先于 timeout 阻塞同一 rank，去除该单一条件后共同进度恢复；没有更早设备/网络错误 |
| 支持 H3 | 独立设备/runtime 错误稳定早于通信等待并对应同一 NPU/rank；更换或隔离该实体的单变量对照改变结果 |
| 支持 H4 | 链路事件稳定早于 timeout、与实际通信路径一致，并在路径单变量对照中出现/消失 |
| 支持 H5 | 所有 rank 的操作契约和进度一致，完成时间分布可重复超过原等待预算；调整预算后任务完成且结果检查通过，无错误仅被延后 |
| 实验失败 | 环境或控制变量漂移、基线不正确、隔离被破坏、资源超限或恢复失败 |
| 无法判断 | 缺少全 rank/时钟/group/设备/网络证据，样本不足，多个变量同时变化，或对照不能恢复 |

“没有复现”“运行退出为 0”“timeout 变晚”或一次 `check_result=success` 不能单独证明任一根因。

## 实际结果与证据

尚未执行。未分配环境，未产生任何 run id、日志、测量、错误或恢复证据。执行后只有在可定位证据完整时才能更新本节；当前 `verification.status` 保持 `not_verified`。

## 局限、来源与后续问题

- [CANN 8.1.RC1.alpha001 HCCL 用户指南，第 88–89 页](https://www.hiascend.com/doc_center/source/zh/CANNCommunityEdition/81RC1alpha001/devguide/hccl/hcclug/CANN%E7%A4%BE%E5%8C%BA%E7%89%88%208.1.RC1.alpha001%20%E9%9B%86%E5%90%88%E9%80%9A%E4%BF%A1%E7%94%A8%E6%88%B7%E6%8C%87%E5%8D%97%2001.pdf)：用于 EI0002 的 rank、较早错误、设备、网络和等待预算分支。
- [cann-hccl 固定 commit](https://gitee.com/ascend/cann-hccl/tree/2d685b084a60366b47ad8e50a563ee5c4dbef7fe)：只固定 HCCL Test/README 证据身份；未构建或运行，不能证明与目标 CANN 配套。
- 局限：本设计不验证任意 CANN/HCCL 组合，不给出通用 timeout、带宽或正确性阈值，也不覆盖交换机/设备破坏性注入。
- 待确认：目标硬件和软件、配套 HCCL Test、日志/trace 能力、设备/网络被动观测、可批准的故障注入范围和恢复负责人。
