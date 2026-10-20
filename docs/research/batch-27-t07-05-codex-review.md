# Batch 27 · T07-05 新建交付初审

## 会话元数据

| 项目 | 实际记录 |
|---|---|
| 角色 | AI 可靠性知识库批次审阅者；T07-05 新建 procedure 初审 |
| 实际执行模型 | `gpt-6.1-sol` |
| 实际推理档位 | `xhigh` |
| 核验依据 | 本地 CLI rollout 的 `turn_context.model/effort` 与 `session_meta.cwd`；会话 ID 与环境变量 `CODEX_THREAD_ID` 一致。所查模型/档位字段只有上述一组，未见模型回退标记；没有按用户要求值反填 |
| 会话 ID | `01a15b23-445e-7190-9fff-29d1defc7339` |
| 运行记录 | `/Users/ywang2397/.codex/sessions/2026/10/21/rollout-2026-10-21T05-06-40-01a15b23-445e-7190-9fff-29d1defc7339.jsonl`；provider=`custom`，CLI=`0.163.0`，source=`exec` |
| cwd | `/Users/ywang2397/work/AI_reliability_knowledge_base` |
| 日期与时区 | 2026-10-21，Asia/Shanghai（UTC+08:00）；会话启动于当地 05:06:40 |
| 审阅基点 | Git HEAD `f1253eeb22086e1837096b0f42bc8d20ff301677` 加工作区未提交内容；下列行号均为原文件坐标 |
| 正文 | [output-quality-evaluation.md](../../knowledge/07-inference/output-quality-evaluation.md)，128 行；SHA-256 `410df4738ff97ec2115ee02ebc1c740e27fff11baec85103053628b086f0cab1` |
| 来源基线 | [batch-27-t07-05-sources.md](batch-27-t07-05-sources.md)，47 行；SHA-256 `566aa23de6033c93a0dd3dd72a2fcb97ac960ca22b51bd18bc393e106aa248f8` |
| 来源登记 | [registry.yaml](../../sources/registry.yaml)，6788 行；SHA-256 `a3310fbc0c68d6efa8f39e6000bb10f4bcad39bceae9cf5f425d2eb5ec724186` |
| 执行范围 | 本会话直接审阅，未调用其他模型或子代理；未安装评估工具，未运行推理、评估或硬件实验；仓库仅新增本报告 |

## 范围与方法

先读取 README、写作指南、AGENTS.md 与内容分工，按[任务清单](../../plans/full-coverage-backlog.yaml) L6406–6426 的 T07-05 五项 acceptance 验收。正文与来源记录逐行核对，另读 registry 对应条目、[T07-04 量化页](../../knowledge/07-inference/quantization-and-quality.md)、[权重加载页](../../knowledge/07-inference/model-loading-and-readiness.md)、[精度差异诊断](../../knowledge/06-training/gpu-npu-precision-difference-triage.md)，检查主归属、引用和边界。

从 `/tmp/b27-fetch/` 读取原文件，并经 GitHub 连接器按固定 commit 重取以下八份文件。重取内容逐字节等于缓存；已有七份哈希前缀与来源记录一致，NIXL 哈希本轮补记。网页工具的显示行号未用于 GitHub 行号锚点。

| 固定快照／缓存文件 | SHA-256 |
|---|---|
| vLLM Ascend `52d4acfa51fb868823d1070b81cbd2d97e9e4696` · `va-using_lm_eval.md` | `29da7eb7d0c595e316526830f3081a875a3487b9b745da93036e7cf66faff6db` |
| 同快照 · `va-using_evalscope.md` | `8e8eaf625027a233f12c41a9667fbfddf83b4c6bd65858aa16212f33d55403fe` |
| 同快照 · `va-using_ais_bench.md` | `19c3087e40c30cb5d7cbecf10ff3f6553c31598bb1b624c1c3763c18483f3d99` |
| 同快照 · `va-using_opencompass.md` | `13a4b8c035e3c6734516df1983f7421e20901936788c5d74de7eb1e8bf653d93` |
| vLLM `b17039bccc17b94a2ea107272ad7bc93508708df` · `vl-quant-int8.md` | `2d0c66123da0334c53e4d860c79efd19072bfbfd5bed3a0afdbfa609534b904e` |
| 同快照 · `vl-nixl_usage.md` | `675eb4152d4151409b63f265d493d55938af77b357f1d778475d78e1d78125b2` |
| MindIE-LLM `69e5a5dd4b533eaffc7e198320435350825a36f7` · `mi-faq.md` | `3c4f5db3c425f4010fd02513971125cd8221995d4491fb6615e2eba78952b0e7` |
| 同快照 · `mi-dev-test.md` | `de6ea3dae38eeffc3848eb51d3e9390de4ba6ab83c6657f9e54ef0978a327698` |

为核验 MindIE 的否定性表述，额外读取同一 commit 的递归文件树（4346 项，`truncated=false`）及 ModelTest 材料。补充原文件暂存于 `/tmp/b27-t07-05-review-evidence/`，只把定位、原创判断与哈希写入本报告；未改 registry。

| 同一 MindIE 快照内的补充文件 | SHA-256 |
|---|---|
| `examples/atb_models/tests/modeltest/README.md`（377 行） | `17f84a1f37c821d8bb3bc339a249a70fd2906711d8bc9eb49b3663ab028fb4b1` |
| `examples/atb_models/tests/modeltest/README_NEW.md`（609 行） | `5ef09a37be30cd92674558094713950290cd1c44d674a0976c80e10016fff35a` |
| `examples/atb_models/tests/modeltest/docs/user_guides/data_preparation.md`（38 行） | `087ae45c0931adeb0002356aada545badc56a39ff02bc4c6cc95f97e7f126bf1` |

另在线核对已登记的 [PyTorch 2.6 数值精度说明](https://docs.pytorch.org/docs/2.6/notes/numerical_accuracy.html)，以及 [AWQ v6](https://arxiv.org/abs/2306.00978v6)、[GPTQ v2](https://arxiv.org/abs/2210.17323v2)、[SmoothQuant v7](https://arxiv.org/abs/2211.10438v7) 的摘要；未读论文全文，不补推实验设置。以下明确区分**来源原文**、**本库方法／审阅归纳**与**待核实**。P1 为严重错误，P2 为影响方法、验收或证据结论的实质问题，P3 为定位与引用问题；全部发现均为 OPEN。

## 发现清单

### C01 · P2 · 固定清单缺少上下文预算与评估协议的具体身份

**位置：**正文 L44–52、L95；关联来源记录 L20–24。

**陈述：**六个必需类别已经列出，模型/tokenizer 还可沿加载页取得不可变身份；但“输出长度”行只列 max tokens／停止条件，却以服务端 `max_model_len` 作依据，没有分别固定输入截断、总上下文预算与生成上限。测试集行仅举任务 YAML 的数据字段，未要求冻结实际任务 YAML、few-shot 数量、答案抽取/filter、指标聚合等评估协议；同一测试集因此仍可能得出不可比的分数。BOS 处理与实际生成模式也未进入清单。“评估通常 temperature=0”应标为方法选择，不能从单次 curl 样例推出工具评测的有效参数。

**上游证据：**[AISBench L153–194](https://github.com/vllm-project/vllm-ascend/blob/52d4acfa51fb868823d1070b81cbd2d97e9e4696/docs/source/developer_guide/evaluation/using_ais_bench.md#L153-L194)明确区分 `max_out_len` 与输入长度之和、服务端上下文上限，并给出采样参数、后处理和重试；[lm-eval YAML L230–275](https://github.com/vllm-project/vllm-ascend/blob/52d4acfa51fb868823d1070b81cbd2d97e9e4696/docs/source/developer_guide/evaluation/using_lm_eval.md#L230-L275)同时包含 target、metric、generation、few-shot 和 filter；[INT8 L130–139](https://github.com/vllm-project/vllm/blob/b17039bccc17b94a2ea107272ad7bc93508708df/docs/features/quantization/int8.md#L130-L139)特别提醒 `add_bos_token` 的精度影响。AISBench 样板用 temperature=0.6，OpenCompass [L101–105](https://github.com/vllm-project/vllm-ascend/blob/52d4acfa51fb868823d1070b81cbd2d97e9e4696/docs/source/developer_guide/evaluation/using_opencompass.md#L101-L105)用 0.01，不能把 temperature=0 写成这些指南的共同要求。

**关闭条件：**以字段或不可变配置引用补齐上述身份，区分“必须固定的有效值”与“尚未核验的参数透传”。单列上下文／截断／输出限制，并说明 [AISBench L41–45](https://github.com/vllm-project/vllm-ascend/blob/52d4acfa51fb868823d1070b81cbd2d97e9e4696/docs/source/developer_guide/evaluation/using_ais_bench.md#L41-L45)自身存在“示例等于 35000、注释要求大于 35000”的不一致；保留其指南限定，不把它当跨模型、跨任务阈值。本项是审阅者对可比性要求的归纳，不要求填入未运行参数或另写完整 tokenizer 教程。

### C02 · P2 · 将 FAQ 中错误的数学术语直接写成技术结论

**位置：**正文 L59；来源记录 L29；registry L6735 的 MindIE notes。

**陈述：**“浮点加法无交换律”确实来自 FAQ，因而不是误译；但将它无保留地作为累加顺序误差的原理仍不正确。这里应解释有限精度加法的非结合性与运算重排的舍入影响，并明确上游术语问题。来源一致性不能替代技术正确性。

**上游证据：**MindIE [FAQ L214–219](https://github.com/Ascend/MindIE-LLM/blob/69e5a5dd4b533eaffc7e198320435350825a36f7/docs/zh/faq/faq.md#L214-L219)原文确用“加法交换律”；已登记的 [PyTorch 2.6 Numerical accuracy](https://docs.pytorch.org/docs/2.6/notes/numerical_accuracy.html)开头则明确说明加法／乘法的非结合性，后续 batched computation 节说明数学等价的计算可能不逐位一致。

**关闭条件：**正文采用正确解释，保留“FAQ 原文如此、本文据数值精度说明更正”的归属；来源记录和 registry notes 同步更正或加紧邻说明。仍可引用该 FAQ 证明 shuffle-k 开关和约 10% 的文档性能代价，但不得把这个代价当成本库测量或全系统吞吐损失。

### C03 · P2 · 差异分层与指标表的结论强于证据

**位置：**正文 L59–61、L67–68、L107，关联 L118–119。

**陈述：**FAQ 支持的是候选非确定性机制，不是“合法／真缺陷”的二分判定。未核容差与任务影响就称累加差异“合法”，以及排除三种机制后使用“真计算缺陷”，都会把尚待定位的差异提前定性。确定输入的输出文本只能观察行为一致性；相同文本不能证明 logits／中间数值相同，不同文本也不能仅凭固定 seed 归因到计算。数值不同同样不能单独证明 kernel 分派路径改变。L107 的恢复对照可增强变量相关的因果假设，不能无条件“验证差异确由该变量引起”。

**上游证据：**MindIE [L205–223](https://github.com/Ascend/MindIE-LLM/blob/69e5a5dd4b533eaffc7e198320435350825a36f7/docs/zh/faq/faq.md#L205-L223)只定义重复一致性、给出 greedy 可基本稳定及两类 batch 原因，没有宣告这些差异均可接受，也没有穷尽所有原因。[PyTorch 数值说明](https://docs.pytorch.org/docs/2.6/notes/numerical_accuracy.html)不保证数学等价计算跨平台逐位相同。本库既有[精度诊断](../../knowledge/06-training/gpu-npu-precision-difference-triage.md) L89–115 要求有依据的容差、任务影响和支持／反证，并保留 unknown。

**关闭条件：**将这些机制写为待检验解释，把“可接受”交给预注册容差和任务判据；排除后进入进一步定位，不直接判缺陷。四层表明确文本一致性、对齐输入／token 历史下的数值比较、实际执行路径取证各自的能力边界。恢复段改为条件性支持，说明恢复后未回到基线或仍有混杂时的未决结论。继续引用既有诊断纪律，无须复制训练侧定位流程。

### C04 · P2 · 预注册提到了不确定性，但缺少据此作结论的规则

**位置：**正文 L76–81、L102–104。

**陈述：**主指标、容差、样本量／重复、失败处理四项均有文字；缺口是只说重复用于估计波动，结果填“置信/波动”，没有要求事先选择估计方法、置信口径及差值的判断规则。L79 又把“低于容差”直接写成“无差异”，会使点估计落入容差但不确定范围跨界的结果被判定通过。实际可接受幅度与统计可检出差异也不应混称。

**上游证据：**T07-05 acceptance 3（任务清单 L6424）明确要求预先确定统计不确定性；[lm-eval L128–131](https://github.com/vllm-project/vllm-ascend/blob/52d4acfa51fb868823d1070b81cbd2d97e9e4696/docs/source/developer_guide/evaluation/using_lm_eval.md#L128-L131)展示的是分任务、分 filter 的指标和标准误，不能当作任意对照差值已具备置信结论。[EvalScope L71–87](https://github.com/vllm-project/vllm-ascend/blob/52d4acfa51fb868823d1070b81cbd2d97e9e4696/docs/source/developer_guide/evaluation/using_evalscope.md#L71-L87)的 10 样本演示也不提供这种保证。此项判断是验收与统计推理层面的审阅归纳，不是声称厂商给了通用统计处方。

**关闭条件：**预注册指标方向／差值口径、容差含义、样本选择与重复单位、适合比较对象的不确定性方法和判定规则；明确“不确定范围跨界／样本不足＝未决”，不把未检出差异等同无差异。区分固定测试集的观察结论、对新样本的推断及运行重复波动；可引用计划文件承载，不要求捏造样本量或统一置信阈值。

### C05 · P2 · 两个 schema 尚不足以关联和核验一次完整对照

**位置：**正文 L87–107；关联 L78–81。

**陈述：**配置表有 exp_id，结果表却没有关联实验／配置／基线的键；两表均不能定位重复运行和预注册计划。配置仅记录引擎版本、模型身份和一个“变量”概述，缺少环境／数值／并行／batch 控制条件的可追溯引用及变量前后有效值，无法核验“其余不变”。结果只有四种计数，没有定义空输出与完成／失败的重叠关系、超时归属和重试口径，也没有明确的质量分母字段；因此正文的分母纪律尚不能由记录审计。恢复是否回到基线也缺记录与完成判据。

**上游证据：**任务 acceptance 3–4（L6424–6425）要求失败不丢失、可复用的配置／结果 schema；官方 AISBench [L158–194](https://github.com/vllm-project/vllm-ascend/blob/52d4acfa51fb868823d1070b81cbd2d97e9e4696/docs/source/developer_guide/evaluation/using_ais_bench.md#L158-L194)含 batch、请求速率、retry、生成及后处理，OpenCompass [L100–105](https://github.com/vllm-project/vllm-ascend/blob/52d4acfa51fb868823d1070b81cbd2d97e9e4696/docs/source/developer_guide/evaluation/using_opencompass.md#L100-L105)也含 batch／retry。不能只记录工具名就假定这些条件相同。具体 schema 最小字段属于本库设计建议，不是上游现成格式。

**关闭条件：**补入实验／运行／基线关联、预注册与完整固定配置的引用、唯一变量的有效值和执行路径证据位置；关联实际输出／逐样本状态或其受管证据。定义质量分母、失败／超时／空输出计数关系及重试是逻辑样本还是请求尝试，给出能核对总提交数的约束；失败仍保留在约定分母。记录恢复与基线的比较及未恢复时的处置。表格形式可以保留，无须另建机器验证器；计划值与运行值分开，未运行数值继续空置。

### C06 · P2 · MindIE unknown 混入了不存在的外链，并遗漏同快照评估材料

**位置：**正文 L112、L128；来源记录 L31、L37；registry L6735。

**陈述：**`developer_guide/test.md` 确为三行存根，但只有标题和一句内容简介，没有 URL、Markdown 链接或“请见外部指南”的指向。“存根指向外部设计指南”无原文依据。更重要的是，“可用口径是 FAQ 与 Qwen 对话样板”遗漏同快照官方仓库内的 ModelTest 精度测试材料。未取得独立评估专页可以是检索范围限制，不能据此把未读材料写成不存在或仅有两种证据。

**上游证据：**[test.md 全文](https://github.com/Ascend/MindIE-LLM/blob/69e5a5dd4b533eaffc7e198320435350825a36f7/docs/zh/developer_guide/test.md)无外链；同 commit 的 [ModelTest README L236–283](https://github.com/Ascend/MindIE-LLM/blob/69e5a5dd4b533eaffc7e198320435350825a36f7/examples/atb_models/tests/modeltest/README.md#L236-L283)有下游数据集精度测试和限制，[L332–333](https://github.com/Ascend/MindIE-LLM/blob/69e5a5dd4b533eaffc7e198320435350825a36f7/examples/atb_models/tests/modeltest/README.md#L332-L333)给出 GSM8K 示例。新版 [README_NEW L267–328](https://github.com/Ascend/MindIE-LLM/blob/69e5a5dd4b533eaffc7e198320435350825a36f7/examples/atb_models/tests/modeltest/README_NEW.md#L267-L328)给出任务 YAML、指标／截断字段和 `modeltest` 命令；[L178–184](https://github.com/Ascend/MindIE-LLM/blob/69e5a5dd4b533eaffc7e198320435350825a36f7/examples/atb_models/tests/modeltest/README_NEW.md#L178-L184)还将该 shuffle-k 开关列为 NPU 精度测试场景的默认设置。这些是本轮补充读取的官方仓库材料，不是本库运行结果。

**关闭条件：**撤回外链说法；将专页表述限定到实际读取／检索范围，登记或链接 ModelTest 入口并同步来源记录、registry notes。可只把新入口列为后续核验，毋须在本轮扩成完整使用指南。保留 ModelTest 新旧接口、脚本实现／判据、模型支持和与 MindIE Server 端到端服务评估关系的 unknown；不把模型侧测试材料提升为服务模式兼容或实测证明。“不是常规部署建议”可保留，但不能因此忽略其在官方精度测试样板中的用途。

### C07 · P3 · 精确锚点、来源摘要和论文近邻引用需修正

**位置：**正文 L60、L113；来源记录 L20、L24、L27、L29。

**陈述与上游证据：**

- 正文 Server 调度段链接 `faq.md#L224-L226`，该范围已经是空行及“异步执行出现定位困难的报错”标题；实际支持段为 [L221–223](https://github.com/Ascend/MindIE-LLM/blob/69e5a5dd4b533eaffc7e198320435350825a36f7/docs/zh/faq/faq.md#L221-L223)。来源记录重复了相同偏移。
- 来源记录将 lm-eval 在线安装／命令归至 L107–116、30 分钟说明归至 L117；原文件命令实际在 [L116–120](https://github.com/vllm-project/vllm-ascend/blob/52d4acfa51fb868823d1070b81cbd2d97e9e4696/docs/source/developer_guide/evaluation/using_lm_eval.md#L116-L120)，时间说明在 L123。OpenCompass 来源摘要写 SYSTEM/USER/BOT，但原配置 [L82–87](https://github.com/vllm-project/vllm-ascend/blob/52d4acfa51fb868823d1070b81cbd2d97e9e4696/docs/source/developer_guide/evaluation/using_opencompass.md#L82-L87)使用 HUMAN/BOT 与保留 SYSTEM。
- 来源记录把“baseline 为未量化模型同任务结果”与 INT8 第四步一并归为官方流程；[L117–139](https://github.com/vllm-project/vllm/blob/b17039bccc17b94a2ea107272ad7bc93508708df/docs/features/quantization/int8.md#L117-L139)提供量化模型评测及 BOS 提醒，没有未量化 baseline 命令或该定义。基线对照合理，但应归为本库方法。
- 正文 L113 对三论文作作者报告归属是正确的，但没有贴近该句的论文链接，正文来源节也未补出；source_refs 不能替代近邻证据。应指向本轮实际读取的版本摘要，并保留 AWQ 的量化误差／基准表现、GPTQ 与 SmoothQuant 的精度声明各自范围，不笼统提升为共同的无损保证。

**关闭条件：**按固定 commit 原文件更正上述坐标与摘要、分开官方示例和本库基线建议，补齐论文版本链接。无需追改历史 T07-04 审阅结论；本项只要求修正 T07-05 当前正文及其证据链。

## acceptance 逐条判定

| 项 | 判定 | 已覆盖的依据 | 尚缺／关联发现 |
|---|---|---|---|
| 1．固定模型/tokenizer/模板/测试集/采样/长度；区分采样与计算 | **部分满足，未通过** | L48–52 六类齐全，加载页 L117–129 可提供模型与 tokenizer 制品身份；FAQ sampling→greedy、累加顺序、Server 组 batch 三段均有原文；开关限定 MindIE，性能代价未冒充实测 | 有效评估协议、上下文预算不完整；数学术语、接受性／缺陷归因、调度锚点需修订：C01–C03、C07 |
| 2．四层指标与适用边界；无跨任务阈值 | **部分满足，未通过** | L65–70 明列 logits/数值、确定输入输出、任务、安全/业务四层；L69、L122 明确不给跨任务合格阈值，未用吞吐/时延替代输出质量 | 四层名称清晰，但文本／数值观察能够支持的结论仍越界：C03 |
| 3．预注册主指标、容差、样本量/重复与不确定性；失败保留分母 | **部分满足，未通过** | L78–81 有四项设计；L81、L120 明确全部提交为分母、失败率并报；正确把 EvalScope 的 10 样本定位为演示 | 差值不确定性的预注册与未决规则不足；空输出、重试与结果计数仍无法审计：C04–C05 |
| 4．基线→单变量→恢复的配置/结果 schema；无未运行测量 | **部分满足，未通过** | L87–107 已给两张字段表、三阶段结构及量化/kernel/图路径变体；“填写”“引用”与实验标签明确是设计占位，没有伪造观测值 | schema 关联、有效配置、分母约束和恢复判据不足，且恢复因果措辞过强：C03、C05。占位本身不列为缺陷 |
| 5．至少一个官方评估例或原始研究质量案例；区分作者报告与本库复现，连接精确指南 | **最低要求满足；附属证据表述待修订** | L72、L111、L126 有固定 commit 的官方流程和四指南，L113 明确论文仅作者报告、摘要级、本库未复现；以下命令级核对支持这些例证的存在性 | MindIE 材料范围与存根描述不准确，部分来源定位／归属需更正：C06–C07；本项最低要求满足不抵销开放问题 |

官方例证的命令级核对结果如下。这里只确认指南提供了这些路径，没有执行，也没有认定各工具的默认行为相同：

| 例证 | 原文件支持位置与结论 | 不据此认定 |
|---|---|---|
| lm-eval | [在线 L105–131](https://github.com/vllm-project/vllm-ascend/blob/52d4acfa51fb868823d1070b81cbd2d97e9e4696/docs/source/developer_guide/evaluation/using_lm_eval.md#L105-L131)：安装 `[api]`，`local-completions` 连接 `/v1/completions` 跑 gsm8k；[离线 L169–184](https://github.com/vllm-project/vllm-ascend/blob/52d4acfa51fb868823d1070b81cbd2d97e9e4696/docs/source/developer_guide/evaluation/using_lm_eval.md#L169-L184)：`--model vllm`、`--batch_size auto`；另有离线数据集 YAML | curl 的 temperature=0 不是后续评测默认值证据；两组官方演示结果不是本库对照 |
| EvalScope | [L56–90](https://github.com/vllm-project/vllm-ascend/blob/52d4acfa51fb868823d1070b81cbd2d97e9e4696/docs/source/developer_guide/evaluation/using_evalscope.md#L56-L90)：独立 venv，`evalscope eval --eval-type server --datasets gsm8k --limit 10`；[L92–113](https://github.com/vllm-project/vllm-ascend/blob/52d4acfa51fb868823d1070b81cbd2d97e9e4696/docs/source/developer_guide/evaluation/using_evalscope.md#L92-L113)为独立 perf 模式 | perf 压测不能代替质量评估；10 样本不能默认成为验收设计 |
| AISBench | [L153–211](https://github.com/vllm-project/vllm-ascend/blob/52d4acfa51fb868823d1070b81cbd2d97e9e4696/docs/source/developer_guide/evaluation/using_ais_bench.md#L153-L211)：服务配置，`ais_bench --models vllm_api_general_chat --datasets … --mode all --dump-eval-details --merge-ds` | gitee 框架实现、采样透传、失败计分和 >35000 的普遍适用性仍未证实 |
| OpenCompass | [L70–113](https://github.com/vllm-project/vllm-ascend/blob/52d4acfa51fb868823d1070b81cbd2d97e9e4696/docs/source/developer_guide/evaluation/using_opencompass.md#L70-L113)：OpenAISDK 配置接服务，`python3 run.py opencompass/configs/eval_vllm_ascend_demo.py --debug` | 角色配置、长度、温度、batch 与 retry 不能隐含视为与其他工具相同 |
| vLLM INT8 第四步 | [L117–139](https://github.com/vllm-project/vllm/blob/b17039bccc17b94a2ea107272ad7bc93508708df/docs/features/quantization/int8.md#L117-L139)：`lm_eval --model vllm` 跑量化产物、gsm8k、5-shot、limit 250，并提醒 BOS | 未提供通用合格阈值，也未执行本库 baseline/recover |
| NIXL accuracy | [L177–183](https://github.com/vllm-project/vllm/blob/b17039bccc17b94a2ea107272ad7bc93508708df/docs/features/nixl_connector_usage.md#L177-L183)：列出 `run_accuracy_test.sh`、`toy_proxy_server.py`、`test_accuracy.py` | 仅入口得到核对；脚本容差、比较对象、输出等价性判据均未读，不宣称其证明 PD 质量等价 |

其余重点维度的判定：

- **元数据与本地引用通过结构核对。** procedure 必需的 applicability/verification 均存在；`draft / source_checked` 与未运行说明分开；`environment_refs: []` 明确无环境档案。6 个 related_ids、6 个 source_refs 及本地链接均可解析；多平台标签没有伴随已验证兼容性声明。`source_checked` 是作者记录的来源核对状态，不等于本轮审阅通过。
- **内容归属和主体边界通过。** 本页主归属是 07.4 的评估设计与记录，没有重写 T07-04 的机制／支持矩阵，也没有复制训练侧首差异诊断流程。共享 INT8 和四指南是短篇证据衔接；C03 所需的判定纪律继续链接既有正文即可。没有因本次邻页阅读而重开 T07-04 历史发现。
- **无未运行测量通过。** 正文未填实测分数、置信区间或成功次数；30 分钟、10% 与工具样例参数均可追溯到上游材料。论文质量文字已明确归属作者，缺少本地复现和全文设置仍保留。框架版本／采样透传、logprobs 接口、NIXL 内部判据保持 unknown 是恰当的；MindIE 的检索结论须按 C06 改写。

## 整体结论

**T07-05 本轮初审未通过，需修订后定向复核。** 已有六类输入清单、四层指标、预注册框架、两张 schema 和充足的官方指南入口；阻断通过的是可比性细节、数值／因果结论边界、统计判定与记录可审计性，以及 MindIE 证据范围的错误表述。7 项发现均开放（6 P2、1 P3），未发现 P1。acceptance 5 的最低例证要求已满足，其余四项为部分满足。

`make check` 通过（112 content entries / 542 sources）；`make build` 在包含本报告的临时源码副本通过，生成产物只写入临时副本，未改工作区 `build/`。`git diff --check` 与报告尾随空白检查通过。对读取阶段记录的 574 个既有文件比较 SHA-256，未发现改动；本会话仅新增本报告。核对期间另有并行会话新增 `batch-27-t07-07-codex-review.md`，不属于本轮编辑。未修改 `src/kb/`，未运行工具代码测试。

上述检查只验证结构和本地引用，不确认技术结论、远程内容或硬件结果。本报告不改变正文状态、任务状态和既有审阅记录；关闭发现需要作者修订正文及相关证据记录，再按上述关闭条件复核。

C01–C07：OPEN 7、CLOSED 0；P1 0、P2 6、P3 1；acceptance：满足最低要求 1、部分满足 4、未覆盖 0；整体：需修订后定向复核。
