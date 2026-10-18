# Batch 24 · T06-03 Codex 定向复核报告

- 复核日期：2026-10-18（Asia/Shanghai）。
- 结论：**暂不通过**。
- 初审发现：**CLOSED 4 项、OPEN 5 项**；仍 OPEN 的 C03、C04、C05、C07、C08 均为 P2。
- 新发现：**3 项，均 OPEN（P2 2 项、P3 1 项）；无 P1**。
- 执行边界：本会话 Codex 独立复核，仅新增本报告；不修改正文、作者取证、registry、导航或计划，不代替 T06-04 或整个 Batch 24 验收。
- 模型审计：当前会话未提供可独立核验的后端模型、推理档位和路由元数据，记录为 `unknown`；未另行派发子代理或声称完成指定模型的额外 CLI 审阅。

## 1. 范围、方法与基线

依次重读[初审报告](batch-24-t06-03-codex-review.md)中 C01–C09 的编号、旧位置及建议关闭条件，再通读[修订正文](../../knowledge/06-training/pretraining-and-finetuning.md) L1–153、[作者取证记录](batch-24-t06-03-sources.md)（特别是 L123–129）、[来源登记表](../../sources/registry.yaml)相应条目。任务依据为[完整覆盖任务表](../../plans/full-coverage-backlog.yaml) L5930–5972 的 T06-03；同时重读仓库 README、编写指南、归属边界、schema，并核对已有并行状态、checkpoint 和执行循环章节。

本报告中的正文行号均指本次修订版本，不沿用初审旧行号；上游源码行号均由实际下载的原文件计数，不使用网页工具重排行号。

| 输入 | 本次 SHA-256 |
|---|---|
| 修订正文 | `216fdadff5004bc66b18d8d1026f3ec3bc396fcd438bf3d50909d1b069e40fe2` |
| 作者取证记录 | `de8cf806e24f779661325c51399716f1f4f0e945dd8ab1b02d7f3b3accec5b5b` |
| 初审报告 | `6ccc35c6ab87172679523121570440ae195ea77a2ecf06101993eb4c2f587dca` |
| 来源登记表 | `cfb95b9746f8405bf2c9f8d0101090fb9086a5a663c31d1d261693d3d700e59a` |
| 完整覆盖任务表 | `53bfc8fe47d56ab322e546c853858cbaa90cf5a5d0305b33a80bab0f39275d54` |

### 1.1 重开记录与限制

1. 通过只读 HTTP 实取 30 个对象：PEFT 6 个源码/测试文件、Transformers 3 个源码文件、MindSpeed-LLM 10 个文件及其 v2.2.0 codeload 包、Megatron 6 个文件及 core_v0.19.2 codeload 包、AMD/PyTorch 两个版本化网页和 LoRA 摘要页；请求均返回 HTTP 200。
2. 网页工具首次打开 MindSpeed `pretrain_gpt.py` 和 AMD 兼容页报内部错误；随后使用同一精确 URL 的只读 curl 均成功。**本轮没有最终无法重开的关键页面**，不将工具错误记成上游页面缺失。
3. 独立枚举 Megatron 档案，确认 Llama3/GPT-3 两个模型脚本存在；独立读取 MindSpeed 包和配套 Megatron 数据参数入口，核查修订中新出现的字段。未执行下载包内任何代码或测试。
4. 固定 tag 文件的关键哈希与初审/作者补证一致。PyTorch 2.6 HIP 页本次完整字节哈希为 `93bde1ef96606447002bb23262255c7c515dc026e02f57177c31401709eb563d`，不同于初审记录；不把版本化网页当作不可变字节快照，本轮按实际重开的内容判断，未据哈希差异推断技术变更。
5. 没有训练、微调、合并、转换、安装或主动 GPU/NPU 操作；上游测试仅阅读，未运行。没有目标环境兼容性、吞吐、质量或恢复一致性实测结论。临时取回件和构建副本均位于仓库外，不是长期证据附件。

### 1.2 精确上游证据索引

以下 E 编号仅供本报告引用，不是新增 registry ID。

| 编号 | 实际重开的固定来源与原文件位置 | 本轮支持范围 |
|---|---|---|
| E01 | [Transformers v4.43.2 data_collator.py](https://github.com/huggingface/transformers/blob/v4.43.2/src/transformers/data/data_collator.py#L803-L825)，另核 L312–322；[modeling_llama.py](https://github.com/huggingface/transformers/blob/v4.43.2/src/transformers/models/llama/modeling_llama.py#L1163-L1174) | 因果 LM labels 的 pad 忽略和模型侧移位。L312 是其他 collator 的字段说明，不能单独证明 prompt 自动屏蔽；正文已另指因果 LM 分支并保留数据管道责任。 |
| E02 | [MindSpeed-LLM v2.2.0 pretrain_gpt.py](https://github.com/Ascend/MindSpeed-LLM/blob/v2.2.0/pretrain_gpt.py#L144-L165)，另核 L225–240、L247–267 | 损失乘 `loss_mask`、token 量取 mask 聚合；`blend`/`blend_per_split` 从 data-path 类参数构造，与 `split`、position/attention reset、EOD mask 字段分列。 |
| E03 | [PEFT v0.7.1 lora/config.py](https://github.com/huggingface/peft/blob/v0.7.1/src/peft/tuners/lora/config.py#L45-L108)；[lora/model.py](https://github.com/huggingface/peft/blob/v0.7.1/src/peft/tuners/lora/model.py#L235-L254)，另核 L353–358、L421–424、L691–728 | bias、额外保存/训练模块、可训练参数范围；不支持的目标模块/配置可以显式报错；merge 与 safe_merge 的限定。 |
| E04 | [PEFT v0.7.1 peft_model.py](https://github.com/huggingface/peft/blob/v0.7.1/src/peft/peft_model.py#L160-L202)，另核 L307–336、L647–692、L733–735 | adapter 保存范围、加载训练开关、`load_adapter` 新增 adapter 不自动激活。该 API 说明不能替代完整训练 checkpoint。 |
| E05 | [Transformers v4.43.2 trainer.py](https://github.com/huggingface/transformers/blob/v4.43.2/src/transformers/trainer.py#L1064-L1099)，另核 L311–327、L2873–2892、L2916–2920、L2931–2967 | optimizer 按实际参数及衰减组构造；训练 checkpoint 在相应条件下另存 optimizer/scheduler、RNG、Trainer state。参数组责任不只是组数量。 |
| E06 | [PEFT v0.7.1 testing_common.py](https://github.com/huggingface/peft/blob/v0.7.1/tests/testing_common.py#L516-L572)；[test_decoder_models.py](https://github.com/huggingface/peft/blob/v0.7.1/tests/test_decoder_models.py#L165-L201)；[lora/layer.py](https://github.com/huggingface/peft/blob/v0.7.1/src/peft/tuners/lora/layer.py#L168-L185) | 同一适配模型合并/重载的 logits 比较；测试还明确区分适配模型与裸基座的输出。默认线性 LoRA 的零增量初始化不能外推为已训练 adapter 装载后仍等于裸基座。 |
| E07 | MindSpeed-LLM v2.2.0 [全参 SFT](https://github.com/Ascend/MindSpeed-LLM/blob/v2.2.0/examples/mcore/llama2/tune_llama2_7b_full_ptd.sh#L36-L75)、[LoRA-SFT](https://github.com/Ascend/MindSpeed-LLM/blob/v2.2.0/examples/mcore/llama2/tune_llama2_7b_lora_ptd.sh#L77-L99)、[预训练](https://github.com/Ascend/MindSpeed-LLM/blob/v2.2.0/examples/mcore/llama2/pretrain_llama2_7b_ptd.sh#L68-L95) | 固定模型脚本的阶段、数据/模板、LoRA 与不载 optimizer/RNG 字段；不把示例选择升级为全部 SFT 的默认行为。 |
| E08 | [MindSpeed-LLM v2.2.0 pack 文档](https://github.com/Ascend/MindSpeed-LLM/blob/v2.2.0/docs/pytorch/solutions/finetune/multi_sample_pack_finetune.md#L9-L21)；[CP 微调文档](https://github.com/Ascend/MindSpeed-LLM/blob/v2.2.0/docs/pytorch/features/fine-tuning-with-context-parallel.md#L18-L28) | pack 的拼接、pad 与 attention 边界；CP 微调的 general mask 限定。它们不是数据源混合权重或重采样方案。 |
| E09 | [Megatron core_v0.12.1 arguments.py](https://github.com/NVIDIA/Megatron-LM/blob/core_v0.12.1/megatron/training/arguments.py#L2241-L2275)；[blended_megatron_dataset_builder.py](https://github.com/NVIDIA/Megatron-LM/blob/core_v0.12.1/megatron/core/datasets/blended_megatron_dataset_builder.py#L552-L578)；[blended_dataset.py](https://github.com/NVIDIA/Megatron-LM/blob/core_v0.12.1/megatron/core/datasets/blended_dataset.py) | 配套 Megatron 的数据入口是 data-path 权重/前缀对等形式；builder 按目标样本数和权重请求各源样本，不是未经限定的原始 token 配额。另在完整 MindSpeed v2.2.0 包内检索 `--data-weight`，未找到该字段。 |
| E10 | [Megatron core_v0.12.1 最小循环](https://github.com/NVIDIA/Megatron-LM/blob/core_v0.12.1/examples/run_simple_mcore_train_loop.py#L39-L75)；[core_v0.19.2 codeload 档案](https://codeload.github.com/NVIDIA/Megatron-LM/tar.gz/refs/tags/core_v0.19.2)；[Llama3-8B 脚本](https://github.com/NVIDIA/Megatron-LM/blob/core_v0.19.2/examples/llama/train_llama3_8b_h100_fp8.sh#L55-L78)与 [GPT-3 175B 脚本](https://github.com/NVIDIA/Megatron-LM/blob/core_v0.19.2/examples/gpt3/train_gpt3_175b_distributed.sh) | 合成循环的范围与两个真实模型预训练脚本的存在、配置字段；不证明模型 SFT 取证完成或实际可运行。 |
| E11 | [MindSpeed requirements](https://github.com/Ascend/MindSpeed-LLM/blob/v2.2.0/requirements.txt#L1-L18)；[install_guide](https://github.com/Ascend/MindSpeed-LLM/blob/v2.2.0/docs/pytorch/install_guide.md#L56-L79)；[README](https://github.com/Ascend/MindSpeed-LLM/blob/v2.2.0/README.md#L57-L95)；[模型表](https://github.com/Ascend/MindSpeed-LLM/blob/v2.2.0/docs/pytorch/models/moe_model.md) | HF 固定依赖、配套 Mcore、按模型覆盖版本、在研组件及 Pass/Test 分级。不同档案不拼成已验证环境。 |
| E12 | [AMD docs-7.1.1 PyTorch compatibility](https://rocm.docs.amd.com/en/docs-7.1.1/compatibility/ml-compatibility/pytorch-compatibility.html)，Support overview、Version support、Docker image compatibility、Key features、Known issues；[PyTorch 2.6 HIP](https://docs.pytorch.org/docs/2.6/notes/hip.html)，HIP interfaces、Checking for HIP、torch.distributed backends | 实际版本线、依赖/功能边界和后端枚举可查；不能推出本页固定 HF 组合、任意模型或外部内核已兼容。 |
| E13 | [LoRA 论文摘要](https://arxiv.org/abs/2106.09685) | 方法和论文自身实验范围；未重开 PDF 全文，不增加平台收益承诺。 |

## 2. 初审发现逐项判定

**判定口径：**修订说明不是关闭证据；某项主要错误改正但仍未满足其关键关闭条件，仍保留原编号 OPEN，不另计一次新发现。

| 初审编号 / 优先级 | 原位置与关闭条件重核 | 修订后依据及上游对照 | 判定 |
|---|---|---|---|
| B24-T063-C01 / P2 | 旧正文 L56、L80、L89：纠正吞吐分子/分母，区分 HF shift/ignore 与 loss_mask，交代计时、rank 和 prompt/pad/pack。 | 新正文 L59–64、L74、L115、L124 已按实际计损预测位置定义 tokens/s，要求声明计时和跨 rank 范围，并区分 attention mask、prompt 屏蔽、pad/pack。作者补证 L127 与 E01、E02、E08 相符。没有以合成计数或未经实测的吞吐作结论。 | **CLOSED** |
| B24-T063-C02 / P2 | 旧正文 L43–48、L60–68、L83、L92、L106：分开目标轴/参数轴，限定 LoRA-SFT 和实际可训练范围，修正资源外推。 | 新正文 L44、L51、L82–88、L118、L127、L146 区分两轴，列出 bias/modules_to_save 的例外，并说明分片/量化/offload 未取证、基座不一定每设备全量驻留。与 E03、E13 对应；纯 LoRA 的范围不再冒充 PEFT 全家族定义。 | **CLOSED** |
| B24-T063-C03 / P2 | 旧正文 L60–72、L76、L82、L92–94：补三类操作矩阵，闭合 adapter 与配套身份、active、可训练集合及 optimizer 参数组、完整 resume。 | 新正文 L90–107 已补操作矩阵、active、adapter-only 不等于完整恢复、safe_merge 和测试边界（E04–E06）。但 L96–101 未把 adapter 工件与数据/tokenizer/模板的具体修订配对；L85 的概括性“身份须记录”和 L117 的独立数据进度口径还不是这套配套契约。L133 对 optimizer 仅检查组数量，没有组成员/稳定参数身份及其状态映射。E05 实际按参数及衰减分组；既有 checkpoint 页也要求精确核对 param group，而非只数个数。 | **OPEN**：需补最低配套身份清单及参数组/状态映射核对，或精确链接已有契约并明确本页适用关系；不要求执行训练。 |
| B24-T063-C04 / P2 | 旧正文 L81、L96、L109：分开等价检查和新目标质量基线，删除曲线连续性及异常表现的绝对判据。 | 新正文 L116、L131–136 已分开两类检查，固定输入/mask/模式/随机条件、限制测试容差并增加第一步机械检查（E06）。但 L149 仍原样声称任一契约错位“都表现为质量异常而非显式报错”；E03 中不支持的目标模块和配置存在明确 ValueError 路径，不能保证只静默劣化。新增同条件检查的另一项过度概括另见 R02。 | **OPEN**：去掉“都……而非……”的保证，分别保留显式装载/配置失败与可能静默质量异常；不能只以曲线解释结束排查。 |
| B24-T063-C05 / P2 | 旧正文 L46、L76、L82、L113：解释 blend/split/pack、采样单位/权重、重采样、消费统计和阶段转换责任。 | 新正文 L66–76、L117 确已分开三种机制并要求按源统计；作者补证 L128 与 E02、E08 对应。但 L72 仅说贡献“样本或 token”，没有说明所选实现权重落在哪个单位、是否/何时重采样以及样本比例为何不自动等于有效监督 token 比例。L76 仍只将重置/继承责任转引并行页，没有给本页三类操作的数据游标/RNG 决策。E09 有按目标样本数构建各源份额的精确入口；未知推荐比例不能替代机制交付。新增无依据字段另见 R01。 | **OPEN**：补所选实现的单位、采样/重复语义及阶段进度策略；未知策略明确列为交付缺口，而不只写“属恢复契约”。 |
| B24-T063-C06 / P2 | 旧正文 L100、旧取证 L5/L51/L101、旧 registry revision：更正“core_v0.19.2 不含模型配置”的否定断言。 | 新正文 L140、新 registry `src.nvidia.megatron-model-configs-core-v0.19.2`（L6100 起）和既有 `src.nvidia.megatron-examples-core-v0.12.1`（L6064 起）已改正。作者 L125 明确撤回早期“tar 实开”说法，解释当时只有两个文件名探测，并提供完整包哈希；本轮 E10 实包、两个脚本及哈希相符。旧取证正文/建议条目仍留历史文字，但末尾明确更正其失效，不再视其为有效否定证据。保留 0.12.1 的依赖对齐理由与示例存在性已分开。 | **CLOSED** |
| B24-T063-C07 / P2 | 旧正文 L100、旧取证 L35：标清合成循环，另补 NVIDIA 选定模型的预训练/SFT 及数据、模板、损失、训练状态入口；未补则不得验收。 | 新正文 L140 已正确标明微型 GPT/MockGPTDataset、模型分片保存和非生产恢复边界；也补了两个官方预训练配置，E10 可证。**同段明确“SFT 专项脚本未逐目录核对”**，作者 L129 无进一步取证；新 registry 题名也仅为模型级预训练示例。仍没有 NVIDIA 选定模型 SFT 的真实数据/模板/损失/训练状态入口。 | **OPEN**：合成标注子项完成，但 SFT 交付缺口未关闭；如实披露 unknown 不等于满足验收。 |
| B24-T063-C08 / P2 | 旧正文 L102、旧取证 L42：以精确官方来源列实际后端条件，分开支持声明、未核实 HF/模型组合和本库未执行。 | 新正文 L142 已补两条版本化链接，区分版本线并将固定 HF 组合标为 unknown；与 E12 的证据边界一致。但仍只是“覆盖其声明的版本线”“分布式后端限制”等目录式概述，未给实际 PyTorch×ROCm 值、已核对的后端限制值或相关功能/依赖条件。E12 可直接核对其 PyTorch 2.9/ROCm 7.1.1 等不同版本节，以及 PyTorch 2.6 HIP 的 nccl/gloo 后端范围。正文没有把这些核查结果落实为本页可读的执行边界；硬件/OS未核查范围也未明确列出。 | **OPEN**：补具体条件及未核查层次，保持不同版本线独立；不要求制造可运行 AMD 样板或宣称该 HF 组合不兼容。 |
| B24-T063-C09 / P3 | 旧正文 L56、L100–101、L113：为正确的 requirements、install_guide、README 事实补近邻精确来源，保留模型覆盖/在研限定。 | 新正文 L141 在相应事实旁给出同 tag 的三个精确文件链接；L153 保留按模型覆盖限定。E11 重开分别核到 requirements L2/L14、install_guide L56–79、README L57–95；其固定版本/脚本族也可由 registry 的 workflows 条目追溯。没有把在研表或 Pass/Test 扩为本库兼容证明。 | **CLOSED** |

### 2.1 未关闭项的最小剩余工作

- **C03**：把基座/adapter 不可变引用与数据、tokenizer、模板修订成组记录；核对 optimizer 组成员、稳定参数身份与状态映射，不以组数相同替代。可复用[Checkpoint 状态一致性](../../knowledge/06-training/checkpoint-state-consistency.md) L123–134 的身份、param group、逻辑进度和同输入比较契约，避免复制整章。
- **C04**：纠正 L149 的绝对化；保留“错误可能显式失败，也可能静默影响质量”，同时按 R02 限定等价检查的参考对象。
- **C05**：在 E02/E09 的固定实现内说明样本级混合与监督 token 统计的差别、采样/重复策略以及阶段切换的数据状态选择。未知推荐比例继续 unknown，不需补造推荐值。
- **C07**：完成一个固定 NVIDIA 档案的所选模型 SFT 配置及对应数据/模板/损失/训练状态取证；否则继续保留该验收缺口。
- **C08**：在不拼配版本的前提下，写出官方已核对的具体支持条件，明确硬件/OS、HF、模型和外部扩展哪些未核查、本库哪些未运行。

## 3. 修订引入的新发现

### B24-T063-R01 — 混合入口新增了无选定版本依据的 `--data-weight`

- **优先级 / 状态：P2 / OPEN。**
- **位置：**修订正文 L68–72；作者补证 L128 没有该参数定义。
- **问题：**该节明确以 MindSpeed-LLM v2.2.0 为例，却把 `--data-weight` 格式化为典型配置入口，没有标为假设性伪字段。读者可能据此使用一个在所选档案中未证实的 CLI 参数。
- **重开依据：**E02 L253–259 从 `args.data_path`、各 split 的 data-path 取 blend。E09 的配套 Megatron core_v0.12.1 参数解析 L2244–2275 将权重/前缀对放在 `--data-path` 或 `--train-data-path` 等参数内。完整 MindSpeed-LLM v2.2.0 包内检索 `--data-weight` 无匹配。这里仅判定本页选定组合没有该字段的支持证据，**不声称所有框架都不存在这个名字**，也未实际启动解析器证明运行结果。
- **影响：**区别于 C05 尚未交付的混合机制解释，这是修订中新加入的具体字段主张；属于命令/配置可操作性的技术问题。
- **关闭条件：**改用已核验的版本化入口并交代单位；如确有另一实现支持该字段，给精确来源并明确其不同适用范围，不把未取证参数混入本页 MindSpeed 样板。

### B24-T063-R02 — 将任意 adapter/权重切换都写成前后输出等价

- **优先级 / 状态：P2 / OPEN。**
- **位置：**修订正文 L133；关联 L96–101 的新阶段操作矩阵。
- **问题：**新增检查要求在“任何状态切换（载入基座/adapter、合并、重分片）后”比较切换前后输出并按预定容差处理，却未限定两侧是**同一组目标权重和相同 adapter 组合的两个表示/装载结果**。载入已训练 adapter、切换新任务 adapter 或有意换基座，本来就可能改变模型函数，不能拿切换前裸基座/旧任务模型当等价 oracle。
- **重开依据：**E06 `testing_common.py` L535–553 比较的是同一适配模型的合并/反合并/卸载表示；L555–559 反而要求该适配模型与裸基座输出不相同。`lora/layer.py` L168–185 的默认零增量初始化只支持相应初始化条件，不能证明已训练增量无效。
- **影响：**这是由修订新增的普遍化验收规则，可能把合法的新阶段装载误判为失败，或诱导错误追求裸基座与适配模型一致。它不同于 C04 尚未删除的“契约错位不会显式报错”旧断言，不重复计数。
- **关闭条件：**区分保函数表示变换/恢复与有意改变模型函数的阶段切换；前者固定同一目标工件、active adapter 和数值条件作等价比较，后者使用已知正确目标复合模型作装载参考并建立独立质量基线。不应要求任意旧、新模型互相等价。

### B24-T063-R03 — 新增 HIP 依据未进入正文来源依赖清单

- **优先级 / 状态：P3 / OPEN。**
- **位置：**修订正文 L8–20、L142；registry L3547 起的既有 `src.pytorch.hip-notes-2.6`。
- **问题与依据：**L142 新增 PyTorch 2.6 HIP 文档作为后端语义依据，但 12 项 `source_refs` 中没有其已存在的精确登记 ID；现有 `src.pytorch.parallel-training-state-2.6` 等不能替代这个独立来源依赖。E12 页面可重开，问题不是页面不可访问或未登记，而是正文的机器可读依赖未同步。
- **关闭条件：**若继续采用该页，补入现有登记 ID 并保持版本边界；如不用该来源，则相应删去该项依赖主张。无需创建重复 registry 条目。

## 4. 任务验收重新核对

| T06-03 验收条目 | 本次修订已补足部分 | 复核结果 |
|---|---|---|
| 1. 四类工作流；监督目标、token/mask/label、样本混合、阶段切换 | 目标/参数轴和 LoRA-SFT 限定成立；tokens/s 与实际损失路径得到修正。 | **部分满足，未通过。** 混合采样单位、重复语义和阶段数据状态未闭合（C05），新增字段有误（R01）。 |
| 2. 数据/模型/tokenizer/adapter 身份，可训练集合与 optimizer；精确合并/恢复边界 | 实际可训练范围、active、adapter-only 与完整 checkpoint、safe_merge、官方测试边界均有改进。 | **部分满足，未通过。** 配套修订身份及 optimizer 参数组/状态映射仍缺最低契约（C03）。 |
| 3. token 吞吐、质量曲线、重复/遗漏、显存与 I/O 口径 | L115–118 已给时间分母、实现差异、跨目标不可直接衔接、按源统计、非全量驻留与存储边界。 | **观察口径部分满足；不据此宣布整体验收。** “不同目标/语料曲线”应按其评价条件解释，不将该句用来否定固定共同评测集上的合法比较；阶段验证仍受 C04/R02 阻断。 |
| 4. mask/label、污染、adapter、状态继承异常与阶段转换验证 | 有实际损失路径、active 检查、污染只是线索、两类验证分离及未执行声明。 | **部分满足，未通过。** C03/C04 残留和 R02 的错误等价范围仍影响判断。 |
| 5. NVIDIA/Ascend 固定配置；AMD 官方支持边界，不任意扩兼容 | Ascend 三个模型脚本及依赖链接可核；NVIDIA 合成标注和模型级预训练证据补足；AMD 不拼版本并保留 HF unknown。 | **部分满足，未通过。** NVIDIA 模型 SFT 证据仍缺（C07），AMD 仍缺正文中的具体条件（C08）。 |

任务另列的三条 `source_discovery` 重核：

- **HF 固定版本文档和测试：**新增的保存/合并测试定位可重开，已满足“有固定测试依据”的取证部分；只读未运行，不等于本库 resume/合并验证完成（E04–E06）。
- **Megatron/MindSpeed 所选模型预训练/SFT 配置与循环对应：**Ascend 有固定脚本，NVIDIA 从合成循环推进到模型级预训练，但 SFT 缺口仍由正文承认，故未完成（E07、E10）。
- **LoRA 原论文只解释方法：**摘要内容和论文环境数字仍未外推为目标平台收益，维持该部分满足；不声称 PDF 全文已核（E13）。

## 5. 元数据、内容边界与检查记录

- 稳定 ID、标题/H1、`type: concept`、`domain: training`、`status: draft`、`platforms: [generic]`、`updated_at: "2026-10-18"` 未被升级为硬件验证或跨平台兼容声明；四个 related_ids 均有现有目标。新模型预训练源已登记并进入正文，HIP 依赖遗漏另列 R03。
- C06 作者更正与 registry 的新旧两条 Megatron 档案一致；0.19.2 模型脚本不与 MindSpeed 的 0.12.1 依赖拼配。Ascend 按模型覆盖版本、在研配套和未运行限制保持；NVIDIA/AMD 的未完成证据不因“已加链接”而关闭（E10–E12）。
- 06 章仍承担目标、参数与训练状态；04 章承担文件持久化/数据路径，08 章承担证据推理；RL rollout 仍为后续任务入口。未发现修订将未来组件标为已实现。与既有 checkpoint 状态契约相比，C03 的检查粒度不足已明确记录，不用上位章节的存在替本页补验收。
- 不变更外部许可或仓库再分发口径；报告只提供链接、短标识和原创判断，不导入上游源码长段或大型日志。

本次结构检查与变更边界核验：

1. 在原工作树执行 `PYTHONDONTWRITEBYTECODE=1 make check`：**PASS，103 content entries / 491 sources**（报告写入前、写入后均通过）。
2. 为遵守“只新增报告”，未在原工作树覆盖生成的 build；将包含既有 build 的源树复制到仓库外临时副本，排除 `.git/` 和 `.venv/`，再执行 `PYTHONDONTWRITEBYTECODE=1 make -C <临时副本> PYTHON=<本仓库 .venv/bin/python 的绝对路径> build`：**PASS，103 content entries / 491 sources**，生成副本内的 `build/catalog.json` 和 `build/catalog.md`。这不是无既有 build 的纯净 bootstrap 测试，也不是原工作树已重建的声明。
3. `git diff --check` 通过；对复核开始时工作树内全部已跟踪及未忽略未跟踪文件的 SHA-256 清单逐项复验，全部不变。本次仅新增指定报告，已有未提交修改保持原样。
4. 未修改 `src/kb/`，不运行与本次报告无关的测试套件。以上通过只证明结构与本地引用，不证明技术正确性、远程页面或硬件行为。

## 6. 结论

**T06-03 本次定向复核暂不通过。** 初审 9 项中 **4 项 CLOSED、5 项 OPEN**；另有 **3 项新 OPEN（2 P2、1 P3）**。合计仍有 **7 项 OPEN P2、1 项 OPEN P3，无 P1**。

用户要求的通过条件“全部初审发现 CLOSED，且无新 OPEN P1/P2”两项均未满足。需要先修订 C03、C04、C05、C07、C08 及 R01/R02，再定向重核；R03 同步完善追溯。不能以 draft/source_checked、保留 unknown、上游脚本存在或结构构建通过宣布技术验收通过。

未开展真实训练/硬件验证的状态继续保持；本报告不替作者关闭任务计划或改写其他批次结论。

## 附录：关键独立取回校验

| 对象 | SHA-256 |
|---|---|
| Megatron core_v0.19.2 codeload 包 | `4c16ccc2a0d4c1b6c96f59baaab99316ac3b39eca2ef960ddf4436a2962eb69a` |
| Llama3-8B H100 FP8 脚本 | `fddc588ca15f24384465f16e171147204feeb691f8fbc54b2a797cf135adc9cc` |
| GPT-3 175B 脚本 | `4bc0e0194fef6cdaf578fcf81259ec7de34b26fc1892741ab314827e23059952` |
| MindSpeed-LLM v2.2.0 codeload 包 | `693f619a8b608726c23dc53a7e0d283684883149fb140951f169a297fe72936e` |
| core_v0.12.1 arguments.py | `f2a56f59b4ebd3913fdda687872e20a4c0f7e434d3166867f068b8ec9a92d454` |
| core_v0.12.1 blended_megatron_dataset_builder.py | `f41e2eb71bf0cb5c9a972a2294642c65edf542ea0d2abf3a6dae75f69b5c5c69` |
| core_v0.12.1 blended_dataset.py | `b7b6eefa4000a8e0a193e4a9b8e8c6fbfe1601be97e7017d292864e94f552d27` |
| Transformers modeling_llama.py | `f4549647e6e3c0cd5f7c869ec16c6c82f318760d37f57d70f5a53afac5b302ed` |
| MindSpeed pretrain_gpt.py | `b3ca649a9f11868da890a2af67b94ccacc938f1128272dfb569f7fac6d2ed549` |
| PEFT testing_common.py | `1e2e7fd4e2ca6836362a4da7d1d46601b6b417a3160b18bd5b9f70a98560503d` |
| PEFT test_decoder_models.py | `f2e5c4f211c80ff13a6b1c0bebfb9263f78b3cd020ae22ac0410ee1b2c6a392c` |
| AMD docs-7.1.1 PyTorch compatibility 页 | `79c10c8262d804ff735c65198a12e72875b768869d8f180c2bb69c94bb85d85c` |

MindSpeed codeload 精确入口为 [v2.2.0](https://codeload.github.com/Ascend/MindSpeed-LLM/tar.gz/refs/tags/v2.2.0)；其他文件路径和 tag 见 E01–E13。包哈希和目录枚举只证明取回对象身份及存在性，不证明脚本执行结果。
