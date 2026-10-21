---
id: reliability.diagnostic-evaluation-method
type: reference
domain: reliability
status: draft
title: 诊断评测方法规范
platforms: [generic]
source_refs:
  - src.arxiv.rcacopilot-2305.15778
  - src.arxiv.cloud-opsbench-2603.00468
  - src.google.sre-effective-troubleshooting
updated_at: "2026-10-21"
summary: 定义诊断能力的评测框架：数据划分（train/dev/held-out 与外置隔离）、来源时间截断与冻结、评审角色、泄漏/污染控制与答案证据强度分级；评测维度不止根因命中率——引用精度、事实/平台边界、假设区分力、下一项检查的成本与有效性、错误处置、abstention 与恢复验证；公开教学题组不构成独立 holdout，独立评测集由 V12 外置管理。
related_ids:
  - reliability.evidence-and-hypotheses
  - reliability.diagnostic-evaluation-fixtures
  - reliability.postmortem-and-knowledge-update
  - reliability.test-design-and-coverage
verification:
  status: source_checked
  evidence_refs:
    - src.arxiv.rcacopilot-2305.15778
    - src.arxiv.cloud-opsbench-2603.00468
  notes: "本批核读 RCACopilot（arXiv:2305.15778v4 摘要与登记口径）与 Cloud-OpsBench（arXiv:2603.00468v1 全文：452 案例构造、State Snapshot 范式、A@k/TCR/轨迹对齐/工具使用/稳健性指标）。本文是方法规范，没有评测系统实现、没有运行任何测试、没有分数。"
---

# 诊断评测方法规范

本库的诊断方法（[证据与假设](evidence-and-hypotheses.md)、各域 triage 正文）写得对不对、Agent 用了它们之后判断质量如何，需要**评测**来回答。本文定义评测的方法规范：数据怎么划分与隔离、泄漏怎么防、答案的证据强度怎么分级、评什么维度。配套的公开教学题组见[诊断评测公开题组](diagnostic-evaluation-fixtures.md)——它只是 train/dev 性质的公开材料，**不是独立 holdout**。

## 一、数据划分与隔离

| 集合 | 用途 | 来源与隔离要求 |
|---|---|---|
| train | 方法与提示词开发的材料 | 公开复盘、已入库 case、合成教学例——**任何进入 knowledge/ 的材料自动成为 train 侧**（对模型和人都可见） |
| dev | 调参与迭代判读 | 与 train 同源但冻结判据；公开题组（fixtures 正文）承担此角色 |
| held-out | 独立评测 | **输入与答案一律外置管理**（不入库、不进对话记录），按案例家族/软件版本/发生时间三个维度与 train 侧隔离：同一案例家族（同根因模板）、同一版本组合、同一时间窗的案例不得同时出现在 train 与 held-out |

三条隔离纪律：

1. **来源时间截断**：held-out 案例的发生时间晚于（或家族上独立于）train 侧全部材料，防止“复盘已在公开渠道流传”造成的答案泄漏；
2. **冻结**：评测开始前冻结知识库版本（commit）、模型/配置与评分规则；任何一项变更即视为新评测轮，旧分数不可比；
3. **外置答案**：held-out 的输入与答案由 V12 工作包（[plans/validation-backlog.yaml](../../plans/validation-backlog.yaml)）按“有授权且可脱敏的独立案例及评测资源”另行获取与审查；**在 V12 交付前，本库不存在独立评测集，也不宣称任何独立评测结论**。

公开研究中的同型做法可作参照：Cloud-OpsBench 用故障注入构造 452 个案例并以“状态快照”冻结现场保证 100% 可复现（[arXiv:2603.00468 §3.2](https://arxiv.org/abs/2603.00468)）；RCACopilot 用一年的真实 Microsoft 事故数据评测并报告 RCA accuracy 至 0.766（[arXiv:2305.15778](https://arxiv.org/abs/2305.15778)）——两者都声明了数据范围，但没有哪个公开基准能替代本地环境的独立 holdout。

## 二、评审角色与污染控制

| 角色 | 职责 | 与编写者的关系 |
|---|---|---|
| 出题者 | 从固定证据构造案例、写答案与 rubric | 不得同时担任被评方法/提示词的作者 |
| 被评对象 | 使用知识库（或其 Agent）作答 | 不接触答案与评分规则细节 |
| 评分者 | 按 rubric 逐维打分；对 abstain 单独判定 | 可与出题者同一，须与被评对象隔离 |

污染（模型预训练已见过案例原文）无法根除，只能控制与披露：记录每个案例的公开渠道与首发时间；对疑似已进预训练语料的案例标注“污染风险”，结论分层报告；换卷策略——按案例家族准备等价第二套（不同版本/不同平台实例），主卷泄漏时启用；评测报告必须写明每卷的来源家族分布。

## 三、答案的证据强度分级

一个案例的“标准答案”本身要先分级，防止用弱证据答案评出虚高分数：

| 级别 | 定义 | 可支持的判分 |
|---|---|---|
| A（证据闭合） | 根因有固定公开证据（复盘自述、修复 commit、可复现实验） | 可判“根因识别正确/错误” |
| B（多方一致） | 运营方＋外部观测双证据互洽（如 Meta 2021-10-04） | 可判根因，但表述须含证据链 |
| C（规则命中） | 只有工具规则/诊断输出支持（如 FaultDiag 报告） | 只能判“候选假设提出正确”，不得判根因 |
| U（无法判定） | 证据不足以在候选间区分 | **正确答案是 abstain＋列出需要的下一项证据** |

U 级案例是必需品：评测不含 U 级会训练出“逢题必答”的坏习惯，与[证据与假设](evidence-and-hypotheses.md)的纪律相反。

## 四、评测维度

只评“根因命中率”或文字流畅度是已知反模式。七个维度（rubric 逐项打分，每维 0–2：未做到/部分/做到）：

| 维度 | 评什么 | 反例（0 分形态） |
|---|---|---|
| 引用精度 | 关键主张是否落在精确来源锚点（页/节/commit/文件行） | 引用只到网站首页；编造锚点 |
| 事实/平台边界 | 是否写明版本、平台、统计口径的适用范围 | 把 Azure GPU 数字说成通用阈值；NPU 侧用 CPU 研究代答 |
| 假设区分力 | 支持证据是否真的区分候选假设 | 列出两个假设但用同一证据“同时支持” |
| 下一项检查 | 提出的检查是否低成本、有区分力、说明预期读数 | “重启试试”；与候选无关的全量扫描 |
| 错误处置 | 隔离/重试/降级/回滚选择是否按[处置选择](mitigation-and-recovery-principles.md)六字段声明影响 | 无预算的同步重试；未声明副作用的注入式动作 |
| abstention | U 级案例是否正确弃答并给出补证清单 | 强行归因到某硬件 |
| 恢复验证 | 是否给出恢复完成的判据（不是“进程起来了”） | 无健康窗口判据即宣布恢复 |

Cloud-OpsBench 的过程指标与本文维度同向，可作实现参照：除 Top-k 准确率与任务完成率外，它评轨迹对齐、工具相关性/覆盖（Relevance/Coverage）、诊断效率（MTTI/Steps），并定义三种失败模式指标——无效动作数（IAC，参数幻觉/非法调用）、冗余动作率（RAR）、零工具诊断率（ZTDR，不取证据直接下结论）（[§5 指标定义](https://arxiv.org/abs/2603.00468)）。ZTDR 即“abstention 反面”的工具化度量。

## 五、公开题组的角色边界

[公开题组](diagnostic-evaluation-fixtures.md)纳入 knowledge/ 后**只能算公开教学与检索回归材料**：用途是教学演示、验证知识库导航/检索能否定位正确正文、以及 dev 轮迭代判读；**不得标注或宣传为独立 holdout**，不得用它宣布“诊断能力已达 X%”。独立评测结论只能来自 V12 外置集。本文与题组都不构成评测系统的实现——不存在运行中的评测框架、分数榜或 API。

## 六、适用边界与待确认

- 评测维度的权重分配（七维等权或按场景加权）未定，待 V12 评审时随评分规则一并冻结；
- “污染风险”的量化检测（如 n-gram 探测）未登记原始方法来源，当前只按披露纪律执行；
- RCACopilot 的正式发表版（arXiv v4 之外）未核对；Cloud-OpsBench 的代码/数据集（GitHub LLM4Ops/Cloud-OpsBench）未读取，仅按论文正文引用。

## 来源核对范围

- [RCACopilot / Automatic RCA via LLMs for Cloud Incidents, arXiv:2305.15778v4](https://arxiv.org/abs/2305.15778)：本批核对摘要与登记口径——一年期真实 Microsoft 事故数据、RCA accuracy 至 0.766、诊断信息采集组件在生产使用四年以上。全文细节未逐节核读，仅引用摘要级事实。
- [Cloud-OpsBench, arXiv:2603.00468v1](https://arxiv.org/abs/2603.00468)（CC BY 4.0）：本批全文核读——452 案例与 40 故障类型、State Snapshot 范式（确定性数字孪生、冻结现场）、K8s v1.31 测试床＋ChaosBlade 注入、指标定义（A@k、TCR、Trajectory Alignment、Relevance/Coverage、MTTI/Steps、IAC/RAR/ZTDR）、反猜测设计（搜索空间与证据链）。仅归纳，不复制其数据。
- [SRE Book, Ch.12 Effective Troubleshooting](https://sre.google/sre-book/effective-troubleshooting/)（既有登记）：假设—演绎与证据保全，是各维度的方法底座。
- 逐条主张与读取范围见[第三十批 T08-08 来源记录](../../docs/research/batch-30-t08-08-sources.md)。
- 待确认：V12 独立案例集的获取授权与脱敏审查；维权重与评分细则冻结版本。
