# Batch 29 来源与交付审计

收尾日期：2026-10-21。四任务：T00-03（容量/成本/能耗与可靠性权衡，new `knowledge/00-overview/design-targets-and-tradeoffs.md`，主题 00.4/00.5）、T08-01（故障模型与传播，new `knowledge/08-reliability/fault-models-and-propagation.md`，主题 08.2/08.5）、T08-02（相关故障与冗余失效公开案例，new `knowledge/08-reliability/correlated-failure-source-case.md`，主题 08.2/08.5）、T08-03（隔离/重试预算/降级/恢复选择，new `knowledge/08-reliability/mitigation-and-recovery-principles.md`，主题 08.5/08.1）。批内顺序按依赖：T08-01 → T08-02 → T08-03 → T00-03。

## 来源账面

- registry 553→559：新增 6 项——Avizienis 2004 依赖性分类学（作者 Landwehr 托管全文 PDF，TDSC 1(1):11–33，curl 取回 2.6MB 逐段核对 §2.2/§3.2.1/§3.3.1/§3.5）、Meta 2021-10-04 复盘（engineering.fb.com，运营方一手，逐段核对）、Cloudflare 2021-10-04 外部观测（blog.cloudflare.com，观测方一手，逐段核对）、AWS Exponential Backoff and Jitter（2015-03-04，Marc Brooker）、MLPerf Inference 功耗测量政策（inference_policies master@d3eba2f，Apache-2.0 经 GitHub 页面 SPDX 确认；器材两类条款按原文轮次分列）、RFC 9110（§9.2.2 全文 curl 取回核对，初审修订轮登记）。
- 既有条目扩展 notes：src.paper.avizienis-dependability-2004（复核轮 §3.5 定位与四视角层级订正）；src.meta/cloudflare 两条（复核轮命令/工具分列、30 倍口径、暂定语气同步）。
- 无扩展 notes 的复用：SRE 三章（implementing-slos 2026-09-29；cascading-failures/handling-overload Batch 28）、Envoy circuit breaking（Batch 28）、K8s v1.32 Job/Pod 两页（Batch 22/28）、PyTorch elastic 2.6（Batch 11 B11-C03 口径）、MindSpeed-LLM HA v2.2.0、SDC at scale、OCP SDC in AI 2025、SuperBench ATC24、nvidia-smi/DCGM（Batch 13 口径；nvidia-smi 三节于 2026-10-21 补核）。

## 审阅账面（全部 gpt-6.1-sol / xhigh，每轮经 turn_context 核验）

| 任务 | 初审 | 复核轮次 | 终态 |
|---|---|---|---|
| T08-01 | 9 项（P2×6、P3×3）＋复核新增 N01 | 3 轮（第一轮 7 CLOSED；第二轮 3 项 CLOSED；第三轮确认） | 10/10 CLOSED |
| T08-02 | 7 项（P2×7） | 1 轮 | 7/7 CLOSED |
| T08-03 | 10 项（P2×9、P3×1）＋复核新增 N01 | 3 轮（第一轮 8 CLOSED；第二轮 C10/N01 CLOSED；第三轮 C05 CLOSED） | 11/11 CLOSED |
| T00-03 | 9 项（P2×8、P3×1）＋复核新增 N01 | 2 轮（第一轮 7 CLOSED；第二轮 3 项 CLOSED） | 10/10 CLOSED |

合计 38 项编号发现全部 CLOSED，无 P1、无例外项。会话核验：四个独立审阅会话（01a15de0-332f / 01a15de0-b038 / 01a15e32-28c3 / 01a15e32-6cde）的全部 turn_context 均为单一 `gpt-6.1-sol / xhigh`、工作目录正确；JSONL 中 `[frontier_llm]` 命中均为文件引用非回退。复核主要修订方向：T08-01 分类对象拆分（存在持续/激活可复现性正交化、elusive 判定须证据）、T08-02 证据边界收缩（命令/审计工具分列、发现时刻 vs 事件时刻、全球口径、未披露事实不补写）、T08-03 条件化改写（幂等判定、backoffLimit 计数对象、elastic 文档概括 vs 实现分支、固定源码锚点）、T00-03 量纲与口径（示例 A 年度量纲闭合与翻转条件分列、示例 B 负载强度、PUE 方向、容量四分、nvidia-smi 读数边界）。未运行任何注入/演练/部署；正文均为 draft、verification source_checked。

## 主题账面

00.4 收口（容量/成本/能耗量化权衡缺口关闭，升已覆盖）、00.5（升已覆盖）、08.2（三缺口关闭，升已覆盖）、08.5（三缺口关闭，升已覆盖）。覆盖统计 53/10/0→57/6/0（covered 含 6 个 covered_basic）。批次与四任务置 done（completion_record：本文件）。reference-architectures 两处 T00-03 前向引用已同步指向新正文。机器可读记录见 plans/topic-coverage.yaml 与 plans/full-coverage-backlog.yaml。

## 写作轮次自记

- 正文均为 draft、verification source_checked；无任何本地环境操作；四篇的 unknown 清单见各自 sources 记录。
- 同步修订：reference-architectures.md 两处"T00-03（Batch 29）"前向引用改指新正文，related_ids 增补；08/00 两 index 的二级主题地图与已有正文列表更新。
- 下一批 Batch 30：T08-04 SDC 检测补齐、T08-05 统一测试方法、T08-06 可靠性统计、T08-07 事故复盘、T08-08 诊断评测（其中 T08-04 修订 silent-errors-and-integrity.md）。
