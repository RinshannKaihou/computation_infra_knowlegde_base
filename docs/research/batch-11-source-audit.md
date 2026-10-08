# 第十一批来源与交付记录

**最新审阅状态（2026-10-08）：** 用户约定的 `gpt-6.1-sol / xhigh` 审阅、修订与定向复核已完成；1 项 P1、3 项 P2、1 项 P3 全部关闭，本批在原审阅范围内通过，见[本批报告](batch-11-codex-review.md)、[定向复核](batch-10-11-12-codex-recheck.md)和[三批汇总](batch-10-11-12-codex-review-summary.md)。旧替代复查与集成计数保留为历史，此前 astra 审阅义务已由用户新约定替代。

集成日期：2026-10-08。第二轮第四批（round-02 backlog 的 R2-10/11/12）由 Opus 编写。**过程备注：本批两个研究方向（算子/图编译、量化质量）的研究子代理先后因 OAuth 故障与两次 2 小时超时失败，按“代理失败则主任务接手”的约定改由主任务用 gh api 直接定向取证**；弹性训练方向的研究子代理正常完成。全部保持 draft；一篇 procedure 与两篇 concept 均为限定来源范围的 source_checked。

## 本批正文

| 任务 | 正文 | 类型 |
|---|---|---|
| R2-10 | [昇腾算子不支持与图编译失败诊断指南](../../knowledge/02-software-stack/ascend-op-graph-failure-triage.md) | procedure |
| R2-11 | [弹性训练与成员变更](../../knowledge/06-training/elastic-training-and-membership.md) | concept |
| R2-12 | [推理量化与输出质量验证](../../knowledge/07-inference/quantization-and-quality.md) | concept |

来源记录：[算子/图编译](batch-11-op-graph-sources.md)、[弹性训练](batch-11-elastic-sources.md)、[量化质量](batch-11-quantization-sources.md)。任务清单：[plans/round-02-backlog.yaml](../../plans/round-02-backlog.yaml)。

## 来源变化

新增 2 项登记（总计 78 项）：`src.pytorch.elastic-2.6`（elastic 系列文档页）、`src.pytorch.dispatcher-v2.6.0`（OperatorEntry.cpp 固定源码）。扩充 4 项既有登记 notes：mindspeed-llm-ha-v2.2.0、torch-npu-v7.2.0-pytorch2.6.0、vllm.inference-v0-14、vllm-ascend-v0-14-0rc1。

## 修订后的重点边界（2026-10-08）

- 算子/图编译：dispatcher 报错需与 kernel/fallback 一起判断。固定 TorchNPU VariableFallbackKernel.cpp 的 PrivateUse1 分支注册 CPU fallback，AutogradPrivateUse1 与 SparsePrivateUse1 另有分支；具体算子成功与梯度正确性未执行验证。插件指南要求使用者显式启用 eager 对照，不证明自动重试；torchair/NPUGraph/_inductor 的启用配套、CANN 图编译排障文档仍为缺口。
- 弹性训练：状态恢复是应用责任；torchrun CLI max-restarts 默认 0，WorkerSpec API 默认 3，记录实际入口及覆盖值。MindSpeed-LLM 弹性仅 DP 粒度、缩容一次/扩容回原规模；开关冲突按固定代码、缩容次数按文档分别核对；两者不拼配套。
- 量化：上游 vLLM 文档有 14 个方法页加 README，registry 已同步；INT8 对 Turing/SM 7.5 的表格与严格 >7.5 条件冲突，kernel/runtime 边界仍未知；Blackwell 限制按方法页/版本限定。上游表不含 NPU，昇腾只看插件声明；固定任务评估与产出指标分开。
- 三篇正文均未执行真实环境验证；procedure 的 `environment_refs` 为空并注明缺失条件。

## 集成时检查与替代复查（历史）

最终 `make check` / `make build` 通过：66 content entries / 78 sources（新增 3 篇正文、2 项来源），catalog 中三篇新条目标题与摘要已核对。

**独立审阅限制同前：当前环境没有 gpt-6-astra/xhigh 派发能力，本轮未能完成约定模型的独立审阅。** 替代措施：同环境只读子代理定向复查（[复查记录](batch-11-substitute-review.md)）；发现 1 项 P1（量化篇虚构负面断言——vLLM Ascend 实际有量化用户指南页，已复核并改为引用）与 1 项 P2（方法页计数 15→14）及 7 项 P3，均已修订关闭并同步研究记录、registry、导航与 README。该复查不构成 astra/xhigh 独立审阅；本批的约定模型审阅义务保留。三篇正文保持 draft、限定范围 source_checked，无 reproduced，无任何环境执行结果。
