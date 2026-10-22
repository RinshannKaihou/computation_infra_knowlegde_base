---
id: cluster-platform.accelerator-sharing-and-isolation
title: 加速器共享与租户隔离机制
type: concept
domain: cluster-platform
status: draft
platforms: [nvidia, ascend]
source_refs:
- src.nvidia.mig-user-guide-2026-10-18
- src.nvidia.mps-docs-2026-10-18
- src.nvidia.k8s-device-plugin-sharing-v0.20.1
- src.nvidia.k8s-device-plugin-mps-v0.20.1
- src.nvidia.k8s-device-plugin-v0.20.1
- src.nvidia.mig-device-names-2026-10-08
- src.nvidia.mig-deployment-considerations-2026-10-18
- src.nvidia.a100-mem-error-recovery-2026-10-18
- src.ascend.ascend-device-plugin-44385c13
- src.ascend.virtual-instance-hdk-44385c13
- src.ascend.virtual-instance-vcann-44385c13
- src.ascend.mind-cluster-v26.1.1
- src.ascend.docker-runtime-44385c13
- src.kubernetes.device-plugins-v1-32
- src.nvidia.container-toolkit-1.20.0
updated_at: "2026-10-22"
summary: 区分租户、容器、设备、显存、算力与故障域边界，比较 NVIDIA 整卡独占/MIG/MPS/time slicing 与 Ascend 静态/动态 vNPU、vCANN-RT 软切分的条件与隔离边界；跨 vNPU 故障隔离保证保留未证实。
related_ids:
- cluster-platform.device-resource-chain
- cluster-platform.container-image-runtime-baseline
- cluster-platform.admission-and-placement
- hardware.accelerator-execution-and-data-movement
- training.elastic-training-and-membership
verification:
  status: source_checked
  evidence_refs:
  - src.nvidia.mig-user-guide-2026-10-18
  - src.nvidia.mps-docs-2026-10-18
  - src.nvidia.k8s-device-plugin-sharing-v0.20.1
  - src.ascend.ascend-device-plugin-44385c13
  - src.ascend.virtual-instance-hdk-44385c13
  - src.ascend.virtual-instance-vcann-44385c13
  - src.nvidia.container-toolkit-1.20.0
  notes: "2026-10-18 经 FetchURL/审阅轮只读核对 MIG Guide（supported-gpus/concepts/deployment-considerations）、MPS（index/when-to-use-mps）、k8s-device-plugin v0.20.1 固定 commit README、A100 显存错误恢复页、mind-cluster v26.1.1 固定 commit 的 ascend-device-plugin README 与虚拟化实例（HDK/vCANN-RT）文档；未固定驱动/CANN 最低版本、未创建 MIG 或 vNPU、未启动 MPS、未配置 time slicing。 2026-10-22 IQ-06 定向重核固定 README 警告与 Container Toolkit 1.20.0 GPU Enumeration 的运行条件；未运行容器或配置设备注入。"
---

# 加速器共享与租户隔离机制

> 范围：NVIDIA MIG User Guide 与 MPS 文档（2026-10-18 观察，可变页）、k8s-device-plugin v0.20.1（commit `487d7a93`）README、MindCluster v26.1.1（commit `44385c13`）组件 README。本文只整理官方文档所述的机制与条件，不构成机型、驱动、CANN、插件组合的兼容声明，也不表示任何共享模式已在现场配置。

## 定义与要解决的问题

“共享加速器”指多个租户、进程或容器同时使用同一块 GPU/NPU；“隔离”指当其中一方超额、崩溃或行为异常时，资源与故障被限制在什么范围。二者不是同一件事：调度器可以把一块卡分配给两个 Pod，却不必提供显存、算力或故障域隔离。

本页回答三个问题：**一条共享路线究竟在哪一层做了强制隔离；它绑定了哪些机型/驱动/插件条件；出现争用或异常时，哪条证据能区分“分配了”与“隔离了”。**

先区分四组常被混用的判断：

- **已分配 ≠ 已隔离**： `nvidia.com/gpu: 1` 表示调度账本上占用一个资源单位，不表示容器独占整卡或独占故障域。
- **容器边界 ≠ 设备边界**：namespace、cgroup 与 device cgroup 能限制进程能看到哪些设备节点，但不能把 GPU 内部的 SM、显存控制器和缓存切开。
- **限额 ≠ 预留**：MPS 的动态资源限额只限制客户端最多用多少，不保证这些资源不会被其他客户端争用（[MPS 文档](https://docs.nvidia.com/deploy/mps/when-to-use-mps.html)原文：`Setting the limit does not reserve dedicated resources for any MPS client context`）。
- **健康状态 ≠ 隔离证明**：Ascend 插件规定虚拟设备健康由物理设备决定，这只说明健康归因，不说明虚拟设备之间不会互相干扰。

## 边界分层：从租户到故障域

| 边界 | 由什么强制 | 能保证什么 | 不能自动保证什么 |
|---|---|---|---|
| 租户/账号 | 平台身份、配额、队列 | 记账与准入归属 | 硬件资源隔离；同一账号内多进程仍可争用 |
| 进程/容器 | namespace、cgroup、device cgroup、运行时 hook | 可见设备节点、CPU/内存配额、部分权限约束 | GPU/NPU 内部调度、显存容量、故障域 |
| 设备 | 独占分配、硬件分区、逻辑共享 | 设备数量层面的分配 | 分区内部的算力/带宽隔离（取决于路线） |
| 显存 | MIG 分区、MPS 限额、time slicing（无） | 容量上限或容量隔离 | 带宽 QoS 与错误隔离（取决于路线） |
| 算力（SM） | MIG 分区、MPS 百分比/静态分区、time slicing（时间片） | 份额或上限 | 确定性性能与抢占公平（取决于路线） |
| 主机 CPU/内存/NUMA | cgroup、调度器 | 主机资源配额 | 加速器侧隔离；主机带宽仍共享 |
| 网络/存储 | QoS、配额、后端隔离 | 带宽/容量份额 | 加速器共享带来的同步干扰 |
| 故障域 | 硬件分区（独立 GI）；CI、整卡与主机仍共享 | 独立 GI 的所述资源与部分错误被限制在实例内 | 同 GI 内 CI、整卡 reset/驱动/主机故障；MPS/time slicing 无独立故障域 |

NVIDIA 官方对照表把三种 CUDA 并发机制放在一起（[MIG Concepts，Table 3](https://docs.nvidia.com/datacenter/tesla/mig-user-guide/concepts.html)，列名为 Streams / MPS / MIG）：分区类型分别为单进程、逻辑、物理；最大分区数 Unlimited / 48 / 7；SM 性能隔离 No / Yes（按百分比，不是分区）/ Yes；显存保护 No / Yes / Yes；显存带宽 QoS No / No / Yes；错误隔离 No / No / Yes；重配置 Dynamic / Process Launch / When Idle。MPS 文档另给出每 server 每设备最多 60 个客户端 CUDA context（默认 `CUDA_DEVICE_MAX_CONNECTIONS=2` 时），与表中的 48 不是同一口径，二者不能合并为统一容量上限；这些数字都不能直接换算成租户数或插件副本数。

## NVIDIA 的三条共享路线

### 整卡独占

device plugin 默认把每块 GPU 作为一个 `nvidia.com/gpu` 单位上报；容器请求 1 个单位时获得整卡访问。[固定 README 的 Running GPU Jobs 警告](https://github.com/NVIDIA/k8s-device-plugin/blob/487d7a93894b0f3ad08097169593972eb3ca8206/README.md#running-gpu-jobs)指出未请求 GPU 时可能暴露全部设备的风险。**这需要结合运行时与镜像条件判断**：例如启用 NVIDIA runtime、按环境变量枚举设备且镜像保留 `NVIDIA_VISIBLE_DEVICES=all` 时，无 GPU 资源请求也可能暴露全部 GPU；不能概括为插件在所有容器中都会无条件注入全部设备。

[Container Toolkit 1.20.0 GPU Enumeration](https://docs.nvidia.com/datacenter/cloud-native/container-toolkit/1.20.0/docker-specialized.html#gpu-enumeration) 区分：`all` 暴露全部 GPU（基础 CUDA 镜像默认值）；`none` 不暴露 GPU，但启用驱动能力；`void`、空或未设置时，所述路径的运行时行为等同 `runc`，不暴露 GPU 或驱动能力。调查时对照 GPU requests/limits、实际 runtime/RuntimeClass、镜像与 Pod 的有效环境变量，以及 envvar/CDI/设备挂载等注入路径；显式 CDI 或其他注入不能仅按环境变量判定。因此容器中可见设备数本身不能证明调度器分配了相同数量的 GPU。

整卡独占提供的是设备级排他，不提供卡内分区；多租户场景下它最安全，但粒度最粗。

### MIG：物理分区

MIG 把受支持的 GPU 切成多个 GPU Instance（GI）。**隔离承诺必须按层说清**：独立 GI 之间按官方所述获得显存容量/带宽与错误隔离；同一 GI 内再切出的 Compute Instance（CI）共享父 GI 的显存与引擎，不具备独立 GI 级边界。关键口径（[MIG Concepts](https://docs.nvidia.com/datacenter/tesla/mig-user-guide/concepts.html)）：

- 支持 Ampere 及更新架构（compute capability ≥ 8.0），官方支持表列 A100/A30、H100/H200/H20、B200/GB200/GB300、RTX PRO Blackwell、Thor iGPU 等，单产品最大实例数 2、4 或 7（[Supported GPUs](https://docs.nvidia.com/datacenter/tesla/mig-user-guide/supported-gpus.html)）。不在表内的产品不能按“同代 GPU”推定支持。
- 分区单位是 memory slice（约 1/8 显存资源，含容量与带宽）与 SM slice（约 1/7 SM）；GI 由若干 slice 加引擎组成，提供 memory QoS；GI 的 SM slice 还可细分为 CI，**CI 共享父 GI 的显存与引擎**，因此不能把 GI 的显存/QoS 承诺套到同 GI 的多个 CI 上。
- Profile 不能任意组合：受物理 slice 位置限制，GI 创建/销毁会产生碎片，后续实例的可放置位置取决于当前布局。
- 独立 GI 在官方对照表中提供显存保护、带宽 QoS 与错误隔离；**这不等于“任何错误都不外溢”**。官方显存错误恢复流程仍包含终止全部 GPU 进程后整卡 reset、OS reboot，以及部分 MIG 分区受损后的 drain-and-reset（[Error Recovery and Response Flags](https://docs.nvidia.com/deploy/a100-gpu-mem-error-mgmt/error-recovery-and-response-flags.html)）。整卡、驱动、主机与共享网络/存储仍是共同故障域，验证时必须声明使用哪类错误。

工程条件（有限样板，不是全机型支持矩阵）：需要机型在支持表内、驱动支持 MIG 模式，并由插件选择暴露策略（`mig-strategy` 的 `none`/`single`/`mixed`）；`mixed` 策略会额外暴露 `nvidia.com/mig-<slice_count>g.<memory_size>gb` 形式的资源（[README](https://github.com/NVIDIA/k8s-device-plugin/blob/487d7a93894b0f3ad08097169593972eb3ca8206/README.md)）。设备命名随驱动分支变化：R470 前后命名方式不同，R570 前后枚举条件也不同；本轮材料不足以建立逐型号最低驱动交集，正文不把 `MIG-<UUID>` 当作所有版本的统一命名（[MIG Device Names](https://docs.nvidia.com/datacenter/tesla/mig-user-guide/mig-device-names.html)、[Deployment Considerations](https://docs.nvidia.com/datacenter/tesla/mig-user-guide/deployment-considerations.html)）。同一物理 GPU 下可挂多个 MIG 设备，**物理卡号与逻辑设备号不一一对应**。

边界：MIG 解决卡内分区，不解决跨节点、网络、存储与主机资源争用；profile 组合和碎片会让“剩余卡数”无法直接回答“还能不能再放一个任务”。

### MPS：逻辑共享与有限错误遏制

MPS 由控制 daemon、server 和客户端 runtime 组成，把多个进程的 CUDA 工作复用到同一 GPU（[MPS Overview](https://docs.nvidia.com/deploy/mps/index.html)）。它提供地址空间隔离，可选地把 SM 限制为总 SM 的百分比，也可以设置每客户端显存上限；但官方明确说明：

- **MPS 当前不提供客户端之间的错误隔离**；SM 可以按百分比限制，但调度硬件仍共享；显存带宽、缓存与容量在客户端之间共享（MIG Concepts 的 CUDA Concurrency Mechanisms 节）。
- 错误遏制是有限的：一个客户端的致命 GPU 故障会被限制在共享该 GPU 子集的客户端范围内，并报告给该范围内的所有客户端，**但不指出肇事者**；server 进入 `FAULT` 状态，等待受影响客户端退出后才重建上下文（[When to Use MPS，Memory Protection and Error Containment](https://docs.nvidia.com/deploy/mps/when-to-use-mps.html)）。
- 系统级限制：仅 Linux/QNX；**同一系统只有一个用户能持有活动 MPS server**；控制 daemon 会串行化不同用户的激活请求，导致用户之间仍然是串行独占；监控与记账把客户端行为归到 server 进程。
- 客户端条件：默认要求同 UID（`-multiuser-server` 会放弃用户间隔离）、仅 64 位、驱动 API ≥ CUDA 4.0、不支持 dynamic parallelism；在默认 `CUDA_DEVICE_MAX_CONNECTIONS=2` 时，每 server 每设备最多 60 个客户端 CUDA context，提高该值会减少可接入客户端数量；未同步就终止客户端可能使 server 和其他客户端进入未定义状态。
- 可选静态 SM 分区（Ampere+，以 chunk 为单位）提供确定性分配与空间隔离，但要求客户端在创建 context 前设置分区环境变量，且不能与 locality domains 同时使用。静态分区本身未被文档列为与 vGPU 互斥——vGPU 不支持属于 locality domains 特性的限制；也不能反向推断静态分区一定支持 vGPU。

在 Kubernetes 插件层，MPS 共享被标注为 **experimental（截至 v0.15.0）**，每客户端显存被限制为总显存的等分、算力也受限；**MIG 启用时设备不支持 MPS 共享**，且只支持整卡 `nvidia.com/gpu`（[README，With CUDA MPS](https://github.com/NVIDIA/k8s-device-plugin/blob/487d7a93894b0f3ad08097169593972eb3ca8206/README.md)）。

### time slicing：插件层的超卖

time slicing 让多个工作负载按时间片交错使用同一 GPU。插件通过 `replicas` 把一块物理卡“复制”成多个可调度名额：8 卡节点配置 `replicas: 10` 会向上报告 80 个 `nvidia.com/gpu`。官方对隔离的表述非常直接：

> `nothing special is done to isolate workloads that are granted replicas from the same underlying GPU, and each workload has access to the GPU memory and runs in the same fault-domain as of all the others (meaning if one workload crashes, they all do).`

此外，请求多于一个共享 GPU **不保证获得按比例的算力**；CUDA 只是把时间片平均分给所有进程。`failRequestsGreaterThanOne` 可以把“申请 1 个”解释为访问名额而非独占资源，但默认是 `false`。time slicing 与 MPS **互斥**，并且共享方式按节点统一配置，不能逐卡设置（同上 README）。

因此 time slicing 适合“提高利用率、允许互相干扰”的批处理或开发场景，不适合需要显存上限、故障隔离或稳定性能的多租户生产切片。

### 有限样板与未闭合条件

下表把“本轮已核对的条件”与“尚未建立的交集”分开；MIG/MPS 的驱动与 OS 条件取自 [MIG Deployment Considerations](https://docs.nvidia.com/datacenter/tesla/mig-user-guide/deployment-considerations.html) 与 MPS 文档。它不是支持矩阵，也不表示这些条件可以随意组合。

| 路线 | 已核对的条件（有限样板） | 尚未建立/保留未知 |
|---|---|---|
| 整卡独占 | device plugin 默认按 `nvidia.com/gpu` 上报；启用 NVIDIA runtime 且按 `NVIDIA_VISIBLE_DEVICES=all` 枚举时，无资源请求也可能暴露全部 GPU（条件见上文）；Kubernetes 扩展资源按整数分配，插件不应把同一资源 ID 重复分给两个容器 | runtime/镜像变量与实际注入路径、跨容器的物理分配互斥现场证据、特权/host 访问旁路、运行时之外的设备共享 |
| MIG | 文档样板：A100/A30 需 CUDA 11 + R525（≥525.53），B200 需 CUDA 12 + R570（≥570.133.20）；仅 CUDA 支持的 Linux；插件 v0.20.1 `mig-strategy=none/single/mixed`；命名/枚举随 R470/R570 变化。注意 NCCL 当前不支持 MIG；R570 仅同 GPU 内 MIG P2P，跨 GI CUDA IPC 不支持。**Deployment 页另列 H100/H200 为 CUDA 12 + R450；该行与其它官方版本材料冲突，本表不采用，保留为未消歧** | 完整 profile 组合与现场组合；MPS-on-MIG 的插件/驱动分层（驱动支持、插件不支持）；H100/H200 驱动下限 |
| MPS | 示例样板：A100-SXM4-40GB；Linux；CUDA 11 + R525（≥525.53，取自 MIG Deployment 的 A100 条件）；k8s-device-plugin v0.20.1（README 前提驱动 ~=384.81 由 R525 满足；toolkit ≥1.7.0；K8s ≥1.10）；**本样板只采用动态限额（active-thread/显存上限）与 Legacy MPS v2 控制路径；静态 SM 分区与 MPS v3 不属于该样板（概念另列）**；功能范围＝整卡共享；插件 MPS experimental；MIG 启用时插件不支持 MPS（驱动层另可支持） | MPS 功能自身的最低驱动/CUDA 版本（本样板是组件交集，不是 MPS 功能认证）；插件 experimental 的长期支持；跨客户端错误隔离 |
| time slicing | 示例样板：A100-SXM4-40GB；Linux；CUDA 11 + R525（≥525.53）；插件 v0.20.1 的 `sharing.timeSlicing` 配置 + NVIDIA 容器运行时；不使用 MPS daemon；节点级 replicas；与 MPS 互斥；无隔离声明 | 实测争用/尾延迟数据；不同插件版本的实现差异 |
| Ascend 静态 vNPU | 有限配套样板：MindCluster 26.1.0（tag v26.1.1）↔ CANN 9.1.0 ↔ HDK 按产品（25.7.RC1/25.1.RC1/25.6.RC1 等，见 release notes 表）；在该配套下 Atlas 800T A2（24 AICore）可用 `vir06_1c_16g`/`vir12_3c_32g`。静态创建/挂载、每 Pod 1 个、创建/销毁需重启 Device Plugin、不支持故障重调度 | 虚拟化功能的最低固件/CANN 版本（release notes 未单列）；跨 vNPU 的故障隔离与性能 QoS |
| Ascend 动态 vNPU | Docker：`ASCEND_VISIBLE_DEVICES`+`ASCEND_VNPU_SPECS`；**动态使用前须关闭 vNPU 恢复功能**；`ASCEND_RUNTIME_OPTIONS` 动态不能含 `VIRTUAL`（静态必须含）。K8s 仅 Volcano、同一时刻只能相同模板、每 Pod 1 个、不支持分布式任务、支持故障重调度。**所引集群推理场景同一集群不能同时存在静态与动态 vNPU 任务；节点切换需删除已有任务；K8s 自动创建/销毁不能与 Docker 操作混用** | 同上；重启后 vNPU 自动销毁失败的现场处置 |
| Ascend vCANN-RT 软切分 | 仅推理；一个容器一个 NPU；requests 为 AICore 百分比；同一物理 NPU 上所有容器须相同软切分策略；A3 需单 die 直通 | 跨容器故障隔离/性能保证、软切分实际开销与最大切分数现场值 |

**MPS 样板的两条限额路径与运行时接入要分开：**

- **动态限额路径**：默认每个客户端可用全部线程；用 `CUDA_MPS_ACTIVE_THREAD_PERCENTAGE`（uniform 限额在客户端启动时固定，之后不能改）或 `CUDA_MPS_PINNED_DEVICE_MEM_LIMIT` 限制。限额不是预留，内核仍可能与其他客户端共享 SM（[When to Use MPS](https://docs.nvidia.com/deploy/mps/when-to-use-mps.html)）。
- **静态 SM 分区路径**：Ampere+，以 chunk 为单位（Hopper+ 为 8 SM/chunk）；创建分区后，客户端必须在创建 context 前设置 `CUDA_MPS_SM_PARTITION`；不能与 locality domains 并用，启用静态分区时动态 provisioning 被忽略。
- **运行时接入路径（插件 v0.20.1 样板）**：使用 `sharing.mps` 时，Device Plugin 检查 MIG 设备（存在则不支持 MPS）、确认 MPS daemon 健康，并在分配响应中注入 `CUDA_MPS_PIPE_DIRECTORY`、把 pipe 目录与 shm 目录挂载到容器（[mps.go](https://github.com/NVIDIA/k8s-device-plugin/blob/487d7a93894b0f3ad08097169593972eb3ca8206/internal/plugin/mps.go)）；daemon/server 生命周期由同 chart 的 `mps-control-daemon` DaemonSet 负责（部署在 `nvidia.com/mps.capable=true` 节点，使用 `mps-root` hostPath 与 `/dev/shm`，[Helm 模板](https://github.com/NVIDIA/k8s-device-plugin/blob/487d7a93894b0f3ad08097169593972eb3ca8206/deployments/helm/nvidia-device-plugin/templates/daemonset-mps-control-daemon.yml)）。站点自管 daemon 是另一条路径，必须提供同等的 pipe/shm 可达性；不能把站点手工启动当作 v0.20.1 默认集成。
- **两条样板的容器 runtime 选路**：要么把 `nvidia-container-runtime` 配置为节点默认低层运行时（此后无需 RuntimeClass），要么保留默认运行时并定义 `RuntimeClass`（name/handler 均为 `nvidia`），Pod 使用 `runtimeClassName: nvidia`。同一节点池统一选择一种，不混用（[README](https://github.com/NVIDIA/k8s-device-plugin/blob/487d7a93894b0f3ad08097169593972eb3ca8206/README.md)）。

### 路线对照

| 维度 | 整卡独占 | MIG | MPS | time slicing |
|---|---|---|---|---|
| 隔离层级 | 设备级排他 | 独立 GI 物理分区；CI 共享父 GI | 逻辑共享 | 时间片共享 |
| 显存隔离 | 整卡 | 独立 GI 的容量与带宽；CI 共享 | 可设上限，容量共享 | 无 |
| SM 隔离 | 整卡 | 独立 GI 分区（7/7 等 profile）；CI 有专属 SM slice，但共享父 GI 的显存与引擎 | 百分比或静态分区（可选） | 时间片，无空间隔离 |
| 错误隔离 | 整卡范围 | 独立 GI：官方表 Yes（限所述错误范围）；整卡/驱动/主机故障仍共享 | 官方表：No（有限遏制） | 无（同一故障域） |
| 典型风险 | 利用率低 | profile/碎片限制、机型与驱动依赖 | 单用户 server、同 UID、提前终止 | 超卖、互相拖慢、崩溃连带 |
| 插件条件 | 默认 | `mig-strategy` | experimental、MIG 开启时不可用 | 与 MPS 互斥、按节点配置 |

## Ascend 的共享与虚拟设备分支

MindCluster 的 Ascend Device Plugin 文档写明：设备发现支持“发现拆分物理设备得到的虚拟设备并上报 Kubernetes 系统”；健康检查规定“虚拟设备健康状态由拆分这些虚拟设备的物理设备决定”；分配支持 NPU 重调度（[组件 README](https://github.com/Ascend/mind-cluster/blob/44385c13d7b1d87def35f1604e8be4d16de6ca4e/component/ascend-device-plugin/README.md)）。**这只是上报与健康归因，不构成隔离证明。**

### HDK 虚拟化实例：静态与动态 vNPU

MindCluster v26.1.1 的虚拟化文档把 NPU 按 AICore、AICPU、内存、DVPP 等资源切分为 vNPU，再挂载到容器（[特性说明](https://github.com/Ascend/mind-cluster/blob/44385c13d7b1d87def35f1604e8be4d16de6ca4e/docs/zh/scheduling/04_usage/02_virtual_instance/00_virtual_instance_with_hdk/01_description.md)）。产品支持表覆盖 Atlas 推理/训练系列、A2/A3 训练与推理系列；Atlas 200/300/500 与 200I/500 A2 明确不支持。模板按产品区分（例如 Atlas 训练系列 vir02/04/08/16，A2 训练 vir06_1c_16g/vir12_3c_32g，A3 训练同为这两档，A2 推理多档含 DVPP 变体），并可用 `npu-smi info -t template-info` 查询（[虚拟化模板](https://github.com/Ascend/mind-cluster/blob/44385c13d7b1d87def35f1604e8be4d16de6ca4e/docs/zh/scheduling/04_usage/02_virtual_instance/00_virtual_instance_with_hdk/03_virtualization_templates.md)）。模板作用于整台服务器，不支持不同规格标卡混插；训练系列仅 AMP 模式支持虚拟化，SMP 不支持。

**有限配套样板**：MindCluster 26.1.0（tag v26.1.1）↔ CANN 9.1.0 ↔ HDK 按产品（25.7.RC1/25.1.RC1/25.6.RC1 等，见 [release notes](https://github.com/Ascend/mind-cluster/blob/44385c13d7b1d87def35f1604e8be4d16de6ca4e/docs/zh/release_notes.md) 表）。在该配套下，Atlas 800T A2（24 AICore）可使用 `vir06_1c_16g` 或 `vir12_3c_32g` 静态 vNPU。release notes 未单列虚拟化功能的最低固件/CANN 版本，因此这只是文档配套样板，不是功能最低版本证明。

**静态 vNPU**：先用 `npu-smi set -t vnpu-mode -d 0`（容器模式）与 `npu-smi set -t create-vnpu` 创建，可配置 `vnpu-cfg-recover` 在重启后恢复配置（[创建 vNPU](https://github.com/Ascend/mind-cluster/blob/44385c13d7b1d87def35f1604e8be4d16de6ca4e/docs/zh/scheduling/04_usage/02_virtual_instance/00_virtual_instance_with_hdk/04_static_vnpu_scheduling/01_creating_vnpu.md)）；挂载到容器时 `ASCEND_RUNTIME_OPTIONS` 必须包含 `VIRTUAL`（[挂载 vNPU](https://github.com/Ascend/mind-cluster/blob/44385c13d7b1d87def35f1604e8be4d16de6ca4e/docs/zh/scheduling/04_usage/02_virtual_instance/00_virtual_instance_with_hdk/04_static_vnpu_scheduling/02_mounting_vnpu_static.md)）。Kubernetes 侧资源名为 `huawei.com/Ascend910-<Y>` 或 `huawei.com/Ascend310P-<Y>`（`Y` 由模板决定），每个 Pod 最多请求 1 个 vNPU；创建/销毁 vNPU 后需重启 Device Plugin；静态 vNPU **不支持故障重调度**，也不支持交换机亲和性调度。

**动态 vNPU**：不需要预先创建，且**使用前须关闭 vNPU 的恢复功能**（与静态可开启 `vnpu-cfg-recover` 相反）。Docker 场景用 `ASCEND_VISIBLE_DEVICES=<物理芯片 ID>` 加 `ASCEND_VNPU_SPECS=<模板>`；`ASCEND_RUNTIME_OPTIONS` 可选 `NODRV`，但**不能包含 `VIRTUAL`**（静态则必须包含）。容器结束时会自动销毁；服务器重启后可能无法自动销毁，需要手工清理（[动态 vNPU 调度](https://github.com/Ascend/mind-cluster/blob/44385c13d7b1d87def35f1604e8be4d16de6ca4e/docs/zh/scheduling/04_usage/02_virtual_instance/00_virtual_instance_with_hdk/05_dynamic_vnpu_scheduling/01_dynamic_vnpu_scheduling_inference.md)）。Kubernetes 场景**只支持 Volcano 调度器**，需将 Device Plugin 的 `-volcanoType=true`、`-presetVirtualDevice=false` 与 Volcano 的 `presetVirtualDevice=false` 配套；同一时刻只能下发相同模板的任务，每个 Pod 最终只挂 1 个 vNPU，仅支持单机单副本或多副本任务，不支持分布式任务；支持芯片/节点故障重调度。

**模式作用域**：在所引集群推理场景，**同一集群不能同时存在使用静态 vNPU 的任务和使用动态 vNPU 的任务**（不是仅指单个任务内部）；节点在静态/动态之间切换时需要先删除已有任务；K8s 自动创建/销毁 vNPU 不能与 Docker 场景的手工操作混用。这些限制不外推到“不同集群永远不能各用一种模式”。

### vCANN-RT 软切分

vCANN-RT 通过软切分配置文件按需分配 AICore 百分比与内存，属于时分复用（[特性说明](https://github.com/Ascend/mind-cluster/blob/44385c13d7b1d87def35f1604e8be4d16de6ca4e/docs/zh/scheduling/04_usage/02_virtual_instance/01_virtual_instance_with_vcann_rt/00_description.md)）。约束：**仅支持推理任务**；一个容器只能挂载一个 NPU；YAML 的 requests 表示 AICore 百分比而非卡数；A3 训练/推理必须开启单 die 直通（Device Plugin 加 `-useSingleDieMode=true`）；同一物理 NPU 上所有容器必须使用相同软切分策略；最大切分数量建议不超过单 device 最大用户进程数；软切分后物理 NPU 不可直通虚拟机。

### 隔离边界与独占基线

可确认的是：HDK 切分给出了显式的资源组成（AICore/AICPU/内存/DVPP），并规定**一个 vNPU 只能被一个任务容器使用**；虚拟化后物理 NPU 不能再挂容器或直通虚拟机。这些是分配与资源组成层面的边界。

**仍未被这些文档建立的是跨 vNPU 的故障隔离与性能 QoS 保证。** 文档用“借助容器进行资源隔离”描述收益，但没有给出“一个 vNPU 的错误不影响其他 vNPU”或“带宽/算力按份额被强制”的承诺。因此：

- 平台分配层面的整卡/NPU 设备独占可以作为**分配单位**描述，但 `ASCEND_VISIBLE_DEVICES` 与 device cgroup 只证明“容器被允许访问哪些设备”，不能单独证明“另一容器没有被分配同一物理设备”；后者需要调度器/插件分配记录与现场核对。
- vNPU 分支的规格、模板、数量与分配约束已有官方材料；**故障隔离与 QoS 仍保留 unknown**，不得从 MIG 机制类推。
- vCANN-RT 软切分是时分复用，隔离能力弱于硬件切分；其跨容器干扰只能由两租户对照实测回答。

容器内 `vdavinciN` 会被重命名为 `davinciN`（[process.go 的 `getMountPath`，L536–L549](https://github.com/Ascend/mind-cluster/blob/44385c13d7b1d87def35f1604e8be4d16de6ca4e/component/ascend-docker-runtime/runtime/process/process.go#L536)）；这是命名转换，不是隔离证据。

## 选择流程

1. **先问故障隔离是否必需。** 需要“一个租户崩溃不影响另一个”时，优先考虑整卡独占或独立 GI 的 MIG（受支持机型/驱动）；MPS 与 time slicing 不满足。同 GI 内的多个 CI 有专属 SM slice，但共享父 GI 的显存与引擎，不承诺独立 GI 级隔离；Ascend vNPU 的跨实例故障隔离保证仍未知，不能作为已确认能力承诺。
2. **再问是否需要显存/算力上限。** 需要硬上限时选 MIG 或 MPS；time slicing 只能提供访问名额；Ascend 静态/动态 vNPU 有模板化资源组成，vCANN-RT 按 AICore 百分比软切分。
3. **再问是否接受节点级统一配置。** time slicing/MPS 共享方式按节点统一设置，不能逐卡；在所引集群推理场景，Ascend 同一集群不能同时存在静态与动态 vNPU 任务，切换需先删除已有任务，K8s 自动生命周期不能与 Docker 手工操作混用。
4. **核对有限样板，而不是“同代即可”。** MIG 机型/驱动/命名分支；MPS 的 v2/v3 接口与连接设置；插件版本与共享模式；Ascend 的产品支持表、模板、Volcano/Device Plugin 参数与单 die 模式。
5. **NPU 先确认共享模式与分配约束。** 静态 vNPU 每 Pod 最多 1 个、创建/销毁需重启 Device Plugin、不支持故障重调度；动态 vNPU 仅 Volcano、同一时刻同一模板、不支持分布式任务；vCANN-RT 仅推理。跨 vNPU 的故障隔离与 QoS 仍需现场验证，未证实前不得承诺。
6. **把账本口径写清楚。** 调度器看到的是副本数/资源名/模板，不是物理卡数；容量与计费必须区分“物理设备”“逻辑实例（vNPU/CI/MIG）”“可调度名额”。

## 观测与异常

| 现象 | 首先看什么 | 不能据此下什么结论 |
|---|---|---|
| 容器看到的 GPU 数多于申请数 | 是否声明了 GPU 请求；插件 device list 策略 | 不能认定调度器多分配了设备 |
| `.shared` 资源上的任务互相拖慢 | replicas 配置、同卡进程、时间片行为 | 不能把“变慢”直接归因于硬件故障 |
| MPS 客户端初始化失败 | server 是否 ACTIVE/FAULT、UID 与 `CUDA_MPS_PIPE_DIRECTORY`、连接数上限 | 不能只看容器日志判定“GPU 坏了” |
| MIG 实例创建失败 | 机型/驱动支持、现有 GI 布局与碎片、profile 是否合法 | 不能把“剩余显存够”当作“能够创建该 profile” |
| 虚拟 NPU 设备不健康 | 物理设备健康（插件口径） | 不能据此证明其他虚拟设备未受影响 |
| 账本显示有空闲但任务放不下 | 资源名、副本数、节点级共享配置、MIG 资源名 | 不能把“总卡数 − 已用卡数”当作可用容量 |

## 最小验证

以下为验证设计，本库尚未执行：

1. **租户可见性**：在两个租户容器内分别记录可见设备数量、UUID/设备名与资源请求，核对“申请—分配—可见”三者是否一致。
2. **分配边界**：确认调度器账本中的资源单位（整卡、MIG profile、replica、vNPU/模板、vCANN 百分比）与实际容器访问的是同一实体；同时记录两个租户是否被分配到同一物理设备的稳定身份，不能只看资源名。
3. **争用对照**：单租户基线 → 同租户重复 → 两租户并发；观察吞吐、尾延迟与错误是否越过分区边界。方法见[多租户争用、公平性与容量验证](contention-capacity-validation.md)。
4. **回收**：释放一个租户后确认设备/副本/vNPU 回到可分配状态、旧进程已退出，新任务能获得正确资源；动态 vNPU 还需核对异常重启后的残留。
5. **故障遏制**：先定义错误类别（进程 OOM、可控退出、致命 GPU 故障、整卡 reset、驱动/主机故障），再在受控环境逐类记录另一租户是否受影响。MPS/time slicing 下共享故障域；独立 GI 的 MIG 只对所述错误范围预期隔离，整卡/驱动/主机错误仍可能外溢；NPU 侧保持未知直到有证据。

## 常见误解

- **“容器有 namespace 和 cgroup，所以租户已经隔离。”** 这两者约束的是进程可见性与主机资源配额，不切开 GPU 内部资源与故障域。
- **“`replicas: 10` 就是 10 倍算力或 10 份独立显存。”** 它只是 10 个访问名额；显存与故障域仍共享。
- **“MPS 设了显存上限就有故障隔离。”** 官方明确 MPS 不提供客户端间错误隔离。
- **“MIG 可以任意切，且切出来的每个实例都完全互不影响。”** 只能使用受支持的 profile，且受物理位置与碎片约束；独立 GI 的隔离是官方所述范围内的，同 GI 内 CI 共享父 GI，整卡/驱动/主机故障仍可能外溢。
- **“插件上报虚拟 NPU 设备，就说明 vNPU 有隔离保证。”** 上报、模板与“一个 vNPU 一个容器”的分配约束已有官方材料，但跨 vNPU 的故障隔离与 QoS 保证仍未证实。
- **“`ASCEND_VISIBLE_DEVICES` 限制了可见设备，所以已经证明整卡独占。”** 它证明访问控制，不证明另一容器没有被分配同一物理设备；分配互斥需调度器/插件记录与现场核对。
- **“总卡数就是可租户数。”** 可共享的租户数取决于路线、副本配置、显存/算力上限与故障域要求。

## 例子与相关知识

- 设备从物理存在到容器可用的状态链见[从物理设备到容器资源的状态链](device-resource-chain.md)。
- 镜像、运行时与设备暴露的基线见[镜像制品、容器运行时与设备暴露基线](container-image-runtime-baseline.md)。
- 配额、队列与放置策略见[作业准入、调度与拓扑放置](admission-and-placement.md)。
- 硬件执行单元与数据移动机制见[加速器执行单元、内存层次与数据移动](../01-hardware/accelerator-execution-and-data-movement.md)。
- 训练侧对中断与恢复的假设见[弹性训练与成员变更](../06-training/elastic-training-and-membership.md)。

## 来源与待确认问题

- [NVIDIA MIG User Guide — Supported GPUs](https://docs.nvidia.com/datacenter/tesla/mig-user-guide/supported-gpus.html)（2026-10-18 观察）
- [NVIDIA MIG User Guide — Concepts](https://docs.nvidia.com/datacenter/tesla/mig-user-guide/concepts.html)（2026-10-18 观察）
- [NVIDIA MIG User Guide — Deployment Considerations](https://docs.nvidia.com/datacenter/tesla/mig-user-guide/deployment-considerations.html)（2026-10-18 观察）
- [NVIDIA GPU Memory Error Management — Error Recovery and Response Flags](https://docs.nvidia.com/deploy/a100-gpu-mem-error-mgmt/error-recovery-and-response-flags.html)（2026-10-18 观察）
- [NVIDIA Multi-Process Service — Overview](https://docs.nvidia.com/deploy/mps/index.html)（2026-10-18 观察）
- [NVIDIA Multi-Process Service — When to Use MPS](https://docs.nvidia.com/deploy/mps/when-to-use-mps.html)（2026-10-18 观察）
- [NVIDIA k8s-device-plugin v0.20.1 README（commit 487d7a93）](https://github.com/NVIDIA/k8s-device-plugin/blob/487d7a93894b0f3ad08097169593972eb3ca8206/README.md)
- [Ascend Device Plugin README（mind-cluster v26.1.1，commit 44385c13）](https://github.com/Ascend/mind-cluster/blob/44385c13d7b1d87def35f1604e8be4d16de6ca4e/component/ascend-device-plugin/README.md)
- [Ascend 虚拟化实例特性说明（HDK）](https://github.com/Ascend/mind-cluster/blob/44385c13d7b1d87def35f1604e8be4d16de6ca4e/docs/zh/scheduling/04_usage/02_virtual_instance/00_virtual_instance_with_hdk/01_description.md)
- [Ascend 虚拟化实例模板](https://github.com/Ascend/mind-cluster/blob/44385c13d7b1d87def35f1604e8be4d16de6ca4e/docs/zh/scheduling/04_usage/02_virtual_instance/00_virtual_instance_with_hdk/03_virtualization_templates.md)
- [Ascend 动态 vNPU 调度](https://github.com/Ascend/mind-cluster/blob/44385c13d7b1d87def35f1604e8be4d16de6ca4e/docs/zh/scheduling/04_usage/02_virtual_instance/00_virtual_instance_with_hdk/05_dynamic_vnpu_scheduling/01_dynamic_vnpu_scheduling_inference.md)
- [Ascend vCANN-RT 软切分特性说明](https://github.com/Ascend/mind-cluster/blob/44385c13d7b1d87def35f1604e8be4d16de6ca4e/docs/zh/scheduling/04_usage/02_virtual_instance/01_virtual_instance_with_vcann_rt/00_description.md)
- 待确认：MIG 的逐型号最低驱动交集与完整 profile 组合；MPS 与 MIG 在驱动侧的完整互斥条件；Ascend 跨 vNPU 的故障隔离与性能 QoS 保证、固件/CANN 最低版本矩阵；vCANN-RT 的实际开销与最大切分数现场值；各机制在现场的实际性能与争用数据。
