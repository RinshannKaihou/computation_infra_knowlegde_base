# Batch 25 T06-05 定向复核报告（第二轮，gpt-6.1-sol / xhigh）

- 日期：2026-10-20（Asia/Shanghai）。
- 对象：[修订正文](../../knowledge/06-training/mixed-precision-and-convergence.md)、[初审 C01–C09](batch-25-t06-05-codex-review.md)、[来源记录及修订补充](batch-25-t06-05-sources.md)、[registry](../../sources/registry.yaml)，以及两篇基础页和 06 章导航的回链。
- 执行方式：本地 Codex CLI 当前会话逐项复核，未另启审阅代理，未执行上游测试或 GPU/NPU 训练。已核对 `/private/tmp/b25/recheck-t06-05-run.log` 启动头及其对应任务提示词：Codex v0.157.1，记录模型 `gpt-6.1-sol`、推理档位 `xhigh`；据本轮启动记录填写，不覆盖初审历史模型记录。
- 对象快照：正文 SHA-256 `ecadd890879af741a75e3c4d3a3a0f2f802f8dcba39d00bcf5fada01d1115c04`；来源记录 SHA-256 `abd62bdee7e702c0b06bff957b2429bfd11805296bd00b393dd2d33960a9afbf`。下列正文行号均指本快照。
- 写入边界：仅新增本报告；不代改正文、来源记录、registry、导航、任务状态或其他批次文件。

## 逐项判定表

**结论：原 9 项中 7 项 CLOSED、2 项 OPEN；新增 1 项 P2（B25-T05-R01）。** CLOSED 只表示原发现中指定的问题在明示范围内已解决，不等于平台兼容、测试通过或整训收敛得到验证。

| 初审发现 | 优先级 | 判定 | 修订位置、上游依据与理由 |
| --- | --- | --- | --- |
| B25-T05-C01 | P2 | **OPEN** | 正文 L61、registry L6428 已纠正“连续 N 次才退避”，也指出退避不复位计数及 docstring 与实现不符。但仍漏掉 **finite 分支达到完整 growth_interval 时，growth tracker 清零、hysteresis tracker 恢复初值并增长 scale** 的唯一正常增长复位分支；三种静态序列未补。来源记录 L43 仍称精确行为只读到参数/docstring，L51 的补充也未交代该复位分支。重读 E3 后，尚不能把目前的半个状态机称为完整机制说明。剩余关闭条件见下节。 |
| B25-T05-C02 | P2 | **CLOSED** | 正文 L59 与 registry L6403 已分清普通路径的 step 决策、融合/自定义路径的更新抑制以及 update 的 scale 调整职责；四项默认值未改变。与 E1 的普通、融合和 update 三段一致。“不能只数 Python 调用”的修订方向正确；新加入的“按参数/状态是否变化”不能独立定义成功更新，另列 R01，不把它与已修正的调用职责混为一项。 |
| B25-T05-C03 | P2 | **CLOSED** | 正文 L59、L70 及 registry L6417 已将 found_inf 降为版本绑定的内部插桩，规定 unscale 后、update 前采集，并限定 CUDA/FSDP2、至少 4 GPU、skipIfRocm；没有写成跨平台公开 API 或已通过测试。E1 的状态清理与 E2 的断言时点、装饰器相符。来源记录 L30 的旧“公开”表述按 L49–53 的后续更正解读，不再采信旧结论；若保留旧表，宜就地标明已被补充替代。任何实际观测方案仍须计入同步/采集影响，尤其 E1 L536–540 明示 get_scale 的同步代价，本轮不认定观测无开销。 |
| B25-T05-C04 | P2 | **CLOSED** | 正文 L70、L83、L92、L105 已将 scale、非有限判定与实际更新分列，不再从 min_scale 或 scale 平台期推出必然跳步；停止条件改为预注册持续次数、跳步率或有效更新停滞。E3 的下界截断和 E4 的 found_inf_flag 分支支持此修订。跳步率如何避免把合法零更新计作 AMP 跳步，仍受新增 R01 限制。 |
| B25-T05-C05 | P2 | **CLOSED** | 正文 L63 与来源补充 L54 已把两个 reduced-precision-reduction 开关的限制绑定到 PyTorch 2.7/2.8＋ROCm 7.0/7.1 节，并与 PyTorch 2.6 机制样板分立；其他组合 unknown。重读 E7 的准确节标题及两个字段，与修订一致。正文第二个字段沿用同一前缀作简写，未产生另一字段的歧义；不将“开关不支持”扩为 AMD 不支持 AMP/BF16。该关闭依据是固定版本 HTML 原件，不是本轮远端重取成功。 |
| B25-T05-C06 | P2 | **CLOSED** | 正文 L81、L86 和来源补充 L55 已区分报告者自述、上游修订/测试设计、本库未复现；补 nightly/设备/cuDNN 环境与 BF16 硬件、cuDNN≥9.13、跳过 ROCm 的测试门槛，删除必然影响收敛的外推，步骤 2 改为定位配置/实现/支持条件。E5 的 issue、固定修复源码与回归测试支持这些有限结论；所属 release、ROCm 对应修复及整训质量仍留 gate。PR 的 closed/unmerged 与 mergebot 落地事件并存，不把二者误读为未落地或质量已验证。 |
| B25-T05-C07 | P2 | **OPEN** | 正文 L82、L84、L94、L101–102 已增加每配置 R 次、冻结起点、scaler 恢复范围、尝试步/成功更新双计数，并要求所有配置进入固定验证集质量检查。但“得到分布”尚未落实为 **R 次结果的预注册聚合/不确定性与通过规则**；也未要求记录跳步时 scheduler 和数据游标的推进策略及实际推进量。“计步口径”仍未明确选择 effective-batch 尝试、样本/token 或成功更新中的哪个作为窗口对齐轴。旧指南冻结起点不能替代这些窗口内账本；E6 的 effective-batch 约束仍相关。剩余关闭条件见下节。 |
| B25-T05-C08 | P2 | **CLOSED** | 正文 L74、L93、L100 已将任务允许退化与统计分辨阈分列，噪声盖过任务阈值时只能补采或 unknown，不再要求放宽质量容差，也不要求跨平台 bitwise。与 E6 的浮点边界说明一致；上游不提供本任务的阈值。本轮关闭的是“噪声授权放宽标准”的错误，重复结果如何形成判定仍归 C07，不视为已经补齐统计方案。 |
| B25-T05-C09 | P3 | **CLOSED** | [精度差异指南](../../knowledge/06-training/gpu-npu-precision-difference-triage.md) L16/L106 已有 related ID 和普通 Markdown 回链；[dtype/layout 基础页](../../knowledge/02-software-stack/dtype-layout-and-precision-semantics.md) L76 已指向训练判据页。06 章索引入口仍在，02 的底层语义与 06 的训练判据主归属未混淆，没有复制整篇正文。 |

### OPEN 项的剩余关闭条件

**C01：补全复位语义，不仅删除“连续”二字。** E3 原文件 L127–153 足以静态确定全部分支，无须把可从源码确定的事实继续记为 unknown；真实设备运行仍另列未验证。正文、registry 和来源记录应统一说明：初始 hysteresis tracker 等于 hysteresis；非有限步清零 growth tracker 并递减 hysteresis tracker；未完成增长窗口的 finite 步不复位 hysteresis；只有完整 finite 增长窗口才同时复位两个 tracker 并增长 scale。补入以下三类预期或等价例子，再定向核对：

| 静态序列（每组重新初始化） | 按固定实现推导的预期 |
| --- | --- |
| found_inf = 真、假、真 | 设初始 scale=16、hysteresis=2、growth_interval=3、growth_factor=2、backoff_factor=0.5、min_scale=1；hysteresis tracker 依次 1、1、0，scale 依次 16、16、8；中间 finite 步未复位。 |
| 真、真、真 | 同一组初值；hysteresis tracker 依次 1、0、−1，scale 依次 16、8、4；退避不复位，后续非有限步继续退避。 |
| 真、真、假、假、假、真 | 前两步后 scale=8、hysteresis tracker=0；第三个连续 finite 步完成增长窗口后 scale=16、growth tracker=0、hysteresis tracker=2；紧接的非有限步只将 hysteresis tracker 减到 1，scale 保持 16，而不是立即再退避。 |

以上是源码静态推演，**没有运行 Megatron 或伪装为行为测试结果**。仅前两类例子不能覆盖复位分支；本报告给出预期也不代替作者修订机制正文。

**C07：把“有 R 次重复”补成可执行的判读契约。** 不要求虚构通用 R 数值或套用特定统计方法，但进入实验前必须要求填明：每次窗口的对齐轴与预算、effective batch/micro-step 的换算、尝试/成功/跳步计数、已消费样本/token 与 scheduler 推进量；溢出跳步时数据和 scheduler 各自是否推进；每配置 R 次结果采用何种汇总量/不确定性表示、哪些规则判通过/失败/unknown。可以把 scheduler/数据推进差异定义为精度策略的自然后果，但必须预注册并报告，不能事后悄悄按不同轴截取“同窗口”。继续保留所有配置的固定验证集质量必经路径和 scaler 状态恢复/实验变量分离。

### 上游重读与取证边界

以下 E 编号用于表内定位，沿用已有登记来源；新增反例的同版本优化器源码仅作本报告定向补核，不代改正文来源集。GitHub 源码锚使用原文件坐标，不使用网页工具重排行号。

- **E1 — PyTorch v2.6.0 GradScaler**：重新打开 [固定 commit 的 step 普通分支 L343–365](https://github.com/pytorch/pytorch/blob/1eba9b3aa3c43f86f4a2c807ac8e12c4a7767340/torch/amp/grad_scaler.py#L343-L365)，并重读原文件融合路径 L398–453、update L463–531、get_scale L536–540。网页读取及 GitHub 连接器均取得有关正文；本地原件完整 SHA-256 与 registry 的 `eb4bc91fda9815ba40206e2dbb68f9845b85622fee3a92611f227b5845b20780` 一致。未执行代码。
- **E2 — 同版本 FSDP2 测试**：重新打开 [测试原文件](https://github.com/pytorch/pytorch/blob/v2.6.0/test/distributed/_composable/fsdp/test_fully_shard_grad_scaler.py)，核对 L19–26、L76–107；原件完整哈希与登记的 `f5e034a50e4c5e57a54442f9c6fa2afe362d96e4d726415a2e106e44286e660f` 一致。只确认测试条件、注入方式和断言设计，不宣称套件运行通过。
- **E3 — Megatron core_v0.19.2 状态机**：网页直接读取失败后，GitHub 连接器成功重取 [grad_scaler.py L127–153](https://github.com/NVIDIA/Megatron-LM/blob/core_v0.19.2/megatron/core/optimizer/grad_scaler.py#L127-L153)；另逐行重读本地固定原件，其完整哈希与登记的 `81402e800476fce96b70d91ff2b799d889ac6ed9407fe74be7cd73d32449c2a7` 一致。
- **E4 — Megatron 同 tag 更新决策**：重新打开 [optimizer.py](https://github.com/NVIDIA/Megatron-LM/blob/core_v0.19.2/megatron/core/optimizer/optimizer.py)，并对照本地原文件 L755–774、L815–822，确认 scaler.update 与 found_inf_flag 的跳步决策分开；原件完整哈希与登记的 `24609822f7c165c9be9f6e95945c873bf474cdce3ca06600b00b52c5d23b31e4` 一致。
- **E5 — #200537 修复链**：重新打开 [issue](https://github.com/pytorch/pytorch/issues/200537)、[PR #200697](https://github.com/pytorch/pytorch/pull/200697)、[commit cbffccce](https://github.com/pytorch/pytorch/commit/cbffccce1e61987e927081fc97cc358b3a7624c3)；GitHub 连接器重取 [AutocastRNN.cpp L39–104](https://github.com/pytorch/pytorch/blob/cbffccce1e61987e927081fc97cc358b3a7624c3/aten/src/ATen/cudnn/AutocastRNN.cpp#L39-L104) 与 [test_cuda.py L13942–14006](https://github.com/pytorch/pytorch/blob/cbffccce1e61987e927081fc97cc358b3a7624c3/test/test_cuda.py#L13942-L14006)。PR API 本轮明确返回 closed、merged=false、merged_at=null；网页时间线记载 mergebot 于 2026-10-14（上游日期）在该 commit 关闭 PR。两项证据同时保留，不用标准 merge 字段代替落地源码或测试执行证据。
- **E6 — PyTorch 2.6 方法边界**：重新阅读 [AMP 文档](https://docs.pytorch.org/docs/2.6/amp.html)、[AMP Examples 的梯度累积节](https://docs.pytorch.org/docs/2.6/notes/amp_examples.html#gradient-accumulation)、[Numerical accuracy](https://docs.pytorch.org/docs/2.6/notes/numerical_accuracy.html) 和既有登记的 [torch.optim](https://docs.pytorch.org/docs/2.6/optim.html)。这些来源不提供本任务的 R、质量阈值、停止阈值或统计通过标准。
- **E7 — ROCm docs-7.1.1**：本轮远端精确 URL 仍未成功取回；改为重新阅读 `/private/tmp/b24-t062-review-8tp_ut74/amd-pytorch-compatibility.html` 的 canonical、版本标记与原 HTML L932–939，对应[精确 Known issues 节](https://rocm.docs.amd.com/en/docs-7.1.1/compatibility/ml-compatibility/pytorch-compatibility.html#known-issues-and-notes-for-pytorch-2-7-2-8-with-rocm-7-0-and-rocm-7-1)。该固定原件 SHA-256 为 `79c10c8262d804ff735c65198a12e72875b768869d8f180c2bb69c94bb85d85c`。不声称已核验本轮远端最新内容，也不从该节推广其他版本组合。
- **E8 — TorchNPU 固定 commit**：raw 网页读取失败，但 GitHub 连接器本轮成功重取 [autocast_utils.py](https://github.com/Ascend/pytorch/blob/bc51ab84cc6f35c77aab1c59886e0ea43681a317/torch_npu/npu/autocast_utils.py) 全文和 [AutoCastOps.cpp L20–159](https://github.com/Ascend/pytorch/blob/bc51ab84cc6f35c77aab1c59886e0ea43681a317/torch_npu/csrc/aten/AutoCastOps.cpp#L20-L159)。已补开初审受阻的两处实现：BF16 dtype 列表受设备能力条件控制；普通注册宏四族之外还有 norm 的 fp32_append_dtype 重分派和 binary_cross_entropy 禁用路径。这里只核对接口/归属，不证明逐算子内部累加、CANN 配套或训练收敛；这些未知不因本轮成功取回源码而关闭。

## 新发现

### B25-T05-R01 — P2／OPEN：把参数或状态“数值发生变化”当作成功更新依据，仍会误计跳步

- **受影响位置**：正文 L59 新增的“跳过更新要按实际参数/状态是否变化观测”，并关联 L70、L82–84、L92、L101 的成功更新计数/跳步率；registry L6403 与来源补充 L52 使用了同一口径。
- **问题与影响**：纠正“只数 Python 调用”是必要的，但参数/状态差分是更新效果证据，不是更新决策的充要判据。一次合法、未被 AMP 抑制的优化器更新也可能数值完全不变。若据此计算跳步率，会把零梯度、零学习率或低精度舍入导致的零增量误作 AMP 跳步，进而误触发新预注册停止条件；反过来，仅部分状态变化也不能保证目标参数更新完整执行。
- **精确证据与静态反例**：E1 的普通路径按 found_inf 决定是否调用优化器，不按参数差分决定。定向补读同一 PyTorch v2.6.0 commit 的 [SGD 参数收集 L82–100](https://github.com/pytorch/pytorch/blob/1eba9b3aa3c43f86f4a2c807ac8e12c4a7767340/torch/optim/sgd.py#L82-L100)、[step L103–148](https://github.com/pytorch/pytorch/blob/1eba9b3aa3c43f86f4a2c807ac8e12c4a7767340/torch/optim/sgd.py#L103-L148)、[单张量更新 L316–353](https://github.com/pytorch/pytorch/blob/1eba9b3aa3c43f86f4a2c807ac8e12c4a7767340/torch/optim/sgd.py#L316-L353)：在普通非融合路径，有限且存在的全零梯度、正学习率、momentum=0、weight_decay=0 时，更新分支会执行，但参数值不变，也不创建 momentum state。它不是 found_inf 导致的跳步。以上为源码静态反例，未运行 SGD/GradScaler 测试，也不借它宣称其他优化器的行为。
- **建议关闭条件**：按 optimizer 分别记录尝试、因非有限值而抑制、确认进入未抑制更新分支的结果，再独立记录参数/master 参数/优化器状态的实际增量；对零增量保留合法零更新、舍入、异常停滞等解释，不直接归为 overflow skip。普通路径可结合调用决策与 found_inf；融合/自定义路径需结合其实际抑制契约与适用测试，不能退回仅数 Python 调用，也不能只凭 scaler.step 返回 None 作判断。预注册跳步率的窗口、分母及未知事件处理；缺乏可靠更新决策证据时保持 unknown。正文、登记和来源补充需同步更正，再针对零梯度/正常非零更新/非有限抑制三类路径复核。
- **与旧发现的关系**：C02 的 step/update 职责分离已经修正，C04 的 min_scale 推断也已删除；本项针对本次替代口径新引入的逆向误判，不重复计入 C02 或 C04。

除 R01 外，本轮未形成其他独立新发现。来源记录旧表与修订补充的可读性问题已在相应 C 项说明，不另拆编号重复计数。

## 总体判定

**仍需修订，第二轮定向复核不通过。** 原发现 C01、C07 尚未闭合，新增 R01 亦为开放 P2；不以多数发现关闭、源码可访问或结构校验成功替代整体通过。已经纠正的调用职责、私有状态边界、min_scale 推断、ROCm 版本范围、案例分层和回链不要求重复返工。

| 验收条款 | 判定 | 本轮依据与剩余门槛 |
| --- | --- | --- |
| 1. FP32/FP16/BF16、累加、master weights、autocast、scale/overflow/跳步及条件 | **部分满足** | 底层 dtype/累加引用 02，master 权重限定于指定路径；GradScaler 职责已修正。Megatron 的完整增长复位分支仍缺（C01），成功更新与零增量的区别仍需更正（R01）。 |
| 2. NVIDIA/AMD 与 Ascend 分别引用，冲突组合保留 unknown | **在明示来源范围内满足** | ROCm 精确版本限定恢复；本轮补开 TorchNPU 两个固定源码。未把多份样板拼成兼容环境；CANN/框架目标配套、算子内部累加、fallback/图/融合冲突和 NPU 收敛数据仍为待验证，不等于三平台环境验收。 |
| 3. 同输入/状态/数据进度、先重复再单因素、分项观测 | **部分满足** | 固定起点、每配置 R 次和三条观测已建立；窗口对齐、scheduler/数据推进账本、可靠更新决策与跳步分母尚未闭合（C07、R01）。 |
| 4. 首差异/传播、窗口/质量、预注册容差/重复/停止，不要求 bitwise | **部分满足** | 质量检查已成为所有通过结论的必经步骤，任务阈值与噪声分离正确。仍需把 R 次分布落实为预注册汇总/不确定性与判定规则（C07），并防止错误跳步率误触发停止（R01）。 |
| 5. 可追溯适配/质量案例及修订或未证实结果，材料不足留 gate | **在算子适配案例范围内满足** | #200537→#200697/cbffccce→回归测试设计可追溯，三层事实与环境门槛齐备；未用 SFT 报告或 issue 关闭替代整训质量因果链。未核定 release、ROCm 对应修复、整训收敛/质量仍显式留 gate。 |

下一轮只需围绕 C01、C07、R01 修订并定向重核。各项关闭前不将 T06-05 标成审阅通过；即使后续全部关闭，正文仍须维持与证据一致的 draft/source_checked 状态，不升级为硬件复现。

### 结构检查与文件范围

- `make check`：在工作仓库通过，107 content entries / 525 sources。
- `make build`：在 `/private/tmp/b25-t06-05-recheck.tVtRW8/repository/` 隔离副本通过，同为 107 content entries / 525 sources；副本保留原有 build/ 链接目标，未改写工作仓库生成目录。两项只验证结构、本地链接与生成流程，不验证技术结论、远端内容或运行行为。
- 以写报告前的文件清单及 SHA-256 清单核对，所有既有受版本管理或未忽略的文件内容均未变化；git status 差集仅新增本报告。其他批次原有改动保留，不作本轮修改或归属。
- 未修改 `src/kb/`，不新增测试，不执行 `make test`、上游单测或训练实验。
