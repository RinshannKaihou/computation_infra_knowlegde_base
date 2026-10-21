# Batch 30 · T08-07 定向复核报告（第四轮）

## 会话元数据

| 项目 | 记录 |
|---|---|
| 审阅角色 | 独立批次审阅者；仅复核第三轮修订后的 C04 及相关修订后果，不承担正文编写或修订 |
| 约定 / 实际执行模型 | 用户指定 `gpt-6.1-sol / xhigh`；本会话实际核验一致 |
| turn_context 核验方法 | 由环境变量 `CODEX_THREAD_ID`、`CODEX_SESSION_ID` 定位本会话 JSONL，核对 `session_meta.id`、cwd 和首条审阅进度消息，再读取全部 `turn_context`；不以配置默认值或其他会话代替 |
| turn_context 核验结果 | 共 1 条；`model=gpt-6.1-sol`、`effort=xhigh`、`cwd=/Users/ywang2397/work/AI_reliability_knowledge_base`；`collaboration_mode.settings.model/reasoning_effort` 同值；写入前复查未观察到模型切换或回退 |
| 核验坐标 | `/Users/ywang2397/.codex/sessions/2026/10/21/rollout-2026-10-21T21-50-05-01a15eb9-d721-7be1-b9c3-c76cb236c166.jsonl` L8，时间戳 `2026-10-21T13:50:15.301Z`；首条进度消息在 L13（`2026-10-21T13:50:19.028Z`），内容与本次任务一致 |
| 会话 ID / turn ID | `01a15eb9-d721-7be1-b9c3-c76cb236c166` / `01a15eb9-eca0-7943-bc5d-24d51e13dec7` |
| 执行方式 | 当前本地 Codex CLI 会话直接复核；`session_meta.originator=codex_exec`、CLI `0.163.0`、`workspace-write`；未另启模型、OpenCode 或审阅子代理 |
| 日期 / 时区 | 2026-10-21 / Asia/Shanghai（UTC+08:00） |
| 写入边界 | 仅新增本报告；保留既有工作区变更，不修改正文、来源记录、registry、历史报告、计划、导航或构建产物 |

以下行号对应本轮读取基准：

| 对象 | 行数 | SHA-256 |
|---|---:|---|
| [初审报告](batch-30-t08-07-codex-review.md) | 127 | `8fd2233be0103de03f7d6de0cbe1ee86ee9a2cee8da7ba12633164d75d28e6ec` |
| [第一轮复核（第二轮审阅）](batch-30-t08-07-codex-recheck.md) | 84 | `1aa66a30660e1cd0736947cd9de330567dc9bf5e8cdaf4959946a553a748c994` |
| [第二轮复核（第三轮审阅）](batch-30-t08-07-codex-recheck-2.md) | 57 | `c67c54fd7a04b245dba4227fffb60fcfeca3899aba13f26700dad38b62b080a7` |
| [修订后正文](../../knowledge/08-reliability/postmortem-and-knowledge-update.md) | 146 | `7ec8bb89866e3564a3ba1ea97959823aedc5cb75f6dd45c7244a445968358c33` |
| [来源与修订记录](batch-30-t08-07-sources.md) | 37 | `2a272ccf0088088ea4ef40d8fc718b3a3be146230a6ab89908f41209df5025cf` |
| [来源登记](../../sources/registry.yaml) | 7227 | `0e0defed4ec29acd3722f8f78dd4926b3e88441c7a48e59a4db96e0b976275b5` |

## 逐项状态

| 编号 | 优先级 | 状态 | 关闭条件与本轮判断 |
|---|---|---|---|
| C04 | P3 | **CLOSED** | 初审 L80–87 要求取证 ID 可解析、正文上游 URL 与对应 registry 登记入口逐字一致，且所选 Meta 入口能定位已核实的同篇原文并保留实际访问观察。第一轮复核 L52–60 留下入口响应与同篇关系的补证缺口；第二轮复核 L36/L47 明确仍缺标题、有效 URL 或重定向等可核对信息。本次来源记录 L36 与 registry L6969 已补请求 URL、工具、日期、最终 HTTP 200、一次重定向、最终 URL、标题和 canonical。最终 URL 与本轮独立读取的原文入口完全相同，标题及文章日期吻合，所缺的同篇定位链已补齐。正文 L14/L144、来源记录 L19 与 registry L6959–6961 的稳定 ID 和登记 URL 仍一致；全部 7 处远程内联链接均匹配对应已登记来源。 |

## C04：定向证据与访问边界

第三轮修订未改变正文，主要在来源记录 L36 和 registry L6969 补充作者请求结果。本轮按前轮明确留下的关闭条件核对这些新增字段，不追加整篇复审或真实环境实验要求。

| 证据层次 | 核对对象与结果 | 判断边界 |
|---|---|---|
| 作者补证记录 | 2026-10-21，作者记载以 `curl -sL` 跟随重定向、30 s 上限请求[登记入口](https://engineering.fb.com/2021/10/05/networking/outage-details/)，最终 HTTP 200，重定向 1 次，最终 URL 为 `https://engineering.fb.com/2021/10/05/networking-traffic/outage-details/`；页面标题为 *More details about the October 4 outage - Engineering at Meta*，canonical 指向该最终入口；来源记录另记响应正文 88403 字节。直接请求最终入口亦记为 200。registry 的对应记录一致 | 这些是作者的请求观察，本轮未独立测得状态码、重定向次数、canonical 或字节数；200 按跟随重定向后的最终响应理解，不补写未记录的首跳状态码 |
| 本轮独立上游核对 | 网页工具可读取上述[最终入口原文](https://engineering.fb.com/2021/10/05/networking-traffic/outage-details/)，页面标题吻合，发布日期为 2021-10-05；定向查看容量评估命令与审计工具、DNS 撤告及恢复段，确认所到达的是历轮已核读文章 | 独立核对了作者所记最终 URL 所指的文章身份；未据此宣称独立观察到登记入口的重定向 |
| 本轮登记入口访问 | 网页工具打开登记精确 URL 仍返回无法通过工具访问，未提供 HTTP 状态、重定向链或正文 | 这是本轮工具可达性限制，不判定公网失效或 HTTP 404 |
| 本轮本地直连 | 对两个精确 URL 分别用 curl GET、跟随重定向、25 s 上限请求，均退出码 6：`Could not resolve host: engineering.fb.com`；状态输出 `000`，重定向数 0，下载量 0 | 失败发生在 DNS 阶段，没有收到 HTTP 响应；不用于否定作者在其访问条件下的观察 |

与前轮仅有“两入口均 200”相比，现在已有“登记请求 URL → 作者记录的一次重定向 → 精确最终 URL → 标题/canonical”的响应定位记录，并能把该最终 URL 与本轮独立可读原文交叉对应。这满足第二轮复核 L47 所要求的“由编写/登记角色补充可核对响应或重定向证据，并提供足以识别文章的内容”。本项关闭依据是新增作者补证与独立原文核对的组合；本轮登记入口的直接 HTTP 复测仍未成功，两者分别记录。

## 新发现与检查边界

本次定向范围内未发现第三轮修订引入的独立新问题，无 N20 起新增项。C01、C02、C03、C05 与 N01 沿用前轮 CLOSED 结论，不在本次重审范围；C02 的既有 P3 注记仍不计为未闭项。未审核 registry 中其他任务的来源主张。

只读定向检查通过：正文 frontmatter 符合 Draft 2020-12 schema 与日期格式要求；8 个 `source_refs`、来源记录中出现的 7 个不同来源 ID 均可解析；registry 无重复 ID；正文 7 处远程内联链接（5 个唯一 URL）均与相应登记入口逐字一致。这些本地检查只证明结构及引用匹配，不代替远程访问或技术正确性判断。

本轮仅新增研究审阅报告，未改变知识正文或构建输入，未运行 `make check`、`make build`、`make test` 或重建 catalog；不将定向检查记作全仓检查通过。写入后复查，本轮读取基准中的 664 个已跟踪及未忽略文件内容均未改变；工作区同期另出现其他任务的复核报告，非本会话写入，未触碰。本会话的唯一仓库写入目标为本报告。正文仍为 `draft / source_checked`；未执行现场诊断、负载、恢复、故障注入或硬件验证，模型审阅不替代真实 GPU/NPU 环境验证。

**第四轮结论：本轮 1/1 CLOSED（C04），无新增 OPEN；承接前轮累计 6/6 CLOSED，T08-07 在历轮既定审阅范围内通过。不作 Batch 30 整批通过或真实环境验证声明。**
