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
| 公开复盘映射示例（事件时刻 vs 外部发现时刻、双证据） | src.meta.oct4-2021-postmortem / src.cloudflare.oct-2021-facebook-outage | 两篇（Batch 29 全文核读）；库内整理见 [correlated-failure-source-case](../../knowledge/08-reliability/correlated-failure-source-case.md) | 单一事件的运营方＋观测方证据 |

## 本文原创部分

复盘必填字段表（在 SRE 模板上加"实体/版本/工作键、采集覆盖、假设三分"三组）、三类材料区分表（本地/公开/合成）、六步追溯链（登记→反查→修订→定向审阅→导航→结构检查与 catalog 重建）与责任角色、四类复核触发表、弃用四规则、"流程不创建的东西"负面清单、公开复盘映射示例的字段对应。

## unknown 清单

1. 本地事故复盘：当前无本地事件，流程未在真实事故上执行过（verification: source_checked 而非 reproduced）。
2. 行动项跟踪载体：当前以条目内表格承载，未选定外部跟踪系统（SRE 的 Requiem 类工具仅作方向参考）。
3. 与外部厂商联合复盘、法律责任边界、客户通报模板：超出本文范围未写。

## 复核轮修订记录（初审后）

- C01：映射示例重写——删除"撤销未生效"与"第二起故障叠加"（原文无据）；机制顺序（命令→审计失效→断连→主动撤回 BGP 宣告，DNS 服务器仍在运行）与外部发现时刻（15:51/15:58）分列；恢复期风险标注为预防性担忧；命令细节保持 unknown。
- C02：证据保全行收缩为按现场已部署工具的条件执行＋采集缺口记录；NCCL flight recorder 例子改挂 Llama 3 §3.3.4（已登记来源）并注明其配置前提未登记；"转储前先拷贝"改条件化表述。
- C03：追溯链补第 6 步（make check/build 重建 catalog、核对受影响 ID、失败阻断完成），登记者确认生成结果；完成判据同步。（第二轮：本记录原创部分原写的"五步"同步更正为六步。）
- C04：正文 Meta URL 对齐登记入口（networking/outage-details/）；取证记录 ID 更正为 src.meta.oct4-2021-postmortem。（第二轮补证；第三轮补齐可核对证据：2026-10-21 作者本地 `curl -sL`（跟随重定向，30 s 上限）请求登记入口 https://engineering.fb.com/2021/10/05/networking/outage-details/ → HTTP 200、重定向 1 次、最终 URL=https://engineering.fb.com/2021/10/05/networking-traffic/outage-details/、页面 title="More details about the October 4 outage - Engineering at Meta"、HTML canonical 指向 networking-traffic 形态（正文 88403 字节）；直接请求 networking-traffic 形态亦 200——登记入口经重定向到达与复核方独立核读相同的文章。该证据已同步 registry notes。复核方工具的 DNS 失败不构成反证。）
- C05："SRE 模板一周内发布"改为好案例表现与反例的对照（非统一时限）。
