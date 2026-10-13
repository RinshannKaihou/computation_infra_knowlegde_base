---
id: communication.rdma-baseline-and-congestion-triage
title: RDMA 网络基线、路由与拥塞诊断
type: procedure
domain: communication
status: draft
platforms: [generic]
source_refs:
  - src.linux.perftest-26.07.8
  - src.linux.perftest-readme-26.07.8-fixed
  - src.linux.perftest-parameters-26.07.8-fixed
  - src.linux.rdma-core-v65.0
  - src.kernel.infiniband-user-verbs-v6.16-fixed
  - src.kernel.infiniband-sysfs-abi-v6.16-fixed
  - src.kernel.mlx5-en-stats-v6.16
  - src.kernel.mlx5-ib-counters-v6.16
  - src.kernel.mlx5-counters-doc-v6.16
  - src.kernel.net-statistics-abi-v6.16
  - src.nvidia.cumulus-43-monitoring-ethtool
  - src.nvidia.cumulus-43-monitoring-best-practices
  - src.nvidia.mlnx-ofed-586042lts-roce
  - src.nvidia.mlnx-ofed-586042lts-ib
  - src.nvidia.mlnx-ofed-586042lts-ecn
  - src.nvidia.mlnx-ofed-586042lts-flow-control
  - src.nvidia.ufm-41815-port-counters
  - src.nvidia.cumulus-43-roce
updated_at: "2026-10-10"
summary: "在 Linux RDMA 客户端与选定 NIC/交换机文档范围内，建立独立于 collective 的跨节点路径、拥塞和长尾判断流程：IB 子网/路由与 RoCE 网络分开（路径工具与计数器来源各自独立），计数器按 UFM 4.18.15 逐项核对方向范围，perftest 两节点/多节点对照（性能扫描与逐尺寸校验分开），基线下降四分法与停止恢复门槛；只给判据不填执行结果。"
related_ids:
  - communication.interconnect-paths
  - communication.ethernet-ib-roce-rdma
  - communication.bandwidth-baselines
  - communication.bandwidth-degradation-triage
applicability:
  environment_refs: []
  notes: "文档级样板已选型：样板 D-IB = perftest 26.07.8（a31f9ea，行号见来源节）+ rdma-core v65.0（58e4080，verbs 语义；完整九页差分未做）+ 内核 v6.16 tag 文件 + OFED 24.10-5.1.6.1（IB/SM 工具与路由引擎）+ UFM 4.18.15（IB 计数器）；样板 D-RoCE = 同客户端 + Cumulus 4.3（Spectrum ASIC，lossless/lossy 模式与交换机配置口径）。硬件样板 H1（文档级）：NIC 为 ConnectX-4 及更新——计数器字段以 v6.16 mlx5 驱动源 + counters.rst 语义为准（en_stats.c：prio marked/pause/storm 事件；IB vport 表字段附 vport_ 前缀；per-QP opcounters 经内核 rdma_counter 绑定，用户态入口未交付故 per-QP 判读待核定；cap 门控；FW 事件细则超出名义部分 unknown）；交换机端口以 Cumulus 4.3 双页引用链 + v6.16 net-statistics ABI 为准（2 秒/10 秒更新边界；ASIC 内部超出 netdev 视图部分 unknown）。具体型号/固件待定。未对准任何具体网络，不能据此认定适用。"
verification:
  status: not_verified
  evidence_refs: []
  notes: "流程未在真实 RDMA 网络执行：rdma-core 完整九页差分、NIC 具体型号/固件、per-QP 用户态管理读取入口、计数器累计位宽/FW 事件细则、ASIC 内部超出 netdev 视图部分待补；来源核对至多记 source_checked，不能记 reproduced。"
---

# RDMA 网络基线、路由与拥塞诊断

## 目标与触发条件

当跨节点带宽低于预期、尾延迟抖动或集合通信出现超时症状，且需要先排除网络本身时，进入本流程。目标是给出"独立于 collective 的网络结论"：路径是否符合预期、拥塞证据是否存在、基线下降归哪一类。本流程只给判据，**不填执行结果**；只有文档证据时明确为来源整理。

## 适用范围与前置条件

### IB 子网分支

- SM：每子网需要 subnet manager；active master 与 standby 区分（[DOCA 3.5.0 Glossary SM](https://networking-docs.nvidia.com/doca/archive/3-5-0/rdma-aware-networks-programming-guide) 局部术语：SM 主备边界）；`opensm.log`/`SUBNET UP` 只证明本节点所见状态。
- 分区/PKey：UFM 4.18.15 以 Xmit/Rcv Constraint Error 记录 FilterRaw、PartitionEnforcement（PKey/分区）、IP version 出向/入向检查失败（多因，需结合分区配置快照定位；版本化隔离样板，见机制文）。
- 路径工具（仅 IB）：`ibtracert`/`ibdiagpath`（路径）、`ibroute`（转发表）、`ibnetdiscover`（拓扑存档）。OpenSM 路由引擎（minhop/updn/ftree/DOR 等）按拓扑选择，fat-tree 要求对称否则回退；file 路由忽略拓扑变化。
- 计数器（仅 IB 端口）：UFM 口径（下表逐项），经 `ports/*/hw_counters/` 与 `ports/*/counters` 采集。

### RoCE 网络分支

- 无需 SM；按 GID/MTU/路由/rail 记录前提：GID 表、`cma_roce_mode`、VLAN/DSCP。
- 路径字段（L3）：下一跳/ECMP（UDP 源端口流标识，见机制文图 M-1）、rail 归属经交换机配置与 GID/VLAN 对齐；**IB 路由工具（ibtracert/ibroute/ibnetdiscover）不用于 RoCE 路径**，RoCE 路径快照 = GID 表 + L3 路由表 + 交换机侧 ECN/PFC 配置快照（Cumulus 4.3 lossy/lossless 口径），缺任一项记 unknown。
- 计数器边界（C09 修正）：OFED RoCE 章"RoCE offload 流量不关联 Ethernet **device driver** 的 counters"——仅指主机侧以太网驱动计数器；**不等于** RDMA NIC 硬件计数器或物理交换机 Ethernet/PFC/ECN 计数器没有该流量。三层（driver/netdev、RDMA NIC 硬件、交换机）分开记录来源，未取得的一层记 unknown。

### 版本前提

perftest 两端**同版本同参**（不同版本可能不互通）；`--data_validation` 仅 `ib_write_bw/ib_read_bw`、RC、`tx_depth>=32`（固定 README L515–523 不兼容表：另含 `-a`/`--post_list>1`/`--run_infinitely`/`--mr_per_qp`/`--gpu_touch`/`--use-null-mr`/`--payload_file_path`）。

## 需要的证据

| 证据 | 采集范围或定位 | 用途 | 缺失时如何处理 |
|---|---|---|---|
| 工具与版本快照 | perftest release+commit、NIC 型号/固件、链路 state/rate/width、NUMA 实际绑定证据、权限 | 口径可比性 | 缺失时不比较跨轮结果 |
| IB 快照 | LID/SM、分区、`ibnetdiscover` 拓扑文件、`ibroute` | IB 路径与前提 | 缺失时不做 IB 路由归因 |
| RoCE 快照 | GID 表、`cma_roce_mode`、VLAN/DSCP、L3 路由、`net add roce` 模式（lossless/lossy） | RoCE 路径与前提 | 缺失时不做 RoCE 路由归因 |
| 计数器窗口 | 下表 IB 逐项（UFM 4.18.15）；RoCE PFC/ECN 计数器分三层记录 | 拥塞与错误判读 | 单位/方向未核对时不下结论 |
| 校验输出 | `--data_validation` 的 errors/races/skips/retries（L536–563：仅 errors 为真问题） | 正确性门禁（覆盖率见 C12） | 无 validation 轮时不判链路健康 |
| 链路掩盖声明 | FDR LLR 掩盖 symbol error（以 `ibdiagnet` LLR 重传率 500/s 为调查线，非 FDR 不套用） | 避免漏报 | 未查 LLR 时注明 |

## 计数器语义（UFM 4.18.15，C10 逐项）

页内版本选择器当前为 4.18.15-LTS-2024-U5；tick 时长未知，**不得换算等待秒数**。下表按指标展开方向/范围/累积口径；reset/采样窗口以各采集工具为准，未统一声明的不假设。

| 指标 | 方向/范围/单位 | 语义与多因 | 判读列 |
|---|---|---|---|
| Xmit/Rcv Data | 端口级、全 VL；**单位 octets/4**（含错包、不含 link 包） | 正常流量基线（收发字节本来应随流量增长） | 正常流量：与同窗口基线比，不要求零增量 |
| Xmit/Rcv Packets | 端口级、全 VL；**单位 packet 数**（含错包、不含 link 包；不是四字节计数） | 正常流量基线 | 同上 |
| Rcv Errors | 收向；物理错（ICRC/VCRC/LPCRC）、畸形包、overrun 丢弃 | 错误计数 | 错误列：零增量要求适用 |
| Xmit Discards | 发向；端口 down **或**拥塞时丢弃（另含 NeighborMTU 超限、lifetime 超限） | **多因，非拥塞专用** | 停止信号之一，不是根因证明 |
| Symbol Errors | 物理 lane minor link error | 链路质量 | 错误列 |
| Link Error Recovery/Downed | 训练状态机恢复成功/失败 down 链路次数 | 链路事件 | 错误列；Downed 增量即停 |
| Local Integrity/Rcv Remote Physical | 本地物理错超阈 / EBP 定界符包 | 链路质量 | 错误列 |
| Xmit/Rcv Constraint Error | 出向/入向未传输/丢弃包：FilterRaw 条件、**PartitionEnforcement（PKey/分区）检查失败**、IP version 检查 | **多因（不只 PKey）**；不能单独证明 PKey 错，需结合分区配置快照 | 配置列，不判拥塞 |
| Rcv Switch Relay Error | DLID/VL 映射、环回 | 交换机转发 | 错误列 |
| VL15 Dropped | 管理 VL 资源不足丢弃 | 管理面 | 错误列 |
| XmitWait | 端口有数要发但整 tick 未发（信用不足或仲裁缺失），**单位 tick** | 流控/拥塞响应，**不是丢包数** | 拥塞响应列：与同窗口基线比 |
| Normalized XmitData | XmitData 增量 / Link Capacity（UFM 显示口径） | 有效利用率 % | 同上；公式仅 UFM 显示范围，不作通用可计算量 |
| Normalized Congested BW | (XmitWait 增量 / Time) × Link Capacity（UFM 显示口径） | 被抑制带宽估计 | 同上 |
| Normalized XmitWait | XmitWait 增量 / XmitPackets 增量；**仅算直连接收主机的端口** | 拥塞/包比 | 适用端口条件必注；不外推其他端口 |

样板内重试/CQE/ECN/PFC 测量字段（参数、计数、率三类分开；ECN/PFC 归 **RoCE 分支**，IB 分支只到 UFM 表为止）：

| 类 | 字段与入口（版本页） | 单位/方向/范围 | 说明 |
|---|---|---|---|
| 重试参数（配置，非计数） | RC QP `timeout/retry/rnr_retry`（`modify_qp` 逐 QP 可配） | 配置值 | 不能当作传输重试计数 |
| 传输重试计数（mlx5 IB 驱动 v6.16，`drivers/infiniband/hw/mlx5/counters.c`） | 重传队列 `duplicate_request` / `rnr_nak_retry_err` / `packet_seq_err` / `implied_nak_seq_err` / `local_ack_timeout_err`（`retransmission_q_counters` cap 门控）；耗尽 `req_transport_retries_exceeded` / `req_rnr_retries_exceeded`（`enhanced_error_q_counters` 门控）；RoCE 自适应 `roce_adp_retrans[_to]`、`roce_slow_restart[_cnps,_trans]`（`roce_accl` 门控）；经 `get_hw_stats` 读出（sysfs `hw_counters/` 路径存在性见 v6.16 ABI 文件） | 计数；按端口/vport 作用域；cap 不满足则无该字段 | FW 事件细则超出名义含义部分 unknown；**非 validator retries** |
| ECN 统计（mlx5 以太网驱动 v6.16，`en_stats.c` + `counters.rst`；RoCE 分支；本机标记口径） | `rx_prio{N}_marked` = 设备因 per-host 拥塞而 ECN 标记的包数（counters.rst L1280–1282；HW PPCNT per-TC-congest 组，N=0..7）+ 同作用域分母 `rx_prio{N}_packets` = 该 L2 priority 物理端口收包总数（L1224–1225）；另 `rx_prio{N}_cong_discard`（per-host 拥塞丢弃）、`rx_prio{N}_buf_discard`（per-host 收缓冲不足丢弃）；入口 `ethtool -S` | 包数；收向；同设备/端口/优先级/窗口 | **本机标记占比 = Δmarked/Δpackets（Δpackets>0；缺字段/零分母/回退/重置/窗口不齐 unknown）**；不是网络已标 CE 的 RoCE 收包比例；IB `np_ecn_marked_roce_packets` 为另一观察点，需其 RoCE 统计范围匹配的分母，不拿物理端口全包数代替 |
| ECN/CNP（mlx5 IB 驱动 v6.16，同文件；cong 表受 `cc_query_allowed` 门控，vport 分支不提供 device cong 表） | `rp_cnp_ignored` / `rp_cnp_handled`、`np_ecn_marked_roce_packets`、`np_cnp_sent`（FW `query_cong_statistics`；端口/device 级） | 计数；端口/device 作用域 | FW 事件细则超出名义部分 unknown |
| ECN/CNP per-QP（同文件，分支待核定） | 完整字段名 `cc_rx_ce_pkts`（`basic_op_cnts`）/ `cc_rx_cnp_pkts`（`rdmarx_cnp_op_cnts`）/ `cc_tx_cnp_pkts`（`rdmatx_cnp_op_cnts`）（counters.c L131–141）；内核侧经 `rdma_counter` QP 绑定（`mlx5_ib_counter_bind_qp` → `mlx5r_fs_bind_op_fc`，`bind_opcnt` 模式门控统计更新；counters.c L578–642/L1199–1217）——**不是**用户态 `ibv_create_counters`/`ibv_read_counters`（`ib_counters` flow 对象，提供配置的 packets/bytes description，不自动提供上述命名字段） | per-QP（绑定后） | 用户态管理/读取入口未交付，per-QP 判读维持待核定 |
| 交换机端口统计（Cumulus 4.3 双页引用链 + 内核 v6.16 ABI） | 入口页：[Monitoring Best Practices](https://docs.nvidia.com/networking-ethernet-software/cumulus-linux-43/Monitoring-and-Troubleshooting/Monitoring-Best-Practices/)（计数器来自硬件或内核，内核汇总硬件；`cat /sys/class/net/[iface]/statistics/[stat_name]`，该表轮询 10 秒）与 [ethtool 监控页](https://docs.nvidia.com/networking-ethernet-software/cumulus-linux-43/Monitoring-and-Troubleshooting/Troubleshooting-Network-Interfaces/Monitoring-Interfaces-and-Transceivers-Using-ethtool/)（Mellanox 交换机物理计数器向内核每 2 秒更新、虚接口 10 秒，高负载更长；`ethtool -S swpX`：`HwIfInOctets/UcastPkts/.../HwIfInDiscards/HwIfInBufferDrops/HwIfInAclDrops/...`；`cl-netstat -c` 不清内核/硬件计数器）；字段语义：v6.16 `sysfs-class-net-statistics`（rx/tx packets/bytes/errors/dropped 等，计数，收发分开，按端口 netdev；ABI errors/dropped 含义按驱动确定，不互加） | 采样须记录 2 秒（/10 秒）更新边界，未更新不得认作同窗零新增 | ASIC 内部超出 netdev 视图部分 unknown |
| CQE 错误 | `poll_cq` `status`/`vendor_err`（失败四字段）+ `IBV_EVENT_CQ_ERR`（CQ overrun 不可用） | 事件/错误码 | 见机制文分阶段映射 |
| ECN 配置（RoCE） | `enable/<X>` 查询/使能（X=0..7，按优先级）与 `params/<requested attribute>` 读/改（参数名是属性名，不是优先级数字；**不存在 `/params/0` 这类入口**）分开；算法 roce_rp（反应点）/roce_np（通知点）（OFED ECN 页 Enabling ECN） | 按设备/端口/优先级 | 配置参数，非标记率 |
| ECN 统计（OFED 页 + 驱动字段） | OFED 页仅声明"parameters and statistics … per device, per port, per priority"（"Next Slide" 未取得正文），逐统计字段名以 mlx5 驱动字段为准（上表），不混用 | 以驱动字段为准 | OFED 页不作统计字段来源 |
| PFC 配置 | `mlnx_qos --pfc` 按优先级开关（页内标题为 ConnectX-4 and above；**"及更新"不自动证明后续型号逐项字段一致，H1 只声明已证入口**，流控页） | 按端口/优先级 | 配置参数 |
| dropless_rq（配置开关） | `ethtool --set-priv-flags <dev> dropless_rq on/off`（默认关；要求 Flow Control 同开；流控页 Dropless RQ 节） | NIC 驱动特性开关 | 配置参数，非计数 |
| out_of_buffer（两条同名不同作用域，分开） | IB 侧 `vport_out_of_buffer`（vport 表，`INIT_VPORT_Q_COUNTER` 附 `vport_` 前缀，counters.c L22–24/L46–52；经 sysfs `hw_counters/`）**与** mlx5e 侧 `rx_out_of_buffer`（qcounter 组 `q_stats_desc`，en_stats.c L552–560；FW `QUERY_Q_COUNTER` 读出 L613–634；经 `ethtool -S`，en_ethtool.c `get_ethtool_stats`）；两者作用域不同（IB counter-set/vport vs mlx5e qcounter），不声明值一一相同 | 按各自作用域 | 语义：dropless 超时丢包（流控页）；累计位宽/FW 细则 unknown |
| PFC 计数（RoCE/NIC 硬件） | `ethtool -S`：`prio{N}_{rx,tx}_{octets,frames,pause,pause_duration,pause_transition}`（N=0..7；pause 类仅 PFC 使能优先级可见）；`pause_duration` 单位为微秒（counters.rst）；另 `tx_pause_storm_warning/error_events`（device_stall 水线事件） | 收发分开 × 8 优先级；octets/frames/次/微秒 | 同窗增量比较；storm 事件进停止门禁 |

采样与回绕：同窗 delta = 窗起止快照相减；计数器回绕位宽未逐项核定——若后快照小于前快照，该窗记 unknown（不比较、不外推回绕修正），原始快照存档。缺字段的停止/恢复门槛维持无法判断（见下表方法行）。

零增量只用于有依据的错误项（Rcv Errors、Downed、Constraint 等）；正常流量与流控/拥塞响应计数与同窗口基线比较。停止是风险控制而非根因证明；恢复前保留原始证据（计数器快照存档），**不要求无依据地清零设备计数器**（"事件清零后"一律指"新采样窗零新增"，不是设备计数器归零）。

## 步骤与判断分支

| 步骤 | 检查或动作 | 运行影响 | 预期证据与解释 | 下一步 |
|---|---|---|---|---|
| 0 | 建基线 G0：两节点；`ibnetdiscover`（IB）或 GID+L3（RoCE）存档；性能扫描（`-a` 全尺寸）与逐尺寸校验分开两轮（互斥，L515–523）；单流 `-q 1`；隔离无背景流；同口径三轮；每轮原始统计存档（latency 轮 min/median/max；BW 轮 bw_peak/bw_avg/msgRate_avg），跨轮聚合见 G1 | 低：独占链路窗口 | 基线聚合值 + 错误列零增量；校验轮 errors=0 且覆盖门禁通过（下） | 进入对照组 |
| 1 | 消息维度 G1：三档固定 message size——64B（时延区）/ 64KB（中间区）/ 4MB（带宽区）；选择规则：覆盖 latency 与 BW 两种测试类型，工具默认 BW size 65536（DEF_SIZE_BW）被本设计显式覆盖，不跨档比较"退化"，MTU 对齐在 NIC 选型后复核。迭代显式固定（不用"默认"）：BW 轮 iters=5000（与 WRITE/WRITE_IMM 默认 DEF_ITERS_WB 对齐，两端同值；固定 .c L1030–1031/.h L105–106），latency 轮 iters=1000（DEF_ITERS）；时长模式（`-D/-N/-H`）与迭代模式二选一声明。聚合规则：latency 取三轮 median 的 median，基线带 = 三轮 median 的 [min, max]；BW 取三轮 bw_avg 的 median（peak 另行记录，不混入聚合），基线带 = 三轮 bw_avg 的 [min, max]；超出带即进入四分法。`--report-cycles` 仅 latency 轮 | 低 | 各档独立基线带；**不跨档比较"退化"** | 选档进入 G2 |
| 2 | 单流/多流 G2：`-q 1` vs `-q 4/8`（多 QP 校验示例存在，不判不支持），配 CQE 轮询批量记录；host/device buffer 路径分开声明 | 中：多流打满 | 多流增益；validation 轮结论限带宽对照（含校验吞吐差不归因网络） | 进入 G3 |
| 3 | 隔离/争用 G3：单流被测 + 可控背景流（第二对 QP/节点/进程，不用推理负载冒充 RDMA 背景；多进程背景注明 validator 竞争降覆盖）；被测与背景 SL/GID/端口分开 | 高：背景流占用 | 争用轮仅与同争用基线比；拥塞以计数器增量为准，不以带宽差反推 | 进入 G4 或判读 |
| 4 | 多节点 G4：≥4 节点，单流逐对 + IB `ibroute` 快照 **或** RoCE L3+GID+交换机配置快照（二选一对应，不互代）；all-to-all-shift 仅作 `ibcongest` 静态分析输入 | 高 | 路径快照对齐计数器窗口 | 四分法判读 |
| 5 | 四分法：测试口径 / 路由映射 / 主机 / 真实网络 | 只读分析 | 口径差异解释、配置/映射原因、链路同期遥测+路径对齐、证据不足记 `unknown` | 满足完成判据后结束 |

计时口径（固定 README L59–81）：CPU cycle counter 取时间戳时避免上下文切换开销（计时调用层面，**不是被测进程全程无切换**）；latency 报 RTT 一半（非对称不准）；单向 BW 由 client 测量（双向各测自发）；latency 报 min/median/max（首值多为最大系 warmup）；`-D/-N/-H` 改变采样口径。

NUMA（固定 README L376–401 + 参数检查 L2463–2471，C11 修正）：默认读 NIC NUMA 自动绑定线程+内存；NIC NUMA 不可知时不绑定继续跑；`--pin_cores`  pin 指定核；`--numa_node` 绑指定节点；`--disable_numa` 关自动绑定。互斥关系只有：`--numa_node` 分别与 `--pin_cores`、`--disable_numa` 互斥（parse 期拒绝；pin_cores+disable_numa 不在拒绝之列）。外部 CPU 限制（taskset/numactl）：检测到则跳过自动绑定，但显式 `--pin_cores`/`--numa_node` 会覆盖外部绑定——**优先级：显式参数 > 外部限制 > 自动检测**；需 libnuma（numa_node 与自动检测），pin_cores 任意 Linux 可用；raw Ethernet 不支持 NUMA 选项。记录请求配置与实际绑定证据（输出头 active NUMA），未运行不填实际放置。

校验覆盖与分支依赖（固定 README L429–459/L472–490/L536–563；实现 host_validation.c/resources.c）：

- validation 自身降带宽（尤其 READ 模式开销；huge pages 缓解 TLB；ARM 另议；非对齐 payload 轻微降速）。
- 多进程并发 validator 争 CPU/GPU/内存/PCIe → 落后块记 skipped/stale → 覆盖下降、正确性可靠性受影响。
- `errors=0` 只说明**已检查部分**未报损坏；必须同轮记录 races/skips/retries 与覆盖声明；含校验与不含校验的吞吐差不得直接归因网络。
- 性能扫描轮（`-a`）与逐尺寸校验轮分开；单进程多 QP、多进程背景的条件各自声明。
- 后端固定为 host（本流程覆盖门禁以后端 host 为准；device 轮须另行映射其输出字段后方可纳入，否则记 unknown，不混用两套字段；`--use_cuda` 的 `libperftest_kernels.so` 为构建期自动探测、运行时 dlopen，仅作分支存在性说明，不作门禁依据）。
- host 校验分支依赖：SIMD 后端（AVX-512/AVX2/SSE4.2/NEON，configure 期选择；跨机二进制缺指令集时 validation 不可用，需在目标机重建）；多 NUMA validator 线程并行 polling。
- host 实际输出字段与粒度（同粒度比较，不跨单位相除）：`chunks_validated` 累加的是 `work_items_processed`（单位：操作数；host_validation.c L1127–1154），`bytes_validated`（字节），`errors_found`，`markers_scanned/hit`（marker 数），`skipped_steps`（marker 步数，`delta-1` 累加，L600–602），`race_overwrites`/`dma_stale_retries`；`queue_full_drops`/`stale_work_skips` 在 host 后端恒 0（L1152–1153），不得跨后端相加称覆盖率。一个 marker 对应 `ops_per_chunk`（= `validation_chunk_size`，由 size/tx_depth 推导，.c L1625–1637）个操作，`chunk_bytes = ops_per_chunk × payload_size`；BW 报告 `iters` 在迭代模式已乘 `num_of_qps`（.c L4802），即操作数口径。
- 覆盖门禁（同粒度规则）：(a) `errors_found==0`；(b) `chunks_validated>0`（==0 时实现直接 FAILURE 并打印 "no data validated"，resources.c L7360–7363）；(c) 已校验操作占比 = `chunks_validated` / 本轮报告 `iters`（同为操作数口径），落在 G0 同档三轮该比值的 [min, max] 带内；(d) `skipped_steps`（marker 步单位，只与 G0 同设计 marker 步带比，不除以操作数）。任一条不满足→覆盖不足→该轮记 unknown（不判健康，不进 G0）；失败分支：errors>0、工具初始化/停止失败、WARNING/"no data validated"、分母缺失或零验证量即停（见停止条件正确性行）。G0 建基线轮须满足同一门禁，否则基线无效重建。

## 停止条件与恢复安排

门槛是"何时停、何时恢复测试"的程序规则；触发后只允许回到隔离基线，不允许直接改 PFC/ECN/路由/SM 配置（配置变更属变更窗口，另行授权）。

| 信号 | 停止门槛 | 恢复门槛 |
|---|---|---|
| 正确性 | validation `errors_found>0`（真问题）；或"no data validated"/WARNING/工具初始化·停止失败/分母缺失；或同窗口 Rcv Errors 类增量 | 查清同参后重跑隔离单轮并通过覆盖门禁（a–d 全过）且错误列新窗零新增，连续 2 轮 |
| 拥塞响应 | `XmitDiscards` 增量>0（停机排查多因）；或 pause storm 事件增量（`tx_pause_storm_warning/error_events`，mlx5 v6.16 驱动字段分支）；本机标记占比（同设备/端口/优先级/窗口 Δmarked/Δpackets，Δpackets>0；仅 mlx5 驱动字段分支，其余维持无法判断，只记 unknown，不默认网络 CE 比例） | 暂停背景后响应计数回落基线带内、错误列新窗零新增，连续 3 采样窗 |
| 链路 | Link Error Downed 增量；或 LLR 率超 500/s（FDR 链路限定） | 证据存档后，新隔离单轮复测速率/宽度一致且错误列零新增 |
| 主机 | 实际绑定偏离记录或端口非 ACTIVE | 纠正后重建 G0 单轮基线点 |
| 方法 | 两端版本/参数不一致、基线缺失、快照未存档 | 结果记 `unknown`；补齐后重跑 |

完成判据（四选一）：(a) 口径差异解释；(b) 定位配置/映射原因并同口径复测确认；(c) 链路支路有同期遥测+路径对齐；(d) 证据不足记 `unknown` 并列缺失项。**"带宽回升"单独不算完成。**

## 来源与验证记录

- [perftest 26.07.8](https://github.com/linux-rdma/perftest)（仓库入口）；[固定 README](https://github.com/linux-rdma/perftest/blob/a31f9ea9df720ee68f941e55f75fec31349fcd35/README)（L59–81 计时、L376–401 NUMA、L472–490 开销、L515–523 互斥、L536–563 计数器）；[固定参数实现](https://github.com/linux-rdma/perftest/blob/a31f9ea9df720ee68f941e55f75fec31349fcd35/src/perftest_parameters.c)（L2463–2471 NUMA 互斥）。
- MLNX_OFED 24.10-5.1.6.1 LTS：[RoCE](https://networking-docs.nvidia.com/mlnxofedswum/586042lts/rdma-over-converged-ethernet-roce)（offload 计数器边界、GID/路由三小节）、[IB 接口与计数器位置](https://networking-docs.nvidia.com/mlnxofedswum/586042lts/infiniband-network)（IB 工具表）、[ECN](https://networking-docs.nvidia.com/mlnxofedswum/586042lts/explicit-congestion-notification-ecn)、[流控](https://networking-docs.nvidia.com/mlnxofedswum/586042lts/flow-control)。
- [UFM 4.18.15 端口计数器](https://networking-docs.nvidia.com/ufmsdnappswum/41815/infiniband-port-counters)（上表全部逐项语义；版本选择器 4.18.15-LTS-2024-U5）；[Cumulus 4.3 RoCE](https://docs.nvidia.com/networking-ethernet-software/cumulus-linux-43/Network-Solutions/RDMA-over-Converged-Ethernet-RoCE/)（lossless/lossy 双模式、Spectrum 限定、RoCEv1 trunk）。
- 逐条主张与证据定位见[第十八批 RDMA 基线来源记录](../../docs/research/batch-18-rdma-baseline-sources.md)。
- 当前验证范围：来源核对；rdma-core 完整九页差分、NIC 具体型号/固件、计数器累计位宽/FW 事件细则、ASIC 内部超出 netdev 视图部分待补；未在真实网络执行。
- 待确认：见取证 unknown 清单；T03-01/T03-02 前置验收后复核引证。
