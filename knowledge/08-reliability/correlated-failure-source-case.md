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
summary: 复盘 Meta 2021-10-04 全球服务中断：例行维护中的容量评估命令因审查/审计工具的缺陷未能被正确停止，撤除全部骨干连接，DNS 服务器随之主动撤回 BGP，服务与运行中的实例同时不可达，内部工具、主用与带外访问一并失效；用运营方复盘与外部 BGP/DNS 观测两类证据区分共同原因、传播与放大。
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
- **故障前的例行维护**：事发时正在执行例行维护作业，其中包括一条**评估骨干网容量的命令**；复盘另描述存在负责审查、阻止危险命令的**审计工具**，其缺陷（"a bug in that audit tool"）使该命令未能被正确停止。命令的具体内容、下发机制与工具缺陷机理均未披露（unknown），本文不合并两者为"一条有缺陷的审计命令"。
- **运维通道**：正常远程访问数据中心、日常使用的内部工具、以及**主用与带外（out-of-band）网络访问**通道并存；数据中心设施有高等级物理与系统安全设计。
- 复盘未披露：审计工具的内部实现与缺陷细节、命令具体内容、骨干路由器数量与拓扑、DNS 服务器部署细节、内部工具的依赖清单。以上均为 unknown。

## 事件与证据时间线

两类证据分列：Meta 复盘只给**机制顺序**（自述"All of this happened very fast"，无任何时刻）；分钟级时刻全部来自 Cloudflare 外部观测，且多为**发现/注意到**的时刻而非事件发生时刻。两列不互相承接。

| 时刻（UTC） | 事件或观测 | 证据类型 | 证据定位 |
|---|---|---|---|
| 无时刻（机制顺序 ①） | 例行维护中评估骨干容量的命令被下发；审计工具的缺陷使其未能正确停止该命令 | 运营方复盘 | [Meta 复盘](https://engineering.fb.com/2021/10/05/networking/outage-details/) |
| 无时刻（机制顺序 ②） | 该命令"unintentionally took down all the connections in our backbone network"，全球数据中心断连 | 运营方复盘 | 同上 |
| 无时刻（机制顺序 ③） | Meta 的 DNS 服务器因无法连接数据中心而"declare themselves unhealthy and withdraw those BGP advertisements"；服务器仍在运行但互联网不可达（"impossible for the rest of the internet to find our servers"） | 运营方复盘 | 同上 |
| ~15:40 | Facebook 侧路由变更出现峰值（"we saw a peak of routing changes"，作者称问题自此开始） | 外部观测 | [Cloudflare 博客](https://blog.cloudflare.com/october-2021-facebook-outage/) |
| ~15:50 / 15:51 | facebook.com 在 1.1.1.1 停止解析；Cloudflare 开内部事故单"Facebook DNS lookup returning SERVFAIL" | 外部观测 | 同上 |
| 15:58 | Cloudflare **注意到**Facebook 已停止宣告 DNS 前缀路由（发现时刻，非消失时刻；示例 `185.89.218.0/23`、`129.134.30.0/23` 不在 BGP 表，较宽前缀 `129.134.0.0/17` 仍在） | 外部观测 | 同上 |
| 中断期间 | Cloudflare 报告其解析流量约为平时 30 倍并缓存 SERVFAIL，作者以"全球解析器"概括该影响（图示数据视角为 1.1.1.1，全球测量口径未披露）；Cloudflare 一度怀疑自家 1.1.1.1 故障，后被多公共解析器同样 SERVFAIL 与 BGP 表观测削弱 | 外部观测 | 同上 |
| 无时刻 | 正常远程访问不可用；"the total loss of DNS broke many of the internal tools"；"Our primary and out-of-band network access was down"；工程师须按安全协议现场进入 | 运营方复盘 | [Meta 复盘](https://engineering.fb.com/2021/10/05/networking/outage-details/) |
| ~21:00–21:28 | BGP 活动恢复（21:17 峰值）、21:20 facebook.com 可解析、21:28 Cloudflare 从外部视角判断 Facebook 重新接入互联网（作者注明应用恢复仍需时间——非全服务恢复验收） | 外部观测 | [Cloudflare 博客](https://blog.cloudflare.com/october-2021-facebook-outage/) |
| 无时刻（恢复顺序） | 现场确认问题并重启骨干，随后按既有 "storm" 演练经验渐进放量（"carefully manage the increasing loads"），未再出现系统性故障 | 运营方复盘 | [Meta 复盘](https://engineering.fb.com/2021/10/05/networking/outage-details/) |

Meta 的机制顺序①②③先于外部观测到的前缀消失，这是复盘因果叙述支持的**顺序**，不是与外部时刻的精确对齐；两文观测点不同，本文不为 Meta 补写任何时刻。

## 假设与调查：共同原因、传播、放大与独立故障的区分

| 候选解释 | 支持证据 | 反对或缺失证据 | 结论边界 |
|---|---|---|---|
| 容量评估命令的全局作用是**共同原因**（一次命令同时作用于全部骨干连接），审计工具缺陷是**保护失效** | 复盘明确该命令撤除了**全部**骨干连接；多条连接同时中断与单一命令一致；复盘另述审计工具未能阻止 | 命令内容、下发机制与工具缺陷机理均未披露 | 以运营方复盘为准的**已确认事实**：共同原因＝命令的全局作用范围；两类对象分开记录，不合并为"一条有缺陷的审计命令" |
| DNS 不可达是**传播**（骨干断→DNS 服务器的数据中心连接条件失败→主动撤 BGP） | 复盘原文描述 DNS 服务器"declare themselves unhealthy and withdraw"；外部 15:58 发现前缀已消失 | DNS 服务器健康判定的具体条件未披露；健康判定指向连接条件，复盘未给进程健康测量记录 | 传播链成立；三个边界分开——服务器仍在运行（复盘口径）、对数据中心的连接条件（撤告触发）、对外解析服务（已失效）；这是骨干失效向 DNS 服务的传播，不是 DNS 进程独立损坏的证据 |
| 解析流量约 30 倍是**放大**（重试风暴），不是独立故障 | Cloudflare 自身观测（图示 1.1.1.1 视角）＋作者"全球解析器"概括 | 全球全体解析器的采集范围、分母与聚合口径未披露，不能当作全互联网直接测量 | 放大效应成立于 Cloudflare 观测范围；对 Meta 恢复的影响原文未评估（unknown） |
| "多服务同时宕机"是各自独立故障 | Facebook/Instagram/WhatsApp 同时不可用 | 单一骨干/DNS 共享依赖足以解释全部服务不可用 | **不获支持**：这是共享依赖的共同失效，按独立故障建模会低估相关失效风险 |
| Cloudflare 自家解析器故障是本次 facebook.com 失败的解释 | 事故单最初标题是 "Facebook DNS lookup returning SERVFAIL"，团队一度怀疑 1.1.1.1 | 原文展示多个公共解析器同样 SERVFAIL 的示例；Cloudflare 自身 BGP 表观测到 Facebook 前缀消失 | 该假设作为**本事件的解释**被上述证据削弱（排障"先怀疑自己"的常态样本）；不等于排除 Cloudflare 的所有潜在独立故障，原文也未给"其他域名对照"记录 |
| "像被人拔了线"（"It was as if someone had 'pulled the cables'"） | —— | Cloudflare 原文明示这是比喻 | 比喻不是证据；物理层无任何故障证据 |

## 冗余与隔离为什么失效

这是本案例对本库最有价值的部分——失效的不是冗余数量，而是**冗余的独立性假设**。以下区分原文事实与本库归纳：

1. **全部骨干连接被一次命令同时撤除**（原文事实）。无论其实际物理布局如何（连接数量、备份路径、独立性——原文未披露，unknown），"一条命令能同时作用于全部连接"本身说明这些连接在**配置/控制路径**维度上共享。本库归纳：冗余的独立性必须按每个故障模式分别核对（分类见[故障模型、跨层传播与共享失效分析](fault-models-and-propagation.md)），"多条连接"不自动等于独立。
2. **服务健康判定与网络可达性是两个不同的服务条件**（原文支持前者的撤告机制与后者的不可达结果）。DNS 服务器仍在运行，却因对数据中心的连接条件失败而撤回宣告；对外服务取决于运行、连接与可达同时成立。本库归纳：健康探针通过不等于可达，两者各自需要判据与观测点。
3. **内部工具与运维通道同时不可用**（原文事实分两条）：许多（many）内部工具因 DNS 全失而不可用；主用与带外网络访问同时失效。**具体共享机制原文未披露**（带外是否依赖 DNS、同一链路或认证——unknown）。本库归纳：同时失效是观测，"共享依赖"是候选解释与迁移检查问题，不是该事故带外失效的已确认原因。
4. **恢复速度与安全设计存在权衡**（原文事实）。复盘承认高等级物理/系统安全设计使现场恢复变慢，并明确认为该取舍值得（"a tradeoff like this is worth it"）——这是显式记录设计权衡的范例，本库不以自己的偏好改写该判断。
5. **恢复本身需要容量与节奏**（原文事实）。重启骨干后按演练经验渐进放量，避免二次崩溃；"恢复完成"是流量逐步回升的过程而非开关事件（与[可靠性维度与故障域](dimensions-and-failure-domains.md)的恢复退出门槛一致）。

## 处置与结果

复盘记录的处置链：远程通道不可用 → 工程师现场到达并激活安全访问协议 → 确认问题 → 重启骨干网络 → 服务与基础设施组件逐步恢复 → 按风暴演练经验管理回切流量。可确认的结果：外部观测约 21:00–21:28 间互联网侧 BGP/DNS 恢复（Cloudflare 视角的暂定判断，应用层恢复另需时间）。复盘公布的后续措施：复盘流程已启动、寻找模拟此类事件的方式（此前从未演练过骨干全断场景）、加强测试/演练与整体韧性。审计工具修复情况、防护措施的落地细节、恢复的业务/状态/性能验收方法与数值均未披露（unknown）。

## 可迁移的检查问题

- 你的"冗余"对象是否共享同一条配置下发路径？一次命令/一个模板错误能否同时作用于全部"冗余"？
- 服务健康判定与网络可达性是两个不同的服务条件——对外不可达时你的系统如何表现？两者各自的判据与观测点是什么？
- 带外/灾备通道是否依赖与主路径共享的 DNS、认证、目录或物理设施？最后核对是什么时候？（本案例未披露其机制，这是迁移者自查的问题）
- 高危维护命令的审查/阻止工具的失效模式是否有测试？下发对象的批处理边界在哪里？
- 是否演练过"骨干/控制面全断"场景？恢复时按什么速率放量、判据是什么？
- 事件中"先怀疑自家"的假设如何被削弱？哪条观测承担了证据？

## 不可外推的条件

- 该案例发生在 Meta 的网络与服务架构（社交/Web 服务）；本案例材料不涉及 GPU/NPU 组件（不是证明其系统不存在这些组件）。数据中心骨干、自有 DNS 的 BGP 宣告、内部工具生态都是其环境特有，DNS 部署细节与物理冗余布局未披露。
- 两篇原文不含任何故障率、恢复时间统计或多环境对比；单次事件不能作为任何系统（包括 Meta 自己的当前系统）的发生率证据。
- 时间线分钟级时刻来自外部观测方且多为发现时刻，与运营方内部视角无精确对齐；因果链以运营方复盘为第一来源。
- 本库未验证任何 Meta 或 Cloudflare 系统；本文是来源整理，不是本地复现。

## 来源与未解问题

- [Meta 工程博客复盘（Janardhan，2021-10-05）](https://engineering.fb.com/2021/10/05/networking/outage-details/)
- [Cloudflare 博客外部观测（Martinho/Strickx，2021-10-04）](https://blog.cloudflare.com/october-2021-facebook-outage/)
- 本地复现状态：未复现原事件、未开展同类机制实验。
- 待确认（原文均未披露，保持 unknown）：容量评估命令内容与下发机制、审计工具缺陷机理与修复落地、骨干连接的物理布局与独立性、DNS 部署细节、带外通道失效的具体依赖链、内部工具依赖清单、恢复的完整决策过程与验收判据、全球 30 倍解析流量的测量口径。
- 迁移到 GPU/NPU 集群时的应用对象（**本库归纳**，非原案事实）：共享配置面（集群管理/网络自动化）、服务发现与 DNS、带外管理网、维护命令的审查工具与下发边界；配套检查方法见[故障模型、跨层传播与共享失效分析](fault-models-and-propagation.md)与[隔离、重试预算、降级与恢复选择](mitigation-and-recovery-principles.md)。
