# Batch 10、11、12 审阅汇总（gpt-6.1-sol / xhigh）

审阅与复核日期：2026-10-08。**三批 9 篇正文的审阅、修订和定向复核已完成，13 项唯一发现全部关闭；三批在原审阅范围内通过。** 用户在初审后要求“直接进行修正”，本会话修订了 8 篇正文及关联研究/登记，供电散热篇未修改。逐项关闭依据和修订后身份见[定向复核](batch-10-11-12-codex-recheck.md)；初审问题与输入身份保留为历史。

## 模型约定与执行身份

用户要求将约定中的“gpt-6-sol 审阅”改为“gpt-6.1-sol 审阅”。本次检索仓库未发现待替换的 `gpt-6-sol` 审阅约定，保存的旧约定实际为 `gpt-6-astra / xhigh`；据本次用户更新，将**当前及后续批次约定统一为 `gpt-6.1-sol / xhigh`**，不把旧模型执行历史改写成新模型。

本次审阅者为 Codex 主助手，当前会话运行上下文确认 `model: gpt-6.1-sol`、`reasoning_effort: xhigh`；原正文编写者为 Opus，修订与定向复核由同一 Codex 会话分阶段完成。审阅者完整读取九篇正文、对应研究记录与来源审计，取得报告所列精确上游证据；修订后再次对照关闭条件与固定证据。本次未派发 astra 或子代理，没有将旧替代复查冒充本次模型审阅。当前规则已同步至 [AGENTS](../../AGENTS.md)、[写作指南第 7 节](../authoring-guide.md#7-批次审阅约定)、[填充计划](../population-plan.md#9-内容验收与审核分工)、[Opus 交接](../handoff-to-opus.md)和[第二轮任务表](../../plans/round-02-backlog.yaml)。

## 结论与发现清单

| 批次 | 正文数 | 初审 P1 | 初审 P2 | 初审 P3 | 当前状态 | 完整报告 |
|---|---:|---:|---:|---:|---|---|
| 10 | 3 | 0 | 2 | 0 | 2 项关闭，原范围内通过 | [batch-10](batch-10-codex-review.md) |
| 11 | 3 | 1 | 3 | 1 | 5 项关闭，原范围内通过 | [batch-11](batch-11-codex-review.md) |
| 12 | 3 | 0 | 4 | 2 | 6 项关闭，原范围内通过 | [batch-12](batch-12-codex-review.md) |
| 合计 | 9 | 1 | 9 | 3 | 13 项关闭，0 项开放 | [定向复核](batch-10-11-12-codex-recheck.md) |

P1 为核心诊断流程与固定实现直接矛盾；P2 影响归因、配置或验收判断；P3 为证据登记、未证实的对应关系或任务映射问题。以下为初审发现及修订后状态，每项只计一次；原位置、证据与关闭条件见初审报告，实际关闭依据见定向复核。

| ID | 优先级 | 发现 | 状态 |
|---|---|---|---|
| B10-C01 | P2 | RAS 未显示离群组不能证明全体 rank 变慢 | CLOSED |
| B10-C02 | P2 | writeback 等待不能排除存储后端，后台阈值也不是唯一触发条件 | CLOSED |
| B11-C01 | P1 | TorchNPU 同一固定文件实际注册 CPU fallback，正文却断言不存在 | CLOSED |
| B11-C02 | P2 | 指南要求显式启用 eager，不能作为引擎自动回退行为 | CLOSED |
| B11-C03 | P2 | torchrun CLI 默认重启 0 次，与 WorkerSpec API 默认 3 次不同 | CLOSED |
| B11-C04 | P2 | INT8 文档在 SM 7.5 支持边界上自相矛盾，正文未标冲突 | CLOSED |
| B11-C05 | P3 | registry 仍把 14 个方法页加 README 记为 15 个方法页 | CLOSED |
| B12-C01 | P2 | DCGM 非零退出码可以表示诊断已执行且检出失败 | CLOSED |
| B12-C02 | P2 | 节点恢复缺少验收门槛，AICore 资源前提和收尾动作遗漏 | CLOSED |
| B12-C03 | P2 | DCP 默认数据文件按分桶组织，并非每个 request 一个文件 | CLOSED |
| B12-C04 | P2 | PD 不提升吞吐的版本声明不意味着评估时排除吞吐 | CLOSED |
| B12-C05 | P3 | connector 注册表不证明 Offloading/LMCache 替代旧共享存储接口 | CLOSED |
| B12-C06 | P3 | Checkpoint 完整性研究记录误标为 R2-12，应为 R2-15 | CLOSED |

## 审阅输入身份

以下为初审开始时记录的完整文件 SHA-256，固定发现对应的输入；修订后的 SHA-256 另见[复核记录](batch-10-11-12-codex-recheck.md)，不要将下表当作修订后身份。稳定 content ID 未改变，初审的行号位置也只对应此输入。

| 批次 | 正文 / 稳定 ID | 输入 SHA-256 |
|---|---|---|
| 10 | [慢 rank](../../knowledge/06-training/slow-rank-triage.md) / `training.slow-rank-triage` | `92847ae72fdd301a82029f69a0a9b55312ae9c32cdb4d5676d0456add5bb42ae` |
| 10 | [供电散热](../../knowledge/01-hardware/power-thermal-evidence.md) / `hardware.power-thermal-evidence` | `27136987c5a74e1a7c54eb79c11130bdf87296d06cf0396afcb26971032ea1ee` |
| 10 | [Checkpoint I/O](../../knowledge/04-data-storage/checkpoint-slow-io-triage.md) / `data-storage.checkpoint-slow-io-triage` | `8e694480cd710312ed3aa14bb4a06155c032fd850d14c792f638fe4dbf01a3b1` |
| 11 | [算子/图编译](../../knowledge/02-software-stack/ascend-op-graph-failure-triage.md) / `software-stack.ascend-op-graph-failure-triage` | `a129e788789a39cd40b2e6bd7c7c41705913ba2d38ba943ef9d2a24e290a210e` |
| 11 | [弹性训练](../../knowledge/06-training/elastic-training-and-membership.md) / `training.elastic-training-and-membership` | `053ae7c8351bb621ab266a3cb3dee14931d8a1e1074b892e4f63563758145743` |
| 11 | [量化质量](../../knowledge/07-inference/quantization-and-quality.md) / `inference.quantization-and-quality` | `161700923bcdc551d029a0ccfd0810cbbf2adbc12d0de73814a894762e7698c2` |
| 12 | [PD 分离](../../knowledge/07-inference/pd-disaggregation.md) / `inference.pd-disaggregation` | `951de847b709da49a1f442b47896a23fbe49823c9f4af58c25cda63970d7c6c7` |
| 12 | [节点验收](../../knowledge/01-hardware/node-acceptance-triage.md) / `hardware.node-acceptance-triage` | `60eee2286827fb29247305a3eea4fe47952c7ebcddab0a18588beb197dcf5efb` |
| 12 | [Checkpoint 完整性](../../knowledge/04-data-storage/checkpoint-integrity-evidence.md) / `data-storage.checkpoint-integrity-evidence` | `3fe63f7e28e2da56a09c6d38363156e159b6620ed555c7f91dd664f300138d00` |

## 证据范围与检查边界

各报告分别列明本次重新取得的固定 commit 文件或官方页面，沿用既有来源登记，未新增外部来源。固定源码、版本化文档、latest 页面和本库方法推论分别理解。未完整重读的外部材料、失败的页面获取和未执行的实验已在各报告记录，不由邻近证据补成已验证。

本次不运行设备诊断、作业、部署、压测、存储修复或损坏注入，不产生真实环境验证结果。九篇正文继续 `status: draft` 与限定范围 `verification.status: source_checked`，没有 `reproduced`。第二轮 backlog 的 `done` 仅表示草稿交付，不能据此推断审阅发现已关闭。

2026-10-08 初审收尾检查（修订前）：`make check` 与 `make build` 均通过，69 content entries / 84 sources，当时九篇正文 SHA-256 与原始元数据未变。此记录只说明初审交付身份；修订后的检查与清单核对另记于[复核报告](batch-10-11-12-codex-recheck.md)。未修改 `src/kb/`，本次不要求开发回归测试。

2026-10-08 修订后收尾：`make check` / `make build` 均通过（69 content entries / 84 sources）。已核对九篇当前清单的全部元数据、路径和 SHA-256，并确认 13 项均 CLOSED；实际修订 8 篇正文，9 篇均保持 `draft / source_checked`，修订后文件身份见复核报告。

结构检查只验证结构与本地引用。技术关闭结论来自逐项对照修订内容、精确来源与关闭条件；它不证明环境兼容或现场运行成功。SM 7.5 支持、NPU 图模式配套、工具覆盖对比等未知条件仍按正文保留。
