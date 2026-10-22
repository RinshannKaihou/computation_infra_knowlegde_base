---
id: path.task.environment-installation
title: 环境安装任务路径
type: path
domain: overview
status: draft
platforms:
- generic
source_refs:
- src.nvidia.driver-installation-guide-latest-2026-10-21
- src.huawei.cann-83rcx-upgrade-uninstall-2026-10-21
- src.amd.rocm-install-docs-10.1.0
updated_at: '2026-10-22'
summary: 软件环境安装与验证的阅读路径：准入门禁、七层验证梯子、平台样板、目标产出与停止条件。
related_ids:
- software-stack.compatibility-evidence
- software-stack.environment-installation-and-upgrade
- software-stack.layers-and-boundaries
- software-stack.runtime-execution-and-library-loading
- software-stack.framework-backend-adaptation
- cluster-platform.container-image-runtime-baseline
- cluster-platform.device-resource-chain
- software-stack.host-resource-pressure-and-device-access
- path.task.node-acceptance
- path.task.migration-and-upgrade
---

# 环境安装任务路径

本页把搭建 GPU/NPU 软件环境时的阅读串成一条路径。它是导航草稿，不是安装手册：三平台安装正文中的命令与回显均来自固定版本官方文档的取样核对（CUDA 12.8、CANN 8.3.RCX、ROCm 10.1.0 样板），本库未在任何环境执行过安装；照抄命令不构成适用性证明，执行依据用户已有授权与现场条件。`generic` 表示导航意图，不表示三平台步骤可互换。

## 前置材料（先于一切步骤）

按[三平台安装基线、迁移升级与回退验证](../../knowledge/02-software-stack/environment-installation-and-upgrade.md)的"变更前准入门禁"，以下三项任一缺位即**停止实际变更**（可继续查证，但不执行安装/升级/卸载）：

1. **完整依赖交集**：硬件 × OS × 驱动 × 运行时 × 框架/引擎每一环节都要有配套依据。用[兼容性证据方法](../../knowledge/02-software-stack/compatibility-evidence.md)区分依据类型并分别记录声明与本地验证状态（发行包兼容矩阵/发行说明、源码分支/构建配置、项目测试声明/CI、本地运行验证——不可压缩为从弱到强的等级）；补不到依据即停止。
2. **有效 baseline**：已有环境的升级须有可复跑的变更前最小验证结果（B0），没有即停止；**首次安装例外**——记录"安装前状态"与清理目标后方可进行。
3. **恢复路径**：回退方案落定（含制品保全与不可逆操作确认）后才执行变更。

另有一项**安装判定要求**（不是门禁的替代）：最小运行基线的结果契约字段（输入、预期输出、容差、同步点、错误码）须在验收前冻结——字段未冻结时，梯子 L6/L7 只能记"样例自带校验通过"，最终安装/升级验收不能记通过（样例自带校验 ≠ 计算正确性契约，见骨架正文）。

## 阅读顺序（先后有序）

1. [三平台安装基线、迁移升级与回退验证](../../knowledge/02-software-stack/environment-installation-and-upgrade.md)：准入门禁 → 七层安装验证梯子（逐层判定）→ 三平台样板节 → 回退与不可逆边界。本路径的骨架。
2. [主机到模型执行的软件栈分层](../../knowledge/02-software-stack/layers-and-boundaries.md)：失败发生在哪一层的责任划分依据。
3. [驱动初始化、运行时执行同步与库装载](../../knowledge/02-software-stack/runtime-execution-and-library-loading.md)：初始化→运算→同步→结果检查的最小验证方法与进程实载库身份核对。
4. [框架到设备后端的适配与能力核对](../../knowledge/02-software-stack/framework-backend-adaptation.md)：框架后端（CUDA/ROCm 内置路径、TorchNPU 扩展后端）的能力核对清单。
5. [镜像制品、容器运行时与设备暴露基线](../../knowledge/05-cluster-platform/container-image-runtime-baseline.md)：容器化部署时的镜像身份、运行时与设备暴露核对。
6. [从物理设备到容器资源的状态链](../../knowledge/05-cluster-platform/device-resource-chain.md)：装完后"任务看不到设备"时的状态分层入口。
7. [OS/进程资源压力与设备访问诊断](../../knowledge/02-software-stack/host-resource-pressure-and-device-access.md)：主机资源压力与设备访问问题的分层取证（安装后首个故障分支）。

## 目标产出

- 七层梯子的逐层判定记录：每层"命令/观察点 / 回显或证据 / 判定（通过/失败/无法判断）"。
- 最小运行基线结果：按结果契约记录（样例自校验通过 ≠ 计算正确性契约，两者区分见骨架正文）。
- 环境档案：版本组合、安装方式（runfile/包管理器/容器）、实载库身份与验证梯子结果，供后续[迁移与升级路径](migration-and-upgrade.md)作 B0 基线。

## 下一步判断

- 满足下方完成条件（七层逐层判定通过＋结果契约已冻结并满足＋环境档案登记完毕）：进入运行阶段——训练/推理负载先走[训练排障](training-triage.md)/[推理排障](inference-triage.md)或[性能优化路径](performance-optimization.md)。
- 某层失败：**先停在该层定位责任层、不继续向上安装**（进入该层对应的诊断正文）；确认需要变更环境（升级/换版本）时转[迁移与升级任务路径](migration-and-upgrade.md)。
- 判定为"无法判断"（缺工具、缺权限、样板与目标版本不匹配）：登记缺口，不视为通过。

## 完成/停止条件

- **完成**：七层梯子逐层通过、最小运行基线结果契约字段已冻结且满足、环境档案登记完毕——三者齐备才进入运行阶段。
- **停止并升级**：准入门禁三项任一缺位（已有环境无 baseline、首次安装未记录安装前状态与清理目标、回退路径未落定）；**任一层失败即停在该层定位、不得继续向上安装**，涉及不可逆/高危边界时另需先核对回退路径再动；结果契约字段未冻结时不得记最终安装/升级验收通过；目标版本组合无配套证据且无法降级到有证据组合。样板（CUDA 12.8 / CANN 8.3.RCX / ROCm 10.1.0）之外的目标版本：本库无安装证据，只能按"无法判断"处理并要求用户自行取得官方依据。

## 原始资料入口

- [NVIDIA Driver Installation Guide（latest 可变页，2026-10-21 观察）](https://docs.nvidia.com/datacenter/tesla/driver-installation-guide/latest/index.html)：NVIDIA 驱动安装官方指南（既有登记）。
- [CANN community 8.3.RCX 安装指南升级与卸载（instg_0027–0033，doc_center/source 静态镜像核读）](https://www.hiascend.com/doc_center/source/zh/CANNCommunityEdition/83RC1/softwareinst/instg/instg_0098.html)：昇腾侧官方升级/卸载入口（既有登记）。
- [Install AMD ROCm 10.1.0](https://rocm.docs.amd.com/en/docs-10.1.0/install/rocm.html)：AMD ROCm 安装官方文档（既有登记）。

以上为外部入口，版本随平台发布更新；实际安装以目标版本的对应官方文档为准。

## 逐链检查（T00-06 交付记录，2026-10-22）

本页全部内链经 `make check` 通过，引用的目标正文均为已交付条目（骨架正文为 T02-12/Batch 31 交付）；未引用未交付正文。页尾三项外部入口均为既有登记来源（`source_refs`），URL 与 registry 逐字对齐。
