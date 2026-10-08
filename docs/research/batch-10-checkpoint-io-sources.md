# 第十批来源记录：Checkpoint 慢写与恢复 I/O（R2-09）

**2026-10-08 修订注记：** Codex `gpt-6.1-sol / xhigh` 按 B10-C02 修正本记录并完成[定向复核](batch-10-11-12-codex-recheck.md)。下述原研究者、首次获取方式与当时任务状态为历史；修订补读和保留的未知条件见本记录及复核报告。

研究日期：2026-09-30。目标正文：`knowledge/04-data-storage/checkpoint-slow-io-triage.md`（procedure）。版本：PyTorch 2.6 文档 + 固定 v2.6.0 commit `1eba9b3aa3c43f86f4a2c807ac8e12c4a7767340`；MindCluster v26.1.1 固定 commit `44385c13`；Linux kernel v6.16 固定 commit（vm.rst）；MLPerf Storage v2.0 固定 commit；fsync man-pages 6.19。未执行任何保存/恢复或存储操作。

## 主张—证据表（DCP async_save 与 staging，PyTorch 2.6）

| 主张 | 证据位置 | 类型 | 反证/未知 |
|---|---|---|---|
| async_save 先把 state_dict 暂存（staging，默认 CPU 内存）到 AsyncStager，再在独立线程调用 save；返回持有 Metadata 的 Future；experimental | docs/2.6/distributed.checkpoint.html async_save 条目；state_dict_saver.py L170–171、L250 | 文档 + 固定源码 | — |
| **主线程承担 staging**：L228–241 先 `storage_writer.stage(state_dict)`（调用线程内、阻塞），再 `executor.submit(save, ...)`（ThreadPoolExecutor max_workers=1）。即 2.6 的"异步"不覆盖 D2H 拷贝本身 | state_dict_saver.py L228–242 | 固定源码 | 大 state_dict 的 staging 仍在主线程阻塞训练循环 |
| 进程组须含 CPU 后端，否则 assert 报错（'A CPU backend must be enabled for async save'）；dist 未初始化时跳过该检查（单机本地保存） | state_dict_saver.py L216–221 | 固定源码 | — |
| AsyncStager 协议：stage 产出"training-safe"副本（完成后训练更新不得影响副本）；默认 BlockingAsyncStager 在 CPU RAM 复制整个 state_dict；cache_staged_state_dict=True 时用 pinned memory 缓存降低 staging 延迟（代价是常驻内存）；FileSystemWriter 继承 BlockingAsyncStager，故默认 writer 即 stager | staging.py L15–41、L70–117；filesystem.py L710 | 固定源码 | L80 注释 "default to True" 与 L81 代码 False 不一致（因同步为 no-op）；注释/代码冲突以代码为准 |
| save 内有两次集合通信同步点：planning 的 reduce_scatter("plan") 与写入的 all_reduce("write")；NCCL 组需把对象内部张量搬到 GPU | state_dict_saver.py L273、L286–317、L320–334；文档 save 条目 Note | 固定源码 + 文档 | 慢 rank 会拖到这两个集合点；文档未量化 |
| FileSystemWriter 参数：thread_count（写线程数，默认 1）、per_thread_copy_ahead（GPU 预拷贝字节数，默认 10MB）、single_file_per_rank（默认 True）、sync_files（默认 True）、cache_staged_state_dict、overwrite | 文档 FileSystemWriter 签名；filesystem.py L444–476、L724–742 | 文档 + 固定源码 | overwrite 实现未核对 |
| 已知性能陷阱（源码 TODO）：多线程与 _OverlappingCpuLoader 组合会 "significant performance degredation"（上游原文拼写如此，与 cuda stream syncs 相关），重叠 D2H 装载仅在 thread_count==1 且 inflight_threshhold>0 时启用，否则退回串行 | filesystem.py L290–302 | 固定源码（作者注释） | 未给量化与 issue 链接 |
| 写入路径：single_file_per_rank 时按大小/类型分桶，起 thread_count−1 个线程加当前线程并发写；张量用 torch.save 逐条序列化；sync_files=True 时每文件写后 os.fsync（无该属性退回 os.sync()）；finish 写 .metadata.tmp、可选 fsync、删旧后 rename | filesystem.py L507–571、L249–270、L331–334、L574–595 | 固定源码 | — |
| 观测接口：save/async_save 被 _dcp_method_logger 装饰，向 dcp_logger 记录 start/end/exception 事件（含 time(ns) 与 times_spent），默认 NullHandler | 文档末节 observability；logger.py L62–99；state_dict_saver.py L57、L161 | 固定源码 + 文档 | 只有方法级总耗时，不分阶段计时 |
| 恢复侧（2.6）：FileSystemReader.__init__ 只有 path 参数，无读取并发参数、无 async_load API；read_data 逐文件逐请求串行读（源码 TODO：sort by offset and cache）；torch.load map_location="cpu" + narrow + copy_ 进目标张量（含 H2D） | filesystem.py L617–622、L633–674 | 固定源码 | loader 集合调用精确行号未核（引用前需补）；读并行化需自定义 StorageReader |

## 主张—证据表（Linux 页缓存/writeback，kernel v6.16 固定 commit 038d61fd）

| 主张 | 证据位置（Documentation/admin-guide/sysctl/vm.rst） | 反证/未知 |
|---|---|---|
| dirty_background_ratio/dirty_background_bytes 定义触发后台 writeback 的脏页阈值 | L165–186 | 不是所有写回的唯一触发条件；同页还有老化脏页与周期写回，显式 fsync 另见已登记 fsync(2) |
| 脏页达 dirty_ratio/dirty_bytes 时，**产生写盘的进程自身被拖入 writeout**（写者节流）——"write 变慢"的内核侧机制 | L188–202、L213–221 | 未展开 direct reclaim 细节；这是等待层定位，不能排除后端慢造成脏页积累；根因需同窗口后端吞吐/延迟/错误证据，此限制为本库归因判断 |
| 脏数据驻留超 dirty_expire_centisecs 才有资格被刷出；flusher 按 dirty_writeback_centisecs 周期唤醒（置 0 关闭周期写回） | L204–211、L235–242 | — |
| docs.kernel.org HTML 为动态 latest 且页头残留 "valid for Linux kernel version 2.6.29" 陈旧字样；固定引用走 git commit | 页面头部（2026-09-30 观察） | 不作不可变快照 |

与 fsync(2)（man-pages 6.19）组合：「write 返回≠落盘；数据在页缓存由 flusher 后台刷出；脏页超限写者被节流」三句均有版本化官方证据。

## 主张—证据表（MindIO ACP 接口文档，MindCluster v26.1.1 固定 commit）

| 主张 | 证据位置（component/mindio/acp/doc/） | 反证/未知 |
|---|---|---|
| save(obj, path, open_way='memfs')：memfs 为"高性能 MemFS"（默认），fopen 为 C 标准库备份路径；返回值区分 -1 失败 / 0 原生 torch.save / 1 memfs / 2 fopen | Interface_description/save接口.md L9–11、L44–54、L66–71 | memfs 内部实现与带宽数字未给出 |
| multi_save：同一数据写多个文件 | multi_save接口.md L3–11、L56–61 | 副本冗余语义未明说 |
| **flush()：等待后台异步刷盘任务全部执行成功**；返回 0 成功 / 1 失败——内存暂存→后端持久化的完成信号接口 | flush接口.md L3–5、L24–27 | 无超时、无部分失败语义 |
| register_checker(callback, check_dict, user_context, timeout_sec) 注册异步回调 | register_checker接口.md L3–9、L81–84 | 回调触发条件细节未读全 |
| load(path, open_way='memfs', map_location=None)；明示 pickle 反序列化安全须知 | load接口.md | — |
| 环境变量仅 MINDIO_AUTO_PATCH_MEGATRON 与 HCOM_FILE_PATH_PREFIX；**无性能/并发调节参数** | doc/环境变量.md（全 33 行） | 无批量/并发/吞吐数据 |

## 主张—证据表（MLPerf Storage v2.0 checkpointing 负载）

| 主张 | 证据位置（Submission_guidelines.md，commit 7e71ca16） | 反证/未知 |
|---|---|---|
| v2.0 起新增 Checkpointing 负载类别，须连跑 10 次取平均 | L47–48、L71 | — |
| 四个 LLaMA3 配置（8B/70B/405B/1T），checkpoint 105GB–18TB，MPI 进程 8–1024 | §2.2.1 L97–117（Table 2） | 规则内配置，非本库环境 |
| 两种模式：default（共享存储）与 subset（节点本地、单主机只写自己份额） | §2.2.2 L119–126 | — |
| 流程：先写 10 个 →（需要时 drop_caches 清缓存）→ 读 10 个；"checkpoint 每客户端大小 < 3× 客户端内存则必须清缓存" | L128–165、§2.2.2.1 L167–180 | 直接支撑"页缓存污染读测量"的诊断点 |
| 规则强制 fsync："We enforce fsync to be applied during checkpoint writes to ensure data is flushed to persistent storage" | L182–184 | 实现未读 |
| 指标：写带宽、读带宽、写完到跨 host 可读的时延；无需真实加速器 | §4.2 L351–355 | — |

## 未解决与抓取失败

- 无抓取失败。
- 网络文件系统/RDMA/对象存储的传输行为无已读来源覆盖，是明确缺口；DCP loader 集合调用行号未核；MLPerf llama3_*.yaml 的 I/O 参数与 DLIO checkpoint 实现未读；MindIO memfs 实现与性能数据未获取；PyTorch 教程页为动态页（含 2.9 内容），只作限定引用。
