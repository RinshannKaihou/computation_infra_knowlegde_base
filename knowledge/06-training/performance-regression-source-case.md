---
id: training.performance-regression-source-case
title: 训练吞吐回归来源案例：Inductor 布局优化未计入 convolution_backward
type: case
domain: training
status: draft
platforms: [nvidia]
source_refs:
- src.pytorch.issue-189239-layout-regression
- src.pytorch.layout-opt-fix-chain
- src.pytorch.profiler-2.6
- src.pytorch.inductor-profiling-2.6
updated_at: "2026-10-20"
summary: "PyTorch 官方仓库的公开训练性能回归链（issue #189239，2026-07）：Inductor 的布局优化决策只统计前向卷积节点，AOTAutograd 拆分出的反向图静默失去 NHWC 优化，训练吞吐回归 20%+；修复 PR 经 MergeBot 以直接 commit 落地（不带回归测试），同期另有一条方向相反的 MPS 布局问题作为平台边界反例。"
related_ids:
- training.performance-analysis
- training.slow-rank-triage
- software-stack.operators-compilers-and-graphs
applicability:
  environment_refs: []
  notes: "案例环境为报告者/修复方自述（RTX 4080 SUPER、Intel Data Center GPU、torch.compile/Inductor 路径）；本库无该环境，结论不外推到其他模型/后端/版本。"
verification:
  status: source_checked
  evidence_refs:
  - src.pytorch.issue-189239-layout-regression
  - src.pytorch.layout-opt-fix-chain
  notes: "全链经 gh API 核对（issue 正文/评论、PR 元数据/创建与关闭时间/文件清单、commit diff、main 分支源码抽查，锚点见 docs/research/batch-25-t06-07-sources.md 与初审/复核报告）；本库未复现任何基准。"
---

# 训练吞吐回归来源案例：Inductor 布局优化未计入 convolution_backward

## 案例来源与问题

本页是对 pytorch/pytorch 公开仓库一条**训练吞吐回归链**的来源整理（[issue #189239](https://github.com/pytorch/pytorch/issues/189239)），非本库事件。选择它的原因：训练场景、报告者给出了完整命令与测量口径、根因链可从 issue 追到引入 commit 与落地 commit、且同期存在一条**方向相反**的 MPS 布局问题可作平台边界反例。

问题现象：`torch.compile`（Inductor 后端）下训练 mobilenetv3_large_100，**默认配置**（反向图布局优化被静默禁用）相对**强制启用布局优化**的同负载明显更慢，作者表述为 20%+ 性能回归，NVIDIA 消费卡与 Intel 数据中心 GPU 均可观察；**没有任何报错**。训练收敛与质量状态在该链中无记录（unknown——性能基准不附带收敛曲线）。

## 当时环境与近期变化

**报告者环境与测量口径**（issue 正文与 Versions 段，作者自述）：

| 项 | 值 |
|---|---|
| GPU | NVIDIA RTX 4080 SUPER（另在 Intel Data Center GPU 观察；型号未给出） |
| 软件 | `torch==2.14.0.dev20260706+cu130`、`triton==3.8.0+git43422b04`（Versions 段记录）；环境采集的 PyTorch/build CUDA 字段为 N/A |
| 工作负载 | 官方基准 `benchmarks/dynamo/timm_models.py --float16 --training --only mobilenetv3_large_100`，`batch_size=512`、`-n 10`、`--cold-start-latency`、`--disable-cudagraphs` |
| 并行 | 公开命令未配置分布式（单卡基准）；分布式场景未在链中测试 |
| 输入尺寸 | 未在正文中给出（unknown，不得自行补全） |

近期变化：2026-05-13 落地的 convolution_backward lowering 变更（commit `9c6b1aa07d56`，PR #178945）按 `V.graph.layout_opt` 决定是否把输入转成 NHWC；布局优化决策函数 `decide_layout_opt()` 只统计前向卷积节点。**两个组件的组合**构成回归条件——该表述是作者定位与修复方向的一致性推断，链中没有逐项隔离实验（工具链/库版本交互未被完整排除，见假设表）。

## 事件与证据时间线

| 时间 | 事件或观测 | 实体与范围 | 证据定位 |
|---|---|---|---|
| 2026-05-13 | commit `9c6b1aa07d56`「Triton backward convolution kernel (#178945)」落地 main（新增 convolution_backward 的 lowering 路径，按 `V.graph.layout_opt` 决定 NHWC 转换；实际执行 kernel 的后端选择与布局转换是不同层） | pytorch/pytorch main | commit search（PR #178945 API 为 closed/merged=false，内容经该 commit 落地） |
| 2026-05-21 | commit `140baa4eec85`（message 描述 dilation guard 问题；**所核 diff 仅 +4 行注释**，`guard_int_seq` 调用在此前代码已存在——message 与实际改动不符，真正 guard 引入点未确认） | main | commit diff 核对 |
| 2026-06-26 | 修复 PR **#188236** 创建（早于回归报告；"Include convolution_backward in decide_layout_opt conv node detection"） | Inductor 布局决策 | PR API |
| 2026-07-08 | issue #189239 报告回归：默认配置 `abs_latency=178.41ms`/eager speedup 1.448819；`TORCHINDUCTOR_FORCE_LAYOUT_OPT=1` 后 `141.91ms`/1.821338（speedup 均为**相对 eager** 的比值，非新旧版本对比）；labels 含 high priority、module: regression | mobilenetv3_large_100、fp16 training、batch 512 | issue 正文 CSV（作者自测） |
| 2026-07-28 | 修复 PR #191306 创建（标题含 "20% training regression"，携带 test_layout_optim.py 改动） | Inductor＋测试 | PR 文件清单 |
| 2026-08-07 | **同期独立问题**：issue #192551 报告 MPS 上布局优化**强制** channels_last 使 compiled training 变慢——作者环境为小型 conv 网络、batch 256@32×32 输入、bf16 autocast、Apple M5 Pro/macOS 27，报告 compiled 相对 **eager** 的训练耗时：nightly 约 4.5×、2.13.0 release wheel 约 9×，`TORCHINDUCTOR_LAYOUT_OPTIMIZATION=0` 后 compile 在其试过的 shape 上转为优势；数字来自作者机器。方向与本案（强制启用变快）相反 | Apple MPS 路径 | issue 正文与元数据 |
| 2026-08-17 | #192551 关闭（先于本案修复落地；关闭链指向 #193623，该修复链未核对） | MPS | issue 关闭事件 |
| 2026-08-28 | #191306 关闭：维护者评论"already a pr out for this"（因已有 PR 而非实现失败）；作者在 PR 内说明方案已重新设计为 forward 决策向 lazy backward 传播（最终 head 含 compile_fx.py 改动，与初始 backward 计数方案不同） | Inductor | PR 评论与文件清单 |
| 2026-09-23 | commit `82b424c7f91d`（"[inductor]: Include convolution_backward in decide_layout_opt conv node detection (#188236)"）落地 main——author 时间 05:31:00Z、MergeBot committer 时间 05:31:07Z；#188236 随之关闭（05:31:12Z，三个时间字段分列不混用）；落地文件仅 `torch/_inductor/graph.py`＋`kernel/conv.py`，**不含回归测试**；issue #189239 同日关闭 | main | commit API（author/committer 字段）、PR 关闭时间、issue 关闭事件 |

修复方在 PR #188236 的 Results 段另报告 Intel Data Center GPU 约 1.3× 提升，2026-09-02 作者评论补充 Intel Client GPU 与 RTX 4080 SUPER 上 1.3×+（PR 作者自报，与最终落地 SHA 的同条件复测绑定关系未确认）。

## 假设与调查

| 候选解释 | 支持证据 | 反对或缺失证据 | 检查与结论 |
|---|---|---|---|
| 布局优化被静默禁用（backward 图） | issue 定位：`decide_layout_opt()` 只统计 `aten.convolution.default`；AOTAutograd 拆图后 backward 图只含 `convolution_backward` → `conv_nodes` 为空 → `layout_opt=False` → lowering 保持 NCHW | 无反向证据 | 得到支持（在报告者负载上）——强制开关对照＋修复方向一致；**固定源码可确认的是节点计数与开关逻辑**，完整因果链（所有其他因素排除）未由该链建立 |
| CUDA/驱动或工具链版本变化 | — | 链中无完整工具链排除实验；布局开关对照不能排除工具链与布局的交互 | **未排除**（尚缺对照），不写成"已排除" |
| 新反向卷积 kernel 相关因素（kernel 选择/访存模式随布局变化） | 强制启用布局后时延恢复（作者数值）说明布局差异在该负载上占主导 | 开关对照未隔离 kernel 因素——布局变化可能改变 kernel 的访存、调用或选择，"变快"不构成对 kernel 因素的排除实验 | 未排除（保持候选，标注开关对照的证据范围） |
| 训练正确性受影响 | — | 链中无收敛/质量记录 | unknown |

## 处理与结果

处理动作（上游）：修复以 PR #188236 为主线——2026-06-26 创建、2026-09-23 经 MergeBot 以直接 commit `82b424c7` 落地（commit message 标注 "(#188236)"、"Pull Request resolved"），PR 的标准 merge 字段保持 closed/merged=false；另一提案 #191306 因已有 PR 而关闭，其测试改动与重新设计方案未随落地。

结果边界（如实记录）：

- **回归测试缺口**：落地 commit 文件清单不含测试；#191306 携带的 `test_layout_optim.py` 改动未随落地。不能写成"已带回归测试闭环"；也不据此断言整个仓库此后没有任何相关测试（未做全仓审计）。
- **修复版本归属 unknown**：修复进入哪个 release tag 未逐 tag 核对（证据止于 main 线与关闭时点）。
- **MPS 反例的定位**：#192551 是**同期独立的平台镜像问题**（方向相反：强制布局在 MPS 有害），先于本案修复存在并关闭（指向 #193623，未核对）；它说明布局决策在不同后端的最优方向可能相反——作为"修复/调优须按平台分别验证"的方法反例，**不是**本案修复引入的次生回归。
- **PR 作者性能报告**（Intel 1.3× 等）与落地 SHA 的关系未确认；issue 关闭、源码包含修改、性能报告、硬件复现是不同证据层次。
- **本库未复现**：全部数字（178.41/141.91ms、speedup 1.449/1.821、20%+、约 4×、1.3×）均为上游报告；时延下降约 20.5%、固定工作量吞吐提升约 25.7% 只是作者数值的算术换算，不是本库测量。

## 可复用经验与边界

可迁移的检查方法（与[性能分解](performance-analysis.md)流程衔接）：

1. **静默回归先查"决策开关"**：无报错的变慢常见于某优化被静默禁用或激活。本案的区分检查是环境变量强制开关（`TORCHINDUCTOR_FORCE_LAYOUT_OPT=1`）对照——单一开关恢复性能即是强定位证据；同时分清对照方向（默认慢/强制快）与基线（相对 eager 还是相对另一配置）。
2. **训练拆图改变组件可见性**：AOTAutograd 拆分 forward/backward 后，"按节点类型做决策"的逻辑（布局优化、kernel 选择）在反向图看到的节点集合不同；评估编译路径变更要检查**两侧图**的决策输入，并区分 lowering、布局转换、后端选择与实际执行 kernel 各层（与[算子/编译/图执行](../02-software-stack/operators-compilers-and-graphs.md)机制层互链）。
3. **回归引入点≠感知点，也≠修复提案点**：本案修复 PR（6-26）先于回归报告（7-8）出现——时间线要逐对象核对创建/落地/关闭三组时间，不能按叙事顺序脑补。
4. **同型问题可能在其他平台反向出现**：MPS 上强制布局有害；修复或调优的适用面按平台分别验证，修复方报告的其他平台数字不能替代目标平台验证。
5. **受害与源头**：本案例是单卡均匀变慢（非分布式不均），不适用慢 rank 定位；分布式场景下若所有 rank 均匀变慢，同样先怀疑全局决策（编译/库/环境），沿[慢 rank 指南](slow-rank-triage.md)的排除路径。
6. **commit message ≠ 实际 diff**：本案时间线中一个 commit 的 message 描述了修复而 diff 只有注释；引用 commit 作为证据时核对实际改动。

不可推广的条件：结论限定为报告者/修复方环境（NVIDIA 消费卡＋Intel 数据中心 GPU、torch.compile/Inductor、mobilenetv3_large_100、fp16、batch 512、禁用 CUDA graphs）；不构成对其他模型/后端（ROCm/Ascend/NPU 图路径）同类问题的判断，也不预设其他版本存在或不存在该回归。

## 来源与未解问题

- [issue #189239](https://github.com/pytorch/pytorch/issues/189239)（回归报告与根因定位）；修复主线 [PR #188236](https://github.com/pytorch/pytorch/pull/188236)（2026-06-26 创建，经 MergeBot 对应落地 commit `82b424c7f91d`，2026-09-23）；另一提案 [PR #191306](https://github.com/pytorch/pytorch/pull/191306)（因已有 PR 关闭，测试与 redesign 未落地）；引入侧 PR [#178945](https://github.com/pytorch/pytorch/pull/178945)（commit `9c6b1aa07d56`）；注释型 commit `140baa4eec85`；同期 MPS 反例 [issue #192551](https://github.com/pytorch/pytorch/issues/192551)（关闭指向 #193623，未核对）。全链经 gh API 观察（2026-10-20，初审与修订轮两遍核对）。
- 本地复现状态：未开展。
- 待确认：修复所属 release tag；#192551/#193623 修复链；Intel GPU 具体型号与输入尺寸；分布式场景的表现；引入 PR 评审记录是否讨论过布局交互。备选案例淘汰记录（Megatron #678 无修复闭环等）见[来源记录](../../docs/research/batch-25-t06-07-sources.md)。
