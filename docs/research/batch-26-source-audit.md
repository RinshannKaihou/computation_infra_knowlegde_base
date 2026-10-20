# 第二十六批来源审计（T06-08/T07-01/T07-02/T07-03）

更新日期：2026-10-21。状态：**Batch 26 四任务均通过既定审阅与定向复核范围；批次完成**；四篇交付正文均为 `draft`，未做真实环境验证。本批与 Batch 25 并行启动（来源准备轮在 Batch 25 审阅期间先行，集成写入按串行规则等 Batch 25 提交后执行）。

## 本批任务状态

| 任务 | 操作 / 类型 | 目标文件 | 最终状态 |
|---|---|---|---|
| T06-08 核验恢复状态与弹性训练的 v1 边界 | 修订 / concept | `knowledge/06-training/checkpoint-state-consistency.md`、`knowledge/06-training/elastic-training-and-membership.md` | **通过审阅**：初审 5 项（4 P2/1 P3），初审＋1 轮定向复核后全部 CLOSED；审阅者并纠正初审对 PDF 整除方向的误读 |
| T07-01 权重加载、引擎 ready 与启动失败诊断 | 新增 / procedure | `knowledge/07-inference/model-loading-and-readiness.md` | **通过审阅**：初审 11 项（10 P2/1 P3），初审＋2 轮定向复核后全部 CLOSED（第二轮关 9 项并指出两处残留，第三轮关闭） |
| T07-02 推理引擎组件与平台功能交集档案 | 新增 / reference | `knowledge/07-inference/engine-backend-boundaries.md` | **通过审阅**：初审 7 项＋复核新增 R01–R04 共 11 项（6 P2 正文＋4 P2 复核新增＋1 P3），初审＋5 轮定向复核后全部 CLOSED |
| T07-03 MindIE 推理执行与配置样板 | 新增 / reference | `knowledge/07-inference/mindie-execution-profile.md` | **通过审阅**：初审 8 项（7 P2/1 P3）＋R01/R02，初审＋3 轮定向复核后共 10 项全部 CLOSED |

## 来源准备与集成

- 新增登记 **12** 项：T07-01 轮 6 项（src.vllm.model-loader-v0-14、src.vllm.tokenizer-registry-v0-14、src.vllm.readiness-health-v0-14、src.vllm.rocm-install-doc-v0-14、src.ascend.mindie-llm-doc-latest、src.ascend.mindie-llm-repo-69e5a5dd）；T06-08 轮 3 项（src.ascend.mindio-ttp-constraints-mindxdl-600、src.nvidia.megatron-checkpointing-core-v0.12.1、src.pytorch.wheel-matrix-2.6.0）；T07-02 轮 3 项（src.vllm.core-components-v0-14、src.vllm.platforms-cuda-rocm-v0-14、src.ascend.mindie-llm-src-69e5a5dd）；T07-03 轮 1 项（src.ascend.mindie-llm-docs-69e5a5dd）。`sources/registry.yaml` 由 525 增至 **538**（无重复 ID）。
- 既有条目 notes 扩展 3 项：src.ascend.mindspeed-llm-checkpoint-v2.2.0（Megatron 委托链）、src.ascend.mindspeed-llm-ha-v2.2.0（adaptor 调用面）、src.ascend.vllm-ascend-v0-14-0rc1（NPUPlatform/组件覆盖/README 版本线）。
- 单任务来源记录：`batch-26-t07-01-sources.md`（vLLM 固定 commit 加载/探针切面＋ROCm 文档＋MindIE 首批证据）、`batch-26-t06-08-sources.md`（MindSpeed HA→Megatron core_v0.12.1 委托链＋MindIO TTP 约束页两次取回＋DCP×ROCm wheel 边界）、`batch-26-t07-02-sources.md`（vLLM 调度/KV/平台切面＋vllm-ascend 平台与覆盖件＋MindIE src 组件族）、`batch-26-t07-03-sources.md`（MindIE 仓内 docs 树：架构/配置/PD/日志/版本说明书＋Qwen 样板）。
- 取证方式：codeload 源码包（MindSpeed-LLM 53f3639c、Megatron core_v0.12.1、vLLM b17039bc、vllm-ascend 52d4acf、MindIE-LLM master@69e5a5dd）＋固定 commit 文件级 SHA-256＋官方文档页渲染取回（hiascend MindIO TTP 约束页两次一致、docs.vllm.ai、pytorch.org、mindie-llm-doc）。**方法论记录**：codeload 整包哈希差异的真正原因是 tag 名/commit 名两种归档命名（顶层目录不同），不是 gzip 不稳定；文件级哈希是跨轮次稳定锚（T06-08-C05 订正）。mindio_ttp whl 下载页两次 500、MindIE《故障恢复加速》PDF 作者直下仅 2 页与审阅分页不符——均如实记录未登记。
- 版本线要点：MindIE-LLM 开源仓 release_notes 自述 **MindIE LLM 3.1.0**（配套 CANN 9.0.1/MindCluster 26.0.0）；同快照 README 版本表（2.3.0↔8.5.0）与数值不同（未裁定，采信 release_notes 为文档线）；readthedocs latest 站经抽查页级一致锚定（不构成整站映射）。

## 关键边界

- 三条引擎线严格分立：vLLM 上游 v0.14.0（b17039bc）、vLLM Ascend v0.14.0rc1 线（52d4acf，配套 CANN 8.5.0/torch-npu 2.9.0）、MindIE-LLM 3.1.0 文档线（69e5a5dd，配套 CANN 9.0.1）——互不拼接为已验证栈；MindIE 产品包（闭源）范围 unknown。
- vLLM 加载/探针结论限固定 commit；`/health` 三层语义（函数/入口/判据）与"死活≠就绪"边界贯穿 T07-01/03。
- MindIE 抢占：配置声明（maxPreemptCount>0 限一轮抢占数且 cpuMemSize≠0）与源码已核路径（RECOMPUTE 默认、SWAP 受计数门控）**分立记录**，不合并（T07-03-C02）；健康检查＝周期性虚拟推理＋利用率三态，与 vLLM 探针是不同证据类型。
- Qwen 样板两表卡数差异未消解（README 测试配置口径 vs 支持列表分级口径，不取并集不判过期）；候选验证样板（Qwen2-7B-Instruct/A2/TP2/BF16/atb/standard/whl）明确**未达可执行条件**。
- 全部为源码/文档口径；未安装、构建或运行任何引擎，无本库实测结果。

## 结构检查

- `make check`：PASS（110 content entries / **538** sources）。`make build`：PASS。
- 只证明结构与本地链接，不证明技术正确性或远程内容。

## 审阅与复核

- 审阅模型：codex exec `-m gpt-6.1-sol --config model_reasoning_effort="xhigh"`；每轮调用方从 `~/.codex/sessions` 的 `turn_context` 核验单一模型/档位、无 fallback 标记（日志中的 `[frontier_llm]` 字样经查均为审阅者读取 authoring-guide 原文的文件引用，非模型回退）。
- 轮次：T06-08 初审＋1 轮；T07-01 初审＋2 轮；T07-02 初审＋5 轮（复核新增 R01–R04）；T07-03 初审＋3 轮（复核新增 R01/R02）。全部发现累计 CLOSED，无 P1，无例外清单项。
- 审阅者独立重开上游证据并复算 SHA-256；两处作者错误由审阅链纠正（MindIO TTP 内存公式量纲 N＝模型参数量而非卡数；Qwen"互证"实为两表卡数冲突）。模型审阅不替代真实硬件、加载、服务或输出质量验证，正文保持 `draft`。
