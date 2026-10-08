---
id: communication.hccl-timeout-source-case
title: "HCCL 启动期超时来源案例：vLLM Ascend #14296"
type: case
domain: communication
status: draft
platforms: [ascend]
source_refs:
  - src.vllm-ascend.issue-14296
updated_at: "2026-09-30"
summary: 整理一个单节点 16 卡、DCP/MoE/AIV 组合在启动阶段超时的外部 Issue，保留报告者归因、缓解反馈、workaround 冲突和修复未证实边界。
related_ids:
  - communication.hccl-timeout-triage
  - communication.hccl-timeout-experiment
  - communication.collectives-and-rank-progress
  - reliability.evidence-and-hypotheses
applicability:
  environment_refs: []
  notes: "外部案例限定于报告者所述 CANN 9.0.1、Ascend 910B3 x16、vLLM Ascend v0.26.0rc 特定启动路径；不能外推到其他 CANN、硬件、模型、通信算法或生产环境。"
verification:
  status: source_checked
  evidence_refs:
    - src.vllm-ascend.issue-14296
  notes: "已核对 Issue 正文、三条评论、状态和时间线；报告者反馈 AI_CPU 可缓解，另有自动回复和含糊 PR 提及。没有本地复现、独立根因确认或可核验的修复/发行证据。"
---

# HCCL 启动期超时来源案例：vLLM Ascend #14296

## 案例来源与问题

本案例整理公开的 [vllm-project/vllm-ascend #14296](https://github.com/vllm-project/vllm-ascend/issues/14296)。报告者描述：在单节点 16 卡的 vLLM 启动阶段启用特定 DCP 配置后，权重加载已经完成，但在 `profile_run` / cudagraph capture、尚未承接真实请求时，全卡 AIV AllGather 长时间不返回，约 300 秒后出现 HCCL `EI0002`、vector core timeout 和引擎初始化失败。

调查问题不是“这个错误码是不是网络坏了”，而是：各 rank 是否到达同一 group/collective，两个 AIV group 的进展如何交错，设备/runtime 错误是首因还是级联后果，以及哪些配置变化真正构成单变量证据。

这是外部 Issue 的来源整理。本库没有取得原始附件、运行环境或模型，也没有复现事件。

## 当时环境与近期变化

以下均为报告者在 Issue 中填写的环境，不是本库验证结果：

| 层次 | 报告值 | 证据边界 |
| --- | --- | --- |
| 硬件 | Ascend 910B3 ×16，单节点，每卡 64 GB HBM | 报告者称在两个物理节点分别复现；没有设备序列、固件、HCCS/网口拓扑和独立健康记录 |
| OS/容器 | openEuler 24.03 LTS，容器 | 容器 digest、宿主 OS/内核、驱动与 runtime 制品身份未给出 |
| CANN | 9.0.1 | 没有更细包版本、补丁或安装清单 |
| 框架 | PyTorch 2.10.0；torch_npu 2.10.0.post2；Python 3.11 | 没有 wheel digest 或依赖锁定文件 |
| vLLM | vllm-ascend `releases/v0.26.0rc` commit `baaf1809`；vllm commit `d02df748bf` | 两个 commit 是报告字段，本库没有检出源码或构建制品 |
| 并行/模式 | 单节点 PD-mixed，TP=16，decode context parallel=16，MoE expert parallel，MTP；AIV expansion mode | 同时存在 DCP、MoE、图捕获、投机推理和多项框架开关，不能从一次对照分离每个因素 |
| 图捕获 | `FULL_DECODE_ONLY`，capture sizes 为 6/12/24/48 | 报告称该设置先绕过另一个 shape 约束，才能到达本次 hang；因此它是复现前置条件之一 |

报告者把近期差异集中在 `enable_dsa_cp` 及相关 DCP/MoE/AIV 路径，但 Issue 的可用 workaround 表述并不一致，见下文。

## 事件与证据时间线

正文日志摘要没有完整日期/时区，按相对阶段与本地时刻记录；后续 GitHub 评论采用 API 的 UTC 时间。两者不能直接拼成同一次运行的绝对时间线。

| 时间与时区 | 事件或观测 | 实体与范围 | 证据定位 |
| --- | --- | --- | --- |
| 启动前 | 配置 TP=16、DCP=16、MoE EP、AIV，并显式给出 capture sizes | 单节点 16 个 worker/rank | [Issue 的 To Reproduce](https://github.com/vllm-project/vllm-ascend/issues/14296) |
| 权重加载后 | 进入 `profile_run` / cudagraph capture；报告称尚无真实请求 | 全部 worker | [Issue Description 与 To Reproduce](https://github.com/vllm-project/vllm-ascend/issues/14296) |
| 约 03:43:22，本地时区未知 | plog 示例记录 AIV task，`deviceId[15]`、op index 181；多个 chip sync 值未完成 | 至少 rank/device 15 的示例；报告称 16 个 worker plog 一致 | [Full Error Stack / plog 摘要](https://github.com/vllm-project/vllm-ascend/issues/14296) |
| 同一阶段 | HCCL 自诊断输出两个包含 AIV 算法的 group：`group_name_103`、`group_name_3`，并提示 multi groups may cause execution stuck | 两个通信 group | 同上 |
| 等待约 300 秒后 | `EI0002` notify wait timeout，task type AIV，tag 指向 `AllGather_group_name_3`；随后 vector core timeout、runtime result `507034` | 报告称 16 卡异常 | [错误栈](https://github.com/vllm-project/vllm-ascend/issues/14296) |
| 随后 | `Engine core initialization failed` 与上层 `ERR99999` | 引擎/API server | 同上；属于超时之后的级联结果 |
| 2026-08-15 03:19 UTC | 报告者根据新 plog 初判 MoE/AllGather 抢核，并反馈改为 AI_CPU 后问题消失，可能有性能代价 | 报告者的调查与缓解反馈 | [评论 5300280446](https://github.com/vllm-project/vllm-ascend/issues/14296#issuecomment-5300280446) |
| 2026-08-17 07:40 UTC | 自标 Automated Response 的回复记录该反馈并请求继续调查 | 自动跟进，不当作独立验证 | [评论 5313215244](https://github.com/vllm-project/vllm-ascend/issues/14296#issuecomment-5313215244) |
| 2026-09-22 03:17 UTC | 报告者含糊提及一个可能解决问题的 PR；Issue 同时以 completed 关闭 | 提及编号为本 Issue 的 14296，未定位到可确认修复链 | [评论 5770710734](https://github.com/vllm-project/vllm-ascend/issues/14296#issuecomment-5770710734)与 Issue API 状态 |
| 2026-09-30 观察 | Closed；Development 未显示关联修复 PR | 状态与技术结果分开 | [Issue](https://github.com/vllm-project/vllm-ascend/issues/14296) |

时间线缺少每个 rank 的“最后成功 collective”和两个 group 的完整创建/提交顺序。报告者说 16 个 plog 完全一致，但公开正文只展示摘要；因此不能仅从示例还原所有 rank 的精确事件序列。

## 假设与调查

| 候选解释 | 支持证据 | 反对或缺失证据 | 检查与结论 |
| --- | --- | --- | --- |
| DCP 与 MoE 的两个 AIV group 并发导致进展死锁 | 两个 AIV group 的日志警告；报告者后续 plog 初判抢核，并反馈切换 AI_CPU 后现象消失 | 自动回复未独立验证归因；完整 rank/group trace、最小复现、源码修复及受控结果仍缺失 | **报告者首选归因，未确认** |
| 某 rank/group 没有按相同次序进入 collective | notify wait、未完成 sync 值和两个 group 与此相容 | 公开摘要没有逐 rank 的最后成功/下一项操作；报告称日志一致也不等于提交顺序已证明一致 | **需完整 rank 时间线** |
| 单卡硬件故障 | 错误包含 vector core timeout 和 runtime 507034 | 报告称两个物理节点都确定性复现且 16 卡行为一致；没有更早的独立设备健康错误 | **证据不支持作为首选，但未做本库硬件验证** |
| 网络故障 | HCCL timeout 一般可以由链路问题引起 | 案例是单节点；正文没有 CQE、link-down、丢包或网络路径事件 | **缺少独立网络证据** |
| 图捕获/shape 前置问题 | 必须显式 capture sizes 才能绕过另一个 shape 约束并到达 hang | 报告者称 capture sizes 与本 bug 无关，但没有单变量矩阵证明 | **可能是复现前置/混杂条件，根因作用未知** |
| timeout 太短 | 约 300 秒后触发 | 启动阶段没有继续进展的证据；延长等待不能解决错序或死锁 | **不能据此建议增加 timeout** |

## 处理与结果

Issue 开头说关闭 `enable_dsa_cp` 后服务可以启动，并称同事独立验证。后面的“规避旁路”和 Additional Context 则写同时把 `enable_dsa_cp` 与 `enable_flashcomm1` 设为 false 才可正常启动。这是两个不同对照：

- 若只改变 `enable_dsa_cp`，可用于检验 DCP 相关性；
- 若同时改变两个开关，只能说明组合变化与现象相关，不能分辨哪个开关或交互项起作用。

公开页面没有给出两个对照的完整配置、重复次数、日志或结果正确性检查。本案例因此不把关闭特性写成默认修复，只记录为**报告者所述 workaround，且表述冲突**。

补读评论后还取得另一条缓解路径：[报告者 8 月 15 日评论](https://github.com/vllm-project/vllm-ascend/issues/14296#issuecomment-5300280446)说改 `HCCL_OP_EXPANSION_MODE` 为 `AI_CPU` 后问题消失，并提醒可能影响性能；同时重申两个框架开关的组合规避。该评论根据 plog 将 MoE 与 AllGather 抢核列为初判，还援引一个 `latest` 手册的多通信域限制。本库尚未独立取得该页可读正文及 CANN 9.0.1 对应条款，**只归属为报告者援引，不当作本库核实的版本保证**。

8 月 17 日跟进明确自标 Automated Response，不能当作维护者完成根因验证。9 月 22 日作者仅称听说某 PR 可能解决，引用编号又与本 Issue 相同；同一时刻的 completed 关闭表明状态变化，但没有可追溯补丁或复验。

因此可确认的是“报告者反馈过配置缓解，Issue 已 completed 关闭”；独立根因确认、真正修复提交、首个发行版本和质量/性能复验仍未知。启动恢复不证明推理结果或长时间稳定性。

## 可复用经验与边界

- 把 HCCL timeout 放回工作负载阶段。这里发生在启动期 profile/图捕获，不是请求负载或训练迭代中的一般网络超时。
- 保存 group/tag、task/stream/op index 和所有 rank 的时间线。仅有“全卡都超时”不足以判断谁先偏离。
- timeout 后的 `ERR99999`、引擎失败和同步错误是级联结果候选；优先找更早的 group、设备或控制流事件。
- 对 workaround 做单变量拆分。两个开关同时关闭不能证明其中任一是根因。
- 跨节点复现可以降低“某一张卡偶发损坏”的可信度，但不能排除相同软件、容器、配置或硬件代际带来的共同因素。
- `Closed` 只是一种 Issue 状态。没有修复证据时，应写“修复未证实”，而不是把状态转成技术结论。

这些方法可以迁移到其他 HCCL timeout 调查；本案例的 CANN 9.0.1、AIV、DCP/MoE 和具体开关结论不能外推。

## 来源与未解问题

- [vLLM Ascend #14296](https://github.com/vllm-project/vllm-ascend/issues/14296)：2026-09-30 核对环境、错误栈、Additional Context、三条评论、状态及关闭时间；静态页漏载评论，通过 GitHub 连接器与公开 API 补齐。
- 本地复现状态：未开展；未安装或运行 vLLM、CANN、torch_npu 或 HCCL。
- 待确认：完整 16-rank/group trace、设备与板内互联健康、宿主/容器制品身份、单变量 `enable_dsa_cp`/`enable_flashcomm1` 对照、AI_CPU 缓解的性能/质量结果、具体关闭依据、独立根因和修复版本。
