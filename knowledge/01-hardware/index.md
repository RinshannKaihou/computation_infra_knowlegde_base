---
id: hardware.index
title: 01 物理设施与计算节点
type: index
domain: hardware
status: draft
platforms: [generic]
source_refs: [src.infrasys.aiinfra, src.ascend.agent-skills]
updated_at: "2026-10-09"
summary: 理解供电散热、主机与加速器组成，建立节点和硬件故障域的知识入口。
related_ids: [hardware.resource-topology, software-stack.index, communication.index, cluster-platform.index, reliability.index, hardware.health-evidence, hardware.power-thermal-evidence, hardware.node-acceptance-triage, hardware.rack-power-cooling-and-failure-domains, hardware.numa-memory-and-io-locality, hardware.accelerator-execution-and-data-movement, hardware.bmc-firmware-and-events, hardware.node-selection-and-lifecycle]
---

# 01 物理设施与计算节点

本页是内容导航草稿。已建设的正文见下方入口，其余二级主题仍待补充；正文均为草稿，未经本地环境实测。`generic` 表示跨平台导航，不表示所有环境兼容。

## 已有正文

[计算节点资源与拓扑参考](resource-topology.md)：区分主机与设备内存、计算设备与互联路径，并用具体 GPU/NPU 机型资料说明记录资源和拓扑时需要保留的条件。

[设备健康证据与检测边界](health-evidence.md)：区分状态、事件、计数器、采集失败与未覆盖项，分别保留 GPU/NPU 的条件。

[供电、散热与性能退化证据](power-thermal-evidence.md)：供电/散热异常经降频、降速与冗余降额表现为性能退化；汇总 GPU 降频位图、violation 计数、健康与诊断边界、机型规格与训练 NPU（HDK 26.1.x）字段及事件级降频机制。

[机柜供电、散热预算与共享依赖](rack-power-cooling-and-failure-domains.md)：持续/瞬态/冗余/余量四种口径的机柜级功率预算、风冷与液冷观察点、设施到设备的影响链与对照方法。

[NUMA、主机内存与 I/O 局部性的成对验证](numa-memory-and-io-locality.md)：first-touch 页分配、进程/线程亲和与设备 NUMA 归属的证据链，局部/远端成对测量方法。

[加速器执行单元、内存层次与数据移动机制](accelerator-execution-and-data-movement.md)：NVIDIA H100、AMD MI200、Ascend Atlas A2 三平台执行组织、内存层次与数据移动路径，统一观察点但不做一一映射。

[新节点与返修节点验收](node-acceptance-triage.md)：规格核对、被动证据、主动诊断、基准验收四层流程；DCGM 级别/测试与昇腾 ascend-dmi 分别固定版本，一次通过不声明硬件完全无故障。

[BMC、固件身份与跨层硬件事件](bmc-firmware-and-events.md)：以 Redfish 为通用角色模型，分列 NVIDIA DGX、华为 iBMC 与 Supermicro（AMD/OEM）三个带外管理实例的固件清单、更新边界与事件记录方法。

[节点选型、隔离返修、长期管理与退役](node-selection-and-lifecycle.md)：容量/成本比较方法（峰值规格与有效能力分开）、九状态生命周期流程、长期健康比较纪律与退役数据/凭据处置。

## 本章范围

覆盖从机柜到计算节点的物理组成、资源约束、硬件健康与生命周期。描述设备是什么、连接在哪里、受哪些物理条件约束。

## 二级主题地图

- **01.1 机柜、供电、散热与故障域** — 已有[机柜供电、散热预算与共享依赖](rack-power-cooling-and-failure-domains.md)与[供电散热与性能退化证据](power-thermal-evidence.md)；BMC/带外事件见[BMC、固件身份与跨层硬件事件](bmc-firmware-and-events.md)。
- **01.2 CPU、NUMA、主机内存与 I/O** — 已有[NUMA、主机内存与 I/O 局部性的成对验证](numa-memory-and-io-locality.md)与[资源与拓扑参考](resource-topology.md)。
- **01.3 GPU/NPU 的执行单元、设备内存与数据移动** — 已有[加速器执行单元、内存层次与数据移动机制](accelerator-execution-and-data-movement.md)；NPU 主机传输/同步语义细节待补充。
- **01.4 板卡、服务器、节点与超节点组成** — 已有[资源与拓扑参考](resource-topology.md)的四层次组成与 NVIDIA GB200 NVL72、Atlas 900 A3 SuperPoD、AMD OEM 节点样板。
- **01.5 BMC、固件、硬件健康与错误信息** — 已有[健康证据参考](health-evidence.md)（含三平台错误码映射）与[BMC、固件身份与跨层硬件事件](bmc-firmware-and-events.md)。
- **01.6 节点选型、验收与设备生命周期** — 已有[新节点与返修节点验收](node-acceptance-triage.md)与[节点选型、隔离返修、长期管理与退役](node-selection-and-lifecycle.md)；真实验收环境档案仍属独立验证轨道。

## 内容边界

- 节点组成、设备资源与硬件健康归本章；链路协议、通信拓扑与数据移动性能归 03。
- 固件属于设备生命周期；驱动初始化、运行时和框架配套归 02。
- 设备健康如何上报给调度系统归 05；通用故障域和验收方法归 08。

## NPU 内容位置

保留 NPU 执行单元、设备内存、服务器形态与硬件健康的独立解释。机型资料示例用于说明记录方式，实际环境仍需另行确认型号、配置和拓扑。

完整路径见[昇腾专题](../../paths/platforms/ascend.md)。其他平台入口见 [NVIDIA 专题](../../paths/platforms/nvidia.md)。

## 关联章节

- [02 系统软件与加速器执行栈](../02-software-stack/index.md)
- [03 互联网络与分布式通信](../03-communication/index.md)
- [05 集群平台与资源管理](../05-cluster-platform/index.md)
- [08 可靠性与计算正确性方法](../08-reliability/index.md)

## 已收集的原始资料入口

以下链接指向厂商或项目自己的资料；引用或改编前仍需核对对应版本、来源许可和适用范围。

- [AIInfra 项目仓库](https://github.com/Infrasys-AI/AIInfra)：计算节点和集群基础设施资料入口。
- [Ascend Agent Skills](https://github.com/Ascend/agent-skills)：昇腾设备查询等任务的资料组织参考；具体技能需核对操作影响。

## 首轮成果与后续

已有节点资源/拓扑（含板卡到超节点四层次与三平台样板）、健康证据（含三平台错误码映射）、供电散热参考、机柜预算、NUMA 局部性方法、加速器执行与数据移动概念、BMC/固件/事件参考、节点验收流程与选型/生命周期流程；后续补充验收环境档案规范与其余领域内容，并开展匹配环境验证。
