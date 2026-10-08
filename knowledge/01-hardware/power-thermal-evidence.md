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
  - src.usenix.superbench-atc24
updated_at: "2026-09-30"
summary: 供电/散热异常经降频、降速与冗余降额表现为性能退化；汇总 GPU 降频位图、violation 计数、健康与主动诊断边界、整机电源散热规格与 NPU 侧观测缺口。
related_ids:
  - hardware.health-evidence
  - hardware.resource-topology
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
  notes: "核对 DCGM v3.3.9 固定源码的字段与判定、DCGM/nvidia-smi latest 文档（可变）、两机型规格与 MindCluster npu-exporter 固定源码；未执行任何设备查询、诊断或压测。"
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

DCGM 的热/电源 watch（选择子 `t`）是**被动**机制：健康模块 “uses passive field watches … without running a dedicated workload”。v3.3.9 的实现是：热 watch 看 `THERMAL_VIOLATION` 计数器**最近一分钟增量**是否非零（最小采样间隔 30s），电源 watch 同理（[DcgmHealthWatch.cpp](https://github.com/NVIDIA/DCGM/blob/b0ec3c624ea21e688b0d93cf9b214ae0eeb6fe52/modules/health/DcgmHealthWatch.cpp)）。被动 watch 只看 violation 增量，不看温度绝对值或趋势。

官方对 Healthy 的限定（[health-monitoring 页](https://docs.nvidia.com/datacenter/dcgm/latest/learn/modules/health-monitoring.html)，latest 可变）：

> A Healthy result means that no enabled health rule found an incident in the retained data. It does not mean that every subsystem was watched or that an active stress test passed.

主动诊断中与电源/散热相关的测试：`targeted_power`（达不到请求的功率阈值，或持续功率负载下出错）、`pulse_test`（电流/功率需求快速变化暴露供电不稳）、`diagnostic` 插件覆盖 thermal excursions（[dcgm-diagnostics 页](https://docs.nvidia.com/datacenter/dcgm/latest/learn/modules/dcgm-diagnostics.html)）。同页明确：诊断不修复故障、不替代离线现场诊断、不决定 RMA；失败可源于 host、权限、库、拓扑、冷却、供电或负载干扰；侵入性测试只能在可移出服务的资源上运行。由“失败可源于环境”可推断其反面同样成立：通过也不证明测试窗口外的冷却/供电没有问题——这是本库的推论，不是页面原文。

## 整机规格（两个固定机型例子）

| 机型 | 电源 | 散热 | 降额/边界 |
|---|---|---|---|
| NVIDIA DGX H100/H200（指南 2026-01-26） | 6×3.3kW PSU，4+2 冗余；≥3 个 PSU 才能开机；系统输入 200–240V AC、10.2kW max | 气流 1105 CFM（80% fan PWM）、38,557 BTU/hr、工作温度 5–30°C | 官方原文：“If three PSUs lose power … the system continues to function, but at a **reduced performance level**.”——供电异常可表现为性能降级而非宕机 |
| Atlas 800T A2（产品页 2026-09-30 观察，可变网页） | 4×2.6kW 热插拔电源模块，2+2 冗余 | 8 个热插拔风扇模组 N+1 冗余、风冷、工作温度 5–35°C | 页面未给 NPU 数量、设备内存或降额行为说明，不能补写 |

环境差异的真实案例：SuperBench 记录同一数据中心内不同机架/机架内不同位置的温度差异，而 GPU 散热设计相同，温暖位置的 GPU 可能 thermal throttling；热带数据中心中 BER>10⁻¹² 的缺陷 IB 链路**数量**多 35 倍（[§2.1，印刷页 837](https://www.usenix.org/system/files/atc24-xiong.pdf#page=3)）。这些是 Azure 特定观察，用于说明环境差异的存在性，不构成通用阈值。

## NPU 侧观测现状（昇腾）

MindCluster v26.1.1 的 npu-exporter 有温度、功耗、电压、AICore 频率、健康状态指标（`npu_chip_info_temperature/power/voltage/aicore_current_freq/health_status`，[collector_for_npu.go L64–70](https://github.com/Ascend/mind-cluster/blob/44385c13d7b1d87def35f1604e8be4d16de6ca4e/component/npu-exporter/collector/metrics/collector_for_npu.go#L64-L70)），采集组默认开启、5 秒间隔。边界：

- 温度、功耗、电压指标的 help 字符串不含单位与口径（如 “the npu temperature”）；`aicore_current_freq` 的 help 注明单位为 MHz、`process_info` 注明 MB，但口径说明仍缺。Ascend310P 有“用整卡功耗替代芯片功耗”的特例注释（L238–247），其他型号的口径未核对。
- **没有降频原因/throttle 类指标**——collector 目录只有频率 gauge，没有 GPU 那样的 reason 位图等价物。NPU 侧“正在降速”的直接证据来源是**确认缺口**。
- npu-smi 的温度/功率查询命令存在（`npu-smi info -t temp/power -i <id> -c <chip_id>`），但已核对的版本化文档属于**边缘/推理产品线**（Atlas 200I A2/500 A2 的 24.1.RC1 命令参考，只核对了目录）；训练产品线（Atlas 800T/910）的对应版本化页面未定位。

## 常见误解

- **“温度正常 = 没有降频”**：被动 watch 只看 violation 增量；当前降频要看 reason 位图，历史降频要看 violation 累计；且 exporter 默认不导出这些字段。
- **“Healthy = 无热/电源问题”**：官方定义只覆盖已启用规则与保留样本（见上）。
- **“violation 数字可以跨工具直接比较”**：单位在 v3.3.9（usec）、master（ns）、nvidia-smi 文档（microseconds）之间不一致。
- **“PSU 失效会立刻宕机”**：冗余设计下是降额运行（DGX 官方 “reduced performance level”），表现为性能退化。
- **“GPU 的降频字段可以套到 NPU”**：NPU 侧没有已核对的等价物，频率/温度指标的单位口径也未确认。

## 来源与待确认问题

- [DCGM v3.3.9 固定源码](https://github.com/NVIDIA/DCGM/tree/v3.3.9)：位图、violation、watch 判定（注意 GitHub Web UI 对裸 commit 页面 404，tag 与 raw 链接可用）。
- [DCGM exporter 指标页](https://docs.nvidia.com/datacenter/dcgm/latest/reference/dcgm-exporter-metrics.html)、[字段定义页](https://docs.nvidia.com/datacenter/dcgm/latest/dcgm-api/dcgm-api-field-ids.html)、[health monitoring](https://docs.nvidia.com/datacenter/dcgm/latest/learn/modules/health-monitoring.html)、[diagnostics](https://docs.nvidia.com/datacenter/dcgm/latest/learn/modules/dcgm-diagnostics.html)、[nvidia-smi](https://docs.nvidia.com/deploy/nvidia-smi/index.html)：均为 latest 可变页，2026-09-30 观察。
- [DGX H100/H200 用户指南](https://docs.nvidia.com/dgx/dgxh100-user-guide/introduction-to-dgxh100.html)、[Atlas 800T A2 产品页](https://e.huawei.com/cn/products/computing/ascend/atlas-800t-a2)、[MindCluster v26.1.1](https://github.com/Ascend/mind-cluster/tree/44385c13d7b1d87def35f1604e8be4d16de6ca4e)、[npu-smi 边缘线命令参考](https://www.hiascend.com/doc_center/source/zh/Atlas%20200I%20A2/24.1.RC1/re/npu/Atlas%20A2%20智能边缘硬件%2024.1.RC1%20npu-smi%20命令参考%2001.pdf)、[SuperBench](https://www.usenix.org/conference/atc24/presentation/xiong)。
- 逐条主张与证据定位见[第十批供电散热来源记录](../../docs/research/batch-10-power-thermal-sources.md)。
- 待确认：训练产品线 npu-smi 版本化文档；NPU 降频事件的可观测等价物；npu-exporter 指标单位口径；DGX 风扇细节；目标机房的温度/供电实测。
