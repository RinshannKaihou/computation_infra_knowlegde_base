---
id: reliability.index
title: 08 可靠性与计算正确性方法
type: index
domain: reliability
status: draft
platforms: [generic]
source_refs: [src.ascend.mind-cluster, src.nvidia.nccl-docs, src.stas.ml-engineering]
updated_at: "2026-10-22"
summary: 建立跨领域的故障模型、证据推理、恢复与验证方法；含八主题五方面入口表与交付核对。
related_ids: [hardware.index, communication.index, data-storage.index, cluster-platform.index, training.index, inference.index, reliability.dimensions-and-failure-domains, reliability.evidence-and-hypotheses, reliability.silent-errors-and-integrity, reliability.fault-models-and-propagation, reliability.correlated-failure-source-case, reliability.mitigation-and-recovery-principles, reliability.test-design-and-coverage, reliability.reliability-metrics-and-recovery-loss, reliability.postmortem-and-knowledge-update, reliability.diagnostic-evaluation-method, reliability.diagnostic-evaluation-fixtures]
---

# 08 可靠性与计算正确性方法

本页是内容导航草稿，已有正文见下方。正文尚无本地环境实测；方法、公开证据与现场结果互不替代——本章交付的是方法与公开来源证据，真实环境结果由独立验证轨道管理。`generic` 表示跨平台导航，不表示所有环境兼容。

## 本章范围

覆盖可用性、正确性、性能稳定性和可恢复性的通用方法。为具体领域提供共同的证据结构、调查方法和验证标准。

## 已有正文

- [可靠性维度与故障域](dimensions-and-failure-domains.md)：可用性、正确性、性能与恢复目标。
- [诊断中的证据、假设与结论](evidence-and-hypotheses.md)：观察、支持/反驳证据与下一项检查。
- [静默错误与计算完整性判定](silent-errors-and-integrity.md)：SDC 与灰色退化的区别、日志盲区、Fleetscanner/Ripple 检测量化、真实节点上的训练传播与 ABFT 反例、检测方法分层与数值噪声扣除、NVIDIA/AMD/Ascend 平台证据清单。
- [统一测试选择、压力/注入与统计方法](test-design-and-coverage.md)：验收/基准/压力/注入四类测试的选择矩阵、统计纪律与预注册判据、注入六字段与压力声明、七份方案的准备矩阵（真实执行 0/7）。
- [可靠性统计、有效产出与恢复损失](reliability-metrics-and-recovery-loss.md)：统计框架与 MTBF/MTTR 边界、有效训练时间与 MPG 三层分解、六类量记账、事件表 schema 与合成计算例。
- [事故复盘、来源更新与知识维护](postmortem-and-knowledge-update.md)：复盘字段与假设三分、三类材料区分、更新→修订→审阅→导航追溯链、四类复核触发与弃用规则。
- [诊断评测方法规范](diagnostic-evaluation-method.md)：train/dev/held-out 与外置隔离、泄漏控制、答案证据强度四级、七维 rubric。
- [诊断评测公开题组](diagnostic-evaluation-fixtures.md)：九条固定输入/oracle/判据的公开教学与检索回归条目（含 U 级与合成条目），不构成独立 holdout。
- [故障模型、跨层传播与共享失效分析](fault-models-and-propagation.md)：fault→error→failure 三链、故障分类、训练与推理两张传播图、有限 FMEA 表与传播/同因区分方法。
- [相关故障与冗余失效来源案例](correlated-failure-source-case.md)：Meta 2021-10-04 断网复盘＋外部观测双证据，共同原因、传播、放大与冗余独立性失效边界。
- [隔离、重试预算、降级与恢复选择](mitigation-and-recovery-principles.md)：处置六字段、按目标维度选措施、重试预算与 jitter 退避、降级判据、恢复选择与有限故障对照设计。

## 八主题五方面入口表

每个主题的原理与边界、设计与使用、观测与判断、故障与处置、验证与案例分别指向正文入口；同一篇可承担多个方面，链接指向正文而非目录标题。各入口的适用边界、未实测状态与未知条件以所链正文为准。

| 主题 | 原理与边界 | 设计与使用 | 观测与判断 | 故障与处置 | 验证与案例 |
|---|---|---|---|---|---|
| **08.1 可用性、正确性、性能稳定性与可恢复性** | [四个维度分别回答什么](dimensions-and-failure-domains.md)与[一项指标至少写清八个部分](dimensions-and-failure-domains.md) | [动手前固定六项](mitigation-and-recovery-principles.md)与[按目标维度选措施](mitigation-and-recovery-principles.md) | [统计框架四要素：对象/窗口/分母/事件](reliability-metrics-and-recovery-loss.md) | [恢复需要一组退出门槛](dimensions-and-failure-domains.md)与[恢复选择：重算、回退还是切换](mitigation-and-recovery-principles.md) | [六类量记账](reliability-metrics-and-recovery-loss.md)与[选择矩阵与统计纪律](test-design-and-coverage.md) |
| **08.2 故障模型、故障域、传播与相关故障** | [fault/error/failure 三链与故障分类](fault-models-and-propagation.md)；[故障域是共享依赖和影响边界](dimensions-and-failure-domains.md) | [两张跨层传播图](fault-models-and-propagation.md)与[有限 FMEA 表](fault-models-and-propagation.md) | [事件与证据时间线](correlated-failure-source-case.md) | [区分传播与同因、检验隔离与冗余独立性](fault-models-and-propagation.md) | [Meta 2021-10-04 案例与可迁移检查问题](correlated-failure-source-case.md)（不可外推条件单列） |
| **08.3 可观测性、时间线与跨层证据关联** | [五种记录对象不能混用](evidence-and-hypotheses.md) | [先对齐对象，再排列时间](evidence-and-hypotheses.md)；[记账 schema 三张表](reliability-metrics-and-recovery-loss.md) | [跨层时间线与对象对齐方法](evidence-and-hypotheses.md)；采集质量边界随所查领域的领域正文 | [结论的最低完整度](evidence-and-hypotheses.md) | [事故记录：证据结构](postmortem-and-knowledge-update.md)与[合成计算例：同一症状四维结论不同](reliability-metrics-and-recovery-loss.md) |
| **08.4 故障发现、假设检验、归因与下一项检查** | [用支持、反驳和未知维护假设](evidence-and-hypotheses.md) | [下一项检查要比较收益、代价和影响](evidence-and-hypotheses.md) | [答案的证据强度分级](diagnostic-evaluation-method.md) | [两个原创合成短例](evidence-and-hypotheses.md)与[评审角色与污染控制](diagnostic-evaluation-method.md) | [公开题组九条](diagnostic-evaluation-fixtures.md)（教学与检索回归用，非独立 holdout） |
| **08.5 隔离、冗余、重试、降级与恢复原则** | [冗余独立性、共享依赖与故障预算](mitigation-and-recovery-principles.md) | [重试：预算、退避与幂等](mitigation-and-recovery-principles.md)与[隔离与降级](mitigation-and-recovery-principles.md) | [重试与恢复开销的记账位置](reliability-metrics-and-recovery-loss.md) | [恢复选择：重算、回退还是切换](mitigation-and-recovery-principles.md) | [有限故障对照设计](mitigation-and-recovery-principles.md)与[冗余与隔离为什么失效](correlated-failure-source-case.md) |
| **08.6 数值异常、静默错误与计算完整性** | [定义与要解决的问题](silent-errors-and-integrity.md)与[“静默”分三层](silent-errors-and-integrity.md) | [检测方法分层：覆盖、成本与假阴性/误报](silent-errors-and-integrity.md) | [判定之前先扣除数值噪声背景](silent-errors-and-integrity.md) | [训练中的传播：真实不健康节点上的三层级证据](silent-errors-and-integrity.md) | [Fleetscanner/Ripple 检测量化对比](silent-errors-and-integrity.md)与[平台证据清单：NVIDIA/AMD/Ascend 按版本记录](silent-errors-and-integrity.md) |
| **08.7 验收、基准、压力测试与故障注入** | [选择矩阵：先声明对象与所问问题](test-design-and-coverage.md) | [注入与压力的设计字段](test-design-and-coverage.md) | [统计纪律：比较之前先固定口径](test-design-and-coverage.md) | [适用边界：真实执行 0/7 与结果留白](test-design-and-coverage.md) | [七份验证方案的准备矩阵](test-design-and-coverage.md)（全部未执行） |
| **08.8 可靠性指标、恢复损失、事故复盘与知识更新** | [MTBF/MTTR/MTBI 的使用边界](reliability-metrics-and-recovery-loss.md) | [事故记录：证据结构](postmortem-and-knowledge-update.md)与[更新→修订→审阅→导航追溯链](postmortem-and-knowledge-update.md) | [推理侧：不能只统计成功请求](reliability-metrics-and-recovery-loss.md) | [复核触发：什么时候必须重查既有知识](postmortem-and-knowledge-update.md) | [弃用规则](postmortem-and-knowledge-update.md)与[诊断评测方法的角色边界](diagnostic-evaluation-method.md) |

## 五方面阅读检查清单

进入任一主题正文前，用以下检查项自检口径；各检查项的展开在所链正文。

- **时间**：先固定统计框架四要素（对象/窗口/分母/事件）；跨层时间线先对齐对象再排列时间，不同对象的时刻不能直接拼接。
- **实体/工作键**：五种记录对象（症状/事件/观察/假设/结论）不能混用；指标八个部分里写清统计对象与共同分母。
- **采集质量**：健康摘要、错误事件、累计计数器、采样失败与未覆盖项分开（设备侧边界见 [01 域健康证据](../01-hardware/health-evidence.md)）；**部署了采集系统不等于方法已覆盖**，覆盖以选择矩阵声明与检测结果为准。
- **覆盖**：测试与检测都先声明对象与所问问题；检测方法分层比较覆盖、成本与假阴性/误报。
- **假设反驳/未知**：假设按支持、反驳、未知三分维护；平台证据按版本记录，unknown 不因正文交付而消失。
- **下一项检查**：比较收益、代价和影响后选择；重试预算与恢复选择按目标维度决定。
- **终止门槛**：恢复验收是一组退出门槛（不只"服务起来了"）；复盘与测试均有停止条件与完成判据。

## 交付核对与保留边界（T08-09，2026-10-22）

对照原目录八主题逐项核对五方面入口，并区分「已交付的方法/样板」「未执行的验证结果」与「仍开放的 unknown」。核对只针对已交付正文的覆盖结构，不改变任何正文的编辑/验证状态。

- **08.1/08.3/08.4（原 covered 主题复核）**：三主题在原有四维目标与证据方法基础上，经 Batch 29/30 交付的处置选择、统计记账、测试方法与诊断评测形成完整链——08.1 补[处置六字段与按维度选措施](mitigation-and-recovery-principles.md)和[统计框架](reliability-metrics-and-recovery-loss.md)；08.3 补[事件表 schema](reliability-metrics-and-recovery-loss.md)与[复盘证据结构](postmortem-and-knowledge-update.md)；08.4 补[证据强度分级](diagnostic-evaluation-method.md)与[公开题组](diagnostic-evaluation-fixtures.md)。
- **08.2/08.5**：由 T08-01/T08-02/T08-03（Batch 29）交付的[故障模型与传播](fault-models-and-propagation.md)、[相关故障案例](correlated-failure-source-case.md)、[处置选择](mitigation-and-recovery-principles.md)承担五方面；各任务来源与最终复核记录：T08-01（[来源](../../docs/research/batch-29-t08-01-sources.md)·[复核](../../docs/research/batch-29-t08-01-codex-recheck-2.md)）、T08-02（[来源](../../docs/research/batch-29-t08-02-sources.md)·[复核](../../docs/research/batch-29-t08-02-codex-recheck.md)）、T08-03（[来源](../../docs/research/batch-29-t08-03-sources.md)·[复核](../../docs/research/batch-29-t08-03-codex-recheck-3.md)）。
- **08.6/08.7/08.8**：由 T08-04～T08-08（Batch 30）交付的四篇新增与一篇修订承担五方面（[T08-04 来源](../../docs/research/batch-30-t08-04-sources.md)、[T08-05 来源](../../docs/research/batch-30-t08-05-sources.md)、[T08-06 来源](../../docs/research/batch-30-t08-06-sources.md)、[T08-07 来源](../../docs/research/batch-30-t08-07-sources.md)、[T08-08 来源](../../docs/research/batch-30-t08-08-sources.md)；最终复核记录见 [Batch 30 审阅汇总](../../docs/research/batch-30-source-audit.md)）。
- **状态边界（入口可见）**：SDC 平台资料中 NPU 发生率保持 unknown、AMD/Ascend 平台证据按版本记录且不外推；七份验证方案真实执行 0/7，结果留白由独立验证轨道（V 工作包）管理；独立诊断评测集待 V12 外置获取，[公开题组](diagnostic-evaluation-fixtures.md)不构成独立 holdout。文档关闭不改变任何条目的 reproduced 状态：本章全部正文为 draft，模型审阅不等于硬件验证。
- **稳定 ID 与维护触发**：本页保留 `reliability.index` 稳定 ID；后续正文任务的必要修订归对应正文任务，导航核对不改动正文技术边界。知识维护的复核触发与弃用规则见[事故复盘与知识维护](postmortem-and-knowledge-update.md)。
- **审阅状态**：本表与核对小节为 T08-09 交付时初稿（2026-10-22），gpt-6.1-sol/xhigh 审阅待做。

## 二级主题地图

- **08.1 可用性、正确性、性能稳定性与可恢复性** — [基础正文草稿](dimensions-and-failure-domains.md)；[处置选择](mitigation-and-recovery-principles.md)按四维组织措施。
- **08.2 故障模型、故障域、传播与相关故障** — [故障模型与传播](fault-models-and-propagation.md)＋[相关故障案例](correlated-failure-source-case.md)；基础正文见[维度与故障域](dimensions-and-failure-domains.md)。
- **08.3 可观测性、时间线与跨层证据关联** — [基础正文草稿](evidence-and-hypotheses.md)；事件表 schema 见[可靠性统计](reliability-metrics-and-recovery-loss.md)。
- **08.4 故障发现、假设检验、归因与下一项检查** — [基础正文草稿](evidence-and-hypotheses.md)；[诊断评测方法](diagnostic-evaluation-method.md)补评测侧入口。
- **08.5 隔离、冗余、重试、降级与恢复原则** — [隔离、重试预算、降级与恢复选择](mitigation-and-recovery-principles.md)；相关案例见[冗余失效来源案例](correlated-failure-source-case.md)。
- **08.6 数值异常、静默错误与计算完整性的判定方法** — [静默错误与计算完整性判定](silent-errors-and-integrity.md)（Batch 30 补齐检测量化、训练传播与平台证据；NPU SDC 发生率保持 unknown）。
- **08.7 验收、基准、压力测试与故障注入方法** — [统一测试选择、压力/注入与统计方法](test-design-and-coverage.md)；真实环境结果证据仍由验证工作包推进（实测 0/7）。
- **08.8 可靠性指标、恢复损失、事故复盘与知识更新** — [可靠性统计、有效产出与恢复损失](reliability-metrics-and-recovery-loss.md)＋[事故复盘、来源更新与知识维护](postmortem-and-knowledge-update.md)＋[诊断评测方法](diagnostic-evaluation-method.md)/[公开题组](diagnostic-evaluation-fixtures.md)（独立评测集待 V12 外置获取）。

## 内容边界

- 本章解释如何提出假设、关联证据和验证结果；具体错误码、组件机制与处置流程归对应系统章节。
- 跨层事故按主要调查问题选择主归属，同时关联所有涉及领域，保留症状与最终结论的区别。
- 案例经验与验证结果均保留当时环境；不能将单次成功、命令退出成功或服务重启成功视为完整恢复证明。

## NPU 内容位置

GPU 与 NPU 共用证据、假设和验证的表达方式；平台错误码、设备工具和恢复机制分别解释。NPU 精度迁移和恢复后的状态验证是本章方法的首批应用场景。

完整路径见[昇腾专题](../../paths/platforms/ascend.md)。其他平台入口见 [NVIDIA 专题](../../paths/platforms/nvidia.md)与 [AMD 专题](../../paths/platforms/amd.md)。

## 关联章节

- [01 物理设施与计算节点](../01-hardware/index.md)
- [03 互联网络与分布式通信](../03-communication/index.md)
- [04 数据路径与存储系统](../04-data-storage/index.md)
- [05 集群平台与资源管理](../05-cluster-platform/index.md)
- [06 训练与后训练系统](../06-training/index.md)
- [07 推理与服务系统](../07-inference/index.md)

## 已收集的原始资料入口

以下链接指向厂商或项目自己的资料；引用或改编前仍需核对对应版本、来源许可和适用范围。

- [MindCluster 官方仓库](https://github.com/Ascend/mind-cluster)：故障诊断、故障表达和恢复组件的参考入口。
- [NVIDIA NCCL 用户指南](https://docs.nvidia.com/deeplearning/nccl/user-guide/docs/index.html)：通信领域的诊断资料，可用于练习区分观察、推断和验证。
- [ML Engineering 项目仓库](https://github.com/stas00/ml-engineering)：工程诊断和测试资料入口。

## 成果与后续

已有可靠性维度、故障域与证据推理方法，七组公开来源案例已按环境、时间线和结果边界整理；Batch 29 新增故障模型/传播、相关故障案例与处置选择三篇；Batch 30 补齐 SDC 检测/传播/平台证据、统一测试方法、可靠性统计、事故复盘与诊断评测方法及公开题组；八主题五方面入口表、阅读检查清单与交付核对已随 T08-09 交付（2026-10-22，审阅待做）。后续维护方向：具体领域案例继续按复盘触发补入、全部真实环境验证（V 工作包）与独立评测集外置获取（V12）。
