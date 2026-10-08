# 第十一批复查记录（替代性复查，非 astra/xhigh）

**历史记录提示（2026-10-08）：** 本文保留当时实际执行与关闭结论。当前 `gpt-6.1-sol / xhigh` 的[新审阅](batch-11-codex-review.md)及[修订/定向复核](batch-10-11-12-codex-recheck.md)已完成，1 项 P1、3 项 P2、1 项 P3 全部关闭，本批在原审阅范围内通过；以新报告和[汇总](batch-10-11-12-codex-review-summary.md)为当前状态。

复查日期：2026-10-08。**限制声明同前：用户约定每轮由 gpt-6-astra / xhigh 独立审阅；当前环境没有该模型派发能力，本轮未能完成约定模型的独立审阅。** 本记录是同环境只读子代理的定向复查。

## 范围与实际核查

完整复读三篇新增正文（ascend-op-graph-failure-triage、elastic-training-and-membership、quantization-and-quality）与三份来源记录；核对固定 commit 源码锚点（PyTorch v2.6.0 OperatorEntry.cpp、vLLM v0.14.0 model.py 与量化文档、TorchNPU bc51ab84 的 fallback/OptionsManager/图组件存在性、MindSpeed-LLM 53f3639c 的 HA 文档全文与实现入口、vLLM Ascend 52d4acfa 的矩阵/图模式/评估目录）、PyTorch 2.6 elastic 文档四页、CANN 错误码页可达性。复查者另运行 `make check`（PASS，66/78）。

## 发现与关闭

| 发现 | 级别 | 状态 | 关闭依据 |
|---|---|---|---|
| 量化篇虚构负面断言：“该 commit 没有量化专题用户文档页”——实际存在 docs/source/user_guide/feature_guide/quantization.md（ModelSlim/LLM-Compressor 工具链、W8A8 示例、RAM 前提） | P1 | 关闭 | 主任务复核该页存在（gh api 读取确认），正文改为引用该页并标注内容未逐字核对；研究记录与 registry notes 同步更正 |
| “15 个方法页”实为 14 个（14 方法页 + README） | P2 | 关闭 | 正文与研究记录改为 14 |
| 评估指南“两份”实为四份（ais_bench/evalscope/lm_eval/opencompass） | P3 | 关闭 | 正文与研究记录改为四份并列名 |
| README 批次叙述止于 batch 10、审计链接缺 batch-11 | P3 | 关闭 | README 已补 batch 11 与审计链接 |
| 02/06/07 index 的 updated_at 未刷新 | P3 | 关闭 | 三处改为 2026-10-08 |
| 昇腾路径收录口径不一致（漏 quantization-and-quality） | P3 | 关闭 | ascend.md 补链接与 related_ids |
| WorkerSpec 默认 3 的引用归属（证据在 agent.html 签名） | P3 | 关闭 | 正文与研究记录标注归属 |
| “文档与代码的约束以代码为更严”过头（缩容次数约束仅见文档，非包含关系） | P3 | 关闭 | 改为“开关组合与冲突约束以代码为更严；缩容次数约束仅见文档” |
| int8.md 评估段锚点 L117–132 略短（实际至 136）；OperatorEntry.cpp 引 L550–559 含函数收尾（实际至 557） | P3 | 关闭 | int8 锚点已改；OperatorEntry 引用为包含性冗余不影响定位，保持不变 |

## 已排除的疑点（核对为正确）

- OperatorEntry.cpp 两种报错文本、_verify_quantization 实现、量化硬件表与表注、int8.md 的 cc>7.5 与 Blackwell 限制、VariableFallbackKernel 性质、torchair/NPUGraph/_inductor 存在性、OptionsManager 环境变量读取点、错误码 207001/245002。
- MindSpeed-LLM HA 文档全文（依赖、开关、四条约束、内存公式）与 high_availability.py 断言；PyTorch 2.6 elastic 文档四页语义（含 WorkerFailure 旧名不存在的确认）。
- 元数据、导航、YAML、不拼配套/不外推 NPU 的边界表述。

## 未覆盖

- 未复核存量 63 篇内容；CANN 图编译排障文档、torchair 启用条件、量化方法细节约束、昇腾量化工具链深入等原文标注的缺口保持开放；未执行任何环境验证。
