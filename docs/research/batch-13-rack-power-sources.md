# 第十三批来源记录：机柜供电、散热预算与共享依赖（T01-01）

研究日期：2026-10-08。研究者：探索子代理（非 gpt-6.1-sol）。目标正文：`knowledge/01-hardware/rack-power-cooling-and-failure-domains.md`（concept，planned，验收标准见 plans/full-coverage-backlog.yaml T01-01）。范围：DMTF Redfish 电源/散热/液冷资源模型、NVIDIA 机柜级设计指南与 GB200 液冷用户指南、OEM 瞬态功率口径、nvidia-smi 功耗观测口径。未执行任何设备查询或容量实测；除本文件外未改动仓库其他文件。

## 主张—证据表（机柜预算与供电分组）

| 主张 | 来源与定位 | 版本/日期 | 证据性质 | 反例/未知 |
|---|---|---|---|---|
| DGX H100 最优 4 台/机柜；1/2/4 台对应每机柜 10.2/20.4/40.8 kW；脚注：超过 4 台因热力学原因不推荐 | [DGX SuperPOD Data Center Design Featuring DGX H100, planning](https://docs.nvidia.com/dgx-superpod/design-guides/dgx-superpod-data-center-design-h100/latest/planning.html) Table 2 | latest 可变页，2026-10-08 观察 | 厂商设计指南 | 仅 H100 风冷形态；其他机型不适用 |
| 供电回路计算（Table 7 照录，表头含 Phase/Distribution Voltage/Line Voltage/Amps/Breaker Derating/Circuit Capacity/Stranded Capacity 等列）：1Φ 230V 63A 100%→13.7 kW；3Φ Delta 208V 60A 80%→32.8 kW；3Φ Wye 400/230V 32A 100%→21 kW；3Φ Wye 415/240V 32A 100%→21.8 kW；3Φ Wye 415/240V 60A 80%→32.7 kW；脚注 1：0.95 PF；脚注 3："Rack densities greater than 4 DGX H100 Systems are not recommended, due to thermodynamic considerations" | 同文档 [electrical](https://docs.nvidia.com/dgx-superpod/design-guides/dgx-superpod-data-center-design-h100/latest/electrical.html) Table 7 | 同上 | 厂商工程口径 | 复核：Wye 行 3×240×60×0.95×0.8≈32.8 与表列 32.7 一致；Delta 行按 √3×208×60×0.95×0.8≈16.4 不能复现表列 32.8，口径未推出，以表列值为准并标注差异（B13-C03 修订：通用公式按接法分开，不用「3×线电压」）；>4 台脚注在 electrical 页而非 planning 页（B13-C14） |
| 冗余口径：容量定额要求 "Each power source must be sized to support 50% of the total peak load"（Power Redundancy 节；另 rPDU Selection 节 "Each of the three required power input paths must support one half of the expected peak power"）；负载分配约束为 Table 7 脚注 2 "a three circuit N+1 power provisioning scheme where no circuit carries more than 50% of the load"；三路 rPDU 各接 6 PSU 中的 2 个，"guaranteeing that a failure or maintenance event on any one of those sources will leave a minimum of four system power supplies energized" | 同文档 electrical 页 | 同上 | 厂商设计指南 | 容量定额（≥50%）与负载分配（≤50%）是两个方向不同的条件，不能合并（B13-C03）；单路失效剩 ≥4 PSU 是冗余降级，不等于必然降性能（B13-C05） |
| 持续 vs 峰值：每组件 EAP（expected average power）与 EPP（expected peak power）；**planning 页**组件功耗表脚注 2："DGX H100 systems operate at or near peak utilization continuously when running AI workloads"，故 EAP=EPP=10,200 W；planning 页 Table 2（1/2/4 台 → 10.2/20.4/40.8 kW）无脚注，另有正文 "optimally deployed at a rack density of four systems per rack" | 同文档 [planning](https://docs.nvidia.com/dgx-superpod/design-guides/dgx-superpod-data-center-design-h100/latest/planning.html) | 同上 | 厂商声明 | EAP=EPP 脚注在 planning 页而非 electrical 页（B13-C14）；非满载负载不成立 |
| 散热：最小风量 157 CFM/kW；ASHRAE A1 15–32°C（DGX H100 允许上限 30°C） | 同文档 planning 页 | 同上 | 厂商设计指南 | 与 DGX H100/H200 用户指南 1105 CFM@80%PWM、38,557 BTU/hr 并存（已登记 src.nvidia.dgx-h100-h200-user-guide-2026-01-26） |

## 主张—证据表（液冷与瞬态）

| 主张 | 来源与定位 | 版本/日期 | 证据性质 | 反例/未知 |
|---|---|---|---|---|
| DGX GB200：机柜功耗约 120 kW；8 个 power shelf N+N，每 shelf 6×5.5 kW PSU、33 kW 输入；AC 转 50–51V DC 经 bus bar 配电 | [DGX GB Rack Scale Systems User Guide](https://docs.nvidia.com/dgx/dgxgb200-user-guide/hardware.html) §1.4（[PDF](https://docs.nvidia.com/dgx/dgxgb200-user-guide/dgxgb200-user-guide.pdf)） | PDF 更新 2026-09-17 | 厂商手册 | 与 OEM 口径差异见冲突节 |
| 液冷结构：compute tray 由沿机柜 manifold 供回液、经 CPU/GPU cold plate 冷却；其余部件风冷；§1.7 有 Leak Detection 专节，Mission Control 可监测供电与液冷并快速检漏 | 同上 §1.2/§1.7 | 同上 | 厂商手册 | 无流量/温度设定值公开 |
| HPE GB200 NVL72：「6 (max: 8) power shelves … Each power shelf can provide up to 33 kW」；「The rack's TDP (thermal design power) is 132 kW nominal with a EDPp (electrical design power – peak) of 1.5x TDP or approximately 192 kW」；「HPE suggests that data centers should provision their bus ways to be able to support 192 kW EDPp」；1 shelf = 6×5.5 kW PSU + PMC；50 V DC Busbar；in-row CDU 1.3 MW 单台最多 8 柜 | [HPE QuickSpecs a50009224enw](https://www.hpe.com/us/en/collaterals/collateral.a50009224enw.html) Power Delivery 段 | V6，2026-09-08 | OEM 规格书 | 1.5×132=198 与「approximately 192 kW」不一致，出入在 HPE 原文（用了 approximately），如实保留不擅自取其一（B13-C04）；「约」值非实测 |
| Supermicro GB200 NVL72（2025 年 2 月版）：「Power Shelves: 8x 1U 33kW (6x 5.5kW PSUs), total power 132kW」；「Operating Power: 125kW to 135kW」；Compute Tray 列另有「Shared power through 4+4 rack power shelves」；in-rack 4U 250 kW CDU（冗余 PSU、双热插拔泵）；可选 in-row 1.3 MW 或 180/240 kW liquid-to-air | [Supermicro datasheet](https://www.supermicro.com/datasheet/datasheet_SuperCluster_GB200_NVL72.pdf)（pdftotext -layout 恢复文本层） | 2025 年 2 月版，©2025 | OEM 数据表 | 8×33=264 与「total power 132kW」并存，数据表未用文字明确 132 kW 是装机总额定还是 4+4 冗余下可用口径，照录原文并标注歧义（B13-C04）；注意可能已有更新版 |
| 功耗观测两口径：Average Power Draw=最近 1 秒平均；Instantaneous Power Draw=最近一次测量；封顶为功耗管理算法强制上限（Enforced Power Limit）；HW Power Brake=外部 Power Brake 断言（如系统电源）触发 | [nvidia-smi 手册](https://docs.nvidia.com/deploy/nvidia-smi/index.html) Power Readings/Limits、Clock Event Reasons（已登记 src.nvidia.nvidia-smi-docs-latest-2026-09-30） | latest | 厂商文档 | 采样窗口随驱动版本可变 |

## 主张—证据表（Redfish 资源模型）

| 主张 | 来源与定位 | 版本/日期 | 证据性质 | 反例/未知 |
|---|---|---|---|---|
| DSP2046《Redfish Resource and Schema Guide》当前 2026.2（2026-09-14）；schemas/v1/ 文件时间 2026-09-15 | [DSP2046](https://www.dmtf.org/dsp/DSP2046)、[schemas 目录](https://redfish.dmtf.org/schemas/v1/) | 2026.2 | 标准规范 | DSP8010 bundle zip 被 Cloudflare 403，未核对 |
| PowerSubsystem v1.2.0：PowerSupplies、PowerSupplyRedundancy、CapacityWatts、MaxRampRateWattsPerSecond（AC 爬升速率上限）、PowerBrake、Status | redfish.dmtf.org/schemas/v1/PowerSubsystem.v1_2_0.json | 2026.2 | 标准规范 | 规范存在不等于设备实现 |
| PowerSupply v1.8.0：PowerCapacityWatts、InputRanges、LineInputStatus、Metrics；旧字段 PowerOutputWatts/LineInputVoltage 已迁至 PowerSupplyMetrics v1.3.0（InputPowerWatts/OutputPowerWatts/InputVoltage/TemperatureCelsius/EnergykWh/PowerLoadPercent/FanSpeedsPercent 数组） | [PowerSupplyMetrics v1.3.0 JSON](https://redfish.dmtf.org/schemas/v1/PowerSupplyMetrics.v1_3_0.json) 对应属性 | 2026.2 | 标准规范 | 2026-10-09 B13-R04 修订：FanSpeedsPercent 的 versionAdded=v1_1_0；单数 FanSpeedPercent 的 versionDeprecated=v1_1_0，为多风扇改用数组，旧字段仅作兼容；缺失/null 不等于 0%，规范不证明设备实现 |
| Thermal v1.7.3 已废弃（in favor of ThermalSubsystem）；新模型：ThermalSubsystem v1.5.0（Fans/Pumps/CoolantConnectors/LeakDetection/FanRedundancy/ThermalMetrics）、Fan v1.6.0（SpeedPercent/PowerWatts）、EnvironmentMetrics v1.7.0（PowerWatts/PowerLimitWatts/EnergykWh/TemperatureCelsius/HumidityPercent/FanSpeedsPercent） | 同目录对应 JSON | 2026.2 | 标准规范 | Thermal.Temperatures[].ReadingCelsius/Fans[].Reading 仅作兼容背景 |
| 液冷：CoolingUnit v1.6.0（Primary/SecondaryCoolantConnectors、LeakDetection、Pumps、CoolingCapacityWatts、四类冗余）；CoolantConnector v1.5.0（Supply/ReturnTemperatureCelsius、DeltaTemperatureCelsius、FlowLitersPerMinute、RatedFlowLitersPerMinute、HeatRemovedkW、Coolant 及 pH/Turbidity/Conductivity）；LeakDetector v1.6.1（DetectorState、PhysicalContext、Warning/CriticalReactionType） | 同目录对应 JSON | 2026.2 | 标准规范 | 无公开 OEM 实际遥测实例 |
| DMTF 版权政策：成员与非成员可复制定规范文档，须正确署名并标注版本与发布日期 | [DMTF copyright policy](https://www.dmtf.org/about/policies/copyright)；每个 schema JSON 含 Copyright 2014-2026 DMTF | 2026-10-08 核对 | 许可原文 | 引用时标注版本 |

## 候选新来源登记

`src.dmtf.redfish-schemas-v1-2026.2`、`src.nvidia.dgx-superpod-dc-design-h100-2026-10-08`、`src.nvidia.dgx-gb200-user-guide-2026-09-17`、`src.hpe.gb200-nvl72-quickspecs-a50009224enw-v6`、`src.supermicro.supercluster-gb200-nvl72-datasheet-2025`。OCP ORv3 Power Shelf（6×3 kW、15 kW N+1、48V）仅作候选记录，实取为 2020-10-15 贡献版、正式 v1.0（NOV22）PDF 未逐页核对，本轮不登记、不进正文。

## 缺口与冲突

- 功率口径冲突：NVIDIA UG「approximately 120 kW」、HPE「TDP 132 kW nominal / EDPp 1.5x TDP or approximately 192 kW」、Supermicro「total power 132 kW / Operating Power 125–135 kW」并存；1.5×132=198≠192 的出入在 HPE 原文；正文按装机/冗余可用/持续设计/瞬态预留四种口径分列（B13-C04 修订）。
- 冗余口径差异：NVIDIA 用户指南称 8 个 power shelf 为 N+N；Supermicro 数据表「total power 132kW」与 8×33=264 kW 的口径歧义未解决（数据表未用文字明确，Compute Tray 列有「4+4 rack power shelves」）。不可把「8 shelf」写成「任意 4 个失效仍满性能」；不从功率除法推出冗余保证（B13-C04 修订，删除原「HPE 需 6 active、8 才 N+1」的无支持表述）。
- NVIDIA GB200 NVL72 产品页无功率数字（仅 "rack-scale, liquid-cooled" 措辞），功率只引用户指南与 OEM 资料。
- Delta 行（3Φ 208V 60A 80%→32.8 kW）按 √3·U·I·PF·d 公式不能复现（≈16.4 kW），指南未给该行推导，以表列值为准并标注差异（B13-C03）。
- AMD OEM 节点的机柜级供电散热预算无公开材料，保留 unknown。
- Redfish 液冷资源只有 schema 定义，无公开真实遥测实例；schema 不等于设备实现。
