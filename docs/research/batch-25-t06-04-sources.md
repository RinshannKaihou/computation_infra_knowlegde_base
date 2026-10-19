# 第二十五批 T06-04 来源记录

任务：T06-04（RL rollout、权重同步与训练推理协同；**new** concept `knowledge/06-training/rl-rollout-consistency.md`，主题 06.4）。取证轮次：主会话作者角色首轮（2026-10-20）。RL 系统样板固定 **verl v0.9.1**（codeload 源码包字节级取回）；论文经 arXiv API 摘要级取证；GitHub issue/PR 经 gh API 观察。未运行任何 RL 训练/rollout/权重同步命令。

版本选择口径：verl 选 tag v0.9.1（2026-09-20 发布的最新正式 release），全部文档/源码坐标锚定该 tag。verl 昇腾教程给出的配套线（vLLM/vLLM-Ascend 0.23.0、torch 2.10.0、torch_npu 2.10.0.post2、CANN 9.1.0）与本库既有登记的 vllm-ascend v0.14.0rc1、TorchNPU 7.2.0 属**不同版本线，不互推**。DPO/GRPO/PPO 论文仅引用方法与作者报告。

## 本轮取回清单（2026-10-20）

| 对象 | 版本 | SHA-256（前 16 位） |
|---|---|---|
| verl codeload 源码包 | v0.9.1 | cef878a5ccc98491 |
| docs/algo/ppo.md | v0.9.1 | 48fe658d2c04ddef |
| docs/algo/grpo.md | v0.9.1 | d43fb13fba50523c |
| docs/hybrid_flow.rst | v0.9.1 | e6328517392492c7 |
| docs/advance/fully_async.md | v0.9.1 | 61676351b33d69f0 |
| docs/advance/one_step_off.md | v0.9.1 | 34046471c0a624c8 |
| docs/advance/dpo_extension.rst | v0.9.1 | be13186cb5743bfd |
| verl/workers/rollout/vllm_rollout/vllm_rollout.py | v0.9.1 | e82e1c6782573e03 |
| verl/trainer/ppo/ray_trainer.py | v0.9.1 | eb41f99ccc66976e |
| docs/ascend_tutorial/zh/get_start/install_guidance.rst | v0.9.1 | 43ff1fe767964f19 |
| docs/ascend_tutorial/zh/feature_support/ascend_backend_features.md | v0.9.1 | a1eeb19d979318d5 |
| docs/amd_tutorial/amd_quick_start.rst | v0.9.1 | f7cbcab68c3e05c7 |
| docs/perf/best_practices.rst | v0.9.1 | 5cf6cfd9c6d84668 |
| arXiv:1707.06347 摘要（API XML） | 取回 2026-10-20 | f7087c34c5c97448 |
| arXiv:2402.03300 摘要（API XML） | 取回 2026-10-20 | d4748da9ecf80f6a |
| arXiv:2305.18290 摘要（API XML） | 取回 2026-10-20 | fa8dde2b70effe36 |
| arXiv:2409.19256 摘要（API XML） | 取回 2026-10-20 | 7da97dafe798a88d |
| MindSpeed-LLM codeload 源码包（trl_ppo） | v2.2.0 | 693f619a8b608726 |
| mindspeed_llm/tasks/posttrain/trl_ppo/TrlPPOTrainer.py | v2.2.0 | da079a2e1ee73bb4 |
| mindspeed_llm/tasks/posttrain/trl_ppo/TrlPPOEngine.py | v2.2.0 | 2b2fa41eb05a06ef |

MindSpeed-LLM v2.2.0 的 mindspeed_llm/training/training.py 本次复核 SHA-256 341c0792…，与 Batch 24 已登记的 src.ascend.mindspeed-llm-training-interface-v2.2.0 一致（补充核对其 get_profiler 基于 torch_npu.profiler，不新增条目）。

## 主张—来源定位表

| 主张 | 登记 ID | 精确位置 | 支持范围 / 未覆盖 |
|---|---|---|---|
| PPO 机制与配置语义 | NEW src.verl.ppo-doc-v0.9.1 | ppo.md（Key Components/Configuration/KL 控制节） | Actor-Critic+GAE+clip、train_batch_size 为 prompt 级全局 batch、响应数=train_batch_size×rollout.n、micro_batch_size 只控内存不改变算法行为、ppo_mini_batch_size/ppo_epochs/clip_ratio、KL loss 与 in-reward penalty 双机制 | 
| GRPO 机制与聚合口径 | NEW src.verl.grpo-doc-v0.9.1 | grpo.md | 无 critic、组采样 rollout.n>1、组内归一化 baseline；**loss_agg_mode 默认 token-mean 而原始论文为 seq-mean-token-mean**（实现与论文口径差异） |
| 两层 dataflow/单控制器 | NEW src.verl.hybrid-flow-v0.9.1 | hybrid_flow.rst（Design Choices 节） | 控制流（RL 算法逻辑）与计算流（训练引擎多进程）分层；单控制器+RPC 驱动多进程的设计选择 |
| 完全异步样板（分离架构） | NEW src.verl.fully-async-v0.9.1 | fully_async.md | Rollouter/Trainer 资源隔离、0.x–多步异步、NCCL 参数同步、staleness_threshold 新鲜度控制、PartialRollout sleep/resume；2.35–2.67× 为作者环境数字不外推 |
| 受控一步异步 | NEW src.verl.one-step-off-v0.9.1 | one_step_off.md | 同步训练的长尾空闲问题、上一步样本并行当前训练（一步 off-policy）；DAPO 32B rollout≈70% 时间为作者观察 |
| DPO 在线化对照 | NEW src.verl.dpo-extension-v0.9.1 | dpo_extension.rst | Online DPO 流程（同权重生成器→verifier 配对→DPO 损失）；与 PPO 的 ratio/KL 机制差异 |
| 权重同步机制（vLLM rollout） | NEW src.verl.vllm-rollout-source-v0.9.1 | vllm_rollout.py：resume/release L195–208、update_weights L210–253、_update_delta_weights L255+ | wake_up(tags)/sleep()（sleep mode）；named_tensors（collective_rpc update_weights_from_ipc＋BucketedWeightSender 分桶，ZMQ/共享内存）与 delta_flush（要求共置 CUDA IPC）双 wire_format；更新后 clear_kv_cache＋set_global_steps（推理侧权重版本） |
| 训练循环职责 | NEW src.verl.ray-trainer-source-v0.9.1 | ray_trainer.py：fit() L1405+ | 单控制器循环；启动即 _load_checkpoint＋update_weights 对齐推理权重；val_before_train 默认 True；global_steps 贯穿 checkpoint/验证/dump；old_log_probs 参与优势计算 |
| verl×Ascend 官方支持 | NEW src.verl.ascend-install-v0.9.1＋src.verl.ascend-features-v0.9.1 | install_guidance.rst（版本表）、ascend_backend_features.md（参数映射表） | vllm/sglang 后端均可在 NPU 运行；vLLM 经 vllm-ascend 插件；verl 参数↔vLLM 参数映射（gpu_memory_utilization/enforce_eager/free_cache_engine/tp_size=rollout.TP×DP 等） |
| verl×AMD 入口存在性 | NEW src.verl.amd-quickstart-v0.9.1 | amd_quick_start.rst | ROCm 侧 quick start 存在；具体 MI×vLLM×ROCm 版本交集未逐条核对（unknown） |
| off-policy 权衡官方口径 | NEW src.verl.perf-best-practices-v0.9.1 | best_practices.rst | train_batch_size 增大→rollout 次数减少但 off-policy drift 增加 |
| PPO 论文方法 | NEW src.paper.ppo-1707.06347 | arXiv 摘要 | clipped surrogate objective 免二阶导；仅方法与作者报告 |
| GRPO 论文方法 | NEW src.paper.grpo-deepseekmath-2402.03300 | arXiv 摘要 | 组内平均奖励为 baseline、免除 critic；摘要级取证，组归一化细节以论文原文为准 |
| DPO 论文方法 | NEW src.paper.dpo-2305.18290 | arXiv 摘要 | 偏好目标等价改写为直接损失，跳过 reward 模型与 RL 采样循环 |
| HybridFlow 系统论文 | NEW src.paper.hybridflow-2409.19256 | arXiv 摘要 | verl 的混合编程模型出处；吞吐对比为作者环境 |
| MindSpeed-LLM PPO 训练器 | NEW src.ascend.mindspeed-llm-trl-ppo-v2.2.0 | TrlPPOTrainer.py（复用 Megatron training_log/timers/forward_backward_func）、TrlPPOEngine.py（rollout_batch 字段：context_length/actor_logprobs/ref_logprobs/values/scores、compute_advantages_and_returns） | Ascend 侧基于 Megatron 循环的 PPO 实现；采样引擎细节未核对（unknown） |
| rollout 引擎侧背景 | 复用 src.vllm.inference-v0-14、src.ascend.vllm-ascend-v0-14-0rc1、src.vllm.plugin-system-v0-14 | （既有） | vLLM 执行/插件边界；本轮未重开 |
| 并行与状态基础 | 复用 src.pytorch.parallel-training-state-2.6 | （既有） | TP/DP 映射与训练状态责任 |

## unknown 清单

1. verl 的 core_algos.py（adv_estimator 实现）、sglang_rollout 源码未逐行核对（正文以文档口径为准）。
2. verl×Ascend 的具体机型（910B/Atlas 等）×CANN 9.1.0 交集未逐条核对；安装指南版本表为文档声明，未实测。
3. vllm-ascend 0.23.0 线与既有登记的 0.14.0rc1 线分立，两者间行为差异未核对。
4. AMD/ROCm 侧仅确认 quick start 存在；MI 系列×vLLM×ROCm 的 RL 训练组合未验证。
5. MindSpeed-LLM TRL PPO 的 rollout 推理后端（generate 路径）与权重同步方式未逐文件核对。
6. fully_async 的 NCCL 参数同步引用 MoonshotAI checkpoint-engine，该外部仓库未取证。
7. 全部代码未运行；吞吐提升倍数、rollout 时间占比等数字均为作者报告。

## 修订轮补充取证（2026-10-20，初审 B25-T04-C01–C11 后）

审阅者（gpt-6.1-sol / xhigh）重开的上游证据与作者据此的补充核对：

| 对象 | 版本 | 说明 |
|---|---|---|
| docs/start/install.rst（8ca5ce30c91222bc） | v0.9.1 | **新增登记 src.verl.install-v0.9.1**（C06）：Python>=3.10、CUDA>=12.8；训练后端 FSDP/FSDP2＋Megatron-LM（声明 core_v0.13.1）；推理 vLLM>=0.18.0（更早不可用）/SGLang/TGI |
| amd_quick_start.rst 细读（f7cbcab68c3e05c7） | v0.9.1 | **登记 notes 补充**（C06）：Fully Async/Colocate、vLLM/SGLang、FSDP/FSDP2/Megatron、gfx942/gfx950、镜像 amdagi/verl-dev:rocm7.14_torch2.12_release_0724、ROCm 7.14 宿主 |
| verl/trainer/config/ppo_trainer.yaml、main_ppo.py | v0.9.1 | 审阅者核对（C08）：默认 `use_v1: true`，V1 模式 sync/colocate_async/separate_async；ray_trainer.py 自标 legacy deprecated；v0.9.1 release 注明旧 experimental fully-async/one-step 下版迁出。正文已加实现线声明 |
| verl/experimental/fully_async_policy/fully_async_rollouter.py L491–507 | v0.9.1 | 审阅者核对（C01）：`staleness_threshold` 为同步周期内样本预算（`(1+staleness_threshold)×(trigger_parameter_sync_step×require_batches×ppo_mini_batch_size)−num_staleness_sample`），非逐样本版本硬上限。正文已改 |
| verl/workers/rollout/vllm_rollout/delta_weight_transfer.py L216–240、delta_checkpoint_engine.py | v0.9.1 | 审阅者核对（C02/C04）：delta 限 CUDA/BF16/DP=1/PP=1、排除量化/投机解码/PD 分离；跨组可 NCCL＋本地 IPC 两跳；**上次 delta 未完成须整作业重启并重收 dense seed**。正文已改 |
| ray_trainer.py L218–279、L1426–1491、L1570–1674 | v0.9.1 | 审阅者核对（C03/C07）：GAE 输入 rewards/values/mask、GRPO 按 uid 组归一化；bypass 与 decoupled 两路径；恢复后首发布步号 0 与 trace 步号 1 的计数差异；path-variance 属 optimal-token-baseline 分支。正文已改 |
| install_guidance.rst L84–101 | v0.9.1 | 审阅者核对（C05）：组件表 torch_npu 2.10.0.post4/HDK 26.0.rc1 与更新条目 post2 冲突，未消解，正文按 unknown 分列 |
| fully_async.md L79–125 | v0.9.1 | 审阅者核对（C09）：streaming 下 train_batch_size 不生效；分离后单阶段可能更慢、收益来自重叠；工作量对齐关系。正文验证方法已改 |

修订后正文重写为"实现线声明＋闭环图＋失败重放一致性规则＋样本契约键"结构；论文引用收窄为摘要级承载（C10）。四篇论文摘要主张与 verl 文档的分工已在正文与登记 notes 中分列。

## 第三轮修订（2026-10-20，复核轮二 C01–C10/R01–R03 后）

- **R01/C03**：正文 logprob 段更正——V0 默认为 decoupled（`rollout_correction.yaml` bypass_mode 默认 **false**，IS/RS 校正默认 null）；bypass 为显式启用模式。**新增登记 src.verl.rollout-correction-config-v0.9.1**（rollout_correction.yaml 25e3a347…）。
- **R02/C04**：delta 限制更正为消费端（vLLM rollout DP=1/PP=1/CUDA/BF16/排除量化/投机/PD）与生产端（训练侧分片汇聚支持非 DP=1）分列；删除 LoRA 适用暗示（FSDP 导出路径注明 Non-LoRA base path）。**新增登记 src.verl.delta-transfer-source-v0.9.1**（delta_weight_transfer/delta_checkpoint_engine/vllm_async_server/fsdp transformer_impl 四文件）。
- **R03/C07**：恢复后首发布步号为 K（0/1 只是从零启动特例）；数据契约改为最小字段表（上游产出 vs 本库建议分列，含 sample_id/attempt/run 代次/update 提交键）；同步模式零滞后按权重身份归一化定义。
- **C01**：预算公式扣减项更正为"上轮超额携入的旧样本"；一步 off-policy 单位更正为"采样/训练轮次（内含多次 optimizer 更新）"。
- **C02**：补停止/隔离触发（冻结新采样/更新/发布、隔离队列与 in-flight）、账本-checkpoint 一致性（恢复旧 checkpoint 连账本回滚）、"更新已执行结果未知/未持久化"分支（save_freq 条件式保存）、重放复用范围与 reward 重试不重复计入、GRPO 组归属保持。
- **C06**：NVIDIA 安装页多版本线并存（core_v0.13.1 声明 vs uv 路径 core_v0.18.0/megatron-bridge 0.5.2）、docker GB200/aarch64 无预构建、Dockerfile.stable.vllm VERL_VERSION=v0.7.1；AMD 自建 Dockerfile.rocm 的 VERL_TAG=7b19203c≠v0.9.1 commit；"本页全部机制证据来自该组合"改为"取自 v0.9.1 文档/源码，不等于任一安装组合已验证"。
- **C10**：PPO 摘要引用收窄为 surrogate objective＋多 epoch minibatch（clipped 归 verl 文档）；registry 三条论文 notes 同步收窄；`src.verl.ray-trainer-source-v0.9.1` 删除"GAE path-variance 代理"误读（该分支属 optimal-token-baseline），`src.verl.fully-async-v0.9.1` 的 staleness 表述改为预算控制。

## 第四轮修订（2026-10-20，复核轮三 C07/C10/S2-01 后）

- **C07/S2-01**：数据契约表补关联规则——prompt 身份（数据集 id＋索引或文本哈希，保证输入可回取）、sample_id＝(uid, i) 与 attempt 正交（重试递增 sample_id 不变）、reward/logprob 绑定 (sample_id, attempt)；条件式产出字段标 ◇（old_logprob 模式条件、ref_log_prob 仅启用 reference/in-reward KL、values 仅 PPO+GAE）。
- **C10**：DeepSeekMath 表述改为摘要原文口径（"PPO 的变体、在增强数学推理的同时优化 PPO 的内存使用"）；src.paper.ppo-1707.06347 notes 按摘要原文重写（去掉摘要未建立的对比表述）；src.paper.grpo-deepseekmath-2402.03300 notes 同步收窄。
