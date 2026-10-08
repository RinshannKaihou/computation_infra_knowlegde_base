---
id: communication.index
title: 03 互联网络与分布式通信
type: index
domain: communication
status: draft
platforms:
- generic
source_refs:
- src.nvidia.nccl-docs
- src.nvidia.nccl-tests
- src.ascend.agent-skills
updated_at: '2026-09-30'
summary: 从网络和拓扑到集合通信，组织通信正确性、性能和故障证据。
related_ids:
- hardware.index
- software-stack.index
- training.index
- inference.index
- reliability.index
- communication.collectives-and-rank-progress
- communication.bandwidth-baselines
- communication.hccl-timeout-triage
- communication.hccl-timeout-source-case
- communication.hccl-timeout-experiment
- communication.nccl-timeout-triage
- communication.nccl-timeout-source-case
- communication.nccl-timeout-experiment
- communication.bandwidth-degradation-triage
---

# 03 互联网络与分布式通信

本页是内容导航草稿，已有正文见下方；其余二级主题继续建设。正文尚无本地环境实测。`generic` 表示跨平台导航，不表示所有环境兼容。

## 本章范围

覆盖节点内与跨节点互联、网络协议、集合通信、初始化与 rank 关系。将通信症状、运行状态、网络和设备证据关联起来。

## 已有正文

- [集合通信与 rank 进度](collectives-and-rank-progress.md)：参与者、次序、参数契约与主机/设备进度。
- [通信带宽与性能基线口径](bandwidth-baselines.md)：带宽、消息大小、计时和平台工具边界。
- [通信带宽退化诊断指南](bandwidth-degradation-triage.md)：把“带宽变低”拆成测量口径、配置/映射与真实链路退化三类，GPU/NPU 证据分开。

## 场景指南、案例与实验

以下均为来源整理草稿；公开案例不代表本库复现，实验仅为设计。

| 主题 | 诊断指南 | 来源案例 | 实验设计 |
|---|---|---|---|
| HCCL 超时 | [指南](hccl-timeout-triage.md) | [案例](hccl-timeout-source-case.md) | [实验设计](hccl-timeout-experiment.md) |
| NCCL 超时 | [指南](nccl-timeout-triage.md) | [案例](nccl-timeout-source-case.md) | [实验设计](nccl-timeout-experiment.md) |


## 二级主题地图

- **03.1 节点内、节点间与超节点互联** — 待建设。
- **03.2 Ethernet、InfiniBand、RoCE 与 RDMA** — 待建设。
- **03.3 拓扑、路由、拥塞与性能基线** — [基础正文草稿](bandwidth-baselines.md)；完整平台分支和具体流程待补。
- **03.4 集合通信原理与通信模式** — [基础正文草稿](collectives-and-rank-progress.md)；完整平台分支和具体流程待补。
- **03.5 NCCL、RCCL、HCCL 等通信库** — [基础正文草稿](collectives-and-rank-progress.md)；完整平台分支和具体流程待补。
- **03.6 通信初始化、rank 映射与执行次序** — [基础正文草稿](collectives-and-rank-progress.md)；完整平台分支和具体流程待补。
- **03.7 超时、链路退化、通信热点与验证** — 已有 HCCL/NCCL 超时指南、公开案例和实验设计；已有[带宽退化诊断](bandwidth-degradation-triage.md)（口径/配置/链路三分支）；拥塞与热点专题待补。

## 内容边界

- 硬件资源和节点组成引用 01；本章解释链路与通信行为。
- 慢 rank 的训练计算原因归 06，推理中的通信依赖归 07；本章保留通信证据和机制。
- 通用假设检验方法归 08；具体 HCCL/NCCL 问题的机制、条件和分支归本章。

## NPU 内容位置

HCCL 独立记录其环境、拓扑、设备与 rank 关系以及诊断证据。与 NCCL 可共用调查问题，但参数、工具、错误语义和可用诊断能力需分别维护。

完整路径见[昇腾专题](../../paths/platforms/ascend.md)。其他平台入口见 [NVIDIA 专题](../../paths/platforms/nvidia.md)。

## 关联章节

- [01 物理设施与计算节点](../01-hardware/index.md)
- [02 系统软件与加速器执行栈](../02-software-stack/index.md)
- [06 训练与后训练系统](../06-training/index.md)
- [07 推理与服务系统](../07-inference/index.md)
- [08 可靠性与计算正确性方法](../08-reliability/index.md)

## 已收集的原始资料入口

以下链接指向厂商或项目自己的资料；引用或改编前仍需核对对应版本、来源许可和适用范围。

- [NVIDIA NCCL 用户指南](https://docs.nvidia.com/deeplearning/nccl/user-guide/docs/index.html)：通信配置和故障定位的官方资料入口。
- [NVIDIA nccl-tests](https://github.com/NVIDIA/nccl-tests)：通信验证项目入口；测试方法及结果需匹配环境。
- [Ascend Agent Skills](https://github.com/Ascend/agent-skills)：HCCL 测试等任务的资料入口。

## 首轮成果与后续

已有 collective/rank 与带宽参考，以及 HCCL/NCCL 超时指南、案例和实验设计；后续补拓扑退化、拥塞与匹配环境的通信验证。
