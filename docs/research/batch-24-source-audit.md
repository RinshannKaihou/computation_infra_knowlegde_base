# 第二十四批来源审计（T05-10/T06-01/T06-02/T06-03）

更新日期：2026-10-19。状态：**Batch 24 已交付并通过审阅**；四篇正文均为 `draft`，未做真实环境验证。

## 本批任务状态

| 任务 | 操作 / 类型 | 目标文件 | 最终状态 |
|---|---|---|---|
| T05-10 控制面故障、平台恢复与账本核对 | 新增 / procedure | `knowledge/05-cluster-platform/control-plane-recovery.md` | **通过审阅**：初审 10 项（8 P2/2 P3）＋复核新发现 R01/R02，初审＋4 轮定向复核后全部 CLOSED；etcd 灾备/主备切换的官方自动化测试负结果如实保留 |
| T06-01 补齐并行策略选择、专家并行与组合映射 | 修订 / concept | `knowledge/06-training/parallelism-and-state.md` | **通过审阅**：初审 9 项＋R01/S3-01/S4-01，初审＋5 轮定向复核后全部 CLOSED；原状态责任矩阵/身份/截取边界章节经回归抽查保持 |
| T06-02 训练框架组件、执行循环与平台职责对照 | 新增 / reference | `knowledge/06-training/framework-execution.md` | **通过审阅**：初审 9 项＋R01/S3×3，初审＋4 轮定向复核后全部 CLOSED |
| T06-03 预训练与微调工作流和状态契约 | 新增 / concept | `knowledge/06-training/pretraining-and-finetuning.md` | **通过审阅**：初审 9 项＋R01/R02/R03/S2-01/S3-01，初审＋4 轮定向复核后全部 CLOSED |

## 来源准备

- 新增登记 **23** 项，`sources/registry.yaml` 由 470 增至 **493**（无重复 ID）；另对 `src.slurm.testsuite-24-11-7-1`、`src.nvidia.megatron-examples-core-v0.12.1`、`src.nvidia.megatron-model-configs-core-v0.19.2`、`src.hf.peft-source-v0.7.1` 补充核对记录，并更正 `src.ascend.mindspeed-llm-training-interface-v2.2.0` 的整除方向措辞、`src.etcd.disaster-recovery-v3.5-docs` 的工件分类口径。
- 单任务来源记录：`docs/research/batch-24-t05-10-sources.md`（K8s v1.32 快照 5 页＋Slurm 24.11.7 归档 6 页，curl 字节级＋SHA-256；etcd v3.5 灾备指南；MindCluster v26.1.1 clusterd/operator README）、`batch-24-t06-01-sources.md`（PyTorch v2.6.0 DeviceMesh/CP 源码、Megatron core_v0.19.2 parallel_state/arguments、MindSpeed-LLM v2.2.0 并行特性与 MoE 脚本）、`batch-24-t06-02-sources.md`（Megatron 训练循环/调度/分布式优化器、PyTorch autograd/optim 文档、MindSpeed-LLM 训练入口与依赖表、PyTorch 官方测试三件）、`batch-24-t06-03-sources.md`（PEFT v0.7.1、Transformers v4.43.2、LoRA 论文摘要、Megatron core_v0.12.1/0.19.2 示例脚本、MindSpeed-LLM 三类工作流脚本）。
- 取证方式：curl 字节级取回（固定 tag/commit/静态快照）＋codeload 源码包（MindSpeed-LLM v2.2.0、Megatron core_v0.12.1/0.19.2、Slurm slurm-24-11-7-1、mind-cluster v26.1.1）；全部 SHA-256 记录在案。**四路取证子代理因账户 403 失败，按 Batch 23 先例改由主会话作者角色直接取证**（同口径记录）。
- 取证限制：24.11.7 归档无 high_availability.html（404＋索引确认）；etcd/Slurm 主备切换的官方自动化测试未定位到（负结果保留）；MindSpeed core 仓本体、MindSpeed-LLM 在研组件配套、纯文本 LLM 的 Megatron SFT 专项脚本未取得（unknown）。

## 关键边界

- 三组训练档案严格分立：PyTorch 2.6 / Megatron core_v0.19.2 / MindSpeed-LLM v2.2.0（其 Mcore 依赖为 core_v0.12.1、PyTorch 2.7.1），两两不组成同一软件环境。
- HF 侧版本固定取自 MindSpeed-LLM v2.2.0 requirements（transformers 4.43.2、peft 0.7.1；install_guide 另注 4.51.0/4.54.0 按模型适用）。
- AMD：ROCm 7.1.1 兼容页与 PyTorch 2.6 HIP 文档为两条独立版本线；固定 HF 组合在 ROCm 的可执行性 unknown；不声明 Megatron/MindSpeed 可迁移。
- 厂商性能数字（MindSpeed CP 算法对照、CCLoRA 提升、moe 模型表）只作"来源记录"，不作本库结论；合成样例（组合身份、选型表、反例）全部显式标注"合成"。

## 结构检查

- `make check`：PASS（103 content entries / **493** sources）。`make build`：PASS。
- 只证明结构与本地链接，不证明技术正确性或远程内容。

## 审阅与复核

- 审阅模型：`codex exec -m gpt-6.1-sol --config model_reasoning_effort="xhigh"`（每轮调用方从 `~/.codex/sessions` 的 `turn_context` 核验单一模型/档位，全部轮次无 fallback 标记）。
- 轮次：初审 4 份＋定向复核 T05-10 4 轮、T06-01 5 轮（第六轮关闭最后单项）、T06-02 4 轮、T06-03 4 轮；全部发现（含各轮新增）累计 CLOSED。
- 审阅者独立重开上游证据并比对 SHA-256；两处作者错误断言由审阅链纠正（core_v0.19.2 目录缺失误判、CLI 无定义误判），修订记录见各 sources 文档与 recheck 报告。
- **最终结论**：四任务均通过既定审阅与定向复核范围；模型审阅不替代真实硬件、训练、恢复或灾备演练，正文保持 `draft`。
