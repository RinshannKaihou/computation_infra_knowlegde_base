# Batch 25 T06-05 定向复核报告（第三轮，gpt-6.1-sol / xhigh）

- 日期：2026-10-20（Asia/Shanghai）。
- 对象：[第三轮修订正文](../../knowledge/06-training/mixed-precision-and-convergence.md)、[来源记录](batch-25-t06-05-sources.md)、[registry](../../sources/registry.yaml)，对照[初审](batch-25-t06-05-codex-review.md)与[第二轮复核](batch-25-t06-05-codex-recheck.md)。验收范围采用[任务表 T06-05](../../plans/full-coverage-backlog.yaml)的条款 1–5。
- 执行方式：本地 Codex CLI 当前会话定向复核，未另启审阅代理。核对 `/private/tmp/b25/recheck2-t06-05-run.log` 启动头及同名任务输入：Codex v0.157.1，记录模型 `gpt-6.1-sol`、推理档位 `xhigh`；本轮据该启动记录填写，不追改前轮模型记录。未执行上游测试、GPU/NPU 训练或优化器行为实验。
- 对象快照：正文 SHA-256 `ba2b56fcbe36052f28ac0b7e9270a77002394a7d69b08795f2d2e76c71b94f68`；来源记录 `e098d93b895bd26d719b37edb40e0822ba1062a6e199d61d771d476f12164b11`；registry `99b81d2047b01fc2ed7885143d062e6e0d7b44a0415db22dd63d1d9dd474857b`。正文及登记行号指此快照。
- 写入边界：只新增本报告；不代改正文、来源记录、registry、导航、任务状态或工作仓库的生成文件。既有其他批次改动不归属于本轮。

## 结论摘要

**C01 CLOSED、C07 CLOSED、R01 OPEN（P2，核心误判已修正，尚余跳步率统计契约）。** 先前关闭的 C02、C03、C04、C05、C06、C08、C09 未见回归；原 C01–C09 现均 CLOSED，第二轮新增的 R01 尚未完全满足其关闭条件。本轮未形成新的独立发现，不分配 `B25-T05-R2-xx`，也不把 R01 的剩余条件换号重复计数。

**整体仍需修订，第三轮定向复核暂不通过。** 唯一剩余门槛是明确按 optimizer 计算跳步率时的分母及未确认事件处理；不要求重写已正确的状态机、重复性设计或补做硬件实验。

## C01：CLOSED——状态机与三组静态序列一致

核对位置：正文 L61、registry L6428、来源第三轮补充 L61。已重新取得 E1 的原文件 L127–153，而非仅复述 docstring：

| 分支 | 固定实现与本次正文的核对结果 |
| --- | --- |
| 初始化 | `_growth_tracker=0`，`_hysteresis_tracker=hysteresis`。 |
| `found_inf=True` | growth 清零，hysteresis 减一；减到 ≤0 才把 scale 乘 backoff，并以 `min_scale` 截断；该分支没有把 hysteresis 复位。 |
| `found_inf=False`，尚未完成窗口 | growth 加一，hysteresis 保留原值；一个或几个 finite 步不能单独恢复迟滞预算。 |
| 完成增长窗口 | growth 恰好达到 `growth_interval` 时，growth 归零、hysteresis 恢复初值，scale 乘 growth factor；这是此 `update()` 内正常增长并复位的分支，不否认外部重新初始化或恢复状态。 |

以下逐步账本为**源码静态推演，非运行结果**。每组独立初始化为 scale=16、hysteresis=2、growth_interval=3、growth_factor=2、backoff_factor=0.5、min_scale=1；真/假指 `found_inf`。每格为更新后的 `(growth_tracker, hysteresis_tracker, scale)`。

| `found_inf` 序列 | 逐步状态 | 正文判定 |
| --- | --- | --- |
| 真、假、真 | `(0,1,16)` → `(1,1,16)` → `(0,0,8)` | 一致：中间 finite 步不复位 hysteresis。 |
| 真、真、真 | `(0,1,16)` → `(0,0,8)` → `(0,-1,4)` | 一致：退避后不复位，后续非有限步继续退避。 |
| 真、真、假、假、假、真 | `(0,1,16)` → `(0,0,8)` → `(1,0,8)` → `(2,0,8)` → `(0,2,16)` → `(0,1,16)` | 一致：第三个连续 finite 步完成增长与复位，随后一次非有限步不立即退避。 |

三组覆盖此前缺失的有限增长复位分支。登记同时保留 docstring 的“连续非有限次数”说法与实现不符的提醒；本轮以实现为准。没有把 `min_scale`、scale 平台期或以上静态序列当作是否执行优化器更新的充分证据。

## C07：CLOSED——比较窗口与重复判读契约补齐

核对位置：正文 L73、L80–84、L94、L100–103，来源第三轮补充 L62；并结合既有[精度差异指南](../../knowledge/06-training/gpu-npu-precision-difference-triage.md) L44–54 的输入、状态与更新边界冻结清单。

- 每配置从同一冻结范围独立重复 R 次；不再用平台内 N 次基线代替各精度配置自身的重复。窗口边界的 scaler 新建/恢复范围固定，scale 初值等实验变量另列，不把“恢复原 scaler”与“改变初值”混为一个操作。
- 在固定窗口预算下，预先选择 effective-batch 尝试数、样本/token 数或成功更新数作为对齐轴，并声明换算，不在观测结果后切换截取口径。E5 的 effective-batch/累积约束与这一方向一致；没有声称三种轴的结果天然等价。
- 预注册跳步时 scheduler、数据游标是否推进，记录实际推进量、消费样本/token 及尝试/抑制/进入更新分支计数；推进差异作为策略后果报告，不以相同初始 checkpoint 掩盖窗口内进度差异。
- R 次汇总量、不确定性表示、通过/失败/unknown 规则与验证集样本量在实验前确定；所有配置均须进入固定验证集质量检查。没有虚构通用 R、统计方法或硬件验证结果。

以上解决第二轮 C07 列出的比较口径和重复判读缺口。**窗口的对齐轴已确定，不等于窗口内“跳步率”的分母也已定义**；后一项是第二轮 R01 明确要求的剩余统计条件，见下节，不重复重开 C07。

## R01：OPEN——事件定义已修正，跳步率仍需可复算

核对位置：正文 L59、L70、L84、L92、L101–102，registry L6403，来源第三轮补充 L63。

### 已完成且无需返工的修订

正文已禁止按参数数值是否变化判定 AMP 跳步；按 optimizer 分列尝试、因非有限值被抑制、确认进入未抑制更新分支，参数/master 参数/优化器状态增量独立记录；零增量允许合法零更新、舍入、异常停滞等解释，也明确 `scaler.step()` 返回 `None` 不能单独判跳步。registry 和第三轮来源补充与此一致。

重新阅读 E2 后，三类路径的静态核对如下。示例限定普通、非融合、单张量 SGD 路径，参数初值 1、学习率 0.5、momentum=0、weight_decay=0、无 closure；finite 梯度指 unscale 后的梯度。不把此例外推为全部优化器、融合内核或平台的行为保证。

| 路径 | 尝试 / 非有限抑制 / 未抑制分支 | 参数效果与判读 |
| --- | --- | --- |
| 有限全零梯度 | `1 / 0 / 1` | 更新表达式执行，参数保持 1，不创建 momentum state；合法零更新，不是 AMP 跳步。 |
| 有限非零梯度 1 | `1 / 0 / 1` | 更新表达式把参数从 1 改为 0.5；参数差分是效果证据，更新决策由分支证据支持。 |
| 本轮检查发现非有限梯度 | `1 / 1 / 0` | 普通 GradScaler 路径不调用底层 SGD step，参数保持原值；与第一行不能仅靠参数差分或 `None` 返回值区分。 |

### 尚未满足的原关闭条件

第二轮 R01 已要求“预注册跳步率的窗口、分母及未知事件处理”。当前 L101 补齐了窗口、三个计数和 **R 次结果**的判读规则，但 L92 仍直接用“实际跳步率”触发停止，没有明确：

1. 每个 optimizer 的该比率以何种尝试为分母，是否是有效 batch 边界的 step 尝试，而非 micro-step、已确认成功更新数或只保留可分类事件的子集；多 optimizer 不能直接沿用一个未说明的全局分母。
2. 当尝试数不等于“确认非有限抑制数＋确认未抑制分支数”时，剩余事件怎样记账、能否形成比率、如何进入停止/unknown 判定；分母为零时也须有规则。

正文 L102 已有“证据缺失只能报 unknown”的总括兜底，本轮**不指控正文允许把未知事件当作成功**。剩余问题是总括兜底尚未落实为这个停止指标的分母及事件账本，不能据此唯一复算跳步率。

例如，同一 optimizer 同一窗口有 10 次尝试，确认 1 次非有限抑制、8 次未抑制分支、1 次未确认：`1/10` 是确认抑制占全部尝试的下界；剔除未确认项则为 `1/9`；若未确认项也属于非有限抑制，真实比例可到 `2/10`。仅报告一个数会隐去证据边界。若预注册停止阈值为 15%，现有计数不能支持一个确定的通过/停止结论。以上为**说明统计歧义的构造例，不是本地实验或通用阈值推荐**。

**最小关闭条件**：在正文的停止条件/完成判据要求中明确每个 optimizer、每个预注册窗口的跳步率分子与分母及粒度；例如选择“确认非有限抑制数 / 有效 batch 的 step 尝试数”。对零分母和未确认事件规定记账与判读规则，不静默丢弃或填作成功/跳步；可预注册保守 unknown，或有依据的上下界及其与阈值的关系。同步第三轮来源补充对 R01 完成范围的说明，再定向核对三类已确认路径和包含未确认事件的账本即可。无须指定统一停止阈值或运行 GPU/NPU 测试。

## 已关闭项的回归检查

| 发现 | 本轮状态 | 当前正文与证据核对 |
| --- | --- | --- |
| C02 | **CLOSED，未回归** | L59、registry L6403 保留 step 的更新决策、融合/自定义契约及 update 只调 scale 的职责分离；E2 的普通、融合、update 分支支持。R01 剩余项是比率记账，不是调用职责再次错误。 |
| C03 | **CLOSED，未回归** | L59/L70、registry L6417 仍限定内部状态、unscale 后/update 前、CUDA/FSDP2/≥4 GPU/skipIfRocm；E4 断言设计及 E2 update 清理支持。不作公开跨平台 API、无采集开销或测试已运行承诺。 |
| C04 | **CLOSED，未回归** | L61/L83/L92 未恢复“触及 min_scale 必然空转”推断；E1 下界截断与 E3 的 found_inf 更新决策分立。停止条件中比率的剩余契约继续归 R01。 |
| C05 | **CLOSED，未回归** | L63 的两个 reduced-precision-reduction 开关仍限 PyTorch 2.7/2.8＋ROCm 7.0/7.1，其他组合 unknown，与 PyTorch 2.6 样板分立。E6 固定 HTML 支持；本轮远端请求 429，不声称重取成功。 |
| C06 | **CLOSED，未回归** | L81/L86 保留报告者自述、上游修复/测试设计、本库未复现三层；BF16 硬件、cuDNN≥9.13、skipIfRocm 与 E7 测试一致。没有从 dtype 错配推出必然整训失效，release/ROCm 修复及质量曲线仍未知。 |
| C08 | **CLOSED，未回归** | L74/L93/L100 仍分列任务退化上限与噪声/统计分辨能力；不确定性不足只补采或 unknown，不提高质量阈值，不要求跨平台 bitwise。 |
| C09 | **CLOSED，未回归** | 精度差异指南 L16/L106、dtype/layout 基础页 L76、06 章索引 L26/L50/L68/L77 的回链仍在，02 底层语义与 06 训练判据的主归属未混淆。 |

来源记录保留的早期“公开状态”“连续 N 次”“仅取证到 docstring”“按参数/状态变化判断”文字分别见 L30、L32、L43、L52。本轮按 L49–63 的分轮更正及当前正文/registry 判读，不再把早期表述当现行技术结论；这沿用第二轮的历史记录处理，不另拆成新发现。后续整理宜在旧行就地注明已被哪一轮更正，避免只读旧表时误用。

## 上游重读与证据边界

GitHub 源码网页直接读取失败的条目，已用 GitHub 连接器取得下列精确版本正文，并与本地原文件坐标核对；不是仅凭搜索摘要判断。下列 E 编号仅为报告定位，不新增 registry 条目或改变来源范围。

- **E1 — Megatron 状态机**：重新取得 [core_v0.19.2 grad_scaler.py L127–153](https://github.com/NVIDIA/Megatron-LM/blob/core_v0.19.2/megatron/core/optimizer/grad_scaler.py#L127-L153)，同时读 L61–126 的参数与 docstring。远端文件 blob `036564889825ef6a5b3f27fc0e39386730f17e36`；本地原件 SHA-256 `81402e800476fce96b70d91ff2b799d889ac6ed9407fe74be7cd73d32449c2a7` 与登记一致。三序列为逐分支静态推演。
- **E2 — PyTorch v2.6.0 决策与零增量反例**：重新取得固定 commit `1eba9b3aa3c43f86f4a2c807ac8e12c4a7767340` 的 [GradScaler L343–460](https://github.com/pytorch/pytorch/blob/1eba9b3aa3c43f86f4a2c807ac8e12c4a7767340/torch/amp/grad_scaler.py#L343-L460)、[update/get_scale L463–540](https://github.com/pytorch/pytorch/blob/1eba9b3aa3c43f86f4a2c807ac8e12c4a7767340/torch/amp/grad_scaler.py#L463-L540)、[SGD 参数收集与 step L82–148](https://github.com/pytorch/pytorch/blob/1eba9b3aa3c43f86f4a2c807ac8e12c4a7767340/torch/optim/sgd.py#L82-L148)和[单张量更新 L316–353](https://github.com/pytorch/pytorch/blob/1eba9b3aa3c43f86f4a2c807ac8e12c4a7767340/torch/optim/sgd.py#L316-L353)。SGD 文件 blob `75cd3279070b4ce259874f311527b65f1ceb6590`；GradScaler 本地原件 SHA-256 `eb4bc91fda9815ba40206e2dbb68f9845b85622fee3a92611f227b5845b20780` 与登记一致。未执行这些实现。
- **E3 — Megatron 更新抑制**：重新取得 [optimizer.py L750–825](https://github.com/NVIDIA/Megatron-LM/blob/core_v0.19.2/megatron/core/optimizer/optimizer.py#L750-L825)，核对 scaler.update 与 found_inf_flag 返回/早退的区别。本地原件 SHA-256 `24609822f7c165c9be9f6e95945c873bf474cdce3ca06600b00b52c5d23b31e4` 与登记一致。
- **E4 — FSDP2 测试边界**：重新取得[同 commit 测试 L19–112](https://github.com/pytorch/pytorch/blob/1eba9b3aa3c43f86f4a2c807ac8e12c4a7767340/test/distributed/_composable/fsdp/test_fully_shard_grad_scaler.py#L19-L112)，核对装饰器、CUDA 设备与私有状态断言时点；本地原件 SHA-256 `f5e034a50e4c5e57a54442f9c6fa2afe362d96e4d726415a2e106e44286e660f` 与登记一致。只确认测试设计，未运行套件。
- **E5 — effective batch 与多 optimizer**：重新阅读 [PyTorch 2.6 梯度累积节](https://docs.pytorch.org/docs/2.6/notes/amp_examples.html#gradient-accumulation)及[多 optimizer 节](https://docs.pytorch.org/docs/2.6/notes/amp_examples.html#working-with-multiple-models-losses-and-optimizers)。前者约束有效 batch 上的检查、跳步与 scale 更新；后者明确各 optimizer 独立作跳步决策。两者均不替本任务提供 R、统计通过标准或停止阈值。
- **E6 — ROCm 精确已知问题节**：[docs-7.1.1 指定节](https://rocm.docs.amd.com/en/docs-7.1.1/compatibility/ml-compatibility/pytorch-compatibility.html#known-issues-and-notes-for-pytorch-2-7-2-8-with-rocm-7-0-and-rocm-7-1)本轮远端返回 429；重读第二轮已用的 `/private/tmp/b24-t062-review-8tp_ut74/amd-pytorch-compatibility.html` 原 HTML L932–939，SHA-256 `79c10c8262d804ff735c65198a12e72875b768869d8f180c2bb69c94bb85d85c` 相同。只据该固定原件检查限定语未回归，不冒称重新核验远端最新版本。
- **E7 — 案例修复与测试**：重新打开 [issue #200537](https://github.com/pytorch/pytorch/issues/200537)和[PR #200697](https://github.com/pytorch/pytorch/pull/200697)，连接器重取固定修复 commit 的 [AutocastRNN.cpp L39–104](https://github.com/pytorch/pytorch/blob/cbffccce1e61987e927081fc97cc358b3a7624c3/aten/src/ATen/cudnn/AutocastRNN.cpp#L39-L104)及[test_cuda.py L13942–14006](https://github.com/pytorch/pytorch/blob/cbffccce1e61987e927081fc97cc358b3a7624c3/test/test_cuda.py#L13942-L14006)。本轮不重判前轮记录的标准 merge API 字段，也不从网页关闭事件或源码存在推出测试/质量通过。

TorchNPU 两个固定文件的成功重取结论沿用第二轮，本轮不冒称再次全文重核；目标 CANN/框架配套、算子内部累加、fallback/图/融合矩阵、NPU 收敛窗口及案例所属 release/ROCm 修复继续留 gate。以上不与本轮已解决的源码状态机混为同一种未知。

## 最终整体判定与验收条款 1–5

| 条款 | 本轮判断 | 依据与剩余范围 |
| --- | --- | --- |
| 1. FP32/FP16/BF16、累加、master weights、autocast、动态 scale/overflow/跳步及条件 | **在已核机制范围内满足** | 底层语义沿用 02，master 权重限定指定实现；C01 状态机与三序列闭合，更新决策不再靠参数差分。跳步率的量化与停止使用仍受 R01 限制。 |
| 2. NVIDIA/AMD 与 Ascend 分别引用，冲突组合 unknown | **在明示来源范围内满足** | 实现档案分立、ROCm 原节版本限定及未知矩阵未回归；不宣称三平台配套或真实环境验证通过。 |
| 3. 同输入/模型/优化器/数据进度，先重复再单因素，分项观察 | **部分满足** | C07 的对齐轴、进度账本、每配置 R 次及恢复范围已闭合；分项观测已纠正，但每 optimizer 跳步率分母及未确认事件的统计契约仍缺（R01）。 |
| 4. 首差异/传播、窗口/质量、预注册容差/重复/停止，不要求 bitwise | **部分满足** | 全配置质量必经、汇总/不确定性预注册与任务阈值独立均已建立；采用“实际跳步率”作停止触发时仍不能唯一复算（R01）。 |
| 5. 可追溯适配/质量案例及修复或未证实结果，材料不足留 gate | **在算子适配案例范围内满足** | 修复源码与回归设计可追溯，事实分层和环境门槛未回归；未以 SFT 报告、issue 关闭或 dtype 断言替代整训质量因果链，材料不足继续留 gate。 |

**因此本轮不声明 T06-05 通过既定审阅范围。** 待 R01 的上述最小剩余条件修订并定向复核关闭，才可作该范围内的审阅通过声明；即使通过，也不升级正文 `draft / source_checked` 为硬件验证、完整兼容矩阵或整训收敛证明。

## 结构检查与文件范围

- `make check`：通过，107 content entries / 525 sources。
- `make build`：在 `/private/tmp/b25-t06-05-recheck2.ebcADp/repository/` 隔离副本通过，同为 107 content entries / 525 sources；保留既有 build 链接目标，未改写工作仓库 `build/`。两项只检查结构、本地链接与构建流程，不证明技术结论、远端内容或运行行为。
- 写报告前后的 SHA-256 清单对照：快照中的 528 个既有文件均未变化或删除，三个复核对象哈希保持不变；同期另有 T06-04/T06-06 的新报告出现，未将其计作本轮写入。E1、E2、E4 的本地原件 Git blob 也分别与连接器返回的文件 blob 一致。
- 本轮只新增 `docs/research/batch-25-t06-05-codex-recheck-2.md`；正文、来源记录及 registry 不代改。未修改 `src/kb/`，不新增测试，不执行 `make test`、上游单测或训练实验。
