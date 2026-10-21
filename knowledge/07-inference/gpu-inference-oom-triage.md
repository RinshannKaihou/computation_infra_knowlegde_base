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

本流程处理 NVIDIA（CUDA）与 AMD（ROCm）GPU 上推理服务的 "CUDA out of memory" 类失败与易混淆的相邻错误，目标是先确定**首失败阶段**与**抛出层**，再决定看哪本账。它是[昇腾推理 OOM 诊断指南](ascend-inference-oom-triage.md)的同问题 GPU 对照：问题结构相同（阶段定位→账户分层→单因素验证），字段与文案不同——昇腾指南作为索引引用，其字段（`PYTORCH_NPU_ALLOC_CONF`、NPUWorkspaceAllocator、EL0004）不迁移到本文。

先分清四类错误含义（固定 vLLM v0.14.0 语义）：

| 错误形态 | 抛出层 | 含义 | 不是什么 |
|---|---|---|---|
| `CUDA out of memory. Tried to allocate …` | PyTorch caching allocator | 张量分配失败（物理/额度/碎片按[内存证据](../02-software-stack/gpu-memory-oom-evidence.md)分层查） | 不等于整卡物理耗尽；也不含引擎级语义 |
| `ValueError: Free memory on device … on startup is less than desired GPU memory utilization…` / `No available memory for the cache blocks…` | vLLM 启动链（[utils.py L253-273](https://github.com/vllm-project/vllm/blob/b17039bccc17b94a2ea107272ad7bc93508708df/vllm/v1/worker/utils.py#L253-L273)、[kv_cache_utils.py L609-645](https://github.com/vllm-project/vllm/blob/b17039bccc17b94a2ea107272ad7bc93508708df/vllm/v1/core/kv_cache_utils.py#L609-L645)） | 启动期显存预算检查或 KV 容量计算失败（配置类） | 不是运行期 OOM；改并发救不了它 |
| `EngineDeadError` | 引擎进程死亡传播（[core.py L927-943](https://github.com/vllm-project/vllm/blob/b17039bccc17b94a2ea107272ad7bc93508708df/vllm/v1/engine/core.py#L927-L943)、[core_client.py L425-428](https://github.com/vllm-project/vllm/blob/b17039bccc17b94a2ea107272ad7bc93508708df/vllm/v1/engine/core_client.py#L425-L428)） | "引擎不可恢复退出"的传播信号；**不单独确定阶段也不证明根因是 OOM**（OOM 依据是更早的分配错误文本） | 不是一种新错误类型，是终态信号 |
| 请求级错误（400/取消/超时） | HTTP/路由层 | 单请求失败（超长输入被 `max_num_batched_tokens` 拒绝、断连取消等） | 不是服务故障；按[路由与流控](routing-and-flow-control.md)的边界处理 |

## 适用范围与前置条件

证据样板：vLLM `v0.14.0`（commit `b17039bc…`，CUDA 与 ROCm 构建线）。进入排查前至少固定：引擎版本/commit、模型与 dtype/量化、驱动与 CUDA/ROCm 版本、GPU 型号与卡数、`gpu_memory_utilization`、`max_model_len`、`max_num_seqs`、graph 模式（full/eager、capture sizes）、并行配置（TP/PP/DP）、启动命令与环境变量（`CUDA_VISIBLE_DEVICES`/`PYTORCH_CUDA_ALLOC_CONF`）。ROCm 侧另核对 gfx 架构与构建来源（vLLM ROCm 无预编译 wheel、ROCm 6.3+/torch 2.8+ 边界，[安装文档](https://docs.vllm.ai/en/v0.14.0/getting_started/installation/gpu.html)，T07-06 已核）。

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
| 2 | **启动链定位**（固定快照顺序）：① request_memory 启动检查（空闲显存 < gmu 预算即首错）→ ② 权重加载 → ③ profile_run → ④ KV 容量计算（不足 ValueError 并建议调 gmu/max_model_len）→ ⑤ warmup/图捕获。GPU 侧 profile 假设同设备其他进程显存不变——共享设备上他进程变动会触发显式断言错误（"other processes sharing the same container release GPU memory…"，[gpu_worker.py L331-339](https://github.com/vllm-project/vllm/blob/b17039bccc17b94a2ea107272ad7bc93508708df/vllm/v1/worker/gpu_worker.py#L331-L339)） | 失败点在哪一步，哪一步就是首要怀疑对象；④ 是配置错误不是运行 OOM | →3/4 |
| 3 | **他进程与共享设备核对**：`nvidia-smi`/`amd-smi` 按进程对账，确认是否独占；CUDA_VISIBLE_DEVICES 是否按预期屏蔽 | 空闲显存不足的常见真相是同卡他进程或 MIG/虚拟实例边界与预期不符 | 独占仍不足→容量核算（步骤 6）；不独占→隔离后复测 |
| 4 | **warmup/图捕获阶段**：图捕获期 OOM 与运行期 OOM 处置不同——官方建议减 `cudagraph_capture_sizes` 或 `enforce_eager` 隔离（[troubleshooting.md L78-81](https://github.com/vllm-project/vllm/blob/b17039bccc17b94a2ea107272ad7bc93508708df/docs/usage/troubleshooting.md#L78-L81)、[conserving_memory.md](https://github.com/vllm-project/vllm/blob/b17039bccc17b94a2ea107272ad7bc93508708df/docs/configuration/conserving_memory.md)）。graph 私有池占用计入分配器 aggregate（[内存证据](../02-software-stack/gpu-memory-oom-evidence.md) graph 节），是用途分解不是独立账户 | capture 窗口的 reserved 峰值高、steady 回落为正常形态 | enforce_eager 后消失→图捕获容量问题；仍失败→5 |
| 5 | **运行期**：先判断是不是真 OOM——固定语义下 KV 不足是**抢占重算**（warning、长尾），不是报错（衔接[长尾诊断](ascend-inference-tail-latency-triage.md)的方法）。真 `CUDA out of memory` 按[内存证据](../02-software-stack/gpu-memory-oom-evidence.md)分层：物理/进程额度（`set_per_process_memory_fraction`）、allocated/reserved/碎片（inactive_split 提示，禁单值确诊）、workspace/graph 用途、他进程 | 抛出层决定查哪本账；进程额度超额时报错时设备可能仍有空闲 | 结合时间线区分容量耗尽、突发大分配（超 profile 覆盖形状）、缓慢爬升（泄漏候选→恢复对照 F2） |
| 6 | **容量核算**：可用 KV = total×gmu − 峰值（权重+激活+非 torch 项）；profiling 假设共享不变（步骤 2）；跨平台比较带 block_size（Ascend 默认/强制 128，GPU 侧默认不同，见[昇腾指南](ascend-inference-oom-triage.md)步骤 6 的同构核算） | 核算能解释报错剩余量→支持容量支路 | 仍不足保留 unknown |
| 7 | **缓解项单因素验证**（官方清单，[conserving_memory.md](https://github.com/vllm-project/vllm/blob/b17039bccc17b94a2ea107272ad7bc93508708df/docs/configuration/conserving_memory.md)）：TP 分摊（注意每进程读全量权重、建议分片 checkpoint）、量化、降 `max_model_len`/`max_num_seqs`、调 gmu——**每次只改一项**，同负载复测并同窗记录 SLO/goodput/错误与质量（判据见[容量与扩缩容](capacity-and-autoscaling.md)的对照） | 单变量消除/复现报错才构成因果；同时改多项的"好了"不可归因 | — |
| 8 | **状态恢复核对**（配合[发布与恢复](release-and-recovery.md)）：进程死亡后 KV/请求/缓存身份随进程消失；重启=重走启动链（冷 cache）。恢复前核对：残留进程（`ps`/节点级）、显存账目归零（SMI 对账）、旧请求不复活（取消链已清，见[路由与流控](routing-and-flow-control.md)）、ready 后质量抽查与错误率稳定窗 | 恢复 ≠ 正确；"服务起来了"不关闭本轮 | 满足完成判据后结束 |

**两个不是修复的修复**：`empty_cache()` 只释放分配器未用缓存，已分配张量/workspace/graph 池不受影响（[内存证据](../02-software-stack/gpu-memory-oom-evidence.md)）；"重启后好了"若未定位首失败阶段，只是把问题推迟——两者都不构成完成判据。

## NVIDIA 与 AMD 的取证差异

- **CUDA（NVIDIA）**：分配器统计与 OOM 文案语义按 PyTorch CUDA 文档/源码锚点（T02-09 已核，本文复用）；整卡口径 `nvidia-smi`；驱动常驻与 ECC 份额按[内存证据](../02-software-stack/gpu-memory-oom-evidence.md)记 unknown 的项处理。
- **ROCm（AMD）**：引擎代码路径与 CUDA 共用（vLLM 上游同一 scheduler/worker 实现，构建线不同），但**观测字段换套**：`amd-smi` 显存口径、`rocm-smi`/`hipMemGetInfo`、PyTorch HIP 语义差异（[hip-notes](https://docs.pytorch.org/docs/2.6/notes/hip.html)）；分配器为同一 caching allocator 的 HIP 实现，`PYTORCH_CUDA_ALLOC_CONF` 选项在 HIP 构建的支持集合不逐项等同（unknown，未逐项核）。vLLM troubleshooting 未单列 ROCm 专属 OOM 条目——ROCm 侧的引擎级特有行为（如 AITER/MIOpen workspace 形态差异）本轮无证据，保持 unknown，不用 CUDA 案例外推。
- **两平台共同**：启动链顺序、KV 容量 ValueError、EngineDeadError 语义来自上游共享代码，两平台一致（该 commit 口径）。

## 停止条件与完成判据

停止：进程反复死亡、显存持续爬升不止、或输出异常时停止加负载，先保存完整报错与时间线；改配置属服务变更，需授权与回滚记录。

完成判据（任一）：

1. OOM 定位到具体阶段（启动检查/权重加载/profiling/KV 容量/图捕获/prefill/decode/并发运行）与抛出层（分配器/启动链检查/引擎死亡传播），证据与文案一致；
2. 容量核算定量解释报错时剩余量，或确认配置类错误（如 gmu 预算超空闲）并修正后稳定复现成功；
3. 单因素配置变更稳定消除或复现报错，且同窗质量/SLO/错误记录完整；
4. 证据不足但缺失项已记录，结论保持 `unknown`。

"调低 gmu 暂时不报错"不单独满足判据（可能只是推迟耗尽）；与[昇腾指南](ascend-inference-oom-triage.md)的判据结构相同，字段不互迁。

## 来源与验证记录

- [vLLM v0.14.0 固定快照](https://github.com/vllm-project/vllm/tree/b17039bccc17b94a2ea107272ad7bc93508708df)：启动链（request_memory/profile_run/KV 容量）、EngineDead 语义、troubleshooting/conserving_memory 文档、弹性扩缩容 503；锚点本轮重新下载校验。
- [GPU 内存与 OOM 证据](../02-software-stack/gpu-memory-oom-evidence.md)（T02-09 交付）：分配器分层、统计键、empty_cache 边界、恢复对照 F2、SMI 口径差异——PyTorch 2.6 源码/文档锚点。
- [vLLM ROCm 安装文档](https://docs.vllm.ai/en/v0.14.0/getting_started/installation/gpu.html)、[PyTorch HIP notes](https://docs.pytorch.org/docs/2.6/notes/hip.html)：ROCm 构建边界与 HIP 语义（既有登记）。
- [nvidia-smi 手册](https://docs.nvidia.com/deploy/nvidia-smi/index.html)、[amd-smi 文档](https://rocm.docs.amd.com/projects/amd-smi/en/latest/)（既有登记）：整卡与按进程口径。
- 逐条主张与证据定位见[第二十八批 T07-11 来源记录](../../docs/research/batch-28-t07-11-sources.md)。
- 当前验证范围：来源核对；未启动引擎、未构造负载、未复现 OOM。
- 待确认：ROCm 侧引擎级 OOM 特有行为与公开案例形态（本轮未取得）；HIP 构建下 allocator 选项支持集合；目标模型真实峰值内存。
