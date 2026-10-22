---
id: path.task.node-acceptance
title: 节点验收任务路径
type: path
domain: overview
status: draft
platforms:
- generic
source_refs:
- src.nvidia.gpu-node-triage-2026-10-08
- src.huawei.mindx-dl-60rc2-ascend-dmi-2026-09-29
updated_at: '2026-10-22'
summary: 新节点/返修节点投产前验收的阅读路径：前置材料、四层证据顺序、目标产出与停止条件。
related_ids:
- hardware.node-acceptance-triage
- hardware.bmc-firmware-and-events
- hardware.health-evidence
- hardware.resource-topology
- hardware.power-thermal-evidence
- hardware.node-selection-and-lifecycle
- communication.bandwidth-baselines
- communication.rccl-runtime-and-verification
- software-stack.nvidia-documented-profile
- software-stack.ascend-documented-profile
- software-stack.amd-rocm-documented-profile
- path.task.selection-and-capacity
- path.task.environment-installation
---

# 节点验收任务路径

本页把新节点或返修节点投产前的验收阅读串成一条路径。它是导航草稿，不是经过实测的验收流程：路径中的主动诊断与基准样板都带有工具前提、机型与版本限制（例如 root 权限、套件级别化限制），执行前先读所链正文的适用边界。本路径只组织阅读，不授予任何操作权限。`generic` 表示导航意图，不表示同一套命令适用于所有平台。

## 前置材料（先于验收）

1. 订单/交付规格清单与节点台账：要核对的目标规格身份。
2. 平台归属与平台档案：NVIDIA / 昇腾 / AMD 各自的文档配套档案（版本边界与工具前提见第 7 步）。
3. 验收窗口内可用的权限与工具：能否取得 root、诊断套件是否可用、基准工具能否安装。
4. 被动证据入口：BMC/固件身份、健康摘要与错误事件的读取渠道。
5. 判定纪律预期：本次验收允许的三种结论（通过 / 失败 / 无法判断）与各自的记录模板（见第 1 步正文）。

## 阅读顺序（四层证据，先后有序）

1. [新节点与返修节点验收](../../knowledge/01-hardware/node-acceptance-triage.md)：规格核对、被动证据、主动诊断与基准样板四层证据的顺序、每层需要的材料与"通过/失败/无法判断"判定纪律。
2. [BMC、固件身份与跨层硬件事件](../../knowledge/01-hardware/bmc-firmware-and-events.md)：固件身份清单、更新边界与单一事件不可直接归因的记录方法。
3. [设备健康证据与检测边界](../../knowledge/01-hardware/health-evidence.md)：健康摘要、错误事件、累计计数器、采样失败与未覆盖项的区分，DCGM / DCMI·npu-smi / AMD SMI 三平台最小映射。
4. [计算节点资源与拓扑参考](../../knowledge/01-hardware/resource-topology.md)：规格核对用的统一记录字段（CPU、NUMA、加速器、PCIe、网络、存储与故障域）。
5. [供电、散热与性能退化证据](../../knowledge/01-hardware/power-thermal-evidence.md)：降频位图、violation 计数与设施/设备关联的观测边界（注意 NPU 侧观测缺口）。
6. 通信基线：先读[通信带宽与性能基线口径](../../knowledge/03-communication/bandwidth-baselines.md)固定口径，再按平台进入样板——AMD 侧[RCCL 运行条件、观测与最小验证档案](../../knowledge/03-communication/rccl-runtime-and-verification.md)；NVIDIA/昇腾侧样板与工具前提汇总见第 1 步正文的验收测试工具前提表。
7. 平台档案与生命周期：三份[文档配套档案](../../knowledge/02-software-stack/nvidia-documented-profile.md)（NVIDIA / [昇腾](../../knowledge/02-software-stack/ascend-documented-profile.md) / [AMD ROCm](../../knowledge/02-software-stack/amd-rocm-documented-profile.md)）核对工具与版本边界；最后以[节点选型、隔离返修、长期管理与退役](../../knowledge/01-hardware/node-selection-and-lifecycle.md)的"验收与投产前证据锚点""隔离与返修证据锚点"收口。

## 目标产出

- 四层证据逐层的验收记录：每层写"观察到什么 / 用什么工具取得 / 判定结论（通过/失败/无法判断）"。
- 无法判断项清单：因权限、工具前提或资料缺失而悬空的项，显式登记而不是默认通过。
- 投产前证据档案：节点身份、固件身份、基准结果与样板的版本组合，接入节点台账。

## 下一步判断

- 规格核对与四层证据全部通过：进入[环境安装任务路径](environment-installation.md)搭软件栈，再进入运行阶段路径。
- 出现失败或无法判断项：按[节点选型与生命周期](../../knowledge/01-hardware/node-selection-and-lifecycle.md)的隔离返修锚点处置；涉及设备故障时转[故障恢复任务路径](fault-recovery.md)与对应平台路径。
- 验收依据本身存疑（工具结论与健康证据冲突）：回到第 1 步正文的判定纪律，先降级为"无法判断"并收集证据。

## 完成/停止条件

- **完成**：四层证据均有记录且结论三选一落定；无法判断项都有明确的补证条件与责任人；节点进入台账。
- **停止并升级**：诊断工具前提不满足（无 root、套件级别限制、机型不在样板内）→ 该项记"无法判断"并升级，不用"健康摘要全绿"替代主动诊断；规格与订单不符 → 停止后续验收，先走商务/返修流程；被动证据已有明确硬件故障事件 → 中止常规验收，直接按故障路径处置。

## 原始资料入口

- [NVIDIA GPU Node Triage and Systematic Debug Guidelines（latest，2026-10-08 观察）](https://docs.nvidia.com/deploy/gpu-debug-guidelines/gpu-node-triage.html)：NVIDIA 侧节点分诊官方指南（既有登记）。
- [MindX DL 6.0.RC2 ascend-dmi 故障诊断](https://www.hiascend.com/doc_center/source/zh/mindx-dl/60rc2/toolbox/ascenddmi/toolboxug_0020.html)：昇腾侧 ascend-dmi 官方文档（既有登记）。

以上为外部入口，引用前需核对各自版本与许可；AMD 侧外部入口见 [AMD 平台路径](../platforms/amd.md)。

## 逐链检查（T00-06 交付记录，2026-10-22）

本页全部内链经 `make check` 通过，引用的目标正文均为已交付条目；未引用未交付正文。页尾两项外部入口均为既有登记来源（`source_refs`），不承载本页导航主张。
