---
id: overview.reference-architectures
title: 单机、集群与超节点的参考架构及选择
type: concept
domain: overview
status: draft
platforms: [generic, nvidia, amd, ascend]
source_refs:
  - src.nvidia.dgx-gb200-user-guide-2026-09-17
  - src.nvidia.gb200-nvl72-product-page-2026-10-09
  - src.nvidia.dgx-superpod-h100-ra-arch-2026-10-09
  - src.nvidia.dgx-superpod-h100-ra-fabrics-2026-10-09
  - src.huawei.atlas-900-a3-superpod-product-2026-10-09
  - src.huawei.atlas-900-a3-superpod-user-guide-13-2026-06-25
  - src.nvidia.dgx-h100-h200-user-guide-2026-01-26
  - src.huawei.atlas-800t-a2-product-2026-09-29
  - src.supermicro.as-8125gs-tnmr2-manual-mnl-2671-r1.0b
  - src.amd.instinct-mi300x-platform-datasheet-2023
  - src.kubernetes.cluster-architecture-2026-10-08
  - src.kueue.admission-v0.19.0
  - src.slurm.docs-24.11.7
updated_at: "2026-10-21"
summary: 比较单机、集群与超节点三种系统组织：各自的控制/数据/管理路径、共同依赖、规模与故障域边界，以及它们对训练/推理任务的适配条件；以 NVIDIA GB200 NVL72 与 Ascend Atlas 900 A3 SuperPoD 两个有官方组成证据的超节点为边界样板，DGX SuperPOD 参考架构为集群样板，AMD 经节点级 OEM 样板与平台档案衔接、不类推超节点能力；给出约束比较表、明确标为假设的设计示例与部署关系核对清单，依赖未知时不输出兼容推荐。
related_ids:
  - hardware.resource-topology
  - hardware.rack-power-cooling-and-failure-domains
  - communication.interconnect-paths
  - data-storage.local-and-shared-storage
  - data-storage.object-and-parallel-storage
  - cluster-platform.kubernetes-job-lifecycle
  - cluster-platform.slurm-jobs-and-device-resources
  - overview.training-lifecycle
  - overview.inference-lifecycle
  - overview.terms-and-system-boundaries
  - overview.design-targets-and-tradeoffs
applicability:
  environment_refs: []
  notes: "超节点样板证据为 DGX GB200 用户指南（2026-09-17）与 Atlas 900 A3 SuperPoD 产品页/用户指南 13（Batch 14 已核）；集群样板为 DGX SuperPOD H100 参考架构（Batch 18 已核）；本文为概念层比较，不代表任何已部署系统，不构成选型结论或兼容性承诺。"
verification:
  status: source_checked
  evidence_refs:
    - src.nvidia.dgx-gb200-user-guide-2026-09-17
    - src.huawei.atlas-900-a3-superpod-user-guide-13-2026-06-25
    - src.nvidia.dgx-superpod-h100-ra-arch-2026-10-09
  notes: "全部复用既有登记来源（Batch 14/18 核对口径），本轮无新增外部来源；组成/互联/故障域主张的精确锚点见 docs/research/batch-28-t00-02-sources.md 与 resource-topology.md 的样板章节。未访问任何真实系统。"
---

# 单机、集群与超节点的参考架构及选择

## 要回答的问题

同一批 GPU/NPU 可以组织成三种形态：**单机**（一个服务器节点内的加速器域）、**集群**（多节点经通用网络互联、由调度器统一管理）、**超节点**（多节点/托盘经厂商专用交换结构组成的高速互联域）。三者不是规模递进的同一事物——控制路径、数据路径、共享依赖与故障域结构各不相同，"买更多节点"不会自动从一种形态变成另一种（术语"超节点"的统一口径见[术语与系统边界](terms-and-system-boundaries.md)——厂商定义的柜内或跨柜高速互联域，与 SuperPoD 等具体产品名分开）。本文给出三类的概念架构、以官方组成证据固定的两个超节点样板与一个集群样板、约束比较表和部署核对方法；具体兼容推荐须待依赖交集核实（见边界）。

## 三类概念架构

以下为本库**原创概念图**：方框与连线是占位结构，不代表任何具体厂商实现；把每条边替换为有来源的端点与链路类型才是实际记录（记录字段见[计算节点资源与拓扑参考](../01-hardware/resource-topology.md)）。

**单机（节点内加速器域）**

```
        ┌────────────────── 一个服务器节点（独立 OS 实例）──────────────────┐
        │  主机侧：CPU/内存/NUMA ── PCIe/NVLink 类节点内互联 ── 加速器域    │
        │  本地启动盘/NVMe ── 主机                                       │
        │  带外管理通道（BMC；供电与时钟归属按机型证据记录，不作独立性保证）  │
        └──────────────────────────────────────────────────────────────┘
控制路径＝本机 OS/驱动/运行时；服务逻辑＝单进程或单机多进程
```

**集群（多节点＋通用网络＋调度器）**

```
 机柜A[节点,节点]──计算通信 fabric（以太/IB/RoCE，leaf-spine 类）──节点间
 机柜B[节点,节点]──存储访问路径（独立或共网：部署条件，需记录）──并行/对象存储
 机柜C[节点,节点]──带内控制（API/调度流量）──管理面：调度器/控制器＋队列/配额
            └────带外管理通道（BMC，独立或共网：部署条件）────┘
```
图例：实线为**逻辑路径**分类；四类路径是否共物理网络是部署事实（所选 H100 RA 为四套分立 fabric，见下文），不得从图读出共用或分立。

**超节点（专用交换结构域）**

```
 ┌───────────── 一个高速互联域（可跨多机柜）─────────────┐
 │ 计算托盘/节点 ──┐                                      │
 │ 计算托盘/节点 ──┼─ 厂商专用交换结构（总线板/交换托盘、   │
 │ 计算托盘/节点 ──┘  铜背板/光纤，L1/L2 或 NVSwitch 层） │
 │ 交换/总线设备与机柜级供电、液冷 manifold 为共享上游      │
 └──────────────────────────────────────────────────────┘
 域外仍需集群式通用网络（参数面/存储面/管理面）与调度器
```

**物理组成与调度/服务逻辑必须分开**：超节点是物理互联形态，集群的调度/服务逻辑（队列、配额、gang、生命周期）在超节点之上照常存在——一个 Atlas 900 A3 SuperPoD 或 GB200 NVL72 机柜仍然要回答"谁在什么约束下用哪部分卡"，那是[05 领域](../05-cluster-platform/index.md)的问题；反过来，把多节点集群的卡数加到"等效超节点"是不成立的（互联与故障域不同）。

三类架构共同的**组件部署职责**（概念层对应，细节在对应领域）：

| 组件 | 部署位置 | 职责 | 细节入口 |
|---|---|---|---|
| 控制服务（调度器/控制器/API） | 管理节点/控制面 | 准入、放置、生命周期 | [K8s 作业生命周期](../05-cluster-platform/kubernetes-job-lifecycle.md)、[Slurm 作业与设备资源](../05-cluster-platform/slurm-jobs-and-device-resources.md) |
| 节点执行端（kubelet/Slurmd/驱动/运行时） | 每节点 | 本地资源执行与上报 | 同上两篇 |
| 负载进程（训练/推理引擎） | 计算/加速器域 | 模型执行（本文各架构的"数据路径"主体） | [训练端到端路径](training-lifecycle.md)/[推理端到端路径](inference-lifecycle.md) |
| 存储服务/客户端 | 存储节点＋各节点客户端 | 数据与制品读写 | [本地与共享存储](../04-data-storage/local-and-shared-storage.md) |
| BMC/带外管理 | 每节点 | 硬件健康与远程管理 | [BMC、固件与事件](../01-hardware/bmc-firmware-and-events.md) |

## 两个有官方证据的超节点样板

### NVIDIA：GB200 NVL72（DGX GB 用户指南，2026-09-17）

一个 NVL72 机柜＝**72-GPU NVLink 域**：18× 1RU compute tray（每 tray 2× Grace＋4× Blackwell）＋9× 1RU NVLink switch tray＋2× 管理 TOR＋power shelf（[UG 硬件页 §1.1](https://docs.nvidia.com/dgx/dgxgb200-user-guide/hardware.html)）；tray 经背部连接器接入 cable cartridge 无源铜背板连通全部 compute tray 与 switch tray；NVLink 5.0 每 GPU 双向 1.8 TB/s，fabric 由 Fabric Manager（NVLSM）管理，NVSwitch 支持 SHARP 网内计算（[UG §2.1](https://docs.nvidia.com/dgx/dgxgb200-user-guide/)）（DGX GB UG §1/§2.1；产品页宣称口径与 HPE/Supermicro OEM 分列，详见[资源拓扑](../01-hardware/resource-topology.md)样板节）。**超节点定义按厂商**："single rack as a 72-GPU NVLink domain" 是 NVIDIA 产品页口径；更大规模（DGX GB UG 引言"multi-rack deployments such as a SuperPOD (eight NVL72 racks)"，"such as" 为示例）属于集群级组织，不是更大的单一 NVLink 域。故障域**候选共享组**（条件性假设，实际影响待验证）：NVLink switch tray、cable cartridge、机柜级供电与液冷是全域共享上游——存在影响整个域的**候选路径**（switch tray 失效的影响无量化口径；power shelf 为 N+N 冗余，任一 shelf 失效不等同全域故障；实际影响按机型/冗余配置与失效模式核对，[资源拓扑](../01-hardware/resource-topology.md)把这些列为待验证假设）。

### Ascend：Atlas 900 A3 SuperPoD（产品页＋用户指南 13）

最大形态 12× 计算柜＋4× 总线设备柜（384 NPU/192 鲲鹏 CPU 上限，[产品概述](https://support.huawei.com/enterprise/zh/doc/EDOC1100401572/bd23f260)）；超节点内部通信走灵衢 LQC 协议（[组网拓扑](https://support.huawei.com/enterprise/zh/doc/EDOC1100401572/d975beba)）（华为缓存一致性互联接口），7 平面组网：L1 层由计算节点内灵衢总线板承载、L2 层由总线设备柜内 LingQu 630 组成，L1–L2 按规模用铜缆或光纤；支持 16/32/64/128/256/384 卡逻辑超节点。**定义边界条款**（用户指南原文）：「当组网不涉及总线设备柜时，计算柜就是 Atlas 900 A3 SuperPoD 超节点」——超节点与机柜不是固定两个层级，按实际组网形态确定；「物理架构 384，实际部署数量取决于解决方案可靠性冗余设计」——384 是物理上限不是必然可用规模。故障域**候选共享组**（与 GB200 同为分层共享结构，但**不跨厂商断言同构影响**）：总线设备柜、灵衢总线板、机柜供电与液冷为共享上游——L1 总线板位于节点内（先按节点边界提出假设）、L2 总线设备柜为跨节点共享、实际冗余配置是变量，具体影响映射未取得（unknown，[资源拓扑](../01-hardware/resource-topology.md) A3 样板节与待验证假设）。

### AMD 的位置与集群样板

AMD 同构超节点：本库本轮未取得官方公开样板（[资源拓扑](../01-hardware/resource-topology.md)已核，超节点层保持 unknown、不向上类推）；其定位是：节点级 OEM 样板（如 AS-8125GS-TNMR2＋8× MI300X、节点内 Infinity Fabric 全互连）＋平台档案（ROCm 软件栈边界，见[AMD ROCm 样板档案](../02-software-stack/amd-rocm-documented-profile.md)）经通用接口（PCIe/以太/RoCE 类）接入集群形态。**集群参考样板**用 DGX SuperPOD H100 参考架构（官方 RA）：SU（scalable unit）组织、4 SU=128 节点的 Leaf/Spine/Core 扩展表；四套 fabric（compute IB/storage IB/in-band/OOB）；每 32 节点 rail-aligned、同 SU 同 rail 一跳、跨 rail 过 spine、storage fabric 约 4:3 轻超配（[RA 架构页](https://docs.nvidia.com/dgx-superpod/reference-architecture-scalable-infrastructure-h100/latest/dgx-superpod-architecture.html)/[fabric 页](https://docs.nvidia.com/dgx-superpod/reference-architecture-scalable-infrastructure-h100/latest/network-fabrics.html)，Batch 18 核对）。RA 是官方示例规模，不是固定定义。

## 约束比较与选择核对

| 约束 | 单机 | 集群 | 超节点 |
|---|---|---|---|
| 典型加速器域 | 节点内 8× GPU/NPU 级 | 数十～数千卡，通用网络分摊 | 数十～数百卡，专用结构低时延高带宽（GB200 NVL72=72 GPU 域；A3 逻辑 16–384 卡） |
| 数据路径候选瓶颈（待核，非定论） | 节点内互联＋单机 I/O | 网络是**候选**瓶颈之一——是否主导取决于负载与并行布局、通信量与重叠、实际拓扑/拥塞及端到端存储（见[互联路径](../03-communication/interconnect-paths.md)）；目标系统的主导瓶颈与扩展收益须测量 | 域内专用结构；域外仍走通用网络 |
| 共享故障域（候选，影响待验证） | 整机（供电/散热/主板） | 网络与调度控制面是新增共享项；节点物理受损≠应用影响定界——作业影响还取决于 collective/作业组依赖与副本进展（见[分布式推理布局](../07-inference/distributed-inference-layouts.md)单副本失败段） | 交换结构/总线设备按层次核对（L1 节点内、L2 跨节点/跨柜按组网形态）、机柜供电散热为**柜内**共享组（power shelf/busbar/manifold 是该机柜组成）——更上层的设施依赖（rPDU/CDU/供液干管等）是否被多柜共用须按实际接线/供液成员核对（[机柜供电散热共享依赖](../01-hardware/rack-power-cooling-and-failure-domains.md)，无映射即 unknown）；按部件/冗余前提/失效模式分别列候选组（N+N 供电等），实际影响映射未核（unknown） |
| 容量与成本（倾向性，非结论） | 上限＝节点规格 | 物理卡数/内存合计随节点数近线性，但**作业可用容量与吞吐扩展**取决于模型/布局、通信量与重叠、存储与拥塞——须实测；成本与能耗的量化权衡与验收口径见[设计目标与权衡](design-targets-and-tradeoffs.md)（无单价来源，成本排序待核） | 所选样板（GB200 NVL72/A3）均为机柜级液冷组成（样板事实，非通用必然）；域的带宽/价格溢价与净收益未取得证据，待核 |
| 适合的作业形态（机制性倾向） | 单节点放得下的模型/实验；调试 | 数据/模型并行可切分、通信可容忍网络的训练与推理集群 | 强一致通信密集负载（TP/EP 等）在低时延高带宽域内**机制上更有利**（[训练并行与状态](../06-training/parallelism-and-state.md)的机制倾向）——跨机 TP/EP 是否可用、是否满足目标须按布局与互联分别核对，不是域外不可用 |
| 调度/服务逻辑 | 本机进程 | 调度器＋队列＋配额（[K8s](../05-cluster-platform/kubernetes-job-lifecycle.md)/[Slurm](../05-cluster-platform/slurm-jobs-and-device-resources.md)） | 逻辑同集群，另有域资源（交换结构/总线设备）的分配与隔离问题 |

**标为假设的设计示例**（非实测、非推荐，只示范比较结构与所需前提）：设某训练任务（固定实现——如普通 DDP 梯度同步或 FSDP `FULL_SHARD` 参数 all-gather，两者通信形态不同，[训练并行与状态](../06-training/parallelism-and-state.md)）需要 TP=8 的单域＋总 64 卡；候选 A＝8 台 8 卡单机组集群（TP 机内、DP 跨机走以太/RoCE），候选 B＝1 个 64 卡超节点域＋其余集群化（64 卡域的可获得性/可放置性本身是待核前提——逻辑卡数列表不证明可分配实现）。**预登记的评价目标**（如固定资源与质量目标下的步时间/成本）后，才谈得上比较；候选 B 值得进入对照验证的条件：①跨机通信占步时间比例 p（按固定窗口与分母测量）显著到域内/域外差异有意义；②域的获取成本溢价 r（限定比较范围）可接受；③域的放置/隔离与软件支持满足任务布局。三项**全部满足**才值得进入实测对照；**任一未知或不满足时结论为"无法判定"**，不是自动反转回 A 更优——A 的优劣同样须实测。p 与 r 为待测/待询价变量，本示例不给出数值结论。

## 部署关系核对清单

对任一实际系统，按层核对（逐项有来源才算关闭）：

1. **物理层**：节点/托盘/交换结构清单与型号；节点内互联类型；供电/散热方案与共享上游（[机柜供电散热](../01-hardware/rack-power-cooling-and-failure-domains.md)）。
2. **网络层**：几套 fabric、各走什么协议、rail/平面组织、带外管理网（[互联路径](../03-communication/interconnect-paths.md)）。
3. **存储层**：本地/共享/并行/对象存储的挂载与数据路径（[本地与共享存储](../04-data-storage/local-and-shared-storage.md)、[对象与并行存储](../04-data-storage/object-and-parallel-storage.md)）。
4. **调度/服务层**：调度器与队列/配额/gang 约定；超节点域资源如何被分配为调度单元（若有专用分域机制，按该平台文档核对）。
5. **故障域**：逐层标出共享上游与其失效影响范围；冗余设计（供电 N+M、链路冗余）与厂商声明对齐。
6. **任务映射**：训练/推理的并行布局落在哪些域/网络（[训练端到端路径](training-lifecycle.md)、[推理端到端路径](inference-lifecycle.md)）。

任一层依赖未知（如超节点域的调度分配机制、跨域网络实测带宽）时，**不输出兼容/性能推荐**，先按独立验证轨道补证据（见[完整覆盖规划的验证工作包](../../docs/full-coverage-roadmap.md)）。

## 边界与未知

- 两个超节点样板的机柜级供电/散热定量、可替换部件粒度与 OEM 冲突口径沿用[资源拓扑](../01-hardware/resource-topology.md)与 01 域已核边界（GB200 无 FRU 清单、A3 细部手册条款未取得等），本文不重复展开。
- AMD 超节点层与集群级参考架构：本库本轮未取得官方同构样板（检索范围见取证记录），相应维度不作断言；集群级另有 DGX SuperPOD RA（NVIDIA 线）。
- 超节点域资源的调度分配机制（如 A3 逻辑超节点 16–384 卡如何被平台切分给租户/作业）：公开文档未见细节，unknown。
- 本文架构图为本库原创示意；来源冲突（算力档位、E1.S 数量等）按[资源拓扑](../01-hardware/resource-topology.md)的分列口径保留。
- 成本与能耗的量化权衡与验收表由[设计目标与权衡](design-targets-and-tradeoffs.md)承担；本文只用符号变量。

## 来源与验证记录

- [NVIDIA DGX GB Rack Scale Systems User Guide（2026-09-17）](https://docs.nvidia.com/dgx/dgxgb200-user-guide/hardware.html)与[GB200 NVL72 产品页](https://www.nvidia.com/en-us/data-center/gb200-nvl72/)：NVLink 域组成/拓扑/宣称口径（Batch 14 核对）。
- [Atlas 900 A3 SuperPoD 产品页](https://e.huawei.com/cn/products/computing/ascend/atlas-900-a3-superpod)与[用户指南 13](https://support.huawei.com/enterprise/zh/doc/EDOC1100401572)：组成/灵衢组网/边界条款（Batch 14 核对）。
- [DGX SuperPOD H100 参考架构](https://docs.nvidia.com/dgx-superpod/reference-architecture-scalable-infrastructure-h100/latest/dgx-superpod-architecture.html)（架构页/[fabric 页](https://docs.nvidia.com/dgx-superpod/reference-architecture-scalable-infrastructure-h100/latest/network-fabrics.html)）：SU 组织与四套 fabric（Batch 18 核对）。
- 节点级样板与平台档案：DGX H100/H200 UG、Atlas 800T A2 产品页、Supermicro AS-8125GS-TNMR2、MI300X 平台数据表（既有登记）。
- 逐条主张与复用定位见[第二十八批 T00-02 来源记录](../../docs/research/batch-28-t00-02-sources.md)。
- 当前验证范围：来源核对（全部复用既有登记）；未访问任何真实系统，未执行选型核对。
