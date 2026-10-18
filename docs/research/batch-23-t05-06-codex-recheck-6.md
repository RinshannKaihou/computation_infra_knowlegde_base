# Batch 23 · T05-06 第六轮定向复核

## 审阅元数据

- 任务：T05-06「加速器共享与租户隔离机制」；承接[第五轮定向复核](batch-23-t05-06-codex-recheck-5.md)，复核 C04（P1）、R06（P2）及本次修订引入的问题。
- 日期：2026-10-18，Asia/Shanghai（UTC+08:00）。
- 角色：沿用同一独立审阅者角色；本轮未参与作者修订，未派发子代理。角色连续性不认证历史各轮实际部署模型相同。
- 实际执行模型：`unknown`；实际 reasoning effort：`unknown`。本接口未暴露可核验的实际模型标识或 effort，不以仓库约定、报告文件名或历史记录代填；本报告不认证指定模型/effort 的执行合规性。
- 方法：重读第五轮关闭条件、相关历史判定、当前正文、来源记录及实际 registry；重新读取 NVIDIA 官方精确页面与插件固定 commit 的 README、MPS 分配实现、Helm 模板和 daemon 生命周期实现。作者摘要只用于定位，不作为关闭依据。
- 写入范围：仅新增本报告；不修改正文、来源记录、registry、历史报告、计划、状态或构建产物。本轮不是整个 Batch 23 的全面重审。

## 本地证据与快照

下文“正文”指 [accelerator-sharing-and-isolation.md](../../knowledge/05-cluster-platform/accelerator-sharing-and-isolation.md)；“来源记录”指 [batch-23-t05-06-sources.md](batch-23-t05-06-sources.md)。行号为本轮本地原文件坐标。

| 材料 | 本轮定位 |
|---|---|
| 正文（243 行） | `source_refs` L8–22，新增 ID 在 L12；MPS/time slicing L96–116；有限样板 L118–136，尤其 L126–127、L134–136；对照表 L140–147；运行时相关知识入口 L224 |
| 来源记录（143 行） | 限额与接入职责 L21；两种 sharing 的语义 L22–23；有限样板及 unknown L37 |
| [registry](../../sources/registry.yaml) | 既有 sharing 登记 L5724–5734；新增 `src.nvidia.k8s-device-plugin-mps-v0.20.1` 实际登记 L5824–5834，非建议登记区 |
| 既有关闭条件 | [第四轮](batch-23-t05-06-codex-recheck-4.md) L55–59；第五轮 L58–74（C04）、L82–88（R06） |
| [任务 acceptance](../../plans/full-coverage-backlog.yaml) | L5620–5625；本轮不变更任务状态 |

本地 Git HEAD 为 `1d07b62d676a51e9ae8725ce04f5d417e6182a74`；正文等 Batch 23 材料在开始时已有未提交/未跟踪改动，判定针对当前工作区，不把 HEAD 冒充作者修订提交。审阅材料 SHA-256 如下，仅标识本地快照，不认证上游网页字节：

| 材料 | SHA-256 |
|---|---|
| 正文 | `99672fbff8fc0d28dfb5119e6bd777578ac3378d8ad253bf8dbe81e03a044b3a` |
| 来源记录 | `1578650dc18a5e76a6627ceab998074d7069dd5bdd51d15352c80d67cf74edcc` |
| 第五轮报告 | `da8108696832fa4c5cef93a78a0f8d144ac10aec1333fab56c692bc2d831519e` |
| registry | `7934a260b4eff07f3b759f883147a2030f25afcd1ca1c5c2a4ccb7c8cf731d55` |

## 本轮上游证据

插件实现均固定于 `487d7a93894b0f3ad08097169593972eb3ca8206`。通过 GitHub 只读连接器重新核对原文件；不把网页转换后的行号用作 GitHub 源码锚点。NVIDIA 文档站为本轮读取的可变页面，不将其当前功能整体回填为 R525 的支持清单。

| 编号 | 精确来源与定位 | 支持范围与边界 |
|---|---|---|
| E01 | [README](https://github.com/NVIDIA/k8s-device-plugin/blob/487d7a93894b0f3ad08097169593972eb3ca8206/README.md)，Prerequisites、Preparing your GPU Nodes、DEVICE_LIST_STRATEGY、Shared Access to GPUs | 默认接入前提是已配置默认低层 `nvidia-container-runtime`；另有非默认 runtime 的 RuntimeClass 路径。`sharing.mps` / `sharing.timeSlicing` 是共享配置，不替代容器 runtime 选择。两种 sharing 互斥，MPS 只支持整卡资源；不证明任意站点已完成接入。 |
| E02 | [internal/plugin/mps.go](https://github.com/NVIDIA/k8s-device-plugin/blob/487d7a93894b0f3ad08097169593972eb3ca8206/internal/plugin/mps.go)，`getMPSOptions`、`waitForDaemon`、`updateReponse` | 按 MPS sharing 分支检查资源管理器中的 MIG 设备、检查 daemon 健康；分配响应注入 `CUDA_MPS_PIPE_DIRECTORY`，将宿主侧 pipe/shm 目录映射到容器。说明分配侧集成职责，不证明其负责配套服务全部生命周期。 |
| E03 | [daemonset-mps-control-daemon.yml](https://github.com/NVIDIA/k8s-device-plugin/blob/487d7a93894b0f3ad08097169593972eb3ca8206/deployments/helm/nvidia-device-plugin/templates/daemonset-mps-control-daemon.yml)，`runtimeClassName`、`mount-shm`、主容器、volumes、nodeSelector | 同 chart 的独立 DaemonSet/容器运行 `mps-control-daemon`，有共享内存初始化、`mps-root` hostPath 与 `/dev/shm` 挂载，并以 `nvidia.com/mps.capable=true` 选节点；模板还支持可选 RuntimeClass。模板存在不等于任意安装已启动服务，也不等于正文选定了某个 runtime 路径。 |
| E04 | [cmd/mps-control-daemon/main.go](https://github.com/NVIDIA/k8s-device-plugin/blob/487d7a93894b0f3ad08097169593972eb3ca8206/cmd/mps-control-daemon/main.go)，启动循环；[mps/daemon.go](https://github.com/NVIDIA/k8s-device-plugin/blob/487d7a93894b0f3ad08097169593972eb3ca8206/cmd/mps-control-daemon/mps/daemon.go)，`Start` / `Stop`、动态限额控制命令 | 配套程序调用 daemon 启停；启动参数为 `-d`，并设置默认显存与 active-thread 限额；该启动段不启用静态模式 `-S`。支持把所选原样集成限定在动态限额/Legacy v2 控制路径，不认证具体驱动组合。 |
| E05 | [When to Use MPS](https://docs.nvidia.com/deploy/mps/when-to-use-mps.html)，Dynamic Execution Resource Provisioning、Static SM Partitioning；[Quick Start](https://docs.nvidia.com/deploy/mps/quick-start.html)，控制器启动、隐式 server 启动、静态模式 | 动态限额不预留专属 SM；Legacy v2 静态模式须另行启用，静态分区与动态 provisioning 有不同条件。server 可以由活动 controller 随客户端启动而隐式启动，故“配套组件负责生命周期”不等于 DaemonSet 是直接执行每次 server 启动的单一进程。 |
| E06 | [v0.20.1 tag ref](https://api.github.com/repos/NVIDIA/k8s-device-plugin/git/ref/tags/v0.20.1) → [annotated tag 对象](https://api.github.com/repos/NVIDIA/k8s-device-plugin/git/tags/03296a61aeb9943906a1789f978ac3c87e13dfdd) | 本轮重新解引用为上述 commit；这是版本身份核对，不是签名认证、安装验证或硬件验证。 |

## 逐项判定

| 项目 | 本轮判定 | 依据与边界 |
|---|---|---|
| **B23-T06-C04 / P1** | **OPEN，剩余缺口已收窄** | 共享配置名称、MPS 配套接入及 IPC 映射、动态限额/静态分区/v3 的样板边界已补齐；仍未给两条有限样板明确选定默认 NVIDIA runtime 或非默认 RuntimeClass 接入路径。 |
| **B23-T06-R06 / P2** | **CLOSED** | 正文 L136、来源记录 L21/L37 已分清分配侧、配套 DaemonSet/程序、站点自管三个层级，并有 E02–E04 精确实现支撑；旧的笼统职责表述已删除。 |
| B23-T06-R05 / P1 | 保持 CLOSED（定向未见回归） | 正文 L126 与来源记录 L37 均明确排除插件样板使用 v3；通用概念不再被当作该样板能力。 |
| 新增来源登记与引用 | 本次同步有效 | 正文 `source_refs` 包含新增 ID；实际 registry 的 URL、commit 与 mps.go/Helm 模板说明一致；来源记录已引用两文件。许可证未核对、站点自管与实测未覆盖的边界保留。 |
| 本轮新增问题 | **无；不新增 B23-T06-R07** | 未发现本次修订引入的独立新问题；runtime 选路是第四、第五轮已明确的 C04 持续缺口，不重复编号。 |

### C04：已满足的部分

1. **MPS 的模式与容器内 IPC 接入已可核查。** 正文 L136 明确 `sharing.mps`，列出 daemon 健康、pipe 环境注入与 pipe/shm 挂载，并选择同 chart 配套 DaemonSet 路径；来源记录 L21/L37 同步。E02–E04 支持这些职责，不再是只有原生 Quick Start 或两个 namespace 中同名环境变量的示意。
2. **time slicing 的 sharing 模式与非 MPS 路线已明确。** 正文 L127 已写 `sharing.timeSlicing`、NVIDIA 容器运行时及不使用 MPS daemon；L110–114 保留目标资源、replicas 与互斥语义。此处有实质修订，不再判为“完全没有 runtime 或 sharing 内容”，也不要求它启动 MPS 服务。
3. **MPS 样板的功能边界已关闭。** 正文 L126 明确“动态限额 + Legacy MPS v2”，将静态 SM 分区与 v3 排除于该有限样板；来源记录 L21/L37 同步。L104、L135 与对照表 L144 的静态分区概念结合该排除条款阅读，不构成样板回归。E04/E05 支持分开说明；不要求删掉静态分区概念，也不推断 R525 一定不支持它。

### C04：尚未满足的唯一剩余条件

**MPS IPC 接入已经说明，但容器 runtime 的实际选路仍未落文。** 第五轮 L60、L70–74 延续的要求，是两条样板明确同用或分别采用哪条 NVIDIA 容器 runtime 接入，而不只是命名组件。

- 正文 L126 的前提仍只有驱动、toolkit 与 K8s 等条件；L136 新增的是 MPS daemon/IPC 路径，没有说明 `nvidia-container-runtime` 已配置为默认低层 runtime，或改用选定的非默认 RuntimeClass 路径。
- time slicing 的 L127 已增加“NVIDIA 容器运行时”，但仍未说明默认还是非默认接入。对正文与来源记录全文检索 `nvidia-container-runtime`、`RuntimeClass`、`runtimeClassName`、`containerd`、`CRI-O` 均无命中；结合完整样板段与来源记录 L21/L37 阅读，也未见用其他文字表达的默认/非默认选择。正文 L224 仍只是相关知识入口。
- E01 对上述两条接入有明确区别，E03 的 `runtimeClassName` 也是条件字段；不能由“采用同 chart”、挂载 pipe/shm、安装 toolkit 或链接 README，替作者推定其选择了哪个 runtime。这个缺口不是要求重做已完成的 IPC 说明，也不是新增安装脚本或现场验证门槛。

**最小关闭条件：**在正文中明确两条有限样板共同采用或分别采用的容器 runtime 选路，并在来源记录同步。例如选择 E01 的默认路径，就明确 NVIDIA runtime 已配置为默认低层 runtime，分别关联 `sharing.mps` / `sharing.timeSlicing`，保留当前 MPS 配套 IPC 与 time slicing 无 MPS daemon 的区别；若选择非默认路径，则明确所选 RuntimeClass 接入。二选一即可，不要求同时实现所有选项。已有机型/驱动/CUDA 取值、MPS 功能最低版本 unknown 和未实测边界无需因此重开。

### R06：关闭依据与职责层级

- **分配侧：**正文 L136 已改为检查 MIG/daemon、注入环境与挂载；E02 支持这些职责。“连接配套服务”按健康/控制交互及为客户端建立接入条件理解，不代表分配进程就是工作负载的 MPS server。
- **配套部署与程序：**正文明确同 chart 的独立 DaemonSet；E03/E04 支持部署、目录映射及 daemon 启停。结合 E05 的隐式 server 启动机制，当前“daemon/server 生命周期由配套组件负责”是组件管理层级的归纳，不是把 Kubernetes DaemonSet 对象、分配二进制、controller 和 server 合成一个进程。
- **站点自管：**正文明确是另一路径并要求同等 pipe/shm 可达性，来源记录保留该路径未覆盖；没有宣称站点手工启动是 v0.20.1 默认集成，也没有要求与配套 DaemonSet 重复启动服务。
- 对正文与来源记录检索旧的“只负责分配”“不负责启动”概括未见残留。R06 的责任边界关闭与 C04 的容器 runtime 选路缺口是不同判定，不互相替代。

## 结论

**C04（P1）仍 OPEN，但仅剩两条有限样板的容器 runtime 默认/非默认选路未明确；R06（P2）CLOSED；本轮无新增 R07；R05 保持 CLOSED。T05-06 本轮仍不能声明审阅通过。**

本轮认可新增固定源码证据、MPS 分配与配套生命周期职责、真实目录映射、两种 sharing 配置名称，以及动态限额/静态分区/v3 的范围修订。不能将这些已经完成的修订说成不存在；也不能把 MPS 的 pipe/shm 接入当作前轮要求的 NVIDIA 容器 runtime 选路已经闭合。此前其他已关闭项未全面重审，本结论不外推为整个 Batch 23 的判定。

## 证据边界与检查

- 本轮只读核对本地文档与官方文档/固定源码；未安装或启动驱动、Toolkit、插件、MPS、MIG/vNPU，未连接集群、变更共享模式、运行 GPU/NPU 负载或故障注入。源码存在、版本身份及结构检查不证明现场接入、限额、隔离、QoS、性能或回收已生效。
- 未重新认证 A100/CUDA 11/R525 等全部兼容交集；沿用前轮已认可的有限组件依据，不把 MIG 部署条件当作 MPS 功能认证，不把当前可变 MPS 页面当作历史功能支持矩阵。站点自管 daemon 仍非本次已验证路径。
- `PYTHONDONTWRITEBYTECODE=1 make check`：**PASS，100 content entries / 470 sources**。只检查结构与本地链接，不检查技术语义、远程内容、审阅结论或硬件组合。
- 未运行 `make build`：该命令会写 `build/catalog.json` 与 `build/catalog.md`，违反本轮仅新增指定报告的限制。未修改 `src/kb/`，未运行单元测试。
- 开始时已有正文、registry、领域索引及其他 Batch 23 工作区改动，均不归为本轮写入；本轮仅创建本报告，未代改问题状态、计划或历史元数据。
- 实际模型与 effort 均为 `unknown`；内容判断、执行模型认证和真实环境验证分别记录，互不替代。
