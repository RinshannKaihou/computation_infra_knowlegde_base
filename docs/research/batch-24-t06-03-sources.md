# 第二十四批 T06-03 来源记录

任务：T06-03（预训练与微调工作流和状态契约；**new** concept `knowledge/06-training/pretraining-and-finetuning.md`，主题 06.4，后训练入口，RL 属 T06-04/Batch 25 不展开）。取证轮次：主会话作者角色首轮（2026-10-18；子代理 403，改主会话直接取证）。curl 字节级取回（SHA-256 见下）＋既有 codeload 源码包；未运行任何训练/转换命令。

版本选择口径：HF 侧版本**取自 MindSpeed-LLM v2.2.0 的 requirements.txt（transformers==4.43.2、peft==0.7.1）**，与既有固定样板形成同一依赖族；install_guide 另注明 qwen3/llama3.3 需 transformers 4.51.0、glm4.5-moe 需 4.54.0（按模型分列，不混同）。NVIDIA 侧 Megatron 示例固定 core_v0.12.1（与 MindSpeed-LLM v2.2.0 install_guide 指定的 Mcore 依赖一致）；Megatron core_v0.19.2（另一冻结档案）不含 examples/llama 等模型配置（tar 实开确认，仅 multimodal/post_training 等）。LoRA 论文仅用于方法边界。

## 本轮取回清单（2026-10-18）

| 对象 | 版本 | SHA-256（前 16 位） |
|---|---|---|
| huggingface/peft src/peft/peft_model.py | v0.7.1 | baeb93af9c9a75f1 |
| huggingface/peft src/peft/tuners/lora/model.py | v0.7.1 | 44e5ceebc868163c |
| huggingface/peft src/peft/tuners/lora/config.py | v0.7.1 | 6e5446f2b0ed6624 |
| huggingface/transformers src/transformers/trainer.py | v4.43.2 | 88320007d5b598d3 |
| huggingface/transformers src/transformers/data/data_collator.py | v4.43.2 | 5ee65cd10be88acb |
| arXiv:2106.09685 摘要页 | 观察日期 2026-10-18 | 70bb70b4fd6d41b8 |
| Megatron-LM examples/run_simple_mcore_train_loop.py | core_v0.12.1 | 5ed11bc783417771 |
| MindSpeed-LLM examples/mcore/llama2/pretrain_llama2_7b_ptd.sh | v2.2.0 | e3bd82f5b1bc562a |
| MindSpeed-LLM examples/mcore/llama2/tune_llama2_7b_full_ptd.sh | v2.2.0 | a0705230d059995c |
| MindSpeed-LLM examples/mcore/llama2/tune_llama2_7b_lora_ptd.sh | v2.2.0 | c9c85c81f8ec405f |
| MindSpeed-LLM requirements.txt（transformers==4.43.2、peft==0.7.1） | v2.2.0 | 见源码包 693f619a… |

注：PEFT v0.7.1 的 `PeftModel.py` 路径为 404，实际文件是 `src/peft/peft_model.py`（小写）。huggingface.co/docs 在线文档为可变页，未使用；证据全部锚定 tag 源码 docstring。

## 主张—来源定位表

| 主张 | 登记 ID | 精确位置 | 支持范围 / 未覆盖 |
|---|---|---|---|
| LoRA 方法边界（论文） | NEW src.paper.lora-2106.09685 | arXiv 摘要页 | 冻结预训练权重＋低秩矩阵 ΔW=BA；"unlike adapters, no additional inference latency"；GPT-3 175B vs Adam 全参微调：可训练参数减少 10,000×、GPU 内存 3×（**论文实验数值，不作目标平台部署效果**）；发布 PyTorch 集成包。方法论边界之外不引数值结论 |
| adapter 保存/加载身份 | NEW src.hf.peft-source-v0.7.1 | peft_model.py：`save_pretrained` L160（safe_serialization、selected_adapters）、`load_adapter` L647（**"Load a trained adapter into the model"，新 adapter 名须唯一、`is_trainable=False` 默认） | adapter 与基座分开保存/装载；**默认加载后不可训练**——"adapter 加载与状态继承异常"检查点的官方依据。version_requirements/多 adapter 并存细节未逐行核 |
| LoRA 合并语义 | NEW src.hf.peft-source-v0.7.1 | lora/model.py：`merge_and_unload` L691–699（把 LoRA 层并入基座、供 standalone 使用；safe_merge/adapter_names 选项） | 合并=权重改写+卸载包装层；合并后与原 adapter 的可逆性无承诺（反合并 API 未在该版本核对，unknown） |
| LoRA 配置身份 | NEW src.hf.peft-source-v0.7.1 | lora/config.py：`LoraConfig` L45+、字段 r=8 默认 L77、target_modules L78–82（模块名或正则）、lora_alpha/lora_dropout L52–53、scaling=alpha/r L74 | 可训练参数的配置身份（r/alpha/target_modules）；与 MindSpeed-LLM 脚本的 --lora-r/--lora-alpha/--lora-target-modules 对应 |
| Trainer 职责与中断续训入口 | NEW src.hf.transformers-trainer-4.43.2 | trainer.py：`class Trainer` L288（feature-complete training and eval loop、data_collator 默认行为）；train_dataset 参数说明 L311–319（**IterableDataset 需各进程一致 generator 或 set_epoch()**）；tokenizer 随模型保存以便 rerun interrupted training L324–327 | SFT 循环职责、数据随机性约束（与 06.1 RNG/DistributedSampler 主张互链）、恢复入口 |
| label/mask 语义 | NEW src.hf.transformers-trainer-4.43.2 | data_collator.py：`DataCollatorForLanguageModeling` L679+；`label_pad_token_id` 默认 -100（L312–313 说明 **-100 会被 PyTorch loss 自动忽略**；L322 字段默认） | 常见 mask/label 检查的官方依据（padding 位不进损失）；因果 LM 的完整 label 构造由应用负责 |
| Megatron 官方最小训练循环 | NEW src.nvidia.megatron-examples-core-v0.12.1 | examples/run_simple_mcore_train_loop.py（L1–60：parallel_state.initialize_model_parallel、TransformerConfig/GPTModel、get_forward_backward_func、torch Adam＋DataLoader、mock dataset） | "预训练循环=分布式初始化→config/模型→数据→schedule→optimizer"的最小官方样板，与 T06-02 训练循环条目互链；mock 数据仅演示，非性能口径 |
| MindSpeed-LLM 预训练配置 | NEW src.ascend.mindspeed-llm-workflows-v2.2.0 | pretrain_llama2_7b_ptd.sh（--tokenizer-type Llama2Tokenizer、--data-path、--split 949,50,1、--save-interval 10000、cosine lr 1.25e-6→min 1.25e-7、warmup 0.01） | 预训练的数据/tokenizer/保存节奏字段实例（与核心循环一致：脚本直接驱动 Megatron 参数） |
| MindSpeed-LLM 全参 SFT 配置 | NEW src.ascend.mindspeed-llm-workflows-v2.2.0 | tune_llama2_7b_full_ptd.sh（--load 预训练权重、--no-load-optim/--no-load-rng、--finetune、--is-instruction-dataset、--prompt-type llama2、--tokenizer-not-use-fast、lr 5e-5 cosine） | **阶段切换的状态契约**：SFT 载入权重但显式不载 optimizer/RNG；指令数据集与模板字段 |
| MindSpeed-LLM LoRA 微调配置 | NEW src.ascend.mindspeed-llm-workflows-v2.2.0 | tune_llama2_7b_lora_ptd.sh（--lora-r 16、--lora-alpha 32、--lora-fusion、--lora-target-modules linear_qkv linear_proj linear_fc1 linear_fc2） | Ascend 侧 LoRA 官方字段（模块名与 HF target_modules 同概念不同命名）；--lora-fusion 即 cc_lora 特性（见 T06-01 条目） |
| CP 微调边界（复用 T06-01 条目） | 复用 src.ascend.mindspeed-llm-parallel-features-v2.2.0 | fine-tuning-with-context-parallel.md（cp-size 整除、mask 只能 general、reset-position-ids） | 长序列微调的并行×数据契约；本轮未重开 |
| Ascend 转换/续训工具面 | 复用既有条目 | examples 内 ckpt_convert_*（hf2mcore/mcore2hf/lora2hf 等，本轮仅目录枚举） | 权重转换入口存在性；转换语义未逐脚本核对（unknown，正文只列名不展开） |
| PyTorch 状态契约基础 | 复用 src.pytorch.parallel-training-state-2.6＋src.pytorch.dcp-2.6 | （既有） | optimizer/scaler/RNG/数据进度的状态责任；本轮未重开 |
| AMD/ROCm 微调边界 | 复用 src.amd.pytorch-compatibility-7.1.1＋src.pytorch.hip-notes-2.6 | （既有） | PyTorch/ROCm 官方支持条件；Megatron/MindSpeed 可迁移性不声明（unknown） |

## unknown 清单

1. PEFT v0.7.1 的多 adapter 并存、`version` 兼容标记、unload/反合并语义未逐行核对。
2. HF 在线文档（huggingface.co/docs/peft、transformers）为可变页未使用；TRL SFTTrainer 未取证（MindSpeed-LLM 用 Megatron 循环而非 TRL；TRL 仅作可选后续）。
3. MindSpeed-LLM ckpt_convert_* 脚本的字段级语义未核对；adapter 合并与恢复边界只以 peft 源码与脚本参数为据。
4. 样本混合比例、数据污染检测工具：无一手固定资料（正文只给检查方法与观测口径，不引具体比例）。
5. LoRA 论文实验数值（10,000×/3×、各模型质量结论）只作为方法边界描述，不作为任何目标平台预期。
6. Megatron core_v0.19.2 档案不含模型配置示例（tar 实开）；NVIDIA 侧配置证据固定在 core_v0.12.1，与 MindSpeed-LLM v2.2.0 的 Mcore 依赖一致，两组档案不混用。
7. 全部脚本未运行；TP/PP/EP 等并行度组合因脚本而异，正文不从中归纳"最优配置"。

## 建议登记条目（5 条新增）

```yaml
- id: src.paper.lora-2106.09685
  title: LoRA: Low-Rank Adaptation of Large Language Models（arXiv 摘要页）
  url: https://arxiv.org/abs/2106.09685
  kind: paper
  registered_at: '2026-10-18'
  revision: arXiv:2106.09685 摘要页观察 2026-10-18（curl，SHA-256 70bb70b4fd6d41b8a0f53fc5148017bf6ef5b73acba822027397f861aee135c6）；未取 PDF 全文
  license:
    status: unknown
    scopes: []
    notes: arXiv 分发条款未核对；仅链接并原创归纳摘要主张。
  notes: Batch 24（T06-03）取证：LoRA=冻结权重+低秩 ΔW=BA；无额外推理时延（相对 adapter）；论文实验数值（GPT-3 175B 可训练参数 10,000×↓、GPU 内存 3×↓、RoBERTa/DeBERTa/GPT-2/GPT-3 质量结论）仅作方法边界，不作为目标平台部署效果。
- id: src.hf.peft-source-v0.7.1
  title: Hugging Face PEFT v0.7.1 PeftModel 与 LoRA 实现源码（冻结）
  url: https://github.com/huggingface/peft/blob/v0.7.1/src/peft/peft_model.py
  kind: repository
  registered_at: '2026-10-18'
  revision: tag v0.7.1；curl raw 取回 2026-10-18（peft_model.py SHA-256 baeb93af9c9a75f1987f47e32e0ae512ea1b3b41158548d18296f8e408d74872、lora/model.py 44e5ceebc868163c52bb5c0eebb992ed259769d2c5c39d21c26cca67bc621048、lora/config.py 6e5446f2b0ed66247496f48cf856241885ae13aaeb0b873badf90f5c19bcee10）；版本取自 MindSpeed-LLM v2.2.0 requirements（peft==0.7.1）
  license:
    status: partial
    scopes:
    - scope: PEFT v0.7.1 仓库源码（Apache-2.0）
      identifier: Apache-2.0
      url: https://github.com/huggingface/peft/blob/v0.7.1/LICENSE
    notes: 仅链接并原创归纳，不复制实现长段。
  notes: Batch 24（T06-03）取证：save_pretrained（safe_serialization/selected_adapters）、load_adapter（名称唯一、is_trainable 默认 False）、merge_and_unload（并入基座供 standalone、safe_merge）、LoraConfig（r 默认 8、target_modules 名或正则、lora_alpha/dropout、scaling=alpha/r）。未运行代码；多 adapter/反合并语义 unknown。
- id: src.hf.transformers-trainer-4.43.2
  title: Hugging Face Transformers v4.43.2 Trainer 与 data collator 源码（冻结）
  url: https://github.com/huggingface/transformers/blob/v4.43.2/src/transformers/trainer.py
  kind: repository
  registered_at: '2026-10-18'
  revision: tag v4.43.2；curl raw 取回 2026-10-18（trainer.py SHA-256 88320007d5b598d3d4b7e4af63ea47ef86e1877da6a5a3ae722cab5174edeb84、data_collator.py 5ee65cd10be88acb5525cc12076b8d6c0f2885844ce057662f917965fd4356fb）；版本取自 MindSpeed-LLM v2.2.0 requirements（transformers==4.43.2，install_guide 另注 4.51.0/4.54.0 按模型适用）
  license:
    status: partial
    scopes:
    - scope: Transformers v4.43.2 仓库源码（Apache-2.0）
      identifier: Apache-2.0
      url: https://github.com/huggingface/transformers/blob/v4.43.2/LICENSE
    notes: 仅链接并原创归纳。
  notes: Batch 24（T06-03）取证：Trainer 职责（feature-complete 训练/评估循环、data_collator 默认、tokenizer 随存以 rerun interrupted training、IterableDataset 需一致 generator 或 set_epoch）、DataCollatorForLanguageModeling 与 label_pad_token_id=-100（PyTorch loss 自动忽略）。未运行代码。
- id: src.nvidia.megatron-examples-core-v0.12.1
  title: NVIDIA Megatron-LM tag core_v0.12.1 官方示例（最小 MCore 训练循环）
  url: https://github.com/NVIDIA/Megatron-LM/blob/core_v0.12.1/examples/run_simple_mcore_train_loop.py
  kind: repository
  registered_at: '2026-10-18'
  revision: tag core_v0.12.1（codeload 源码包 2026-10-18，包 SHA-256 3e83d4a79014d77c121b257c03ba592b55bcc68ed24bece705e54978942e04d8；脚本 5ed11bc7834177718e836da7e61e2b067256528b55821c0b8397b82e75773064）；该 tag 为 MindSpeed-LLM v2.2.0 install_guide 指定的 Mcore 依赖；core_v0.19.2 档案不含 examples/llama 等模型配置（tar 实开）
  license:
    status: unknown
    scopes: []
    notes: Apache-2.0 为仓库主许可（未逐文件核对）；仅链接并原创归纳。
  notes: Batch 24（T06-03）取证：run_simple_mcore_train_loop.py（initialize_model_parallel→TransformerConfig/GPTModel→数据→get_forward_backward_func→torch Adam；mock 数据仅演示）。examples 另含 post_training/modelopt 配置目录（本轮未展开）。未运行代码。
- id: src.ascend.mindspeed-llm-workflows-v2.2.0
  title: MindSpeed-LLM v2.2.0 预训练/全参 SFT/LoRA 示例脚本与依赖清单
  url: https://github.com/Ascend/MindSpeed-LLM/blob/v2.2.0/examples/mcore/llama2/pretrain_llama2_7b_ptd.sh
  kind: repository
  registered_at: '2026-10-18'
  revision: tag v2.2.0；codeload 源码包取回 2026-10-18（pretrain e3bd82f5b1bc562af4c4dcdcc4e225a28eae32a09ff65af747dded8796cced41、full SFT a0705230d059995cfe820bad210ea0d8c2214dd281337d075ab14d409063d24c、LoRA c9c85c81f8ec405fae960c3e8342c243bba2d326d13f9620499b58d04958752a；requirements：transformers==4.43.2、peft==0.7.1）
  license:
    status: identified
    scopes:
    - scope: 固定 tag 的 examples 脚本与 requirements；根 LICENSE 声明范围
      identifier: BSD-3-Clause
      url: https://github.com/Ascend/MindSpeed-LLM/blob/v2.2.0/LICENSE
    notes: 不复制脚本长段，仅引用字段与默认值。
  notes: Batch 24（T06-03）取证：pretrain（tokenizer/data-path/split 949,50,1/save-interval、cosine lr）；full SFT（--load＋--no-load-optim/--no-load-rng＋--finetune＋--is-instruction-dataset＋--prompt-type）；LoRA（--lora-r 16/--lora-alpha 32/--lora-fusion/--lora-target-modules linear_qkv 等）。ckpt_convert_* 仅目录枚举未逐脚本核对。未运行任何脚本。
```

## 修订轮补充取证与更正（2026-10-18，初审发现 B24-T063-C01–C09 处理）

- **C06 更正（重要）**：首轮"core_v0.19.2 档案不含模型级配置示例（tar 实开）"的断言**不成立**——当时只对两个不存在的具体文件名做 raw 探测，未下载完整包。修订轮实取 core_v0.19.2 codeload 包（SHA-256 4c16ccc2a0d4c1b6c96f59baaab99316ac3b39eca2ef960ddf4436a2962eb69a，与审阅轮一致），examples/ 下含 llama/train_llama3_8b_h100_fp8.sh（fddc588c…）与 gpt3/train_gpt3_175b_distributed.sh（4bc0e019…）等；新登记 src.nvidia.megatron-model-configs-core-v0.19.2 并入正文 NVIDIA 平台实践；registry 的 src.nvidia.megatron-examples-core-v0.12.1 错误断言同步更正。
- **PEFT 测试补证（C03/C04）**：v0.7.1 tests/testing_common.py L516–572、tests/test_decoder_models.py L165–201（合并前后/保存重载的同输入 logits 对照；已读未运行）。
- **loss 路径补证（C01）**：Transformers v4.43.2 modeling_llama.py L1163–1174（labels 移位）与 MindSpeed pretrain_gpt.py（loss_mask 聚合）。
- **blend/split/pack 区分（C05）**：MindSpeed 配置中 blend/blend_per_split 与 split 分列；multi_sample_pack_finetune.md 为序列打包方案。
- 其余（C02/C07/C08/C09）为正文表述、合成标注与近邻链接修订；无其他新增上游材料。

## 修订轮二补充（2026-10-18，复核轮发现处理）

- R01：删除无依据的 --data-weight；混合入口改为 core_v0.12.1 arguments.py L2244–2275 的 --data-path 权重前缀对/长度推断（SHA-256 f2a56f59…，登记于 src.nvidia.megatron-examples-core-v0.12.1 补充核对）。
- C05：补混合单位（权重作用于子数据集构建规模，非运行期重采样）与"样本比例≠监督 token 比例"；补本页三类操作的数据游标/RNG 决策。
- C03：补 adapter 最低配套身份清单（基座/tokenizer/模板/adapter 配置与权重/数据集修订）与 optimizer param groups 成员级映射核对。
- C04/R02：装载等价检查限定为"同一目标权重的两种表示/装载"（合并/重载/重分片）；有意换模型函数的切换用独立基线；常见误解去掉"都表现为质量异常而非显式报错"的绝对化。
- C07：补 core_v0.19.2 多模态 NVLM SFT 官方脚本（sft_qwen20_72b_internvit_6b.sh，SHA-256 d96068af…，登记于 src.nvidia.megatron-model-configs-core-v0.19.2 修订轮二补充）；纯文本 LLM SFT 专项缺口如实保留。
- C08：AMD 分层补具体值（兼容页 2025-12-10 更新、覆盖 PyTorch 2.9+ROCm 7.1.1/2.8+ROCm 7.1/2.7-2.8+ROCm 7.0 分节、Docker 镜像兼容；HIP 2.6 分布式后端范围与 TF32；2.6+ROCm 具体配套值 unknown）。
- R03：source_refs 补 src.pytorch.hip-notes-2.6。

## 修订轮三补充（2026-10-19）

- C05：blend 语义落实到 core_v0.12.1 blended builder 构建规则（权重×size 双层作用、无权重分支封顶不额外采样）与 GPT 数据集预构建索引/多 epoch 文档重复（gpt_dataset.py L112–113/L233 起/L366–378）。
- C08：HIP 条件值入正文（torch.distributed 后端限 nccl/gloo、ROCm 无 TF32、torch.version.hip 判别；绑定 2.6 文档不外推）；未核查范围逐项列出。
- S2-01：NVLM SFT 的 FINETUNE_DIR（输出/恢复目录）与 CHECKPOINT_DIR（预训练转换来源，--pretrained-checkpoint）区分；加载分支（--load 目录无 checkpoint 才用 pretrained_checkpoint 并置 finetune=True）与三类操作矩阵对接。

## 修订轮四补充（2026-10-19，复核第三轮发现处理）

- S3-01：epoch 条件量纲改为「所需 token 总量（样本数×序列长＋额外 token）超过单 epoch token 总量」，定位到 _get_num_epochs/_build_document_index。
