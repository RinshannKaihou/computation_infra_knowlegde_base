# 第八批来源记录：训练数据加载饥饿观测（R2-02）

研究日期：2026-09-30。目标正文：`knowledge/04-data-storage/data-starvation-triage.md`（procedure）。版本统一为 PyTorch 2.6：文档页 `docs/2.6/*`；源码固定 commit `1eba9b3aa3c43f86f4a2c807ac8e12c4a7767340`（tag v2.6.0）。小节锚点经页面原始 HTML `id=` 核实；源码行号按原文件核对。主任务抽查确认 dataloader.py L1262–1266（worker 崩溃错误）与 L1234–1236（prefetch 预填）。未运行任何代码。

## 主张—证据表

### DataLoader 参数语义（https://docs.pytorch.org/docs/2.6/data.html）

| 主张 | 证据位置 | 证据类型 | 反证/未知 |
|---|---|---|---|
| num_workers=0（默认）在主进程加载；可能阻塞计算，但错误栈更可读、适合调试 | #torch.utils.data.DataLoader 参数表；#single-process-data-loading-default | 官方文档 | 无 |
| num_workers>0 每次创建迭代器时创建相应数量 worker；dataset/collate_fn/worker_init_fn 传入各 worker；worker 在迭代结束或迭代器 GC 时关闭 | #multi-process-data-loading | 官方文档 | 无 |
| prefetch_factor：每 worker 预取 batch 数；num_workers=0 时默认 None，>0 时默认 2；仅多进程可设。源码佐证：num_workers==0 且显式给 prefetch_factor 抛 ValueError；迭代器 reset 末尾按 prefetch_factor*num_workers 预填索引 | 参数表；dataloader.py#L269-L277、#L1234-L1236、#L1087 | 官方文档 + 固定源码 | 无 |
| persistent_workers=True：一轮消费后不关闭 worker，worker 内 dataset 实例跨 epoch 存活；要求 num_workers>0。源码佐证：迭代器在 DataLoader 生命周期内只创建一次（L478–491）；persistent_workers 且 num_workers==0 抛 ValueError（L279–280） | 参数表；dataloader.py#L478-L491、#L279-L280 | 官方文档 + 固定源码 | 文档未承诺 dataset 内部状态跨 epoch 的具体保留语义 |
| timeout：若为正，为「从 worker 收集一个 batch」的超时值，应非负，默认 0；文档未写 0 的含义 | 参数表 | 官方文档 | 文档缺口由源码补齐 |
| 源码：timeout<0 抛 ValueError；timeout==0 走无超时循环收数、每 MP_STATUS_CHECK_INTERVAL=5.0 秒检查一次 worker 存活（_utils/__init__.py L20）；timeout>0 超时抛 RuntimeError("DataLoader timed out after … seconds")；单进程迭代器 assert self._timeout == 0（num_workers=0 设正 timeout 触发断言，文档未写） | dataloader.py#L266-L267、#L743、#L1389、#L1400-L1422；_utils/__init__.py#L20 | 固定源码（文档未覆盖项标为源码行为） | 无 |
| pin_memory=True：返回前把 Tensor 复制到 pinned memory，加速到 CUDA GPU 的传输；自定义 batch 类型需自定义 pin_memory()；pin_memory_device 默认 ''。源码：空设备名时 `torch.cuda.is_available()` 决定（"choose cuda for default"） | 参数表、#memory-pinning；dataloader.py#L657-L669、#L1150-L1163 | 官方文档 + 固定源码 | pinning 的加速语义属 CUDA 语境；非 CUDA 平台行为不能据此声明 |
| worker_init_fn：在每个 worker 上以 worker id 调用，时机在 seeding 之后、数据加载之前；spawn 下必须可 pickle；worker 种子为 base_seed+worker_id | 参数表及 Warning；#platform-specific-behaviors；#randomness-in-multi-process-data-loading | 官方文档 | 无 |
| in_order=False 不保证 batch 按 FIFO 返回，仅 num_workers>0 生效；Warning：可能损害可复现性、数据不均衡时可能使数据分布倾斜 | 参数表及 Warning | 官方文档 | 无 |

### worker 异常与失败模式（文档缺口由固定源码补齐）

| 主张 | 证据位置 | 证据类型 | 反证/未知 |
|---|---|---|---|
| data.html 未说明 worker 崩溃时主进程收到什么错误 | 全文检索无对应文本 | 负面结论 | 需引源码 |
| 主进程 _try_get_data 手动存活检查，发现本应存活的 worker 不存活时抛 RuntimeError("DataLoader worker (pid(s) …) exited unexpectedly")（主任务抽查确认）；docstring 原文 "if any worker died expectedly"（疑为 unexpectedly 笔误，照录）；非 Windows 另有 SIGCHLD handler，手动检查是 Windows 上唯一检测机制 | dataloader.py#L770、#L1238、#L1240-L1246、#L1262-L1266 | 固定源码 | docstring 笔误按原文 |
| pin_memory_thread 死亡抛 RuntimeError("Pin memory thread exited unexpectedly") | dataloader.py#L1400-L1422 分支 | 固定源码 | 无 |
| worker 内 dataset/collate 抛异常时包为 ExceptionWrapper 传回主进程 reraise | dataloader.py#L1502-L1506 | 固定源码 | 无 |
| Linux 上 worker 与主进程经 SHM 文件/FD 传数据，FD 耗尽抛 RuntimeError("Too many open files. Communication with the workers is no longer possible…")；NOTE 建议 ulimit -n 或 set_sharing_strategy('file_system') | dataloader.py#L1280-L1289、#L1292-L1320 | 固定源码 | 仅 Linux 语境 |
| Warning：多进程加载若干次迭代后，worker 对父进程中被访问过的所有 Python 对象消耗与父进程等量的 CPU 内存（总内存 ≈ worker 数 × 父进程大小）；建议换成非引用计数表示（Pandas/Numpy/PyArrow），链接 issue #13246 | #multi-process-data-loading 第一个 Warning | 官方文档 | 是 refcount/fork 内存放大，不是泄漏措辞；页面没有把 persistent_workers 与内存增长关联 |
| Warning：一般不建议多进程加载返回 CUDA tensor（多进程共享 CUDA tensor 的微妙之处），建议改用 pin_memory=True | #multi-process-data-loading 第二个 Warning | 官方文档 | 仅 CUDA |

### torch.profiler（https://docs.pytorch.org/docs/2.6/profiler.html，新登记 src.pytorch.profiler-2.6）

| 主张 | 证据位置 | 证据类型 | 反证/未知 |
|---|---|---|---|
| activities 支持 ProfilerActivity.CPU/CUDA/XPU；默认为 CPU 加可用的 CUDA 或 XPU；枚举成员为 CPU、XPU、MTIA、CUDA、PrivateUse1 | #torch.profiler.profile、#torch.profiler.ProfilerActivity | 官方文档 | 页面无 NPU 字样；PrivateUse1 无任何使用说明——只能写「枚举含 PrivateUse1，文档未给进一步语义」 |
| schedule(*, wait, warmup, active, repeat=0, skip_first=0, skip_first_wait=0)：跳过 skip_first 步、等待 wait、warmup、记录 active，repeat=0 循环到 profiling 结束；warmup 步不产出 trace | #torch.profiler.schedule | 官方文档 | 无 |
| on_trace_ready 在 RECORD_AND_SAVE 的每一步调用；官方建议 tensorboard_trace_handler；默认 schedule 在整个 context manager 期间连续记录 | #torch.profiler.profile | 官方文档 | ProfilerAction 成员名未在页面枚举 |
| export_chrome_trace(path) 导出 Chrome JSON；启用 kineto 时只导出 schedule 的最后一个 cycle | #torch.profiler._KinetoProfile.export_chrome_trace | 官方文档 | 无 |
| key_averages 可按输入形状/栈分组（需 record_shapes/with_stack）；record_shapes=True 临时持有 tensor 引用，带来额外开销和拷贝 | #torch.profiler._KinetoProfile.key_averages；profile Notes | 官方文档 | 无 |
| profile_memory 跟踪 tensor 内存分配/释放；export_memory_timeline 可导出 .html/.json 时间线 | 参数表；#torch.profiler._KinetoProfile.export_memory_timeline | 官方文档 | 无 |
| record_function 不在 profiler.html；它在 torch.autograd.profiler.record_function（生成页 HTTP 200 确认存在，未逐句读正文） | profiler.html 全文检索；docs/2.6/autograd.html | 负面结论 + 官方文档 | 未读生成页正文 |
| DataLoader 迭代器每次 __next__ 包在 record_function 里，区间名 `enumerate(DataLoader)#{_SingleProcessDataLoaderIter|_MultiProcessingDataLoaderIter}.__next__`——trace/key_averages 中可直接观测取 batch 等待 | dataloader.py#L680、#L703-L704 | 固定源码 | 无 |

## 未解决与抓取失败

- 无抓取失败。
- ProfilerAction 成员名、record_function 生成页正文未逐句核对。
- data.html 无 GC 与 worker 关系的说明；data.html 未覆盖 FD 耗尽（仅源码）。
- NPU 侧 profiler 能力（torch_npu.profiler 等）本轮未核对，正文标未知并指向平台文档。
