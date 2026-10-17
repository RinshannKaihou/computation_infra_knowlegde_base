---
id: cluster-platform.device-resource-chain
title: 从物理设备到容器资源的状态链
type: concept
domain: cluster-platform
status: draft
platforms: [generic]
source_refs:
  - src.kubernetes.device-plugins-v1-32
  - src.ascend.mind-cluster-v26.1.1
  - src.nvidia.k8s-device-plugin-v0.20.1
  - src.slurm.docs-24.11.7
  - src.slurm.gres-tres-cgroup-24.11.7
updated_at: "2026-10-17"
summary: 区分设备物理存在、驱动可见、平台资源账本、具体分配、容器访问和框架可用，说明各层证据的证明边界；并按 NVIDIA k8s-device-plugin v0.20.1 与 Slurm 24.11.7 两个固定实现给出独立的发现、分配、健康与回收视图。
related_ids:
  - hardware.resource-topology
  - software-stack.layers-and-boundaries
  - software-stack.compatibility-evidence
  - cluster-platform.container-image-runtime-baseline
  - cluster-platform.kubernetes-job-lifecycle
  - cluster-platform.slurm-jobs-and-device-resources
verification:
  status: source_checked
  evidence_refs:
    - src.kubernetes.device-plugins-v1-32
    - src.ascend.mind-cluster-v26.1.1
    - src.nvidia.k8s-device-plugin-v0.20.1
    - src.slurm.docs-24.11.7
    - src.slurm.gres-tres-cgroup-24.11.7
  notes: 已核对 Kubernetes v1.32 Device Plugins 版本化页面（含 kubelet 重启、不健康设备、ResourceHealthStatus、PodResources 与部署节），MindCluster v26.1.1 解引用 commit 的组件文档与实现，NVIDIA k8s-device-plugin v0.20.1 的 server.go 全 557 行与 internal/rm/health.go 全 363 行（本机 curl 字节级取回，行数与 blob 页一致）；Slurm 24.11.7 归档 GRES/TRES/cgroup 材料经 T05-03 取证复用，本轮未重开；未在真实集群、容器、GPU 或 NPU 上执行验证。
---

# 从物理设备到容器资源的状态链

“节点有卡”不是一个足以判断任务能否使用加速器的状态。物理设备、驱动枚举、设备插件上报、节点资源账本、调度结果、具体设备分配、容器内访问条件和框架初始化分别由不同组件负责，也需要不同证据。

本文把这些观察位置组织成一条证据链：

> 物理设备存在 → 驱动可见 → 插件注册并上报 → 节点 `capacity` / `allocatable` → 调度 → 设备分配 → 容器设备节点、权限与用户态依赖 → 框架可用

箭头表示下一层通常依赖上一层，不表示已观察到左侧就能推出右侧，也不表示系统只能单向变化。这是一张跨层核对图，不是严格状态机。这条链是 Kubernetes 形态的；Slurm 的 GRES/TRES 账本是另一种实现形态，在下文“Slurm 例子”节独立说明，两套术语不互套。

## 每一层负责什么

| 层次 | 主要责任方 | 能支持判断的证据 | 不能据此推出 |
|---|---|---|---|
| 物理设备存在 | 板卡、服务器、固件与硬件管理面 | 固定节点与时点的硬件清单、插槽/总线身份、固件或带外管理记录；拓扑归属见[资源拓扑](../01-hardware/resource-topology.md) | OS 已初始化设备、驱动能枚举、设备健康、容器或框架可用 |
| 驱动可见 | 主机 OS、内核驱动、固件接口和厂商设备管理库 | 同一时点的驱动枚举结果、设备身份和驱动返回的健康/错误状态 | 设备插件已运行或注册；Kubernetes 已拥有该资源；用户态运行库与框架版本匹配 |
| 插件注册与持续上报 | 厂商设备插件和 kubelet | 注册的 API 版本、socket、资源名，以及 `ListAndWatch` 返回的设备 ID 与健康状态。Kubernetes v1.32 要求插件先提供 gRPC 服务，再通过 kubelet socket 注册；成功注册后由插件持续报告设备列表和状态（[注册与实现流程](https://v1-32.docs.kubernetes.io/docs/concepts/extend-kubernetes/compute-storage-net/device-plugins/#device-plugin-registration)） | API server 已看到最新节点状态；调度器已经选择节点；某个 Pod 已拿到具体设备 |
| 节点资源账本 | kubelet、API server 和调度器缓存 | 对应扩展资源名下的 `capacity`、`allocatable`、更新时间，以及 Pod 的资源请求。插件上报健康设备后，kubelet 负责把资源写入节点状态（[Device Plugins](https://v1-32.docs.kubernetes.io/docs/concepts/extend-kubernetes/compute-storage-net/device-plugins/#device-plugin-registration)） | `allocatable` 等于当前空闲设备数；资源字段反映设备的全部实时故障；具体设备 ID 已分给某个容器 |
| 调度 | 调度器及其插件、队列或控制器 | Pod 请求的扩展资源、调度事件、绑定节点和当时使用的资源快照。标准设备插件模型中的扩展资源是整数且不能超卖（[资源请求约束](https://v1-32.docs.kubernetes.io/docs/concepts/extend-kubernetes/compute-storage-net/device-plugins/#example)） | 标准调度器已经决定具体设备 ID；kubelet 的分配调用成功；容器已经创建或业务已经启动 |
| 具体设备分配 | kubelet Device Manager 与厂商设备插件 | kubelet 保存的 Pod/容器到资源名和设备 ID 的分配关系，以及插件 `Allocate` 的请求、返回或明确错误。`Allocate` 在容器创建期间调用，返回设备节点、环境变量、挂载或 CDI 设备名等运行时配置（[接口语义](https://v1-32.docs.kubernetes.io/docs/concepts/extend-kubernetes/compute-storage-net/device-plugins/#device-plugin-implementation)） | 返回的配置已经被容器运行时完整应用；容器权限、文件和库均正确；设备能执行计算 |
| 容器访问条件 | kubelet、容器运行时、厂商 runtime/hook、镜像与安全策略 | 容器最终配置和容器内实际可见的设备节点、权限、挂载、环境变量，以及所需用户态库和动态链接依赖 | 框架后端已加载；运行库 ABI 与驱动匹配；算子、通信或数值结果正确 |
| 框架可用 | 平台运行时、框架设备后端和业务进程 | 目标镜像与进程中的框架设备枚举、初始化结果，以及与目标负载相符的最小功能证据；软件分层见[主机到模型执行的软件栈分层](../02-software-stack/layers-and-boundaries.md)，版本证据规则见[如何判断版本配套是否有依据](../02-software-stack/compatibility-evidence.md) | 其他镜像、节点、框架版本、分布式规模或完整模型同样可用；平台资源账本会随框架错误自动变化 |

## 资源账本不等于实时健康

`capacity`、`allocatable`、已请求量、已分配设备和实时健康是不同对象。

- 对设备插件资源，Kubernetes v1.32 明确说明：设备被标为不健康后，kubelet 会降低该资源的 `allocatable`，用于影响**新 Pod** 的调度；`capacity` 不变。已经分到故障设备的 Pod 仍保持该分配，应用可能失败或进入重启循环（[不健康设备的处理](https://v1-32.docs.kubernetes.io/docs/concepts/extend-kubernetes/compute-storage-net/device-plugins/#device-plugin-and-unhealthy-devices)）。因此，不能用“节点还有 `capacity`”否定设备故障，也不能用“新 Pod 不再调度到该设备”证明原有 Pod 已迁移或恢复。
- `allocatable` 表示节点可供调度核算的上限，不是当前未占用设备的直接清单。Kubernetes 的 PodResources 文档要求把可分配资源与运行中 Pod 的分配信息结合起来判断未分配资源，并说明底层资源或健康变化时需要重新获取（[GetAllocatableResources](https://v1-32.docs.kubernetes.io/docs/concepts/extend-kubernetes/compute-storage-net/device-plugins/#getallocatableresources-grpc-endpoint)）。
- Pod 级健康关联是有条件的：v1.32 文档中 `ResourceHealthStatus` 为 v1.31 引入的 alpha 特性门控，默认关闭；启用后 Pod `.status` 的容器状态增加 `allocatedResourcesStatus` 字段，报告已分配给容器的设备健康信息。未启用时，判断 Pod 是否关联故障设备只能用 PodResources API（[不健康设备节](https://v1-32.docs.kubernetes.io/docs/concepts/extend-kubernetes/compute-storage-net/device-plugins/#device-plugin-and-unhealthy-devices)）。
- 健康上报也不是硬件状态的完整镜像。设备插件把厂商检测结果映射为 Device Plugin API 的健康值；映射规则、采样间隔、容错策略和上报延迟都属于具体实现。资源账本正常只能说明对应控制面所见状态，不能替代驱动、硬件或任务进程的证据。

这些区别解释了两种常见分叉：设备变为不健康后，原有 Pod 仍持有分配而新 Pod 的可调度数量下降；框架因用户态库或 ABI 问题初始化失败时，设备插件和节点资源账本仍可能保持健康。

## 昇腾例子：固定 MindCluster 快照

本节只用 MindCluster tag `v26.1.1` 解引用到的 commit [`44385c13d7b1d87def35f1604e8be4d16de6ca4e`](https://github.com/Ascend/mind-cluster/tree/44385c13d7b1d87def35f1604e8be4d16de6ca4e)。它是通用链条的一个实现例子，不代表任意 MindCluster、Kubernetes、驱动、CANN 或 TorchNPU 组合均受支持。

固定快照的组件文档说明，Ascend Device Plugin 从驱动/DCMI 获取芯片类型、数量和健康状态，向 kubelet 上报，并在资源挂载阶段把选中的芯片信息传给 Ascend Docker Runtime（[英文组件说明](https://github.com/Ascend/mind-cluster/blob/44385c13d7b1d87def35f1604e8be4d16de6ca4e/docs/en/scheduling/introduction/01_component_description.md#ascend-device-plugin)）。同一快照的中文说明把接口职责明确写成 `Register` 上报资源名、`ListAndWatch` 上报数量/编号/健康状态、`Allocate` 配合 Ascend Docker Runtime 完成容器挂载（[中文组件说明](https://github.com/Ascend/mind-cluster/blob/44385c13d7b1d87def35f1604e8be4d16de6ca4e/docs/zh/scheduling/01_introduction/01_component_description.md#ascend-device-plugin)）。

源码使这些边界更具体：

- [`server.go`](https://github.com/Ascend/mind-cluster/blob/44385c13d7b1d87def35f1604e8be4d16de6ca4e/component/ascend-device-plugin/pkg/server/server.go#L144-L152) 构造包含 API 版本、endpoint 和资源名的 `RegisterRequest` 并调用 kubelet 注册接口。
- [`plugin.go` 的上报路径](https://github.com/Ascend/mind-cluster/blob/44385c13d7b1d87def35f1604e8be4d16de6ca4e/component/ascend-device-plugin/pkg/server/plugin.go#L193-L220) 把设备 ID 与健康值装入 `ListAndWatchResponse`；[`ListAndWatch`](https://github.com/Ascend/mind-cluster/blob/44385c13d7b1d87def35f1604e8be4d16de6ca4e/component/ascend-device-plugin/pkg/server/plugin.go#L293-L344) 负责把响应发给 kubelet 并维持流。
- [`Allocate`](https://github.com/Ascend/mind-cluster/blob/44385c13d7b1d87def35f1604e8be4d16de6ca4e/component/ascend-device-plugin/pkg/server/plugin.go#L1295-L1346) 根据 kubelet 请求形成 `ContainerAllocateResponse`。在该固定实现中，配置可走两条路径：直接添加带 `rw` 权限的设备节点，或设置 Ascend Docker Runtime 使用的环境信息（[挂载实现](https://github.com/Ascend/mind-cluster/blob/44385c13d7b1d87def35f1604e8be4d16de6ca4e/component/ascend-device-plugin/pkg/server/plugin.go#L1087-L1169)）。

这些文件能证明该快照中组件的职责和实现路径，不能证明某个现场 DaemonSet 正在运行、节点状态已经收敛、实际容器获得了预期设备，也不能证明容器内驱动文件、CANN 用户态库和框架后端彼此兼容。现有 TorchNPU 档案没有给出它与本 MindCluster 快照的同版本官方交集，所以不能把两组来源拼成“整栈已支持”。

## GPU 例子：NVIDIA k8s-device-plugin v0.20.1

本节固定为 tag `v0.20.1` 的 [NVIDIA k8s-device-plugin](https://github.com/NVIDIA/k8s-device-plugin/tree/v0.20.1)，取证范围为 [`internal/plugin/server.go`](https://github.com/NVIDIA/k8s-device-plugin/blob/v0.20.1/internal/plugin/server.go) 全 557 行与 [`internal/rm/health.go`](https://github.com/NVIDIA/k8s-device-plugin/blob/v0.20.1/internal/rm/health.go) 全 363 行（字节级取回，行数与仓库页面一致）。它是通用链条在 NVIDIA GPU 上的一个实现例子；分配 ID→注入通道→最终 OCI 节点→稳定身份的字段级核对方法（M-ID）在[镜像运行时基线](container-image-runtime-baseline.md) §2，本节不重复，也不从本实现推导其他版本或其他厂商插件。

### 发现、标识与上报

- 设备集由插件的资源管理层提供。插件向 kubelet 注册时上报 API 版本、socket endpoint 与资源名（如 `nvidia.com/gpu`），并声明支持 `GetPreferredAllocation`（[`Register` L229–256](https://github.com/NVIDIA/k8s-device-plugin/blob/v0.20.1/internal/plugin/server.go#L229-L256)）。注册后 `ListAndWatch` 的首个响应即全量设备清单（[`ListAndWatch` L267–270](https://github.com/NVIDIA/k8s-device-plugin/blob/v0.20.1/internal/plugin/server.go#L267-L285)）。
- 稳定标识：`Allocate` 按 `deviceIDStrategy` 把 kubelet 请求的设备 ID 转换并去重——`uuid` 策略下分配 ID 即 UUID，`index` 策略下为序号（[`uniqueDeviceIDsFromAnnotatedDeviceIDs` L456–474](https://github.com/NVIDIA/k8s-device-plugin/blob/v0.20.1/internal/plugin/server.go#L456-L474)）。`index` 序号→UUID 的宿主侧核对方法未取源（同基线 M-ID 的 K1 记录），多卡枚举顺序语义同样保持 K1。

### 分配与容器映射

- `Allocate`（[L306–320](https://github.com/NVIDIA/k8s-device-plugin/blob/v0.20.1/internal/plugin/server.go#L306-L320)）校验请求后构造响应：CDI 策略填 qualified CDI 名（annotations 或 `CdiDevices[].Name`，[`updateResponseForCDI` L377–409](https://github.com/NVIDIA/k8s-device-plugin/blob/v0.20.1/internal/plugin/server.go#L377-L409)）；`envvar` 策略把分配 ID 逗号串直写 `NVIDIA_VISIBLE_DEVICES`（[`updateResponseForDeviceListEnvVar` L481–483](https://github.com/NVIDIA/k8s-device-plugin/blob/v0.20.1/internal/plugin/server.go#L481-L483)）；`volume-mounts` 策略把 `/dev/null` 挂到 `/var/run/nvidia-container-devices/<id>`（[`updateResponseForDeviceMounts` L497–514](https://github.com/NVIDIA/k8s-device-plugin/blob/v0.20.1/internal/plugin/server.go#L497-L514)）；`passDeviceSpecs` 开启时另返回 `rw` DeviceSpec，其中 `/dev/nvidiactl` 等可选项 stat 不存在即跳过（[`apiDeviceSpecs` L516–557](https://github.com/NVIDIA/k8s-device-plugin/blob/v0.20.1/internal/plugin/server.go#L516-L557)）。这些只决定“分配了什么、以什么形式给容器”，不构成框架设备编号映射。
- 分配记录的查询入口：kubelet PodResources `List` 端点按 Pod/容器报告插件上报的设备 ID（[Monitoring 节](https://v1-32.docs.kubernetes.io/docs/concepts/extend-kubernetes/compute-storage-net/device-plugins/#monitoring-device-plugin-resources)）。容器最终配置与框架可见集的核对按基线 §2 M-ID 逐段执行，缺项按 K1/K2/K3 分类。

### 健康检查与上报

- 机制（[`health.go` checkHealth L44–172](https://github.com/NVIDIA/k8s-device-plugin/blob/v0.20.1/internal/rm/health.go)）：NVML 事件集，注册掩码含 XidCriticalError、双比特与单比特 ECC 三类（L78），但事件循环只处理 XidCriticalError，其余事件跳过（L133–136）。
- 忽略清单：硬编码忽略 XID 13、31、43、45、68、109（注释定性为应用错误、GPU 仍应视为健康；源码 FIXME 自述该清单未正式化，L229–240）；环境变量 `DP_DISABLE_HEALTHCHECKS`（`all`/`xids` 全禁或逗号分隔的忽略清单，L34）与 `DP_ENABLE_HEALTHCHECKS`（覆盖禁用，L40）调整该清单。
- 启动期失败即标记：placement 解析失败、按 UUID 取 handle 失败、读取支持事件类型失败都会立即把该设备标记为 unhealthy；`RegisterEvents` 返回 `ERROR_NOT_SUPPORTED` 时只警告“设备太老不支持健康检查”，不标记（L104–112）。
- 事件循环：等待超时继续；非超时等待错误标记**全部**设备（L124–131）；事件 UUID 解析失败同样标记全部（L145–153）；不属于本插件设备的事件忽略（L155–158）；MIG 设备按父 UUID＋GI/CI 过滤，事件携带无效 GI/CI 时不过滤（L160–167）；命中的 XID 把对应设备标记为 unhealthy（L169–170）。
- 降级路径：NVML 初始化失败时 `failOnInitError=true` 返回错误、`false` 直接返回（L46–57）；`Start` 对健康检查启动失败只记日志并继续运行，健康检查处于关闭状态（[`server.go` L151–157](https://github.com/NVIDIA/k8s-device-plugin/blob/v0.20.1/internal/plugin/server.go#L151-L157)）。此期间节点账本中的健康值不再反映 NVML 事件（按代码路径的推论，非文档明文）。
- 恢复：本版本 `ListAndWatch` 循环只有置 Unhealthy 的分支，源码注释写明 `FIXME: there is no way to recover from the Unhealthy state.`（[L277](https://github.com/NVIDIA/k8s-device-plugin/blob/v0.20.1/internal/plugin/server.go#L267-L285)）。设备恢复健康在上报层的条件未给出（unknown）；插件进程重建后该状态是否重置未取证（unknown）。

### 重启与账本刷新

- kubelet 重启：新 kubelet 实例启动时删除 `/var/lib/kubelet/device-plugins` 下全部既有 socket，插件应监测自身 socket 被删除并重新注册（[Handling kubelet restarts](https://v1-32.docs.kubernetes.io/docs/concepts/extend-kubernetes/compute-storage-net/device-plugins/#handling-kubelet-restarts)）。
- 插件进程：`Serve` 内置崩溃重启环——gRPC Serve 崩溃即重启，每次存活不足 1 小时计一次崩溃，累计超过 5 次即 `klog.Fatalf` 进程退出（[L186–215](https://github.com/NVIDIA/k8s-device-plugin/blob/v0.20.1/internal/plugin/server.go#L186-L215)）；`Stop` 删除 socket（[L163–174](https://github.com/NVIDIA/k8s-device-plugin/blob/v0.20.1/internal/plugin/server.go#L163-L174)）。DaemonSet 部署时可依赖 Kubernetes 在 daemon Pod 失败后重启它（[Deployment 节](https://v1-32.docs.kubernetes.io/docs/concepts/extend-kubernetes/compute-storage-net/device-plugins/#device-plugin-deployment)）。
- 插件进程重启（非 kubelet 重启）窗口内节点 `capacity`/`allocatable` 的表现，以及重启与既有分配的关系：所选来源未覆盖（unknown）。v1.32 文档“不健康设备”节只覆盖设备被标不健康的情形，不能外推到插件进程重启。

## Slurm 例子：固定 24.11.7 归档的 GRES/TRES 账本

Slurm 没有 Device Plugin 链条；它的设备账本由 slurm.conf/gres.conf 声明、slurmd 注册与作业生命周期共同维护，是独立视图，不能把上文的层一一映射过来。字段级参考见 [Slurm 作业生命周期、设备资源与状态参考](slurm-jobs-and-device-resources.md)（含全部归档页链接与站点配置边界），本节只取账本视角；来源固定为 24.11 归档（`https://slurm.schedmd.com/archive/slurm-24.11.7/` 前缀，裸域名可变页禁用），经 T05-03 取证复用。NPU（指 Ascend）接入无一手证据（unknown），以下 GPU 内容不得套用于 NPU。

### 发现、标识与声明

- 默认无 GRES：须 slurm.conf `GresTypes/Gres` 声明，未声明时节点无 GRES 资源——声明缺失不等于设备缺失，先查配置再查硬件。
- 稳定标识：gres.conf `File=/dev/nvidia<N>` 按 `/dev` minor 号记录；`AutoDetect=nvml`/`nvidia` 检测（24.11 起 `nvidia` 无需 nvml 库但不检 MIG/NVLink；仍需 slurm.conf Gres 行声明期望数）。NVML 按 PCI bus ID 编号、`/dev/nvidia*` 按 minor 号，两者映射“nondeterministic and system dependent, and could vary between boots”，文档要求 after-bootup check，且须 `CUDA_DEVICE_ORDER=PCI_BUS_ID` 才与 CUDA 编号一致。因此 gres.conf `File`、NVML 枚举与框架可见编号之间的对账不是一次性配置，而是每次启动后的核对动作（编号不稳影响坏卡/分卡对账为本库推论，非原文）。
- 记账：GRES 须写入 `AccountingStorageTRES` 才进入记账；`gres/gpu` 会同时置 `gres/gpumem` 与 `gres/gpuutil`；Billing 由分区 TRESBillingWeights 计算，权重为站点配置。

### 分配与 step 映射

- 分配记录：`scontrol show job` 的 GRES/TRES 字段；job 与 job step 严格区分，资源继承/独占按 gres 页，`scancel job.step` 只取消 step 不释放分配。
- step 映射：每个 step 设置 `CUDA_VISIBLE_DEVICES`，只反映该 step 所在节点的分配（sbatch 环境变量只反映 node zero）；`--gpu-bind`/`--tres-bind` 是绑定不是分配。
- 硬隔离前提：cgroup.conf `ConstrainDevices=yes`（文档默认 no）未开启时，GRES 分配不构成设备文件级隔离；Prolog/Epilog 在 cgroup 外运行，`CUDA_VISIBLE_DEVICES` 可与 job 内不同。设备可见≠应用成功：GRES 已分配不证框架初始化成功。

### 健康、daemon 重启与账本刷新

- 一致性校验：gres.conf `File`↔`Count` 一致，`Type`/`Cores`/`Links` 作 sanity check；失配节点的处理两页口径并存（gres 页“omitted from the node with an error”、gres.conf 页 invalid+drain）。检测设备多于配置时 slurmd 同样被 drain。
- 节点状态：INVAL＝注册资源少于配置，需 slurmd 重启后有效注册才清除；“有效配置”指内存/GRES/CPU ≥ slurm.conf 配置。DOWN 会终止其上运行与挂起的作业；`ReturnToService` 文档默认 0（须人工恢复，站点实际 unknown）；slurmctld 探测 `SlurmdTimeout` 默认 300 s。
- 健康检查：`HealthCheckProgram` 在 slurmd 启动注册前执行一次，之后按间隔在非 NOT_RESPONDING 节点定期执行（60 s 未结束被杀；发现问题由脚本自己 drain/发信）。GPU 运行期健康探测（ECC/XID 类）在所取页面无条目（unknown），站点脚本检查内容不可推定。
- 失败处置：Epilog 非零→节点 DRAIN；Prolog 非零→节点 DRAIN＋job 重排（默认 held）。
- 账本刷新条件：slurmd 重启并重新有效注册是节点 GRES 账本刷新的前提；作业结束经 Epilog 完成后节点才离开 COMPLETING。

## 三种实现的账本对照

三类常见不一致在不同实现里的证据位置和处理前置条件不同；下表只给定位入口，不设计统一错误码。处理动作的前置条件（授权、drain、重排/重启策略）以各生命周期指南为准：[Kubernetes 作业生命周期](kubernetes-job-lifecycle.md)、[Slurm 状态参考](slurm-jobs-and-device-resources.md)、[镜像运行时基线](container-image-runtime-baseline.md) §4 异常分支表、[容器内 NPU 可见性指南](ascend-device-visibility-triage.md)。

| 症状 | Kubernetes＋NVIDIA 插件 v0.20.1 | Slurm 24.11.7 | 昇腾（MindCluster 固定 commit） |
|---|---|---|---|
| 缺设备（驱动可见但平台无资源） | 插件注册/`ListAndWatch` 断点；注意健康检查降级不阻断上报，只让账本失去 NVML 事件来源 | 先查 slurm.conf `GresTypes/Gres` 声明与 AutoDetect/Type 子串匹配，再查 gres.conf 失配 drain；无声明不等于无设备 | 见上文“昇腾例子”节与可见性指南；插件注册/`ListAndWatch` 层同样适用 |
| 重复/过期分配 | 扩展资源为整数且不可超卖（调度层约束）；过期核对＝PodResources `List`（运行中分配）与容器最终配置/可见集比对，按 M-ID 逐段对应 | 重排队作业用 `sacct -D` 查同一 job ID 全部记录；`scancel job.step` 只取消 step 不释放分配；节点滞留 COMPLETING＝清理未完成 | 分配路径见“昇腾例子”节；容器内可见变量与分配 ID 的核对同指南 |
| 账本与实际占用不符 | `capacity` 不变而 `allocatable` 下降＝健康事件之后；`GetAllocatableResources` 须与运行中分配结合读取；本版插件无 Unhealthy 恢复路径，设备修复后账本不自动回升（恢复条件 unknown） | 节点 GRES 与 `slurmd -C/-G` 检测不符→invalid+drain；账本刷新以 slurmd 重注册为条件；DOWN/DRAIN 后作业已终止但节点未回 IDLE 属状态未收敛 | 插件上报与实际芯片状态之间无自动对账承诺（固定快照语义见“昇腾例子”节） |

## 身份核对与回收验证入口

- **GPU（Kubernetes）**：身份核对＝[镜像运行时基线](container-image-runtime-baseline.md) §2 M-ID 逐 ordinal 核对表（可见集快照→分配 ID→CDI 名/传递字段→最终 OCI 节点→UUID），缺项按 K1/K2/K3 分类记录。回收验证（设计，未执行）：Pod 删除前后各取一次 kubelet PodResources `List` 与节点 `allocatable`，核对分配条目消失且与容器留存证据一致；所选文档未给分配释放的专节语义，结果只作观察记录，不作释放完成的充分证明。
- **Slurm**：身份核对＝gres.conf `File` ↔ NVML PCI bus 枚举 ↔ `CUDA_DEVICE_ORDER=PCI_BUS_ID` 下框架编号的 after-bootup 对账（文档明示编号可变）；`slurmd -C/-G` 核对声明与检测。回收验证（设计，未执行）：作业结束后核对节点离开 COMPLETING（Epilog 完成）、`scontrol show node` 的 GRES/AllocTRES 释放、节点回 IDLE；清理卡住时查未退出进程/Epilog 与 `UnkillableStepTimeout`。
- **昇腾**：沿用[容器内 NPU 可见性指南](ascend-device-visibility-triage.md)、[来源案例](ascend-device-visibility-source-case.md)与[实验设计](ascend-device-visibility-experiment.md)三个入口；身份核对与回收验证的未知条件以各页记录为准。

## 如何读取一组互相矛盾的观察

| 观察组合 | 优先定位的断点 | 仍需补的证据 |
|---|---|---|
| 带外清单有设备，驱动不枚举 | 物理/固件到主机驱动之间 | 同一设备身份、固件与驱动初始化状态；不能先查调度 |
| 驱动枚举正常，节点没有扩展资源 | 设备插件注册、上报或 kubelet 节点状态更新 | 固定版本插件的注册对象、`ListAndWatch` 流和节点状态时序 |
| `capacity` 有值，`allocatable` 下降 | 健康上报到资源账本之间 | 不健康设备 ID、上报时间、原有 Pod 分配；不能把 `capacity` 当可用数 |
| Pod 已绑定节点，容器创建失败 | 具体分配或运行时配置应用阶段 | `Allocate` 结果、容器运行时事件、最终容器配置 |
| 容器内有设备节点，框架看不到设备 | 用户态依赖或框架后端阶段 | 目标进程的库加载、版本关系、框架初始化结果；不能回推为“没有物理设备” |
| 原有 Pod 仍在设备上，新 Pod 不再获得资源 | 健康变化对旧分配与新调度的不同作用 | 旧 Pod 的设备 ID、当前健康、节点 `allocatable` 与新 Pod 调度事件 |
| `slurmd -C/-G` 检出设备，节点却无 GRES 或被 drain（Slurm） | GRES 声明、AutoDetect 匹配或 gres.conf 一致性校验 | slurm.conf `GresTypes/Gres`、gres.conf `File/Count/Type`、节点状态与管理员填写的原因；不能把“无 GRES”读成“无设备” |

表中的“优先定位”只是缩小证据缺口，不是根因结论。跨层时间戳、节点身份、Pod UID、容器 ID、资源名和设备 ID 没有对齐时，看似矛盾的记录可能只是来自不同对象或不同时间。

## 适用边界与待确认

- `generic` 只表示本文用通用 Kubernetes Device Plugin 概念组织证据，不表示所有 Kubernetes 版本、厂商插件、GPU/NPU runtime 或框架具有相同字段和行为；Slurm GRES/TRES 是与该链独立的账本视图，两者不互相套用。
- Kubernetes 部分固定为 v1.32 文档；MindCluster 部分固定为 `v26.1.1` 解引用 commit；NVIDIA 插件部分固定为 tag `v0.20.1` 的 server.go 与 health.go；Slurm 部分固定为 24.11.7 归档（经 T05-03 取证复用，本轮未重开）。没有使用 `master`、main 或更晚文档补充这些快照的行为。
- 本文没有提供可执行诊断命令，也没有运行上游构建、安装、设备查询或集群操作；“身份核对与回收验证入口”为设计，未执行。`verification.status: source_checked` 只覆盖上述来源中职责、接口与实现位置的核对。
- 待确认：目标现场的 Kubernetes、设备插件、容器运行时、驱动/固件、用户态平台软件、框架后端、硬件型号和安全策略；Slurm 站点配置（`GresTypes`/gres.conf/cgroup.conf/`ReturnToService` 等全部数值，文档默认值不可当结论）；插件进程重启窗口的账本表现与不健康状态重置条件（unknown）；插件 NVML 设备发现层的失败场面行为（本轮取证范围为 server.go/health.go）；从设备健康变化到各控制面观察点的实际延迟。

## 来源

- [Kubernetes v1.32 Device Plugins](https://v1-32.docs.kubernetes.io/docs/concepts/extend-kubernetes/compute-storage-net/device-plugins/)：注册、`ListAndWatch`、`Allocate`、资源账本、kubelet 重启、不健康设备、`ResourceHealthStatus` 与 PodResources 语义。
- [NVIDIA k8s-device-plugin v0.20.1](https://github.com/NVIDIA/k8s-device-plugin/tree/v0.20.1)：[server.go](https://github.com/NVIDIA/k8s-device-plugin/blob/v0.20.1/internal/plugin/server.go)（注册、`ListAndWatch`、`Allocate` 响应构造、崩溃重启环）与 [health.go](https://github.com/NVIDIA/k8s-device-plugin/blob/v0.20.1/internal/rm/health.go)（NVML 事件健康检查）；取证记录见 [T05-04 来源记录](../../docs/research/batch-22-t05-04-sources.md)。
- [MindCluster `v26.1.1` 固定 commit](https://github.com/Ascend/mind-cluster/tree/44385c13d7b1d87def35f1604e8be4d16de6ca4e)：Ascend Device Plugin 文档与实现例子；来源核对范围见[研究记录](../../docs/research/batch-02-f11-sources.md)。
- [Slurm 24.11.7 归档 GRES/TRES/cgroup 页](https://slurm.schedmd.com/archive/slurm-24.11.7/gres.html)：GRES 声明/请求/AutoDetect、gres.conf 一致性、TRES 记账、cgroup 隔离前提与绑定（经 [Slurm 状态参考](slurm-jobs-and-device-resources.md) 复用 T05-03 取证）。
