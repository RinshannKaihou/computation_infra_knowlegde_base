# 第二十七批 T07-04 来源记录

任务：T07-04（补齐量化、算子优化与支持冲突边界；**revise** 既有 `knowledge/07-inference/quantization-and-quality.md`，主题 07.4）。取证轮次：主会话作者角色首轮（2026-10-21；前置 Batch 26 的 T07-02/T07-03 已交付并审阅闭环）。本轮目标：把原文"存在性核对"升级为全文/实现级证据，建立机制—格式—kernel—运行 dtype 的分层口径与三平台支持矩阵。

版本线（沿用既有钉扎，不新选版本）：vLLM **v0.14.0**＝commit `b17039bccc17b94a2ea107272ad7bc93508708df`（src.vllm.inference-v0-14）；vLLM Ascend **v0.14.0rc1**＝commit `52d4acfa51fb868823d1070b81cbd2d97e9e4696`（src.ascend.vllm-ascend-v0-14-0rc1）；MindIE-LLM＝master@`69e5a5dd4b533eaffc7e198320435350825a36f7`（文档线 3.1.0，src.ascend.mindie-llm-docs-69e5a5dd）。本轮未运行任何引擎或量化工具。

## 本轮取回清单（2026-10-21，均为固定 commit 原文件；SHA-256 前 16 位）

vLLM Ascend @52d4acfa：

| 文件 | SHA-256 前 16 位 |
|---|---|
| docs/source/user_guide/feature_guide/quantization.md（164 行） | 85e988fa0eaf9a6d |
| docs/source/user_guide/support_matrix/supported_features.md（48 行） | 9c576fc4063ad971 |
| docs/source/user_guide/support_matrix/supported_models.md（108 行） | 8f8a02d898d993cf |
| docs/source/developer_guide/evaluation/using_lm_eval.md（307 行） | 29da7eb7d0c595e3 |
| docs/source/developer_guide/evaluation/using_evalscope.md（176 行） | 8e8eaf625027a233 |
| docs/source/developer_guide/evaluation/using_ais_bench.md（327 行） | 19c3087e40c30cb5 |
| docs/source/developer_guide/evaluation/using_opencompass.md（126 行） | 13a4b8c035e3c673 |

vLLM @b17039bc：

| 文件 | SHA-256 前 16 位 |
|---|---|
| docs/features/quantization/README.md（70 行） | acab44330aafa446 |
| docs/features/quantization/quantized_kvcache.md（162 行） | 008f9addad3a5270 |
| docs/features/quantization/int8.md（150 行） | 2d0c66123da0334c |
| docs/features/quantization/fp8.md（142 行） | 00567a20882d6a68 |
| docs/features/quantization/auto_awq.md（82 行） | 980326181102bfe3 |
| docs/features/quantization/gptqmodel.md（99 行） | 9615e9cac9ac678d |
| docs/features/quantization/quark.md（316 行） | 50aa3efcc756dec8 |
| vllm/model_executor/layers/quantization/kv_cache.py（153 行） | 63f7e5b4ddddebc4 |
| vllm/model_executor/layers/quantization/awq.py（277 行） | 9dd02ea1a265248d |
| vllm/model_executor/layers/quantization/gptq.py（393 行） | 66eb332cc2f83a0e |
| vllm/model_executor/layers/quantization/fp8.py（1224 行） | bc1d30059e0f3123 |
| vllm/config/model.py（2026 行） | bb8a629254b756f0 |

MindIE-LLM @69e5a5dd（docs/zh/user_guide/ 下）：

| 文件 | SHA-256 前 16 位 |
|---|---|
| feature/w8a8.md（73 行） | acf67cd05ce9d8e8 |
| feature/w8a8sc.md（137 行） | 3823dba7b57a84d8 |
| feature/w8a16.md（61 行） | 79ca638da635e84b |
| feature/w4a8_mixed_precision_quantization.md（71 行） | 39023b486eb6dc16 |
| feature/w16a16sc.md（135 行） | 2d5475dc4a490d29 |
| feature/kv_cache_int8.md（62 行） | df13bb44dc5a41fb |
| feature/attention_quantization.md（85 行） | 984dbbde852c09f9 |
| feature/fa3_quantization.md（129 行） | 3b035f3b369e8ada |
| feature/anti_outlier.md（82 行） | 08870af9ba936dd5 |
| optimization_and_tuning.md（192 行） | 0c348668366760a0 |

论文（abs 页读取，仅摘要级）：arXiv:2306.00978v6（AWQ，2026-04-25 最新版）、arXiv:2210.17323v2（GPTQ，2023-03-22）、arXiv:2211.10438v7（SmoothQuant，2024-03-29）。

## 主张—来源定位表

### 机制层（论文＋引擎文档）

| 主张 | 登记 ID | 精确位置 | 支持范围 / 未覆盖 |
|---|---|---|---|
| AWQ：激活感知的 weight-only 量化——按离线激活统计识别显著通道（约 1%），对显著权重通道做等效缩放降低量化误差，不混合精度、不反传；per-channel 缩放粒度 | NEW src.arxiv.awq-2306.00978 | abs 页摘要（v6） | 机制解释；论文实验数字（3x 加速等）属作者报告，本库未复现 |
| GPTQ：基于近似二阶信息（OBS 框架启发）的一次性逐层量化——逐行量化权重并用剩余未量化权重补偿已量化误差；2/3/4/8-bit | NEW src.arxiv.gptq-2210.17323；扩展 src.vllm.inference-v0-14 | abs 页摘要（v2）；gptq.py L92–94（非 2/3/4/8 bit 抛 ValueError） | 机制与实现位宽校验；175B/4GPU 小时等数字为作者报告 |
| SmoothQuant：激活离群点使 W8A8 难量化——通过数学等效变换把量化难度从激活迁移到权重（离线平滑），训练无关 PTQ | NEW src.arxiv.smoothquant-2211.10438 | abs 页摘要（v7） | 机制；1.56x/2x 为作者报告 |
| MindIE 侧离群值处理：Anti-Outlier 抑制激活离群点拉大 scale 造成的精度损失；非对称算法引入 norm_bias（Norm 层加、Linear 层减以保等价）；per-tensor 场景融合进 quant_bias、per-token 场景体现为普通 bias（原 Linear 有 bias 直接融合如 Qwen2，无则新建如 Qwen3-32B）；可配合 W4A8/W8A8/W8A8C8 | 扩展 src.ascend.mindie-llm-docs-69e5a5dd | anti_outlier.md（特性简介/执行逻辑节 L31–51） | 文档口径；未实测 |
| MindIE W8A8 产物结构与运行语义：`quant_model_description.json` 逐张量标注；MatMul 新增 input_scale/input_offset（激活量化，**shape [1]＝per-tensor**）、quant_bias（int32 [n]）、deq_scale（fp16 权重线 dtype int64 / bf16 权重线 fp32——按文档表 1/2 原文记录）；fp16 与 bf16 源权重均支持 | 扩展 src.ascend.mindie-llm-docs-69e5a5dd | w8a8.md（简介节 L21–52 表 1/2） | 文档口径的格式与 dtype/shape；deq_scale int64 为原文表述未复核实现 |
| MindIE W8A16：weight-only 8bit、**per-channel**（weight_scale/offset [n,1]、dtype float32）；仅 A2；仅 LLaMA3-70B、Qwen1.5-110B、Qwen2-72B | 扩展 src.ascend.mindie-llm-docs-69e5a5dd | w8a16.md（简介 NOTE 节 L7–11、表 1/2 L46–58） | 文档声明集合 |
| MindIE W4A8 混合量化（仅 DeepSeek-R1/V3）：前三层 MLP＝W8A8 Dynamic、MLA 与共享专家＝W8A8、路由专家＝W4A8 Dynamic（权重 per-channel＋per-group 4bit、激活 8bit；weight_scale [n,1]＋weight_scale_second [n,group_num]）；仅支持 Anti-Outlier、**暂不支持 KV Cache int8 配合** | 扩展 src.ascend.mindie-llm-docs-69e5a5dd | w4a8_mixed_precision_quantization.md（简介 L5–11、表 1/2） | 文档声明；表 2 出现"bfloat32"为原文笔误口径照录 |
| MindIE 稀疏量化族：W8A8S（稀疏＋量化）→W8A8SC（再压缩，part0-3-of-4 分片、TP 须与运行一致）；压缩算法硬件强相关**仅 300I Duo**、bf16 不支持、仅 Qwen3-8B/14B/32B、仅与并行解码/Prefix Cache/Function Call/长序列同用；W16A16SC 浮点稀疏（16bit 计算＋稀疏压缩）同样仅 300I Duo、仅 Qwen3-32B，index＋outdim 复原 | 扩展 src.ascend.mindie-llm-docs-69e5a5dd | w8a8sc.md（NOTE L11–16、前提/生成/执行节）；w16a16sc.md（NOTE L10–12、生成/执行节） | 文档声明集合 |

### 支持矩阵与冲突（三平台分别取证）

| 主张 | 登记 ID | 精确位置 | 支持范围 / 未覆盖 |
|---|---|---|---|
| vLLM v0.14.0 量化 README 硬件表（实现×硬件）：**AMD GPU 列**仅 FP8(W8A8) 与 GGUF 为 ✅，AWQ/GPTQ/Marlin/INT8(W8A8)/BitBLAS/bnb/DeepSpeedFP 全 ❌；INC(W8A8) 仅 Intel Gaudi ✅；表注自述随版本变化、以 model_executor/layers/quantization 实现为准 | 扩展 src.vllm.inference-v0-14 | quantization/README.md L46–70（表＋脚注） | 该快照文档表；不外推其他版本 |
| 运行时方法检测与 override 顺序：`_verify_quantization` 从 HF quant_method 检测，override 依次探查 bitblas→gptq_marlin_24→gptq_marlin→gptq_bitblas→awq_marlin→ipex→moe_wna16→modelopt→modelopt_fp4→petit_nvfp4→mxfp4→cpu_awq（重量级后端排最后避免不必要 import），未知方法 ValueError | 扩展 src.vllm.inference-v0-14 | vllm/config/model.py L867–905（L880–897 override 清单） | 启动期配置校验路径 |
| AWQ 实现 kernel 门控：`get_min_capability`＝75（代码注释"AWQ kernel only supports Turing or newer"） | 扩展 src.vllm.inference-v0-14 | awq.py L72–75 | min capability 口径；README 表 Turing ✅ 与之相容 |
| GPTQ 实现：min capability＝60（代码内注释"Need to figure it out"，该值自身标注未定）；**4-bit gptq_gemm kernel 有 bug，警告默认切 gptq_marlin/gptq_bitblas**——即 GPTQ 格式（checkpoint）与实际执行 kernel（Marlin 族）分离的实证 | 扩展 src.vllm.inference-v0-14 | gptq.py L96–101（警告）、L133–137（min capability） | 已核路径 |
| FP8 实现的 kernel 分派：capability<89（无 FP8 硬件支持）→ Marlin weight-only FP8；**ROCm 上禁用 Marlin**；ROCm 走 AITER（`rocm_aiter_ops.is_linear_fp8_enabled`）；MoE all2all 场景 Marlin/AITER 抛 NotImplementedError | 扩展 src.vllm.inference-v0-14 | fp8.py L314–321（marlin 门控＋ROCm 禁用）、L325（aiter）、L909–911（all2all 限制） | kernel 选择逻辑；各 kernel 数值行为未核 |
| FP8 文档口径：W8A8 官方支持仅 Hopper＋Ada；Ampere 走 W8A16（weight-only FP8）via Marlin；NVIDIA FP8 计算要求 capability>8.9；硬件加速示例 H100 与 AMD MI300x | 扩展 src.vllm.inference-v0-14 | fp8.md L3–16 | 文档声明 |
| AMD Quark（ROCm 量化工具链）：产出 OCP 规范 MXFP4/MXFP6 模型；MI325/MI300/MI250 无原生 OCP MX 硬件时用融合 kernel 在线反量化 FP4/FP6→half（约 2.5–4x 省内存 vs fp16/bf16）；支持逐层混合精度 {MXFP4, FP8}；官方建议按设备选最低精度（MI355 MXFP4、MI300 FP8）并警告激进低精度伤精度 | 扩展 src.vllm.inference-v0-14 | quark.md L259–295（MXFP4/MXFP6、混合精度节） | vLLM 页面对 Quark 的集成口径；quark.docs.amd.com 未逐页核 |
| KV cache 量化 dtype×平台：`kv_cache_dtype="fp8"/"fp8_e4m3"`＝CUDA 11.8+ **与 ROCm**；`"fp8_e5m2"`＝**仅 CUDA 11.8+（不含 ROCm）**；E4M3 动态范围 ±240 需 FP32 scale；当前仅 per-tensor scale；存储量化、attention 计算用反量化后的值（无融合量化 attention，暂无延迟收益）；MI300/Hopper+ 有原生格式转换硬件但未完全利用 | 扩展 src.vllm.inference-v0-14 | quantized_kvcache.md L9–18（格式/限制）、L20–37（流程/性能）、L64–68（dtype 支持行） | 文档声明 |
| KV cache scale 语义（实现）：dtype="auto" 时 k/v_scale 强制 1.0（忽略 checkpoint scale）；优先用分离 k_scale/v_scale，单一 kv_scale 会被重映射复制；**fp8_fnuz 平台（AMD 变体）k/v_scale×2**；calculate_kv_scales=True 可在线计算 | 扩展 src.vllm.inference-v0-14 | kv_cache.py L55–75 | 已核路径 |
| vLLM Ascend 工具链与运行开关：量化工具二选一——ModelSlim（推荐；gitcode Ascend/msit，示例钉 `br_release_MindStudio_8.3.0_20261231` 分支；quant 脚本带 anti_dataset＋calib_dataset、多卡 ASCEND_RT_VISIBLE_DEVICES、PYTORCH_NPU_ALLOC_CONF=expandable_segments:False）与 LLM-Compressor（pip 安装，支持 W8A8/W8A8_DYNAMIC）；**ModelSlim 产物须 `--quantization ascend`，LLM-Compressor 产物不加该参数**；官方预量化样例 ModelScope vllm-ascend/Kimi-K2-Instruct-W8A8；命令页自注"for reference only" | 扩展 src.ascend.vllm-ascend-v0-14-0rc1 | quantization.md 全文（L13–107 工具/运行节） | 文档口径；命令未运行 |
| vLLM Ascend 模型级 W8A8 列（supported_models.md 核心表）：DeepSeek V3/3.1、V3.2、R1、Qwen3、Qwen3-Moe、Qwen3-Next、Qwen2.5、GLM-4.x、Qwen2.5-VL 标 ✅；Qwen3-Coder、Kimi-K2-Thinking、Qwen3-VL、Qwen3-VL-MOE 该列为**空白**（未标注＝不可推断）；硬件列 A2/A3；页首指向 issue #1608 取最新 | 扩展 src.ascend.vllm-ascend-v0-14-0rc1 | supported_models.md L17–28（核心表 W8A8 列）、L3–9（图例） | 该快照矩阵；空白格保持 unknown |
| vLLM Ascend 评估指南四份（先前仅确认目录存在，本轮全文取回）：lm-eval / EvalScope / AISBench / OpenCompass，统一结构＝docker 起 vllm-ascend 服务（`/dev/davinciN` 设备、quay.io/ascend/vllm-ascend 镜像、substitutions 版本占位）＋在线服务/离线两路径做精度测试 | 扩展 src.ascend.vllm-ascend-v0-14-0rc1 | using_lm_eval.md L1–30、using_evalscope.md L1–30、using_ais_bench.md L1–30、using_opencompass.md L1–30（各文件后半命令细节供 T07-05 展开） | 结构与工具范围；具体命令参数未逐字核 |
| MindIE KV Cache int8：**仅 A2；仅搭配 W8A8；仅 LLaMA3.1-70B、Qwen2-72B、Qwen2.5-72B-Instruct；仅 float16**；新增 kv_cache_type "C8" 与 k/v_proj 的 kv_cache_scale/offset（shape [kv_head_num×kv_head_dim]＝按 KV 头维度粒度），推理时推导 4 组 quant/dequant scale/offset，PagedAttention 输出反量化 | 扩展 src.ascend.mindie-llm-docs-69e5a5dd | kv_cache_int8.md（NOTE L7–12、简介 L28–45、表 1/2） | 文档声明集合 |
| **文档间冲突（保留不裁定）**：kv_cache_int8.md NOTE 写"仅支持搭配W8A8使用"，而 w8a16.md NOTE 写 W8A16"仅支持和Anti-Outlier离群值处理、KV Cache int8量化配合使用"——KV Cache int8 可否配 W8A16 两页声明相反；正文按"两说并存、组合保持 unknown、需 msModelSlim 实测或后续版本文档裁定"处理 | 扩展 src.ascend.mindie-llm-docs-69e5a5dd | kv_cache_int8.md L10 vs w8a16.md L11 | 冲突记录；不合成一致口径 |
| MindIE Attention 量化：q/k/v 量化 8bit 优化 decode attention；fa_quant_type "FAQuant"；per-head scale（[q_head_num,head_dim]/[kv_head_num,head_dim]）；**仅 A2、仅 W8A8 配合、仅 LLaMA3.1-70B、仅与长序列/Function Call 同用** | 扩展 src.ascend.mindie-llm-docs-69e5a5dd | attention_quantization.md（NOTE L7–12、简介 L28–59、表 1/2） | 文档声明集合 |
| MindIE FA3 量化（DeepSeek MLA）：k 的非 rope 张量量化 8bit、**k rope 不量化**（rope 取值变化过大）；perhead；fa_quant_type "FAKQuant"；**A2＋A3**、支持 W8A8 配合、仅 DeepSeek R1/V3/R1-0528、仅 float16、**必须开 KV Cache NZ 格式**（纯模型 atb_llm conf enable_nz / 服务化 ModelConfig→models.deepseekv2.kv_cache_options.enable_nz；PD 分离同样要求）；生成走 msmodelslim example quant_deepseek_w8a8.py --fa_quant --mindie_format | 扩展 src.ascend.mindie-llm-docs-69e5a5dd | fa3_quantization.md（简介 L3–13、生成 L74–84、执行 L86–122） | 文档声明集合 |
| MindIE 量化×并行组合约束：SP（KV Cache 切分）与 CP（上下文并行，切分数仅 2、须与 SP 同用）**当前仅 DeepSeek-V3/R1/V3.1 的 W8A8 量化权重支持**（该约束同时是 T07-06 布局证据）；EP 两级（ep_level 1=AllGather、2=AllToAll＋通算融合，ep_level=2 时 moe_tp 只能 1）；DP 暂不支持与 CP 叠加 | 扩展 src.ascend.mindie-llm-docs-69e5a5dd | optimization_and_tuning.md L111–119（SP）、L136–145（CP）、L161–191（EP）、L88–95（DP） | 服务化配置口径；未实测 |

## unknown 清单

1. 各 MindIE 量化方式的 msModelSlim 实际实现（校准算法、anti-outlier 算法细节）未核——msit 仓未取回，仅登记入口；文档口径照录。
2. vLLM Ascend `--quantization ascend` 在插件内的实现路径（supported_quantization＝ASCEND_QUANTIZATION_METHOD 等，T07-02 已有 platform.py 层证据）与 W4A8 在研状态无进一步材料。
3. AMD AITER/DeepGEMM kernel 的数值行为与 MI250/MI300 实际可用组合未核（fp8.py 门控逻辑已核，kernel 本体未读）。
4. Quark 工具文档站（quark.docs.amd.com）未逐页取回；MXFP4 混合精度在 vLLM 的加载路径未核。
5. MindIE w8a8.md 表 1 deq_scale dtype int64、w4a8 表 2 "bfloat32" 等原文异常值照录，未从实现复核（MindIE-LLM src/ 量化加载实现未逐行核）。
6. vLLM Ascend 评估指南四份的后半命令细节（数据集参数、离线路径）未逐字核——留待 T07-05 需要时展开。
7. 未运行任何量化、推理或评估命令；全部为文档/源码/论文摘要口径，无本库实测结果。

## 集成轮结果（2026-10-21 已执行）

- 新登记 4 项：src.arxiv.awq-2306.00978、src.arxiv.gptq-2210.17323、src.arxiv.smoothquant-2211.10438（论文，abs 页摘要级，arXiv non-exclusive license 口径）＋ src.ascend.msmodelslim-msit（ModelSlim 工具仓入口，未固定 commit）。
- 扩展 3 项 notes：src.vllm.inference-v0-14（量化 README 表/kvcache/fp8/quark/auto_awq/gptqmodel 页＋awq/gptq/fp8/kv_cache/config.model 实现）、src.ascend.vllm-ascend-v0-14-0rc1（quantization.md/supported_models.md/评估指南四份）、src.ascend.mindie-llm-docs-69e5a5dd（量化特性 9 页＋optimization_and_tuning）。
- registry 538→542；T07-04 正文进入撰写轮。
