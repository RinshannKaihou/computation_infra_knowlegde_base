---
id: path.platform.nvidia
title: NVIDIA 平台知识路径
type: path
domain: overview
status: draft
platforms:
- nvidia
source_refs:
- src.nvidia.nccl-docs
- src.nvidia.nccl-tests
- src.stas.ml-engineering
- src.infrasys.aiinfra
updated_at: '2026-10-08'
summary: 通过各领域主目录定位 NVIDIA GPU 的全栈知识。
related_ids:
- overview.index
- hardware.index
- hardware.resource-topology
- software-stack.index
- software-stack.layers-and-boundaries
- software-stack.compatibility-evidence
- communication.index
- data-storage.index
- data-storage.training-data-path
- cluster-platform.index
- cluster-platform.device-resource-chain
- training.index
- inference.index
- reliability.index
- communication.collectives-and-rank-progress
- communication.bandwidth-baselines
- reliability.dimensions-and-failure-domains
- reliability.evidence-and-hypotheses
- data-storage.checkpoint-durability
- training.parallelism-and-state
- training.checkpoint-state-consistency
- inference.execution-and-kv-cache
- inference.latency-metrics
- overview.training-lifecycle
- overview.inference-lifecycle
- hardware.health-evidence
- cluster-platform.admission-and-placement
- software-stack.nvidia-documented-profile
- communication.nccl-timeout-triage
- communication.nccl-timeout-source-case
- communication.nccl-timeout-experiment
- training.gpu-npu-precision-difference-triage
- training.gpu-npu-precision-difference-source-case
- training.gpu-npu-precision-difference-experiment
- training.checkpoint-state-recovery-triage
- training.checkpoint-state-recovery-source-case
- training.checkpoint-state-recovery-experiment
- hardware.power-thermal-evidence
- training.slow-rank-triage
- hardware.node-acceptance-triage
- data-storage.checkpoint-integrity-evidence
- inference.pd-disaggregation
---

# NVIDIA 平台知识路径

这是阅读与知识定位路径，尚未形成经过实测的安装、诊断或恢复流程。已有正文与仍待建设的主题在各章节入口分别标明。

## 已有阅读材料

先读[软件栈分层](../../knowledge/02-software-stack/layers-and-boundaries.md)和[配套证据判断](../../knowledge/02-software-stack/compatibility-evidence.md)，再读[节点资源与拓扑](../../knowledge/01-hardware/resource-topology.md)、[训练数据供给路径](../../knowledge/04-data-storage/training-data-path.md)和[设备资源链](../../knowledge/05-cluster-platform/device-resource-chain.md)。硬件页包含 DGX H100 例子，数据页包含 PyTorch 2.6/CUDA 的限定语义；设备资源链中的 MindCluster 例子仅属于昇腾实现。已有[NVIDIA 文档配套档案](../../knowledge/02-software-stack/nvidia-documented-profile.md)，保留来源冲突与未知组合；尚无本地验证结果。

## 先明确环境

后续查阅具体条目前，记录 GPU 与服务器、固件与驱动、CUDA 与相关库、框架、通信库、引擎及拓扑；工作负载相关内容还需要模型、精度和并行配置。当前尚无本库实测的兼容档案。

## 完整平台阅读路径

1. [00 导读与系统全景](../../knowledge/00-overview/index.md)：训练任务与推理请求涉及哪些系统领域。
2. [01 物理设施与计算节点](../../knowledge/01-hardware/index.md)：GPU、主机资源、服务器组成与硬件健康。
3. [02 系统软件与加速器执行栈](../../knowledge/02-software-stack/index.md)：驱动、CUDA、算子、编译器及框架依赖。
4. [03 互联网络与分布式通信](../../knowledge/03-communication/index.md)：网络和拓扑、NCCL、rank 关系及通信验证。
5. [04 数据路径与存储系统](../../knowledge/04-data-storage/index.md)：数据加载与模型、checkpoint 文件路径。
6. [05 集群平台与资源管理](../../knowledge/05-cluster-platform/index.md)：容器、设备分配、调度与任务生命周期。
7. [06 训练与后训练系统](../../knowledge/06-training/index.md)：并行训练、数值行为、性能与训练状态恢复。
8. [07 推理与服务系统](../../knowledge/07-inference/index.md)：推理引擎、缓存、流量和请求路径。
9. [08 可靠性与计算正确性方法](../../knowledge/08-reliability/index.md)：证据关联、假设检验与恢复验证。

## 跨平台比较的阅读方式

与[昇腾路径](ascend.md)使用相同的领域归属，先明确要比较的任务和环境，再比较具体机制。共同的知识问题包括设备可见性、集合通信进展、数值行为和恢复正确性；两平台的错误码、环境变量、诊断工具与支持边界分别查证。

## 原始资料入口

- [NVIDIA NCCL 用户指南](https://docs.nvidia.com/deeplearning/nccl/user-guide/docs/index.html)：通信原理、配置与诊断资料。
- [NVIDIA nccl-tests](https://github.com/NVIDIA/nccl-tests)：通信测试项目资料。
- [ML Engineering](https://github.com/stas00/ml-engineering)：硬件、训练、推理和工程诊断资料。
- [AIInfra](https://github.com/Infrasys-AI/AIInfra)：全栈背景资料。

NCCL 资料仅覆盖平台知识的一部分；其余领域仍需逐项补齐对应官方来源。

## 通信与可靠性基础

- [集合通信与 rank 进度](../../knowledge/03-communication/collectives-and-rank-progress.md)和[通信性能口径](../../knowledge/03-communication/bandwidth-baselines.md)：解释参与者、超时与可比较的性能证据；各平台版本独立核对。
- [可靠性维度](../../knowledge/08-reliability/dimensions-and-failure-domains.md)和[证据与假设](../../knowledge/08-reliability/evidence-and-hypotheses.md)：定义成功标准、故障范围和下一项检查。
- [Checkpoint 持久化边界](../../knowledge/04-data-storage/checkpoint-durability.md)：区分模型/训练状态文件的写入、提交与恢复可用性，不代表引擎热加载或训练恢复已验证。

## 工作负载状态与指标

- [并行策略与训练状态](../../knowledge/06-training/parallelism-and-state.md)。
- [Checkpoint 恢复一致性](../../knowledge/06-training/checkpoint-state-consistency.md)。
- [推理执行与 KV cache](../../knowledge/07-inference/execution-and-kv-cache.md)。
- [推理延迟与吞吐指标字典](../../knowledge/07-inference/latency-metrics.md)。

这些是固定来源下的概念与参考草稿；框架、NPU 插件与硬件条件分别核对，不自动组成支持矩阵。

## 全流程、健康与放置

- [训练全流程](../../knowledge/00-overview/training-lifecycle.md)与[推理全流程](../../knowledge/00-overview/inference-lifecycle.md)：按阶段定位主目录正文。
- [设备健康证据](../../knowledge/01-hardware/health-evidence.md)：分别阅读 GPU/NPU 字段与检测边界。
- [供电、散热与性能退化证据](../../knowledge/01-hardware/power-thermal-evidence.md)：DCGM 降频位图、violation 计数与健康/诊断边界；NPU 侧观测缺口单独标注。
- [新节点与返修节点验收](../../knowledge/01-hardware/node-acceptance-triage.md)：规格核对、被动证据、DCGM 主动诊断级别与 nccl-tests 基线四层；field diagnostic 与 RMA 边界。
- [PD 分离与流量分配](../../knowledge/07-inference/pd-disaggregation.md)：vLLM v0.14.0 的 connector 形态与"不提升吞吐"的官方边界。
- [Checkpoint 完整性与校验证据](../../knowledge/04-data-storage/checkpoint-integrity-evidence.md)：torch.save CRC32、DCP 2.6 无应用层校验和与存储层 scrub 的分层边界。
- [准入、调度与拓扑放置](../../knowledge/05-cluster-platform/admission-and-placement.md)：从配额与约束定位资源等待。
- [慢 rank 诊断](../../knowledge/06-training/slow-rank-triage.md)：PyTorch 2.8/NCCL RAS 证据样板。

## 场景阅读入口

指南给出证据分支，案例保留原始环境和未解项，实验仅提供待执行设计。

- NCCL 超时：[诊断](../../knowledge/03-communication/nccl-timeout-triage.md) · [案例](../../knowledge/03-communication/nccl-timeout-source-case.md) · [实验设计](../../knowledge/03-communication/nccl-timeout-experiment.md)。

- GPU→NPU 精度差异：[诊断](../../knowledge/06-training/gpu-npu-precision-difference-triage.md) · [案例](../../knowledge/06-training/gpu-npu-precision-difference-source-case.md) · [实验设计](../../knowledge/06-training/gpu-npu-precision-difference-experiment.md)。

- Checkpoint 恢复状态：[诊断](../../knowledge/06-training/checkpoint-state-recovery-triage.md) · [案例](../../knowledge/06-training/checkpoint-state-recovery-source-case.md) · [实验设计](../../knowledge/06-training/checkpoint-state-recovery-experiment.md)。该恢复案例为 CPU 来源，GPU/NPU 运行条件另核。
