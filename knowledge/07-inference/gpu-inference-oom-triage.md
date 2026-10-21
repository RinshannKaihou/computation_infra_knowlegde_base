---
id: inference.gpu-inference-oom-triage
title: GPU 推理 OOM 与状态恢复诊断
type: procedure
domain: inference
status: draft
platforms: [nvidia, amd]
source_refs:
  - src.vllm.inference-v0-14
  - src.vllm.rocm-install-doc-v0-14
  - src.pytorch.torch-cuda-memory-usage-2.6
  - src.pytorch.torch-cuda-memory-stats-2.6
  - src.pytorch.cuda-allocator-config-v2.6.0
  - src.pytorch.caching-device-allocator-stats-v2.6.0
  - src.pytorch.hip-notes-2.6
  - src.amd.pytorch-rocm-fork
  - src.nvidia.nvidia-smi-docs-latest-2026-09-30
  - src.amd.amd-smi-docs-10.1.0
updated_at: "2026-10-21"
summary: 按首失败阶段（启动显存检查、权重加载、profiling、KV 容量、warmup/图捕获、prefill、decode、并发运行）定位 NVIDIA/AMD GPU 推理 OOM；区分 CUDA OOM 分配器文本、vLLM KV 容量 ValueError、EngineDeadError 与请求错误四类含义；物理显存/allocated/reserved/碎片/他进程按 CUDA 与 ROCm 各自字段取证；减负载或改配置逐项单因素验证，不以重启或 empty_cache 为通用修复；与昇腾指南和发布恢复流程对照核对残留进程、旧请求与缓存身份。
related_ids:
  - inference.ascend-inference-oom-triage
  - inference.release-and-recovery
  - inference.execution-and-kv-cache
  - inference.model-loading-and-readiness
  - software-stack.gpu-memory-oom-evidence
  - software-stack.amd-rocm-documented-profile
  - reliability.evidence-and-hypotheses
applicability:
  environment_refs: []
  notes: "证据样板为 vLLM v0.14.0 上游（CUDA 与 ROCm 构建线共用同一引擎代码路径）＋PyTorch 2.6 文档/源码锚点（T02-09 已核）＋ROCm 7.14/10.1 文档线。vLLM Ascend/MindIE 不适用本文字段（见昇腾指南与 MindIE 样板）；目标环境的引擎/驱动/固件/模型/dtype 需另行固定。"
verification:
  status: source_checked
  evidence_refs:
    - src.vllm.inference-v0-14
    - src.pytorch.torch-cuda-memory-usage-2.6
    - src.nvidia.nvidia-smi-docs-latest-2026-09-30
  notes: "已复核 vLLM v0.14.0 固定 commit 启动链/引擎死亡/KV 容量锚点（本轮重新下载校验）、troubleshooting 与 conserving_memory 文档、PyTorch 分配器统计语义与 nvidia-smi 口径（T02-09 交付锚点复用）。未启动任何引擎、未构造负载、未复现任何 OOM。逐条主张与定位见 docs/research/batch-28-t07-11-sources.md。"
---

# GPU 推理 OOM 与状态恢复诊断

## 目标与触发条件

本流程处理 NVIDIA（CUDA）与 AMD（ROCm）GPU 上推理服务的 "CUDA out of memory" 类失败与易混淆的相邻错误，目标是先确定**首失败阶段**与**抛出层**，再决定看哪本账。它是[昇腾推理 OOM 诊断指南](ascend-inference-oom-triage.md)的同问题 GPU 对照：问题结构相同（阶段定位→账户分层→单因素验证），字段与文案不同——昇腾指南作为索引引用，其字段（`PYTORCH_NPU_ALLOC_CONF`、NPUWorkspaceAllocator、EL0004，分层依据见[昇腾 NPU 内存与 OOM 证据](../02-software-stack/ascend-memory-oom-evidence.md)）不迁移到本文，本文的 CUDA 分配器语义（[GPU 内存与 OOM 证据](../02-software-stack/gpu-memory-oom-evidence.md)）同样不反向迁移。

先分清四类错误含义（固定 vLLM v0.14.0 语义）：

| 错误形态 | 抛出层 | 含义 | 不是什么 |
|---|---|---|---|
| `CUDA out of memory. Tried to allocate …` | PyTorch caching allocator | 张量分配失败（物理/额度/碎片按[内存证据](../02-software-stack/gpu-memory-oom-evidence.md)分层查） | 不等于整卡物理耗尽；也不含引擎级语义 |
| `ValueError: Free memory on device … on startup is less than desired GPU memory utilization…` / `No available memory for the cache blocks…` | vLLM 启动链（[utils.py L253-273](https://github.com/vllm-project/vllm/blob/b17039bccc17b94a2ea107272ad7bc93508708df/vllm/v1/worker/utils.py#L253-L273)、[kv_cache_utils.py L609-645](https://github.com/vllm-project/vllm/blob/b17039bccc17b94a2ea107272ad7bc93508708df/vllm/v1/core/kv_cache_utils.py#L609-L645)） | 启动期显存预算检查或 KV 容量计算失败（配置类）；在线到达并发不参与 request_memory，但 `max_num_seqs` 等批规模配置影响 dummy/profile 规模、可改变后续自动 KV 预算 | 不是运行期 OOM；调整方向按步骤 2 的首错分支定（两个 KV 子分支方向见步骤 2） |
| `EngineDeadError` | 引擎进程死亡传播（[core.py L927-943](https://github.com/vllm-project/vllm/blob/b17039bccc17b94a2ea107272ad7bc93508708df/vllm/v1/engine/core.py#L927-L943)、[core_client.py L425-428](https://github.com/vllm-project/vllm/blob/b17039bccc17b94a2ea107272ad7bc93508708df/vllm/v1/engine/core_client.py#L425-L428)） | "引擎不可恢复退出"的传播信号；**不单独确定阶段也不证明根因是 OOM**（OOM 依据是更早的分配错误文本） | 不是一种新错误类型，是终态信号 |
| 请求级错误（400/取消/超时） | HTTP/路由层 | 三条不同原因链：**输入验证**——普通 completion/chat 以 `max_model_len` 与输入/输出 token 合计为逐请求边界（[serving_engine.py L1065-1085](https://github.com/vllm-project/vllm/blob/b17039bccc17b94a2ea107272ad7bc93508708df/vllm/entrypoints/openai/serving_engine.py#L1065-L1085)，**不是** `max_num_batched_tokens`——后者是每迭代调度预算，启用 chunked prefill 时超预算 prefill 可分块；**主动取消/断连**（按取消链处理）；**deadline/代理超时**（入口层时序，可能反映容量或引擎问题） | 单个请求的错误**既不单独证明** allocator OOM，**也不单独证明或排除**副本故障——服务健康判断要关联同窗服务/引擎证据（错误率、waiting/running、引擎日志）；按[路由与流控](routing-and-flow-control.md)的边界处理 |

## 适用范围与前置条件

证据样板：vLLM `v0.14.0`（commit `b17039bc…`，CUDA 与 ROCm 构建线）；启动五阶段与 ready 边界的完整定义见[权重加载、引擎 ready 与启动失败诊断](model-loading-and-readiness.md)，KV/抢占语义见[推理执行与 KV cache](execution-and-kv-cache.md)。进入排查前至少固定：引擎版本/commit、模型与 dtype/量化、驱动与 CUDA/ROCm 版本、GPU 型号与卡数、`gpu_memory_utilization`、`max_model_len`、`max_num_seqs`、graph 模式（full/eager、capture sizes）、并行配置（TP/PP/DP）、启动命令与环境变量（`CUDA_VISIBLE_DEVICES`/`PYTORCH_CUDA_ALLOC_CONF`）。ROCm 侧另核对 gfx 架构与构建来源（vLLM ROCm 无预编译 wheel、ROCm 6.3+/torch 2.8+ 边界，[安装文档](https://docs.vllm.ai/en/v0.14.0/getting_started/installation/gpu.html)，T07-06 已核）。

## 需要的证据

| 证据 | 采集范围或定位 | 用途 | 缺失时如何处理 |
|---|---|---|---|
| 报错全文与抛出层 | 分配器文本（含请求字节数）/ 启动链 ValueError / EngineCore 日志（"failed to start" vs "encountered a fatal error"） | 按上表分类 | 只有 "EngineDeadError" 时不能定位阶段，须找 EngineCore 原始日志与栈 |
| 启动期日志 | "Free memory on device … on startup"、profile_run、"Available KV cache memory"、KV cache size、warmup/图捕获段 | 定位启动链失败点（见步骤表） | 只看最终 traceback 会把阶段误判为运行期 |
| 分配器统计 | `memory_stats` 的 allocated/reserved（current+peak）、inactive_split_bytes、requested_bytes、num_ooms；`mem_get_info`（物理视角） | 账户分层（[内存证据](../02-software-stack/gpu-memory-oom-evidence.md)的记录表） | 无统计时保留 unknown，不用 SMI 单值替代 |
| 整卡与他进程口径 | `nvidia-smi`（NVIDIA）/ `amd-smi`（ROCm）按进程显存；同卡他进程清单 | 物理视角与共享设备干扰 | SMI used 与 memory_allocated 的差是正常现象（缓存仍计入 SMI），不据此断泄漏 |
| 负载与时间线 | 并发、输入/输出长度分布、报错前显存爬升 | 区分容量耗尽/突发大分配/缓慢爬升 | 无时间线保留多候选 |
| 配置生效值 | gmu、block/graph 配置、allocator backend 与选项 | 复核运行条件 | — |

## 步骤与判断分支

| 步骤 | 检查或动作 | 预期证据与解释 | 下一步 |
|---|---|---|---|
| 1 | **判断阶段**：启动是否完成（ready 前日志）、最后成功请求时间、EngineCore 原始日志。"failed to start"=启动链内死亡；运行期死亡另有更早错误 | EngineDeadError 只是终态信号 | 启动期→2；运行期→5 |
| 2 | **启动链定位**（固定快照顺序，④内再分两段）：① request_memory 启动检查（空闲显存 < gmu 预算即首错，建议方向=降低 gmu 或减少同卡他进程，[utils.py L262-270](https://github.com/vllm-project/vllm/blob/b17039bccc17b94a2ea107272ad7bc93508708df/vllm/v1/worker/utils.py#L262-L270)）→ ② 权重加载 → ③ profile_run（`max_num_seqs` 等批规模配置影响 dummy/profile 规模，[gpu_model_runner.py L4281-4308](https://github.com/vllm-project/vllm/blob/b17039bccc17b94a2ea107272ad7bc93508708df/vllm/v1/worker/gpu_model_runner.py#L4281-L4308)、L4693-4755——**引擎批规模配置**与在线到达并发是两回事）→ ④ KV 配置：自动预算路径先算容量——两个子分支：`available_memory <= 0` 的错误**仅建议增加 gmu**；单请求所需 KV 大于可用值时**才同时**建议增加 gmu 或降低 `max_model_len`（[kv_cache_utils.py L615-642](https://github.com/vllm-project/vllm/blob/b17039bccc17b94a2ea107272ad7bc93508708df/vllm/v1/core/kv_cache_utils.py#L615-L642)），随后 executor 经 `initialize_from_config`/`compile_or_warm_up_model` RPC 让 worker **实际创建 KV**（[core.py L254-270](https://github.com/vllm-project/vllm/blob/b17039bccc17b94a2ea107272ad7bc93508708df/vllm/v1/engine/core.py#L254-L270)、[abstract.py L110-116](https://github.com/vllm-project/vllm/blob/b17039bccc17b94a2ea107272ad7bc93508708df/vllm/v1/executor/abstract.py#L110-L116)、worker L398-415）——容量检查失败与分配过程 OOM 是两类；显式 `kv_cache_memory_bytes` 分支仍跑 profile 但 KV 预算直接用指定值、不套自动公式（[gpu_worker.py L295-313](https://github.com/vllm-project/vllm/blob/b17039bccc17b94a2ea107272ad7bc93508708df/vllm/v1/worker/gpu_worker.py#L295-L313)，步骤 6 公式仅适用自动路径；手工预算支路的核对对象是指定字节值与实际空闲量——提高 gmu 不扩大指定值）→ ⑤ warmup/图捕获（profiling 本身可执行编译，编译错误不一定落在⑤）。GPU 侧 profile 断言要求**初始空闲 > profile 后空闲**，仅当终值≥初值才失败——以 G＝本进程净增长、R＝他进程净释放计，失败对应 **R ≥ G**（释放净效应足以抵消或超过增长）的部分形态；R<G 时断言通过。他进程**增加**占用不会被该断言识别、通过断言也不证明共享占用不变（[gpu_worker.py L329-339](https://github.com/vllm-project/vllm/blob/b17039bccc17b94a2ea107272ad7bc93508708df/vllm/v1/worker/gpu_worker.py#L329-L339)；独占性另行以同窗进程读数证明） | 失败点在哪一步、错误文本指向哪一段（容量检查 vs 实际分配），哪一段就是首要怀疑对象；调参方向按首错分支定（①降 gmu/减他进程，④升 gmu/降 max_model_len），不承诺任一参数必然修复 | →3/4 |
| 3 | **他进程与共享设备核对**：`nvidia-smi`/`amd-smi` 按进程对账，确认是否独占；CUDA_VISIBLE_DEVICES 是否按预期屏蔽 | 空闲显存不足的常见真相是同卡他进程或 MIG/虚拟实例边界与预期不符 | 独占仍不足→容量核算（步骤 6）；不独占→隔离后复测 |
| 4 | **warmup/图捕获阶段**：官方对 graph replay 附近的 CUDA 错误建议用 `enforce_eager` **隔离具体操作**（[troubleshooting.md L78-81](https://github.com/vllm-project/vllm/blob/b17039bccc17b94a2ea107272ad7bc93508708df/docs/usage/troubleshooting.md#L78-L81)）、对内存压力建议减 `cudagraph_capture_sizes`（[conserving_memory.md](https://github.com/vllm-project/vllm/blob/b17039bccc17b94a2ea107272ad7bc93508708df/docs/configuration/conserving_memory.md)）。**eager 后错误消失只支持"问题与图/编译执行路径有关"的归因**；要下"图捕获容量不足"的结论还须组合证据：首个 OOM 文本与请求字节数、同窗分配记录（current/peak、active/reserved 分阶段）、捕获规模对照。graph 私有池占用计入分配器 aggregate（[内存证据](../02-software-stack/gpu-memory-oom-evidence.md) graph 节）；捕获结束时以 free 差值计图占用且 wrapper 保留 graph 供 replay（[gpu_model_runner.py L4838-4862](https://github.com/vllm-project/vllm/blob/b17039bccc17b94a2ea107272ad7bc93508708df/vllm/v1/worker/gpu_model_runner.py#L4838-L4862)）——保留量持续存在**不必然异常**，也**不保证** capture 后 reserved 必然回落；图类非 OOM 错误转[GPU 算子/图失败诊断](../02-software-stack/gpu-op-graph-failure-triage.md) | capture 窗口峰值与 steady 形态按同窗记录判断，不预设方向 | eager 隔离后与图路径无关→5；与图路径相关→减 capture sizes 单因素验证 |
| 5 | **运行期**：先判断是不是真 OOM——固定语义下 KV 不足是**抢占重算**（文档给出 warning 作为可能观测、长尾表现，不要求每次必有同一条 warning；衔接[长尾诊断](ascend-inference-tail-latency-triage.md)的方法）。真 `CUDA out of memory` 按[内存证据](../02-software-stack/gpu-memory-oom-evidence.md)分层：物理/进程额度（`set_per_process_memory_fraction`）、allocated/reserved/碎片（inactive_split 提示，禁单值确诊）、workspace/graph 用途、他进程。**阶段判别证据**（每案采集）：请求 ID 与输入/已计算 token 数、输出进度（首失败发生在首 prefill、后续 decode 还是并发混合轮）、该轮调度形态（是否混批/是否启用 chunked prefill）、失败栈——同轮混合 batch 拆不开单请求阶段时保留 unknown | 抛出层决定查哪本账；进程额度超额时报错时设备可能仍有空闲 | 结合时间线区分容量耗尽、突发大分配（超 profile 覆盖形状）、缓慢爬升（泄漏候选→恢复对照 F2） |
| 6 | **容量核算**：可用 KV = total×gmu − 峰值（权重+激活+非 torch 项）；profiling 假设共享不变（步骤 2）；跨平台比较带 block_size（Ascend 默认/强制 128，GPU 侧默认不同，见[昇腾指南](ascend-inference-oom-triage.md)步骤 6 的同构核算） | 核算能解释报错剩余量→支持容量支路 | 仍不足保留 unknown |
| 7 | **缓解项单因素验证**（按首失败阶段从官方文档**选取的候选项**，非官方清单全部内容：[conserving_memory.md](https://github.com/vllm-project/vllm/blob/b17039bccc17b94a2ea107272ad7bc93508708df/docs/configuration/conserving_memory.md) 提供 TP/量化/max_model_len/max_num_seqs/图捕获项——注意其 TP 注记是**加载 I/O 时间**属性（每进程读全量权重、建议分片 checkpoint 解耦读取时间），不是每 GPU 必驻全量权重的内存结论；该页无 gmu 条目，gmu 的依据在 request_memory/KV 错误建议（步骤 2 分支方向）与 [optimization.md](https://github.com/vllm-project/vllm/blob/b17039bccc17b94a2ea107272ad7bc93508708df/docs/configuration/optimization.md) 抢占节；多模态负载另有多模态输入数量/尺寸候选，CPU RAM 项不属 GPU 显存处方）——**每次只改一项**，同负载复测并同窗记录 SLO/goodput/错误与质量（判据见[容量与扩缩容](capacity-and-autoscaling.md)的对照） | 单变量消除/复现报错才构成因果；同时改多项的"好了"不可归因 | — |
| 8 | **状态恢复**（查询→终止→清理→再启动闭环，配合[发布与恢复](release-and-recovery.md)；按版本与部署形态执行）：① 保存现场与请求账（错误文本、时间线、在途请求清单）；② 隔离目标流量（路由/端点摘除）；③ 确认终止对象与退出范围（引擎进程、worker、connector/offload 组件、分布式成员）后**发起终止并等待退出**（时限预登记；到期未退或成员退出不完整→**停止清理与重建、维持隔离**、记录影响范围——不进入⑤对象清理、⑥采样对账与⑦再启动）；④ 核对退出与残留（进程、显存按**同条件基线**核对本实例占用——SMI/运行时/框架口径不互减、驱动常驻不等于零）；⑤ 仅清理**已识别且无其他消费者**的本实例对象；⑥ 同步采样对账；⑦ 同身份重启（模型/tokenizer/adapter/量化身份不变），ready 后用固定输入验证与质量检查；⑧ 同负载观察至预登记稳定窗（窗长/基线/分母/超时终态预登记；复用 02 域[内存证据](../02-software-stack/gpu-memory-oom-evidence.md)恢复对照 F2 的窗口方法）。**所有者分立**：仅"已终止所有者的本地活动状态"不自动被继承；外部/offload 缓存与远端 KV 的生存与身份兼容（token/block、LoRA、隔离字段，见[执行与 KV cache](execution-and-kv-cache.md)）按实现核对（unknown 时不在该缓存上重建结论）；旧 frontend 请求、重试 attempt 与已提交输出各自核对终态——不以"重启"证明缓存必冷或取消已完成 | 恢复 ≠ 正确；"服务起来了"只是诊断分支的开始 | 满足恢复判据（见下）后结束 |

**两个不是修复的修复**：`empty_cache()` 只释放分配器未用缓存，已分配张量/workspace/graph 池不受影响（[内存证据](../02-software-stack/gpu-memory-oom-evidence.md)）；"重启后好了"若未定位首失败阶段，只是把问题推迟——两者都不构成完成判据。

## NVIDIA 与 AMD 的取证差异

- **CUDA（NVIDIA）**：分配器统计与 OOM 文案语义按 PyTorch CUDA 文档/源码锚点（T02-09 已核，本文复用）；整卡口径 `nvidia-smi`；驱动常驻与 ECC 份额按[内存证据](../02-software-stack/gpu-memory-oom-evidence.md)记 unknown 的项处理。
- **ROCm（AMD）**：引擎侧默认 worker 与 CUDA 共用 gpu_worker 路径（[rocm.py L443-444](https://github.com/vllm-project/vllm/blob/b17039bccc17b94a2ea107272ad7bc93508708df/vllm/platforms/rocm.py#L443-L444)，有配置前提如 auto——非全部配置分支已核）。观测层按 CUDA/HIP 分列取证字段：
  - **PyTorch 语义（2.6 文档线）**：HIP **复用 `torch.cuda` 接口名**（memory_allocated/reserved、memory_stats/snapshot 等，[hip-notes Memory management 节](https://docs.pytorch.org/docs/2.6/notes/hip.html#memory-management)）；构建判别用 `torch.version.hip`；**hipBLAS workspace 已核边界**：workspace 按 handle＋stream 组合建立、可持续持有（不随常规释放），有专门清理接口与配置项（[hip-notes hipBLAS workspaces 节](https://docs.pytorch.org/docs/2.6/notes/hip.html#hipblas-workspaces)）；MIOpen/AITER workspace 形态未核（unknown）。
  - **可填写字段映射**（列组沿用[内存证据](../02-software-stack/gpu-memory-oom-evidence.md) L102-126 的记录表；三列支持状态分列，填写时未核字段记 unknown、查询失败记失败状态并排除比较，不把未知记成 0）：
    | 记录表列组 | CUDA（已核，PyTorch 2.6 线） | HIP（2.6 文档支持） | 目标 HIP 构建待核 |
    |---|---|---|---|
    | allocated/reserved（current/peak）、memory_stats 细项与计数器、snapshot | `torch.cuda.memory_*` + snapshot（native 统计实现证据） | 张量 allocated/max allocated、allocator reserved/max reserved、memory_stats、memory_snapshot（[hip-notes Memory management](https://docs.pytorch.org/docs/2.6/notes/hip.html#memory-management) 明确列出） | 细项键/统计限制是否与 CUDA 相同（backend 差异） |
    | 采集 API 与 backend | `torch.cuda.memory_*`；实际 backend 记录 `get_allocator_backend()` 查询结果，请求配置（env/启动参数）另列——不能据请求配置推定已生效；查询失败时实际 backend 记 unknown 并排除依赖其语义的统计比较（沿用 02 域 L116 口径） | 同名接口复用（2.6 文档） | 实际 backend/选项集合、fork 差异 |
    | 字节单位与换算、来源工具 | 记录表以字节计；单位换算口径随来源工具记录 | 同左 | CLI 字段与单位按版本核对 |
    | 进程显存 | `usedGpuMemory`（pynvml/NVML 分支的 list_gpu_processes 输出——来源口径为 NVML 而非 SMI） | `vram_mem`（list_gpu_processes ROCm 分支；**字段名按所用 AMD SMI CLI 版本核对**，不直接对齐数值） | amdsmi 版本字段 |
    | 整卡口径 | nvidia-smi | amd-smi（固定 10.1.0 文档线） | 现场字段/版本 |
    | PID/rank/设备身份 | 记录表身份列可直接沿用（进程/设备枚举 API 已核） | 身份列沿用；设备映射 API 的 HIP 行为按 2.6 文档逐项 | 可见设备映射/backend 实际值 |
    | 峰值重置、累计计数器、同步窗口 | reset 语义为 native 统计实现证据（02 域 L126：不推为所有 backend 保证）；同步窗口按 F0/F1/F2 纪律 | 同名 reset 接口存在（2.6 文档列出 memory_stats 等）；backend 语义未核 | reset/backend 语义、窗口适用性 |
    | 字段不支持/查询失败 | 记录失败状态并排除比较（02 域记录方法） | 同左（通用记录约束） | 查询失败时的 CLI 替代路径 |
  - **版本分线**：PyTorch 2.6 文档为**语义参考**；vLLM v0.14.0 ROCm 安装文档要求 torch 2.8+——两者是不同资料样板，不构成已核部署组合；目标实际 torch/HIP 构建的 allocator 选项集合、默认 backend 与 fork 差异待目标版本复核（unknown）。
  - vLLM troubleshooting 未单列 ROCm 专属 OOM 条目——ROCm 侧引擎级特有行为保持 unknown，不用 CUDA 案例外推；平台档案见[AMD ROCm 样板](../02-software-stack/amd-rocm-documented-profile.md)。
- **两平台共同**：启动链顺序、KV 容量 ValueError、EngineDeadError 语义来自上游共享代码，两平台一致（该 commit 口径）。

## 停止条件与完成判据

停止：进程反复死亡、显存持续爬升不止、或输出异常时停止加负载，先保存完整报错与时间线；改配置属服务变更，需授权与回滚记录。

**本轮诊断结束**（任一）：

1. OOM 定位到具体阶段（启动检查/权重加载/profiling/KV 容量检查/KV 实际分配/图捕获/prefill/decode/并发运行）与抛出层（分配器/启动链检查/引擎死亡传播），证据与文案一致；
2. 容量核算定量解释报错时剩余量，或确认配置类错误（如 gmu 预算超空闲）并修正后稳定复现成功；
3. 单因素配置变更稳定消除或复现报错，且同窗质量/SLO/错误记录完整；
4. 证据不足但缺失项已记录，结论保持 `unknown`。

**恢复完成/允许接流**（诊断结束之外的独立判据，须同时满足）：无未解释的实例残留（对同条件基线）、旧请求/缓存身份已核对——**终态不明的旧请求须有受控处置**（隔离、禁用未经验证的缓存复用、控制透明重试边界；仅"记录 unknown"不满足此门）、副本 ready、固定输入质量检查通过、错误率与 SLO 在预登记稳定窗内回到基线。两组判据不互相替代——"定位了阶段"不等于"可以回服"。

"调低 gmu 暂时不报错"不单独满足任一组判据（可能只是推迟耗尽）；与[昇腾指南](ascend-inference-oom-triage.md)的判据结构相同，字段不互迁。

## 来源与验证记录

- [vLLM v0.14.0 固定快照](https://github.com/vllm-project/vllm/tree/b17039bccc17b94a2ea107272ad7bc93508708df)：启动链（request_memory/profile_run/KV 容量）、EngineDead 语义、troubleshooting/conserving_memory 文档、弹性扩缩容 503；锚点本轮重新下载校验。
- [GPU 内存与 OOM 证据](../02-software-stack/gpu-memory-oom-evidence.md)（T02-09 交付）：分配器分层、统计键、empty_cache 边界、恢复对照 F2、SMI 口径差异——PyTorch 2.6 源码/文档锚点。
- [vLLM ROCm 安装文档](https://docs.vllm.ai/en/v0.14.0/getting_started/installation/gpu.html)、[PyTorch HIP notes](https://docs.pytorch.org/docs/2.6/notes/hip.html)：ROCm 构建边界与 HIP 语义（既有登记）。
- [nvidia-smi 手册](https://docs.nvidia.com/deploy/nvidia-smi/index.html)（latest，2026-09-30 观察）、[amd-smi 文档](https://rocm.docs.amd.com/projects/amdsmi/en/docs-10.1.0/index.html)（固定 10.1.0 线，登记 ID src.amd.amd-smi-docs-10.1.0）：整卡与按进程口径。
- 逐条主张与证据定位见[第二十八批 T07-11 来源记录](../../docs/research/batch-28-t07-11-sources.md)。
- 当前验证范围：来源核对；未启动引擎、未构造负载、未复现 OOM。
- 待确认（分列）：① 部署组合——PyTorch 2.6 语义参考与 vLLM ROCm 要求的 torch 2.8+ 未拼成已核组合，目标实际构建待固定；② HIP 构建下 allocator 选项支持集合、默认 backend 与 fork 差异；③ CUDA graph capture 期 workspace/私有池的分配路径（未逐行核）；④ 目标模型真实峰值内存；⑤ 外部/offload 缓存与取消链在具体部署的生存与清理行为；⑥ ROCm 侧引擎级 OOM 特有行为与公开案例形态（本轮未取得）。
