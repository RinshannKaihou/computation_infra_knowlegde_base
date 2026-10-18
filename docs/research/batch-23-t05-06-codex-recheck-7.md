# Batch 23 · T05-06 第七轮定向复核

## 审阅元数据

- 任务：T05-06「加速器共享与租户隔离机制」；承接[第六轮定向复核](batch-23-t05-06-codex-recheck-6.md)，只复核 C04（P1）的最后一个 runtime 选路缺口，以及本次增补是否引入回归或独立新问题。
- 日期：2026-10-18，Asia/Shanghai（UTC+08:00）。
- 角色：沿用同一独立审阅者角色；本轮未参与作者修订，未派发子代理。角色连续性不等于能够认证历史各轮部署模型相同。
- 实际执行模型：`unknown`；实际 reasoning effort：`unknown`。本接口没有暴露可核验的实际模型标识或 effort；不以仓库约定、历史报告或文件名代填，也不据此认证指定模型/effort 的执行合规性。
- 方法：重新读取上一轮关闭条件、当前正文与来源记录的相关完整段落、实际 registry；只读重开插件固定 commit 的 README 与两份 Helm DaemonSet 模板。作者摘要仅用于定位，不作为关闭证据。
- 写入范围：仅新增本报告；不修改正文、来源记录、registry、历史报告、计划、状态或构建产物。不作整个 Batch 23 的全面重审。

## 本地证据与快照

下文“正文”指 [accelerator-sharing-and-isolation.md](../../knowledge/05-cluster-platform/accelerator-sharing-and-isolation.md)；“来源记录”指 [batch-23-t05-06-sources.md](batch-23-t05-06-sources.md)。行号均为本轮工作区原文件坐标。

| 材料 | 本轮定位与用途 |
|---|---|
| 正文（244 行） | L8–22 的来源引用；L106、L114 的 sharing 约束；L126–127 的 MPS/time slicing 两条有限样板；L132–137 的限额、IPC 与新增 runtime 选路，尤其 L137 |
| 来源记录（143 行） | L9 的固定版本；L21–23 的 MPS 接入与 sharing 语义；L37（unknown #3）的同步选路及未实测边界 |
| 第六轮报告 | L50 的 C04 OPEN 判定，L62–71 的唯一剩余缺口与最小关闭条件；R05/R06 的既有 CLOSED 判定 |
| [registry](../../sources/registry.yaml) | L5237 起的 `src.nvidia.k8s-device-plugin-v0.20.1`、L5724 起的 sharing 条目、L5824 起的 MPS 实现/配套部署条目；所用 NVIDIA 文件与既有登记的固定 commit 一致 |

本地 Git HEAD：`1d07b62d676a51e9ae8725ce04f5d417e6182a74`。正文等 Batch 23 材料在开始时已有未提交/未跟踪改动；本轮判定针对工作区快照，不把 HEAD 当成作者修订提交。以下 SHA-256 只标识本地材料，不认证上游网页字节：

| 材料 | SHA-256 |
|---|---|
| 正文 | `8c3a42938fa15fde1777a3ca1c0d98bb010a86697eeeff66dfa5906a581021c1` |
| 来源记录 | `9a3af9b713554e4da439647c59c0d6233f3cc92478bcb54b27d3bcee5fee4e42` |
| 第六轮报告 | `906d084a98edb4721d090d04d60b84ea0cc38e2484afd0bdc5050240105edb07` |
| registry | `7934a260b4eff07f3b759f883147a2030f25afcd1ca1c5c2a4ccb7c8cf731d55` |

## 本轮上游证据

以下插件文件均固定于 commit `487d7a93894b0f3ad08097169593972eb3ca8206`，不沿 README 内其他示例版本的链接替换所审实现。README 经 raw 页面与 GitHub 只读连接器核对；模板同时核对原文件片段。源码位置采用连接器原文件坐标，未将网页转换行号拼作 GitHub 锚点。

| 编号 | 精确来源与定位 | 支持范围 |
|---|---|---|
| E01 | [README.md](https://github.com/NVIDIA/k8s-device-plugin/blob/487d7a93894b0f3ad08097169593972eb3ca8206/README.md)：Prerequisites、Preparing your GPU Nodes、Setting other helm chart values、Shared Access to GPUs | 默认路径以前置配置 NVIDIA runtime 为条件；未设为默认时给出 name/handler 均为 `nvidia` 的 RuntimeClass 示例，并提供 chart 的 `runtimeClassName` 选项。共享配置另分 time-slicing/MPS，二者互斥且同节点不可逐卡配置。 |
| E02 | [daemonset-device-plugin.yml](https://github.com/NVIDIA/k8s-device-plugin/blob/487d7a93894b0f3ad08097169593972eb3ca8206/deployments/helm/nvidia-device-plugin/templates/daemonset-device-plugin.yml)，L51–53 | Device Plugin 的 Pod 模板在 chart 指定 `runtimeClassName` 时写入该字段；非默认接入不能被理解为只给业务 Pod 选路而让插件 Pod 遗漏。 |
| E03 | [daemonset-mps-control-daemon.yml](https://github.com/NVIDIA/k8s-device-plugin/blob/487d7a93894b0f3ad08097169593972eb3ca8206/deployments/helm/nvidia-device-plugin/templates/daemonset-mps-control-daemon.yml)，L51–53 | 同 chart 的 MPS 配套 Pod 使用同一 `runtimeClassName` 值；支持在非默认路径下保持插件、配套 daemon 与相关工作负载的接入一致。模板存在不证明现场已经设置该值。 |

## 逐项判定

| 项目 | 本轮判定 | 依据与边界 |
|---|---|---|
| **B23-T06-C04 / P1** | **CLOSED** | 正文 L137 已明确默认 NVIDIA runtime 与非默认 RuntimeClass 的二选一路径，并约束同一节点池统一选择；来源记录 L37 同步。第六轮所列唯一剩余关闭条件已满足。 |
| 默认 runtime 路径与 README 一致性 | 满足 | 明确把 `nvidia-container-runtime` 配置为节点默认低层运行时，而不只是安装 Toolkit 或泛称“NVIDIA 容器运行时”；此路径不要求额外使用 RuntimeClass，与 E01 的默认接入前提一致。 |
| 非默认 RuntimeClass 路径与 README 一致性 | 满足 | 保留其他默认运行时，用 name/handler 均为 `nvidia` 的 RuntimeClass，并在 Pod 中指定 `runtimeClassName: nvidia`；与 E01 的示例及 E02/E03 的字段传递一致。这里是选择已配置的 NVIDIA runtime，不是创建一个 RuntimeClass 就会自动安装或注册节点 handler。 |
| MPS 与 time slicing 两条有限样板覆盖 | 同时覆盖 | L137 的“两条样板”结合 L126–127 的两条 sharing 样板与来源记录 L37 阅读，是共用的容器 runtime 约束；并非要求 MPS 与 time slicing 同时启用，也不是给静态 SM 分区/v3 扩展样板。 |
| 避免选路及共享模式混用 | 满足 | L137 明文要求同一节点池二选一且不混用；L114/L127 仍保留 MPS 与 time slicing 的互斥。runtime 路径的一致性策略与 sharing 模式互斥是两个层级，没有互相替代。 |
| 来源记录 unknown #3 | 同步有效 | L37 与正文的两个分支、类名/handler、Pod 字段及同池不混用一致；MPS 功能最低版本、站点自管与实际部署仍保留 unknown，没有因补齐选路冒充已实测。 |
| R05 / P1、R06 / P2 | 保持 CLOSED（定向未见回归） | L126 仍限动态限额与 Legacy MPS v2；L136 与来源记录 L21/L37 仍区分分配侧、配套 daemon 生命周期和站点自管路径。新增容器 runtime 选路未撤回这些边界。 |
| 本轮新增问题 | **无；不新增 B23-T06-R07** | 本次增补未发现需要独立编号的新错误或回归；不把已有现场验证 unknown 改记成新缺陷，也不以新增安装脚本作为本轮关闭门槛。 |

### C04 关闭理由与解释边界

1. **从泛称组件落实为可区分的接入分支。** 上轮缺的是默认/非默认的落文，而不是再次描述 MPS IPC。L137 已分别给出默认 NVIDIA runtime 与非默认 `nvidia` RuntimeClass，并说明 Pod 如何选用，直接满足 E01 所区分的路径。保留两个明确的可选分支、要求实施时同池统一选择，不等于继续把选路留作 unknown；本页是有限概念样板，不是某现场的已部署清单。
2. **两种 sharing 共用 runtime 层要求，不共享 MPS 特有服务。** MPS 仍采用 L136 的 `sharing.mps`、配套 daemon 与 pipe/shm 接入；time slicing 仍采用 L127 的 `sharing.timeSlicing` 且不使用 MPS daemon。L137 仅补这两条样板都需要的容器接入，不能读成 time slicing 也要启动 MPS 服务。L132/L134–135 的动态/静态限额介绍不是本轮“两条 sharing 样板”的替代对象；L126 仍明确静态分区不在该插件样板内。
3. **同池不混用是本文选定的实施约束，不冒充上游 API 禁令。** E01 支持默认/非默认路径，但不能据此声称 Kubernetes 技术上禁止默认 runtime 与显式 RuntimeClass 共存。本文要求同池统一，比“API 是否允许”更窄；这一约束合理且不与 README 冲突。真正由 README 明确互斥的是 MPS 与 time-slicing 两种 sharing 模式。
4. **非默认路径的前置配置和适用范围没有被豁免。** E01 的节点 runtime 配置在创建 RuntimeClass 之前；E02/E03 说明 chart 的选路还要传到插件及 MPS 配套 Pod。正文的“Pod 使用”按相关 Pod 的共同约束理解，而非只针对业务 Pod 的例外。实际节点 handler、chart 渲染结果与工作负载字段仍须现场核实；README 的插件最低 Kubernetes 版本也不能单独当作所有 RuntimeClass/CRI 组合的兼容认证。本轮不要求新增容器引擎安装脚本或现场部署记录。

## 结论

**C04（P1）CLOSED；本轮无新增问题，不新增 B23-T06-R07；R05/R06 在本次定向范围内保持 CLOSED。** 新增选路与固定版本 README 一致，同时覆盖 MPS/time slicing 两条有限样板，并明确同一节点池不混用。

按第六轮“仅 C04 OPEN”的问题账承接，本轮最后一个开放项已关闭，**T05-06 在既有审阅范围及本次定向复核范围内通过**。这不是对整篇重新初审，也不是整个 Batch 23 通过；此前其他 CLOSED 项不声称本轮全部重验。仅在本报告记录判定，不代改任务状态或正文的 `draft / source_checked`。

## 证据边界与检查

- 本轮仅核对本地文档和官方固定源码；未连接集群、安装/配置/重启 runtime，未创建 RuntimeClass、部署插件或 daemon，未运行 GPU/NPU 工作负载、切换 sharing 模式或做故障注入。文中配置名称与上游一致，不证明设备已注入、IPC 可达、限额/隔离/QoS 生效。
- 不重新认证全部机型/驱动/CUDA/Kubernetes/CRI/Toolkit 交集；MPS 最低版本、站点自管路径及现场实测边界继续保留。未重开许可证，未复制大段上游材料；未新增或修改 registry 条目。
- `PYTHONDONTWRITEBYTECODE=1 make check`：**PASS，100 content entries / 470 sources**。仅验证结构与本地文件链接，不验证远程页面、技术判断、runtime 接入或硬件组合。
- 不运行 `make build`：该命令会写 `build/catalog.json` 与 `build/catalog.md`，违反本轮仅创建指定报告的限制。未修改 `src/kb/`，不运行内容无关的单元测试。
- 开始时已有其他工作区改动，不归为本轮写入；使用排除本报告的 Git 已跟踪/未忽略未跟踪文件 SHA-256 汇总核对写入边界，不更改历史材料。
- 实际模型/effort 的可核验性、内容审阅判定与硬件验证分别记录；`unknown / unknown` 不得改写为仓库约定模型已获认证，审阅通过也不升级为真实环境验证通过。
