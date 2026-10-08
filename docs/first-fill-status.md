# 首轮内容交付核对

更新：2026-09-30。首轮 41 项正文已交付，任务清单全部为 done；第三至第七批已完成独立 astra/xhigh 审阅、修订及定向复核，发现均已关闭。以下统计以本次实际文件和构建结果为准，不计模板、调研笔记或候选来源为正文。

2026-09-30 补审更新：用户授权 Codex 主助手替代 astra 审阅 batch 01、02、08、09，已完成[四批补审](research/batch-01-02-08-09-codex-review-summary.md)、修订和[定向复核](research/batch-02-08-09-codex-recheck.md)。batch 01 无修改项；其他三批的 9 项唯一发现（5 P2、4 P3）全部关闭。以下正文统计和首轮检查数字保留为首轮交付快照；当前目录为 60 entries / 71 sources，第二轮新增范围见 README 与 batch 08/09 来源审计。正文仍为 draft，本次没有硬件验证。

## 实际内容

| 主领域 | 正文数 | 当前范围 |
|---|---:|---|
| 00 全景 | 2 | 训练与推理端到端路径 |
| 01 硬件 | 2 | 节点资源/拓扑与健康证据 |
| 02 软件栈 | 7 | 分层、配套依据、GPU/NPU 文档档案及昇腾版本专题 |
| 03 通信 | 8 | collective/rank、带宽口径、HCCL 与 NCCL 超时专题 |
| 04 数据存储 | 2 | 数据供给与 checkpoint 持久化 |
| 05 集群平台 | 5 | 设备资源链、准入放置与 NPU 可见性专题 |
| 06 训练 | 8 | 并行/状态、恢复一致性、精度迁移与恢复异常专题 |
| 07 推理 | 5 | 执行/KV、指标字典与昇腾长尾专题 |
| 08 可靠性 | 2 | 维度/故障域与证据推理 |

正文类型为 13 篇概念、7 篇参考、7 篇流程、7 篇公开来源案例、7 篇实验设计。另有 9 个领域首页、2 条平台路径和 2 条任务路径。登记外部来源 63 项；来源数量不代表所有关联项目已经完整读取。

全部正文保持 `draft`。34 篇为限定范围的 `source_checked`；7 篇实验为 `not_verified`，没有任何 `reproduced` 条目。独立模型审阅与结构检查都不能代替现场验证。

## 使用入口

- Human 从[首页](../README.md)选择领域、平台或任务，再进入指南/案例/实验；同一正文只有一个主归属。
- Agent 从生成的 [catalog.json](../build/catalog.json)读取稳定 ID、路径、类型、平台、来源、适用条件与验证状态，再打开对应 Markdown。该文件是静态内容清单，不是检索服务或执行 API。
- [catalog.md](../build/catalog.md)提供生成的完整列表；[backlog](../plans/content-backlog.yaml)记录任务交付状态。`done` 表示约定内容产物已交付，不自动改变编辑或实验状态。

## 审阅与检查记录

| 批次 | 交付范围 | 证据记录 |
|---|---|---|
| 01–02 | 软件分层、配套、昇腾档案、硬件/数据/设备基础 | [第一批来源](research/batch-01-source-audit.md)、[第二批来源](research/batch-02-source-audit.md)；[01 Codex 补审](research/batch-01-codex-review.md)、[02 Codex 补审](research/batch-02-codex-review.md) |
| 03 | 通信、持久化和可靠性基础 | [来源记录](research/batch-03-source-audit.md)、[astra 审阅](research/batch-03-astra-review.md) |
| 04 | 训练状态/恢复、推理执行/指标 | [来源记录](research/batch-04-source-audit.md)、[astra 审阅](research/batch-04-astra-review.md) |
| 05 | 全流程、健康、准入放置、NVIDIA 档案 | [来源记录](research/batch-05-source-audit.md)、[astra 审阅](research/batch-05-astra-review.md) |
| 06 | 版本、设备可见性、HCCL/NCCL 四组专题 | [来源记录](research/batch-06-source-audit.md)、[astra 审阅](research/batch-06-astra-review.md) |
| 07 | 精度迁移、恢复异常、推理长尾三组专题 | [来源记录](research/batch-07-source-audit.md)、[astra 审阅](research/batch-07-astra-review.md) |

最终修订后 `make check` 与 `make build` 通过：54 content entries / 63 sources。另核对 41 项任务的稳定 ID、路径、类型、领域、平台、摘要和生成文件摘要，确认清单与源文件一致。工具仅检查结构和本地引用，技术主张与远程内容按上述独立审阅范围核对。没有修改 `src/kb/`，本轮没有增加或声称运行代码测试。

## 留给下一阶段的证据缺口

1. **可实际部署的完整环境档案。** 现有 GPU/NPU 档案是固定资料样板；HDK、机型、固件、OS、镜像摘要、各用户态组件与模型的完整交集还未现场核实，不能直接选作生产安装清单。
2. **真实验证。** 七项实验都有准备、影响、对照和判据，但都未执行。后续应先取得匹配环境与已有执行授权，再补受控证据；不从公开 Issue 推导本地通过。
3. **未闭环案例。** 已保留缓解、自动回复、补丁合入、stale/completed 关闭与真实复验之间的区别。带来源的未解决问题可以用于学习调查方法，不是已证明有效的处方。
4. **其余内容覆盖。** 供电散热、OS/NUMA、存储实现、算子/编译、慢 rank、强化学习、推理发布与容量等仍有空白。首轮覆盖九章和七组优先场景，不代表全部二级主题完成；扩展顺序见[填充计划](population-plan.md)。
5. **产品化和维护。** 目前是 Markdown/YAML 与静态清单，没有网站、向量检索、知识 API、工具执行器或独立诊断评测系统。已有公开复盘不能再冒充未见评测集。
6. **发布许可。** 来源表区分文档、代码、产品包和用户讨论；仓库尚未选择统一对外许可。现阶段成果以原创归纳与精确链接为主。

优先后续工作是选择一套真实昇腾环境，完成制品与拓扑档案、设备可见性和最小功能基线，再按实际故障与资源条件推进通信、数值、恢复及服务负载实验。其他 NPU 平台需要各自的官方支持与执行证据，不能继承昇腾条目中的参数和阈值。

## 交接与暂停

首轮结束后已按用户要求暂停，没有启动第八批。后续撰写交由 Opus，完整上下文、规范、审阅要求和建议任务见[交接提示词](handoff-to-opus.md)。没有创建自动续作或定时任务。
