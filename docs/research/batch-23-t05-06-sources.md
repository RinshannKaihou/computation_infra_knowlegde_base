# 第二十三批 T05-06 来源记录

任务：T05-06（加速器共享与租户隔离机制，concept 类新文章的知识材料）。取证轮次：作者侧首轮（2026-10-18）。原计划的只读取证子代理因账户周配额（403）未执行，本记录由主会话作者角色直接取证。取证方式全部为 FetchURL 只读；未做 curl 字节级取回与哈希校验；未部署、未配置共享模式、未运行任何 GPU/NPU 工作负载。

版本声明：

- NVIDIA MIG User Guide：`https://docs.nvidia.com/datacenter/tesla/mig-user-guide/` 为随驱动更新的可变文档站，本轮实开 index、supported-gpus、concepts 三页（2026-10-18 观察），未固定驱动版本；引用时以观察日期标注。
- NVIDIA MPS 文档：`https://docs.nvidia.com/deploy/mps/` 为可变文档站，本轮实开 index 与 when-to-use-mps 两页（2026-10-18 观察）；文档区分 Legacy MPS v2 与 MPS v3，本文引用未绑定具体 CUDA 版本。
- NVIDIA k8s-device-plugin：固定 commit `487d7a93894b0f3ad08097169593972eb3ca8206`（tag v0.20.1），实开同一 commit 的 `README.md`（raw 全文）。
- Ascend：固定 mind-cluster commit `44385c13d7b1d87def35f1604e8be4d16de6ca4e`（tag v26.1.1），实开 `component/ascend-device-plugin/README.md`（raw 全文）。

## 主张—来源定位表（ID—精确页面/节—字段/支持范围）

| 主张 | 登记 ID | 精确页面/节 | 支持范围 / 未覆盖 |
|---|---|---|---|
| MIG 的支持代际与机型 | NEW src.nvidia.mig-user-guide-2026-10-18 | [supported-gpus.html](https://docs.nvidia.com/datacenter/tesla/mig-user-guide/supported-gpus.html)（Supported GPUs 表） | 支持 Ampere 及更新（compute capability ≥ 8.0）；表列 A100/A30、H100/H200/H20、B200/GB200/GB300、RTX PRO Blackwell、Thor iGPU，单产品最大实例数 2/4/7。未覆盖：具体驱动最低版本、各机型 profile 全集 |
| MIG 的分区单位与隔离语义 | NEW src.nvidia.mig-user-guide-2026-10-18 | [concepts.html](https://docs.nvidia.com/datacenter/tesla/mig-user-guide/concepts.html)（Terminology/Partitioning/Profile Placement 节） | memory slice≈1/8 显存资源（含容量与带宽）、SM slice≈1/7 SM；GI=slice+引擎，提供 memory QoS；CI 细分 SM slice、共享父 GI 的显存与引擎；profile 组合受物理位置限制，创建/销毁可产生碎片。未覆盖：各机型完整可组合 profile 表（supported profiles 页未开） |
| MIG/MPS/streams 的隔离能力对照 | NEW src.nvidia.mig-user-guide-2026-10-18 | concepts.html 的 CUDA Concurrency Mechanisms 节与 Table 3 | 分区类型 Streams 单进程 / MPS 逻辑 / MIG 物理；最大分区 Unlimited/48/7；SM 性能隔离 No/Yes（按百分比，非分区）/Yes；显存保护 No/Yes/Yes；显存带宽 QoS No/No/Yes；错误隔离 No/No/Yes；跨分区互操作 Always/IPC/Limited IPC；重配置 Dynamic/Process Launch/When Idle。这是本任务最关键的一张官方对照表 |
| MPS 的适用条件与共享语义 | NEW src.nvidia.mps-docs-2026-10-18 | [index.html](https://docs.nvidia.com/deploy/mps/index.html)（组件、收益、文档结构）；[when-to-use-mps.html](https://docs.nvidia.com/deploy/mps/when-to-use-mps.html)（System Considerations/Application Considerations/Memory Protection and Error Containment/Dynamic Execution Resource Provisioning/Limits/Static SM Partitioning 节） | 控制 daemon + server + client runtime 三段式；仅 Linux/QNX；**同一系统只有一个用户可持有活动 MPS server**，控制 daemon 会串行化不同用户的激活请求；客户端行为在监控/记账中归属 server 进程；客户端地址空间完全隔离，但错误遏制有限（故障波及共享该 GPU 子集的全部客户端且不指出肇事者，server 转 FAULT）；动态资源限额只是上限、不是预留；静态 SM 分区（Ampere+，chunk 单位）提供确定性分配与空间隔离。未覆盖：服务器故障注入、实际性能数据 |
| MPS 的关键限制清单 | NEW src.nvidia.mps-docs-2026-10-18 | when-to-use-mps.html（Limitations/Client-Server Connection Limits/MPS Device Memory Limit/Client Early Termination） | 仅 64 位应用；驱动 API ≥ CUDA 4.0；不支持 dynamic parallelism；默认要求同 UID（`-multiuser-server` 会放弃用户间隔离）；未同步即终止客户端可使 server 与其他客户端进入未定义状态；默认连接上限 60 client CUDA contexts/device（`CUDA_DEVICE_MAX_CONNECTIONS=2` 时）；显存上限用 `CUDA_MPS_PINNED_DEVICE_MEM_LIMIT`，超限返回 OOM |
| MPS 的限额路径与运行时接入 | NEW src.nvidia.mps-docs-2026-10-18＋NEW src.nvidia.k8s-device-plugin-mps-v0.20.1 | when-to-use-mps.html（Dynamic Execution Resource Provisioning/Static SM Partitioning）；[quick-start.html](https://docs.nvidia.com/deploy/mps/quick-start.html)（控制器/客户端 pipe 目录）；[mps.go@487d7a93](https://github.com/NVIDIA/k8s-device-plugin/blob/487d7a93894b0f3ad08097169593972eb3ca8206/internal/plugin/mps.go)（MIG 检查、daemon 健康、注入 `CUDA_MPS_PIPE_DIRECTORY`、挂载 pipe/shm）；[daemonset-mps-control-daemon.yml](https://github.com/NVIDIA/k8s-device-plugin/blob/487d7a93894b0f3ad08097169593972eb3ca8206/deployments/helm/nvidia-device-plugin/templates/daemonset-mps-control-daemon.yml)（配套 DaemonSet、mps-root hostPath、/dev/shm、nodeSelector） | 动态限额：`CUDA_MPS_ACTIVE_THREAD_PERCENTAGE`（uniform 在客户端启动时固定）与 `CUDA_MPS_PINNED_DEVICE_MEM_LIMIT`，限额非预留、内核仍可能共享 SM；静态 SM 分区：Ampere+、chunk 单位、context 前设 `CUDA_MPS_SM_PARTITION`、不与 locality domains 并用、静态模式忽略动态 provisioning；插件 v0.20.1 样板只采用动态限额 + Legacy v2，并通过配套 `mps-control-daemon` DaemonSet 管理生命周期；站点自管 daemon 是另一路径，须提供同等 pipe/shm 可达性。未覆盖：站点自管路径与实际部署验证 |
| device-plugin time slicing 的隔离边界 | NEW src.nvidia.k8s-device-plugin-sharing-v0.20.1 | [README.md@487d7a93](https://github.com/NVIDIA/k8s-device-plugin/blob/487d7a93894b0f3ad08097169593972eb3ca8206/README.md)（Shared Access to GPUs / With CUDA Time-Slicing 节） | time-slicing 只让工作负载交错执行，**不做任何隔离**：每个工作负载都能访问整块 GPU 显存、处于同一故障域（一个崩溃全部受影响）；replicas 只是访问名额（8 卡 × 10 replicas 上报 80），请求多于 1 不保证按比例算力；`failRequestsGreaterThanOne` 建议开启但默认 false；time-slicing 与 MPS 互斥，且同一节点只能统一配置、不能逐卡配置；支持资源为 `nvidia.com/gpu` 与 mixed MIG 资源名 |
| device-plugin MPS 的共享语义 | NEW src.nvidia.k8s-device-plugin-sharing-v0.20.1 | README 同节 With CUDA MPS | MPS 由控制 daemon 管理共享 GPU；每客户端显存被限制为总显存等分，算力也受限；**截至 v0.15.0 MPS 支持仍属 experimental**；**MIG 启用时设备不支持 MPS 共享**；仅支持整卡 `nvidia.com/gpu` |
| 容器默认设备暴露的注意点 | NEW src.nvidia.k8s-device-plugin-sharing-v0.20.1 | README（Running GPU Jobs 节 WARNING） | 若容器未声明 GPU 请求，插件会把机器上全部 GPU 暴露进容器——容器内可见设备数不等于已分配数，是租户可见性核对的常见反例 |
| Ascend 插件对虚拟设备（vNPU）的上报与健康口径 | NEW src.ascend.ascend-device-plugin-44385c13 | [component/ascend-device-plugin/README.md@44385c13](https://github.com/Ascend/mind-cluster/blob/44385c13d7b1d87def35f1604e8be4d16de6ca4e/component/ascend-device-plugin/README.md)（支持的产品形态/组件介绍节） | 设备发现支持「发现拆分物理设备得到的虚拟设备并上报 Kubernetes」；**虚拟设备健康状态由拆分它的物理设备决定**；支持产品含 Atlas 训练/A2/A3、300I/推理系列、800I A2。规格与隔离保证见下两行（HDK/vCANN-RT 文档） |
| Ascend HDK 虚拟化实例（静态/动态 vNPU） | NEW src.ascend.virtual-instance-hdk-44385c13 | [01_description.md](https://github.com/Ascend/mind-cluster/blob/44385c13d7b1d87def35f1604e8be4d16de6ca4e/docs/zh/scheduling/04_usage/02_virtual_instance/00_virtual_instance_with_hdk/01_description.md)（特性/产品支持/使用约束）；[03_virtualization_templates.md](https://github.com/Ascend/mind-cluster/blob/44385c13d7b1d87def35f1604e8be4d16de6ca4e/docs/zh/scheduling/04_usage/02_virtual_instance/00_virtual_instance_with_hdk/03_virtualization_templates.md)；[01_creating_vnpu.md](https://github.com/Ascend/mind-cluster/blob/44385c13d7b1d87def35f1604e8be4d16de6ca4e/docs/zh/scheduling/04_usage/02_virtual_instance/00_virtual_instance_with_hdk/04_static_vnpu_scheduling/01_creating_vnpu.md)；[02_mounting_vnpu_static.md](https://github.com/Ascend/mind-cluster/blob/44385c13d7b1d87def35f1604e8be4d16de6ca4e/docs/zh/scheduling/04_usage/02_virtual_instance/00_virtual_instance_with_hdk/04_static_vnpu_scheduling/02_mounting_vnpu_static.md)；[01_dynamic_vnpu_scheduling_inference.md](https://github.com/Ascend/mind-cluster/blob/44385c13d7b1d87def35f1604e8be4d16de6ca4e/docs/zh/scheduling/04_usage/02_virtual_instance/00_virtual_instance_with_hdk/05_dynamic_vnpu_scheduling/01_dynamic_vnpu_scheduling_inference.md) | 按 AICore/AICPU/内存/DVPP 切分；产品支持表与模板（如 Atlas 800T A2 24 AICore 的 vir06_1c_16g/vir12_3c_32g）；有限配套样板 MindCluster 26.1.0（tag v26.1.1）+CANN 9.1.0+HDK 分产品；静态创建（vnpu-mode/create-vnpu/vnpu-cfg-recover）、挂载须含 VIRTUAL、每 Pod 1 个、创建/销毁需重启 Device Plugin、不支持故障重调度；动态须**关闭恢复功能**、Docker 的 ASCEND_RUNTIME_OPTIONS **不能含 VIRTUAL**、仅 Volcano、同一时刻同一模板、每 Pod 1 个、不支持分布式任务、支持故障重调度；**所引集群推理场景同一集群不能同时存在静态与动态 vNPU 任务**、切换需删除已有任务、K8s/Docker 生命周期不混用；一个 vNPU 只给一个任务容器；虚拟化后物理 NPU 不可再挂容器/直通。未覆盖：虚拟化功能最低固件/CANN 版本、跨 vNPU 故障隔离/QoS |
| Ascend vCANN-RT 软切分 | NEW src.ascend.virtual-instance-vcann-44385c13 | [00_description.md](https://github.com/Ascend/mind-cluster/blob/44385c13d7b1d87def35f1604e8be4d16de6ca4e/docs/zh/scheduling/04_usage/02_virtual_instance/01_virtual_instance_with_vcann_rt/00_description.md) | 时分复用软切分；仅推理；一个容器一个 NPU；requests 为 AICore 百分比；A3 需单 die 直通；同一物理 NPU 上所有容器须相同策略；最大切分数建议不超过单 device 最大用户进程数；软切分后不可直通 VM。未覆盖：跨容器隔离/开销数据 |
| 容器内 vNPU 设备名重映射 | 复用 src.ascend.docker-runtime-44385c13 | 既有登记：`runtime/process/process.go` L86–L93；本轮审阅轮定位到 `getMountPath` L536–L549（vNPU 时 `vdavinciN` 在容器内重命名为 `davinciN`） | 支撑「容器内设备名与宿主机 `/dev` 名不一致属预期」；这是命名转换，不是隔离证据；本轮未重开该文件 |
| K8s 设备插件资源语义 | 复用 src.kubernetes.device-plugins-v1-32 | 既有登记：Register/ListAndWatch/Allocate、capacity/allocatable、健康上报 | 支撑「插件上报什么、容器能请求什么」；本轮未重开 |
| MIG 逻辑设备与物理设备不一一对应 | 复用 src.nvidia.mig-device-names-2026-10-08 | 既有登记：MIG Device Names 页（R570 驱动 H100 示例、8×A100 示例） | 支撑「一个物理 GPU 下挂多个 MIG UUID」的反例；本轮未重开 |
| NVIDIA device-plugin 实现侧分配与健康 | 复用 src.nvidia.k8s-device-plugin-v0.20.1 | 既有登记：server.go/health.go 等（Allocate、ListAndWatch、MIG GI/CI 过滤） | 支撑「共享副本/健康检查来自插件实现」；本轮只重开 README，未重开实现文件 |

## unknown 清单

1. Ascend vNPU：规格、模板、产品支持与分配约束已取得官方材料（HDK 静态/动态、vCANN-RT 软切分）；**仍未知的是跨 vNPU 的故障隔离与性能 QoS 保证、固件/CANN 最低版本矩阵、vCANN-RT 实际开销与最大切分数现场值**。不得把“资源切分 + 一个 vNPU 一个容器”推成故障隔离承诺，也不得用 GPU 机制类推。
2. MIG 的逐型号最低驱动交集与各机型完整 profile 组合表：本轮只采用 A100/A30（CUDA 11+R525≥525.53）与 B200（CUDA 12+R570≥570.133.20）作为有限样板；Deployment 页另列 H100/H200 为 CUDA 12+R450，该行与其它官方版本材料冲突，**不采用、保留未消歧**。完整 profile 组合仍未建立。
3. MPS 与 MIG 的互斥条件在插件层的实现细节：README 只写「MIG enabled 时 MPS sharing 不支持」；驱动侧另有 MIG 上可用 MPS 的说明（deployment-considerations），两者层级不同，不能合并为“驱动层一概禁止”。MPS 有限样板采用 A100-SXM4-40GB + CUDA 11 + R525（≥525.53）+ 插件 v0.20.1 前提（驱动 ~=384.81、toolkit ≥1.7.0、K8s ≥1.10）；**样板只采用动态限额 + Legacy MPS v2；静态 SM 分区与 MPS v3 不属于该样板**（驱动/工具支持 v3 不等于插件可任选 v3）。运行时接入：插件注入 `CUDA_MPS_PIPE_DIRECTORY` 并挂载 pipe/shm，daemon/server 生命周期由同 chart 的 `mps-control-daemon` DaemonSet 负责；站点自管 daemon 是另一路径。两条样板的容器 runtime 选路为“默认 `nvidia-container-runtime`”或“`RuntimeClass` name/handler `nvidia` + `runtimeClassName: nvidia`”二选一，同节点池不混用。MPS 功能自身的最低驱动/CUDA 版本、站点自管路径与实际部署仍 unknown。
4. device-plugin time-slicing/MPS 的实际争用与性能数据：README 只有语义与告警，无性能案例；不得编造数字。
5. Ascend 容器内设备 cgroup 的精确权限集合：本轮复用既有 docker-runtime 证据，未重开源码。
6. 站点实际配置（是否启用 MIG、replicas 数、MPS 静态分区、Ascend 虚拟化模式与模板）：unknown，须读现场。
7. 全部实测未做：未创建 MIG 实例、未启动 MPS server、未配置 time-slicing、未创建/挂载 vNPU、未运行 vCANN-RT 软切分。

## 建议登记条目

```yaml
- id: src.nvidia.mig-user-guide-2026-10-18
  title: NVIDIA MIG User Guide（Supported GPUs 与 Concepts；2026-10-18 观察）
  url: https://docs.nvidia.com/datacenter/tesla/mig-user-guide/
  kind: documentation
  registered_at: '2026-10-18'
  revision: 可变文档站（随驱动更新）；2026-10-18 经 FetchURL 实开 index、supported-gpus.html、concepts.html 三页；未固定驱动版本，引用按观察日期
  license:
    status: unknown
    scopes: []
    notes: NVIDIA 文档站许可未在打开页面中核对；只链接并原创归纳，未复制图表或长段。
  notes: Batch 23（T05-06）取证：supported-gpus（Ampere+、compute capability ≥8.0、A100/A30/H100/H200/H20/B200/GB200/GB300/RTX PRO Blackwell/Thor iGPU 与最大实例数）；concepts（memory slice≈1/8、SM slice≈1/7、GI/CI 语义、profile placement 与碎片、CUDA Concurrency Mechanisms 对照表：分区类型/最大分区/SM 隔离/显存保护/带宽 QoS/错误隔离/跨分区互操作/重配置）。未覆盖：最低驱动版本、supported profiles 全集、MIG 与 Kubernetes 专项页（该站 mig-kubernetes.html 本轮 404）。
- id: src.nvidia.mps-docs-2026-10-18
  title: NVIDIA Multi-Process Service 文档（Overview 与 When to Use MPS；2026-10-18 观察）
  url: https://docs.nvidia.com/deploy/mps/index.html
  kind: documentation
  registered_at: '2026-10-18'
  revision: 可变文档站；2026-10-18 经 FetchURL 实开 index.html 与 when-to-use-mps.html；文档区分 Legacy MPS v2 与 MPS v3，未绑定 CUDA 版本
  license:
    status: unknown
    scopes: []
    notes: NVIDIA 文档站许可未核对；只链接并原创归纳。
  notes: Batch 23（T05-06）取证：index（控制 daemon/server/client runtime、收益、文档结构）；when-to-use-mps（仅 Linux/QNX、单用户活动 server、不同用户激活被串行化、记账归属 server、EXCLUSIVE_PROCESS 建议、64 位/同 UID/dynamic parallelism 限制、地址空间隔离与有限错误遏制、FAULT 状态语义、动态资源限额非预留、60 client contexts 默认上限、设备显存上限与 OOM、静态 SM 分区与 chunk 规则、客户端提前终止未定义状态）。未覆盖：实际性能数据、驱动最低版本。
- id: src.nvidia.k8s-device-plugin-sharing-v0.20.1
  title: NVIDIA k8s-device-plugin v0.20.1 README — Shared Access to GPUs（time-slicing/MPS）
  url: https://github.com/NVIDIA/k8s-device-plugin/blob/487d7a93894b0f3ad08097169593972eb3ca8206/README.md
  kind: repository
  registered_at: '2026-10-18'
  revision: commit 487d7a93894b0f3ad08097169593972eb3ca8206（tag v0.20.1）；2026-10-18 经 FetchURL 读取 raw README 全文
  license:
    status: unknown
    scopes: []
    notes: 本轮未重开 LICENSE；沿用既有 src.nvidia.k8s-device-plugin-v0.20.1 的仓库口径（未核对），只链接并原创归纳。
  notes: Batch 23（T05-06）取证：Shared Access to GPUs（time-slicing 与 MPS 互斥、同节点统一配置不可逐卡）；time-slicing（不做隔离、共享显存与故障域、replicas 语义与 8×10=80 示例、请求 >1 不保证比例算力、failRequestsGreaterThanOne 默认 false、支持资源含 mixed MIG 资源名）；MPS（等分显存与算力限制、v0.15.0 起 experimental、MIG 启用时不支持、仅整卡）；Running GPU Jobs 的「未请求 GPU 会暴露全部 GPU」告警。未覆盖：实际争用/性能数据。
- id: src.ascend.ascend-device-plugin-44385c13
  title: Ascend Device Plugin（mind-cluster v26.1.1）组件 README
  url: https://github.com/Ascend/mind-cluster/blob/44385c13d7b1d87def35f1604e8be4d16de6ca4e/component/ascend-device-plugin/README.md
  kind: repository
  registered_at: '2026-10-18'
  revision: commit 44385c13d7b1d87def35f1604e8be4d16de6ca4e（annotated tag v26.1.1）；2026-10-18 经 FetchURL 读取 raw 全文
  license:
    status: partial
    scopes:
    - scope: 仓库根许可证（代码与组件文档）
      identifier: Apache-2.0
      url: https://github.com/Ascend/mind-cluster/blob/44385c13d7b1d87def35f1604e8be4d16de6ca4e/LICENSE
    notes: 沿用既有 src.ascend.mind-cluster-v26.1.1 在同 commit 已核对的仓库根许可口径，本轮未重开 LICENSE；只链接并原创归纳。
  notes: Batch 23（T05-06）取证：支持产品形态（Atlas 训练/A2/A3、300I/推理系列、800I A2）；组件介绍（设备发现含「拆分物理设备得到的虚拟设备」上报、健康检查「虚拟设备健康状态由物理设备决定」、设备分配与 NPU 重调度）。vNPU 规格/隔离/回收语义见下方 HDK 与 vCANN-RT 条目；跨 vNPU 故障隔离仍 unknown。
- id: src.nvidia.mig-deployment-considerations-2026-10-18
  title: NVIDIA MIG User Guide — Deployment Considerations（2026-10-18 观察）
  url: https://docs.nvidia.com/datacenter/tesla/mig-user-guide/deployment-considerations.html
  kind: documentation
  registered_at: '2026-10-18'
  revision: 可变页，页面标注 2026-10-13 更新；2026-10-18 经审阅轮实开；未固定驱动版本
  license:
    status: unknown
    scopes: []
    notes: NVIDIA 文档站许可未核对；只链接并原创归纳。
  notes: Batch 23（T05-06 审阅补充，作者采纳）：GPU/CUDA/驱动条件、Linux/容器边界，以及驱动层可在 MIG 上使用 MPS 的说明；用于区分“插件层不支持 MPS-on-MIG”与“驱动层一概禁止”。逐型号最低驱动交集仍未建立（unknown）。
- id: src.nvidia.a100-mem-error-recovery-2026-10-18
  title: NVIDIA GPU Memory Error Management — Error Recovery and Response Flags（2026-10-18 观察）
  url: https://docs.nvidia.com/deploy/a100-gpu-mem-error-mgmt/error-recovery-and-response-flags.html
  kind: documentation
  registered_at: '2026-10-18'
  revision: 可变页，页面标注 2026-09-09 更新；2026-10-18 经审阅轮实开；未固定驱动/机型
  license:
    status: unknown
    scopes: []
    notes: NVIDIA 文档站许可未核对；只链接并原创归纳。
  notes: Batch 23（T05-06 审阅补充，作者采纳）：恢复动作包含终止全部 GPU 进程后整卡 reset、OS reboot，以及部分 MIG 分区受损后的 drain-and-reset；作为“MIG 错误隔离不是任意错误都不外溢”的官方边界证据，不是本库故障注入结果。
- id: src.ascend.virtual-instance-hdk-44385c13
  title: MindCluster v26.1.1 虚拟化实例（HDK）文档（特性、模板、静态/动态 vNPU）
  url: https://github.com/Ascend/mind-cluster/blob/44385c13d7b1d87def35f1604e8be4d16de6ca4e/docs/zh/scheduling/04_usage/02_virtual_instance/00_virtual_instance_with_hdk/01_description.md
  kind: repository
  registered_at: '2026-10-18'
  revision: commit 44385c13d7b1d87def35f1604e8be4d16de6ca4e（annotated tag v26.1.1）；2026-10-18 经 FetchURL 实开 raw：01_description、03_virtualization_templates、04_static_vnpu_scheduling/01_creating_vnpu 与 02_mounting_vnpu_static、05_dynamic_vnpu_scheduling/01_dynamic_vnpu_scheduling_inference
  license:
    status: partial
    scopes:
    - scope: 固定 commit 的 docs 目录文档；第三方素材按各自声明核查
      identifier: CC-BY-4.0
      url: https://github.com/Ascend/mind-cluster/blob/44385c13d7b1d87def35f1604e8be4d16de6ca4e/docs/LICENSE
    notes: docs/LICENSE 由既有条目 src.ascend.mind-cluster-v26.1.1 在同 commit 核对，本轮未重开；只链接并原创归纳。
  notes: Batch 23（T05-06 修订）：HDK 虚拟化（产品支持表、模板、静态创建/挂载、动态调度、使用约束）。未覆盖：跨 vNPU 故障隔离与性能 QoS 保证、固件/CANN 最低版本矩阵。
- id: src.ascend.virtual-instance-vcann-44385c13
  title: MindCluster v26.1.1 vCANN-RT 软切分虚拟化文档（特性与软切分调度）
  url: https://github.com/Ascend/mind-cluster/blob/44385c13d7b1d87def35f1604e8be4d16de6ca4e/docs/zh/scheduling/04_usage/02_virtual_instance/01_virtual_instance_with_vcann_rt/00_description.md
  kind: repository
  registered_at: '2026-10-18'
  revision: commit 44385c13d7b1d87def35f1604e8be4d16de6ca4e（annotated tag v26.1.1）；2026-10-18 经 FetchURL 实开 raw 的 00_description
  license:
    status: partial
    scopes:
    - scope: 固定 commit 的 docs 目录文档；第三方素材按各自声明核查
      identifier: CC-BY-4.0
      url: https://github.com/Ascend/mind-cluster/blob/44385c13d7b1d87def35f1604e8be4d16de6ca4e/docs/LICENSE
    notes: 沿用既有条目在同 commit 的 docs/LICENSE 口径，本轮未重开；只链接并原创归纳。
  notes: Batch 23（T05-06 修订）：vCANN-RT 软切分（时分复用、仅推理、一个容器一个 NPU、requests 为 AICore 百分比、A3 单 die、同一物理 NPU 相同策略、最大切分数限制）。未覆盖：跨容器隔离/开销数据。
```
