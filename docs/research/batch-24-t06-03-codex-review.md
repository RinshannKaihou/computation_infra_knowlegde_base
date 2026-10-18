# Batch 24 · T06-03 Codex 技术审阅报告

- 审阅日期：2026-10-18（Asia/Shanghai）。
- 结论：**暂不通过**。
- 发现：**P1 0 项、P2 8 项、P3 1 项，共 9 项，全部 OPEN**。存在 OPEN P2，须修订并经同一审阅者定向复核后再判断是否通过。
- 执行者：本会话 Codex，独立技术审阅角色；未派发子代理，未修改正文、导航、取证记录、来源登记或任务计划。本轮仅新增本报告。
- 模型审计边界：当前会话未提供可独立核验的实际后端模型、推理档位和路由元数据，记录为 `unknown`。不把文档中的模型约定或导航标注当作本轮执行证明，不声称另行完成指定模型路由验真或额外 CLI 审阅轮次。

## 1. 审阅范围与方法

### 1.1 输入与基线

已读取 `README.md`、`docs/authoring-guide.md`（特别是第 5–7 节）、`content-outline.md` 和 `schemas/content.schema.json`。审阅以任务定义和技术证据为准，结构检查成功不代替技术验收。

| 对象 | 本轮范围 |
|---|---|
| 任务 | [完整覆盖任务表](../../plans/full-coverage-backlog.yaml) L5930–5972 的 T06-03；完整读取 objective、五条 acceptance、source_packages、existing_source_ids、source_discovery、depends_on、context_topic_refs 和 targets |
| 正文 | [预训练与微调工作流和状态契约](../../knowledge/06-training/pretraining-and-finetuning.md) L1–113，含完整 front matter、全部表格和各节 |
| 作者取证 | [T06-03 来源记录](batch-24-t06-03-sources.md) L1–121，含版本选择、哈希、主张定位、unknown 和五条建议登记项 |
| 导航 | [06 训练与后训练系统](../../knowledge/06-training/index.md) L1–104；重点核对 L24、L44、L67 |
| 来源 | [来源登记表](../../sources/registry.yaml) 中全部 11 个 source_refs 对应项；另核对作者记录提及的 `src.pytorch.hip-notes-2.6` |
| 上下文 | 核对前置任务 T06-02、04.3/04.6 的职责边界及四个 related_ids；A10/A13/A18/S21/S25 是来源工作包，不是已完成核验的证据 |

本轮不改变任务仍为 `planned`、`needs_source_preparation`、`source_revision: null` 的状态，不替 T06-04/RL rollout 或整个 Batch 24 作验收。

| 基线文件 | SHA-256 |
|---|---|
| 正文 | `3e7b105cc1b119080ba1404e1e873f3e578b7e9b51ad028ad1bd2dfdd5b438ae` |
| 作者取证记录 | `59fa93af94db1e192dc749700d6114a89bf17cfea3fa575d76e172486eebda07` |
| 训练导航 | `300b3a5a3a3d05db0da0dfb380c7d88a12a8841a2dbc958fcd9407f02d73b049` |
| 完整覆盖任务表 | `53bfc8fe47d56ab322e546c853858cbaa90cf5a5d0305b33a80bab0f39275d54` |
| 来源登记表 | `5f5a04731081d986d6fed0d22d29bb16c25ea39682795243e29e8e08ea4ab406` |

### 1.2 独立核对方式和限制

1. 通读正文与作者记录后，使用只读 HTTP 请求重新取回正文引用的 GitHub 固定 tag 文件、论文摘要页和对应登记页；GitHub blob 地址使用同仓库、同 tag、同路径的 raw 入口取回。以实际文件字节计算 SHA-256，以 `nl` 的原文件坐标核对行号，不采用网页工具重排后的行号。
2. 第一组 23 个请求全部成功，覆盖正文全部显式远程链接及补充的 requirements、install_guide、README、CCLoRA 文档和相关登记页。另取回四个固定版本源码文件，用于检查初始化、label shift、真实 loss mask 和 pack 边界。
3. 为核对作者关于目录缺失的断言及任务要求的测试证据，尝试 GitHub tree API；两次请求均返回 HTTP 403：PEFT `v0.7.1` 和 Megatron `core_v0.19.2` 的递归 tree **未能独立重开（GitHub API 拒绝访问）**。随后分别从 codeload 成功取得相同 tag 的源码包，实际枚举目录并读取选定文件。没有把 API 错误当成文件不存在的证据。
4. 作者提供完整单文件哈希的 10 个对象全部与本轮取回字节一致，见附录 A。未重新下载作者的 MindSpeed-LLM v2.2.0 和 Megatron core_v0.12.1 整包，不声称独立确认其整包哈希；相关关键文件已逐文件核对。
5. 仅读取上游测试代码，**未执行这些测试**。未执行预训练、SFT、LoRA、合并、转换、主动 GPU/NPU 检查或任何安装命令；没有本地性能、质量、兼容性或恢复结果。
6. 取回件与构建副本放在仓库外临时目录；报告给出精确 URL、原文件位置与关键哈希，临时目录不是永久证据附件。正文没有引用、作者也没有取回的 LoRA PDF 全文仍不在本轮核验范围。

## 2. 精确上游证据与逐节抽查

下表的 E 编号仅为本报告内部证据索引，不是新增的来源登记 ID。链接均为实际重开的固定版本文件或版本化页面；源码行号是原文件坐标。每个正文小节均至少检查一组主张与证据的对应，不能对应的部分计入发现或保留未证实状态。

| 编号 | 精确证据、位置 | 抽查对象与结果 |
|---|---|---|
| E01 | [LoRA 摘要页](https://arxiv.org/abs/2106.09685)，页面标识 v2、2021-10-16 修订；完整字节哈希与作者一致 | “定义与要解决的问题”L43–50：冻结预训练权重、低秩适配及原论文的参数/内存数字有摘要依据；数字没有转写为本库平台收益。摘要不把 PEFT 整体限定为 SFT，见 C02 |
| E02 | [Transformers v4.43.2 data_collator.py](https://github.com/huggingface/transformers/blob/v4.43.2/src/transformers/data/data_collator.py#L312-L322)，另查 L679–690、L803–825 | “token/mask/label 契约”L56：所引默认值存在，但 L312 所在对象是 token classification collator；因果 LM 分支 L821–824 从 input_ids 构造 labels 并忽略 pad，不能据此推导自动屏蔽 prompt。正文把 prompt 屏蔽责任留给数据管道的限定正确 |
| E03 | [PEFT v0.7.1 peft_model.py](https://github.com/huggingface/peft/blob/v0.7.1/src/peft/peft_model.py#L160-L202)，另查 L647–692、L733–735 | “状态契约”L68、“合并与恢复”L72、“异常检查”L92：保存 adapter 权重/配置、选择性保存和加载默认不可训练有依据；同一 loader 还明确新 adapter 不会自动激活，且加载不恢复完整训练状态，见 C03 |
| E04 | [LoRA config.py](https://github.com/huggingface/peft/blob/v0.7.1/src/peft/tuners/lora/config.py#L45-L108)；[model.py](https://github.com/huggingface/peft/blob/v0.7.1/src/peft/tuners/lora/model.py#L235-L254)，另查 L429–456、L691–728 | “状态契约”L60–68、“常见误解”L106：默认 r、模块匹配、alpha/dropout 和合并 API 存在；同版配置还允许训练 bias、modules_to_save，不能概括为永远只训练低秩矩阵。safe_merge 文档检查的是 NaN 风险，不是质量等价证明 |
| E05 | [LoRA layer.py](https://github.com/huggingface/peft/blob/v0.7.1/src/peft/tuners/lora/layer.py#L168-L185)；[tests/testing_common.py](https://github.com/huggingface/peft/blob/v0.7.1/tests/testing_common.py#L516-L572)，另查 L457–482；[tests/test_decoder_models.py](https://github.com/huggingface/peft/blob/v0.7.1/tests/test_decoder_models.py#L165-L201) | “阶段转换验证”L96：默认线性 LoRA 的 B 零初始化；上游测试比较合并前后、保存重载后的同输入 logits。测试代码已读未跑，其容差不是目标平台的通用阈值。不能用跨阶段质量曲线连续性替代这些同条件检查，见 C04 |
| E06 | MindSpeed-LLM v2.2.0 [全参 SFT 脚本](https://github.com/Ascend/MindSpeed-LLM/blob/v2.2.0/examples/mcore/llama2/tune_llama2_7b_full_ptd.sh#L36-L75)、[LoRA 脚本](https://github.com/Ascend/MindSpeed-LLM/blob/v2.2.0/examples/mcore/llama2/tune_llama2_7b_lora_ptd.sh#L77-L99)、[预训练脚本](https://github.com/Ascend/MindSpeed-LLM/blob/v2.2.0/examples/mcore/llama2/pretrain_llama2_7b_ptd.sh#L68-L95) | “阶段切换的官方脚本证据”L76、“常见误解”L107：所列不载入 optimizer/RNG、finetune、指令数据、模板和 LoRA 参数确实存在。注意预训练示例也显式不载入 optimizer/RNG；参数是这些示例的选择，不是整个 SFT 类别的必然行为。split 不是样本混合方案，见 C05 |
| E07 | [Transformers Trainer](https://github.com/huggingface/transformers/blob/v4.43.2/src/transformers/trainer.py#L311-L327)，另查 L2873–2892、L2916–2920、L2931–2967 | “阶段切换”L76：IterableDataset 随机性和 tokenizer 随存的引文准确。真实 checkpoint 另存 optimizer/scheduler、RNG 和 Trainer 状态；仅保存/加载 adapter 不等于恢复该训练检查点，见 C03 |
| E08 | [MindSpeed pretrain_gpt.py](https://github.com/Ascend/MindSpeed-LLM/blob/v2.2.0/pretrain_gpt.py#L144-L165)，另查 L225–240、L247–263；[Transformers Llama 实现](https://github.com/huggingface/transformers/blob/v4.43.2/src/transformers/models/llama/modeling_llama.py#L1163-L1174) | “观察口径”L80–83、“异常检查”L89：真实计损 mask 与 raw labels 不等价；Llama 的 labels 在 loss 中移位，MindSpeed 单独聚合 loss_mask。有效监督 token 计数需要以实际损失路径为准，见 C01；blend 与 split 在配置中是不同字段，见 C05 |
| E09 | [CP 微调文档](https://github.com/Ascend/MindSpeed-LLM/blob/v2.2.0/docs/pytorch/features/fine-tuning-with-context-parallel.md#L18-L28)；[pack 文档](https://github.com/Ascend/MindSpeed-LLM/blob/v2.2.0/docs/pytorch/solutions/finetune/multi_sample_pack_finetune.md#L9-L21)；[CCLoRA 文档](https://github.com/Ascend/MindSpeed-LLM/blob/v2.2.0/docs/pytorch/features/cc_lora.md) | L56 的 CP 微调 general mask 限定有依据；pack 文档描述样本拼接与注意力边界，不是语料域采样比例。L76 对 lora-fusion 的特性归属可对应；没有采用文档性能表为本库结论 |
| E10 | [Megatron core_v0.12.1 最小循环](https://github.com/NVIDIA/Megatron-LM/blob/core_v0.12.1/examples/run_simple_mcore_train_loop.py#L21-L100)，另查 L107–155 | “NVIDIA 平台实践”L100：固定 tag 和循环真实存在，但模型是两层、hidden_size=12 的演示 GPT，使用 MockGPTDataset 和空 tokenizer；保存函数只展示模型分片状态，不是所选生产模型的完整预训练/SFT 状态配置。正文未明确标注“合成”，见 C07 |
| E11 | [Megatron core_v0.19.2 codeload 包](https://codeload.github.com/NVIDIA/Megatron-LM/tar.gz/refs/tags/core_v0.19.2)；实读 [Llama3 8B 脚本](https://github.com/NVIDIA/Megatron-LM/blob/core_v0.19.2/examples/llama/train_llama3_8b_h100_fp8.sh#L55-L72) 与 [GPT-3 脚本](https://github.com/NVIDIA/Megatron-LM/blob/core_v0.19.2/examples/gpt3/train_gpt3_175b_distributed.sh) | L100 以及作者记录 L5、L51、L101 的目录缺失主张不成立于本轮实际取回的 tag 档案；examples/llama 与 examples/gpt3 及具体模型字段均存在，见 C06。文件存在不等于配置可运行或与 Ascend 配套 |
| E12 | [MindSpeed requirements](https://github.com/Ascend/MindSpeed-LLM/blob/v2.2.0/requirements.txt#L1-L18)；[install_guide](https://github.com/Ascend/MindSpeed-LLM/blob/v2.2.0/docs/pytorch/install_guide.md#L56-L79)；[README 依赖表](https://github.com/Ascend/MindSpeed-LLM/blob/v2.2.0/README.md#L57-L95)；[MoE 模型表](https://github.com/Ascend/MindSpeed-LLM/blob/v2.2.0/docs/pytorch/models/moe_model.md) | “Ascend 平台边界”L101、“适用边界与来源”L113：HF 固定版本、按模型覆盖版本、Mcore 依赖、在研组件以及 Pass/Test 分级都能对应。README 的 PyTorch 为 2.7.1，不得与登记的 TorchNPU/PyTorch 2.6 快照自动拼成部署组合；正文目前未明确作这种拼配 |
| E13 | [AMD docs-7.1.1 PyTorch compatibility](https://rocm.docs.amd.com/en/docs-7.1.1/compatibility/ml-compatibility/pytorch-compatibility.html)，Support overview、Version support、Docker image compatibility、Key features 等节；[PyTorch 2.6 HIP semantics](https://docs.pytorch.org/docs/2.6/notes/hip.html)，Checking for HIP、torch.distributed backends 等节 | “AMD 边界”L102：官方后端支持条件与具体版本线可查，但不据此证明所选 Transformers/PEFT 版本、模型或外部内核的微调组合可执行，见 C08。保留 Megatron/MindSpeed 迁移 unknown 正确 |

另已成功取回登记的 [PyTorch 2.6 distributed](https://docs.pytorch.org/docs/2.6/distributed.html)、[DCP](https://docs.pytorch.org/docs/2.6/distributed.checkpoint.html)、[TorchNPU 固定快照入口](https://github.com/Ascend/pytorch/tree/bc51ab84cc6f35c77aab1c59886e0ea43681a317) 和 [huggingface_hub v0.33.0 入口](https://github.com/huggingface/huggingface_hub/tree/v0.33.0)。这些入口的存在不补足 adapter 续训证据，也不构成跨版本配套。未把入口页的可达性算作目标硬件技术验证。

## 3. 发现表

优先级：P1 表示高风险实质问题；P2 表示影响技术判断、状态/指标契约或任务验收的实质问题；P3 表示不单独阻断验收的可追溯性问题。以下各项均为 **OPEN**，建议关闭条件不是已完成的修订或复核。

| 编号 | 优先级 / 状态 | 位置 | 发现与证据 | 建议关闭条件 |
|---|---|---|---|---|
| B24-T063-C01 | P2 / OPEN | 正文 L56、L80、L89；验收第 1、3、4 条 | **有效 token 吞吐的分子/分母倒置，且监督 token 的计数被写成跨框架统一的非 -100 计数。** L80 写“分母只计参与损失的 token”，未给时间分母和单位。E08 的 Llama 实现对 labels 移位；MindSpeed 使用独立 loss_mask，E10 也以 loss_mask 参与计损。仅统计原始 labels 非 -100 会与实际被监督的预测位置不一致；attention_mask 也不能直接当 loss mask。 | 明确定义“计量窗口内实际计损的有效预测 token 数 / 对应经过时间”，给出 tokens/s、计时范围和跨 rank 去重/汇总范围；分别说明 HF label shift/ignore_index 与 Megatron/MindSpeed loss_mask 的映射。明确 prompt、pad、pack 边界检查，不把非 -100 作为通用实现。若放小型计数例子，须标注“合成”，不得写成实测。 |
| B24-T063-C02 | P2 / OPEN | 正文 L43–48、L60–68、L83、L92、L106；验收第 1、2 条 | **把训练目标与参数适配方法混成同一分类，并无条件断言 PEFT/LoRA 只训练低秩增量。** “LoRA/PEFT＝同 SFT”没有说明是本页选定的 LoRA-SFT 样板，而不是 PEFT 的定义。即便只看所引 PEFT v0.7.1，E04 config L57–61、L91–98 允许训练 bias 与 modules_to_save，model L235–254 有相应可训练分支。因此“requires_grad 集合恰为低秩增量”和“optimizer state 只覆盖增量”不适用于所声称的整个范围。 | 区分预训练/继续预训练/SFT 的目标轴与全参/LoRA/其他 PEFT 的参数轴；将本页具体比较明确限定为 LoRA-SFT，或补充其他范围。若采用纯 LoRA，明确 bias、modules_to_save 等限制；可训练集合、保存范围和 optimizer 参数组按实际配置核对，而不是按参数名称一刀切。资源结论同步保留分片、量化、offload 等未覆盖边界，不把“仍需基座”误写为每设备必须常驻完整权重。 |
| B24-T063-C03 | P2 / OPEN | 正文 L60–72、L76、L82、L92–94；验收第 2、4 条 | **adapter 身份、激活与完整续训的状态契约没有闭合。** 本页给出了配置字段和 is_trainable，却未列 adapter 工件身份与匹配基座/数据/tokenizer/模板修订的最低契约；E03 L651–654 还说明新加载 adapter 不会自动激活。E03 的保存接口只承诺 adapter 权重和配置；E07 L2873–2892、L2916–2920 另存 optimizer/scheduler、RNG、训练状态。仅“分离形态＋is_trainable”不能区分新阶段微调、同阶段 resume 和推理装载，tokenizer 随存也不能证明完整恢复。 | 给出这三类操作的继承/重置矩阵，列出基座和 adapter 不可变身份、配置、active adapter、可训练集合及 optimizer 参数组、scheduler/步数、适用的精度状态、RNG 和数据进度责任；可以链接既有 04/06 专题的具体契约，避免复制正文。明确 adapter-only 工件不自动具备完整 resume 状态，合并结果不能代替分离训练检查点。合并检查要区分数值比对与 safe_merge 的 NaN 检查，并补固定版本测试依据；未核实的反合并能力继续为 unknown。 |
| B24-T063-C04 | P2 / OPEN | 正文 L81、L96、L109；验收第 3、4 条 | **阶段转换验证使用了不可靠的跨目标连续性判据。** 新语料、模板、监督区域或指标改变时，前一阶段 loss 与新阶段 loss 不必连续。L96 又要求对同一校准 batch 的差异解释为“分布变化”，混淆了“同输入同监督的装载等价检查”和“换目标后的质量评价”。E05 默认 LoRA 初始化及同输入合并/重载测试提供的是前一种检查思路，不能用历史指标斜率证明状态契约正确；L109 对异常表现的绝对化也缺乏保证。 | 将未更新权重前的装载/适配/合并同条件 logits 或 loss 对照，与切换数据/目标后的独立基线和质量评估分开；声明需要固定的输入、监督 mask、模式、随机性与数值条件，容差由实际环境和验证计划决定。增加第一步更新的可训练参数/梯度/状态检查，并说明质量曲线只能提供线索；不同目标指标不可比时如实标注，不要求无依据的曲线衔接。 |
| B24-T063-C05 | P2 / OPEN | 正文 L46、L76、L82、L113；验收第 1 条 | **“样本混合”验收实际未交付。** 只有“可与旧语料混合”和“比例 unknown”，没有解释混合对象、采样单位/权重、重采样及阶段转换的数据进度责任。E06 的 split 是集合划分字段；E08 配置 L253–259 将 blend、blend_per_split 与 split 分列；E09 的 pack 是序列打包，不能用 split 或 pack 替代语料混合说明。 | 不必发明推荐比例，但需解释数据集混合、训练/验证划分与 pack 三者区别，以及样本级/token 级权重口径、数据修订、实际消费统计和阶段切换重置/继承策略。用精确固定来源支持所选实现；没有取证的比例和策略继续写 unknown，不能以比例未知为由省略机制。 |
| B24-T063-C06 | P2 / OPEN | 正文 L100；作者取证 L5、L51、L101；来源登记 `src.nvidia.megatron-examples-core-v0.12.1` 的 revision | **“core_v0.19.2 档案不含模型级配置示例 / examples/llama”的否定主张被本轮实际档案反证。** E11 实取包含 examples/llama/train_llama3_8b_h100_fp8.sh 和 examples/gpt3/train_gpt3_175b_distributed.sh；前者 L55–72 有明确模型结构字段。不能由目录检查不充分得出上游不存在，再把它作为样板降级的依据。 | 更正正文、取证记录及登记项的缺失断言；如作者原档案确实不同，应提供原包完整哈希、tag/commit 和目录清单解释差异，不能继续沿用无边界的否定。保留 core_v0.12.1 以对齐 MindSpeed 依赖本身可以合理，不要求切换版本；须把选择理由与“上游是否有示例”分开。新增脚本只可作来源记录，不能视为运行成功。 |
| B24-T063-C07 | P2 / OPEN | 正文 L100；作者取证 L35；任务 source_discovery 第 2 条及验收第 5 条 | **NVIDIA 侧只有合成最小循环，没有所选模型的预训练/SFT 工作流配置，且正文未标注“合成”。** E10 L39–51 的两层微型 GPT 和 L64–75 的 MockGPTDataset 只能支持循环示意；其 checkpoint 函数也只展示模型状态。作者记录识别了 mock，但正文平台实践没有把这一证据限制告知读者，不能据此认为模型级预训练/微调配置取证已完成。 | 将该例明确标注为“合成数据、最小循环演示，非性能/质量/生产恢复配置”；另补所选固定版本、选定模型的官方预训练/SFT 配置与真实数据/模板/损失/训练状态入口，或明确相关平台交付仍有缺口、不得验收通过。可以维持不同平台独立档案，不能拼配版本或复制脚本后声称已验证。 |
| B24-T063-C08 | P2 / OPEN | 正文 L102；作者取证 L42；验收第 5 条 | **AMD 执行边界被替换成生态归属推断，缺少本页实际采用的官方条件。** L102 只放登记 ID，并称 HF Trainer/PEFT 的相关部分“随其 ROCm 支持条件成立”，未列哪个 PyTorch/ROCm、硬件/OS 或算子/依赖范围。E13 可支持官方后端及指定版本线的声明，却不能自动外推到本页固定的 Transformers 4.43.2/PEFT 0.7.1 和某个模型。这里是支持证据缺口，不是已证明这些版本不兼容。 | 在正文近邻给出精确官方版本化链接，提炼与本页有关的后端支持条件，并把“官方声明的后端范围”“HF/模型/扩展尚未核实的组合”“本库未执行”分层。所选 HF 组合没有证据即保持 unknown；不必制造 AMD 可运行样板，不把 PyTorch 2.6 的 HIP 文档与 docs-7.1.1 的其他 PyTorch 版本线拼成一套环境。 |
| B24-T063-C09 | P3 / OPEN | 正文 L56、L100–101、L113 | **已核对正确的依赖与支持级别事实缺少近邻精确入口。** requirements 固定版本、install_guide 的 Mcore 依赖/模型覆盖版本，以及 README 在研组件在正文只有文件名或概述。E12 能支持这些事实，但正文给出的其他 URL 不能代替读者直接定位这些文件；`source_refs` 也不能替代论断附近的来源。 | 为 requirements、install_guide、README 依赖表补充相同固定 tag 的精确链接和原文件位置；让登记项能追溯实际支持文件。保留“在研”和按模型覆盖的限定，不扩写为兼容组合。 |

## 4. 验收条目逐条核对

| 验收条目（任务 L5946–5950） | 已交付且能对应的部分 | 缺口与判定 |
|---|---|---|
| 1. 四类工作流区别；监督目标、token/mask/label、样本混合和阶段切换 | 四行目标/数据表；HF ignore index 与 CP general mask 的基本来源；Ascend 阶段切换参数 | **部分满足，未通过。** 参数适配方法与训练目标的关系不清；跨实现 mask/shift 口径未闭合；样本混合机制缺失。C01、C02、C05 |
| 2. 数据/模型/tokenizer/adapter 身份、可训练参数与 optimizer 责任；精确的合并/恢复边界 | 状态表、部分 LoraConfig 字段、adapter 保存/加载默认值和合并 docstring | **部分满足，未通过。** 可训练集合过度概括；adapter 身份、激活与完整 resume 状态责任没有闭环。反合并 unknown 保留正确，不要求把未知写成支持。C02、C03 |
| 3. 有效 token 吞吐、质量曲线、重复/遗漏、显存与 I/O 观察口径 | 有四类观察项；重复/遗漏采用数据修订和去重键；I/O 正确指向 04 章 | **部分满足，未通过。** tokens/s 契约错误/不完整；质量曲线跨目标连续性的判据不成立；资源口径须随真实可训练范围限定。C01、C02、C04 |
| 4. mask/label、污染、adapter 加载、状态继承的区分检查及阶段转换验证 | 异常表覆盖这四类名称；训练/评测重叠检查属于可用的调查方法入口 | **部分满足，未通过。** 需要实际损失路径、active adapter 和完整恢复检查；阶段转换不应依靠分布解释或斜率判断契约正确。污染重叠只能作为证据线索，不是质量劣化根因证明；当前没有检测工具或运行结果。C01、C03、C04 |
| 5. NVIDIA/Ascend 锁定框架配置；AMD 官方执行边界，不声明任意模型兼容 | Ascend 三个 Llama2 脚本、requirements/Mcore 依赖与在研版本限定可对应；未宣称 AMD 任意模型可迁移 | **部分满足，未通过。** NVIDIA 只有合成最小循环，且上游配置缺失断言错误；AMD 缺可核验的条件和 HF 组合 unknown 分层。C06、C07、C08；追溯改进 C09 |

任务的三条 source_discovery 另外核对如下：

- **HF 固定版本文档与测试：部分完成。** 作者有源码/docstring，没有测试定位；本轮已只读核到 v0.7.1 保存/合并测试。作者仍需把与所写恢复/验证主张相关的测试边界纳入修订，不得把本轮阅读写成执行通过。
- **Megatron 与 MindSpeed-LLM 所选模型预训练/SFT 配置及循环对应：部分完成。** Ascend 侧有模型级脚本；NVIDIA 侧仍是合成演示，C07 未关闭。
- **原始 LoRA 论文只解释方法，不外推实验数字：满足当前摘要引用范围。** 摘要中的原论文数字明确标为论文环境结论，正文没有目标平台收益承诺；PDF 全文未核验。

## 5. 元数据、导航与硬规则检查

### 5.1 Front matter 与来源

- 稳定 ID 为 `training.pretraining-and-finetuning`，与任务 target 一致；`type: concept`、`domain: training`、`status: draft`、标题及 H1 一致，主归属正确。
- `updated_at: "2026-10-18"` 是合法字符串日期，与本轮日期一致；没有以未来日期充当已完成验证。
- `platforms: [generic]` 是概念覆盖范围，不是三平台兼容性证明。作为 concept，不强制要求 applicability；缺少环境档案不能改写为已验证配套。
- 11 个 source_refs、4 个 related_ids 和 4 个 verification.evidence_refs 全部能解析；作者建议新增的五个来源都已登记。取证中补用的 HIP 文档也有既有登记项。
- `verification.status: source_checked` 和 notes 明确没有执行训练/合并/转换，没有冒记 reproduced；但这一状态不豁免 C01–C08 的实质发现。`evidence_refs` 引用论文或源码只代表来源核对，不是硬件证据。
- 来源许可保留 unknown/partial 等边界；本轮仅链接、短字段定位与原创分析，不改变第三方材料许可，不为仓库增加统一再分发许可。

### 5.2 导航与内容边界

- 训练导航 L24 的 related_id，以及 L44、L67 的两处 Markdown 链接都指向本任务正确文件；导航把 RL rollout 留给后续批次，没有宣称已交付。
- 正文对并行策略、框架执行、数据路径和 checkpoint 持久化的本地链接存在；四个 related_ids 都属于现有内容。04.3/04.6 的文件语义没有被本页复制替代，训练状态仍归 06。
- “见 04 章”“见 08 章验收主题”是宽泛指引，不应被视为本页已经给出阶段转换的可核验标准；C03、C04 的关闭可以链接既有具体章节，不要求复制其正文。
- 本轮只审阅目标文件与必要上下文；不修改已有其他 Batch 24 审阅，不声称它们的问题已关闭，也不把前置任务状态自动视为已验收。

### 5.3 未知项和禁止外推

- 作者对未核实反合并能力、多 adapter/version 细节、转换脚本字段语义、TRL、具体混合比例和污染检测工具保留 unknown，属于正确的证据边界。发现 C03 要求的是恢复责任说明，不要求虚构这些能力。
- 所引 LoRA 数字仍是**来源记录**；CP/CCLoRA/模型表里的厂商性能数字没有转成普遍结论，本轮也没有增加任何收益或质量阈值。
- 模型/数据工件和真实 GPU/NPU 环境、实际兼容性、吞吐、质量、续训一致性仍未验证；上游测试存在或模型表标 Pass 都不能替代本库验证。
- **合成标注尚不合格的具体位置为 C07。** 本轮没有把合成数据、合成计数或未执行示例写成现场事实。

## 6. 结构检查与执行记录

1. 在原工作树执行 `PYTHONDONTWRITEBYTECODE=1 make check`：**PASS，103 content entries / 489 sources**。这只确认 schema、引用 ID 和本地文件链接。
2. 为遵守“只新增报告”，未在原工作树生成或覆盖 build。复制源树到仓库外临时目录后执行 `make build`；第一次副本排除了既有 build，因 `docs/first-fill-status.md` 的两个既有 catalog 链接目标缺失而失败。这是副本缺件，不归因于 T06-03，也没有修改相关源码。
3. 将工作树原有 build 文件一并复制到临时副本，再执行 `PYTHONDONTWRITEBYTECODE=1 make -C <临时副本> PYTHON=<本仓库 .venv/bin/python 的绝对路径> build`：**PASS，103 content entries / 489 sources**，生成该副本内的 `build/catalog.json` 和 `build/catalog.md`。不是干净无 build 目录的 bootstrap 测试，也不是原工作树已重建的声明。
4. 已检查临时 catalog 中目标记录：ID、draft、generic、updated_at、related_ids 和 verification 与源文件相符。未改动 `src/kb/`，未运行测试套件；本轮不声称训练代码、硬件或远端内容测试通过。

## 7. 结论与复核要求

**T06-03 暂不通过：8 项 P2、1 项 P3 均 OPEN；无 P1。** 需要先修订 C01–C08，再定向复核各条关闭条件及其影响到的验收项。C09 同步补齐追溯入口。不能仅凭构建通过、补上链接、报告写入完成或保留 draft 状态宣布技术审阅通过。

复核应重新读取修订正文及受影响的取证/登记项，重点检查：实际 loss mask 与 token 计量、LoRA/PEFT 范围、adapter 装载/激活/续训状态、阶段转换同条件检查与独立质量基线、样本混合机制、Megatron 档案目录及合成标识、AMD 官方后端条件与未证实 HF 组合。未开展真实环境验证的结论必须继续保留。

## 附录 A：独立取回的字节校验

### A.1 与作者完整哈希一致的 10 个对象

下列均为 2026-10-18 独立取回；源码使用上述同 tag、同路径的 raw 入口。表中原文件哈希与作者取证及对应登记项一致，不等于这些文件支持作者的全部解释。

| 对象 | SHA-256 |
|---|---|
| arXiv 摘要页 | `70bb70b4fd6d41b8a0f53fc5148017bf6ef5b73acba822027397f861aee135c6` |
| Transformers v4.43.2 data_collator.py | `5ee65cd10be88acb5525cc12076b8d6c0f2885844ce057662f917965fd4356fb` |
| PEFT v0.7.1 peft_model.py | `baeb93af9c9a75f1987f47e32e0ae512ea1b3b41158548d18296f8e408d74872` |
| PEFT v0.7.1 lora/config.py | `6e5446f2b0ed66247496f48cf856241885ae13aaeb0b873badf90f5c19bcee10` |
| PEFT v0.7.1 lora/model.py | `44e5ceebc868163c52bb5c0eebb992ed259769d2c5c39d21c26cca67bc621048` |
| MindSpeed v2.2.0 全参 SFT 脚本 | `a0705230d059995cfe820bad210ea0d8c2214dd281337d075ab14d409063d24c` |
| MindSpeed v2.2.0 LoRA 脚本 | `c9c85c81f8ec405fae960c3e8342c243bba2d326d13f9620499b58d04958752a` |
| MindSpeed v2.2.0 预训练脚本 | `e3bd82f5b1bc562af4c4dcdcc4e225a28eae32a09ff65af747dded8796cced41` |
| Transformers v4.43.2 trainer.py | `88320007d5b598d3d4b7e4af63ea47ef86e1877da6a5a3ae722cab5174edeb84` |
| Megatron core_v0.12.1 run_simple_mcore_train_loop.py | `5ed11bc7834177718e836da7e61e2b067256528b55821c0b8397b82e75773064` |

### A.2 补充语义核验的关键对象

| 对象 | SHA-256 |
|---|---|
| PEFT v0.7.1 lora/layer.py | `46ec9453fb9ca8d843ef1190a67c6b1bed2e5d917addc36e9027786b1c69e7cf` |
| Transformers v4.43.2 modeling_llama.py | `f4549647e6e3c0cd5f7c869ec16c6c82f318760d37f57d70f5a53afac5b302ed` |
| MindSpeed v2.2.0 pretrain_gpt.py | `b3ca649a9f11868da890a2af67b94ccacc938f1128272dfb569f7fac6d2ed549` |
| MindSpeed v2.2.0 multi_sample_pack_finetune.md | `113508437ecd6d4666218cae37c1dfed2fa3b5e02d1f08faf8084e4690ecdb04` |
| MindSpeed v2.2.0 requirements.txt | `b32319f8ddbff5f6610311159f4df6524e0ff501a32aa0a2de89077c5eb21053` |
| MindSpeed v2.2.0 install_guide.md | `8dd60a6cc0983ffcf1e1aaa84da2cba054d1362a7b53a6bffacd665c0bdad423` |
| MindSpeed v2.2.0 README.md | `7b4893c93e8884d18eb0ff5eee5291bd93eced52dd91572d6a2566c4a7b12f99` |
| MindSpeed v2.2.0 fine-tuning-with-context-parallel.md | `f899c7292961f6c5cd69eb9e46ccb9e2099c9c86e9fb5ca7fbcd77cb810bdc51` |
| MindSpeed v2.2.0 moe_model.md | `5119b6e207cf832844478be4665ddd544c53c01886ccef2d814f756666a0653a` |
| MindSpeed v2.2.0 cc_lora.md | `f974dcc69574a4482a7cf8beb673c49a4a6165515c946c7a594b21a929f743a3` |
| AMD docs-7.1.1 PyTorch compatibility 页面 | `79c10c8262d804ff735c65198a12e72875b768869d8f180c2bb69c94bb85d85c` |
| PyTorch 2.6 HIP 页面 | `96206063b54cff562b49bfc094fe16a0bcc1b85d65d17f15809594af36e7d23a` |

### A.3 目录反证与只读测试核对

PEFT 包入口为 [codeload v0.7.1](https://codeload.github.com/huggingface/peft/tar.gz/refs/tags/v0.7.1)，Megatron 包入口见 E11。以下四个文件从对应包直接读取；没有执行包内脚本或测试，也没有把它们解压到仓库。

| 对象 | SHA-256 |
|---|---|
| PEFT v0.7.1 codeload 包 | `4468f4f255ca8ddd7ec6eecf93d9481dc83d89bd689e520ef90057008211efb9` |
| Megatron core_v0.19.2 codeload 包 | `4c16ccc2a0d4c1b6c96f59baaab99316ac3b39eca2ef960ddf4436a2962eb69a` |
| core_v0.19.2 examples/llama/train_llama3_8b_h100_fp8.sh | `fddc588ca15f24384465f16e171147204feeb691f8fbc54b2a797cf135adc9cc` |
| core_v0.19.2 examples/gpt3/train_gpt3_175b_distributed.sh | `4bc0e0194fef6cdaf578fcf81259ec7de34b26fc1892741ab314827e23059952` |
| PEFT v0.7.1 tests/testing_common.py | `1e2e7fd4e2ca6836362a4da7d1d46601b6b417a3160b18bd5b9f70a98560503d` |
| PEFT v0.7.1 tests/test_decoder_models.py | `f2e5c4f211c80ff13a6b1c0bebfb9263f78b3cd020ae22ac0410ee1b2c6a392c` |
