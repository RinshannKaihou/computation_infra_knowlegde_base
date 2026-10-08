# 第八批来源记录：Kueue 空闲设备但作业等待（R2-03）

研究日期：2026-09-30。目标正文：`knowledge/05-cluster-platform/idle-resource-job-waiting-triage.md`（procedure）。全部证据来自 Kueue 固定 commit `911a822a49bcfd99c9c62203a009efa4130ad604`（v0.19.0，已登记 src.kueue.admission-v0.19.0，根 LICENSE Apache-2.0 已核对）；行号按 raw.githubusercontent.com 原文件逐一核对。未部署或运行任何调度器。本批结论并入该既有登记条目的 notes，不新增来源。

## 主张—证据表

### Workload 条件与状态字段

| 主张 | 证据位置（固定 commit，GitHub blob 基座 `kubernetes-sigs/kueue/blob/911a822a…`） | 证据类型 | 反证/未知 |
|---|---|---|---|
| v1beta1 Workload 条件常量块在 workload_types.go L628–668：Admitted（L629–631）、QuotaReserved（L633–634）、Finished（L636–638）、PodsReady（L640–642）、Evicted（L644–653）、Preempted（L655–660）、Requeued（L662–663）、DeactivationTarget（L665–667） | apis/kueue/v1beta1/workload_types.go#L628-L668 | 源码注释 | 无 |
| Admitted = 配额已预留 **且** 所有 admissionChecks 满足；QuotaReserved 只表示配额预留。「QuotaReserved=True 且 Admitted=False」即准入检查未就绪；文档示例见 troubleshooting_jobs.md L218–241（admissionChecks state: Pending） | 同上 L629–634；site/content/en/docs/tasks/troubleshooting/troubleshooting_jobs.md#L218-L241 | 源码注释 + 文档示例 | 无 |
| PodsReady = 至少 `.spec.podSets[*].count` 个 Pod ready 或已 succeeded；PodsReady=False 的 reason 为 WaitForStart / WaitForRecovery（常量 L750–763） | workload_types.go#L640-L642、#L750-L763 | 源码注释 | 无 |
| Evicted reason：Preempted / PodsReadyTimeout / AdmissionCheck / ClusterQueueStopped / Deactivated（L644–653）；Preempted reason：InClusterQueue / InCohortReclamation / InCohortFairSharing / InCohortReclaimWhileBorrowing（L672–686） | workload_types.go#L644-L653、#L672-L686 | 源码注释 | Evicted 注释列举不完整（另有 LocalQueueStopped L712、NodeFailures L716），引用以常量区为准 |
| 该 commit 中 v1beta1 已标记 deprecated（kubebuilder warning），v1beta2 存在且条件集合相同（v1beta2 workload_types.go L928–1019），文档示例均用 `kueue.x-k8s.io/v1beta2` | v1beta1 文件内标记；apis/kueue/v1beta2/workload_types.go | 源码标记 + 文档 | 引用 v1beta1 行号时须注明 deprecated 状态 |
| Workload status 字段全集：conditions/admission/requeueState/reclaimablePods/admissionChecks/resourceRequests/schedulingStats/unhealthyNodes 等（L355–450）；**该版本不存在 status.clusterAssignment 字段**，准入结果在 status.admission（podSetAssignments 含 flavors/resourceUsage/count/topologyAssignment/delayedTopologyRequest，L154/L174 起） | workload_types.go#L355-L450、#L246-L266 | 源码 | 无 |
| status.resourceRequests 只在未准入 Workload 上有值；admission 非空后转空 | workload_types.go#L404-L411 | 源码注释 | 无 |
| status.admissionChecks[] 元素含 name/state/lastTransitionTime/message/requeueAfterSeconds/retryCount/podSetUpdates；state 枚举 Pending/Ready/Retry/Rejected | workload_types.go#L522-L531 | 源码 | 无 |

### ClusterQueue 状态

| 主张 | 证据位置 | 证据类型 | 反证/未知 |
|---|---|---|---|
| ClusterQueueStatus（L268）：conditions（L276）、flavorsReservation（L283，当前预留）、flavorsUsage（L291，已准入用量）、pendingWorkloads（L296）、reservingWorkloads（L301）、admittedWorkloads（L306）、pendingWorkloadsStatus（L316）、fairSharing（L322） | apis/kueue/v1beta1/clusterqueue_types.go#L268-L322 | 源码注释 | 无 |
| pendingWorkloadsStatus 自 v0.14.0 起废弃，注释建议迁移到 VisibilityOnDemand | clusterqueue_types.go#L308-L316 | 源码注释 | 不再作为观测面 |
| Active 条件（L372）；Active=False 的 reason：Stopped、FlavorNotFound、AdmissionCheckNotFound、AdmissionCheckInactive、TopologyNotFound 等（L27–37），正常为 Ready | clusterqueue_types.go#L27-L37、#L372 | 源码 | 无 |
| FlavorUsage.resources[].total 为含借入的总用量，borrowed 为超出 nominalQuota 的部分 | clusterqueue_types.go#L356-L366 | 源码注释 | 无 |

### 排障文档与命令（该 commit 实际存在并逐条核对原文）

| 主张 | 证据位置 | 证据类型 | 反证/未知 |
|---|---|---|---|
| 定位 Job 对应 Workload：kubectl describe job 看 CreatedWorkload 事件；按 `kueue.x-k8s.io/job-uid` 标签查；`kubectl describe workload` / `kubectl get workload -o yaml` | troubleshooting_jobs.md#L16-L74、#L123-L134 | 文档 | 无 |
| 配额不足等待样例：QuotaReserved=False、reason Pending、message "couldn't assign flavors to pod set main: insufficient quota for cpu in flavor default-flavor in ClusterQueue"，status.resourceRequests 给需求量 | troubleshooting_jobs.md#L159-L178（主任务抽查确认） | 文档示例 | message 为示例措辞，随版本/配置可能不同 |
| StrictFIFO 下未尝试的 Workload 可能没有任何 condition（status.conditions 为空）；**空列表本身不证明控制器已处理该对象，也不能反推队列策略是 StrictFIFO**——需另核 queueingStrategy、对象创建时间与控制器接管状态（Codex 代审 B08-C03 修订点） | troubleshooting_jobs.md#L243-L248 | 文档 | 反向推断不成立时保持 unknown |
| 配置错误态：QuotaReserved=False、reason Inadmissible、message 如 LocalQueue 不存在 | troubleshooting_jobs.md#L250-L263 | 文档示例 | 无 |
| 被抢占后组合：Evicted(True, Preempted) + Admitted(False, NoReservation) + 重新准入失败时新的 QuotaReserved(False, Pending) | troubleshooting_jobs.md#L268-L300 | 文档示例 | 无 |
| 队列侧：kubectl get localqueue/clusterqueue -o yaml；Active=False 示例 reason ClusterQueueIsInactive（LocalQueue）与 FlavorNotFound（ClusterQueue） | troubleshooting_queues.md#L9-L80 | 文档 | 无 |
| VisibilityOnDemand（beta 默认开）：`kubectl get --raw "/apis/visibility.kueue.x-k8s.io/v1beta2/clusterqueues/<cq>/pendingworkloads"` 返回 PendingWorkloadsSummary，含 positionInClusterQueue/positionInLocalQueue，支持 limit/offset | tasks/manage/monitor_pending_workloads/pending_workloads_on_demand.md#L66-L109、#L182-L190、#L306-L312 | 文档 | 需集群部署 visibility APIService |

### 事件、细分 reason 与门控

| 主张 | 证据位置 | 证据类型 | 反证/未知 |
|---|---|---|---|
| 调度器对 Workload 发事件：准入失败 Warning（reason 为 Pending/Inadmissible 等）scheduler.go L1085；TAS 二次调度失败 SecondPassFailed（Warning）L1059；QuotaReserved（Normal）L1103–1108；Admitted（Normal）L1124 | pkg/scheduler/scheduler.go#L1056-L1085、#L1103-L1124 | 源码 | describe 输出 Events 的 From 列具体字符串未核对 |
| 抢占时对被抢占方发 Preempted、对抢占方发 PreemptedWorkload | pkg/scheduler/preemption/preemption.go#L256-L259 | 源码 | 无 |
| 细分等待 reason（TopologyPlacementFailed、NoMatchingFlavor、WaitingForQuota、ExceedsMaxQuota、WaitingForPreemptedWorkloads、Misconfigured、Suspended、PendingEvaluation、WaitingForPodsReady）定义于 **v1beta2** workload_types.go L943–977；写入点 flavorassigner.go L796–835 | apis/kueue/v1beta2/workload_types.go#L928-L977；pkg/scheduler/flavorassigner/flavorassigner.go#L796-L835 | 源码 | **关键限制**：受 UnadmittedWorkloadsObservability 特性门控制，v0.19 中 Beta 但默认关闭（pkg/features/kube_features.go#L479-L481、#L788-L790，Default: false）；默认部署只见回退 reason Pending（scheduler.go L1072）；v1beta1 API 无这些常量 |
| TAS + Provisioning AdmissionCheck 三段流程：配额预留 → 等待所有 AdmissionCheck 报 Ready → 写入 topology assignment；delayedTopologyRequest（Pending/Ready）API 证据 workload_types.go L246–266；二次调度失败发 SecondPassFailed 并重新入队 | concepts/topology_aware_scheduling.md#L124-L141；workload_types.go#L246-L266；scheduler.go#L1056-L1061 | 文档 + 源码 | 无 |
| Provisioning 等待观测：kubectl describe workload 看 status.admissionChecks；ProvReq 命名 `[workload]-[check]-[retry]`；kubectl get/describe provisioningrequest；ProvReq 条件 Accepted/Provisioned/Failed/BookingExpired/CapacityRevoked；失败示例 Failed=True reason OutOfResources | troubleshooting_provreq.md#L22-L118、#L138-L212 | 文档 | ProvisioningRequest 本体属 kubernetes/autoscaler，未登记为来源，仅行内链接 |
| TAS 任务页排障：未准入看 describe workload Events；检查 ResourceFlavor spec.topologyName、Topology 存在性、节点标签（kubectl get nodes --show-labels）；已准入看 status.admission.podSetAssignments[].topologyAssignment | tasks/run/topology_aware_scheduling.md#L190-L215、#L249-L282 | 文档 | 无 |

### Cohort 借用与 Admitted 后交接

| 主张 | 证据位置 | 证据类型 | 反证/未知 |
|---|---|---|---|
| nominalQuota/borrowingLimit/lendingLimit 定义 | concepts/cluster_queue.md#L59-L64 | 文档 | 无 |
| 借用判定：≤ 本队列未用 nominal，或 ≤ cohort 内各 CQ 未用 nominal 之和且 ≤ 本队列 nominal+borrowingLimit；Kueue 在 cohort 内优先调度不需要借用的 Workload | concepts/cluster_queue.md#L222-L250 | 文档 | 无 |
| cohort 级 nominalQuota 是 CQ 配额之上的额外共享池；CQ 必须为目标资源/flavor 定义 nominal（哪怕为 0）才能借用 | concepts/cohort.md#L29-L79 | 文档 | 无 |
| 「借入被收回」证据链：reclaimWithinCohort 允许 pending Workload 抢占 cohort 内用量超过其 nominal 的 Workload（cluster_queue.md L440–452）；被收回方出现 Preempted reason InCohortReclamation/InCohortReclaimWhileBorrowing（v1beta1 L676–686）；借入量可在 CQ status flavorsUsage[].resources[].borrowed 观测（L364–366） | cluster_queue.md#L415-L460；workload_types.go#L676-L686；clusterqueue_types.go#L364-L366 | 文档 + 源码 | 文档没有专门叙述「本队列 nominal 未满但因借入被收回而等待」的排障案例；正文该场景标为归纳而非原文结论 |
| 直接管理 Pod：Kueue 注入 `kueue.x-k8s.io/admission` scheduling gate，准入后 patch 移除，之后交给 kube-scheduler | tasks/run/plain_pods.md#L82-L85 | 文档 | 无 |
| Kueue 只移除自己管理的 gate；自定义 gate 残留时准入后 Pod 仍 gated。troubleshooting_pods.md L116–120 原文把前缀误写为 `keueu.x-k8s.io`（两处，原文拼写错误已核实） | troubleshooting_pods.md#L116-L120 | 文档 | 原文 typo 如实记录；kueue.x-k8s.io/topology gate 另有 TAS ungater 控制器佐证（pkg/controller/tas/topology_ungater.go，未逐行读） |
| Job 类工作负载用 spec.suspend 交接：未准入 suspend=true 不建 Pod，准入后解除悬挂再由 kube-scheduler 调度；Pod 卡住时 kubectl describe pod 看 FailedScheduling | troubleshooting_jobs.md#L107-L121、#L302-L357 | 文档 | 无 |
| 架构边界：pod-to-node 调度是 kube-scheduler 职责，Kueue 不重复实现 | overview/_index.md#L23 | 文档 | 无 |
| kueuectl 文档树完整（reference/kubectl-kueue/）；`kueuectl list workload [--clusterqueue X] [--localqueue Y] [--status all/pending/admitted/finished]` | reference/kubectl-kueue/commands/kueuectl_list/kueuectl_list_workload.md#L19、#L131-L137 | 文档 | 其他子命令页未逐页展开 |

## 未解决与抓取失败

- 无抓取失败；git trees API 返回 truncated=false，文件树完整。
- 未读：troubleshooting_agent_skills.md、troubleshooting_delete_clusterqueue.md、pending_workloads_in_grafana.md（Prometheus 指标名未核对）、kueuectl 其他子命令页。
- labels-and-annotations 参考页在该 commit 是 9 行 Hugo 短代码桩，标签正文由站点数据生成，无法按行引用。
- LocalQueue status 字段、unhealthyNodes 源码路径未逐行核对。
