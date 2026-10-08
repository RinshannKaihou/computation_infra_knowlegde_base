---
id: reliability.index
title: 08 可靠性与计算正确性方法
type: index
domain: reliability
status: draft
platforms: [generic]
source_refs: [src.ascend.mind-cluster, src.nvidia.nccl-docs, src.stas.ml-engineering]
updated_at: "2026-09-30"
summary: 建立跨领域的故障模型、证据推理、恢复与验证方法。
related_ids: [hardware.index, communication.index, data-storage.index, cluster-platform.index, training.index, inference.index, reliability.dimensions-and-failure-domains, reliability.evidence-and-hypotheses, reliability.silent-errors-and-integrity]
---

# 08 可靠性与计算正确性方法

本页是内容导航草稿，已有正文见下方；其余二级主题继续建设。正文尚无本地环境实测。`generic` 表示跨平台导航，不表示所有环境兼容。

## 本章范围

覆盖可用性、正确性、性能稳定性和可恢复性的通用方法。为具体领域提供共同的证据结构、调查方法和验证标准。

## 已有正文

- [可靠性维度与故障域](dimensions-and-failure-domains.md)：可用性、正确性、性能与恢复目标。
- [诊断中的证据、假设与结论](evidence-and-hypotheses.md)：观察、支持/反驳证据与下一项检查。
- [静默错误与计算完整性判定](silent-errors-and-integrity.md)：SDC 与灰色退化的区别、日志盲区、检测方法与数值噪声扣除。

## 二级主题地图

- **08.1 可用性、正确性、性能稳定性与可恢复性** — [基础正文草稿](dimensions-and-failure-domains.md)；具体工具与案例继续补充。
- **08.2 故障模型、故障域、传播与相关故障** — [基础正文草稿](dimensions-and-failure-domains.md)；具体工具与案例继续补充。
- **08.3 可观测性、时间线与跨层证据关联** — [基础正文草稿](evidence-and-hypotheses.md)；具体工具与案例继续补充。
- **08.4 故障发现、假设检验、归因与下一项检查** — [基础正文草稿](evidence-and-hypotheses.md)；具体工具与案例继续补充。
- **08.5 隔离、冗余、重试、降级与恢复原则** — 待建设。
- **08.6 数值异常、静默错误与计算完整性的判定方法** — 已有[静默错误与计算完整性判定](silent-errors-and-integrity.md)；NPU 侧一手证据待补。
- **08.7 验收、基准、压力测试与故障注入方法** — 待建设。
- **08.8 可靠性指标、恢复损失、事故复盘与知识更新** — 待建设。

## 内容边界

- 本章解释如何提出假设、关联证据和验证结果；具体错误码、组件机制与处置流程归对应系统章节。
- 跨层事故按主要调查问题选择主归属，同时关联所有涉及领域，保留症状与最终结论的区别。
- 案例经验与验证结果均保留当时环境；不能将单次成功、命令退出成功或服务重启成功视为完整恢复证明。

## NPU 内容位置

GPU 与 NPU 共用证据、假设和验证的表达方式；平台错误码、设备工具和恢复机制分别解释。NPU 精度迁移和恢复后的状态验证是本章方法的首批应用场景。

完整路径见[昇腾专题](../../paths/platforms/ascend.md)。其他平台入口见 [NVIDIA 专题](../../paths/platforms/nvidia.md)。

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

## 首轮成果与后续

已有可靠性维度、故障域与证据推理方法，七组公开来源案例已按环境、时间线和结果边界整理；后续用独立案例与真实验证检验方法，完整入库复盘不作为未见评测。
