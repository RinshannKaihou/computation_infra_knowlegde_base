---
id: communication.interconnect-paths
title: 节点内、节点间与超节点互联路径参考
type: reference
domain: communication
status: draft
platforms: [generic, nvidia, ascend]
source_refs:
  - src.nvidia.dgx-h100-h200-user-guide-2026-01-26
  - src.nvidia.nvlink-nvswitch-page-2026-10-09
  - src.nvidia.hopper-architecture-page-2026-10-09
  - src.nvidia.h100-product-page-2026-10-09
  - src.nvidia.dgx-superpod-h100-ra-arch-2026-10-09
  - src.nvidia.dgx-superpod-h100-ra-fabrics-2026-10-09
  - src.nvidia.nvidia-smi-manual-2026-10-09
  - src.nvidia.nccl-user-guide-2.27.5
  - src.huawei.atlas-800t-a2-product-2026-09-29
  - src.ascend.cann-aclrt-devices-topo-2026-10-09
  - src.ascend.mindcluster-affinity-principles-730-2026-10-09
  - src.ascend.hccl-intro-link-types-2026-10-09
  - src.ascend.mind-cluster-v26.1.1
  - src.huawei.atlas-900-a3-superpod-product-2026-10-09
  - src.huawei.atlas-900-a3-superpod-user-guide-13-2026-06-25
  - src.huawei.atlas-900-a3-superpod-maintenance-guide-14-2026-08-18
  - src.huawei.atlas-900-a3-superpod-brochure-26h1
  - src.huawei.lingqu-630-v1-user-guide-03-2026-01-30
updated_at: "2026-10-10"
summary: "以 DGX H100（NVLink 4 代/NVSwitch）与 Atlas 800T A2 + Atlas 900 A3 SuperPoD 为两个独立样板，给出端口—设备—交换结构—网络路径—共享故障域的核对表、两份原创物理路径图、软件发现视图到资产记录的核对行、异常候选与最小路径验证计划；文档带宽口径与作业可用带宽分开，Ascend 缺口如实保留 unknown。"
related_ids:
  - hardware.resource-topology
  - communication.collectives-and-rank-progress
  - communication.bandwidth-baselines
  - communication.bandwidth-degradation-triage
  - communication.rdma-baseline-and-congestion-triage
  - communication.ethernet-ib-roce-rdma
applicability:
  environment_refs: []
  notes: "尚无环境档案：DGX H100 样板固定用户指南（2026-01-26 更新）与 NVLink 产品页（2026-10-09 观察）；Ascend 样板固定 800T A2 产品页、A3 SuperPoD 用户指南组与 LingQu 630 V1 指南；CANN 900 aclrt 页适用表按 2026-10-10 原文逐行转录（training/inference 合并行，见样板 A）；目标机型/互联代次需另行固定。"
verification:
  status: source_checked
  evidence_refs:
    - src.nvidia.dgx-h100-h200-user-guide-2026-01-26
    - src.ascend.mindcluster-affinity-principles-730-2026-10-09
    - src.ascend.cann-aclrt-devices-topo-2026-10-09
  notes: "对照第十八批取证记录所列固定版本来源核对；三份原创 ASCII 图（N-1、A-1、A-2，有证边/逻辑归属/unknown 图例一致，A2/A3 独立片段），未复制官方拓扑图；DGX Table 5 计算网 8 端口全量 + Slot/板载字段摘要（Slot3 类型不推定）+ Table 6 联合身份；CANN 六行适用表逐行转录（C01 CLOSED）；nvidia-smi 按 topo 矩阵亲和/nvlink 本端状态/remote 远端三入口分列，目标工具版本未固定；计划 N/A 观察点与上表对应；未在任何互联硬件上执行验证。"
---

# 节点内、节点间与超节点互联路径参考

## 范围与阅读方式

本文只做一件事：给出"作业 traffic 实际经过哪些物理段、每段归谁管、坏了看哪里"的核对表。两个样板各自独立——NVIDIA 侧 DGX H100（SXM 形态，NVLink 4 代/NVSwitch），Ascend 侧 800T A2 节点 + Atlas 900 A3 SuperPoD。分层见[板卡到超节点组成](../01-hardware/resource-topology.md)；集合通信语义见[集合通信与 rank 进度](collectives-and-rank-progress.md)；基线与退化诊断见[带宽基线](bandwidth-baselines.md)与[退化诊断](bandwidth-degradation-triage.md)。独立于 collective 的网络对照流程见[RDMA 网络基线、路由与拥塞诊断](rdma-baseline-and-congestion-triage.md)。

硬边界：**文档标称带宽 ≠ 作业可用带宽**。H100 SXM 版 NVLink 900GB/s 与 H100 NVL 版 600GB/s 是两种形态（[H100 产品页](https://www.nvidia.com/en-us/data-center/h100/)），DGX H100 样板只取前者；作业可用值归基线轨道（T03-03）的实测口径，本文只记录文档口径。

## 样板 N：DGX H100（节点内 + 节点间 fabric）

机型与互联代次固定：8×H100、节点内 900GB/s GPU-to-GPU、4×NVSwitch 芯片（[DGX H100/H200 用户指南](https://docs.nvidia.com/dgx/dgxh100-user-guide/introduction-to-dgxh100.html)，2026-01-26 更新；指南把 NVSwitch 行写成 "4 x 4th generation NVLinks"，引用时照录原文、不改写代次归属）。NVLink 代次锚定（4 代=900GB/s、18 links/GPU，页脚 preliminary 可变）见 [NVLink 产品页](https://www.nvidia.com/en-us/data-center/nvlink/)。

### 图 N-1：DGX H100 物理路径（原创示意）

```text
图例：── 有证边（指南/RA 明确记载）  ┄┄ 逻辑归属（Table 6 GPU 列，无直连线缆证据）

[GPU0..7] ──NVLink── [4× NVSwitch]          节点内交换（组件表 + System Topology 图节）
[GPU0..7] ──PCIe Gen5── [CPU Xeon 8480C]    主机路径（128GB/s 口径见 H100 产品页）
[CX-7 卡 ×8] ──DensiLink── [OSFP P1/P2] ──线缆── [rail fabric]
      │                          │
  网络模块内 4 卡合一       同一 OSFP 的 P1/P2 来自两张不同卡
[GPU7] ┄┄归属┄┄ [模块1/CX0/mlx5_11/OSFP1P1]   例：归属≠直连（Table 6 GPU 列）
```

有证边（实线）：GPU↔NVSwitch、GPU↔CPU PCIe、卡→OSFP（Table 5/6）、OSFP→fabric（RA fabric 页）。GPU 到 CX 卡只有 Table 6 GPU 列的逻辑归属（虚线），**无 GPU—CX 直连线缆证据**，不得把归属线读成物理边。Unknown：官方拓扑矢量边清单未取得，线缆级走线不展开。

### 端口映射（Table 5 计算网络 8 端口全量转录，联合身份）

指南 Table 5 "Network Port Mapping"（Port Designation / PCI Bus / Default IB / RDMA 设备名），计算网络 8 个 OSFP 端口逐行全量转录：

| OSFP 端口 | PCI Bus | 默认 IB 名 | RDMA 名 |
|---|---|---|---|
| OSFP1P1 | dc:00.0 | ibp220s0 | mlx5_11 |
| OSFP1P2 | 9a:00.0 | ibp154s0 | mlx5_6 |
| OSFP2P1 | ce:00.0 | ibp206s0 | mlx5_10 |
| OSFP2P2 | c0:00.0 | ibp192s0 | mlx5_9 |
| OSFP3P1 | 4f:00.0 | ibp79s0 | mlx5_4 |
| OSFP3P2 | 40:00.0 | ibp64s0 | mlx5_3 |
| OSFP4P1 | 5e:00.0 | ibp94s0 | mlx5_5 |
| OSFP4P2 | 18:00.0 | ibp24s0 | mlx5_0 |

另有 Slot1 P1/P2（aa:00.0/aa:00.1，ibp170s0f0/f1，mlx5_7/mlx5_8）、Slot2 P1/P2（29:00.0/00.1，ibp41s0f0/f1，mlx5_1/mlx5_2）、Slot3 P1/P2（82:00.0/00.1，ens6f0/f1，irdma0/irdma1）与板载口（0b:00.0，eno3）——以上为原表字段摘要（未完整展开用途与卡型号；Slot3 卡类型无精确 BOM 证据，不推定），属扩展/管理面，不计入计算 rail。

### 网络模块与 CX 编号（Table 6 联合身份，C02 修正）

指南原文："Consolidates four ConnectX-7 networking cards into a single device"（每网络模块 4 张卡），"Two networking modules are installed on interposer board"（共 8 张卡），"Each DensiLink cable has two ports, one from each ConnectX-7 card"（每根 DensiLink 线缆的两个端口来自两张不同卡）。

**CX 编号是模块内局部编号，不可跨模块合并**。Table 6 "Network Modules"（Port / ConnectX Device / Network Module-CPU / GPU / Default / RDMA）：模块 1（含 CPU1）CX0–CX3 对应 OSFP1P1/CX0→GPU7/dc:00.0/mlx5_11、OSFP1P2/CX1→GPU4、OSFP2P1/CX2→GPU6、OSFP2P2/CX3→GPU5；模块 0（含 CPU0）CX2/CX3/CX0/CX1 对应 OSFP3P1/CX2→GPU2、OSFP3P2/CX3→GPU1、OSFP4P1/CX0→GPU3/5e:00.0/mlx5_5、OSFP4P2/CX1→GPU0。例如两个 "CX0" 分别是 GPU7（模块 1）与 GPU3（模块 0），BDF 与 mlx5 名均不同。资产记录必须以**模块/CPU + CX + 槽位 + BDF + mlx5 名**联合身份建档，禁止以 CX 标签单独合并。

### 共享故障域（修正：只写原文明确共用的组件）

- 单 NVSwitch 芯片（4 芯片服务 8 GPU，组件表）。
- 单网络模块（含其中 4 张 CX-7 卡）与转接板（interposer）。
- 单根 DensiLink 线缆 / 单个 OSFP 连接器的 P1+P2 对（两端口来自两张卡：如 OSFP1P1↔CX0 与 OSFP1P2↔CX1 同命运）。
- 单 PSU 组（4+2，组件表）。
- storage fabric 约 4:3 轻超配（拥塞候选，RA fabric 页）。

### 软件发现 → 资产记录核对行（展开一组示例）

| 软件身份 | 物理资产字段 | 映射依据 |
|---|---|---|
| `mlx5_11`（ibp220s0，dc:00.0） | OSFP1P1；模块 1/CX0；GPU7；CPU1 侧 | Table 5 行 + Table 6 行联合 |
| `mlx5_5`（ibp94s0，5e:00.0） | OSFP4P1；模块 0/CX0；GPU3；CPU0 侧 | Table 5 行 + Table 6 行联合（与上一行 CX 同名不同卡） |
| `nvidia-smi topo -m` | GPU↔NIC/直连设备连接矩阵 + CPU/内存亲和（legend X/SYS/NODE/PHB…；Linux only）；**不是完整 BDF 身份表**，不反推物理边 | [nvidia-smi 手册 topo 节](https://docs.nvidia.com/deploy/nvidia-smi/index.html)（手册无版本号，输出字段以目标机驱动版本为准，当前未固定） |
| `nvidia-smi nvlink --status` + `-p/--pcibusid` + `-R/--remotelinkinfo` | `--status` 给本端链路状态与 Active 带宽；远端 PCI bus / 远端 device+NVLink ID 须另用 `-p` / `-R` 子命令取得，"两端"需组合 | 同上手册 nvlink 第 4/6/7 项（协商值与标称分列） |
| `nvidia-smi -q` Platform Info | Chassis/Slot/Tray/Host ID/GPU Fabric GUID（稳定 ID 优先） | 同上 |
| NCCL `NCCL_TOPO_DUMP_FILE` + /sys | 虚拟拓扑降级为"次优假设" | [NCCL 2.27.5 troubleshooting](https://docs.nvidia.com/deeplearning/nccl/archives/nccl_2275/user-guide/docs/troubleshooting.html)（Topology detection/GPU Direct/env 三节；`topo -m` 语句不在 2.27.5 页内，不引用） |
| `lspci -vvv` ACS | SrcValid+ 记异常候选 | 同上 troubleshooting 页 GPU Direct 节 |

其余 6 个 OSFP 端口按相同联合身份逐行建档（字段同上，略写）。

### 节点间 fabric 与超节点范围

compute IB / storage IB / in-band / OOB 四套 fabric 分立；每 32 节点 rail-aligned、同 SU 同 rail 一跳、跨 rail 过 spine（[SuperPOD RA Network Fabrics](https://docs.nvidia.com/dgx-superpod/reference-architecture-scalable-infrastructure-h100/latest/network-fabrics.html)，Last updated Nov 19, 2025）。4 SU=128 DGX 节点起，可扩至 64 SU/2000+ 节点（RA 示例规模，非固定定义，[SuperPOD RA Architecture](https://docs.nvidia.com/dgx-superpod/reference-architecture-scalable-infrastructure-h100/latest/dgx-superpod-architecture.html)）。

### 最小路径验证计划 N（待执行）

- 固定输入：两节点同 rail（Table 6 模块/CPU/GPU/OSFP 四元组快照）+ `nvidia-smi topo -m`（连接矩阵+亲和）/ `nvlink --status`（本端状态+Active 带宽）/ `-p`/`-R`（远端 PCI bus 与远端 device+link）快照 + NCCL TOPO dump。
- 比较对象：同 rail 对打 vs 跨 rail 对打（RA fabric 页一跳/过 spine 区分）；`ib_write_bw` 同参两轮。
- 观察点：带宽/时延 + `port_xmit/recv_data` 增量 + 路径快照（`ibroute`，IB fabric）；NVLink 两端对齐以后者 `-R` 输出为准，不用 `--status` 单命令断言。
- 通过：同 rail 达到基线带内且计数器零错误增量。失败：错误计数增量或带宽低于基线带。无法判断：快照缺失、版本/参数不一致、跨 rail 路由未对齐、nvidia-smi 目标版本未固定（记 unknown，不归因）。不填执行结果。

## 样板 A：800T A2 节点 + A3 SuperPoD（稀疏版）

机型锚点：800T A2 主机/网络/供电规格（4×鲲鹏920、8×200GE QSFP RoCE、PCIe 4.0×3，[产品页](https://e.huawei.com/cn/products/computing/ascend/atlas-800t-a2)）；**NPU 数量、单 NPU 内存、NPU—CPU/HCCS 边未知**（产品页无，用户指南 support 页不可达）。

### CANN 900 aclrtGetDevicesTopo 适用表（逐行转录，C01）

2026-10-10 实测 canonical 页（`doc_center/source/en/CANNCommunityEdition/900/...`）与 `:6066` 端口页**字节一致（均 12307 B），内容相同**，转录如下：

| Product 行 | Supported |
|---|---|
| Atlas 350 Accelerator Card | √ |
| Atlas A3 training product / Atlas A3 inference product | √ |
| Atlas A2 training product / Atlas A2 inference product | √ |
| Atlas 200I/500 A2 inference product | √ |
| Atlas inference product | √ |
| Atlas training product | √ |

Note 原文："This API cannot be called for the Atlas 200I/500 A2 inference product in the Ascend RC form."（Ascend RC 形态例外）

**注记**：定向复核确认初审系误读产品列斜杠（B18-C01 CLOSED）：合并行原文包含 training/inference 两个名称，六行 Supported 均为 `√`，两页 SHA 与原抓取一致。产品族声明仍不证明具体 SKU、部署形态或现场调用；RC Note 与目标形态确认继续有效。返回值枚举（HCCS 0x01 / PIX / PHB / SYS / SIO / HCCS_SW 0x40 / PIB 保留不支持）与宏定义照录（适用表之后各节）。

### 图 A-1：800T A2 节点片段（原创示意）

```text
[CPU 鲲鹏920 ×4] ──PCIe 4.0── [8×200GE QSFP RoCE]    有证：主机扩展段（产品页）
[NPU --边 unknown-- CPU/HCCS ?? ]                   unknown：NPU 数量/内存/互联边
[链路类型候选集：HCCS / RoCE / PCIe / UB]            类型分层（HCCL 简介），非本型号拓扑
```

### 图 A-2：Atlas 900 A3 SuperPoD 片段（原创示意，独立于 A-1）

```text
[12×计算柜 + 4×总线设备柜，384 NPU 物理上限]        A3 用户指南组
[L1 总线板 / L2 LingQu 630 7 平面]                   同上（"取决于冗余设计"限定必引）
["理论达到"双向 784GB/s]                            同上（厂商理论口径）
[L2 端口：LingQu 630 V1 48×QSFP-DD-400G]           LingQu 指南 03
```

两片段各自独立，不共用竖线；A-1 的类型候选集不是物理设备，不与 A-2 的柜/板/平面连边。

代际对照（灰色虚线，不可比）：910 代每设备 2×HCCS ring、各 ring 4 处理器、同 ring 可通/跨 ring 不可、单 pod ≤4 NPU 须同 ring；**800T A2 训练服务器与 900 A2 PoD 基本单元不支持 NPU 亲和调度**（[MindCluster 730 亲和原则页](https://www.hiascend.com/document/detail/en/mindcluster/730/clustersched/schedulingug/dl_affinity_0004.html)，肯定句限 910 代，否定句逐字引用）。910 代数字不得填入 A2 任何字段。

| 段 | 路径 | 证据位置 |
|---|---|---|
| 主机扩展 | CPU — PCIe 4.0 — 8×200GE QSFP（RoCE） | 产品页技术规格区 |
| 链路类型候选集 | HCCL 支持 HCCS/RoCE/PCIe/UB 四种高速链路、Ring/Mesh/RHD 算法（A2 支持范围限三款硬件） | [HCCL 简介](https://www.hiascend.com/document/detail/en/CANNCommunityEdition/910/commlib/hcclug/docs/en/user_guide/hccl_intro.md) |
| 软件发现 | `aclrtGetDevicesTopo` 两设备间拓扑枚举（上表适用范围；PIB 保留不支持） | [CANN 900 aclrt API 页](https://www.hiascend.com/doc_center/source/en/CANNCommunityEdition/900/API/runtimeapi/aclcppdevg_03_1895.html)（canonical；`:6066` 镜像字节一致） |
| 超节点 | 12×计算柜 + 4×总线设备柜、384 NPU 物理上限、L1 总线板 / L2 LingQu 630 7 平面、"理论达到"双向 784GB/s | A3 SuperPoD 用户指南组（T01-05 已登记，复用不重取；"取决于冗余设计"限定必引） |
| L2 端口 | LingQu 630 V1 48×QSFP-DD-400G（2×200G）、电源 1+1/风扇 3+1 | [LingQu 630 V1 用户指南 03](https://support.huawei.com/enterprise/zh/doc/EDOC1100463086)（T01-05 已登记；柜级 672×400G 口径并列不合并） |

### 最小路径验证计划 A（待执行，接口条件分支）

- 前提分支：若目标训练节点可调用 `aclrtGetDevicesTopo`（按上表 Note 排除 RC 形态后在目标形态上确认），采集全对矩阵；**若不可调用或返回语义不明，该分支记证据不足、不能执行**，只保留 npu-smi 健康快照（不作拓扑证据）+ HCCL 性能测试工具（既有 CANN 9.1.X 登记）。
- 比较对象：同柜对打 vs 跨柜对打（L1/L2 路径区分）；观察点：HCCL 工具带宽/时延 + 健康快照。
- 通过/失败/无法判断条件与计划 N 同构；800T A2 的 NPU 边缺失时一律记 unknown。不填执行结果。

放置取舍：同 rail/同 ring 共置降跳数 vs 爆炸半径集中；成本以 SU 整配、leaf-spine 预布线为准。

## 来源与更新范围

- NVIDIA（固定机型与代次）：[DGX H100/H200 用户指南](https://docs.nvidia.com/dgx/dgxh100-user-guide/introduction-to-dgxh100.html)、[NVLink 页](https://www.nvidia.com/en-us/data-center/nvlink/)、[Hopper 架构页](https://www.nvidia.com/en-us/data-center/technologies/hopper-architecture/)、[H100 页](https://www.nvidia.com/en-us/data-center/h100/)、[SuperPOD RA 架构](https://docs.nvidia.com/dgx-superpod/reference-architecture-scalable-infrastructure-h100/latest/dgx-superpod-architecture.html)与[网络 fabric](https://docs.nvidia.com/dgx-superpod/reference-architecture-scalable-infrastructure-h100/latest/network-fabrics.html)、[nvidia-smi 手册](https://docs.nvidia.com/deploy/nvidia-smi/index.html)、[NCCL 2.27.5 troubleshooting](https://docs.nvidia.com/deeplearning/nccl/archives/nccl_2275/user-guide/docs/troubleshooting.html)。
- Ascend（各绑定机型/版本）：[800T A2 产品页](https://e.huawei.com/cn/products/computing/ascend/atlas-800t-a2)、[aclrtGetDevicesTopo](https://www.hiascend.com/doc_center/source/en/CANNCommunityEdition/900/API/runtimeapi/aclcppdevg_03_1895.html)（canonical；`:6066` 镜像）、[MindCluster 730 亲和原则](https://www.hiascend.com/document/detail/en/mindcluster/730/clustersched/schedulingug/dl_affinity_0004.html)、[HCCL 简介](https://www.hiascend.com/document/detail/en/CANNCommunityEdition/910/commlib/hcclug/docs/en/user_guide/hccl_intro.md)、A3 SuperPoD 用户指南组与 LingQu 指南（T01-05 登记）。
- 逐条主张与证据定位见[第十八批互联路径来源记录](../../docs/research/batch-18-interconnect-paths-sources.md)。
- 待确认：800T A2 的 NPU 数量/内存/互联边；是否含 HCCS 交换及端口带宽；A3 分档指标；DGX 官方拓扑矢量边清单；NVL72/GB200 代际隔离；两样板作业可用带宽（归 T03-03）；所选训练形态的 aclrt 可调用性（目标形态确认）。
