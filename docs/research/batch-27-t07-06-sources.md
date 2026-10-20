# 第二十七批 T07-06 来源记录

任务：T07-06（分布式推理布局与并行选择；**new** concept `knowledge/07-inference/distributed-inference-layouts.md`，主题 07.5）。取证轮次：主会话作者角色首轮（2026-10-21；前置 Batch 26 的 T07-02/T07-03 已交付并审阅闭环）。目标：TP/PP/DP/EP/CP/SP（及 dcp）的容量—通信—选型证据，三平台布局限制，跨机初始化与失败的可观察证据。

版本线（沿用既有钉扎）：vLLM v0.14.0＝`b17039bccc17b94a2ea107272ad7bc93508708df`；vLLM Ascend v0.14.0rc1＝`52d4acfa51fb868823d1070b81cbd2d97e9e4696`；MindIE-LLM＝master@`69e5a5dd4b533eaffc7e198320435350825a36f7`（文档线 3.1.0）。v0.14.0 的分布式服务文档在 `docs/serving/`（不在 docs/features/）。本轮未运行任何分布式部署。

## 本轮取回清单（2026-10-21，固定 commit 原文件；SHA-256 前 16 位）

vLLM @b17039bc：

| 文件 | SHA-256 前 16 位 |
|---|---|
| docs/serving/parallelism_scaling.md（220 行） | ee64a18691d16f46 |
| docs/serving/context_parallel_deployment.md（47 行） | 7f0559ad25f36483 |
| docs/serving/data_parallel_deployment.md（133 行） | 24eecb8e13d89f13 |
| docs/serving/expert_parallel_deployment.md（322 行） | 0d21023710921910 |
| docs/serving/distributed_troubleshooting.md（16 行） | e925dff3c9a19a55 |
| vllm/config/parallel.py（703 行） | 0673811d4f37058d |

MindIE-LLM @69e5a5dd（docs/zh/user_guide/feature/）：

| 文件 | SHA-256 前 16 位 |
|---|---|
| tensor_parallel.md（100 行） | d121df6eca46276b |
| data_parallel.md（95 行） | 86bfa6f496129adc |
| context_parallel.md（93 行） | 81079974f242e90a |
| sequence_parallel.md（91 行） | a444200c23cc49b8 |
| expert_parallel.md（99 行） | 34e11a572286c43f |
| expert_parallelism_load_balancer.md（134 行） | b020d1ec5e0d37d7 |
| moe.md（37 行） | 512331151682669e |
| micro_batch.md（94 行） | e5af759ca7e6d0c2 |

另：vLLM Ascend supported_features.md（9c576fc4063ad971，T07-04 轮已取回）重读并行各行；MindIE optimization_and_tuning.md（0c348668366760a0）并行节已在 T07-04 轮登记，本轮交叉引用。

## 主张—来源定位表

### vLLM v0.14.0（上游，NVIDIA/ROCm 通用主线）

| 主张 | 登记 ID | 精确位置 | 支持范围 / 未覆盖 |
|---|---|---|---|
| 选型基线：单卡放得下→不分布式；单机多卡→TP；多机→TP×PP（TP=每机卡数、PP=机数）；模型不均分割或无 NVLink（如 L40S）→PP（按层切、支持不均匀、通信开销更低） | 扩展 src.vllm.inference-v0-14 | parallelism_scaling.md L5–23（指南＋edge case 框） | 官方选型口径；无量化延迟数字 |
| 容量判据的可观察日志：`GPU KV cache size: N tokens` 与 `Maximum concurrency for X tokens per request: Yx`（X 取 ModelConfig.max_model_len）——扩容判据 | 扩展 src.vllm.inference-v0-14 | parallelism_scaling.md L13–20 | 日志行形态；样例数字为文档示例 |
| 执行后端：多机默认 Ray、单机默认 multiprocessing（`distributed_executor_backend`/`--distributed-executor-backend` 可覆盖 mp|ray）；mp 多机用 `--nnodes --node-rank --master-addr --headless`；TP 实现引用 Megatron-LM TP 算法（arXiv:1909.08053） | 扩展 src.vllm.inference-v0-14 | parallelism_scaling.md L31–33、L133–153 | 后端选择与启动形态 |
| 跨机 TP 通信前提：IB 等高速网卡；GPUDirect RDMA 开启条件（IPC_LOCK、/dev/shm 挂载）；**确认判据** `NCCL_DEBUG=TRACE` 下 `[send] via NET/IB/GDRDMA`（高效）vs `[send] via NET/Socket`（跨机 TP 低效） | 扩展 src.vllm.inference-v0-14 | parallelism_scaling.md L155–213 | NVIDIA 语境（NCCL/GDRDMA）；ROCm 侧对应物未在该页给出 |
| Decode Context Parallel（`-dcp`）：KV cache 沿 T 维切分减少复制——tp>H（kv head 数）时 KV 复制 tp_size/H 次；dcp∈[1, tp_size/H]，**不增加 GPU 数只减复制**；交织切分使未来 token 自然分布（Moonshot 提出，arXiv:2507.07120）；案例：DeepSeek-R1（1 kv head）tp8→dcp8、Kimi-K2 tp16→dcp16/8（dcp8 时复制降至 2x 且通信限节点内）、Qwen3-235B-A22B（4 kv heads）tp8→dcp2；MLA 与 GQA 均支持；部分 attention backend 支持 DCP＋MTP | 扩展 src.vllm.inference-v0-14 | cp_deployment.md L19–43 | 机制与案例；prefill CP 两策略（partial query full KV / ring-attention）页内自注 under active development |
| Context Parallel 参数校验（实现）：tp 须被 dcp 整除；total_cp_rank＝pcp_rank×dcp_world_size＋dcp_rank；block_size 须被 cp_kv_cache_interleave_size 整除 | 扩展 src.vllm.inference-v0-14 | config/parallel.py L252–273 | 已核校验逻辑 |
| Data Parallel：MoE（如 DeepSeek MLA）建议 DP attention＋EP/TP MoE；**DP rank 非独立副本**——每 forward 专家层跨全部 rank 同步、无请求 rank 须跑 dummy forward（DP Coordinator 每 N 步 collective 判 idle）；每 rank 独立 core engine 进程（ZMQ 连前端）；每 DP engine 独立 KV cache（负载均衡应考虑排队状态与 prefix 亲和）；`--max-num-seqs` 按 per-DP-rank 计 | 扩展 src.vllm.inference-v0-14 | dp_deployment.md L7–19 | 语义级；ZMQ/Coordinator 实现未逐行核 |
| DP 两种部署模式：self-contained（`--data-parallel-size` 单端点内部均衡）与 external per-rank（`--data-parallel-rank --data-parallel-size-local --data-parallel-address --data-parallel-rpc-port --headless`，外部 LB 逐 rank 部署）；DP×TP 组合时专家层默认成 DP×TP 组，`--enable-expert-parallel` 切 EP | 扩展 src.vllm.inference-v0-14 | dp_deployment.md L11–15、L21–49 | CLI 形态与组合语义 |
| Expert Parallel：`--all2all-backend` 选择（默认 allgather_reducescatter 通用；pplx；flashinfer_all2allv 面向 MNNVL 多机 NVLink；deepep_low_latency 多机示例）；EPLB（`--enable-eplb`）重分配 expert 映射均衡负载；实现约束：EPLB 须 enable_expert_parallel=True 且 TP×DP>1，async EPLB 仅默认 policy | 扩展 src.vllm.inference-v0-14 | ep_deployment.md L15–28、L136–142；config/parallel.py L308–341 | backend 清单与约束；各 backend 性能差异未测 |
| 分布式排障入口：节点间 GPU 通信验证（troubleshooting script）、`NCCL_SOCKET_IFNAME` 随集群创建下发、多 IP 环境的 `No available node types can fulfill resource request`→统一 `VLLM_HOST_IP`＋`ray status`/`ray list nodes` 核对、Ray observability | 扩展 src.vllm.inference-v0-14 | distributed_troubleshooting.md 全文（16 行） | 排障入口；细节指向 usage/troubleshooting.md |
| world_size 语义（实现）：world_size＝TP×PP；world_size_across_dp＝TP×PP×DP | 扩展 src.vllm.inference-v0-14 | config/parallel.py L238–239、L351–354 | 字段语义 |

### vLLM Ascend v0.14.0rc1

| 主张 | 登记 ID | 精确位置 | 支持范围 / 未覆盖 |
|---|---|---|---|
| 并行五行状态：Tensor Parallel Functional（下一步：graph mode 下 TP>4）；Pipeline Parallel Functional（下一步：官方指南）；Expert Parallel Functional（下一步：dynamic EPLB）；Data Parallel Functional（Qwen3 MoE）；Context Parallel Functional（链接 context_parallel 特性页）；功能对齐 vLLM 原则声明 | 扩展 src.ascend.vllm-ascend-v0-14-0rc1 | supported_features.md L20–25（并行各行）＋L3（对齐原则） | 该快照矩阵 |

### MindIE-LLM @69e5a5dd（文档线 3.1.0）

| 主张 | 登记 ID | 精确位置 | 支持范围 / 未覆盖 |
|---|---|---|---|
| 并行参数总约束：dp×tp＝worldSize；cp 与 sp 配合时 dp×tp×cp＝worldSize 且 dp 必须为 1；sp＝tp；**不配置并行参数时默认使用 tp 和 moe_tp**；开启并行的环境变量 PYTORCH_NPU_ALLOC_CONF=expandable_segments:True＋ATB_WORKSPACE_MEM_ALLOC_ALG_TYPE=3 | 扩展 src.ascend.mindie-llm-docs-69e5a5dd | data_parallel.md（使用场景/限制/参数表 L13–24） | 服务化 config 口径 |
| DP：显存足够即可开以提高吞吐；A2＋A3；所有模型 Attention/MLP 模块均支持；可与 TP 同模块叠加 | 扩展 src.ascend.mindie-llm-docs-69e5a5dd | data_parallel.md（限制与约束节） | 文档声明 |
| TP：A2＋A3；DeepSeek-V3/R1/V3.1 支持 lm_head_local_tp 与 o_proj_local_tp（[1, worldSize/节点数]，默认 -1 不开启，配在 ModelConfig→models.deepseekv2.parallel_options）；"tp大于1时，不支持（o_proj local tp）同时开启，也不建议和 LmHead local tp 同开"；PD 分离低时延场景 tp>1 支持 MLA tp 切分 | 扩展 src.ascend.mindie-llm-docs-69e5a5dd | tensor_parallel.md（限制与约束节 L5–12、参数表） | 与 optimization_and_tuning.md 存在口径冲突，见下 |
| **跨页冲突①（保留不裁定）**：optimization_and_tuning.md 称 lm_head/o_proj local tp "仅当 tp=1 时能够开启"且"推荐在 PD 分离且 D 节点**未分布式**的场景"；tensor_parallel.md 称"PD 分离且 D 节点**是分布式**的场景，支持 lm_head 矩阵 local tp 切分和 O project 矩阵 local tp 切分"，并给出 tp>1 与两项 local tp 的排斥/不建议关系。两页对（a）tp=1 前提、（b）D 节点分布式与否两个维度表述不一致 | 扩展 src.ascend.mindie-llm-docs-69e5a5dd | optimization_and_tuning.md L62–68 vs tensor_parallel.md L7–11 | 冲突记录；正文按两说并存、组合 unknown 处理 |
| CP（上下文并行）：A2＋A3；ring 传 KV（类 ring-attention）＋FA2 分块运算＋结果修正；切分份数仅支持 2；不支持单独开启（须同时 SP）；PD 混部时 DP=1、SP=TP、CP×DP×TP＝worldSize，可与 MTP=1/异步调度/Prefix Cache 叠加；PD 分离仅 P 节点开启；**不支持 BF16** | 扩展 src.ascend.mindie-llm-docs-69e5a5dd | context_parallel.md（简介/限制与约束/参数表 L3–25） | 文档声明 |
| SP（序列并行）：KV Cache 切分、各 sp rank 保存不同 KV 省显存支持长序列；SP 必须等于 TP；A2＋A3；PD 分离仅 P 节点；可与 DP×TP 或 CP×TP 叠加（乘积＝worldSize）；可与 MTP=1/异步调度/Prefix Cache 叠加；**不支持 BF16** | 扩展 src.ascend.mindie-llm-docs-69e5a5dd | sequence_parallel.md（限制与约束节 L5–20、参数表） | 文档声明 |
| **跨页冲突②（保留不裁定）**：CP/SP 支持的量化权重集合——context_parallel.md 与 sequence_parallel.md 均列"DeepSeek-R1 的 W8A8、R1 的 W4A8、V3 的 W4A8、V3.1 的 W4A8"（**无 V3-W8A8**）；optimization_and_tuning.md L114/L139 写"当前仅 DeepSeek-V3、DeepSeek-R1、DeepSeek-V3.1 等**模型 W8A8 量化权重**支持此特性"。两处集合不一致（V3-W8A8 与各 W4A8 项互缺） | 扩展 src.ascend.mindie-llm-docs-69e5a5dd | context_parallel.md L9、sequence_parallel.md L9 vs optimization_and_tuning.md L114/L139 | 冲突记录；正文不合成并集也不判谁新 |
| EP：DeepSeek-V2/V3/R1 支持；ep_level 1＝AllGather、2＝AllToAll＋通算融合；**双机部署且 ep_level=2 时两服务器必须经交换机连接，否则拉起服务失败**；专家并行数>32 时 DeepSeek-V3/R1 自动使能 Grouped MatMul 融合算子；ep_level=1 可配 topk 截断（enable_init_routing_cutoff＋topk_scaling_factor，截 hidden_states 无效后段省显存）；ep_level=2 可配 alltoall_ep_buffer_scale_factors（按序列长度选 AllToAll buffer 系数） | 扩展 src.ascend.mindie-llm-docs-69e5a5dd | expert_parallel.md（限制与约束/参数表 L5–30） | 文档声明 |
| EPLB（MindIE）：expert_parallelism_load_balancer.md 独立特性页（134 行）本轮已取回哈希，正文细节留撰写轮展开 | 扩展 src.ascend.mindie-llm-docs-69e5a5dd | expert_parallelism_load_balancer.md（全文） | 已取回；逐条摘录待撰写轮 |
| MoE/micro_batch 特性页与 moe.md（37 行）、micro_batch.md（94 行）已取回（T07-06 边界内辅助：MoE 语义与 micro batching），撰写轮按需引用 | 扩展 src.ascend.mindie-llm-docs-69e5a5dd | moe.md、micro_batch.md | 已取回登记哈希 |

## unknown 清单

1. vLLM config/parallel.py 仅核校验分支与 world_size 语义；Ray/mp 执行器实现、DP Coordinator 与 ZMQ 通信实现未逐行核。
2. vLLM Ascend 的 TP>4×graph mode 限制、PP 官方指南缺失、dynamic EPLB "Next Step" 均为矩阵声明，无实现级证据；vllm_ascend/distributed/ 覆盖件与上游语义差异未核（T07-02 已记 unknown 的延续）。
3. MindIE 两处跨页冲突（TP local tp 前提/场景、SP·CP 量化权重集合）未裁定；产品包 release notes 或后续版本可能修正，本轮无更多证据。
4. MindIE EPLB 页与 moe/micro_batch 页内容未逐条摘录；ranktable 多机组网细节未展开（T07-03 已有 worldSize/ranktable 语义）。
5. AMD ROCm 侧分布式部署差异（RCCL/多机 RDMA 对应 GPUDirect 的口径）未从 ROCm 专属文档取证；本轮仅有上游通用页（NCCL 语境）。
6. 未运行任何分布式部署；全部为文档/源码校验口径。

## 集成轮结果（2026-10-21 已执行）

- 无新增来源条目（本轮文件均落在既有三个固定快照登记的 scope 内）。
- 扩展 2 项 notes：src.vllm.inference-v0-14（docs/serving/ 五页＋config/parallel.py）、src.ascend.mindie-llm-docs-69e5a5dd（并行特性 6 页＋冲突两处）；src.ascend.vllm-ascend-v0-14-0rc1 notes 补并行五行状态。
- registry 维持 542 sources；T07-06 正文进入撰写轮。
