# 第十批来源记录：供电、散热与性能退化证据（R2-08）

研究日期：2026-09-30。目标正文：`knowledge/01-hardware/power-thermal-evidence.md`（reference）。版本：DCGM v3.3.9 固定 commit `b0ec3c624ea21e688b0d93cf9b214ae0eeb6fe52`、DCGM/nvidia-smi latest 文档（可变，2026-09-30 观察）、DGX H100/H200 指南（2026-01-26）、Atlas 800T A2 产品页（2026-09-30 复核）、MindCluster v26.1.1 固定 commit、SuperBench（印刷页 837–838）。未执行任何设备查询或诊断。

## 主张—证据表（NVIDIA 降频/降速观测）

| 主张 | 证据位置 | 类型 | 反证/未知 |
|---|---|---|---|
| 降频事件以位图字段暴露：bit 定义 GPU_IDLE=0x1（注释称未来版本可能移除）、CLOCKS_SETTING=0x2（"GPU clocks are limited by current setting of applications clocks"，无移除说明）、SW_POWER_CAP=0x4、HW_SLOWDOWN=0x8（温度过高/外部 Power Brake/Fast Trigger；注释称未来版本可能移除）、SYNC_BOOST=0x10、SW_THERMAL=0x20、HW_THERMAL=0x40（核心频率降≥2 倍）、HW_POWER_BRAKE=0x80（外部 Power Brake，如系统电源）、DISPLAY_CLOCKS=0x100（nvidia-smi 文档注明仅 Volta 设备支持） | DCGM v3.3.9 dcgmlib/dcgm_fields.h L100–103、L107–154 | 固定源码 | 复查修正：移除说明只在 GPU_IDLE 与 HW_SLOWDOWN 两处 |
| 该字段表示**当前正在发生**而非历史："Current clock throttle reasons (bitmask)"；nvidia-smi 文档："If all event reasons are returned as 'Not Active' it means that clocks are running as high as possible." | dcgm_fields.h L480–482（DCGM_FI_DEV_CLOCK_THROTTLE_REASONS 112）；nvidia-smi latest 页 | 源码 + 官方文档 | — |
| 历史累计由 violation 计数器承载：POWER_VIOLATION 240、THERMAL_VIOLATION 241、SYNC_BOOST 242、BOARD_LIMIT 243、LOW_UTIL 244、RELIABILITY 245 | dcgm_fields.h L666–693 | 固定源码 | **单位跨版本冲突**：v3.3.9 注释 usec；DCGM master（2026-09-30 观察）为 ns；nvidia-smi 文档为 microseconds——引用必须固定版本 |
| exporter 默认不导出降频/violation 信号：Shipped Default 只有温度/功率/时钟 gauge；violation counter 与 DCGM_EXP_CLOCK_EVENTS_* 在 Optional（commented） | exporter 指标页 Shipped Default/Optional；dcgm-exporter 仓库 etc/default-counters.csv（main 可变，未 pin） | 文档 + 可变仓库 | 默认部署看不到降频信号，需显式开启 |
| DCGM_EXP_CLOCK_EVENTS_COUNT 计窗口内 bit active 的样本记录数（非事件数，受采集频率影响）；TOTAL 计 inactive→active 跳变，重启/hot reload 清零；label 值 9 种 | exporter 页 Windowed sample counts/Cumulative totals 小节 | 官方文档 | — |
| 命名演变：v3.3.9 为 CLOCK_THROTTLE_REASONS；master 主名改为 CLOCKS_EVENT_REASONS（旧名别名、Deprecated）；nvidia-smi 变更日志 v525→v530 改名、后续版本为兼容加回 | master dcgm_fields.h（SHA 64df9f89，可变）；nvidia-smi 变更日志 | 可变源码 + 文档 | v3.3.9 中不存在 CLOCKS_EVENT 命名，引用勿混用 |

## 主张—证据表（DCGM health/diagnostics 边界）

| 主张 | 证据位置 | 反证/未知 |
|---|---|---|
| 热/电源 watch 的选择子为 t（"Thermal and power watches"）；健康模块 "uses passive field watches … without running a dedicated workload" | health-monitoring 页 | — |
| Healthy 语义边界（官方原文）："A Healthy result means that no enabled health rule found an incident in the retained data. It does not mean that every subsystem was watched or that an active stress test passed." | health-monitoring 页 | 这是"健康摘要不能证明无热/电源问题"的一手依据 |
| v3.3.9 GPU thermal 用范围内升序 GetSamples 取起始样本，再取该实体 GetLatestSample；后者不传 endTime，不保证限定于历史查询上界内，比较两计数器值的非零差值。未指定 startTime 时设为 now−60s，最小采样间隔 30s。GPU power 的 violation 两端分别取同一范围内升序/降序 GetSamples；另在当前功耗取样 ret=DCGM_ST_OK、blank 且非 NOT_SUPPORTED 时产生 DCGM_FR_POWER_UNREADABLE WARN | [固定 MonitorThermal L1550–1609](https://github.com/NVIDIA/DCGM/blob/b0ec3c624ea21e688b0d93cf9b214ae0eeb6fe52/modules/health/DcgmHealthWatch.cpp#L1550-L1609)、[MonitorPower L1612–1687](https://github.com/NVIDIA/DCGM/blob/b0ec3c624ea21e688b0d93cf9b214ae0eeb6fe52/modules/health/DcgmHealthWatch.cpp#L1612-L1687) | 2026-10-09 B13-R03/R06 修订：thermal 与 power 不共享严格窗口端点语义，关联历史事件须核对实际样本时间戳，未知时不按请求窗口归属 WARN。不直接判断温度仅限 GPU thermal violation 分支；被动不表示全部规则只看 violation，CPU thermal 另有阈值路径，功耗不可读不等于节流 |
| 完整硬件验证需离线诊断（RMA 要求） | health-monitoring 页 Warning 块 | — |
| 主动诊断中与电源/散热相关：targeted_power（达不到请求的功率阈值或持续功率负载下出错）、pulse_test（电流/功率需求快速变化暴露供电不稳）、diagnostic 插件覆盖 thermal excursions | dcgm-diagnostics 页 "Diagnostic selection by suspected defect" 表 | 无独立纯散热测试 |
| "测试通过不等于硬件完全正常"（官方原文）："DCGM Diagnostics do not repair faults, replace NVIDIA offline field diagnostics, or determine RMA eligibility…a failure can originate in the host, permissions, libraries, topology, cooling, power, or workload interference as well as in the target processor."；节点可以无被动事件但主动诊断失败，反之亦然 | dcgm-diagnostics 页 "Beyond Scope"/"When diagnostics are useful" | 侵入性测试只能在可移出服务的资源上运行 |

## 主张—证据表（整机规格）

| 主张 | 证据位置 | 反证/未知 |
|---|---|---|
| DGX H100/H200：6×3.3kW PSU，4+2 冗余；"If three PSUs lose power … the system continues to function, but at a reduced performance level."；≥3 PSU 才能开机；单路 3300W@200–240V，系统输入 200–240V AC、10.2kW max | DGX 用户指南 Power Specifications / Support for PSU Redundancy | "reduced performance level" 是供电异常→性能降级的厂商自述；指南未给风扇数量 |
| DGX 环境：气流 1105 CFM @80% fan PWM；38,557 BTU/hr；工作温度 5–30°C | 同页 Environmental Specifications | — |
| Atlas 800T A2：4×2.6kW 热插拔电源 2+2 冗余；8 热插拔风扇模组 N+1 冗余；风冷；工作温度 5–35℃ | 产品页技术规格区（2026-09-30 curl+UA 复核） | 页面可变；仍未给 NPU 数量/设备内存 |

## 主张—证据表（NPU 侧）

| 主张 | 证据位置 | 反证/未知 |
|---|---|---|
| MindCluster npu-exporter 有温度/功耗/电压/AICore 频率/健康指标：npu_chip_info_temperature（L64）、power（L65）、voltage（L66）、aicore_current_freq（L68，help 注明 MHz）、health_status（L70）；数据源 GetDeviceTemperature（L180）、GetMcuPowerInfo/GetDevicePowerInfo（L238–247，Ascend310P 用整卡功耗替代）；采集组默认开启、5 秒间隔 | component/npu-exporter/collector/metrics/collector_for_npu.go；build/metricConfiguration.json（固定 commit 44385c13） | **温度/功耗/电压**的 help 字符串不含单位与口径；aicore_current_freq 有 MHz、process_info 有 MB；未见 910B 训练卡口径说明 |
| **NPU 侧无降频原因/throttle 类指标**（collector 目录检索只有频率 gauge，无 reason/事件位图等价物） | 同上（缺失证据） | 降频事件可观测等价物为确认缺口 |
| npu-smi 有温度/功率查询命令：`npu-smi info -t temp/power -i <id> -c <chip_id>`（《Atlas A2 智能边缘硬件 24.1.RC1 npu-smi 命令参考 01》目录含 §4.16–4.19） | hiascend PDF 目录（2026-09-30） | **该 PDF 属边缘/推理产品线（Atlas 200I A2/500 A2），不能外推训练线**；正文表格抓取截断未逐字读取 |

## 主张—证据表（环境退化案例，SuperBench 印刷页 837–838）

| 主张 | 证据位置 | 反证/未知 |
|---|---|---|
| 热带数据中心中 BER>10⁻¹² 的缺陷 IB 链路多 35 倍（注意：是缺陷链路数量 35×，不是 BER 高 35×），导致训练与推理性能显著退化 | §2.1，印刷页 837 | Azure 特定观察，不外推 |
| 同一数据中心内不同机架/机架内不同位置温度不同，而 GPU 散热设计相同，温暖位置的 GPU 可能 thermal throttling | 同段，印刷页 837 | — |

## 未解决与抓取失败

- violation 单位跨版本冲突（usec/ns/microseconds）按版本各引各的。
- 训练产品线（Atlas 800T A2/910B）的 npu-smi 版本化官方页未定位；NPU 降频事件位图确认缺口。
- DGX 指南无风扇数量细节；DCGM commit 页面经 tag 访问（Web UI 对裸 commit 页面 404，raw 与 tag 链接可用）。
- hiascend HTML 页 JS 渲染，npu-smi 命令正文未完整取得。
