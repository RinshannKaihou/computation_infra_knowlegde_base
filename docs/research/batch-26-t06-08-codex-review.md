# Batch 26 · T06-08 v1 边界修订独立审阅

## 审阅头部

- 审阅角色：与正文作者独立的批次审阅者；本轮只审阅，不代作者修订正文。
- 实际审阅模型 / 推理档位：`gpt-6.1-sol / xhigh`。已读取本次 Codex CLI 会话的 `turn_context` 元数据，确认 `model=gpt-6.1-sol`、`effort=xhigh`；本轮未委派其他模型，报告无回退标记。
- 日期：2026-10-20（Asia/Shanghai）。
- 审阅基准：[内容编写指南](../authoring-guide.md)第 5、7 节、[T06-08 验收五条](../../plans/full-coverage-backlog.yaml)（L6182 起），以及本轮工作区相对 `HEAD` 的修订差异。
- 审阅对象：
  1. [Checkpoint 恢复一致性](../../knowledge/06-training/checkpoint-state-consistency.md)：本轮新增保存/加载职责、重分片表、TTP 约束、EP/CP/工作流引用与元数据。
  2. [弹性训练与成员变更](../../knowledge/06-training/elastic-training-and-membership.md)：本轮空中加油行、外部约束、机制表、来源与元数据。
  3. [训练领域索引](../../knowledge/06-training/index.md)：仅两处条目描述。
  4. [来源登记表](../../sources/registry.yaml)：指定三条新增来源及两条既有来源 notes 的并入。
  5. [作者来源记录](batch-26-t06-08-sources.md)：哈希、主张定位、unknown 与整包哈希说明。
- 既有内容只核对保留情况及与新证据的相容性，不重新裁定历史审阅结论。工作区原有其他批次改动不属于本轮审阅或修改范围。

### 取证方式与覆盖限制

1. 经 GitHub 连接器重新读取固定 ref 的上游文件和所需行段，而非只读作者摘要。Megatron `core_v0.12.1` 本次解析到 commit `a845aa7e12b3a117e24c2352b9e3e60bad2e3a17`；MindSpeed-LLM 使用 commit `53f3639c3da9c000a187c44cc0c08d55026ddded`。
2. 为取得原文件行坐标，对已有临时源码副本计算 Git blob SHA-1，并与本次远程返回的 blob SHA 比较；一致后才用原始 UTF-8 文件的 `nl -ba` 行号抽查及 SHA-256 复算。没有使用网页转换后的行号拼接 GitHub 锚点。复核范围包括 Megatron `generate_state_dict` L649–700、`_load_base_checkpoint` L878–935；另为核查数据计数这一具体主张读取 L1355–1372，不据此宣称完整加载流程已经核验。
3. 重新打开 [PyTorch 历史版本页](https://pytorch.org/get-started/previous-versions/#v260)的 v2.6.0 节及 [DCP 2.6 页面](https://docs.pytorch.org/docs/2.6/distributed.checkpoint.html)，核对发行矩阵与重分片/API 边界。
4. **指定的 [MindX DL 6.0.0 HTML 约束页](https://www.hiascend.com/document/detail/zh/mindx-dl/600/clusterscheduling/ref/mindiottp/mindiotft005.html)本次未能成功重新取回**：网页读取返回 404/内部取回错误；本地网络无法解析远程域名，也未取得浏览器读取授权。这只是本轮工具可达性结果，不断言原网页已被官方删除。作者未保留该页字节快照，不能把其“已渲染取回”记录直接当作本轮独立核验。
5. 补充读取同产品路径下的官方 [MindCluster 6.0.0《故障恢复加速》PDF](https://www.hiascend.com/doc_center/source/zh/mindx-dl/600/clusterscheduling/ref/mindiottp/%E6%95%85%E9%9A%9C%E6%81%A2%E5%A4%8D%E5%8A%A0%E9%80%9F.pdf)，封面文档版本 01、发布日期 2024-12-30；对 §2.1.2 的印刷页 4–5 / 文件第 10–11 页截图核对。**该 PDF 是补充证据，不被冒充为作者 2026-10-20 所见 HTML 的同一快照**；两者可能有修订差异，见 C04。
6. 未安装 whl，未运行 PyTorch/Megatron/MindSpeed、保存/恢复、弹性伸缩、故障注入或精度实验；结构检查不作为技术或硬件验证。

### 文件级来源指纹抽查

下列文件的本地 Git blob 均与本次远程元数据一致，SHA-256 前 16 位也均与作者记录相符；README 与 training.py 的远程 blob 另作复核。作者记录中的哈希没有因 C05 的整包归因问题而失效。

| 固定源码文件 | 本轮复算 SHA-256 前 16 位 | 核对内容 |
|---|---|---|
| Megatron `megatron/training/checkpointing.py` | `713fc0fcb172b710` | 保存组装、加载入口、args 内数据计数 |
| Megatron `megatron/core/dist_checkpointing/serialization.py` | `b535efb72229fbf3` | 文件身份；不声称完整重分片契约已核 |
| MindSpeed-LLM `docs/pytorch/features/high_availability.md` | `83b6b6d8e3590f0e` | 开关、外链、HA/弹性约束 |
| MindSpeed-LLM `docs/pytorch/install_guide.md` | `8dd60a6cc0983ffc` | Megatron tag、MindSpeed 分支钉扎 |
| MindSpeed-LLM `mindspeed_llm/training/checkpointing.py` | `beaa6057ac72f74f` | import、wrapper、finalize 职责 |
| MindSpeed-LLM `initialize_patch.py` | `5051c2494f1022c7` | L26、L48 的 adaptor 调用面 |
| MindSpeed-LLM `high_availability.py` | `a9be983cd7e61a00` | `validate_args` 条件与冲突断言 |
| MindSpeed-LLM `pretrain_gpt.py` | `b3ca649a9f11868d` | L200 的 taskd 导入及 ImportError 回退 |
| MindSpeed-LLM `README.md` | `7b4893c93e8884d1` | 依赖表中的 PyTorch 2.7.1 |
| MindSpeed-LLM `mindspeed_llm/training/training.py` | `341c0792484b7113` | 作者用于跨轮对照的文件身份 |

## 发现列表

### T06-08-C01 · P2 · TTP 内存公式的变量和计量范围被误释

- **受影响位置**：`knowledge/06-training/elastic-training-and-membership.md:76`；同一公式见 `knowledge/06-training/checkpoint-state-consistency.md:148`、`sources/registry.yaml:6652`、`docs/research/batch-26-t06-08-sources.md:36`。
- **发现**：弹性正文把 N 解释为卡数、B 解释为单卡优化器字节数量级；这不是该公式的含义。其余位置仅写 N(B)×12×副本数，未给正确量纲，因而不能纠正这一误读。
- **证据**：上述官方 6.0.0 PDF §2.1.2，印刷页 5 / 文件第 11 页：计算对象是需要增加的片上内存**总量，单位 GB**；N 是模型参数量，B 表示十亿参数的单位。它不是单卡显存或卡数的函数。此处依据实际打开并截图核对的 PDF，不声称已重新读到 HTML 同句。
- **影响**：读者会用错误变量估算副本开销，且混淆总量与单卡量，影响启用 HA 前的容量判断。
- **关闭条件**：同步订正两篇正文、registry notes 与来源记录的变量定义和总量单位；不把总量公式直接当成每卡需求，也不补造目标环境的扩容结论。修订后定向核对来源及相邻版本声明。

### T06-08-C02 · P2 · “无 tracker 即随机初始化”遗漏前置分支

- **受影响位置**：`knowledge/06-training/checkpoint-state-consistency.md:103`；`sources/registry.yaml:6666`；`docs/research/batch-26-t06-08-sources.md:39`。
- **发现**：新增段把缺失 tracker 直接等同于随机初始化/按开关退出。实际流程允许显式 `ckpt_step` 提供 iteration，也允许先命中非持久 checkpoint；缺 tracker 本身并不必然进入随机初始化分支。
- **证据**：固定 Megatron [L900–935](https://github.com/NVIDIA/Megatron-LM/blob/a845aa7e12b3a117e24c2352b9e3e60bad2e3a17/megatron/training/checkpointing.py#L900-L935)：L906–907 先接受有效的显式 `ckpt_step`；L909–918 可直接返回非持久 checkpoint；到 L924 仍为 `iteration == -1` 才走告警、可选退出和返回空状态。非持久 iteration 比较的是这一阶段的有效 iteration，并非总是 tracker 中的持久 iteration。
- **影响**：这一简化会把仍可恢复的启动路径误判为从随机起点训练，并误述 `--exit-on-missing-checkpoint` 的触发范围。
- **关闭条件**：把描述改为有序分支，明确未命中可用非持久 checkpoint、也无 tracker/有效显式 iteration 等条件后才进入缺 checkpoint 分支；同步更新 registry 和来源记录。保留恢复后核对 iteration/身份的原则，但不要以错误分支条件支撑它。

### T06-08-C03 · P2 · “数据进度不在组装范围”忽略了序列化的 args

- **受影响位置**：`knowledge/06-training/checkpoint-state-consistency.md:102`。
- **发现**：新增小节笼统说数据进度与业务计数不在 `generate_state_dict` 的组装范围。该函数虽未逐项生成独立的数据游标键，却会把完整 args 对象放入状态；不能据此断言数据进度没有被携带。
- **证据**：固定 Megatron [L657–662](https://github.com/NVIDIA/Megatron-LM/blob/a845aa7e12b3a117e24c2352b9e3e60bad2e3a17/megatron/training/checkpointing.py#L657-L662)保存 args；同文件 [L1357–1370](https://github.com/NVIDIA/Megatron-LM/blob/a845aa7e12b3a117e24c2352b9e3e60bad2e3a17/megatron/training/checkpointing.py#L1357-L1370)在相应非 finetune 分支从 checkpoint args 取出 consumed/skipped train samples 和 consumed valid samples，并据消费样本数更新 microbatch 配置。另有累计 FLOP 计数确实由外层 wrapper 添加，两种情况不应混为“都不在范围内”。
- **影响**：状态覆盖矩阵本身仍完整，但新增实现解释会让读者漏查 args 内的逻辑计数，错误理解数据进度到底在哪里保存和恢复。
- **关闭条件**：区分“函数保存 args 中已有计数”“调用方维护/补充计数”与“未自动覆盖任意 sampler/loader 游标、预取和 exactly-once 语义”。保留后两项未知，不把部分计数存在扩大成精确数据恢复保证；同时说明 optimizer/scheduler、RNG 的组装分别受 `no_save_optim`、`no_save_rng` 条件控制。

### T06-08-C04 · P2 · TTP DP/MoE 限制的转述与可重开的证据存在未消解差异

- **受影响位置**：`knowledge/06-training/elastic-training-and-membership.md:75`；`knowledge/06-training/checkpoint-state-consistency.md:148`；`sources/registry.yaml:6652`；`docs/research/batch-26-t06-08-sources.md:36`。
- **发现与证据**：指定 HTML 未能重新取回且作者无快照；可打开的官方 6.0.0 PDF §2.1.2（印刷页 4–5 / 文件第 10–11 页）至少提出以下需要解释的差异：
  - PDF 的偶数 DP 限定出现在 ZeRO-1 的总体条件中，正文却把偶数仅挂到“副本数=2”。不能在未说明修订差异的情况下把它当作等价转述。
  - PDF 的多副本整除表述按中文语法是“副本数被 DP Size 整除”，正文改成 DP size 被副本数整除；原文可能存在笔误或表达歧义，但这需要显式记载、查证，不能无声修正。checkpoint 正文“其他副本数须被副本数整除”还丢失了应核对的 DP 主体。
  - PDF 区分开启 MoE **前/后**，正文和 notes 改成“新版本后”，把配置状态写成版本演进；MindSpeed-LLM 的固定 HA 文档也要求 MoE 场景 dense/sparse DP 均大于 1，没有支持这一“新版本”界线。
  - 作者来源记录及弹性正文使用“以算代存”，PDF 使用的是减少优化器切分范围的“以算代传”机制描述，应核对后避免术语替换。
- **核对边界**：PDF 支持健康卡数严格大于 `world_size/2`、副本完整性与分片迭代一致性要求，未见正文把 `>` 错写为 `>=`。但它不能替代本轮对指定 HTML 中 Atlas 9000、ARF、级联故障及不走 ACP 等新增细节的逐条独立核对。本项**不以旧 PDF 宣判现有 HTML 必然错误**，而是要求消解已观察到的证据差异与尚未复取的部分。
- **关闭条件**：重新取得指定 HTML 的可定位原文，或明确登记采用的同版本替代来源及其修订范围；逐项补齐 DP/副本数量、整除方向、MoE 前后与机制用语。若官方整除语句仍歧义，保留来源原意并标 unknown，不自行给出支持组合。没有证据覆盖的硬限制须降格为待确认；完成后对两正文、registry 和作者记录同源复核。

### T06-08-C05 · P3 · 两个整包哈希不同被错误归因为 gzip 元数据不稳定

- **受影响位置**：`docs/research/batch-26-t06-08-sources.md:7`、`:13`、`:22`。
- **发现**：记录把 Batch 25 与本轮 MindSpeed-LLM 整包不同归因于跨次下载的 gzip 元数据不稳定。本轮检查已有的这两个压缩包，原因至少不是该证据所说的同一 ref gzip 元数据变化。
- **证据**：两个包 SHA-256 分别为 `693f619a8b608726c23dc53a7e0d283684883149fb140951f169a297fe72936e` 与 `c6db8136f3163c595d614fd2aa26aa4f4a13f3719a9706db4609636b2b8d3bd1`；gzip 的前 10 字节都为 `1f8b0800000000000003`，解压后的 tar 哈希却仍不同。归档顶层目录分别是 `MindSpeed-LLM-2.2.0/` 与 `MindSpeed-LLM-53f3639c3da9c000a187c44cc0c08d55026ddded/`，全局 PAX comment 都指向同一 commit。去除顶层目录后，1903 个成员的路径集合、内容哈希和所比较的成员元数据完全一致。
- **影响**：文件级哈希可作为内容锚这一做法正确，但当前文字把不同 ref 命名的归档差异写成下载不确定性，削弱来源可追溯性；Megatron 行也不应直接继承未经证明的 gzip 归因。
- **关闭条件**：记录这是 tag 名称与 commit 名称归档前缀不同造成的可观察包装差异，保留两个包的实际哈希、相同 commit 和文件级一致性；没有同一 URL/ref 的重复下载证据时，不宣称其整包哈希不稳定或已证明 gzip 元数据是原因。

## 逐维度核对结果

| 维度 | 结果 |
|---|---|
| Megatron 保存/加载职责 | 见 C02、C03。三种格式的分派与 `use_dist_ckpt` 形参废弃说明有源码支持；未将形参废弃泛化为所有同名运行开关废弃。 |
| MindSpeed import、安装钉扎与 HA 入口 | **已核对，未见问题**。install guide 钉 Megatron tag 与 MindSpeed 分支；checkpoint import、L210/L236、finalize 责任及 adaptor 调用面相符。后训练缺包退出有 HA/训练分支前提，不据此宣称所有入口缺包均退出。 |
| 版本线不互推 | **已核对，未见问题**。PyTorch 2.6 与 MindSpeed-LLM 的 2.7.1 依赖不混用；MindX DL 6.0.0 与 MindCluster 71RC1 只记录外链/组件来源，配套矩阵保持未知。机制对照表中的 TTP 行应连同前面的版本声明阅读，不能视为已安装组合。 |
| 重分片支持/不支持/未知 | **已核对，未见问题**，就本轮取证边界而言，保守保留 Megatron 跨并行重分片、torch_dcp 互读、外部 whl 和 mid-step 为未知是适当的；未知不是上游不支持的证明。MindSpeed EP/CP 拒绝条件仅用于 elastic 分支，未扩张到一切 HA 配置。TTP 条件仍受 C04 限制。 |
| TTP 数值与外部限制 | 见 C01、C04。严格多数阈值和一致性门有补充官方证据；其他未成功复取的 HTML 细节不标为本轮“已核对无问题”。 |
| frontmatter、ID、related_ids 与验证状态 | **已核对，未见问题**。两篇稳定 ID、draft、generic 导航语义与 source_checked/未实测说明保持；EP/CP、预训练/微调与 RL 引用目标存在。 |
| registry 新增三项与 notes 并入 | 技术转述需随 C01、C02、C04 同步修订；除此之外**已核对，未见问题**。三条新 ID 存在且未重复增设 wrapper/HA-code 来源；两处 notes 并入对象正确。Megatron 文件身份与根许可声明已核对，网站许可保持 unknown，未套用仓库许可。 |
| 两处索引描述 | **已核对，未见问题**。链接与内容范围相符，明确 draft、未实测，未提前宣称审阅通过。 |
| 作者来源记录与指纹 | 文件哈希与原始源码行号抽查**已核对，未见问题**；归档解释见 C05。来源准备记录中的 NEW 拟登记名需结合末尾集成结果阅读，最终 registry 已选择并入既有来源，本轮不要求重复登记。 |
| 既有内容保持与新旧一致性 | 除 C03 的新增实现解释外**已核对，未见问题**。完整 step、状态责任矩阵、API/对象加载/正确续训分层、同输入单步与持续窗口、重放/遗漏、容差方法均保留；未重审历史结论。 |

## 验收五条逐项对照

| acceptance | 本轮结论 |
|---|---|
| 1. 完整 step 与模型/optimizer/scheduler/scaler/RNG/数据进度/并行身份矩阵；EP/CP、工作流引用 | 矩阵和引用**已核对，未见问题**；新增 Megatron 数据进度解释须按 C03 订正。 |
| 2. DCP/torchrun、MindSpeed HA/MindIO 保存/加载/成员变更职责；组合不拼接，mid-step 未知 | 不拼接和 mid-step 边界保持；加载分支与 TTP 约束存在 C01、C02、C04，暂不满足完整验收。 |
| 3. 新旧 world size/并行映射支持表及精确来源 | 表存在，保守 unknown 不构成问题；TTP 精确原文与条件仍待 C04 闭环，不能只因已登记来源而判通过。 |
| 4. 身份/结构、逻辑进度、状态值、同输入单步、持续窗口、重放/遗漏；成功加载与正确续训分开 | **已核对，未见问题**；既有恢复后验证表及成功加载不等于正确续训的要求保留。 |
| 5. CPU 优先 DCP 实验及精度方法保持 not_verified，不要求硬件实验通过 | **已核对，未见问题**。[DCP 实验设计](../../knowledge/06-training/checkpoint-state-recovery-experiment.md)与[GPU/NPU 精度实验设计](../../knowledge/06-training/gpu-npu-precision-difference-experiment.md)仍为 not_verified、无实验结果。本轮未改其状态，也未把 2.8/补丁实验设计冒充成 2.6 已验证运行结果。 |

## 结构检查与写入边界

- `make check`：通过，108 content entries / 534 sources；只核对结构、本地链接，不证明技术正确性或远程 URL 可达性。
- `make build`：在隔离临时镜像通过，同为 108 content entries / 534 sources。首次镜像遗漏现有 build 导航，导致既有 `first-fill-status.md` 链接检查失败；补拷现有 build 后重新执行通过，未修改仓库内容来绕过检查。
- 本轮唯一写入为本报告。未修改两篇正文、索引、registry、作者来源记录、计划或既有实验；隔离构建不回写当前仓库的 build 目录。验证前后对原仓库文件做哈希对照，验证命令未改变其内容。工作区其他并行任务的文件不归入本轮交付。

## 整体结论

**需修订，T06-08 本轮不通过。** 共 5 项开放发现：4 项 P2（C01–C04）、1 项 P3（C05），未发现 P1。版本线不互推、完整状态矩阵和既有验证方法总体保留，但公式量纲、加载分支、args 内数据计数以及 TTP 条件的证据歧义尚未关闭；指定 HTML 的独立重开也未完成。作者修订后须针对上述发现复核，不能以构建成功或已生成本报告替代通过结论；无需为关闭文档问题虚构或提前要求硬件实验成功。
