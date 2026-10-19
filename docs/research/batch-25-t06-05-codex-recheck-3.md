# Batch 25 T06-05 定向复核报告（第四轮，gpt-6.1-sol / xhigh）

- 日期：2026-10-20（Asia/Shanghai）。
- 对象：[第四轮修订正文](../../knowledge/06-training/mixed-precision-and-convergence.md)、[来源记录第四轮补充](batch-25-t06-05-sources.md)，对照[第三轮复核](batch-25-t06-05-codex-recheck-2.md)、[第二轮复核](batch-25-t06-05-codex-recheck.md)与[初审 C01–C09](batch-25-t06-05-codex-review.md)。验收范围沿用[任务表 T06-05](../../plans/full-coverage-backlog.yaml)的条款 1–5。
- 执行方式：本地 Codex CLI 当前会话定向复核，未另启审阅代理。核对 `/private/tmp/b25/recheck3-t06-05-run.log` 启动头与对应任务输入：Codex v0.157.1，启动记录的单一模型为 `gpt-6.1-sol`、推理档位为 `xhigh`；据该记录填写，不追改历史模型记录。未执行上游单测、GradScaler/优化器行为实验或 GPU/NPU 训练。
- 对象快照：正文 SHA-256 `ea2516eee89e583ecdf03b212a115d712b403e3bcf5d316999d888b814ad65d8`；来源记录 `c1ef90a0011f1f4a7accf3634bdf7887fffcf6e90919d76a1c525f7e0935bdc8`；registry `99b81d2047b01fc2ed7885143d062e6e0d7b44a0415db22dd63d1d9dd474857b`。下列正文与来源行号指此快照。
- 写入边界：只新增本报告；不代改正文、来源记录、registry、导航、任务状态或工作仓库的生成文件。既有其他批次改动不归属于本轮。

## 结论摘要

**B25-T05-R01：CLOSED。C01–C09 全部维持 CLOSED，未见回归；未发现需要新增 `B25-T05-R3-xx` 编号的独立问题。开放审阅项为 0。**

**T06-05 通过既定审阅范围。** 本轮关闭的是跳步率的统计契约缺口，不是平台兼容、真实训练收敛或任务质量的实验验收；正文仍应保持与证据一致的 `draft / source_checked` 状态。

## R01：CLOSED——分母、未确认事件与零尝试窗口闭合

核对位置：正文 L59、L92、L101–103；来源记录 L63、L65–67。第三轮的最小剩余关闭条件已逐项满足：

| 检查项 | 当前修订与复核判断 |
| --- | --- |
| 统计对象与窗口 | L92 按 optimizer 分列并预注册分子、分母；L101 仍要求预注册窗口对齐轴、实际推进量和判读规则。窗口按样本/token 或成功更新数对齐，也不会将它们偷换为跳步率分母。 |
| 分子 | 仅计该窗口内“确认因非有限值被抑制”的次数，不以参数零增量、scale 不变或 `scaler.step()` 返回 `None` 判跳步；L59 的普通路径与融合/自定义路径证据要求保留。 |
| 分母与粒度 | 明确为该 optimizer 在有效 batch 边界的 step 尝试数；显式排除 micro-step、成功更新数和仅可分类事件的子集，多 optimizer 不共用全局分母。与 E1 的有效 batch 粒度及独立 optimizer 决策一致。 |
| 未确认事件 | 尝试数与两类确认数不闭合时保留未确认账本，报告有依据的上下界或保守 unknown；明确禁止静默丢弃及填作成功/跳步。因而不再把证据缺失伪装成完整分类。 |
| 阈值判读 | L92 的上下界/unknown 与 L101 的预注册通过、失败、unknown 规则及 L102 的缺证据兜底合读；不能用跨越阈值的区间强行给出确定结论。无须由本库指定统一停止阈值。 |
| 零分母 | L92 明确无尝试的窗口不产出比率；不能将其填为 0% 或据此推出“未跳步、质量通过”。 |
| 来源记录同步 | L67 准确记录上述剩余修订，与正文一致；L63 的事件定义继续有效。registry 中更新决策与参数效果分离的说明未被改写。 |

### 三类已确认路径与不完整账本的静态核对

以下为**构造账本与源码静态推演，不是训练或优化器运行结果**。前三行沿用第三轮的普通、非融合、单张量 SGD 限定：参数初值 1、学习率 0.5、momentum=0、weight_decay=0、无 closure；finite 梯度指 unscale 后的梯度。E2 支持其更新分支与参数效果的区别，不向其他优化器或融合内核外推。

| 构造路径/窗口 | 尝试数 | 确认非有限抑制数 | 确认未抑制分支数 | 未确认数 | 按修订契约的结果 |
| --- | --- | --- | --- | --- | --- |
| finite 全零梯度 | 1 | 0 | 1 | 0 | 跳步率 0/1；参数保持 1 属合法零增量，不能改记为跳步。 |
| finite 非零梯度 1 | 1 | 0 | 1 | 0 | 跳步率 0/1；参数静态计算为 0.5，更新决策与增量分别记账。 |
| 本轮检查发现非有限梯度 | 1 | 1 | 0 | 0 | 跳步率 1/1；普通 GradScaler 路径不调用底层 SGD 更新，不能与第一行仅凭参数不变混为一类。 |
| optimizer A：10 次尝试中 1 次未确认 | 10 | 1 | 8 | 1 | 确认抑制占比 1/10；完整跳步比例只可约束为 [1/10, 2/10]，或保守 unknown，不能报 1/9 或伪造点值。 |
| optimizer B：另有独立 4 次尝试 | 4 | 1 | 3 | 0 | 单列 1/4，不借 A 的 10 次尝试或两者合计 14 次作分母。 |
| 只有未确认结果 | 3 | 0 | 0 | 3 | 至多得到 [0, 1] 或 unknown；不能因确认抑制数为零就报实际跳步率 0%。 |
| 没有 step 尝试 | 0 | 0 | 0 | 0 | 不产出比率，不计算 0/0，不填 0%。 |

当尝试总数已知、确认分类互斥且账本能闭合时，未确认数可由 `attempts - confirmed_suppressed - confirmed_not_suppressed` 得到；上述可行上下界分别为 `confirmed_suppressed / attempts` 与 `(confirmed_suppressed + unconfirmed) / attempts`。这是对未知分类的**确定性边界推算，不是统计置信区间**；重复窗口的不确定性仍按 L101 的另行预注册规则处理。无法建立有依据的边界时保持 unknown，不补造确认事件。

对第四行，若沿用第三轮构造例的停止阈值 15%，[10%, 20%] 跨越阈值，不能把 10% 当成确定的真实比例来放行；按预注册规则保留 unknown，或采用事先约定的保守处置。这只是判读演示，不是通用阈值建议，也不替代固定验证集质量检查。即便该窗口含 40 个 micro-step，分母仍为 10 次有效 batch 边界尝试，不变成 40。

**R01 的事件定义、统计粒度、分母与未知事件处理现已共同可复算，满足第三轮关闭条件。** 无须重写已正确的状态机或要求补做硬件实验才关闭此编辑问题。

## C01–C09 回归检查

先核验第三轮隔离副本 `/private/tmp/b25-t06-05-recheck2.ebcADp/repository/` 的正文、来源记录、registry 哈希，均与第三轮报告快照一致，再与本轮对象逐文件比较：**正文唯一变化为 L92 的 R01 统计契约；来源记录仅追加 L65–67 的第四轮修订；registry、两篇关联基础页与 06 章索引字节级未变。** 下表另对当前段落和回链作了定向重读，不仅依据作者修订摘要判断。

| 原发现 | 判定 | 当前证据与不回归依据 |
| --- | --- | --- |
| B25-T05-C01 | **CLOSED，未回归** | L61 保留初始 tracker、非有限减计数/退避不复位、finite 未满窗口不复位、完整增长窗口同时复位/增长，以及三组静态序列；重取 E3 的实现与之相符。 |
| B25-T05-C02 | **CLOSED，未回归** | L59 与 registry L6403 保留普通 step 决策、融合/自定义内核抑制、update 只调 scale 的职责分离；E2 重读支持。新 L92 不将 update 或 Python 调用次数重新用作跳步判据。 |
| B25-T05-C03 | **CLOSED，未回归** | L59/L70 与 registry L6417 继续将 found_inf 标为固定实现内部插桩，规定 unscale 后/update 前采集；E4 的 CUDA/FSDP2、≥4 GPU、skipIfRocm 及 E2 的状态清理相符。不承诺跨平台公开接口或观测无开销。 |
| B25-T05-C04 | **CLOSED，未回归** | L61/L83/L92 仍分开 scale、非有限事件与更新决策；触及 min_scale 即停只可能是本库保守策略，不被写成实现必然空转。新增统计契约没有重新引入从 scale 形状推断跳步的逻辑。 |
| B25-T05-C05 | **CLOSED，未回归** | L63 与来源 L54 的两个 reduced-precision-reduction 开关限制仍绑定 PyTorch 2.7/2.8＋ROCm 7.0/7.1 节，并与 PyTorch 2.6 样板分立；其他组合继续 unknown。本轮未重新核验远端 ROCm 页，不扩大第三轮证据范围。 |
| B25-T05-C06 | **CLOSED，未回归** | L81/L86 保留报告者自述、上游修复/测试设计、本库未复现三层，以及 BF16 硬件、cuDNN≥9.13、跳过 ROCm 等限定；不从 dtype 错配推导整训收敛必然异常。案例所属 release、ROCm 对应修复及整训质量影响仍未知。 |
| B25-T05-C07 | **CLOSED，未回归** | L80–84/L94/L101–103 保留每配置 R 次、冻结状态恢复、窗口对齐轴、scheduler/数据游标推进账本、汇总量与不确定性及判读规则；所有通过结论均须质量验收。跳步率分母在此基础上补齐，没有把对齐轴与统计分母混为一谈。 |
| B25-T05-C08 | **CLOSED，未回归** | L74/L91/L93/L100 继续分列任务质量上限与噪声/统计分辨能力；不确定性不足时补采或 unknown，不提高质量容差、不要求跨平台 bitwise。本轮未确认事件的边界亦未被用作放宽质量标准的依据。 |
| B25-T05-C09 | **CLOSED，未回归** | 精度差异指南 L16/L106、dtype/layout 基础页 L76 与 06 章索引 L26/L50/L68/L77 的普通 Markdown 链接/related ID 均保留；02 的底层语义与 06 的训练机制、窗口/质量判据主归属未变。 |

来源记录早期表中“公开状态”“连续 N 次”“仅读到 docstring”“按参数/状态变化判断”的旧文字，继续按 L49–67 的分轮更正及当前正文/registry 解读，沿用前两轮的历史记录处理，不把已更正的历史表述重新计为当前发现。

## 本轮上游取证与新问题检查

以下 E 编号只为本报告定位，均对应既有登记来源，不新增来源或变更版本范围：

- **E1 — 有效 batch 与多 optimizer**：重新打开 [PyTorch 2.6 梯度累积节](https://docs.pytorch.org/docs/2.6/notes/amp_examples.html#gradient-accumulation)和[多 optimizer 节](https://docs.pytorch.org/docs/2.6/notes/amp_examples.html#working-with-multiple-models-losses-and-optimizers)。前者将检查、跳步与 scale 更新约束到有效 batch；后者按 optimizer 分别 step、独立作跳步决策。统计上下界、重复次数和停止阈值是本库验证设计，不冒称上游提供了这些验收标准。
- **E2 — 更新决策、参数效果与状态清理**：GitHub 连接器重新取得固定 commit `1eba9b3aa3c43f86f4a2c807ac8e12c4a7767340` 的 [GradScaler L343–460](https://github.com/pytorch/pytorch/blob/1eba9b3aa3c43f86f4a2c807ac8e12c4a7767340/torch/amp/grad_scaler.py#L343-L460)、[update/get_scale L463–540](https://github.com/pytorch/pytorch/blob/1eba9b3aa3c43f86f4a2c807ac8e12c4a7767340/torch/amp/grad_scaler.py#L463-L540)、[SGD L82–148](https://github.com/pytorch/pytorch/blob/1eba9b3aa3c43f86f4a2c807ac8e12c4a7767340/torch/optim/sgd.py#L82-L148)与[单张量更新 L316–353](https://github.com/pytorch/pytorch/blob/1eba9b3aa3c43f86f4a2c807ac8e12c4a7767340/torch/optim/sgd.py#L316-L353)。对应文件 blob 分别为 `3e99b223adb441fecd227129664cc463572e147c`、`75cd3279070b4ce259874f311527b65f1ceb6590`。只据源码判断普通/融合职责及零增量反例，没有执行框架行为测试。
- **E3 — Megatron 状态机**：raw 页面读取失败后，经 GitHub 连接器重取 [core_v0.19.2 grad_scaler.py L127–153](https://github.com/NVIDIA/Megatron-LM/blob/core_v0.19.2/megatron/core/optimizer/grad_scaler.py#L127-L153)，文件 blob `036564889825ef6a5b3f27fc0e39386730f17e36` 与第三轮一致；不是依据 docstring 推断 finite 复位分支。optimizer 的 master 权重与更新抑制实现沿用第三轮证据，不冒称本轮再次重核全文。
- **E4 — 私有状态测试边界**：重新取得[同 PyTorch commit 的 FSDP2 测试 L19–83](https://github.com/pytorch/pytorch/blob/1eba9b3aa3c43f86f4a2c807ac8e12c4a7767340/test/distributed/_composable/fsdp/test_fully_shard_grad_scaler.py#L19-L83)，核对装饰器、设备与 unscale 后的断言位置；只确认测试设计，未运行套件。

本轮针对新增 L92 检查了分母偷换、不同 optimizer 频次、合法零增量、未确认事件丢失/填值、区间跨阈值及零分母等反例，未发现新的独立缺陷；**不分配 `B25-T05-R3-01` 或后续编号**，也不将 R01 的本轮关闭重编号为新问题。TorchNPU、ROCm 及案例修复/测试原件没有在本轮全部重取，未变部分的来源结论沿用第三轮明示范围，不冒称完成新一轮全量远端核验。

## 最终整体判定与验收条款 1–5

| 条款 | 本轮判断 | 范围与保留边界 |
| --- | --- | --- |
| 1. 精度、累加、master weights、autocast、scale/overflow/跳步及条件 | **在已核机制范围内满足** | 底层语义沿用 02；master 权重限定指定实现；C01–C04 维持关闭，R01 的事件与比率契约现已闭合。不等于全部优化器/融合内核行为均已验证。 |
| 2. NVIDIA/AMD 与 Ascend 分别引用，冲突组合 unknown | **在明示来源范围内满足** | 实现样板分立，ROCm 版本限定保留；目标 TorchNPU/CANN 配套、逐算子内部累加、fallback/图/融合支持交集仍待验证。 |
| 3. 同输入/状态/数据进度、先重复再单因素、分项观测 | **在流程设计范围内满足** | C07 的冻结范围、每配置重复和进度账本未回归；新增逐 optimizer 的有效 batch 尝试分母与未确认事件保留规则，使停止指标可复算。 |
| 4. 首差异/传播、有限窗口/质量、预注册容差/重复/停止 | **在判读契约范围内满足** | 全配置质量必经、汇总/不确定性与通过/失败/unknown 预注册、任务阈值独立均保留；R01 不再阻断停止判据。没有给出虚构的通用阈值、样本量或质量结果。 |
| 5. 可追溯适配案例及修复或未证实结果，材料不足留 gate | **在算子适配案例范围内满足** | 沿用已核的 #200537→#200697/固定修复 commit→测试设计链及事实分层；所属 release、ROCm 对应修复和整训质量影响继续留 gate，不用 SFT 报告、issue 关闭或 dtype 断言替代质量因果链。 |

**最终：R01 CLOSED；C01–C09 CLOSED 且未回归；无新增开放项，T06-05 通过既定审阅范围。** 上述来源/环境/实验 gate 是明确保留的证据边界，不因审阅通过而自动关闭；本报告不将正文改为 `reviewed` 或 `reproduced`，也不代改任务表状态。

## 结构检查与文件范围

- `make check`：通过，107 content entries / 525 sources。
- `make build`：在 `/private/tmp/b25-t06-05-recheck3.RUN4El/repository/` 隔离副本通过，同为 107 content entries / 525 sources；副本保留原有 build 链接目标，未改写工作仓库 `build/`。两项只验证结构、本地链接与生成流程，不证明技术结论、远端内容或运行行为。
- 7 组构造账本的纯算术校核通过，包括三类已确认路径、未确认/全未确认、不同 optimizer 分母与零尝试窗口；这不是上游单测、硬件实验或训练结果。
- 文件边界核对：535 个既有文件的首次 SHA-256 对照均未变化或删除，三个复核对象哈希始终不变。随后观察到工作仓库 `build/catalog.json` 同期变化；已核对其与本轮隔离副本为不同文件、不同 inode，本轮未写入或还原该工作仓库产物，不将同期变化归为本轮修改。另有 `batch-25-t06-07-codex-recheck-2.md` 新报告同期出现，不计作本轮写入；本报告通过空白检查。
- 本轮只新增 `docs/research/batch-25-t06-05-codex-recheck-3.md`；正文、来源记录与 registry 不代改。未修改 `src/kb/`，不新增测试，不执行 `make test`、上游单测或训练实验。
