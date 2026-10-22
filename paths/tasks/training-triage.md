---
id: path.task.training-triage
title: 训练排障知识路径
type: path
domain: overview
status: draft
platforms:
- generic
source_refs:
- src.ascend.mind-cluster
- src.ascend.torch-npu
- src.nvidia.nccl-docs
- src.stas.ml-engineering
updated_at: '2026-10-22'
summary: 按问题和证据位置跨领域查找训练诊断知识。
related_ids:
- hardware.resource-topology
- data-storage.training-data-path
- cluster-platform.device-resource-chain
- hardware.index
- software-stack.index
- communication.index
- data-storage.index
- cluster-platform.index
- training.index
- reliability.index
- communication.collectives-and-rank-progress
- communication.bandwidth-baselines
- reliability.dimensions-and-failure-domains
- reliability.evidence-and-hypotheses
- data-storage.checkpoint-durability
- training.parallelism-and-state
- training.checkpoint-state-consistency
- overview.training-lifecycle
- hardware.health-evidence
- cluster-platform.admission-and-placement
- software-stack.ascend-version-mismatch-triage
- software-stack.ascend-version-mismatch-source-case
- software-stack.ascend-version-mismatch-experiment
- cluster-platform.ascend-device-visibility-triage
- cluster-platform.ascend-device-visibility-source-case
- cluster-platform.ascend-device-visibility-experiment
- communication.hccl-timeout-triage
- communication.hccl-timeout-source-case
- communication.hccl-timeout-experiment
- communication.nccl-timeout-triage
- communication.nccl-timeout-source-case
- communication.nccl-timeout-experiment
- training.gpu-npu-precision-difference-triage
- training.gpu-npu-precision-difference-source-case
- training.gpu-npu-precision-difference-experiment
- training.checkpoint-state-recovery-triage
- training.checkpoint-state-recovery-source-case
- training.checkpoint-state-recovery-experiment
- data-storage.data-starvation-triage
- cluster-platform.idle-resource-job-waiting-triage
- software-stack.ascend-memory-oom-evidence
- communication.bandwidth-degradation-triage
- reliability.silent-errors-and-integrity
- training.slow-rank-triage
- data-storage.checkpoint-slow-io-triage
- hardware.power-thermal-evidence
- training.elastic-training-and-membership
- data-storage.checkpoint-integrity-evidence
- hardware.node-acceptance-triage
- software-stack.gpu-op-graph-failure-triage
- software-stack.gpu-memory-oom-evidence
- software-stack.host-resource-pressure-and-device-access
- software-stack.environment-installation-and-upgrade
- training.performance-analysis
- training.performance-regression-source-case
- cluster-platform.control-plane-recovery
- cluster-platform.node-drain-resource-reclamation
- cluster-platform.accelerator-sharing-and-isolation
- cluster-platform.contention-capacity-validation
- data-storage.storage-client-backend-recovery
- hardware.bmc-firmware-and-events
tasks:
- training-triage
---

# 训练排障知识路径

本页帮助 Human 和 Agent 定位需要阅读的知识；它是待完善的导航草稿，不是经过实测的检查顺序或操作处方。`generic` 表示跨平台的导航意图，不保证任意环境适用。

## 先整理问题描述

记录环境和任务配置、最早观察到异常的时间、正常基线、近期变更、受影响的任务或 rank，以及已经掌握的日志和指标。把观察到的现象与推测的原因分开。

对应的方法入口是 [08 可靠性与计算正确性方法](../../knowledge/08-reliability/index.md)，训练状态和正常推进过程的入口是 [06 训练与后训练系统](../../knowledge/06-training/index.md)。

先用[训练任务全流程](../../knowledge/00-overview/training-lifecycle.md)定位观察阶段。资源等待见[准入与放置](../../knowledge/05-cluster-platform/admission-and-placement.md)，设备状态见[健康证据边界](../../knowledge/01-hardware/health-evidence.md)。

## 阅读目标与完成检查

**进入条件**：已按上节整理问题描述（环境配置、异常时间、基线、近期变更、受影响 rank、已掌握证据）。

**知识目标**：按现象找到首要知识领域与候选原因，形成可检验的假设与下一项检查，而不是直接跳到结论。

**完成检查**：一次知识定位完成时应能写出——①现象与影响范围（对象/时间窗口/统计口径）；②首要领域入口与至少两个候选原因（含已排除项及排除证据）；③缺失证据与下一项检查（比较收益、代价和影响）；④停止/升级条件（证据不足、权限不足、无回退时各自的动作）。任一写不出即未完成；仍不能定位时，记录已排除范围与缺口后升级，不反复猜测。

## 按问题选择知识入口

| 观察到的问题 | 首要阅读位置 | 需要关联的位置 |
|---|---|---|
| 环境安装失败、库加载或算子执行异常 | [02 软件栈](../../knowledge/02-software-stack/index.md) | [06 训练](../../knowledge/06-training/index.md)：模型和执行配置 |
| 任务未获得设备、容器内设备不可见 | [设备资源状态链](../../knowledge/05-cluster-platform/device-resource-chain.md) | [节点资源与拓扑](../../knowledge/01-hardware/resource-topology.md)及[02 软件栈](../../knowledge/02-software-stack/index.md)：物理资源、主机驱动与执行环境 |
| 集合通信超时、不同 rank 进度不一致 | [03 通信](../../knowledge/03-communication/index.md) | [06 训练](../../knowledge/06-training/index.md)与[01 硬件](../../knowledge/01-hardware/index.md)：计算进展和设备证据 |
| 吞吐退化、慢 rank、资源使用不均 | [慢 rank 诊断](../../knowledge/06-training/slow-rank-triage.md) | [通信带宽退化诊断](../../knowledge/03-communication/bandwidth-degradation-triage.md)与[04 数据存储](../../knowledge/04-data-storage/index.md)：通信口径/配置/链路分支和数据路径 |
| checkpoint 保存/恢复慢、保存期间训练停顿 | [Checkpoint 慢写诊断](../../knowledge/04-data-storage/checkpoint-slow-io-triage.md) | [Checkpoint 持久化边界](../../knowledge/04-data-storage/checkpoint-durability.md) 与[06 训练](../../knowledge/06-training/index.md)：完成语义与训练状态 |
| 节点故障后训练能否缩容继续、成员变更后状态是否正确 | [弹性训练与成员变更](../../knowledge/06-training/elastic-training-and-membership.md) | [Checkpoint 恢复一致性](../../knowledge/06-training/checkpoint-state-consistency.md)：状态恢复是应用责任；[08 可靠性](../../knowledge/08-reliability/index.md)：恢复验证 |
| loss 偏差怀疑硬件误算、健康检查全绿但结果异常 | [静默错误与计算完整性判定](../../knowledge/08-reliability/silent-errors-and-integrity.md) | [06 训练](../../knowledge/06-training/gpu-npu-precision-difference-triage.md)：先按精度差异诊断扣除数值噪声 |
| 取 batch 等待增加、设备间歇空闲 | [训练数据加载饥饿诊断](../../knowledge/04-data-storage/data-starvation-triage.md) | [训练数据供给路径](../../knowledge/04-data-storage/training-data-path.md) 与[节点资源与拓扑](../../knowledge/01-hardware/resource-topology.md)：阶段框架、主机内存、I/O 路径和共享资源 |
| 集群有空闲设备但作业不运行 | [空闲设备但作业等待诊断](../../knowledge/05-cluster-platform/idle-resource-job-waiting-triage.md) | [准入与放置](../../knowledge/05-cluster-platform/admission-and-placement.md) 与[设备资源链](../../knowledge/05-cluster-platform/device-resource-chain.md) |
| loss、梯度或迁移后的数值行为变化 | [06 训练](../../knowledge/06-training/index.md) | [02 软件栈](../../knowledge/02-software-stack/index.md)与[08 可靠性](../../knowledge/08-reliability/index.md)：精度语义和验证方法 |
| checkpoint 读取失败或恢复后状态异常 | [06 训练](../../knowledge/06-training/index.md) | [04 数据存储](../../knowledge/04-data-storage/index.md)：文件与持久性；[Checkpoint 完整性与校验证据](../../knowledge/04-data-storage/checkpoint-integrity-evidence.md)：字节/文件损坏的分层发现能力；[08 可靠性](../../knowledge/08-reliability/index.md)：完成判据 |
| 新节点或返修节点能否承担训练负载 | [新节点与返修节点验收](../../knowledge/01-hardware/node-acceptance-triage.md) | [健康证据](../../knowledge/01-hardware/health-evidence.md) 与[供电散热证据](../../knowledge/01-hardware/power-thermal-evidence.md)：被动证据层的边界 |
| GPU 侧算子、编译或图执行失败（NVIDIA/AMD） | [GPU 算子、编译和图执行失败的定向诊断](../../knowledge/02-software-stack/gpu-op-graph-failure-triage.md) | [02 软件栈](../../knowledge/02-software-stack/index.md)：后端注册、动态编译、graph capture 与异步报错四分支；昇腾侧另见[昇腾算子与图编译失败诊断](../../knowledge/02-software-stack/ascend-op-graph-failure-triage.md) |
| GPU 显存占用疑问或设备侧 OOM（NVIDIA/AMD） | [GPU 分配器、保留内存与 OOM 证据](../../knowledge/02-software-stack/gpu-memory-oom-evidence.md) | [06 训练](../../knowledge/06-training/index.md)：负载与并行配置；昇腾侧见[昇腾 NPU 内存与 OOM 证据](../../knowledge/02-software-stack/ascend-memory-oom-evidence.md) |
| 主机内存/进程资源压力影响训练或设备访问 | [OS/进程资源压力与设备访问诊断](../../knowledge/02-software-stack/host-resource-pressure-and-device-access.md) | [NUMA 与 I/O 局部性](../../knowledge/01-hardware/numa-memory-and-io-locality.md) 与[05 集群平台](../../knowledge/05-cluster-platform/index.md)：局部性与限额 |
| 训练吞吐退化、性能不达预期（非单 rank 异常） | [训练性能分解、profiling 与优化验证](../../knowledge/06-training/performance-analysis.md) | [慢 rank 诊断](../../knowledge/06-training/slow-rank-triage.md) 与[性能优化任务路径](performance-optimization.md)：先固定口径再分层 |
| 平台/调度器故障后作业与队列状态异常 | [控制面故障、平台恢复与账本核对](../../knowledge/05-cluster-platform/control-plane-recovery.md) | [05 集群平台](../../knowledge/05-cluster-platform/index.md)：Kubernetes/Slurm 分支与恢复后账本核验 |
| 节点摘除、drain 期间的作业与资源回收 | [节点摘除、drain 与资源回收流程](../../knowledge/05-cluster-platform/node-drain-resource-reclamation.md) | [弹性训练与成员变更](../../knowledge/06-training/elastic-training-and-membership.md)：缩容续训的状态责任 |
| 多租户共享引起的争用或不公平 | [加速器共享与租户隔离机制](../../knowledge/05-cluster-platform/accelerator-sharing-and-isolation.md) | [多租户争用与容量验证](../../knowledge/05-cluster-platform/contention-capacity-validation.md)：利用率不等于可用容量 |
| 存储客户端/后端异常影响数据读取或 checkpoint | [存储客户端、后端异常与恢复验证](../../knowledge/04-data-storage/storage-client-backend-recovery.md) | [04 数据存储](../../knowledge/04-data-storage/index.md)：先保留证据、保护恢复点 |
| 固件身份或带外（BMC）事件需要核对 | [BMC、固件身份与跨层硬件事件](../../knowledge/01-hardware/bmc-firmware-and-events.md) | [健康证据](../../knowledge/01-hardware/health-evidence.md)：单一事件不可直接归因 |

表中的首要入口是内容归属，不是根因结论。调查过程可能需要多次跨层回查。

## 平台分支

- [昇腾平台路径](../platforms/ascend.md)：进一步定位 CANN/torch_npu 配套、HCCL、NPU 设备管理和训练恢复资料。
- [NVIDIA 平台路径](../platforms/nvidia.md)：进一步定位驱动/CUDA、NCCL 与 GPU 相关资料。
- [AMD 平台路径](../platforms/amd.md)：进一步定位 ROCm/HIP、RCCL 与 AMD GPU 相关资料。

## 任务路径

本页是排障首要入口；准备与运行阶段的完整路径另有分页：[选型与容量](selection-and-capacity.md) · [节点验收](node-acceptance.md) · [环境安装](environment-installation.md) · [性能优化](performance-optimization.md) · [迁移与升级](migration-and-upgrade.md) · [故障恢复](fault-recovery.md)（恢复验收要求正确性与持续进展双判据）。按角色阅读见[角色路径](../roles/reading-by-role.md)。

## 形成案例时保留什么

保留原始环境、证据时间线、候选原因、区分检查、采取的动作及验证结果。明确哪些原因已排除、哪些仍未知，以及是否确认了训练状态正确和持续进展。案例归入主要调查问题所在的章节，再关联其他涉及领域。

## 原始资料入口

- [MindCluster](https://github.com/Ascend/mind-cluster)：故障诊断与恢复相关资料。
- [TorchNPU](https://github.com/Ascend/pytorch)：环境与框架后端相关资料。
- [NVIDIA NCCL 用户指南](https://docs.nvidia.com/deeplearning/nccl/user-guide/docs/index.html)：通信诊断资料。
- [ML Engineering](https://github.com/stas00/ml-engineering)：训练工程问题资料。

当前提供概念、参考、带条件的诊断指南、公开来源案例和实验设计；现场可执行步骤及本地验证证据仍需匹配环境。

## 通信与可靠性基础

- [集合通信与 rank 进度](../../knowledge/03-communication/collectives-and-rank-progress.md)和[通信性能口径](../../knowledge/03-communication/bandwidth-baselines.md)：解释参与者、超时与可比较的性能证据；各平台版本独立核对。
- [可靠性维度](../../knowledge/08-reliability/dimensions-and-failure-domains.md)和[证据与假设](../../knowledge/08-reliability/evidence-and-hypotheses.md)：定义成功标准、故障范围和下一项检查。
- [Checkpoint 持久化边界](../../knowledge/04-data-storage/checkpoint-durability.md)：区分模型/训练状态文件的写入、提交与恢复可用性，不代表引擎热加载或训练恢复已验证。

## 工作负载状态与指标

- [并行策略与训练状态](../../knowledge/06-training/parallelism-and-state.md)。
- [Checkpoint 恢复一致性](../../knowledge/06-training/checkpoint-state-consistency.md)。

这些是固定来源下的概念与参考草稿；框架、NPU 插件与硬件条件分别核对，不自动组成支持矩阵。

## 场景阅读入口

指南给出证据分支，案例保留原始环境和未解项，实验仅提供待执行设计。

- 昇腾版本配套：[诊断](../../knowledge/02-software-stack/ascend-version-mismatch-triage.md) · [案例](../../knowledge/02-software-stack/ascend-version-mismatch-source-case.md) · [实验设计](../../knowledge/02-software-stack/ascend-version-mismatch-experiment.md)。
- 容器内 NPU 可见性：[诊断](../../knowledge/05-cluster-platform/ascend-device-visibility-triage.md) · [案例](../../knowledge/05-cluster-platform/ascend-device-visibility-source-case.md) · [实验设计](../../knowledge/05-cluster-platform/ascend-device-visibility-experiment.md)。
- HCCL 超时：[诊断](../../knowledge/03-communication/hccl-timeout-triage.md) · [案例](../../knowledge/03-communication/hccl-timeout-source-case.md) · [实验设计](../../knowledge/03-communication/hccl-timeout-experiment.md)。
- NCCL 超时：[诊断](../../knowledge/03-communication/nccl-timeout-triage.md) · [案例](../../knowledge/03-communication/nccl-timeout-source-case.md) · [实验设计](../../knowledge/03-communication/nccl-timeout-experiment.md)。

- GPU→NPU 精度差异：[诊断](../../knowledge/06-training/gpu-npu-precision-difference-triage.md) · [案例](../../knowledge/06-training/gpu-npu-precision-difference-source-case.md) · [实验设计](../../knowledge/06-training/gpu-npu-precision-difference-experiment.md)。

- Checkpoint 恢复状态：[诊断](../../knowledge/06-training/checkpoint-state-recovery-triage.md) · [案例](../../knowledge/06-training/checkpoint-state-recovery-source-case.md) · [实验设计](../../knowledge/06-training/checkpoint-state-recovery-experiment.md)。该恢复案例为 CPU 来源，GPU/NPU 运行条件另核。
