# 第二十二批 T05-02 第五次定向复核（作者第五轮修订后，仅 C10）

复核日期：2026-10-14（实际取证日，取证结束于 2026-10-14T15:17:56Z）。

**结论：通过。范围内 1 项（B22-C10）CLOSED。连同前四轮已关闭的 10 项（C01–C09、C11），B22-C01–C11 合计 CLOSED 11 / OPEN 0。** 前次列出的三条剩余关闭条件均已落实，位置证据见下。未新增发现 ID。有两处与前次关闭条件的字面表述不一致，判为非阻断：

- 来源记录把 `reconciler.go` 写进了 L16（官方测试入口行），而不是前次指定的 L15 Kueue 行。该处写明"归 src.kueue.job-lifecycle-v0.19.0"，与登记一致。
- 修订映射写"记录 L15 同步"，实际落盘位置是 L16，L15 未变。

审阅者角色独立于作者修订角色。审阅模型为 `claude-opus-5-5`，由用户明确要求试用；这不是既有的 `gpt-6.1-sol / xhigh` 批量审阅约定，也不改写该约定。本会话内未见 `[frontier_llm]` 标记、认证失败或模型自报变化。审阅者无法在会话内读取 `modelUsage` 等运行元数据，也不补造。若操作方在运行记录中发现多键或模型不一致，按约定本轮作废，不留档、不引用。

本轮只写本报告一个文件。未改作者正文、来源记录、登记、修订映射或计划；未部署集群、未提交 Job、未运行任何测试。模型审阅不构成平台或现场验证。

## 输入（以 SHA-256 识别）

| 输入 | SHA-256 | 与任务给定前缀 |
|---|---|---|
| [T05-02 正文](../../knowledge/05-cluster-platform/kubernetes-job-lifecycle.md)（155 行） | `15a1b70e514126d87fc9fa2c4b56f4e290f0acadfd9e0c4791f14be58e75b09b` | 一致 |
| [作者来源记录](batch-22-t05-02-sources.md)（26 行） | `6abf163bfda7fdd1e36667273b86d9e7e1411755635bfb9b3946af1baa0dede9` | 一致 |
| [修订映射](batch-21-review-fixes.md)（T05-02 第五轮修订节 L351–353） | `3cb08a2824862fdbcd512546b2440b4d10a78d250cd5df662e18764aae8163e7` | 一致 |
| [前次复核报告](batch-22-t05-02-claude-recheck-4.md)（C10 剩余三条的权威来源） | `dc92ee5d0eac554ed7132a3061fe94f0b461e0e197c3211d391251ac0c15692c` | 任务未给前缀，记实值 |
| [来源登记](../../sources/registry.yaml)（440 项；相关条目 L559–572、L5361–5374、L5375–5385） | `756344f57ed602e862ed8b6ce64bfccba6c4e827243fc241c72812d2347a854f` | 任务未给前缀；与前次所记 `8d59b5c8…` 不同，与映射所称"登记 reconciler.go 归属"相符 |
| [任务计划](../../plans/full-coverage-backlog.yaml)（仅用于 acceptance 对照） | 前缀 `5f9bcf865b8c77e1` | 任务未列；与前五轮相同 |

五个任务输入在取证开始和成稿前各哈希一次，结果相同。正文与来源记录是未跟踪文件，登记在 HEAD 中不含第二十二批条目，三者都没有上一轮副本可做 diff。本轮按落盘现状对照前次三条剩余关闭条件判定，修订映射只用作核对线索。"L15 未变"是把当前 L15 与前次报告逐字引用的 L15 文字对照得出的。

## 取证方法与限制

- **取证方式**：
  - 全部用 `curl -sSL` 只读获取，默认 TLS 校验（`ssl_verify_result=0`）。
  - 版本锚用 `git ls-remote`：Kueue `refs/tags/v0.19.0^{}` 为 `911a822a49bcfd99c9c62203a009efa4130ad604`，Kubernetes `refs/tags/v1.32.0^{}` 为 `70d3cc986aa8221cd1dfb1121852688902d3bf53`，与登记及前五轮一致。
  - 原文放在新建临时目录 `/tmp/b22rec5/`（取证前不存在），未入库。未使用 GitHub API。
- **与前次复核逐字节比对**：本轮重取 4 个前次已记哈希的文件，全部字节一致，因此前次报告中的行号在本轮仍有效。
  - `pkg/features/kube_features.go` `225c13d6…`
  - `pkg/controller/jobframework/reconciler.go` `f92d8294…`
  - setup_failure_recovery `499ea5b7…`
  - jobs.md `9ff23de3…`
- **本轮新增取证**：用 `git fetch --depth 1 --filter=blob:none` 只取 commit `911a822a` 的树对象，再用 `git ls-tree -r --name-only` 列出全树。全仓库只有一个名为 `reconciler.go` 的文件，即 `pkg/controller/jobframework/reconciler.go`。据此可判断登记中缩写的 `jobframework/reconciler.go` 没有歧义。
- **链接可达性**：正文与来源记录共有 29 个不重复外链，与前次数量相同。来源记录新增的 `reconciler.go` 链接与正文 L125 同址，L130 新增链接与正文其余 `kube_features.go` 链接同址。
  - 第一轮：28 个 HTTP 200；GitHub blob 页 `…/911a822a…/site/content/en/docs/tasks/run/jobs.md` 返回 HTTP 503。
  - 该链接间隔 3 秒连续重试 3 次，均为 HTTP 200、`ssl_verify_result=0`。同 commit 的 raw 文件为 HTTP 200，哈希 `9ff23de3…` 与前次相同。判为 GitHub 暂时性错误。
- **结构校验**：运行了 `make check`，设 `PYTHONDONTWRITEBYTECODE=1`，结果 `PASS: 96 content entries; 440 sources.`。前后 `git status --porcelain` 哈希相同（`b20557d2521a781a`）。该目标只校验结构与本地链接，不校验技术正确性或远程内容。
- **限制**：
  - 未运行 `make build`，因为它会写 `build/`，与"只写本报告"冲突。
  - 测试与 CI 均未执行、未查。
  - 登记只核对了本文相关条目，其余条目不在本轮范围。

### 关键抽查点（原文文字核对）

| 抽查点 | 原文 / 落盘文字 | 结果 |
|---|---|---|
| `kube_features.go` L682–684 | L682 `FailureRecoveryPolicy: {`；L683 `{Version: version.MustParse("0.15"), Default: false, PreRelease: featuregate.Alpha},`；L684 `},` | 该门控只有 0.15 Alpha、默认 false 一条阶段记录，之后没有升级记录，因此 v0.19.0 下"v0.15 Alpha 默认关"成立 → C10 第 3 条 |
| `kube_features.go` L544、L273 | L544 `var defaultVersionedFeatureGates = map[featuregate.Feature]featuregate.VersionedSpecs{`；L272–273 `// Enabled failure recovery of pods stuck in terminating state.`、`FailureRecoveryPolicy featuregate.Feature = "FailureRecoveryPolicy"`；全文件 `FailureRecoveryPolicy` 只命中 L273 与 L682 | L682 位于默认版本化门控表内，不在别的表 → C10 第 3 条 |
| setup_failure_recovery | 全页检索 alpha（不分大小写）0 命中 | 与前次相同：L62 的链接不支撑"Alpha 默认关"，由 L130 新链接支撑 → C10 第 3 条 |
| `reconciler.go` L1476 | `if err := ctrl.SetControllerReference(object, wl, c.Scheme()); err != nil {` | 与前次相同；登记与来源记录所标行号属实 → C10 第 1、2 条 |
| commit `911a822a` 全树 | `reconciler.go` 只此一处：`pkg/controller/jobframework/reconciler.go` | 登记缩写路径唯一 → C10 第 1 条 |
| 登记 L5366（`src.kueue.job-lifecycle-v0.19.0` revision） | `…kube_features.go（门控阶段/默认值）、pkg/workload（reason 回退/Elastic 判定）、jobframework/reconciler.go L1476（Workload controller owner）与 job 控制器测试函数行号经只读核对 2026-10-14…` | 已写入 → C10 第 1 条 |
| 来源记录 L15、L16 | L15 仍以 `…/kube_features.go 与 pkg/workload（门控阶段/默认值、reason 回退）` 结束，与前次引用相同；L16 第三列新增 `Kueue [reconciler.go L1476](…/pkg/controller/jobframework/reconciler.go)（`SetControllerReference`，Workload controller owner 为 Job，归 src.kueue.job-lifecycle-v0.19.0）`；全文件 `reconciler` 只在 L16 命中，`jobframework` 只在该行 URL 中出现 1 次 | 已写入，但在 L16 不在 L15 → C10 第 2 条（非阻断偏离） |
| 正文 L130 | `FailureRecoveryPolicy（v0.15 Alpha 默认关（[kube_features.go L682–683](…/pkg/features/kube_features.go)），需开门控＋Pod 注解）` | 链接与行号属实 → C10 第 3 条 |
| 正文 L68 | `被 GC 级联删除的情形见核对方法第 2 步取消分支`；正文检索 `见 L<数字>` 0 命中 | 前次 C04 非阻断项已按建议改为节名＋步号 |

## 逐项判定

### B22-C10 — CLOSED

对照前次报告所列的三条剩余关闭条件：

1. **登记写入 `reconciler.go`：已落实。**
   - `src.kueue.job-lifecycle-v0.19.0` 的 revision（L5366）现含 `jobframework/reconciler.go L1476（Workload controller owner）`，行号与属主关系都对得上。
   - 前次要求写 `pkg/controller/jobframework/reconciler.go`，登记写的是缩写路径 `jobframework/reconciler.go`，与同行 `kube_features.go`、`pkg/workload` 的缩写风格一致。经全树核对，该缩写只对应一个文件，不会误指。
   - notes（L5374）未提及 `reconciler.go`。前次只要求写入 revision，不阻断。
2. **来源记录同步：已落实，位置与前次指定不同（非阻断）。**
   - 前次指出的缺陷是来源记录检索 `reconciler`、`jobframework` 均为 0 命中，且没有写明属主关系。现在 L16 已有该文件的固定 commit 链接、行号 L1476、所支撑的主张（Workload 的 controller owner 为 Job），以及明确的登记归属"归 src.kueue.job-lifecycle-v0.19.0"。这与登记 L5366 一致，链接与正文 L125 同址。
   - 前次关闭条件写的是"来源记录 L15 的 Kueue 行同步"，实际写在 L16，L15 未变。判为不阻断，理由是：前次接受 `strategy.go`/`storage.go` 写在 L16，依据就是"归属与登记一致"；本条按同一标准已满足，而且没有错误归属。
   - 剩余瑕疵：L16 的"登记 ID"列是 `src.kubernetes.job-controller-tests-v1.32.0`，"主张"列是"官方测试入口"，而 `reconciler.go` 既不是 K8s 文件，也不是测试。按 ID 列查 `src.kueue.job-lifecycle-v0.19.0` 的读者会落到 L15，看不到这个文件。建议把该子句移到 L15 末尾，例如"…/kube_features.go 与 pkg/workload（…）/jobframework/reconciler.go L1476（Workload controller owner 为 Job）"，让 L15 与登记 L5366 一一对应。
3. **L130 FailureRecoveryPolicy 出处：已落实。**
   - L130 已链接 `kube_features.go` L682–683，所标行号属实。
   - L684 即闭合该门控块，没有后续阶段记录；该块位于 L544 起的 `defaultVersionedFeatureGates` 表内。因此 v0.19.0 下"v0.15 Alpha 默认关"有逐行出处。
   - L62 与 L114 只写"v0.15+、需开门控"，不含阶段与默认值，与 L130 不冲突。

顺带确认（前次 C04 非阻断项，C04 仍为 CLOSED）：L68 的"见 L125"已改为"见核对方法第 2 步取消分支"，正文已无指向本文件行号的引用。该处指向"终止 / 重试 / 取消后的核对方法"第 2 步；目标处原文写作"取消分四种触发"，首个触发"删 Job→…"即包含 Background/Foreground 下被 GC 删除的分支。"取消分支"是概括说法，靠节名加步号能定位。L68 主语仍是 Kueue，没有回退。

## 修订映射核对

映射第五轮节（L351–353）与落盘状态对照：

- "登记 reconciler.go 归属"：与登记 L5366 一致。
- **"记录 L15 同步"：位置与落盘不符。** 改动落在 L16，L15 未变。来源记录确已同步，归属也正确，所以不影响判定。但该节标题写明"只列落盘改动"，建议把该条改为"记录 L16 补 reconciler.go（归 Kueue 条目）"，或按上文建议把子句移到 L15，使映射成立。
- "L130 门控出处"：与正文 L130 一致。
- "L68 自引用修正"：与正文 L68 一致。
- 本节标题"claude 第四次定向复核 10/11"与前次结论（合计 CLOSED 10/11）一致。前次指出的第四轮节标题（L346）"第三次定向复核 6/9"计数有误，仍未更正（非阻断）。

## 前次非阻断项现状（不在本轮范围，仅记录仍未改）

- L82"达 `backoffLimitCount` 后去活见 setup_wait_for_pods_ready L107–110"仍是纯文本；L84 仍未直接链接 `workload.go` L1565 或 jobs.md L226–229。
- L125"测试 L4042"仍未注明测试以手动清空 ownerReferences 模拟孤立。
- frontmatter `verification.notes`（L29）仍未列入 setup_* 三页、metrics、`kube_features.go`、`workload.go`、`reconciler.go`，并仍写"经 webfetch…curl 字节级取回未执行"，与正文实际依据不同步。
- 登记 `src.kubernetes.job-controller-tests-v1.32.0` 标题（L5376）仍为"（存在性）"，license notes（L5384）仍写"只链接并记录存在性"，与 revision（L5380）已收录的行为样本不符。
- C09 遗留：`backoffLimitPerIndex`"默认开"所依据的 v1.32 Feature Gates 页仍未在正文链接，也不在登记范围内。

## acceptance 对照

| acceptance | 判定 | 未关闭发现 |
|---|---|---|
| 1 UID、generation/attempt、控制器责任与状态转移；区分 API 接收/admitted/Running/应用 ready/持续进展 | 满足。与前次相同 | — |
| 2 backoff/deadline/retry/replacement、删除/finalizer、退出/回收与配额撤销；行为绑定版本 | 满足。前次唯一缺口（L130 FailureRecoveryPolicy 的阶段与默认值）已有 `kube_features.go` L682–683 出处 | — |
| 3 三视图对齐表、关键事件、卡住/重试/清理的下一项检查 | 满足。与前次相同 | — |
| 4 终止/重试/取消后账本与应用结果核对、官方测试/例子；训练恢复归应用 | 满足。取消分支的属主前提 `reconciler.go` L1476 已写入登记，来源记录也有记载 | — |

## 结论

**T05-02 第五轮修订后第五次定向复核通过：范围内 CLOSED 1/1（C10）；B22-C01–C11 合计 CLOSED 11/11、OPEN 0/11。**

- C10 前次剩余的三条均已落实，经本轮独立重取核对属实：登记 L5366 写入 `reconciler.go` L1476；来源记录有该文件与正确归属；L130 链接 `kube_features.go` L682–683。
- 非阻断建议（不需复核即可关闭本轮）：
  - 把来源记录中 `reconciler.go` 子句从 L16 移到 L15 Kueue 行，或把映射 L353 的"记录 L15 同步"改为实际位置；
  - 更正映射第四轮节标题计数；
  - 处理上节所列前次遗留项。
  这些改动只涉及记录、映射或登记措辞，不影响本结论。若同时改动正文，需另行定向确认。
- 本复核只覆盖编辑与来源层面。文中 Kubernetes/Kueue 行为都是文档或源码层证据，不得标为 reproduced。正文 `verification.status: source_checked` 现可视为在文档与源码核对层面成立，不代表平台兼容性或实测结果；正文状态仍为 `draft`。
