---
id: software-stack.gpu-memory-oom-evidence
title: GPU 分配器、保留内存与 OOM 证据
type: concept
domain: software-stack
status: draft
platforms: [generic, nvidia, amd]
source_refs:
  - src.pytorch.cuda-semantics-2.6
  - src.pytorch.torch-cuda-memory-api-2.6
  - src.pytorch.torch-cuda-memory-stats-2.6
  - src.pytorch.torch-cuda-memory-usage-2.6
  - src.pytorch.torch-cuda-memory-source-v2.6.0
  - src.pytorch.cuda-caching-allocator-v2.6.0
  - src.pytorch.cuda-allocator-config-v2.6.0
  - src.pytorch.cublas-handle-pool-v2.6.0
  - src.pytorch.caching-device-allocator-stats-v2.6.0
  - src.pytorch.cudagraph-api-2.6
  - src.pytorch.profiler-2.6
  - src.pytorch.hip-notes-2.6
  - src.nvidia.cuda-12-8-runtime-memory
  - src.nvidia.cuda-12-8-stream-ordered-alloc
  - src.nvidia.cuda-12-8-graph-mgmt
  - src.amd.hip-memory-7.14.0
  - src.amd.hip-stream-ordered-alloc-7.14.0
  - src.amd.pytorch-rocm-fork
updated_at: "2026-10-09"
summary: "补齐 CUDA/PyTorch GPU 内存管理证据：设备总量与可用量、框架 allocated/reserved、缓存分配器双池与碎片证据提示、workspace 与 graph 池的用途分解（经分配器分配，已含在 aggregate 内，不另行相加）、graph 活跃量与保留量的分窗口记录；给出按进程、rank、设备身份和阶段对齐的记录表与固定负载/单变量/恢复三对照；AMD（HIP 7.14.60850）能力与字段独立核对，不与 CUDA 合并阈值或 API。"
related_ids:
  - software-stack.ascend-memory-oom-evidence
  - software-stack.runtime-execution-and-library-loading
  - software-stack.gpu-op-graph-failure-triage
  - software-stack.layers-and-boundaries
applicability:
  environment_refs: []
  notes: "尚无环境档案：CUDA 侧固定 PyTorch v2.6.0（commit 1eba9b3）与 CUDA 12.8.0 归档；AMD 侧固定 docs-7.14.0（ROCm Core SDK 7.14.0，站标 HIP 7.14.60850），docs-10.1.0 样板仅作配套档案引用、内存语义不跨线混用。目标环境的框架/驱动/分配器组合需另行固定。"
verification:
  status: source_checked
  evidence_refs:
    - src.pytorch.cuda-caching-allocator-v2.6.0
    - src.pytorch.torch-cuda-memory-source-v2.6.0
    - src.nvidia.cuda-12-8-stream-ordered-alloc
    - src.pytorch.hip-notes-2.6
  notes: "对照第十七批取证记录（docs/research/batch-17-gpu-memory-sources.md）所列固定版本来源核对；HIP 流序分配器 7.14.0 页执行时须逐条重核（取证以 6.3.3 同路径页过渡对照）；ROCm 构建默认 backend 与 fork/上游 allocator diff 未取得；未在任何 GPU 环境运行代码。"
---

# GPU 分配器、保留内存与 OOM 证据

## 定义与要解决的问题

“CUDA out of memory”是一条分配器错误文本，不直接等于“整卡物理内存被张量用完”。与[昇腾 NPU 内存与 OOM 证据](ascend-memory-oom-evidence.md)的四层模型对应，GPU 路径同样至少分开四层：物理设备内存、框架分配器（allocated/reserved）、算子 workspace 与外部库缓存、graph capture 私有池等用途分类，外加异步执行的时间错位。注意：**用途分类 ≠ 互斥账户**——cuBLAS workspace 经 caching allocator 分配、graph 私有池分配同样进入分配器 aggregate 统计（见“外部库与 graph capture”节），不能无条件作为互斥账户求和。两文术语槽位可对照，但**阈值、API 与选项集不合并**——`PYTORCH_CUDA_ALLOC_CONF` 与 `PYTORCH_NPU_ALLOC_CONF` 名称相似但集合、默认值与互斥关系各自独立。昇腾侧 `NPUWorkspaceAllocator` 的独立性是 Ascend 快照事实，不迁移为 CUDA 结论。

本文 CUDA 侧固定 PyTorch v2.6.0（commit `1eba9b3`）与 CUDA 12.8.0 归档；AMD 侧固定 docs-7.14.0（HIP 7.14.60850）。不构成任何生产环境的内存配置建议。

## 机制与关键关系

### 设备总量与可用量

运行时口径是 [`cudaMemGetInfo(free, total)`](https://docs.nvidia.com/cuda/archive/12.8.0/cuda-runtime-api/group__CUDART__MEMORY.html) / [`hipMemGetInfo(free, total)`](https://rocm.docs.amd.com/projects/HIP/en/docs-7.14.0/reference/hip_runtime_api/modules/memory_management.html)；PyTorch 侧 [`torch.cuda.mem_get_info`](https://docs.pytorch.org/docs/2.6/cuda.html) 即前者的直接封装（[`memory.py`](https://raw.githubusercontent.com/pytorch/pytorch/1eba9b3aa3c43f86f4a2c807ac8e12c4a7767340/torch/cuda/memory.py)）。三者函数名相似但分属三栈文档，不合并为同一 API。`nvidia-smi`/`rocm-smi` 显示口径是另一账户：caching allocator 持有的未用缓存仍计入 SMI，`memory_allocated < SMI used` 为正常现象（[CUDA semantics](https://docs.pytorch.org/docs/2.6/notes/cuda.html#memory-management)；HIP 侧同理见 [HIP semantics](https://docs.pytorch.org/docs/2.6/notes/hip.html#memory-management)）。

### 框架分配器：allocated、reserved 与碎片

`memory_allocated` = `allocated_bytes.all.current`（当前活跃块占用），`memory_reserved` = `reserved_bytes.all.current`（分配器从运行时取得并管理的总量）（[memory.py @1eba9b3](https://raw.githubusercontent.com/pytorch/pytorch/1eba9b3aa3c43f86f4a2c807ac8e12c4a7767340/torch/cuda/memory.py)）。reserved 与 allocated 的差包含空闲缓存块和不可释放碎片；`inactive_split(_bytes)` 是碎片的**证据提示键**（不是单键确诊），辅以 `oversize_*` 与 `requested_bytes`（rounding 开销对照分母）。注意两处实现边界：`backend:cudaMallocAsync` 下部分 stats 恒零（恒零≠无占用）；expandable segment 的切分不走普通 `inactive_split` 累加路径（[`CUDACachingAllocator.cpp` L1410–1423](https://github.com/pytorch/pytorch/blob/1eba9b3aa3c43f86f4a2c807ac8e12c4a7767340/c10/cuda/CUDACachingAllocator.cpp#L1410-L1423) 的 `!block->expandable_segment_` 条件）。

**禁单值断言**：`reserved − allocated` 大不等于碎片确诊，更不等于泄漏。v2.6.0 分配器为 small/large 双池（2MiB/20MiB，最小块 512B），失败走复用→回调→申请→放缓存的重试链；OOM 文案为 `CUDA out of memory. Tried to allocate …`，另有 ≥1EB 请求的防御分支与真实耗尽无关（[`CUDACachingAllocator.cpp` @1eba9b3](https://raw.githubusercontent.com/pytorch/pytorch/1eba9b3aa3c43f86f4a2c807ac8e12c4a7767340/c10/cuda/CUDACachingAllocator.cpp)）。

`PYTORCH_CUDA_ALLOC_CONF` 在 v2.6.0 的选项集以 [`CUDAAllocatorConfig.cpp` 解析](https://github.com/pytorch/pytorch/blob/1eba9b3aa3c43f86f4a2c807ac8e12c4a7767340/c10/cuda/CUDAAllocatorConfig.cpp#L306-L336)为准：backend、max_split_size_mb、roundup_power2_divisions、max_non_split_rounding_mb、garbage_collection_threshold、expandable_segments、**release_lock_on_cudamalloc**、pinned_use_cuda_host_register、pinned_num_register_threads、pinned_use_background_threads；另接受 `release_lock_on_hipmalloc` 与 `pinned_use_hip_host_register` 两种选项名拼写（hipify 别名，是选项名兼容不是新的 HIP 环境变量）。**无 HIP 专用环境变量名**。`backend:cudaMallocAsync`（需 CUDA≥11.4）切换底层为 CUDA 内建异步分配器，此模式下 max_split/gc/roundup 被忽略、部分 stats 恒零（[CUDA semantics](https://docs.pytorch.org/docs/2.6/notes/cuda.html#optimizing-memory-usage-with-pytorch-cuda-alloc-conf) + memory_stats 页 Note）。该 backend 在 ROCm 构建的可用性 unknown。

进程额度是独立 OOM 成因：[`set_per_process_memory_fraction`](https://docs.pytorch.org/docs/2.6/cuda.html)（fraction × total）超额即 OOM——“设备仍有空闲却报 OOM”的第一嫌疑项。Ascend 侧 `set_fraction/allowed` 机制为平行证据，数值语义不合并。

### 外部库与 graph capture：用途分类与分配器可见性

cuBLAS workspace 按 handle+stream 缓存、不随常规释放（须 `_cuda_clearCublasWorkspaces`），大小由 `CUBLAS_WORKSPACE_CONFIG` 控制；cuFFT plan cache 另有 LRU（[CUDA semantics](https://docs.pytorch.org/docs/2.6/notes/cuda.html#cublas-workspaces)）。但 workspace 在用途上独立，在账户上**不独立**：固定实现中 `getNewWorkspace()` 经 `CUDACachingAllocator::get()->allocate(…)` 分配（[`CublasHandlePool.cpp` L166–167](https://github.com/pytorch/pytorch/blob/1eba9b3aa3c43f86f4a2c807ac8e12c4a7767340/aten/src/ATen/cuda/CublasHandlePool.cpp#L166-L167)），即 workspace 占用已含在 allocated/reserved aggregate 内——它是用途分解项，不是可与 allocated 相加的互斥账户。MIOpen/rocBLAS 对应机制待 AMD 侧取证（unknown）。

graph capture 同理：capture 期分配走 graph-private pool，但该 pool 的活跃分配同样进入 aggregate 统计——活跃块插入时 `allocated_bytes/active` 增加（[allocator L1443–1448](https://github.com/pytorch/pytorch/blob/1eba9b3aa3c43f86f4a2c807ac8e12c4a7767340/c10/cuda/CUDACachingAllocator.cpp#L1443-L1448)），graph 私有池块创建时 `total_allocated_memory` 与 `reserved_bytes` 照常增加（[allocator L2775–2784](https://github.com/pytorch/pytorch/blob/1eba9b3aa3c43f86f4a2c807ac8e12c4a7767340/c10/cuda/CUDACachingAllocator.cpp#L2775-L2784)）。`cudaMalloc` 在 capture 中可能 unsafe（`capture_error_mode` 三档）（[CUDA semantics 图节](https://docs.pytorch.org/docs/2.6/notes/cuda.html) + [CUDAGraph](https://docs.pytorch.org/docs/2.6/generated/torch.cuda.CUDAGraph.html) + allocator 源码 `Note [Interaction with CUDA graph capture]`）。运行时侧 mem alloc/free node 语义见 [Graph Management 6.30](https://docs.nvidia.com/cuda/archive/12.8.0/cuda-runtime-api/group__CUDART__GRAPH.html)（取证轮仅确认模块存在，执行引用前逐节核对）。

### 流序分配器（CUDA 侧底层语义）

[`cudaMallocAsync/FreeAsync`](https://docs.nvidia.com/cuda/archive/12.8.0/cuda-runtime-api/group__CUDART__MEMORY__POOLS.html)：分配后须等分配操作完成才可访问；free 语义分三个时点——(a) 主机 API 返回：`cudaFreeAsync` 返回后，再下发访问该内存的 GPU 工作或查询其指针属性即未定义行为（与“stream 尚未执行到 free”无关，返回后不得再提交新访问）；(b) 已下发访问：按 stream/event 建立的流序依赖保证分配与释放之间的合规访问；(c) 设备实际释放。分配侧同流后续工作可依靠流序，跨流须显式建立依赖，不得误读为每次都要先做主机全局同步。capture 期间生成 allocation/free node 归 graph 而非 pool 所有；pool 属性含 `ReleaseThreshold`、三项 Reuse 开关、`ReservedMem/UsedMem` 当前与高水位四水位；能力查询 `cudaDevAttrMemoryPoolsSupported`。

### AMD 侧独立证据

- 释放与同步契约按平台、按分配来源分开：HIP 侧 `hipFree/hipFreeHost` 文档写明隐式调用 `hipDeviceSynchronize`；CUDA 侧 `cudaFree` 按指针来源区分——经 `cudaMallocAsync/cudaMallocFromPoolAsync` 分配的指针**不做隐式同步**（调用者须确保访问结束，推荐用 `cudaFreeAsync` 释放），**其他指针可能隐式同步**（[CUDA 12.8 cudaFree Description](https://docs.nvidia.com/cuda/archive/12.8.0/cuda-runtime-api/group__CUDART__MEMORY.html) 原文 "may perform implicit synchronization"）。文档措辞差异（HIP 写明同步、CUDA 写“可能”+ async 例外）不得读成“CUDA 释放不会同步”；相同函数名或不同措辞不建立跨平台对照（[Memory management（docs-7.14.0）](https://rocm.docs.amd.com/projects/HIP/en/docs-7.14.0/reference/hip_runtime_api/modules/memory_management.html)；`hipPointerGetAttributes` 页 Note 对应 11.0 之前的 CUDA 行为，不可与现行 CUDA 属性 API 对读）。
- 流序分配器：`hipMallocAsync/FreeAsync + hipMemPool*` 全套存在、标 Beta、Linux 已实现（[7.14.0 页](https://rocm.docs.amd.com/projects/HIP/en/docs-7.14.0/reference/hip_runtime_api/modules/memory_management/stream_ordered_memory_allocator.html)，取证以 6.3.3 同路径页过渡对照、7.14.0 逐条重核后引用）。
- ROCm PyTorch 分叉定位：上游已上游化、AMD 另维护 [ROCm/pytorch](https://github.com/ROCm/pytorch) 分叉、HIP 代码由 CUDA 经 HIPIFY 生成；v2.6.0 同一套 `CUDACachingAllocator` 在 ROCm 构建生效（`USE_ROCM` 仅 driver-API 守卫）——“同一套代码编译”≠“同一行为”（无 driver API 平台 expandable_segments 熄火）；fork 与上游在 v2.6.0 时刻的 allocator diff、默认 backend 均 unknown。
- `list_gpu_processes` 在 CUDA 走 pynvml、在 ROCm 走 amdsmi（`memory.py` 双分支实测：`usedGpuMemory` vs `vram_mem`），记录表须保留“来源工具”列，不直接对齐数值。

## 适用边界

- 全部 API 行号、选项集、文案与错误语义仅对 PyTorch v2.6.0（commit `1eba9b3`）与 CUDA 12.8.0 归档负责；HIP 侧仅对 docs-7.14.0 负责（另有说明除外）。
- `torch/cuda/graphs.py @v2.6.0` 全文无 ROCm/HIP 字样：CUDA 图内存结论不套 HIP。
- profiler 分布式唯一表述是 `tensorboard_trace_handler` 的 `worker_name=[hostname]_[pid]`（[profiler](https://docs.pytorch.org/docs/2.6/profiler.html)），无多进程聚合视图——跨进程/跨 rank 对齐须外部拼表。
- 本文没有覆盖 SMI 计数器语义细节、NCCL/集合通信的设备内存占用、以及任何实测数值。

## 常见误解

- **“reserved − allocated 单值能确诊碎片/泄漏”**：不能。`inactive_split_bytes` 只是证据提示（async backend 下部分统计恒零、expandable segment 不走该累加路径）；须 `requested_bytes` + snapshot event 历史互证；`max_split_size_mb` 只是 OOM 文案内置提示。
- **“empty_cache() 能把内存还给别的进程救急”**：它只释放分配器持有的未使用缓存；已分配张量、workspace、graph 私有池都不受影响。
- **“CUDA 的分配器选项照搬到 ROCm/NPU”**：`PYTORCH_CUDA_ALLOC_CONF` 的 backend、roundup、pinned_* 等选项在 TorchNPU 快照中不存在；ROCm 构建是否同名变量生效待实测。
- **“报错栈位置就是耗尽位置”**：异步执行下设备错误在触发调用之后浮现；`cudaFree/hipFree`、event 查询、SMI 采样与 allocator 计数器分属不同步点，须以 snapshot event 历史 + 同步点复测对齐。

## 记录表与对照方法

按进程、rank、设备身份和阶段对齐的记录表（每行一次采样；阶段枚举 `init / warmup / steady / checkpoint / oom-event / recovery`；设备身份三键 `hostname, gpu_uuid_or_bdf, cuda_visible_index↔smi_index 映射`）：

| 列 | 内容 | 来源口径 |
|---|---|---|
| ts_wall / ts_monotonic | wall 时间与单调时钟双记（防 NTP 跳变） | 通用 |
| hostname / pid / rank / local_rank | 进程与分布式身份（profiler 侧 `worker_name`） | profiler-2.6 |
| device_identity | 设备属性 + SMI UUID/BDF + 可见设备变量当时值 | 12.8 / 7.14.0 device 页（执行时补定位） |
| stage / step / iter | 阶段标签与训练步号；OOM 行另记触发算子/分配点栈 | snapshot TraceEntry frames |
| mem_get_info_free / total | 物理视角（当时值） | 主张：运行时口径 |
| allocated / reserved（current + peak） | 张量占用 / allocator 管理总量 | memory_stats 键 |
| inactive_split_bytes / requested_bytes | 碎片证据提示（非单键确诊；async backend 与 expandable segments 有统计限制）/ rounding 对照分母 | memory_stats 键 |
| num_ooms / num_alloc_retries / num_device_alloc-free | 事件计数器（看斜率不看绝对值；peak 为历史最大值，重置语义见对照定义） | memory_stats 键 |
| allocator 设置当时值 | 已证实际 backend（`get_allocator_backend()`）+ 请求配置（`PYTORCH_CUDA_ALLOC_CONF` env 快照）；请求配置未必等于初始化后实际生效值 | memory.py；env（固定 `memory.py` 无 `_get_allocator_settings`，不虚构该 getter） |
| workspace_estimate | 外部库 workspace 用途侧写（经 caching allocator 分配的部分已含在 allocated/reserved 内，此处为用途分解，不另行相加） | cuBLAS/MIOpen 节（AMD 侧待补） |
| graph_active_bytes | graph 私有池活跃分配（与 `allocated_bytes.all.current` 同窗口采样的子集关系；采样窗口须一致） | snapshot 归属 + 同窗口 allocated |
| graph_reserved_high | graph 私有池保留高水位（与 `reserved_bytes` 高水位同口径的子集关系；保留量可含非活跃块，不得说成当前 allocated 的子集） | CUDAGraph pool（高水位窗口） |
| external_procs + smi_used / smi_free | 他进程表（注明 pynvml/amdsmi 分支）与 SMI 整卡口径（与 mem_get_info 并列，不相减） | memory.py 双分支 |

**解释行 A（归因清单，不做算术余量）**：同一设备同一时间并列以下口径，各自保留来源，不相加减——`cudaMemGetInfo`（total/free，物理视角）、`reserved`（分配器管理总量）、`allocated`（活跃块）、`inactive_split_bytes`（碎片提示）、workspace/graph 用途分解（已含在上述 aggregate 内，仅作归因参考）、他进程表与 SMI 整卡口径（与 `mem_get_info` 并列，不相减）。仅将已证明互斥且同设备同时间口径的量用于余量估算；驱动/固件常驻、free 与缓存的划分、无法测量项一律记 unknown。余量本身不是泄漏证据；CUDA/AMD 侧常驻项须逐项取证后才可列入。

**解释行 B（观测不同步）**：同一时刻的 `reserved − allocated` 单值、单次 SMI 读数、报错栈位置三者不得单独作为碎片/泄漏/根因位置的断言。

对照实验（只定义输入与判据，不填结果；全部待执行；统计口径二选一：**口径 A** 下述有序重置，**口径 B** 不重置累计值而比较明确前后增量；一次对照只用一种口径）：**固定负载基线 F0**（窗口 init→warmup→steady：新进程 + 记录 env 与 `get_allocator_backend()` → warmup → 窗口开始 `reset_peak_memory_stats` + `reset_accumulated_memory_stats` 并保存起点读数 → 固定负载 3 次 → 同步 → **再次 reset 前保存终点读数、峰值与计数器** → 取中位；比较只在同阶段基线之间做）。**单变量对照 F1**（每次只改一个分配器选项或开关；切换 backend 时用独立新进程并固定该 backend 配置，指标按各 backend 有意义项分别选取）。**恢复对照 F2**（有序窗口：① 保存失败现场读数（终点/峰值/num_ooms）与存活对象基线（仍存活张量清单、失败引用）；② 明确对象清理/保留（哪些释放、哪些保留作基线）+ `empty_cache` + 同步完成确认 + 采样；③ 窗口开始重置并保存起点；④ 同负载复跑；⑤ 同步并在再次 reset 前保存终点/峰值；⑥ 比较同阶段基线；⑦ 最后才为下一窗口重置。另设干净进程对照）。判据：复跑后 allocated 不回落**且与步骤①对象基线对不上**判泄漏候选（正常保留对象与 warmup 缓存不在此列）；`empty_cache` 后 reserved 回落判缓存行为；额度/容量失败（fraction 或物理上限先到）判配置/容量；口径不支持或证据不足判无法判断。依据：[`memory.py L334–370`](https://github.com/pytorch/pytorch/blob/1eba9b3aa3c43f86f4a2c807ac8e12c4a7767340/torch/cuda/memory.py#L334-L370) 两种 reset 定义、[allocator L1637–1679](https://github.com/pytorch/pytorch/blob/1eba9b3aa3c43f86f4a2c807ac8e12c4a7767340/c10/cuda/CUDACachingAllocator.cpp#L1637-L1679)与 [`CachingDeviceAllocator.h` `Stat::reset_peak` L25–32](https://github.com/pytorch/pytorch/blob/1eba9b3aa3c43f86f4a2c807ac8e12c4a7767340/c10/core/CachingDeviceAllocator.h#L25-L32)（reset 归零 num_ooms 等历史计数；峰值重置到当前值 `peak = current`，起点快照允许非零，窗口 peak 是绝对高水位，不能直接作为新增分配或泄漏量；reset 不释放业务对象、不完成设备工作；native 统计实现，不推为所有 backend 保证）。

## 例子与相关知识

典型误归因链条：训练中途报 `CUDA out of memory`，先读文案区分抛出层（分配器同步抛错 vs 下发路径 vs 1EB 防御分支），再取 `memory_stats` 的 allocated/reserved/inactive_split/num_ooms 并对照 `mem_get_info` 物理视角；若怀疑碎片，取 `_dump_snapshot` 经 memory_viz 看 segment/block 三态与 event 历史；最后才评估异步错位。本文未提供可执行命令。

相关条目：[昇腾 NPU 内存与 OOM 证据](ascend-memory-oom-evidence.md)（四层模型对照）、[驱动初始化、运行时执行同步与库装载](runtime-execution-and-library-loading.md)、[GPU 算子、编译和图执行失败的定向诊断](gpu-op-graph-failure-triage.md)。

## 来源与待确认问题

- PyTorch 2.6（固定文档 + v2.6.0 源码 `1eba9b3`）：[CUDA semantics](https://docs.pytorch.org/docs/2.6/notes/cuda.html)、[torch.cuda 内存 API](https://docs.pytorch.org/docs/2.6/cuda.html)、[memory_stats](https://docs.pytorch.org/docs/2.6/generated/torch.cuda.memory_stats.html)、[Understanding CUDA Memory Usage](https://docs.pytorch.org/docs/2.6/torch_cuda_memory.html)（snapshot/dump）、[CUDAGraph](https://docs.pytorch.org/docs/2.6/generated/torch.cuda.CUDAGraph.html)、[profiler](https://docs.pytorch.org/docs/2.6/profiler.html)、[HIP semantics](https://docs.pytorch.org/docs/2.6/notes/hip.html)；源码 [memory.py](https://raw.githubusercontent.com/pytorch/pytorch/1eba9b3aa3c43f86f4a2c807ac8e12c4a7767340/torch/cuda/memory.py)（无 `_get_allocator_settings`；以 `get_allocator_backend()` 取已证实际 backend）、[CUDACachingAllocator.cpp](https://raw.githubusercontent.com/pytorch/pytorch/1eba9b3aa3c43f86f4a2c807ac8e12c4a7767340/c10/cuda/CUDACachingAllocator.cpp)（活跃统计 L1443–1448、expandable 条件 L1410–1423、graph 池 L2775–2784）、[CUDAAllocatorConfig.cpp](https://github.com/pytorch/pytorch/blob/1eba9b3aa3c43f86f4a2c807ac8e12c4a7767340/c10/cuda/CUDAAllocatorConfig.cpp#L306-L336)（选项解析，含 release_lock_on_cudamalloc 及 hip 拼写别名）、[CublasHandlePool.cpp](https://github.com/pytorch/pytorch/blob/1eba9b3aa3c43f86f4a2c807ac8e12c4a7767340/aten/src/ATen/cuda/CublasHandlePool.cpp#L166-L167)（workspace 经 caching allocator 分配）。
- NVIDIA（12.8.0 归档）：[Memory Management 6.11](https://docs.nvidia.com/cuda/archive/12.8.0/cuda-runtime-api/group__CUDART__MEMORY.html)（cudaFree 按分配来源区分隐式同步：async 来源不做、其他可能做）、[Stream Ordered Allocator 6.13](https://docs.nvidia.com/cuda/archive/12.8.0/cuda-runtime-api/group__CUDART__MEMORY__POOLS.html)（三时点：返回后禁新访问、流序依赖、实际释放）、[Graph Management 6.30](https://docs.nvidia.com/cuda/archive/12.8.0/cuda-runtime-api/group__CUDART__GRAPH.html)。
- AMD（docs-7.14.0）：[HIP Memory management](https://rocm.docs.amd.com/projects/HIP/en/docs-7.14.0/reference/hip_runtime_api/modules/memory_management.html)、[Stream ordered allocator](https://rocm.docs.amd.com/projects/HIP/en/docs-7.14.0/reference/hip_runtime_api/modules/memory_management/stream_ordered_memory_allocator.html)、[ROCm/pytorch fork](https://github.com/ROCm/pytorch)。
- 逐条主张与证据定位见[第十七批 GPU 内存来源记录](../../docs/research/batch-17-gpu-memory-sources.md)。
- 待确认：HIP 7.14.0 流序分配器逐条重核；CUDA Graph Management 6.30 逐节核对；MIOpen/rocBLAS workspace 对应机制；ROCm 构建默认 backend 与 fork/上游 allocator diff；HIP 错误码（hipErrorOutOfMemory 等）定位；驱动/固件常驻占用逐项取证；任何实测数值。
- 修订记录：2026-10-09 按初审 B17-C01/C03/C04/C05/C11 修订（见 [batch-17-review-fixes.md](../../docs/research/batch-17-review-fixes.md)），定向复核待执行。
