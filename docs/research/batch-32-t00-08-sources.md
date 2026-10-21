# 第三十二批 T00-08 来源记录

任务：T00-08（三平台入口与现有排障路径的收口；**new/navigation** `paths/platforms/amd.md`；**revise** `paths/platforms/nvidia.md`＋`paths/platforms/ascend.md`＋`paths/tasks/training-triage.md`＋`paths/tasks/inference-triage.md`，主题 00.6）。取证轮次：主会话作者角色首轮（2026-10-22）。

## 新增来源与主张定位

无。AMD 入口的外部引用严格限既有登记的官方材料（见下表）；未以任何未登记主页冒充兼容依据。NVIDIA/昇腾入口与两个排障路径的更新只增补对已交付正文的链接，不改正文主张。

## 复用来源与主张定位

| 主张 | 登记 ID | 精确位置 | 支持范围 |
|---|---|---|---|
| AMD 入口页尾四项外部入口 | src.amd.rocm-install-docs-10.1.0 / src.amd.rocm-release-notes-10.1.0 / src.amd.rccl-docs-6.3.3 / src.amd.amd-smi-docs-10.1.0 | 仓库登记 URL，与 registry 逐字对齐 | 入口指引；具体能力以所用版本为准 |
| AMD 入口正文条目 | 不适用（链接库内正文） | 30 篇 platform 含 amd 的正文（ROCm 档案、RCCL 档案、GPU 算子/内存诊断、健康证据 AMD SMI/RAS 映射、BMC OEM 支路、参考架构 AMD 位置节等），均为 Batch 13–31 交付、多篇经审阅修订 | 各自固定版本与审阅边界 |
| NVIDIA/昇腾入口与排障路径新增条目 | 不适用（链接库内正文） | Batch 13–31 交付的领域正文（硬件固件选型/软件栈执行/平台作业/训练推理执行各节），平台归属逐条核对（不含该平台的不列入） | 各自固定版本与审阅边界 |

## 本文原创部分

AMD 入口页的结构（已有阅读材料/先明确环境/完整平台阅读路径/按问题选择入口/尚未取得资料与未证实的边界/跨平台比较/任务路径入口）；"样板不等于兼容矩阵、未列出的组合是无证据"表述；五个导航目标的共用逐链检查记录（`path.platform.amd` 新稳定 ID，其余四页保留原 ID）。NVIDIA/昇腾页的分组小节与排障页新增表格行。

## unknown 清单

1. AMD 同构超节点无官方公开组成样板：保持 unknown、不类推（引用参考架构"AMD 的位置与集群样板"节原口径）。
2. AMD 侧尚未取得资料的设备/版本组合以 AMD ROCm 档案与 RCCL 档案的 unknown 清单为准，入口页不复制不汇总（避免转写出错）。
3. 五页均为导航草稿，不构成任何兼容矩阵或部署推荐；全部正文 draft、未实测。

## 复核轮修订记录（初审后）

（待审阅后追记）
