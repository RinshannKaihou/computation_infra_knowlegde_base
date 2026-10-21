# 第二十九批 T08-02 来源记录

任务：T08-02（相关故障与冗余失效的公开案例；**new** `knowledge/08-reliability/correlated-failure-source-case.md`，主题 08.2/08.5）。取证轮次：主会话作者角色首轮（2026-10-21；批内前置 T08-01 已交付）。

## 新增来源与主张定位

| 主张 | 登记 ID | 精确位置 | 支持范围 |
|---|---|---|---|
| 运营方复盘全链：审计工具 bug 无法停止命令→全部骨干连接被撤→DNS 服务器主动 declare unhealthy 并撤 BGP→外部不可达；内部工具因 DNS 全失而不可用；主用与带外网络访问同时失效；现场安全协议进入；按 storm 演练经验渐进放量；后续措施（复盘、模拟此类事件、加强测试/演练/韧性、安全取舍值得） | src.meta.oct4-2021-postmortem（**本轮新增**） | [More details about the October 4 outage](https://engineering.fb.com/2021/10/05/networking/outage-details/)（Santosh Janardhan，2021-10-05；2026-10-21 WebFetch 逐段核对，关键句已入 registry notes） | 第一手运营方事实；原文无精确时间戳、无工具缺陷机理、无发生率 |
| 外部观测时间线：~15:40 路由变更峰值、15:51 事故单、15:58 DNS 前缀停止宣告（185.89.218.0/23 与 129.134.30.0/23 不在 BGP 表、129.134.0.0/17 仍在）；resolver 30 倍查询与 SERVFAIL；21:00–21:28 恢复序列 | src.cloudflare.oct-2021-facebook-outage（**本轮新增**） | [Understanding how Facebook disappeared from the Internet](https://blog.cloudflare.com/october-2021-facebook-outage/)（Celso Martinho/Tom Strickx，2021-10-04；2026-10-21 WebFetch 逐段核对） | 外部 BGP/DNS 观测事实；其根因表述为对 Meta 博客的转述（第二手），正文已区分 |

## 复用来源与主张定位

| 主张 | 登记 ID | 精确位置 | 支持范围 |
|---|---|---|---|
| 共同原因/相关/独立故障与故障域框架 | 既有 08 域正文 | [dimensions-and-failure-domains](../../knowledge/08-reliability/dimensions-and-failure-domains.md) | 案例分析表的分类依据 |
| fault→error→failure 与跨层传播 | 本批 T08-01 交付正文 | [fault-models-and-propagation](../../knowledge/08-reliability/fault-models-and-propagation.md) | 传播链表述与共同原因域用语 |
| 假设-演绎与证据区分 | 既有 08 域正文 | [evidence-and-hypotheses](../../knowledge/08-reliability/evidence-and-hypotheses.md) | 假设与调查表的"支持/反驳/未知"结构 |
| 恢复退出门槛 | 既有 08 域正文 | 同 dimensions-and-failure-domains | "恢复完成是过程不是开关"的判据引用 |

## 选案说明

source_discovery 要求优先原始运营方复盘或论文附带事件、不以二手新闻替代。本案例选择 Meta 官方工程博客复盘（运营方一手）＋Cloudflare 博客（观测方一手，其根因段落明确标注转述 Meta）；两篇均为作者署名的原始发布，非新闻聚合。GitHub 2018-10-21、Cloudflare 2019-07-02 等同类候选未采用，检索与取舍过程未逐项落盘（本记录如实标注）。

## 本文原创部分

两类证据的时间线合并表（口径差异显式保留）、假设与调查表六行（含两个被反驳假设）、冗余/隔离失效五点分析、可迁移检查问题六条、不可外推条件四条。

## unknown 清单

1. 审计工具缺陷机理、命令内容、骨干路由器数量与拓扑、DNS 部署细节、内部工具依赖清单——复盘未披露，正文 unknown。
2. 精确时间戳全部来自外部观测方，与 Meta 内部视角的时钟对齐未核（两文口径差异保留）。
3. 恢复过程内部决策（放量速率、判据数值）未披露；复盘未给故障损失统计。
4. 30 倍解析流量增长对 Meta 自身恢复的影响原文未评估。
5. 案例为 Web/社交基础设施（无 GPU/NPU 组件）；迁移到训练/推理集群的对象映射是本库归纳，不是原案事实。
