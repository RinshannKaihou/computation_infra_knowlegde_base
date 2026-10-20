# Batch 27 · T07-04 第一轮定向复核

## 会话元数据

| 项目 | 实际记录 |
|---|---|
| 角色与范围 | AI 可靠性知识库批次审阅者；仅复核[初审报告](batch-27-t07-04-codex-review.md) C01–C13 的关闭条件及修订引入的问题，不重做整篇初审 |
| 实际执行模型 | `gpt-6.1-sol` |
| 实际推理档位 | `xhigh` |
| 元数据依据 | 当前 Codex 会话 JSONL 的 `turn_context.model`、`turn_context.effort` 与 `session_meta.cwd`；不是从用户指定值反填 |
| 会话 ID | `01a15af6-1aa6-7ae3-b13f-8195d795f31d` |
| 运行记录 | `/Users/ywang2397/.codex/sessions/2026/10/21/rollout-2026-10-21T04-17-20-01a15af6-1aa6-7ae3-b13f-8195d795f31d.jsonl`；provider=`custom`，CLI=`0.163.0` |
| cwd | `/Users/ywang2397/work/AI_reliability_knowledge_base` |
| 日期与时区 | 2026-10-21，Asia/Shanghai（UTC+08:00）；会话启动于当地 04:17:20 |
| 复核基点 | Git HEAD `d5bef70a40e2210c223467de17c035829179cd05` 加修订后的工作区；以下行号均为本轮工作区原文件坐标 |
| 正文 | [quantization-and-quality.md](../../knowledge/07-inference/quantization-and-quality.md)，176 行；SHA-256 `8498c6c3dba1c89876e0fa75c522201cb727d1274055111b9e21d5491c88876d` |
| registry | [registry.yaml](../../sources/registry.yaml)，SHA-256 `6e22a2d6e9930886f3c252aef26c1c1f5029e260d1ca0b5ce7878b2977ebd518` |
| 来源修订记录 | [batch-27-t07-04-sources.md](batch-27-t07-04-sources.md)，SHA-256 `d0906c31f0e0cb77ceb5edf5d66159e31b2b1ad2d31354a3d7caeecd57530a96`；本轮修订节为 L108–121 |
| 执行边界 | 本会话直接复核，未调用其他审阅模型或子代理；未运行量化、推理、质量评估或硬件实验；仓库只新增本报告 |

按 README、写作指南与初审关闭条件逐项读取修订。技术依据优先使用 `/tmp/b27-fetch/` 原文件，沿用固定快照：vLLM `b17039bccc17b94a2ea107272ad7bc93508708df`、vLLM Ascend `52d4acfa51fb868823d1070b81cbd2d97e9e4696`、MindIE-LLM `69e5a5dd4b533eaffc7e198320435350825a36f7`。缺少的两个实现文件通过 GitHub 连接器按固定 commit 重取至 `/tmp/b27-recheck-evidence/`：`_aiter_ops.py` 的 SHA-256 为 `83ac6929c31aaf8c894823766f0a8e7167c34974c9d8a8f5cfa05ee6be07d23e`，`gptq_marlin.py` 为 `27992b98ce1e0af9175602e446f24e2493028c150cad08733f577e1953197c9e`，均与初审记录相符。另打开三篇固定版本摘要页及各自 license 链接；论文机制仍限摘要级。

来源记录末尾的“初审修订轮”作为对前文首轮记录的更正读取；例如 L112/L113/L118/L120 分别覆盖前文 AWQ、GPTQ 机制、评估指南与定位的旧摘要。本轮不因历史段落保留而重复开放问题，后续引用应指向修订节。**当前 registry 的 notes 则仍是有效登记**，其中相互矛盾的现行摘要不能由来源记录末尾的“已改”声明消除。CLOSED 只代表该项关闭条件满足，不证明未知组合可用，也不代表实验验证。

## C01–C13 逐项判定

### C01 · OPEN（仍开放）：AITER 条件已补，Marlin 强制开关逻辑写反

- **已满足部分**：正文 L72/L111/L157/L176 已撤回“ROCm 必然走 AITER”，改为谓词候选及不通过时路径 unknown；L72 补入 batch invariant。vLLM 登记 notes（registry L536）及来源修订节 L110 同步采用条件口径。重取的 [`_aiter_ops.py` L29–49](https://github.com/vllm-project/vllm/blob/b17039bccc17b94a2ea107272ad7bc93508708df/vllm/_aiter_ops.py#L29-L49)、[L829–831](https://github.com/vllm-project/vllm/blob/b17039bccc17b94a2ea107272ad7bc93508708df/vllm/_aiter_ops.py#L829-L831)、[L874–882](https://github.com/vllm-project/vllm/blob/b17039bccc17b94a2ea107272ad7bc93508708df/vllm/_aiter_ops.py#L874-L882)支持平台、gfx9、库存在及 AITER/LINEAR 开关门控。
- **未满足部分**：正文 L72 与 registry L536 将 Marlin 写为“capability<89、非 batch invariant 且非测试强制”。[`Fp8LinearMethod.__init__` 的 fp8.py L315–325](https://github.com/vllm-project/vllm/blob/b17039bccc17b94a2ea107272ad7bc93508708df/vllm/model_executor/layers/quantization/fp8.py#L315-L325) 实际先以 `not has_device_capability(89) or VLLM_TEST_FORCE_FP8_MARLIN` 置位，再由 ROCm 或 batch invariant 清除。测试强制是 **OR 的启用项**，不是排除项。这是修订新引入的反向条件。
- **关闭所需**：正文及现行 notes 按上述布尔顺序改正，并限定为该类初始化中的标志逻辑；继续保留 AITER 未命中时的 unknown 与回退候选口径。

### C02 · OPEN（仍开放）：正文已修正，GPTQ 登记仍留“默认切”

- **已满足部分**：正文 L72 明写“警告建议”、警告本身不切换、`gptq_gemm` 调用仍在；补兼容性与用户选项条件，以及显式 `gptq` 保留。L157 已改回退“候选”，不再承诺自动保障；vLLM 登记 L536 和来源修订节 L110 同步修正。[gptq.py L96–102](https://github.com/vllm-project/vllm/blob/b17039bccc17b94a2ea107272ad7bc93508708df/vllm/model_executor/layers/quantization/gptq.py#L96-L102) 确为警告；重取的 [gptq_marlin.py L215–240](https://github.com/vllm-project/vllm/blob/b17039bccc17b94a2ea107272ad7bc93508708df/vllm/model_executor/layers/quantization/gptq_marlin.py#L215-L240) 要求兼容且 `user_quant` 为 `None`、`marlin` 或 `gptq_marlin`，显式 `gptq` 不 override；[L272–295](https://github.com/vllm-project/vllm/blob/b17039bccc17b94a2ea107272ad7bc93508708df/vllm/model_executor/layers/quantization/gptq_marlin.py#L272-L295)有平台、字段、位宽与 group size 核验。
- **未满足部分**：`src.arxiv.gptq-2210.17323` 的现行 notes（registry L6761）仍写“gptq_gemm 4-bit buggy 默认切 Marlin 族”，与正文和同表 vLLM notes 矛盾。初审已将该位置列入受影响范围，重复表述尚未清完。
- **关闭所需**：删除或按条件改写该登记中的默认切换断言。不能用它与另一条已修正 notes 的交叉引用代替更正。

### C03 · CLOSED：accumulation 已独立，未知边界明确

正文 L17/L38 不再声称累加精度已核实；L71–74 区分 checkpoint、kernel、参数保存/运行操作数与累加器，第 4 项明确 MatMul/attention 累加精度 unknown，参数及反量化后的类型均不能证明 accumulator。L165/L176 和来源修订节 L111 保持相同边界。[MindIE w8a8.md L33–52](https://github.com/Ascend/MindIE-LLM/blob/69e5a5dd4b533eaffc7e198320435350825a36f7/docs/zh/user_guide/feature/w8a8.md#L33-L52)、[KV 文档 L24–28](https://github.com/vllm-project/vllm/blob/b17039bccc17b94a2ea107272ad7bc93508708df/docs/features/quantization/quantized_kvcache.md#L24-L28)及 `kv_cache.py` 的 scale 分支均未被提升为累加器精度证据。异常 `deq_scale=int64` 仍仅照录且注明实现未复核。

### C04 · CLOSED：AWQ 预处理与产物粒度已分开

正文 L51 不再用 AWQ 显著通道缩放证明 per-channel 量化 scale；L55 明写量化前预处理，L55/L60 的约 1% 均指显著**权重**。L52 保留的是另取实现证据的 AWQ 分组 scale，并非把预处理重新放回粒度表。[AWQ v6 摘要](https://arxiv.org/abs/2306.00978v6)支持显著权重比例、激活识别通道及等效变换；[awq.py L184–242](https://github.com/vllm-project/vllm/blob/b17039bccc17b94a2ea107272ad7bc93508708df/vllm/model_executor/layers/quantization/awq.py#L184-L242)确有 `group_size`、`num_groups` 和分组 scale 张量。registry L6747 与来源修订节 L112 已按此区分；没有将摘要推成输出通道比例或产物布局证明。

### C05 · CLOSED：GPTQ 机制已收缩至摘要范围

正文 L59 将正面机制限定为一次性后训练权重量化、近似二阶信息；OBS 渊源、逐行与补偿细节明写未取证。与 [GPTQ v2 摘要](https://arxiv.org/abs/2210.17323v2)吻合；实现位宽限制另归 `gptq.py`，未用于补足算法机制。registry L6761 的机制部分与来源修订节 L113 同步收缩。该 notes 中剩余的 kernel 默认切换错误归 C02，不重复计为机制越界。

### C06 · CLOSED：GPTQ Volta 与两条 BitBLAS 已忠实分列

正文 L93–102 明示为 v0.14.0 文档表声明，AWQ 的 Volta ❌、GPTQ 的 Volta ✅、Marlin 的 Ampere 起 ✅ 各自独立；BitBLAS 的 Volta–Hopper ✅ 与 BitBLAS(GPTQ) 的 Ampere 起 ✅ 已分句区分。与原文件 [README L46–58](https://github.com/vllm-project/vllm/blob/b17039bccc17b94a2ea107272ad7bc93508708df/docs/features/quantization/README.md#L46-L58)逐行对应。来源修订节 L114 记录一致；不重新展开初审已通过的其他平台列。

### C07 · CLOSED：E4M3 两页数值冲突已保留

正文 L76 同列 [quantized_kvcache.md L9–14](https://github.com/vllm-project/vllm/blob/b17039bccc17b94a2ea107272ad7bc93508708df/docs/features/quantization/quantized_kvcache.md#L9-L14)的 ±240 与 [fp8.md L10–13](https://github.com/vllm-project/vllm/blob/b17039bccc17b94a2ea107272ad7bc93508708df/docs/features/quantization/fp8.md#L10-L13)的 ±448，各归页面，不自行配对平台变体；L176 继续列作待核。来源修订节 L115 同步记录两说。registry L536 的 ±240 位于 `quantized_kvcache.md` 专属摘要中，按该页口径读取，不能脱离页面限定引用为全部 E4M3 的统一事实；本轮不裁定实际格式范围。

### C08 · CLOSED：MindIE 未声明项与 dtype 三类信息已区分

正文 L123/L127/L132 将 W8A8、W4A8 未给出的硬件改成“该页未声明”，由表前总说明限定 unknown；W4A8 的 DeepSeek 模型范围回到模型栏。L125/L136 将源权重类型、产物参数布局与运行限制分别解释，明确三者不互推、交叉组合未核。与 [w8a8.md L33–52](https://github.com/Ascend/MindIE-LLM/blob/69e5a5dd4b533eaffc7e198320435350825a36f7/docs/zh/user_guide/feature/w8a8.md#L33-L52)、[W4A8 L9–11](https://github.com/Ascend/MindIE-LLM/blob/69e5a5dd4b533eaffc7e198320435350825a36f7/docs/zh/user_guide/feature/w4a8_mixed_precision_quantization.md#L9-L11)及 [L54](https://github.com/Ascend/MindIE-LLM/blob/69e5a5dd4b533eaffc7e198320435350825a36f7/docs/zh/user_guide/feature/w4a8_mixed_precision_quantization.md#L54)的证据边界相符；来源修订节 L116 一致。其余已通过的 NOTE 限制不重新展开。

### C09 · OPEN（仍开放）：融合例证补入，图优化机制缺口与新定位错误仍在

- **已满足部分**：正文 L86 的 Grouped MatMul 改引 [expert_parallel.md L13–14](https://github.com/Ascend/MindIE-LLM/blob/69e5a5dd4b533eaffc7e198320435350825a36f7/docs/zh/user_guide/feature/expert_parallel.md#L13-L14)，保留 DeepSeek-V3/R1 与专家并行数>32；补入 [Quark L271](https://github.com/vllm-project/vllm/blob/b17039bccc17b94a2ea107272ad7bc93508708df/docs/features/quantization/quark.md#L271) 的融合在线反量化与 MindIE 通算融合例证，并要求日志/profiling 确认命中。L84/L163 将 KV 延迟结论限定为该快照 vLLM FP8 KV 实现；来源修订节 L117 同步记录。
- **未满足部分**：初审关闭条件还包括有精确来源支撑的**图优化机制边界**。正文 L87 仍仅指出 Quantization/Graph Mode 是独立支持行、组合 unknown，与初审指出的原缺口相同；[supported_features.md L28–29](https://github.com/vllm-project/vllm-ascend/blob/52d4acfa51fb868823d1070b81cbd2d97e9e4696/docs/source/user_guide/support_matrix/supported_features.md#L28-L29)只能支持独立状态声明，不能补足图优化的执行、内存和数值边界。L86 的“改变内存布局”也未说明具体是哪种布局变化、由哪份例证支持。
- **修订新问题**：L86 把 `ep_level=2` 的 AllToAll＋通算融合定位为 `expert_parallel.md L5–7`；原文件 L7 实为 `ep_level=1` 的 AllGather，`ep_level=2` 在 [L9](https://github.com/Ascend/MindIE-LLM/blob/69e5a5dd4b533eaffc7e198320435350825a36f7/docs/zh/user_guide/feature/expert_parallel.md#L9)及参数表 L25。Grouped MatMul 的 L13–14 已正确，不能把两处混为同一定位问题。
- **关闭所需**：改正新例证坐标，按具体例证说明实际支持的融合边界，并补有精确来源的图优化机制解释及命中证据要求。未取证的量化×图组合继续 unknown；不要求虚构兼容结论或运行硬件实验。

### C10 · CLOSED：四份指南按工具记录路径

正文 L145、registry 的 Ascend notes（L555）和来源修订节 L118 已区分：lm-eval [L5](https://github.com/vllm-project/vllm-ascend/blob/52d4acfa51fb868823d1070b81cbd2d97e9e4696/docs/source/developer_guide/evaluation/using_lm_eval.md#L5)/[L135](https://github.com/vllm-project/vllm-ascend/blob/52d4acfa51fb868823d1070b81cbd2d97e9e4696/docs/source/developer_guide/evaluation/using_lm_eval.md#L135)为在线/离线两节；EvalScope [L66–77](https://github.com/vllm-project/vllm-ascend/blob/52d4acfa51fb868823d1070b81cbd2d97e9e4696/docs/source/developer_guide/evaluation/using_evalscope.md#L66-L77)为 server/API；OpenCompass [L90–106](https://github.com/vllm-project/vllm-ascend/blob/52d4acfa51fb868823d1070b81cbd2d97e9e4696/docs/source/developer_guide/evaluation/using_opencompass.md#L90-L106)用 OpenAISDK 连服务；AISBench [L153–201](https://github.com/vllm-project/vllm-ascend/blob/52d4acfa51fb868823d1070b81cbd2d97e9e4696/docs/source/developer_guide/evaluation/using_ais_bench.md#L153-L201)的实际示例为 `attr="service"`。AISBench 对 `local` 可选值的介绍不等于该指南提供了对应离线引擎流程。全文取回、路径结构核对和命令参数未逐字核的边界已分开；本轮未执行示例命令。

### C11 · CLOSED：FP8 质量短语已归 vLLM 文档

正文 L146 将该句明确归为 [vLLM quantized_kvcache.md L39](https://github.com/vllm-project/vllm/blob/b17039bccc17b94a2ea107272ad7bc93508708df/docs/features/quantization/quantized_kvcache.md#L39)对研究的概括，并说明所指研究未独立核对、本库未复现；来源修订节 L119 同步。没有再把它归入本轮 AWQ/GPTQ/SmoothQuant 摘要。

### C12 · CLOSED：指定的四组定位已更正

正文 L72/L153 将方法检测/override 与未知方法校验分开，后者定位 [model.py L940–948](https://github.com/vllm-project/vllm/blob/b17039bccc17b94a2ea107272ad7bc93508708df/vllm/config/model.py#L940-L948)；L119 将文本表 L17–28 与多模态表 [supported_models.md L77–81](https://github.com/vllm-project/vllm-ascend/blob/52d4acfa51fb868823d1070b81cbd2d97e9e4696/docs/source/user_guide/support_matrix/supported_models.md#L77-L81)分开；L138 的 MindIE 冲突双方链接实际带 [kv_cache_int8.md #L10](https://github.com/Ascend/MindIE-LLM/blob/69e5a5dd4b533eaffc7e198320435350825a36f7/docs/zh/user_guide/feature/kv_cache_int8.md#L10)与 [w8a16.md #L11](https://github.com/Ascend/MindIE-LLM/blob/69e5a5dd4b533eaffc7e198320435350825a36f7/docs/zh/user_guide/feature/w8a16.md#L11)。逐一对照原文件，指定内容均在所指范围内。来源修订节 L120 给出同样更正；新补的 EP 融合错位另归 C09，不因此重新开放已修正的四组坐标。

### C13 · OPEN（仍开放）：许可标识及 URL 正确，范围说明沿用旧许可

- **已满足部分**：直接读取 registry：GPTQ L6757–6759、SmoothQuant L6771–6773 的 identifier 均已改 `CC BY 4.0`，URL 均为 `https://creativecommons.org/licenses/by/4.0/`，scope 带 2026-10-21 的版本页复核说明。重新打开 [GPTQ v2](https://arxiv.org/abs/2210.17323v2)与 [SmoothQuant v7](https://arxiv.org/abs/2211.10438v7)各自 license 链接，均到该许可；[AWQ v6](https://arxiv.org/abs/2306.00978v6)仍到 arXiv non-exclusive，与其登记一致。来源修订节 L121 已更正三篇统一许可的旧摘要。
- **未满足部分**：两条 `license.notes`（registry L6760/L6774）仍写“该许可授予 arXiv 分发权，不是本库复制、改编或再发布全文的通用许可”。这沿用的是 arXiv non-exclusive 的说明，与新 identifier 不相容。[CC BY 4.0 官方说明](https://creativecommons.org/licenses/by/4.0/)允许在遵守署名、许可链接与修改说明等条件下分享、改编，并非仅向 arXiv 授予分发权。初审的关闭条件明确包括**范围说明**，所以不能仅凭 identifier 和 URL 正确关闭。
- **关闭所需**：分别改正两条许可范围 notes；保留“本库仅原创摘要与链接、未复制全文图表”的使用事实及仓库尚无统一再分发许可的状态。该项不指称本轮发生了未经授权的再分发。

## 修订是否引入新问题

**是。** 本轮在原问题内记录以下修订问题，不另增加 C 编号或重复计数：

| 对应项 | 修订问题 | 影响与处理 |
|---|---|---|
| C01（P2） | 正文 L72、registry L536 把测试强制启用 Marlin 写成“非测试强制” | 反转了已核分支的布尔条件；须按 `(!capability89 OR force) AND !ROCm AND !batch_invariant` 的初始化标志逻辑修正，实际 kernel 命中仍另取证 |
| C09（P3） | 新补 `ep_level=2` 融合例证标为 L5–7 | 指向 AllGather/level 1；应定位 L9 或参数表 L25。Grouped MatMul 的 L13–14 及模型限定已正确 |
| C13（P3） | 两条登记改为 CC BY 4.0 后，notes 仍描述 arXiv 专用分发授权 | 新标识与旧范围说明形成现行元数据矛盾；须同步修正说明 |

其余本轮改动中未发现需要另立编号的新问题。来源修订节作为更正记录使用，不把被覆盖的首轮摘要再算作新发现；C02 的 GPTQ notes 默认切换是未修完的旧问题，C09 的图优化机制解释是原缺口，均与上表区分。

## 整体结论

**本轮仍需修订后定向复核，不能声明 C01–C13 全部关闭或 T07-04 审阅通过。** 已关闭 C03、C04、C05、C06、C07、C08、C10、C11、C12；仍开放 C01、C02、C09、C13。下一轮只需核对 Marlin 条件、GPTQ 残留 notes、融合定位与图优化机制缺口、两条许可范围说明及其关联改动；本报告不重新展开初审已通过的维度。

`make check` 通过（111 content entries / 542 sources）；`make build` 在包含本报告的临时源码副本通过，生成物仅写入临时副本，随后清理。复核前后的文件指纹比较确认原有工作区文件与原有 build/catalog.json、build/catalog.md 均未改变，仓库仅新增本报告。这些检查只验证结构与本地引用，不替代上述语义判断；本轮没有硬件或模型质量验证结论。

C01–C13：CLOSED 9、OPEN 4
