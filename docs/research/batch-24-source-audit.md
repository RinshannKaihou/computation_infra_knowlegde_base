# 第二十四批来源审计（T05-10/T06-01/T06-02/T06-03）

更新日期：2026-10-19。状态：**Batch 24 已交付并通过审阅**；四篇正文均为 `draft`，未做真实环境验证。

## 本批任务状态

| 任务 | 操作 / 类型 | 目标文件 | 最终状态 |
|---|---|---|---|
| T05-10 控制面故障、平台恢复与账本核对 | 新增 / procedure | `knowledge/05-cluster-platform/control-plane-recovery.md` | **通过审阅**：初审 10 项（8 P2/2 P3）＋复核新发现 R01/R02，初审＋4 轮定向复核后全部 CLOSED；etcd 灾备/主备切换的官方自动化测试负结果如实保留 |
| T06-01 补齐并行策略选择、专家并行与组合映射 | 修订 / concept | `knowledge/06-training/parallelism-and-state.md` | **通过审阅**：初审 9 项＋R01/S3-01/S4-01，初审＋6 轮定向复核后全部 CLOSED；原状态责任矩阵/身份/截取边界章节经回归抽查保持 |
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
- 轮次：初审 4 份＋定向复核 T05-10 4 轮、T06-01 6 轮、T06-02 4 轮、T06-03 4 轮；全部发现（含各轮新增）累计 CLOSED。
- 审阅者独立重开上游证据并比对 SHA-256；两处作者错误断言由审阅链纠正（core_v0.19.2 目录缺失误判、CLI 无定义误判），修订记录见各 sources 文档与 recheck 报告。
- **最终结论**：四任务均通过既定审阅与定向复核范围；模型审阅不替代真实硬件、训练、恢复或灾备演练，正文保持 `draft`。

## 交付后复查（2026-10-19）

- 用户告知本批正文、来源记录与收尾账面由 GLM-5.3 编写；原记录未写明编写模型，此处补记。复查与修订由 `claude-opus-5-5` 在用户要求下执行，定向复核仍为 codex `gpt-6.1-sol / xhigh`。
- 复查确认 22 轮原审阅会话真实存在且报告未被改动；发现 6 项（B24-PC-01–06）：收尾账面缺口/evidence_refs/盘点表未同步，06.2、06.4 依赖 Batch 25 任务却记为已覆盖，T06-01 专家 grid 轴序与 Megatron 默认相反，三情形表拼接 PyTorch 与 Megatron 的 scaler 语义，融合 QKV offset 与切分术语错误，06 导航双句号。
- 处理后：05.7、06.3 为已覆盖（基础），06.2 保持部分覆盖，06.4 由未覆盖升为部分覆盖；8 个缺口关闭、3 个保持 open。逐项证据与关闭条件见 [batch-24-post-close-review](batch-24-post-close-review.md)，定向复核见 [第一次](batch-24-post-close-codex-recheck.md)（关闭 5 项，PC-04 未关闭并新增 R01/R02）与 [第二次](batch-24-post-close-codex-recheck-2.md)（PC-04、R01、R02 全部关闭，无新增问题）；两轮均为 codex `gpt-6.1-sol / xhigh`，经 `turn_context` 核验。
- 遗留处理（第二轮）：B24-PC-07–10（轮次口径、05.2 账面、覆盖统计、四篇正文可读性重排）见 [batch-24-post-close-review](batch-24-post-close-review.md)；复核见 [第三次](batch-24-post-close-codex-recheck-3.md)（PC-09 因两项 P3 未关闭）、[第四次](batch-24-post-close-codex-recheck-4.md)（R3-01/R3-02 关闭，新增 R4-01）与[第五次](batch-24-post-close-codex-recheck-5.md)（PC-09、R4-01 关闭，第二轮遗留处理全部 CLOSED）。
