---
id: training.index
title: 06 训练与后训练系统
type: index
domain: training
status: draft
platforms:
- generic
source_refs:
- src.ascend.torch-npu
- src.ascend.mind-cluster
- src.stas.ml-engineering
updated_at: '2026-10-18'
summary: 组织训练状态、并行、框架执行、预训练微调、数值行为、性能与故障恢复。
related_ids:
- software-stack.index
- communication.index
- data-storage.index
- cluster-platform.index
- inference.index
- reliability.index
- training.parallelism-and-state
- training.framework-execution
- training.pretraining-and-finetuning
- training.checkpoint-state-consistency
- training.gpu-npu-precision-difference-triage
- training.gpu-npu-precision-difference-source-case
- training.gpu-npu-precision-difference-experiment
- training.checkpoint-state-recovery-triage
- training.checkpoint-state-recovery-source-case
- training.checkpoint-state-recovery-experiment
- training.slow-rank-triage
- training.elastic-training-and-membership
---

# 06 训练与后训练系统

本页是内容导航草稿。下方已有基础正文，其余主题继续建设；新正文正在轮末审阅，未经本地环境实测。`generic` 表示跨平台导航，不表示所有环境兼容。

## 已有正文

- [并行策略与训练状态](parallelism-and-state.md)：DP/FSDP/TP/PP 基础上补齐专家并行（token dispatch/combine）、序列维 SP/CP、组合身份与冲突检查、固定假设选型表和单步边界（Batch 24 修订，gpt-6.1-sol/xhigh 审阅已闭环的 draft，未实测）。
- [训练框架组件、执行循环与平台职责对照](framework-execution.md)：训练驱动→autograd→分布式封装→optimizer→编译→算子后端→checkpoint 的职责图，PyTorch 2.6 / Megatron-Core core_v0.19.2 / MindSpeed-LLM v2.2.0 三组独立档案与各阶段故障分界（T06-02，Batch 24，gpt-6.1-sol/xhigh 审阅已闭环的 draft，未实测）。
- [预训练与微调工作流和状态契约](pretraining-and-finetuning.md)：预训练/继续预训练/全参 SFT/LoRA-PEFT 的目标、数据与状态契约、adapter 保存合并边界、观察口径与阶段切换验证（T06-03，Batch 24，gpt-6.1-sol/xhigh 审阅已闭环的 draft，未实测）。
- [Checkpoint 恢复一致性](checkpoint-state-consistency.md)。
- [弹性训练与成员变更](elastic-training-and-membership.md)：rendezvous、成员变更与失败语义；PyTorch elastic 与 MindSpeed-LLM 副本机制的对照边界。

## 本章范围

覆盖预训练、微调与强化学习等任务的执行过程和状态。把“作业运行”“持续进展”“结果正确”和“性能符合预期”分别作为需要证据的判断。

## 场景指南、案例与实验

来源案例保留各自平台与版本，实验均未执行。Checkpoint 案例来自 CPU 环境，不构成 GPU/NPU 恢复证明。

| 主题 | 诊断指南 | 来源案例 | 实验设计 |
|---|---|---|---|
| GPU→NPU 精度差异 | [指南](gpu-npu-precision-difference-triage.md) | [案例](gpu-npu-precision-difference-source-case.md) | [实验设计](gpu-npu-precision-difference-experiment.md) |
| Checkpoint 恢复状态 | [指南](checkpoint-state-recovery-triage.md) | [案例](checkpoint-state-recovery-source-case.md) | [实验设计](checkpoint-state-recovery-experiment.md) |
| 慢 rank | [指南](slow-rank-triage.md) | 待补充 | 待补充 |

## 二级主题地图

- **06.1 训练计算过程与状态：权重、梯度、优化器、数据进度** — 已有[状态责任基础草稿](parallelism-and-state.md)（Batch 24 补单步内所有权与合法跳步）。
- **06.2 数据、张量、流水线、专家等并行策略** — 已有[DP/FSDP/TP/PP/EP/CP 布局与组合映射](parallelism-and-state.md)（Batch 24 补专家并行、SP/CP 区别、冲突检查与选型表）。
- **06.3 训练框架与执行：框架通用机制及平台实现** — 已有[框架执行职责对照](framework-execution.md)（PyTorch 2.6/Megatron core_v0.19.2/MindSpeed-LLM v2.2.0 三组档案）；具体工作负载与执行验证待补。
- **06.4 预训练、微调、强化学习与 rollout** — 已有[预训练与微调工作流和状态契约](pretraining-and-finetuning.md)（T06-03，RL rollout 属后续批次）。
- **06.5 算子适配、混合精度、数值行为与收敛** — 已有[GPU→NPU 精度差异指南](gpu-npu-precision-difference-triage.md)、公开案例与实验设计；算子和训练质量专题待补。
- **06.6 性能分析、慢 rank、资源不均与吞吐退化** — 已有[慢 rank 诊断指南](slow-rank-triage.md)（PyTorch 2.8/NCCL RAS 证据样板，NPU 侧观测缺口标注）；资源不均与吞吐专题待补。
- **06.7 Checkpoint 状态、一致性、容错与弹性恢复** — 已有[恢复一致性与重分片边界](checkpoint-state-consistency.md)、[状态异常指南](checkpoint-state-recovery-triage.md)、公开案例与实验设计，以及[弹性训练与成员变更](elastic-training-and-membership.md)；尚未实测。
- **06.8 恢复后的正确性与持续进展验证** — 已有[验证分层与容差说明](checkpoint-state-consistency.md)，尚未执行实验。

## 内容边界

- 算子和 dtype/layout 的底层语义引用 02；本章解释模型、loss、梯度及优化器层面的行为。
- 通信机制引用 03，文件持久化引用 04；本章负责训练状态及恢复点的一致性。
- 强化学习中的 rollout 服务机制可引用 07；训练循环与状态推进仍归本章。

## NPU 内容位置

训练框架适配、MindSpeed 相关实践、精度变化、慢 rank 和容错恢复均在本章逐步展开。具体能力需关联芯片、软件栈、模型和并行配置。

完整路径见[昇腾专题](../../paths/platforms/ascend.md)。其他平台入口见 [NVIDIA 专题](../../paths/platforms/nvidia.md)。

## 关联章节

- [02 系统软件与加速器执行栈](../02-software-stack/index.md)
- [03 互联网络与分布式通信](../03-communication/index.md)
- [04 数据路径与存储系统](../04-data-storage/index.md)
- [05 集群平台与资源管理](../05-cluster-platform/index.md)
- [07 推理与服务系统](../07-inference/index.md)
- [08 可靠性与计算正确性方法](../08-reliability/index.md)

## 已收集的原始资料入口

以下链接指向厂商或项目自己的资料；引用或改编前仍需核对对应版本、来源许可和适用范围。

- [TorchNPU 官方仓库](https://github.com/Ascend/pytorch)：框架与设备后端适配资料入口。
- [MindCluster 官方仓库](https://github.com/Ascend/mind-cluster)：训练故障恢复与相关组件资料入口，需逐项核对适用条件。
- [ML Engineering 项目仓库](https://github.com/stas00/ml-engineering)：训练工程、性能与诊断资料入口。

## 首轮成果与后续

已有并行/状态（含 EP/CP 与组合映射）、框架执行职责对照、预训练与微调状态契约、恢复一致性，以及精度迁移、恢复异常、慢 rank、弹性训练的指南/案例/实验设计；后续补强化学习 rollout（后续批次）与实际环境验证。
