---
id: inference.distributed-inference-layouts
title: 分布式推理布局与并行选择
type: concept
domain: inference
status: draft
platforms: [nvidia, amd, ascend]
source_refs:
  - src.vllm.inference-v0-14
  - src.vllm.rocm-install-doc-v0-14
  - src.ascend.vllm-ascend-v0-14-0rc1
  - src.ascend.mindie-llm-docs-69e5a5dd
  - src.nvidia.nccl-user-guide-2.27.5
  - src.huawei.hccl-api-cann-8.0-rc1-alpha003
updated_at: "2026-10-21"
summary: 推理布局回答"哪些 rank 拿请求、哪些 rank 拿权重、哪些 rank 拿 KV"：纯独立副本 DP 与 MoE 的 DP attention＋跨 DP 专家分片语义不同；TP/PP/EP/CP/SP 各有所有权与同步路径；选型按模型/序列/并发/硬件/互联比较跨机通信代价、扩展效率因素与尾延迟；vLLM（NVIDIA/ROCm 分记）、vLLM Ascend 与 MindIE 的布局限制分别固定并保留跨页冲突；跨机初始化、mapping、通信等待与单副本失败用可观察证据与最小验证设计判定。
related_ids:
  - inference.execution-and-kv-cache
  - inference.pd-disaggregation
  - inference.engine-backend-boundaries
  - inference.latency-metrics
  - inference.quantization-and-quality
  - communication.interconnect-paths
  - communication.collectives-and-rank-progress
  - communication.rdma-baseline-and-congestion-triage
  - communication.bandwidth-baselines
verification:
  status: source_checked
  evidence_refs:
    - src.vllm.inference-v0-14
    - src.ascend.vllm-ascend-v0-14-0rc1
    - src.ascend.mindie-llm-docs-69e5a5dd
  notes: "已核对 vLLM v0.14.0 docs/serving/ 五页与 config/parallel.py 的字段说明及实际赋值/校验分支（另按初审补充核对 vllm/engine/arg_utils.py、vllm/config/vllm.py、vllm/config/model.py 的 dcp 断言）、vLLM Ascend v0.14.0rc1 supported_features 并行各行、MindIE-LLM@69e5a5dd 并行特性六页。ROCm 侧另引已登记的 v0.14.0 安装文档口径。逐条主张与行号锚点见 docs/research/batch-27-t07-06-sources.md（含初审后修订）。未运行任何分布式部署。"
applicability:
  environment_refs: []
  notes: "无环境档案；证据线为 vLLM v0.14.0 固定 commit、vllm-ascend v0.14.0rc1 固定 commit、MindIE-LLM 文档线 3.1.0（master@69e5a5dd）、vLLM v0.14.0 ROCm 安装文档。具体机型、卡数、互联与通信库版本须现场补齐，本文不构成部署建议。"
---

# 分布式推理布局与并行选择

## 定义与要解决的问题

分布式推理布局回答三个所有权问题：**请求由谁接收与分配**（路由/负载均衡层）、**权重由谁持有**（整模型副本还是分片、分片跨不跨副本组）、**KV cache 由谁持有**（每副本独立还是分片/复制）。不同并行方式只是这三个问题的不同答案组合；与训练并行的区别是：推理没有梯度同步与参数更新，副本间可以独立服务不同请求，但模型内并行的每一步 forward 仍需通信，MoE 的专家同步还会穿透副本边界（见下）。

平台口径：NVIDIA/通用证据来自 vLLM v0.14.0 上游（commit `b17039bc`）；ROCm 侧分记上游实现门控与安装文档口径（见"三平台布局限制"）；Ascend 分 vLLM Ascend v0.14.0rc1（`52d4acfa`）与 MindIE 文档线（master@`69e5a5dd`，3.1.0）两条，互不推断。

## 各并行方式的所有者与同步语义

| 方式 | 权重所有者 | KV 所有者 | 请求分配 | 每步同步 | 关键证据 |
|---|---|---|---|---|---|
| DP（纯独立副本，Dense 模型） | 每个 DP rank 持有完整模型 | 每个 DP engine 独立 KV cache | 请求按 rank 分批，各 rank 处理不同请求 | 无跨副本同步（Dense） | [vLLM DP 部署文档 L13–17](https://github.com/vllm-project/vllm/blob/b17039bccc17b94a2ea107272ad7bc93508708df/docs/serving/data_parallel_deployment.md#L13-L17)（独立 core engine 进程＋独立 KV） |
| DP（MoE：DP attention＋EP/TP 专家） | **attention 与专家所有权不同**：TP=1 时 attention 权重跨 DP rank 复制、TP>1 时在各 DP 组内 TP 分片；**专家层跨全部 EP ranks（＝TP×DP 组）分片** | attention 侧各 DP engine 独立 | 请求按 DP rank 分批 | **每 forward 专家层跨全部 rank 同步**（token 按路由分发）；无请求的 rank 跑 dummy forward（DP Coordinator 每 N 步 collective 判 idle） | [ep_deployment L40–59](https://github.com/vllm-project/vllm/blob/b17039bccc17b94a2ea107272ad7bc93508708df/docs/serving/expert_parallel_deployment.md#L40-L59)（层行为表＋TP=2/DP=4 示例）、[dp_deployment L7–15](https://github.com/vllm-project/vllm/blob/b17039bccc17b94a2ea107272ad7bc93508708df/docs/serving/data_parallel_deployment.md#L7-L15) |
| TP（张量并行） | 权重矩阵按维度切分到组内各卡 | KV 按 attention head 切分；**tp 超过 kv head 数 H 时 KV 复制 tp/H 次** | 组内各卡协作同一批请求 | 每 forward 层内集合通信（TP 实现引用 Megatron-LM 算法，[parallelism_scaling L31](https://github.com/vllm-project/vllm/blob/b17039bccc17b94a2ea107272ad7bc93508708df/docs/serving/parallelism_scaling.md#L31)） | [cp_deployment L23–27](https://github.com/vllm-project/vllm/blob/b17039bccc17b94a2ea107272ad7bc93508708df/docs/serving/context_parallel_deployment.md#L23-L27) |
| PP（流水线并行） | 按层切分，各 rank 持一段（支持不均分割） | 本库归纳：各段持有该层 KV、相邻段传递激活（来源仅述按层切分与不均分割支持，未逐列陈述 KV 细节） | 请求流过各段 | 段间点对点传激活（归纳） | [parallelism_scaling L22–23](https://github.com/vllm-project/vllm/blob/b17039bccc17b94a2ea107272ad7bc93508708df/docs/serving/parallelism_scaling.md#L22-L23) |
| EP（专家并行） | 专家分到不同设备（DeepSeek-V2/V3/R1 对接） | 随所在 attention/DP 组 | token 按路由分发专家 | AllGather（MindIE ep_level 1）或 AllToAll＋通算融合（ep_level 2；vLLM 按所选 all2all 后端） | [MindIE expert_parallel](https://github.com/Ascend/MindIE-LLM/blob/69e5a5dd4b533eaffc7e198320435350825a36f7/docs/zh/user_guide/feature/expert_parallel.md)、[ep_deployment L15–26](https://github.com/vllm-project/vllm/blob/b17039bccc17b94a2ea107272ad7bc93508708df/docs/serving/expert_parallel_deployment.md#L15-L26) |
| CP（上下文并行，MindIE） | 与 TP 配合（该页未细列权重切分） | 序列分块计算，KV 经 ring 传递获得分块结果（类 ring-attention＋FA2 分块＋结果修正） | 组内协作 | ring 传 KV＋分块结果修正 | [context_parallel.md L3–13](https://github.com/Ascend/MindIE-LLM/blob/69e5a5dd4b533eaffc7e198320435350825a36f7/docs/zh/user_guide/feature/context_parallel.md#L3-L13) |
| SP（序列并行，MindIE） | 与 TP 配合（该页未细列） | **KV Cache 切分，各 sp rank 保存不同 KV** | 组内协作 | 该页未声明同步机制（unknown） | [sequence_parallel.md L3–21](https://github.com/Ascend/MindIE-LLM/blob/69e5a5dd4b533eaffc7e198320435350825a36f7/docs/zh/user_guide/feature/sequence_parallel.md#L3-L21) |
| DCP（vLLM decode context parallel） | 复用 TP 组 | KV 沿序列维度交织切分，减少 TP 组内复制 | 组内协作 | DCP 组间通信（越大开销越大） | [cp_deployment L19–31](https://github.com/vllm-project/vllm/blob/b17039bccc17b94a2ea107272ad7bc93508708df/docs/serving/context_parallel_deployment.md#L19-L31) |

**DP 与模型内并行的本质区别**：纯独立副本（Dense DP）是服务维度的独立单元（独立进程、独立 KV、独立调度），扩展吞吐与并发且单副本失败理论上不波及其他副本（失败边界见下文验证设计）；模型内并行（TP/PP/EP）是模型维度的分片，扩展单请求可用的内存与算力，但每步 forward 引入通信。**MoE 打破"DP=独立"的简化**：专家层形成跨全部 rank 的 `EP_SIZE＝TP×DP` 组（[ep_deployment L40–42](https://github.com/vllm-project/vllm/blob/b17039bccc17b94a2ea107272ad7bc93508708df/docs/serving/expert_parallel_deployment.md#L40-L42)），不开 `--enable-expert-parallel` 时专家层用 TP（组大小仍为 `DP×TP`，[dp_deployment L11–15](https://github.com/vllm-project/vllm/blob/b17039bccc17b94a2ea107272ad7bc93508708df/docs/serving/data_parallel_deployment.md#L11-L15)）。

**组合示意（本库归纳，依据上述来源约束；不是实际运行时 rank 编号或 placement 的验证结果）**——`TP=2、DP=4`（8 卡，MoE＋EP 开启，对应 ep_deployment 示例）：

```text
请求入口（单一 API 端点 / 外部 LB）
  ├─ DP rank0 组 ─┐
  ├─ DP rank1 组   │ attention：各组内 TP=2 分片（TP>1）
  ├─ DP rank2 组   │ KV：各组独立
  ├─ DP rank3 组 ─┘ 请求：只进本组
  └─ 专家层：跨全部 8 卡的 EP 组（EP_SIZE=TP×DP=8）
       每 forward：token 按路由 dispatch 到专家所在卡 → 结果 combine 回本 DP 组
       无请求的组：dummy forward 对齐（Coordinator 周期性 collective 判 idle）
```

**MindIE 的组合语义以乘积等式表达**：`dp×tp＝worldSize`；开 CP 时 `dp×tp×cp＝worldSize` 且 `dp＝1`、`sp＝tp`（[data_parallel.md 参数表](https://github.com/Ascend/MindIE-LLM/blob/69e5a5dd4b533eaffc7e198320435350825a36f7/docs/zh/user_guide/feature/data_parallel.md)）。vLLM 侧的 world_size 口径需限定：字段说明写 `world_size＝TP×PP`、跨 DP 为 `TP×PP×DP`（[config/parallel.py L238–239、L351–354](https://github.com/vllm-project/vllm/blob/b17039bccc17b94a2ea107272ad7bc93508708df/vllm/config/parallel.py#L238-L239)），但**实际赋值**在普通布局之外还有分支：赋值行乘入 `prefill_context_parallel_size`（[L539–547](https://github.com/vllm-project/vllm/blob/b17039bccc17b94a2ea107272ad7bc93508708df/vllm/config/parallel.py#L539-L547)，PCP 尚在开发），`external_launcher` 后端再乘入 DP（同段）。本文的简式仅指 PCP=1 且非 external launcher 的普通布局。

**KV 复制与 dcp**：GQA/MLA 模型 kv head 数 H 小于 tp 时，TP 组内 KV 复制 tp/H 次。vLLM DCP 沿序列维度再切分：`dcp∈[1, tp/H]`，不增加 GPU 数、只减少复制，代价是通信；交织切分让未来 token 自然分布（[cp_deployment L19–31](https://github.com/vllm-project/vllm/blob/b17039bccc17b94a2ea107272ad7bc93508708df/docs/serving/context_parallel_deployment.md#L19-L31)）。文档案例：DeepSeek-R1（MLA，1 kv head）tp8 复制 8x，`-dcp 8` 消除；Kimi-K2 tp16→`-dcp 16` 完全消除或 `-dcp 8` 降至 2x 且通信限制在节点内；Qwen3-235B-A22B（4 kv heads）tp8 复制 2x，`-dcp 2` 消除。**实际执行断言**（区别于字段说明）：TP 须被 dcp 整除（[arg_utils.py L1387–1395](https://github.com/vllm-project/vllm/blob/b17039bccc17b94a2ea107272ad7bc93508708df/vllm/engine/arg_utils.py#L1387-L1395)）；DCP>1 时 block_size 须 ≥ 且可被 cp_kv_cache_interleave_size 整除（[config/vllm.py L830–854](https://github.com/vllm-project/vllm/blob/b17039bccc17b94a2ea107272ad7bc93508708df/vllm/config/vllm.py#L830-L854)）；GQA/非 MLA 还要求 TP＞总 kv head 数、dcp ≤ TP//H、每 KV head 的 query head 数可被 dcp 整除（[config/model.py L1076–1098](https://github.com/vllm-project/vllm/blob/b17039bccc17b94a2ea107272ad7bc93508708df/vllm/config/model.py#L1076-L1098)）——即 **DCP>1 以 TP>H 为前提**，TP=H 时无可消除的复制、无从开 DCP。MindIE 对应机制是 SP（sp=tp，KV 切分）＋CP（切分份数目前仅 2，须与 SP 同开）。

## 选型表：按约束选布局

综合三平台文档的选型规则（未标注处为本库归纳的判据框架，非来源声明）：

| 约束条件 | 首选布局 | 依据与代价 |
|---|---|---|
| 单卡放得下 | 不分布式 | vLLM 官方基线（parallelism_scaling L7） |
| 单卡放不下、单机多卡放得下 | TP | 跨卡通信走机内互联；TP 要求高带宽机内互联（L8） |
| 单机放不下 | TP×PP（TP=每机卡数、PP=机数） | 跨机通信用 PP 的段间点对点，代价低于跨机 TP 的每层集合通信（L9、L11） |
| 卡数不整分模型 / 无 NVLink（如 L40S） | PP（按层切，支持不均） | parallelism_scaling L22–23 |
| MoE 大规模部署 | DP attention＋EP（或默认 TP）MoE | vLLM dp_deployment L7、ep_deployment L40 起；MindIE ep_level 1/2 |
| 长上下文 / KV 占用主导 | KV 侧并行：先 TP 到 H 上方取得目标性能，再 dcp（vLLM，须 TP>H）/SP·CP（MindIE） | cp_deployment L23–29、L41（先调 TP 再加 dcp）；MindIE sequence_parallel |
| 吞吐扩展、副本独立 | DP（叠加在上述之上） | 每 rank 独立 KV 与调度；MoE 有专家同步例外 |

**布局间的比较维度（本库归纳的比较框架；具体扩展效率、内存分配与尾延迟数值未测，unknown）**：

- **跨机通信代价**：TP 每层 forward 都有跨机集合通信（对互联最敏感，IB/RDMA 见下文判据）；PP 只有段间激活点对点（通信量小但有流水线气泡）；EP 的 dispatch/combine 量随路由与 batch 变化；DP 稳态零跨副本通信（MoE 专家同步除外）。
- **扩展效率的限制因素**：TP 受机内/机间带宽与集合通信同步等待限制；PP 受 stage 负载不均（气泡）限制；EP 受专家负载倾斜限制（vLLM 为此提供 EPLB 重分配专家映射，MindIE 有对应 EPLB 特性页）；DP 近线性但受单副本容量上限与请求均衡质量限制。
- **尾延迟因素**：跨机集合通信的等待（慢 rank 拖整组）、PP 气泡、EP 热点专家排队；观察方法见[collectives 与 rank 进度](../03-communication/collectives-and-rank-progress.md)，带宽基线见[集合通信带宽基线](../03-communication/bandwidth-baselines.md)。

容量判据的可观察证据：vLLM 启动日志的 `GPU KV cache size: N tokens` 与 `Maximum concurrency for X tokens per request: Yx`（X 取 max_model_len）——低于吞吐需求时按上表方向扩（parallelism_scaling L13–20）。尾延迟与吞吐的度量口径见[延迟指标](latency-metrics.md)；互联与拥塞判断见[互联路径](../03-communication/interconnect-paths.md)与[RDMA 基线](../03-communication/rdma-baseline-and-congestion-triage.md)，本文不重复底层实现。

## 三平台布局限制（固定快照）

### vLLM v0.14.0 —— NVIDIA 语境

- **执行后端**：部署指南称多机默认 Ray、单机默认 multiprocessing（[parallelism_scaling L31–33](https://github.com/vllm-project/vllm/blob/b17039bccc17b94a2ea107272ad7bc93508708df/docs/serving/parallelism_scaling.md#L31-L33)）；这是指南口径，**实际选择有实现条件**（[config/parallel.py L590–631](https://github.com/vllm-project/vllm/blob/b17039bccc17b94a2ea107272ad7bc93508708df/vllm/config/parallel.py#L590-L631)）：未显式指定且 world_size>1 时从 mp 起步；CUDA 且 `nnodes>1` 分支选 mp（即用 `--nnodes` 启动多机 mp 不需要 Ray）；本机 GPU 数不足且未正确设置 nnodes/后端时报错并提示选择；`data_parallel_backend=ray` 或已初始化 Ray placement group 时选 ray。结论：多机既可 Ray 也可 mp（`--nnodes/--node-rank/--master-addr/--headless`），排障时应记录最终生效后端而不是从"多机"推断。
- **EP**：`--all2all-backend` 可选——默认 `allgather_reducescatter`（通用，任意 EP＋DP 配置）、`pplx`、`flashinfer_all2allv`（多机 NVLink/MNNVL 系统）、`deepep_low_latency`（[ep_deployment L15–26](https://github.com/vllm-project/vllm/blob/b17039bccc17b94a2ea107272ad7bc93508708df/docs/serving/expert_parallel_deployment.md#L15-L26)）。EPLB（`--enable-eplb`）：实现门控为 `is_cuda_alike()`（CUDA 或 ROCm）、须 `--enable-expert-parallel`、TP×DP>1（[parallel.py L325–338](https://github.com/vllm-project/vllm/blob/b17039bccc17b94a2ea107272ad7bc93508708df/vllm/config/parallel.py#L325-L338)）；async EPLB 仅默认 policy（[L85–88](https://github.com/vllm-project/vllm/blob/b17039bccc17b94a2ea107272ad7bc93508708df/vllm/config/parallel.py#L85-L88)）。
- **prefill CP**：两种策略（partial query/full KV、ring-attention）文档自注 under active development（[cp_deployment L17](https://github.com/vllm-project/vllm/blob/b17039bccc17b94a2ea107272ad7bc93508708df/docs/serving/context_parallel_deployment.md#L17)），不作为可用能力。
- **跨机 TP 通信判据（NCCL/GPUDirect，NVIDIA 语境）**：`NCCL_DEBUG=TRACE` 下 `[send] via NET/IB/GDRDMA`（IB＋GPUDirect RDMA 生效）vs `[send] via NET/Socket`（回退 TCP，跨机 TP 低效）；GPUDirect RDMA 需要 IPC_LOCK 与 /dev/shm 挂载（[parallelism_scaling L155–213](https://github.com/vllm-project/vllm/blob/b17039bccc17b94a2ea107272ad7bc93508708df/docs/serving/parallelism_scaling.md#L155-L213)）。

### vLLM v0.14.0 —— ROCm 侧（有限证据）

已固定的 ROCm 证据分三层。**平台/后端层（实现）**：EPLB 平台门控 `is_cuda_alike()` 覆盖 CUDA 与 ROCm（同上 L325–338）；[platforms/rocm.py L161–169](https://github.com/vllm-project/vllm/blob/b17039bccc17b94a2ea107272ad7bc93508708df/vllm/platforms/rocm.py#L161-L169)——RocmPlatform 的 `dist_backend` 字符串为 `nccl`、`device_type` 为 `cuda`（共享 CUDA 分发路径与 `CUDA_VISIBLE_DEVICES`）；[L508–512](https://github.com/vllm-project/vllm/blob/b17039bccc17b94a2ea107272ad7bc93508708df/vllm/platforms/rocm.py#L508-L512) 通信器类指向 `cuda_communicator.CudaCommunicator`。**库名选择层（实现）**：[utils/nccl.py L17–35](https://github.com/vllm-project/vllm/blob/b17039bccc17b94a2ea107272ad7bc93508708df/vllm/utils/nccl.py#L17-L35)——`VLLM_NCCL_SO_PATH` 可覆盖（覆盖优先）；无覆盖项时 HIP 构建默认**返回** librccl.so.1、CUDA 构建默认返回 libnccl.so.2——这只是库名选择：ROCm 上 backend 名为 nccl、默认库名指向 RCCL，不能从类名（CudaCommunicator）或 backend 字符串推断实际加载与命中。**all-reduce 路径层（实现）**：[cuda_communicator.py L126–174](https://github.com/vllm-project/vllm/blob/b17039bccc17b94a2ea107272ad7bc93508708df/vllm/distributed/device_communicators/cuda_communicator.py#L126-L174)——TP 组 all_reduce 按序尝试 symmetric-mem NCCL→quick reduce（注释注明 just for ROCM MI3*）→custom all-reduce→symm-mem→pynccl，最终兜底 `torch.distributed.all_reduce`；实现注释声明模型运行时 allreduce 只发生在 TP 组。**安装口径（同 commit 文档 [gpu.rocm.inc.md L87–115](https://github.com/vllm-project/vllm/blob/b17039bccc17b94a2ea107272ad7bc93508708df/docs/getting_started/installation/gpu.rocm.inc.md#L87-L115)）**：无预编译 ROCm wheel、docker 推荐、ROCm Triton 钉固定 commit；**AITER 为可选自建组件**（可指定 branch/commit 构建，validated 版本见 Dockerfile.rocm_base），其布局依赖与可省略条件 unknown；**MORI 是文档声明用于 EP 或 PD 分离的可选组件**（gfx942;gfx950）——两者不可混述。**库名→实际加载的桥接（实现）**：find_nccl_library 只返回库名；实际加载链是 CudaCommunicator 构造（world_size>1 时创建 PyNcclCommunicator，[cuda_communicator.py L56–63](https://github.com/vllm-project/vllm/blob/b17039bccc17b94a2ea107272ad7bc93508708df/vllm/distributed/device_communicators/cuda_communicator.py#L56-L63)）→ PyNcclCommunicator 初始化检查（world_size=1 或 `VLLM_DISABLE_PYNCCL` 置 disabled；库加载异常置 unavailable，[pynccl.py L90–105](https://github.com/vllm-project/vllm/blob/b17039bccc17b94a2ea107272ad7bc93508708df/vllm/distributed/device_communicators/pynccl.py#L90-L105)）→ NCCLLibrary 以 find_nccl_library 结果 `ctypes.CDLL` 加载（[pynccl_wrapper.py L311–318](https://github.com/vllm-project/vllm/blob/b17039bccc17b94a2ea107272ad7bc93508708df/vllm/distributed/device_communicators/pynccl_wrapper.py#L311-L318)）。据此分三层：**默认库名选择**（无覆盖项时 HIP→librccl.so.1）、**满足条件可走的实现路径**——以 PyNcclCommunicator **初始化成功**为前提（库加载成功本身不充分：available/disabled 之后还须取得 unique ID、同步、ncclCommInitRank 与 warmup all_reduce，[pynccl.py L104–147](https://github.com/vllm-project/vllm/blob/b17039bccc17b94a2ea107272ad7bc93508708df/vllm/distributed/device_communicators/pynccl.py#L104-L147)），且进入普通 pynccl all_reduce 还以前序优化分支（symm-mem/quick/custom）未返回为前提（[cuda_communicator.py L126–174](https://github.com/vllm-project/vllm/blob/b17039bccc17b94a2ea107272ad7bc93508708df/vllm/distributed/device_communicators/cuda_communicator.py#L126-L174)）——以及**现场实际命中**（须从日志确认，不能从库名或类名断定）。**初始化前提（实现）**：SymmMemCommunicator 要求 `is_cuda()`（ROCm 不构造）；custom/quick all-reduce 受 `use_custom_allreduce` 且 world_size>1 门控，ROCm 分支注释声明该开关为真时当前即 MI300 系列（[cuda_communicator.py L65–90](https://github.com/vllm-project/vllm/blob/b17039bccc17b94a2ea107272ad7bc93508708df/vllm/distributed/device_communicators/cuda_communicator.py#L65-L90)）。**硬件/依赖文档边界（同 commit [gpu.rocm.inc.md L3–14](https://github.com/vllm-project/vllm/blob/b17039bccc17b94a2ea107272ad7bc93508708df/docs/getting_started/installation/gpu.rocm.inc.md#L3-L14)）**：ROCm 6.3+／torch 2.8+；GPU 为 MI200（gfx90a）/MI300（gfx942）/MI350（gfx950，需 ROCm 7.0+）/RX 7900/RX 9000/Ryzen AI（需 7.0.2+）——"单节点 Dense TP、PP=DP=DCP=1、EP 关闭"基线的适用边界以上述文档口径为限（非本库实测配套）；安装三项另见同文件：docker 推荐方式（[L3–6](https://github.com/vllm-project/vllm/blob/b17039bccc17b94a2ea107272ad7bc93508708df/docs/getting_started/installation/gpu.rocm.inc.md#L3-L6)）、无预编译 ROCm wheel（[L22–24](https://github.com/vllm-project/vllm/blob/b17039bccc17b94a2ea107272ad7bc93508708df/docs/getting_started/installation/gpu.rocm.inc.md#L22-L24)）、ROCm Triton 固定 commit 安装（[L47–64](https://github.com/vllm-project/vllm/blob/b17039bccc17b94a2ea107272ad7bc93508708df/docs/getting_started/installation/gpu.rocm.inc.md#L47-L64)，钉 f9e5bf54）。未核（unknown）：各 all2all 后端（pplx/deepep/flashinfer）在 ROCm 的可用组合、DCP/SP 在 ROCm 的支持、GPUDirect RDMA 的 RCCL 对应判据（NCCL 判据不搬运到 ROCm）、ROCm 专属部署文档。

### vLLM Ascend v0.14.0rc1

功能矩阵并行五行均为 Functional——TP（下一步：graph mode 下 TP>4）、PP（下一步：官方指南）、EP（下一步：dynamic EPLB）、DP（Qwen3 MoE）、CP（[supported_features.md L23–26](https://github.com/vllm-project/vllm-ascend/blob/52d4acfa51fb868823d1070b81cbd2d97e9e4696/docs/source/user_guide/support_matrix/supported_features.md#L23-L26) 与 [L31](https://github.com/vllm-project/vllm-ascend/blob/52d4acfa51fb868823d1070b81cbd2d97e9e4696/docs/source/user_guide/support_matrix/supported_features.md#L31)）；"Next Step" 是状态声明，不构成当前能力证据。MoE/非对称 TP 等混合组合不从名称推断：PD 分离的非对称 TP（仅 P_tp>D_tp 且整除）属[PD 分离](pd-disaggregation.md)边界，不外推到常规服务。

### MindIE（文档线 3.1.0）

**配置层级（逐字段，两页写法有差异的照录）**：`tp/dp/cp/sp` 在 ModelDeployConfig 的 ModelConfig（[data_parallel.md 表 1](https://github.com/Ascend/MindIE-LLM/blob/69e5a5dd4b533eaffc7e198320435350825a36f7/docs/zh/user_guide/feature/data_parallel.md)）；`moe_tp/moe_ep` 直接在 ModelConfig 模型项（`moe_ep×moe_tp＝worldSize`，[optimization_and_tuning.md L169–191 示例](https://github.com/Ascend/MindIE-LLM/blob/69e5a5dd4b533eaffc7e198320435350825a36f7/docs/zh/user_guide/optimization_and_tuning.md#L169-L191)）；`ep_level` 在 `models.deepseekv2` 下（[expert_parallel.md 表 1/示例](https://github.com/Ascend/MindIE-LLM/blob/69e5a5dd4b533eaffc7e198320435350825a36f7/docs/zh/user_guide/feature/expert_parallel.md)）；`lm_head_local_tp/o_proj_local_tp` 的层级写法存在**两页差异**：[tensor_parallel.md 参数表 L17–34](https://github.com/Ascend/MindIE-LLM/blob/69e5a5dd4b533eaffc7e198320435350825a36f7/docs/zh/user_guide/feature/tensor_parallel.md#L17-L34) 与[服务化示例 L75–80](https://github.com/Ascend/MindIE-LLM/blob/69e5a5dd4b533eaffc7e198320435350825a36f7/docs/zh/user_guide/feature/tensor_parallel.md#L75-L80)都放在 `models.deepseekv2.parallel_options` 下；[optimization_and_tuning.md L70–85 示例](https://github.com/Ascend/MindIE-LLM/blob/69e5a5dd4b533eaffc7e198320435350825a36f7/docs/zh/user_guide/optimization_and_tuning.md#L70-L85)则将两项直接放在 `models.deepseekv2` 下——两页不一致，照录待核解析实现（复核更正：初审所称"同页参数表与示例不一致"有误，tensor_parallel.md 页内写法一致）。

**硬约束**：不配置并行参数时默认 tp＋moe_tp；SP 必须＝TP；CP 不能单独开（须同时 SP）、切分份数仅 2（[context_parallel.md L32](https://github.com/Ascend/MindIE-LLM/blob/69e5a5dd4b533eaffc7e198320435350825a36f7/docs/zh/user_guide/feature/context_parallel.md#L32)）、**不支持 BF16**、PD 分离时 CP/SP 仅在 P 节点开启（[context_parallel.md L9–25](https://github.com/Ascend/MindIE-LLM/blob/69e5a5dd4b533eaffc7e198320435350825a36f7/docs/zh/user_guide/feature/context_parallel.md#L9-L25)、[sequence_parallel.md L9–21](https://github.com/Ascend/MindIE-LLM/blob/69e5a5dd4b533eaffc7e198320435350825a36f7/docs/zh/user_guide/feature/sequence_parallel.md#L9-L21)；SP 同样不支持 BF16)；PD 混部开 CP 时 dp 必须为 1；DP 暂不支持与 CP 叠加；**EP 双机部署且 ep_level=2 时两服务器必须经交换机连接，否则拉起服务失败**（[expert_parallel.md L25](https://github.com/Ascend/MindIE-LLM/blob/69e5a5dd4b533eaffc7e198320435350825a36f7/docs/zh/user_guide/feature/expert_parallel.md#L25)）；专家并行数>32 时 DeepSeek-V3/R1 自动使能 Grouped MatMul 融合算子（[expert_parallel.md L13–14](https://github.com/Ascend/MindIE-LLM/blob/69e5a5dd4b533eaffc7e198320435350825a36f7/docs/zh/user_guide/feature/expert_parallel.md#L13-L14)）；ep_level=2 时 moe_tp 只能为 1（optimization_and_tuning.md L172 附近）。

**量化×布局组合**：SP/CP 支持的量化权重集合见[量化边界](quantization-and-quality.md)——**该集合存在跨页冲突**：[context_parallel.md L11](https://github.com/Ascend/MindIE-LLM/blob/69e5a5dd4b533eaffc7e198320435350825a36f7/docs/zh/user_guide/feature/context_parallel.md#L11) 与 [sequence_parallel.md L8](https://github.com/Ascend/MindIE-LLM/blob/69e5a5dd4b533eaffc7e198320435350825a36f7/docs/zh/user_guide/feature/sequence_parallel.md#L8) 列"DeepSeek-R1-W8A8、R1-W4A8、V3-W4A8、V3.1-W4A8"（无 V3-W8A8），[optimization_and_tuning.md L114/L139](https://github.com/Ascend/MindIE-LLM/blob/69e5a5dd4b533eaffc7e198320435350825a36f7/docs/zh/user_guide/optimization_and_tuning.md#L114) 写"仅 DeepSeek-V3/R1/V3.1 模型 W8A8 量化权重"，两集合互缺项，两说并存、相应组合 unknown，不合成并集。**另有冲突①（local tp 前提/场景）**：[optimization_and_tuning.md L62–68](https://github.com/Ascend/MindIE-LLM/blob/69e5a5dd4b533eaffc7e198320435350825a36f7/docs/zh/user_guide/optimization_and_tuning.md#L62-L68) 称 lm_head/o_proj local tp "仅当 tp=1 时能够开启"且推荐"PD 分离且 D 节点未分布式"场景；[tensor_parallel.md L9–11](https://github.com/Ascend/MindIE-LLM/blob/69e5a5dd4b533eaffc7e198320435350825a36f7/docs/zh/user_guide/feature/tensor_parallel.md#L9-L11) 称"PD 分离且 D 节点是分布式的场景支持"，并给出"tp>1 时不支持与 o_proj local tp 同开、不建议与 lm_head local tp 同开"——两页在 tp=1 前提与 D 节点场景两个维度表述不一致，同样两说并存。

## 跨机初始化、mapping 与失败的可观察证据

| 观察点 | 可观察证据 | 来源 |
|---|---|---|
| 跨机初始化 | Ray：`ray status`/`ray list nodes` 核对节点与 GPU 数；mp：`--nnodes/--node-rank/--master-addr` 对齐；记录最终生效的执行后端（见三平台节） | [distributed_troubleshooting](https://github.com/vllm-project/vllm/blob/b17039bccc17b94a2ea107272ad7bc93508708df/docs/serving/distributed_troubleshooting.md) |
| mapping/地址 | 多 IP 主机报 `No available node types can fulfill resource request`——**每个节点设为本节点自身可达的地址（各节点值不同），并与该节点上 Ray 所用地址一致**，再用 ray 命令复核选择的地址 | [distributed_troubleshooting.md L11](https://github.com/vllm-project/vllm/blob/b17039bccc17b94a2ea107272ad7bc93508708df/docs/serving/distributed_troubleshooting.md#L11)、[parallelism_scaling L77–104](https://github.com/vllm-project/vllm/blob/b17039bccc17b94a2ea107272ad7bc93508708df/docs/serving/parallelism_scaling.md#L77-L104) |
| 通信路径命中 | `NCCL_DEBUG=TRACE` 下 `[send] via NET/IB/GDRDMA` vs `[send] via NET/Socket`（NVIDIA/NCCL 语境） | [parallelism_scaling L207–213](https://github.com/vllm-project/vllm/blob/b17039bccc17b94a2ea107272ad7bc93508708df/docs/serving/parallelism_scaling.md#L207-L213) |
| 通信等待进展 | 集合通信的 group/成员/操作/进度与时间线字段，见[collectives 与 rank 进度](../03-communication/collectives-and-rank-progress.md)——传输路径命中只证明选路，不证明等待在推进 | 03 领域正文 |
| 通信域建立失败 | MindIE PD 的 kv_link_timeout（通信域建立超时，重试直至成功或超时退出）与 kv_trans_timeout（D 侧拉 KV 超时）——PD 语境，不外推一般 TP/EP 通信域 | [服务参数](mindie-execution-profile.md)（T07-03 取证） |
| 容量与并发 | 启动日志 `GPU KV cache size`/`Maximum concurrency` 两行（见选型节） | parallelism_scaling L13–20 |

**单副本失败的最小证据/验证设计（设计，未执行；运行期表现无文档证据处标 unknown）**：目标是判断"故障是否只影响一个副本/一个组"。证据链按序取证——①请求面：失败/停滞的请求集合（API 错误、超时、空输出），定位其被调度到的 DP rank/组；②进程面：该 rank 对应 core engine 进程状态（存活/退出/心跳）；③组面：故障 rank 参与的组——纯 DP 副本只在本副本组，MoE 还在跨 DP 的专家组（EP_SIZE=TP×DP），据组关系预判影响范围；④其余副本：其他 DP engine 的请求进度是否继续（Coordinator 判 idle 的集体操作是否停滞）；⑤collective 面：故障前后的集合通信进入/完成时间线（[collectives 与 rank 进度](../03-communication/collectives-and-rank-progress.md)的字段）与前序错误；⑥节点/设备面：rank↔进程↔节点↔卡的 mapping（启动日志/.rank 文件）。通过/失败判据：若纯 DP 副本故障且其余副本进度与 collective 时间线正常，判"影响限于单副本"；若故障 rank 在共享专家组内且其他副本的专家同步集体操作停滞，判"跨副本影响"——两类判据都要有②–⑤的证据支撑，不从单一现象推断。

**三项最小验证（框架，未运行）**：correctness——固定小模型与确定输入，分布式布局下输出与单卡基线对照（采样参数固定，区分布局数值差异与合法浮点差异，纪律见[精度差异诊断](../06-training/gpu-npu-precision-difference-triage.md)）；throughput——同负载按布局变体测 goodput，请求失败/超时不得从分母消失；latency——TTFT/尾延迟按[延迟指标](latency-metrics.md)口径分桶观察跨机通信引入的尾延迟。三项共用固定口径：同一模型/权重、同输入输出长度分布、同采样参数、同负载与资源上限，并记录错误与超时。MindIE 侧多机由 ranktable 决定卡号与总 Rank（[服务参数](mindie-execution-profile.md)），布局变更后应重跑三项。

## 常见误解

- **"DP 就是多副本，完全独立"**：Dense 成立；MoE 场景 DP rank 每 forward 需跨 DP 专家层同步，空 rank 跑 dummy forward——副本独立性有例外。
- **"加了卡就该加 TP"**：KV 复制由 tp/H 决定，H 固定后继续加 tp 只增复制；vLLM 在 TP>H 后用 dcp、MindIE 用 SP/CP 在序列维度继续切（DCP>1 以 TP>H 为前提）。
- **"多机 TP 与单机 TP 等价"**：跨机 TP 每层集合通信走跨机网络，指南建议多机用 TP×PP；`NET/Socket` 回退时性能显著劣化（NVIDIA 语境判据）。
- **"多机默认就是 Ray"**：指南如此概述，但实现按条件分支选择（nnodes、后端显式配置、placement group），排障先记录最终生效后端。
- **"并行名相同 = 语义相同"**：vLLM dcp 与 MindIE SP/CP 都切 KV，但组合约束、切分数上限（dcp∈[1,tp/H] vs MindIE CP 仅 2）与量化配伍不同；MindIE SP 与训练语境的序列并行（激活/buffer 分布，见[训练并行与状态](../06-training/parallelism-and-state.md)）语义不同。
- **"布局支持与量化支持独立核对过就行"**：MindIE SP/CP 明确绑定量化权重集合（且有跨页冲突），组合必须整体核。

## 来源与待确认问题

- vLLM v0.14.0：[docs/serving/](https://github.com/vllm-project/vllm/tree/b17039bccc17b94a2ea107272ad7bc93508708df/docs/serving)（parallelism_scaling、context_parallel_deployment、data_parallel_deployment、expert_parallel_deployment、distributed_troubleshooting）、[vllm/config/parallel.py](https://github.com/vllm-project/vllm/blob/b17039bccc17b94a2ea107272ad7bc93508708df/vllm/config/parallel.py)、[vllm/engine/arg_utils.py](https://github.com/vllm-project/vllm/blob/b17039bccc17b94a2ea107272ad7bc93508708df/vllm/engine/arg_utils.py)、[vllm/config/vllm.py](https://github.com/vllm-project/vllm/blob/b17039bccc17b94a2ea107272ad7bc93508708df/vllm/config/vllm.py)、[vllm/config/model.py](https://github.com/vllm-project/vllm/blob/b17039bccc17b94a2ea107272ad7bc93508708df/vllm/config/model.py)。
- vLLM Ascend v0.14.0rc1：[supported_features.md](https://github.com/vllm-project/vllm-ascend/blob/52d4acfa51fb868823d1070b81cbd2d97e9e4696/docs/source/user_guide/support_matrix/supported_features.md)。
- MindIE-LLM@69e5a5dd：[feature/ 并行特性页](https://github.com/Ascend/MindIE-LLM/tree/69e5a5dd4b533eaffc7e198320435350825a36f7/docs/zh/user_guide/feature)（tensor_parallel/data_parallel/context_parallel/sequence_parallel/expert_parallel/expert_parallelism_load_balancer）、[optimization_and_tuning.md](https://github.com/Ascend/MindIE-LLM/blob/69e5a5dd4b533eaffc7e198320435350825a36f7/docs/zh/user_guide/optimization_and_tuning.md)。
- 逐条主张与证据定位见[第二十七批分布式布局来源记录](../../docs/research/batch-27-t07-06-sources.md)（含初审后修订）。
- 待确认：ROCm 布局组合级证据（all2all 后端/DCP/RCCL 判据）——单节点 Dense TP 最小链条已补实现级证据，其余组合仍缺；MindIE 两处跨页冲突（local tp 前提/场景；SP/CP 量化权重集合）；MindIE local tp 参数的 parallel_options 与示例直挂 deepseekv2 的层级差异（解析实现未核）；MindIE SP 的同步机制与权重切分细节（该页未声明）；MindIE EPLB 页细节（已取回待展开）；vLLM Ascend TP>4×graph mode 与 dynamic EPLB 的实现级证据；单副本失败的实际运行表现（本文只交付验证设计）；PCP 与 external_launcher 分支的完整语义。以上未核项保持 unknown。
