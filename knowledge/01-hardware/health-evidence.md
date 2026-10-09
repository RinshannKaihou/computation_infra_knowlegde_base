---
id: hardware.health-evidence
title: 设备健康证据与检测边界
type: reference
domain: hardware
status: draft
platforms: [generic, nvidia, ascend, amd]
source_refs:
  - src.nvidia.dcgm-v3.3.9
  - src.nvidia.dcgm-health-monitoring-latest-2026-09-30
  - src.nvidia.dcgm-diagnostics-latest-2026-09-30
  - src.nvidia.dcgm-exporter-metrics-latest-2026-09-30
  - src.ascend.mind-cluster-v26.1.1
  - src.huawei.mindx-dl-60rc2-ascend-dmi-2026-09-29
  - src.nvidia.xid-errors-docs-2026-09-09
  - src.nvidia.gpu-mem-error-mgmt-2026-09-09
  - src.nvidia.dgx-gb200nvl72-2-release-notes-2026-10-07
  - src.nvidia.dcgm-diag-user-guide-latest-2026-10-08
  - src.nvidia.gpu-node-triage-2026-10-08
  - src.huawei.hdk-26.1x-a2-npu-smi-2026-10-08
  - src.huawei.hdk-26.1x-a2-blackbox-errorcode-02-2026-10-09
  - src.huawei.hdk-26.1x-a3-blackbox-errorcode-02-2026-10-09
  - src.huawei.hdk-26.1x-a2-dcmi-returncode-2026-10-09
  - src.huawei.hdk-26.1x-a2-health-fault-def-02-2026-10-08
  - src.huawei.hdk-26.1x-a3-health-fault-def-02-2026-10-08
  - src.amd.amd-smi-docs-10.1.0
  - src.amd.afid-event-list-70122-v1.0
  - src.kernel.amdgpu-ras-v6.16
  - src.ocp.gpu-accelerator-ras-requirements-v1.0
updated_at: "2026-10-09"
summary: 区分设备健康摘要、错误事件、累计计数器、采样失败与未覆盖项；在 DCGM 与 DCMI/MindX 边界之外，补充 NVIDIA Xid 与诊断返回、昇腾 npu-smi/黑匣子/健康管理、AMD SMI/RAS 的三平台最小映射、五种含义对照与跨层时间线方法。
related_ids:
  - hardware.index
  - hardware.resource-topology
  - hardware.bmc-firmware-and-events
  - hardware.node-acceptance-triage
  - reliability.dimensions-and-failure-domains
  - reliability.evidence-and-hypotheses
verification:
  status: source_checked
  evidence_refs:
    - src.nvidia.dcgm-v3.3.9
    - src.nvidia.dcgm-health-monitoring-latest-2026-09-30
    - src.nvidia.dcgm-diagnostics-latest-2026-09-30
    - src.nvidia.dcgm-exporter-metrics-latest-2026-09-30
    - src.ascend.mind-cluster-v26.1.1
    - src.huawei.mindx-dl-60rc2-ascend-dmi-2026-09-29
    - src.nvidia.xid-errors-docs-2026-09-09
    - src.nvidia.gpu-mem-error-mgmt-2026-09-09
    - src.nvidia.dgx-gb200nvl72-2-release-notes-2026-10-07
    - src.nvidia.dcgm-diag-user-guide-latest-2026-10-08
    - src.nvidia.gpu-node-triage-2026-10-08
    - src.huawei.hdk-26.1x-a2-npu-smi-2026-10-08
    - src.huawei.hdk-26.1x-a2-blackbox-errorcode-02-2026-10-09
    - src.huawei.hdk-26.1x-a3-blackbox-errorcode-02-2026-10-09
    - src.huawei.hdk-26.1x-a2-dcmi-returncode-2026-10-09
    - src.huawei.hdk-26.1x-a2-health-fault-def-02-2026-10-08
    - src.huawei.hdk-26.1x-a3-health-fault-def-02-2026-10-08
    - src.amd.amd-smi-docs-10.1.0
    - src.amd.afid-event-list-70122-v1.0
    - src.kernel.amdgpu-ras-v6.16
    - src.ocp.gpu-accelerator-ras-requirements-v1.0
  notes: "核对范围：既有部分同前（DCGM v3.3.9 固定源码字段、DCGM health/diagnostics/exporter 当前页、MindCluster v26.1.1 DCMI 接口与 Go 封装、MindX DL 6.0.RC2 ascend-dmi 页）。本批新增：NVIDIA XID Errors 目录（2026-09-09 版，2026-10-09 观察，含目录结构、代表性条目与 Xid-Catalog.xlsx 可下载性）、DCGM Diagnostics User Guide 退出码、GPU Memory Error Management（仅目录结构）、GPU Node Triage 入口、DGX GB200 NVL72 2.0.0 Release Notes Improvements 页条目、华为 npu-smi 健康状态页、Atlas A2 黑匣子错误码列表 02（xlsx 逐行解析，91 数据行 13 列）、A2 健康管理故障定义 02、DCMI 返回码 dcmi_238（19 条 6 类）、AMD SMI docs-10.1.0（conceptual/ras、gpu-reset-behavior、amdsmi-cli-tool）、AFID Event List 70122 v1.0、内核 v6.16 固定 commit amdgpu ras.rst、OCP GPU & Accelerator RAS Requirements v1.0。A3 黑匣子与 A3 故障定义仅存在性核对。2026-10-09 按独立审阅（gpt-6.1-sol/xhigh）发现修订：重新打开 Xid 目录页并下载 Xid-Catalog.xlsx 逐行重建代表性 Xid 表（含 Table 2 的 Subcode V1/V2 版本条件）；复核 DCGM Exit Codes 原文（226/205/237 恢复原始语义）；复核 amd-smi reset Warning（XGMI hive、共享上游 PCIe switch SBR、/dev/kfd 进程三项影响范围）、monitor 参数表（-e/--ecc 为计数采样、-V/--violation 与 -v/--vram-usage 区分）与 About N/A values（字段级/节级区分）；复核 AFID Table 1 逐行（19=坏页退休门限 Fatal、22=片内 ECC Uncorrected Non-fatal）；GPU Node Triage 链接对齐到 gpu-debug-guidelines 路径（旧 gpu-node-triage/introduction.html 实测 404）；iBMC 告警处理 05 第一轮统一为部分取得口径。2026-10-09 第二轮定向复核后修订：Xid 140 删除「多到」数量因果、Xid 155 仅陈述 intentional 触发条件并保留 INVESTIGATE_SW_USER 非预期调查分支；Table 3 工作流阈值条件（WORKFLOW_NVLINK_ERR 第五寄存器 bits 20/23/26/29=ECC 错误阈值超过、WORKFLOW_XID_48 查 SRAM Error Threshold 标志）与「事件标识≠计数器读数」区分；AMD Not Available 改记为数据不可用并给出联合判定规则（覆盖边界/采集失败/解析错配/unknown），「诊断失败」示例改用有明确执行失败证据的条目；Empty Section CSV 双行为补全（全设备缺报省略整组列、部分缺失才填 N/A，缺列不得解释为零值/正常/已覆盖）；iBMC 告警处理 05 经渲染提取取得事件类告警页原文，所引 12 个事件码逐字复核一致，带外—带内官方映射仍未取得。2026-10-09 第三轮（第二轮定向复核后）修订：WORKFLOW_NVLINK_ERR 寄存器位图补 Hopper 产品限定（「valid for Hopper-based products」，不推广到 A100 或 Blackwell 的 WORKFLOW_NVLINK5_ERR）；iBMC 告警码引用补独立核验边界标注——所引码的含义/影响/建议为编写者经渲染提取取得并逐字核对的记录，独立审阅者两轮均未取得原文、未独立核验，不据此单独建立处置规则。未访问真实 GPU/NPU、未执行任何查询、诊断、复位或注入测试，未验证任一型号和版本组合。"
---

# 设备健康证据与检测边界

## 范围与阅读方式

本文回答“设备健康证据实际说明了什么”。它提供统一的记录方法，再分别说明 NVIDIA GPU 的 DCGM 与昇腾 NPU 的 DCMI/MindX 资料；其后给出三平台（NVIDIA / 昇腾 / AMD）错误码与健康映射的最小代表集合、五种证据含义的跨平台对照，以及带外/驱动/应用时间线的对齐方法。它不提供通用健康阈值、主动测试处方或本地验收结论。

`generic` 表示状态、事件、计数器、采集质量和覆盖范围可以用同一套证据结构记录，不表示 GPU 与 NPU 的字段、错误码、健康状态或诊断能力相同。设备身份与物理连接应先在[计算节点资源与拓扑参考](resource-topology.md)中对齐；状态与故障域之间的推理边界见[可靠性维度与故障域](../08-reliability/dimensions-and-failure-domains.md)。

本文引用的 DCGM 高层说明是 2026-09-30 观察到的 `latest` 页面，MindX 页面是 2026-09-29 观察到的 6.0.RC2 页面；固定源码只用于说明对应 commit 中的接口和字段。三者都不是目标环境的支持证明。

## 五类证据不能压成一个“健康”字段

| 证据类型 | 最低记录内容 | 可以支持的有限判断 | 不能推出 |
|---|---|---|---|
| 状态摘要 | 工具和版本、设备身份、查询时间、状态值、查询调用是否成功、已启用检查 | 该工具在该次查询和已覆盖范围内给出的摘要 | 所有子系统都被检查；未来仍健康；设备不存在其他故障 |
| 错误事件或错误码 | 事件码、来源组件、设备、发生/接收时间、上下文、丢失与保留条件 | 某来源在给定窗口记录了一个事件 | 任意非零码都等于永久硬件损坏；不同平台的码可以直接对照 |
| 计数器 | 字段名、单位、累计或窗口语义、起止值、采样时刻、重置边界 | 指定窗口内计数或增量如何变化 | 没有窗口与基线时，单个裸值可直接判故障；计数为零就证明没有事件 |
| 采样失败 | API/工具返回值、超时、权限、设备可见性、空值或无数据状态 | 检测链本身未能产生合格样本 | 把读不到记成零或 PASS；仅凭失败就断言器件损坏 |
| 未覆盖或不支持 | 未启用的 watch、型号/版本/插件限制、实体类型、容器与权限条件、明确的 `SKIP` | 指出本次证据没有回答哪些问题 | 未覆盖项已经通过；未见错误等于通过 |

状态摘要是其他证据的派生解释，不应覆盖原始返回值、字段值和采集质量。推荐把“设备状态”和“检测状态”分列：设备可以被工具判为 `PASS`，同时存在未启用项目；检测也可以失败，此时设备状态应保持 `unknown`，而不是改成 `FAIL` 或 `PASS`。

## GPU：DCGM 被动健康证据

### 被动 watch 的结论范围

[DCGM Health Monitoring](https://docs.nvidia.com/datacenter/dcgm/latest/learn/modules/health-monitoring.html)把 `dcgmi health` 描述为基于后台 field watches 和已保留样本的被动检查，并与主动的 `dcgmi diag` 区分。当前页面列出的健康系统包括 PCIe、内存、InfoROM、驱动、温度/功耗、NVLink/NVSwitch 等；实际覆盖仍取决于启用的 watch、实体和版本。

因此，“Healthy”只支持以下有限表述：在工具所看的时间范围内，已启用规则没有从已取得的样本中形成 incident。它不表示每种健康系统都已启用，不表示字段一定有有效样本，也不表示主动压力测试已通过。

被动证据至少应保存：

- DCGM 发行版或固定 commit，以及调用端/hostengine 的身份；
- GPU、GPU instance、compute instance、NVSwitch 等实体类型和稳定设备标识；
- 启用的 health systems、采样周期、保留期和判断时间窗；
- 原始字段或 incident、单位、样本时间和状态；
- `no data`、`not watched`、blank、`not supported` 与 API 失败等检测状态；
- 发生过 exporter、hostengine、驱动或设备复位时的计数器连续性。

### 固定字段例子

以下字段来自 DCGM tag `v3.3.9` 解引用后的固定 commit `b0ec3c624ea21e688b0d93cf9b214ae0eeb6fe52`。它们用于说明记录语义，不组成一张跨版本阈值表。

| 字段族 | 固定源码支持的语义 | 解释限制 |
|---|---|---|
| PCIe replay counter | [`dcgm_fields.h` 第 604–607 行](https://github.com/NVIDIA/DCGM/blob/b0ec3c624ea21e688b0d93cf9b214ae0eeb6fe52/dcgmlib/dcgm_fields.h#L604-L607)定义 replay counter | 裸总数没有观察窗口、链路代际/宽度、重置与规则版本时，不能直接判定异常 |
| XID | [第 640–643 行](https://github.com/NVIDIA/DCGM/blob/b0ec3c624ea21e688b0d93cf9b214ae0eeb6fe52/dcgmlib/dcgm_fields.h#L640-L643)说明字段值是具体 XID | XID 是事件码，不是可任意累加的严重度；含义需匹配驱动、GPU 与对应文档 |
| ECC volatile/aggregate totals | [第 758–778 行](https://github.com/NVIDIA/DCGM/blob/b0ec3c624ea21e688b0d93cf9b214ae0eeb6fe52/dcgmlib/dcgm_fields.h#L758-L778)区分 volatile 与跨驱动持续的 aggregate 值，并注明 aggregate SBE/DBE 单调增加 | 两类生命周期不同，不能在未记录驱动复位边界时混用；字段存在也不保证目标 GPU 可采集 |
| retired pages | [第 915–930 行](https://github.com/NVIDIA/DCGM/blob/b0ec3c624ea21e688b0d93cf9b214ae0eeb6fe52/dcgmlib/dcgm_fields.h#L915-L930)区分 SBE、DBE 与 pending retirement | 单个累计值不能说明发生时间；pending、已退休和错误事件是不同证据 |
| NVLink CRC FLIT total | [第 982–985 行](https://github.com/NVIDIA/DCGM/blob/b0ec3c624ea21e688b0d93cf9b214ae0eeb6fe52/dcgmlib/dcgm_fields.h#L982-L985)定义累计字段 | 必须记录链路端点、采样窗口和支持状态；不能把该字段外推到未覆盖的链路类型 |

固定实现内部包含版本特定规则和常量。那些实现值只能描述该快照中的判断逻辑，不能复制成所有 GPU、驱动和 DCGM 版本的运维阈值。

### exporter 计数需要采集生命周期

[DCGM Exporter Metrics](https://docs.nvidia.com/datacenter/dcgm/latest/reference/dcgm-exporter-metrics.html)在当前页面中区分以下派生指标；这些语义不倒推到固定 DCGM v3.3.9 或未知 exporter 版本。

| 指标 | 统计对象 |
|---|---|
| `DCGM_EXP_XID_ERRORS_COUNT` | 配置窗口内的 XID 样本记录，按 `xid` 分类 |
| `DCGM_EXP_CLOCK_EVENTS_COUNT` | 窗口内对应 clock-event bit 为 active 的样本记录 |
| `DCGM_EXP_XID_ERRORS_TOTAL` | collector 启动后观察到的非零 XID 记录 |
| `DCGM_EXP_CLOCK_EVENTS_TOTAL` | 对应 clock event 从 inactive 到 active 的转换；初始化时已经 active 的状态不计新转换 |

两个 `COUNT` 族是样本数，受采集节奏影响，不是唯一事故次数。窗口内无有效来源样本时，可能输出缺少事件分类标签的零值序列；两个 `TOTAL` 族在首次观察前可能无序列，累计值在 exporter 启动或 hot reload 重建 collector 后重置。**零值、序列缺失与没有事件不能互换。** 原始 XID 字段仍是事件码，不是这里的派生计数。

因此，监控记录至少要区分设备/驱动计数器、DCGM 缓存窗口和 exporter 进程生命周期。跨重启拼接曲线前没有连续性证据时，应在重启点断开，而不是把值下降解释成设备恢复或把新进程的零值解释成没有历史事件。

## GPU：主动诊断的边界

[DCGM Diagnostics](https://docs.nvidia.com/datacenter/dcgm/latest/learn/modules/dcgm-diagnostics.html)说明，主动诊断可能占用 GPU 计算、显存、PCIe/NVLink、CPU、功耗和散热资源；较长套件可能复位设备或与同时运行的工作负载冲突。文档还要求显式指定实体并与调度环境协调，使目标硬件脱离普通服务。

主动诊断结果的正确解释是“某个 DCGM 版本、某组可用插件和依赖，在给定硬件、权限及隔离条件下运行了某个测试集合”。它不是单一的“硬件好/坏”判决：

- 失败可能来自宿主环境、权限、库/可执行文件、拓扑、供电、散热或并发工作负载，也可能来自设备；
- 可用测试取决于 DCGM 版本、插件、实体、GPU 型号及所需动态库/程序；未运行的测试保持未覆盖；
- 诊断不负责修复，不替代离线现场诊断，也不能单独决定 RMA；
- 被动健康与主动诊断可以因为时间窗、覆盖和负载不同而给出不同结果，不能强行归并。

本文不提供通用运行步骤。任何实际主动测试都需要另行确认目标、影响范围、服务隔离、证据保全、停止条件、恢复验证和已有执行授权。

## NPU：DCMI 状态、错误与计数器

NPU 部分以 MindCluster `v26.1.1` 固定 commit `44385c13d7b1d87def35f1604e8be4d16de6ca4e` 的 DCMI 接口和 Go 封装为边界。该源码证明此快照怎样区分查询返回与设备值；它不构成所有昇腾型号或软件版本的支持表。

| 证据 | 固定源码位置 | 应保留的区别 |
|---|---|---|
| 健康摘要 | [`dcmi_interface_api.h` 第 606 行](https://github.com/Ascend/mind-cluster/blob/44385c13d7b1d87def35f1604e8be4d16de6ca4e/component/ascend-common/devmanager/dcmi/dcmi_interface_api.h#L606-L606)；Go 封装[第 1567–1582 行](https://github.com/Ascend/mind-cluster/blob/44385c13d7b1d87def35f1604e8be4d16de6ca4e/component/ascend-common/devmanager/dcmi/dcmi.go#L1567-L1582) | DCMI 调用返回与健康码分开；源码未在此给出所有健康码的产品化自然语言含义 |
| 错误码 | 接口[第 608 行](https://github.com/Ascend/mind-cluster/blob/44385c13d7b1d87def35f1604e8be4d16de6ca4e/component/ascend-common/devmanager/dcmi/dcmi_interface_api.h#L608-L608)；封装[第 1504–1524 行](https://github.com/Ascend/mind-cluster/blob/44385c13d7b1d87def35f1604e8be4d16de6ca4e/component/ascend-common/devmanager/dcmi/dcmi.go#L1504-L1524) | 查询失败、错误码数量和错误码内容是三类记录，不能把调用失败伪装成空错误列表 |
| ECC | `dcmi_ecc_info` [第 72–91 行](https://github.com/Ascend/mind-cluster/blob/44385c13d7b1d87def35f1604e8be4d16de6ca4e/component/ascend-common/devmanager/dcmi/dcmi_interface_api.h#L72-L91)；Go 封装[第 2266–2290 行](https://github.com/Ascend/mind-cluster/blob/44385c13d7b1d87def35f1604e8be4d16de6ca4e/component/ascend-common/devmanager/dcmi/dcmi.go#L2266-L2290) | 使能标志、当前/累计 SBE/DBE 与隔离页分别保存；接口存在不证明每个型号返回有效值 |
| 网络健康 | 接口[第 642 行](https://github.com/Ascend/mind-cluster/blob/44385c13d7b1d87def35f1604e8be4d16de6ca4e/component/ascend-common/devmanager/dcmi/dcmi_interface_api.h#L642-L642)；封装[第 1780–1813 行](https://github.com/Ascend/mind-cluster/blob/44385c13d7b1d87def35f1604e8be4d16de6ca4e/component/ascend-common/devmanager/dcmi/dcmi.go#L1780-L1813) | 调用返回、健康码与超时分开；源码注释说明掉卡后调用可能阻塞，超时不是一个正常健康值 |
| 故障事件 | `dcmi_dms_fault_event` [第 404–420 行](https://github.com/Ascend/mind-cluster/blob/44385c13d7b1d87def35f1604e8be4d16de6ca4e/component/ascend-common/devmanager/dcmi/dcmi_interface_api.h#L404-L420)及订阅入口[第 674 行](https://github.com/Ascend/mind-cluster/blob/44385c13d7b1d87def35f1604e8be4d16de6ca4e/component/ascend-common/devmanager/dcmi/dcmi_interface_api.h#L674-L674) | 事件流与一次状态查询是不同证据；还需另记订阅生命周期、丢失条件和设备身份 |

Go 封装的[第 1955–2023 行](https://github.com/Ascend/mind-cluster/blob/44385c13d7b1d87def35f1604e8be4d16de6ca4e/component/ascend-common/devmanager/dcmi/dcmi.go#L1955-L2023)还包含超时、重试以及 `DeviceNotReady` 到掉卡故障码的封装层映射。引用该码时应说明它来自这个实现层，不能把封装逻辑误写成所有 DCMI 版本的原始设备返回。

## NPU：MindX 主动诊断与压测边界

2026-09-29 观察到的 [MindX DL 6.0.RC2 `ascend-dmi` 故障诊断页](https://www.hiascend.com/doc_center/source/zh/mindx-dl/60rc2/toolbox/ascenddmi/toolboxug_0020.html)列出设备、网络、HBM、AICore、signal quality、PRBS 和 stress 等项目。各项目的产品、环境和权限条件不同，不能把其中一项 PASS 扩张为整个 NPU 或整机通过。

下表按测试项保留条件，依据同页“约束与限制”“前提条件”和表 3；不将某项条件移给其他测试：

| 测试项 | 该页限定的前提或影响 |
|---|---|
| AICore 诊断/压测 | Atlas A2 配套 HDK 23.0.0+ 的 MCU/驱动/固件，CANN 7.0.0+ toolkit 与配套 kernels；表 3 另限支持产品、root 和执行环境。两者影响业务，诊断后与压测分析定位后分别有设备重启要求 |
| AICore 压测的额外资源 | HOST 内存约 20–40 GB；不能扩张为全部诊断的内存要求 |
| PRBS 码流诊断 | 工具 6.0.RC2.1+；表 3 限 Atlas 800T A2、200T A2 Box16、800I A2，root、物理机或特权容器，不能与其他诊断并行；影响业务。AICore 的 HDK/CANN 条款不能据此转给 PRBS |
| network 诊断 | Host root 配置 RoCE IP/子网掩码及检测对象 IP；型号范围另见表 3 |
| HBM 诊断与压测 | 表 1 的普通片上内存诊断标为不影响业务，表 2 的内存压测及高危地址压测标为影响；支持产品和执行环境仍需对应参数核对 |
| 带宽、AI FLOPS | 影响训练/推理；并行 DCMI 监控还可能干扰带宽结果 |

表中出现的特权环境和重启要求只是来源条件，不是执行建议。输出 `SKIP` 可表示产品或权限不支持，`FAIL` 也可能是读取/执行失败；二者都不能直接变成器件损坏的结论。

页面末端 PRBS 结果表的中英文描述内部冲突：`FAIL` 行写有“检测通过/误码率小于…”，`PASS` 行反而写“检测失败/误码率大于…”。在没有勘误或另一份同版本权威资料前，本文不采用其中的阈值或 PASS/FAIL 解释，只把该项目标为来源冲突。

MindX 6.0.RC2 页面与 MindCluster v26.1.1 固定源码不构成同一套已验证环境。前者只能说明其页面所列主动测试和适用条件，后者只能说明固定 DCMI 封装。二者不应拼成版本支持矩阵。

## 统一记录格式

下面的字段是本库建议的证据记录结构，不是任何厂商 API，也不是已经采集的样例结果。

| 字段 | 记录规则 |
|---|---|
| `platform` / `tool_identity` | GPU/NPU 平台、工具或库、版本/commit、进程或服务身份 |
| `device_identity` | 物理设备、切分实例、总线/板内位置及与节点资源档案的映射 |
| `observation_kind` | `status_summary`、`error_event`、`counter`、`sampling_failure` 或 `uncovered` |
| `observed_at` / `window` | 查询时间，或开始/结束时间与所用时钟；不能只写“最近” |
| `raw_value` / `unit` | 保留原始码和值，派生解释另列；未知单位不得补写 |
| `counter_scope` | 累计、进程启动以来、缓存窗口或区间增量；保存已知重置点 |
| `collection_status` | 成功、无数据、未监视、不支持、blank、超时、权限失败或其他原始返回 |
| `coverage` | 已启用系统/测试、未启用或跳过项、型号/插件/权限限制 |
| `interpretation` | 仅写该证据在已知范围内支持的判断，并列出替代解释 |
| `source_or_evidence` | 精确文档/源码位置，或经管理的实际证据引用；不嵌入大日志和实时集群状态 |

跨 GPU/NPU 汇总时，只汇总“是否有合格证据”和“结论状态”，不要把不同厂商的错误码或计数器数值放进同一个可比较量。把观测推进为根因结论的方法见[诊断中的证据、假设与结论](../08-reliability/evidence-and-hypotheses.md)。

## NVIDIA：Xid 与诊断返回的最小代表集合

### Xid 目录的版本与结构

Xid 是 NVIDIA 内核驱动经内核日志上报的事件码。2026-09-09 版（2026-10-09 观察）的 [XID Errors 文档集](https://docs.nvidia.com/deploy/xid-errors/analyzing-xid-catalog.html)给出以下口径：

- Xid 含义跨驱动版本保持一致，但目录是**调试指引，不是根因判决**；
- 采集入口为 `journalctl` 中 grep `"NVRM: Xid"`；首条 Xid 行之前有一条带 GPU GUID/PCI BDF 的前置行，设备身份应与事件一并保存；官方列出的辅助工具为 nvidia-smi、DCGM 与 `nvidia-bug-report.sh`；
- 目录持续新增条目（143 起对应 CUDA 12.9/R575，另有 162–172 等新行），**固定引用必须带观察日期**；新增行的 Resolution 桶可以为空；
- SXid 仅适用 Hopper 及更早，Volta 及更早另有旧目录，不同代际的码表不可混用。

结构警示：现行 Analyzing with the Xid Catalog 的 Table 1 共 12 列，其中四个 YES/NO 列是 A100/H100/B100/GB200 的**产品适用性**（"Signifies if the Code is supported on this particular product"），不是归因列；第三方旧版转载中的 HW Error/Driver Error 归因列结构已被官方废弃，不可再引用。目录另设 Guidance Classes（34 个处置桶），同一 Xid 的立即动作（immediate）与排查动作（investigatory）可以不同；Xid 13/31 等走 workflow 桶（WORKFLOW_XID_13/31），同一码出现在不同桶时以 workflow 桶的解释优先。配套的 Xid-Catalog.xlsx 与 XID_Errors.pdf 于 2026-10-09 可下载，与页面同源。

### 代表性 Xid 的最小集合

下表从官方目录 Table 1 逐行选录代表性条目（2026-10-09 重新打开页面并与同源 Xid-Catalog.xlsx 交叉核对）。Xid 是**事件码**，本身无物理单位；但「事件标识」与「计数/阈值证据」要区分——Xid 码本身是事件标识而不是计数器读数，目录的个别工作流却带有阈值条件，须按条目解码：Table 3 的 WORKFLOW_NVLINK_ERR 中，目录明示「The first, third, fourth and fifth registers are valid for **Hopper-based products**」——第一、第三、第四和第五寄存器的位图解释仅适用于 Hopper：其中第五寄存器 bits 20/23/26/29 置位表示 ECC 错误阈值超过（目录原文 "These errors represent a threshold of ECC errors being exceeded"，当时无不可纠正错误、可继续运行，可选跑 Field Diags 检查链路完整性）；该位图不得仅凭 Xid 74 的产品适用性（A100 YES）推广到 A100，也不适用于 Blackwell 的 WORKFLOW_NVLINK5_ERR（其解码按 Table 2 的 Subcode/Error Status 位图，见表中 144–150 行）；WORKFLOW_XID_48 要求检查 SRAM Error Threshold 标志（nvidia-smi `<sram_threshold_exceeded>` 或 NSM Msg Type 0x3 Cmd Code 0x7D bit 0，置位则 RUN_FIELDDIAG）。既不能从某个 Xid 码推导计数门限（如对 Xid 140），也不能否定目录中这些带阈值语义的工作流分支。每条的检测前提都是“驱动在运行系统上经内核日志上报”——上报成功只说明事件进入日志，不说明已被任何监控消费。四列产品适用性（A100/H100/B100/GB200）照录目录 YES/NO；立即动作（Immediate）与调查动作（Investigatory）是目录的 Resolution Bucket，桶的展开步骤在目录的 Fault Resolution Buckets 工作表中定义，本文不另行发明处置动作。

| Xid | 码义（目录 Description） | 产品适用性（A100/H100/B100/GB200） | 立即动作 | 调查动作 | 影响解释的边界 |
|---|---|---|---|---|---|
| 13 | Graphics Engine Exception | YES/YES/YES/YES | RESTART_APP | WORKFLOW_XID_13 | 一般为用户应用 fault（越界、非法指令/寄存器等）；目录明示罕见情况下硬件或系统软件问题也可表现为 Xid 13 |
| 31 | GPU memory page fault | YES/YES/YES/YES | RESTART_APP | WORKFLOW_XID_31 | MMU 上报 fault（片上单元非法地址访问）；通常为应用级 bug，也可能是驱动或硬件 bug——不是 push buffer 事件 |
| 32 | Invalid or corrupted push buffer stream（PBDMA error） | YES/YES/YES/YES | RESTART_APP | CHECK_APP/CUDA | 驱动与 GPU 间 PCIe 通信流的 DMA 控制器 fault；目录明示主要涉及 PCI 质量问题，一般不是用户应用动作引起 |
| 43 | GPU stopped processing（ResetChannel Verif Error） | YES/YES/YES/YES | IGNORE | CONTACT_SUPPORT | 用户应用命中软件诱导 fault 被终止；目录明示 "The GPU remains in a healthy state"——立即动作是忽略而非复位 |
| 45 | Preemptive cleanup, due to previous errors | YES/YES/YES/YES | WORKFLOW_XID_45 | Solo: RESTART_FM；Not Solo: IGNORE (follow other Xid) | 应用 abort（Ctrl-C、GPU reset、sigkill）后驱动拆除通道；目录明示多数情况下是用户或系统动作而非 bug；须按其工作流与伴随事件解释 |
| 48 | Double Bit ECC Error | YES/YES/YES/YES | WORKFLOW_XID_48 | WORKFLOW_XID_48 | 不可纠正内存错误事件，需 GPU reset 或节点重启清除；SRAM DBE 超阈值走 RMA 流程（阈值标志读取方式见目录行）；与累计计数（volatile/aggregate）是不同证据 |
| 62 | Internal micro-controller halt（newer drivers） | YES/YES/YES/YES | RESET_GPU | CONTACT_SUPPORT | 内部微控制器/PMU 停止——**不是 NVLink 事件**；Xid 154 linkage 列注明 CUDA 12.7/R565 起 |
| 63 | GPU memory remapping event | YES/YES/YES/YES | IGNORE | IGNORE | ECC 内存错误处理事件：Ampere 起支持行重映射（row remapping）的 GPU 上为重映射活动记录，更早支持动态页退休的 GPU 上为页退休活动记录——按 GPU 代际分述，不混用 |
| 64 | GPU memory remapping failure | YES/YES/YES/YES | RESET_GPU | CONTACT_SUPPORT | 同上的重映射/退休**失败**事件；63 记录成功动作、64 记录动作失败，是错误→处置链的不同环节 |
| 74 | NVLINK Error | YES/YES/NO/NO | WORKFLOW_NVLINK_ERR | CONTACT_SUPPORT | 链路本身或对端设备问题都可能在两端报出；需 GPU reset 或节点重启清除；反复出现且复位不能清除时联系硬件厂商；产品适用性不含 B100/GB200（NVLink 5 代际走 144–150） |
| 79 | GPU has fallen off the bus | YES/YES/YES/YES | RESTART_BM | CONTACT_SUPPORT | PCIe 访问不到 GPU；常因 PCIe 链路硬件问题，也可能是 GPU 硬件或驱动问题，目录不作单一归因，建议查系统事件日志与内核 PCI 事件日志 |
| 92 | High single-bit ECC error rate | YES/YES/YES/YES | IGNORE | CONTACT_SUPPORT | 单比特 ECC 错误率过高——**不是错误遏制级别**；与 94/95 的遏制语义无关 |
| 94 | Contained memory error | YES/YES/YES/YES | RESTART_APP | IGNORE (sympathetic) | 支持错误遏制的 GPU（自 A100 起）：错误限于单个应用，该应用须重启，其他应用不受影响；目录建议方便时复位 GPU |
| 95 | Uncontained memory error | YES/YES/YES/YES | RESET_GPU | IGNORE (sympathetic) | 同上但影响多个应用；受影响 GPU 必须复位后才能重启应用 |
| 109 | Context Switch Timeout Error | YES/YES/YES/YES | RESET_GPU | CONTACT_SUPPORT | Xid 154 linkage 列注明 CUDA 12.7/R570 起 |
| 110 | Security Fault Error | NO/YES/YES/YES | RESET_GPU | INVESTIGATE_SW | 安全故障（SEC_FAULT_ERROR），**不是热相关事件**；目录明示除非硬件故障否则应当罕见，恢复为回退近期硬件改动并冷复位 |
| 119 | GSP RPC Timeout | YES/YES/YES/YES | RESET_GPU | INVESTIGATE_SW | GSP 核心代码错误或 RPC 超时；持续存在需 GPU reset 或节点下电 |
| 120 | GSP Error | YES/YES/YES/YES | RESET_GPU | INVESTIGATE_SW | 同 119；GSP 相关码的解释随驱动与 GSP 固件版本变化 |
| 121 | C2C Error | NO/NO/NO/YES | IGNORE | CONTACT_SUPPORT | Grace C2C NVLink 连接上的**已纠正**错误，系统已纠正、无运行影响；仅 GB200 适用；服务窗口复位 GPU 可重训链路 |
| 140 | ECC Unrecovered Error | YES/YES/YES/YES | RESET_GPU | CONTACT_SUPPORT | 驱动观察到显存中的不可纠正错误，其方式中断了驱动将这些页标记为动态页离线或行重映射的能力；复位 GPU，持续则联系硬件厂商——目录只说错误以某种方式中断了标记能力，**没有**「数量过多」或「ECC 计数超门限」语义，不得从码名推导阈值 |
| 143 | GPU Initialization Error | NO/YES/YES/YES | RESET_GPU | CONTACT_SUPPORT | GPU 初始化错误——不是 ECC 事件；Xid 154 linkage 列注明 CUDA 12.9/R575 起 |
| 144–150 | NVLink 5 错误族：144 SAW / 145 RLW / 146 TLW / 147 TREX / 148 NVLPW_CTRL / 149 NETIR / 150 MSE | NO/NO/YES/YES | WORKFLOW_NVLINK5_ERR | WORKFLOW_NVLINK5_ERR | 仅 B100/GB200 适用；须按目录 Table 2（Xid 144-150 Decode）结合消息中的 Subcode 与 Error Status 位图解码：Subcode 有 **V1（<R575，IntrInfo[9:5]）与 V2（≥R575，IntrInfo[6:0]）两个版本**，解码列给出 Resolution Bucket、Severity（Link Fatal/Fatal/non-fatal 等）、HW/SW 与 Local/Remote；145 的子码行含 IGNORE、RESET_GPU、XID_154_EVAL 等桶，**处置并非空白** |
| 154 | GPU Recovery Action Changed | YES/YES/YES/YES | XID_154 | N/A（Informational only regarding another Xid） | 与其他 Xid 并发，汇总所需恢复动作，取值集合 {None, Drain P2P, Drain and Reset, GPU Reset Required, Node Reboot Required}；官方枚举把 GPU 级复位与节点级重启区分为不同恢复动作，是 NVIDIA 侧 reset 语义的权威边界；不能脱离伴随 Xid 解释 |
| 155 | NVLINK: SW Defined Error | NO/NO/YES/YES | RESET_GPU | INVESTIGATE_SW_USER | 触发条件是标记为「intentional」的链路下线事件（含转入 SLEEP）；intentional 标记只说明该次链路下线被标记为有意动作，不证明其符合预期——非预期出现时的调查桶为 INVESTIGATE_SW_USER（调查软件或用户动作），不直接判为无异常 |
| 156 | Resource Retirement Event | NO/YES/YES/YES | RESET_GPU | IGNORE | 资源退休事件；A100 不适用 |
| 158 | GPU Fatal Timeout | YES/YES/YES/YES | RESET_GPU | CONTACT_SUPPORT | GPU 致命超时；Xid 154 linkage 列注明 "yes; support with Xid introduction" |

目录另有 162–172 等较新条目（PSHC 电源平滑、CC 机密计算、DRAM/SRAM 细节区分等），这些行的 Resolution 桶在 2026-10-09 观察时为空——“新增行桶可为空”适用于这些行，不代表无需处置，也不适用于上表任何行。

表中没有官方解释的码不在本集合内；具体机型动作以[官方 GPU Node Triage](https://docs.nvidia.com/deploy/gpu-debug-guidelines/gpu-node-triage.html)的处置链（常见 Xid 动作表→Running DCGM Diagnostics→Running Field Diagnostics）为准，本文不另行发明处置动作。注意 `https://docs.nvidia.com/deploy/gpu-node-triage/introduction.html` 于 2026-10-09 实测返回 HTTP 404，有效地址为 gpu-debug-guidelines 路径（与登记来源一致）。

### DCGM diag 退出码：诊断失败与未覆盖的机器可读语义

[DCGM Diagnostics User Guide](https://docs.nvidia.com/datacenter/dcgm/latest/user-guide/dcgm-diagnostics.html)（2026-10-08 观察的 latest 页面，2026-10-09 复核 Exit Codes 表）给出的进程退出码中，五条直接对应“诊断失败/未覆盖”类别，应与设备故障分开记录。退出码是 `dcgmReturn_t` 枚举值的机器可读语义，**本身不携带处置动作**：

| 退出码 | 符号与原始含义 | 证据类别 |
|---|---|---|
| 226 | DCGM_ST_NVVS_ERROR："DCGM GPU Diagnostic was successfully executed, but **reported an error**" | 诊断运行完成且报告了错误；**不能由该码单独推出节点重启**——后续分支以官方处置链（见下）与现场授权为准 |
| 205 | DCGM_ST_NVVS_ISOLATE_ERROR："The diagnostic returned an error that **indicates the need for isolation**" | 诊断返回的错误表明**需要隔离**；隔离的执行动作（drain/cordon 等）以官方处置链与现场授权为准 |
| 242 | DCGM_ST_NO_DATA："No data is available" | 未覆盖：该次诊断没有产生数据 |
| 240 | DCGM_ST_NOT_WATCHED："The given field id is not being updated by the cache manager" | 未覆盖：相关项未被监视 |
| 237 | DCGM_ST_RESET_REQUIRED："**GPU requires a reset**" | 设备状态语义：目标 GPU 需要复位；复位本身是高影响动作，其前提、影响范围与恢复安排按本文「五种含义的区分」与「高影响处置入口与现场授权」节处理 |

240/242 是**未覆盖**而不是 PASS；226/205 是诊断判定的失败结论（205 额外携带隔离需求）；237 描述设备需要复位这一状态。退出码描述的是这一次诊断运行，不直接等价于硬件损坏判决。官方处置链（[GPU Node Triage](https://docs.nvidia.com/deploy/gpu-debug-guidelines/gpu-node-triage.html)）把 Xid、DCGM 字段与退出码串成一条线，本文不复制其流程，只要求记录时保留三者的原始值。

### 错误→处置链的官方结构：GPU Memory Error Management

[GPU Memory Error Management](https://docs.nvidia.com/deploy/a100-gpu-mem-error-mgmt/index.html)（2026-09-09 版）的章节结构展示了 NVIDIA 侧内存错误的官方处置链：Overview / Supported GPUs / Error Containment / Dynamic Page Offlining / Row Remapping / RAS Repair / Response to Uncorrectable Contained ECC Errors / Error Recovery and Response Flags / User Visible Statistics / RMA Policy / SRAM Uncorrectable Errors。**本轮只核对了文档目录结构，各小节正文未逐段核对**；因此本文只引用“错误遏制→动态页离线→行重映射→RMA 政策”这条链的存在性，具体阈值、适用 GPU 清单与 RMA 条件在补核前不写入正文。

## Ascend：健康与错误码映射（Atlas A2 取证快照）

### npu-smi 五态健康摘要

[npu-smi 健康状态页](https://www.hiascend.com/doc_center/source/zh/HDK/2610/A2/A2npu/26.1RC1/npu-smi/npusmi_12_0050.html)（HDK 26.1.x，Atlas A2 文档树）把设备健康分为五态：OK / Warning / Alarm / Critical / UNKNOWN。其中 **UNKNOWN 表示设备不存在或未启动**，是覆盖性语义而不是故障严重度。两条边界：

- 设备是否“可恢复”不由该状态判定，由黑匣子错误码与《健康管理故障定义》共同判定；
- 官方明示恢复后健康状态回到 OK **不代表故障未发生，也不能证明后续运行无异常**——当前状态与已计数历史必须分列（见“五种含义的区分”一节）。

故障码引用必须带二进制版本：版本是“该问题是否已修复”的区分依据，不带版本的裸码不构成完整的健康证据。

### 黑匣子错误码最小集合（Atlas A2，文档版本 02）

[黑匣子错误码信息列表 02](https://www.hiascend.com/doc_center/source/zh/HDK/2610/A2/A2blackboxerrorcode/codelista2_01.html)（2026-08-19；2026-10-09 下载 xlsx 附件逐行解析）共 91 个数据行、13 列：错误码、错误名称、所属一级/二级模块、错误类型、错误级别、检测条件、错误影响、错误原因、系统自处理过程、修复建议、日志路径、错误信息。结构性事实：

- 码为十六进制事件码，**本身无单位**；数值阈值在《健康管理故障定义》而不在本表；
- 错误类型含 Host已恢复 / Device已恢复 / Device异常 / Device恢复 / Host异常——**故障与恢复是不同事件码**，配对出现但不一一对应；
- 错误级别为 提示/次要/重要/紧急；检测条件为 在线上报/复位后上报/检查上报——**复位后上报类事件在复位前的在线查询中不可见**；
- 日志路径列给出每个码的落盘位置，采集记录应保留该路径。

代表性最小集合（名称要点照录 xlsx，完整语义以原表行为准）：

| 错误码 | 名称要点 | 检测条件/类型 | 影响解释边界 |
|---|---|---|---|
| 0x68020002 | compute unit 虚焊风险预警（二级内存 SBE 计数超门限） | 计数阈值型 | 受影响 NPU 需恢复；阈值数值在故障定义文档而非本表 |
| 0x68020001 | 片外内存故障预警 | 事件码 | 官方影响表述为 NPU 无法继续训练、需下电换件——属高影响处置入口 |
| 0xA606000C | 名称见 xlsx；本行作检测前提示例 | 检测条件为“驱动加载后” | 检测前提随码而异：驱动未加载时该码不可能出现 |
| 0xB4060006 / 0xB4060007 | OS 繁忙 / OS 异常 | 事件码 | Host 侧状态事件，不是 NPU 器件故障证据 |
| 0xA6301002 | 片外内存动态页隔离失败 | 事件码 | 官方影响为可能反复出现片外内存故障 |
| 0xA6192D15 | 设备侧无法创建 mbx | **复位后上报** | 复位前的在线查询中不可见；时间线解释须考虑上报延迟 |
| 0xA6183207 / 0x96183207 | 过温预警 / 高温告警恢复 | 故障码与恢复码成对 | 配对码不表示所有故障码都有恢复码；恢复事件不等于无故障历史 |
| 0xA4183208 / 0xA4183209 | P2P 建链失败 / P2P 传输超时 | 事件码 | 跨卡归属：事件涉及两端 NPU，定位须结合拓扑 |
| 0xA8021000–0xA8021002 | HBM 故障恢复三连记 | 错误类型 Device已恢复 | “恢复”是独立事件码，不能与故障码互相抵消或合并 |

### 三套编码不可混排

昇腾侧至少有三套并行的码，命名相近但命名空间不同：

1. **黑匣子错误码**（上表）：设备/驱动事件与恢复事件；
2. **健康管理事件 0x80E2xxxx 族**（[健康管理故障定义 02](https://www.hiascend.com/doc_center/source/zh/HDK/2610/A2/A2healthmgmt/faultdefa2_02.html)，Atlas A2）：如 0x80E28007（AI CPU 调频异常）、0x80E2800D（HBM 介质 repair 失败）、0x80E2801B（RoCE 重传超时）、0x80E28025（AI CPU 超门限）。该族是健康管理框架的事件码，与黑匣子编码**不可混排互译**；同一芯片的错误码可在故障定义 xlsx 与黑匣子文档之间不一致，本文以各自 2026-10-09 快照为准，不做跨版本合并；
3. **DCMI API 返回码**（[dcmi_238](https://www.hiascend.com/doc_center/source/zh/HDK/2610/A2/A2DCMI/dcmi_238.html)，19 条 6 类）：执行成功（DCMI_OK=0）；入参/设备状态/环境异常（-8001 参数错误、-8003 内存接口操作失败、-8007 无效 device ID、-8008 设备不存在、-8023 配置信息不存在）；权限或功能不支持（-8002、-8013 容器中不支持、-8255 设备 ID/功能不支持）；超时重试（-8006 响应超时、-8012 尚未就绪、-8017 正在升级、-8020 资源被占用）；内部执行异常（-8004/-8005/-8009/-8010/-8011、-8015 复位失败、-8016 复位取消）。这些是 **API 调用返回码，描述检测链自身状态，不是设备故障码**；-8006/-8012/-8017/-8020 属“采样失败/暂不可读”而非设备故障证据；多数条目的处理建议为“联系华为工程师”，没有公开根因目录。

A3 说明：[Atlas A3 黑匣子错误码信息列表 02](https://www.hiascend.com/doc_center/source/zh/HDK/2610/A3/A3blackboxerrorcode/codelista3_01.html)与 [A3 健康管理故障定义 02](https://www.hiascend.com/doc_center/source/zh/HDK/2610/A3/A3healthmgmt/faultdefa3_02.html)本轮**仅作存在性核对**（确认文档存在），未下载逐行解析；A2 的码表不能外推 A3，引用 A3 具体码前须补解析。

## AMD：SMI/RAS 独立分支

AMD 侧证据链与 NVIDIA/昇腾均不同构，单列分支。来源为 [AMD SMI docs-10.1.0](https://rocm.docs.amd.com/projects/amdsmi/en/docs-10.1.0/index.html)（页面标题 AMD SMI 27.1.0，对应 ROCm Core SDK 10.1.0；许可证 MIT）、[AFID Event List（文档号 70122，v1.0）](https://docs.amd.com/r/en-US/AMD_Field_ID_70122_v1.0/AFID-Event-List)与[内核 v6.16 固定 commit 的 amdgpu RAS 文档](https://github.com/torvalds/linux/blob/038d61fd642278bab63ee8ef722c50d10ab01e8f/Documentation/gpu/amdgpu/ras.rst)。amd-smi 是 rocm_smi 的后继；CLI 输出是示例级接口，官方推荐 Python/C++ 库作为健壮数据源。本库未运行该工具。

### RAS 概念与 CPER

[conceptual/ras](https://rocm.docs.amd.com/projects/amdsmi/en/docs-10.1.0/conceptual/ras.html)：ECC 1-bit 错误由硬件纠错并记录；uncorrectable（2-bit）错误必须上报。错误经 CPER 上报，CPER 记录含 Error source、Error type、severity 与 Timestamp；severity 取值 0–3：0 Recoverable（non-fatal uncorrected）、1 Fatal、2 Corrected、3 Informational。AFID（AMD Field ID）是事件/错误的唯一数值 ID，每条 CPER 至多携带 12 个 AFID；AFID 是永久数值 ID，但官方明示 "do not always reveal the root cause"。

### ECC 计数：单位与采集前提

- `amd-smi metric -e` 输出 TOTAL_CORRECTABLE / TOTAL_UNCORRECTABLE / DEFERRED 等字段，`-k` 按 IP block 分解（[CLI 页](https://rocm.docs.amd.com/projects/amdsmi/en/docs-10.1.0/how-to/amdsmi-cli-tool.html)）；单位是**计数**，须记录采样窗口与重置边界，规则同本文前部的 DCGM 计数器；
- 内核侧（v6.16 ras.rst）：sysfs 只读计数 `/sys/class/drm/cardN/device/ras/<block>_err_count`，输出 `"ue: <count>"` / `"ce: <count>"`（ue=multi-uncorrectable，ce=single-correctable）；支持 RAS 的 block **因 ASIC 而异**，查 `/sys/module/amdgpu/parameters/ras_mask` 与 `.../ras/features`，不能按“Instinct 全系”概括；
- `amd-smi monitor -e/--ecc` 采样输出 SINGLE_ECC / DOUBLE_ECC / PCIE_REPLAY **错误计数**（官方参数描述："Monitor ECC single bit, ECC double bit, and PCIe replay error counts"）——这是**计数采样**，不是独立事件流；单次执行为一次快照，持续采集必须显式加 watch 参数（`-w/--watch <interval>`，可配 `-W/--watch_time`、`-i/--iterations`）。本文不给出已执行的持续采样示例；现场如需持续采样，示例形态为 `amd-smi monitor --ecc --watch 1`（未执行，须在目标平台验证输出与开销），并记录计数值、差值、采样窗口与重置边界——与真正的事件记录（如 CPER 上报）是不同证据。

### bad-pages 三态与持久化

`amd-smi bad-pages` 以 `-p`/`-r`/`-u` 分列三类页；内核侧 `/sys/class/drm/cardN/device/ras/gpu_vram_bad_pages` 每行为 `"gpu pfn : gpu page size : flags"`（十六进制），flags 为 **R=reserved / P=pending / F=unable to reserve**（v6.16 ras.rst）。pending（待处理）、reserved（已保留）与 unreservable（无法保留）是三种不同状态，不能与 NVIDIA retired pages 的 SBE/DBE/pending 三分直接对照。坏页列表持久化在 EEPROM（`ras_eeprom_reset` 清零）。

### AFID 15–34：五个 category 的最小集合

[AFID Event List 70122 v1.0](https://docs.amd.com/r/en-US/AMD_Field_ID_70122_v1.0/AFID-Event-List)（Table 1，2026-10-09 逐行复核）把 AFID 15–34 分为 5 个 category；severity 定义为 Corrected（硬件已纠正，仅供诊断）/ Fatal（触发设备复位恢复）/ Uncorrected Non-fatal（不可纠正但可遏制）/ ALL（前三者任一）：

| Category | 代表条目（AFID 号，Severity） | 边界 |
|---|---|---|
| Off-Package Link Errors | WAFL（15 Corrected、16 Fatal）、XGMI（17 Corrected、18 Fatal） | 封装间链路事件，不等于单卡器件故障 |
| HBM Errors | **Bad Page Retirement Threshold（19，Fatal）**、On-die ECC（20 Fatal、22 Uncorrected Non-fatal）、End-to-end CRC（21 Fatal、23 Uncorrected Non-fatal）、HBM All（24 Corrected）、HBM All Others（25 Fatal） | Bad Page Retirement Threshold 是阈值型事件（**AFID 19**，不是 22）；**阈值数值本文未取得**，不从码值推导未公开门限 |
| Device Internal Errors | Hardware Assertion（26，Fatal）、Watchdog Timeout（27，Fatal）、All Others（28 Uncorrected Non-fatal、29 Corrected、30 Fatal） | 设备内部检测事件；Fatal 的官方恢复路径含设备复位；All Others 三行按 severity 分列，均属本 category |
| CPER Format Errors | Malformed CPER（31，ALL）、Incomplete ACA Data（32，ALL）、Invalid ACA Data（33，ALL） | 上报通道自身的格式错误，属采集质量问题而非设备故障 |
| Unidentified Errors | Unidentified Error（34，ALL） | 未识别事件不可归因；本 category 只有 34 一行 |

文档明示 "not all events necessitate immediate attention or action … contact your service provider"——**没有公开的逐 AFID 处置/阈值表**，本文不仿照 Xid 目录编造处置动作。

### GPU reset 语义与影响范围核对

[conceptual/gpu-reset-behavior](https://rocm.docs.amd.com/projects/amdsmi/en/docs-10.1.0/conceptual/gpu-reset-behavior.html)与 [CLI 页 `amd-smi reset` 的 Warning](https://rocm.docs.amd.com/projects/amdsmi/en/docs-10.1.0/how-to/amdsmi-cli-tool.html)（2026-10-09 逐字复核）给出的影响范围**不止 XGMI hive**。复位前必须分别核对以下三项：

1. **XGMI hive**：在 XGMI/Infinity Fabric 系统上，复位一个 GPU 会复位同一 XGMI hive 内的所有 GPU；用 `amd-smi xgmi`/`amd-smi topology` 或 `/sys/class/drm/card*/device/xgmi_info/xgmi_hive_id` 确认 hive 成员。
2. **共享上游 PCIe switch 的复位域**：CLI Warning 明示 "resetting one GPU may trigger a **Secondary Bus Reset (SBR)** on the upstream switch port, affecting all GPUs behind the same switch, **independent of XGMI hive membership**"——共享上游 switch 的 GPU 即使不在同一 hive 内也可能被波及。
3. **持有 `/dev/kfd` 句柄的进程**：CLI Warning 明示 "Any process with an open `/dev/kfd` handle will be terminated when a GPU reset occurs, **even if that process is not using the GPU being reset**"，且 `ROCR_VISIBLE_DEVICES`/`HIP_VISIBLE_DEVICES` 不能阻止——这两个变量是用户态过滤器，"do not create a kernel-enforced isolation boundary"。

概念页另明示 "Do not assume that amd-smi reset --gpureset provides per-GPU fault containment inside an XGMI hive"，实际爆炸半径取决于 GPU 代际、复位方法、驱动路径、固件、PCIe 拓扑与流量模式；复位期间 KFD 可驱逐队列，应用须重建全部 GPU 状态。**授权确认、负载退出、证据保全与恢复安排必须与上述三项影响范围绑定**；无法确认影响范围（hive 成员、PCIe switch 拓扑、/dev/kfd 占用进程任一项不明）时，不得据 hive 清单推断复位是安全的。该页「Further reading」指向的内核侧 GPU recovery 独立文档不存在（链接与内容不符），此文档缺口如实保留。

这与 NVIDIA 的 reset 语义（Xid 154 枚举区分 GPU Reset Required 与 Node Reboot Required）、昇腾的“复位后上报”检测条件是**三种不同的 reset 语义，不可合并**（见下节）。

### N/A 三分与代际门控

amd-smi 把无值输出分为三类（[About N/A values](https://rocm.docs.amd.com/projects/amdsmi/en/docs-10.1.0/how-to/amdsmi-cli-tool.html)，2026-10-09 逐字复核），且要区分**字段级**与 **section（节）级**：

- **Not Applicable**（字段级）：该功能或参数不适用于当前硬件/配置（如无头计算卡的显示时钟、未分区 GPU 的分区详情）——对应未覆盖；
- **Not Available**（字段级）：此刻无法取回该信息，官方列出三种原因：硬件组件不上报该指标；当前 amdgpu 驱动版本不支持经 amd-smi-lib 查询该项；驱动报告的 `gpu_metrics` 版本比已装 AMD SMI 支持的更新（`gpu_metrics` 是带版本结构体，AMD SMI 需显式支持每个版本布局，ROCm 7.13 起支持 v1.9 动态布局后不再受此错配影响）——Not Available 本身只记录为**数据不可用**（此刻无法取回），不直接赋予失败类别；归类须联合支持说明、设备/驱动/库版本与调用状态判定：硬件不上报或驱动不支持查询属**覆盖边界**（不支持/不提供），查询本身失败属**采集失败**，`gpu_metrics` 版本解析错配**单独记录为解析错配**，原因不能确定时记 **unknown**——不得仅凭 N/A 归为采样失败或版本错配；
- **Empty Section**（节级）：节头显示 N/A 有两种官方情形——节内确实无条目（如 AI-NIC 的 `RDMA_DEVICES:` 在 `ionic_rdma` 未加载时为空），**或该节的查询失败、整节被 N/A 替代**（官方举例：`amd-smi static` 的 NIC/SMU/IFWI、`amd-smi firmware` 的 FW_LIST）。JSON 输出中空节为空对象；CSV 行为分两种情形——本次运行**所有设备**均不报告该节时，CSV **整组省略该节的列**（官方原文 "CSV drops the section's columns when no device in the run reports it"），仅**部分设备**缺失时才对这些设备**填 N/A**。因此 CSV 缺列与列内 N/A 是不同情形：缺列不能解释为零值、正常状态或「已覆盖」，须先区分整节省略还是单设备缺值。

因此 N/A 不能机械映射为「空结果」或「未覆盖」：字段级 N/A 要区分 Not Applicable 与 Not Available，节级 N/A 要区分「无条目」与「查询失败」；记录时保留原始输出与 API/调用状态，**不能确定原因时记 unknown**。代际门控示例：`monitor -V/--violation`（大写 `-V`，功耗/温度违例状态；注意小写 `-v` 是 `--vram-usage` 显存用量，两者不可混淆）仅 MI300 或更新型号支持。

### 内核接口与特权操作

v6.16 ras.rst 另记录：debugfs `ras_ctrl` 支持 disable/enable/inject（错误注入为特权操作，本库不执行）；unrecoverable error 时可用 `/sys/kernel/debug/dri/N/ras/auto_reboot` 配置自动重启系统（默认行为文档未给出）。`amd-smi ras --cper` 需 sudo（权限前提），`ras --afid` 为纯离线解析（无需驱动/GPU）——采集记录应注明所用通道与权限。

### 本分支不可覆盖项（如实保留）

- 逐 AFID 的处置动作与阈值：官方明示联系服务商，无公开表；
- 页退休（Bad Page Retirement）阈值数值；
- CPER 的保留条件（平台侧持久化策略未取证）；
- MI200 系列的字段级支持矩阵。

## 五种含义的区分：跨平台对照

“健康”在三个平台上分别由不同机制拼出。下表把五种含义各举一例；同一行的三列**不可互相换算**，只说明各平台用什么证据承载该含义。

| 含义 | NVIDIA 例 | Ascend 例 | AMD 例 |
|---|---|---|---|
| 错误事件 | Xid 48（DBE）内核日志事件 | 黑匣子 0x68020002（二级内存 SBE 计数超门限预警） | AFID 19 Bad Page Retirement Threshold（Fatal），经 CPER 上报 |
| 已计数历史 | DCGM ECC volatile/aggregate、retired pages 累计 | DCMI/npu-smi 的 ECC 当前与累计计数（见前文 DCMI 表） | `metric -e` TOTAL_CORRECTABLE/UNCORRECTABLE；sysfs `ue`/`ce` 计数；`monitor -e/--ecc` 的计数采样（非事件流） |
| 当前状态 | DCGM `Healthy`（已启用 watch 在观察窗内无 incident） | npu-smi `OK` | bad-pages 查询时刻无 pending/reserved 页（amd-smi 无单一健康字段） |
| 诊断失败 | DCGM diag 退出码 226（诊断报错）/205（需隔离） | DCMI 返回码 -8004/-8005/-8015/-8016（内部执行异常） | `ras --cper` 无 sudo 权限（执行前提不满足）；节级「整节查询失败被 N/A 替代」（官方举例 `amd-smi static` 的 NIC/SMU/IFWI、`amd-smi firmware` 的 FW_LIST）——仅凭字段级 Not Available 不归类为诊断失败，须按上节规则联合判定，原因未定记 unknown |
| 未覆盖 | 退出码 240 NOT_WATCHED / 242 NO_DATA | npu-smi `UNKNOWN`（设备不存在或未启动）；DCMI -8255（功能不支持）、-8013（容器中不支持） | N/A=Not Applicable；`monitor -V/--violation` 在非 MI300+ 上不可用；Empty Section 须区分「无条目」与「整节查询失败」，未定记 unknown |

厂商同名语义不合并：

- **healthy / OK**：DCGM `Healthy` 限定为“已启用 watch 在观察窗内未形成 incident”；npu-smi `OK` 是五态摘要之一，且官方明示恢复后的 OK 不代表故障未发生；amd-smi 没有等价单一字段，只能用各查询时刻的输出分别陈述。三者的覆盖范围、判定主体与重置条件各不相同。
- **reset**：NVIDIA 的 Xid 154 枚举把 GPU Reset Required 与 Node Reboot Required 区分为不同恢复动作，DCGM 退出码 237（DCGM_ST_RESET_REQUIRED）表示 GPU 需要复位这一设备状态；昇腾的“复位后上报”是检测条件（复位前在线不可见），DCMI -8015/-8016 是复位失败/取消的 API 返回；AMD 的 `amd-smi reset --gpureset` 在 XGMI 系统上波及整个 hive，且共享上游 PCIe switch 时复位域可超出 hive 边界、持有 /dev/kfd 句柄的进程可能被终止（见上节三项核对）。四种“reset”的作用域、可观测性与恢复语义都不同。

## 跨层时间线对齐：需求级证据、官方共存案例与未执行的匹配方法

### 需求级证据与官方共存案例

[OCP GPU & Accelerator RAS Requirements v1.0](https://www.opencompute.org/documents/ocp-gpu-and-accelerators-ras-requirements-1-0-final-pdf) §4.3 要求同一错误事件在带内（CPER）与带外（Redfish）双通道记录——这是**需求级**证据，说明双通道共存是设计意图，而非重复故障。

[DGX GB200 NVL72 2.0.0 Release Notes（Improvements）](https://docs.nvidia.com/dgx/dgxgb200nvl72-2-release-notes/improvements.html)（2026-10-07 更新）提供了双通道共存的官方实例：Release 1.3.10 第 07 条把 HBM SBE 的 RAS 日志侧上报默认关闭，原因是 "they are already reported via XIDs"——同一故障可在 BMC/CPER 通道与内核 Xid 通道各出现一次（旧版本或开启对应 BCT knob 时两侧各记录一条），**时间线合并必须去重**。同页相关条目：第 49 条 GPU Containment CPER 日志增强；第 56 条 GPU-Status CPER 经 Redfish 上报的 severity 从 fatal 改为 informational；第 87 条 BERT 错误漏报修复为按索引读取、支持消费多条 RAS 记录；以及 bmcweb 修复 CPER event severity 在 SSE 与 event log 两条路径处理不一致的问题——severity 随通道而异是官方修复过的真实缺陷类别，对齐时不能只取单通道的 severity。

### 未执行的匹配方法（以 Xid 79 为例）

三个平台均无可展示的完整端到端对齐案例，本节只给出**未执行**的匹配方法，以 Xid 79（"GPU has fallen off the bus"）为例：

1. 带内：`journalctl` 中的 `NVRM: Xid` 79 行及其前置 GPU GUID/PCI BDF 行，记录内核时钟时间戳；
2. 带外：同一窗口的 BMC SEL/Redfish 事件（记录字段、时钟偏差与丢失条件见[BMC、固件身份与跨层硬件事件](bmc-firmware-and-events.md)），注意 `EventTimestamp` 只承诺与 Redfish 服务时间一致；
3. 应用层：同一设备身份上的作业失败/重试时间戳；
4. 对齐：先按设备身份（GUID/BDF ↔ Redfish `OriginOfCondition` ↔ 节点资源档案）连接，再按显式记录的时钟源对齐时间；`EventGroupId` 不蕴含顺序；双通道命中按上节去重。

该方法未在任何真实设备上执行；没有实际日志前，不声称任何一次 Xid 79 与某条 BMC 事件同源。

## 高影响处置入口与现场授权

错误码到处置动作的官方链入口：NVIDIA 侧为 [GPU Node Triage](https://docs.nvidia.com/deploy/gpu-debug-guidelines/gpu-node-triage.html)（常见 Xid 动作表、Running DCGM Diagnostics、Running Field Diagnostics 三节）；昇腾侧为黑匣子错误码与《健康管理故障定义》的“系统自处理过程/修复建议”列（如 0x68020001 官方表述需下电换件）；AMD 侧 AFID 文档明示联系服务商，无公开处置表。

涉及节点级动作（隔离、下线、复位、返修、回服）时：

- 节点隔离与验收分诊流程见[节点验收与分诊](node-acceptance-triage.md)；
- 隔离/返修/回服的全生命周期流程见[节点选型、隔离返修、长期管理与退役](node-selection-and-lifecycle.md)（`hardware.node-selection-and-lifecycle`，T01-08）；
- BMC/固件层的配合动作（固件身份核对、SEL 导出、事件采集质量）见[BMC、固件身份与跨层硬件事件](bmc-firmware-and-events.md)。

本文所有文档引用不授予执行权限。主动诊断、设备复位（AMD 复位的影响范围含 XGMI hive、共享上游 PCIe switch 复位域与 /dev/kfd 句柄进程三项核对，见本文 AMD 分支）、节点隔离与返修的实际执行，以现场已有授权、影响范围确认与证据保全完成为前提。

## 已知证据缺口

- DCGM `latest` 页面与 `v3.3.9` 固定源码不是同一冻结版本；尚无与固定快照匹配的完整产品/插件支持矩阵。
- 未核对目标 GPU 型号、MIG/NVSwitch/ConnectX/CPU 实体、驱动、固件或实际字段可读性。
- MindCluster 固定源码没有在所引位置给出所有健康码的产品化说明，也不证明所有昇腾型号支持相同查询。
- MindX 页面与固定 MindCluster 快照没有同版本交集证据；PRBS 结果表还有未解决的内部冲突。
- 没有真实采样、事件、计数器、主动诊断、恢复验证或 RMA 结论。任何目标环境仍需单独建立版本、设备、覆盖和本地证据档案。
- iBMC 告警处理 05：本文引用的事件码条目（0x0100000D、0x56000019、0x0D000007、0x100000C3、0x1A000029、0x1A000011/0x1A00001B/0x1A00001D、0x1A000025、0x2C00000F、0x2C000063、0x0200000F）已于 2026-10-09 第二轮定向复核时取得事件类告警页原文（该页为 JS 渲染，此前两轮直接 curl 仅取得页面壳，本轮经渲染提取取得正文）并逐字核对含义、说明、影响与建议一致（核对明细以 [batch-14-bmc-firmware-sources.md](../../docs/research/batch-14-bmc-firmware-sources.md) 为准）；全册未引用条目不作完整性断言，该检索路径的稳定性不作保证。仍未取得的是**带外 iBMC 告警码（0x56 NPU 段等）与带内黑匣子/健康管理码之间的官方对应关系**——「告警条目取得情况」与「带外—带内映射取得情况」是两件事，两套码目前不能互译，映射保持 unknown。另按独立审阅第二轮结论标注证据链边界：上述事件码的含义/影响/建议为**编写者经渲染提取取得并逐字核对的记录**，独立审阅者两轮（2026-10-09）均未能取得该页原文、**未做独立核验**；相关内容不据此单独建立处置规则（处置以现场确认与厂商支持为准）。
- Atlas A3 黑匣子错误码 xlsx 与 A3 健康管理故障定义仅存在性核对，逐行内容未解析；A2 码表不能外推 A3。
- NVIDIA GPU Memory Error Management 仅核对目录结构；行重映射、动态页离线与 RMA 政策的正文条款未核对，具体阈值与条件未写入。
- AMD 分支不可覆盖项：逐 AFID 处置动作与阈值（官方明示联系服务商）、页退休阈值数值、CPER 保留条件、MI200 字段级矩阵；amd-smi「Further reading」指向的内核侧 GPU recovery 独立文档缺失。
- 跨层端到端时间线：三个平台均无可展示的完整对齐案例，本文的匹配方法未执行；DGX GB200 NVL72 的双通道去重条目是官方发布说明，不是本地对齐实例。
- 同一昇腾芯片的错误码可在故障定义 xlsx 与黑匣子文档之间不一致；本文以 2026-10-09 各快照为准，未做跨版本合并。

## 来源与更新范围

- [NVIDIA DCGM v3.3.9 固定源码](https://github.com/NVIDIA/DCGM/tree/b0ec3c624ea21e688b0d93cf9b214ae0eeb6fe52)：只用于本文引用的字段定义和固定实现边界；未构建或运行。
- [DCGM Health Monitoring](https://docs.nvidia.com/datacenter/dcgm/latest/learn/modules/health-monitoring.html)、[Diagnostics](https://docs.nvidia.com/datacenter/dcgm/latest/learn/modules/dcgm-diagnostics.html)与[Exporter Metrics](https://docs.nvidia.com/datacenter/dcgm/latest/reference/dcgm-exporter-metrics.html)：2026-09-30 核对的当前网页，可继续变化。
- [MindCluster v26.1.1 固定源码](https://github.com/Ascend/mind-cluster/tree/44385c13d7b1d87def35f1604e8be4d16de6ca4e)：只用于所引 DCMI 头文件和 Go 封装；未安装或运行。
- [MindX DL 6.0.RC2 `ascend-dmi`](https://www.hiascend.com/doc_center/source/zh/mindx-dl/60rc2/toolbox/ascenddmi/toolboxug_0020.html)：2026-09-29 核对资源影响、产品/版本条件和输出边界；没有执行页面中的检查。
- [NVIDIA XID Errors 文档集](https://docs.nvidia.com/deploy/xid-errors/analyzing-xid-catalog.html)：2026-09-09 版（2026-10-09 复核），核对 Introduction、Working with Xid Errors 与 Analyzing with the Xid Catalog 的目录结构、12 列中产品适用性列的含义、Guidance Classes，并重新逐行核对代表性条目及 Table 2（Xid 144-150 Decode，Subcode V1 <R575 / V2 ≥R575）；同源 Xid-Catalog.xlsx（55,673 字节）2026-10-09 下载交叉核对一致；目录持续滚动，引用须带观察日期。
- [DCGM Diagnostics User Guide](https://docs.nvidia.com/datacenter/dcgm/latest/user-guide/dcgm-diagnostics.html)：2026-10-08 观察的 latest 页面（2026-10-09 复核 Exit Codes 表），退出码 226 DCGM_ST_NVVS_ERROR、205 DCGM_ST_NVVS_ISOLATE_ERROR、242 DCGM_ST_NO_DATA、240 DCGM_ST_NOT_WATCHED、237 DCGM_ST_RESET_REQUIRED。
- [NVIDIA GPU Node Triage](https://docs.nvidia.com/deploy/gpu-debug-guidelines/gpu-node-triage.html)：官方处置链入口（常见 Xid 动作表、reset 能力矩阵、DCGM 套件 1–3、field diagnostic 的 RMA 地位），2026-10-09 复核可读取（HTTP 200）；`/deploy/gpu-node-triage/introduction.html` 同日实测 404。本文不复制其流程。
- [NVIDIA GPU Memory Error Management](https://docs.nvidia.com/deploy/a100-gpu-mem-error-mgmt/index.html)：2026-09-09 版，仅核对章节结构。
- [DGX GB200 NVL72 2.0.0 Release Notes（Improvements）](https://docs.nvidia.com/dgx/dgxgb200nvl72-2-release-notes/improvements.html)：2026-10-07 更新，引用时固定条目编号（07/49/56/87 等）。
- 华为 [npu-smi 健康状态页](https://www.hiascend.com/doc_center/source/zh/HDK/2610/A2/A2npu/26.1RC1/npu-smi/npusmi_12_0050.html)、[Atlas A2 黑匣子错误码信息列表 02](https://www.hiascend.com/doc_center/source/zh/HDK/2610/A2/A2blackboxerrorcode/codelista2_01.html)（xlsx 逐行解析）、[A2 健康管理故障定义 02](https://www.hiascend.com/doc_center/source/zh/HDK/2610/A2/A2healthmgmt/faultdefa2_02.html)、[DCMI 返回码 dcmi_238](https://www.hiascend.com/doc_center/source/zh/HDK/2610/A2/A2DCMI/dcmi_238.html)：HDK 26.1.x，Atlas A2 文档树，2026-10-09 核对；[A3 黑匣子 02](https://www.hiascend.com/doc_center/source/zh/HDK/2610/A3/A3blackboxerrorcode/codelista3_01.html)与 [A3 故障定义 02](https://www.hiascend.com/doc_center/source/zh/HDK/2610/A3/A3healthmgmt/faultdefa3_02.html)仅存在性核对。
- [AMD SMI docs-10.1.0](https://rocm.docs.amd.com/projects/amdsmi/en/docs-10.1.0/index.html)（27.1.0，MIT）：核对 conceptual/ras、conceptual/gpu-reset-behavior 与 how-to/amdsmi-cli-tool（2026-10-09 复核 monitor 参数表、reset Warning 三项影响范围、About N/A values 三分）；`latest` 与固定版本可能漂移，引用固定 docs-10.1.0。
- [AMD AFID Event List 70122 v1.0](https://docs.amd.com/r/en-US/AMD_Field_ID_70122_v1.0/AFID-Event-List)：核对 Table 1（AFID 15–34 逐行，2026-10-09 复核）与 severity 定义；无公开处置/阈值表。
- [Linux v6.16 固定 commit 的 amdgpu ras.rst](https://github.com/torvalds/linux/blob/038d61fd642278bab63ee8ef722c50d10ab01e8f/Documentation/gpu/amdgpu/ras.rst)：sysfs/debugfs 接口边界；未执行注入或复位操作。
- [OCP GPU & Accelerator RAS Requirements v1.0](https://www.opencompute.org/documents/ocp-gpu-and-accelerators-ras-requirements-1-0-final-pdf)：§4.3 带内带外双记录的需求级证据。
