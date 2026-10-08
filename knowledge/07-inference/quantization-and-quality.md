---
id: inference.quantization-and-quality
title: 推理量化与输出质量验证
type: concept
domain: inference
status: draft
platforms: [generic]
source_refs:
  - src.vllm.inference-v0-14
  - src.ascend.vllm-ascend-v0-14-0rc1
updated_at: "2026-10-08"
summary: 量化以精度换内存与速度；支持矩阵按实现×硬件分别核对，NPU 不能从上游表推断；输出质量用固定任务的评估对照验证，量化故障按加载、执行、精度三层归因。
related_ids:
  - inference.execution-and-kv-cache
  - inference.latency-metrics
  - inference.ascend-inference-oom-triage
  - reliability.silent-errors-and-integrity
  - training.gpu-npu-precision-difference-triage
verification:
  status: source_checked
  evidence_refs:
    - src.vllm.inference-v0-14
    - src.ascend.vllm-ascend-v0-14-0rc1
  notes: "已核对 vLLM v0.14.0 量化文档目录、硬件支持表、int8 方法页与 _verify_quantization 实现，以及 vLLM Ascend v0.14.0rc1 支持矩阵与评估指南存在性；未运行量化、推理或评估。"
---

# 推理量化与输出质量验证

## 定义与要解决的问题

量化以模型精度换取更小的内存占用与更高的吞吐，使大模型能在更多设备上运行（[vLLM v0.14.0 量化文档](https://github.com/vllm-project/vllm/blob/b17039bccc17b94a2ea107272ad7bc93508708df/docs/features/quantization/README.md)的定义）。本文回答三个问题：支持矩阵怎么读、量化后的输出质量如何验证、量化相关故障按什么分层归因。

`generic` 指问题框架通用；上游 vLLM 的硬件支持表**不含 NPU**，昇腾的支持范围只能看插件自己的声明（见下）。

## 支持矩阵怎么读

vLLM v0.14.0 的量化文档目录含 14 个方法页（AWQ、AutoRound、BitBLAS、bitsandbytes、FP8、GGUF、GPTQ、INC、INT4、INT8、ModelOpt、Quark、TorchAO、量化 KV cache），并给出实现×硬件的支持表（[quantization README 的 Supported Hardware](https://github.com/vllm-project/vllm/blob/b17039bccc17b94a2ea107272ad7bc93508708df/docs/features/quantization/README.md)），例如：表中将 INT8 W8A8 的 Turing/Ampere/Ada/Hopper 与 x86 CPU、FP8 W8A8 的 Ada/Hopper 与 AMD GPU 标为支持，Marlin 从 Ampere 起列为支持；INT8 的 SM 7.5 冲突见下。读表时的边界：

- 表注明确说明矩阵随版本变化，最新状态以 `model_executor/layers/quantization` 的实现为准——表是文档快照，不是运行时保证。
- 矩阵按**实现**分列：同一量化格式（如 W8A8）的 INT8 与 FP8 是不同实现，支持集不同。
- **SM 7.5 存在同快照文档冲突**：README 将 Turing 标为 SM 7.5 且支持 INT8 W8A8（[L46–63](https://github.com/vllm-project/vllm/blob/b17039bccc17b94a2ea107272ad7bc93508708df/docs/features/quantization/README.md#L46-L63)）；INT8 方法页却写 compute capability >7.5，又在同句列出 Turing（[int8.md L8–13](https://github.com/vllm-project/vllm/blob/b17039bccc17b94a2ea107272ad7bc93508708df/docs/features/quantization/int8.md#L8-L13)）。不能合成为一致的支持条件；具体 kernel/runtime 边界未核对，SM 7.5 可用性保持 `unknown`，需固定量化实现与硬件后另证。
- 同一 INT8 W8A8 方法页对 Blackwell 写 compute capability >=100 不支持，并建议 FP8；这里按页面原标度记录，声明只归属该方法页与 v0.14.0 快照，不外推所有 INT8 实现、设备或版本。

运行时校验入口在 `ModelConfig._verify_quantization`（[vllm/config/model.py L867 起](https://github.com/vllm-project/vllm/blob/b17039bccc17b94a2ea107272ad7bc93508708df/vllm/config/model.py#L867)）：从 HF 模型配置的 `quant_method` 检测方法，override 类方法按序检查（重量级后端排在最后以避免不必要的 import），无法识别时抛 `ValueError`。即“配置写错/方法不存在”在启动早期报配置错误，与执行期失败分层。

## 昇腾侧的支持声明与边界

vLLM Ascend v0.14.0rc1 的功能矩阵把 Quantization 标为 Functional：**“W8A8 available; working on more quantization method support (W4A8, etc)”**（[supported_features.md L28](https://github.com/vllm-project/vllm-ascend/blob/52d4acfa51fb868823d1070b81cbd2d97e9e4696/docs/source/user_guide/support_matrix/supported_features.md#L28)）。读这行的边界：

- “W8A8 available”是插件对**该版本**的功能声明，不等于每个模型/硬件组合都验证过；模型支持范围另见模型矩阵。
- 该 commit 有量化用户指南页（[feature_guide/quantization.md](https://github.com/vllm-project/vllm-ascend/blob/52d4acfa51fb868823d1070b81cbd2d97e9e4696/docs/source/user_guide/feature_guide/quantization.md)）：介绍 ModelSlim（推荐，昇腾方向）与 LLM-Compressor 两条工具链及 W8A8 示例；量化前要求确认主机 RAM 足够。该页的安装与示例命令本轮未逐字核对，不作为操作依据。
- 上游 vLLM 的支持表与插件的声明是两套证据，不能互相推断；[昇腾推理 OOM 诊断](ascend-inference-oom-triage.md)的 Issue 现场（如 w8a8 模型）只说明有人这样跑过。

## 输出质量如何验证

量化改变数值语义：精度差异的判定纪律（容差、固定开关、排除合法数值噪声）见[静默错误与计算完整性判定](../08-reliability/silent-errors-and-integrity.md)与[GPU→NPU 精度差异诊断](../06-training/gpu-npu-precision-difference-triage.md)。在此之上，引擎层的质量验证证据：

- **固定任务的基准对照**：vLLM 的 INT8 方法页把“评估精度”列为量化流程的第四步，示例用 `lm_eval` 跑 gsm8k（[int8.md L117–136](https://github.com/vllm-project/vllm/blob/b17039bccc17b94a2ea107272ad7bc93508708df/docs/features/quantization/int8.md#L117-L136)）。要点：评估任务、指标、baseline（未量化模型同任务结果）与样本量都要固定；“跑过基准”不等于“质量达标”，阈值是业务约定。
- **昇腾侧评估指南**：vLLM Ascend 该 commit 的 `docs/source/developer_guide/evaluation/` 有四份评估指南（ais_bench、evalscope、lm_eval、opencompass），内容本轮未逐字读，存在性已核对。
- **产出侧指标不能替代质量**：吞吐/TTFT 正常不证明输出正确；质量结论必须来自输出本身的评估。

## 量化相关故障的三层归因

| 层 | 典型现象 | 证据方向 |
|---|---|---|
| 加载/配置 | 启动报 `ValueError`（未知 quant_method）、不支持组合 | `_verify_quantization` 的方法检测与 override 顺序；模型配置 quant_method 与实际 checkpoint 是否一致 |
| 执行 | 算子/内核错误、显存异常、性能异常 | 该量化实现对该硬件的支持状态（支持表+插件矩阵分别核）；执行层错误按[算子/图编译流程](../02-software-stack/ascend-op-graph-failure-triage.md)与 [OOM 流程](ascend-inference-oom-triage.md)分层 |
| 精度 | 输出质量下降、发散、异常 token | 固定任务评估对照 + 数值纪律；注意与静默错误、配置差异（dtype/KV cache 精度）区分 |

## 常见误解

- **“上游支持 = 昇腾支持”**：上游硬件表不含 NPU；昇腾支持只看插件声明与实测。
- **“量化只影响精度”**：量化还改变内存占用（KV cache、权重）与 kernel 路径，性能与故障形态都随之变化；量化 KV cache 是独立主题（quantized_kvcache.md 本轮未逐字读）。
- **“基准跑通 = 质量达标”**：跑通只证明流程可执行；达标阈值是业务/模型约定，本文不提供。
- **“报错在量化配置 = 根因在量化”**：执行期错误可能来自算子、内存或图路径，按层归因。

## 来源与待确认问题

- [vLLM v0.14.0 量化文档目录与 int8 页](https://github.com/vllm-project/vllm/tree/b17039bccc17b94a2ea107272ad7bc93508708df/docs/features/quantization)、[vllm/config/model.py](https://github.com/vllm-project/vllm/blob/b17039bccc17b94a2ea107272ad7bc93508708df/vllm/config/model.py)。
- [vLLM Ascend v0.14.0rc1 支持矩阵](https://github.com/vllm-project/vllm-ascend/blob/52d4acfa51fb868823d1070b81cbd2d97e9e4696/docs/source/user_guide/support_matrix/supported_features.md)与评估指南目录。
- 逐条主张与证据定位见[第十一批量化来源记录](../../docs/research/batch-11-quantization-sources.md)。
- 待确认：INT8 在 SM 7.5 的文档冲突与具体 kernel/runtime 条件；各量化方法的 quant config 硬件检查细节；量化与 KV cache dtype 的组合关系；vLLM Ascend 评估指南正文；昇腾量化工具链（AMCT 等）未研究。
