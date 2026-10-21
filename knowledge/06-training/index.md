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
updated_at: '2026-10-21'
summary: 组织训练状态、并行、框架执行、预训练微调、RL rollout、数值行为、性能与故障恢复；含八主题五方面入口表与交付核对。
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
- training.rl-rollout-consistency
- training.mixed-precision-and-convergence
- training.performance-analysis
- training.performance-regression-source-case
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
- [RL rollout、权重同步与训练推理协同](rl-rollout-consistency.md)：在线 RL（PPO/GRPO，verl v0.9.1 样板）的采样—打分—更新—发布循环、权重同步与陈旧策略边界、同步/异步代价、一致性与吞吐观察及单变量验证；DPO 作离线对照（T06-04，Batch 25，gpt-6.1-sol/xhigh 审阅已闭环的 draft，未实测）。
- [混合精度、算子适配与收敛验证](mixed-precision-and-convergence.md)：autocast/动态 loss scale/master 权重机制与三套实现分立边界、平台内重复性到单因素精度对照的流程、NaN/Inf 与 loss scale 分项观察、有限窗口收敛与质量判据及静默 dtype 案例（T06-05，Batch 25，gpt-6.1-sol/xhigh 审阅已闭环的 draft，未实测）。
- [训练性能分解、profiling 与优化验证](performance-analysis.md)：有效产出与配置口径、应用级/系统级工具对照（含取证边界）、PP bubble/EP 热点/长度偏斜/通信等待分支、受害与最早瓶颈区分、单因素优化与吞吐质量双判据（T06-06，Batch 25，gpt-6.1-sol/xhigh 审阅已闭环的 draft，未实测）。
- [Checkpoint 恢复一致性](checkpoint-state-consistency.md)：状态覆盖与截取一致性、API 完成观察点、Megatron core_v0.12.1 保存/装载职责、重分片各线支持/不支持/未知表、MindIO TTP 临终约束与恢复后验证分层（T06-08，Batch 26，draft，未实测）。
- [弹性训练与成员变更](elastic-training-and-membership.md)：rendezvous、成员变更与失败语义；PyTorch elastic 与 MindSpeed-LLM 副本机制的对照边界，及 MindIO TTP 外部组件约束（T06-08，Batch 26，draft，未实测）。

## 本章范围

覆盖预训练、微调与强化学习等任务的执行过程和状态。把“作业运行”“持续进展”“结果正确”和“性能符合预期”分别作为需要证据的判断。

## 八主题五方面入口表

每个主题的原理与边界、设计与使用、观测与判断、故障与处置、验证与案例分别指向正文入口；同一篇可承担多个方面，链接指向正文而非目录标题。各入口的适用边界、未实测状态与未知条件以所链正文为准。

| 主题 | 原理与边界 | 设计与使用 | 观测与判断 | 故障与处置 | 验证与案例 |
|---|---|---|---|---|---|
| **06.1 训练计算过程与状态** | [执行循环职责图](framework-execution.md)：训练驱动→autograd→optimizer→提交的各环节责任；[状态责任矩阵](parallelism-and-state.md)：参数/梯度/optimizer/进度的持有者 | [单步边界与合法跳步](parallelism-and-state.md)：micro-step、梯度累积与 optimizer step 的状态提交点；[预训练与微调状态契约](pretraining-and-finetuning.md)：各工作流应保存与恢复什么 | [状态身份与共同键](parallelism-and-state.md)：global step、样本/token 数、RNG 与并行身份；[框架层源码—职责定位表](framework-execution.md) | [各阶段故障分界](framework-execution.md)：按首失败环节区分训练驱动/框架/后端责任 | [验证判据与示例](parallelism-and-state.md)；[恢复状态实验设计](checkpoint-state-recovery-experiment.md)（未执行） |
| **06.2 数据/张量/流水线/专家并行** | [并行改变了什么](parallelism-and-state.md)与[专家并行 token dispatch/combine](parallelism-and-state.md)、[SP/CP 与 TP 的区别](parallelism-and-state.md) | [组合并行身份与冲突检查](parallelism-and-state.md)、[固定假设选型比较](parallelism-and-state.md)；[组合并行的性能验证入口](performance-analysis.md) | [性能分解与取证边界](performance-analysis.md)：分 rank/阶段 profiling 与最早瓶颈区分 | [慢 rank 诊断](slow-rank-triage.md)；[PP bubble/EP 热点/长度偏斜分支](performance-analysis.md) | [性能分析完成判据](performance-analysis.md)（吞吐与质量双判据）；[训练吞吐回归来源案例](performance-regression-source-case.md) |
| **06.3 训练框架与执行** | [执行循环职责图与 eager/compiled 路径](framework-execution.md) | [三组版本化档案](framework-execution.md)：PyTorch 2.6 / Megatron-Core core_v0.19.2 / MindSpeed-LLM v2.2.0 的职责与接口 | [源码—职责定位表（实现＋测试/断言）](framework-execution.md) | [各阶段故障分界与小规模验证方法](framework-execution.md) | 小规模验证方法见[故障分界节](framework-execution.md)；具体工作负载执行验证仍缺（见交付核对） |
| **06.4 预训练、微调、RL 与 rollout** | [预训练/微调机制与状态契约](pretraining-and-finetuning.md)；[RL 采样—打分—更新—发布循环](rl-rollout-consistency.md) | [阶段切换与 adapter 保存合并边界](pretraining-and-finetuning.md)；[同步/异步 rollout 代价与权重版本设计](rl-rollout-consistency.md) | [预训练/微调观察口径](pretraining-and-finetuning.md)；[rollout 一致性与吞吐观察](rl-rollout-consistency.md) | [异常区分检查与阶段转换验证](pretraining-and-finetuning.md)；[rollout 异常区分检查](rl-rollout-consistency.md)（陈旧策略/数据/状态三类） | [rollout 单变量验证设计](rl-rollout-consistency.md)（verl v0.9.1 样板）；DPO 离线对照；未实测 |
| **06.5 算子适配、混合精度与收敛** | [autocast/loss scale/master 权重机制速览](mixed-precision-and-convergence.md)与三套实现分立边界 | [平台内重复性到单因素精度对照流程](mixed-precision-and-convergence.md) | [NaN/Inf 与 loss scale 分项证据](mixed-precision-and-convergence.md) | [混合精度步骤与判断分支](mixed-precision-and-convergence.md)；[GPU→NPU 精度差异诊断](gpu-npu-precision-difference-triage.md) | [有限窗口收敛与质量判据](mixed-precision-and-convergence.md)（含静默 dtype 案例 #200537）；[精度差异来源案例](gpu-npu-precision-difference-source-case.md)；[实验设计](gpu-npu-precision-difference-experiment.md)（未执行） |
| **06.6 性能分析、慢 rank 与吞吐退化** | [有效产出与配置口径](performance-analysis.md)：先固定统计分母再谈吞吐 | [应用级/系统级工具选择与取证边界](performance-analysis.md) | [分 rank/阶段证据与受害/最早瓶颈区分](performance-analysis.md) | [慢 rank 诊断指南](slow-rank-triage.md)；[通信等待与带宽退化分支](../03-communication/bandwidth-degradation-triage.md) | [单因素优化与吞吐质量双判据](performance-analysis.md)；[Inductor 布局回归案例](performance-regression-source-case.md)（pytorch #189239 全链） |
| **06.7 Checkpoint 状态、一致性与弹性** | [状态覆盖与截取一致性](checkpoint-state-consistency.md)；[弹性成员变更语义](elastic-training-and-membership.md)（rendezvous/失败语义） | [DCP/Megatron/MindIO 保存装载职责与重分片支持表](checkpoint-state-consistency.md)；[PyTorch elastic 与 MindSpeed 副本机制对照](elastic-training-and-membership.md) | [API 完成是一组不同的观察点](checkpoint-state-consistency.md)（写入/提交/持久化分层） | [恢复状态异常诊断指南](checkpoint-state-recovery-triage.md)（strict 分支/world size 变化） | [恢复后验证分层](checkpoint-state-consistency.md)；[恢复异常来源案例](checkpoint-state-recovery-source-case.md)与[实验设计](checkpoint-state-recovery-experiment.md)（CPU 来源，未执行） |
| **06.8 恢复后正确性与持续进展** | [先定义希望恢复到什么](checkpoint-state-consistency.md)：恢复身份、逻辑进度与离散/浮点状态 | [恢复验证分层设计](checkpoint-state-consistency.md)：结构→逐字段→同输入单步→持续窗口 | [精确字段与浮点容差](checkpoint-state-consistency.md)；[恢复诊断需要的证据](checkpoint-state-recovery-triage.md) | [恢复异常步骤与判断分支](checkpoint-state-recovery-triage.md) | [恢复后验证方法](checkpoint-state-consistency.md)；[CPU DCP 端到端实验设计](checkpoint-state-recovery-experiment.md)（未执行，GPU/NPU 条件另核） |

## 场景指南、案例与实验

来源案例保留各自平台与版本，实验均未执行。Checkpoint 案例来自 CPU 环境，不构成 GPU/NPU 恢复证明。

| 主题 | 诊断指南 | 来源案例 | 实验设计 |
|---|---|---|---|
| GPU→NPU 精度差异 | [指南](gpu-npu-precision-difference-triage.md) | [案例](gpu-npu-precision-difference-source-case.md) | [实验设计](gpu-npu-precision-difference-experiment.md) |
| Checkpoint 恢复状态 | [指南](checkpoint-state-recovery-triage.md) | [案例](checkpoint-state-recovery-source-case.md) | [实验设计](checkpoint-state-recovery-experiment.md) |
| 慢 rank | [指南](slow-rank-triage.md) | 待补充 | 待补充 |
| 混合精度与收敛 | [指南](mixed-precision-and-convergence.md) | 见指南内 #200537 案例锚 | 沿用精度差异实验设计 |
| 训练吞吐回归 | 见[性能分解](performance-analysis.md) | [案例](performance-regression-source-case.md) | 见性能分解流程验证节 |

## 交付核对与保留边界（T06-09，2026-10-21）

对照原目录八主题逐项核对五方面入口，并区分「已交付的方法/样板」「未执行的验证结果」与「仍开放的 unknown」。核对只针对已交付正文的覆盖结构，不改变任何正文的编辑/验证状态。

- **06.1/06.7/06.8（原 covered 主题复核）**：三主题五方面均有正文入口。06.1 的状态责任以[并行策略与训练状态](parallelism-and-state.md)的状态矩阵/截取边界和[框架执行](framework-execution.md)的职责图为证；06.7/06.8 以 T06-08（Batch 26）交付的[恢复一致性](checkpoint-state-consistency.md)、[弹性训练](elastic-training-and-membership.md)及其保留边界为证——重分片”不支持/未知”行、MindIO TTP 临终约束、NPU 侧恢复实测缺口均按 [T06-08 最终复核记录](../../docs/research/batch-26-t06-08-codex-recheck.md)保留，未因导航核对升级。
- **06.2–06.6**：分别由 T06-01～T06-07（Batch 24/25）交付的正文承担五方面。各任务的来源/缺口说明与修订、最终复核记录可定位：T06-01（[来源](../../docs/research/batch-24-t06-01-sources.md)·[最终复核](../../docs/research/batch-24-t06-01-codex-recheck-6.md)）、T06-02（[来源](../../docs/research/batch-24-t06-02-sources.md)·[最终复核](../../docs/research/batch-24-t06-02-codex-recheck-4.md)）、T06-03（[来源](../../docs/research/batch-24-t06-03-sources.md)·[最终复核](../../docs/research/batch-24-t06-03-codex-recheck-4.md)）、T06-04（[来源](../../docs/research/batch-25-t06-04-sources.md)·[最终复核](../../docs/research/batch-25-t06-04-codex-recheck-4.md)）、T06-05（[来源](../../docs/research/batch-25-t06-05-sources.md)·[最终复核](../../docs/research/batch-25-t06-05-codex-recheck-3.md)）、T06-06（[来源](../../docs/research/batch-25-t06-06-sources.md)·[最终复核](../../docs/research/batch-25-t06-06-codex-recheck-4.md)）、T06-07（[来源](../../docs/research/batch-25-t06-07-sources.md)·[最终复核](../../docs/research/batch-25-t06-07-codex-recheck-3.md)）。其中两类边界需要区分，不以”内容缺口”笼统表述：
  - 06.3 的[小规模执行路径验证方法](framework-execution.md)已交付并经审阅，缺的是**执行结果**——验证未执行属独立验证轨道，不是内容缺口（06.3 各内容缺口已随 Batch 24 关闭）。
  - 06.4 的受控异步样板**已交付**：verl v0.9.1 legacy V0 含同步、一步异步、完全异步三档 recipe（见[RL rollout](rl-rollout-consistency.md)）；剩余为 V1 控制流等 unknown 与未实测，不是”样板待补”。
- **账面同步（本批执行）**：执行清单（full-coverage-backlog）中 06.2-G3、06.4-G2/G3、06.5-G1/G2/G3、06.6-G1/G2/G3 共 9 项内容缺口的状态此前未随 Batch 25 交付同步——盘点清单（topic-coverage）已记为关闭、对应任务已 done 且上述最终复核记录存在；本批（2026-10-21）按该关闭证据将 9 项同步为 closed。同步只改状态字段，不改变任何技术边界或验证状态。
- **平台边界**：三组框架档案各自绑定固定版本（PyTorch 2.6、Megatron-Core core_v0.19.2、MindSpeed-LLM v2.2.0；checkpoint 侧另有 core_v0.12.1），互不外推；`generic` 行不构成任何平台兼容承诺。
- **未验证状态**：本章全部正文为 draft、未实测；独立实验条目为[精度差异](gpu-npu-precision-difference-experiment.md)与[恢复状态](checkpoint-state-recovery-experiment.md)两篇，其余验证设计内嵌于各指南或复用这两篇（如混合精度沿用精度差异设计、性能验证内嵌于性能分解），全部案例为来源整理；真实环境验证由独立验证轨道（V 工作包）管理。

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

## 成果与后续

已有并行/状态（含 EP/CP 与组合映射）、框架执行职责对照、预训练与微调状态契约、RL rollout 协同、混合精度与收敛验证、性能分解与吞吐回归案例，以及精度迁移、恢复异常、慢 rank、弹性训练的指南/案例/实验设计；八主题五方面入口表与交付核对已随 T06-09 交付（2026-10-21）。后续维护方向：具体工作负载的执行结果（06.3）、verl V1 控制流等 unknown 的取证（06.4）、慢 rank 专用案例/实验补齐与全部真实环境验证（V 工作包）。
