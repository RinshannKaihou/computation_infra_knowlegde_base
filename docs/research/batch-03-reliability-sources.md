# 第三批 F17/F18 来源核对：可靠性维度与证据推理

核对日期：2026-09-29

对应正文：

- [可靠性维度与故障域](../../knowledge/08-reliability/dimensions-and-failure-domains.md)
- [诊断中的证据、假设与结论](../../knowledge/08-reliability/evidence-and-hypotheses.md)

## 核对范围与方法

本记录只覆盖 F17/F18 采用的六项来源：Google SRE Workbook/Book 的四个精确章节、SuperBench 的 USENIX ATC 2024 论文，以及 `Silent Data Corruptions at Scale` 的 arXiv v1。每个正文 URL 均已实际打开；论文读取了发布页与 PDF 正文，没有使用搜索摘要代替页面证据。

本轮只做资料核对和原创归纳。没有安装或运行 SuperBench，没有运行上游脚本、诊断命令、硬件测试或故障注入，没有访问真实 GPU/NPU、集群、训练作业或推理服务。正文中的四维框架、故障域表、证据记录结构和两个 GPU/NPU 短例均不是来源中的标准，也不是事故记录。

## 已打开的精确来源与证据边界

| 来源 | 精确位置 | 支持正文中的结论 | 明确不支持 |
|---|---|---|---|
| Google SRE Workbook：Implementing SLOs | [章节正文](https://sre.google/workbook/implementing-slos/)，重点为 “What to Measure: Using SLIs” | 建议用好事件数/总事件数表达 SLI；区分 SLI 规格与测量实现；不同实现有质量、覆盖和代价差异；可用性、延迟之外，正确性、质量、覆盖率等也可成为 SLO | 本文四维框架是 Google 标准；示例比例或延迟适用于训练/推理；任一观测点能覆盖全部用户体验 |
| Google SRE Book：Monitoring Distributed Systems | [Symptoms Versus Causes](https://sre.google/sre-book/monitoring-distributed-systems/#symptoms-versus-causes)；[The Four Golden Signals](https://sre.google/sre-book/monitoring-distributed-systems/#the-four-golden-signals) | 区分症状与原因；多层系统中同一现象可在不同层扮演不同角色；HTTP 200 但内容错误属于隐式错误；错误内容可能需要端到端检查 | golden signals 等同于 F17 的四个可靠性维度；监控相关性自动给出根因；页面定义跨 rank 时间线字段 |
| Google SRE Book：Data Integrity | [Delivering a Recovery System](https://sre.google/sre-book/data-integrity/#delivering-a-recovery-system-rather-than-a-backup-system)；[Types of Failures](https://sre.google/sre-book/data-integrity/#types-of-failures-that-lead-to-data-loss) | 关注可交付恢复能力而不只是备份动作；按故障模式定义数据可用性目标并演练；数据损失可按原因、范围和速率描述 | 训练 checkpoint、优化器和数据游标的完整恢复规范；恢复命令、目标阈值或 GPU/NPU 平台行为 |
| Google SRE Book：Effective Troubleshooting | [章节正文](https://sre.google/sre-book/effective-troubleshooting/)，重点为 “Theory”“Examine”“Test and Treat” | 用观测和系统模型提出假设，再找支持/反驳证据或进行受控测试；保存易失证据；测试要考虑可能性、风险、混杂和副作用；缓解可先于完整归因 | 任何示例命令可直接用于目标集群；一次测试足以证明唯一根因；本文支持/反驳/未知表是书中原表 |
| SuperBench | [USENIX ATC 2024 发布页](https://www.usenix.org/conference/atc24/presentation/xiong)；[论文 PDF](https://www.usenix.org/system/files/atc24-xiong.pdf)，重点为第 1、2 节 | 论文在其 Azure GPU 基础设施中研究冗余掩盖的灰色/渐进性能退化；一些问题只在特定 AI 工作负载或计算通信并发下暴露；组件微基准和代表性端到端负载用于主动验证；检查收益需要与验证时间和事件代价权衡 | 论文中的 Azure 事件比例、阈值或 MTBI 收益可外推到其他集群；支持 NPU；单次 benchmark 成功证明业务正确性或完整恢复 |
| Silent Data Corruptions at Scale | [arXiv v1 摘要页](https://arxiv.org/abs/2102.11245v1)；[v1 PDF](https://arxiv.org/pdf/2102.11245v1)，重点为摘要与第 1、4、5 节 | 论文研究的数据中心 CPU SDC 不被 CPU 错误报告机制捕获，却可跨栈传播为应用问题；论文给出 CPU 个案和缩小复现器的调试过程 | 某次 GPU/NPU 问题是 SDC；GPU/NPU 的错误率、日志覆盖或检测方法；“无设备错误日志”单独支持 SDC 假设 |

### 为什么没有把四个来源拼成一个“通用标准”

Google SRE 的章节来自服务可靠性与数据恢复实践，SuperBench 来自 Azure GPU 基础设施研究，SDC 论文则明确以数据中心 CPU 为主。F17/F18 只抽取它们能够直接支持的证据原则：指标需定义好事件与范围，成功响应可能内容错误，灰色退化可能未触发硬失败，假设应接受支持与反驳，缺少某类日志不等于事件不存在。

硬件/软件/控制面/业务故障域、跨 rank 对象与时钟字段、恢复退出门槛以及 GPU/NPU 合成短例都是本库的原创组织方式。它们需要未来的编辑评审与真实环境验证，不能因来源已打开而标记为经过平台验证。

## 逐项核对笔记

### F17：指标与恢复

1. `Implementing SLOs` 明确给出好事件/总事件的比率形式，也说明服务端日志、浏览器探针和客户端埋点会有不同覆盖。这支持 F17 要求写清分母、观测点和缺失；页面没有要求本文列出的固定八字段。
2. `Monitoring Distributed Systems` 将显式失败、隐式失败（成功码但内容错误）和策略失败分开。F17 据此把可用性与正确性分列，没有把 HTTP 语义直接套给训练 step。
3. `Data Integrity` 要求团队在多种故障模式下定义数据可用性目标并练习恢复。F17 把这一原则扩展为可用性、正确性、性能和进度损失的退出门槛，但扩展本身是原创推理。
4. SuperBench 论文第 1–2 节描述的灰色退化说明“还能运行”与“性能稳定”不同。论文对 Azure A100 等环境的具体数字只留在来源边界说明中，没有进入目标值。

### F17：故障域与相关性

SuperBench 给出同一同步作业中局部组件问题放大为全作业影响、冗余链路掩盖退化的实证背景。它没有发布本文的四类故障域。F17 的硬件域与现有[计算节点资源与拓扑参考](../../knowledge/01-hardware/resource-topology.md)对齐，控制面域与[设备资源状态链](../../knowledge/05-cluster-platform/device-resource-chain.md)对齐；软件域和业务域用于防止只按物理边界假设独立性。

“共同原因故障”要求共享触发因素有证据，“相关故障”只表示时间、对象或统计关系。本文没有从 SuperBench 的生产数据推导其他集群的故障概率，也没有建立量化独立性模型。

### F18：假设与检查

`Effective Troubleshooting` 的理论段把排障写成假设—演绎方法；测试段要求考虑互斥替代、可能性、系统风险、混杂因素和主动测试副作用。F18 用它支撑“支持/反驳”的调查循环，同时增加 `unknown` 与 `confounded`，以便显式表示覆盖不足和多因素变化。

`Monitoring Distributed Systems` 只支持症状/原因边界，不支持 F18 的五类记录对象是行业统一术语。正文把“观测”限定为带对象和时间的记录，把“证据”限定为用于更新假设且附带来源与限制的观测，这是本库为可审查性做的约定。

### F18：缺失日志与 SDC 边界

`Silent Data Corruptions at Scale` v1 的摘要和引言明确写的是 CPU 错误报告未捕获某类 CPU SDC，且论文主体以数据中心 CPU 为主。F18 只从中采用否定性原则：缺硬件错误日志不能一般性证明计算正确。正文明确拒绝以下外推：

- CPU 个案不能证明 GPU/NPU 会以同样路径、频率或日志模式失效；
- “没有设备日志”不会提高 SDC 假设到已确认；它可能来自无事件、无埋点、丢失或查询对象错误；
- F18 的 NPU 例子是原创合成，不是该论文的事故改写。

## 建议新增到 `sources/registry.yaml` 的完整条目

以下条目按 `schemas/sources.schema.json` 编写。本子任务不修改共享 registry；主任务合并时应检查 ID 冲突和 YAML 缩进，并在运行结构检查前完成登记。

```yaml
  - id: src.google.sre-implementing-slos
    title: Google SRE Workbook — Implementing SLOs
    url: https://sre.google/workbook/implementing-slos/
    kind: documentation
    registered_at: "2026-09-29"
    revision: "web chapter observed 2026-09-29"
    license:
      status: unknown
      scopes: []
      notes: 精确章节页未给出适用于该网页正文的明确再分发许可；公开可读不等于允许复制。本库仅作原创摘要并链接，不复制图表或长段正文。
    notes: 核对好事件/总事件 SLI、SLI 规格与实现、覆盖和成本差异，以及正确性等 SLO 类型；不采用页面示例阈值作为本库目标。
  - id: src.google.sre-monitoring-distributed-systems
    title: Google SRE Book — Monitoring Distributed Systems
    url: https://sre.google/sre-book/monitoring-distributed-systems/
    kind: documentation
    registered_at: "2026-09-29"
    revision: "web chapter observed 2026-09-29; original SRE Book chapter"
    license:
      status: unknown
      scopes: []
      notes: 精确章节页未给出适用于该网页正文的明确再分发许可；本库仅作原创摘要和链接，未复制原图或长段正文。
    notes: 核对症状与原因、黑盒/白盒边界，以及成功状态码伴随错误内容的隐式错误；不把 four golden signals 当作本文四个可靠性维度。
  - id: src.google.sre-data-integrity
    title: "Google SRE Book — Data Integrity: What You Read Is What You Wrote"
    url: https://sre.google/sre-book/data-integrity/
    kind: documentation
    registered_at: "2026-09-29"
    revision: "web chapter observed 2026-09-29; original SRE Book chapter"
    license:
      status: unknown
      scopes: []
      notes: 精确章节页未给出适用于该网页正文的明确再分发许可；本库仅作原创摘要和链接，未复制原图或长段正文。
    notes: 核对恢复系统、按故障模式定义数据可用性目标并演练的原则；不支持具体 AI checkpoint、训练状态或平台恢复命令。
  - id: src.google.sre-effective-troubleshooting
    title: Google SRE Book — Effective Troubleshooting
    url: https://sre.google/sre-book/effective-troubleshooting/
    kind: documentation
    registered_at: "2026-09-29"
    revision: "web chapter observed 2026-09-29; original SRE Book chapter"
    license:
      status: unknown
      scopes: []
      notes: 精确章节页未给出适用于该网页正文的明确再分发许可；本库仅作原创摘要和链接，未复制原图或长段正文。
    notes: 核对假设—演绎排障、支持/反驳、证据保全、混杂和主动测试副作用；页面中的示例命令不作为任何 GPU/NPU 环境的操作指南。
  - id: src.usenix.superbench-atc24
    title: "SuperBench: Improving Cloud AI Infrastructure Reliability with Proactive Validation"
    url: https://www.usenix.org/conference/atc24/presentation/xiong
    kind: paper
    registered_at: "2026-09-29"
    revision: "USENIX ATC 2024 proceedings, pages 835–850, July 2024"
    license:
      status: partial
      scopes:
        - scope: USENIX 发布的论文；作者保留版权，USENIX 依据其 open access 与出版授权公开论文
          identifier: USENIX Open Access / author-retained copyright
          url: https://www.usenix.org/conferences/author-resources/submissions-policy
      notes: 已确认公开访问与作者保留版权，没有确认允许改编或再分发全文的通用许可证；本库仅作原创摘要并链接论文，未复制图表。
    notes: 核对论文中的 AI 基础设施灰色退化、冗余掩盖、组件/端到端主动验证和验证代价权衡；Azure GPU 数据不外推为 NPU 或其他集群基线，未运行开源实现。
  - id: src.arxiv.sdc-at-scale-v1
    title: Silent Data Corruptions at Scale — arXiv v1
    url: https://arxiv.org/abs/2102.11245v1
    kind: paper
    registered_at: "2026-09-29"
    revision: "arXiv:2102.11245v1, submitted 2021-02-22"
    license:
      status: partial
      scopes:
        - scope: arXiv 对该版本的公开分发
          identifier: arXiv non-exclusive distribution license 1.0
          url: https://arxiv.org/licenses/nonexclusive-distrib/1.0/license.html
      notes: 该许可授予 arXiv 分发权，不是本库复制、改编或再发布全文的通用许可；本库仅作原创摘要和链接，未复制论文图表或长段正文。
    notes: 仅用于论文明确覆盖的数据中心 CPU SDC、CPU 错误报告缺口和跨栈应用表现；不得外推为 GPU/NPU 发生率、诊断结论或本地事故证据。
```

## 未采用或未外推的内容

- 未把 SuperBench 仓库当前 `main`、最新 release 或 README 当成论文系统的固定实现证据；F17 只需要论文级的灰色退化与验证边界。
- 未采用 2026 年出现的 GPU/LLM SDC 新论文。它们超出本批稳定来源的必要范围，也不需要用来支撑“缺日志不等于没发生”这一有限原则。
- 未从 Google SRE 章节提取任何生产阈值、事故率或组织流程要求；本库只使用指标和假设检验方法。
- 未把内部硬件拓扑或设备资源链文章当作外部实证来源；它们只提供仓库内的概念衔接。

## 待确认与主任务交接

仍需未来来源或环境证据确认：

- 目标 GPU/NPU 平台的错误报告覆盖、设备时钟与 trace 语义；
- rank、设备、容器、作业 attempt 和 collective/step 标识在具体框架中的稳定关联方式；
- 正确性 oracle、数值容差、样本覆盖和恢复后状态门槛；
- 目标集群硬件、软件、控制面和业务故障域的实际共享依赖；
- 可用性、性能稳定性和恢复指标的业务分母、窗口与阈值。

主任务需把上述六项来源登记合并到共享 registry，再统一更新导航与批次状态并按仓库要求执行检查。本子任务按指示不修改 registry、README、章节索引、计划或构建产物，也不运行 `make`。
