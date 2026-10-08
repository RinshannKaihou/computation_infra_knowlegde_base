---
id: communication.hccl-timeout-triage
title: HCCL 超时诊断指南
type: procedure
domain: communication
status: draft
platforms: [ascend]
source_refs:
  - src.huawei.hccl-user-guide-cann-8.1-rc1-alpha001
  - src.huawei.hccl-api-cann-8.0-rc1-alpha003
  - src.ascend.cann-hccl-2d685b08
updated_at: "2026-09-30"
summary: 从 HCCL 超时症状回溯各 rank 的共同进度和更早异常，再分别验证计算/次序、设备、网络与超时配置支路。
related_ids:
  - communication.collectives-and-rank-progress
  - communication.bandwidth-baselines
  - reliability.evidence-and-hypotheses
  - software-stack.ascend-documented-profile
applicability:
  environment_refs: []
  notes: "流程以 CANN 8.1.RC1.alpha001 HCCL 用户指南的 EI0002 排查分支为主要依据；目标环境仍需补齐 CANN/HCCL、torch_npu/框架、NPU 型号、rank 映射与单机/多机拓扑。"
verification:
  status: source_checked
  evidence_refs:
    - src.huawei.hccl-user-guide-cann-8.1-rc1-alpha001
    - src.huawei.hccl-api-cann-8.0-rc1-alpha003
    - src.ascend.cann-hccl-2d685b08
  notes: "已核对 CANN 8.1.RC1.alpha001 HCCL 用户指南第 88–89 页的 EI0002 分支，并以固定 HCCL API/Test 来源限定 rank 与测试口径；未在 NPU 或集群执行日志采集、配置修改、通信测试或故障注入。"
---

# HCCL 超时诊断指南

## 目标与触发条件

本流程用于解释训练、推理或初始化期间出现的 HCCL 执行超时，例如 `Communication_Error_Timeout(EI0002)`、notify wait timeout，或上层同步调用在 HCCL 任务之后失败。目标是找出**最早偏离共同进度的 rank 或独立设备/链路事件**，并说明其余 rank 为什么等待。

超时是等待结果，不是网络故障的同义词。某个 rank 没有进入同一 collective、进入了不同操作、在更早的计算中卡住或退出，都可能使其他 rank 最终在通信层报错。分析 rank、group 与操作契约的方法见[集合通信与 rank 进度](collectives-and-rank-progress.md)，假设与结论的分级见[诊断中的证据、假设与结论](../08-reliability/evidence-and-hypotheses.md)。

## 适用范围与前置条件

主要操作依据是 [CANN 8.1.RC1.alpha001《集合通信用户指南》](https://www.hiascend.com/doc_center/source/zh/CANNCommunityEdition/81RC1alpha001/devguide/hccl/hcclug/CANN%E7%A4%BE%E5%8C%BA%E7%89%88%208.1.RC1.alpha001%20%E9%9B%86%E5%90%88%E9%80%9A%E4%BF%A1%E7%94%A8%E6%88%B7%E6%8C%87%E5%8D%97%2001.pdf)印刷第 83–84 页（零基索引 88–89）9.1.2 节。目标环境若不是该版本，先核对同版文档、变量范围和日志格式；不能把这里的示例数值直接移植到 CANN 9.x 或其他发行版。

进入排查前至少固定：

- CANN、HCCL、torch_npu 和上层框架的完整版本或制品身份；
- NPU 型号、固件/驱动、节点数和 rank 到节点、设备、进程、网口的映射；
- world/custom group、group 内 rank、collective、tag、stream/task/op index；
- 报错发生在初始化、正常迭代、checkpoint、编译/图捕获、推理请求还是退出阶段；
- 各节点日志使用的时钟和时区，时钟不能对齐时明确记录偏差未知；
- 目标是否为生产作业，以及当前是否已有保存证据、停止任务或执行主动测试的授权。

本文不假定任何统一的 `HCCL_EXEC_TIMEOUT` 值。指南里的 timeout 设置是版本内机制与示例，不构成所有工作负载的推荐值。

## 需要的证据

| 证据 | 采集范围或定位 | 用途 | 缺失时如何处理 |
| --- | --- | --- | --- |
| 软件与制品身份 | 每个节点/容器的 CANN、HCCL、torch_npu、框架和镜像/包来源 | 判断日志字段、变量和已知限制是否适用 | 版本未知时不执行版本特定修改，结论限于症状描述 |
| rank 映射 | global/group/local rank 到进程、NPU、节点、网口 | 把日志事件映射到实体和故障域 | 不从 `deviceId` 或 `rank` 单字段猜映射 |
| 全 rank 日志 | 从最后一次共同成功之前到所有进程退出之后；保留原始时间、group/tag、stream/task | 建立共同进度和第一异常 | 只有单 rank 日志时，不下网络或设备根因结论 |
| 更早的框架/运行时错误 | 数据、checkpoint、图捕获、kernel、OOM、进程退出、elastic/launcher | 区分“没到达 collective”与“通信内部未完成” | 超时后的级联错误单独标为后果候选 |
| 设备证据 | 与 rank 对应的 NPU/runtime/AICore/AIV、掉卡与健康事件 | 验证设备支路是否先于通信等待 | “无记录”只有在采集成功且覆盖充分时才有意义 |
| 网络证据 | CQE、link-down、packet loss、拥塞、接口/路由和跨节点路径 | 验证链路支路 | `remote rank unknown` 不等于网络已坏；单机也不自动排除板内链路问题 |
| timeout 配置与正常耗时 | 当前值、默认来源、作业阶段的正常分布和变更历史 | 判断是否只是合法长操作超过等待预算 | 没有基线时不以调大 timeout 作为完成 |

日志中不得写入凭证或未脱敏业务数据。大日志保留在受管理证据系统，本页只记录索引和必要摘要。

## 步骤与判断分支

| 步骤 | 检查或动作 | 运行影响 | 预期证据与解释 | 下一步 |
| --- | --- | --- | --- | --- |
| 1 | 冻结调查窗口，记录环境、作业阶段、rank/group/设备映射和当前 timeout 配置 | 只读记录；若保留进程会继续占用资源，应由现场决定停止策略 | 获得可复核的实体与版本身份 | 身份缺失先补齐；不要先改配置 |
| 2 | 对齐全 rank 的最早错误、最后成功 collective、当前等待项和进程退出 | 读取日志和证据存储；不改变作业 | 找到共同进度点以及第一个分叉或第一异常 | 进入部分 rank/全 rank 分支 |
| 3A | 若只有部分 rank 先报 timeout，检查其他 rank 是否更早退出、报设备/运行时错误，或停在计算、数据、checkpoint、图捕获和另一 collective | 只读 | 一个 rank 的更早事件可以解释其余 rank 等待 | 验证该事件是否时间、group 和实体一致 |
| 3B | 若各 rank 都报 timeout，比较首末报错时间和每个 rank 的最后进度 | 只读；跨机时需考虑时钟误差 | 时间分散且某 rank 最后才进入，推动长任务/进度分叉；时间集中仍需设备/网络证据 | 分别进入次序、设备、网络和预算支路 |
| 4 | 核对同一 group 内操作类型、tag、参数契约与相对次序 | 日志/trace 可能增加存储和运行开销；本流程未授权重新运行 | 找到缺 rank、不同 collective 或不一致顺序时，先解释控制流 | 修复需在框架/工作负载层另行评审，不直接调 timeout |
| 5 | 检查 timeout 之前的设备/runtime 事件 | 被动查询通常较低影响；主动诊断不在本流程内 | 先于等待、对应同一 NPU/rank 的独立错误支持设备支路 | 按设备流程隔离与处置；保留通信超时为级联症状 |
| 6 | 多机或有网络线索时，检查 CQE、link、丢包、拥塞、接口和路由的同时段证据 | 查询交换/网卡状态可能需网络权限；不在此做故障注入 | 同期独立链路事件并与通信路径相符，才支持网络支路 | 转入网络专项验证；证据不符则回到进度分支 |
| 7 | 仅在所有 rank 次序一致、仍持续进展且正常耗时证据超过当前等待预算时，评估同版本 timeout 配置 | 配置改变会延迟故障显现并改变资源占用时长 | 调整只能验证等待预算，不证明根因消失 | 采用受控变更、回滚计划和完成判据；否则保持原值 |
| 8 | 汇总事实、推断、反证和未知项 | 无运行影响 | 每个结论能回链到 rank、时间、group 和实体 | 满足完成判据后结束，否则列出最小补采项 |

官方指南提出的 `error cqe` 搜索和 `HCCL_EXEC_TIMEOUT` 示例只作为分支依据。本页不提供可直接复制的日志路径或环境变量命令，因为路径、引号、变量范围和默认值必须与目标 CANN 版本和现场权限一致。

## 如何解释常见分支

| 分支 | 可以支持的结论 | 仍需排除 |
| --- | --- | --- |
| 某 rank 没进入同一 collective | 其他 rank 的 timeout 可由参与者缺失解释 | 该 rank 为什么没有进入：数据、计算、设备、退出或控制流错误 |
| 同 group 中操作/次序不一致 | collective 契约被破坏，是直接的进度分叉 | 不同 group 的序号不能混比；先核对 group 身份 |
| checkpoint/图捕获/长 kernel 先发生 | 等待可能来自合法或异常的上游阻塞 | 是否超过同环境正常分布，以及为何只有部分 rank 阻塞 |
| 设备错误早于 timeout | 设备/运行时故障是首因候选 | timeout 后出现的同步失败可能只是级联后果 |
| CQE/link-down/丢包与路径对齐 | 网络支路得到独立支持 | 配置错序和设备错误可能同时存在，不能只保留一个解释 |
| 延长 timeout 后暂不报错 | 原来的等待预算可能过短 | 作业是否继续取得共同进度、结果是否正确、错误是否只是被推迟 |

## 停止条件与恢复安排

出现以下任一情况时停止主动复现或配置试探，先保存证据并按现场控制面清理：

- NPU/runtime 不可恢复错误、掉卡、进程异常退出或结果一致性风险；
- link-down、持续 CQE/丢包或测试影响共享网络；
- rank 身份、日志时钟或 group 映射无法保持，继续运行只会生成不可比较证据；
- 运行超过批准的时间、功耗、温度、带宽或日志空间范围；
- 需要主动诊断、停服务、重启、改网络或执行故障注入，但尚无相应授权与隔离。

若做过受控配置变更，应记录原值、作用范围和生效时点；恢复后确认测试进程/communicator 已清理、配置已还原、设备与链路被动状态可读，再由现场决定是否解除隔离。一次服务重新启动不证明 collective 结果正确。

## 完成判据

以下任一结果可以结束本轮诊断：

1. 找到第一个没有进入同一 collective、进入不同操作或在上游阶段停住的 rank，并能用同一 group 的时间线解释其他 rank 的等待；
2. 找到早于 timeout 且与 rank、设备或通信路径一致的独立设备/网络事件；
3. 在固定版本、rank 映射和负载的受控环境中，单变量对照稳定改变了预定义的进度或 timeout 观测；
4. 证据不足，但已明确记录哪些 rank 日志、时钟、拓扑、版本或设备/网络证据缺失，并将结论保持为 `unknown`。

“命令成功”“timeout 变长”“作业暂时未报错”或“服务重启成功”均不单独满足完成判据。

## 来源与验证记录

- [CANN 8.1.RC1.alpha001 HCCL 用户指南，印刷第 83–84 页（零基索引 88–89）9.1.2](https://www.hiascend.com/doc_center/source/zh/CANNCommunityEdition/81RC1alpha001/devguide/hccl/hcclug/CANN%E7%A4%BE%E5%8C%BA%E7%89%88%208.1.RC1.alpha001%20%E9%9B%86%E5%90%88%E9%80%9A%E4%BF%A1%E7%94%A8%E6%88%B7%E6%8C%87%E5%8D%97%2001.pdf)：核对 EI0002 的 rank 进度、较早错误、设备、网络与 timeout 分支。
- [CANN 8.0.RC1.alpha003 HCCL API 参考](https://www.hiascend.com/doc_center/source/zh/CANNCommunityEdition/80RC1alpha003/apiref/hcclapiref/CANN%208.0.RC1.alpha003%20%E9%9B%86%E5%90%88%E9%80%9A%E4%BF%A1%E6%8E%A5%E5%8F%A3%E5%8F%82%E8%80%83%2001.pdf)：只用于 rank/group 与 collective 契约背景，不与 8.1 参数范围混用。
- [cann-hccl 固定 commit](https://gitee.com/ascend/cann-hccl/tree/2d685b084a60366b47ad8e50a563ee5c4dbef7fe)：只用于固定 HCCL Test/实现来源身份，未构建或运行。
- 当前验证范围：来源核对；没有目标环境、日志或执行结果。
