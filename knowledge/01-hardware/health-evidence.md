---
id: hardware.health-evidence
title: 设备健康证据与检测边界
type: reference
domain: hardware
status: draft
platforms: [generic]
source_refs:
  - src.nvidia.dcgm-v3.3.9
  - src.nvidia.dcgm-health-monitoring-latest-2026-09-30
  - src.nvidia.dcgm-diagnostics-latest-2026-09-30
  - src.nvidia.dcgm-exporter-metrics-latest-2026-09-30
  - src.ascend.mind-cluster-v26.1.1
  - src.huawei.mindx-dl-60rc2-ascend-dmi-2026-09-29
updated_at: "2026-09-30"
summary: 区分设备健康摘要、错误事件、累计计数器、采样失败与未覆盖项，并分别说明 GPU DCGM 和 NPU DCMI/MindX 证据的适用边界。
related_ids:
  - hardware.index
  - hardware.resource-topology
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
  notes: "核对 DCGM v3.3.9 固定源码中的字段定义、当前 DCGM health/diagnostics/exporter 文档、MindCluster v26.1.1 固定 DCMI 接口与 Go 封装，以及 MindX DL 6.0.RC2 ascend-dmi 页面；未访问真实 GPU/NPU、执行查询或主动测试，也未验证任一型号和版本组合。"
---

# 设备健康证据与检测边界

## 范围与阅读方式

本文回答“设备健康证据实际说明了什么”。它提供统一的记录方法，再分别说明 NVIDIA GPU 的 DCGM 与昇腾 NPU 的 DCMI/MindX 资料。它不提供通用健康阈值、主动测试处方或本地验收结论。

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

## 已知证据缺口

- DCGM `latest` 页面与 `v3.3.9` 固定源码不是同一冻结版本；尚无与固定快照匹配的完整产品/插件支持矩阵。
- 未核对目标 GPU 型号、MIG/NVSwitch/ConnectX/CPU 实体、驱动、固件或实际字段可读性。
- MindCluster 固定源码没有在所引位置给出所有健康码的产品化说明，也不证明所有昇腾型号支持相同查询。
- MindX 页面与固定 MindCluster 快照没有同版本交集证据；PRBS 结果表还有未解决的内部冲突。
- 没有真实采样、事件、计数器、主动诊断、恢复验证或 RMA 结论。任何目标环境仍需单独建立版本、设备、覆盖和本地证据档案。

## 来源与更新范围

- [NVIDIA DCGM v3.3.9 固定源码](https://github.com/NVIDIA/DCGM/tree/b0ec3c624ea21e688b0d93cf9b214ae0eeb6fe52)：只用于本文引用的字段定义和固定实现边界；未构建或运行。
- [DCGM Health Monitoring](https://docs.nvidia.com/datacenter/dcgm/latest/learn/modules/health-monitoring.html)、[Diagnostics](https://docs.nvidia.com/datacenter/dcgm/latest/learn/modules/dcgm-diagnostics.html)与[Exporter Metrics](https://docs.nvidia.com/datacenter/dcgm/latest/reference/dcgm-exporter-metrics.html)：2026-09-30 核对的当前网页，可继续变化。
- [MindCluster v26.1.1 固定源码](https://github.com/Ascend/mind-cluster/tree/44385c13d7b1d87def35f1604e8be4d16de6ca4e)：只用于所引 DCMI 头文件和 Go 封装；未安装或运行。
- [MindX DL 6.0.RC2 `ascend-dmi`](https://www.hiascend.com/doc_center/source/zh/mindx-dl/60rc2/toolbox/ascenddmi/toolboxug_0020.html)：2026-09-29 核对资源影响、产品/版本条件和输出边界；没有执行页面中的检查。
