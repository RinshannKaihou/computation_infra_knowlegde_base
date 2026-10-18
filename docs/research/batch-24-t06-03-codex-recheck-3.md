# Batch 24 · T06-03 Codex 定向复核第三轮报告

- 复核日期：2026-10-19（Asia/Shanghai）。
- 结论：**通过本轮定向复核**。第二轮仍 OPEN 的 **B24-T063-C05、B24-T063-C08、B24-T063-S2-01 全部 CLOSED**，没有新 OPEN P1/P2。
- 新发现：**B24-B24-T063-S3-01，P3 / OPEN**，关于多 epoch 条件的量纲表述；不阻断用户指定的本轮通过标准。
- 历史问题合计：C01–C09、R01–R03、S2-01 共 **13 项 CLOSED**；其中原已 CLOSED 的 10 项仅做关联回归抽查，不冒称重新完成全面审阅。计入本轮新编号后，仍 OPEN **1 项 P3，0 项 P1/P2**。
- 执行边界：只新增本报告，不修改正文、作者取证、registry、导航、计划或其他报告。不代表整个 Batch 24 通过，也不改变正文的 `draft / source_checked` 状态。
- 模型审计：当前 Codex CLI 会话执行，未派发子代理或另行运行模型 CLI。会话没有提供可独立核验的实际后端模型、推理档位及路由元数据，记为 `unknown`，不冒称已核验为仓库约定的指定模型。本报告的技术判定不构成模型路由合规证明。

## 1. 范围、输入和方法

以[第二轮复核报告](batch-24-t06-03-codex-recheck-2.md)中三个 OPEN 项及各自剩余关闭条件为范围，重读[修订正文](../../knowledge/06-training/pretraining-and-finetuning.md)对应的 L77、L143、L145，并核对[作者取证“修订轮三补充”](batch-24-t06-03-sources.md) L141–145。通读正文的相关上下文，必要时查看初审关闭条件及正文已经链接的[Checkpoint 恢复一致性](../../knowledge/06-training/checkpoint-state-consistency.md)，不另起全面审阅或扩大模型/平台交付范围。

遵循 README、编写指南、内容归属和 metadata schema；按[任务表 T06-03](../../plans/full-coverage-backlog.yaml) L5930–5972 重新核对五条验收要求及三条来源准备要求。正文行号及源码链接行号均以本轮实际原文件为准，不使用网页工具删除空行后的坐标。

| 输入 | 本轮 SHA-256 |
|---|---|
| 修订正文 | `2828c8592a7774c0c26dd8c7a4ff00a48ff4d3b474d765410f4b98db0f072e68` |
| 作者取证 | `f9187f7150eafa7da10d086611d9b37c8d9be72b7a808155dffd934870e0d0e8` |
| 第二轮报告 | `3a1fbcc0af17e576a4c24ed16db41a52db637c705ad767bce6dee20682c22fc8` |
| 来源登记 | `3ea07202e7e0573c8ff8089bc5fcdd142b5a51269dc1f646a9d4a08d065215a2` |
| 完整覆盖任务表 | `53bfc8fe47d56ab322e546c853858cbaa90cf5a5d0305b33a80bab0f39275d54` |

### 1.1 只读取证及限制

本轮重新取回 12 个精确上游文件/版本化页面，按下表的相关片段核对；不执行取回的源码，不下载训练数据，不执行安装、预训练、SFT、合并、转换或任何主动 GPU/NPU 操作。官方测试不在本轮重新执行的范围内。

首次 Python HTTP 读取因本机证书链校验失败，随后改用保留 TLS 校验的 `curl --fail --location`，12 个地址均取得 HTTP 200 的可读预期内容，没有关闭证书校验。临时文件保存在仓库外；它们不是长期证据附件。AMD 页面与第二轮完整哈希相同；HIP 页整页字节哈希不同，本轮按实际章节内容判断，不从可变网页的整页哈希变化推断功能语义改变。

| 证据 | 本轮重开位置与核对范围 |
|---|---|
| E01：混合构建和读取 | core_v0.12.1 [blended builder L107–126](https://github.com/NVIDIA/Megatron-LM/blob/core_v0.12.1/megatron/core/datasets/blended_megatron_dataset_builder.py#L107-L126)，另核 L201–246、L551–578；[BlendedDataset L88–103](https://github.com/NVIDIA/Megatron-LM/blob/core_v0.12.1/megatron/core/datasets/blended_dataset.py#L88-L103)，另核 L140–157；[helpers.cpp L102–126](https://github.com/NVIDIA/Megatron-LM/blob/core_v0.12.1/megatron/core/datasets/helpers.cpp#L102-L126)。 |
| E02：GPT 索引和重复 | 同 tag [gpt_dataset.py L112–113](https://github.com/NVIDIA/Megatron-LM/blob/core_v0.12.1/megatron/core/datasets/gpt_dataset.py#L112-L113)，另核 `__getitem__` / 查询路径 L160 起、L233 起，epoch 计算 L365–380、L533–553，以及文档索引构建 L410–413、L556–582。 |
| E03：NVLM 的两个目录和转换前提 | core_v0.19.2 [SFT 脚本 L23–38](https://github.com/NVIDIA/Megatron-LM/blob/core_v0.19.2/examples/multimodal/nvlm/sft_qwen20_72b_internvit_6b.sh#L23-L38)，另核 L65–143；[NVLM README L70–84](https://github.com/NVIDIA/Megatron-LM/blob/core_v0.19.2/examples/multimodal/nvlm/README.md#L70-L84)。 |
| E04：核心装载分支与状态 | 同 tag [checkpointing.py L2092–2104](https://github.com/NVIDIA/Megatron-LM/blob/core_v0.19.2/megatron/training/checkpointing.py#L2092-L2104)，另核 L2472–2502、L2555–2616、L2627 起；[training.py L2190–2225](https://github.com/NVIDIA/Megatron-LM/blob/core_v0.19.2/megatron/training/training.py#L2190-L2225)；[arguments.py L2878–2881](https://github.com/NVIDIA/Megatron-LM/blob/core_v0.19.2/megatron/training/arguments.py#L2878-L2881)中的不载入状态开关。 |
| E05：数据状态不是消费计数的同义词 | 同 tag [dataloader_provider.py L123–141](https://github.com/NVIDIA/Megatron-LM/blob/core_v0.19.2/examples/multimodal/dataloader_provider.py#L123-L141)，另核 L152–165。 |
| E06：AMD 与 HIP 的独立版本线 | [AMD docs-7.1.1 PyTorch compatibility](https://rocm.docs.amd.com/en/docs-7.1.1/compatibility/ml-compatibility/pytorch-compatibility.html)的日期、Linux 范围和各版本特性节；[PyTorch 2.6 HIP](https://docs.pytorch.org/docs/2.6/notes/hip.html)的 Checking for HIP、TensorFloat-32(TF32) on ROCm、torch.distributed backends。 |

E 编号仅用于本报告，不是新增 registry ID。同一仓库/tag 的补充定位归入既有来源档案，没有借审阅任务新增来源或改写历史登记。

## 2. 第二轮 OPEN 项逐项判定

### B24-T063-C05 — CLOSED（原 P2）

**对应修订：**正文 L77；作者取证 L143。L73–75 的 blend / split / pack 区分，以及 L118、L120 的计量口径继续保留。

第二轮剩余缺口是没有说明预构建源/样本索引的消费方式，以及加权配额与底层语料重复之间的关系，而不是要求发明推荐混合比例。本轮已补足这一机制链：

1. 在多源混合范围，显式权重与目标 size 同时参与子数据集请求规模和顶层混合分布；无显式权重分支按源长度组织并限制顶层长度。E01 的构建规则、配额计算和源/源内样本索引能支持这些描述。这里不把多源分支的封顶规则外推为单一 prefix 的通用无重复保证。
2. L77 已明确 GPT 的 document/sample/shuffle 索引在构建期生成，并由读取路径消费；请求规模需要多个 epoch 时，底层文档索引会重复并重排。E02 可连通 epoch 计算、文档索引构建和样本查询，不能再把它理解为“没有运行期 token 动态重采样，所以原始语料不会重复”。
3. 重复量归入按源消费统计；样本占比不代替有效监督 token 占比；L120 仍要求用数据修订、游标和去重键核对重复/遗漏。推理、同阶段 resume、新阶段训练的数据游标/RNG 策略也保持明确。

因此原先的**机制交付缺失**关闭。新加入的“请求样本数超过单 epoch 的文档量”尚有量纲歧义，另列本轮 P3：S3-01；不把这处措辞问题等同于第二轮整段采样/重复语义仍然缺失。推荐比例未知、未执行数据恢复验证等限制继续成立。

### B24-T063-C08 — CLOSED（原 P2）

**对应修订：**正文 L145；作者取证 L144。

E06 独立重开确认，正文现在给出了上一轮缺失的实际条件值，而不只是列章节名：

- PyTorch 2.6 的 HIP 页列出的分布式后端为 `nccl` 和 `gloo`，该版本页写明 ROCm 不支持 TF32，并用 `torch.version.hip` 辅助区分 HIP 构建。正文没有把 CUDA 接口复用名称误写成 NVIDIA 硬件依赖。
- 限制明确绑定 **PyTorch 2.6 版本化文档**，不扩成所有 ROCm 版本的永久结论。AMD docs-7.1.1 页的 2025-12-10 日期、Linux 范围，以及 PyTorch 2.9 / ROCm 7.1.1、2.8 / 7.1、2.7–2.8 / 7.0 分节仍与本轮页面对应；未把它们与 HIP 2.6 拼成一套支持组合。
- 具体 GPU、OS 发行版和驱动组合、外部内核/扩展、PyTorch 2.6 的具体镜像/驱动配套、固定 HF 组合的 ROCm 可执行性均已逐层列为未核查。本库未执行 AMD 验证，与官方声明分开。

剩余关闭条件满足。上述 unknown 不是“不兼容”结论，也不要求为关闭来源审阅问题制作 AMD 可运行样板。

### B24-T063-S2-01 — CLOSED（原 P2）

**对应修订：**正文 L143，结合 L77、L95–104、L131、L134–137；作者取证 L145。

本轮正文已不再把 `--load ${FINETUNE_DIR}` 无条件概括为首次 SFT 的预训练起点。与 E03/E04 对照：

| 场景 | 当前正文与固定实现的对应关系 |
|---|---|
| 首次 SFT，目标输出目录没有 checkpoint | `FINETUNE_DIR` 是本阶段输出/后续恢复目录；预训练权重来自 `CHECKPOINT_DIR`，由 `--pretrained-checkpoint` 引用。目标目录没有 checkpoint 才选择该来源并设置 finetune。README 的 72B 路径要求先从预训练 PP=1 转为 SFT PP=4、TP=8；正文现已说明必须按目标 PP 转换，未把任意已有权重目录当作可用起点。 |
| 新阶段的状态责任 | 核心装载逻辑在 finetune 路径将 iteration 置零，并跳过旧阶段 optimizer/scheduler 和 RNG 的常规恢复；消费计数也不按普通 resume 分支继承。这与正文新阶段重置、归档前阶段消费统计的契约相符。重置不等于声称两个阶段的随机数状态完全相同。 |
| 已有本阶段 checkpoint 的 resume | 不再回退到预训练来源，按目标目录恢复。对于所选脚本预期的普通训练 checkpoint，在未另行禁用装载等条件下，E04 分别支持 iteration/消费计数、optimizer/scheduler 和 RNG 的恢复；正文 L131 仍要求核对实际启动参数及 state_dict，而不是只检查参数名。 |

**数据与停止边界也需按全文读取，而不能从“目录存在”推断恢复完成。** E05 显示 loader 状态另按 iteration/rank 查找和恢复；缺失或装载失败可只打印信息后继续，不由消费计数自动保证样本流恢复。本轮没有把该脚本写成“自动失败即停”的实现保证：正文 L77 与矩阵仍要求同阶段恢复数据进度，L104 指向的 Checkpoint 契约 L94–100 要求核对完整状态及截取点、在继续写入前完成验证；L136 另规定装载等价检查超差即停。依照该明确转引的验收契约，loader 未恢复不能被认定为完整 resume。无需为此要求作者运行脚本或证明 loader 实测可靠。

因此，首次阶段来源、恢复目录、转换前提、继承/重置责任及其验证约束已可以闭合。这里关闭的是原来的**分支解释错误**，不是认证输出目录中的工件已经完整，也不是保证所有 Megatron 脚本遵循相同分支；纯文本 SFT 专项仍是已披露的有限 unknown。

## 3. 已 CLOSED 项的关联回归抽查

仅检查本轮三处修订可能触及的结论，不将历史已关闭项全面重开。

| 历史项 | 本轮抽查位置与结果 | 判定 |
|---|---|---|
| C01、C02 | L45、L62–63、L84、L118、L121、L149：目标轴/参数轴、HF 移位计损与 loss_mask、实际可训练集合和基座驻留边界仍在；混合节没有重新使用原始 labels 通用计数。 | 维持 CLOSED |
| C03、C04、R02 | L95–110、L131、L136–137、L152：adapter 身份、active/可训练范围、成员级 param group 映射、完整 resume、同目标装载等价与跨目标质量基线的区分未被新 NVLM 段撤销。 | 维持 CLOSED |
| C06、C07 | L143、作者取证 L125/L137、既有两个 Megatron 来源档案：0.19.2 模型级示例存在，0.12.1 最小循环保留合成标识，NVLM 保留多模态范围。未重下完整源码包，未重新逐目录核验模型清单。 | 维持 CLOSED |
| C09 | L144、L156：Ascend 固定依赖近邻链接、按模型的 HF 版本覆盖、在研与 Pass/Test 限定仍保留；本轮不重复调研未变化的 Ascend 文件。 | 维持 CLOSED |
| R01、R03 | L73 仍使用有依据的 data-path 入口，没有恢复无依据的 data-weight；L21 仍登记 HIP 来源依赖，L145 的两个版本线分开。 | 维持 CLOSED |

## 4. 本轮新发现

### B24-B24-T063-S3-01 — 多 epoch 条件的“样本数 / 文档量”量纲不清

- **优先级 / 状态：P3 / OPEN。** 按用户指定保留 `B24-B24-` 编号前缀。
- **位置：**正文 L77 的“当请求样本数超过单 epoch 的文档量时”，以及紧随的 gpt_dataset.py L366–378 定位；作者取证 L143 采用同一说明方向。
- **依据：**E02 的 `_get_num_epochs` L533–553 实际比较的是**所需 token 数与每 epoch token 数**。所需量由 `num_samples × sequence_length + add_extra_token_to_sequence` 决定，不能直接把样本个数与文档篇数比较；L525–531 从所选文档长度求每 epoch token 总量。L366–378 使用这个 epoch 结果，真正复制/打乱文档索引在 L556–582。
- **影响与定级：**“文档量”可能被理解为篇数，从而误解增加 epoch 的阈值。正文已经正确交付多 epoch 重复机制，并要求按源消费/去重统计，不依靠该模糊阈值推定实际重复量；没有给出据此执行的容量公式或命令。因此定为 P3 的精确性问题，而非再次判定原 C05 的机制缺失，也不新增 P2 阻断。
- **关闭条件：**将条件明确为“按目标样本数、序列长度及额外 token 换算的所需 token 总量超过单 epoch 可提供的 token 总量时”；补到同 tag `_get_num_epochs` 与 `_build_document_index` 的精确位置。不必展开所有末 epoch 优化或增加实验。

除此之外，本轮定向范围没有发现新 OPEN P1/P2。正文缺少的运行结果、推荐比例、纯文本专项及未核实兼容组合，继续按既有 unknown 边界管理，不把它们重新包装成已经取得的证据。

## 5. 任务验收重新核对

“满足”指本任务要求的来源整理和概念交付范围，不表示平台实验通过。

| T06-03 验收条目 | 本轮结论与依据 |
|---|---|
| 1. 四类工作流、监督目标、token/mask/label、样本混合及阶段切换 | **满足，附 S3-01/P3 精确性尾项。** L45–77 区分目标/参数轴及三种数据组织机制；本轮补齐混合索引与原始语料重复链，阶段切换策略没有被替换成比例推荐或 split。 |
| 2. 数据/模型/tokenizer/adapter 身份、可训练范围与 optimizer 责任；合并/恢复边界 | **满足。** L81–114 保留身份、成员映射、adapter-only 与完整训练状态的区别；L143 修正首次 SFT 和同阶段恢复的来源选择。合并反向恢复能力未知仍不冒称支持。 |
| 3. 有效 token 吞吐、质量曲线、重复/遗漏、显存和 I/O 口径 | **满足，附上述 P3。** L118–121 保留真实计损、计时、跨 rank、独立质量基线和去重口径；底层重复机制已有说明，不以 epoch 数代替实际消费计量。 |
| 4. mask/label、污染、adapter 加载和状态异常的区分检查及阶段验证 | **满足。** L125–139 的检查继续区分线索与根因、装载等价与新目标评价；NVLM 来源选择与继承/重置契约现可对应。验证方法明确未执行。 |
| 5. NVIDIA/Ascend 固定配置；AMD 经官方条件核查的边界 | **满足于选定示例范围。** NVIDIA 两个独立版本档案、NVLM 多模态 SFT 和 Ascend 锁定配置不拼配；AMD 补出了 2.6 后端/TF32 条件及硬件、OS、扩展等未核查层次，不声称任意模型兼容。 |

来源准备三项：HF 固定版本文档/源码/测试沿用第二轮已核结果，仅做上述关联回归；Megatron/MindSpeed 所选模型入口在既定官方示例范围成立，本轮补核 NVLM 状态分支，不扩大为纯文本 SFT 全面调研；LoRA 论文仍只用于方法及其实验环境边界，本轮未重开论文全文、未新增或外推其性能数字。

## 6. 元数据、结构检查和变更边界

正文稳定 ID、标题、06 章主归属、13 个 source_refs 和 4 个 related_ids 保持有效；`status: draft`、`platforms: [generic]`、`verification.status: source_checked` 没有被升级为平台兼容或硬件复现证明。`updated_at: "2026-10-18"` 早于本轮日期，不把这个日期视为现场验证记录，也不代作者修改。没有调整许可或第三方再分发边界。

本轮实际校验：

1. 原工作树执行 `PYTHONDONTWRITEBYTECODE=1 make check`：**PASS，103 content entries / 493 sources**；报告写入后复跑通过。
2. 为同时遵守“只新增一个文件”和构建要求，将仓库复制到仓库外临时目录，保留既有 build，排除 `.git/`、`.venv/`、`.agents/`、`.codex/` 和 Python 缓存，用原仓库 Python 的绝对路径执行 `PYTHONDONTWRITEBYTECODE=1 make -C <临时副本> PYTHON=<原仓库 .venv/bin/python 绝对路径> build`：**PASS，103 content entries / 493 sources**；写入报告后同步报告并再次构建通过。未改写原工作树 build，也不声称这是没有既有 build 的纯净 bootstrap 测试。
3. `git diff --check` 通过；对比开始时 497 个既有文件的 SHA-256 清单（已跟踪、未忽略未跟踪文件及既有 build 文件），既有文件没有变化，新增集合仅为本报告。开始时已有的所有修改和未跟踪内容保持原样。
4. 没有修改 `src/kb/`，未新增内容测试、未运行无关测试。结构检查与构建不验证远程语义、模型输出、性能或硬件能力。

## 7. 结论

**通过。** 第二轮 3 项 OPEN 已全部 CLOSED；本轮没有新 OPEN P1/P2，满足用户指定的通过条件。历史 13 项均已关闭，本轮仅余 **B24-B24-T063-S3-01 / P3 / OPEN**，建议下一次文字修订时明确 token 预算的量纲并补精确源码定位，再定向核对该句即可。

该结论仅限 T06-03 本轮技术来源审阅，不提升正文编辑/验证状态，不代表其他 Batch 24 任务或任何 GPU/NPU 环境已经验收。

## 附录：关键上游取回对象校验

| 对象 | 本轮 SHA-256 |
|---|---|
| core_v0.12.1 blended builder | `f41e2eb71bf0cb5c9a972a2294642c65edf542ea0d2abf3a6dae75f69b5c5c69` |
| core_v0.12.1 gpt_dataset.py | `3c7fecd01608f8af5fa23589905ed80b6a602bfd303645c389c17e2599ed50f3` |
| core_v0.19.2 NVLM SFT 脚本 | `d96068afbe20ff53dc1ecf4a4321d203e18bc10b98c221bd945bfdc63a1e354b` |
| core_v0.19.2 checkpointing.py | `b4b4fcc725d543dd382a838dc72679c9de4dca8502ee274d8864c46ab55bba49` |
| core_v0.19.2 dataloader_provider.py | `57d5bdcee2377347bd9bae8b4b44965f923fcc7451d82026b809bdfa6dea2240` |
| AMD docs-7.1.1 兼容页 | `79c10c8262d804ff735c65198a12e72875b768869d8f180c2bb69c94bb85d85c` |
| PyTorch 2.6 HIP 页 | `c544cb55f21a9578a4239114ef5b905286e1b1a763c1f2280a9ef2a2ead522f8` |

校验值只标识本轮读取的对象，不是运行成功、兼容性或恢复正确性的证明。
