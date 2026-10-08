# 第二批 F11 来源核对：设备资源状态链

核对日期：2026-09-29

对应正文：[从物理设备到容器资源的状态链](../../knowledge/05-cluster-platform/device-resource-chain.md)

## 核对范围与方法

本轮只核对通用 Kubernetes Device Plugin 语义和一个固定 MindCluster Ascend Device Plugin 快照。Kubernetes 沿用已登记的 `src.kubernetes.device-plugins-v1-32`；MindCluster 新增固定来源 `src.ascend.mind-cluster-v26.1.1`。

MindCluster 通过官方 Git 仓库执行只读 refs 查询，确认 annotated tag `v26.1.1` 解引用到 commit `44385c13d7b1d87def35f1604e8be4d16de6ca4e`，随后浅克隆该 tag 到临时目录逐文件阅读。`HEAD` 与 tag 解引用 commit 一致，commit 日期为 2026-08-29。没有安装、编译或运行仓库中的组件和命令，也没有访问真实集群、容器或 NPU。

固定快照的 `README-EN.md` 维护表没有列出 `v26.1.1`，因此本记录只把 Git tag 与解引用 commit 当作来源身份，不从该表推断此 tag 的维护期、兼容矩阵或生产适用性。仓库 `master` 及更晚文档未用于补写该快照行为。

## 已打开的精确来源

| 对象 | 固定位置 | 核对到的内容 | 不能支持的结论 |
|---|---|---|---|
| Kubernetes Device Plugins v1.32 | <https://v1-32.docs.kubernetes.io/docs/concepts/extend-kubernetes/compute-storage-net/device-plugins/> | 注册所需 socket/API 版本/资源名；成功注册后的设备列表与节点状态；`ListAndWatch`、`Allocate`；不健康设备降低 `allocatable` 而 `capacity` 不变；原有 Pod 保持分配；PodResources 的分配与可分配语义 | 任意厂商插件的具体资源名、容错策略、挂载内容或版本兼容 |
| MindCluster tag 身份 | <https://github.com/Ascend/mind-cluster/tree/44385c13d7b1d87def35f1604e8be4d16de6ca4e> | `v26.1.1` 解引用后的固定源码树 | 该 tag 与 TorchNPU、CANN、驱动、Kubernetes 或硬件的整栈兼容 |
| Ascend Device Plugin README | <https://github.com/Ascend/mind-cluster/blob/44385c13d7b1d87def35f1604e8be4d16de6ca4e/component/ascend-device-plugin/README.md> | 文件标题为 “Ascend Device Plugin”；组件介绍说明从驱动发现设备数、向 Kubernetes 上报、健康检查和设备分配 | 现场已经部署；README 中产品列表覆盖所有功能组合；重调度在未列出的组件与策略下必然发生 |
| 英文组件说明 | <https://github.com/Ascend/mind-cluster/blob/44385c13d7b1d87def35f1604e8be4d16de6ca4e/docs/en/scheduling/introduction/01_component_description.md#ascend-device-plugin> | 文件中 “Ascend Device Plugin” 段说明从驱动/DCMI 获取类型、数量和健康信息，向 kubelet/ClusterD 上报，并把调度选中的芯片信息交给 Ascend Docker Runtime | 运行时环境、镜像或框架后端已经可用 |
| 中文组件说明 | <https://github.com/Ascend/mind-cluster/blob/44385c13d7b1d87def35f1604e8be4d16de6ca4e/docs/zh/scheduling/01_introduction/01_component_description.md#ascend-device-plugin> | “组件功能”逐项列出 `Register`、`ListAndWatch` 和 `Allocate` 的职责；“组件上下游依赖”列出 DCMI、kubelet、ClusterD 与 Ascend Docker Runtime | 接口调用在目标集群成功，或每种设备/虚拟化模式都走同一分支 |
| 注册实现 | <https://github.com/Ascend/mind-cluster/blob/44385c13d7b1d87def35f1604e8be4d16de6ca4e/component/ascend-device-plugin/pkg/server/server.go#L144-L152> | 构造包含 `Version`、`Endpoint`、`ResourceName` 的 `RegisterRequest` 并调用 kubelet registration client | kubelet 已接受请求、API server 已看到资源或节点状态已收敛 |
| 上报实现 | <https://github.com/Ascend/mind-cluster/blob/44385c13d7b1d87def35f1604e8be4d16de6ca4e/component/ascend-device-plugin/pkg/server/plugin.go#L193-L220> 与 <https://github.com/Ascend/mind-cluster/blob/44385c13d7b1d87def35f1604e8be4d16de6ca4e/component/ascend-device-plugin/pkg/server/plugin.go#L293-L344> | `ListAndWatchResponse` 包含设备 ID 与健康值；实现向 kubelet 发送响应并维持流 | 该健康值等于全部实时硬件状态，或没有采样/容错/传播延迟 |
| 分配与挂载实现 | <https://github.com/Ascend/mind-cluster/blob/44385c13d7b1d87def35f1604e8be4d16de6ca4e/component/ascend-device-plugin/pkg/server/plugin.go#L1087-L1169> 与 <https://github.com/Ascend/mind-cluster/blob/44385c13d7b1d87def35f1604e8be4d16de6ca4e/component/ascend-device-plugin/pkg/server/plugin.go#L1295-L1346> | `Allocate` 形成 `ContainerAllocateResponse`；固定实现可直接返回 `rw` 设备节点，也可设置 Ascend Docker Runtime 所用信息 | 容器运行时已应用响应、容器内文件/权限/库完整、框架可以初始化或执行负载 |
| 根代码许可证 | <https://github.com/Ascend/mind-cluster/blob/44385c13d7b1d87def35f1604e8be4d16de6ca4e/LICENSE> | Apache License 2.0 文本 | `docs/`、第三方依赖和发行包自动属于相同许可范围 |
| Device Plugin 组件许可证 | <https://github.com/Ascend/mind-cluster/blob/44385c13d7b1d87def35f1604e8be4d16de6ca4e/component/ascend-device-plugin/LICENSES/LICENSE> | Apache License 2.0 文本；`LICENSES/vendor/` 另含依赖许可证 | vendored 依赖可一概按 Apache-2.0 处理 |
| 文档许可证 | <https://github.com/Ascend/mind-cluster/blob/44385c13d7b1d87def35f1604e8be4d16de6ca4e/docs/LICENSE> | Creative Commons Attribution 4.0 International 文本 | 代码、构建产物或发行包属于 CC-BY-4.0 |

正文采用原创归纳并链接精确文件，没有复制图片、长段文档或源码。代码、`docs/` 文档、vendored 依赖和发行包的许可范围分别处理。

## 证据边与缺口

| 关系 | 本轮状态 | 依据或缺口 |
|---|---|---|
| Kubernetes 插件注册 → 节点扩展资源上报 | 来源已核对 | Kubernetes v1.32 注册段直接描述 kubelet 的节点状态更新职责 |
| 健康变化 → `allocatable` 下降、`capacity` 不变 | 来源已核对 | Kubernetes v1.32 “Device plugin and unhealthy devices” 段直接说明 |
| 健康变化 → 原有 Pod 自动迁移 | 不成立为通用推论 | 同一段明确说明原有 Pod 继续保持对故障设备的分配；迁移/重调度需要另行证明具体控制器与策略 |
| MindCluster v26.1.1 的注册、上报和分配实现 | 来源已核对 | 固定组件文档、`server.go` 和 `plugin.go` 相互印证职责与代码路径 |
| `AllocateResponse` → 容器实际访问成功 | 未验证 | 缺目标集群的 kubelet/运行时事件、最终容器配置和容器内观察 |
| 容器设备可见 → 框架可用 | 未验证 | 缺目标镜像的驱动用户态文件、CANN、框架后端、ABI 与最小负载证据 |
| MindCluster v26.1.1 ↔ 现有 TorchNPU/CANN 档案 | `unknown` | 没有把该 MindCluster commit 与 `torch_npu 2.6.0.post3 + CANN 8.3.RC1` 放在同一支持声明中的官方来源；不得把第一批 TorchNPU 档案拼成整栈结论 |

## 建议加入 `sources/registry.yaml` 的完整条目

以下条目符合当前 `schemas/sources.schema.json`。F11 子任务不修改共享 registry，由主任务统一合入。

```yaml
- id: src.ascend.mind-cluster-v26.1.1
  title: MindCluster v26.1.1 固定源码快照
  url: https://github.com/Ascend/mind-cluster/tree/44385c13d7b1d87def35f1604e8be4d16de6ca4e
  kind: repository
  registered_at: "2026-09-29"
  revision: 44385c13d7b1d87def35f1604e8be4d16de6ca4e
  license:
    status: partial
    scopes:
      - scope: 固定 commit 的仓库根代码与配置；第三方文件按各自声明核查
        identifier: Apache-2.0
        url: https://github.com/Ascend/mind-cluster/blob/44385c13d7b1d87def35f1604e8be4d16de6ca4e/LICENSE
      - scope: 固定 commit 的 component/ascend-device-plugin 自有代码；LICENSES/vendor 下依赖另计
        identifier: Apache-2.0
        url: https://github.com/Ascend/mind-cluster/blob/44385c13d7b1d87def35f1604e8be4d16de6ca4e/component/ascend-device-plugin/LICENSES/LICENSE
      - scope: 固定 commit 的 docs 目录文档；第三方素材按各自声明核查
        identifier: CC-BY-4.0
        url: https://github.com/Ascend/mind-cluster/blob/44385c13d7b1d87def35f1604e8be4d16de6ca4e/docs/LICENSE
    notes: 代码、文档和 vendored 依赖分开登记；未核验发行包、镜像及其第三方内容的再分发条件。
  notes: annotated tag v26.1.1 在 2026-09-29 核查时解引用到此 commit。用于核对 Ascend Device Plugin 的 README、组件说明及 Register、ListAndWatch、Allocate 实现；未安装、构建或运行，也不构成与 Kubernetes、驱动、CANN、TorchNPU 或硬件的整栈配套声明。
```

## 未完成项

- 没有目标集群环境档案，无法判断现场 Kubernetes 版本、插件部署参数、设备型号、驱动/固件、Ascend Docker Runtime、CANN、镜像或框架后端。
- 没有现场时间线，无法量化驱动健康变化、`ListAndWatch`、节点状态、调度器缓存和工作负载行为之间的传播延迟。
- 没有制品摘要、镜像 digest、运行日志、Pod UID/容器 ID 或设备 ID 对齐记录；本轮只做来源核对。
- 未核验 MindCluster 发行包和容器镜像的内容、签名、依赖许可证或与源码快照的一致性。
