# 第二十九批 T08-02 来源记录

任务：T08-02（相关故障与冗余失效的公开案例；**new** `knowledge/08-reliability/correlated-failure-source-case.md`，主题 08.2/08.5）。取证轮次：主会话作者角色首轮（2026-10-21；批内前置 T08-01 已交付）。

## 新增来源与主张定位

| 主张 | 登记 ID | 精确位置 | 支持范围 |
|---|---|---|---|
| 运营方复盘全链：例行维护中的**容量评估命令**被下发→负责审查/阻止危险命令的**审计工具**因缺陷未能正确停止该命令（两类对象分开，不合并为"一条有缺陷的审计命令"）→全部骨干连接被撤→DNS 服务器因对数据中心的连接条件失败主动 declare unhealthy 并撤 BGP→外部不可达；许多（many）内部工具因 DNS 全失而不可用；主用与带外网络访问同时失效（机制未披露）；现场安全协议进入；按 storm 演练经验渐进放量；后续措施（复盘、模拟此类事件、加强测试/演练/韧性、安全取舍值得） | src.meta.oct4-2021-postmortem（**本轮新增**） | [More details about the October 4 outage](https://engineering.fb.com/2021/10/05/networking/outage-details/)（Santosh Janardhan，2021-10-05；2026-10-21 WebFetch 逐段核对，关键句已入 registry notes；初审修订后与正文同步分列命令/工具） | 第一手运营方事实；原文无任何时刻（仅机制顺序）、无命令内容/下发机制、无工具缺陷机理、无物理冗余布局、无发生率 |
| 外部观测时间线（多为发现时刻而非事件时刻）：~15:40 路由变更峰值、15:51 事故单、15:58 **注意到**DNS 前缀已停止宣告（185.89.218.0/23 与 129.134.30.0/23 不在 BGP 表、129.134.0.0/17 仍在）；Cloudflare 自身解析流量约 30 倍（图示 1.1.1.1 视角，作者以"全球解析器"概括、全球口径未披露）与 SERVFAIL 缓存；21:00–21.28 恢复序列（21:28 为外部视角暂定判断，应用恢复另需时间） | src.cloudflare.oct-2021-facebook-outage（**本轮新增**） | [Understanding how Facebook disappeared from the Internet](https://blog.cloudflare.com/october-2021-facebook-outage/)（Celso Martinho/Tom Strickx，2021-10-04；2026-10-21 WebFetch 逐段核对；初审修订后全球口径与发现时刻语义与正文同步） | 外部 BGP/DNS 观测事实；其根因表述为对 Meta 博客的转述（第二手），正文已区分 |

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

机制顺序与外部时间轴分列的时间线表（Meta 无时刻、外部多为发现时刻，两列不互相承接）、假设与调查表六行（共同原因与保护失效分列；一个被削弱假设＝1.1.1.1 作为本事件解释，原文无"其他域名对照"；一个比喻辨析）、冗余/隔离失效五点分析（原文事实与本库归纳分标；物理布局/anycast 不补写）、可迁移检查问题六条、不可外推条件四条。

## unknown 清单

1. 容量评估命令内容与下发机制、审计工具缺陷机理与修复落地、骨干连接物理布局与独立性、DNS 部署细节（含是否 anycast）、内部工具依赖清单、带外通道失效具体机制、恢复验收判据与数值、全球 30 倍测量口径——复盘/外部文均未披露，正文 unknown。
2. Meta 复盘无任何时刻；外部时刻多为发现时刻，两者无精确对齐（两文口径差异保留）。
3. 恢复过程内部决策（放量速率、判据数值）未披露；复盘未给故障损失统计。
4. 30 倍解析流量增长对 Meta 自身恢复的影响原文未评估。
5. 案例为 Web/社交基础设施（无 GPU/NPU 组件）；迁移到训练/推理集群的对象映射是本库归纳，不是原案事实。
