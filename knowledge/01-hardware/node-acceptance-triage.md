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
updated_at: "2026-10-08"
summary: 把验收分成规格核对、被动证据、主动诊断、基准验收四层，逐层记录证据强度与侵入性；DCGM 级别/单项测试与昇腾 ascend-dmi 分别固定版本，一次通过不声明硬件完全无故障，RMA 资格以厂商 field diagnostics 为准。
related_ids:
  - hardware.health-evidence
  - hardware.power-thermal-evidence
  - hardware.resource-topology
  - reliability.evidence-and-hypotheses
  - reliability.silent-errors-and-integrity
applicability:
  environment_refs: []
  notes: "GPU 侧证据样板为 DCGM latest 文档（2026-09-30/2026-10-08 观察）与 v3.3.9 固定源码、NVIDIA GPU Node Triage 页与 DGX H100/H200 用户指南；NPU 侧为 MindX DL 6.0.RC2 ascend-dmi 文档，AICore 的产品配套、HDK/CANN/算子包、HOST 内存与重启条件见正文；基准方法来自 SuperBench。目标集群的版本、机型、权限、资源预算与维护窗口需另行固定，本文不授予执行权限。"
verification:
  status: source_checked
  evidence_refs:
    - src.nvidia.dcgm-diag-user-guide-latest-2026-10-08
    - src.nvidia.gpu-node-triage-2026-10-08
    - src.usenix.superbench-atc24
    - src.huawei.mindx-dl-60rc2-ascend-dmi-2026-09-29
  notes: "已核对 DCGM 级别-测试表、插件前提、退出码与结果语义、SuperBench 判据方法与生产统计、ascend-dmi 参数、页首耗时表、AICore 前提/收尾及状态表、DGX 规格基线；未执行任何诊断、重启、压测或基准。"
---

# 新节点与返修节点验收

## 目标与触发条件

触发：新节点入网、集群扩容交付、故障维修后回服前，需要回答"这个节点现在能否承担生产负载"。验收结论分四档证据强度递增的层：**规格与配置核对 → 被动证据 → 主动诊断 → 基准验收**。层级之间不能互相替代：一次主动诊断通过不证明无灰色退化，基准达标也不替代故障诊断；每层都要记录自己的证据与边界。

## 适用范围与前置条件

- 证据样板：DCGM latest 文档（learn 与 user-guide 两种形态页，测试清单口径不一致处已分别注明）、DCGM v3.3.9 固定源码、NVIDIA GPU Node Triage 页（latest，2026-10-08 观察）、DGX H100/H200 用户指南（2026-01-26）、MindX DL 6.0.RC2 ascend-dmi 文档、SuperBench 论文（USENIX ATC 2024）。
- 权限与现场前提：主动诊断前把节点移出服务（drain 应用、与调度器协调）；DCGM 诊断默认降权到非特权 service account 执行，存在 `DCGM_ST_REQUIRES_ROOT`（退出码 227）等权限失败形态（[user-guide 页 Exit Codes 与 Pulse Test 注意事项](https://docs.nvidia.com/datacenter/dcgm/latest/user-guide/dcgm-diagnostics.html)）；ascend-dmi 的 aicore/prbs 等项要求 root 与特权容器（见步骤 4）。
- AICore 软件前提：该页列出 Atlas A2 训练系列配套的 HDK 23.0.0+ MCU/驱动/固件，以及 CANN 7.0.0+ 的 Ascend-cann-toolkit、配套 Ascend-cann-kernels 和环境变量配置（[ascend-dmi 前提条件](https://www.hiascend.com/doc_center/source/zh/mindx-dl/60rc2/toolbox/ascenddmi/toolboxug_0020.html)）。这是页面所列前提，不是一套已验证兼容矩阵；目标产品的软件配套仍须核对。
- **缺口声明**：ascend-dmi 页提供单项诊断/压测耗时表，尚未取得 DCGM r1–r4 式级别化套件和对应错误严重度/分类处置枚举；两工具覆盖差异未证实，不声明等价。多节点诊断（dcgmi mndiag）与各 SKU 具体阈值未核对。

## 需要的证据

| 证据 | 采集范围或定位 | 用途 | 缺失时如何处理 |
|---|---|---|---|
| 机型规格与拓扑 | 厂商组件表、端口↔PCI↔设备映射、电源冗余行为 | 第 1 层核对基线 | 无规格基线时只做外观与清点，不作符合性结论 |
| 被动健康证据 | 健康 watch、Xid、ECC/错误计数、降频位图与 violation 计数（见[健康证据](health-evidence.md)、[供电散热证据](power-thermal-evidence.md)） | 已知规则的当前状态 | 无事件只覆盖已启用规则与保留样本，不证明无故障 |
| 主动诊断结果 | DCGM diag 级别/单项，ascend-dmi -dg/-s | 受控负载下的故障检出 | 未 drain 或被负载干扰时结果不可信 |
| 基准证据 | nccl-tests 逐对结果与投产前基线；群体判据（SuperBench 方法） | 灰色退化/性能退化检出 | 无基线时只能给单次测量值，不给退化结论 |
| 处置记录 | 退出码、per-test/per-entity 结果、错误 ID/Severity/Category、必要重启/复测及回服决定 | 升级、隔离与回服门槛 | 非零码可能表达诊断检出失败，但不能单独判根因；失败或必需检查未覆盖时不回服（见步骤 6） |

## 步骤与判断分支

| 步骤 | 检查或动作 | 运行影响 | 预期证据与解释 | 下一步 |
|---|---|---|---|---|
| 1 | 规格与配置核对：以机型文档为基线核对组件数量与拓扑（如 DGX H100：8×H100 640GB、4×NVSwitch 900GB/s、6×3.3kW PSU 4+2、≥3 PSU 才开机且 3 PSU 时降性能运行，[DGX 用户指南](https://docs.nvidia.com/dgx/dgxh100-user-guide/introduction-to-dgxh100.html)，H100/H200 数值分列勿混）；NPU 侧用 ascend-dmi 显示界面核对芯片型号、NPU 数量、PCIe LnkCap/LnkSta、内存容量等（[toolboxug_0019 表2](https://www.hiascend.com/doc_center/source/zh/mindx-dl/60rc2/toolbox/ascenddmi/toolboxug_0019.html)） | 只读 | 配置与规格不一致 → 配置/装机问题，不进诊断层 | 进步骤 2 |
| 2 | 被动证据：健康状态、Xid、ECC 计数、降频位图与 violation 计数（字段语义与窗口边界分别见[健康证据](health-evidence.md)与[供电散热证据](power-thermal-evidence.md)） | 只读 | 有事件/计数 → 按事件处置；无事件 → 只能说明已启用规则在保留窗口内未命中 | 进步骤 3 |
| 3 | GPU 主动诊断（DCGM）：按级别选择——r1 software（就绪检查，Hopper 口径 <2.5 秒）；r2 加 pcie/memory/memory_bandwidth（8 卡 <10.5 分钟）；r3 加 diagnostic/targeted_stress/targeted_power/nvbandwidth/nccl_tests（8 卡 <35 分钟）；r4 加 memtest/pulse（8 卡 <2.25 小时）（[user-guide 页 Run Levels and Tests 表](https://docs.nvidia.com/datacenter/dcgm/latest/user-guide/dcgm-diagnostics.html)，表头注明 Hopper 实测口径；learn 页清单口径不同：含 context_create、不含 nccl_tests/sm_stress）。级别定位：r1 作收工前就绪检查、r2 作失败作业后检查、隔离疑似故障选单项、返修回服前跑管理员级长测（[learn 页 When diagnostics are useful](https://docs.nvidia.com/datacenter/dcgm/latest/learn/modules/dcgm-diagnostics.html)）。前提：先 drain；software/deployment 插件遇其他图形进程判失败；nvbandwidth 遇 MCUTIL>10% 判失败；nccl_tests 限单节点且需预设 DCGM_NCCL_TESTS_BIN_PATH（未设则优雅跳过） | 高：消耗算力/显存/供电/散热，侵入性测试只能在可移出服务的资源上运行 | 失败不一定在目标处理器——官方明示失败可源于 host/权限/库/拓扑/冷却/供电/负载干扰 | 按结果进步骤 5/6 |
| 4 | NPU 主动诊断（昇腾 ascend-dmi，MindX DL 6.0.RC2）：`-dg` 分软件与硬件检查项，bandwidth 覆盖 H2D/D2H/D2D/P2P；`-s` 触发 HBM/AICore 压测，`-st` 是 HBM 的 60–604800 秒参数，`--sc` 是 AICore 的 1–100 次参数；防呆提示与互斥条件按[参数表](https://www.hiascend.com/doc_center/source/zh/mindx-dl/60rc2/toolbox/ascenddmi/toolboxug_0020.html)核对。network/hbm 按各自机型清单（hbm 含 800I A2）；aicore 限 A2 训练/800I A2、root，容器/VM 需特权且不能与其他项同测；prbs 限指定机型、root、物理机/特权容器和 prbs31。先核对上列 HDK/CANN/算子包前提 | 高：AICore 压测需预留 HOST 约 20–40GB；页表1/2给 AICore 一轮诊断 7–20 分钟、压测 15–40 分钟，属文档量级，不是本站耗时保证 | 表1建议上线/巡检执行 3 轮 AICore 诊断并全部通过；任一 EMERGENCY_WARN 转故障处置。诊断完成需重启设备；压测完成需先分析定位再重启（页“约束与限制”），纳入维护窗口。PRBS 状态描述冲突继续保留，不能只凭 PASS/FAIL 名字验收 | 结果归档后进步骤 5/6；必要收尾未完成不恢复服务 |
| 5 | 基准验收（性能退化层）：投产前用 nccl-tests all_reduce_perf 逐对测试并记录性能作基线，多 rail 拓扑可按 rail 隔离（[GPU Node Triage 页 Network Testing](https://docs.nvidia.com/deploy/gpu-debug-guidelines/gpu-node-triage.html)）。判据来源要分清：SuperBench 的方法是**与集群群体判据比**而非与厂商规格比——端到端性能无法直接映射硬件规格、无 ground truth，其在集群 build-out 全集结果上用无监督 CDF 相似度判据（α=0.95、单向距离只判更差、迭代剔除后取中位样本），两阶段执行（单机→多机，阶段间剔除缺陷节点）（[SuperBench §2.3/§3.4/§4/§5.3](https://arxiv.org/html/2402.06194v2)）。单机/小规模验收没有群体判据时，只能依赖本地历史基线或诊断内建阈值（如 targeted_power 达 target_power 75% 判过、targeted_stress 默认达成 95% GFLOPS），二者证据强度不同 | 高：基准占用整机 | 显著低于基线/判据 → 灰色退化嫌疑，回步骤 2/3 定位；达标 → 记录基线入库 | 进步骤 6 |
| 6 | 处置与升级：同时解析退出码与结果本体（per-test/per-entity、Warning、SKIPPED、错误 ID/Severity/Category）。非零码可能表示请求/启动/连接失败，也可能表示已运行的诊断检出失败：226 / `DCGM_ST_NVVS_ERROR` 为诊断执行后报错，205 / `DCGM_ST_NVVS_ISOLATE_ERROR` 表示需隔离（[Exit Codes](https://docs.nvidia.com/datacenter/dcgm/latest/user-guide/dcgm-diagnostics.html#exit-codes)）。ISOLATE/RESET 级按官方建议及时处置，其余作站点分析/重跑/查日志；退出码不单独证明硬件根因，JSON 无稳定 schema。GPU 故障节点按[Xid 动作表](https://docs.nvidia.com/deploy/gpu-debug-guidelines/gpu-node-triage.html)处置；DCGM 不修复故障、不替代 field diagnostics、不判定 RMA 资格 | 结果解析为只读；隔离/reset/重启等处置依已有授权与维护窗口 | 失败、必需检查 skipped 且无替代证据、unknown 均保持节点不可调度并记录下一步；处置、必要重启/复测、验收判据满足后才形成回服决定 | 满足完成判据可结束调查；只有回服门槛满足才恢复服务 |

## 停止条件与恢复安排

- 任一层出现明确故障证据即停止本级继续测试，转入处置；不为"跑完流程"在故障节点上继续加压。
- 主动诊断/基准完成仅结束测试，不自动恢复节点。未处置故障、必需检查 skipped 且无替代证据、`unknown` 或必要收尾未完成时，维持 drain/隔离并记录缺失项与下一步。问题处置、必要重启/复测和验收判据均满足后，才按进入时记录恢复服务。
- AICore 诊断完成后的设备重启、AICore 压测后的分析定位再重启，按同页要求分别安排；保存结果并核对重启后状态。重启、固件/驱动/配置变更需已有授权、维护窗口与相应恢复计划，本文不授予执行权限。
- 诊断失败但原因指向 host/权限/拓扑/负载干扰时，先排除干扰源重跑，不直接判硬件故障。

## 完成判据

以下任一结果可以结束本轮验收；只有第 1 项且必要收尾完成才满足回服门槛，第 2/3 项保持隔离或证据待补状态：

1. 四层证据齐全且一致：规格核对符合、被动证据无未处置事件、主动诊断通过（级别与机型条件已记录）、基准达到基线/判据——结论表述为"在已执行的覆盖范围内未发现问题"，**不写"硬件完全无故障"**（被动健康无事件与主动诊断失败可以互现；一次通过不证明无灰色退化，SuperBench 自身也声明无法覆盖全部负载×规模组合且罕见负载需先漏检一次）；
2. 某层发现故障或退化，处置结论（修复/隔离/RMA 流程）与证据链已归档；
3. 证据不足（如无法 drain、工具版本未固定、无基线）时，结论保持 `unknown`，缺失项写入待补清单。

SuperBench 的生产统计（24k+ A100、90 天、10.36% 节点判缺陷、有效 benchmark 复测一致性 >97.5%）说明主动验证能检出厂商出厂测试漏掉的退化，但它是 Azure 特定集群与负载的结果，不外推为本环境缺陷率；其 MTBI 提升 22.61× 来自仿真且假设全集 benchmark 能发现所有 incident。

## 来源与验证记录

- [DCGM Diagnostics user-guide 页（latest，2026-10-08 观察）](https://docs.nvidia.com/datacenter/dcgm/latest/user-guide/dcgm-diagnostics.html)：级别-测试表、插件前提与判据、Exit Codes、错误枚举；[learn 形态页（2026-09-30/10-08 观察）](https://docs.nvidia.com/datacenter/dcgm/latest/learn/modules/dcgm-diagnostics.html)：级别定位、drain 前提、结果组织、范围边界。两页清单口径不一致处已在步骤 3 注明；[DCGM v3.3.9 固定源码](https://github.com/NVIDIA/DCGM/tree/b0ec3c624ea21e688b0d93cf9b214ae0eeb6fe52)：diag-skus.yaml.in 按 SKU 配置与 plugin_src 目录边界（pulse/nvbandwidth/nccl_tests 不在开源目录）。
- [NVIDIA GPU Node Triage（latest，2026-10-08 观察）](https://docs.nvidia.com/deploy/gpu-debug-guidelines/gpu-node-triage.html)：排查结构、Xid 动作表、reset 能力矩阵、field diagnostic 的 RMA 地位、nccl-tests 基线建议；该页只提 diag 套件 1–3，与 DCGM 文档的 r4 并存。
- [SuperBench（USENIX ATC 2024，arXiv HTML v2）](https://arxiv.org/html/2402.06194v2)：主动验证动机、三层分类、群体判据方法与局限；Table 2 逐项清单未被 HTML 渲染，未逐项核对。
- [ascend-dmi 故障诊断（MindX DL 6.0.RC2，toolboxug_0020）](https://www.hiascend.com/doc_center/source/zh/mindx-dl/60rc2/toolbox/ascenddmi/toolboxug_0020.html)与[显示界面（toolboxug_0019）](https://www.hiascend.com/doc_center/source/zh/mindx-dl/60rc2/toolbox/ascenddmi/toolboxug_0019.html)：检查项、压测参数与产品/权限限制。
- [DGX H100/H200 用户指南（2026-01-26）](https://docs.nvidia.com/dgx/dgxh100-user-guide/introduction-to-dgxh100.html)：规格核对基线；该页无验收/burn-in 专章。
- 逐条主张与证据定位见[第十二批节点验收来源记录](../../docs/research/batch-12-node-acceptance-sources.md)。
- 当前验证范围：来源核对；未执行任何诊断、压测或基准。
- 待确认：NPU 与 DCGM 对应的级别化套件/处置枚举及覆盖对比；未在来源页给出的 ascend-dmi 内部判据，以及其他机型/配置的耗时与资源影响；DCGM pulse_test 权限问题的修复状态；dcgmi mndiag 多节点诊断；SuperBench Table 2 逐项清单与开源实现的实测口径。单项耗时表与 AICore HOST 内存预算已按该页补齐。
