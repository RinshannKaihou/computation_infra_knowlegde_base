---
id: path.task.migration-and-upgrade
title: 迁移与升级任务路径
type: path
domain: overview
status: draft
platforms:
- generic
source_refs:
- src.pytorch.numerical-verification-2.6
updated_at: '2026-10-22'
summary: 计划内变更的阅读路径：把迁移/升级显式分为软件环境、平台节点与模型语义三类变化，各自连接准入、执行与回退验证。
related_ids:
- software-stack.environment-installation-and-upgrade
- software-stack.compatibility-evidence
- cluster-platform.platform-change-and-rollback
- cluster-platform.node-drain-resource-reclamation
- hardware.node-acceptance-triage
- hardware.node-selection-and-lifecycle
- training.gpu-npu-precision-difference-triage
- training.mixed-precision-and-convergence
- software-stack.dtype-layout-and-precision-semantics
- inference.quantization-and-quality
- inference.output-quality-evaluation
- path.task.environment-installation
- path.task.fault-recovery
---

# 迁移与升级任务路径

本页把计划内的变更阅读串成一条路径。核心纪律：**先分类，再动手**——软件环境变化、平台节点变化与模型语义变化的证据链和回退路径完全不同，混在一起会导致无法归因。本页是导航草稿，不是变更工单；所链正文中的命令与样板均未在本库环境执行。`generic` 表示导航意图，不表示所有平台适用。

## 前置材料（先于变更）

1. **变更分类**（三类选一或逐项分列）：
   - ①软件环境：驱动/平台软件（CUDA、CANN、ROCm）/框架/通信库/引擎的安装、升级、替换；
   - ②平台节点：扩容新节点、更换节点、摘除节点、调度器/平台组件变更；
   - ③模型语义：精度策略（autocast/loss scale）、量化、dtype/layout、模型或 tokenizer 变更、跨平台迁移。
2. **当前环境档案**：版本组合与配套证据等级（沿用[环境安装路径](environment-installation.md)的产出作 B0 基线）。
3. **回退准备**：回退路径、保全安排与不可逆操作清单。
4. **结果判据**：变更后按什么口径判定"等价"或"可接受"（性能、数值、质量三层）。

## 阅读顺序（按变更分类分流，共同起点→分支→验证）

**共同起点**：

1. [三平台安装基线、迁移升级与回退验证](../../knowledge/02-software-stack/environment-installation-and-upgrade.md)：变更前准入门禁三项——**完整依赖交集**（硬件×OS×驱动×运行时×框架/引擎逐环节配套依据）、**有效 baseline**（已有环境的升级无可复跑的 B0 即停；首次安装例外为记录"安装前状态"与清理目标，不泛化到升级）、**恢复路径**（含制品保全与不可逆确认）——任一缺位停止实际变更；另迁移与升级变化矩阵、B0/N/R（baseline/变更/恢复）对照方法与回退/不可逆边界；结果契约字段冻结是独立的验收前提（未冻结不得记变更验收通过）。
2. [如何判断版本配套是否有依据](../../knowledge/02-software-stack/compatibility-evidence.md)：目标组合的配套证据按依据类型分别记录（发行包兼容矩阵/发行说明、源码分支/构建配置、项目测试声明/CI、本地运行验证），声明与本地验证两轴分开。

**①软件环境分支**：

3. [平台组件升级、发布、回退与回服](../../knowledge/05-cluster-platform/platform-change-and-rollback.md)：预检 → 波次与观测 → 失败停发与恢复 → 回服门槛的完整发布流程。
4. 变更后按安装正文的验证梯子重跑（安装身份、加载身份、结果契约分项判定，见第 1 步正文）。

**②平台节点分支**：

5. 新节点：[新节点与返修节点验收](../../knowledge/01-hardware/node-acceptance-triage.md)（配合[节点验收任务路径](node-acceptance.md)）。
6. 摘除/更换：[节点摘除、drain 与资源回收流程](../../knowledge/05-cluster-platform/node-drain-resource-reclamation.md)；平台故障期间见[控制面故障、平台恢复与账本核对](../../knowledge/05-cluster-platform/control-plane-recovery.md)。
7. 投产边界：[节点选型、隔离返修、长期管理与退役](../../knowledge/01-hardware/node-selection-and-lifecycle.md)的验收与投产前证据锚点。

**③模型语义分支**：

8. 跨平台迁移：[GPU 到 NPU 的精度差异诊断](../../knowledge/06-training/gpu-npu-precision-difference-triage.md)（先扣数值噪声，再谈差异）。
9. 精度策略：[混合精度、算子适配与收敛验证](../../knowledge/06-training/mixed-precision-and-convergence.md)（平台内重复性 → 单因素对照的流程）与[dtype、layout 与有限精度语义](../../knowledge/02-software-stack/dtype-layout-and-precision-semantics.md)。
10. 推理量化：[推理量化与输出质量验证](../../knowledge/07-inference/quantization-and-quality.md)与[推理输出质量的对照评估方法](../../knowledge/07-inference/output-quality-evaluation.md)（输入身份固定、指标预注册）。

**变更后验证（三分支共用）**：按 B0/N/R 对照记录变更前后结果；数值/质量对照的容差与判据预先固定。

## 目标产出

- 变更档案：变更分类、前后版本身份、配套证据等级、回退准备与结果判据。
- 变更前后对照记录：性能口径、数值口径（按分支选择）、质量口径各自的 B0/N/R 三行。
- 回退演练记录或回退路径确认（不可逆操作显式列出并单独授权）。

## 下一步判断

- 变更后性能不达预期：转[性能优化任务路径](performance-optimization.md)。
- 变更引入故障或恢复失败：转[故障恢复任务路径](fault-recovery.md)。
- 变更后数值/质量差异待归因：留在③分支的正文按分层归因。

## 完成/停止条件

- **完成**：变更档案完整、B0/N/R 对照齐备且结果判据满足、回退路径确认有效。
- **停止并升级**：准入门禁三项任一缺位即停——已有环境无可复跑 B0 的升级必须停止（首次安装例外不适用），依赖交集补不到依据即停止，回退路径未落定不执行变更；**变更/取证操作权限不足**（升级、drain、CRD 修改与回退均有授权边界，见[平台变更正文](../../knowledge/05-cluster-platform/platform-change-and-rollback.md)）→ 停止相应变更、保全现有证据并交由有权责任方；目标组合配套证据不足且无法降级 → 登记 unknown 并停，不用"社区有人这么配"代替证据；涉及不可逆/高危操作（见安装正文边界）→ 停下单独升级授权；结果契约字段未冻结 → 不得记变更验收通过；变更后结果不符且无法归因 → 转故障恢复路径，不反复盲试。

## 原始资料入口

- [PyTorch 数值精度与可复现性文档（2.6）](https://docs.pytorch.org/docs/2.6/notes/numerical_accuracy.html)：变更后数值对照与容差方法的官方参考（既有登记）。

以上为外部入口，引用前需核对版本与许可。

## 逐链检查（T00-07 交付记录，2026-10-22）

本页全部内链经 `make check` 通过，引用的目标正文均为已交付条目；未引用未交付正文。页尾外部入口为既有登记来源（`source_refs`），不承载本页导航主张。
