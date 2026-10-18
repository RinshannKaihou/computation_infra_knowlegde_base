# Batch 23 · T05-06 独立技术审阅（初审）

## 审阅元数据

- 任务：T05-06「加速器共享与租户隔离机制」，concept；以 `plans/full-coverage-backlog.yaml` 的五条 acceptance 和本次用户要求为准。
- 实际执行模型：`gpt-6.1-sol / xhigh`，本地 Codex CLI 0.157.1。本会话 rollout 的 `turn_context.model`、`effort` 及协作配置均已只读核验；模型/档位集合仅为 `gpt-6.1-sol / xhigh`。未派发子代理、未调用其他模型执行审阅。
- 时间：2026-10-18，Asia/Shanghai（UTC+08:00）；取证开始约 16:25，报告编写约 16:34。
- 轮次：初审；角色为独立技术审阅者，不是正文作者。本报告不执行修订，也不声明发现已关闭。
- 取证方式：逐 URL 打开官方页面和固定 commit 的 raw 文件；使用 Web 工具读取原文，GitHub 连接器按完整 commit 读取文件和指定源码行段，并通过 Git ref/tag API 核对两个 annotated tag 的解引用。未仅凭搜索片段或作者来源记录作结论；未做原始 HTTP 字节下载与本地哈希比对。
- 写入范围：仅本报告。正文、来源记录、registry、plans、邻近正文及构建产物均不修改。

### 审阅文件清单

1. [目标正文](../../knowledge/05-cluster-platform/accelerator-sharing-and-isolation.md)，190 行；下文“正文”均指此文件，位置采用审阅时的 1-based 行号。
2. [作者来源记录](batch-23-t05-06-sources.md)，含主张—来源表、unknown 与建议登记条目。
3. [来源登记表](../../sources/registry.yaml)：逐项读取用户指定的七项 ID：`src.nvidia.mig-user-guide-2026-10-18`、`src.nvidia.mps-docs-2026-10-18`、`src.nvidia.k8s-device-plugin-sharing-v0.20.1`、`src.ascend.ascend-device-plugin-44385c13`、`src.nvidia.mig-device-names-2026-10-08`、`src.ascend.docker-runtime-44385c13`、`src.kubernetes.device-plugins-v1-32`；同时核对正文另外两项 `src.nvidia.k8s-device-plugin-v0.20.1`、`src.ascend.mind-cluster-v26.1.1`。
4. 邻近正文：[设备资源链](../../knowledge/05-cluster-platform/device-resource-chain.md)、[镜像运行时基线](../../knowledge/05-cluster-platform/container-image-runtime-baseline.md)、[准入与放置](../../knowledge/05-cluster-platform/admission-and-placement.md)；容量链接及方法边界另核对[争用与容量验证](../../knowledge/05-cluster-platform/contention-capacity-validation.md)。不对这些页面另作完整技术审阅。
5. 仓库约定与验收：`README.md`、`docs/authoring-guide.md`、`content-outline.md`、`schemas/content.schema.json`、`plans/full-coverage-backlog.yaml` 的 T05-06 条目；只读检查 `Makefile` 和校验入口以避免生成其他文件。

## 结论：需修订

共 **7 项开放发现：4 项 P1、2 项 P2、1 项 P3**。NVIDIA 共享路线已有实质内容，`replicas` 不等于算力份额、MPS 非预留、插件 experimental、GPU 机制不得套用于 NPU 等主要警告有官方依据。但 MIG 的故障/分区边界被概括过宽，NPU 的访问控制证据被放在“独占”基线下，NVIDIA 版本条件尚未落到可核查的有限样板，且有一项 MPS 限制错配。

**NPU 共享分支仍是 `blocked_on_evidence / open`。** 正文诚实保留未知是正确做法，却不能替代第五条必交验收；本次不能据此判 T05-06 通过。所有发现须由作者修订，再由独立审阅者定向复核；结构检查通过不关闭技术发现，也不构成硬件验证。

## 逐 URL 取证清单

以下均在 2026-10-18 本轮实际取得正文或源码。可变页的“页面更新时间”和“本轮观察日期”分别记录，不把观察日期当发布版本。

| 证据 | 实开官方 URL / 固定文件 | 版本与实际支持范围 |
|---|---|---|
| E01 | [MIG Supported GPUs](https://docs.nvidia.com/datacenter/tesla/mig-user-guide/supported-gpus.html) | 可变页，页面标注 2026-10-13 更新。核对列出的产品及 2/4/7 实例上限；不能以 Ampere+ 代替逐产品支持条件。 |
| E02 | [MIG Concepts](https://docs.nvidia.com/datacenter/tesla/mig-user-guide/concepts.html) | 可变页，2026-10-13 更新。核对 GI/CI、slice、profile placement、碎片和 Table 3；CI 共享父 GI 的显存/引擎，表中的三列是 Streams、MPS、MIG，而不是 device-plugin 的三种配置。 |
| E03 | [MPS index](https://docs.nvidia.com/deploy/mps/index.html) | 实开时重定向至 `/deploy/mps/latest/index.html`，页面标注 2026-09-09 更新。核对 daemon/server/client runtime，及 Legacy MPS v2 与显式选择的 MPS v3；这是可变文档入口，不是 CUDA/驱动版本锚。 |
| E04 | [MPS When to Use MPS](https://docs.nvidia.com/deploy/mps/when-to-use-mps.html) | 可变页，2026-09-09 更新。逐节核对系统/客户端限制、有限错误遏制、动态限额、连接上限、显存限额、提前终止、locality domains、静态 SM 分区。具体发现见 C02/C05/C06。 |
| E05 | [k8s-device-plugin README@487d7a93](https://github.com/NVIDIA/k8s-device-plugin/blob/487d7a93894b0f3ad08097169593972eb3ca8206/README.md)；[同 commit raw](https://raw.githubusercontent.com/NVIDIA/k8s-device-plugin/487d7a93894b0f3ad08097169593972eb3ca8206/README.md) | 核对 Running GPU Jobs 告警、MIG_STRATEGY、Shared Access、time-slicing/MPS。无 GPU 请求的暴露告警、按进程分时、共享副本、节点级配置、MPS experimental 与插件层 MIG 限制均确有原文。 |
| E06 | [Ascend Device Plugin README@44385c13](https://github.com/Ascend/mind-cluster/blob/44385c13d7b1d87def35f1604e8be4d16de6ca4e/component/ascend-device-plugin/README.md)；[raw](https://raw.githubusercontent.com/Ascend/mind-cluster/44385c13d7b1d87def35f1604e8be4d16de6ca4e/component/ascend-device-plugin/README.md) | 核对“支持的产品形态”及组件介绍。产品列表前的适用描述是资源监测；虚拟设备发现、物理设备决定虚拟设备健康、分配/重调度有说明，没有所选共享模式的固件/CANN 配套及资源隔离承诺。 |
| E07 | [Ascend Docker Runtime README@44385c13](https://github.com/Ascend/mind-cluster/blob/44385c13d7b1d87def35f1604e8be4d16de6ca4e/component/ascend-docker-runtime/README.md) | 重开既有 runtime 登记对应的设计简介：可见设备变量、namespace 挂载、device cgroup、主机 CANN 库挂载。它说明访问边界，不说明不同容器之间的分配互斥。 |
| E08 | [runtime/process/process.go@44385c13](https://github.com/Ascend/mind-cluster/blob/44385c13d7b1d87def35f1604e8be4d16de6ca4e/component/ascend-docker-runtime/runtime/process/process.go)；[raw](https://raw.githubusercontent.com/Ascend/mind-cluster/44385c13d7b1d87def35f1604e8be4d16de6ca4e/component/ascend-docker-runtime/runtime/process/process.go) | raw 原文与 GitHub 分段读取交叉定位；GitHub 返回 blob SHA `acbd7a1ec0703498abfcfcb6ce1aa493069091b1`。核对 `parseDevices`、`getMountPath`、`addDeviceToSpec` 等；原始文件 L536–549 为重命名函数，不能沿用正文的 L411–421。Web 解析会重排空行，源码行号采用 GitHub 文件行段，不采用解析器的行号。 |
| E09 | [MIG Device Names](https://docs.nvidia.com/datacenter/tesla/mig-user-guide/mig-device-names.html) | 本轮重开，页面标注 2026-10-13 更新；既有登记的 2026-10-08 是此前观察日期，不被本轮追改。核对 R470 前后命名差异、R570 前后枚举条件、同一 GPU 下多个 CI UUID 示例。 |
| E10 | [Kubernetes v1.32 Device Plugins](https://v1-32.docs.kubernetes.io/docs/concepts/extend-kubernetes/compute-storage-net/device-plugins/) | 版本化文档快照。核对整数扩展资源、不可超配/设备不可在容器间共享的 API 口径、注册/上报/Allocate 及运行时配置；这些约束不证明不同插件 ID 背后的物理设备必不共享。 |
| E11 | [MIG Deployment Considerations](https://docs.nvidia.com/datacenter/tesla/mig-user-guide/deployment-considerations.html) | 审阅补充，可变页，2026-10-13 更新。有 GPU/CUDA/驱动条件、Linux/容器边界，以及驱动层可在 MIG 上使用 MPS 的说明；不能把插件不支持等同于所有驱动层组合不支持。驱动表仍须结合选定产品的其他官方材料交叉确认。 |
| E12 | [GPU Memory Error Management — Error Recovery and Response Flags](https://docs.nvidia.com/deploy/a100-gpu-mem-error-mgmt/error-recovery-and-response-flags.html) | 审阅补充，可变页，2026-09-09 更新。恢复动作包含终止全部 GPU 进程后整卡 reset、OS reboot，以及部分 MIG 分区受损后的 drain-and-reset；是反对“任何错误都互不影响”的边界证据，不是本库故障注入结果。 |

标签核验：[NVIDIA tag 对象](https://api.github.com/repos/NVIDIA/k8s-device-plugin/git/tags/03296a61aeb9943906a1789f978ac3c87e13dfdd) 的目标确为 `487d7a93894b0f3ad08097169593972eb3ca8206`；[MindCluster tag 对象](https://api.github.com/repos/Ascend/mind-cluster/git/tags/387a7f2b5f9ddfdbcdff0d8c85386fc68e2fe7fb) 的目标确为 `44385c13d7b1d87def35f1604e8be4d16de6ca4e`。这是 ref/对象关系核对，不是签名或发行包完整性认证。

E11/E12 是本报告新增的审阅证据，未借此修改来源登记。若作者采纳其技术内容，应在后续修订权限范围内登记精确来源与观察范围。

## 发现表

| ID | 优先级 | 位置（文件＋章节） | 问题 | 支持证据（URL / 原文定位） | 关闭条件 |
|---|---|---|---|---|---|
| B23-T06-C01 | P1 | `knowledge/05-cluster-platform/accelerator-sharing-and-isolation.md:122`，§Ascend 的共享与虚拟设备分支，尤其 L128–141；任务验收 3/5 | **NPU 共享模型仍未交付。** 现有内容仅证实虚拟设备上报/健康归因，并以独占和 unknown 收束；没有选定型号、固件、CANN、plugin 的共享支持交集，也没有该共享模式的分配、显存/计算、争用、故障与回收边界。这不是要求把未知改写成支持，而是必交子项仍开放，不能判整项通过。 | [E06 组件 README](https://github.com/Ascend/mind-cluster/blob/44385c13d7b1d87def35f1604e8be4d16de6ca4e/component/ascend-device-plugin/README.md) 的设备发现与健康检查只覆盖上报语义；正文 L128 自认未取得共享规格/隔离/回收证据；backlog T05-06 第五条明令不得以独占/unknown 代替共享验收。 | 取得并登记至少一个选定 NPU 共享模式的官方型号/固件/CANN/plugin 条件，补齐可由材料支持的资源、故障、分配/回收语义和最小验证设计，再定向复核。资料仍不足时，维持该子项 `blocked_on_evidence / open`，本发现不关闭，T05-06 不通过；不得仅补资料计划或独占说明。 |
| B23-T06-C02 | P1 | `knowledge/05-cluster-platform/accelerator-sharing-and-isolation.md:64`，§边界分层；§路线对照 L115–118；§选择流程 L137；§最小验证 L163 | **MIG 的有条件隔离被写成了不分层、不分错误的保证。** “一个实例的错误不影响其他实例”没有区分独立 GI 与同 GI 内 CI；对照表又把 GI/CI 并列为物理分区，易把 GI 显存边界套到共享父 GI 显存的 CI。选择与验证还把任意“触发错误”直接分为 MIG 不影响、MPS/time slicing 会影响，未定义错误类别或整卡/节点故障边界。前文 L81 确实说明 CI 共享，但未约束后面的承诺。 | [E02 Partitioning](https://docs.nvidia.com/datacenter/tesla/mig-user-guide/concepts.html) 明确 CIs 共享父 GI 的 engines/memory；[E12 恢复动作](https://docs.nvidia.com/deploy/a100-gpu-mem-error-mgmt/error-recovery-and-response-flags.html) 仍有整卡 reset/节点 reboot；[E04 显存限额与终止节](https://docs.nvidia.com/deploy/mps/when-to-use-mps.html) 区分客户端 OOM、致命 GPU 故障及安全终止，并非所有错误都传播。 | 所有摘要、矩阵、选择和验证口径统一到“独立 GI 的所述资源隔离”和官方支持的具体错误范围；同 GI 多 CI 不承诺独立 GI 级显存/QoS。明确整卡、驱动、主机等共享故障域，定义验证所用错误类别与判据；删除对任意错误的必然传播/必然隔离判断。无需在本次文档修订中执行故障注入。 |
| B23-T06-C03 | P1 | `knowledge/05-cluster-platform/accelerator-sharing-and-isolation.md:130`，§Ascend 的共享与虚拟设备分支“可确认的基线”；关联 L159–162 | **runtime 可见性/访问控制不足以证明整卡独占。** `ASCEND_VISIBLE_DEVICES` 和 device cgroup 能说明某容器允许访问指定设备，不能说明另一容器没有被指定同一物理设备。把这组证据归为“整卡/NPU 设备独占”，使未建立的分配互斥看似已经确认；最小验证也没有显式核对两个租户的物理分配是否互斥及原访问者是否退出。 | [E07 runtime 设计简介](https://github.com/Ascend/mind-cluster/blob/44385c13d7b1d87def35f1604e8be4d16de6ca4e/component/ascend-docker-runtime/README.md) 说明按指定设备挂载和访问控制；[E08 addDeviceToSpec](https://github.com/Ascend/mind-cluster/blob/44385c13d7b1d87def35f1604e8be4d16de6ca4e/component/ascend-docker-runtime/runtime/process/process.go#L551) 添加节点及按 major/minor 的许可，没有给出跨容器互斥证明。邻文运行时基线 L79/L113 也明确可见性不替代访问证明、整栈支持交集仍未知。 | 将已证事实收窄为设备暴露/访问控制；若保留独占模式，单列受信分配器不重复分配同一物理设备、非特权访问路径与旁路约束等前提，并给出相应官方/实现证据。验证设计至少检查两个租户的分配记录与稳定物理身份、未获配设备的访问边界、释放后旧进程退出及新分配；未取得证据的环节保持未知，不再称已确认独占。 |
| B23-T06-C04 | P1 | `knowledge/05-cluster-platform/accelerator-sharing-and-isolation.md:80`，§MIG 工程条件 L85；§MPS L91–99；§选择流程 L140；§待确认 L190 | **验收要求的机型/驱动/plugin 条件尚未绑定，且一个命名结论已越过版本边界。** 列出很多机型、插件 commit 和“需要驱动支持”不等于给出各路线的有限适用条件；MIG 最低驱动与 MPS 功能版本还整体待确认。L85 将 MIG 设备统一写成 `MIG-<UUID>`，却没有 R470 条件。未说明选用哪套 MPS 功能/控制接口与插件共享样板的支持交集。 | [E09 CUDA Device Enumeration](https://docs.nvidia.com/datacenter/tesla/mig-user-guide/mig-device-names.html) 分 R470 前后的两种名字，并分 R570 前后枚举；[E03 MPS index](https://docs.nvidia.com/deploy/mps/index.html) 区分 v2/v3；[E05 README](https://github.com/NVIDIA/k8s-device-plugin/blob/487d7a93894b0f3ad08097169593972eb3ca8206/README.md) 给的是插件前置/共享限制，不自动覆盖每项 MIG/MPS 特性；[E11](https://docs.nvidia.com/datacenter/tesla/mig-user-guide/deployment-considerations.html) 另有部署条件。 | 对 MIG、MPS、time slicing 分别给出可核查的有限样板或支持条件表，区分 GPU 型号、OS/驱动/CUDA 功能条件、plugin 版本/模式，不要求覆盖所有列出的 GPU。补齐 UUID/枚举的驱动边界及 MPS 功能口径；官方材料冲突或没有支持交集的组合不得宣称适用，亦不得以“待现场核对”关闭该内容验收。 |
| B23-T06-C05 | P2 | `knowledge/05-cluster-platform/accelerator-sharing-and-isolation.md:97`，§MPS 静态 SM 分区限制 | **把 locality domains 的 vGPU 禁用条件错误移给静态 SM 分区。** 当前所引页面支持“静态 SM 分区与 locality domains 互斥”，但不能由此推出静态 SM 分区与 vGPU 互斥。 | [E04](https://docs.nvidia.com/deploy/mps/when-to-use-mps.html) 的 Limitations of Locality Domains 才列 vGPU 不支持；Limitations of Static SM Partitioning 列与 locality domains 互斥、context 前设环境变量、不能删除正在使用的分区、静态模式忽略动态 provisioning 等，没有正文所称的 vGPU 限制。 | 删除或收窄静态分区的 vGPU 断言，将两种特性的限制分开；若坚持此结论，另提供精确型号/版本下的官方依据。不能反向推断“静态分区一定支持 vGPU”。 |
| B23-T06-C06 | P2 | `knowledge/05-cluster-platform/accelerator-sharing-and-isolation.md:66`，§官方并发对照表解释；§MPS L96 | **给 48 与 60 补出了未经证实的统一层级解释。** Table 3 的 MPS 数值 48 确有原文，但把它解释为“驱动层口径”并不能消除与另一文档 60 个 client CUDA contexts 的条件差异；正文也省略了 60 所依赖的具体连接设置。原表第一列为 Streams，应明确标出，避免与后文 time slicing 混读。两类数量均不能直接作为租户/replica 容量。 | [E02 Table 3](https://docs.nvidia.com/datacenter/tesla/mig-user-guide/concepts.html) 只列并发机制的数值，没有给出正文新增的版本/层级归因；[E04 Client-Server Connection Limits](https://docs.nvidia.com/deploy/mps/when-to-use-mps.html) 的 60 绑定 `CUDA_DEVICE_MAX_CONNECTIONS=2`，增加该值会减少可接入客户端数量。 | 标明表的三个列名，分别记录两个来源的指标、配置前提与观察范围；给不出版本/实现对应关系时明确“未对齐，不能合并为通用容量上限”，不自行解释为某层固定上限。显式区分 context、进程、租户与插件访问名额；不得用这些数字推定租户公平份额。 |
| B23-T06-C07 | P3 | `knowledge/05-cluster-platform/accelerator-sharing-and-isolation.md:126`，§Ascend 容器侧重命名；`docs/research/batch-23-t05-06-sources.md:25` 对应复用证据行 | **技术事实可支持，但给出的固定源码行号错误。** 所指 commit 的 L411–421 属 `parseDevices` 附近，而不是虚拟设备挂载名称转换；来源记录的定位也沿用了旧范围。这会使“精确复用既有证据”的读者无法按声明位置复核。 | [E08 getMountPath，L536–549](https://github.com/Ascend/mind-cluster/blob/44385c13d7b1d87def35f1604e8be4d16de6ca4e/component/ascend-docker-runtime/runtime/process/process.go#L536) 的 `case virtualDavinciName` 提取数字并构造 `davinci` 路径；GitHub 按完整 commit 分段读取已确认。 | 后续作者修订时将正文与来源记录统一定位到该 commit 的 `getMountPath`，给出正确行号/函数名；保留 `vdavinciN`→`davinciN` 的事实，不把重命名解释成隔离。此次仅记录发现，不代改来源记录。 |

## 验收项覆盖表

“覆盖”仅表示指定文档要素可定位，不抵消发现表中的技术错误或证据缺口。

| 验收项 | 判断 | 正文定位与依据 | 未关闭内容 |
|---|---|---|---|
| 1. 租户/进程/容器，以及设备、显存、CPU、主机内存、网络、存储、故障域边界；命名空间/配额不保证硬件安全隔离 | **部分覆盖** | §定义 L40–51、§边界分层 L53–66、§常见误解 L165–171 已列出所需层次；未用 namespace/cgroup 直接证明 GPU 内部切分。 | 故障域和独占结论仍过强，C02/C03；主机资源、访问控制与设备资源隔离不能在总结处重新合并。 |
| 2. MIG、MPS、device-plugin time slicing 的机型/驱动/plugin 条件及分区、调度、公平性、显存、故障比较 | **部分覆盖** | §NVIDIA L68–120 已分别介绍机制，含插件版本、replicas、节点级配置、MPS 限额非预留及 experimental；time slicing 的按进程分时有描述。 | C02/C04/C05/C06。尚缺可核查的有限支持交集及统一口径比较；按进程分时或按 context 限额不是租户级公平性保证，应明确后者仍需平台策略和容量验证。 |
| 3. Ascend 选型号/固件/CANN/plugin 官方条件；无材料则保持未证实并列独占 | **部分覆盖** | §Ascend L122–133、§选择流程 L141 正确执行了不从 GPU 外推、证据不足保持开放的兜底规则。 | 兜底记录合规，但没有选定共享模式的官方支持交集，C01；所谓独占基线本身也需收窄，C03。 |
| 4. 选择流程、观测/异常、最小可见性/分配/争用/回收验证、官方反例、容量指南链接 | **覆盖（文档要素）** | §选择流程 L135–142、§观测 L144–153、§最小验证 L155–163，四类最小验证均有；L72/L168–171 提供官方材料支持的反例；L161 链接容量指南且目标存在。 | 选择与额外故障遏制测试的技术判据仍须按 C02/C03 修订；“有设计”不是“执行通过”。 |
| 5. GPU/NPU 共享是必交分支；资料不足时 NPU 仍 blocked/open，独占或 unknown 不替代共享验收 | **缺口** | GPU 分支已有正文；NPU L128 明确 `blocked_on_evidence / open`，来源记录 unknown #1 亦一致。 | C01 未关闭前，不得把 T05-06 或 NPU 共享子项标为已验收。保持 blocked/open 是准确状态，不是缺口已补齐。 |

## 元数据、来源与本地链接

- 目标 frontmatter 的 `id` 为 `cluster-platform.accelerator-sharing-and-isolation`，全库仅一处；`title` 与 H1 一致，`type: concept`、`domain: cluster-platform`、`status: draft`、`platforms: [nvidia, ascend]` 与主归属/内容类型相符。
- `updated_at: "2026-10-18"` 是日期字符串；`summary`、五个 `related_ids`、`verification` 结构符合 schema。concept 不强制要求 `applicability`，不据此报缺失。
- 九个 `source_refs` 全部已登记；四个 `verification.evidence_refs` 均可解析；五个 `related_ids` 均存在。`source_checked` 的 notes 明确只读核对范围及未执行事项，未冒称 `reproduced`。该元数据状态不使错误技术主张或开放验收自动成立。
- 只读运行 `PYTHONDONTWRITEBYTECODE=1 make check`，结果为 **PASS: 100 content entries; 465 sources**；目标的本地正文链接及容量指南链接有效。检查不证明远程支持交集、远程锚点或技术正确性；C07 是证据定位错误，不是本地链接失效。
- 未运行 `make build`：它会写 `build/catalog.json`、`build/catalog.md`，与用户“只允许创建本报告”冲突；此处遵守更具体的写入限制。未改 `src/kb/`，未运行测试或硬件实验。

## 与邻近正文的口径一致性

| 邻近正文 | 核对结论 |
|---|---|
| `device-resource-chain.md`，GPU 账本 ID/运行时 ID及“重复/过期分配” | 该页 L93/L163 已区分 `UUID::n` 账本副本与去注解后的物理 UUID。本文 L48/L142 关于资源单位不等于整卡的主张与其一致；time slicing 的“物理超卖”不是让 Kubernetes 超配同一扩展资源 ID，不应改写为上游 API 允许整数资源超配。 |
| `container-image-runtime-baseline.md`，§2 权限、§3 Ascend 样板、§4 缺项分类 | 该页 L79 区分设备可见性和访问许可，L113 保留产品/驱动/固件/CANN 支持交集未知，L137 强调设备集合按身份映射而非文本/数量判等。本文 L130 将 runtime 证据列成独占已确认基线与此不一致，见 C03；vNPU 名称转换也不能消除这些未知。 |
| `admission-and-placement.md`，§沿状态找等待位置及配额/准入 | 其 L43/L66–69 区分配额、准入、设备分配和应用进展。本文没有宣称准入就提供卡内隔离，整体一致；应继续避免用 replica 名额、MPS 上限或调度成功推定租户公平与硬件 QoS。未发现需要单独新增的术语冲突。 |

## unknown / 证据边界

1. **NPU 共享支持与隔离仍未知**：所选资料没有建立任何具体型号/固件/CANN/plugin 的共享支持交集，也未建立虚拟设备数量/规格、资源保证、越界行为或回收保证。E06 的资源监测产品列表不是上述支持矩阵。这里的结论是“本次材料不足”，不是“厂商不存在此类文档/能力”。
2. **NPU 独占及安全威胁模型尚未证明**：runtime 的指定设备访问控制可核对，但跨容器分配互斥、特权/host 访问旁路及共享驱动攻击面不由这些证据解决；不能把 cgroup 许可当完整硬件安全隔离。
3. **GPU 的整栈支持交集未建立**：固定 plugin commit 与可变 MIG/MPS 页面并列，不自动构成同一已支持部署。静态 SM 分区的驱动版本交集、MPS 接口选择及插件是否实际启用相应能力仍需精确材料。插件层禁止 MPS-on-MIG 不等于驱动层一概禁止。
4. **上游数字/版本差异不能自行消歧**：E02 的 48 与 E04 的有条件 60 保留为不同来源口径；E09 的 R570 示例含 `470.42.01+` 括注混写，不用该示例括注确定最低驱动。E11 当前驱动表把 A100/A30 列 R525、H100/H200 列 R450，而 E09 另有 CUDA/驱动分支枚举条件；这些页面不足以在本报告内建立可靠的逐型号最低驱动交集，不机械抄表作为修订答案。
5. **租户级公平性、性能和现场结果未知**：没有吞吐、尾延迟、带宽 QoS 实测或已授权故障注入结果；按进程分时、context 上限和静态分区不单独证明租户公平。不把一方的普通 OOM、可控退出与致命 GPU 故障当成同一种传播测试。
6. **回收不是清场/保密证明**：设计上“新任务获得资源”不能单独证明旧进程不再访问、设备状态已清理或残留数据不可读；本轮未核对设备清零/复位的机型保证，不据此补写安全承诺。

## 审阅局限

- 用户要求实开的核心 URL 最终均取得原文；没有核心材料因最终无法访问而仅凭摘要判定。首次普通 Web raw 访问 runtime 源码返回 Cache miss、Node HTTP 通道返回 fetch failed，随后已由 Web 连接器 raw 原文和 GitHub 固定 commit 行段补齐；未把失败通道当“文件不存在”。
- 未取得所选 NPU 共享模式的专门官方支持材料；没有声称已穷尽厂商全部文档，也没有用搜索片段、源码中出现 vdevice 或未来取证计划关闭 C01。
- Web 结果可能来自服务端缓存/解析；未校验原始响应字节、全文 SHA-256、网页存档、tag 签名、发行包或容器镜像。本轮观察不能追溯证明作者 2026-10-08 时看到的网页内容。
- 未逐行重审相邻正文全部上游实现，亦未重审 NVIDIA 分配/健康检查实现、Ascend DCMI 切分/销毁实现、固件或 CANN 行为；本报告只在 T05-06 主张和一致性需要的范围内下结论。
- 未连接集群，未安装/编译组件，未创建/销毁 MIG 或 vNPU，未启动 MPS、配置 time slicing、提交租户负载、读取现场租户数据或执行故障/回收测试。本报告不授予任何执行授权。
- 工作区原已有正文、来源登记和其他 Batch 23 草稿变动；它们不是本次审阅的写入。本轮仅新增本文件，所有发现仍待作者修订与定向复核。
