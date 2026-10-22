# Batch 32 来源与交付审计

收尾日期：2026-10-22。四任务（末批）：T00-06（选型、节点验收与环境安装任务路径，**new/navigation** `paths/tasks/selection-and-capacity.md`＋`paths/tasks/node-acceptance.md`＋`paths/tasks/environment-installation.md`，主题 00.6）、T08-09（可靠性主题五方面及状态边界核对，**navigation/revise** `knowledge/08-reliability/index.md`，主题 08.1–08.8）、T00-07（性能优化、迁移升级与故障恢复任务路径，**new/navigation** `paths/tasks/performance-optimization.md`＋`paths/tasks/migration-and-upgrade.md`＋`paths/tasks/fault-recovery.md`，主题 00.6）、T00-08（三平台入口与现有排障路径的收口，**new/navigation** `paths/platforms/amd.md`＋**revise** `paths/platforms/nvidia.md`/`ascend.md`/`paths/tasks/training-triage.md`/`inference-triage.md`，主题 00.6）。批内顺序按依赖：T00-06、T08-09 → T00-07 → T00-08。内容提交 90c38f7（交付时初稿）；本文件为审阅闭环后终稿。

## 来源账面

- registry **无新增**（577 维持）：四任务均为导航任务，外部引用全部复用既有登记（T00-06 页尾 5 项、T00-07 页尾 3 项、T00-08 AMD 页尾 4 项；selection-and-capacity 页 `source_refs` 为空）。
- 所有页尾外部入口 URL 与 registry 逐字核对（其中 NVIDIA 驱动指南与 CANN 升级/卸载两处在起草时曾按记忆误写，回查 registry 原文更正——教训再次验证：URL 只能从登记原文抄）。初审 C04 又将三处链接文本补齐为登记完整标题（含 latest 观察日期与 instg_0027–0033 静态镜像核读范围）。
- AMD 入口的外部引用限既有登记官方材料（ROCm 安装/发布说明、RCCL、AMD SMI），未登记任何主页类新来源。

## 审阅账面（全部 gpt-6.1-sol / xhigh，每轮经 turn_context 核验）

| 任务 | 初审 | 复核轮次 | 终态 |
|---|---|---|---|
| T00-06 | 5 项（P2×2、P3×3） | 1 轮 | 5/5 CLOSED |
| T08-09 | 4 项（P2×2、P3×2） | 1 轮 | 4/4 CLOSED |
| T00-07 | 4 项（P2×3、P3×1） | 1 轮 | 4/4 CLOSED |
| T00-08 | 3 项（P2×2、P3×1） | 1 轮 | 3/3 CLOSED |

合计 16 项编号发现全部 CLOSED，无 P1、无例外项。每轮审阅报告自含会话元数据（rollout JSONL 定位＋`CODEX_SESSION_ID`/`CODEX_THREAD_ID` 互核＋最新 `turn_context` 的 model/effort/cwd），调用方核验单一模型/档位。复核主要修订方向：**门禁与判据的忠实转写**（安装/迁移页"三类准入"改回骨架原文三项——依赖交集/有效 baseline（首次安装例外）/恢复路径，结果契约独立为验收前提；恢复页"动手前六项"改回处置正文原表六字段；兼容性方法改"分别记录声明与本地验证两轴"）；**状态与计数口径**（08 索引题组"九条"→十条 PTF-01–10、Batch 30"四篇"→五篇新增；矩阵 08.6/08.7 恢复原主题全题名）；**AMD 证据分层**（慢 rank/设备资源链降为"通用伴读、AMD 实现能力未核对"，补链含 AMD 取证的主机资源压力正文）；**导航功能补全**（五个导航目标补"进入条件/知识目标/完成检查"三要素；三平台互链与排障首要入口收口；角色页接入六条任务路径与 AMD 枚举）；**停止/升级矩阵补齐**（三页各补"无回退/权限不足"触发与动作）。未运行任何安装、查询、样例或集群操作。

## 交付账面

- 新增 7 个内容条目（稳定 ID）：`path.task.selection-and-capacity`、`path.task.node-acceptance`、`path.task.environment-installation`、`path.task.performance-optimization`、`path.task.migration-and-upgrade`、`path.task.fault-recovery`、`path.platform.amd`；全部 `type: path`、`status: draft`。
- 修订 7 个既有条目（稳定 ID 不变）：`reliability.index`（八主题五方面入口表、五方面阅读检查清单与交付核对小节）、`path.platform.nvidia`、`path.platform.ascend`、`path.task.training-triage`、`path.task.inference-triage`（新诊断分支行、恢复验证入口、AMD 分支、任务路径节、阅读目标与完成检查）、`overview.index`（00.6 行与任务/平台入口接入）、README（平台/任务入口行）。修订另涉及 `path.role.reading-by-role`（任务路径与 AMD 枚举接入，属审阅发现修订）。
- 链接纪律：新页只链接已交付正文（128 entries 全量核对平台归属后取材）；平台页新增条目逐条核对 `platforms` 字段（不含该平台的不列入）；五导航目标共用一次链接/稳定 ID 验收。
- 交付提交（90c38f7）未触碰账面文件；本收尾提交按 857702c/b0f00d1 先例更新 backlog（批次与四任务置 done、00.6-G1/G2 关闭）、topic-coverage（00.6 升 covered_basic）、盘点审计文档与 roadmap。

## 主题账面（收尾终态）

00.6 的 G1（三角色路径，T00-05）与 G2（六条任务路径与三平台入口收口，T00-06/07/08）随本批审阅闭环关闭，00.6 升为**已覆盖（基础）**；08.1–08.8 为维护验收（T08-09 核对覆盖结构与状态边界，不改变主题覆盖判断）。统计重算 **62/1/0**（部分覆盖余 03.5-BLOCKED-1）。至此 Batch 13–32 共 20 个批次与 85 项内容任务全部闭环；剩余开放项为独立验证轨道（V 工作包，七份方案执行 0/7）、V12 独立评测集外置获取与 03.5-BLOCKED-1 厂商一手资料。批次与四任务置 done（completion_record：本文件）。机器可读记录见 plans/topic-coverage.yaml 与 plans/full-coverage-backlog.yaml。

## 写作轮次自记

- 四任务均 navigation 类型：不新增技术主张，全部主张由所链正文承载；路径页的原创部分限于结构（前置材料/顺序/产出/停止条件）、分类法（三类变化、六分支影响范围）与检查清单。
- 停止/升级条件按任务验收要求逐条落页并在审阅后补齐：验收工具前提不满足记"无法判断"；安装准入门禁三项缺一即停、任一层失败不得向上安装；性能优化无基线先补基线、无回退只留只读结论；恢复验收双判据（正确性＋持续进展）。
- 各页 unknown 清单与"导航不产生运行结果""样板不等于兼容矩阵"边界显式声明；未执行任何命令、未访问任何设备。
- 审阅修订逐项记录见四份 sources 记录的"复核轮修订记录（初审后）"小节；初审/复核报告共八份落盘于 docs/research/。
- 后续维护：新增正文交付后同步更新路径入口与完成检查口径（00.6 维护判据）；知识维护的复核触发与弃用规则见 08 域正文。
