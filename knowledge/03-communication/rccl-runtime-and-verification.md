---
id: communication.rccl-runtime-and-verification
title: RCCL 运行条件、观测与最小验证档案
type: reference
domain: communication
status: draft
platforms: [generic, amd]
source_refs:
  - src.amd.rccl-docs-10.1.0
  - src.rocm.rocm-systems-therock-10.1
  - src.rocm.rocm-systems-pr-9745
  - src.amd.rocm-compatibility-matrix-10.1.0
  - src.amd.rocm-release-notes-10.1.0
  - src.amd.instinct-mi300x-system-acceptance-2026-10-09
updated_at: "2026-10-14"
summary: "以 RCCL 2.30.7（docs-10.1.0）＋ rocm-systems therock-10.1 ＋ MI300X 文档条件为独立样板，给出通信接口、初始化映射、返回/完成/错误语义、日志与环境开关、rccl-tests 计时校验口径、两节点最小验证设计与 PR #9745 来源整理；NCCL 相似处只作对照；整栈已测组合缺口如实保留 unknown。"
related_ids:
  - communication.collectives-and-rank-progress
  - communication.communication-library-profiles
  - communication.rdma-baseline-and-congestion-triage
  - hardware.resource-topology
applicability:
  environment_refs: []
  notes: "尚无环境档案：样板交集为文档各自支持（RCCL 2.30.7 docs-10.1.0、rocm-systems tag therock-10.1 commit 7da4302、ROCm 10.1.0 兼容矩阵 MI300X/gfx942 × Ubuntu 24.04.5 × amdgpu 31.60.0）；无单页证明该五元为已测组合，不作部署组合声明。目标设备/主机/驱动组合需另行固定。"
verification:
  status: source_checked
  evidence_refs:
    - src.amd.rccl-docs-10.1.0
    - src.rocm.rocm-systems-therock-10.1
    - src.rocm.rocm-systems-pr-9745
  notes: "对照第十九批取证记录（docs/research/batch-19-rccl-sources.md）所列固定版本来源核对；作者核对范围：docs-10.1.0 别名 6 页（首页/spec/api/env/fault-tolerance/troubleshooting/usage-tips）、therock-10.1 树与 tag commit、兼容矩阵、acceptance 页（latest 可变）、PR #9745 API 正文；审阅方独立取证（group.cc、common.cu/util.cu 行号、PR merge commit 等）见审阅报告，不冒充作者当时已完成；latest 与别名未逐页 diff；PR #9745 最早入版与 hang 机理调用栈未证；未在任何 AMD 硬件上执行验证。"
---

# RCCL 运行条件、观测与最小验证档案

## 范围与阅读方式

本文只做一件事：给出 AMD/RCCL 侧"作业 traffic 经过哪些软件层、每层如何观察、坏了看哪里"的版本化档案。样板独立于 NCCL/HCCL——集合语义通用模型见[集合通信与 rank 进度](collectives-and-rank-progress.md)，其 NCCL 2.27.5 结论不继承到本样板。

硬边界：**样板交集 ≠ 已测部署组合**。下文五元（RCCL 2.30.7、ROCm 10.1.0、MI300X、Ubuntu 24.04.5、amdgpu 31.60.0）来自各文档自支持集，无任何单页证明其组合已测；引用一律写"文档各自支持的样板交集"。三库并列见[通信库能力档案](communication-library-profiles.md)。

## 固定样板

| 维度 | 固定值 | 出处 |
|---|---|---|
| RCCL 文档 | 2.30.7（`docs-10.1.0` 别名，本轮复核可达） | [RCCL 首页](https://rocm.docs.amd.com/projects/rccl/en/docs-10.1.0/index.html) |
| RCCL 源码/测试 | rocm-systems tag `therock-10.1`（commit `7da4302`） | [projects/rccl](https://github.com/ROCm/rocm-systems/tree/therock-10.1/projects/rccl)（旧 `ROCm/rccl` 已退役，页有搬迁横幅） |
| ROCm 版本 | Core SDK 10.1.0（组件表 RCCL 2.30.7 → therock-10.1 树） | [兼容矩阵](https://rocm.docs.amd.com/en/docs-10.1.0/compatibility/compatibility-matrix.html)（页为 JS 选择器，MI300X 数据在 HTML 条件块） |
| 设备/主机 | MI300X（CDNA3/gfx942）× Ubuntu 24.04.5（GA 6.8）× amdgpu 31.60.0 | 同上（三表各自支持；驱动与 ROCm 用户态为两个版本序列） |
| 健康基线 | `all_reduce_perf -b 8 -e 8G -f 2 -g 8` bus BW ≥304 GB/s（Ubuntu 22.04 样例） | [MI300X system acceptance](https://instinct.docs.amd.com/projects/system-acceptance/en/latest/gpus/mi300x.html)（latest 可变页，引用带观察日期，不作固定判据） |

## 接口、初始化与 rank/device 映射

- 建连：`ncclGetUniqueId`（单 rank 生成→分发全员）→ 各 rank 先设 HIP device → 普通 `ncclCommInitRank(nranks, commId, rank)`（rank 0..n-1，clique 内唯一，隐式同步）**或**带配置 `ncclCommInitRankConfig(nranks, commId, rank, config)`（`ncclConfig_t *config`，`NCCL_CONFIG_INITIALIZER` 初始化；`blocking` 等字段见 Communicator Configuration）；单进程用 `ncclCommInitAll`（devlist 顺序即用户 rank 序，无 config 参数）；查询 `ncclCommCount/CommCuDevice/CommUserRank`。（[library-specification](https://rocm.docs.amd.com/projects/rccl/en/docs-10.1.0/api-reference/library-specification.html) Communicator functions 节；[api-library](https://rocm.docs.amd.com/projects/rccl/en/docs-10.1.0/api-reference/api-library.html) Communicator Configuration 与 InitRankConfig）
- 措辞冲突照录：`ncclCommInitRank` 段残留"CUDA device"字样，以 `ncclCommCuDevice`（ROCm device index）为准；root 均为 rank 非 device。
- 原语：all-reduce/all-gather/reduce/broadcast/reduce-scatter/gather/scatter/all-to-all（`ncclAllToAll` 已 deprecated，用 `ncclAlltoAll`；`ncclBcast` 已 deprecated，用 `ncclBroadcast`）＋ send/recv 初步支持。（[api-library](https://rocm.docs.amd.com/projects/rccl/en/docs-10.1.0/api-reference/api-library.html)）
- 返回/完成（五态分列）：(a) 普通阻塞调用成功返回 = 已入队 hip stream，不等于设备完成；(b) group 内单次调用在 `ncclGroupEnd` 前只暂存，未提交；(c) 最外层 `ncclGroupEnd` 在阻塞分支返回成功 = 组内调用已提交/入队；(d) **进入后台 group job 分支、返回 `ncclInProgress` 时**（源码条件：non-blocking **且**有 preconnect/async job，[group.cc L919–958](https://github.com/ROCm/rocm-systems/blob/7da43026e4f2ef7600433c38c820732f7a205d22/projects/rccl/src/group.cc#L919-L958)；其他分支可正常返回成功——返回值判断不被模式标签替代）：此时不得凭主机返回把依赖操作或 event 当作已排在通信之后——须 `ncclCommGetAsyncError` poll 至离 `ncclInProgress`（`ncclSuccess` 后）再建立依赖，CPU 让出等待，错误分支按 (e) 处理；(e) 设备完成按 HIP stream/event 语义另行判断。`ncclSend/Recv` 要求对端同 datatype+同 count，GPU 侧阻塞，并发必须 group 融合。
- 错误：`ncclResult_t` 9 码（含 `ncclInProgress`/`ncclTimeout`；`ncclUnhandledCudaError` 实为 HIP 错误）；仅 `ncclInvalidArgument` 非致命，fatal 污染同 group 全 communicator；网络故障经 `ncclCommGetAsyncError` 滞后上报；clean 关机 `Finalize→poll→Destroy`。（[fault-tolerance](https://rocm.docs.amd.com/projects/rccl/en/docs-10.1.0/how-to/fault-tolerance.html)）
- 恢复前提（不可省略）：容错要求 communicator 以 non-blocking 模式创建（`config.blocking=0`；此时除 `ncclCommDestroy/Abort` 外所有调用立即返回）；`ncclCommAbort` 调用时**不得有线程位于 RCCL 调用中**；对称内存路径无 proxy、无 device 侧超时，对端缺席时 `GetAsyncError`/超时永不报告，abort 须由调用方自己的 deadline 或带外 watchdog 驱动（`hipStreamSynchronize` 会永久 hang）。坏态用 `Abort`，之后 shrink 掉失败 rank 或重建。
- 边界：对称内存路径无 proxy、无 device 侧超时，对端缺席时 abort 须由调用方 deadline 驱动（`hipStreamSynchronize` 会永久 hang）；`revoke/shrink/grow` 流程与约束见同页。

## NCCL 相似 ≠ 等价（对照专用五点）

RCCL"继承 NCCL 错误模型＋AMD 扩展"，以下差异禁止当作等价证据：`NCCL_PXN_C2C` 上游默认 1、RCCL 保持 0（C2C 路径 NVIDIA 专用）；`NVLS` 子系统对 RCCL 无效；MSCCL/MSCCL++ 已移除（符号留空 no-op 保链接）；GIN v14 类型重编号；`ncclCommCuDevice` 为 ROCm device index（见上节措辞冲突）。（[env-variables](https://rocm.docs.amd.com/projects/rccl/en/docs-10.1.0/api-reference/env-variables.html) PXN/NVLS 行；[CHANGELOG](https://github.com/ROCm/rocm-systems/blob/therock-10.1/projects/rccl/CHANGELOG.md) 2.30.4/2.28.3 Removed 节）

## 日志、环境开关与观测

- `NCCL_DEBUG` 默认 ERROR（NONE/ERROR/VERSION/WARN/INFO；TRACE 需 ENABLE_TRACE 构建）；`VERSION` 打印 `librccl` 版本（设后跑 rccl-tests 即得版本）；`NCCL_DEBUG_FILE` 用 `%h.%p` 防交错（`%h`=hostname、`%p`=pid，与 rank 的关联靠启动行/合并清单建立，不自动等于 rank 号）；子系统变量全名是 `NCCL_DEBUG_SUBSYS`（写 `SUBSYS=` 不生效），默认 `INIT,BOOTSTRAP,ENV`，`NVLS` 对 RCCL 无效；对称内存确认看 `INIT` 日志对应行。
- 按目的采集（何时开采）：初始化/NIC 问题用 `NCCL_DEBUG=INFO` + `NCCL_DEBUG_SUBSYS=INIT,BOOTSTRAP,NET`（含 `Local Net device counts min/max` 行）；调优确认用 `NCCL_DEBUG_SUBSYS=INIT,TUNING,COLL`（实际 channels/algo/proto）；collective 时间线/Replayer 用 `NCCL_DEBUG_SUBSYS=COLL`（只设 COLL 采不到初始化期 NIC 日志）。MPI 远端环境变量传递按所选 launcher 条件记录，不假设 shell 变量必然传播到所有节点。
- `NCCL_CHECK_MODE`（`DEBUG_GLOBAL` 每次 group launch 加 bootstrap all-gather，禁生产；`NCCL_CHECK_POINTERS` 已废弃）；`NCCL_IGNORE_NET_MISMATCH` 默认 1 继续、`0` 即 `ncclSystemError`（初始化期 min/max 日志样例见 troubleshooting）；`NCCL_ALGO/PROTO` 覆盖自动选择；`NCCL_LAUNCH_ORDER_IMPLICIT` 多 communicator 定序（默认关）。（[env-variables](https://rocm.docs.amd.com/projects/rccl/en/docs-10.1.0/api-reference/env-variables.html)）
- 采集清单：`/opt/rocm/.info/version`、`rocm_agent_enumerator`、`rocminfo`、`amd-smi*`、`hipconfig --full`、`ibv_devinfo`/`rdma link`、`ldd librccl.so`、`NCCL_DEBUG=VERSION/INFO`；Replayer 三步（per-rank `%h.%p` 日志→合并→`mpirun rcclReplayer`）；性能三件套 TransferBench/RCCL UT/rccl-tests（含 `sysctl kernel.numa_balancing=0`）；NIC 数量不一致初始化期检测。（[troubleshooting](https://rocm.docs.amd.com/projects/rccl/en/docs-10.1.0/how-to/troubleshooting-rccl.html)）
- 版本化行为变更（MI350X 调优，MI300X 样板引用作版本差异证据）：RCCL 2.30.4（ROCm 7.14）MI350X 多节点默认 64→48 ch，10.0 起恢复 64（以 `NCCL_DEBUG=INFO` + `NCCL_DEBUG_SUBSYS=INIT,TUNING,COLL` 确认实际值）；`<8 GPU` 时 `NCCL_MIN_NCHANNELS=32`；CPX+NPS4（MI300X）vs DPX+NPS2（MI350X）。（[usage-tips](https://rocm.docs.amd.com/projects/rccl/en/docs-10.1.0/how-to/rccl-usage-tips.html)）

## rccl-tests 计时/校验口径（固定 tag therock-10.1）

host `steady_clock` 主计时（[`timer.cc`](https://github.com/ROCm/rocm-systems/blob/therock-10.1/projects/rccl-tests/src/timer.cc)，默认路径）；`deltaSec`→`getBw`→`algbw/busbw`；输出 time 列单位是**微秒**（`timeUsec = 秒×1.0E6`，[common.cu](https://github.com/ROCm/rocm-systems/blob/7da43026e4f2ef7600433c38c820732f7a205d22/projects/rccl-tests/src/common.cu#L1259-L1266)；表头 `(us)`，[util.cu](https://github.com/ROCm/rocm-systems/blob/7da43026e4f2ef7600433c38c820732f7a205d22/projects/rccl-tests/src/util.cu#L780-L787)）——[`doc/PERFORMANCE.md`](https://github.com/ROCm/rocm-systems/blob/therock-10.1/projects/rccl-tests/doc/PERFORMANCE.md) 写 ms 与实现冲突，**以实现为准**，该文档句记来源冲突。默认每操作归一化（`normalizeElapsedPerIter`，`-m` 聚合计入）；MPI 多 rank 结果聚合 `-a`（0=Rank0/1=Avg/2=Min/3=Max，默认 1，[README](https://github.com/ROCm/rocm-systems/blob/therock-10.1/projects/rccl-tests/README.md)）；device 实现核（`-D≠0`）报 wall/kernel 时间，`cputimeSec` 为主机侧（common.cu 注释）。`-C`（CPU 时间）、`-I`（per-iter HIP event）、`-G`（HIP graph 回放）是另外口径，不概括为默认模式。

本设计只用默认模式单次运行（最终命令与参数声明一致，执行前选定并记入完整命令；全文采用默认 Float/Sum/双 placement，不混示例）：`all_reduce_perf -d float -o sum -n 20 -w 1 -m 1 -b 8 -e 1G -f 2 -g 1 -c 1`（`-d` 默认 Float、`-o` 默认 Sum、`-O` 省略即默认双 placement（in-place 与 out-of-place 各输出行；`-O 0/1` 只跑其一，不得误读 `both` 为取值）；`-n` 默认 20、`-w` 默认 1；`-c 1` 为默认：计时后重初始化 buffer 再跑一遍 collective 做 datacheck，**与计时分离**；重跑校验不证明每个计时迭代的输出都已校验）。`-c 0` 时 `#wrong` 列为 `N/A`，不得当零错误读。预期扫描行/placement：`-b/-e/-f` 扫描各尺寸行（in-place 与 out-of-place 两组输出行）；实际输出核对要求：行数齐全、无缺行、无提前停止、校验实际开启（`#wrong` 列为数值非 `N/A`）；缺行、N/A、提前停止或未完成计划一律不判 P1。

退出与门限：`NCCL_TESTS_MIN_BW` 从环境继承（未设则 -1，不过滤）；退出失败条件 = `errors≠0` **或** `bw < 0.9×设置值`（common.cu 尾部）。因此设计必须记录该环境项当时值（本设计要求 unset 并记录）；同一命令的非零退出含义随环境改变。判据四分：校验失败（`#wrong≠0`/越界）/ 带宽门限失败（设阈值且 `FAILED`）/ 程序错误（非零退出无 wrong）/ 无法判断（见下）。

修正因子（`doc/PERFORMANCE.md`，设计目标口径）：`algbw=S/t`，busbw AllReduce `2(n-1)/n`、RS/AG/AlltoAll `(n-1)/n`、Bcast/Reduce `1`（busbw 对标硬件峰值、与 rank 数无关）。构建：`make MPI=1`（或 cmake `-DUSE_MPI=ON`），无 MPI 构建不得跑跨节点；1 proc/GPU（`mpirun -np 8 --bind-to numa … -g 1`）。

## 上游案例整理：PR #9745（非本库实测）

- 作者观测：`WindowRegisterSingleRankNonSymTeardown` 在 gfx908/MI100、`NCCL_CUMEM_ENABLE=0` 非对称路径、`ncclCommWindowRegister` 内无限 hang。
- 原因证据：PR #8341 超时 30s→300s 暴露旧 hang ＋ 7 commit×3 run bisect（gfx950 上 34–37s 持平）；hang 机理调用栈未给，机制记 unknown。
- 反例：gfx950 不受影响的分项计时表。
- 修复：arch allowlist skip（[`RegisterTests.cpp` L55–66/L574–581/L671](https://github.com/ROCm/rocm-systems/blob/therock-10.1/projects/rccl/test/RegisterTests.cpp)）＋ CI 超时 300s；修复在 `therock-10.1` 样本存在已验，**最早入版 release 未证**（[CHANGELOG](https://github.com/ROCm/rocm-systems/blob/therock-10.1/projects/rccl/CHANGELOG.md) 2.30.4 已解决列表无此条）。（[PR #9745](https://github.com/ROCm/rocm-systems/pull/9745)）

## 两节点最小验证设计（待执行）

前置：2 节点 × 8×MI300X，Ubuntu 24.04.5，amdgpu 31.60.0，ROCm 10.1.0（RCCL 2.30.7）；MPI 实现与两节点分配（`mpirun -np 16 -N 8`，节点名/hostname、local rank→device、NET transport/HCA/端口逐轮记录）；`ibv_devinfo`/`rdma link` 只证明 RDMA 设备存在，**不证明本次 RCCL 走了 RDMA**，实际路径须上述 transport 记录确认，否则 RDMA 分支记未确认；`NCCL_DEBUG=VERSION` 先确认两端 `librccl` 同为 2.30.7；`NCCL_TESTS_MIN_BW` 记录当时值（要求 unset）。

- 构建：`make MPI=1 MPI_HOME=/path/to/mpi HIP_HOME=/opt/rocm NCCL_HOME=/opt/rocm`（`GPU_TARGETS=gfx942` 可选）。
- 命令（单次运行，计时＋重跑校验同调用，参数与上节一致）：`mpirun -np 16 -N 8 --bind-to numa ./build/all_reduce_perf -d float -o sum -n 20 -w 1 -m 1 -b 8 -e 1G -f 2 -g 1 -c 1`。
- 判据：P1 通过 = 两端 exit 0 **＋** 全部计划行完成（in-place/out-of-place 两组扫描行齐全）**＋** 校验实际开启（`#wrong` 数值列）**＋** `#wrong`=0 且页脚无越界（`Avg bus bandwidth … OK` 只在设阈值时出现；**不设阈值时无性能门限**，busbw 只与同配置基线比，无基线则未判定——≥304 GB/s 口径为单节点单进程八 GPU 扫描至 8G，不作两节点同量级目标；正确性通过与性能未判定分开）；F1 失败 = 任一 rank 非零退出/`#wrong≠0`；hang 按 B-hang 等待约束处理，不直接记失败。
- 有限等待/停止：`-T` 默认关闭（工具 timeout 不覆盖全程），总体等待约束 = B-hang 预声明期限（执行前声明 wall-clock 上限，期限届满仍未结束即停采保留证据）；F1/超时/证据不足三分：测试失败、原因未知、证据不足。
- 无法判断分支：B-hang（启动前即保留联合子系统日志：`NCCL_DEBUG_SUBSYS=INIT,BOOTSTRAP,NET` 存启动日志 **＋** `NCCL_DEBUG_SUBSYS=COLL` 跟时间线；或先读另存的启动日志再分析 COLL 时间线；先查启动日志的 `Local Net device counts min/max`，缺启动证据时该检查记无法判断，不把无日志当 NIC count 一致；对齐 T03-04 时间线，记 unknown）；B-slow（先确认实际 channels/algo/proto，再单节点同命令对照分离节点内/跨节点退化；`HSA_NO_SCRATCH_RECLAIM` 为 MI200 专项，不用于 MI300X）；B-ver（两端 VERSION 不一致即停测，记 blocked_on_evidence）；B-env（输入超出矩阵支持集只记录不外推）。

## 来源与待确认问题

- [RCCL 2.30.7 文档](https://rocm.docs.amd.com/projects/rccl/en/docs-10.1.0/index.html)（`docs-10.1.0` 别名；latest 未逐页 diff）；[rocm-systems therock-10.1](https://github.com/ROCm/rocm-systems/tree/therock-10.1/projects/rccl)（rccl/rccl-tests 固定源码）；[兼容矩阵](https://rocm.docs.amd.com/en/docs-10.1.0/compatibility/compatibility-matrix.html)；[MI300X acceptance](https://instinct.docs.amd.com/projects/system-acceptance/en/latest/gpus/mi300x.html)（latest 可变，带观察日期）。
- 逐条主张与证据定位见[第十九批 RCCL 来源记录](../../docs/research/batch-19-rccl-sources.md)。
- 待确认：latest/别名 diff；"CUDA device"残留措辞官方澄清；PR #9745 最早入版与 hang 机理；MI350 LL 协议问题影响面；整栈已测组合（U1）；仓库根许可；GitHub API 限流未查项。
