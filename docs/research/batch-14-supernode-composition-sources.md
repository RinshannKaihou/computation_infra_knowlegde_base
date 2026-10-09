# 第十四批来源记录：板卡到超节点的组成与拓扑约束（T01-05）

研究日期：2026-10-09。研究者：探索子代理（非 gpt-6.1-sol）。目标正文：`knowledge/01-hardware/resource-topology.md`（reference，draft，验收标准见 plans/full-coverage-backlog.yaml T01-05）。范围：NVIDIA GB200 NVL72 超节点组成/互联/可维护单元复核（已登记来源直核）、华为 Atlas 900 A3 SuperPoD 与灵衢 LingQu 630 V1 官方资料新取证、AMD OEM 8 卡节点（Supermicro AS-8125GS-TNMR2 + AMD MI300X 平台数据表）新取证、OCP OAI/OAM/UBB 分层规范定位。未执行任何设备查询或实测；除本文件外未改动仓库其他文件。所有网页证据均为 2026-10-09 观察。

## 主张—证据表（NVIDIA GB200 NVL72 超节点：组成）

| 主张 | 来源与定位 | 版本/日期 | 证据性质 | 反例/未知 |
|---|---|---|---|---|
| 一个 NVL72 机柜 = 72-GPU NVL 域，含 18× 1RU compute tray（每 tray 2 Grace CPU + 4 Blackwell GPU）、9× 1RU NVLink switch tray、2× 管理用 TOR 交换机、向所有 tray 供电的 power shelf；整机柜级系统由 compute tray（含一到两块计算板）、NVLink switch tray、NVLink 无源铜缆背板（cable cartridge）、power shelf、bus bar、液冷 manifold 组成 | [DGX GB Rack Scale Systems User Guide](https://docs.nvidia.com/dgx/dgxgb200-user-guide/hardware.html) §1 Hardware 引言、§1.1 Rack Configuration（[PDF](https://docs.nvidia.com/dgx/dgxgb200-user-guide/dgxgb200-user-guide.pdf)，pdftotext 核对一致）；已登记 src.nvidia.dgx-gb200-user-guide-2026-09-17 | PDF/网页均标 2026-09-17（网页页脚 "Last updated on Sep 17, 2026"）；index 页页脚另显示 "Last updated on Mar 03, 2026"，以章节页与 PDF 为准 | 厂商手册 | 文档同时覆盖 GB200/GB300 两型，引用时须分机型；未列整机柜重量 |
| compute tray = 承载计算板与外围扣板、运行 OS 镜像的 1RU 机箱；CPU/GPU 由沿机柜 manifold 供液的 cold plate 液冷，网络/存储等其余部件风冷；tray 间经背部连接器通过 NVSwitch tray 以 NVLink 互连；OOB 管理由 BMC + HMC 组合提供 | 同上 §1.2 Compute Trays | 同上 | 厂商手册 | 未给单 tray 重量/功耗 |
| compute tray 配置表：Compute node = 2× Grace CPU + 4× Blackwell GPU；GB200 集群网络 4× ConnectX-7 单口 400G OSFP（GB300 为 4× CX-8 800G）；存储/管理网络 2× BlueField-3 DPU 双口 400G；OOB = tray BMC 1× 1GbE RJ45 + BF-3 BMC 2× 1GbE RJ45；数据缓存 4× 3.84TB E1.S NVMe/tray 软 RAID 0；启动盘 1× 1.92TB M.2 NVMe | 同上 §1.2 配置表（Component/Function 两列表） | 同上 | 厂商手册 | E1.S 数量与 HPE/Supermicro 口径冲突，见「缺口与冲突」 |
| NVLink switch tray：1U 内 57.6 Tbps 全双工（第五代 NVLink）；每 tray 2× NVLink NVSwitch（每颗 72 个 NVLink 端口）、NVOS 2.0+、BMC（attestation/recovery）、FM/SM 控制面、CPU ERoT | 同上 §1.3 NVLink Switch Trays | 同上 | 厂商手册 | 未给 switch tray 功耗/重量 |
| 供电：bus bar 配电；power shelf 将 AC 转 50–51V DC；机柜功耗约 120 kW；8 个 power shelf N+N，每 shelf 6× 5.5 kW 风冷 PSU、33 kW 输入 | 同上 §1.4 Power Shelves（与第十三批记录一致） | 同上 | 厂商手册 | 与 OEM 口径差异已在第十三批记录 |
| NVLink 拓扑：NVLink 5.0 每 GPU 双向 1.8 TB/s；tray 背部连接器接入 cable cartridge，沿机柜上下连通全部 compute tray 与 NVLink switch tray；fabric 由 Fabric Manager（NVLSM）管理；NVSwitch 支持 SHARP 网内计算 | 同上 §2.1 NVLink Networking | 同上 | 厂商手册 | 未给端口级连线表 |
| GB200 NVL72 产品页口径：36 Grace CPU + 72 Blackwell GPU，单机柜 72-GPU NVLink 域，NVLink Switch System 提供 130 TB/s GPU 通信；GB200 superchip = 1 Grace + 2 Blackwell 经 NVLink-C2C 互联；整柜 GPU 显存 13.4 TB HBM3E/576 TB/s、CPU 内存 17 TB LPDDR5X/14 TB/s、CPU 共 2,592 核 | [NVIDIA GB200 NVL72 产品页](https://www.nvidia.com/en-us/data-center/gb200-nvl72/) Specifications 表 | 可变网页，2026-10-09 观察 | 厂商产品页 | 产品页无功率/重量数字；性能倍数为厂商宣称口径（页面自带测算脚注） |
| HPE GB200 NVL72：18× compute tray（每 tray 2× Grace + 4× Blackwell；每 tray 含 2 块 GB200 板、每板 1 颗 Grace ARM 处理器）、9× NVLink switch tray、6（最大 8）× 33 kW power shelf、50 V DC busbar、2× SN2201 TOR、44U 机柜液冷 manifold；Grace CPU 72 核 Neoverse V2、焊接 512 GB LPDDR5X（480 GB 可用）、ECC 默认开启、内存不可配置；BMC 基于 OpenBMC + ASPEED 2600 | [HPE QuickSpecs a50009224enw](https://www.hpe.com/us/en/collaterals/collateral.a50009224enw.html) Standard Features › Platform Information / Processors / Memory / On System Management Chipset；已登记 src.hpe.gb200-nvl72-quickspecs-a50009224enw-v6 | V6，2026-09-08（Summary of Changes 表） | OEM 规格书 | 「NVL72 contains 18 compute trays. Each compute tray contains 2 GB200 boards. Each board has 1 Grace ARM processor.」为 tray→board→CPU 层级关系的直接原文 |
| HPE：每 compute tray 存储 = 8× 3.84 TB E1.S（前置，SED，Opal/TCP，hot-pluggable and hot-swappable）+ 1× 1.98 TB M.2（内置）；FIO 面板：USB 3.0/2.0、mini DP、1 GbE 管理口、3× 状态 LED | 同上 Internal Storage 表 / Platform Information › FIO | 同上 | OEM 规格书 | 与 NVIDIA UG「4× E1.S/tray」冲突，见「缺口与冲突」 |
| Supermicro GB200 NVL72：72× B200 + 36× 72 核 Grace；18× 1U compute tray；9× NVLink switch tray（每 compute tray 4 个 NVLink 端口接 72 GPU，1.8 TB/s GPU-to-GPU）；compute tray 内含 2 颗 GB200 superchip，GPU 显存最高 372 GB HBM3e/superchip（744 GB/tray），CPU 内存最高 480 GB LPDDR5X/superchip（960 GB/tray），后部 4× NVLink 端口，前部 4× 单口 CX-7、最多 2× BF-3，最多 8× E1.S PCIe 5.0；tray 由机柜 4+4 power shelf 共享供电 | [Supermicro SuperCluster GB200 NVL72 datasheet](https://www.supermicro.com/datasheet/datasheet_SuperCluster_GB200_NVL72.pdf)「72-GPU Scalable Unit」表 + Compute Tray 列（pdftotext -layout 恢复文本层）；已登记 src.supermicro.supercluster-gb200-nvl72-datasheet-2025 | ©2025，2025 年 2 月版 | OEM 数据表 | 「Up to」为可选上限口径；与 NVIDIA UG 4× E1.S 口径冲突见「缺口与冲突」 |

## 主张—证据表（NVIDIA GB200 NVL72 超节点：可维护性）

| 主张 | 来源与定位 | 版本/日期 | 证据性质 | 反例/未知 |
|---|---|---|---|---|
| DGX GB 系统维护操作对象包括 compute tray、switch tray、trunk links、cable cartridge 更换； Mission Control 宣称可隔离故障组件并隔离受影响基础设施 | [DGX GB UG](https://docs.nvidia.com/dgx/dgxgb200-user-guide/) §7.1 Cold Reboot Sequence 前置条件列表、§4.1 Mission Control Software | PDF 2026-09-17 | 厂商手册 | 用户指南无 FRU 清单与更换流程章节；可更换粒度以该枚举为准，不能扩写为「现场可换 GPU 载板」 |
| 电源/风扇类安全警告：PSU 为 hot-plug、内部无用户可维护部件；更换 hot-plug PSU 需先拔该 PSU 电源线；非 hot-plug 部件拆装前须断电 | 同上 §5 Safety（Power and Electrical Warnings、Cooling and Airflow） | 同上 | 厂商手册 | 安全警告级证据，不等同维护流程 |
| HPE 服务口径：硬件 3 年保修；CSR（Customer Self Repair）分 Mandatory（易更换，用户拒绝自换则收取差旅人工费）与 Optional 两类 | [HPE QuickSpecs a50009224enw](https://www.hpe.com/us/en/collaterals/collateral.a50009224enw.html) Product Warranty 节 Notes | V6，2026-09-08 | OEM 规格书 | 未列出 NVL72 哪些部件属 Mandatory/Optional CSR，具体部件清单未取得 |

## 主张—证据表（NVIDIA DGX H100/H200：服务器节点层样板）

| 主张 | 来源与定位 | 版本/日期 | 证据性质 | 反例/未知 |
|---|---|---|---|---|
| DGX H100/H200 = 8U 节点：8× H100（640 GB）或 8× H200（1,128 GB）、2× Intel Xeon 8480C（各 56 核）、4× 第四代 NVSwitch（900 GB/s GPU-to-GPU）、2× 1.92 TB M.2 RAID1（OS）+ 8× 3.84 TB U.2 SED RAID0（缓存）、8× CX-7 单口 IB（4 个 OSFP 口）+ 2× CX-7 双口以太、2 TB/32 DIMM、BMC 1 GbE、6× 3.3 kW PSU | [DGX H100/H200 User Guide](https://docs.nvidia.com/dgx/dgxh100-user-guide/introduction-to-dgxh100.html) Table 1 Component Description；已登记 src.nvidia.dgx-h100-h200-user-guide-2026-01-26 | last updated 2026-01-26（页脚复核一致） | 厂商手册 | x86 CPU 节点与 Grace 节点并存，不可跨机型类推 |
| 节点内分 motherboard tray 与 GPU tray 两个可抽拉单元（各有部件图）；网络模块：4 张 CX-7 集成为单模块、2 个网络模块装于 interposer 板、DensiLink 电缆至后部 OSFP | 同上 Motherboard Tray Components / GPU Tray Components / Network Modules（Table 6） | 同上 | 厂商手册 | 无单一部件更换流程；维护以整 tray/整机为界 |
| PSU 冗余与降级行为：6 PSU 按 4+2 冗余；3 PSU 失电系统降性能继续运行；仅 ≥3 PSU 才允许开机；<3 PSU 时仅 BMC 可用 | 同上 Support for PSU Redundancy and Continuous Operation | 同上 | 厂商手册 | 为供电共享根故障隔离假设的直接口径 |

## 主张—证据表（Ascend 超节点：Atlas 900 A3 SuperPoD 与灵衢 LingQu 630 V1）

| 主张 | 来源与定位 | 版本/日期 | 证据性质 | 反例/未知 |
|---|---|---|---|---|
| Atlas 900 A3 SuperPoD 形态 = 12× 计算柜（47U）+ 4× 总线设备柜（47U）；最大 384× 昇腾910（产品页原文；彩页写昇腾910C）NPU、192× 鲲鹏920 CPU、1536× DDR5（5200 MT/s，单条 64/96 GB）、384× 128 GB 片上内存（带宽最大 3.2 TB/s）；D2D 双向 784 GB/s；本地存储最大 480× 2.5 英寸盘；供电三相 380V AC + 三相 380V AC；散热 = 液冷（计算柜）+ 风冷（总线设备柜）；48 TB 片上内存统一编址、总线带宽 1:1 无收敛、200 ns 单跳时延；支持 16/32/64/128/256/384 卡逻辑超节点 | [华为 Atlas 900 A3 SuperPoD 产品页](https://e.huawei.com/cn/products/computing/ascend/atlas-900-a3-superpod)「技术规格」区与「超节点架构」特性区（服务端渲染 HTML 直接核对）；[官方硬件彩页 PDF（26H1 预训练版）](https://e-file.huawei.com/marketingcloud/pep/asset/20000001/Material/5d4c82c0af394286b120ce799b786bc5/M3T1A669N1253094776671068388/Atlas%20900%20A3%20SuperPoD%E7%A1%AC%E4%BB%B6%E5%BD%A9%E9%A1%B5-%E5%A4%A7%E6%A8%A1%E5%9E%8B%E9%A2%84%E8%AE%AD%E7%BB%83%E8%A7%A3%E5%86%B3%E6%96%B9%E6%A1%8825_0-%E5%BD%A9%E9%A1%B5_26H1_.pdf) | 产品页为可变网页，2026-10-09 观察；彩页文件名标 26H1 | 厂商产品页/彩页 | 产品页写「昇腾910」、彩页写「昇腾910C」，型号后缀口径不一，正文引用须保留原样并注明；AI 算力口径产品页为 307.2/288.7 PFLOPS@FP16，彩页预训练版写 288.7、另一彩页版本写 240.3，为不同 SKU/档位口径 |
| 计算柜单柜：47U，4× 8U 计算节点；2× 3U 电源框共 66 kW；最大输入功耗 54 kW；预留 1× 1U GE 交换机位；RM211 管理模块（2 GE + 1 Mgmt + 1 RS485）；Manifold 供水 5–40℃、流量 45–60 LPM、最大压力 350 kPa；满配含水约 1285 kg；单柜 AI 算力 20.032/24.064/25.600 PFLOPS@FP16；单柜片上内存最大 4096 GB（带宽 2×1600 GB/s） | [Atlas 900 A3 SuperPoD 超节点用户指南 13](https://support.huawei.com/enterprise/zh/doc/EDOC1100401572)（EDOC1100401572）计算柜章节 表9-2 特性规格 | 文档版本 13，2026-06-25（修改记录表核对） | 厂商用户指南 | 「极限压测功耗不代表实际业务功耗」为原文脚注；12 柜 × 4 节点 × 8 NPU = 384 与总量自洽 |
| 单计算柜物理组成：平板前门（可选）、平板后门（可选）、4 个计算节点、2 个电源框（主+扩展）、1 个 GE 交换机（可选）、液冷机柜、RM211 管理模块、电源转接板；总线设备柜：14× 灵衢总线设备 LingQu 630 V1、1 个电源框（电源机箱+电源模块）、1 个 GE 交换机（可选）、RM211；「当组网不涉及总线设备柜时，计算柜就是 Atlas 900 A3 SuperPoD 超节点」 | 同上用户指南 产品概述章节（[页面](https://support.huawei.com/enterprise/zh/doc/EDOC1100401572/bd23f260)，图2-1/2-2/2-3 及部件表） | 同上 | 厂商用户指南 | 计算柜可独立成超节点这一口径对「超节点 vs 机柜」层级划分很关键 |
| 计算节点物理结构 = CPU 抽屉（K）+ NPU 抽屉（A1）+ NPU 抽屉（A2）+ 机框 + 3× 灵衢总线板（PIC1–PIC6）+ 1× 灵衢总线和以太板（PIC7/PIC8）；CPU 抽屉含 2× CPU 基础板、内存、硬盘背板、Riser 模组 1/2、8080 风扇模块、4056 风扇托盘/模块、3× 1420W 液冷电源模块（PSU1/2/3）+ 1× 600W 风冷电源模块、BMC 扩展板、Busbar 接线排、缓启板、超级电容支架；NPU 抽屉含液冷散热器、风扇模块、NPU 模组（TOP/BOTTOM 面）、低速管理板、风扇背板 | 同上用户指南 物理结构章节（[页面](https://support.huawei.com/enterprise/zh/doc/EDOC1100401572/d3e2c244)，图6-2/6-3/6-4 部件表） | 同上 | 厂商用户指南 | 部件级清单为节点→抽屉→模组层级关系的直接原文 |
| 计算节点逻辑结构：2× 天池基础板共 4× 鲲鹏920（每处理器 8× DDR DIMM）；8× NPU 模组，每模组直出 2×200G 以太（参数面）+ 2×7×200G LQC（灵衢总线面）经线缆至灵衢总线板；4× 灵衢总线板（3 总线板 + 1 总线和以太板）：灵衢下行连 NPU/CPU、上行至灵衢总线设备；以太下行连 NPU、上行至柜外 RoCE 标准交换机；最大 8× NVMe（CPU4 直出）+ 2× SATA（经 Riser+RAID 卡）；BMC 扩展板为华为自研芯片外出 1 GE | 同上用户指南 逻辑结构章节（[页面](https://support.huawei.com/enterprise/zh/doc/EDOC1100401572/6e226b8e)，图6-5） | 同上 | 厂商用户指南 | 每节点 8 NPU + 4 CPU 与柜/超节点总量自洽（4×8×12=384、4×4×12=192） |
| 灵衢组网：LQC 协议（华为缓存一致性互联接口协议，视作处理器内部 SoC 总线的外延）承载超节点内部通信，7 个平面组网；L1 层由计算节点内灵衢总线板承载，L2 层由总线设备柜内灵衢总线设备（LingQu 630 V1，即灵衢交换机）组成，L1–L2 间按规模用铜缆或光纤；支持 64/96/192/384 超节点配置；384 超节点光互联 = 一套总线设备柜内 56 台灵衢总线设备 + 多套计算柜内 48 台计算节点光纤全互联（物理架构 384，实际部署数量取决于解决方案可靠性冗余设计） | 同上用户指南 组网拓扑章节（[页面](https://support.huawei.com/enterprise/zh/doc/EDOC1100401572/d975beba)，图3-1） | 同上 | 厂商用户指南 | 56 = 4 柜 × 14 台与产品概述自洽；「实际部署数量取决于可靠性冗余设计」提示物理 384 与可用规模可能不同，正文不得默认满配可用 |
| 超节点级带宽口径：超节点内任意两个 NPU 模组之间高速总线互联带宽理论达到双向 784 GB/s | 同上用户指南 技术规格章节（[页面](https://support.huawei.com/enterprise/zh/doc/EDOC1100401572/de187aa3)）表9-1「带宽」行 | 同上 | 厂商用户指南 | 「理论达到」，非实测；详细参数指向《Atlas 900 A3 SuperPoD 超节点 系统关键参数》（未取得，见缺口） |
| 灵衢 LingQu 630 V1（L2 总线设备）：2U（88.1×442×600 mm）、20 kg、风冷 4× 风扇模块 3+1 备份（风扇热备份）；业务端口 48× QSFP-DD-400G（2×200G，每个 QSFP-DD 分接 2 个交换芯片）；1× 管理网口 + 1× 管理串口；供电 AC 220–240V / HVDC 240V / ±48V DC；整机最大功耗 <1200 W；2× 电源模块 1+1 备份；电源模块与风扇模块支持热插拔 | [灵衢总线设备 LingQu 630 V1 用户指南 03](https://support.huawei.com/enterprise/zh/doc/EDOC1100463086)（EDOC1100463086）特性规格章节（[页面](https://support.huawei.com/enterprise/zh/doc/EDOC1100463086/afae8edb)） | 文档版本 03，2026-01-30 | 厂商用户指南 | 彩页另给「单总线设备交换容量 19.2T、总线设备柜 14 台共 672× 400G 端口、柜最大功耗 17.8 kW」口径 |
| Atlas 900 A3 SuperPoD 可维护性证据：维护与服务指南覆盖巡检、故障处理、应急处理、部件更换；部件更换章节含 CPU 抽屉、NPU 抽屉、NPU 模组、内存、Riser 模组、PCIe 卡、RAID 卡、电源模块（版本 10 修改记录注明「电源模块支持热插拔」）、光模块、RTC 电池、风扇模块等；漏液运维含 iRM 上报 Manifold 漏液告警、iBMC 上报服务器节点漏液告警、节点下架快接头漏液处理；前言定义渗漏/喷射两类漏液 | [Atlas 900 A3 SuperPoD 超节点维护与服务指南 14](https://support.huawei.com/enterprise/zh/doc/EDOC1100401573)（EDOC1100401573）概述、前言「常见的漏液现象」表1、修改记录 | 文档版本 14，2026-08-18（修改记录表核对） | 厂商维护指南 | 具体更换步骤页未逐页核对，仅确认章节存在与主题范围；是否算「热维护」需按各部件章节原文，不在本轮展开 |
| Atlas 800T A2（节点层，已登记来源复核）：4U 训练服务器；8× 昇腾910 AI 处理器，每路 7 条 HCCS 链路、最大理论带宽 392 GB/s，8 颗经 HCCS 组成 8P Full mesh；单 AI 处理器 64 GB 片上内存（1600 GB/s）、200GE QSFP 直出 RoCE、最大 400 W、PCIe 4.0 x16 连 CPU；4× 鲲鹏920（7265 64 核/5250 48 核）、2 路 Hydra 总线 30 GT/s；最多 32× DDR4 RDIMM（3200 MT/s）；8× 热插拔风扇 N+1；硬盘热插拔；iBMC | [Atlas 800T A2 用户指南 技术规格](https://support.huawei.com/enterprise/zh/doc/EDOC1100317202/f3dba488) 表3-1/表3-2；已登记 src.huawei.atlas-800t-a2-user-guide-26-2026-10-08 | 文档 26（登记口径）；2026-10-09 复核内容一致 | 厂商用户指南 | 该机型为 PCIe/HCCS 代际节点，与 A3 超节点灵衢架构不同代，不可混用数字 |

## 主张—证据表（AMD OEM 节点样板：Supermicro AS-8125GS-TNMR2 + MI300X 平台）

| 主张 | 来源与定位 | 版本/日期 | 证据性质 | 反例/未知 |
|---|---|---|---|---|
| AS-8125GS-TNMR2 = 8U 双路节点：2× AMD EPYC 9005/9004（SP5，TDP 最高 400 W）、24× DDR5 DIMM（9004 最高 6 TB 4800 MT/s；9005 最高 6 TB 6000 MT/s，需主板 rev 2.0+）、8× 板载 MI300X GPU（GPU tray 内 GPU 基板）、4× PCIe switch（用于 GPU 直通的通信路径）、12+4× 热插拔 2.5" NVMe + 2× 热插拔 2.5" SATA + 2× M.2 NVMe、8× PCIe 5.0 x16 LP + 最多 4× FHFL、5 前 + 5 后重载热插拔风扇、6× 3000 W Titanium（96%）3+3 冗余 PSU（最多可装 8 个）、BMC 专用 RJ45 | [A+ Server AS-8125GS-TNMR2 User's Manual MNL-2671](https://www.supermicro.com/manuals/superserver/8U/MNL-2671.pdf) §1.1 System Overview 表、§1.2 Motherboard Tray/GPU Tray Features（pdftotext -layout 核对） | Manual Revision 1.0b，©2025 | OEM 用户手册 | 手册同页声明规格随配置变；「Power supply full redundancy based on configuration and application load」为原文保留条件 |
| 该机 PSU 可不下电更换，但不超过冗余余量；标准配置 3+3 冗余，最多 3 个模块离线维护（不推荐）；PSU 支持 100–120 V / 180–240 V 自适应 | 同上 §3.7 Power Supply | 同上 | OEM 用户手册 | 「up to three modules can be offline for service, although that is not recommended」照录 |
| NVMe 支持 surprise hot-swap，推荐 orderly hot-swap（可远程弹出更换） | 同上 §3.x Hot-Swap for NVMe Drives | 同上 | OEM 用户手册 | 无厂商实测故障率数据 |
| 官方数据表（网页版）要点：8U、8× MI300X、24 DIMM 最高 6 TB、8× PCIe 5.0 x16 LP + 最多 4× FHFL、2× 热插拔 SATA + 1× M.2 启动 + 最多 16× 热插拔 NVMe（12 默认 + 4 可选）、10× 重载风扇、6× 3000 W Titanium 冗余 PSU、「8 NIC for GPU direct RDMA (1:1 GPU Ratio)」 | [Supermicro AS-8125GS-TNMR2 datasheet 页](https://www.supermicro.com/en/products/system/datasheet/as-8125gs-tnmr2) Key Features | 网页 ©2024，2026-10-09 观察 | OEM 数据表 | 网页表格主体以图片渲染，仅 Key Features 文本层可核对；详细行项目以用户手册为准 |
| MI300X 平台（板卡→底板层）：UBB 2.0 通用底板承载 8× OAM 形态 MI300X；每 OAM 192 GB HBM3（合计 1.5 TB）；每 GPU 7× 128 GB/s Infinity Fabric 链路全互连（8 卡环聚合 896 GB/s）；每 OAM 1× PCIe Gen5 x16 上行至主机；单 GPU 最大 TBP 750 W；RAS 含全芯片 ECC、page retirement/avoidance | [AMD Instinct MI300X Platform Data Sheet](https://www.amd.com/content/dam/amd/en/documents/instinct-tech-docs/data-sheets/amd-instinct-mi300x-platform-data-sheet.pdf) Specifications 表与「AMD Instinct MI300X Platform」段 | ©2023，PID #232405395-D | 芯片厂平台数据表 | 「industry-standard-based universal baseboard (UBB 2.0)」「eight OCP Accelerator Modules (OAMs)」为板卡/底板层级术语的直接原文；AMD 无同构超节点公开样板，按任务要求不向上类推 |

## 主张—证据表（四层次通用关系：开放规范锚点）

| 主张 | 来源与定位 | 版本/日期 | 证据性质 | 反例/未知 |
|---|---|---|---|---|
| OCP OAI（Open Accelerator Infrastructure）子项目明确定义分层对象：OAI-OAM（加速器模块）、OAI-UBB（通用底板）、OAI-HIB（主机接口板）、OAI-PDB（配电）、OAI-EXP（UBB 之外扩展）、OAI-SCM（安全控制管理）、OAI-Tray、OAI Chassis（含风冷/液冷）；当前已发布 OAI-OAM r2.0 v1.0、OAI-UBB r2.0 v1.0、OAI-EXP r2.0 v1.0（均 2023-09-14 提交，OWF CLA 许可）；历史版 OAM v1.5 / UBB v1.5（2022-02-23）；另有 NVIDIA 贡献的 HGX Form Factor Specification（r1.0/v0.1，2022-05-05） | [OCP Server/OAI wiki](https://www.opencompute.org/wiki/Server/OAI) Welcome/Current Status/Active documents 表 | 2026-10-09 观察 | 开放标准组织页面 | 规范 PDF 本体未逐页核对（本轮只固定版本与层级划分）；OWF CLA 是贡献许可，引用规范文本前需确认再分发条款 |
| 「PCIe 板卡 → 模块/托盘 → 服务器节点 → 超节点/机柜」四层在三家官方资料中均有对应实体：NVIDIA = GPU（SXM/板）→ compute board/tray（1RU，含 2 Grace+4 GPU）→ NVL72 机柜（18 tray + 9 switch tray）→ SuperPOD（8 机柜，DGX GB UG 引言「multi-rack deployments such as a SuperPOD (eight NVL72 racks)」）；Ascend = NPU 模组 → NPU/CPU 抽屉（计算节点）→ 计算柜（4 节点）→ Atlas 900 A3 SuperPoD（12 计算柜 + 4 总线设备柜）；AMD = OAM → UBB 2.0 底板（GPU tray）→ 8U 服务器节点 →（无官方同构超节点，保留 unknown） | 上列各来源综合；SuperPOD 8 机柜口径见 [DGX GB UG](https://docs.nvidia.com/dgx/dgxgb200-user-guide/) 概述段 | 同各来源 | 跨来源归纳（每层均有至少一个官方来源） | 「SuperPOD = 8× NVL72 机柜」为 DGX GB UG 的示例口径（"such as"），不是固定定义；AMD 行不得外推 |

## 候选新来源登记

| 建议 source ID | 标题 | URL | kind | 许可状态 |
|---|---|---|---|---|
| src.nvidia.gb200-nvl72-product-page-2026-10-09 | NVIDIA GB200 NVL72 产品页（2026-10-09 观察） | https://www.nvidia.com/en-us/data-center/gb200-nvl72/ | documentation | unknown（厂商营销页，仅登记链接与摘录要点） |
| src.huawei.atlas-900-a3-superpod-product-2026-10-09 | Atlas 900 A3 SuperPoD 产品页（2026-10-09 观察） | https://e.huawei.com/cn/products/computing/ascend/atlas-900-a3-superpod | documentation | unknown（华为网站法律声明限制复制，仅登记链接并原创归纳） |
| src.huawei.atlas-900-a3-superpod-user-guide-13-2026-06-25 | Atlas 900 A3 SuperPoD 超节点用户指南 13（EDOC1100401572） | https://support.huawei.com/enterprise/zh/doc/EDOC1100401572 | documentation | unknown（同上；引用标注文档版本 13 / 2026-06-25） |
| src.huawei.atlas-900-a3-superpod-maintenance-guide-14-2026-08-18 | Atlas 900 A3 SuperPoD 超节点维护与服务指南 14（EDOC1100401573） | https://support.huawei.com/enterprise/zh/doc/EDOC1100401573 | documentation | unknown（同上；文档版本 14 / 2026-08-18） |
| src.huawei.lingqu-630-v1-user-guide-03-2026-01-30 | 灵衢总线设备 LingQu 630 V1 用户指南 03（EDOC1100463086） | https://support.huawei.com/enterprise/zh/doc/EDOC1100463086 | documentation | unknown（文档版本 03 / 2026-01-30） |
| src.huawei.atlas-900-a3-superpod-brochure-26h1 | Atlas 900 A3 SuperPoD 硬件彩页（26H1，预训练版） | https://e-file.huawei.com/marketingcloud/pep/asset/20000001/Material/5d4c82c0af394286b120ce799b786bc5/M3T1A669N1253094776671068388/Atlas%20900%20A3%20SuperPoD%E7%A1%AC%E4%BB%B6%E5%BD%A9%E9%A1%B5-%E5%A4%A7%E6%A8%A1%E5%9E%8B%E9%A2%84%E8%AE%AD%E7%BB%83%E8%A7%A3%E5%86%B3%E6%96%B9%E6%A1%8825_0-%E5%BD%A9%E9%A1%B5_26H1_.pdf | documentation | unknown（营销材料，标注 26H1 版本） |
| src.supermicro.as-8125gs-tnmr2-manual-mnl-2671-r1.0b | A+ Server AS-8125GS-TNMR2 User's Manual（MNL-2671 Rev 1.0b） | https://www.supermicro.com/manuals/superserver/8U/MNL-2671.pdf | documentation | unknown（©2025 Super Micro，仅登记链接与摘录） |
| src.supermicro.as-8125gs-tnmr2-datasheet-2024 | Supermicro AS-8125GS-TNMR2 Datasheet（网页版，©2024） | https://www.supermicro.com/en/products/system/datasheet/as-8125gs-tnmr2 | documentation | unknown（可变网页，引用带观察日期） |
| src.amd.instinct-mi300x-platform-datasheet-2023 | AMD Instinct MI300X Platform Data Sheet（©2023，PID #232405395-D） | https://www.amd.com/content/dam/amd/en/documents/instinct-tech-docs/data-sheets/amd-instinct-mi300x-platform-data-sheet.pdf | documentation | unknown（©2023 AMD，仅登记链接与摘录） |
| src.ocp.oai-wiki-2026-10-09 | OCP Server/OAI wiki（OAM/UBB/EXP r2.0 v1.0 版本索引） | https://www.opencompute.org/wiki/Server/OAI | documentation | 规范本体 OWF CLA；wiki 页面许可未单独确认，引用前核对 |

仅作记录、本轮未取证不登记：Atlas 900 A3 SuperPoD 超节点技术白皮书 07（e.huawei.com 文档页 c6e81925d3cf4673a44a687d03a0d6d7，页面要求下载且疑似需权限，内容未取得）；《Atlas 900 A3 SuperPoD 超节点 系统关键参数》（用户指南多处引用，未取得）。

## 缺口与冲突

- **E1.S 数量口径冲突**：NVIDIA DGX GB UG §1.2 配置表写「4x 3.84TB E1.S NVMe per compute tray」；HPE QuickSpecs V6 写每 tray 8× 3.84 TB E1.S（SED）；Supermicro 数据表写「Up to 8 E1.S PCIe 5.0 drives」。未以任何一方为准做换算，正文须按 DGX 配置与 OEM 配置分列或保留 unknown。
- **昇腾型号后缀口径不一**：华为产品页写「昇腾910」，官方彩页（26H1）写「昇腾910C」；用户指南 13 正文以「昇腾910 AI 处理器」表述。引用时保留各来源原样，不统一改写。
- **Atlas 900 A3 SuperPoD 算力多档**：产品页「307.2/288.7 PFLOPS@FP16」、彩页预训练版「288.7」、另一彩页「240.3」并存，对应不同档位/版本，按来源分开引用。
- **「物理 384 与实际部署」**：用户指南组网拓扑明确「物理架构 384，实际部署数量取决于解决方案可靠性冗余设计」，正文不得把 384 NPU 写成必然可用规模。
- **CloudMatrix 384**：本轮未取得华为云官方 CloudMatrix 384 组成/互联公开文档（仅见第三方转述），如实标未取得；不引用第三方数字进正文。
- **Atlas 900 A3 SuperPoD 技术白皮书 07**：e.huawei.com 文档页存在但需下载（页面提示无法预览），内容未取得；「系统关键参数」文档同样未取得，用户指南中标注「具体请参见」的细项（如分档带宽指标）保留 unknown。
- **NVIDIA 侧 FRU 颗粒度**：DGX GB UG 无 FRU 清单章节，仅维护操作枚举（compute tray / switch tray / trunk links / cable cartridge）与 PSU hot-plug 安全警告；HPE 仅给 CSR 分类框架未给部件清单。GB200 的「服务可替换部件」证据薄，正文按既有枚举写、注明缺口。
- **AMD 侧无超节点**：按任务约定，AMD 只取 OEM 节点样板（AS-8125GS-TNMR2 + MI300X 平台），不类推同构超节点；MI300X 之外（MI325X/MI355X）本轮未取证。
- **OCP OAI 规范本体**：wiki 已固定 r2.0 v1.0（2023-09-14）版本索引，OAM/UBB 规范 PDF 内容未逐页核对，四层次引用层级划分可用 wiki 页，引规范条文需另取 PDF。
- **可变网页风险**：NVIDIA 产品页、华为产品页、Supermicro datasheet 页均为可变网页，引用必须带观察日期（2026-10-09）；华为 support.huawei.com 文档页带 EDOC 号与文档版本号，可稳定定位。
