---
id: cluster-platform.idle-resource-job-waiting-triage
title: 空闲设备但作业等待诊断指南
type: procedure
domain: cluster-platform
status: draft
platforms: [generic]
source_refs:
  - src.kueue.admission-v0.19.0
  - src.kubernetes.device-plugins-v1-32
  - src.ascend.mind-cluster-v26.1.1
  - src.volcano.podgroup-gang-v1.15.0
updated_at: "2026-09-30"
summary: 以 Kueue v0.19.0 为主要样板，把“集群有空闲设备但作业不运行”定位到对象接管、配额、准入检查、拓扑指派、kube-scheduler 放置或设备分配中的具体等待层。
related_ids:
  - cluster-platform.admission-and-placement
  - cluster-platform.device-resource-chain
  - reliability.evidence-and-hypotheses
  - hardware.resource-topology
applicability:
  environment_refs: []
  notes: "流程以 Kueue v0.19.0（固定 commit 911a822a）文档与源码为证据样板；其他调度实现（Slurm、Volcano、MindCluster 适配版）只有边界提示，目标环境的调度栈、队列配置与设备插件需先补齐。"
verification:
  status: source_checked
  evidence_refs:
    - src.kueue.admission-v0.19.0
  notes: "已核对 Kueue v0.19.0 固定 commit 的 Workload/ClusterQueue API、troubleshooting 与 pending workloads 文档、scheduler 事件与特性门控源码；未部署调度器、提交作业或修改集群。"
---

# 空闲设备但作业等待诊断指南

## 目标与触发条件

“集群里明明有空闲设备，作业却一直不运行”——本流程把这种症状定位到具体的等待层：作业对象是否被接管、配额是否预留、准入检查是否通过、拓扑指派是否完成、Pod 是否被 kube-scheduler 放置、设备是否真正分配到容器。概念背景见[作业准入、调度与拓扑放置](admission-and-placement.md)；设备分配之后的证据链见[从物理设备到容器资源的状态链](device-resource-chain.md)。

核心原则：**空闲的物理设备不是调度承诺**。配额账本、准入条件、组级约束、拓扑组合和节点碎片都可以在设备空闲时阻止放置。

## 适用范围与前置条件

主要证据样板是 **Kueue v0.19.0**（固定 commit `911a822a49bcfd99c9c62203a009efa4130ad604`）。版本事实先记录：该 commit 的 v1beta1 API 已标记 deprecated，文档示例使用 `kueue.x-k8s.io/v1beta2`，两者条件集合相同；本文引用的 API 行号以 v1beta1 文件为主，正式环境应按实际安装版本的 API 阅读。Slurm、上游 Volcano、MindCluster 适配版调度器的术语和状态不与此等同；不经 Kueue 的作业直接进入步骤 6 的 Pod/设备层检查。

进入排查前至少固定：调度栈与版本、作业提交方式（Job/Pod/其他 CRD）、队列与 ClusterQueue 配置、ResourceFlavor 与拓扑配置、目标节点与设备型号；确认是否有读取集群对象和事件的权限。本文列出的 kubectl/kueuectl 命令均来自固定文档；文档本身不授予执行权限。

## 需要的证据

| 证据 | 采集范围或定位 | 用途 | 缺失时如何处理 |
|---|---|---|---|
| 作业与 Workload 身份 | Job/Pod UID、`kueue.x-k8s.io/job-uid` 标签、对象 generation | 确认作业被哪个控制器接管、对应哪个 Workload | 无 Workload 则不适用 Kueue 分支，转步骤 6 |
| Workload status 与事件 | `status.conditions`、`status.admission`、`status.admissionChecks`、`status.resourceRequests`、Events | 区分配额、准入、拓扑、抢占等等待层 | conditions 为空不能单独反推原因（见步骤 2）；先核对控制器是否已处理该对象 |
| ClusterQueue/LocalQueue status | Active 条件、flavorsUsage/flavorsReservation、pendingWorkloads/admittedWorkloads | 判断队列可用性与配额占用、借入量 | 队列非 Active 时先查队列原因 |
| 节点与拓扑证据 | 节点 Ready/标签、ResourceFlavor、Topology 对象 | 判断放置与拓扑支路 | 标签匹配不等于带宽或健康证据 |
| Pod 与设备分配证据 | Pod 调度事件、Allocate 映射、容器状态 | 准入通过后的下游支路 | 见设备资源链条目 |

## 步骤与判断分支

| 步骤 | 检查或动作 | 运行影响 | 预期证据与解释 | 下一步 |
|---|---|---|---|---|
| 1 | 确认作业被 Kueue 接管：`kubectl describe job` 看 `CreatedWorkload` 事件；或按 `kueue.x-k8s.io/job-uid` 标签查 Workload（[troubleshooting_jobs.md L16–74](https://github.com/kubernetes-sigs/kueue/blob/911a822a49bcfd99c9c62203a009efa4130ad604/site/content/en/docs/tasks/troubleshooting/troubleshooting_jobs.md#L16-L74)） | 只读 | 找到 Workload 对象；找不到说明作业未经 Kueue 或接管失败 | 有 Workload 进入步骤 2；没有则检查控制器部署与作业 label/queue 标注 |
| 2 | 读 Workload conditions：`kubectl describe workload` / `kubectl get workload -o yaml`（[同文档 L123–134](https://github.com/kubernetes-sigs/kueue/blob/911a822a49bcfd99c9c62203a009efa4130ad604/site/content/en/docs/tasks/troubleshooting/troubleshooting_jobs.md#L123-L134)）。典型分支：`QuotaReserved=False, reason=Pending` 且 message 形如 “couldn't assign flavors to pod set …: insufficient quota …”（[L159–178](https://github.com/kubernetes-sigs/kueue/blob/911a822a49bcfd99c9c62203a009efa4130ad604/site/content/en/docs/tasks/troubleshooting/troubleshooting_jobs.md#L159-L178)）→ 配额支路；`reason=Inadmissible`（如 LocalQueue 不存在，[L250–263](https://github.com/kubernetes-sigs/kueue/blob/911a822a49bcfd99c9c62203a009efa4130ad604/site/content/en/docs/tasks/troubleshooting/troubleshooting_jobs.md#L250-L263)）→ 配置支路。**conditions 为空不能单独反推**：来源只说“使用 StrictFIFO、尚未尝试准入的 Workload *可能*没有 condition”（[L243–248](https://github.com/kubernetes-sigs/kueue/blob/911a822a49bcfd99c9c62203a009efa4130ad604/site/content/en/docs/tasks/troubleshooting/troubleshooting_jobs.md#L243-L248)）；空列表不证明控制器已处理该对象，也不证明队列策略是 StrictFIFO。先核对实际 `queueingStrategy`、对象创建时间、控制器是否已接管，并结合步骤 5 的队列位置与队首状态，满足这些证据才把“尚未尝试/队首阻塞”列为候选；只有空列表时保持 `unknown` | 只读 | 等待层被定位到配额/配置/准入，或明确为待补证据 | 分别进入步骤 3、修正配置；空 conditions 按上述补证后再判断 |
| 3 | `QuotaReserved=True` 但 `Admitted=False`：读 `status.admissionChecks[]` 的 state（Pending/Ready/Retry/Rejected）——Admitted 要求配额预留**且**所有准入检查满足（[workload_types.go L628–643](https://github.com/kubernetes-sigs/kueue/blob/911a822a49bcfd99c9c62203a009efa4130ad604/apis/kueue/v1beta1/workload_types.go#L628-L643)；示例 [L218–241](https://github.com/kubernetes-sigs/kueue/blob/911a822a49bcfd99c9c62203a009efa4130ad604/site/content/en/docs/tasks/troubleshooting/troubleshooting_jobs.md#L218-L241)）。挂 Provisioning AdmissionCheck 时：`kubectl describe provisioningrequest` 看 Accepted/Provisioned/Failed/BookingExpired/CapacityRevoked（[troubleshooting_provreq.md L22–118](https://github.com/kubernetes-sigs/kueue/blob/911a822a49bcfd99c9c62203a009efa4130ad604/site/content/en/docs/tasks/troubleshooting/troubleshooting_provreq.md#L22-L118)）；TAS 的配额预留→等准入→拓扑指派三段流程见 [topology_aware_scheduling.md L124–141](https://github.com/kubernetes-sigs/kueue/blob/911a822a49bcfd99c9c62203a009efa4130ad604/site/content/en/docs/concepts/topology_aware_scheduling.md#L124-L141) | 只读 | 等待被定位到具体准入检查或 Provisioning/拓扑指派 | 按准入检查的各自控制器继续；拓扑指派失败看 `SecondPassFailed` 事件与 `status.admission.podSetAssignments[].delayedTopologyRequest` |
| 4 | 配额支路细看：读 ClusterQueue `kubectl get clusterqueue <name> -o yaml`——Active 条件（False 的 reason 如 FlavorNotFound/Stopped/AdmissionCheckNotFound/TopologyNotFound）、`flavorsUsage[].resources[].borrowed`（超出 nominalQuota 的借入量）、pendingWorkloads/admittedWorkloads（[clusterqueue_types.go L268–322](https://github.com/kubernetes-sigs/kueue/blob/911a822a49bcfd99c9c62203a009efa4130ad604/apis/kueue/v1beta1/clusterqueue_types.go#L268-L322)、[L356–366](https://github.com/kubernetes-sigs/kueue/blob/911a822a49bcfd99c9c62203a009efa4130ad604/apis/kueue/v1beta1/clusterqueue_types.go#L356-L366)）。注意 `pendingWorkloadsStatus` 字段自 v0.14.0 废弃，pending 观测改用 VisibilityOnDemand（见步骤 5） | 只读 | 区分“本队列 nominal 已满”“借入被收回”“队列/Flavor 配置错误” | 借入被收回支路：查 cohort 内是否有 reclaim 证据（被收回方 Preempted reason `InCohortReclamation`/`InCohortReclaimWhileBorrowing`）；配置错误则修队列/Flavor |
| 5 | 观察 pending 全貌：`kueuectl list workload --status pending [--clusterqueue X]`（[kueuectl_list_workload.md L19、L131–137](https://github.com/kubernetes-sigs/kueue/blob/911a822a49bcfd99c9c62203a009efa4130ad604/site/content/en/docs/reference/kubectl-kueue/commands/kueuectl_list/kueuectl_list_workload.md#L19)）；或 VisibilityOnDemand API `kubectl get --raw "/apis/visibility.kueue.x-k8s.io/v1beta2/clusterqueues/<cq>/pendingworkloads"` 看 `positionInClusterQueue`/`positionInLocalQueue`（[pending_workloads_on_demand.md L66–109](https://github.com/kubernetes-sigs/kueue/blob/911a822a49bcfd99c9c62203a009efa4130ad604/site/content/en/docs/tasks/manage/monitor_pending_workloads/pending_workloads_on_demand.md#L66-L109)，需集群部署该 APIService） | 只读 | 得到本作业在队列中的位置与同类等待者 | 结合步骤 4 判断是配额不足还是队首效应 |
| 6 | `Admitted=True` 之后：Kueue 对 Job 类工作负载是解除 `spec.suspend`、对直接管理的 Pod 是移除 `kueue.x-k8s.io/admission` scheduling gate（[plain_pods.md L82–85](https://github.com/kubernetes-sigs/kueue/blob/911a822a49bcfd99c9c62203a009efa4130ad604/site/content/en/docs/tasks/run/plain_pods.md#L82-L85)、[troubleshooting_jobs.md L107–121](https://github.com/kubernetes-sigs/kueue/blob/911a822a49bcfd99c9c62203a009efa4130ad604/site/content/en/docs/tasks/troubleshooting/troubleshooting_jobs.md#L107-L121)）；pod-to-node 调度由 kube-scheduler 负责（[overview/_index.md L23](https://github.com/kubernetes-sigs/kueue/blob/911a822a49bcfd99c9c62203a009efa4130ad604/site/content/en/docs/overview/_index.md#L23)）。此后 `kubectl describe pod` 看 `FailedScheduling`；Kueue 只移除自己的 gate，用户自定义 gate 残留时 Pod 仍 gated（[troubleshooting_pods.md L116–120](https://github.com/kubernetes-sigs/kueue/blob/911a822a49bcfd99c9c62203a009efa4130ad604/site/content/en/docs/tasks/troubleshooting/troubleshooting_pods.md#L116-L120)，原文把前缀误写为 `keueu.x-k8s.io`，已按原文核实） | 只读 | 等待层移出 Kueue，进入 kube-scheduler/节点/设备分配支路 | 节点资源碎片与设备分配见[准入与放置](admission-and-placement.md)的“数量足够仍放不下”和[设备资源链](device-resource-chain.md) |
| 7 | 核对“空闲”口径：空闲设备是物理账本；Workload 看到的是 flavor/quota/拓扑账本。单 Pod 需求超过任一节点剩余、可用组合不满足拓扑约束、或 flavor 未覆盖该资源标签时，物理空闲与可放置性分叉 | 只读 | 空闲但不可放置的三个独立原因被区分 | 分别按配额、拓扑、碎片处置；不要凭“有空卡”修改配额或驱逐其他作业 |
| 8 | 汇总事实、推断、反证和未知项 | 无 | 每个结论回链到对象、字段/事件与时间 | 满足完成判据后结束 |

**细分 reason 的可见性边界**：`TopologyPlacementFailed`、`NoMatchingFlavor`、`WaitingForQuota` 等细分 reason 定义于 v1beta2 API（[v1beta2 workload_types.go L928–977](https://github.com/kubernetes-sigs/kueue/blob/911a822a49bcfd99c9c62203a009efa4130ad604/apis/kueue/v1beta2/workload_types.go#L928-L977)），但受 `UnadmittedWorkloadsObservability` 特性门控制，在 v0.19 中为 Beta 且**默认关闭**（[kube_features.go L479–481、L788–790](https://github.com/kubernetes-sigs/kueue/blob/911a822a49bcfd99c9c62203a009efa4130ad604/pkg/features/kube_features.go#L479-L481)）；默认部署下这些原因都回退显示为 `Pending`（[scheduler.go L1072](https://github.com/kubernetes-sigs/kueue/blob/911a822a49bcfd99c9c62203a009efa4130ad604/pkg/scheduler/scheduler.go#L1072)）。因此默认环境不能从 `Pending` 直接区分配额、拓扑或其他细分原因，需要步骤 3–5 的对象级证据。

**其他实现的边界提示**：MindCluster v26.1.1 的调度器是适配修改的 Volcano，芯片亲和性按型号分列且 Atlas 800T A2/900 A2 PoD 不适用前述亲和规则（见[准入与放置](admission-and-placement.md)的 NPU 段）；上游 Volcano 的 gang/`minMember` 语义见同一条目。两者的状态对象与事件模型与 Kueue 不同，本文的 Workload 字段路径不适用于它们。

## 停止条件与恢复安排

- 不为了“让作业跑起来”直接驱逐其他作业、修改配额或删除准入检查；任何配额/队列/拓扑变更需现场授权与回滚计划。
- 发现队列配置错误（如 FlavorNotFound、LocalQueue 不存在）时先修配置对象，不重提作业充数。
- 证据矛盾（对象 generation 混杂、事件时间与日志时间对不上）时停止归因，先固定同一调度尝试的证据。

## 完成判据

以下任一结果可以结束本轮诊断：

1. 等待被定位到具体一层（对象接管/配额/准入检查/拓扑指派/kube-scheduler 放置/设备分配），并有该层对象字段或事件证据；
2. “空闲但不可放置”被拆成配额、拓扑或碎片中的具体原因，且解释与 ClusterQueue/节点证据一致；
3. 处置后 Workload 条件按预期推进（QuotaReserved→Admitted→PodsReady）且应用进程到达初始化——应用层进展另按[集合通信与 rank 进度](../03-communication/collectives-and-rank-progress.md)核对；
4. 证据不足，但已明确记录缺失的对象、权限或版本信息，结论保持 `unknown`。

“作业后来跑起来了”不单独满足完成判据：需要说明它此前停在哪一层、什么条件发生了变化。

## 来源与验证记录

- [Kueue v0.19.0 固定快照](https://github.com/kubernetes-sigs/kueue/tree/911a822a49bcfd99c9c62203a009efa4130ad604)：troubleshooting_jobs/queues/pods/provreq、pending_workloads_on_demand、tasks/run/topology_aware_scheduling 与 plain_pods、concepts/cluster_queue 与 cohort 文档；v1beta1/v1beta2 API 与 scheduler/features 源码。逐条主张与行号见[第八批 Kueue 来源记录](../../docs/research/batch-08-kueue-pending-sources.md)。
- [Kubernetes v1.32 Device Plugins](https://v1-32.docs.kubernetes.io/docs/concepts/extend-kubernetes/compute-storage-net/device-plugins/)、[MindCluster v26.1.1](https://github.com/Ascend/mind-cluster/tree/44385c13d7b1d87def35f1604e8be4d16de6ca4e)、[Volcano v1.15.0 文档](https://volcano.sh/docs/v1.15.0/concepts/podgroup/)：仅作设备分配与其他调度实现的边界引用，未重新核对。
- 当前验证范围：来源核对；未部署 Kueue、提交作业或修改集群。
- 待确认：LocalQueue status 字段细节、Prometheus 指标名（pending_workloads_in_grafana 页未读）、ProvisioningRequest 本体 API（属 kubernetes/autoscaler，未登记）、事件 From 列的具体 source 字符串。
