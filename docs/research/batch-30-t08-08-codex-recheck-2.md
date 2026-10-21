# Batch 30 · T08-08 第三轮定向复核报告

## 会话元数据

| 项目 | 记录 |
|---|---|
| 审阅角色 | 独立批次审阅者；仅复核第二轮修订后的 C07、C08、C09、N01，不承担正文编写或问题修订 |
| 实际执行模型 / 档位 | `gpt-6.1-sol / xhigh`，符合本次用户指定及写作指南 §7 |
| 模型核验方法 | 以环境中的 `CODEX_THREAD_ID`、`CODEX_SESSION_ID` 定位本会话 JSONL，读取最新 `turn_context` 的 `model`、`effort`、`cwd` 及嵌套 `collaboration_mode.settings`；未以配置默认值或其他会话代替 |
| 模型核验结果 | 本会话全部 `turn_context` 仅一个模型：`gpt-6.1-sol`；`effort=xhigh`；`cwd=/Users/ywang2397/work/AI_reliability_knowledge_base`；嵌套 `model/reasoning_effort` 一致；已产生的 assistant 输出文本未见 `[frontier_llm]` 标记，未观察到回退 |
| 模型核验坐标 | `/Users/ywang2397/.codex/sessions/2026/10/21/rollout-2026-10-21T21-38-26-01a15eaf-4097-7301-9efd-8b717e5f9143.jsonl` L8；时间戳 `2026-10-21T13:38:51.416Z`；turn ID `01a15eaf-42ae-78d0-a159-e44ebecabf8f` |
| 会话 ID / 执行方式 | `01a15eaf-4097-7301-9efd-8b717e5f9143`；当前本地 Codex CLI 直接审阅，`originator=codex_exec`、CLI `0.163.0`；未另启模型或审阅子代理 |
| 日期 / 时区 | 2026-10-21 / Asia/Shanghai（UTC+08:00） |
| 写入范围 | 仅新增本报告；正文、来源记录、registry、导航、计划与构建产物均不修改 |

## 复核输入与方法

重读 `README.md`、`AGENTS.md`、[写作指南](../authoring-guide.md)、[归属规则](../../content-outline.md)、[初审原始关闭条件](batch-30-t08-08-codex-review.md)、[第一轮复核的剩余差距](batch-30-t08-08-codex-recheck.md)、两篇修订后正文、[来源记录及第二轮修订记录](batch-30-t08-08-sources.md)，并定向检查 [registry](../../sources/registry.yaml) 的有关条目。C07 另对照 T08-08 的场景覆盖验收要求；相邻 checkpoint 正文仅用于核对存储判据的证据边界。本轮不重审已关闭的 C01–C06、C10。

| 输入快照 | 行数 | SHA-256 |
|---|---:|---|
| [诊断评测方法规范](../../knowledge/08-reliability/diagnostic-evaluation-method.md) | 102 | `35561b63bf98e94c2a8967c8a2d6877d2325dd8d804c60b8c7248f043b9894da` |
| [诊断评测公开题组](../../knowledge/08-reliability/diagnostic-evaluation-fixtures.md) | 132 | `66c02772679f42a22e5e1adcc406aaaee63f92db57a3c99884ba969715a0795c` |
| 初审报告 | 163 | `b9358fd085ed468ef52c0e793266c42135ad4fac3cb247f6b63f07885ba1a9f0` |
| 第一轮复核报告 | 94 | `d3ea7a2e04445c8e0f98a3884a309a8a990d7010432389f54b498d1dbaee5d26` |
| 来源记录 | 54 | `e9beb7548d31824f7059ff25dce4f9021714386840d815de063053f33f1859fc` |
| registry | 7226 | `334b739bf47e5032bc702f87b3c23d53199dc6b8d6cd6181e35c30c37cda7536` |

以下“方法 L…”、“题组 L…”、“来源记录 L…”及 registry 行号均指上述快照。重新打开 Cloud-OpsBench v1、ABFT arXiv v1、Llama 3 v3 的固定入口与相关 HTML 节，核对 RCACopilot v4 许可栏，并通过 GitHub 只读连接器读取固定 PyTorch commit 的 `serialization.py` L177–215。Meta 两种路径分别尝试读取，限制另记于 C08。没有运行上游材料中的代码或命令。

## 逐项状态表

| 编号 | 优先级 | 状态 | 对照原始关闭条件及第一轮剩余差距的结果 |
|---|---|---|---|
| C07 | P2 | **OPEN** | 十题、六域及无法判定样例的映射仍在；PTF-10 L105–112 有实际存储完整性输入、固定证据与独立内容校验判据，且已标构造输入，公开题组仍不充当 holdout。但 L125 的合成题号映射仍只列 PTF-09，未同步 PTF-08/10，与原关闭条件“新增合成内容准确标注”及第一轮明确要求的合成范围同步尚有差距；与 N01 为同一残留 |
| C08 | P3 | **OPEN** | Llama v3 URL 已对齐；PTF-10 的精确文件 URL 已在 `src.pytorch.dcp-2.6` notes 明列，满足第一轮允许的等效明确入口安排；Meta ID、RCACopilot v4 许可正确。但新登记的 `src.arxiv.sdc-llm-training-2502-v1` 仅在题组 L85 和来源记录 L21 以文字引用，未加入题组 L8–19 的 `source_refs`；题组声明的论文依赖仍只有 ACL 版，未完成精确版本入口与本篇来源元数据的连接。Meta 旧入口独立读取也仍有限制，见下文 |
| C09 | P3 | **CLOSED** | 来源记录 L10 已就地改为 Cloud 固定 v1 与 §3.2/§4.2；L21 明确 arXiv v1 D.1–D.4 及其独立登记 ID；L22 改为 Llama §3.3.4/Table 5。与方法 L84/L99、题组 L85/L92/L101 和 registry 的版本说明一致。重新打开固定版本可找到对应定义、结果和表，原来的 §5、§2.2 与两版附录混用问题已消除 |
| N01 | P2 | **OPEN** | PTF-10 标题、L107 合成标注与 L109“假设情境”已明确来源身份，L21/L36 及来源记录 L52 也同步为三处合成。第一轮要求的局部标注已完成；但 L125 仍以“合成＝PTF-09”提供不完整的合成范围映射，未满足原关闭条件“所有合成范围声明一致” |

## 未闭项的具体残留

### C07 / N01：局部标注已补，合成范围映射仍遗漏两题

题组 L21、L36 明确列出三处合成内容：PTF-08 的本地情境、PTF-09 全条、PTF-10 的现场情境；L98、L107、L116 的逐题标注与此相符。PTF-10 也不再把训练继续、偶发数值异常和现场人员判断冒充公开事故事实。重新读取的 [PyTorch 固定源码 L196–209](https://github.com/pytorch/pytorch/blob/1eba9b3aa3c43f86f4a2c807ac8e12c4a7767340/torch/serialization.py#L196-L209)是 CRC32 配置与加载行为的文档依据，不能证明该假设事件发生过；修订已正确划开这条边界。

残留在**题组 L125**：使用规则仍写“无法判定＝PTF-08、合成＝PTF-09”，没有列出 PTF-08 的合成本地情境与 PTF-10 的合成现场情境，也没有声明这里只列专门的工具输出夹具、完整合成范围另见何处。这正是第一轮复核 N01 已指出的题号映射遗漏，不能仅凭摘要和逐题修复将整项关闭。

剩余关闭条件：使该使用规则中的合成范围与三处逐题标注一致，或明确限定该栏目含义并指向完整的合成范围说明；保持公开机制事实与假设症状的区分。C07 的存储判分内容、十题数量和六域覆盖已经满足，无须为本项再增加题目或执行损坏注入实验。C07、N01 保留各自 ID，但不把这个共同残留计作两个新问题。

### C08：精确入口已登记，正文来源元数据还未接入

本轮去除 URL 页内 fragment 后逐字比较：方法外链 **6/6** 对应本篇 `source_refs` 条目的主 `url`；题组 **11/12** 对应全表某条主 `url`，其中只有 **10/12** 对应本篇实际声明的 `source_refs` 主 `url`。这三种口径不同，不能互相代替：

| 入口 | 已完成部分 | 尚缺部分 / 核验边界 |
|---|---|---|
| PTF-06 的 arXiv v1 | registry L7213–7226 新条目存在，L7215 与题组 L85 URL 逐字一致；明确区分 arXiv D.1–D.4 与 ACL D.1/D.2，来源记录 L21 同步 | 新 ID 未列入题组 `source_refs`。按写作指南 §3、§5，登记后仍须把实际使用来源 ID 接入正文元数据；正文内写出 ID 不能替代该依赖字段。此处是 C08 原有精确版本追溯未完成，不另记 N10 |
| PTF-07/08 的 Llama v3 | registry L7034 起的主 URL 已固定 v3，与题组两处及所声明来源一致 | 该入口差异已消除 |
| PTF-10 的 `serialization.py` | registry L321 notes 明列与题组 L110 逐字相同的固定文件 URL；正文也明确说明此入口登记在哪个来源条目 | 接受为第一轮允许的“等效明确入口安排”，不再要求为同一文件另外新建来源 ID；不能把主 URL 机械匹配不足 12/12 单独当作失败 |
| Meta 旧登记路径 | registry L6969 新增作者记录：2026-10-21 两路径经 curl 均返回 200，并称为同一文章；题组与登记 URL 一致 | 本轮网页工具仍无法读取 `/networking/` 路径；本地只读 HTTP 请求因 DNS 解析失败，两路径均未取得响应。成功读取的是 [networking-traffic 路径](https://engineering.fb.com/2021/10/05/networking-traffic/outage-details/)。作者的 200 记录已补，但本轮未独立复现旧路径的响应或同文内容；不把工具失败解释成 HTTP 404，也不否定复盘事实 |

重新打开 [RCACopilot v4](https://arxiv.org/html/2305.15778v4)，许可栏为 CC BY 4.0，与登记一致；来源记录 L19 的 Meta ID 可解析。有关子问题维持关闭。C08 至少仍须完成 PTF-06 的来源元数据连接；旧 Meta 路径的可核读性保留上述独立取证限制，不把作者新增记录写成本轮实测结果。

## C09 的上游定位核验

本轮采用固定版本 HTML 定向核读，核验的是版本、节号与支持内容，不声称完成新的 PDF 页序或图像核验：

- [Cloud-OpsBench v1](https://arxiv.org/html/2603.00468v1)：§3.2 为 State Snapshot 范式，§4.2 为 Evaluation Metrics，下分 §4.2.1 与 §4.2.2；来源记录已固定 v1，不再把 §5 当指标定义，也未要求改用 v2。
- [ABFT arXiv v1](https://arxiv.org/html/2502.12340v1)：附录 D.1 实验细节、D.2 结果、D.3 可能解释、D.4 低精度讨论均可定位；D.2 明确两种精度设置的发生率不必对应。正文、取证表与 registry 已选择这组坐标；C08 的元数据连接缺口不改变节号已经核正的判断。
- [Llama 3 v3](https://arxiv.org/html/2407.21783v3)：§3.3.4 内可找到 Table 5 及 Unknown/NCCL watchdog 行；来源记录不再将其定位到 §2.2。表中计数与百分比的来源自身差异不在本轮重新裁定。

## 新发现、检查与限制

未发现需要从 N10 起另行编号的独立新问题。合成范围映射遗漏沿用 C07/N01；PTF-06 来源元数据连接未完成沿用 C08，避免重复计数。

两篇 frontmatter 通过带日期格式检查的 JSON Schema 校验，已声明的 `source_refs` 均可解析，正文相对文件链接目标存在；两篇仍为 `reference / reliability / draft / generic / source_checked`。这些检查不会发现“实际使用的新来源没有列入 `source_refs`”这类语义遗漏，也不证明远程来源、技术兼容性或实验正确性。

本轮只新增审阅报告，未改正文或代码；没有运行 `make check`、`make build`、`make test`，没有生成构建产物。执行的本地操作限读取、哈希、定向结构/引用检查和上游只读取证；没有运行评测系统、故障注入、checkpoint 保存/加载或 GPU/NPU 测试。开始时已有作者修订和多份未跟踪审阅报告，均不作为本会话产出；交付前后核对上述输入快照，未由本会话更改。

V12 的独立输入/答案、授权与脱敏审查、执行记录缺口仍保留。模型审阅不替代真实环境验证，本报告不对其他任务或整个 Batch 30 作通过声明。

## 结论

**本轮 1/4 CLOSED（C09）；OPEN：C07、C08、N01。C07 与 N01 共享同一剩余标注缺口；无新增 N10 起发现。T08-08 暂不通过，须完成剩余修订后继续定向复核。**
