---
id: cluster-platform.index
title: 05 集群平台与资源管理
type: index
domain: cluster-platform
status: draft
platforms:
- generic
source_refs:
- src.ascend.mind-cluster
- src.ascend.agent-skills
- src.infrasys.aiinfra
updated_at: '2026-10-18'
summary: 组织容器、设备资源管理、调度、多租户和集群变更。
related_ids:
- cluster-platform.device-resource-chain
- hardware.resource-topology
- hardware.index
- software-stack.index
- training.index
- inference.index
- reliability.index
- cluster-platform.admission-and-placement
- cluster-platform.ascend-device-visibility-triage
- cluster-platform.ascend-device-visibility-source-case
- cluster-platform.ascend-device-visibility-experiment
- cluster-platform.idle-resource-job-waiting-triage
- cluster-platform.accelerator-sharing-and-isolation
- cluster-platform.contention-capacity-validation
- cluster-platform.node-drain-resource-reclamation
- cluster-platform.platform-change-and-rollback
- cluster-platform.control-plane-recovery
---

# 05 集群平台与资源管理

本页是内容导航草稿。已建设的正文见下方入口，其余二级主题仍待补充；正文均为草稿，未经本地环境实测。`generic` 表示跨平台导航，不表示所有环境兼容。

## 已有正文

[从物理设备到容器资源的状态链](device-resource-chain.md)：区分物理存在、驱动可见、插件上报、调度分配、容器访问和框架可用，记录各阶段的证据边界；含 NVIDIA k8s-device-plugin v0.20.1 与 Slurm 24.11.7 GRES/TRES 两个固定实现的独立发现/分配/健康/回收视图（T05-04 修订，claude-opus-5-5 审阅已闭环，未做真实环境验证）。

[作业准入、调度与拓扑放置](admission-and-placement.md)：区分队列配额、准入、组级约束、节点放置与设备分配，保留 NPU 型号差异。

[空闲设备但作业等待诊断指南](idle-resource-job-waiting-triage.md)：以 Kueue v0.19.0 为样板，把“有空闲设备但作业不运行”定位到接管、配额、准入、拓扑、放置或设备分配的具体等待层。

[Kubernetes 作业全生命周期与控制器责任](kubernetes-job-lifecycle.md)：以 Kubernetes v1.32 与 Kueue v0.19.0 为样板，解释提交、准入、运行、退出、重试、取消和资源清理（T05-02，claude-opus-5-5 审阅已闭环，未做真实环境验证）。

[Slurm 作业生命周期、设备资源与状态参考](slurm-jobs-and-device-resources.md)：固定 Slurm 24.11.7 归档，查询 Job/Step、GRES/TRES、分区/QOS/优先级/预留、cgroup 与状态（T05-03，claude-opus-5-5 审阅已闭环，未做真实环境验证）。

[加速器共享与租户隔离机制](accelerator-sharing-and-isolation.md)：区分租户、容器、设备、显存、算力与故障域边界，比较整卡独占、MIG、MPS 与 time slicing 的隔离和支持条件；Ascend 虚拟设备分支保留未证实（T05-06 gpt-6.1-sol/xhigh 审阅已闭环的 draft，未做真实环境验证）。

[多租户争用、公平性与容量验证](contention-capacity-validation.md)：把设备与主机/网络/存储争用关联到容量记录、Kueue/Slurm 公平性口径和两租户对照设计（T05-07 gpt-6.1-sol/xhigh 审阅已闭环的 draft，未执行）。

[节点摘除、drain 与资源回收流程](node-drain-resource-reclamation.md)：分别组织 Kubernetes cordon/drain/删除与 Slurm DRAIN/DOWN/RESUME，按负载类型说明停止准入、Checkpoint、卷/设备清理与重新准入（T05-08 gpt-6.1-sol/xhigh 审阅已闭环的 draft，未执行）。

[平台组件升级、发布、回退与回服](platform-change-and-rollback.md)：以 Kubernetes/Slurm 与 NVIDIA/Ascend 有限版本样板，规划预检、波次、观测、失败停发、回退与回服门槛，明确不可直接回退边界（T05-09 gpt-6.1-sol/xhigh 审阅已闭环的 draft，未执行）。

[控制面故障、平台恢复与账本核对](control-plane-recovery.md)：区分 Kubernetes API/etcd/控制器与 Slurm slurmctld/slurmd/slurmdbd 的故障分支，给出只读证据入口、etcd/StateSaveLocation 备份恢复前提、停止门槛与恢复后账本/作业进展核验清单（T05-10，Batch 24，gpt-6.1-sol/xhigh 审阅已闭环的 draft，未执行任何恢复操作）。

## 本章范围

覆盖设备如何被平台发现、分配给任务、上报健康状态，以及作业如何被调度、运行和恢复。连接物理资源、平台资源对象与工作负载。

## 场景指南、案例与实验

以下均为来源整理草稿；公开案例不代表本库复现，实验仅为设计。

| 主题 | 诊断指南 | 来源案例 | 实验设计 |
|---|---|---|---|
| 容器内 NPU 可见性 | [指南](ascend-device-visibility-triage.md) | [案例](ascend-device-visibility-source-case.md) | [实验设计](ascend-device-visibility-experiment.md) |


## 二级主题地图

- **05.1 容器、镜像、设备暴露与运行环境** — 已有[设备访问条件的概念草稿](device-resource-chain.md)，新增[镜像运行时基线](container-image-runtime-baseline.md)（T05-01 草稿，gpt-6.1-sol/xhigh 审阅已闭环，未做真实环境验证）；部署与实测待补充。
- **05.2 Kubernetes、Slurm 等平台与作业生命周期** — 已有[Kueue/Volcano 状态边界](admission-and-placement.md)，新增[Kubernetes 作业生命周期](kubernetes-job-lifecycle.md)与[Slurm 状态参考](slurm-jobs-and-device-resources.md)（T05-02/T05-03，审阅已闭环，仍为 draft 且未做真实环境验证）；T05-08 已交付[节点摘除与回收流程](node-drain-resource-reclamation.md)（gpt-6.1-sol/xhigh 审阅已闭环的 draft，未执行），T05-10 已交付[控制面故障与恢复](control-plane-recovery.md)（gpt-6.1-sol/xhigh 审阅已闭环的 draft），05.2 主题验收已随 Batch 24 置 accepted。
- **05.3 设备发现、分配、健康上报与资源账本** — 已有[设备资源状态链](device-resource-chain.md)（T05-04 修订后含 GPU/Slurm 独立账本视图与三实现对照，审阅已闭环），已有容器内 NPU 可见性指南、公开案例和实验设计；现场验证待补充。
- **05.4 配额、排队、gang、放置与拓扑亲和性** — 已有[准入与放置概念](admission-and-placement.md)和[空闲设备但作业等待诊断指南](idle-resource-job-waiting-triage.md)；新增[多租户争用、公平性与容量验证](contention-capacity-validation.md)（T05-07 gpt-6.1-sol/xhigh 审阅已闭环的 draft，未执行）；现场配置与验证待补充。
- **05.5 多租户、隔离、资源争用与容量管理** — 新增[加速器共享与租户隔离机制](accelerator-sharing-and-isolation.md)（T05-06）与[多租户争用、公平性与容量验证](contention-capacity-validation.md)（T05-07），均为 gpt-6.1-sol/xhigh 审阅已闭环的 draft；Ascend vNPU 的共享规格与分配约束已交付，跨 vNPU 故障隔离/QoS 保留未证实。
- **05.6 节点上下线、升级、发布与变更** — 新增[节点摘除、drain 与资源回收流程](node-drain-resource-reclamation.md)（T05-08）与[平台组件升级、发布、回退与回服](platform-change-and-rollback.md)（T05-09），均为 gpt-6.1-sol/xhigh 审阅已闭环的 draft，未做真实演练。
- **05.7 调度失败、控制面异常与集群恢复** — 新增[控制面故障、平台恢复与账本核对](control-plane-recovery.md)（T05-10 gpt-6.1-sol/xhigh 审阅已闭环的 draft，未执行任何恢复操作）；节点级回收与变更边界见 05.6 两篇。

## 内容边界

- 设备暴露、平台分配和容器配置归本章；驱动是否初始化及运行时配套归 02。
- 调度和放置策略归本章；并行策略的训练语义归 06，服务流量策略归 07。
- 节点回到可调度状态与任务恢复正确是不同判断；后者链接到工作负载章节。

## NPU 内容位置

Device Plugin、NPU Exporter、容器设备可见性和 MindCluster 的平台能力在本章定位；通过版本和部署方式区分具体实现。

完整路径见[昇腾专题](../../paths/platforms/ascend.md)。其他平台入口见 [NVIDIA 专题](../../paths/platforms/nvidia.md)。

## 关联章节

- [01 物理设施与计算节点](../01-hardware/index.md)
- [02 系统软件与加速器执行栈](../02-software-stack/index.md)
- [06 训练与后训练系统](../06-training/index.md)
- [07 推理与服务系统](../07-inference/index.md)
- [08 可靠性与计算正确性方法](../08-reliability/index.md)

## 已收集的原始资料入口

以下链接指向厂商或项目自己的资料；引用或改编前仍需核对对应版本、来源许可和适用范围。

- [MindCluster 官方仓库](https://github.com/Ascend/mind-cluster)：集群组件、设备管理和调度资料入口。
- [Ascend Agent Skills](https://github.com/Ascend/agent-skills)：设备与容器环境相关任务的组织参考。
- [AIInfra 项目仓库](https://github.com/Infrasys-AI/AIInfra)：云原生平台与资源管理的背景资料。

## 首轮成果与后续

已有设备状态链、准入放置、Kubernetes/Slurm 作业生命周期、加速器共享与租户隔离、争用与容量验证、节点摘除与平台变更回退、控制面故障与恢复，以及容器内 NPU 可见性指南、案例和实验设计；后续补调度失败专题的现场验证与 V11 类演练。
