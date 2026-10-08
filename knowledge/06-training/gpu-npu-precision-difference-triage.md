---
id: training.gpu-npu-precision-difference-triage
title: GPU 到 NPU 的精度差异诊断指南
type: procedure
domain: training
status: draft
platforms: [ascend, nvidia]
source_refs:
  - src.ascend.msprobe-training-guide-2026-09-30
  - src.pytorch.numerical-verification-2.6
  - src.pytorch.parallel-training-state-2.6
updated_at: "2026-09-30"
summary: 先证明 GPU/NPU 比较对象和训练位置相同，再从平台内重复性、首个数值分叉和下游影响逐层缩小精度差异。
related_ids:
  - training.parallelism-and-state
  - reliability.evidence-and-hypotheses
  - software-stack.ascend-documented-profile
  - software-stack.nvidia-documented-profile
applicability:
  environment_refs: []
  notes: "流程以固定 msprobe commit 的 PyTorch 训练定位文档和 PyTorch 2.6 数值边界为依据；目标 GPU/NPU、软件栈、模型、数据、并行布局和任务容差尚未建立环境档案。"
verification:
  status: source_checked
  evidence_refs:
    - src.ascend.msprobe-training-guide-2026-09-30
    - src.pytorch.numerical-verification-2.6
    - src.pytorch.parallel-training-state-2.6
  notes: "已核对 msprobe 固定训练精度定位/比对文档及 PyTorch 2.6 numerical accuracy/并行资料；未安装工具，未运行 GPU/NPU 训练、dump、单算子或硬件测试。"
---

# GPU 到 NPU 的精度差异诊断指南

## 目标与触发条件

本流程用于调查同一训练任务从 GPU 迁移到 NPU 后出现的 loss/gradient 差异、非有限值、收敛速度变化或下游质量下降。目标是确定两侧是否真的在比较同一个训练状态，找到**第一个可复核的数值分叉**，再验证它是否传播为训练或质量问题。

浮点计算不是跨平台 bitwise 契约。[PyTorch 2.6 数值文档](https://docs.pytorch.org/docs/2.6/notes/numerical_accuracy.html)明确说明，浮点运算顺序会改变结果，不同 release、commit 和 platform 即使输入逐位相同并控制随机性，也不保证逐位相同。因此“有差异”是症状；只有超过有依据的容差、出现非有限值，或能解释下游失败时，才构成需要处置的异常。

## 适用范围与前置条件

流程聚焦 PyTorch 训练的 NVIDIA GPU 与 Ascend NPU 对照。两侧的驱动、CUDA/CANN、框架、算子库和集合通信实现分别记录，不能把一个平台的变量、融合开关或确定性设置复制到另一个平台。

进入比较前固定：

- 模型代码/图、参数与 buffer 的稳定身份、shape、dtype、layout 和逐字节权重来源；
- 同一输入/label/mask/token 字节、样本顺序、padding、预处理与训练 step/micro-step；
- optimizer、scheduler、loss scale、梯度累积、clip、zero-grad 和更新边界；
- autocast/混合精度、TF32 或设备等效模式、融合/编译/图模式与规约实现；
- DP/TP/PP/EP/CP 维度、rank 映射、world size 和数据切分；
- 两侧完整软件/制品身份、硬件和拓扑；
- 比较指标、参考、`rtol/atol` 或任务判据及其来源。

相同 seed 不是相同输入的充分条件。固定 [msprobe 指南](https://github.com/Ascend/msprobe/blob/7783f6b2d0cbae0e2f6200b05e604a09d7820c50/docs/zh/best_practices/train_debug_guide.md#2312-%E9%A6%96step-loss%E5%B7%AE%E5%BC%82)还指出，不同硬件即使设置相同 seed，也可能生成不同随机张量。需要同一随机输入时，直接保存并核对张量字节及身份。

## 需要的证据

| 证据 | 范围 | 用途 | 缺失时的处理 |
| --- | --- | --- | --- |
| 环境与实现 | GPU/NPU 各自硬件、driver/runtime、PyTorch/torch_npu、库、容器/包 commit | 判断差异是否混入版本/实现变化 | 不把“同一 PyTorch 主版本”当完整配套 |
| 模型与状态 | 代码/图、参数/buffer、optimizer/scheduler/loss scale、step | 证明起点相同 | key/shape/dtype/layout 或内容不同，先停止数值归因 |
| 输入与数据进度 | 输入/label/mask/token 的字节/摘要、样本顺序、rank 分片 | 排除数据不一致 | 只有 seed/epoch 不足，保持 unknown |
| 平台内重复 | 每个平台至少按预注册次数独立重复的同一观测 | 区分自身非确定性与跨平台偏差 | 单次 GPU 对单次 NPU 不估计自然波动 |
| 分层观测 | forward 输出、loss、backward gradient、optimizer state/update | 找首差异和传播路径 | 后期输入已漂移时，不把后期同名 API 直接配对 |
| 非有限值/范围 | `NaN/Inf`、溢出、loss scale、最大/最小/范数 | 将数值失效与小偏差分开 | 非有限值先停止长训，保全第一现场 |
| API/模块匹配 | 名称、调用次数、forward/backward、输入输出索引和 tensor 数 | 防止工具错配 | 自研 API 无对端、调用次数不同或映射不明时标为不可比 |
| 容差与任务结果 | 指标公式、单位、参考、容差依据；收敛/评测判据 | 判断差异是否可接受 | 不采用工具默认标红值作为任务结论 |

dump 可能包含模型输入、权重或业务数据。采集前定义脱敏、访问、容量、保存期和删除责任；日志/张量不直接提交到知识正文。

## 步骤与判断分支

| 步骤 | 检查或动作 | 运行影响 | 解释与下一步 |
| --- | --- | --- | --- |
| 1 | 冻结两侧环境、模型、状态、输入、step、并行和数值配置 | 只读记录；必要时暂停继续训练以保留第一现场 | 任一身份不一致先修复实验设计，不进入算子归因 |
| 2 | 分别在 GPU、NPU 上重复同一最小步骤，先测平台内波动 | 占用训练资源；不启用新 dump | 单个平台自己不重复时，先调查随机源、非确定实现或并发 |
| 3 | 检查 key/shape/dtype/layout、输入字节、权重和 loss/gradient 的 finite 状态 | 低到中等观测开销 | 结构/输入不一致是更早分支；`NaN/Inf` 先回看溢出和第一异常 |
| 4 | 将问题缩到第一个出现差异的 step 和阶段：forward、loss、backward、reduce、optimizer update | 需要保存少量阶段性观测 | 第一步已分叉查输入/算子；多步后分叉查误差累积、更新和数据进度 |
| 5 | 从粗粒度模块到细粒度 API，核对两侧匹配关系，再找首差异节点 | dump 增加内存、I/O、同步和时延 | 后期输入已不同只说明传播；优先分析输入仍可比的首节点 |
| 6 | 对候选节点做单变量验证：同一输入、同一语义，保留 GPU/NPU 与条件明确的第三参考 | 可能改变实现/设备路径；需独立环境与回滚 | CPU/FP64 只能作为已定义参考；不自动是真值 |
| 7 | 比较候选差异是否传播到梯度、optimizer update、loss 和任务质量 | 可能需要短程训练；限定步数和资源 | 局部差异不传播时，不扩大为整机故障；传播时记录路径 |
| 8 | 复核观测干扰：未插桩、同步 dump、异步 dump/最小 hook 作为分开的运行 | 插桩本身可能改变时序、内存和融合 | 问题随观测消失只支持时序/实现依赖假设，不证明唯一根因 |
| 9 | 汇总支持、反证和未知，按预注册容差与任务判据下结论 | 无运行影响 | 满足完成判据结束，否则列最小补采项 |

固定 [msprobe 比对文档](https://github.com/Ascend/msprobe/blob/7783f6b2d0cbae0e2f6200b05e604a09d7820c50/docs/zh/user_guide/accuracy_compare/pytorch_accuracy_compare_instruct.md)支持整网、首差异和 API 映射思路，也提醒误差累积后同名 API 的输入可能已经不同。本文不收录通用 `msprobe compare` 命令：工具未安装，目标路径、采集模式、API 映射、版本和数据治理尚未确定。

## 假设分支

| 候选解释 | 支持证据 | 不足以支持 |
| --- | --- | --- |
| 输入/状态/训练位置不同 | 字节、key、step、样本/rank 对不上 | “脚本一样”或“seed 一样” |
| 平台内非确定性 | 同平台重复的首差异位置/方向变化 | 单次跨平台差异 |
| 正常有限精度/实现差异 | 结构一致、finite、差异在有依据容差内且不影响任务 | 工具显示某列不同就判硬件错 |
| 特定算子/融合/编译路径 | 同一输入的首差异稳定落在同一节点，单变量实现对照改变结果 | 同时关闭多项融合或改多版本 |
| 通信/并行更新差异 | 单卡对齐、多卡首差异出现在 reduce/update，rank 证据一致 | 多卡 loss 不同就判通信库错误 |
| 设备/硬件异常 | 同一物理实体出现独立错误，差异随设备映射迁移或固定 | 只凭数值偏差；主动压测未获授权 |

## 停止条件与恢复安排

出现 `NaN/Inf`、结果校验失败、设备/runtime 错误、输入或权重身份无法证明相同、插桩超出内存/磁盘/时长预算、采集触及未授权数据，或需要修改生产模型/融合/库版本时，停止继续训练和扩大采集。

若做过临时插桩或配置对照，记录原值、生效范围和 run id；恢复后撤销 hook/dump/同步/实现覆盖，确认原始未插桩路径与资源状态，再决定是否继续。关闭特性或改用 CPU 能使现象消失，不自动构成最终修复。

## 完成判据

本轮诊断在以下任一状态完成：

1. 找到结构、输入、状态或训练位置不一致，并能解释差异；
2. 找到输入仍相同的首差异节点，单变量对照和传播链支持具体实现/算子/并行假设；
3. 差异在预先定义且有任务依据的容差内，平台内波动与下游结果均支持“可接受”；
4. 证据不足，但已明确缺失的环境、输入/状态、重复样本、映射或容差依据，结论保持 `unknown`。

相同 seed、一次 loss 接近、工具退出成功、一个指标 Pass 或关闭某特性后运行成功，均不单独满足完成判据。

## 来源与验证记录

- [msprobe 固定训练精度定位指南](https://github.com/Ascend/msprobe/blob/7783f6b2d0cbae0e2f6200b05e604a09d7820c50/docs/zh/best_practices/train_debug_guide.md)与[精度比对文档](https://github.com/Ascend/msprobe/blob/7783f6b2d0cbae0e2f6200b05e604a09d7820c50/docs/zh/user_guide/accuracy_compare/pytorch_accuracy_compare_instruct.md)：核对 checklist、固定/重复、缩小、首差异、API 匹配和观测干扰。
- [PyTorch 2.6 Numerical accuracy](https://docs.pytorch.org/docs/2.6/notes/numerical_accuracy.html)：核对跨平台不保证 bitwise、非有限值和低精度路径边界。
- 当前验证范围：来源核对；没有目标环境、dump、训练或任务评测结果。
