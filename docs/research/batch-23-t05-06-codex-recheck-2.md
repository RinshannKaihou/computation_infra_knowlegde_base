# Batch 23 · T05-06 第二轮定向复核

## 审阅元数据

- 任务：T05-06「加速器共享与租户隔离机制」；承接[上一轮复核](batch-23-t05-06-codex-recheck.md)，核验 C01、C04、R01、R02、R03 的修订及其回归。沿用独立审阅者角色，未参与作者修订，未派发子代理。
- 日期：2026-10-18，Asia/Shanghai（UTC+08:00）。
- 实际执行模型：`unknown`；实际 reasoning effort：`unknown`。本轮接口未暴露可核验的实际部署模型标识和 effort；不以仓库约定、前轮记录或角色连续性替代实际模型证明，不追改历史记录。
- 方法：重新读取正文、来源记录、registry 相关条目、前轮关闭条件及任务 acceptance；重新打开 NVIDIA 精确页面和 Ascend 固定 commit 的 release notes、HDK 产品表、模板、静态/动态文档。作者说明只作为定位线索，不作为关闭证据。
- 写入范围：仅新增本报告；不修改正文、来源记录、registry、plans、其他报告或生成产物。`CLOSED` 只关闭相应内容问题，不代表整篇通过、功能最低版本已确定或硬件已验证。

### 本地证据定位

以下“正文”指 [accelerator-sharing-and-isolation.md](../../knowledge/05-cluster-platform/accelerator-sharing-and-isolation.md)；“来源记录”指 [batch-23-t05-06-sources.md](batch-23-t05-06-sources.md)；“registry”指 [sources/registry.yaml](../../sources/registry.yaml)。行号为本轮读取的原文件坐标。

| 材料 | 本轮重点位置 |
|---|---|
| 正文（236 行） | L23、L39、L66–72、L84–105；有限样板 L119–129；路线表 L133–140；HDK L148–156；隔离边界 L164–170；选择 L176–180；验证 L194–202；待确认 L236 |
| 来源记录 | L7–10、L16–30、L34–40；建议登记区 L93–127（与实际 registry 区分） |
| registry | MindCluster 快照 L235–255；MIG/MPS/共享 L5702–5734；MIG Deployment L5774–5784；HDK L5796–5809 |
| [任务 acceptance](../../plans/full-coverage-backlog.yaml) | T05-06 L5603 起，尤其 L5620–5625；不放宽 GPU/NPU 共享必交要求，不修改计划状态 |

审阅快照 SHA-256：正文 `e3f74d5d04b73d2bc385956a0025aedf36ca963fd84313ea37d5f11a974bc25f`；来源记录 `2b0ce2a58a9ec13180c3500434a17c63f739a116f179ac0dc549d19536bb72c3`；registry `a336ce6edc17521e79c164d254c2fb272dde9cb60aea8b978ac5018262cce62c`。它们标识本地审阅对象，不是远程材料的字节完整性认证。

### 本轮重新打开的关键上游材料

E01–E06 均读取于 Ascend commit `44385c13d7b1d87def35f1604e8be4d16de6ca4e`；E11 固定于 NVIDIA commit `487d7a93894b0f3ad08097169593972eb3ca8206`。GitHub 行号来自按原文件行段读取，不把网页转换后的行号用作 GitHub 锚点。

| 编号 | 精确页面 / 文件 | 核验位置 |
|---|---|---|
| E01 | [MindCluster release_notes.md](https://github.com/Ascend/mind-cluster/blob/44385c13d7b1d87def35f1604e8be4d16de6ca4e/docs/zh/release_notes.md) | 产品版本信息；L29–36 表 1；CANN/HDK 兼容表。表 1 对不同产品给出不同 HDK，不能横向拼用 |
| E02 | [HDK 特性说明](https://github.com/Ascend/mind-cluster/blob/44385c13d7b1d87def35f1604e8be4d16de6ca4e/docs/zh/scheduling/04_usage/02_virtual_instance/00_virtual_instance_with_hdk/01_description.md) | 产品支持表，特别是 L107 起 Atlas 800T A2（24 AICore）的物理机→vNPU→容器、静态/动态支持行；使用约束 |
| E03 | [HDK 虚拟化模板](https://github.com/Ascend/mind-cluster/blob/44385c13d7b1d87def35f1604e8be4d16de6ca4e/docs/zh/scheduling/04_usage/02_virtual_instance/00_virtual_instance_with_hdk/03_virtualization_templates.md) | 表 1 的 A2 训练系列（24 AICore）两种模板与模板查询说明 |
| E04 | [创建 vNPU](https://github.com/Ascend/mind-cluster/blob/44385c13d7b1d87def35f1604e8be4d16de6ca4e/docs/zh/scheduling/04_usage/02_virtual_instance/00_virtual_instance_with_hdk/04_static_vnpu_scheduling/01_creating_vnpu.md) | 创建方法；“配置 vNPU 恢复状态”：1 开启、0 关闭、默认开启 |
| E05 | [静态挂载 vNPU](https://github.com/Ascend/mind-cluster/blob/44385c13d7b1d87def35f1604e8be4d16de6ca4e/docs/zh/scheduling/04_usage/02_virtual_instance/00_virtual_instance_with_hdk/04_static_vnpu_scheduling/02_mounting_vnpu_static.md) | 方式二 Ascend Docker Runtime 的表 1：静态 `ASCEND_RUNTIME_OPTIONS` 必选且包含 `VIRTUAL`；方式三的静态/动态互斥说明 |
| E06 | [动态 vNPU 调度](https://github.com/Ascend/mind-cluster/blob/44385c13d7b1d87def35f1604e8be4d16de6ca4e/docs/zh/scheduling/04_usage/02_virtual_instance/00_virtual_instance_with_hdk/05_dynamic_vnpu_scheduling/01_dynamic_vnpu_scheduling_inference.md) | L13–40 的 Docker 前提/参数；L47–75 的 K8s 前提；表 3 L149–180 的切换与生命周期限制；L286–288 的集群推理任务互斥/单机任务范围 |
| E07 | [MIG Deployment Considerations](https://docs.nvidia.com/datacenter/tesla/mig-user-guide/deployment-considerations.html) | GPU/CUDA/驱动表；System Considerations；Application Considerations。该页确实写有正文复制的三组数字，但 H100/H200 行与 E12/E13 存在冲突，见 R04 |
| E08 | [MIG Concepts](https://docs.nvidia.com/datacenter/tesla/mig-user-guide/concepts.html) | Terminology；Partitioning → Compute Instance 明确每个 CI 有专属 SM、共享父 GI 的显存/引擎；不是从 Table 3 反推 CI |
| E09 | [MPS Overview](https://docs.nvidia.com/deploy/mps/index.html) | 重定向至 latest/index.html；Legacy MPS v2 与显式 opt-in 的 v3；不是某个已选定 CUDA/驱动版本的证明 |
| E10 | [When to Use MPS](https://docs.nvidia.com/deploy/mps/when-to-use-mps.html) | System/Application Considerations；Client-Server Connection Limits；Static SM Partitioning 的 v2/v3 不同启动/管理方式及限制 |
| E11 | [k8s-device-plugin README](https://github.com/NVIDIA/k8s-device-plugin/blob/487d7a93894b0f3ad08097169593972eb3ca8206/README.md) | Prerequisites L70–80；Shared Access L358 起；time-slicing；With CUDA MPS L516 起（experimental、MIG 不支持、仅 full GPU、等分限额） |
| E12 | [CUDA 12.0.0 Release Notes](https://docs.nvidia.com/cuda/archive/12.0.0/cuda-toolkit-release-notes/index.html) | §1.1，Table 2（minor-version compatibility 最低驱动）与 Table 3（toolkit 配套驱动），区分两种口径 |
| E13 | [450.80.02 驱动 Release Notes](https://docs.nvidia.com/datacenter/tesla/tesla-release-notes-450-80-02/index.html) | §1.1 Software Versions；§3 API Support 与 Supported NVIDIA Data Center GPUs；该版列 CUDA 11.0 和 A100 等产品，不列 Hopper/H100/H200 |
| E14 | [CUDA Minor Version Compatibility](https://docs.nvidia.com/deploy/cuda-compatibility/minor-version-compatibility.html) | CUDA 11/12/13 的驱动范围表与受限特性说明；用于交叉核验，不作为全机型 MIG 支持表 |
| E15 | [MIG Device Names](https://docs.nvidia.com/datacenter/tesla/mig-user-guide/mig-device-names.html) | R470 命名边界与 R570 枚举分支，确认正文没有恢复为统一 UUID 规则 |

另重开了 [v26.1.1 tag ref](https://api.github.com/repos/Ascend/mind-cluster/git/ref/tags/v26.1.1) 与其 [annotated tag 对象](https://api.github.com/repos/Ascend/mind-cluster/git/tags/387a7f2b5f9ddfdbcdff0d8c85386fc68e2fe7fb)，核对指向上述 commit。只确认对象关系，不认证签名。NVIDIA 可变页按本轮观察记录，不以页脚更新日期代替软件版本。

## 逐项复核表

| ID / 原优先级 | 判定 | 本地证据位置与上游核验 | 剩余要求 / 关闭边界 |
|---|---|---|---|
| **B23-T06-C01 / P1** | **CLOSED** | 正文 L127、L148–152；来源记录 L25、L34；registry L235–255、L5796–5809。E01 给出产品版本 26.1.0、CANN 9.1.0 和按产品划分的 HDK 配套；E02/E03 将 Atlas 800T A2（24 AICore）、物理机容器场景及 `vir06_1c_16g`/`vir12_3c_32g` 连起来；E04/E05 支持静态生命周期前提 | 满足前轮“至少一个有官方配套依据的组合/适用范围”，不再因缺少全部功能最低版本而保持本项 blocked/open。须按下文的**产品对应关系**解读，不能把为其他产品列出的 RC 版本直接配给 A2；跨 vNPU 故障隔离/QoS 和功能最低固件/CANN 仍 unknown |
| **B23-T06-C04 / P1** | **OPEN** | 正文 L91、L102–105、L119–126、L179；来源记录 L8、L19–22、L35–36；registry L5713–5734、L5774–5784。E07 证实新增 MIG 数字和 Linux/IPC/NCCL 限制确有出处；E09/E10 证实 legacy v2 / 显式 v3、连接数条件；E11 证实插件限制。但 E07 的 H100/H200 驱动行未被消歧，且 MPS 仍未绑定选定功能/控制接口与具体软件栈 | 不能关闭。需排除 R04 的冲突组合；为 MPS 选定至少一个可核查的产品、Linux/驱动/CUDA、v2 或 v3、功能口径与插件模式交集。time-slicing 也须绑定至少一个硬件/软件前提下的插件样板，而非只有策略摘要和“README 无版本表”。无需穷举全矩阵 |
| **B23-T06-R01 / P2** | **CLOSED** | 正文 L23、L84–89、L135–138、L176、L198–202；来源记录 L17。SM 行现明确 CI 有专属 SM slice、共享父 GI 显存/引擎，与 E08 的 Compute Instance 说明一致；摘要未否定 CI 专属计算资源，选择流程也已同向修正 | 最小验证未再将“CI 不具备独立 GI 的显存/故障边界”误作“CI 没有专属 SM”；仍是未执行的验证设计。没有把专属 SM 升级成同 GI 内独立显存/QoS/任意故障隔离 |
| **B23-T06-R02 / P2** | **CLOSED** | 正文 L128、L152、L154；来源记录 L25；registry L5809。E04 的恢复状态默认开启与 E06 的动态使用前关闭要求相互印证；E05/E06 参数表分别要求静态包含 `VIRTUAL`、动态不包含，动态可选 `NODRV` | 所缺必要前提已补齐，来源记录主张表与实际 registry 同步。上述环境变量结论按 Ascend Docker Runtime 分支理解，不当作原生 Docker 或所有 K8s 组件的统一配置命令；L201 的回收/残留检查仍未执行，不构成异常销毁成功证明 |
| **B23-T06-R03 / P2** | **CLOSED** | 正文 L128、L156、L178；来源记录 L25；registry L5809。E06 L286–288 的约束针对同一集群同时运行的推理任务，不限于单任务内部；表 3 分别规定节点切换前删除已有任务，以及 K8s 与 Docker 生命周期操作不能混用 | 现已恢复集群级作用域，并分开节点切换和生命周期管理边界；没有扩大到不同集群不能分别采用不同模式。原文切换条件是“动态与非动态”之间，正文静态↔动态是其子场景，不应被反向解读为整卡↔动态无需清理 |

### C01 的配套链与保留未知

E01 表 1 实际列出：Atlas 350→HDK 25.7.RC1；Atlas 950 SuperPoD→25.1.RC1；Atlas 850E/650E→25.6.RC1；**其他产品→26.1.0**。将 E01 的“其他产品”行与 E02/E03 的 A2 支持行结合，可核查的有限样板是：

**该固定 tag/commit 文档中的 MindCluster 产品版本 26.1.0 + CANN 9.1.0 + HDK 26.1.0（其他产品行）+ Atlas 800T A2（24 AICore）+ 静态 vNPU + 上述两档模板之一 + 对应静态组件/挂载条件。**

这是同一固定文档快照内配套表与功能表的组合读取，不是把三种 RC 任意连给 A2，也不是宣称 tag 名就是二进制产品版本。正文已提供“按产品、见 release notes 表”的限制和近邻链接，故没有实际声明 A2 支持那些 RC；建议后续把 A2 对应的 HDK 26.1.0 直接写出以减少误读，但不将可沿精确表核查的省略重新列为 P1 阻塞。

release notes 不单列该虚拟化功能的最低固件/CANN；本轮也未拆解 HDK 包的驱动/固件子版本。前轮明确不要求穷举最低版本，故不能仅凭这项剩余 unknown 否定已经形成的文档配套范围。跨 vNPU 故障/QoS 无证据的结论继续保持 unknown，不借软件配套表关闭。

### C04 尚未闭合的具体部分

1. **MIG：有出处不等于组合已消歧。** 正文忠实复制了 E07 的三行，不是作者把 R450/R525 抄反；Linux、R570 P2P、跨 GI IPC 与驱动层 MPS-on-MIG 等边界也有出处。但表内 H100/H200 + CUDA 12 + R450 下限与其他官方版本证据冲突，必须处理为来源冲突，不能列作已核对可用条件。A100/A30 与 B200 两行来源匹配，不代表本轮已核验其全部 SKU/Toolkit 小版本支持交集。
2. **MPS：名词已补，样板未选。** L125 的“Legacy v2 或显式 v3 二选一”准确，但仍没有选定其中一套作为样板，也没有将所选功能（动态百分比/显存上限或静态 SM 分区）、CUDA/驱动与插件 v0.20.1 绑定。E10 两套静态分区管理不同，静态模式还会忽略动态资源 provisioning；不能把可变文档里的可选功能整体视为该插件样板的已支持能力。连接数环境变量不是功能版本证明；L125 右栏仍明认版本交集未知。
3. **time-slicing：插件语义有证据，运行前提没有落为有限组合。** E11 的 README 不只有 sharing 段，还有 Prerequisites（驱动、container toolkit/runtime、Kubernetes）。正文 L126 只列 replicas/互斥/节点作用域；不要求 README 提供全 GPU/CUDA 矩阵，但仍须选一套可核查前提并绑定 `sharing.timeSlicing`，不能由“未给版本表”直接关闭原验收。

## 新增发现

### B23-T06-R04 · P1 · 将存在上游冲突的 H100/H200 驱动下限列作已核对样板

- **状态**：**OPEN**。这是本轮新增的具体回归；也是 C04 保持开放的原因之一，不重复计算成两份独立缺陷。
- **位置**：正文 L119 的“本轮已核对的条件”及 L124 的 `H100/H200 需 CUDA 12 + R450（≥450.80.02）`；关联来源记录 L35、L102 与 registry L5784 的交集仍 unknown 口径。
- **问题**：E07 当前页面的确如此列示，故不是简单转录错误；问题是正文把尚未解决的官方材料冲突转换成了正向适用条件。表前“不是支持矩阵/不能随意组合”不能排除该行明确允许的 H100/H200、CUDA 12、450.80.02 组合，表后整体 unknown 也没有明确撤回它。
- **交叉证据**：E12 的 §1.1 Table 2 对 CUDA 12.0.x 的 Linux x86_64 minor-version compatibility 给出 `≥525.60.13`，而 `450.80.02` 对应 CUDA 11.x；E14 同样区分 CUDA 12.x 的 R525 与 CUDA 11.x 的 R450 基线。E13 的 450.80.02 版本说明列 CUDA 11.0、A100 等支持产品，不列 Hopper/H100/H200。这足以说明 E07 一行不能独立建立正文所声称的可用交集；不依赖“年代看起来不对”的猜测。
- **影响**：读者可能依表把无法由本轮材料支持的驱动/硬件/Toolkit 组合当作 MIG 部署前提，背离原 C04 对“冲突组合不得宣称适用”的要求。
- **关闭条件**：明确记录 E07 的待消歧冲突并撤回该行的可用下限承诺；选择具体 GPU/SKU、Toolkit 与驱动版本，用对应硬件支持和软件兼容材料建立一个不冲突的有限样板。不要直接交换 A100/H100 两行，也不要只把 R450 改成 R525 后便宣称整个 H100/H200 系列都可用；CUDA 通用最低驱动不自动等于具体 GPU 的支持下限。若依赖 forward-compatibility 包，还须单独给出其基础驱动、硬件及功能范围依据。

本轮未增加 R05；MPS/time-slicing 未选定样板属于尚未解决的 C04，不另起重复编号。没有把保留的跨 vNPU 故障/QoS unknown 视为修订回归。

## 结论

**本轮五项复核：4 项 CLOSED（C01、R01、R02、R03），1 项 OPEN（C04）；新增 R04（P1）OPEN。T05-06 仍不可声明审阅通过。**

- NPU 共享分支已经有可核查的文档配套样板，C01 不再因“没有任何官方组合”而维持 `blocked_on_evidence / open`；未改 plans，也未把隔离/QoS unknown 改成已确认。
- NVIDIA 条件表相较前轮更具体，但 MPS/time-slicing 的有限样板仍未闭合，MIG 新增版本行还须处理 R04 的上游冲突；修订后需再次定向复核 C04/R04。
- 前轮已经关闭的 C02、C03、C05、C06、C07 不在本轮完整重审范围；本报告不把“未发现本次相关回归”升级为全篇重新通过。
- 模型/effort 核验仍受接口限制，即便内容问题关闭，也不能据本报告证明满足指定执行模型，更不能代替 GPU/NPU 实验验证。

## 证据边界

- Ascend 材料通过 GitHub 连接器按完整 commit 重新读取；长响应截断处对 A2 产品行、动态参数、表 3 和集群互斥段作了分段补读。未逐行审计 HDK/DCMI 或 runtime 实现，也未重做 vCANN-RT 全分支审阅。
- NVIDIA 以精确页面正文为依据；E12 为版本化归档，其他可变页面的当前内容不构成其历史状态证明。另一次尝试打开 520.61.05 驱动 release-notes URL 失败，未把失败结果当作否定支持的证据，也未采用搜索摘要推定最低驱动。
- E12/E13/E14 是本轮用于交叉核验的新证据入口，已在本报告精确列出；受“仅创建本报告”限制，未将它们追加到 registry。若作者据此修正文，应依仓库规则补登记后再建立新的适用声明。
- 未下载/安装驱动、HDK/CANN 或插件；未连接集群，未创建/销毁 MIG/vNPU、启动 MPS、配置共享、提交负载或故障注入。恢复功能、分配互斥、故障遏制、QoS、回收与残留均无本地实测结果；文档中的操作不构成执行授权。
- 执行 `PYTHONDONTWRITEBYTECODE=1 make check`：**PASS，100 content entries / 469 sources**；仅检查结构和本地链接。未运行 `make build`，因为它会写 `build/catalog.json` / `build/catalog.md`，违反本轮仅新增指定报告的限制；未改 `src/kb/`，未运行单元测试。
- 工作区开始时已有正文、registry、索引及其他 Batch 23 报告等变动；它们不是本轮写入。本报告只判断上述五项及本次修订相关新增发现，不对其他任务或整个 Batch 23 宣布通过。
