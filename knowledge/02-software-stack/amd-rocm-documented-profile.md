---
id: software-stack.amd-rocm-documented-profile
title: AMD ROCm 软件栈的文档配套档案
type: reference
domain: software-stack
status: draft
platforms: [amd]
source_refs:
  - src.amd.rocm-release-notes-10.1.0
  - src.amd.rocm-compatibility-matrix-10.1.0
  - src.amd.rocm-install-docs-10.1.0
  - src.amd.rocm-therock-transition-docs-10.1.0
  - src.amd.rocm-license-docs-10.1.0
  - src.amd.rocm-what-is-rocm-docs-10.1.0
  - src.amd.rocm-components-docs-10.1.0
  - src.amd.hip-docs-10.1.0
  - src.amd.rocr-runtime-docs-10.1.0
  - src.amd.rocblas-docs-10.1.0
  - src.amd.hipblas-docs-10.1.0
  - src.amd.miopen-docs-10.1.0
  - src.amd.rccl-docs-10.1.0
  - src.amd.rocminfo-docs-10.1.0
  - src.amd.rocm-llvm-docs-10.1.0
  - src.amd.hipcc-docs-10.1.0
  - src.amd.rocm-pytorch-install-2026-10-09
  - src.amd.amdgpu-driver-docs-31.60.0
  - src.amd.instinct-mi300x-system-acceptance-2026-10-09
  - src.amd.instinct-health-checks-2026-10-09
  - src.amd.instinct-system-validation-2026-10-09
  - src.pytorch.get-started-locally-2026-10-09
  - src.pytorch.whl-index-2026-10-09
  - src.amd.amd-smi-docs-10.1.0
  - src.amd.rocm-bandwidth-test-d7f5efe
  - src.amd.hip-docs-6.3.3
  - src.amd.rocr-runtime-docs-6.3.3
  - src.amd.instinct-mi300x-platform-datasheet-2023
updated_at: "2026-10-09"
summary: 以 ROCm Core SDK 10.1.0、Instinct MI300X、Ubuntu 24.04.5 与 amdgpu 31.60.0 为文档样板，分层记录组件版本、兼容矩阵、HIP/ROCr 编程运行路径、PyTorch 构建分发关系、安装与验证入口及组件许可，并保留版本标注冲突与未取证边界。
related_ids:
  - software-stack.layers-and-boundaries
  - software-stack.compatibility-evidence
  - software-stack.nvidia-documented-profile
  - software-stack.ascend-documented-profile
  - software-stack.runtime-execution-and-library-loading
applicability:
  environment_refs: []
  notes: "这是围绕 ROCm Core SDK 10.1.0 公开文档的文档样板档案；未选择、安装或检查任何真实主机、GPU、驱动、固件、操作系统、容器或集群环境，也不预先声称 10.1.0 或任何列出版本适配目标负载。"
verification:
  status: source_checked
  evidence_refs:
    - src.amd.rocm-release-notes-10.1.0
    - src.amd.rocm-compatibility-matrix-10.1.0
    - src.amd.rocm-install-docs-10.1.0
    - src.amd.rocm-therock-transition-docs-10.1.0
    - src.amd.rocm-license-docs-10.1.0
    - src.amd.rocm-components-docs-10.1.0
    - src.amd.rocm-pytorch-install-2026-10-09
    - src.amd.amdgpu-driver-docs-31.60.0
    - src.amd.instinct-mi300x-system-acceptance-2026-10-09
  notes: "文档样板，未安装、未运行任何 ROCm 组件。2026-10-09 逐页核对 docs-10.1.0 版本化 URL（release notes、兼容矩阵、安装指南、TheRock 过渡指南、许可页、组件职责页组，及 HIP/ROCr/rocBLAS/hipBLAS/MIOpen/RCCL/rocminfo/llvm-project/HIPCC 组件文档）、amdgpu 31.60.0 驱动安装页、Instinct system-acceptance 三份 latest 页、PyTorch get-started 与 wheel 索引；取证记录见 docs/research/batch-16-rocm-profile-sources.md。未下载任何包，未访问任何 GPU 设备。"
---

# AMD ROCm 软件栈的文档配套档案

## 范围与阅读方式

本文选择一个官方资料齐全的 ROCm 版本切面，回答"围绕这个切面，AMD 官方页面能固定哪些版本、职责与约束，哪些组合仍然未知或冲突"。它是文档研究样板，不是部署推荐、本地环境清单或支持承诺；选择 10.1.0 是取证便利，不预先声称该版本适合任何目标环境。

软件层次见[主机到模型执行的软件栈分层](layers-and-boundaries.md)，配套证据的判断方法见[如何判断版本配套是否有依据](compatibility-evidence.md)。本文与[NVIDIA 软件栈的文档配套档案](nvidia-documented-profile.md)、[昇腾软件栈的文档配套档案](ascend-documented-profile.md)并列；三平台的对照仅比较职责，不建立包名、版本或兼容规则等价关系。

## 选定样板与理由

| 样板轴 | 选定值 | 依据 |
|---|---|---|
| ROCm 版本线 | ROCm Core SDK **10.1.0**（[release notes](https://rocm.docs.amd.com/en/docs-10.1.0/about/release-notes.html) 页面日期 2026-10-05） | [过渡指南](https://rocm.docs.amd.com/en/docs-10.1.0/about/transition-guide-TheRock.html)确认"The transition … began with ROCm Core SDK 7.14.0, the first production release. ROCm 10.1.0 is the latest production release."；docs Hub 全部页面有 `/en/docs-10.1.0/` 版本化 URL，`latest` 与 `docs-10.1.0` 当前一致，引用固定 docs-10.1.0 |
| 硬件代际 | AMD Instinct **MI300X**（gfx942，CDNA 3） | 兼容矩阵给出 MI300 系列行；官方 system-acceptance 文档覆盖 MI300X 全流程；本库已登记 [MI300X platform datasheet](https://www.amd.com/content/dam/amd/en/documents/instinct-tech-docs/data-sheets/amd-instinct-mi300x-platform-data-sheet.pdf)（[Instinct MI300X system acceptance](https://instinct.docs.amd.com/projects/system-acceptance/en/latest/gpus/mi300x.html)） |
| OS 样板 | **Ubuntu 24.04.5 LTS**（Instinct 用内核 GA 6.8） | 10.1.0 release notes "Operating system support update"：新增 Ubuntu 26.04.1（kernel 7.0 GA）与 24.04.5（Instinct 用 GA 6.8、Radeon/Ryzen 用 HWE 7.0），替换此前的 26.04/24.04.4；兼容矩阵对全部 Instinct GPU 列出 24.04.5 |
| 内核驱动样板 | AMD GPU Driver (amdgpu) **31.60.0** | 兼容矩阵与 release notes "Kernel driver and firmware bundle support" 均以 31.60.0 为当前最高支持版本；[amdgpu 31.60.0 Ubuntu 安装页](https://instinct.docs.amd.com/projects/amdgpu-docs/en/docs-31.60.0/install/detailed-install/package-manager/package-manager-ubuntu.html)提供版本化驱动文档 |
| 配套监控版本线 | AMD SMI **27.1.0**（即 10.1.0 随附版本） | 与已登记 [AMD SMI docs-10.1.0 文档](https://rocm.docs.amd.com/projects/amdsmi/en/docs-10.1.0/index.html)同版本线，可互相印证（见下文版本标注冲突） |

选择理由归纳：(1) 10.1.0 是过渡指南确认的当前 production release，文档 URL 可版本化固定；(2) 与已登记 AMD SMI 27.1.0 来源同 release，健康证据两文可互证；(3) MI300X 是官方验收文档覆盖最全的数据中心代际之一，且硬件规格已有独立登记；(4) Ubuntu 24.04.5 在兼容矩阵中对全部 Instinct GPU 列出，取证选择器的默认可达性最好。

### 版本标注冲突：文档站标题与 release notes 组件表

两处 AMD 官方口径对同一制品给出不同版本号，本文按取证结论以 release notes 组件表为准，并保留双方位置：

| 组件 | release notes 组件表（10.1.0） | 组件文档站标题（docs-10.1.0 URL） | 处理 |
|---|---|---|---|
| HIP | HIP 10.0.0 ⇒ 10.1.0 | [HIP 文档](https://rocm.docs.amd.com/projects/HIP/en/docs-10.1.0/index.html)全站标题 "HIP 7.16.0 Documentation"（title 标签经复核） | 均为官方口径，未能判定制品真实版本号；本档案写 HIP 10.1.0 并注明站标差异 |
| LLVM | LLVM 24.0.0 | [llvm-project 文档](https://rocm.docs.amd.com/projects/llvm-project/en/docs-10.1.0/index.html)标题 "llvm-project 22.0.0 Documentation" | 同上；本档案写 LLVM 24.0.0 并注明站标差异 |

与之对照，ROCr Runtime 1.21.0、rocBLAS 5.7.0、hipBLAS 3.7.0、MIOpen 3.6.1、RCCL 2.30.7、rocminfo 1.0.0 的文档站标题与组件表一致，无冲突。

## 组件与版本清单

[What is ROCm?](https://rocm.docs.amd.com/en/docs-10.1.0/about/what-is-rocm.html) 把 ROCm 描述为 AMD GPU 加速计算的开放软件栈，含 runtimes、compilers、性能与系统工具及数学库；ROCm Core SDK 提供基础组件，生态含 PyTorch 等框架。10.1.0 组件版本总表见 [release notes "ROCm Core SDK components"](https://rocm.docs.amd.com/en/docs-10.1.0/about/release-notes.html)；表头 Important 注明组件支持按 GPU/OS 可变，以[兼容矩阵](https://rocm.docs.amd.com/en/docs-10.1.0/compatibility/compatibility-matrix.html)为准。

| 类别 | 组件与版本（10.1.0 组件表） | 职责要点 |
|---|---|---|
| 运行时与编译器 | HIP 10.0.0⇒10.1.0、HIPIFY 10.1.0、LLVM 24.0.0、ROCr Runtime 1.21.0、SPIRV-LLVM-Translator 24.0.0、libhipcxx 3.0.2；hipcc（[HIPCC 文档](https://rocm.docs.amd.com/projects/HIPCC/en/docs-10.1.0/index.html)站标 1.1.1） | HIP 为 C++ runtime API 与 kernel 编程语言；LLVM 24.0.0 含 ROCm 设备编译器 amdclang，编译 HIP 与 OpenCL（[runtimes and compilers](https://rocm.docs.amd.com/en/docs-10.1.0/components/runtimes-and-compilers.html)）；ROCr 为 HSA runtime 实现（见下文路径节） |
| 数学库 | rocBLAS 5.6.0⇒5.7.0、hipBLAS 3.6.0⇒3.7.0、hipBLASLt 1.4.1、MIOpen 3.6.0⇒3.6.1、Composable Kernel 1.3.0、rocFFT 1.0.40、rocSOLVER 3.37.0、rocSPARSE 5.1.0、hipCUB 4.7.0、rocPRIM 4.6.0、rocThrust 4.7.0、rocRAND 5.0.0、rocWMMA 2.2.1、hipSPARSELt 0.2.9 | 分层见下文 roc\*/hip\* 表述；[math and compute libraries](https://rocm.docs.amd.com/en/docs-10.1.0/components/math-and-compute-libs.html) |
| 通信 | RCCL 2.30.7（组件表标注仅 Linux）、rocSHMEM 3.7.0 | RCCL 为独立的多 GPU/多节点集合通信原语库，使用 PCIe 与 xGMI 高速互联，公开仓库在 ROCm/rocm-systems（[RCCL 文档](https://rocm.docs.amd.com/projects/rccl/en/docs-10.1.0/index.html)、[communication libraries](https://rocm.docs.amd.com/en/docs-10.1.0/components/communication-libs.html)） |
| 监控与诊断 | AMD SMI 27.0.0⇒27.1.0、rocminfo 1.0.0、RDC 1.3.1、ROCprofiler-SDK 1.4.1、Compute Profiler 3.9.0、Systems Profiler 1.9.0、ROCdbgapi 0.80.0、ROCgdb 16.3、ROCr Debug Agent 2.2.0 | rocminfo 为 HSA 系统信息枚举工具（[rocminfo 文档](https://rocm.docs.amd.com/projects/rocminfo/en/docs-10.1.0/index.html)）；健康证据见[设备健康证据与检测边界](../01-hardware/health-evidence.md)的 AMD SMI/RAS 分支 |
| 其他 | hipFile 0.5.0、rocDecode 1.10.0、rocJPEG 1.10.0、RPP 3.2.0 | 仅记录组件表版本，职责未逐项取证 |

**roc\* 与 hip\* 的官方分层表述**（[math and compute libraries](https://rocm.docs.amd.com/en/docs-10.1.0/components/math-and-compute-libs.html)）：`roc*` 是以 HIP 编写的 AMD 原生高性能实现；`hip*` 是可移植的 marshalling 包装层，支持与 CUDA 对应库（rocBLAS↔cuBLAS、rocFFT↔cuFFT、rocSOLVER↔cuSOLVER、rocSPARSE↔cuSPARSE 等）双后端；MIOpen 是开源深度学习原语库；hipBLASLt 提供超越传统 BLAS 的灵活 GEMM API。注意后端默认随代际可变：release notes rocBLAS 变更节注明 rocBLAS 5.7.0 起 gfx950 上单/双精度 GEMM 默认改用 hipBLASLt 后端。

**TheRock 打装与"包名≠能力"**：自 ROCm 7.14.0 起 ROCm 改用 TheRock 作为构建/发布系统（[过渡指南](https://rocm.docs.amd.com/en/docs-10.1.0/about/transition-guide-TheRock.html)）。安装目录为 `/opt/rocm/core-10.1`（extras 在 `/opt/rocm/extras-10/`），包名从旧流 `rocm-*`/`roc*`/`hip*` 合并为 `amdrocm-*`：`amdrocm-runtime` 含 HIP+ROCR+runtime compilation、`amdrocm-blas` 含 rocBLAS+hipBLAS+hipBLASLt+hipSPARSELt、`amdrocm-llvm` 含 amdclang++/hipcc/flang、`amdrocm-rccl` 含 rccl、`amdrocm-dnn` 含 hipDNN+MIOpen、`amdrocm-base` 含 rocminfo+rocm-core；`amdrocm` meta 包经 update-alternatives 提供 `/opt/rocm/bin`、`/opt/rocm/lib` 兼容符号链接；按架构分包（如 `-gfx942` 对应 gfx94X-dcgpu tarball family）。因此一个 `amdrocm-blas` 包对应四个组件、HIPCC/FLANG 并入 `amdrocm-llvm`——**安装包粒度比组件粒度粗，不能从包名直接推断文件与 ABI 边界**（这正是[分层文档](layers-and-boundaries.md)"一个产品名不是一层"的实例）；旧流包名与新名的对照表在同页。

## 兼容性矩阵（限所选字段）

来源为 [ROCm 10.1.0 compatibility matrix](https://rocm.docs.amd.com/en/docs-10.1.0/compatibility/compatibility-matrix.html)（页面日期 2026-08-26）。**取证边界**：该页是 JS 选择器驱动的单页（Device family → GPU → Linux distribution），静态抓取默认显示 MI355X 视图，MI300X 数据存于 HTML `data-show-cond` 条件块；无 URL 查询参数可固定选择状态，因此引用只能指向"页面 + 选择器组合 + 观察日期（2026-10-09）"，不能深链到 MI300X 视图。

| 字段 | MI300X（gfx942）取值 | 边界与反例 |
|---|---|---|
| 架构与 LLVM target | MI300 Series（MI325X/MI300X/MI300A）：CDNA 3，gfx942 | MI350 Series 为 CDNA 4 / gfx950，勿混 |
| OS（Ubuntu） | 26.04.1（GA 7.0）、24.04.5（GA 6.8）、22.04.5（GA 5.15） | OS 表行级差异须逐 GPU 核对：MI325X 的 RHEL 行不含 8.10；不能按"Instinct 全系"概括 |
| OS（其他发行版） | Debian 13/12、RHEL 10.2/10.0/9.8/9.6/9.4/8.10、Oracle Linux 10/9/8、Rocky Linux 9、SLES 16.0/15.7 | OL 行含 10/9/8、Rocky 行含 MI300X/MI300A，均为逐行条件块；本档案只取证 MI300X 行 |
| 内核驱动 | AMD GPU Driver (amdgpu) 31.60.0、31.50.0、31.40.1、31.40.0、31.30.0、31.20.0、31.10.0、30.30.3、30.30.2、30.30.1、30.30.0、30.20.1、30.20.0、30.10.2（共 14 版） | 驱动版本与 ROCm 用户态版本是两个序列，配套关系以此表为准，不能从 ROCm 版本号推导驱动版本 |
| 固件 | PLDM bundle 01.26.00.04（or later）/ 01.25.06.05 | 固件由 OEM/基础设施方分发（AMD 供 PLDM bundle，OEM 集成）；获取路径在 OEM 侧，应向 OEM 索取并核对版本 |
| 虚拟化 | SR-IOV 需 GPU-IOV Module (GIM) 9.3.0.K；KVM passthrough/SR-IOV 配置见矩阵 GPU virtualization support 节 | 虚拟化样板未深入取证，GIM 文档未打开（见"未取得材料"） |

本档案的 documented 组合因此限于：**兼容矩阵 MI300X 选择器状态下的 gfx942 × 上述 OS/驱动/固件字段 × ROCm 10.1.0 用户态**。矩阵行级条件块之外的组合（其他 GPU、其他 OS 行、未列驱动）保持 unknown，不从相邻版本或职责边界倒推。

## 编程与运行路径

按官方概念页，MI300X 上的执行路径可概括为：

**HIP（编程语言 + C++ runtime API）→ ROCr Runtime（HSA runtime）→ amdgpu/ROCK 内核驱动 → GPU**。

- **HIP**：C++ runtime API 与 kernel 编程语言的组合，面向 AMD GPU、与 CUDA 接口对齐以便移植；runtime API（streams/events/memory）实现在 CLR（Compute Language Runtime）仓库；kernel 语言为单源 C++。HIPIFY 把 CUDA 源码转换为 HIP C++，但官方明示**不是 drop-in 替代**（[What is HIP?](https://rocm.docs.amd.com/projects/HIP/en/docs-10.1.0/what_is_hip.html)、[HIP 文档索引](https://rocm.docs.amd.com/projects/HIP/en/docs-10.1.0/index.html)，站标 7.16.0 冲突见上节）。
- **ROCr Runtime**：AMD 的 HSA（Heterogeneous System Architecture）runtime 实现，官方表述为 "AMD's implementation of the HSA runtime, providing the foundation for GPU execution and management"（[runtimes and compilers](https://rocm.docs.amd.com/en/docs-10.1.0/components/runtimes-and-compilers.html)、[ROCR 1.21.0 文档](https://rocm.docs.amd.com/projects/ROCR-Runtime/en/docs-10.1.0/index.html)）。6.3.x 版本线文档进一步把 ROCr 描述为 thin, user-mode API，经 AMDGPU 驱动组与 ROCK 内核驱动访问设备（[ROCR 1.14.0 文档](https://rocm.docs.amd.com/projects/ROCR-Runtime/en/docs-6.3.3/index.html)，已登记旧版本线来源）；10.1.0 单页未展开 HSA 与内核 KFD/ROCk 的分层关系，本文引用概念页措辞为限。
- **内核驱动**：Instinct/Radeon 使用 amdgpu（DKMS 包 `amdgpu-dkms`）；ROCK 内核驱动以独立组件列于许可表（GPL 2.0 WITH Linux-syscall-note），与发行版 inbox amdgpu 的关系未逐项取证。
- **编译器**：LLVM 24.0.0 是 AMD 的 LLVM 编译器基础设施，含 ROCm 设备编译器 amdclang，编译 HIP 与 OpenCL；hipcc 为驱动脚本（站标 1.1.1），过渡指南注明 HIPCC/FLANG 已并入 `amdrocm-llvm` 包。

**三平台仅比较职责**：NVIDIA 路径为框架 → CUDA Driver/Runtime API 与配套库 → 内核驱动 → GPU（见 [NVIDIA 档案](nvidia-documented-profile.md)）；昇腾路径为 PyTorch → TorchNPU → CANN（AscendCL 等）→ NPU 驱动固件（见 [昇腾档案](ascend-documented-profile.md)）；AMD 路径为 HIP → ROCr → amdgpu/ROCK。三者抽象位置相似，但 API、ABI、包名、日志与兼容规则互不等价，不存在包名等价表；HIP 与 CUDA 的接口对齐只是移植便利，不承诺语义与性能一致（HIPIFY 非 drop-in）。接口级的初始化、stream/event 同步与库装载记录方法见[驱动初始化、运行时执行同步与库装载](runtime-execution-and-library-loading.md)（该文固定的是 HIP 6.3.42134 版本线，与本档案 10.1.0 线分属不同版本，引用语义须带版本线标注）。

## PyTorch 构建关系

**ROCm 侧声明**（release notes AI ecosystem 表，兼容矩阵同表）：PyTorch 2.14.0（Linux，Python 3.10–3.14；Windows，3.11–3.14）、2.13.0 与 2.12.0（仅 Instinct GPU）；vLLM 0.29.0 与 SGLang 0.5.18 要求 PyTorch 2.13.0。release highlights 同页另写 10.1.0 框架配套为 PyTorch 2.14.0、JAX 0.11.1、vLLM 0.29.0、SGLang 0.5.18、MIGraphX 2.18（替换 10.0.0 的 PyTorch 2.11.0），并称本版起 drop TensorFlow 2.19.1——而 AI ecosystem 表仍列 TensorFlow 2.21/2.20，两处口径并存，照录不裁断。表内注明框架支持随 GPU/OS 可变，以兼容矩阵为准。

**安装渠道**（[Install PyTorch for ROCm](https://rocm.docs.amd.com/projects/ai-ecosystem/en/latest/frameworks/pytorch/install.html)，latest 可变页，2026-10-09 观察，选择器含 ROCm 10.1.0/10.0.0/7.14.1/7.14.0 × PyTorch 2.14.0/2.13.0/2.12.0）：

| 渠道 | 内容 | 边界 |
|---|---|---|
| Docker | 镜像 `rocm/pytorch:rocm10.1.0_ubuntu26.04_py3.14_pytorch_release_2.14.0`（另有 ubuntu24.04_py3.12、ubuntu22.04_py3.10 变体）；容器启动挂 `--device /dev/kfd --device /dev/dri --group-add=video` | 镜像未拉取，digest 与内容未核验 |
| pip（AMD 索引） | 索引 `https://stable.repo.amd.com/rocm/whl-next/`，按架构选 wheel：`torch[device-gfx942]==2.14.0+rocm10.1.0`、`torchvision[device-gfx942]==0.29.0a0+rocm10.1.0`、`torchaudio==2.11.0.3+rocm10.1.0` | wheel 未下载，本地版本标识 `+rocm10.1.0` 是索引声明 |

**wheel 分发渠道分叉**（取证要点）：[download.pytorch.org/whl/](https://download.pytorch.org/whl/) 的 ROCm 目录 2026-10-09 只到 rocm7.14（另有 rocm3.7–rocm7.2 历史目录）；ROCm 10.x 的 torch wheel 仅由 AMD 自有索引分发（10.1.0 在 `stable.repo.amd.com/rocm/whl-next/`，7.14.x 示例另见 `repo.amd.com/rocm/whl-multi-arch/`）。因此**不能把"PyTorch 官方 wheel 支持 ROCm 10.1.0"写成既成事实**；上游客轮渠道与 AMD 索引是两个并行分发渠道，应写"AMD 分发带 `+rocm10.1.0` 本地版本标识的 wheel"。上游是否/何时补 rocm10.x 目录未知。

**PyTorch 官方口径**（[Get Started Locally](https://pytorch.org/get-started/locally/)，latest 可变页，2026-10-09 观察）：Linux pip 选择器含 ROCm 计算平台选项；"the ROCm build of PyTorch uses the same semantics at the python API level"，验证入口 `torch.cuda.is_available()`；源码构建 AMD GPU 需先安装 ROCm。选择器生成的具体 wheel 命令为 JS 动态内容，未逐版本核对。ROCm 侧安装文档的验证样板为 `python -c "import torch; print(torch.cuda.is_available())"` 输出 True——本文未运行。

**PyTorch ROCm 已知问题**（同 AMD 安装页，latest）：导入时 rocSHMEM 报 libnuma 缺失消息（装 libnuma-dev/numactl-devel 可消除，不影响正常运行）；部分 RDNA 推理负载 PyTorch<2.14 性能偏低，workaround `TORCH_BLAS_PREFER_HIPBLASLT=1`（2.14 起这些架构默认）；Radeon 训练负载 GPU reset 问题 workaround `TORCH_BLAS_PREFER_HIPBLASLT=0`——该 reset 问题在 10.1.0 release notes 中列为已解决（Llama-Factory/Unsloth on RX 9070/R9700），两处口径并存，引用须区分版本语境。

## 安装前提与最小验证入口

以下全部为文档样板，本文未执行任何步骤。

**五种安装方式**（[Install AMD ROCm 10.1.0](https://rocm.docs.amd.com/en/docs-10.1.0/install/rocm.html) "Compare installation methods"）：package manager（apt/dnf/zypper，系统级）、amdgpu-install（仅 Radeon/Ryzen）、pip（venv）、tarball（免 root/自定义目录）、Runfile（引导式、可含驱动）。apt 路径为注册 `stable.repo.amd.com/rocm/core/packages/ubuntu{2604,2404,2204}/` 仓库（GPG key `stable.repo.amd.com/rocm/gpg/packages.gpg`）后 `sudo apt install amdrocm10.1`（或按架构 `amdrocm10.1-gfx942` 等）。该页同为选择器驱动单页，锚点含选择器状态串，引用指页面 + 方法名。

**内核驱动单独安装**：Instinct/Radeon 需 AMD GPU Driver (amdgpu)，文档在 instinct.docs.amd.com amdgpu-docs；Ubuntu 24.04 为注册 `https://repo.radeon.com/amdgpu/31.60/ubuntu noble main`（key `repo.radeon.com/rocm/rocm.gpg.key`）后 `sudo apt install amdgpu-dkms`，装完重启；卸载 `sudo apt autoremove amdgpu-dkms`；Ryzen APU 用发行版 inbox 驱动。装新驱动前须先卸载旧 AMDGPU 驱动（页面 Caution）；dkms 与内核版本的实际匹配未验证。

**GPU 访问权限**（install/rocm.html "Configure permissions for GPU access"）：组成员方式把用户加入默认的 video 与 render 组（`sudo usermod -a -G render,video $LOGNAME`；video 管视频设备、render 管 DRM render node），或 udev 规则 `/etc/udev/rules.d/70-amdgpu.rules`（`KERNEL=="kfd", GROUP="render", MODE="0666"` 与 `SUBSYSTEM=="drm", KERNEL=="renderD*", GROUP="render", MODE="0666"`）；改完需重启生效；容器环境在宿主机上配置。

**最小验证入口**（install/rocm.html "Verify your installation"；示例输出为厂商样例，非本库实测）：

| 验证层 | 入口 | 文档样例要点 |
|---|---|---|
| 设备与运行时可见 | `rocminfo`（枚举 HSA agent） | 样例输出含 GPU agent 与 "ROCk module version 6.16.6 is loaded" |
| 工具/驱动/ROCm 版本线 | `amd-smi version` | 样例 "AMDSMI Tool: 27.1.0+7da43026 \| AMDSMI Library version: 27.1.0 \| ROCm version: 10.1.0 \| amdgpu version: 7.1.9.31600000" |
| pip 路径安装身份 | `pip freeze \| grep rocm`、`rocm-sdk` CLI | 文档样板；Windows 用 `hipinfo` |

设备级健康与验收入口（[Instinct MI300X system acceptance](https://instinct.docs.amd.com/projects/system-acceptance/en/latest/gpus/mi300x.html)、[Basic system health checks](https://instinct.docs.amd.com/projects/system-acceptance/en/latest/common/health-checks.html)、[System Validation](https://instinct.docs.amd.com/projects/system-acceptance/en/latest/common/system-validation.html)；三份均为 latest 形态、无版本别名，阈值随文档更新可变，示例输出取自 Ubuntu 22.04 系统）：

- 流程：Prerequisites Validation → Basic Health Checks → System Validation → Performance Benchmarks。健康检查含 `sudo lspci -d 1002:74a1`（应见 8 GPU）、`lspci -vvv` 看 LnkSta 32GT/s x16、`amd-smi monitor -putm` 空闲指标、dmesg 驱动错误（有错则重装 amdgpu）、内核启动参数（如 `pci=realloc=off iommu=pt`）。
- 算子/带宽门槛（文档样板阈值）：rocblas-bench FP32 ≥94100 / BF16 ≥130600 / INT8 ≥162700 GFLOPS；TransferBench a2a ≥32.9 GB/s、p2p 单向 ≥33.9/双向 ≥43.9 GB/s；BabelStream 8 卡阈值（Copy ≥4,177,285 MB/s 等）。
- 同步/集合通信门槛：rccl-tests `all_reduce_perf -b 8 -e 8G -f 2 -g 8` bus BW ≥304 GB/s。
- RVS（ROCm Validation Suite，`sudo apt install rocm-validation-suite`）模块：gpup（属性）、gst（GEMM 压力，目标 GFLOPS `met: TRUE`）、iet（功耗压力）、gm（温度/风扇/时钟/功耗 violations 0）、mem（内存测试，带宽约 2 TB/s）、pebb/peqt（PCIe 带宽/资格，peqt 需 sudo）、pbqt（P2P）；MI300X 专用 conf 在 `/opt/rocm/share/rocm-validation-suite/conf/MI300X/`。多数模块无 PASS/FAIL 判定，文档自述以"输出在合理范围"为准。AGFHC 为更完整的现场健康检查工具，需向 AMD customer success 索取安装。
- 运行侧健康证据的字段语义（ECC 计数、CPER/AFID、坏页、复位影响范围）见[设备健康证据与检测边界](../01-hardware/health-evidence.md)的 AMD SMI/RAS 分支（固定 AMD SMI 27.1.0 / docs-10.1.0 来源）。

**ROCm Bandwidth Test 的 EOL 边界**：过渡指南 "ROCm Core SDK component changes (moved or removed)" 节注明 ROCm Bandwidth Test 自 TheRock 架构的 ROCm 7.14.0 起 end-of-life，官方指引改用 TransferBench 或 RVS；ROCm SMI 同步移除，由 AMD SMI 替代。因此已登记的 [rocm_bandwidth_test 固定 commit d7f5efe](https://github.com/ROCm/rocm_bandwidth_test) 仍是该工具本身的有效源码证据，但**不能作为 10.x 流的推荐验证工具引用**——凡引用带宽验证入口时应指向 TransferBench/RVS。

## 典型配套/装载故障与回退边界

| 故障类别 | 文档化表现与处置 | 边界 |
|---|---|---|
| KFD/设备节点权限 | 未配置权限时 `/dev/kfd` 与 `/dev/dri/renderD*` 不可访问；处置为 video/render 组成员或 udev 规则（见上节） | 安装指南未单列"权限不足报错"排错条目，权限步骤的存在理由即此故障模式 |
| 内核驱动与用户态不匹配 | 驱动版本序列（amdgpu 31.60.0…30.10.2）与 ROCm 用户态版本序列相互独立，配套以兼容矩阵表为准；健康检查页指引 dmesg 有驱动错误则重装 amdgpu | dkms 与具体内核版本的匹配未验证；无面向"KFD 初始化失败/驱动-用户态版本不匹配"的独立官方排错页（缺口如实记录） |
| 旧版本共存 | 安装指南 Note："If you have ROCm 7.2.4 or older installed, please uninstall it before proceeding"；跨大版本（7.14→10.1）无原地升级的明确声明，按"先卸后装"处理 | 未给出官方升级路径声明，不推断 |
| RCCL 集合通信错误结果 | 10.1.0 known issues：MI350 系列上 RCCL allreduce 走 LL 协议可能产生错误结果，workaround `export NCCL_PROTO=LL128,Simple`（GitHub issue #8792） | 属通信域问题，通信库与 rank 进度的主文在[集合通信与 rank 进度](../03-communication/collectives-and-rank-progress.md)（03 域），本文只作软件栈配套层面的记录；known issues 随 release 滚动，引用固定 docs-10.1.0 |
| 装载/执行类 known issues（10.1.0 选录） | MI200 系列上 device-to-device hipMemcpyAsync 可能失败；部分 Instinct GPU 多应用负载可能遇到间歇 GPU page fault；MI350P 上 RAS 错误注入/查询不可用 | 均为厂商已知问题清单，非本库实测；处置见对应 release notes 与 issue |
| 卸载/回退 | ROCm 用户态 `sudo apt autoremove amdrocm10.1`（及各架构变体）；内核驱动 `sudo apt autoremove amdgpu-dkms`；装新驱动前先卸旧 AMDGPU 驱动 | 回退边界只到文档声明的包操作；回退后状态需重新按验证入口确认 |

## 组件许可与再利用边界

来源为 [ROCm licenses](https://rocm.docs.amd.com/en/docs-10.1.0/about/license.html) "ROCm component licenses" 表（ROCm 按组件分别授权）：

| 许可 | 组件（选录） |
|---|---|
| MIT | HIP、HIPCC、CLR、hipBLAS、hipBLASLt、MIOpen、rocBLAS、rocFFT、rocRAND、rocSPARSE、hipFFT、hipSOLVER、hipSPARSE、hipSPARSELt、rocPRIM、rocWMMA、MIGraphX、AMD SMI、ROCm SMI Lib、TransferBench、ROCm Validation Suite、ROCm Bandwidth Test |
| NCSA（University of Illinois） | ROCR-Runtime、rocminfo、ROCr Debug Agent、Comgr、ROCm-Device-Libs |
| Custom | RCCL、hipCUB（许可表标注；RCCL 许可页正文实际为 BSD 三条款式文本，两种官方口径并存照录，再利用前须查仓库 LICENSE） |
| GPL 2.0 WITH Linux-syscall-note | ROCK-Kernel-Driver |
| Apache / Apache 2.0 | llvm-project（Apache；flang 为 Apache 2.0）、libhipcxx 与 hipThreads（Apache 2.0 with LLVM Exceptions）、rocThrust（Apache 2.0） |
| BSD-2-Clause | rocSOLVER |
| GPLv3 | ROCgdb |

文档仓库本体为 MIT（许可页顶部全文；页面尾部另有 ©2023-2025 法律声明与 MIT 头 ©2023-2026 并存，照录）。包内许可文本位于 `/opt/rocm/share/doc/<component-name>/`；开源组件经 GitHub 与 repo.radeon.com 发布，专有组件在 repo.radeon.com 的 proprietary 子目录；ROCprof Trace Decoder 与 AOCC 二进制另有许可协议。本知识库未选统一再分发许可，本文只保存链接、短字段与原创归纳，不镜像网页、包或文档。

## 官方声明与本地验证状态

按[版本配套证据方法](compatibility-evidence.md)的两条轴归纳（官方声明轴为 `documented`/`conflict`/`unknown`，本地验证轴一律 `not_run`）：

| 对象 | 官方声明轴 | 本地验证轴 | 依据与限制 |
|---|---|---|---|
| 10.1.0 组件版本总表（release notes） | `documented`，限厂商发布清单自述 | `not_run` | HIP/LLVM 站标差异另列；组件支持按 GPU/OS 可变，以兼容矩阵为准 |
| MI300X × Ubuntu 24.04.5 × amdgpu 31.60.0（兼容矩阵选择器状态） | `documented`，限矩阵 MI300X 条件块 | `not_run` | 选择器页面无深链，引用带观察日期；固件 PLDM 版本由 OEM 分发 |
| HIP 与 LLVM 组件版本号 | `conflict`（组件表 vs 文档站标题） | `not_run` | 本文以组件表为准并保留双方位置；制品真实版本未判定 |
| PyTorch 2.14.0 × ROCm 10.1.0（AI ecosystem 表） | `documented`，限该表 | `not_run` | wheel 渠道分叉另列；TensorFlow 两处口径并存 |
| PyTorch wheel 分发渠道（上游只到 rocm7.14；10.x 走 AMD 索引） | `documented`，限 2026-10-09 索引实查 | `not_run` | 上游是否补 rocm10.x 目录未知 |
| TheRock 打装与包合并（amdrocm-\*、/opt/rocm/core-10.1） | `documented`，限过渡指南 | `not_run` | 包名≠能力；旧流包名对照表同页 |
| 安装/权限/验证/卸载步骤与 known issues | `documented`，限 install guide、驱动文档、release notes、验收文档 | `not_run` | 全部为文档样板，未安装、未运行任何 ROCm 组件 |
| GIM/SR-IOV 虚拟化样板 | `unknown` | `not_run` | 仅记录矩阵声明（GIM 9.3.0.K），Instinct Virtualization Driver 文档未取证 |
| Windows / WSL2 路径 | `unknown` | `not_run` | HIP SDK on Windows 与 WSL2 technical preview（10.1.0 TheRock 产物含 librocdxg）仅见 release notes 段落，未展开 |
| AGFHC 与 Cluster Validation Suite | `unknown` | `not_run` | AGFHC 无公开下载（需 AMD customer success）；CVS 配置仅见验收文档描述 |
| Radeon（gfx120x/gfx110x）与 Ryzen（gfx115x）矩阵行 | `unknown` | `not_run` | 取证以 Instinct 为主线，其他行只扫过选择器结构，未逐字段记录 |
| KFD 排错独立页 | `unknown`（未发现） | `not_run` | 权限、驱动重装、旧版先卸载等散落在安装指南与健康检查页，无专门排错页 |

`documented` 严格表示来源对自己发布内容的声明，不表示本知识库对任何用户环境作出支持承诺；`not_run` 表示未安装、未运行任何 ROCm 组件，任何条目都不因此转为 reproduced。

## 来源与更新范围

- [ROCm Core SDK 10.1.0 release notes](https://rocm.docs.amd.com/en/docs-10.1.0/about/release-notes.html)（页面日期 2026-10-05）：production release 地位、OS 支持更新、组件版本总表、AI ecosystem、驱动/固件 bundle、known issues；版本化 URL，latest 当前一致，引用固定 docs-10.1.0。
- [ROCm 10.1.0 compatibility matrix](https://rocm.docs.amd.com/en/docs-10.1.0/compatibility/compatibility-matrix.html)（页面日期 2026-08-26，2026-10-09 观察选择器条件块）：MI300X 的架构、OS、驱动 14 版、固件与虚拟化字段。
- [Install AMD ROCm 10.1.0](https://rocm.docs.amd.com/en/docs-10.1.0/install/rocm.html)：五种安装方式、apt 仓库与包名、权限配置、验证入口、卸载与旧版本先卸要求。
- [Transition guide from legacy ROCm release stream](https://rocm.docs.amd.com/en/docs-10.1.0/about/transition-guide-TheRock.html)：TheRock 生产发布口径、/opt/rocm/core-10.1 布局、amdrocm-\* 合并包、update-alternatives、Bandwidth Test/ROCm SMI EOL。
- [What is ROCm?](https://rocm.docs.amd.com/en/docs-10.1.0/about/what-is-rocm.html)、[runtimes and compilers](https://rocm.docs.amd.com/en/docs-10.1.0/components/runtimes-and-compilers.html)、[math and compute libraries](https://rocm.docs.amd.com/en/docs-10.1.0/components/math-and-compute-libs.html)、[communication libraries](https://rocm.docs.amd.com/en/docs-10.1.0/components/communication-libs.html)：栈定位与组件职责表述。
- 组件文档（docs-10.1.0 版本化 URL，2026-10-09 观察站标）：[HIP](https://rocm.docs.amd.com/projects/HIP/en/docs-10.1.0/index.html)（站标 7.16.0）、[ROCR-Runtime 1.21.0](https://rocm.docs.amd.com/projects/ROCR-Runtime/en/docs-10.1.0/index.html)、[rocBLAS 5.7.0](https://rocm.docs.amd.com/projects/rocBLAS/en/docs-10.1.0/index.html)、[hipBLAS 3.7.0](https://rocm.docs.amd.com/projects/hipBLAS/en/docs-10.1.0/index.html)、[MIOpen 3.6.1](https://rocm.docs.amd.com/projects/MIOpen/en/docs-10.1.0/index.html)、[RCCL 2.30.7](https://rocm.docs.amd.com/projects/rccl/en/docs-10.1.0/index.html)、[rocminfo 1.0.0](https://rocm.docs.amd.com/projects/rocminfo/en/docs-10.1.0/index.html)、[llvm-project](https://rocm.docs.amd.com/projects/llvm-project/en/docs-10.1.0/index.html)（站标 22.0.0）、[HIPCC](https://rocm.docs.amd.com/projects/HIPCC/en/docs-10.1.0/index.html)（站标 1.1.1）。
- [Install PyTorch for ROCm](https://rocm.docs.amd.com/projects/ai-ecosystem/en/latest/frameworks/pytorch/install.html)（latest 可变页，2026-10-09 观察）：Docker 镜像、AMD wheel 索引与架构 wheel、验证样板与已知问题。
- [AMD GPU Driver (amdgpu) 31.60.0 Ubuntu 安装页](https://instinct.docs.amd.com/projects/amdgpu-docs/en/docs-31.60.0/install/detailed-install/package-manager/package-manager-ubuntu.html)（docs-31.60.0）：驱动仓库、amdgpu-dkms、重启与卸载、旧驱动先卸 Caution。
- [Instinct MI300X system acceptance](https://instinct.docs.amd.com/projects/system-acceptance/en/latest/gpus/mi300x.html)、[Basic system health checks](https://instinct.docs.amd.com/projects/system-acceptance/en/latest/common/health-checks.html)、[System Validation](https://instinct.docs.amd.com/projects/system-acceptance/en/latest/common/system-validation.html)（latest 形态，2026-10-09 观察）：验收流程、健康检查、RVS/AGFHC 与性能门槛。
- [PyTorch Get Started Locally](https://pytorch.org/get-started/locally/)（latest 可变页，2026-10-09 观察）与 [download.pytorch.org/whl/](https://download.pytorch.org/whl/)（索引实查，2026-10-09）：ROCm 渠道说明、API 语义声明与 wheel 目录边界。
- 既有登记复用：[AMD SMI 27.1.0 文档](https://rocm.docs.amd.com/projects/amdsmi/en/docs-10.1.0/index.html)（同 release 健康证据；CLI 页内嵌示例含旧版捕获 "Version: 27.0.0 | ROCm version: 7.14.0"，引用 amd-smi 输出示例须注明版本语境）、[ROCR 1.14.0 文档](https://rocm.docs.amd.com/projects/ROCR-Runtime/en/docs-6.3.3/index.html)与 [HIP 6.3.42134 编程手册](https://rocm.docs.amd.com/projects/HIP/en/docs-6.3.3/user_guide/programming_manual.html)（旧版本线，仅历史对照与 thin user-mode API 表述）、[rocm_bandwidth_test d7f5efe](https://github.com/ROCm/rocm_bandwidth_test)（工具已 EOL 的源码证据）、[MI300X platform datasheet](https://www.amd.com/content/dam/amd/en/documents/instinct-tech-docs/data-sheets/amd-instinct-mi300x-platform-data-sheet.pdf)（硬件代际规格）。
- 逐条主张、冲突原文与缺口见[第十六批取证记录](../../docs/research/batch-16-rocm-profile-sources.md)。
- 待确认：目标环境的 GPU SKU/固件（向 OEM 核对 PLDM 版本）、宿主 OS/内核与 dkms 匹配、GIM/虚拟化与 Windows/WSL2 样板、AGFHC/CVS 材料、Radeon/Ryzen 矩阵行、ROCm 10.x 在上游 wheel 索引的收录状态。

本文未下载、安装、构建或运行任何软件，也未访问本地 GPU、驱动、容器或网络。所有本地验证状态均为 `not_run`。
