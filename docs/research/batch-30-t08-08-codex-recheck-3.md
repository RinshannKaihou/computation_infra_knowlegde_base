# Batch 30 · T08-08 第四轮定向复核报告

## 会话元数据

| 项目 | 记录 |
|---|---|
| 审阅角色 | 独立批次审阅者；仅复核第三轮修订后的 C07、C08、N01 及该修订引入的问题，不承担正文编写或修订 |
| 实际执行模型 / 档位 | `gpt-6.1-sol / xhigh`，符合本次用户指定 |
| turn_context 核验方法 | 用环境中的 `CODEX_THREAD_ID`、`CODEX_SESSION_ID` 定位当前会话 JSONL，核对全部 `turn_context` 的 `model`、`effort`、`cwd` 及嵌套 `collaboration_mode.settings`；不以默认配置或其他会话代替 |
| 核验结果 | 当前仅一条 `turn_context`：`model=gpt-6.1-sol`、`effort=xhigh`、`cwd=/Users/ywang2397/work/AI_reliability_knowledge_base`；嵌套 `model/reasoning_effort` 一致。写报告前已产生的 3 条 assistant 消息无回退标记，未观察到路由失败或模型回退 |
| 核验坐标 | `/Users/ywang2397/.codex/sessions/2026/10/21/rollout-2026-10-21T21-50-03-01a15eb9-d722-7af1-bc57-e0cd9c7d1973.jsonl` L8；时间戳 `2026-10-21T13:50:20.784Z`；turn ID `01a15eb9-e5dd-7231-9ef8-c2fad367bdf8` |
| 会话 ID / 执行方式 | `01a15eb9-d722-7af1-bc57-e0cd9c7d1973`；当前本地 Codex CLI 直接审阅，`originator=codex_exec`、CLI `0.163.0`、`source=exec`；未另启模型或审阅子代理 |
| 日期 / 时区 | 2026-10-21 / Asia/Shanghai（UTC+08:00） |
| 写入范围 | 仅新增 `docs/research/batch-30-t08-08-codex-recheck-3.md` |

## 依据链与输入快照

先读 `README.md`、`AGENTS.md`、[写作指南](../authoring-guide.md)、[归属规则](../../content-outline.md)和 metadata schema；对照[初审 C07/C08 的原始关闭条件](batch-30-t08-08-codex-review.md)、[第一轮复核及 N01 关闭条件](batch-30-t08-08-codex-recheck.md)、[第二轮复核的剩余差距](batch-30-t08-08-codex-recheck-2.md)，重读两篇修订后正文与[来源记录](batch-30-t08-08-sources.md)，定向检查 [registry](../../sources/registry.yaml)。T08-08 的场景覆盖验收及 V12 仅用于核对本轮边界；不重审已关闭的 C01–C06、C09、C10。

| 输入 | 行数 | SHA-256 |
|---|---:|---|
| [诊断评测方法规范](../../knowledge/08-reliability/diagnostic-evaluation-method.md) | 102 | `35561b63bf98e94c2a8967c8a2d6877d2325dd8d804c60b8c7248f043b9894da` |
| [诊断评测公开题组](../../knowledge/08-reliability/diagnostic-evaluation-fixtures.md) | 133 | `4bcd451e76559cc6ce6bd68adbfa355be51c80abf8230ca4444d88276b7ad8b1` |
| 初审报告 | 163 | `b9358fd085ed468ef52c0e793266c42135ad4fac3cb247f6b63f07885ba1a9f0` |
| 第一轮复核报告 | 94 | `d3ea7a2e04445c8e0f98a3884a309a8a990d7010432389f54b498d1dbaee5d26` |
| 第二轮复核报告 | 83 | `b5b8f7a37cdda527b631563edee1048c2f54436be085160cd1c150515b1f6dc6` |
| 来源记录 | 54 | `e9beb7548d31824f7059ff25dce4f9021714386840d815de063053f33f1859fc` |
| registry | 7227 | `0e0defed4ec29acd3722f8f78dd4926b3e88441c7a48e59a4db96e0b976275b5` |

下文行号均指上述快照。来源记录 L37–48、L50–54 分别保留初审后和第二轮修订记录；**当前文件未见单列的第三轮修订记录**，其哈希与上一轮报告所列相同。本轮直接核对题组 L20/L126 及 registry L6970 的实际内容，不把不存在的修订记录或作者处置自述当成本轮核验结果。该审计记录缺口不妨碍从实际正文判断下列关闭条件。

## 逐项状态表

| 编号 | 优先级 | 状态 | 对照历轮关闭条件及剩余差距的结果 |
|---|---|---|---|
| C07 | P2 | **CLOSED** | 题组 L126 现在完整列出六域、无法判定样例及三处合成范围；L106–113 的 PTF-10 仍有独立的文件完整性观察、固定证据、判据与下一项检查。总数十题，L42/L129 保持公开教学及非 holdout 边界。上一轮唯一剩余的合成题号映射遗漏已消除 |
| C08 | P3 | **CLOSED** | 题组 L20 已声明 `src.arxiv.sdc-llm-training-2502-v1`，与 L86 的精确版本入口及 registry L7214–7227 接通；Llama v3、Meta ID、RCACopilot v4 许可和 PyTorch 文件入口安排保持正确。Meta notes 已补具体重定向链记录，满足前轮允许的入口补证路径；独立读取限制与证据归属见下文 |
| N01 | P2 | **CLOSED** | 题组 L22、L37、L99、L108、L117、L126 及来源记录 L52 的三处合成范围一致：PTF-08 的本地情境、PTF-09 全条、PTF-10 的现场情境。PTF-10 L110 继续以“假设情境”引入，不再把公开代码机制当作现场事件记录；原关闭条件“所有合成范围声明一致”满足 |

C07 与 N01 保留各自 ID，但共享同一已修复的标注残留，不重复计作新发现。

## 定向上游核验与关闭理由

### C07 / N01：合成范围已同步，存储判分内容与证据边界保留

本轮通过 GitHub 只读连接器取得固定 commit 的原文件，按原文件行序核对 [serialization.py L184–209](https://github.com/pytorch/pytorch/blob/1eba9b3aa3c43f86f4a2c807ac8e12c4a7767340/torch/serialization.py#L184-L209)：默认 CRC32 选项及关闭该选项后外部解压可能报 CRC 问题、`torch.load` 仍可加载的文档说明均在。它支持反驳“加载成功就保证字节正确”的一般保证，不能证明题设中的恢复异常事件发生过。PTF-10 的假设标注与独立内容校验判据保持这一区分。

相邻[Checkpoint 完整性正文](../../knowledge/04-data-storage/checkpoint-integrity-evidence.md) L60–69、L92/L114 仍区分形状与内容检查，并保留 C++ reader 全路径未逐行核对及全部实测未执行的限制。本轮没有把 Python 文档证据扩大为对全部 C++ 分支的独立验证。题组 L126 已明确 PTF-08/09/10 的完整合成范围，摘要、verification notes 和局部标注之间不再存在上一轮指出的遗漏；不需要为关闭该项新增题目或执行损坏注入。

### C08：来源依赖已接入，入口安排可追溯

去除 URL 页内 fragment 后逐字比较：方法正文外链 **6/6** 对应本篇 `source_refs` 的主 `url`；题组正文外链 **11/12** 对应本篇 `source_refs` 的主 `url`，余 **1/12** 为已声明的 `src.pytorch.dcp-2.6` notes 中明确列出的固定 `serialization.py` 文件入口。按前轮已接受的等效明确入口安排，题组实际使用的 **12/12** 外链均可追溯到本篇声明来源，不以“全 registry 能找到”替代本篇依赖检查。

- **PTF-06**：题组 L20、L86 与 registry L7216 的 `https://arxiv.org/abs/2502.12340v1` 一致。重新打开[固定 v1 入口](https://arxiv.org/abs/2502.12340v1)及其[HTML 附录 D](https://arxiv.org/html/2502.12340v1)：D.1–D.4 分别为实验细节、结果、可能解释和低精度讨论，D.2 保留 float32 ABFT 与 bf16 失配率不必对应的说明。没有用 ACL 的附录编号替换 v1 坐标。`verification.evidence_refs` 仍保留 ACL 来源，不要求它穷举全部依赖；本次缺口针对的 `source_refs` 已补齐。
- **其他已修复入口与许可**：Llama 两处外链与已声明的 v3 主 URL 一致，本轮打开[该 v3 入口](https://arxiv.org/abs/2407.21783v3)确认版本。来源记录 L19 的 Meta ID 可解析。重新核对 [RCACopilot v4 许可栏](https://arxiv.org/html/2305.15778v4)及其[CC BY 4.0 链接](https://creativecommons.org/licenses/by/4.0/)，与 registry L7163–7169 一致；未把论文许可扩大到 Issue 讨论或其他材料。
- **Meta 登记入口**：题组 L72 与 registry L6962 逐字相同。registry L6970 现在明确记录作者于 2026-10-21 使用 curl 跟随重定向后的 HTTP 200、一次重定向、最终 `networking-traffic` URL、标题及 canonical，补全前轮要求的旧入口与实际文章之间的追溯链。本轮独立核读了[该最终文章](https://engineering.fb.com/2021/10/05/networking-traffic/outage-details/)，标题及相关复盘段落相符；接受该明确跳转记录作为登记入口补证。**旧入口的 HTTP 200、重定向次数及 canonical 仍属于作者记录，本轮未独立复现**：网页工具继续报该 URL 不可读，本地 curl 对两路径均因 DNS 解析失败退出（exit 6，未取得 HTTP 响应）；浏览器补充通道无可用实例。此限制不作旧入口 HTTP 错误的证据，也不冒充本轮实测。C08 关闭的是来源入口、依赖与许可的追溯缺口，不是对远程服务可用性的保证。

## 新发现、检查与限制

未发现本次修订引入、需要从 **N20** 起编号的独立新问题。未单列第三轮修订记录的事实已在输入说明中保留；来源记录 L52 的合成范围本身与现行正文一致，不据此重开 N01。

两篇 frontmatter 通过带日期格式检查的 JSON Schema 校验；已声明 `source_refs` 全部可解析，本地 Markdown 文件链接目标存在，题组标题计数为十条。两篇仍为 `reference / reliability / draft / generic / source_checked`。这些是定向结构与引用检查，不是技术兼容性、远程全文正确性或实验结果证明。

本会话唯一仓库写入为本报告；未修改正文、来源记录、registry、导航、计划或代码。交付前后核对上述输入哈希。开始时已有作者修订及多份未跟踪审阅报告，期间其他任务的报告也有并发新增，均非本会话写入。本轮不是知识内容修订，未运行 `make check`、`make build` 或 `make test`，未生成构建产物；未执行来源材料中的代码、评测系统、checkpoint 保存/加载、故障注入或 GPU/NPU 测试。

V12 的独立输入/答案、授权与脱敏审查、执行记录仍未取得；本轮公开题组复核不关闭该缺口。**模型审阅不替代真实环境验证。** 本轮结论仅覆盖 C07、C08、N01，不对其他编号重新背书，也不代表整个 Batch 30 通过。

## 结论

**3/3 CLOSED（C07、C08、N01）；OPEN：无；无新增 N20 起发现。**
