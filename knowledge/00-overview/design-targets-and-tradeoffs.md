---
id: overview.design-targets-and-tradeoffs
title: 设计目标与约束：可靠性、性能、容量、成本、能耗的权衡
type: reference
domain: overview
status: draft
platforms: [generic]
source_refs:
  - src.google.sre-implementing-slos
  - src.mlcommons.inference-power-policy
  - src.usenix.superbench-atc24
  - src.nvidia.nvidia-smi-docs-latest-2026-09-30
  - src.nvidia.dcgm-v3.3.9
updated_at: "2026-10-21"
summary: 把可靠性、性能、容量、成本、能耗五类设计目标统一成可比较的口径：分别定义训练有效进展与推理 goodput、资源峰值/可用容量/冗余余量、成本项与折旧/利用率假设、以及设备级到墙表级的能耗测量边界；用两个标为假设的符号化计算示例展示单机扩容与集群冗余/批处理的权衡，并给出正常/故障/恢复三窗口的目标与验收表模板。
related_ids:
  - overview.reference-architectures
  - reliability.dimensions-and-failure-domains
  - reliability.mitigation-and-recovery-principles
  - hardware.rack-power-cooling-and-failure-domains
  - hardware.node-selection-and-lifecycle
  - inference.latency-metrics
  - inference.capacity-and-autoscaling
  - training.performance-analysis
  - cluster-platform.contention-capacity-validation
  - data-storage.storage-workload-baselines
applicability:
  environment_refs: []
  notes: "跨平台设计方法与口径表。本文不含任何真实集群测量，不含市场价格（无登记来源，全部以符号表示）；两个计算示例明确标为假设，结论形式均为\"在该组假设下\"。"
verification:
  status: source_checked
  evidence_refs:
    - src.google.sre-implementing-slos
    - src.mlcommons.inference-power-policy
    - src.usenix.superbench-atc24
  notes: "已对照 Google SRE Implementing SLOs（错误预算）、MLPerf Inference 功耗测量政策（at-the-wall 边界，master 快照 2026-10-21）与 SuperBench 论文（灰色退化）核对引用表述；设备级读数边界于 2026-10-21 补核 nvidia-smi 文档三节（整板/模块/显存）。目标表、示例与验收表模板为本库原创整理；两个示例为符号推导，未实测。初审修订（C01–C09）后有效产出、容量四分、PUE 方向、示例 A 量纲与翻转条件、示例 B 负载强度均已改写。"
---

# 设计目标与约束：可靠性、性能、容量、成本、能耗的权衡

## 要回答的问题

同一批预算可以买更多节点、更大冗余或更高能效设备——"更好"在没有统一口径前无法比较。本文把五类目标各自的**对象、分母、单位与测量边界**固定下来，说明它们互相冲突的位置，并用两个标为假设的计算示例演示权衡的写法。系统形态（单机/集群/超节点）本身的比较见[单机、集群与超节点的参考架构及选择](reference-architectures.md)；本文回答"形态选定后，目标怎么设、怎么验收"。

## 五类目标的统一口径

| 目标 | 对象与分母 | 常用单位 | 口径要点与链接 |
|---|---|---|---|
| 可靠性 | 四维（可用性/正确性/性能稳定性/可恢复性）各自的合格事件/合格事件总数 | 比率、预算剩余 | 每项指标八要素见[可靠性维度与故障域](../08-reliability/dimensions-and-failure-domains.md)；错误预算（error budget）把容错额度显式化（[Implementing SLOs](https://sre.google/workbook/implementing-slos/)） |
| 性能 | 训练：有效产出口径下的吞吐；推理：绑定 SLO 的延迟分位与 goodput | tokens/s、samples/s、ms | 训练口径见[训练性能分解](../06-training/performance-analysis.md)（高利用率≠有效产出）；推理口径见[延迟与吞吐指标字典](../07-inference/latency-metrics.md)（无 SLO 集合即无 goodput） |
| 容量 | 见下方三词区分 | 卡数、tokens/s 上限、并发数 | 物理合计与作业可用容量是两回事（[参考架构](reference-architectures.md)比较表容量行）；多租户下的容量验证见[争用与容量验证](../05-cluster-platform/contention-capacity-validation.md) |
| 成本 | 成本项清单，按项计费/折算 | 货币/单位时间 | 本库无可引用市场价格来源，只用符号：`C_acq`（购置）、`C_energy`（能耗，货币/kWh）、`C_facility`（机房/供电/散热）、`C_network`、`C_people`；折旧期 `T` 与利用率 `u` 是**假设**，必须显式登记 |
| 能耗 | 见下方测量边界分层 | W（功率）、J 或 kWh（能耗） | 设备级读数与墙表级实测不可互换；比较能效时必须声明边界 |

### 有效产出：训练与推理分别定义

- **训练有效进展**：以有效产出口径（pad/pack/过滤样本/跳过 step 的处理已写明）计的**净进展**。扣除项按显式判据定义，而不是按速度：因故障回退到旧 checkpoint 后重算的 step 计入总吞吐但不计净进展；**仅因降频/降级而变慢、仍通过质量与状态判据的更新仍计有效进展**——变慢是性能维度的损失，不自动构成正确性损失；确实未过质量/一致性判据的更新才从净进展排除。三个量分开记录：总吞吐、净进展（有效进展）与重算量；SRE 式错误预算是另一对象（按声明的 SLI 事件/分母/窗口计算），与产出速率差之间**没有默认换算**，如需映射须写明同一有效工作单位与换算公式。
- **推理 goodput**：同时满足**已声明的逐请求条件**的成功请求速率——对每个成功请求逐项判定所提供的 TTFT/TPOT/E2E 阈值，全部满足才计 good completed，除以窗口时长（定义与报告要件见[延迟与吞吐指标字典](../07-inference/latency-metrics.md)）。三个易混口径分列：①逐请求联合合格（goodput 的定义）；②窗口延迟分位 gate（如窗口 P99 是否越界，是另一类观测，不是 goodput 本身）；③服务端分位与客户端逐请求判定的观测点差异。降级期间的请求如何归类按各自声明的合格事件定义处理：可用性契约决定它是否计入可用性；**只有当质量被显式声明为 goodput 条件并有对应判定时**，低于质量判据的请求才据此排除（质量判据的设定见[隔离、重试预算、降级与恢复选择](../08-reliability/mitigation-and-recovery-principles.md)）。

### 容量：供给上限、需求与余量分列

对同一资源对象（功率、卡数、副本容量）分别记录四行，不混成一个"容量"：

- **设计供给上限**：设备或系统在设计条件下可达到的最大供给（铭牌/设计功率、拓扑上限）。注意 EAP（平均功率需求）是**需求侧**例子不是峰值；EPP 才是峰值需求口径（样板见[机柜供电散热与故障域](../01-hardware/rack-power-cooling-and-failure-domains.md)）。
- **负载需求**：实际工作负载对该资源的占用（平均与峰值分开）。
- **可承诺容量**：给定失效组合下仍可供给的部分（如 N+1 供电时单路承载能力；多副本下容忍 `k` 个失效的剩余服务能力）。
- **故障余量**：供给减需求后的剩余，可表达为"对哪种失效组合仍满足 SLO 容量"。

**冗余的两种实现要分开**：空置备用（standby，平时不承载生产负载，故障时接管）与运行期共同承载（active-active，如双副本各担一半流量，故障时靠剩余容量接管——它的"余量"体现在剩余副本的 SLO 容量是否覆盖全部流量）。冗余是**成本换可靠性**的交易，但方向带条件：余量只有在冗余独立（跨相关故障域）、接管机制有效、剩余容量足够且有效产出不因降级大量流失时才转化为可用性；这些条件逐一核对前不作方向断言。**可用容量**是扣除冗余配置、已知故障域、维护窗口与调度碎片后**可实际分配**给负载的部分；物理合计与作业可用容量是两回事（[参考架构](reference-architectures.md)比较表容量行）。多租户下的容量验证见[争用与容量验证](../05-cluster-platform/contention-capacity-validation.md)。

### 能耗测量边界：四个层级不可混用

| 层级 | 测什么 | 典型手段 | 限制 |
|---|---|---|---|
| 设备级 | GPU/NPU 板级/模块级功耗 | `nvidia-smi` 功耗读数、DCGM 功耗字段 | 边界**按所选字段/实体声明**：nvidia-smi 的 GPU 功耗读数为整板功率（entire board，含 GPU 内存等板载组件，文档原文口径），另有模块级读数（GPU＋受支持 NVIDIA CPU＋其他组件，限 Hopper 及以上数据中心产品）与显存子系统读数；文档未声明这些读数与主机 DRAM、机箱风扇、电源转换损耗的关系——不从工具名推定排除清单，采样口径按工具文档（[nvidia-smi GPU Power Readings](https://docs.nvidia.com/deploy/nvidia-smi/index.html)，2026-10-21 补核） |
| 整机级（at-the-wall） | 墙表交流输入 | 功率分析仪 | MLPerf Inference 功耗政策要求：系统级"at the wall"、包含受负载影响的全部组件（运行负载的主机处理器、加速器、内存、风扇等）、电源路径不得含储能，功耗与性能**来自同一次运行**、仅评测性能阶段（[power_measurement.adoc](https://github.com/mlcommons/inference_policies/blob/master/power_measurement.adoc)，master 快照） |
| 机柜级 | 机柜输入总功率 | 分支电路监测 | 含交换/存储等共享设备；多机柜共享的 CDU/供液损耗归属要声明 |
| 设施级 | PUE（总设施能耗/IT 能耗） | 电表级统计 | PUE 是设施指标，不能反推单作业能耗；比较单系统能效时必须退回整机级 |

规则：**任何能效比较必须先对齐层级与测量条件**。设备级读数与墙表能耗之间是**组件边界缺口**（缺主机、风扇、网络、电源损耗等，缺口大小未测即 unknown）；IT 能耗与设施能耗之间才存在 `设施能耗 = PUE × IT 能耗` 的代数关系（要求同周期、同边界；分摊到单作业还须另作假设）。不存在"设备功率除以 PUE"这类换算。

## 五类目标的冲突面

- 冗余↑（可靠性↑）⇒ 成本↑、可分配容量↓（同批资源）；可用性收益以独立性、接管与剩余容量条件为前提。
- 批大小↑可提高原始吞吐，但也引入凑批等待并改变排队——是否越界逐请求延迟条件、goodput 是否下降，由固定负载与策略下两股相反效应的实测判断（见示例 B）。
- 限功率是**功率约束**，不是能耗结论：功率降低而完成时间增加时，同一有效工作的总能耗（E=∫P dt）可能升也可能降，方向须同窗实测。
- 灰性性能退化还会被冗余掩盖（SuperBench 在 Azure GPU 环境的观察，[ATC 2024](https://www.usenix.org/conference/atc24/presentation/xiong)），因此验收必须含性能包络项。
- 高利用率（成本效率↑）⇒ 余量↓，故障时损失的服务与恢复时间↑。
- 快速扩缩容（跟随负载省成本）⇒ 冷启动与容量震荡风险（见[容量、扩缩容与冷启动决策](../07-inference/capacity-and-autoscaling.md)）。

## 假设计算示例

**以下两个示例全部使用符号与显式假设，没有任何实测或市场价格来源；结论只在该组假设下成立，假设改变时结论可能翻转（每例末尾列出翻转条件）。**

### 示例 A：单机 8 卡 → 两台 8 卡（训练侧扩容）

符号与假设先登记（`P` 只计运行窗口；空闲功率忽略并声明；`a'` 内的故障损失恰好折算一次，不与 `P` 重复扣）：

```text
P   单机运行期有效吞吐（tokens/s，有效产出口径）
W   单机运行期平均墙表功率（kW）；u  计划运行时间占比（0–1，年口径）
a、a'  单机 / 两机运行窗口的净产出折算（有效进展 ÷ 名义进展；重算与失败窗口按显式判据折入）
s   两机扩展效率（≤1，通信与负载均衡损耗）
C_acq 单机购置（货币）；T 折旧期（年）；C_energy 电价（货币/kWh）；H=8760 h/年
```

年度量（两机；单机同法）：

```text
年净产出   Q₂ = 2·s·P·u·a'·H·3600        （tokens/年）
年成本     K₂ = 2·C_acq/T + 2·W·u·H·C_energy   （货币/年）
单位净产出成本 = K₂/Q₂（货币/token）；能耗 E₂=2·W·u·H（kWh/年），单位净产出能耗 = E₂/Q₂
```

比值推导（同 `u`/`W`/`C_acq`、各折算恰用一次）：

```text
两机净产出速率 / 单机 = 2·s·a'/a
两机单位净产出成本 / 单机 = 两机单位净产出能耗 / 单机 = a/(s·a')
```

**在该组假设下**：总吞吐增加的条件是 `s·a' > a/2`（未取值时不能判断目标任务是否满足，不预设其通常成立）；而单位成本/单位能耗更低需要 `s·a' > a`，在 `s≤1` 且 `a'≤a` 的损耗情形下**恒不成立**——即两机方案买到的是吞吐规模与故障域变化（如单节点故障只损失一半部署，该收益须按作业组织方式另声明，本例未计入 `a'`），不是更便宜的 token。要示范单位成本翻转，须另设不同的价格/功率/效率假设（如共享网络设备摊薄）并显式登记；零净产出时单位成本不可计算。这正是超节点域内高速互联与作业内弹性要优化的量（机制见[参考架构](reference-architectures.md)，量化须实测）。

### 示例 B：推理集群的冗余与批处理（服务侧）

符号：负载 `R`（请求/s）、单副本 **SLO 有效容量** `c`（该 SLO 下每秒可完成且达标的请求上限）、副本数 `N=⌈R/c⌉`、单副本墙表功率 `W`。两个决策：

1. **冗余**：`N+1` 部署在"**容量可加、接管后重新均衡**"的声明假设下，使单副本故障时剩余 `N·c ≥ R` 仍覆盖负载。注意这只是**稳态容量**覆盖：接管窗口（路由收敛、缓存冷启动、流量重均衡期间）的表现不在该不等式内，须实测；购置与能耗各增约 `1/N`（能耗增幅条件＝每副本 `W` 同周期常量）；平均利用率 `U_N=R/(N·c)`、`U_{N+1}=U_N·N/(N+1)`（后者是相对保留因子，不是下降百分点）。`N+1` 不保证扛并发双故障——那需要 `N+2` 或降级预案（见[处置选择](../08-reliability/mitigation-and-recovery-principles.md)）。
2. **批处理**：区分两个量——原始服务能力 `c_raw(b)`（不受延迟约束的吞吐）与 SLO 有效容量 `c(b)`；每副本到达率 `λ=R/M`（`M`=实际服务副本数），负载强度 `ρ=λ/c_raw(b)`（无量纲）。固定 `λ` 时 `b` 增大→`c_raw(b)` 通常增大→`ρ` 下降；但**凑批等待**（等 batch 凑满的时间）与长度分布差异引入另一类延迟，可能使逐请求延迟条件越界——两股效应方向相反。因此**不预设转折点存在**：`b*`（吞吐升而 goodput 降的转折）可能存在也可能不在（最佳点可能落在允许区间端点），按预登记候选集合与目标负载实测（方法链接[容量验证](../05-cluster-platform/contention-capacity-validation.md)与[延迟与吞吐指标字典](../07-inference/latency-metrics.md)）。

两个决策叠加时注意交互：冗余副本在故障接管时承接突发流量，此时批大小策略应按**过载态**而非稳态设定，否则 `N+1` 的可用性收益被延迟越界吃掉。

## 目标与验收表模板

为每项设计目标按下表登记三个窗口。失败阈值的设定方法只有两类：**来自已验证基线**（同口径历史数据或领域级验证方法的结果，如[带宽基线](../03-communication/bandwidth-baselines.md)、[存储负载基线](../04-data-storage/storage-workload-baselines.md)、[节点验收](../01-hardware/node-acceptance-triage.md)），或**来自业务约定并显式标为约定**；没有来源的阈值必须标 unknown。

| 窗口 | 观测字段（示例） | 失败阈值设定方法 | 通过判据 |
|---|---|---|---|
| 正常 | goodput/有效进展、延迟分位、功耗、利用率、错误分类计数 | 基线包络（如基线±噪声带，噪声带须有数据支撑） | 连续窗口达标且无越界趋势 |
| 故障 | 受影响范围（域）、错误率、容量余量、降级状态 | 按故障模型预登记（每类故障的最大允许影响范围） | 影响不超出预登记域；降级按预案执行 |
| 恢复 | 恢复时间、进度损失（重算量）、状态一致性校验、性能回包络时间 | 恢复门槛（时间/损失上限）按业务设定并标为约定 | 六条退出条件全部满足（见[可靠性维度](../08-reliability/dimensions-and-failure-domains.md)恢复门槛） |

**不可比较条件**（违反即不可比）：SLO 集合不同（goodput 无意义）；有效产出口径不同（是否扣重算、pad 处理）；能耗层级不同（设备级 vs 墙表）；窗口与聚合不同（分位 vs 平均）；负载混合与版本不同；观测点不同（客户端 vs 服务端）。

## 适用边界与待确认

- 本文不含任何真实集群的量化结论；示例 A/B 的所有符号值未取数。补齐需要：目标环境的价格来源（或维持符号化）、同口径基线测量、按 MLPerf 式边界声明的能耗实测——这些属于独立验证轨道，正文完成不等于验证完成。
- MLPerf 功耗政策是**基准提交规则**，本文只取其测量边界定义（at-the-wall、同一次运行、含受影响组件）；不构成对本库任何环境的测量承诺，其"仅 performance 阶段"等规则也不自动适用于日常监控口径。
- 机柜级供电/散热的口径与机型文档绑定（见 01 域样板），跨机型比较前须按对应文档核对；设施级 PUE 属运营数据，本库无登记来源。
- 成本的完整口径（折旧方法、资金成本、人力分摊）超出本文范围；本文只要求把假设显式化。

## 来源核对范围

- [Google SRE Workbook：Implementing SLOs](https://sre.google/workbook/implementing-slos/)：核对错误预算概念与 SLI 事件比率表达；未采用其示例阈值。
- [MLPerf Inference 功耗测量政策](https://github.com/mlcommons/inference_policies/blob/master/power_measurement.adoc)（master 快照＝commit d3eba2f，2026-10-21）：核对 at-the-wall 边界、受影响组件清单、无储能要求、同一运行测功耗与性能、仅性能阶段。**器材限制属历史提交条件且两类条款范围不同**：单表单 SUT、仅 Yokogawa 分析仪按固定原文明确列出 v1.0/v1.1/v2.0 三轮（原文 L154–159/L216–219）；"不适用拆分式系统（disaggregated systems）"是所取 v2.0 版本文件的本版本限制（原文 L65），更早轮次是否同样限制未取证（unknown）。本篇只采用其测量边界原则，后续轮次的支持矩阵亦未取证（unknown）。具体精度/采样率数值该页未给（unknown）。
- [SuperBench，USENIX ATC 2024](https://www.usenix.org/conference/atc24/presentation/xiong)：核对冗余掩盖灰色退化（限其 Azure GPU 场景），支持"验收含性能包络"的主张；不外推任何阈值。
- 设备级功耗读数边界：本轮补核 [nvidia-smi 文档](https://docs.nvidia.com/deploy/nvidia-smi/index.html) 的 GPU Power Readings（整板功率，"entire board"）、Module Power Readings（GPU＋受支持 NVIDIA CPU＋其他组件，限 Hopper 及以上数据中心产品）与 GPU Memory Power Readings（显存子系统）三节（2026-10-21）；页面未声明这些读数与主机 DRAM/机箱风扇/电源损耗的关系。DCGM 功耗字段沿用既有登记口径（Batch 13）。
