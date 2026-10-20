# Batch 27 · T07-05 第一轮定向复核

## 会话元数据

| 项目 | 实际记录 |
|---|---|
| 角色 | AI 可靠性知识库批次审阅者；仅复核初审 C01–C07 的关闭条件与相关修订回归 |
| 实际执行模型 | `gpt-6.1-sol` |
| 实际推理档位 | `xhigh` |
| 核验依据 | 读取本地 CLI rollout 的 `session_meta` 与全部已记录的 `turn_context`；会话 ID 与 `CODEX_THREAD_ID` 一致，`model/effort/cwd` 只有本表所列一组；本轮未另行派发其他模型或子代理 |
| 会话 ID | `01a15b2d-c9e3-75c0-b6b2-c71faf0e52a9` |
| 运行记录 | `/Users/ywang2397/.codex/sessions/2026/10/21/rollout-2026-10-21T05-18-09-01a15b2d-c9e3-75c0-b6b2-c71faf0e52a9.jsonl`；provider=`custom`，CLI=`0.163.0`，source=`exec` |
| 日期与时区 | 2026-10-21，Asia/Shanghai（UTC+08:00）；会话启动于当地 05:18:09 |
| cwd | `/Users/ywang2397/work/AI_reliability_knowledge_base` |
| 审阅基点 | Git HEAD `f1253eeb22086e1837096b0f42bc8d20ff301677` 加本轮读取时的工作区内容；行号均为原文件坐标 |
| 初审依据 | [batch-27-t07-05-codex-review.md](batch-27-t07-05-codex-review.md) 的 C01–C07；不重做整篇初审或其他任务验收 |
| 执行边界 | 只新增本报告；不修订被检对象、不改历史报告、正文状态或任务状态；未安装评估工具，未运行推理、评估或硬件实验 |

被检对象及读取时的 SHA-256：

| 文件 | 行数 | SHA-256 |
|---|---:|---|
| [正文](../../knowledge/07-inference/output-quality-evaluation.md) | 132 | `41e674c32350cf1151b3051df847a65ef49bbae2ebb75a4c222b6694db51f4a4` |
| [来源登记](../../sources/registry.yaml) | 6788 | `30435a08607d0207cbef085d665060dd9575a65b32f89bb2927730110453bf42` |
| [来源记录](batch-27-t07-05-sources.md) | 58 | `5212372b06c42f9dfc1daea94dbe36be15ee3d7b745158bbad47291d428f4e12` |

方法：读取 README、写作指南、AGENTS.md 与相关内容分工；将当前正文、registry 对应条目及来源记录与初审关闭条件逐项对照。来源记录 L49–58 是追加的修订说明；其前面的主张表和 unknown 清单没有标为已失效的历史快照，因此仍按当前证据链核对，不能仅凭修订说明自述认定关闭。

本轮用 `/tmp/b27-fetch/` 原文件核对以下位置，缓存哈希与初审记录相符；没有把网页转换后的行号用作 GitHub 锚点：

| 固定来源／原文件 | 本轮定向核对位置 | SHA-256 前 16 位 |
|---|---|---|
| vLLM Ascend `52d4acfa51fb868823d1070b81cbd2d97e9e4696` · `using_lm_eval.md` | L116–123、L128–131、L230–275 | `29da7eb7d0c595e3` |
| 同快照 · `using_ais_bench.md` | L41–45、L153–194 | `19c3087e40c30cb5` |
| 同快照 · `using_opencompass.md` | L82–87、L100–105 | `13a4b8c035e3c673` |
| vLLM `b17039bccc17b94a2ea107272ad7bc93508708df` · `int8.md` | L117–139 | `2d0c66123da0334c` |
| MindIE-LLM `69e5a5dd4b533eaffc7e198320435350825a36f7` · `faq.md` | L205–223 | `3c4f5db3c425f401` |
| 同快照 · `developer_guide/test.md` | 全文 3 行 | `de6ea3dae38eeffc` |
| 同快照 · ModelTest `README.md` | L236–283、L332–333 | `17f84a1f37c821d8` |
| 同快照 · ModelTest `README_NEW.md` | L178–184、L267–328 | `5ef09a37be30cd92` |

ModelTest 两份 README 与 `test.md` 经 GitHub 连接器按上述固定 commit 重取，逐字节等于初审原文件，重取文件暂存于 `/tmp/b27-t07-05-recheck-evidence/`。另直接打开 [PyTorch 2.6 数值精度说明](https://docs.pytorch.org/docs/2.6/notes/numerical_accuracy.html)及 [AWQ v6](https://arxiv.org/abs/2306.00978v6)、[GPTQ v2](https://arxiv.org/abs/2210.17323v2)、[SmoothQuant v7](https://arxiv.org/abs/2211.10438v7) 摘要页，只核对 C02/C03/C07 所涉表述；未扩读论文全文或 ModelTest 实现。

## C01–C07 逐项判定

### C01 · CLOSED · 固定身份与评估协议已补齐

**位置：**正文 L44–54、L95–99；来源记录 L51。

正文现要求不可变配置引用，明确固定任务 YAML 本身、few-shot 数量、答案抽取/filter、指标聚合、生成模式和 BOS。输入截断、总上下文上限、生成上限与停止条件分别列明；未核的采样透传行为与必须记录的有效值已经区分。

greedy/低温已归属本库方法，AISBench 的 0.6、OpenCompass 的 0.01 作为反例均与原文件一致。正文同时保留 AISBench [示例等于 35000、注释要求大于 35000](https://github.com/vllm-project/vllm-ascend/blob/52d4acfa51fb868823d1070b81cbd2d97e9e4696/docs/source/developer_guide/evaluation/using_ais_bench.md#L41-L45)的冲突及“多数数据集”的指南限定。没有补造有效运行参数，符合本项关闭条件。来源记录 L25 仍只写大于 35000，需随当前主张表同步清理；此处不另计发现，见 C07 的证据记录同步要求。

### C02 · OPEN（部分修复，保留 P2）· 来源主表仍未同步数学术语更正

**位置：**正文 L61；registry L6735；来源记录 L29、L52。

正文已用非结合性与运算重排的舍入影响解释差异，并把 FAQ 的错误术语作为来源用词加以说明；这与 [PyTorch 数值精度说明开篇](https://docs.pytorch.org/docs/2.6/notes/numerical_accuracy.html)一致。registry L6735 也已紧邻加注更正。shuffle-k 与约 10% 的代价仍归属文档声明，没有升级为本库测量。

**未满足的关闭条件：**来源记录 L29 的主张表仍把“浮点加法无交换律”直接并入根因叙述，支持范围仅写“FAQ 口径；数值未实测”，没有紧邻指出术语错误或引用更正依据。L52 虽追加了正确的修订说明，但没有同步更新主表或将旧表标为已被替代，尚不满足初审要求的“来源记录同步更正或加紧邻说明”。

**剩余动作：**直接修正 L29 的解释及来源归属，或在该行紧邻注明 FAQ 原文术语有误、正确解释及 PyTorch 依据；保留目前正文与 registry 的更正。无需再做数学机制扩写。

### C03 · CLOSED · 候选解释、指标能力与恢复结论已收敛

**位置：**正文 L58–74、L108、L121–122。

“合法/真缺陷”二分已撤回。采样、运算重排和 batch 差异现列为待检验解释；可接受性交给预注册容差和任务判据，排除后只进入进一步定位。此范围符合 [FAQ L205–223](https://github.com/Ascend/MindIE-LLM/blob/69e5a5dd4b533eaffc7e198320435350825a36f7/docs/zh/faq/faq.md#L205-L223)所能提供的机制线索。

四层表已区分能支持与不能支持的结论：数值比较须对齐输入与 token 历史，文本一致性不证明中间数值相同，固定 seed 不足以归因计算，kernel 分派另需执行路径证据。恢复行采用“支持因果假设”，并明确未恢复或仍有混杂时未决；继续链接既有证据判定纪律。C03 关闭；恢复结果如何关联实际基线运行，仍属 C05 的记录问题。

### C04 · OPEN（部分修复，保留 P2）· 样本／重复单位与未决规则仍不完整

**位置：**正文 L80–83、L106–108、L124；来源记录 L54。

已补主指标方向、绝对/相对差值口径、预选估计方法与置信口径、差值判定规则，并明确“不确定范围跨界＝未决”“未检出差异≠无差异”。三种结论范围也已列出，原先把点估计小于容差直接当成无差异的错误已修复。

**未满足的关闭条件：**

- L82 仅要求声明样本量和同配置重跑次数，未要求登记样本选择方式及重复单位；第一步的样本清单固定身份，不能替代第四步对抽样／推断范围和独立重复单位的声明。
- 没有把初审明确要求的“样本不足＝未决”写入判定规则。L81/L107/L124 只覆盖不确定范围跨界，仍缺无法形成有效不确定性估计、重复或有效样本不足时的停止判定。
- 方法举例是基线重复波动范围和二项比例标准误，尚未明确所选方法必须适用于**对照差值及比较结构**。官方 [lm-eval L128–131](https://github.com/vllm-project/vllm-ascend/blob/52d4acfa51fb868823d1070b81cbd2d97e9e4696/docs/source/developer_guide/evaluation/using_lm_eval.md#L128-L131)展示分任务/filter 的单个指标标准误，不能直接充当基线与变体差值的不确定性。

**剩余动作：**在预注册字段或其计划引用要求中补样本选择、重复单位，以及与比较结构匹配的差值不确定性方法；明确样本／重复不足、无法有效估计时未决。容差应注明是实际可接受变化的边界，统计可检出差异另行解释，不仅写成“多大差异算有变化”。无需本轮填具体样本量、统一置信阈值或选定所有任务通用的统计方法。

### C05 · OPEN（部分修复，保留 P2）· 结果关联、证据链与计数约束仍不闭合

**位置：**正文 L83、L89–108；来源记录 L55。

配置表已补 `exp_id/run_id`、`baseline_ref/prereg_ref`、变量有效值对、完整固定配置引用和实际执行路径证据；恢复也有判据与未决处置。提交数按声明口径可以承载质量分母，不要求另设一个重复字段；未运行数值继续留空是正确的。

**未满足的关闭条件：**

1. 结果表 L103–108 仍没有 `run_id` 等关联字段。标题“每 run 一行”和配置表中的运行标识说明了意图，但没有让导出的每条结果携带可连接的键；`baseline_ref` 只指基线实验，多个基线运行如何选取或聚合也需能沿引用定位。
2. 只有配置侧的执行路径日志/profiling 引用，没有实际输出、逐样本终态与重试记录或其受管证据引用，无法从原始状态重算分数与核对计数。
3. 新增固定等式“提交＝完成＋失败＋超时＋空输出”，同时仍允许预先决定“空输出是否计入失败”。若空输出已计入失败，再加空输出就重复计数；完成是否包括空输出、失败是否包括超时也没有互斥定义。仅写“关系预先声明”不足以保证这条固定等式成立。逻辑样本／请求尝试的二选一已允许预注册，但尚缺重试后如何归并终态与质量计分的规则或记录引用。

**剩余动作：**结果显式携带运行键并可追溯基线运行／聚合口径及预注册配置；补输出与逐样本状态／重试证据引用。将等式四类定义为互斥且穷尽的终态，或按包含关系改写等式；另定义失败率、质量计分与重试归并，使失败仍留在约定分母。恢复行沿用同一差值不确定性判据并链接比较结果，未恢复或混杂未排除继续未决。仍可使用 Markdown 表格，无需新建验证器或实际运行评估。

### C06 · OPEN（部分修复，保留 P2）· 入口补齐，但旧否定性说法仍在证据记录中生效

**位置：**正文 L61、L115、L130–132；registry L6735；来源记录 L31、L37、L56。

正文与 registry 已撤回存根外链说法并登记 ModelTest。重取的 [README L236–283](https://github.com/Ascend/MindIE-LLM/blob/69e5a5dd4b533eaffc7e198320435350825a36f7/examples/atb_models/tests/modeltest/README.md#L236-L283)、[L332–333](https://github.com/Ascend/MindIE-LLM/blob/69e5a5dd4b533eaffc7e198320435350825a36f7/examples/atb_models/tests/modeltest/README.md#L332-L333)及 [README_NEW L267–328](https://github.com/Ascend/MindIE-LLM/blob/69e5a5dd4b533eaffc7e198320435350825a36f7/examples/atb_models/tests/modeltest/README_NEW.md#L267-L328)支持相应入口描述；[L178–184](https://github.com/Ascend/MindIE-LLM/blob/69e5a5dd4b533eaffc7e198320435350825a36f7/examples/atb_models/tests/modeltest/README_NEW.md#L178-L184)支持精度测试默认设置的 README 级归属。新旧接口、实现判据、模型支持及 Server 端到端关系继续 unknown，未冒充服务实测证明。

**未满足的关闭条件：**来源记录 L31 仍写存根“指向外部设计指南”，L37 仍写 FAQ＋Qwen 对话测试是“仅有口径”并再次提及外部指南；两处均未在原位置撤回，且与 L56、正文和 registry 冲突。原始 [test.md 全文](https://github.com/Ascend/MindIE-LLM/blob/69e5a5dd4b533eaffc7e198320435350825a36f7/docs/zh/developer_guide/test.md)没有外链。此外，正文 L115 的“本快照 docs/ 内无官方精度评估专页”仍是整个目录的不存在判断，没有限定为实际读取／检索范围内未找到；本轮未新增支持该全称判断的检索范围证据。

**剩余动作：**同步改来源主表和 unknown 清单，登记 ModelTest 的准确入口／核对层级；将专页说法改为实际检索范围内未取得或未找到，或提供足以支撑明确范围结论的检索记录。保留当前实现与服务关系的 unknown 即可，不扩写使用指南。

### C07 · OPEN（部分修复，保留 P3）· 正文已改，来源主表仍保留旧锚点与归属

**位置：**正文 L62、L74、L114、L116；来源记录 L22、L25–29、L57。

正文 FAQ 调度锚点、lm-eval 命令和时间说明、OpenCompass HUMAN/BOT＋保留 SYSTEM 均已改正。未量化 baseline 已归本库方法；AWQ v6、GPTQ v2、SmoothQuant v7 的版本化链接已贴近论文质量句，摘要支持范围与作者报告／未复现边界保留。本轮打开三篇摘要未见因修订引入共同无损保证。

**未满足的关闭条件：**来源记录主张表仍有下列旧值，追加 L57 没有替换当前表：

| 来源记录位置 | 仍保留的内容 | 按原文件应修正为 |
|---|---|---|
| L22 | 命令 L107–116、30 分钟 L117 | 命令 [L116–120](https://github.com/vllm-project/vllm-ascend/blob/52d4acfa51fb868823d1070b81cbd2d97e9e4696/docs/source/developer_guide/evaluation/using_lm_eval.md#L116-L120)，时间 L123；安装可另定位 |
| L25 | 只保留 max_model_len 大于 35000 的要求 | 与正文一致注明 [L41–45](https://github.com/vllm-project/vllm-ascend/blob/52d4acfa51fb868823d1070b81cbd2d97e9e4696/docs/source/developer_guide/evaluation/using_ais_bench.md#L41-L45)示例／注释冲突及指南限定（关联 C01，不新增计数） |
| L26 | SYSTEM/USER/BOT | [L82–87](https://github.com/vllm-project/vllm-ascend/blob/52d4acfa51fb868823d1070b81cbd2d97e9e4696/docs/source/developer_guide/evaluation/using_opencompass.md#L82-L87)是 HUMAN/BOT，保留角色 SYSTEM |
| L27 | 未量化 baseline 与量化第四步并列归属“官方流程” | [INT8 L117–139](https://github.com/vllm-project/vllm/blob/b17039bccc17b94a2ea107272ad7bc93508708df/docs/features/quantization/int8.md#L117-L139)只给量化侧评测；未量化 baseline 对照单列为本库方法 |
| L29 | Server 调度 L224–226 | [FAQ L221–223](https://github.com/Ascend/MindIE-LLM/blob/69e5a5dd4b533eaffc7e198320435350825a36f7/docs/zh/faq/faq.md#L221-L223)；原范围是空行及下一条标题 |

**剩余动作：**直接同步上述主表，或明确隔离为已失效的历史版本并提供完整、权威的现行映射。只追加“已更正”的修订清单不能使旧表自动准确。无需重开 T07-04 历史审阅。

## 新问题

没有新增独立发现 ID。新增计数等式与允许空输出包含于失败的冲突，是修订中出现的具体问题，已归入 C05 的原关闭条件，不重复计数。其余未关闭项为初审残留或证据记录未同步。

附带核对 T07-07-C09：正文 L110 已有指向 [PD 分离](../../knowledge/07-inference/pd-disaggregation.md)的普通本地链接，目标文件存在，返回入口补齐；这里只确认该附带修订，没有重做 T07-07 复核或更改其报告。

## 整体结论

**本轮定向复核未通过。C01、C03 关闭；C02、C04、C05、C06、C07 保持开放。** 正文的主要概念边界已有改善，但来源记录的主表／unknown 清单尚未同步，统计预注册与结果审计仍缺部分明确条件。下一轮只需复核上述剩余动作及相关回归，无须重做整篇初审。

`make check` 通过（112 content entries / 542 sources）；`make build` 在含本报告的临时源码副本通过，生成产物仅写入临时副本。临时副本第一次构建因未复制被既有文档链接的 `build/catalog.json` 与 `build/catalog.md` 而失败；补入工作区已有两份产物后重建通过，此失败来自副本准备，不是本轮正文或报告的结构问题。`git diff --check`、新增报告的 diff 空白检查与尾随空白检查通过。对读取阶段记录的 577 个既有文件比较 SHA-256，没有改动；本会话只新增本报告。检查期间工作区另出现 `docs/research/batch-27-t07-07-codex-recheck.md`，本会话未写入该文件，不属于本轮编辑。未修改 `src/kb/`，未运行工具代码测试。

本报告不改变正文的 `draft / source_checked` 状态；结构检查与模型审阅均不构成技术执行成功、平台兼容性或真实硬件验证。

C01–C07：CLOSED 2、OPEN 5（部分修复 5）；开放优先级：P1 0、P2 4、P3 1；新增独立发现 0；整体：未通过，需按剩余关闭条件修订后定向复核。
