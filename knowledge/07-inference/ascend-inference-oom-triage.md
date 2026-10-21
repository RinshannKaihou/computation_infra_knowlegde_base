---
id: inference.ascend-inference-oom-triage
title: 昇腾推理 OOM 诊断指南
type: procedure
domain: inference
status: draft
platforms: [ascend]
source_refs:
  - src.vllm.inference-v0-14
  - src.ascend.vllm-ascend-v0-14-0rc1
  - src.ascend.torch-npu-v7.2.0-pytorch2.6.0
  - src.vllm-ascend.issue-15920
  - src.vllm-ascend.issue-12692
updated_at: "2026-09-30"
summary: 按启动检查、内存 profiling、warmup/图编译、prefill、decode 与并发阶段区分昇腾推理 OOM；以固定 vLLM/vLLM Ascend 快照为样板，保留分配器分层与未闭环公开报告边界。
related_ids:
  - inference.execution-and-kv-cache
  - inference.latency-metrics
  - software-stack.ascend-memory-oom-evidence
  - inference.ascend-inference-tail-latency-triage
  - reliability.evidence-and-hypotheses
applicability:
  environment_refs: []
  notes: "流程以 vLLM v0.14.0 与 vLLM Ascend v0.14.0rc1 固定快照为证据样板，两者未拼成已验证组合；目标环境的引擎/插件/CANN/torch_npu/模型/dtype/硬件需另行固定。"
verification:
  status: source_checked
  evidence_refs:
    - src.vllm.inference-v0-14
    - src.ascend.vllm-ascend-v0-14-0rc1
    - src.ascend.torch-npu-v7.2.0-pytorch2.6.0
    - src.vllm-ascend.issue-15920
    - src.vllm-ascend.issue-12692
  notes: "已核对两固定快照的启动内存链、KV 容量计算、图编译警告、FAQ 与 release notes，以及两条公开 Issue 的状态与评论（Issue 仅作症状形态记录，不归因）；未启动推理服务、构造负载或复现任何 OOM。"
---

# 昇腾推理 OOM 诊断指南

## 目标与触发条件

本流程处理昇腾 NPU 上推理服务的 “NPU out of memory” 类失败，目标是先确定 OOM 发生在哪个阶段、由哪一层抛出，再决定看什么证据。设备内存的分层机制（物理 HBM、框架 allocated/reserved、workspace 分配器、碎片）见[昇腾 NPU 内存与 OOM 证据](../02-software-stack/ascend-memory-oom-evidence.md)，本文只写引擎与请求层的判断。

注意区分两类看似相似的现场：**启动/加载期失败**（服务起不来）与**运行期失败**（服务已运行一段时间后才报错），两者的证据完全不同；运行期 KV cache 不足在固定 vLLM 语义下通常不是 OOM，而是抢占重算（见步骤 5）。GPU（NVIDIA/AMD）的同问题对照见[GPU 推理 OOM 与状态恢复诊断](gpu-inference-oom-triage.md)——问题结构同构，字段与文案不互迁。

## 适用范围与前置条件

证据样板：上游 vLLM `v0.14.0`（commit `b17039bc…`）与 vLLM Ascend `v0.14.0rc1`（commit `52d4acfa…`）两个固定快照。**两者没有拼成已验证组合**：插件 conf.py 的文档变量指向 vLLM v0.14.1，与本文上游样板不同（见[推理执行与 KV cache](execution-and-kv-cache.md)的 Ascend 边界）。其他引擎（MindIE 等）不适用本文字段。

进入排查前至少固定：引擎与插件版本/commit、模型与 dtype、CANN/torch_npu 版本、硬件型号、`gpu_memory_utilization`、`max_model_len`、graph 模式（aclgraph/eager）、并行配置、启动命令与环境变量（特别是 `PYTORCH_NPU_ALLOC_CONF` 的实际生效值）。

## 需要的证据

| 证据 | 采集范围或定位 | 用途 | 缺失时如何处理 |
|---|---|---|---|
| 报错全文与抛出层 | 完整错误文本：张量分配器 / NPUWorkspaceAllocator / 下发重试路径 / GE 错误码（如 EL0004） | 按[内存分层](../02-software-stack/ascend-memory-oom-evidence.md)区分账户 | 只有 “NPU out of memory” 前缀时不能区分根因 |
| 启动期日志 | "Free memory on device … on startup"、profiling、"Available memory"（NPU 文案）、KV cache size、warmup 日志 | 定位启动链中的失败点 | NPU 侧日志文案与上游不同（见步骤 2），按上游关键字 grep 会漏 |
| 实际生效的内存配置 | 启动日志中的 "Set PYTORCH_NPU_ALLOC_CONF=%s"、`gpu_memory_utilization`、block_size、`set_per_process_memory_fraction` 生效值 | 固定运行条件；区分物理耗尽与进程额度到顶 | 插件会默认追加 expandable_segments（见步骤 3），不能只看用户环境变量 |
| 负载与时间线 | 并发、输入/输出长度分布、报错前的显存爬升曲线 | 区分容量耗尽与突发分配 | 无时间线时保留多种候选 |
| 模型/算子约束 | MLA head 约束、graph capture size 列表 | 识别结构性不支持 | 见步骤 4 的 FAQ 证据 |

## 步骤与判断分支

| 步骤 | 检查或动作 | 运行影响 | 预期证据与解释 | 下一步 |
|---|---|---|---|---|
| 1 | 判断阶段：`EngineDeadError` **不能单独确定阶段**。固定上游代码中，EngineCore 构造失败时记 "EngineCore failed to start."，但已进入 `run_busy_loop()` 后死亡会记 "EngineCore encountered a fatal error." 并发送 `ENGINE_CORE_DEAD`，客户端收到该标记会抛 `EngineDeadError`（[core.py L927–943](https://github.com/vllm-project/vllm/blob/b17039bccc17b94a2ea107272ad7bc93508708df/vllm/v1/engine/core.py#L927-L943)、[core_client.py L425–428](https://github.com/vllm-project/vllm/blob/b17039bccc17b94a2ea107272ad7bc93508708df/vllm/v1/engine/core_client.py#L425-L428)）。它只是“引擎不可恢复退出”的传播信号，也不单独证明根因是 OOM。阶段依据：启动是否完成（启动日志/服务就绪）、最后成功请求时间、EngineCore 原始日志与栈；OOM 依据：更早的分配或容量错误文本 | 只读 | 服务已运行一段时间再死亡必须进入运行分支；阶段无法确定时保持 `unknown` | 启动期进步骤 2；运行期进步骤 5 |
| 2 | 启动链定位：上游固定快照的顺序是 ① request_memory 检查空闲显存（不足即 `ValueError("Free memory on device … on startup is less than desired GPU memory utilization…")`，[utils.py L253–273](https://github.com/vllm-project/vllm/blob/b17039bccc17b94a2ea107272ad7bc93508708df/vllm/v1/worker/utils.py#L253-L273)）→ ② 权重加载 → ③ profile_run 做 memory profiling → ④ 计算可用 KV 内存并生成 KV cache config（不足抛 "No available memory for the cache blocks…" 或建议调整 `gpu_memory_utilization`/`max_model_len`，[kv_cache_utils.py L609–645](https://github.com/vllm-project/vllm/blob/b17039bccc17b94a2ea107272ad7bc93508708df/vllm/v1/core/kv_cache_utils.py#L609-L645)）→ ⑤ warmup 与图捕获。NPU 侧日志是 "Available memory: …, total memory: …"（[worker.py L291–293](https://github.com/vllm-project/vllm-ascend/blob/52d4acfa51fb868823d1070b81cbd2d97e9e4696/vllm_ascend/worker/worker.py#L291-L293)），不是上游的 "Available KV cache memory" | 只读 | 失败点落在哪一步，哪一步就是首要怀疑对象 | 进入步骤 3/4 |
| 3 | 核对实际生效的分配器配置：插件在非 sleep mode 下默认给 `PYTORCH_NPU_ALLOC_CONF` 追加 `expandable_segments:True`（用户已配 expandable_segments/max_split_size_mb/garbage_collection_threshold 则不追加，[platform.py L404–422](https://github.com/vllm-project/vllm-ascend/blob/52d4acfa51fb868823d1070b81cbd2d97e9e4696/vllm_ascend/platform.py#L404-L422)）；v0.14.0rc1 release notes 记录该默认化是为修多模态 OOM（PR #5855，[release_notes.md L34](https://github.com/vllm-project/vllm-ascend/blob/52d4acfa51fb868823d1070b81cbd2d97e9e4696/docs/source/user_guide/release_notes.md#L34)） | 只读 | 实际生效值与运维预期不一致本身是一个发现 | 需要改配置时对照[内存证据条目](../02-software-stack/ascend-memory-oom-evidence.md)的版本边界，不凭 CUDA 经验 |
| 4 | warmup/图编译阶段：full graph 模式捕获过多 batch size 可导致 OOM 或推理 hang（插件警告，[platform.py L317–329](https://github.com/vllm-project/vllm-ascend/blob/52d4acfa51fb868823d1070b81cbd2d97e9e4696/vllm_ascend/platform.py#L317-L329)）；上游建议减 `cudagraph_capture_sizes` 或 `enforce_eager`（[conserving_memory.md L48–76](https://github.com/vllm-project/vllm/blob/b17039bccc17b94a2ea107272ad7bc93508708df/docs/configuration/conserving_memory.md#L48-L76)），`graph.replay()` 附近错误也可用 enforce_eager 隔离（[troubleshooting.md L78–81](https://github.com/vllm-project/vllm/blob/b17039bccc17b94a2ea107272ad7bc93508708df/docs/usage/troubleshooting.md#L78-L81)）。**注意区分**：FAQ 18 的 "insufficient available streams" 是 stream 资源耗尽，不是显存 OOM（[faqs.md L210–224](https://github.com/vllm-project/vllm-ascend/blob/52d4acfa51fb868823d1070b81cbd2d97e9e4696/docs/source/faqs.md#L210-L224)）；FAQ 14 的 MLA + NPU graph 每 KV head query 数须为 32/64/128（[L152–154](https://github.com/vllm-project/vllm-ascend/blob/52d4acfa51fb868823d1070b81cbd2d97e9e4696/docs/source/faqs.md#L152-L154)）是结构性约束 | 改 enforce_eager/capture sizes 属配置变更，需授权与回滚 | 图捕获期 OOM 与运行期 OOM 的处置不同 | 结构性不支持则调整模型/graph 组合；容量问题进步骤 5 |
| 5 | 运行期：先判断是不是真 OOM。固定上游语义下 KV cache 不足会抢占请求重算并打 warning（[optimization.md L8–30](https://github.com/vllm-project/vllm/blob/b17039bccc17b94a2ea107272ad7bc93508708df/docs/configuration/optimization.md#L8-L30)），表现为长尾而非报错（衔接[昇腾推理长尾诊断](ascend-inference-tail-latency-triage.md)）。真出现 "NPU out of memory" 时按抛出层分支：张量分配器文案 → **先查进程额度**（`set_per_process_memory_fraction` 生效值；分配器在额度检查时会产生同一错误码，此时设备可能仍有空闲，见[内存证据](../02-software-stack/ascend-memory-oom-evidence.md)），再查 allocated/reserved/inactive_split 与本次请求大小；NPUWorkspaceAllocator 文案 → workspace 账户（两账户不共享可观测口径）；下发路径含一次"清缓存重试"（机制见[内存证据](../02-software-stack/ascend-memory-oom-evidence.md)） | 只读为主 | 抛出层决定查哪本账 | 结合负载时间线区分容量耗尽、突发大分配与碎片 |
| 6 | 容量核算：可用 KV = total × gpu_memory_utilization − 峰值（权重+激活+非 torch），NPU 实现见 [worker.py L252–293](https://github.com/vllm-project/vllm-ascend/blob/52d4acfa51fb868823d1070b81cbd2d97e9e4696/vllm_ascend/worker/worker.py#L252-L293)；block_size 在 Ascend 默认 128，启用 prefix caching 或 chunked prefill 时强制 128（qwen3_next 除外，实现内有 TODO；[utils.py L1121–1143](https://github.com/vllm-project/vllm-ascend/blob/52d4acfa51fb868823d1070b81cbd2d97e9e4696/vllm_ascend/utils.py#L1121-L1143)）——跨平台比较 KV 容量时必须带上 block_size；profiling 假设同设备其他进程显存不变（上游 [gpu_worker.py L331–339](https://github.com/vllm-project/vllm/blob/b17039bccc17b94a2ea107272ad7bc93508708df/vllm/v1/worker/gpu_worker.py#L331-L339)），共享设备会打破该假设 | 只读 | 核算能解释报错时的剩余量则支持容量支路 | 仍不足时保留未知，不强行归因 |
| 7 | 汇总事实、推断、反证和未知项 | 无 | 结论回链到阶段、抛出层与配置 | 满足完成判据后结束 |

## 公开报告形态（未闭环，不归因）

以下来自固定查询日期的公开 Issue，仅作症状形态与现场参数记录；报告者归因均未获维护者确认，无修复 PR 链：

| 报告 | 阶段/形态 | 现场参数 | 状态与边界 |
|---|---|---|---|
| [#15920](https://github.com/vllm-project/vllm-ascend/issues/15920)（Open） | prefill：~98K prompt 分配 18.00 GiB 失败；81K 时 HBM 99.7%、AICore 0% 静默卡住 | 910B2×8、driver 25.2.1、vLLM/vllm-ascend 0.9.1、CANN 8.1.RC1、Qwen2.5-14B-1M、gmu 0.85、enforce_eager | 报告者先归因强制 chunked prefill，后自行撤回并改称 L² causal mask 不被 profile 形状覆盖；均为单方说法 |
| [#12692](https://github.com/vllm-project/vllm-ascend/issues/12692)（Open） | 运行期：约 37 分钟显存爬升后 workspace 分配器 OOM（216.00 MiB）、torch.OutOfMemoryError、EL0004 | qwen3-5-397b-a17b-w8a8-mtp、v0.20.2rc1、tp16、max-model-len 262144、FULL_DECODE_ONLY、expandable_segments、gmu 0.90 | 评论计数元数据与实取不一致（2 vs 1），已如实记录；碎片化归因未证实 |

这两个形态分别对应步骤 4/5 的分支：突发大分配（profile 未覆盖的形状）与运行期缓慢爬升后 workspace 耗尽。它们不证明任何修复或根因结论。

## 停止条件与恢复安排

- 调整 `gpu_memory_utilization`、`max_model_len`、capture sizes、`PYTORCH_NPU_ALLOC_CONF` 或 graph 模式都属于服务配置变更：需变更授权、记录原值与回滚计划；在生产服务上先离线验证。
- 出现进程反复死亡、显存爬升不止或输出异常时停止加负载，先保存完整报错与日志时间线。
- 不要把 FAQ 的缓解建议当成根因确认；缓解生效后仍需容量核算或对照实验闭环。

## 完成判据

以下任一结果可以结束本轮诊断：

1. OOM 被定位到具体阶段（启动检查/profiling/KV 生成/warmup 图捕获/prefill/decode/并发运行期）与抛出层（张量分配器/workspace/下发路径/引擎检查），证据与日志文案一致；
2. 容量核算（可用 KV、峰值、block_size、并发）能定量解释报错时的剩余量，或结构性约束（如 MLA head 要求）确认不适用；
3. 单变量配置变更稳定消除或复现报错，并记录原值、生效条件与影响范围；
4. 证据不足，但已记录缺失的日志、版本或负载证据，结论保持 `unknown`。

“调低 gpu_memory_utilization 后暂时不报错”不单独满足完成判据：它可能只是推迟了耗尽。

## 来源与验证记录

- [vLLM v0.14.0 固定快照](https://github.com/vllm-project/vllm/tree/b17039bccc17b94a2ea107272ad7bc93508708df)：启动内存链、KV 容量计算、抢占语义、conserving_memory 与 troubleshooting 文档。
- [vLLM Ascend v0.14.0rc1 固定快照](https://github.com/vllm-project/vllm-ascend/tree/52d4acfa51fb868823d1070b81cbd2d97e9e4696)：NPU profiling 与日志文案、分配器默认配置、图模式警告、FAQ 13/14/18、release notes、block_size 规则；注意其中两处未决 OOM TODO 注释（model_runner_v1.py L2073、L2437–2438）表明作者侧定位未完成。
- [昇腾 NPU 内存与 OOM 证据](../02-software-stack/ascend-memory-oom-evidence.md)：分配器分层与 OOM 文案（TorchNPU 固定快照）。
- 公开 Issue：#15920、#12692（登记见 sources/registry.yaml）。
- 逐条主张与证据定位见[第九批推理 OOM 来源记录](../../docs/research/batch-09-inference-oom-sources.md)。
- 当前验证范围：来源核对；未启动推理服务、构造负载或复现 OOM。
- 待确认：aclgraph 每 capture size 的显存占用定量关系；hiascend `PYTORCH_NPU_ALLOC_CONF` 官方页面；NPU 侧 KV 容量实测；目标模型的真实峰值内存。
