# 第二十六批 T07-02 来源记录

任务：T07-02（推理引擎组件与平台功能交集档案；**new** reference `knowledge/07-inference/engine-backend-boundaries.md`，主题 07.2/07.3）。取证轮次：主会话作者角色首轮（2026-10-20；前置 T07-01 已于同日通过审阅闭环）。

版本选择口径：vLLM 上游沿用既有固定 commit `b17039bc`（v0.14.0）；vllm-ascend 沿用既有登记 commit `52d4acf`（v0.14.0rc1 线）；MindIE-LLM 沿用 T07-01 轮钉扎的 master@`69e5a5dd`（无 release tag，版本 gate 继承）。三线版本互不拼接：vllm-ascend README 给出 CANN 8.5.0 配套与 v0.7.3/v0.9.1/v0.11.0 版本线，MindIE-LLM README 给出 MindIE 软件 2.3.0↔CANN 8.5.0——两条 Ascend 线各自独立，也不与 vLLM 上游组合成"已验证栈"。本轮未运行任何引擎。

## 本轮取回清单（2026-10-20）

| 对象 | 版本/ref | SHA-256（前 16 位） |
|---|---|---|
| vllm-ascend codeload 源码包 | 52d4acf（v0.14.0rc1 线） | 98b138527766be0b |
| vllm/v1/core/sched/scheduler.py | b17039bc | b4e664fe7dc9ea5c |
| vllm/v1/core/sched/request_queue.py | 同上 | 4b8d938e5fb8152f |
| vllm/v1/core/kv_cache_manager.py | 同上 | 6362906d91adf7d1 |
| vllm/platforms/cuda.py | 同上 | 2f698ee37b78dee7 |
| vllm/platforms/rocm.py | 同上 | b7fcec9a5263d8f9 |
| vllm_ascend/platform.py | 52d4acf | 94be9c24fa206819 |
| vllm_ascend/README.md → 仓库根 README.md（版本线/配套表；vllm_ascend/ 目录内无该文件——审阅订正 T07-02-C07） | 同上 | 5342a427e0bdc117 |
| MindIE-LLM src/scheduler/scheduler.h | master@69e5a5dd | 3039a647751fb260 |
| MindIE-LLM src/scheduler/pre_scheduler.h | 同上 | 4d5d0b01db1e2d25 |
| MindIE-LLM src/scheduler/policy/policy.h | 同上 | 2de8dc933e0fcae4 |
| MindIE-LLM src/scheduler/policy/fcfs_policy.h | 同上 | 9411e37461a1f972 |
| MindIE-LLM src/scheduler/policy/pdds_policy.h | 同上 | e61fb9b4d4c1d6cb |
| MindIE-LLM src/scheduler/policy/layerwise_fcfs_policy.h | 同上 | fefb8c7032fee938 |
| MindIE-LLM src/block_manager/block_allocator.h | 同上 | 5c075c2d678d30d3 |
| MindIE-LLM src/block_manager/copy_on_write_tracker.cpp | 同上 | 088508a25a9c1fe4 |
| MindIE-LLM src/block_manager/self_attn_block_manager.h | 同上 | 6bb1764f860847e0 |
| MindIE-LLM src/engine/llm_engine.h | 同上 | 95e7ebfa8d7255bb |
| MindIE-LLM src/scheduler/scheduler.cpp（复核轮 R01 补核） | 同上 | 2a46338316abe4ad |
| MindIE-LLM src/sequence/scheduling_budget.cpp（复核轮 R01 补核） | 同上 | e512c6f55db58e02 |
| MindIE-LLM src/scheduler/policy/policy_helper.cpp（复核轮 R01 补核） | 同上 | 6acd5989b39fe8d1 |

## 主张—来源定位表

| 主张 | 登记 ID | 精确位置 | 支持范围 / 未覆盖 |
|---|---|---|---|
| vLLM 调度组件：Scheduler（实现 SchedulerInterface 抽象；AsyncScheduler 为子类）、schedule() 产出 SchedulerOutput；请求队列策略 SchedulingPolicy 枚举与 FCFS/Priority 两种 RequestQueue 实现；**chunked prefill 是否启用由最终配置与模型条件决定**——EngineArgs 在 enable_chunked_prefill 未设置时按 model_config.is_chunked_prefill_supported 推导默认（generate/pooling 分别处理覆盖），SchedulerConfig dataclass 默认仅供测试、实际取值由 EngineArgs 决定，pooling 门控注释（L572）限其原上下文；SchedulerConfig 区分 max_num_batched_tokens（单迭代 token 预算）与 max_num_seqs（单迭代 sequence 上限）；Scheduler 按 token 进度统一调度、先处理 running 请求；**已核局部抢占链**：allocate_slots 返回 None 后按序选择抢占对象（PRIORITY 分支按 priority/arrival_time、另一分支取 running 尾部），\_preempt\_request 释放 KV/encoder cache、置 PREEMPTED、清零计算进度并放回 waiting | NEW src.vllm.core-components-v0-14 | sched/scheduler.py（class Scheduler L65、schedule L252–289、pooling 门控 L572–578、**抢占选择 L351–401 与 \_preempt\_request L800–819（复核轮三补核）**）、sched/interface.py、sched/request_queue.py（SchedulingPolicy L13、FCFS L75、Priority L131）、sched/async_scheduler.py；config/scheduler.py L50–61/L78–83/L214–223；engine/arg_utils.py \_set\_default\_chunked\_prefill\_and\_prefix\_caching\_args L1900–1934 | 组件结构、分派与有限调度语义（含已核局部抢占链）；完整调度算法（token 预算实现细节、完整触发路径、async 模式语义）不在本切面 |
| vLLM KV 管理：KVCacheManager（usage、prefix cache stats、get_computed_blocks、allocate_slots、free、remove_skipped_blocks）＋KVCacheBlocks 抽象；配套 block_pool/kv_cache_coordinator/single_type_kv_cache_manager 分层 | NEW src.vllm.core-components-v0-14 | kv_cache_manager.py（L22 KVCacheBlocks、L94 KVCacheManager 及 L144/152/164/206/373/383 方法）；v1/core/ 目录结构 | 职责面；各 attention 后端的实际分配行为不在此 |
| vLLM 平台层（NVIDIA）：CudaPlatform 的 get_device_capability/get_device_total_memory/get_current_memory_usage/check_and_update_config 责任面 | NEW src.vllm.platforms-cuda-rocm-v0-14 | platforms/cuda.py L130/L138/L150/L251–256 | 责任面（与已登记 interface.py 的抽象对照）；CUDA 特有校验分支未逐条摘录 |
| vLLM 平台层（AMD）：ROCm 平台的 supported_quantization 列表（含条件追加 bitsandbytes）、use_rocm_custom_paged_attention、"V0 attention backends have been removed" 提示、ViT 注意力后端支持集与断言 | NEW src.vllm.platforms-cuda-rocm-v0-14 | platforms/rocm.py L116/L171–188/L299/L303–320 | 能力声明的代码层；运行行为未实测 |
| vllm-ascend 平台实现：NPUPlatform 继承 Platform、_enum 为 **OOT**（树外插件注册）；simple_compile_backend 字段默认 "eager"（**仅该字段的 simple backend 范围**——同实现另有 get_compile_backend/compilation mode/OOT compiler/use_inductor 分派，完整默认执行路径未核）；supported_quantization 仅 ascend 量化与 compressed_tensors；check_and_update_config/get_device_capability | 扩展 src.ascend.vllm-ascend-v0-14-0rc1（notes） | vllm_ascend/platform.py（L95 class NPUPlatform、L99、L104、L159、L175）；编译分派 L234–246/L282–307、compilation/compiler_interface.py L109–139 | 平台责任面；编译默认路径 unknown；平台特有校验分支细节待 T07-03 深化 |
| vllm-ascend 组件覆盖与版本线：子模块覆盖 attention/core（含 recompute_scheduler、scheduler_dynamic_batch 两个核心覆盖件）/device/distributed/eplb/kv_offload/lora/model_loader/compilation/_310p；README 配套 CANN 8.5.0、vLLM 与 vllm-ascend 同版本；维护线 v0.7.3-dev/v0.9.1-dev/v0.11.0-dev；310p/A3 专用 Dockerfile | 扩展 src.ascend.vllm-ascend-v0-14-0rc1（notes） | vllm_ascend/ 目录结构、core/ 目录、platform.py；README.md L29–33/L55–61/L83–93；Dockerfile.310p/Dockerfile.a3 | 覆盖面与版本线；各覆盖件的语义未逐一核对（unknown） |
| MindIE-LLM 引擎组件：src/ 分层为 scheduler（pre/post scheduler＋policy）/block_manager/engine（llm_engine、layerwise_mixin、lora_manager、buffered_responser、seq_group_builder）/config_manager/executor/kernels/llm_manager(+v2)/load_balance/py_interface/sequence/server/utils | NEW src.ascend.mindie-llm-src-69e5a5dd | src/ 目录结构；src/engine/llm_engine.h、engine/ 文件清单 | 组件存在性与文件归属；llm_manager 与 llm_manager_v2 的关系未核（unknown） |
| MindIE-LLM 调度策略族：Policy 基类与 PolicyType 枚举（FCFS/PRIORITY——**枚举存在不证明 PRIORITY 已实现**）；**可构造策略经 PolicyFactory**：PnD/Flex 分支按 layerwiseDisaggregated 构造 LayerwiseFcfsPolicy 或 FcfsPolicy（工厂注释：当前 Prefill/Decode 只支持 FCFS 调度策略），P/D 分支构造 PDDSPolicy，其余角色抛错；KVTransferSchedulePolicy 继承 KVTransferPolicy（PD 的 KV 迁移调度）；PolicyHelper；PreemptionMode 枚举（NONE/SWAP/RECOMPUTE）；SchedulerConfig（config_info.h）有 maxPrefillBatchSize/maxPrefillTokens/maxBatchSize/dynamicBatchSizeEnable 等字段——**字段名不等于运行边界**（复核轮 R01 订正：非 chunked 初始预算取 max(maxSeqLen, maxPrefillTokens)，scheduler.cpp L297–308；开 chunked prefill 时 SchedulingBudget 将共享 maxNumBatchedTokens\_ 置为 maxPrefillTokens、maxNumSeqs\_ 置为 maxBatchSize，scheduling_budget.cpp L17–34（构造函数同时初始化 partialPrefillOccupiedBudgetPerSlot\_ 表，但已核 GetPrefillSlots L44–72 中读取该表的动态分支在固定实现中不可达——chunked 且 prefillChunkSize≠0 返回该配置值、否则返回 maxPrefillTokens，实际调用方 policy_helper.cpp L100–106 取 min(待计算 token、剩余共享预算、GetPrefillSlots())，即已核路径为配置切块＋剩余预算裁剪，slot 表动态消费不作为机制依据——复核轮 R04 订正）；MIX 路径先 running/有条件 swapped 再 waiting 且共用同一预算，decode 同样累计，fcfs_policy.cpp L92–111/L325–337、policy_helper.cpp L48–55）；FcfsPolicy 按阶段优先级分派、MIX 路径先 running/swapped 再 waiting；pre/post 双调度器＋latency_predictor（scheduler/ 下，与 policy/ 同级——审阅订正 T07-02-C07）＋dynamic batch（dynamic_batch_size/recorder）＋stage_policy；**已核抢占模式选择与 RECOMPUTE 分支**（SWAP/RECOMPUTE 模式选择、RECOMPUTE 下置 WAITING、FreeSeq、状态重置——fcfs_policy.cpp L468–510，复核轮三补核；该片段无队列插入操作，完整触发条件与再入队链未核） | NEW src.ascend.mindie-llm-src-69e5a5dd | scheduler/scheduler.h（L33 PreemptionMode、L61 Scheduler:IScheduler）、pre_scheduler.h、policy/policy.h（L22 PolicyType、L67 Policy、L75 KVTransferPolicy）、fcfs_policy.h L63 与 fcfs_policy.cpp L37–111/**L468–510（复核轮三补核）**、pdds_policy.h L27/L38、layerwise_fcfs_policy.h L19、policy_factory.h L21 与 policy_factory.cpp L26–54；include/config/config_info.h L151–176/L399–427；scheduler/ 目录（latency_predictor、policy/ 子目录） | 类结构、可构造路径与有限调度语义（含已核模式选择/RECOMPUTE 片段）；PRIORITY 实现、完整触发条件、再入队链与完整算法未核（unknown） |
| MindIE-LLM 块管理：block_allocator/block_obj/block_table/block_tracker/copy_on_write_tracker/ref_counter/self_attn_block_manager/request_single_block_manager | NEW src.ascend.mindie-llm-src-69e5a5dd | block_manager/ 文件清单与头文件 | 组件清单；分配算法/LRU 语义/与 prefix cache 的关系未逐行核（unknown） |
| 平台能力交集背景（模型支持分级矩阵、loader/探针、Feature×Hardware） | 复用 src.ascend.mindie-llm-doc-latest、src.vllm.model-loader-v0-14、src.vllm.readiness-health-v0-14、src.vllm.rocm-install-doc-v0-14、src.vllm.inference-v0-14、src.vllm.platform-interface-0.14、src.vllm.plugin-system-v0-14 | （既有） | 本轮未重开 |
| 产品包与源码仓范围区分（MindIE 产品文档线 vs MindIE-LLM 开源仓） | 复用 src.ascend.mindie-llm-repo-69e5a5dd、src.ascend.mindie-llm-doc-latest | （既有，T07-01 轮 notes） | 产品包功能范围未取证（hiascend 门户 JS，unknown） |

## unknown 清单

1. vLLM Scheduler 的完整调度算法（token 预算实现细节、完整触发路径、async 模式语义）未全面核对；已核局部抢占链（allocate_slots 返回 None 后的抢占选择 L351–401、_preempt_request 释放/置位/放回 waiting L800–819，复核轮三补核）。
2. vllm-ascend 各覆盖件（recompute_scheduler、scheduler_dynamic_batch、attention、kv_offload 等）与上游对应件的语义差异未核对；_310p（Atlas 300I Duo/310P 线？）目录的适用硬件未从文档确认。
3. MindIE-LLM 各调度策略的运行语义、PreemptionMode 完整触发条件、block_manager 分配算法与 LRU/CoW 行为未全面核对；已核 FcfsPolicy 抢占模式选择与 RECOMPUTE 分支（置 WAITING、FreeSeq、状态重置，fcfs_policy.cpp L468–510，复核轮三补核；该片段无队列插入，完整再入队链未核）；llm_manager 与 llm_manager_v2 并存关系未核。
4. MindIE 产品包（闭源部分）的功能范围与开源仓的差异未取证；产品文档门户 JS 渲染未能直读（继承 T07-01 轮 gate）。
5. vllm-ascend README 中最新 release 为 v0.11.0（2025-12），与登记 commit 所在的 v0.14.0rc1 线的关系（tag 时间序）未逐 tag 核对。
6. 三线的 batch/KV/缓存参数语义对照（如 vLLM max_num_batched_tokens/max_num_seqs 与 MindIE 配置项）未做逐参数映射——正文比较时按"参数不同名不直译"处理。
7. 未运行任何引擎；全部为源码/文档口径。

## 集成轮结果（2026-10-20 已执行）

- 新登记 3 项：src.vllm.core-components-v0-14、src.vllm.platforms-cuda-rocm-v0-14（均沿用固定 commit 的 Apache-2.0 已核验口径）、src.ascend.mindie-llm-src-69e5a5dd（木兰 PSL-2，同 commit LICENSE 已核）。
- 扩展 1 项：src.ascend.vllm-ascend-v0-14-0rc1 的 notes 补第二十六批平台与组件覆盖核对。
- registry 534→537；T07-02 正文进入撰写轮。
