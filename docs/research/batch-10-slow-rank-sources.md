# 第十批来源记录：慢 rank 观测证据（R2-07）

**2026-10-08 修订注记：** Codex `gpt-6.1-sol / xhigh` 按 B10-C01 修正本记录并完成[定向复核](batch-10-11-12-codex-recheck.md)。下述原研究者、首次获取方式与当时任务状态为历史；修订补读和保留的未知条件见本记录及复核报告。

研究日期：2026-09-30。目标正文：`knowledge/06-training/slow-rank-triage.md`（procedure）。版本：PyTorch 2.8 文档 + 固定 v2.8.0 commit `ba56102387ef21a3b04b357e5b183d48f0afefc7` 源码；NCCL 2.27.5 归档；DCGM latest 页（可变，2026-09-30 观察）+ DCGM v3.3.9 固定 commit。未运行任何分布式作业。

## 主张—证据表（PyTorch 2.8 ProcessGroupNCCL）

| 主张 | 证据位置 | 类型 | 反证/未知 |
|---|---|---|---|
| TORCH_NCCL_DESYNC_DEBUG：watchdog 超时/异常时输出 desync 报告；文档页只说明其用于定位 collective desync 的肇事 rank，三类文本（从未进入 collective（"never joined any collectives"）、进入但未完成（"joined but didn't finish collective #N"）、完成 #N 但未加入 #N+1）存在于固定源码；附全体 rank 最新状态快照 | docs/2.8/torch_nccl_environment_variables.html 表格；TraceUtils.h L78–258（analyzeMissingRanks/analyzeLaggingRanks/dumpSnapshot/retrieveDesyncReport）；ProcessGroupNCCL.cpp L2242–2249、L2429–2460 | 文档 + 固定源码 | 依赖各 rank 向 c10 Store 写 trace key，Store 不可达时报告失败；报告措辞 "To our best knowledge" 是推断非证明 |
| DESYNC_DEBUG 默认关闭；若 TORCH_NCCL_ASYNC_ERROR_HANDLING=0，源码会**强制把 async error handling 改回开启**（置 SkipCleanUp）并日志提示；开启时顺带开启 per-collective timing | ProcessGroupNCCL.cpp L976–980、L992–999 | 固定源码 | 文档未写默认值，默认值来自源码；复查修正：强制改回的方向是开启 async error handling，不是禁用 desync |
| TORCH_NCCL_DUMP_ON_TIMEOUT + TRACE_BUFFER_SIZE>0：watchdog 超时或异常触发 flight recorder dump；dump 经 TCPStore 跨 rank 协调（首个超时 rank 写 key，其余 rank monitor 轮询后同样 dump） | 文档页表格；ProcessGroupNCCL.cpp L1764–1829、L1882–1906 | 文档 + 源码 | 源码注释承认变量名与"含异常"的实际行为不符，名字可能变化 |
| flight recorder entry 字段：collective_seq_id、op_id、profiling_name、input/output sizes 与 dtypes、time_created_ns、duration_ms、timeout_ms、time_discovered_started/completed_ns、state、thread；顶层含 pg_status（lastEnqueuedWorkName/lastCompletedWorkName 等）；**time_discovered_* 是 CPU 侧发现时刻，"will always be after it actually started"——不是设备真实起止** | FlightRecorder.hpp L23、L33–52、L105–166；ProcessGroupNCCL.cpp L2372–2374 | 固定源码 | 观测假象类候选的重要限定 |
| TRACE_BUFFER_SIZE：环形缓冲最大事件数；v2.8.0 源码 PG 侧默认 2000（L967），FlightRecorder.hpp L100 同名（含 TORCH_FR_BUFFER_SIZE 别名）默认 0——两处口径不一致，实际生效路径未追到底，标未知 | ProcessGroupNCCL.cpp L967；FlightRecorder.hpp L100 | 固定源码 | 默认值口径冲突未解 |
| heartbeat monitoring：2.8 的变量名是 TORCH_NCCL_ENABLE_MONITORING（不存在 TORCH_NCCL_HEARTBEAT_MONITOR）；watchdog 无心跳超 TORCH_NCCL_HEARTBEAT_TIMEOUT_SEC（默认 480s）后 abort。**与 watchdog 的区别**：watchdog 按 collective 的 PG timeout 盯每个 work；heartbeat monitor 盯 watchdog 线程本身是否卡住（典型 CUDA/NCCL API hang 或持 GIL 调 CUDA API 死锁） | 文档页表格；ProcessGroupNCCL.cpp L1671–1684、L1833–1858 | 文档 + 源码 | 报错文案自认可误报（false positive abort 可提 issue） |
| TORCH_NCCL_WAIT_TIMEOUT_DUMP_MILSEC：退出并抛超时异常前等待 dump 完成的额外时间；源码默认 15000ms | 文档页；ProcessGroupNCCL.cpp L1673–1674、L1900–1905 | 文档 + 源码 | L1876 注释写 "one minute" 与默认值矛盾，以代码为准 |
| flight recorder dump 按 rank 分文件（DebugInfoWriter 文件名含 rank），比对各 rank 最后一条 entry 的 seq 可定位落后 rank；可用 TORCH_NCCL_DEBUG_INFO_PIPE_FILE 手动触发 | FlightRecorder.hpp L61–84；文档页 | 源码 + 文档 | 环形缓冲在进程内，崩溃前未必落盘 |

## 主张—证据表（PyTorch 2.8 distributed.html）

| 主张 | 证据位置 | 反证/未知 |
|---|---|---|
| TORCH_DISTRIBUTED_DEBUG=OFF（默认）/INFO/DETAIL；DETAIL 输出按 rank 分行的运行时统计（Avg forward/backward compute、Avg backward comm、comm/comp overlap），可直接横向对比慢在哪个阶段；DETAIL 还对每次 collective 做一致性检查（monitored_barrier + 类型/shape 校验），失配给明确错误而非 hang；DETAIL 影响性能仅调试用 | #torch-distributed-debug 小节 | 统计只有 DDP 路径；开销未量化 |
| monitored_barrier(timeout, wait_all_ranks)：rank 0 报告哪些 rank 未在超时内通过 barrier；**仅支持 GLOO backend**；有性能影响 | #monitored-barrier | NCCL 不可用，NCCL 训练须另建 GLOO 组 |
| NCCL 层排障：NCCL_DEBUG=INFO；NCCL_DEBUG_SUBSYS=COLL 打印 collective 调用日志，对 hang（尤其类型/大小失配导致）有用；GRAPH 打印拓扑检测 | "Other NCCL environment variables" 小节 | 只覆盖 hang/mismatch 场景 |
| Logging 矩阵：TORCH_CPP_LOG_LEVEL × TORCH_DISTRIBUTED_DEBUG 决定有效级别 | #logging | — |
| torch.distributed.breakpoint(rank)：单 rank 进 pdb，其余经 barrier 等待 | API 条目 | 交互式，不适合生产 |

## 主张—证据表（NCCL 2.27.5 RAS，troubleshooting/ras.html）

| 主张 | 证据位置 | 反证/未知 |
|---|---|---|
| RAS 自 2.24 内建默认开启；每进程一个 RAS 线程走 bootstrap 带外 TCP，与 RDMA 主流量不竞争；输出格式 "expected to evolve" | Principle of Operation | 格式未冻结 |
| MISMATCH：communicator 各 rank 上报计数/状态不一致；离群组可逐成员列出 Rank/GPU/进程 PID/节点 IP。默认组规模 ≤25% 总数且 ≤10 成员才展开，verbose 放宽为 <50% 且取消成员数限制 | [Sample Output MISMATCH 段](https://docs.nvidia.com/deeplearning/nccl/archives/nccl_2275/user-guide/docs/troubleshooting/ras.html#sample-output) | 只提供候选 rank；无差异或未展开不能区分全体/个别慢，计算/数据阶段慢可能不形成 collective 计数差异；这是本库推论，需完整响应与各 rank 阶段时间线支持 |
| 活跃通信期间计数差异是正常瞬态；"an experience with a particular workload is needed to determine what's normal"；重复查询计数不推进可能提示 stuck，仍需调查 | MISMATCH 段后半 | 无判定阈值（查询次数/间隔未定义） |
| INIT/FINALIZE 过渡期 MISMATCH 同为瞬态 | 第二个样例 | — |
| 进程无响应：先 INCOMPLETE，RAS 绕行重试，60 秒不可达判 DEAD（permanent） | INCOMPLETE/DEAD 段 | DEAD 后动作留给用户 |
| ncclras 客户端：localhost:28028（NCCL_RAS_ADDR）；文本协议，可 telnet/netcat；命令 STATUS/VERBOSE STATUS/TIMEOUT | RAS Queries 段 | 每节点本地查询，跨节点汇总需自行编排 |

## 主张—证据表（DCGM 慢 rank 设备侧字段）

| 主张 | 证据位置 | 反证/未知 |
|---|---|---|
| 慢 rank 相关字段：SM/MEM 时钟（gauge）、GPU/显存温度（°C）、整板功耗（W）、累计能耗（mJ，自驱动加载起）、GPU_UTIL（NVML 口径）、PROF_GR_ENGINE_ACTIVE 等比例字段（0–1）、PROF_PCIE_TX/RX_BYTES（方向从 GPU 视角）、PCIE_REPLAY_COUNTER（重传=链路质量信号）、NVLINK_BANDWIDTH_TOTAL | dcgm-exporter-metrics.html 各表 + dcgm-api-field-ids.html | 单位个别未明示（SM_CLOCK 的 MHz 为惯例）；PROF_PCIE gauge 的速率口径未写清 |
| violation 计数器（POWER/THERMAL 等六个，ns）与 DCGM_EXP_CLOCK_EVENTS_COUNT/TOTAL 默认注释掉需显式开启；COUNT 计窗口内样本数不是事件数，TOTAL 计 inactive→active 跳变、重启清零 | exporter 页 Shipped Optional/Exporter-Owned 小节 | shipped CSV 无 MAX_SM_CLOCK，当前 vs 目标时钟对比需自定义字段 |
| 字段不保证运行时输出（取决于 DCGM/GPU/驱动/权限/部署）；PROF_* 按 GPU 0 探测能力集 | exporter 页限定段 | — |
| PyTorch 2.6 profiler 的分布式能力：仅 tensorboard_trace_handler 的 worker_name（默认 [hostname]_[pid]），页面无多进程聚合视图 | docs/2.6/profiler.html 全文 | 跨 rank 对齐需自行按文件组织 |

## 未解决与抓取失败

- 无抓取失败。
- flight recorder 默认值口径冲突（PG 2000 vs FR 0）未追到底；DCGM 个别单位未明示；RAS 判读无阈值。
- NPU 侧的慢 rank 观测（HCCL/MindCluster 等价物）本轮未研究，正文标缺口。
