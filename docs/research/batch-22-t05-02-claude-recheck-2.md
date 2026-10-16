# 第二十二批 T05-02 第二次定向复核（作者第二轮修订后）

复核日期：2026-10-14（实际取证日）。

**结论：不通过。范围内 9 项（B22-C02–C07、C09–C11）：CLOSED 6（C02、C03、C05、C06、C07、C11），OPEN 3（C04、C09、C10）。连同前次已关闭的 C01、C08，B22-C01–C11 合计 CLOSED 8 / OPEN 3。** 未新增发现 ID。本轮新查实的事实问题按原 ID 追记于 C04，共两条，其中一条纠正前次复核的遗漏。

审阅者角色独立于作者修订角色。审阅模型为 `claude-opus-5-5`，由用户明确要求试用；这不是既有的 `gpt-6.1-sol / xhigh` 批量审阅约定，也不改写该约定。本会话内未见 `[frontier_llm]` 标记、认证失败或模型自报变化。审阅者无法在会话内读取 `modelUsage` 等运行元数据，也不补造。若操作方在运行记录中发现多键或模型不一致，按约定本轮作废，不留档、不引用。

作者自述已独立复核 `kube_features.go` 门控与 `workload.go` reason 回退取证点。本轮按任务要求独立重取，判定以下列核对为准。

本轮只写本报告一个文件。未改作者正文、来源记录、登记、索引或计划；未部署集群、未提交 Job、未运行任何测试。模型审阅不构成平台或现场验证。

## 输入（以 SHA-256 识别）

| 输入 | SHA-256 | 与任务给定前缀 |
|---|---|---|
| [T05-02 正文](../../knowledge/05-cluster-platform/kubernetes-job-lifecycle.md)（155 行） | `2fe86689318fb26038ccf625cf0241ea9c0f5bbd62fd777db27c87caa6e6c698` | 一致 |
| [作者来源记录](batch-22-t05-02-sources.md)（25 行） | `65a6fbf2debd665ce82daabb1b307fe6cb80bd02d3d84f5039ba62ac829e11b8` | 一致 |
| [修订映射](batch-21-review-fixes.md)（T05-02 第二轮修订节 L329–338） | `0f6a990206011ca4f71d88e5895133f8f5c674799abe3c66691ec690b16b1719` | 一致 |
| [前次复核报告](batch-22-t05-02-claude-recheck.md)（剩余关闭条件权威来源） | `cee92793122b0778c62afe23d3b17515d8cc3e3d2ff9a9be27992d423a1accae` | 任务未给前缀，记实值 |
| [初审报告](batch-22-t05-02-claude-review.md) | `082ad71dcf190c6846bd3de87f632f02f083eb28b80146a8b11c4a44406e1420` | 任务未给前缀；与前次复核所记相同 |
| [任务计划](../../plans/full-coverage-backlog.yaml)（T05-02 L5431–5467，acceptance L5448–5452） | `5f9bcf865b8c77e13cc8ee5f1c03140c37b86f558d8227d8bb2080249f4fcfc3` | 任务未给前缀；与前两轮相同，计划未变 |
| [来源登记](../../sources/registry.yaml)（440 项；本文相关条目 L559–572、L5347–5385、L5430–5440） | `8d59b5c88cacc70432b93e0b1763ad89d83821bebe53d4964d3a66027b7c5f8a` | 一致 |

七个输入在取证开始和成稿前各哈希一次，结果相同。正文 frontmatter 的六个来源 ID 在前次复核时均已存在；登记从 438 项增到 440 项，增量不涉及本文 ID。

## 取证方法与限制

- **取证方式**：全部用 `curl -sSL` 只读获取，默认 TLS 校验（`ssl_verify_result=0`），下列原文 HTTP 均为 200。版本锚用 `git ls-remote`：Kueue `refs/tags/v0.19.0^{}` 为 `911a822a49bcfd99c9c62203a009efa4130ad604`，Kubernetes `refs/tags/v1.32.0^{}` 为 `70d3cc986aa8221cd1dfb1121852688902d3bf53`，与登记和前两轮一致。HTML 去标签后按文字核对，不只判可达性。原文放在新建临时目录 `/tmp/b22rec2c3/`（取证前不存在），未入库。
- **目录枚举**：未使用 GitHub API（前次遇未认证限流）。改用 `git clone --depth 1 --filter=blob:none --no-checkout --branch v0.19.0`，HEAD 为 `911a822a…`，再用 `git ls-tree` 定位文件路径。只读，不检出工作区；文件内容仍以 curl 取回为准。
- **与前次复核逐字节比对**：前次已记哈希的文件，本轮重取后全部字节一致。K8s 侧包括 Job 页 `b7c09281…`、Pod 生命周期 `3b6cd176…`、Job v1 API `c98f84c2…`、ObjectMeta `74abd6c2…`、GC `3bb19013…`、owners-dependents `462bf102…`、Feature Gates `7c308138…`、`job_test.go` `76ab4c0f…`、`strategy.go` `60591891…`、`storage.go` `bf36a996…`。Kueue 侧包括 jobs.md `9ff23de3…`、workload.md `b6a40f70…`、admission.md `69eb59b9…`、admission_check `6b95a63f…`、troubleshooting_jobs `fe6dfefb…`、cluster_queue `7b35c9f7…`、metrics `cd42760a…`、setup_failure_recovery `499ea5b7…`、setup_wait_for_pods_ready `c57c86c1…`、setup_object_retention_policy `4c688b65…`、v1beta1/v1beta2 workload_types `feea64aa…`/`50b9523e…`、v1beta2 clusterqueue_types `6092ac24…`、v1beta2 constants `30cae6ee…`、kube_features `225c13d6…`、workload.go `ccbff32a…`、admissionchecks.go `75c26960…`、集成测试 `cc9a477e…`、README `f508b57e…`。因此前次报告中的行号在本轮仍有效。前次记录的 constants `30cae6ee…` 对应 `apis/kueue/v1beta2/constants.go`。本轮先误取 `pkg/constants/constants.go`（`24ce8fc0…`，不含该 finalizer 常量），未使用。
- **本轮新增取证**（前两轮未取）：

  | 来源 | 位置 | SHA-256 | 用途 |
  |---|---|---|---|
  | Kueue `getting-started/installation.md`@911a822a | [链接](https://github.com/kubernetes-sigs/kueue/blob/911a822a49bcfd99c9c62203a009efa4130ad604/site/content/en/docs/getting-started/installation.md) | `5260d45537be94a8e2e983c6774f790f4378928aa19eb7ba12946867e0acdc17` | L39 的 K8s ≥1.29 声明 → C09/C10。纠正前次"安装页按猜测路径 404"的限制：实际路径在 `getting-started/` 下 |
  | Kueue `pkg/controller/jobframework/reconciler.go`@911a822a | [链接](https://github.com/kubernetes-sigs/kueue/blob/911a822a49bcfd99c9c62203a009efa4130ad604/pkg/controller/jobframework/reconciler.go) | `f92d82943df2318d7cea39fb40dc7c21734478ad6d6133e2c85ca05ddd2ea94e` | L1476 Workload 的 controller owner → C04 追记 |
  | K8s `staging/src/k8s.io/api/batch/v1/types.go`@v1.32.0 | [链接](https://github.com/kubernetes/kubernetes/blob/v1.32.0/staging/src/k8s.io/api/batch/v1/types.go) | `b51be02a14925c84d0727b71f2a8221676251d32a0e6122924ef62b82cc2e461` | L636–657 JobReason 常量 → C06 非阻断 |
  | K8s v1.32 TTL-after-finished 页 | [链接](https://v1-32.docs.kubernetes.io/docs/concepts/workloads/controllers/ttlafterfinished/) | `e2f40f3e761fd338fd805748be010e0cc90c0b795ed7fe0b4d37036ffda95be3` | v1.23 stable、级联删除 → C05 |
  | K8s v1.32 finalizers 页 | [链接](https://v1-32.docs.kubernetes.io/docs/concepts/overview/working-with-objects/finalizers/) | `de96f53cbbb734c3c11e44414996fde34fd277b6e0bec96d475e2ffdacc6b94a` | 清理跳 → C05 |

- 限制：
  - 测试只核对了函数名、It/Describe 名与行号。L2365、L2416、L4042 三个 It 另读了 `By` 步骤与关键断言，其余断言未审计；CI 结果未查；所有测试都没有执行。Kueue 集成测试的运行环境配置（例如是否运行 GC 控制器）本轮未核，因此不从 L2365 中"删 Job 后 Workload 仍可 Get"推断真实集群行为。
  - `kube_features.go` 中 `FailureRecoveryPolicy` 只有 L683 一项（0.15 Alpha，默认 false）。紧随其后的 L686 `0.16 … Default: true … Beta` 属于 `SkipFinalizersForPodsSuspendedByParent`，按行 grep 时容易误读，本轮已读完整代码块确认。
  - `UnadmittedWorkloadsObservability` 只核到 `workload.go` L1568–1575 与 `admissionchecks.go` L47–80，其余调用点未穷举。
  - 未读 Kueue `concurrent_admission.md`、`elastic_workload.md`。K8s 文档网站源提交未固定，按 v1.32 快照 HTML 文字核对。

### 关键抽查点（原文文字核对）

| 抽查点 | 原文 | 结果 |
|---|---|---|
| 替换（Job 页 "Delayed creation of replacement pods"） | `By default, the Job controller recreates Pods as soon they either fail or are terminating`；`the number of running Pods for a Job can be greater than parallelism or greater than one Pod per index (if you are using an Indexed Job)`；`the control plane creates replacement Pods immediately upon Pod deletion`；`For Jobs with a Pod failure policy set, the default podReplacementPolicy is Failed, and no other value is permitted` | L52 原文与推论已分开 → C02 |
| ObjectMeta 页 | `generation`：`A sequence number representing a specific generation of the desired state. Populated by the system. Read-only.`；`uid`：`unique in time and space` | L82 → C03 |
| Pod 生命周期页 | 示例输出列 `NAMESPACE NAME READY STATUS RESTARTS AGE`；`PodReadyToStartContainers: (beta feature; enabled by default)` | L82 → C03；L130 → C09 |
| workload.md L23–27、L59、L147–163 | `When Concurrent Admission is enabled for the Workload's ClusterQueue`；`Changing .spec.Active from true to false will cause a running workload to be evicted and not be requeued`；`.status.requeueState.count indicates the numbers of times a Workload has already been backoff re-queued` | C03、C04 |
| admission.md L17–24、L28–32 | `two-phase admission cycle`；L32 `Kueue creates new ProvisioningRequest with -attempt<N> suffix each retry` | C03、C05 |
| jobs.md L56–57、L191–202、L222–240 | `you do not need to create the Job in a suspended state` / `via webhook`；事件表；L201–202 `the events might be listed in a slightly different order from which they actually occurred`；L222 页头 `alpha` `v0.13`；门控 `ElasticJobsViaWorkloadSlices` 与注解 `kueue.x-k8s.io/elastic-job: "true"`；扩容时建新 Workload，旧 Workload 标 `Finished` | C05、C09、C11 |
| troubleshooting_jobs.md L32 | `CreatedWorkload … Created Workload: my-namespace/job-my-job-19797` | C05 |
| admission_check/_index.md L119–128 | Retry：驱逐，reason 为 `AdmissionCheck`，释放 QuotaReservation；Rejected：`Spec.Active is set to False` | C05 |
| setup_wait_for_pods_ready.md L107–110 | `re-queue a Workload evicted by the PodsReadyTimeout reason until the number of re-queues reaches backoffLimitCount`；`Kueue deactivates the Workload` | C03、C06 |
| setup_failure_recovery.md L9–33、L177–181 | `podReplacementPolicy: Failed, preventing the Job from making progress`；`grace period of 60 seconds`；`v0.15 or newer`；`FailureRecoveryPolicy feature gate enabled`；`Only pods annotated with kueue.x-k8s.io/safe-to-forcefully-delete`；`5 minute toleration for the node.kubernetes.io/unreachable taint` | L62、L114 属实 → C06 |
| Job 页 "Terminal Job conditions" | 五条失败原因：backoffLimit、activeDeadlineSeconds、backoffLimitPerIndex 失败索引、maxFailedIndexes、podFailurePolicy `FailJob`。页面失败侧 reason 示例只有 `reason: DeadlineExceeded`、`reason: FailedIndexes`；成功侧另有 `SuccessPolicy` reason | L116 属实 → C06 |
| v1.32.0 `batch/v1/types.go` L636–657 | `PodFailurePolicy`、`BackoffLimitExceeded`、`DeadlineExceeded`、`MaxFailedIndexesExceeded`、`FailedIndexes`（失败侧）；`SuccessPolicy`、`CompletionsReached`（成功侧） | C06 非阻断 |
| v1.32.0 `strategy.go` L62–74、`storage.go` L56–57 | `case batchv1.SchemeGroupVersion: // for back compatibility return rest.OrphanDependents`；`child pods are preserved by default when jobs are deleted` | C04、C06 |
| GC 页 | `By default, Kubernetes uses background cascading deletion unless you manually use foreground deletion or choose to orphan the dependent objects.` | C04 追记 |
| v1beta2 `clusterqueue_types.go` L132–144、L362–392；cluster_queue.md L545–546 | `HoldAndDrain - Admitted workloads are evicted and Reserving workloads will cancel the reservation`；`Hold - Admitted workloads will run to completion and Reserving workloads will cancel the reservation`；`flavorsReservation`/`flavorsUsage`/`pendingWorkloads`/`reservingWorkloads`/`admittedWorkloads` | L125 属实 → C04 |
| v1beta2 `workload_types.go` L635–637、L931–1174；v1beta1 L779 | `admission can be set back to null`；条件与 reason 常量；PodsReady reason L1148–1159（`WaitForStart`/`WaitForRecovery`/`Started`/`Recovered`）；v1beta2 L1179 `storageversion`；v1beta1 L779 `This version is deprecated. Use v1beta2 instead.` | C04、C05、C07 |
| metrics.md L59、L121–122 | `kueue_evicted_workloads_total` 的标签 `reason`、`underlying_cause`；`kueue_cluster_queue_resource_reservation` / `_usage` | L125 属实 → C04 |
| Kueue 门控（`kube_features.go`） | `PartialAdmission` L546–547：0.5 Beta，默认 true。`ElasticJobsViaWorkloadSlices` L602–603：0.13 Alpha 默认 false，0.18 Beta 默认 true。`FailureRecoveryPolicy` L683：0.15 Alpha，默认 false。`ConcurrentAdmission` L758：0.18 Alpha，默认 false。`UnadmittedWorkloadsObservability` L789：0.19 Beta，默认 false；注释 L479–480 | C07、C09 |
| `workload.go` L1559–1575；`admissionchecks.go` L47–80 | `IsElasticWorkload` 要求门控开启且带注解；`UnadmittedWorkloadReasonWithFallback` 在门控关闭时返回回退值；Admitted 的 reason 分支同样受门控影响（门控关时为 `NoReservationUnsatisfiedChecks`） | C07、C09 |
| K8s v1.32 Feature Gates 表；Job 页 feature-state | `JobBackoffLimitPerIndex` Beta 1.29–，true；`JobSuccessPolicy` Beta 1.31–，true；`JobManagedBy` Beta 1.32–，true；`JobPodReplacementPolicy` Beta 1.29–，true；`PodReadyToStartContainersCondition` Beta 1.29–，true。Pod failure policy v1.31 stable；Elastic Indexed Jobs v1.31 stable；tracking finalizer v1.26 stable；TTL v1.23 stable | C09 |
| Kueue installation.md L39；README L95 | `A Kubernetes cluster with version 1.29 or newer is running.`；`**Requires Kubernetes 1.29 or newer**.` | L130 "README/安装页" 属实 → C09/C10 |
| `jobframework/reconciler.go` L1461–1478 | `wl := NewWorkload(...)`；L1476 `ctrl.SetControllerReference(object, wl, c.Scheme())` | C04 追记 |
| Kueue 集成测试 | L2365 `Its workload finalizer should be removed`；L2416 `Should allow reclaim of resources that are no longer needed`；L2707 `Should not readmit a job to the queue after Active is changed to false`；L3388 `should re-queue a workload evicted due to PodsReady timeout after the backoff elapses`；L3916 `Describe("Job controller with ObjectRetentionPolicies")`；L4042 `should delete orphaned Workload after finishing if the Job is deleted with PropagationPolicy=DeletePropagationOrphan`；L4307 `Describe("Job with elastic jobs via workload-slices support")`；L5306 `Should handle rapid scale cycles without quota leaks` | 行号属实；L88 两处、L125 一处引名或归类不符 → C04 |
| K8s `job_test.go` | L260、L1236、L1623、L2889、L3154、L3594、L3686、L3776、L3884 九个函数名全部属实 | — |

## 逐项判定

### B22-C02 — CLOSED

位置证据：

- L52 把原文与推论分开。"默认策略下终止中即建替换，运行 Pod 数可超 parallelism、Indexed Job 同一 index 可多于一个 Pod"注明出自 Job 页原文，与 "Delayed creation of replacement pods" 节一致。"分布式训练同 rank 两进程并存、资源双占、影响进程视图与账本"标为本库推论。
- `podReplacementPolicy` 的两种取值、默认值与 podFailurePolicy 约束经原文核对属实；v1.28 起的行为注释（`recreates terminating Pods only once these Pods reach the terminal Failed phase`）也属实。

非阻断：L52 句尾"只把'…'标为本库推论"是把前次关闭条件的措辞搬进了正文，读来像修订指令。建议改为陈述句，例如"本库推论：分布式训练中同一 rank 可能两进程并存、资源双占，影响进程视图与账本"。

### B22-C03 — CLOSED

位置证据：L82 身份/代次清单逐项给出来源，经核对全部属实。

- UID 与 `metadata.generation` → ObjectMeta 页（有链接），原文见上表。
- 容器重启数 → Pod 生命周期页 `RESTARTS` 列。
- `status.failed`/`failedIndexes` → Job v1 API（有链接）。
- `requeueState.count` → workload 页 L147–163；`backoffLimitCount` 去活 → setup_wait_for_pods_ready L107–110。
- ProvisioningRequest `-attempt<N>` → admission 页 L28–32（原文在 L32）。
- ElasticJob 多 Workload → jobs.md L222–240。
- Concurrent Admission → workload 页 L23–27，标为 Alpha、默认关，与 `kube_features.go` L758 一致。

非阻断：

- "Pod 替换产生新 Pod（新名新 UID，Job 页替换节）"：Job 页替换节只写了建 replacement Pods，没有写"新名新 UID"。"新 UID"可以由 ObjectMeta 页的 uid 定义（`unique in time and space`）支撑，建议把出处改挂到该页。
- setup_wait_for_pods_ready 只写了页名与行号，没有链接，并入 C10 剩余第 2 条处理。

### B22-C04 — OPEN

已落实（对照前次剩余关闭条件）：

1. 取消分支按四种触发分别写出预期：删 Job、`spec.active=false`、`stopPolicy: Hold`、`HoldAndDrain`。Hold 与 HoldAndDrain 的写法与 v1beta2 `clusterqueue_types.go` L137–139 和 cluster_queue.md L545–546 一致；`spec.active=false` 的写法与 workload.md L59 一致。
2. 加入三条不一致判读，各配一项下一步检查：已 Finished 但 `flavorsUsage` 未降；已 Evicted 但 reservation 仍在；Job 已删但 `resource-in-use` 仍在。
3. 终止分支：`reclaimablePods` 改归运行期部分释放（Dynamic Reclaim）；`status.admission` 终止后是否保留改记为待确认，与 v1beta2 `workload_types.go` L635–637 不冲突。
4. L5306 改归"弹性扩缩账本"，并注明其所属 Describe（L4307）。L125 中 L2707 的 It 名已按原文引用。

剩余关闭条件：

1. **L88 的 It 名仍未按原文**。L88 仍写 `Should not readmit after Active=false`（L2707），不是原文子串。前次第 4 条点名了 L88 与 L125 两处，本轮只改了 L125。需改为原文 `Should not readmit a job to the queue after Active is changed to false`。
2. **追记（前次复核遗漏）：L2416 归类错误，且引名截断**。L125 把 `Should allow reclaim of resources`（L2416）列在"取消见…"之下。该 It 的原文名为 `Should allow reclaim of resources that are no longer needed`，测试内容如下：job1 设 `Completions(5)`/`Parallelism(2)`（L2419–2420）；把 `Status.Succeeded` 置为 4（L2454）；断言 Workload 的 `Status.ReclaimablePods` 为 `[{main, Count: 1}]`（L2462–2465）；随后原本放不下的 job2 被解除挂起（L2468–2472）。这是运行期部分释放（Dynamic Reclaim）的样本，不涉及取消。同一段落已写明"`reclaimablePods` 属运行期部分释放 Dynamic Reclaim，非终止后账本信号"，把该测试列为取消样本因此前后矛盾。L88 与 L125 用代码格式写的 `Should allow reclaim of resources` 只是原文名的截断前缀。需把 L2416 移出"取消"，改作运行期部分释放的样本，并按原文全名引用。前次复核写"每类情形都配了带行号的测试，行号全部属实"，当时只核了行号与名称，没有核归类，此处一并纠正。
3. **追记（删 Job 分支的预期不准）**：L125 写"删 Job→Workload `resource-in-use` finalizer 移除（测试 L2365），对象按保留策略（默认保留，可选回收可级联）"。同一 commit 中，Kueue 建 Workload 时把 Job 设为其 controller owner（`jobframework/reconciler.go` L1476 `ctrl.SetControllerReference(object, wl, …)`）。因此 Job 删除后 Workload 对象的去留取决于传播策略：
   - 以 Background 或 Foreground 删除时（GC 页 L889–890：未另行指定时默认 background），Workload 作为依赖对象由 GC 删除。
   - 以 Orphan 删除时，Workload 保留，可由保留策略 `afterFinished` 回收（Kueue 测试 L4042 `should delete orphaned Workload after finishing if the Job is deleted with PropagationPolicy=DeletePropagationOrphan`）。通过 `batch/v1` API 删除且未带传播策略时，默认即为 Orphan（v1.32.0 `strategy.go` L62–74，正文 L117 已写）。

   setup_object_retention_policy 的 `leaves all Workload objects in cluster indefinitely`（L12–13）说的是 Kueue 默认不主动删除已完成或已去活的 Workload，不是 GC 行为。"可选回收可级联"指回收去活 Workload 时可能连带删除其属主（同页 Notes L204–208），Job 已删除时不适用。L2365 只断言 finalizer 被移除（L2406–2411），不能支撑"对象默认保留"。需按传播策略写出 Workload 的预期去留；"Job 已删但 `resource-in-use` 仍在"一条判读也应先区分该 Workload 是否本应被 GC 删除。

### B22-C05 — CLOSED

位置证据：L103 状态转移链逐跳给出出处，覆盖前次列出的九跳，所引行号经核对全部属实：

- `uid`/`creationTimestamp`/`generation` → ObjectMeta 页
- webhook 置 suspend → jobs.md L56–57
- `CreatedWorkload` → 排障页 L32
- QuotaReserved → admission 页 L17–24
- AdmissionChecks 的 Retry/Rejected → admission_check L119–128
- `Started`/`Resumed` → jobs.md L191–197（同一范围内含 job-controller 的 `SuccessfulCreate`，可支撑"Pod 创建（job-controller）"一跳）
- Pod 条件 → Pod 生命周期页
- Kueue PodsReady 的 reason → v1beta2 类型 L1148–1159
- 终止条件 → Job 页 "Terminal Job conditions"
- 清理 → TTL 页与 finalizers/owners 页

非阻断：清理跳引的是 finalizers/owners 页，不是前次点名的 GC 页。owners 页覆盖级联删除，可以接受。GC 页在正文中仍无链接，并入 C10 剩余第 2 条。

### B22-C06 — CLOSED

位置证据：

- L114–L117 四行都已按页名加行号给出处，经核对属实：
  - L114 → setup_failure_recovery L9–33、L177–181
  - L115 → workload L147–163、setup_wait_for_pods_ready L107–110
  - L116 → Job 页 "Terminal Job conditions"
  - L117 → v1.32.0 `strategy.go` L62–74、`storage.go` L56–57
- L116 已按 Job 页列出五条失败原因，不再把 spec 字段名当作 reason。reason 字符串只把页面示例中出现的 `DeadlineExceeded`、`FailedIndexes` 当作已证，其余记为 unknown，符合前次"要么引证，要么记为 unknown"的要求。
- L62 与 setup_failure_recovery 的说法一致（`podReplacementPolicy: Failed` 的 Job 无法推进；60 秒；v0.15+；门控；注解；5 分钟容忍）。

非阻断：

- v1.32.0 `staging/src/k8s.io/api/batch/v1/types.go` L636–657 定义了全部五个失败侧 reason 常量（`PodFailurePolicy`、`BackoffLimitExceeded`、`DeadlineExceeded`、`MaxFailedIndexesExceeded`、`FailedIndexes`）。作者可以据此把 L116 的 unknown 改为引证，采用时需先登记该文件。
- 四行所引页面在正文中没有链接，并入 C10 剩余第 2 条。

### B22-C07 — CLOSED

位置证据：

1. 正文 L80、L154 与来源记录 L14 已没有 v1beta1"全集"一说（全文检索命中 0），改为"本文用到的子集（v1beta2）"，v1beta1 只保留"已弃用"说明。
   - L80 所列条件 `Admitted`/`QuotaReserved`/`Finished`/`PodsReady`/`Evicted`/`Preempted`/`Requeued`/`DeactivationTarget` 均可在 v1beta2 L931–1023 找到。
   - reason `Preempted`/`PodsReadyTimeout`/`AdmissionCheck`/`ClusterQueueStopped`/`MaximumExecutionTimeExceeded`/`Succeeded`/`Failed` 均可在 L1083–1167 找到。
   - L80 标为"新增"的 `BlockedOnPreemptionGates`、`WaitingForReplacementPods` 及 QuotaReserved/Admitted 的细分 reason，经比对在 v1beta1 中均不存在。
2. L80 已注明：细分等待 reason 只在开启 `UnadmittedWorkloadsObservability`（v0.19 Beta，默认关）后出现，默认只见回退 reason，不能作为默认环境下的排查证据。这与 `kube_features.go` L479–480、L789，`workload.go` L1568–1575，`admissionchecks.go` L47–80 一致。

非阻断：

- L80 先写"本文用到的子集（v1beta2…，v1beta1 已弃用）"，隔一句又写"条件与 reason 以 v1beta2 为准（…v1beta1 已弃用…）"，并在门控说明之后再次列出细分 reason，内容重复，可以合并。
- 门控状态在正文中没有任何出处，并入 C10 剩余第 2 条。

### B22-C09 — OPEN

已落实：

- L130 写入 `backoffLimitPerIndex`（门控 JobBackoffLimitPerIndex，默认开）与 `successPolicy`（门控 JobSuccessPolicy，默认开），与 v1.32 Feature Gates 表一致。
- L84 与 L130 写入 `PartialAdmission`（v0.5 Beta，默认开），与 `kube_features.go` L547 一致。
- L84 与 L130 把 ElasticJob 改为"代码 v0.18 Beta 默认开，仍需逐个 Job 加 `kueue.x-k8s.io/elastic-job: "true"` 注解，jobs.md 页头仍标 v0.13 alpha"。这与 `kube_features.go` L602–603、`workload.go` L1561–1566、jobs.md L222、L228–229 一致。
- L82、L84、L130 写入 Concurrent Admission（v0.18 Alpha，默认关，需在 ClusterQueue 上启用），与 `kube_features.go` L758 和 workload.md L23–24 一致。
- L130 的"README/安装页"经本轮核对属实（installation.md L39、README L95）。

剩余关闭条件：`PodReadyToStartContainers` 仍缺门控名。L130 写的是"`PodReadyToStartContainers`（Beta，默认开）"，而门控名是 `PodReadyToStartContainersCondition`（v1.32 Feature Gates 表：Beta 1.29–，默认 true），与条件名不同。同一行中其他 K8s 特性都按"门控 X 默认开"的格式写明了门控名，前次关闭条件也已点名该门控。需补上门控名；L58 是否同时标注 beta 可由作者决定。只需改一处短语。

### B22-C10 — OPEN

已落实：

- 前次第 1 条（登记）：登记 L5366 的 revision 已把 setup_failure_recovery、setup_wait_for_pods_ready、setup_object_retention_policy、metrics 与 cluster_queue 页、`kube_features.go`（门控阶段与默认值）、`pkg/workload`（reason 回退与 Elastic 判定）以及 README/安装页的 K8s ≥1.29 声明并入 `src.kueue.job-lifecycle-v0.19.0`，并写明了范围。本轮确认安装页确实存在（`site/content/en/docs/getting-started/installation.md` L39）。
- 前次第 2 条（来源记录）大部分已同步：
  - L14 已无"全集"一说，并带有三篇 setup_* 的链接，写明了 `kube_features.go`/`pkg/workload` 以及对 admission-v0.19.0 和 device-plugins 的复用。
  - L15 改为"上游行为样本，非现场验证；断言未审计、CI 未查"。
  - unknown 第 5 条已划线纠正。

剩余关闭条件：

1. **来源记录仍缺 api-gc**：来源记录中检索 `api-gc`、`ObjectMeta`、`GC` 均无命中，主张—来源定位表没有 `src.kubernetes.api-gc-v1-32`（ObjectMeta 页、GC 页）这一行。`strategy.go`/`storage.go` 也只出现在登记 tests 条目的 revision 字段中，来源记录没有提及。需补一行：ObjectMeta、GC、owners 归 api-gc；strategy、storage 写明归属的登记条目。
2. **正文链接（前次第 3 条）未处理**。以下依据在正文中只有页名加行号，或完全没有出处，都没有 Markdown 链接：
   - metrics.md（L125 只写了指标名）
   - v1beta2 `clusterqueue_types.go`（L125）
   - cluster_queue.md（正文未提及）
   - setup_failure_recovery（L62、L114）
   - setup_wait_for_pods_ready（L82、L115）
   - setup_object_retention_policy（L68 只写"retention 场景 B 及 Notes"）
   - GC 页（L70 仍只写登记 ID）
   - v1.32.0 `strategy.go`/`storage.go`（L117）
   - admission_check/_index.md（L103）
   - README 与安装页（L130）
   - `kube_features.go` 与 `pkg/workload/*.go`（L80、L84 的门控状态在正文中没有任何出处）

   按 AGENTS.md "cite exact supporting pages or revisions near substantive claims" 与前次第 3 条，需以固定 commit、v1.32 文档或 v1.32.0 tag 链接补齐。C03、C05、C06、C07 的非阻断链接问题随本条一次处理。

非阻断：登记 `src.kubernetes.job-controller-tests-v1.32.0` 的标题仍为"（存在性）"，license notes 仍写"只链接并记录存在性"，而 revision 已改为"上游行为样本"，三处说法建议统一。

### B22-C11 — CLOSED

位置证据：L96 已改为无序列举（`Suspended`、`CreatedWorkload`、`SuccessfulCreate`、`Started`、`Resumed`、`Completed`），并就地注明"列出顺序≠发生顺序，jobs.md L201–202"。jobs.md L201–202 原文为 `the events might be listed in a slightly different order from which they actually occurred`，属实。

非阻断（前次已记，仍未改）：L80 仍写"`Hold`（已有运行到完、reserv 取消）"，截断词还在。修订映射 L338 声称已修正，但正文未改。L125 的写法完整。

## 修订映射核对

映射 L329–338 与落盘状态对照：

- C02、C03、C05、C07 的映射描述与正文一致。
- C04 写"L2707 按原文 It 名"：只改了 L125，L88 未改（见 C04 剩余第 1 条）。
- C06 写"L56 与 failure recovery 对齐"：L56 是小节标题，对应的改动在 L62（内容一致，只是行号有误）。
- C09 写"门控/默认值补齐（…PodReadyToStartContainers…）"：补了默认值，没有补门控名。
- C10 写"api-gc 新登记；…admission.md 链接；测试文件行号"：这三项都是首轮修订的改动（前次复核已确认 api-gc 位于登记 L5430–5440，L78 已有 admission.md 链接，L88 已有测试行号），本轮该条目的位置与内容都未变，不属于第二轮落盘改动。
- C11 写"Hold 截断词修正"：正文 L80 未改。

## acceptance 对照

| acceptance | 判定 | 未关闭发现 |
|---|---|---|
| 1 UID、generation/attempt、控制器责任与状态转移；区分 API 接收/admitted/Running/应用 ready/持续进展 | 满足。身份清单逐项有出处（C03），转移链逐跳有出处（C05），层次区分保持明确；链接缺口记在 C10 | —（C10 横向） |
| 2 backoff/deadline/retry/replacement、删除/finalizer、退出/回收与配额撤销；行为绑定版本 | 部分满足。替换的出处标注、Workload 条件口径、细分 reason 门控、Elastic 与 Concurrent Admission 的状态都已落实；仍缺一个 K8s 门控名；删 Job 后 Workload 的去留未按传播策略区分 | C04、C09 |
| 3 三视图对齐表、关键事件、卡住/重试/清理的下一项检查 | 满足。四行异常排查各有出处，失败原因五条，事件顺序已注明（C06、C11） | —（C10 横向） |
| 4 终止/重试/取消后账本与应用结果核对、官方测试/例子；训练恢复归应用 | 部分满足。四种触发、不一致判读、字段与指标都已落地，"训练恢复归应用"仍写明（L126）；一个测试归类错误，两处 It 名引用不准，删 Job 分支的预期不准 | C04 |

横向问题：C10（来源一致性与正文链接）。

## 结论

**T05-02 第二轮修订后第二次定向复核不通过：范围内 CLOSED 6/9（C02、C03、C05、C06、C07、C11），OPEN 3/9（C04、C09、C10）；B22-C01–C11 合计 CLOSED 8/11、OPEN 3/11。**

- 前次指出的与固定 commit 不符的事实问题已全部改正：C07 的细分 reason 门控，C09 的 ElasticJob 状态与 Concurrent Admission 状态，C02 的出处标注。作者对 `kube_features.go` 与 `workload.go` 取证点的转述，经本轮独立核对一致。
- 仍需修订的事实问题都在 C04：L2416 被当作取消样本，实为 Dynamic Reclaim 测试；删 Job 后 Workload 的去留取决于传播策略，正文只写了"默认保留"。其余是 L88 一处 It 名、C09 一个门控名，以及 C10 的来源记录与正文链接。
- 建议修订顺序：先处理 C04 剩余第 2、3 条（事实与归类）；再一次性补齐 C10 剩余第 2 条的正文链接，同时补来源记录中的 api-gc 一行；最后改 C04 第 1 条与 C09 的单句。非阻断项（C02 句式、C03 出处改挂、C06 reason 常量、C07 重复、C11 截断词）可以在同一轮顺手处理。
- 修订后需按上列剩余关闭条件做定向复核。
- 本复核只覆盖编辑与来源层面。文中 Kubernetes/Kueue 行为都是文档或源码层证据，不得标为 reproduced；正文 `verification.status: source_checked` 在上述问题修订前只能视为部分成立。
