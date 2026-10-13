# 第十八批第八次定向复核

复核日期：2026-10-10（Asia/Shanghai；输入快照时间 2026-10-10 04:47:49 UTC）。作者第八轮修订节标注 2026-10-14，保留为作者标签；以以下文件 SHA-256 识别实际输入，不由标签推导执行日期。

**结论：C10 转 CLOSED；累计 16 CLOSED / 0 OPEN，Batch 18 在原定有限文档范围内通过。** [第七次复核](batch-18-codex-seventh-recheck.md)的四项修正与现行注记同步已完成，无新增阻断项或发现 ID。此前 15 项 CLOSED 保持；T03-03 的有限文档流程通过，T03-01/T03-02/T03-04 的已接受范围保留。通过不建立具体型号/固件配套或实机验证。

约定模型 / effort 为 `gpt-6.1-sol / xhigh`，本会话 Codex 主助手执行，未派发子代理；实际运行标识没有可独立核验的元数据，沿用[初审说明](batch-18-codex-review.md)。依据[路线图](../full-coverage-roadmap.md)、[T03-03 验收](../../plans/full-coverage-backlog.yaml)、[写作指南](../authoring-guide.md#7-批次审阅约定)、[归属边界](../../content-outline.md)及 [AGENTS](../../AGENTS.md)，按第七次关闭条件复核修订影响，不重开其他已关闭项，不扩大为全部硬件覆盖或实机结果要求。

## 输入身份与变化范围

| 输入 | SHA-256 |
|---|---|
| [RDMA 基线正文](../../knowledge/03-communication/rdma-baseline-and-congestion-triage.md) | `e52e3086b1c6062d90615b1dd3677e1c69e6433fdc420232e9a5850be3b1875a` |
| [基线研究记录](batch-18-rdma-baseline-sources.md) | `5539814d13a1b3282df789a090ed61d6d1737470be1a0ee4d0cb28492d141a6c` |
| [修订映射](batch-18-review-fixes.md) | `8176b17986a4f0d1c9ee7dd451fd52d6fde79ded98613bceb9bb8ed96d9dc822` |
| [来源审计](batch-18-source-audit.md) | `9dc9626725d3804e2b0784a2bbd7a6073d2427ae2b842d514ef615275f606bfb` |
| [来源登记](../../sources/registry.yaml) | `654e5f497ef49c8a4b9b123f25c02a8bdf03242c4993d9e27b4a114526abfa69`（381 项） |

受保护输入中只有基线正文、基线研究记录和修订映射相对第七次输入变化；另外三篇 Batch 18 正文、对应研究记录、章索引、Batch 17、独立审计和路线图/约定文件保持前轮身份。作者新增 `src.kernel.mlx5-counters-doc-v6.16` 与 Cumulus 4.3 两个统计页登记，来源 378→381。本轮读取新增行、测量表、H1/verification、停止表、研究修订节、修订映射及受影响登记。

## 一次源复验

用默认 TLS 校验的 curl 只读重抓以下五份精确来源，均 HTTP 200，字节数和 SHA 与第七次相同。网页工具也取得 Cumulus 两页；GitHub blob 未取得时采用 raw。临时原文不入库、不编译或执行，不宣称所有远端 URL 本轮重新取得。

| 本轮重抓来源 | 字节数 | SHA-256 |
|---|---:|---|
| [mlx5 en_stats.c v6.16](https://github.com/torvalds/linux/blob/v6.16/drivers/net/ethernet/mellanox/mlx5/core/en_stats.c) | 95081 | `9f5eea7c1b082983ec36c6a09e5ea9599575c83fdcec039ef06cee3bfd9a5a06` |
| [mlx5 IB counters.c v6.16](https://github.com/torvalds/linux/blob/v6.16/drivers/infiniband/hw/mlx5/counters.c) | 34987 | `292177935746d101ab81811cccbc5d49a833a30eb90c793353f1340d79686246` |
| [mlx5 counters.rst v6.16](https://github.com/torvalds/linux/blob/v6.16/Documentation/networking/device_drivers/ethernet/mellanox/mlx5/counters.rst) | 48415 | `838baabf8e0d91539db795bbeebdaeca5e2d79067648bd7c246577a999a3d482` |
| [Cumulus 4.3 Monitoring Best Practices](https://docs.nvidia.com/networking-ethernet-software/cumulus-linux-43/Monitoring-and-Troubleshooting/Monitoring-Best-Practices/) | 71791 | `d1ce189bcb654d4789db2308849e61e3f5d9322b4ebed38dda3ba4dcaa7eb472` |
| [Cumulus 4.3 ethtool 监控页](https://docs.nvidia.com/networking-ethernet-software/cumulus-linux-43/Monitoring-and-Troubleshooting/Troubleshooting-Network-Interfaces/Monitoring-Interfaces-and-Transceivers-Using-ethtool/) | 53576 | `4ce2af2e00cd4bcab173ad814929d9cac0d21f261ffeea2d23e3753caac11332` |

辅助接入与作用域重读第七次固定快照：[en_ethtool.c](https://github.com/torvalds/linux/blob/v6.16/drivers/net/ethernet/mellanox/mlx5/core/en_ethtool.c)、[IB fs.c](https://github.com/torvalds/linux/blob/v6.16/drivers/infiniband/hw/mlx5/fs.c)、[InfiniBand sysfs ABI](https://github.com/torvalds/linux/blob/v6.16/Documentation/ABI/stable/sysfs-class-infiniband)与 [net-statistics ABI](https://github.com/torvalds/linux/blob/v6.16/Documentation/ABI/testing/sysfs-class-net-statistics)。四份 SHA 核对未变，身份见[第七次证据表](batch-18-codex-seventh-recheck.md#一次源复验)；不将重读快照写成重新抓取。

## C10 — CLOSED：关闭条件逐项复验

| 第七次要求 | 当前正文位置及修订 | 一次源定位与判定 |
|---|---|---|
| out_of_buffer 两条字段/入口/作用域 | L115 拆为 IB `vport_out_of_buffer` / sysfs 与 mlx5e `rx_out_of_buffer` / ethtool；明确作用域不同，不声明值相同 | `counters.c` L22–24、46–52 确认 vport 前缀；`en_stats.c` L552–606、613–634 确认 qcounter 字段导出与 FW query；`en_ethtool.c` L318–340 接入 ethtool。已接受。 |
| opcounters 与 ib_counters API 区分 | L107 保留 port/device cong；L108 列完整 cc_* 名字、rdma_counter QP 绑定与 bind_opcnt 条件，明确 ibv_create/read_counters 为另一 flow 对象；用户态入口未交付，per-QP 判读待核定 | `counters.c` L448–480、578–642、1196–1217 与 `fs.c` L1066–1130、1400–1435 支持 QP 绑定/更新分支；`counters.c` L150–208、994–1026 支持 ib_counters 的 packets/bytes description。按前轮允许的有限分支关闭，不要求补实机或强行交付 per-QP 用户态入口。 |
| 本机 marked 占比与有效分母 | L106 定义设备因 per-host 拥塞执行的标记，使用同设备/端口/priority/窗口的 Δmarked/Δpackets，要求 Δpackets>0；缺字段、零分母、回退/重置及窗口不齐 unknown；L155 同步指标名与观察点 | `counters.rst` L1206–1225、1271–1282 支持 L2 priority、物理端口包数与本机标记语义。未把该比值当作网络已标 CE 的 RoCE 收包比例；NP 为另一个观察点，须匹配其分母。已接受。 |
| Cumulus 4.3 统计引用、汇总与刷新范围 | L109 就近链接两页；区分推荐轮询 10 秒与 Mellanox 物理统计向内核 2 秒/虚接口 10 秒的更新边界，高负载可更长；未更新不当作同窗零新增；ABI errors/dropped 按驱动确定且不互加 | Best Practices 的 Layer 1 Protocols and Interfaces 明列统计入口/汇总；ethtool 页的查询示例、View and Clear Interface Counters 支持 HwIf* 字段、刷新范围及 cl-netstat -c 不清内核/硬件。netdev 有限视图已建立版本引用链，不证明交换机实际运行 v6.16。已接受。 |

H1（L36）与 verification（L40）已同步上述分支和剩余 unknown，旧“传输重试/交换机字段待补”已移除；L168、研究记录第八轮节、修订映射及受影响来源 notes 与现行范围相符。带日期的旧修订节保留历史，不用它们否定现行交付。第七次已接受的三类字段存在性、cap 门控及不同重试/异常事件不互作总重传包数的范围保持。

附带修订已接受：L116 将 `pause_duration` 单位改为微秒，`counters.rst` L1243–1249、1265–1268 明确给出单位及 PFC 使能条件；它不建立未选型号的全字段支持，也不改变原同窗增量比较规则。

**非阻断定位提示：** 正文 L108 的 `basic_op_cnts` 括注只精确定位 `cc_rx_ce_pkts`（`counters.c` L131–133）；另外两项分别在 `rdmarx_cnp_op_cnts` 与 `rdmatx_cnp_op_cnts`（L135–141）。后续文字维护宜拆分该括注或删去表名简称。本轮按三个实际表核对字段，不把此括注解释成三项均无独立 cap 条件；正文已明确 per-QP 判读待核定，该定位简写不影响本次原定关闭条件，不新增发现 ID。

## 通过范围与保留条件

| 状态 | ID |
|---|---|
| CLOSED（16） | C01、C02、C03、C04、C05、C06、C07、C08、C09、C10、C11、C12、C13、C14、C15、C16 |
| OPEN（0） | 无 |

T03-01/T03-02/T03-04 的既有有限文档通过范围与本轮 T03-03 的有限诊断设计共同构成 Batch 18 的审阅通过，不升级为全平台通用或现场复现。以下保留条件不会因 CLOSED 消失：

- NIC 具体型号/固件、FW 未公开事件细则、累计位宽、ASIC 内部超出 netdev 的部分仍 unknown；不能把能力门控源代码当作任意 ConnectX/Spectrum 型号的配套保证。
- per-QP 用户态管理/读取入口未交付，per-QP 判读仍待核定；可用 port/device 分支与它分开。未知/缺字段/不可比窗口维持无法判断，不强行代入停止或恢复门槛。
- rdma-core 完整九页差分仍未完成；此前接受的固定 v65.0 语义范围保留。host 覆盖门禁、EP 有限字节公式、未核定 device/fused/padding/具体路由条件不扩大。
- 所选目标形态、两节点/多节点、背景争用等方案没有实机结果；所有正文仍 draft，基线仍 not_verified，不能写 reproduced。

本轮只更新审阅报告、历史最新指针、来源审计和既有来源 notes；作者正文/研究记录/修订映射、索引、路线图任务/主题覆盖、Batch 17 与独立审计文件保持输入，不代替所有者修改完成状态。来源仍 381 项，复核不新增来源 ID，无实机验证。

交付核对：`make check` / `make build` 均 PASS（86 篇内容、381 项来源），catalog JSON/Markdown 已重建。十份审阅/审计文件的 187 个本地文件链接与最新指针核对通过，16 项状态集合为 16 CLOSED / 0 OPEN。70 个受保护文件 SHA 保持本轮输入；381 个来源 ID 与非 notes 字段不变，仅五个既有 notes 追加本轮定位和有限关闭范围。结构检查不替代技术正确性、远端语义或硬件验证。
