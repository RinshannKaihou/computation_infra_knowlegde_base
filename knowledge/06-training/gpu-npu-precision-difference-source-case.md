---
id: training.gpu-npu-precision-difference-source-case
title: "GPU 到 NPU 的精度差异来源案例：Ascend PyTorch #17"
type: case
domain: training
status: draft
platforms: [ascend, nvidia]
source_refs:
  - src.ascend.pytorch-issue-17
updated_at: "2026-09-30"
summary: 整理一个 V100 与 Ascend 910B 的 SFT loss 轨迹差异报告，保留 GPU 环境和控制实验缺口，不把 DDP stride warning 写成根因。
related_ids:
  - training.gpu-npu-precision-difference-triage
  - training.gpu-npu-precision-difference-experiment
  - training.parallelism-and-state
  - reliability.evidence-and-hypotheses
applicability:
  environment_refs: []
  notes: "外部案例限定于报告者所述 V100/Ascend 910B SFT 与 CANN 7.0.RC1/torch_npu 2.1.0rc1 环境；GPU 软件栈、模型、数据、数值模式和并行细节不完整，不能外推。"
verification:
  status: source_checked
  evidence_refs:
    - src.ascend.pytorch-issue-17
  notes: "已核对 Issue 正文、当前 Open 状态、环境、loss 陈述、DDP warning、代码怀疑点及 connector 返回的一条评论；未取得训练制品或本地复现，也没有根因、修复或复验。"
---

# GPU 到 NPU 的精度差异来源案例：Ascend PyTorch #17

## 案例来源与问题

本案例整理公开的 [Ascend/pytorch #17](https://github.com/Ascend/pytorch/issues/17)。报告者称使用 PEFT、TRL 和 `accelerate launch` 进行大模型 supervised fine-tuning 时，V100 上的 loss 从约 1.3 在半个 epoch 内降到 0.3，而 Ascend 910B 上训练 5 epochs 后仍约 0.8。

报告者说两侧训练脚本和参数除 `cuda`/`npu` 部分外相同，并把 DDP gradient/bucket stride warning 及 torch/torch_npu reducer 实现差异列为怀疑点。案例要回答的是这些材料能支持哪些调查方向，而不是据此宣布 DDP reducer 导致数值错误。

这是外部未闭环 Issue。本库没有模型、数据、两侧日志、权重、输入或运行环境，也没有复现训练。

## 当时环境与近期变化

| 层次 | 来源给出的事实 | 缺失与限制 |
| --- | --- | --- |
| 比较硬件 | NVIDIA V100 与 Ascend 910B | 数量、拓扑、rank 映射、GPU/NPU 具体配置和健康状态未知 |
| NPU OS/软件 | Ubuntu 20.04；kernel `4.19.90-vhulk2211.3.0.h1543.eulerosv2r10.aarch64`；CANN 7.0.RC1；Python 3.9；torch 2.1.0；torch_npu 2.1.0rc1.post20231013 | 驱动/固件、容器、包 digest 和算子库未给全 |
| GPU 软件栈 | 未给出 | OS、driver、CUDA/cuDNN/NCCL、PyTorch build、dtype/TF32 等不能从 V100 推断 |
| 训练框架 | PEFT、TRL、Accelerate/分布式 | 精确版本、commit、DDP 配置、world size、bucket 参数和并行映射未知 |
| 模型与数据 | “large language models” SFT | 模型/权重、数据集、tokenization、sample/batch 顺序、epoch 定义未知 |
| 数值与随机性 | 未给出完整记录 | 输入/权重字节、seed/RNG、确定性、dtype/autocast、loss scale、梯度累积/clip 未知 |

因此“脚本和参数相同”不能证明两侧执行了同一数据顺序、同一随机张量、同一低精度路径或同一 collective/optimizer 更新。

## 事件与证据时间线

| 时间与时区 | 事件或观测 | 实体与范围 | 证据定位 |
| --- | --- | --- | --- |
| 2023-12-19 | Issue 打开，报告 V100 与 910B 的 SFT loss/收敛差异 | 两个平台的训练，运行日期和时区未给出 | [Issue Description](https://github.com/Ascend/pytorch/issues/17) |
| 报告中的 V100 运行 | loss 约从 1.3 降到 0.3，时间尺度为“前半个 epoch” | GPU 训练 | 报告者陈述；没有曲线附件、重复次数或原始数据 |
| 报告中的 910B 运行 | 5 epochs 后 loss 仍约 0.8 | NPU 训练 | 报告者陈述；两侧 epoch/sample/token 是否同口径未知 |
| 同一调查 | DDP warning：gradient stride 与 bucket view stride 不匹配；warning 明说不是 error，但可能影响性能 | NPU reducer 路径 | [Issue warning 与代码对比](https://github.com/Ascend/pytorch/issues/17) |
| 评论时间未由 connector 返回 | 评论者说明 NPU/GPU、私有格式及 bucketing/传输实现有差异，但称当前功能上没有问题；询问是否固定输入/随机种子/确定性并逐 step 比较 loss | 需要的控制实验 | [issuecomment-2029286848](https://github.com/Ascend/pytorch/issues/17#issuecomment-2029286848) |
| 2026-09-30 观察 | Issue 仍为 `Open`，页面无关联 branch/PR | Issue 状态 | [Issue Metadata](https://github.com/Ascend/pytorch/issues/17) |

GitHub 静态页面没有加载评论；本轮通过只读 GitHub connector 取得上述一条评论。connector 没有返回创建时间或 author association，因此本文只称“评论者”，不推断维护者身份。

## 假设与调查

| 候选解释 | 支持证据 | 反对或缺失证据 | 结论 |
| --- | --- | --- | --- |
| 两侧输入、权重、随机性或训练进度未真正对齐 | 报告只说脚本/参数近似相同；评论明确追问固定输入、seed、确定性和逐 step loss | 没有输入/权重摘要、RNG、sample/token 顺序和 step 对照 | **首要证据缺口** |
| DDP bucket stride 差异导致收敛问题 | NPU warning 和 reducer 代码差异与该路径相关 | warning 自述不是 error、可能影响性能；没有 gradient 值、单卡/多卡或代码单变量对照；评论称当前无已知功能问题 | **报告者怀疑，不能确认为数值根因** |
| 正常有限精度/平台实现差异逐步累积 | 跨平台浮点实现本可不同；长程 loss 差异与累积相容 | 没有平台内重复、首差异 step、逐层输出/梯度和任务容差 | **未量化** |
| GPU/NPU 软件或低精度配置不一致 | GPU 栈完全缺失，NPU 栈只部分给出 | 没有两侧 dtype、autocast、TF32/融合/算子版本 | **未排除** |
| NPU 硬件故障 | 收敛较差可能被误归因设备 | 没有设备错误、实体关联、换卡或健康证据 | **无支持证据** |

## 处理与结果

公开材料中没有显示报告者完成评论所要求的固定输入/随机性/确定性逐 step 对照，也没有首差异节点、梯度内容、单卡与多卡分离、修复 commit 或复验结果。

截至 2026-09-30：

- Issue 为 `Open`；
- DDP reducer/stride 只是报告者怀疑，不是已确认根因；
- 一条评论认为实现差异存在但当前没有已知功能问题，并要求补充控制实验；
- 没有恢复到预期收敛的公开动作或验证结果。

因此案例状态是“真实来源、症状与部分环境明确、根因和修复未闭环”。

## 可复用经验与边界

- “同脚本、同参数、同 seed”不等于同输入字节和同训练位置；先保存权重、输入、样本/token 和 step 身份。
- 先分别做 GPU/GPU 与 NPU/NPU 重复，再比较 GPU/NPU；否则无法区分平台内非确定性。
- DDP stride warning 明确描述性能风险时，不能把它改写成梯度数值错误。需要 gradient/bucket 内容和单变量对照。
- 比较 loss 曲线前统一 epoch、sample/token consumed、batch、梯度累积和 optimizer step 口径。
- Issue `Open` 也不证明报告仍可复现；当前状态、历史环境、根因证据和修复分别记录。

本案例的方法边界可迁移，V100/910B 和所列版本不能作为目标环境兼容或精度结论。

## 来源与未解问题

- [Ascend/pytorch #17](https://github.com/Ascend/pytorch/issues/17)：核对正文、环境、warning、代码怀疑点与状态。
- [公开评论](https://github.com/Ascend/pytorch/issues/17#issuecomment-2029286848)：核对其要求的固定输入/随机性/确定性逐 step 对照；未推断评论者身份。
- 本地复现状态：未开展；未运行训练、dump、梯度或硬件测试。
- 待确认：GPU 完整栈、模型/数据/权重/输入、随机性和低精度配置、并行与训练进度、平台内重复、首差异、任务容差、评论后续、根因和修复。
