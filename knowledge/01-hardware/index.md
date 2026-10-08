---
id: hardware.index
title: 01 物理设施与计算节点
type: index
domain: hardware
status: draft
platforms: [generic]
source_refs: [src.infrasys.aiinfra, src.ascend.agent-skills]
updated_at: "2026-10-08"
summary: 理解供电散热、主机与加速器组成，建立节点和硬件故障域的知识入口。
related_ids: [hardware.resource-topology, software-stack.index, communication.index, cluster-platform.index, reliability.index, hardware.health-evidence, hardware.power-thermal-evidence, hardware.node-acceptance-triage]
---

# 01 物理设施与计算节点

本页是内容导航草稿。已建设的正文见下方入口，其余二级主题仍待补充；正文均为草稿，未经本地环境实测。`generic` 表示跨平台导航，不表示所有环境兼容。

## 已有正文

[计算节点资源与拓扑参考](resource-topology.md)：区分主机与设备内存、计算设备与互联路径，并用具体 GPU/NPU 机型资料说明记录资源和拓扑时需要保留的条件。

[设备健康证据与检测边界](health-evidence.md)：区分状态、事件、计数器、采集失败与未覆盖项，分别保留 GPU/NPU 的条件。

[供电、散热与性能退化证据](power-thermal-evidence.md)：供电/散热异常经降频、降速与冗余降额表现为性能退化；汇总 GPU 降频位图、violation 计数、健康与诊断边界、机型规格与 NPU 侧观测缺口。

[新节点与返修节点验收](node-acceptance-triage.md)：规格核对、被动证据、主动诊断、基准验收四层流程；DCGM 级别/测试与昇腾 ascend-dmi 分别固定版本，一次通过不声明硬件完全无故障。

## 本章范围

覆盖从机柜到计算节点的物理组成、资源约束、硬件健康与生命周期。描述设备是什么、连接在哪里、受哪些物理条件约束。

## 二级主题地图

- **01.1 机柜、供电、散热与故障域** — 已有[供电散热与性能退化证据](power-thermal-evidence.md)；机柜级供电拓扑与故障域细节待补充。
- **01.2 CPU、NUMA、主机内存与 I/O** — 已有[资源与拓扑参考](resource-topology.md)，具体调优与验证待补充。
- **01.3 GPU/NPU 的执行单元、设备内存与数据移动** — 已有[内存与互联边界](resource-topology.md)，芯片执行细节待补充。
- **01.4 板卡、服务器、节点与超节点组成** — 已有[机型资料示例](resource-topology.md)，更多形态待补充。
- **01.5 BMC、固件、硬件健康与错误信息** — 已有[健康证据参考](health-evidence.md)；BMC、固件与现场验收仍待补充。
- **01.6 节点选型、验收与设备生命周期** — 已有[新节点与返修节点验收](node-acceptance-triage.md)（DCGM/ascend-dmi/SuperBench 固定样板）；选型评估与生命周期其余环节待建设。

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

已有节点资源/拓扑、健康证据、供电散热参考与节点验收流程；后续按具体机型补充资产档案与生命周期细节，并开展匹配环境验证。
