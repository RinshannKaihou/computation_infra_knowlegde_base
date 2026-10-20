---
id: inference.output-quality-evaluation
title: 推理输出质量的对照评估方法与案例
type: procedure
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
  - src.pytorch.numerical-verification-2.6
updated_at: "2026-10-21"
summary: 输出质量评估先固定输入身份（模型/tokenizer/模板/测试集与评估协议/采样/上下文与输出预算），再分层归因差异（采样变化与候选计算机制——greedy、累加顺序重排、组 batch 差异均按待检验解释处理）；指标分 logits/数值、确定输入输出、任务质量、安全/业务四层且各层能力边界明确、不给跨任务通用阈值；主指标、容差、样本量、不确定性判定与失败处理预先注册；基线→单变量→恢复对照用可关联可审计的 schema 记录、未运行留空；官方评估例按引擎各自指南引用，论文质量数字属作者报告。
related_ids:
  - inference.quantization-and-quality
  - inference.model-loading-and-readiness
  - inference.latency-metrics
  - inference.pd-disaggregation
  - reliability.silent-errors-and-integrity
  - training.gpu-npu-precision-difference-triage
verification:
  status: source_checked
  evidence_refs:
    - src.vllm.inference-v0-14
    - src.ascend.vllm-ascend-v0-14-0rc1
    - src.ascend.mindie-llm-docs-69e5a5dd
    - src.pytorch.numerical-verification-2.6
  notes: "已核对 vLLM Ascend v0.14.0rc1 四份评估指南全文（lm-eval/EvalScope/AISBench/OpenCompass）、vLLM v0.14.0 int8 评估步骤与 NIXL accuracy 脚本入口、MindIE-LLM@69e5a5dd FAQ 确定性条目与 ModelTest 入口（README 级）、三篇论文摘要、PyTorch 2.6 数值精度说明。逐条主张与行号锚点见 docs/research/batch-27-t07-05-sources.md（含初审修订轮）。未运行任何评估命令；schema 中不填写未运行测量。"
applicability:
  environment_refs: []
  notes: "无环境档案；评估工具按各官方指南口径引用（指南未钉评估框架版本，采样参数透传行为未核）。具体执行前须补齐模型/硬件/引擎版本与评估框架版本，本文不构成可执行处方。"
---

# 推理输出质量的对照评估方法与案例

## 定义与要解决的问题

量化、kernel/图路径变更或平台迁移之后，"输出还对不对"需要一个可复用的对照评估方法。本文回答五个问题：评估前要固定哪些输入身份；输出差异怎么区分**生成采样变化**与**候选计算机制**；指标分哪四层、各自能下什么结论；主指标/容差/样本量/不确定性与失败处理怎么预先注册；基线→单变量→恢复的对照怎么用可审计的 schema 记录。数值差异的判定纪律见[静默错误与计算完整性判定](../08-reliability/silent-errors-and-integrity.md)与[GPU→NPU 精度差异诊断](../06-training/gpu-npu-precision-difference-triage.md)；量化机制与支持矩阵见[量化边界](quantization-and-quality.md)。本文是方法与官方证据的汇编，**没有本库实测结果**。

## 第一步：固定输入身份与评估协议

任何对照之前，以下各项必须逐项固定并记录为不可变配置引用（缺一项，差异就无法归因）：

| 固定项 | 内容 | 依据与边界 |
|---|---|---|
| 模型与 tokenizer | 模型 revision/权重摘要、tokenizer 版本 | 身份固定清单见[权重加载](model-loading-and-readiness.md) |
| 提示模板 | chat template/system prompt/few-shot 格式、BOS 处理 | vLLM int8 指南特别提醒 `add_bos_token` 影响精度（[int8.md L130–139](https://github.com/vllm-project/vllm/blob/b17039bccc17b94a2ea107272ad7bc93508708df/docs/features/quantization/int8.md#L130-L139)） |
| **测试集与评估协议** | 数据集版本/split/样本清单**＋任务 YAML 本身**：few-shot 数量、答案抽取与 filter、指标聚合方式、生成模式 | lm-eval 的任务 YAML 同时承载 target/metric/generation/few-shot/filter（[using_lm_eval.md L230–275](https://github.com/vllm-project/vllm-ascend/blob/52d4acfa51fb868823d1070b81cbd2d97e9e4696/docs/source/developer_guide/evaluation/using_lm_eval.md#L230-L275)）——冻结 YAML 而不只是数据集名，否则同一测试集仍可得不可比分数 |
| 采样参数 | temperature/top_p/top_k/seed | **评估用 greedy/低温是本库方法选择**，不是各指南的共同默认——AISBench 样例用 temperature=0.6（[L153–194](https://github.com/vllm-project/vllm-ascend/blob/52d4acfa51fb868823d1070b81cbd2d97e9e4696/docs/source/developer_guide/evaluation/using_ais_bench.md#L153-L194)）、OpenCompass 配置用 0.01（[L100–105](https://github.com/vllm-project/vllm-ascend/blob/52d4acfa51fb868823d1070b81cbd2d97e9e4696/docs/source/developer_guide/evaluation/using_opencompass.md#L100-L105)）；各工具对采样参数的透传默认值未核（见待确认） |
| **上下文与输出预算（分列）** | 输入截断、总上下文上限（服务端 max_model_len）、生成上限 max tokens、停止条件 | AISBench 指南区分 max_out_len 与输入长度之和、服务端上下文上限、后处理与重试（L153–194）；其 max_model_len 要求存在**指南自身不一致**——示例命令设 `--max_model_len 35000` 而注释写"should be greater than 35000"（[L41–45](https://github.com/vllm-project/vllm-ascend/blob/52d4acfa51fb868823d1070b81cbd2d97e9e4696/docs/source/developer_guide/evaluation/using_ais_bench.md#L41-L45)）——两说照录，且该数字是该指南对"多数数据集"的适用口径，不是跨模型/跨任务阈值 |

## 第二步：区分采样变化与候选计算机制

输出不一致时先分层归因；以下各机制是**待检验的解释**，不是预先判定"合法"或"缺陷"的依据——是否可接受交给预注册容差与任务判据：

- **采样随机性（第一层检验）**：开放采样下输出天然波动。MindIE FAQ 给出的处置：后处理从 sampling 改为 **greedy** 可基本保证输出文本稳定（[faq.md L209–213](https://github.com/Ascend/MindIE-LLM/blob/69e5a5dd4b533eaffc7e198320435350825a36f7/docs/zh/faq/faq.md#L209-L213)）。greedy 后仍不一致，才继续往下查。
- **运算重排的舍入差异（候选机制）**：即使输入相同，batch 组成或执行顺序不同可能改变浮点运算的**结合顺序**，有限精度下重排会引入舍入差异。MindIE FAQ 将此表述为"matmul 算子不同行的累加顺序不完全相同＋浮点加法无交换律"（[L215–219](https://github.com/Ascend/MindIE-LLM/blob/69e5a5dd4b533eaffc7e198320435350825a36f7/docs/zh/faq/faq.md#L215-L219)）——"无交换律"是 FAQ 原文用词，技术上更准确的表述是**浮点加法/乘法的非结合性**与运算重排的舍入影响（[PyTorch 数值精度说明](https://docs.pytorch.org/docs/2.6/notes/numerical_accuracy.html)开篇；本文据此更正归属，FAQ 原文照录）。MindIE 提供 `ATB_MATMUL_SHUFFLE_K_ENABLE=0` 关闭 shuffle k、强制各行累加顺序一致（文档口径性能降约 10%）——**归因工具**（检验差异是否来自顺序重排），且 ModelTest 将该开关列为 NPU 精度测试场景的默认设置之一（[README_NEW L178–184](https://github.com/Ascend/MindIE-LLM/blob/69e5a5dd4b533eaffc7e198320435350825a36f7/examples/atb_models/tests/modeltest/README_NEW.md#L178-L184)）；不是常规部署建议，10% 代价是文档声明非本库实测。
- **组 batch 位形差异（候选机制）**：Server 模式下 CPU 负载等环境影响请求到达时间，两次运行组出的 batch 不同（10 请求组一个 batch vs 只组到 5 个），输出随之不同；调度框架在 block 查询模式下本身可保证确定性（[faq.md L221–223](https://github.com/Ascend/MindIE-LLM/blob/69e5a5dd4b533eaffc7e198320435350825a36f7/docs/zh/faq/faq.md#L221-L223)）。
- **排除后仍稳定复现的差异**：进入进一步定位（对照[静默错误与计算完整性判定](../08-reliability/silent-errors-and-integrity.md)的纪律：有依据的容差、任务影响、支持/反证），**不直接判"缺陷"**。

## 第三步：指标分四层，各层结论不越界

| 层 | 观察对象 | 能支持的结论 | 不能支持的结论 |
|---|---|---|---|
| logits/数值层 | 逐 token 概率、隐藏态数值（对齐输入与 token 历史下比较） | 数值路径是否改变、量级是否合理 | 不能换算成任务质量；数值不同不单独证明 kernel 分派改变（执行路径要另行取证） |
| 确定输入输出层 | greedy/固定 seed 下相同输入的输出文本 | **行为一致性**的观察（同/不同） | 相同文本不能证明 logits/中间数值相同；不同文本不能仅凭固定 seed 归因到计算 |
| 任务质量层 | 固定测试集上的任务分数（gsm8k 准确率等） | 该任务上的相对变化 | **不给跨任务通用合格阈值**——阈值是业务/模型约定 |
| 安全/业务层 | 业务指标、安全评估 | 业务可用性判断 | 需要业务方定义，本库不代设 |

任务质量层是量化对照的主力（vLLM INT8 量化流程把"评估精度"列为第四步，示例 `lm_eval` 跑量化产物 gsm8k 5-shot limit 250 并提醒 BOS，[int8.md L117–139](https://github.com/vllm-project/vllm/blob/b17039bccc17b94a2ea107272ad7bc93508708df/docs/features/quantization/int8.md#L117-L139)；**"与未量化基线同任务对照"是本库方法要求**，该页只给了量化侧评测命令）；logits 层用于归因而非评分。

## 第四步：预先注册主指标、容差、样本量、不确定性与失败处理

评估设计在跑之前写死（本库方法建议）：

- **主指标与方向**：一个主指标＋差值口径（绝对差/相对差、方向是否有意义）＋少量辅助指标；不用"多指标里挑好的"。
- **容差含义**：预先声明多大的差异算"有变化"。**"落入容差"的判读必须结合不确定性**：点估计差值低于容差但不确定范围跨界＝**未决**，不得记为"无差异"——未检出差异≠无差异。
- **样本量、抽样与重复单位**：预先声明样本选择方式（全量测试集还是抽样、抽样框与规则）、样本量依据（测试集规模与期望检出差异）、**重复单位**（同配置独立重跑计一次重复；重跑内不引入新抽样则只反映运行波动）。lm-eval 输出含分任务/分 filter 的**单个**指标标准误（[using_lm_eval.md L128–131](https://github.com/vllm-project/vllm-ascend/blob/52d4acfa51fb868823d1070b81cbd2d97e9e4696/docs/source/developer_guide/evaluation/using_lm_eval.md#L128-L131)），不能直接充当基线与变体**差值**的不确定性。
- **不确定性与判定规则**：**预先选择**适用于**对照差值及比较结构**（两配置对同一测试集的配对比较 vs 独立样本比较）的估计方法与置信口径（如基线重复测量的波动范围、两比例之差的标准误）；声明差值判定规则——**不确定范围跨界＝未决；重复或有效样本不足、无法形成有效不确定性估计＝未决**。容差是**实际可接受变化**的业务边界，与统计上可检出的差异幅度是两个概念，分别声明、不混用。区分三种结论范围：固定测试集上的观察结论、对新样本的推断、运行重复波动——三者不混用。
- **失败请求处理**：负载失败、超时、空输出**不能从质量分母中消失**——分母＝全部提交请求；失败率单列，与质量分并报；重试与空输出的归并口径按结果 schema 的预声明执行。

## 第五步：基线→单变量→恢复的对照 schema

三阶段结构：baseline（未改）→ 单变量（仅改一个量化/kernel/图路径项）→ recover（恢复基线）。配置与结果用可关联、可审计的 schema（本库设计建议）：

配置 schema（每行一个实验；每行还关联其重复运行）：

| 字段 | 说明 |
|---|---|
| exp_id / run_id | 实验标识与每次运行标识（结果按 run 关联，不按实验混计） |
| baseline_ref | 基线实验的 exp_id（单变量与恢复行都填） |
| prereg_ref | 预注册计划（第四步各项）的文件引用 |
| 引擎＋固定 commit / 模型＋revision / 评估工具＋版本 | 三重身份 |
| 变量（前值→后值） | 唯一变量的**有效值对**，不是概述 |
| 完整固定配置引用 | 第一步清单的不可变配置（模板 YAML/任务 YAML/采样/预算/环境/数值/并行与 batch 控制条件） |
| 执行路径证据位置 | 该变量实际命中的证据（日志/profiling 引用）——"其余不变"要可核验 |

结果 schema（每 run 一行）：

| 字段 | 说明 |
|---|---|
| run_id / exp_id | 每条结果携带所属运行与实验键；沿 baseline_ref 可定位基线实验的各次运行及其聚合口径（用哪次/均值/区间） |
| 预注册引用 | prereg_ref（配置表） |
| 提交数 / 完成数 / 失败数 / 超时数 | 四个计数字段：**完成/失败/超时为三类互斥且穷尽的终态，提交数＝三者之和**；空输出不另设第四类，按预声明归入完成（质量按零分计）或失败，二选一 |
| 重试归并 | 预先声明：重试计为请求尝试还是逻辑样本；多次尝试如何归并为一个终态与质量计分（如取最终尝试） |
| 主指标值＋不确定性与口径 | 按预注册方法 |
| 原始证据引用 | 实际输出/逐样本终态/重试记录或其受管证据的位置——分数与计数可从原始状态重算核对 |
| 相对基线差＋判定 | 差值、是否超容差、是否未决（不确定范围跨界或样本/重复不足） |
| 恢复判据 | 恢复行与基线运行按同一差值不确定性判据比较；回到容差内＝支持"差异由该变量引起"的因果假设；**未恢复或仍有混杂＝未决**，记录后续排查项 |

**未运行的格子保持空，不填写估计值**。[PD 分离](pd-disaggregation.md)等部署形态的输出一致性对照可参考 NIXL 集成测试入口（run_accuracy_test.sh/test_accuracy.py，[nixl_connector_usage.md L177–183](https://github.com/vllm-project/vllm/blob/b17039bccc17b94a2ea107272ad7bc93508708df/docs/features/nixl_connector_usage.md#L177-L183)；脚本内部判据未核，不宣称其证明 PD 质量等价）。

## 官方评估例（按引擎各自的指南）

- **vLLM Ascend 四份评估指南**（docker 起 vllm-ascend 服务为共同样板；命令参数与批量/重试等条件按各指南）：[lm-eval](https://github.com/vllm-project/vllm-ascend/blob/52d4acfa51fb868823d1070b81cbd2d97e9e4696/docs/source/developer_guide/evaluation/using_lm_eval.md) 在线（`lm_eval --model local-completions … --tasks gsm8k`，命令在 [L116–120](https://github.com/vllm-project/vllm-ascend/blob/52d4acfa51fb868823d1070b81cbd2d97e9e4696/docs/source/developer_guide/evaluation/using_lm_eval.md#L116-L120)，演示约 30 分钟 [L123](https://github.com/vllm-project/vllm-ascend/blob/52d4acfa51fb868823d1070b81cbd2d97e9e4696/docs/source/developer_guide/evaluation/using_lm_eval.md#L123)）与离线（`--model vllm`，任务 YAML 自定义）两路径；[EvalScope](https://github.com/vllm-project/vllm-ascend/blob/52d4acfa51fb868823d1070b81cbd2d97e9e4696/docs/source/developer_guide/evaluation/using_evalscope.md) 服务评估＋perf 压测两模式（`--limit 10` 为演示样本量）；[AISBench](https://github.com/vllm-project/vllm-ascend/blob/52d4acfa51fb868823d1070b81cbd2d97e9e4696/docs/source/developer_guide/evaluation/using_ais_bench.md) 多数据集精度＋性能（C-Eval/MMLU/GPQA 逐个安装；batch/请求速率/重试/生成/后处理参数见其 L153–194）；[OpenCompass](https://github.com/vllm-project/vllm-ascend/blob/52d4acfa51fb868823d1070b81cbd2d97e9e4696/docs/source/developer_guide/evaluation/using_opencompass.md) 经 OpenAISDK 连服务（meta_template 用 HUMAN/BOT 角色并保留 SYSTEM，[L82–87](https://github.com/vllm-project/vllm-ascend/blob/52d4acfa51fb868823d1070b81cbd2d97e9e4696/docs/source/developer_guide/evaluation/using_opencompass.md#L82-L87)；batch/retry 等条件见其配置）。四者结构与默认条件不同，按各自指南使用。
- **MindIE**：本轮检索范围内未取得 docs/ 内的官方精度评估专页（developer_guide/test.md 为标题＋一句内容简介的存根，无外链——检索范围＝docs/zh 目录树清点，非全仓穷举）；**仓内可用入口是 ModelTest**——[examples/atb_models/tests/modeltest/README.md](https://github.com/Ascend/MindIE-LLM/blob/69e5a5dd4b533eaffc7e198320435350825a36f7/examples/atb_models/tests/modeltest/README.md) 有下游数据集精度测试与限制（L236–283）、GSM8K 示例（L332–333），新版 [README_NEW.md](https://github.com/Ascend/MindIE-LLM/blob/69e5a5dd4b533eaffc7e198320435350825a36f7/examples/atb_models/tests/modeltest/README_NEW.md) 给出任务 YAML、指标/截断字段与 `modeltest` 命令（L267–328）——本轮按 README 级登记为入口，新旧接口差异、脚本判据、模型支持与 MindIE Server 端到端服务评估的关系未核（unknown）。另有 FAQ 确定性条目（上文）。
- **论文质量案例**：[AWQ v6](https://arxiv.org/abs/2306.00978v6) 报告量化误差降低机制与基准表现、[GPTQ v2](https://arxiv.org/abs/2210.17323v2) 与[SmoothQuant v7](https://arxiv.org/abs/2211.10438v7) 报告精度保持——均属**作者报告**（摘要级证据，各自范围不笼统提升为无损保证），本库未复现，与官方评估例分开归属。

## 常见误解

- **"跑个基准就是质量验证"**：不固定输入身份与评估协议、不预注册容差与失败处理的基准跑分无法归因。
- **"输出不一样＝有 bug"**：先过采样/运算重排/batch 位形三层检验；各机制是待检验解释，是否可接受交给预注册判据。
- **"任务分没降＝数值没变"**：任务分数对小的数值差异不敏感；数值层归因用对齐输入的 logits/确定输入对照。
- **"失败请求剔除后算平均"**：失败/超时/空输出从分母消失会高估质量；分母＝全部提交。
- **"差值小于容差＝无差异"**：不确定范围跨界＝未决；未检出差异≠无差异。
- **"论文报告的精度保持可直接引用为本地结论"**：作者报告≠本库复现，两者分开记录。
- **"一个阈值走天下"**：合格阈值是任务与业务约定，本文不提供跨任务通用阈值。

## 来源与待确认问题

- vLLM Ascend v0.14.0rc1 [评估指南目录](https://github.com/vllm-project/vllm-ascend/tree/52d4acfa51fb868823d1070b81cbd2d97e9e4696/docs/source/developer_guide/evaluation)；vLLM v0.14.0 [int8 评估步骤](https://github.com/vllm-project/vllm/blob/b17039bccc17b94a2ea107272ad7bc93508708df/docs/features/quantization/int8.md#L117-L139)与 [NIXL accuracy 脚本](https://github.com/vllm-project/vllm/blob/b17039bccc17b94a2ea107272ad7bc93508708df/tests/v1/kv_connector/nixl_integration/)；MindIE [FAQ](https://github.com/Ascend/MindIE-LLM/blob/69e5a5dd4b533eaffc7e198320435350825a36f7/docs/zh/faq/faq.md)与 [ModelTest](https://github.com/Ascend/MindIE-LLM/blob/69e5a5dd4b533eaffc7e198320435350825a36f7/examples/atb_models/tests/modeltest/README.md)；[PyTorch 2.6 数值精度说明](https://docs.pytorch.org/docs/2.6/notes/numerical_accuracy.html)。
- 逐条主张与证据定位见[第二十七批评估来源记录](../../docs/research/batch-27-t07-05-sources.md)（含初审修订轮）。
- 待确认：各评估框架版本与采样参数透传默认值；引擎 logprobs/数值接口在 v0.14.0 的字段细节；NIXL accuracy 脚本内部判据；MindIE ModelTest 新旧接口与 Server 端到端评估关系；论文全文实验设置。本文 schema 无任何已填写测量——首次实测后按 schema 落盘并引用。
