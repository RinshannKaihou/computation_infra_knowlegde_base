# 第十八批第七次定向复核

**后续进展：第八次定向复核关闭 C10，累计 16 CLOSED / 0 OPEN，Batch 18 在原定有限文档范围内通过。** 见[第八次复核](batch-18-codex-eighth-recheck.md)；正文仍 draft，基线 not_verified，无实机验证。以下为第七次历史输入与判定，不作为最新状态。

复核日期：2026-10-10（Asia/Shanghai；输入快照时间 2026-10-10 03:21:06 UTC）。作者第七轮修订节标注 2026-10-14，保留为作者标签；以以下 SHA-256 识别实际复核输入，不由标签推导执行日期。

**结论：C10 继续 P2 OPEN，Batch 18 仍暂不通过；累计 16 项保持 15 CLOSED / 1 OPEN，无新增发现 ID。** 新增三项 v6.16 来源和字段存在性已复验，前轮“没有实际字段”的状态已有进展；仍有 out_of_buffer 与 per-QP 统计的错误采集映射，以及测量语义和引用衔接需要修订。此前 15 项 CLOSED 保持，T03-01/T03-02/T03-04 的有限文档通过范围保留。

约定模型 / effort 为 `gpt-6.1-sol / xhigh`，本会话 Codex 主助手执行，未派发子代理；实际运行标识没有可独立核验的元数据，沿用[初审说明](batch-18-codex-review.md)。依据[路线图](../full-coverage-roadmap.md)、[T03-03 验收](../../plans/full-coverage-backlog.yaml)、[写作指南](../authoring-guide.md#7-批次审阅约定)、[归属边界](../../content-outline.md)及 [AGENTS](../../AGENTS.md)，按[第六次关闭条件](batch-18-codex-sixth-recheck.md)复核新增字段及其影响，不扩大为实机验证。

## 输入身份与范围

| 输入 | SHA-256 |
|---|---|
| [RDMA 基线正文](../../knowledge/03-communication/rdma-baseline-and-congestion-triage.md) | `9fa2ae1e7cc0f8c45fd714daf2dec3f1fdf023807682bae4ec1f16cdc59813e0` |
| [基线研究记录](batch-18-rdma-baseline-sources.md) | `bc91a56e727fd01012265d424720ed8e7081cd69c2935b3d464fcbca3cd47adc` |
| [修订映射](batch-18-review-fixes.md) | `86d896497806c8cf40db8fd83541581d13ca9c44cb8bd312218939e80087949e` |
| [来源审计](batch-18-source-audit.md) | `5d26cc97b53a5367f4cdc79eb76313770833067f5da6145489aae04e2959eb03` |
| [来源登记](../../sources/registry.yaml) | `382c7a34bcd7b136a1f35eb685150d1d07f970815218001aa5aebbb999635366`（378 项） |

互联路径、RDMA 机制、集合正文及对应三份研究记录与[第六次输入](batch-18-codex-sixth-recheck.md)相同；章索引仍为 `9102358b1e7d08455114dda724b0e3bb24ecdb06118eece19b80dc9d003989e5`。本轮读取基线新增测量行、适用/验证注记、停止表、研究记录第七轮节、修订映射及三项新增登记，不重开 C12/C14 或其他已关闭项。

## 一次源复验

网页工具未取得 GitHub raw 文件，随后用默认 TLS 校验的 curl 只读取得下列精确来源，均 HTTP 200。原文只在临时目录，不入库、不编译或执行。前三项是作者本轮交付的主文件；其余用于核对同 tag 的语义、不同统计 API 与 Cumulus 4.3 的版本衔接，不宣称所有远端链接本轮重抓。

| 精确来源 | 字节数 | SHA-256 |
|---|---:|---|
| [mlx5 en_stats.c v6.16](https://github.com/torvalds/linux/blob/v6.16/drivers/net/ethernet/mellanox/mlx5/core/en_stats.c) | 95081 | `9f5eea7c1b082983ec36c6a09e5ea9599575c83fdcec039ef06cee3bfd9a5a06` |
| [mlx5 IB counters.c v6.16](https://github.com/torvalds/linux/blob/v6.16/drivers/infiniband/hw/mlx5/counters.c) | 34987 | `292177935746d101ab81811cccbc5d49a833a30eb90c793353f1340d79686246` |
| [net-statistics ABI v6.16](https://github.com/torvalds/linux/blob/v6.16/Documentation/ABI/testing/sysfs-class-net-statistics) | 7294 | `b6d77eab5d6a59ca25aca74cf7be5af8efa926baeb0188f64f6b58457efb2fb9` |
| [mlx5 counters.rst v6.16](https://github.com/torvalds/linux/blob/v6.16/Documentation/networking/device_drivers/ethernet/mellanox/mlx5/counters.rst) | 48415 | `838baabf8e0d91539db795bbeebdaeca5e2d79067648bd7c246577a999a3d482` |
| [mlx5 en_ethtool.c v6.16](https://github.com/torvalds/linux/blob/v6.16/drivers/net/ethernet/mellanox/mlx5/core/en_ethtool.c) | 82340 | `d753fd21f57283a30fbfd169bf57ede90fd412c791e4bbf14f0a69aed75c060a` |
| [mlx5 IB fs.c v6.16](https://github.com/torvalds/linux/blob/v6.16/drivers/infiniband/hw/mlx5/fs.c) | 97431 | `fcfd60b23b532ad9b920795f2cee5a8985a75a6e31779d89a461e77d4f43cc62` |
| [InfiniBand sysfs ABI v6.16](https://github.com/torvalds/linux/blob/v6.16/Documentation/ABI/stable/sysfs-class-infiniband) | 28133 | `04e19b90171502f140496137f1be0a6c0ec5c34195d673fccfaeae4155dc4512` |
| [Cumulus 4.3 Monitoring Best Practices](https://docs.nvidia.com/networking-ethernet-software/cumulus-linux-43/Monitoring-and-Troubleshooting/Monitoring-Best-Practices/) | 71791 | `d1ce189bcb654d4789db2308849e61e3f5d9322b4ebed38dda3ba4dcaa7eb472` |
| [Cumulus 4.3 Monitoring Interfaces and Transceivers Using ethtool](https://docs.nvidia.com/networking-ethernet-software/cumulus-linux-43/Monitoring-and-Troubleshooting/Troubleshooting-Network-Interfaces/Monitoring-Interfaces-and-Transceivers-Using-ethtool/) | 53576 | `4ce2af2e00cd4bcab173ad814929d9cac0d21f261ffeea2d23e3753caac11332` |

## 已接受的交付

- **重试相关字段已取得。** `counters.c` L38–44、77–96 及 L700–728 确认五个 retrans 字段、两个耗尽字段和五个 RoCE ACCL 字段及各自 cap 门控；L284–303、375–430、538–566、1196–1222 确认查询和 `get_hw_stats` 接入。它们是不同的重试/异常/自适应事件计数，不能合加成统一总重传包数；本轮没有要求 FW 未公开的全部事件细则。端口、device 和 vport 分支需按实际提供的目录/模式区分，vport 字段名由宏附 `vport_` 前缀（L22–24）。
- **ECN/CNP 字段及 pause storm 字段确实存在。** `en_stats.c` L1679–1681、1811–1817、1864–1872 确认 marked、包/字节、丢弃及 stall 事件字段；marked 组受 `sbcam_reg` 门控。IB cong 表为 L70–75，受 `cc_query_allowed` 门控，vport 分支不提供这一 device cong 表（L730–738、400–402）。这些计数与配置开关分开可以接受。
- **不把驱动组名差异判为优先级不一致。** 虽然 marked 与 packets 查询不同 PPCNT 组，同 tag 的 `counters.rst` L1206–1225、1271–1282 明确把它们放在 L2 priority（0–7）范围。不能仅由 `PER_TRAFFIC_CLASS_CONGESTION_GROUP` 与 `PER_PRIORITY_COUNTERS_GROUP` 的名字推断两个 N 必然不一致；本轮不登记这一缺陷。率的具体含义仍须按下文限定。
- **交换机 netdev 有限视图有版本化入口依据。** Cumulus 4.3 的 Monitoring Best Practices 在 Layer 1 Protocols and Interfaces 明列 `/sys/class/net/[iface]/statistics/[stat_name]`，说明内核汇总硬件统计。由此可以建立 Cumulus 4.3 入口与通用 ABI 定义的引用链，不能因读取的是 v6.16 ABI 就认定 Cumulus 4.3 没有入口，也不能把这写成该交换机实际运行 v6.16。

## C10 — P2，OPEN：采集映射与测量口径仍需修订

### 1. out_of_buffer 两条入口被合写成 sysfs

位置：[正文](../../knowledge/03-communication/rdma-baseline-and-congestion-triage.md) L111，H1 注记 L33；登记 `src.kernel.mlx5-ib-counters-v6.16` 的 vport 摘要。

正文将“mlx5 IB vport `out_of_buffer` 与 mlx5e qcounter `rx_out_of_buffer`”一并附“经 sysfs hw_counters”。实际 IB basic 表提供 `out_of_buffer`，vport 表展开为 **`vport_out_of_buffer`**（`counters.c` L22–24、26–32、46–52）；mlx5e 的 `rx_out_of_buffer` 则由 `en_stats.c` L552–606 作为 **ethtool 统计**导出，L613–634 经 FW query 获取并汇总 q-counter。`en_ethtool.c` L318–340、2628–2630 接入 `get_ethtool_stats`。FW query 是内部读取，不等于两个字段都出现在 IB sysfs 目录。

这会使读者按错误目录或无前缀名字采集字段，也会混淆 IB counter-set/vport 与 mlx5e qcounter 的作用域。需按字段拆成 IB sysfs 与 mlx5e `ethtool -S` 两条路径，准确列出 vport 名字与条件；保留流控页 dropless 超时丢包的局部说明，但不要把两个不同作用域的值声明为一一相同。累计位宽/FW 细则未核定可继续 unknown。

### 2. per-QP opcounters 被映射到另一种 verbs counter API

位置：正文 L104，H1 注记 L33，研究记录第七轮节及登记 `src.kernel.mlx5-ib-counters-v6.16`。

`counters.c` L131–140 的完整字段名是 `cc_rx_ce_pkts`、`cc_rx_cnp_pkts`、`cc_tx_cnp_pkts`。per-QP 路径使用 **`rdma_counter` 的 QP 绑定/统计更新**：L612–642 的 `counter_bind_qp` 调用 `mlx5r_fs_bind_op_fc`；L578–592 的 `counter_update_stats` 在 `bind_opcnt` 分支调用 L448–480 的 per-QP 统计读取。`fs.c` L1066–1104、1121–1130、1400–1435 核对 CE/CNP 条件、收/发 QP 匹配及 optional counter 条件。底层确实使用 flow counters，但这不等于用户态 `ibv_create_counters` / `ibv_read_counters` 对象自动提供这些命名字段。

相邻的 `create/read_counters` 属于 **`ib_counters` flow 对象**（L150–208、994–1026），提供配置的 packets/bytes description/index，不能凭函数相邻把它写成上述 per-QP opcounters 的采集入口。“flow counters 需 attach”也未交代实际 QP 绑定/optional 启用范围。需纠正 API、完整字段名、方向与绑定条件；若暂不交付用户态管理/读取入口，可将 **per-QP 分支**降为待核定，保留已取得的 port/device cong 分支。无需为关闭 C10 强行实现或现场执行 per-QP 采集。

### 3. ECN 率须限定为本机标记口径

位置：正文 L103、151，研究记录第七轮“率可计算”及对应登记。

`counters.rst` L1280–1282 定义 marked 为**设备因 per-host 拥塞而标记的包**；`rx_prio[p]_packets` 是物理端口该 L2 priority 收包总数（L1224–1225）。因此可保留同设备/端口/priority、同窗口的 **`Δmarked / Δpackets` 本机标记占比**，注明字段可用及 `Δpackets>0`，缺字段、零分母、回退/重置或窗口不齐时 unknown。不能把“字段齐备”单独当作有效率，也不能把这一比值默认为网络已标 CE 的 RoCE 收包比例。

IB 的 `np_ecn_marked_roce_packets` 与可选 `cc_rx_ce_pkts` 是另一路观察点，应与本机标记量分开；若将来用它们计算接收 CE 比例，需要该 RoCE 统计范围匹配的分母，不拿物理端口全部包数直接代替。当前停止表只写“ECN 标记率”而没有上述观察点限定，容易把 NIC 本机缓冲拥塞归到不同的网络作用域。修订正文与停止表的指标名称/条件即可，不新增普适 ECN 阈值要求。

### 4. 交换机引用链与现行状态注记须同步

正文 L105/H1 已选 Cumulus 4.3 netdev 视图，可保留这一有限范围；但现行引证只有 RoCE 配置页与通用 ABI，需在统计行附近补上 **Cumulus 4.3 的实际统计入口页**，区分交换机的内核/硬件汇总与 mlx5 NIC 的 pause-storm 字段。ABI L44–60 等亦要求按驱动确定具体 errors/dropped 含义，不能据字段名将丢包项互加或推成完整 ASIC 丢包量。

Cumulus 4.3 的 ethtool 页 View and Clear Interface Counters 说明 Mellanox 物理统计向内核通常每 2 秒更新，高负载可能更慢。采样设计须记录/考虑这一更新边界，避免把内核快照未更新认作同窗零新增；无需现场验证全部 ASIC 内部字段。该限制是本轮所选交换机 netdev 视图的测量范围，不是扩大硬件覆盖要求。

正文 **verification L37 仍写“RoCE 交换机侧逐统计字段、传输重试计数字段待补”**，与现行测量表、L164 和第七轮“已交付字段”不一致。需改成现存的语义/入口/选型等具体待补项，并同步 H1、研究记录、修订映射和登记中受以上修正影响的表述。历史带日期节无需改写成现行状态。

## 关闭条件与状态

C10 下一轮仅需定向复验：两条 out_of_buffer 的准确字段/入口/作用域；opcounters 与 `ib_counters` API 的区分（per-QP 可以明确待核定）；本机 marked 占比的指标名、delta 和有效分母分支；Cumulus 4.3 统计引用与刷新范围；现行注记同步。**三类实际字段已取得，不再要求重新证明“字段是否存在”。** 已接受的 UFM、ECN 双入口、PFC 配置限定、dropless 开关归类、host 校验门禁及 EP 映射不重开；FW 未公开细则、具体型号/固件、累计位宽和 ASIC 内部超出 netdev 的部分可继续 unknown，保留相应无法判断分支。仍不要求实机结果。

| 状态 | ID |
|---|---|
| CLOSED（15） | C01、C02、C03、C04、C05、C06、C07、C08、C09、C11、C12、C13、C14、C15、C16 |
| OPEN（1，P2） | C10 |

T03-01/T03-02/T03-04 的有限文档通过范围保持，T03-03 与整批仍暂不通过。本轮只更新审阅报告、历史最新进展、来源审计及既有来源 notes；作者正文/研究记录/修订映射、索引、任务/主题覆盖、Batch 17 与独立审计文件保持输入。来源仍 378 项，不新增 ID；知识保持 draft，基线 not_verified，无实机验证。

交付核对：`make check` / `make build` 均 PASS（86 篇内容、378 项来源），catalog JSON/Markdown 已重建。九份审阅/审计文件的 172 个本地文件链接、最新指针和 16 项完整互斥状态集合核对通过；15 CLOSED / 1 OPEN。70 个受保护文件 SHA 保持输入；378 个来源 ID 与非 notes 字段完全不变，仅五个既有 notes 追加本轮核对定位与限定。结构检查不替代技术正确性、远端语义或硬件验证。
