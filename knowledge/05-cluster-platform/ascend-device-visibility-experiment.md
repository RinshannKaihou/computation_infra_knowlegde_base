---
id: cluster-platform.ascend-device-visibility-experiment
title: 容器内 NPU 不可见验证实验设计
type: experiment
domain: cluster-platform
status: draft
platforms: [ascend]
source_refs:
  - src.kubernetes.device-plugins-v1-32
  - src.ascend.mind-cluster-v26.1.1
  - src.vllm-ascend.issue-2557
  - src.vllm-ascend.pr-2541
updated_at: "2026-09-30"
summary: 用有请求、无请求、编号混用和恢复四组对照，逐层验证 NPU 从插件上报到框架逻辑设备的可见性。
related_ids:
  - cluster-platform.ascend-device-visibility-triage
  - cluster-platform.ascend-device-visibility-source-case
  - cluster-platform.device-resource-chain
applicability:
  environment_refs: []
  notes: 仅为专用 Kubernetes/Ascend 测试环境的实验设计；现场硬件、插件/runtime、镜像与资源名尚未确定。
verification:
  status: not_verified
  evidence_refs: []
  notes: 尚未创建 Pod、占用 NPU、修改设备映射或执行框架初始化；预期观察不是实测结果。
---

# 容器内 NPU 不可见验证实验设计

## 问题与假设

研究问题是：能否用主机、插件、节点资源、Pod 分配、容器最终配置和框架枚举的同一条证据链，区分“未请求设备”“设备注入成功”“物理 ID 被当作逻辑 ID”三种状态，并在恢复正常映射后回到基线？

假设 H1：正确请求一个健康 NPU 时，B0 可在每层关联到同一分配，并在目标进程中形成一个可选择的逻辑设备。假设 H2：无资源请求的 C0 不应出现 NPU 分配。假设 H3：若只把未经映射的物理编号传给要求逻辑范围的框架，N1 应在 ID 映射/选择层出现差异，而主机、插件和分配层仍与 B0 的相应条件一致。

实验不验证 HCCL、模型加载、吞吐、长时间稳定性或数值正确性。

## 环境与输入

执行前冻结并登记：

- 专用健康节点及硬件、驱动/固件、CANN；
- Kubernetes/kubelet、Ascend Device Plugin、Ascend Docker Runtime 与 container runtime；
- 设备扩展资源名和固定 Pod/镜像规格；
- 框架与设备后端版本、镜像 digest、运行用户和安全上下文；
- 节点、Pod UID、container ID、插件实例和设备 ID 的关联方法；
- 单设备枚举/选择脚本、退出状态和预期逻辑设备数。

MindCluster v26.1.1 固定文档仅提供设计依据：[Docker client usage](https://github.com/Ascend/mind-cluster/blob/44385c13d7b1d87def35f1604e8be4d16de6ca4e/docs/en/scheduling/usage/containerization/02_usage_on_the_docker_client.md)要求核对容器内外设备节点、驱动目录、DCMI 与管理工具；[Device Plugin 安装说明](https://github.com/Ascend/mind-cluster/blob/44385c13d7b1d87def35f1604e8be4d16de6ca4e/docs/en/scheduling/developer_guide/installation_deployment/manual_installation/04_ascend_device_plugin.md)记录 runtime、DCMI 权限和版本条件。实际环境必须有自己的配套依据。

## 实验设计

| 组 | 资源与映射条件 | 控制变量 | 预期用途 |
|---|---|---|---|
| B0 | Pod 正确请求 1 个 NPU，使用正常 runtime 注入和逻辑 ID | 固定节点、插件/runtime、镜像、用户和脚本 | 正控制；建立完整状态链 |
| C0 | 同镜像和用户，但 Pod 不请求 NPU；使用不会默认注入设备的 runtime 配置 | 除资源请求外与 B0 同类 | 负控制；验证在已固定隔离条件下“未申请”的状态 |
| N1 | 正确请求设备，但在隔离进程中把一个未经映射的物理 ID 当作逻辑 ID | 与 B0 同节点/镜像；只改选择输入 | 定位 ID 命名空间错误，不运行模型或 HCCL |
| R0 | 撤销 N1，恢复 B0 的正常注入和逻辑 ID | 与 B0 相同 | 回退对照，排除设备健康或插件状态漂移 |

B0、C0、N1、R0 按执行前确定的次数重复，并限定在同一时间窗。C0 必须与 B0 一样禁用 `privileged`、设备 `hostPath`、人工设备挂载和宿主机 PID/文件系统访问，并确认所选 runtime 不会在无资源请求时默认注入 NPU。否则“不请求扩展资源”本身不能推出“容器看不到设备”，C0 不能作为有效负控制。

N1 只有在平台文档和环境证据能安全区分物理/逻辑 ID 时才执行；不得猜测变量或设备编号。若无法构造单变量 N1，只保留 B0/C0/R0 并把 H3 记为未验证。

## 前置条件与运行影响

- 使用专用节点和隔离命名空间；实验会占用至少一个 NPU 和相应调度容量。
- 执行前确认没有其他租户依赖目标设备，并给 Pod 建立自动清理和资源回收方案。
- 固定 B0/C0 的 runtime class、安全上下文、设备 `hostPath`、人工挂载和显式设备环境变量；除计划中的资源请求外不得产生旁路注入。
- 不重启共享 kubelet、container engine 或设备插件，不修改生产 DaemonSet、安全策略或节点标签。
- N1 只做设备枚举和逐设备选择，不启动模型、collective 或长时任务。
- 发现主机设备健康变化、插件重启、节点资源账本漂移、Pod 被重建到其他节点，或实验影响其他负载时立即停止。

## 执行与记录方法

1. 采集主机设备/健康、插件实例与注册资源名、`ListAndWatch` 状态、节点 capacity/allocatable，确认基线稳定。
2. 审核 B0/C0 的 Pod 最终规格与 runtime 默认行为，确认没有 `privileged`、设备 `hostPath`、人工设备挂载或显式旁路注入；不满足则不使用 C0 推断可见性。
3. 创建 B0；记录 Pod UID、节点绑定、资源 request/limit、Allocate 的请求/返回、container ID 和最终容器配置。
4. 在 B0 同一用户进程记录设备节点、权限、挂载、注入环境、框架设备数和逻辑设备选择结果。
5. 清理 B0 并确认资源回收；创建 C0，重复相同观察，确认没有 Allocate 分配与旁路设备注入。
6. 重新建立正常基线后，在满足安全前提时执行 N1；只改变设备选择输入，保存首个错误和框架接受的逻辑范围。
7. 撤销 N1 建立 R0，重复 B0 输入；核对设备健康、插件代次和分配状态未变化。
8. 清理全部实验对象，确认节点资源账本、设备健康和命名空间回到实验前状态。

## 分层记录表

| 层次 | 必记对象与字段 |
|---|---|
| 主机 | 节点 UID、物理设备 ID、健康、驱动/固件、观察时间 |
| 插件 | Pod/进程实例、重启代次、资源名、设备 ID/health、上报时间 |
| 资源 | capacity、allocatable、Pod request/limit、调度事件 |
| 分配 | Pod UID、container 名、Allocate 请求/响应、分配设备 ID |
| 容器 | container ID、设备节点、权限、挂载、runtime 环境、安全上下文 |
| 进程 | 用户、PID/启动代次、框架设备数、逻辑 ID、逐设备选择与退出状态 |
| 恢复 | 资源回收时间、插件/设备健康、R0 与 B0 差异 |

Kubernetes v1.32 的 [Device Plugin 接口](https://v1-32.docs.kubernetes.io/docs/concepts/extend-kubernetes/compute-storage-net/device-plugins/#device-plugin-implementation)是记录 Register、ListAndWatch 和 Allocate 边界的依据。它不规定 Ascend 的具体物理/逻辑编号映射，因此映射语义仍须固定厂商 runtime 或框架资料。

## 通过、失败与无法判断的判据

设计通过要求同时满足：

1. B0 和 R0 在每层身份一致，插件上报与分配可关联，容器得到预期设备，框架只枚举并成功选择一个逻辑设备。
2. C0 没有 NPU request、Allocate 分配或容器设备注入，并且已排除 privileged、设备 hostPath、人工挂载和 runtime 默认注入；若这些隔离条件不成立，C0 结果为无法判断。镜像中只有用户态库不应误记为设备可用。
3. 若执行 N1，其与 B0 的唯一计划差异是编号输入，并且差异稳定地首现于框架逻辑 ID 选择；恢复后消失。
4. 实验对象清理后，节点资源账本和设备健康回到基线。

若主机健康、插件代次、分配设备、镜像或安全上下文同时变化，结果为无法判断。N1 不失败也不能证明任意物理编号可作为逻辑编号；它可能表示所选编号恰好重合或目标版本采用不同映射。B0 成功不证明多卡 HCCL、模型或长期任务正确。

## 实际结果与证据

尚未执行。当前没有 Pod、Allocate、容器配置、框架输出或恢复记录。

完成复现后才可将 `verification.status` 设为 `reproduced`，并填写非空、可定位的 `evidence_refs`。

## 局限、来源与后续问题

- [Kubernetes v1.32 Device Plugin 实现](https://v1-32.docs.kubernetes.io/docs/concepts/extend-kubernetes/compute-storage-net/device-plugins/#device-plugin-implementation)
- [MindCluster v26.1.1 Docker client usage](https://github.com/Ascend/mind-cluster/blob/44385c13d7b1d87def35f1604e8be4d16de6ca4e/docs/en/scheduling/usage/containerization/02_usage_on_the_docker_client.md)
- [vLLM Ascend #2557](https://github.com/vllm-project/vllm-ascend/issues/2557)与 [PR #2541](https://github.com/vllm-project/vllm-ascend/pull/2541)只提供物理/逻辑 ID 错配的案例依据。
- 局限：尚无目标环境，且固定 MindCluster 与案例中的 vLLM Ascend 版本没有被证明为一个官方配套组合。
- 待确认：专用节点、资源名、插件/runtime 版本、可安全执行的逻辑 ID 检查与重复次数。
