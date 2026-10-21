---
id: path.task.selection-and-capacity
title: 选型与容量任务路径
type: path
domain: overview
status: draft
platforms:
- generic
source_refs: []
updated_at: '2026-10-22'
summary: 准备阶段的选型与容量阅读路径：前置材料、阅读顺序、目标产出、下一步判断与完成/停止条件。
related_ids:
- overview.design-targets-and-tradeoffs
- overview.reference-architectures
- hardware.node-selection-and-lifecycle
- hardware.rack-power-cooling-and-failure-domains
- hardware.resource-topology
- communication.interconnect-paths
- data-storage.local-and-shared-storage
- data-storage.object-and-parallel-storage
- training.parallelism-and-state
- inference.distributed-inference-layouts
- inference.capacity-and-autoscaling
- path.task.node-acceptance
- path.task.environment-installation
---

# 选型与容量任务路径

本页把"为新集群/新负载做选型与容量规划"所需的阅读串成一条路径。它是导航草稿：只链接已交付正文，不给出任何选型结论、采购建议或容量数字；正文中的超节点样板、机型规格与成本示例均为固定来源下的文档样板，未经实测，不构成可直接部署的环境。`generic` 表示导航意图，不表示任何平台兼容。

## 前置材料（先于阅读）

1. 工作负载画像：训练还是推理（或两者）、模型规模与并行意图、请求分布与 SLO 目标。
2. 五类目标（可靠性、性能、容量、成本、能耗）的初步主次与现有口径；尚无口径时先读第 1 步再回来补。
3. 硬约束：预算、机房供电/散热上限、机房空间、运维与验证能力。
4. 候选清单：候选机型/系统与各自的官方资料入口；资料取不到的候选先标记，不进入比较。

## 阅读顺序（先后有序）

1. [设计目标与约束的权衡](../../knowledge/00-overview/design-targets-and-tradeoffs.md)：五类目标的统一口径、有效产出定义、能耗测量边界与三窗口验收表模板——后续所有比较都引用这里的口径。
2. [单机、集群与超节点的参考架构及选择](../../knowledge/00-overview/reference-architectures.md)：三类组织的控制/数据/管理路径、共享故障域与规模边界；两个有官方组成依据的超节点样板与集群样板的约束比较。
3. [节点选型、隔离返修、长期管理与退役](../../knowledge/01-hardware/node-selection-and-lifecycle.md)：选型四步法（需求转译→有效能力测量→成本预算→有效成本核对）与生命周期状态机。
4. [机柜供电、散热预算与共享依赖](../../knowledge/01-hardware/rack-power-cooling-and-failure-domains.md)与[计算节点资源与拓扑参考](../../knowledge/01-hardware/resource-topology.md)：机柜级容量预算、共同故障域与节点资源的统一记录字段。
5. [节点内、节点间与超节点互联路径参考](../../knowledge/03-communication/interconnect-paths.md)：互联样板、端口—设备—交换结构核对表与文档带宽口径和作业可用带宽的区分。
6. [本地与共享文件存储版本化参考](../../knowledge/04-data-storage/local-and-shared-storage.md)与[对象与并行存储版本化参考](../../knowledge/04-data-storage/object-and-parallel-storage.md)：存储接口、一致性与选型条件的双样板。
7. 负载决定的资源形态：训练侧[并行策略与训练状态](../../knowledge/06-training/parallelism-and-state.md)，推理侧[分布式推理布局与并行选择](../../knowledge/07-inference/distributed-inference-layouts.md)与[容量、扩缩容与冷启动决策](../../knowledge/07-inference/capacity-and-autoscaling.md)。

## 目标产出

- 一张选型对照表草稿：候选 × 五类目标，每格写结论依据与证据类型（官方组成依据 / 文档样板 / 未实测假设 / 缺证 unknown）。
- 一张容量预算表：机柜供电散热、互联、存储三条线各自的预算口径与共享故障域标注。
- 每个候选的"下一步验证清单"：哪些结论可以在节点验收与环境安装阶段落地核对。

## 下一步判断

- 候选确定、设备到货在即：进入[节点验收任务路径](node-acceptance.md)。
- 环境搭建开始前：进入[环境安装任务路径](environment-installation.md)。
- 选型结论仍缺关键证据（如某候选无官方组成依据）：保持缺口登记，不用推测填充；是否接受该候选是用户决策，不是本库结论。

## 完成/停止条件

- **完成**：能对每个候选写出五类目标的主次排序、量化的假设计算示例（标明为假设）与证据类型；能指出任一结论哪些来自文档样板、哪些从未验证。
- **停止并升级**：候选的官方组成依据或关键规格资料取不到；供电/散热数据缺失无法构造机柜预算；成本数据不可得。以上任一成立时，在选型对照表中登记 blocked 项并交由决策者处置，本路径不代替决策。

## 逐链检查（T00-06 交付记录，2026-10-22）

本页全部内链经 `make check` 通过，引用的目标正文均为已交付条目（早期批次与 Batch 13–31 交付，多篇经审阅修订）；未引用未交付正文。本路径不新增外部来源（`source_refs` 为空，延伸阅读见所链正文的来源记录）。
