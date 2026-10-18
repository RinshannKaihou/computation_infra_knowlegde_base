# Batch 23 · T05-06 第五轮定向复核

## 审阅元数据

- 任务：T05-06「加速器共享与租户隔离机制」；承接[第四轮定向复核](batch-23-t05-06-codex-recheck-4.md)，只复核 C04 的剩余关闭条件、time-slicing 样板是否回归及本次修订引入的问题。
- 日期：2026-10-18，Asia/Shanghai（UTC+08:00）。
- 角色：沿用同一独立审阅者角色；本轮未参与作者修订，未派发子代理。角色连续性不认证历史各轮的实际部署模型相同。
- 实际执行模型：`unknown`；实际 reasoning effort：`unknown`。接口未暴露可核验的实际模型标识或 effort；不能以仓库约定、文件名或历史报告代替实际证明，也不认证本轮满足指定模型/effort 的执行约定。
- 方法：重新读取正文、来源记录、registry 相关条目、原 C04、第四轮剩余关闭条件及任务 acceptance；重新打开精确 NVIDIA 页面及插件固定 commit 的 README、daemon、分配响应和配套部署源码。作者修订摘要仅作定位，不作关闭证据。
- 写入限制：仅新增本报告；不修改正文、registry、来源记录、plans、历史报告或构建产物。本轮是内容定向复核，不是整个 Batch 23 的全面重审或硬件验证。

## 本地证据与快照

下文“正文”指 [accelerator-sharing-and-isolation.md](../../knowledge/05-cluster-platform/accelerator-sharing-and-isolation.md)；“来源记录”指 [batch-23-t05-06-sources.md](batch-23-t05-06-sources.md)。行号为本轮本地原文件坐标。

| 材料 | 本轮定位 |
|---|---|
| 正文（242 行） | MPS L95–105；time slicing L107–115；有限样板 L117–129，尤其 L125–126；新增三条路径 L131–135；对照表 L143；选择与验证 L181–208；运行时基线链接 L223 |
| 来源记录（143 行） | 新增“限额路径与运行时接入”行 L21；插件共享语义 L22–23；样板及 unknown L35–39 |
| [registry](../../sources/registry.yaml) | MPS 文档登记 L5713–5723，插件共享登记 L5724–5734；不是来源记录末尾的建议登记区 |
| 既有验收 | [初审 C04](batch-23-t05-06-codex-review.md) L56；[第四轮最小剩余关闭条件](batch-23-t05-06-codex-recheck-4.md) L59；[任务 acceptance](../../plans/full-coverage-backlog.yaml) L5620–5625 |

审阅快照 SHA-256（只标识本地材料，不认证上游网页字节）：

- 正文：`e9d406b254e20d7136ff9af75ecb5bf2a48cc37ab47e8034fecf71c13cb30406`。
- 来源记录：`8acf5b8d3ef630c204bddb4c216284fdd2ba2e28371bd7d53fc3585e56bb444b`。
- registry：`a336ce6edc17521e79c164d254c2fb272dde9cb60aea8b978ac5018262cce62c`。

## 本轮上游证据

均为本轮重新读取的官方材料。NVIDIA 文档站为可变页面；以下当前机制说明不能整体回填成 R525 的功能清单。插件源码固定于 `487d7a93894b0f3ad08097169593972eb3ca8206`，沿用前轮已解引用的 v0.20.1 身份；涉及源码行号的定位以连接器读取的原文件为准，不采用网页转换行号。

| 编号 | 精确页面 / 文件 | 支持范围与边界 |
|---|---|---|
| E01 | [When to Use MPS](https://docs.nvidia.com/deploy/mps/when-to-use-mps.html)，Dynamic Execution Resource Provisioning、MPS Device Memory Limit、Static SM Partitioning | uniform 限额在客户端启动时固定；动态限额不是专属资源预留，客户端内核仍可能共享 SM。静态分区为 Ampere+、按 chunk；Legacy v2 须在 daemon 启动时另用 `-S`，context 前设 `CUDA_MPS_SM_PARTITION`；与 locality domains 互斥、忽略动态 execution provisioning。Hopper+ dGPU 为 8 SM/chunk；这些说明不证明本样板 R525 支持静态分区 |
| E02 | [Quick Start](https://docs.nvidia.com/deploy/mps/quick-start.html)，Starting the MPS controller、Starting multiple MPS servers、Enabling static SM partitioning | 支持原生 MPS 控制器/客户端的 pipe 选择与启动模式区别；不是 k8s-device-plugin 的容器 runtime 或自动化集成说明 |
| E03 | [Appendix: Environment Variables](https://docs.nvidia.com/deploy/mps/appendix-environment-variables.html)，`CUDA_MPS_PIPE_DIRECTORY` / `CUDA_MPS_LOG_DIRECTORY` | pipe 对应 IPC；log 目录配置在 control daemon 环境、由 server 继承。Quick Start 的客户端示例同时带两变量，不能据此把 log 变量提升为所有客户端的连接必要条件 |
| E04 | [README](https://github.com/NVIDIA/k8s-device-plugin/blob/487d7a93894b0f3ad08097169593972eb3ca8206/README.md#L70)，Prerequisites / Preparing your GPU Nodes；[Shared Access](https://github.com/NVIDIA/k8s-device-plugin/blob/487d7a93894b0f3ad08097169593972eb3ca8206/README.md#L358) | 原文件 L70–115 指向默认 `nvidia-container-runtime` 或非默认时定义 RuntimeClass 的接入选择；L358 起区分 `sharing.timeSlicing`、`sharing.mps`。支持节点级互斥、replica 访问名额及 time-slicing 无隔离的机制，不证明容器仅安装 toolkit 就已接入 |
| E05 | [cmd/mps-control-daemon/mps/daemon.go](https://github.com/NVIDIA/k8s-device-plugin/blob/487d7a93894b0f3ad08097169593972eb3ca8206/cmd/mps-control-daemon/mps/daemon.go#L84)，`EnvVars` / `Start`，L84–129 | 配套程序启动 control daemon 使用 `-d`，设置 device-pinned-memory 和 active-thread-percentage 默认限额；该启动段没有静态模式 `-S`。支持原样集成属于动态限额路径，不支持静态分区已随之开启 |
| E06 | [internal/plugin/mps.go](https://github.com/NVIDIA/k8s-device-plugin/blob/487d7a93894b0f3ad08097169593972eb3ca8206/internal/plugin/mps.go#L61)，`waitForDaemon` / `updateReponse`，L61–91 | 分配侧检查 daemon 健康、向响应加入 pipe 环境变量，并映射宿主侧 pipe 与共享内存目录；不能把容器接入简化为两个 namespace 中环境变量字符串相同 |
| E07 | [daemonset-mps-control-daemon.yml](https://github.com/NVIDIA/k8s-device-plugin/blob/487d7a93894b0f3ad08097169593972eb3ca8206/deployments/helm/nvidia-device-plugin/templates/daemonset-mps-control-daemon.yml)，L158–220；[main.go](https://github.com/NVIDIA/k8s-device-plugin/blob/487d7a93894b0f3ad08097169593972eb3ca8206/cmd/mps-control-daemon/main.go#L210)，L210–222 | 同一发行物含独立 MPS DaemonSet/程序，带目录挂载、节点选择条件并调用 `mpsDaemon.Start()`。证明存在配套生命周期实现，不证明任意安装方式默认已部署、站点已经运行或可以重复启动另一套 daemon |
| E08 | [Supported GPUs](https://docs.nvidia.com/datacenter/tesla/mig-user-guide/supported-gpus.html)，A100-SXM4 40GB 行；[Deployment Considerations](https://docs.nvidia.com/datacenter/tesla/mig-user-guide/deployment-considerations.html)，A100/A30 行；[CUDA Minor Version Compatibility](https://docs.nvidia.com/deploy/cuda-compatibility/minor-version-compatibility.html)，Table 1 | 产品身份及 A100/CUDA 11/R525≥525.53 的既有组件依据仍可定位；较新驱动的向后兼容不等于完整共享模式认证。MIG 条件表不能单独证明 MPS/time-slicing 集成 |

## 逐项判定

| 项目 | 判定 | 依据与边界 |
|---|---|---|
| **B23-T06-C04 / P1** | **OPEN，部分修复** | 已新增三条机制说明，但两条有限样板仍未绑定容器 runtime 接入；MPS 行仍未明确仅采用动态限额、静态分区不在本样板。第四轮 L59 的两个剩余要求未全部满足 |
| 动态限额机制 | 本次补充可核查 | 正文 L133、来源记录 L21 与 E01 一致；不能把通用 MPS 的默认全部线程，误当成插件按 replicas 配置后的默认份额；插件实际设置限额见 E05 |
| 静态分区机制 | 概念分支可核查；样板范围未闭合 | L134 的代际、chunk、context 前环境变量及互斥说明有 E01；但列出独立 bullet 不等于明确排除其属于 L125 的样板 |
| MPS 运行时接入 | 原生 MPS 提示有效；插件/容器接入仍不完整 | L135 补了 daemon 和 pipe 的通用关系；E02 不提供 NVIDIA OCI runtime 接入，E06/E07 也表明还应分清分配接口、配套服务与目录映射 |
| time-slicing 样板 | 原机制与组件依据保留；完整接入样板仍未成立 | L109–115、L126 未引入 MPS 静态分区依赖或隔离承诺；但它与 MPS 共用的容器 runtime 缺口没有因新增 MPS 段而解决，仍计入 C04 |
| B23-T06-R05 / P1 | 保持 CLOSED（本次定向未见回归） | L125、来源记录 L37 仍明确排除把驱动/工具 v3 能力视作插件可任选接口；不全面重审此前已关闭项 |
| 本轮新增 | **B23-T06-R06 / P2，OPEN** | 新增“设备插件只负责分配 GPU”的未限定责任概括应收窄；详见下文。它不替代或重复编号 C04 的样板绑定缺口 |

### C04：仍缺哪些内容

**1. 原生 MPS 客户端接入不等于 Kubernetes 容器 runtime 接入。**

正文 L135 已有有用的 daemon/pipe 提示，不能再说“完全没有运行时内容”。但第四轮要求的是为 L125、L126 指定容器侧采用哪条 NVIDIA runtime 路径，并关联各自插件共享模式。对正文全文检索 `nvidia-container-runtime`、`RuntimeClass`、`runtimeClassName`、`containerd`、`CRI-O`、`sharing.mps`、`sharing.timeSlicing` 均无命中；L223 仍只是相关知识入口，不是两行样板的条件绑定。E04 给出可核对的路径选择，E06 显示 pipe 环境与真实目录映射也不能混为一谈。要求作者明确选路，不要求新增安装脚本或实际部署。

**2. 两类限额已经分列，但没有明确“哪一类属于所选样板”。**

L131 的标题和 L133–134 正确区分了两种机制；本轮认可这部分进展。可是 L125 的功能范围仍只有“整卡共享”，L143 仍概括“百分比或静态分区（可选）”；新增文字未写明 A100/R525/v0.20.1 样板只采用 E05 的动态限额、静态分区另属未建立版本/插件交集的概念分支。E01 的 Legacy v2 静态模式需额外启用，E05 原样启动没有 `-S`，所以“v2 + Ampere + 整卡”仍不足以区分二者。此项是第四轮已有关闭条件，不是新要求证明 R525 的历史静态分区能力。

**3. 来源同步有所增加，但没有补出上述两条绑定。**

来源记录 L21 已同步通用机制，并诚实声明未覆盖 v0.20.1 自动化接入；这个 unknown 本身不是错误。不过 L37 的有限样板没有补 runtime 选择或排除静态分区，不能用通用 Quick Start 加自动化 unknown 代替所选插件路径的有限说明。也不要求作者必须提供“自动化实现”才能关闭：可以引用 E05–E07 说明所选原样集成，保留站点执行验证 unknown。

**C04 最小剩余关闭条件（延续第四轮）：**

- 给 MPS 与 time-slicing 两条样板明确同用或分别采用的 NVIDIA 容器 runtime 接入路径，并分别关联 `sharing.mps` / `sharing.timeSlicing` 及目标资源；不要求同时实现所有 runtime 选项。
- 把 MPS 样板范围明确限定为所引插件实现的动态显存/active-thread 限额；静态 SM 分区与 v3 均不属于该有限样板。静态分区概念可以保留，不需要删去，也不能顺势宣称 R525 一定不支持它。
- 将所选 MPS 接入方式写清是配套 daemon 路径还是独立站点管理路径；说明 IPC 目录实际可达/映射，而不是只给同名环境变量。正文与来源记录同步，不以现场验证计划替代条件说明。

### time slicing：保留什么，不能宣称什么

E04 仍支持节点级 replicas、与 MPS 互斥、没有显存/故障隔离且请求更多名额不保证比例算力的既有语义。E08 没有给出推翻 L126 既有产品/组件取值的新依据；CUDA 11 与 R525 也不能因为 minor-version 表的 `<525` 就判为不兼容，该表明确保留更新驱动的向后兼容。

因此，**其机制说明和有限组件依据仍成立，未被本次 MPS 修订破坏；若“样板成立”指一个已经写清运行时接入的插件共享样板，则仍未闭合**。缺口属于 C04，不新增 time-slicing 问题，不要求 time slicing 启动 MPS daemon，也不新增硬件实测作为内容关闭门槛。

### 新增 B23-T06-R06：接入责任概括缺少层级限定

- **优先级 / 状态：P2 / OPEN。**
- **位置：**正文 L135“设备插件只负责分配 GPU，**不负责启动 MPS server**”；来源记录 L21 的对应概括。
- **问题：**“分配二进制本身不直接启动 MPS daemon/server”这个狭义区别可以成立，不能把配套 `mps-control-daemon` 冒充为同一个进程；但正文没有这一层级限定，反而以“只负责分配”概括整个 v0.20.1 插件接入，并紧接宿主机启动的写法。E06 表明分配侧还负责 pipe 环境注入和 pipe/共享内存挂载；E07 表明同一发行物另有配套 daemon 生命周期实现。因此该表述会模糊“单独插件进程”“配套发行/部署组件”“站点自管 daemon”的责任边界，不能据此推导必须由站点另行手工启动一套宿主机服务。
- **影响：**可能让读者遗漏既有配套组件或误配目录映射；重复启动、连接错控制器只是需防范的风险，本轮未观察到站点发生此类故障。不以此声称所有 Helm 安装都自动启动可用 MPS 服务。
- **关闭条件：**收窄成明确的组件职责：分配进程检查/连接配套服务并注入所需环境和挂载，daemon/server 生命周期由另一个配套程序或明确选定的站点机制负责；若保留手工宿主机示意，将其标成独立站点路径，不等同于 v0.20.1 默认/原样集成。同步来源记录并引用精确实现；不要求本轮实际部署。
- **不另报：**Quick Start 的客户端示例可同时设置 pipe/log，作为示例不能直接判错；E03 仅提醒不能将客户端同设 log 变量写成普遍连接必要条件。本轮不再为此新增 R07，也不将一般性简写升级成 P1。

## 结论

**C04（P1）仍 OPEN；新增 R06（P2）OPEN；R05 保持 CLOSED。T05-06 本轮仍不可声明审阅通过。**

有效修订是动态限额、静态分区及原生 MPS 接入已经分条且有精确来源。未完成的是把这些概念绑定回所选插件有限样板，并将容器 runtime 与 MPS IPC 接入分开说明。time-slicing 的机制没有回归，但它原有的 runtime 条件缺口也没有被 MPS 段补齐。此前其他已关闭项不作全面重审，不能由本结论推出全部历史问题重新开放或整个 Batch 23 均未通过。

## 证据边界与检查

- 本轮只核对文档和固定源码。MIG 部署条件不是 MPS 功能支持表；CUDA 向后兼容、源码存在和组件分工都不证明任意 OS、CUDA 小版本、驱动、插件、runtime 的完整兼容，也不证明现场限额已生效。
- 未安装或启动驱动、Toolkit、插件、MPS、MIG/vNPU；未连接集群、修改共享模式或协议、提交 GPU/NPU 负载、执行故障注入。上游命令只读，文档不产生新执行授权；不认证隔离、QoS、回收或性能。
- `PYTHONDONTWRITEBYTECODE=1 make check`：**PASS，100 content entries / 469 sources**。仅验证结构与本地链接，不验证技术语义、远程内容、报告结论或真实组合。
- 未运行 `make build`：它会写 `build/catalog.json`、`build/catalog.md`，违反本轮仅新增指定报告的限制。未修改 `src/kb/`，未运行单元测试；未改登记、问题状态、计划或历史元数据。
- 开始时正文、registry、领域索引及其他 Batch 23 文件已有工作区改动，均不归为本轮写入；本轮只新增本报告。复核新增的上游实现证据仅记录于本报告，未绕过写入限制追加 registry。
- 实际模型/effort 继续为 unknown；内容结论、执行模型认证、真实硬件验证分别记录，互不替代。
