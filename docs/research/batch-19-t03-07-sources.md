# 第十九批 T03-07 来源记录

任务：T03-07（修订 `bandwidth-baselines.md`，只做加法）。作者取证轮次：首轮（同批来源准备：逐页实开）＋第二轮（broadcast/policy/common 行段、CANN 0004/0005/0006、NCCL env、CROSS_NIC、SuperPOD fabric、GPU Node Triage 正确 URL 核对）；审阅方独立取证（22 文件、gin_sdma policy L145–155、device-time host 头等）见 [T03-07 加法初审](batch-19-t03-07-codex-review.md)，不冒充作者当时已完成。

## 主张—来源定位表（完整 ID—精确地址—行段/字段—支持范围/未覆盖）

固定 commit：rocm-systems `7da43026e4f2ef7600433c38c820732f7a205d22`（tag therock-10.1）；nccl-tests `b4d5beebca8a76cf01335f724d154b9b9d394d96`；CANN 9.1.X 指南 910 路径。

| 主张 | 已登记 ID | 精确地址与行段/字段 | 支持范围 / 未覆盖 |
|---|---|---|---|
| RCCL 六算子修正因子 | src.rocm.rocm-systems-therock-10.1 | [PERFORMANCE.md](https://github.com/ROCm/rocm-systems/blob/therock-10.1/projects/rccl-tests/doc/PERFORMANCE.md) 全文（普通模式；首段 ms 与实现冲突已标注） | 不覆盖 ALLGATHERV 环境分支 |
| AllReduce 实现口径 | 同上 | [all_reduce.cu AllReduceGetBw L78–84](https://github.com/ROCm/rocm-systems/blob/7da43026e4f2ef7600433c38c820732f7a205d22/projects/rccl-tests/src/all_reduce.cu#L78-L84)（`count·typesize/1E9/sec`） | 与 PERFORMANCE 一致 |
| AllGather 实现系数 | 同上 | [`gin_sdma_allgather_policy.h` L145–155](https://github.com/ROCm/rocm-systems/blob/7da43026e4f2ef7600433c38c820732f7a205d22/projects/rccl-tests/src/gin_sdma_allgather_policy.h#L145-L155)（审阅方核对，作者引用注角色） | `perRankCount·typeSize·n` + `(n-1)/n` |
| Broadcast 环境分支 | 同上 | [`broadcast.cu` L82–93](https://github.com/ROCm/rocm-systems/blob/7da43026e4f2ef7600433c38c820732f7a205d22/projects/rccl-tests/src/broadcast.cu#L82-L93) + [README grouped-broadcast](https://github.com/ROCm/rocm-systems/blob/therock-10.1/projects/rccl-tests/README.md#user-content-grouped-broadcast-allgatherv-mode) | 普通 vs ALLGATHERV 分开 |
| us 口径/归一化/例外 | 同上 | [common.cu L1070–1128](https://github.com/ROCm/rocm-systems/blob/7da43026e4f2ef7600433c38c820732f7a205d22/projects/rccl-tests/src/common.cu#L1070-L1128)（归一化/graph 缩放）/[L1259–1266](https://github.com/ROCm/rocm-systems/blob/7da43026e4f2ef7600433c38c820732f7a205d22/projects/rccl-tests/src/common.cu#L1259-L1266)（×1.0E6）；[normalizeElapsedPerIter](https://github.com/ROCm/rocm-systems/blob/7da43026e4f2ef7600433c38c820732f7a205d22/projects/rccl-tests/src/gin_sdma_devtime_host.h#L41-L51)；`-C/-z 3`/device-only 例外同文件 | 默认 host 模式；其余算子实现未逐一回查 |
| 页脚判据方向 | 同上 | [common.cu L2757–2788](https://github.com/ROCm/rocm-systems/blob/7da43026e4f2ef7600433c38c820732f7a205d22/projects/rccl-tests/src/common.cu#L2757-L2788)（平均 busbw < MIN_BW×0.9，未设取 -1） | 环境相关，非通用门限 |
| 默认参数/聚合 | 同上 | [README Arguments](https://github.com/ROCm/rocm-systems/blob/therock-10.1/projects/rccl-tests/README.md#user-content-arguments)（`-b/-e` 32M、`-n 20`、`-w 1`、`-m 1`、`-a 1`、`-O`、`-A`）；`-a` 聚合、`-I/-K` 分布 | MPI 默认 Avg |
| HCCL 算法带宽/字段 | src.huawei.hccl-perf-test-guide-cann-9.1.x | [0001](https://www.hiascend.com/doc_center/source/zh/CANNCommunityEdition/910/devaids/hccltool/HCCLpertest_16_0001.html)（算法带宽定义）；[0006](https://www.hiascend.com/doc_center/source/zh/CANNCommunityEdition/910/devaids/hccltool/HCCLpertest_16_0006.html)（data_size 单 NPU、avg_time us、check_result NULL 两分支＋最大卡数表） | 计时实现 unknown；BLOCKED-1 |
| HCCL 参数契约 | 同上 | [0005](https://www.hiascend.com/doc_center/source/zh/CANNCommunityEdition/910/devaids/hccltool/HCCLpertest_16_0005.html)（MPI `-n` vs 工具 `-n`；`-t` 默认 0/三条件；`-c 0/1/2`；`-p` 常规分支；对齐微调） | `-t` 文档契约不在 unknown 内 |
| HCCL 跨节点/例外 | 同上 | [0004](https://www.hiascend.com/doc_center/source/zh/CANNCommunityEdition/910/devaids/hccltool/HCCLpertest_16_0004.html)（hostfile 双格式、A3 约束、IFNAME 4 格式、CONNECT_TIMEOUT 分档、BUFFSIZE、HCCL_TEST_USE_DEVS 例外） | 3K/5K 为示例建议；IFNAME 为建链网卡 |
| NCCL 路径选择 | src.nvidia.nccl-user-guide-2.27.5 | [env CROSS_NIC](https://docs.nvidia.com/deeplearning/nccl/archives/nccl_2275/user-guide/docs/env.html#nccl-cross-nic)（0/1/2＋成员不同例外）；IB_HCA/多 QP/ALGO-PROTO 调试类 | rail 官方出处；不代替实际映射 |
| fabric 事实 | src.nvidia.dgx-superpod-h100-ra-fabrics-2026-10-09 | [Compute IB fabric](https://docs.nvidia.com/dgx-superpod/reference-architecture-scalable-infrastructure-h100/latest/network-fabrics.html#computeinfiniband-fabric)（同 SU 对应 rail 一跳；storage 4:3） | 跨 SU 同 rail 可过 spine |
| 基线方法 | src.nvidia.gpu-node-triage-2026-10-08 | [Network Testing](https://docs.nvidia.com/deploy/gpu-debug-guidelines/gpu-node-triage.html#network-testing)（成对建基线/换节点隔离/按 rail 隔离；可变页，观察日期 2026-10-13） | 方法引用；URL 已更正 |
| T03-03 联动 | T03-03 已审阅口径 | [RDMA 诊断](../../knowledge/03-communication/rdma-baseline-and-congestion-triage.md)“计数器语义”与“停止条件与恢复安排”两节 | 计数器语义不转录；恢复限定 RDMA 分支 |
| T03-01 联动 | T03-01 已审阅口径 | [互联路径正文](../../knowledge/03-communication/interconnect-paths.md) Table 6 联合身份、`nvidia-smi topo`/`aclrtGetDevicesTopo` | 主机/设备路径行 |
| MI300X 门槛 | src.amd.instinct-mi300x-system-acceptance-2026-10-09 | Performance Benchmarks（≥304 GB/s） | 厂商示例反例，非本库判据 |

## unknown / blocked 清单

- BLOCKED-1（延续）：HCCL Test×CANN/HDK/机型交集，凡可运行组合处同步 blocked。
- U1 已关闭（AllGather 系数经审阅方核对，角色已注）；余算子实现未逐一回查保留。
- U2：HCCL avg_time 实现；U3：HCCL_OP_EXPANSION_MODE；U4：T03-03 联动（计数器/恢复以其为准）；U5：聚合口径（HCCL 多 rank 归入 U2）；U6：许可照录；版本线不拼环境。
