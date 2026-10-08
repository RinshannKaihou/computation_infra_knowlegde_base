# 第十批来源与交付记录

**最新审阅状态（2026-10-08）：** 用户约定的 `gpt-6.1-sol / xhigh` 审阅、修订与定向复核已完成；2 项 P2 全部关闭，本批在原审阅范围内通过，见[本批报告](batch-10-codex-review.md)、[定向复核](batch-10-11-12-codex-recheck.md)和[三批汇总](batch-10-11-12-codex-review-summary.md)。旧替代复查与集成计数保留为历史，此前 astra 审阅义务已由用户新约定替代。

集成日期：2026-09-30。第二轮第三批（round-02 backlog 的 R2-07/08/09）由 Opus 编写；研究由三个只读子代理完成，关键锚点经子代理按固定 commit 原文件核对。全部保持 draft；两篇 procedure 与一篇 reference 均为限定来源范围的 source_checked。

## 本批正文

| 任务 | 正文 | 类型 |
|---|---|---|
| R2-07 | [慢 rank 诊断指南](../../knowledge/06-training/slow-rank-triage.md) | procedure |
| R2-08 | [供电、散热与性能退化证据](../../knowledge/01-hardware/power-thermal-evidence.md) | reference |
| R2-09 | [Checkpoint 慢写与恢复 I/O 诊断指南](../../knowledge/04-data-storage/checkpoint-slow-io-triage.md) | procedure |

来源记录：[慢 rank](batch-10-slow-rank-sources.md)、[供电散热](batch-10-power-thermal-sources.md)、[checkpoint I/O](batch-10-checkpoint-io-sources.md)。任务清单：[plans/round-02-backlog.yaml](../../plans/round-02-backlog.yaml)。

## 来源变化

新增 5 项登记（总计 76 项）：

- `src.kernel.docs-sysctl-vm-v6.16`：Linux v6.16 固定 commit 的 dirty/writeback 语义。
- `src.nvidia.nvidia-smi-docs-latest-2026-09-30`：Clocks Event Reasons 语义（latest 可变）。
- `src.nvidia.dcgm-field-identifiers-latest-2026-09-30`：DCGM 字段定义页（latest 可变）。
- `src.huawei.npu-smi-atlas-a2-edge-24.1.rc1-pdf`：边缘产品线 npu-smi 命令参考（只核对目录；不外推训练线）。
- `src.pytorch.tutorial-async-checkpoint-2026-09-30`：异步保存教程（动态页，含 2.9 内容，限定引用）。

扩充 11 项既有登记 notes：processgroupnccl-env-2.8、distributed-2.8、nccl-user-guide-2.27.5、dcgm-exporter-metrics、dcgm-v3.3.9、dcgm-health-monitoring、dcgm-diagnostics、mind-cluster-v26.1.1、atlas-800t-a2、dcp-2.6、mindio-acp-v26.1.1、mlcommons.storage-rules-v2.0、profiler-2.6、superbench-atc24。

## 修订后的重点边界（2026-10-08）

- 慢 rank：PyTorch 2.8 无 `TORCH_NCCL_HEARTBEAT_MONITOR` 变量（对应能力为 ENABLE_MONITORING）；flight recorder 时间戳是 CPU 侧发现时刻不是设备真实起止；RAS 持续计数差异只提供候选 rank，无差异/未展开/响应不完整不证明全体变慢，须结合各 rank 阶段时间线；活跃期间差异可能是正常瞬态；flight recorder 默认值冲突（PG 2000 vs FR 0）未解；NPU 等价观测仍为缺口。
- 供电散热：violation 计数器单位跨版本冲突（v3.3.9 usec / master ns / nvidia-smi 文档 microseconds）；exporter 默认不导出降频信号；Healthy 的官方限定只覆盖已启用规则与保留样本；NPU 侧无降频原因类指标，训练线 npu-smi 版本化页面未定位。
- Checkpoint I/O：PyTorch 2.6 `async_save` 的 staging 在主线程（大模型阻塞训练循环）；`sync_files=True` 的每文件 fsync 是显式耗时但关系故障一致性；writeback 阈值不是唯一写回条件，节流等待不排除后端慢，根因需同窗口后端证据；FileSystemReader 2.6 无并发参数；MindIO `flush()` 是完成信号但无超时语义；网络存储传输证据仍为缺口。
- 三篇正文均未执行真实环境验证；两篇 procedure 的 `environment_refs` 为空并注明缺失条件。

## 集成时检查与替代复查（历史）

最终 `make check` / `make build` 通过：63 content entries / 76 sources（新增 3 篇正文、5 项来源），catalog 中三篇新条目标题与摘要已核对。

**独立审阅限制同前：当前环境没有 gpt-6-astra/xhigh 派发能力，本轮未能完成约定模型的独立审阅。** 替代措施：同环境只读子代理定向复查（[复查记录](batch-10-substitute-review.md)），核对 14 处固定 commit 源码锚点与 17 个外部页面；发现 3 项 P2（推论误写成原文、README 计数滞后、位图注释归属错误）与 6 项 P3，均已修订关闭并同步研究记录。该复查不构成 astra/xhigh 独立审阅。batch 01/02/08/09 的 Codex 代审已复核闭环（9 项发现全部关闭），batch 10 的约定模型审阅义务同样保留。三篇正文保持 draft、两篇 procedure 与一篇 reference 为限定范围 source_checked，无 reproduced 条目，无任何环境执行结果。
