---
id: reliability.postmortem-and-knowledge-update
type: procedure
domain: reliability
status: draft
title: 事故复盘、来源更新与知识维护
platforms: [generic]
source_refs:
  - src.google.sre-postmortem-culture
  - src.google.sre-managing-incidents
  - src.google.sre-effective-troubleshooting
  - src.google.sre-monitoring-distributed-systems
  - src.ascend.faultdiag-v26.1.1
  - src.meta.oct4-2021-postmortem
  - src.cloudflare.oct-2021-facebook-outage
updated_at: "2026-10-21"
summary: 把一次事故的证据组织成复盘记录（影响、时间线、实体/版本/工作键、假设支持/反驳/未知、处置与遗留风险），并定义证据如何转化为知识库的来源案例、诊断修订与失效复核：更新→受影响条目→修订→定向审阅→导航的追溯链，以及版本变更/上游冲突/链接失效/验证反例四类复核触发与弃用规则。
related_ids:
  - reliability.evidence-and-hypotheses
  - reliability.correlated-failure-source-case
  - reliability.reliability-metrics-and-recovery-loss
  - reliability.diagnostic-evaluation-fixtures
applicability:
  environment_refs: []
  notes: "流程框架适用于任何 GPU/NPU 环境的事故证据整理；具体采集工具与字段按现场已部署的监控/日志系统确定，当前无已登记环境档案。"
verification:
  status: source_checked
  evidence_refs:
    - src.google.sre-postmortem-culture
    - src.google.sre-managing-incidents
    - src.ascend.faultdiag-v26.1.1
  notes: "本批核读 SRE Workbook 第 10 章 Postmortem Culture 与 SRE Book 第 14 章 Managing Incidents 全文（CC BY-NC-ND 4.0，仅归纳）；FaultDiag v26.1.1 固定 commit 的诊断输出结构作为自动化诊断输入的样板。本文是流程设计，未在任何真实事故上执行。"
---

# 事故复盘、来源更新与知识维护

事故的价值在两处：恢复服务时保住的证据，和事后把证据转成可复用的知识。本文是操作流程：**怎么记录一次事故**（第一节），**怎么把它（或一次公开事件、一次上游更新）转化为知识库修订**（第二、三节），以及**知识什么时候必须复核或弃用**（第四节）。目标读者是负责复盘的工程师和维护本知识库的角色。

Google SRE 的两条总原则贯穿全程：**“先止血、恢复服务、并为根因分析保全证据”**（[Managing Incidents](https://sre.google/sre-book/managing-incidents/)）；**复盘针对“发生了什么”而不是“谁造成的”**——归责化的复盘让人规避风险、掩盖事实，无责（blameless）文化才产出可靠系统（[Postmortem Culture](https://sre.google/workbook/postmortem-culture/)）。

## 一、事故记录：证据结构

### 事件期间的记录（影响复盘质量的动作）

在事件进行中就要为复盘留下原料（SRE：指挥官维护一份**实时事件文档**，可多人并发编辑、关键信息置顶、事后保留用于复盘）：

| 动作 | 要点 | 依据 |
|---|---|---|
| 尽早宣布事件 | 需要第二团队介入、用户可见、或分析一小时无解即宣布；宁可宣布后快速关闭 | Managing Incidents |
| 角色与指挥 | 指挥（持有全局状态、未授权职责默认归其保留）、操作（**唯一**改动系统的组）、沟通（对内对外周期更新）、规划（长期事项、交接、记录系统偏差供回退） | 同上（职责分离让个人更有自主性，不是官僚） |
| 决策留痕 | 每个动作记下：时间、执行者、动作、结果；改过的配置/开关单独列表（回退依据） | 同上 |
| 保全证据 | 转储前先拷贝环形缓冲/飞行记录（如 NCCL flight recorder 在 watchdog 超时自动转储的机制）、日志、计数器快照；**清缓存/重启前采集** | Effective Troubleshooting（既有登记） |

### 复盘记录的必填字段

事件结束后（SRE 模板：一周内发布，拖四个月是反例），按本库扩展的字段填写——比 SRE 通用模板多出“实体/版本/工作键”“采集覆盖”“假设三分”三组，服务于知识库转化：

| 字段组 | 内容 | 纪律 |
|---|---|---|
| 影响 | 受影响对象与规模、四维目标各自的影响（参照[可靠性统计](reliability-metrics-and-recovery-loss.md)的记账：有效产出损失、失败/取消请求、降级时长）、检测方式、恢复方式 | 量化用当次口径，不追改 |
| 时间线 | 统一时钟源下的逐条事件：根因时刻（可确定时）、首个异常观测、检测、宣布、各处置动作、恢复判据达成；**事件发生时刻与外部发现时刻分开标注** | 每条带证据指针；推测性条目显式标注 |
| 实体/版本/工作键 | 受影响与参与对象的身份键：硬件型号/批次、驱动/固件/框架/镜像版本、作业 ID、rank 拓扑、模型/checkpoint 版本 | 版本错记会让后续“版本变更触发复核”失效 |
| 采集覆盖 | 哪些对象/时段有数据、哪些没有、为什么（未部署/滚动覆盖/被覆盖） | 覆盖缺口不是复盘的失败，是结论的边界 |
| 假设三分 | 对每个候选根因：**支持证据 / 反驳证据 / 未知**；结论按 confirmed / suspected / unknown 归档 | **不凭结果倒推根因**：恢复了≠修对了；关闭的 Issue≠修复（既有登记口径） |
| 处置与恢复 | 采取的隔离/重试/降级/回滚/重启动作及效果；自动化占比；人工介入点 | 与[处置选择](mitigation-and-recovery-principles.md)六字段对齐 |
| 遗留风险 | 未解决假设、临时缓解的到期条件、暂缓的行动项及负责人 | 行动项要有单一负责人、优先级、类型（prevent/mitigate/detect/repair/investigate）与跟踪载体，否则会重复出事故（SRE） |

自动化诊断输出（如 Ascend FaultDiag 的诊断报告：根因节点、首错节点、根因节点链、故障分类、建议方案、关键日志、传播链）是**候选假设的输入**，不是复盘结论——规则匹配不等于根因确认（固定 v26.1.1 文档口径，见[静默错误](silent-errors-and-integrity.md)平台证据表）。

### 三类材料必须区分

| 类别 | 定义 | 进入知识库的方式 |
|---|---|---|
| 本地事故 | 本库辖内环境发生、有一手证据的事件 | 复盘记录→（脱敏后）`case` 条目；敏感日志/大附件用管理引用，**不复制凭证或现场可变状态** |
| 公开来源案例 | 运营方复盘或外部观测等固定公开证据 | 登记来源→`case` 条目并标“来源整理”，如[相关故障来源案例](correlated-failure-source-case.md) |
| 合成教学例 | 为教学构造的示例 | 显式标注“合成”；只验证方法/规则，不证明任何发生率（见[诊断评测题组](diagnostic-evaluation-fixtures.md)） |

### 公开复盘映射示例

以 Meta 2021-10-04 断网为例（运营方复盘＋外部观测双证据，已在库），演示字段映射：影响＝多服务不可用（运营方口径）＋全球多地 DNS/BGP 解析失败（观测方口径）；时间线＝配置命令下发（事件时刻）→ 撤销未生效 → 全球 DNS 服务器停播（**外部发现时刻**）→ 修复与逐步恢复；实体/版本＝骨干路由器配置系统与审计工具（按复盘口径）；假设三分＝根因 confirmed（运营方自述）；遗留风险＝维护期期间第二起故障叠加（复盘自述）。完整推理过程见[相关故障来源案例](correlated-failure-source-case.md)——该条目即本节流程的已交付实例。

## 二、从证据到知识库：追溯链与责任

一次 source / release / patch / case 的更新，沿以下链路流转；每步有明确责任角色（编写者＝起草修订的人；审阅者＝按批次约定执行定向技术审阅的独立角色；登记＝在 registry/目录登记的人——可以是同一人但角色分开记录）：

```text
上游变化（四类触发，见第三节）
  └─ 1 证据登记：来源进 sources/registry.yaml（精确页/版本/commit＋许可）；
       本地事故先落 case/experiment 条目（含采集覆盖与假设三分）
       └─ 2 影响定位：沿 source_refs 反查受影响 content IDs；
            case 类更新还要反查 related_ids 与域 index
            └─ 3 修订：正文最小修改——修正主张、收窄边界、更新来源锚点；
                 主张与来源记录（docs/research/*-sources.md）同步改，不留旧句
                 └─ 4 定向技术审阅：按批次审阅约定重读正文与精确上游证据，
                      记录发现 ID/优先级/关闭条件；开放高优先级未解决不得宣布通过
                      └─ 5 导航与账面：域 index、topic-coverage、
                           roadmap/batch 审计同步；统计重算
```

责任要点：步骤 2 的反查以 `source_refs` 为准，**正文内联引用了但 source_refs 未登记的来源是流程缺陷**，发现即补登记；步骤 4 的审阅模型与执行方式按 authoring-guide 的批次约定，**实际使用的模型如实记录**（包括历史轮次不追改）；模型审阅、来源核对、真实环境实测三种证据分别记录，互不冒充。

## 三、复核触发：什么时候必须重查既有知识

| 触发 | 信号源 | 必查内容 |
|---|---|---|
| 版本变更 | 来源方发布新 release/文档版本、registry 里 pinned commit/tag 之外出现新稳定版 | 该来源支撑的全部主张：仍成立/需改写/已失效；历史案例按“固定版本维护”原则**不追改原文**，只加后续版本注记 |
| 上游冲突 | 同一主张出现第二个来源且口径不一致（如不同语言文档、文档 vs 源码分支） | 记录所采信的位置与未解决差异（既有“文档概括 vs 实现分支”口径）；不可静默择一 |
| 链接失效 | registry 或正文引用的精确 URL 失效 | 先找同版本归档（版本化页面、固定 commit、PDF）；换版本＝版本变更触发，不是简单改 URL |
| 验证反例 | 新的本地实验/事故或新公开证据与既有正文矛盾 | 优先假设正文有错；修订时保留反例证据；被推翻的结论按第四节弃用或收窄 |

## 四、弃用规则

结论被推翻或被替代条目覆盖时：

1. **保留稳定 ID**：条目不删除；`status: deprecated`，正文顶部加替代说明与弃用原因；
2. **指向替代**：说明由哪个条目/来源取代、取代的证据是什么；
3. **保留历史真实**：被弃用正文引用的历史审阅模型、当时来源版本原样保留——“按当时证据是对的”与“现在不再采信”并存；
4. **导航同步**：域 index 移入弃用区（或移除链接但保留条目），topic-coverage 的 evidence_refs 更新，避免读者经旧路径到达已弃用结论。

## 五、停止条件与完成判据

**停止（复盘暂不宣布完成）**：关键时间线无证据支撑且无采集可能（记录为 unknown 后可完成，但相关结论标 suspected/unknown）；行动项无负责人或无跟踪载体。

**完成判据**：复盘记录字段齐全且假设三分就位；受影响的库内条目已完成第二节全链路（登记→定位→修订→审阅→导航）；弃用（如有）符合第四节。**一次复盘完成不等于根因已证实**——confirmed 只授予证据闭合的假设。

**本流程不创建的东西**：不实现自动化复盘、网站、API 或定时任务（SRE 提到的工具化实践——模板自动填充、可搜索复盘库、行动项跟踪看板——是方向参考，本库只登记口径，不声明实现）。

## 六、适用边界

- 事件期间的指挥/角色结构源自 SRE 对服务运维的实践；迁移到训练集群时，“操作组唯一改动系统”对应为“唯一持有作业/集群变更权限的组”，语义不变、载体自定。
- 本文的追溯链与触发规则为本库原创设计（对齐 AGENTS.md 与 authoring-guide 既有约定），SRE 章节提供的是复盘文化与模板口径依据。
- 未包含：与外部厂商的联合复盘流程、法律责任边界、客户通报模板——需要时另行立文。

## 来源核对范围

- [SRE Workbook, Ch.10 Postmortem Culture: Learning from Failure](https://sre.google/workbook/postmortem-culture/)（CC BY-NC-ND 4.0）：本批全文核读——无责原则与组织激励、好坏复盘对照、模板字段（摘要/影响/根因与触发/时间线/经验教训/行动项表）、行动项负责人/优先级/类型/跟踪、复盘阅读会与 Wheel of Misfortune。仅归纳。
- [SRE Book, Ch.14 Managing Incidents](https://sre.google/sre-book/managing-incidents/)（CC BY-NC-ND 4.0）：本批全文核读——四大角色与递归职责分离、实时事件文档要求、尽早宣布、明确交接、演练；“止血、恢复、保全证据”。仅归纳。
- [Ascend FaultDiag v26.1.1 固定 commit 文档](https://github.com/Ascend/mind-cluster/blob/44385c13d7b1d87def35f1604e8be4d16de6ca4e/docs/zh/faultdiag/ascend-faultdiag/05_usage/04_fault_diagnosis.md)：诊断报告结构与根因节点/传播链字段（作为“自动化输出=候选假设”的样板）。
- [Meta 2021-10-04 复盘](https://engineering.fb.com/2021/10/05/networking-traffic/outage-details/) 与 [Cloudflare 外部观测](https://blog.cloudflare.com/october-2021-facebook-outage/)（既有登记，Batch 29 全文核读）：公开复盘映射示例的素材。
- 逐条主张与读取范围见[第三十批 T08-07 来源记录](../../docs/research/batch-30-t08-07-sources.md)。
- 待确认：本地事故的第一份真实复盘（当前无本地事件）；行动项跟踪载体的具体选型（当前以条目内表格承载）。
