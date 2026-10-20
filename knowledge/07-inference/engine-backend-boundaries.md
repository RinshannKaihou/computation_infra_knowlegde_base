---
id: inference.engine-backend-boundaries
title: 推理引擎组件与平台功能交集档案
type: reference
domain: inference
status: draft
platforms: [nvidia, amd, ascend]
source_refs:
- src.vllm.inference-v0-14
- src.vllm.core-components-v0-14
- src.vllm.platform-interface-0.14
- src.vllm.platforms-cuda-rocm-v0-14
- src.vllm.plugin-system-v0-14
- src.vllm.rocm-install-doc-v0-14
- src.vllm.model-loader-v0-14
- src.vllm.readiness-health-v0-14
- src.ascend.vllm-ascend-v0-14-0rc1
- src.ascend.mindie-llm-repo-69e5a5dd
- src.ascend.mindie-llm-src-69e5a5dd
- src.ascend.mindie-llm-doc-latest
updated_at: "2026-10-20"
applicability:
  environment_refs: []
  notes: "未建立环境档案。三线各自锚定固定 ref：vLLM 上游 v0.14.0（commit b17039bc）、vLLM Ascend v0.14.0rc1 线（commit 52d4acf）、MindIE-LLM master@69e5a5dd（无 release tag，latest 文档站未定版）。三线互不拼接为已验证栈；目标部署组合须现场另行核验。"
verification:
  status: source_checked
  evidence_refs:
  - src.vllm.core-components-v0-14
  - src.ascend.vllm-ascend-v0-14-0rc1
  - src.ascend.mindie-llm-src-69e5a5dd
  notes: "仅核对固定 ref 源码与官方文档语义（锚点见 docs/research/batch-26-t07-02-sources.md 及既有登记 notes）；未安装、构建或运行任何引擎，未实测任何功能交集。"
summary: 对照 vLLM 上游、vLLM Ascend 与 MindIE 的组件分层与调度/KV 语义，给出 NVIDIA/CUDA、AMD/ROCm、Ascend/CANN 三份平台能力交集档案（支持/条件/未证实/冲突）与引擎升级替换的重核验检查表。
related_ids:
- inference.execution-and-kv-cache
- inference.model-loading-and-readiness
- inference.quantization-and-quality
- inference.pd-disaggregation
- inference.latency-metrics
- inference.ascend-inference-oom-triage
---

# 推理引擎组件与平台功能交集档案

本页回答两类问题：其一，三个引擎样板（vLLM 上游、vLLM Ascend 插件、MindIE）各自由哪些组件构成、职责边界在哪；其二，在 NVIDIA/CUDA、AMD/ROCm、Ascend/CANN 三个平台上，模型/量化/并行/图/PD/KV 等特性的支持、条件、未证实与冲突如何登记。装载与启动失败见[权重加载、引擎 ready 与启动失败诊断](model-loading-and-readiness.md)，执行路径细节见[推理执行与 KV cache](execution-and-kv-cache.md)。

**范围与产品包区分**：本文只比较源码仓口径——vLLM 上游 v0.14.0（固定 commit）、vllm-ascend v0.14.0rc1 线（固定 commit，README 最新正式 release 为 v0.11.0，同 commit 的 conf.py/version policy 存在 v0.14.1 与 v0.14.1rc1 标注冲突，按登记保留）、MindIE-LLM 开源仓 master 快照。**MindIE 产品包（闭源部分）与开源仓的功能范围不同**：产品文档门户（JS 渲染）未取证，产品包含而不在开源仓的能力为 unknown；反过来开源仓代码也不等于产品包默认行为。三线版本互不拼接：vllm-ascend README 给出 CANN 8.5.0 配套，MindIE-LLM README 给出 MindIE 软件 2.3.0↔CANN 8.5.0，两条 Ascend 线各自独立。

## 组件对照

| 组件层 | vLLM 上游（v0.14.0） | vLLM Ascend（52d4acf） | MindIE-LLM（69e5a5dd） |
|---|---|---|---|
| 前端/入口 | OpenAI API server（引擎构建后才开始 HTTP 服务）、legacy API server、gRPC server | 复用上游前端 | src/server＋py_interface（Python 框架层 mindie_llm 负责请求接入/文本生成/模型抽象）；gRPC/HTTP 端点在 C++ 层 |
| 调度 | v1/core/sched：Scheduler（实现 SchedulerInterface 抽象，AsyncScheduler 为子类），请求队列 SchedulingPolicy 枚举与 FCFS/Priority 两种实现；chunked prefill 是否启用由最终配置决定（见下节） | 复用上游调度框架；core/ 下另有 recompute_scheduler、scheduler_dynamic_batch 两个覆盖件（与上游的语义差异未核） | src/scheduler：pre_scheduler/post_scheduler 双段＋policy 子树；PreemptionMode 枚举（NONE/SWAP/RECOMPUTE）；可构造策略经 PolicyFactory——普通 PnD/Flex 分支按 layerwiseDisaggregated 构造 LayerwiseFcfsPolicy 或 FcfsPolicy（工厂注释：当前 Prefill/Decode 只支持 FCFS 调度策略），P/D 分支构造 PDDSPolicy；PolicyType 枚举另含 PRIORITY 但工厂未见其实现分派（枚举存在不证明可用）；latency_predictor（scheduler/ 下，与 policy/ 同级）与 dynamic batch（dynamic_batch_size/recorder） |
| KV/块管理 | v1/core：KVCacheManager（usage、prefix cache stats、get_computed_blocks、allocate_slots、free）＋KVCacheBlocks，分层 block_pool/kv_cache_coordinator/single_type_kv_cache_manager | 复用上游框架；utils.py 将 block_size 默认/强制为 128（登记 notes） | src/block_manager：SelfAttnBlockManager（自回归 token 的 KV 分配/交换/回收，提供 prefix caching 与 CoW；cacheBlockSize 当前默认 128）＋block_allocator/block_table/block_tracker/copy_on_write_tracker/ref_counter 等组件族 |
| 模型执行/worker | v1/worker：gpu_worker（设备初始化、内存判定）＋gpu_model_runner（装载、执行）；量化处理在装载后 | 自有 worker/model_runner 覆盖件与 attention/ 目录（NPU 注意力后端） | src/engine（llm_engine、layerwise_mixin、model_exec_output_handler 等）＋src/executor、src/kernels（C++ 执行与算子层） |
| 平台后端 | vllm/platforms：interface.py 定义平台责任面（能力查询、check_and_update_config、verify_model_arch/quantization 等）；cuda.py/rocm.py 为具体实现 | NPUPlatform 继承上游 Platform、以 **OOT（树外插件）** 方式注册；simple_compile_backend 字段默认 eager（该字段的 simple backend 范围，见编译行）；supported_quantization 仅 ascend 量化与 compressed_tensors | 平台即 CANN/TorchNPU 栈本身（经 ATB Models 等组件）；无上游"平台插件"抽象 |
| 其他 | KV offload、PD connector（registry 登记） | eplb、kv_offload、lora、model_loader、compilation、_310p（专用硬件线）子模块 | config_manager、llm_manager(+v2 并存关系未核)、load_balance、sequence、utils |

对照结论（限定源码结构层）：三线都存在"前端—调度—KV/块—执行—平台"五层，但**分层切割点不同**——vLLM 把平台差异收进 platforms 插件层（同一引擎多平台），vllm-ascend 以覆盖件替换核心组件，MindIE 是独立的 Python/C++ 双层引擎。组件名相似不等于语义相同，跨引擎排障时按层对齐而不按名对齐。

## 调度与 KV 策略语义对照（参数不同名不直译）

**chunked prefill 的启用规则（vLLM）**：是否分块由最终配置与模型条件共同决定。默认值推导发生在 EngineArgs 的 `_set_default_chunked_prefill_and_prefix_caching_args`：用户未设置 `enable_chunked_prefill` 时按 `model_config.is_chunked_prefill_supported` 推导并打日志（该函数内保留已显式设置的值）；SchedulerConfig dataclass 的字段默认注释明确"主要为测试便利，实际取值应由 EngineArgs 决定"。**显式设置不是最终生效的无条件保证**：后续模型校验可强制覆盖——例如 encoder-decoder 模型在 `SchedulerConfig.__post_init__` 被直接置 `enable_chunked_prefill = False`（连带关闭 chunked mm 输入与长 prefill 阈值，与用户是否显式开启无关；[arg_utils.py](https://github.com/vllm-project/vllm/blob/b17039bccc17b94a2ea107272ad7bc93508708df/vllm/engine/arg_utils.py)、[config/scheduler.py L214–223](https://github.com/vllm-project/vllm/blob/b17039bccc17b94a2ea107272ad7bc93508708df/vllm/config/scheduler.py#L214-L223)）；调度器内的 pooling 门控注释（scheduler.py L572）限其原上下文。

**批/调度语义的有限对照**（每条锚定源码，覆盖有限场景而非全集）：

- **预算参数的字段与初始化不同**：vLLM SchedulerConfig 区分 `max_num_batched_tokens`（单次迭代的 token 预算，prefill/decode 共用口径）与 `max_num_seqs`（单次迭代 sequence 数上限；[config/scheduler.py L50–61](https://github.com/vllm-project/vllm/blob/b17039bccc17b94a2ea107272ad7bc93508708df/vllm/config/scheduler.py#L50-L61)）；MindIE SchedulerConfig 使用 `maxPrefillBatchSize`/`maxPrefillTokens`/`maxBatchSize`/`dynamicBatchSizeEnable` 等字段（[config_info.h](https://github.com/Ascend/MindIE-LLM/blob/69e5a5dd4b533eaffc7e198320435350825a36f7/src/include/config/config_info.h)），但**字段名不等于运行边界**：已核路径显示，非 chunked 初始预算取 `max(maxSeqLen, maxPrefillTokens)`（[scheduler.cpp L297–308](https://github.com/Ascend/MindIE-LLM/blob/69e5a5dd4b533eaffc7e198320435350825a36f7/src/scheduler/scheduler.cpp#L297-L308)）；开启 chunked prefill 时共享预算改写为 `maxNumBatchedTokens_=maxPrefillTokens`、`maxNumSeqs_=maxBatchSize`（[scheduling_budget.cpp L17–34](https://github.com/Ascend/MindIE-LLM/blob/69e5a5dd4b533eaffc7e198320435350825a36f7/src/sequence/scheduling_budget.cpp#L17-L34)；构造函数同时初始化 partial prefill slot 表，但已核 `GetPrefillSlots`（[L44–72](https://github.com/Ascend/MindIE-LLM/blob/69e5a5dd4b533eaffc7e198320435350825a36f7/src/sequence/scheduling_budget.cpp#L44-L72)）中读取该表的动态分支在固定实现中不可达——chunked 且 `prefillChunkSize≠0` 时返回该配置值、否则返回 `maxPrefillTokens`；实际调用方取三者最小值：待计算 token、剩余共享预算、`GetPrefillSlots()`，见 [policy_helper.cpp L100–106](https://github.com/Ascend/MindIE-LLM/blob/69e5a5dd4b533eaffc7e198320435350825a36f7/src/scheduler/policy/policy_helper.cpp#L100-L106)。**已核路径因此是"配置切块＋剩余共享预算裁剪"，slot 表的动态消费不作为机制依据**），MIX 路径先 running/有条件 swapped、再 waiting 并共用同一预算（[fcfs_policy.cpp L92–111](https://github.com/Ascend/MindIE-LLM/blob/69e5a5dd4b533eaffc7e198320435350825a36f7/src/scheduler/policy/fcfs_policy.cpp#L92-L111)）。**两侧不可直接等价的原因**是阶段选择规则、预算初始化与共享消耗结构各自不同（已核口径：vLLM 单一迭代预算字段 vs MindIE 的初始化/覆盖两段式；slot 表动态路径不可达，不作为差异依据）——不是"一侧计 decode 一侧不计"；对照实验须分别固定各自口径（见[延迟与吞吐指标字典](latency-metrics.md)）。
- **调度先后与抢占的受限对照**：vLLM Scheduler 按 token 进度统一调度、先处理 running 请求再准入 waiting（[scheduler.py L252–289](https://github.com/vllm-project/vllm/blob/b17039bccc17b94a2ea107272ad7bc93508708df/vllm/v1/core/sched/scheduler.py#L252-L289)）；MindIE FcfsPolicy 按阶段优先级分派、MIX 路径同为先 running 后 waiting。**抢占→释放/重置→再入队的已核片段**：vLLM 在 `allocate_slots` 返回 None（块分配失败）这一**已核局部条件**下按序选择抢占对象（[L351–401](https://github.com/vllm-project/vllm/blob/b17039bccc17b94a2ea107272ad7bc93508708df/vllm/v1/core/sched/scheduler.py#L351-L401)；PRIORITY 分支按 priority/arrival_time 选取，另一分支从 running 尾部取出），`_preempt_request` 释放 KV 与 encoder cache、置 PREEMPTED、放回 waiting 队列（[L800–819](https://github.com/vllm-project/vllm/blob/b17039bccc17b94a2ea107272ad7bc93508708df/vllm/v1/core/sched/scheduler.py#L800-L819)）；MindIE FcfsPolicy 先选择 SWAP 或 RECOMPUTE 模式，RECOMPUTE 分支将 running 序列置 WAITING、调用 FreeSeq 并重置计算状态（[fcfs_policy.cpp L468–510](https://github.com/Ascend/MindIE-LLM/blob/69e5a5dd4b533eaffc7e198320435350825a36f7/src/scheduler/policy/fcfs_policy.cpp#L468-L510)；该片段无队列插入操作）。**取证覆盖深度不同**：vLLM 片段已核到"放回 waiting"，MindIE 片段核到"状态重置"、完整再入队链未核——这是本轮取证范围的差异，不是对两引擎实际链条完整性的结论。**完整触发路径两侧均未全面核对**（已核仅上述局部条件与模式选择），不能比较完整"何时抢占"，只能比较"抢占后做什么"。
- **KV 命中与块职责**：vLLM 在 `get_computed_blocks` 计算前缀命中以减少待计算量（[kv_cache_manager.py L164–204](https://github.com/vllm-project/vllm/blob/b17039bccc17b94a2ea107272ad7bc93508708df/vllm/v1/core/kv_cache_manager.py#L164-L204)），块分配/释放集中在 KVCacheManager（`free` 见 [L373](https://github.com/vllm-project/vllm/blob/b17039bccc17b94a2ea107272ad7bc93508708df/vllm/v1/core/kv_cache_manager.py#L373)）；MindIE 的对应职责在 SelfAttnBlockManager（自回归 token 的 KV 分配/交换/回收，含 prefix caching 与 CoW 入口；cacheBlockSize 当前默认 128，cpuBlockNum/npuBlockNum 由模型侧 CacheManager 计算；[self_attn_block_manager.h](https://github.com/Ascend/MindIE-LLM/blob/69e5a5dd4b533eaffc7e198320435350825a36f7/src/block_manager/self_attn_block_manager.h)）。**接口职责相似不证明前缀复用行为等价**——命中判定与块粒度行为差异未实测。
- **观测/诊断入口**不在本页展开：引擎执行与 KV 生命周期见[推理执行与 KV cache](execution-and-kv-cache.md)，启动/OOM 见[推理 OOM 诊断](ascend-inference-oom-triage.md)与[加载与 ready](model-loading-and-readiness.md)，指标口径见[指标字典](latency-metrics.md)。

## 平台能力交集档案

**证据身份分层**：源码事实锚定上文固定 ref；MindIE 的模型支持表属 **latest 文档站（2026-10-20 取回）的文档声明，未与 69e5a5dd 源码或具体产品包核同版**，仅作取回时声明引用，不并入固定源码档案。每行标注支持/条件/未证实/冲突；**缺失依赖不得写成已支持组合**。三份档案都是有限样板（本文与既有登记取证到的范围），不是支持全集。

### NVIDIA / CUDA（vLLM 上游 v0.14.0）

| 特性 | 状态 | 依据与条件 |
|---|---|---|
| 硬件 | 支持 | compute capability 7.0+（V100、T4、RTX20xx、A100、L4、H100 等；[安装页 Requirements](https://docs.vllm.ai/en/v0.14.0/getting_started/installation/gpu/#requirements)）；特性矩阵标注 Volta 无 chunked prefill/prefix caching |
| 制品/运行库 | 条件性 | pip wheel 含**预编译 C++ 与 CUDA 二进制**——同页概述称 CUDA 12.8，而 Pre-built wheels 段声明**默认构建为 CUDA 12.9**（另提供 12.8/13.0 变体）；两种说法在同页并存（固定 ref 的 gpu.cuda.inc.md 亦然，按冲突记录保留）。未选定具体 wheel 变体前，制品身份 unknown；OS Linux、Python 3.10–3.13；不原生支持 Windows |
| 模型 | 按实现 | 模型集由上游实现登记表决定（架构不支持报错见[加载页](model-loading-and-readiness.md)）；本文以 Llama 实现为装载样板 |
| 量化 | 支持（按方法） | 引擎量化文档 14＋方法页（W8A8 等按方法各条件，[quantization 目录](https://github.com/vllm-project/vllm/blob/b17039bccc17b94a2ea107272ad7bc93508708df/docs/features/quantization/README.md)）；**冲突样例**：量化 README 与 int8.md 在 Turing（SM 7.5）上存在">7.5"严格要求与"标为支持"的矛盾（kernel/runtime 边界未证） |
| 并行 | 部分 | TP/PP 为引擎层机制（本文装载机制节）；EP 在 NVIDIA 侧的支持条件本轮未取证（未证实） |
| 编译/图 | 支持 | CUDA graph 为默认路径（enforce_eager 可关）；profile run 见加载页 |
| PD 分离 | 条件性 | experimental；connector 注册表见 [factory.py 注册段](https://github.com/vllm-project/vllm/blob/b17039bccc17b94a2ea107272ad7bc93508708df/vllm/distributed/kv_transfer/kv_connector/factory.py#L146-L204)，NIXL 前置条件见 [nixl_connector_usage.md](https://github.com/vllm-project/vllm/blob/b17039bccc17b94a2ea107272ad7bc93508708df/docs/features/nixl_connector_usage.md#L5-L28)；"不提升吞吐"反面声明见 [disagg_prefill.md](https://github.com/vllm-project/vllm/blob/b17039bccc17b94a2ea107272ad7bc93508708df/docs/features/disagg_prefill.md) |
| KV | 支持 | KVCacheManager 块层（上文）；block 大小默认值未在本档核对（未证实） |
| 样板身份 | — | 模型样板＝上游 Llama 实现读表（装载页）；权重/tokenizer 身份不预置，按[加载页身份表](model-loading-and-readiness.md)现场固定；wheel 变体未选（见制品行）；**驱动版本 unknown**（安装页未给单一值，随所选 wheel 的 CUDA 线现场确定） |

### AMD / ROCm（vLLM 上游 v0.14.0）

| 特性 | 状态 | 依据与条件 |
|---|---|---|
| 硬件 | 支持 | ROCm 6.3+/torch 2.8.0+；MI350 需 7.0+、Ryzen AI MAX/AI 300 需 7.0.2+；gfx90a/942/950、Radeon 1100/1101/1200/1201、1151/1150 |
| 制品/运行库 | 条件性 | **无预编译 ROCm wheel**（源码编译，文档声明 pip install . 不可用）；docker（rocm/vllm、rocm/vllm-dev）推荐；ROCm Triton 指定 commit、flash-attn v2.8.0 可选、AITER/MORI（EP/PD）可选 |
| 模型 | 按实现 | 模型集同上游实现登记（无 ROCm 特定模型清单）；本文以上游 Llama 实作为共同样板，某模型在 ROCm 的可用性按实现与实测取证 |
| 量化 | 代码层清单 | rocm.py supported_quantization 列表（含条件追加 bitsandbytes）；**特性矩阵不含量化/加载格式行，运行支持未实测** |
| 并行 | 部分 | TP/PP 同上游；EP/PD 依赖 AITER/MORI 可选组件（安装页） |
| 注意力 | 条件性 | "V0 attention backends have been removed"；use_rocm_custom_paged_attention 分支；ViT 注意力后端有独立支持集与断言 |
| 特性矩阵 | 部分 | chunked prefill/prefix caching/LoRA/spec decoding/CUDA graph/multimodal ✅；encoder-decoder、async output ❌；prompt-embeds ❔ |
| PD | 未证实 | PD 机制属上游（条件性），ROCm 上的运行与 AITER/MORI 依赖组合未实测；安装页仅声明组件可选 |
| KV | 未证实 | 块层同上游实现；ROCm 侧块大小/注意力分页路径未核 |
| 样板身份 | — | 模型样板＝上游 Llama 实现同源（无 ROCm 特定清单）；权重/tokenizer 按加载页现场固定；**驱动（ROCm 栈）版本与容器/制品身份未选制品前 unknown**（docker 镜像或源码配套随安装方式确定） |

### Ascend / CANN（vllm-ascend 52d4acf＋MindIE-LLM 69e5a5dd，两线分开登记）

| 特性 | vLLM Ascend | MindIE-LLM |
|---|---|---|
| 模型样板 | 具体教程样板＝DeepSeek 系（[DeepSeek-R1](https://github.com/vllm-project/vllm-ascend/blob/52d4acfa51fb868823d1070b81cbd2d97e9e4696/docs/source/tutorials/DeepSeek-R1.md)、[DeepSeek-V3.1](https://github.com/vllm-project/vllm-ascend/blob/52d4acfa51fb868823d1070b81cbd2d97e9e4696/docs/source/tutorials/DeepSeek-V3.1.md)、V3.2、GLM4.x、Kimi-K2-Thinking 教程存在）；README L47 另有 Transformer-like/MoE/Embedding/多模态类别声明。**样板归属**：R1 教程给出 W8A8 量化与 A2/A3 节点条件、V3.1 教程给出 BF16 与量化变体——这些是文档条件；图/EP/PD 对该样板的组合支持 unknown（下述全局行不替代样板级结论）；教程存在不等于具体版本组合支持（未证实） | 读表样板＝Qwen2-7B-Instruct（**latest 取回声明**）：充分验证支持（●）、最大上下文 128k；量化列 W8A8 ✅/W4A8 ❌/W8A16 ❌/LoRA ✅；图列 atbgraph ✅/aclgraph ❌；卡数 Atlas 800I A2 1/2/4 卡（推荐 2 卡）、A3 1/2 卡（推荐 1 卡）、300I Duo 1/2 卡（推荐 1 卡）；快速入门装载示例另用 Qwen2-7B（基础版，勿与 Instruct 行混同） |
| 硬件/配套 | README Prerequisites：Atlas 800I A2 推理系列、Atlas A2 训练系列、Atlas 800I A3 推理系列、Atlas A3 训练系列、Atlas 300I Duo（Experimental）；Linux；Python ≥3.10 且 <3.12；**CANN==8.5.0**、PyTorch==2.9.0、torch-npu==2.9.0；vLLM 与 vllm-ascend 同版本 | 模型支持列表（**latest 取回声明**）按 Atlas 800I A2/A3、300I Duo 给出卡数矩阵 |
| 制品 | 310p/A3 专用 Dockerfile；wheel 见仓库 setup（登记 notes 已核 package metadata） | 容器组件栈与 whl/run 两种安装形态（快速入门，**latest 取回声明**） |
| 量化 | [supported_features.md](https://github.com/vllm-project/vllm-ascend/blob/52d4acfa51fb868823d1070b81cbd2d97e9e4696/docs/source/user_guide/support_matrix/supported_features.md) Quantization 行：W8A8 Functional、W4A8 在研；代码层仅 ascend 量化＋compressed_tensors | 支持列表逐模型给出 W8A8/W4A8/W8A16/LoRA 矩阵；样板 Qwen2-7B-Instruct：W8A8 ✅/W4A8 ❌/W8A16 ❌/LoRA ✅（**latest 取回声明**，两级分级） |
| 编译/图 | simple_compile_backend 字段默认 eager——**该字段只覆盖 simple backend 分支**；同平台实现另有 get_compile_backend、compilation mode、OOT compiler 与 use_inductor 分派及 ACL graph，完整默认执行路径未核（未证实）；MLA graph 限制见 [faqs.md FAQ 14](https://github.com/vllm-project/vllm-ascend/blob/52d4acfa51fb868823d1070b81cbd2d97e9e4696/docs/source/faqs.md) | aclgraph/atbgraph 按模型列入支持矩阵；样板 Qwen2-7B-Instruct 为 atbgraph ✅/aclgraph ❌（**latest 取回声明**） |
| 并行/EP | 大规模 EP 官方教程存在（[README L29–30](https://github.com/vllm-project/vllm-ascend/blob/52d4acfa51fb868823d1070b81cbd2d97e9e4696/README.md#L29-L30) 新闻行）；eplb 子模块存在；教程存在性不等于具体组合支持（未证实） | 卡数矩阵按模型登记（**latest 取回声明**） |
| PD | [supported_features.md](https://github.com/vllm-project/vllm-ascend/blob/52d4acfa51fb868823d1070b81cbd2d97e9e4696/docs/source/user_guide/support_matrix/supported_features.md) Prefill Decode Disaggregation 行：Functional, xPyD；[disaggregated_prefill.md](https://github.com/vllm-project/vllm-ascend/blob/52d4acfa51fb868823d1070b81cbd2d97e9e4696/docs/source/developer_guide/feature_guide/disaggregated_prefill.md)：MooncakeConnector D 拉取/逐层推送 P、异构 P/D 不支持、非对称 TP 仅 P_tp>D_tp 且整除 | KVTransferSchedulePolicy 存在于调度策略族；MindIE 侧 PD 支持材料未取得（**不建立支持结论**，T07-03 核） |
| KV | block_size 默认/强制 128（登记 notes）；kv_offload 子模块存在 | SelfAttnBlockManager 的 cacheBlockSize 当前默认 128（固定源码）；分配算法未核（未证实） |
| 冲突记录 | 同 commit conf.py（vLLM v0.14.1）与 version policy（v0.14.1rc1）标注冲突，按登记保留 | 开源仓无 release tag、文档站 latest 未定版（版本 gate）；训练侧 MindIO TTP 约束不外推到推理 |
| 依赖身份 | **HDK/驱动版本 unknown**（README L55 单列 HDK 参考入口，CANN==8.5.0 不等于 HDK 身份已知）；DeepSeek 样板权重/tokenizer 按教程现场固定；镜像未选（310p/A3 Dockerfile 存在但未选具体制品）——unknown | **HDK/驱动版本 unknown**；样板权重与 **tokenizer 的 revision 均未固定（unknown，待现场按[加载页身份表](model-loading-and-readiness.md)固定）**——读表行的 HF/ModelScope 链接列只给仓库入口，不构成已固定身份；制品未选——unknown |

## 引擎升级或替换的重核验检查表

升级引擎/插件/后端任一层后，按此表重核；每项记录"核验对象的新 ref＋证据位置＋结论"。

1. **身份五元组重建**：新引擎/插件 commit、后端与驱动/运行库版本、容器镜像摘要、模型与 tokenizer 身份（沿用[加载页](model-loading-and-readiness.md)的身份表）。
2. **功能交集重核**：按上表逐特性重新取证（支持/条件/未证实/冲突），旧档案不自动继承——尤其量化方法×硬件、PD connector 依赖、编译后端默认值（vllm-ascend 的 simple_compile_backend=eager 属版本敏感项，且仅覆盖该字段范围）。
3. **数值质量与服务指标基线重测**：固定输入与任务口径的输出质量对照（见[量化与质量](quantization-and-quality.md)），TTFT/TPOT/吞吐基线重测（见[指标字典](latency-metrics.md)）；无参考基线时先建基线再切换。
4. **版本线冲突清点**：升级后重新检查同线内部版本标注（如 vllm-ascend 的 conf.py/version policy 类冲突）与跨线配套声明（CANN/torch_npu/vLLM 版本对），冲突未消解前不宣称组合支持。
5. **回退条件预先固化**：回退到哪个 ref/镜像、回退判据（哪项指标或功能失败触发）、回退后的验证范围（至少身份核对＋功能交集抽检＋一轮质量/指标对照）；回退路径本身也要演练记录。
6. **停用旧能力的显式登记**：升级移除的特性（如 ROCm 侧"V0 attention backends 已移除"类变更）写入替换记录，避免排障时按旧文档推断。

## 来源与验证记录

- vLLM v0.14.0 固定 commit：[调度组件](https://github.com/vllm-project/vllm/blob/b17039bccc17b94a2ea107272ad7bc93508708df/vllm/v1/core/sched/scheduler.py)、[KV 管理](https://github.com/vllm-project/vllm/blob/b17039bccc17b94a2ea107272ad7bc93508708df/vllm/v1/core/kv_cache_manager.py)、[CUDA 平台](https://github.com/vllm-project/vllm/blob/b17039bccc17b94a2ea107272ad7bc93508708df/vllm/platforms/cuda.py)、[ROCm 平台](https://github.com/vllm-project/vllm/blob/b17039bccc17b94a2ea107272ad7bc93508708df/vllm/platforms/rocm.py)。
- vLLM Ascend 52d4acf：[platform.py](https://github.com/vllm-project/vllm-ascend/blob/52d4acfa51fb868823d1070b81cbd2d97e9e4696/vllm_ascend/platform.py)、[README](https://github.com/vllm-project/vllm-ascend/blob/52d4acfa51fb868823d1070b81cbd2d97e9e4696/README.md)；量化/PD/内存等历史核对见 registry 该条 notes（第九/十一/十二批）。
- MindIE-LLM master@69e5a5dd：[src/scheduler](https://github.com/Ascend/MindIE-LLM/tree/69e5a5dd4b533eaffc7e198320435350825a36f7/src/scheduler)、[src/block_manager](https://github.com/Ascend/MindIE-LLM/tree/69e5a5dd4b533eaffc7e198320435350825a36f7/src/block_manager)、[src/engine](https://github.com/Ascend/MindIE-LLM/tree/69e5a5dd4b533eaffc7e198320435350825a36f7/src/engine)；[模型支持列表](https://mindie-llm-doc.readthedocs.io/zh-cn/latest/user_guide/model_support_list/)（latest 未定版）。
- 当前验证范围：仅固定 ref 源码与文档语义核对（锚点与 SHA-256 见 [batch-26-t07-02-sources](../../docs/research/batch-26-t07-02-sources.md)）；未安装、构建或运行任何引擎，未实测任何功能交集。
- 待确认：MindIE 调度策略运行语义与抢占触发条件；MindIE block_manager 分配算法；vllm-ascend 覆盖件与上游的语义差异；MindIE 产品包范围；MindIE 侧 PD 支持（T07-03）；llm_manager(+v2) 关系；各参数跨引擎映射。
