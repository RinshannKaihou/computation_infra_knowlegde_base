# 第二十二批 T05-05 第五次定向复核（作者第五轮修订后，仅 C23）

复核日期：2026-10-15。

**结论：定向复核通过。本轮范围 1 项（B22-C23）：CLOSED 1，OPEN 0。连同前几轮已关闭的 C22、C24–C30，B22-C22–C30 共 9 项全部 CLOSED。本轮不新增发现 ID，也没有发现新的事实错误。**

C23 按前次报告的方案 A 关闭。L169 原括注“默认不设 `AccountingStorageEnforce` 时不按记账库限额执行”点名了选项、写出了默认行为，但没有已登记的就近出处。现在改为“站点配置 unknown”，与方案 A 给出的示例写法逐字一致。全文已不出现 `AccountingStorageEnforce`、“记账库”和 `resource_limits`，不再有缺出处的实质主张。

审阅者角色独立于作者。审阅模型为 `claude-opus-5-5`，由用户明确要求试用；这不是既有的 `gpt-6.1-sol / xhigh` 批量审阅约定，也不改写该约定。本轮未出现 `[frontier_llm]` 标记、模型不一致或认证失败；推理等级等运行元数据没有可核验记录，不补造。本轮只做只读取证和审阅：只写本报告；未改作者正文、来源记录、登记、修订映射、计划或前次报告；未部署 Slurm 或其他平台，未提交作业，未运行任何上游测试。模型审阅不构成平台或现场验证。

## 输入（以 SHA-256 识别）

| 输入 | SHA-256 |
|---|---|
| [T05-05 正文](../../knowledge/05-cluster-platform/admission-and-placement.md)（177 行） | `1c55afd01f4abfd2d1d8dffec8b0cf27d7ad9b1be6a71cc84a22b1900c883e98`；L169 单行 `de342d4a17f6030b373578b89f9ac57b7662d2fe912b49a435a213ac40506ae1` |
| [作者来源记录](batch-22-t05-05-sources.md)（22 行） | `ad5d0f38ca9152dd89ba199bf87f82577245824dcf68efb0348741f5066882f0`；L11 单行 `113112dec6f207423566add5d2b3f7a775f213f6d0820155e1a767dcd6a8f66c` |
| [修订映射](batch-21-review-fixes.md)（398 行；T05-05 第五轮修订节 L396–398） | `8c996021a27ce9f717f4cd26f358010def6e222d5454186ee2302e25d5f53d8c`；L396–398 段 `7be4c3baf21352ca31a6a488afd3053692feaca3a806a329a34fba6664994f62` |
| [前次复核报告](batch-22-t05-05-claude-recheck-4.md) | `e9918d51c74184db56c3c6860e896dfefbf7740aec19cb250933863bb65f4e17`（与本地会话记录 `4820240c…` 中审阅者的 Write 原稿一致，此后没有 Edit） |
| [来源登记](../../sources/registry.yaml)（444 项） | `b9cdbedf73379dd24d704e0363e1fcbcc550f3c8f9581b93659a32a1e39a6b0f`（与前两轮相同，本轮未改） |

任务给出的三个前缀（正文 `1c55afd01f4abfd2`、来源记录 `ad5d0f38ca9152dd`、修订映射 `8c996021a27ce9f7`）均与实测一致。前次报告与登记任务未给前缀，上表记录实测值。登记 444 项与任务所述一致。输入在开始时取哈希，成稿前复取一次，结果相同（见文末）。

前次报告是 C23 剩余关闭条件的唯一权威来源，因此本轮先核对它没有被改动：现文件与审阅者原稿逐字一致，作者没有改动审阅者报告。

## 本轮实际改动（逆向重建上一版后比对）

方法：对现文件做与修订映射所述相反的替换，得到候选上一版，再与前次复核输入表记录的哈希比对。重建结果与前次哈希逐字一致，说明本轮改动恰好只有这些，没有其他改动：

| 文件:行 | 改动 | 逆向重建哈希 |
|---|---|---|
| 正文 L169 | 括注“（默认不设 `AccountingStorageEnforce` 时不按记账库限额执行）”改为“（站点配置 unknown）”，其余字不变 | 还原后为 `f63325bfec3d93e7…`，与前次输入表一致 |
| 来源记录 L11 | 删除 `（minAvailable 同步）` 之后的残留片段 `(https://github.com/volcano-sh/volcano/blob/8fc394c1…/pkg/controllers/job/job_controller_util.go)（默认 Sync）` | 还原后为 `80d20e0b2ac2e350…`，与前次输入表一致 |
| 修订映射 | 只在文末追加 L395 空行和 L396–398 第五轮修订节 | 前 394 行的哈希为 `61f17ac43a6f26d3…`，与前次输入表一致 |

正文其余 176 行、来源记录其余 21 行、登记均没有变化。重建文件只放在临时目录 `/tmp/b22rc05e/`，未入库。

## 一次源

本轮没有重新获取上游页面或源码。理由：

1. 本轮对正文只做了删除：去掉一项缺出处的实质主张（选项名与默认行为），换成 unknown。没有新增任何需要一次源支撑的主张。
2. L169 其余前提（同一 QOS/分区、`DenyOnLimit`、Partition QOS/`OverPartQOS`）和正反例 reason（`QOSMax*PerJob`、`QOSMaxGRESPerJob`）的文字未变。前次复核已按 Slurm 24.11.7 归档 qos、job_reason_codes 页逐句核对，结论为属实，当时取回的哈希也与更早一轮相同。
3. 来源记录 L11 的改动只是删去重复的 util URL，保留下来的链接与区间（`job_controller_util.go L182–196/L286–288`、`job_controller_actions.go L813–816/L877–880`，固定在 `8fc394c1`）前次已核对属实。

取证限制：本轮没有访问任何远程链接；如果上游归档页在前次复核之后变化，本报告无法察觉。这一限制不影响 C23 判定，因为判定依据是正文已不再引用这类主张。

## 逐项判定

### B22-C23 — P1 / CLOSED

前次报告的剩余关闭条件为二选一：方案 A（不点名选项，只写 unknown）或方案 B（就近引用 resource_limits 页并登记）。

| 前次剩余条件 | 判定 | 位置证据 |
|---|---|---|
| **A**：把 L169 括注改为不含选项与默认行为的写法，例如“站点实际执行 QOS 限额（站点配置 unknown）” | **已落实** | L169 现为“站点实际执行 QOS 限额（站点配置 unknown）”，与方案 A 的示例逐字一致；全文 1 处，在 L169。正文中 `AccountingStorageEnforce` 0 处、“记账库” 0 处、`resource_limits` 0 处。来源记录中 `AccountingStorageEnforce` 0 处 |
| **B**：就近引用 resource_limits 页并登记 | 不适用（作者选了 A） | 登记哈希与前次相同，`resource_limits` 在登记中 0 处、正文中 0 处，与选 A 一致，没有留下引用了却未登记的悬空出处 |

关闭理由：

1. 前次判 OPEN 的唯一原因，是一项点名选项的实质主张没有已登记出处。这项主张已删除，原因随之消失。
2. 替换后的“站点配置 unknown”是对未知条件的显式记录，符合 AGENTS.md“记录未知条件与缺失证据”的要求，不需要出处。
3. “站点实际执行 QOS 限额”这一前提本身仍保留在对照验收中。反例要求 `%r` 为 `QOSMaxGRESPerJob`，必须以限额实际被执行为前提，因此删掉括注不削弱验收设计，只是不再断言默认值。
4. 句末出处“（job_reason_codes、qos 页）”现在覆盖的主张都在这两页内：`DenyOnLimit`、Partition QOS/`OverPartQOS` 在 qos 页，`QOSMaxGRESPerJob` 在 job_reason_codes 页（前次已核对原文）。没有任何主张挂在不支撑它的出处下。

前次已落实的另一项条件（L169 补 Partition QOS/`OverPartQOS` 前提）本轮文字未变，仍成立。

建议（非阻断）：删除默认行为后，读者无法从本页得知“未配置时限额可能不执行”这一常见陷阱。如果作者以后想恢复这条操作提示，仍可走方案 B：登记 [resource_limits](https://slurm.schedmd.com/archive/slurm-24.11.7/resource_limits.html) 并就近引用（前次报告已摘录支撑原文）。这不影响本轮关闭。

## 修订映射与落盘差异

[修订映射](batch-21-review-fixes.md) L396–398 标题注明“逐条 grep 已核对”。逐条对照如下：

| 映射条目 | 落盘情况 |
|---|---|
| L398 C23“对照前提改通用写法（站点实际执行 QOS 限额，站点配置 unknown）” | 一致（见上节逆向重建） |
| L398“L11 残留清理” | 一致：来源记录 L11 中 util URL 由 2 处减为 1 处，“默认 Sync”由 2 处减为 1 处；半角括号 4/4、全角括号 5/5、方括号 4/4 均配对，4 个 URL 都处在 Markdown 链接语法中。这一项属于前次已关闭的 C30 的非阻断项，不在本轮判定范围，这里只核对映射与落盘是否一致 |

本轮映射与文件完全一致，没有“映射写了、文件里没有”或“文件改了、映射没写”的情况。

## acceptance 对照

| acceptance | 判定 | 未关闭项 |
|---|---|---|
| 1 以固定 Volcano 实现解释 minMember/minResources、成组决策、启动失败、重排队/回退及与 rendezvous 的不同 | 满足（前次已满足，相关行本轮未改） | — |
| 2 Kueue 与 Slurm 两个独立配置/状态样板；选择依据与公平性代价分开 | 满足（本轮未改） | — |
| 3 每个样板的资源向量、拓扑、碎片、配额、运行进展观测，失败或不适用反例及对照验收 | 满足：样板 B 对照验收的前提已完整，且不再有缺出处的括注 | — |
| 4 MindCluster 边界；链接 idle-resource-job-waiting-triage 与 Slurm 状态参考；不是统一推荐策略 | 满足（L177 未变） | — |

`verification.status: source_checked`：B22-C22–C30 已全部关闭，初审对 Volcano 部分的保留（前次已解除）以及 Slurm 样板的出处缺口都已不存在。`source_checked` 只表示源码与文档层面的核对成立，不代表 reproduced；文中 Volcano/Kueue/Slurm 行为均未在任何平台上部署或运行。

## 范围外遗留（只记录，不影响判定）

逆向重建表明，正文只改了 L169，来源记录只改了 L11。因此前次报告列出的以下非阻断建议仍未改。它们不属于本轮范围，也不新增发现 ID：

- 正文 L149 末尾“否则只见 `Pending`，unknown”中的 unknown 指代不清；门控名旁可补 `kube_features.go` 链接。
- 正文 L167 的 `%R` 措辞（Pending、失败终止、其他状态三种语义）。
- 正文 L88 全角括号未闭合，以及 L85–87 三个空行。
- 正文 L95 “（L152–169）”的挂靠位置。
- 来源记录 L3 方法句与 L10“精确页面/节”列仍写“gangreclaim 同模型”，没有链接。
- 登记 L5489 标题“调度动作实现（enqueue/allocate/gangpreempt）”未覆盖 gangreclaim.go 与 api/job_info.go。

## 结论

**T05-05 第五次定向复核通过。本轮范围 1 项：B22-C23（P1）CLOSED。B22-C22–C30 合计 CLOSED 9、OPEN 0。不新增发现 ID，无新事实错误追记。**

- C23 按方案 A 关闭：L169 括注已改为“站点配置 unknown”，不再点名选项或断言默认行为；正文、来源记录、登记中均无悬空出处。
- 本轮改动经逆向重建核实，恰为修订映射 L398 所列两处，没有其他改动。
- 这次通过只表示编辑与来源层面的复核已关闭；文中 Volcano/Kueue/Slurm 行为都是源码或文档层证据，审阅者未部署、未运行，不得标为 reproduced。上节所列非阻断建议可在后续修订中一并处理。

## 检查记录

- 成稿前复取输入哈希：五个输入文件与“输入”表逐字一致，复核期间输入未变。
- `make check`：`PASS: 96 content entries; 444 sources.`（复核期间运行；`check` 分支不写文件）。它只校验结构与本地链接，不说明技术正确性，也不访问远程链接。
- 未运行 `make build`：本轮只新增 `docs/research/` 下的审阅报告，按任务约束不改其他文件，也不生成 `build/` 产物。
