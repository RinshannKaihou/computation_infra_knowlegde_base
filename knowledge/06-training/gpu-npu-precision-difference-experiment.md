---
id: training.gpu-npu-precision-difference-experiment
title: GPU 到 NPU 的精度差异验证实验设计
type: experiment
domain: training
status: draft
platforms: [ascend, nvidia]
source_refs:
  - src.ascend.msprobe-training-guide-2026-09-30
  - src.pytorch.numerical-verification-2.6
  - src.pytorch.parallel-training-state-2.6
updated_at: "2026-09-30"
summary: 通过平台内重复、逐字节固定输入与状态、首差异定位及下游影响对照，区分 GPU/NPU 数值差异的来源和可接受范围。
related_ids:
  - training.gpu-npu-precision-difference-triage
  - training.gpu-npu-precision-difference-source-case
  - training.parallelism-and-state
  - reliability.evidence-and-hypotheses
applicability:
  environment_refs: []
  notes: "适用于已能分别运行 NVIDIA GPU 与 Ascend NPU PyTorch 训练最小步骤、且能合法保存同一模型状态和输入字节的受控环境；具体硬件、软件栈、模型、数据、并行布局和任务容差尚未确定。"
verification:
  status: not_verified
  evidence_refs: []
  notes: "仅完成实验设计；未安装或运行 msprobe，未执行 GPU/NPU 训练、dump、单算子、故障注入或硬件测试，没有测量结果。"
---

# GPU 到 NPU 的精度差异验证实验设计

> 本页定义可复核的实验，不授权在共享或生产环境执行。当前没有实际实验结果。

## 问题与假设

研究问题是：当同一训练任务从 NVIDIA GPU 迁移到 Ascend NPU 后出现 loss、gradient、收敛或质量差异，差异首先出现在哪里，是否超过目标任务预先认可的容差，以及它是否会传播到训练状态或最终质量。

实验同时检验以下可区分的假设：

| 编号 | 假设 | 可证伪或支持的关键观察 |
| --- | --- | --- |
| E1 | 两侧模型、输入、权重、训练位置或数值配置并不相同 | key/shape/dtype/layout、输入或权重字节、step、样本/token、并行映射任一不一致，即支持“比较对象未对齐”；全部对齐后不能再用此假设解释首差异 |
| E2 | 差异主要来自某个平台内部的非确定性 | 同平台重复间的波动已覆盖跨平台差异，或首差异位置和方向在同平台重复中不稳定；单次运行不能支持本假设 |
| E3 | 差异属于有限精度或等价实现的预期范围 | 两侧均 finite，差异落在预注册、与 dtype/算子/任务相符的容差内，且没有越过梯度、更新或质量判据 |
| E4 | 某个算子、融合、编译或低精度实现形成稳定首差异 | 在输入仍相同的条件下，首差异稳定出现在同一节点；只改变一个实现条件后，位置或幅度按预测变化 |
| E5 | 多卡通信或并行更新引入差异 | 单设备对齐，而多设备的首差异稳定出现在 reduce、rank-local 状态或 optimizer update，且 rank 证据能匹配同一 collective/更新 |
| E6 | 个别设备存在异常 | 数值异常与明确物理实体稳定关联，并有独立设备错误或换位对照；只有跨平台差异不能支持硬件故障 |

[PyTorch 2.6 数值文档](https://docs.pytorch.org/docs/2.6/notes/numerical_accuracy.html)不保证不同平台即使输入逐位相同也得到逐位相同结果。本实验不以 bitwise identical 作为默认通过条件，也不把相同 seed 当作跨设备相同随机张量的保证。

## 环境与输入

执行前为 GPU、NPU 分别建立环境记录，且不把某个平台的配置名直接映射到另一个平台：

- 硬件型号/数量/设备实体、拓扑，以及 host OS/kernel；
- GPU driver、CUDA、cuDNN、NCCL 与 NPU driver/firmware、CANN、HCCL 的实际版本或制品身份；
- Python、PyTorch、torch_npu、训练框架、编译/融合组件、容器或包 digest；
- 模型代码/图、配置、参数与 buffer 的 key、shape、dtype、layout 和逐字节来源；
- 输入、label、mask、token、预处理结果与样本顺序的字节或受控摘要；
- optimizer、scheduler、loss scale、梯度累积、clip、zero-grad 和训练 step/micro-step；
- autocast、低精度、TF32 或平台等效模式、图/编译模式、融合和确定性设置；
- DP/TP/PP/EP/CP 维度、world size、rank/设备映射、数据分片和规约实现；
- 计划观察的 tensor/API、指标公式、参考、单位、容差和下游任务判据。

同一权重和输入先在受控位置序列化，再核对两侧加载后的 key、shape、dtype、layout 与内容摘要。摘要只作为身份核对手段；敏感数据不进入知识库或公共附件。若两侧只能各自按 seed 生成随机输入，则该运行不能声称比较了相同输入。

重复次数、测量步数和容差在看到跨平台结果前登记。数值规模、目标 dtype、参考误差与业务风险不同，阈值也会不同。固定 [msprobe 比对文档](https://github.com/Ascend/msprobe/blob/7783f6b2d0cbae0e2f6200b05e604a09d7820c50/docs/zh/user_guide/accuracy_compare/pytorch_accuracy_compare_instruct.md)中的 Loss 1%、Cosine 0.99、MaxAbsErr 0.001 等工具规则不作为本实验的默认验收线。

## 实验设计

每个运行使用唯一 run id，记录预注册配置和偏差。先做未插桩基线，再做观测运行；开启 hook、同步、dump、禁用融合或改变编译路径的运行不能与基线混为同一处理组。

### A. 平台内重复基线

1. 在 GPU 上以同一序列化状态和输入独立重复预注册次数，记录 forward、loss、backward、optimizer update 的有限性和选定统计量。
2. 在 NPU 上做同样的独立重复。
3. 分别估计两个平台自身的波动范围，并记录首个不重复的位置。

若任一平台内部已经不稳定，先调查 RNG、非确定实现、并发和未固定状态。此时单次 GPU/NPU 差值不能估计平台效应。

### B. 最小跨平台对照

加载同一模型/optimizer 起点和同一输入字节，只运行足以覆盖一次完整 forward、loss、backward 与 optimizer update 的最小步骤。先比较结构、finite 状态和粗粒度统计，再比较实际预注册指标。

从输入到 update 依次保存少量阶段边界观测。若 key、shape、dtype、layout、权重/输入内容或训练位置不一致，停止数值归因并记录为 E1；不继续产生大规模 dump 来掩盖更早的实验设计错误。

### C. 从模块到 API 的首差异定位

在 B 的输入与起点不变时，先按模块/阶段采集统计量，只在疑似边界附近扩大到 API 或 tensor。核对名称、调用次数、forward/backward、输入输出索引和 tensor 数，再把两侧节点配对。

误差累积后，下游同名 API 的输入可能已经不同。[固定 msprobe 文档](https://github.com/Ascend/msprobe/blob/7783f6b2d0cbae0e2f6200b05e604a09d7820c50/docs/zh/best_practices/train_debug_guide.md)支持从首 step、模块到单算子的缩小过程；本实验只把“输入仍可比的首个稳定分叉”作为候选根因位置。自研 API 没有对端或调用次数不同的节点标记为不可直接比较。

### D. 候选节点单变量对照

对 C 找到的候选节点固定同一输入、shape、dtype、layout 和语义，每次只改变一个实现条件。需要第三参考时，只有在操作、转换和误差定义明确的前提下使用 CPU/float64 或独立实现；它们是条件参考，不是绝对真值。

若要检验融合、编译、规约或低精度路径，把原路径与一个替代路径作为成对运行，并保留恢复方法。多个开关同时改变只能说明组合条件相关，不能定位单一原因。

### E. 传播与并行对照

从候选首差异向后跟踪到 gradient、collective 前后、optimizer state/update、后续 loss 与任务质量，只覆盖预注册的有限步数。多卡假设用相同起点的单设备对照、rank 级进展和各并行域映射来区分；不能把多卡 loss 差异直接写成通信库错误。

任务质量对照只在数据切分、样本/token consumed、optimizer step 和评测输入一致时解释。局部算子差异若没有越过预注册传播或质量判据，不外推为整次训练失败。

### F. 观测干扰对照

对必要的定位阶段至少保留：

- 原始未插桩运行；
- 最小统计采集运行；
- 如确有需要，单独的同步或 tensor dump 运行。

记录插桩造成的峰值内存、I/O、时延、同步和实现路径变化。问题只在插桩关闭时出现，支持“观测或时序相关”的进一步调查，但不能单独证明内存踩踏或唯一根因。

## 前置条件与运行影响

实验只在已授权、与生产流量隔离的专用 GPU/NPU 资源上进行。运行前确定设备数量、主机 CPU/内存、共享文件系统或本地盘容量、网络/collective 范围、最长时长和责任人。默认不做压力测试、故障注入、降频、重启、链路切换或生产配置修改。

tensor dump 可能显著增加显存/内存、磁盘、I/O、同步和训练时间，也可能包含模型、输入或业务数据。采集前限定节点、step、tensor、保留期、访问权限和删除路径；磁盘/内存预计越界、数据范围未授权或脱敏无法确认时不启动。

出现下列任一情况就停止当前运行，保存最小证据并恢复：

- `NaN/Inf`、runtime/设备/collective 错误或数据校验失败；
- 输入/权重/step 身份无法证明相同，或发现意外数据/代码变更；
- 显存、内存、磁盘、I/O、网络、时长达到预注册上限；
- 插桩触及未授权数据或运行越出隔离的设备/rank/网络范围；
- 需要改变共享环境、生产任务、固件/驱动或扩大主动测试。

恢复时撤销 hook、dump、同步、编译/融合覆盖和临时环境变量，核对设备与存储资源释放，并以未插桩最小检查确认回到原始实验路径。关闭某项特性后现象消失不自动构成修复。

## 执行与记录方法

1. 冻结实验计划、环境身份、输入/状态身份、重复次数、观测点、指标、容差、资源预算和停止条件。
2. 分别完成 A 的 GPU/GPU 与 NPU/NPU 重复，先判断平台内基线是否可解释。
3. 只有结构、输入和状态对齐后才执行 B；从粗粒度观测逐步进入 C，不一次性扩大 dump。
4. 对稳定候选执行 D 的单变量对照，必要时执行 E 的传播/并行对照和 F 的观测干扰对照。
5. 为每次运行保存配置、run id、起止时间及时区、输入/状态摘要、rank/设备映射、指标与单位、日志/附件受控位置、退出状态和计划偏差。
6. 按停止或完成判据结束，恢复临时配置和资源；把支持、反证、未知分别记录。

本页不提供可直接运行的通用命令：目标工具安装、版本、采集路径、权限、数据治理和环境都未确定，实验设计也不构成执行授权。

## 通过、失败与无法判断的判据

| 结论 | 必要条件 |
| --- | --- |
| 支持“差异在当前任务可接受范围内” | 两侧比较对象和训练位置已对齐；各自平台内重复已量化；结果 finite；跨平台差异落在预注册且有依据的逐项容差内；有限传播和下游判据均未失败 |
| 支持具体实现/算子/并行根因 | 在输入仍相同处出现稳定首差异；单变量对照按假设改变结果；重复运行和传播链一致；更早的结构/输入/状态不一致已排除 |
| 判定实验失败 | 预注册的数值、finite、传播或任务质量判据被稳定越过，但“失败”只描述目标组合和实验范围，不等同硬件故障 |
| 无法判断 | 环境/输入/状态/调用映射未对齐，平台内不稳定且样本不足，参考或容差没有依据，观测改变路径，资源上限提前触发，或结果相互矛盾 |

工具运行成功、某一个指标显示 Pass、一次 loss 接近、相同 seed、关闭融合后能运行，均不单独构成通过。设备异常还需要实体关联和独立硬件证据；本实验不以数值偏差替代设备健康检测。

## 实际结果与证据

尚未执行。没有 GPU/NPU 训练、平台内重复、跨平台测量、dump、单算子、任务质量或恢复结果；`verification.status` 保持 `not_verified`，`evidence_refs` 为空。

执行后只能填写真实的 run id、环境、观测、单位、统计方法、退出状态和证据位置。预期方向与来源文档不能写成实测结果。

## 局限、来源与后续问题

- [msprobe 固定训练精度定位指南](https://github.com/Ascend/msprobe/blob/7783f6b2d0cbae0e2f6200b05e604a09d7820c50/docs/zh/best_practices/train_debug_guide.md)与[精度比对文档](https://github.com/Ascend/msprobe/blob/7783f6b2d0cbae0e2f6200b05e604a09d7820c50/docs/zh/user_guide/accuracy_compare/pytorch_accuracy_compare_instruct.md)：用于固定/重复、缩小范围、首差异和匹配边界；未安装或运行。
- [PyTorch 2.6 Numerical accuracy](https://docs.pytorch.org/docs/2.6/notes/numerical_accuracy.html)：用于跨平台不保证 bitwise identical、非有限值和低精度路径边界。
- 局限：该设计不证明任何未记录 GPU/NPU 组合兼容，不给通用容差，也不能用 CPU/float64 取代任务参考或用数值实验诊断硬件健康。
- 待确认：目标模型/数据、完整软件栈、实际并行映射、可合法保存的数据范围、重复次数、指标与容差依据、第三参考的定义、资源预算和执行授权。
