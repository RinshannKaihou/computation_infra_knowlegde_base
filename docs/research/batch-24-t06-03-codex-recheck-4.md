# Batch 24 · T06-03 Codex 定向复核第四轮报告

- 复核日期：2026-10-19（Asia/Shanghai）。
- 结论：**通过**。第三轮唯一仍 OPEN 的 **B24-B24-T063-S3-01（P3）已 CLOSED**；本轮没有新发现，新增 OPEN P1/P2/P3 均为 0。
- 范围：只复核上述遗留项，并重新核对 T06-03 的验收条目与当前正文的对应关系。第三轮已经 CLOSED 的 C01–C09、R01–R03、S2-01 共 13 项**不重查、不重新判定**，沿用历史记录。
- 变更边界：只新增本报告；不修改正文、作者取证、来源登记、导航、任务表、历史报告或原工作树构建产物。
- 模型审计：由当前 Codex CLI 会话直接审阅，未派发子代理、未另行调用模型 CLI。会话未提供可独立核验的实际后端模型、推理档位和路由元数据，记为 `unknown`；不冒称已核验为仓库约定的指定模型。本报告不构成模型路由合规证明。

## 1. 输入与方法

遵循 README、内容编写指南及内容归属约定，以[第三轮报告](batch-24-t06-03-codex-recheck-3.md)第 4 节的唯一 OPEN 项及其关闭条件为复核清单。用户提示中的第三轮路径为 `docs/research/batch-24/t06-03-codex-recheck-3.md`，仓库实际文件为上述扁平路径，本轮读取后者，没有创建替代报告或目录。

本轮重读：

1. [修订正文](../../knowledge/06-training/pretraining-and-finetuning.md) L67–77，重点为 L77 的 token 预算、多 epoch 与文档索引说明。
2. [作者取证](batch-24-t06-03-sources.md)末尾“修订轮四补充”（L147–149）。该记录说明拟修正的内容，不单独作为上游技术结论的证明。
3. [任务表 T06-03](../../plans/full-coverage-backlog.yaml) L5930–5972，以及正文中对应的工作流、状态、观察、验证和平台范围。验收核对只检查当前交付内容及边界是否对应任务，不借此重开已经关闭的问题或重做其上游审阅。

| 输入 | 本轮 SHA-256 |
|---|---|
| 修订正文 | `1249cd4d00384a1bbcaac33c14b040a052ae7277a6b0ae3e29c59c2690e9e90e` |
| 作者取证 | `3e43a84bc070918c4b5ab5087afb23e0f95f0dadb5be5b879cfd109ac2c43a76` |
| 第三轮报告 | `b097607e17ecf013d4f4dfd8a647ef0cefffaf6f4b84c1412cc2f2a748900df9` |
| 完整覆盖任务表 | `53bfc8fe47d56ab322e546c853858cbaa90cf5a5d0305b33a80bab0f39275d54` |

### 1.1 精确上游证据

本轮仅重新取回一个上游文件：NVIDIA/Megatron-LM 的 **core_v0.12.1** `megatron/core/datasets/gpt_dataset.py`。网页读取未取得正文，随后使用保留 TLS 校验的 `curl --fail --location` 读取同 tag 原文件，得到 HTTP 200；未执行下载的源码。原始文件 SHA-256 为：

`3c7fecd01608f8af5fa23589905ed80b6a602bfd303645c389c17e2599ed50f3`

该值与第三轮报告记录一致；它只标识本轮读取对象，不证明运行效果。行号以下载原文件为准，不使用网页转换后的行号。

| 证据 | 精确位置 | 本轮核对内容 |
|---|---|---|
| E01-a | [配置定义 L46–49](https://github.com/NVIDIA/Megatron-LM/blob/core_v0.12.1/megatron/core/datasets/gpt_dataset.py#L46-L49)、[读取路径 L175–182](https://github.com/NVIDIA/Megatron-LM/blob/core_v0.12.1/megatron/core/datasets/gpt_dataset.py#L175-L182) | `add_extra_token_to_sequence` 是布尔配置，默认开启；额外读取的 token 用于形成相应长度的输入和移位标签。 |
| E01-b | [每 epoch token 总量与 epoch 判定 L525–553](https://github.com/NVIDIA/Megatron-LM/blob/core_v0.12.1/megatron/core/datasets/gpt_dataset.py#L525-L553) | 前者为所选文档长度之和；请求量按样本数、序列长和额外 token 配置计算，循环增加 epoch 直到 token 预算足够。 |
| E01-c | [调用链 L365–367](https://github.com/NVIDIA/Megatron-LM/blob/core_v0.12.1/megatron/core/datasets/gpt_dataset.py#L365-L367)、[文档索引构建调用 L410–413](https://github.com/NVIDIA/Megatron-LM/blob/core_v0.12.1/megatron/core/datasets/gpt_dataset.py#L410-L413)、[索引函数 L556–586](https://github.com/NVIDIA/Megatron-LM/blob/core_v0.12.1/megatron/core/datasets/gpt_dataset.py#L556-L586) | epoch 结果用于文档索引构建；索引包含跨 epoch 的文档重复与重排，末 epoch 单独处理时通过递归构建后拼接。 |

其他上游页面、LoRA 论文、HF 测试及 NVIDIA/Ascend/AMD 配套不在本轮重新取证范围。没有运行安装、数据构建、预训练、微调、合并、转换或 GPU/NPU 实验。

## 2. 遗留项逐项判定

### B24-B24-T063-S3-01 — CLOSED（原 P3）

**对应位置：**正文 L77；作者取证 L149。保留第三轮的完整历史编号，不把它改写为新问题编号。

**原问题与关闭条件：**第三轮指出“请求样本数超过单 epoch 的文档量”混用了样本个数与文档篇数，要求明确为按目标样本数、序列长度及额外 token 换算的 token 总量比较，并定位到同 tag 的 `_get_num_epochs` 与 `_build_document_index`。

**本轮依据：**

1. **比较量纲已修正。**正文改为“所需 token 总量”超过“单 epoch 可提供的 token 总量”，不再比较样本数和文档篇数。E01-b 的 L531 从所选文档长度求 token 总量，L547–552 按所需 token 数决定是否增加 epoch，能够支持这项修订。
2. **预算表达与源码对应。**源码请求量为 `self.num_samples * self.config.sequence_length + self.config.add_extra_token_to_sequence`。正文括号将额外 token 写在“样本数×序列长度”的乘积之后相加，与该表达对应。这里的额外配置值在总请求量中只加一次，**不是**把每条读取长度相加成“样本数×（序列长度＋额外 token）”；单条序列读取的额外 token 含义与全局 epoch 预算不可混同。`num_samples is None` 时源码直接返回一个 epoch；正文该句讨论的是给定目标样本数后的预算，不将其外推到未指定目标的分支。
3. **函数定位与机制链已补齐。**正文仍链接 core_v0.12.1 的原文件，并明确点名 `_get_num_epochs` 和 `_build_document_index`，能够唯一定位判定函数和索引函数，不再仅指向调用处。E01-c 进一步确认判定结果传入索引构建，随后重复、打乱文档索引；本报告给出原文件精确行号作为核对依据。无需要求作者另行展开所有末 epoch 优化。
4. **重复消费的计量边界仍明确。**L77 将重复量归入按源消费统计，并区分样本比例与有效监督 token 比例；L120 要求按数据修订、游标和去重键核对重复/遗漏，而不是从 epoch 数直接推算。这里仅检查遗留句的解释是否落回原有计量契约，不重新审查已关闭的混合构建发现。

**判定：CLOSED。**量纲修正和两个函数的定位均满足第三轮关闭条件。关闭的是该句的来源与精确性问题，不是确认数据管道已经运行、实际重复量已经测得，或所有 GPT/混合数据实现均遵循此 tag 的逻辑。

## 3. 本轮新发现

**无。**本轮定向范围没有需要以 `B24-T063-S4-xx` 编号的新问题；新增 OPEN P1、P2、P3 均为 0。未核实的推荐混合比例、运行结果和平台组合继续按正文既有 unknown 边界保留，不将历史已经接受的有限范围重新登记为发现。

## 4. 任务验收重新核对

下表的“满足”仅针对 T06-03 已选定的概念与来源整理交付范围。对已 CLOSED 项沿用第三轮结论，不宣称重新核验其实现、平台条件或测试结果。

| T06-03 验收条目 | 当前交付位置与本轮结论 |
|---|---|
| 1. 覆盖预训练、继续预训练、全参 SFT、LoRA/PEFT 的区别，说明监督目标、token/mask/label、样本混合和阶段切换 | **满足。**L45–77 区分训练目标轴与参数适配轴、四种选样及三种数据组织机制；L95–114 展示状态切换契约。本轮关闭 L77 的 token 预算精确性尾项。 |
| 2. 列出数据/模型/tokenizer/adapter 身份、可训练参数及 optimizer state 责任，精确说明合并和恢复边界 | **满足，沿用前轮来源判定。**L81–110 给出身份与责任表、三类装载/续训矩阵、最低身份清单和合并边界；区分 adapter-only 工件与完整训练恢复。未重新核查相关 HF 源码和测试。 |
| 3. 解释有效 token 吞吐、质量曲线、重复/遗漏、显存与 I/O 的观察口径 | **满足。**L118–121 分列实际计损 token、计时与跨 rank 口径、独立目标曲线、按源消费及去重、显存和 I/O。修订后的多 epoch 判定与实际消费计量分开，不以理论预算冒充实际重复量。 |
| 4. 给出 mask/label、数据污染、adapter 加载、状态继承异常的区分检查和阶段转换验证 | **满足，沿用前轮来源判定。**L125–139 覆盖相应检查，区分装载等价与换目标后的独立质量评价，并将污染重叠统计标为线索；验证方法明确未执行。 |
| 5. NVIDIA/Ascend 分别引用锁定配置；AMD 保留官方条件核查后的执行边界，不声明任意模型兼容 | **满足于既定示例范围，沿用前轮判定。**L143–145 保留 NVIDIA 两个独立版本档案与多模态 NVLM 范围、Ascend 锁定配置及 AMD 分版本边界；纯文本 SFT 专项、具体硬件/OS/驱动/扩展和固定 HF 组合在 ROCm 上的可执行性等仍列 unknown。本轮不重开平台来源。 |

三条来源准备要求同时按交付对应关系核对：

- **固定 HF LoRA/SFT/adapter 文档、源码与测试：**L62、L89–110、L136、L156 仍提供固定版本入口及“已读未运行”等限制；技术判定沿用第三轮，不重新打开这些来源。
- **Megatron 与 MindSpeed-LLM 所选模型配置及核心循环说明：**L73–77、L114、L143–144 保留既定配置及版本边界；本轮只增量重开 core_v0.12.1 GPT 数据集的预算/索引代码。NVLM 为多模态示例，不能据此声明纯文本专项或所有配置均已覆盖。
- **原始 LoRA 论文仅解释方法边界：**L54、L151 仍将论文数字限定为论文实验环境，不作为目标平台收益；本轮没有重开论文或新增性能外推。

任务表自身的计划状态不是本轮修改对象；不因报告通过而更新计划、正文编辑状态或实验验证状态。

## 5. 结构检查与文件边界

本轮实际执行并记录：

1. 原工作树执行 `PYTHONDONTWRITEBYTECODE=1 make check`：**PASS，103 content entries / 493 sources**；报告写入后复跑通过。
2. 为满足只新增一个文件的约束，将仓库复制到仓库外临时目录，保留既有 `build/`，排除 `.git/`、`.venv/`、`.agents/`、`.codex/` 和缓存目录，使用原仓库 `.venv/bin/python` 的绝对路径执行 `PYTHONDONTWRITEBYTECODE=1 make -C <临时副本> PYTHON=<原仓库 Python 绝对路径> build`：**PASS，103 content entries / 493 sources**；报告写入后同步报告并再次构建通过。没有改写原工作树 `build/`，也不将此描述为无既有构建产物的纯净 bootstrap 验证。
3. `git diff --check` 通过；新增报告另行检查无尾随空白。对比开始时 **501 个既有文件**的 SHA-256 清单（已跟踪、未忽略未跟踪文件及既有构建文件）：既有文件未变化，新增集合仅为本报告。开始时已有的修改和未跟踪文件保持原样。
4. 没有修改 `src/kb/`，没有新增测试或运行无关测试。上述校验只检查结构、本地引用与构建，不验证远程语义、硬件兼容性、训练质量或吞吐。

正文仍为 `draft / source_checked`，`generic` 仍是概念范围而非跨平台运行证明；本轮不新增许可、再分发或实际执行授权。

## 6. 最终结论

**通过。**本轮纳入复核的唯一历史 OPEN 项 **B24-B24-T063-S3-01 已 CLOSED**，无新 OPEN P1/P2，满足“全部 OPEN 项 CLOSED 且无新 OPEN P1/P2”的验收规则。第三轮已关闭的 13 项不重查；计入本轮关闭的遗留项，历史发现记录不再有 OPEN 项。

结论仅覆盖 T06-03 本次定向技术来源复核，不代表整个 Batch 24 完成，不提升正文或平台的验证等级，也不替代真实 GPU/NPU/AMD 环境验证。
