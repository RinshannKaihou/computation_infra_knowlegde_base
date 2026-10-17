# Batch 22 整批收尾定向复核（B22X-C01/C02）

日期：2026-10-17（Asia/Shanghai）。角色：独立审阅者，与正文及收尾记录作者分离；延续[上轮整批审阅](batch-22-acceptance-codex-review.md)，不代作者修订。指定模型与档位：`gpt-6.1-sol / xhigh`；本轮与已弃用尝试的实际运行元数据分别见 §9。

## 1. 总结论

**定向复核通过；Batch 22 整批收尾在上轮审阅范围内成立、通过。** B22X-C01、B22X-C02 均满足各自关闭条件：**CLOSED 2 / OPEN 0；新增发现 0**（未启用 B22X-C03）。六项内容缺口关闭与任务/批次 done 的原判定不变，不代表主题最终验收或真实平台验证通过。

| 发现 | 原优先级/状态 | 本轮状态 | 判据 |
|---|---|---|---|
| B22X-C01 | P3 / OPEN | **CLOSED** | 六轮计数、调用方核验范围、两份盘点概括及末次复核的前提一致；不把调用方说明升级为审阅者亲读六份 JSON |
| B22X-C02 | P3 / OPEN | **CLOSED** | 三处导航改为任务审阅已闭环，保留 draft、未实测和 05.2 主题 planned / Batch 24 边界 |

## 2. 版本、输入与哈希

按要求首先运行 `git log --oneline -3` 与 `git status --short`。最近三项为 `76788a2`、`34d98c9`、`f9d8a15`；HEAD 为 `76788a20e33684a8ea538d457f0a214fd378b6a2`，符合指定修订提交。

**工作区并非全净：** 开始即存在 ` M docs/research/batch-22-source-audit.md`。只读差异显示其为新增“验收复核作废记录”一节，共 4 行，记录此前错误模型/档位的 resume 尝试及断流弃用；不是本审阅者的写入。本轮保留该改动，区分提交差异与工作区附加记录，不把它算入 `76788a2`。下表审计文件哈希取实际工作区版本；提交内该文件的 SHA-256 另为 `8838a23db643ee022cde17120e6b8071bd1ea3d0ebc7079ec2d429a45985dbfd`。附加节不改 C01/C02 修订文本。

开始取样：**2026-10-17T22:20:35+08:00**；成稿前复取：**2026-10-17T22:24:09+08:00**。六项均逐字节一致；成稿前 HEAD 仍为同一完整提交，状态仍仅为上述既有改动。

| 输入文件 | 开始时 SHA-256 | 成稿前 SHA-256 |
|---|---|---|
| `plans/full-coverage-backlog.yaml` | `6f44bd8e41c9d7e1c2554f5d4d97beb86a166552d911124c1fbbabdefc6da561` | `6f44bd8e41c9d7e1c2554f5d4d97beb86a166552d911124c1fbbabdefc6da561` |
| `plans/topic-coverage.yaml` | `4b9ecf5858efc3d5552ba8cc35cabb39074bbf983aa3cf011994232634d259a0` | `4b9ecf5858efc3d5552ba8cc35cabb39074bbf983aa3cf011994232634d259a0` |
| `docs/topic-coverage-audit.md` | `be782f541568784a035d42ee178252cd037931c4d04bfd4dab6ada4fd716767e` | `be782f541568784a035d42ee178252cd037931c4d04bfd4dab6ada4fd716767e` |
| `docs/research/batch-22-source-audit.md`（工作区） | `e73978bb8f491ab3169052e5eb232ed20d5d36d582254d9f139f41f07e9719c5` | `e73978bb8f491ab3169052e5eb232ed20d5d36d582254d9f139f41f07e9719c5` |
| `knowledge/05-cluster-platform/index.md` | `3731d218b2f2f1b7eb8c96da12dbe111da06f130a3d89e573825fbefb28a3349` | `3731d218b2f2f1b7eb8c96da12dbe111da06f130a3d89e573825fbefb28a3349` |
| `docs/research/batch-22-acceptance-codex-review.md` | `4e95ace8d37e1d6ef271e8bd105e039c8be87db47159c89d4c95a2d4729b9ba4` | `4e95ace8d37e1d6ef271e8bd105e039c8be87db47159c89d4c95a2d4729b9ba4` |

已读根 `AGENTS.md`、`README.md`、[编写指南 §7](../authoring-guide.md#7-批次审阅约定)及内容归属说明；检查 `docs/`、`plans/`、`knowledge/` 未发现更深层 `AGENTS.md`。以上轮发现的原关闭条件为判据，而非以作者修订摘要代替实际文件。

## 3. B22X-C01 — P3 / CLOSED

### 逐字对照与轮次核对

- [来源审计](batch-22-source-audit.md) L3 现为：“六轮审阅（初审＋五次定向复核）的模型元数据均经调用方按 CLI 输出核验：`modelUsage` 仅 `claude-opus-5-5` 单一模型、无 fallback 标记，均计入有效轮次。”
- 同文件 L13 的对应原文为：“六轮（初审＋五次定向复核）模型元数据均经调用方核验：CLI 输出 `modelUsage` 仅 `claude-opus-5-5` 单一模型、无 fallback 标记，均计入有效轮次”。不再出现“五轮核验”与“初审＋五次复核”的计数冲突。
- 枚举磁盘报告，确为 `batch-22-t05-04-claude-review.md`、`batch-22-t05-04-claude-recheck.md` 及 `-2`、`-3`、`-4`、`-5`，共六份。审计待办第 2 项（提交版 L31，当前工作区 L35）同为“初审＋五次定向复核”。
- [T05-04 第 5 次复核](batch-22-t05-04-claude-recheck-5.md) L5 与模型核验节保留“本轮模型元数据经调用方核验有效”的前提，未被追改成报告作者自行看过 CLI 元数据。
- [YAML 盘点](../../plans/topic-coverage.yaml) L59 与 [Markdown 盘点](../topic-coverage-audit.md) L3 的共同限定逐字为：“T05-04 初审＋五次定向复核共六轮经调用方核验 CLI modelUsage 单一模型、无 fallback，T05-02/03/05 各轮按其报告记录”。不再将 T05-04 的明确核验范围概括成其他任务每轮均已同法核验；T05-01 仍保留其实际 `gpt-6.1-sol / xhigh` 历史。

### 证据等级与关闭判定

本次调用方明确补充：T05-04 六轮 CLI 输出的 `modelUsage` 均只有 `claude-opus-5-5` 一项、无 fallback 标记，六份 result JSON 均在。这一补充不是只把“五”改成“六”，而是调用方对六轮真实输出核验范围的明确确认；与修订后的审计、盘点及末次报告前提吻合。**按上轮要求的“调用方核验、准确记载”条件，C01 CLOSED。**

本审阅者未取得或逐个打开这六份原始 JSON，也未重放历史调用；“六份均在、均已核验”依据本次调用方补充说明，审计只是相应记录，二者不算两份独立机器证据。本结论不写成“审阅者独立核验六轮实际执行模型”，不替 T05-02/03/05 补造相同等级的元数据证明。

## 4. B22X-C02 — P3 / CLOSED

对 [章节导航](../../knowledge/05-cluster-platform/index.md) 三个修改点逐字核对：

| 位置 | 修订后的对应原文 | 关闭条件核对 |
|---|---|---|
| L42 | `（T05-02，claude-opus-5-5 审阅已闭环，未做真实环境验证）。` | 不再标待审阅；真实环境验证未被宣称完成 |
| L44 | `（T05-03，claude-opus-5-5 审阅已闭环，未做真实环境验证）。` | 与 T05-03 实际历史审阅模型及闭环结论一致 |
| L62 | `（T05-02/T05-03，审阅已闭环，仍为 draft 且未做真实环境验证）；05.2 主题内容验收仍为 planned、属 Batch 24（T05-08/T05-10 等未交付）。` | 同时保留草稿、未实测、未来主题验收及未交付任务边界 |

交叉读取 [T05-02 第 5 次复核](batch-22-t05-02-claude-recheck-5.md) L5 与 [T05-03 第 4 次复核](batch-22-t05-03-claude-recheck-4.md) L5：分别为累计 CLOSED 11 / OPEN 0、CLOSED 10 / OPEN 0；来源审计 L9/L10 与 backlog 的 done 一致。读取两篇正文元数据仍为 `status: draft`、`verification.status: source_checked`，并有未部署/未提交作业等限定；没有因导航删去“草稿，待审阅”而升格正文状态。

L42/L44 未重复 draft，但同一导航 L62 与正文明确保留，三处合看不产生“审阅闭环即不再为 draft”的含义。结构与本地链接检查通过。**C02 CLOSED。**

## 5. 修订波及检查

实际运行 `git diff --stat 34d98c9 76788a2`、`git diff --name-status 34d98c9 76788a2`、`git diff --check 34d98c9 76788a2` 并读取差异。结果为 **5 文件，187 增 / 7 删**，无空白错误：

| 文件 | 实际范围 |
|---|---|
| `docs/research/batch-22-acceptance-codex-review.md` | 新增上轮独立审阅报告，179 行；保留 C01/C02 当时 OPEN 的历史，不倒改成已关闭 |
| `docs/research/batch-22-source-audit.md` | L3/L13 六轮计数与限定；追加上轮审阅发现、修订及待复核记录 |
| `docs/topic-coverage-audit.md` | 仅头段中的模型核验概括收窄 |
| `plans/topic-coverage.yaml` | 仅 `batch_planning.notes` 中对应模型核验概括收窄 |
| `knowledge/05-cluster-platform/index.md` | 仅 L42/L44/L62 三处导航文字 |

文件集合与预期精确一致；未夹带 backlog、五篇正文、来源登记、实现代码或其他审阅报告的改动。另对两份 YAML 作解析后递归比较：backlog 相对 `34d98c9` **零差异**；topic-coverage 只有 `$.batch_planning.notes` 改变，topics/documents/closure_criteria 未变。§2 的既有工作区作废记录另外核对、另外披露，不冒充提交内修订。

## 6. 账面与主题边界复核

- Backlog 的 T05-01–T05-05 仍为 `done / source_preparation_completed`；T05-02/03/04/05 属 Batch 22，其批次仍为 done。四份末次复核与审计任务表的 CLOSED 汇总一致；本轮没有修改这些状态。
- 六个关闭项仍为 05.1-G1/G2、05.2-G1/G2、05.4-G1/G3，均为 `closure_lane: content`、`validation_refs: []`。05.1-G3、05.4-G2、05.5-G1/G2/G3、05.7-G1/G2 仍 open；同时抽查 05.6-G1/G2/G3 亦仍 open。T05-06–T05-10 均 planned，没有把未来任务支撑的缺口误关。
- 逐项解析两份清单的 05.1–05.7 覆盖状态，依次仍为 `partial / partial / covered / partial / missing / missing / partial`；05.3 为原基线 covered，不是本轮新晋。所有这些主题的 `content_acceptance_status` 仍 planned：05.1/05.4/05.5/05.6 属 Batch 23，05.2/05.3/05.7 属 Batch 24。05.2 的任务集合仍含未交付的 T05-08/T05-10。
- Markdown 盘点头段继续如实写“本批无主题升为已覆盖”“Batch 17–21 的主题范围记录未在本文件回填（批次账面待订正）”；YAML notes 继续明确无主题升为已覆盖及未来批次归属，不因本次元数据措辞修订改变其余基线口径。
- 与 `34d98c9` 比较，五篇交付正文均逐字节不变，其 SHA-256 与上轮列值相符；稳定 ID、draft、source_checked 均保留。Backlog 全部未变，也就未破坏 closure_criteria 中真实审阅历史、稳定 ID、草稿及真实验证分离的要求。
- Batch 22 exit_gate 的交付、来源审计、修订与定向复核、结构检查、主题范围复核落点仍为上轮报告所列文件；本轮仅关闭两项收尾记录问题。历史 Claude 试用按编写指南 §7 保留，未伪装成当时使用 Codex；主题最终验收不提前到本批。

## 7. 本地结构检查

实际执行 `PYTHONDONTWRITEBYTECODE=1 make check` 与 `PYTHONDONTWRITEBYTECODE=1 make build`，均 exit 0：

```text
PASS: 96 content entries; 446 sources.
Checked structure and local file links; not technical correctness or remote links.
Built build/catalog.json and build/catalog.md.
```

`build/` 为按约定重建的生成目录，`git ls-files build` 无跟踪文件。上述结果只证明结构和本地文件链接，不证明技术主张、远程来源可访问性、版本组合兼容性或现场行为。

## 8. 局限与写入边界

1. 本轮为 C01/C02 的定向复核及必要波及、状态、边界检查；不重新开展整批技术首审，不新增远程技术取证，也不将上轮有限抽查扩充成全量来源重新验证。
2. 历史六份 Claude JSON 的存在性及内容由调用方确认；本审阅者亲读的是库内报告、修订文本和当前 Codex 本地会话元数据，证据等级分别记载。
3. 未运行集群/设备命令，未部署平台、构建镜像、提交作业、运行容器或开展恢复实验；模型审阅与结构校验均不构成平台、硬件或现场验证。没有新实测证据，不标 reproduced。
4. 本轮唯一新增文件为本报告，不修改作者任何源文件或上轮报告，不执行 git 提交或创建分支。开始时既有的审计工作区改动保留，不回滚、不代提交；审阅结论仅在本报告落盘。

## 9. 模型与运行元数据核验

- **指定值、会话自述与实际取证分开：** 用户与指南指定 `gpt-6.1-sol / xhigh`；不能仅据提示词、自述或上一轮 §9 推断本次执行身份。本次重新读取当前本地 CLI JSONL，按 `turn_context` 的 turn ID 区分各轮，而不把共享 session 的所有轮次混为一轮。
- **实际读取的位置：** session ID `01a14a28-8094-70a2-9362-ae55195c77fe`；文件 `~/.codex/sessions/2026/10/17/rollout-2026-10-17T21-58-50-01a14a28-8094-70a2-9362-ae55195c77fe.jsonl`。`session_meta` 为 `originator=codex_exec`、`source=exec`、`cli_version=0.157.1`、`model_provider=custom`，创建于 `2026-10-17T13:58:50.833Z`；另运行 `codex --version`，返回 `codex-cli 0.157.1`。
- **不能隐去的先前不合约尝试：** 同一 JSONL 共见 3 条 `turn_context`：上轮 `gpt-6.1-sol / xhigh`；本地 22:15:56 的 `gpt-6-astra / ultra`；本轮恢复为指定模型/档位。中间一条证实曾有与指定模型/档位不一致的尝试，不能写“整个 session 从未切换/回退”。现有审计作废节称该次 resume 有模型警告、断流、exit 1，未产生有效报告，已弃用并显式重派；其中断流、exit code 和 stderr 细节按作者记录转述，本轮未亲读那个进程的原始 stderr。该尝试不作为有效复核、不计入本轮结论；本轮不是沿用它的审阅产物。
- **本轮上下文核验：** 当前 turn ID 为 `01a14a3a-a0cd-7042-b02b-751a7482e7e1`；时间 `2026-10-17T14:20:15.795Z`（本地 22:20:15）。其 `model=gpt-6.1-sol`、`effort=xhigh`，`collaboration_mode.settings.model=gpt-6.1-sol`、`reasoning_effort=xhigh`。本轮所见上下文为指定单一模型/档位，**不是仅凭会话自述**。本轮没有另启 Codex 子会话或委派其他模型。
- **本轮 fallback 检查：** 成稿前仅对上述当前 turn 已落盘的 5 段 assistant `output_text` 检索实际回退标记，使用与上轮相同的 `[frontier_llm]` 与 `fallback/falling back` 后接 `to/model/:/=` 的模式，命中 0；同时未见本轮错误/失败/中止事件或当前上下文再切换。提示词、工具参数、引用历史报告、作废尝试的记录及本节说明性标记名不冒充当前轮实际回退。`codex --version` 的 PATH aliases 权限警告不是模型回退。
- **核验上限：** 上述确认的是本地 CLI 所记的执行上下文，不是独立服务端路由、底层计算模型或供应商证明；`model_provider=custom` 如实保留，不据此猜测另一个实际模型。历史 Claude 六轮的调用方 `modelUsage` 核验与本次 Codex 本地元数据核验不是同一证据来源，均不构成真实平台或硬件验证。
