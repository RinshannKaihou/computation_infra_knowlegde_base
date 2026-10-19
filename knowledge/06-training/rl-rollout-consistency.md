---
id: training.rl-rollout-consistency
title: RL rollout、权重同步与训练推理协同
type: concept
domain: training
status: draft
platforms: [generic]
source_refs:
- src.verl.ppo-doc-v0.9.1
- src.verl.grpo-doc-v0.9.1
- src.verl.hybrid-flow-v0.9.1
- src.verl.fully-async-v0.9.1
- src.verl.one-step-off-v0.9.1
- src.verl.dpo-extension-v0.9.1
- src.verl.vllm-rollout-source-v0.9.1
- src.verl.delta-transfer-source-v0.9.1
- src.verl.rollout-correction-config-v0.9.1
- src.verl.ray-trainer-source-v0.9.1
- src.verl.perf-best-practices-v0.9.1
- src.verl.install-v0.9.1
- src.verl.ascend-install-v0.9.1
- src.verl.ascend-features-v0.9.1
- src.verl.amd-quickstart-v0.9.1
- src.paper.ppo-1707.06347
- src.paper.grpo-deepseekmath-2402.03300
- src.paper.dpo-2305.18290
- src.paper.hybridflow-2409.19256
- src.ascend.mindspeed-llm-trl-ppo-v2.2.0
- src.vllm.inference-v0-14
- src.pytorch.parallel-training-state-2.6
updated_at: "2026-10-20"
summary: 以 verl v0.9.1（legacy V0 recipe 为机制样板，V1 入口并陈）解释在线 RL（PPO/GRPO）的采样—打分—更新—发布闭环、权重同步与陈旧样本的预算控制、同步与受控异步的代价、失败与重放的一致性规则，以及 rollout 一致性与吞吐的观察、异常区分和单变量验证方法；DPO 仅作离线对照。
related_ids:
- training.pretraining-and-finetuning
- training.parallelism-and-state
- training.framework-execution
- training.checkpoint-state-consistency
- training.slow-rank-triage
- inference.execution-and-kv-cache
verification:
  status: source_checked
  evidence_refs:
  - src.verl.vllm-rollout-source-v0.9.1
  - src.verl.delta-transfer-source-v0.9.1
  - src.verl.rollout-correction-config-v0.9.1
  - src.verl.ray-trainer-source-v0.9.1
  - src.verl.fully-async-v0.9.1
  - src.verl.ascend-features-v0.9.1
  notes: 仅核对 verl v0.9.1 固定 tag 文档/源码（含审阅轮补开的 delta 传输/V1 配置/安装页）、四篇论文摘要与 MindSpeed-LLM v2.2.0 源码（锚点见 docs/research/batch-25-t06-04-sources.md 与审阅报告）；未运行任何 RL 训练、rollout、权重同步或基准，文中性能数字均为来源作者报告。
---

# RL rollout、权重同步与训练推理协同

本页解释强化学习后训练（RL post-training）如何把**训练引擎与推理引擎放进同一个闭环**：采样（rollout）用推理引擎执行，更新（update）用训练引擎执行，两者之间必须交换权重与样本数据。工作流背景见[预训练与微调工作流和状态契约](pretraining-and-finetuning.md)，并行布局见[并行策略与训练状态](parallelism-and-state.md)，rollout 引擎内部机制引用 07 章。

**实现线声明**：本页机制证据固定于 verl v0.9.1 的 **legacy（V0）recipe 与 `ray_trainer.py` 循环**（该源码自身标注 legacy deprecated；本批另核对到同一 tag 的默认入口已启用 V1：`ppo_trainer.yaml` 默认 `use_v1: true`，异步模式列为 sync/colocate_async/separate_async，v0.9.1 release 说明旧 experimental fully-async/one-step 将在下一版迁出但本 tag 未删除）。V1 的实际控制流未逐行核对；本页把 V0 机制当作**结构样板**解释通用契约，参数名与默认值以所选实现线的配置为准，不能把 V0 参数直接当作 V1 配置使用。

## 定义与要解决的问题

先区分三类后训练工作流。它们共享"基座权重＋数据"，但循环结构不同：

| 工作流 | 循环结构 | 是否需要推理引擎在线采样 | 权重同步需求 |
|---|---|---|---|
| SFT（监督微调） | 数据预先静态存在→直接训练 | 否 | 无（单一训练引擎） |
| 离线偏好优化（DPO 选样） | 偏好对预先构造→直接训练 | 否（偏好数据可离线生产） | 无 |
| 在线 RL（PPO/GRPO 选样） | 每批样本由**当前策略**生成→打分→更新→发布新策略→再采样 | 是 | **每轮把训练权重发到推理引擎** |

DPO 论文（[arXiv:2305.18290 摘要](https://arxiv.org/abs/2305.18290)）把偏好优化目标改写为对策略的直接损失、跳过显式 reward 模型与 RL 采样循环——这是与 PPO 的结构性差别，不是"更好的 PPO"。verl 的 Online DPO 扩展（[dpo_extension.rst](https://github.com/volcengine/verl/blob/v0.9.1/docs/advance/dpo_extension.rst)）演示了另一种组合：用与 actor 同权重的生成器在线采样、verifier 打分配对、再走 DPO 损失更新——它有采样循环但没有 PPO 的 ratio 与 KL-in-reward 机制。PPO 论文（[arXiv:1707.06347 摘要](https://arxiv.org/abs/1707.06347)）提出 surrogate objective 与多 epoch minibatch 更新（clipped 形式等细节以 [verl PPO 文档](https://github.com/volcengine/verl/blob/v0.9.1/docs/algo/ppo.md)的实现口径为准）；GRPO 由 DeepSeekMath 提出（[arXiv:2402.03300 摘要](https://arxiv.org/abs/2402.03300)称其为 PPO 的变体、在增强数学推理的同时优化 PPO 的内存使用；组归一化等机制细节以 [verl GRPO 文档](https://github.com/volcengine/verl/blob/v0.9.1/docs/algo/grpo.md)为准）。摘要级论文引用只承载论文确实写出的内容。

verl 文档把 RL 训练表述为两层 dataflow（[hybrid_flow.rst](https://github.com/volcengine/verl/blob/v0.9.1/docs/hybrid_flow.rst)）：**控制流**（rollout→打分→优势计算→更新的算法逻辑）与**计算流**（每个模型的前向/反向/优化器，多进程实现）。系统论文 HybridFlow（[arXiv:2409.19256 摘要](https://arxiv.org/abs/2409.19256)）提出混合编程模型。"训练推理协同"的问题就具体化为：**控制流如何在正确的时间把正确版本的权重和样本数据送到正确的引擎组**。

### 闭环与数据从哪来

以同步 PPO/GRPO 为例（GRPO 无 critic；PPO 另有 critic 模型与 reference 可选）：

```
            ┌────────────────────────────────────────────────────┐
            │                    训练循环（控制流）                 │
            │                                                    │
  prompts ─▶│ ① 采样 rollout ──▶ ② 打分 reward ──▶ ③ 优势计算     │
            │   （推理引擎，       （reward 模型或      （GAE: rewards+values+mask │
            │    策略版本 v_k）     规则 verifier）      GRPO: 组内奖励归一化）   │
            │                                          │          │
            │                                          ▼          │
            │  ⑤ 发布新权重 ◀──────────────────────── ④ 更新 actor │
            │   （权重同步＋KV 作废；                    （＋PPO critic；│
            │    推理侧回到版本 v_{k+1}）                 logprob 锚点见下）│
            │       │                                            │
            └───────┼────────────────────────────────────────────┘
                    └──▶ 回到 ①：下一批 prompts 用新策略采样（回边）
```

三类工作流的数据来源对照：SFT/DPO 的训练样本在训练开始前已构造完成（静态偏好对或指令对）；在线 RL 的每个训练 batch 都由循环内的 ① 产出，样本的存在性与策略版本绑定。图中 ① 依赖"⑤ 发布的权重"，这是与普通训练唯一的结构性差异，也是本页其余各节的根源。

## 机制与关键关系

### 循环的五个环节

以 verl v0.9.1 的 PPO 配置（[ppo.md](https://github.com/volcengine/verl/blob/v0.9.1/docs/algo/ppo.md)）为准（V0 线）：

1. **采样（rollout）**：推理引擎按当前策略为每批 prompt 生成响应。`data.train_batch_size` 是 prompt 级全局 batch；响应数为 `train_batch_size × actor_rollout.ref.rollout.n`（GRPO 要求 `rollout.n > 1` 做组采样）。
2. **打分（reward）**：reward 模型或规则函数（verifier）为每条响应给出标量分数；数据必须与 reward 函数的 `data_source` 匹配（[best_practices.rst](https://github.com/volcengine/verl/blob/v0.9.1/docs/perf/best_practices.rst)）。规则 verifier 的"身份"是**其代码与配置版本**，不只是模型权重。
3. **参考与数值（logprob 家族）**：需要区分四类量——**rollout logprob**（采样时推理引擎实际策略的 logprob）、**`old_log_probs`**（训练侧的 proximal 锚点）、当前 actor 在更新时重算的 logprob（ratio 的分子，proximal 锚点为分母）、**`ref_log_prob`**（冻结 reference 模型）。V0 配置的默认路径是 **decoupled**（`rollout_correction.bypass_mode` 默认 `false`，训练侧重算 proximal 锚点；重要性权重/拒绝采样校正另有开关且默认 `null` 不自动启用，[rollout_correction.yaml](https://github.com/volcengine/verl/blob/v0.9.1/verl/trainer/config/algorithm/rollout_correction.yaml)）；**bypass（`old_log_probs`＝采样策略 logprob 的两策略模式）是显式启用的模式**。判定一致性时先确认所处模式：bypass 下 `old_log_probs` 应等于采样策略 logprob；decoupled 下两者本来就可不同（由训练侧重算），不能把差异当作异常。优势计算的直接输入按算法不同：GAE 用 rewards/values/mask，GRPO 按 uid 分组做组内归一化；reference 经 in-reward KL 惩罚间接影响 advantage，而 GRPO 的 actor KL loss 是损失项而非优势输入（[ppo.md](https://github.com/volcengine/verl/blob/v0.9.1/docs/algo/ppo.md)/[grpo.md](https://github.com/volcengine/verl/blob/v0.9.1/docs/algo/grpo.md)、[ray_trainer.py](https://github.com/volcengine/verl/blob/v0.9.1/verl/trainer/ppo/ray_trainer.py)）。
4. **优势与更新**：PPO 用 GAE＋clip（`ppo_mini_batch_size`、`ppo_epochs`、`clip_ratio` 默认 0.2）；GRPO 用组内归一化优势＋KL loss。`micro_batch_size` 只控制单次前反向的样本/token 上限以避免 OOM，**不改变算法行为**（两份算法文档均显式声明）。
5. **发布（publish）**：更新后的权重同步到推理引擎（机制见下节），采样回到 ①。

角色集合：actor（可训练策略）、critic（仅 PPO）、reference（冻结）、reward（可选）、rollout engine（推理后端）。verl 的角色可共置在同一组进程（colocate/hybrid engine）也可分离部署。

### 数据契约：一条样本必须绑定什么

一条 rollout 样本不只是 prompt＋response 文本。最小字段契约（标注产出/存在/必需条件与缺失处置，区分上游产出与本库建议自建）与关联规则：

| 字段 | 内容与关联 | 产出/存在/必需条件与缺失处置 |
|---|---|---|
| prompt 身份 | 数据集 id＋样本索引或 prompt 文本哈希（保证输入可回取比对）；组归属按 prompt uid 分组（GRPO） | 索引/哈希为本库建议必采；uid 上游产出 |
| response | 生成的 token 序列＋attention mask＋采样参数；**一条 prompt 的第 i 个响应记 `(uid, i)`** | 上游产出 |
| sample_id | ＝`(uid, i)`（样本身份，与 attempt 正交） | 本库建议自建（按上游 uid＋序号构造） |
| attempt | 同一 sample_id 的重试序号（重试递增、sample_id 不变）；**reward/logprob 均绑定到 `(sample_id, attempt)`** | 本库建议自建 |
| `old_log_probs`（proximal 锚点） | 更新时 ratio 的分母锚 | **必需**：所选更新路径不允许更新时缺失；模式只改变生产方式（decoupled 由训练侧重算、bypass 从 rollout 数值建立） |
| rollout logprob | 采样时推理引擎实际策略的 logprob | **条件式**：实际返回受采样配置与后端影响；decoupled 且依赖该量的 IS/RS 校正关闭时**可缺失**（记模式与开关，不判关联故障）；bypass 或启用依赖该量的校正时**必须取得**，缺失则拒绝进入该路径/停止更新，不得静默当作校正已生效 |
| 当前 actor logprob | 更新时由训练侧计算（ratio 分子） | 训练侧计算产物，不属于持久化样本字段（见环节 3，不与采样产物混列） |
| reward＋verifier 身份 | 分数（绑定 `(sample_id, attempt)`）＋规则函数代码/配置版本或 reward 模型权重身份 | 分数上游产出；verifier 版本为本库建议必采 |
| ref_log_prob＋reference 权重身份 | 冻结侧数值与权重标识 | **条件式（可判定分支）**：`algorithm.use_kl_in_reward` 或 `actor_rollout_ref.actor.use_kl_loss` 任一启用才需要 reference；两者均关闭时数值/身份记 `not_applicable`（或等价）并保留开关记录，不虚构数值 |
| values（critic 价值） | GAE 的价值输入 | **条件式**：默认样板下 PPO＋GAE 需要、GRPO（无 critic）不需要；存在 `critic.enable` 显式覆盖与 `need_critic()` 判定（本页限定描述默认样板，覆盖配置不在已取证范围） |
| 行为策略权重身份 | 采样时策略的 checkpoint/发布标识 | 上游仅有发布侧步号锚；完整标识为本库建议 |
| run / 恢复代次 | 作业运行与每次恢复的标识（防跨恢复混批） | 本库建议自建 |
| update 提交键 | 消费该样本的更新轮次标识（账本用） | 本库建议自建 |
| tokenizer 身份 | 两侧 tokenizer 版本（logprob 可比的前提） | 配置项，须记录 |

入口配置完整性检查（本库前置校验规则，不假设上游自动报错）：进入更新前核对"当前模式（bypass/decoupled）×校正开关×所需数值"的交集——启用依赖 rollout logprob 的路径而该数值缺失时停止；模式与开关随每批记录。该检查不能由全局"更新结果未知冻结"规则替代。

版本锚点的边界：verl 在推理侧维护的 `set_global_steps` 只是**发布侧的步号锚**——从零启动时首次发布为 0、下一轮采样 trace 为 1；从 checkpoint `global_step_K` 恢复时首次发布用 K、之后为 K+1（0/1 只是从零启动的特例）。步号标签**不等于**实际权重身份（同一步号可对应不同 run 的权重），策略滞后按行为策略权重身份与消费时身份归一化计算（同步模式恒为 0 的定义以此为准），不能仅凭两个步号标签相减。

### 权重同步：训练引擎 → 推理引擎

verl v0.9.1 的 vLLM rollout 适配（[vllm_rollout.py](https://github.com/volcengine/verl/blob/v0.9.1/verl/workers/rollout/vllm_rollout/vllm_rollout.py)）给出可核对的实现样板。传输路径分两跳看：**训练组 → checkpoint/同步组件 → rollout 引擎组**（跨组可为 NCCL 传输，delta 引擎在此显式汇聚训练分片），**rollout 引擎组内部 → 各推理 worker** 为本地 CUDA IPC/共享内存——"IPC"指最后一跳，不代表训练/推理两组资源必须共置：

- **全量/桶式更新**（`wire_format="named_tensors"`）：`collective_rpc` 下发 `update_weights_from_ipc`，`BucketedWeightSender` 按配置分桶经 ZMQ/共享内存发送；桶大小（`update_weights_bucket_megabytes`）是带宽与延迟的权衡旋钮。
- **增量更新**（`wire_format="delta_flush"`，V0 delta 引擎）：发送变化位置与值，最后一跳要求 rollout 侧本地 CUDA IPC 可达。固定实现的限制分属两侧记录（[delta 传输源码组](https://github.com/volcengine/verl/blob/v0.9.1/verl/workers/rollout/vllm_rollout/delta_weight_transfer.py)）：**消费端（vLLM rollout）限 CUDA/BF16、data parallel=1、pipeline parallel=1，排除量化、投机解码与 PD 分离**；**生产端（训练侧）**通过分片汇聚导出、支持非 DP=1 的训练布局（FSDP 导出路径的既有实现注明为 Non-LoRA base path——LoRA 的适用性不由该组证据建立，须另行取证）。
- **更新后的缓存处理**：权重更新后调用 `clear_kv_cache`——旧策略的 KV cache 对新策略无效；`set_global_steps` 记录发布步号（语义边界见上节）。
- **显存腾挪**：`release()`/`resume()` 调用推理引擎的 `sleep()`/`wake_up(tags)`，共置模式下训练阶段释放推理权重/KV 显存、采样阶段换回（受 `free_cache_engine` 开关控制）。
- **布局转换的同步代价**：训练侧并行布局（FSDP/Megatron 各自的参数分布）与 rollout 引擎的 TP/副本布局不同，发布路径包含权重组装/重映射；FSDP 与 Megatron 的转换实现不是同一条代码路径，共置/分离与全量/增量的选择都要把这部分耗时计入同步成本。
- **恢复对齐**：V0 训练循环从 checkpoint 恢复后先执行一次权重同步再开始采样（fit() 启动序列），保证推理引擎不带着旧策略采样。

### 同步、一步异步与完全异步（V0 recipe）

| 模式 | 机制 | 陈旧样本 | 边界与代价 |
|---|---|---|---|
| 同步（默认） | 每轮用最新权重采样，训练等待最长输出完成 | 无 | 算法最直接；长尾样本让生成侧资源空闲（[one_step_off.md](https://github.com/volcengine/verl/blob/v0.9.1/docs/advance/one_step_off.md)：作者观察 DAPO 32B 中 rollout 阶段约占 70% 时间） |
| 一步 off-policy | 上轮样本并行用于当前训练 | 恰好一个**采样/训练轮次**（一轮内含 `ppo_epochs`×mini-batch 的多次 optimizer 更新；"一步"的计数单位是轮次不是更新次数） | 受控折衷；资源在生成/训练间预先划分 |
| 完全异步（分离架构，legacy recipe） | Rollouter 与 Trainer 资源隔离持续并行；每轮参数同步的样本预算＝`(1 + staleness_threshold) × (trigger_parameter_sync_step × require_batches × ppo_mini_batch_size) − 上轮超额携入的旧样本`——即**每个同步周期允许超前产生的样本预算** | 按同步周期形成批次性滞后 | 需要消息队列与参数同步器（NCCL，参考 MoonshotAI checkpoint-engine）；作者报告 Qwen2.5-7B/128 GPU 2.35–2.67×（仅其环境）；streaming 模式下 `data.train_batch_size` 不生效，改由同步周期参数控制（[fully_async.md](https://github.com/volcengine/verl/blob/v0.9.1/docs/advance/fully_async.md)） |

关键澄清：`staleness_threshold` 控制的是**同步周期内的样本生产预算**（可小于 1，表示一个周期的一部分），不是逐样本的"版本滞后硬上限"过滤器。真实的版本滞后分布要**另行观测**：分别记录样本行为策略的发布轮次、训练消费时的已发布轮次与本地 optimizer 更新次数，三者是不同计数。若需要版本硬上限，属本库/应用侧的额外策略，须自行实现并声明超限样本的处理方式，不能声称该参数已提供该保证。`train_batch_size` 增大在同步模式下减少 rollout 次数但增加 off-policy 漂移（[best_practices.rst](https://github.com/volcengine/verl/blob/v0.9.1/docs/perf/best_practices.rst)）——该权衡表述属同步样板。

### 资源形态：共置与分离

**共置**（colocate/hybrid engine）：同一组加速器交替承担训练与采样，靠 sleep/resume 腾挪显存；权重路径短（本地 IPC 可用），代价是每轮引擎切换开销与显存切分约束。**分离**：训练组与推理组各自独立，跨组传输走网络（delta 引擎亦支持分离形态，见上节两跳结构）；资源配比可独立调整（缓解长尾空闲），代价是跨组同步带宽与部署复杂度，且分离后各阶段可能更慢、收益来自重叠（作者表述）。verl 昇腾特性文档给出参数映射（`tp_size = rollout.tensor_model_parallel_size × data_parallel_size`、`gpu_memory_utilization`、`enforce_eager`、`free_cache_engine` 等，[ascend_backend_features.md](https://github.com/volcengine/verl/blob/v0.9.1/docs/ascend_tutorial/zh/feature_support/ascend_backend_features.md)）：**rollout 引擎与训练引擎的并行度是两组独立配置**，同一循环里必须分别固定并记录。

### 失败、重放与重复计算的一致性规则

RL 循环把"消息队列＋两套引擎"引入训练，失败后的重放语义必须显式规定（以下为本库一致性规则；上游 runtime 不自动提供 exactly-once 保证，且 checkpoint 保存受 `save_freq` 等条件限制——**更新成功后可能尚无可恢复的 checkpoint**）：

| 失败位置 | 一致性风险 | 规则 |
|---|---|---|
| 采样中（部分请求完成） | 半批样本 | 丢弃未完成样本或整批重采；按 attempt 记录，不把半批计入有效样本 |
| reward 失败 | 有响应无分数 | 该样本不得进入优势计算；规则 verifier 失败先核对其代码/配置版本；reward 重试只更新该样本分数，**不重复计入计数** |
| 更新前失败 | 样本被重复消费 | 恢复后按 sample_id 去重账本跳过已消费样本，或从 checkpoint 后整批重放（二选一，预注册）；**账本必须与所恢复的 checkpoint 一致**——恢复旧 checkpoint 时消费记录一并回滚到该点，否则会跳过实际已被回滚的更新（反向：更新已持久化而账本回退会导致重复更新） |
| 更新已执行、**结果未知或未持久化** | 无可恢复 checkpoint / 提交状态不明 | 先冻结：停止新采样、新更新与新发布，隔离队列与 in-flight 请求；若能确认更新已持久（checkpoint/账本双确认）则只重发发布；不能确认则回到最后一个完整边界（checkpoint＋账本一致点）并重放该点之后的输入 |
| 更新后、发布前失败 | 权重不一致窗口 | 从已完成更新后的 checkpoint 恢复并重新发布（恢复对齐语义），未发布的更新不重复执行 |
| **增量（delta）发布中途失败** | **部分权重已写入** | 固定实现的约束：上次 delta 更新未完成时**重启整个作业并重新接收 dense（全量）seed**，仅重启 vLLM worker 不安全——这不是普通重试可覆盖的失败 |
| 重启后队列残留 | 旧版本样本回流 | 按 run/恢复代次与行为策略权重身份过滤或重放校验，禁止跨代次混入同一批 |

**重放的复用范围**要预先声明：重放一批时复用哪些已生成的 tokens（还是重新采样）、采样策略身份、reward/verifier 身份；GRPO 的组归属（uid 分组）在重放中保持不变。**去重键**贯穿 sample_id（样本）与 update 提交键（消费记录），见数据契约表。

重复计数的两条合法形态要区分：`ppo_epochs`/mini-batch 对同一批样本的**声明内重用**是算法的一部分；故障恢复导致的**计划外重复消费**是错误，用账本区分。计数口径分别记录：生成样本数、进入更新的样本数、optimizer 更新次数、发布轮次——四者不等价。

## 观察口径

| 观察对象 | 口径 | 用途与边界 |
|---|---|---|
| 生成吞吐 | 单位时间 rollout 产出 token 数（按引擎侧统计） | 与训练吞吐分开计量；重试/截断样本单列 |
| 训练吞吐 | 单位时间完成更新的 token 数（沿 06.6 有效 token 口径） | 与生成吞吐不可互相替代；共置时按阶段分别计 |
| 版本滞后 | 样本行为策略发布轮次 vs 消费时最新轮次（分布） | 同步模式应为恒定（见"版本锚点"节，不用步号直减）；异步模式按分布观测，对照样本预算的预期 |
| 权重同步耗时 | update_weights 计时（verl 记录 time cost 日志），含布局转换 | 共置/分离、全量/增量的直接代价 |
| 采样失败/队列 | 失败响应数、队列深度、超时率 | 区分引擎故障与负载压力 |
| 有效样本率 | 进入更新的样本 ÷ 生成样本 | 剔除截断/过滤/格式错误/失败重放后才是训练输入 |
| 质量口径 | reward 均值/分布、验证集通过率 | 训练是否有效最终看质量，不只看吞吐 |

## 异常区分检查与验证

常见异常的分界：

- **训练 loss 正常但质量下降**：优先查版本一致性（rollout logprob 是否真来自采样策略、所处 bypass/decoupled 路径）、reward 函数与 `data_source` 匹配、reference 模型身份、verifier 版本。
- **吞吐远低于预期**：区分 rollout 长尾（同步模式固有等待）、权重同步耗时（含布局转换）、共置切换开销（sleep/resume 计时）三者；分别对应异步化/换传输路径/改部署形态。
- **采样输出与训练侧 logprob 对不上**：查 tokenizer 版本一致性、采样参数记录、KV cache 是否在权重更新后清空。
- **异步训练后质量劣化**：查实际版本滞后分布（不是预算参数值）、样本版本标注完整性；异步引入的是分布偏移，不是单纯工程问题。

**验证方法（先固定、再单变量，工作量对齐）**：异步/部署形态改变会同时改变 batch 单位与资源分配，必须先固定可比工作量再比较：

1. **一致性基线**：固定权重与输入（同 checkpoint、同 prompt 集、同采样参数），比较两次 rollout 输出与 logprob，确认可复现边界（引擎非确定性范围）。
2. **同步模式基线**：固定**总资源、prompt/组数、有效训练 token 数、每样本更新次数、采样与校正方式、质量评估预算**，跑固定窗口，记录吞吐、质量、版本滞后（应为恒定）。
3. **单变量异步度**：仅改异步度（一步 off-policy → 分离异步的样本预算），其余工作量项不变；streaming 模式下 `train_batch_size` 不生效，须改用同步周期参数对齐等效 batch；同时观测吞吐**与**质量，不允许只报吞吐；阶段吞吐与端到端吞吐分别计时。
4. **单变量资源形态**：仅改共置/分离（或 `free_cache_engine`、桶大小），观测同步耗时与总吞吐；注意分离可能让单阶段变慢而端到端变快，按端到端判。
5. 每次改变前后保存 checkpoint 与样本记录（含版本标注与 attempt 账本），保证可按上节规则回放。

作者报告的收益数字（2.35–2.67× 等）只说明该形态**可能**带来收益的可能量级与前提（其模型/规模/基线），不是任何环境的预期值。

## 平台实践与边界

三组独立证据线，**版本配套分立、不互推**：

- **verl × NVIDIA/CUDA**：主安装文档声明的最低要求为 Python>=3.10、CUDA>=12.8；训练后端 FSDP/FSDP2（原型推荐）与 Megatron-LM，推理后端 vLLM 0.18.0 及以后（更早不可用）、SGLang、TGI（调试）（[install.rst](https://github.com/volcengine/verl/blob/v0.9.1/docs/start/install.rst)）。该页内部并存多条版本线（页首声明 Megatron core_v0.13.1，uv 路径另列 core_v0.18.0＋megatron-bridge 0.5.2、限 Linux/Python 3.12/x86_64+aarch64、cu130/torch 2.11 轮子线）；docker README 注明 GB200/aarch64 当时无预构建镜像，`Dockerfile.stable.vllm` 自带 `VERL_VERSION=v0.7.1`＋CUDA 13.0.2/Torch 2.11.0——**最低要求与任一锁定环境是两回事，具体安装路径须另选并核对**。本页机制证据取自 verl v0.9.1 文档/源码（不等于任一具体安装组合已验证）；本库 07 章的 vLLM v0.14.0 背景来源是另一版本线，与 verl 要求的 vLLM>=0.18.0 不组成同一环境。
- **verl × Ascend**：官方昇腾教程声明 vllm/sglang 两种推理后端均可在 NPU 运行，vLLM 经 vllm-ascend 插件（[ascend_backend_features.md](https://github.com/volcengine/verl/blob/v0.9.1/docs/ascend_tutorial/zh/feature_support/ascend_backend_features.md)）。安装指南内部存在**未消解的版本差异**：2026-08-03 更新条目写 torch_npu 2.10.0.post2，同文件组件表写 2.10.0.post4（HDK 26.0.rc1、CANN 9.1.0）——两处位置如实分列，实际应选 post 版本在未进一步核对安装脚本/镜像前保持 unknown；该配套线与本库 02/07 章登记的 vllm-ascend v0.14.0rc1、TorchNPU 7.2.0 也是不同版本线，行为差异未核对，不能互推。参数映射表存在不等于任一具体模型×CANN×机型组合已验证。
- **MindSpeed-LLM × Ascend（另一条独立实现线）**：v2.2.0 内置基于 Megatron 训练循环的 TRL PPO 训练器（TrlPPOTrainer 复用 Megatron 的 training_log/timers；TrlPPOEngine 管理 rollout_batch 的 actor/ref logprobs、values、scores 字段与优势计算），其采样引擎实现细节未逐文件核对（unknown）。它与 verl 是两套独立 RL 实现，机制对照只到本页的通用契约层。
- **verl × AMD/ROCm**：quick start 声明软硬件范围——运行模式 Fully Async 与 Colocate、推理引擎 vLLM 与 SGLang、训练后端 FSDP/FSDP2/Megatron、GPU 目标 MI300X/MI325X（gfx942）与 MI350X/MI355X（gfx950）；软件基线预置镜像 `amdagi/verl-dev:rocm7.14_torch2.12_release_0724`，宿主需 ROCm 7.14 驱动栈与 `/dev/kfd`、`/dev/dri` 访问（[amd_quick_start.rst](https://github.com/volcengine/verl/blob/v0.9.1/docs/amd_tutorial/amd_quick_start.rst)）。自建路径（docker/rocm/Dockerfile.rocm）的默认 `VERL_TAG=7b19203c…` **不是本页固定的 v0.9.1 commit**、vLLM 亦另设 ref——自建镜像内实际代码版本须独立核对。以上为上游文档声明；任一具体组合×模型×版本的可用性未验证（unknown），且不能从"vLLM 能在 ROCm 启动"推导"verl RL 在 ROCm 可用"。

## 常见误解

- **"rollout 就是推理服务"**：rollout 复用推理引擎执行机制（07 章），但生命周期由训练循环控制——权重每轮变更、KV cache 每轮作废、请求批量由循环参数决定。
- **"异步一定更快更好"**：异步改变的是资源利用形态与样本-策略版本对应关系；质量下降不会出现在吞吐指标里。
- **"staleness_threshold 是版本安全上限"**：它是同步周期内的样本生产预算；版本硬上限（若需要）是额外策略。
- **"权重同步只是拷贝文件"**：传输两跳、布局转换/重映射、增量限制、失败后的整作业重启边界、恢复后的对齐同步，每一项都影响一致性。
- **"GRPO 实现等于 GRPO 论文"**：聚合口径等实现细节可能与论文不同（verl 默认 token-mean 的实例）；以实现文档为准。
- **"DPO 是没有 reward 模型的 PPO"**：DPO 改写的是目标函数本身；Online DPO 是把 DPO 损失放进采样循环的另一种组合。

## 适用边界与来源

本页机制证据固定于 verl v0.9.1 的 legacy（V0）文档＋源码（含审阅轮补开的 delta 传输、V1 配置、安装页）与四篇论文摘要；V1 控制流、`core_algos.py` 实现、sglang rollout 源码、昇腾 post2/post4 消解、AMD 具体组合、MindSpeed-LLM 采样引擎细节均未核对（unknown）。性能数字（2.35–2.67×、rollout 占 70% 时间）均为来源作者报告，本库未复现。全部内容未经真实环境验证，正文不构成执行处方。

主要来源：verl v0.9.1 的 [PPO](https://github.com/volcengine/verl/blob/v0.9.1/docs/algo/ppo.md)、[GRPO](https://github.com/volcengine/verl/blob/v0.9.1/docs/algo/grpo.md)、[HybridFlow 编程指南](https://github.com/volcengine/verl/blob/v0.9.1/docs/hybrid_flow.rst)、[完全异步](https://github.com/volcengine/verl/blob/v0.9.1/docs/advance/fully_async.md)、[一步异步](https://github.com/volcengine/verl/blob/v0.9.1/docs/advance/one_step_off.md)、[DPO 扩展](https://github.com/volcengine/verl/blob/v0.9.1/docs/advance/dpo_extension.rst)、[vLLM rollout 源码](https://github.com/volcengine/verl/blob/v0.9.1/verl/workers/rollout/vllm_rollout/vllm_rollout.py)、[delta 传输源码组](https://github.com/volcengine/verl/blob/v0.9.1/verl/workers/rollout/vllm_rollout/delta_weight_transfer.py)、[rollout_correction 配置](https://github.com/volcengine/verl/blob/v0.9.1/verl/trainer/config/algorithm/rollout_correction.yaml)、[训练循环源码](https://github.com/volcengine/verl/blob/v0.9.1/verl/trainer/ppo/ray_trainer.py)、[主安装文档](https://github.com/volcengine/verl/blob/v0.9.1/docs/start/install.rst)、[昇腾安装指南](https://github.com/volcengine/verl/blob/v0.9.1/docs/ascend_tutorial/zh/get_start/install_guidance.rst)、[昇腾后端特性](https://github.com/volcengine/verl/blob/v0.9.1/docs/ascend_tutorial/zh/feature_support/ascend_backend_features.md)、[AMD quick start](https://github.com/volcengine/verl/blob/v0.9.1/docs/amd_tutorial/amd_quick_start.rst)、[最佳实践](https://github.com/volcengine/verl/blob/v0.9.1/docs/perf/best_practices.rst)；论文 [PPO](https://arxiv.org/abs/1707.06347)、[DeepSeekMath/GRPO](https://arxiv.org/abs/2402.03300)、[DPO](https://arxiv.org/abs/2305.18290)、[HybridFlow](https://arxiv.org/abs/2409.19256)；MindSpeed-LLM v2.2.0 [TrlPPO 训练器](https://github.com/Ascend/MindSpeed-LLM/blob/v2.2.0/mindspeed_llm/tasks/posttrain/trl_ppo/TrlPPOTrainer.py)。取证记录、审阅发现与 SHA-256 见[来源记录](../../docs/research/batch-25-t06-04-sources.md)与[初审报告](../../docs/research/batch-25-t06-04-codex-review.md)。
