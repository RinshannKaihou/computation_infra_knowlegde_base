---
id: path.platform.ascend
title: 昇腾平台知识路径
type: path
domain: overview
status: draft
platforms:
- ascend
source_refs:
- src.ascend.agent-skills
- src.ascend.mind-cluster
- src.ascend.torch-npu
- src.ascend.vllm-ascend
updated_at: '2026-10-22'
summary: 通过各领域主目录定位昇腾 NPU 的全栈知识。
related_ids:
- overview.index
- hardware.index
- hardware.resource-topology
- software-stack.index
- software-stack.layers-and-boundaries
- software-stack.compatibility-evidence
- software-stack.ascend-documented-profile
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
- software-stack.ascend-version-mismatch-triage
- software-stack.ascend-version-mismatch-source-case
- software-stack.ascend-version-mismatch-experiment
- cluster-platform.ascend-device-visibility-triage
- cluster-platform.ascend-device-visibility-source-case
- cluster-platform.ascend-device-visibility-experiment
- communication.hccl-timeout-triage
- communication.hccl-timeout-source-case
- communication.hccl-timeout-experiment
- inference.ascend-inference-tail-latency-triage
- inference.ascend-inference-tail-latency-source-case
- inference.ascend-inference-tail-latency-experiment
- training.gpu-npu-precision-difference-triage
- training.gpu-npu-precision-difference-source-case
- training.gpu-npu-precision-difference-experiment
- training.checkpoint-state-recovery-triage
- training.checkpoint-state-recovery-source-case
- training.checkpoint-state-recovery-experiment
- software-stack.ascend-memory-oom-evidence
- inference.ascend-inference-oom-triage
- communication.bandwidth-degradation-triage
- hardware.power-thermal-evidence
- data-storage.checkpoint-slow-io-triage
- software-stack.ascend-op-graph-failure-triage
- training.elastic-training-and-membership
- inference.quantization-and-quality
- inference.pd-disaggregation
- hardware.node-acceptance-triage
- data-storage.checkpoint-integrity-evidence
- hardware.accelerator-execution-and-data-movement
- hardware.bmc-firmware-and-events
- hardware.numa-memory-and-io-locality
- hardware.node-selection-and-lifecycle
- communication.interconnect-paths
- software-stack.runtime-execution-and-library-loading
- software-stack.operators-compilers-and-graphs
- software-stack.dtype-layout-and-precision-semantics
- software-stack.framework-backend-adaptation
- software-stack.host-resource-pressure-and-device-access
- software-stack.environment-installation-and-upgrade
- cluster-platform.container-image-runtime-baseline
- cluster-platform.kubernetes-job-lifecycle
- cluster-platform.slurm-jobs-and-device-resources
- cluster-platform.accelerator-sharing-and-isolation
- cluster-platform.contention-capacity-validation
- training.framework-execution
- training.pretraining-and-finetuning
- training.rl-rollout-consistency
- training.mixed-precision-and-convergence
- training.performance-analysis
- inference.engine-backend-boundaries
- inference.mindie-execution-profile
- inference.model-loading-and-readiness
- inference.distributed-inference-layouts
- inference.output-quality-evaluation
- inference.capacity-and-autoscaling
- inference.release-and-recovery
---

# 昇腾平台知识路径

这是阅读与知识定位路径，尚未形成经过实测的安装、诊断或恢复流程。专题通过引用组织内容，具体正文在主目录维护。

## 第一组阅读材料

依次阅读[软件栈分层](../../knowledge/02-software-stack/layers-and-boundaries.md)、[配套证据判断](../../knowledge/02-software-stack/compatibility-evidence.md)、[昇腾文档配套档案](../../knowledge/02-software-stack/ascend-documented-profile.md)。这组草稿帮助识别组件与版本证据，档案中的未知项需要匹配实际环境继续核查。

继续阅读[节点资源与拓扑](../../knowledge/01-hardware/resource-topology.md)、[训练数据供给路径](../../knowledge/04-data-storage/training-data-path.md)和[设备资源链](../../knowledge/05-cluster-platform/device-resource-chain.md)。其中 Atlas 产品资料与 MindCluster 固定快照分别支撑硬件例子和插件实现；它们不与 TorchNPU 档案自动组成一套已验证环境。数据路径中的 CUDA 参数说明也不代表 NPU 行为。

## 先明确环境

后续查阅具体条目前，记录芯片与服务器、固件与驱动、CANN、框架及设备后端、训练或推理引擎、算子包和拓扑；工作负载相关内容还需要模型、精度、执行模式与并行配置。当前尚无本库实测的兼容档案。

## 阅读目标与完成检查

**进入条件**：已读[00 导读](../../knowledge/00-overview/index.md)并按上节记录目标环境身份；首次接触软件栈分层者先读[软件栈分层](../../knowledge/02-software-stack/layers-and-boundaries.md)。

**知识目标**：能按问题在本页定位昇腾侧正文与平台档案，并说出每个入口的证据边界。

**完成检查**：走完路径后应能——①列出目标环境的版本/制品身份，并指出哪些组合在[昇腾文档配套档案](../../knowledge/02-software-stack/ascend-documented-profile.md)中无证据（文档样板与实际环境分开；TorchNPU 档案不与 MindCluster/Atlas 资料自动组成已验证环境）；②对选定任务（配套/算子/内存/通信/推理/恢复）说出首要入口与下一项验证还缺什么证据；③区分通用机制正文与含昇腾取证的正文（如 GPU 侧通用指南不自动适用 NPU）。任一答不出即回到对应入口补读。

## 跨平台比较的阅读方式

与[NVIDIA 路径](nvidia.md)、[AMD 路径](amd.md)使用相同的领域归属，先明确要比较的任务和环境，再比较具体机制；各平台的错误码、环境变量、诊断工具与支持边界分别查证，术语与字段名不作直译映射。

## 完整平台阅读路径

1. [00 导读与系统全景](../../knowledge/00-overview/index.md)：先确定是在学习系统组成，还是定位一个训练或推理问题。
2. [01 物理设施与计算节点](../../knowledge/01-hardware/index.md)：NPU 执行单元、设备内存、服务器组成和硬件健康。
3. [02 系统软件与加速器执行栈](../../knowledge/02-software-stack/index.md)：CANN、驱动、框架、torch_npu、算子与环境配套。
4. [03 互联网络与分布式通信](../../knowledge/03-communication/index.md)：HCCL、拓扑、rank 关系、通信性能和异常证据。
5. [04 数据路径与存储系统](../../knowledge/04-data-storage/index.md)：数据加载、模型文件及 checkpoint I/O 和持久性。
6. [05 集群平台与资源管理](../../knowledge/05-cluster-platform/index.md)：容器设备可见性、设备分配、健康上报和集群调度。
7. [06 训练与后训练系统](../../knowledge/06-training/index.md)：框架与 MindSpeed 相关实践、精度与性能、训练状态和恢复验证。
8. [07 推理与服务系统](../../knowledge/07-inference/index.md)：vLLM Ascend、MindIE 等引擎的执行与服务问题。
9. [08 可靠性与计算正确性方法](../../knowledge/08-reliability/index.md)：将现场证据组织成可验证的判断和案例。

## 按问题选择入口

- 版本配套、算子或执行模式问题：从 [02 软件栈](../../knowledge/02-software-stack/index.md)开始；算子不支持与图编译失败另有[分层诊断](../../knowledge/02-software-stack/ascend-op-graph-failure-triage.md)。
- NPU 内存占用疑问或 “NPU out of memory”：从[昇腾 NPU 内存与 OOM 证据](../../knowledge/02-software-stack/ascend-memory-oom-evidence.md)开始，先按报错文案区分抛出层。
- 宿主机识卡，但任务看不到设备：从[设备资源链](../../knowledge/05-cluster-platform/device-resource-chain.md)开始，并关联 02。
- batch 供给不及时或设备间歇空闲：从[训练数据供给路径](../../knowledge/04-data-storage/training-data-path.md)开始，再关联节点拓扑和通信。
- HCCL 超时或多机性能退化：从 [03 通信](../../knowledge/03-communication/index.md)开始，再按证据关联工作负载和设备层；带宽类退化另有[通信带宽退化诊断](../../knowledge/03-communication/bandwidth-degradation-triage.md)（含 HCCL Test 口径分支）。
- 迁移后 loss、吞吐或训练恢复状态变化：从 [06 训练](../../knowledge/06-training/index.md)开始。
- 推理长尾、OOM 或输出质量变化：从 [07 推理](../../knowledge/07-inference/index.md)开始；OOM 另有[昇腾推理 OOM 诊断](../../knowledge/07-inference/ascend-inference-oom-triage.md)；量化支持与质量验证见[推理量化与输出质量验证](../../knowledge/07-inference/quantization-and-quality.md)（含 vLLM Ascend 量化指南与评估指南入口）；PD 分离的形态、连接器与昇腾限制见[PD 分离与流量分配](../../knowledge/07-inference/pd-disaggregation.md)。
- 设备降速怀疑（温度/功耗/供电）：从[供电、散热与性能退化证据](../../knowledge/01-hardware/power-thermal-evidence.md)开始，注意 NPU 侧观测缺口。
- Checkpoint 保存慢（MindIO/存储路径）：从[Checkpoint 慢写诊断](../../knowledge/04-data-storage/checkpoint-slow-io-triage.md)开始，含 MindIO ACP 分支；字节/文件是否损坏的分层证据见[Checkpoint 完整性与校验证据](../../knowledge/04-data-storage/checkpoint-integrity-evidence.md)（含 MindIO checker 的文件个数完备性语义）。
- [新节点或返修节点能否投产：从[新节点与返修节点验收](../../knowledge/01-hardware/node-acceptance-triage.md)开始，昇腾侧用 ascend-dmi -dg/-s，注意 root/机型限制与无级别化套件的缺口。

这些是知识归属入口，不能仅凭症状确定根因。

## 硬件、固件与选型（Batch 13–31 交付）

- [加速器执行单元、内存层次与数据移动机制](../../knowledge/01-hardware/accelerator-execution-and-data-movement.md)：Ascend Atlas A2 为三平台样板之一，术语不强行映射。
- [BMC、固件身份与跨层硬件事件](../../knowledge/01-hardware/bmc-firmware-and-events.md)：华为 iBMC 侧固件身份清单与告警事件记录方法（带外—带内映射仍未取得）。
- [NUMA、主机内存与 I/O 局部性的成对验证](../../knowledge/01-hardware/numa-memory-and-io-locality.md)：局部/远端成对测量方法。
- [节点内、节点间与超节点互联路径参考](../../knowledge/03-communication/interconnect-paths.md)：Atlas 800T A2＋Atlas 900 A3 SuperPoD 样板与路径核对表。
- [节点选型、隔离返修、长期管理与退役](../../knowledge/01-hardware/node-selection-and-lifecycle.md)：选型四步法与生命周期状态机。

## 软件栈执行、算子与内存（续）

- [三平台安装基线、迁移升级与回退验证](../../knowledge/02-software-stack/environment-installation-and-upgrade.md)：Ascend（CANN 8.3.RCX 样板）节与七层安装验证梯子。
- [驱动初始化、运行时执行同步与库装载](../../knowledge/02-software-stack/runtime-execution-and-library-loading.md)：CANN 8.2.RC1.alpha001 样板的初始化与库装载核对。
- [算子分发、编译与计算图执行机制](../../knowledge/02-software-stack/operators-compilers-and-graphs.md)：TorchNPU/TorchAir 与 CANN 取证路径。
- [dtype、layout 与有限精度语义](../../knowledge/02-software-stack/dtype-layout-and-precision-semantics.md)：CANN 8.2.RC1.alpha001 入口级精度开关条件句。
- [框架到设备后端的适配与能力核对](../../knowledge/02-software-stack/framework-backend-adaptation.md)：TorchNPU 扩展后端（v7.2.0-pytorch2.6.0 固定快照）能力核对。
- [OS/进程资源压力与设备访问诊断](../../knowledge/02-software-stack/host-resource-pressure-and-device-access.md)：主机资源压力与设备访问分层取证。

## 平台与作业管理

- [镜像制品、容器运行时与设备暴露基线](../../knowledge/05-cluster-platform/container-image-runtime-baseline.md)：MindCluster 固定 commit 的 device-plugin 实现样板。
- [Kubernetes 作业全生命周期与控制器责任](../../knowledge/05-cluster-platform/kubernetes-job-lifecycle.md)与[Slurm 作业生命周期、设备资源与状态参考](../../knowledge/05-cluster-platform/slurm-jobs-and-device-resources.md)：两种调度器的作业状态边界（Slurm 侧 NPU 接入无一手证据）。
- [加速器共享与租户隔离机制](../../knowledge/05-cluster-platform/accelerator-sharing-and-isolation.md)：昇腾静态/动态 vNPU、vCANN-RT 软切分的条件与隔离边界（跨 vNPU 故障隔离保证未证实）。
- [多租户争用、公平性与容量验证](../../knowledge/05-cluster-platform/contention-capacity-validation.md)：单租户基线到两租户并发的对照方法。

## 训练与推理执行（Batch 24/25/27 交付为主）

- [训练框架组件、执行循环与平台职责对照](../../knowledge/06-training/framework-execution.md)：Megatron-Core 与 MindSpeed-LLM v2.2.0 档案的各阶段故障分界。
- [预训练与微调工作流和状态契约](../../knowledge/06-training/pretraining-and-finetuning.md)与[RL rollout、权重同步与训练推理协同](../../knowledge/06-training/rl-rollout-consistency.md)：工作流状态契约与 rollout 一致性。
- [混合精度、算子适配与收敛验证](../../knowledge/06-training/mixed-precision-and-convergence.md)：平台内重复性到单因素精度对照的流程；跨平台首差异另见[GPU→NPU 精度差异诊断](../../knowledge/06-training/gpu-npu-precision-difference-triage.md)。
- [训练性能分解、profiling 与优化验证](../../knowledge/06-training/performance-analysis.md)：有效产出口径与性能取证。
- [推理引擎组件与平台功能交集档案](../../knowledge/07-inference/engine-backend-boundaries.md)与[MindIE 推理执行与配置样板](../../knowledge/07-inference/mindie-execution-profile.md)：vLLM Ascend/MindIE 组件对照与平台交集档案。
- [权重加载、引擎 ready 与启动失败诊断](../../knowledge/07-inference/model-loading-and-readiness.md)：MindIE 装载链与四类启动阶段。
- [分布式推理布局与并行选择](../../knowledge/07-inference/distributed-inference-layouts.md)：vLLM Ascend 与 MindIE 的布局限制（跨页冲突照录）。
- [推理输出质量的对照评估方法与案例](../../knowledge/07-inference/output-quality-evaluation.md)：输入身份固定与四层指标。
- [容量、扩缩容与冷启动决策](../../knowledge/07-inference/capacity-and-autoscaling.md)与[服务版本发布、副本故障与恢复验证](../../knowledge/07-inference/release-and-recovery.md)：容量口径与恢复验证设计。

以上均为固定来源下的文档样板与 draft 正文，不组成支持矩阵；各条目版本边界以正文为准。

## 任务路径入口

排障首要入口：[训练排障](../tasks/training-triage.md) · [推理排障](../tasks/inference-triage.md)。准备阶段：[选型与容量](../tasks/selection-and-capacity.md) · [节点验收](../tasks/node-acceptance.md) · [环境安装](../tasks/environment-installation.md)。运行阶段：[性能优化](../tasks/performance-optimization.md) · [迁移与升级](../tasks/migration-and-upgrade.md) · [故障恢复](../tasks/fault-recovery.md)。按角色阅读见[角色路径](../roles/reading-by-role.md)。

## 原始资料入口

- [Ascend Agent Skills](https://github.com/Ascend/agent-skills)：任务化资料与流程组织参考；本库未安装或执行。
- [MindCluster](https://github.com/Ascend/mind-cluster)：集群管理、诊断与恢复组件资料。
- [TorchNPU](https://github.com/Ascend/pytorch)：框架后端与环境配套资料。
- [vLLM Ascend](https://github.com/vllm-project/vllm-ascend)：推理引擎后端资料。

具体能力和支持关系以所用版本为准。NPU 是覆盖范围，昇腾是当前已有资料的平台专题；其他 NPU 平台待按实际环境补充。

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
- [准入、调度与拓扑放置](../../knowledge/05-cluster-platform/admission-and-placement.md)：从配额与约束定位资源等待。

## 场景阅读入口

指南给出证据分支，案例保留原始环境和未解项，实验仅提供待执行设计。

- 昇腾版本配套：[诊断](../../knowledge/02-software-stack/ascend-version-mismatch-triage.md) · [案例](../../knowledge/02-software-stack/ascend-version-mismatch-source-case.md) · [实验设计](../../knowledge/02-software-stack/ascend-version-mismatch-experiment.md)。
- 容器内 NPU 可见性：[诊断](../../knowledge/05-cluster-platform/ascend-device-visibility-triage.md) · [案例](../../knowledge/05-cluster-platform/ascend-device-visibility-source-case.md) · [实验设计](../../knowledge/05-cluster-platform/ascend-device-visibility-experiment.md)。
- HCCL 超时：[诊断](../../knowledge/03-communication/hccl-timeout-triage.md) · [案例](../../knowledge/03-communication/hccl-timeout-source-case.md) · [实验设计](../../knowledge/03-communication/hccl-timeout-experiment.md)。
- 昇腾推理长尾：[诊断](../../knowledge/07-inference/ascend-inference-tail-latency-triage.md) · [案例](../../knowledge/07-inference/ascend-inference-tail-latency-source-case.md) · [实验设计](../../knowledge/07-inference/ascend-inference-tail-latency-experiment.md)。

- GPU→NPU 精度差异：[诊断](../../knowledge/06-training/gpu-npu-precision-difference-triage.md) · [案例](../../knowledge/06-training/gpu-npu-precision-difference-source-case.md) · [实验设计](../../knowledge/06-training/gpu-npu-precision-difference-experiment.md)。

- Checkpoint 恢复状态：[诊断](../../knowledge/06-training/checkpoint-state-recovery-triage.md) · [案例](../../knowledge/06-training/checkpoint-state-recovery-source-case.md) · [实验设计](../../knowledge/06-training/checkpoint-state-recovery-experiment.md)。该恢复案例为 CPU 来源，GPU/NPU 运行条件另核。
