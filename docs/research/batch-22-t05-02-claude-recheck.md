# 第二十二批 T05-02 定向复核（作者首轮修订后）

复核日期：2026-10-14（实际取证日）。

**结论：不通过。B22-C01–C11 共 11 项：CLOSED 2（C01、C08），OPEN 9（C02、C03、C04、C05、C06、C07、C09、C10、C11）。** 未新增发现 ID。修订中新出现的事实问题，以及初审遗漏、本轮在固定 commit 上查实的问题，按原 ID 追记于 C02、C04、C06、C07、C09；其中 C07 追记包含对初审证据的纠正。

审阅者角色独立于作者修订角色。审阅模型为 `claude-opus-5-5`，由用户本次明确要求试用。这不是既有的 `gpt-6.1-sol / xhigh` 批量审阅约定，也不改写该约定。本会话内未见 `[frontier_llm]` 标记、认证失败或模型自报变化。审阅者无法在会话内读取 `modelUsage` 等运行元数据，也不补造。若操作方在运行记录中发现多键或模型不一致，按约定本轮作废，不留档、不引用。

本轮只写本报告一个文件。未改作者正文、来源记录、登记、索引或计划；未部署集群、未提交 Job、未运行任何测试。模型审阅不构成平台或现场验证。

## 输入（以 SHA-256 识别）

| 输入 | SHA-256 | 与任务给定前缀 |
|---|---|---|
| [T05-02 正文](../../knowledge/05-cluster-platform/kubernetes-job-lifecycle.md)（155 行） | `fdb8d0dcb839b85ad46a6fbac7fa22c52b74c268a469ff305c3a0bb5f9f4c5dc` | 一致 |
| [作者来源记录](batch-22-t05-02-sources.md)（25 行） | `ea793721f4b4a2f8bc326b994243a3a1a8b239dc2cbdb42bf09b7cb9393fa03d` | 一致 |
| [修订映射](batch-21-review-fixes.md)（T05-02 首轮修订节 L159–171） | `4bb9653f65a66ac98aa96952c30cb711287993b4e83af2f49cc61f7a3e519589` | 一致 |
| [初审报告](batch-22-t05-02-claude-review.md)（关闭条件权威来源；L294 计数已由作者机械修正为 437 并注明） | `082ad71dcf190c6846bd3de87f632f02f083eb28b80146a8b11c4a44406e1420` | 任务未给前缀，记实值 |
| [任务计划](../../plans/full-coverage-backlog.yaml)（T05-02 L5431–5467，acceptance L5448–5452） | `5f9bcf865b8c77e13cc8ee5f1c03140c37b86f558d8227d8bb2080249f4fcfc3` | 任务未给前缀；与初审所记完全相同，计划未变 |
| [来源登记](../../sources/registry.yaml)（`make check` 计 438 项；本文相关条目 L129–142、L559–572、L5347–5385、L5430–5440） | `7f64bf94474248b5edfed8ea671bb5950abd63e3721e39e7b6f749f2f559a9d4` | 一致 |

六个输入在取证开始和成稿前各哈希一次，结果相同。工作区在本轮期间出现 `docs/research/batch-21-t05-01-codex-recheck-8.md`，来自并行 T05-01 会话，与本复核无关，本轮未读。

## 取证方法与限制

- 方法：全部用 `curl -sSL` 默认 TLS 校验只读获取，下列原文 HTTP 均为 200。版本锚用 `git ls-remote`：Kueue `refs/tags/v0.19.0^{}` 为 `911a822a49bcfd99c9c62203a009efa4130ad604`，Kubernetes `refs/tags/v1.32.0^{}` 为 `70d3cc986aa8221cd1dfb1121852688902d3bf53`，均与登记和初审一致。HTML 去标签后按文字核对，不只判可达性。原文放在新建临时目录 `/tmp/b22rec02c/`（取证前不存在），未入库。
- **与初审逐字节比对**：本轮重取的初审文件全部字节一致。K8s 侧包括 Job 页 `b7c09281…`、Pod 生命周期 `3b6cd176…`、Job v1 API `c98f84c2…`、owners-dependents `462bf102…`、GC `3bb19013…`、ObjectMeta `74abd6c2…`、`job_test.go` `76ab4c0f…`、`strategy.go` `60591891…`、`storage.go` `bf36a996…`。Kueue 侧包括 jobs.md `9ff23de3…`、workload.md `b6a40f70…`、admission.md `69eb59b9…`、admission_check `6b95a63f…`、troubleshooting_jobs `fe6dfefb…`、cluster_queue `7b35c9f7…`、metrics `cd42760a…`、三篇 setup_* `c57c86c1…`/`4c688b65…`/`499ea5b7…`、v1beta1/v1beta2 workload_types `feea64aa…`/`50b9523e…`、v1beta2 clusterqueue_types `6092ac24…`、constants `30cae6ee…`、集成测试 `cc9a477e…`、README `f508b57e…`。因此初审表中的行号在本轮仍有效。
- **本轮新增取证**（初审未取）：

  | 来源 | 位置 | SHA-256 | 用途 |
  |---|---|---|---|
  | Kueue `pkg/features/kube_features.go`@911a822a | [链接](https://github.com/kubernetes-sigs/kueue/blob/911a822a49bcfd99c9c62203a009efa4130ad604/pkg/features/kube_features.go) | `225c13d60dcff1372b08855b51a9eb2ac1a6b05cc8a348f42a455e50ff8de02d` | Kueue 门控阶段与默认值 → C07/C09 |
  | Kueue `pkg/workload/workload.go`@911a822a | [链接](https://github.com/kubernetes-sigs/kueue/blob/911a822a49bcfd99c9c62203a009efa4130ad604/pkg/workload/workload.go) | `ccbff32a67a89ae37ca0e157f8a0daa91c7a85627f12802ae6a5a989f95bc41d` | 细分 reason 回退、ElasticJob 判定 → C07/C09 |
  | Kueue `pkg/workload/admissionchecks.go`@911a822a | [链接](https://github.com/kubernetes-sigs/kueue/blob/911a822a49bcfd99c9c62203a009efa4130ad604/pkg/workload/admissionchecks.go) | `75c26960e23ab0cb176ed753ff8a9e545835a7236b5180d2960219d0e40b2864` | Admitted reason 受门控 → C07 |
  | K8s v1.32 Feature Gates 页（未登记，旁证） | [feature-gates](https://v1-32.docs.kubernetes.io/docs/reference/command-line-tools-reference/feature-gates/) | `7c30813832d15f3ee9e274294ab5e765f3b56d6c21d9412ad87e66c990dbd407` | K8s 门控默认值 → C09 |

- 限制：
  - GitHub contents/trees API 本轮返回 rate limit（未认证），未能枚举目录树，只能按已知路径直取文件。按猜测路径取 Kueue `site/content/en/docs/installation/_index.md` 返回 404，未使用；K8s ≥1.29 的声明以 README L95 为准。
  - `UnadmittedWorkloadsObservability` 只追到 `workload.go` L1570–1575 与 `admissionchecks.go` L47–80 两处。同取的 `pkg/scheduler/scheduler.go` 中没有该门控字样；其余调用点未穷举。
  - 测试只核对函数名、It 名、行号，以及 Kueue L5306 所在的 Describe；断言未审计，CI 结果未查，所有测试都没有执行。
  - 未读 Kueue `concurrent_admission.md`、`elastic_workload.md`；K8s 文档网站源提交未固定，按 v1.32 快照 HTML 文字核对。

### 关键抽查点（原文文字核对）

| 抽查点 | 原文 | 结果 |
|---|---|---|
| 终止条件延迟（Job 页 "Terminal Job conditions"） | `In Kubernetes v1.31 and later the Job controller delays the addition of the terminal conditions, Failed or Complete, until all of the Job Pods are terminated`；`JobManagedBy and the JobPodReplacementPolicy (both enabled by default)` | 正文 L54 引文属实 |
| 早期信号（Job 页 "Termination of Job pods"） | `You can use the FailureTarget or the SuccessCriteriaMet condition to evaluate whether the Job has failed or succeeded without having to wait`；`terminationGracePeriodSeconds might increase the amount of time` | 支持 L54、L112 |
| 替换（Job 页 "Delayed creation of replacement pods"） | `the number of running Pods for a Job can be greater than parallelism or greater than one Pod per index (if you are using an Indexed Job)`；`creates replacement Pods immediately upon Pod deletion`；`For Jobs with a Pod failure policy set, the default podReplacementPolicy is Failed, and no other value is permitted` | 取值与默认值属实；L52 出处标注有误 → C02 |
| Job 失败原因（Job 页 "Terminal Job conditions"） | 五条：backoffLimit、activeDeadlineSeconds、backoffLimitPerIndex 失败索引、maxFailedIndexes、podFailurePolicy FailJob；页面示例 reason 只见 `DeadlineExceeded`、`FailedIndexes` | L116 计数与用词不准 → C06 |
| 删除默认孤立（v1.32.0 `strategy.go` L62–74、`storage.go` L56–57） | `case batchv1.SchemeGroupVersion: // for back compatibility return rest.OrphanDependents`；`child pods are preserved by default when jobs are deleted` | L117 属实，未给出处 → C06 |
| 属主与 GC（owners-dependents、GC 页）、记账（Job v1 API） | `Cross-namespace owner references are disallowed by design`；`deletes dependents it knows about`；`the only dependents that block owner …`；`Add the pod UID to the arrays … 2. Remove the pod finalizer. 3. Remove the pod UID from the arrays while increasing the corresponding counter` | L70、L72 属实 → C08 |
| Pending 与沙箱条件（Pod 生命周期页） | Pending 含 `waiting to be scheduled` 与镜像下载；`PodReadyToStartContainers: (beta feature; enabled by default) the Pod sandbox has been successfully created and networking configured` | L58 属实，beta 未标 → C09 |
| Workload 命名（troubleshooting_jobs.md L32、L35–40、L51） | `Normal CreatedWorkload … Created Workload: my-namespace/job-my-job-19797`；`kueue.x-k8s.io/job-uid`；`<api-name>-<job-name>-<hash>` | L76 属实 |
| stopPolicy（v1beta2 `clusterqueue_types.go` L132–144；cluster_queue.md L545–546） | `Hold - Admitted workloads will run to completion and Reserving workloads will cancel the reservation`；`HoldAndDrain - Admitted workloads are evicted` | L125 取消分支与此不符 → C04 |
| 账本字段与指标（v1beta2 `clusterqueue_types.go` L362–392；metrics.md L59、L121–122） | `flavorsReservation`/`flavorsUsage`/`pendingWorkloads`/`reservingWorkloads`/`admittedWorkloads … haven't finished yet`；`kueue_evicted_workloads_total`、`kueue_cluster_queue_resource_reservation`/`_usage` | L125 字段与行号属实 |
| Dynamic Reclaim（workload.md L124–140）；admission 字段（v1beta2 workload_types.go L635–637） | `allowing a currently Admitted workload to release a part of it's Quota Reservation`；`admission can be set back to null` | L125 终止分支用法不准或无出处 → C04 |
| 驱逐与去活（admission_check/_index.md L119–128；admission.md L28–38；workload.md L59；setup_wait_for_pods_ready.md L107–110） | Retry：驱逐并释放，不去活；Rejected：`Spec.Active` 置 False；`-attempt<N>` 属 ProvisioningRequest；重排达到 `backoffLimitCount` 后去活 | L78、L125 属实 |
| Failure recovery（setup_failure_recovery.md L9–28、L33、L177–181） | `grace period of 60 seconds`；`v0.15 or newer`；`FailureRecoveryPolicy feature gate enabled`；`Only pods annotated with kueue.x-k8s.io/safe-to-forcefully-delete`；默认 5 分钟 unreachable 容忍 | L62、L114 属实 |
| 保留与 finalizer（retention L10–14、L34–41；constants.go L20） | `By default, Kueue leaves all Workload objects in cluster indefinitely`；`afterFinished`/`afterDeactivatedByKueue`；`ResourceInUseFinalizerName = "kueue.x-k8s.io/resource-in-use"` | L68 属实 |
| Kueue 门控（kube_features.go） | `PartialAdmission` L545–547 0.5 Beta 默认 true；`ElasticJobsViaWorkloadSlices` L601–603 0.13 Alpha 默认 false → 0.18 Beta 默认 true；`FailureRecoveryPolicy` L682–683 0.15 Alpha 默认 false；`ConcurrentAdmission` L757–758 0.18 Alpha 默认 false；`UnadmittedWorkloadsObservability` L788–789 0.19 Beta 默认 false，注释 L479–481 `updates status reasons for QuotaReserved/Admitted conditions to use tiered reasons` | → C07、C09 |
| K8s 门控（v1.32 Feature Gates 表） | `JobBackoffLimitPerIndex` Beta 1.29– 默认 true；`JobSuccessPolicy` Beta 1.31– 默认 true；`JobManagedBy` Beta 1.32– 默认 true；`JobPodReplacementPolicy` Beta 1.29– 默认 true；`PodReadyToStartContainersCondition` Beta 1.29– 默认 true | → C09 |
| 测试行号 | K8s `job_test.go`：L260、L1236、L1623、L2889、L3154、L3594、L3641、L3686、L3776、L3884 的函数名全部属实。Kueue 集成测试：L2365、L2416、L2707、L3388、L3916、L4042、L5306 的 It/Describe 名全部属实；L5306 位于 `Describe("Job with elastic jobs via workload-slices support")`（L4307） | 行号属实；两处 It 名转写与归类有误 → C04 |
| 版本交集（README L95） | `**Requires Kubernetes 1.29 or newer**.` | L130 属实 |

## 逐项判定

### B22-C01 — CLOSED

位置证据：

- L54 区分了 terminal phase 与对象删除。原文引用 `delays the addition of the terminal conditions … until all of the Job Pods are terminated` 与两个门控（默认开）；`the Pods are usually not deleted either` 作为正常保留处理；`FailureTarget`/`SuccessCriteriaMet` 写为更早的信号；写明 ≤1.30 或门控关闭时行为不同。
- 关闭条件中"此时 Pod 可能仍在 terminating"在 L112 落实：该行先看 `status.terminating`、`deletionTimestamp`、节点状态与 tracking finalizer。
- 初审 L101 已拆成 L112（早期条件已出、终态条件迟迟不出）与 L113（`Complete` 后 Pod 对象仍在，属正常保留）两行。
- L88 引用了 `TestDelayTerminalPhaseCondition`，`job_test.go` L1236，含文件链接与函数名。

### B22-C02 — OPEN

已落实：

- L52 写入 `podReplacementPolicy`：两种取值；未设 podFailurePolicy 时默认 `TerminatingOrFailed`；设了 podFailurePolicy 时默认且只能为 `Failed`；v1.29 beta；门控默认开。门控名 JobPodReplacementPolicy 见 L54、L72。
- 初审指出的反向转述已改正为原文 `recreates terminating Pods only once these Pods reach the terminal Failed phase`。
- L111 加入 `status.terminating` 与替换策略判断。
- L88 引用 `TestJobPodReplacementPolicy` L2889 与 `TestJobPodReplacementPolicyFeatureToggling` L3154。

追记（修订中新出现的出处错误）：L52 写"默认策略下旧 Pod 优雅终止时新 Pod 已启动、同一 index 可能并存两 Pod（本库推论，非原文）"。Job 页 "Delayed creation of replacement pods" 节原文已写明：`By default, the Job controller recreates Pods as soon they either fail or are terminating` 与 `the number of running Pods for a Job can be greater than parallelism or greater than one Pod per index (if you are using an Indexed Job)`。把原文事实标为"非原文"是出处错误。初审证据第 2 条（原文）与第 4 条（审阅者推论：分布式训练同一 rank 两进程并存、资源双占）本来是分开的。

剩余关闭条件：拆开 L52 这一句。"Pod 数可超过 parallelism、Indexed Job 同一 index 可多于一个 Pod、终止中即建替换"按原文引用；只把"分布式训练同 rank 进程并存、资源双占、影响进程视图与账本"标为本库推论。

### B22-C03 — OPEN

已落实：

- L76：名称格式 `<api-name>-<job-name>-<hash>`，用 `CreatedWorkload` 事件或 `job-uid` label 反查，并说明按 Job 名直接查找不到；jobs.md 的 `with a matching name` 示例与排障页、控制器代码不一致，以后两者为准。
- L78：`-attempt<N>` 归 ProvisioningRequest，并注明只在配置了 ProvisioningRequest AdmissionCheck 时出现。L124 写"如有"。
- L82 增加了身份/代次清单。
- 来源记录 unknown 第 1 条已划线纠正（记录 L19）；登记 L5374 的 notes 已更正为"非同名，纠正初稿"。

剩余关闭条件：L82 自称"逐项列来源"，但除 ProvisioningRequest 一项"见上"之外，各项都没有给出来源。关闭条件要求每项写来源，需逐项补上：

- `metadata.generation` → v1.32 ObjectMeta 页。正文全文没有该页链接，L70 只写了登记 ID。
- 容器重启数 → Pod 生命周期页。
- `status.failed`/`failedIndexes` → Job v1 API。
- `requeueState.count` → workload.md L147–163；达到 `backoffLimitCount` 后去活 → setup_wait_for_pods_ready.md L107–110。
- ElasticJob 多 Workload → jobs.md L222–240。
- Concurrent Admission → workload.md L23–27，并带上 feature state（见 C09）。

确实没有来源的项保留 unknown。

### B22-C04 — OPEN

已落实：

- L125 把核对拆成终止、重试（重排）、取消三种情形。
- ClusterQueue 账本字段引 v1beta2 `clusterqueue_types.go` L362–392，经核属实。
- 指标 reservation/usage 与 `kueue_evicted_workloads_total` 的 `reason`/`underlying_cause` 属实。
- 每类情形都配了带行号的测试，行号全部属实。
- 初审 L110 的"本轮未读…unknown 保留"已删除。
- 写明 ResourceQuota（`Across all pods in a non-terminal state`）不在范围内。
- 复用 `src.kueue.admission-v0.19.0` 的理由见 frontmatter notes L29 与登记 L5374。

剩余关闭条件：

1. **取消分支混用了预期结果不同的三种触发**。v1beta2 `clusterqueue_types.go` L132–144 与 cluster_queue.md L545–546 写明，`stopPolicy: Hold` 下 `Admitted workloads will run to completion`，只有 Reserving workloads 取消预留。因此 Hold 不撤销已准入负载，其 usage 在负载结束前不下降。`HoldAndDrain` 与 `spec.active=false` 会驱逐负载并释放配额，但 Workload 对象仍在（workload.md L59），不会出现"finalizer 移除"。"Workload finalizer 移除"只对应删除 Job（Kueue 测试 L2365–2414）。需按触发方式分别写出预期变化。
2. 关闭条件要求"逐项写出预期变化与不一致时的判断"，三种情形目前都没有"不一致时"的判读。例如：已 Finished 但 `flavorsUsage` 未降；已 Evicted 但 reservation 仍在；Job 已删但 `resource-in-use` 仍在。每种情况需写出下一项检查。
3. 终止分支有两处不准：
   - `reclaimablePods` 属于 Dynamic Reclaim，原文为 `allowing a currently Admitted workload to release a part of it's Quota Reservation`（workload.md L124–140），是运行期的部分释放，不是终止后的账本信号。
   - "Workload `status.admission` 保留"没有出处。v1beta2 `workload_types.go` L635–637 只写 `admission can be set back to null`。需引证，或改记为待确认。
4. 测试归类与引名：
   - L5306 `Should handle rapid scale cycles without quota leaks` 位于 `Describe("Job with elastic jobs via workload-slices support")`（L4307），测的是 ElasticJob 扩缩循环下的配额泄漏，不是重试或重排样本。需改归为弹性扩缩的账本样本，或从"重排"中移出。
   - L2707 的 It 名在 L88 写成 `Should not readmit after Active=false`，在 L125 写成 `Should not readmit a job after Active is false`，用代码格式呈现，但都不是原文子串。原文为 `Should not readmit a job to the queue after Active is changed to false`，按原文引用。

### B22-C05 — OPEN

已落实：

- L103 增加了从创建到清理的转移链，覆盖初审关闭条件列出的各跳，并写了负责组件与证据字段或事件。
- L98 把 `FailedScheduling`（`default-scheduler`）与 `NotTriggerScaleUp`（`cluster-autoscaler`）移到"控制面（调度/扩缩）"行，与 troubleshooting_jobs.md L355–356 的 From 列一致。
- L97 节点行改用 Pod 条件、容器状态与重启计数。
- L58 按原文收窄了 Pending，沙箱联网归 `PodReadyToStartContainers`。

剩余关闭条件：关闭条件要求"各跳引版本化来源"，L103 全链没有逐跳来源，只有"v1.31+ 门控见上"一处回指。需逐跳给出处（链接或页面加行号）：

- `uid`/`creationTimestamp`/`generation` → ObjectMeta 页
- webhook 置 suspend → jobs.md L56–57
- `CreatedWorkload` → troubleshooting_jobs.md L32
- QuotaReserved 与 AdmissionChecks → admission.md L17–24、admission_check/_index.md L119–128
- `Started`/`Resumed` → jobs.md L191–197
- Pod 条件 → Pod 生命周期页
- Kueue PodsReady 的 reason → v1beta2 `workload_types.go` L1148–1159
- 终止条件 → Job 页 "Terminal Job conditions"
- 清理 → TTL 页与 GC 页

### B22-C06 — OPEN

已落实：

- 新增四行：L114 节点失联卡 Terminating、L115 驱逐重排循环、L116 按失败原因分流、L117 删除传播。
- L62 与 Kueue failure recovery 文档的说法一致，60 秒、v0.15+、门控、注解、5 分钟容忍均经核属实。
- FailureRecoveryPolicy 标为可选、需开门控并加 Pod 注解，与 `kube_features.go` L682–683（0.15 Alpha，默认 false）一致。
- L117 的默认孤立与 `strategy.go` L62–74、`storage.go` L56–57 一致。

剩余关闭条件：

1. 关闭条件要求"每行写先看的证据与下一项检查，并引来源"，L114–L117 四行都没有出处。另外：
   - setup_failure_recovery.md 与 setup_wait_for_pods_ready.md 在正文中没有任何链接，也未登记（见 C10）。
   - `strategy.go`/`storage.go` 在正文中没有链接，只出现在测试登记条目的 revision 字段里。
   - 需逐行补出处：L114 → setup_failure_recovery.md L9–33、L177–181；L115 → workload.md L147–163、setup_wait_for_pods_ready.md L107–110；L116 → Job 页 "Terminal Job conditions"；L117 → v1.32.0 `strategy.go` L62–74、`storage.go` L56–57。
2. L116 写"按五类失败原因分流"，却只列四项：backoffLimitPerIndex 的失败索引与 maxFailedIndexes 被合并成了"索引失败"。该列还把 spec 字段名当作"终止条件 reason"。需按 Job 页列出五条原因。reason 字符串在该页只见 `DeadlineExceeded`、`FailedIndexes`（页面示例），其余 reason 值要么引证，要么记为 unknown。

### B22-C07 — OPEN

已落实：

- L78、L125 按原因区分驱逐与去活：AdmissionCheck `Retry` 驱逐但不去活，`Rejected` 去活；抢占后重排；`spec.active=false`、重排超限、`maximumExecutionTimeSeconds` 超时会去活。各项与 admission_check/_index.md L119–128、admission.md L28–38、workload.md L59、setup_wait_for_pods_ready.md L107–110 一致。
- L68 补上 Workload 与 ClusterQueue 的 `kueue.x-k8s.io/resource-in-use` finalizer（constants.go L20；集成测试 L2365），以及 Workload 保留策略：默认一直保留，可选回收可能级联删除 Job。
- L80 增加了"条件与 reason 以 v1beta2 为准、v1beta1 已弃用"一句，并列出 v1beta2 新增的条件类型与 reason。

剩余关闭条件：

1. L80 前半句仍是"Workload 条件全集以 [v1beta1 `workload_types.go`] 常量为准：…"，紧接着又写"条件与 reason 以 v1beta2 为准"，两句自相矛盾。同类残留还有：L154 仍以 v1beta1 `workload_types.go` 作为"Workload 状态与对齐方法依据"；来源记录 L14 写"conditions 常量与 reason 全集"。需删去 v1beta1"全集"一句，改为"本文用到的子集（v1beta2）"，或给出 v1beta2 的完整列表并引行号。v1beta1 只保留"已弃用"的说明。修订映射 L169 写"v1beta2 为准"，但该句前半没有删除。
2. **追记（纠正初审证据）**：初审 C07 写 v1beta2 的 QuotaReserved/Admitted 细分 reason "正好可以用于'长期无 Pod'的排查"，这一说法过宽，本轮在固定 commit 上查实如下：
   - `kube_features.go` L479–481：`UnadmittedWorkloadsObservability … updates status reasons for QuotaReserved/Admitted conditions to use tiered reasons`；L788–789：v0.19 Beta，`Default: false`。
   - `pkg/workload/workload.go` L1570–1575：`UnadmittedWorkloadReasonWithFallback` 只在门控开启时返回细分 reason，否则返回回退值。
   - `pkg/workload/admissionchecks.go` L47–80：Admitted 的 reason 分支同样受门控影响，例如门控关闭时为 `NoReservationUnsatisfiedChecks`。
   - 已有登记 `src.kueue.admission-v0.19.0`（L572）也记有"细分等待 reason 默认不可见，只见 Pending 回退"。

   正文 L80 列出 `WaitingForQuota`/`Misconfigured`/`Suspended`/`NoReservation`/`UnsatisfiedAdmissionChecks` 等 reason，但没有写这一条件。需注明：这些细分 reason 只在开启 `UnadmittedWorkloadsObservability`（v0.19 Beta，默认关）后出现，默认只见回退 reason；不能作为默认环境下的排查证据。初审的相应表述就此撤回。

### B22-C08 — CLOSED

位置证据：

- L70 按原文改正：跨 namespace 引用按设计不允许；命名空间级依赖可以指向集群级或命名空间级 owner；`OwnerRefInvalidNamespace` 的两种情形。前台删除写为"删除已知依赖对象，只有 `blockOwnerDeletion=true` 且在 GC 缓存中的依赖会阻塞 owner 删除"。`orphan` finalizer 与 owners-dependents 页一致。
- L72 的 `uncountedTerminatedPods` 三步与 Job v1 API 原文一致。
- GC 页与 ObjectMeta 页已登记为 `src.kubernetes.api-gc-v1-32`（登记 L5430–5440），满足"以 GC 页为依据需先登记"。

非阻断：L70 用登记 ID 代替页面链接，并入 C10 第 3 条处理。

### B22-C09 — OPEN

已落实：

- L130 写明"Kueue v0.19.0 文档声明要求 K8s ≥1.29，v1.32 在声明范围内，但未见测试矩阵，两者组合的运行状态为 unknown"，与 README L95 一致。
- L130 列出 `podReplacementPolicy`、`managedBy`（JobManagedBy 默认开）、Elastic Indexed Job、tracking finalizer、FailureRecoveryPolicy 的状态；L54 写明终止条件延迟所依赖的门控。

剩余关闭条件：

1. 以下特性的门控名或默认值仍缺：
   - `backoffLimitPerIndex`：L130 只写"v1.29 beta"。Job 页注明门控为 JobBackoffLimitPerIndex；v1.32 Feature Gates 表为 Beta 1.29–，默认 true。
   - `successPolicy`：L50 只写"v1.31 beta"，L130 未列。Job 页为 `v1.31 [beta] (enabled by default: true)`，门控 JobSuccessPolicy。
   - `PodReadyToStartContainers`：L58 未标 beta。Pod 生命周期页为 `beta feature; enabled by default`，门控 PodReadyToStartContainersCondition。
   - Kueue `PartialAdmission`：L84 只写"v0.5 beta"。`kube_features.go` L545–547 为默认 true。
2. **追记（与固定 commit 不符）**：L84 写"`ElasticJob`（v0.13 alpha）"，L130 写"`ElasticJobsViaWorkloadSlices` 门控＋注解"。同一 commit 中：
   - `kube_features.go` L601–603 为 0.13 Alpha（默认 false）→ 0.18 Beta（默认 true）。
   - jobs.md L222 页头仍标 `alpha` `v0.13`，文档滞后于代码。
   - `pkg/workload/workload.go` L1561–1566 的 `IsElasticWorkload` 要求门控开启，且 Job 带注解 `kueue.x-k8s.io/elastic-job: "true"`。

   需改为：v0.19.0 代码中为 Beta、默认开，仍需逐个 Job 加注解；并注明 jobs.md 页头与代码不一致。
3. **追记（初审遗漏）**：L78、L82 把 Concurrent Admission 作为一个 Job 对应多个 Workload 的来源之一，但未标 feature state。`kube_features.go` L757–758 显示其为 0.18 Alpha，默认 false；workload.md L23–24 的原文是 `When Concurrent Admission is enabled for the Workload's ClusterQueue`。需标出 alpha、默认关，并说明需在 ClusterQueue 上启用。初审 C03 引用它时同样漏标了状态，在此一并记录。

### B22-C10 — OPEN

已落实：

- frontmatter 的 `source_refs` 与 `evidence_refs` 已加入 `src.kubernetes.api-gc-v1-32`、`src.kueue.admission-v0.19.0`、`src.kubernetes.device-plugins-v1-32`（L8–14、L23–28）。
- 两个计划 ID 的复用理由写在 L29 与登记 L5374。
- 两个 Kueue 条目已划分范围，L5374 写明"准入两阶段与类型定义原文见 src.kueue.admission-v0.19.0（复用，不重复登记）"，notes 已更正。
- L78 补上了 admission.md 链接。
- L88 的测试写到具体文件与行号。

剩余关闭条件：

1. 关闭条件点名的 setup_* 文档仍未登记。正文依据 Kueue `setup_failure_recovery.md`（L62、L114）、`setup_wait_for_pods_ready.md`（L82、L115）、`setup_object_retention_policy.md`（L68、L125），以及 README 的 K8s ≥1.29 声明（L130），但登记中没有任何条目提到它们（对登记全文检索无命中）。需单独登记，或并入 `src.kueue.job-lifecycle-v0.19.0`，并写明实际读到的范围。C07、C09 的修订若引用 `kube_features.go` 或 `pkg/workload/*`，也照此处理。
2. 来源记录与正文不同步：
   - L14 仍写 `workload_types.go（conditions 常量与 reason 全集）`。
   - 主张—来源定位表没有 api-gc、admission-v0.19.0（复用）、device-plugins（复用）三行。
   - L15 仍写"仅存在性；不断言语义"，而正文 L88、L125 已按行号把测试用作"上游行为样本"。
   - unknown 第 5 条（L23）仍写"本轮未读 cluster_queue/metrics 页"，与正文 L125 引用 `clusterqueue_types.go` L362–392 和指标的写法矛盾。
3. 正文缺少本轮新增依据的链接：metrics.md、v1beta2 `clusterqueue_types.go`、三篇 setup_* 文档、ObjectMeta 页与 GC 页（L70 只写了登记 ID）、`strategy.go`/`storage.go`。这一条与 C03、C05、C06 的"逐项、逐跳、逐行出处"重叠，补一次链接即可同时处理。

### B22-C11 — OPEN

已落实：

- L76 "不必"按原文改正。
- L109 写明 `RESERVED IN`/`ADMITTED` 是输出列，不是事件。
- L120 写明 ready 一词在排障页中用语较松，与 Job API 的定义口径不同。
- L141 区分了两个同名的 `Started`。

剩余关闭条件：L96 对齐表"控制面"行仍是箭头链 `Suspended→CreatedWorkload→SuccessfulCreate→Started→Resumed→Completed`。这个顺序照抄了 jobs.md L191–197 的列出顺序，其中第一个 `SuccessfulCreate` 排在 `Started`/`Resumed` 之前。按挂起创建的 Job 在 resume 之前不会建 Pod，所以这个顺序不可能是实际发生顺序；jobs.md L201–202 也提示列出顺序可能与发生顺序不同。作者把"不据此推断因果"的提示放在了另一张表的 L109，L96 本身没有变。需把 L96 改为无序列举，或就地注明"列出顺序≠发生顺序（jobs.md L201–202）"。

非阻断：L80 中 `Hold`（"已有运行到完、reserv 取消"）有截断词，原文为 `Reserving workloads will cancel the reservation`（clusterqueue_types.go L139–140）。

## 修订映射核对

映射 L161–171 所列改动多数已落盘。以下三条映射的说法比正文实际状态更进一步：

- C03 写"身份/代次对照表"：正文实为不带出处的清单。
- C07 写"v1beta2 为准"：v1beta1"全集"一句未删。
- C10 写"source_refs/evidence 与依据一致"：setup_* 文档未登记，来源记录未同步。

## acceptance 对照

| acceptance | 判定 | 未关闭发现 |
|---|---|---|
| 1 UID、generation/attempt、控制器责任与状态转移；区分 API 接收/admitted/Running/应用 ready/持续进展 | 部分满足。命名、反查、attempt 归属、身份清单、转移链都已补上；身份项与转移链缺出处 | C03、C05 |
| 2 backoff/deadline/retry/replacement、删除/finalizer、退出/回收与配额撤销；行为绑定版本 | 部分满足。终止条件语义（C01）与属主/记账（C08）已关闭；替换的出处标注、Workload 条件口径、门控状态未完成 | C02、C07、C09 |
| 3 三视图对齐表、关键事件、卡住/重试/清理的下一项检查 | 部分满足。表格结构与分支齐全；新增四行无出处，失败原因行不准，事件箭头链未注明 | C06、C11 |
| 4 终止/重试/取消后账本与应用结果核对、官方测试/例子；训练恢复归应用 | 部分满足。三情形、字段、指标、测试都已落地，"训练恢复归应用"保持明确（L126）；取消分支混用触发方式，缺不一致时的判读，一处测试归类错误、一处 It 名转写不准 | C04 |

横向问题：C10（来源一致性）。

## 结论

**T05-02 首轮修订后定向复核不通过：CLOSED 2/11（C01、C08），OPEN 9/11（C02、C03、C04、C05、C06、C07、C09、C10、C11）。**

- 初审中与原文方向相反的几处转述已全部改正：终止条件、替换注释、Workload 命名、`-attempt<N>`、属主与记账。
- 仍有几处与固定 commit 不符：C07 的细分 reason 受默认关闭的门控控制，C09 的 ElasticJob 状态、Concurrent Admission 状态。C02 还有一处出处标注错误。这些修订完成前，正文 `verification.status: source_checked` 只能视为部分成立。
- 建议修订顺序：先处理 C07 第 2 条、C09 第 2–3 条（与固定 commit 不符的事实），再处理 C04 第 1–3 条（账本判读）。C03、C05、C06、C10 的出处与登记问题可以合并成一轮处理，补链接加登记 setup_* 即可。C02、C11 是单句修改。
- 修订后需按上列剩余关闭条件做定向复核。
- 本复核只覆盖编辑与来源层面。文中 Kubernetes/Kueue 行为都是文档或源码层证据，不得标为 reproduced。

`make check`（取证完成后、写入本报告前运行）：`PASS: 96 content entries; 438 sources.` 与 `Checked structure and local file links; not technical correctness or remote links.`
