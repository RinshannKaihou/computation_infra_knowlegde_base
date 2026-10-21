# 第二十八批 T00-02 来源记录

任务：T00-02（单机、集群与超节点的参考架构及选择；**new** `knowledge/00-overview/reference-architectures.md`，主题 00.4）。取证轮次：主会话作者角色首轮（2026-10-21；前置 T01-05/T03-01/T04-03/T05-02/T05-03 均 done）。本轮**无新增外部来源**：两个超节点样板与集群/存储/调度证据全部复用既有登记，evidence_blocker 依 Batch 14/18 已核来源解除。

## 复用来源与主张定位

| 主张 | 登记 ID | 精确位置 | 支持范围 |
|---|---|---|---|
| NVIDIA 超节点样板：GB200 NVL72＝18 compute tray＋9 NVLink switch tray＋2 TOR＋power shelf，72-GPU NVLink 域；NVLink 5.0 1.8 TB/s、cable cartridge 铜背板、Fabric Manager（NVLSM）管理、SHARP；HPE/Supermicro OEM 口径与 E1.S/算力档位冲突按来源分列 | src.nvidia.dgx-gb200-user-guide-2026-09-17、src.nvidia.gb200-nvl72-product-page-2026-10-09、src.hpe.gb200-nvl72-quickspecs-a50009224enw-v6、src.supermicro.supercluster-gb200-nvl72-datasheet-2025 | resource-topology.md（T01-05 交付）§GB200 样板；UG §1/§2.1 | 组成/互联枚举；可替换粒度只到 tray/背板级（[GB 硬件页 §1.1–1.4](https://docs.nvidia.com/dgx/dgxgb200-user-guide/hardware.html)、[NVLink 拓扑 §2.1](https://docs.nvidia.com/dgx/dgxgb200-user-guide/)） |
| Ascend 超节点样板：Atlas 900 A3 SuperPoD＝12 计算柜＋4 总线设备柜（384 NPU/192 CPU 上限）；灵衢 LQC 7 平面、L1 总线板/L2 LingQu 630、铜/光分界；"计算柜即超节点"边界条款；物理 384 与实际部署冗余声明 | src.huawei.atlas-900-a3-superpod-product-2026-10-09、src.huawei.atlas-900-a3-superpod-user-guide-13-2026-06-25、src.huawei.atlas-900-a3-superpod-maintenance-guide-14-2026-08-18、src.huawei.lingqu-630-v1-user-guide-03-2026-01-30 | [产品概述](https://support.huawei.com/enterprise/zh/doc/EDOC1100401572/bd23f260)/[组网拓扑](https://support.huawei.com/enterprise/zh/doc/EDOC1100401572/d975beba)（Batch 14 核对；组成细节另见 resource-topology.md §A3 样板） | 组成/互联（故障域为候选共享组口径） |
| AMD 边界：本库本轮未取得官方同构超节点公开样板（检索范围为已登记来源与 T01-05 取证）（OEM 节点 AS-8125GS-TNMR2＋MI300X 为节点级）；AMD 只通过平台档案接口边界衔接，不类推超节点能力 | src.supermicro.as-8125gs-tnmr2-manual-mnl-2671-r1.0b、src.amd.instinct-mi300x-platform-datasheet-2023 | [resource-topology.md 四层表](../../knowledge/01-hardware/resource-topology.md)＋[AS-8125GS-TNMR2 手册](https://www.supermicro.com/manuals/superserver/8U/MNL-2671.pdf)＋[MI300X 平台数据表](https://www.amd.com/content/dam/amd/en/documents/instinct-tech-docs/data-sheets/amd-instinct-mi300x-platform-data-sheet.pdf) | 节点级样板（本库本轮未取得官方同构超节点样板——检索范围限已登记来源）；超节点层 unknown |
| 集群参考架构（多机架）：DGX SuperPOD RA——SU 组织、4 SU=128 节点扩展表、四套 fabric（compute IB/storage IB/in-band/OOB）、每 32 节点 rail-aligned、同 SU 同 rail 一跳、跨 rail 过 spine、storage fabric ~4:3 轻超配 | src.nvidia.dgx-superpod-h100-ra-arch-2026-10-09、src.nvidia.dgx-superpod-h100-ra-fabrics-2026-10-09 | [RA 架构页](https://docs.nvidia.com/dgx-superpod/reference-architecture-scalable-infrastructure-h100/latest/dgx-superpod-architecture.html)/[fabric 页](https://docs.nvidia.com/dgx-superpod/reference-architecture-scalable-infrastructure-h100/latest/network-fabrics.html)（Batch 18 核对） | H100 风冷形态的官方参考架构；RA 示例规模非固定定义 |
| 单机样板：DGX H100/H200 UG（8 GPU 节点级）；Atlas 800T A2 产品页 | src.nvidia.dgx-h100-h200-user-guide-2026-01-26、src.huawei.atlas-800t-a2-product-2026-09-29 | [DGX H100/H200 UG](https://docs.nvidia.com/dgx/dgxh100-user-guide/introduction-to-dgxh100.html)（2026-01-26）/[Atlas 800T A2 产品页](https://e.huawei.com/cn/products/computing/ascend/atlas-800t-a2) | 节点组成 |
| 调度/服务逻辑层：K8s 集群架构（控制面/数据面）、Kueue 准入、Slurm 作业与设备资源 | src.kubernetes.cluster-architecture-2026-10-08、src.kueue.admission-v0.19.0、src.slurm.docs-24.11.7 等 | [K8s 集群架构](https://kubernetes.io/docs/concepts/architecture/)（登记 ID src.kubernetes.cluster-architecture-2026-10-08）＋[kubernetes-job-lifecycle](../../knowledge/05-cluster-platform/kubernetes-job-lifecycle.md)/[slurm-jobs-and-device-resources](../../knowledge/05-cluster-platform/slurm-jobs-and-device-resources.md) | 与物理组成分开的调度/服务逻辑 |
| 存储层：Lustre/Ceph/ext4/NFS 四类代表后端 | src.lustre.ops-manual-2x、src.ceph.repo-v19.2.7 等 | [local-and-shared-storage](../../knowledge/04-data-storage/local-and-shared-storage.md)/[object-and-parallel-storage](../../knowledge/04-data-storage/object-and-parallel-storage.md) | 存储路径参考 |
| 互联机制层：NVLink/NVSwitch/IB/RoCE/HCCS/灵衢语义 | src.nvidia.nvlink-nvswitch-page-2026-10-09、src.ascend.hccl-intro-link-types-2026-10-09 等 | [interconnect-paths](../../knowledge/03-communication/interconnect-paths.md)/[ethernet-ib-roce-rdma](../../knowledge/03-communication/ethernet-ib-roce-rdma.md) | 机制不互推 |

## unknown 清单

1. 两个超节点样板的机柜级供电/散热定量沿用 01 域已核口径（DGX SuperPOD DC design 等），本文不重复展开，只按共享依赖引用。
2. AMD 超节点级与集群级参考架构：本库本轮未取得官方同构样板（检索范围为已登记来源与 T01-05 取证），相应维度不作断言，不以 OEM 节点拼装外推。
3. 成本项：无任何可引用单价来源，设计示例的成本仅以符号化变量出现（T00-03 承担量化权衡）。
4. 本文为概念/导航层：架构图为本库原创示意，不代表任何已部署系统；部署关系核对清单为方法，不是已执行的验收记录。

## 初审修订轮（2026-10-21，响应 batch-28-t00-02-codex-review.md 的 C01–C06）

- C01：GB200/A3 故障域改"候选共享组＋条件性假设"（switch tray 影响无量化口径、power shelf N+N 任一失效≠全域、L1 节点内/L2 跨节点分层假设、实际冗余配置为变量、影响映射未核 unknown）；删跨厂商"同构影响"断言；比较表共享故障域行改候选组口径＋节点物理受损≠应用影响定界（链接分布式布局单副本失败段）。
- C02：比较表改"倾向性，非结论"——容量区分物理合计与作业可用/吞吐扩展（须实测）；成本无单价来源排序待核；液冷限定为所选样板组成事实；TP/EP 改"域内机制上更有利"，跨机可用性按布局核对（链接训练并行与状态）。
- C03：设计示例补齐——预登记评价目标；区分 DDP/FSDP 通信形态；B 的域可获得性/放置为待核前提；三条件全满足才进对照，任一未知=无法判定（不自动反转回 A）。
- C04：集群图改四类逻辑路径（计算通信/存储访问/带内控制/带外管理）＋图例（逻辑路径≠物理共网，RA 四套分立为样板事实）；删"BMC 独立供电与时钟"无据保证；新增组件部署职责表（控制服务/节点执行端/负载进程/存储服务/BMC→05/04/01 域入口）。
- C05：来源记录 ID 更正（gb200-nvl72-product-page-2026-10-09；A3 三指南补全 src.huawei. 前缀）；正文 AMD"本库本轮未取得"限定检索范围；删"比较表相应单元格"的不存在承诺。
- C06：正文首段链术语页并注明柜内/跨柜口径与产品名分开；related_ids 补 overview.terms-and-system-boundaries；术语页侧的迁移条目本批已建（双向可达）。

## 复核第一轮修订·补充（2026-10-21，响应 batch-28-t00-02-codex-recheck.md 的 C02/C05/C06 剩余与 N01）

- C02 剩余：比较表数据路径行改"候选瓶颈（待核）"——网络敏感性取决于负载/布局/通信重叠/拓扑拥塞/存储，主导瓶颈须测量；三种形态统一候选口径。
- C05 剩余：来源记录两个裸 ID 补全 src.huawei. 前缀；主张表各关键行补可点击上游定位（GB 硬件页 §1.1-1.4/§2.1、A3 产品概述/组网拓扑、RA 架构/fabric 页）；AMD 范围改"本库本轮未取得"（检索范围限定）；删除不存在单元格承诺（本条已在前轮修订完成，本轮核对一致）。
- C06 剩余：术语页超节点短定义扩为"柜内或跨柜高速互联"，SuperPoD/DGX SuperPOD 标为具体产品名非同义词。
- N01：比较表超节点共享故障域行更正——机柜供电散热为柜内共享组（power shelf/busbar/manifold 为该机柜组成）；上层设施依赖（rPDU/CDU/供液干管）是否多柜共用按实际接线/供液成员核对（无映射 unknown，链接机柜供电散热）；互联保留 L1/L2 分层。

## 复核第二轮修订（2026-10-21，响应 batch-28-t00-02-codex-recheck-2.md 的 C05 剩余）

（订正：该轮脚本实际未生效于 A3 行——见"复核第三轮修订"）- C05 剩余：来源记录 A3 行补产品概述/组网拓扑链接；AMD 行改"本库本轮未取得"并补 OEM 手册/数据表链接；单机样板/调度逻辑/存储层/互联机制行分别替换"既有登记/某域交付正文"为具体页面或仓库正文链接；unknown 行删单元格承诺改"不作断言"；正文关键数字附近补就近上游定位（UG §1.1/§2.1、A3 产品概述/组网拓扑、RA 架构/fabric 页）。

## 复核第三轮修订（2026-10-21，响应 batch-28-t00-02-codex-recheck-3.md 的 C05 剩余）

- C05 剩余（落实主张表与 unknown 清单的现行修订——订正：前两轮脚本对 A3 行均未实际生效，见第四轮修订说明）：AMD 行改"本库本轮未取得"（限定检索范围）并补 OEM 手册/MI300X 数据表链接；单机样板行定位补 DGX H100/H200 UG 与 Atlas 800T A2 产品页链接；调度/服务逻辑行补 K8s 集群架构页与 05 域两篇正文链接；存储层/互联机制行分别替换为 04/03 域实际正文链接；unknown 第 2 条删"比较表相应单元格"承诺改"相应维度不作断言"。正文关键数字就近定位已于上轮落实（本轮核对仍在）。

## 复核第四轮修订（2026-10-21，响应 batch-28-t00-02-codex-recheck-4.md 的 C05 剩余）

- A3 行精确位置栏落实产品概述/组网拓扑可点击链接（前两轮脚本对该行未实际生效，本轮直接验证后写入）；支持范围栏注明故障域为候选共享组口径。
- 四个新增 URL 对齐 registry 登记入口：AS-8125GS→manuals/superserver/8U/MNL-2671.pdf；MI300X→data-sheets/amd-instinct-mi300x-platform-data-sheet.pdf；DGX H100/H200→dgxh100-user-guide/introduction-to-dgxh100.html；Atlas 800T A2→atlas-800t-a2。
- 调度/服务逻辑行的 K8s 架构链接恢复登记入口 kubernetes.io/docs/concepts/architecture/（注明对应登记 ID），不再用 v1-32 快照页冒充原观察页。
- 订正第二轮修订摘要中对 A3 行的错误完成声明。

## 复核第五轮修订（2026-10-21，响应 batch-28-t00-02-codex-recheck-5.md 的 C05 剩余）

- L14 K8s 链接修复：登记 ID 说明移出链接目标（链接本体只含 URL、括注登记 ID 置于链接外），恢复可点击的登记入口。
- L47 订正残留：改为"前两轮脚本对 A3 行均未实际生效"（与 L51 一致）。
