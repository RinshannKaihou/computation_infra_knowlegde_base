---
id: hardware.rack-power-cooling-and-failure-domains
title: 机柜供电、散热预算与共享依赖
type: concept
domain: hardware
status: draft
platforms: [generic]
source_refs:
  - src.nvidia.dgx-superpod-dc-design-h100-2026-10-08
  - src.nvidia.dgx-gb200-user-guide-2026-09-17
  - src.nvidia.dgx-h100-h200-user-guide-2026-01-26
  - src.huawei.atlas-800t-a2-product-2026-09-29
  - src.hpe.gb200-nvl72-quickspecs-a50009224enw-v6
  - src.supermicro.supercluster-gb200-nvl72-datasheet-2025
  - src.dmtf.redfish-schemas-v1-2026.2
  - src.nvidia.nvidia-smi-docs-latest-2026-09-30
updated_at: "2026-10-09"
summary: 从节点额定/运行功耗、PDU 供电分组、冗余降额和冷却边界构造机柜级容量预算与共同故障域；区分持续、瞬态、冗余、余量四种口径，并给出容量验收、告警归因与单变量对照方法。
related_ids:
  - hardware.power-thermal-evidence
  - hardware.resource-topology
  - hardware.health-evidence
  - reliability.dimensions-and-failure-domains
verification:
  status: source_checked
  evidence_refs:
    - src.nvidia.dgx-superpod-dc-design-h100-2026-10-08
    - src.nvidia.dgx-gb200-user-guide-2026-09-17
    - src.hpe.gb200-nvl72-quickspecs-a50009224enw-v6
    - src.dmtf.redfish-schemas-v1-2026.2
  notes: "核对 NVIDIA 设计指南/用户指南、HPE/Supermicro 规格书与 DMTF Redfish schema；2026-10-09 补核 PowerSupplyMetrics v1.3.0 的 FanSpeedsPercent 数组及单数字段自 v1.1.0 废弃的边界。未执行任何机柜测量、断电或温控操作。"
---

# 机柜供电、散热预算与共享依赖

单个节点的电源/风扇规格回答「这台机器需要什么」，机柜级预算回答「这一柜能放几台、失效一路供电会怎样、散热是否足够」。本文解释机柜供电与散热预算的构造方法、设施到设备的影响链，以及容量验收与告警归因方法。设备侧降频/温度证据见[供电、散热与性能退化证据](power-thermal-evidence.md)；节点内部件与共享上游的记录字段见[计算节点资源与拓扑参考](resource-topology.md)。

`generic` 表示预算构造方法通用；具体数值、冗余级别和观察字段按机型与供电设计分别核对，机型规格不表示所有故障情形下的运行保证。

## 四种功率口径

机柜预算最常见的错误是把不同口径的功率混用。至少区分四种：

| 口径 | 含义 | 实例与来源 |
|---|---|---|
| 持续负载 | 长时间运行的平均功率 | NVIDIA DGX SuperPOD 设计指南为每组件列 EAP（expected average power）与 EPP（expected peak power），并在 planning 页组件功耗表脚注注明「DGX H100 systems operate at or near peak utilization continuously when running AI workloads」，故 DGX H100 的 EAP=EPP=10,200 W（[planning 页](https://docs.nvidia.com/dgx-superpod/design-guides/dgx-superpod-data-center-design-h100/latest/planning.html)，2026-10-08 观察） |
| 峰值/瞬态 | 短窗口的功率上冲 | HPE 为 GB200 NVL72 给出原文「TDP … 132 kW nominal with a EDPp (electrical design power – peak) of 1.5x TDP or approximately 192 kW」，并建议母线按 192 kW EDPp 预留（[QuickSpecs V6](https://www.hpe.com/us/en/collaterals/collateral.a50009224enw.html)，2026-09-08）。注意 1.5×132=198 与原文「approximately 192 kW」不一致，该出入存在于 HPE 原文（用了 approximately），本文如实保留而不擅自取其一；观测侧 nvidia-smi 区分「最近 1 秒平均」与「最近一次瞬时」两种功耗读数（[nvidia-smi 手册](https://docs.nvidia.com/deploy/nvidia-smi/index.html)） |
| 冗余后可承诺容量 | 失效情景下存活路径能承载的功率 | 该指南 electrical 页 Power Redundancy 节给出**容量定额要求**：「Each power source must be sized to support 50% of the total peak load」，机柜至少三路 rPDU、每路接 6 个 PSU 中的 2 个，「guaranteeing that a failure or maintenance event on any one of those sources will leave a minimum of four system power supplies energized」；负载分配约束在同页 Table 7 脚注 2：「a three circuit N+1 power provisioning scheme where no circuit carries more than 50% of the load」（[electrical 页](https://docs.nvidia.com/dgx-superpod/design-guides/dgx-superpod-data-center-design-h100/latest/electrical.html)，2026-10-08 观察） |
| 可用余量与搁浅容量 | 承诺容量减去已分配预算；因分组/相位不平衡而无法利用的部分 | 同一 Table 7 直接列出 Stranded Capacity（搁浅容量）0.6–12.4 kW |

参数化预算例（系数与数值均来自上述指南 Table 7 与对应页面，非实测）：

- 配电路径容量按接法分开定义，**不能把「3×线电压」当通用公式**：单相 `P = U × I × PF × d`；三相 `P = √3 × U_线 × I × PF × d`（Wye 接法也可写 `3 × U_相 × I × PF × d`，因 `U_相 = U_线/√3`）。指南 Table 7 的五行实例（照录）：`1Φ 230V 63A 100% → 13.7 kW`；`3Φ Delta 208V 60A 80% → 32.8 kW`；`3Φ Wye 400/230V 32A 100% → 21 kW`；`3Φ Wye 415/240V 32A 100% → 21.8 kW`；`3Φ Wye 415/240V 60A 80% → 32.7 kW`（表头分列 Distribution Voltage 与 Line Voltage，脚注 1 为 0.95 power factor）。复核：Wye 行按 `3 × 240 × 60 × 0.95 × 0.8 ≈ 32.8` 与表列 32.7 一致；Delta 行按上述线电压公式（`√3 × 208 × 60 × 0.95 × 0.8 ≈ 16.4`）**不能复现**表列 32.8，其电流/容量口径未从该页推出，本文不强行解释，引用时以表列值为准并标注此差异。
- 机柜持续预算：`P_rack = 台数 × 单台持续`，例：4 × 10.2 kW = 40.8 kW。密度口径：planning 页正文称 DGX H100「optimally deployed at a rack density of four systems per rack」；「Rack densities greater than 4 … are not recommended, due to thermodynamic considerations」则是 electrical 页 Table 7 脚注 3，两处不要混引。
- 冗余后可承诺：`P_commit = min(各失效情景下存活路径的容量合计)`；容量定额要求（每路按总峰值 50% 定额）与负载分配约束（三回路 N+1 下任一回路负载 ≤ 50%）是**两个方向不同的条件**，分别核对，不能合并写成「任一路径 ≤ 50% 峰值」。
- 瞬态预留：`P_busway ≥ k × TDP`，GB200 NVL72 实例 HPE 原文为「1.5x TDP or approximately 192 kW」（k 的名义值 1.5 与 192 kW 的算术出入见上，保留原文措辞）。
- 余量：`headroom = P_commit − P_rack持续 − 瞬态裕度`；搁浅容量单列，不计入可用余量。

## 风冷与液冷的观察点

风冷边界：NVIDIA 指南给 DGX H100 机柜最小风量 157 CFM/kW、ASHRAE A1 进风 15–32°C（DGX H100 允许上限 30°C）；DGX H100/H200 用户指南列整机气流 1105 CFM（80% fan PWM）、38,557 BTU/hr、工作温度 5–30°C（[用户指南](https://docs.nvidia.com/dgx/dgxh100-user-guide/introduction-to-dgxh100.html)，2026-01-26）。Atlas 800T A2 产品页列 4×2.6 kW 电源 2+2、8 个热插拔风扇模组 N+1、风冷、工作温度 5–35°C（[产品页](https://e.huawei.com/cn/products/computing/ascend/atlas-800t-a2)，2026-09-29 观察，可变网页）。

液冷边界：DGX GB200 用户指南描述 compute tray 由沿机柜的 manifold 供回液、经 CPU/GPU cold plate 冷却，其余部件风冷；机柜功耗约 120 kW，8 个 power shelf N+N（每 shelf 6×5.5 kW PSU、33 kW 输入），AC 转 50–51V DC 经 bus bar 配电；§1.7 有漏液检测专节，Mission Control 可监测供电与液冷并快速检漏（[DGX GB200 UG](https://docs.nvidia.com/dgx/dgxgb200-user-guide/hardware.html)，2026-09-17）。

同一 GB200 NVL72 机柜在不同资料中的功率数字必须按口径分列，不能合并成一个「规格」：

| 口径 | 数值与原文 | 出处 |
|---|---|---|
| 装机电源架 | NVIDIA：8 个 power shelf、每个 33 kW 输入（N+N）；HPE：「6 (max: 8) power shelves … Each power shelf can provide up to 33 kW」；Supermicro：「8x 1U 33kW (6x 5.5kW PSUs)」 | NVIDIA UG 2026-09-17；[HPE QuickSpecs V6](https://www.hpe.com/us/en/collaterals/collateral.a50009224enw.html)；[Supermicro 数据表](https://www.supermicro.com/datasheet/datasheet_SuperCluster_GB200_NVL72.pdf)（2025 年 2 月版） |
| 冗余/可用口径 | Supermicro 同表写「total power 132kW」——注意 8×33=264 kW 与 132 kW 并存，而其 Compute Tray 列另有「Shared power through 4+4 rack power shelves」；数据表未用文字明确 132 kW 是装机总额定还是 4+4 冗余下可用口径，本文照录原文并标注此歧义，不自行选定解释 | 同上 |
| 持续/设计功耗 | NVIDIA「approximately 120 kW」；HPE「TDP 132 kW nominal」；Supermicro「Operating Power 125kW to 135kW」 | 同上 |
| 瞬态预留 | HPE「EDPp … 1.5x TDP or approximately 192 kW」，建议母线按 192 kW 预留（1.5×132=198≠192 的出入在 HPE 原文，保留原文措辞） | HPE QuickSpecs V6 |

引用任何一项都必须带口径与出处；把「约 120 kW / TDP 132 kW / 运行 125–135 kW」取单一数写成通用规格是错误的。

遥测字段的标准化模型以 DMTF Redfish 为准（DSP2046 2026.2，[schemas/v1](https://redfish.dmtf.org/schemas/v1/)）：

| 观察点 | Redfish 资源（版本） | 关键字段 |
|---|---|---|
| 供电子系统 | PowerSubsystem v1.2.0 | PowerSupplies、PowerSupplyRedundancy、CapacityWatts、MaxRampRateWattsPerSecond、PowerBrake、Status |
| 单个 PSU | PowerSupplyMetrics v1.3.0 | InputPowerWatts、OutputPowerWatts、InputVoltage、TemperatureCelsius、EnergykWh、PowerLoadPercent、FanSpeedsPercent（数组） |
| 机柜/设备环境 | EnvironmentMetrics v1.7.0 | PowerWatts、PowerLimitWatts、EnergykWh、TemperatureCelsius、HumidityPercent、FanSpeedsPercent |
| 液冷单元 | CoolingUnit v1.6.0 | Primary/SecondaryCoolantConnectors、Pumps、CoolingCapacityWatts、LeakDetection、四类冗余 |
| 冷却液回路 | CoolantConnector v1.5.0 | Supply/ReturnTemperatureCelsius、DeltaTemperatureCelsius、FlowLitersPerMinute、HeatRemovedkW、Coolant 品质（pH/浊度/电导率） |
| 漏液 | LeakDetector v1.6.1 | DetectorState、PhysicalContext、Warning/CriticalReactionType |

注意：`Thermal` v1.7.3 已被标记废弃（in favor of `ThermalSubsystem`）；`PowerSupply.PowerOutputWatts/LineInputVoltage` 在新版本迁至 `PowerSupplyMetrics`。引用字段必须带 schema 版本。**Redfish schema 定义了「可以表达什么」，不等于具体设备实现了这些资源；设备能力以机型 BMC 文档和现场枚举为准。**

PSU 风扇优先核对 `FanSpeedsPercent` 数组：它自 v1.1.0 加入，用于表达多个风扇；单数 `FanSpeedPercent` 同时自 v1.1.0 标记废弃，在 v1.3.0 中保留作旧实现兼容字段（[PowerSupplyMetrics v1.3.0 JSON 的两个属性](https://redfish.dmtf.org/schemas/v1/PowerSupplyMetrics.v1_3_0.json)）。逐元素保留身份和读数，不能把单值当作全部风扇。设备未实现字段、属性缺失或读数为 null 均应记录 unknown，不能当作 0% 或无故障。

## 设施→机柜→PSU/风扇→设备的影响链

供电异常的典型链条：市电/配电异常 → rPDU 某一路掉电 → 该路所接 PSU 退出 → 冗余度下降。这里必须区分四个不同状态：**冗余降级**（冗余余量减少）、**容量不足**（存活路径无法承载负载）、**功率限制**（设备被强制压功耗）、**性能下降**（工作负载实际变慢）。以 DGX H100 的三路供电设计为例：每路接 6 个 PSU 中的 2 个，指南保证任一路失效后至少 4 个 PSU 带电（[electrical 页 Power Redundancy 节](https://docs.nvidia.com/dgx-superpod/design-guides/dgx-superpod-data-center-design-h100/latest/electrical.html)）——此时是冗余降级，不必然限性能。而 DGX H100/H200 用户指南的降性能条款针对更重的失效：「If three PSUs lose power … the system continues to function, but at a reduced performance level」（[电源冗余节](https://docs.nvidia.com/dgx/dgxh100-user-guide/introduction-to-dgxh100.html#support-for-psu-redundancy-and-continuous-operation)；该系统 6×3.3 kW PSU 4+2 冗余、至少 3 个 PSU 才能开机）。把三 PSU 失效条款外推到任意单路失效是错误的。nvidia-smi 的 Clock Event Reasons 中 `HW Power Brake` 表示外部 Power Brake 断言（如系统电源）触发降频——这是功率限制事件，同样不等于供电故障已定位。散热异常同理：进风温度升高或风量不足 → 风扇提速 → 设备温度逼近阈值 → 热降频。设备侧字段与 NPU/GPU 差异见[供电、散热与性能退化证据](power-thermal-evidence.md)。

液冷增加了新的共享依赖：manifold、CDU、泵与冷却液品质（Redfish 模型中的 FlowLitersPerMinute、供/回液温差、HeatRemovedkW、漏液检测）。一次 CDU 或泵故障可能影响整柜甚至整排（HPE 资料：1.3 MW in-row CDU 单台最多支持 8 柜）——故障域比风冷单机风扇更大，记录共享上游时必须包含冷却分配层级。

## 容量验收、告警归因与单变量对照

**容量验收**（规划层核对，非实测）：逐项核对 机柜台数×单台持续功率 ≤ 冗余后可承诺容量；瞬态预留按厂商 EDPp 或等效口径；风量/液冷流量满足厂商最小值；搁浅容量已记录。任何一项只能给出「按文档口径成立」的结论；实测容量验收属于验证轨道，本页不给出实测结果。

**告警归因**：从设备侧性能退化（降频位图、Aicore curFreq 与 Aicore Freq 读数差异、violation 计数）反查时，按 设备读数 → BMC/Redfish PSU/风扇/温度资源 → rPDU/配电 → 设施 的顺序逐层取证；任一单层证据不足以定位根因（例如功耗读数下降既可能是供电降额，也可能是负载变化；NPU 的 curFreq 差异也可能是空闲或策略限制，见[供电、散热与性能退化证据](power-thermal-evidence.md)）。同一节点时间线中设施/BMC/驱动/应用证据的对齐方法见该文的关联表。

**单变量对照**：验证「某供电/散热条件是否导致退化」时，只改变一个条件（例如按厂商维护流程临时退出一路供电、或在厂商允许范围内调整进风温度），保持负载、软件版本、并发与其他环境不变，观察功耗/频率/温度读数的变化方向；每组对照记录前提、操作、窗口与恢复步骤。此类操作影响供电或散热冗余，必须按现场授权与维护窗口执行，本文不授予执行权限。

## 适用边界

- 预算公式中的系数（80% 断路器降额、0.95 PF、50% 路径规则、1.5×EDPp）全部来自特定厂商设计指南/规格书，是**工程口径**而非通用标准；目标机房以当地电气规范与供电设计为准。
- 机型冗余级别（如 4+2 PSU、N+1 风扇、N+N power shelf）是设计口径：它说明设计允许哪类单点失效，不证明设备在所有失效组合、固件状态或负载下都不中断。NVIDIA 用户指南称 8 个 power shelf 为 N+N；Supermicro 数据表的「total power 132kW」与 8×33=264 kW 的口径歧义未解决（见上表）——冗余语义按具体 OEM 配置与文档逐条核对，不从功率除法推出保证。
- AMD OEM 节点的机柜级供电散热预算本轮未取得公开材料，保留 unknown；Redfish 液冷资源目前只有 schema 定义，无公开的 OEM 实际遥测实例。
- 数字规格（40.8 kW/柜、约 120 kW/柜、157 CFM/kW）绑定具体机型与文档版本，不外推到其他机型或机柜。

## 常见误解

- **「PSU 有冗余，断电一路没影响」**：冗余设计下单路失效首先是冗余降级（DGX 三路设计保证剩 ≥4 PSU 带电）；DGX 官方的「reduced performance level」条款针对三个 PSU 失效的更重情景。失效数量、接线和机型不同，后果不同；且冗余只在设计假定的失效模式内成立。
- **「设备没告警 = 供电散热正常」**：设备字段覆盖有限；冗余降额和渐进热退化可能无告警（见[静默错误与灰色退化](../08-reliability/silent-errors-and-integrity.md)）。
- **「机柜功率 = 各节点额定功率之和」**：忽略瞬态预留、冗余降额与搁浅容量，三者都是预算的一阶项。
- **「Redfish 有 CoolingUnit，所以设备能报液冷遥测」**：schema 是表达模型，实现按机型；当前无公开实测实例。
- **「液冷没有风扇问题」**：GB200 形态中仍有风冷部件与 power shelf 风扇；液冷引入的是另一组共享依赖（manifold/CDU/泵/漏液）。

## 例子与相关知识

容量规划时，把本页的预算表与[计算节点资源与拓扑参考](resource-topology.md)的共享上游字段一起使用：先定机柜内节点清单，再核对每个节点的供电分组与散热区，最后标注共同依赖（同一 rPDU、同一 CDU、同一风道）。设备侧已经怀疑供电/散热退化时，转[供电、散热与性能退化证据](power-thermal-evidence.md)；新节点入柜前的规格核对转[新节点与返修节点验收](node-acceptance-triage.md)；故障域与冗余的通用概念见[可靠性维度与故障域](../08-reliability/dimensions-and-failure-domains.md)。

## 来源与待确认问题

- [NVIDIA DGX SuperPOD Data Center Design Featuring DGX H100](https://docs.nvidia.com/dgx-superpod/design-guides/dgx-superpod-data-center-design-h100/latest/planning.html)（latest，2026-10-08 观察）：机柜密度、供电回路、EAP/EPP、风量。
- [NVIDIA DGX GB200 用户指南](https://docs.nvidia.com/dgx/dgxgb200-user-guide/hardware.html)（2026-09-17）：液冷结构、约 120 kW/柜、漏液检测。
- [HPE GB200 NVL72 QuickSpecs](https://www.hpe.com/us/en/collaterals/collateral.a50009224enw.html)（V6，2026-09-08）：TDP/EDPp 瞬态口径；[Supermicro 数据表](https://www.supermicro.com/datasheet/datasheet_SuperCluster_GB200_NVL72.pdf)（©2025）：运行功耗与 CDU 规格。
- [DMTF Redfish schemas](https://redfish.dmtf.org/schemas/v1/)（DSP2046 2026.2）：电源/散热/液冷遥测资源模型。
- [DGX H100/H200 用户指南](https://docs.nvidia.com/dgx/dgxh100-user-guide/introduction-to-dgxh100.html)、[Atlas 800T A2 产品页](https://e.huawei.com/cn/products/computing/ascend/atlas-800t-a2)、[nvidia-smi 手册](https://docs.nvidia.com/deploy/nvidia-smi/index.html)：机型规格与设备侧读数。
- 逐条主张与证据定位见[第十三批机柜供电散热来源记录](../../docs/research/batch-13-rack-power-sources.md)。
- 待确认：目标机房的实际供电分组、PDU 遥测与温度实测；AMD OEM 节点的机柜级材料；Redfish 液冷资源的设备实现实例；OCP ORv3 电源架规范（本轮仅候选记录，未逐页核对）。
