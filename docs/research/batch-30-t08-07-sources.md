# 第三十批 T08-07 来源记录

任务：T08-07（事故复盘、来源更新与知识维护；**new** `knowledge/08-reliability/postmortem-and-knowledge-update.md`，主题 08.8/08.3/08.4）。取证轮次：主会话作者角色首轮（2026-10-21；同批前置 T08-06 已于本轮完成，跨批前置 T08-03 已于 Batch 29 交付）。

## 新增来源与主张定位

| 主张 | 登记 ID | 精确位置 | 支持范围 |
|---|---|---|---|
| 无责复盘原则与组织激励；模板字段（影响/根因与触发/时间线/经验教训/行动项表）；行动项须有负责人/优先级/类型（prevent/mitigate/detect/repair/investigate）/跟踪 bug；发布时机；复盘库与阅读会/Wheel of Misfortune | src.google.sre-postmortem-culture（**本轮新增**） | [SRE Workbook Ch.10](https://sre.google/workbook/postmortem-culture/)（2026-10-21 全文核读；CC BY-NC-ND 4.0） | 服务运维文化实践 |
| 四角色递归职责分离（Command/Ops/Communication/Planning；Ops 唯一改动系统）；实时事件文档要求；尽早宣布三触发；明确交接；"止血、恢复、保全证据" | src.google.sre-managing-incidents（**本轮新增**） | [SRE Book Ch.14](https://sre.google/sre-book/managing-incidents/)（2026-10-21 全文核读；CC BY-NC-ND 4.0） | 事件指挥方法论 |
| 诊断报告结构（根因节点/首错节点/现象/根因节点链/故障分类/建议方案/关键日志/传播链；-p 性能劣化；16 条上限与 diag_report.json） | src.ascend.faultdiag-v26.1.1（**本轮新增**，与 T08-04 共用） | 固定 commit 44385c1 概述/04_fault_diagnosis 页（2026-10-21 核读） | 自动化输出＝候选假设的样板；示例非真实事故 |

## 复用来源与主张定位

| 主张 | 登记 ID | 精确位置 | 支持范围 |
|---|---|---|---|
| 假设—演绎、证据保全、主动测试副作用 | src.google.sre-effective-troubleshooting | 章节（2026-09-29 已核） | 方法论 |
| 症状/观测与覆盖纪律（复盘字段"采集覆盖"的底座） | src.google.sre-monitoring-distributed-systems | 章节（2026-09-29 已核） | 同上 |
| 公开复盘映射示例（事件时刻 vs 外部发现时刻、双证据） | src.meta.oct-2021-facebook-outage / src.cloudflare.oct-2021-facebook-outage | 两篇（Batch 29 全文核读）；库内整理见 [correlated-failure-source-case](../../knowledge/08-reliability/correlated-failure-source-case.md) | 单一事件的运营方＋观测方证据 |

## 本文原创部分

复盘必填字段表（在 SRE 模板上加"实体/版本/工作键、采集覆盖、假设三分"三组）、三类材料区分表（本地/公开/合成）、五步追溯链（登记→反查→修订→定向审阅→导航）与责任角色、四类复核触发表、弃用四规则、"流程不创建的东西"负面清单、公开复盘映射示例的字段对应。

## unknown 清单

1. 本地事故复盘：当前无本地事件，流程未在真实事故上执行过（verification: source_checked 而非 reproduced）。
2. 行动项跟踪载体：当前以条目内表格承载，未选定外部跟踪系统（SRE 的 Requiem 类工具仅作方向参考）。
3. 与外部厂商联合复盘、法律责任边界、客户通报模板：超出本文范围未写。
