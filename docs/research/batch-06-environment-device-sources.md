# 第六批 T01/T02 环境与设备场景来源准备

交付日期：2026-09-30。本记录为 T01“昇腾版本配套失败”和 T02“容器内 NPU 不可见”各自的流程、来源案例与实验设计准备证据。公开资料于 2026-09-30 只读核对；没有安装软件、拉取镜像、运行上游项目、访问集群或使用 NPU。

## backlog 身份与边界

| 任务 | 标题 | 稳定 ID | 目标路径 |
|---|---|---|---|
| T01-P | 昇腾版本配套失败诊断指南 | `software-stack.ascend-version-mismatch-triage` | `knowledge/02-software-stack/ascend-version-mismatch-triage.md` |
| T01-C | 昇腾版本配套失败来源案例 | `software-stack.ascend-version-mismatch-source-case` | `knowledge/02-software-stack/ascend-version-mismatch-source-case.md` |
| T01-X | 昇腾版本配套失败验证实验设计 | `software-stack.ascend-version-mismatch-experiment` | `knowledge/02-software-stack/ascend-version-mismatch-experiment.md` |
| T02-P | 容器内 NPU 不可见诊断指南 | `cluster-platform.ascend-device-visibility-triage` | `knowledge/05-cluster-platform/ascend-device-visibility-triage.md` |
| T02-C | 容器内 NPU 不可见来源案例 | `cluster-platform.ascend-device-visibility-source-case` | `knowledge/05-cluster-platform/ascend-device-visibility-source-case.md` |
| T02-X | 容器内 NPU 不可见验证实验设计 | `cluster-platform.ascend-device-visibility-experiment` | `knowledge/05-cluster-platform/ascend-device-visibility-experiment.md` |

T01 只诊断“当前制品身份是否落在一个明确发行快照的配套声明中，以及失败在哪一层”。它不把源码主干、分支名、wheel 版本和 CANN/HDK 版本拼成一个组合。T02 沿用 F11 的状态链，分开主机驱动、设备插件、节点资源账本、Pod 分配、容器访问和框架枚举；HCCL 初始化失败只有在前述层次已核对后才进入通信专题，不能自动改写成“设备不可见”。

## 复用的现有正文和来源

| 对象 | 本批用途 | 边界 |
|---|---|---|
| [昇腾软件栈的文档配套档案](../../knowledge/02-software-stack/ascend-documented-profile.md) | T01 的固定版本样板 | 固定 TorchNPU tag `v7.2.0-pytorch2.6.0` 解引用 commit `bc51ab84cc6f35c77aab1c59886e0ea43681a317`；不代表最新推荐或本地可用 |
| [如何判断版本配套是否有依据](../../knowledge/02-software-stack/compatibility-evidence.md) | 把官方支持与本地验证分成两条轴 | `supported/unsupported/unknown/conflict` 与 `passed/failed/not_run/inconclusive` 不能互相替代 |
| [从物理设备到容器资源的状态链](../../knowledge/05-cluster-platform/device-resource-chain.md) | T02 的层次和责任 | 物理存在、驱动可见、插件上报、资源账本、分配、容器访问和框架可用不是同一状态 |
| [证据、假设与排障闭环](../../knowledge/08-reliability/evidence-and-hypotheses.md) | 两个流程的证据/假设表达 | 症状不等于根因；结论必须绑定实体、时间和支持/反对证据 |
| `src.ascend.torch-npu-v7.2.0-pytorch2.6.0` | T01 发行矩阵、安装前提和快速验证样板 | 固定 commit；根 LICENSE 为 BSD-3-Clause，历史快照无独立 docs/LICENSE |
| `src.huawei.cann-83rcx-install-2026-09-29` | T01 的驱动/固件在宿主机的责任边界 | 页面 URL 含 83RC1、页头为 8.3.RCX；不能补齐固定历史 HDK 版本 |
| `src.kubernetes.device-plugins-v1-32` | T02 Register、ListAndWatch、Allocate、资源账本语义 | Kubernetes v1.32 文档，不代表现场版本 |
| `src.ascend.mind-cluster-v26.1.1` | T02 的固定 Ascend Device Plugin / Docker Runtime 实现样板 | 固定 commit `44385c13d7b1d87def35f1604e8be4d16de6ca4e`；未与上述 TorchNPU/CANN 快照做整栈配套 |

## T01：官方机制来源核对

固定 TorchNPU README 的实际位置如下：

- [安装段](https://github.com/Ascend/pytorch/blob/bc51ab84cc6f35c77aab1c59886e0ea43681a317/README.md#installation)先要求安装 CANN，再给 PyTorch 与 `torch-npu` wheel 的示例；固定文件第 13、22/28、54 行分别承载这些声明。
- [Quick Verification](https://github.com/Ascend/pytorch/blob/bc51ab84cc6f35c77aab1c59886e0ea43681a317/README.md#quick-verification)的固定文件第 115–128 行只做两个 NPU tensor 的矩阵乘法。它可以作为最小功能样板，不能证明上层服务、通信或目标模型正确。
- [PyTorch/Python 表](https://github.com/Ascend/pytorch/blob/bc51ab84cc6f35c77aab1c59886e0ea43681a317/README.md#pytorch-and-python-version-matching-table)第 134–146 行把 PyTorch 2.6.0 对应到 Python 3.9.x、3.10.x、3.11.x。
- [Ascend Auxiliary Software 表](https://github.com/Ascend/pytorch/blob/bc51ab84cc6f35c77aab1c59886e0ea43681a317/README.md#ascend-auxiliary-software)第 148–162 行把 CANN 8.3.RC1、PyTorch 2.6.0、Extension 2.6.0.post3 和分支 `v2.6.0-7.2.0` 放在同一发行快照中。

固定矩阵支持“这些值在该 README 同一行被声明为配套”，不支持以下推断：具体硬件型号和 HDK 自动满足、下载 wheel 与源码 commit 字节一致、vLLM/MindSpeed/MindCluster 也纳入组合、源码 `master` 的新矩阵可以解释旧事故。

### T01-P 的证据分支

| 分支 | 必需观察 | 可形成的判断 | 不能形成的判断 |
|---|---|---|---|
| 身份未固定 | 包版本、构建标签、镜像 digest、Python ABI、CANN 子包、驱动/固件、OS/架构中任一关键项缺失 | `unknown`，先补证据 | “版本不兼容”或“官方支持” |
| 与同一固定矩阵直接冲突 | 实际 PyTorch/torch_npu/CANN/Python 明确落在不同矩阵行，且无目标发行说明覆盖 | 官方支持轴可记为 `conflict` 或 `unsupported`，仍需按来源措辞区分 | 冲突一定是当前报错的唯一根因 |
| 矩阵一致、导入或动态链接失败 | 制品身份一致，但 import、共享库或符号解析在框架初始化前失败 | 包来源、ABI、加载路径、制品完整性成为优先假设 | CANN、驱动或硬件必然正常 |
| 导入成功、ACL/运行时接口缺失 | torch/torch_npu 可导入，调用设备运行时或最小算子失败 | CANN 子包、运行时/驱动接口和环境加载成为优先假设 | 上层服务版本一定匹配 |
| 最小算子通过、上层服务失败 | 固定 quick verification 或等价最小功能通过，目标应用仍失败 | 转向上层引擎/插件、模型或通信条件 | 底层整栈已被全面验证 |
| 只有 HCCL 初始化或 collective 失败 | 设备已枚举，失败发生在通信初始化/执行 | 移交通信专题，并保留版本和设备证据 | “容器看不到 NPU”或“版本不匹配”已被证明 |

流程的停止条件应包括：无法确认制品来源或同一时点；需要修改共享环境、驱动、固件或生产镜像但没有隔离/回退；候选矩阵来自 `master` 而事故是发行版本；现有证据同时支持多个层次且无法设计低影响区分检查。完成判据应要求：每个实际制品有稳定身份；只用同一固定发行资料做支持判断；本地最小验证状态单独记录；未排除假设保持 `unknown`。

### T01-C：选定 vLLM Ascend #1188

[Issue #1188](https://github.com/vllm-project/vllm-ascend/issues/1188)是可用但存在未解项的真实来源案例：

| 时间（GitHub UTC） | 可确认事件 | 证据与限制 |
|---|---|---|
| 2025-06-12 | 报告者给出 vLLM 0.9.0、vLLM Ascend 0.9.0、CANN 8.1.RC1，并称已装 torch/torch_npu 2.5.1；问题是 vLLM 0.9.0 会要求 torch 2.7.0，而当时没有相应 TorchNPU | [Issue 正文](https://github.com/vllm-project/vllm-ascend/issues/1188)；缺硬件、驱动/固件、OS、Python、镜像/wheel 摘要和实际错误全文 |
| 2025-06-15 02:40 | 项目成员回复当前应使用 torch 2.5.1，指向版本化 `v0.9.0rc2` 安装页，并解释先安装 vLLM、再安装 vLLM Ascend 时依赖会把 torch 调整回 2.5.1 | [关键评论](https://github.com/vllm-project/vllm-ascend/issues/1188#issuecomment-2973444343)；评论另有一句把 `python 2.5.1` 写入上下文，正文不能把这句扩写成 Python 版本声明 |
| 2025-06-15 03:00 | 同一成员询问是否还有问题，Issue 随后标记 completed | [后续评论](https://github.com/vllm-project/vllm-ascend/issues/1188#issuecomment-2973451049)与 Issue 状态；没有报告者贴出重装、启动或最小算子复验 |

该案例可以支持“安装顺序和上游/后端的 torch 约束发生冲突时，要固定整组依赖并看版本化发行说明”。它不能支持“建议步骤已在报告者环境修复”，也不能外推到 TorchNPU 2.6/CANN 8.3.RC1。关闭为 completed 是项目状态，不是本库的复现实验。

未选用的 T01 候选：

- [vLLM Ascend #1401](https://github.com/vllm-project/vllm-ascend/issues/1401)有较完整版本和 `aclmdlRICaptureBegin` 缺失，但同一日志还出现 vLLM `_C` undefined symbol；页面无评论、无关联 PR，关闭原因和修复未知。
- [vLLM Ascend #3190](https://github.com/vllm-project/vllm-ascend/issues/3190)称跨平台驱动不一致，但日志残缺，Issue 以 `wontfix` 关闭且无评论/PR，不能确认根因或修复。
- [vLLM Ascend #11928](https://github.com/vllm-project/vllm-ascend/issues/11928)有更完整的 2026 年 CPU-only 文档修复链，但使用 main/dev 与无 NPU 环境；它适合作为独立文档案例，不应与本批固定发行样板混写。

### T01-X 的设计边界

实验必须先选择一个**完整且可取得的发行基线**。固定 TorchNPU README 提供的候选核心为 CANN 8.3.RC1、PyTorch 2.6.0、torch-npu 2.6.0.post3、Python 3.9/3.10/3.11；但 HDK、硬件型号、OS/内核、CANN 子包、wheel 来源与摘要尚未由同一来源补齐，所以当前只能写实验设计，不能把这组值直接当可执行基线。

建议矩阵：

| 组 | 控制变量 | 变更 | 预期用途 |
|---|---|---|---|
| B0 | 固定硬件、HDK、OS、Python、镜像、CANN 子包、PyTorch、torch_npu | 全部采用已核实基线 | 建立 import、设备枚举和固定 quick verification 的参照 |
| N1 | 与 B0 相同 | 只把 PyTorch 改为不在同一矩阵行的版本 | 验证包解析/import/符号错误的可观测边界，不预设必然失败方式 |
| N2 | 与 B0 相同 | 只把 torch_npu 改为其他发行制品 | 区分 extension 与 PyTorch/CANN 的配套影响 |
| N3 | 与 B0 相同 | 只改变 CANN 用户态子包，保留 HDK | 区分 import 与运行时/算子阶段；仅在可隔离、可回退环境执行 |
| R0 | 恢复 B0 | 撤销变更并重跑同一输入 | 证明环境可回到基线，避免把节点漂移当版本效应 |

每组记录包摘要、加载到的动态库、退出状态、设备数、最小算子输出和错误首现层；重复次数和阈值必须执行前确定。任何驱动/固件变更需要专用节点和明确恢复方案，本设计默认不做。通过指“B0 与 R0 满足预先定义的最小功能，而单变量组的差异可重复且只关联该变量”；若基线本身失败、制品身份漂移或多个变量同时变化，则结论为无法判断。

## T02：官方机制与固定实现核对

MindCluster `v26.1.1` 固定 commit 中，本轮实际打开两个精确文件：

1. [Docker client usage](https://github.com/Ascend/mind-cluster/blob/44385c13d7b1d87def35f1604e8be4d16de6ca4e/docs/en/scheduling/usage/containerization/02_usage_on_the_docker_client.md)：固定文件第 49–64 行要求在容器内外核对设备节点、驱动目录、DCMI 和 `npu-smi`；第 109 行说明需要 NPU 时必须指定 `ASCEND_VISIBLE_DEVICES`，`void` 表示不挂载 NPU、驱动或目录。
2. [Ascend Device Plugin installation](https://github.com/Ascend/mind-cluster/blob/44385c13d7b1d87def35f1604e8be4d16de6ca4e/docs/en/scheduling/developer_guide/installation_deployment/manual_installation/04_ascend_device_plugin.md)：固定文件第 5–7 行说明哪些调度场景需要插件；第 31–40 行说明 Docker Runtime 的安装顺序、版本一致和重启 container engine 条件，并列 Atlas 200I SoC A1 例外；第 44–53 行记录 DCMI 路径所有权、权限、深度和 `LD_LIBRARY_PATH` 长度限制。

这些文档与 F11 已核对的固定代码共同支持：插件通过 Register/ListAndWatch 上报，通过 Allocate 返回设备节点或 runtime 环境信息。它们不能证明某现场已经执行了这些步骤，也不能证明一个用户态工具的失败等于设备节点不存在。

### T02-P 的证据分支

| 层次 | 同一实体/时点应观察什么 | 异常时的优先假设 | 不能跳到的结论 |
|---|---|---|---|
| 主机与驱动 | 节点身份、物理设备清单、驱动枚举和健康 | 硬件/固件/驱动、设备被占用或管理库异常 | 插件、Pod 或容器一定有问题 |
| 插件 | 插件 Pod/进程、Register 资源名、ListAndWatch 的 ID/health 和时间 | 插件未注册、DCMI/权限/版本/重启条件、上报中断 | 调度器一定已看到最新值 |
| 节点资源账本 | 目标资源名的 capacity/allocatable、更新时间 | kubelet 状态未收敛、设备 unhealthy、资源名不一致 | 某 Pod 已获得具体设备 |
| 调度与分配 | Pod UID、节点绑定、资源 request/limit、kubelet 分配和 Allocate 请求/响应 | 无资源请求、请求名错误、调度不足、Allocate 失败 | runtime 已应用返回配置 |
| 容器访问 | container ID/最终配置、设备节点、权限、挂载、runtime 注入环境 | hook/runtime 未应用、security policy、节点/库/目录缺失 | 框架后端一定可用 |
| 用户态/框架 | 同一容器、同一用户、同一进程看到的设备数、ID 命名空间、初始化和最小选择 | 物理/逻辑 ID 混用、库/ABI、权限、框架后端 | HCCL 或模型一定正确 |

停止条件：节点/Pod/container/device identity 对不上；需要重启 container engine、插件、kubelet 或修改生产安全策略而没有批准和回退；插件/runtime 版本交集未知；只有 HCCL 错误而设备节点、枚举和单卡选择均已通过。完成判据：在同一时间窗口串起主机、插件、资源、分配、容器和目标进程证据；目标进程只枚举已分配设备并能选择它们；未检查通信/模型时不得写成整个工作负载恢复。

### T02-C：选定 vLLM Ascend #2557 与 PR #2541

该公开案例的价值在于“容器内有设备”和“框架能正确使用设备 ID”发生了分叉，而不是一个简单的设备节点缺失案例。

| 时间（GitHub UTC） | 可确认事件 | 证据与解释边界 |
|---|---|---|
| 2025-08-26 | [Issue #2557](https://github.com/vllm-project/vllm-ascend/issues/2557)报告 Kubernetes Pod 请求 4 个 `huawei.com/Ascend910`；环境为 Ubuntu 22.04 aarch64、torch/torch_npu 2.5.1/2.5.1.post1、vLLM 0.9.1、vLLM Ascend dev commit `f6a0e1629`、CANN 8.2.RC1 | `npu-smi` 在容器中列出 0、3、4、7 且健康，说明这不是“所有设备节点均缺失”的证据模式 |
| 2025-08-26 | 报告者从 `/dev/davinci*` 得到 0、3、4、7 并写入 `ASCEND_RT_VISIBLE_DEVICES`；torch_npu 初始化报输入范围 `[0-4)`，4/7 无效，随后设备计数/选择失败 | 错误文本支持物理 ID 与容器逻辑 ID 混用；不能据此推断所有 Kubernetes/CANN 版本都采用相同映射 |
| 2025-09-01 | 另一用户报告多节点场景遇到同类错误 | [评论](https://github.com/vllm-project/vllm-ascend/issues/2557#issuecomment-3241077552)只有症状相似陈述，没有完整环境或复验 |
| 2025-09-03 | 贡献者称 cherry-pick [PR #2541](https://github.com/vllm-project/vllm-ascend/pull/2541)可处理该问题，同时明确这不是最佳方案，未来可能在 Mooncake TE 侧改进 | [关键评论](https://github.com/vllm-project/vllm-ascend/issues/2557#issuecomment-3247467513)；属于维护者/贡献者建议，不等于报告者复验 |
| 2025-09-03 | PR #2541 合入 `main`，merge commit `07d44ade194b018ae2cc172482d55cb746c5fd0e`；页面记录 25 checks passed、两次 approval 和新增单元测试 | 固定代码在 [`envs.py`](https://github.com/vllm-project/vllm-ascend/blob/07d44ade194b018ae2cc172482d55cb746c5fd0e/vllm_ascend/envs.py#L138-L141)新增 `PHYSICAL_DEVICES`，在 [`mooncake_connector.py`](https://github.com/vllm-project/vllm-ascend/blob/07d44ade194b018ae2cc172482d55cb746c5fd0e/vllm_ascend/distributed/mooncake_connector.py#L759-L778)按 DP/TP 切片物理 ID；测试只覆盖 `PHYSICAL_DEVICES="10,11"` 时默认 rank 选择 10 |
| 2025-09-03 | 审阅者称当前改法是 hack，作者回复未来寻找更稳健方式 | [审阅评论](https://github.com/vllm-project/vllm-ascend/pull/2541#discussion_r2319156564)和[作者回复](https://github.com/vllm-project/vllm-ascend/pull/2541#discussion_r2319163741)；应把补丁限定为当时 Mooncake connector 的实现 |
| 2025-12-18 | Issue 作者把 Issue 关闭为 completed | 关闭发生在补丁合入后，但 Issue 没有贴出同一集群的复测日志、镜像版本或发行版本；“现场已修复”仍未知 |

该案例同时保留两个设备命名空间：容器中实际暴露的物理编号 0/3/4/7，以及 torch_npu 在该容器进程内接受的逻辑范围 0–3。PR 使用新增 `PHYSICAL_DEVICES` 为 Mooncake/TE 连接保留物理 ID，而不应被改写成“所有框架都必须设置此变量”或“把 `/dev` 编号写入 `ASCEND_RT_VISIBLE_DEVICES`”。

未选用的 T02 候选：

- [cann-container-image #63](https://github.com/Ascend/cann-container-image/issues/63)给出 CANN 8.5.0 镜像和非 root 用户下 DCMI 初始化失败，但仍为 open、无评论/PR，也没有证明设备节点不存在。
- [cann-container-image #46](https://github.com/Ascend/cann-container-image/issues/46)只有容器内 `npu-smi` 的 DCMI `device is used` 错误，缺镜像启动参数、版本和处理时间线。
- [vLLM Ascend #9490](https://github.com/vllm-project/vllm-ascend/issues/9490)是非 root 下 TP>1 的 HCCL 初始化失败；作者的派生镜像同时改变用户条目和环境变量，且设备文件已由 runtime 暴露，不能作为 NPU 不可见案例。
- [vLLM Ascend #6942](https://github.com/vllm-project/vllm-ascend/issues/6942)显式挂载设备，且无其他容器时服务可启动；更接近设备占用/资源隔离，关闭为 stale/not planned，不能证明不可见。

### T02-X 的设计边界

实验要把状态链逐层记录，不能只比较一次框架报错。

| 组 | 资源/容器条件 | 预期用途 |
|---|---|---|
| B0 | 健康专用节点、固定插件/runtime/镜像，Pod 正确请求 1 个 NPU | 正控制；应有插件上报、资源分配、容器设备节点和框架 1 个逻辑设备 |
| C0 | 同节点/镜像，不请求 NPU；与 B0 一样排除 privileged、设备 hostPath、人工挂载/显式旁路注入，并确认 runtime 无默认设备注入 | 仅此前提成立时用作无分配/无容器设备的负控制；否则无法据“不请求”推断不可见 |
| N1 | 正确请求设备，但在隔离容器中刻意使用未经映射的物理 ID 作为框架逻辑 ID | 复现命名空间错误的边界；不运行模型或 HCCL |
| R0 | 撤销 N1，恢复正常注入和逻辑 ID | 回退对照；排除设备健康漂移或插件状态变化 |

每组至少记录节点、Pod UID、container ID、资源名、分配设备 ID、插件 `ListAndWatch`/`Allocate` 时序、最终设备节点/权限/挂载/环境，以及同一用户进程的设备数和逐设备选择。B0/C0/R0 应在同一镜像和时间窗内重复；若节点健康、插件或调度状态变化，结论为无法判断。实验会临时占用设备和调度容量；只能用专用节点/命名空间，停止前不得重启共享 runtime、kubelet 或插件。通过标准是 B0/R0 的整条链一致、C0 明确无分配、N1 只在 ID 映射层出现预期差异；这不验证 HCCL、模型加载、性能或数值正确性。

## 新来源登记 YAML proposals

以下条目按 `schemas/sources.schema.json` 编写。本子任务不修改共享 registry；Issue 评论属于用户生成内容，不能用仓库 Apache-2.0 许可证覆盖。

```yaml
  - id: src.vllm-ascend.issue-1188
    title: "vLLM Ascend Issue #1188：v0.9.0 与 torch 版本关系"
    url: https://github.com/vllm-project/vllm-ascend/issues/1188
    kind: issue
    registered_at: "2026-09-30"
    revision: "issue opened 2025-06-12; maintainer comments and completed close observed 2026-09-30"
    license:
      status: unknown
      scopes: []
      notes: GitHub Issue 正文与评论为用户生成内容；仓库根 Apache-2.0 不能自动覆盖讨论文本。本库只保存链接、短摘要和原创时间线，不复制长段正文。
    notes: 核对报告者列出的 vLLM 0.9.0、vLLM Ascend 0.9.0、CANN 8.1.RC1 与 torch/torch_npu 2.5.1，项目成员 2025-06-15 的版本化安装建议及 completed 状态；没有报告者复验、硬件/HDK/OS/Python/wheel 摘要或关联修复 PR，不把关闭状态写成已复现修复。
  - id: src.vllm-ascend.issue-2557
    title: "vLLM Ascend Issue #2557：Kubernetes 容器中的物理与逻辑 NPU ID"
    url: https://github.com/vllm-project/vllm-ascend/issues/2557
    kind: issue
    registered_at: "2026-09-30"
    revision: "issue opened 2025-08-26; comments, linked PR and completed close observed 2026-09-30"
    license:
      status: unknown
      scopes: []
      notes: GitHub Issue 正文与评论为用户生成内容；仓库根 Apache-2.0 不能自动覆盖讨论文本。本库只保存链接、短摘要和原创时间线，不复制日志全文。
    notes: 核对 Kubernetes 资源请求、容器内 npu-smi 的 0/3/4/7 设备、torch_npu 对逻辑范围 0-3 的错误、关键评论与 2025-12-18 completed close；页面没有同一现场合入后复验，不能声称 incident 已被发行版本修复，也不能把该 Mooncake 场景外推到所有框架。
  - id: src.vllm-ascend.pr-2541
    title: "vLLM Ascend PR #2541：Kubernetes Mooncake 初始化设备 ID 修正"
    url: https://github.com/vllm-project/vllm-ascend/pull/2541
    kind: repository
    registered_at: "2026-09-30"
    revision: "merged 2025-09-03; merge commit 07d44ade194b018ae2cc172482d55cb746c5fd0e"
    license:
      status: partial
      scopes:
        - scope: merge commit 07d44ade194b018ae2cc172482d55cb746c5fd0e 的仓库自有代码和文档；第三方文件另计
          identifier: Apache-2.0
          url: https://github.com/vllm-project/vllm-ascend/blob/07d44ade194b018ae2cc172482d55cb746c5fd0e/LICENSE
      notes: 根 LICENSE 可支持该固定 commit 的仓库自有改动；PR/Issue 评论和审阅文本是用户生成内容，许可仍未知。本库只做短摘要和精确链接。
    notes: 核对 PR 合入状态、25 checks passed、approval、PHYSICAL_DEVICES 定义、Mooncake connector 的 DP/TP 切片、部署指南和单元测试；审阅者明确称方案是 hack，且没有目标 Kubernetes/NPU 现场端到端复验，因此只作为当时实现修正，不作为通用 runtime 配置处方。
```

## 仍需保留的未知项

- 没有为任何目标硬件得到 TorchNPU/CANN 与 HDK、OS、镜像、MindCluster、vLLM Ascend 的同一官方整栈交集。
- T01 #1188 没有报告者复验；T02 #2557 虽有合入 PR 和单测，也没有同一集群的端到端复验或明确首个包含修复的 release tag。
- MindCluster 固定文档的 Docker 命令和文件列表是该版本样板；正式流程不应在未知现场直接执行，也不应把 Atlas 产品例外删掉。
- `ASCEND_VISIBLE_DEVICES`、`ASCEND_RT_VISIBLE_DEVICES`、`PHYSICAL_DEVICES` 的责任、命名空间和适用组件不同，不能按名字相似互换。
- 两个实验都没有执行。没有测量阈值、性能结论、故障注入结果或本地 incident 证据。
- HCCL 初始化失败、DCMI 初始化失败、设备节点缺失、框架 device count 为零和物理/逻辑 ID 错误是不同观测；正文必须分别保留。

## 执行记录

- 通过公开 GitHub 页面、固定 raw 文件和公开 Issue/PR HTML 只读核对正文、关键评论、时间线、合入 commit、代码位置与 LICENSE。
- 没有运行 `make`、upstream 测试、容器、Kubernetes、GPU/NPU 或安装命令；没有拉取镜像或下载二进制包。
- 没有修改 `sources/registry.yaml`、计划、导航或索引。本批只新增本研究记录和 backlog 指定的六篇草稿。

## 审阅后的独立 Docker 分流补充

T02-P 的适用范围包含独立 Docker；因此步骤 1 固定路径，主机正常后 Kubernetes 走插件/账本/Allocate，独立 Docker 直接用创建规格、`ASCEND_VISIBLE_DEVICES` 与 runtime 配置为期望进入容器/目标进程核对。完成判据按两路径拆分，无插件/kubelet 本身不是 Docker 故障。依据为上述固定安装文档第 5–7 行及 Docker client usage。T02-X 原本只设计 Kubernetes 实验，范围保持不变。
