---
id: cluster-platform.ascend-device-visibility-triage
title: 容器内 NPU 不可见诊断指南
type: procedure
domain: cluster-platform
status: draft
platforms: [ascend]
source_refs:
  - src.kubernetes.device-plugins-v1-32
  - src.ascend.mind-cluster-v26.1.1
updated_at: "2026-09-30"
summary: 沿主机、设备插件、节点资源、Pod 分配、容器访问和框架枚举逐层定位 Ascend NPU 可见性断点。
related_ids:
  - cluster-platform.device-resource-chain
  - software-stack.ascend-documented-profile
  - reliability.evidence-and-hypotheses
applicability:
  environment_refs: []
  notes: 适用于 Kubernetes Device Plugin 或 Ascend Docker Runtime 路径的证据分层；现场版本、硬件、资源名和 runtime 配置尚未指定。
verification:
  status: source_checked
  evidence_refs:
    - src.kubernetes.device-plugins-v1-32
    - src.ascend.mind-cluster-v26.1.1
  notes: 已核对 Kubernetes v1.32 Device Plugin 文档及 MindCluster v26.1.1 固定文档和实现边界；未访问集群、容器或 NPU。
---

# 容器内 NPU 不可见诊断指南

## 目标与触发条件

当 Pod 已调度或独立 Docker 容器已创建，但容器里没有 NPU 节点、管理工具与框架看到的设备不一致、框架设备数为零，或选择某个编号失败时，本流程用于定位最早断点。调查必须沿[物理设备到容器资源的状态链](device-resource-chain.md)按实际路径连接同一主机、容器和设备身份；Kubernetes 路径另需 Pod、插件与分配身份。

“NPU 不可见”至少可能指四种不同状态：主机驱动未枚举设备；Kubernetes 没有该扩展资源；容器未得到已分配设备；容器有设备但框架的逻辑编号或用户态依赖失败。HCCL 初始化失败发生在设备枚举之后时，应转交通信诊断，不能自动归入不可见。

## 适用范围与前置条件

- 两条路径都固定主机身份、container ID、时间窗和目标进程用户；Kubernetes 另记节点 UID、Pod UID、资源名和插件实例。只按名称关联可能串入重建后的对象。
- 两条路径都记录 container runtime、驱动/固件、CANN、框架、镜像及使用的 Ascend runtime 版本；Kubernetes 另记录 kubelet、插件与平台版本。独立 Docker 没有这些组件是可接受的路径差异。
- 先明确工作负载是否通过 Device Plugin 请求 NPU，还是使用独立 Docker client/runtime 路径；两条路径不能混成同一调用链。
- 观察应尽量只读。重启 kubelet、container engine、插件，修改安全策略或重新创建 Pod 都会改变证据，须另有授权和回退。
- MindCluster tag `v26.1.1` 固定 commit `44385c13d7b1d87def35f1604e8be4d16de6ca4e` 只作为一种实现样板，不代表现场组合受支持。

## 需要的证据

| 层次 | 同一实体/时点的观察对象 | 用途 | 缺失时如何处理 |
|---|---|---|---|
| 主机与驱动 | 物理设备清单、驱动枚举、健康状态、节点身份 | 判断断点是否早于 Kubernetes | 不先检查插件或 Pod；主机状态记未知 |
| Kubernetes：设备插件 | 实例、注册资源名、`ListAndWatch` 设备 ID/health 与时间 | 判断插件是否持续上报 | 不能用“插件进程存在”代替注册和上报证据 |
| Kubernetes：节点资源账本 | 对应资源名的 capacity、allocatable、更新时间 | 判断 kubelet/API server 所见状态 | 不能把 capacity 当空闲数或具体分配 |
| Kubernetes：调度与分配 | Pod request/limit、绑定节点、Allocate 请求/响应、分配 ID | 判断 Pod 是否获得设备 | 已绑定不等于具体分配或容器创建成功 |
| 容器最终配置 | 设备节点、权限、挂载、runtime 注入环境、container ID | 判断 Allocate 返回或独立 Docker 创建配置是否被应用 | 不能由控制面预期代替容器实况 |
| 用户态与框架 | 同一用户/进程的设备数、逻辑 ID、初始化和最小选择 | 判断编号映射、库/ABI 或后端问题 | 不外推到 HCCL、模型或数值正确性 |

独立 Docker 路径另保存容器创建规格、选用的 runtime、`ASCEND_VISIBLE_DEVICES` 原值及实际注入；以这些配置作为期望，不要求 Kubernetes 注册、节点资源或 Allocate 记录。固定 [Device Plugin 安装说明第 5–7 行](https://github.com/Ascend/mind-cluster/blob/44385c13d7b1d87def35f1604e8be4d16de6ca4e/docs/en/scheduling/developer_guide/installation_deployment/manual_installation/04_ascend_device_plugin.md#L5-L7)明确仅容器化/监控用途无需该插件。

Kubernetes v1.32 的 [Device Plugin 实现文档](https://v1-32.docs.kubernetes.io/docs/concepts/extend-kubernetes/compute-storage-net/device-plugins/#device-plugin-implementation)规定插件经注册后用 `ListAndWatch` 报告设备和健康，在容器创建期间由 `Allocate` 返回设备节点、环境变量、挂载或 CDI 信息。因此，节点有扩展资源、Pod 已绑定、Allocate 成功和容器能访问设备是四个不同状态。

## 步骤与判断分支

| 步骤 | 检查或动作 | 运行影响 | 预期证据与解释 | 下一步 |
|---|---|---|---|---|
| 1 | 选择 Kubernetes 或独立 Docker 路径，冻结其主机/容器/设备及可选 Pod 身份，保存症状 | 只读 | 身份一致才可串链；任一对象重建则另起时间线 | 完整进入 2，否则停止补证 |
| 2 | 在主机边界确认驱动是否枚举目标设备及健康 | 只读管理查询；具体命令须按版本核实 | 主机不可见时先查硬件/驱动；正常后按部署路径分流 | Kubernetes 进入 3；独立 Docker 以创建规格/runtime 注入为期望，直接进入 5 |
| 3（仅 Kubernetes） | 核对插件实例、资源名、注册与 `ListAndWatch` | 只读日志/状态 | 无注册、资源名不符、DCMI/权限失败或上报中断支持插件层假设 | 正常进入 4；异常保留版本和权限证据 |
| 4（仅 Kubernetes） | 对齐节点 capacity/allocatable、Pod request/limit、绑定和 Allocate | 只读控制面/节点证据 | 无请求、资源名错误、调度不足与 Allocate 失败须分开 | 已分配进入 5；否则停在对应层 |
| 5 | Kubernetes 对比 Allocate 返回；独立 Docker 对比创建规格/可见设备变量/runtime 配置；均核对容器最终节点、权限、挂载、环境 | 容器内只读；不重建 | 缺节点/挂载或策略拒绝支持 runtime/hook/安全层断点 | 一致进入 6；不一致定位 runtime 应用 |
| 6 | 在目标用户、目标进程中核对设备数、逻辑 ID 与单设备选择 | 可能初始化设备并占少量资源；需现场授权 | 管理工具可见而框架失败支持编号映射、库/ABI 或后端假设 | 枚举成功后移交后续专题 |

### 固定 MindCluster 资料给出的具体边界

MindCluster v26.1.1 的 [Docker client usage](https://github.com/Ascend/mind-cluster/blob/44385c13d7b1d87def35f1604e8be4d16de6ca4e/docs/en/scheduling/usage/containerization/02_usage_on_the_docker_client.md#operation-procedure)要求在容器内外核对设备节点、驱动目录、DCMI 和 `npu-smi`；同一文件的[环境变量说明](https://github.com/Ascend/mind-cluster/blob/44385c13d7b1d87def35f1604e8be4d16de6ca4e/docs/en/scheduling/usage/containerization/02_usage_on_the_docker_client.md#L101-L110)说明需要 NPU 的任务应指定 `ASCEND_VISIBLE_DEVICES`，值为 `void` 时不挂载 NPU、驱动或相关目录。这是 Docker client 路径的固定实现说明，不应改写成所有 Kubernetes 部署都需人工设置相同变量。

同一快照的 [Ascend Device Plugin 安装说明](https://github.com/Ascend/mind-cluster/blob/44385c13d7b1d87def35f1604e8be4d16de6ca4e/docs/en/scheduling/developer_guide/installation_deployment/manual_installation/04_ascend_device_plugin.md#L31-L53)要求注意 runtime 安装顺序与版本一致、特定条件下重启 container engine，并列出 DCMI 路径所有权、权限、目录深度和 `LD_LIBRARY_PATH` 长度限制。Atlas 200I SoC A1 还有文档中的例外；未确认硬件时不得套用其他型号流程。

固定源码显示该实现的 [`Register`](https://github.com/Ascend/mind-cluster/blob/44385c13d7b1d87def35f1604e8be4d16de6ca4e/component/ascend-device-plugin/pkg/server/server.go#L144-L152)、[`ListAndWatch`](https://github.com/Ascend/mind-cluster/blob/44385c13d7b1d87def35f1604e8be4d16de6ca4e/component/ascend-device-plugin/pkg/server/plugin.go#L293-L344)与 [`Allocate`](https://github.com/Ascend/mind-cluster/blob/44385c13d7b1d87def35f1604e8be4d16de6ca4e/component/ascend-device-plugin/pkg/server/plugin.go#L1295-L1346)职责。源码证明实现路径，不证明现场实例已成功执行。

## 常见证据组合

涉及插件、capacity/allocatable、Pod 与 Allocate 的行只适用 Kubernetes；独立 Docker 以创建规格和 runtime 注入证据代替这些环节。

| 观察组合 | 优先定位 | 仍不能声称 |
|---|---|---|
| 主机不枚举，插件也不上报 | 硬件/固件/驱动或主机管理库 | 插件配置是唯一根因 |
| 主机正常，节点无扩展资源 | 插件注册、DCMI/权限、版本或 kubelet 状态 | 调度与容器已经检查 |
| capacity 有，allocatable 下降 | 健康上报与资源账本 | capacity 表示空闲设备数 |
| Pod 已绑定，Allocate 失败 | 请求资源名、设备健康、插件分配路径 | 容器 runtime 一定有问题 |
| Allocate 有返回，容器缺设备/挂载 | runtime/hook 应用、安全策略或容器创建 | 框架版本是根因 |
| 容器管理工具列出设备，框架数为零或选号失败 | 物理/逻辑 ID、用户权限、用户态库/ABI、框架后端 | “容器内没有任何 NPU” |
| 枚举和单设备选择通过，HCCL 初始化失败 | 通信配置、拓扑、进程成员或权限 | 设备不可见仍是首要假设 |

## 停止条件与恢复安排

节点/Pod/container/device 身份对不上，观测跨越重建前后，现场版本不在来源覆盖范围，或关键层只有推断而没有记录时，停止形成根因结论。需要重启 container engine、kubelet、插件，修改 DaemonSet/安全策略或重新调度生产 Pod 时，也应停止并走独立变更流程。

只在设备已枚举和单设备选择通过后出现 HCCL 或 collective 错误时，本流程完成到“设备可见”，后续移交通信专题。若已做隔离变更，按路径恢复 Pod 或独立 Docker 创建规格、runtime 配置和安全策略，确认工作负载与适用的资源账本回到记录中的基线；恢复失败时不得继续叠加动作。

## 完成判据

完成时按路径验收：

- Kubernetes：同一时间窗串起主机、插件、节点资源、调度/Allocate、容器最终配置和目标进程；恢复可见性时只枚举分配给该容器的设备并能按逻辑 ID 选择。
- 独立 Docker：串起主机、容器创建规格/目标设备集、所选 runtime 与注入配置、容器最终配置和目标进程；恢复可见性时枚举/选择与期望设备集一致，无需补造插件或 Allocate 证据。

两条路径都要给出最早断点、责任组件及未知项；没有恢复验证时只交付定位结论，不写设备可见性已恢复。所有修改已恢复或明确移交。

完成“可见性诊断”不等于 HCCL、模型加载、推理/训练持续运行、性能或数值正确。未核对的层次和现场版本保持 `unknown`。

## 来源与验证记录

- [Kubernetes v1.32 Device Plugins](https://v1-32.docs.kubernetes.io/docs/concepts/extend-kubernetes/compute-storage-net/device-plugins/)
- [MindCluster v26.1.1 Docker client usage](https://github.com/Ascend/mind-cluster/blob/44385c13d7b1d87def35f1604e8be4d16de6ca4e/docs/en/scheduling/usage/containerization/02_usage_on_the_docker_client.md)
- [MindCluster v26.1.1 Ascend Device Plugin installation](https://github.com/Ascend/mind-cluster/blob/44385c13d7b1d87def35f1604e8be4d16de6ca4e/docs/en/scheduling/developer_guide/installation_deployment/manual_installation/04_ascend_device_plugin.md)
- 当前验证范围：只核对公开文档与固定源码，未访问真实集群或容器。
- 待确认：现场硬件、Kubernetes、插件/runtime、驱动/CANN/框架版本及资源名。
