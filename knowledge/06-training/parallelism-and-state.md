---
id: training.parallelism-and-state
title: 并行策略与训练状态
type: concept
domain: training
status: draft
platforms: [generic]
source_refs:
  - src.pytorch.parallel-training-state-2.6
  - src.pytorch.dcp-2.6
  - src.pytorch.device-mesh-source-v2.6.0
  - src.pytorch.cp-experimental-source-v2.6.0
  - src.pytorch.distributed-backend-2.6
  - src.ascend.mindspeed-llm-ha-v2.2.0
  - src.ascend.mindspeed-llm-checkpoint-v2.2.0
  - src.ascend.mindspeed-llm-parallel-features-v2.2.0
  - src.ascend.mindspeed-llm-training-interface-v2.2.0
  - src.nvidia.megatron-lm-core-v0.19.2
  - src.nvidia.megatron-training-loop-core-v0.19.2
updated_at: "2026-10-19"
summary: 说明数据、状态分片、张量、流水线、专家与序列并行如何改变训练状态的所有者、布局、通信与恢复责任，并给出组合映射、冲突检查与固定假设下的选型比较。
related_ids:
  - communication.collectives-and-rank-progress
  - data-storage.checkpoint-durability
  - training.checkpoint-state-consistency
verification:
  status: source_checked
  evidence_refs:
    - src.pytorch.parallel-training-state-2.6
    - src.pytorch.dcp-2.6
    - src.pytorch.device-mesh-source-v2.6.0
    - src.pytorch.cp-experimental-source-v2.6.0
    - src.nvidia.megatron-lm-core-v0.19.2
    - src.ascend.mindspeed-llm-parallel-features-v2.2.0
  notes: 核对 PyTorch 2.6 版本化文档与 v2.6.0 源码、Megatron-LM core_v0.19.2 冻结源码、MindSpeed-LLM v2.2.0 固定文档；未运行训练、保存、加载或 GPU/NPU 实验。EP dispatch/combine 行状锚点沿用 Batch 18 轮的 SHA-256 冻结核对记录。2026-10-19 交付后复查补核 Megatron 稠密/专家 grid 默认轴序、本地专家编号、fp16 grad scaler 与 linear_qkv 切分（以 RankGenerator 对合成样例做纯算术复算，未初始化进程组）。
---

# 并行策略与训练状态

训练状态不只是模型权重。一个可解释的训练恢复点还可能包含 optimizer、scheduler、loss scaler、随机数生成器、数据进度、逻辑步和并行映射。并行策略会改变这些状态是复制、分片、按 stage 所有，还是只在一个计算窗口内短暂存在；因此 `world_size` 和一组 tensor 字节不足以描述训练状态。

本页讨论状态的所有者、布局和 checkpoint 表示。collective 匹配与 rank 进展见[集合通信语义、rank 进展与超时](../03-communication/collectives-and-rank-progress.md)，文件写入、提交和持久化见 [Checkpoint 写入与持久化边界](../04-data-storage/checkpoint-durability.md)，装载后是否能正确继续训练见 [Checkpoint 恢复一致性](checkpoint-state-consistency.md)。

## 并行改变了什么

下表以 PyTorch 2.6 的 DDP、FSDP、Tensor Parallel 和 Pipeline Parallel 为版本化样板。它用于解释关系，不表示其他框架采用相同格式或提供相同恢复能力。

| 策略 | 状态布局与所有者 | 主要通信或执行关系 | 对 checkpoint 的影响 |
|---|---|---|---|
| DDP 式数据并行 | 每个 rank 有完整模型副本；普通 optimizer state 通常也随副本本地持有；每个 rank 消费不同数据子集 | backward 同步梯度；参数由各进程的 optimizer 以相同方式更新；buffer 可按配置广播 | 权重和 optimizer 可能可去重，数据进度与 RNG 却可能是 rank-local；不能因模型有副本就只保留一个 rank 的全部应用状态 |
| FSDP/ZeRO 式状态分片 | 以 FSDP `FULL_SHARD` 为例，参数、梯度和 optimizer state 均被分片；完整参数只在计算窗口内聚合 | forward/backward 前 all-gather 参数，backward 后 reduce-scatter 梯度 | 单个 local shard 不是完整模型；需要声明 full、sharded 或 local 表示，以及目标布局如何重建 |
| Tensor Parallel | 单层参数和中间 tensor 按 row、column、sequence 等规则分片；布局依赖 module FQN、mesh 和 plan | 层内 collective 或 layout redistribution 连接各分片计算 | 参数身份必须与 mesh、placement 和 parallel plan 关联；只记录 global rank 不能解释 shard |
| Pipeline Parallel | 各 stage 拥有不同模块，micro-batch 由 schedule 在 stage 间推进 | stage 间传输 activation 和 gradient；schedule 决定飞行中的 micro-batch | 普通 step 边界可避免保存飞行状态；若要 mid-step 恢复，还要覆盖梯度累积、schedule 与在途状态 |
| 组合并行 | 同一进程可同时属于 DP、TP、PP、expert/context 等多个通信域 | 多个 group 的 collective 与点对点操作按各自次序叠加 | 需要记录每个并行维度、成员顺序、stage/shard 分配和状态格式；单一 `world_size` 不能描述布局 |

PyTorch 2.6 的 DDP 文档明确把输入切分留给应用，并说明参数不会在每次迭代中广播；DDP 依靠梯度同步后各 optimizer 以相同方式更新副本（[DistributedDataParallel](https://docs.pytorch.org/docs/2.6/generated/torch.nn.parallel.DistributedDataParallel.html)）。因此“权重副本相同”不能推出 sampler 位置、RNG 或任意应用计数也相同。

FSDP `FULL_SHARD` 的参数、梯度和 optimizer state 分片及其 all-gather/reduce-scatter 关系由 [PyTorch 2.6 FSDP 文档](https://docs.pytorch.org/docs/2.6/fsdp.html)定义。Tensor Parallel 则用 DTensor 和 1-D `DeviceMesh` 表达 row/column/sequence 等布局，并按 module FQN 应用 plan（[Tensor Parallelism](https://docs.pytorch.org/docs/2.6/distributed.tensor.parallel.html)）。Pipeline Parallel 同时切分权重和执行，以 micro-batch、stage 通信和 schedule 组织计算；PyTorch 2.6 将该包标为 alpha（[Pipeline Parallelism](https://docs.pytorch.org/docs/2.6/distributed.pipelining.html)）。这些资料没有提供跨框架通用的 shard 或 stage checkpoint 格式。

## 专家并行：token dispatch/combine 与专家负载

专家并行（EP）把 MoE 层的不同专家分布到一组 rank 上；它改变的不是权重切分维，而是**token 的路由归属**。以冻结的 NVIDIA Megatron-LM tag `core_v0.19.2` 实现为样板：

- **dispatch**：router 先产生 per-token 的路由映射与概率（`routing_map`/`probs`；具体路由算法与均衡策略由上层决定），`MoEAlltoAllTokenDispatcher` 消费该映射，把 token 按 expert 归属重排后经 all-to-all 发往持有该专家的 rank（[token_dispatcher.py](https://github.com/NVIDIA/Megatron-LM/blob/core_v0.19.2/megatron/core/transformer/moe/token_dispatcher.py) L372–383、L618–640、L698–716；Batch 18 轮 SHA-256 冻结核对）。非 fused 分支中 tokens 为 `m×hidden` 的行选、probs 为一维 `[m]`（[moe_utils.py](https://github.com/NVIDIA/Megatron-LM/blob/core_v0.19.2/megatron/core/transformer/moe/moe_utils.py) L423–467）。
- **combine**：各专家输出按原 token 顺序聚合；`tp_size>1` 时 combine 前先做 reduce-scatter，再经 all-to-all 交换 input/output splits（token_dispatcher.py L817–826、L857–862）。
- **专家负载**：均衡由 router 策略承担——`--moe-router-load-balancing-type` 与 `--moe-aux-loss-coeff` 是入口（[arguments.py](https://github.com/NVIDIA/Megatron-LM/blob/core_v0.19.2/megatron/training/arguments.py) L3365、L3369）。路由偏斜在机制上直接改变 dispatch 后各 rank 的计算量与 A2A 消息分布，是 EP 吞吐长尾的重要候选原因；是否成为主因取决于负载与路由策略，本库无测量不作断言。

组合约束（同一冻结 tag 的启动校验）：`num_experts` 必须能被 EP size 整除，且 EP>1 必须显式设置专家数（arguments.py L1600–1603）；`overlap_moe_expert_parallel_comm` 在 Hopper 及更早硬件上不建议与 TP/CP 同用，且要求更大的 `CUDA_DEVICE_MAX_CONNECTIONS`（L1426–1431）。Ascend 侧的官方组合实例见 MindSpeed-LLM v2.2.0 的 GLM4.5-MoE 106B A3 预训练脚本：TP=1、PP=4、EP=16，配 `--num-experts 128 --moe-router-topk 8 --moe-token-dispatcher-type alltoall_seq --moe-grouped-gemm` 等（[脚本](https://github.com/Ascend/MindSpeed-LLM/blob/v2.2.0/examples/mcore/glm45-moe/pretrain_glm45_moe_106b_4k_A3_ptd.sh)）。

## 序列维并行：SP 与 CP 和 TP 的区别

三者名字都带"并行"，切分对象不同：

| 维度 | 切分对象 | 通信关系 | 精确来源 |
|---|---|---|---|
| TP | **权重矩阵与中间激活**按 row/column 规则切分；每个 micro-batch 在 TP 组内经 collective 连接 | TP 组内 all-reduce（或配 SP 时 all-gather/reduce-scatter） | PyTorch 2.6 `ColwiseParallel/RowwiseParallel`（[tensor.parallel](https://docs.pytorch.org/docs/2.6/distributed.tensor.parallel.html)；v2.6.0 源码 `__all__` 见 [parallel/__init__.py](https://github.com/pytorch/pytorch/blob/v2.6.0/torch/distributed/tensor/parallel/__init__.py) L14–23） |
| SP | **激活与部分 buffer 沿序列维**在 TP 组内分布，消除 TP 引入的激活重复 | 与 TP 同组配合：进 TP 块前 gather、出块后 scatter | `SequenceParallel` 是与 Colwise/Rowwise 并列的 ParallelStyle（同上 `__all__`）；MindSpeed-LLM 明确 2D TP 特性**不与** `--sequence-parallel` 兼容（[tensor_parallel_2d](https://github.com/Ascend/MindSpeed-LLM/blob/v2.2.0/docs/pytorch/features/tensor_parallel_2d.md)） |
| CP | **输入序列本身**按块分布到 CP 组；注意力所需的 KV 块在 CP 组内环形/全对全交换 | CP 组内 KV/dKV 点对点或 A2A；与 DP 组可组合（"含 CP 的 DP 组"） | PyTorch 2.6 experimental `context_parallel`：patch SDPA＋把 buffers 沿序列维 in-place 切分（[_attention.py](https://github.com/pytorch/pytorch/blob/v2.6.0/torch/distributed/tensor/experimental/_attention.py) L1211–1246）；Megatron `parallel_state` 为 KV/dKV 交换维护 CP 组与分层 CP 组（[parallel_state.py](https://github.com/NVIDIA/Megatron-LM/blob/core_v0.19.2/megatron/core/parallel_state.py) L123–131），并提供 `get_tensor_and_context_parallel_group`（L1923–1928） |

Ascend 侧 CP 算法选择（MindSpeed-LLM v2.2.0）：`--context-parallel-algo` 三选——`megatron_cp_algo`（Ring Attention：KV 块环形传递、计算通信重叠）、`ulysses_cp_algo`、`hybrid_cp_algo`；ulysses 要求 attention heads 能被 ulysses×TP 整除（[arguments 校验](https://github.com/Ascend/MindSpeed-LLM/blob/v2.2.0/mindspeed_llm/training/arguments.py) L242 起），Ring Attention 无此整除要求但必须开 FlashAttention，且短序列（seq/cp 小）可能出现负优化（[ring-attention 文档](https://github.com/Ascend/MindSpeed-LLM/blob/v2.2.0/docs/pytorch/features/ring-attention-context-parallel.md)）。

## 组合并行：身份样例与冲突检查

PyTorch 的 `DeviceMesh` 把多维布局命名为如 `("dp","cp","tp")` 的 n-d 数组，每个格子是对应进程组的 global rank，并遵循 SPMD 编程模型（[device_mesh.py](https://github.com/pytorch/pytorch/blob/v2.6.0/torch/distributed/device_mesh.py) L379–390、L87–110）。Megatron 侧同一 rank 同时属于多个进程组：TP 组、PP 组、CP 组（含分层 CP）、可选含/不含 CP 的 DP 组、EP 组与"TP+CP"组（parallel_state.py L601 起、L133–135、L1758–1807）。

一个**完整合成身份样例**（本库构造的配置，按已核对的源码规则做纯映射推导，**不是**任何启动验证）。合成假设：64 个 rank（8 节点×8 卡）、32 层 Transformer、num_experts=128，取 `pp=2, cp=2, tp=2`，dense 数据并行 `dp = 64/(2×2×2) = 8`。mesh 维度顺序与步长（stride）为 `[pp=32, dp=4, cp=2, tp=1]`，即 `global_rank = 32×pp_idx + 4×dp_idx + 2×cp_idx + 1×tp_idx`。这与 Megatron core_v0.19.2 的默认轴序一致：`initialize_model_parallel` 默认 `order="tp-cp-ep-dp-pp"`（[parallel_state.py](https://github.com/NVIDIA/Megatron-LM/blob/core_v0.19.2/megatron/core/parallel_state.py) L617），排在前面的维度变化最快（`generate_masked_orthogonal_rank_groups` 文档式 L292：`global_rank = tp_rank + dp_rank × tp_size + …`），稠密 generator 的 EP=1。传入非默认 `order` 时组成员随之改变。

取 **global rank 37**：37 = 1×32 + 1×4 + 0×2 + 1 → 坐标 `pp=1, dp=1, cp=0, tp=1`。由步长可直接推出各维组成员（固定其余坐标、扫描本维）：

| 身份项 | rank 37 的取值（合成推导） |
|---|---|
| mesh 坐标 | (pp=1, dp=1, cp=0, tp=1)，dim 名可用 `mesh_dim_names` 命名（device_mesh.py 的 ("dp","cp","tp") 示例推广） |
| TP 组成员（同 pp,dp,cp） | {36, 37}，组内 rank 37 为第 1 号（0 起） |
| CP 组成员（同 pp,dp,tp） | {37, 39}，组内第 0 号 |
| TP+CP 组成员（同 pp,dp） | {36, 37, 38, 39} |
| PP 组成员（同 dp,cp,tp） | {5, 37}，组内第 1 号 |
| dense DP 组成员（同 pp,cp,tp） | 扫描 dp=0..7：{33, 37, 41, 45, 49, 53, 57, 61}，组内 rank 37 为第 1 号（0 起） |
| stage/layer 区间 | pp=1 → 第 16–31 层（合成约定 32 层对半） |
| expert 集合 | EP=4 时每 rank 持 32 个本地专家；rank 37 是其 EP 组的第 2 号 → expert 64–95（推导见下文 expert grid 身份） |
| 参数身份示例 | 第 20 层（属本 rank 的 stage）的融合 QKV 权重 `linear_qkv.weight`。合成 MHA，全局 shape `[3×hidden, hidden]`。Megatron 用 column-parallel 线性层实现 `linear_qkv`（[gpt_layer_specs.py](https://github.com/NVIDIA/Megatron-LM/blob/core_v0.19.2/megatron/core/models/gpt/gpt_layer_specs.py) L324 的 Transformer Engine spec、L444 的 local spec），即沿 dim 0（输出维）切分，对应 PyTorch 术语 ColwiseParallel：TP 组内第 1 片，本地 `[3×hidden/2, hidden]`，dim-0 offset = 1×(3×hidden/2)。该权重按 query group 交错存放 q/k/v（[attention.py](https://github.com/NVIDIA/Megatron-LM/blob/core_v0.19.2/megatron/core/transformer/attention.py) L1840–1841 的交错注释；L1861–1867 按 query group 重排、L1887–1903 在组内拆分 Q/K/V），因此 offset 是 Megatron 存储布局中的行号，不能换算成"q/k/v 依次拼接"布局的位置 |

覆盖/唯一性检查（样例自洽性）：dense 各维大小乘积 2×8×2×2 = 64 = world size；每维成员表按步长互斥且覆盖全部 rank；`world_size % (TP×PP×CP) = 64 % 8 = 0` ✓、`num_experts % EP = 128 % 4 = 0` ✓、`seq(32k) % (2×CP=4) = 0` ✓——即该合成配置通过上文全部硬断言。

**expert grid 身份（按 core_v0.19.2 源码规则推导，非启动验证）**：core_v0.19.2 的 `parallel_state` 用**两套 RankGenerator** 分别生成稠密层与专家层的 rank 布局——稠密 generator 含 CP、不含 EP；专家 generator 含 EP、不含 CP（两者不能同时出现在一个 generator，[parallel_state.py](https://github.com/NVIDIA/Megatron-LM/blob/core_v0.19.2/megatron/core/parallel_state.py) L479–491），且两个 grid 的 **PP 组必须一致**（L898–907）。专家 grid 的维度公式：`ETP`（expert tensor parallel）默认等于 TP；`expert_dp = world_size // (ETP × EP × PP × EGTP)`，不整除即 RuntimeError（L871–884）。本样例：ETP=2、EP=4、PP=2 → expert_dp = 64/(2×4×2) = **4**（注意 expert_dp=4 ≠ dense dp=8：MoE 层与稠密层的数据并行度不同，这是 EP 的直接后果）。

专家 generator 的轴序取 `expert_order = _inject_gtp_remat_axis(order, after="ep")`（L886–893），默认即 `tp-cp-ep-dp-pp` 去掉 cp（专家 generator 的 cp=1），也就是 `tp-ep-dp-pp`：**EP 紧接在 ETP 之后变化，expert DP 在 EP 之外**。本样例的专家步长因此是 `[pp=32, edp=8, ep=2, etp=1]`（慢→快），`global_rank = 32×pp + 8×edp + 2×ep + etp`；rank 37 = 32 + 0×8 + 2×2 + 1 → (pp=1, edp=0, ep=2, etp=1)。下表组员已用该文件的 `RankGenerator` 对本样例做纯算术复算（未初始化进程组），结果一致：

| 专家侧身份项 | rank 37 的取值（源码规则推导） |
|---|---|
| expert TP 组（同 pp、edp、ep） | {36, 37}，组内第 1 号 |
| EP 组（同 pp、edp、etp） | {33, 35, 37, 39}，组内第 2 号；按"连续 8 个 rank 为一节点"的合成放置，4 个成员都在节点 4，dispatch/combine 的 all-to-all 在节点内完成 |
| expert DP 组（同 pp、ep、etp） | {37, 45, 53, 61}，组内第 0 号；跨节点 4–7（stride 8） |
| 持有专家 | num_experts=128、EP=4 → 每 rank 32 个本地专家；Megatron 按 `local_expert_indices_offset = ep_rank × num_local_experts` 分配连续编号（[moe_layer.py](https://github.com/NVIDIA/Megatron-LM/blob/core_v0.19.2/megatron/core/transformer/moe/moe_layer.py) L181–194，`ep_rank` 为 EP 组内序号）→ rank 37 持有 **expert 64–95**；同 EP 组的 4 个 rank 依次持 0–31/32–63/64–95/96–127，无重无漏 |
| 参数 shard 示例（合成张量） | `layers.20.mlp.experts.expert_64.gate_proj`（合成命名），全局 shape `[11008, 4096]`（ffn×hidden，合成值）、bf16；ETP=2 沿 dim 0（输出维）切分，即 column-parallel / PyTorch ColwiseParallel；本地 `[5504, 4096]`；rank 37 是 expert-TP 组 {36, 37} 的第 1 号 → dim-0 offset = 1×5504 = 5504（行 5504–11007） |
| 数据并行副本 | expert DP 组 {37, 45, 53, 61} 的四个 rank 的 ep/etp 坐标相同，持有同一批专家（64–95）同一 shard 的副本，不是不同 shard |

覆盖检查：每个专家的 gate_proj 恰由其 EP rank 的 2 个 ETP shard 覆盖 [0, 11008) 全部行，无重无漏。层编号按全局序解释并与所属 stage 对应。与稠密 grid 对照：同一个 rank 37 的稠密 DP 组 {33, 37, …, 61} 跨 4 个节点，而专家侧的 EP 组留在节点内、expert DP 组跨节点——两套 generator 产生不同的组放置。

组合约束（同一冻结 tag 的启动校验；不通过即拒绝启动，这是组合合法性的第一道验证）。注意区分三类：**硬断言**（启动期 assert/raise，拒绝启动）、**功能不支持**（特定组合被 assert 明确排除）、**性能提醒**（`warn_rank_0` 提示，不拒绝启动）。下表按类分列：

**硬断言（拒绝启动）**

| 检查 | 约束（统一用取模等式表述） | 来源 |
|---|---|---|
| world-size 整除 | `world_size % (TP×PP×CP×gtp_remat) == 0`（gtp 未启用时为 1） | Megatron arguments.py L422–431 |
| CP×序列长 | `seq_length % (2×CP) == 0`（CP>1 时） | 同上 L1295–1298 |
| 分层 CP | hierarchical CP sizes 乘积须等于 CP；a2a+p2p CP 通信必须显式设置 | 同上 L555–567 |
| EP×专家数 | `num_experts % EP == 0`（num-experts 须能被 EP 整除）；EP>1 须设专家数 | 同上 L1600–1603 |
| ulysses CP×头数 | `num_attention_heads % (ulysses_size×TP) == 0`；GQA 时 `num_query_groups % TP == 0`，且**未启用** `--kv-head-repeat-before-uly-alltoall` 时 `num_query_groups`（TP 切分后）还须能被 ulysses_size 整除（启用该开关可绕过，代价是 ulysses alltoall 通信量与内存增加） | MindSpeed-LLM arguments.py `_validate_cp_args` L247–263 |

**功能不支持（assert 排除）**：`--use-torch-fsdp2` 不支持 PP>1、EP>1、Megatron distributed optimizer（arguments.py L998–1006）。

**性能提醒（warn_rank_0，不拒绝启动）**：Hopper 及更早硬件上 TP/CP 与 `overlap_moe_expert_parallel_comm` 同用时提示两者偏好不同的 `CUDA_DEVICE_MAX_CONNECTIONS`（设 1 或 32，按优先侧取舍）；TP/CP 与 Torch-FSDP2/Megatron-FSDP 同用有同类提示（arguments.py L1413–1435）。

**文档声明的兼容/前提**（MindSpeed-LLM v2.2.0 特性文档口径）：`--tp-2d` 不兼容 `--sequence-parallel`/`--use-fused-rmsnorm`、不支持 MoE；MC2 需 CANN 8.0.RC2＋HDK 24.1.RC2 及后续、MoE 模型 MLP 不使能。

静态代入核对（合成推导，非启动测试）：满足组——heads=48、TP=2、ulysses CP=4：48 % (4×2) = 0 ✓；不满足组——heads=52 同配置：52 % 8 = 4 ≠ 0，`_validate_cp_args` 将 raise ValueError。

## 固定假设下的选型比较

比较只在固定假设下有意义。**合成场景（全部为合成假设，本库无任何测量）**：32 层 Transformer、hidden 4096、序列 32768、精度 bf16、全局 batch 512、**拓扑＝8 节点×8 卡共 64 rank，节点内 8 卡高速互联、节点间互联带宽低于节点内**（合成假设，代表"节点内/间不对称"一类拓扑；真实拓扑须以实测为准）。全局 batch 的合成口径：**micro-batch 1 × 梯度累积数 × 数据并行度 = 512**（Megatron 的 `num_micro_batches = global_batch_size // (micro_batch_size × dp)` 口径，见[微批计算器](https://github.com/NVIDIA/Megatron-LM/blob/core_v0.19.2/megatron/core/num_microbatches_calculator.py) `init_num_microbatches_calculator` 起，含整除断言）。适用实现：PyTorch 2.6（DDP/FSDP `FULL_SHARD`/TP/PP alpha）与 Megatron core_v0.19.2 语义。**公共放置约定与统一轴序（合成）**：连续 8 个 global rank 构成一个节点（`node = rank // 8`，节点内 0–7 为本地设备）。各候选的组员按**统一轴序重算步长**构造（不是沿用某一固定样例的步长）：稠密轴序 `[pp, dp, cp, tp]`（慢→快），`rank = ((pp_idx×DP + dp_idx)×CP + cp_idx)×TP + tp_idx`；专家轴序 `[pp, edp, ep, etp]` 同理（按各候选的 ETP/EP/EDP 大小重算步长）。两条轴序都取 Megatron core_v0.19.2 的默认 `order`（稠密 `tp-cp-ep-dp-pp`，专家 `tp-ep-dp-pp`，见上文身份样例）。下表各行的组员放置均由该公式与本约定推出（上文身份样例 TP2/CP2/PP2/DP8 是它的一个实例，其步长不能直接搬到其他候选）。下表每行给出一组**占满全部 64 rank** 的完整维度分解、对应累积数与主要通信组的放置（合成复算：各候选的 TP×PP×CP 乘积整除 64，剩余为 dense DP；EP 行另按 expert grid 公式复算；未写的维度＝1）：

| 策略（合成候选配置，均占满 64 rank） | 状态内存（机制） | 主要通信（机制） | bubble/负载（机制） | 分析预期与边界 |
|---|---|---|---|---|
| 纯 DP（tp=pp=cp=1，dp=64；micro=1，累积 8；DP 组跨 8 节点） | 每 rank 全量权重＋优化器状态 | backward 后对全量梯度做 all-reduce；通信总量随参与 rank 数与参数量增长（时延还取决于实现分桶与拓扑） | 无流水 bubble；数据不均才偏斜 | 内存先到顶；通信量级随模型与卡数增长，具体占比无测量（unknown） |
| FSDP `FULL_SHARD`（dp=64；micro=1，累积 8；分片聚合通信跨 8 节点） | 参数/梯度/优化器**全分片**（`FULL_SHARD` 策略语义；ZeRO 各阶段是不同策略，未在本库分阶段取证） | 计算窗口前 all-gather 参数、backward 后 reduce-scatter 梯度 | 无流水 bubble；分桶影响通信与计算重叠 | 分片降低单 rank 内存；聚合通信量与参数量成正比（机制），净收益无测量 |
| TP（tp=2 配 SP，pp=cp=1，dp=32；micro=1，累积 16；`rank=2×dp+tp` → TP 组为相邻 rank 对（节点内），DP 组 stride 2 跨节点） | 单层参数/激活按 row/column/sequence 分片，激活不重复（配 SP 时） | TP 组内 all-reduce（次数与层数和实现的重叠策略相关，不给固定数） | 组内同步；组越大、每步同步次数越多 | 组宜落在低时延域（如节点内）是机制性倾向，具体上限取决于互联与模型（不给通用卡数上限） |
| PP（pp=2，tp=cp=1，dp=32；micro=1，累积 16；PP 组 [r, r+32] 跨节点） | 各 stage 只持本段权重 | stage 间 activation/梯度点对点 | bubble 比例与 stage 数、micro-batch 数相关（更深 pipeline 需更多 micro-batch 填充；本例每 step 16 个 micro-batch 在 2 stage 间填充） | 用点对点流量换单卡内存；bubble 数值无测量 |
| VPP（pp=2，vp=2，dp=32；micro=1，累积 16；点对点跨节点） | 同 PP，stage 更细 | 点对点更频繁、消息更小 | 以更多通信换更低 bubble 比例（MindSpeed VPP 16 层 TP1/PP4/VPP2 示例） | 权衡方向有来源，具体收益无测量 |
| CP（cp=2，tp=pp=1，dp=32，累积 16，`rank=2×dp+cp` → CP 组为相邻 rank 对（节点内）；或 cp=4，dp=16，累积 32，`rank=4×dp+cp` → CP 组 [4k..4k+3] 仍节点内（每节点两个组）） | KV 与激活按序列分块 | CP 组内 KV 环形（megatron_cp）或 A2A（ulysses）交换 | MindSpeed 文档口径：seq/cp 过小可能负优化、算法约束不同（见上文） | 长序列为主；算法按整除约束选择 |
| EP（tp=2，pp=cp=1，EP=4；dense dp=32，累积 16；expert 轴 `rank=8×edp+2×ep+etp`（EDP=8）→ ETP 组为相邻 rank 对（节点内）；EP 组 stride 2、4 个成员在同一节点内（组例：{0,2,4,6}），每节点容纳 2 个 EP 组；expert-DP 组 stride 8、8 个成员各在一个节点（组例：{0,8,16,…,56}，跨全部 8 节点）） | 专家权重按 EP 分布（expert grid：ETP 默认=TP=2，expert_dp = 64/(2×4×1) = 8） | token A2A dispatch/combine | 路由偏斜→rank 间 token 不均 | 需 router 负载策略配合；偏斜影响是机制性的，量级无测量 |

候选配置间要满足上文硬断言（如 `world_size % (TP×PP×CP) == 0`、`num_experts % EP == 0`、expert grid 的 `world % (ETP×EP×PP) == 0`）；micro-batch 与梯度累积的改变会同时改变全局 batch 语义与 bubble 填充，属同一决策空间。**不构成任何无条件最佳配置**；换模型、序列长、精度或真实拓扑后结论可能反转，无测量处保持分析预期或 unknown。

有来源的选择实例（各自固定在其文档环境，不可跨环境照搬）：MindSpeed-LLM 对 Llama2-7B 32k 长序列微调给出 TP2/PP1/CP4 下 megatron 与 ulysses 两种 CP 算法的吞吐对照（[CP 微调文档](https://github.com/Ascend/MindSpeed-LLM/blob/v2.2.0/docs/pytorch/features/fine-tuning-with-context-parallel.md)）；对大 TP 场景推荐 2D TP（如 TP=16 时 tp-x 8、tp-y 2，且注明小模型/小 TP 会负优化）；GLM4.5-MoE 106B 在 A3 上取 TP1/PP4/EP16。AMD/ROCm 侧的分布式支持条件以 PyTorch 官方分布式文档为准（[PyTorch 2.6 distributed](https://docs.pytorch.org/docs/2.6/distributed.html)），NCCL 结论不得平移。

## 状态责任矩阵

训练系统应为每类状态指定逻辑所有者、物理持有者、保存表示和恢复规则。“逻辑全局”不表示只有一个物理副本；“每 rank 持有”也不表示每份都能互换。

| 状态 | 并行下的典型变化 | checkpoint 责任 |
|---|---|---|
| 模型参数与持久 buffer | DDP 复制，FSDP/TP 分片，PP 按 stage 分配；buffer 的同步规则可不同 | 保存稳定参数身份、shape、dtype、布局和模型结构版本；用对应并行 API 生成可加载表示 |
| 梯度与累积槽 | 可能经 all-reduce/reduce-scatter，也可能只存在于本 rank；micro-step 内仍可能是暂态 | 在完整 optimizer step 后保存时，可把“无待提交梯度”列为前提；若支持 mid-step 恢复，需显式保存梯度、累积计数与未决更新 |
| optimizer state 与 param groups | DDP 可复制；FSDP、ZeRO 或 distributed optimizer 可分片 | 保存 state、param groups、参数身份映射和分片格式；不要把普通 parameter ID 当作跨布局稳定键 |
| scheduler | 通常是逻辑全局进度，但实例可能在各 rank 复制 | 单独保存其 `state_dict` 和装载顺序；当前 LR 或 global step 未必能重建全部内部状态 |
| GradScaler/loss scale | 副本通常需要逻辑一致，overflow 决议可能涉及归约 | 保存 scale、growth tracker 和策略字段；PyTorch 2.6 的实现建议在 `update()` 后截取状态 |
| RNG | Python、NumPy、PyTorch CPU、设备 generator、模型并行 tracker 和 worker 可能彼此独立 | 明确保存哪些 generator，并记录其与 rank、设备和并行域的映射；单一 seed 不等于同一随机序列位置 |
| 数据进度 | DP rank 数和 sampler epoch 会改变样本分区；worker 预取使“已读取”与“已训练”不同 | 记录数据修订、epoch、已提交样本/批次、sampler/loader 可恢复状态，以及允许重放或去重的规则 |
| global step、micro-step、样本/token 数 | gradient accumulation、DP size 和 batch 语义会改变这些计数的对应关系 | 分开记录 optimizer step、micro-step、samples/tokens consumed 和最近完整提交点；不能只保存一个 `step` 整数 |
| 并行映射 | 决定参数、optimizer shard、stage、RNG 和数据分区由谁持有 | 保存 TP/PP/DP/EP/CP 维度、mesh/group 成员顺序、stage/layer 分配和格式版本 |
| 模型、代码与数据身份 | 不因并行而消失，却决定序列化字段如何解释 | 记录模型结构、配置、tokenizer/数据修订和必要代码版本；同名 key 或相同步数不证明语义一致 |

PyTorch optimizer 的普通 `state_dict` 以 parameter ID 保存 state，并在 `param_groups` 中保存参数列表和超参数；加载时按列表关系匹配，没有额外的参数身份验证（[Optimizer.state_dict](https://docs.pytorch.org/docs/2.6/generated/torch.optim.Optimizer.state_dict.html)）。`LRScheduler` 有自己的 `state_dict`（[LRScheduler](https://docs.pytorch.org/docs/2.6/generated/torch.optim.lr_scheduler.LRScheduler.html)）。固定 PyTorch v2.6.0 的 [`GradScaler.state_dict` 与 `update`](https://github.com/pytorch/pytorch/blob/1eba9b3aa3c43f86f4a2c807ac8e12c4a7767340/torch/amp/grad_scaler.py)还说明 loss scale 的当前值和 growth tracker 是独立状态。把这三类状态折叠为“optimizer 已保存”会遗漏恢复语义。

随机性也不是一个字段。PyTorch 提供 CPU 默认 generator 的取回和设置接口，而可复现性说明同时列出 Python、NumPy 和库内独立 generator 等来源（[`torch.random`](https://docs.pytorch.org/docs/2.6/random.html)、[Reproducibility](https://docs.pytorch.org/docs/2.6/notes/randomness.html)）。`DistributedSampler` 还要求每个 epoch 在创建迭代器前调用 `set_epoch()` 以改变排序（[数据加载文档](https://docs.pytorch.org/docs/2.6/data.html#torch.utils.data.distributed.DistributedSampler)）。这些资料不保证任意 DataLoader worker 预取位置可由 seed 和 epoch 精确恢复。

## 状态身份需要超过 global rank

rank 是某个通信域中的编号，不是长期稳定的状态身份。组合并行中，一个进程同时拥有 global rank、各 group 内 rank、设备映射、mesh coordinate 和 pipeline stage。重启或改变 world size 后，这些编号可能重新分配，而逻辑参数、stage 或数据分区仍需找到对应状态。

可供恢复协议使用的身份至少包括：

- canonical parameter FQN、模型结构版本和 tensor 的 shape/dtype；
- 旧、目标 DP/TP/PP/EP/CP 维度与有序 group/mesh 描述；
- shard offset/placement，或框架支持的等价布局描述；
- pipeline stage 与 layer/module 的映射；
- RNG、optimizer shard 和数据分区所绑定的逻辑域；
- checkpoint 格式、框架版本和必要转换器版本。

PyTorch 2.6 的 distributed state-dict API 用 canonical FQN 统一若干并行表示，并声明模型和 optimizer state 可面向不同 trainer 数或并行方式重分片（[DCP `get_state_dict`](https://docs.pytorch.org/docs/2.6/distributed.checkpoint.html)）。这个接口范围不能推广为任意应用状态或第三方 shard 自动可转换；目标对象初始化、支持的 tensor 类型和格式条件仍需在恢复侧满足。

## 截取边界决定暂态是否属于 checkpoint

恢复点若定义在完整 optimizer step 之后，可以把无飞行 micro-batch、无待提交梯度累积、scaler 已完成 `update()`、scheduler 和数据提交计数已推进到同一逻辑点作为截取条件。这样不必声称“所有 checkpoint 都必须保存梯度”。

若要求从 step 中间精确恢复，则需要另行覆盖梯度、micro-step、未完成的 overflow 决议、pipeline schedule、在途 activation/gradient、数据预取和异步状态更新。所选资料没有给出跨 DDP/FSDP/TP/PP 的通用 mid-step checkpoint 协议，因此这项能力应在具体实现资料和实验出现前保持 `unknown`。

### 单步内的所有权与合法跳步

把一个训练 step 拆开看，各阶段的暂态有明确所有者，由此决定"哪些状态在 step 边界保存时可以合法跳过"：

| 阶段 | 状态所有者 | step 边界保存时可跳过 | 依据 |
|---|---|---|---|
| forward | 各并行域内计算（TP 组内 collective、PP stage 间 activation、CP 的 KV 交换、EP 的 dispatch） | 在途 activation/中间 tensor——仅在"无飞行 micro-batch"前提下合法 | Megatron 把 forward/backward 组织进 schedule（[schedules.py](https://github.com/NVIDIA/Megatron-LM/blob/core_v0.19.2/megatron/core/pipeline_parallel/schedules.py) L48、L397、L532）；backward 的非最后 stage 需收 output_tensor_grad |
| backward | 梯度按布局归约（DDP all-reduce、FSDP reduce-scatter、TP 组内同步、PP 梯度回传） | 未提交的累积梯度——前提是截取点在完整 optimizer step 之后 | PyTorch autograd 的 no-grad 边界与图释放语义（[Autograd mechanics](https://docs.pytorch.org/docs/2.6/notes/autograd.html)） |
| gradient accumulation | 计数与未提交梯度归训练驱动（如 Megatron `train_step` 的 micro-step 循环） | 不可默认跳过：mid-step 截取必须显式保存累积计数 | [training.py](https://github.com/NVIDIA/Megatron-LM/blob/core_v0.19.2/megatron/training/training.py) L2336（train_step 组合 forward_step_func/optimizer/schedule） |
| optimizer update | optimizer 对象（分布式实现把 state 分片到 DP 组） | 无 | DistributedOptimizer "shard state across data-parallel ranks"（[distrib_optimizer.py](https://github.com/NVIDIA/Megatron-LM/blob/core_v0.19.2/megatron/core/optimizer/distrib_optimizer.py) L113–124） |
| scaler update | GradScaler（growth tracker 与 scale 是独立状态） | 无；且应在 `update()` 后截取 | PyTorch 2.6 `GradScaler.state_dict`（见上文状态责任矩阵） |
| data commit | sampler/loader 与应用计数（epoch、已提交样本） | 不可跳过；但允许按声明规则重放或去重 | DistributedSampler `set_epoch` 等语义（上文） |

"合法跳步"有两层不同含义，须分开：**合法不序列化暂态**（上文：step 边界截取时飞行激活/未提交梯度可不入 checkpoint）与**合法不更新/不推进**（一次迭代因 overflow 等原因不执行参数更新）。后者以 Megatron core_v0.19.2 的 `train_step` 分支为样板：`optimizer.step()` 返回 `update_successful`（fp16 时由 Megatron 自有的 grad scaler 检测 inf/NaN，语义与 PyTorch GradScaler 不同，见下表）；训练循环把 `update_successful` 经模型并行组归约后分叉——**成功**：推进 `opt_param_scheduler`（增量 = micro-batch 数×micro-batch size×DP size×gtp）并置 `skipped_iter = 0`；**不成功**：置 `skipped_iter = 1`、学习率调度不推进；而 `consumed_train_samples` 在两种分支下都按本迭代序列数推进（[training.py](https://github.com/NVIDIA/Megatron-LM/blob/core_v0.19.2/megatron/training/training.py) L2474、L2518–2531、L3941–3942；`skipped iterations` 作为指标单独累计）。因此恢复契约里要区分**尝试迭代数、成功更新数、scheduler 进度与已消费样本数**四类计数——它们在 overflow 迭代上合法地分叉，不能互相推算。**梯度累积窗口内的完整执行契约（三情形）**：

下表的 scaler 分两列，分别对应两个实现，不能把 PyTorch 列的单次 backoff 套到 Megatron 列上；scheduler 与计数两列按 Megatron `train_step` 记。

| 情形 | 参数更新 | PyTorch 2.6 `GradScaler` | Megatron core_v0.19.2 动态 grad scaler（fp16，未设 `--loss-scale`） | scheduler/成功更新计数（Megatron） | 数据/计数 |
|---|---|---|---|---|---|
| 非最后 micro-step | **不执行** | **不变更 scale，不调用 `update()`**（`update()` 只在整个有效 batch 的所有 `scaler.step()` 之后调用；累积期间 scaled gradients 使用**同一 scale**） | 不触及：scaler 只在 `optimizer.step()` 内的 `prepare_grads` 中检查 inf/NaN 并调用 `update()`（[optimizer.py](https://github.com/NVIDIA/Megatron-LM/blob/core_v0.19.2/megatron/core/optimizer/optimizer.py) L741–774） | 不推进 | 只累积梯度、推进 micro-step 计数与已读取进度 |
| 窗口末、成功 | 执行 optimizer 更新 | `update()`：连续 `growth_interval` 个未跳步后按 `growth_factor` 放大 | `DynamicGradScaler.update(False)`：growth tracker 加 1；累计到 `growth_interval`（`--loss-scale-window`，默认 1000）个连续有限步时，scale 乘 growth_factor（2.0），growth tracker 归零，hysteresis tracker 恢复为 `--hysteresis`（[grad_scaler.py](https://github.com/NVIDIA/Megatron-LM/blob/core_v0.19.2/megatron/core/optimizer/grad_scaler.py) L144–153）；未满一个增长窗口的有限步不恢复 hysteresis tracker | 推进（`skipped_iter=0`；scheduler 步进） | consumed samples 推进（两种分支都推进） |
| 窗口末、overflow | **跳过** optimizer 更新 | `update()` 仍执行：按 `backoff_factor` 缩小 scale、**重置 growth tracker** | `update(True)`：growth tracker 归零，hysteresis tracker 减 1；tracker ≤ 0 时 scale 乘 backoff_factor（0.5），下限为 `--min-loss-scale`（默认 1.0）（grad_scaler.py L138–143；默认值见 [arguments.py](https://github.com/NVIDIA/Megatron-LM/blob/core_v0.19.2/megatron/training/arguments.py) L2913、L2917）。tracker 只在上一行的增长窗口完成时恢复，所以触发 backoff 的 overflow **不必连续**：默认 `--hysteresis 2` 时，自初始化或上次恢复起的第 1 次 overflow 不缩小，第 2 次起每次都缩小，直到下一个增长窗口完成。每次 overflow 都令 `step()` 返回 `update_successful=False`（optimizer.py L816–822），跳过参数更新与是否缩小 scale 无关 | 不推进（`skipped_iter=1`） | consumed samples 仍推进 |

bf16 且未设 `--loss-scale` 时，Megatron 不创建 grad scaler（[optimizer/__init__.py](https://github.com/NVIDIA/Megatron-LM/blob/core_v0.19.2/megatron/core/optimizer/__init__.py) L638–662），`prepare_grads` 直接返回 False（optimizer.py L774），不存在由 loss scaling 引起的 overflow 跳步分支。显式设置 `--loss-scale` 时使用 `ConstantGradScaler`，其 `update()` 不调整 scale（[grad_scaler.py](https://github.com/NVIDIA/Megatron-LM/blob/core_v0.19.2/megatron/core/optimizer/grad_scaler.py) L43–52），上表动态规则不适用。动态 scaler 的 `state_dict` 含 scale、growth tracker 与 hysteresis tracker（L155–165），恢复时三者都要还原，只恢复 scale 会改变后续 overflow 是否缩小的轨迹。

**overflow 跳过更新时 scaler 仍在更新**：PyTorch GradScaler 语义——`scaler.step(optimizer)` 在检测到 inf/NaN 梯度时**跳过 `optimizer.step()`**以避免污染参数（[grad_scaler.py](https://github.com/pytorch/pytorch/blob/1eba9b3aa3c43f86f4a2c807ac8e12c4a7767340/torch/amp/grad_scaler.py) L355–365），但 `scaler.update()` 仍须在每个迭代末尾调用：发生过跳步则按 `backoff_factor` 缩小 scale、连续 `growth_interval` 个未跳步则按 `growth_factor` 放大（L463–480）——即"合法不更新"≠"合法不推进 scaler"。**未完成梯度累积时不得提前发生参数更新**：参数更新只应发生在完整累积窗口结束时；中途保存的恢复点若恢复到累积中途，必须连同未提交梯度与累积计数一起恢复，否则首个更新会只消费部分 micro-batch（mid-step 契约，通用协议 unknown）。应用层 data commit（哪些样本算"已训练"）没有跨框架通用来源，属于各训练系统的显式恢复契约（未声明的保持 unknown，不从 sampler epoch 或样本计数反推）。

回到截取边界：只有当截取点定义在完整 optimizer step 之后，飞行激活、未提交梯度与未决 overflow 决议才允许不入 checkpoint——跳过它们不是优化，而是恢复契约的一部分。VPP/CP 场景下 schedule 内状态更复杂，能否同样跳过没有跨框架通用资料（unknown）。

## MindSpeed-LLM v2.2.0 样板

固定 MindSpeed-LLM v2.2.0 的[高可用性文档](https://github.com/Ascend/MindSpeed-LLM/blob/53f3639c3da9c000a187c44cc0c08d55026ddded/docs/pytorch/features/high_availability.md)说明 distributed optimizer state 分布在 DP 组内，replica optimizer 还会把 DP 组划成副本组。其弹性训练只按 DP 粒度缩扩，并列出 DP size、MoE、长序列、并行组合、配置和缩扩次数限制。这是一个“并行布局直接限制恢复能力”的具体例子，不是任意 world size 恢复的承诺。

同一 commit 的 [`save_checkpoint_wrapper`](https://github.com/Ascend/MindSpeed-LLM/blob/53f3639c3da9c000a187c44cc0c08d55026ddded/mindspeed_llm/training/checkpointing.py)把 model、optimizer、scheduler、RNG 和 iteration 交给外部 Megatron 的 `generate_state_dict`，并补充累计 FLOP；legacy distributed optimizer 与 distributed checkpoint 走不同分支，异步保存只允许 distributed `torch_dist` 格式。同步分支在 barrier 后更新 latest iteration tracker，异步分支把更新注册为 finalize callback。

这段 wrapper 只能支持“调用者传递了哪些对象”和“哪些分支在何时更新 tracker”。`generate_state_dict` 的完整字段、加载顺序、格式兼容和重分片语义属于没有在该文件中固定的外部依赖，保持 `unknown`。该 tag 的 README 指向 PyTorch 2.7.1，并把多个 NPU 组件标为“在研版本”，所以不能与本页 PyTorch 2.6 样板拼成已支持软件组合。

同一 v2.2.0 tag 的并行特性文档补充了平台侧边界：CP 微调要求 `--context-parallel-size` 整除序列长、微调场景 `--attention-mask-type` 只能 `general`（[CP 微调](https://github.com/Ascend/MindSpeed-LLM/blob/v2.2.0/docs/pytorch/features/fine-tuning-with-context-parallel.md)）；MC2 融合计算通信需 CANN 8.0.RC2＋HDK 24.1.RC2 及后续、默认关闭且“可能带来精度问题”、MoE 模型 MLP 不使能（[mc2](https://github.com/Ascend/MindSpeed-LLM/blob/v2.2.0/docs/pytorch/features/mc2.md)）；2D TP 不与 SP/fused-rmsnorm 兼容且不支持 MoE（[tp2d](https://github.com/Ascend/MindSpeed-LLM/blob/v2.2.0/docs/pytorch/features/tensor_parallel_2d.md)）。这些是该 tag 在其配套组合内的有效约束，NPU 驱动/CANN 实际版本未核验，跨版本不自动成立。

## 验证判据与示例

并行策略是否按预期工作，用以下判据核对（每条都对应可观测对象，不以"训练在跑"代替）：

- **映射一致性（区分两种情形）**：同布局原样恢复时，每个 rank 报告的 TP/CP/PP/EP 组成员表、stage 区间与 expert 集合应与 checkpoint 记录一致。若发生**有支持证据的布局转换**（如 DCP `get_state_dict` 在其声明支持范围内跨 trainer 数/并行方式重分片，见上文），则不要求物理 rank/placement 相同，改为验证旧→新逻辑身份的**覆盖与唯一性**及加载结果正确（每个旧逻辑 shard 恰好被新布局承接、无重无漏）；未受支持的第三方转换能力保持 unknown，不做推断。
- **梯度/更新一致性**：固定输入与 seed，比较单步 loss/梯度范数在并行度变化前后的对齐情况（容差内）；分布式优化器分片重建后参数更新等价。
- **吞吐扩展**：固定全局 batch 与模型，记录 step 时间随各并行维度的变化曲线，与选型表的通信/bubble 预期对照；单 rank 计算时间分位暴露负载偏斜（EP 下按 expert token 分布看）。
- **恢复检查**：改变并行度重分片加载后，从同一步继续的有效 token 吞吐与损失曲线不发生无法解释的跳变（详见 [Checkpoint 恢复一致性](checkpoint-state-consistency.md)）。

**有来源的实现例**：MindSpeed-LLM v2.2.0 的 GLM4.5-MoE 106B A3 预训练脚本给出一组完整组合配置（TP=1、PP=4、EP=16、num-experts 128、router-topk 8、dispatcher `alltoall_seq`、grouped-gemm、alltoall overlap comm、permutation async comm），并通过 `--moe-router-load-balancing-type none` 显式选择无辅助损失的 router 策略——这是一个"组合并行＋EP 路由策略"共同决定的官方配置实例（[脚本](https://github.com/Ascend/MindSpeed-LLM/blob/v2.2.0/examples/mcore/glm45-moe/pretrain_glm45_moe_106b_4k_A3_ptd.sh)）；其配套模型表按【Pass】（经昇腾官方版本测试）与【Test】（内部测试）区分认证级别。

**合成反例（明确标注：本库构造，非任何官方记录；静态推导，非启动测试）**：在固定拓扑 64 rank、TP=2、PP=2、ulysses CP=4 的合成配置下（前提：`--use-mcore-models` 已启用——`_validate_cp_args` 的 head 检查位于该前提之后（[arguments.py](https://github.com/Ascend/MindSpeed-LLM/blob/v2.2.0/mindspeed_llm/training/arguments.py) L273 起），且假定已通过其前置的 Megatron 侧校验；world-size 整除 `64 % (2×2×4) == 0`、序列长 `32768 % (2×4) == 0` 均满足），把 `num_attention_heads` 从 48 改为 52：此时 `52 % (4×2) = 4 ≠ 0`，MindSpeed-LLM 的 `_validate_cp_args` 将在启动校验处 raise ValueError——**单独违反 ulysses 头数整除这一条约束**（其余前置约束均满足），用于隔离演示该约束的判定方式。若人为绕过该校验，绕过后的实际执行行为（报错形态或静默错误）**未核实（unknown）**，本库不做断言。该反例说明：启动校验失败是组合合法性的第一道信号，应修正配置而不是绕过校验。

## 常见误解

- **“所有 rank 的权重相同，所以只保存一个 rank 的状态即可。”** DDP 权重副本不覆盖 rank-local RNG、数据进度或应用状态；分片并行下单 rank 权重本身也不完整。
- **“保存了 global step 就保存了训练进度。”** step 与 micro-step、样本数、token 数、scheduler、scaler 和 sampler 位置不是同一状态。
- **“分片只是存储优化，不改变恢复协议。”** shard placement、参数身份和目标布局决定字节由谁读入以及如何组合。
- **“world size 描述了整个并行布局。”** 相同 world size 可以对应不同 DP/TP/PP/EP/CP 分解、group 顺序和 stage 分配。
- **“同 seed 就能续接随机轨迹。”** 多类 generator、rank 映射和随机调用顺序都可能变化。
- **“EP 只是另一种模型并行，随便开就行。”** 专家数须能被 EP 整除（`num_experts % EP == 0`）；dispatch/combine 的 A2A 消息分布由 router 决定，路由偏斜会放大 rank 间负载差；MoE 通信重叠与 TP/CP 在部分硬件代际同用时是性能提醒（`CUDA_DEVICE_MAX_CONNECTIONS` 取舍），不是拒绝启动的硬约束。
- **“SP 和 CP 都是‘序列方向的 TP’。”** SP 在 TP 组内分布激活以消除重复；CP 把输入序列本身分块并交换 KV。约束（头数整除、seq 整除、mask 类型）完全不同。
- **“选型表给出了最优配置。”** 表格只在固定假设下成立；厂商文档的推荐组合（如 2D TP 的 tp-x/tp-y、CP 算法选择）绑定其测试环境，跨环境不自动成立。

## 适用边界与待确认问题

本文的共用模型是“内容、身份、布局、逻辑时间”四部分，`generic` 不表示任何 GPU/NPU 组合已经兼容。PyTorch 结论固定在 2.6 文档和 v2.6.0 源码；Megatron 结论固定在 core_v0.19.2 冻结源码；MindSpeed 结论固定在 v2.2.0 tag（其配套 Mcore 为 core_v0.12.1、PyTorch 2.7.1，与本文其他样板不组成同一环境）；AMD/ROCm 边界以 PyTorch 官方后端文档为限。未安装或运行 PyTorch、MindSpeed、MindIO、TorchNPU、Megatron，也未核验 CANN、驱动、固件和硬件配套。MindSpeed 文档中的性能数字仅为其固定环境的记录，不作为本库预期。

待确认：目标训练框架实际生成的状态 schema，optimizer 与参数稳定身份的映射，设备与模型并行 RNG tracker，DataLoader 的可恢复边界，PP/CP mid-step 状态，目标 NPU 组合的完整加载和重分片能力，以及各状态在失败时允许的重放范围。来源核查和许可证范围见[第四批研究记录](../../docs/research/batch-04-training-sources.md)与[第二十四批研究记录](../../docs/research/batch-24-t06-01-sources.md)。
