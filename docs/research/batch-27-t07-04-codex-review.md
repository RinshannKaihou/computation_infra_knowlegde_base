# Batch 27 · T07-04 修订交付初审

## 会话元数据

| 项目 | 实际记录 |
|---|---|
| 角色 | AI 可靠性知识库批次审阅者；本轮为修订交付初审，不是问题关闭复核 |
| 实际执行模型 | `gpt-6.1-sol` |
| 实际推理档位 | `xhigh` |
| 元数据依据 | 本次 Codex 会话 JSONL 的 `turn_context.model`、`turn_context.effort`；工作目录同时见 `session_meta.cwd`。不是从审阅提示词反填 |
| 会话 ID | `01a15aeb-1945-7a21-ac56-169d65cc4589` |
| 运行记录 | `/Users/ywang2397/.codex/sessions/2026/10/21/rollout-2026-10-21T04-05-19-01a15aeb-1945-7a21-ac56-169d65cc4589.jsonl`；记录的 provider 为 `custom`，CLI 为 `0.163.0` |
| 工作目录 | `/Users/ywang2397/work/AI_reliability_knowledge_base` |
| 日期与时区 | 2026-10-21，Asia/Shanghai（UTC+08:00）；会话启动时间为当地 04:05:19 |
| 审阅基点 | Git HEAD `d5bef70a40e2210c223467de17c035829179cd05` 加工作区未提交正文；不是只审 HEAD 中的旧稿 |
| 正文指纹 | SHA-256 `4866c5ab03dbad230927898d13cdb6245ad657d07eb0b5ddf865bb1865625628` |
| 执行范围 | 本会话直接审阅，未调用其他审阅模型或子代理；未运行量化、推理、硬件测试或模型质量评估 |

## 审阅范围与方法

审阅主对象为 [quantization-and-quality.md](../../knowledge/07-inference/quantization-and-quality.md)，下文正文行号均对应上述指纹的 157 行工作区版本。验收依据为 [full-coverage-backlog.yaml](../../plans/full-coverage-backlog.yaml) L6357–6377 的 T07-04，`operation: revise`。读取了 README、AGENTS、写作指南、主题归属表、元数据 schema、[作者来源记录](batch-27-t07-04-sources.md)，并核对正文七项 `source_refs` 对应的 [registry](../../sources/registry.yaml) 条目。相邻布局正文仅用于确认本地链接及其明确承接的冲突，未对 T07-06 作全面审阅。

取证以固定 commit 原文件为准：vLLM `b17039bccc17b94a2ea107272ad7bc93508708df`、vLLM Ascend `52d4acfa51fb868823d1070b81cbd2d97e9e4696`、MindIE-LLM `69e5a5dd4b533eaffc7e198320435350825a36f7`。对来源记录列出的 **29 份** `/tmp/b27-fetch/` 文件重新计算 SHA-256，前 16 位与记录全部一致；文件行数也全部一致。随后按原文件空行和换行核对技术主张，不采用网页渲染行号。

独立网络取证如下。GitHub raw 的一次网页抓取返回 cache miss，随后通过 GitHub 连接器读取相同的固定 commit raw URL，取得原文件内容；没有把抓取失败记为已核实。

| 独立重取对象 | 原文件坐标/目的 | 重取 SHA-256 前 16 位 | 与作者缓存比较 |
|---|---|---|---|
| [vLLM fp8.py](https://raw.githubusercontent.com/vllm-project/vllm/b17039bccc17b94a2ea107272ad7bc93508708df/vllm/model_executor/layers/quantization/fp8.py) | L307–353、L896–911；kernel 条件与 MoE 限制 | `bc1d30059e0f3123` | 全文件字节一致 |
| [vLLM gptq.py](https://raw.githubusercontent.com/vllm-project/vllm/b17039bccc17b94a2ea107272ad7bc93508708df/vllm/model_executor/layers/quantization/gptq.py) | L91–101、L129–140、L379–390；警告与执行路径 | `66eb332cc2f83a0e` | 全文件字节一致 |
| [vLLM config/model.py](https://raw.githubusercontent.com/vllm-project/vllm/b17039bccc17b94a2ea107272ad7bc93508708df/vllm/config/model.py) | L867–948；override 与未知方法校验 | `bb8a629254b756f0` | 全文件字节一致 |
| [MindIE fa3_quantization.md](https://raw.githubusercontent.com/Ascend/MindIE-LLM/69e5a5dd4b533eaffc7e198320435350825a36f7/docs/zh/user_guide/feature/fa3_quantization.md) | L5–13、L59–72、L86–122；量化对象与 NZ 前提 | `3b035f3b369e8ada` | 全文件字节一致 |
| [MindIE optimization_and_tuning.md](https://raw.githubusercontent.com/Ascend/MindIE-LLM/69e5a5dd4b533eaffc7e198320435350825a36f7/docs/zh/user_guide/optimization_and_tuning.md) | L15–17 与正文融合主张不对应；SP/CP 约束 | `0c348668366760a0` | 全文件字节一致 |
| [vLLM Ascend supported_models.md](https://raw.githubusercontent.com/vllm-project/vllm-ascend/52d4acfa51fb868823d1070b81cbd2d97e9e4696/docs/source/user_guide/support_matrix/supported_models.md) | L17–28、L77–81；W8A8 标记与空白格 | `8f8a02d898d993cf` | 全文件字节一致 |
| [vLLM _aiter_ops.py](https://raw.githubusercontent.com/vllm-project/vllm/b17039bccc17b94a2ea107272ad7bc93508708df/vllm/_aiter_ops.py) | L37–49、L829–831、L874–882；AITER 实际门控 | `83ac6929c31aaf8c` | 补充证据，作者本任务清单未列 |
| [vLLM gptq_marlin.py](https://raw.githubusercontent.com/vllm-project/vllm/b17039bccc17b94a2ea107272ad7bc93508708df/vllm/model_executor/layers/quantization/gptq_marlin.py) | L215–240、L272–295；转换条件与显式 GPTQ 选择 | `27992b98ce1e0af9` | 补充证据，作者本任务清单未列 |
| [MindIE expert_parallel.md](https://raw.githubusercontent.com/Ascend/MindIE-LLM/69e5a5dd4b533eaffc7e198320435350825a36f7/docs/zh/user_guide/feature/expert_parallel.md) | L13–14；Grouped MatMul 真正出处及模型限制 | `34e11a572286c43f` | 与 `mi-f-expert_parallel.md` 全文件字节一致 |

另独立打开 [AWQ v6 摘要](https://arxiv.org/abs/2306.00978v6)、[GPTQ v2 摘要](https://arxiv.org/abs/2210.17323v2)、[SmoothQuant v7 摘要](https://arxiv.org/abs/2211.10438v7)，并逐一打开各页的 license 链接。论文仍只作摘要级审阅，未以全文知识补足作者未取证的细节。未重取 msit 工具仓、Quark 外部文档站或硬件 kernel 本体。

本报告区分三类证据：**来源原文支持**只覆盖其确切版本和条件；**作者合理归纳**需要明确标识，不能变成厂商支持声明；**待核实**包括来源冲突、实现未读、运行未做，不能写成支持或反对。报告的修订建议也不构成本地运行成功的证据。

## 发现清单

### C01 · P2 应修：ROCm 禁用 Marlin 不等于必然使用 AITER

- **受影响位置**：[正文](../../knowledge/07-inference/quantization-and-quality.md) L70、L82、L95、L139；作者来源记录和 vLLM registry notes 有同样的简化。
- **问题陈述**：正文把“ROCm 上禁用 Marlin、走 AITER”及“ROCm 走 AITER 是自动的”写成确定事实。所引代码只给 AITER 条件标志赋值；不能从平台名称推出命中。对 `<89` 的 Marlin 描述也遗漏 batch invariant 模式关闭 Marlin 的条件。
- **上游证据**：[fp8.py L315–325](https://github.com/vllm-project/vllm/blob/b17039bccc17b94a2ea107272ad7bc93508708df/vllm/model_executor/layers/quantization/fp8.py#L315-L325) 同时检查 capability、测试强制开关、ROCm、batch invariant；AITER 来自谓词。[`_aiter_ops.py` L37–49](https://github.com/vllm-project/vllm/blob/b17039bccc17b94a2ea107272ad7bc93508708df/vllm/_aiter_ops.py#L37-L49) 检查平台、架构和库是否存在；[L829–831](https://github.com/vllm-project/vllm/blob/b17039bccc17b94a2ea107272ad7bc93508708df/vllm/_aiter_ops.py#L829-L831)、[L874–882](https://github.com/vllm-project/vllm/blob/b17039bccc17b94a2ea107272ad7bc93508708df/vllm/_aiter_ops.py#L874-L882) 还要求 AITER 与 LINEAR 开关。这里只能确认**条件路径**，未核其他后端时不能自行指定 fallback。
- **关闭条件**：修正全部重复表述及对应来源摘要，保留具体类/方法范围、门控和未核条件；回退段不得承诺所有 ROCm 或所有 `<89` 配置都会自动落入所述实现。

### C02 · P2 应修：GPTQ 警告被误写成无条件换 kernel 的保证

- **受影响位置**：正文 L70、L139；作者来源记录 GPTQ 行及 registry L6761 和 vLLM notes。
- **问题陈述**：`gptq.py` 的警告本身不执行切换。“默认用 gptq_marlin/gptq_bitblas”把日志建议、注释中的默认预期和运行时转换混为一体；回退入口因此不可靠。格式与 kernel 可以分离的结论成立，但必须加转换条件。
- **上游证据**：[gptq.py L96–102](https://github.com/vllm-project/vllm/blob/b17039bccc17b94a2ea107272ad7bc93508708df/vllm/model_executor/layers/quantization/gptq.py#L96-L102) 是 warning；[L379–390](https://github.com/vllm-project/vllm/blob/b17039bccc17b94a2ea107272ad7bc93508708df/vllm/model_executor/layers/quantization/gptq.py#L379-L390) 仍有 `gptq_gemm` 调用。[gptq_marlin.py L215–240](https://github.com/vllm-project/vllm/blob/b17039bccc17b94a2ea107272ad7bc93508708df/vllm/model_executor/layers/quantization/gptq_marlin.py#L215-L240) 要求兼容且用户选项允许；显式指定 `gptq` 时会保留 GPTQ。[L272–295](https://github.com/vllm-project/vllm/blob/b17039bccc17b94a2ea107272ad7bc93508708df/vllm/model_executor/layers/quantization/gptq_marlin.py#L272-L295) 还核平台、配置字段、位宽与 group size 等条件。
- **关闭条件**：写成“警告建议切换；符合 override 条件时可选择 Marlin”等可证口径，区分默认探查与显式选择；不能把 BitBLAS 与 Marlin 都说成无条件默认路径。同步修正作为回退依据的句子。

### C03 · P2 应修：四层中的 accumulation 尚未真正与张量 dtype 分开

- **受影响位置**：正文 L65–72、L144；summary L17。
- **问题陈述**：所谓 accumulation 实证列的是偏置 dtype、反量化参数 dtype、反量化后的操作数和 scale 修正，没有定义累加器或给出实际累加精度。`quant_bias=int32`、`deq_scale=int64/fp32` 不能据此证明 MatMul accumulator 的 dtype；FP16/BF16 反量化结果也不能直接证明 attention 内部累加精度。运行 dtype 小节同样主要举 checkpoint 参数表，尚需区分参数保存类型与 kernel 操作数类型。
- **上游证据**：[MindIE w8a8.md L33–52](https://github.com/Ascend/MindIE-LLM/blob/69e5a5dd4b533eaffc7e198320435350825a36f7/docs/zh/user_guide/feature/w8a8.md#L33-L52) 描述张量和反量化用途，不声明 accumulator；[quantized_kvcache.md L24–28](https://github.com/vllm-project/vllm/blob/b17039bccc17b94a2ea107272ad7bc93508708df/docs/features/quantization/quantized_kvcache.md#L24-L28) 描述恢复的操作数精度；[kv_cache.py L59–82](https://github.com/vllm-project/vllm/blob/b17039bccc17b94a2ea107272ad7bc93508708df/vllm/model_executor/layers/quantization/kv_cache.py#L59-L82) 描述 scale 处理。三者都不足以完成正文宣称的累加精度核验。
- **关闭条件**：明确分开保存格式、运行操作数/输出 dtype、乘加累积 dtype、scale/bias 的表示与反量化步骤；没有 kernel 证据的 accumulator 明写 unknown。可保留 `deq_scale=int64` 的原文照录及未复核说明，不应据此推断累加精度。

### C04 · P2 应修：AWQ 的通道缩放被混作量化 scale 的粒度证据

- **受影响位置**：正文 L51、L58；AWQ registry notes L6747。
- **问题陈述**：粒度表将 AWQ 的显著通道等效缩放与 MindIE `[n,1]` 的量化反量化 scale 并列，并统一解释为“按输出通道一个 scale”。前者是降低量化误差的变换，摘要没有据此声明量化产物的 scale 布局或输出通道轴；正文还把约 1% 显著**权重**改写成约 1% 显著**通道**。
- **上游证据**：[AWQ v6 摘要](https://arxiv.org/abs/2306.00978v6) 区分显著权重比例、利用激活识别显著通道、等效通道缩放，没有给出上述输出轴推论。引擎本身的 [awq.py L184–219](https://github.com/vllm-project/vllm/blob/b17039bccc17b94a2ea107272ad7bc93508708df/vllm/model_executor/layers/quantization/awq.py#L184-L219)、[L234–242](https://github.com/vllm-project/vllm/blob/b17039bccc17b94a2ea107272ad7bc93508708df/vllm/model_executor/layers/quantization/awq.py#L234-L242) 则有 `group_size`、`num_groups` 和分组 scale 张量，不能用摘要中的通道预处理代替这些格式证据。
- **关闭条件**：把 AWQ 的预处理缩放移出量化参数粒度实证或明确区分；约 1% 按显著权重照录，不计算通道比例。MindIE 的 `[n,1]` 证据可继续作为该方法的 per-channel 示例。

### C05 · P2 应修：GPTQ 机制细节超出所注明的摘要级证据

- **受影响位置**：正文 L57；作者来源记录“机制层”GPTQ 行；registry L6761。
- **问题陈述**：正文将 OBS 框架启发、逐行量化和剩余权重补偿都归于 GPTQ 摘要。这些细节不在本轮指定的摘要里；当前记录不足以判定这些扩展解释是否准确，不能按已核实机制交付。
- **上游证据**：[GPTQ v2 摘要](https://arxiv.org/abs/2210.17323v2) 支持一次性权重量化、近似二阶信息及作者实验报告，没有说明 OBS、逐行算法或补偿更新。`gptq.py` 的位宽校验另有独立代码证据，不补足算法原理来源。
- **关闭条件**：按本轮摘要级范围收缩为一次性权重量化与近似二阶信息；若保留额外细节，需另有明确取证范围和精确位置，不能继续标作“摘要支持”。同步改正来源记录与 notes 的证据范围。

### C06 · P2 应修：NVIDIA 硬件表漏掉 GPTQ 的 Volta 支持声明

- **受影响位置**：正文 L88。
- **问题陈述**：“AWQ/GPTQ 从 Turing/Ampere 起支持”没有忠实转述所引硬件表。它把两个不同支持集合合并，至少错误排除了该表 GPTQ 的 Volta 标记；也不清楚 Turing/Ampere 分别对应哪个方法。
- **上游证据**：[量化 README L48–50](https://github.com/vllm-project/vllm/blob/b17039bccc17b94a2ea107272ad7bc93508708df/docs/features/quantization/README.md#L48-L50)：AWQ 的 Volta 为否、Turing 起为是；GPTQ 的 Volta 为是；Marlin 从 Ampere 起为是。[L53–54](https://github.com/vllm-project/vllm/blob/b17039bccc17b94a2ea107272ad7bc93508708df/docs/features/quantization/README.md#L53-L54) 还区分 BitBLAS 与 BitBLAS(GPTQ)，不能按方法名称省略实现边界。
- **关闭条件**：逐行或明确分句转述方法×硬件集合，保留“文档表声明”限定；若源码与表存在差异，另列差异，不以未经核实的统一起点替代表格。

### C07 · P2 应修：E4M3 数值范围的同快照冲突被当成已确定事实

- **受影响位置**：正文 L71；作者来源记录 KV dtype 行及 vLLM registry notes。
- **问题陈述**：正文无范围限定地将 E4M3 动态范围写为 ±240，但本轮已读取的另一方法页给出 ±448。作者对 `deq_scale=int64` 已采用照录加未复核的纪律，这里尚未同样处理；不宜自行推定两值对应不同平台变体来消除矛盾。
- **上游证据**：同一 commit 的 [quantized_kvcache.md L9–14](https://github.com/vllm-project/vllm/blob/b17039bccc17b94a2ea107272ad7bc93508708df/docs/features/quantization/quantized_kvcache.md#L9-L14) 先列 E4M3FN 后写 ±240；[fp8.md L10–13](https://github.com/vllm-project/vllm/blob/b17039bccc17b94a2ea107272ad7bc93508708df/docs/features/quantization/fp8.md#L10-L13) 对 E4M3 写 ±448。当前引用没有证明二者如何对应或哪一处适用。
- **关闭条件**：分别记录两页口径和冲突，或删去没有必要的确定数值；实际 dtype/平台变体的范围留待实现或格式规范核验。正文及证据摘要不得把其中一个值提升为全部 E4M3 的统一事实。

### C08 · P2 应修：MindIE 的“未单列硬件”被提升为“通用”

- **受影响位置**：正文 L109–118，尤其 L111。
- **问题陈述**：W8A8 硬件栏“（未单列，通用）”从页面未声明限制推出通用支持，违反本任务的 unknown 纪律。W4A8 的硬件栏“（DeepSeek 专用）”实际填的是模型范围，也不能替代硬件证据。dtype 栏又将“源权重可量化类型”、scale 张量类型与运行限制并列，容易被当作精确运行组合。
- **上游证据**：[w8a8.md L5–52](https://github.com/Ascend/MindIE-LLM/blob/69e5a5dd4b533eaffc7e198320435350825a36f7/docs/zh/user_guide/feature/w8a8.md#L5-L52) 给出方法与原始权重/产物类型，没有列出通用硬件集合；[W4A8 NOTE L9–11](https://github.com/Ascend/MindIE-LLM/blob/69e5a5dd4b533eaffc7e198320435350825a36f7/docs/zh/user_guide/feature/w4a8_mixed_precision_quantization.md#L9-L11) 与[源权重说明 L54](https://github.com/Ascend/MindIE-LLM/blob/69e5a5dd4b533eaffc7e198320435350825a36f7/docs/zh/user_guide/feature/w4a8_mixed_precision_quantization.md#L54) 给出模型/配伍与源权重条件，不能凭此建立硬件支持关系。
- **关闭条件**：未单列的硬件明确写“该页未声明，unknown”；模型信息回到模型栏。区分源权重 dtype、产物 dtype、运行 dtype 限制，未核的交叉组合不合成支持结论。保留其余已准确照录的 NOTE 限制。

### C09 · P2 应修：融合/图优化机制未补齐，唯一融合例证还指错文件并漏模型条件

- **受影响位置**：正文 L76–82、L145；验收项 2。
- **问题陈述**：Attention 与 FP8 KV 的路径区别已有实质解释；融合部分仅给自动启用阈值，没有说明验收要求的内存、执行和数值路径边界；图优化只有“组合未核”一句，不能作为已经完成机制解释的依据。保持组合 unknown 是正确的，但不等于完成这部分验收。Grouped MatMul 的引文也不是所述原文，且正文遗漏其模型限定。
- **上游证据**：所引 [optimization_and_tuning.md L15–17](https://github.com/Ascend/MindIE-LLM/blob/69e5a5dd4b533eaffc7e198320435350825a36f7/docs/zh/user_guide/optimization_and_tuning.md#L15-L17) 是透明大页代码块结尾与 jemalloc 标题；该文件全文没有 Grouped MatMul。真正出处是 [feature/expert_parallel.md L13–14](https://github.com/Ascend/MindIE-LLM/blob/69e5a5dd4b533eaffc7e198320435350825a36f7/docs/zh/user_guide/feature/expert_parallel.md#L13-L14)，阈值描述限于 DeepSeek-V3/R1。另 [vLLM Ascend 功能表 L28–29](https://github.com/vllm-project/vllm-ascend/blob/52d4acfa51fb868823d1070b81cbd2d97e9e4696/docs/source/user_guide/support_matrix/supported_features.md#L28-L29) 的 Quantization 与 Graph Mode 是独立行，不证明组合命中。
- **关闭条件**：更正融合出处和模型条件；补上有精确来源支撑的融合/图优化机制边界及命中证据要求。L145 对 KV 量化“不是延迟优化”的概括应限于前文 vLLM FP8 KV 的该快照口径。未取证的量化×图组合继续 unknown，不要求虚构兼容结论或开展硬件实验来关闭本轮内容缺口。

### C10 · P3 建议：四份评估指南被统一概括成均有在线/离线两路径

- **受影响位置**：正文 L127；作者来源记录“评估指南四份”行。
- **问题陈述**：文件全文取回属实，但并非四份指南都提供两种推理路径。“命令细节待后续展开”不能支撑尚未准确核对的统一结构结论。
- **上游证据**：lm-eval 的[在线节 L5](https://github.com/vllm-project/vllm-ascend/blob/52d4acfa51fb868823d1070b81cbd2d97e9e4696/docs/source/developer_guide/evaluation/using_lm_eval.md#L5)与[离线节 L135](https://github.com/vllm-project/vllm-ascend/blob/52d4acfa51fb868823d1070b81cbd2d97e9e4696/docs/source/developer_guide/evaluation/using_lm_eval.md#L135) 均存在；[using_evalscope.md L66–77](https://github.com/vllm-project/vllm-ascend/blob/52d4acfa51fb868823d1070b81cbd2d97e9e4696/docs/source/developer_guide/evaluation/using_evalscope.md#L66-L77) 是 server/API 评估；[using_opencompass.md L90–106](https://github.com/vllm-project/vllm-ascend/blob/52d4acfa51fb868823d1070b81cbd2d97e9e4696/docs/source/developer_guide/evaluation/using_opencompass.md#L90-L106) 用 OpenAISDK；[AISBench L153–201](https://github.com/vllm-project/vllm-ascend/blob/52d4acfa51fb868823d1070b81cbd2d97e9e4696/docs/source/developer_guide/evaluation/using_ais_bench.md#L153-L201) 也是服务评估路径。这三个文件没有与 lm-eval 对应的离线引擎小节。
- **关闭条件**：按工具分别列实际覆盖路径并加具体页链接；“全文取回”“已核结构”“命令参数未核”分别记录，不据此关闭尚未取证的运行组合。

### C11 · P3 建议：FP8 质量表述被误归为论文报告

- **受影响位置**：正文 L128。
- **问题陈述**：示例中的 FP8 E4M3 质量短语来自 vLLM KV 文档，不来自本轮三篇论文摘要。当前写法没有具体论文链接，容易把引擎文档对研究的概括当作已核查的原始论文证据。
- **上游证据**：[quantized_kvcache.md L39](https://github.com/vllm-project/vllm/blob/b17039bccc17b94a2ea107272ad7bc93508708df/docs/features/quantization/quantized_kvcache.md#L39) 有该表述，但没有在该句定位研究；本轮三篇摘要分别是 AWQ、GPTQ、SmoothQuant。
- **关闭条件**：改归“vLLM 文档的质量声明，所指研究未独立核对”，或换用确实在三篇摘要中核到的论文结论并加版本化链接；继续说明本库未复现。

### C12 · P3 建议：部分真实主张的锚点尚未覆盖所指内容

- **受影响位置**：正文 L70、L103、L120；作者来源记录和相关 notes 的同类定位。
- **问题陈述**：`config/model.py L867–905` 不包含“未知方法 ValueError”的实现；`supported_models.md L17–28` 不包含正文同时讨论的 Qwen2.5-VL、Qwen3-VL、Qwen3-VL-MOE。MindIE 冲突的链接标签虽写 L10/L11，URL 没有实际行锚点。内容可被找到，但尚未达到本轮要求的精确定位。
- **上游证据**：未知方法校验在 [model.py L940–948](https://github.com/vllm-project/vllm/blob/b17039bccc17b94a2ea107272ad7bc93508708df/vllm/config/model.py#L940-L948)；多模态 W8A8 单元格在 [supported_models.md L77–81](https://github.com/vllm-project/vllm-ascend/blob/52d4acfa51fb868823d1070b81cbd2d97e9e4696/docs/source/user_guide/support_matrix/supported_models.md#L77-L81)。这些坐标均以原文件核对。
- **关闭条件**：把检测/override、未知方法校验、两张模型表分别定位，并为冲突双方补实际行锚点。Grouped MatMul 的实质错引另由 C09 关闭，不重复计数。

### C13 · P3 建议：两篇论文的许可登记与精确版本页面不一致

- **受影响位置**：[registry](../../sources/registry.yaml) L6754–6760、L6768–6774；作者来源记录“集成轮结果”的三篇统一许可口径。
- **问题陈述**：GPTQ v2 与 SmoothQuant v7 都登记为 arXiv non-exclusive；独立打开版本页面的 license 链接后，两者实际指向 CC BY 4.0。AWQ v6 的 non-exclusive 记录与页面相符，不能把该结果复制给另外两篇。这是来源元数据错误，不是本轮发生了全文再分发的指控。
- **上游证据**：[GPTQ v2 页面](https://arxiv.org/abs/2210.17323v2)与 [SmoothQuant v7 页面](https://arxiv.org/abs/2211.10438v7)的 license 链接均指向 [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/)；[AWQ v6 页面](https://arxiv.org/abs/2306.00978v6)指向 arXiv non-exclusive 页面。
- **关闭条件**：按各自固定论文版本的页面修正许可 identifier、URL 和范围说明；保留本库仅原创摘要与链接的事实，不改变整个仓库尚无统一再分发许可证的状态。

### 已核对通过的维度与证据分类

以下“通过”均为所列维度的来源/结构核对结果，不等于整篇或硬件验证通过。

| 维度 | 判定与依据 | 证据类别 |
|---|---|---|
| 固定版本与缓存身份 | 通过：29 份作者清单文件哈希、行数相符；9 份独立 raw 重取中，7 份有现有缓存可比较且全字节相同 | 来源原文支持 |
| weight-only / W8A8 基础区分 | 通过：[w8a16.md L5](https://github.com/Ascend/MindIE-LLM/blob/69e5a5dd4b533eaffc7e198320435350825a36f7/docs/zh/user_guide/feature/w8a16.md#L5) 与 [w8a8.md L5–33](https://github.com/Ascend/MindIE-LLM/blob/69e5a5dd4b533eaffc7e198320435350825a36f7/docs/zh/user_guide/feature/w8a8.md#L5-L33) 支持激活是否量化的区别；不能扩展为全部 kernel 的统一 accumulation | 来源原文支持 |
| MindIE 粒度张量形状 | 通过：W8A8 `[1]`、W8A16 `[n,1]`、W4A8 两组 scale 形状、KV 头维度形状均照录正确；Attention/FA3 的头与维度形状应保留。AWQ 的另一类缩放例外见 C04 | 来源原文支持；形状到粒度为有限归纳 |
| 校准与离群值 | 通过：SmoothQuant 摘要支持等效迁移量化难度；[anti_outlier.md L8–51](https://github.com/Ascend/MindIE-LLM/blob/69e5a5dd4b533eaffc7e198320435350825a36f7/docs/zh/user_guide/feature/anti_outlier.md#L8-L51) 支持离群值影响及 bias 处理；[Ascend quantization.md L52–56](https://github.com/vllm-project/vllm-ascend/blob/52d4acfa51fb868823d1070b81cbd2d97e9e4696/docs/source/user_guide/feature_guide/quantization.md#L52-L56) 确有两组数据参数 | 来源原文支持；Anti-Outlier 与 SmoothQuant“同族”已明确标作作者归纳，可保留 |
| 指定实现坐标 | 通过：awq L72–75 的 75、gptq L92–94 的位宽限制、L133–137 的 60 与未定注释、config/model 的 override 清单、fp8 L909–911 的特定方法异常、kv_cache L55–75 的所列分支原文都存在。警告与门控的解释需按 C01/C02 修正 | 来源原文支持，限具体路径 |
| FP8 KV 容量/延迟边界 | 通过：[quantized_kvcache.md L24–37](https://github.com/vllm-project/vllm/blob/b17039bccc17b94a2ea107272ad7bc93508708df/docs/features/quantization/quantized_kvcache.md#L24-L37) 确实给出反量化后 attention、约两倍空间、当时无延迟改善。结论限该快照该页的 FP8 KV 实现，不泛化到全部 KV 量化 | 来源原文支持 |
| Attention / FA3 与 NZ 前提 | 通过：[attention_quantization.md L5–59](https://github.com/Ascend/MindIE-LLM/blob/69e5a5dd4b533eaffc7e198320435350825a36f7/docs/zh/user_guide/feature/attention_quantization.md#L5-L59)、前述 FA3 L5–13/L86–122 支持计算路径区别、k 非 rope 对象与 NZ 条件；无本库收益实测 | 来源原文支持 |
| AMD 表列及 KV dtype | 通过：README L46–58 的 AMD 列确实仅 FP8(W8A8)/GGUF 为是；KV 页 L64–68 仅为 `fp8`/`fp8_e4m3` 明列 ROCm，`fp8_e5m2` 只列 CUDA。这里核的是文档声明，不证明所有 AMD 设备均可运行 | 来源原文支持 |
| Quark MXFP4/MXFP6 | 通过：[quark.md L259–293](https://github.com/vllm-project/vllm/blob/b17039bccc17b94a2ea107272ad7bc93508708df/docs/features/quantization/quark.md#L259-L293) 支持模型加载、非原生设备融合反量化、混合精度及精度取舍。正文所说设备选精度是该页示例，不能提升为每台设备的最优部署证明 | 来源原文支持；外部工具与实际加载组合仍待核实 |
| vLLM Ascend W8A8 / 空白格 | 通过：功能表 W8A8 Functional、W4A8 在研的口径准确；量化指南的 ModelSlim/LLM-Compressor 参数差异准确；模型表所述勾选与四个空白项均准确，空白没有被当作不支持。多模态定位需按 C12 补齐 | 来源原文支持；空白组合待核实 |
| MindIE 九份特性页覆盖 | 通过：八行方法表加已在机制节讨论的 Anti-Outlier 共对应九份特性文件，不应误算为漏了一种表内方法。W8A16、KV int8、Attention、FA3、W4A8、两种稀疏方法的明确模型/硬件/NOTE 限制基本照录正确；硬件未知项及 dtype 口径见 C08 | 来源原文支持，未单列条件待核实 |
| 两组指定支持冲突 | 通过：正文 L88/L120 保留 INT8 Turing 的 README 与严格大于号矛盾，以及 KV int8 仅搭 W8A8 与 W8A16 页声明的冲突；相应组合保持 unknown，未自行裁定或合成并集 | 冲突原文已核；可用性待核实 |
| MindIE 异常 dtype | 通过：正文 L72/L157 将 `deq_scale=int64` 明写为来源原文且未核实现；W4A8 表 2 的 `bfloat32` 只在证据记录/notes 照录，没有被正文宣布为已验证运行类型。不能以此关闭 C03 | 来源原文照录；实现待核实 |
| 三层判断与联合验收框架 | 通过其框架：正文 L124–139 有固定任务、baseline、样本量、阈值归属、三层证据方向及 BF16/FP16 单变量回退。具体自动回退例子需按 C01/C02 改正 | 作者合理归纳；不是厂商统一验收标准 |
| frontmatter、本地链接与来源 ID | 结构通过：稳定 ID、`draft`、三平台、七项来源 ID、六项 related ID 均有效；`source_checked` 的 notes 明示未运行实验。`evidence_refs` 仅列三条引擎来源不违反 schema；论文仍在 `source_refs` 中。notes 的“已核对”不能替代本报告发现的语义修正 | 结构核对通过；来源许可元数据另见 C13 |

## acceptance 五项逐条判定

依据 [T07-04 acceptance](../../plans/full-coverage-backlog.yaml) L6373–6377，逐项判定如下。这里的“部分满足，需修订”不计为通过，也不因为有 unknown 就判定组合不支持。

| 验收项 | 判定 | 已满足依据 | 尚需关闭 |
|---|---|---|---|
| 1. 说明 scale/zero point、粒度、校准、weight-only/W8A8 等机制，区分文件格式、kernel、运行 dtype、accumulation | **部分满足，需修订** | L44 的整数近似式、MindIE 张量形状、离群值处理、weight-only/W8A8 区分和格式/kernel 分离入口已建立 | C01–C05：kernel 门控被过度简化；累加精度未真正区分；AWQ 缩放/比例与 GPTQ 摘要范围须改正。整数公式应保留其整数近似语境，不能据此声称已解释 FP8 编码 |
| 2. 解释融合/attention/图优化的内存、执行、数值路径边界，不能把启用视为命中 | **部分满足，需修订** | L80–81 的 FP8 KV 与 MindIE attention/FA3 对照有直接来源，NZ 前提准确 | C01、C09：确定性 AITER 描述违背该节原则；融合出处/条件需纠正，融合及图优化机制还未补齐。量化×图组合继续 unknown |
| 3. 分别核查三平台精确硬件/方法/dtype/KV 组合；保留冲突并说明采信范围 | **部分满足，需修订** | 三条引擎证据线分开；AMD 列、KV dtype、Quark、Ascend 模型空白格及两组指定冲突均核实 | C01/C02、C06–C08：修正 kernel 条件、GPTQ Volta、E4M3 冲突及 MindIE “通用”推断；C12 补准确坐标。不得把独立支持行拼成未核的交叉组合 |
| 4. 建立初始化/算子/质量三层判断、回退及质量/性能共同验收入口 | **部分满足，需修订** | L124–139 框架齐备，baseline、固定任务和业务阈值边界清楚，确有 `lm_eval` 上游示例 | C01/C02：回退段把可选实现当自动保障，应改为符合条件的候选路径；C10/C11 改正评估指南范围与质量声明来源。联合验收规则标明为本库建议 |
| 5. 支持矩阵覆盖本任务采取组合；未核组合保持 unknown，不能用目录存在关闭缺口 | **部分满足，需修订** | 已从存在性升级为具体文件和实现核查；msit、kernel 数值行为、Quark 加载、图组合明确未核；没有虚构运行结果 | C08 是明确反例：“未单列”不能转“通用”；C01/C02/C07 还需恢复条件与冲突。C10 须区分取回全文和实际核实范围。本任务没有真实部署组合，不能以本轮来源核对宣称任一现场组合验收成功 |

## 整体结论

**需修订后复核。** 无 P1；C01–C09 为应修项，主要涉及把条件分支写成默认保障、四层精度概念未分清、支持矩阵误读及验收项 2 的内容缺口。C10–C13 为来源范围、定位和登记建议，一并处理可以避免后续沿用错误证据摘要。作者的缓存身份、平台分线、两组既有冲突保留、异常 dtype 照录及未执行硬件实验的边界均可保留。

修订后须按 C01–C13 的关闭条件定向复核，重新记录正文指纹；本报告不把“报告已交付”或“结构检查通过”记作问题已关闭。允许未取证的具体组合继续保持 unknown，不要求为通过内容审阅而虚构技术裁定。

本轮仅新增本报告，不修改正文、来源记录、registry、任务状态或导航。`make check` 已通过（111 content entries / 542 sources）；`make build` 在临时源码副本通过，并确认新生成 catalog 中正文 SHA-256 和元数据与本次审阅版本相符。首次临时构建因既有文档链接要求 `build/catalog.json`、`build/catalog.md` 预先存在而失败；复制工作区已有的这两个目标到临时副本后重新构建通过，未修改源文件或检查规则。生成物只写入临时副本并随副本清理，工作区原有文件指纹未变。结构检查和构建只验证结构与本地引用，不建立技术正确性或硬件复现结论。

发现 13 项：P1 0、P2 9、P3 4
