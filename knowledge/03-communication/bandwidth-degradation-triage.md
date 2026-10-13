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
  - src.nvidia.nccl-issue-2409
  - src.nvidia.nccl-issue-814
  - src.nvidia.nccl-issue-209
updated_at: "2026-10-14"
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
  notes: "已核对 nccl-tests 计时/校验实现、NCCL 2.27.5 troubleshooting/env/RAS 页、HCCL Test 版本化指南的参数与结果字段及 cann-hccl 算法页定性表述；作者共十三轮：首轮（#2409/#814 全文实开）＋第二/三/四/五/六/七/八/九/十次修订＋第十一次修订（映射同步）＋第十二次修订（账本表交付）＋第十三次修订（本轮：第四轮复用列明、#223 未采用交代、L19 定位改稳定节名；无新增远程取证，仅复用已核对来源；逐轮明细精确引用来源记录逐轮账本表，未解历史范围见该表）；审阅方独立取证轮次：加法初审＋Codex 定向复核（一/二/三/四/五/六/七/八/九/十/十一/十二次）见加法初审与复核报告（输入时既有十三份，后续新增复核报告不计入本轮输入），不冒充作者当时已完成；跨节点矩阵字段契约见 T03-07（实测矩阵未交付）；旧遥测缺口为原批范围，当前 T03-03 文档可复用但现场能力未证实；未构建或运行任何通信测试，未采集链路遥测。"
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
| 链路遥测 | NIC/交换机/互联端口计数器、链路状态事件 | (c) 支路 | “尚无核对”为原批（Batch 09）核对范围；当前 T03-03 计数器文档可复用（UFM/mlx5/Cumulus 口径），但现场机型/字段能力未证实，见步骤 6 的缺口说明 |
| 时间窗对齐包 | 库日志时间戳＋计数器采样窗口＋测试输出三者可对齐到同一窗口，并记录 rank↔设备↔NIC/rail 映射与时钟条件；跨节点矩阵字段见[基线口径跨节点矩阵](bandwidth-baselines.md) | acceptance (1) | 计数器缺失→链路支路 unknown；时钟条件缺失→慢 rank 判定 unknown |

最小对齐登记契约（无真实数值不填，仅定字段）：run 身份、节点/rank 身份、测试窗起止、采样窗起止、日志时钟基准（wall/CPU/tick 注明）、跨节点对齐依据及不确定度（NTP/PTP/事后对齐/未知）、计数器更新边界（采样/推送周期，如 Cumulus 2 秒/hardware 页）、端口/rail 映射。同期增量仅在同窗同基准（或已量化偏差）下比较；否则只保留单节点/静态证据。时钟条件缺失限制**所有**依赖跨节点先后/同期关系的支路（路径归属、争用对照、慢 rank 判定，不只慢 rank）；设计记录与现场已取得证据分开登记（前者是要求，后者是实际）。

## 步骤与判断分支

| 步骤 | 检查或动作 | 运行影响 | 预期证据与解释 | 下一步 |
|---|---|---|---|---|
| 1 | 核对 (a) 口径：消息大小的单位与语义（nccl-tests 的 `-b/-e` 后缀是二进制 M=MiB，输出 GB/s 是十进制；HCCL Test 会对 `-b/-e/-i` 输入做地址对齐或 rank 倍数微调；nccl-tests 内存不足时自动下调 maxBytes 并打印提示）；算子的 `S` 口径（ReduceScatter/AllGather 的 S 是全数组而非单 rank 分片）；是否混入 in-place/out-of-place 两列择优 | 只读 | 口径不一致可直接解释“退化”，无需怀疑硬件 | 口径对齐后重比；一致则进步骤 2 |
| 2 | 核对计时与聚合：nccl-tests 主计时是 host 墙钟、整个 iters 循环除以 `iters*agg_iters`（[common.cu L795–801](https://github.com/NVIDIA/nccl-tests/blob/b4d5beebca8a76cf01335f724d154b9b9d394d96/src/common.cu#L795-L801)），CUDA events 只在 `-I` 逐迭代统计中使用；`-c` 正确性校验在计时循环之外，不进 time/algbw/busbw（[L757–771 与 L831–884](https://github.com/NVIDIA/nccl-tests/blob/b4d5beebca8a76cf01335f724d154b9b9d394d96/src/common.cu#L757-L771)）；`-a` 的 rank 聚合（默认 MPI 平均）与 `-z` blocking 模式改变口径。HCCL Test 的 warmup 默认 10 次不参与统计，`-t` 可切 Device-only 计时（[参数说明](https://www.hiascend.com/document/detail/zh/CANNCommunityEdition/910/devaids/hccltool/HCCLpertest_16_0005.html)）；其 `avg_time` 的计时实现未公开核对，标为未知 | 只读 | 计时/聚合差异被排除 | 进步骤 3 |
| 3 | 核对正确性与有效性：nccl-tests 页脚 “Out of bounds values: N FAILED/OK” 是**出现数据校验错误的测量行数**（名称易误读为数组越界；[util.cu L901](https://github.com/NVIDIA/nccl-tests/blob/b4d5beebca8a76cf01335f724d154b9b9d394d96/src/util.cu#L901)），N>0 时该结果不作性能证据；页脚 “Avg bus bandwidth” 只在设了 `NCCL_TESTS_MIN_BW` 时与阈值 90% 比较。HCCL Test 的 `check_result` 为 NULL 的情形（`-c 0`、数值溢出或超出可精确表达范围）见[结果说明](https://www.hiascend.com/document/detail/zh/CANNCommunityEdition/910/devaids/hccltool/HCCLpertest_16_0006.html) | 只读 | 校验失败/NULL 的样本剔除出性能比较 | 样本有效则进步骤 4 |
| 4 | (b) 配置/映射支路（GPU）：`NCCL_DEBUG=INFO` 配合 `NCCL_DEBUG_SUBSYS`（GRAPH=拓扑检测与图搜索、TUNING=算法/协议调优等；[env.html](https://docs.nvidia.com/deeplearning/nccl/archives/nccl_2275/user-guide/docs/env.html)）确认实际选中的传输（P2P/SHM/NET）与算法；对照 `NCCL_ALGO`/`NCCL_PROTO` 是否被人为设置（官方劝阻设置 PROTO；不支持 LL128 的平台强行开启可致 data corruption）。官方排查建议包括：ACS/IOMMU 会把 P2P 流量重定向到 CPU root complex 导致显著性能下降甚至 hang（`lspci -vvv \| grep ACSCtl` 检查）；VM/容器的虚拟 PCI 拓扑会导致次优选择；跑 NCCL 前先用 `ib_write_bw` 验证 IB 链路（[troubleshooting.html](https://docs.nvidia.com/deeplearning/nccl/archives/nccl_2275/user-guide/docs/troubleshooting.html) 各小节） | 读取日志低影响；改环境变量需授权 | 实际路径与预期路径不一致即支持配置支路 | 修正映射/配置后同口径复测；路径正常进步骤 5 |
| 5 | (b) NPU 侧对照：HCCL Test 只输出算法带宽（数据量/耗时，无 bus 带宽列，[工具介绍](https://www.hiascend.com/document/detail/zh/CANNCommunityEdition/910/devaids/hccltool/HCCLpertest_16_0001.html)）；注意 `-p x` 从 Device ID 0 连续启动 x 个设备且有各产品取值范围（[规格约束](https://www.hiascend.com/document/detail/zh/CANNCommunityEdition/910/devaids/hccltool/HCCLpertest_16_0007.html)）；执行前提含防火墙、somaxconn、ulimit -n 等（[工具执行](https://www.hiascend.com/document/detail/zh/CANNCommunityEdition/910/devaids/hccltool/HCCLpertest_16_0004.html)）。cann-hccl 算法文档的定性表述（如大流量下某些算法的链路编排可能引起交换机流量冲突）只作机制提示，不作测量依据 | 只读 | NPU 侧先确认参数与设备映射符合工具约束 | 配置支路排除后进步骤 6 |
| 6 | (c) 真实链路退化支路：GPU 侧 NCCL 2.27.5 文档只提供配置语义（`NCCL_IB_TIMEOUT`、`NCCL_IB_RETRY_CNT`、`NCCL_IB_RETURN_ASYNC_EVENTS` 把 IB 异步事件以 warning 报出）与 [RAS 健康事件及正常瞬态示例](https://docs.nvidia.com/deeplearning/nccl/archives/nccl_2275/user-guide/docs/troubleshooting/ras.html#sample-output)。RAS 的 communicator 进度 MISMATCH 可以提示慢 rank/进度分叉，但官方示例同时说明：**活跃通信期间各 rank 的计数差异可能是正常瞬态**，初始化/销毁过渡也可能暂时出现 MISMATCH；对同一 communicator、相同阶段连续查询，并与该负载的正常进度/不均衡基线比较；计数持续不推进才值得调查，而持续停滞也不直接证明链路退化。60 秒不可达判 DEAD。**NCCL 文档没有链路级硬件计数器**。降速、flap、重传的直接证据需要 NIC/交换机/互联遥测来源，本库尚未核对此类来源；有现场遥测时按[基线口径](bandwidth-baselines.md)的遥测字段要求与测试窗口对齐后比较，没有则该支路结论保持 `unknown`，不用带宽数字反推链路故障 | 遥测查询按现场权限 | 同期链路事件与通信路径对齐才支持链路支路 | 证据不足则保留 unknown（“尚无核对”指原批 Batch 09 范围；T03-03 UFM/mlx5/Cumulus 文档已核对可复用，目标机型字段能力 unknown）；勿凭单一带宽值定性 |
| 7 | 汇总三类候选的排除/确认证据 | 无 | 每个结论回链到口径、配置或遥测证据 | 证据齐全且满足完成判据→结束；有未完成候选或证据缺口（口径未对齐/映射未确认/遥测缺失）→转步骤 8 |
| 8 | 热点/争用四分支区分检查：按固定顺序记录四项的排除/确认证据——(a) 路由/映射/热链路：最小输入（rank→设备→NIC/端口映射＋算法/tree-ring/QP 配置＋rail 选择记录＋预期负载/历史对照＋端口集中度定位，见 [T03-07 跨节点矩阵](bandwidth-baselines.md)）；支持（配置不一致纠正后复测恢复——该方向支持原配置/映射原因；或同窗遥测热点集中定位）；排除（映射与预期一致且遥测无集中）；unknown（映射/历史缺失）。配置不一致与热点集中分开判读。多流交织行为引用注推断强度（[维护者解释](https://github.com/NVIDIA/nccl/issues/814#issuecomment-1493802672)，AMD CPU 双向/多流交织影响流水）；(b) 共享干扰：CPU、网络、存储分别设隔离轮（独占/停背景）与背景轮（加载重现），比较同窗口指标；支持（背景轮退化、隔离轮恢复）/排除（两轮无差）；缺任一轮或无同窗计数器/负载记录时不能判争用；socket 线程与 `--bind-to none` 为 [NCCL #209](https://github.com/NVIDIA/nccl/issues/209) TCP 路径个案一线排查，不外推 IB 路径；(c) 物理错误（标签限强度：仅陈述已选事件，不作"硬件根因"断言）：所选端口/字段（收向错误、训练失败 down、lane minor 错误；[UFM 语义](../../knowledge/03-communication/rdma-baseline-and-congestion-triage.md)，版本 UFM 4.18.15）＋前后值/增量＋窗口/重置边界＋路径关系＋掩盖/覆盖声明；支持（增量与路径对齐且排除配置差）；有限排除（仅在以下同时成立时：有效同窗、所选同路径/同作用域事件在本窗无新增（错误事件 delta 为零，正增量不得进入本分支）、同路径同作用域字段、采样/重置边界可解释、路径关系已建立、覆盖声明允许——结论最多为"本窗未观测到这些事件"；重置/回退或采样边界无法解释、路径关系/掩盖条件/覆盖不足则保留 unknown，不能凭"已观测范围"一语进入排除）；unknown（字段未选/窗口不齐）。收向错误含 overrun 等，不统一当硬件物理根因；Xmit Discards 为多因响应，不单独定硬件故障；未选字段保留 unknown，**不用吞吐低证明硬件故障**；ACS/IOMMU/GDR/注册限制属配置/映射条件，见 (a) 对应检查，不列为硬件错误信号；(d) 调用/消息变化：回链实际 collective、datatype/count/root/rank/次序及消息记录做同口径比较；支持（参数差异纠正后复测恢复）/排除（参数一致）；`SPLIT_DATA_ON_QPS` 默认值以 env 页为准；设备顺序按映射解释；记录/消息序列缺失或未能对齐时记 unknown（不只要求"回链"） | 只读 | 四分支状态齐全才能进入对照设计 | 进步骤 9 |
| 9 | 隔离/并发/替代路径对照设计（只设计不执行；入口：步骤 8 四分支状态齐全后进入；工具与路径分列——独立测量（`ib_write_bw` 同条件跨层对照）/日志回放（Replayer：rank 日志回放定位，不作路径替代）/解析候选（FaultDiag parse：版本/输入未选定，保留候选）/真实路径替代（换 rail/换 NIC/换传输：[RCCL 档案](rccl-runtime-and-verification.md)工具说明与 [troubleshooting](https://rocm.docs.amd.com/projects/rccl/en/docs-10.1.0/how-to/troubleshooting-rccl.html)采集节；TransferBench 为设备间拷贝基准，不与回放互换）；单列失败/超时/错误/窗口失效停止条件（正确性失败、超时/异步错误、观测窗口失效即停，与诊断完成出口分开）；恢复以**保存的原值**或经批准的修复配置为准（默认配置不一定是原批准配置；正常诊断结束不同于风险触发停止），并明确同条件正确性/覆盖复测要求。链接 NCCL（troubleshooting/RAS/env）/HCCL（Test 指南/用户指南）/RCCL（[T03-06 三库对照之 RCCL 列](communication-library-profiles.md)与 [RCCL 档案](rccl-runtime-and-verification.md)）资料 | 按现场授权；不新增执行授权 | 预期证据：四类轮次输入/判定齐全（明细见下节"步骤 9 四类轮次明细"）；未完成/unknown 留痕 | 对照完成、未完成、unknown 均先回步骤 7 汇总，再由 7 决定继续 8/9 或按完成判据结束（可做对照的缺口走 7→8→9；无法取得证据的缺口经 7 登记 unknown 后按完成判据 4 结束）；风险触发停止独立，不并入正常出口 |

### 步骤 9 四类轮次明细（设计交付；变更/保持项分开；未选标 unknown；共同准入：固定输入见步骤 1–3，同窗有效性见时窗契约，正确性/覆盖门禁见 T03-03 host 后端）

- 隔离基线轮：输入（默认配置全量记录：工具/库版本、算子/消息/映射、拓扑/并发声明；停背景声明）；变更项（无）；保持项（路径/配置/负载基线）；输出（原生输出存档）；校验/完整性（`#wrong`/覆盖/缺行声明；测试自身正确性与输出完整性、同窗有效性全部通过才形成有效基线，失败/缺行/无法解释时退出判读记 unknown）；判定（基线有效，或缺输入记 unknown）。默认配置不代替原批准配置（以保存原值为准）。
- 可控背景轮：输入（固定基线的测试输入、实际路径、计时口径与隔离条件，只改选定背景域）；变更项（每次只引入一域背景）；保持项（其余两域＋基线配置）；输出（测试原生输出＋同窗口指标＋背景实际达到声明的输出）；校验/完整性（复用基线共同门禁）；判定（退化/无差/无法比较；缺轮记 unknown）。三域可重现输入契约：CPU（计算任务身份：可执行文件/命令＋参数＋输入数据身份；并发：线程/进程数配置；强度/持续时间；作用进程；复现方法：同命令重放）；网络（完整生成命令/参数，或可定位生成方法＋完整配置身份/内容：流量生成工具/方法＋版本、并发/流配置、强度/持续时间、作用端点与路径、复现方法；缺输入记未完成/unknown）；存储（完整生成命令/参数，或可定位生成方法＋完整配置身份/内容：生成工具/方法＋版本、并发、具体作用后端/对象身份＋数据集/访问模式、强度/持续时间、复现方法；缺输入记未完成/unknown）。未选/缺输入时该背景轮为未完成/unknown。
- 单变量轮：输入（基线可比输入＋采用的隔离/背景共同条件）；变更项（选定一类路径变量如 rail/NIC/transport/算法/协议＋版本能力门禁声明；变量名/原值/新值）；保持项（其余配置/负载逐项列出）；输出（实际配置/路径记录＋测试原生输出）；校验/完整性（复用基线共同门禁；性能判读显式依赖有效基线/本轮校验和完整性准入）；判定（恢复/无变化/unknown；变量未选择或能力未证实记未完成）。
- 替代端点/rail/路径轮：输入（与基线匹配的输入/背景＋共同完整性/同窗准入）；变更项（被替代项；替代端点/HCA/端口/transport 身份）；保持项（其余配置/测试口径/隔离条件）；输出（替代成功的库/路径证据＋原生输出＋校验/覆盖，校验/覆盖有效才进入性能差异判读）；判定（替代成功/未发生/版本能力未证实 unknown）。工具用途列表不代替本轮；替代成功只是路径干预发生，不是完整性能对照已经有效。

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

## 上游退化案例：NCCL #2409（来源整理，非本库实测；角色分列）

- 实际环境（报告者自述）：2×8 H100 SXM、8×CX-7 400G RoCE、单 leaf、PFC+ECN lossless、PCIe Gen5 x16 GPU↔NIC PIX、MTU 9000；NCCL `2.31.2-1+cuda13.3`（亦复现于 2.29.7）、nccl-tests master `a0b82b2`、CX-7 fw `28.43.8016`、OFED 24.10、driver 595.71.05/CUDA 13.2/Ubuntu 24.04 kernel 6.8.0-137——环境逐项为报告者记录值，不作本库精确定位表。（[Issue #2409](https://github.com/NVIDIA/nccl/issues/2409)，2026-09-14 开，维护者 stephenmsachs 按报告者请求关闭，非独立验证）
- 开帖假说（报告者当时）：同 rail perftest 成功 → 推测为 NCCL 侧限制（后被其最终回复纠正，见修正行）；开帖 1 MiB 392.6 Gb/s 与首个跟帖单 QP/128 KiB 线速为**不同条件**，不得简写为同条件。
- 粒度对照跟帖（[首个](https://github.com/NVIDIA/nccl/issues/2409#issuecomment-5660150852)）：同 QP 数、同 per-WQE 消息大小下 perftest 线速而 NCCL 连接 105 Gb/s；仍在 NCCL handoff 假说阶段，不是修后结论。
- 深度对照跟帖（[QP/深度](https://github.com/NVIDIA/nccl/issues/2409#issuecomment-5660232470)：同 mlx5_0、host buffer、单向、每点 3 s，默认 tx depth 128）：128 KiB 下 1 QP/depth 8 为 293.4 Gb/s（**未线速**）、8 QP/depth 8 为 392.1 Gb/s、8 QP/depth 64 为 392.0 Gb/s；depth 1 的约 8.8 us（128 KiB）为推算值。QP/深度/buffer/方向/rail/阶段必须保留定位，不合并。
- 修正回复（[报告者最终回复](https://github.com/NVIDIA/nccl/issues/2409#issuecomment-5673453587)）：撤回开帖解释——深流水（perftest）可掩盖平台路径问题，NCCL 浅流水暴露它；平台修正后单连接 13.1→29.6GB/s；`NCCL_IB_SPLIT_DATA_ON_QPS=0`（完整变量名；默认 0，误设为 1 时每消息在 8 QP 间条带、单 QP 在途窗口缩 ~8×）后 358→456GB/s；`ADAPTIVE_ROUTING +22%` 修后复测无差（455.0 vs 455.2），证伪为同 artifact。
- perftest 反证收窄为其覆盖范围：同 rail、同粒度、同深度、同 buffer、同时段的成功**只排除该路径/参数/窗口**，深流水可掩盖平台路径问题（报告者最终回复修正开帖结论），NCCL 浅流水暴露它；**不保留普遍"先排除 fabric"规则**。
- 原因强度限报告者自述和所列比较：(1) 平台 ACS 重定向＋IOMMU Translated；(2) 配置 `NCCL_IB_SPLIT_DATA_ON_QPS` 误设（完整变量名；默认 0）。配置修复不等于库发布修复版本（NCCL 库版本未变更）。
- 关闭（[维护者回复](https://github.com/NVIDIA/nccl/issues/2409#issuecomment-5699369631)：stephenmsachs 按报告者请求关闭，不是独立复现双因）。
- 复用约 97% 时注明：456GB/s 约为报告者相对未独立核验期望（~470GB/s，引 nccl-tests#309，未实开）的估算，不作验收门槛。
- 可复用检查清单：时间窗三方对齐 → 同条件 perftest 反证（带 QP/深度/buffer 条件）→ 单变量 sweep → 修后复测证伪中间假说。
- 未定事项：交换机侧计数器原文未给出（unknown）；~470GB/s 期望来源未核验（unknown）。
- 相关案例索引：[NCCL #814](https://github.com/NVIDIA/nccl/issues/814)（实际观察：AMD CPU ＋ 6×RTX 4090 拓扑 XML ＋ p2p/pairwise 矩阵 ＋作者 ring 顺序调整未果（[作者关闭](https://github.com/NVIDIA/nccl/issues/814#issuecomment-1496450442)，未验证替代 CPU 即关闭）；维护者解释：AMD CPU 双向/多流交织影响流水（[首个回复](https://github.com/NVIDIA/nccl/issues/814#issuecomment-1493802672)，推断强度）；后续评论二则：[2.23 P2P 避让说明](https://github.com/NVIDIA/nccl/issues/814#issuecomment-2283482549)（不超出设置 `NCCL_P2P_LEVEL=PHB` 的效果）与 [GeForce P2P 支持边界澄清](https://github.com/NVIDIA/nccl/issues/814#issuecomment-2825666454)（不表示近期 GeForce 支持 P2P）；两条不合成 RTX 4090 修复/支持结论；`--bind-to none`、tree 流量解释、最慢链路因果证明**均无原文支持，已删除归属**）。

## 来源与验证记录

- [nccl-tests 固定快照](https://github.com/NVIDIA/nccl-tests/tree/b4d5beebca8a76cf01335f724d154b9b9d394d96)：计时/校验/页脚实现与参数语义。
- [NCCL 2.27.5 归档用户指南](https://docs.nvidia.com/deeplearning/nccl/archives/nccl_2275/user-guide/docs/)：env.html 的变量语义、troubleshooting.html 的官方排查建议、troubleshooting/ras.html 的 RAS 健康事件（注意 RAS 实际路径在 troubleshooting/ 下，顶层 ras.html 不存在）。
- [cann-hccl 固定快照](https://gitee.com/ascend/cann-hccl/tree/2d685b084a60366b47ad8e50a563ee5c4dbef7fe)：算法页定性机制与参考资料索引；仓库内无 HCCL Test 结果解释文档。
- [CANN 9.1.X《HCCL性能测试工具》](https://www.hiascend.com/document/detail/zh/CANNCommunityEdition/910/devaids/hccltool/HCCLpertest_16_0001.html)：算法带宽定义、参数、结果字段与规格约束；经 redirect 解析落点，redirect 为可变定位。
- [NCCL Issue #2409](https://github.com/NVIDIA/nccl/issues/2409)（主案例：环境/证据/反证/双因/配置侧修复；交换机计数器与 ~470GB/s 期望 unknown）、[NCCL Issue #814](https://github.com/NVIDIA/nccl/issues/814)（相关案例索引，个案不泛化）。
- [T03-06 三库能力对照](communication-library-profiles.md)（RCCL/HCCL 对照条件与版本边界）与 [T03-05 RCCL 档案](rccl-runtime-and-verification.md)（Replayer/TransferBench 工具说明）：对照轮版本/能力入口。
- 跨节点矩阵见[基线口径跨节点矩阵](bandwidth-baselines.md)（T03-07 已交付字段契约与判据，实测矩阵未交付；与正文 L34 及来源记录一致）。
- 逐条主张与证据定位见[本页作者来源记录](../../docs/research/batch-19-t03-08-sources.md)（[第九批带宽来源记录](../../docs/research/batch-09-bandwidth-sources.md)为历史范围）。
- 当前验证范围：来源核对；未构建或运行测试工具，未采集遥测。
- 待确认：HCCL Test 计时实现；链路级计数器：“可用来源缺失”指原批范围，当前 T03-03（UFM/mlx5/Cumulus）文档已核对可复用、目标机型字段能力 unknown；目标机型“应达带宽”的机型级依据。
