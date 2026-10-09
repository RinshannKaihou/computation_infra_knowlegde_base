---
id: hardware.power-thermal-evidence
title: 供电、散热与性能退化证据
type: reference
domain: hardware
status: draft
platforms: [generic]
source_refs:
  - src.nvidia.dcgm-v3.3.9
  - src.nvidia.dcgm-exporter-metrics-latest-2026-09-30
  - src.nvidia.dcgm-field-identifiers-latest-2026-09-30
  - src.nvidia.dcgm-health-monitoring-latest-2026-09-30
  - src.nvidia.dcgm-diagnostics-latest-2026-09-30
  - src.nvidia.nvidia-smi-docs-latest-2026-09-30
  - src.nvidia.dgx-h100-h200-user-guide-2026-01-26
  - src.huawei.atlas-800t-a2-product-2026-09-29
  - src.ascend.mind-cluster-v26.1.1
  - src.huawei.npu-smi-atlas-a2-edge-24.1.rc1-pdf
  - src.huawei.hdk-26.1x-a2-npu-smi-2026-10-08
  - src.huawei.hdk-26.1x-a2-dcmi-low-power-2026-10-08
  - src.huawei.hdk-26.1x-a2-health-fault-def-02-2026-10-08
  - src.huawei.hdk-26.1x-a3-npu-smi-2026-10-08
  - src.usenix.superbench-atc24
updated_at: "2026-10-09"
summary: 供电/散热异常经降频、降速与冗余降额表现为性能退化；汇总 GPU 降频位图、violation 计数、健康与主动诊断边界、整机电源散热规格，以及训练 NPU（HDK 26.1.x）npu-smi 读数、DCMI 当前降频原因、历史事件与设施/BMC/设备关联方法。
related_ids:
  - hardware.health-evidence
  - hardware.resource-topology
  - hardware.rack-power-cooling-and-failure-domains
  - reliability.dimensions-and-failure-domains
  - training.slow-rank-triage
verification:
  status: source_checked
  evidence_refs:
    - src.nvidia.dcgm-v3.3.9
    - src.nvidia.dcgm-health-monitoring-latest-2026-09-30
    - src.nvidia.dcgm-diagnostics-latest-2026-09-30
    - src.nvidia.dgx-h100-h200-user-guide-2026-01-26
    - src.huawei.atlas-800t-a2-product-2026-09-29
    - src.ascend.mind-cluster-v26.1.1
    - src.huawei.hdk-26.1x-a2-npu-smi-2026-10-08
    - src.huawei.hdk-26.1x-a2-dcmi-low-power-2026-10-08
    - src.huawei.hdk-26.1x-a2-health-fault-def-02-2026-10-08
  notes: "核对 DCGM v3.3.9 固定源码的字段与判定、DCGM/nvidia-smi latest 文档（可变）、两机型规格、MindCluster npu-exporter 固定源码；2026-10-08 编写者核对训练线 npu-smi 与故障定义 xlsx，独立审阅者未取得 xlsx。2026-10-09 补核 A2 DCMI LP 原因位图及 GPU power 遥测不可读分支。未执行任何设备查询、诊断或压测。"
---

# 供电、散热与性能退化证据

供电或散热异常很少直接报“电源坏了/风扇坏了”。它们在计算层的典型表现是**性能退化**：硬件自保机制降低频率或功耗，或整机进入冗余降额运行。本页汇总这类退化的观测证据：字段语义、覆盖边界与机型规格。被动健康证据的通用边界见[设备健康证据与检测边界](health-evidence.md)；因降速导致个别 rank 变慢的排查见[慢 rank 诊断](../06-training/slow-rank-triage.md)。

`generic` 表示证据分类方法通用；具体字段名、单位和阈值按平台与版本分别核对，GPU 字段不能照搬到 NPU。

## 退化路径与证据分层

| 层 | 机制 | 可观测证据 | 不能推出什么 |
|---|---|---|---|
| 供电异常（PSU 失效、功率上限、供电不稳） | 冗余降额运行、power brake、功率封顶 | 当前 clock event 位图、violation 累计、功耗读数、整机告警 | 具体哪路 PSU 或供电元件故障（需 BMC/硬件日志） |
| 散热异常（风扇、风道、环境热点） | 热降频（SW/HW thermal slowdown） | 温度读数、热 violation 增量、时钟降档 | 故障风扇或风道的物理定位（需硬件层证据） |
| 自保降频/降速 | 频率、电压、功耗被限制 | 时钟 gauge 下降 + 对应 reason bit 置位 | 降频的根因（需结合上下文分支） |
| 冗余掩盖 | 性能已降但无报警 | 见[静默错误与灰色退化](../08-reliability/silent-errors-and-integrity.md)的掩盖讨论 | “无告警 = 无退化” |

## GPU 侧：降频事件位图与累计计数（固定 DCGM v3.3.9）

降频原因以**位图字段**暴露（`DCGM_FI_DEV_CLOCK_THROTTLE_REASONS`，ID 112，[dcgm_fields.h L480–482](https://github.com/NVIDIA/DCGM/blob/b0ec3c624ea21e688b0d93cf9b214ae0eeb6fe52/dcgmlib/dcgm_fields.h#L480-L482)），语义是**当前正在发生**；nvidia-smi 文档明确 “If all event reasons are returned as 'Not Active' it means that clocks are running as high as possible.”（[nvidia-smi 文档](https://docs.nvidia.com/deploy/nvidia-smi/index.html)，latest 可变页）。

位定义（[dcgm_fields.h L107–154](https://github.com/NVIDIA/DCGM/blob/b0ec3c624ea21e688b0d93cf9b214ae0eeb6fe52/dcgmlib/dcgm_fields.h#L107-L154)）：

| 位 | 含义（头文件注释归纳） |
|---|---|
| GPU_IDLE (0x1) | 空闲（注释称未来版本可能移除） |
| CLOCKS_SETTING (0x2) | 时钟受应用时钟设置限制 |
| SW_POWER_CAP (0x4) | 软件功率封顶算法把时钟压到请求值以下 |
| HW_SLOWDOWN (0x8) | 温度过高、外部 Power Brake 断言或 Fast Trigger 降压 |
| SYNC_BOOST (0x10) | Sync Boost 组内平衡 |
| SW_THERMAL (0x20) | GPU 超最大工作温度或显存超温 |
| HW_THERMAL (0x40) | 过热，核心频率降 2 倍或以上 |
| HW_POWER_BRAKE (0x80) | 外部 Power Brake 断言（如系统电源） |
| DISPLAY_CLOCKS (0x100) | 显示时钟（nvidia-smi 文档注明仅 Volta 设备支持该 reason） |

**历史累计**由 violation 计数器承载（POWER/THERMAL/SYNC_BOOST/BOARD_LIMIT/LOW_UTIL/RELIABILITY_VIOLATION，ID 240–245，[L666–693](https://github.com/NVIDIA/DCGM/blob/b0ec3c624ea21e688b0d93cf9b214ae0eeb6fe52/dcgmlib/dcgm_fields.h#L666-L693)）。**单位跨版本冲突，引用必须固定版本**：v3.3.9 头文件注释为 usec；DCGM master（2026-09-30 观察）注释为 ns；nvidia-smi 文档的 counters 写 microseconds。命名也在演变：v3.3.9 用 `CLOCK_THROTTLE_REASONS`，master 主名已改为 `CLOCKS_EVENT_REASONS`（旧名别名标记 Deprecated），nvidia-smi 在 v525→v530 改名后为兼容又加回旧名。

采集侧的两个默认陷阱：

- **exporter 默认不导出降频信号**：shipped 默认指标只有时钟/温度/功耗 gauge；violation 计数器与 `DCGM_EXP_CLOCK_EVENTS_COUNT/TOTAL` 在可选区（注释掉），需显式开启。默认部署下“看不到降频”是配置结果，不是无降频的证据。
- `DCGM_EXP_CLOCK_EVENTS_COUNT` 计的是**窗口内 bit 为 active 的样本记录数**（受采集频率影响，不是独立事件数）；`TOTAL` 计 inactive→active 跳变，重启/hot reload 即清零。

## 健康监测与主动诊断的边界

DCGM 的热/电源 watch（选择子 `t`）是**被动**机制，即不启动专用测试负载（[health-monitoring](https://docs.nvidia.com/datacenter/dcgm/latest/learn/modules/health-monitoring.html)，latest 可变）。规则须按版本和实体区分。固定 v3.3.9 的 **GPU thermal violation 分支**用升序 `GetSamples(startTime, endTime)` 取得范围内起始样本，再用 `GetLatestSample` 取得该实体的最新 `THERMAL_VIOLATION` 样本，比较两值的非零差值；后一次调用不传 `endTime`，**不保证末样本落在指定历史查询上界内**。`startTime` 未指定时设为当前时间减一分钟，不代表实际两样本严格相隔一分钟；该 watch 最小采样间隔为 30s。关联历史事件时须核对实际样本时间戳，不能仅凭请求的窗口归属 WARN；样本时间未知时保留归属未知。这一分支不直接判断温度绝对值或趋势，不能外推到整个健康模块（[MonitorThermal L1550–1609](https://github.com/NVIDIA/DCGM/blob/b0ec3c624ea21e688b0d93cf9b214ae0eeb6fe52/modules/health/DcgmHealthWatch.cpp#L1550-L1609)）。

**GPU power 分支**的 `POWER_VIOLATION` 两端样本分别用同一 `startTime/endTime` 范围内升序、降序 `GetSamples` 取得，与上述 thermal 末端取样方式不同（[MonitorPower L1643–1687](https://github.com/NVIDIA/DCGM/blob/b0ec3c624ea21e688b0d93cf9b214ae0eeb6fe52/modules/health/DcgmHealthWatch.cpp#L1643-L1687)）。此外它读取当前 `DCGM_FI_DEV_POWER_USAGE`：仅在取样返回 `DCGM_ST_OK`、值为 blank 且不是 `DCGM_FP64_NOT_SUPPORTED` 时，产生 `DCGM_FR_POWER_UNREADABLE` WARN；这不能解释为已发生功率节流，也不表示任意查询失败都会触发该 WARN（[L1629–1639](https://github.com/NVIDIA/DCGM/blob/b0ec3c624ea21e688b0d93cf9b214ae0eeb6fe52/modules/health/DcgmHealthWatch.cpp#L1629-L1639)）。同文件另有 CPU 温度阈值监测路径。解释健康结果时须记录实体、规则、请求窗口、实际样本时间及具体 incident/error code，不能仅凭 WARN 或 watch 名称归因。

官方对 Healthy 的限定（[health-monitoring 页](https://docs.nvidia.com/datacenter/dcgm/latest/learn/modules/health-monitoring.html)，latest 可变）：

> A Healthy result means that no enabled health rule found an incident in the retained data. It does not mean that every subsystem was watched or that an active stress test passed.

主动诊断中与电源/散热相关的测试：`targeted_power`（达不到请求的功率阈值，或持续功率负载下出错）、`pulse_test`（电流/功率需求快速变化暴露供电不稳）、`diagnostic` 插件覆盖 thermal excursions（[dcgm-diagnostics 页](https://docs.nvidia.com/datacenter/dcgm/latest/learn/modules/dcgm-diagnostics.html)）。同页明确：诊断不修复故障、不替代离线现场诊断、不决定 RMA；失败可源于 host、权限、库、拓扑、冷却、供电或负载干扰；侵入性测试只能在可移出服务的资源上运行。由“失败可源于环境”可推断其反面同样成立：通过也不证明测试窗口外的冷却/供电没有问题——这是本库的推论，不是页面原文。

## 整机规格（两个固定机型例子）

| 机型 | 电源 | 散热 | 降额/边界 |
|---|---|---|---|
| NVIDIA DGX H100/H200（指南 2026-01-26） | 6×3.3kW PSU，4+2 冗余；≥3 个 PSU 才能开机；系统输入 200–240V AC、10.2kW max | 气流 1105 CFM（80% fan PWM）、38,557 BTU/hr、工作温度 5–30°C | 官方原文：“If three PSUs lose power … the system continues to function, but at a **reduced performance level**.”——供电异常可表现为性能降级而非宕机 |
| Atlas 800T A2（产品页 2026-09-30 观察，可变网页） | 4×2.6kW 热插拔电源模块，2+2 冗余 | 8 个热插拔风扇模组 N+1 冗余、风冷、工作温度 5–35°C | 页面未给 NPU 数量、设备内存或降额行为说明，不能补写 |

环境差异的真实案例：SuperBench 记录同一数据中心内不同机架/机架内不同位置的温度差异，而 GPU 散热设计相同，温暖位置的 GPU 可能 thermal throttling；热带数据中心中 BER>10⁻¹² 的缺陷 IB 链路**数量**多 35 倍（[§2.1，印刷页 837](https://www.usenix.org/system/files/atc24-xiong.pdf#page=3)）。这些是 Azure 特定观察，用于说明环境差异的存在性，不构成通用阈值。

## NPU 侧观测（昇腾训练产品线，HDK 26.1.x）

训练产品线的版本化 npu-smi 文档位于 HDK 文档树（《Atlas A2 npu-smi命令参考》，HDK 26.1.x，URL 路径 2610），其逐命令支持矩阵显式包含 Atlas 800T A2 训练服务器与 Atlas 900 A2 PoD 集群基础单元（另含 800I A2、200T A2 Box16 等）。本批逐页核对后的字段证据：

| 观测 | 命令与字段（HDK 26.1.x） | 单位 | 边界 |
|---|---|---|---|
| 温度 | `npu-smi info -t temp -i id [-c chip_id]` → NPU Temperature；MCU 芯片另有 LM75A_TE/LM75B_TE（进/出风口温度）（[npusmi_0023](https://www.hiascend.com/doc_center/source/zh/HDK/2610/A2/A2npu/npusmi_0023.html)） | °C | 高温门限具体 °C 值文档未给 |
| 功耗 | `npu-smi info -t power` → NPU Real-time Power（[npusmi_0025](https://www.hiascend.com/doc_center/source/zh/HDK/2610/A2/A2npu/npusmi_0025.html)） | W | 无功率上限/封顶类设置命令 |
| 电压 | `npu-smi info -t volt` → Voltage（[npusmi_0027](https://www.hiascend.com/doc_center/source/zh/HDK/2610/A2/A2npu/npusmi_0027.html)） | V | 训练服务器不支持查 MCU 电压 |
| 频率 | Aicore Freq（输出说明仅称「Aicore频率」）与 Aicore curFreq（「Aicore当前频率」）成对出现，同屏含 Aicore Usage Rate、Temperature、NPU Real-time Power（[npusmi_0016](https://www.hiascend.com/doc_center/source/zh/HDK/2610/A2/A2npu/npusmi_0016.html)） | MHz | 页面未把 Freq 定义为标称值或任何降频判定阈值；其示例本身给出 利用率 0、Freq 1850、curFreq 800——空闲时 curFreq 同样走低，curFreq 低于 Freq **不能单独**判定热/功耗节流，须结合同窗口负载、温度与功耗 |
| 周期监测 | `npu-smi info watch` 表头：Pwr、Temp、AI Core、AI Cpu、Ctrl Cpu、Memory、Memory BW、NPU Util、AI Cube（[npusmi_0012](https://www.hiascend.com/doc_center/source/zh/HDK/2610/A2/A2npu/npusmi_0012.html)） | W/°C/% | 开 profiling 时 AI Core(%) 返回 0（页内注明） |
| 传感器 | `npu-smi info -t sensors -c chip_id` → Soc Max/SFP/NDIE/HBM Temperature（[npusmi_0039](https://www.hiascend.com/doc_center/source/zh/HDK/2610/A2/A2npu/npusmi_0039.html)）；内存信息含 HBM Temperature、HBM Clock Speed 当前值（[npusmi_0019](https://www.hiascend.com/doc_center/source/zh/HDK/2610/A2/A2npu/npusmi_0019.html)） | °C/MHz | — |
| 健康 | `npu-smi info -t health` → OK/Warning/Alarm/Critical/UNKNOWN 五态；指定芯片显示 Error Code/Error Information，页面指引查《健康管理故障定义》（[npusmi_0029](https://www.hiascend.com/doc_center/source/zh/HDK/2610/A2/A2npu/npusmi_0029.html)）；`-c chip_id` 最多查最近 8 次 RAS Event ID | — | Error Code 的权威解释在故障定义 xlsx |

**降频机制（事件级证据）**：同版本《健康管理故障定义 02》xlsx（[hma2_01.html](https://www.hiascend.com/doc_center/source/zh/HDK/2610/A2/A2healthmanagement/hma2_01.html) 附件）给出两条官方事件描述——0x80E20207「SOC 非致命高温异常告警（不含 DDR/HBM 颗粒）」：LPM 10ms 轮询 SOC Tsensor，自处理含「系统调节 AIcore 频率进行温控」，迟滞 5°C（降到阈值下 5°C 才恢复/再报），业务影响「通常业务性能受损」，建议可继续训练或存 ckpt 复位；0x80E21007「主电源过流告警」：「SOC ACG（或者 POWERBRAKE，以产品分表为准）模块触发快速降频」，瞬态过流无需处理。关联事件还有 0x80E21008（EDP 降电流手段用完仍失控）、0x80E24E00（LPM 心跳异常，温保/EDP/AVS/PMU 全失效）、0x80E39200（Tsensor 异常）、0x80E3A201（DVFS 功能异常）。事件获取途径：msnpureport 收集 device-os slog 搜 event_id。**阈值数值与 ACG/POWERBRAKE 产品分表未公开。**

**npu-smi 页面范围内的负面确认**：在编写者扫描的 HDK 26.1.x A2 npu-smi 命令页（npusmi_0002–0181 的存在页）中未找到当前降频原因位图；这只描述该组命令页，不能推断整个训练 NPU 平台没有此能力。`info -h` 类型清单（[npusmi_0008](https://www.hiascend.com/doc_center/source/zh/HDK/2610/A2/A2npu/npusmi_0008.html)）含 `pwm-mode`、`pwm-duty-ratio`、`cpu-freq-up` 等，但无逐类型支持矩阵，类型出现不证明训练机型支持，各类型命令页的矩阵未逐条核对。Freq/curFreq 是读数证据，健康查询和 device-os 日志是事件证据；它们不能替代下述当前原因查询。

**DCMI 当前降频原因**：同版本 A2 文档公开 `dcmi_get_device_info` 的 `DCMI_MAIN_CMD_LP` / `DCMI_LP_SUB_CMD_AICORE_FREQREDUC_CAUSE` 路径，返回 8Byte（`unsigned long long`）的 64 位原因位图，每 100ms 更新，**不提供历史查询**（[dcmi_077 约束及表 1–3](https://www.hiascend.com/doc_center/source/zh/HDK/2610/A2/A2DCMI/dcmi_077.html)）。表 2 定义：IDLE bit 0（空闲节能）、THERMAL bit 2（温控）、SW_EDP bit 3（软件限流）、HW_EDP bit 4（瞬态过流快速降频）、POWER_BREAK bit 5（主板功率上限）、SVFD bit 8（供电不稳）、POWERCAPPING bit 10（iBMC 功耗控制）；`POWER_BREAK` 保留上游拼写。多个位可同时置位，**IDLE 不等于故障节流**，任意置位也不能直接定位故障；这些位不与 NVIDIA 逐位等价。

该页表 3 对 Atlas 800T A2、Atlas 900 A2 PoD 的裸机 root、裸机运行用户组非 root、普通容器 root、AVI 容器 root 四种场景均列 Y；未列的虚拟机、其他权限、版本及产品场景保留未知。本文只说明文档接口，未调用 DCMI；应用前须核对实际机型、配套版本、部署方式和权限。当前原因、频率/负载、历史健康事件及设施日志应分别采集，不能用一次当前位图查询证明过去未发生降频。

降P启动是管理性隔离/降额启动，不是温度/供电异常的自保动作，不要与降频混淆。适用形态与查询途径按官方页逐字区分（[npusmi_0177](https://www.hiascend.com/doc_center/source/zh/HDK/2610/A2/A2npu/npusmi_0177.html)、[npusmi_0178](https://www.hiascend.com/doc_center/source/zh/HDK/2610/A2/A2npu/npusmi_0178.html)、[npusmi_0099](https://www.hiascend.com/doc_center/source/zh/HDK/2610/A2/A2npu/npusmi_0099.html)）：仅服务器形态产品（含 HCCS 款和 PCIe 款）支持降P启动，推理卡和训练卡（标卡）暂不支持；查询方法 1 为 msnpureport 收集 Device 侧日志，方法 2 为 iBMC `ipmcget -d npustatus`；**HCCS 款两种方法均有效，PCIe 款只支持方法 1（方法 2 查询无效）**；设置经 iBMC `ipmcset -d npuisolation -v <id> 1`（1=NPU 隔离即降P启动）；降P启动的 NPU 支持单 NPU 复位，正常启动的不支持。「iBMC 查不到」不等于「没有降P」。

**采集侧**：MindCluster v26.1.1 的 npu-exporter 有温度、功耗、电压、AICore 频率、健康状态指标（`npu_chip_info_temperature/power/voltage/aicore_current_freq/health_status`，[collector_for_npu.go L64–70](https://github.com/Ascend/mind-cluster/blob/44385c13d7b1d87def35f1604e8be4d16de6ca4e/component/npu-exporter/collector/metrics/collector_for_npu.go#L64-L70)），采集组默认开启、5 秒间隔。边界：温度、功耗、电压指标的 help 字符串不含单位与口径；`aicore_current_freq` 的 help 注明 MHz；Ascend310P 有「用整卡功耗替代芯片功耗」的特例注释，其他型号口径未核对；exporter 没有降频原因类指标。exporter 字段与 HDK 26.1.x npu-smi 字段的逐条对应关系未核对，不默认等价。

**历史记录**：早期批次仅核对了边缘/推理产品线文档（Atlas 200I A2/500 A2 智能边缘硬件 24.1.RC1 npu-smi 命令参考 PDF，且只核对了目录），训练产品线证据长期缺失；本批（2026-10-08）在 HDK 26.1.x 树取得训练线证据，边缘线文档仍不可外推训练型号，两条产品线的字段差异未逐条比对。A3 线（Atlas 800T A3 超节点、900 A3 SuperPoD 等）存在同构文档（[npusmia3_0023](https://www.hiascend.com/doc_center/source/zh/HDK/2610/A3/A3npu/npusmia3_0023.html) 抽查）与故障定义 02（存在性核对，未逐行解析）。

## 设施/BMC/驱动/应用证据的最小关联

同一节点时间线中，供电/散热问题需要跨层证据对齐才能归因。最小关联表（NPU 训练服务器例；GPU 侧对应字段见上文 DCGM 节）：

| 层 | 证据来源 | 本页已核对的字段/事件 | 不能单独推出什么 |
|---|---|---|---|
| 设施/机柜 | rPDU 遥测、Redfish PowerSupply/EnvironmentMetrics/CoolingUnit（见[机柜供电、散热预算与共享依赖](rack-power-cooling-and-failure-domains.md)） | 供电路径容量、功耗、进风温度、液冷供/回液温度与流量（schema 模型） | 机柜正常 ≠ 单节点正常；schema 有字段 ≠ 设备已实现 |
| BMC/带外 | iBMC `ipmcget -d npustatus`（仅 HCCS 款有效，PCIe 款无效）、MCU LM75A/B 进出风温度（npusmi_0023/0177/0178） | 降P 状态（HCCS 款）、进/出风口温度 | BMC 无告警 ≠ 无降额运行；PCIe 款查不到 ≠ 无降P |
| 设备（npu-smi） | 上表温度/功耗/电压/频率/健康字段 | Aicore curFreq 与 Aicore Freq 的读数差异、健康五态、最近 8 次 RAS Event ID | 频率差异也可由空闲/策略产生，非单独判据；当前读数与历史事件分开 |
| 设备（DCMI） | `DCMI_MAIN_CMD_LP` / `DCMI_LP_SUB_CMD_AICORE_FREQREDUC_CAUSE`（dcmi_077） | 当前 64 位原因，每 100ms 更新 | 无历史查询；IDLE 不是故障；接口支持和现场可用性须分别核对 |
| 驱动/OS | msnpureport 收集的 device-os slog | 0x80E20207（高温→AIcore 频率温控）、0x80E21007（过流→ACG/POWERBRAKE 快速降频）等事件 | 事件是机制描述与历史记录，不是实时降频证明 |
| 应用 | 训练侧 step 时间、慢 rank 证据（见[慢 rank 诊断](../06-training/slow-rank-triage.md)） | 性能退化窗口 | 应用退化不能反向单独证明供电/散热根因 |

对齐方法：跨时钟域（BMC、主机、设备、应用）比较绝对先后，前提是有时钟校准或误差界估计；本页未核对 BMC 与主机的时钟偏差，**在偏差未知时不做跨层「最早异常」排序**——只按稳定身份（设备 ID、Event ID、作业 ID）与逻辑关联键串联证据，或在各自时钟域内比较顺序，跨层先后与因果方向保留未知（时间线纪律见[证据与假设](../08-reliability/evidence-and-hypotheses.md)：没有偏移估计与不确定度时，不得把时间先后写成因果顺序）。例如在同一时钟域内取得「0x80E21007 事件 + curFreq 下降 + 同窗口功耗/温度异常 + 训练 step 变长」构成供电异常导致退化的支持证据链；仅「step 变长」或仅「curFreq 下降」（空闲或策略限制也可产生）都不构成。官方来源事件（上两条）是机制定义而非本站现场告警；本文不虚构现场告警案例。

## 常见误解

- **“温度正常 = 没有降频”**：GPU 当前原因位图、历史 violation 与温度读数是不同证据；v3.3.9 GPU thermal violation 分支不直接判断温度，GPU power 另有遥测不可读分支。WARN 须看具体错误码；DCGM exporter 默认不导出上述降频信号。
- **“Healthy = 无热/电源问题”**：官方定义只覆盖已启用规则与保留样本（见上）。
- **“violation 数字可以跨工具直接比较”**：单位在 v3.3.9（usec）、master（ns）、nvidia-smi 文档（microseconds）之间不一致。
- **“PSU 失效会立刻宕机”**：冗余设计下单路失效首先是冗余降级；DGX 官方的 “reduced performance level” 条款针对三个 PSU 失效的更重情景，失效数量与接线决定后果。
- **“GPU 的降频字段可以套到 NPU”**：A2 DCMI 有独立的当前原因位图和支持矩阵；npu-smi 频率/健康字段、历史事件与 exporter 是其他观测路径。DCMI 不提供历史原因查询，IDLE 置位及 curFreq 降低均不直接等于热/功耗故障；不默认与 NVIDIA 字段或 exporter 指标等价。
- **“npu-smi 文档支持矩阵有训练型号 = 已实测该机型”**：支持矩阵是文档声明；本文所有 NPU 字段均为网页/附件证据，未在任何真实设备执行。
- **“降P启动 = 供电/温度异常触发的降频”**：降P是管理性隔离/降额启动（iBMC 设置），与 0x80E21007 这类事件级快速降频机制不同。

## 来源与待确认问题

- [DCGM v3.3.9 固定源码](https://github.com/NVIDIA/DCGM/tree/v3.3.9)：位图、violation、watch 判定（注意 GitHub Web UI 对裸 commit 页面 404，tag 与 raw 链接可用）。
- [DCGM exporter 指标页](https://docs.nvidia.com/datacenter/dcgm/latest/reference/dcgm-exporter-metrics.html)、[字段定义页](https://docs.nvidia.com/datacenter/dcgm/latest/dcgm-api/dcgm-api-field-ids.html)、[health monitoring](https://docs.nvidia.com/datacenter/dcgm/latest/learn/modules/health-monitoring.html)、[diagnostics](https://docs.nvidia.com/datacenter/dcgm/latest/learn/modules/dcgm-diagnostics.html)、[nvidia-smi](https://docs.nvidia.com/deploy/nvidia-smi/index.html)：均为 latest 可变页，2026-09-30 观察。
- [DGX H100/H200 用户指南](https://docs.nvidia.com/dgx/dgxh100-user-guide/introduction-to-dgxh100.html)、[Atlas 800T A2 产品页](https://e.huawei.com/cn/products/computing/ascend/atlas-800t-a2)、[MindCluster v26.1.1](https://github.com/Ascend/mind-cluster/tree/44385c13d7b1d87def35f1604e8be4d16de6ca4e)、[npu-smi 边缘线命令参考](https://www.hiascend.com/doc_center/source/zh/Atlas%20200I%20A2/24.1.RC1/re/npu/Atlas%20A2%20智能边缘硬件%2024.1.RC1%20npu-smi%20命令参考%2001.pdf)、[SuperBench](https://www.usenix.org/conference/atc24/presentation/xiong)。
- [Atlas A2 npu-smi命令参考（HDK 26.1.x）](https://www.hiascend.com/doc_center/source/zh/HDK/2610/A2/A2npu/npusmi_0007.html) 与[健康管理故障定义 02（xlsx）](https://www.hiascend.com/doc_center/source/zh/HDK/2610/A2/A2healthmanagement/hma2_01.html)：训练线温度/功耗/电压/频率字段、健康五态、降频机制事件；[A3 线同构文档](https://www.hiascend.com/doc_center/source/zh/HDK/2610/A3/A3npu/npusmia3_0007.html)（抽查）。
- [Atlas A2 DCMI LP（HDK 26.1.x）](https://www.hiascend.com/doc_center/source/zh/HDK/2610/A2/A2DCMI/dcmi_077.html)：当前 AI Core 降频原因位图、100ms 更新、无历史查询与表 3 支持矩阵，2026-10-09 重取核对。
- 逐条主张与证据定位见[第十批供电散热来源记录](../../docs/research/batch-10-power-thermal-sources.md)（GPU/整机/采集侧）与[第十三批训练 NPU 来源记录](../../docs/research/batch-13-training-npu-power-sources.md)（训练线 NPU 补齐）。
- 待确认：高温门限与 ACG/POWERBRAKE 产品分表数值（未公开）；仅用 Freq/curFreq 判定故障节流的口径（该页未给）；本地 DCMI 版本/机型/权限及未列部署场景；npu-exporter 与 npu-smi/DCMI 字段对应关系；A3 故障定义 xlsx 逐行核对；HDK 26.1.x 之前版本训练线文档；边缘线与训练线字段差异比对；DGX 风扇细节；目标机房的温度/供电实测；BMC 与主机时钟偏差。
