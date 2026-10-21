# 第三十二批 T00-06 来源记录

任务：T00-06（选型、节点验收与环境安装任务路径；**new/navigation** `paths/tasks/selection-and-capacity.md`＋`paths/tasks/node-acceptance.md`＋`paths/tasks/environment-installation.md`，主题 00.6）。取证轮次：主会话作者角色首轮（2026-10-22；前置 Batch 13–31 全部内容任务已交付，T02-12 安装正文为 Batch 31 交付）。

## 新增来源与主张定位

无。三条路径以已交付本库正文为依据（选型连接容量/成本与硬件组成、验收连接被动证据/主动诊断/样板验证、安装连接三平台档案与最小运行基线）。

## 复用来源与主张定位

| 主张 | 登记 ID | 精确位置 | 支持范围 |
|---|---|---|---|
| 节点验收路径全部条目 | 不适用（链接库内正文） | 四层证据与工具前提以[新节点与返修节点验收](../../knowledge/01-hardware/node-acceptance-triage.md)等正文为准（Batch 12/13–20 交付、多篇经审阅修订） | 各自固定版本与审阅边界 |
| 安装路径骨架 | 不适用（链接库内正文） | [三平台安装基线、迁移升级与回退验证](../../knowledge/02-software-stack/environment-installation-and-upgrade.md)（T02-12，Batch 31，gpt-6.1-sol/xhigh 审阅已闭环的 draft） | CUDA 12.8 / CANN 8.3.RCX / ROCm 10.1.0 文档样板 |
| 页尾外部入口（node-acceptance 两项） | src.nvidia.gpu-node-triage-2026-10-08 / src.huawei.mindx-dl-60rc2-ascend-dmi-2026-09-29 | 仓库登记 URL（latest 可变页注明观察日期） | 入口指引，不承载路径主张 |
| 页尾外部入口（environment-installation 三项） | src.nvidia.driver-installation-guide-latest-2026-10-21 / src.huawei.cann-83rcx-upgrade-uninstall-2026-10-21 / src.amd.rocm-install-docs-10.1.0 | 仓库登记 URL，与 registry 逐字对齐 | 入口指引；实际安装以目标版本官方文档为准 |

selection-and-capacity 页 `source_refs` 为空（无外部入口段，延伸阅读由所链正文承载）。

## 本文原创部分

三条路径的"前置材料/阅读顺序/目标产出/下一步判断/完成与停止条件"结构；三类停止条件的归纳（工具前提不满足记"无法判断"、规格不符停验、准入门禁三类缺一即停）；逐链检查记录。

## unknown 清单

1. 三条路径均为导航草稿，不产生任何运行结果；路径中全部"未验证/未实测"标注以所链正文为准。
2. 安装样板外（CUDA 12.8 / CANN 8.3.RCX / ROCm 10.1.0 之外）的目标版本本库无安装证据，路径只允许按"无法判断"处理。
3. NVIDIA 驱动指南为 latest 可变页（2026-10-21 观察口径），内容随官方更新漂移。

## 复核轮修订记录（初审后）

（待审阅后追记）
