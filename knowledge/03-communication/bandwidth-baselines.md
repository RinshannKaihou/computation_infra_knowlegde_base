---
id: communication.bandwidth-baselines
title: 通信带宽与性能基线口径
type: reference
domain: communication
status: draft
platforms: [generic]
source_refs:
  - src.nvidia.nccl-tests-b4d5beeb
  - src.ascend.cann-hccl-2d685b08
  - src.rocm.rocm-systems-therock-10.1
  - src.nvidia.nccl-user-guide-2.27.5
  - src.nvidia.dgx-superpod-h100-ra-fabrics-2026-10-09
  - src.nvidia.gpu-node-triage-2026-10-08
  - src.huawei.hccl-perf-test-guide-cann-9.1.x
updated_at: "2026-10-14"
summary: 区分集合通信的操作耗时、算法带宽、模型换算带宽与物理链路遥测，并给出建立可比较基线所需的消息、rank、缓冲区、计时、拓扑及正确性字段。
related_ids:
  - communication.collectives-and-rank-progress
  - hardware.resource-topology
  - reliability.dimensions-and-failure-domains
verification:
  status: source_checked
  evidence_refs:
    - src.nvidia.nccl-tests-b4d5beeb
    - src.ascend.cann-hccl-2d685b08
  notes: 仅核对固定 NCCL-tests 与 cann-hccl 仓库快照中本文引用的 README、性能说明、实现和许可证；2026-10-13 第二轮加法核对 rccl-tests therock-10.1（PERFORMANCE/参数/计时实现交叉；AllGather gin_sdma 系数经审阅方核对，角色已注；余算子实现未逐一回查）、NCCL 2.27.5 env（路径选择证据）、SuperPOD fabric（同 SU rail/超配）、GPU Node Triage（正确 URL 与 Network Testing 锚点已核对，可变页观察日期 2026-10-13）、CANN 9.1.X 指南 0001/0004–0007（算法带宽、参数契约、跨节点字段；计时实现 unknown；BLOCKED-1 交集保持 blocked）；审阅方独立取证见 [T03-07 加法初审](../../docs/research/batch-19-t03-07-codex-review.md)，不冒充作者当时已完成；未运行工具、未访问 GPU/NPU，也未验证任何机型峰值或通用阈值。
---

# 通信带宽与性能基线口径

集合通信报告中的 `time`、`algbw`、`busbw`、`alg_bandwidth` 和链路计数器回答的问题不同。比较两个结果之前，必须先固定算子、消息大小的定义、rank 数、数据类型、缓冲区模式、计时与同步方式、拓扑和并发负载；只比较一列“GB/s”通常没有可解释性。

本文给出记录和解释通信性能基线的口径。`generic` 表示这套区分方法可用于组织 GPU/NPU 证据，不表示 NCCL 与 HCCL 的字段、公式、工具实现或硬件峰值等价。正文中的 NCCL 公式来自固定的 NVIDIA `nccl-tests` 快照；HCCL 小节只复述固定官方来源明确给出的字段语义。本文没有本地性能结果，也不提供跨机型、跨规模或跨平台的合格阈值。

集合算子的输入、输出和 rank 进度关系见[集合通信语义与 rank 进度](collectives-and-rank-progress.md)；本文只讨论如何度量和比较其性能。

## 先区分四种量

| 量 | 本文中的定义 | 主要用途 | 不能直接推出什么 |
|---|---|---|---|
| 操作耗时 `t` | 在明确同步边界下，一次集合操作从所选计时起点到完成点的时间；报告可为均值、最小/最大或分位数 | 小消息固定开销、同一条件下的端到端操作成本、长尾 | 大消息的 `t` 同时包含固定开销和随数据量增长的传输/规约时间，不能一概称为纯 latency |
| 算法带宽 `algbw` | 按基准定义的逻辑消息量 `S` 除以操作时间：`S / t` | 估算相同算子和相同 `S` 口径下的大消息完成时间 | 不是物理链路逐字节采样；不同算子的 `S` 可能代表每 rank 输入、总输入或总输出 |
| 模型换算带宽 `busbw` | 将 `algbw` 乘以算子和 rank 数相关的模型系数，试图把集合操作换算为可与瓶颈互联能力对照的量 | 在同一工具定义内减弱 rank 数和集合语义对数值的影响 | 不是 NIC/NVLink/PCIe 的实测吞吐，也不保证对应某一条链路；层次化、聚合卸载或特殊算法会使简单模型与真实流量分布不同 |
| 物理链路遥测 | 从 NIC、交换机、PCIe、设备互联或 profiler 读取的端口/链路字节、包、利用率和时间窗口 | 判断哪条实际链路承载了多少流量、拥塞或重试发生在哪里 | 不能不经时间对齐和开销说明就替代集合操作耗时；单端口值也不等于整个通信域的逻辑吞吐 |

固定 `nccl-tests` 性能说明把小尺寸的时间用于观察常量开销，并指出大尺寸时间近似为“开销 + 大小/带宽”；同一说明定义 `algbw = S/t`，再按算子应用系数得到 `busbw`（[`doc/PERFORMANCE.md`](https://github.com/NVIDIA/nccl-tests/blob/b4d5beebca8a76cf01335f724d154b9b9d394d96/doc/PERFORMANCE.md)）。因此，本页将“latency”保留给小消息区间的固定开销讨论或经过模型拟合的截距；若报告只是大消息平均操作时间，应写“操作耗时”，不要改名为网络 latency。

## 单位和消息大小必须成对记录

带宽的分子与分母必须写出单位。`nccl-tests` 的 `-b/-e/-i` 大小后缀采用二进制倍数：`K=1024 B`、`M=1024^2 B`、`G=1024^3 B`；它输出带宽时，源码用 `1.0E9` 将 `byte/s` 换成 `GB/s`。所以命令中的 `32M` 是 32 MiB，而结果中的 `GB/s` 是十进制十亿字节每秒。这两个约定可以同时成立，不能把 `M` 参数误写成 MB，也不能把结果列擅自改成 GiB/s（[`README.md` 的 size 参数](https://github.com/NVIDIA/nccl-tests/blob/b4d5beebca8a76cf01335f724d154b9b9d394d96/README.md#arguments)，[`src/common.cu` 的大小解析](https://github.com/NVIDIA/nccl-tests/blob/b4d5beebca8a76cf01335f724d154b9b9d394d96/src/common.cu#L240-L274)）。

一个可比较记录至少包含：

- 原始命令或等价配置中的 `min/max/step`，并展开为精确 byte 数；
- 输出 `size` 列究竟是每 rank 输入、每 rank 输出、全体 rank 合计，还是工具内部归一化量；
- 数据类型和元素数，确认 `count × sizeof(datatype)` 与 byte 数一致；
- 带宽单位是 `GB/s`、`GiB/s`、`Gb/s` 还是端口线速单位；若从 bit/s 转 byte/s，明确除以 8，且不要忽略编码、协议头、重传和有效载荷比例；
- payload 是否包含 padding、对齐截断、元数据或控制流量。固定 `nccl-tests` 对部分算子会按 16-byte 边界调整 count，不能只用原始命令参数反推实际 payload。

“消息大小”也不是跨算子的同义词。对 ReduceScatter，NCCL 性能说明中的 `S` 是每个 rank 的总输入数组大小，即 `recvcount × sizeof(datatype) × n`；对 AllGather，`S` 是每个 rank 最终总输出数组大小，即 `sendcount × sizeof(datatype) × n`。这两项若误用每 rank 的分片大小，`algbw` 会相差一个 rank 数因子（[`PERFORMANCE.md` ReduceScatter/AllGather`](https://github.com/NVIDIA/nccl-tests/blob/b4d5beebca8a76cf01335f724d154b9b9d394d96/doc/PERFORMANCE.md#reducescatter)）。

## NCCL-tests 的算子换算表

下表只适用于固定快照 `b4d5beebca8a76cf01335f724d154b9b9d394d96` 中 `nccl-tests` 的定义。令 `n` 为参与该 communicator 的 rank 数，`t` 为 `getBw` 实际使用的 `deltaSec` 完成时间分母（归一化与聚合条件见下文），不一定是显示的 `time` 列，`S` 为表中逻辑消息量。所有 `GB/s` 都以 `10^9 byte/s` 换算。

| 算子 | `S` 的口径 | `algbw` | `busbw` 换算 | 解释条件 |
|---|---|---|---|---|
| AllReduce | 每 rank 的输入/输出 payload | `S/t` | `algbw × 2(n-1)/n` | 性能说明按每元素 `2(n-1)` 次跨 rank 数据转移并由 `n` 个 rank 的外向能力分摊；这是模型换算，不是实际选中 ring 的证明 |
| ReduceScatter | 每 rank 的总输入；输出为 `S/n` | `S/t` | `algbw × (n-1)/n` | `S = recvcount × datatype_size × n`，不能把单 rank 输出分片当成 `S` |
| AllGather | 每 rank 的总输出；输入为 `S/n` | `S/t` | `algbw × (n-1)/n` | `S = sendcount × datatype_size × n`，固定实现据此计算 base bandwidth |
| Broadcast | root 的 payload，也是每个接收 rank 的结果大小 | `S/t` | `algbw` | 模型把 root 的外向能力作为瓶颈，系数为 1；不能据此声称实际只有一次物理传输 |
| Reduce | 每 rank 的输入 payload，也是 root 的结果大小 | `S/t` | `algbw` | 模型把流向 root 的能力作为瓶颈，系数为 1；规约计算与协议开销仍在 `t` 中 |
| AlltoAll | 每 rank 总发送量/总接收量，即全部 peer 分片之和 | `S/t` | `algbw × (n-1)/n` | 每 rank 给自己的分片不经过外部链路；固定实现不支持 in-place AlltoAll 的正确性报告 |

公式来源见固定 [`doc/PERFORMANCE.md` 的 Summary](https://github.com/NVIDIA/nccl-tests/blob/b4d5beebca8a76cf01335f724d154b9b9d394d96/doc/PERFORMANCE.md#summary)。实现交叉核对显示：AllReduce 直接以 `count × typesize` 为 base bandwidth；AllGather 以 `count × typesize × n` 为 base bandwidth；AlltoAll 也将单 peer 的参数 count 乘以 `n` 后作为每 rank 总量（[`all_reduce.cu`](https://github.com/NVIDIA/nccl-tests/blob/b4d5beebca8a76cf01335f724d154b9b9d394d96/src/all_reduce.cu#L59-L65)、[`all_gather.cu`](https://github.com/NVIDIA/nccl-tests/blob/b4d5beebca8a76cf01335f724d154b9b9d394d96/src/all_gather.cu#L38-L44)、[`alltoall.cu`](https://github.com/NVIDIA/nccl-tests/blob/b4d5beebca8a76cf01335f724d154b9b9d394d96/src/alltoall.cu#L48-L54)）。

这组系数是 `nccl-tests` 的性能模型，不是从链路计数器采集的事实。官方说明最后说 `busbw` 应反映 NVLink、PCI、QPI 或网络等硬件瓶颈，但同一操作可能同时经过节点内和节点间路径，且层次化算法会让不同层承载不同字节量。结果高于某个单端口标称值时，先检查 rank 分组、端口聚合、双向口径、节点内/节点间分层、算法和卸载，再谈异常；不能直接用 `busbw / 单链路线速` 当链路利用率。

对表外算子、工具新增实现、设备侧自定义实现或 offload 路径，不应自创“通用 bus factor”。应固定工具版本，读取该算子的 size 和 bandwidth 实现，并将公式作为基准定义的一部分保存。

### RCCL-tests 的计时与换算（独立口径，therock-10.1；默认 host 模式）

下述只适用于 rocm-systems tag `therock-10.1`（commit `7da4302`，RCCL 2.30.7 线）的 rccl-tests **默认 host 计时模式**，不与上表 NCCL 公式互换；CPU 显示、graph、device-only 为例外分支（见下）。

- 修正因子（[`doc/PERFORMANCE.md`](https://github.com/ROCm/rocm-systems/blob/therock-10.1/projects/rccl-tests/doc/PERFORMANCE.md)）：`algbw=S/t`；busbw AllReduce `2(n-1)/n`、ReduceScatter/AllGather/AlltoAll `(n-1)/n`、Broadcast/Reduce `1`（busbw 对标硬件峰值、与 rank 数无关的设计目标；**普通 Broadcast 模式**，环境分支见下）。AllReduce 实现交叉核对：`baseBw = count·typesize/1.0E9/sec`，`busBw = baseBw·2(n-1)/n`（[`all_reduce.cu AllReduceGetBw` L78–84](https://github.com/ROCm/rocm-systems/blob/7da43026e4f2ef7600433c38c820732f7a205d22/projects/rccl-tests/src/all_reduce.cu#L78-L84)）；AllGather 实现 `gin_sdma_allgather::bandwidthGBps` 经审阅方核对为 `perRankCount·typeSize·n/1.0E9/sec` 与 `(n-1)/n` 系数（[`gin_sdma_allgather_policy.h` L145–155](https://github.com/ROCm/rocm-systems/blob/7da43026e4f2ef7600433c38c820732f7a205d22/projects/rccl-tests/src/gin_sdma_allgather_policy.h#L145-L155)，角色见注记），与 PERFORMANCE 页一致；其余算子实现未逐一回查。
- Broadcast 环境分支：`RCCL_TESTS_ALLGATHERV_ENABLE=1` 时用 `count·nranks·typesize` 与 `(n-1)/n`；普通 Broadcast 用 `count·typesize` 与系数 1（[`broadcast.cu` L82–93](https://github.com/ROCm/rocm-systems/blob/7da43026e4f2ef7600433c38c820732f7a205d22/projects/rccl-tests/src/broadcast.cu#L82-L93)；[`README grouped-broadcast`](https://github.com/ROCm/rocm-systems/blob/therock-10.1/projects/rccl-tests/README.md#user-content-grouped-broadcast-allgatherv-mode)）。PERFORMANCE 六系数只覆盖普通模式。
- 计时：报告 `time` 为 **us**（`deltaSec·1.0E6`，表头 `(us)`）；`getBw` 分母恒为 `deltaSec`；默认先按 `iters×agg_iters` 归一化（[`normalizeElapsedPerIter`](https://github.com/ROCm/rocm-systems/blob/7da43026e4f2ef7600433c38c820732f7a205d22/projects/rccl-tests/src/gin_sdma_devtime_host.h#L41-L51)），再按 graph launch 数缩放、按 `-a` 聚合。例外分支：`-C 1` 只有 `report_cputime && deviceImpl==0` 才显示 CPU 列（设备实现分支仍显示 deltaSec）；device-only 分支以设备 hook 返回时间替换 deltaSec；`-z 3` 报告时间排除 barrier。([common.cu L1070–1128](https://github.com/ROCm/rocm-systems/blob/7da43026e4f2ef7600433c38c820732f7a205d22/projects/rccl-tests/src/common.cu#L1070-L1128)、[L1259–1266](https://github.com/ROCm/rocm-systems/blob/7da43026e4f2ef7600433c38c820732f7a205d22/projects/rccl-tests/src/common.cu#L1259-L1266))
- 默认参数：`-b/-e` 默认 32M（二进制 MiB）、`-n 20`、`-w 1`、`-m 1`、`-a 1`（[`README Arguments`](https://github.com/ROCm/rocm-systems/blob/therock-10.1/projects/rccl-tests/README.md#user-content-arguments)）；`-O` 控制 in/out-of-place 取舍；`-A 1` 记录 algo/proto/nchannels（经 `rcclGetAlgoInfo`）。不写任何 GB/s 阈值；页脚判据为**平均 busbw < `NCCL_TESTS_MIN_BW`×0.9**（环境未设时取 -1，不过滤），方向不得写反（[common.cu L2757–2788](https://github.com/ROCm/rocm-systems/blob/7da43026e4f2ef7600433c38c820732f7a205d22/projects/rccl-tests/src/common.cu#L2757-L2788)）。

## rank 数、进程布局和并发组

固定 `nccl-tests` README 定义总 rank 数为：

```text
n = MPI process 数 × 每进程 thread 数 × 每 thread GPU 数
```

其中 MPI 管理进程数，`-t` 指每进程线程数，`-g` 指每线程 GPU 数（[`README.md` Usage](https://github.com/NVIDIA/nccl-tests/blob/b4d5beebca8a76cf01335f724d154b9b9d394d96/README.md#usage)）。基线不能只写“8 卡”或“64 rank”；还应保存节点数、每节点进程数、每进程线程和设备数、local/global rank 到物理设备的映射、CPU/NUMA 绑定以及 communicator 是否被拆分。

同一仓库支持用 `NCCL_TESTS_SPLIT` 将全体 GPU 分成多个并发通信组，并明确说明报告带宽是**每组**带宽；只有在分组确实并发且需要估算总负载时，才可再乘组数（[`README.md` Running multiple operations in parallel](https://github.com/NVIDIA/nccl-tests/blob/b4d5beebca8a76cf01335f724d154b9b9d394d96/README.md#running-multiple-operations-in-parallel)）。这个乘积仍是逻辑组吞吐之和，不是某个共享上联的实测流量。并发组若竞争相同 NIC、交换路径或设备互联，每组与总和都必须连同拓扑和端口遥测解释。

## in-place 与 out-of-place 是不同基线

固定 `nccl-tests` 对每个 size 依次执行并打印 out-of-place 和 in-place 结果（[`src/common.cu` 的 `TimeTest`](https://github.com/NVIDIA/nccl-tests/blob/b4d5beebca8a76cf01335f724d154b9b9d394d96/src/common.cu#L952-L960)）。两种模式的逻辑算子可以相同，但缓冲区地址、初始化、可注册内存、缓存效应和潜在拷贝行为不同，因此应保留成两条基线，不能择优混合。

记录时至少写明：

- send/recv buffer 是否独立，in-place 的有效数据位于 recv buffer 的哪个 rank offset；
- buffer 是否本地注册、对称注册、对齐或故意 misalign；
- 是否使用传统 host implementation、device implementation、host RMA 或 CUDA Graph；
- 工具是否真的支持该算子的 in-place 正确性检查。固定 AlltoAll 实现明确写出不支持 in-place AlltoAll，并在该模式关闭错误报告（[`src/alltoall.cu`](https://github.com/NVIDIA/nccl-tests/blob/b4d5beebca8a76cf01335f724d154b9b9d394d96/src/alltoall.cu#L23-L49)），所以不能把它的 in-place 性能列连同 `#wrong 0` 当成已验证基线。

## warm-up、iterations、计时和同步

“平均 20 次”仍不足以复现一个结果。至少保存以下字段：warm-up 次数、timed iterations、每个 iteration 聚合的操作数、run cycle、rank 聚合方式、blocking 模式、是否按 iteration 使用设备事件、是否跳过前几个样本、是否使用 graph capture，以及报告的是设备事件时间、CPU 提交时间还是端到端同步时间。

在固定快照中：

- 默认 `warmup_iters=1`、`iters=20`、`agg_iters=1`；warm-up 不计时。工具在数据初始化后发起 warm-up，等待完成，然后通过线程/MPI barrier 对齐再开始性能循环（[`README.md` Arguments](https://github.com/NVIDIA/nccl-tests/blob/b4d5beebca8a76cf01335f724d154b9b9d394d96/README.md#arguments)、[`src/common.cu` `BenchTime`](https://github.com/NVIDIA/nccl-tests/blob/b4d5beebca8a76cf01335f724d154b9b9d394d96/src/common.cu#L720-L733)）。
- 默认报告时间把性能循环总时间除以 `iters × agg_iters`，完成后再跨线程/进程按 `-a` 选择 rank 0、平均、最小或最大。MPI 场景默认 `-a 1` 为平均；比较时必须保留该聚合选项（[`README.md` `--average`](https://github.com/NVIDIA/nccl-tests/blob/b4d5beebca8a76cf01335f724d154b9b9d394d96/README.md#arguments)、[`src/common.cu`](https://github.com/NVIDIA/nccl-tests/blob/b4d5beebca8a76cf01335f724d154b9b9d394d96/src/common.cu#L795-L811)）。
- 默认 `-C 0` 显示由 `deltaSec` 换算的时间；`-C 1` 改为显示 `cputimeSec`。后者在最终 `completeColl` 之前取值，不能无条件解释为设备完成时间；blocking 选项也会改变它包含的等待。`getBw` 始终使用 `deltaSec`，所以不能用 `-C 1` 的显示时间反算主表带宽。CUDA Graph 模式对 `deltaSec` 另除以 graph launch 次数，而显示 CPU 时间没有这一步；必须保留 graph 配置（[`时间分母`](https://github.com/NVIDIA/nccl-tests/blob/b4d5beebca8a76cf01335f724d154b9b9d394d96/src/common.cu#L795-L824)、[`显示选择`](https://github.com/NVIDIA/nccl-tests/blob/b4d5beebca8a76cf01335f724d154b9b9d394d96/src/common.cu#L886-L887)）。
- `-I 1` 另用 CUDA event 记录逐 iteration 时间；聚合操作数大于 1 时除以 `agg_iters`。逐次报告取跨 GPU/线程/进程的最大值再生成摘要；它不是主表 `-a` 的聚合结果，也不替换 `getBw` 分母。`-K` 仅让逐次摘要跳过开头样本，原始数据仍保留，不改变主表带宽。少于 100 个样本时，README 警告 nearest-rank 的 p99 可能等于最大值（[`event timing`](https://github.com/NVIDIA/nccl-tests/blob/b4d5beebca8a76cf01335f724d154b9b9d394d96/src/common.cu#L666-L683)、[`逐次摘要`](https://github.com/NVIDIA/nccl-tests/blob/b4d5beebca8a76cf01335f724d154b9b9d394d96/src/common.cu#L889-L914)）。
- `-z` 改变操作内或外层 iteration 的等待和 barrier 位置；模式 3 的报告时间排除 barrier。不同 `-z` 值不能视为同一计时口径（[`README.md` `--blocking`](https://github.com/NVIDIA/nccl-tests/blob/b4d5beebca8a76cf01335f724d154b9b9d394d96/README.md#arguments)）。

小消息基线应查看单次分布和抖动，而不只看平均值；大消息基线应确认样本已进入近似线性区间，并同时保存操作耗时与带宽。若 warm-up 后仍有首次连接、内存注册、算法选择、时钟升频或缓存状态变化，应该把这些现象作为基线条件记录，而不是任意删除“不好看”的样本。

## 单机、多机、拓扑和并发条件

单机结果主要约束节点内路径，多机结果还叠加节点间 NIC、主机/设备到 NIC 的路径、交换网络、路由、拥塞和跨节点同步。即使 rank 数相同，以下任一变化都足以建立新的基线系列：

- 节点数与每节点 rank 数；rank 是否连续或交错放置；
- GPU/NPU、CPU/NUMA、PCIe 根/交换器、NIC 或设备直出端口的映射；
- 节点内互联和节点间网络类型、端口数、bond/rail、MTU、RDMA 模式、路由与交换路径；
- communicator 分组、channel/算法/协议选择和是否存在网络或交换侧聚合/规约卸载；
- 同机计算、存储、其他通信组及其他租户的并发；
- 电源、频率、温度、链路健康、错误、重传和后台维护状态；
- 容器、调度放置、CPU 绑定、设备可见性以及通信库、驱动、固件和运行时版本。

物理关系的记录字段见[计算节点资源与拓扑参考](../01-hardware/resource-topology.md)。若没有端口到 rank 的映射和同时段链路遥测，`busbw` 只能保留为工具模型值，不能定位“哪条链路跑了多少”。若有遥测，也要明确单向/双向、端口/设备/节点聚合、采样窗口和协议开销，再与基准的逻辑 payload 对齐。

并发测试要分开回答两个问题：单个 communicator 在竞争下完成一次操作需要多久，以及共享系统在同一窗口承载了多少总流量。前者用每组操作耗时，后者需要各组时间对齐并结合链路计数器；把各组 `busbw` 相加只能得到模型值之和。

### 跨节点矩阵与 rail 身份记录条件

矩阵轴（记录项，非测量值）：消息大小（`-b/-e/-i/-f` 展开为精确 byte）× 节点数/每节点 rank × rank→设备→NIC/端口映射 × rail 身份（`NCCL_IB_HCA` 选择、`NCCL_CROSS_NIC` 取值及 fabric 是否 rail-optimized、SU/rail/路径记录）× 并发（SPLIT 分组、其他租户/计算/IO 负载）× 健康（错误/重试/超时）。

请求配置、实际库端点/映射证据、IB/RoCE 路径、同窗端口计数器四列分开记录：`NCCL_IB_HCA` 过滤与 `NCCL_CROSS_NIC` 意图（0 同 rail / 1 允许跨 rail / 2 默认兼顾，[NCCL 2.27.5 env](https://docs.nvidia.com/deeplearning/nccl/archives/nccl_2275/user-guide/docs/env.html#nccl-cross-nic)）**不等于**实际选中 NIC/端口及其 fabric 映射——`CROSS_NIC=0` 有例外：各节点 communicator GPU 成员不同时仍可能跨 NIC；algo/proto/channel 数也不代替实际映射。HCCL 的 host socket 选择（`HCCL_SOCKET_IFNAME`）只记录 bootstrap 路径，不证明设备侧 RDMA rail。实际路径缺失时记 unknown。

SU 边界：SuperPOD 一跳事实限**同一 SU 内对应 rail**（[Compute IB fabric](https://docs.nvidia.com/dgx-superpod/reference-architecture-scalable-infrastructure-h100/latest/network-fabrics.html#computeinfiniband-fabric)）；跨 SU 的同 rail 也可能经过 spine；storage fabric 约 4:3 超配（拥塞候选，非路径证据）。

四类候选判据（最小输入/观察/对照/无法判断；复用[T03-03](../../knowledge/03-communication/rdma-baseline-and-congestion-triage.md)“计数器语义”与“停止条件与恢复安排”两节，不重复其内容）：

| 候选 | 输入 | 观察与对照 | 无法判断 |
|---|---|---|---|
| 路径选择/均衡 | 已映射 rail、algo/proto/channel 记录、`NCCL_IB_HCA`/CROSS_NIC 取值 | 按已映射 rail 的预期负载比较方向一致的同窗遥测 | 实际映射缺失时不判路径 |
| 热点 | 多 rank/多节点同条件基线 | 热点**不由单列 busbw 证明**；须同窗端口计数器定位到链路 | 无同窗遥测时不定位链路/rail |
| 多租户争用 | 同条件隔离轮 vs 背景负载轮 | 争用须与同条件隔离/背景负载对照；SPLIT 分组带宽按组解释 | 无对照轮时不判争用 |
| 协议重试 | 已核对含义/范围的重试计数器（T03-03 重传表；validator retries 不互换） | 只用计数器增量判读 | 无计数器时**不得凭吞吐下降推出重试**；单一响应计数不判根因 |

路径选择证据三分：库侧（上表字段）→ RDMA 侧（T03-03 perftest/GID/路由/计数器，见[RDMA 诊断](rdma-baseline-and-congestion-triage.md)）→ 物理侧（UFM/mlx5/Cumulus 同窗 delta＋[成对建基线/换节点隔离/按 rail 隔离](https://docs.nvidia.com/deploy/gpu-debug-guidelines/gpu-node-triage.html#network-testing)对照，可变页，观察日期 2026-10-13）。

## 正确性是性能基线的准入条件

一个性能数值必须先通过该工具在该模式下定义的结果检查，且没有超时、异步错误或被跳过的 rank。固定 `nccl-tests` 默认 `--check 1`，会初始化输入和期望值，在性能测量之外执行检查迭代，统计错误元素；实现把各线程/进程的错误数汇总后写入结果（[`README.md` `--check`](https://github.com/NVIDIA/nccl-tests/blob/b4d5beebca8a76cf01335f724d154b9b9d394d96/README.md#arguments)、[`src/common.cu` data check](https://github.com/NVIDIA/nccl-tests/blob/b4d5beebca8a76cf01335f724d154b9b9d394d96/src/common.cu#L828-L883)）。这只能证明工具生成的该组输入、数据类型、规约操作和检查迭代在当次运行中匹配期望，不等于训练模型数值正确，也不覆盖未检查的性能迭代。

正确性基线至少保存：测试算子、datatype、reduction op、root、消息大小、rank 数与映射、in/out-of-place、check 次数、错误元素数或工具状态、超时/进程退出状态，以及所有跳过或不支持项。以下结果不得纳入“正常性能”分布：

- `#wrong` 非零、HCCL `check_result` 非 success，或检查被关闭/模式不支持；
- 任一 rank 超时、异常退出、重启或没有参与相同 communicator；
- 结果中发生降级、重试或错误，但基线没有单独标注；
- 只得到部分 size 或部分 rank 的输出，却将缺失行填为 0；
- 同一表混入不同 datatype、root、算子、缓冲区模式或拓扑条件。

### 六信号同记（无阈值；完成率与恢复按 T03-03 限定）

正确性（`#wrong`/`check_result`/perftest errors）、错误（异步错误/abort、IB 异步事件）、完成率（分子＝按计划完成的运行/矩阵单元/操作数，分母＝计划尝试数；超时、缺行、跳过、不支持、未校验分开记录——清理残留进程不代表计划测试已完成；分母/证据缺失记 unknown）、时延分布（`-I/-K`；HCCL 在本次所选文档未定义逐次分布，不宣称所有实现都不存在）、吞吐（algbw/busbw 或 alg-only，不互换）、恢复（记录起止事件/观察窗口；零新增**仅限已定义错误列**，正常流量/流控响应按同窗基线带比较，校验须满足覆盖门禁——见[T03-03“停止条件与恢复安排”节](../../knowledge/03-communication/rdma-baseline-and-congestion-triage.md)，仅适用 RDMA 分支的门槛明确限定并链接，collective/应用恢复不由进程退出或计数器一项代替）。MI300X ≥304 GB/s 等厂商门槛**不得**写入本节；如提及仅作"厂商验收示例反例"并标注非本库判据。

## HCCL 输出只能按其自身来源解释

固定 cann-hccl commit `2d685b084a60366b47ad8e50a563ee5c4dbef7fe` 的 README 给出一项 HCCL Test 示例，并明确：`data_size` 是**单个 NPU 上参与集合通信的数据量**，单位 byte；`aveg_time` 是集合通信算子执行耗时，单位 μs；`alg_bandwidth` 单位 GB/s；`check_result=success` 表示示例 AllReduce 功能结果正确（[固定 README“上板测试”](https://gitee.com/ascend/cann-hccl/blob/2d685b084a60366b47ad8e50a563ee5c4dbef7fe/README.md#上板测试)）。同一示例展示单节点 8 NPU、AllReduce、fp32、sum 和消息扫描参数，但它是使用示例，不是本文环境的实测结果或推荐阈值。

该固定 README 没有在所述输出说明中定义 `alg_bandwidth` 的精确公式、是否另有 bus bandwidth、默认 warm-up/iterations、rank 聚合方式、同步边界或各算子的消息换算。因此，本页不把 HCCL 的 `alg_bandwidth` 与 NCCL-tests 的 `algbw` 判为可直接比较，也不把 NCCL 的 `2(n-1)/n` 等系数移植到 HCCL 输出。要比较 HCCL 结果，需另外固定与 CANN/HCCL 配套的 HCCL Test 版本，并从其文档或实现补齐这些字段；无法取得时把统计口径标为 `unknown`。

同一 cann-hccl README 的 α–β 模型把 α 定义为节点间固定时延、β 定义为每 byte 传输时间、γ 定义为每 byte 规约计算时间，并写出单步模型。为避免与前文 rank 数 `n` 混淆，本页将原文数据量符号改为 `m`，即 `D = α + mβ + mγ`；`m` 的单位是 byte，原文节点数另用 `p`。这可用于理解“固定开销 + 随消息量增长的传输/规约成本”，但不能从一条 HCCL Test 输出反推出通用 α、β、γ，也不能代替目标拓扑上的拟合和验证（[固定 README“算法介绍”](https://gitee.com/ascend/cann-hccl/blob/2d685b084a60366b47ad8e50a563ee5c4dbef7fe/README.md#alg_desc)）。

本文不知道任何目标 NPU 机型的链路数、链路速率、端口聚合方式、协议效率或“应达带宽”。这些参数必须来自具体机型与拓扑资料、目标版本文档和现场遥测，不能从 GPU 数值或另一个 Ascend 型号推算。

### HCCL Test 跨节点与计时条件（9.1.X 指南独立口径）

下述只适用于 CANN 9.1.X《HCCL 性能测试工具》指南（0001/0004/0005/0006/0007），不与 NCCL/RCCL 公式互换；凡涉及"HCCL Test × CANN/HDK/机型可运行组合"处记 `blocked_on_evidence/open`（BLOCKED-1），不得用本节参数表关闭。

- 只有算法带宽（[0001](https://www.hiascend.com/doc_center/source/zh/CANNCommunityEdition/910/devaids/hccltool/HCCLpertest_16_0001.html)：带宽＝数据量/耗时，无 bus 列）；`data_size` 为**单个 NPU 数据量**（[0006](https://www.hiascend.com/doc_center/source/zh/CANNCommunityEdition/910/devaids/hccltool/HCCLpertest_16_0006.html)）；`avg_time` 单位 us（0006）；`-b/-e` 默认 64M、`-w 10` 不计统计（[0005](https://www.hiascend.com/doc_center/source/zh/CANNCommunityEdition/910/devaids/hccltool/HCCLpertest_16_0005.html)）；`-n` 有两处不同角色：`mpirun -n <number>` 为 MPI launcher 进程数，工具 `-n <iters_count>` 为迭代次数（0005 命令格式与 MPI/工具两表，不可混用）；`-t/--onlydevicetime` 默认 0 计全部耗时（含 Host 软件与 kernel 加载），置 1 仅计 Device 侧（开启三条件：展开模式 AIV/CCU、`HCCL_BUFFSIZE`>100MB、`-w/-n`≤100；0005）；`-c 0/1/2`（默认 1；0005）与 `check_result`（success/failed/NULL；NULL 两类未校验分支：`-c 0` 未开启，或溢出/超精确表达范围不开启——后者附分算子/数据类型最大卡数表，0006；**NULL 不得洗为正确性通过，通过须 `-c 1/2` 且 success**）；`-p` 从 Device 0 连续选择为 [0007 规格约束](https://www.hiascend.com/doc_center/source/zh/CANNCommunityEdition/910/devaids/hccltool/HCCLpertest_16_0007.html)所述常规分支，另有 [0004](https://www.hiascend.com/doc_center/source/zh/CANNCommunityEdition/910/devaids/hccltool/HCCLpertest_16_0004.html) `HCCL_TEST_USE_DEVS` 指定设备例外；对齐/rank-size 微调警告（0005）。
- 跨节点四字段：总规模由 `mpirun -n <number>`（MPI 进程数）与工具 `-p <npus>`（单节点参与 NPU 数）共同决定；工具 `-n <iters_count>` 仅为迭代次数（与 MPI `-n` 区分，三处一致）；hostfile 双格式（MPICH/OpenMPI）与 A3 超节点集中配置约束；`HCCL_SOCKET_IFNAME` 4 格式（建链网卡，Host 侧，不等于 RDMA rail 身份）；`HCCL_CONNECT_TIMEOUT` 默认 120s（指南示例建议：3K 卡→240s、5K 卡→600s）；`HCCL_BUFFSIZE` 建议大于测试数据量（0004/0005）。
- 计时实现 unknown 收窄为：实现中的具体计时点与跨 rank 归约方式未给出，不得按 NCCL `deltaSec`/`-a` 或 RCCL `×1.0E6` 推定（`-t` 文档契约本身不在 unknown 内）。

## 建立一条可比较基线的最小记录

以下字段同时成立，结果才适合进入同一对照组：

| 类别 | 必填字段 | 比较规则 |
|---|---|---|
| 身份 | 工具仓库/包、固定 commit/tag 或包版本；通信库、驱动、运行时、固件 | 任一关键版本变化均保留为新条件；`latest` 不能作为长期身份 |
| 算子 | collective、datatype、reduction op、root、算法/协议或其未知状态 | 不同算子不共用 `busbw` 阈值；算法未知时不得反推流量路径 |
| 消息 | 精确 payload byte、元素 count、size 列语义、单位、扫描范围与步长 | 按相同 `S` 定义对齐；MiB 与 MB、GB/s 与 Gb/s 分开 |
| 规模 | 总 rank、节点数、每节点 rank、进程×线程×设备布局、communicator/split group | rank 或分组改变时按公式重新解释，不能只按卡数归一化 |
| 缓冲区 | in/out-of-place、地址 offset、对齐、注册、实现模式、graph | 两种 buffer 模式分别保留，不混合择优 |
| 计时 | warm-up、iters、aggregate、cycle、blocking/sync、rank 聚合、设备事件/CPU 时间、分位数算法 | 同一统计口径比较；均值与 max/p99 不互换 |
| 拓扑 | rank→设备→NUMA/PCIe/NIC 映射、节点内互联、网络 rail/端口、路由和共享上游 | 单机与多机分开；拓扑变化另建序列 |
| 并发 | 其他通信组、计算、I/O、租户和维护负载；测试时间窗口 | 空载与带载是不同基线，不能只保留较高者 |
| 健康 | 温度/频率、链路状态、错误/重试、超时、进程退出 | 异常样本保留证据但不混入健康参考分布 |
| 正确性 | check 配置、结果、错误元素数、不支持或跳过项 | 只有在目标模式下通过检查的运行才进入性能基线 |
| 输出 | 每个 size 的原始 `t/algbw/busbw` 或 HCCL 原字段、逐次样本/分布、端口遥测 | 保留原字段，派生值另列公式和单位；缺失写 unknown |

基线应是带环境标签的分布，而不是一个全局常数。建议分别保存小消息操作时间曲线、大消息带宽平台区、重复运行的中位数与尾部、rank/节点扩展曲线，以及对应的错误与链路遥测。报警或验收阈值只能从同机型、同拓扑、同软件和同负载目的的参考分布推导，并记录样本期和变更历史；本文没有给出任何百分比、GB/s 或 μs 的通用及格线。

### 应用→库→RDMA→物理链路工具矩阵（记录口径；参数逐工具归属）

| 层级 | 工具（固定版本，各不互拼） | 记录字段 |
|---|---|---|
| 应用/库 NCCL | nccl-tests b4d5beeb | 每 size 原始 `t/algbw/busbw`、`-a` rank 聚合（0/1/2/3）、`-I/-K` 分布、`NCCL_TESTS_SPLIT` 分组；`-A/-X/-Z` **本快照无此参数**（属 rccl-tests，见下行） |
| 应用/库 RCCL | rccl-tests therock-10.1 | 每 size 原始 `t/algbw/busbw`、`-a` 聚合、`-I/-K` 分布、`-A` 算法身份、`-X/-Z` 机器可读行、SPLIT 分组 |
| 应用/库 HCCL | HCCL Test 9.1.X | 原字段（`data_size/avg_time/alg_bandwidth/check_result`）；`-a` 在此为**特定产品 accelerator 选择**，不得按 NCCL/RCCL 的 rank average 解释；`NCCL_TESTS_SPLIT` 不外推 HCCL；逐次分布在本次所选文档未定义（记 unknown，不宣称所有实现都不存在）；缺字段记 unknown |
| RDMA（verbs/传输） | perftest 26.07.8（T03-03 固定行号；host 后端覆盖门禁，操作数口径） | 两节点/多节点、单流/多流、隔离/争用对照；errors/skips/stale 覆盖门禁（门禁属 perftest host 后端，不作三 collective 工具通用输出） |
| 物理链路 | UFM 4.18.15 / mlx5 v6.16 计数器 / Cumulus 4.3 / netdev ABI（T03-03 已审阅口径） | 同窗 delta、方向/聚合层级、采样窗口、回绕 unknown |
| 主机/设备路径 | [T03-01 互联路径](interconnect-paths.md)（Table 6 GPU-CX-mlx5 联合身份、`nvidia-smi topo`/`aclrtGetDevicesTopo`；版本边界见 [T03-05 正文](rccl-runtime-and-verification.md)、[T03-06 正文](communication-library-profiles.md)及本页[作者来源记录](../../docs/research/batch-19-t03-07-sources.md)）＋ NCCL_TOPO_DUMP_FILE（可选） | rank→设备→NUMA/PCIe/NIC 全链 |

## 来源范围与仍需补齐的证据

- [NVIDIA nccl-tests 固定 README](https://github.com/NVIDIA/nccl-tests/blob/b4d5beebca8a76cf01335f724d154b9b9d394d96/README.md)、[性能说明](https://github.com/NVIDIA/nccl-tests/blob/b4d5beebca8a76cf01335f724d154b9b9d394d96/doc/PERFORMANCE.md)及本文链接的实现文件：核对 rank 计算、单位、算子公式、in/out-of-place 调用、warm-up/iteration、计时同步和 correctness check。固定 commit 是 2026-09-29 对官方 `master` 的只读解析结果；它是证据快照，不是部署版本推荐。
- [Ascend cann-hccl 固定 README](https://gitee.com/ascend/cann-hccl/blob/2d685b084a60366b47ad8e50a563ee5c4dbef7fe/README.md)：核对 HCCL Test 示例输出字段和 α–β 模型；该 commit 同样是官方 `master` 的固定快照。README 自身警告 master 可能与 CANN 版本不配套，因此本文不据此声明任何可运行组合。
- 2026-10-14 加法：[rccl-tests PERFORMANCE](https://github.com/ROCm/rocm-systems/blob/therock-10.1/projects/rccl-tests/doc/PERFORMANCE.md)（六算子修正因子；首段 ms 与实现 us 冲突已标注）、[rccl-tests README 参数节](https://github.com/ROCm/rocm-systems/blob/therock-10.1/projects/rccl-tests/README.md#user-content-arguments)（默认值与聚合口径）、[NCCL 2.27.5 env](https://docs.nvidia.com/deeplearning/nccl/archives/nccl_2275/user-guide/docs/env.html)（`NCCL_CROSS_NIC`/`NCCL_IB_HCA`/多 QP/ALGO-PROTO 调试类）、[SuperPOD fabric](https://docs.nvidia.com/dgx-superpod/reference-architecture-scalable-infrastructure-h100/latest/network-fabrics.html)（rail-aligned/超配）、CANN 9.1.X 指南 0001/0004/0005/0006/0007（算法带宽与跨节点字段；计时实现 unknown；BLOCKED-1 交集保持 blocked）。

仍需补齐：与目标 CANN/HCCL 配套的固定 HCCL Test 文档或实现、目标 GPU/NPU 机型的精确互联规格、端口到 rank 的现场映射、物理链路遥测定义、并发负载和重复样本。本库没有运行 nccl-tests/HCCL Test，没有安装或构建上游项目，也没有产生 GPU/NPU 的 latency、bandwidth、正确性或阈值结果。
