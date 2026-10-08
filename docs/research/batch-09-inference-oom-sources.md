# 第九批来源记录：昇腾推理 OOM（R2-04）

研究日期：2026-09-30。目标正文：`knowledge/07-inference/ascend-inference-oom-triage.md`（procedure）。行号按固定 commit 原文件核对（raw URL + grep）；主任务抽查确认 gpu_worker.py 的 profile_run/日志/150MiB 冗余、utils.py 的 request_memory ValueError、vllm-ascend platform.py L404–422 与 utils.py L1121–1143、faqs.md L140–150。未运行任何推理服务。

## 主张—证据表（vLLM v0.14.0，commit b17039bc）

| 主张 | 证据位置 | 类型 | 反证/未知 |
|---|---|---|---|
| gpu_memory_utilization 默认 0.9，语义为当前 vLLM 实例可占用显存比例（per-instance），区间 (0,1] | vllm/config/cache.py L50–57 | 代码+docstring | 引擎自身记账，不感知其他进程后续分配 |
| 启动时 request_memory：requested=ceil(total×gpu_memory_utilization)，空闲不足直接 ValueError("Free memory on device … on startup is less than desired GPU memory utilization …") | vllm/v1/worker/utils.py L253–273（主任务抽查确认） | 代码 | — |
| determine_available_memory：一次 dummy forward（profile_run）做 memory profiling；available = requested − non_kv_cache（权重+峰值激活+非 torch）；日志 "Available KV cache memory: %s GiB" | vllm/v1/worker/gpu_worker.py L283–365（profile_run L320–324，计算 L341–343，日志 L359–362）；分解 vllm/utils/mem_utils.py L174–177、L283–284 | 代码 | profiling 假设同 GPU 其他进程显存不变，否则触发 assert（L331–339） |
| warmup/图捕获分两步：compile/capture size dummy run + kernel_warmup，再 capture_model() 返回 cuda_graph_memory_bytes；注释明确 memory_profiling 不考虑 CUDAGraph 内存，预留 150MiB 冗余 "to avoid OOM"；分解日志为 logger.debug（默认不可见） | gpu_worker.py L417–533（注释 L461–464；redundancy L470–471；debug 日志 L489–509）（主任务抽查确认 L471） | 代码注释 | 无"捕获 N 个 size ≈ 多少显存"的定量关系 |
| KV 初始化总入口 EngineCore._initialize_kv_caches；日志 "init engine (profile, create kv cache, warmup model) took %.2f seconds" | vllm/v1/engine/core.py L222–278 | 代码 | — |
| 启动成功日志 "GPU KV cache size: %s tokens" 与 "Maximum concurrency for %s tokens per request: %.2fx" | vllm/v1/core/kv_cache_utils.py L1305、L1310–1315（注意在 kv_cache_utils.py 而非 core.py） | 代码 | — |
| KV 内存不足启动期 ValueError：可用 ≤0 "No available memory for the cache blocks…"；放不下 max_model_len "…increasing gpu_memory_utilization or decreasing max_model_len…" | vllm/v1/core/kv_cache_utils.py L609–645 | 代码 | — |
| 运行期 KV 不足不抛 OOM 而是抢占重算，warning "…not enough KV cache space…Increase gpu_memory_utilization or tensor_parallel_size…" | docs/configuration/optimization.md L8–30 | 文档 | warning 示例中的 scheduler.py:1057 是旧行号样例 |
| EngineDeadError 传播语义：EngineCore 构造失败（engine_core is None）记 "EngineCore failed to start."；已进入 run_busy_loop 后死亡记 "EngineCore encountered a fatal error." 并 _send_engine_dead()；客户端收到 ENGINE_CORE_DEAD 标记抛 EngineDeadError（"Unrecoverable"）。**这些引证未证明构造失败必然抛同一异常，但运行期死亡同样可产生该异常**，它不能单独确定启动/运行阶段，也不单独证明根因是 OOM（Codex 代审 B09-C01 修订点） | core.py L927–943；core_client.py L425–428；vllm/v1/engine/exceptions.py L9–10 | 代码 | 具体 OOM 文本不统一改写，出现在 EngineCore 栈中 |
| 文档：CUDA graphs "take up extra memory"，可用 cudagraph_capture_sizes 减档或 enforce_eager 关闭；troubleshooting "Out of memory" 节与 "Error near self.graph.replay()" 节（建议 enforce_eager 隔离图内错误） | docs/configuration/conserving_memory.md L48–76；docs/usage/troubleshooting.md L21–23、L78–81 | 文档 | 站点页已实际打开确认 #out-of-memory 锚点 |

## 主张—证据表（vLLM Ascend v0.14.0rc1，commit 52d4acfa）

| 主张 | 证据位置 | 类型 | 反证/未知 |
|---|---|---|---|
| FAQ 13 OOM 建议：--max-model-len 省 KV 初始化显存；--gpu-memory-utilization 默认 0.9 可调低减少碎片风险；PYTORCH_NPU_ALLOC_CONF=expandable_segments:True 缓解碎片 | docs/source/faqs.md L140–150（主任务抽查确认） | 文档（FAQ） | FAQ 链接指向 docs.vllm.ai/en/latest（非版本化）与 hiascend Pytorch/700 页（未核对） |
| 插件在非 sleep mode 默认追加 PYTORCH_NPU_ALLOC_CONF=expandable_segments:True；已含 expandable_segments/max_split_size_mb/garbage_collection_threshold 则不追加（注释：后两者不能与 expandable_segments 同开）；生效打日志 "Set PYTORCH_NPU_ALLOC_CONF=%s" | vllm_ascend/platform.py L404–422（主任务抽查确认） | 代码 | sleep mode（RL）不设置；互斥语义与 TorchNPU 快照一致但此处置信来自注释 |
| v0.14.0rc1 release notes："Fix multi-modal inference OOM issues by setting expandable_segments:True by default"（PR #5855）；MLAPO 默认开启 "will cost more memory"；profiler 环境变量不可用需 --profiler-config | docs/source/user_guide/release_notes.md L34–35、L46 | 文档 | 属该 RC 版本节 |
| NPU 等价 profiling：NPUWorker.determine_available_memory 用 torch.npu.mem_get_info 取总量，profile_run() 后按 allocated_bytes.all.peak + 非 torch 分配估算峰值，available = total×gpu_memory_utilization − peak（下限 0）；日志 "Available memory: …, total memory: …"（与上游 "Available KV cache memory" 文案不同，按上游关键字 grep NPU 日志会漏） | vllm_ascend/worker/worker.py L252–293 | 代码 | — |
| NPU graph（aclgraph）full graph 模式警告："capturing too many batch sizes can lead to OOM (Out of Memory) errors or inference hangs"，建议调低 gpu_memory_utilization 或缩小 capture size；自称 early experimental stage | vllm_ascend/platform.py L317–329 | 代码警告 | — |
| FAQ 18：aclgraph capture 可因 stream 资源耗尽失败（"insufficient available streams"），缓解：减 cudagraph_capture_sizes 或改 full graph；这是 stream 耗尽不是显存 OOM | docs/source/faqs.md L210–224 | 文档（FAQ） | 勿与显存 OOM 混淆 |
| FAQ 14：MLA + NPU graph mode 要求每 KV head 的 query 数为 32/64/128，DeepSeek-V2-Lite（16 heads）不支持 | docs/source/faqs.md L152–154 | 文档（FAQ） | — |
| graph_mode.md：ACLGraph 默认启用；ACLGraph 与 XliteGraph 都失败时回退 eager；全文无显存/warmup 占用说明 | docs/source/user_guide/feature_guide/graph_mode.md L15–20、L68（grep 确认无命中） | 文档 + 负面核对 | — |
| NPU profile_run 前有 eplb_warmup；代码内两处未决 OOM 注释（PP 非首 rank 多一次 all-gather 会 "incorrect memory estimation and potentially causing OOM"；TODO: remove this after the OOM issue is located and fixed） | vllm_ascend/worker/model_runner_v1.py L2162–2185、L2073、L2437–2438 | 代码注释 | TODO 表明作者侧定位未完成 |
| README.md 与 env_vars.md 在该 commit 无 OOM/显存/PYTORCH_NPU_ALLOC_CONF 条目 | grep 无命中 | 负面核对 | — |
| block_size：上游无静态默认（CUDA 仅 ≤32），由 Platform 按平台设置；Ascend 默认 128，启用 prefix caching 或 chunked prefill 时强制 128（qwen3_next 除外，有 TODO） | vllm/config/cache.py L44–48；vllm_ascend/utils.py L1121–1143（platform.py L363 调用）（主任务抽查确认） | 代码 | — |
| cache_dtype="auto" 时被设为模型 dtype 字符串 | vllm_ascend/platform.py L212 | 代码 | — |

## 公开 Issue 候选（已登记）

- src.vllm-ascend.issue-15920（Open）：prefill OOM；两次归因均报告者单方且后者撤回前者；无修复 PR 链。详见 registry notes。
- src.vllm-ascend.issue-12692（Open）：运行期 workspace 分配 OOM（216.00 MiB、EL0004）；comments 元数据 2 与实取 1 不一致；无修复 PR 链；碎片化归因未证实。

两条均只作"症状形态与现场参数记录"，不归因。

## 未解决与抓取失败

- api.github.com 未认证请求触发 rate limit，改用 gh CLI；timeline 无 cross-referenced 事件不排除存在未关联 PR。
- aclgraph 每 capture size 的显存占用无定量来源；hiascend PYTORCH_NPU_ALLOC_CONF 页（Pytorch/700）未打开核对。
- FAQ 13 引用的 vLLM latest 路径为非版本化；固定 commit 对应源文件为 docs/usage/troubleshooting.md。
