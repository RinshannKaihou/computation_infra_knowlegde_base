---
id: cluster-platform.kubernetes-job-lifecycle
title: Kubernetes 作业全生命周期与控制器责任
type: concept
domain: cluster-platform
status: draft
platforms: [generic]
source_refs:
- src.kubernetes.job-lifecycle-v1-32
- src.kubernetes.api-gc-v1-32
- src.kueue.job-lifecycle-v0.19.0
- src.kueue.admission-v0.19.0
- src.kubernetes.job-controller-tests-v1.32.0
- src.kubernetes.device-plugins-v1-32
updated_at: "2026-10-14"
summary: 以 Kubernetes v1.32 Job/Pod 与 Kueue v0.19.0 Workload 为固定样板，解释提交、准入、运行、退出、重试、取消和资源清理的责任与状态边界；训练恢复状态仍归应用。
related_ids:
- cluster-platform.admission-and-placement
- cluster-platform.device-resource-chain
- cluster-platform.idle-resource-job-waiting-triage
verification:
  status: source_checked
  evidence_refs:
  - src.kubernetes.job-lifecycle-v1-32
  - src.kubernetes.api-gc-v1-32
  - src.kueue.job-lifecycle-v0.19.0
  - src.kueue.admission-v0.19.0
  - src.kubernetes.job-controller-tests-v1.32.0
  notes: "经 webfetch 只读核对 v1.32 版本化文档（Job、Pod 生命周期、TTL-after-finished、finalizers、owners-dependents、Job v1 API、ObjectMeta/GC）与 Kueue v0.19.0 固定 commit（Job 集成、两阶段准入、AdmissionCheck、stopPolicy、排障页、v1beta2 类型、账本字段、测试函数行号）；复用 src.kueue.admission-v0.19.0（准入两阶段/类型原文）与 src.kubernetes.device-plugins-v1-32（设备侧入口，细节见 device-resource-chain.md）；curl 字节级取回未执行，未部署集群、未提交 Job。"
---

# Kubernetes 作业全生命周期与控制器责任

> 范围：Kubernetes v1.32 版本化文档与 Kueue v0.19.0（commit `911a822a`）固定样板。`generic` 仅为概念组织，不表示任意版本、发行版或调度器组合受支持；Kueue 与 Volcano/MindCluster 是否可共同部署未知。

## 定义与要解决的问题

“作业已提交”之后，对象要依次经过 API 接收、队列与配额核算、准入检查、节点放置、设备分配与容器启动、进程初始化与持续进展。每一跳由不同控制器负责，也留下不同证据。本页回答：一个 Kubernetes Job 从创建到清理，**谁在每一步做决策、留下什么状态、卡住时先看哪一层**。

关键区分有三组：Job（用户作业意图）≠ Workload（Kueue 准入单元，Kueue 不直接操作 Job）；Pod 阶段（kubelet 视角）≠ Job 状态（job-controller 视角）≠ Workload 条件（Kueue 视角）；`Running`/`Ready`（容器视角）≠ 应用持续进展（业务视角）。

## 机制与关键关系

### Job 控制器：完成计数与重试

Job 用“成功完成数”定义结束。`spec.completions` 为要达成的成功数，`spec.parallelism` 为期望并行度；两者都不设时各默认为 1。三种形态（[Job 页](https://v1-32.docs.kubernetes.io/docs/concepts/workloads/controllers/job/)）：非并行（各 1）、固定完成数（`completions` 非零）、工作队列（不设 `completions`，靠 Pod 或外部服务协调，任一 Pod 成功后不再建新 Pod）。

失败处理分两层。容器层由 Pod 的 `restartPolicy`（Job 只允许 `Never`/`OnFailure`）决定本机重跑；作业层由 `backoffLimit`（默认 6，指数退避 10s/20s/40s…封顶 6 分钟）决定重建 Pod 上限。计数口径有两种：`Failed` phase 的 Pod 数，以及 `OnFailure` 时 Pending/Running Pod 内各容器的重试数，任一达到上限即判失败。`OnFailure` 下达到退避上限时运行中的 Pod 会被终止，调试困难时建议用 `Never` 或日志系统（同页“Pod backoff failure policy”）。

定向失败策略用 `podFailurePolicy`（v1.31 稳定）：按容器退出码与 Pod 条件（`DisruptionTarget` 表中断）匹配规则，动作 `FailJob`/`Ignore`/`Count`/`FailIndex`，要求 `restartPolicy: Never`，只匹配 `Failed` phase。Indexed Job 可再配 `backoffLimitPerIndex`/`maxFailedIndexes`（`failedIndexes`/`completedIndexes` 以 `1,3-5,7` 区间格式记录）与 `successPolicy`（v1.31 beta，按索引子集或成功数提前判成功）。

`activeDeadlineSeconds` 到期杀死运行 Pod 并置 `Failed/DeadlineExceeded`，优先级高于 `backoffLimit`。替换时机由 `podReplacementPolicy` 控制（v1.29 beta，门控默认开）：`TerminatingOrFailed`（默认，未设 podFailurePolicy 时，`creates replacement Pods immediately upon Pod deletion`）/`Failed`（等 Pod 进入终态再建；设了 podFailurePolicy 时默认且只能为该值）；v1.28 起用 podFailurePolicy 时控制器 `recreates terminating Pods only once these Pods reach the terminal Failed phase`。默认策略下终止中即建替换，运行 Pod 数可超 parallelism、Indexed Job 同一 index 可多于一个 Pod（Job 页原文）。本库推论：分布式训练同 rank 两进程并存、资源双占，影响进程视图与账本。`spec.suspend` 翻转删除非 Completed Pod（SIGTERM 优雅期），`status.startTime` 重置，deadline 随之重置；同时有 `Suspended` 条件与 `Suspended/Resumed/Completed` 事件。`spec.managedBy` 不可变，外部控制器不得复用 Job 的 tracking finalizer。

Pod 带 `batch.kubernetes.io/job-tracking` finalizer：只有计入 Job 状态后才摘除（`removes the finalizer only after the Pod has been accounted for`）。v1.31 起 Job 控制器推迟 terminal 条件：`delays the addition of the terminal conditions, Failed or Complete, until all of the Job Pods are terminated`（受 JobManagedBy 与 JobPodReplacementPolicy 门控，均默认开）；此时 Pod 已达 terminal phase，`status.terminating` 应为 0。**`Complete`/`Failed` 出现后仍能看到 Pod 对象属正常保留**（`the Pods are usually not deleted either`，看日志用），按 TTL 或删除策略清理；`FailureTarget`/`SuccessCriteriaMet` 才是更早的信号。v1.30 及以前或门控关闭时行为不同。

### Pod 生命周期：阶段、条件与探针

Pod 阶段只有五个（[Pod 生命周期页](https://v1-32.docs.kubernetes.io/docs/concepts/workloads/pods/pod-lifecycle/)）：`Pending`（原文仅含等待调度与下载镜像）、`Running`（已绑定节点，至少一容器运行或启动中）、`Succeeded`、`Failed`、`Unknown`（与节点失联）。phase 不是完备状态机（`not intended to be a comprehensive rollup/state machine`），`kubectl` 的 STATUS 列不等于 phase。沙箱联网属于 `PodReadyToStartContainers` 条件（kubelet 在沙箱创建且网络配好后置），`Initialized`/`ContainersReady`/`Ready` 另列。

`Ready` 由 conditions 决定：容器全 Ready 且 `readinessGates` 全 True（缺失的门默认为 False）。`liveness` 失败按 `restartPolicy` 重启，`readiness` 失败摘除 endpoints（删除时自动 unready），`startup` 期间屏蔽其余探针。**Ready ≠ Running ≠ 应用持续进展**：探针只证容器与门的状态，不证训练 step 或请求进度。

Pod 级 `restartPolicy`（`Always` 默认/`OnFailure`/`Never`）由 kubelet 在同节点内指数退避执行（10s 起，封顶 300s，正常运行 10 分钟重置）。节点失联时 Pod 处置按 Kueue failure recovery 口径（[setup_failure_recovery L9–33、L177–181](https://github.com/kubernetes-sigs/kueue/blob/911a822a49bcfd99c9c62203a009efa4130ad604/site/content/en/docs/tasks/manage/setup_failure_recovery.md)）：`node.kubernetes.io/unreachable` 默认容忍 5 分钟后 Pod 被标记终止；无 failure recovery 时 Pod 长时间停在 Terminating（此时 `podReplacementPolicy: Failed` 的 Job 无法推进）；`FailureRecoveryPolicy`（Kueue v0.15+ 可选，需开门控且 Pod 带 `kueue.x-k8s.io/safe-to-forcefully-delete` 注解）60 秒后强制置 Failed（重调度前须确认无数据损坏，见该页警告）。1.27 起 kubelet 把已删 Pod 先转 terminal 再从 API 删除。

### 完成清理：TTL、finalizer 与属主

自动清理只支持 Job：`spec.ttlSecondsAfterFinished` 从 `Complete`/`Failed` 条件出现起计时，到期级联删除，过期后再延长不保证保留，时钟 skew 可致误删或晚删（[TTL 页](https://v1-32.docs.kubernetes.io/docs/concepts/workloads/controllers/ttlafterfinished/)，v1.23 stable）。

删除语义（[finalizers 页](https://v1-32.docs.kubernetes.io/docs/concepts/overview/working-with-objects/finalizers/)）：带 finalizer 的 DELETE 只写 `deletionTimestamp` 并返回 202，`metadata.finalizers` 清空才真正删除；删除中禁加 finalizer。卡删时勿手摘 finalizer，先查原因（如 `pv-protection` 例）。Kueue 侧：已准入 Workload 带 `kueue.x-k8s.io/resource-in-use` finalizer（删 Job 后移除，见集成测试 `Its workload finalizer should be removed`），ClusterQueue 同名 finalizer 在资源释放前阻止其删除；Workload 对象 Kueue 默认不主动删除（`leaves all Workload objects in cluster indefinitely`，主语是 Kueue；被 GC 级联删除的情形见核对方法第 2 步取消分支），可选 `objectRetentionPolicies.workloads.afterFinished`/`afterDeactivatedByKueue` 回收（[retention](https://github.com/kubernetes-sigs/kueue/blob/911a822a49bcfd99c9c62203a009efa4130ad604/site/content/en/docs/tasks/manage/setup_object_retention_policy.md)）（去活 Workload 回收可级联删 Job，见 retention 场景 B 及 Notes）。

属主关系（[owners 页](https://v1-32.docs.kubernetes.io/docs/concepts/overview/working-with-objects/owners-dependents/)、[GC 页](https://v1-32.docs.kubernetes.io/docs/concepts/architecture/garbage-collection/)，见 src.kubernetes.api-gc-v1-32）：`metadata.ownerReferences` 记属主名与 UID（Job/CronJob 自动设置）；跨 namespace 引用按设计不允许，命名空间级依赖可指向集群级或命名空间级 owner；`OwnerRefInvalidNamespace` 用于无效跨 namespace 引用或集群级依赖引用命名空间级 kind。foreground 删除：owner 进删除中后控制器删除其已知依赖对象，只有 `blockOwnerDeletion=true` 且在 GC 缓存中的依赖会阻塞 owner 删除；orphan 删除加 `orphan` finalizer。

Job v1 API（[Job 参考](https://v1-32.docs.kubernetes.io/docs/reference/kubernetes-api/workload-resources/job-v1/)）的状态字段：`active`（非 terminating 的 pending+running）、`ready`（Ready 且非 terminating）、单调增的 `succeeded`/`failed`（弹性缩容时 succeeded 可降）、`completedIndexes`/`failedIndexes`、`conditions`（`Complete` 与 `Failed` 互斥）、`uncountedTerminatedPods`（三步：Pod UID 入数组→摘 Pod finalizer→移出数组并增对应计数）、`terminating`（Pending/Running 且带 deletionTimestamp 的 Pod，beta，受 JobPodReplacementPolicy 门控）。

### Kueue：两阶段准入与 Workload 状态

Kueue 不直接操作 Job，而是为带 `kueue.x-k8s.io/queue-name` label 的 Job 创建对应的 Workload 作为准入单元（[Job 集成页](https://github.com/kubernetes-sigs/kueue/blob/911a822a49bcfd99c9c62203a009efa4130ad604/site/content/en/docs/tasks/run/jobs.md)），`does not directly manipulate Job objects … syncs the decisions and statuses`。Workload 名称格式为 `<api-name>-<job-name>-<hash>`（如事件 `Created Workload: my-namespace/job-my-job-19797`），用 `CreatedWorkload` 事件或 `kueue.x-k8s.io/job-uid` label 反查（`GetWorkloadNameForJob(jobName, jobUID)`），按 Job 名直接查 Workload 会找不到；Job 集成页个别示例写 `with a matching name`（`sample-job-sl4bm`），与排障页和控制器代码不一致，以后者为准。不必手动建 suspend 状态的 Job（原文 `you do not need to create the Job in a suspended state`），suspend 由 webhook 代管；每 Pod 须写 requests（只写 limits 时按 requests 折算）。

准入分两阶段（[workload 页](https://github.com/kubernetes-sigs/kueue/blob/911a822a49bcfd99c9c62203a009efa4130ad604/site/content/en/docs/concepts/workload.md)与 [admission 页](https://github.com/kubernetes-sigs/kueue/blob/911a822a49bcfd99c9c62203a009efa4130ad604/site/content/en/docs/concepts/admission.md)，同 commit）：先 `QuotaReserved`（配额预留，配额 = Σ(requests×count)，经 LimitRange 默认值、runtime overhead 调整），再等 AdmissionChecks 全 Ready 才 `Admitted`（两阶段见 admission 页 L17–24）。临时失败释放配额重排；`retryStrategy` 是 ProvisioningRequestConfig 的字段（`Kueue creates new ProvisioningRequest with -attempt<N> suffix each retry`），`-attempt<N>` 是 ProvisioningRequest 名后缀（仅配了 ProvisioningRequest AdmissionCheck 时出现），不是 Workload/Job 的 attempt。永久失败记 `Rejected`。驱逐与去活按原因区分：AdmissionCheck `Retry` 驱逐释配额但不去活，只有 `Rejected` 才 `spec.active=false` 去活；抢占后重排继续准入；`spec.active=false`、重排超限、`maximumExecutionTimeSeconds` 超时去活。一个 Job 可对应多 Workload（ElasticJob 扩容建新 Workload、Concurrent Admission 有 Parent＋多 Variant），对齐默认一对多，按 job-uid 反查可能返回多个对象。

`stopPolicy` 是 ClusterQueue/LocalQueue 的字段（非 Job 字段，[v1beta2 `clusterqueue_types.go` L132–144](https://github.com/kubernetes-sigs/kueue/blob/911a822a49bcfd99c9c62203a009efa4130ad604/apis/kueue/v1beta2/clusterqueue_types.go)），只有 `None`（正常准入）、`Hold`（已准入负载运行到完（`Admitted workloads will run to completion`），仅 Reserving 负载取消预留）、`HoldAndDrain`（已 admit 的也驱逐）三值；非 `None` 即 Inactive。Workload 条件本文用到的子集（v1beta2 [`workload_types.go`](https://github.com/kubernetes-sigs/kueue/blob/911a822a49bcfd99c9c62203a009efa4130ad604/apis/kueue/v1beta2/workload_types.go)，v1beta1 已弃用）：`Admitted`/`QuotaReserved`/`Finished`/`PodsReady`/`Evicted`/`Preempted`/`Requeued`/`DeactivationTarget`，reason 含 `Preempted`/`PodsReadyTimeout`/`AdmissionCheck`/`ClusterQueueStopped`/`MaximumExecutionTimeExceeded`/`Succeeded`/`Failed` 等。细分等待 reason（`WaitingForQuota` 等）只在开启 `UnadmittedWorkloadsObservability`（v0.19 Beta，默认关，[`kube_features.go` L479–481、L788–789](https://github.com/kubernetes-sigs/kueue/blob/911a822a49bcfd99c9c62203a009efa4130ad604/pkg/features/kube_features.go)；[`workload.go` L1568–1575](https://github.com/kubernetes-sigs/kueue/blob/911a822a49bcfd99c9c62203a009efa4130ad604/pkg/workload/workload.go) 门控关闭返回回退值）后出现，默认只见回退 reason，不能作为默认环境的排查证据。`Finished` 只表示 Job Complete/Failed，不表示训练结果正确。条件与 reason 以 v1beta2 为准（[`workload_types.go`](https://github.com/kubernetes-sigs/kueue/blob/911a822a49bcfd99c9c62203a009efa4130ad604/apis/kueue/v1beta2/workload_types.go)，`storageversion`；v1beta1 已弃用 `Use v1beta2 instead`）：新增 `BlockedOnPreemptionGates`、`WaitingForReplacementPods`，QuotaReserved/Admitted 细分 reason（`WaitingForQuota`/`Misconfigured`/`Suspended`/`NoReservation`/`UnsatisfiedAdmissionChecks` 等）；另有 `Deactivated`、`LocalQueueStopped`、`RequeuingLimitExceeded`、`OwnerNotFound`。

身份/代次对照（无统一计数器，逐项列来源）：Job/Pod/Workload UID（`metadata.uid`，[ObjectMeta 页](https://v1-32.docs.kubernetes.io/docs/reference/kubernetes-api/common-definitions/object-meta/)；Workload 用 job-uid 反查，[排障页](https://github.com/kubernetes-sigs/kueue/blob/911a822a49bcfd99c9c62203a009efa4130ad604/site/content/en/docs/tasks/troubleshooting/troubleshooting_jobs.md)）；`metadata.generation`（spec 修订序号，系统填充只读，非重试次数，ObjectMeta 页同上）；Pod 替换产生新 Pod（新名新 UID；新 UID 以 ObjectMeta 页 uid 定义为准，Job 页替换节只写建 replacement Pods）；容器重启数（[Pod 生命周期页](https://v1-32.docs.kubernetes.io/docs/concepts/workloads/pods/pod-lifecycle/) RESTARTS 列）；Job `status.failed`/`failedIndexes`（[Job v1 API](https://v1-32.docs.kubernetes.io/docs/reference/kubernetes-api/workload-resources/job-v1/)）；Workload `status.requeueState.count`（[workload 页 L147–163](https://github.com/kubernetes-sigs/kueue/blob/911a822a49bcfd99c9c62203a009efa4130ad604/site/content/en/docs/concepts/workload.md)，达 `backoffLimitCount` 后去活见 setup_wait_for_pods_ready L107–110）；ProvisioningRequest `-attempt<N>`（[admission 页 L28–32](https://github.com/kubernetes-sigs/kueue/blob/911a822a49bcfd99c9c62203a009efa4130ad604/site/content/en/docs/concepts/admission.md)）；ElasticJob 多 Workload（[jobs.md L222–240](https://github.com/kubernetes-sigs/kueue/blob/911a822a49bcfd99c9c62203a009efa4130ad604/site/content/en/docs/tasks/run/jobs.md)）/Concurrent Admission 多 Variant（workload 页 L23–27，Alpha 默认关）。

`spec.active=false` 驱逐运行中的负载；`maximumExecutionTimeSeconds` 从 Admitted 起累计，超时去活并清零；`requeueState{count,requeueAt}` 记录 PodsReadyTimeout 退避。`PartialAdmission`（v0.5 Beta，默认开，[`kube_features.go` L545–547](https://github.com/kubernetes-sigs/kueue/blob/911a822a49bcfd99c9c62203a009efa4130ad604/pkg/features/kube_features.go)）注解只降 parallelism 不改 completions；`ElasticJob`（代码 v0.18 Beta 默认开（[`kube_features.go` L601–603](https://github.com/kubernetes-sigs/kueue/blob/911a822a49bcfd99c9c62203a009efa4130ad604/pkg/features/kube_features.go)），仍需逐 Job 加 `kueue.x-k8s.io/elastic-job: "true"` 注解；jobs.md 页头仍标 v0.13 alpha，文档滞后于代码）扩容建新 Workload、旧标 Finished，缩容不建新 Workload；Concurrent Admission（v0.18 Alpha，默认关（[`kube_features.go` L757–758](https://github.com/kubernetes-sigs/kueue/blob/911a822a49bcfd99c9c62203a009efa4130ad604/pkg/features/kube_features.go)），需在 ClusterQueue 上启用）下有 Parent＋多 Variant Workload。

### 官方测试入口

Kubernetes `v1.32.0` tag 下 [`pkg/controller/job`](https://github.com/kubernetes/kubernetes/tree/v1.32.0/pkg/controller/job)（含 `job_controller.go`、`backoff_utils.go`、`pod_failure_policy.go`、`success_policy.go`、`tracking_utils.go` 及各自单测）与 [`test/integration/job/job_test.go`](https://github.com/kubernetes/kubernetes/blob/v1.32.0/test/integration/job/job_test.go)（4620 行）：`TestJobPodFailurePolicy` L260、`TestDelayTerminalPhaseCondition` L1236（测试 finalizer 阻塞 Pod 删除，终态条件延迟）、`TestBackoffLimitPerIndex` L1623、`TestJobPodReplacementPolicy` L2889、`TestJobPodReplacementPolicyFeatureToggling` L3154、`TestOrphanPodsFinalizersClearedWithGC` L3594、`TestJobPodsCreatedWithExponentialBackoff` L3686、`TestJobFailedWithInterrupts` L3776、`TestSuspendJob` L3884。Kueue 同 commit [`job_controller_test.go`](https://github.com/kubernetes-sigs/kueue/blob/911a822a49bcfd99c9c62203a009efa4130ad604/test/integration/singlecluster/controller/jobs/job/job_controller_test.go)（5523 行）：`Its workload finalizer should be removed` L2365、`Should allow reclaim of resources that are no longer needed` L2416（运行期部分释放 Dynamic Reclaim 样本，非取消）、`Should not readmit a job to the queue after Active is changed to false` L2707、PodsReady 重排 L3388、ObjectRetentionPolicies 组 L3916（含 `DeletePropagationOrphan` L4042）、无配额泄漏 L5306。以上为上游行为样本，不是现场验证，不复制代码。

## 控制面 / 节点 / 进程视图对齐表

下表为本库组装的观察模型（无现成官方表），行内证据来自三处不同组件，时间戳与对象身份须先对齐才能比较。

| 视图 | 观察位置 | 关键证据 | 尚不能推出 |
|---|---|---|---|
| 控制面（API/控制器） | Job 对象、Workload、事件 | Job `status`（active/ready/succeeded/failed、conditions）、`batch.kubernetes.io/job-name` 选择器列 Pod；Workload `Admitted/QuotaReserved/Finished/Evicted`；事件集合（无序列举：`Suspended`、`CreatedWorkload`、`SuccessfulCreate`、`Started`、`Resumed`、`Completed`；列出顺序≠发生顺序，jobs.md L201–202） | Pod 已在节点运行；应用已就绪或持续进展 |
| 节点（kubelet/运行时） | Pod phase、conditions、容器状态 | Pod phase、`PodScheduled`/`PodReadyToStartContainers`/`Initialized`/`ContainersReady`/`Ready` 条件、容器状态与重启计数 | Job 完成计数已更新；配额已释放；训练状态已保存 |
| 控制面（调度/扩缩） | 调度与扩缩事件 | `FailedScheduling`（`default-scheduler`）、`NotTriggerScaleUp`（`cluster-autoscaler`） | 节点已实际放置 Pod；应用已就绪 |
| 进程（应用） | 训练/服务进程日志与检查点 | step/request 进度、checkpoint 写入完成、通信组成员 | 平台资源账本已刷新；其他副本同样正常 |

对齐键：`Job.metadata.uid` —label `kueue.x-k8s.io/job-uid`— Workload 反查（一对多时返回多个）；`batch.kubernetes.io/controller-uid` 选择器列 Job 的 Pod；`batch.kubernetes.io/job-completion-index` 对 Indexed Job 的索引。不同 generation/attempt 的历史事件与当前状态可能属于不同对象，先按 UID 与时间窗口归并再下结论。

状态转移链（创建→清理，每跳负责组件与证据）：API 接收（API server；`uid`/`creationTimestamp`/`generation`，ObjectMeta 页）→ Kueue webhook 置 suspend（jobs.md L56–57）→ Workload 创建（job reconciler；`CreatedWorkload` 事件，排障页 L32）→ QuotaReserved（scheduler；admission 页 L17–24）→ AdmissionChecks（`Retry` 释配额重排/`Rejected` 去活，[admission_check L119–128](https://github.com/kubernetes-sigs/kueue/blob/911a822a49bcfd99c9c62203a009efa4130ad604/site/content/en/docs/concepts/admission_check/_index.md)）→ Admitted/unsuspend（Job 事件 `Started`/`Resumed`，jobs.md L191–197）→ Pod 创建（job-controller）→ PodScheduled（kube-scheduler）→ 沙箱就绪 `PodReadyToStartContainers`/`Initialized`（kubelet，Pod 生命周期页）→ Running → `ContainersReady`/`Ready`（kubelet；缺门默认 False）→ Kueue PodsReady（reason 见 v1beta2 类型 L1148–1159）→ 应用进展（应用自证）→ 终止条件（job-controller；Job 页 Terminal Job conditions，v1.31+ 门控见上）→ 清理（TTL controller 按 TTL 页；GC 按 finalizers/owners 页与传播策略）。

## 关键事件与下一项检查

| 症状 | 先看的证据 | 下一项检查 |
|---|---|---|
| Job 长期无 Pod 创建 | `describe workload` 的 `Admitted=False/Pending(workload didn't fit)`、`QuotaReserved` 条件；`spec.suspend` 是否为 true（未 admitted 或被抢占时挂起） | `kubectl get workloads` 的 `RESERVED IN`/`ADMITTED` 输出列（非事件）、ClusterQueue 配额与 cohort 借用、LocalQueue 是否存在/激活（`Inadmissible`）；事件时间戳只精确到秒，列出顺序不等于发生顺序，不据此推断因果 |
| 有 Pod 但不 Running | `describe pod` 的调度事件；`status.active/ready` 列 | `FailedScheduling`（资源/亲和/污点）、`NotTriggerScaleUp`（自动扩缩未触发）、镜像拉取与卷挂载 |
| Pod 反复重建 | Job `status.failed` 计数、`status.terminating`、`backoffLimit`、`podReplacementPolicy`、失败 Pod 退出码与 `DisruptionTarget` 条件 | 是否命中 `podFailurePolicy` 的 `FailJob`（如特定退出码表软件 bug）或 `Ignore`（中断不计入）；`OnFailure` 本地重启与新 Pod 重建分开计数；替换时机看 `podReplacementPolicy`（默认 `TerminatingOrFailed` 立即建，`Failed` 等终态） |
| `SuccessCriteriaMet`/`FailureTarget` 已出、`Complete`/`Failed` 迟迟不出 | `status.terminating`、Pod `deletionTimestamp`、所在节点状态、tracking finalizer | 查卡在 terminating 的 Pod 与门控（JobManagedBy/JobPodReplacementPolicy），再看节点与 finalizer |
| `Complete` 后 Pod 对象仍在 | Job 条件与 Pod 列表 | 属正常保留，按 TTL 或删除策略清理（删除传播见下行），不要当故障处理 |
| 节点失联、Pod 卡 Terminating | Pod phase/conditions、节点 `unreachable` 容忍、`podReplacementPolicy`（[setup_failure_recovery L9–33、L177–181](https://github.com/kubernetes-sigs/kueue/blob/911a822a49bcfd99c9c62203a009efa4130ad604/site/content/en/docs/tasks/manage/setup_failure_recovery.md)） | 无 recovery 时等节点恢复或人工干预；`Failed` 策略的 Job 无法推进；可选 FailureRecoveryPolicy（v0.15+、开门控、Pod 注解）60 秒强制 Failed，重调度前确认无数据损坏 |
| Workload 驱逐重排循环 | `Evicted` reason、`requeueState{count,requeueAt}`、PodsReady 条件（[workload L147–163](https://github.com/kubernetes-sigs/kueue/blob/911a822a49bcfd99c9c62203a009efa4130ad604/site/content/en/docs/concepts/workload.md)；[setup_wait_for_pods_ready L107–110](https://github.com/kubernetes-sigs/kueue/blob/911a822a49bcfd99c9c62203a009efa4130ad604/site/content/en/docs/tasks/manage/setup_wait_for_pods_ready.md)） | 按原因区分重排与去活（`backoffLimitCount` 内重排，超限去活）；查 PodsReadyTimeout 退避 |
| Job 以 Failed 结束 | 终止条件五类原因（Job 页 Terminal Job conditions：backoffLimit、activeDeadlineSeconds、backoffLimitPerIndex 失败索引、maxFailedIndexes、podFailurePolicy FailJob；reason 字符串仅 `DeadlineExceeded`/`FailedIndexes` 有页面示例，其余记 unknown） | 按五条分流，再看计数器与策略字段 |
| 删除 Job 后 Pod 残留 | 删除传播策略、Pod `ownerReferences`，再看 `deletionTimestamp`/`finalizers`（v1.32.0 [`strategy.go` L62–74](https://github.com/kubernetes/kubernetes/blob/v1.32.0/pkg/registry/batch/job/strategy.go)、[`storage.go` L56–57](https://github.com/kubernetes/kubernetes/blob/v1.32.0/pkg/registry/batch/job/storage/storage.go)） | 先查 propagationPolicy：API/控制器删除未带策略时 `batch/v1` 默认孤立（`OrphanDependents`，`child pods are preserved by default`），再查 job-tracking/foreground finalizer |
| TTL 到期未删或误删 | `ttlSecondsAfterFinished`、条件出现时间、时钟 skew | 完成条件出现时刻 vs 删除时刻；过期后延长不保证保留 |

Kueue 侧补充（[排障页](https://github.com/kubernetes-sigs/kueue/blob/911a822a49bcfd99c9c62203a009efa4130ad604/site/content/en/docs/tasks/troubleshooting/troubleshooting_jobs.md)）：`QuotaReserved True + Admitted True` = 已准入；`Pending + QuotaReserved False + resourceRequests` = 缺配额；`Evicted True + Preempted + Admitted False` = 被抢占；StrictFIFO 下队头阻塞时可能无 condition。`Are Pods running` 一节的 `the ready field shows how many of them are running` 把 ready 与 running 混用（文档用语较松），与 Job API 对 `ready` 的定义口径不同，此处不视为已做区分。

## 终止 / 重试 / 取消后的核对方法

1. **先定身份**：记录 Job UID、Workload 名（`<api-name>-<job-name>-<hash>` 反查，一对多时全列）、`metadata.generation`（spec 修订）、`requeueState.count` 与 ProvisioningRequest `-attempt<N>`（如有），同一窗口的事件、Pod 列表与节点状态归并到该身份下。
2. **再查账本（分三种情形，均为上游行为样本，非现场验证）**：终止（Complete/Failed）后看 `flavorsUsage` 下降（`reclaimablePods` 属运行期部分释放 Dynamic Reclaim，非终止后账本信号；`status.admission` 终止后是否保留无出处，记待确认）（ClusterQueue [`flavorsReservation`/`flavorsUsage`/`reservingWorkloads`/`admittedWorkloads`](https://github.com/kubernetes-sigs/kueue/blob/911a822a49bcfd99c9c62203a009efa4130ad604/apis/kueue/v1beta2/clusterqueue_types.go)（v1beta2 L362–392）与指标 [`kueue_cluster_queue_resource_reservation`/`_usage`](https://github.com/kubernetes-sigs/kueue/blob/911a822a49bcfd99c9c62203a009efa4130ad604/site/content/en/docs/reference/metrics.md)；重试（重排）时 `Evicted` 释配额但未必去活（`Retry` 重排继续，`Rejected`/`backoffLimitCount` 超限/`maximumExecutionTimeSeconds` 超时去活），`requeueState` 退避，`kueue_evicted_workloads_total` 按 `reason`/`underlying_cause` 区分；取消分四种触发（预期不同）：删 Job→Workload `resource-in-use` finalizer 移除（测试 L2365）＋对象去留按传播策略（Kueue 建 Workload 时把 Job 设为其 controller owner，[`reconciler.go` L1476](https://github.com/kubernetes-sigs/kueue/blob/911a822a49bcfd99c9c62203a009efa4130ad604/pkg/controller/jobframework/reconciler.go) `SetControllerReference`）（Background/Foreground 下 Workload 作为依赖被 GC 删除；Orphan 下保留，可由保留策略 `afterFinished` 回收，测试 L4042；经 `batch/v1` API 未带策略删除默认 Orphan；Kueue 默认不主动删已完成/去活 Workload 指非 GC 行为）；`spec.active=false`→驱逐释配额、不重排，Workload 仍在；ClusterQueue `stopPolicy: Hold`→已准入负载运行到完、仅 Reserving 取消预留（usage 不降）；`HoldAndDrain`→已 admit 的也驱逐释配额，对象仍在。不一致判读：已 Finished 但 `flavorsUsage` 未降→查 ClusterQueue 状态与指标采集；已 Evicted 但 reservation 仍在→查驱逐原因与重排状态；Job 已删但 `resource-in-use` 仍在→先区分该 Workload 是否本应被 GC 删除（Background/Foreground 下应删，Orphan 下保留），再查级联删除与 finalizer 阻塞。三类对应测试：终止见 K8s `TestDelayTerminalPhaseCondition`（L1236）/`TestJobFailedWithInterrupts`（L3776）；重排见 Kueue `should re-queue a workload evicted due to PodsReady timeout after the backoff elapses`（L3388）；弹性扩缩账本见 `Should handle rapid scale cycles without quota leaks`（L5306，`Describe("Job with elastic jobs via workload-slices support")`）；取消见 `Should not readmit a job to the queue after Active is changed to false`（L2707）/`Its workload finalizer should be removed`（L2365）。运行期部分释放见 `Should allow reclaim of resources that are no longer needed`（L2416：Completions(5)/Succeeded=4 后 `ReclaimablePods=[{main,1}]`，job2 解挂；非取消）。K8s 原生 ResourceQuota（`Across all pods in a non-terminal state`）不在本文账本范围内，本文只核 Kueue 配额。
3. **后验应用**：用 Job `completedIndexes`/`succeeded` 与业务侧 checkpoint/输出比对；`Finished` 只证 Job Complete/Failed。**训练恢复状态仍归应用**：Job 文档要求新 Pod 自理临时文件、锁与不完整输出；平台只保证重建、重排与记账，不保证续训正确。

## 适用边界

- Kubernetes 侧固定 v1.32 文档快照；Kueue v0.19.0 文档声明要求 K8s ≥1.29（[README](https://github.com/kubernetes-sigs/kueue/blob/911a822a49bcfd99c9c62203a009efa4130ad604/README.md)/[安装页](https://github.com/kubernetes-sigs/kueue/blob/911a822a49bcfd99c9c62203a009efa4130ad604/site/content/en/docs/getting-started/installation.md)），v1.32 在声明范围内，但未见测试矩阵，两者组合的运行状态为 unknown。特性门控：`backoffLimitPerIndex`（v1.29 Beta，门控 JobBackoffLimitPerIndex 默认开）、`successPolicy`（v1.31 Beta，门控 JobSuccessPolicy 默认开）、`podReplacementPolicy`（v1.29 Beta，门控 JobPodReplacementPolicy 默认开）、`managedBy`（v1.32 Beta，门控 JobManagedBy 默认开）、Elastic Indexed Job（v1.31 stable）、tracking finalizer（v1.26 stable）、`PodReadyToStartContainers`（Beta，门控 `PodReadyToStartContainersCondition` 默认开）、Kueue `PartialAdmission`（默认开）/`ElasticJobsViaWorkloadSlices`（Beta 默认开＋逐 Job 注解）/FailureRecoveryPolicy（v0.15 Alpha 默认关（[kube_features.go L682–683](https://github.com/kubernetes-sigs/kueue/blob/911a822a49bcfd99c9c62203a009efa4130ad604/pkg/features/kube_features.go)），需开门控＋Pod 注解）/Concurrent Admission（Alpha 默认关，需在 ClusterQueue 启用）。其他版本的行为差异不在本文范围。
- Kueue 侧固定 v0.19.0 commit；`maximumExecutionTimeSeconds` 与 `activeDeadlineSeconds` 叠加语义、TTL 删除与配额释放时序无直接证据，记 unknown。
- `generic` 不表示任意 CNI/CSI/设备插件/调度器组合受支持；设备分配后的证据链见[从物理设备到容器资源的状态链](device-resource-chain.md)，队列与放置见[作业准入、调度与拓扑放置](admission-and-placement.md)。
- 本文无可执行命令的验证记录；`verification.status: source_checked` 只覆盖上述文档核对。

## 常见误解

- `Job UID = Workload UID`：错。两者是不同对象，靠 label `kueue.x-k8s.io/job-uid` 关联；`generation` 是 spec 修订序号（非重试次数），重试/重排计数分散在 `status.failed`、`requeueState.count`、ProvisioningRequest attempt 等字段，没有统一计数器。
- `stopPolicy` 是 Job 字段：错。它是 ClusterQueue/LocalQueue 字段，仅三值。
- `backoffLimit: N` 即应用最多跑 N+1 次：错。`OnFailure` 本地重启与新 Pod 重建分开计数，`podFailurePolicy`/`backoffLimitPerIndex` 会改变口径。
- TTL 可用于 CronJob 或任意资源：错。仅 Job；过期后延长不保证保留。
- `Running + Ready` 即作业健康：错。Ready 只证容器与门的状态；Kueue `PodsReady=True` 的 reason `Started` 与 kueue-job-controller 发出的 Job 事件 `Started`（已准入）同名不同义；应用持续进展是第三层判断。
- Workload `Finished` 即训练结果正确：错。它只映射 Job Complete/Failed。
- Kueue 条件可直接等同 K8s 条件或 Volcano 语义：错。三套术语各自独立，本文不做映射。

## 例子与相关知识

- 准入与放置的队列、配额与拓扑语义见[作业准入、调度与拓扑放置](admission-and-placement.md)；设备分配后的链条见[从物理设备到容器资源的状态链](device-resource-chain.md)。
- “有空闲设备但作业不运行”时先按[空闲设备但作业等待诊断指南](idle-resource-job-waiting-triage.md)定位等待层，再用本页的事件与条件确认 Job/Workload/Pod 各自卡在哪一跳。
- Slurm 侧的独立状态机见[Slurm 作业生命周期、设备资源与状态参考](slurm-jobs-and-device-resources.md)；两套术语不可互套。

## 来源与待确认问题

- [Kubernetes v1.32 Job](https://v1-32.docs.kubernetes.io/docs/concepts/workloads/controllers/job/)、[Pod 生命周期](https://v1-32.docs.kubernetes.io/docs/concepts/workloads/pods/pod-lifecycle/)、[TTL-after-finished](https://v1-32.docs.kubernetes.io/docs/concepts/workloads/controllers/ttlafterfinished/)、[finalizers](https://v1-32.docs.kubernetes.io/docs/concepts/overview/working-with-objects/finalizers/)、[owners-dependents](https://v1-32.docs.kubernetes.io/docs/concepts/overview/working-with-objects/owners-dependents/)、[Job v1 API](https://v1-32.docs.kubernetes.io/docs/reference/kubernetes-api/workload-resources/job-v1/)：上文各节的版本化依据。
- [Kueue Job 集成（v0.19.0 commit）](https://github.com/kubernetes-sigs/kueue/blob/911a822a49bcfd99c9c62203a009efa4130ad604/site/content/en/docs/tasks/run/jobs.md)、[排障页](https://github.com/kubernetes-sigs/kueue/blob/911a822a49bcfd99c9c62203a009efa4130ad604/site/content/en/docs/tasks/troubleshooting/troubleshooting_jobs.md)、[v1beta2 `workload_types.go`](https://github.com/kubernetes-sigs/kueue/blob/911a822a49bcfd99c9c62203a009efa4130ad604/apis/kueue/v1beta2/workload_types.go)：Workload 状态与对齐方法依据（v1beta1 已弃用）。
- 待确认：TTL 删除与配额释放时序；`maximumExecutionTimeSeconds` 与 `activeDeadlineSeconds` 叠加语义；应用结果核对的官方例子；全部实测（未执行）。generation/attempt 口径见身份对照表（分散字段，无统一计数器）；账本字段与测试见核对方法（ResourceQuota 不在范围）。
