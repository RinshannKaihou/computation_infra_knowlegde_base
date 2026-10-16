# 第二十二批 T05-05 定向复核（作者首轮修订后）

复核日期：2026-10-15。

**结论：定向复核不通过。B22-C22–C30 共 9 项：CLOSED 1（C28），OPEN 8（C22–C27、C29、C30）。本轮不新增发现 ID。**

修订方向正确，多数实质内容已经落地，抽查一次源后属实：五层失败与回退表、两个样板的五维观测表、`minMember`/`minResources` 归属、按动作分写的抢占保护、Kueue 抢占字段默认 `Never`、Slurm 评估顺序与 fair-share、ReqNodeNotAvail 的前提，以及 Kueue 来源术语。仍 OPEN 的原因分三类：

1. 修订映射写了，正文或记录中没有对应改动：C24 的 Ready 实现口径与文档差异；C29 的"设备三层"；C22 的 unknown 未同步到 frontmatter、来源记录和 gang 登记 notes；C30 来源记录的行区间。
2. 新写内容中有事实不精确：C22 表中"仍 Pending 则跳过 allocate"漏了"配置了 enqueue 动作时"这一前提；C27 对照验收把 `ExceedsMaxQuota` 的阈值写成"超 borrowingLimit"。
3. 就近引用：正文 7 个 Volcano 链接和两条新登记仍指向可变 tag `v1.15.0`，没有行区间；gangreclaim、job 控制器同步 PodGroup 两处主张的来源文件不在任何登记范围内（C24、C25、C30）。

各项剩余关闭条件都较窄，多数是改一句话或换一个链接。

审阅者角色独立于作者。审阅模型为 `claude-opus-5-5`，由用户本次明确要求试用；这不是既有的 `gpt-6.1-sol / xhigh` 批量审阅约定，也不改写该约定。本轮未出现 `[frontier_llm]` 标记、模型不一致或认证失败；推理等级等运行元数据没有可核验记录，不补造。本轮只做只读取证和审阅：只写本报告；未改作者正文、来源记录、登记、修订映射或计划；未部署 Volcano/Kueue/MindCluster/Slurm，未提交作业，未运行任何上游测试。模型审阅不构成平台或现场验证。

## 输入（以 SHA-256 识别）

| 输入 | SHA-256 |
|---|---|
| [T05-05 正文](../../knowledge/05-cluster-platform/admission-and-placement.md)（177 行） | `2dc0c4bec2cf0b8575278a1e6a164b2e922e370addd704533865db7a581a165c` |
| [作者来源记录](batch-22-t05-05-sources.md)（16 行） | `e96299d64441a93bb84f734c6cc266cd8d7bad3b5dc086f69602f74496750ae7` |
| [修订映射](batch-21-review-fixes.md)（T05-05 首轮修订节 L355–365） | `b94cfc995ec0b2173033682df62be516dda3ac558a8eddf04549b8f3c4820244` |
| [来源登记](../../sources/registry.yaml)（444 项；T05-05 相关 L5463–5509） | `4b7857814f5e28f1c36266102b1bda5d11acce8aba7849f0898d870e346638ab`；L5463–5510 段 `eaa9797e71f284bbf900ff27ecb02ca09495447339695ba2ef8a9a4b0c3004ec` |
| [初审报告](batch-22-t05-05-claude-review.md)（关闭条件权威来源） | `2095a6fe21717e2ef9ce6977e79c197e72ca11f1000904ad229f80dbf098cde1` |
| [任务计划](../../plans/full-coverage-backlog.yaml)（T05-05 acceptance L5569–5573） | `5f9bcf865b8c77e13cc8ee5f1c03140c37b86f558d8227d8bb2080249f4fcfc3` |

前四项与任务给出的前缀一致。六个输入在开始时取哈希，成稿前复取一次，结果相同（见文末）。

## 一次源抽查（审阅者独立获取）

方法：全部用 `curl -sSL` 默认 TLS 校验只读获取，HTTP 均为 200，本轮没有重试或失败。GitHub 文件经 `raw.githubusercontent.com` 按固定 commit 取回；HTML 去标签后按文字核对，不只判可达性。版本锚用 `git ls-remote`。原文只放在临时目录 `/tmp/b22rc05/raw/`，未入库。

版本锚：Volcano `refs/tags/v1.15.0` 为 tag 对象 `4691eac388eb8ec033908cbe144b8f3aafcaeef7`，`^{}` 指向 commit `8fc394c11e8db0d0ada5c17816b58bced9d7213d`；Kueue `refs/tags/v0.19.0` 为 tag 对象 `7b3cad14a540cd256dc9c658be5a23fff809ff68`，指向 commit `911a822a49bcfd99c9c62203a009efa4130ad604`。两者与初审、登记一致。

与初审重叠的文件，本轮取回的哈希全部与初审相同，说明上游内容在两轮之间没有变化，判定差异都来自作者修订。下表"同初审"即哈希逐字相同。

### Volcano（commit `8fc394c1`）

| 文件 | SHA-256 | 核对点与结果 |
|---|---|---|
| `pkg/scheduler/actions/allocate/allocate.go` | 同初审 `7eefa6ac…bc632` | L152–163：`if job.IsPending()` 时，**只有** `conf.EnabledActionMap["enqueue"]` 为真才 `continue`（跳过）；否则注释 `If not config enqueue action, change Pending pg into Inqueue state`，就地改为 `PodGroupInqueue` 并继续。L166–169 `JobValid` 不通过跳过。L313–322、L329–336 `stmt != nil && ssn.JobReady(job)` 才 `Commit`（注释 `do not commit stmt when job is pipelined`），剩余任务时 `jobs.Push(job)`。L832–844 SubJob 不 ready 不 pipelined 时 `stmt.Discard()`。→ C22 |
| `pkg/scheduler/actions/enqueue/enqueue.go` | 同初审 `38b8feb1…f2cde` | L95–99 `MinResources == nil \|\| ssn.JobEnqueueable(job)` 时转 `PodGroupInqueue`。正文 L94 属实 |
| `pkg/scheduler/plugins/gang/gang.go` | 同初审 `9f3fe992…a2159` | L97–125 `preemptableFn`：L113 `jobOccupiedMap > job.MinAvailable` 才放行；L127–129 只注册给 Reclaimable/Preemptable；L131–137 `AddUnifiedEvictableFn` `permits all candidates`。L250–252 消息 x=`MinAvailable − schedulableTaskNum()`、y=`len(job.Tasks)`；L256 `RegisterJobRetries`；L267 `NotEnoughResourcesReason`；L277–281 `PodGroupScheduled`/`tasks in gang are ready to be scheduled`。正文 L88、L96 属实 |
| `pkg/scheduler/actions/gangpreempt/gangpreempt.go` | 同初审 `440e6ff3…1694d` | L32–52 `defaultWholeBundleOn = true`；L70 可由参数覆盖；L248 只在显式关闭时跳过 whole bundle |
| `pkg/scheduler/actions/gangreclaim/gangreclaim.go`（初审未取） | `56b0068100156c14d5f4f826bd44d427b7d8c8d180c36b0cc409569fc8b66982` | L32–52 同样 `defaultWholeBundleOn = true`；L70 参数覆盖；L247 同样判定。正文 L88 把 `allowWholeBundle` 默认 `true` 同时归给 gangpreempt/gangreclaim，**属实**，但只链了 gangpreempt.go，gangreclaim.go 也不在登记范围内。→ C25、C30 |
| `pkg/scheduler/api/job_info.go` | 同初审 `e8d19400…5823b` | L877–886 `ReadyTaskNum` 计 Bound/Binding/Running/Allocated/Succeeded，不计 Pipelined；L1202–1204 `IsReady` 另加 PendingBestEffort；L1206–1208 `IsPipelined` 另加 Waiting。→ C24 |
| `pkg/controllers/job/state/running.go` | 同初审 `97cadbe2…74544` | L35–46 Restart* 转 Restarting 且 `RetryCount++`；L107–110 `status.Pending > jobReplicas − MinAvailable` 时回 Pending。正文 L97 属实 |
| `pkg/controllers/job/state/restarting.go` | 同初审 `954f7fb4…10f6a` | L35–40 `RetryCount >= maxRetry` 转 Failed；L41–49 只在 `total − Terminating >= MinAvailable` 时转 Pending，否则 L51 `return false`，即暂留 Restarting。正文 L97"否则回 Pending"省略了这一条件（非阻断，见 C22 建议） |
| `pkg/controllers/job/job_controller_util.go` | 同初审 `e9632a06…e070b` | L182–191 `default action is sync job`；L193–196 请求自带 action 时直接采用；L286–288 只有 `PodPendingEvent` 需要配 Timeout。正文 L97 属实 |
| `pkg/controllers/job/job_controller_actions.go` | 同初审 `c2bc5da7…aaaed2` | L813–816 建 PodGroup 时 `MinMember: job.Spec.MinAvailable`、`MinResources: cc.calcPGMinResources(job)`；L877–880 不一致时同步。正文 L88"job 控制器按 `minAvailable` 计算并同步"**属实但无引用**，该文件也不在 `src.volcano.job-controller-v1.15.0` 所列范围内。→ C24、C30 |
| `pkg/webhooks/admission/jobs/mutate/mutate_job.go`（初审未取） | `a20c6922eeaa6513637a6b99a9bb14fc1132c14923fed2fb6c64a9ce68b715ef` | L116–142 依次 patch 默认 queue、scheduler、maxRetry、task spec、minAvailable、plugins，**没有注入 lifecycle policies**（全文 `Policies`/`LifecyclePolic` 0 处）；L43–46、L161–165 默认 `maxRetry` 为 3。可支持正文"默认只 SyncJobAction"在 mutate webhook 层成立；validate webhook 及其他路径未查 |
| `pkg/controllers/job/job_controller_handler.go` | 同初审 `6b559057…cdecb` | 仅取回比对哈希；正文 L90 把 handler 事件路径记为 unknown，与作者登记范围一致 |
| [PodGroup 文档](https://volcano.sh/docs/v1.15.0/concepts/podgroup/)、[Gang 文档](https://volcano.sh/docs/v1.15.0/scheduler/plugins/gang/) | 同初审 `17fe53e5…f50e2`、`6a39b97d…d1ec26b`（可变网页，仅本次观察） | 页头 `Version: v1.15.0`。Gang 页仍写 Ready 状态 `including Binding, Bound, Running, Allocated, Succeed, and Pipelined`，与 `ReadyTaskNum` 不计 Pipelined 不一致；正文没有写出这一差异。→ C24 |

### Kueue（commit `911a822a`）

| 文件 | SHA-256 | 核对点与结果 |
|---|---|---|
| `site/content/en/docs/concepts/cluster_queue.md` | 同初审 `7b35c9f7…0b346` | L87–94 同一 resource group 的资源在准入时分配同一 flavor，正文 L149 属实。L201–209 StrictFIFO 阻塞、默认 BestEffortFIFO，属实。L233–242 fit 规则 1–3：规则 3 的上限是未用的 `nominalQuota + borrowingLimit`。L248 cohort 内优先调度 nominalQuota 内负载，属实。L443、L459、L469 三个抢占字段默认 `Never`，属实。L444–452 启用 Fair Sharing 时，`reclaimWithinCohort` 的 `LowerPriority`/`Any` 改按 `Fair Sharing preemption strategies` 选受害者；L457 `borrowWithinCohort` `not with Fair Sharing`。正文只写了后者。→ C26、C27 |
| `apis/kueue/v1beta2/workload_types.go` | 同初审 `50b9523e…c4dc1` | L947–949 `WaitingForQuota`；L951–954 `ExceedsMaxQuota`：`exceeding the maximum capacity limits of the ClusterQueue or Cohort. This also includes exceeding ClusterQueue nominal + borrowingLimit constraints`；L956–958 `TopologyPlacementFailed`。→ C23、C27 |
| `site/content/en/docs/reference/metrics.md` | 同初审 `cd42760a…c2c85` | L121–122 `kueue_cluster_queue_resource_reservation`/`_usage` 存在；L58–59 `kueue_evicted_workloads*` 带 `reason` 标签；L69 `kueue_unadmitted_workloads` 只在门控开启时发出。正文 L152 新链 metrics.md，属实 |
| `site/content/en/docs/concepts/topology_aware_scheduling.md`（初审未取） | `371b15e960d1d1540a827c95eb32a9a6352c44921d367d0a86d34b3d85ba3f35` | L89–96 preferred 逐层向上，最高层仍放不下则分散准入；L97–100 required 要求全部 Pod 在同一拓扑域。正文 L150 反例属实。本页与 cluster_queue.md **都不含** `TopologyPlacementFailed`（0 处）。→ C23 |
| `site/content/en/docs/concepts/workload.md` | 同初审 `b6a40f70…659e6b1` | 用于核对 L100、L153 的 PodsReady 驱逐重排方向 |

站内旁证：[T05-02 正文](../../knowledge/05-cluster-platform/kubernetes-job-lifecycle.md) L115 现为"Workload 驱逐重排循环"行（`requeueState{count,requeueAt}`、PodsReady、workload L147–163），正文 L100、L173 引用的行号仍然有效。

### Slurm 24.11.7 归档（src.slurm.docs-24.11.7 / src.slurm.gres-tres-cgroup-24.11.7）

| 页面 | SHA-256 | 核对点与结果 |
|---|---|---|
| [priority_multifactor](https://slurm.schedmd.com/archive/slurm-24.11.7/priority_multifactor.html) | 同初审 `acd6dead…720f58d` | 评估顺序 `Jobs that can preempt`→`Jobs with an advanced reservation`→`Partition PriorityTier`→`Job priority`→`Job submit time`→`Job ID`，以及 `the job with the highest priority may not be the first to be evaluated`；fair-share `does not involve a fixed allotment`、`under-serviced are scheduled first`；`PriorityWeightAge`/`PriorityWeightFairshare` 等。正文 L159、L171 属实 |
| [reservations](https://slurm.schedmd.com/archive/slurm-24.11.7/reservations.html) | 同初审 `ef527511…ab0e9a8` | `jobs using that reservation can use only those resources (this behavior can be change using FLEX flag) and no other jobs can use those resources`；`does not alter a job's priority, but it does act as an enhancement`；`only by user root or the configured SlurmUser`。正文 L159、L171 属实 |
| [qos](https://slurm.schedmd.com/archive/slurm-24.11.7/qos.html) | 同初审 `f6b74df2…2ba5f` | `three key ways`；`When the "PreemptType" is set to "preempt/qos"`；页中有 `GrpTRES`。正文 L171 属实 |
| [job_reason_codes](https://slurm.schedmd.com/archive/slurm-24.11.7/job_reason_codes.html) | 同初审 `f8e4f3c9…1592a` | `ReqNodeNotAvail — Some node specifically required by the job is not currently available`；DOWN/DRAINED/不响应节点 `identified as part of the job's "reason" field as "UnavailableNodes"`；`Resources — The resources requested by the job are not available (e.g., already used by other jobs)`；`QOSMax*`/`QOSGrp*`/`AssocGrp*`/`AssocMax*`。正文 L165、L166、L169 属实 |
| [squeue](https://slurm.schedmd.com/archive/slurm-24.11.7/squeue.html)（初审未取） | `48e576039a8fb2904a08e911085c2f8e5b201924355f3adb757374e0903ba214` | `%r`：`The reason a job is in its current state`。`%R`：Pending 作业打印等待原因，`For terminated jobs with failure: an explanation as to why the job failed`，**其他状态（含 R）打印分配的节点列表**。正文 L167 把"`R` 状态"与"`%R` 失败说明"放在同一格，读者可能以为运行中作业的 `%R` 会给失败说明（非阻断，见 C23） |
| [gres](https://slurm.schedmd.com/archive/slurm-24.11.7/gres.html)（初审未取） | `4c7a58746e36f07ac7bf43cde934a7342b16698068ceb61ee83debc1c6eccff9` | `--gres`、`--cpus-per-gpu` 存在。正文 L163 属实 |

`src.slurm.docs-24.11.7` 登记 notes（L5396）已写明 reservations/priority_multifactor/qos/squeue 等页在 T05-03 取证范围内，本文复用合规。

### 取证限制

- 只读了上表所列行区间。proportion/capacity/overcommit 的 `JobEnqueueable` 公式、statement.go 的 Commit/Discard 内部、bundle 切分（`utils.CreateJobBundles`）、Kueue flavorassigner 与 fair_sharing 文档都没有审计。
- mutate webhook 只查了 `mutate_job.go`。"默认只 Sync"在 validate webhook 或其他准入路径下是否仍成立，本轮没有核对。
- Volcano 文档站是可变网页，哈希只代表本次观察。
- 没有核对作者的 webfetch 取证过程本身。作者来源记录写明"curl 字节级取回未执行"，因此本报告的哈希不能写成作者取证。
- 修订映射说作者已"独立复核 enqueue/allocate/gangpreempt/running/restarting/util 全文"。这一说法见于新登记的 revision（L5493、L5504），来源记录 L3 却只写了 gang 插件与 ClusterQueue 全文。本报告按正文主张逐条对照一次源，不以作者自述代替。

## 逐项判定

### B22-C22 — P1 / OPEN

已落实：

- 正文 L90–98 新增五层表（入队、会话内成组决策、会话关闭、控制器、应用 rendezvous），L100 Kueue 行引 T05-02 L115 与 workload.md。
- 各层主张与一次源相符：enqueue L95–99；allocate L313–336、L832–844；gang L250–256；util L182–191、L286–288；running L35–46、L107–110；restarting L35–40。
- L88、L94 把"启用哪些动作/插件取决于站点配置"记为 unknown。L90 标题把 unknown 收窄为"handler 事件路径未覆盖"。
- 新增两条登记：`src.volcano.scheduler-actions-v1.15.0`、`src.volcano.job-controller-v1.15.0`。

剩余问题：

1. **事实不精确（新写内容）**：L95"`JobValid` 不通过或仍 Pending 则跳过 allocate"。allocate.go L152–163 显示，只有配置了 enqueue 动作时才跳过 Pending；未配置时就地转 Inqueue 并继续分配。初审证据原文也写了"配置了 enqueue 时"，正文把这个前提丢了。它直接影响读者判断"作业为什么停在 Pending"：没配 enqueue 的站点不会因为 Pending 被 allocate 跳过。
2. **unknown 未同步，与正文表格矛盾**：
   - frontmatter `verification.notes`（L38）仍写"Volcano job 控制器重排队逻辑未覆盖（unknown）"，同文 L97 却已按控制器源码写了这一层。
   - 来源记录 L9 仍写"job 控制器重排队/回退未覆盖（unknown）"；unknown 清单第 1 条（L16）仍是"Volcano job 控制器重排队/回退逻辑"。
   - 来源记录主张表没有列出新增的两条 Volcano 登记。
   - `src.volcano.gang-plugin-v1.15.0` notes（L5473）仍写"job 控制器重排队逻辑未覆盖（unknown）"。
   - 初审关闭条件要求"正文、来源记录与登记 notes 同步更新"，修订映射也写了"unknown 收窄"，但只在正文 L90 标题落地。
3. **未"逐行引 file@commit 与行区间"**：L94、L95、L97 链接 `blob/v1.15.0`（可变 tag），都没有行区间；L96 会话关闭行只写了 `gang.go`，没有链接。

剩余关闭条件：

- L95 改为"配置了 enqueue 动作时，仍 Pending 的作业跳过 allocate；未配置时转 Inqueue 继续（allocate.go L152–163）"。
- frontmatter notes、来源记录 L9/L16 与主张表、gang 登记 notes 改为与 L90 一致的 unknown 范围（handler 事件路径、站点启用的 action/plugin、配额类插件判定公式），并在来源记录中列出两条新登记。
- 表中各行改用 commit `8fc394c1…` 链接并补行区间；L96 补 gang.go 链接与 L229–297（或 L250–256）。

建议（非阻断）：

- L97"达 `maxRetry` 转 Failed，否则回 Pending"可补"终止 Pod 足够后（`total − Terminating >= MinAvailable`，restarting.go L41–49）"。
- "默认只 Sync"可补"mutate webhook 不注入 policy（mutate_job.go L116–142），validate webhook 未核"。

### B22-C23 — P1 / OPEN

已落实：

- L143–155、L157–171 两个样板各有一张"维度 × 观测字段/命令 × 来源 × 不能推出什么 × 反例"表，覆盖资源向量、拓扑、碎片、配额、运行进展五个维度。
- 两个对照验收都标了"设计，未执行"。
- Slurm 拓扑记为 unknown（L164）；"总量够但单节点放不下"标为本库推论（L165）。
- 样板 A 的对照验收（L155）正例与反例改变的是同一个因素（请求量与配额），写了预期条件值与判定方式。

初审 P1 的核心缺口（缺维度、缺对照）已经补上。剩余问题较窄：

1. **样板 B 的对照不是正反配对**：L169 正例是"在限额内的作业应被受理并显示 reason 为空或资源等待"，反例是"指定节点不可用→ReqNodeNotAvail"。两者改变的不是同一个因素（一个是限额，一个是节点可用性），无法互为对照。"reason 为空或资源等待"也不是可判定的字段值："资源等待"不是 reason 代码，且允许两种结果。初审关闭条件要求"正反配对……写明预期字段值与判定方式"。
2. **来源列错位**：L150 拓扑行的 `TopologyPlacementFailed` 标"同上＋TAS 文档"，但 cluster_queue.md 与 TAS 文档都不含该词（0 处）。它的出处是 v1beta2 workload_types.go L956–958。

剩余关闭条件：

- 样板 B 补一组只改变一个因素的配对。例如：同一 QOS 下，请求在 QOS 限额内时 `squeue %r` 不应出现 `QOSMax*`/`QOSGrp*`（正例）；超出 QOS 每作业上限时应为 `QOSMax*`（反例）（job_reason_codes）。指定节点不可用一组可保留，写成另一对，配上"同作业不指定节点"的正例。
- L150 `TopologyPlacementFailed` 的来源改为 v1beta2 workload_types.go L956–958（固定 commit），并注明需开 `UnadmittedWorkloadsObservability`。

建议（非阻断）：

- L167 改为"Pending 时 `%r`/`%R` 为等待原因；失败终止的作业 `%R` 为失败说明；R 状态下 `%R` 为节点列表"（squeue 页）。
- L149 资源向量行的反例实际讲的是 cohort 借出，更适合放在配额行。
- L163 反例"请求超分区上限→拒绝或 Pending"的来源列是 gres 页，不支撑分区上限的行为，宜标推论或改引对应页面。

### B22-C24 — P2 / OPEN

已落实：

- L88 改为"`minMember` 由 gang 插件在会话内判定，`minResources` 不在该插件内……在入队阶段由 enqueue 动作与配额类插件使用"，与 gang.go 全文无 `MinResources`、enqueue.go L95–99 一致。
- 区分了 `NotEnoughPodsReason`（Pod 对象不够）与 `NotEnoughResourcesReason`。
- `jobReady` 改为 `AddJobReadyFn`。
- 消息 x/y 的含义正确（gang.go L250–252）。

剩余问题：

1. **Ready 实现口径与文档差异没有落地**：初审关闭条件明确要求"写明 Ready 的实现口径（含 Allocated/Succeeded、不含 Pipelined）及其与文档的差异"。修订映射写了"Ready 口径＋文档差异"，L82 标题也写"文档差异另注"，但全文没有 `ReadyTaskNum`、`Allocated`、`Succeeded`。`Pipelined` 只出现在 `AddJobPipelinedFn` 中；文档与实现的差异在正文任何地方都没有注出。一次源仍然支持这一要求：job_info.go L877–886 不计 Pipelined，Gang 文档列出 Pipelined。
2. **"job 控制器按 `minAvailable` 计算并同步 PodGroup 的 `minMember`/`minResources`"无引用**：出处是 job_controller_actions.go L813–816、L877–880，该文件既没有被正文链接，也不在 `src.volcano.job-controller-v1.15.0` 的 revision 范围内（L5504 只列 running/restarting/util）。
3. L88 的 gang.go、enqueue.go 链接用可变 tag，没有行区间。

剩余关闭条件：

- 在 L88 或 L102 加一句：调度器 Ready（`ReadyTaskNum`，job_info.go L877–886）计 Bound/Binding/Running/Allocated/Succeeded，不计 Pipelined；`IsReady` 另加 Pending 的 BestEffort 任务（L1202–1204）；Gang 文档把 Pipelined 列入 Ready，与实现不一致，以实现为准。
- 控制器同步一句补 job_controller_actions.go@`8fc394c1` L813–816、L877–880，并把该文件纳入 job-controller 登记范围。
- 链接改用 commit 并补行区间。

### B22-C25 — P2 / OPEN

已落实：L88 已按动作分写。旧 preempt/reclaim 由 `preemptableFn` 保护 MinAvailable（gang.go L97–129，属实）；gangpreempt/gangreclaim 采用 bundle 模型，`allowWholeBundle` 默认 `true`，被抢作业可能整体被驱逐；启用哪些动作取决于站点配置，记为 unknown。审阅者取回 gangreclaim.go 后确认，它与 gangpreempt.go 的默认值相同（L32–52、L247），正文的实质结论成立。

剩余问题：

1. 初审关闭条件要求"引上述文件与行区间"。L88 只链了 `gangpreempt.go@v1.15.0`（可变 tag），没有行区间；gang.go 的 `preemptableFn`/`AddUnifiedEvictableFn` 也没有行区间。
2. 主张中 gangreclaim 的一半没有来源：正文没有链 gangreclaim.go，`src.volcano.scheduler-actions-v1.15.0` 的 revision（L5493）只列了 enqueue/gangpreempt/allocate。

剩余关闭条件：补 gang.go L97–137、gangpreempt.go L32–52/L248、gangreclaim.go L32–52/L247（commit `8fc394c1`）；把 gangreclaim.go 纳入 scheduler-actions 登记范围。

### B22-C26 — P2 / OPEN

已落实：

- "……时用 X"句式已删（全文 0 处），两个样板改为"适用前提"（L145、L159），并注明不是产品推荐。
- Kueue 代价：`reclaimWithinCohort` 只在非 `Never` 时回收、三个字段默认 `Never`、默认时 cohort 只优先接纳 nominalQuota 内负载、`StrictFIFO` 队头阻塞（cluster_queue.md L201–209、L248、L443/L459/L469，属实）。
- Slurm 代价按评估顺序重写，补了 fair-share 与预留独占、不改 priority（priority_multifactor、reservations，属实）。
- L171 补了 `PriorityWeight*`、分区 `PriorityTier`、`PreemptType=preempt/qos`（属实）。

剩余问题：

1. **Fair Sharing 的代价没有写**：关闭条件要求"补 Fair Sharing 与 StrictFIFO 的代价"。正文只写了"Fair Sharing 与 `borrowWithinCohort` 互斥"（L457），这是配置约束，不是代价。cluster_queue.md L444–452 写明：启用 Fair Sharing 后，`reclaimWithinCohort` 的 `LowerPriority`/`Any` 改按 Fair Sharing 抢占策略选受害者，而不是按"是否在 nominalQuota 内"的经典规则。
2. **Slurm 参数仍有两项只是类别名**："QOS 限额字段""预留 flags"不是参数名。L171 段首"预留配置/状态参数"中的"预留"在本文专指 reservation，而这一组参数大多与 reservation 无关，容易误读。
3. L145 括注"（平台相同不作区分依据；不是产品推荐）"语义不清。按上下文，本意应是"两平台共有的能力（如抢占）不作区分依据"。

剩余关闭条件：

- 补一句 Fair Sharing 代价：启用后 cohort 内回收改按 Fair Sharing 抢占策略执行（cluster_queue.md L444–452），具体策略未取证则记 unknown。
- 把两项类别名换成所引页面上的具体参数，例如 qos 页的 `GrpTRES`、reservations 页的 `FLEX` flag；段首改为"配置/状态参数"。
- 修正 L145 括注措辞。

### B22-C27 — P2 / OPEN

已落实：

- Slurm 反例改为"指定节点（`--nodelist`）不可用→`ReqNodeNotAvail`，DOWN/DRAINED 显示为 `UnavailableNodes`"（L169），与 job_reason_codes 原文一致。
- "总量够但单节点放不下"标为推论（L165）。
- Kueue lending 反例写了前提（本 CQ 名额被借出且在使用、`lendingLimit` 未设）、`reclaimWithinCohort` 两个分支，以及门控关闭时只见 `Pending`（L149）。
- L152 区分了"请求超 nominal＋borrowingLimit→`ExceedsMaxQuota`"与"已借＋本次超限→`WaitingForQuota`"，与 workload_types L947–954 一致。

剩余问题：

- **对照验收重新把两者混在一起，且阈值写错**：L155 反例写"超 borrowingLimit 的请求应持续 Pending/`ExceedsMaxQuota`"。按 cluster_queue.md L233–242 规则 3 与 workload_types L951–954，阈值是 `nominalQuota + borrowingLimit`，不是 `borrowingLimit`。反例：nominalQuota=10、borrowingLimit=5、CQ 空闲时，请求 8 已"超 borrowingLimit"，却能在规则 1 下直接 fit 并被准入。
- L152 配额行的 `ExceedsMaxQuota`/`WaitingForQuota` 旁没有门控说明。说明只出现在 L149 资源向量行。

剩余关闭条件：L155 改为"请求超过本 CQ 该 flavor 的 `nominalQuota + borrowingLimit`→持续 Pending（开 `UnadmittedWorkloadsObservability` 时 reason 为 `ExceedsMaxQuota`，关闭时只见 `Pending`）"；L152 补同样的门控说明。

### B22-C28 — P3 / CLOSED

L173 改为来源术语："Workload 整体配额预留＋可选 waitForPodsReady 超时驱逐与退避重排"，引 T05-02 L115（已核该行仍为驱逐重排循环）。全文已无"Kueue gang""成组准入"。

### B22-C29 — P3 / OPEN

已落实：

- 重复段已删，概念（L84）在实现（L88）之前。
- "admission 规则""三档"已无（全文 0 处），L145 改为"三个抢占字段"。
- 消息 x/y 已注明。
- L171 改为"root 或配置的 SlurmUser"（reservations 原文属实）。
- 旧 F12 链接已改为本次来源记录（L139）。

剩余问题：

1. **L177"再用本页样板确认配额/放置/设备三层"未改**。修订映射写了"去设备层"，正文没有改。两个样板仍都不涉及设备分配层。
2. **L139 链接文字超出目标内容**："来源差异、固定版本与许可范围见本批 T05-05 来源记录"，但[来源记录](batch-22-t05-05-sources.md)中没有许可信息，也没有来源差异的讨论。这是修正 F12 链接后带出的新问题，许可口径实际在登记中。

剩余关闭条件：L177 改为"配额/放置两层"或删去层数；L139 改为与来源记录实际内容相符的说法，许可范围改指登记条目。

建议（非阻断）：L85–87 删段后留下三个空行。

### B22-C30 — P3 / OPEN

已落实：

- `src.volcano.gang-plugin-v1.15.0`（L5463–5473）revision 补了 tag 对象 `4691eac3` 与 commit `8fc394c1`，URL 改为 commit，与 `git ls-remote` 一致。
- `src.kueue.cluster-queue-v0.19.0` 的许可改为 partial/Apache-2.0，与 `src.kueue.admission-v0.19.0` 口径统一，revision 写明两条登记的分工。
- frontmatter `evidence_refs` 补了新增 Volcano 与 Slurm ID，`related_ids` 补了三个站内页。
- L152 链 metrics.md；样板 B 链接各归档页。
- 来源记录 L3 写明取证方法（webfetch，curl 未执行）。

剩余问题：

1. **新增两条登记重复了 C30 已指出的缺陷**：`src.volcano.scheduler-actions-v1.15.0`（L5490）与 `src.volcano.job-controller-v1.15.0`（L5501）的 URL 仍用 `blob/v1.15.0`，revision 只写"所指 commit 8fc394c1"，没有 tag 对象。正文 7 个 Volcano 源码链接（L88、L94、L95、L97）也全部用 tag。
2. **登记范围与正文主张不一致**：gangreclaim.go（C25）与 job_controller_actions.go（C24）支撑正文主张，但不在任何登记的 revision 范围内。
3. **来源记录仍没有行区间**（关闭条件"补取证方法、行区间"只完成了前一半），也没有新增两条 Volcano 登记（与 C22 第 2 条相同）。

剩余关闭条件：两条新登记的 URL 改用 commit，revision 补 tag 对象；正文 Volcano 链接改用 commit；登记 revision 补上 gangreclaim.go、job_controller_actions.go；来源记录补行区间与两条新登记。

## 修订映射与落盘差异

[修订映射](batch-21-review-fixes.md) L355–365 自称"处理全部 9 项"。下列条目写在映射中，但在正文、记录或登记中没有找到对应改动：

| 映射条目 | 落盘情况 |
|---|---|
| C22"unknown 收窄" | 只在正文 L90 标题落地；frontmatter L38、来源记录 L9/L16、登记 L5473 未改 |
| C24"Ready 口径＋文档差异" | 正文没有对应文字（全文 0 处 `ReadyTaskNum`/`Allocated`/`Succeeded`） |
| C29"去设备层" | L177 仍为"配额/放置/设备三层" |
| C30"记录方法/行区间" | 方法已写；行区间没有 |

映射标题注明"只列落盘改动"，以上四条与该标注不符。下一轮修订后建议逐条用 grep 核对落盘情况，再写映射。

## acceptance 对照

| acceptance | 判定 | 未关闭项 |
|---|---|---|
| 1 以固定 Volcano 实现解释 minMember/minResources、成组决策、启动失败、重排队/回退及与 rendezvous 的不同 | 大部分满足。五层表与归属已立住，事实基本属实。剩余：allocate 跳过 Pending 的前提、Ready 实现口径与文档差异、unknown 同步、行区间 | C22、C24、C25 |
| 2 Kueue 与 Slurm 两个独立配置/状态样板；选择依据与公平性代价分开 | 大部分满足。适用前提与代价分开写，Never 默认、评估顺序、fair-share 已补。剩余：Fair Sharing 代价、两项 Slurm 参数仍为类别名 | C26 |
| 3 每个样板的资源向量、拓扑、碎片、配额、运行进展观测，失败或不适用反例及对照验收 | 大部分满足。五维表与反例齐全，A 的对照成立。剩余：B 的对照不是同因素正反配对；A 的反例阈值写错；`TopologyPlacementFailed` 来源错位 | C23、C27 |
| 4 MindCluster 边界；链接 idle-resource-job-waiting-triage 与 Slurm 状态参考；不是统一推荐策略 | 基本满足。L177 链接诊断指南，样板 B 链接 Slurm 归档页，"不是推荐所有平台的统一策略"保留，"时用 X"已删。剩余：L177 仍说样板覆盖设备层 | C29 |

`verification.status: source_checked`：初审要求 C22–C25 关闭前，Volcano 部分不视为成立。本轮四项仍 OPEN，这一保留继续有效。剩余问题以引用与同步为主；实质上仍有两处不精确，即 C22 的 allocate 前提与 C24 的 Ready 口径。

## 结论

**T05-05 定向复核不通过。B22-C22–C30 共 9 项：CLOSED 1（C28），OPEN 8（C22、C23 为 P1；C24–C27 为 P2；C29、C30 为 P3）。**

- 修订后须按上文各项"剩余关闭条件"再做一次定向复核。各项剩余工作量都不大，多数是改一句话、补一个链接或同步一处 unknown。
- 正文没有虚构命令输出或实测结果。新写的对照验收都标了"设计，未执行"，MindCluster 边界保持得当。
- 本复核只覆盖编辑与来源层面。文中 Volcano/Kueue/Slurm 行为都是源码或文档层证据，审阅者未部署、未运行，不得标为 reproduced。

## 检查记录

- 成稿前复取输入哈希：六个输入与"输入"表逐字一致，复核期间输入未变。
- `make check`：`PASS: 96 content entries; 444 sources.`（成稿前运行）。它只校验结构与本地链接，不说明技术正确性，也不访问远程链接。
- 未运行 `make build`：本轮只新增 `docs/research/` 下的审阅报告，按任务约束不改其他文件，也不生成 `build/` 产物。
