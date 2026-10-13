# 第十八批 T03-03 RDMA 基线来源记录

任务：T03-03（`rdma-baseline-and-congestion-triage.md`，procedure，not_verified）。取证日期 2026-10-09。固定：perftest 26.07.8（a31f9ea，行号待重核）、rdma-core tag 待定、内核 v6.16 或另行固定、OFED 586042lts、UFM 4.18.15、Cumulus 4.3（或 5.x 重核）；NIC/交换机未选型。

## 候选来源（3 项新登记 + 复用）

新登记：perftest-26.07.8（README 方法框架）、ufm-41815-port-counters（IB 计数器语义）、cumulus-43-roce（RoCE 配置示例，URL 经 Network-Solutions 路径修正并复核 200）。复用 rdma-core/内核/OFED 四页。

## 主张—来源定位表

IB/RoCE 分开（SM 页 + RoCE 页）；封装边界（RoCE 章 + Cumulus）；GID/路由（RoCE 章三小节）；MTU/路由观测（ibv_devinfo + fabric 工具表）；路由算法不泛化（SM 页）；计数器分层（IB 接口页 + RoCE 章）；IB 计数器语义（UFM）；perftest 同参/计时/NUMA/校验（README）；四分法与停止恢复门槛（方法定义，不填结果）。

## unknown 清单

perftest commit 行号、rdma-core tag、内核选型、NIC/固件/交换机选型、计数器逐项语义、IB/RoCE 示例细节、IBTA 全文、S26/S27 弱相关、procedure 空环境块、T03-01/02 前置复核、许可限制。见取证报告 §5 全表。

## 2026-10-10 修订（B18-C04、C09–C12）

- C09：IB/RoCE 路径与计数器来源分列；RoCE 计数器边界修正为三层（driver/netdev、NIC 硬件、交换机）；SM 主备（DOCA Glossary）；RoCE 快照=GID+L3+交换机配置；G4 双快照二选一。
- C10：UFM 4.18.15 全表逐项转录（Xmit/Rcv Data octets/4；Discards 多因；XmitWait tick 非丢包；Normalized 三公式与端口条件；Constraint 含分区检查）；正常/响应/错误三列；零增量仅错误列；tick 不换算秒；恢复=新窗零新增。
- C11：perftest README L376–401 + parameters.c L2463–2471：互斥仅 numa_node×pin_cores、numa_node×disable_numa；优先级显式>外部>自动；计时 L59–81 取时间戳层面。
- C12：README L472–490（validation 开销/竞争降覆盖/skipped-stale）+ L536–563（仅 errors 真问题）+ L515–523（互斥）；性能扫描与逐尺寸校验分轮；errors=0 限已检查部分。
- C04：perftest 行号按 a31f9ea 固定并分拆登记；rdma-core tag 待定如实保留；内核改固定文件。

## 2026-10-11 第二轮修订（B18-C04、C10、C12）

- C04：诊断样板选型 D-IB（perftest 26.07.8 + rdma-core v65.0 + v6.16 文件 + OFED 24.10-5.1.6.1 + UFM 4.18.15）/ D-RoCE（同客户端 + Cumulus 4.3）；NIC/交换机型号未选，逐项固件/交换机语义仍 unknown，流程仅文档级待执行设计。
- C10：Packets 单位修正（包数）；Constraint 多因（FilterRaw/PKey/IP version，需结合分区快照）；补样板内重试/CQE/ECN/PFC 指标与同窗 delta；回绕位宽 unknown；Normalized 为 UFM 显示口径，不作通用可计算量。
- C12：G1 设计值（64B/64KB/4MB 三档 + 选择规则；迭代默认 1000；统计与基线带 [min,max] 推导规则）；host/device 校验分支依赖（SIMD configure 选择/目标机重建；CUDA 插件自动构建 + dlopen）；资源隔离规则；覆盖判据与失败分支。

## 2026-10-12 第三轮修订（B18-C04、C10、C12；状态说明）

- 状态说明：本记录第 3 行"rdma-core tag 待定"与第二轮追加节 C04 句为 2026-10-09/10-10 历史状态；现行选型为 D-IB/D-RoCE 样板均采用 rdma-core v65.0（58e4080，verbs 语义），未完成的是完整九页差分（见正文 applicability/verification 现行注记）。历史节保留，不代表现行状态。
- C10：ECN 页（canonical 24.10-5.1.6.1lts，本轮只读取得）：sysfs enable/params 按设备/端口/优先级（roce_rp/roce_np，X∈{0..7}）；统计口径存在但逐字段名未转录→标记率判据无法判断。流控页：ConnectX-4+ `mlnx_qos --pfc`；`ethtool -S` prio{N}_rx/tx_octets/frames/pause/pause_duration/pause_transition（收发×8优先级；pause 类仅 PFC 使能优先级可见；pause_duration 单位未核定）。正文测量表改参数/计数/率三类，ECN/PFC 归 RoCE 分支；重试计数未取得（validator retries≠传输重试）；回绕记 unknown 分支。
- C12：迭代显式固定（BW 5000 = DEF_ITERS_WB，.c L1030–1031/.h L105–106；latency 1000；工具默认 BW size 65536 被设计显式覆盖）；BW 聚合 = 三轮 bw_avg 的 median（peak 另记；单轮无 median，.c L4829–4831）；覆盖门禁 = errors==0 且 (skips+stale)/iters 落 G0 同档带；硬件样板 H1（ConnectX-4+ 入口/UFM/Cumulus；型号固件待定）。

## 2026-10-13 第四轮修订（B18-C10、C12）

- C10：ECN 入口纠正（`enable/<X>` 与 `params/<requested attribute>` 分开；无 `/params/0`）；PFC 配置行加"及更新"不限定后续型号声明；H1 注记同步。传输重试计数、ECN 逐统计字段、交换机侧统计继续 unknown（页内无字段，不补造）。
- C12：覆盖门禁改同粒度规则——后端固定 host；实际输出字段（chunks_validated=Σwork_items_processed 操作数、bytes/errors/markers/skipped_steps marker 步、host 后端 queue_full/stale 恒 0）；ops_per_chunk=validation_chunk_size（size/tx_depth 推导），BW iters 已乘 num_qps；门禁 a–d（含 chunks_validated==0 即 "no data validated" FAILURE、占比同操作数口径、skipped_steps 只与同设计带比）；正确性停止行加 init/stop 失败与 WARNING/no-data；G0 同门禁。

## 2026-10-14 第五轮修订（B18-C10、C12；取证尝试记录）

- C12（P3）：修正本记录 L40 倒置——`chunks_validated==0` 即 "no data validated" FAILURE（resources.c L7360–7363），与正文一致。
- C10 取证尝试（均只读，未新增登记）：ECN canonical 页正文仅列参数入口与"parameters and statistics … per device, per port, per priority"范围声明（"Next Slide" 为引用标记，静态 HTML 无载荷），无逐统计字段名；流控页为 prio 收发计数 + dropless 开关语义 + out_of_buffer 丢包计数语义三者分开——其中 `dropless_rq` 为 `ethtool --set-priv-flags` 功能开关，`out_of_buffer` 为 RQ 满超时未补 WQE 的丢包计数（两者分开，前者非计数）；IB 章 canonical 页为索引（无计数器内容）；OFED 树 pagetree 无独立计数器/统计页；QoS 页仅配置（mlnx_qos/tc_wrap），无计数语义；UFM 表已全转录（前轮接受）。结论：版本化的传输重试计数、ECN 逐统计字段、交换机侧统计字段在本批已取官方入口内无字段可转录，逐项 unknown 保留；C10 是否关闭由复核判定，不宣布必交项通过。

## 2026-10-14 第七轮修订（B18-C10：版本化字段交付）

- 新增 3 项登记（375→378）：mlx5 以太网驱动计数器表（en_stats.c）、mlx5 IB 驱动计数器表（counters.c）、netdev 统计 ABI（sysfs-class-net-statistics），均为 v6.16 tag、raw 200 核对，原文不入库。
- 传输重试：retrans 表 5 字段 + 耗尽 2 字段 + RoCE ACCL 5 字段（cap 门控 + get_hw_stats/sysfs 读出）；validator retries 不互换（保留）。
- ECN 统计：`rx_prio{N}_marked` + 同作用域分母（驱动字段分支，率可计算）；IB 侧 cong/CNP/opcounters（per-QP 经 verbs flow counters）；OFED 页不作统计字段来源（保留）。
- 交换机统计：Cumulus swpX netdev + v6.16 net-statistics ABI（ASIC 内部 unknown 保留）。
- 停止/恢复拥塞行改条件分支（驱动字段分支可算，非分支 unknown）；FW 事件细则、累计位宽、具体型号固件继续 unknown（诚实保留，由复核判定）。

## 2026-10-14 第八轮修订（B18-C10：采集映射与口径修正）

- out_of_buffer 拆分一次源核对：IB `vport_out_of_buffer`（vport 表 vport_ 前缀，经 sysfs hw_counters）vs mlx5e `rx_out_of_buffer`（qcounter 组 q_stats_desc，FW QUERY_Q_COUNTER 读出，经 ethtool -S）；作用域不同，不声明值相同。
- per-QP opcounters 修正：完整字段名 cc_rx_ce_pkts/cc_rx_cnp_pkts/cc_tx_cnp_pkts；内核 rdma_counter QP 绑定路径（bind_qp→bind_op_fc，bind_opcnt 门控）；用户态 ibv_create/read_counters 为 ib_counters flow 对象，不提供上述命名字段；用户态管理/读取入口未交付→per-QP 判读待核定（port/device cong 分支保留）。
- ECN 率限定本机标记口径：counters.rst（新登记）marked=per-host 拥塞标记、packets=同级收包总数；Δmarked/Δpackets（Δpackets>0）；IB np_ecn_marked 另观察点（需匹配分母）；停止表改本机标记占比名称与条件。
- 交换机引用链：Cumulus Best Practices（统计入口页，新登记）+ ethtool 监控页（HwIf* 字段与 2 秒/10 秒更新边界，新登记）+ v6.16 net-statistics ABI（字段语义）；ABI errors/dropped 按驱动确定，不互加；cl-netstat -c 不清内核/硬件。
- pause_duration 单位纠正为微秒（counters.rst）；其余 FW 细则/位宽/型号固件/ASIC 内部 unknown 保留。
