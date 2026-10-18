# Batch 24 · T06-03 Codex 定向复核第二轮报告

- 复核日期：2026-10-19（Asia/Shanghai，采用本轮最新环境日期；作者补证和前轮报告的 2026-10-18 日期保持原样）。
- 结论：**暂不通过**。
- 本轮要求重核的 8 项：**CLOSED 6 项、OPEN 2 项**；仍 OPEN 的是 **C05、C08，均 P2**。
- 前轮已 CLOSED 的 C01/C02/C06/C09：关联回归抽查后 **4 项维持 CLOSED**。
- 本轮新发现：**B24-T063-S2-01，P2 / OPEN**。合并历史编号计 **CLOSED 10 项、OPEN 3 项（全部 P2）；无 OPEN P1/P3**。
- 执行边界：仅新增本报告，不修改正文、作者取证、registry、导航、计划及其他审阅报告；结论限于 T06-03，不代表整个 Batch 24 验收。
- 模型审计：由当前 Codex 会话执行。会话未提供可独立核验的实际后端模型、推理档位或路由元数据，记为 `unknown`；没有另行派发子代理，也不冒称完成了一轮经元数据确认的指定模型 CLI 调用。

## 1. 范围、输入与方法

重读[第一轮复核报告](batch-24-t06-03-codex-recheck.md)、[初审发现与关闭条件](batch-24-t06-03-codex-review.md)、[修订后正文](../../knowledge/06-training/pretraining-and-finetuning.md) L1–156，以及[作者取证](batch-24-t06-03-sources.md)的“修订轮二补充”L131–139；核对相应[来源登记](../../sources/registry.yaml)和[任务表](../../plans/full-coverage-backlog.yaml) T06-03（L5930–5972）。同时遵循 README、编写指南、内容归属和 metadata schema，核对正文转引的并行状态及 checkpoint 恢复契约。

正文行号均指本轮实际读取版本；上游 GitHub 行号均按实际取回原文件计数，不采用网页工具重排行号。

| 输入 | 本轮 SHA-256 |
|---|---|
| 修订正文 | `9850a72823c6d6eb5a886c2a412b1682272a5901eb37688837deec0e640d16c6` |
| 作者取证 | `ba56a70d00da39b4ce13f9ba61f087c25c0a3650fad059b93e12b66c44e3e348` |
| 第一轮复核报告 | `de798aece5bb4eb8cd4daf98538e087cc2ef610a792ce9aea00d71a14a9f8011` |
| 初审报告 | `6ccc35c6ab87172679523121570440ae195ea77a2ecf06101993eb4c2f587dca` |
| 来源登记 | `656c2f814bb2b0a28bd60de2c3a113f133550ae0ddd12eb1c6e4305646354d15` |
| 完整覆盖任务表 | `53bfc8fe47d56ab322e546c853858cbaa90cf5a5d0305b33a80bab0f39275d54` |

### 1.1 只读重开与证据限制

- 使用只读 HTTP 取回 30 个上游文件/版本化页面，包括配套 Megatron 数据参数、blend/GPT 索引实现，NVLM SFT 脚本及其数据、模板、损失、loader 和 checkpoint 入口，PEFT/Transformers 源码和测试，以及 AMD/PyTorch 文档。均成功取得可读的预期内容；不下载或运行训练数据，不执行取回代码。
- 网页工具打开 AMD 兼容页返回 HTTP 429，打开 NVLM raw 脚本返回工具内部错误；同一精确地址的只读 `curl --fail --location` 已成功，且 AMD 页与 NVLM 脚本字节哈希均与既有记录一致。因此不是最终取证失败，也不是上游内容缺失。
- HIP 2.6 页本轮字节哈希与第一轮不同；版本化网页不是不可变快照。本轮按实际节内容判定，不由整页哈希变化推断后端语义变更。
- 官方测试仅阅读，未运行。未执行预训练、SFT、LoRA、合并、转换、安装或主动 GPU/NPU 操作；没有本库目标环境兼容、质量、吞吐、数据恢复或 optimizer 恢复的实测结论。
- 临时取回件与构建副本均在仓库外。下列 E 编号是本报告内部证据索引，不是新增 registry ID，也不把临时目录当长期证据附件。

### 1.2 精确上游证据索引

| 编号 | 本轮实际读取位置 | 本轮用途 |
|---|---|---|
| E01 | [Megatron core_v0.12.1 arguments.py](https://github.com/NVIDIA/Megatron-LM/blob/core_v0.12.1/megatron/training/arguments.py#L2244-L2275)；[MindSpeed-LLM v2.2.0 pretrain_gpt.py](https://github.com/Ascend/MindSpeed-LLM/blob/v2.2.0/pretrain_gpt.py#L247-L267) | 权重/前缀对、无权重前缀列表及独立 split 入口；MindSpeed 将其传入 blend 配置。 |
| E02 | 同一 core_v0.12.1 的 [builder](https://github.com/NVIDIA/Megatron-LM/blob/core_v0.12.1/megatron/core/datasets/blended_megatron_dataset_builder.py#L107-L126)（另核 L201–246、L551–578）、[BlendedDataset](https://github.com/NVIDIA/Megatron-LM/blob/core_v0.12.1/megatron/core/datasets/blended_dataset.py#L88-L103)（另核 L140–157）、[helpers.cpp](https://github.com/NVIDIA/Megatron-LM/blob/core_v0.12.1/megatron/core/datasets/helpers.cpp#L102-L126)、[GPTDataset](https://github.com/NVIDIA/Megatron-LM/blob/core_v0.12.1/megatron/core/datasets/gpt_dataset.py#L533-L582) | 样本配额、预构建的源/样本索引、无显式权重的分支，以及 GPT 子数据集为满足目标样本数而跨 epoch 重复原始文档的边界。 |
| E03 | [PEFT v0.7.1 peft_model.py](https://github.com/huggingface/peft/blob/v0.7.1/src/peft/peft_model.py#L647-L692)（另核 L160–202）；[LoraConfig](https://github.com/huggingface/peft/blob/v0.7.1/src/peft/tuners/lora/config.py#L45-L108)；[Transformers v4.43.2 Trainer 参数组](https://github.com/huggingface/transformers/blob/v4.43.2/src/transformers/trainer.py#L1063-L1080)（另核 L2873–2920） | adapter 配置、激活/可训练范围、adapter-only 保存与完整训练状态的差别；optimizer 按实际成员分组，不只比较组数。 |
| E04 | [PEFT testing_common.py](https://github.com/huggingface/peft/blob/v0.7.1/tests/testing_common.py#L516-L572)；[decoder 测试入口](https://github.com/huggingface/peft/blob/v0.7.1/tests/test_decoder_models.py#L165-L201)；[LoRA 显式错误路径](https://github.com/huggingface/peft/blob/v0.7.1/src/peft/tuners/lora/model.py#L353-L358)（另核 L421–424） | 合并、重载等价比较的对象；适配模型与裸基座的非等价断言；不支持模块/配置可显式报错。 |
| E05 | [core_v0.19.2 NVLM SFT 脚本](https://github.com/NVIDIA/Megatron-LM/blob/core_v0.19.2/examples/multimodal/nvlm/sft_qwen20_72b_internvit_6b.sh#L28-L38)（另核 L65–143、L150–162）；[NVLM README](https://github.com/NVIDIA/Megatron-LM/blob/core_v0.19.2/examples/multimodal/nvlm/README.md#L70-L82)；[sft_blend.yaml](https://github.com/NVIDIA/Megatron-LM/blob/core_v0.19.2/examples/multimodal/nvlm/sft_blend.yaml)；[nvlm_prompts.json](https://github.com/NVIDIA/Megatron-LM/blob/core_v0.19.2/examples/multimodal/nvlm/nvlm_prompts.json) | 官方多模态 SFT 配置确实存在；数据/模板配置入口、预训练 checkpoint 转换前提及两种装载路径。YAML 内有数据路径占位符，不是已绑定的本地数据集。 |
| E06 | 同 tag [dataset_helpers.py](https://github.com/NVIDIA/Megatron-LM/blob/core_v0.19.2/examples/multimodal/dataset_helpers.py#L155-L178)（另核 L276–289）、[train.py](https://github.com/NVIDIA/Megatron-LM/blob/core_v0.19.2/examples/multimodal/train.py#L115-L168)（另核 L244–254、L385–401）、[dataloader_provider.py](https://github.com/NVIDIA/Megatron-LM/blob/core_v0.19.2/examples/multimodal/dataloader_provider.py#L95-L141)（另核 L152–165） | 所选脚本确有对话 tokenize/labels、prompt/pad mask、loss 聚合、核心训练循环与可保存 loader 状态入口；不是沿用 0.12.1 mock 循环来证明 NVLM 行为。 |
| E07 | 同 tag [checkpointing.py](https://github.com/NVIDIA/Megatron-LM/blob/core_v0.19.2/megatron/training/checkpointing.py#L2092-L2104)（另核 L2472–2502、L2555–2606、L2627 起）；[training.py](https://github.com/NVIDIA/Megatron-LM/blob/core_v0.19.2/megatron/training/training.py#L2199) | `--load` 指定目录没有 checkpoint 时，才回退至 `--pretrained-checkpoint` 并设置 finetune；两条分支的 iteration、optimizer/scheduler、RNG 责任不同。 |
| E08 | [AMD docs-7.1.1 PyTorch compatibility](https://rocm.docs.amd.com/en/docs-7.1.1/compatibility/ml-compatibility/pytorch-compatibility.html)，Support overview、Version support、Docker image compatibility、各版本特性节；[PyTorch 2.6 HIP](https://docs.pytorch.org/docs/2.6/notes/hip.html)，Checking for HIP、TensorFloat-32、torch.distributed backends | 核对实际版本线、Linux 范围，以及 HIP 2.6 页明确列出的后端和 TF32 条件；不据此推出固定 HF/模型/外部扩展兼容。 |
| E09 | [Transformers causal LM collator](https://github.com/huggingface/transformers/blob/v4.43.2/src/transformers/data/data_collator.py#L803-L825)、[Llama loss](https://github.com/huggingface/transformers/blob/v4.43.2/src/transformers/models/llama/modeling_llama.py#L1163-L1174)；[Llama3 预训练脚本](https://github.com/NVIDIA/Megatron-LM/blob/core_v0.19.2/examples/llama/train_llama3_8b_h100_fp8.sh#L55-L78)；MindSpeed [requirements](https://github.com/Ascend/MindSpeed-LLM/blob/v2.2.0/requirements.txt)、[install_guide](https://github.com/Ascend/MindSpeed-LLM/blob/v2.2.0/docs/pytorch/install_guide.md#L56-L79)、[README](https://github.com/Ascend/MindSpeed-LLM/blob/v2.2.0/README.md#L57-L95)、[全参 SFT 脚本](https://github.com/Ascend/MindSpeed-LLM/blob/v2.2.0/examples/mcore/llama2/tune_llama2_7b_full_ptd.sh) | 仅对关联改动抽查 C01/C02/C06/C09；不重做与本轮无关的全篇初审。 |

## 2. 前轮 OPEN 项逐项判定

判定以当前正文及精确来源为准，不以作者“已补充”的说明代替核验。未完成原关闭条件的残余仍使用原编号；新加入的具体错误另记 S2 编号。

### B24-T063-C03 — CLOSED（原 P2）

正文 L95–106 已形成三类操作矩阵，L104 新增的最低配套身份清单将基座 checkpoint、tokenizer、模板/prompt-type、adapter 配置与权重修订、训练数据修订成组核对；resume 另列 optimizer/scheduler/步数/RNG/数据游标，明确不属于 adapter-only 工件。可训练集合按实际配置、active adapter 和 `is_trainable` 责任没有被删掉。

本轮重点核对的 param group 要求也已从“数量”推进到**逐组成员、稳定参数身份、每组超参及 state 键对应**，并指向[Checkpoint 恢复一致性](../../knowledge/06-training/checkpoint-state-consistency.md)的精确字段、状态内容和同输入单步契约。它与 E03 中 Trainer 实际按可训练参数及衰减规则分组一致。L136 的第一步检查仍只简写“参数组数量”，但全文 L104 已明确不能只数数量，故不将这一简写重复判成 C03 未修复。该 CLOSED 不表示已成功恢复任何 checkpoint。

### B24-T063-C04 — CLOSED（原 P2）

正文 L136、L137 分开装载等价检查与换目标后的独立质量基线，保留同输入、监督 mask、模式、随机性、数值条件、预定义容差及第一步可训练集合/梯度检查。L152 已删除“契约错位都不会显式报错”的绝对化，明确区分**显式配置/装载失败**与**可能静默的质量异常**。E04 的不支持 target module/配置的 ValueError 路径支持前者；正文没有声称所有模板错配都一定静默。原残余关闭，等价对象的范围另按 R02 判定。

### B24-T063-C05 — OPEN（P2）

已补足：正文 L73–77 区分 blend/split/pack；将权重落点写成目标样本数而非 token 配额；区分样本比例与有效监督 token 比例；三类操作的数据游标/RNG 也已明确为推理不适用、同阶段 resume 恢复、新阶段重置并归档前阶段消费统计。作者 L134 与这些实际修订对应。

**尚未补足原关闭条件中的采样/重复语义。** L77 只说明“构建期确定，不是运行期按 token 动态重采样”，没有说明如何沿预构建源/样本索引消费，以及为满足加权样本目标时原始语料是否可能被重复使用。E02 显示：权重不仅参与子数据集配额，也参与顶层混合索引；`__getitem__` 按该索引选源和源内样本。GPT 子数据集在请求量超过单 epoch token 数时增加 epoch，并重复、打乱文档索引。无显式权重的长度推断分支又有“不额外采样”及长度封顶条件，不能把两类分支混成一个无重复保证。

本轮**不把“不做运行期 token 动态重采样”判为错误**，也不要求逐行抄写构建公式或发明推荐比例；问题是这句话没有交付原 C05 要求的“重复/重采样究竟发生在哪里、如何计量”。L120 的去重观察要求仍不能替代该机制解释。最低剩余工作：在选定 core_v0.12.1 GPT/blend 范围补明加权目标、预构建索引及底层多 epoch 重复之间的关系，限定长度推断分支，并将这些条件与按源消费/重复统计对应。未知推荐比例可继续 unknown。

### B24-T063-C07 — CLOSED（原 P2，限模型级官方配置与入口取证）

正文 L143 继续明确 0.12.1 最小循环是合成数据演示，并已在独立 core_v0.19.2 档案给出真实模型预训练配置及**多模态 NVLM SFT** 脚本。作者补证 L137 和 registry 相应 notes 的脚本路径、哈希与本轮实取一致。

本轮沿新增脚本只读追踪确认：数据入口为 `sft_blend.yaml`，prompt 文件与 qwen2p0 格式明确；TaskEncoder 对话 tokenize 产生输入/标签；`train.py` 移位标签、屏蔽 pad/prompt、聚合 loss，并把数据 provider 和 forward_step 交给核心 `pretrain`；脚本另含保存/装载、预训练 checkpoint 和 dataloader 状态目录，loader 有状态恢复入口（E05–E07）。因此原先“只有 mock 最小循环、没有选定模型 SFT 配置和对应入口”的缺口已补足。

**不额外把“纯文本 LLM SFT 专项未逐目录定位”升级为新的必需验收项**：原任务没有限定只能用纯文本模型；正文已经明确 NVLM 多模态范围，并把纯文本专项缺口保留为有限 unknown。此关闭也不表示数据路径占位符已填写、完整 SFT 数据已取得、脚本可运行或 loader 恢复可靠。新增文字对 `--load` 起点的解释有另一个具体错误，单列 **S2-01**；不能由本项 CLOSED 推出 NVIDIA 平台状态示例整体已通过。

### B24-T063-C08 — OPEN（P2）

正文 L145 新增的具体版本值已核对正确：AMD 页日期为 2025-12-10、适用 Linux，分别有 PyTorch 2.9 / ROCm 7.1.1、2.8 / 7.1、2.7–2.8 / 7.0 特性节；没有把这些节与 HIP 2.6 拼成单一支持组合。固定 HF 组合及 PyTorch 2.6 的具体镜像/驱动配套继续 unknown，本库未执行也已单列。这些改进有效。

但 HIP 部分仍只写“可用后端范围与 TF32 说明”，**没有写出已经能从该精确来源核对的条件值**。E08 的 PyTorch 2.6 页明确限定 `torch.distributed` 为 `nccl` / `gloo`，且该版本页写明 ROCm 不支持 TF32；检查 HIP 的 `torch.version.hip` 判别也可直接核对。作者 L138 只是继续列主题，没有把条件提炼进正文。对 GPU 型号、具体 OS 发行版/驱动和模型外部内核/扩展，本轮修订同样未明确列出核查与未核查范围；“Applies to Linux”本身不构成任意 Linux/GPU 组合支持。

最低剩余工作：把实际采用的版本化后端/功能限制写成可读条件，明确硬件、OS 细分与外部扩展的未核查边界。HIP 2.6 的限制只能绑定该版本文档，不能外推为所有 ROCm 版本的永久限制；不要求制造 AMD 可运行样板。

### B24-T063-R01 — CLOSED（原 P2）

正文 L73 已删除 `--data-weight`，改用 `--data-path` 的权重/前缀对与纯前缀列表，后者按长度推断权重；独立 train/valid/test 入口与 E01 的 help 一致。作者 L133、registry 既有 Megatron 来源的补充核对都能对应同一 tag 和参数文件哈希；MindSpeed E01 将这些 data-path 参数接到 blend 配置。R01 的字段真实性问题关闭，采样/重复机制残余仍归 C05，不重复计数。

### B24-T063-R02 — CLOSED（原 P2）

正文 L136 已把等价检查限定为**同一目标权重及相同 adapter 组合的不同表示/装载**，有意换已训练 adapter/基座的操作明确排除，改用已知正确的目标复合模型作装载参考并建立独立质量基线。E04 比较同一适配模型的合并/重载结果，并另要求其与裸基座不同，与修订后的范围一致。第一步检查与平台容差仍未冒称已执行；不再要求任意旧、新模型相互等价。

### B24-T063-R03 — CLOSED（原 P3）

正文 L21 已加入既有 `src.pytorch.hip-notes-2.6`，与 L145 实际采用的精确 HIP 页、registry L3547 起条目对应，没有重复登记。机器可读依赖遗漏关闭；这不代替 C08 尚缺的正文条件提炼。

## 3. 已 CLOSED 项关联回归抽查

| 编号 | 本轮关联抽查 | 判定 |
|---|---|---|
| C01 / 原 P2 | L62–63、L118 仍按实际计损预测位置除以经过时间，区分 HF 移位/忽略索引与 MindSpeed loss_mask，要求说明计时及跨 rank 口径；新增混合节没有改回原始 labels 通用计数。E09 与 E01 对应路径未见回归。 | **维持 CLOSED** |
| C02 / 原 P2 | L45、L84、L89、L121、L149 仍区分目标轴与参数轴、纯 LoRA 与 bias/modules_to_save 扩展、基座可用与每设备全量驻留；新身份清单要求记录实际可训练范围，没有重引入按方法名推断全部状态的错误。 | **维持 CLOSED** |
| C06 / 原 P2 | L143、作者 L125 和两个独立 Megatron registry 档案继续保留目录否定断言的更正；新 NVLM 脚本进一步支持 0.19.2 有模型级配置。E09 重开 Llama3 脚本未见回归；本轮未重下整包，不冒称重新核完其完整目录。 | **维持 CLOSED** |
| C09 / 原 P3 | L144、L156 的 requirements/install_guide/README 近邻链接、HF 模型覆盖版本与在研配套限定保留，E09 取回对应内容；没有把其他模型版本或官方 Pass/Test 扩为本库硬件验证。 | **维持 CLOSED** |

## 4. 本轮新发现

### B24-T063-S2-01 — NVLM SFT 的首次阶段起点与恢复目录被混为一谈

- **优先级 / 状态：P2 / OPEN。**
- **位置：**正文 L143 将 `--load ${FINETUNE_DIR}` 概括为“起点”；作者补证 L137 只证明脚本存在，registry L6111 的新增 notes 也只列 `--load`，没有解释另一入口及其选择条件。
- **直接证据：**E05 脚本 L28 将 `FINETUNE_DIR` 定义为本次输出 checkpoint 目录；L32–36 另定义从预训练结果转换来的 `CHECKPOINT_DIR`。L113–116 同时设置保存到 FINETUNE_DIR、从 FINETUNE_DIR 装载、dataloader 保存目录及 `--pretrained-checkpoint ${CHECKPOINT_DIR}`。README L72–79 要求先把预训练 checkpoint 转为 PP=4，再用于 SFT。E07 loader L2092–2104 只有在 `--load` 目录不存在 checkpoint 时，才选择 pretrained_checkpoint 并置 `args.finetune=True`；若存在，则走目标目录恢复路径。L2472–2502、L2555 起等进一步区分 iteration/消费计数与 optimizer/scheduler/RNG 状态责任。
- **问题与影响：**正文省略了首次 SFT 的预训练来源及回退条件，读者可能把 FINETUNE_DIR 当作已准备好的阶段起点，或以为反复启动总是从预训练权重重新微调。实际是否已有输出 checkpoint 会改变所选权重及继承状态，正是本页应辨明的“新阶段微调 vs 同阶段 resume”。本轮没有运行脚本；这里判断的是固定版本配置与源码逻辑，不是报告发生过错误恢复。
- **关闭条件：**区分“首次 SFT / 无输出 checkpoint”和“已有 SFT checkpoint 的 resume”，分别交代 pretrained_checkpoint、load/save、必要的预训练 checkpoint 转换、步数/optimizer/RNG/数据状态责任与失败停止条件。补同 tag 精确入口，不把该行为外推到其他脚本。无需复制执行命令或制造运行成功记录。
- **与 C07 的关系：**C07 原缺口是官方模型级 SFT 配置和循环入口未取得，现已取得并独立核对；本项是新加脚本摘要中的具体状态语义错误，单独计数，不重复计算“纯文本专项 unknown”。

## 5. 任务验收重新核对

| T06-03 验收条目 | 本轮结果 |
|---|---|
| 1. 四类工作流；监督目标、token/mask/label、样本混合、阶段切换 | **部分满足，未通过。** 目标/参数轴及损失口径维持正确，三类操作的游标/RNG 已补；采样与底层重复语义仍未完成 C05 的原关闭条件。 |
| 2. 数据/模型/tokenizer/adapter 身份、可训练集合与 optimizer；精确合并/恢复边界 | **通用契约已补足，平台实例仍需修订。** C03 的最低配套清单和成员级映射已闭合，合并/完整 resume 边界保留；NVLM 新阶段起点不能按现摘要使用，见 S2-01。 |
| 3. token 吞吐、质量曲线、重复/遗漏、显存与 I/O 口径 | **观察口径满足。** 吞吐计量、按源去重、显存与 I/O 限定保留；不把观察口径的满足当成 C05 重复机制已交付，也不将质量曲线解释为跨目标必须连续。 |
| 4. mask/label、污染、adapter 与状态异常；阶段转换验证 | **通用区分检查满足，平台状态示例仍受 S2-01 阻断。** C04/R02 已纠正；污染重叠只是线索，两类异常均需检查，验证方法仍明确未执行。 |
| 5. NVIDIA/Ascend 锁定配置；AMD 官方执行边界，不任意扩兼容 | **部分满足，未通过。** NVIDIA 已有固定多模态 SFT 及循环取证，但需纠正装载分支摘要；Ascend 版本边界未回归；AMD 的版本线已具体化，后端/功能条件与未核查层次仍缺，C08 未关闭。 |

任务的三条 `source_discovery` 另行核对：

1. **HF 固定版本文档/源码与测试：取证条件满足。** 保存、合并、加载、Trainer 状态及同输入官方测试已读；这不是本库 resume 或合并验证通过。
2. **Megatron/MindSpeed 所选模型配置与核心循环对应：在已选官方示例范围内已取得。** NVLM SFT 的数据/模板/损失与状态入口本轮可独立连通；不把模态不同、有限纯文本专项 unknown 或路径占位符改称已实测的完整生产工作流。取证成立不免除 S2-01 的错误解释。
3. **原始 LoRA 论文只解释方法：维持原审阅边界满足。** 本轮没有修改或新增论文数字主张，未重新核 PDF 全文，不将其论文实验结果外推为平台收益。

## 6. 元数据、结构检查与变更边界

- 稳定 ID、标题/H1、主归属、`type: concept`、`status: draft`、`platforms: [generic]`、`verification.status: source_checked` 保留。`updated_at: "2026-10-18"` 早于本轮日期，并非未来验证日期；不擅自替作者更新。正文现有 13 项 source_refs 均能解析，4 项 related_ids 保持有效。
- 主体仍归 06 章，04/08 章通过链接承担文件持久化、数据路径和证据方法；RL rollout 仍是后续入口。没有因补脚本而宣称未来网站/API、平台迁移或硬件能力已实现。
- 不修改许可与再分发口径；报告仅给短标识、链接与原创判断，不导入大段上游代码、原始网页或大型日志。

实际检查记录：

1. 在原工作树执行 `PYTHONDONTWRITEBYTECODE=1 make check`，报告写入前后均 **PASS：103 content entries / 493 sources**。它检查结构与本地引用，不检查技术正确性或远程链接。
2. 为遵守“只新增一个文件”，没有在原工作树重写 `build/`。使用仓库外临时副本（保留已有 build，排除 `.git/`、`.venv/`、`.agents/`、`.codex/`），通过本仓库 Python 的绝对路径执行 `PYTHONDONTWRITEBYTECODE=1 make -C <临时副本> PYTHON=<本仓库 .venv/bin/python 的绝对路径> build`：**PASS：103 content entries / 493 sources**，生成副本内 catalog。报告写入后同步该报告并再次构建通过。这不是无既有 build 的纯净 bootstrap 测试，也不声称原工作树 build 已更新。
3. `git diff --check` 通过；以复核开始时的已跟踪与未忽略未跟踪文件 SHA-256 清单逐项复验，既有文件均未变化，新增集合仅为本报告。保留开始时已有的所有未提交修改与未跟踪文件。
4. 未修改 `src/kb/`，未增加内容测试，也未运行与报告无关的测试套件。结构检查与构建不能提升任何硬件验证状态。

## 7. 结论与下一轮最小范围

**暂不通过。** 本轮要求重核的 8 项中，C03/C04/C07/R01/R02/R03 共 **6 项 CLOSED**，C05/C08 共 **2 项 OPEN**；前轮 4 项 CLOSED 维持不变。新增 **1 项 OPEN P2：S2-01**。全部已记录编号合计 **CLOSED 10 项 / OPEN 3 项（3 P2、0 P1、0 P3）**。

用户要求的“全部前轮 OPEN 项 CLOSED，且无新 OPEN P1/P2”两项均未满足。下一轮只需围绕 C05 的采样/重复机制、C08 的实际条件值与未核查边界、S2-01 的首次 SFT/resume 分支修订并定向重核关联段落；不要求额外扩成纯文本 SFT 全面调研，也不要求为关闭来源审阅问题而运行训练或硬件实验。

## 附录：关键取回对象校验

| 对象 | 本轮 SHA-256 |
|---|---|
| core_v0.12.1 arguments.py | `f2a56f59b4ebd3913fdda687872e20a4c0f7e434d3166867f068b8ec9a92d454` |
| core_v0.12.1 blended_megatron_dataset_builder.py | `f41e2eb71bf0cb5c9a972a2294642c65edf542ea0d2abf3a6dae75f69b5c5c69` |
| core_v0.12.1 gpt_dataset.py | `3c7fecd01608f8af5fa23589905ed80b6a602bfd303645c389c17e2599ed50f3` |
| core_v0.19.2 NVLM SFT 脚本 | `d96068afbe20ff53dc1ecf4a4321d203e18bc10b98c221bd945bfdc63a1e354b` |
| PEFT v0.7.1 testing_common.py | `1e2e7fd4e2ca6836362a4da7d1d46601b6b417a3160b18bd5b9f70a98560503d` |
| AMD docs-7.1.1 兼容页 | `79c10c8262d804ff735c65198a12e72875b768869d8f180c2bb69c94bb85d85c` |
| PyTorch 2.6 HIP 页 | `2ba49fd5368bd93fadcb9f326f7c54695c4aeb0c1e7e388bf4f2ef1acc4aa5d1` |

校验值只标识本次取回内容，不证明脚本执行成功；具体文件、tag 和支持范围见 E01–E09。
