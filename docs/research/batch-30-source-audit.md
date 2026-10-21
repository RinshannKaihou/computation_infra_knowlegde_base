# Batch 30 来源与交付审计

交付日期：2026-10-21（内容提交）。五任务：T08-04（SDC 检测/训练传播/平台证据，**revise** `knowledge/08-reliability/silent-errors-and-integrity.md`，主题 08.6）、T08-05（统一测试选择/压力注入/统计方法，new `knowledge/08-reliability/test-design-and-coverage.md`，主题 08.7/08.1/08.3/08.4/08.6）、T08-06（可靠性统计/有效产出/恢复损失，new `knowledge/08-reliability/reliability-metrics-and-recovery-loss.md`，主题 08.1/08.8）、T08-07（事故复盘/来源更新/知识维护，new `knowledge/08-reliability/postmortem-and-knowledge-update.md`，主题 08.8/08.3/08.4）、T08-08（诊断评测方法与公开题组，new `knowledge/08-reliability/diagnostic-evaluation-method.md`＋`knowledge/08-reliability/diagnostic-evaluation-fixtures.md`，主题 08.4/08.8）。批内顺序按依赖：T08-04 → T08-05 → T08-06 → T08-07 → T08-08。**审阅未开始**；本文件为交付时初稿，审阅闭环后更新。

## 来源账面

- registry 559→572：新增 13 项——arXiv:2203.08989（Meta 检测量化，CC BY-NC-ND 4.0，HTML 全文）、ACL 2025 LLM 训练 SDC（=arXiv:2502.12340v1，全文含附录 D）、Llama 3（arXiv:2407.21783v3 §2 与 Table 5，百分比经 GPU 六行求和自洽核对、绝对计数不自洽故不引用）、Google MPG（arXiv:2502.06982v1 全文）、SRE Book Ch.17 Testing for Reliability（全文，URL 经目录页定位）、SRE Workbook Ch.10 Postmortem Culture（全文）、SRE Book Ch.14 Managing Incidents（全文）、Kalibera & Jones arXiv:2007.10899（全文）、msprobe 固定 tag MindStudio_26.2.0.B110_001（比对判据逐条；tag 根无 LICENSE）、hiascend dcmi_047 DCMI ECC（doc_center/source 静态页逐字段）、Ascend FaultDiag v26.1.1 固定 commit（文件树重新定位后核读四页）、RCACopilot arXiv:2305.15778v4（摘要级）、Cloud-OpsBench arXiv:2603.00468v1（全文，CC BY 4.0）。
- 既有条目扩展 notes：src.ocp.sdc-in-ai-2025（补读 §5.2–§7 至文末；pdfinfo 重核 30 页并更正 29 页旧记）；src.huawei.hdk-26.1x-a2-npu-smi-2026-10-08（补核 npusmi_0034 ECC 全字段）。
- 无扩展复用：SRE implementing-slos/monitoring/effective-troubleshooting、SuperBench、PyTorch numerical-verification/elastic、vLLM v0.14（经 latency-metrics 转引）、MLPerf Storage v2.0、nccl-tests、HCCL 性能指南、Meta/Cloudflare 2021-10-04、三个 PyTorch/ vllm-ascend Issue 及 dcp 修复 commit。
- 取证方法备注：hiascend `document/detail` 页 JS 挡墙不可直读，改用同版本 `doc_center/source` 静态页；两篇 SDC 论文与 Llama 3/MPG/Cloud-OpsBench 经 arXiv HTML 全文逐节核读；GitHub API 限流未影响 raw 取证。

## 主题账面（交付时点，审阅后重算）

T08-04 关闭 08.6 三个缺口（NPU 一手依据→已建平台证据清单且边界明确、训练侧检测/传播正文、目录级分类→节级）；T08-05 关闭 08.7 前两缺口（统一选择/覆盖矩阵、压力注入模型与统计方法；第三缺口"真实环境结果"按验收条款仍由 validation-backlog 管理，不因正文关闭）；T08-06/T08-07/T08-08 关闭 08.8 三个缺口（有效产出/长期统计、复盘与知识更新方法、独立诊断评测集的方法与公开题组——**独立评测集本体仍待 V12**）。08.7 覆盖状态在收尾提交按"方法已覆盖、实测另行"口径重算。

## 写作轮次自记

- 正文均为 draft、verification source_checked（T08-07 为 procedure 且 applicability.environment_refs 空＋notes 说明）；无任何本地环境操作、注入或评测执行。
- T08-04 修订保留稳定 ID 与既有正确章节（定义/被动盲区/噪声扣除），新增检测量化、三层级传播、检测方法分层（并入 ABFT 实测反例）、平台证据清单与 NPU 边界四块；旧"待确认"中已解决项（两篇论文、OCP §5.2、NPU 证据边界）就地关闭，未解决项保留并更新。
- 六篇新增/修订的 unknown 清单见各 sources 记录；08 index 已更新（新增五条正文与 08.6/08.7/08.8 地图行）。
- 下一批 Batch 31：T06-09/T07-12/T02-12/T00-04/T00-05（按依赖图）。
