---
id: communication.communication-library-profiles
title: 三套通信库能力与版本条件档案
type: reference
domain: communication
status: draft
platforms: [generic, nvidia, amd, ascend]
source_refs:
  - src.nvidia.nccl-user-guide-2.27.5
  - src.nvidia.nccl-tests-b4d5beeb
  - src.pytorch.distributed-2.8
  - src.pytorch.hip-notes-2.6
  - src.rocm.rocm-systems-therock-10.1
  - src.amd.rccl-docs-10.1.0
  - src.huawei.hccl-api-cann-8.0-rc1-alpha003
  - src.huawei.hccl-user-guide-cann-8.1-rc1-alpha001
  - src.huawei.hccl-perf-test-guide-cann-9.1.x
  - src.ascend.cann-hccl-2d685b08
updated_at: "2026-10-14"
summary: "NCCL 2.27.5、RCCL 2.30.7、HCCL（8.0 API ∥ 8.1 指南 ∥ 9.1.X Test 三线分立）三套通信库的能力对照：原语、框架后端、硬件/驱动/运行时、网络路径、初始化、错误/完成、诊断工具逐库独立取证；HCCL Test 与目标 CANN/HDK/机型交集无官方材料，保持 blocked_on_evidence/open。"
related_ids:
  - communication.collectives-and-rank-progress
  - communication.rccl-runtime-and-verification
  - communication.rdma-baseline-and-congestion-triage
  - hardware.resource-topology
applicability:
  environment_refs: []
  notes: "尚无环境档案：三库版本各自独立（NCCL 2.27.5 归档；RCCL 2.30.7 docs-10.1.0 + therock-10.1；HCCL 三件分属 8.0/8.1/9.1.X），不拼成同一环境或部署组合。目标库/版本/硬件组合需另行固定。"
verification:
  status: source_checked
  evidence_refs:
    - src.nvidia.nccl-user-guide-2.27.5
    - src.nvidia.nccl-tests-b4d5beeb
    - src.amd.rccl-docs-10.1.0
    - src.huawei.hccl-api-cann-8.0-rc1-alpha003
  notes: "对照第十九批取证记录（docs/research/batch-19-t03-06-sources.md）所列固定版本来源核对；作者核对轮次：首轮（既有登记存在性、plain-fetch 可达性、HCCL PDF 存活/长度头）＋本轮（两份 HCCL PDF 全文提取验证、troubleshooting 锚点核对）；审阅方独立取证（两份 PDF 全文渲染与双页码、NCCL 八页、PyTorch HIP 2.6、Test 静态正文、CANN 静态正文）见[补充初审](../../docs/research/batch-19-t03-06-codex-review.md)，正文引用其定位时按记录角色注明，不冒充作者当时已完成；RCCL 列取证见 [T03-05 研究记录](../../docs/research/batch-19-rccl-sources.md)；HCCL 9.1.X Test 普通入口曾返回异题页面，内容以 910 静态正文为准；HCCL Test×CANN/HDK/机型交集无官方材料，保持 blocked_on_evidence/open；未在任何硬件上执行验证。"
---

# 三套通信库能力与版本条件档案

## 范围与阅读方式

本文只做一件事：把 NCCL、RCCL、HCCL 的接口与支持条件并列——每库一行版本档案，各自选定证据样板；概念同名（communicator/group、rank、stream、all-reduce）**不直接等价**，跨库结论不互推。集合语义通用模型见[集合通信与 rank 进度](collectives-and-rank-progress.md)；RCCL 运行细节见[RCCL 档案](rccl-runtime-and-verification.md)；独立网络基线见[RDMA 诊断](rdma-baseline-and-congestion-triage.md)。

硬边界：**三库版本不拼部署组合**。 NCCL 2.27.5（归档）∥ RCCL 2.30.7（docs-10.1.0＋therock-10.1）∥ HCCL（8.0 API ∥ 8.1 用户指南 ∥ 9.1.X Test ∥ 源码快照 2d685b08）各自独立；HCCL 三件分属三条版本线（8.0/8.1/9.1.X，见版本档案表），任何跨线组合须自洽交集证据，否则记 blocked。

## 版本档案（一库一行）

| 库 | 档案版本 | 出处 |
|---|---|---|
| NCCL | User Guide 2.27.5（归档 URL 固定）＋ nccl-tests `b4d5beeb` | [2.27.5 指南](https://docs.nvidia.com/deeplearning/nccl/archives/nccl_2275/user-guide/docs/)；[nccl-tests README](https://github.com/NVIDIA/nccl-tests/blob/b4d5beebca8a76cf01335f724d154b9b9d394d96/README.md)（固定 commit） |
| RCCL | 文档 2.30.7（`docs-10.1.0` 别名）＋ rocm-systems tag `therock-10.1`（commit `7da4302`） | [RCCL 2.30.7](https://rocm.docs.amd.com/projects/rccl/en/docs-10.1.0/index.html)；[therock-10.1](https://github.com/ROCm/rocm-systems/tree/therock-10.1/projects/rccl) |
| HCCL | API 文档样板 8.0.RC1.alpha003（文档 01，2024-06-06）∥ 用户指南 8.1.RC1.alpha001（文档 01，2025-03-19）∥ Test 指南 9.1.X（910 路径，2026-09-30 观察）∥ 源码快照 `2d685b08` | 三 PDF/页各自登记；redirect 浮动（本轮指向 910beta3）**不可作版本证据** |

## 能力对照表

| 能力行 | NCCL（2.27.5＋nccl-tests） | RCCL（2.30.7＋rccl-tests） | HCCL（8.0 API ∥ 8.1 指南 ∥ 9.1.X Test） |
|---|---|---|---|
| 原语 | AllReduce/Broadcast/Reduce/AllGather/ReduceScatter＋p2p 五模式（sendrecv/scatter/gather/all-to-all/neighbor exchange）；collective 同 count+datatype 否则未定义（[collectives](https://docs.nvidia.com/deeplearning/nccl/archives/nccl_2275/user-guide/docs/usage/collectives.html)、[p2p](https://docs.nvidia.com/deeplearning/nccl/archives/nccl_2275/user-guide/docs/usage/p2p.html)） | all-reduce/all-gather/reduce/broadcast/reduce-scatter/gather/scatter/all-to-all（`ncclAllToAll`→`ncclAlltoAll` deprecated）＋send/recv 初步支持（[api-library](https://rocm.docs.amd.com/projects/rccl/en/docs-10.1.0/api-reference/api-library.html)） | collective（AllReduce/Broadcast/AllGather/ReduceScatter/AlltoAll 等，清单非穷举）＋C++ P2P：`HcclSend/Recv` 配对同步调用、`HcclBatchSendRecv`（同卡收发异步不阻塞，卡间同步须一一对应；[8.0 §3.4.1–3.4.3](https://www.hiascend.com/doc_center/source/zh/CANNCommunityEdition/80RC1alpha003/apiref/hcclapiref/CANN%208.0.RC1.alpha003%20%E9%9B%86%E5%90%88%E9%80%9A%E4%BF%A1%E6%8E%A5%E5%8F%A3%E5%8F%82%E8%80%83%2001.pdf#page=56)）＋`HcclBarrier`、`HcclAlltoAllV`（变长，[8.1 §4](https://www.hiascend.com/doc_center/source/zh/CANNCommunityEdition/81RC1alpha001/devguide/hccl/hcclug/CANN%E7%A4%BE%E5%8C%BA%E7%89%88%208.1.RC1.alpha001%20%E9%9B%86%E5%90%88%E9%80%9A%E4%BF%A1%E7%94%A8%E6%88%B7%E6%8C%87%E5%8D%97%2001.pdf#page=17)）＋错误查询 `HcclGetCommAsyncError`（当前版本仅返回 `HCCL_E_REMOTE`，[8.0 §3.5.1](https://www.hiascend.com/doc_center/source/zh/CANNCommunityEdition/80RC1alpha003/apiref/hcclapiref/CANN%208.0.RC1.alpha003%20%E9%9B%86%E5%90%88%E9%80%9A%E4%BF%A1%E6%8E%A5%E5%8F%A3%E5%8F%82%E8%80%83%2001.pdf#page=59)）；Python send/receive 配对约束＋跨 Server 物理 id 相同条件（仅 Python 图接口 §2.4.6/2.4.7，印刷 p26–27/物理 p32–33；**不外推为 C++ 条件，C++ 跨 Server 映射不受此句支持也不反向断言任意映射受支持**）；算法名（Ring/Mesh/HD 等）≠原语，批量局部异步不提升为统一主机返回语义 |
| 框架后端 | PyTorch `nccl` 后端（GPU-only 能力矩阵；[取舍规则](https://docs.pytorch.org/docs/2.8/distributed.html)）；NCCL 相似 API 不构成跨库等价 | ROCm 上后端名为 `nccl`/`gloo`（[PyTorch HIP 2.6](https://docs.pytorch.org/docs/2.6/notes/hip.html)；底层库/二进制实际加载（`librccl.so` 核对）与版本配套是不同事实，不拼 PyTorch 2.8 × RCCL 2.30.7 已测组合；[RCCL PyTorch CPX 说明](https://rocm.docs.amd.com/projects/rccl/en/docs-10.1.0/how-to/rccl-usage-tips.html)为有限接入证据） | C 语言接口用于单算子模式框架适配（HCCL 单算子 API 嵌入 PyTorch 后端，用户用 PyTorch 原生集合 API），Python 接口用于图模式（TensorFlow）（[8.1 概述 §1](https://www.hiascend.com/doc_center/source/zh/CANNCommunityEdition/81RC1alpha001/devguide/hccl/hcclug/CANN%E7%A4%BE%E5%8C%BA%E7%89%88%208.1.RC1.alpha001%20%E9%9B%86%E5%90%88%E9%80%9A%E4%BF%A1%E7%94%A8%E6%88%B7%E6%8C%87%E5%8D%97%2001.pdf#page=7)）；TorchNPU 实际加载路径 unknown，不反推 |
| 硬件/驱动/运行时 | CUDA 设备＋驱动（GDRDMA 需 `nvidia-peermem`/DMA-BUF）；**不声明与某 CUDA/驱动配套** | MI300X（CDNA3/gfx942）× Ubuntu 24.04.5 × amdgpu 31.60.0（各自支持，无整栈声明） | Atlas A2/训练系列/300I Duo；固件驱动按产品×CANN 查；CANN/HDK 精确交集见 blocked 项 |
| 网络路径 | PCIe/NVLink/IB Verbs/IP sockets＋CollNet | PCIe/xGMI（RCCL 首页）；节点间按 troubleshooting 采集确认 | HCCS/RoCE/PCIe；Server 内外算法区分 |
| 初始化信息 | UniqueId 广播＋static rank→device＋InitAll 限单进程；多 communicator：隐式总序关闭时（默认 0）由调用方经显式 CUDA stream 依赖/同步维持跨 communicator 一致总序；2.26+ 隐式总序须显式启用 `NCCL_LAUNCH_ORDER_IMPLICIT`（启用后各设备主机发起顺序仍须匹配，否则死锁；CUDA 12.3+ 才允许重叠执行，低版本串行）；PyTorch 侧另有创建/执行/async 跨组条件（下表） | UniqueId→HIP device→InitRank/InitAll；带配置走 `ncclCommInitRankConfig`（`NCCL_CONFIG_INITIALIZER`）；devlist 顺序即 rank 序；RCCL 多 communicator 约束不由 NCCL 文档推出 | C++ 通信域初始化→建链→执行→销毁见下表（[8.1 四阶段](https://www.hiascend.com/doc_center/source/zh/CANNCommunityEdition/81RC1alpha001/devguide/hccl/hcclug/CANN%E7%A4%BE%E5%8C%BA%E7%89%88%208.1.RC1.alpha001%20%E9%9B%86%E5%90%88%E9%80%9A%E4%BF%A1%E7%94%A8%E6%88%B7%E6%8C%87%E5%8D%97%2001.pdf#page=9)；[8.0 为三阶段](https://www.hiascend.com/doc_center/source/zh/CANNCommunityEdition/80RC1alpha003/apiref/hcclapiref/CANN%208.0.RC1.alpha003%20%E9%9B%86%E5%90%88%E9%80%9A%E4%BF%A1%E6%8E%A5%E5%8F%A3%E5%8F%82%E8%80%83%2001.pdf#page=7)；world/custom group 与 rank 重编号（8.0 rank 概念） |
| 错误/完成 | 8 值（[Types](https://docs.nvidia.com/deeplearning/nccl/archives/nccl_2275/user-guide/docs/api/types.html#ncclresult-t)：`ncclSuccess`＋`ncclInProgress`＋6 类错误含 `ncclRemoteError`；Success/InProgress 不是错误；communicators 摘要表只有七行，漏 RemoteError——行数不作完整计数）＋异步轮询＋nonblocking 中止；stream/event 语义＋nonblocking group `ncclInProgress`；PyTorch Work 分支（见 T03-04） | 9 码＋`ncclInProgress` poll＋`ncclTimeout`（RCCL 扩展值；两库按 Success/InProgress/错误分母一致比较，不从摘要表推导类型不存在）；fatal 污染同组；non-blocking 创建＋Abort 线程前提＋调用方 deadline（RCCL 档案五态） | 单卡与链路问题均可致集群大量超时、全组日志定位（8.0 p9）；HCCL 主机返回统一边界 **unknown** |
| 诊断工具 | NCCL_DEBUG*/RAS/troubleshooting 分支（[Errors](https://docs.nvidia.com/deeplearning/nccl/archives/nccl_2275/user-guide/docs/troubleshooting.html#errors)、[RAS](https://docs.nvidia.com/deeplearning/nccl/archives/nccl_2275/user-guide/docs/troubleshooting.html#ras)、[GPU Direct](https://docs.nvidia.com/deeplearning/nccl/archives/nccl_2275/user-guide/docs/troubleshooting.html#gpu-direct)、[Topology](https://docs.nvidia.com/deeplearning/nccl/archives/nccl_2275/user-guide/docs/troubleshooting.html#topology-detection)）＋nccl-tests 口径（`-b/-e/-f/-n/-w/-c`，algbw/busbw，[PERFORMANCE](https://github.com/NVIDIA/nccl-tests/blob/b4d5beebca8a76cf01335f724d154b9b9d394d96/doc/PERFORMANCE.md)） | NCCL_DEBUG*/Replayer/TransferBench/UT/rccl-tests（`-c` 默认 1，us 口径，MIN_BW 门限；RCCL 档案） | HCCL Test（9.1.X：只有算法带宽；`-b/-e` 默认 64M、`-n` 20、`-w` 10；计时实现 unknown）＋用户指南 EI0002/§9.1.2；[cann-hccl](https://gitee.com/ascend/cann-hccl/blob/2d685b08/README.md) LLT `--test`（**库自测非 HCCL Test，不混用**） |

## rank/group/设备映射与执行次序

- NCCL communicator 固定 rank↔device（样例 rank=device 只作样例，不扩成通用映射）；库层：隐式总序启用后各设备主机发起顺序仍须匹配（单主机线程确定性顺序最易满足；CUDA graph 捕获/launch 时同规则）；框架层（PyTorch 2.8，独立契约）：`new_group` 要求主组**全部进程进入**（含非成员），各进程按**相同顺序**建组（`use_local_synchronization=True` 只做组内局部 barrier，属例外，另记）；NCCL 多组 collective 执行保持全局一致，多线程须显式同步；async 跨组须 `work.wait()` 做 stream 同步（work.wait 建立当前 CUDA stream 对完成的依赖，见 T03-04，不统一解释成 CPU 等待设备全部完成）；`get_group_rank/get_global_rank` 要求被查 rank 为组成员（[new_group](https://docs.pytorch.org/docs/2.8/distributed.html#torch.distributed.new_group)、[get_group_rank](https://docs.pytorch.org/docs/2.8/distributed.html#torch.distributed.get_group_rank)）。以上不推出 RCCL/HCCL 相同约束。
- 独立指南/案例/实验导航：NCCL [communicators 并发节](https://docs.nvidia.com/deeplearning/nccl/archives/nccl_2275/user-guide/docs/usage/communicators.html#using-multiple-nccl-communicators-concurrently)（发起顺序）与 [T03-04 次序/进度契约](collectives-and-rank-progress.md)（匹配模型）；NCCL [超时指南](nccl-timeout-triage.md)、[来源案例](nccl-timeout-source-case.md)、[复现实验](nccl-timeout-experiment.md)；HCCL [超时指南](hccl-timeout-triage.md)、[来源案例](hccl-timeout-source-case.md)、[复现实验](hccl-timeout-experiment.md)；RCCL 次序见 [RCCL 档案](rccl-runtime-and-verification.md)（group/后台 job）。
- RCCL：同上结构，`ncclCommCuDevice` 为 ROCm device index；group 暂存/后台 job/InProgress 分支见 RCCL 档案。
- HCCL（Python world/custom/local vs C++ comm/rank/device，分层）：Python 侧 world group（默认全局，ranktable 创建）/custom group（子集，rank 本组内从 0 重排）/local rank **id**（group 内本 Server 进程的**编号**，区别于 local rank size 即**数量**；二者都不是设备逻辑 ID；[8.0 表 1-1](https://www.hiascend.com/doc_center/source/zh/CANNCommunityEdition/80RC1alpha003/apiref/hcclapiref/CANN%208.0.RC1.alpha003%20%E9%9B%86%E5%90%88%E9%80%9A%E4%BF%A1%E6%8E%A5%E5%8F%A3%E5%8F%82%E8%80%83%2001.pdf#page=10)）；查询转换接口：`get_rank_id`（device 在 group 中的 rank）、`get_local_rank_id`、`get_world_rank_from_group_rank`/`get_group_rank_from_world_rank`（[§2.2.5–2.2.8](https://www.hiascend.com/doc_center/source/zh/CANNCommunityEdition/80RC1alpha003/apiref/hcclapiref/CANN%208.0.RC1.alpha003%20%E9%9B%86%E5%90%88%E9%80%9A%E4%BF%A1%E6%8E%A5%E5%8F%A3%E5%8F%82%E8%80%83%2001.pdf#page=18)，均要求初始化完成后调用）；C++ 侧 ranktable 初始化（`HcclCommInitClusterInfo`）、`HcclGetRootInfo`→广播→`HcclCommInitRootInfo` 配对（InitRootInfo 只能串行调用，各 rank nranks/rootInfo 须相同）、`HcclGetRankId`、单机 `HcclCommInitAll`（devices 为 device 逻辑 ID 列表，按序建域，不可重复；仅单机场景；多线程调集合操作 API 须在 `HCCL_CONNECT_TIMEOUT` 内；**不支持一张卡同时调用多个通信操作 API**；设备选择按 devices 列表，样例 rank=device 只作样例；[§3.2](https://www.hiascend.com/doc_center/source/zh/CANNCommunityEdition/80RC1alpha003/apiref/hcclapiref/CANN%208.0.RC1.alpha003%20%E9%9B%86%E5%90%88%E9%80%9A%E4%BF%A1%E6%8E%A5%E5%8F%A3%E5%8F%82%E8%80%83%2001.pdf#page=38)）。生命周期四阶段归 8.1（概述 §1，印刷 p3–4/物理 p9–10）；8.0 为三阶段（简介 §1，通信初始化/建链/执行），8.0 rank 概念见简介 rank 表。三线版本不组合成目标环境。

## HCCL Test 交集状态（blocked_on_evidence/open）

HCCL Test（9.1.X）与目标 CANN/HDK/机型组合的版本/运行条件交集**无官方材料**：现有三件分属 8.0/8.1/9.1.X 三条线，cann-hccl 快照 `2d685b08` 明确非配套 tag，redirect 浮动不可引用。候选交集路径（CANN↔HDK 配套表、固件驱动页、同版本 HCCL Test 指南）待浏览器复核后登记；交集证实前本子项保持 `blocked_on_evidence/open`，**不得因已登记测试工具或罗列 unknown 而关闭**。CANN×芯片×OS 容器矩阵只证明容器发行存在，不证明支持交集。

## 来源与待确认问题

- NCCL：[2.27.5 指南](https://docs.nvidia.com/deeplearning/nccl/archives/nccl_2275/user-guide/docs/)、nccl-tests（既有登记）；PyTorch：[distributed 2.8](https://docs.pytorch.org/docs/2.8/distributed.html)（后端矩阵与次序约束）。
- RCCL：取证见 [T03-05 研究记录](../../docs/research/batch-19-rccl-sources.md)（本表 RCCL 列不重复登记）。
- HCCL：[8.0 API PDF](https://www.hiascend.com/doc_center/source/zh/CANNCommunityEdition/80RC1alpha003/apiref/hcclapiref/CANN%208.0.RC1.alpha003%20%E9%9B%86%E5%90%88%E9%80%9A%E4%BF%A1%E6%8E%A5%E5%8F%A3%E5%8F%82%E8%80%83%2001.pdf)（rank/通信域/P2P/错误查询；三阶段）、[8.1 用户指南 PDF](https://www.hiascend.com/doc_center/source/zh/CANNCommunityEdition/81RC1alpha001/devguide/hccl/hcclug/CANN%E7%A4%BE%E5%8C%BA%E7%89%88%208.1.RC1.alpha001%20%E9%9B%86%E5%90%88%E9%80%9A%E4%BF%A1%E7%94%A8%E6%88%B7%E6%8C%87%E5%8D%97%2001.pdf)（框架适配/四阶段/AlltoAllV/EI0002）、9.1.X Test 指南（910 静态正文 0001/0004–0007；普通入口曾返回异题页面，版本定位限制见记录）、[cann-hccl 快照](https://gitee.com/ascend/cann-hccl/blob/2d685b08/README.md)（算法名单与配套警告）。
- 逐条主张与证据定位见[第十九批 T03-06 来源记录](../../docs/research/batch-19-t03-06-sources.md)。
- 待确认：HCCL Test 交集（blocked）；HCCL Test 计时实现；HCCL 主机返回边界；NCCL/CUDA/驱动配套；TorchNPU 加载路径。
