# Batch 27 来源与交付审计

收尾日期：2026-10-21。四任务：T07-04（量化边界，revise）、T07-05（输出质量评估，new）、T07-06（分布式布局，new）、T07-07（PD connector，revise）。

## 来源账面

- registry 538→542：新增 AWQ（2306.00978v6）/GPTQ（2210.17323v2）/SmoothQuant（2211.10438v7）三篇论文（摘要级；GPTQ/SmoothQuant 许可经复核更正为 CC BY 4.0、AWQ 为 arXiv non-exclusive）＋ src.ascend.msmodelslim-msit（工具入口，未固定 commit）。
- 扩展 notes：src.vllm.inference-v0-14（量化实现/分布式 serving/ROCm 链/PD connector 族）、src.ascend.vllm-ascend-v0-14-0rc1（量化指南/模型矩阵/评估指南/PD 两式与教程）、src.ascend.mindie-llm-docs-69e5a5dd（量化特性 9 页/并行 6 页/FAQ/ModelTest）、src.ascend.mindie-llm-src-69e5a5dd 与 mindie-llm-repo（KV 传输封装局部取证）。
- 版本线：vLLM v0.14.0（b17039bc）、vLLM Ascend v0.14.0rc1（52d4acfa）、MindIE-LLM master@69e5a5dd（文档线 3.1.0）；Mooncake 教程钉 v0.3.7.post2、nixl>=0.7.1（教程/需求内钉扎）。全部文件 SHA-256 与行号锚点见 batch-27-t07-0{4,5,6,7}-sources.md。
- 修复两处历史 YAML 截断（vllm-ascend notes issue #1608 段、Batch 21 tracker #8914 段，plain scalar 含 # 被截断，改块标量）。

## 审阅账面（全部 gpt-6.1-sol / xhigh，每轮经 turn_context 核验）

| 任务 | 初审 | 复核轮次 | 终态 |
|---|---|---|---|
| T07-04 | 13 项 | 3 轮 | 13/13 CLOSED |
| T07-06 | 11 项＋N01/N02 | 4 轮 | 13/13 CLOSED |
| T07-05 | 7 项 | 3 轮 | 7/7 CLOSED |
| T07-07 | 10 项＋N01 | 3 轮 | 11/11 CLOSED |

合计 47 项编号发现全部 CLOSED，无 P1、无例外项。未运行任何引擎/评估/分布式部署；正文均为 draft、verification source_checked。

## 主题账面

07.4（量化与输出质量）与 07.5（分布式推理/PD）经本批对照交付内容复核升为已覆盖（基础）；覆盖统计 49/12/2→51/10/2。机器可读记录见 plans/topic-coverage.yaml 与 docs/topic-coverage-audit.md。
