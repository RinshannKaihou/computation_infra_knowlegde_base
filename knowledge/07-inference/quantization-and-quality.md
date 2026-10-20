---
id: inference.quantization-and-quality
title: 推理量化与输出质量验证
type: concept
domain: inference
status: draft
platforms: [nvidia, amd, ascend]
source_refs:
  - src.vllm.inference-v0-14
  - src.ascend.vllm-ascend-v0-14-0rc1
  - src.ascend.mindie-llm-docs-69e5a5dd
  - src.arxiv.awq-2306.00978
  - src.arxiv.gptq-2210.17323
  - src.arxiv.smoothquant-2211.10438
  - src.ascend.msmodelslim-msit
updated_at: "2026-10-21"
summary: 量化以精度换内存与速度；机制上区分 scale/zero point、粒度、校准与 weight-only/W8A8；工程上量化文件格式、执行 kernel 与运行 dtype 是三层独立事实，乘加累加精度本轮无证据保持 unknown；支持矩阵按 vLLM NVIDIA、AMD/ROCm 与 Ascend/MindIE 分别核对并保留冲突声明；输出质量用固定任务的评估对照验证，量化故障按初始化、算子、精度三层归因。
related_ids:
  - inference.execution-and-kv-cache
  - inference.latency-metrics
  - inference.ascend-inference-oom-triage
  - inference.model-loading-and-readiness
  - reliability.silent-errors-and-integrity
  - training.gpu-npu-precision-difference-triage
verification:
  status: source_checked
  evidence_refs:
    - src.vllm.inference-v0-14
    - src.ascend.vllm-ascend-v0-14-0rc1
    - src.ascend.mindie-llm-docs-69e5a5dd
  notes: "已核对 vLLM v0.14.0 固定 commit 的量化文档页（README 硬件表/int8/fp8/kvcache/quark）与实现（awq/gptq/fp8/kv_cache/config.model 及复核补充的 _aiter_ops、gptq_marlin）、vLLM Ascend v0.14.0rc1 的 quantization 指南与模型矩阵、MindIE-LLM@69e5a5dd 的九个量化特性页与性能调优页、三篇论文摘要。论文为摘要级证据，机制细节以摘要原文为限。逐条主张与行号锚点见 docs/research/batch-27-t07-04-sources.md（含初审后修订）。未运行任何量化、推理或评估；乘加累加精度与 kernel 数值行为未核。"
---

# 推理量化与输出质量验证

## 定义与要解决的问题

量化以模型精度换取更小的内存占用与更高的吞吐（[vLLM v0.14.0 量化文档](https://github.com/vllm-project/vllm/blob/b17039bccc17b94a2ea107272ad7bc93508708df/docs/features/quantization/README.md)的定义）。本文回答五个问题：量化机制怎么读（scale、zero point、粒度、校准）；量化文件格式、执行 kernel 与运行 dtype 这三层怎么区分、乘加累加精度为什么仍是 unknown；优化选项启用为什么不等于实际命中；支持矩阵怎么按三平台分别核对；量化后的输出质量如何验证、量化故障按什么分层归因。

平台口径：本文的 NVIDIA/AMD 证据来自 vLLM v0.14.0 上游（commit `b17039bc`）；Ascend 证据分两条线——vLLM Ascend v0.14.0rc1（commit `52d4acfa`）与 MindIE-LLM 文档线（master@`69e5a5dd`，自述 3.1.0）。三线是不同证据，互相不能推断。

## 机制：scale、zero point、粒度与校准

量化的基本运算是把高精度数值近似为低位整数表示，scale/zero point 决定映射关系（对称量化无 zero point）。这一近似式描述的是定点整数量化（INT8/INT4 一族）；FP8 是浮点格式（见下文 dtype 节），不适用同一公式。**scale/zero point 存在于哪、按什么粒度存、怎么标定**是三个独立维度。

**粒度 ladder**（各引擎实证，同引擎不同方法粒度不同）：

| 粒度 | 实证（引擎×方法） | 证据 |
|---|---|---|
| per-tensor | MindIE W8A8 的激活 scale：input_scale/input_offset shape `[1]`（[w8a8.md 表 1/2](https://github.com/Ascend/MindIE-LLM/blob/69e5a5dd4b533eaffc7e198320435350825a36f7/docs/zh/user_guide/feature/w8a8.md)）；vLLM FP8 KV cache 当前仅 per-tensor（[quantized_kvcache.md L16–18](https://github.com/vllm-project/vllm/blob/b17039bccc17b94a2ea107272ad7bc93508708df/docs/features/quantization/quantized_kvcache.md#L16-L18)） | 激活整张量一个 scale |
| per-channel | MindIE W8A16 的权重 scale：weight_scale/offset `[n,1]`（[w8a16.md 表 1/2](https://github.com/Ascend/MindIE-LLM/blob/69e5a5dd4b533eaffc7e198320435350825a36f7/docs/zh/user_guide/feature/w8a16.md)） | 按输出通道一个 scale |
| per-channel＋per-group | MindIE W4A8 路由专家：weight_scale `[n,1]`＋weight_scale_second `[n,group_num]`（[w4a8 混合量化](https://github.com/Ascend/MindIE-LLM/blob/69e5a5dd4b533eaffc7e198320435350825a36f7/docs/zh/user_guide/feature/w4a8_mixed_precision_quantization.md)）；AWQ 实现侧有 group_size/分组 scale 张量（[awq.py L184–242](https://github.com/vllm-project/vllm/blob/b17039bccc17b94a2ea107272ad7bc93508708df/vllm/model_executor/layers/quantization/awq.py#L184-L242)） | 4bit 权重的常规做法：通道内再分组 |
| per-head / 按 KV 头维度 | MindIE KV Cache int8：kv_cache_scale/offset shape `[kv_head_num×kv_head_dim]`（[kv_cache_int8.md 表 1/2](https://github.com/Ascend/MindIE-LLM/blob/69e5a5dd4b533eaffc7e198320435350825a36f7/docs/zh/user_guide/feature/kv_cache_int8.md)）；Attention 量化/FA3 量化 per-head（[attention_quantization.md 表 1](https://github.com/Ascend/MindIE-LLM/blob/69e5a5dd4b533eaffc7e198320435350825a36f7/docs/zh/user_guide/feature/attention_quantization.md)、[fa3_quantization.md](https://github.com/Ascend/MindIE-LLM/blob/69e5a5dd4b533eaffc7e198320435350825a36f7/docs/zh/user_guide/feature/fa3_quantization.md)） | KV 类量化按头维度标定 |

注意区分两类"缩放"：上表是**量化产物中的 scale/zero point 参数布局**；AWQ 论文的"显著通道等效缩放"是量化前的预处理变换（用激活统计保护约 1% 显著**权重**，对相应通道做数学等效缩放以降低量化误差），不是量化 scale 的粒度声明——摘要未给出其量化产物的 scale 布局，产物布局以实现侧 group_size 证据为准。

**校准与离群值**：scale 通常不能直接取数值范围，需要校准数据集统计分布，并对激活离群值做处理——离群点会把 scale 拉大、压低正常数值的量化分辨率。三种代表做法（论文证据限摘要级）：

- **GPTQ**：一次性后训练权重量化，利用权重的近似二阶信息（[arXiv:2210.17323](https://arxiv.org/abs/2210.17323) 摘要）。其 OBS 框架渊源、逐行量化与剩余权重补偿等算法细节超出摘要证据，本轮未取证，保持 unknown。vLLM 实现限制权重 2/3/4/8-bit（[gptq.py L92–94](https://github.com/vllm-project/vllm/blob/b17039bccc17b94a2ea107272ad7bc93508708df/vllm/model_executor/layers/quantization/gptq.py#L92-L94)）。
- **AWQ**：weight-only，按离线激活统计识别显著权重（约 1%），对相应通道做等效缩放降低量化误差；不混合精度、不反传、不重建（[arXiv:2306.00978](https://arxiv.org/abs/2306.00978) 摘要）。
- **SmoothQuant**：观察到激活难量化（有离群点）而权重易量化，用数学等效变换把量化难度从激活迁移到权重（[arXiv:2211.10438](https://arxiv.org/abs/2211.10438) 摘要）。

MindIE 的 Anti-Outlier 属于同族思路（本库归纳，非来源声明）：抑制激活离群点对 scale 的影响，非对称算法引入 norm_bias 在 Norm 层加、Linear 层减以保计算等价；per-tensor 场景融合进 quant_bias，per-token 场景体现为普通 bias（[anti_outlier.md L31–51](https://github.com/Ascend/MindIE-LLM/blob/69e5a5dd4b533eaffc7e198320435350825a36f7/docs/zh/user_guide/feature/anti_outlier.md)）。ModelSlim 的量化流程同时带 `anti_dataset` 与 `calib_dataset` 两组提示词（[vLLM Ascend quantization.md L52–56](https://github.com/vllm-project/vllm-ascend/blob/52d4acfa51fb868823d1070b81cbd2d97e9e4696/docs/source/user_guide/feature_guide/quantization.md#L52-L56)），对应"离群值处理＋校准"两步。

**weight-only 与 W8A8 的区别是激活是否量化**：MindIE W8A16 只量化权重（per-channel，激活保持浮点，[w8a16.md L5](https://github.com/Ascend/MindIE-LLM/blob/69e5a5dd4b533eaffc7e198320435350825a36f7/docs/zh/user_guide/feature/w8a16.md)）；W8A8 权重与激活都量化为 int8，MatMul 直接用量化后的激活×权重计算，再经 quant_bias/deq_scale 反量化（[w8a8.md L33](https://github.com/Ascend/MindIE-LLM/blob/69e5a5dd4b533eaffc7e198320435350825a36f7/docs/zh/user_guide/feature/w8a8.md)）。W8A8 减少 MatMul 计算量，但激活量化正是离群值问题的来源，因此校准/反离群对 W8A8 更关键。

## 格式、kernel、运行 dtype 三层事实与累加精度缺口

读支持矩阵时最容易混淆的是把以下几层当成一层。分层的实证：

1. **量化文件格式（checkpoint 侧）**：GPTQ 用 `quantize_config.json`（[gptq.py L139–140](https://github.com/vllm-project/vllm/blob/b17039bccc17b94a2ea107272ad7bc93508708df/vllm/model_executor/layers/quantization/gptq.py#L139-L140) 的 get_config_filenames）；MindIE 用 `quant_model_description.json` 逐张量标注量化类型与新增张量。格式只说明"这个 checkpoint 是什么量化"，不说明执行时用哪个 kernel。
2. **执行 kernel（运行时选择，条件路径而非平台保证）**：vLLM 启动时 `_verify_quantization` 从 HF `quant_method` 检测方法并按优先级探查 override：bitblas→gptq_marlin_24→gptq_marlin→gptq_bitblas→awq_marlin→ipex→moe_wna16→modelopt→modelopt_fp4→petit_nvfp4→mxfp4→cpu_awq（[vllm/config/model.py L867–905](https://github.com/vllm-project/vllm/blob/b17039bccc17b94a2ea107272ad7bc93508708df/vllm/config/model.py#L867-L905)），未知方法抛 `ValueError`（[L940–948](https://github.com/vllm-project/vllm/blob/b17039bccc17b94a2ea107272ad7bc93508708df/vllm/config/model.py#L940-L948)）。kernel 与格式可以分离，但**分离是有条件的**：4-bit gptq_gemm kernel 有 bug，实现发出警告建议切换 Marlin/BitBLAS（[gptq.py L96–101](https://github.com/vllm-project/vllm/blob/b17039bccc17b94a2ea107272ad7bc93508708df/vllm/model_executor/layers/quantization/gptq.py#L96-L101)）——警告本身不执行切换，gptq_gemm 调用路径仍在（[L379–390](https://github.com/vllm-project/vllm/blob/b17039bccc17b94a2ea107272ad7bc93508708df/vllm/model_executor/layers/quantization/gptq.py#L379-L390)）；gptq_marlin override 还要求兼容性核验与用户选项允许（平台、配置字段、位宽、group size 等，[gptq_marlin.py L215–240、L272–295](https://github.com/vllm-project/vllm/blob/b17039bccc17b94a2ea107272ad7bc93508708df/vllm/model_executor/layers/quantization/gptq_marlin.py#L272-L295)），显式指定 `gptq` 时保留原实现。FP8 的分派同样是条件谓词：use_marlin（weight-only 路径）的置位条件是 capability<89 **或**测试强制开关（VLLM_TEST_FORCE_FP8_MARLIN），随后 ROCm 与 batch invariant 模式会把该标志清除（[fp8.py L315–325](https://github.com/vllm-project/vllm/blob/b17039bccc17b94a2ea107272ad7bc93508708df/vllm/model_executor/layers/quantization/fp8.py#L315-L325)）；AITER 命中由 `rocm_aiter_ops.is_linear_fp8_enabled()` 谓词决定（平台/架构/库存在＋开关，[_aiter_ops.py L37–49、L829–831、L874–882](https://github.com/vllm-project/vllm/blob/b17039bccc17b94a2ea107272ad7bc93508708df/vllm/_aiter_ops.py#L37-L49)）——"ROCm 禁用 Marlin"是已核分支，"ROCm 必然走 AITER"不是：谓词不通过时的路径未核，保持 unknown。MoE all2all 场景 Marlin/AITER 抛 NotImplementedError（[fp8.py L909–911](https://github.com/vllm-project/vllm/blob/b17039bccc17b94a2ea107272ad7bc93508708df/vllm/model_executor/layers/quantization/fp8.py#L909-L911)）。
3. **运行 dtype（参数保存类型与操作数类型）**：MindIE W8A8 对 fp16 源权重产出 input_scale/input_offset 为 fp16、对 bf16 源权重为 bf16（[w8a8.md 表 1/2](https://github.com/Ascend/MindIE-LLM/blob/69e5a5dd4b533eaffc7e198320435350825a36f7/docs/zh/user_guide/feature/w8a8.md)）——这是量化参数的保存类型；vLLM FP8 KV cache 存储时量化、attention 计算用**反量化后的高精度操作数**（[quantized_kvcache.md L20–28](https://github.com/vllm-project/vllm/blob/b17039bccc17b94a2ea107272ad7bc93508708df/docs/features/quantization/quantized_kvcache.md#L20-L28)）；AMD 的 fp8_fnuz 变体在实现中把 KV 的 k/v_scale 乘 2 处理（[kv_cache.py L63–66](https://github.com/vllm-project/vllm/blob/b17039bccc17b94a2ea107272ad7bc93508708df/vllm/model_executor/layers/quantization/kv_cache.py#L63-L66)）；MindIE W8A8 的偏置 quant_bias 保存为 int32 `[n]`、反量化参数 deq_scale 在 fp16 源权重线文档记为 int64、bf16 源权重线记为 fp32（原文口径照录，未复核实现）。
4. **乘加累加精度（accumulation）——本轮无证据，unknown**：上列 int32 偏置、int64/fp32 反量化参数、反量化后的操作数类型，都**不能**推知 MatMul 累加器或 attention 内部累加的精度。各来源文档均未声明累加器 dtype；kernel 本体未读。需要累加精度结论时须另取 kernel 实现证据，不得以参数表示类型替代。

FP8 的两个表示（[quantized_kvcache.md L9–14](https://github.com/vllm-project/vllm/blob/b17039bccc17b94a2ea107272ad7bc93508708df/docs/features/quantization/quantized_kvcache.md#L9-L14)）：E5M2（5 指数 2 尾数）与 E4M3FN（4 指数 3 尾数）。**同快照数值口径冲突（保留不裁定）**：quantized_kvcache.md 写 E4M3 动态范围 ±240（并因此要求 FP32 scale），[fp8.md L10–13](https://github.com/vllm-project/vllm/blob/b17039bccc17b94a2ea107272ad7bc93508708df/docs/features/quantization/fp8.md#L10-L13) 写 E4M3 可存至 ±448——两页数值不同，各自归属其页面，实际范围对应哪种 dtype/平台变体留待格式规范或实现核验。

由此得出读表规则：上游支持矩阵按**实现**分列（同一 W8A8 的 INT8 与 FP8 是不同实现列，支持集不同），且表是文档快照、运行时以 `model_executor/layers/quantization` 实现为准（[quantization README 表注](https://github.com/vllm-project/vllm/blob/b17039bccc17b94a2ea107272ad7bc93508708df/docs/features/quantization/README.md#L67-L70)）。

## 优化开关 ≠ 实际命中

量化与相关优化选项"配置里打开"不等于"数值路径真的变了"或"收益真的拿到"，四层实证：

- **容量收益≠延迟收益（限该快照的 vLLM FP8 KV 实现）**：主要收益是约 2x 的 KV 空间（更长上下文或更大 batch），**没有延迟改善**——因为尚未实现融合的量化 attention，attention 计算仍用反量化后的值；MI300/Hopper+ 的原生格式转换硬件"尚未完全利用"（[quantized_kvcache.md L30–37](https://github.com/vllm-project/vllm/blob/b17039bccc17b94a2ea107272ad7bc93508708df/docs/features/quantization/quantized_kvcache.md#L30-L37)）。此结论不得外推到其他引擎或其他 KV 量化实现。
- **MindIE 的 attention 类量化真正改变 attention 计算路径**：Attention 量化把 q/k/v 量化为 int8 参与 decode attention 计算（fa_quant_type "FAQuant"）；FA3 量化针对 DeepSeek MLA 只量化 k 的非 rope 张量、k rope 不量化（rope 取值变化过大），且必须同时开启 KV Cache NZ 格式（enable_nz）（[fa3_quantization.md L3–13、L86–122](https://github.com/Ascend/MindIE-LLM/blob/69e5a5dd4b533eaffc7e198320435350825a36f7/docs/zh/user_guide/feature/fa3_quantization.md)）。前置条件不满足时该路径不成立。
- **融合类优化把多步计算合并执行；执行路径与内存影响的已核边界按例证分别记录**：AMD Quark 在无原生 OCP MX 硬件的设备（MI325/MI300/MI250）上用**融合 kernel 在线反量化** FP4/FP6→half（[quark.md L271](https://github.com/vllm-project/vllm/blob/b17039bccc17b94a2ea107272ad7bc93508708df/docs/features/quantization/quark.md#L271)）；MindIE 的 EP 有两级实现——ep_level=1 基于 AllGather（[expert_parallel.md L5–7](https://github.com/Ascend/MindIE-LLM/blob/69e5a5dd4b533eaffc7e198320435350825a36f7/docs/zh/user_guide/feature/expert_parallel.md#L5-L7)）、ep_level=2 基于 **AllToAll＋通算融合**（[L9](https://github.com/Ascend/MindIE-LLM/blob/69e5a5dd4b533eaffc7e198320435350825a36f7/docs/zh/user_guide/feature/expert_parallel.md#L9)）——通算融合把通信与计算合并到同一执行路径；专家并行数超过 32 时 DeepSeek-V3/R1 自动使能 Grouped MatMul 融合算子（[L13–14](https://github.com/Ascend/MindIE-LLM/blob/69e5a5dd4b533eaffc7e198320435350825a36f7/docs/zh/user_guide/feature/expert_parallel.md#L13-L14)，模型限定 DeepSeek-V3/R1）。融合的命中判据与 kernel 分派一样是条件路径：从日志/profiling 确认实际执行路径，不从配置推断。
- **图优化的已核边界（执行路径与内存占用）**：vLLM 的图机制分两段——`determine_available_memory` 计算初始可用 KV 内存、无图相关缓冲（[gpu_worker.py L320–343](https://github.com/vllm-project/vllm/blob/b17039bccc17b94a2ea107272ad7bc93508708df/vllm/v1/worker/gpu_worker.py#L320-L343)）；`compile_or_warm_up_model` 在非 `enforce_eager` 时捕获图并取得**实测** `cuda_graph_memory_bytes`，且当未显式指定 `kv_cache_memory_bytes` 而依赖 memory profiling 时，**日志中的 KV cache 配置建议值**会扣除权重＋峰值激活＋非 torch 内存＋实测图内存＋150MiB 经验缓冲（注释原文："memory profiling 可能低估内存消耗，留小缓冲避免 OOM"；[L453–510](https://github.com/vllm-project/vllm/blob/b17039bccc17b94a2ea107272ad7bc93508708df/vllm/v1/worker/gpu_worker.py#L453-L510)）——150MiB 是配置建议的缓冲，不是图内存预留，图内存也不是固定值；`enforce_eager` 是关闭图捕获的开关（[conserving_memory.md L48–75](https://github.com/vllm-project/vllm/blob/b17039bccc17b94a2ea107272ad7bc93508708df/docs/configuration/conserving_memory.md#L48-L75)）。vLLM Ascend 侧：full graph 捕获过多 batch sizes 导致 OOM 或推理挂起的警告在 [vllm_ascend/platform.py L308–326](https://github.com/vllm-project/vllm-ascend/blob/52d4acfa51fb868823d1070b81cbd2d97e9e4696/vllm_ascend/platform.py#L308-L326)；[faqs.md FAQ 14 L152–160](https://github.com/vllm-project/vllm-ascend/blob/52d4acfa51fb868823d1070b81cbd2d97e9e4696/docs/source/faqs.md#L152-L160) 记录 MLA 的 head 比例限制、[FAQ 18 L210–224](https://github.com/vllm-project/vllm-ascend/blob/52d4acfa51fb868823d1070b81cbd2d97e9e4696/docs/source/faqs.md#L210-L224) 记录 capture sizes 的 stream 耗尽（FAQ 13 为一般 OOM/碎片建议，不属图模式）。MindIE 的 Modeling 层经 Compilation 提供 ACLGraph/ATBGraph 两种图模式后端、eager→graph 整图下发执行（[architecture_overview.md L28–31](https://github.com/Ascend/MindIE-LLM/blob/69e5a5dd4b533eaffc7e198320435350825a36f7/docs/zh/developer_guide/architecture_design/architecture_overview.md#L28-L31)，T07-03 已核）。图捕获/重放是否改变数值结果未核（unknown）。**量化×图模式组合未核**：vLLM Ascend 功能矩阵中 Quantization 与 Graph Mode 是两条独立的支持行（[supported_features.md L28–29](https://github.com/vllm-project/vllm-ascend/blob/52d4acfa51fb868823d1070b81cbd2d97e9e4696/docs/source/user_guide/support_matrix/supported_features.md#L28-L29)），不证明组合命中；量化权重在图模式下的执行路径无证据，保持 unknown。

## 支持矩阵：三平台分别核

### vLLM 上游（NVIDIA 主线）

vLLM v0.14.0 的[硬件支持表](https://github.com/vllm-project/vllm/blob/b17039bccc17b94a2ea107272ad7bc93508708df/docs/features/quantization/README.md#L46-L58)按实现逐行转述（✅/❌ 为该快照文档声明）：

- **AWQ**：Volta ❌；Turing/Ampere/Ada/Hopper ✅
- **GPTQ**：Volta–Hopper 全线 ✅（含 Volta，与 AWQ 不同）
- **Marlin（GPTQ/AWQ/FP8）**：Ampere 起才 ✅
- **INT8(W8A8)**：Turing–Hopper＋x86 CPU ✅（Volta ❌）
- **FP8(W8A8)**：仅 Ada/Hopper ✅
- **BitBLAS**：Volta–Hopper ✅；**BitBLAS(GPTQ)**：Ampere 起 ✅（与 BitBLAS 是不同行）
- bitsandbytes、DeepSpeedFP、GGUF：Volta–Hopper 全线；GGUF 的 AMD 列也是 ✅
- **INC(W8A8)**：仅 Intel Gaudi ✅

同快照冲突与实现差异：**INT8 在 SM 7.5（Turing）**——README 表标 Turing 支持，[int8.md L8–9](https://github.com/vllm-project/vllm/blob/b17039bccc17b94a2ea107272ad7bc93508708df/docs/features/quantization/int8.md#L8-L9) 写 "compute capability > 7.5 (Turing, …)"，同一句内严格大于与列举 Turing 自相矛盾；实现侧 awq min capability=75（[awq.py L72–75](https://github.com/vllm-project/vllm/blob/b17039bccc17b94a2ea107272ad7bc93508708df/vllm/model_executor/layers/quantization/awq.py#L72-L75)），gptq min capability=60 但代码注释自标"Need to figure it out"（[gptq.py L133–137](https://github.com/vllm-project/vllm/blob/b17039bccc17b94a2ea107272ad7bc93508708df/vllm/model_executor/layers/quantization/gptq.py#L133-L137)）。SM 7.5 的 INT8 可用性保持 unknown。另 int8 页声明 Blackwell（capability≥100）不支持 INT8、建议 FP8（[int8.md L11–13](https://github.com/vllm-project/vllm/blob/b17039bccc17b94a2ea107272ad7bc93508708df/docs/features/quantization/int8.md#L11-L13)，声明只归属该方法页与该快照）。FP8 文档口径：W8A8 官方支持仅 Hopper＋Ada，Ampere 走 W8A16（weight-only FP8）via Marlin（[fp8.md L3–5](https://github.com/vllm-project/vllm/blob/b17039bccc17b94a2ea107272ad7bc93508708df/docs/features/quantization/fp8.md#L3-L5)）。

### AMD/ROCm

上游表的 AMD GPU 列：**仅 FP8(W8A8) 与 GGUF 标支持**；AWQ、GPTQ、Marlin、INT8(W8A8)、BitBLAS、bitsandbytes、DeepSpeedFP 全部标不支持（同上表）。ROCm 专属补充：

- KV cache dtype 组合：`fp8`/`fp8_e4m3` 支持 CUDA 11.8+ 与 ROCm；**`fp8_e5m2` 仅 CUDA 11.8+，不含 ROCm**（[quantized_kvcache.md L64–68](https://github.com/vllm-project/vllm/blob/b17039bccc17b94a2ea107272ad7bc93508708df/docs/features/quantization/quantized_kvcache.md#L64-L68)）。
- FP8 kernel：ROCm 上 Marlin 被禁用（已核分支）；AITER 命中由谓词决定（见"格式、kernel"节），非平台保证；fp8_fnuz 变体的 scale 处理见运行 dtype 节。
- AMD Quark 工具链：产出 OCP 规范的 MXFP4/MXFP6 模型；MI325/MI300/MI250 无原生 OCP MX 硬件时以融合 kernel 在线反量化 FP4/FP6→half（约 2.5–4x 省内存）；支持逐层混合精度 {MXFP4, FP8}；该页以 MI355 用 MXFP4、MI300 用 FP8 为例说明按设备选精度，并明示激进低精度可能损害精度（[quark.md L259–295](https://github.com/vllm-project/vllm/blob/b17039bccc17b94a2ea107272ad7bc93508708df/docs/features/quantization/quark.md#L259-L295)）——示例不是每台设备的最优部署证明。

### Ascend 线一：vLLM Ascend v0.14.0rc1

功能矩阵把 Quantization 标为 Functional："W8A8 available; working on more quantization method support (W4A8, etc)"（[supported_features.md L28](https://github.com/vllm-project/vllm-ascend/blob/52d4acfa51fb868823d1070b81cbd2d97e9e4696/docs/source/user_guide/support_matrix/supported_features.md#L28)）。配套口径：

- 量化工具二选一：**ModelSlim**（昇腾方向，推荐）与 **LLM-Compressor**（支持 W8A8/W8A8_DYNAMIC）。运行开关不同——ModelSlim 产物须 `--quantization ascend`，LLM-Compressor 产物**不加**该参数（[quantization.md L103–107](https://github.com/vllm-project/vllm-ascend/blob/52d4acfa51fb868823d1070b81cbd2d97e9e4696/docs/source/user_guide/feature_guide/quantization.md#L103-L107)）。
- 模型级 W8A8 列（文本模型表 [supported_models.md L17–28](https://github.com/vllm-project/vllm-ascend/blob/52d4acfa51fb868823d1070b81cbd2d97e9e4696/docs/source/user_guide/support_matrix/supported_models.md#L17-L28)；多模态表 [L77–81](https://github.com/vllm-project/vllm-ascend/blob/52d4acfa51fb868823d1070b81cbd2d97e9e4696/docs/source/user_guide/support_matrix/supported_models.md#L77-L81)）：DeepSeek V3/3.1、V3.2、R1、Qwen3、Qwen3-Moe、Qwen3-Next、Qwen2.5、GLM-4.x、Qwen2.5-VL 标 ✅；**Qwen3-Coder、Kimi-K2-Thinking、Qwen3-VL、Qwen3-VL-MOE 的 W8A8 列为空白**——空白是未标注，不能推断支持也不能推断不支持，保持 unknown。硬件列 A2/A3。

### Ascend 线二：MindIE（文档线 3.1.0）

MindIE 文档把量化方式连同硬件/模型/配伍约束逐项声明（各页 NOTE 节；"未声明"不是"通用"，保持 unknown）：

| 方式 | 硬件（该页声明） | 模型限定 | 配伍限定 | 源权重/运行口径 |
|---|---|---|---|---|
| W8A8 | 该页未声明 | 该页未声明 | 可配 Anti-Outlier；SP/CP 布局对量化权重的限定见[分布式布局](distributed-inference-layouts.md)（该约束另有跨页冲突） | fp16/bf16 源权重均可量化；产物激活 scale per-tensor |
| W8A16 | 仅 A2 | 仅 LLaMA3-70B、Qwen1.5-110B、Qwen2-72B | 声明仅与 Anti-Outlier、KV Cache int8 配合 | fp16/bf16 均可；权重 per-channel |
| KV Cache int8 | 仅 A2 | 仅 LLaMA3.1-70B、Qwen2-72B、Qwen2.5-72B-Instruct | **声明仅搭配 W8A8** | 仅 float16 |
| Attention 量化 | 仅 A2 | 仅 LLaMA3.1-70B | 仅搭配 W8A8；仅与长序列、Function Call 同用 | 源权重 fp16/bf16；per-head scale |
| FA3 量化 | A2＋A3 | 仅 DeepSeek R1/V3/R1-0528 | 支持配 W8A8；必须开 KV Cache NZ | 仅 float16 |
| W4A8 混合 | 该页未声明 | 仅 DeepSeek-R1/V3 | 仅支持 Anti-Outlier；暂不支持配 KV Cache int8 | fp16/bf16 源权重均可；路由专家 per-channel＋per-group |
| W8A8SC 稀疏 | 仅 300I Duo | 仅 Qwen3-8B/14B/32B | 仅与并行解码、Prefix Cache、Function Call、长序列同用 | bf16 不支持 |
| W16A16SC 浮点稀疏 | 仅 300I Duo | 仅 Qwen3-32B | 该页未声明 | 该页未声明 |

上表"源权重/运行口径"列混合了三类信息：可量化的源权重类型（如 W8A8 的 fp16/bf16）、产物的参数布局、以及运行限制（如 KV Cache int8 的"仅 float16"是该页 NOTE 的运行限定）。三者不互推，交叉组合未核的保持 unknown。

**文档间冲突（保留不裁定）**：kv_cache_int8.md 写 KV Cache int8 "仅支持搭配W8A8使用"（[L10](https://github.com/Ascend/MindIE-LLM/blob/69e5a5dd4b533eaffc7e198320435350825a36f7/docs/zh/user_guide/feature/kv_cache_int8.md#L10)），而 w8a16.md 写 W8A16 "仅支持和Anti-Outlier离群值处理、KV Cache int8量化配合使用"（[L11](https://github.com/Ascend/MindIE-LLM/blob/69e5a5dd4b533eaffc7e198320435350825a36f7/docs/zh/user_guide/feature/w8a16.md#L11)）——**KV Cache int8 可否配 W8A16，两页声明相反**。本文按两说并存处理：该组合保持 unknown，需 msModelSlim 实测或后续版本文档裁定。生成工具均为 msModelSlim（`msmodelslim quant --device npu --quant_type …`，[入口登记](../../sources/registry.yaml)），工具实现未核。

## 输出质量如何验证

量化改变数值语义：精度差异的判定纪律（容差、固定开关、排除合法数值噪声）见[静默错误与计算完整性判定](../08-reliability/silent-errors-and-integrity.md)与[GPU→NPU 精度差异诊断](../06-training/gpu-npu-precision-difference-triage.md)。引擎层证据：

- **固定任务的基准对照**：vLLM INT8 方法页把"评估精度"列为量化流程第四步，示例用 `lm_eval` 跑 gsm8k（[int8.md L117–136](https://github.com/vllm-project/vllm/blob/b17039bccc17b94a2ea107272ad7bc93508708df/docs/features/quantization/int8.md#L117-L136)）。评估任务、指标、baseline（未量化模型同任务结果）与样本量都要固定；"跑过基准"不等于"质量达标"，阈值是业务约定。
- **昇腾侧评估指南（四份均已全文取回；命令参数未逐字核）**：[lm-eval](https://github.com/vllm-project/vllm-ascend/blob/52d4acfa51fb868823d1070b81cbd2d97e9e4696/docs/source/developer_guide/evaluation/using_lm_eval.md) 有在线服务（L5 起）与离线（L135 起）两种评估路径；[EvalScope](https://github.com/vllm-project/vllm-ascend/blob/52d4acfa51fb868823d1070b81cbd2d97e9e4696/docs/source/developer_guide/evaluation/using_evalscope.md) 为服务/API 评估（L66–77）；[OpenCompass](https://github.com/vllm-project/vllm-ascend/blob/52d4acfa51fb868823d1070b81cbd2d97e9e4696/docs/source/developer_guide/evaluation/using_opencompass.md) 经 OpenAI SDK 连服务评估（L90–106）；[AISBench](https://github.com/vllm-project/vllm-ascend/blob/52d4acfa51fb868823d1070b81cbd2d97e9e4696/docs/source/developer_guide/evaluation/using_ais_bench.md) 为服务评估路径（L153–201）。四份不是同一结构，选用时按各指南实际覆盖的路径。
- **质量声明的归属**：vLLM KV cache 文档称 FP8 E4M3 量化"通常只最小限度降低推理精度"（[quantized_kvcache.md L39](https://github.com/vllm-project/vllm/blob/b17039bccc17b94a2ea107272ad7bc93508708df/docs/features/quantization/quantized_kvcache.md#L39)）——这是引擎文档对研究的概括，所指研究未独立核对，本库未复现。论文自身的质量结论同样只作作者报告。
- **产出侧指标不能替代质量**：吞吐/TTFT 正常不证明输出正确；质量结论必须来自输出本身的评估。质量与性能的联合验收（本库方法建议）：容量型优化（KV 量化、稀疏压缩）以"质量不降＋容量/吞吐提升"为判据，延迟型优化（attention 类量化、融合）以"质量不降＋延迟改善"为判据——收益类型要与优化机制对得上（见"优化开关≠实际命中"节）。

## 量化相关故障的三层归因与回退

| 层 | 典型现象 | 证据方向 |
|---|---|---|
| 初始化/配置 | 启动报 `ValueError`（未知 quant_method、不支持组合）、MindIE 量化描述与实际 checkpoint 不符 | `_verify_quantization` 的方法检测与 override 顺序（L867–905）、未知方法校验（L940–948）；quant_model_description.json 与权重文件是否一致；[权重加载与启动失败](model-loading-and-readiness.md)的加载链分层 |
| 算子/执行 | 算子/内核错误、显存异常、性能未达预期 | 该量化实现对该硬件的支持状态（三平台矩阵分别核）；kernel 实际分派（条件谓词，从日志取证）；执行层错误按[算子/图编译流程](../02-software-stack/ascend-op-graph-failure-triage.md)与 [OOM 流程](ascend-inference-oom-triage.md)分层 |
| 精度 | 输出质量下降、发散、异常 token | 固定任务评估对照＋数值纪律；区分采样变化与计算差异；与静默错误、dtype/KV 精度配置差异区分 |

回退路径按层选择（本库方法建议，非引擎保障）：配置层回退是改回被支持的组合（或基线 dtype）；算子层回退**候选**包括 kernel 分派的条件路径——FP8 在无 FP8 硬件支持时可落 Marlin weight-only、ROCm 上 Marlin 被禁用后 AITER 是条件谓词允许的候选、GPTQ 4-bit 在满足 override 条件时可选 gptq_marlin/gptq_bitblas（警告建议但非自动保证，显式指定 gptq 时保留原实现）——是否实际命中须从日志/profiling 确认；精度层回退是恢复 BF16/FP16 基线后逐个重新启用单变量量化项，对照质量与性能两栏记录。每一层的回退判据都应预先写下，不以其"配置成功"代替"质量与性能共同验收"。

## 常见误解

- **"上游支持 = 昇腾支持"**：上游硬件表不含 NPU；Ascend 支持分 vLLM Ascend 与 MindIE 两线各自声明。
- **"W8A8 就是 W8A8"**：INT8 与 FP8 的 W8A8 是不同实现；MindIE 的 W8A8 还有 static/dynamic、per-tensor 激活 scale 等变体。
- **"量化只影响精度"**：量化改变内存（权重、KV）、kernel 路径与故障形态；该快照 vLLM 的 FP8 KV 量化是容量优化不是延迟优化。
- **"开了优化选项就是命中了"**：kernel 分派与融合命中由条件谓词决定，attention 类量化有硬前提（NZ 格式等）；命中与否从实际执行路径取证。
- **"参数表里的 dtype 就是计算精度"**：偏置/反量化参数的保存类型不等于累加器精度；累加精度未证。
- **"基准跑通 = 质量达标"**：跑通只证明流程可执行；达标阈值是业务/模型约定。
- **"报错在量化配置 = 根因在量化"**：执行期错误可能来自算子、内存或图路径，按层归因。

## 来源与待确认问题

- vLLM v0.14.0：[量化文档目录](https://github.com/vllm-project/vllm/tree/b17039bccc17b94a2ea107272ad7bc93508708df/docs/features/quantization)（README/int8/fp8/quantized_kvcache/quark/auto_awq/gptqmodel）、[vllm/config/model.py](https://github.com/vllm-project/vllm/blob/b17039bccc17b94a2ea107272ad7bc93508708df/vllm/config/model.py)、[model_executor/layers/quantization](https://github.com/vllm-project/vllm/tree/b17039bccc17b94a2ea107272ad7bc93508708df/vllm/model_executor/layers/quantization)（awq/gptq/fp8/kv_cache/gptq_marlin）、[_aiter_ops.py](https://github.com/vllm-project/vllm/blob/b17039bccc17b94a2ea107272ad7bc93508708df/vllm/_aiter_ops.py)。
- vLLM Ascend v0.14.0rc1：[quantization 指南](https://github.com/vllm-project/vllm-ascend/blob/52d4acfa51fb868823d1070b81cbd2d97e9e4696/docs/source/user_guide/feature_guide/quantization.md)、[支持矩阵](https://github.com/vllm-project/vllm-ascend/blob/52d4acfa51fb868823d1070b81cbd2d97e9e4696/docs/source/user_guide/support_matrix/supported_models.md)、[评估指南四份](https://github.com/vllm-project/vllm-ascend/tree/52d4acfa51fb868823d1070b81cbd2d97e9e4696/docs/source/developer_guide/evaluation)。
- MindIE-LLM@69e5a5dd：[feature/ 量化特性页](https://github.com/Ascend/MindIE-LLM/tree/69e5a5dd4b533eaffc7e198320435350825a36f7/docs/zh/user_guide/feature)（w8a8/w8a16/w8a8sc/w16a16sc/w4a8/kv_cache_int8/attention_quantization/fa3_quantization/anti_outlier）、[expert_parallel.md](https://github.com/Ascend/MindIE-LLM/blob/69e5a5dd4b533eaffc7e198320435350825a36f7/docs/zh/user_guide/feature/expert_parallel.md)。
- 论文：[AWQ](https://arxiv.org/abs/2306.00978)、[GPTQ](https://arxiv.org/abs/2210.17323)、[SmoothQuant](https://arxiv.org/abs/2211.10438)（摘要级）。
- 逐条主张与证据定位见[第二十七批量化来源记录](../../docs/research/batch-27-t07-04-sources.md)（含初审修订轮）。
- 待确认：乘加累加精度（MatMul/attention 累加器 dtype）；INT8 在 SM 7.5 的文档冲突与 kernel/runtime 条件；E4M3 动态范围两页 ±240/±448 冲突；MindIE KV Cache int8×W8A16 配伍冲突；MindIE w8a8.md 表 1 deq_scale dtype int64 的实现复核；msModelSlim 校准/反离群算法实现（msit 仓未核）；AITER 谓词不通过时 FP8 在 ROCm 的实际路径；Quark 混合精度在 vLLM 的加载路径；量化与图模式的组合执行路径；GPTQ 算法细节（OBS 渊源/逐行补偿）超出摘要级的取证。以上未核组合均保持 unknown。
