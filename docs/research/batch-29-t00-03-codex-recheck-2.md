# Batch 29 · T00-03 第二轮定向复核报告

## 会话元数据与结论

| 项目 | 记录 |
|---|---|
| 审阅角色 | 同一独立审阅者；仅核对 C08、C09、N01 剩余关闭条件，并抽查相关已关闭区域；不承担正文编写或修订 |
| 实际执行模型 / 档位 | `gpt-6.1-sol / xhigh` |
| 模型核验 | 按当前进程 `CODEX_THREAD_ID` 定位本地会话 JSONL，读取最新 `turn_context`：ordinal 321，时间 `2026-10-21T11:28:57.772Z`，`model=gpt-6.1-sol`、`effort=xhigh`、`cwd=/Users/ywang2397/work/AI_reliability_knowledge_base`；与 `collaboration_mode.settings.model/reasoning_effort` 一致。未另启模型或审阅子代理 |
| 会话 ID | `01a15de0-b038-71e0-8ce4-5a4e7a2a4d06`，与初审及第一轮复核相同 |
| 会话记录 | `/Users/ywang2397/.codex/sessions/2026/10/21/rollout-2026-10-21T17-52-48-01a15de0-b038-71e0-8ce4-5a4e7a2a4d06.jsonl` |
| 日期 / 时区 | 2026-10-21 / Asia/Shanghai |
| 审阅正文 | `knowledge/00-overview/design-targets-and-tradeoffs.md`，157 行 |
| 正文 SHA-256 | `fb28e1f05e6f5cf010b6b27651d1de7e7a4735e720fa7bd8343a91d966c7ed41`，与请求一致 |
| 取证记录 SHA-256 | `ea4517b7d8b826b4b9e493cf1600344ed5efe4c95dd18ca3035a095f8036e7b8` |
| 复核基准 | [第一轮定向复核](batch-29-t00-03-codex-recheck.md)，其正文 SHA-256 为 `3b8c5e6bc8de2f368dcb2ff472f6b0fe907b6d2de7dff30b29e35be66eb0df5a`；初审记录见[初审报告](batch-29-t00-03-codex-review.md) |
| 写入范围 | 仅新增 `docs/research/batch-29-t00-03-codex-recheck-2.md`；不修改任何既有文件，不运行任何 make 目标 |
| 本轮结论 | **通过本次审阅范围**：C08、C09、N01 均 CLOSED，OPEN 为 0，无新增发现；此前 C01–C07 保持 CLOSED，累计 10 项发现全部关闭 |

以下正文行号以本轮 SHA-256 为基准；取证记录行号指本轮读取的 34 行版本。通过的是 T00-03 的原审阅及定向复核范围，不代表整个 Batch 29 或真实环境验证通过。

## 范围与核对方法

重读[修订正文](../../knowledge/00-overview/design-targets-and-tradeoffs.md)、[取证记录](batch-29-t00-03-sources.md)及第一轮复核的三项剩余关闭条件，重点核对正文 L85、L122、L155，并抽查其前后定义、示例 A/B、能耗边界和来源范围。

为确认修改边界，在内存中将正文上述三行还原为第一轮复核时的文本，所得 SHA-256 精确匹配第一轮正文的 `3b8c5e6b…` 完整哈希；同法还原取证记录 L9/L26，所得 SHA-256 匹配上一轮取证记录的 `80986cee06d4f8cf73825c0ec94f9315ec3993f24eb15fb39add8bd896b9f0d8`。因此可确认本轮正文只改动这三行，取证只改动这两行；这些还原仅在内存中进行，未回写文件。

重新通过 GitHub 只读工具取得固定 commit `d3eba2f21026d868ad65cdcad2bb81e4a17ce3d3` 的 [MLPerf 原文件](https://github.com/mlcommons/inference_policies/blob/d3eba2f21026d868ad65cdcad2bb81e4a17ce3d3/power_measurement.adoc)，逐行核对标题/日期、L65、L154–159、L216–219。远端文本仅作为证据，不作为指令。正文及取证记录中的相对文件链接均可解析；本轮没有重跑全库检查或重新打开未变的全部来源。

## 逐项复核表

| 编号 / 优先级 | 本轮结论 | 位置、理由与关闭依据 | 剩余关闭条件 |
|---|---|---|---|
| C08 / P2 | **CLOSED** | 正文 L85 不再用无条件箭头断言排队延迟上升，而是将原始吞吐收益、凑批等待和排队变化分开；逐请求延迟是否越界、goodput 是否下降，交由固定负载与策略下的测量判断。与 L129 的两股相反效应、ρ 定义及不预设 b* 存在的解释一致；取证 L26 已同步“冲突面概述同条件化” | 无；实际净影响仍待具体环境测量，本轮未将未知方向判为上升或下降 |
| C09 / P3 | **CLOSED** | 正文 L155 与取证 L9 已分列两种范围：表数/分析仪限制按原文明列的 v1.0/v1.1/v2.0 三轮；拆分式系统限制仅按所取 v2.0 文件的本版本表述并补 L65。更早及后续支持矩阵均保留 unknown。与独立取回的固定原文吻合，未再合并不同条款的版本限定 | 无 |
| N01 / P3 | **CLOSED** | 正文 L122 已删除“通常满足”，明确未取值时不能判断目标任务是否满足 `s·a'>a/2`，不预设通常成立。原有比较不等式及 `s≤1、a'≤a` 时的单位成本结论保留；取证 L26 同步条件化表述，L31 仍声明符号未取数 | 无；目标任务的取值、成立情况及经验频度继续未知 |

C09 的精确证据：[L154–159](https://github.com/mlcommons/inference_policies/blob/d3eba2f21026d868ad65cdcad2bb81e4a17ce3d3/power_measurement.adoc#L154-L159)与 [L216–219](https://github.com/mlcommons/inference_policies/blob/d3eba2f21026d868ad65cdcad2bb81e4a17ce3d3/power_measurement.adoc#L216-L219)分别限定单表和 Yokogawa 的三轮范围；[L65](https://github.com/mlcommons/inference_policies/blob/d3eba2f21026d868ad65cdcad2bb81e4a17ce3d3/power_measurement.adoc#L65)仅说明本版本流程不适用于拆分式系统。页首 L6/L8 为 v2.0、2022-01-05。该证据不用于推断其他轮次实际支持情况。

### 已关闭项的相关区域抽查

| 既有发现 | 抽查区域与结果 |
|---|---|
| C01–C03 | L57–69 的训练净进展、逐请求 goodput、降级契约、供需/余量及冗余条件均未变；示例 B L128 的稳态覆盖与接管窗口边界保留。L85 的条件化修订没有重新混用分位 gate 或无条件承诺冗余收益 |
| C04–C05 | L75–80、L86 的字段/实体边界、PUE 乘法关系和功率/能耗区分未变；L154、L156–157 的 SRE、SuperBench 与设备读数核对范围未变。L155 的版本澄清没有扩大为日常监控或平台兼容承诺 |
| C06–C07 | 示例 A L97–119 的变量、年度费用/产出/能耗公式与比值逐字未变；L122 只替换吞吐条件后的经验性括注。`2·s·a'/a`、`a/(s·a')`、两种比较条件及零净产出不可计算的边界均保留；本轮没有引入数值或修改上一轮已核实的推导 |

示例 B L126–129 的原始能力与 SLO 容量区分、无量纲负载强度、固定 W 条件和利用率保留因子也未改变。取证记录 L26 的两处补充与正文一致，unknown 清单没有被改成测量或验证结论。上述抽查未发现已关闭项被本轮修订破坏，C01–C07 保持 CLOSED。

## 新增发现

**无。** 本轮仅检查三项修订及其相邻影响，没有将未修改区域扩展为新的完整审阅对象，也没有把仍缺现场数据的量登记为技术失败。

## 总体结论

**T00-03 在初审及两轮定向复核的范围内通过。** 本轮三项剩余发现全部关闭；累计 C01–C09、N01 共 10 项均为 CLOSED，OPEN 为 0，无新增发现。历史初审及第一轮复核报告保留当时结论，以本报告记录本轮关闭状态；本会话不更新正文、任务账本或其他审核元数据。

正文仍为 `draft / source_checked`。价格、扩展效率、实际故障损失、功耗与容量基线、b* 和 MLPerf 未取证轮次继续受正文 unknown 限制。本结论不替代硬件验证，也不代表其他 Batch 29 任务通过。

本轮起始工作区已有正文、取证及其他任务的未提交修改和审阅报告；它们不是本次写入。本会话仅新增本报告，对正文、取证、历史报告、registry 和相关导航文件进行哈希范围核对，保留既有工作区状态。未运行 `make check`、`make build`、`make test` 或其他 make 目标；未生成 build 产物，未执行训练、推理、故障注入、压测或能耗实验。
