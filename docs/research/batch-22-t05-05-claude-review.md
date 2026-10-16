# 第二十二批 T05-05 初审

审阅日期：2026-10-14 至 2026-10-15（实际取证跨越本地零点）。正文 `updated_at: "2026-10-14"` 与审阅日接近，但输入以下表 SHA-256 识别，不以日期推导。

**结论：T05-05 需修订。新增 9 项发现（B22-C22–C30）：P1 ×2、P2 ×4、P3 ×3，全部 OPEN。** acceptance 4 基本满足，acceptance 1–3 只部分满足。

- acceptance 1：gang 插件的成组校验、条件上报转述基本属实。但启动失败、重排队与回退整体记为 unknown，而同一 tag 的 allocate/enqueue 动作和 job 控制器中有可读实现。`minResources` 被归给 gang 插件，与实现不符。抢占保护的说法只对旧版 preempt/reclaim 动作成立。
- acceptance 2：Kueue 与 Slurm 两个样板分开写，字段名大体属实，"选择依据""公平性代价"也分了标签。问题在内容：Kueue 的回收代价忽略了默认值 `Never` 和 Fair Sharing；Slurm 的公平性代价表述混乱，也没有写 fair-share；"时用 X"的选择依据读起来像产品推荐。
- acceptance 3：两个样板都缺资源向量、拓扑、运行进展的观测，碎片只在 Slurm 侧有一句；"对照验收"只是一个站内链接。
- acceptance 4：MindCluster 型号与调度路径边界保持住了，抽查的三份一次源与正文一致；已链接 idle-resource-job-waiting-triage 与 Slurm 状态参考，L134 有"不是统一策略"的声明，正文也没有写成已验证的部署指南。

正文没有虚构命令输出或实测结果，`verification.notes` 如实写明未部署、未提交、未验证。`make check` 结果见文末；它只校验结构与本地链接，不说明技术正确性。

审阅者角色独立于作者。审阅模型为 `claude-opus-5-5`，由用户本次明确要求试用。这不是既有的 `gpt-6.1-sol / xhigh` 批量审阅约定，也不改写该约定。本轮未出现 `[frontier_llm]` 标记、模型不一致或认证失败；推理等级等运行元数据没有可核验记录，不补造。本轮只做审阅和只读取证：未改作者正文、来源记录、登记、索引或计划；未部署 Volcano/Kueue/MindCluster/Slurm，未提交作业，未运行任何测试。模型审阅不构成平台或现场验证。

发现编号说明：审阅开始时在 `docs/research/` 中检索 `B22-C`，最大号为 C21（[T05-03 初审](batch-22-t05-03-claude-review.md) 用到 C21），没有 C22 及以上的占用，本报告从 B22-C22 续号。

## 输入（以 SHA-256 识别）

| 输入 | SHA-256 |
|---|---|
| [T05-05 正文](../../knowledge/05-cluster-platform/admission-and-placement.md)（134 行，concept / draft，revise） | `df7f423f291529efc58f288685b87a1e4ac96e7802aac46e68423918fef9ad7e` |
| [作者来源记录](batch-22-t05-05-sources.md)（16 行） | `ad68dab7b518ed68ae18c831f02a484e5e74360e75b4ac6010d99d3210882ddd` |
| [任务计划](../../plans/full-coverage-backlog.yaml)（T05-05 L5552–5590，acceptance L5569–5573，source_discovery L5581–5583） | `5f9bcf865b8c77e13cc8ee5f1c03140c37b86f558d8227d8bb2080249f4fcfc3` |
| [来源登记](../../sources/registry.yaml)（T05-05 新登记 L5463–5484：`src.volcano.gang-plugin-v1.15.0`、`src.kueue.cluster-queue-v0.19.0`） | `bf28034112d7b830869ed65438928e769089aa465862dfa12ced39b50f088e3f`；L5463–5484 段 `8c4031b3a1cacdf7bc79528a0da59f28776a0012f46a8302a7dbba83105d8d18` |

四个输入在审阅开始时取哈希，成稿前复取一次（见文末）。

旁证（按本库现行草稿核对，未重新取其一次源）：正文 L128 与 L134 的两个站内链接（`slurm-jobs-and-device-resources.md`、`idle-resource-job-waiting-triage.md`）及 L124 的 `kubernetes-job-lifecycle.md` 都能解析到已有文件；[T05-02 正文](../../knowledge/05-cluster-platform/kubernetes-job-lifecycle.md) L115 已写 Kueue 的 Workload 驱逐重排循环（`requeueState`、PodsReadyTimeout 退避），可供本文引用。

## 一次源取证（审阅者独立获取）

方法：全部用 `curl -sSL` 默认 TLS 校验只读获取，HTTP 均为 200（例外见取证限制）。GitHub 文件经 `raw.githubusercontent.com` 按固定 commit 取回；HTML 去标签后按文字核对，不只判可达性。版本锚用 `git ls-remote`。原文只放在临时目录 `/tmp/b22rev05c/raw/`，未入库。

作者来源记录没有写取证方法与哈希；[第二十二批来源审计](batch-22-source-audit.md) 记载作者侧 curl 访问 `raw.githubusercontent.com` 时 DNS 失败，改用 webfetch。本表哈希是本审阅的取证，不能写成作者取证。

版本锚：

- Volcano：`refs/tags/v1.15.0` 为 tag 对象 `4691eac388eb8ec033908cbe144b8f3aafcaeef7`，`^{}` 指向 commit `8fc394c11e8db0d0ada5c17816b58bced9d7213d`。经 tag 与经该 commit 取回的 `gang.go` 字节一致。
- Kueue：`refs/tags/v0.19.0` 为 tag 对象 `7b3cad14a540cd256dc9c658be5a23fff809ff68`，指向 commit `911a822a49bcfd99c9c62203a009efa4130ad604`，与正文和登记一致。
- MindCluster：`refs/tags/v26.1.1` 指向 commit `44385c13d7b1d87def35f1604e8be4d16de6ca4e`，与登记一致。
- Slurm：归档页页头均为 `Version 24.11`，补丁级只由路径 `archive/slurm-24.11.7/` 确定。reservations、priority_multifactor、qos、job_reason_codes 的哈希与 T05-03 初审所记相同。

### Volcano v1.15.0（commit `8fc394c1`）

| 来源（登记 ID） | 位置 | SHA-256（原文） | 核对点与结果 |
|---|---|---|---|
| gang 插件（src.volcano.gang-plugin-v1.15.0） | [gang.go](https://github.com/volcano-sh/volcano/blob/8fc394c11e8db0d0ada5c17816b58bced9d7213d/pkg/scheduler/plugins/gang/gang.go)（297 行） | `9f3fe99299e26bd93bf05705aac6216ffb969642e03f087d8f6949e8a1ad2159` | **属实**：`validJobFn` L58–93：`CheckTaskValid` 与 `CheckSubJobValid` 都给 `NotEnoughPodsOfTaskReason`，`ValidTaskNum < MinAvailable` 给 `NotEnoughPodsReason`。`preemptableFn` L97–125 在 `ReadyTaskNum() > MinAvailable` 时才逐个放行 victim。`AddJobReadyFn` L191–197、`AddJobPipelinedFn` L204–211。`OnSessionClose` L229–297：未就绪写 `PodGroupUnschedulableType`/`NotEnoughResourcesReason`，消息 `%v/%v tasks in gang unschedulable: %v`；就绪写 `PodGroupScheduled`，reason 为 `tasks in gang are ready to be scheduled`。**正文未用**：L131–137 `AddUnifiedEvictableFn` 对 GangReclaim/GangPreempt `permits all candidates`；L256 `metrics.RegisterJobRetries`；全文不引用 `MinResources`。→ C24、C25、C29 |
| JobInfo（未登记，同 commit） | [job_info.go](https://github.com/volcano-sh/volcano/blob/8fc394c11e8db0d0ada5c17816b58bced9d7213d/pkg/scheduler/api/job_info.go) | `e8d19400b3493b6909843dc4633449c41272c15e9a0f6ebd1a3c790e79a5823b` | `ReadyTaskNum` L877–886 计 Bound/Binding/Running/Allocated/Succeeded；`ValidTaskNum` L1130–1142 另计 Pending 与 Pipelined；`IsReady`/`IsPipelined`/`IsStarving` L1202–1212；`GetMinResources` L599–606。→ C24 |
| allocate 动作（未登记） | [allocate.go](https://github.com/volcano-sh/volcano/blob/8fc394c11e8db0d0ada5c17816b58bced9d7213d/pkg/scheduler/actions/allocate/allocate.go) | `7eefa6aca0cb96b49096cc195bb8f4fc7b81ead79c87039bcf42570bd30bc632` | L152–169：配置了 enqueue 时，Pending 的 PodGroup 跳过 allocate；`JobValid` 不通过也跳过。L313–322、L329–336：只有 `ssn.JobReady(job)` 时才 `stmt.Commit()`（注释 `do not commit stmt when job is pipelined`），`minAvailable < replicas` 时把作业放回队列。L832–844：SubJob ready 或 pipelined 时返回 statement，否则 `stmt.Discard()`。→ C22 |
| enqueue 动作及测试（未登记） | [enqueue.go](https://github.com/volcano-sh/volcano/blob/8fc394c11e8db0d0ada5c17816b58bced9d7213d/pkg/scheduler/actions/enqueue/enqueue.go)；[enqueue_test.go](https://github.com/volcano-sh/volcano/blob/8fc394c11e8db0d0ada5c17816b58bced9d7213d/pkg/scheduler/actions/enqueue/enqueue_test.go) | `38b8feb1d0e3f74f119fbabb7add38f9c35a44cfd0d89a7988ebd068594e2cde`；`f09d7636185e2dff1d4e666ec093d4e7730f61917746f42f2f6760f1bfa6a1ad` | enqueue.go L95–99：`MinResources == nil` 或 `ssn.JobEnqueueable(job)` 时转 `PodGroupInqueue`。测试 L112 用例 `pggroup cannot enqueue because queue resources are less than podgroup MinResources`，期望保持 Pending（只读，未运行）。→ C22、C24 |
| JobEnqueueable 提供方（未登记） | [proportion.go](https://github.com/volcano-sh/volcano/blob/8fc394c11e8db0d0ada5c17816b58bced9d7213d/pkg/scheduler/plugins/proportion/proportion.go)、[capacity.go](https://github.com/volcano-sh/volcano/blob/8fc394c11e8db0d0ada5c17816b58bced9d7213d/pkg/scheduler/plugins/capacity/capacity.go)、[overcommit.go](https://github.com/volcano-sh/volcano/blob/8fc394c11e8db0d0ada5c17816b58bced9d7213d/pkg/scheduler/plugins/overcommit/overcommit.go) | `9077aae9669b08bcb832175907a9955d9847db841bf5793e0a1e269a7de72c53`；`1bef988f1461d338c81f0d26aab7991f519c58f93a14a3015690dba6e537b006`；`b04c395507dcbd783bfa9abce3c85930f20c544e5c61ed1032cc3077a389e283` | 三个插件都读取 `PodGroup.Spec.MinResources`（proportion L419–423、capacity L769–779、overcommit L95–141）。只用 grep 定位，未审计各自的判定公式。→ C24 |
| 动作注册与 gangpreempt（未登记） | [factory.go](https://github.com/volcano-sh/volcano/blob/8fc394c11e8db0d0ada5c17816b58bced9d7213d/pkg/scheduler/actions/factory.go)；[gangpreempt.go](https://github.com/volcano-sh/volcano/blob/8fc394c11e8db0d0ada5c17816b58bced9d7213d/pkg/scheduler/actions/gangpreempt/gangpreempt.go) | `cd04cb3e374e992b89dfe38bb3d3502a0a066d36275c95285475de4ff7735e54`；`440e6ff3cb6a53d13311bad0eeb6b5cae0c7c4f5767df0866a8bd9694e31694d` | factory.go L36–43 注册 reclaim/allocate/backfill/preempt/gangpreempt/gangreclaim/enqueue/shuffle。gangpreempt.go L32–52 `allowWholeBundle` 默认 `true`（`whole-job ("whole-bundle") victim bundles may be selected`），L248 只有显式关掉时才跳过 whole bundle。→ C25 |
| job 控制器（未登记） | [job_controller_handler.go](https://github.com/volcano-sh/volcano/blob/8fc394c11e8db0d0ada5c17816b58bced9d7213d/pkg/controllers/job/job_controller_handler.go)、[job_controller_util.go](https://github.com/volcano-sh/volcano/blob/8fc394c11e8db0d0ada5c17816b58bced9d7213d/pkg/controllers/job/job_controller_util.go)、[state/running.go](https://github.com/volcano-sh/volcano/blob/8fc394c11e8db0d0ada5c17816b58bced9d7213d/pkg/controllers/job/state/running.go)、[state/restarting.go](https://github.com/volcano-sh/volcano/blob/8fc394c11e8db0d0ada5c17816b58bced9d7213d/pkg/controllers/job/state/restarting.go)、[job_controller_actions.go](https://github.com/volcano-sh/volcano/blob/8fc394c11e8db0d0ada5c17816b58bced9d7213d/pkg/controllers/job/job_controller_actions.go) | `6b559057d0e077d0775fd1ecb4536ddbc56a8e6125f3a7bbd785f55ec7cbdecb`；`e9632a066d72f0907eacde5d6e131bb5ee6de77c28e9a5cb2ee3f81bb47e070b`；`97cadbe2a70ca6b5fc280f9bd7169c0322fbae60a3e115f5cf66a7e8f2b74544`；`954f7fb4d9bfc2ea3b7b4a3633df5db5ff5dace4b88fe4b72728c53c34310f6a`；`c2bc5da70272f41c21dab40355bbe0d0c5e53e0f5f1a31cb155625d6b2aaaed2` | handler L273–281：Pod 转 Failed 产生 `PodFailedEvent`，取第一个容器的退出码。util `applyPolicies` L182–284：默认动作是 `SyncJobAction`；先按 task 级、再按 job 级 policy 的事件或 exitCode 匹配；L286–288 `PodPendingEvent` 只有带 `Timeout` 时才生效。running.go L35–45：RestartJob/RestartTask/RestartPod/RestartPartition 杀 Pod、转 Restarting、`RetryCount++`；L107–108 `status.Pending > jobReplicas-MinAvailable` 时 job 转回 Pending。restarting.go L35–47：`RetryCount >= maxRetry` 转 Failed，否则在终止数足够后转 Pending。actions L816、L877–880、L923：控制器按 `minAvailable` 计算并同步 PodGroup 的 `minMember`/`minResources`。→ C22、C24 |
| 测试文件存在性 | `pkg/scheduler/plugins/gang/gang_test.go`、`pkg/controllers/job/state/running_test.go` | 两者 404 | 该 commit 下 gang 插件目录没有单元测试文件。allocate_test.go（`9a7bc70a29f11a499e77372c9dc1b8cff3f790a8c244de904ed49a0d8c0f72fe`）L4711 有 `can not allocate job when minMember is not satisfied`；job_controller_util_test.go（`7bf0ed2f15cfcef00b99411ecfe52c16ffb6a6d20add6f8f69b8d5a461b37758`）L481 有 `TestApplyPolicies`，L867–917 覆盖 PodPending+Timeout。只读用例名，未审计断言，未运行。→ C22 |
| PodGroup 文档（src.volcano.podgroup-gang-v1.15.0） | [PodGroup](https://volcano.sh/docs/v1.15.0/concepts/podgroup/) | `17fe53e5e166cf82abef73ea94e325d3816720facdec0180270ebdabf7cf50e2`（可变网页，仅本次观察） | 页头 `Version: v1.15.0`。**属实**：minMember、minResources（`no pod or task in the PodGroup will be scheduled`）。**正文未用**：phase `unknown`（`some are running while others are not scheduled … The scheduler will wait until ControllerManager starts these pods or tasks again`）；`inqueue`（`passed validation and is waiting to be bound to a node … transient state between pending and running`）；`If no PodGroup is specified … Volcano will create a PodGroup`。→ C22 |
| Gang 文档（同上） | [Gang](https://volcano.sh/docs/v1.15.0/scheduler/plugins/gang/) | `6a39b97d0bc7bb780dcd1057c8770442b6deab3a5f5a1d6d1c3f44026d1ec26b`（同上） | **属实**：`All or nothing`、JobReadyFn/JobPipelinedFn/JobValidFn。**与实现不一致**：文档说 Ready 状态包含 `Binding, Bound, Running, Allocated, Succeed, and Pipelined`，实现中 `ReadyTaskNum` 不计 Pipelined（Pipelined 只计入 `IsPipelined`）。→ C24 |

### Kueue v0.19.0（commit `911a822a`）

| 来源（登记 ID） | 位置 | SHA-256（原文） | 核对点与结果 |
|---|---|---|---|
| ClusterQueue 文档（src.kueue.cluster-queue-v0.19.0） | [cluster_queue.md](https://github.com/kubernetes-sigs/kueue/blob/911a822a49bcfd99c9c62203a009efa4130ad604/site/content/en/docs/concepts/cluster_queue.md)（561 行，与登记所记行数一致） | `7b35c9f7e8caee0815ca506f463975a09202412422c03c1f63dd91224510b346` | **属实**：resourceGroups/nominalQuota（L60–74）；borrowingLimit/lendingLimit（L309–413）；StrictFIFO 阻塞、默认 BestEffortFIFO（L201–209）；三个抢占字段（L438–472）；flavorFungibility 的 `whenCanBorrow` 默认 `MayStopSearch`、`whenCanPreempt` 默认 `TryNextFlavor`（L506–515）。**正文未用或与正文不符**：三个抢占字段默认都是 `Never`（L443、L459、L469）；Fair Sharing（L6、L14、L446–452），以及 `borrowWithinCohort` 不可与 Fair Sharing 同用（L457）；cohort 内优先满足 nominalQuota 内的负载（L248、L304–307）；fits 判定规则 1–3（L233–242）。→ C26、C27、C29 |
| Workload 条件 reason（src.kueue.admission-v0.19.0 范围内） | [v1beta2 workload_types.go](https://github.com/kubernetes-sigs/kueue/blob/911a822a49bcfd99c9c62203a009efa4130ad604/apis/kueue/v1beta2/workload_types.go) | `50b9523e7ad0cb8c59fbb9133c03bb2e74a293f369b8333cda816c4c0dd44dc1` | **属实**：`WaitingForQuota` 存在（L947–949）。**正文未用**：`ExceedsMaxQuota`（L951–954，`This also includes exceeding ClusterQueue nominal + borrowingLimit constraints`）；`TopologyPlacementFailed`（L956–958）；`WaitingForPreemptedWorkloads`、`Suspended`、`WaitingForPodsReady` 等。→ C23、C27 |
| 细分 reason 的门控 | [kube_features.go](https://github.com/kubernetes-sigs/kueue/blob/911a822a49bcfd99c9c62203a009efa4130ad604/pkg/features/kube_features.go)、[workload.go](https://github.com/kubernetes-sigs/kueue/blob/911a822a49bcfd99c9c62203a009efa4130ad604/pkg/workload/workload.go)、[scheduler.go](https://github.com/kubernetes-sigs/kueue/blob/911a822a49bcfd99c9c62203a009efa4130ad604/pkg/scheduler/scheduler.go) | `225c13d60dcff1372b08855b51a9eb2ac1a6b05cc8a348f42a455e50ff8de02d`；`ccbff32a67a89ae37ca0e157f8a0daa91c7a85627f12802ae6a5a989f95bc41d`；`b857d0bdd94ea5e9b32070ce33d35a97655a0687f0ed1190553aeefbfe0bea10` | **属实**：`UnadmittedWorkloadsObservability` 为 0.19 Beta、默认 false（features L479–481、L788–790）；`UnadmittedWorkloadReasonWithFallback` 门控关闭时返回 fallback（workload.go L1570–1575）；scheduler L1072 的 fallback 为 `"Pending"`；L425–455 在 NoFit、无抢占候选、目标重叠、不再 fit 时设置相应 reason |
| ClusterQueue 状态 | [v1beta2 clusterqueue_types.go](https://github.com/kubernetes-sigs/kueue/blob/911a822a49bcfd99c9c62203a009efa4130ad604/apis/kueue/v1beta2/clusterqueue_types.go) | `6092ac24e01b5e5546cc21c71fd626c1f0b35ca1249aac971029a0093de3dad9` | **属实**：`flavorsReservation`/`flavorsUsage`（L362–377） |
| 指标（未在正文引用） | [metrics.md](https://github.com/kubernetes-sigs/kueue/blob/911a822a49bcfd99c9c62203a009efa4130ad604/site/content/en/docs/reference/metrics.md) | `cd42760a27887720a9900baec9056b2fab7aa4ba9737dfa7ea06e1e1b4cc2c85` | `kueue_cluster_queue_resource_reservation`（L121）等存在；`kueue_unadmitted_workloads` 只在门控开启时发出（L69）。正文"指标 reservation/usage"没有出处。→ C30 |
| All-or-nothing 语义 | [workload.md](https://github.com/kubernetes-sigs/kueue/blob/911a822a49bcfd99c9c62203a009efa4130ad604/site/content/en/docs/concepts/workload.md)；[overview](https://github.com/kubernetes-sigs/kueue/blob/911a822a49bcfd99c9c62203a009efa4130ad604/site/content/en/docs/overview/_index.md) | `b6a40f7092a7f6b417408088c17efabf6318acbb223579ad91c1a5491659e6b1`；`ae08879409d38d1cdf7e6f34d136cdc471e0226279b5248ece37326d57a18db5` | workload.md L142–157：`evicted and re-queued if the job doesn't become ready`，PodsReadyTimeout 后按指数退避重排，`requeueState.count`/`requeueAt`。overview L33：`All-or-nothing with ready Pods: A timeout-based implementation`。所取 Kueue 页面中没有 "gang" 一词。→ C22、C28 |

### Slurm 24.11.7 归档（src.slurm.docs-24.11.7，复用）

| 页面 | SHA-256（原文） | 核对点与结果 |
|---|---|---|
| [reservations](https://slurm.schedmd.com/archive/slurm-24.11.7/reservations.html) | `ef52751124e893ee6de3eb69f8cb013952b9b02e33cd5fa402d856e66ab0e9a8` | **属实**：`not compatible with Slurm's gang scheduler plugin`；`must explicitly specify that reservation name`；`contained completely within the named reservation`。**与正文不符**：`created, updated, or destroyed only by user root or the configured SlurmUser`（正文写"仅 root"）。**正文未用**：`does not alter a job's priority, but it does act as an enhancement`，同分区内带预留的作业先被考虑；预留核/节点 `no other jobs can use those resources`。→ C26、C29 |
| [priority_multifactor](https://slurm.schedmd.com/archive/slurm-24.11.7/priority_multifactor.html) | `acd6dead998a88f63b06aa090571d29bd49f20449bcc9b811e5d69a63720f58d` | **属实**：`nine factors`。**正文未用或表述错乱**：评估顺序依次为 `Jobs that can preempt`、`Jobs with an advanced reservation`、`Partition PriorityTier`、`Job priority`、`Job submit time`、`Job ID`，且 `the job with the highest priority may not be the first to be evaluated`；fair-share 节：under-serviced 账户先调度，`does not involve a fixed allotment`。→ C26 |
| [qos](https://slurm.schedmd.com/archive/slurm-24.11.7/qos.html) | `f6b74df28881e89b2e056bd2f15c0059247f78a7dc979063b16f77b062e2ba5f` | **属实**：`three key ways: scheduling priority, preemption, and resource limits` |
| [job_reason_codes](https://slurm.schedmd.com/archive/slurm-24.11.7/job_reason_codes.html) | `f8e4f3c93113f0278d676d1177642b2e613223ca4f9905decf7e1b436281592a` | `Resources — The resources requested by the job are not available (e.g., already used by other jobs)`，页中没有"总量够但单节点放不下"。**与正文不符**：`ReqNodeNotAvail — Some node specifically required by the job is not currently available`；DOWN/DRAINED 节点在 reason 中显示为 `UnavailableNodes`。→ C27 |
| [gang_scheduling](https://slurm.schedmd.com/archive/slurm-24.11.7/gang_scheduling.html)（未登记） | `02a1c074cfc880d9161510cf0a9f9150fdae52fb7f400e5894035ddf5a2e06a1` | **属实**：`timesliced gang scheduling`，与正文 L130"Slurm gang scheduling（分时）"一致 |
| [topology](https://slurm.schedmd.com/archive/slurm-24.11.7/topology.html)（未登记） | `837dbf5e7bf35dda1dc0d173c68ce60028c950c201db3a42dc4a47c5be91d989` | `TopologyPlugin=topology/tree`，best-fit 选最低层交换机；`--switches` 可设最大叶交换机数与最长等待时间；`topology/block`。正文 Slurm 样板没有拓扑观测，且本页不在已登记范围。→ C23 |

### MindCluster v26.1.1（commit `44385c13`，src.ascend.mind-cluster-v26.1.1）

| 页面 | SHA-256（原文） | 核对点与结果 |
|---|---|---|
| [调度流程](https://github.com/Ascend/mind-cluster/blob/44385c13d7b1d87def35f1604e8be4d16de6ca4e/docs/zh/scheduling/04_usage/03_basic_scheduling/02_scheduling_process_of_the_ascend_ai_processor.md) | `3fd2a1eb276e11f5743f888da1418d98d33f4760c5bc3043c458761380a74558` | **属实**：L3 `华为在开源Volcano框架上进行适配修改的调度器`；L13 `self-maintain-available-card` 默认 true，L29 起为 false 时的另一条路径；Annotations、`predicate-time` 与 Allocate 对账（L52–62） |
| [芯片亲和性](https://github.com/Ascend/mind-cluster/blob/44385c13d7b1d87def35f1604e8be4d16de6ca4e/docs/zh/scheduling/04_usage/03_basic_scheduling/01_affinity_scheduling/03_ascend_ai_processor_based_affinity.md) | `f60845acb2225d85f87cf5ef6c83bec2ca93bd4e4a650f789a8b01503671a4f0` | **属实**：Atlas 训练系列双 HCCS 环（L7–9）；L16 `Atlas 800T A2 训练服务器和Atlas 900 A2 PoD 集群基础单元没有昇腾AI处理器的亲和性调度`；Box16（L18–20）；A3 HiAM 模组（L26–30、L42–46） |
| [交换机亲和性](https://github.com/Ascend/mind-cluster/blob/44385c13d7b1d87def35f1604e8be4d16de6ca4e/docs/zh/scheduling/04_usage/03_basic_scheduling/01_affinity_scheduling/04_node_based_affinity.md) | `d2bf8356acf79259058355e8ef038c87959a2935df3274382fd2486e2bb20b8a` | 可达且为对应主题页；本轮未逐条核对内容 |

取证限制：

- 先尝试对 Volcano 与 Kueue 做浅克隆以便全仓检索，因速度过慢中止并删除了部分克隆，改为按固定 commit 逐文件取回。因此"某符号在全仓不出现"这类结论只覆盖上表所列文件。例如 `MinResources` 的使用方是按 enqueue、allocate 与三个插件文件 grep 得到的，没有遍历全部插件。
- 一次 Slurm 取回遇到 `SSL_ERROR_SYSCALL`，重试后 200，哈希与 T05-03 初审所记一致。
- Volcano 文档站是可变网页，所记哈希只代表本次观察，不能代替固定 revision。HTML 均按去标签文字核对。
- 只读了上表所列行区间。statement.go 的 Commit/Discard 内部、gangreclaim 细节、proportion/capacity/overcommit 的 `JobEnqueueable` 判定公式、Kueue `preemption.md`/`cohort.md` 与 flavorassigner 实现都没有审计。测试只读用例名，没有运行。
- 许可：gang.go 文件头为 Apache License 2.0（L10–20），Volcano 仓库根 LICENSE 没有打开；Slurm 站点许可未核。

## 发现

### B22-C22 — P1 / OPEN：启动失败、重排队与回退整体记为 unknown，但同一 tag 中可读

位置：正文 L75 末句；`verification.notes`（L29）；来源记录 L9 支持范围、unknown 第 1 条（L16）；登记 L5468、L5473。对应 acceptance 1"启动失败、重排队/回退"与 source_discovery L5582（`核对 gang 失败和回滚路径`）。

证据：

- **调度会话内的回退**：allocate.go L313–322、L329–336 只有在 `ssn.JobReady(job)` 时才 `stmt.Commit()`；L832–844 中，SubJob 既不 ready 也不 pipelined 时 `stmt.Discard()`。部分分配在会话内撤销，这正是成组决策的"回退"。它在 allocate 动作中，不在 gang 插件，也不在 job 控制器。
- **入队门**：enqueue.go L95–99 以 `MinResources` 与 `JobEnqueueable` 决定 Pending→Inqueue；allocate.go L152–169 在配置了 enqueue 时跳过仍为 Pending 的 PodGroup，`JobValid` 不通过的作业也被跳过。PodGroup 文档把 `inqueue` 写成 pending 与 running 之间的过渡态。
- **启动失败与重排队（控制器）**：
  - handler L273–281：Pod 转 Failed 产生 `PodFailedEvent` 并带退出码。
  - `applyPolicies`（util L182–284）：默认只做 `SyncJobAction`；task/job 级 policy 按事件或 exitCode 映射到 RestartJob/RestartTask/AbortJob 等；`PodPendingEvent` 须配 `Timeout`（L286–288），可用来处理长时间 Pending 的启动失败。
  - running.go L35–45：Restart* 杀 Pod、转 Restarting、`RetryCount++`。restarting.go L35–47：达到 `maxRetry` 转 Failed，否则转回 Pending。running.go L107–108：Pending 的 Pod 数超过 `replicas − minAvailable` 时 job 转回 Pending。
- **部分运行态**：PodGroup 文档 phase `unknown`：minMember 中部分在运行、部分未调度，调度器会等 ControllerManager 重新拉起这些 Pod。所谓"成组"并不保证启动后仍成组。
- **会话级重试计数**：gang.go L256 每次会话结束对 gang 不可调度的作业调用 `metrics.RegisterJobRetries`。这是调度重试，不是 job 控制器的 `RetryCount`，两者不能混读。
- **Kueue 侧**：任务 objective 写的是"补齐 Kueue/Volcano 组调度失效/回退"。Kueue 的对应机制是 workload.md L142–157 的 PodsReady 超时驱逐与指数退避重排（`requeueState`）。T05-02 正文 L115 已写，本文没有引用。
- 以上都是只读源码与文档层证据。作者只取了 `gang.go` 一个文件，source_discovery 要求的"代码/测试"和"回滚路径"没有完成；gang 插件目录本身没有测试文件（404），可用的是 allocate_test、enqueue_test 与 `TestApplyPolicies`。

关闭条件：

- 新增"失败与回退分层"表，至少分五层，逐行引 file@commit 与行区间，并注明只读未执行：
  1. 入队：`minResources` 与 `JobEnqueueable`，Pending→Inqueue，由哪些插件提供判定取决于调度器配置。
  2. 会话内成组决策：JobValid 跳过；JobReady 时 Commit；pipelined 时保留不提交；否则 Discard。
  3. 会话关闭：写 Unschedulable/Scheduled 条件；`RegisterJobRetries`。
  4. 控制器：Pod 事件→policy→Restart*/Abort/Terminate，`RetryCount`/`MaxRetry`，Running→Pending 回落。
  5. 应用 rendezvous：不在 Volcano 范围。
- Kueue 一行引 T05-02 L115 与 workload.md，说明 PodsReady 超时驱逐与退避重排。
- 把 unknown 收窄为真正未取证的项，例如：站点启用了哪些 action/plugin、未写 policy 时的实际行为是否只有 Sync（需结合 webhook 默认值核对）、Pod 删除与重建的时序。正文、来源记录与登记 notes 同步更新。

### B22-C23 — P1 / OPEN：两个样板缺资源向量、拓扑、碎片与运行进展的观测，也没有对照验收

位置：正文 L122–130；acceptance 3。

证据：

- acceptance 3 要求**每个**样板说明资源向量、拓扑、碎片、配额与运行进展的观测，并给出失败或不适用反例及对照验收。现状如下：

  | 维度 | 样板 A（Kueue，L124） | 样板 B（Slurm，L128） |
  |---|---|---|
  | 资源向量 | 未写。只有"每资源设 nominalQuota"，没有说明 PodSet count × 每 Pod 请求的多资源核算，也没有说明 resourceGroup 的 `coveredResources` 要求同组资源同 flavor | 未写 TRES/GRES 请求向量 |
  | 拓扑 | 未写。本页 L71、L100 讲过 TAS，样板没有接上；`TopologyPlacementFailed`（workload_types L956–958，门控开启时可见）未用 | 未写。topology.html 有 `topology/tree`/`topology/block` 与 `--switches`，但该页未登记 |
  | 碎片 | 未写。Kueue 配额是逻辑账本，配额 fit 不代表节点无碎片；这正是本页 L83–89 的例子，样板没有关联 | 有一句"总量够但单节点放不下→Pending（Resources）"，但 Resources 释义不含此推论（见 C27） |
  | 配额 | 有：flavorsReservation/flavorsUsage | 规则中提到 QOS 限额，观测未写对应 reason（QOS*/Assoc* 系列） |
  | 运行进展 | 未写。`PodsReady` 在 L67 定义过，样板没有用；Admitted 不代表运行进展 | 未写。`R` 状态不证明应用进展 |
  | 对照验收 | 只链接 T05-02 | 只链接 T05-03 |

- "对照验收"应当是可判定的预期，例如"同配置下请求不超过 nominalQuota 的负载应得到 `QuotaReserved=True`、`Admitted=True`"作正例，与反例配对。只放一个站内链接不能代替。

关闭条件：每个样板补一张"维度 × 观测字段/命令 × 来源 × 不能推出什么"表，覆盖上述五个维度。各配至少一个失败或不适用反例，以及正反配对的对照验收（写明预期字段值与判定方式，标"设计，未执行"）。Slurm 拓扑或者登记 topology.html 后引用，或者记 unknown。不得把文档默认行为写成站点结论。

### B22-C24 — P2 / OPEN：`minResources` 被归给 gang 插件；调度器 Ready 的口径未按实现写明

位置：正文 L79（"Gang 插件据此避免……"）、L75（`validJobFn`/`jobReady`/`pipelined` 的转述）、L77/L81。

证据：

- gang.go 全文不引用 `MinResources`。插件只用 `MinAvailable`、task 级 `TaskMinAvailable` 与 SubJob 约束（L58–93、L191–219；job_info.go L1025–1055）。
- `minResources` 的实际使用方：enqueue 动作（enqueue.go L95–99），以及 proportion/capacity/overcommit 插件（入队与容量判定）。job 控制器按 `minAvailable` 计算并同步 PodGroup 的 `minResources`（job_controller_actions.go L816、L877–880、L923）。enqueue_test L112 是对应的上游用例。由此看，`minMember` 主要在会话内的成组决策中起作用，`minResources` 主要在入队阶段起作用（审阅者归纳，依据上述文件，不代表全仓穷举）。
- 调度器的 "Ready" 不等于运行：`ReadyTaskNum`（job_info.go L877–886）把 Allocated（会话内暂分配、未绑定）与 Succeeded 计入；`IsReady` 还加上 Pending 的 BestEffort 任务（L1202–1204）。gang 插件写的 `PodGroupScheduled` 只表示 `tasks in gang are ready to be scheduled`。这些是"调度器 Ready ≠ 应用 rendezvous"最直接的实现证据，正文没有用。
- 文档与实现不一致：Gang 文档说 Ready 状态包含 Pipelined，`ReadyTaskNum` 并不计 Pipelined。acceptance 1 要求以实现为准，这类差异应写出来。
- `NotEnoughPodsReason` 来自 `ValidTaskNum < MinAvailable`，而 `ValidTaskNum` 把 Pending 的 Pod 也计入（L1130–1142）。它表示"作业已有的 Pod 对象不够"（例如控制器尚未创建或重建），不是资源不足。正文"按任务有效性拒绝"没有讲出这个区别，而这个区别正好关联启动失败场景。

关闭条件：L79 改为"`minMember` 由 gang 插件在会话内判定，`minResources` 在入队阶段由 enqueue 与配额类插件使用"，逐项引 file@commit。写明 Ready 的实现口径（含 Allocated/Succeeded、不含 Pipelined）及其与文档的差异。说明 `NotEnoughPodsReason` 与 `NotEnoughResourcesReason` 的区别。`jobReady` 不是函数名，改为 `AddJobReadyFn`。

### B22-C25 — P2 / OPEN：抢占保护"只在 ready 数高于 MinAvailable 时才允许"只对旧动作成立

位置：正文 L75"抢占/回收函数只在被抢作业 ready 数高于 `MinAvailable` 时才允许拿走任务"。

证据：

- gang.go L97–129 的 `preemptableFn` 只注册给 `AddReclaimableFn`/`AddPreemptableFn`，供 preempt/reclaim 动作使用。
- 同文件 L131–137 对 GangReclaim/GangPreempt 注册了 `AddUnifiedEvictableFn`，`the plugin permits all candidates here`，由 bundle 模型处理 MinAvailable。
- factory.go L36–43 在 v1.15.0 注册了 gangpreempt/gangreclaim 动作；gangpreempt.go L32–52 `allowWholeBundle` 默认 `true`，允许整作业作为 victim bundle。
- 因此在启用 gangpreempt/gangreclaim 的配置下，被抢作业可能整体被驱逐，正文的"只在……才允许"会让读者误以为 gang 作业不会被抢到 MinAvailable 以下。站点启用了哪些动作取决于调度器配置，属于 unknown。

关闭条件：按动作分别写：旧 preempt/reclaim 保留 MinAvailable；gangpreempt/gangreclaim 采用 bundle 模型，默认允许 whole bundle。注明启用哪些动作取决于站点配置（unknown），并引上述文件与行区间。

### B22-C26 — P2 / OPEN：选择依据读起来像产品推荐，公平性代价在两个样板中都不准确

位置：正文 L124"选择依据……时用 Kueue；公平性代价……"；L128"选择依据……时用 Slurm；公平性代价：priority/Tier/预留优先于单纯 priority 排序"；L128"admission 规则"；acceptance 2、acceptance 4。

证据：

- **Kueue 公平性代价**：
  - "借用方在对方需要时被收回（reclaim）"只在 `reclaimWithinCohort` 不为 `Never` 时成立。三个抢占字段默认都是 `Never`（cluster_queue.md L443、L459、L469）。默认配置下，cohort 只是优先接纳 nominalQuota 内的新负载（L248、L304–307），已在运行的借用方不会被回收。
  - Kueue 自己的公平机制 Fair Sharing（L6、L14、L446–452），以及它与 `borrowWithinCohort` 互斥（L457），正文都没有提。
- **Slurm 公平性代价**：
  - "priority/Tier/预留优先于单纯 priority 排序"无法对上原文。原文评估顺序为可抢占作业 → 带预留作业 → 分区 PriorityTier → job priority → 提交时间 → job ID（priority_multifactor），并说明最高 priority 的作业不一定最先被评估。
  - 公平性的主要机制 fair-share 没有写：under-serviced 账户先调度，不是固定配额。
  - 预留的代价没有写：预留核/节点 `no other jobs can use those resources`；预留不改 priority，但同分区内带预留的作业先被考虑（reservations 页）。
- **选择依据**："需借用与抢占语义时用 Kueue"与"需预留与 QOS 限额时用 Slurm"不能区分两者。L128 自己写了 QOS 的作用包括抢占，Slurm 同样有抢占。两者实际的分界是工作负载所在的平台（Kubernetes 还是 Slurm），以及站点是否已有相应基础设施。"……时用 X"的句式读起来像推荐，与 L134"本文示例不是推荐所有平台的统一策略"和 acceptance 4 有张力。
- **Slurm 样板缺少配置/状态字段**："admission 规则"只是概念罗列，没有给出 acceptance 2 要求的"配置/状态样板"所需的参数名，例如 `PriorityWeight*`、分区 `PriorityTier`、`PreemptType=preempt/qos`、QOS 限额字段、预留 flags；样板 A 至少列出了字段。

关闭条件：

- 选择依据改为"适用前提"：所在平台、已有的队列/账户体系、需要哪些语义。两个平台都具备的能力（如抢占）不作区分依据。删去"时用 X"句式。
- Kueue 代价写明 reclaim 只在非 Never 时成立、默认 Never，并补 Fair Sharing 与 StrictFIFO 的代价。
- Slurm 代价按评估顺序重写，补 fair-share 与预留独占的代价。
- Slurm 样板补配置/状态参数名，逐项引归档页。

### B22-C27 — P2 / OPEN：失败反例的触发条件与 reason 不精确

位置：正文 L124 两个 Kueue 反例；L128 两个 Slurm 反例。

证据：

- **Slurm `ReqNodeNotAvail`**：原文为 `Some node specifically required by the job is not currently available`，DOWN/DRAINED 节点在 reason 中显示为 `UnavailableNodes`。只有作业明确指定的节点不可用时才是这个 reason；一般作业遇到节点 DOWN/DRAIN，只是可用容量减少。正文"节点 DOWN/DRAIN→ReqNodeNotAvail"漏了这个前提。
- **Slurm Resources**：原文只说 `The resources requested by the job are not available (e.g., already used by other jobs)`。"总量够但单节点放不下"是本库推论（T05-03 初审 C21 已对同类说法提出过同样要求），应标为推论。
- **Kueue"flavor 名额够但 cohort 被占满→Pending"**：按 cluster_queue.md L235–236 规则 1 的字面意思，ClusterQueue 自身未用的 nominalQuota 足够即 fits。反例要成立，必须写明前提：本 CQ 的名额已被借出且仍在使用，`lendingLimit` 未设。此时的行为取决于 `reclaimWithinCohort`：为 `Never` 时等待，否则可回收抢占。审阅者未核对 flavorassigner 实现，这一前提下的确切 reason 没有取证，应记 unknown 或补证。
- **Kueue"借超 borrowingLimit→不准入"**：这里有两种不同情况。请求本身超过 nominal+borrowingLimit 时永远不能满足，细分 reason 为 `ExceedsMaxQuota`（workload_types L951–954）。当前已借量加本次请求超限时，是等待 `WaitingForQuota`。门控关闭时两者都只显示 `Pending`，正文没有区分。

关闭条件：Slurm 反例改为"作业指定节点（如 `--nodelist`）不可用 → ReqNodeNotAvail/UnavailableNodes"，"总量够但单节点放不下"标为推论。Kueue 反例写明前提与 `reclaimWithinCohort` 的分支，并区分 `ExceedsMaxQuota` 与 `WaitingForQuota`，注明门控关闭时只见 `Pending`。

### B22-C28 — P3 / OPEN："Kueue gang（成组准入）"不是来源术语

位置：正文 L130。

证据：所取 Kueue 页面中没有 "gang"。Kueue 的对应机制叫 `All-or-nothing with ready Pods`，并明说是 `timeout-based implementation`（overview L33），语义是作业未就绪即驱逐并重排（workload.md L142–145）。本库 [Slurm 参考](../../knowledge/05-cluster-platform/slurm-jobs-and-device-resources.md) L28 的写法是"Volcano/Kueue 的全有或全无成组调度"。L130 这句本意是防止同名术语混用，却引入了来源中没有的术语，而且"成组准入"没有涵盖超时驱逐与重排。

关闭条件：改为来源术语。Kueue 写成"Workload 整体配额预留，加上可选的 waitForPodsReady 超时驱逐与退避重排"，并引 T05-02 L115。

### B22-C29 — P3 / OPEN：结构与措辞

位置：正文 L75、L77、L81、L118、L124、L128、L134。

证据与改法：

- L77 与 L81 两段逐字相同，删去一段。L75 的实现细节放在 L79 的概念定义之前，建议先概念、后实现。
- L128 行首有空格，"admission 规则"与 L124 的"准入规则"不统一。
- L118"来源差异……见[本批 F12 研究记录]"链到 batch-05 的文件，而本次修订的来源记录 `batch-22-t05-05-sources.md` 没有从正文链接。"本批"已不准确。
- L124"抢占分……三档"：三者是三个独立字段，不是三个档位。
- L75 消息 `x/y tasks in gang unschedulable` 中，x 为 `MinAvailable` 减可调度数，y 为 `len(job.Tasks)`（全部任务数，不是 minMember），读者容易误读，建议注明。
- L128"仅 root 建"：原文为 root 或配置的 SlurmUser。
- L134"再用本页样板确认配额/放置/设备三层"：两个样板都不涉及设备层，这句说多了。

关闭条件：逐条修正。

### B22-C30 — P3 / OPEN：版本锚、登记、元数据与就近引用

位置：登记 L5463–5484；正文 frontmatter L8–29；正文 L124、L128；来源记录 L7–12。

证据：

- `src.volcano.gang-plugin-v1.15.0` 的 revision 只写了 `tag v1.15.0`，URL 也用 tag（可变引用）。实际 tag 对象为 `4691eac3…`，指向 commit `8fc394c11e8db0d0ada5c17816b58bced9d7213d`，可以补上。license 写"Apache-2.0 未在本轮打开核对"；gang.go 文件头有 Apache 2.0 声明（L10–20），仓库根 LICENSE 审阅者也没有打开，只作提示。
- `src.kueue.cluster-queue-v0.19.0` 与既有 `src.kueue.admission-v0.19.0`（L559–572）是同一 commit。后者 notes 已写第八批读过 `concepts/cluster_queue.md 与 cohort.md`，并按根 LICENSE 登记了 Apache-2.0；新条目却把 license 记为 unknown。两条在覆盖范围上重叠，许可口径也不一致。
- frontmatter `verification.evidence_refs` 没有本次新增的两个 ID，也没有 Slurm 两个 ID，`notes` 却写已核对。`related_ids` 缺正文已链接的 `cluster-platform.kubernetes-job-lifecycle`、`cluster-platform.slurm-jobs-and-device-resources`、`cluster-platform.idle-resource-job-waiting-triage`。
- 就近引用：L128 的 Slurm 主张（九因子、QOS 三作用、预留权限与 gang 不兼容、ReqNodeNotAvail）旁边没有归档页链接，只链了站内参考页。L124 的指标说法没有出处（metrics.md L121 等）。AGENTS.md 要求在实质主张附近引用精确页面或 revision。
- 来源记录没有写取证方法（curl 还是 webfetch），没有哈希，也没有行区间；Slurm 与 MindCluster 只写"复用"，正文却新增了 Slurm 主张。

关闭条件：登记补 tag 对象与 commit，URL 改用 commit。两条 Kueue 登记合并，或写明分工并统一许可口径。frontmatter 补 evidence_refs 与 related_ids。L124/L128 就近加归档页、metrics.md 链接。来源记录补取证方法、行区间，以及新增 Slurm 主张对应的页面。

## acceptance 对照

| acceptance | 判定 | 相关发现 |
|---|---|---|
| 1 以固定 Volcano 实现解释 minMember/minResources、成组决策、启动失败、重排队/回退及与 rendezvous 的不同 | 部分满足。成立的部分：gang 插件的校验、条件上报、"Ready 不是 rendezvous"的方向。缺口：启动失败/重排队/回退整体记为 unknown，而同一 tag 可读；minResources 归属错误；抢占保护说过头；只取了一个文件，没有核对测试 | C22（P1）；C24、C25（P2） |
| 2 Kueue 与 Slurm 两个独立配置/状态样板；选择依据与公平性代价分开 | 部分满足。成立的部分：两个样板分开写，字段名大体属实，标签分开。缺口：Kueue 回收代价忽略默认 Never 与 Fair Sharing；Slurm 公平性代价表述混乱、缺 fair-share；选择依据不能区分两者且读起来像推荐；Slurm 缺配置/状态字段 | C26（P2）；C28（P3） |
| 3 每个样板的资源向量、拓扑、碎片、配额、运行进展观测，失败或不适用反例及对照验收 | 大部分未满足。两个样板都只有配额观测与反例；资源向量、拓扑、运行进展缺失；对照验收只有链接；反例的前提与 reason 不精确 | C23（P1）；C27（P2） |
| 4 MindCluster 边界；链接 idle-resource-job-waiting-triage 与 Slurm 状态参考；不是统一推荐策略 | 基本满足。MindCluster 三份一次源抽查一致，两个链接都在，有"不是统一策略"的声明，没有写成已验证的部署指南。附带问题："时用 X"句式（见 C26），L134 说样板覆盖设备层（见 C29） | C26（P2）；C29（P3） |

横向问题：作者只读了 gang 插件一个文件，把读不到的部分统一归为"job 控制器职责（unknown）"。实际上回退在 allocate 动作，入队门在 enqueue 动作与配额类插件，重排队在 job 控制器，这几处都在同一 tag 中可读。可取证的内容被记为 unknown，这与 T05-03 初审横向问题中指出的偏差属于同一类。

范围外观察（不计入本轮发现）：cluster_queue.md 的 cohort 一节文字写 `.spec.cohort`（L216–218），同页 v1beta2 示例用的却是 `cohortName`（L267）。这是上游文档自身的不一致，后续引用 cohort 字段时需要按 API 类型核对。

## 结论

**T05-05 初审不通过，需修订。B22-C22–C30 共 9 项：P1 ×2（C22、C23），P2 ×4（C24–C27），P3 ×3（C28–C30），全部 OPEN。**

- 修订后须按各项关闭条件做定向复核。
- C22–C25 关闭前，正文 `verification.status: source_checked` 对 Volcano 部分不应视为成立：其中实现归属与抢占语义两处与所引代码不符，回退路径的取证没有完成。
- 正文没有虚构命令输出或实测结果，`verification.notes` 如实写明未部署、未提交、未验证；MindCluster 边界保持得当。
- 本审阅只覆盖编辑与来源层面。文中 Volcano/Kueue/Slurm 的行为都是源码、测试源码或文档层证据，审阅者未部署、未运行，不得标为 reproduced。

## 检查记录（作者机械补记，审阅者原写被拒）

- 成稿前复取输入哈希：四个输入与"输入"表一致（审阅者已核，作者侧当前正文/记录已修订，哈希见复核任务）。
- `make check`：成稿前基线为 `PASS: 96 content entries; 442 sources.`（审阅者记录）；本补记时重跑为 `PASS: 96 content entries; 444 sources.`，差值为 scheduler-actions/job-controller 两个 volcano 登记条目，以实时运行为准。
