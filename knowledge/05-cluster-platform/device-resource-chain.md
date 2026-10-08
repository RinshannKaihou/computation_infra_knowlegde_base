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
updated_at: "2026-09-29"
summary: 区分设备物理存在、驱动可见、平台资源账本、具体分配、容器访问和框架可用，并说明各层证据的证明边界。
related_ids:
  - hardware.resource-topology
  - software-stack.layers-and-boundaries
  - software-stack.compatibility-evidence
verification:
  status: source_checked
  evidence_refs:
    - src.kubernetes.device-plugins-v1-32
    - src.ascend.mind-cluster-v26.1.1
  notes: 已核对 Kubernetes v1.32 Device Plugins 版本化页面，以及 MindCluster v26.1.1 解引用 commit 中的组件文档、README 和相关实现；未在真实集群、容器或 NPU 上执行验证。
---

# 从物理设备到容器资源的状态链

“节点有卡”不是一个足以判断任务能否使用加速器的状态。物理设备、驱动枚举、设备插件上报、节点资源账本、调度结果、具体设备分配、容器内访问条件和框架初始化分别由不同组件负责，也需要不同证据。

本文把这些观察位置组织成一条证据链：

> 物理设备存在 → 驱动可见 → 插件注册并上报 → 节点 `capacity` / `allocatable` → 调度 → 设备分配 → 容器设备节点、权限与用户态依赖 → 框架可用

箭头表示下一层通常依赖上一层，不表示已观察到左侧就能推出右侧，也不表示系统只能单向变化。这是一张跨层核对图，不是严格状态机。

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

## 如何读取一组互相矛盾的观察

| 观察组合 | 优先定位的断点 | 仍需补的证据 |
|---|---|---|
| 带外清单有设备，驱动不枚举 | 物理/固件到主机驱动之间 | 同一设备身份、固件与驱动初始化状态；不能先查调度 |
| 驱动枚举正常，节点没有扩展资源 | 设备插件注册、上报或 kubelet 节点状态更新 | 固定版本插件的注册对象、`ListAndWatch` 流和节点状态时序 |
| `capacity` 有值，`allocatable` 下降 | 健康上报到资源账本之间 | 不健康设备 ID、上报时间、原有 Pod 分配；不能把 `capacity` 当可用数 |
| Pod 已绑定节点，容器创建失败 | 具体分配或运行时配置应用阶段 | `Allocate` 结果、容器运行时事件、最终容器配置 |
| 容器内有设备节点，框架看不到设备 | 用户态依赖或框架后端阶段 | 目标进程的库加载、版本关系、框架初始化结果；不能回推为“没有物理设备” |
| 原有 Pod 仍在设备上，新 Pod 不再获得资源 | 健康变化对旧分配与新调度的不同作用 | 旧 Pod 的设备 ID、当前健康、节点 `allocatable` 与新 Pod 调度事件 |

表中的“优先定位”只是缩小证据缺口，不是根因结论。跨层时间戳、节点身份、Pod UID、容器 ID、资源名和设备 ID 没有对齐时，看似矛盾的记录可能只是来自不同对象或不同时间。

## 适用边界与待确认

- `generic` 只表示本文用通用 Kubernetes Device Plugin 概念组织证据，不表示所有 Kubernetes 版本、厂商插件、GPU/NPU runtime 或框架具有相同字段和行为。
- Kubernetes 部分固定为 v1.32 文档；MindCluster 部分固定为 `v26.1.1` 解引用 commit。没有使用 `master` 或更晚文档补充该快照的行为。
- 本文没有提供可执行诊断命令，也没有运行上游构建、安装、设备查询或集群操作。`verification.status: source_checked` 只覆盖上述来源中职责、接口与实现位置的核对。
- 待确认：目标现场的 Kubernetes、设备插件、容器运行时、驱动/固件、用户态平台软件、框架后端、硬件型号和安全策略，以及从设备健康变化到各控制面观察点的实际延迟。

## 来源

- [Kubernetes v1.32 Device Plugins](https://v1-32.docs.kubernetes.io/docs/concepts/extend-kubernetes/compute-storage-net/device-plugins/)：注册、`ListAndWatch`、`Allocate`、资源账本、不健康设备和 PodResources 语义。
- [MindCluster `v26.1.1` 固定 commit](https://github.com/Ascend/mind-cluster/tree/44385c13d7b1d87def35f1604e8be4d16de6ca4e)：Ascend Device Plugin 文档与实现例子；来源核对范围见[研究记录](../../docs/research/batch-02-f11-sources.md)。
