# Batch 27 · T07-05 第二轮定向复核

## 会话元数据

| 项目 | 实际记录 |
|---|---|
| 角色与范围 | AI 可靠性知识库批次审阅者；仅核对第一轮仍开放的 C02、C04、C05、C06、C07 及相关修订回归；C01/C03 沿用 CLOSED |
| 实际执行模型 | `gpt-6.1-sol` |
| 实际推理档位 | `xhigh` |
| 核验依据 | 读取本地 CLI rollout 的 `session_meta` 与已记录的全部 `turn_context`；会话 ID 与 `CODEX_THREAD_ID` 一致，`model/effort/cwd` 只有本表所列一组，报告文本无回退标记；本轮直接审阅，未另行派发模型或子代理 |
| 会话 ID | `01a15b34-d254-71e1-b1f3-fc205f25ff92` |
| 运行记录 | `/Users/ywang2397/.codex/sessions/2026/10/21/rollout-2026-10-21T05-25-50-01a15b34-d254-71e1-b1f3-fc205f25ff92.jsonl`；provider=`custom`，CLI=`0.163.0`，source=`exec` |
| 日期与时区 | 2026-10-21，Asia/Shanghai（UTC+08:00）；会话启动于当地 05:25:50 |
| cwd | `/Users/ywang2397/work/AI_reliability_knowledge_base` |
| 审阅基点 | Git HEAD `f1253eeb22086e1837096b0f42bc8d20ff301677` 加读取时的工作区版本；本文行号为原文件坐标 |
| 关闭条件依据 | [第一轮定向复核](batch-27-t07-05-codex-recheck.md)的五项剩余动作；必要时回查[初审](batch-27-t07-05-codex-review.md)，不重做整篇或其他任务验收 |
| 执行边界 | 仓库只新增本报告；不修改被检对象、历史报告、正文状态或任务状态；未安装评估工具，未运行推理、评估或硬件实验 |

被检对象及读取时的 SHA-256：

| 文件 | 行数 | SHA-256 |
|---|---:|---|
| [正文](../../knowledge/07-inference/output-quality-evaluation.md) | 137 | `9573a4b12c137211886a9e1baf84c4fdd87836c0e24de9339ae7248fb949abff` |
| [来源记录](batch-27-t07-05-sources.md) | 58 | `7e283677fdb0afc9674b64a44ebdafa4d74d3ec8d09c4edc7426254bf09a5683` |
| [来源登记](../../sources/registry.yaml) | 6788 | `9410454cb0d1a19a7ad87a18742a265d03891d4b6abc82500045193e6d4b2652` |

方法：读取 README、写作指南、AGENTS.md、相关主题分工和元数据 schema；将五项剩余关闭条件逐条与上述三个文件对照。来源记录的主表与 unknown 清单按当前有效证据记录核对；L49–58 则按其标题作为初审修订轮的历史说明，不用历史说明替代当前表格。

使用 `/tmp/b27-fetch/` 原文件核对以下位置，哈希与初审及第一轮记录相符；没有将网页转换后的行号用作 GitHub 锚点：

| 固定来源／原文件 | 本轮核对位置 | SHA-256 前 16 位 |
|---|---|---|
| vLLM Ascend `52d4acfa51fb868823d1070b81cbd2d97e9e4696` · `using_lm_eval.md` | L107–131 | `29da7eb7d0c595e3` |
| 同快照 · `using_ais_bench.md` | L41–45、L153–194 | `19c3087e40c30cb5` |
| 同快照 · `using_opencompass.md` | L82–105 | `13a4b8c035e3c673` |
| vLLM `b17039bccc17b94a2ea107272ad7bc93508708df` · `int8.md` | L117–139 | `2d0c66123da0334c` |
| MindIE-LLM `69e5a5dd4b533eaffc7e198320435350825a36f7` · `faq.md` | L205–226 | `3c4f5db3c425f401` |
| 同快照 · `developer_guide/test.md` | 全文 3 行 | `de6ea3dae38eeffc` |
| 同快照 · ModelTest `README.md` | L236–283、L332–333 | `17f84a1f37c821d8` |
| 同快照 · ModelTest `README_NEW.md` | L178–184、L267–328 | `5ef09a37be30cd92` |

ModelTest 两份 README 经 GitHub 连接器按固定 commit 重取，逐字节等于第一轮缓存，暂存于 `/tmp/b27-t07-05-recheck-2-evidence/`。另直接打开 PyTorch 2.6 数值精度页及三篇版本化论文摘要，只核对原五项所涉归属；未扩读 ModelTest 实现或论文全文。

## C02/C04/C05/C06/C07 逐项判定

### C02 · CLOSED · 来源主表已同步术语更正

**位置：**正文 L61；来源记录 L29；registry L6735。

来源主表 L29 现已在同一行明确指出 FAQ 的“浮点加法无交换律”为来源术语错误，并将正确解释归于浮点非结合性与运算重排的舍入影响，同时给出 PyTorch 2.6 依据；不再依赖追加的 L52 修订说明。正文与 registry 保留相同更正归属，满足第一轮剩余条件。

这与 [PyTorch 2.6 数值精度说明开篇](https://docs.pytorch.org/docs/2.6/notes/numerical_accuracy.html)一致。[FAQ L218–219](https://github.com/Ascend/MindIE-LLM/blob/69e5a5dd4b533eaffc7e198320435350825a36f7/docs/zh/faq/faq.md#L218-L219)仍用于证明 shuffle-k 开关及其 matmul 性能代价的文档声明，未改写成本库测量或全系统吞吐结论。

### C04 · CLOSED · 抽样、重复单位和差值判据已补齐

**位置：**正文 L80–84、L110、L112–113、L129。

本轮剩余条件均已落入预注册要求：

- L82 要求声明全量或抽样、抽样框与规则、样本量依据、独立重跑的重复单位；同一测试集重跑而不重新抽样，只反映运行波动。
- L83 明确估计方法及置信口径须适用于对照差值和配对／独立样本比较结构；固定测试集观察、对新样本推断和运行波动分别解释。方法例子须服从这一适用性前提，不能仅凭有标准误就认可任意差值推断。
- L83 已明列“不确定范围跨界＝未决”及“重复或有效样本不足、无法形成有效不确定性估计＝未决”；结果判定与恢复行也承接同一规则。
- 容差现明确为实际可接受变化的业务边界，与统计可检出的差异幅度分别声明。L81 的“有变化”须按紧邻 L83 的这一定义理解，不能用作显著性或无差异声明。

官方 [lm-eval L128–131](https://github.com/vllm-project/vllm-ascend/blob/52d4acfa51fb868823d1070b81cbd2d97e9e4696/docs/source/developer_guide/evaluation/using_lm_eval.md#L128-L131)确为分任务／filter 的单指标标准误表；正文现已明确不能直接充当基线与变体差值的不确定性。本项不要求本轮选择统一统计方法或填入未运行样本量。

### C05 · OPEN（实质缺口已修复，降为 P3）· 四个计数字段仍被误称为四类互斥终态

**位置：**正文 L94–113，残留在 L108。

第一轮要求的运行键、基线运行／聚合口径、原始证据引用和重试归并均已补齐：结果行携带 `run_id/exp_id`，沿 `baseline_ref` 定位实际基线运行及用哪次／均值／区间的口径，关联预注册配置；输出、逐样本终态与重试记录可供重算。恢复行明确按同一差值不确定性判据比较，并保留未恢复或仍有混杂时的未决结论。L84 继续要求失败保留在全部提交的质量分母中。

**原 P2 计数问题已修复：**等式已改为“提交数＝完成＋失败＋超时”，空输出预声明归入完成（零分）或失败，二选一；不再把已计入失败的空输出重复加到总数中。逻辑样本／请求尝试的计数单位及多次重试如何归并终态与质量计分，也已要求预声明。

**剩余问题：**L108 同时写“四类互斥且穷尽的请求终态”及“空输出不是第五类”。该行列出的四个字段中，提交数是总数；等式右侧完成、失败、超时才是三类终态。提交总数与其分项不能同时作为互斥类别。这是分类文字与已正确修订的等式不一致，尚不宜认定计数定义全部闭合；但原先会重复计数的实质缺陷已经消除，优先级由 P2 降为 P3。

**最小剩余动作与关闭条件：**把该行改为“四个计数字段；完成／失败／超时为三类互斥且穷尽的终态，提交数为三者之和；空输出不另设第四类，按预声明归入完成或失败”。保留已有等式、空输出零分与二选一归属、重试归并和原始证据要求。修订后只需定向核对该行与 L84/L109 的口径一致性，不需新增字段、验证器或实测。

### C06 · CLOSED · 否定性说法已限定检索范围，ModelTest 已进入可用口径

**位置：**正文 L120、L135–137；来源记录 L31、L37；registry L6735。

正文现表述为“本轮检索范围内未取得”，并在同一句明确范围是 `docs/zh` 目录树清点、非全仓穷举；来源 unknown 清单 L37 同步限定范围，且已将 ModelTest README 级入口列入可用口径。主表 L31 和 unknown L37 均已撤回存根外链说法。这满足第一轮要求，没有再将有限检索写成整个 `docs/` 目录或全仓不存在评估材料。

[test.md 全文](https://github.com/Ascend/MindIE-LLM/blob/69e5a5dd4b533eaffc7e198320435350825a36f7/docs/zh/developer_guide/test.md)确为无外链的三行存根。重取的 [ModelTest README L236–283](https://github.com/Ascend/MindIE-LLM/blob/69e5a5dd4b533eaffc7e198320435350825a36f7/examples/atb_models/tests/modeltest/README.md#L236-L283)、[L332–333](https://github.com/Ascend/MindIE-LLM/blob/69e5a5dd4b533eaffc7e198320435350825a36f7/examples/atb_models/tests/modeltest/README.md#L332-L333)与 [README_NEW L267–328](https://github.com/Ascend/MindIE-LLM/blob/69e5a5dd4b533eaffc7e198320435350825a36f7/examples/atb_models/tests/modeltest/README_NEW.md#L267-L328)支持正文和 registry 的入口描述；新旧接口、脚本判据、模型支持及 Server 端到端关系仍保持 unknown，未升级为服务模式验证。

### C07 · CLOSED · 当前来源主表的坐标与归属已直接更正

**位置：**正文 L54、L62、L74、L119、L121；来源记录 L22、L25–29。

| 第一轮剩余项 | 当前主表与原文件核对结果 |
|---|---|
| lm-eval 命令和时间说明 | L22 现分别为命令 L116–120、时间 L123；安装段另列 L107–120，与[原文件](https://github.com/vllm-project/vllm-ascend/blob/52d4acfa51fb868823d1070b81cbd2d97e9e4696/docs/source/developer_guide/evaluation/using_lm_eval.md#L107-L123)一致 |
| AISBench 上下文要求 | L25 已紧邻注明示例 35000 与注释要求大于 35000 不一致，两说照录并限定指南口径；正文 L54 同时保留“多数数据集”的范围，符合[原文件 L41–45](https://github.com/vllm-project/vllm-ascend/blob/52d4acfa51fb868823d1070b81cbd2d97e9e4696/docs/source/developer_guide/evaluation/using_ais_bench.md#L41-L45) |
| OpenCompass 角色 | L26 直接改为 HUMAN/BOT＋保留 SYSTEM，并在该主张中给出 L82–87，符合[配置原文](https://github.com/vllm-project/vllm-ascend/blob/52d4acfa51fb868823d1070b81cbd2d97e9e4696/docs/source/developer_guide/evaluation/using_opencompass.md#L82-L87) |
| 未量化 baseline 归属 | L27 直接说明未量化模型同任务基线是本库方法，非 INT8 页内容；[INT8 L117–139](https://github.com/vllm-project/vllm/blob/b17039bccc17b94a2ea107272ad7bc93508708df/docs/features/quantization/int8.md#L117-L139)仅给量化侧评测与 BOS 提醒，未再混同归属 |
| FAQ 调度锚点 | L29 已改为 L221–223，正文 L62 同步；[该范围](https://github.com/Ascend/MindIE-LLM/blob/69e5a5dd4b533eaffc7e198320435350825a36f7/docs/zh/faq/faq.md#L221-L223)含标题及支持段，旧 L224–226 已从当前映射撤回 |

正文 L121 继续贴近链接 [AWQ v6](https://arxiv.org/abs/2306.00978v6)、[GPTQ v2](https://arxiv.org/abs/2210.17323v2)、[SmoothQuant v7](https://arxiv.org/abs/2211.10438v7)，保留各自的摘要级作者报告范围与本库未复现边界。本轮重开摘要未见修订引入共同无损保证。C07 的第一轮残留已在当前主表原位置消除，关闭。

## 新问题

没有新增独立发现 ID。C05 的终态类别数文案残留属于原计数关系关闭条件，已在 C05 内记录并降级，不另计一项。除该处外，本次五项修订范围内未发现需要另立发现的回归；C01/C03 的 CLOSED 状态沿用第一轮。

## 整体结论

**本轮定向复核尚未通过全部关闭条件：C02、C04、C06、C07 关闭；C05 仅剩 P3 终态类别数文案修订。** 第一轮开放的四项 P2 实质缺口均已修复，原 C07 的 P3 证据同步问题也已消除；当前没有开放 P1/P2。完成 C05 所列最小修订并定向复核前，不声明 T07-05 全部审阅通过。

`make check` 通过（112 content entries / 542 sources）；`make build` 在包含本报告的临时源码副本通过，构建产物只写入临时副本，工作区 `build/` 未改动。`git diff --check` 与新增报告的尾随空白核验通过。对读取阶段记录的 586 个既有文件比较 SHA-256，无改动或删除；本会话只新增本报告。检查期间工作区另出现 `docs/research/batch-27-t07-07-codex-recheck-2.md`，本会话未写入该文件，不属于本轮编辑。未修改 `src/kb/`，未运行工具代码测试。

本报告不改变正文的 `draft / source_checked` 状态；结构检查与模型审阅均不构成评估执行成功、平台兼容性或真实硬件验证。

本轮 C02/C04/C05/C06/C07：CLOSED 4、OPEN 1（C05，P3）；累计 C01–C07：CLOSED 6、OPEN 1；开放优先级：P1 0、P2 0、P3 1；新增独立发现 0；整体：尚未全部通过，待 C05 最小文案修订及定向复核。
