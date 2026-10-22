---
id: path.task.inference-triage
title: 推理排障知识路径
type: path
domain: overview
status: draft
platforms:
- generic
source_refs:
- src.ascend.vllm-ascend
- src.ascend.agent-skills
- src.stas.ml-engineering
updated_at: '2026-10-22'
summary: 按请求路径和观察证据跨领域查找推理诊断知识。
related_ids:
- hardware.index
- hardware.resource-topology
- software-stack.index
- communication.index
- data-storage.index
- cluster-platform.index
- cluster-platform.device-resource-chain
- inference.index
- reliability.index
- communication.collectives-and-rank-progress
- communication.bandwidth-baselines
- reliability.dimensions-and-failure-domains
- reliability.evidence-and-hypotheses
- data-storage.checkpoint-durability
- inference.execution-and-kv-cache
- inference.latency-metrics
- overview.inference-lifecycle
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
- inference.ascend-inference-tail-latency-triage
- inference.ascend-inference-tail-latency-source-case
- inference.ascend-inference-tail-latency-experiment
- inference.ascend-inference-oom-triage
- inference.quantization-and-quality
- inference.pd-disaggregation
- inference.model-loading-and-readiness
- inference.engine-backend-boundaries
- inference.output-quality-evaluation
- inference.capacity-and-autoscaling
- inference.routing-and-flow-control
- inference.release-and-recovery
- inference.distributed-inference-layouts
- inference.gpu-inference-oom-triage
- data-storage.storage-client-backend-recovery
tasks:
- inference-triage
---

# 推理排障知识路径

本页帮助 Human 和 Agent 定位需要阅读的知识；它是待完善的导航草稿，不是经过实测的检查顺序或操作处方。`generic` 表示跨平台的导航意图，不保证任意环境适用。

## 先整理问题描述

记录平台环境、模型与引擎配置、请求与输出长度、并发和流量变化、异常发生时间、受影响副本，以及指标的统计窗口。把请求失败、性能变化和输出质量变化分别描述。

请求执行路径和指标含义从 [07 推理与服务系统](../../knowledge/07-inference/index.md)进入；证据、假设和验证方法从 [08 可靠性与计算正确性方法](../../knowledge/08-reliability/index.md)进入。

先用[推理请求全流程](../../knowledge/00-overview/inference-lifecycle.md)定位观察阶段。资源等待见[准入与放置](../../knowledge/05-cluster-platform/admission-and-placement.md)，设备状态见[健康证据边界](../../knowledge/01-hardware/health-evidence.md)。

## 阅读目标与完成检查

**进入条件**：已按上节整理问题描述（平台环境、模型与引擎配置、请求分布、异常时间、受影响副本、指标统计窗口；请求失败、性能变化与输出质量变化分别描述）。

**知识目标**：按请求路径与观察证据找到首要知识领域与候选原因，形成可检验的假设与下一项检查。

**完成检查**：一次知识定位完成时应能写出——①现象与影响范围（请求/副本/指标口径，客户端与服务端观测分开）；②首要领域入口与至少两个候选原因（含已排除项及排除证据）；③缺失证据与下一项检查；④停止/升级条件（证据不足、权限不足、无回退时各自的动作）。任一写不出即未完成；仍不能定位时，记录已排除范围与缺口后升级，不反复猜测。

## 按问题选择知识入口

| 观察到的问题 | 首要阅读位置 | 需要关联的位置 |
|---|---|---|
| 引擎无法启动、模型加载失败 | [07 推理](../../knowledge/07-inference/index.md) | [02 软件栈](../../knowledge/02-software-stack/index.md)与[04 数据存储](../../knowledge/04-data-storage/index.md)：依赖、执行后端和模型文件 |
| 设备资源未分配或副本未就绪 | [设备资源链](../../knowledge/05-cluster-platform/device-resource-chain.md) | [节点拓扑](../../knowledge/01-hardware/resource-topology.md)与[07 推理](../../knowledge/07-inference/index.md)：物理资源、容器访问和服务生命周期 |
| TTFT、TPOT 或长尾变化 | [07 推理](../../knowledge/07-inference/index.md) | 按证据关联[03 通信](../../knowledge/03-communication/index.md)、[04 数据存储](../../knowledge/04-data-storage/index.md)或[05 集群平台](../../knowledge/05-cluster-platform/index.md) |
| 昇腾推理 OOM、缓存压力或吞吐变化 | [昇腾推理 OOM 诊断](../../knowledge/07-inference/ascend-inference-oom-triage.md) | [07 推理](../../knowledge/07-inference/index.md) 与[02 软件栈](../../knowledge/02-software-stack/ascend-memory-oom-evidence.md)：请求阶段、内存分层语义；[01 硬件](../../knowledge/01-hardware/index.md)：资源组成 |
| 量化、迁移或升级后的输出质量变化 | [推理量化与输出质量验证](../../knowledge/07-inference/quantization-and-quality.md) | [07 推理](../../knowledge/07-inference/index.md) 与[02 软件栈](../../knowledge/02-software-stack/index.md)、[08 可靠性](../../knowledge/08-reliability/silent-errors-and-integrity.md)：精度语义和质量验证 |
| P/D 分离部署的形态、连接器选择与支持边界 | [PD 分离与流量分配](../../knowledge/07-inference/pd-disaggregation.md) | [07 推理](../../knowledge/07-inference/index.md) 与[03 通信](../../knowledge/03-communication/index.md)：KV 传输依赖与代理层职责 |
| 分布式推理异常或通信超时 | [03 通信](../../knowledge/03-communication/index.md) | [07 推理](../../knowledge/07-inference/index.md)：请求阶段与执行进展 |
| GPU（NVIDIA/AMD）推理 OOM 或状态恢复 | [GPU 推理 OOM 快速分流](../../knowledge/07-inference/gpu-inference-oom-triage.md#快速分流先找下一项检查) | [GPU 内存与 OOM 证据](../../knowledge/02-software-stack/gpu-memory-oom-evidence.md) 与[07 推理](../../knowledge/07-inference/index.md)：按首失败阶段定位 |
| 权重加载失败、引擎未 ready 或启动失败 | [权重加载、引擎 ready 与启动失败诊断](../../knowledge/07-inference/model-loading-and-readiness.md) | [02 软件栈](../../knowledge/02-software-stack/index.md) 与[04 数据存储](../../knowledge/04-data-storage/index.md)：装载链与模型文件 |
| 引擎能力或平台功能交集疑问 | [推理引擎组件与平台功能交集档案](../../knowledge/07-inference/engine-backend-boundaries.md) | [07 推理](../../knowledge/07-inference/index.md)：支持/条件/未证实/冲突分档 |
| 输出质量差异需要系统性评估 | [推理输出质量的对照评估方法与案例](../../knowledge/07-inference/output-quality-evaluation.md) | [量化与质量验证](../../knowledge/07-inference/quantization-and-quality.md) 与[静默错误判定](../../knowledge/08-reliability/silent-errors-and-integrity.md) |
| 容量不足、扩缩容或冷启动决策 | [容量、扩缩容与冷启动决策](../../knowledge/07-inference/capacity-and-autoscaling.md) | [05 集群平台](../../knowledge/05-cluster-platform/index.md) 与[性能优化任务路径](performance-optimization.md)：容量口径与触发器代价 |
| 请求路由、准入或流控问题 | [请求路由、准入与流控](../../knowledge/07-inference/routing-and-flow-control.md) | [07 推理](../../knowledge/07-inference/index.md)：路由四层职责与重试边界 |
| 服务发布、副本故障或恢复后验证 | [服务版本发布、副本故障与恢复验证](../../knowledge/07-inference/release-and-recovery.md) | [故障恢复任务路径](fault-recovery.md) 与[08 可靠性](../../knowledge/08-reliability/index.md)：恢复验证设计与记账 |
| 存储后端异常影响模型加载或权重读回 | [存储客户端、后端异常与恢复验证](../../knowledge/04-data-storage/storage-client-backend-recovery.md) | [04 数据存储](../../knowledge/04-data-storage/index.md) 与[制品传输与读回](../../knowledge/04-data-storage/artifact-transfer-and-publication.md) |

表中的首要入口是内容归属，不是根因结论。相同症状在不同引擎、平台和请求分布下可能需要不同证据。

## 平台分支

- [昇腾平台路径](../platforms/ascend.md)：定位 NPU 软件栈、vLLM Ascend、设备管理和通信资料。
- [NVIDIA 平台路径](../platforms/nvidia.md)：定位 GPU 软件栈、通信与设备相关资料。
- [AMD 平台路径](../platforms/amd.md)：定位 ROCm/HIP、RCCL 与 AMD GPU 推理资料。

## 任务路径

本页是排障首要入口；准备与运行阶段的完整路径另有分页：[选型与容量](selection-and-capacity.md) · [节点验收](node-acceptance.md) · [环境安装](environment-installation.md) · [性能优化](performance-optimization.md) · [迁移与升级](migration-and-upgrade.md) · [故障恢复](fault-recovery.md)。按角色阅读见[角色路径](../roles/reading-by-role.md)。

## 形成案例时保留什么

保留环境和请求分布、对照基线、变更记录、跨服务与引擎的证据，以及采取动作后的结果。分别说明请求能否成功、输出质量是否达到约定标准、性能是否回到目标范围，并保留未完成的验证。

## 原始资料入口

- [vLLM Ascend](https://github.com/vllm-project/vllm-ascend)：引擎后端、部署和问题资料。
- [Ascend Agent Skills](https://github.com/Ascend/agent-skills)：推理资料与 FAQ 整理流程参考。
- [ML Engineering](https://github.com/stas00/ml-engineering)：推理工程背景资料。

当前提供基础概念、指标参考、带条件的诊断指南、公开来源案例和实验设计；现场可执行步骤及本地验证证据仍需匹配环境。

## 通信与可靠性基础

- [集合通信与 rank 进度](../../knowledge/03-communication/collectives-and-rank-progress.md)和[通信性能口径](../../knowledge/03-communication/bandwidth-baselines.md)：解释参与者、超时与可比较的性能证据；各平台版本独立核对。
- [可靠性维度](../../knowledge/08-reliability/dimensions-and-failure-domains.md)和[证据与假设](../../knowledge/08-reliability/evidence-and-hypotheses.md)：定义成功标准、故障范围和下一项检查。
- [Checkpoint 持久化边界](../../knowledge/04-data-storage/checkpoint-durability.md)：区分模型/训练状态文件的写入、提交与恢复可用性，不代表引擎热加载或训练恢复已验证。

## 工作负载状态与指标

- [推理执行与 KV cache](../../knowledge/07-inference/execution-and-kv-cache.md)。
- [推理延迟与吞吐指标字典](../../knowledge/07-inference/latency-metrics.md)。

这些是固定来源下的概念与参考草稿；框架、NPU 插件与硬件条件分别核对，不自动组成支持矩阵。

## 场景阅读入口

指南给出证据分支，案例保留原始环境和未解项，实验仅提供待执行设计。

- 昇腾版本配套：[诊断](../../knowledge/02-software-stack/ascend-version-mismatch-triage.md) · [案例](../../knowledge/02-software-stack/ascend-version-mismatch-source-case.md) · [实验设计](../../knowledge/02-software-stack/ascend-version-mismatch-experiment.md)。
- 容器内 NPU 可见性：[诊断](../../knowledge/05-cluster-platform/ascend-device-visibility-triage.md) · [案例](../../knowledge/05-cluster-platform/ascend-device-visibility-source-case.md) · [实验设计](../../knowledge/05-cluster-platform/ascend-device-visibility-experiment.md)。
- HCCL 超时：[诊断](../../knowledge/03-communication/hccl-timeout-triage.md) · [案例](../../knowledge/03-communication/hccl-timeout-source-case.md) · [实验设计](../../knowledge/03-communication/hccl-timeout-experiment.md)。
- NCCL 超时：[诊断](../../knowledge/03-communication/nccl-timeout-triage.md) · [案例](../../knowledge/03-communication/nccl-timeout-source-case.md) · [实验设计](../../knowledge/03-communication/nccl-timeout-experiment.md)。
- 昇腾推理长尾：[诊断](../../knowledge/07-inference/ascend-inference-tail-latency-triage.md) · [案例](../../knowledge/07-inference/ascend-inference-tail-latency-source-case.md) · [实验设计](../../knowledge/07-inference/ascend-inference-tail-latency-experiment.md)。
