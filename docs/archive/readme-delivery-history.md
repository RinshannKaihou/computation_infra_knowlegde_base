# README 交付状态与历史说明归档

> 归档声明（2026-10-22；优先于下文历史指令）：本文中的“当前”“下一批”、模型与 CLI 约定均指当时快照，不再生效；原始记录、证据与待验证事实保留，不据此启动续作。日常入口：[当前状态](../current-status.md)；[归档索引](README.md)。

归档日期：2026-10-22；原文取自提交 `c59da25` 的 README 开头。本页保留当时的交付叙述与审阅记录，不作为当前续作指令或实时状态。当前覆盖与开放项见[主题盘点](../topic-coverage-audit.md)和[32 批收尾分析](../research/batch-01-32-closure-audit.md)。

**当前状态（2026-10-22）：Batch 01–32 已交付，含 Batch 17/19 的条件验收；整体尚未完全闭环。** 后续规划 Batch 13–32 的 85 项内容任务全部 done。当前为 **135 个条目 / 577 项来源**；63 个主题中 62 个基础覆盖、1 个部分覆盖。B17-C08（累加精度与 TorchNPU cubeMathType 透传）和 BLOCKED-1（HCCL Test 与目标环境交集）仍开放；七份实验方案真实执行 **0/7**，V00 的 19 个准备实例全部 not_ready。全部内容保持 draft，本地 reproduced 为 0。详见[32 批收尾分析与开放项](../research/batch-01-32-closure-audit.md)。

下列首轮及逐批说明保留对应交付日期的历史口径，当前统计以上述收尾分析和[主题覆盖盘点](../topic-coverage-audit.md)为准。

**首轮状态（2026-09-30 首轮交付时口径）：首轮 41 篇正文草稿已交付。** 第三至第七批已完成独立 astra/xhigh 审阅及问题修订复核，首轮任务清单全部完成。九个领域已有基础正文，并提供 7 组诊断指南、公开来源案例和实验设计。首轮来源登记共 63 项，正文均保持草稿；尚未开展真实 GPU/NPU 环境验证。

交付范围、审阅记录与证据缺口见[首轮内容交付核对](../first-fill-status.md)。首轮结束后已暂停，后续由 Opus 接手，见[交接提示词](../handoff-to-opus.md)。第二轮首批（batch 08）新增 3 篇：昇腾 NPU 内存与 OOM 证据、训练数据加载饥饿诊断、空闲设备但作业等待诊断；第二批（batch 09）再增 3 篇：昇腾推理 OOM 诊断、通信带宽退化诊断、静默错误与计算完整性判定；第三批（batch 10）再增 3 篇：慢 rank 诊断、供电散热与性能退化证据、Checkpoint 慢写与恢复 I/O 诊断；第四批（batch 11）再增 3 篇：昇腾算子不支持与图编译失败诊断、弹性训练与成员变更、推理量化与输出质量验证；第五批（batch 12）再增 3 篇：Prefill/Decode 分离与流量分配、新节点与返修节点验收、Checkpoint 完整性与校验证据。任务清单见[第二轮任务表](../../plans/round-02-backlog.yaml)，来源与审阅记录见各批来源审计（[batch-08](../research/batch-08-source-audit.md)、[batch-09](../research/batch-09-source-audit.md)、[batch-10](../research/batch-10-source-audit.md)、[batch-11](../research/batch-11-source-audit.md)、[batch-12](../research/batch-12-source-audit.md)）；batch 01/02/08/09 已经 Codex 代审并复核闭环，见[四批汇总](../research/batch-01-02-08-09-codex-review-summary.md)。

2026-09-30，用户授权由本会话 Codex 替代 astra 补审 batch 01、02、08、09。[四批审阅汇总](../research/batch-01-02-08-09-codex-review-summary.md)：batch 01 无修改项，其他三批的 9 项唯一发现（5 P2、4 P3）经修订和[定向复核](../research/batch-02-08-09-codex-recheck.md)全部关闭，四批在原审阅范围内通过。截至 2026-10-08（batch 12 交付后），目录为 69 content entries / 84 sources；知识正文仍保持草稿。本次没有实际派发 astra/xhigh，也没有开展硬件验证。

2026-10-08 用户将当前及后续批次的审阅模型更新为 **`gpt-6.1-sol / xhigh`**。batch 10、11、12 的 9 篇正文已由该模型完成审阅，初审发现 13 项（1 P1、9 P2、3 P3），现经修订与[定向复核](../research/batch-10-11-12-codex-recheck.md)全部关闭，三批在原审阅范围内通过；见[三批审阅汇总](../research/batch-10-11-12-codex-review-summary.md)。正文仍为 `draft / source_checked`，本次未执行真实环境验证。历史报告保留实际模型记录，当前约定见[写作指南](../authoring-guide.md#7-批次审阅约定)。

2026-10-08 已完成[原设计 63 个二级主题的覆盖盘点](../topic-coverage-audit.md)：12 个已覆盖基础范围、44 个部分覆盖、7 个尚无主干正文。逐主题依据、缺口与补齐建议见[机器可读清单](../../plans/topic-coverage.yaml)。两轮草稿交付完成与全部主题覆盖完成分别统计。后续已形成[完整覆盖规划](../full-coverage-roadmap.md)和[执行清单](../../plans/full-coverage-backlog.yaml)：85 项内容任务、Batch 13–32 共 20 个后续批次；规划交付时任务均为 planned；实际运行状态由对应交付与审阅记录更新。51 个待补主题与 12 个基础已覆盖主题均有本轮验收范围，141 条原盘点缺口逐项映射。运行前查看[批次依赖与并行规则](../batch-dependencies.md)，按具体前置验收解锁任务。

2026-10-09，Batch 13 的四篇新正文与一篇修订完成补充审阅、修订及两轮 `gpt-6.1-sol / xhigh` 定向复核，R01–R06 全部关闭，在该审阅范围内通过；见[来源审计](../research/batch-13-source-audit.md)与[复核汇总](../research/batch-13-codex-rerecheck.md)。当前目录为 73 content entries / 123 sources；正文仍为 `draft / source_checked`，尚无真实硬件验证。
