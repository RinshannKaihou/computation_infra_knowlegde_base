# 第二十四批 T06-01 来源记录

任务：T06-01（补齐并行策略选择、专家并行与组合映射；**revise** 既有 `knowledge/06-training/parallelism-and-state.md`，保持原 ID 与单篇主归属）。取证轮次：主会话作者角色首轮（2026-10-18；四路取证子代理因账户 403 全部失败，按 Batch 23 先例改主会话直接取证）。方式：curl 字节级取回固定 tag/commit 的 raw 源码与版本化文档页（SHA-256 见下）＋ codeload 源码包（MindSpeed-LLM v2.2.0）；未运行任何训练/分布式命令。

## 现有正文已覆盖 / 本轮补齐边界

现有 `training.parallelism-and-state` 已覆盖：DP/FSDP/TP/PP 的状态责任矩阵、状态身份（FQN/mesh/placement）、截取边界（step 边界 vs mid-step）、MindSpeed-LLM HA 与 checkpoint wrapper、常见误解。**本轮补齐**：EP 的 token dispatch/combine 与专家负载（Batch 18 已核对 core_v0.19.2 token_dispatcher.py 的登记条目直接复用）；CP/SP 与 TP 的区别；组合并行 rank/mesh/stage/expert/shard 身份样例与冲突检查；固定假设的选型比较表（新增小节，不承诺无条件最优）；Megatron 组合约束校验源码；MindSpeed-LLM 侧 CP/TP2D/MC2/VPP/MoE 官方文档。原文已引用 `docs.pytorch.org/docs/2.6/distributed.tensor.parallel.html`，本轮对该页重开核对（新 SHA）并补源码级锚点。

## 本轮取回清单（curl/codeload，2026-10-18）

| 对象 | 版本 | SHA-256（前 16 位） |
|---|---|---|
| docs.pytorch.org/docs/2.6/distributed.tensor.parallel.html | PyTorch 2.6 文档 | a27a792170f22a11cb |
| torch/distributed/device_mesh.py | tag v2.6.0 | d16e1975093c53fd |
| torch/distributed/tensor/parallel/__init__.py | tag v2.6.0 | 877f1578fe013f22 |
| torch/distributed/tensor/experimental/__init__.py | tag v2.6.0 | f17ddd5747d2c09d |
| torch/distributed/tensor/experimental/_attention.py | tag v2.6.0 | 325e6a434113d42a |
| NVIDIA/Megatron-LM megatron/core/parallel_state.py | tag core_v0.19.2 | 1f6e23a01022c06b |
| NVIDIA/Megatron-LM megatron/training/arguments.py | tag core_v0.19.2 | f7fad20bc0e0cd9b |
| MindSpeed-LLM 源码包（含下列文件） | tag v2.2.0（codeload） | 包 693f619a8b608726 |
| ├ docs/pytorch/features/fine-tuning-with-context-parallel.md | v2.2.0 | f899c7292961f6c5 |
| ├ docs/pytorch/features/ring-attention-context-parallel.md | v2.2.0 | c15aa4faecb39cdb |
| ├ docs/pytorch/features/tensor_parallel_2d.md | v2.2.0 | fcc3dab563fcf720 |
| ├ docs/pytorch/features/mc2.md | v2.2.0 | 1de465bde728e1d5 |
| ├ docs/pytorch/features/virtual_pipeline_parallel.md | v2.2.0 | 126e2895b8f4499d |
| ├ docs/pytorch/features/cc_lora.md | v2.2.0 | f974dcc69574a448 |
| ├ docs/pytorch/models/moe_model.md | v2.2.0 | 5119b6e207cf8328 |
| └ examples/mcore/glm45-moe/pretrain_glm45_moe_106b_4k_A3_ptd.sh | v2.2.0 | 5f065dbb1adb044c |

注：`docs.pytorch.org/docs/2.6/distributed.device_mesh.html` 与 `…experimental.context_parallel.html` 均为 404（2.6 版本化文档无独立页）；DeviceMesh/CP 以 **v2.6.0 源码 docstring** 为证据。MindSpeed-LLM 与既有条目 commit 53f3639c… 为同 tag 内容（codeload tar.gz），字节等同未逐文件核对（tag 一致性由 GitHub ref 保证，未另验）。

## 主张—来源定位表

| 主张 | 登记 ID | 精确位置 | 支持范围 / 未覆盖 |
|---|---|---|---|
| DeviceMesh 语义与多维命名 | NEW src.pytorch.device-mesh-source-v2.6.0 | torch/distributed/device_mesh.py（class DeviceMesh docstring L379–390；submesh mesh_dim_names L87–110） | DeviceMesh 是 n-d 设备布局、值为默认进程组 global rank；作为集群内通信代理；**遵循 SPMD 编程模型**；mesh_dim_names 可为各维命名（示例 ("dp","cp","tp")）——组合并行身份样例的直接依据 |
| PyTorch TP API 面 | 复用 src.pytorch.parallel-training-state-2.6（重开 distributed.tensor.parallel 页）＋NEW 源码条目 | tp/__init__.py `__all__` L14–23；文档页重开 | ColwiseParallel/RowwiseParallel/SequenceParallel/ParallelStyle/PrepareModuleInput/PrepareModuleOutput/parallelize_module/loss_parallel 为 2.6 实际导出面；SP 作为 ParallelStyle 与 TP 同 API 面——SP/TP 区别的 PyTorch 侧依据 |
| PyTorch CP（实验 API） | NEW src.pytorch.cp-experimental-source-v2.6.0 | experimental/__init__.py L1–11（__all__）；_attention.py `context_parallel` L1211–1276、`context_parallel_unshard` L1279+ | 2.6 的 CP 为 experimental：context_parallel 上下文管理器①patch SDPA 为 CP 版、②把 buffers 沿序列维切分（in-place、退出恢复、no_restore_buffers 可选）；context_parallel_unshard 反切输出；implicit_replication 带不正确结果警告——CP 与 TP 切分对象不同（序列维 vs 权重维）的官方依据 |
| Megatron 并行域初始化与组合 | 复用 src.nvidia.megatron-lm-core-v0.19.2（本轮重开补锚点） | parallel_state.py `initialize_model_parallel` L601+；L123–131（_CONTEXT_PARALLEL_GROUP 及 KV/dKV 交换 rank 注释、分层 CP 组、DP×CP 混合组）；L133–135（full DP 组=replicate_DP×gtp_remat）；get_data_parallel_group(with_context_parallel=, partial_data_parallel=) L1758–1807；get_tensor_and_context_parallel_group L1923–1928 | Megatron 侧组合映射：TP/PP/CP/EP 各有独立 process group；DP 组可选含/不含 CP 维；"tensor+context" 组独立存在——组合并行 group 身份样例与冲突检查的实现依据 |
| Megatron 组合约束校验 | 复用 src.nvidia.megatron-lm-core-v0.19.2（本轮重开补锚点） | megatron/training/arguments.py L1295–1298（seq_length 须为 2×CP 的倍数）、L555–567（hierarchical CP 乘积须等于 CP size；a2a+p2p 须设 hierarchical）、L1600–1603（num_experts 须能被 EP size 整除即 num_experts % EP == 0、EP>1 须设 num_experts；修订轮二更正方向表述）、L998–1006（FSDP2 不支持 PP>1/EP>1/distributed optimizer）、L1426–1431（overlap_moe_expert_parallel_comm 在 Hopper 及以前避免与 TP/CP 同用、需更大 CUDA_DEVICE_MAX_CONNECTIONS）、L1447（EP>1 时 ep_dp 进 high_priority_stream_groups） | 组合并行的**冲突检查表**官方依据：CP×seq、EP×experts、FSDP2 互斥组、MoE 通信 overlap 限制 |
| Megatron EP token dispatch/combine | 复用 src.nvidia.megatron-lm-core-v0.19.2（Batch 18 已核对，含 SHA 与行号） | token_dispatcher.py L372–383/690–720/817–862（MoEAlltoAllTokenDispatcher 工作流、A2A dispatch、TP>1 时 combine 前 RS、split 交换）；moe_utils.py L423–467（tokens m×H 行选、probs [m]） | EP 机制（dispatch/combine、expert 负载、通信形状）已核对的冻结实现证据；本轮未重开文件，锚点沿用既有登记 notes |
| Megatron MoE 参数面 | 复用 src.nvidia.megatron-lm-core-v0.19.2 | arguments.py --num-experts L3351、--moe-router-load-balancing-type L3365、--moe-layer-freq L3353、--moe-aux-loss-coeff L3369、--moe-use-upcycling L3361 | MoE 配置字段与专家负载均衡（aux loss/router 类型）入口；并行度参数由 TransformerConfig/ModelParallelConfig 字段经参数工厂生成 CLI（argument_utils.py L96–107/L214–229 将 dataclass 字段转为 --kebab-case 旗标；CLI 实际解析未运行）——修订轮更正：此前"无 CLI 定义"的说法不成立 |
| MindSpeed-LLM CP 微调与算法选择 | NEW src.ascend.mindspeed-llm-parallel-features-v2.2.0 | fine-tuning-with-context-parallel.md（--context-parallel-size 须整除序列长度；微调 CP 场景 --attention-mask-type 只能 general；--context-parallel-algo 三选：megatron_cp_algo/ulysses_cp_algo/hybrid_cp_algo；seq/cp>8k 建议；Llama2-7B 32k TP2/PP1/CP4 两算法吞吐对照表） | Ascend 侧 CP 的官方使用边界与算法选择依据；性能数字仅为其文档表格（Atlas 环境），不作为本库结论 |
| MindSpeed-LLM Ring Attention 机制 | NEW src.ascend.mindspeed-llm-parallel-features-v2.2.0 | ring-attention-context-parallel.md（分块 softmax、KV 块环形传递、计算通信重叠条件 c≥F/B 与 S/(T·α)≥1/(W·β)、无需 head_size 整除、须开 FlashAttention、8k 以下可能负优化、默认 ulysses_cp_algo） | CP 与 TP/DP 的机制差异（序列维切分+KV 环通信）的官方中文文档依据；引用 arXiv:2310.01889 |
| MindSpeed-LLM 2D TP | NEW src.ascend.mindspeed-llm-parallel-features-v2.2.0 | tensor_parallel_2d.md（--tp-2d + tp=N1×N2，N1/N2>1；不兼容 --sequence-parallel/--use-fused-rmsnorm；不支持 MoE；推荐大 TP 场景；融合算子依赖 CANN 8.0.1.B020+ 且仅 micro-batch-size=1；三个 forward 优化参数互斥） | TP 组内再切分的组合约束反例（TP2D × SP/MoE 冲突） |
| MindSpeed-LLM MC2 | NEW src.ascend.mindspeed-llm-parallel-features-v2.2.0 | mc2.md（前提 CANN 8.0.RC2+HDK 24.1.RC2 及后续；默认关闭需改 arguments.py；可能精度问题；MoE 模型 MLP 不使能；TP+SP 场景建议开启） | 计算通信融合与 TP/SP 的关系及版本前提；"版本不混用"边界例子 |
| MindSpeed-LLM VPP | NEW src.ascend.mindspeed-llm-parallel-features-v2.2.0 | virtual_pipeline_parallel.md（16 层 TP1 PP4 VPP2 → 8 段示例；以更多通信换更低空泡；引用 SC21 Megatron-LM 论文） | pipeline bubble 与 VPP 的取舍表述依据 |
| MindSpeed-LLM MoE/EP 官方脚本与模型表 | NEW src.ascend.mindspeed-llm-parallel-features-v2.2.0 | examples/mcore/glm45-moe/pretrain_glm45_moe_106b_4k_A3_ptd.sh（TP=1/PP=4/EP=16；--num-experts 128 --moe-router-topk 8 --moe-token-dispatcher-type alltoall_seq --moe-grouped-gemm --moe-alltoall-overlap-comm --moe-permutation-async-comm --n-shared-experts 1 --moe-router-load-balancing-type none 等）；docs/pytorch/models/moe_model.md（预置 MoE 模型表：【Pass】=经昇腾官方版本测试、【Test】=内部测试；Qwen3-30B-A3B 2x8 Pass、Qwen3-235B 16x16 Test） | Ascend EP 官方组合配置样例（有来源实现例候选）；模型认证分级口径 |
| AMD/ROCm 分布式边界 | 复用 src.pytorch.distributed-backend-2.6＋src.pytorch.hip-notes-2.6 | （Batch 17 已核对） | PyTorch ROCm 后端支持条件与差异；不把 NCCL 命令套用到 AMD。本轮未重开 |

## unknown 清单

1. Megatron developer guide（docs.nvidia.com latest 线）为可变页，既有条目已注明"不作实现证据"；本轮未使用 latest 页新增主张，EP/CP 结论全部锚定 core_v0.19.2 源码。
2. core_v0.19.2 的并行度 CLI 由 TransformerConfig/ModelParallelConfig 字段经参数工厂生成（argument_utils.py L96–107/L214–229；修订轮更正：首轮"未定义 CLI"的表述不成立——未找到字面量 add_argument 不等于无生成入口）；CLI 实际解析未运行。
3. MindSpeed（核心仓，非 LLM 套件）的 CP 算法文档（gitcode 链接）未取回；MindSpeed-LLM 文档对其为外链引用，本轮不转述其内容细节。
4. MC2/TP2D 融合算子的 ATB/CANN 组件配套仅到文档声明的版本门槛；实际硬件行为、精度影响范围 unknown。
5. PyTorch CP experimental API 在 NPU（TorchNPU）上的可用性：无一手资料，unknown；不以 CUDA 语义推定。
6. 全部性能数字（MindSpeed-LLM 文档表、cc_lora 提升表）为厂商文档口径（特定 Atlas 环境与配置），本库只作"存在该文档记录"引用，不作为通用预期。
7. 未运行任何代码：所有 dispatch/combine 形状、约束断言均为源码/文档转述。

## 建议登记条目（3 条新增；Megatron/PyTorch 主样板条目为复用＋重开补证）

```yaml
- id: src.pytorch.device-mesh-source-v2.6.0
  title: PyTorch v2.6.0 DeviceMesh 与张量并行导出源码（冻结）
  url: https://github.com/pytorch/pytorch/blob/v2.6.0/torch/distributed/device_mesh.py
  kind: repository
  registered_at: '2026-10-18'
  revision: tag v2.6.0；curl raw 取回 2026-10-18（device_mesh.py SHA-256 d16e1975093c53fd6e5415adf6c3f98093b7a03cc8123b905f5c8dfa13246012、tensor/parallel/__init__.py 877f1578fe013f22d37aea8665a971442123dc0be5eca7741a3c9ba341bdc058）；2.6 版本化文档无 device_mesh 独立页（404 实开确认）
  license:
    status: partial
    scopes:
    - scope: PyTorch v2.6.0 仓库自有代码与随附文档
      identifier: BSD-3-Clause
      url: https://github.com/pytorch/pytorch/blob/v2.6.0/LICENSE
    notes: 沿用既有 PyTorch 条目许可口径；仅链接并原创归纳。
  notes: Batch 24（T06-01）取证：DeviceMesh=n-d 设备布局（值为默认进程组 global rank）、通信代理、SPMD 编程模型、mesh_dim_names 命名（示例 dp/cp/tp）；tensor.parallel __all__（Colwise/Rowwise/SequenceParallel、ParallelStyle、PrepareModuleInput/Output、parallelize_module、loss_parallel）。未运行代码。
- id: src.pytorch.cp-experimental-source-v2.6.0
  title: PyTorch v2.6.0 Context Parallel experimental 源码（冻结）
  url: https://github.com/pytorch/pytorch/blob/v2.6.0/torch/distributed/tensor/experimental/_attention.py
  kind: repository
  registered_at: '2026-10-18'
  revision: tag v2.6.0；curl raw 取回 2026-10-18（_attention.py SHA-256 325e6a434113d42ae4742545bb926215b8a8f7013bf0348091088b7c3ae3fb12、experimental/__init__.py f17ddd5747d2c09dd322aaacc2c8bee9074f1040a569f385ba21b2baf3b995f3）
  license:
    status: partial
    scopes:
    - scope: PyTorch v2.6.0 仓库自有代码与随附文档
      identifier: BSD-3-Clause
      url: https://github.com/pytorch/pytorch/blob/v2.6.0/LICENSE
    notes: 沿用既有 PyTorch 条目许可口径；仅链接并原创归纳。
  notes: Batch 24（T06-01）取证：context_parallel 上下文管理器（patch SDPA＋沿序列维 in-place 切分 buffers、退出恢复、no_restore_buffers、不得含 Parameter）；context_parallel_unshard；implicit_replication 带错误结果警告；导出面 context_parallel/implicit_replication/local_map/register_sharding。CP 在 2.6 为 experimental。未运行代码。
- id: src.ascend.mindspeed-llm-parallel-features-v2.2.0
  title: MindSpeed-LLM v2.2.0 并行特性文档与 MoE 官方脚本（CP/TP2D/MC2/VPP/MoE）
  url: https://github.com/Ascend/MindSpeed-LLM/blob/v2.2.0/docs/pytorch/features/ring-attention-context-parallel.md
  kind: documentation
  registered_at: '2026-10-18'
  revision: tag v2.2.0；codeload 源码包取回 2026-10-18（包 SHA-256 693f619a8b608726c23dc53a7e0d283684883149fb140951f169a297fe72936e；各文件哈希见 docs/research/batch-24-t06-01-sources.md）；与既有条目 commit 53f3639c… 同 tag
  license:
    status: identified
    scopes:
    - scope: 固定 tag 的 features 文档、models 文档与 examples 脚本；根 LICENSE 声明范围
      identifier: BSD-3-Clause
      url: https://github.com/Ascend/MindSpeed-LLM/blob/v2.2.0/LICENSE
    notes: 根 LICENSE 列出若干第三方文件其他许可；不复制文档长段与性能表，仅引用口径。
  notes: Batch 24（T06-01/T06-03 共用）取证：CP 微调（cp-size 整除序列长、mask 只能 general、三种 cp 算法、seq/cp>8k 建议、两算法吞吐表）；Ring Attention 机制（KV 环通信、重叠条件、须 FlashAttention、8k 以下可能负优化）；TP2D（tp=N1×N2、不兼容 SP/fused-rmsnorm、不支持 MoE、融合算子 CANN 8.0.1.B020+）；MC2（CANN 8.0.RC2+HDK 24.1.RC2 前提、默认关、可能精度问题、MoE MLP 不使能）；VPP（空泡/通信取舍与 16 层示例）；GLM4.5-MoE 106B A3 预训练脚本（TP1/PP4/EP16 与全部 MoE 参数）；moe_model.md 预置模型 Pass/Test 分级；cc_lora（--lora-fusion、与 --overlap-param-gather 冲突、兼容 PP/VPP/dist-optimizer）。性能数字仅为其文档口径。未运行任何脚本。
```

## 修订轮二补充（2026-10-18，复核轮发现处理）

- R01：全局 batch 合成口径改为 micro-batch 1×累积×DP=512（纯 DP/FSDP dp=64 累积 8；TP/PP/VPP/CP2 dp=32 累积 16；CP4 dp=16 累积 32；EP 行 dense dp=32）；微批公式锚点更正为 megatron/core/num_microbatches_calculator.py（SHA-256 a540540481321f233a23355bd5857854e3bfc86d36e69f611d1c7b66dd8d494f）。
- C02：expert grid 身份按源码语义补齐（两套 RankGenerator、EP/CP 分属两 grid、expert_dp=world/(ETP×EP×PP)、PP 组两 grid 一致；parallel_state.py L479–491/L871–907）；rank 37 的 EP 组 {37,45,53,61} 等为合成约定（实际 order unknown）；expert_dp=4≠dense dp=8 已写明；层号示例修正为 stage 内合法层。
- C05：取证 L40 整除方向更正为"num_experts 能被 EP 整除"。
- C06：补 scaler 语义（overflow 跳过 optimizer.step 但 update() 仍执行并调整 scale；grad_scaler.py L355–365/L463–480，与登记 SHA 一致）；补"未完成累积不得提前更新"边界。
- C07：反例补 --use-mcore-models 前提（arguments.py L276–277 在 head 检查之前）与"假定已过前置 Megatron 校验"限定。

## 修订轮三补充（2026-10-19）

- C01：补公共放置约定（node = rank//8）与各候选通信组放置标注。
- C02：补合成分配规则（EP 组内序号 k → experts [32k,32k+32)；rank 37 持 0–31）与完整参数 shard 身份（gate_proj [11008,4096] bf16、ETP=2 第 0 维 row-shard、rank 37 offset 5504、本地 [5504,4096]；expert-DP 副本语义；覆盖检查）。
- C06：补梯度累积窗口三情形表（非最后 micro-step 不调 update 不变 scale；窗口末成功/overflow 分支）。

## 修订轮四补充（2026-10-19，复核第三轮发现处理）

- C01：统一轴序公式（[pp,dp,cp,tp] 慢→快）与逐候选步长重算，放置标注更正；S3-01：overflow 行 growth tracker 改为重置（连续未跳步计数归零）。

## 修订轮五补充（2026-10-19，复核第四轮发现处理）

- S4-01：选型表 EP 行 expert-DP 组放置更正为「8 成员 stride 2、跨两个节点（相邻对同节点）」；身份样例处补「放置随 EDP 大小变化」限定。

## 修订轮六补充（2026-10-19，复核第五轮发现处理）

- S4-01 精确化：expert-DP 组（EDP=8、stride 2）跨两个节点、**每节点 4 个成员**，补完整组例 {0,2,4,6,8,10,12,14}；修正上一轮"只有相邻成员对同节点"的错误说法。
