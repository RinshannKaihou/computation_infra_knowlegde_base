# 第十一批来源记录：推理量化与输出质量（R2-12）

**2026-10-08 修订注记：** Codex `gpt-6.1-sol / xhigh` 按 B11-C04/C05 修正本记录并完成[定向复核](batch-10-11-12-codex-recheck.md)。下述原研究者、首次获取方式与当时任务状态为历史；修订补读和保留的未知条件见本记录及复核报告。

研究日期：2026-09-30（子代理首次尝试超时两次）至 2026-10-08（主任务直接定向取证）。目标正文：`knowledge/07-inference/quantization-and-quality.md`（concept）。取证经 `gh api` 按固定 commit 原文件进行；未运行任何推理或评估。

## 主张—证据表

| 主张 | 证据位置 | 版本 | 类型 | 反证/未知 |
|---|---|---|---|---|
| vLLM 量化定义：“trades off model precision for smaller memory footprint”；文档目录 14 个方法页 + README（auto_awq、auto_round、bitblas、bnb、fp8、gguf、gptqmodel、inc、int4、int8、modelopt、quantized_kvcache、quark、torchao） | docs/features/quantization/README.md（vLLM v0.14.0，commit b17039bc） | v0.14.0 | 固定文档 | 代查修正：此前误写 15 |
| 硬件支持表按实现×硬件给出支持矩阵（如 INT8 W8A8：Turing/Ampere/Ada/Hopper + x86 CPU，Volta/AMD GPU/Intel GPU/Gaudi 不支持；FP8 W8A8：Ada/Hopper + AMD GPU）；表注：“subject to change”，最新以 model_executor/layers/quantization 为准；目录为 14 个方法页 + README（代查修正：此前误写 15） | 同上 README 的 Supported Hardware 表与注释 | 同上 | 固定文档 | 矩阵不含 NPU；NPU 支持不能从上游表推断 |
| INT8 W8A8 页写 compute capability >7.5，但同句列 Turing；README 又将 Turing（SM 7.5）标为支持，存在文档冲突。该方法页对 Blackwell 写 >=100 不支持并建议 FP8。四步流程为加载模型→准备校准数据→应用量化→评估精度，评估示例 lm_eval/gsm8k | [README L46–63](https://github.com/vllm-project/vllm/blob/b17039bccc17b94a2ea107272ad7bc93508708df/docs/features/quantization/README.md#L46-L63)、[int8.md L8–13](https://github.com/vllm-project/vllm/blob/b17039bccc17b94a2ea107272ad7bc93508708df/docs/features/quantization/int8.md#L8-L13)、L117–136 | 同上 | 固定文档及内部冲突 | B11-C04：SM 7.5 的 kernel/runtime 条件未核对，可用性保持 unknown；Blackwell 限定于此方法页和快照，不外推所有 INT8；流程未实测 |
| vLLM 的量化校验入口：ModelConfig._verify_quantization（vllm/config/model.py L867 起）：从 HF 模型配置的 quant_method 检测，override 方法按序检查（bitblas、gptq_marlin_24、gptq_marlin、gptq_bitblas、awq_marlin、ipex、moe_wna16、modelopt、modelopt_fp4、petit_nvfp4、mxfp4、cpu_awq——重后端最后避免不必要 import）；不支持时 ValueError | vllm/config/model.py L867–945 | 同上 | 固定源码 | 具体每种方法的硬件检查分散在各 quant config 类，未逐一展开 |
| vLLM Ascend 支持矩阵：Quantization 行 “W8A8 available; working on more quantization method support (W4A8, etc)”（Functional） | supported_features.md L28（commit 52d4acfa） | v0.14.0rc1 | 固定文档 | “available”不等于每个模型/硬件组合验证过 |
| vLLM Ascend 有评估指南四份：docs/source/developer_guide/evaluation/ 的 using_ais_bench.md、using_evalscope.md、using_lm_eval.md、using_opencompass.md | 固定 commit 文件树 | 同上 | 文档存在性 | 内容未逐字读；代查修正：此前只列两份 |
| 该 commit 有量化用户指南页 docs/source/user_guide/feature_guide/quantization.md（ModelSlim 推荐 + LLM-Compressor 两条工具链、W8A8 示例、量化前确认 RAM）；developer_guide 下另有 quantization 页；assets/quantization/ 仅为配图 | 固定 commit 文件树与该页头部（主任务复核，2026-10-08） | 同上 | 文档存在性 + 内容摘录 | 安装与示例命令未逐字核对，不作操作依据；代查修正了此前“无量化专题页”的错误负面断言 |

## 未解决与抓取失败

- 研究子代理两次 2 小时超时，改由主任务直接取证（本记录）。
- INT8 的 SM 7.5 文档冲突未以 kernel/runtime 证据解决；vLLM 各量化方法的 quant config 硬件检查细节、KV cache 量化与模型量化的组合关系（quantized_kvcache.md 未逐字读）、vLLM Ascend 评估指南正文未读。
- 昇腾侧量化工具链（AMCT 等）未研究，缺口保留。
