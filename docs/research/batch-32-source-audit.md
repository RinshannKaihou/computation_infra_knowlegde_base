# Batch 32 来源与交付审计

交付日期：2026-10-22（内容提交）。四任务（末批）：T00-06（选型、节点验收与环境安装任务路径，**new/navigation** `paths/tasks/selection-and-capacity.md`＋`paths/tasks/node-acceptance.md`＋`paths/tasks/environment-installation.md`，主题 00.6）、T08-09（可靠性主题五方面及状态边界核对，**navigation/revise** `knowledge/08-reliability/index.md`，主题 08.1–08.8）、T00-07（性能优化、迁移升级与故障恢复任务路径，**new/navigation** `paths/tasks/performance-optimization.md`＋`paths/tasks/migration-and-upgrade.md`＋`paths/tasks/fault-recovery.md`，主题 00.6）、T00-08（三平台入口与现有排障路径的收口，**new/navigation** `paths/platforms/amd.md`＋**revise** `paths/platforms/nvidia.md`/`ascend.md`/`paths/tasks/training-triage.md`/`inference-triage.md`，主题 00.6）。批内顺序按依赖：T00-06、T08-09 → T00-07 → T00-08。**审阅未开始**；本文件为交付时初稿，审阅闭环后更新。

## 来源账面

- registry **无新增**（577 维持）：四任务均为导航任务，外部引用全部复用既有登记（T00-06 页尾 5 项、T00-07 页尾 3 项、T00-08 AMD 页尾 4 项；selection-and-capacity 页 `source_refs` 为空）。
- 所有页尾外部入口 URL 与 registry 逐字核对（其中 NVIDIA 驱动指南与 CANN 升级/卸载两处在起草时曾按记忆误写，已回查 registry 原文更正；教训再次验证：URL 只能从登记原文抄）。
- AMD 入口的外部引用限既有登记官方材料（ROCm 安装/发布说明、RCCL、AMD SMI），未登记任何主页类新来源。

## 交付账面

- 新增 7 个内容条目（稳定 ID）：`path.task.selection-and-capacity`、`path.task.node-acceptance`、`path.task.environment-installation`、`path.task.performance-optimization`、`path.task.migration-and-upgrade`、`path.task.fault-recovery`、`path.platform.amd`；全部 `type: path`、`status: draft`。
- 修订 7 个既有条目（稳定 ID 不变）：`reliability.index`（新增八主题五方面入口表、五方面阅读检查清单与交付核对小节）、`path.platform.nvidia`、`path.platform.ascend`、`path.task.training-triage`、`path.task.inference-triage`（新增诊断分支行、恢复验证入口、AMD 分支与任务路径节）、`overview.index`（00.6 行与任务/平台入口接入）、README（平台/任务入口行）。
- 链接纪律：新页只链接已交付正文（128 entries 全量核对平台归属后取材）；平台页新增条目逐条核对 `platforms` 字段（不含该平台的不列入，如 ascend 页不列 routing-and-flow-control、nvidia/ascend 页不列 rccl 档案）；五导航目标共用一次链接/稳定 ID 验收。
- 本批不触碰 plans/full-coverage-backlog.yaml 与 plans/topic-coverage.yaml（交付提交不动账面，审阅闭环后按口径更新——沿 857702c/d0b5cc3 先例）。

## 主题账面（交付时点，审阅后重算）

00.6 的 G1（三角色路径）已于 Batch 31 关闭；G2（选型/验收/安装/优化/升级/恢复任务路径）与三平台入口收口随本批 T00-06/07/08 交付内容齐备，缺口关闭与否待审阅闭环后按主题验收批次（00.6 为 Batch 32）重算。08.1–08.8 为维护验收（T08-09 核对覆盖结构，不改变任何主题判断）。统计重算留待收尾提交。

## 写作轮次自记

- 四任务均 navigation 类型：不新增技术主张，全部主张由所链正文承载；路径页的原创部分限于结构（前置材料/顺序/产出/停止条件）、分类法（三类变化、六分支影响范围）与检查清单。
- 停止/升级条件按任务验收要求逐条落页：验收工具前提不满足记"无法判断"；安装准入门禁三类缺一即停；性能优化无基线先补基线；恢复验收双判据（正确性＋持续进展）。
- 各页 unknown 清单与"导航不产生运行结果""样板不等于兼容矩阵"边界显式声明；未执行任何命令、未访问任何设备。
- 下一状态：gpt-6.1-sol/xhigh 初审＋复核（留给交互会话）；审阅闭环后批次与四任务置 done、00.6 主题验收重算、统计与盘点审计同步。
