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
  notes: "已对照 Google SRE Implementing SLOs（错误预算）、MLPerf Inference 功耗测量政策（at-the-wall 边界，master 快照 2026-10-21）与 SuperBench 论文（灰色退化）核对引用表述；目标表、示例与验收表模板为本库原创整理。设备级功耗字段引用沿用 nvidia-smi/DCGM 既有登记口径，本轮未新开页面。"
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
| 成本 | 成本项清单×折旧期×利用率假设 | 货币/单位时间 | 本库无可引用市场价格来源，只用符号：`C_acq`（购置）、`C_energy`（能耗）、`C_facility`（机房/供电/散热）、`C_network`、`C_people`；折旧期 `T` 与利用率 `u` 是**假设**，必须显式登记 |
| 能耗 | 见下方测量边界分层 | W（功率）、J 或 kWh（能耗） | 设备级读数与墙表级实测不可互换；比较能效时必须声明边界 |

### 有效产出：训练与推理分别定义

- **训练有效进展**：以有效产出口径（pad/pack/过滤样本/跳过 step 的处理已写明）计的**净进展**，再扣除故障与恢复造成的重复计算——回退到旧 checkpoint 重算的 step、因降频/降级完成的低质量 step 都不能按正常产出计。总吞吐（含重算）≥有效进展，两者差距就是故障预算消耗的直读数。
- **推理 goodput**：同时满足已声明 SLO 的成功请求速率（定义与报告要件见[延迟与吞吐指标字典](../07-inference/latency-metrics.md)）；降级期间"仍在服务"的请求若低于质量判据，计入可用性但**不计入 goodput**，质量判据的设定见[隔离、重试预算、降级与恢复选择](../08-reliability/mitigation-and-recovery-principles.md)。

### 容量三词与冗余余量

- **资源峰值（铭牌/设计）**：设备或系统在设计条件下可达到的最大占用（如机柜 EAP/EPP 电力口径，见[机柜供电散热与故障域](../01-hardware/rack-power-cooling-and-failure-domains.md)）。
- **可用容量**：扣除冗余配置、已知故障域、维护窗口与调度碎片后，**可实际分配**给负载的部分。
- **冗余余量**：为可用性预留、平时不承载生产负载的部分（N+1 供电、备用节点、双副本的第二个）。冗余是**成本换可靠性**的显式交易：余量越大可用性越高、单位有效产出的成本越高。

### 能耗测量边界：四个层级不可混用

| 层级 | 测什么 | 典型手段 | 限制 |
|---|---|---|---|
| 设备级 | 单 GPU/NPU 功耗 | `nvidia-smi` 功耗字段、DCGM 功耗字段（既有登记口径） | 不含主机、内存、风扇、网络与电源损耗；采样口径按工具文档 |
| 整机级（at-the-wall） | 墙表交流输入 | 功率分析仪 | MLPerf Inference 功耗政策要求：系统级"at the wall"、包含受负载影响的全部组件（运行负载的主机处理器、加速器、内存、风扇等）、电源路径不得含储能，功耗与性能**来自同一次运行**、仅评测性能阶段（[power_measurement.adoc](https://github.com/mlcommons/inference_policies/blob/master/power_measurement.adoc)，master 快照） |
| 机柜级 | 机柜输入总功率 | 分支电路监测 | 含交换/存储等共享设备；多机柜共享的 CDU/供液损耗归属要声明 |
| 设施级 | PUE（总设施能耗/IT 能耗） | 电表级统计 | PUE 是设施指标，不能反推单作业能耗；比较单系统能效时必须退回整机级 |

规则：**任何能效比较必须先对齐层级与测量条件**；设备级读数除以 PUE 不等于该作业的墙表能耗，只是一种估算假设。

## 五类目标的冲突面

- 冗余↑（可靠性↑）⇒ 成本↑、可用容量↓（同批资源）。
- 批大小↑（吞吐↑）⇒ 排队延迟↑，P99 越界会把吞吐换成 goodput 下降。
- 降频/限功率（能耗↓）⇒ 性能↓；灰性性能退化还会被冗余掩盖（SuperBench 在 Azure GPU 环境的观察，[ATC 2024](https://www.usenix.org/conference/atc24/presentation/xiong)），因此验收必须含性能包络项。
- 高利用率（成本效率↑）⇒ 余量↓，故障时损失的服务与恢复时间↑。
- 快速扩缩容（跟随负载省成本）⇒ 冷启动与容量震荡风险（见[容量、扩缩容与冷启动决策](../07-inference/capacity-and-autoscaling.md)）。

## 假设计算示例

**以下两个示例全部使用符号与显式假设，没有任何实测或市场价格来源；结论只在该组假设下成立，假设改变时结论可能翻转（每例末尾列出翻转条件）。**

### 示例 A：单机 8 卡 → 两台 8 卡（训练侧扩容）

设：单机有效吞吐 `P`（tokens/s，有效产出口径）、可用性 `a`（单机作业级，重试与恢复后仍损失的窗口折算）、墙表功率 `W`、购置成本 `C_acq`、折旧期 `T` 年、平均利用率 `u`。两台同构节点经通用网络互联后，设扩展效率 `s`（≤1，通信与负载均衡损耗）。

```text
吞吐：两机 ≈ 2·s·P        （s<1 的每一点都是通信/均衡税）
可用性：作业级可用性随参与对象数变化——参与的设备/节点/链路任一不可用都可能中断作业；
        两机作业的故障对象数近似翻倍，恢复依赖 checkpoint 间隔与重启预算
成本：单位有效产出成本 ≈ (2·C_acq/T + 2·W·C_energy·u·8760) / (2·s·P·a')
能耗：单位有效产出能耗 ≈ 2·W / (2·s·P·a')（忽略网络设备能耗时要声明该假设）
```

其中 `a'` 是**含恢复损失的可用产出折算**（不是在线率：恢复窗口内重算的 step 不计入产出）。在 `s=1、a'=a` 的乐观假设下，单位成本/能耗与单机相同、吞吐翻倍；但 `s<1` 时单位成本/能耗按 `1/s` 变差，`a'` 因故障对象数增加而下降时进一步变差。**翻转条件**：若跨机通信开销使 `s` 低于某个阈值，或故障频率×恢复窗口使 `a'` 损失超过吞吐增益，两机方案的单位有效产出成本反而高于单机——这正是超节点域内高速互联与作业内弹性要优化的量（机制见[参考架构](reference-architectures.md)，量化须实测）。

### 示例 B：推理集群的冗余与批处理（服务侧）

设：负载 `R`（请求/s）、单副本容量 `c`（同 SLO 下）、副本数 `N=⌈R/c⌉`、单副本墙表功率 `W`、单副本成本 `C_acq`。两个决策：

1. **冗余**：`N+1` 部署使单副本故障时容量仍 ≥ `R`（可用性↑），代价是购置与能耗各增约 `1/N`，且日常平均利用率下降 `N/(N+1)`。若 `N` 较小（如 2→3），成本增幅显著；若 `N` 大，单副本故障时集群过载概率仍取决于剩余容量与突发余量的关系（`N+1` 不保证扛住并发双故障——那需要 `N+2` 或降级预案，见[处置选择](../08-reliability/mitigation-and-recovery-principles.md)）。
2. **批处理**：批大小 `b` 增大通常提高单副本吞吐 `c(b)`（收益递减），但排队延迟随负载强度 ρ=c(b) 上限逼近而陡增；**goodput 的 SLO 含延迟分位**，因此存在 `b*`：超过它后吞吐上升而 goodput 下降。`b*` 无法从铭牌推出，只能按负载混合与 SLO 实测（方法链接[容量验证](../05-cluster-platform/contention-capacity-validation.md)）。

两个决策叠加时注意交互：冗余副本在故障接管时往往承接突发流量，此时批大小策略应按**过载态**而非稳态设定，否则 `N+1` 的可用性收益被延迟越界吃掉。

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
- [MLPerf Inference 功耗测量政策](https://github.com/mlcommons/inference_policies/blob/master/power_measurement.adoc)（master 快照，2026-10-21）：核对 at-the-wall 边界、受影响组件清单、无储能要求、同一运行测功耗与性能、仅性能阶段、单表单 SUT 与分析仪/PTD 要求；具体精度/采样率数值该页未给（unknown）。
- [SuperBench，USENIX ATC 2024](https://www.usenix.org/conference/atc24/presentation/xiong)：核对冗余掩盖灰色退化（限其 Azure GPU 场景），支持"验收含性能包络"的主张；不外推任何阈值。
- 设备级功耗观测字段沿用 `nvidia-smi` 与 DCGM 文档的既有登记（Batch 13 核对口径），本文未新开页面。
