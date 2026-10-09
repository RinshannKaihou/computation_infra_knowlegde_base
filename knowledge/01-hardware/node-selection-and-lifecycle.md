---
id: hardware.node-selection-and-lifecycle
title: 节点选型、隔离返修、长期管理与退役
type: procedure
domain: hardware
status: draft
platforms: [generic, nvidia, ascend, amd]
source_refs:
  - src.nvidia.dgx-h100-h200-service-manual-2026-10-09
  - src.nvidia.rma-process-deploy-latest-2026-10-09
  - src.nvidia.dgx-os-7-user-guide-reimaging-2026-10-09
  - src.nvidia.nvsm-user-guide-25.03
  - src.nvidia.dgx-superpod-deployment-guide-v16-2024-12-11
  - src.nist.sp-800-88r2-2025-09
  - src.supermicro.sys-821ge-tnhr-manual-mnl-2596-1.0c
  - src.supermicro.as-2124gq-nart-manual-mnl-2356-1.0a
  - src.dell.system-erase-idrac9-poweredge-2020
  - src.dell.kb-000186133-data-wipe-2026-10-09
  - src.huawei.atlas-800t-a2-maintenance-guide-26-2026-10-09
  - src.mlcommons.mlperf-training-results-v6.0-2026-10-09
  - src.usenix.superbench-atc24
  - src.nvidia.gpu-node-triage-2026-10-08
  - src.huawei.mindx-dl-60rc2-ascend-dmi-2026-09-29
  - src.nvidia.dgx-h100-h200-user-guide-2026-01-26
  - src.nvidia.dgx-superpod-dc-design-h100-2026-10-08
updated_at: "2026-10-09"
summary: 把加速计算节点从选型、入库、验收、投产、降额、隔离、返修、回服到退役组织成可审计的状态机；容量与成本比较区分峰值规格与有效能力，长期健康比较要求同身份、同版本与观测窗口，退役数据处置以 NIST SP 800-88 Rev.2 和 OEM 官方说明为准，每次状态变更保留证据与角色记录。
related_ids:
  - hardware.node-acceptance-triage
  - hardware.health-evidence
  - hardware.resource-topology
  - hardware.rack-power-cooling-and-failure-domains
  - hardware.power-thermal-evidence
applicability:
  environment_refs: []
  notes: "尚无环境档案；套用本流程前须先补齐现场资产身份（型号/BOM/固件版本）、软件版本、物理拓扑与授权边界。generic 只表示流程结构可跨平台复用，不表示任何具体命令或步骤在某个 GPU/NPU 平台已验证适用；NVIDIA、昇腾、AMD-OEM 的处置动作分别按其服务手册与维护指南核对。本文不授予执行权限。"
verification:
  status: not_verified
  evidence_refs: []
  notes: "方法层流程，未在真实环境执行或走通一轮完整生命周期；各状态的证据锚点来自对厂商文档、政府规范与论文的来源核对（逐条定位见正文与第十四批来源记录），不构成任何现场已执行的证明。"
---

# 节点选型、隔离返修、长期管理与退役

## 目标与触发条件

本文回答的问题是：**一个加速计算节点从选型到退役，如何形成可审计的状态变更流程**——每次状态迁移由谁发起、依据什么证据、留下什么记录、满足什么判据才能进入下一状态。

触发条件包括：扩容或新购前的选型评估；新节点到货；节点反复出现故障或性能退化需要降额、隔离或返修；维修件返回；设备到达退役时点（资产生命周期结束、换代、介质处置要求触发等）。

两条阅读前提：

- **症状不等于根因。** 本文规定的是状态变更的证据与记录要求，不规定某个故障现象对应哪种处置；错误码到高影响处置动作的入口（Xid/黑匣子/AFID 映射）见[设备健康证据与检测边界](health-evidence.md)，验收分层的诊断细节见[新节点与返修节点验收](node-acceptance-triage.md)，本文只衔接、不重复这两篇。
- **本文是方法流程，不是执行处方。** 文中引用的厂商命令与流程步骤用于说明证据锚点；现场执行任何主动测试、固件操作、介质清除或设备处置，都以现场已有授权、影响范围确认与恢复安排为前提，本文不授予执行权限。

## 适用范围与前置条件

- **平台范围**：状态机结构是 generic 的；具体动作锚点分平台——NVIDIA 侧为 DGX 用户指南/服务手册、NVSM、GPU Node Triage 与 RMA 流程页；昇腾侧为 Atlas 800T A2 维护与服务指南（文档 26）与 ascend-dmi；AMD 侧目前只有 OEM（Supermicro）手册证据，无 AMD 官方生命周期文档，不外推到未取证的型号代际。
- **资产身份**：进入本流程的每个节点必须先建立稳定身份，字段见[计算节点资源与拓扑参考](resource-topology.md)的「节点身份」（`node_id`、厂商、产品型号、机箱/主板版本、BOM 或配置标识）与「物理位置」。身份缺失的节点不进入状态机，只做 `unknown` 登记。
- **验收入口**：「验收」与「回服」两个状态的分层证据与通过/失败纪律，统一复用[新节点与返修节点验收](node-acceptance-triage.md)（规格核对→被动证据→主动诊断→基准验收四层），本文不另立验收标准。
- **现场授权**：DGX H100/H200 官方明示设备「must be installed by NVIDIA partner network personnel or NVIDIA field service engineers. If not performed accordingly, your hardware warranty will be voided」（[DGX H100/H200 用户指南 Quickstart 页 Installation and Configuration](https://docs.nvidia.com/dgx/dgxh100-user-guide/quickstart-basics.html)，2026-01-26）——安装与维修动作的执行主体本身影响保修资格，角色分配时须保留该前提。
- **角色词汇**：本文使用本库自定义的最小角色集（需求/容量负责人、采购与资产管理员、现场工程师、平台运维、维修协调人、安全/数据处置负责人），不照抄任何厂商或标准文本的组织名称。NIST SP 800-88 Rev.2 §4.7 列出的 Program Manager、CIO、Information System Owner、SAISO、Property Management Officer 等是美国联邦语境的职责清单（[SP 800-88 Rev.2](https://csrc.nist.gov/pubs/sp/800/88/r2/final)），引用时映射到本地角色而非照搬。

## 选型与容量/成本比较方法

本节给出以**模型、数据、并行策略、服务 SLO** 为输入的比较方法框架。它不是任何厂商的推荐方法：官方单价、残值与维保价格等 TCO 要素均未取得公开来源，成本侧只能由本库自建框架锚定各环节假设（依据与缺口见取证记录「成本比较方法无官方 TCO 来源」一条），任何假设计算必须显式标注假设值，不得写成已验证配置推荐。

### 第一步：需求转译

把模型规模与精度（决定设备内存下限）、数据与流水线形态（决定主机内存/存储入口压力）、并行策略（决定节点内互联与跨节点带宽需求）、服务 SLO（决定吞吐与尾延迟目标）转译为对节点的约束清单。约束清单只写「需要满足什么」，不写「买什么」。峰值规格（GPU FLOPS、内存带宽、NVLink 速率）只能作为过滤条件，不能作为能力结论——SuperBench 论文明确指出「the end-to-end performance cannot be directly mapped to hardware specifications (e.g., GPU FLOPS, memory bandwidth, NVLink speed)」，且软件栈显著影响效率、没有 ground truth 区分缺陷件与正常件（[SuperBench §2.3，arXiv HTML v2](https://arxiv.org/html/2402.06194v2)，USENIX ATC 2024，2026-10-09 复读）。该结论出自 Azure A100 生产背景，不外推为普适数值阈值。

### 第二步：有效能力测量

候选机型的有效能力用可复现基准而非规格表比较：

- **MLPerf Training**：官方定位是「measures how fast systems can train models to a target quality metric」，以 time-to-train 承载有效能力比较；官方 Benchmarks 表是**跨版本基准索引**，按行给出每个基准的 Latest Version Available（2026-10-09 复核）：DeepSeek v3、GPT-OSS 20B、Llama3.1 8b、Llama3.1 405b、Llama 2 70B（finetuning）、DLRM-dcnv2、FLUX.1 各行为 v6.0；RetinaNet（Object detection light weight，Open Images，34.0% mAP）的最新可用版本为 **v5.1**；表内另有 NLP Llama3.1 8b、GNN R-GAT 等 v5.1 行，BERT-large、Stable Diffusion v2（v5.0）、GPT3、resnet-50（v4.1）、3D U-Net（v4.0）、Mask R-CNN（v3.1）等更老行。不能把该表整体称为「v6.0 基准集」；引用某基准的结果须按该基准的最新可用版本对齐，结果比较只在同版本、同规则下进行。引用结果时注意页面明示「Published results are sometimes modified or invalidated…View Change Log」与「The rules remain the official source of truth」——结果为提交方自测加审计机制，引用单行结果须查 results sheet 与 change log，页面为 JS/Tableau 可变形态，引用须带观察日期（[MLPerf Training 结果页](https://mlcommons.org/benchmarks/training/)，2026-10-09 观察）。本批未抽取具体数值条目。
- **SuperBench 测量纪律**：三层 benchmark 集（端到端代表性负载 / component-wise 微基准 / pattern-wise 微基准），并「leverage third-party tools accredited by hardware vendors」（[同论文 §3.2](https://arxiv.org/html/2402.06194v2)）；测量存在不可消除方差，论文转引 MLPerf 口径约 ±2.5%（稳定视觉类）与 ±5.0%（高方差类），并定义 repeatability 为「N 个不同节点或运行的两两相似度算术均值」（§3.4）。±2.5%/±5.0% 是转引口径，不是实测保证；Table 2 的逐项 benchmark 清单未被 HTML 渲染，本批仍未取得（沿用 batch-12 缺口）。

### 第三步：成本侧预算（供电/散热锚点）

容量成本比较的运营成本侧目前唯一取得的全要素官方输入是 DGX SuperPOD 数据中心设计指南（H100 风冷形态）：DGX H100 连续满载 EAP=EPP=10.2 kW/台；每机柜 1/2/4 台对应 10.2/20.4/40.8 kW；回路冗余定额为每路供电 ≥50% 峰值且任一路负载 ≤50%；散热风量 157 CFM/kW；环境等级 ASHRAE A1（[DGX SuperPOD: Data Center Design Featuring DGX H100，planning 页](https://docs.nvidia.com/dgx-superpod/design-guides/dgx-superpod-data-center-design-h100/latest/planning.html)，latest 可变页，2026-10-08 观察）。这些数值只覆盖 H100 风冷形态，不外推到其他机型；机柜级预算的完整方法（持续/瞬态/冗余口径区分）见[机柜供电、散热预算与共享依赖](rack-power-cooling-and-failure-domains.md)。

假设计算示例（仅演示方法，假设值须就地替换）：若某方案按 4 台/柜部署，单柜连续满载预算 40.8 kW，电价假设为 `P`（元/kWh，本地填写），则单柜年电费量级约为 `40.8 × 8760 × P`。该式不含制冷乘数、折旧、维保与残值——这些要素本库未取得官方来源，比较表中对应列保留 `unknown` 或标注为假设。

### 第四步：有效成本与部署核对

把成本除以有效能力（而非峰值规格）得到可比较的单位成本；有效能力的测量窗口与版本条件按本文「长期健康管理」一节的同身份、同版本、同窗口纪律记录，否则两次测量不可比。集群部署完成后，配置级验证的官方样例是 DGX SuperPOD 部署指南的 bcm-validate-pod——「verify whether all the settings are applied correctly according to the specification」，示例逐项核对 slurm 23.02.7、Ubuntu 22.04 并输出 Passed（[DGX SuperPOD Deployment Guide，Validation 页](https://docs.nvidia.com/dgx-superpod/deployment-guide-dgx-superpod/latest/validation.html)，DG-11251-001 V16，2024-12-11）。注意它是软件配置核对而非性能验收，且文档为 A100/H100 代（Base Command Manager 10.24.11），不能据此宣布 GB200 代或性能层面的验收结论。

**不推荐未验证配置**：本节所有产物（约束清单、有效能力表、成本假设表）以可复核的假设与来源为准；没有来源支撑的配置组合不进入候选清单，也不因「常见配置」而获得豁免。

## 生命周期状态机

节点生命周期定义为九个状态：**采购 → 入库 → 验收 → 投产 → 降额 → 隔离 → 返修 → 回服 → 退役**。状态可以回退（如回服验收失败退回返修），但每次迁移都必须满足退出判据并留下记录。降额是投产的可选子状态（能力降级但仍在服务），不是必经环节；隔离、返修可由投产或降额进入。

| 状态 | 进入条件 | 证据（文档/工具/日志） | 负责角色 | 退出判据 |
|---|---|---|---|---|
| 采购 | 需求转译完成（本文选型节） | 约束清单、有效能力比较表、成本假设表（含假设标注） | 需求/容量负责人、采购与资产管理员 | 采购订单与约束清单一致；差异项书面记录 |
| 入库 | 设备到货 | 交付 BOM、序列号、外观清点；资产身份登记（[节点身份字段](resource-topology.md)）；安装授权确认（DGX 保修前提见前置条件） | 采购与资产管理员、现场工程师 | 资产身份与物理位置登记完成；BOM 与订单差异处理完毕 |
| 验收 | 入库完成 | [新节点与返修节点验收](node-acceptance-triage.md) 四层证据；DGX 官方要求投产前跑 pre-flight stress test（见下） | 现场工程师 | 达到验收文档完成判据第 1 项；失败则转隔离并记录 |
| 投产 | 验收通过 | 投产前基线（nccl-tests 等，见下）；调度系统纳入记录 | 平台运维、现场工程师 | 基线归档；节点在调度侧可分配 |
| 降额 | 出现可容忍退化（部分单元失效但残余能力可用） | 健康计数器与事件窗口记录（[计数器语义](health-evidence.md)）；降额范围与调度可见性变更记录 | 平台运维、现场工程师 | 降额配置生效且残余能力有测量记录；恢复或转隔离时退出 |
| 隔离 | 故障证据达到处置门槛或需保护性退出 | Xid/错误事件原始记录、drain/cordon 动作记录（Xid 动作表见下） | 平台运维 | 节点不可调度且现场确认无残留负载；转返修或回服 |
| 返修 | 隔离完成且判定向厂商/OEM 送修 | field diagnostic 日志、RMA 号、更换件与旧件序列号、维修工单 | 维修协调人、现场工程师 | 修复件返回且随附记录齐全 |
| 回服 | 维修件返回或隔离解除 | 重跑验收四层证据；更换后 `nvsm show health` 复核（见下） | 现场工程师、平台运维 | 同「验收」退出判据 |
| 退役 | 资产生命周期结束或处置要求触发 | 处置决策记录、介质处置证书、资产与拓扑更新记录（见退役节） | 安全/数据处置负责人、采购与资产管理员 | 退役节完成判据全部满足 |

### 验收与投产前证据锚点

DGX H100/H200 官方建议在投产前或维修后运行 pre-flight stress test：「running the pre-flight stress test before putting a system into a production environment or after servicing」，`sudo nvsm stress-test --force` 覆盖 GPU/CPU/内存/存储约 20 分钟；快速健康检查用 `sudo nvsm show health`，全部 Healthy（[DGX H100/H200 用户指南 Quickstart 页](https://docs.nvidia.com/dgx/dgxh100-user-guide/quickstart-basics.html)，2026-01-26）。stress test 通过不等于长期稳定，时长为约数。

投产前基线：用 nccl-tests 的 all_reduce_perf 逐对测试并「record the performance achieved…provide a baseline for future comparisons」；多 rail 拓扑可按 rail 隔离；网络性能随拓扑变化，应与网络厂商确认可达性能（[GPU Node Triage，Network Testing](https://docs.nvidia.com/deploy/gpu-debug-guidelines/gpu-node-triage.html)，latest 可变页，2026-10-09 复读）。基线仅在拓扑/配置不变时可比。

### 隔离与返修证据锚点

**Xid 动作表与 drain/cordon**：[GPU Node Triage](https://docs.nvidia.com/deploy/gpu-debug-guidelines/gpu-node-triage.html)（2026-10-09 复读）给出常见 Xid（13/31/45/48/61/62/63/64/74/79/92/94/95/123）的对应动作（drain/cordon、reset、field diag、报 bug），并明确「Field diagnostic is the authoritative and comprehensive NVIDIA tool…usually required before an RMA」，运行时机须咨询系统厂商。该页只提 dcgmi diag 套件 1–3（未提 level 4），与 DCGM 文档口径差异沿用 batch-12 冲突记录；错误码含义与处置边界以[设备健康证据与检测边界](health-evidence.md)为准，本文不重复映射表。

**DGX 返修闭环**（[DGX H100/H200 Service Manual](https://docs.nvidia.com/dgx/dgxh100-service-manual/introduction.html)，页脚 Last updated 2025-12-09，2026-10-09 观察）：

- 客户可更换部件（CRU）清单：Bezel、锁定电源线、电源模块、风扇模组、前面板、U.2 数据盘、M.2 启动盘、含 2×M.2 的 Riser 组件、ConnectX-7 PCIe 卡（存储网）、50GbE 网卡、DIMM、机柜导轨套件、TPM、电池。清单外部件（如 GPU/NVSwitch 底板）不在客户自换范围，须由 NVIDIA 处理。
- 流程闭环（以 [DIMM Replacement](https://docs.nvidia.com/dgx/dgxh100-service-manual/dimm-replacement.html) 与 [Network Interface Card Replacement](https://docs.nvidia.com/dgx/dgxh100-service-manual/network-card-replacement.html) 两个 14 步流程为实例）：用 `nvsm show health` 定位坏件 → 向 NVIDIA Enterprise Support 取 RMA 号（原文「Contact NVIDIA Enterprise Support to obtain an RMA number for any system or component that needs to be returned for repair or replacement. When replacing a component, use only the replacement supplied to you by NVIDIA.」）→ 更换 → 开机用 nvsm 复核健康/测试网卡 → 「Ship back the failed unit to NVIDIA Enterprise Support using the packaging provided」。手册未给 RMA 时限/SLA；更换后验证仅 nvsm 级，未要求重跑性能基线——本流程要求回服仍按验收文档补齐基准层。

**NVIDIA RMA legacy 页（标注陈旧性）**：[NVIDIA RMA Process](https://docs.nvidia.com/deploy/rma-process/index.html)（无版本/日期，2026-10-09 观察）要求 RMA Checklist 附 `nvidia-bug-report.log.gz` 与 `fieldiag.log`，缺日志「may result in delays」；提交前须先排除系统级原因（辅助供电线、重插、换好卡交叉验证、跨机验证）；ECC 限定「NVIDIA will not accept RMA requests for failures that occur only with ECC disabled」；提交入口 portal.nvidia.com。该页为 Tesla 时代内容（nvidia-healthmon、DU-05711-001/DU-05363-001 文档号），与现行 DGX Enterprise Support 流程的关系未证实，引用时须标注其陈旧性。

**昇腾返修锚点**（Atlas 800T A2 [维护与服务指南](https://support.huawei.com/enterprise/zh/doc/EDOC1100317204)，文档 26，2026-09-18，2026-10-09 观察）：覆盖拆卸与安装、上电、下电和故障处理，面向华为/渠道/企业管理员。[NPU 模组更换页](https://support.huawei.com/enterprise/zh/doc/EDOC1100317204/47be00cc)要求更换前记录固件版本（iBMC「系统管理>系统信息>其他>HiAM」查 MCU/CPLD、「处理器>NPU」查 NPU 固件；无 OS 时需找部署/升级人员确认版本）、下电、防静电、至少四人抬机。文档 23 修改记录起「NPU载板及其组件 章节增加检查更换后NPU模组的HCCS链路状态步骤」（更换后验证锚点）；文档 12 修改记录起主板/NPU 模组章节增加 SSL 证书相关说明（更换涉及凭据处置，正文内容本批未取）。该指南是工程师更换操作手册，不含客户侧 RMA 物流/SLA 流程——华为侧返修主要靠服务合同，介质/故障件保留条款本批未取得（见已知缺口）。

**Supermicro（OEM）锚点**：

- Intel 侧（SYS-821GE-TNHR，[手册 MNL-2596 Rev 1.0c](https://www.supermicro.com/manuals/superserver/8U/MNL-2596.pdf)，2024-01-05）§7.10「Returning Merchandise for Service」：保修服务需购买凭证（发票/收据）；向 vendor 获取 RMA 号并标示于包装箱外，预付邮资或自送；可在线申请（supermicro.com/support/rma/）；保修仅覆盖正常使用，不覆盖改装/误用/滥用/不当维护；报障需提供系统/主板/机箱型号与 PCB 版本、BIOS 日期/版本、系统配置。「normal consumer use」措辞与数据中心场景的张力如实保留。
- AMD 侧（AS-2124GQ-NART/NART+，[手册 MNL-2356 Rev 1.0a](https://www.supermicro.com/manuals/superserver/2U/MNL-2356.pdf)，2021-05-11）「Replacing GPUs」：「Individual GPU and GPU baseboards are recommended to be serviced by Supermicro」，且「Prior to submitting an RMA for GPUs, Nvidia requires that their Field Diagnostic tool is first run to isolate hardware failures and obtain a log file for review」（引用 NVIDIA 文档 DU-09163-001 Baseboard Field Diagnostics Software Guide）。这是 A100 代手册：GPU 由 OEM 集中维修而非用户自换，并与 NVIDIA triage 页「RMA 前通常要求 field diag」相互印证；不外推到 MI300 代。

**修理流转参考（非官方标准）**：SuperBench 建议 repair system 维护 defective buffer（OFR，out for repair）与 hot buffer（修复好的健康节点），运行时将新坏节点与 hot buffer 节点置换交还编排系统（[SuperBench §3.1 Workflow 第 7 步](https://arxiv.org/html/2402.06194v2)）。这是 Azure 单一厂商生产实践描述，不是行业通用流程，只作设计参考。

昇腾侧主动诊断/压测的业务影响与前提（root/特权容器、互斥项、`-st` 60–604800 秒压测时长等）见 [ascend-dmi 故障诊断页（MindX DL 6.0.RC2）](https://www.hiascend.com/doc_center/source/zh/mindx-dl/60rc2/toolbox/ascenddmi/toolboxug_0020.html)与[验收文档步骤 4](node-acceptance-triage.md)，本文不重复参数表；PRBS PASS/FAIL 内部冲突等未解决项维持原记录。

## 长期健康管理

长期健康比较的三条纪律——**同身份、同版本、同观测窗口**——均有官方来源支撑：

- **同版本**（SuperBench §5.1 Setup）：验证环境与生产完全一致——「The environment for validation uses the exact same settings as production clusters, including firmware versions, hypervisor settings, BIOS configurations, etc. We fixed all software versions by using a dedicated VHD image for VM and a Docker image for validation execution」。固件/驱动更新后须重调重估：「After firmware/driver updates, re-tune and re-evaluate the repeatability in case it deteriorates on newer versions」（§3.4）；集群级固件/软件升级本身是触发再验证的事件（§3.1）。版本变更使旧基线不可比，这是「同版本比较」的直接依据。
- **同身份与观测窗口**（SuperBench §3.1/§5.2）：原则是「Quick but frequent validations. Proactive validation should not be an one-time effort. Each node should be validated quickly but frequently in line with incident probability estimations to guarantee enduring reliability」；Selector 用节点 total up time、historical incident count、各类型 MTBI 预测下次事故时间（TBNI）；验证分事件触发（节点加入/作业分配/事故后 cordon-drain）与定期两类。按节点身份纵向追踪 up time/事故史/MTBI，即「同身份观测」；没有同一观测窗口的两个测量值不做直接比较。
- **计数器与窗口语义**：计数器生命周期、累计/窗口口径、重启断点与「零值≠无事件」的记录规则见[设备健康证据与检测边界](health-evidence.md)；供电散热侧的降频与 violation 计数见[供电、散热与性能退化证据](power-thermal-evidence.md)。本文不重复字段表。

NVIDIA 侧的长期监控组件为 NVSM（[NVSM User Guide Release 25.03](https://docs.nvidia.com/datacenter/nvsm/nvsm-user-guide/latest/nvsm-user-guide.pdf)，PDF 署期 2026-07-13，2026-10-09 抽取核对 §1/§1.1）：「NVSM is an "always-on" health monitoring engine which catches issues proactively」；健康告警落持久存储并可邮件通知，状态分 critical/warning/cleared；提供 Prometheus exporter 供外部拉取关键系统指标（支撑长期趋势）；按需健康检查「reports deviations from expected results」；call-home 可自动开支持工单；「Always on」不支持 DGX Station。覆盖 DGX/CGX/RTX 服务器；latest PDF 链接可变，引用带署期。

长期管理进入本状态机的接口：任一监控/复核发现达到处置门槛的证据，按「隔离」状态入口处理；固件/驱动/拓扑变更后，投产基线作废，按「验收」层补测后才能继续使用旧基线做退化判断。

## 退役流程

退役是状态机的终态，包含五个缺一不可的环节：调度退出、数据/凭据处置、资产与拓扑关系更新、处置记录、完成判据。现场执行依已有授权；产品级退役安全步骤取自 OEM 官方说明（本批仅 Dell 一条完整证据，见已知缺口）。

### 调度退出

节点 drain（驱逐负载、标记不可调度）属于集群平台职责，本文只定义硬件侧衔接：进入退役流程前，节点须经平台侧完成 drain 并确认无残留负载；该流程在 05 领域（[集群平台与资源管理](../05-cluster-platform/index.md)）承载，其「节点上下线、升级、发布与变更」主题当前标注待建设——本库尚无调度侧退出流程正文，衔接动作的现场证据（drain 记录、残留负载确认）按本文状态表要求先行保留。

### 数据/凭据处置（NIST SP 800-88 Rev.2）

**版本事实**：任务书原指定的 NIST SP 800-88 Rev.1（2014-12）已于 2025-09-26 被 NIST 撤回（Withdrawn），由 Rev.2（2025-09 final，DOI 10.6028/NIST.SP.800-88r2）整体取代；本节以 Rev.2 为准（[CSRC 页面](https://csrc.nist.gov/pubs/sp/800/88/r2/final)、[PDF](https://nvlpubs.nist.gov/nistpubs/SpecialPublications/NIST.SP.800-88r2.pdf)，2026-10-09 逐节核对）。Rev.2 为美国政府作品，「not subject to copyright in the United States」，引用署名 NIST。

- **三级方法定义**（§3.1.1–3.1.3）：Clear = 逻辑技术清除全部用户可寻址位置、防简单非侵入恢复（覆写或恢复出厂）；Purge = 物理或逻辑技术使目标数据用 state-of-the-art 实验室技术不可恢复且介质可复用（应优先于 Clear）；Destroy = 使恢复不可行且介质不可再用于存储（Disintegrate/Incinerate/Melt/Pulverize/Shred；打洞/弯折等只算部分损坏）。Rev.2 明确：SSD 等有过剩预留的闪存「multiple overwrite passes…should be avoided as very little confidentiality protection is achieved」；去磁对非磁性介质不适用，且现不被视为批准的 destroy 技术。
- **密码学擦除（CE）**（§3.2）：CE 是 purge 技术，通过清除加密密钥实现快速清除；联邦机构须用 FIPS-140 验证的加密模块（SED）；CE 依赖加密实现质量、密钥清除与可追溯性（§3.2.1–3.2.5）；对云/虚拟化逻辑存储，CE 可能是唯一可行的 purge 选项。CE 有效性依赖厂商实现，规范要求向 ISM 厂商索取 sanitize 命令实现与验证信息（Appendix B）。
- **介质控制权**（§4.3）：§4.3.3——不复用时最简单经济的是 destroy；§4.3.4——**保修换件、折抵等不返还的介质视为脱离组织控制**（交给维护商需有保密合同才算仍在组织控制下），这直接支撑「RMA 前完成数据处置」的要求；§4.3.6——决策须记录并保证流程与资源；§4.4——执行应符合 IEEE 2883 或组织认可标准；Fig.1 给出决策流。
- **验证（Verification）与确认（Validation）分离**（§4.5）：§4.5.1 验证 = 检查清除动作完成状态（破坏性方法查残骸与设备；非破坏性查工具完成状态/错误/介质健康；除组织策略要求外不需要对清除后介质做精细抽样）；§4.5.2 确认 = 判定目标数据是否有效清除，不合格则换技术重清或升级到更安全方法。规范给出的反例：SSD 去磁「completed successfully, but no sensitive data is sanitized」——**工具报告成功不等于数据已清除**，两个阶段分开记录。
- **处置证书**（§4.6、Appendix C）：每个被清除介质应完成 Certificate of Sanitization，至少记录 Manufacturer/Model/Serial number/资产编号/介质类型/介质来源/（可选）原密级/Sanitization method（Clear/Purge/Destroy）/technique（degauss、overwrite、block erase、CE）/工具及版本/Verification method/执行与验证人员（姓名、职务、日期、地点、联系方式、签名）；附录 C 样表含去向勾选（Internal Reuse/External Reuse/Recycling Facility/Manufacturer/Other）；清除后应去除介质上原密级标记。全生命周期介质台账缺口会使记录只能证明「这些介质清过」而非「所有介质都清了」——入库时未登记的介质在退役时无法被证明已处置。

**OEM 官方退役/擦除说明**：

- **DGX OS 7 重镜像**（[DGX OS 7 User Guide — Reimaging the System](https://docs.nvidia.com/dgx/dgx-os-7-user-guide/reimaging.html)，2026-10-09 复核 Boot Options 节；示例 ISO DGXOS-7.6.0-2026-08-27）：页首 Caution 为重镜像「erases all data stored on the OS drives」（含 /home），需保留的文件应先移到 `/raid` 并选择保留选项安装。GRUB 菜单有两个分支，数据破坏范围不同：**默认的「Install DGX OS \<version\>」分支会重新分区全部驱动器（OS 盘与数据盘），数据盘被配置为 RAID 阵列挂载 `/raid`，该过程覆写 OS 与数据盘上的全部数据和文件系统**；只有显式选择「Install DGX OS \<version\>: Without Reformatting Data RAID (does not mount /raid)」分支才保留数据盘（安装 cache daemon 但默认禁用、`/etc/fstab` 中注释 `/raid` 条目、不格式化 RAID 盘）。重镜像不改变 MIG 设置与数据盘加密等持久硬件配置；ISO 需 Enterprise Support 账号下载；另可选 Encrypted Root 安装。边界必须写清：重镜像是安装/恢复动作，**该文档未作任何 sanitization 合规声明**，不应对其赋予 NIST 的 Clear/Purge 等级——按 §4.5 的验证/确认框架，重装或重格式化本身不构成清除等级证据；数据盘是否被覆写取决于上述显式分支选择，「跑了重镜像」既不能证明数据已处置，也不能证明数据被保留。DGX 整机退役/处置的专门官方文档本批未取得（见已知缺口）。
- **Dell System Erase**（iDRAC9，PowerEdge，[技术说明](https://dl.dell.com/manuals/common/dell-emc-system-erase-poweredge-idrac9.pdf)，©2020，面向 14G）：用于 repurposing 或 retiring，「erasing data from server storage devices and server non-volatile stores such as caches and logs」；覆盖 HDD/SED/ISE/NVMe/NVDIMM/BOSS；ISE/SED/NVMe/NVDIMM 用 cryptographic erase，非 ISE 的 SATA HDD 用覆写；入口为 Redfish / Lifecycle Controller GUI（F10）/ RACADM CLI。如实记录两处限制：其方法映射基于旧版 NIST 800-88r1 时代；页脚带「Internal Use - Confidential」字样但文档公网可取（矛盾标记）。15G/16G 现行文档未逐份核对。
- **Dell Data Wipe 命令-方法映射**（[KB 000186133](https://www.dell.com/support/kbdoc/en-us/000186133/dell-data-wipe-nist-800-88r1-supported-hard-drive-sanitize-actions)，2026-10-09 观察）：按介质发不同 sanitize 命令，结果为 Purge 或 Clear（NVMe SSD/SED→Sanitize→Purge；ATA SSD→Sanitize→Purge；ATA HDD→Enhanced Security Erase→Purge；eMMC→Erase+Sanitize→Clear）；并明示「The BIOS is only issuing the command, and not directly telling the storage media how to perform the command. The BIOS does not control the storage media behavior once the wipe commands are issued」——与 NIST Rev.2 §4.5.2 的反例一致：发命令≠控制实现。注意该 KB 的 Affected Products 全为消费/商用客户端（Alienware/OptiPlex/Latitude 等），**非 PowerEdge 服务器**；服务器侧以 System Erase 为准。
- **凭据处置**：昇腾侧主板/NPU 模组更换涉及 SSL 证书的说明（文档 12 修改记录）属于维修场景的凭据证据锚点；退役场景的整机凭据清单（BMC 账户、证书、许可证、管理面权限）本批未取得平台级官方清单，按处置决策记录要求逐项列出并保留处置证据，未覆盖项写 `unknown`。注意 NIST Rev.2 §4.6 的介质清除证书只证明介质处置，不能单独证明 BMC 账户、证书或其他管理面权限已经撤销——凭据处置是独立的关闭项（见完成判据第 6 项），不编造 OEM 命令或未取得的许可证政策。

### 资产与拓扑关系更新

退役完成前，按[计算节点资源与拓扑参考](resource-topology.md)的字段更新资产与拓扑记录：节点身份标记为已退役（保留 ID 与历史，不删除档案）；物理位置、故障域成员关系、共享上游成员清单同步移除该节点；与之关联的机柜供电/散热预算（[机柜供电、散热预算与共享依赖](rack-power-cooling-and-failure-domains.md)）在节点下架后重算。退役节点曾是其他节点共享故障域成员时，更新记录须注明变化日期与依据。

### 处置记录与完成判据

退役完成判据（全部满足才可关闭状态）：

1. 调度退出证据齐全（drain 记录、无残留负载确认）；
2. 每块介质有一份符合 NIST Rev.2 §4.6 字段要求的处置证书，介质清单与入库资产登记可对账；无法对账的介质差异保留为未关闭问题；
3. 处置决策（§4.3 复用/销毁/失控判定）与执行符合性（§4.4 标准）有记录，验证与确认两阶段结果分开记录；
4. 资产与拓扑记录更新完成；
5. 执行与验证人员、日期、地点、签名齐全（映射 NIST 证书字段与 §4.7 角色分工到本地角色）；
6. **凭据处置关闭项**：BMC 账户、证书、管理面权限（含远程管理入口、API 令牌、许可证绑定）已逐项列出清单，每项登记处置方式（撤销/轮换/保留并记录理由）、责任人与证据；存在未解决凭据项时不得正常关闭——要么完成处置，要么进入**明确授权、可审计的残余风险接受流程**（记录授权人、接受范围、期限与复审点），不能仅留下 `unknown` 后关闭。

## 停止条件与恢复安排

- 任何主动测试、固件操作、重镜像或介质清除动作，执行前须现场确认授权、影响范围与回退安排；本文为方法框架，不授予执行权限。
- 证据不足时保留 `unknown` 并记录缺失项，不做处置决定：无基线时不判退化、无介质台账时不宣告处置完成、更换后复核未跑时不回服。
- 重镜像与介质清除不可撤销：执行前确认数据备份与介质去向决策已记录；DGX OS 7 重镜像的**默认安装分支会重新分区并重格式化 OS 与数据盘**，只有显式选择「Without Reformatting Data RAID」分支才保留数据盘——擦除范围是显式分支选择的结果，选择时须显式确认；「跑了重镜像」既不能当作「数据已处置」的证据（重镜像文档无 sanitization 合规声明），也不能当作「数据盘已保留」的证据。
- 介质无法按要求级别清除（工具不支持、CE 依赖的加密实现不可证实、介质故障无法响应命令）时停止并升级到处置决策（如改判 Destroy），不得降低处置级别后放行。
- 返修中等待厂商响应期间，节点保持隔离状态与证据保全；旧件寄出前确认介质处置决策已按 §4.3.4 完成（保修换件不返还 = 介质脱离组织控制）。
- 回服验收失败时退回返修或重新隔离，不降级通过；恢复安排以进入隔离/返修时记录的现场状态为准。

## 完成判据与已知缺口

本文层面可接受的完成判据：状态机每个状态的进入/退出都有可审计记录（证据、角色、时间、判据），缺口显式保留而不是被默认填补。当前已知缺口（如实呈现，未关闭）：

1. **OEM 特定整机退役步骤只有 Dell 一条完整证据**（System Erase，2020，14G，且方法映射基于旧版 NIST）；NVIDIA 侧无 DGX 整机退役/处置专门文档（DGX OS 7 重镜像默认安装分支会重分区并重格式化 OS 与数据盘，另有显式的「Without Reformatting Data RAID」保留分支；文档明示不动 MIG 设置与数据盘加密，且未作任何 sanitization 合规声明——重镜像不是介质处置证据）；Supermicro 手册无数据擦除章节（只有 RMA 物流与保修限定）。
2. **华为保修介质/故障件保留条款未取得**：保修概览页（ENEWS1000008538，V2.24，2026-08-29）正文为 PDF 附件，本批仅见搜索片段级证据（介质保留服务、已消磁硬盘不予更换等），未登记为来源，引用前必须取得 PDF 原文复核。
3. **AMD 官方生命周期/RMA 文档未取得**：AMD 侧证据只有 Supermicro AMD EPYC 平台手册（MNL-2356，A100 代）与 SuperBench 测试床（MI250X），不外推到 MI300 代。
4. **官方 TCO/单价/残值/维保价格缺失**：成本比较为本库自建方法框架，各环节假设须锚定来源或显式标注为假设。
5. **SuperBench Table 2 逐项 benchmark 清单未取得**（HTML 未渲染，沿用 batch-12 缺口）；±2.5%/±5.0% 方差为转引口径。
6. **SuperPOD 验证仅配置级且为 A100/H100 代**（V16，2024-12-11，BCM 10.24.11）：bcm-validate-pod 核对软件配置，不含性能验收；GB200 代对应文档未取。
7. **NVIDIA RMA 流程页陈旧**（Tesla 时代）：与现行 Enterprise Support 流程的关系未证实。
8. docs.nvidia.com 的 latest 形态页、mlcommons.org 结果页、华为 EDOC 页均为可变内容，引用均须带观察日期；NVSM 以 Release 25.03 PDF 署期为准。

## 来源与验证记录

- [SuperBench（USENIX ATC 2024，arXiv HTML v2）](https://arxiv.org/html/2402.06194v2)（2026-10-09 复读 §2.3/§3.1/§3.2/§3.4/§5.1/§5.2）：规格≠性能、三层 benchmark、repeatability 定义与重调重估、同版本验证环境、quick-but-frequent 原则与 TBNI 追踪、repair system buffer 实践。
- [MLCommons MLPerf Training 结果页](https://mlcommons.org/benchmarks/training/)（2026-10-09 观察并复核 Benchmarks 表）：time-to-train 定位；该表为跨版本基准索引，按行给出 Latest Version Available（DeepSeek v3、GPT-OSS 20B、Llama3.1 8b/405b、Llama 2 70B finetuning、DLRM-dcnv2、FLUX.1 为 v6.0；RetinaNet 为 v5.1；另有 v5.0–v3.1 的更老行）；change log/规则为准声明；未抽取单行数值。
- [DGX H100/H200 用户指南 Quickstart 页](https://docs.nvidia.com/dgx/dgxh100-user-guide/quickstart-basics.html)（2026-01-26，2026-10-09 读取）：pre-flight stress test、安装授权与保修前提、`nvsm show health`。
- [DGX H100/H200 Service Manual](https://docs.nvidia.com/dgx/dgxh100-service-manual/introduction.html)（页脚 Last updated 2025-12-09，2026-10-09 观察）：CRU 清单、RMA 声明；[DIMM Replacement](https://docs.nvidia.com/dgx/dgxh100-service-manual/dimm-replacement.html) 与 [Network Interface Card Replacement](https://docs.nvidia.com/dgx/dgxh100-service-manual/network-card-replacement.html) 各 14 步流程与更换后复核。
- [GPU Node Triage](https://docs.nvidia.com/deploy/gpu-debug-guidelines/gpu-node-triage.html)（latest 可变页，2026-10-09 复读）：Xid 动作表、field diagnostic 的 RMA 地位、nccl-tests 基线与按 rail 隔离。
- [NVIDIA RMA Process](https://docs.nvidia.com/deploy/rma-process/index.html)（无版本/日期，Tesla 时代 legacy，2026-10-09 观察）：RMA Checklist 证据要求、系统级排除、ECC 限定；引用须标注陈旧性。
- [NVSM User Guide Release 25.03](https://docs.nvidia.com/datacenter/nvsm/nvsm-user-guide/latest/nvsm-user-guide.pdf)（PDF 署期 2026-07-13）：always-on 监控、告警持久化与状态、Prometheus exporter、call-home、DGX Station 例外。
- [DGX SuperPOD Deployment Guide V16（2024-12-11）](https://docs.nvidia.com/dgx-superpod/deployment-guide-dgx-superpod/latest/validation.html)：bcm-validate-pod 配置级验证边界；A100/H100 代文档。
- [DGX SuperPOD Data Center Design Featuring DGX H100](https://docs.nvidia.com/dgx-superpod/design-guides/dgx-superpod-data-center-design-h100/latest/planning.html)（latest，2026-10-08 观察，batch-13 已核）：EAP=EPP=10.2 kW/台、机柜功率档、回路冗余定额、157 CFM/kW、ASHRAE A1。
- [DGX OS 7 User Guide — Reimaging the System](https://docs.nvidia.com/dgx/dgx-os-7-user-guide/reimaging.html)（2026-10-09 观察并复核 DGX OS ISO Boot Options 节）：OS 盘擦除 Caution、默认安装分支重分区并重格式化 OS 与数据盘、显式「Without Reformatting Data RAID」保留分支、MIG/加密边界、Encrypted Root；文档无 sanitization 合规声明。
- [NIST SP 800-88 Rev.2](https://csrc.nist.gov/pubs/sp/800/88/r2/final)（[PDF](https://nvlpubs.nist.gov/nistpubs/SpecialPublications/NIST.SP.800-88r2.pdf)，final 2025-09，2026-10-09 逐节核对 §3.1/§3.2/§4.3/§4.4/§4.5/§4.6/§4.7、Appendix B/C）：Clear/Purge/Destroy 定义、CE 前提、介质控制权、验证与确认分离、处置证书字段、角色分工；Rev.1 已于 2025-09-26 撤回。
- [Supermicro SYS-821GE-TNHR 手册 MNL-2596 Rev 1.0c](https://www.supermicro.com/manuals/superserver/8U/MNL-2596.pdf)（2024-01-05，pdftotext 抽取）：§7.9 备件渠道、§7.10 RMA 流程与保修限定。
- [Supermicro AS-2124GQ-NART/NART+ 手册 MNL-2356 Rev 1.0a](https://www.supermicro.com/manuals/superserver/2U/MNL-2356.pdf)（2021-05-11，pdftotext 抽取）：GPU 集中维修、RMA 前 NVIDIA Field Diagnostic 前置（DU-09163-001）；A100 代，不外推。
- [Dell System Erase（iDRAC9，PowerEdge，©2020）](https://dl.dell.com/manuals/common/dell-emc-system-erase-poweredge-idrac9.pdf)：适用场景、介质清单、CE/覆写分工、Redfish/LC GUI/RACADM 入口；方法映射基于旧版 NIST，页脚矛盾标记如实记录。
- [Dell KB 000186133](https://www.dell.com/support/kbdoc/en-us/000186133/dell-data-wipe-nist-800-88r1-supported-hard-drive-sanitize-actions)（2026-10-09 观察）：命令-方法映射、「BIOS 只发命令不控制实现」；Affected Products 为客户端产品线，非服务器。
- [Atlas 800T A2 维护与服务指南（文档 26，2026-09-18）](https://support.huawei.com/enterprise/zh/doc/EDOC1100317204)与 [NPU 模组更换页](https://support.huawei.com/enterprise/zh/doc/EDOC1100317204/47be00cc)（2026-10-09 观察）：更换前固件版本记录、下电/防静电/四人抬机、文档 23 的 HCCS 链路复核、文档 12 的 SSL 证书说明。
- [ascend-dmi 故障诊断（MindX DL 6.0.RC2）](https://www.hiascend.com/doc_center/source/zh/mindx-dl/60rc2/toolbox/ascenddmi/toolboxug_0020.html)（2026-10-09 复读参数表）：诊断/压测项的产品与权限前提、互斥与时长参数。
- 逐条主张—证据定位、候选登记与缺口冲突见[第十四批来源记录：节点选型、隔离返修、长期管理与退役](../../docs/research/batch-14-node-lifecycle-sources.md)。
- 当前验证范围：来源核对；未在真实环境执行任何命令、诊断、基准、重镜像或介质清除，状态机未在任何集群走完一轮。
- 待确认：华为保修介质保留条款 PDF 原文；DGX 整机退役专门文档；AMD 官方生命周期文档；官方 TCO 要素；SuperBench Table 2 逐项清单；GB200 代部署验证文档；Dell 15G/16G 现行 System Erase 文档。
