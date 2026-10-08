# 第四批来源与交付记录

交付日期：2026-09-30，资料首次读取主要在 2026-09-29。写作使用 `gpt-5.6-sol / high`；集成后按用户要求派 `gpt-6-astra / xhigh` 独立验证审阅。此文件记录草稿交付，不是硬件验证。

## 本批正文

| 任务 | 正文 | 来源记录 |
|---|---|---|
| F13 | [并行策略与训练状态](../../knowledge/06-training/parallelism-and-state.md) | [训练侧核查](batch-04-training-sources.md) |
| F14 | [Checkpoint 恢复一致性](../../knowledge/06-training/checkpoint-state-consistency.md) | [训练侧核查](batch-04-training-sources.md) |
| F15 | [推理执行与 KV cache](../../knowledge/07-inference/execution-and-kv-cache.md) | [推理侧核查](batch-04-inference-sources.md) |
| F16 | [推理延迟与吞吐指标字典](../../knowledge/07-inference/latency-metrics.md) | [推理侧核查](batch-04-inference-sources.md) |

累计 15 篇正文、13 个导航/路径条目；本批新增 7 项来源，累计 40 项。正文接入训练、推理章节和相关平台/任务路径；持久化与训练恢复通过链接关联。

## 已保留的关键边界

- PyTorch 2.6 的 DCP 重分片能力限于所支持的表示、目标对象和版本条件；应用仍负责 scheduler、RNG、数据进度与训练语义。
- MindSpeed-LLM v2.2.0 固定文档与 wrapper 说明各自能力和外部依赖，不与 PyTorch 2.6/MindIO 档案拼成已支持软件栈。
- vLLM v0.14.0 的客户端和服务端指标按源码拆分；chunk、engine output update 与 token 不混用，成功过滤和 0/1 token 边界明确记录。
- vLLM Ascend v0.14.0rc1 的功能矩阵、发布限制和文档宏分别核对，不从上游支持推断 NPU 支持。
- 代码、文档和发行制品的许可范围分开；保留未核查项。未复制上游长文或图表。

## 轮末审阅

独立 astra/xhigh 初审发现 2 项 P2、2 项 P3，已全部修订并通过定向复核，见[完整审阅报告](batch-04-astra-review.md)。

- 修正默认 DCP planner 的写入者、metadata 去重与 rank-local 状态覆盖。
- 修正 vLLM HTTP 预处理、engine request arrival、输出接收与两种服务端时间源；第五批推理总览同步。
- 区分 Ascend conf substitutions 与 README requirements，保持未知配套而不否定兼容。
- 更新来源获取计划的实际已读范围与 Sphinx 配置定位。

修订后 `make check` 和 `make build` 通过；此时第五批也已集成，全库为 33 个条目、51 项来源。本批刚集成时的 28/40 是历史数量。结构检查不代替技术审阅，更不代表现场验证。

## 未执行与下一轮

没有安装、导入或执行上游软件，没有训练、推理、benchmark、故障注入、保存/恢复或 GPU/NPU 实测。实验阈值、目标模型和现场环境均未凭空填写。

下一轮按依赖补设备健康、NVIDIA 配套档案、作业准入与放置，以及训练/推理端到端总览；随后进入有证据支持的诊断指南、案例与实验设计。
