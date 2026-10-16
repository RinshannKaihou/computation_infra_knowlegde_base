# 第二十二批 T05-05 第三次定向复核（作者第三轮修订后）

复核日期：2026-10-15。

**结论：定向复核不通过。本轮范围 6 项（B22-C22–C25、C29、C30）：CLOSED 2（C24、C29），OPEN 4（C22、C23、C25、C30）。连同前轮已关闭的 C26、C27、C28，B22-C22–C30 共 9 项：CLOSED 5，OPEN 4。本轮不新增发现 ID；C23 下追记一处配对前提遗漏，按原 ID 处理。**

本轮正文、来源记录和登记新写或改写的引用，抽查一次源后全部属实，行区间也正确：allocate/enqueue/running/restarting/job_controller_util、gangreclaim L32–52/L247、job_info.go、job_controller_actions.go、Kueue `TopologyPlacementFailed` 定义 L956–958、门控 `UnadmittedWorkloadsObservability`（v0.19 Beta，默认关闭）、Slurm `DenyOnLimit` 与 `QOSMaxGRESPerJob`。登记侧前次的剩余条件已全部落地。

仍 OPEN 的 4 项中，3 项与前两轮相同，原因是映射写了改动，文件里没有；1 项是新追记：

1. **映射写了，文件里没有**：C22 正文 L95 仍无 allocate.go L152–169；C25 来源记录仍只写"gangreclaim 同模型"，没有 L32–52/L247；C30 来源记录缺 job_controller_actions.go、gangreclaim.go 区间和 job_controller_util.go 数字区间。这三处都在来源记录或一个表格单元内，改一处可同时推进 C25 与 C30。
2. **C23 追记（审阅者侧遗漏）**：样板 B 的 QOS 配对按前次关闭条件逐字落地，但前次条件本身漏了两个前提。一是 Partition QOS 的上限优先于作业 QOS；二是站点要实际执行 QOS 限额。缺少这两点时，正例和反例的预期都可能不成立（见下文 C23）。作者没有做错，需要补一句前提。

另：作者在本轮修订中直接改了前次复核报告（审阅者产物）。审阅者核对了这些改动：所改 5 处数字全部正确，但作者声明的处数与"未找到"说法不准确。勘误与流程意见见"前次复核报告的改动与勘误"一节。

审阅者角色独立于作者。审阅模型为 `claude-opus-5-5`，由用户本次明确要求试用；这不是既有的 `gpt-6.1-sol / xhigh` 批量审阅约定，也不改写该约定。本轮未出现 `[frontier_llm]` 标记、模型不一致或认证失败；推理等级等运行元数据没有可核验记录，不补造。本轮只做只读取证和审阅：只写本报告；未改作者正文、来源记录、登记、修订映射、计划或前次报告；未部署 Volcano/Kueue/MindCluster/Slurm，未提交作业，未运行任何上游测试。模型审阅不构成平台或现场验证。

## 输入（以 SHA-256 识别）

| 输入 | SHA-256 |
|---|---|
| [T05-05 正文](../../knowledge/05-cluster-platform/admission-and-placement.md)（177 行） | `b9e477c4a45d00d1c5722656fe732442f6843e0b49389a3c6c584dba1fb9464c` |
| [作者来源记录](batch-22-t05-05-sources.md)（22 行） | `2369f6cb0b21d0d406bc978d70492a691187758203bdc77a35e7009a6d6f997f` |
| [修订映射](batch-21-review-fixes.md)（T05-05 第三轮修订节 L378–386） | `5810b93635485402a5fed04d91f492beb10a99904779fbbf88e586377b46ca61`；L378–386 段 `c284b743c9702c8e8247c5ddc6207bc84f91a4581744bc9811a90dc4bd56496b` |
| [来源登记](../../sources/registry.yaml)（444 项；T05-05 相关 L5463–5509） | `b9cdbedf73379dd24d704e0363e1fcbcc550f3c8f9581b93659a32a1e39a6b0f`；L5463–5509 段 `de6d0a9079431d077facc717ab1be8f99b14cbbc63d4b9c102da2b1c75d39f2a` |
| [前次复核报告](batch-22-t05-05-claude-recheck-2.md)（现文件，已被作者改动，见下文） | `83adf3934f3484efd821e93fca7f400592e54ec0de69c7287c2dc78aaa264c28` |
| 前次复核报告审阅者原稿（本地会话记录中的 Write 内容，未入库） | `10bdb2da7e4f9e567a220029bf7284d3208250b964a42bda1ab05dde1b672be4` |
| [初审报告](batch-22-t05-05-claude-review.md) | `2095a6fe21717e2ef9ce6977e79c197e72ca11f1000904ad229f80dbf098cde1` |
| [任务计划](../../plans/full-coverage-backlog.yaml)（T05-05 acceptance L5569–5573） | `5f9bcf865b8c77e13cc8ee5f1c03140c37b86f558d8227d8bb2080249f4fcfc3` |

任务给出的五个前缀（正文、来源记录、修订映射、登记，及前次报告无前缀）中，四个给定前缀均一致。输入在开始时取哈希，成稿前复取一次，结果相同（见文末）。

## 一次源抽查（审阅者独立获取）

方法：全部用 `curl -sSL` 默认 TLS 校验只读获取，HTTP 均为 200，本轮没有重试或失败。GitHub 文件经 `raw.githubusercontent.com` 按固定 commit 取回；HTML 去标签后按文字核对，不只判可达性。版本锚用 `git ls-remote`。原文只放在临时目录 `/tmp/b22rc05c/`，未入库。

版本锚：Volcano `refs/tags/v1.15.0` 为 tag 对象 `4691eac388eb8ec033908cbe144b8f3aafcaeef7`，`^{}` 指向 commit `8fc394c11e8db0d0ada5c17816b58bced9d7213d`；Kueue `refs/tags/v0.19.0` 为 tag 对象 `7b3cad14a540cd256dc9c658be5a23fff809ff68`，指向 commit `911a822a49bcfd99c9c62203a009efa4130ad604`。与前三轮及登记一致。

与前次重叠的文件/页面，本轮取回的 SHA-256 全部与前次相同（下表"同前次"），说明上游未变，判定差异都来自作者修订。

### Volcano（commit `8fc394c1`）

| 文件 | SHA-256 | 核对点与结果 |
|---|---|---|
| `pkg/scheduler/actions/allocate/allocate.go`（973 行） | 同前次 `7eefa6ac…bc632` | L152–164：`job.IsPending()` 且 `conf.EnabledActionMap["enqueue"]` 为真则 `continue`（L155–158）；否则日志 `no enqueue action is configured` 并就地设 `PodGroupInqueue`（L159–163）。L166–169 `JobValid` 不通过则 `continue`。L314、L330 `stmt != nil && ssn.JobReady(job)` 才 `Commit`；L319–321、L333–335 有剩余任务时 `jobs.Push(job)`。L832–844 SubJob 不 ready 不 pipelined 则 `stmt.Discard()`。**正文 L95 文字属实，但仍无 L152–169**（C22） |
| `pkg/scheduler/actions/enqueue/enqueue.go`（106 行） | 同前次 `38b8feb1…f2cde` | L95–99 `MinResources == nil \|\| ssn.JobEnqueueable(job)` → `PodGroupInqueue`。**正文 L94 区间正确**（C22） |
| `pkg/scheduler/plugins/gang/gang.go`（297 行） | 同前次 `9f3fe992…a2159` | L58 `validJobFn`；L97 `preemptableFn`；L128–129 注册；L133 `AddUnifiedEvictableFn`；L191 `AddJobReadyFn`、L211 `AddJobPipelinedFn`；L229 `OnSessionClose`；L251 消息 x/y；L256 `RegisterJobRetries`。**正文 L88、L96 区间正确** |
| `pkg/scheduler/actions/gangpreempt/gangpreempt.go`（254 行） | 同前次 `440e6ff3…1694d` | L32–33 `AllowWholeBundleKey`；L37 `defaultWholeBundleOn = true`；L48 为空行，L49–52 `New()` 采用默认；L70 `arguments.GetBool` 覆盖；L248 `bundle.Type == utils.BundleWhole && !gp.allowWholeBundle` 才跳过。**正文 L88 `L32–52、L248` 正确** |
| `pkg/scheduler/actions/gangreclaim/gangreclaim.go`（263 行） | 同前次 `56b00681…66982` | 结构相同：L37 默认 `true`，L49–52 `New()`，L70 覆盖，**L247** 跳过判定。**正文 L88 `L32–52、L247` 正确**；来源记录仍无区间（C25、C30） |
| `pkg/scheduler/api/job_info.go`（1537 行） | 同前次 `e8d19400…5823b` | L877–886 `ReadyTaskNum` 计 Bound/Binding/Running/Allocated/Succeeded；L1202–1204 `IsReady`；L1206–1208 `IsPipelined` 另加 `WaitingTaskNum`。**正文 L88、来源记录 L10、登记 L5493 区间全部正确**（C30） |
| `pkg/controllers/job/job_controller_actions.go`（1137 行） | 同前次 `c2bc5da7…aaaed2` | L813 `MinMember: job.Spec.MinAvailable`、L816 `MinResources: cc.calcPGMinResources(job)`；L877–881 不一致时同步两字段。**正文 L88、登记 L5504 区间正确**；来源记录未列（C30） |
| `pkg/controllers/job/state/running.go`（114 行） | 同前次 `97cadbe2…74544` | L35–46 Restart* → Restarting、`RetryCount++`；L107–110 `status.Pending > jobReplicas − MinAvailable` 回 Pending。**正文 L97 区间正确**（C22） |
| `pkg/controllers/job/state/restarting.go`（63 行） | 同前次 `954f7fb4…10f6a` | L35–40 `RetryCount >= maxRetry` → Failed；L46–49 `total − Terminating >= MinAvailable` → Pending。正文 L97 正确 |
| `pkg/controllers/job/job_controller_util.go`（471 行） | 同前次 `e9632a06…e070b` | L182 `func applyPolicies`；L190–191 `default action is sync job`；L194–197 请求自带 action 时直接采用并返回（L197 为右花括号）；L223–236 task 级 policy 匹配事件、`shouldConfigureTimeout` 与 `policy.Timeout`；L286–288 只有 `PodPendingEvent` 需配 Timeout。**正文 L97 `L182–196/L286–288` 正确**（C22） |
| [Gang 文档](https://volcano.sh/docs/v1.15.0/scheduler/plugins/gang/) | 同前次 `6a39b97d…d1ec26b`（可变网页，仅本次观察） | 页头 `Version: v1.15.0`；原文 `considers tasks not in the Ready state (including Binding, Bound, Running, Allocated, Succeed, and Pipelined)`。**来源记录 L18 差异行属实**（C29） |

### Kueue（commit `911a822a`）

| 文件 | SHA-256 | 核对点与结果 |
|---|---|---|
| `apis/kueue/v1beta2/workload_types.go`（1220 行） | 同前次 `50b9523e…c4dc1` | L956–958 `WorkloadQuotaReservedReasonTopologyPlacementFailed`，注释 `topology requirements that cannot be satisfied with the current cluster topology usage`。**正文 L150 新链接与区间正确**（C23） |
| `pkg/features/kube_features.go`（843 行） | 同前次 `225c13d6…ff8de02d` | L479–481 `UnadmittedWorkloadsObservability`（`updates status reasons for QuotaReserved/Admitted conditions to use tiered reasons`）；L788–789 `0.19`、`Default: false`、`PreRelease: Beta`。**正文 L149、L150"v0.19 Beta，默认关"属实**（C23） |
| `site/content/en/docs/concepts/cluster_queue.md`（561 行） | 同前次 `7b35c9f7…0b346` | `TopologyPlacementFailed` 0 处，与前次结论一致 |

### Slurm 24.11.7 归档

| 页面 | SHA-256 | 核对点与结果 |
|---|---|---|
| [qos](https://slurm.schedmd.com/archive/slurm-24.11.7/qos.html)（登记内） | 同前次 `f6b74df2…2ba5f` | `DenyOnLimit — If set, jobs using this QOS will be rejected at submission time if they do not conform to the QOS 'Max' limits as stand-alone jobs`，否则 `will pend until resources are available (as by default without DenyOnLimit)`：**正文 L169 DenyOnLimit 前提属实**。同页 Partition QOS 节：`the Partition QOS limits will override the job's QOS. If the opposite is desired you may configure the job's QOS with Flags=OverPartQOS`（C23 追记依据） |
| [job_reason_codes](https://slurm.schedmd.com/archive/slurm-24.11.7/job_reason_codes.html)（登记内） | 同前次 `f8e4f3c9…1592a` | `QOSMaxGRESPerJob — The GRES request exceeds the maximum each job is allowed to use for the requested QOS`。**正文 L169 反例 reason 属实** |
| [squeue](https://slurm.schedmd.com/archive/slurm-24.11.7/squeue.html)（登记内） | 同前次 `48e57603…ba214` | 仅比对哈希；L167 相关措辞本轮未改 |
| [resource_limits](https://slurm.schedmd.com/archive/slurm-24.11.7/resource_limits.html)（**未登记**，本轮新取） | `5212b674e87ae9ea571e1652028219e47bfd9ffbed528d9008fcdae92cf91992` | `In order to enforce scheduling policy, set the value of AccountingStorageEnforce`；`Without AccountingStorageEnforce being set (the default behavior) jobs will be executed based upon policies configured in Slurm on each cluster`；限额层级 `a limit set on a Partition QOS will be applied before a limit on the job's requested QOS`；`if a job request breaches a given limit on its own, the job will pend unless the job's QOS has the DenyOnLimit flag set`（C23 追记依据） |
| [slurm.conf](https://slurm.schedmd.com/archive/slurm-24.11.7/slurm.conf.html)（登记内，本轮新取） | `f4151769ed29968c7de408809a5acb8f0591865cd525d5f2c70925e847a1ff34` | `AccountingStorageEnforce` 的 `limits` 选项：`Users can be limited by association to whatever job size or run time limits are defined`（原文只写 association，未直接写 QOS） |

### 取证限制

- 只读了上表所列行区间与段落。proportion/capacity/overcommit 的 `JobEnqueueable` 公式、Kueue flavorassigner 的 reason 分支、Fair Sharing 策略细节仍未审计（与前次相同）。
- C23 追记的第二点（QOS 限额需站点执行）只有文档层证据：resource_limits 页把调度策略的执行挂在 `AccountingStorageEnforce` 上，默认不设；qos 页说明 QOS 限额与关联限额属同一体系。slurm.conf 对 `limits` 的原文只提 association。审阅者没有读 slurmctld 源码，不能确认 QOS 限额只依赖 `limits` 这一个选项。因此关闭条件只要求写明"站点实际执行 QOS 限额"这一前提，不要求写死具体选项。
- Volcano 文档站是可变网页，哈希只代表本次观察。
- 没有核对作者的 webfetch 取证过程本身；本报告的哈希不能写成作者取证。

## 逐项判定

### B22-C22 — P1 / OPEN

| 前次剩余条件 | 判定 | 位置证据 |
|---|---|---|
| L94 补 `enqueue.go` L95–99 | 已落实 | 正文 L94 链接文字 `enqueue.go` L95–99@`8fc394c1`，区间正确 |
| L95 补 `allocate.go` L152–169 | **未落实** | 正文 L95 只有 L313–336、L832–844，`L152` 全文 0 处；单元格前半句"`JobValid` 不通过则跳过 allocate；配置了 enqueue 动作时仍 Pending 的作业跳过 allocate，未配置时就地转 Inqueue 继续"仍无区间。修订映射 L380 写了"allocate L152–169/L313–336/L832–844" |
| L97 补 `running.go`、`job_controller_util.go` 区间 | 已落实 | 正文 L97 `running.go` L35–46/L107–110、`job_controller_util.go` L182–196/L286–288，均与一次源一致 |

剩余关闭条件：正文 L95 补 `allocate.go` L152–169（写在"未配置时就地转 Inqueue 继续"之后，或把链接文字改为 `allocate.go` L152–169/L313–336/L832–844@`8fc394c1`）。

### B22-C23 — P1 / OPEN

前次三条剩余关闭条件全部落实：

| 前次剩余条件 | 判定 | 位置证据 |
|---|---|---|
| 样板 B 同因素配对＋`DenyOnLimit` 前提；指定节点一组配正例；删"reason 为空或资源等待" | 已落实 | L169：同一 QOS、同一分区、未设 `DenyOnLimit`，只改 GRES 请求，正例 `%r` 不为 `QOSMax*PerJob`，反例 `%r` 为 `QOSMaxGRESPerJob`；`--nodelist` 一组配"同作业不指定节点"正例；"资源等待"0 处 |
| L150 `TopologyPlacementFailed` 来源改为 v1beta2 workload_types.go L956–958 | 已落实 | L150 观测单元格内直接链接 `workload_types.go#L956-L958`@`911a822a`。"来源"列仍为"同上＋TAS 文档"，但该列现在只对应 TAS 标签层级，该 reason 已有就近的精确出处，不再错位 |
| 写出门控名 | 已落实 | L149、L150 均写 `UnadmittedWorkloadsObservability`（v0.19 Beta，默认关），与 kube_features.go L479–481、L788–789 一致 |

**按原 ID 追记（审阅者侧遗漏）**：L169 的 QOS 配对缺两个前提。缺少这两个前提时，"只改变一个因素"的配对推不出所写的预期：

1. **Partition QOS 优先**。qos 页（登记内）原文：`the Partition QOS limits will override the job's QOS`，除非作业 QOS 设 `Flags=OverPartQOS`。如果该分区挂了 Partition QOS 且定义了每作业 GRES 上限，生效的就是分区 QOS 的上限，不是 L169 所说的"QOS 每作业 GRES 上限"。分区上限更低时，正例也会出现 `QOSMaxGRESPerJob`；分区上限更高时，反例不会出现该 reason。
2. **站点要实际执行 QOS 限额**。resource_limits 页：`In order to enforce scheduling policy, set the value of AccountingStorageEnforce`，`Without AccountingStorageEnforce being set (the default behavior) jobs will be executed based upon policies configured in Slurm on each cluster`。未启用时，反例不会因 QOS 限额停在 Pending。证据层级见"取证限制"。

这两点都不在前次报告给出的关闭条件里：前次只要求排除 `DenyOnLimit`。作者已逐字落实前次条件，这里不记为作者修订或映射问题。

剩余关闭条件（一句前提即可）：

- L169 前提补"该分区未设 Partition QOS 的每作业 GRES 上限（或作业 QOS 设 `OverPartQOS`）"，出处为 qos 页 Partition QOS 节。
- L169 前提补"站点实际执行 QOS 限额（如 `AccountingStorageEnforce` 含 `limits`；站点值 unknown）"。如果正文写出具体选项并引用 resource_limits 页，须先登记该页：它目前不在 `src.slurm.docs-24.11.7` 的页面范围内，登记中 `resource_limits` 为 0 处。只写"站点实际执行 QOS 限额（unknown）"而不点名选项，也满足本条。

建议（非阻断）：

- L149 末尾"否则只见 `Pending`，unknown"中的 unknown 指代不清，建议写成"站点是否开启 unknown"。
- 门控名旁可补 [kube_features.go L479–481、L788–789](https://github.com/kubernetes-sigs/kueue/blob/911a822a49bcfd99c9c62203a009efa4130ad604/pkg/features/kube_features.go#L479-L481) 链接（`src.kueue.admission-v0.19.0` 已覆盖该文件）。
- L167 `%R` 措辞（前两轮已提）仍未改：Pending 时 `%r`/`%R` 为等待原因，失败终止作业 `%R` 为失败说明，其他状态（含 R）`%R` 为节点列表。

### B22-C24 — P2 / CLOSED

- 前次唯一剩余条件已落实：登记 L5504 `src.volcano.job-controller-v1.15.0` revision 列入"job_controller_actions.go（L813–816/L877–880 同步）"，与一次源一致。
- 正文 L88 的 Ready 实现口径、文档差异、控制器同步句与一次源一致（见上表）。

建议（非阻断，前次已提，仍未改）：

- L88"调度器 Ready 实现口径（[…]：`ReadyTaskNum` 计……以实现为准。"中的全角左括号仍未闭合（L88 计 `（` 13 个、`）` 12 个），建议在"以实现为准"后补"）"。
- L88 第一个 `gang.go@v1.15.0` 链接支撑 `validJobFn` 等主张，可补来源记录已有的 L58–93，并把链接文字改为 `@8fc394c1`。

### B22-C25 — P2 / OPEN

| 前次剩余条件 | 判定 | 位置证据 |
|---|---|---|
| 正文 L88 补 gangreclaim.go L32–52/L247 | 已落实 | L88 `gangreclaim.go` L32–52、L247@`8fc394c1`，与一次源一致（跳过判定 L247，不是 gangpreempt 的 L248） |
| 来源记录 L10 补 gangreclaim.go L32–52/L247 | **未落实** | 来源记录 L3"gangreclaim 同模型"、L10"＋gangreclaim 同模型（bundle 默认开）"，`L247` 全文 0 处。修订映射 L383 写了"（正文＋记录）" |

剩余关闭条件：来源记录 L10（及 L3 方法句）把"gangreclaim 同模型"补为 gangreclaim.go L32–52/L247（可附 `8fc394c1` 链接）。此处同时满足 C30 第 4 条中的 gangreclaim 部分。

### B22-C29 — P3 / CLOSED

- 来源记录新增"来源差异记录"节（L16–18）：Gang 文档把 Pipelined 列入 Ready，实现 `ReadyTaskNum` 不计 Pipelined（job_info.go L877–886），以实现为准。审阅者本轮重取 Gang 文档与 job_info.go，两处原文均与该行一致。
- 正文 L139"来源差异、固定版本见本批 T05-05 来源记录"现在与记录内容相符：差异见 L16–18，固定版本见 L9–11 的 commit 链接。前次给出的第三种关闭方式已满足。

建议（非阻断，前次已提）："来源登记条目"可链接到 `sources/registry.yaml`；正文 L85–87 仍是三个空行。

### B22-C30 — P3 / OPEN

| 前次剩余条件 | 判定 | 位置证据 |
|---|---|---|
| L5490、L5501 URL 改 commit | 已落实 | 登记 L5490、L5501 均为 `blob/8fc394c11e8db0d0ada5c17816b58bced9d7213d/…`；L5463–5509 段内 `blob/v1.15.0` 0 处 |
| L5504 补 tag 对象并列入 job_controller_actions.go | 已落实 | L5504"tag v1.15.0（tag 对象 4691eac3，所指 commit 8fc394c1）；…job_controller_actions.go（L813–816/L877–880 同步）"，与 git ls-remote 一致 |
| job_info.go 列入某一 Volcano 登记 | 已落实 | L5493 scheduler-actions revision 列入"api/job_info.go（ReadyTaskNum L877–886/IsReady L1202–1204/IsPipelined L1206–1208）"，区间正确 |
| 来源记录补四个文件的区间 | **部分落实（1/4）** | job_info.go L877–886/L1202–1208 已在 L10。其余三个未补：job_controller_actions.go 全文 0 处；gangreclaim.go 无区间（同 C25）；job_controller_util.go 仍只写"applyPolicies"（L3、L11），`L182`、`L286` 均 0 处。修订映射 L385 写了"记录补行区间" |

剩余关闭条件（全部在来源记录内）：

- L11 控制器行补 job_controller_actions.go L813–816/L877–880（PodGroup `minMember`/`minResources` 同步）。
- L11 "job_controller_util.go applyPolicies"后补 L182–197/L286–288（L182–196 也可接受，L197 只是右花括号）。
- gangreclaim.go L32–52/L247：与 C25 同一处修改。

建议（非阻断）：登记 L5489 标题"调度动作实现（enqueue/allocate/gangpreempt）"现在还覆盖 gangreclaim.go 和非动作文件 api/job_info.go，可酌情更新标题或 notes。

## 前次复核报告的改动与勘误

修订映射 L386 声明"recheck-2 报告 4 处行号笔误机械修正（L48–52 一处未在文件中找到，未改）"。审阅者把本地会话记录中前次报告的原稿（`10bdb2da…`）与现文件（`83adf393…`）逐行比对，结果如下：

- **实际改动为 3 行 5 处数字**：L45 `L329`→`L330`、`L319–322`→`L319–321`、`L332–335`→`L333–335`；L54 `L193–196`→`L194–197`；L203 `L182–196`→`L182–197`。其余 241 行逐字相同，结论、计数和关闭条件都没有被改。
- **5 处改动全部正确**：本轮一次源显示，Commit 判定在 allocate.go L314/L330（L329 是 `allocateResourcesForTasks`）；放回队列在 L319–321/L333–335（L322 为右花括号，L332 为空行）；请求自带 action 的分支在 job_controller_util.go L194–197（L193 为空行）。这些改动与前次审阅会话成稿后尝试过的自我更正一致；那次更正因写权限未获批没有落盘。
- **声明与实际不符的两点**：
  1. 前次报告 L48、L49 两处 `L48–52` 都在文件中，"未在文件中找到"的说法不准确。正确值为 `L49–52`（gangpreempt.go 与 gangreclaim.go 的 L48 均为空行）。
  2. 前次报告 L104 的 `job_controller_util.go L182–196` 没有改，声明也没有提到。它与同报告 L203 的 `L182–197` 不一致。

  以上两点都不影响任何判定：`L48–52` 只多含一个空行，`L182–196` 只少一个右花括号。**本节即为前次报告这 3 处残留的权威勘误。** 按任务约束，本报告不回改前次报告。

流程意见：前次报告是审阅者产物，作者在修订轮直接改动后，前次报告的哈希就不再对应审阅者的原始输出（本轮输入表因此另列原稿哈希）。这次的改动正确且已声明，没有造成内容损害。今后审阅报告里的错误建议由下一轮审阅以勘误节发布，作者只在修订映射中指出疑点，不在原报告上改。

## 修订映射与落盘差异

[修订映射](batch-21-review-fixes.md) L378–386 标题注明"逐条 grep 已核对"。下列条目与文件不符：

| 映射条目 | 落盘情况 |
|---|---|
| L380 C22"allocate L152–169/L313–336/L832–844" | 正文 L95 无 L152–169（`L152` 0 处） |
| L383 C25"gangreclaim.go L32–52/L247（正文＋记录）" | 正文已落地；来源记录无区间（`L247` 0 处） |
| L385 C30"记录补行区间" | 只补了 job_info.go；job_controller_actions.go、gangreclaim.go、job_controller_util.go 数字区间均未补 |
| L386"4 处行号笔误机械修正（L48–52 一处未在文件中找到）" | 实为 3 行 5 处；`L48–52` 在前次报告 L48、L49 均存在；L104 `L182–196` 未改且未声明 |

L381（C23）、L382（C24）、L384（C29）三条与文件一致。建议下一轮修订后，用 grep 检查目标文件中的新文字（例如正文中的 `L152–169`、来源记录中的 `L247`、`job_controller_actions`、`L182`），不要检查映射本身。

## acceptance 对照

| acceptance | 判定 | 未关闭项 |
|---|---|---|
| 1 以固定 Volcano 实现解释 minMember/minResources、成组决策、启动失败、重排队/回退及与 rendezvous 的不同 | 实质满足：本轮抽查的 Volcano 主张与行区间全部属实，登记范围已覆盖全部引用文件。剩余是正文一处区间和来源记录三处区间 | C22、C25、C30（均为引用记录） |
| 2 Kueue 与 Slurm 两个独立配置/状态样板；选择依据与公平性代价分开 | 满足 | — |
| 3 每个样板的资源向量、拓扑、碎片、配额、运行进展观测，失败或不适用反例及对照验收 | 大部分满足：样板 A 对照成立，`TopologyPlacementFailed` 出处与门控名已改正；样板 B 已改为同因素配对。剩余是 QOS 配对的两条前提 | C23 |
| 4 MindCluster 边界；链接 idle-resource-job-waiting-triage 与 Slurm 状态参考；不是统一推荐策略 | 满足（L177 未变） | — |

`verification.status: source_checked`：初审要求 C22–C25 关闭前不视 Volcano 部分为成立。本轮 C22、C25 仍 OPEN，该保留形式上继续有效。但三轮一次源抽查都没有发现 Volcano 部分的事实错误，C22、C25 剩余的都是引用区间问题。

## 结论

**T05-05 第三次定向复核不通过。本轮范围 6 项：CLOSED 2（C24、C29），OPEN 4（C22、C23 为 P1；C25 为 P2；C30 为 P3）。B22-C22–C30 合计 CLOSED 5、OPEN 4。不新增发现 ID；C23 的 Partition QOS 与限额执行两条前提按原 ID 追记，属于审阅者前次关闭条件的遗漏。**

- 剩余工作共 4 处文字修改：正文 L95 补一个区间；正文 L169 补一句前提；来源记录 L10/L11 补三个文件的区间，其中 gangreclaim 一处同时关闭 C25 和 C30 的对应部分。如果 L169 点名 `AccountingStorageEnforce` 并引用 resource_limits 页，须同时登记该页。
- 正文没有虚构命令输出或实测结果；对照验收都标了"设计，未执行"；MindCluster 边界保持得当。
- 修订后须按上文各项"剩余关闭条件"再做一次定向复核。本复核只覆盖编辑与来源层面；文中 Volcano/Kueue/Slurm 行为都是源码或文档层证据，审阅者未部署、未运行，不得标为 reproduced。

## 检查记录

- 成稿前复取输入哈希：七个输入文件与"输入"表逐字一致，复核期间输入未变。
- `make check`：`PASS: 96 content entries; 444 sources.`（成稿前运行；`check` 分支不写文件）。它只校验结构与本地链接，不说明技术正确性，也不访问远程链接。
- 未运行 `make build`：本轮只新增 `docs/research/` 下的审阅报告，按任务约束不改其他文件，也不生成 `build/` 产物。
