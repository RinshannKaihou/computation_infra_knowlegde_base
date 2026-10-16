# 第二十二批 T05-02 第四次定向复核（作者第四轮修订后）

复核日期：2026-10-14（实际取证日）。

**结论：不通过。范围内 2 项（B22-C04、C10）：CLOSED 1（C04），OPEN 1（C10）。连同前三轮已关闭的 9 项（C01–C03、C05–C09、C11），B22-C01–C11 合计 CLOSED 10 / OPEN 1。** 未新增发现 ID，本轮也没有按原 ID 追记的事实错误。C10 剩下的都是出处与登记问题，所涉事实均已核实属实：

- `reconciler.go` 已在正文挂链接，但登记和来源记录都还没写入这个文件。
- L130 的 FailureRecoveryPolicy"Alpha 默认关"在正文任何位置都找不到出处。

审阅者角色独立于作者修订角色。审阅模型为 `claude-opus-5-5`，由用户明确要求试用；这不是既有的 `gpt-6.1-sol / xhigh` 批量审阅约定，也不改写该约定。本会话内未见 `[frontier_llm]` 标记、认证失败或模型自报变化。审阅者无法在会话内读取 `modelUsage` 等运行元数据，也不补造。若操作方在运行记录中发现多键或模型不一致，按约定本轮作废，不留档、不引用。

本轮只写本报告一个文件。未改作者正文、来源记录、登记、索引或计划；未部署集群、未提交 Job、未运行任何测试。模型审阅不构成平台或现场验证。

## 输入（以 SHA-256 识别）

| 输入 | SHA-256 | 与任务给定前缀 |
|---|---|---|
| [T05-02 正文](../../knowledge/05-cluster-platform/kubernetes-job-lifecycle.md)（155 行，与前次相同） | `3313662d4e7952fb56471a5d0dc7379298b370ad668b2a89b7f7be136bd8c88d` | 一致 |
| [作者来源记录](batch-22-t05-02-sources.md)（26 行，与前次相同） | `a87084b81758697ffbba07004238dcbe0b2fb8a8f778406341a8df09ce589685` | 一致 |
| [修订映射](batch-21-review-fixes.md)（T05-02 第四轮修订节 L346–349） | `168cbf4d0598a29ad9eec0be9b4843e15f0131c65a6056958fdc431a369825ed` | 一致 |
| [前次复核报告](batch-22-t05-02-claude-recheck-3.md)（剩余关闭条件权威来源） | `cf92d67d487f14f5c61ef63a679e92d9bec41054e32e2b1ebf343d0270f395ea` | 任务未给前缀，记实值 |
| [初审报告](batch-22-t05-02-claude-review.md) | `082ad71dcf190c6846bd3de87f632f02f083eb28b80146a8b11c4a44406e1420` | 任务未给前缀；与前三轮所记相同 |
| [任务计划](../../plans/full-coverage-backlog.yaml)（T05-02 acceptance 4 条） | `5f9bcf865b8c77e13cc8ee5f1c03140c37b86f558d8227d8bb2080249f4fcfc3` | 任务未给前缀；与前四轮相同，计划未变 |
| [来源登记](../../sources/registry.yaml)（440 项；本文相关条目 L559–572、L5347–5385、L5430–5440） | `8d59b5c88cacc70432b93e0b1763ad89d83821bebe53d4964d3a66027b7c5f8a` | 任务未给前缀；与前次复核所记逐字节相同，本轮修订未改登记 |

七个输入在取证开始和成稿前各哈希一次，结果相同。正文与来源记录是未跟踪文件，没有上一轮副本可做 diff。本轮按落盘现状对照前次剩余关闭条件判定，修订映射只用作核对线索。

## 取证方法与限制

- **取证方式**：
  - 全部用 `curl -sSL` 只读获取，默认 TLS 校验（`ssl_verify_result=0`），下列原文 HTTP 均为 200。
  - 版本锚用 `git ls-remote`：Kueue `refs/tags/v0.19.0^{}` 为 `911a822a49bcfd99c9c62203a009efa4130ad604`，Kubernetes `refs/tags/v1.32.0^{}` 为 `70d3cc986aa8221cd1dfb1121852688902d3bf53`，与登记和前四轮一致。
  - HTML 去标签后按文字核对，不只判可达性。
  - 原文放在新建临时目录 `/tmp/b22rec4/`（取证前不存在），未入库。
  - 未使用 GitHub API。
- **与前次复核逐字节比对**：本轮重取 15 个前次已记哈希的文件，全部字节一致，因此前次报告中的行号在本轮仍有效。
  - Kueue 侧：v1beta2 `clusterqueue_types.go` `6092ac24…`、`localqueue_types.go` `b0f37660…`、`kube_features.go` `225c13d6…`、`workload.go` `ccbff32a…`、`jobframework/reconciler.go` `f92d8294…`、setup_object_retention_policy `4c688b65…`、jobs.md `9ff23de3…`、setup_failure_recovery `499ea5b7…`、setup_wait_for_pods_ready `c57c86c1…`、cluster_queue.md `7b35c9f7…`、集成测试 `cc9a477e…`。
  - K8s 侧：`strategy.go` `60591891…`、`storage.go` `bf36a996…`、GC 页 `3bb19013…`、owners-dependents `462bf102…`。
- **本轮新增取证**：

  | 来源 | 位置 | SHA-256 | 用途 |
  |---|---|---|---|
  | Kueue `pkg/constants/constants.go`@911a822a | [链接](https://github.com/kubernetes-sigs/kueue/blob/911a822a49bcfd99c9c62203a009efa4130ad604/pkg/constants/constants.go) | `24ce8fc04de3b933de4898f6fed6e373b208236450d853e438160db81a687974` | L87–88 `ElasticJobAnnotation` → C10（L84 注解要求） |
  | Kueue `pkg/controller/constants/constants.go`@911a822a | 同 commit | `846f1559130e17d8f002229bbf0755a4538745a7ade767088b3bdef43903378a` | 检索 `ElasticJobAnnotation` 0 命中，排除该文件 |

- **链接可达性**：正文与来源记录共有 29 个不重复外链（前次 28 个，加上新增的 `reconciler.go`），逐个用 curl 打开，首次即全部 HTTP 200，`ssl_verify_result=0`。
- **结构校验**：运行了 `make check`，设 `PYTHONDONTWRITEBYTECODE=1`，结果 `PASS: 96 content entries; 440 sources.`。该目标只读，前后 `git status --porcelain` 哈希相同。它只校验结构与本地链接，不校验技术正确性或远程内容。
- 限制：
  - 测试只读了下表列出的行，未执行，CI 结果未查。
  - K8s 文档网站的源提交未固定，按 v1.32 快照 HTML 文字核对。
  - 未运行 `make build`，因为它会写 `build/`，与"只写本报告"冲突。

### 关键抽查点（原文文字核对）

| 抽查点 | 原文 | 结果 |
|---|---|---|
| setup_object_retention_policy L10–14、L125–126 | L12–13 `By default, Kueue leaves all Workload objects in cluster indefinitely`；L125 为空行，L126 `### Scenario B: Evicted Workload via waitForPodsReady` | L68 主语已改为 Kueue → C04；L68 的"见 L125"按本文行号惯例会被读作该页 L125 → C04 非阻断 |
| GC 页 | `By default, Kubernetes uses background cascading deletion unless you manually use foreground deletion or choose to orphan the dependent objects.`；`By default, Kubernetes deletes dependent objects.` | L68"被 GC 级联删除的情形"与 L125 的 GC 分支一致 → C04 |
| `jobframework/reconciler.go` L1476 | `if err := ctrl.SetControllerReference(object, wl, c.Scheme()); err != nil {` | L125 新增链接与行号属实 → C04、C10 |
| v1beta2 `clusterqueue_types.go` L132–144 | L132 `stopPolicy - if set to a value different from None, the ClusterQueue is considered Inactive`；L137–139 `None - Workloads are admitted`、`HoldAndDrain - Admitted workloads are evicted and Reserving workloads will cancel the reservation.`、`Hold - Admitted workloads will run to completion and Reserving workloads will cancel the reservation.`；L141 `Enum=None;Hold;HoldAndDrain`；L144 `StopPolicy *StopPolicy` | L80 新增链接与所标行号属实，正文三值、Inactive 与 Hold 引文逐字对上 → C10 |
| `localqueue_types.go` L45–51 | 与 ClusterQueue 相同的 HoldAndDrain/Hold 注释与 Enum；L51 `StopPolicy *StopPolicy` | LocalQueue 侧未加链接，前次已定为由作者决定 → C10 非阻断 |
| `kube_features.go` L545–547、L601–603、L757–758 | L545 `PartialAdmission: {`，L546 0.4 Alpha false，L547 0.5 Beta true；L601 `ElasticJobsViaWorkloadSlices: {`，L602 0.13 Alpha false，L603 0.18 Beta true；L757 `ConcurrentAdmission: {`，L758 0.18 Alpha false | L84 新增三处链接与行号属实，均含前次所列 L547、L602–603、L758 → C10 |
| `kube_features.go` L682–683 | L682 `FailureRecoveryPolicy: {`，L683 `{Version: version.MustParse("0.15"), Default: false, PreRelease: featuregate.Alpha}` | 正文所有 `kube_features.go` 链接的行号（L479–481、L788–789、L545–547、L601–603、L757–758）都不含此处 → C10 |
| setup_failure_recovery L28–29 | `A running Kueue installation at **v0.15** or newer.`；`The FailureRecoveryPolicy feature gate enabled in the Kueue controller manager.`；全页检索 alpha（不分大小写）0 命中 | L62 的链接只支撑"v0.15+、需开门控"，不支撑 L130 的"Alpha 默认关" → C10 |
| jobs.md L222、L226–229；`workload.go` L1565；`pkg/constants/constants.go` L88 | jobs.md `feature-state state="alpha" for_version="v0.13"`，`The ElasticJobsViaWorkloadSlices feature gate is set to true`，`The Job is annotated with kueue.x-k8s.io/elastic-job: "true"`；`return features.Enabled(features.ElasticJobsViaWorkloadSlices) && wl.GetAnnotations()[constants.ElasticJobAnnotation] == "true"`；`ElasticJobAnnotation = "kueue.x-k8s.io/elastic-job"` | L84"仍需逐 Job 加注解"与"页头仍标 v0.13 alpha"属实，L82 已链接的 jobs.md L222–240 覆盖 L229 → C10 |
| v1.32.0 `strategy.go` L62–74；`storage.go` L56–57 | L67–70 `case batchv1.SchemeGroupVersion: // for back compatibility return rest.OrphanDependents`；`child pods are preserved by default when jobs are deleted; set propagationPolicy=Background to remove them …` | 来源记录 L16 的归属与所标行号属实，与登记 L5380 一致 → C10 |
| 登记 L5366、L5374、L572；来源记录 L15 | L5366 revision 只列到 `kube_features.go（门控阶段/默认值）、pkg/workload（reason 回退/Elastic 判定）与 job 控制器测试函数行号`；L5374 notes 无 jobframework；`src.kueue.admission-v0.19.0` 的 L572 只有第八批的 `jobframework events`；来源记录检索 `reconciler`、`jobframework` 均为 0 命中，L15 只列 `kube_features.go 与 pkg/workload` | `reconciler.go` 未写入登记范围与来源记录 → C10 |

## 逐项判定

### B22-C04 — CLOSED

位置证据：前次只剩一条关闭条件（追记的 L68 与 L125 矛盾），本轮已落实。

- **主语**：L68 现为"Workload 对象 Kueue 默认不主动删除（`leaves all Workload objects in cluster indefinitely`，主语是 Kueue；被 GC 级联删除的情形见 L125 取消分支）"。主语已从"Workload 对象"改回 Kueue，与 retention 页 L12–13 原文一致。
- **与 L125 一致**：L68 明确承认 Workload 会被 GC 级联删除，与 L125"Background/Foreground 下 Workload 作为依赖被 GC 删除；Orphan 下保留…；Kueue 默认不主动删已完成/去活 Workload 指非 GC 行为"相互一致。这两处所依据的 `reconciler.go` L1476、GC 页默认 background、`strategy.go` L67–70 均经本轮重取核对属实。前次所指的"删 Job 后 Workload 默认一直保留"的读法已不成立。
- **其余部分**：L88、L125 的 It 名、测试归类与测试细节，与前次核对时的原文逐字节相同，本轮未发现回退。

非阻断（建议与 C10 同轮处理）：

- **L68 的"见 L125"是正文唯一一处指向本文件自身行号的引用**。本文其余"L<n>"都指上游原文行号，例如"测试 L2365""admission 页 L17–24"。这一处紧跟在 retention 页引文之后，读者会按惯例把它读作 retention 页 L125，那里是 L126 `### Scenario B: Evicted Workload via waitForPodsReady`。该场景讲的是去活 Workload 被回收后级联删 Job，方向正好相反；而 L68 句末还写了"见 retention 场景 B"，更容易让人这样理解。另外，Markdown 行号在构建产物中不可见，正文一改就会漂移。
  - 建议改为"见核对方法第 2 步取消分支"，或用页内锚点链接。
  - 事实本身无误：当前源文件第 125 行确为该分支，且"取消分支"可在页内检索到，因此不阻断关闭。
- **前次已记、仍未改**：L125"测试 L4042"可注明"测试以手动清空 ownerReferences 模拟孤立"（集成测试 L4072–4080）。

### B22-C10 — OPEN

已落实（对照前次三条剩余关闭条件）：

1. **第 1 条**：来源记录 L16 已写明"`strategy.go` L62–74 删除默认孤立、`storage.go` L56–57 默认保留子 Pod，均归本条目"，即归 `src.kubernetes.job-controller-tests-v1.32.0`，与登记 L5380 的 revision 一致，所标行号属实。
2. **第 2 条前半（L80 stopPolicy）**：L80 已链接 v1beta2 `clusterqueue_types.go` L132–144，所标行号与正文三值、Inactive 判定、`Admitted workloads will run to completion` 引文逐字对上。LocalQueue 侧 `localqueue_types.go` L51 未链接，属前次所定的作者可选项。
3. **第 2 条后半之 L84**：L84 新增 `kube_features.go` L545–547（PartialAdmission）、L601–603（ElasticJobsViaWorkloadSlices）、L757–758（ConcurrentAdmission）三处链接，行号属实，都包含前次所列的行。
   - 前次所列的 `workload.go` L1561–1566 未链接。不过 L84"仍需逐 Job 加 `kueue.x-k8s.io/elastic-job: "true"` 注解"在页面层已有出处：L82 已链接 jobs.md L222–240，覆盖 L229 `The Job is annotated with kueue.x-k8s.io/elastic-job: "true"`；L84 同一括注也点名 jobs.md。
   - 按 AGENTS.md"cite exact supporting pages … near substantive claims"，该主张已满足，代码链接降为非阻断。
4. **第 3 条前半**：L125 已链接 `jobframework/reconciler.go` L1476 并引 `SetControllerReference`，行号与原文属实，链接可达。

剩余关闭条件：

1. **`reconciler.go` 未写入登记范围与来源记录**（前次第 3 条后半）。
   - 登记与前次复核逐字节相同。`src.kueue.job-lifecycle-v0.19.0` 的 revision（L5366）与 notes（L5374）仍只覆盖 `kube_features.go`、`pkg/workload` 与测试行号，不含 `pkg/controller/jobframework`。
   - 来源记录检索 `reconciler`、`jobframework` 均为 0 命中，Kueue 行（L15）只列到 `kube_features.go 与 pkg/workload`。
   - `src.kueue.admission-v0.19.0` 的 L572 虽有 `jobframework events`，但那是第八批对事件的读取记录，没有点名 `reconciler.go`，也没有写属主关系，不能替代。
   - 需在 `src.kueue.job-lifecycle-v0.19.0` 的 revision 中写入 `pkg/controller/jobframework/reconciler.go`（L1476，Job 为 Workload 的 controller owner），并在来源记录 L15 的 Kueue 行同步。
   - 修订映射 L349 只写了"L125 reconciler owner 出处"，没有声称已改登记，与落盘状态一致，所以这是未完成，不是映射失实。
2. **L130 的 FailureRecoveryPolicy"v0.15 Alpha 默认关"无出处**（前次第 2 条后半中的 L130 部分）。
   - "Alpha"与"默认关"只见于 `kube_features.go` L682–683。正文所有 `kube_features.go` 链接的行号都不含这两行。
   - L62 所链 setup_failure_recovery 只写 `v0.15 or newer` 与需开门控（L28–29），全页没有 alpha 字样。
   - 需在 L130（或 L62）链接 `kube_features.go` L682–683。
   - L130 另三个 Kueue 门控（PartialAdmission、ElasticJobsViaWorkloadSlices、Concurrent Admission）在同页 L84 已有逐行链接，读者能找到出处，不阻断。如加指引，宜用节名或锚点，不用本文行号（理由见 C04 非阻断）。

非阻断：

- L84 可补 `workload.go` L1565 或 jobs.md L226–229 的直接链接，让注解要求与代码判定紧邻。
- 前次已记、仍未改：
  - L82"达 `backoffLimitCount` 后去活见 setup_wait_for_pods_ready L107–110"仍是纯文本（该页在 L115 已有链接）。
  - frontmatter `verification.notes`（L29）未包括 setup_* 三页、metrics、`kube_features.go`、`workload.go`、`reconciler.go`（检索 0 命中），且仍写"经 webfetch…curl 字节级取回未执行"，与正文实际依据不同步。
  - 登记 `src.kubernetes.job-controller-tests-v1.32.0` 标题（L5376）仍为"（存在性）"，license notes（L5384）仍写"只链接并记录存在性"，而 revision（L5380）已写"上游行为样本"并收录 `strategy.go`/`storage.go` 与 Kueue 测试行号。Kueue 测试仍建议统一归到 Kueue 条目。
  - C09 遗留：`backoffLimitPerIndex`"默认开"只能由 v1.32 Feature Gates 页支撑，该页仍未在正文链接，也不在登记范围内。

## 修订映射核对

映射 L346–349 与落盘状态对照：

- C04"L68 Workload 保留改 Kueue 不主动删（与 L125 GC 区分）"：与正文 L68 一致。
- C10"L80 stopPolicy 出处"：与 L80 一致。
- C10"L125 reconciler owner 出处"：与 L125 一致。映射只声称改了正文，没有声称改登记和来源记录，与落盘一致。
- C10"记录 strategy/storage 归属"：与来源记录 L16 一致。
- **映射漏记一处已落盘改动**：L84 的三处 `kube_features.go` 链接。前次复核时该链接只在 L80，本轮 L84 已补，映射未列。属少报，不是失实。
- **节标题计数有误**：标题写"claude 第三次定向复核 6/9"，但第三次复核的结果是范围内 CLOSED 1/3、合计 CLOSED 9/11。"6/9"是第二次复核的数字，应是沿用上一节标题。不影响判定，建议更正。
- 登记哈希与前次复核所记相同，本轮未改登记，与映射一致。

## acceptance 对照

| acceptance | 判定 | 未关闭发现 |
|---|---|---|
| 1 UID、generation/attempt、控制器责任与状态转移；区分 API 接收/admitted/Running/应用 ready/持续进展 | 满足。与前次相同 | —（C10 横向） |
| 2 backoff/deadline/retry/replacement、删除/finalizer、退出/回收与配额撤销；行为绑定版本 | 基本满足。L68 与 L125 已一致（C04 关闭）；L80、L84 的 Kueue 字段与门控已有逐行出处；只剩 L130 的 FailureRecoveryPolicy 阶段与默认值无出处 | C10 |
| 3 三视图对齐表、关键事件、卡住/重试/清理的下一项检查 | 满足。与前次相同 | —（C10 横向） |
| 4 终止/重试/取消后账本与应用结果核对、官方测试/例子；训练恢复归应用 | 满足。取消分支的属主前提已在正文挂 `reconciler.go` L1476，"训练恢复归应用"仍写明（L126）；该文件尚未写入登记范围 | —（C10 横向） |

横向问题：C10（`reconciler.go` 的登记与来源记录；L130 门控出处）。

## 结论

**T05-02 第四轮修订后第四次定向复核不通过：范围内 CLOSED 1/2（C04），OPEN 1/2（C10）；B22-C01–C11 合计 CLOSED 10/11、OPEN 1/11。**

- C04 的最后一条关闭条件（L68 改为以 Kueue 为主语，消除与 L125 的矛盾）已落实，经本轮独立重取核对属实。
- 正文已无未关闭的事实问题。C10 剩下三处出处与登记改动，所涉事实均已核实属实：
  1. 登记 `src.kueue.job-lifecycle-v0.19.0` 的 revision（L5366）写入 `pkg/controller/jobframework/reconciler.go`（L1476）；
  2. 来源记录 L15 的 Kueue 行同步写入该文件；
  3. L130（或 L62）链接 `kube_features.go` L682–683，作为 FailureRecoveryPolicy"v0.15 Alpha 默认关"的出处。
- 建议同一轮顺手处理：
  - L68 的"见 L125"改为节名或锚点（C04 非阻断）；
  - 修订映射第四轮节标题的计数；
  - 前次遗留的非阻断项。
- 修订后只需对 C10 上列三条做定向复核；如 L68 一并改动，顺带确认。
- 本复核只覆盖编辑与来源层面。文中 Kubernetes/Kueue 行为都是文档或源码层证据，不得标为 reproduced；正文 `verification.status: source_checked` 在 C10 关闭前只能视为大部分成立。
