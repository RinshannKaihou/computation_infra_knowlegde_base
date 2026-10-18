# Batch 23 · T05-06 第四轮定向复核

## 审阅元数据

- 任务：T05-06「加速器共享与租户隔离机制」；承接[第三轮定向复核](batch-23-t05-06-codex-recheck-3.md)，核验 C04、R05 及相关修订是否引入问题。沿用同一独立审阅者角色，未参与作者修订，未派发子代理；角色连续性不证明执行模型连续性。
- 日期：2026-10-18，Asia/Shanghai（UTC+08:00）。
- 实际执行模型：`unknown`；实际 reasoning effort：`unknown`。本轮接口未提供可核验的实际部署模型标识或 effort，不以仓库约定、Codex 文件名、作者摘要或历史元数据代替实际证明；本轮不能认证满足指定模型/effort 的执行约定。
- 方法：重新读取正文、来源记录、registry 相关条目、原 C04、前轮剩余关闭条件与任务 acceptance；重新打开 NVIDIA 精确页面、固定 commit 的插件 README 和 MPS daemon 实现，并核对 v0.20.1 annotated tag 的解引用。作者修订摘要仅作定位，不作关闭证据。
- 写入范围：仅新增本报告；不修改正文、来源记录、registry、plans、其他报告或构建产物。仅对本次定向范围作判定，不重新认证整个 Batch 23。

### 本地证据与快照

下文“正文”指 [accelerator-sharing-and-isolation.md](../../knowledge/05-cluster-platform/accelerator-sharing-and-isolation.md)；“来源记录”指 [batch-23-t05-06-sources.md](batch-23-t05-06-sources.md)。行号为本轮原文件坐标。

| 材料 | 本轮重点位置 |
|---|---|
| 正文（236 行） | MPS L95–105；time slicing L107–115；有限样板 L117–129，尤其 L125–126；路线对照 L137；选择流程 L179；验证与 unknown L194–236 |
| 来源记录（142 行） | 版本口径 L7–9；MPS/共享主张 L19–22；unknown #2/#3 L35–36；建议登记的版本描述 L61 |
| [registry](../../sources/registry.yaml) | 实际登记的 MIG/MPS/共享条目 L5702–5734；MIG Deployment L5774–5784；不是来源记录的“建议登记区” |
| 验收与关闭条件 | [初审 C04](batch-23-t05-06-codex-review.md) L56；[第三轮 C04 剩余要求](batch-23-t05-06-codex-recheck-3.md) L54–59、R05 关闭条件 L76；[任务 acceptance](../../plans/full-coverage-backlog.yaml) L5620–5625 |

审阅快照 SHA-256（本地文件身份，不认证上游网页字节）：

- 正文：`47387ec14be44b5e56a31b95a65c07b4443b7c3bb96687d2f68455808ad49cf0`。
- 来源记录：`21b77154eeba453f879194534681041703b95a8b810a54a476e314e01367a893`。
- registry：`a336ce6edc17521e79c164d254c2fb272dde9cb60aea8b978ac5018262cce62c`。

## 本轮关键上游证据

均于 2026-10-18 本轮重新读取。E03、E04 固定于 commit `487d7a93894b0f3ad08097169593972eb3ca8206`；GitHub 原文件行段经连接器读取，不把网页转换行号拼成源码锚点。NVIDIA 文档站为可变页，其当前功能说明不能整体回填为 R525 的功能清单。

| 编号 | 精确页面 / 文件 | 本轮核验与适用边界 |
|---|---|---|
| E01 | [MIG Supported GPUs](https://docs.nvidia.com/datacenter/tesla/mig-user-guide/supported-gpus.html) | Supported GPU Products 表有 A100-SXM4、40GB、Ampere、compute capability 8.0；支持产品身份核对，不证明插件集成或每项 MPS 功能 |
| E02 | [MIG Deployment Considerations](https://docs.nvidia.com/datacenter/tesla/mig-user-guide/deployment-considerations.html) | 开头表确列 A100/A30：CUDA 11、R525 ≥525.53；System Considerations 限 CUDA 支持的 Linux。它给的是 MIG 条件，不是 MPS 功能最低版本证明；H100/H200 冲突行仍存在 |
| E03 | [插件 README](https://github.com/NVIDIA/k8s-device-plugin/blob/487d7a93894b0f3ad08097169593972eb3ca8206/README.md#L70) | Prerequisites / Preparing your GPU Nodes（L70–115）除驱动、container toolkit、K8s 外，还要求默认低层 `nvidia-container-runtime`，并描述非默认路径需 RuntimeClass；Shared Access（L358–399）列节点级、互斥和 `sharing.timeSlicing`；MPS（L516–599）列 `sharing.mps`、experimental、整卡资源与 MIG 限制、显存等分及算力限额 |
| E04 | [插件 MPS daemon.go](https://github.com/NVIDIA/k8s-device-plugin/blob/487d7a93894b0f3ad08097169593972eb3ca8206/cmd/mps-control-daemon/mps/daemon.go#L84) | EnvVars L84–89；Start L92–128：`-d` 启动，设置 device-pinned-memory 与 active-thread-percentage 限额；AssertHealthy / EchoPipeToControl L203–233：legacy 命令经 stdin 管道发送。此启动段未选择 protocol 3，也未启用静态分区的 `-S` |
| E05 | [MPS v3 Interface](https://docs.nvidia.com/deploy/mps/latest/mpsv3-interface.html) | Enabling MPS v3、CLI Command Structure：默认 protocol 2，v3 需显式选择且控制命令结构不同。用于解释 E04 的接口边界，不证明该插件支持 v3，也不证明 R525 提供 v3 |
| E06 | [When to Use MPS](https://docs.nvidia.com/deploy/mps/when-to-use-mps.html) | System Considerations；Dynamic Execution Resource Provisioning；Static SM Partitioning。Linux 属所列 OS；动态限额不构成专属资源预留；Legacy v2 本身也可有静态 SM 分区，其启用需要单独模式，不能由“v2”或“整卡”区分动态/静态功能 |
| E07 | [CUDA Minor Version Compatibility](https://docs.nvidia.com/deploy/cuda-compatibility/minor-version-compatibility.html) | CUDA 11.x 驱动范围表注明更新驱动仍可经向后兼容使用。不能把表中 minor-version compatibility 的 `<525` 误读成 R525 禁止运行 CUDA 11；这仍不是 MPS 功能认证 |

另经 [v0.20.1 ref](https://api.github.com/repos/NVIDIA/k8s-device-plugin/git/ref/tags/v0.20.1) → [annotated tag 对象](https://api.github.com/repos/NVIDIA/k8s-device-plugin/git/tags/03296a61aeb9943906a1789f978ac3c87e13dfdd) 确认其目标 commit 为上述 `487d7a93…`。此处只核对版本身份，不作签名认证。

## 逐项判定

| ID / 原优先级 | 本轮判定 | 判定边界 |
|---|---|---|
| **B23-T06-C04 / P1** | **OPEN，已部分修复** | 产品、Linux/驱动/CUDA 的组件样板及 legacy v2 接口已具体化；“组件交集、不是 MPS 功能认证”已明确。但前轮要求的运行时接入路径仍未绑定，MPS 动态限额与静态 SM 分区的样板范围仍未显式分开。不得继续以“未给驱动/CUDA”概括本轮剩余问题 |
| **B23-T06-R05 / P1** | **CLOSED** | 正文 L125 与来源记录 L36 明确排除插件样板可任选 v3；固定实现支持 legacy 控制路径。检索范围内未发现其他正文/实际来源登记把驱动或工具的 v3 能力推成该插件兼容性 |
| **本轮新增问题** | **无；未新增 B23-T06-R06** | 运行时与功能范围问题已在第三轮 C04 关闭条件中列出，属于持续缺口，不重新编号；没有把仍保留的最低版本 unknown 当作新缺陷 |

### C04：哪些已补齐，哪些还未关闭

1. **产品与 OS/驱动/CUDA 条件已从泛指变为有限组件样板。** 正文 L125–126 均选择 A100-SXM4-40GB、Linux、CUDA 11、R525（≥525.53）及插件 v0.20.1；E01/E02 可核对产品与所引 A100 条件，E07 支持不把 R525/CUDA 11 误判为基本版本冲突。此处认可的是组件条件的选择与可追溯性，不是从 MIG 条件推出 MPS 动态限额已经认证。README 的 `~=384.81` 仍按原文口径记录，不将其正规化为 MPS 的功能最低版本；`toolkit ≥1.7.0` 应理解为该 README 的 nvidia-container-toolkit，而非 CUDA Toolkit 版本。
2. **接口与风险边界的修订有效。** 正文 L125 已指定 legacy v2，保留整卡、experimental、MIG 启用时插件不支持 MPS 的条件；来源记录 L36 同步。正文 L125 右栏明确“本样板是组件交集，不是 MPS 功能认证”，MPS 功能最低驱动/CUDA 仍 unknown。本轮不要求删除此 unknown，也不要求完整兼容矩阵或现场实测作为概念文章的关闭前提。time slicing 的节点级 replicas、与 MPS 互斥和无隔离口径与 E03 一致。
3. **运行时路径仍缺失，影响两行样板。** 正文 L125–126 的“README 前提”只列驱动、toolkit、K8s，未说明选择默认低层 `nvidia-container-runtime`，还是 README 所述非默认 runtime + RuntimeClass 路径。对正文与来源记录检索 `nvidia-container-runtime`、`RuntimeClass`、`runtimeClassName`、`containerd`、`CRI-O` 均无命中；正文 L217 的运行时基线链接只是相关知识入口，没有把其中某一路径绑定到这两行样板。E03 显式区分这些接入条件；安装 toolkit 本身不等于已经选定并配置 NVIDIA runtime。此项正是第三轮 C04 已列的剩余要求，不是新增验收门槛。
4. **“整卡 + v2”仍未界定所选 MPS 功能。** 正文 L105 已有等分显存和算力受限的通用插件描述，故不能说正文完全没讲限额；但 L125 的样板仅写“功能范围＝整卡共享”，L103 与 L137 仍给出可选静态 SM 分区，没有注明该选项不在这个 A100/R525/插件样板内。E06 表明 legacy v2 也区分动态限额和静态分区；E04 的原样插件启动并不启用静态分区，而是设置动态显存/active-thread 限额。因此排除 v3 不能同时视为已排除静态 SM 分区。这里要求补的是样板范围，不是断言 R525 一定不支持某功能，也不是要求作者证明所有历史功能最低版本。

**C04 最小剩余关闭条件**：在两条有限样板中明确采用的 NVIDIA runtime 接入路径，并将各自的 `sharing.mps` / `sharing.timeSlicing` 模式与该路径关联；MPS 样板明确仅采用 E04 对应的动态显存/active-thread 限额，把静态 SM 分区及 v3 列为非本样板。正文与来源记录同步后定向复核。可以继续保留 MPS 功能最低版本、完整产品矩阵、QoS/性能实测 unknown；不能只用“现场再核对”或“不是认证”替代样板自身的范围说明。

### R05：v3 残留与关闭依据

- 正文 L125 及来源记录 unknown #3（L36）已从接口任选改为：插件采用 legacy v2，通用 v3 能力不证明插件集成相容，v3 不纳入样板。结合 E04/E05，满足 R05 的核心关闭条件；不要求执行一次强制 v3 失败实验。
- 检索 `knowledge/`、`sources/` 与本任务来源记录中的 MPS v3、v2/v3、Legacy v2、协议变量及显式 v3 表述。正文 L179 仍说核对“MPS 的 v2/v3 接口与连接设置”，但它是通用选择检查项，没有再声称插件 v0.20.1 可任选；与 L125 的明确排除合读，不构成继续开放 R05 的反证。
- 来源记录 L8/L61、实际 registry L5718 仅描述上游文档区分两种接口且未绑定 CUDA 版本，不是插件兼容声明。来源记录 L19/L66 所述静态 SM 分区属于 C04 的功能范围问题，不是由驱动 v3 推出插件兼容。
- 历史初审/复核报告内的旧措辞是发现记录，不算当前适用声明残留，也不得为关闭问题而追改。本轮未发现相关新回归；R05 关闭不等于证实 v3 与该插件不可能集成，更不证明选定 R525 具有 v3 能力。

## 结论

**C04（P1）仍 OPEN；R05（P1）CLOSED；本轮无新增 R06。T05-06 仍不可声明审阅通过。**

此次补入驱动/CUDA 的有限组件样板、排除插件任选 v3、保留 MPS 功能最低版本 unknown 都是有效修订。C04 的剩余阻塞收敛为既有关闭条件中的运行时路径与动态/静态功能范围绑定，不再重复要求作者证明 MPS 历史最低版本或开展硬件认证。前轮已关闭项（包括 R04）不作全面重审；本轮未见 H100/H200 冲突行重新作为有效样板采用。

## 证据边界与检查

- 可变文档仅代表本轮观察；MIG Deployment 的 A100 条件不是 MPS 功能支持表，CUDA 向后兼容不是插件认证，固定插件实现也不是实际启动/限额生效的证明。未建立全部 SKU、OS 发行版、CUDA 小版本、container runtime、驱动与插件的完整兼容矩阵。
- GitHub 网页入口读取失败后改用连接器按固定 commit 读取有界行段；没有以失败入口或搜索摘要认定缺乏支持。上游源码与命令仅供只读核验，未执行其中任何部署、启动、配置或故障操作。
- 未安装驱动/Toolkit/插件，未连接集群，未创建 MIG/vNPU，未启动 MPS、改变协议、配置 replicas、提交 GPU/NPU 负载或故障注入；不证明隔离、QoS、回收或性能，也不产生新的执行授权。
- `PYTHONDONTWRITEBYTECODE=1 make check`：**PASS，100 content entries / 469 sources**；只检查结构与本地文件链接，不验证远程来源语义、技术正确性或实际兼容性。报告不属于知识正文目录，此检查也不等于对报告结论的技术认证。
- 未运行 `make build`：它会写 `build/catalog.json`、`build/catalog.md`，违反本轮“只创建指定报告”的更具体限制。未改 `src/kb/`，未运行单元测试；未追加来源登记或修改问题/计划状态。
- 开始时正文、registry、领域索引及其他 Batch 23 报告已有工作区改动，不归为本轮写入；本轮只新增本报告。模型/effort 保持 unknown，内容复核、执行模型认证与硬件验证三者分开记录。
