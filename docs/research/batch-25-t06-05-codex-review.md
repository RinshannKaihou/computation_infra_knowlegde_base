# Batch 25 T06-05 初审报告（gpt-6.1-sol / xhigh）

- 日期：2026-10-20（Asia/Shanghai）。
- 审阅对象：[混合精度、算子适配与收敛验证](../../knowledge/06-training/mixed-precision-and-convergence.md)，连同[本批来源记录](batch-25-t06-05-sources.md)、[来源登记](../../sources/registry.yaml)、06 章导航及两篇关联正文。
- 审阅方式：本地 Codex CLI 独立初审；CLI 启动头记录模型 `gpt-6.1-sol`、推理档位 `xhigh`。未委托其他审阅者，未执行 AMP 训练、上游测试或 GPU/NPU 实验。
- 对象快照：正文 SHA-256 `694ade5cc3ec8a3005fbd6429f0a315f7c3ff894f1578d98d866f2adca9690c1`；来源记录 SHA-256 `71627149a53d23b89fe3300312dd73f2d7dd57af6ca2847cb6db6d2796e97686`。下列正文行号针对该快照。
- 写入范围：仅新增本报告；不修改正文、来源记录、registry、导航或其他批次文件。

## 核对范围与取证限制

已重新阅读仓库规范、T06-05 五条验收条款、正文全文、13 个 `source_refs` 的登记，以及 `gpu-npu-precision-difference-triage.md` 和 `dtype-layout-and-precision-semantics.md` 的相关机制、验证与边界段落。

本轮通过网页读取工具重新打开 PyTorch v2.6.0 GradScaler / ShardedGradScaler / FSDP2 测试、2.6 AMP / AMP Examples / Numerical accuracy，以及 issue #200537、PR #200697、commit `cbffccce1e61987e927081fc97cc358b3a7624c3` 的正文、时间线与差异。Shell 的 raw.githubusercontent.com 域名解析失败，GitHub 连接器也发生传输失败，未把失败调用写成成功的 `curl` 或 `gh api` 核验。

对部分无法在线重取的原文件，重新读取 `/private/tmp/b25/` 中的固定取证原件，并将以下六份源码的完整 SHA-256 与 registry/来源记录比对，均相符；行锚以原文件坐标为准，不使用网页工具重排行号：

| 固定原件 | SHA-256 前 16 位 | 本轮核对重点 |
| --- | --- | --- |
| PyTorch v2.6.0 `torch/amp/grad_scaler.py` | `eb4bc91fda9815ba` | 默认参数、unscale/step/update、私有状态清理、融合优化器分支 |
| 同版本 `torch/distributed/fsdp/sharded_grad_scaler.py` | `a54ce5b209840eea` | 分片路径的非有限值收集与指定 process group 归约 |
| 同版本 `test/test_autocast.py` | `df95ba0c7746d4b2` | CPU/GPU/MPS/TorchAutocast 测试组织及条件限制 |
| 同版本 `test/distributed/_composable/fsdp/test_fully_shard_grad_scaler.py` | `f5e034a50e4c5e57` | CUDA/FSDP2 测试条件、内部断言、step 与 update 的先后 |
| Megatron `core_v0.19.2` `megatron/core/optimizer/grad_scaler.py` | `81402e800476fce9` | Constant/Dynamic、hysteresis 状态机及 min_scale |
| 同 tag `megatron/core/optimizer/optimizer.py` | `24609822f7c165c9` | main 参数副本、found_inf、prepare_grads 与跳过更新 |

另重新阅读了本机已留存的 ROCm docs-7.1.1 官方 HTML 原件（含 canonical URL、版本和对应 Known issues 节）；本轮未成功在线重取该页，不声称已验证其当前远端内容。TorchNPU 两个精确 raw URL 本轮未取回，也未找到可独立复读的原件；其底层实现重新核验保持 **unknown**，仅核对了登记与既有 02 章的有限覆盖声明。MindSpeed 脚本的配置不当作 TorchNPU/CANN 收敛或版本交集证明。

## 发现列表

共 **9 项：P1 0 项、P2 8 项、P3 1 项**。以下均为开放发现，须修订并定向复核；没有用测试文件存在、Issue 关闭或结构检查成功替代实际验证。

### B25-T05-C01 — P2：Megatron hysteresis 的“连续 N 次 NaN”与固定实现不一致

- **受影响位置**：正文第 61、112 行；来源记录第 32、43 行；registry `src.nvidia.megatron-grad-scaler-core-v0.19.2` 的 notes（约第 6418 行起）。
- **问题描述**：正文和登记把 hysteresis 写成连续 N 次 NaN/Inf 才回退，来源记录却将精确语义列为 unknown。固定实现不会在每个 finite step 重置 hysteresis；其 docstring 的 consecutive 表述不能代替代码状态机。计数耗尽后，退避本身也不重置计数，后续非有限步可继续退避。因此当前说法会把符合实现的 scale 变化误判为机制异常。
- **证据（上游定位）**：[Megatron grad_scaler.py L131–153](https://github.com/NVIDIA/Megatron-LM/blob/core_v0.19.2/megatron/core/optimizer/grad_scaler.py#L131-L153)：`found_inf` 时递减 `_hysteresis_tracker`，不大于零即退避；finite 分支仅在达到 `growth_interval` 并增长 scale 时重置 hysteresis。静态推演：`hysteresis=2`、`growth_interval>1` 时，`True, False, True` 已可在第三步触发退避，并不要求两次非有限步相邻。这是源码推演，不是本库运行结果。
- **建议关闭条件**：正文、来源记录和登记统一描述实际状态机，指出 docstring 与实现的差别；至少给出交错 finite/non-finite、连续非有限、完整 growth interval 三种静态序列的预期计数。把“实现已读”和“目标环境未运行”分开，不再以笼统 unknown 掩盖已能从代码确定的行为。

### B25-T05-C02 — P2：把 update 与跳过 optimizer step 的责任合在一起

- **受影响位置**：正文第 59 行；registry `src.pytorch.amp-grad-scaler-source-v2.6.0` 的 notes（约第 6390 行起）。
- **问题描述**：“发现 inf/NaN 梯度时 update() 乘 backoff_factor 并跳过该优化器 step”没有区分两个调用的责任。通常路径在 `scaler.step(optimizer)` 决定是否调用底层 step，`update()` 随后消费本轮结果并调 scale，不能撤销先前已执行的更新。融合/自定义 AMP 优化器路径还可能实际调用 `optimizer.step()`，但把 `found_inf` 交给优化器/内核抑制参数更新；不能用 Python step 是否被调用统一定义“跳过更新”。
- **证据（上游定位）**：[PyTorch GradScaler L343–365](https://github.com/pytorch/pytorch/blob/1eba9b3aa3c43f86f4a2c807ac8e12c4a7767340/torch/amp/grad_scaler.py#L343-L365) 为通常 step 的检查/调用分支；[L398–453](https://github.com/pytorch/pytorch/blob/1eba9b3aa3c43f86f4a2c807ac8e12c4a7767340/torch/amp/grad_scaler.py#L398-L453) 为自定义 AMP 路径；[L463–531](https://github.com/pytorch/pytorch/blob/1eba9b3aa3c43f86f4a2c807ac8e12c4a7767340/torch/amp/grad_scaler.py#L463-L531) 才是 scale 更新及清理。FSDP2 测试分别在 [L90–107](https://github.com/pytorch/pytorch/blob/1eba9b3aa3c43f86f4a2c807ac8e12c4a7767340/test/distributed/_composable/fsdp/test_fully_shard_grad_scaler.py#L90-L107) 观察 step 后 optimizer state 与 update 后 scale。
- **建议关闭条件**：明确 `scale/backward → unscale/检查 → scaler.step/更新抑制 → update` 的时序，并注明普通与融合路径区别；按 optimizer 记录真实参数/状态更新和跳步，而不是仅计数 Python 调用。同步更正登记，保留默认四参数数值不变。

### B25-T05-C03 — P2：官方测试的私有 found_inf 状态被称为公开接口

- **受影响位置**：正文第 59、70、83 行；来源记录第 30 行；registry `src.pytorch.amp-tests-v2.6.0` 的证据解释。
- **问题描述**：`_per_optimizer_states[id(opt)]["found_inf_per_device"]` 是固定实现的内部状态，官方测试断言它不等于公开、跨版本稳定的观测 API。正文没有规定采集时点；在 `update()` 后读取已经被清空的字典，可能丢失本轮结果。该测试还明确限制 CUDA/FSDP2 条件并跳过 ROCm，不能作为三平台观测接口或运行通过的证明。
- **证据（上游定位）**：[GradScaler L150–152](https://github.com/pytorch/pytorch/blob/1eba9b3aa3c43f86f4a2c807ac8e12c4a7767340/torch/amp/grad_scaler.py#L150-L152) 初始化内部字典，[L530–540](https://github.com/pytorch/pytorch/blob/1eba9b3aa3c43f86f4a2c807ac8e12c4a7767340/torch/amp/grad_scaler.py#L530-L540) 重置它并说明 `get_scale()` 的同步代价。测试 [L19–26](https://github.com/pytorch/pytorch/blob/1eba9b3aa3c43f86f4a2c807ac8e12c4a7767340/test/distributed/_composable/fsdp/test_fully_shard_grad_scaler.py#L19-L26) 要求至少 4 GPU、`skipIfRocm`；[L76–83](https://github.com/pytorch/pytorch/blob/1eba9b3aa3c43f86f4a2c807ac8e12c4a7767340/test/distributed/_composable/fsdp/test_fully_shard_grad_scaler.py#L76-L83) 在 unscale 后、update 前检查该状态。
- **建议关闭条件**：删除“公开状态”，改为固定源码版本的私有插桩锚；写清采集时点、版本绑定、同步/观测影响及跨平台 unknown。scale 值使用公开方法时也不推导“scale 不变就没有跳步”（Megatron hysteresis/min_scale 下尤其不成立）；测试描述统一用“断言/设计”，不用“已通过”。

### B25-T05-C04 — P2：到达 min_scale 不等于每步被跳过

- **受影响位置**：正文第 83、92 行的 scale 解释和停止条件。
- **问题描述**：将回退到下界与“每步都被跳过、长期空转”直接联系，缺少持续非有限梯度和真实跳步证据。`min_scale` 只是 scale 下限；之后若梯度 finite，优化器仍可正常更新。反过来，hysteresis 尚未耗尽或已到下界时，scale 不变也可能发生跳步。仅凭 scale 形状无法判定训练是否空转；“初期退避后长期稳定”也不是所有动态策略唯一的正常形态。
- **证据（上游定位）**：[Megatron grad_scaler.py L138–153](https://github.com/NVIDIA/Megatron-LM/blob/core_v0.19.2/megatron/core/optimizer/grad_scaler.py#L138-L153) 只对 scale 做下界截断/增长；[optimizer.py L755–774](https://github.com/NVIDIA/Megatron-LM/blob/core_v0.19.2/megatron/core/optimizer/optimizer.py#L755-L774) 返回当前 `found_inf_flag`，[L815–822](https://github.com/NVIDIA/Megatron-LM/blob/core_v0.19.2/megatron/core/optimizer/optimizer.py#L815-L822) 据此跳过更新，不根据 scale 是否等于下界作决定。PyTorch 的 [update 警告](https://github.com/pytorch/pytorch/blob/1eba9b3aa3c43f86f4a2c807ac8e12c4a7767340/torch/amp/grad_scaler.py#L482-L487) 也不保证 scale 大于 1，不能移植 Megatron 下界概念。
- **建议关闭条件**：把停止策略写成预注册的非有限值持续次数/跳步率/有效更新停滞条件；若选择“一触下界就暂停”作为保守策略，明确这是本库建议而非实现必然空转。分列 scale、found_inf、实际更新三条观测，按实现解释常数、增长、退避和下界平台期。

### B25-T05-C05 — P2：ROCm 已知不支持项缺失原页的版本限定

- **受影响位置**：正文第 53、63 行；来源记录第 37 行的支持范围。
- **问题描述**：正文把相关开关概括成 ROCm 侧已知不支持项，却遗漏原页节标题限定的 **PyTorch 2.7/2.8 + ROCm 7.0/7.1**。`docs-7.1.1` 是文档版本，不表示页面内每项结论适用于该版本的所有 PyTorch 组合，更不能把它直接套到正文的 PyTorch 2.6 样板。此发现不是断言其他组合已支持，而是要求那些组合保持 unknown。
- **证据（上游定位）**：[ROCm docs-7.1.1 精确章节](https://rocm.docs.amd.com/en/docs-7.1.1/compatibility/ml-compatibility/pytorch-compatibility.html#known-issues-and-notes-for-pytorch-2-7-2-8-with-rocm-7-0-and-rocm-7-1) 在该版本组合节内列出 `torch.backends.cuda.matmul.allow_fp16_reduced_precision_reduction` 和 `allow_bf16_reduced_precision_reduction` 不支持。本轮重新阅读的官方 HTML 原件有同一 canonical URL 与节标题；没有在线成功重取，不据此扩张至当前远端或未列组合。
- **建议关闭条件**：正文与来源记录保留精确版本组合和两个完整字段；明确 PyTorch 2.6 AMP 机制样板与 AMD 兼容档案分立，不暗示拼成已验证环境。需要覆盖其他 PyTorch/ROCm 组合时另取精确证据；不把“开关不支持”扩大成“AMD 不支持 AMP/BF16”。

### B25-T05-C06 — P2：dtype 案例被外推成收敛表现，且缺少关键环境门槛

- **受影响位置**：正文第 81、86 行；来源记录第 38 行的案例支持范围。
- **问题描述**：案例末句“静默偏差不会报错，只会在收敛曲线上现形”超过证据。该链支持的是 autocast 目标 dtype 错配及包装器修订，未提供有限训练窗口、optimizer update 或任务质量曲线；dtype 检查本身已能观察异常，不能承诺必在收敛曲线显现。正文也没有带入报告者的版本/设备和回归测试的 BF16 硬件、cuDNN >= 9.13、跳过 ROCm 条件。步骤 2 将此类问题统称“先修配置”，会混淆用户配置错误与上游硬编码实现错误。
- **证据（上游定位）**：[issue #200537](https://github.com/pytorch/pytorch/issues/200537) 于 **2026-10-10** 打开，报告者给出 nightly `2.16.0.dev20261010+cu130`、RTX 3090、cuDNN 9.26 的 dtype 观测，并自述另外两版本表现；调查文字由报告者提交，不是本库复现。修复 commit [AutocastRNN.cpp L39–104](https://github.com/pytorch/pytorch/blob/cbffccce1e61987e927081fc97cc358b3a7624c3/aten/src/ATen/cudnn/AutocastRNN.cpp#L39-L104) 将目标类型接到 autocast 配置；[test_cuda.py L13942–14006](https://github.com/pytorch/pytorch/blob/cbffccce1e61987e927081fc97cc358b3a7624c3/test/test_cuda.py#L13942-L14006) 设计 dtype、同路径参考输出及 backward 梯度断言，并显式限定硬件/cuDNN、跳过 ROCm。这不是训练收敛或测试执行通过记录。
- **建议关闭条件**：案例分列“报告者自述”“修复方实现/测试设计”“本库未复现”；删除收敛必然变化断言，保留可迁移的实际 dtype 核对经验。补环境门槛和“修复进入何 release、ROCm 修复、整训质量仍 unknown”的来源 gate。步骤 2 改为先定位配置/实现/支持条件，再在授权范围内选修订或替代路径，不能把改 dtype 当成已证修复。

### B25-T05-C07 — P2：有限窗口对照的重复、计步与质量验收路径未闭合

- **受影响位置**：正文第 80–84、100–104 行。
- **问题描述**：已通过旧指南继承输入/状态/数据进度冻结，但本页步骤 3 写每组一次窗口、步骤 5 写各一窗口；“重复次数/样本量”条目实际只列窗口步数、验证样本量与 seed，没有写每配置独立重复次数及汇总规则。改变 scale 后，尝试的 batch 数与实际成功更新数可分离，正文未规定窗口按哪一个计步或如何记录 scheduler/数据推进。步骤 3 只在“差异传播到质量”时转步骤 5，也没有规定未见明显首差异/已知偏差的组仍须做独立质量验收，容易提前判可接受。
- **证据（上游定位）**：[AMP Examples 的 Gradient accumulation 节](https://docs.pytorch.org/docs/2.6/notes/amp_examples.html#gradient-accumulation) 把检查、跳步、scale 更新绑定到 effective batch；[GradScaler 的 step 分支](https://github.com/pytorch/pytorch/blob/1eba9b3aa3c43f86f4a2c807ac8e12c4a7767340/torch/amp/grad_scaler.py#L343-L365) 说明一次尝试不必产生一次更新。上游没有给本任务的重复次数或验收阈值；这些必须由本库验证方案预注册，不能从官方单测的固定 seed 推出。
- **建议关闭条件**：预注册每配置重复次数、每次从同一状态恢复的范围、窗口按样本/token/尝试步计量的口径，并同时记录成功更新数、跳步与 scheduler 推进。说明新建/恢复 scaler 时哪些状态固定、哪个是实验变量。每组重复的聚合/不确定性规则写清；将固定验证集质量检查设为所有“通过/可接受”结论的必经步骤，证据缺失只能报 unknown。

### B25-T05-C08 — P2：容差必须大于噪声的规则缺少任务质量上限

- **受影响位置**：正文第 74、99、101 行。
- **问题描述**：噪声带描述平台内波动，不自动授权把验收阈值放宽到它上方。当噪声已大于任务允许退化时，“容差必须大于噪声”会与任务质量约束及不放宽阈值的停止条件冲突。当前没有规定这种情况应补充重复/样本、缩小不确定性或保持 unknown，而不是提高容差。也没有区分单算子数值误差界、训练窗口波动界与任务质量可接受界。
- **证据（上游定位）**：[PyTorch 2.6 Numerical accuracy](https://docs.pytorch.org/docs/2.6/notes/numerical_accuracy.html) 解释浮点非结合性、平台差异和有限精度边界，但不提供本任务的收敛/质量阈值，也不能推出“验收容差必须随噪声增大”。本库旧[精度差异指南](../../knowledge/06-training/gpu-npu-precision-difference-triage.md) 第 103–112 行要求有任务依据的容差，且证据不足时允许 unknown。
- **建议关闭条件**：把任务允许退化阈值与噪声估计/统计分辨能力分列；预先定义当不确定性无法支持阈值判定时补采或停止的规则。可以采用与任务相称的区间/重复汇总方法，但不得事后放宽质量标准，也不要求跨平台 bitwise。

### B25-T05-C09 — P3：新页只有出链，关联基础页没有回链

- **受影响位置**：新页第 24–28、49 行；`gpu-npu-precision-difference-triage.md` 的 related_ids/完成判据；`dtype-layout-and-precision-semantics.md` 第 37 行起及第 76、86–90 行。
- **问题描述**：06 章索引已正确登记本页，但两篇基础页都没有指回新页的普通 Markdown 链接或 related ID。02 章仍仅以“归 06.5”描述训练判据去向，读者从底层 dtype/累加语义进入时无法直接到达新增训练流程。当前主归属没有冲突，问题是要求的互链尚未闭合。
- **证据（定位）**：本地[06 章索引](../../knowledge/06-training/index.md) 第 50、68、77 行已有入口；两篇基础页的相关段和元数据均无 `training.mixed-precision-and-convergence` 或目标文件链接。上游 [AMP 机制页](https://docs.pytorch.org/docs/2.6/amp.html) 与 [AMP Examples](https://docs.pytorch.org/docs/2.6/notes/amp_examples.html) 分列机制与训练使用，也不能代替本库内部导航。
- **建议关闭条件**：后续修订在两篇基础页各补一个明确的训练层回链，必要时补 related ID；02 保留 dtype/计算/累加底层语义，06.5 保留梯度、优化器、窗口和质量判断，不复制整篇正文。本轮按只新增报告的限制不代改。

## 已核实而不构成新发现的事项

- frontmatter 的 ID、type、domain、标题、日期及 `draft / source_checked` 形式符合约定；13 个 source_refs、4 个 evidence_refs 均能在 registry 找到对应 ID。正文明确没有训练/硬件运行结果；没有把官方测试写成“本库已通过”。语义上的 source_checked 覆盖仍受开放发现和本轮 unknown 限制。
- PyTorch v2.6.0 `GradScaler` 的四项默认值确为 `init_scale=2^16`、growth 2.0、backoff 0.5、interval 2000（原文件 L119–126）；cuda AMP shim 的弃用方向正确。unscale 后 clip、有效 batch 边界 update 的方向与官方示例一致。
- Megatron 固定 `Float16OptimizerWithFloat16Params` 路径确有低精度模型参数的 FP32 main 参数副本（`optimizer.py` L988–1026）；这不自动变成所有 autocast 或全部优化器的 master-weight 承诺。FP32/FP16/BF16 格式及内部累加的基础解释可继续引用 02 章，无须在本页重写底层语义。
- ShardedGradScaler 原文件 L258–278 确有按指定 process group 的 found_inf 归约；不能把该特定实现扩大成普通 GradScaler 自动替任意 DDP/并行组合完成一致性保证。本文未建立全部分布式组合，继续细项标 unknown 合理。
- 案例时间线与关闭方式没有发现相反证据：Issue 于 **2026-10-14** 由 bot 在 `cbffccce...` 关闭；PR 页面显示 Closed、Merged 标签及指向该 commit 的 bot 关闭事件，commit 注明对应 #200697。支持“经 mergebot 提交落地”，不以 Closed 推导未落地，也不以 Merged 标签推导测试/任务质量通过。GitHub API 的 `merged` 字段本轮未重取，沿用记录而不宣称重新核验。
- fallback、图/融合路径与精度支持交集的未知没有被虚写为完整兼容矩阵；NPU 官方训练窗口数据缺失、案例 ROCm 侧修复未核对、未确定 release tag 的边界应保留。

## 总体判断与验收条款对照

**总体判断：需修订，初审不通过；不是硬件验证失败结论。** 当前骨架、主归属和来源可追溯性基本成立，但精确机制、版本限定和对照判据仍存在开放 P2，不能据此宣布 T06-05 验收通过。

| 验收条款 | 本轮判断 | 已有覆盖与缺口 |
| --- | --- | --- |
| 1. FP32/FP16/BF16、累加、master weights、autocast、动态 scale/overflow/跳步及条件 | 部分满足 | 可引用 02 的底层语义，已有训练机制骨架、默认值和 master 参数实现；hysteresis、step/update、私有观测及 min_scale 推断须关闭 C01–C04。 |
| 2. NVIDIA/AMD 与 Ascend 分别引用，冲突组合 unknown | 部分满足 | 来源分立及 fallback/图/融合 unknown 方向正确；ROCm 精确版本条件须关闭 C05。TorchNPU 两原文件本轮重新核验受阻，目标 CANN/框架配套、逐算子累加与收敛证据仍 unknown，不计作已重核。 |
| 3. 同输入/状态/数据进度，先重复再单因素，分项观察 | 部分满足 | 已继承旧指南冻结清单，观察项分列；found_inf 观测契约、各配置重复和尝试步/成功更新计量须关闭 C03、C07。 |
| 4. 首差异/传播、有限窗口/质量、预注册容差/重复/停止，不要求跨平台 bitwise | 部分满足 | 主方向正确；质量验收必经路径、重复与不确定性、噪声/任务阈值分离、停止语义须关闭 C04、C07、C08。 |
| 5. 可追溯适配/质量案例及修复或未证实结果，材料不足留 gate | 部分满足 | Issue→PR/commit→测试设计链可作为算子适配案例；须关闭 C06，补环境门槛与事实分层。整训收敛/质量因果链仍无证据，必须显式保留来源 gate；没有用既有 SFT 报告替代。 |

优先修订 C01–C06 的机制与证据边界，再补 C07–C08 的判据闭环，最后补 C09 回链。修订后需同一审阅者定向重读对应源码和正文/来源/登记三处的一致性；被网络限制的精确来源也需补开。任何关闭结论均只覆盖明示范围，不升级为平台兼容、训练收敛或本地硬件复现。

## 结构检查与文件范围

- `make check`：通过，107 content entries / 522 sources；仅证明结构和本地文件链接，不证明技术正确性或远端内容。
- `make build`：在 `/private/tmp/` 隔离副本通过，同为 107 content entries / 522 sources，生成 `build/catalog.json` 和 `build/catalog.md`；未改写工作仓库的生成目录。首次复制排除了已有 build，导致既有 `docs/first-fill-status.md` 的两条 build 链接在预检时缺目标；补入已有生成目录后重跑成功，该隔离准备问题不计入正文发现。
- 正文与来源记录的 SHA-256 在写报告后保持上述快照不变；本轮对仓库的写入仅为本报告。其他批次已有/并发改动保留，不作归属或修改。
- 未修改 `src/kb/`，未新增测试；未执行 `make test`、上游测试、硬件测试或训练验证。
