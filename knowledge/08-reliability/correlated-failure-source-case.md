---
id: reliability.correlated-failure-source-case
title: 相关故障与冗余失效来源案例（Meta 2021-10-04 断网）
type: case
domain: reliability
status: draft
platforms: [generic]
source_refs:
  - src.meta.oct4-2021-postmortem
  - src.cloudflare.oct-2021-facebook-outage
updated_at: "2026-10-21"
summary: 复盘 Meta 2021-10-04 全球服务中断：一条维护审计命令因工具缺陷撤除全部骨干连接，DNS 服务器随之主动撤回 BGP，服务与健康实例同时不可达，内部工具、主用与带外访问一并失效；用运营方复盘与外部 BGP/DNS 观测两类证据区分共同原因、传播与放大。
related_ids:
  - reliability.fault-models-and-propagation
  - reliability.dimensions-and-failure-domains
  - reliability.evidence-and-hypotheses
  - reliability.mitigation-and-recovery-principles
applicability:
  environment_refs: []
  notes: "案例限定为 Meta 2021-10 公开的网络与服务架构（以复盘披露为准，内部细节未公开）；是 Web/社交基础设施案例，不含 GPU/NPU 组件。检查问题可迁移到任何有共享骨干、DNS/服务发现与带外通道的系统；结论不可外推到任何加速器平台的故障率或恢复能力。"
verification:
  status: source_checked
  evidence_refs:
    - src.meta.oct4-2021-postmortem
    - src.cloudflare.oct-2021-facebook-outage
  notes: "已逐段核对 Meta 工程博客复盘（Janardhan，2021-10-05）与 Cloudflare 博客外部观测（Martinho/Strickx，2021-10-04）两篇原文；未访问 Meta 或 Cloudflare 任何系统，无第三方根因结论。精确时间戳仅来自 Cloudflare 外部观测；Meta 复盘未给时间戳，两文口径差异如实保留。"
---

# 相关故障与冗余失效来源案例（Meta 2021-10-04 断网）

## 案例来源与问题

本案例来自两份原始公开材料：Meta（运营方）工程博客复盘 [More details about the October 4 outage](https://engineering.fb.com/2021/10/05/networking/outage-details/)（Santosh Janardhan，2021-10-05）与 Cloudflare（外部观测方）博客 [Understanding how Facebook disappeared from the Internet](https://blog.cloudflare.com/october-2021-facebook-outage/)（Celso Martinho/Tom Strickx，2021-10-04）。它回答本库 08.2/08.5 的两个问题：**共享依赖如何把一次单点操作放大为全局失效**，以及**冗余与隔离假设在什么边界上失效**。选它不是因为规模大，而是因为运营方复盘与外部观测两类证据可交叉核对，覆盖共同原因、传播、放大与恢复四个环节。

本库不写本地事故，也不引用任何发生率；本文所有事实限于两篇原文披露范围。

## 当时环境与架构边界

按复盘披露记录（未披露部分保持 unknown，不以常识补写）：

- **系统边界**：Meta 的全球服务（文中列举 Facebook、Instagram、WhatsApp 等）依赖其**骨干网络（backbone）**互联各数据中心，服务的域名解析由 Meta 自有 DNS 服务器承担；这些 DNS 服务器通过 BGP 向互联网宣告自身地址。
- **故障前的例行维护**：事发时正在执行例行维护作业，其中包括一条**评估骨干容量的审计命令**；该命令经由自动化工具下发。
- **运维通道**：正常远程访问数据中心、日常使用的内部工具、以及**主用与带外（out-of-band）网络访问**通道并存；数据中心设施有高等级物理与系统安全设计。
- 复盘未披露：审计工具的内部实现与缺陷细节、命令具体内容、骨干路由器数量与拓扑、DNS 服务器部署细节、内部工具的依赖清单。以上均为 unknown。

## 事件与证据时间线

| 时刻（UTC） | 事件或观测 | 证据类型 | 证据定位 |
|---|---|---|---|
| 事发前 | 例行维护中的审计命令因工具 bug 无法正确停止（"a bug in that audit tool prevented it from properly stopping the command"） | 运营方复盘 | [Meta 复盘](https://engineering.fb.com/2021/10/05/networking/outage-details/) |
| 事发（复盘称"非常快"，无时刻） | 命令"unintentionally took down all the connections in our backbone network"，全球数据中心断连 | 运营方复盘 | 同上 |
| ~15:40 | Facebook 侧路由变更出现峰值（"we saw a peak of routing changes"） | 外部观测 | [Cloudflare 博客](https://blog.cloudflare.com/october-2021-facebook-outage/) |
| ~15:50 / 15:51 | facebook.com 在 1.1.1.1 停止解析；Cloudflare 开内部事故单"Facebook DNS lookup returning SERVFAIL" | 外部观测 | 同上 |
| 15:58 | Cloudflare 注意到 Facebook 停止宣告 DNS 前缀路由（示例 `185.89.218.0/23`、`129.134.30.0/23` 不在 BGP 表，较宽前缀 `129.134.0.0/17` 仍在） | 外部观测 | 同上 |
| 随后数分钟 | Meta 的 DNS 服务器因无法连接数据中心而"declare themselves unhealthy and withdraw those BGP advertisements"；服务器进程仍在运行但互联网不可达（"impossible for the rest of the internet to find our servers"） | 运营方复盘 | [Meta 复盘](https://engineering.fb.com/2021/10/05/networking/outage-details/) |
| 中断期间 | 全球解析器查询量升至约 30 倍并缓存 SERVFAIL；Cloudflare 一度怀疑自家 1.1.1.1 故障，后被观测反驳 | 外部观测 | [Cloudflare 博客](https://blog.cloudflare.com/october-2021-facebook-outage/) |
| 中断期间 | 正常远程访问不可用；"the total loss of DNS broke many of the internal tools"；"Our primary and out-of-band network access was down"；工程师须按安全协议现场进入 | 运营方复盘 | [Meta 复盘](https://engineering.fb.com/2021/10/05/networking/outage-details/) |
| ~21:00–21:28 | BGP 活动恢复（21:17 峰值）、21:20 facebook.com 可解析、21:28 判定重新接入互联网 | 外部观测 | [Cloudflare 博客](https://blog.cloudflare.com/october-2021-facebook-outage/) |
| 恢复过程 | 现场确认问题并重启骨干，随后按既有 "storm" 演练经验渐进放量（"carefully manage the increasing loads"），未再出现系统性故障 | 运营方复盘 | [Meta 复盘](https://engineering.fb.com/2021/10/05/networking/outage-details/) |

两文时间口径的差异如实保留：Meta 复盘自述事件发生"very fast"但未给时刻；分钟级时刻均来自 Cloudflare 侧观测，观测点与 Meta 内部时钟并非同一来源。

## 假设与调查：共同原因、传播、放大与独立故障的区分

| 候选解释 | 支持证据 | 反对或缺失证据 | 结论边界 |
|---|---|---|---|
| 审计命令缺陷是**共同原因**（一次操作同时作用于全部骨干连接） | 复盘明确该命令撤除了**全部**骨干连接；多条连接同时中断与单一命令一致 | 工具缺陷机理未披露 | 以运营方复盘为准的**已确认事实**；不是外部推断 |
| DNS 不可达是**传播**（骨干断→健康检查失败→主动撤 BGP） | 复盘原文描述 DNS 服务器"declare themselves unhealthy and withdraw"；外部观测 15:58 前缀消失在骨干中断之后 | DNS 服务器健康判定的具体条件未披露 | 传播链成立；DNS 服务器本身"进程健康但不可达"，不是 DNS 自身故障 |
| 全球解析量 30 倍增长是**放大**（重试风暴），不是独立故障 | Cloudflare 观测 30x 查询与 SERVFAIL 缓存；对象是全互联网解析器 | 无 | 放大效应；对 Meta 恢复的影响原文未评估（unknown） |
| "多服务同时宕机"是各自独立故障 | Facebook/Instagram/WhatsApp 同时不可用 | 单一骨干/DNS 共享依赖足以解释全部服务不可用 | **不获支持**：这是共享依赖的共同失效，按独立故障建模会低估相关失效风险 |
| Cloudflare 自家解析器故障 | 事故单最初标题是 "Facebook DNS lookup returning SERVFAIL"，团队一度怀疑 1.1.1.1 | 其他域名解析正常、BGP 表变化独立佐证 | 被观测反驳的**误假设**；保留它作为"先怀疑自己"的排障常态样本 |
| "像被人拔了线"（"It was as if someone had 'pulled the cables'"） | —— | Cloudflare 原文明示这是比喻 | 比喻不是证据；物理层无任何故障证据 |

## 冗余与隔离为什么失效

这是本案例对本库最有价值的部分——失效的不是冗余数量，而是**冗余的独立性假设**：

1. **骨干的多条连接共享同一控制路径**。物理上冗余的骨干连接，其可用性共同取决于"一条命令能否同时撤除它们"。当配置/控制面把全部连接作为同一批次作用对象时，物理冗余退化为共同原因域（分类见[故障模型、跨层传播与共享失效分析](fault-models-and-propagation.md)）。
2. **健康≠可达**。DNS 服务器进程正常运行，但它们用"撤回 BGP"表达不健康；服务健康性与网络可达性是两个故障域，对外服务取决于两者同时成立。
3. **运维通道与被管系统共享依赖**。内部工具依赖同一 DNS；主用与带外网络访问同时失效。备份通道没有跨出主通道的故障域时，最需要它的时刻恰是它失效的时刻。
4. **恢复速度与安全设计存在权衡**。复盘承认高等级物理/系统安全设计使现场恢复变慢，并明确认为该取舍值得（"a tradeoff like this is worth it"）——这是显式记录设计权衡的范例，本库不以自己的偏好改写该判断。
5. **恢复本身需要容量与节奏**。重启骨干后按演练经验渐进放量，避免二次崩溃；"恢复完成"是流量逐步回升的过程而非开关事件（与[可靠性维度与故障域](dimensions-and-failure-domains.md)的恢复退出门槛一致）。

## 处置与结果

复盘记录的处置链：远程通道不可用 → 工程师现场到达并激活安全访问协议 → 确认问题 → 重启骨干网络 → 服务与基础设施组件逐步恢复 → 按风暴演练经验管理回切流量。可确认的结果：外部观测约 21:00–21:28 间互联网侧恢复。复盘公布的后续措施：复盘流程已启动、寻找模拟此类事件的方式（此前从未演练过骨干全断场景）、加强测试/演练与整体韧性。审计工具修复情况、防护措施的落地细节未披露（unknown）。

## 可迁移的检查问题

- 你的"冗余"对象是否共享同一条配置下发路径？一次命令/一个模板错误能否同时撤除全部"冗余"？
- 服务健康判定（进程/探针）与网络可达性（路由/DNS/服务发现）是否分属不同故障域？对外不可达时你的系统如何表现？
- 带外/灾备通道是否依赖与主路径共享的 DNS、认证、目录或物理设施？最后核对是什么时候？
- 高危维护工具的停止与回滚语义是否有测试？下发对象的批处理边界在哪里？
- 是否演练过"骨干/控制面全断"场景？恢复时按什么速率放量、判据是什么？
- 事件中"先怀疑自家"的假设如何被反驳？哪条观测承担了反驳证据？

## 不可外推的条件

- 该案例发生在 Meta 的网络与服务架构（社交/Web 服务，无 GPU/NPU 组件）；数据中心骨干、DNS anycast 式宣告、内部工具生态都是其环境特有。
- 两篇原文不含任何故障率、恢复时间统计或多环境对比；单次事件不能作为任何系统（包括 Meta 自己的当前系统）的发生率证据。
- 时间线分钟级时刻来自外部观测方，与运营方内部视角存在观测点差异；因果链以运营方复盘为第一来源。
- 本库未验证任何 Meta 或 Cloudflare 系统；本文是来源整理，不是本地复现。

## 来源与未解问题

- [Meta 工程博客复盘（Janardhan，2021-10-05）](https://engineering.fb.com/2021/10/05/networking/outage-details/)
- [Cloudflare 博客外部观测（Martinho/Strickx，2021-10-04）](https://blog.cloudflare.com/october-2021-facebook-outage/)
- 本地复现状态：未开展（本案例不可复现，属他人事件复盘）。
- 待确认：审计工具缺陷机理、带外通道失效的具体依赖链、内部工具依赖清单、恢复的完整决策过程——原文均未披露，保持 unknown。
- 迁移到 GPU/NPU 集群时的应用对象：共享配置面（集群管理/网络自动化）、服务发现与 DNS、带外管理网、维护工具的下发边界；配套检查方法见[故障模型、跨层传播与共享失效分析](fault-models-and-propagation.md)与[隔离、重试预算、降级与恢复选择](mitigation-and-recovery-principles.md)。
