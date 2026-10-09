# 第十六批来源记录：AMD ROCm 软件栈文档样板（T02-04）

研究日期：2026-10-09。研究者：探索子代理（非 gpt-6.1-sol）。目标正文：`knowledge/02-software-stack/amd-rocm-documented-profile.md`（reference，planned，验收标准见 plans/full-coverage-backlog.yaml T02-04）。范围：ROCm 版本线与文档结构、选定 release 的兼容性矩阵、组件职责与版本、PyTorch ROCm 构建关系、安装与验证入口、组件许可。只做了公开网页取证，未执行任何安装、命令或设备操作；除本文件外未改动仓库其他文件。

**选定样板**：ROCm Core SDK **10.1.0**（release notes 页面日期 2026-10-05），硬件代际 **AMD Instinct MI300X（gfx942，CDNA 3）**，OS 样板 **Ubuntu 24.04.5 LTS（内核 GA 6.8）**，驱动样板 **AMD GPU Driver (amdgpu) 31.60.0**。理由：(1) 10.1.0 是过渡指南确认的当前 production release，docs Hub 全部页面有 `/en/docs-10.1.0/` 版本化 URL；(2) 与已登记的 `src.amd.amd-smi-docs-10.1.0`（AMD SMI 27.1.0，正是 10.1.0 随附版本）同版本线，可互相印证；(3) MI300X 是官方 system-acceptance 文档覆盖最全的数据中心代际之一，且本库已登记 MI300X platform datasheet；(4) Ubuntu 24.04.5 在兼容矩阵中对全部 Instinct GPU 列出。

## 主张—证据表（release 选定与版本线）

| 主张 | 来源与定位 | 版本/日期 | 证据性质 | 反例/未知 |
|---|---|---|---|---|
| ROCm Core SDK 10.1.0 是当前 production release；自 ROCm 7.14 起用 TheRock 作为构建/发布系统，取代单体发布流程；10.1.0 发布重点为 AI 推理、开发者工具与 profiling | [ROCm Core SDK 10.1.0 release notes](https://rocm.docs.amd.com/en/docs-10.1.0/about/release-notes.html) 开头 Note 与 Release highlights；[Transition guide from legacy ROCm release stream](https://rocm.docs.amd.com/en/docs-10.1.0/about/transition-guide-TheRock.html)（"The transition … began with ROCm Core SDK 7.14.0, the first production release. ROCm 10.1.0 is the latest production release."） | release notes 页面日期 2026-10-05；2026-10-09 观察 | 厂商发布文档 | `latest` 与 `docs-10.1.0` 当前一致，引用应固定 docs-10.1.0 |
| 文档 Hub 结构（Install / How to / Conceptual / Reference）与版本化 URL 模式：`/en/docs-10.1.0/<page>`、组件文档 `/projects/<name>/en/docs-10.1.0/` | [ROCm documentation hub](https://rocm.docs.amd.com/en/docs-10.1.0/index.html) 导航；实测 HIP/rocBLAS/hipBLAS/MIOpen/rccl/rocminfo/ROCR-Runtime/llvm-project 的 docs-10.1.0 URL 均 200 | 2026-10-09 观察 | 站点结构核对 | 组件文档页标题自带组件版本号，与 release notes 组件表存在两处不一致（见「缺口与冲突」） |
| 10.1.0 新增 OS 支持：Ubuntu 26.04.1（kernel 7.0 GA）与 Ubuntu 24.04.5（Instinct 用 GA 6.8、Radeon/Ryzen 用 HWE 7.0），替换此前的 26.04/24.04.4 | release notes "Operating system support update" 节 | 同上 | 厂商发布文档 | 无 |
| 10.1.0 AI 框架配套：PyTorch 2.14.0、JAX 0.11.1、vLLM 0.29.0、SGLang 0.5.18、MIGraphX 2.18；替换 10.0.0 的 PyTorch 2.11.0 等；本版起 drop TensorFlow 2.19.1 | release notes "AI inference and frameworks" 节 | 同上 | 厂商发布文档 | AI ecosystem 表中仍列 TensorFlow 2.21/2.20（见 PyTorch 节） |

## 主张—证据表（兼容性矩阵：MI300X / gfx942 / Ubuntu 样板）

| 主张 | 来源与定位 | 版本/日期 | 证据性质 | 反例/未知 |
|---|---|---|---|---|
| 兼容矩阵页存在且版本化：ROCm 10.1.0 compatibility matrix，选择器驱动（Device family → GPU → Linux distribution），逐 GPU 给出架构、LLVM target、OS、驱动、固件 | [ROCm 10.1.0 compatibility matrix](https://rocm.docs.amd.com/en/docs-10.1.0/compatibility/compatibility-matrix.html) | 页面日期 2026-08-26；2026-10-09 观察 | 厂商兼容矩阵 | 页面为 JS 选择器；静态抓取默认显示 MI355X 视图，MI300X 数据存于 `data-show-cond` 条件块，无 URL 查询参数可固定选择状态，引用只能指页面+选择器组合 |
| MI300 Series（MI325X/MI300X/MI300A）：架构 CDNA 3，LLVM target gfx942 | 同上，System requirements 表 `data-show-cond '{"gpu": ["amd-instinct-mi325x","amd-instinct-mi300x","amd-instinct-mi300a"]}'` 行 | 同上 | 厂商兼容矩阵 | MI350 Series 为 CDNA 4 / gfx950，勿混 |
| MI300X 支持 OS（Ubuntu）：26.04.1（GA 7.0）、24.04.5（GA 6.8）、22.04.5（GA 5.15）；另 Debian 13/12、RHEL 10.2/10.0/9.8/9.6/9.4/8.10、Oracle Linux 10/9/8、Rocky Linux 9、SLES 16.0/15.7 | 同上，对应条件块（Ubuntu 行条件含全部 Instinct；OL 行 `{"gpu": ["amd-instinct-mi300x"]}` 含 10/9/8；Rocky 行 `{"gpu": ["amd-instinct-mi300x","amd-instinct-mi300a"]}`） | 同上 | 厂商兼容矩阵 | MI325X 的 RHEL 行不含 8.10；OS 表行级差异须逐 GPU 核对，不能按「Instinct 全系」概括 |
| Instinct Linux 驱动支持版本：AMD GPU Driver (amdgpu) 31.60.0、31.50.0、31.40.1、31.40.0、31.30.0、31.20.0、31.10.0、30.30.3、30.30.2、30.30.1、30.30.0、30.20.1、30.20.0、30.10.2 | 同上 "Supported AMD GPU Driver (amdgpu) versions" 行；release notes "Kernel driver and firmware bundle support" 表同列 | 同上 | 厂商兼容矩阵 | 驱动版本与 ROCm 用户态版本是两个序列，配套关系以此表为准 |
| MI300X 固件：PLDM bundle 01.26.00.04（or later）/ 01.25.06.05；固件由 OEM/基础设施方分发（AMD 供 PLDM bundle，OEM 集成分发） | 同上；release notes "Kernel driver and firmware bundle support" 节正文 | 同上 | 厂商兼容矩阵 | 固件包获取路径在 OEM 侧，正文应写「向 OEM 索取并核对版本」 |
| SR-IOV 虚拟化需 GPU-IOV Module (GIM) 9.3.0.K；MI300X 的 KVM passthrough/SR-IOV 配置见矩阵 GPU virtualization support 节 | 兼容矩阵 "GPU virtualization support" 节 | 同上 | 厂商兼容矩阵 | 虚拟化样板未深入取证，正文如需再补 GIM 文档 |

## 主张—证据表（组件职责、版本与编程/运行路径）

| 主张 | 来源与定位 | 版本/日期 | 证据性质 | 反例/未知 |
|---|---|---|---|---|
| ROCm 是 AMD GPU 加速计算的开放软件栈，含 runtimes、compilers、性能/系统工具与数学库；ROCm Core SDK 提供基础组件，生态含 PyTorch 等框架 | [What is ROCm?](https://rocm.docs.amd.com/en/docs-10.1.0/about/what-is-rocm.html) | docs-10.1.0，2026-10-09 观察 | 厂商概念页 | 无 |
| 组件版本总表（10.1.0）：HIP 10.0.0⇒10.1.0、HIPIFY 10.1.0、LLVM 24.0.0、ROCr Runtime 1.21.0、SPIRV-LLVM-Translator 24.0.0；rocBLAS 5.6.0⇒5.7.0、hipBLAS 3.6.0⇒3.7.0、hipBLASLt 1.4.1、MIOpen 3.6.0⇒3.6.1、Composable Kernel 1.3.0、rocFFT 1.0.40、rocSOLVER 3.37.0、rocSPARSE 5.1.0、hipCUB 4.7.0、rocPRIM 4.6.0、rocThrust 4.7.0、rocRAND 5.0.0、rocWMMA 2.2.1、libhipcxx 3.0.2、hipSPARSELt 0.2.9；RCCL 2.30.7、rocSHMEM 3.7.0；AMD SMI 27.0.0⇒27.1.0、rocminfo 1.0.0、RDC 1.3.1；ROCprofiler-SDK 1.4.1、Compute Profiler 3.9.0、Systems Profiler 1.9.0、ROCdbgapi 0.80.0、ROCgdb 16.3、ROCr Debug Agent 2.2.0；hipFile 0.5.0、rocDecode 1.10.0、rocJPEG 1.10.0、RPP 3.2.0 | release notes "ROCm Core SDK components" 表；兼容矩阵页同表（不带 ⇒ 旧版列） | 2026-10-05 / 2026-10-09 | 厂商发布清单 | HIP 与 llvm-project 文档站标题版本与此表不一致（见「缺口与冲突」）；组件支持按 GPU/OS 可变，表头 Important 注明以兼容矩阵为准 |
| HIP 职责：C++ runtime API + kernel 编程语言，面向 AMD GPU、与 CUDA 接口对齐以便移植；runtime 实现在 CLR（Compute Language Runtime）仓库，含 streams/events/memory API；kernel 语言为单源 C++；HIPIFY 把 CUDA 源码转为 HIP C++，但不是 drop-in 替代 | [What is HIP?](https://rocm.docs.amd.com/projects/HIP/en/docs-10.1.0/what_is_hip.html)；[HIP documentation index](https://rocm.docs.amd.com/projects/HIP/en/docs-10.1.0/index.html) | docs-10.1.0（页标题 "HIP 7.16.0 Documentation"），2026-10-09 观察 | 厂商组件文档 | HIP 编程手册在 docs-10.1.0 下位于 how-to/programming_manual.html（user_guide/ 旧路径亦可达）；已登记 src.amd.hip-docs-6.3.3 是旧版本线 |
| ROCr Runtime 职责：AMD 的 HSA（Heterogeneous System Architecture）runtime 实现，是 ROCm 栈中 GPU 执行与管理的基础层 | [ROCm runtimes and compilers](https://rocm.docs.amd.com/en/docs-10.1.0/components/runtimes-and-compilers.html)（"AMD's implementation of the HSA runtime, providing the foundation for GPU execution and management"）；[ROCR documentation](https://rocm.docs.amd.com/projects/ROCR-Runtime/en/docs-10.1.0/index.html)（标题 "ROCR 1.21.0 Documentation"） | docs-10.1.0，2026-10-09 观察 | 厂商组件文档 | HSA 与内核 KFD/ROCk 的分层关系未在单页展开，正文引用概念页措辞即可 |
| 编译器职责：LLVM 24.0.0 是 AMD 的 LLVM 编译器基础设施，含 ROCm 设备编译器 amdclang，编译 HIP 与 OpenCL；hipcc 在 HIPCC 文档（docs-10.1.0，标题 "HIPCC 1.1.1 Documentation"）；过渡指南注明 HIPCC/FLANG 已并入 `amdrocm-llvm` 包 | 同上 runtimes-and-compilers 页；[HIPCC documentation](https://rocm.docs.amd.com/projects/HIPCC/en/docs-10.1.0/index.html)；transition guide "Notable package relocations" | 同上 | 厂商组件文档 | llvm-project 文档站标题显示 22.0.0，与组件表 24.0.0 冲突（见「缺口与冲突」） |
| 数学库分层：roc* 为 HIP 编写的 AMD 原生高性能实现；hip* 为可移植 marshalling 包装层，支持与 CUDA 对应库（rocBLAS↔cuBLAS、rocFFT↔cuFFT、rocSOLVER↔cuSOLVER、rocSPARSE↔cuSPARSE 等）双后端；MIOpen 是开源深度学习原语库；hipBLASLt 提供超越传统 BLAS 的灵活 GEMM API | [ROCm math and compute libraries](https://rocm.docs.amd.com/en/docs-10.1.0/components/math-and-compute-libs.html) 开头与逐条描述 | 同上 | 厂商组件文档 | rocBLAS 5.7.0 起 gfx950 上单/双精度 GEMM 默认改用 hipBLASLt 后端（release notes rocBLAS 变更节），后端默认随代际可变 |
| RCCL 职责：独立的多 GPU/多节点集合通信原语库，针对 AMD GPU 优化，使用 PCIe 与 xGMI 高速互联；公开仓库在 ROCm/rocm-systems | [RCCL documentation](https://rocm.docs.amd.com/projects/rccl/en/docs-10.1.0/index.html)；[ROCm communication libraries](https://rocm.docs.amd.com/en/docs-10.1.0/components/communication-libs.html) | docs-10.1.0（RCCL 2.30.7），2026-10-09 观察 | 厂商组件文档 | 组件表标注 RCCL 仅 Linux |
| rocminfo 职责：HSA 系统信息枚举工具（组件表 "Control and monitoring tools"，rocminfo 1.0.0） | [rocminfo documentation](https://rocm.docs.amd.com/projects/rocminfo/en/docs-10.1.0/index.html)（标题 "rocminfo 1.0.0 Documentation"） | 同上 | 厂商组件文档 | 无 |
| 打包形态（TheRock）：安装目录 `/opt/rocm/core-10.1`，extras 在 `/opt/rocm/extras-10/`；包名 `amdrocm-*`（如 `amdrocm-runtime` 含 HIP/ROCR/runtime compilation、`amdrocm-blas` 含 rocBLAS+hipBLAS+hipBLASLt+hipSPARSELt、`amdrocm-llvm` 含 amdclang++/hipcc/flang、`amdrocm-rccl` 含 rccl、`amdrocm-base` 含 rocminfo+rocm-core）；`amdrocm` meta 包配置 update-alternatives 提供 `/opt/rocm/bin`、`/opt/rocm/lib` 兼容符号链接；按架构分包（-gfx942 对应 gfx94X-dcgpu tarball family） | [Transition guide](https://rocm.docs.amd.com/en/docs-10.1.0/about/transition-guide-TheRock.html) "Major changes"/"Paths and linking"/"Software packages" 各表 | 同上 | 厂商过渡指南 | 旧流包名（rocm-*/roc*/hip*）与新名对照表在该页，迁移类内容应引用 |

## 主张—证据表（PyTorch ROCm 构建关系）

| 主张 | 来源与定位 | 版本/日期 | 证据性质 | 反例/未知 |
|---|---|---|---|---|
| ROCm 10.1.0 AI ecosystem 表：PyTorch 2.14.0（Linux，Python 3.10–3.14；Windows，3.11–3.14）、2.13.0 与 2.12.0（仅 Instinct GPU）；vLLM 0.29.0 与 SGLang 0.5.18 要求 PyTorch 2.13.0 | release notes "AI ecosystem support" 表；兼容矩阵页同表 | 2026-10-05 / 2026-10-09 | 厂商发布文档 | 表内注明框架支持随 GPU/OS 可变，以兼容矩阵为准 |
| ROCm 侧 PyTorch 安装页（ai-ecosystem 项目）提供 Docker 与 pip 两路：Docker 镜像 `rocm/pytorch:rocm10.1.0_ubuntu26.04_py3.14_pytorch_release_2.14.0`（另有 ubuntu24.04_py3.12、ubuntu22.04_py3.10 变体），容器启动挂 `--device /dev/kfd --device /dev/dri --group-add=video`；pip 走 AMD wheel 索引 `https://stable.repo.amd.com/rocm/whl-next/`，按架构选 wheel，如 `torch[device-gfx942]==2.14.0+rocm10.1.0`、`torchvision[device-gfx942]==0.29.0a0+rocm10.1.0`、`torchaudio==2.11.0.3+rocm10.1.0` | [Install PyTorch for ROCm](https://rocm.docs.amd.com/projects/ai-ecosystem/en/latest/frameworks/pytorch/install.html) | latest 可变页，2026-10-09 观察（选择器含 ROCm 10.1.0/10.0.0/7.14.1/7.14.0 × PyTorch 2.14.0/2.13.0/2.12.0） | 厂商安装文档 | 该页为 latest 且无 docs-10.1.0 别名，版本组合可能漂移；引用时记观察日期 |
| PyTorch 官方 get-started：Linux pip 选择器含 ROCm 计算平台选项；"the ROCm build of PyTorch uses the same semantics at the python API level"，验证用 `torch.cuda.is_available()`；源码构建 AMD GPU 需先装 ROCm | [PyTorch Get Started Locally](https://pytorch.org/get-started/locally/) "With ROCm"/"Verification"/"Building from source" 节 | latest 可变页，2026-10-09 观察 | 上游框架文档 | 选择器生成的具体 wheel 命令为 JS 动态内容，未逐版本核对 |
| PyTorch 官方 wheel 索引（download.pytorch.org/whl/）当前 ROCm 目录只到 rocm7.14（另有 rocm3.7–rocm7.2 历史目录）；ROCm 10.x 的 torch wheel 由 AMD 自有索引（stable.repo.amd.com/rocm/whl-next/）分发 | [download.pytorch.org/whl/](https://download.pytorch.org/whl/) 目录列表 | 2026-10-09 观察 | 上游分发索引实查 | 上游是否/何时补 rocm10.x 目录未知；正文应区分「上游 wheel」与「AMD wheel」两个分发渠道 |
| ROCm 侧 PyTorch 安装验证：`python -c "import torch; print(torch.cuda.is_available())"` 输出 True 表示 PyTorch 与 ROCm 安装正确且 GPU 可见 | Install PyTorch for ROCm 页 "Verify your PyTorch installation" | latest，2026-10-09 观察 | 厂商安装文档 | 仅文档样板，未运行 |
| ROCm 侧 PyTorch 已知问题：导入时 rocSHMEM 报 libnuma 缺失消息（装 libnuma-dev/numactl-devel 可消除，不影响正常运行）；部分 RDNA 推理负载 PyTorch<2.14 性能偏低，workaround `TORCH_BLAS_PREFER_HIPBLASLT=1`（2.14 起为这些架构默认值）；Radeon 训练负载 GPU reset 问题 workaround `TORCH_BLAS_PREFER_HIPBLASLT=0` | 同页 "Known issues" 节 | 同上 | 厂商已知问题 | 训练 reset 问题在 10.1.0 release notes 中列为已解决（Llama-Factory/Unsloth on RX 9070/R9700），两处口径并存，引用时区分版本语境 |

## 主张—证据表（安装前提、验证入口与典型故障）

| 主张 | 来源与定位 | 版本/日期 | 证据性质 | 反例/未知 |
|---|---|---|---|---|
| 五种安装方式：package manager（apt/dnf/zypper，系统级）、amdgpu-install（仅 Radeon/Ryzen）、pip（venv）、tarball（免 root/自定义目录）、Runfile（引导式、可含驱动）；包管理器安装为 apt 注册 stable.repo.amd.com/rocm/core/packages/ubuntu{2604,2404,2204}/ 仓库（GPG key: stable.repo.amd.com/rocm/gpg/packages.gpg）后 `sudo apt install amdrocm10.1`（或按架构 `amdrocm10.1-gfx942` 等） | [Install AMD ROCm 10.1.0](https://rocm.docs.amd.com/en/docs-10.1.0/install/rocm.html) "Compare installation methods" 表、"Register ROCm repositories"、"Install ROCm packages" 节 | docs-10.1.0，2026-10-09 观察（选择器单页，全部变体内嵌） | 厂商安装指南 | 页面为选择器驱动单页，锚点含选择器状态串；引用指页面+方法名 |
| 内核驱动单独安装：Instinct/Radeon 需 AMD GPU Driver (amdgpu)，文档在 instinct.docs.amd.com amdgpu-docs；Ubuntu 24.04 为注册 `https://repo.radeon.com/amdgpu/31.60/ubuntu noble main`（key: repo.radeon.com/rocm/rocm.gpg.key）后 `sudo apt install amdgpu-dkms`，装完重启；卸载 `sudo apt autoremove amdgpu-dkms`；Ryzen APU 用发行版 inbox 驱动 | [Ubuntu native installation — amdgpu 31.60.0](https://instinct.docs.amd.com/projects/amdgpu-docs/en/docs-31.60.0/install/detailed-install/package-manager/package-manager-ubuntu.html) | docs-31.60.0，2026-10-09 观察 | 厂商驱动安装文档 | 装新驱动前须先卸载旧 AMDGPU 驱动（页面 Caution）；dkms 与内核版本的实际匹配未验证 |
| GPU 访问权限两种方式：组成员（默认 video 与 render 组，`sudo usermod -a -G render,video $LOGNAME`；video 管视频设备、render 管 DRM render node）或 udev 规则（`/etc/udev/rules.d/70-amdgpu.rules`：`KERNEL=="kfd", GROUP="render", MODE="0666"` 与 `SUBSYSTEM=="drm", KERNEL=="renderD*", GROUP="render", MODE="0666"`）；改完需重启生效；容器环境在宿主机上配置 | install/rocm.html "Configure permissions for GPU access"（Post-installation） | 同上 | 厂商安装指南 | 未配置权限时 /dev/kfd 与 /dev/dri/renderD* 不可访问是本步骤的存在理由，页面未单列「权限不足报错」排错条目 |
| 安装后验证入口：`rocminfo`（枚举 HSA agent，示例输出含 gfx950/MI350X 与 "ROCk module version 6.16.6 is loaded"）；`amd-smi version`（示例输出 "AMDSMI Tool: 27.1.0+7da43026 | AMDSMI Library version: 27.1.0 | ROCm version: 10.1.0 | amdgpu version: 7.1.9.31600000"）；pip 路径 `pip freeze | grep rocm` 与 `rocm-sdk` CLI；Windows 用 `hipinfo` | install/rocm.html "Verify your installation"（Post-installation） | 同上 | 厂商安装指南 | 示例输出为厂商样例，非本库实测 |
| 卸载/回退边界：`sudo apt autoremove amdrocm10.1`（及各架构变体）；旧流 ROCm 7.2.4 或更早版本须先卸载再装 10.1.0（"If you have ROCm 7.2.4 or older installed, please uninstall it before proceeding"） | install/rocm.html "Uninstalling" 与 "Installation" Note | 同上 | 厂商安装指南 | 未给出跨大版本（7.14→10.1）原地升级路径的明确声明，正文按「先卸后装」写 |
| 文档化配套/装载故障（release notes 10.1.0 known issues，选录）：MI350 系列上 RCCL allreduce 走 LL 协议可能产生错误结果（workaround：`export NCCL_PROTO=LL128,Simple`，GitHub issue #8792）；MI200 系列上 device-to-device hipMemcpyAsync 可能失败；部分 Instinct GPU 上多应用负载可能遇到间歇 GPU page fault；MI350P 上 RAS 错误注入/查询不可用 | release notes "ROCm known issues" 节 | 2026-10-05 / 2026-10-09 | 厂商已知问题 | 已知问题随 release 滚动，正文引用须固定 docs-10.1.0 |
| 验收级验证（Instinct system acceptance，MI300X 页）：流程为 Prerequisites Validation → Basic Health Checks → System Validation → Performance Benchmarks；健康检查含 `sudo lspci -d 1002:74a1`（应见 8 GPU）、`lspci -vvv` 看 LnkSta 32GT/s x16、`amd-smi monitor -putm` 空闲指标、dmesg 驱动错误（有错则重装 amdgpu）、内核启动参数（如 `pci=realloc=off iommu=pt`）；性能门槛示例：TransferBench a2a ≥32.9 GB/s、p2p 单向 ≥33.9/双向 ≥43.9 GB/s；rccl-tests `all_reduce_perf -b 8 -e 8G -f 2 -g 8` bus BW ≥304 GB/s；rocblas-bench FP32 ≥94100 / BF16 ≥130600 / INT8 ≥162700 GFLOPS；BabelStream 8 卡阈值（Copy ≥4,177,285 MB/s 等） | [AMD Instinct MI300X system acceptance](https://instinct.docs.amd.com/projects/system-acceptance/en/latest/gpus/mi300x.html)；[Basic system health checks](https://instinct.docs.amd.com/projects/system-acceptance/en/latest/common/health-checks.html)；[System Validation](https://instinct.docs.amd.com/projects/system-acceptance/en/latest/common/system-validation.html) | latest 可变页，2026-10-09 观察 | 厂商验收文档 | latest 无版本别名，阈值随文档更新可变；示例输出取自 Ubuntu 22.04 系统，文档自述其他发行版输出可能略异 |
| RVS（ROCm Validation Suite，`sudo apt install rocm-validation-suite`）模块：gpup（属性）、gst（GEMM 压力，目标 GFLOPS `met: TRUE`）、iet（功耗压力）、gm（温度/风扇/时钟/功耗 violations 0）、mem（内存测试，带宽约 2 TB/s）、pebb/peqt（PCIe 带宽/资格，peqt 需 sudo）、pbqt（P2P）；MI300X 专用 conf 在 `/opt/rocm/share/rocm-validation-suite/conf/MI300X/`；AGFHC 为更完整的现场健康检查工具，需向 AMD customer success 索取安装 | system-validation.html "RVS Validation"/"AGFHC Validation" 节 | 同上 | 厂商验收文档 | AGFHC 获取路径非公开下载；RVS 多数模块无 PASS/FAIL 判定，文档自述以「输出在合理范围」为准 |
| ROCm Bandwidth Test 已 EOL：自 TheRock 架构的 ROCm 7.14.0 起 end-of-life，官方指引改用 TransferBench 或 RVS；ROCm SMI 亦移除，由 AMD SMI 替代 | transition guide "ROCm Core SDK component changes (moved or removed)" 节 | docs-10.1.0，2026-10-09 观察 | 厂商过渡指南 | 已登记 src.amd.rocm-bandwidth-test-d7f5efe 仍是有效源码证据，但正文须注明其在 10.x 流中已 EOL，不能作为 10.1.0 的推荐验证工具 |

## 主张—证据表（许可）

| 主张 | 来源与定位 | 版本/日期 | 证据性质 | 反例/未知 |
|---|---|---|---|---|
| ROCm 按组件分别授权。主要组件：HIP/HIPCC/CLR/hipBLAS/hipBLASLt/MIOpen/rocBLAS/rocFFT/rocRAND/rocSPARSE/hipFFT/hipSOLVER/hipSPARSE/hipSPARSELt/rocPRIM/rocRAND/rocWMMA/MIGraphX/AMD SMI/ROCm SMI Lib/rocminfo 以外的多数工具为 MIT；ROCR-Runtime、rocminfo、ROCr Debug Agent、Comgr、ROCm-Device-Libs 为 The University of Illinois/NCSA；RCCL 为 Custom；hipCUB 为 Custom；ROCK-Kernel-Driver 为 GPL 2.0 WITH Linux-syscall-note；llvm-project 为 Apache（flang 为 Apache 2.0）；libhipcxx、hipThreads 为 Apache 2.0 with LLVM Exceptions；rocThrust 为 Apache 2.0；rocSOLVER 为 BSD-2-Clause；ROCgdb 为 GPLv3；TransferBench、ROCm Validation Suite、ROCm Bandwidth Test 为 MIT | [ROCm licenses](https://rocm.docs.amd.com/en/docs-10.1.0/about/license.html) "ROCm component licenses" 表 | docs-10.1.0，2026-10-09 观察 | 厂商许可页 | 「Custom」未在该页展开，需查各仓库 LICENSE；RCCL 的 Custom 正文引用时保持原文措辞 |
| 文档仓库本体为 MIT（页面顶部全文）；包内许可文本位置 `/opt/rocm/share/doc/<component-name>/`；开源组件经 GitHub 与 repo.radeon.com 发布，专有组件在 repo.radeon.com 的 proprietary 子目录；ROCprof Trace Decoder 与 AOCC 二进制另有许可协议 | 同页 MIT 全文、"Package licensing" 节 | 同上 | 厂商许可页 | 页面尾部法律声明 ©2023-2025 与 MIT 头 ©2023-2026 并存，照录即可 |

## 候选新来源登记

建议 ID 格式 `src.<org>.<slug>-<version-or-date>`；kind 与许可状态按 registry.yaml 现有惯例填写。未标注「latest」的均为版本化固定 URL。

| 建议 ID | 标题 | URL | kind | 许可状态 |
|---|---|---|---|---|
| src.amd.rocm-release-notes-10.1.0 | ROCm Core SDK 10.1.0 release notes | https://rocm.docs.amd.com/en/docs-10.1.0/about/release-notes.html | official-docs | AMD 文档（页面 MIT/文档条款），2026-10-05 |
| src.amd.rocm-compatibility-matrix-10.1.0 | ROCm 10.1.0 compatibility matrix | https://rocm.docs.amd.com/en/docs-10.1.0/compatibility/compatibility-matrix.html | official-docs | 同上；选择器页面，引用需注明 GPU/OS 选择状态 |
| src.amd.rocm-install-docs-10.1.0 | Install AMD ROCm 10.1.0 | https://rocm.docs.amd.com/en/docs-10.1.0/install/rocm.html | official-docs | 同上 |
| src.amd.rocm-therock-transition-docs-10.1.0 | Transition guide from legacy ROCm release stream | https://rocm.docs.amd.com/en/docs-10.1.0/about/transition-guide-TheRock.html | official-docs | 同上 |
| src.amd.rocm-license-docs-10.1.0 | ROCm licenses | https://rocm.docs.amd.com/en/docs-10.1.0/about/license.html | official-docs | 同上 |
| src.amd.rocm-what-is-rocm-docs-10.1.0 | What is ROCm? | https://rocm.docs.amd.com/en/docs-10.1.0/about/what-is-rocm.html | official-docs | 同上 |
| src.amd.rocm-components-docs-10.1.0 | ROCm 组件职责页组（runtimes-and-compilers / math-and-compute-libs / communication-libs） | https://rocm.docs.amd.com/en/docs-10.1.0/components/runtimes-and-compilers.html 等 | official-docs | 同上 |
| src.amd.hip-docs-10.1.0 | HIP 文档（docs-10.1.0，站标 7.16.0） | https://rocm.docs.amd.com/projects/HIP/en/docs-10.1.0/index.html | official-docs | 同上；版本标注冲突见下 |
| src.amd.rocr-runtime-docs-10.1.0 | ROCR-Runtime 文档（1.21.0） | https://rocm.docs.amd.com/projects/ROCR-Runtime/en/docs-10.1.0/index.html | official-docs | 同上 |
| src.amd.rocblas-docs-10.1.0 | rocBLAS 文档（5.7.0） | https://rocm.docs.amd.com/projects/rocBLAS/en/docs-10.1.0/index.html | official-docs | 同上 |
| src.amd.hipblas-docs-10.1.0 | hipBLAS 文档（3.7.0） | https://rocm.docs.amd.com/projects/hipBLAS/en/docs-10.1.0/index.html | official-docs | 同上 |
| src.amd.miopen-docs-10.1.0 | MIOpen 文档（3.6.1） | https://rocm.docs.amd.com/projects/MIOpen/en/docs-10.1.0/index.html | official-docs | 同上 |
| src.amd.rccl-docs-10.1.0 | RCCL 文档（2.30.7） | https://rocm.docs.amd.com/projects/rccl/en/docs-10.1.0/index.html | official-docs | 同上 |
| src.amd.rocminfo-docs-10.1.0 | rocminfo 文档（1.0.0） | https://rocm.docs.amd.com/projects/rocminfo/en/docs-10.1.0/index.html | official-docs | 同上 |
| src.amd.rocm-llvm-docs-10.1.0 | ROCm LLVM compiler infrastructure 文档（站标 22.0.0） | https://rocm.docs.amd.com/projects/llvm-project/en/docs-10.1.0/index.html | official-docs | 同上；版本标注冲突见下 |
| src.amd.hipcc-docs-10.1.0 | HIPCC 文档（1.1.1） | https://rocm.docs.amd.com/projects/HIPCC/en/docs-10.1.0/index.html | official-docs | 同上 |
| src.amd.rocm-pytorch-install-2026-10-09 | Install PyTorch for ROCm（ai-ecosystem，latest） | https://rocm.docs.amd.com/projects/ai-ecosystem/en/latest/frameworks/pytorch/install.html | official-docs | 同上；latest 可变，登记观察日期 |
| src.amd.amdgpu-driver-docs-31.60.0 | AMD GPU Driver (amdgpu) 31.60.0 Ubuntu native installation | https://instinct.docs.amd.com/projects/amdgpu-docs/en/docs-31.60.0/install/detailed-install/package-manager/package-manager-ubuntu.html | official-docs | 同上 |
| src.amd.instinct-mi300x-system-acceptance-2026-10-09 | AMD Instinct MI300X system acceptance（latest） | https://instinct.docs.amd.com/projects/system-acceptance/en/latest/gpus/mi300x.html | official-docs | 同上；latest 可变 |
| src.amd.instinct-health-checks-2026-10-09 | Basic system health checks（latest） | https://instinct.docs.amd.com/projects/system-acceptance/en/latest/common/health-checks.html | official-docs | 同上 |
| src.amd.instinct-system-validation-2026-10-09 | System Validation（RVS/AGFHC，latest） | https://instinct.docs.amd.com/projects/system-acceptance/en/latest/common/system-validation.html | official-docs | 同上 |
| src.pytorch.get-started-locally-2026-10-09 | PyTorch Get Started Locally（含 ROCm 选择器与验证语义） | https://pytorch.org/get-started/locally/ | upstream-docs | PyTorch 文档（BSD-3-Clause 站点条款） |
| src.pytorch.whl-index-2026-10-09 | PyTorch 官方 wheel 索引目录列表 | https://download.pytorch.org/whl/ | upstream-artifact | 索引实查，2026-10-09 |

已有可复用登记：`src.amd.amd-smi-docs-10.1.0`（与本样板同 release）、`src.amd.hip-docs-6.3.3`（旧版本线，仅历史对照）、`src.amd.rocm-bandwidth-test-d7f5efe`（工具在 10.x 已 EOL，仅作历史/源码证据）、`src.amd.instinct-mi300x-platform-datasheet-2023`（硬件代际规格）。

## 缺口与冲突

- **HIP 文档站版本标注冲突**：`projects/HIP/en/docs-10.1.0/` 全站标题为 "HIP 7.16.0 Documentation"（curl 复核 title 标签确认），而 release notes 组件表写 "HIP 10.0.0 ⇒ 10.1.0"。两个均为 AMD 官方发布口径，未能判定哪一个是 HIP 制品的真实版本号；正文引用组件版本时应以 release notes 组件表为准，并注明文档站标注差异。
- **llvm-project 文档站版本标注冲突**：`projects/llvm-project/en/docs-10.1.0/` 标题为 "llvm-project 22.0.0 Documentation"，release notes 组件表写 "LLVM 24.0.0"。处理方式同上。
- **PyTorch wheel 分发渠道分叉**：download.pytorch.org/whl/ 的 ROCm 目录 2026-10-09 只到 rocm7.14；ROCm 10.x 的 torch wheel 只在 AMD 索引 stable.repo.amd.com/rocm/whl-next/（10.1.0）与 repo.amd.com/rocm/whl-multi-arch/（7.14.x 示例）分发。正文不能把「PyTorch 官方 wheel 支持 ROCm 10.1.0」写成既成事实；应写「AMD 分发带 rocm10.1.0 本地版本标识的 wheel」。
- **选择器页面不可深链**：compatibility-matrix.html 与 install/rocm.html 的全部 GPU/OS/方法变体内嵌于单页、由 JS 按选择器状态显隐，无稳定 URL 表达「MI300X+Ubuntu 24.04」选择状态。本取证从 HTML `data-show-cond` 条件块提取逐 GPU 行；正文引用此类页面须注明选择器状态与观察日期。
- **Radeon/Ryzen 范围未展开**：取证以 Instinct（MI300X 为主）为主线；Radeon（gfx120x/gfx110x）与 Ryzen（gfx115x）的矩阵行、虚拟化行只在核对选择器结构时扫过，未逐字段记录。
- **Windows/WSL2 路径未取证**：HIP SDK on Windows 与 WSL2 technical preview（10.1.0 起 TheRock 产物含 librocdxg）仅见 release notes 段落，未展开。
- **GIM/虚拟化驱动文档未取证**：SR-IOV 需要 GIM 9.3.0.K，仅记录矩阵声明，未打开 Instinct Virtualization Driver 文档。
- **AGFHC 与 Cluster Validation Suite 细节未核对**：AGFHC 安装「需联系 AMD customer success」，无公开下载；CVS 配置仅见验收文档描述。
- **已登记 amd-smi 来源的一处旧捕获**：registry 注记中 amd-smi CLI 内嵌示例显示 "Version: 27.0.0 | ROCm version: 7.14.0"（旧版捕获），与本样板 10.1.0 的 27.1.0 页面版本不冲突，但正文引用 amd-smi 输出示例时须注明版本语境。
- **「装载故障」官方排错材料有限**：权限（video/render、udev）、驱动重装（dmesg 有错 → reinstall amdgpu）、旧版先卸载等散落在安装指南与健康检查页；未发现面向「KFD 初始化失败/驱动-用户态版本不匹配」的独立排错页面（amd-smi 文档注记过「内核侧无独立 GPU recovery 文档页」的类似缺口）。正文应按「文档未提供专门排错页」如实标注。
