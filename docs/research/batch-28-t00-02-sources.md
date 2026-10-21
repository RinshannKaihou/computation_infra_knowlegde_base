# 第二十八批 T00-02 来源记录

任务：T00-02（单机、集群与超节点的参考架构及选择；**new** `knowledge/00-overview/reference-architectures.md`，主题 00.4）。取证轮次：主会话作者角色首轮（2026-10-21；前置 T01-05/T03-01/T04-03/T05-02/T05-03 均 done）。本轮**无新增外部来源**：两个超节点样板与集群/存储/调度证据全部复用既有登记，evidence_blocker 依 Batch 14/18 已核来源解除。

## 复用来源与主张定位

| 主张 | 登记 ID | 精确位置 | 支持范围 |
|---|---|---|---|
| NVIDIA 超节点样板：GB200 NVL72＝18 compute tray＋9 NVLink switch tray＋2 TOR＋power shelf，72-GPU NVLink 域；NVLink 5.0 1.8 TB/s、cable cartridge 铜背板、Fabric Manager（NVLSM）管理、SHARP；HPE/Supermicro OEM 口径与 E1.S/算力档位冲突按来源分列 | src.nvidia.dgx-gb200-user-guide-2026-09-17、src.nvidia.gb200-nvl72-product-page-2026-09-09、src.hpe.gb200-nvl72-quickspecs-a50009224enw-v6、src.supermicro.supercluster-gb200-nvl72-datasheet-2025 | resource-topology.md（T01-05 交付）§GB200 样板；UG §1/§2.1 | 组成/互联/故障域枚举；可替换粒度只到 tray/背板级 |
| Ascend 超节点样板：Atlas 900 A3 SuperPoD＝12 计算柜＋4 总线设备柜（384 NPU/192 CPU 上限）；灵衢 LQC 7 平面、L1 总线板/L2 LingQu 630、铜/光分界；"计算柜即超节点"边界条款；物理 384 与实际部署冗余声明 | src.huawei.atlas-900-a3-superpod-product-2026-10-09、atlas-900-a3-superpod-user-guide-13-2026-06-25、atlas-900-a3-superpod-maintenance-guide-14-2026-08-18、src.huawei.lingqu-630-v1-user-guide-03-2026-01-30 | resource-topology.md（T01-05 交付）§A3 样板 | 组成/互联/故障域 |
| AMD 边界：无官方同构超节点公开样板（OEM 节点 AS-8125GS-TNMR2＋MI300X 为节点级）；AMD 只通过平台档案接口边界衔接，不类推超节点能力 | src.supermicro.as-8125gs-tnmr2-manual-mnl-2671-r1.0b、src.amd.instinct-mi300x-platform-datasheet-2023 | resource-topology.md 四层表 | 节点级样板；超节点层 unknown |
| 集群参考架构（多机架）：DGX SuperPOD RA——SU 组织、4 SU=128 节点扩展表、四套 fabric（compute IB/storage IB/in-band/OOB）、每 32 节点 rail-aligned、同 SU 同 rail 一跳、跨 rail 过 spine、storage fabric ~4:3 轻超配 | src.nvidia.dgx-superpod-h100-ra-arch-2026-10-09、src.nvidia.dgx-superpod-h100-ra-fabrics-2026-10-09 | RA 架构页/fabric 页（Batch 18 核对） | H100 风冷形态的官方参考架构；RA 示例规模非固定定义 |
| 单机样板：DGX H100/H200 UG（8 GPU 节点级）；Atlas 800T A2 产品页 | src.nvidia.dgx-h100-h200-user-guide-2026-01-26、src.huawei.atlas-800t-a2-product-2026-09-29 | 既有登记 | 节点组成 |
| 调度/服务逻辑层：K8s 集群架构（控制面/数据面）、Kueue 准入、Slurm 作业与设备资源 | src.kubernetes.cluster-architecture-2026-10-08、src.kueue.admission-v0.19.0、src.slurm.docs-24.11.7 等 | 05 域交付正文 | 与物理组成分开的调度/服务逻辑 |
| 存储层：Lustre/Ceph/ext4/NFS 四类代表后端 | src.lustre.ops-manual-2x、src.ceph.repo-v19.2.7 等 | 04 域交付正文 | 存储路径参考 |
| 互联机制层：NVLink/NVSwitch/IB/RoCE/HCCS/灵衢语义 | src.nvidia.nvlink-nvswitch-page-2026-10-09、src.ascend.hccl-intro-link-types-2026-10-09 等 | 03 域交付正文 | 机制不互推 |

## unknown 清单

1. 两个超节点样板的机柜级供电/散热定量沿用 01 域已核口径（DGX SuperPOD DC design 等），本文不重复展开，只按共享依赖引用。
2. AMD 超节点级与 T00-02 集群级参考架构：无官方公开样板，比较表中相应单元格保持 unknown，不以 OEM 节点拼装外推。
3. 成本项：无任何可引用单价来源，设计示例的成本仅以符号化变量出现（T00-03 承担量化权衡）。
4. 本文为概念/导航层：架构图为本库原创示意，不代表任何已部署系统；部署关系核对清单为方法，不是已执行的验收记录。
