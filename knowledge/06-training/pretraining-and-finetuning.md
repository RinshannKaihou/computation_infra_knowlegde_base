---
id: training.pretraining-and-finetuning
title: 预训练与微调工作流和状态契约
type: concept
domain: training
status: draft
platforms: [generic]
source_refs:
- src.paper.lora-2106.09685
- src.hf.peft-source-v0.7.1
- src.hf.transformers-trainer-4.43.2
- src.hf.huggingface-hub-v0.33.0
- src.nvidia.megatron-examples-core-v0.12.1
- src.nvidia.megatron-model-configs-core-v0.19.2
- src.ascend.mindspeed-llm-workflows-v2.2.0
- src.ascend.mindspeed-llm-parallel-features-v2.2.0
- src.pytorch.parallel-training-state-2.6
- src.pytorch.dcp-2.6
- src.ascend.torch-npu-v7.2.0-pytorch2.6.0
- src.amd.pytorch-compatibility-7.1.1
- src.pytorch.hip-notes-2.6
updated_at: "2026-10-19"
summary: 比较预训练、继续预训练、全参 SFT 与参数高效微调的目标、数据、状态与资源路径，给出四类工作流的状态契约、观察口径、阶段切换验证与常见异常的区分检查，形成后训练（RL）入口。
related_ids:
- training.parallelism-and-state
- training.framework-execution
- training.checkpoint-state-consistency
- data-storage.training-data-path
verification:
  status: source_checked
  evidence_refs:
  - src.hf.peft-source-v0.7.1
  - src.hf.transformers-trainer-4.43.2
  - src.ascend.mindspeed-llm-workflows-v2.2.0
  - src.paper.lora-2106.09685
  notes: 仅核对固定 tag 源码/脚本与论文摘要（锚点见 docs/research/batch-24-t06-03-sources.md）；未运行任何预训练/微调/合并/转换命令，未实测吞吐或质量。
---

# 预训练与微调工作流和状态契约

本页比较四种工作流在**目标、数据、状态与资源路径**上的差别，并给出阶段切换时哪些状态继承、哪些显式丢弃。并行机制见[并行策略与训练状态](parallelism-and-state.md)，执行循环见[训练框架组件与执行循环](framework-execution.md)，checkpoint 文件语义见 04 章。强化学习后训练（PPO/GRPO 类 rollout 与权重同步）见[RL rollout、权重同步与训练推理协同](rl-rollout-consistency.md)，本页只作入口。

## 定义与要解决的问题

先区分两个正交的轴：**训练目标轴**（预训练 / 继续预训练 / SFT——决定损失落在什么数据上）与**参数适配轴**（全参微调 / LoRA / 其他 PEFT 方法——决定哪些参数可训练）。本页四行对照是"目标 × 参数"的一个具体选样：前三行是全参轴，第四行是 **LoRA-SFT**（本页选定的 PEFT 样板）；PEFT 家族还有前缀微调、prompt tuning 等其他方法与可训练范围，不在本页展开（保持边界，不把 LoRA 等同于 PEFT 全部）。

| 工作流（本页选样） | 监督目标 | 数据形态 | 起点 | 结果产物 |
|---|---|---|---|---|
| 预训练 | 自回归/掩码语言建模损失 | 大规模无标注语料（token 流、pack 拼接） | 随机初始化或公开基座 | 基座模型权重＋tokenizer |
| 继续预训练 | 同预训练 | 新领域无标注语料，可与旧语料混合（混合机制见下文"样本混合"节） | 已有基座 checkpoint | 更新后的基座权重 |
| 全参 SFT | 指令/对话格式的条件语言建模损失 | 指令样本（prompt＋response，模板拼接） | 基座 checkpoint（示例脚本显式不载入其 optimizer/RNG） | 全量权重的新版本 |
| LoRA-SFT（PEFT 样板） | 同 SFT | 同 SFT | 冻结的基座＋低秩可训练增量 | adapter 权重（或合并后的权重） |

LoRA 的方法边界（[arXiv:2106.09685 摘要](https://arxiv.org/abs/2106.09685)）：冻结预训练权重，把权重增量约束为低秩分解 ΔW=BA，只训练低秩矩阵；论文报告相对全参微调大幅减少可训练参数与显存、且与 adapter 方法不同、不增加推理时延。论文数值（GPT-3 175B 上可训练参数约少 10,000 倍、GPU 内存约少 3 倍等）是其实验环境的结论，**不作为任何目标平台的预期**。

## 机制与关键关系

### token/mask/label 契约

损失只应落在被监督的 token 上，而**各实现的计损路径不同**，检查时必须按实际路径取数：

- **HF/Transformers 4.43.2 路径**：`label_pad_token_id` 默认 `-100`，该值会被 PyTorch 损失函数自动忽略（[data_collator.py](https://github.com/huggingface/transformers/blob/v4.43.2/src/transformers/data/data_collator.py) L312–322）；因果 LM 分支从 `input_ids` 构造 labels 并忽略 pad（L821–824）；模型侧（如 Llama）在计算损失时对 labels 做**移位**（[modeling_llama.py](https://github.com/huggingface/transformers/blob/v4.43.2/src/transformers/models/llama/modeling_llama.py) L1163–1174）——被监督的是"移位后的预测位置"，不是原始 labels 逐位。**prompt 屏蔽由数据管道负责**，框架只保证忽略索引语义；`attention_mask` 不等于 loss mask。
- **Megatron/MindSpeed 路径**：计损由独立的 `loss_mask` 控制（如 MindSpeed `pretrain_gpt.py` 的损失聚合单读 loss_mask），与 attention mask、原始 labels 是不同对象。

Ascend 侧 MindSpeed-LLM 的长序列 CP 微调另有约束：`--attention-mask-type` 只能 `general`（[CP 微调](https://github.com/Ascend/MindSpeed-LLM/blob/v2.2.0/docs/pytorch/features/fine-tuning-with-context-parallel.md)）。

### 样本混合、划分与 pack 是三件不同的事

继续预训练/SFT 的数据组织常被混为一谈，实际是三个独立机制（口径以 MindSpeed-LLM v2.2.0 配置为例，其他框架字段名不同但概念对应）：

| 机制 | 是什么 | 典型字段/入口 | 与恢复/计量的关系 |
|---|---|---|---|
| **数据集混合**（blend） | 多个语料源的加权组合，决定每个源贡献多少样本 | 官方入口是 `--data-path` 的**权重前缀对**（`weight1 prefix1 weight2 prefix2`）或纯前缀列表（此时权重按各数据集长度推断）；`--train/valid/test-data-path` 可独立分列（来源见表下） | 权重与数据修订决定"训练了什么"；消费统计按源分开记录才能核对重复/遗漏 |
| **训练/验证/测试划分**（split） | 同一数据集内部的集合划分 | `--split 949,50,1`（[预训练脚本](https://github.com/Ascend/MindSpeed-LLM/blob/v2.2.0/examples/mcore/llama2/pretrain_llama2_7b_ptd.sh)） | 划分泄漏（评测样本进训练集）是污染检查的对象之一 |
| **pack（序列打包）** | 把多个短样本拼进一个定长序列以提升利用率 | MindSpeed 多样本 pack 微调方案（[文档](https://github.com/Ascend/MindSpeed-LLM/blob/v2.2.0/docs/pytorch/solutions/finetune/multi_sample_pack_finetune.md)） | pack 改变样本边界与注意力边界（如 reset-position-ids），有效 token 计数须扣除拼接 padding，不能按序列条数折算 |

数据集混合行的来源：[Megatron core_v0.12.1 arguments.py](https://github.com/NVIDIA/Megatron-LM/blob/core_v0.12.1/megatron/training/arguments.py) L2244–2275 的 --data-path help（`src.nvidia.megatron-examples-core-v0.12.1` 补充核对）。

**混合的单位与采样/重复语义**（[core_v0.12.1 blended builder](https://github.com/NVIDIA/Megatron-LM/blob/core_v0.12.1/megatron/core/datasets/blended_megatron_dataset_builder.py) 构建规则原文口径）：

- ①权重与目标 size 都给出时——中层子数据集按"权重×size"比例采样构建，顶层混合数据集长度略超 size、同样按比例采样（即权重同时决定子集配额与顶层混合索引的分布）；
- ②只给前缀（无权重）时——中层"无超额采样"，顶层长度按各数据集长度比例、**封顶在中层长度之和**（不额外采样）；
- ③权重与 size 都缺省——按一个 epoch 等价构建。
- **读取与重复**：GPT 子数据集的 document/sample/shuffle 索引在构建期预生成，`__getitem__` 沿该索引取样本（[gpt_dataset.py](https://github.com/NVIDIA/Megatron-LM/blob/core_v0.12.1/megatron/core/datasets/gpt_dataset.py) L112–113、L233 起）。
- **重复消费**：当**所需 token 总量**（按目标样本数×序列长度＋每序列额外 token 换算）**超过单 epoch 可提供的 token 总量**时按 epoch 数放大并重复（重排）文档索引（epoch 判定与文档索引复制分别见 [gpt_dataset.py](https://github.com/NVIDIA/Megatron-LM/blob/core_v0.12.1/megatron/core/datasets/gpt_dataset.py) `_get_num_epochs` 与 `_build_document_index`）——即加权目标超过源数据时会**重复消费原始语料**，重复量计入按源消费统计。

因此**样本比例不自动等于有效监督 token 比例**（各源样本长度不同），有效 token 占比要按上文的计损路径另行统计。具体混合比例、按模型/领域的推荐值没有取证（unknown，交付缺口如实保留）。

**本页三类操作的数据游标/RNG 决策**：

- 推理装载——不适用（不消费训练数据）；
- 同阶段 resume——恢复截点的游标与 RNG 状态（见[并行页](parallelism-and-state.md)数据进度行与[Checkpoint 恢复一致性](checkpoint-state-consistency.md)）；
- 新阶段微调/继续预训练——游标与 RNG 重置，切换前的消费统计归档为上一阶段终态。

### 状态契约：身份与责任

| 状态 | 预训练 | 全参 SFT | LoRA-SFT（PEFT 样板） |
|---|---|---|---|
| 模型权重 | 可训练，产物身份＝权重＋结构版本 | 可训练，起点须记录来源 checkpoint 身份 | **冻结**（默认纯 LoRA 配置）；身份＝基座 checkpoint 引用 |
| 可训练参数 | 全部 | 全部 | 默认仅低秩增量（r/alpha/target_modules 定义，见下）；**PEFT v0.7.1 还允许把 bias、modules_to_save 等纳入可训练范围**（[config.py](https://github.com/huggingface/peft/blob/v0.7.1/src/peft/tuners/lora/config.py) L57–61、L91–98）——可训练集合按实际配置核对，不按方法名一刀切 |
| optimizer state | 与全参对应 | 重新初始化（见下节脚本证据） | 只覆盖实际可训练参数；基座参数不需要 optimizer state |
| tokenizer/模板 | 随训练固定，身份须记录 | 必须与基座一致或显式声明扩展 | 同左；模板（prompt-type）错误=数据契约错误 |
| 数据游标/RNG | 记录已提交样本 | 指令数据集独立游标 | 同左 |

PEFT v0.7.1 源码级依据（[peft_model.py](https://github.com/huggingface/peft/blob/v0.7.1/src/peft/peft_model.py)、[lora/config.py](https://github.com/huggingface/peft/blob/v0.7.1/src/peft/tuners/lora/config.py)）：`LoraConfig` 的身份字段是 `r`（默认 8）、`target_modules`（模块名或正则）、`lora_alpha`、`lora_dropout`，缩放为 alpha/r（L45–108）；`save_pretrained` 支持安全序列化与选择性保存 adapter（L160 起）；`load_adapter` 要求 adapter 名称唯一、`is_trainable` 默认 **False**，且新加载的 adapter **不会自动激活**（L647 起、L651–654）——用于推理的 adapter 默认不可训练且需显式设为 active，续训必须显式声明。

### adapter 装载/激活/续训的继承与重置矩阵

同一份 adapter 工件在不同操作下的状态契约不同（以 PEFT v0.7.1 与 Transformers 4.43.2 为样板）：

| 状态项 | 推理装载（新阶段使用） | 同阶段 resume（恢复训练） | 新阶段微调（从 adapter 续训新任务） |
|---|---|---|---|
| 基座权重身份 | 必须匹配（结构版本/修订） | 同左 | 同左或显式迁移 |
| adapter 工件身份（配置＋权重修订） | 记录 | 记录 | 记录来源 |
| active adapter | 需显式激活 | 需显式激活 | 需显式激活＋`is_trainable=True` |
| 可训练集合 | 空 | 与中断前一致 | 按新配置声明 |
| optimizer/scheduler/步数 | 不适用 | **必须恢复**（adapter-only 工件不含这些：HF Trainer 的训练 checkpoint 另存 optimizer/scheduler、RNG 与 Trainer 状态，[trainer.py](https://github.com/huggingface/transformers/blob/v4.43.2/src/transformers/trainer.py) L2873–2892、L2916–2920） | 重新初始化 |
| 精度状态/RNG/数据进度 | 不适用 | 恢复 | 重置或按新契约 |

**adapter 工件的最低配套身份清单**（装载/续训前必须配对核对，缺一即无法判定身份）：基座 checkpoint 的精确修订（结构版本/权重哈希或来源 tag）；tokenizer 修订（与基座一致或显式声明的扩展）；训练模板/prompt-type 及其版本；adapter 自身的 LoraConfig（r/alpha/target_modules/可训练范围扩展）与权重修订；训练数据集修订（指令集版本）；（resume 场景另需）optimizer/scheduler/步数/RNG/数据游标——这些不在 adapter 工件内。optimizer 侧的核对不止数量：**param groups 的成员与稳定参数身份映射**要逐组核对（哪些参数在哪一组、每组超参、state 键与参数的对应；仅数个数相同不能证明映射正确——对照[Checkpoint 恢复一致性](checkpoint-state-consistency.md)的状态契约）。

因此 **adapter-only 保存/加载不等于完整训练恢复**：`save_pretrained` 只承诺 adapter 权重与配置；合并结果（下节）也不能替代分离形态的训练检查点。固定版本的官方测试对照（已读未运行）：PEFT v0.7.1 的 [testing_common.py](https://github.com/huggingface/peft/blob/v0.7.1/tests/testing_common.py) L516–572 与 [test_decoder_models.py](https://github.com/huggingface/peft/blob/v0.7.1/tests/test_decoder_models.py) L165–201 用同输入比较**合并前后、保存重载后**的 logits——其容差是该测试套件的设定，不是目标平台通用阈值。

### adapter 合并与恢复边界

`merge_and_unload` 把 LoRA 层并入基座权重、返回可独立使用的模型（[lora/model.py](https://github.com/huggingface/peft/blob/v0.7.1/src/peft/tuners/lora/model.py) L691–728，`safe_merge` 选项做的是数值异常检查——NaN 类风险的防护，**不是合并前后质量等价的证明**）。边界：合并是**权重改写**，合并后的模型与"基座＋adapter 分离形态"是两种部署表示；本版本未核对从合并结果恢复分离 adapter 的反合并 API（unknown）。恢复（续训）时以分离形态＋显式 `is_trainable` 与完整训练检查点为准；合并形态用于推理部署。

### 阶段切换的官方脚本证据

MindSpeed-LLM v2.2.0 的 Llama2 示例给出两类切换契约，另有预训练与 HF Trainer 侧的对照：

- **全参 SFT**：从基座 `--load` 后**显式** `--no-load-optim --no-load-rng`、`--finetune`、`--is-instruction-dataset`、`--prompt-type llama2`（[tune 脚本](https://github.com/Ascend/MindSpeed-LLM/blob/v2.2.0/examples/mcore/llama2/tune_llama2_7b_full_ptd.sh)）；
- **LoRA 微调**：用 `--lora-r 16 --lora-alpha 32 --lora-target-modules linear_qkv linear_proj linear_fc1 linear_fc2`（[lora 脚本](https://github.com/Ascend/MindSpeed-LLM/blob/v2.2.0/examples/mcore/llama2/tune_llama2_7b_lora_ptd.sh)；`--lora-fusion` 为其 CCLoRA 加速特性）。
- **预训练侧**：记录数据与保存节奏（`--data-path`、`--split 949,50,1`、`--save-interval`、cosine 学习率）（[pretrain 脚本](https://github.com/Ascend/MindSpeed-LLM/blob/v2.2.0/examples/mcore/llama2/pretrain_llama2_7b_ptd.sh)）。
- **HF Trainer 侧**：tokenizer 随模型保存以便"rerun an interrupted training"；IterableDataset 场景要求各进程一致的 generator 或 `set_epoch()`（[trainer.py](https://github.com/huggingface/transformers/blob/v4.43.2/src/transformers/trainer.py) L288–327）。

## 观察口径

- **有效 token 吞吐**：定义为**计量窗口内实际计损的有效预测 token 数 ÷ 对应经过时间**（单位 tokens/s，注明计时范围、是否含 checkpoint/评估时间、跨 rank 的汇总或去重口径）。"实际计损"按上文实现路径取数：HF 侧是移位后 labels 中非忽略索引的位置数，Megatron/MindSpeed 侧是 loss_mask 生效位置数——**不是**原始 labels 的非 `-100` 计数，也不能用 attention_mask 代替。pack 拼接要扣除拼接 padding。与"样本数""batch 数""序列条数"分开记录；这些口径改变时不可比。
- **质量曲线**：预训练看损失/验证困惑度随有效 token 的曲线；SFT/LoRA 看任务指标。**不同目标/语料/监督区域的曲线之间没有可比性**——切换阶段后的曲线起点不要求与前一阶段衔接（见下节验证方法），曲线异常只能作为线索。
- **样本重复/遗漏**：以数据修订＋游标（已提交样本/epoch，混合场景按语料源分开）为口径核对；切换工作流后 sampler 重置造成的重复训练或遗漏，用去重键统计而不是靠 epoch 数推断。
- **显存与 I/O**：LoRA 的显存节约来自"基座参数不产生梯度/optimizer state"（冻结，且按实际可训练配置为准），不是权重变小——基座权重仍需可用（每设备是否全量常驻取决于是否采用分片/量化/offload 等机制，这些机制未在本页取证，不排除非全量驻留的实现）；I/O 压力来自 checkpoint 体积与保存节奏，见[Checkpoint 写入与持久化边界](../04-data-storage/checkpoint-durability.md)与[数据路径](../04-data-storage/training-data-path.md)。

## 异常区分检查与阶段转换验证

| 症状 | 候选原因 | 区分检查 |
|---|---|---|
| 损失异常高/不收敛 | mask/label 契约错误（如 prompt 计损、pad 未忽略、loss_mask 配置错） | 按实现路径抽样核对：HF 侧解码移位后 labels 与忽略索引占比；Megatron/MindSpeed 侧核对 loss_mask 与 attention_mask 是否混用 |
| 损失正常但输出质量差 | 模板/prompt-type 不匹配、tokenizer 版本不一致 | 同一输入走训练与推理两条 tokenize 路径对比；模板字段逐项核对 |
| SFT 后表现劣化 | 数据污染（评测集混入训练集） | 训练/评测集 n-gram 或去重键交叉统计（线索）；污染子集单独评估 |
| adapter 加载后不更新 | `is_trainable` 未显式开启、adapter 未激活 | 检查 requires_grad 集合是否与实际配置的可训练范围一致（纯 LoRA 默认＝低秩增量；含 bias/modules_to_save 时更大），并确认 active adapter |
| 状态继承异常 | optimizer/RNG 未按预期丢弃或继承 | 核对启动参数（如 `--no-load-optim/--no-load-rng`）与实际 state_dict 内容；按继承/重置矩阵分操作类型判断 |
| 合并后结果异常 | 合并版本/配置与训练时不一致 | 以 LoraConfig 身份字段对照；数值级用同输入 logits 对照（装载等价检查）；`safe_merge` 只查 NaN 类异常，不是等价证明 |

**阶段转换验证（两类检查分开，均未执行）**：

- **装载等价检查（同条件对照，仅适用于"同一目标权重的两种表示/装载"）**：适用对象是**同一组目标权重＋相同 adapter 组合**在不同表示或装载方式之间的对照——合并 vs 未合并、保存重载 vs 原始、重分片转换前后（PEFT 官方测试即此思路，且要求适配后模型与裸基座输出**不相同**）。做法：在**未做任何参数更新前**，用固定的校准输入（同 batch、同监督 mask、同推理/训练模式、固定随机性与数值条件）比较两种表示的输出（logits 或 loss）；比较规则与容差事先写定，超差即停止排查。**有意改变模型函数的切换**（载入已训练的新任务 adapter、更换基座）不在等价检查范围内——切换前后的模型本来就应不同，改用"已知正确的目标复合模型作装载参考＋下条的独立质量基线"评价。PEFT v0.7.1 官方测试（[testing_common.py](https://github.com/huggingface/peft/blob/v0.7.1/tests/testing_common.py) L516–572 等）即此类"合并前后/保存重载后同输入对照"的思路，其容差不是本库阈值。另做第一步更新的机械检查：可训练参数集合、梯度是否只在预期集合上产生、optimizer 参数组数量。
- **独立质量基线（换目标后的评价）**：新阶段开始前，在新任务/新语料上以未训练（或基线）模型取得独立基线指标；训练进展与该基线比较，而不是与前一阶段的曲线斜率衔接比较。跨目标的指标不可比时如实标注。

污染重叠统计只是**线索**：训练/评测集 n-gram 或去重键交叉给出证据方向，不直接证明质量劣化的根因；结论仍按 08 章假设检验流程收敛。

## 平台实践与边界

- **NVIDIA（Megatron-Core，两个固定档案）**：
  - core_v0.12.1 的[最小循环示例](https://github.com/NVIDIA/Megatron-LM/blob/core_v0.12.1/examples/run_simple_mcore_train_loop.py)是**合成数据的最小循环演示**（两层微型 GPT、MockGPTDataset；保存函数只展示模型分片状态）——只支撑"循环职责"示意，非性能/质量/生产恢复配置；选它是因为与 MindSpeed-LLM v2.2.0 的 install_guide 指定 Mcore 依赖一致。
  - **模型级预训练配置**在 core_v0.19.2 档案：[examples/llama/train_llama3_8b_h100_fp8.sh](https://github.com/NVIDIA/Megatron-LM/blob/core_v0.19.2/examples/llama/train_llama3_8b_h100_fp8.sh)（Llama3-8B 结构字段：hidden 4096、32 头、GQA 8 组、swiglu/RMSNorm、rope base 1M、H100 fp8）与 [examples/gpt3/train_gpt3_175b_distributed.sh](https://github.com/NVIDIA/Megatron-LM/blob/core_v0.19.2/examples/gpt3/train_gpt3_175b_distributed.sh)。
  - **模型级 SFT 示例**：[examples/multimodal/nvlm/sft_qwen20_72b_internvit_6b.sh](https://github.com/NVIDIA/Megatron-LM/blob/core_v0.19.2/examples/multimodal/nvlm/sft_qwen20_72b_internvit_6b.sh)（`--tokenizer-prompt-format qwen2p0` 模板、`--data-path`；SHA-256 d96068af…，`src.nvidia.megatron-model-configs-core-v0.19.2` 修订轮二补充）——范围为**多模态 NVLM**。
  - 该脚本的**两个目录语义不同，勿混同**：`FINETUNE_DIR` 是本次 SFT 的**输出 checkpoint 目录**（保存与 `--load` 都指向它），`CHECKPOINT_DIR` 是**从预训练结果转换来的权重目录**（经 `--pretrained-checkpoint` 引用；README 要求先把预训练 checkpoint 按目标 PP 转换后再用于 SFT）。
  - **加载侧分支**：`--load` 目录**不存在** checkpoint 时才选用 `pretrained_checkpoint` 并置 `finetune=True`（首次 SFT 路径），**存在**时走目标目录的恢复路径（同阶段 resume：恢复 iteration、消费计数与 optimizer/scheduler/RNG 状态）。即"首次微调"与"断点续训"由输出目录是否有 checkpoint 区分，正文上文的三类操作矩阵据此落到该脚本。
  - 纯文本 LLM 的 SFT 专项脚本在该 tag 未逐目录定位（有限缺口如实保留）。脚本存在不等于可运行或与 Ascend 配套。
- **Ascend（MindSpeed-LLM v2.2.0）**：
  - 预置模型清单按【Pass】（经昇腾官方版本测试）与【Test】（内部测试）分级（[moe_model 等模型表](https://github.com/Ascend/MindSpeed-LLM/blob/v2.2.0/docs/pytorch/models/moe_model.md)）；
  - 依赖与版本入口：[requirements.txt](https://github.com/Ascend/MindSpeed-LLM/blob/v2.2.0/requirements.txt)（transformers==4.43.2、peft==0.7.1）、[install_guide](https://github.com/Ascend/MindSpeed-LLM/blob/v2.2.0/docs/pytorch/install_guide.md)（MindSpeed core 2.2.0_core_r0.12.1＋Megatron-LM core_v0.12.1；qwen3/llama3.3 需 transformers 4.51.0、glm4.5-moe 需 4.54.0）、[README 依赖表](https://github.com/Ascend/MindSpeed-LLM/blob/v2.2.0/README.md)（NPU 驱动/固件/Toolkit/torch_npu 在研版本）；
  - 实际部署须按目标版本重新核对，本页结论不跨版本成立。
- **AMD（分层表述，均为官方页面原文口径）**：
  - ①官方声明的版本线——[ROCm 7.1.1 PyTorch 兼容页](https://rocm.docs.amd.com/en/docs-7.1.1/compatibility/ml-compatibility/pytorch-compatibility.html)（2025-12-10 更新，Applies to Linux）分节覆盖 **PyTorch 2.9＋ROCm 7.1.1、PyTorch 2.8＋ROCm 7.1、PyTorch 2.7/2.8＋ROCm 7.0** 的特性/已知问题与 Docker 镜像兼容；
  - ②PyTorch 2.6 构建侧——[HIP 文档](https://docs.pytorch.org/docs/2.6/notes/hip.html) 可直接核对的条件值：`torch.distributed` 在该版本 ROCm 构建下支持的后端为 **nccl 与 gloo**；该版本页写明 **ROCm 不支持 TF32**；HIP 构建判别用 `torch.version.hip`；接口命名复用 CUDA 名称。这些限制**只绑定 PyTorch 2.6 版本化文档**，不外推为所有 ROCm 版本的永久限制。
  - 两者是**不同版本线**，不拼成一套环境。
  - **未核查范围（如实列出）**：具体 GPU 型号、OS 发行版与驱动版本组合、以及模型外部内核/扩展（FlashAttention 类）在 ROCm 的可用性均未核对（unknown）；PyTorch 2.6＋ROCm 的官方镜像/驱动配套值亦未在上述两页取得（unknown）。本页固定的 HF 组合（Transformers 4.43.2＋PEFT 0.7.1）在 ROCm 上的可执行性**未核实（unknown）**；Megatron/MindSpeed-LLM 向 AMD 的迁移性同样不声明。本库未执行任何 AMD 侧验证。

## 常见误解

- **"LoRA 让模型变小。"** 基座权重仍需可用（是否每设备全量驻留取决于分片/量化/offload 等机制，本页未取证）；默认纯 LoRA 节约的是可训练参数与相应梯度/optimizer state（注意 PEFT 还允许 bias、modules_to_save 等可训练项），推理部署可用合并形态换取无额外时延。
- **"SFT 从基座继续训练会自动带上预训练的 optimizer。"** 官方脚本显式 `--no-load-optim/--no-load-rng`；继承什么是声明出来的，不是默认续接。
- **"论文数字就是我们的预期收益。"** LoRA 论文数值来自其实验环境，只解释方法边界。
- **"阶段切换就是换个数据集。"** 模板、mask、tokenizer、可训练集合与状态继承构成数据与状态双契约。错位可能**显式报错**（如 PEFT 对不支持的 target_modules/配置直接 ValueError），也可能表现为**静默质量异常**（如模板错配）——两类都要查，不能预设它一定静默。

## 适用边界与来源

HF 侧版本按 MindSpeed-LLM v2.2.0 requirements 固定（transformers 4.43.2、peft 0.7.1；install_guide 另注 qwen3/llama3.3 需 4.51.0、glm4.5-moe 需 4.54.0，按模型分列）；在线 HF 文档为可变页未使用。TRL/其他 SFT 框架、样本混合比例与数据污染检测工具无固定资料（unknown，只给方法）。未运行任何脚本；性能与质量数字未实测。取证记录见 [batch-24-t06-03-sources](../../docs/research/batch-24-t06-03-sources.md)。
