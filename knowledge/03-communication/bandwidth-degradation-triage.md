---
id: communication.bandwidth-degradation-triage
title: 通信带宽退化诊断指南
type: procedure
domain: communication
status: draft
platforms: [generic]
source_refs:
  - src.nvidia.nccl-tests-b4d5beeb
  - src.nvidia.nccl-user-guide-2.27.5
  - src.ascend.cann-hccl-2d685b08
  - src.huawei.hccl-perf-test-guide-cann-9.1.x
updated_at: "2026-09-30"
summary: 把“通信带宽变低”先拆成测量口径错误、配置/映射问题和真实链路退化三类；GPU 用 nccl-tests/NCCL 2.27.5 证据，NPU 用 CANN 9.1.X HCCL Test 证据，两边口径不互比。
related_ids:
  - communication.bandwidth-baselines
  - communication.collectives-and-rank-progress
  - communication.nccl-timeout-triage
  - communication.hccl-timeout-triage
  - reliability.evidence-and-hypotheses
applicability:
  environment_refs: []
  notes: "流程以 nccl-tests 固定 commit b4d5beeb、NCCL 2.27.5 归档文档与 CANN 9.1.X《HCCL性能测试工具》为证据样板；目标环境的工具版本、拓扑、机型互联规格与链路遥测来源需另行固定。"
verification:
  status: source_checked
  evidence_refs:
    - src.nvidia.nccl-tests-b4d5beeb
    - src.nvidia.nccl-user-guide-2.27.5
    - src.ascend.cann-hccl-2d685b08
    - src.huawei.hccl-perf-test-guide-cann-9.1.x
  notes: "已核对 nccl-tests 计时/校验实现、NCCL 2.27.5 troubleshooting/env/RAS 页、HCCL Test 版本化指南的参数与结果字段及 cann-hccl 算法页定性表述；未构建或运行任何通信测试，未采集链路遥测。"
---

# 通信带宽退化诊断指南

## 目标与触发条件

触发场景：通信测试结果低于历史基线、低于他人报告，或训练/推理的通信阶段耗时上升。本流程先把“带宽低”拆成三类互不相同的候选：

- **(a) 测量口径错误**：两次“带宽”根本不是同一个量（消息大小、计时方式、聚合、公式、工具版本不同）；
- **(b) 配置/映射问题**：拓扑检测、算法/协议选择、rank 映射、亲和性或环境配置使流量走了更慢的路径；
- **(c) 真实链路退化**：链路降速、flap、重传、拥塞或硬件健康导致的真实能力下降。

判断口径本身的方法见[通信带宽与性能基线口径](bandwidth-baselines.md)；本文是该口径的操作化流程。GPU 侧证据固定为 nccl-tests `b4d5beeb` 与 NCCL 2.27.5 归档文档；NPU 侧证据固定为 CANN 9.1.X《HCCL性能测试工具》。**两边输出的字段语义不同，不可直接互比**（见步骤 2）。

## 适用范围与前置条件

进入排查前至少固定：测试工具与通信库版本、算子、datatype、消息大小扫描参数、rank 数与映射、in/out-of-place、计时与聚合口径、单机/多机拓扑、并发负载，以及一条可比较的历史基线（字段要求见[基线口径](bandwidth-baselines.md)的最小记录表）。没有同口径基线时，“退化”本身不成立，先做基线建设。

## 需要的证据

| 证据 | 采集范围或定位 | 用途 | 缺失时如何处理 |
|---|---|---|---|
| 完整命令与输出 | 工具原始终端输出（含表头/页脚）、命令行参数 | 判断口径 | 只有截图或二手数字时不作比较 |
| 基线记录 | 同机型、同拓扑、同软件、同负载的历史分布 | 定义“退化” | 无基线则本轮只能建立基线 |
| 配置与拓扑证据 | rank↔设备↔NUMA/NIC 映射、通信库初始化日志、环境变量 | (b) 支路 | 拓扑未知时不能定位路径 |
| 链路遥测 | NIC/交换机/互联端口计数器、链路状态事件 | (c) 支路 | 本库尚无遥测来源核对，见步骤 5 的缺口说明 |

## 步骤与判断分支

| 步骤 | 检查或动作 | 运行影响 | 预期证据与解释 | 下一步 |
|---|---|---|---|---|
| 1 | 核对 (a) 口径：消息大小的单位与语义（nccl-tests 的 `-b/-e` 后缀是二进制 M=MiB，输出 GB/s 是十进制；HCCL Test 会对 `-b/-e/-i` 输入做地址对齐或 rank 倍数微调；nccl-tests 内存不足时自动下调 maxBytes 并打印提示）；算子的 `S` 口径（ReduceScatter/AllGather 的 S 是全数组而非单 rank 分片）；是否混入 in-place/out-of-place 两列择优 | 只读 | 口径不一致可直接解释“退化”，无需怀疑硬件 | 口径对齐后重比；一致则进步骤 2 |
| 2 | 核对计时与聚合：nccl-tests 主计时是 host 墙钟、整个 iters 循环除以 `iters*agg_iters`（[common.cu L795–801](https://github.com/NVIDIA/nccl-tests/blob/b4d5beebca8a76cf01335f724d154b9b9d394d96/src/common.cu#L795-L801)），CUDA events 只在 `-I` 逐迭代统计中使用；`-c` 正确性校验在计时循环之外，不进 time/algbw/busbw（[L757–771 与 L831–884](https://github.com/NVIDIA/nccl-tests/blob/b4d5beebca8a76cf01335f724d154b9b9d394d96/src/common.cu#L757-L771)）；`-a` 的 rank 聚合（默认 MPI 平均）与 `-z` blocking 模式改变口径。HCCL Test 的 warmup 默认 10 次不参与统计，`-t` 可切 Device-only 计时（[参数说明](https://www.hiascend.com/document/detail/zh/CANNCommunityEdition/910/devaids/hccltool/HCCLpertest_16_0005.html)）；其 `avg_time` 的计时实现未公开核对，标为未知 | 只读 | 计时/聚合差异被排除 | 进步骤 3 |
| 3 | 核对正确性与有效性：nccl-tests 页脚 “Out of bounds values: N FAILED/OK” 是**出现数据校验错误的测量行数**（名称易误读为数组越界；[util.cu L901](https://github.com/NVIDIA/nccl-tests/blob/b4d5beebca8a76cf01335f724d154b9b9d394d96/src/util.cu#L901)），N>0 时该结果不作性能证据；页脚 “Avg bus bandwidth” 只在设了 `NCCL_TESTS_MIN_BW` 时与阈值 90% 比较。HCCL Test 的 `check_result` 为 NULL 的情形（`-c 0`、数值溢出或超出可精确表达范围）见[结果说明](https://www.hiascend.com/document/detail/zh/CANNCommunityEdition/910/devaids/hccltool/HCCLpertest_16_0006.html) | 只读 | 校验失败/NULL 的样本剔除出性能比较 | 样本有效则进步骤 4 |
| 4 | (b) 配置/映射支路（GPU）：`NCCL_DEBUG=INFO` 配合 `NCCL_DEBUG_SUBSYS`（GRAPH=拓扑检测与图搜索、TUNING=算法/协议调优等；[env.html](https://docs.nvidia.com/deeplearning/nccl/archives/nccl_2275/user-guide/docs/env.html)）确认实际选中的传输（P2P/SHM/NET）与算法；对照 `NCCL_ALGO`/`NCCL_PROTO` 是否被人为设置（官方劝阻设置 PROTO；不支持 LL128 的平台强行开启可致 data corruption）。官方排查建议包括：ACS/IOMMU 会把 P2P 流量重定向到 CPU root complex 导致显著性能下降甚至 hang（`lspci -vvv \| grep ACSCtl` 检查）；VM/容器的虚拟 PCI 拓扑会导致次优选择；跑 NCCL 前先用 `ib_write_bw` 验证 IB 链路（[troubleshooting.html](https://docs.nvidia.com/deeplearning/nccl/archives/nccl_2275/user-guide/docs/troubleshooting.html) 各小节） | 读取日志低影响；改环境变量需授权 | 实际路径与预期路径不一致即支持配置支路 | 修正映射/配置后同口径复测；路径正常进步骤 5 |
| 5 | (b) NPU 侧对照：HCCL Test 只输出算法带宽（数据量/耗时，无 bus 带宽列，[工具介绍](https://www.hiascend.com/document/detail/zh/CANNCommunityEdition/910/devaids/hccltool/HCCLpertest_16_0001.html)）；注意 `-p x` 从 Device ID 0 连续启动 x 个设备且有各产品取值范围（[规格约束](https://www.hiascend.com/document/detail/zh/CANNCommunityEdition/910/devaids/hccltool/HCCLpertest_16_0007.html)）；执行前提含防火墙、somaxconn、ulimit -n 等（[工具执行](https://www.hiascend.com/document/detail/zh/CANNCommunityEdition/910/devaids/hccltool/HCCLpertest_16_0004.html)）。cann-hccl 算法文档的定性表述（如大流量下某些算法的链路编排可能引起交换机流量冲突）只作机制提示，不作测量依据 | 只读 | NPU 侧先确认参数与设备映射符合工具约束 | 配置支路排除后进步骤 6 |
| 6 | (c) 真实链路退化支路：GPU 侧 NCCL 2.27.5 文档只提供配置语义（`NCCL_IB_TIMEOUT`、`NCCL_IB_RETRY_CNT`、`NCCL_IB_RETURN_ASYNC_EVENTS` 把 IB 异步事件以 warning 报出）与 [RAS 健康事件及正常瞬态示例](https://docs.nvidia.com/deeplearning/nccl/archives/nccl_2275/user-guide/docs/troubleshooting/ras.html#sample-output)。RAS 的 communicator 进度 MISMATCH 可以提示慢 rank/进度分叉，但官方示例同时说明：**活跃通信期间各 rank 的计数差异可能是正常瞬态**，初始化/销毁过渡也可能暂时出现 MISMATCH；对同一 communicator、相同阶段连续查询，并与该负载的正常进度/不均衡基线比较；计数持续不推进才值得调查，而持续停滞也不直接证明链路退化。60 秒不可达判 DEAD。**NCCL 文档没有链路级硬件计数器**。降速、flap、重传的直接证据需要 NIC/交换机/互联遥测来源，本库尚未核对此类来源；有现场遥测时按[基线口径](bandwidth-baselines.md)的遥测字段要求与测试窗口对齐后比较，没有则该支路结论保持 `unknown`，不用带宽数字反推链路故障 | 遥测查询按现场权限 | 同期链路事件与通信路径对齐才支持链路支路 | 证据不足则保留 unknown；勿凭单一带宽值定性 |
| 7 | 汇总三类候选的排除/确认证据 | 无 | 每个结论回链到口径、配置或遥测证据 | 满足完成判据后结束 |

## 停止条件与恢复安排

- 通信测试会占用设备与链路：在生产集群或共享网络上运行前确认授权与窗口；大规模集群开启结果校验（`-c`）会增加执行耗时（HCCL 文档明确提示）。
- 修改 `NCCL_ALGO`/`NCCL_PROTO`、P2P/SHM 开关或 HCCL 环境变量属配置变更：记录原值、限定范围、可回滚；`NCCL_PROTO` 官方劝阻设置，强行开启不支持 LL128 的平台可致 data corruption。
- 不要为了“好看的数字”删除 warm-up 后的首轮样本或失败行；异常样本单独标注保留。

## 完成判据

以下任一结果可以结束本轮诊断：

1. “退化”被证明是口径差异：两次测量在固定字段表逐项对齐后差异消失；
2. 定位到具体配置/映射原因（传输选择、算法、拓扑检测、rank 映射），同口径复测确认；
3. 链路支路有同期遥测或官方工具（如 `ib_write_bw`）独立证据，并与通信路径一致；
4. 证据不足，但已记录缺失的基线、拓扑或遥测证据，结论保持 `unknown`。

“带宽数字回升”不单独满足完成判据；需要说明是哪一类原因、什么证据支持。

## 来源与验证记录

- [nccl-tests 固定快照](https://github.com/NVIDIA/nccl-tests/tree/b4d5beebca8a76cf01335f724d154b9b9d394d96)：计时/校验/页脚实现与参数语义。
- [NCCL 2.27.5 归档用户指南](https://docs.nvidia.com/deeplearning/nccl/archives/nccl_2275/user-guide/docs/)：env.html 的变量语义、troubleshooting.html 的官方排查建议、troubleshooting/ras.html 的 RAS 健康事件（注意 RAS 实际路径在 troubleshooting/ 下，顶层 ras.html 不存在）。
- [cann-hccl 固定快照](https://gitee.com/ascend/cann-hccl/tree/2d685b084a60366b47ad8e50a563ee5c4dbef7fe)：算法页定性机制与参考资料索引；仓库内无 HCCL Test 结果解释文档。
- [CANN 9.1.X《HCCL性能测试工具》](https://www.hiascend.com/document/detail/zh/CANNCommunityEdition/910/devaids/hccltool/HCCLpertest_16_0001.html)：算法带宽定义、参数、结果字段与规格约束；经 redirect 解析落点，redirect 为可变定位。
- 逐条主张与证据定位见[第九批带宽来源记录](../../docs/research/batch-09-bandwidth-sources.md)。
- 当前验证范围：来源核对；未构建或运行测试工具，未采集遥测。
- 待确认：HCCL Test 计时实现；链路级计数器的可用来源（NIC/交换机/HCCS）；目标机型“应达带宽”的机型级依据。
