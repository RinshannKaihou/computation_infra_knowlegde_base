# 第八批来源与交付记录

集成日期：2026-09-30。第二轮首批（round-02 backlog 的 R2-01/02/03）由 Opus 编写；研究由只读子代理完成，主任务对关键锚点做了独立抽查（curl 取固定 commit 原文件核对 memory.py `__all__` 与 `memory_allocated`、NPUCachingAllocator.cpp 的 getenv 与 OOM 文案、Kueue troubleshooting_jobs.md 配额样例、dataloader.py 的 worker 崩溃错误与 prefetch 预填，均一致）。全部保持 draft；两篇 procedure 与一篇 concept 均为限定来源范围的 source_checked。

2026-09-30 补审：用户授权 Codex 主助手替代 astra，已完成[第八批审阅](batch-08-codex-review.md)及[修订定向复核](batch-02-08-09-codex-recheck.md)。本批新增 1 项 P2、2 项 P3 及继承的 B02-C01 全部关闭，B08-C01 的下游影响同步关闭。本批在原审阅范围内通过；没有实际派发 astra/xhigh 或硬件验证，正文仍为 draft。四批总体状态见[补审汇总](batch-01-02-08-09-codex-review-summary.md)；下文原替代复查保留为另一轮历史。

## 本批正文

| 任务 | 正文 | 类型 |
|---|---|---|
| R2-01 | [昇腾 NPU 内存与 OOM 证据](../../knowledge/02-software-stack/ascend-memory-oom-evidence.md) | concept |
| R2-02 | [训练数据加载饥饿诊断指南](../../knowledge/04-data-storage/data-starvation-triage.md) | procedure |
| R2-03 | [空闲设备但作业等待诊断指南](../../knowledge/05-cluster-platform/idle-resource-job-waiting-triage.md) | procedure |

来源记录：[内存/OOM](batch-08-memory-sources.md)、[Kueue 等待](batch-08-kueue-pending-sources.md)、[数据加载](batch-08-dataloader-sources.md)。任务清单：[plans/round-02-backlog.yaml](../../plans/round-02-backlog.yaml)。

## 来源变化

新增 4 项登记（总计 67 项）：

- `src.huawei.cann-82rc1alpha001-acl-runtime-memory`：CANN 8.2.RC1.alpha001 运行时内存管理页（0094/0095/0096）；0094 页头版本未直接核验。
- `src.huawei.cann-82rc1-aclerror`：aclError 错误码页（URL 路径 82RC1，页头版本未核验）。
- `src.pytorch.profiler-2.6`：torch.profiler 2.6 文档。
- `src.pytorch.dataloader-source-v2.6.0`：PyTorch v2.6.0 固定 dataloader.py 源码。

扩充 3 项既有登记的 notes：`src.ascend.torch-npu-v7.2.0-pytorch2.6.0`（内存 API 与分配器实现范围、master 选项集差异、docstring 沿用 CUDA 措辞警示）、`src.pytorch.cuda-semantics-2.6`（memory-management 等小节锚点，仍仅 CUDA 对照）、`src.kueue.admission-v0.19.0`（troubleshooting/pending/kueuectl/cohort/scheduler/features 扩展阅读，v1beta1 deprecated 与门控事实）。

## 重点边界

- TorchNPU 固定快照的 `PYTORCH_NPU_ALLOC_CONF` 为五选项；master 分支选项集已变（仅作发现入口）。张量分配器、workspace 分配器、下发重试路径与 1EB 防御分支共用 “NPU out of memory” 前缀，抛出层不同。
- memory.py docstring 沿用 CUDA 措辞（nvidia-smi/cudaMalloc），不作为 NPU 行为证据；API 对照表对 memory_snapshot/get_allocator_backend 及私有 _record_memory_history 等的 NPU 兼容列留空，读作未承诺。
- 昇腾“OOM 报在无关位置”的错位陈述在固定 commit 只有间接证据（TASK_QUEUE_ENABLE 默认 1 等），正文标为机制推断，未写成官方语义。
- Kueue v0.19.0：v1beta1 已 deprecated（文档示例 v1beta2）；细分等待 reason（TopologyPlacementFailed 等）受 UnadmittedWorkloadsObservability 门控且默认关闭，默认只见 Pending；pendingWorkloadsStatus 字段自 v0.14.0 废弃。「借入被收回导致等待」是三条证据的归纳，非文档原文结论。
- PyTorch 2.6：`timeout=0` 禁用超时、num_workers=0 设正 timeout 触发断言、worker 崩溃/FD 耗尽错误文本均为源码行为（data.html 未覆盖）；profiler 页无 NPU/PrivateUse1 使用说明。
- 三篇正文均未执行真实环境验证；两篇 procedure 的 applicability.environment_refs 为空并注明缺失条件。

## 检查与轮末审阅

最终 `make check` / `make build` 通过：57 content entries / 67 sources（新增 3 篇正文、4 项来源），catalog 中三篇新条目的标题、摘要、类型、平台与验证状态已逐一核对，无 YAML 截断。

**独立审阅限制：当前环境没有 gpt-6-astra/xhigh 模型派发能力，本轮未能完成约定模型的独立验证审阅。** 已完成的替代措施：同环境只读子代理做定向复查（[复查记录](batch-08-substitute-review.md)），实际经固定 commit 原文件核对 20 余处锚点；发现 4 项 P3（1⅛ 引用位置、开区间端点、1EB 分支数量、04 index 日期），均已修订关闭。该复查不构成 astra/xhigh 独立审阅；若后续环境具备派发能力，建议对本批补做一次约定模型审阅。三篇正文保持 draft、两篇 procedure 为限定范围 source_checked，没有新增 reproduced 条目，也没有任何环境执行结果。
