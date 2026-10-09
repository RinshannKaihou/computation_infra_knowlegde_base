---
id: hardware.node-acceptance-triage
title: 新节点与返修节点验收
type: procedure
domain: hardware
status: draft
platforms: [generic]
source_refs:
  - src.nvidia.dcgm-diagnostics-latest-2026-09-30
  - src.nvidia.dcgm-diag-user-guide-latest-2026-10-08
  - src.nvidia.dcgm-v3.3.9
  - src.usenix.superbench-atc24
  - src.huawei.mindx-dl-60rc2-ascend-dmi-2026-09-29
  - src.huawei.mindx-dl-60rc2-ascend-dmi-display-2026-10-08
  - src.nvidia.gpu-node-triage-2026-10-08
  - src.nvidia.dgx-h100-h200-user-guide-2026-01-26
  - src.nvidia.nvsm-user-guide-25.03
  - src.ocp.server-component-resilience-spec-2023-06-30
  - src.nersc.n10-rfp-trd-v6.0-2024-01-26
updated_at: "2026-10-09"
summary: "把验收分成规格核对、被动证据、主动诊断、基准验收四层，并规定验收环境档案（型号/BOM、部件/固件/OS/驱动/工具身份、实际拓扑、负载、历史与验收目标）与证据接入规则（真实档案登记、脱敏/外置、首次测试、修订后复验与回服确认）；一次通过不声明硬件完全无故障，RMA 资格以厂商 field diagnostics 为准；真实环境档案缺口保持 open，由受授权验证轨道关闭。"
related_ids:
  - hardware.health-evidence
  - hardware.power-thermal-evidence
  - hardware.resource-topology
  - hardware.node-selection-and-lifecycle
  - hardware.bmc-firmware-and-events
  - reliability.evidence-and-hypotheses
  - reliability.silent-errors-and-integrity
applicability:
  environment_refs: []
  notes: "尚无真实验收环境档案（topic 01.6-G3 保持 open）：environment_refs 保持空列表，实际环境 reference 与可追踪证据须由受授权验证轨道（V08）交付后才能填入并关闭该缺口。证据样板为 DCGM latest 文档（2026-09-30/2026-10-08 观察，2026-10-09 复读）与 v3.3.9 固定源码、NVIDIA GPU Node Triage 页（有效地址为 gpu-debug-guidelines 路径）、DGX H100/H200 用户指南、NVSM User Guide Release 25.03；NPU 侧为 MindX DL 6.0.RC2 ascend-dmi 文档（AICore 的产品配套、HDK/CANN/算子包、HOST 内存与重启条件见正文）；环境档案字段方法锚定 OCP Server Component Resilience 规范 External Ver 0.3 与 SuperBench §3.4/§5.1，NERSC-10 RFP 仅作采购语境的公开验收实践参考。目标集群的版本、机型、权限、资源预算与维护窗口需另行固定，本文不授予执行权限。"
verification:
  status: not_verified
  evidence_refs: []
  notes: "方法层流程与档案/证据规范，未在真实环境执行任何诊断、重启、压测或基准。正文技术结论所依据的来源已逐页复读核对（2026-10-09：DCGM 级别-测试表与插件前提、退出码，ascend-dmi 前提条件/表1/表2/约束与限制/表4，NVSM User Guide 25.03 §3.8.4（正文复读取得；第 76 页示例图像内容为编写者 600 DPI OCR 核对记录，独立审阅者未能判读图像、未独立核验），OCP 规范 §7/§8/§9，NERSC-10 TRD §12.0/Appendix A，SuperBench §3.4/§5.1，GPU Node Triage 上报与 Network Testing 节），逐条定位见第十五批来源记录；来源核对不构成任何现场已执行的证明。"
---

# 新节点与返修节点验收

## 目标与触发条件

触发：新节点入网、集群扩容交付、故障维修后回服前，需要回答"这个节点现在能否承担生产负载"。验收结论分四档证据强度递增的层：**规格与配置核对 → 被动证据 → 主动诊断 → 基准验收**。层级之间不能互相替代：一次主动诊断通过不证明无灰色退化，基准达标也不替代故障诊断；每层都要记录自己的证据与边界。

验收结论只对**某一确定环境**成立：四层证据必须挂到一份按统一字段建立的**验收环境档案**上（型号/BOM、部件/固件/OS/驱动/工具身份、实际拓扑、负载、历史与验收目标，见「验收环境档案」节），证据的登记、脱敏/外置、首次测试、修订后复验与回服挂接规则见「证据接入与档案登记」节。本文只交付方法——本库尚无真实验收环境档案（topic 01.6-G3 保持 open），该缺口由后续受授权验证轨道（V08）交付实际环境 reference 与证据后关闭，本文不新增假装真实的空档案。

## 适用范围与前置条件

- 证据样板：DCGM latest 文档（learn 与 user-guide 两种形态页，测试清单口径不一致处已分别注明）、DCGM v3.3.9 固定源码、NVIDIA GPU Node Triage 页（latest，2026-10-09 复读；有效地址为 [gpu-debug-guidelines 路径](https://docs.nvidia.com/deploy/gpu-debug-guidelines/gpu-node-triage.html)，早期引用的 `https://docs.nvidia.com/deploy/gpu-node-triage/` 于 2026-10-09 实测返回 404，引用以有效地址为准）、DGX H100/H200 用户指南（2026-01-26）、NVSM User Guide Release 25.03（PDF 署期 2026-07-13）、MindX DL 6.0.RC2 ascend-dmi 文档、SuperBench 论文（USENIX ATC 2024）。
- 方法层来源：验收环境档案字段锚定 OCP Server Component Resilience 规范 External Ver 0.3（§7/§8/§9，见「验收环境档案」节）与 SuperBench §3.4/§5.1；公开验收流程实践参考为 NERSC-10 RFP 技术需求文档 v6.0 的 §12.0 与 Appendix A Sample ATP（美国国家实验室采购样板语境，不是本库执行标准，见「通过、失败与无法判断的判定纪律」节）。跨厂商、面向数据中心现场验收的 burn-in 执行指南（时长、负载曲线、判据）无公开权威文档，NVIDIA 工厂测试（L10 级）内容不公开——本文不编写无来源的 burn-in 处方。
- 权限与现场前提：主动诊断前把节点移出服务（drain 应用、与调度器协调）；DCGM 诊断默认降权到非特权 service account 执行，存在 `DCGM_ST_REQUIRES_ROOT`（退出码 227）等权限失败形态（[user-guide 页 Exit Codes 与 Pulse Test 注意事项](https://docs.nvidia.com/datacenter/dcgm/latest/user-guide/dcgm-diagnostics.html)）；ascend-dmi 的 aicore/prbs 等项要求 root 与特权容器（见步骤 4）。
- ascend-dmi 软件前提：该页列出 Atlas A2 训练系列配套的 HDK 23.0.0 及以后版本的 MCU/驱动/固件，以及 CANN 7.0.0 及以后版本的 Ascend-cann-toolkit、配套 Ascend-cann-kernels 和环境变量配置；network 诊断前需在 Host 侧以 root 配置 RoCE 网卡 IP 地址和子网掩码，再配置网络检测对象 IP，否则可能导致诊断失败（[ascend-dmi 前提条件](https://www.hiascend.com/doc_center/source/zh/mindx-dl/60rc2/toolbox/ascenddmi/toolboxug_0020.html)，2026-10-09 经桌面浏览器渲染复读取得）。这是页面所列前提，不是一套已验证兼容矩阵；目标产品的软件配套仍须核对。
- **缺口声明**：ascend-dmi 页提供单项诊断/压测耗时表，尚未取得 DCGM r1–r4 式级别化套件和对应错误严重度/分类处置枚举；两工具覆盖差异未证实，不声明等价。多节点诊断（dcgmi mndiag）与各 SKU 具体阈值未核对。NVSM stress test 的 DURATION 单位与 `--force` 语义在 Release 25.03 正文与示例图像中均未明示（`--no-prompt` 对确认提示的作用取自示例图像，属编写者核对记录、独立审阅者未能判读图像未独立核验，见「验收测试工具前提汇总」）；当前具体机型的 NIC 压测支持保持 unknown。

## 验收环境档案

验收环境档案是四层证据的挂载点：没有档案，诊断输出和基准数值只是一次匿名运行，无法复验、无法纵向比较、也无法支撑回服决定。档案在首次测试前建立，每次复验更新版本/拓扑/历史面。字段命名直接复用本库既有的资产、拓扑与固件身份字段，不另起一套：

| 档案面 | 建议字段 | 对齐与来源锚点 | 缺失时处理 |
|---|---|---|---|
| 资产身份（型号/BOM） | `node_id`、厂商、产品型号、机箱/主板版本、BOM 或配置标识；物理位置（机房、机架、机位、机箱/托盘、供电分组） | 字段复用[计算节点资源与拓扑参考](resource-topology.md)的「节点身份」与「物理位置」行：产品型号与具体配置分开，保留来源日期或文档版本 | 身份缺失的节点只做 `unknown` 登记、不进入验收流程（同[生命周期状态机](node-selection-and-lifecycle.md)入库退出判据） |
| 部件身份 | 加速器/NIC/本地存储的物理槽位或板内位置、设备/芯片 ID、序列号范围、分区父子关系；介质/盘 ID | 复用 resource-topology.md「加速器」「NIC/端口」「本地存储」行 | 型号已知但 BOM/序列号未知时，不套用可选部件数量，保持 `unknown` |
| 固件身份 | `Id`/`SoftwareId`、`Version`（及 `AdditionalVersions`）、`LowestSupportedVersion`、`Updateable`、`WriteProtected`、`RelatedItem`（固件作用的设备身份）、来源文档与机型/修订、采集时间 | 复用[BMC、固件身份与跨层硬件事件](bmc-firmware-and-events.md)的固件身份清单字段（对齐 Redfish SoftwareInventory 模型）；清单是文档或某次查询的快照，不是稳定事实；三平台回退机制（iBMC 三分区/Supermicro 四镜像/NVIDIA 双分区）分列记录，不合并叙述 | 未取得清单时固件面记 `unknown`，不凭工具banner或经验值补全 |
| 软件身份（OS/驱动/库） | OS 版本与 OS 级调整（是否需 admin/root、`/sys` 或 `/proc/sys` 变更）、依赖库、驱动版本；可公开时的关联 kernel 与 firmware 版本 | OCP 规范 §7 software environment selection（建议实践为 VM 镜像、容器或 Dockerfile 加 host）与 §8「Associated kernel and firmware versions」；SuperBench §5.1 用专用 VHD（Ubuntu 22.04 基）与 Docker（NGC 20.12 基）镜像固定全部软件版本的实践参考 | 版本未固定的测试结果只挂到本次运行，不进基线、不做纵向比较 |
| 工具身份 | 工具/套件名、命令行参数、版本号甚至构建信息（编译器、静态/动态链接） | OCP 规范 §7 Tool configuration，目的原文「to provide the entity executing the testing the necessary information on what to run to ensure proper reproduction」 | 版本未固定的工具输出不作为复验可比证据 |
| 实际拓扑 | 端口↔PCI↔设备映射、节点内互联边、共享上游、故障域成员 | 复用 resource-topology.md 拓扑字段与 `documented`/`observed`/`allocated` 三分列原则；文档拓扑不证明现场可达 | 未确认的共享关系只作待验证假设；缺证据写 `unknown` |
| 负载 | 验收所用负载清单（诊断套件级别、压测项、基准与输入）、时长与重复次数、期望运行时长 | OCP 规范 §7 Desired run-time（保证数据采集充分）；§8 要求记录所有失败测试名与每芯片测试时长、time-to-failure 与跨迭代复现率（示例下限 10 次迭代） | 无负载定义的诊断结论不可复现，只作一次性观测 |
| 历史 | 事故记录、维修/更换记录、固件变更记录、服役时长 | OCP 规范 §9 part history（age at first failure、T=0 或 t>0 退化、厂商诊断细节——规范自述可能需 NDA 才提供）；本库档案按自有运维记录填写，不依赖厂商 NDA 数据 | 历史缺失保持 `unknown`，不从零假设"无历史" |
| 验收目标 | 本节点要承担的负载类型与性能门槛、通过判据、期望运行时长 | DCGM 设计目标第 1 条「Provide a system-level tool, in production environments, to assess cluster readiness levels before a workload is deployed」（[user-guide 页 Goals](https://docs.nvidia.com/datacenter/dcgm/latest/user-guide/dcgm-diagnostics.html)）；网络性能目标须与网络厂商确认——「Coordinate with your network vendor/architect to help understand what performance should be achievable」（[GPU Node Triage Network Testing](https://docs.nvidia.com/deploy/gpu-debug-guidelines/gpu-node-triage.html)） | 无目标时不做通过/失败结论，只记录测量值 |

上述字段结构的行业锚点是 OCP Server Component Resilience Workstream《Server Component Resilience》External Ver 0.3（2023-06-30，[OCP 文档页](https://www.opencompute.org/documents/external-ver-0-3open-compute-specification-server-component-resilience-workstream-pdf/)，2026-10-09 打开核对）——目前取得的唯一一份行业多方（贡献者含 Google/Meta/Microsoft/AMD/Intel/ARM/NVIDIA，文档自述 OWFa 1.0.2 许可、附录不受该许可覆盖仅供参考）签署的测试环境档案字段规范：§7 Test Input Specification 规定测试输入档案（工具配置、软件环境、硬件环境含固件版本、期望运行时长），§8 Test Output Specification 规定测试输出档案（设备类型与架构、技术节点、制造期测试、制造后测试——明确含「pre-deployment or datacenter acceptance testing」、测试环境是 bare-metal 还是 VM/容器、可公开时的关联 kernel 与 firmware 版本、time-to-failure、跨迭代复现率、错误检测延迟、示例日志），§9 规定 part history。边界必须写清：该规范面向 SDC（silent data corruption）缺陷件信息共享，**不是验收流程规范**；External Ver 0.3 为早期版本，规范自述完整格式留待后续版本；§9 part history 的厂商诊断细节可能需 NDA。本文只借用其字段结构，不引用其流程与阈值。

## 需要的证据

| 证据 | 采集范围或定位 | 用途 | 缺失时如何处理 |
|---|---|---|---|
| 验收环境档案 | 按「验收环境档案」节字段：首次测试前建立，版本/拓扑/历史面随变更更新 | 全部四层结论的挂载点 | 身份缺失只做 `unknown` 登记；不新增假装真实的空档案；档案未建立时结论只能是 `unknown` |
| 机型规格与拓扑 | 厂商组件表、端口↔PCI↔设备映射、电源冗余行为 | 第 1 层核对基线 | 无规格基线时只做外观与清点，不作符合性结论 |
| 被动健康证据 | 健康 watch、Xid、ECC/错误计数、降频位图与 violation 计数（见[健康证据](health-evidence.md)、[供电散热证据](power-thermal-evidence.md)） | 已知规则的当前状态 | 无事件只覆盖已启用规则与保留样本，不证明无故障 |
| 主动诊断结果 | DCGM diag 级别/单项，ascend-dmi -dg/-s | 受控负载下的故障检出 | 未 drain 或被负载干扰时结果不可信 |
| 基准证据 | nccl-tests 逐对结果与投产前基线；群体判据（SuperBench 方法） | 灰色退化/性能退化检出 | 无基线时只能给单次测量值，不给退化结论 |
| 处置记录 | 退出码、per-test/per-entity 结果、错误 ID/Severity/Category、必要重启/复测及回服决定 | 升级、隔离与回服门槛 | 非零码可能表达诊断检出失败，但不能单独判根因；失败或必需检查未覆盖时不回服（见步骤 6） |

## 步骤与判断分支

| 步骤 | 检查或动作 | 运行影响 | 预期证据与解释 | 下一步 |
|---|---|---|---|---|
| 1 | 规格与配置核对：先按「验收环境档案」一节建立或核对本节点档案（身份缺失只做 `unknown` 登记，登记规则见「证据接入与档案登记」），再以机型文档为基线核对组件数量与拓扑（如 DGX H100：8×H100 640GB、4×NVSwitch 900GB/s、6×3.3kW PSU 4+2、≥3 PSU 才开机且 3 PSU 时降性能运行，[DGX 用户指南](https://docs.nvidia.com/dgx/dgxh100-user-guide/introduction-to-dgxh100.html)，H100/H200 数值分列勿混）；NPU 侧用 ascend-dmi 显示界面核对芯片型号、NPU 数量、PCIe LnkCap/LnkSta、内存容量等（[toolboxug_0019 表2](https://www.hiascend.com/doc_center/source/zh/mindx-dl/60rc2/toolbox/ascenddmi/toolboxug_0019.html)） | 只读 | 配置与规格不一致 → 配置/装机问题，不进诊断层 | 进步骤 2 |
| 2 | 被动证据：健康状态、Xid、ECC 计数、降频位图与 violation 计数（字段语义与窗口边界分别见[健康证据](health-evidence.md)与[供电散热证据](power-thermal-evidence.md)） | 只读 | 有事件/计数 → 按事件处置；无事件 → 只能说明已启用规则在保留窗口内未命中 | 进步骤 3 |
| 3 | GPU 主动诊断（DCGM）：按级别选择——r1 software（就绪检查，Hopper 口径 <2.5 秒）；r2 加 pcie/memory/memory_bandwidth（8 卡 <10.5 分钟）；r3 加 diagnostic/targeted_stress/targeted_power/nvbandwidth/nccl_tests（8 卡 <35 分钟）；r4 加 memtest/pulse（8 卡 <2.25 小时）（[user-guide 页 Run Levels and Tests 表](https://docs.nvidia.com/datacenter/dcgm/latest/user-guide/dcgm-diagnostics.html)，表头注明 Hopper 实测口径，同表另列 4 卡口径 2.5 分钟/10 分钟/45 分钟按序对应 r2/r3/r4；learn 页清单口径不同：含 context_create、不含 nccl_tests/sm_stress）。级别定位：r1 作收工前就绪检查、r2 作失败作业后检查、隔离疑似故障选单项、返修回服前跑管理员级长测（[learn 页 When diagnostics are useful](https://docs.nvidia.com/datacenter/dcgm/latest/learn/modules/dcgm-diagnostics.html)）。前提：先 drain；software/deployment 插件遇其他图形进程判失败；nvbandwidth 遇 MCUTIL>10% 判失败；nccl_tests 限单节点且需预设 DCGM_NCCL_TESTS_BIN_PATH（未设则优雅跳过）。完整前提清单见下文「验收测试工具前提汇总」 | 高：消耗算力/显存/供电/散热，侵入性测试只能在可移出服务的资源上运行 | 失败不一定在目标处理器——官方明示失败可源于 host/权限/库/拓扑/冷却/供电/负载干扰 | 按结果进步骤 5/6 |
| 4 | NPU 主动诊断（昇腾 ascend-dmi，MindX DL 6.0.RC2）：`-dg` 分软件与硬件检查项，bandwidth 覆盖 H2D/D2H/D2D/P2P；`-s` 触发 HBM/AICore 压测，`-st` 是 HBM 的 60–604800 秒参数，`--sc` 是 AICore 的 1–100 次参数；防呆提示与互斥条件按[参数表](https://www.hiascend.com/doc_center/source/zh/mindx-dl/60rc2/toolbox/ascenddmi/toolboxug_0020.html)核对。network/hbm 按各自机型清单（hbm 含 800I A2）；aicore 限 A2 训练/800I A2、root，容器/VM 需特权且不能与其他项同测；prbs 限指定机型、root、物理机/特权容器和 prbs31。先核对上列 HDK/CANN/算子包与 network IP 前提 | 高：AICore 压测需预留 HOST 约 20–40GB；页表1/2给 AICore 一轮诊断 7–20 分钟、压测 15–40 分钟，属文档量级，不是本站耗时保证 | 表1建议上线/巡检执行 3 轮 AICore 诊断并全部通过；任一 EMERGENCY_WARN 转故障处置。诊断完成需重启设备；压测完成需先分析定位再重启（页“约束与限制”），纳入维护窗口。PRBS 状态描述冲突继续保留，不能只凭 PASS/FAIL 名字验收 | 结果归档后进步骤 5/6；必要收尾未完成不恢复服务 |
| 5 | 基准验收（性能退化层）：投产前用 nccl-tests all_reduce_perf 逐对测试并记录性能作基线，多 rail 拓扑可按 rail 隔离（[GPU Node Triage 页 Network Testing](https://docs.nvidia.com/deploy/gpu-debug-guidelines/gpu-node-triage.html)）。判据来源要分清：SuperBench 的方法是**与集群群体判据比**而非与厂商规格比——端到端性能无法直接映射硬件规格、无 ground truth，其在集群 build-out 全集结果上用无监督 CDF 相似度判据（α=0.95、单向距离只判更差、迭代剔除后取中位样本），两阶段执行（单机→多机，阶段间剔除缺陷节点）（[SuperBench §2.3/§3.4/§4/§5.3](https://arxiv.org/html/2402.06194v2)）。单机/小规模验收没有群体判据时，只能依赖本地历史基线或诊断内建阈值（如 targeted_power 达 target_power 75% 判过、targeted_stress 默认达成 95% GFLOPS），二者证据强度不同 | 高：基准占用整机 | 显著低于基线/判据 → 灰色退化嫌疑，回步骤 2/3 定位；达标 → 记录基线入库 | 进步骤 6 |
| 6 | 处置与升级：同时解析退出码与结果本体（per-test/per-entity、Warning、SKIPPED、错误 ID/Severity/Category）。非零码可能表示请求/启动/连接失败，也可能表示已运行的诊断检出失败：226 / `DCGM_ST_NVVS_ERROR` 为诊断执行后报错，205 / `DCGM_ST_NVVS_ISOLATE_ERROR` 表示需隔离（[Exit Codes](https://docs.nvidia.com/datacenter/dcgm/latest/user-guide/dcgm-diagnostics.html#exit-codes)）。ISOLATE/RESET 级按官方建议及时处置，其余作站点分析/重跑/查日志；退出码不单独证明硬件根因，JSON 无稳定 schema。GPU 故障节点按[Xid 动作表](https://docs.nvidia.com/deploy/gpu-debug-guidelines/gpu-node-triage.html)处置；DCGM 不修复故障、不替代 field diagnostics、不判定 RMA 资格 | 结果解析为只读；隔离/reset/重启等处置依已有授权与维护窗口 | 失败、必需检查 skipped 且无替代证据、unknown 均保持节点不可调度并记录下一步；处置、必要重启/复测、验收判据满足后才形成回服决定 | 满足完成判据可结束调查；只有回服门槛满足才恢复服务 |

## 验收测试工具前提汇总

四层流程中各主动测试工具的**环境前提**属于验收环境档案的软件/权限面，执行前逐项核对；任一前提不满足时对应测试证据记为缺失（skipped/未覆盖），不得用相邻测试代替。流程位置分别见步骤 3/4/5。

| 工具/测试 | 前提与约束 | 判据与边界 | 来源定位 |
|---|---|---|---|
| DCGM diag 级别选择 | 级别-耗时（表头注明 measured on Hopper GPU systems）：r1 software <2.5 秒；r2 加 pcie/memory/memory_bandwidth，8 卡 <10.5 分钟；r3 加 diagnostic/targeted_stress/targeted_power/nvbandwidth/nccl_tests，8 卡 <35 分钟；r4 加 memtest/pulse，8 卡 <2.25 小时；同表另列 4 卡口径 2.5 分钟/10 分钟/45 分钟（按表序对应 r2/r3/r4）。其他 GPU 数/型号耗时未给 | 耗时为 Hopper 实测口径，不作本站或他机型保证；GPU Node Triage 页只提套件 1–3（long 约 30 分钟），与 DCGM 文档 r4 的口径差异沿用既有冲突记录；learn 页与 user-guide 页测试清单口径不一致（步骤 3 已注明） | [user-guide 页 Run Levels and Tests 表](https://docs.nvidia.com/datacenter/dcgm/latest/user-guide/dcgm-diagnostics.html) |
| DCGM deployment 插件 | Preconditions：`LD_LIBRARY_PATH` 须含 CUDA 库路径（如 `/usr/local/cuda-X.Y/lib64`）；nouveau 驱动不得运行（应 blacklist）。Failure 条件：设备节点被 cgroup 阻挡或无读写权限、NVML 库无法加载、CUDA 运行时库无法加载、nouveau 已加载、存在 pending page retirements、存在 pending/failed row remaps、目标 GPU 上有其他图形进程 | 这些前提失败属于环境/配置问题而非加速器硬件故障；排查顺序先环境后硬件 | [user-guide 页 Deployment Plugin Preconditions/Failure](https://docs.nvidia.com/datacenter/dcgm/latest/user-guide/dcgm-diagnostics.html) |
| DCGM nccl_tests 插件 | libnccl.so 与 nccl-tests 均不随 DCGM 分发，须单独安装/构建且需 CUDA toolkit；限单节点——「does not require MPI support. Multi-node NCCL tests are not currently supported」；须预设 `DCGM_NCCL_TESTS_BIN_PATH`（host engine 环境读取，非调用 shell）；root 运行时对 nccl 测试二进制有 owner/权限安全检查 | 未设路径时该测试优雅跳过——跳过不是通过，该层证据缺失须记录；多节点 NCCL 验收走步骤 5 的 nccl-tests 基线路径 | [user-guide 页 NCCL Tests Plugin Prerequisites](https://docs.nvidia.com/datacenter/dcgm/latest/user-guide/dcgm-diagnostics.html) |
| DCGM nvbandwidth | 「The test will fail if current memory copy utilization (MCUTIL) is over 10% or cannot be retrieved」 | 失败可能源于并发拷贝负载干扰而非硬件；执行前确认节点已 drain | [user-guide 页 NVBandwidth Failure Conditions](https://docs.nvidia.com/datacenter/dcgm/latest/user-guide/dcgm-diagnostics.html) |
| NVSM stress test（Release 25.03） | `sudo` 执行；语法 `sudo nvsm stress-test [--usage] [--force] [--no-prompt] [<test>...] [DURATION]`，示例 `sudo nvsm stress-test 60 --force`。**§3.8.4 正文泛述**：「NVSM supports functionality to simultaneously stress various components (GPU, PCIe, DIMMs, Storage Drives, CPUs, Network Cards) of the system with large workloads」，结束给出每组件 pass/fail 汇总，期间监控各项系统指标。**示例中的机型限定（印刷页 70 / PDF 第 76 页示例截图）**——**证据链边界：以下三项图像内容（NIC 机型限定与非支持平台结果说明、`--no-prompt` 提示作用、示例结果表 NIC=SKIPPED）均为编写者对官方 PDF 图像页的核对记录（2026-10-09 经 600 DPI 渲染 OCR），独立审阅者会话图像调用失败、未能判读该页图像，未独立核验**；PDF URL 与页码（第 76 页/印刷页 70）保留以便后续独立复核：NIC（network interface card）压测「is only available on DGX-1, DGX-2, and Luna Systems」，非支持平台「results for this component will be blank」；示例结果表 GPU/CPU/Memory/Storage/PCIE 均 PASS、NIC 为 SKIPPED。示例限定不等于当前全部机型的支持矩阵——**当前具体机型的 NIC 压测支持保持 unknown**，相邻 DGX H100/H200 quickstart 页不能补足 NIC 支持证明。**参数语义**：示例中的确认提示（"Are you sure you want to proceed [y/n]?"）已给出跳过说明——图像原文「(Pass --no-prompt option in command next time to suppress this prompt)」，即 `--no-prompt` 用于抑制该提示（此项同为编写者图像核对记录，未经独立核验）；`--no-prompt` 的完整行为与 `--force` 含义未取得说明，不推导。**DURATION 单位继续 unknown**（示例用 60，正文与示例图像均未注明单位）。DGX quickstart 页口径：「running the pre-flight stress test before putting a system into a production environment or after servicing」，`sudo nvsm stress-test --force` 覆盖 GPU/CPU/内存/存储、「takes approximately 20 minutes」（约数非保证）。两文档覆盖组件清单口径不同（NVSM §3.8.4 多 PCIe/网卡），各自引用不合并 | 时机为投产前或维修后；一次压测通过不等于长期稳定；引用 NIC 覆盖时必须分列「§3.8.4 正文泛述」与「示例中的机型限定」 | [NVSM User Guide Release 25.03 §3.8.4](https://docs.nvidia.com/datacenter/nvsm/nvsm-user-guide/latest/nvsm-user-guide.pdf)（PDF 署期 2026-07-13；正文 pdftotext 抽取 + 示例图像核验）、[DGX H100/H200 用户指南 Quickstart 页 Running the Pre-flight Test](https://docs.nvidia.com/dgx/dgxh100-user-guide/quickstart-basics.html) |
| ascend-dmi（MindX DL 6.0.RC2） | aicore 诊断/压测：Atlas A2 训练系列配套 HDK 23.0.0+ 的 MCU/驱动/固件，CANN 7.0.0+ 的 Ascend-cann-toolkit 与配套 Ascend-cann-kernels 并配置环境变量；network 诊断前 root 配置 RoCE 网卡 IP 与子网掩码再配置检测对象 IP；aicore 压测预留 HOST 约 20–40GB 内存；aicore 压测未返回不得重复压测；诊断完成后重启设备、压测完成后先分析定位再重启；「为确保带宽诊断效果准确性，建议在训练或推理业务开局的时候执行带宽诊断」——CCAE 或 npu-exporter 等监控组件会调用 dcmi 接口占用带宽导致误差，**环境干扰源要写入档案**；prbs 打流自动开关 NPU 与 CDR 自适应，偶现误码数 67092480 为正常现象；仅 6.0.RC2.1+ 支持码流诊断。耗时（页表1/2，文档量级非本站保证）：诊断 driver 1~4s、CANN 兼容性 2~7s、device 2~4s、network 30~70s、signalQuality 16~30s、片上内存 2~4s（均**不**影响业务）；bandwidth 1~5min、aiflops 29~40s、aicore 7~20min、prbs 3~10s（影响业务）；压测片上内存 1~3h、aicore 15~40min、片上内存高危地址 ≤17min（均影响业务） | 「是否影响 NPU 训练或推理」列是安排维护窗口与 drain 的直接依据；版本下限是页面所列前提，不是已验证配套矩阵；表4 prbs 行 PASS/FAIL 名字与描述相反（「FAIL 码流检测通过。RoCE端口信号质量正常（误码率小于10-5）」与「PASS 码流检测失败。RoCE端口存在误码，且误码率大于10-5」），为原文矛盾、未向厂商证实，不能只凭状态名验收 | [ascend-dmi 故障诊断页 前提条件/表1/表2/约束与限制/表4](https://www.hiascend.com/doc_center/source/zh/mindx-dl/60rc2/toolbox/ascenddmi/toolboxug_0020.html)（JS 动态页，2026-10-09 经桌面浏览器渲染整页复读取得；FetchURL 仅得参数表） |
| GPU Node Triage 基线与 RMA 地位 | 投产前用 nccl-tests `all_reduce_perf` 逐对测试并「record the performance achieved…provide a baseline for future comparisons」；多 rail 拓扑可按 rail 隔离定位；期望性能须与网络厂商/架构师确认（见「验收环境档案」验收目标行）；基线仅在拓扑/配置不变时可比。field diagnostic 是「the authoritative and comprehensive NVIDIA tool…usually required before an RMA」 | DCGM 的设计目标是投产前就绪评估，**不修复问题、不替代 field diagnosis、不判定 RMA 资格**（user-guide 页 Beyond the Scope；learn 页措辞为「do not repair faults, replace NVIDIA offline field diagnostics, or determine RMA eligibility」，语义一致） | [GPU Node Triage Network Testing 与 field diagnostic 相关节](https://docs.nvidia.com/deploy/gpu-debug-guidelines/gpu-node-triage.html)（2026-10-09 复读） |

## 证据接入与档案登记

1. **建档（首次测试前）**：按「验收环境档案」字段为节点建档。只有来自**授权实际节点**的证据才能填入档案——交付 BOM/配置清单、授权下的现场枚举、工具输出、运维与维修记录。身份缺失的节点只做 `unknown` 登记、不进入验收流程（与[节点选型、隔离返修、长期管理与退役](node-selection-and-lifecycle.md)的入库退出判据一致）；不得为「补齐版面」新增假装真实的空档案——字段无证据时保留 `unknown`，不借用同型号数值或「常见配置」。本库当前无任何真实验收环境档案（topic 01.6-G3 保持 open），实际档案由受授权验证轨道（V08）交付，未来以 `reference` 类条目承载并在本文 `environment_refs` 中引用。
2. **证据登记**：每次测试保留命令、目标选择、完整输出、debug log 与相关 plugin statistics（[DCGM learn 页 Results and Logging](https://docs.nvidia.com/datacenter/dcgm/latest/learn/modules/dcgm-diagnostics.html)）；注意其 JSON 输出「not governed by a stable schema」，作为集成边界前先看该页 JSON output 节。升级上报厂商时的证据清单（厂商口径）：基本系统配置（OS 与驱动信息）、问题描述与关键日志、已执行的调试步骤、完整日志、`nvidia-bug-report.sh` 输出、HGX 的 fabric manager 日志、DCGM Diagnostics 日志、应用细节（ISV、框架、版本号）（[GPU Node Triage Reporting a GPU Issue](https://docs.nvidia.com/deploy/gpu-debug-guidelines/gpu-node-triage.html)，2026-10-09 复读）。
3. **脱敏与外置**：档案与证据附件不得包含凭证（BMC 账户、证书、API 令牌）与未处理的敏感信息；机架位置、供电分组、序列号、node network identifiers 等资产/拓扑敏感字段按本地资产管理制度控制可见范围，正文只记录字段存在与脱敏状态；大日志（完整诊断输出、bug-report 打包、SEL 导出）引用受管存储位置而非内嵌正文——本库只保存方法、字段与结论，可变实时状态与大型证据一律外置。
4. **首次测试**：四层流程首次跑完即固定首版档案（版本面+拓扑面+负载面+结果面），基准层产出投产基线（步骤 5）。验证环境与生产一致性的参考口径是 SuperBench §5.1：「The environment for validation uses the exact same settings as production clusters, including firmware versions, hypervisor settings, BIOS configurations, etc. We fixed all software versions by using a dedicated VHD image for VM and a Docker image for validation execution」（VHD 基于 Ubuntu 22.04，Docker 基于 NGC 20.12，两镜像含 GPU/OFED 驱动与相关库，[arXiv HTML v2](https://arxiv.org/html/2402.06194v2)）——Azure 特定环境取值不可照搬，「与生产同版本」的原则可借鉴。
5. **修订后复验**：固件/驱动更新后须重新调参与重估——「After firmware/driver updates, re-tune and re-evaluate the repeatability in case it deteriorates on newer versions」（SuperBench §3.4；repeatability 定义为 N 个不同节点或运行的两两相似度算术均值）；本库纪律扩展到拓扑变更：「固件/驱动/拓扑变更后，投产基线作废，按『验收』层补测后才能继续使用旧基线做退化判断」（[node-selection-and-lifecycle.md 长期健康管理节](node-selection-and-lifecycle.md)）。复验只更新档案的版本/拓扑/历史面与对应证据，其余面保持不变，新旧结果才可比。
6. **回服确认**：维修件返回或隔离解除后，按[生命周期状态机](node-selection-and-lifecycle.md)的「回服」状态判据执行——重跑验收四层证据，更换后 `nvsm show health` 复核，退出判据同「验收」。注意 DGX 服务手册的更换后验证仅到 nvsm 级、未要求重跑性能基线，本流程要求回服仍按本文补齐基准层（同文「隔离与返修证据锚点」）；回服验收失败退回返修或重新隔离，不降级通过。

## 通过、失败与无法判断的判定纪律

- 三档结论与四层流程及「完成判据」衔接：**通过**=四层证据齐全且一致（完成判据第 1 项），结论表述为「在已执行的覆盖范围内未发现问题」；**失败**=任一层出现明确故障证据（完成判据第 2 项），转入处置；**无法判断**=证据不足（无法 drain、工具版本未固定、无基线、档案未建立），结论保持 `unknown` 并记录缺失项（完成判据第 3 项）。三档之间不允许降档通过：故障未处置不得回服，证据不足不得升级为通过，`unknown` 不是「默认健康」。
- 公开验收实践参考（采购文档语境，**不是本库执行标准**）：[NERSC《RFP Technical Requirements Document for NERSC-10 System》Version 6.0（2024-01-26）](https://www.nersc.gov/assets/NERSC-10/RFP-Technical-Requirements-Document-N10_v6.0_-1_26_24.pdf)的 §12.0 与 Appendix A Sample Acceptance Test Plan 给出一份公开可查的完整验收结构（2026-10-09 抽取核对）：验收测试「may exercise the system infrastructure with a combination of functionality tests, performance tests, forced failures, and stability tests」；pre-delivery 工厂测试含「Burn-in of all components」与 **72-Hour Test**（「High availability…for a 72-hour test period under constant throughput load」），测试清单另含 System Power Up/Down、Monitoring、Reset、Power On/Off、Fail Over/Resilience、Benchmarks；post-delivery 在全系统规模复跑全部 pre-delivery 测试；验收期（目标 60 天）由 Functionality Demonstration / System Test / System Resilience Test / Performance Test / Availability Test（30 连续日滑动窗口）组成。与本文档案/证据规范直接相关的条款：「All tests must be performed on the production configuration of the system, as it will be deployed to the University user community」（A.4）；「The Subcontractor must supply source code used, compile scripts, output, and verification files for all tests」（证据移交）；每项 benchmark 至少跑 5 次且「Performance must be consistent from run-to-run」（A.4.4）；「All performance tests must continue to meet acceptance criteria throughout the lifetime of the system」（§3.0）；可用性测试期间「if any system software upgrade or significant hardware repairs are applied, the Subcontractor shall be required to run the Benchmark Tests and demonstrate that the changes cause no loss of performance」，且最后 7 天禁止软硬件升级、不得有未关闭 critical bug（A.4.5）——与 SuperBench §3.4 的固件/驱动更新后重调重估互为印证，NERSC 口径把「重大硬件维修」也列为复验触发。
- 该文档的边界：它是美国国家实验室（LBNL/UC）采购需求**样板**——「The specifics of an acceptance plan will be determined before system delivery」，面向整机系统交付而非单节点验收；其引用的 benchmark run rules（gitlab.com/NERSC/N10-benchmarks/run-rules-and-ssi）未核。本文借其「生产配置上验收、证据全量移交、修订后复验」的结构作参考，不照搬其时长与阈值。
- **burn-in 缺口**：跨厂商、面向数据中心现场验收的 burn-in 执行指南（时长、负载曲线、判据）无公开权威文档，NVIDIA 工厂测试（L10 级）内容不公开。本文不编写无来源的 burn-in 处方；现场 burn-in 的负载曲线与判据保持 `unknown`，等待授权环境下的实践记录。

## 停止条件与恢复安排

- 任一层出现明确故障证据即停止本级继续测试，转入处置；不为"跑完流程"在故障节点上继续加压。
- 主动诊断/基准完成仅结束测试，不自动恢复节点。未处置故障、必需检查 skipped 且无替代证据、`unknown` 或必要收尾未完成时，维持 drain/隔离并记录缺失项与下一步。问题处置、必要重启/复测和验收判据均满足后，才按进入时记录恢复服务。
- AICore 诊断完成后的设备重启、AICore 压测后的分析定位再重启，按同页要求分别安排；保存结果并核对重启后状态。重启、固件/驱动/配置变更需已有授权、维护窗口与相应恢复计划，本文不授予执行权限。
- 诊断失败但原因指向 host/权限/拓扑/负载干扰时，先排除干扰源重跑，不直接判硬件故障。
- 验收期间发生固件/驱动/拓扑变更的，本轮证据只挂到变更前的档案版本；变更后按「证据接入与档案登记」第 5 条复验，不混用两个版本面的结果。

## 完成判据

以下任一结果可以结束本轮验收；只有第 1 项且必要收尾完成才满足回服门槛，第 2/3 项保持隔离或证据待补状态：

1. 四层证据齐全且一致：验收环境档案已建立且证据挂载一致、规格核对符合、被动证据无未处置事件、主动诊断通过（级别与机型条件已记录）、基准达到基线/判据——结论表述为"在已执行的覆盖范围内未发现问题"，**不写"硬件完全无故障"**（被动健康无事件与主动诊断失败可以互现；一次通过不证明无灰色退化，SuperBench 自身也声明无法覆盖全部负载×规模组合且罕见负载需先漏检一次）；
2. 某层发现故障或退化，处置结论（修复/隔离/RMA 流程）与证据链已归档；
3. 证据不足（如无法 drain、工具版本未固定、无基线、档案未建立）时，结论保持 `unknown`，缺失项写入待补清单。

SuperBench 的生产统计（24k+ A100、90 天、10.36% 节点判缺陷、有效 benchmark 复测一致性 >97.5%）说明主动验证能检出厂商出厂测试漏掉的退化，但它是 Azure 特定集群与负载的结果，不外推为本环境缺陷率；其 MTBI 提升 22.61× 来自仿真且假设全集 benchmark 能发现所有 incident。

## 来源与验证记录

- [DCGM Diagnostics user-guide 页（latest，2026-10-08 观察、2026-10-09 复读）](https://docs.nvidia.com/datacenter/dcgm/latest/user-guide/dcgm-diagnostics.html)：级别-测试表（含 Hopper 口径与 4 卡口径）、Deployment 插件 Preconditions/Failure、NCCL Tests Prerequisites、NVBandwidth Failure Conditions、Pulse Test 权限注意事项、Exit Codes、错误枚举；[learn 形态页（2026-09-30/10-08 观察，2026-10-09 复读）](https://docs.nvidia.com/datacenter/dcgm/latest/learn/modules/dcgm-diagnostics.html)：级别定位、drain/service account/timeout 前提、环境变量（NVVS_BIN_PATH、NVVS_PLUGIN_DIR、NVVS_HANGDETECT_DISABLE、NVVS_HANGDETECT_EXPIRY_SEC）、结果组织与证据保留清单、JSON 无稳定 schema、范围边界。两页清单口径不一致处已在步骤 3 注明；[DCGM v3.3.9 固定源码](https://github.com/NVIDIA/DCGM/tree/b0ec3c624ea21e688b0d93cf9b214ae0eeb6fe52)：diag-skus.yaml.in 按 SKU 配置与 plugin_src 目录边界（pulse/nvbandwidth/nccl_tests 不在开源目录）。
- [NVIDIA GPU Node Triage（latest，2026-10-09 复读）](https://docs.nvidia.com/deploy/gpu-debug-guidelines/gpu-node-triage.html)：排查结构、Xid 动作表、reset 能力矩阵、field diagnostic 的 RMA 地位、nccl-tests 基线建议、上报厂商证据清单；该页只提 diag 套件 1–3，与 DCGM 文档的 r4 并存。有效地址为 gpu-debug-guidelines 路径；早期引用的 `https://docs.nvidia.com/deploy/gpu-node-triage/` 于 2026-10-09 实测返回 HTTP 404，登记与引用均以有效地址为准。
- [SuperBench（USENIX ATC 2024，arXiv HTML v2）](https://arxiv.org/html/2402.06194v2)：主动验证动机、三层分类、群体判据方法与局限；§5.1 验证环境与生产完全一致并以专用 VHD/Docker 镜像固定全部软件版本、§3.4 固件/驱动更新后重调重估 repeatability（2026-10-09 复读）；Table 2 逐项清单未被 HTML 渲染，未逐项核对。
- [ascend-dmi 故障诊断（MindX DL 6.0.RC2，toolboxug_0020）](https://www.hiascend.com/doc_center/source/zh/mindx-dl/60rc2/toolbox/ascenddmi/toolboxug_0020.html)与[显示界面（toolboxug_0019）](https://www.hiascend.com/doc_center/source/zh/mindx-dl/60rc2/toolbox/ascenddmi/toolboxug_0019.html)：检查项、压测参数与产品/权限限制。0020 页为 JS 动态加载：FetchURL 抓取仅得参数表，前提条件、表1/表2 耗时与业务影响、约束与限制、表4 状态语义于 2026-10-09 经桌面浏览器渲染整页复读取得；表4 prbs 行 PASS/FAIL 与描述相反的冲突为原文矛盾，保持记录不作裁断。
- [DGX H100/H200 用户指南（2026-01-26）](https://docs.nvidia.com/dgx/dgxh100-user-guide/introduction-to-dgxh100.html)：规格核对基线；该页无验收/burn-in 专章。其 [Quickstart 页 Running the Pre-flight Test](https://docs.nvidia.com/dgx/dgxh100-user-guide/quickstart-basics.html)（2026-10-09 复读）：投产前/维修后 pre-flight stress test、约 20 分钟口径。
- [NVSM User Guide Release 25.03（PDF 署期 2026-07-13）](https://docs.nvidia.com/datacenter/nvsm/nvsm-user-guide/latest/nvsm-user-guide.pdf)：§3.8.4 stress test（sudo 执行、覆盖组件泛述与每组件 pass/fail 汇总；2026-10-09 下载 pdftotext 抽取第 69–70 页核对正文）。印刷页 70 / PDF 第 76 页示例截图的三项内容（NIC 压测限 DGX-1/DGX-2/Luna 且非支持平台该项结果为空白、确认提示给出「Pass --no-prompt option in command next time to suppress this prompt」的跳过说明、示例表 NIC 为 SKIPPED）为**编写者对官方 PDF 图像页的核对记录**（600 DPI 渲染 OCR，2026-10-09）：独立审阅第二轮定向复核会话图像调用失败、未能判读该页图像，未独立核验——URL 与页码保留以便后续独立复核。DURATION 单位与 `--force` 语义未明示，保留 `unknown`；当前具体机型 NIC 压测支持 unknown；latest PDF 链接可变，引用以 Release 25.03 署期为准。
- [OCP Server Component Resilience Workstream《Server Component Resilience》External Ver 0.3（2023-06-30）](https://www.opencompute.org/documents/external-ver-0-3open-compute-specification-server-component-resilience-workstream-pdf/)（2026-10-09 打开核对 §1/§4/§7/§8/§9）：测试环境档案字段规范（§7 输入、§8 输出、§9 part history）；面向 SDC 缺陷件信息共享而非验收流程；External Ver 0.3 为早期版本；贡献者含 Google/Meta/Microsoft/AMD/Intel/ARM/NVIDIA；文档自述 OWFa 1.0.2 许可、附录不受该许可覆盖。
- [NERSC《RFP Technical Requirements Document for NERSC-10 System》Version 6.0（2024-01-26）](https://www.nersc.gov/assets/NERSC-10/RFP-Technical-Requirements-Document-N10_v6.0_-1_26_24.pdf)（2026-10-09 下载 pdftotext 抽取 §3.0/§12.0/Appendix A）：采购验收结构（burn-in、72 小时恒吞吐、全规模复跑、生产配置验收、证据移交、修订后复验）；美国国家实验室采购样板语境，面向整机系统，不是本库执行标准。
- 逐条主张与证据定位见[第十二批节点验收来源记录](../../docs/research/batch-12-node-acceptance-sources.md)与[第十五批节点验收环境档案来源记录](../../docs/research/batch-15-node-acceptance-sources.md)。
- 当前验证范围：来源核对；未执行任何诊断、压测或基准。本文只交付方法——真实验收环境档案缺口（topic 01.6-G3）保持 open，由后续受授权验证轨道（V08）交付实际环境 reference 与证据后关闭。
- 待确认：NPU 与 DCGM 对应的级别化套件/处置枚举及覆盖对比；未在来源页给出的 ascend-dmi 内部判据，以及其他机型/配置的耗时与资源影响；DCGM pulse_test 权限问题的修复状态；dcgmi mndiag 多节点诊断；SuperBench Table 2 逐项清单与开源实现的实测口径；NVSM stress test 的 DURATION 单位与 `--force` 语义（`--no-prompt` 对确认提示的作用为编写者图像核对记录、未经独立核验，其完整行为未取证），以及当前具体机型的 NIC 压测支持（含第 76 页图像的独立复核）；NERSC-10 引用的 benchmark run rules 仓库；跨厂商现场 burn-in 执行指南（当前无公开权威文档）。单项耗时表与 AICore HOST 内存预算已按 ascend-dmi 页补齐。
