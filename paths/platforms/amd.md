---
id: path.platform.amd
title: AMD 平台知识路径
type: path
domain: overview
status: draft
platforms:
- amd
source_refs:
- src.amd.rocm-install-docs-10.1.0
- src.amd.rocm-release-notes-10.1.0
- src.amd.rccl-docs-6.3.3
- src.amd.amd-smi-docs-10.1.0
updated_at: '2026-10-22'
summary: 通过各领域主目录定位 AMD GPU（ROCm）的全栈知识；取证样板与尚未取得资料的边界单列。
related_ids:
- overview.index
- overview.reference-architectures
- hardware.index
- hardware.resource-topology
- hardware.accelerator-execution-and-data-movement
- hardware.bmc-firmware-and-events
- hardware.health-evidence
- hardware.node-selection-and-lifecycle
- software-stack.index
- software-stack.layers-and-boundaries
- software-stack.compatibility-evidence
- software-stack.amd-rocm-documented-profile
- software-stack.environment-installation-and-upgrade
- software-stack.runtime-execution-and-library-loading
- software-stack.operators-compilers-and-graphs
- software-stack.dtype-layout-and-precision-semantics
- software-stack.framework-backend-adaptation
- software-stack.gpu-memory-oom-evidence
- software-stack.gpu-op-graph-failure-triage
- software-stack.host-resource-pressure-and-device-access
- communication.index
- communication.communication-library-profiles
- communication.rccl-runtime-and-verification
- data-storage.index
- cluster-platform.index
- cluster-platform.device-resource-chain
- training.index
- training.mixed-precision-and-convergence
- training.performance-analysis
- inference.index
- inference.engine-backend-boundaries
- inference.model-loading-and-readiness
- inference.distributed-inference-layouts
- inference.gpu-inference-oom-triage
- inference.quantization-and-quality
- inference.output-quality-evaluation
- inference.capacity-and-autoscaling
- inference.routing-and-flow-control
- inference.pd-disaggregation
- inference.release-and-recovery
- reliability.index
- reliability.silent-errors-and-integrity
---

# AMD 平台知识路径

这是阅读与知识定位路径，尚未形成经过实测的安装、诊断或恢复流程。本库 AMD 侧内容以固定文档样板为据（ROCm Core SDK 10.1.0、Instinct MI300X、RCCL 2.30.7 等来源组合，各正文分别注明），**样板不等于兼容矩阵**：未列出的设备/版本组合是无证据，不是不支持，也不是已支持。`amd` 平台标记表示正文含 AMD 取证内容，不构成任何组合的兼容承诺。

## 已有阅读材料

依次阅读[软件栈分层](../../knowledge/02-software-stack/layers-and-boundaries.md)、[配套证据判断](../../knowledge/02-software-stack/compatibility-evidence.md)、[AMD ROCm 软件栈的文档配套档案](../../knowledge/02-software-stack/amd-rocm-documented-profile.md)。档案分层记录组件版本、兼容矩阵、HIP/ROCr 编程运行路径、PyTorch 构建分发关系与安装验证入口，并保留版本标注冲突与未取证边界；档案中的未知项需要匹配实际环境继续核查。继续阅读[计算节点资源与拓扑参考](../../knowledge/01-hardware/resource-topology.md)、[加速器执行单元、内存层次与数据移动机制](../../knowledge/01-hardware/accelerator-execution-and-data-movement.md)（AMD MI200 为三平台样板之一，保留各自真实术语）与[三套通信库能力与版本条件档案](../../knowledge/03-communication/communication-library-profiles.md)（RCCL 2.30.7 独立取证）。

## 先明确环境

后续查阅具体条目前，记录 Instinct 型号与服务器（当前文档样板为 MI300X 平台）、固件 bundle 与 amdgpu 驱动版本、ROCm 版本及其组件（HIP/ROCr/rocBLAS/MIOpen/RCCL）、框架构建或分发渠道、引擎与拓扑；工作负载相关内容还需要模型、精度和并行配置。当前尚无本库实测的 AMD 兼容档案。

## 阅读目标与完成检查

**进入条件**：已读[00 导读](../../knowledge/00-overview/index.md)并按上节记录目标环境身份；首次接触软件栈分层者先读[主机到模型执行的软件栈分层](../../knowledge/02-software-stack/layers-and-boundaries.md)。

**知识目标**：能按问题在本页定位 AMD 侧的取证正文与平台档案，并说出每个入口的证据边界（含 AMD 取证 / 通用方法伴读 / AMD 实现能力未核对三类区分）。

**完成检查**：走完路径后应能——①列出目标环境的版本/制品身份，并指出哪些组合在[AMD ROCm 档案](../../knowledge/02-software-stack/amd-rocm-documented-profile.md)中无证据（文档样板与实际环境分开表述）；②对任一 AMD 术语/工具（如 AMD SMI、RCCL、HIP）能定位其取证正文与 unknown 清单；③对选定任务（安装/诊断/通信/精度/推理）说出下一项验证还缺什么证据。三者任一答不出即未完成，回到对应入口补读。

## 完整平台阅读路径

1. [00 导读与系统全景](../../knowledge/00-overview/index.md)：训练任务与推理请求涉及哪些系统领域；AMD 在参考架构中的位置见[参考架构及选择](../../knowledge/00-overview/reference-architectures.md)——节点级 OEM 样板接入集群形态，超节点层无官方公开样板、保持 unknown 不类推。
2. [01 物理设施与计算节点](../../knowledge/01-hardware/index.md)：GPU 执行组织、设备内存、服务器组成与硬件健康。
3. [02 系统软件与加速器执行栈](../../knowledge/02-software-stack/index.md)：amdgpu 驱动、ROCm/HIP、算子编译与框架适配。
4. [03 互联网络与分布式通信](../../knowledge/03-communication/index.md)：网络和拓扑、RCCL、rank 关系及通信验证。
5. [04 数据路径与存储系统](../../knowledge/04-data-storage/index.md)：数据加载与模型、checkpoint 文件路径（平台无关侧共用）。
6. [05 集群平台与资源管理](../../knowledge/05-cluster-platform/index.md)：容器、设备分配、调度与任务生命周期。设备暴露核对见[设备资源链](../../knowledge/05-cluster-platform/device-resource-chain.md)——它给的是通用责任链（实现例为 MindCluster/NVIDIA 设备插件与 Slurm，**AMD 插件接入未取证**）；AMD 侧设备/容器访问的具体取证（`/dev/kfd`、render node、权限与 ROCm 容器文档）见[OS/进程资源压力与设备访问诊断](../../knowledge/02-software-stack/host-resource-pressure-and-device-access.md)。
7. [06 训练与后训练系统](../../knowledge/06-training/index.md)：并行训练、数值行为、性能与训练状态恢复。
8. [07 推理与服务系统](../../knowledge/07-inference/index.md)：推理引擎、缓存、流量和请求路径。
9. [08 可靠性与计算正确性方法](../../knowledge/08-reliability/index.md)：证据关联、假设检验与恢复验证。

## 按问题选择入口

- 安装、升级或回退：从[三平台安装基线、迁移升级与回退验证](../../knowledge/02-software-stack/environment-installation-and-upgrade.md)的 AMD（ROCm 10.1.0 样板）节开始，先过变更前准入门禁。
- 算子、编译或图执行失败：从[GPU 算子、编译和图执行失败的定向诊断](../../knowledge/02-software-stack/gpu-op-graph-failure-triage.md)开始（NVIDIA CUDA 与 AMD ROCm·HIP 双路径分层取证；CUDA 路径结论不能直接宣称 HIP 适用）。
- 显存占用疑问或 OOM：训练侧[GPU 分配器、保留内存与 OOM 证据](../../knowledge/02-software-stack/gpu-memory-oom-evidence.md)（AMD HIP 7.14.60850 能力与字段独立核对）；推理侧[GPU 推理 OOM 与状态恢复诊断](../../knowledge/07-inference/gpu-inference-oom-triage.md)。
- RCCL 通信异常、带宽或超时：从[RCCL 运行条件、观测与最小验证档案](../../knowledge/03-communication/rccl-runtime-and-verification.md)开始（含 rccl-tests 计时校验口径与两节点最小验证设计）；带宽类退化另见[通信带宽退化诊断](../../knowledge/03-communication/bandwidth-degradation-triage.md)。
- 设备健康、ECC 或 RAS 证据：从[设备健康证据与检测边界](../../knowledge/01-hardware/health-evidence.md)开始（AMD SMI/RAS 最小映射、AFID 事件、N/A 语义与数据不可用判定）；固件与带外事件见[BMC、固件身份与跨层硬件事件](../../knowledge/01-hardware/bmc-firmware-and-events.md)（AMD 机型经 Supermicro BMC OEM 支路取证）。
- 选型、节点验收与生命周期：从[节点选型、隔离返修、长期管理与退役](../../knowledge/01-hardware/node-selection-and-lifecycle.md)开始；四层验收方法见[新节点与返修节点验收](../../knowledge/01-hardware/node-acceptance-triage.md)（通用方法，AMD 侧通信基线样板用 RCCL 档案）。
- 精度、混合精度或收敛疑问：从[混合精度、算子适配与收敛验证](../../knowledge/06-training/mixed-precision-and-convergence.md)与[dtype、layout 与有限精度语义](../../knowledge/02-software-stack/dtype-layout-and-precision-semantics.md)开始。
- 推理引擎、量化或输出质量：从[推理引擎组件与平台功能交集档案](../../knowledge/07-inference/engine-backend-boundaries.md)（AMD/ROCm 交集档案）与[权重加载、引擎 ready 与启动失败诊断](../../knowledge/07-inference/model-loading-and-readiness.md)开始；量化支持与质量验证见[推理量化与输出质量验证](../../knowledge/07-inference/quantization-and-quality.md)（AMD/ROCm 支持矩阵分列）与[输出质量对照评估](../../knowledge/07-inference/output-quality-evaluation.md)。
- 训练性能或慢 rank：从[训练性能分解、profiling 与优化验证](../../knowledge/06-training/performance-analysis.md)开始（含 AMD 取证）。[慢 rank 诊断](../../knowledge/06-training/slow-rank-triage.md)为通用阶段分析方法伴读——其证据样板是 PyTorch 2.8/NCCL RAS/DCGM，**RCCL/ROCm 侧对应检查能力未核对**，不能由接口相似推定适用。
- 健康全绿但结果异常：从[静默错误与计算完整性判定](../../knowledge/08-reliability/silent-errors-and-integrity.md)的平台证据清单（NVIDIA/AMD/Ascend 按版本记录）开始。

这些是知识归属入口，不能仅凭症状确定根因。

## 尚未取得资料与未证实的边界

- 尚未取得资料的设备/版本组合与未取证边界，以[AMD ROCm 档案](../../knowledge/02-software-stack/amd-rocm-documented-profile.md)与[RCCL 档案](../../knowledge/03-communication/rccl-runtime-and-verification.md)的 unknown 清单为准（如整栈实测组合缺口、版本标注冲突的处理口径）。
- AMD 同构超节点：本库未取得官方公开组成样板，超节点层保持 unknown、不从集群样板或 NVIDIA 超节点类推（见[参考架构](../../knowledge/00-overview/reference-architectures.md)的"AMD 的位置与集群样板"节）。
- 本库全部正文为 draft、未经本地环境实测；本文所列均为文档样板与来源核对，不是部署版本推荐。

## 跨平台比较的阅读方式

与[昇腾路径](ascend.md)、[NVIDIA 路径](nvidia.md)使用相同的领域归属，先明确要比较的任务和环境，再比较具体机制。共同的知识问题包括设备可见性、集合通信进展、数值行为和恢复正确性；三平台的错误码、环境变量、诊断工具与支持边界分别查证，术语与字段名不作直译映射（见[三套通信库能力与版本条件档案](../../knowledge/03-communication/communication-library-profiles.md)与[推理引擎组件与平台功能交集档案](../../knowledge/07-inference/engine-backend-boundaries.md)的对照边界）。

## 任务路径入口

准备阶段：[选型与容量](../tasks/selection-and-capacity.md) · [节点验收](../tasks/node-acceptance.md) · [环境安装](../tasks/environment-installation.md)。运行阶段：[性能优化](../tasks/performance-optimization.md) · [迁移与升级](../tasks/migration-and-upgrade.md) · [故障恢复](../tasks/fault-recovery.md)。排障首要入口：[训练排障](../tasks/training-triage.md) · [推理排障](../tasks/inference-triage.md)。

## 原始资料入口

- [Install AMD ROCm 10.1.0](https://rocm.docs.amd.com/en/docs-10.1.0/install/rocm.html)：安装官方文档（既有登记）。
- [ROCm Core SDK 10.1.0 release notes](https://rocm.docs.amd.com/en/docs-10.1.0/about/release-notes.html)：组件版本总表与 known issues（既有登记）。
- [RCCL documentation](https://rocm.docs.amd.com/projects/rccl/en/docs-6.3.3/index.html)：RCCL 官方文档入口（既有登记）。
- [AMD SMI 27.1.0 文档](https://rocm.docs.amd.com/projects/amdsmi/en/docs-10.1.0/index.html)：AMD SMI/RAS 官方文档（既有登记）。

以上均为已登记来源的入口页；具体能力以所用版本为准，其余领域仍需逐项补齐对应官方来源。

## 逐链检查（T00-08 交付记录，2026-10-22）

本页与同批更新的[昇腾](ascend.md)、[NVIDIA](nvidia.md)、[训练排障](../tasks/training-triage.md)、[推理排障](../tasks/inference-triage.md)五个导航目标共用一次链接/稳定 ID 验收：全部内链经 `make check` 通过，`path.platform.amd` 为新稳定 ID，其余四页保留原 ID；AMD 侧外部引用仅限已登记官方材料，未以未登记主页冒充兼容依据。
