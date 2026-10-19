# Batch 24 遗留处理：第四次 Codex 定向复核

日期：2026-10-19（Asia/Shanghai）。基线：`0e8ff0f5348ce8197fc9fc692ede1aee9675dcc8`，加本轮开始时工作区已有的未提交修订。本文位置指本轮工作区源文件；历史位置另注明提交。只复核 B24-PC-09、B24-PC-R3-01、B24-PC-R3-02，不重新审阅第三次报告已关闭的技术内容。

## 1. 结论

**暂不通过。** B24-PC-R3-01、B24-PC-R3-02 的原问题均为 **CLOSED**；B24-PC-09 因更正记录仍有一处历史归因混写而保持 **OPEN**。本轮新增 **1 项 OPEN P3：B24-PC-R4-01**，无新增 OPEN P1/P2。当前批次、主题、catalog 数值均正确；阻塞点仅为复查记录“已记录、本次未处理”节把两个不同时间点的停更状态合并表述，不是要求重做已经通过的统计或正文审阅。

| 复核项 | 优先级 | 判定 | 依据 |
|---|---|---|---|
| B24-PC-09 | P3 | **OPEN** | 43/18/2、followup 20、未映射 0、20 个规划批次与 8 个剩余批次全部复算一致；但 `docs/research/batch-24-post-close-review.md:61` 对 `summary` 与 `batch_planning` 共同使用“自 Batch 16 后未随批次更新”，与 Git 历史及该文 `:47` 的分别限定不一致，见第 6 节。 |
| B24-PC-R3-01 | P3 | **CLOSED** | `planned_followup_batches: 20` 明确指完整规划 Batch 13–32；`remaining_planned_batches: 8` 指 Batch 25–32，字段、说明、backlog 与路线图相符，见第 3 节。 |
| B24-PC-R3-02 | P3 | **CLOSED** | 已明确区分初始基线 12/44/7、followup 51，与含 Batch 13–16 更新的旧滚动统计 22/34/7、followup 41；不再把后者称为“2026-10-08 首次盘点”，见第 4 节。 |

B24-PC-07/08/10 保持第三次报告的 **CLOSED**，本轮仅对可能受本次更正影响的轮次文字、主题统计和正文身份作回归抽查。原 R3-02 的“首次盘点”误标已修正；新增 R4-01 针对的是另一项新改写的批次字段停更归因，不把同一问题重复计成两项发现。

## 2. 角色、模型与证据边界

- 承担同一 Codex 技术审阅角色；未派发子代理，未启动另一模型调用。用户指定模型/档位为 `gpt-6.1-sol / xhigh`。
- 本轮以进程环境中的 `CODEX_THREAD_ID` 定位并实际读取本地会话记录 `~/.codex/sessions/2026/10/19/rollout-2026-10-19T11-19-17-01a1522b-b243-75f3-a171-9cb1b7f51875.jsonl`。L1 的 `session_meta` 为本仓库 cwd、`originator=codex_exec`、`cli_version=0.157.1`、`model_provider=custom`；L6 的 `turn_context` 记录 `model=gpt-6.1-sol`、`effort=xhigh`、`approval_policy=never`、workspace-write、`network_access=false`。可核验本地 CLI 记录的单一模型/档位；**不能独立认证自定义服务端实际执行的模型权重或推理档位，后者仍为 unknown**。不以用户指定值替代实际核验证据。
- 已读取 `README.md`、`docs/authoring-guide.md`、`content-outline.md`、[第三次报告](batch-24-post-close-codex-recheck-3.md)、[复查记录](batch-24-post-close-review.md)、两个计划 YAML 和对应盘点、路线图。`docs/`、`plans/` 下未发现更深的 AGENTS.md。
- 依据当前 `git diff` 辨认既有九个文件的未提交修订，并用第三轮隔离副本对照实际增量。第三轮副本的九个相关文件分别与该轮 `workspace-before.json` 摘要相符；本轮没有把前轮正文重排重新归为本轮修订。
- 本轮只使用仓库文件、Git 历史及本地隔离构建证据；没有重新抓取远端上游，不声称重新认证已经关闭的技术主张或早期各批的技术验收，也未进行真实硬件验证。

## 3. B24-PC-R3-01：CLOSED

第三次报告 `:255` 的关闭条件要求：明确批次数口径，按实际批次集合重算，同步说明和处理记录，不能只声明已更新而保留无口径的 19。本轮已满足。

### 3.1 字段与独立批次集合

| 检查对象 | 当前值或独立结果 | 判定 |
|---|---|---|
| `plans/topic-coverage.yaml:55` | `planned_followup_batches: 20` | 与完整规划 Batch 13–32 的 20 个批次相符。 |
| `plans/topic-coverage.yaml:56` | `remaining_planned_batches: 8` | 与执行清单当前 `status: planned` 的 Batch 25–32 共 8 批相符。 |
| `plans/topic-coverage.yaml:60` | `planning_notes` 分别定义上述两种口径，并说明原 19 不符、于 2026-10-19 更正 | 没有把 20 同时当作当前待执行数量，也没有把 19 冒充有证据的历史规模。 |
| `plans/full-coverage-backlog.yaml` 的全部 `batches` | 编号连续为 13–32；13–24 共 12 批 `done`，25–32 共 8 批 `planned` | 20＝12＋8；没有遗漏、重复或其他批次状态。 |
| `plans/full-coverage-backlog.yaml:64` 的规划摘要 | `planned_batches: 20`、first 13、last 32、total including completed 32 | 与实际 batches 及主题计划相符。 |
| `docs/full-coverage-roadmap.md:51` | 85 项内容任务、20 个后续批次（13–32），加原 12 批合计 32 | 与 backlog 实际 85 项任务及批次口径相符。 |
| `docs/research/batch-24-post-close-review.md:54` | 明记 19→20、另列剩余 8 及相应区间 | 已同步处理记录。 |

同组 `completed_batches: 01–24`、`next_batch: 25`、last 32、total 32 与当前执行清单相符。`final_batch_count: null`、`planning_status: in_progress`、`execution_started: true` 没有宣称全部规划完工。这里核对的是账面集合及其说明，不重新确认前 12 批或后续 12 个 done 批次的所有技术结论。

## 4. B24-PC-R3-02：CLOSED

第三次报告 `:262` 要求区分初始基线与旧滚动统计，并同步 YAML notes、Markdown 括号与处理记录。本轮针对原“首次盘点”误标的修复成立。

| 统计层次 | covered / partial / missing | followup | 本轮独立证据 |
|---|---:|---:|---|
| 完整覆盖规划的初始基线 | 12 / 44 / 7 | 51 | `plans/full-coverage-backlog.yaml:48` 的 summary；另逐项统计全部 63 个 `topics[].baseline_coverage_status`，结果相同。 |
| 首个入库提交已经保存的滚动结果 | 22 / 34 / 7 | 41 | `git show b89abb9:plans/topic-coverage.yaml` 的 summary 与全部 topics 独立统计相符；该提交的 completed 为 01–16、next 为 17。 |
| 本轮当前重算结果 | 43 / 18 / 2 | 20 | 当前 63 个 topics 独立计数，见第 5 节。 |

首次引入 `plans/topic-coverage.yaml` 的提交是 `b89abb99dc8f6b5e8fde59e2bbd8f3b778862985`；作者日期和提交日期均为 **2026-10-09 14:13:10 +08:00**。该提交已记录 Batch 13–16 完成并保存 22/34/7，不是首次基线 12/44/7。不能用文件 `created_at: 2026-10-08` 把滚动结果倒推成当天首次盘点。

逐处核对修订：

- `plans/topic-coverage.yaml:50` 的 `summary.notes` 已把 22/34/7、followup 41 称为“本轮重算前保留的 summary”，注明包含 Batch 13–16 的主题升级、首个提交已为该值，并另写初始 12/44/7、followup 51。
- `docs/topic-coverage-audit.md:9` 的统计节括号同样分列初始与旧滚动结果，没有继续使用“2026-10-08 首次盘点”的错误归因。该文 `:185`、`:187` 仍分别保留原基线与 51 个待补主题的规划解释，与本次更正不冲突。
- `docs/research/batch-24-post-close-review.md:47` 的 PC-09 行已分别写明：summary 停在 Batch 16 后的 22/34/7，而 batch_planning 的 completed 停在 01–22。`:55` 承认原误标、给出两种统计及 b89abb9 的实际日期。上述更正与独立 Git/YAML 证据一致。

“已记录、本次未处理”节 `:61` 也确有改动，但其对两个字段共用停更时点的剩余问题另列 R4-01；不撤销本节对原数值/“首次”归因修复的 CLOSED 判定。

## 5. B24-PC-09：数值复核通过，记录尚未闭环

### 5.1 主题与 catalog 复算

解析当前 YAML、盘点 Markdown 和隔离副本重新生成的 catalog；先按唯一内容 ID 分类，再以全部 `topics[].evidence_refs` 的并集核对正文映射，不以 `background_refs` 充当正向覆盖。

| 项目 | 独立结果 | 对照 |
|---|---|---|
| 主题总数、覆盖分布 | 63；covered 43 / partial 18 / missing 2 | 与 YAML summary、盘点 `:9` 相符。 |
| 有内容缺口的主题 | 20＝18＋2 | 与 `followup_topics` 相符；这是主题数，不是批次数。 |
| Markdown 逐主题行与领域小计 | 63 行覆盖状态全部一致；9 个领域小计全部一致 | 未发现数值或状态回归；不重复 PC-08 的正文覆盖适足性审阅。 |
| catalog / 实质正文 / 导航 | 103 / 90 / 13，103 个 ID 均唯一 | 与盘点 `:11` 相符。 |
| 来源 | catalog 493 / registry 493 | 与盘点 `:11` 相符。 |
| 正文类型 | concept 28、reference 22、procedure 26、case 7、experiment 7 | 合计 90；另有 index 9、path 4。 |
| 正文验证状态 | source_checked 75、not_verified 15、reproduced 0 | 与盘点 `:13` 相符；not_verified 为 experiment 7＋procedure 8。 |
| 编辑状态 | draft 103 | 没有把结构检查或内容盘点改写为 reviewed 或实测。 |
| 未映射实质正文、无效 evidence ID | 0 / 0 | 90 个正文 ID 均在 evidence_refs 中；全部 evidence ID 在 catalog 存在。 |

### 5.2 保留快照

`input_snapshot`、`validation`、`documents` 三组分别与 HEAD 和 b89abb9 解析比较，均完全相同。它们仍保留 73 catalog entries / 60 篇实质正文 / 13 个导航、119 来源及旧 documents 摘要，并非本轮 103/493 的重新采集结果。

`summary.notes` 现已使用“登记日期 2026-10-08”的限定，且明确“未重新生成”；只能确认其与既存快照相同，不能独立证明每个旧摘要的实际采集时刻。本轮不要求改写这些快照，也不把其中旧 passed 或旧 sha256 当作当前文件身份。该保留策略不构成新问题。

### 5.3 PC-09 的剩余关闭条件

数据、批次口径、初始/滚动/当前统计的区分均已通过；只需按第 6 节消除处理记录中两个停更时点的混写，再作该位置的定向复核。**不要为此改动已正确的 20、8、43/18/2、正文或保留快照。**

## 6. 新问题与关闭条件

### B24-PC-R4-01 — P3 — OPEN：遗留记录仍把两种停更状态归于同一 Batch 16 时点

- **位置**：`docs/research/batch-24-post-close-review.md:61`；对照该文 `:47`，以及历史 `plans/topic-coverage.yaml` 的 batch_planning。
- **本轮改动**：该行把原“自 2026-10-08 起”替换为“自 Batch 16 后”，但保留并列主语“`summary` 计数与 `batch_planning`（completed_batches 01–22）”，形成二者“自 Batch 16 后未随批次更新”的共同归因。PC-09 表格行已经分别限定两种停更状态，这里却仍混写。
- **证据**：`summary` 确实一直保留 22/34/7；但 batch_planning 在 Batch 16 以后有可核对的实际更新，不是同一冻结时点：

| Git 版本 | 提交日期（+08:00） | summary（covered / partial / missing） | completed_batches / next_batch |
|---|---|---|---|
| b89abb9（首次入库） | 2026-10-09 14:13:10 | 22 / 34 / 7 | 01–16 / 17 |
| d01cc71 | 2026-10-18 03:24:52 | 22 / 34 / 7 | 01–20、22（Batch 21 缺 T04-08，未完成）/ 23 |
| 1d07b62 | 2026-10-18 14:28:44 | 22 / 34 / 7 | 01–22 / 23 |
| 本轮 HEAD 0e8ff0f | 2026-10-19 10:17:01 | 22 / 34 / 7 | 01–22 / 23 |
| 当前工作区 | 本次待复核修订 | 43 / 18 / 2 | 01–24 / 25 |

历史原文件坐标：`b89abb9:plans/topic-coverage.yaml:50`、`d01cc71:plans/topic-coverage.yaml:50`、`1d07b62:plans/topic-coverage.yaml:50`。这足以区分“主题计数保留 Batch 16 滚动值”与“批次字段后来更新到 Batch 22，但本轮前未跟上 Batch 23/24”。不是要求删除保留的历史记录，而是更正本轮新写的共同时间归因。

- **影响**：不影响当前统计、批次划分、主题正文或第三轮已关闭的技术事项；影响 PC-09 处理链的可追溯性。读者在 `:47` 与 `:61` 会得到不同的停更范围，因此用户本轮明确要求核对的“已记录、本次未处理”节尚未准确收尾。严重性为 P3。
- **关闭条件**：将 `:61` 改为分别陈述两件事，例如“summary 保留 Batch 16 后的 22/34/7；batch_planning.completed_batches 在本轮前为 01–22、next 23，未反映后续两批；已在 PC-09 及 R3-01 修订中处理”。也可移除对并列两项共用的“自 Batch 16 后”限定，并引用 `:47` 的准确分项说明。保留原始记述/更正/已处理的层次，不再把两者写成同一停更时间。定向对照该行、PC-09 行和上述历史后关闭。

本轮唯一新增发现即 R4-01，无新增 P1/P2，不因该 P3 重新打开 PC-07/08/10。

## 7. 已关闭事项的回归抽查

第三轮隔离副本仍可读取，位置为 `/private/tmp/b24-recheck3.dwYLN6/repo`；其相关文件已先与第三轮原始摘要核对。与本轮当前工作区比较，第三轮后实际变化只有四个已跟踪文件：主题计划、盘点、复查记录、Batch 24 来源审计。没有把 HEAD 起累计九文件差异误当成全部为本轮新增。

- **PC-07**：来源审计的本次新增差异仅在 `docs/research/batch-24-source-audit.md:45` 补第三次报告链接、第三轮 PC-09 未关闭说明及第四次报告路径；两处“初审＋6 轮”与第三轮副本相同。路线图文件逐字节相同。保留 CLOSED，不重数或重审 T06-01 技术链。
- **PC-08**：主题计划的全部 `topics` 对象与第三轮副本相同；盘点除统计节 `:9` 外逐行相同。当前 63 行与领域小计的数值核对也通过，没有因为字段口径更正改变 05.2 或其他主题判定。保留 CLOSED，不重审已关闭的覆盖依据。
- **PC-10**：四篇正文 `control-plane-recovery.md`、`framework-execution.md`、`parallelism-and-state.md`、`pretraining-and-finetuning.md` 均与第三轮副本逐字节相同，没有本轮新增重排。保留 CLOSED，不重复逐段技术审阅。

## 8. 隔离检查、可重复性与文件保护

隔离目录为 `/private/tmp/b24-recheck4.DJQKQW/repo`，在仓库外。复制本轮起始工作区（含既有未提交修订），排除 `.git`、`.venv`、`.agents`、`.codex`、Python/测试缓存与 `.DS_Store`；保留原有 build 文件作为副本检查本地链接的起点，随后只在副本重新构建。统计与摘要取副本**重新生成**的 catalog，不以原工作区旧产物代替。

实际使用原工作区解释器 `/Users/ywang2397/work/AI_reliability_knowledge_base/.venv/bin/python`，实测版本 **Python 3.11.15**。副本无 `.venv`，make 输出确认调用上述绝对路径；没有安装或升级依赖。实际命令，cwd 为上述隔离 repo：

```bash
make check PYTHON=/Users/ywang2397/work/AI_reliability_knowledge_base/.venv/bin/python
make build PYTHON=/Users/ywang2397/work/AI_reliability_knowledge_base/.venv/bin/python
```

| 阶段 | make check | make build | 实际输出 |
|---|---|---|---|
| 报告写入前 | PASS，exit 0 | PASS，exit 0 | 103 content entries / 493 sources；生成副本 build/catalog.json、build/catalog.md。 |
| 含本报告 | PASS，exit 0 | PASS，exit 0 | 同为 103 content entries / 493 sources；副本重新生成的 catalog 摘要与报告写入前一致。 |

辅助复算脚本第一次运行 exit 1：脚本未适配 Markdown 第一列加粗且编号与标题同列的格式，误读为 0 个主题行。修改仓库外脚本的解析规则后重跑 exit 0，读到 63 行、逐行不一致 0、领域小计不一致 0，全部 21 项程序断言通过。该失误不是仓库内容错误或 make 失败；初次与最终输出均保留，没有修改被审阅文件以适配脚本。

复算脚本、结果、初次输出、历史核对和 make 日志保留在仓库外的 `/private/tmp/b24-recheck4.DJQKQW`：`audit.py`、`audit-results.json`、`audit-output.txt`、`audit-results-initial.json`、`history-and-regression.json`、`session-identity.json`、`workspace-before.json` 及相应检查日志。临时材料不是永久仓库证据，不加入知识正文，也不改变来源登记。

| 复核输入或新构建产物 | SHA-256 |
|---|---|
| plans/topic-coverage.yaml | `57a89112e48f36a4ce94099690a8f0d0e665220d8cea26588fa06f84f3c8fded` |
| plans/full-coverage-backlog.yaml | `5a98b4224b1947e735ef4ca28697d5082e89840ec80ffe833508db4159b64b37` |
| docs/topic-coverage-audit.md | `f4979a9b98072d02b712613a3b7b3374e8411313b2ef181f1d4720d56ce60743` |
| docs/research/batch-24-post-close-review.md | `05c4f726367994b2f02604e98f6e2fc53a1a4d4db9217c5a111954658da11f03` |
| 隔离重新生成 build/catalog.json | `05f565352b1f06ffabaa0af128601dbfe52a131b9cb4e06bbbda814fc386f9ca` |

报告落盘后的文件保护核验：起始纳入摘要对照的 510 个既有文件中，**变更 0、删除 0，唯一新增为本报告**；原工作区 build/catalog.json、build/catalog.md 均未改变，起始九文件 `git diff` 逐字节不变，HEAD 仍为 `0e8ff0f5348ce8197fc9fc692ede1aee9675dcc8`。结果保存在仓库外 `workspace-protection.json`。未创建分支或提交，未修改第三次报告或修订者已有文件。

本次未改 `src/kb/`，未运行 `make test`，未执行 GPU/NPU、训练、进程组、集群、灾备或 checkpoint 操作。结构检查 PASS 仅说明结构与本地文件链接符合校验，不证明远程内容、技术正确性或现场效果；本报告暂不通过也不是硬件验证失败。
