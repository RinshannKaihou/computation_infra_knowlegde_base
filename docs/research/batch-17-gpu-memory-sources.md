# 第十七批 T02-09 GPU 内存与 OOM 来源记录

任务：T02-09 GPU 分配器、保留内存与 OOM 证据（`gpu-memory-oom-evidence.md`，concept）。取证日期 2026-10-09。版本线：CUDA 侧 `PyTorch v2.6.0（1eba9b3）+ CUDA 12.8.0 归档`；AMD 侧 `docs-7.14.0（ROCm Core SDK 7.14.0，站标 HIP 7.14.60850）`；docs-10.1.0 样板仅作配套档案引用，内存语义不跨线混用。

## 候选来源（10 项新登记 + 2 复核复用）

| proposed-id | 精确 URL | 核对要点 |
|---|---|---|
| （复用核对）src.pytorch.cuda-semantics-2.6 | docs/2.6/notes/cuda.html | memory-management（SMI 口径）、ALLOC_CONF 选项集、asynchronous-execution、cublas-workspaces、Graph memory management |
| src.pytorch.torch-cuda-memory-api-2.6 | docs/2.6/cuda.html（torch.cuda.html 404） | Memory management 全表 |
| src.pytorch.torch-cuda-memory-stats-2.6 | docs/2.6/generated/torch.cuda.memory_stats.html | 键三维度、计数器、oversize/requested_bytes、cudaMallocAsync 下 Note |
| src.pytorch.torch-cuda-memory-usage-2.6 | docs/2.6/torch_cuda_memory.html | snapshot/dump 三件套 schema、两视图 |
| src.pytorch.torch-cuda-memory-source-v2.6.0 | raw torch/cuda/memory.py @1eba9b3 | mem_get_info、allocated/reserved 定义、fraction、list_gpu_processes 双路径（pynvml/amdsmi） |
| src.pytorch.cuda-caching-allocator-v2.6.0 | raw c10/cuda/CUDACachingAllocator.cpp @1eba9b3（4056 行） | 双池、重试链、OOM 文案、1EB 分支、graph capture Note、只读 PYTORCH_CUDA_ALLOC_CONF、USE_ROCM 仅 2 处 |
| （复用核对）src.pytorch.profiler-2.6 | docs/2.6/profiler.html | profile_memory、export_memory_timeline、worker_name 唯一分布式表述 |
| src.pytorch.cudagraph-api-2.6 | docs/2.6/generated/torch.cuda.CUDAGraph.html | capture_begin 三档、pool/replay/reset、beta；graphs.py 无 HIP 字样 |
| src.nvidia.cuda-12-8-runtime-memory | 12.8 group__CUDART__MEMORY.html | cudaMemGetInfo、pinned、async errors 注记 |
| src.nvidia.cuda-12-8-stream-ordered-alloc | 12.8 group__CUDART__MEMORY__POOLS.html | 流序语义、capture node 归属、pool 属性四水位、能力查询（集成者实开全文复核） |
| src.nvidia.cuda-12-8-graph-mgmt | 12.8 group__CUDART__GRAPH.html | 仅确认模块存在 + mem node 结构清单，未逐节读 |
| src.amd.hip-memory-7.14.0 | docs-7.14.0 memory_management.html | hipFree 隐式同步、hipMemGetInfo 签名、pointer 属性 Note（11.0 前 CUDA 行为） |
| src.amd.hip-stream-ordered-alloc-7.14.0 | docs-7.14.0 …/stream_ordered_memory_allocator.html | 6.3.3 同页过渡对照（Beta/Linux 已实现）；7.14.0 页 HTTP 200，执行时逐条重核 |
| src.amd.pytorch-rocm-fork | github.com/ROCm/pytorch | fork 存在性；上游化/HIPIFY 见 7.2.3 兼容页 |

## 主张—来源定位表

| 主张 | 来源 | 定位 | 边界 |
|---|---|---|---|
| mem_get_info 三栈口径 | memory-source + 12.8 MEMORY + hip-memory | 各函数定义/签名 | 分属三栈，不合并为同一 API |
| SMI 显示占用≠张量占用 | cuda-semantics + memory.py docstring | Memory management 段 | 仅 CUDA 官方陈述；他侧另取证 |
| allocated/reserved 定义；差值含缓存与碎片 | memory-source + memory-stats | 两函数体；键维度说明 | 禁单值断言 |
| 碎片官方键 inactive_split + oversize + requested_bytes | memory-stats + allocator 源码 | 调优段；should_split 逻辑 | Ascend 侧键名同代码各属 |
| ALLOC_CONF 完整选项集；无 HIP 专用变量 | allocator 源码 + cuda-semantics | Config.h parse；文档选项节 | 与 NPU 五选项不合并 |
| backend:cudaMallocAsync 切换底层；部分 stats 恒零 | cuda-semantics + memory-stats Note + 12.8 POOLS | backend 条；底层语义 | ROCm 可用性 unknown |
| OOM 形态 OutOfMemoryError + num_ooms + snapshot oom entry | allocator 源码 + memory-usage | malloc 失败路径；TraceEntry schema | 与 Ascend 三文案对照，同前缀不同层 |
| 进程额度独立 OOM 成因 | memory-source | set_per_process_memory_fraction | Ascend allowed 平行证据 |
| snapshot/dump 证据链 | memory-usage + memory-source | 全页 + snapshot 实现 | 与 NPU pickle 机制不互认 |
| 外部库独立记账 | cuda-semantics | cublas-workspaces、cuFFT 两节 | MIOpen/rocBLAS 待补 |
| graph capture 私有池 | cuda-semantics + cudagraph-api + allocator Note | 图节；capture_begin；源码注释 | CUDA 结论不套 HIP |
| HIP 流序分配器对位但独立 | hip-stream-ordered + hip-memory | 分配器页；hipFree 条 | Beta + 平台差异写入正文边界 |
| ROCm allocator 分叉定位 | rocm-fork + allocator 源码 + 7.2.3 兼容页 | fork 页；USE_ROCM 守卫 | 同代码编译≠同行为；diff unknown |
| 跨进程对齐须外部拼表 | profiler + memory-source | worker_name；双分支函数 | 保留来源工具列 |

## 记录表与对照草案

记录表：ts 双时钟、hostname/pid/rank、device_identity 三键、stage/step、mem_get_info、allocated/reserved peak、inactive_split/requested_bytes、计数器斜率、allocator 设置当时值、workspace 侧写、graph 池水位、他进程表、SMI 并列。解释行 A（不可归属显存余量≠泄漏证据）、B（单值/SMI/栈位三者不得单独断言）。对照：F0 固定负载基线（3 次中位）、F1 单变量、F2 恢复对照。详见正文。

## unknown 清单

HIP 7.14.0 分配器逐条重核；Graph Management 6.30 逐节核对；MIOpen/rocBLAS workspace；ROCm 默认 backend 与 fork diff；hipErrorOutOfMemory 定位；TORCH_BLAS_PREFER_HIPBLASLT 适用版本；任何实测数值。

## 修订记录（2026-10-09，按初审 B17-C01/C03/C04/C05/C11）

- C01：用途分类 vs 分配器可见性。复核 CublasHandlePool.cpp L166–167（workspace 经 caching allocator 分配）、allocator L1443–1448（活跃块计入 allocated）与 L2775–2784（graph 池块计入 total_allocated_memory/reserved）；正文余量公式改写为归因清单（并列不相加），仅互斥同口径量可估算；Ascend 独立 workspace 不迁移为 CUDA 事实。
- C03：选项集补 release_lock_on_cudamalloc 及 release_lock_on_hipmalloc/pinned_use_hip_host_register 拼写别名（CUDAAllocatorConfig.cpp L306–336，非新环境变量）；记录表移除虚构 getter，改用 get_allocator_backend()（已证实际 backend）+ env 快照（请求配置）；Config.h 定位改为 CUDAAllocatorConfig.cpp。
- C04：cudaFree 按分配来源区分（async 来源不做隐式同步、其他可能做；12.8 MEMORY 页 Description 原文复核），HIP 侧保留显式同步；不作跨平台对照。
- C05：流序语义补三时点（返回后禁新访问、流序依赖、实际释放）与跨流依赖说明。
- C11：F0–F2 补初始化/恢复/存活对象/同步/统计窗口定义、跨 backend 独立进程与分指标、四判据；inactive_split 改证据提示并注 async/expandable 统计限制。定向复核待执行。

## 第二轮复核修订（2026-10-09，按 B17-C01/C03/C11 剩余条件）

- C01：摘要改用途/可见性口径；记录表 graph 行拆分为活跃量（同窗口 allocated 子集）与保留高水位（reserved 高水位子集，保留可含非活跃块）；登记 notes 同步三处行号证据。
- C03：登记纠正 get_allocator_backend 查询 active backend（memory.py L925–934），env 单列请求配置；两者都不代表全部选项生效值。
- C11：F0–F2 改写为有序窗口（保存现场→清理/保留+同步→重置存起点→负载→同步并 reset 前存终点→比较同阶段基线→再重置）与口径二选一；依据 memory.py L334–370 与 allocator L1637–1679（本次复核）；干净进程对照保留。

## 第三轮修订（2026-10-09，按第二次复核 C11 剩余条件）

- 峰值语义更正：Stat::reset_peak 原文 peak = current（CachingDeviceAllocator.h L25–32，本次 raw 实测），累计量/事件计数归零；起点快照允许非零，窗口 peak 为绝对高水位。登记沿用复核补登 src.pytorch.caching-device-allocator-stats-v2.6.0，正文 source_refs 追加该 ID。
