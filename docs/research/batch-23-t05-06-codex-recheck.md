# Batch 23 · T05-06 定向复核（recheck）

## 审阅元数据

- 任务：T05-06「加速器共享与租户隔离机制」；承接[初审报告](batch-23-t05-06-codex-review.md)，逐项复核 B23-T06-C01–C07，并检查修订引入的问题。未参与正文修订，未派发子代理。
- 日期：2026-10-18，Asia/Shanghai（UTC+08:00）。
- 实际执行模型：`unknown`；实际 reasoning effort：`unknown`。本轮接口未暴露可核验的实际部署模型标识和 effort，不能把约定名称或初审元数据当作本轮执行证明；不追改初审历史记录，也不声称本轮已满足指定模型核验要求。
- 方法：重新读取正文、作者来源记录、registry 对应条目和任务 acceptance；实开 NVIDIA 官方页面，通过 GitHub 连接器按完整 commit 读取 Ascend/NVIDIA 文件，并按原文件行段复核源码与关键约束。不是仅采信作者的修订说明。
- 写入范围：仅新增本报告；不修改正文、来源记录、registry、plans 或其他文件。
- 判定规则：`CLOSED` 仅关闭原发现对应的问题，不代表整篇通过、已建立完整支持矩阵或已完成硬件验证。新增回归单独编号，不重复计入原发现。

### 本地证据位置

下文“正文”指 [accelerator-sharing-and-isolation.md](../../knowledge/05-cluster-platform/accelerator-sharing-and-isolation.md)，共 232 行；“来源记录”指 [batch-23-t05-06-sources.md](batch-23-t05-06-sources.md)。行号为本轮读取时的原文件坐标。

| 文件 | 本轮核对范围 |
|---|---|
| 正文 | frontmatter；边界分层；NVIDIA 各路线及有限条件表；Ascend HDK/vCANN-RT 新节；选择、异常、验证与待确认项 |
| 来源记录 | 主张—来源表 L16–30、unknown L34–40、登记建议，尤其 HDK/vCANN-RT 与 `getMountPath` 定位 |
| [registry.yaml](../../sources/registry.yaml) | MIG/MPS/sharing L5702–5748；新增部署/错误恢复 L5774–5795；HDK L5796–5809；vCANN-RT L5810–5823；复用 runtime L5441–5450 |
| [full-coverage-backlog.yaml](../../plans/full-coverage-backlog.yaml) | T05-06 L5603 起，acceptance L5620–5625；未改任务状态或放宽验收 |

正文快照 SHA-256：`1a0e287585b50027b42d1b1b626c9115ab5225e0b29b9ba5e843318ee250d623`。来源记录：`df89e10449c9209c1ba33bc5b6050eca7884dbb02c76e5671f3ad09c8132e912`。registry：`c2f1fad836ddfa72105f54f028d6a094d0bc9107c9a36bc7bbbfefdd61bf4b25`。这些是本地审阅快照标识，不是远程文件完整性认证。

### 重新打开的关键上游证据

Ascend 以下文件均固定于 `44385c13d7b1d87def35f1604e8be4d16de6ca4e`；NVIDIA 插件 README 固定于 `487d7a93894b0f3ad08097169593972eb3ca8206`。NVIDIA 文档页按 2026-10-18 的本轮观察记录，不把观察日期当作驱动或 CUDA 版本。

| 编号 | 实开页面 / 文件 | 本轮核对位置与边界 |
|---|---|---|
| E01 | [HDK 特性说明](https://github.com/Ascend/mind-cluster/blob/44385c13d7b1d87def35f1604e8be4d16de6ca4e/docs/zh/scheduling/04_usage/02_virtual_instance/00_virtual_instance_with_hdk/01_description.md) | 原理、产品支持表、使用约束；产品表区分静态/动态及物理机/虚拟机场景；一个 vNPU 一个任务容器，不是跨 vNPU 故障/QoS 保证 |
| E02 | [HDK 虚拟化模板](https://github.com/Ascend/mind-cluster/blob/44385c13d7b1d87def35f1604e8be4d16de6ca4e/docs/zh/scheduling/04_usage/02_virtual_instance/00_virtual_instance_with_hdk/03_virtualization_templates.md) | 表 1 的产品、模板和 AICore/AICPU/内存字段；现场模板查询入口 |
| E03 | [创建 vNPU](https://github.com/Ascend/mind-cluster/blob/44385c13d7b1d87def35f1604e8be4d16de6ca4e/docs/zh/scheduling/04_usage/02_virtual_instance/00_virtual_instance_with_hdk/04_static_vnpu_scheduling/01_creating_vnpu.md) | 容器模式、创建参数、ID、配置恢复；配置恢复默认开启，0 为关闭 |
| E04 | [静态挂载 vNPU](https://github.com/Ascend/mind-cluster/blob/44385c13d7b1d87def35f1604e8be4d16de6ca4e/docs/zh/scheduling/04_usage/02_virtual_instance/00_virtual_instance_with_hdk/04_static_vnpu_scheduling/02_mounting_vnpu_static.md) | Docker Runtime 的 `VIRTUAL`；K8s 每 Pod 1 个、创建/销毁后重启插件、不支持故障重调度；模板到资源类型映射 |
| E05 | [动态 vNPU 调度](https://github.com/Ascend/mind-cluster/blob/44385c13d7b1d87def35f1604e8be4d16de6ca4e/docs/zh/scheduling/04_usage/02_virtual_instance/00_virtual_instance_with_hdk/05_dynamic_vnpu_scheduling/01_dynamic_vnpu_scheduling_inference.md) | Docker 段 L13–40；K8s 前提和参数；表 3 L121 起；L286–288 的集群静态/动态互斥与单机任务约束。截断的长响应已用原文件行段补读 |
| E06 | [vCANN-RT 特性说明](https://github.com/Ascend/mind-cluster/blob/44385c13d7b1d87def35f1604e8be4d16de6ca4e/docs/zh/scheduling/04_usage/02_virtual_instance/01_virtual_instance_with_vcann_rt/00_description.md) | 时分复用、产品支持表、需编译部署 vCANN-RT 的前提、推理/百分比/单 die/同策略约束；没有由此证明跨容器故障隔离 |
| E07 | [MIG Concepts](https://docs.nvidia.com/datacenter/tesla/mig-user-guide/concepts.html) | Terminology、Partitioning 的 CI 专属 SM 与共享显存/引擎；Table 3 的列名与 48。页面标注 2026-10-13 更新 |
| E08 | [GPU Memory Error Recovery and Response Flags](https://docs.nvidia.com/deploy/a100-gpu-mem-error-mgmt/error-recovery-and-response-flags.html) | Reset、Reboot、Drain and Reset；恢复动作与共同故障域。页面标注 2026-09-09 更新 |
| E09 | [MIG Device Names](https://docs.nvidia.com/datacenter/tesla/mig-user-guide/mig-device-names.html) | R470 命名分界、R570 枚举分界；不能把含混的示例括注当最低驱动矩阵。页面标注 2026-10-13 更新 |
| E10 | [MIG Deployment Considerations](https://docs.nvidia.com/datacenter/tesla/mig-user-guide/deployment-considerations.html) | OS/驱动表与驱动层 MPS-on-MIG 说明；页面驱动表本身不足以消解初审指出的产品/分支交集疑点。页面标注 2026-10-13 更新 |
| E11 | [MPS Overview](https://docs.nvidia.com/deploy/mps/index.html) | 本轮重定向到 `/deploy/mps/latest/index.html`；Legacy MPS v2 与显式选择的 v3 控制接口。页面标注 2026-09-09 更新 |
| E12 | [When to Use MPS](https://docs.nvidia.com/deploy/mps/when-to-use-mps.html) | 60 contexts 的连接设置；有限错误遏制；Locality Domains / Static SM Partitioning 的不同限制与 v2/v3 管理差异。页面标注 2026-09-09 更新 |
| E13 | [k8s-device-plugin README](https://github.com/NVIDIA/k8s-device-plugin/blob/487d7a93894b0f3ad08097169593972eb3ca8206/README.md) | Prerequisites、Shared Access、time slicing、MPS；核对至 MPS 等分限额段，不将 README 基础前提解释为所有特性支持交集 |
| E14 | [runtime `getMountPath` L536–L549](https://github.com/Ascend/mind-cluster/blob/44385c13d7b1d87def35f1604e8be4d16de6ca4e/component/ascend-docker-runtime/runtime/process/process.go#L536-L549) | 按固定原文件坐标读取；`virtualDavinciName` 分支提取编号并构造 `davinci` 路径 |
| E15 | [Ascend Device Plugin README](https://github.com/Ascend/mind-cluster/blob/44385c13d7b1d87def35f1604e8be4d16de6ca4e/component/ascend-device-plugin/README.md) | 发现、健康归因与分配功能；产品列表是资源监测支持，不替代虚拟化产品/版本条件 |
| E16 | [MIG Supported GPUs](https://docs.nvidia.com/datacenter/tesla/mig-user-guide/supported-gpus.html) | 机型与实例数支持表；不按架构代际扩推；页面标注 2026-10-13 更新 |

另经 [MindCluster annotated tag 对象](https://api.github.com/repos/Ascend/mind-cluster/git/tags/387a7f2b5f9ddfdbcdff0d8c85386fc68e2fe7fb)核对 `v26.1.1` 指向上述完整 commit；只核对对象关系，未认证签名。重开同 commit 的 [docs/LICENSE 开头](https://github.com/Ascend/mind-cluster/blob/44385c13d7b1d87def35f1604e8be4d16de6ca4e/docs/LICENSE)，其标题与新增条目的 CC-BY-4.0 标识一致；不据此宣称所有第三方素材均可再分发。

## 逐项复核表

| ID | 判定 | 证据 | 剩余问题 / 关闭条件 |
|---|---|---|---|
| **B23-T06-C01（P1）** | **OPEN（实质补齐，但未完全关闭）** | 正文 L127–129、L146–166 已交付 HDK 静态/动态及 vCANN-RT 的共享模型，不再仅列独占与 unknown。E01/E02 可核对产品与模板；E04/E05 支持每 Pod 1 个、静态插件重启/不重调度、动态 Volcano 参数、同模板、单机副本、退出销毁及异常重启残留等条件；E06 支持软切分限制。来源记录 L25–26、L34，registry L5796–5823 已登记两项新增来源，commit/路径可解析。正文 L162–165 仍诚实保留跨 vNPU 故障隔离和性能 QoS 未证实。 | **原关闭条件中的“选定型号/固件/CANN/plugin 官方条件”仍未满足**：正文 L127、L232、来源记录 L34 和 registry L5809 明认固件/CANN 条件未建立；尚无一个按具体产品、模式、模板和软件栈绑定的有限支持样板。文档资源组成也不能升级成已确认的强制 QoS。需补至少一个有官方配套依据的组合/适用范围，不必穷举全部最低版本；无法取得时保留该必交子项 `blocked_on_evidence / open`。不能因材料显著增加而放宽第五条验收。动态约束另见 R02/R03。 |
| **B23-T06-C02（P1）** | **CLOSED（原故障隔离过度承诺已撤回）** | 正文 L70、L84–89、L135–138、L172、L198、L205 已区分独立 GI、同 GI 内 CI、整卡 reset、驱动与主机故障；最小验证先分错误类别，不再把任意“触发错误”都判为 MIG 必隔离或 MPS 必传播。E07 的显存/引擎共享边界与 E08 的恢复动作支持此收窄。 | 原“任意错误互不影响”的问题关闭；不等于已交付某机型逐错误码保证，也未做故障注入。修订把 CI 的 SM 独立性否定过头，是另一维度的新回归，见 R01。 |
| **B23-T06-C03（P1）** | **CLOSED** | 正文 L164、L207 明确 runtime 环境变量/device cgroup 只是访问控制，要求调度器/插件分配记录与现场核对；L195 要同时记录两个租户的物理设备稳定身份，判断是否同卡，不能只比资源名。L194–195 与“整卡独占”分配前提结合，已把跨租户物理分配互斥纳入核对对象。 | 未把设计当作结果：这些记录尚未采集，不能声明独占已经验证。实际执行时，独占样板若出现相同物理身份的重叠分配，应判不满足互斥；共享样板则不能把同卡本身判成错误。 |
| **B23-T06-C04（P1）** | **OPEN** | 正文 L91 已撤回统一 `MIG-<UUID>` 的说法并提及 R470/R570；L117–129 新增已知/未知表，L105/L140 区分插件限制。E09 确认命名与枚举分支；E10 的驱动层支持与 E13 的插件层不支持 MPS-on-MIG 属不同层级。 | 条件表仍不是原要求的可核查有限样板：MIG 行仍为“支持表内机型、驱动支持”，最低交集整体未知；MPS 只在 L125/L175 列“v2/v3 接口”字样，正文没有说明 v2 legacy / v3 显式选择，也未选定功能/控制口径，更未建立与插件 v0.20.1 的交集。E11/E12 明确两套控制与静态分区管理存在差异。需分别绑定至少一组 MIG/MPS/time-slicing 的产品、OS、驱动/CUDA 适用条件及 plugin 模式；冲突组合继续排除，不要求完整全机型矩阵，但不能仅给 unknown 表就关闭本验收。 |
| **B23-T06-C05（P2）** | **CLOSED** | 正文 L103 已把 vGPU 不支持归回 locality domains，仅保留静态 SM 分区与 locality domains 不能并用，并明确不能反推静态分区一定支持 vGPU。与 E12 的两个 Limitations 小节一致。 | 无原问题剩余；不因此确认任何静态分区/vGPU 实际部署组合。 |
| **B23-T06-C06（P2）** | **CLOSED** | 正文 L72 标明 Table 3 为 Streams / MPS / MIG，分别保留 48 的 Max Partitions 与 60 的 client CUDA contexts；L102 补 `CUDA_DEVICE_MAX_CONNECTIONS=2` 及增大后减少可接入客户端的条件。没有再用“驱动层口径”统一消歧，明确不能合并为通用容量/租户/副本上限。E07 Table 3 与 E12 Client-Server Connection Limits 可复核。 | 两来源的版本/实现对应关系仍未对齐；这一 unknown 保留合理，不是一个已建立的 48→60 演进结论。 |
| **B23-T06-C07（P3）** | **CLOSED** | 正文 L168 与来源记录 L27 均指向 `getMountPath` L536–L549；E14 本轮按同 commit 原文件坐标重读，虚拟设备重命名分支确在此处。正文继续声明重命名不构成隔离证据。 | 来源记录提到的 L86–L93 已标为既有登记，而非本轮重命名证据；本轮不采信该旧范围支持重命名。原错误 L411–L421 未被继续用作现行定位。 |

### C01 的已确认边界与未闭合项

为避免把 OPEN 误读为“仍完全没有 NPU 共享内容”，本轮作如下拆分：

- **型号/模板/分配约束已有可核查材料**：例如 E01 的 Atlas 800T A2（24 AICore）产品项、E02 的 `vir06_1c_16g` / `vir12_3c_32g`，以及 E04 的模板到资源类型映射，足以支持有限产品范围的概念描述。不能因此自行拼出固件/CANN/plugin 兼容组合。
- **静态/动态资源生命周期已有部分官方语义**：静态预创建、配置恢复、插件重启与不支持故障重调度，动态创建/销毁、调度约束与重启残留都有对应材料。但静态任务释放不等于删除预创建 vNPU；动态任务删除也不证明设备清零、旧权限清除或数据不可恢复。
- **故障语义已正确收窄**：物理设备决定虚拟设备健康、动态支持故障重调度，不等于故障被隔离在单个 vNPU。跨 vNPU 故障隔离、带宽/算力 QoS 的强制保证仍 unknown。正文 L166 的软/硬切分隔离强弱比较也不能用作这些保证的替代证据。
- **仍有必交条件欠缺**：至少一个所选 NPU 共享模式的固件/CANN/plugin 配套条件尚未绑定；因此第三、第五条 acceptance 不能宣布全部完成。开放原因是支持条件证据不足，不是要求本次执行硬件实验。

## 新增发现

### B23-T06-R01 · P2 · CI 的 SM 边界被过度否定

- **位置**：正文 L137，路线对照表“SM 隔离”行的“CI 不独立”；对照 L87 的 CI 描述。
- **问题**：修订正确撤回了同 GI 多 CI 的独立显存/QoS/故障承诺，但将这一收窄写进 SM 行，变成 CI 没有独立 SM 资源。共享显存和引擎不等于共享全部计算切片。
- **依据**：E07 的 Partitioning / Compute Instance 明确各 CI 有专属 SM 资源，同时共享父 GI 的显存与引擎。不是由 Table 3 的 GI 隔离能力反推 CI，也不据此扩张到任意故障隔离。
- **关闭条件**：将 SM 行改为准确的 CI 专属计算切片描述；显存、带宽 QoS、错误隔离分别保留其边界。核对摘要、矩阵与最小验证没有再把“CI 不具备 GI 级隔离”简化成“CI 没有专属 SM”。不要求执行实验。

### B23-T06-R02 · P2 · 动态 vNPU 遗漏与静态模式不同的必要前提

- **位置**：正文 L128、L150–152、L175–176、L197；来源记录 L25 与 registry HDK notes 的动态条件摘要。
- **问题**：静态段介绍可开启 `vnpu-cfg-recover`，紧接的动态段却只列两个环境变量和退出销毁，没有写出动态使用前须关闭恢复功能。另未区分静态挂载须含 `VIRTUAL`、动态 Docker 场景反而不能含 `VIRTUAL`。读者可能把相邻静态配置沿用于动态模式，尤其在切换与重启回收设计中。
- **依据**：E03“配置 vNPU 恢复状态”说明默认开启；E05 Docker 段 L21 明确动态须关闭恢复，L37–40 的参数表限定动态 `ASCEND_RUNTIME_OPTIONS` 可选 `NODRV` 而不能包含 `VIRTUAL`。E04 的静态要求正好相反。这是已取得材料中的明确前提，不应留作未知。
- **关闭条件**：按 Docker 静态/动态分别写清恢复状态与环境变量语义；在切换/回收验证中核对实际模式、恢复状态和残留，不把该要求未经证据扩推为所有 K8s 组件的统一配置命令。来源摘要同步准确保留必要前提，仍不声称异常销毁一定成功。

### B23-T06-R03 · P2 · 静态/动态 vNPU 禁止混用的集群作用域被收窄

- **位置**：正文 L150、L174 的“同一集群任务中混用”；来源记录 L25、registry L5809 的简写。
- **问题**：当前表述容易被读成“单个任务里不能同时使用静态/动态”，从而允许在同一集群分别投递两个模式的任务。材料要求的边界更宽，不只是单任务内部混用。
- **依据**：E05 原文件 L286–288 明确针对集群同时运行的多个推理任务，禁止同时存在使用静态 vNPU 的任务和使用动态 vNPU 的任务；同页表 3 还分别规定切换需删除已有任务、K8s 的自动创建/销毁不能与 Docker 操作混用。这些限制不能由“每 Pod 一个”替代。
- **关闭条件**：明确写为“在所引集群推理场景，同一集群不能同时存在静态与动态 vNPU 任务”，分开说明节点切换和 K8s/Docker 生命周期管理不可混用；不要扩大成不同集群永远不能各用一种模式。正文、选择表和来源摘要保持相同作用域。

## 结论

**T05-06 目前不可声明审阅通过。**

- 原 7 项：**5 项 CLOSED（C02、C03、C05、C06、C07），2 项 P1 仍 OPEN（C01、C04）**。
- 本轮新增 **3 项 P2 OPEN（B23-T06-R01–R03）**，须修订并定向复核。
- NPU 共享模型相较初审已有实质交付；不能再说只有独占说明。但至少一个官方支持组合仍未闭合，因此必交子项继续按 `blocked_on_evidence / open` 对待，不以独占/unknown/资料计划代替共享模型验收。本报告不改 plans 状态。
- 完成上述修订后方可重新判断内容审阅；本轮模型/effort 仍无法由接口核验，应另保留此元数据限制。即使内容问题全部关闭，也不等于真实 GPU/NPU 验证通过。

## 证据边界

- 本轮重新打开了表列关键材料。最初通过普通 Web 通道读取四个 Ascend raw URL 返回 Cache miss，之后均由 GitHub 连接器按同一完整 commit 取得内容；没有把失败请求当成材料不存在，也没有仅依据搜索摘要关闭问题。
- GitHub 长文件响应有截断，已对本次判定所需的产品表、静态限制、动态参数/场景/集群互斥及源码函数分段补读；没有宣称逐行审计全部实现。未追踪 HDK/DCMI 销毁实现、固件行为或 vCANN-RT 内部强制机制。
- 未安装组件、未连接集群、未创建/销毁 MIG 或 vNPU、未启动 MPS、未提交共享负载、未进行故障注入或权限旁路测试。官方错误隔离、调度恢复与本地实验验证是不同证据层级；本报告不授予执行授权。
- 未建立完整机型/驱动/固件/CANN/plugin 支持交集，未解决可变 NVIDIA 页面间的全部数字/驱动差异，未验证租户公平性、尾延迟、带宽 QoS、设备清零或跨租户保密性。缺少材料不等于厂商一定不支持。
- 执行 `PYTHONDONTWRITEBYTECODE=1 make check`：**PASS，100 content entries / 469 sources**；仅证明结构及本地链接。未运行 `make build`，因为会写 `build/catalog.json` / `build/catalog.md`，违反本次只允许创建报告的限制；未改 `src/kb/`，未运行单元测试。
- 工作区原有正文、registry 和其他 Batch 23 文件变动；它们不是本轮写入。本轮不对相邻任务或整个 Batch 23 宣布通过。
