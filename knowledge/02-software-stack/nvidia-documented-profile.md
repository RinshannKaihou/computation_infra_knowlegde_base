---
id: software-stack.nvidia-documented-profile
title: NVIDIA 软件栈的文档配套档案
type: reference
domain: software-stack
status: draft
platforms: [nvidia]
source_refs:
  - src.nvidia.pytorch-container-25.01-release-notes-2026-09-30
  - src.nvidia.ngc-pytorch-25.01-py3-catalog-2026-09-30
  - src.nvidia.cuda-toolkit-12-8
  - src.nvidia.cuda-compatibility-latest-2026-09-30
  - src.nvidia.framework-containers-user-guide-2026-09-30
  - src.nvidia.dcgm-v3.3.9
updated_at: "2026-09-30"
summary: 以 NGC PyTorch 25.01-py3 为文档研究基线，分层记录宿主驱动、容器运行层、CUDA 与基础库、PyTorch、通信库和诊断组件，并保留来源冲突与未知组合。
related_ids:
  - software-stack.index
  - software-stack.layers-and-boundaries
  - software-stack.compatibility-evidence
  - hardware.health-evidence
applicability:
  environment_refs: []
  notes: "这是围绕 NGC PyTorch 25.01-py3 的官方文档研究档案；未选择、检查或配置任何真实主机、GPU、驱动、容器运行时、网络或集群环境。"
verification:
  status: source_checked
  evidence_refs:
    - src.nvidia.pytorch-container-25.01-release-notes-2026-09-30
    - src.nvidia.ngc-pytorch-25.01-py3-catalog-2026-09-30
    - src.nvidia.cuda-toolkit-12-8
    - src.nvidia.cuda-compatibility-latest-2026-09-30
    - src.nvidia.framework-containers-user-guide-2026-09-30
    - src.nvidia.dcgm-v3.3.9
  notes: "核对 NVIDIA PyTorch Release 25.01、NGC 25.01-py3 catalog layer 元数据、CUDA 12.8/当前 compatibility 文档、当前 Frameworks Containers User Guide 及 DCGM v3.3.9 固定源码；未拉取或验签镜像，未取得 manifest digest，未安装或运行任何组件。"
---

# NVIDIA 软件栈的文档配套档案

## 范围与阅读方式

本文选择一个明确的 NVIDIA 容器发行标签，回答“围绕这个标签，官方页面能固定哪些版本和职责，哪些组合仍然未知或冲突”。它不是部署推荐、本地环境清单或支持承诺，也不声称 25.01 是当前最新或适合目标负载。

软件层次见[主机到模型执行的软件栈分层](layers-and-boundaries.md)，配套证据的判断方法见[如何判断版本配套是否有依据](compatibility-evidence.md)。文档中的容器 OS、CUDA 和库版本不能替代宿主 OS、内核和驱动记录；同一页面列出多个组件，也不证明任意硬件、网络和工作负载已经通过验证。

## 固定研究基线

本档案选择镜像标签 `nvcr.io/nvidia/pytorch:25.01-py3`。核心来源是 [NVIDIA PyTorch Release 25.01](https://docs.nvidia.com/deeplearning/frameworks/pytorch-release-notes/rel-25-01.html)和 [NGC `25.01-py3` catalog layer 页面](https://catalog.ngc.nvidia.com/orgs/nvidia/-/containers/pytorch/25.01-py3/layers)。

NGC 页面在 2026-09-30 可见 tag `25.01-py3`、签名标记、build id `134983853` 和 build ref `3857cfd7a27acea1d4e19243329fcd1dae3b222e`。这些元数据帮助定位制品，但页面展示的 layer SHA 不是本轮已核验的 image manifest digest。本档案没有拉取镜像、执行签名验证或检查镜像配置，因此制品 digest 和实际文件内容仍为未知。

## 分层档案

| 层次 | 本基线可记录的事实 | 证据状态与边界 |
|---|---|---|
| 宿主硬件 | release 页写 25.01 针对 Blackwell 优化，并从 25.01 起停止 Volta 支持 | 不是所有数据中心 GPU、MIG 模式或 SKU 的完整支持表；本档案没有目标 GPU |
| 宿主 OS 与内核 | 未固定 | 容器内 Ubuntu 24.04 不是宿主 OS 声明；内核、IOMMU、cgroup、Fabric Manager、NIC 驱动和固件均未知 |
| 宿主 NVIDIA driver | release 页首先写 570+，随后列出部分数据中心 GPU 可用的旧分支例外 | 同一 Driver Requirements 紧接着对 R545 给出冲突表述，见下文；没有本地 driver 或设备验证 |
| 容器引擎/runtime/toolkit | 当前 Frameworks User Guide 说明 Docker/NVIDIA Container Toolkit 位于宿主运行层，并把宿主驱动能力和设备提供给容器 | 25.01 release 页没有固定 Docker、containerd、NVIDIA Container Toolkit 或 runtime 的精确版本；不能从当前指南倒推 2025-01 的唯一组合 |
| 容器制品 | `nvcr.io/nvidia/pytorch:25.01-py3`；catalog 可见 build id/ref 与签名标记 | manifest digest 与签名验证结果未知；tag 可被服务端重新关联，不能替代 digest |
| 容器 OS/Python | release Contents 写 Ubuntu 24.04，包括 Python 3.12；catalog layer 环境字段写 `PYVER=3.12`、`PYVER_MAJMIN=312` | release 页另一处仍写 `/usr/local/lib/python3.10/dist-packages/torch`，差异保持未解决，不能擅改路径 |
| CUDA | `12.8.0.038` | 容器内 CUDA 用户态内容不等于宿主已安装 Toolkit，也不单独证明宿主驱动兼容 |
| 基础库 | cuBLAS `12.8.3.14`、cuDNN `9.7.0.66`、TensorRT `10.8.0.40` | 只记录 release 页列出的容器内容；具体动态链接、插件和第三方 notice 未核验 |
| 框架 | PyTorch `2.6.0a0+ecf3bae40a`；catalog 环境字段为截短形式 `2.6.0a0+ecf3bae` | NVIDIA 容器构建不等于上游 PyTorch v2.6.0 tag；未核验 wheel、源码树或 ABI |
| 集合通信与网络库 | NCCL `2.25.1`、HPC-X `2.21`、SHARP `3.9.0`、UCC `1.4.0`、OpenUCX `1.18.0`、OpenMPI `4.1.7`、rdma-core `50.0` | 证明 release 页列入这些内容，不证明目标 NIC、交换网络、RDMA、GPUDirect 或多机拓扑可用 |
| 诊断组件 | DCGM `v3.3.9` 可作为接近该时期的固定健康证据样板 | 25.01 release 页没有声明该 DCGM 版本是镜像依赖或随镜像提供；只能列为研究参考，不能写进已验证配套链 |

上表刻意不补齐未知格。驱动、容器运行层、容器用户态库、框架、通信库和诊断组件属于不同证据对象；只有同一官方来源明确给出交集，或限定环境完成本地验证，才能把多行合并为一个可用组合。

## 宿主驱动：R545 条款保持冲突

[Release 25.01 的 Driver Requirements](https://docs.nvidia.com/deeplearning/frameworks/pytorch-release-notes/rel-25-01.html#driver-requirements)包含两段不能同时当作无条件真值的陈述：

1. 第一段先要求 NVIDIA driver 570+，又说数据中心 GPU 可以使用若干旧分支，并列出 R545 545.23+。
2. 紧接段落说明 CUDA compatibility package 支持特定驱动，并把 R545 与 R418、R440、R450、R460、R510、R520、R530、R555、R560 一同列为不具备 CUDA 12.8 forward compatibility、应升级的分支。

[当前 CUDA Minor Version Compatibility](https://docs.nvidia.com/deploy/cuda-compatibility/minor-version-compatibility.html)把 CUDA 12.x 的大类最低驱动写为 525，并说明 minor-version compatibility 存在功能限制；它没有回答 25.01 页面中 R545 例外对哪些 GPU、功能或 compatibility package 成立。因此本档案记录：

> `R545 + PyTorch container 25.01`：官方声明 `conflict`；本地验证 `not_run`。

不能只摘第一段写“R545 已支持”，也不能只摘第二段写“所有 R545 必然不可用”。需要同一时期、同一产品范围的驱动表或正式勘误，才能消解冲突。目标环境还必须记录完整驱动版本和 GPU 型号，不能只写分支名。

## 容器运行层没有精确版本交集

[NVIDIA Deep Learning Frameworks Containers User Guide](https://docs.nvidia.com/deeplearning/frameworks/user-guide/index.html)说明宿主需要容器引擎和 NVIDIA Container Toolkit；Toolkit 在宿主 OS/driver 之上把 GPU 与驱动能力提供给容器。该指南还明确说明不应在构建镜像时把 NVIDIA driver 安装进镜像。

这些内容支持职责边界：

- 宿主 driver 管理设备并提供内核侧能力；
- 容器引擎与 NVIDIA Container Toolkit/runtime 负责设备和驱动能力的容器暴露；
- 镜像提供 CUDA 用户态库、框架和应用环境，不携带一个可替代宿主 driver 的驱动安装。

当前指南是可变页面，25.01 release 页又没有给出与镜像绑定的 Docker、containerd 或 Container Toolkit 版本。因此本档案不选择一个“看起来同期”的 Toolkit 版本补入矩阵。实际档案需另记引擎、Toolkit/runtime、配置模式、宿主 driver 和制品来源，再判断它们的官方交集与本地结果。

## Python 3.12 与 `python3.10` 路径差异

release 页的 Contents 把 Ubuntu 24.04 和 Python 3.12 列入容器；NGC layer 元数据独立给出 `PYVER=3.12` 与 `PYVER_MAJMIN=312`。两项来源共同支持“catalog 所示构建元数据与 release Contents 指向 Python 3.12”。

同一 release 页的概述仍写预构建 PyTorch 位于 `/usr/local/lib/python3.10/dist-packages/torch`。在没有拉取镜像检查解释器、`sys.path`、包 metadata 和文件系统前，不能判断这是过期路径、兼容层、某个变体还是其他文档问题。

本档案因此同时保存三个原始字段，不把路径改成 `python3.12`，也不凭路径把默认 Python 改写为 3.10：

| 字段 | 文档值 | 当前解释 |
|---|---|---|
| release Contents | Python 3.12 | 官方 release 内容声明 |
| catalog build 环境 | `PYVER=3.12`、`PYVER_MAJMIN=312` | NGC 可见构建元数据 |
| release 概述中的包路径 | `/usr/local/lib/python3.10/dist-packages/torch` | 与前两项不一致，保持冲突；实际制品未检查 |

## 框架、CUDA 和通信库的身份边界

release 页列出的 PyTorch `2.6.0a0+ecf3bae40a` 是 NVIDIA 容器中的构建身份，不能简写为“上游 PyTorch 2.6.0”。catalog 元数据中的 `2.6.0a0+ecf3bae` 又是截短形式；两者只在明确说明来源时并列保存。

CUDA `12.8.0.038`、cuBLAS、cuDNN、TensorRT、NCCL 与其他网络库是容器内容字段。它们不能推出：

- 宿主安装了同版 CUDA Toolkit，或宿主 driver 已满足全部功能；
- NCCL 已选择正确传输并在目标 NIC/交换网络上工作；
- HPC-X、SHARP、UCC、UCX、OpenMPI 与 NCCL 在目标作业中都会被加载；
- 单机导入成功等于多机通信、精度、性能或故障恢复已通过。

许可上，现有 `src.nvidia.cuda-toolkit-12-8` 提供 CUDA 12.8 归档与 EULA 入口，但不能概括镜像内所有 NVIDIA 组件和第三方库。容器制品、框架、库和 notices 仍需按实际复用范围核查。

## 诊断组件单独建档

[设备健康证据与检测边界](../01-hardware/health-evidence.md)用 DCGM `v3.3.9` 固定源码说明 GPU 字段与健康证据结构。该版本在时间上接近 25.01，但“接近”不是配套依据；PyTorch 25.01 release 页没有把 DCGM v3.3.9 声明为镜像内容或依赖。

因此 E02 只把 DCGM 标成“诊断研究参考”。实际环境必须另查 DCGM 安装位置、版本、宿主 driver/GPU 支持、插件和权限，不能从本档案推断应在宿主或容器中运行某一套诊断。

## 官方声明与本地验证状态

按[版本配套证据方法](compatibility-evidence.md)的两条轴，本档案可以这样归纳：

| 对象 | 官方声明轴 | 本地验证轴 | 依据与限制 |
|---|---|---|---|
| tag `25.01-py3` 与 release 25.01 内容 | `supported`，限该 release/catalog 自述 | `not_run` | 没有 digest、拉取、验签或容器启动 |
| PyTorch 构建与 CUDA/NCCL 等容器内容 | `supported`，限 release 页列出的构建 | `not_run` | 未检查镜像内文件、ABI、动态加载或功能 |
| R545 driver 与 25.01 | `conflict` | `not_run` | 同页前后条款冲突，当前 CUDA 大类表不足以消解 |
| Python 默认版本/包路径 | `conflict` | `not_run` | 3.12 字段与 `python3.10` 路径并存 |
| Docker/Container Toolkit 精确版本 | `unknown` | `not_run` | 当前用户指南只支持职责边界，没有 25.01 的固定版本交集 |
| DCGM v3.3.9 与 25.01 | `unknown` | `not_run` | 只是研究参考，没有同一配套声明 |

`supported` 在这里严格表示来源对自己发布内容的声明，不表示本知识库对用户环境作出支持承诺。

## 实际环境仍需补齐的字段

- GPU 产品/SKU、设备和切分模式、固件、VBIOS、Fabric Manager 与拓扑；
- 宿主 OS、内核、CPU 架构、cgroup/IOMMU 和完整 NVIDIA driver 版本；
- Docker/containerd、NVIDIA Container Toolkit/runtime 的版本、配置和包来源；
- 镜像 registry、tag、manifest digest、签名验证结果、拉取时间与可验证的软件清单；
- 容器内实际 Python 可执行文件、PyTorch 包 metadata、CUDA/库文件和动态加载结果；
- NIC、固件、交换网络、RDMA/GPUDirect 条件及 NCCL 实际传输；
- DCGM 或其他诊断组件的版本、部署位置、实体/插件覆盖和采集质量；
- 与目标训练或推理负载对应的功能、正确性、通信、性能和恢复验证证据。

缺少这些字段时，可以把本档案用于提出核查问题，不能把它改写成一份“已支持环境”。

## 许可与再利用边界

NVIDIA release notes、NGC catalog、CUDA compatibility 和 Frameworks User Guide 的网页许可范围未在本轮确认为可全文再发布。本条目只保存精确链接、短字段和原创归纳，不镜像网页、容器或软件包。

CUDA Toolkit 12.8 的归档入口指向相应 EULA；它不自动覆盖 NGC 容器、PyTorch、NCCL、HPC-X、UCX、OpenMPI、rdma-core 或其他第三方内容。DCGM 固定仓库的 Apache-2.0 只覆盖其许可声明范围内的源码，不扩张到 DCGM 二进制 SLA 或 NVIDIA 产品文档。

## 来源与更新范围

- [NVIDIA PyTorch Release 25.01](https://docs.nvidia.com/deeplearning/frameworks/pytorch-release-notes/rel-25-01.html)：核对容器内容、driver 条款、PyTorch/CUDA/NCCL 等版本、Python 路径、Blackwell 优化和 Volta 停止支持；页面标注最后更新于 2026-09-08，本轮于 2026-09-30 读取。
- [NGC PyTorch `25.01-py3` catalog layer 页面](https://catalog.ngc.nvidia.com/orgs/nvidia/-/containers/pytorch/25.01-py3/layers)：核对 tag、签名标记、build id/ref 和 Python 构建环境字段；没有把 layer SHA 充当 manifest digest。
- [CUDA Toolkit 12.8 归档](https://docs.nvidia.com/cuda/archive/12.8.0/)与[当前 CUDA Minor Version Compatibility](https://docs.nvidia.com/deploy/cuda-compatibility/minor-version-compatibility.html)：前者固定工具包文档范围，后者只用于解释大类兼容机制和限制，不能消解 25.01 的 R545 冲突。
- [NVIDIA Deep Learning Frameworks Containers User Guide](https://docs.nvidia.com/deeplearning/frameworks/user-guide/index.html)：只用于宿主 driver、容器引擎/Toolkit 与镜像职责边界；没有据此补写 25.01 的精确运行层版本。
- [DCGM v3.3.9 固定源码](https://github.com/NVIDIA/DCGM/tree/b0ec3c624ea21e688b0d93cf9b214ae0eeb6fe52)：诊断研究参考，不是与该镜像已配套的证明。

本文未下载、安装、构建或运行任何软件，也未访问本地 GPU、驱动、容器或网络。所有本地验证状态均为 `not_run`。
