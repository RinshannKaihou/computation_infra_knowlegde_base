# 第二十九批 T00-03 来源记录

任务：T00-03（容量、成本、能耗与可靠性目标的设计权衡；**new** `knowledge/00-overview/design-targets-and-tradeoffs.md`，主题 00.4/00.5）。取证轮次：主会话作者角色首轮（2026-10-21；跨批前置 T01-01/T04-06/T05-07 均已 done）。

## 新增来源与主张定位

| 主张 | 登记 ID | 精确位置 | 支持范围 |
|---|---|---|---|
| 功耗按系统级 at-the-wall 测量；含受 LoadGen 影响的全部组件（主机处理器/加速器/内存/风扇等）；电源路径不得含储能；功耗与性能须同一次运行、仅 performance 阶段；**器材限制两类条款范围不同**：单表单 SUT、仅 Yokogawa 分析仪按固定原文明确列出 v1.0/v1.1/v2.0 三轮（原文 L154–159/L216–219，页首标 v2.0、更新 2022-01-05）；"不适用拆分式系统"为所取 v2.0 版本文件的本版本限制（原文 L65），更早轮次未取证（unknown）；director/PTD 职责；无法复现的结果无效 | src.mlcommons.inference-power-policy（**本轮新增**） | [power_measurement.adoc](https://github.com/mlcommons/inference_policies/blob/master/power_measurement.adoc)（master 快照 commit d3eba2f，2026-10-21 WebFetch 核对；仓库 Apache-2.0 经 GitHub 页面 SPDX 确认） | 能耗测量边界表的整机级行与"层级不可混用"规则；本篇只采用测量边界原则，器材清单属历史提交条件、后续轮次支持矩阵未取证（unknown）；不构成日常监控承诺 |

## 复用来源与主张定位

| 主张 | 登记 ID | 精确位置 | 支持范围 |
|---|---|---|---|
| 错误预算概念与 SLI 事件比率 | src.google.sre-implementing-slos | [Implementing SLOs](https://sre.google/workbook/implementing-slos/)（2026-09-29 已核） | 可靠性目标行与故障预算引用 |
| 冗余掩盖灰色退化、验证代价权衡 | src.usenix.superbench-atc24 | [ATC 2024](https://www.usenix.org/conference/atc24/presentation/xiong)（既有核对口径） | "验收含性能包络"主张 |
| 设备级功耗读数边界：GPU Power Readings＝整板功率（entire board，含 GPU 内存等板载组件）；Module Power Readings＝GPU＋受支持 NVIDIA CPU＋其他组件（限 Hopper 及以上数据中心产品）；GPU Memory Power Readings＝显存子系统；页面未声明与主机 DRAM/机箱风扇/电源损耗的关系 | src.nvidia.nvidia-smi-docs-latest-2026-09-30、src.nvidia.dcgm-v3.3.9 | [nvidia-smi 文档](https://docs.nvidia.com/deploy/nvidia-smi/index.html) 三节（2026-10-21 初审修订轮补核）；DCGM 字段沿用既有登记（Batch 13） | 能耗边界表设备级行——按所选字段/实体声明边界，不从工具名推定排除清单；NPU 字段未核（unknown） |
| goodput 定义与报告要件（逐请求联合合格条件、无 SLO 集合即无 goodput；窗口分位 gate 与逐请求判定分列） | 07 域正文 | [latency-metrics](../../knowledge/07-inference/latency-metrics.md) | 有效产出定义（推理侧）；降级请求归类按各自声明的合格事件定义 |
| 有效产出口径（pad/pack/过滤样本/利用率≠有效产出；变慢但合格的更新仍计有效进展，扣除按显式质量/状态判据） | 06 域正文 | [performance-analysis](../../knowledge/06-training/performance-analysis.md) | 有效产出定义（训练侧）；总吞吐/净进展/重算量/SRE 错误预算四个对象分记 |
| 容量物理合计 vs 作业可用、比较表容量行 | 本批 T00-02 交付正文 | [reference-architectures](../../knowledge/00-overview/reference-architectures.md) | 容量三词的衔接（本文已同步该文两处 T00-03 前向引用） |
| 机柜供电口径：设计供给上限/负载需求（EAP 平均、EPP 峰值为需求侧）/可承诺容量/故障余量四分；N+1 等冗余样板 | 01 域已核登记 | [rack-power-cooling-and-failure-domains](../../knowledge/01-hardware/rack-power-cooling-and-failure-domains.md) | 容量四分定义的样板事实（数值不重复；EAP 不是峰值） |
| 多租户容量验证方法 | 05 域正文 | [contention-capacity-validation](../../knowledge/05-cluster-platform/contention-capacity-validation.md) | 验收表"基线"阈值来源链接 |

## 本文原创部分

五类目标统一口径表、有效产出两侧定义（扣除项按显式判据、四个对象分记）、容量供给/需求四分与两种冗余实现、能耗四层级表（设备/整机 at-the-wall/机柜/设施 PUE 不可混用规则；设备级与 IT→设施两个边界分开）、五类冲突面清单、两个假设计算示例（符号化；示例 A 年度量纲闭合、单位成本比 a/(s·a') 与翻转条件 s·a'>a 分列（吞吐条件 s·a'>a/2 不预设通常成立）；示例 B λ/c_raw(b) 负载强度、b* 为预登记待测点不预设存在、冲突面概述同条件化）、三窗口验收表模板与不可比较条件清单。初审修订（C01–C09）同步：有效产出、容量、PUE 方向、示例 A 量纲与翻转、示例 B ρ 与 b* 均已改写。

## unknown 清单

1. 市场价格：无可引用单价来源，成本全部以符号表示（`C_acq`/`C_energy`/`C_facility` 等）；引入价格时须另登记可追溯来源或显式假设。
2. 两个示例的符号均未取数；任何代入数值后的结论须重新验证（示例已标注"假设，非实测"；示例 A 的比较条件为显式不等式 s·a'>a/2 与 s·a'>a，示例 B 的 b* 为预登记候选集合上的待测点）。
3. MLPerf 功耗政策的精度/采样率具体数值该页未给（unknown）；其规则限推理基准提交语境。
4. 设施级 PUE、跨机柜 CDU/供液损耗归属：无登记来源，正文只要求显式声明归属。
5. 完整成本口径（折旧方法、资金成本、人力分摊）超出本文范围，正文已声明。
