# Batch 29 来源与交付审计

状态：来源准备与写作完成（2026-10-21），审阅进行中。四任务：T00-03（容量/成本/能耗与可靠性权衡，new `knowledge/00-overview/design-targets-and-tradeoffs.md`）、T08-01（故障模型与传播，new `knowledge/08-reliability/fault-models-and-propagation.md`）、T08-02（相关故障与冗余失效公开案例，new `knowledge/08-reliability/correlated-failure-source-case.md`）、T08-03（隔离/重试预算/降级/恢复选择，new `knowledge/08-reliability/mitigation-and-recovery-principles.md`）。

## 来源账面

- registry 553→558：新增 5 项——Avizienis 2004 依赖性分类学（作者 Landwehr 托管全文 PDF，TDSC 1(1):11–33）、Meta 2021-10-04 复盘（engineering.fb.com，运营方一手）、Cloudflare 2021-10-04 外部观测（blog.cloudflare.com，观测方一手）、AWS Exponential Backoff and Jitter（2015-03-04，Marc Brooker）、MLPerf Inference 功耗测量政策（inference_policies master@d3eba2f，Apache-2.0 经 SPDX 确认）。
- 无扩展 notes 的既有条目复用：SRE 两章（Batch 28）、Envoy circuit breaking（Batch 28）、K8s v1.32 Job/Pod 两页（Batch 22/28）、PyTorch elastic 2.6（Batch 11 核对口径）、MindSpeed-LLM HA v2.2.0、SDC at scale、OCP SDC in AI 2025、SuperBench ATC24、nvidia-smi/DCGM（Batch 13 口径）。
- 版本线：inference_policies master@d3eba2f21026d868ad65cdcad2bb81e4a17ce3d（2026-10-21 观察）；Avizienis PDF 2026-10-21 curl 取回（2.6MB）经 pdftotext 核对 §2.2/§3.2.1/§3.3/§4；三篇博客均 2026-10-21 WebFetch 逐段核对并留关键句于 registry notes。

## 审阅账面（全部 gpt-6.1-sol / xhigh，每轮经 turn_context 核验）

（审阅完成后回填）

| 任务 | 初审 | 复核轮次 | 终态 |
|---|---|---|---|
| T08-01 | — | — | — |
| T08-02 | — | — | — |
| T08-03 | — | — | — |
| T00-03 | — | — | — |

## 主题账面

（审阅闭环后与覆盖统计一并回填；本批目标主题 00.4 收口、00.5、08.2、08.5）

## 写作轮次自记

- 批内顺序按依赖：T08-01 → T08-02 → T08-03 → T00-03（后者独立）。
- 正文均为 draft、verification source_checked；无任何本地环境操作；四篇的 unknown 清单见各自 sources 记录。
- 同步修订：reference-architectures.md 两处"T00-03（Batch 29）"前向引用改指新正文，related_ids 增补；08/00 两 index 的二级主题地图与已有正文列表更新。
