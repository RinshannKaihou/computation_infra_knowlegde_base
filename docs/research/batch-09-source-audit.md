# 第九批来源与交付记录

集成日期：2026-09-30。第二轮第二批（round-02 backlog 的 R2-04/05/06）由 Opus 编写；研究由只读子代理完成，主任务抽查关键锚点（vLLM gpu_worker.py/utils.py、vllm-ascend platform.py/utils.py/faqs.md、nccl-tests common.cu/util.cu，均命中）。全部保持 draft；两篇 procedure 与一篇 concept 均为限定来源范围的 source_checked。

2026-09-30 补审：用户授权 Codex 主助手替代 astra，已完成[第九批审阅](batch-09-codex-review.md)及[修订定向复核](batch-02-08-09-codex-recheck.md)。本批新增 3 项 P2、2 项 P3 及关联的 B08-C01 全部关闭。本批在原审阅范围内通过；没有实际派发 astra/xhigh 或硬件验证，正文仍为 draft。四批总体状态见[补审汇总](batch-01-02-08-09-codex-review-summary.md)；下文原替代复查保留为另一轮历史。

## 本批正文

| 任务 | 正文 | 类型 |
|---|---|---|
| R2-04 | [昇腾推理 OOM 诊断指南](../../knowledge/07-inference/ascend-inference-oom-triage.md) | procedure |
| R2-05 | [通信带宽退化诊断指南](../../knowledge/03-communication/bandwidth-degradation-triage.md) | procedure |
| R2-06 | [静默错误与计算完整性判定](../../knowledge/08-reliability/silent-errors-and-integrity.md) | concept |

来源记录：[推理 OOM](batch-09-inference-oom-sources.md)、[带宽退化](batch-09-bandwidth-sources.md)、[静默错误](batch-09-silent-error-sources.md)。任务清单：[plans/round-02-backlog.yaml](../../plans/round-02-backlog.yaml)。

## 来源变化

新增 4 项登记（总计 71 项）：

- `src.vllm-ascend.issue-15920`、`src.vllm-ascend.issue-12692`：两条未闭环 NPU OOM 报告，仅作症状形态记录。
- `src.huawei.hccl-perf-test-guide-cann-9.1.x`：HCCL Test 版本化指南（算法带宽口径；redirect 为可变定位）。
- `src.ocp.sdc-in-ai-2025`：OCP SDC 白皮书（CC BY-SA 4.0，已读 p.1–19/29）。

扩充 8 项既有登记 notes：vllm.inference-v0-14（启动内存链）、vllm-ascend-v0-14-0rc1（分配器默认/日志文案/block_size/FAQ）、nccl-tests-b4d5beeb（计时与校验实现）、nccl-user-guide-2.27.5（troubleshooting/env/RAS）、cann-hccl-2d685b08（算法页与 test 占位）、pytorch.numerical-verification-2.6（testing.html/randomness.html）、arxiv.sdc-at-scale-v1（仅 v1、节级内容）、usenix.superbench-atc24（已读页范围）。

## 重点边界

- vLLM v0.14.0 与 vLLM Ascend v0.14.0rc1 两个快照未拼成已验证组合；NPU 侧日志文案（"Available memory"）与上游（"Available KV cache memory"）不同；Ascend block_size 默认/强制 128。
- vLLM Ascend 插件默认追加 PYTORCH_NPU_ALLOC_CONF=expandable_segments:True（非 sleep mode），与 R2-01 的 TorchNPU 快照选项语义衔接；FAQ 13 的缓解建议不等于根因。
- 两条公开 OOM Issue 均 Open、无修复 PR 链、归因未证实；#12692 评论计数不一致已如实记录。
- nccl-tests 主计时为 host 墙钟、-c 校验不进计时、"Out of bounds values" 是校验错误行数（非数组越界）；HCCL Test 只有算法带宽无 busbw，两边数字不互比；链路级计数器来源缺口如实标注。
- SDC 概念篇：Meta v1 为 CPU 证据；温度/频率依赖证据在 OCP 而非 v1；SuperBench 灰色退化属性能域；OCP 检测分类法只引用目录级（正文未读）；PyTorch 数值噪声是判定前的背景扣除项。

## 检查与轮末审阅

最终 `make check` / `make build` 通过：60 content entries / 71 sources（新增 3 篇正文、4 项来源），catalog 中三篇新条目标题、摘要、类型、平台与验证状态已逐一核对。

**独立审阅限制同 batch 08：当前环境没有 gpt-6-astra/xhigh 派发能力，本轮未能完成约定模型的独立审阅。** 替代措施：同环境只读子代理定向复查（[复查记录](batch-09-substitute-review.md)），核对 17 处固定 commit 源码锚点与全部新增文档页；发现 2 项 P2（OCP 白皮书的 DUE 展开与 fault-masking 锚点）与 7 项 P3，均已修订关闭。该复查不构成 astra/xhigh 独立审阅；建议后续具备派发能力时对 batch 08–09 补审。三篇正文保持 draft、两篇 procedure 为限定范围 source_checked，无 reproduced 条目，无任何环境执行结果。
