# 第二十二批 T05-05 第二次定向复核（作者第二轮修订后）

复核日期：2026-10-15。

**结论：定向复核不通过。本轮范围 8 项（B22-C22–C27、C29、C30）：CLOSED 2（C26、C27），OPEN 6（C22、C23、C24、C25、C29、C30）。连同前轮已关闭的 C28，B22-C22–C30 共 9 项：CLOSED 3，OPEN 6。本轮不新增发现 ID。**

作者本轮新写的实质内容，抽查一次源后全部属实：allocate 跳过 Pending 的前提、调度器 Ready 实现口径及其与文档的差异、控制器同步 PodGroup 的出处、Fair Sharing 代价、`GrpTRES`/`FLEX`、`nominalQuota + borrowingLimit` 阈值与门控回退。正文 13 个 Volcano 链接已全部改为 commit。本轮没有发现新的事实错误。

仍 OPEN 的 6 项都不是事实问题，而是修订映射所列改动没有全部落盘：

1. **映射写了，文件里没有**：C23 两条关闭条件都没落地（样板 B 正文 L169 未改，L150 来源列未改）；C24 的 job_controller_actions.go 没有纳入登记；C30 两条新登记的 URL 仍是 `blob/v1.15.0`，job-controller 登记没有补 tag 对象；C25 正文与来源记录都没有 gangreclaim.go 的行区间。
2. **部分落地**：C22 表中三处证据位置仍缺行区间；C29 L139 改掉了"许可范围"，"来源差异"仍与来源记录内容不符。
3. **本轮新引出处未登记**（按 C30 原 ID 追记）：正文 L88 新引的 `pkg/scheduler/api/job_info.go` 不在任何登记条目的 revision 范围内，来源记录也没有列出。

修订映射标题注明"只列落盘改动，逐条 grep 已核对"，但下文"修订映射与落盘差异"一节列出 7 条不符。各项剩余工作都是改一句话、补一个行区间或改一个 URL。

审阅者角色独立于作者。审阅模型为 `claude-opus-5-5`，由用户本次明确要求试用；这不是既有的 `gpt-6.1-sol / xhigh` 批量审阅约定，也不改写该约定。本轮未出现 `[frontier_llm]` 标记、模型不一致或认证失败；推理等级等运行元数据没有可核验记录，不补造。本轮只做只读取证和审阅：只写本报告；未改作者正文、来源记录、登记、修订映射或计划；未部署 Volcano/Kueue/MindCluster/Slurm，未提交作业，未运行任何上游测试。模型审阅不构成平台或现场验证。

## 输入（以 SHA-256 识别）

| 输入 | SHA-256 |
|---|---|
| [T05-05 正文](../../knowledge/05-cluster-platform/admission-and-placement.md)（177 行） | `213339608097769eb4069d85a1d6b07b073558b95651e801cf49a7a796b34677` |
| [作者来源记录](batch-22-t05-05-sources.md)（18 行） | `543bdea004b6626afed02d10d8af78756036733a5b633057ffe3f9649fa6a2c5` |
| [修订映射](batch-21-review-fixes.md)（T05-05 第二轮修订节 L367–376） | `a7ad28f3dd627c42a8736804194da00dda3b1ef913f0e4532cf38635ce0e7aa8`；L367–376 段 `a8139dd362db46afbc4a1a3cb2e6dab95be60d77aea264df52b2aec93944929d` |
| [来源登记](../../sources/registry.yaml)（444 项；T05-05 相关 L5463–5509） | `fe34a22d15545d91e4c64341586751dfe1bdf2f6b9bbb99e2d7197d2951fa30f`；L5463–5509 段 `26e70df2cd37acc7235a68a57a616c60cd6315455917ac26d757c6c038384196` |
| [前次复核报告](batch-22-t05-05-claude-recheck.md)（剩余关闭条件权威来源） | `725ac99560bf3f22c8fea38f743649c158ee9200e85428d9ab9299d0ac3aaceb` |
| [初审报告](batch-22-t05-05-claude-review.md) | `2095a6fe21717e2ef9ce6977e79c197e72ca11f1000904ad229f80dbf098cde1` |
| [任务计划](../../plans/full-coverage-backlog.yaml)（T05-05 acceptance L5569–5573） | `5f9bcf865b8c77e13cc8ee5f1c03140c37b86f558d8227d8bb2080249f4fcfc3` |

任务给出的四个前缀（正文、来源记录、修订映射、登记）均一致。七个输入在开始时取哈希，成稿前复取一次，结果相同（见文末）。

## 一次源抽查（审阅者独立获取）

方法：全部用 `curl -sSL` 默认 TLS 校验只读获取，HTTP 均为 200，本轮没有重试或失败。GitHub 文件经 `raw.githubusercontent.com` 按固定 commit 取回。为在 Kueue 全仓检索门控用法，另用 curl 从 `codeload.github.com` 取回同一 commit 的源码包（22,498,653 字节）；包内 `apis/kueue/v1beta2/workload_types.go` 与 raw 单独取回的文件逐字节相同（`cmp` 通过）。HTML 去标签后按文字核对，不只判可达性。版本锚用 `git ls-remote`。原文只放在临时目录 `/tmp/b22rc05b/`，未入库。

版本锚：Volcano `refs/tags/v1.15.0` 为 tag 对象 `4691eac388eb8ec033908cbe144b8f3aafcaeef7`，`^{}` 指向 commit `8fc394c11e8db0d0ada5c17816b58bced9d7213d`；Kueue `refs/tags/v0.19.0` 为 tag 对象 `7b3cad14a540cd256dc9c658be5a23fff809ff68`，指向 commit `911a822a49bcfd99c9c62203a009efa4130ad604`。与前两轮及登记一致。

与前次复核重叠的 21 个文件/页面，本轮取回的 SHA-256 全部与前次相同，说明上游内容没有变化，判定差异都来自作者修订。下表"同前次"即哈希逐字相同。

### Volcano（commit `8fc394c1`）

| 文件 | SHA-256 | 核对点与结果 |
|---|---|---|
| `pkg/scheduler/actions/allocate/allocate.go` | 同前次 `7eefa6ac…bc632` | L152–163：`job.IsPending()` 时，`conf.EnabledActionMap["enqueue"]` 为真则 `continue`；否则日志 `no enqueue action is configured`，就地改为 `PodGroupInqueue` 并继续。L166–169 `JobValid` 不通过 `continue`。L314、L330 `stmt != nil && ssn.JobReady(job)` 才 `Commit`（注释 `do not commit stmt when job is pipelined`）；L319–321、L333–335 注释 `There are still left tasks that need to be allocated when min available < replicas, put the job back`，有剩余任务才 `jobs.Push(job)`。L832–844 SubJob 不 ready 不 pipelined 则 `stmt.Discard()`。**正文 L95 属实**（C22） |
| `pkg/scheduler/actions/enqueue/enqueue.go` | 同前次 `38b8feb1…f2cde` | L95–99 `MinResources == nil \|\| ssn.JobEnqueueable(job)` 时转 `PodGroupInqueue`。正文 L94 属实，但正文未给行区间（C22） |
| `pkg/scheduler/plugins/gang/gang.go`（297 行） | 同前次 `9f3fe992…a2159` | L97–125 `preemptableFn`：`jobOccupiedMap` 初值为 `job.ReadyTaskNum()`，`> job.MinAvailable` 才逐个放行；L127–129 注册给 Reclaimable/Preemptable；L131–137 `AddUnifiedEvictableFn`，注释 `Currently handles GangReclaim and GangPreempt only`、`permits all candidates`。L191 `AddJobReadyFn` 至 L211 `AddJobPipelinedFn`。L229–297 `OnSessionClose`；L250–252 消息 x/y；L256 `RegisterJobRetries`。全文 `MinResources` 0 处。**正文 L88、L96 属实，行区间正确**（C24、C25） |
| `pkg/scheduler/actions/gangpreempt/gangpreempt.go` | 同前次 `440e6ff3…1694d` | L33 `AllowWholeBundleKey`、L37 `defaultWholeBundleOn = true`、L48–52 `New()` 采用默认；L70 `arguments.GetBool` 覆盖；L248 `bundle.Type == utils.BundleWhole && !gp.allowWholeBundle` 才跳过。**正文 L88 行区间 L32–52、L248 正确**（C25） |
| `pkg/scheduler/actions/gangreclaim/gangreclaim.go` | 同前次 `56b00681…66982` | 结构相同：L37 默认 `true`，L48–52 `New()`，L70 覆盖，**L247**（不是 L248）跳过判定。正文 L88 结论属实，但正文和来源记录都没有行区间（C25） |
| `pkg/scheduler/api/job_info.go` | 同前次 `e8d19400…5823b` | L877–886 `ReadyTaskNum` 计 Bound/Binding/Running/Allocated/Succeeded；L1202–1204 `IsReady` = `ReadyTaskNum + PendingBestEffortTaskNum >= MinAvailable`；L1206–1208 `IsPipelined` 另加 `WaitingTaskNum`。**正文 L88 新增 Ready 口径属实，行区间正确**；该文件不在任何登记范围内（C24、C30） |
| `pkg/controllers/job/job_controller_actions.go` | 同前次 `c2bc5da7…aaaed2` | L813 `MinMember: job.Spec.MinAvailable`、L816 `MinResources: cc.calcPGMinResources(job)`；L877–880 不一致时同步两字段。**正文 L88 新增引用属实，行区间正确**；登记 L5504 仍未列入（C24、C30） |
| `pkg/controllers/job/state/running.go` | 同前次 `97cadbe2…74544` | L35–46 Restart* → Restarting、`RetryCount++`；L107–110 `status.Pending > jobReplicas − MinAvailable` 回 Pending。正文 L97 属实，正文未给行区间（C22） |
| `pkg/controllers/job/state/restarting.go` | 同前次 `954f7fb4…10f6a` | L35–40 `RetryCount >= maxRetry` → Failed；L46–49 `total − Terminating >= MinAvailable` → Pending；L51 `return false`。正文 L97 已补该条件，属实 |
| `pkg/controllers/job/job_controller_util.go` | 同前次 `e9632a06…e070b` | L190–191 `default action is sync job`；L194–197 请求自带 action 时直接采用；L286–288 只有 `PodPendingEvent` 需配 Timeout。正文 L97 属实，正文未给行区间（C22） |
| [Gang 文档](https://volcano.sh/docs/v1.15.0/scheduler/plugins/gang/) | 同前次 `6a39b97d…d1ec26b`（可变网页，仅本次观察） | 页头 `Version: v1.15.0`；原文 `considers tasks not in the Ready state (including Binding, Bound, Running, Allocated, Succeed, and Pipelined)`。正文 L88"Gang 文档把 Pipelined 列入 Ready，与实现不一致，以实现为准"属实 |

另取回 `pkg/scheduler/framework/session_plugins.go`（`a573e705a4547ae8a1114c7f6fbbe469c392526b3448aed5964903cb0fbdbd25`），未用于判定。

### Kueue（commit `911a822a`）

| 文件 | SHA-256 | 核对点与结果 |
|---|---|---|
| `site/content/en/docs/concepts/cluster_queue.md` | 同前次 `7b35c9f7…0b346` | L233–242 fit 规则 3：上限为未用的 `nominalQuota + borrowingLimit`。L440–443 `reclaimWithinCohort` 默认 `Never`；L444–452 `LowerPriority`/`Any` 在 Fair Sharing 下只抢 `satisfy the Fair Sharing preemption strategies` 的负载。L454–457 `borrowWithinCohort` `not with Fair Sharing`。**正文 L145、L155 属实，L444–452 区间正确**（C26、C27） |
| `apis/kueue/v1beta2/workload_types.go` | 同前次 `50b9523e…c4dc1` | L947–949 `WaitingForQuota`；L951–954 `ExceedsMaxQuota`（`This also includes exceeding ClusterQueue nominal + borrowingLimit constraints`）；L956–958 `TopologyPlacementFailed`（`topology requirements that cannot be satisfied with the current cluster topology usage`） |
| `pkg/features/kube_features.go`（本轮新取） | `225c13d60dcff1372b08855b51a9eb2ac1a6b05cc8a348f42a455e50ff8de02d` | L479–481 `UnadmittedWorkloadsObservability`：`updates status reasons for QuotaReserved/Admitted conditions to use tiered reasons`；L788–789 v0.19 `Default: false, PreRelease: Beta` |
| `pkg/workload/workload.go`（源码包内，本轮新取） | `ccbff32a67a89ae37ca0e157f8a0daa91c7a85627f12802ae6a5a989f95bc41d` | L1568–1575 `UnadmittedWorkloadReasonWithFallback`：门控开启返回细分 reason，否则返回 fallback。各调用点 fallback 为 `kueue.WorkloadPending`（如 `pkg/controller/jobframework/reconciler.go` L578）；`pkg/util/testing/observability.go` 的门控关闭模拟把其余 `QuotaReserved=False` reason 归为 `Pending`（测试辅助，仅作旁证）。**正文 L149、L152、L155"开门控可见，否则只见 `Pending`"属实**；但正文全文没有写出门控名（0 处） |
| `site/content/en/docs/concepts/topology_aware_scheduling.md` | 同前次 `371b15e9…5ba3f35` | 本页、cluster_queue.md、metrics.md 都不含 `TopologyPlacementFailed`（0 处），已取回 Kueue 文件中只有 workload_types.go 含该词。**正文 L150 来源列"同上＋TAS 文档"仍错位**（C23） |
| `site/content/en/docs/reference/metrics.md` | 同前次 `cd42760a…c2c85` | L69、L95 `kueue_unadmitted_workloads*` 只在该门控开启时发出 |

登记旁证：`src.kueue.admission-v0.19.0` notes（L572）已写明第八批读取了同一 commit 的 v1beta2 workload_types.go 与 kube_features.go（含该门控），C23 修正 L150 来源无需新增登记。

### Slurm 24.11.7 归档（src.slurm.docs-24.11.7）

| 页面 | SHA-256 | 核对点与结果 |
|---|---|---|
| [qos](https://slurm.schedmd.com/archive/slurm-24.11.7/qos.html) | 同前次 `f6b74df2…2ba5f` | `GrpTRES set to the desired resource limits`；`DenyOnLimit — If set, jobs using this QOS will be rejected at submission time if they do not conform to the QOS 'Max' limits as stand-alone jobs`。正文 L171 `GrpTRES` 属实；`DenyOnLimit` 与 C23 配对前提有关 |
| [reservations](https://slurm.schedmd.com/archive/slurm-24.11.7/reservations.html) | 同前次 `ef527511…ab0e9a8` | `(this behavior can be change using FLEX flag) and no other jobs can use those resources`；有 `FLEX Reservations` 小节。正文 L171 `FLEX` 属实 |
| [job_reason_codes](https://slurm.schedmd.com/archive/slurm-24.11.7/job_reason_codes.html) | 同前次 `f8e4f3c9…1592a` | 每作业上限系列共 19 个 `QOSMax*PerJob` 代码，例如 `QOSMaxGRESPerJob — The GRES request exceeds the maximum each job is allowed to use for the requested QOS`；`ReqNodeNotAvail — Some node specifically required by the job…`。正文 L169 仍未使用 `QOSMax*`（0 处） |
| [squeue](https://slurm.schedmd.com/archive/slurm-24.11.7/squeue.html) | 同前次 `48e57603…ba214` | `%R`：`For pending jobs: the reason…`；`For terminated jobs with failure: an explanation…`；`For all other job states: the list of allocate nodes`。正文 L167 仍写"`R` 状态；squeue `%R` 失败说明"（前次非阻断建议未采纳） |
| [priority_multifactor](https://slurm.schedmd.com/archive/slurm-24.11.7/priority_multifactor.html)、[gres](https://slurm.schedmd.com/archive/slurm-24.11.7/gres.html) | 同前次 `acd6dead…720f58d`、`4c7a5874…cc6eccff9` | 仅比对哈希，相关正文本轮未改 |

### 取证限制

- 只读了上表所列行区间。proportion/capacity/overcommit 的 `JobEnqueueable` 公式、statement.go、bundle 切分、Kueue flavorassigner 选 reason 的完整分支、Fair Sharing 抢占策略细节都没有审计。
- Kueue 的门控回退结论来自 `workload.go` 的 fallback 函数和调用点 grep。没有逐一追踪每个 reason 写入路径在门控关闭时的最终值；测试辅助代码只作旁证。
- Volcano 文档站是可变网页，哈希只代表本次观察。
- 没有核对作者的 webfetch 取证过程本身；本报告的哈希不能写成作者取证。

## 逐项判定

### B22-C22 — P1 / OPEN

前次剩余关闭条件的落实情况：

| 条件 | 判定 | 位置证据 |
|---|---|---|
| L95 补 allocate 跳过前提 | 已落实 | L95"配置了 enqueue 动作时仍 Pending 的作业跳过 allocate，未配置时就地转 Inqueue 继续"，与 allocate.go L152–163 一致 |
| unknown 同步（frontmatter、来源记录、gang 登记 notes） | 已落实 | frontmatter L38"handler 事件路径未覆盖（unknown）；调度动作与控制器 running/restarting/policy 已读"；来源记录 L11、L18；登记 L5473"控制器实现见 job-controller 登记条目，handler 事件路径未覆盖" |
| 来源记录列出两条新登记 | 已落实 | 来源记录 L10、L11 |
| 表中各行改用 commit 链接 | 已落实 | 正文 13 个 Volcano 链接全部指向 `8fc394c1…`，`blob/v1.15.0` 0 处 |
| L96 补 gang.go 链接与区间 | 已落实 | L96 `gang.go` L229–297 |
| 表中各行补行区间 | **未全部落实** | L94 `enqueue.go` 无区间；L95 只给了 L313–336、L832–844，本轮刚改正的跳过/转 Inqueue 主张没有给 L152–169；L97 `running.go`、`job_controller_util.go` 无区间（只有 restarting.go L35–49） |

剩余关闭条件：L94 补 `enqueue.go` L95–99；L95 补 `allocate.go` L152–169；L97 补 `running.go` L35–46/L107–110、`job_controller_util.go` L182–196/L286–288。前三个区间来源记录 L10–11 已有，照抄进正文表格即可。

建议（非阻断）：L94 链接文字 `enqueue.go@v1.15.0` 与 L88 `gang.go@v1.15.0` 的 URL 已是 commit，链接文字可改为 `@8fc394c1`，避免读者误以为指向可变 tag。

### B22-C23 — P1 / OPEN

两条剩余关闭条件都没有落地。修订映射 L370 写了"样板 B 同因素正反配对（QOS 限额）；TopologyPlacementFailed 来源修正＋门控注"。

1. **样板 B 仍不是同因素配对**：L169 原文仍为"同配置在限额内的作业应被受理并显示 reason 为空或资源等待；指定节点（`--nodelist`）不可用→`ReqNodeNotAvail`……（正例配对）"。正例改变的是限额，反例改变的是节点可用性；"reason 为空或资源等待"仍不是可判定的字段值。正文全文 `QOSMax`/`QOSGrp` 0 处。
2. **L150 来源列仍错位**：`TopologyPlacementFailed` 的来源仍标"同上＋TAS 文档"。审阅者已确认，cluster_queue.md 与 TAS 文档都不含该词，出处只有 v1beta2 workload_types.go L956–958。L150 新增了"（门控开启可见）"，但正文全文没有写出门控名 `UnadmittedWorkloadsObservability`（0 处），读者无法据此确认该开哪个门控。

剩余关闭条件：

- 样板 B 补一组只改变一个因素的配对，例如：同一 QOS、同一分区、该 QOS 未设 `DenyOnLimit`；请求不超过 QOS 每作业 GRES 上限时，`squeue %r` 不应为 `QOSMax*PerJob`（正例）；只把 GRES 请求提高到超过该上限时，`%r` 应为 `QOSMaxGRESPerJob`（反例）（job_reason_codes、qos 页）。设了 `DenyOnLimit` 时作业在提交时即被拒，不会进入 Pending，须在前提中排除。指定节点一组可保留，但需配上"同作业不指定节点"的正例，并删去"reason 为空或资源等待"。
- L150 来源改为 v1beta2 [workload_types.go L956–958](https://github.com/kubernetes-sigs/kueue/blob/911a822a49bcfd99c9c62203a009efa4130ad604/apis/kueue/v1beta2/workload_types.go#L956-L958)（`src.kueue.admission-v0.19.0` 已覆盖）。
- 在首次提到门控处（L149 或 L150）写出门控名 `UnadmittedWorkloadsObservability`（v0.19 Beta，默认关闭；kube_features.go L479–481、L788–789）。L152、L155 的"开门控"随之可读。

建议（非阻断，前次已提）：L167 改为"Pending 时 `%r`/`%R` 为等待原因；失败终止的作业 `%R` 为失败说明；其他状态（含 R）`%R` 为节点列表"。

### B22-C24 — P2 / OPEN

已落实：

- Ready 实现口径与文档差异：L88 写明 `ReadyTaskNum` 计 Bound/Binding/Running/Allocated/Succeeded、不计 Pipelined，`IsReady` 另加 Pending 的 BestEffort 任务，Gang 文档把 Pipelined 列入 Ready、与实现不一致、以实现为准；并引 job_info.go L877–886、L1202–1204@`8fc394c1`。与一次源逐字一致。
- 控制器同步句：L88 引 job_controller_actions.go L813–816、L877–880@`8fc394c1`，属实。
- L88 的 gang.go（L191–211、L97–137）、gangpreempt.go 链接已改 commit 并给区间。

剩余问题：前次关闭条件"把该文件（job_controller_actions.go）纳入 job-controller 登记范围"没有落地。登记 L5504 revision 仍只列 running.go/restarting.go/job_controller_util.go；修订映射 L371 写的"actions 登记"不在文件中。

剩余关闭条件：`src.volcano.job-controller-v1.15.0` 的 revision 补 job_controller_actions.go（本轮新引的 job_info.go 归入 C30 处理）。

建议（非阻断）：

- L88"调度器 Ready 实现口径（[…]：`ReadyTaskNum` 计……以实现为准。"中的全角左括号没有闭合，建议在"以实现为准"后补"）"。
- L88 第一个 gang.go 链接支撑 `validJobFn` 等主张，可补来源记录已有的 L58–93。

### B22-C25 — P2 / OPEN

已落实：

- gang.go L97–137、gangpreempt.go L32–52/L248 已在 L88 给出，区间与一次源一致。
- `src.volcano.scheduler-actions-v1.15.0` revision（L5493）已列 gangreclaim.go。

剩余问题：gangreclaim.go 在正文 L88 只有裸链接，来源记录 L10 只写"＋gangreclaim 同模型"，两处都没有行区间。修订映射 L372 写了"gang.go/gangpreempt/gangreclaim 行区间"。注意 gangreclaim.go 的跳过判定在 **L247**，与 gangpreempt.go 的 L248 不同，不能直接套用。

剩余关闭条件：正文 L88 与来源记录 L10 补 gangreclaim.go L32–52/L247（commit `8fc394c1`）。

### B22-C26 — P2 / CLOSED

- Fair Sharing 代价：L145"启用 Fair Sharing 后 cohort 内回收改按 Fair Sharing 抢占策略执行（cluster_queue.md L444–452，具体策略未取证，unknown）"，与 L444–452 原文一致，并把策略细节记为 unknown。
- 具体参数名：L171 改为"QOS `GrpTRES` 等限额字段、预留 `FLEX` 等 flags"，qos 页与 reservations 页原文均有；段首改为"配置/状态参数"。
- L145 括注改为"两平台共有的能力如抢占不作区分依据；不是产品推荐"，语义清楚。

三条剩余关闭条件全部满足。

### B22-C27 — P2 / CLOSED

- L155 反例阈值改为"请求超过本 CQ 该 flavor 的 `nominalQuota + borrowingLimit`→持续 Pending（开门控时 reason 为 `ExceedsMaxQuota`，关闭时只见 `Pending`）"，与 cluster_queue.md 规则 3（L233–242）、workload_types.go L951–954 一致。前次指出的反例（nominalQuota=10、borrowingLimit=5、请求 8）不再成立。
- L152 两个 reason 旁都补了门控说明（"开门控可见，否则只见 `Pending`""同上门控条件"）。门控回退行为已由 workload.go L1568–1575 核实。

前次关闭条件中的门控名 `UnadmittedWorkloadsObservability` 没有写进正文。这一缺口与 C23"注明需开 `UnadmittedWorkloadsObservability`"是同一处，归入 C23 关闭条件统一处理，不在本项重复阻断。本项发现的实质问题（阈值写错、L152 缺门控说明）已关闭。

建议（非阻断）：L155 正例"同配置请求不超过 nominalQuota 的负载应得 `QuotaReserved=True`、`Admitted=True`"按规则 1 实际要求的是不超过**未用的** nominalQuota；`Admitted=True` 还要求没有未满足的 AdmissionCheck。建议补"CQ 空闲、未配置 AdmissionCheck"作为前提。

### B22-C28 — P3 / CLOSED（前次已关闭，不在本轮范围）

### B22-C29 — P3 / OPEN

已落实：

- L177 改为"再用本页样板确认配额/放置两层"，不再声称覆盖设备层。
- L139 许可范围改指来源登记条目。

剩余问题：L139 仍写"来源差异、固定版本见本批 T05-05 来源记录"。来源记录全文"差异"0 处：它只有取证方法、主张—来源定位表和 unknown 清单，没有讨论来源之间的差异（Gang 文档与实现关于 Ready 口径的差异只写在正文 L88）。前次关闭条件要求"改为与来源记录实际内容相符的说法"，本轮只改了许可范围那一半。

剩余关闭条件：L139 删去"来源差异"，或改为"主张—来源定位、支持范围与 unknown 清单"；也可以在来源记录中补一行 Gang 文档与实现的 Ready 口径差异，使链接文字成立。

建议（非阻断）："来源登记条目"可链接到 `sources/registry.yaml`；L85–87 仍是三个空行。

### B22-C30 — P3 / OPEN

已落实：

- 正文 13 个 Volcano 链接全部改用 commit `8fc394c1…`。
- `src.volcano.scheduler-actions-v1.15.0` revision（L5493）补了 tag 对象 `4691eac3`，并列入 gangreclaim.go。
- 来源记录 L9–11 补了行区间，主张表列出两条新登记。

剩余问题：

1. **两条新登记的 URL 仍用可变 tag**：L5490 `…/blob/v1.15.0/pkg/scheduler/actions/enqueue/enqueue.go`、L5501 `…/blob/v1.15.0/pkg/controllers/job/state/running.go`。修订映射 L376 写了"新登记 commit＋tag 对象"。
2. **job-controller 登记没有 tag 对象**：L5504 仍为"tag v1.15.0（所指 commit 8fc394c1）"，与 L5468、L5493 的写法不一致。
3. **登记范围与正文主张仍不一致**：job_controller_actions.go 不在 L5504 范围内（同 C24）。**按原 ID 追记**：本轮正文 L88 新引的 `pkg/scheduler/api/job_info.go` 也不在任何登记的 revision 范围内。它属于同一类缺陷（正文主张的出处未登记），不新增 ID。
4. **来源记录未覆盖本轮新引出处**：job_info.go、job_controller_actions.go 没有出现在来源记录中；gangreclaim.go（同 C25）与 job_controller_util.go 没有数字行区间（L11 只写"applyPolicies"）。

剩余关闭条件：

- L5490、L5501 的 URL 改为 `blob/8fc394c11e8db0d0ada5c17816b58bced9d7213d/…`。
- L5504 revision 补 tag 对象 `4691eac3`，并列入 job_controller_actions.go。
- 把 job_info.go 列入某一 Volcano 登记的 revision（例如 scheduler-actions 或 gang-plugin，注明"Ready/Pipelined 计数"）。
- 来源记录补 job_info.go L877–886/L1202–1208、job_controller_actions.go L813–816/L877–880、gangreclaim.go L32–52/L247、job_controller_util.go L182–197/L286–288。

## 修订映射与落盘差异

[修订映射](batch-21-review-fixes.md) L367–376 标题注明"只列落盘改动，逐条 grep 已核对"。下列条目在正文、记录或登记中没有找到对应改动，或只落地了一部分：

| 映射条目 | 落盘情况 |
|---|---|
| C22"commit 链接＋行区间" | commit 链接已全部落地；L94、L97（running/util）和 L95 跳过主张仍无行区间 |
| C23"样板 B 同因素正反配对（QOS 限额）" | 未落地：L169 未改，正文 `QOSMax*` 0 处 |
| C23"TopologyPlacementFailed 来源修正＋门控注" | 来源未改（L150 仍"同上＋TAS 文档"）；门控注只有"门控开启可见"，没有门控名 |
| C24"控制器同步句＋actions 登记" | 正文句已落地；登记 L5504 未列 job_controller_actions.go |
| C25"gang.go/gangpreempt/gangreclaim 行区间" | gangreclaim.go 在正文与来源记录中均无区间 |
| C29"链接文字修正" | 许可范围已改；"来源差异"仍与来源记录不符 |
| C30"新登记 commit＋tag 对象；registry 增文件" | 两条 URL 仍为 tag；job-controller 无 tag 对象；只增了 gangreclaim.go，未增 job_controller_actions.go |

这 7 条与"逐条 grep 已核对"的标注不符。下一轮修订后，建议用 grep 检查目标文件中的新文字（如 `QOSMaxGRESPerJob`、`workload_types.go#L956`、`blob/8fc394c1` 在登记 L5490/L5501、`job_controller_actions` 在登记中、`gangreclaim.go` 后的区间），而不是检查映射本身。

## acceptance 对照

| acceptance | 判定 | 未关闭项 |
|---|---|---|
| 1 以固定 Volcano 实现解释 minMember/minResources、成组决策、启动失败、重排队/回退及与 rendezvous 的不同 | 实质满足：本轮抽查的 Volcano 主张全部属实，Ready 口径、allocate 前提、控制器同步均已落地。剩余只是行区间与登记范围 | C22、C24、C25（均为引用/登记） |
| 2 Kueue 与 Slurm 两个独立配置/状态样板；选择依据与公平性代价分开 | 满足 | — |
| 3 每个样板的资源向量、拓扑、碎片、配额、运行进展观测，失败或不适用反例及对照验收 | 大部分满足：样板 A 对照成立，阈值已改正。剩余：样板 B 对照仍不是同因素配对；`TopologyPlacementFailed` 来源错位；门控未命名 | C23 |
| 4 MindCluster 边界；链接 idle-resource-job-waiting-triage 与 Slurm 状态参考；不是统一推荐策略 | 满足：L177 已改为"配额/放置两层"，链接与"不是推荐所有平台的统一策略"保留 | —（C29 剩余为 L139 链接文字，与本条无关） |

`verification.status: source_checked`：初审要求 C22–C25 关闭前不视 Volcano 部分为成立。本轮这四项仍 OPEN，该保留形式上继续有效。但本轮一次源抽查没有发现 Volcano 部分的事实错误，剩余都是行区间与登记范围的引用问题。

## 结论

**T05-05 第二次定向复核不通过。本轮范围 8 项：CLOSED 2（C26、C27），OPEN 6（C22、C23 为 P1；C24、C25 为 P2；C29、C30 为 P3）。B22-C22–C30 合计 CLOSED 3、OPEN 6。不新增发现 ID；job_info.go 未登记按 C30 原 ID 追记。**

- 唯一仍涉及内容设计的是 C23：样板 B 需要一组只改变一个因素的对照，L150 需要改正来源并写出门控名。其余 5 项都是补行区间、改 URL、在登记 revision 里加文件名或改一处链接文字。
- 正文没有虚构命令输出或实测结果；对照验收都标了"设计，未执行"；MindCluster 边界保持得当。
- 修订后须按上文各项"剩余关闭条件"再做一次定向复核。本复核只覆盖编辑与来源层面；文中 Volcano/Kueue/Slurm 行为都是源码或文档层证据，审阅者未部署、未运行，不得标为 reproduced。

## 检查记录

- 成稿前复取输入哈希：七个输入与"输入"表逐字一致，复核期间输入未变。
- `make check`：`PASS: 96 content entries; 444 sources.`（成稿前运行）。它只校验结构与本地链接，不说明技术正确性，也不访问远程链接。
- 未运行 `make build`：本轮只新增 `docs/research/` 下的审阅报告，按任务约束不改其他文件，也不生成 `build/` 产物。
