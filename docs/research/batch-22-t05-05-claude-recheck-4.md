# 第二十二批 T05-05 第四次定向复核（作者第四轮修订后）

复核日期：2026-10-15。

**结论：定向复核不通过。本轮范围 4 项（B22-C22、C23、C25、C30）：CLOSED 3（C22、C25、C30），OPEN 1（C23）。连同前轮已关闭的 C24、C26–C29，B22-C22–C30 共 9 项：CLOSED 8，OPEN 1。本轮不新增发现 ID，也没有发现新的事实错误。**

本轮新写的行区间都已核对一次源，全部正确：allocate.go L152–169、gangreclaim.go L32–52/L247、job_controller_actions.go L813–816/L877–880、job_controller_util.go L182–196/L286–288。L169 新写的 Partition QOS/`OverPartQOS` 前提也有 qos 页原文支撑。

C23 仍 OPEN，只差一处出处。L169 括注“默认不设 `AccountingStorageEnforce` 时不按记账库限额执行”点名了选项并写出默认行为，这是实质主张。它与 Slurm 原文一致，但原文只在 resource_limits 页。该页未登记，正文也未引用。正文句末所引的 qos 页、job_reason_codes 页，以及登记内的 slurm.conf 条目，都没有这句。这正是前次关闭条件写明的情形：点名选项就须登记并引用 resource_limits 页，否则只写 unknown。

另有两处非阻断问题：来源记录 L11 留下一段编辑残留（重复的 util 裸 URL 和“（默认 Sync）”）；前次复核报告 L31 的“五个前缀”措辞有误，修订映射 L394 认为它“已准确”，这个判断不成立。权威勘误见下文。

审阅者角色独立于作者。审阅模型为 `claude-opus-5-5`，由用户明确要求试用；这不是既有的 `gpt-6.1-sol / xhigh` 批量审阅约定，也不改写该约定。本轮未出现 `[frontier_llm]` 标记、模型不一致或认证失败；推理等级等运行元数据没有可核验记录，不补造。本轮只做只读取证和审阅：只写本报告；未改作者正文、来源记录、登记、修订映射、计划或前次报告；未部署 Volcano/Kueue/MindCluster/Slurm，未提交作业，未运行任何上游测试。模型审阅不构成平台或现场验证。

## 输入（以 SHA-256 识别）

| 输入 | SHA-256 |
|---|---|
| [T05-05 正文](../../knowledge/05-cluster-platform/admission-and-placement.md)（177 行） | `f63325bfec3d93e7249ed9f6e688e16dfe58eeba136f98cea8dd08d7c704889d` |
| [作者来源记录](batch-22-t05-05-sources.md)（22 行） | `80d20e0b2ac2e350c5af3b7081827e47dd72b6c46bf767d5d65df07d97651dfb` |
| [修订映射](batch-21-review-fixes.md)（T05-05 第四轮修订节 L388–394） | `61f17ac43a6f26d3562cf39e07d3d7f3306749182c19f0d7442ce2511b3fbc19`；L388–394 段 `d85ab1237b537a19b39b92bc240f34036c426b66c47066ccb8fc56f2f22cb4e1` |
| [前次复核报告](batch-22-t05-05-claude-recheck-3.md) | `946a01dd458bea53ddad393f2d7a87b60500af4dc706dbd054c32c775eea09be`（与本地会话记录中审阅者 Write 原稿一致，见“前次复核报告措辞勘误”） |
| [初审报告](batch-22-t05-05-claude-review.md) | `2095a6fe21717e2ef9ce6977e79c197e72ca11f1000904ad229f80dbf098cde1` |
| [任务计划](../../plans/full-coverage-backlog.yaml)（T05-05 acceptance L5569–5573） | `5f9bcf865b8c77e13cc8ee5f1c03140c37b86f558d8227d8bb2080249f4fcfc3`（与前次相同） |
| [来源登记](../../sources/registry.yaml)（444 项；T05-05 相关 L5463–5509，Slurm 文档 L5386–5396） | `b9cdbedf73379dd24d704e0363e1fcbcc550f3c8f9581b93659a32a1e39a6b0f`（与前次相同，本轮未改）；L5463–5509 段 `de6d0a9079431d077facc717ab1be8f99b14cbbc63d4b9c102da2b1c75d39f2a`；L5386–5396 段 `d9d09916c2e434db2911f785e376b427d08e10cc0763114f139f3f440f3cccf8` |
| 上一版正文与来源记录（由第三轮会话记录中的 Read 结果重建，未入库） | 规范化末尾空行后为 `b9e477c4a45d00d1…`、`2369f6cb0b21d0d4…`，与前次复核输入表逐字一致 |

任务给出的三个前缀（正文、来源记录、修订映射）均与实测一致；其余四项任务未给前缀，上表记录实测值。登记 444 项与任务所述一致。输入在开始时取哈希，成稿前复取一次，结果相同（见文末）。

## 本轮实际改动（上一版与现文件逐行比对）

把重建的上一版与现文件 `diff`，本轮改动只有以下 4 行，没有其他改动：

| 文件:行 | 改动 |
|---|---|
| 正文 L95 | “配置了 enqueue 动作时仍 Pending 的作业跳过 allocate”后插入“（L152–169）” |
| 正文 L169 | `DenyOnLimit` 前提后插入“分区未挂优先于作业 QOS 的 Partition QOS（除非作业 QOS 设了 `OverPartQOS`）、站点实际执行 QOS 限额（默认不设 `AccountingStorageEnforce` 时不按记账库限额执行）” |
| 来源记录 L10 | 登记 ID 列括注追加“；gangreclaim.go L32–52/L247 bundle 默认开” |
| 来源记录 L11 | util 链接文字改为 `job_controller_util.go L182–196/L286–288 applyPolicies`；其后新增 `job_controller_actions.go L813–816/L877–880` 链接及“（minAvailable 同步）”，再之后残留 `(https://…/job_controller_util.go)（默认 Sync）` |

来源记录 L3 方法句、正文其余行和登记都没有变化。

## 一次源抽查（审阅者独立获取）

方法：全部用 `curl -sSL` 默认 TLS 校验只读获取。HTTP 均为 200，本轮没有重试或失败。GitHub 文件经 `raw.githubusercontent.com` 按固定 commit 取回。HTML 去标签后按文字核对，不只判可达性。版本锚用 `git ls-remote` 取得。原文只放在临时目录 `/tmp/b22rc05d/`，未入库。

版本锚：Volcano `refs/tags/v1.15.0` 为 tag 对象 `4691eac388eb8ec033908cbe144b8f3aafcaeef7`，`^{}` 指向 commit `8fc394c11e8db0d0ada5c17816b58bced9d7213d`。Kueue `refs/tags/v0.19.0` 为 tag 对象 `7b3cad14a540cd256dc9c658be5a23fff809ff68`，指向 commit `911a822a49bcfd99c9c62203a009efa4130ad604`。两者与前几轮及登记一致。

本轮取回的 10 份文件/页面，SHA-256 全部与前次相同（下表记为“同前次”），说明上游未变，判定差异都来自作者修订。

### Volcano（commit `8fc394c1`）

| 文件 | SHA-256 | 核对点与结果 |
|---|---|---|
| `pkg/scheduler/actions/allocate/allocate.go`（973 行） | 同前次 `7eefa6ac…bc632` | L152 `for _, job := range ssn.Jobs`；L154–158：`job.IsPending()` 且 `conf.EnabledActionMap["enqueue"]` 时，日志 `skip allocate, reason: job status is pending` 后 `continue`；L159–163：否则日志 `no enqueue action is configured`，并就地设 `PodGroupInqueue`；L166–169：`JobValid` 不通过时 `continue`。**正文 L95 新增的 L152–169 覆盖该单元格前三个子句，区间正确**（C22） |
| `pkg/scheduler/actions/gangreclaim/gangreclaim.go`（263 行） | 同前次 `56b00681…66982` | L32–33 `AllowWholeBundleKey`；L37 `defaultWholeBundleOn = true`；L48 为空行，L49–52 `New()` 采用默认值；L247 仅当 `bundle.Type == utils.BundleWhole && !gr.allowWholeBundle` 时跳过。**来源记录 L10 新增的 `gangreclaim.go L32–52/L247` 正确**（C25、C30） |
| `pkg/scheduler/actions/gangpreempt/gangpreempt.go`（254 行） | 同前次 `440e6ff3…1694d` | 只比对哈希；L10 中 gangpreempt 区间本轮未改 |
| `pkg/controllers/job/job_controller_actions.go`（1137 行） | 同前次 `c2bc5da7…aaaed2` | L813 `MinMember: job.Spec.MinAvailable`，L816 `MinResources: cc.calcPGMinResources(job)`；L877 重算 `minResources`，L878–880 在不一致时同步 `MinMember`/`MinResources`（L881 `pgShouldUpdate = true`）。**来源记录 L11 新增的链接与区间正确**（C30） |
| `pkg/controllers/job/job_controller_util.go`（471 行） | 同前次 `e9632a06…e070b` | L182 `func applyPolicies`；L190–191 `default action is sync job`；L194–197：请求自带 action 时直接采用并返回（L197 为右花括号）；L286–288：`shouldConfigureTimeout` 只对 `PodPendingEvent` 成立。**来源记录 L11 的 `L182–196/L286–288` 正确**（前次已说明 L182–196 可接受）（C30） |
| `pkg/scheduler/api/job_info.go`（1537 行） | 同前次 `e8d19400…5823b` | L877–886 `ReadyTaskNum`；L1202–1204 `IsReady`；L1206–1208 `IsPipelined`。L10 区间未变，仍正确 |

### Slurm 24.11.7 归档

| 页面 | SHA-256 | 核对点与结果 |
|---|---|---|
| [qos](https://slurm.schedmd.com/archive/slurm-24.11.7/qos.html)（登记内） | 同前次 `f6b74df2…2ba5f` | Partition QOS 节原文：`the Partition QOS limits will override the job's QOS. If the opposite is desired you may configure the job's QOS with Flags=OverPartQOS which will reverse the order of precedence`；Flags 节原文：`OverPartQOS — If set, jobs using this QOS will be able to override any limits used by the requested partition's QOS limits`。**L169 的 Partition QOS/`OverPartQOS` 前提属实，句末“qos 页”出处成立**。`DenyOnLimit` 原文同前次。全页 `AccountingStorageEnforce` 共 5 处，都在 `UsageFactorSafe`/`Safe` 语境中，并指向 `See AccountingStorageEnforce in slurm.conf man page`。**本页没有该选项的默认值，也没有“未设则不执行限额”的原文**（C23） |
| [job_reason_codes](https://slurm.schedmd.com/archive/slurm-24.11.7/job_reason_codes.html)（登记内） | 同前次 `f8e4f3c9…1592a` | 原文：`QOSMaxGRESPerJob — The GRES request exceeds the maximum each job is allowed to use for the requested QOS`。L169 反例 reason 属实；本页不涉及 `AccountingStorageEnforce` |
| [slurm.conf](https://slurm.schedmd.com/archive/slurm-24.11.7/slurm.conf.html)（登记内，`src.slurm.docs-24.11.7` notes 列有 slurm.conf） | 同前次 `f4151769…a1ff34` | 原文：`AccountingStorageEnforce — This controls what level of association-based enforcement to impose on job submissions`，选项为 all/associations/limits/nojobs/nosteps/qos/safe/wckeys；`limits — Users can be limited by association to whatever job size or run time limits are defined`；`qos — Jobs will not be scheduled unless a valid qos is specified`。**条目内没有默认值，也没有“未设时限额不执行”的原文**（C23） |
| [resource_limits](https://slurm.schedmd.com/archive/slurm-24.11.7/resource_limits.html)（**未登记**） | 同前次 `5212b674…91992` | 原文：`In order to enforce scheduling policy, set the value of AccountingStorageEnforce`；`Without AccountingStorageEnforce being set (the default behavior) jobs will be executed based upon policies configured in Slurm on each cluster`。**L169 括注“默认不设 `AccountingStorageEnforce` 时不按记账库限额执行”的原文依据只找到这一处；登记中 `resource_limits` 为 0 处，正文中也为 0 处**（C23） |

### Kueue

本轮没有重取 Kueue 文件。理由：比对显示正文 L149–L155 自前次以来未改，门控名条件已在前次关闭；前次取回的 `workload_types.go`、`kube_features.go` 区间仍适用。

### 取证限制

- 只读了上表所列行区间与段落。proportion/capacity/overcommit 的 `JobEnqueueable` 公式、Kueue flavorassigner 的 reason 分支、Fair Sharing 策略细节仍未审计（与前次相同）。
- QOS 限额是否只依赖 `AccountingStorageEnforce` 的某个具体选项（如 `limits`），仍只有文档层证据，审阅者没有读 slurmctld 源码（与前次相同）。L169 没有点名具体选项，因此这一限制不影响本轮判定。
- 上一版正文与来源记录是从第三轮审阅会话的 Read 输出重建的。重建结果与前次复核输入哈希逐字一致，因此 diff 可靠；这份重建文件不是仓库内产物。
- 没有核对作者的 webfetch 取证过程本身；本报告的哈希不能写成作者的取证。

## 逐项判定

### B22-C22 — P1 / CLOSED

| 前次剩余条件 | 判定 | 位置证据 |
|---|---|---|
| 正文 L95 补 `allocate.go` L152–169 | 已落实 | L95 含“（L152–169）”，全文 1 处。L152–169 依次覆盖 Pending 且配置 enqueue 时跳过（L154–158）、未配置时就地转 Inqueue（L159–163）、`JobValid` 不通过时跳过（L166–169），与该单元格前三个子句一一对应 |

前次的另外两项条件（L94 enqueue 区间、L97 控制器区间）已在前次落实，本轮未改。

建议（非阻断）：“（L152–169）”现在挂在中间子句后面，但它同样支撑前面的 `JobValid` 子句和后面的“就地转 Inqueue”子句。可以挪到“未配置时就地转 Inqueue 继续”之后，或把链接文字改为 `allocate.go` L152–169/L313–336/L832–844@`8fc394c1`，让区间覆盖范围一目了然。

### B22-C23 — P1 / OPEN

| 前次剩余条件 | 判定 | 位置证据 |
|---|---|---|
| L169 补“该分区未设 Partition QOS 的每作业 GRES 上限（或作业 QOS 设 `OverPartQOS`）”，出处为 qos 页 Partition QOS 节 | 已落实 | L169 写“分区未挂优先于作业 QOS 的 Partition QOS（除非作业 QOS 设了 `OverPartQOS`）”，句末出处含“qos 页”，原文见上表。这比前次条件更强（要求没有 Partition QOS，而不只是它没定义每作业 GRES 上限），作为充分前提成立 |
| L169 补“站点实际执行 QOS 限额”。若点名具体选项并引用 resource_limits 页，须先登记该页；只写 unknown、不点名选项也可 | **未落实** | 前提句“站点实际执行 QOS 限额”已写。括注“（默认不设 `AccountingStorageEnforce` 时不按记账库限额执行）”点名了选项并写出默认行为，属于实质主张。句末出处只有 job_reason_codes 与 qos 页，两页都没有这句原文；登记内 slurm.conf 条目没有默认值；唯一原文在 resource_limits 页，而该页未登记（登记 0 处）、正文也未引用（正文 0 处）。本轮登记哈希与前次相同 |

这不是事实错误：括注内容与 resource_limits 页原文一致（“不按记账库限额执行”是对 `jobs will be executed based upon policies configured in Slurm on each cluster` 的合理转述）。缺的是可追溯、已登记的就近出处。修订映射 L391 把它写成“＋AccountingStorageEnforce 前提”，没有提到出处。

剩余关闭条件（二选一）：

- **A（不点名选项）**：把 L169 括注改为不含选项与默认行为的写法，例如“站点实际执行 QOS 限额（站点配置 unknown）”。
- **B（保留选项）**：在 L169 括注处就近链接 [resource_limits](https://slurm.schedmd.com/archive/slurm-24.11.7/resource_limits.html)，并把该页登记到 `src.slurm.docs-24.11.7` 的 revision/notes，写明支撑点（`Without AccountingStorageEnforce being set (the default behavior) …`）。只引用 slurm.conf 不够，该条目没有默认值。

建议（非阻断，前次已提，仍未改）：

- L149 末尾“否则只见 `Pending`，unknown”中的 unknown 指代不清，建议写成“站点是否开启 unknown”。
- 门控名旁可补 [kube_features.go L479–481、L788–789](https://github.com/kubernetes-sigs/kueue/blob/911a822a49bcfd99c9c62203a009efa4130ad604/pkg/features/kube_features.go#L479-L481) 链接。
- L167 的 `%R` 措辞：Pending 时 `%r`/`%R` 为等待原因；失败终止的作业 `%R` 为失败说明；其他状态（含 R）`%R` 为节点列表。

### B22-C25 — P2 / CLOSED

| 前次剩余条件 | 判定 | 位置证据 |
|---|---|---|
| 来源记录 L10 补 gangreclaim.go L32–52/L247 | 已落实 | L10 登记 ID 列括注“gangreclaim.go L32–52/L247 bundle 默认开”，与一次源一致；`L247` 全文 1 处 |
| （括注部分）L3 方法句同步改 | 未改；本轮降为非阻断 | L3 仍为“gangreclaim 同模型”；L10 的“精确页面/节”列也仍是“＋gangreclaim 同模型（bundle 默认开）”，没有链接 |

关闭理由（审阅者对前次条件括注部分的调整，在此明示）：

1. C25 的实质问题（抢占保护只对旧动作成立）已在前几轮改正，正文 L88 的 gangreclaim 区间自前次起正确。
2. 来源记录同一行现在已有精确区间，登记 L5493 也在同一 commit 下列有 gangreclaim.go，读者可以追溯。
3. 前次复核接受了 job_info.go 区间写在同一“登记 ID”列括注里（C30 第 4 条），本轮按同一标准处理。
4. L3 是方法概述，“同模型”的说法本身准确。

建议（非阻断）：把 gangreclaim 区间移到 L10 的“精确页面/节”列，写成 `gangreclaim.go L32–52/L247@8fc394c1` 链接，替换“gangreclaim 同模型”；L3 同步改。

### B22-C30 — P3 / CLOSED

| 前次剩余条件 | 判定 | 位置证据 |
|---|---|---|
| L11 补 job_controller_actions.go L813–816/L877–880 | 已落实 | L11 `[job_controller_actions.go L813–816/L877–880](…/pkg/controllers/job/job_controller_actions.go)（minAvailable 同步）`，链接固定在 `8fc394c1`，区间正确 |
| L11 util 补 L182–197/L286–288（L182–196 可接受） | 已落实 | L11 `job_controller_util.go L182–196/L286–288 applyPolicies`，区间正确 |
| gangreclaim.go L32–52/L247 | 已落实 | 同 C25 |

前次已落实的登记条件（URL 改 commit、tag 对象、job_info.go/job_controller_actions.go 纳入登记）本轮未改，仍成立。

编辑残留（非阻断，须清理）：L11 的 job_controller_actions 链接之后，多出 `(https://github.com/volcano-sh/volcano/blob/8fc394c1…/pkg/controllers/job/job_controller_util.go)（默认 Sync）`。这是上一版 util 链接的尾部 `](…job_controller_util.go)（默认 Sync）` 在改写链接文字时没有删掉，结果 L11 中 util URL 出现 2 次、“（默认 Sync）”出现 2 次。残留部分仍然指向 util、仍然标“默认 Sync”，出处没有挂错，所以不阻断；前次复核对 C24 的括号未闭合也按非阻断处理。但它不是 Markdown 链接语法，渲染后是一段带括号的裸 URL。修订映射 L393 没有提到这处残留。处理方式：删除该片段。

建议（非阻断，前次已提，仍未改）：登记 L5489 标题“调度动作实现（enqueue/allocate/gangpreempt）”现在还覆盖 gangreclaim.go 和非动作文件 api/job_info.go，可酌情更新标题或 notes。

## 前次复核报告措辞勘误

- **前次报告未被改动**：recheck-3 现文件 SHA-256 `946a01dd…` 与本地会话记录中审阅者的 Write 原稿完全一致，作者本轮没有改动审阅者报告，符合前次报告提出的流程意见。
- **“五个前缀”不准确**：recheck-3 L31 写的是“任务给出的五个前缀（正文、来源记录、修订映射、登记，及前次报告无前缀）中，四个给定前缀均一致”。第三轮任务原文（本地会话记录）共列 7 项输入，其中给了前缀的只有 4 项：正文 `b9e477c4…`、来源记录 `2369f6cb…`、修订映射 `5810b936…`、登记 `b9cdbedf…`；前次报告、初审报告、计划 3 项都没有前缀。“五个”既不是输入数（7），也不是前缀数（4）。
- **当时的自我更正没有落盘**：审阅者在第三轮成稿约 8 秒后，曾尝试把该句改为“任务给出的四个前缀（正文、来源记录、修订映射、登记）均一致；前次报告、初审报告与计划未给前缀”，但因写权限未获批没有落盘。修订映射 L394 及本轮任务说明认为“原文已准确，改动反而失实”，这个判断不成立；不过作者不改审阅者报告的做法是对的。
- **权威勘误**：recheck-3 L31 应读作上一条中“四个前缀……”那一句。这只涉及输入核对说明，不影响 recheck-3 的任何判定与计数。按任务约束，本报告不回改 recheck-3。

## 修订映射与落盘差异

[修订映射](batch-21-review-fixes.md) L388–394 标题注明“逐条 grep 已核对”。逐条对照如下：

| 映射条目 | 落盘情况 |
|---|---|
| L390 C22“L95 补 allocate L152–169” | 一致 |
| L391 C23“Partition QOS/OverPartQOS＋AccountingStorageEnforce 前提；门控名三处齐全” | 前提已写，但 `AccountingStorageEnforce` 括注缺登记出处（见 C23）。门控名 `UnadmittedWorkloadsObservability` 实际只出现 2 处（L149、L150）；L152、L155 用“开门控”“同上门控条件”回指，没写名字。门控名条件前次已关闭，此差异不影响判定 |
| L392 C25“gangreclaim L247（正文＋记录）” | 一致（L10 登记 ID 列括注；L3 未改，映射也没有声称改了） |
| L393 C30“job_info/actions/util 行区间入记录；登记已含文件” | 区间一致；L11 编辑残留未提及（见 C30）；登记本轮未改，与“登记已含文件”相符 |
| L394“recheck-3 报告‘五个→四个’措辞未改，原文已准确” | “未改”属实（哈希一致）；“已准确”不成立（见上节） |

与前两轮相比，本轮映射与文件基本一致，没有再出现“映射写了、文件里没有”的情况。

## acceptance 对照

| acceptance | 判定 | 未关闭项 |
|---|---|---|
| 1 以固定 Volcano 实现解释 minMember/minResources、成组决策、启动失败、重排队/回退及与 rendezvous 的不同 | 满足：C22、C24、C25、C30 均已关闭，本轮抽查的 Volcano 行区间全部属实 | — |
| 2 Kueue 与 Slurm 两个独立配置/状态样板；选择依据与公平性代价分开 | 满足 | — |
| 3 每个样板的资源向量、拓扑、碎片、配额、运行进展观测，失败或不适用反例及对照验收 | 实质满足：样板 B 的 QOS 配对前提已补全，只剩一处括注的出处 | C23 |
| 4 MindCluster 边界；链接 idle-resource-job-waiting-triage 与 Slurm 状态参考；不是统一推荐策略 | 满足（L177 未变） | — |

`verification.status: source_checked`：初审要求 C22–C25 关闭前不把 Volcano 部分视为成立。现在与 Volcano 相关的 C22、C24、C25 都已关闭（C23 涉及 Kueue/Slurm 样板），这一保留可以解除。解除只表示源码与文档层面的核对成立，不代表 reproduced。

## 结论

**T05-05 第四次定向复核不通过。本轮范围 4 项：CLOSED 3（C22 为 P1；C25 为 P2；C30 为 P3），OPEN 1（C23，P1）。B22-C22–C30 合计 CLOSED 8、OPEN 1。不新增发现 ID，无新事实错误追记。**

- 关闭剩余项只需改一处：正文 L169 的 `AccountingStorageEnforce` 括注，或改成不点名选项的 unknown 写法（方案 A），或就近引用 resource_limits 页并登记（方案 B）。
- 下一轮修订建议一并处理以下非阻断项（不影响关闭）：删除来源记录 L11 的编辑残留；把 gangreclaim 区间移到 L10“精确页面/节”列并同步 L3；以及 C22、C23、C30 下列出的其他建议。前次遗留的 L88 全角括号未闭合（`（` 13 个、`）` 12 个）和 L85–87 三个空行也仍未改。
- 正文没有虚构命令输出或实测结果，对照验收都标了“设计，未执行”，MindCluster 边界保持得当。
- 修订后须再做一次 C23 定向复核。本复核只覆盖编辑与来源层面；文中 Volcano/Kueue/Slurm 行为都是源码或文档层证据，审阅者未部署、未运行，不得标为 reproduced。

## 检查记录

- 成稿前复取输入哈希：七个输入文件与“输入”表逐字一致，复核期间输入未变。
- `make check`：`PASS: 96 content entries; 444 sources.`（成稿前运行；`check` 分支不写文件）。它只校验结构与本地链接，不说明技术正确性，也不访问远程链接。
- 未运行 `make build`：本轮只新增 `docs/research/` 下的审阅报告，按任务约束不改其他文件，也不生成 `build/` 产物。
