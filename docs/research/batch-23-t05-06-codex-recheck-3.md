# Batch 23 · T05-06 第三轮定向复核

## 审阅元数据

- 任务：T05-06「加速器共享与租户隔离机制」；承接[第二轮定向复核](batch-23-t05-06-codex-recheck-2.md)，核验 C04、R04 及本次修订相关问题。沿用同一独立审阅者角色，未参与作者修订，未派发子代理；角色连续性不证明执行模型连续性。
- 日期：2026-10-18，Asia/Shanghai（UTC+08:00）。
- 实际执行模型：`unknown`；实际 reasoning effort：`unknown`。本轮接口未暴露可核验的实际部署模型标识或 effort，不把仓库约定、文件名中的 Codex、作者说明或前轮记录当作实际模型证明；不能据此认证满足指定模型/effort 的审阅约定。
- 方法：重新读取正文、来源记录、registry 相关条目、原 C04 与前轮关闭条件及任务 acceptance；重新打开 NVIDIA 精确文档和插件固定 commit 的 README，并补查同 commit 的 MPS daemon 实现。作者修订摘要仅用于定位，不作为关闭证据。
- 写入范围：仅新增本报告；不修改正文、registry、来源记录、plans、其他报告或构建产物。判定只覆盖本次定向范围，不重审整个 Batch 23。

### 本地证据定位

以下“正文”指 [accelerator-sharing-and-isolation.md](../../knowledge/05-cluster-platform/accelerator-sharing-and-isolation.md)；“来源记录”指 [batch-23-t05-06-sources.md](batch-23-t05-06-sources.md)；“registry”指 [sources/registry.yaml](../../sources/registry.yaml)。行号为本轮读取的原文件坐标。

| 材料 | 本轮重点位置 |
|---|---|
| 正文（236 行） | MIG L84–91；MPS L95–105；time slicing L107–115；有限样板 L117–129，尤其 L124–126；选择流程 L179；来源与 unknown L224–236 |
| 来源记录（142 行） | 版本声明 L7–9；主张表 L16–22；unknown L35–37；建议登记区 L56–77、L92–102 |
| registry | MIG/MPS/插件共享 L5702–5734；Deployment L5774–5784；注意实际登记与来源记录的“建议登记”不是同一对象 |
| 原验收与前轮结论 | [初审 C04](batch-23-t05-06-codex-review.md) L56；[第二轮复核](batch-23-t05-06-codex-recheck-2.md) L54、L68–83；[任务 acceptance](../../plans/full-coverage-backlog.yaml) L5620–5625 |

审阅快照 SHA-256（本地文件身份，不认证远程文档字节）：

- 正文：`a781d1ab1dcd98086963bfd77e78891e8b171fe288a132800f73cb7494c91250`。
- 来源记录：`1d5689b04c8f432a0501aeef2da197020bf1efb08641ba6a600d00eada476706`。
- registry：`a336ce6edc17521e79c164d254c2fb272dde9cb60aea8b978ac5018262cce62c`。

## 本轮关键上游证据

均为 2026-10-18 本轮重新读取。E03、E06 固定于 NVIDIA commit `487d7a93894b0f3ad08097169593972eb3ca8206`；其 GitHub 行号经连接器按原文件行段核实，不采用网页转换后的行号。可变文档不因页脚日期而成为某个驱动/CUDA 发行版的版本化证明。

| 编号 | 精确页面 / 文件 | 核验位置与用途 |
|---|---|---|
| E01 | [MIG Deployment Considerations](https://docs.nvidia.com/datacenter/tesla/mig-user-guide/deployment-considerations.html) | 开头 GPU/CUDA/driver 表；System / Application Considerations。支持正文采用的 A100/A30、B200 文档条件，以及 Linux、P2P、IPC、NCCL 和驱动侧 MPS-on-MIG 边界；H100/H200 冲突行仍在上游 |
| E02 | [MIG Supported GPUs](https://docs.nvidia.com/datacenter/tesla/mig-user-guide/supported-gpus.html) | Supported GPU Products 表。核对选定产品在表内；不把产品入表推成任意驱动/CUDA 组合可用 |
| E03 | [插件 README](https://github.com/NVIDIA/k8s-device-plugin/blob/487d7a93894b0f3ad08097169593972eb3ca8206/README.md) | Prerequisites L70–80；MIG_STRATEGY L251–264；Shared Access L358 起；MPS L516–599；GFD 标签示例 L970–975。分别核对通用前提、共享模式与产品示例的证据范围 |
| E04 | [MPS Overview](https://docs.nvidia.com/deploy/mps/index.html)、[When to Use MPS](https://docs.nvidia.com/deploy/mps/when-to-use-mps.html) | 通用组件和 v2/v3 区分；System / Application Considerations、Dynamic Execution Resource Provisioning、Limits。通用功能说明不是插件版本的集成支持声明 |
| E05 | [MPS v3 Interface](https://docs.nvidia.com/deploy/mps/latest/mpsv3-interface.html)、[MPS Quick Start](https://docs.nvidia.com/deploy/mps/quick-start.html) | Enabling MPS v3、CLI Command Structure、Server；Quick Start 的启动/退出对照。默认 protocol 2，v3 需显式选择，控制命令形态不同 |
| E06 | [插件 MPS daemon.go](https://github.com/NVIDIA/k8s-device-plugin/blob/487d7a93894b0f3ad08097169593972eb3ca8206/cmd/mps-control-daemon/mps/daemon.go#L84) | EnvVars L84–89；Start L113–128；健康检查与 EchoPipeToControl L203–233。用于核对该插件实际采用的控制接口，而非只看当前通用 MPS 文档 |
| E07 | [CUDA 12.0.0 Release Notes](https://docs.nvidia.com/cuda/archive/12.0.0/cuda-toolkit-release-notes/index.html) | §1.1 Table 2：CUDA 12.0.x 的 Linux x86_64 minor-version compatibility 下限为 525.60.13；与 Table 3 的 Toolkit 配套驱动口径区分 |
| E08 | [CUDA Minor Version Compatibility](https://docs.nvidia.com/deploy/cuda-compatibility/minor-version-compatibility.html) | CUDA 11.x / 12.x 驱动范围表及功能限制，用于交叉核验 E01 的冲突，不充当逐 GPU 的 MIG/MPS 支持表 |

## 逐项判定

| ID / 原优先级 | 本轮判定 | 理由与关闭边界 |
|---|---|---|
| **B23-T06-C04 / P1** | **OPEN** | MIG 冲突组合已排除；MPS/time-slicing 新增了机型、Linux 和插件通用前提，但还没有选定可核查的驱动/CUDA 软件栈。MPS 仍列 v2/v3 二选一，且未证明所选接口与该插件集成相容，见 R05。准确保留“功能最低版本 unknown”不等于已经满足有限样板验收 |
| **B23-T06-R04 / P1** | **CLOSED（撤回错误适用声明）** | 正文 L124、来源记录 L35 均明确 H100/H200 的 CUDA 12 + R450 行“不采用、未消歧”，不再作为可用下限。没有以另一通用 CUDA 下限替换成新的 H100/H200 支持承诺；上游冲突本身没有被解决 |
| **B23-T06-R05 / P1** | **OPEN，本轮新增发现** | 正文 L125、来源记录 L36 把“Legacy v2 或显式 v3”并入插件 v0.20.1 样板；E06 的集成路径实际使用 legacy 控制方式，不能从 E04/E05 的通用 v3 能力推出插件可任选 v3。详见下节 |

### C04：三条路线分别是否闭合

1. **MIG：本轮所需的有限文档条件已明显补齐，不再因 R04 阻塞。** 正文 L124 的 A100/A30（CUDA 11、R525 ≥525.53）与 B200（CUDA 12、R570 ≥570.133.20）可在 E01/E02 核对；Linux 与插件版本/暴露策略也有定位。NCCL 不支持 MIG、R570 仅同 GPU 内 MIG P2P、跨 GI CUDA IPC 不支持均保留，未扩大为任意 P2P/IPC 可用。这里认可的是有限文档条件表，不是认证所有 SKU、Toolkit 小版本与 profile 的部署矩阵，也不是确认这些版本就是全部产品的真实最低版本。
2. **MPS：仍未形成选定的软件/功能交集。** 正文 L125 明确把 `~=384.81`、nvidia-container-toolkit ≥1.7.0、K8s ≥1.10 称为插件前提，右栏与来源记录 L36 明确保留 MPS 功能最低驱动/CUDA unknown；因此本轮**不判其把插件前提直接改名为 MPS 功能最低版本**。但该行没有提供一套支持 A100、所需动态算力/显存限额及控制接口的实际驱动/CUDA 版本范围；L102 的 CUDA Driver API 4.0 条件也不能填补这项交集。仅“整卡共享”没有明确排除 L103 的可选静态 SM 分区进入该插件样板。v2/v3 的集成问题还有 E06 的具体反证，不能只让读者二选一。
3. **time slicing：插件语义已绑定，运行样板仍不完整。** 正文 L126 与 L109–113 的 replicas、节点级配置、与 MPS 互斥及无隔离口径均可由 E03 核对，新增 A100 与 Linux 也比前轮具体。但“同上前提”只继承通用插件要求，没有选定 A100 的驱动/CUDA 组合或运行时接入分支；E03 的前提还包括默认低层 NVIDIA runtime，正文没有在此样板交代采用该路径还是其他有依据的路径。无需全版本矩阵，但至少应把一套支持的硬件/软件条件与 `sharing.timeSlicing` 关联起来。

**最低版本未知与样板缺失必须分开。** C04 的剩余关闭要求不是推导 MPS 每项功能的历史最低版本，也不要求现场实测；而是选定至少一套有证据的正向适用范围。通用 Prerequisites、产品标签示例和当前 MPS 文档不能自动拼成该范围。尤其 E03 的 `A100-SXM4-40GB-MIG-1g.5gb-SHARED` 位于 `migStrategy=single` 的标签示例，不能独立证明“整卡 MPS + 任意 v2/v3 + 所列软件前提”的联合样板。

关闭 C04 时，作者仍需为 MPS/time-slicing 选定产品、Linux/驱动/CUDA 范围、运行时路径与插件共享模式；MPS 按该插件实现明确动态限额及控制接口，并把静态 SM 分区/其他接口另列为非本样板。可继续保留功能最低版本、完整矩阵和性能实测 unknown。不得仅删除 unknown、改写成“现场再核对”，或拿插件通用前提替代这套交集。

### R04：撤回范围与残留检查

- 正文 L124 只把 H100/H200 冲突行作为明确否定采用的警示；L86 的 H100/H200 支持产品列表不包含驱动下限，不能等同于仍采纳该冲突组合。L91、L179、L236 也未重新确认 R450 为 Hopper 可用条件。
- 对 `knowledge/`、实际 registry 及本任务来源记录搜索 `R450` / `450.80.02`；除明确撤回的上述位置外，另一正文命中为 [NVIDIA 软件栈档案](../../knowledge/02-software-stack/nvidia-documented-profile.md) L96，语义是 CUDA 12.8 forward-compatibility 不支持该分支、应升级，不是采用 H100/H200 + CUDA 12 + R450。未发现其他正文把本次冲突行作为已确认条件。
- 来源记录 L35 已同步撤回；实际 registry L5784 仍为逐型号交集 unknown 的概括，没有重复确认冲突数字。历史初审/复核报告中的旧引文属于问题记录，不应为“消除残留”追改。E07/E08 仍显示版本口径冲突；本轮只关闭作者错误采用该行的问题，**不宣布官方冲突已消歧，也不补造 H100/H200 最低驱动**。

## 新增发现

### B23-T06-R05 · P1 · 插件样板仍承诺可选 v3，但固定实现走 legacy 控制路径

- **状态与性质**：**OPEN**。这是本轮补查实现后确认的具体接口适用问题，不是把“尚未选样板”重复编号。前轮已出现 v2/v3 二选一措辞，并曾认可它作为通用接口描述；本轮不能据此继续认可其与插件 v0.20.1 的联合适用声明。没有证据证明该措辞是此次修订才新引入，故记为**本轮新发现，而非确认新引入的回归**。
- **受影响位置**：正文 L125；来源记录 L36。正文 L179 的“核对 v2/v3”流程应与修订后的样板范围一致。
- **实现证据**：E06 的 `EnvVars` 只提供 pipe/log 目录；`Start` L113 以 `nvidia-cuda-mps-control -d` 启动，随后 L120/L126 经 stdin 下发 `set_default_device_pinned_mem_limit` / `set_default_active_thread_percentage`；L205 的健康检查同样使用 legacy 命令，L210 起实现 stdin 管道。该路径没有选择 protocol 3，也没有将这些管理操作转换成 v3 的 module/verb 调用。
- **交叉核验与推论**：E05 明确 protocol 2 为默认、protocol 3 需显式选择，v3 用新的命令结构管理 server 等对象。结合固定实现，本轮可确认的是插件默认的 legacy 控制路径；**不能据通用文档宣称“显式选择 v3”是该插件样板的等价选项**。这是源码与接口文档的组合判断，不是已执行的强制 v3 失败实验，更不是宣称驱动层不支持 v3。
- **影响**：读者可能把自行启用 v3 当作原样插件仍能完成启动、限额与健康检查的已确认路径，使“有限样板”的接口条件失效。本项与 C04 相关，不将同一接口问题另算成第二份样板缺失。
- **关闭条件**：把原样插件 v0.20.1 样板收窄到有固定实现依据的 legacy v2 与动态显存/active-thread 限额；通用 v3 能力另述，明确它不属于本插件已核对样板。若坚持纳入 v3，则须提供与该固定插件版本相容的集成依据，不能只引用 MPS 通用页或给出启用 v3 的环境变量。来源记录同步；C04 所缺驱动/CUDA 范围仍需独立补齐。

未再增加 R06。通用插件前提尚未落成驱动/CUDA 交集、运行时路径未选定属于 C04 的持续缺口，不重复编号；保留 MPS 功能最低版本与现场性能 unknown 也不是新缺陷。

## 结论

**C04（P1）仍 OPEN；R04（P1）CLOSED；本轮新增发现 R05（P1）OPEN。T05-06 仍不可声明审阅通过。**

- MIG 的冲突适用行已经撤回，并保留未消歧状态；这项修订有效，不因上游尚未改正而重新开放 R04。
- MPS/time-slicing 的样板已更具体，但插件通用前提不是选定的产品/驱动/CUDA 功能支持交集；准确标注“功能最低版本 unknown”是必要边界，不是关闭 C04 的替代物。v3 与固定插件的联合适用还须按 R05 收窄或补证。
- 前轮关闭的 C01、R01、R02、R03 及更早关闭项，本轮不作完整重审；不把其未见本次相关回归提升成整篇重新通过。修订后继续定向复核 C04/R05。

## 证据边界与检查

- NVIDIA 可变网页只代表本轮观察；版本化 CUDA 12.0.0 文档与固定插件 commit 的证据范围分别保留。未建立全部 GPU/SKU、OS 发行版、驱动、Toolkit、runtime 与插件的兼容矩阵，未确定 MPS 功能历史最低版本；不把 README 的 `~=` 自行正规化成新的最低驱动承诺。
- 本轮补查 E05/E06/E07/E08 等精确证据入口，受仅创建报告限制，没有向 registry 或正文追加登记。作者后续据此修改适用声明时，应补足相应来源登记/定位。本轮还读取了 450.80.02 驱动版本说明；它不是本报告为 H100/H200 指定替代驱动的依据。
- GitHub 网页入口读取失败后改用连接器按固定 commit 分段读取；MPS v3 页通过文档目录定位到 E05 的实际地址。不把失败页面、搜索摘要或被截断的大树响应当作缺乏支持的证据；关键代码与 README 位置均另作了有界读取。
- 未安装驱动/Toolkit/插件，未连接集群，未创建 MIG/vNPU、启动 MPS、设置协议、配置共享、提交负载或故障注入。本文未证明启动成功、限额生效、隔离/QoS、回收或性能；文档和源码中的命令均未执行，不产生新的执行授权。
- `PYTHONDONTWRITEBYTECODE=1 make check`：**PASS，100 content entries / 469 sources**；只验证结构和本地引用，不验证远程内容或技术正确性。未运行 `make build`，因为它会写生成产物，违反本轮只创建指定报告的限制；未改 `src/kb/`，未运行单元测试。
- 开始时工作区已有正文、registry、索引及其他 Batch 23 报告等变动，不归为本轮写入。本轮仅新增本报告，不修改已有问题记录或计划状态；模型/effort 仍为 unknown，内容审阅结论与执行模型认证、硬件验证分别记录。
