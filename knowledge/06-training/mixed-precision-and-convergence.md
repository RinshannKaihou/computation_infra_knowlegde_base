---
id: training.mixed-precision-and-convergence
title: 混合精度、算子适配与收敛验证
type: procedure
domain: training
status: draft
platforms: [nvidia, amd, ascend]
source_refs:
- src.pytorch.amp-2.6
- src.pytorch.amp-examples-2.6
- src.pytorch.amp-grad-scaler-source-v2.6.0
- src.pytorch.amp-tests-v2.6.0
- src.pytorch.set-float32-matmul-precision-2.6
- src.pytorch.numerical-verification-2.6
- src.nvidia.megatron-grad-scaler-core-v0.19.2
- src.ascend.torchnpu-amp-7.2.0
- src.ascend.torchnpu-autocast-ops-7.2.0
- src.ascend.mindspeed-llm-workflows-v2.2.0
- src.ascend.msprobe-training-guide-2026-09-30
- src.amd.pytorch-compatibility-7.1.1
- src.pytorch.issue-200537
updated_at: "2026-10-20"
summary: 把首差异诊断扩展到 autocast、动态 loss scale、master 权重与算子精度策略：先证平台内重复性，再做单因素精度/算子对照，把误差、NaN/Inf、梯度与 loss scale 分开观察，用预先固定的容差与有限训练窗口判断收敛与任务质量是否可接受。
related_ids:
- training.gpu-npu-precision-difference-triage
- training.parallelism-and-state
- training.framework-execution
- software-stack.dtype-layout-and-precision-semantics
- reliability.silent-errors-and-integrity
applicability:
  environment_refs: []
  notes: "流程以 PyTorch 2.6（固定 v2.6.0 源码）、Megatron core_v0.19.2、TorchNPU 7.2.0（固定 commit）与 ROCm docs-7.1.1 文档为可核对样板；目标 GPU/NPU 环境、模型、数据与并行布局尚未建立环境档案。"
verification:
  status: source_checked
  evidence_refs:
  - src.pytorch.amp-grad-scaler-source-v2.6.0
  - src.pytorch.amp-tests-v2.6.0
  - src.nvidia.megatron-grad-scaler-core-v0.19.2
  - src.pytorch.issue-200537
  notes: "已核对固定版本源码/测试/文档与案例链（锚点见 docs/research/batch-25-t06-05-sources.md）；未运行任何 AMP 训练、GradScaler 行为测试或精度对照。"
---

# 混合精度、算子适配与收敛验证

## 目标与触发条件

本流程回答三个问题：**启用/调整混合精度后训练是否还在算同一件事**（数值行为）、**loss scale 与算子精度策略是否按预期工作**（机制）、**训练是否仍收敛且任务质量可接受**（结果）。触发条件：切换 FP16/BF16/autocast 配置、更换算子精度策略（fusion/图路径）、迁移平台后出现 loss 曲线差异、NaN/Inf、loss scale 异常波动或下游质量下降。

首差异定位与平台内重复性的基础方法沿用[GPU 到 NPU 的精度差异诊断指南](gpu-npu-precision-difference-triage.md)；本页在其上补齐 autocast/loss scale 机制层与收敛/质量判据层。dtype/layout 的底层语义见 02 章[dtype、layout、格式转换与有限精度语义](../02-software-stack/dtype-layout-and-precision-semantics.md)。

## 适用范围与前置条件

三组证据样板分立，不可交叉外推：PyTorch 2.6（v2.6.0 固定源码）、Megatron core_v0.19.2（自带 loss scale 实现）、TorchNPU 7.2.0（固定 commit，配 CANN 栈）。ROCm 侧依据 docs-7.1.1 兼容文档。前置条件：固定的模型/数据/优化器/并行配置 checkpoint 与输入样本（沿用精度差异指南的证据清单）；预先写下的容差、重复次数与停止条件（见完成判据）。

## 机制速览（判断分支的依据）

**autocast 的边界**：`torch.autocast` 只包裹 forward（含 loss），backward 沿用 forward 产生的 dtype；算子分三类处理——强制低精度、强制 FP32、按输入提升（[AMP 文档](https://docs.pytorch.org/docs/2.6/amp.html)）。`torch.cuda.amp.*` 命名已弃用，以 `torch.autocast(device_type=…)` 与 `torch.amp.GradScaler` 为准（[cuda shim 源码](https://github.com/pytorch/pytorch/blob/v2.6.0/torch/cuda/amp/grad_scaler.py)）。TorchNPU 侧 `get_amp_supported_dtype` 按设备支持返回 `[float16, bfloat16]` 或 `[float16]`——**BF16 autocast 在 NPU 上是条件能力，不是默认承诺**；逐算子的 autocast 归属在 TorchNPU 的 AutoCastOps 注册表，归属策略不等于该算子计算/累加精度的证据。

**GradScaler 的精确语义**（[v2.6.0 源码](https://github.com/pytorch/pytorch/blob/v2.6.0/torch/amp/grad_scaler.py)）：一轮的时序是 `scale(loss)→backward→unscale_（检查 inf/NaN）→ scaler.step(optimizer)`——普通路径下 `step()` 按本轮检查结果决定是否调用底层 `optimizer.step()`（被跳过时权重不被该批梯度破坏）→ `update()` 消费本轮结果并调整 scale。**职责边界**：`update()` 只调 scale，不能撤销已执行的更新；融合/自定义 AMP 优化器路径可能实际调用 `optimizer.step()` 而由优化器/内核按 `found_inf` 抑制参数更新。因此**跳步的判据不能是"参数数值是否变化"**——一次未被抑制的合法更新也可能数值不变（零梯度、零学习率或舍入为零增量的静态反例见 v2.6.0 SGD 更新分支）；可靠的观测是按 optimizer 分三层计数：**尝试的 step 数**、**因非有限值被抑制的数**（普通路径结合 `scaler.step` 调用决策与 found_inf 判定，版本绑定的插桩；融合路径按其实际抑制契约）、**确认进入未抑制更新分支的数**；参数/master 参数/优化器状态的实际增量**独立记录**，零增量保留"合法零更新/舍入/异常停滞"等多种解释，不直接归为 overflow skip（`scaler.step` 返回 None 也不单独构成判断）。scale 调整规则：本轮发现 inf/NaN 乘 `backoff_factor`；连续 `growth_interval` 轮无 inf/NaN 乘 `growth_factor`。默认 `init_scale=2^16`、growth 2.0、backoff 0.5、growth_interval 2000。`_per_optimizer_states[id(opt)]["found_inf_per_device"]` 是**固定实现的内部状态**，不是公开 API：FSDP 官方测试在 unscale 之后、update 之前断言它（该测试限 CUDA/FSDP2、要求 ≥4 GPU、`skipIfRocm`——是断言设计而非三平台接口或运行通过证明）；自建观测须绑定版本与时点（update 后该状态会被重置）。使用纪律沿用 [AMP Examples](https://docs.pytorch.org/docs/2.6/notes/amp_examples.html)：`unscale_` 后再 clip；梯度累加期间保持 scaled，`update()` 只在有效 batch 边界调用——一次累加尝试不必对应一次更新，计步时把**尝试的 batch 数**与**实际成功更新数**分列。

**框架级实现的独立性**：Megatron core_v0.19.2 有自己的 `ConstantGradScaler`/`DynamicGradScaler`，参数面含 `min_scale` 下界与 `hysteresis`（与 PyTorch 参数面不同）。DynamicGradScaler 的完整状态机（固定源码静态推演，未运行）：初始 `_growth_tracker=0`、`_hysteresis_tracker=hysteresis`；**非有限步**——growth tracker 清零、hysteresis tracker 减一，减到 ≤0 时 scale 乘 backoff（受 min_scale 截断）且**退避不重置计数**（后续非有限步继续退避）；**finite 步**——growth tracker 加一，未达到 growth_interval 时 hysteresis tracker **不复位**；**只有完整连续 growth_interval 个 finite 步**才同时复位两个 tracker（growth→0、hysteresis→初值）并乘 growth_factor——这是唯一的正常增长/复位分支。三类静态序列示例（初始 scale=16、hysteresis=2、growth_interval=3、growth 2、backoff 0.5、min_scale=1；源码推演非运行结果）：`真,假,真`→hys 依次 1,1,0、scale 16,16,8（中间 finite 步不复位）；`真,真,真`→hys 1,0,−1、scale 16,8,4（退避不复位）；`真,真,假,假,假,真`→两步后 scale=8/hys=0，第三个连续 finite 步完成增长窗口后 scale=16、两 tracker 复位，紧接的非有限步只把 hys 减到 1、scale 保持 16。fp16 训练经 `Float16OptimizerWithFloat16Params` 维护 **FP32 master 权重**（fp16 参数＋fp32 优化器状态的组合；该 master 权重承诺限此路径，不外推到所有 autocast/优化器组合）；MindSpeed-LLM v2.2.0 预训练脚本以 `--initial-loss-scale 65536` 显式给初值。三套实现不共用代码，语义以各自源码为准。

**平台边界**：`set_float32_matmul_precision` 只改内部计算精度、不改输出 dtype，当前只影响 CUDA（[文档](https://docs.pytorch.org/docs/2.6/generated/torch.set_float32_matmul_precision.html)）；ROCm 兼容文档在其 **PyTorch 2.7/2.8＋ROCm 7.0/7.1** 的已知问题节内列出 `torch.backends.cuda.matmul.allow_fp16_reduced_precision_reduction` 与 `allow_bf16_reduced_precision_reduction` 不支持（[该节](https://rocm.docs.amd.com/en/docs-7.1.1/compatibility/ml-compatibility/pytorch-compatibility.html)）——该版本组合与本页 PyTorch 2.6 机制样板**分立**，其他 PyTorch/ROCm 组合的支持情况 unknown（既不推断已支持，也不扩大成"AMD 不支持 AMP/BF16"）。算子 fallback、图/融合路径与精度支持冲突的组合矩阵未逐项建立——**遇到冲突组合保持未知，不用"大概兼容"替代验证**。

## 需要的证据

| 证据 | 采集范围或定位 | 用途 | 缺失时如何处理 |
|---|---|---|---|
| autocast 配置与算子归属 | 使用的 device_type/dtype、关键算子在实际路径的执行 dtype（dump 或 profiler） | 确认"以为在 BF16"与"实际在 FP16/FP32"是否一致 | 无 dump 则先固定单算子复现，不推进整训对照 |
| loss scale 分项记录 | 三条分列：scale 值序列、每轮 inf/NaN 判定（found_inf，版本绑定的内部插桩或应用侧重算）、实际参数更新数/跳步数 | 把"scale 变化""非有限梯度""真实更新停滞"分开归因；scale 形状不能单独判定空转（见机制速览） | 无分项记录则先加观测，不做盲调 |
| loss/梯度/权重的分项记录 | loss 曲线、梯度范数、权重更新量（unscale 后）分别记录 | 把"误差""NaN/Inf""更新异常"分开归因 | 混合记录不用于判据 |
| 首差异位置 | 沿用精度差异指南的首差异定位 | 把差异锚定到算子/步骤 | 无法定位则保留未知，不猜 |
| 有限窗口结果 | 固定步数窗口的 loss/指标＋固定验证集任务质量 | 收敛与质量判据的输入 | 无验证集则只报数值行为，不宣称质量可接受 |
| 平台内重复基线 | 同配置重复 N 次的同一指标 | 估计噪声/不确定性（判据见完成判据：噪声与任务阈值分列） | 不做跨配置比较 |

## 步骤与判断分支

| 步骤 | 检查或动作 | 运行影响 | 预期证据与解释 | 下一步 |
|---|---|---|---|---|
| 1 | 固定输入/模型/优化器/数据进度（同 checkpoint、同 batch），平台内重复运行 N 次 | 只读基线 | 得到该平台的重复性噪声估计；NaN/Inf 是否可复现 | 可复现→步骤 2；不可复现→按非确定性问题处理（查随机性与并行非确定，见 06.2/08.6） |
| 2 | 核对 autocast 实际生效面 | 低成本检查 | 各关键算子执行 dtype 与配置一致；发现 dtype 偏差→先定位来源（配置错误 / 上游包装器实现 / 支持条件），再在授权范围内选择修订或替代路径——改配置不能修复上游实现级问题（案例 #200537 即实现级） | 一致→步骤 3 |
| 3 | 单因素精度对照：只改一个精度变量（FP16↔BF16、autocast 开↔关、scale 初值），**每配置独立重复 R 次**（从同一冻结状态恢复） | 每配置 R 个完整窗口 | 每配置得分布（不只是单窗口）；loss 曲线差与首差异位置；首差异在可解释算子上且不传播→记录为已知偏差 | 所有配置（含无显著差异组）都进入步骤 5 质量验收 |
| 4 | loss scale 机制观察：scale、found_inf、实际更新数三条分列 | 随训练采集 | 按实现解释形态：常数 scale 无退避；动态 scale 初期退避后稳定是常见形态，但 scale 平台期≠无跳步、到下界≠必然空转（见机制速览）；持续非有限梯度→查 inf 源 | 机制异常→先修机制（数据/算子/初值）再谈收敛 |
| 5 | 有限训练窗口＋固定验证集质量对照（**所有配置的必经步骤**） | 每配置 R 窗口 | 按预注册判据判"一致/可解释差异/不可接受差异"；计步口径同时报告尝试步与实际成功更新数 | 通过→记录边界收尾；不通过→回到步骤 3 收窄单因素 |

**案例锚（静默 dtype 适配错误）**：PyTorch issue [#200537](https://github.com/pytorch/pytorch/issues/200537)（2026-10-10 报告，报告者环境 nightly 2.16.0.dev20261010+cu130、RTX 3090、cuDNN 9.26，自述 2.11.0/2.13.0 线同样复现）：`torch.autocast("cuda", dtype=bfloat16)` 下 cuDNN 路径的 `nn.LSTM/GRU` 输出/h/c 为 FP16——autocast 的 RNN 包装器硬编码 `at::kHalf`（fp16-only 时代遗留，属**上游实现级**问题而非用户配置错误），非 cuDNN 路径与 Cell 层均正确 BF16，直接 `.to(bfloat16)` 调 cuDNN 也正确；报告者用三组 dtype 对照定位。修复 commit cbffccce 改用 `get_autocast_dtype`，并设计 test/test_cuda.py 回归（断言 dtype、同路径参考输出与 backward 梯度；测试限定 BF16 硬件、cuDNN≥9.13、跳过 ROCm；2026-10-14 落地 main，PR #200697 为非标准合并路径）。三个事实层分开：dtype 现象与定位为报告者自述，修复与测试设计为上游实现，本库未复现；修复进入哪个 release、ROCm 侧 miopen_rnn 的对应问题、以及该类偏差对整训收敛的影响均 unknown（案例链未提供训练窗口或质量曲线）。可迁移经验：**精度对照的第一步是核对"配置声明"与"实际执行 dtype"一致**——静默偏差不报错，dtype 检查本身即可观察，不必等收敛异常才发现。

## 停止条件与恢复安排

- 出现不可复现的 NaN/Inf 且无法定位到算子级：停止对照，转入[静默错误与计算完整性判定](../08-reliability/silent-errors-and-integrity.md)的分层判定；不把硬件问题当精度调参。
- 对照差异超出预注册容差且首差异不可解释：停止，记录差异形态；不通过放宽容差"让它通过"。
- 非有限梯度/跳步达到预注册阈值：停止更新，检查数据与算子。触发条件按**预注册的非有限值持续次数、跳步率或有效更新停滞**定义，其中**跳步率按 optimizer 分列且分子分母预注册**：分子＝该窗口"确认因非有限值被抑制"的次数，分母＝该 optimizer 在**有效 batch 边界的 step 尝试数**（不是 micro-step、不是成功更新数、也不是只保留可分类事件的子集；多 optimizer 各自计算，不共用全局分母）。当尝试数≠确认抑制＋确认未抑制时，未确认事件**记账保留**：报告为有依据的上下界（如确认 1/10 抑制＋1 次未确认 → 比例区间 [1/10, 2/10]）或保守 unknown，不静默丢弃、不填作成功或跳步；分母为零（无尝试）时该窗口不产出比率。把"scale 触及下界即停"作为保守策略时，明确它是本库选择而非实现必然空转——`min_scale` 只是下界，之后梯度恢复 finite 仍可正常更新。
- 噪声/不确定性大到无法支撑任务阈值判定：补重复/样本或保持 unknown 收尾；不以提高容差的方式"解决"。
- 变更恢复：精度配置全部参数化记录（autocast 域与 dtype、scale 参数、matmul precision 档位、scaler 状态的新建/恢复范围），回退=恢复记录值＋从对照前 checkpoint 重启窗口；实验变量（如 scale 初值）单独声明。

## 完成判据

预先固定（进入对照前写下）：

1. **容差（两类分列）**：任务质量允许退化阈值（有任务依据，不随噪声放宽）与数值行为的统计分辨阈值。后者须与平台内重复的不确定性（步骤 1 的 N 次重复估计）相称——当不确定性大到盖过任务阈值时，结论只能是补采或 unknown，不是放宽阈值；不要求跨平台 bitwise 相同（浮点顺序差异是常态，见 PyTorch 数值文档）。
2. **重复与样本量（可执行的判读契约）**：每配置独立重复次数 R、每次从同一冻结状态恢复的范围、固定随机种子；**窗口对齐轴预先选定**（effective-batch 尝试数、样本/token 数、成功更新数三选一并声明换算——溢出跳步时 scheduler 与数据游标是否随尝试推进也要预注册并记录实际推进量，跳步造成的推进差异作为精度策略的自然后果报告，不事后按不同轴截取）；同时记录尝试步、抑制数、进入更新分支数、已消费样本/token 与 scheduler 推进量。**R 次结果的汇总量与不确定性表示、通过/失败/unknown 规则**预注册（如按指标的区间/极差与预注册阈值的关系判定；不虚构通用 R 值与统计方法）；固定验证集样本量写明。scaler 状态在窗口边界的新建/恢复范围固定，实验变量（如 scale 初值）单独声明。
3. **判读规则**：loss 曲线差、首差异算子、质量指标差各自单独判；"一致"要求全部在容差内；"可解释差异"要求首差异定位＋不传播到质量；其余为"不可接受"。固定验证集质量检查是所有"通过/可接受"结论的必经步骤，证据缺失只能报 unknown。
4. **停止条件**：如上节。

完成后能回答：当前配置下精度机制的观测形态是什么（scale/非有限/实际更新三条分列）、与对照的差异是否可解释、有限窗口内收敛与任务质量是否在容差内、哪些组合仍属未知（未测的算子 fallback/图路径/平台组合如实列出）。

## 来源与验证记录

- PyTorch v2.6.0：[AMP 文档](https://docs.pytorch.org/docs/2.6/amp.html)、[AMP Examples](https://docs.pytorch.org/docs/2.6/notes/amp_examples.html)、[GradScaler 源码](https://github.com/pytorch/pytorch/blob/v2.6.0/torch/amp/grad_scaler.py)、[FSDP GradScaler 测试](https://github.com/pytorch/pytorch/blob/v2.6.0/test/distributed/_composable/fsdp/test_fully_shard_grad_scaler.py)、[autocast 测试](https://github.com/pytorch/pytorch/blob/v2.6.0/test/test_autocast.py)。
- Megatron core_v0.19.2：[grad_scaler.py](https://github.com/NVIDIA/Megatron-LM/blob/core_v0.19.2/megatron/core/optimizer/grad_scaler.py)、[optimizer.py](https://github.com/NVIDIA/Megatron-LM/blob/core_v0.19.2/megatron/core/optimizer/optimizer.py)。
- TorchNPU 7.2.0 autocast 与算子归属、MindSpeed-LLM v2.2.0 脚本、ROCm docs-7.1.1 兼容页、案例 [#200537](https://github.com/pytorch/pytorch/issues/200537)：见来源登记。
- 当前验证范围：仅来源核对（源码/测试/文档/案例链，含审阅轮对 GradScaler 时序、Megatron hysteresis 状态机、ROCm 已知问题版本限定的重核），未在真实 GPU/NPU 环境执行任何步骤。
- 待确认：GradScaler 跨 rank 归约实现（ShardedGradScaler 的 process group 归约限其自身路径）、案例 ROCm 侧修复与所属 release tag、NPU 侧收敛窗口官方对照数据、fallback/图路径精度冲突矩阵（见来源记录 unknown 清单）。
