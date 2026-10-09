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
  - src.huawei.cann-83rcx-version-compatibility-2026-10-09
  - src.ascend.torch-npu-7.2.0-releasenote-2026-10-09
  - src.ascend.torch-npu-7.2.0-install-guide-2026-10-09
  - src.pypi.torch-npu-2.6.0.post3-2026-10-09
  - src.huawei.modelzoo-pies-software-download-2026-10-09
updated_at: "2026-10-09"
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
    - src.huawei.cann-83rcx-version-compatibility-2026-10-09
    - src.ascend.torch-npu-7.2.0-releasenote-2026-10-09
    - src.ascend.torch-npu-7.2.0-install-guide-2026-10-09
    - src.pypi.torch-npu-2.6.0.post3-2026-10-09
    - src.huawei.modelzoo-pies-software-download-2026-10-09
  notes: "核对 TorchNPU 固定 commit 的英文 README、version.txt 与根 LICENSE，并补充当前 CANN 8.3.RCX 安装页中的驱动/固件前提；URL 含 83RC1 而页头为 8.3.RCX，不能据此固定历史 HDK 配套。2026-10-09 补核 TorchNPU 7.2.0 版本兼容性说明与安装指南（Pytorch/720 文档树）、CANN 版本兼容性页（8.3.RCX↔HDK 系列级通配）、PyPI torch-npu 2.6.0.post3 的 6 个 wheel 索引身份及 ModelZoo 教程旁证；CANN 8.3.RC1 的精确驱动/固件版本交集仍未取得，对应补齐子项保持阻塞。未安装、构建或运行软件。"
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
| 硬件（该快照声明） | 训练：Atlas 800（9000/9010）、Atlas 900 PoD（9000）、Atlas 300T/300T Pro（9000）、Atlas 800T A2、Atlas 900 A2 PoD、Atlas 200T A2 Box16、Atlas 300T A2；推理：Atlas 800I A2 | 固定 commit 的 [README “Hardware support” 节](https://github.com/Ascend/pytorch/blob/bc51ab84cc6f35c77aab1c59886e0ea43681a317/README.md)。Atlas 800T A2 在该快照硬件表内（A2 训练系列）；**Atlas 900 A3 不在该快照硬件表内**——CANN 快速安装页的产品选择器含「Atlas A3 系列产品」且默认命令展示 `a3-cann-kernels==8.3.RC1`，说明 A3 的 CANN 侧安装有文档入口，但 A3 × 本固定快照的组合在快照内无声明，不能据此纳入本基线。 |

这里的“配套”严格限于 TorchNPU 固定 README 同一行或同一节的明确声明。后续打开的 CANN community 安装页虽在 URL 中包含 `83RC1`，页面标题和版本选择器却显示 `8.3.RCX`。因此它只作为下文的补充来源，不能当作不可变的 CANN 8.3.RC1 历史条件，也不能把其他版本、商用版或搜索摘要拼进这一组合。

本轮补齐后，本档案的 documented 组合明确为：固定 commit `bc51ab84cc6f35c77aab1c59886e0ea43681a317` 声明的 Atlas 训练/推理机型表（含 Atlas 800T A2，不含 Atlas 900 A3）× torch-npu `2.6.0.post3` × PyTorch `2.6.0` × CANN `8.3.RC1` × Python `3.9.x`–`3.11.x`（3.11 受 CANN 上限 3.11.4 约束，见下文 CANN 与 HDK 节）；wheel 身份以 PyPI 索引的六个文件为准（abi1 变体身份未取得）。交集之外的列——精确驱动/固件版本、机型 × OS 组合、CANN 子包精确集合——保持 `unknown`（驱动/固件补齐子项 blocked），不把 releasenote 的产品家族宽口径或 CANN 版本兼容性页的系列通配写进这一组合。即使上述组合满足文档层面的交集条件，本地验证轴仍为 `not_run`，不转为 reproduced。

## 源码、发行包与运行环境的边界

### 源码快照

固定 commit 可用于复核 README、`version.txt` 和代码树。源码分支 `v2.6.0-7.2.0` 是 README 中给出的开发或维护入口，会随提交变化。只写分支名无法复现本文看到的文件状态。

### 发行包声明

README 把 `torch-npu==2.6.0.post3` 作为二进制安装版本，并把它与 PyTorch 2.6.0、CANN 8.3.RC1 对应。本文没有下载 wheel、读取其 `METADATA`、比对构建 commit 或校验下载摘要，所以不能进一步断言发布 wheel 由固定 commit 原样构建。

2026-10-09 经 [PyPI JSON API](https://pypi.org/pypi/torch-npu/2.6.0.post3/json) 取得 `torch-npu` 2.6.0.post3 的索引身份：共 6 个 wheel，上传日期 2025-10-30，索引声明 License 为 BSD License，`requires_python` 未设置，project URLs 指向 gitcode.com/ascend/pytorch。6 个 wheel 覆盖 cp39 / cp310 / cp311 × manylinux_2_17_x86_64（manylinux2014_x86_64）与 manylinux_2_28_aarch64，无 cp38（与固定 README 的 Python 3.9–3.11 一致）。索引声明的文件名与 sha256：

| wheel 文件名 | 索引声明 sha256 |
|---|---|
| `torch_npu-2.6.0.post3-cp39-cp39-manylinux_2_17_x86_64.manylinux2014_x86_64.whl` | `55ca4cce58f3c8b2a1f31f44733f383e8f2c9cc69e7490eb61ca618fd4b3ae86` |
| `torch_npu-2.6.0.post3-cp39-cp39-manylinux_2_28_aarch64.whl` | `904f16872a7346c400506869182275fb822f02d53451fa7363dc57fb039d0b9e` |
| `torch_npu-2.6.0.post3-cp310-cp310-manylinux_2_17_x86_64.manylinux2014_x86_64.whl` | `36fbe05e19141ffd8a8103cdd0e298ca6e20283ff437e92eb5c978d7f2558105` |
| `torch_npu-2.6.0.post3-cp310-cp310-manylinux_2_28_aarch64.whl` | `3a751498997171349bcba2ae0461dacc8ac4d05b52880d11a08cc07116a0d060` |
| `torch_npu-2.6.0.post3-cp311-cp311-manylinux_2_17_x86_64.manylinux2014_x86_64.whl` | `7ff85f28a2a7146a99111d289eab19c9198b8dfd626e889ab71d49487c4414fa` |
| `torch_npu-2.6.0.post3-cp311-cp311-manylinux_2_28_aarch64.whl` | `35ae3e7884b8b33e36c90506dba5d6d31f74f400ae90f1cb0ecb56c114683975` |

sha256 为索引声明值，未下载 wheel 比对内容。[hiascend 安装指南 insg_0002](https://www.hiascend.com/document/detail/zh/Pytorch/720/configandinstg/instg/insg_0002.html) 另说明 PyTorch 2.7.1+ 的 wheel 默认 CXX11_ABI=1，2.1.0/2.6.0 配套 wheel 可选 abi0/abi1——这是不同制品变体；PyPI 文件名不带 abi 标记，abi1 制品的独立身份（文件名与摘要）未取得，不能把 PyPI 清单直接当作两种 ABI 变体的完整身份。固定 README 二进制段还给出 6 个带内嵌 sha256 的 download.pytorch.org 上游 torch 链接（x86 为 `torch-2.6.0+cpu` linux_x86_64、aarch64 为 `torch-2.6.0+cpu` manylinux_2_28_aarch64，各 cp39/cp310/cp311），链接内嵌摘要未逐一下载验证。

### CANN 与 HDK

固定 README 的配套表只给出 `CANN 8.3.RC1`。2026-09-29 使用浏览器加载 community 文档后，补充核对了以下两条当前页面声明；它们说明安装职责边界，不补齐本档案的历史配套矩阵。

| 当前文档声明 | 精确来源与限制 |
|---|---|
| 安装 CANN 前，需要确认 NPU 驱动和固件已经安装 | [快速安装，“安装前准备”](https://www.hiascend.com/document/detail/zh/CANNCommunityEdition/83RC1/softwareinst/instg/instg_quick.html?Mode=PmIns&InstallType=netconda&OS=openEuler&Software=cannToolKit#ZH-CN_TOPIC_0000002474377814__zh-cn_topic_0000002473322892_section574172816522)。当次页面选择为物理机、在线 Conda、openEuler、Toolkit，页头为 8.3.RCX；未据此扩展任意操作系统或安装方式。 |
| 物理机和容器部署场景的 NPU 驱动、固件安装位于物理机 | [安装 NPU 驱动和固件](https://www.hiascend.com/document/detail/zh/CANNCommunityEdition/83RC1/softwareinst/instg/instg_0005.html?Mode=PmIns&InstallType=netconda&OS=openEuler&Software=cannToolKit#ZH-CN_TOPIC_0000002474537728)。这不表示容器无需用户态库、设备映射或其他运行条件，也没有给出本档案的精确 HDK 版本。 |

2026-10-09 在同一文档树补充核对以下声明（均为可变页面，带观察日期引用）；它们进一步说明安装顺序、版本口径与查询边界，同样不补齐本档案的历史配套矩阵：

| 当前文档声明 | 精确来源与限制 |
|---|---|
| 首次安装顺序为「驱动 > 固件」，覆盖安装为「固件 > 驱动」；包名模式 `Ascend-hdk-<chip_type>-npu-driver_<version>_linux-<arch>.run`、`Ascend-hdk-<chip_type>-npu-firmware_<version>.run`；默认安装路径 `/usr/local/Ascend`，并有 `--install-for-all` 与运行用户组要求 | [安装 NPU 驱动和固件 instg_0005](https://www.hiascend.com/document/detail/zh/CANNCommunityEdition/83RC1/softwareinst/instg/instg_0005.html?Mode=PmIns&InstallType=netconda&OS=openEuler&Software=cannToolKit)。`<chip_type>` 与 `<version>` 为占位符，本页不钉版本。 |
| CANN 8.3.RCX 配套 Ascend HDK 版本为 25.3.X / 25.2.X / 25.0.X / 24.1.X / 24.1.RC3；支持的操作系统列只写「详见兼容性查询助手」 | [CANN 版本兼容性 releasenote_0000](https://www.hiascend.com/document/detail/zh/CANNCommunityEdition/83RC1/releasenote/releasenote_0000.html)。表头为 8.3.RCX 可变口径；这是**系列级通配**，没有钉 CANN 8.3.RC1 的精确驱动/固件版本，不能以系列通配冒充精确配套。 |
| TorchNPU 7.2.0 物理机 OS 兼容性查「兼容性查询助手」（交互工具，选择器含产品系列/型号/NPU/OS/解决方案），虚拟机/容器场景查《CANN 软件安装指南》「操作系统兼容性说明」；CANN 快速安装页的 OS 选择器列 openEuler、Ubuntu、Debian、Kylin、CentOS、BCLinux、UOSV20、AntOS、AliOS、CTyunOS、CULinux、Tlinux、MTOS、veLinux 共 14 个 OS | [安装说明 insg_0001](https://www.hiascend.com/document/detail/zh/Pytorch/720/configandinstg/instg/insg_0001.html)、[快速安装 instg_0001](https://www.hiascend.com/document/detail/zh/CANNCommunityEdition/83RC1/softwareinst/instg/instg_0001.html)。查询助手静态抓取只能取得页面外壳，具体机型 × OS 结果未取得；选择器列出的 OS 不等于每个机型 × OS 组合均有支持声明。 |
| 安装 CANN 前须已装 NPU 驱动和固件（`npu-smi info` 查验）；「当前 CANN 支持 Python3.7.x 至 3.11.4 版本」；默认产品选择（Atlas A3 系列）下安装命令为 `conda install ascend::cann-toolkit==8.3.RC1` + `ascend::a3-cann-kernels==8.3.RC1`（channel `https://repo.huaweicloud.com/ascend/repos/conda/`） | [快速安装 instg_0001](https://www.hiascend.com/document/detail/zh/CANNCommunityEdition/83RC1/softwareinst/instg/instg_0001.html)。CANN 的 Python 上限 3.11.4 与固定 README 的 Python 3.9/3.10/3.11 交集为 3.9.x–3.11.x，其中 3.11 受 ≤3.11.4 约束；`a3-cann-kernels` 是默认 A3 选择下的包名，A2 机型对应 kernels 包名未观察，不推测。 |
| 训练/在线推理需「安装配套版本的 NPU 驱动固件、CANN 软件（Toolkit、Kernels 和 NNAL）」，具体版本指向《CANN 软件安装指南》；环境变量 `source /usr/local/Ascend/ascend-toolkit/set_env.sh` 与 `nnal/atb/set_env.sh`；「Python3.11 的调度（即下发）性能优于 Python3.10，建议用 Python3.11 及以上」 | [安装前准备 insg_0002](https://www.hiascend.com/document/detail/zh/Pytorch/720/configandinstg/instg/insg_0002.html)。本页不钉驱动/固件版本，仍指回 CANN 安装指南；性能建议不改变上文交集的版本范围。 |

### 产品版本口径与固定制品口径的交集收窄

[TorchNPU 7.2.0 版本兼容性说明 releasenote_0005](https://www.hiascend.com/document/detail/zh/Pytorch/720/releasenote/releasenote_0005.html)（Pytorch/720 文档树，2026-10-09 观察）按**产品版本**列出：TorchNPU 7.2.0 ↔ CANN 8.3.RC1 / 8.2.RC1 / 8.1.RC1 / 8.0.0 / 8.0.RC3 / 8.0.RC2 六个版本，并称「DrivingSDK 7.2.RC1 兼容 CANN 8.1.RC1、CANN 8.2.RC1、CANN 8.3.RC1」。这与固定 README 的口径对象不同：README 的配套表把本档案的固定制品（Extension 2.6.0.post3）单行钉在 CANN 8.3.RC1，releasenote 按产品家族 7.2.0 列宽口径。两者不是直接矛盾，但**交集对本档案固定基线仍只支持 CANN 8.3.RC1**——不能把六个 CANN 版本都写进本档案的组合，也不能用 DrivingSDK 的宽口径代替 HDK 精确配套。

### 精确驱动/固件交集保持阻塞

页面可以持续更新，路径、版本选择器和正文示例并不构成同一个固定版本标识。**CANN 8.3.RC1 的精确驱动/固件版本交集本轮（2026-10-09）仍未取得，该补齐子项保持阻塞（blocked），不得以系列通配冒充精确配套**：CANN 版本兼容性页只给出 HDK 系列级通配（25.3.X / 25.2.X / 25.0.X / 24.1.X / 24.1.RC3）；[ModelZoo 教程的版本配套表](https://www.hiascend.com/doc_center/source/zh/ModelZoo/pytorchframework/pies/pies_00003.html)（适用 Atlas 300I Pro/300V Pro/300V/300I Duo/800I A2 等推理产品）从 CANN 8.3.RC2 起列，**表内没有 8.3.RC1 行**，教程页不能当作 8.3.RC1 的 HDK 配套依据、不升级为权威矩阵；另有搜索摘要提示 MindSDK 7.2.RC1 把 CANN 8.3.RC1 与 npu-driver 25.3.RC1 列在一起，但对应页面经静态抓取未取得、未一手核对，只作发现入口，不能入正文。机型 × OS 的精确交集（兼容性查询助手结果）同样未取得。以下字段仍保持未知：

- 具体 Atlas/NPU 型号与板卡形态；
- firmware 和 driver 的包名、版本、补丁及组合；
- 主机操作系统、内核、glibc、CPU 架构与容器基础镜像；
- CANN Toolkit 之外所需的 kernels/ops、NNAL、HCCL 等包的精确集合；
- 目标安装方式下的 Python 微版本、PyTorch 构建标签与 C++ ABI（hiascend 指南称 2.6.0 配套 wheel 可选 abi0/abi1，但 abi1 制品的独立文件名与摘要未取得）；
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
- [TorchNPU 7.2.0 版本兼容性说明](https://www.hiascend.com/document/detail/zh/Pytorch/720/releasenote/releasenote_0005.html)与[安装指南 insg_0001](https://www.hiascend.com/document/detail/zh/Pytorch/720/configandinstg/instg/insg_0001.html)/[insg_0002](https://www.hiascend.com/document/detail/zh/Pytorch/720/configandinstg/instg/insg_0002.html)（Pytorch/720 文档树，2026-10-09 观察）：产品级 CANN 口径、安装前准备、Python 调度建议与 abi0/abi1 变体说明。
- [CANN 版本兼容性](https://www.hiascend.com/document/detail/zh/CANNCommunityEdition/83RC1/releasenote/releasenote_0000.html)（2026-10-09 观察）：8.3.RCX ↔ HDK 系列级通配；CANN 8.3.RC1 精确驱动/固件配套未取得，该补齐子项保持阻塞。
- [PyPI torch-npu 2.6.0.post3](https://pypi.org/pypi/torch-npu/2.6.0.post3/json)（2026-10-09 经 JSON API 取得）：6 个 wheel 的索引身份与 sha256；索引声明值，未下载比对。
- [ModelZoo 教程版本配套表](https://www.hiascend.com/doc_center/source/zh/ModelZoo/pytorchframework/pies/pies_00003.html)（2026-10-09 观察）：仅作旁证；表内无 CANN 8.3.RC1 行，不升级为权威矩阵。
- 逐条主张、冲突原文与缺口见[第十五批取证记录](../../docs/research/batch-15-profile-intersection-sources.md)。
- 待确认：硬件对应 HDK 精确版本、OS/内核、CANN 子包、abi1 wheel 身份，以及 MindCluster、MindSpeed、vLLM Ascend 的同版本交集。
