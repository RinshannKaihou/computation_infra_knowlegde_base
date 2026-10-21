---
id: software-stack.environment-installation-and-upgrade
title: 三平台安装基线、迁移升级与回退验证
type: procedure
domain: software-stack
status: draft
platforms: [generic, nvidia, ascend, amd]
source_refs:
  - src.nvidia.cuda-12-8-installation-guide-linux
  - src.nvidia.driver-installation-guide-latest-2026-10-21
  - src.nvidia.driver-readme-580.105.08
  - src.nvidia.cuda-forward-compatibility-2026-10-09
  - src.nvidia.cuda-compatibility-latest-2026-09-30
  - src.nvidia.framework-containers-user-guide-2026-09-30
  - src.nvidia.cuda-samples-bandwidthtest-2026-10-08
  - src.nvidia.cuda-samples-v12.8
  - src.huawei.cann-83rcx-install-2026-09-29
  - src.huawei.cann-83rcx-upgrade-uninstall-2026-10-21
  - src.ascend.torch-npu-7.2.0-install-guide-2026-10-09
  - src.amd.rocm-install-docs-10.1.0
  - src.amd.rocm-compatibility-matrix-10.1.0
  - src.amd.rocm-release-notes-10.1.0
  - src.amd.rocm-bandwidth-test-d7f5efe
  - src.amd.rocm-install-linux-prerequisites-7.2.4
  - src.vllm-ascend.issue-1188
updated_at: "2026-10-21"
summary: 按 NVIDIA/CUDA、Ascend/CANN、AMD/ROCm 三份文档样板构造安装验证梯子、迁移升级变化矩阵与回退边界；全部步骤来自官方文档，未在任何环境执行。
related_ids:
  - software-stack.compatibility-evidence
  - software-stack.layers-and-boundaries
  - software-stack.nvidia-documented-profile
  - software-stack.ascend-documented-profile
  - software-stack.amd-rocm-documented-profile
  - software-stack.ascend-version-mismatch-triage
  - software-stack.runtime-execution-and-library-loading
  - software-stack.host-resource-pressure-and-device-access
  - hardware.node-acceptance-triage
applicability:
  environment_refs: []
  notes: "本文是三份固定文档样板（CUDA 12.8、CANN 8.3.RCX、ROCm 10.1.0）上的安装/升级/回退方法档案，不是可直接部署的环境清单；未建立环境档案，未执行任何安装、升级或卸载命令。现场执行依据既有授权与变更窗口。"
verification:
  status: source_checked
  evidence_refs:
    - src.nvidia.cuda-12-8-installation-guide-linux
    - src.nvidia.driver-installation-guide-latest-2026-10-21
    - src.huawei.cann-83rcx-upgrade-uninstall-2026-10-21
    - src.amd.rocm-install-docs-10.1.0
  notes: 已对照所列官方文档核对本文各步骤、命令名与回显描述；核对范围以各来源 notes 记录的章节为准。未在任何 GPU/NPU 主机执行；命令可用性、结果与回退效果不经本文证明。
---

# 三平台安装基线、迁移升级与回退验证

环境安装不是"装完一个包"的单步操作：目标硬件与 OS 支持、固件/驱动、用户态库、实际装载路径、后端设备初始化、最小算子/同步、直到结果检查，任何一层跳过都会把问题推迟到训练或推理作业里才暴露。本文按 NVIDIA/CUDA、Ascend/CANN、AMD/ROCm 三份固定文档样板，给出一条安装验证梯子、一张迁移升级变化矩阵和回退边界。所有步骤与命令来自官方文档原文；本文未在任何环境执行它们。

三个平台样板各自绑定文档线：CUDA 12.8 归档文档、CANN community 8.3.RCX 安装指南（页头 8.3.RCX、URL 路径 83RC1，沿用既有登记的版本标识边界）、ROCm docs-10.1.0。`generic` 表示梯子结构跨平台通用，不表示三平台步骤、包名或回退能力等价。

## 目标与触发条件

- 新节点或返修节点首次部署某平台软件栈，需要一条可判定的安装验收路径。
- 计划迁移（换 OS/驱动/运行时/框架后端/引擎版本）或升级平台组件，需要变化清单、兼容约束与恢复对照。
- 升级或变更失败后需要回退，需要事先确认回退路径存在且未越不可逆边界。

被动证据层的节点验收（带外健康、事件记录）见[节点验收分诊](../01-hardware/node-acceptance-triage.md)；本文只覆盖主动安装/升级/回退的软件栈层。

## 变更前准入门禁（先于一切步骤）

出现以下任一情况，**停止实际变更**（可以继续查证，但不执行安装/升级/卸载）：

| 缺项 | 判定 | 处置 |
|---|---|---|
| 完整依赖交集缺失 | 硬件×OS×驱动×运行时×框架/引擎的任一环节查不到配套依据 | 按 [兼容性证据方法](compatibility-evidence.md) 补证；补不到即停止 |
| 有效 baseline 缺失 | 变更前没有可复跑的最小验证结果（见下文 B0） | 首次安装例外：记录"安装前状态"与清理目标；已有环境的升级没有 baseline 即停止 |
| 恢复路径未落实 | 回退方案未落定（含制品保全与不可逆确认） | 先完成回退准备一节的检查，再执行变更 |

证据状态与操作门槛分开记录：**查不到支持证据时操作上不放行，但证据状态保持 `unknown`**；只有来源明确否定支持、或声明为封闭全集的支持表按其规则缺席时，才可记为"不支持"（判定规则见[兼容性证据方法](compatibility-evidence.md)）。把抓取失败或查询工具不可用写成"平台不支持"是错误归类。

## 安装验证梯子（七层，逐层判定）

每层分别记录**所需证据**、**该证据能证明的状态**与**仍不能证明的部分**；任一层失败，先在该层定位（进入对应诊断正文），不要继续向上安装。

| 层 | 检查对象 | 所需证据 | 能证明 / 不能证明 | 失败时进入 |
|---|---|---|---|---|
| L1 硬件/OS 支持 | 目标加速器型号 × OS/内核在所选文档的支持表内 | 官方支持表条目（含版本号与读取日期） | 能证明文档线内支持/不支持/unknown；不能证明其他版本组合 | [兼容性证据方法](compatibility-evidence.md) |
| L2 固件/驱动 | 驱动已加载设备、固件与驱动版本身份可读 | 官方查询命令返回设备与驱动/固件版本信息 | 能证明驱动加载与版本身份；设备文件存在只是部分证据，不等于全部驱动条件满足 | [主机资源压力与设备访问](host-resource-pressure-and-device-access.md) |
| L3 用户态库 | toolkit/runtime/算子包安装且版本配套 | 包管理器登记（或 .run 安装回显）与配套表一致 | 能证明安装动作完成与登记身份；覆盖不了页内其他安装方式时按各自制品记录 | 各平台档案（见文末连接） |
| L4 实载路径 | 目标进程实际加载的库与版本 | 对运行中进程记录实载库身份（方法见[驱动初始化与库装载](runtime-execution-and-library-loading.md)） | 环境脚本/`PATH`/`LD_LIBRARY_PATH` 指向某版本只是必要条件，**不能证明进程实载**；实载无法采集时本层记未完成 | [驱动初始化与库装载](runtime-execution-and-library-loading.md) |
| L5 后端设备初始化 | 框架/运行时后端能枚举并初始化设备 | 平台验证命令/样例列出设备且无异常 | 能证明后端可用路径存在；不证明全部算子或功能可用 | [框架后端适配](framework-backend-adaptation.md) |
| L6 最小算子/同步 | 一个最小计算或传输用例执行 | 官方样例运行及其自带校验 | 样例自带校验的性质见下节；不含数值契约时不能证明计算正确性 | [GPU 算子/图执行失败](gpu-op-graph-failure-triage.md) |
| L7 结果检查 | 用例输出可核对 | 输出与官方示例/判据比对通过 | "命令没报错"不是本层通过标准 | 本文各平台"结果检查"行 |

L2 与 L5 是两个不同状态：驱动枚举设备（L2）不等于框架后端初始化成功（L5）；这与[设备资源状态链](../05-cluster-platform/device-resource-chain.md)的分层一致。

### 最小算子/同步与结果契约（三平台统一说明）

官方安装验证样例的判据由**样例自带校验**定义，它们覆盖"安装可用"层面，不等于计算正确性验证：

- NVIDIA：`deviceQuery` 核对设备枚举与属性（"a device was found"、"the test passed"）；`bandwidthTest` 为传输测量，其通过判据由样例自身给出。样例不包含逐元素数值比较。
- Ascend：官方推理样例输出 top1–top5 概率，与样例示例信息比对的是**输出形态**。
- AMD：`rocminfo`/`amd-smi` 为设备与工具级检查；rocm_bandwidth_test 为传输测量。

三平台的最小运算/同步/结果检查**方法入口**与待冻结字段：

| 平台 | 最小运算方法入口 | 同步/错误语义入口 | 待冻结契约字段 |
|---|---|---|---|
| NVIDIA | cuda-samples：`vectorAdd`（[v12.8 固定 tag](https://github.com/NVIDIA/cuda-samples/tree/v12.8/Samples/0_Introduction/vectorAdd)，含自带结果校验）、`bandwidthTest`（[v12.8 固定 tag](https://github.com/NVIDIA/cuda-samples/tree/v12.8/Samples/1_Utilities/bandwidthTest)，传输） | [驱动初始化与库装载](runtime-execution-and-library-loading.md)的 stream/event 同步与错误发现时机节（CUDA 侧样板） | 输入、预期输出、容差、同步点、错误码 |
| Ascend | 官方推理样例（[instg_0094](https://www.hiascend.com/doc_center/source/zh/CANNCommunityEdition/83RC1/softwareinst/instg/instg_0094.html)"运行推理样例"） | 同上正文的 CANN 侧初始化/同步样板 | 同上 |
| AMD | rocm_bandwidth_test（传输，固定 commit）；hip 级运算样例未在本文冻结，引用前另行登记 | 同上正文的 HIP 侧样板 | 同上 |

**这些字段未冻结时，L6/L7 只能记录"样例自带校验通过"，最终安装/升级验收不能记通过**（B0/N/R 对照同样以冻结契约为前提）。本文不定义数值；把样例通过写成"计算正确"会高估安装状态。

注意：运行时篇固定的样板版本为 CANN 8.2.RC1.alpha001 与 HIP 6.3.42134（docs-6.3.3 文档线），与本文档线（CANN 8.3.RCX、ROCm 10.1.0）不同——上表入口只提供**旧版方法样板**；目标文档线上的接口、样例与适用条件须另核，未核时对应验证环节保持未完成。

## NVIDIA（CUDA 12.8 样板）

以下步骤来自 CUDA 12.8 安装指南（归档版本化页）与驱动安装指南（latest 可变页，2026-10-21 观察，示例分支 575/580）；固定 580.105.08 README 只用于设备文件语义，两者分立不合并。

| 层 | 官方步骤与命令 | 来源定位 |
|---|---|---|
| L1 | 安装前动作：核对 GPU 型号与 Linux/gcc 版本；选择包管理器或 runfile 方式，先处理冲突安装方法（"Handle Conflicting Installation Methods"要求先移除与所选方式冲突的既有安装） | [CUDA 12.8 Installation Guide](https://docs.nvidia.com/cuda/archive/12.8.0/cuda-installation-guide-linux/index.html) Ch.2 |
| L2 | Ubuntu：安装 linux-headers 后启用驱动仓库——local 方式安装 `nvidia-driver-local-repo-...` 包并复制其 keyring，network 方式安装 `cuda-keyring` 包——随后 `apt install nvidia-open`，重启；`apt update` 前完成对应 GPG keyring 配置。本层证据分三项登记：**安装身份**（驱动包名与版本）、**设备节点**（/dev/nvidiactl、/dev/nvidia[0-9]+ 必须存在且应用用户可读写，默认 0666——必要条件）、**已加载身份**（官方核验方法：驱动指南 Post-installation Actions 的 "Verify the Driver Version"——`cat /proc/driver/nvidia/version` 核验已加载版本，latest 页 2026-10-21 核读；本批首登该来源时仅核读 Ubuntu/version-locking 两节，本节为复核轮补充核读并已补入登记。缺该证据时本层记未完成，不以 L5 deviceQuery 成功倒填） | [Driver Installation Guide · Ubuntu](https://docs.nvidia.com/datacenter/tesla/driver-installation-guide/latest/ubuntu.html)；[README 580.105.08 Ch17B/Ch7](https://download.nvidia.com/XFree86/Linux-x86_64/580.105.08/README/README.txt) |
| L3 | 安装 `cuda-toolkit-12-8` 元包（该表列元包不含驱动；含驱动的组合另见元包表）；多版本可并列安装——注意上游同节并列句写 `cuda-toolkit-X.Y`、锁定句写 `cuda-toolkit-X-Y`、表列为 `cuda-toolkit-12-8`，模板不一致照录，本文引用一律用具体坐标 `cuda-toolkit-12-8` | 同 L1 §3.12.2/§3.12.3.7 |
| L4 | 安装后配置环境；并列多版本的切换经 update-alternatives（指南 §10.3.3）；实载库身份按梯子 L4 的方法另记。容器场景遵循"驱动不入镜像"原则（驱动属宿主，镜像带 toolkit/框架运行时） | 同 L1 §10；[Frameworks Containers User Guide](https://docs.nvidia.com/deeplearning/frameworks/user-guide/index.html) |
| L5/L6 | 官方验证走 cuda-samples：构建并运行 `deviceQuery`（核对找到的设备与系统一致、"test passed"），再运行 `bandwidthTest`；注意该验证节未以 `nvidia-smi`/`nvcc -V` 作为判据，且提示缺 /dev/nvidia* 文件会失败、SELinux 系统可能需临时 `setenforce 0` | 同 L1 §10.2.2；[bandwidthTest 样例（v12.8 固定 tag）](https://github.com/NVIDIA/cuda-samples/tree/v12.8/Samples/1_Utilities/bandwidthTest)（master 树入口在本轮连接器读取不稳定，正文一律用固定 tag 树） |
| L7 | deviceQuery 输出设备参数且 Result = PASS；bandwidthTest 按样例自带判据通过 | 同上 |

停止条件：L2 设备文件缺失或权限不符→先按 README 语义修宿主驱动层；L5 deviceQuery 找不到设备→回 L2/L4，不先改应用配置。

## Ascend（CANN 8.3.RCX 样板）

以下步骤来自 CANN community 安装指南（物理机场景为主；场景选择页区分物理机/虚拟机/容器）、安装后配置页与 Ascend Extension for PyTorch 7.2.0 安装指南。

| 层 | 官方步骤与命令 | 来源定位 |
|---|---|---|
| L1 | 先选安装场景（物理机/虚拟机/容器）与安装类型（在线 Conda/Yum、离线 .run）；OS 兼容性按官方查询工具/说明核对（交互查询工具静态抓取只得外壳，具体机型×OS 结果未取得——该组合保持 `unknown`，不记为不支持） | [选择安装场景](https://www.hiascend.com/doc_center/source/zh/CANNCommunityEdition/83RC1/softwareinst/instg/instg_0000.html)；[torch-npu 7.2.0 insg_0001](https://www.hiascend.com/document/detail/zh/Pytorch/720/configandinstg/instg/insg_0001.html) |
| L2 | 安装/确认 NPU 驱动与固件：`npu-smi info` 返回驱动/固件版本信息且无异常才继续（升级页明示"若返回驱动相关信息说明加载成功"——本样板的已加载身份证据）；未安装则按"安装NPU驱动和固件"页操作（固件与驱动为两个包，分别登记版本） | [快速安装](https://www.hiascend.com/document/detail/zh/CANNCommunityEdition/83RC1/softwareinst/instg/instg_quick.html)安装前准备；instg_0005 |
| L3 | 安装 CANN 软件包（示例 `conda install ascend::cann-toolkit==8.3.RC1`，或 Yum `Ascend-cann-toolkit-8.3.RC1`，或离线 `.run --install`）；训练/推理场景按配套关系安装 Toolkit+Kernels+NNAL（配套版本以《CANN 软件安装指南》为准，安装页不钉版本） | 同 L2 快速安装表；[insg_0002](https://www.hiascend.com/document/detail/zh/Pytorch/720/configandinstg/instg/insg_0002.html) |
| L4 | 安装后配置：`source .../ascend-toolkit/set_env.sh`（或手动 export `ASCEND_TOOLKIT_HOME`/`LD_LIBRARY_PATH`/`PATH` 等，见该页环境变量清单）；安装运行依赖 g++ 与指定 Python 第三方库（如 `protobuf==3.20.0`、`numpy>=1.19.2,<=1.24.0`）。环境脚本为必要条件，进程实载另按 L4 方法记录 | [安装后配置 instg_0094](https://www.hiascend.com/doc_center/source/zh/CANNCommunityEdition/83RC1/softwareinst/instg/instg_0094.html) |
| L5/L6/L7 | 运行官方推理样例：下载快速入门样例，按 README 准备模型与测试图片、编译并运行；安装正确时输出 top1–top5 概率（与样例示例信息比对——形态比对，见上文结果契约说明） | 同 L4 安装后配置"运行推理样例" |

停止条件：`npu-smi info` 无返回→驱动/固件层（L2）未就绪，不装 CANN；样例编译失败但 L2–L4 已过→按[算子/图执行失败](ascend-op-graph-failure-triage.md)分诊。版本配套错配的症状与调查见[昇腾版本错配分诊](ascend-version-mismatch-triage.md)。

## AMD（ROCm 10.1.0 样板）

以下步骤来自 ROCm docs-10.1.0 安装页（选择器驱动单页，引用指页面＋方法名）与兼容性矩阵（MI300X 视图经原始 HTML 条件块核对）。

| 层 | 官方步骤与命令 | 来源定位 |
|---|---|---|
| L1 | OS/内核支持查兼容性矩阵（MI300X：Ubuntu 24.04.5 GA 6.8 等；矩阵为选择器页，引用指页面+选择器组合并带观察日期）；内核/用户态兼容另见矩阵页链接 | [compatibility matrix](https://rocm.docs.amd.com/en/docs-10.1.0/compatibility/compatibility-matrix.html)；[release notes](https://rocm.docs.amd.com/en/docs-10.1.0/about/release-notes.html) |
| L2 | 内核驱动（amdgpu）是独立步骤：Instinct/Radeon 的包管理器路径先装独立驱动包（页面 Install the kernel driver 步骤）；Ryzen 路径可用发行版 inbox 驱动（按页面条件句）；runfile 安装器有单独 amdgpu 目标（可含或不含驱动）。**安装身份**（驱动包/来源与版本）在本层登记；**已加载身份**——本文档线的加载确认即 Post-installation 的 `rocminfo`（来源原句"确认 ROCm runtimes 和 drivers 已正确安装并加载"），即本样板中 L2 与 L5 共用同一验证命令，属文档线自身的分层合并，如实记录，不以其他方式拆造；**固件信息**——安装页未提供独立的固件版本查询证据，本项保持 `unknown`/未完成，不以 rocminfo 结果补齐 | [Install ROCm 10.1.0](https://rocm.docs.amd.com/en/docs-10.1.0/install/rocm.html)（Install the kernel driver 步骤） |
| L3 | 用户态 ROCm 包：五种安装方式（包管理器 apt/dnf/zypper、amdgpu-install（仅 Radeon/Ryzen）、pip venv、tarball、runfile）按官方对比表选择；apt 路径注册 stable 仓库后 `sudo apt install amdrocm10.1`（或按架构 `amdrocm10.1-gfx942`） | 同上（Install ROCm 步骤） |
| L4 | GPU 访问：默认 `video`+`render` 双系统组（`usermod -a -G render,video $LOGNAME`），或写 /etc/udev/rules.d/70-amdgpu.rules（kfd 与 renderD* 规则）后重启；容器环境此步必须在宿主机执行；runfile 安装器对应 `gpu-access=user|all`。组与权限是访问条件，实载库身份仍按 L4 方法另记 | 同 L2；组语义另见 [7.2.4 prerequisites](https://rocm.docs.amd.com/projects/install-on-linux/en/docs-7.2.4/install/prerequisites.html)（版本映射随页注明） |
| L5 | 验证安装：`rocminfo` 列出检测到的 AMD GPU 并确认 ROCm runtime 与驱动已加载（这是 L5 的整体反馈，L2 的驱动身份仍以本层登记为准，不用它倒填）；`amd-smi version` 核对系统信息（pip 安装另有 `which rocm-sdk`、`ls .venv/bin`） | 同上 Post-installation |
| L6/L7 | 传输级用例走 rocm_bandwidth_test（固定 commit 样板）；输出与设备规格和工具文档核对——传输测量不含计算正确性契约（见上文） | [rocm_bandwidth_test @d7f5efe](https://github.com/ROCm/rocm_bandwidth_test/tree/d7f5efe854b82baa21f34a978841e341de354b97) |

停止条件：`rocminfo` 列不出 GPU→回 L2/L4（驱动未装或权限组未生效，注销/重启前用户组不生效）；页内卸载/回退能力边界见下节。

## 迁移与升级变化矩阵

升级前先填这张表：**十一类改变项逐项登记"变/不变"**，每项有独立约束来源与重检层；"官方支持升级"不构成整表放行。

| 改变项 | NVIDIA（CUDA 12.8 样板） | Ascend（CANN 8.3.RCX 样板） | AMD（ROCm 10.1.0 样板） | 检查层 |
|---|---|---|---|---|
| hardware（加速器/整机） | 换卡重跑 L1 支持表；驱动与 toolkit 兼容按支持表重核 | 机型×OS 兼容重查（查询工具，结果 unknown 时停止） | 兼容性矩阵按新 GPU 重查（架构如 gfx942/gfx950 勿混） | L1 全部重查 |
| OS/内核 | 随 CUDA 安装指南支持表核对新 OS/内核（Ch.2） | 场景选择页与 OS 兼容说明重查；升级后"确保所有软件满足版本配套关系"（升级前必读） | 兼容性矩阵重查（10.1.0 OS 支持窗口随版本更新，release notes） | L1＋L2 |
| 驱动（driver/固件） | 驱动升级随仓库 `apt dist-upgrade`；版本锁定经 `nvidia-driver-pinning-<分支/版本>` 锁包（建议先装锁包；APT Pin-Priority>=1000 允许降级；Ubuntu 580 及以前包名带分支、590 起去分支化）——version-locking 节 | 固件>驱动>CANN 顺序；`.run --upgrade` 后必须 reboot，再 `npu-smi info` 验证（升级固件和驱动，instg_0029） | amdgpu 驱动随所选安装方式更新；7.2.4 及以下旧流须先卸载再装（页内多处要求） | L2＋L5 重跑 |
| runtime（toolkit/CANN/ROCm 主包） | `cuda-toolkit-12-8` 并列安装＋update-alternatives 切换（§10.3.3）；minor version compatibility 与 cuda-compat 前向兼容边界另查（compat 包仅对特定分支标支持，R545 不在列） | CANN 升级在 yum/conda 指定目标版本号或 `.run --upgrade`（升级 CANN，instg_0030）；Toolkit 升级前磁盘要求"可用>已占用+10G"（`df -h`/`du -sh`）——升级 CANN 节 | meta 包随仓库升级（`amdrocm10.1` 等）；pip 路径按 venv 重装 | L3＋L4 |
| library（独立库/算子包） | 独立库（cuBLAS 等）随 toolkit 元包；单独改动按包坐标登记 | **跟随 Toolkit/NNAE/NNRT 安装的 Kernels，在升级宿主包时会被自动卸载，须按配套表重装**；独立安装的 Kernels（8.0.0 起支持）按其配套另判 | kernels 等组件随 ROCm 包 | L3＋L6 |
| framework（PyTorch/torch_npu 等） | 框架容器内 runtime 与宿主驱动兼容另核（framework containers 指南） | torch_npu 与 CANN/驱动固件配套（如 vLLM Ascend issue #1188 记录的 0.9.0×CANN 8.1.RC1×torch 2.5.1 组合建议——版本化安装建议，不构成配套证明） | PyTorch ROCm 构建按 vLLM ROCm 安装文档核架构与版本（无预编译 wheel 等边界见该文档） | L5＋L6 |
| backend（设备后端/插件） | 后端插件与驱动/runtime 接口匹配 | torch_npu 后端属 framework 配套；容器插件挂载见容器安装登记 | HIP 后端随 ROCm | L5 |
| engine（推理/训练引擎） | 引擎支持按各自矩阵重核（07 域档案） | 同左；MindIE 档案线另核 | 同左（vLLM ROCm 支持矩阵） | 引擎级验证 |
| model/config/input | 模型格式、量化、配置与输入分布的改变独立登记；量化×图等组合冲突不因升级消解（07 域档案） | 同左 | 同左 | 结果契约层 |
| （不变项） | 每次变更显式登记"本次不变"的项，避免隐式假设 | 同左 | 同左 | — |

每行通过判据＝该行 L 层验证重跑通过＋升级后版本配套核对；只看安装命令回显不算通过。

### baseline/变更/恢复对照（B0/N/R 方法）

矩阵之外，每次变更按三状态对照执行，三者使用**同一负载、同一判据**：

| 状态 | 定义 | 必须记录 |
|---|---|---|
| B0（变更前基线） | 变更前环境上按上文梯子 L5–L7（及受影响层）跑出的结果 | 环境身份（版本清单）、负载/输入身份、判据与输出、日期 |
| N（变更后） | 同一负载在变更后环境重跑 | 同上＋变更清单（对应矩阵中"变"的行） |
| R（恢复后） | 回退执行后同一负载再跑 | 同上＋回退动作记录 |

判读：N 与 B0 一致（在预登记容差内）→ 变更通过；N 异常→按矩阵检查层分诊；R 与 B0 一致→回退成功，否则回退未完成。首次安装没有 B0：以"安装前状态记录＋安装目标清单"替代，清理/卸载时以此为恢复目标；本文不虚构未运行过的基线。

## 回退与不可逆边界

回退在变更前就要落定，不是失败后的即兴操作。

### 变更前的回退准备

- **制品保全（区别于全量卸载）**：保全对象＝准确版本/变体的包或镜像及其摘要、依赖清单、仓库/镜像快照、现场配置与数据。NVIDIA 保留旧版经 `cuda-toolkit-12-8` 并列安装实现；当应用依赖 `/usr/local/cuda` 等软链接且旧 toolkit 完整保留时，可经 update-alternatives 选择已安装版本（§10.3.3）——切换后须重启相关进程并按 L4 复核实载，且这只覆盖该场景；显式版本路径、容器/框架自带 runtime、驱动与缺失制品按各自恢复路径处理，不把 alternatives 当作整个 NVIDIA 栈的回退定义；CANN 离线 .run 保留原包；ROCm 按安装方式保留包/venv/tarball 制品。仓库与镜像快照三平台都须自行留存（文档不承诺旧制品可得）。
- **不可逆确认**：固件升级须 reboot 生效且公开文档未见固件层降级路径（`unknown`，变更前向支持渠道确认）；数据/模型转换/状态格式变化（量化导出、checkpoint 格式迁移等）逐项确认可逆性或有备份，不可逆者在变更窗口内不可回退。
- **恢复判据**：R 状态与 B0 同判据对比（见上节），不是"服务起来了"。

### 各平台回退路径与卸载（来源定位）

- **NVIDIA**：驱动经 `nvidia-driver-pinning-<版本>` 锁包＋`apt-get -V dist-upgrade --autoremove` 降级到指定版本（指南 Debian 示例从 580.103 降 57 个包到 570.199）；Pin-Priority>=1000 是允许降级的前提（version-locking 节）。toolkit：runfile 安装用 toolkit bin 内 `cuda-uninstaller`（§5.4）；包管理器安装按指南 §11 通配 purge（cuda/cublas/cufft/…/nvvm）＋`autoremove --purge -V`——**注意通配会同时命中并列安装的旧版本，全量卸载与"保留旧版回退"是两条不同路径，混用会破坏并列基线**（此为命令模式语义推断，未执行验证）。
- **Ascend**：官方升级须知明示**"如果需要从高版本回退至低版本，需卸载高版本后重新安装所需版本"——没有原地降级路径**（升级前必读，instg_0028）。卸载定位（instg_0032/0033）：CANN 脚本卸载（推荐）按包分列——Toolkit/NNRT 为 `<安装路径>/ascend-toolkit|nnrt/<version>/<arch>-linux/script`、NNAE 为 `<安装路径>/nnae/<version>/script`、Kernels 为对应包 `opp_kernel/script`、NNAL 为 `<安装路径>/nnal/atb/<version>/scripts`，各目录执行 `./uninstall.sh`；或 `xxx.run --uninstall`（读取 /etc/Ascend/ascend_cann_install.info 或 $HOME/Ascend/ 下配置的 Install_Path）。Yum 卸载按 Kernels>CANN 顺序、Conda 用 `conda remove ascend::xxx`。驱动与固件分别卸载：`/usr/local/Ascend/driver/script/uninstall.sh` 与 `/usr/local/Ascend/firmware/script/uninstall.sh`（两者无先后顺序要求）。升级默认作用于安装目录下 latest 软链接指向版本；旧版本目录在升级后是否原样保留，所读页面未说明——`unknown`，保全以自留 .run 制品为准。
- **AMD**：安装页 Uninstalling 节按安装方式分列——包管理器卸载（`sudo apt autoremove amdrocm10.1` 及 gfx942/gfx950 等架构变体）、Remove ROCm repositories（`sudo rm /etc/apt/sources.list.d/amdrocm-stable.sources`）与缓存清理（`sudo rm -rf /var/cache/apt/*`、`sudo apt clean`、`sudo apt update`），另有 venv/tarball/runfile 分支；旧流 7.2.4 及以下必须先卸载再装新版。**完整版本回退与依赖恢复能力**（降级回旧版本并恢复依赖至可用）未见专门说明（`unknown`）——回退方案必须在变更前按自留制品落定，不依赖页内承诺。

### 不可逆与高危操作

固件升级（reboot 生效）；升级过程"禁止进行其他维护操作"且"会导致业务中断"（CANN 升级前必读原文），应提前切走或停止业务；跨大版本原地升级路径未见官方明确声明处（如 ROCm 7.x→10.1），按先卸后装处理并在门禁处停核。

### 恢复门槛

回退完成后按**实际受影响的层**重跑梯子（至少 L2/L5/L6/L7；触及 L1/L3/L4 的变更同样重查），并与 B0 同判据对比；跨层状态另按各自恢复验证入口核对（训练状态见 [Checkpoint 恢复一致性](../06-training/checkpoint-state-consistency.md)，服务恢复见[服务版本发布、副本故障与恢复验证](../07-inference/release-and-recovery.md)），不以设备可见为完成。

## 与相邻正文的连接

- 依赖交集为什么不能证明整栈支持、`unknown`/`conflict` 的处理：[兼容性证据方法](compatibility-evidence.md)。
- 三平台文档样板档案：[NVIDIA](nvidia-documented-profile.md)、[Ascend](ascend-documented-profile.md)、[AMD ROCm](amd-rocm-documented-profile.md)。
- 错配症状分诊：[昇腾版本错配](ascend-version-mismatch-triage.md)（含公开案例与实验设计）；驱动/库装载层：[驱动初始化与库装载](runtime-execution-and-library-loading.md)。
- 上层框架与引擎的安装不在本文：PyTorch/torch_npu 配套见 06 域执行档案，vLLM/MindIE 见 07 域各安装与档案正文。

## 来源与验证记录

全部来源见 frontmatter `source_refs`；关键主张的页内定位已随各表格"来源定位"列与回退小节就近给出。本文为 draft、`source_checked`：已对照官方文档核对步骤与命令名，未在任何环境执行安装、升级或卸载；"实际安装已成功"不由本文声明，实跑验证由独立验证轨道（V00 环境准备起）承接。NVIDIA 驱动指南为 latest 可变页（2026-10-21 观察，示例分支 575/580）；CANN 指南沿用 8.3.RCX/83RC1 版本标识不一致的既有边界；ROCm 矩阵为选择器页、引用带观察日期。
