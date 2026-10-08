---
id: software-stack.ascend-documented-profile
title: 昇腾软件栈的文档配套档案
type: reference
domain: software-stack
status: draft
platforms: [ascend]
source_refs:
  - src.ascend.torch-npu-v7.2.0-pytorch2.6.0
  - src.huawei.cann-83rcx-install-2026-09-29
updated_at: "2026-09-29"
summary: 固定一组 TorchNPU 已发布源码快照，区分源码、安装包和运行环境声明，并记录尚未获得证据的整栈条件。
related_ids:
  - software-stack.index
  - software-stack.compatibility-evidence
  - software-stack.layers-and-boundaries
applicability:
  environment_refs: []
  notes: "这是官方文档研究档案；未选定或检查任何真实硬件、驱动、固件、操作系统、容器镜像或集群环境。"
verification:
  status: source_checked
  evidence_refs:
    - src.ascend.torch-npu-v7.2.0-pytorch2.6.0
    - src.huawei.cann-83rcx-install-2026-09-29
  notes: "核对 TorchNPU 固定 commit 的英文 README、version.txt 与根 LICENSE，并补充当前 CANN 8.3.RCX 安装页中的驱动/固件前提；URL 含 83RC1 而页头为 8.3.RCX，不能据此固定历史 HDK 配套。未安装、构建或运行软件。"
---

# 昇腾软件栈的文档配套档案

## 范围与阅读方式

本文固定一组已经发布的 TorchNPU 资料作为研究基线，回答“官方文件在这个快照中分别声明了什么”。它不是部署建议、环境清单或本地验收记录，也不声称这是最新版本。判断配套证据的方法见[如何判断版本配套是否有依据](compatibility-evidence.md)，组件位置见[主机到模型执行的软件栈分层](layers-and-boundaries.md)。任何实际环境仍需重新确认硬件型号、HDK（驱动与固件）、操作系统、架构、CANN 软件包集合、Python 构建、PyTorch 构建和上层应用。

本档案选用官方 tag `v7.2.0-pytorch2.6.0`，并把该 tag 在核查时解析到的 commit 固定为 [`bc51ab84cc6f35c77aab1c59886e0ea43681a317`](https://github.com/Ascend/pytorch/tree/bc51ab84cc6f35c77aab1c59886e0ea43681a317)。tag 名和发布分支名不是同一标识；tag 仍可能被仓库维护者重指，后续引用以完整 commit 为准。

## 固定基线

| 层次 | 本档案记录的值 | 证据与边界 |
|---|---|---|
| 发布 tag | `v7.2.0-pytorch2.6.0` | 2026-09-29 查询官方远端得到上述解引用 commit，定位方法和结果见[来源核查记录](../../docs/research/batch-01-source-audit.md)；后续内容引用固定到 commit。 |
| 源码分支名 | `v2.6.0-7.2.0` | 固定 commit 的 [README “Ascend Auxiliary Software” 表](https://github.com/Ascend/pytorch/blob/bc51ab84cc6f35c77aab1c59886e0ea43681a317/README.md#ascend-auxiliary-software)把这一分支名列在对应行。分支可继续变化，不能代替 commit。 |
| 源码版本文件 | `2.6.0.post3` | 固定 commit 的 [`version.txt`](https://github.com/Ascend/pytorch/blob/bc51ab84cc6f35c77aab1c59886e0ea43681a317/version.txt)。它描述该源码快照中的版本字段；本档案没有自行构建 wheel。 |
| README 声明的安装包 | `torch-npu==2.6.0.post3` | 固定 commit 的 [README “From Binary” 段](https://github.com/Ascend/pytorch/blob/bc51ab84cc6f35c77aab1c59886e0ea43681a317/README.md#from-binary)。这是发布文档中的安装包声明，不证明仓库源码与已发布 wheel 的文件内容逐字对应。 |
| PyTorch | `2.6.0` | 同一 README 的二进制安装段和配套表均给出 2.6.0。README 分别展示了 AArch64 的 `2.6.0` 与 x86 的 `2.6.0+cpu` 获取方式；本档案未核查任一 wheel。 |
| CANN | `8.3.RC1` | 同一 [配套表](https://github.com/Ascend/pytorch/blob/bc51ab84cc6f35c77aab1c59886e0ea43681a317/README.md#ascend-auxiliary-software)把 CANN 8.3.RC1、PyTorch 2.6.0、Extension 2.6.0.post3 和分支名放在同一行。 |
| Python | `3.9.x`、`3.10.x`、`3.11.x` | 固定 commit 的 [“PyTorch and Python Version Matching Table”](https://github.com/Ascend/pytorch/blob/bc51ab84cc6f35c77aab1c59886e0ea43681a317/README.md#pytorch-and-python-version-matching-table)针对 PyTorch 2.6.0 的声明。没有据此补写微版本或 ABI。 |

这里的“配套”严格限于 TorchNPU 固定 README 同一行或同一节的明确声明。后续打开的 CANN community 安装页虽在 URL 中包含 `83RC1`，页面标题和版本选择器却显示 `8.3.RCX`。因此它只作为下文的补充来源，不能当作不可变的 CANN 8.3.RC1 历史条件，也不能把其他版本、商用版或搜索摘要拼进这一组合。

## 源码、发行包与运行环境的边界

### 源码快照

固定 commit 可用于复核 README、`version.txt` 和代码树。源码分支 `v2.6.0-7.2.0` 是 README 中给出的开发或维护入口，会随提交变化。只写分支名无法复现本文看到的文件状态。

### 发行包声明

README 把 `torch-npu==2.6.0.post3` 作为二进制安装版本，并把它与 PyTorch 2.6.0、CANN 8.3.RC1 对应。本文没有下载 wheel、读取其 `METADATA`、比对构建 commit 或校验下载摘要，所以不能进一步断言发布 wheel 由固定 commit 原样构建。

### CANN 与 HDK

固定 README 的配套表只给出 `CANN 8.3.RC1`。2026-09-29 使用浏览器加载 community 文档后，补充核对了以下两条当前页面声明；它们说明安装职责边界，不补齐本档案的历史配套矩阵。

| 当前文档声明 | 精确来源与限制 |
|---|---|
| 安装 CANN 前，需要确认 NPU 驱动和固件已经安装 | [快速安装，“安装前准备”](https://www.hiascend.com/document/detail/zh/CANNCommunityEdition/83RC1/softwareinst/instg/instg_quick.html?Mode=PmIns&InstallType=netconda&OS=openEuler&Software=cannToolKit#ZH-CN_TOPIC_0000002474377814__zh-cn_topic_0000002473322892_section574172816522)。当次页面选择为物理机、在线 Conda、openEuler、Toolkit，页头为 8.3.RCX；未据此扩展任意操作系统或安装方式。 |
| 物理机和容器部署场景的 NPU 驱动、固件安装位于物理机 | [安装 NPU 驱动和固件](https://www.hiascend.com/document/detail/zh/CANNCommunityEdition/83RC1/softwareinst/instg/instg_0005.html?Mode=PmIns&InstallType=netconda&OS=openEuler&Software=cannToolKit#ZH-CN_TOPIC_0000002474537728)。这不表示容器无需用户态库、设备映射或其他运行条件，也没有给出本档案的精确 HDK 版本。 |

页面可以持续更新，路径、版本选择器和正文示例并不构成同一个固定版本标识。未取得与所选 TorchNPU/CANN 历史组合匹配的完整 HDK 条件；以下字段仍保持未知：

- 具体 Atlas/NPU 型号与板卡形态；
- firmware 和 driver 的包名、版本、补丁及组合；
- 主机操作系统、内核、glibc、CPU 架构与容器基础镜像；
- CANN Toolkit 之外所需的 kernels/ops、NNAL、HCCL 等包的精确集合；
- 目标安装方式下的 Python 微版本、PyTorch 构建标签与 C++ ABI；
- 单机或多机拓扑以及 HCCL、RDMA、交换网络的条件。

## 上层组件纳入状态

| 组件 | 本基线状态 | 原因 |
|---|---|---|
| MindCluster | 未纳入 | 本轮没有获得把某一固定 MindCluster release/commit 与 `torch_npu 2.6.0.post3 + CANN 8.3.RC1` 放在同一配套表中的官方证据。设备插件、监控和调度版本不能从 CANN 大版本推导。 |
| MindSpeed / MindSpeed-LLM | 未纳入 | 本轮没有核实到同时固定 MindSpeed、Megatron/MCore、TorchNPU 及 CANN 的同版本官方交集。训练文章应另建配套档案。 |
| vLLM Ascend | 未纳入 | 本轮未完成把固定 vLLM Ascend release 与本基线逐项对照的来源核查，因此没有同版本交集证据。 |

“未纳入”表示证据不足，不表示组件一定不兼容。

## 许可与再利用边界

固定 commit 的 [根 `LICENSE`](https://github.com/Ascend/pytorch/blob/bc51ab84cc6f35c77aab1c59886e0ea43681a317/LICENSE)包含 BSD 3-Clause 条款，可作为仓库根代码许可证据。以下范围没有被该结论替代：

- 固定 commit 下没有 `docs/LICENSE` 文件；因此不能沿用 `master` 分支可能存在的文档许可声明来概括这个历史快照；
- `torch_npu` wheel 的打包许可文件及随附 notice 未下载核对；
- CANN、HDK 和其他二进制包受各自下载页、EULA、notice 与第三方条款约束；
- 仓库中的第三方目录和 notice 需要按具体复用文件再核查。

本知识条目只保存链接、短摘要和自行整理的事实表，没有镜像第三方文档或软件包。

## 使用与解释注意事项

1. 不要用 `7.2.0` 单个数字代表完整环境。这里至少有产品/tag 命名、源码分支、wheel 版本、PyTorch 版本和 CANN 版本五组不同标识。
2. 不要把固定 commit 的矩阵外推到分支当前 tip、`master`、其他 PyTorch 版本或其他 CANN 补丁。
3. 不要把 README 的快速示例当作验收结果。本文没有执行 `import torch_npu`、NPU 算子、分布式作业或性能测试。
4. 固定 commit 没有独立 `COMPATIBILITY.md`；本基线的配套表来自英文 README。该 tag 下的中文 README 留有合并冲突标记，因此未作为主要证据。
5. 实际建档时应记录软件包来源和摘要、安装后查询结果、设备/驱动/固件信息以及最小算子和通信验证证据，再决定是否将环境称为可用。

## 来源与更新范围

- [TorchNPU 固定 commit](https://github.com/Ascend/pytorch/tree/bc51ab84cc6f35c77aab1c59886e0ea43681a317)：核对英文 README、`version.txt` 与根 LICENSE。
- CANN 安装页的读取方式、版本标识差异和采用范围见[第二批来源核查记录](../../docs/research/batch-02-source-audit.md)。当前页面补充不改变上述固定基线，也不撤销第一批记录的错误引用纠正。
- 待确认：硬件对应 HDK、OS/内核、CANN 子包、wheel 构建来源和摘要，以及 MindCluster、MindSpeed、vLLM Ascend 的同版本交集。
