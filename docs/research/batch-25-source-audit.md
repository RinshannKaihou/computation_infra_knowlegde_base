# 第二十五批来源审计（T06-04/T06-05/T06-06/T06-07）

更新日期：2026-10-20。状态：**Batch 25 已交付并通过审阅**；四篇正文均为 `draft`，未做真实环境验证。

## 本批任务状态

| 任务 | 操作 / 类型 | 目标文件 | 最终状态 |
|---|---|---|---|
| T06-04 RL rollout、权重同步与训练推理协同 | 新增 / concept | `knowledge/06-training/rl-rollout-consistency.md` | **通过审阅**：初审 11 项（2 P1/8 P2/1 P3）＋复核新增 R01–R03/S2-01，初审＋4 轮定向复核后累计 15 项全部 CLOSED；V0/V1 实现线、staleness 预算语义、delta 两跳与整作业重启、失败重放一致性、样本字段条件契约（产出/存在/必需分列）均经重开上游核对 |
| T06-05 混合精度、算子适配与收敛验证 | 新增 / procedure | `knowledge/06-training/mixed-precision-and-convergence.md` | **通过审阅**：初审 9 项＋R01，初审＋3 轮定向复核后累计 10 项全部 CLOSED；GradScaler step/update 职责、Megatron hysteresis 完整状态机（含唯一复位分支与三类静态序列）、found_inf 私有插桩边界、跳步率统计契约（分子分母与未确认事件）均经固定源码核对 |
| T06-06 训练性能分解、profiling 与优化验证 | 新增 / procedure | `knowledge/06-training/performance-analysis.md` | **通过审阅**：初审 7 项＋R01，初审＋4 轮定向复核后累计 8 项全部 CLOSED；nsys 版本锚更正（Dockerfile.stable.sglang＝2025.6.1，指南自述的 Dockerfile.vllm.sglang.megatron 在 v0.9.1 不存在）、收益测量与质量观察协议、A→B→A 恢复复测、组合并行候选对照的组成员具体填写均经独立复算 |
| T06-07 训练吞吐回归的公开证据案例 | 新增 / case | `knowledge/06-training/performance-regression-source-case.md` | **通过审阅**：初审 8 项（1 P1/5 P2/2 P3）＋R01，初审＋3 轮定向复核后累计 9 项全部 CLOSED；#192551 由"次生回归"更正为同期独立 MPS 镜像问题（先于修复存在并关闭）、#188236 创建 2026-06-26 早于 issue 且经 MergeBot 落地、140baa4eec85 实为仅注释 diff、author/committer 时间字段分列均经 gh API 复核 |

## 来源准备

- 新增登记 **32** 项，`sources/registry.yaml` 由 493 增至 **525**（无重复 ID）：verl v0.9.1 相关 17 项（算法文档 2、架构/异步/扩展 4、源码 4、昇腾/AMD/安装文档 4、profiling 指南 3）、论文摘要 4 项（PPO/GRPO/DPO/HybridFlow）、PyTorch AMP 源码/测试 2 项、Megatron loss scale 1 项、案例链 1 项、Nsight 归档 1 项、TorchNPU profiler 源码 1 项、Megatron training_log 1 项；复核轮补登 delta 传输源码组与 rollout_correction 配置 2 项、verl 主安装文档 1 项；另修订轮更正既有三条（verl ray-trainer/fully-async、Megatron grad-scaler、GradScaler、amp-tests、两条论文 notes）的事实表述。
- 单任务来源记录：`docs/research/batch-25-t06-04-sources.md`（verl v0.9.1 codeload 包 cef878a5＋MindSpeed-LLM v2.2.0 包复核＋四篇 arXiv API 摘要，含修订轮四段）、`batch-25-t06-05-sources.md`（v2.6.0 GradScaler 源码/测试、core_v0.19.2 优化器、#200537 案例链）、`batch-25-t06-06-sources.md`（Nsight 2025.3 归档目录页、verl profiling 三指南、TorchNPU profiler、Megatron training_log/timers、Dockerfile.stable.sglang）、`batch-25-t06-07-sources.md`（#189239 全链 gh API 观察：issue/PR/commit/次生 issue，含备选淘汰记录）。
- 取证方式：codeload 源码包＋raw 固定 commit＋arXiv API＋gh API（issue/PR/commit 元数据与 diff）；全部 SHA-256 记录在案。审阅者独立重开上游并复算 blob/SHA（T06-04 轮核 24＋26 个文件全部一致）。
- 取证限制：Nsight 2025.3 user-guide 子页双路径 403（工具细节不转述）；hiascend msprof 页面需 JS 渲染未取得（保持 unknown）；verl 昇腾安装指南内部 post2/post4 冲突未消解（unknown 分列）；AMD 自建镜像 VERL_TAG≠v0.9.1。

## 关键边界

- verl 机制证据固定于 v0.9.1 的 **legacy（V0）recipe**（ray_trainer 自标 deprecated；同 tag 默认入口 V1 use_v1: true 未逐行核对）；V0 默认 logprob 路径为 **decoupled**（rollout_correction.bypass_mode 默认 false），bypass 为显式启用模式。
- `staleness_threshold` 为同步周期内样本生产预算（非逐样本版本滞后硬上限）；delta 更新限 vLLM rollout 消费端 DP=1/PP=1/CUDA/BF16（排除量化/投机/PD 分离），上次 delta 未完成须整作业重启重收 dense seed。
- 三组混合精度实现分立（PyTorch 2.6 GradScaler / Megatron core_v0.19.2 DynamicGradScaler 含 hysteresis 状态机 / MindSpeed --initial-loss-scale）；ROCm 已知不支持项限定在 PyTorch 2.7/2.8＋ROCm 7.0/7.1 节内两个完整字段。
- 工具取证受限如实记录：Nsight 只有目录级证据＋verl 使用面（配套 2025.6.1）；msprof 命令不写；正文未转述任何未取得的命令细节。
- 案例事实三分（作者报告/源码推断/本库未复现）贯穿 T06-07；#192551 为同期独立 MPS 镜像问题（非次生回归）；基准数字（178.41/141.91ms、20%+、4.5×/9×、1.3×）全部为上游报告。
- 合成样例（组合并行候选对照 A/B 的组员推导、hysteresis 三序列）均显式标注"源码/算术推导，未运行"。

## 结构检查

- `make check`：PASS（107 content entries / **525** sources）。`make build`：PASS。
- 只证明结构与本地链接，不证明技术正确性或远程内容。

## 审阅与复核

- 审阅模型：`codex exec -m gpt-6.1-sol --config model_reasoning_effort="xhigh"`（每轮调用方从 `~/.codex/sessions` 的会话记录核验单一模型/档位；审阅报告自身声明无法读取运行元数据的轮次如实记录为约定标识，调用方核验结果为准）。
- 轮次：初审 4 份；定向复核 T06-04 4 轮、T06-05 3 轮、T06-06 4 轮、T06-07 3 轮；全部发现（含各轮新增）累计 CLOSED，四任务均声明**通过既定审阅范围**。
- 审阅链纠正的作者错误包括：staleness 语义误写为版本上限（P1）、失败恢复一致性缺失（P1）、#192551 误写为次生回归（P1）、V0 默认路径误写为 bypass、delta 限制误安到训练侧、恢复步号误写为 0、nsys 版本锚指向不存在的 Dockerfile、140baa4eec85 message/diff 混淆、frontmatter summary 被 `#` 截断等；修订记录见各 sources 文档与 recheck 报告。
- **最终结论**：四任务均通过既定审阅与定向复核范围；模型审阅不替代真实硬件、训练、rollout、profiling 或回归复现，正文保持 `draft`。
