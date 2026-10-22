---
id: path.task.fault-recovery
title: 故障恢复任务路径
type: path
domain: overview
status: draft
platforms:
- generic
source_refs:
- src.google.sre-effective-troubleshooting
updated_at: '2026-10-22'
summary: 非计划故障的处置与恢复阅读路径：先固定影响范围与状态责任，按范围分流到隔离、重试、训练续训与服务恢复；恢复验收同时检查正确性与持续进展。
related_ids:
- reliability.mitigation-and-recovery-principles
- reliability.reliability-metrics-and-recovery-loss
- reliability.postmortem-and-knowledge-update
- inference.release-and-recovery
- cluster-platform.control-plane-recovery
- cluster-platform.node-drain-resource-reclamation
- cluster-platform.platform-change-and-rollback
- data-storage.storage-client-backend-recovery
- data-storage.checkpoint-integrity-evidence
- training.checkpoint-state-recovery-triage
- training.checkpoint-state-consistency
- training.elastic-training-and-membership
- hardware.node-selection-and-lifecycle
- path.task.performance-optimization
- path.task.migration-and-upgrade
---

# 故障恢复任务路径

本页把非计划故障发生后的处置与恢复阅读串成一条路径。两条纪律贯穿全路径：**动手前先固定影响范围与状态责任**，**恢复验收同时检查正确性与持续进展**（"服务起来了 / 进程拉起来了"不等于恢复完成）。本页是导航草稿，不是应急手册；处置动作的执行依据用户已有授权与现场条件。`generic` 表示导航意图，不表示所有平台适用。

## 前置材料（先于处置）

按[隔离、重试预算、降级与恢复选择](../../knowledge/08-reliability/mitigation-and-recovery-principles.md)的"第一步：动手前固定六项"先写下——**目标维度、证据门槛、影响域（动作本身会中断谁，与故障已发生的影响范围分开判断）、状态前提、停止/回退条件、恢复判据**——缺任何一项的动作都是盲操作。本页另需补充材料：故障开始的证据时间线、近期变更清单、可用回退点（checkpoint/制品/上一版本）、各分支的状态责任方、证据保全安排、重试预算与授权边界（处置动作依既有授权与现场条件执行）。

## 阅读顺序（先方法，再按影响范围分流）

1. **处置方法**：[隔离、重试预算、降级与恢复选择](../../knowledge/08-reliability/mitigation-and-recovery-principles.md)——按目标维度选措施、重试预算与退避幂等、恢复选择（重算/回退/切换）；怀疑冗余/隔离失效时对照[相关故障案例](../../knowledge/08-reliability/correlated-failure-source-case.md)。
2. **按影响范围分流**（先判断范围再进分支）：
   - **单请求/输出异常**：[诊断中的证据、假设与结论](../../knowledge/08-reliability/evidence-and-hypotheses.md)；健康全绿但结果异常时[静默错误与计算完整性判定](../../knowledge/08-reliability/silent-errors-and-integrity.md)；输出质量侧[对照评估方法](../../knowledge/07-inference/output-quality-evaluation.md)。
   - **推理副本/服务**：[服务版本发布、副本故障与恢复验证](../../knowledge/07-inference/release-and-recovery.md)（副本故障证据与处置分支、基线→受控切换→恢复的验证设计、不承诺 exactly-once 的语义边界）；启动失败见[权重加载、引擎 ready 与启动失败诊断](../../knowledge/07-inference/model-loading-and-readiness.md)。
   - **单节点/单设备**：[节点摘除、drain 与资源回收流程](../../knowledge/05-cluster-platform/node-drain-resource-reclamation.md)；设备证据[设备健康证据与检测边界](../../knowledge/01-hardware/health-evidence.md)与[供电、散热与性能退化证据](../../knowledge/01-hardware/power-thermal-evidence.md)；隔离返修与再投产锚点见[节点选型与生命周期](../../knowledge/01-hardware/node-selection-and-lifecycle.md)。
   - **平台/控制面**：[控制面故障、平台恢复与账本核对](../../knowledge/05-cluster-platform/control-plane-recovery.md)（Kubernetes/Slurm 分支、恢复后账本核验）；平台组件回服门槛见[平台组件升级、发布、回退与回服](../../knowledge/05-cluster-platform/platform-change-and-rollback.md)。
   - **存储**：[存储客户端、后端异常与恢复验证](../../knowledge/04-data-storage/storage-client-backend-recovery.md)（先保留证据、保护恢复点）；字节/文件损坏的分层发现能力见[Checkpoint 完整性与校验证据](../../knowledge/04-data-storage/checkpoint-integrity-evidence.md)。
   - **训练状态**：[Checkpoint 恢复状态异常诊断](../../knowledge/06-training/checkpoint-state-recovery-triage.md) → [Checkpoint 恢复一致性](../../knowledge/06-training/checkpoint-state-consistency.md)（恢复后验证分层：身份/结构→逻辑进度→状态内容→同输入单步→持续窗口）；成员变更/缩容续训见[弹性训练与成员变更](../../knowledge/06-training/elastic-training-and-membership.md)（状态恢复是应用责任）。
3. **恢复验收与记账**：正确性与持续进展两条都要落——[可靠性统计、有效产出与恢复损失](../../knowledge/08-reliability/reliability-metrics-and-recovery-loss.md)（恢复损失六类量记账、事件表）。
4. **复盘**：[事故复盘、来源更新与知识维护](../../knowledge/08-reliability/postmortem-and-knowledge-update.md)（复盘字段、追溯链与复核触发）。

## 目标产出

- 处置记录：影响范围、处置六项（目标维度/证据门槛/影响域/状态前提/停止回退条件/恢复判据）、采取的措施与时间线、被排除与仍开放的候选原因。
- 恢复验证记录：正确性判据（按范围选择：单步对照/输出质量/账本核对）与持续进展判据（训练 step 推进 / goodput 恢复）各自的结果。
- 恢复损失记账：按六类量记入事件表，区分本次故障损失与恢复开销。

## 下一步判断

- 恢复后性能不达预期：转[性能优化任务路径](performance-optimization.md)。
- 故障根因指向需要变更（版本缺陷/容量不足）：转[迁移与升级任务路径](migration-and-upgrade.md)或[选型与容量任务路径](selection-and-capacity.md)。
- 需要平台/机型细节：进[平台路径](../platforms/nvidia.md)（[昇腾](../platforms/ascend.md)/[AMD](../platforms/amd.md)）与[训练排障](training-triage.md)/[推理排障](inference-triage.md)。

## 完成/停止条件

- **完成**：恢复验证双判据（正确性 + 持续进展）满足且经观察窗口确认；复盘完成并触发对应正文/来源更新。
- **停止并升级**：证据不足以支撑任何处置选择 → 先收集证据（保留现场），不用试错代替诊断；重试预算耗尽 → 换措施（隔离/降级/切换），不无限重试；回退点缺失或操作不可逆 → 立即升级授权，不先动手；**处置动作超出既有授权或权限不足 → 停止相应动作、保护现有证据并交由有权责任方，不因重试预算耗尽或需要恢复而默认取得新权限**；恢复后无法验证正确性或持续进展 → 保持"未恢复完成"状态并升级；涉及安全/数据保全风险 → 保全优先于恢复速度。

## 原始资料入口

- [Google SRE Book — Effective Troubleshooting](https://sre.google/sre-book/effective-troubleshooting/)：通用紧急诊断流程的公开参考（既有登记）。

以上为外部入口，引用前需核对版本与许可。

## 逐链检查（T00-07 交付记录，2026-10-22）

本页全部内链经 `make check` 通过，引用的目标正文均为已交付条目；未引用未交付正文。页尾外部入口为既有登记来源（`source_refs`），不承载本页导航主张。
