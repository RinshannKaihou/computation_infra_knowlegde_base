---
id: cluster-platform.contention-capacity-validation
title: 多租户争用、公平性与容量验证
type: procedure
domain: cluster-platform
status: draft
platforms: [nvidia, ascend]
source_refs:
- src.kueue.fair-sharing-v0.19.0
- src.kueue.admission-v0.19.0
- src.kueue.cluster-queue-v0.19.0
- src.kueue.job-lifecycle-v0.19.0
- src.slurm.docs-24.11.7
- src.slurm.sshare-24.11.7
- src.slurm.gres-tres-cgroup-24.11.7
- src.mlcommons.storage-rules-v2.0
- src.ascend.mind-cluster-v26.1.1
- src.ascend.ascend-device-plugin-44385c13
- src.ascend.virtual-instance-hdk-44385c13
- src.ascend.virtual-instance-vcann-44385c13
- src.nvidia.k8s-device-plugin-sharing-v0.20.1
- src.nvidia.mps-docs-2026-10-18
- src.nvidia.mig-user-guide-2026-10-18
updated_at: "2026-10-18"
applicability:
  environment_refs: []
  notes: "未建立环境档案。方法以 Kubernetes v1.32（快照）/Kueue v0.19.0（commit 911a822a）与 Slurm 24.11.7（归档）为固定样板；实际队列配置、共享模式与负载条件须在目标环境补齐，不能据此认定适用。"
verification:
  status: not_verified
  evidence_refs: []
  notes: "尚未部署 Kueue/Slurm、未提交任务、未运行两租户对照；以下为可审查的验证设计，不是已执行结果。"
summary: 把设备共享与主机/网络/存储争用关联到容量记录、队列公平性和应用 SLO，给出单租户基线到两租户并发、限额与恢复的对照方法；强调利用率与总卡数不能单独表示可用容量。
related_ids:
- cluster-platform.accelerator-sharing-and-isolation
- cluster-platform.admission-and-placement
- cluster-platform.idle-resource-job-waiting-triage
- cluster-platform.device-resource-chain
- cluster-platform.kubernetes-job-lifecycle
- cluster-platform.slurm-jobs-and-device-resources
- data-storage.storage-workload-baselines
---

# 多租户争用、公平性与容量验证

> 范围：Kubernetes v1.32 文档快照、Kueue v0.19.0（commit `911a822a`）、Slurm 24.11.7 归档，以及 2026-10-18 观察的 NVIDIA 共享文档。本文是验证设计，**尚未在任何环境执行**；队列名称、权重、共享模式与阈值均为待填字段，不得当作现成配置。

## 目标与触发条件

当出现以下任一情况时进入本流程：

- 新租户要求共享现有 GPU/NPU 池，需要判断“还有多少可承诺容量”。
- 两个租户同时运行后出现吞吐下降、尾延迟上升或排队变长，需要区分“配额不足”“设备争用”“主机/网络/存储瓶颈”。
- 调整了共享模式（整卡、MIG、MPS、time slicing、vNPU）或队列权重，需要验证改动是否达到预期。
- 需要回答“公平性是否达标”，但手头只有 GPU 利用率或总卡数。

目标不是证明“集群很忙”，而是产出一份可复核的记录：**容量如何记账、争用首先出现在哪一层、公平性用什么口径计算、哪些结论仍是未知。**

## 适用范围与前置条件

| 项 | 要求 |
|---|---|
| 平台 | Kubernetes + Kueue 或 Slurm；两者分别组织，术语不互译 |
| 固定版本 | Kubernetes v1.32 快照、Kueue v0.19.0、Slurm 24.11.7；NVIDIA 文档记录观察日期 |
| 共享模式 | 明确当前是整卡独占、MIG、MPS、time slicing 还是 Ascend 虚拟设备；未确认的模式按未知处理 |
| 负载 | 固定镜像/模型/数据集/输入规模、并发与时限；训练与服务分别定义“有效产出” |
| 观测 | 能读取队列/配额、Pod/Job 状态、设备分配、主机压力、网络与存储指标 |
| 权限 | 只读观测为主；变更共享模式或限额须另行授权，本文不授予执行权限 |
| 环境档案 | 当前为空；缺少硬件、驱动、CANN、插件与拓扑记录时，结果只能作为方法演示 |

平台条件必须分开记录：Kueue 的配额、借用、抢占与公平共享是 Kueue 语义；Slurm 的分区、QOS、association、TRES 与 FairShare 是 Slurm 语义。**不因为都叫“队列”就认为行为相同。**

## 需要的证据

| 证据 | 采集范围或定位 | 用途 | 缺失时如何处理 |
|---|---|---|---|
| 容量资源向量 | 每类资源：加速器型号/profile、CPU、内存、本地盘、网络带宽、存储容量与 IOPS | 判断“可用容量”而不是“卡数” | 缺项标注未知，不补默认值 |
| 队列/配额 | Kueue ClusterQueue/LocalQueue 的配额、borrow/lending、preemption、stopPolicy；Slurm Partition/QOS/Association 的 TRES 限额 | 区分“配额挡住”与“资源不够” | 记录为未取得，不能假定无限 |
| 拓扑与碎片 | 节点/机架/rail、MIG profile 布局、NUMA、设备亲和 | 解释“总数够但放不下” | 保留碎片未知 |
| 保留与余量 | 系统预留、daemon 占用、故障预算、headroom | 计算可承诺容量 | 未记录时不承诺容量 |
| 任务需求 | 每任务资源向量、并发、时限、优先级、可重排队性 | 计算队列需求与公平份额 | 用实测申请值，不用峰值猜测 |
| 共享模式证据 | MIG 实例/profile、MPS server 与客户端、time slicing replicas、Ascend 虚拟设备 | 判断隔离边界与超卖倍数 | 模式未知则争用结论不可归因 |
| 应用指标 | 吞吐、等待时间、完成率、失败/取消、训练 step 时间、推理 TTFT/TPOT/尾延迟 | 计算公平性与 SLO | 明确分母与截尾，不混用成功/失败样本 |
| 主机/网络/存储 | CPU throttling、内存压力、NUMA 命中、NIC 计数与重传、存储时延/带宽 | 找到“首个受影响边界” | 缺层则不做跨层因果判断 |
| 时间线与身份 | 统一时钟、提交/开始/就绪/稳态/结束时间点、run/attempt、实际节点与设备映射 | 判定“首个”变化与因果顺序；确认两租户负载实际重叠 | 缺时间线时只报并列变化，不排序、不归因 |
| 变更记录 | 对照前后的队列、限额、共享模式与负载差异 | 保证单变量对照 | 多变量同时变化时结论降级 |

容量记录建议使用如下字段（每租户、每队列各一份）：

```text
资源向量: {加速器型号/profile/副本, CPU, 内存, 本地盘, 网络, 存储}
队列/配额: {硬配额, 借用上限, 权重, 抢占策略, 停止策略}
拓扑/碎片: {可用节点, 机架/rail, MIG 布局, NUMA, 设备亲和}
保留/余量: {系统预留, 故障预算, headroom}
任务需求: {单任务向量, 并发, 时限, 可重排队}
失效预算: {允许的 SLO 违约时长/比例, 允许的失败率}
```

**设备利用率或总卡数不能单独表示可用容量**：利用率不区分“被有效使用”与“互相拖慢”；总卡数不包含 profile 形状、碎片、保留与网络/存储约束。

## 步骤与判断分支

| 步骤 | 检查或动作 | 运行影响 | 预期证据与解释 | 下一步 |
|---|---|---|---|---|
| 1 | 固定定义：租户、队列、负载、有效产出、SLO 分母、噪声带 | 无 | 形成一份可复现的对照清单 | 定义不清则停止 |
| 2 | 建立容量记录与机制映射（上表字段 + 租户→队列/association + 初态控制方案） | 只读 | 能回答“配额、形状、余量、故障预算各是什么”；说明初态如何建立（匹配预置历史、交换顺序的配对轮次，或按各轮历史预测准入顺序）；Slurm 还需核验 `PriorityType`/Fair Tree、真实 association、QOS、`TRESBillingWeights` 与 `PriorityWeightFairshare` 等**有效优先级权重**，以及 A/B 作业的实际因子贡献；未配置计费权重时 Raw Usage 是 CPU-seconds 而非 GPU 物理服务量 | 缺关键项、初态不可审查或公平因子无有效贡献时，只做资源/SLO 观察，不据等待差异判公平策略 |
| 3 | 单租户基线 A：只运行租户 A，记录吞吐/时延/资源使用 | 占用共享资源 | 得到 A 的无争用基线；记录重复次数与噪声带；**基线自身不可重复则不进入并发阶段** | 先固定环境、补重复或停止 |
| 4 | 同租户重复 A：相同负载再跑 | 同上 | 估计噪声带；**只有基线自身差异落在预登记噪声带内才进入下一步**；超出时固定条件、补重复或停止 | 不稳定则停止/补采，不能“带病并发” |
| 5 | 单租户基线 B（异构负载必需） | 占用共享资源 | 得到 B 的独立参照。若 A/B 负载可比较，登记相同有效工作单位、目标份额与资源请求；若异构，分别用各自归一化退化/SLO 评价，不把不同模型 step 或请求直接求份额 | 缺 B 基线时不做份额比较 |
| 6 | 两租户并发：A+B 同时提交，确认应用负载实际重叠 | 生产影响需授权 | 预登记共同分析窗口、采样间隔、时间戳误差与各层相对基线的变化判据；记录开始/就绪/稳态时间点、run/attempt、实际节点/设备映射。充分观测下未检出显著退化 → 记“给定负载/窗口下未观察到显著退化”；采集缺失或分辨率不足 → “证据不足无法排序”；两者不能合并，也不能写成零干扰 | 不把候选边界直接当根因；超出时序分辨能力时保留并列候选 |
| 7 | 隔离/限额（按控制层分支） | 配置变更，可能中断任务 | 先声明改变的是哪一层：准入/并发上限、运行期 GPU 限额、硬件分区、主机/网络/存储控制。为所选控制写清“参数/对象 → 生效时机与支持条件 → 实际生效证据 → 不满足时停止或降级”；每轮只改已登记参数，记录实际并发、设备身份与资源形状；切换共享模式或 profile 时重建基线 | 无可用观测时不得作该层隔离因果结论；若改善只来自总并发下降，标为策略权衡 |
| 8 | 恢复：按已登记的安全退出路径释放 B，确认 A 回到基线，再重新准入 B | 可逆性取决于退出路径 | 资源回收、账本一致、MPS server/client 状态、新任务进展；MPS 不得以未同步终止方式释放 | 不能安全退出则保持隔离并停止 |

Kueue 与 Slurm 的观测入口分别组织：

| 维度 | Kubernetes/Kueue | Slurm |
|---|---|---|
| 准入与等待 | Workload 条件与事件、ClusterQueue/LocalQueue 状态、pending 数量 | 作业状态与 reason、分区可用节点、`squeue` |
| 配额与借用 | ClusterQueue 的配额/借用/抢占配置与用量字段 | Partition/QOS/Association 的 TRES 限额与用量 |
| 公平性 | Admission Fair Sharing 的 `status.fairSharing`（consumedResources、weightedShare、lastUpdate） | `sshare` 的 Raw/Norm Shares、Raw/Effectv Usage、FairShare、Level FS |
| 设备分配 | 资源名（整卡/MIG profile/replica）与 Pod 分配 | GRES/TRES 分配、`SLURM_JOB_GPUS`、cgroup 约束 |
| 回收 | Workload/Job 完成与资源释放 | 作业结束、Epilog、节点状态 |

Kueue 的准入公平共享按 LocalQueue 历史用量排序，用量随时间衰减，并在准入时施加 entry penalty 防止瞬时大量提交绕过统计；`resourceWeights` 表示资源类型相对权重，LocalQueue 的 `fairSharing.weight` 默认为 1（[Admission Fair Sharing](https://github.com/kubernetes-sigs/kueue/blob/911a822a49bcfd99c9c62203a009efa4130ad604/site/content/en/docs/concepts/admission_fair_sharing.md)）。但**feature gate 默认开不等于目标 ClusterQueue 已启用**：CQ 还需 `admissionScope.admissionMode: UsageBasedAdmissionFairSharing`；该机制只在同一 ClusterQueue 的多个 LocalQueue 之间排序，跨 ClusterQueue 的公平属于 cohort/借用/抢占路径，不能套用 AFS。`status.fairSharing.admissionFairSharingStatus` 记录 `consumedResources` 与 `lastUpdate`；`weightedShare` 的 API 注释是“超 nominal quota 相对 cohort 可借资源的加权份额”，不是历史用量标量，也不是应用公平分数。示例配置中的 `168h`/`5m` 是示例值，不是默认值。

**历史初态是试验门槛，不是背景噪声。** 先跑 A 基线会改变历史用量；随后 B 被优先准入可能正是 AFS 的策略预期，不能直接据此判“不公平”。应记录基线前后与并发前的历史状态、采样窗口和被选中的 admissionMode，把初态作为对照的一部分；不得为试验清零生产账本。

Slurm 侧需分别核验 `PriorityType`/Fair Tree、association 层级、QOS、TRES 计费口径与 decay；FairShare 只是多因子优先级的一部分；FAIR_TREE 默认下 `Level FS = Norm Shares / Effectv Usage`，小于 1 表示过服务，大于 1 表示欠服务，无用量时为 infinity（[sshare 24.11.7](https://slurm.schedmd.com/archive/slurm-24.11.7/sshare.html)）。**Kueue 的准入公平与 Slurm 的优先级公平不是同一层**：前者决定谁先被准入，后者影响排队次序；两者都不能证明已运行任务获得了硬件隔离。

## 公平性口径

公平性必须写明“对什么公平、在什么窗口、用什么分母”：

| 口径 | 计算对象 | 适合回答 | 常见误用 |
|---|---|---|---|
| 吞吐份额 | 单位时间有效产出（样本/step/请求） | 谁的产出占比与份额相符 | 把失败/取消样本计入产出 |
| 等待时间 | 提交到开始服务的时长分布 | 排队是否偏向某租户 | 只看平均值，忽略长尾 |
| SLO/完成率 | 在时限内完成的比例 | 公平是否转化为可用性 | 分母随成功数变化，导致虚高 |
| 资源份额 | 加速器/CPU/内存/存储的实际占用 | 配额与使用是否偏离 | 用利用率代替“有效占用” |

判断规则：

- 先固定窗口（例如同一批任务从提交到完成的完整区间），再计算份额；窗口不一致的对比无效。
- 排队中的需求与已运行的需求分开记录；只统计已运行任务会掩盖“根本进不来”的租户。
- 训练看有效 step 与恢复损失，服务看成功请求的 TTFT/TPOT/尾延迟；两类负载不共用一套 SLO。
- 公平性变好但总产出下降，属于策略权衡，不是自动成功；需同时报告总产出与 SLO。

## 官方共享限制案例（来源支持）

本任务要求一个官方共享/隔离限制或上游性能案例。可用的**语义级**官方材料是：

- device plugin 的 time slicing **不做任何隔离**：每个工作负载可访问整块 GPU 显存，处于同一故障域，一个崩溃全部受影响；`replicas` 只是访问名额，请求多于 1 不保证按比例算力（[README](https://github.com/NVIDIA/k8s-device-plugin/blob/487d7a93894b0f3ad08097169593972eb3ca8206/README.md)）。
- MPS 不提供客户端间错误隔离；一个致命故障会波及共享该 GPU 子集的客户端，且不指出肇事者；同一系统只有一个用户能持有活动 server（[When to Use MPS](https://docs.nvidia.com/deploy/mps/when-to-use-mps.html)）。
- MIG 在官方对照表中提供显存保护、带宽 QoS 与错误隔离，但受 profile 与碎片约束（[MIG Concepts](https://docs.nvidia.com/datacenter/tesla/mig-user-guide/concepts.html)）。

这条案例能预测“两租户并发时哪些指标可能互相影响”，**但不提供任何性能数字**。预计结果与实际结果必须分栏：

| 项目 | 预计（来自机制） | 实际（本次测量） |
|---|---|---|
| time slicing 两租户 | 尾延迟与吞吐互相影响；错误可能连带 | 待填；未执行 |
| MPS 两租户 | 显存/算力受限，但错误仍可能波及；未同步终止客户端可能反伤 server 与 A | 待填；未执行 |
| MIG 两租户 | 若位于**不同 GI**，官方所述显存/带宽/错误范围可受限；同 GI 的 CI 共享显存/引擎；主机/PCIe/网络/存储仍可能相互影响；整卡 reset/驱动/主机故障仍共享 | 待填；未执行 |
| Ascend 虚拟设备 | 静态/动态 vNPU 有资源切分与分配约束（[HDK 虚拟化实例](https://github.com/Ascend/mind-cluster/blob/44385c13d7b1d87def35f1604e8be4d16de6ca4e/docs/zh/scheduling/04_usage/02_virtual_instance/00_virtual_instance_with_hdk/01_description.md)），但跨 vNPU 故障隔离/QoS 未证实；vCANN-RT 为时分复用（[vCANN-RT 特性](https://github.com/Ascend/mind-cluster/blob/44385c13d7b1d87def35f1604e8be4d16de6ca4e/docs/zh/scheduling/04_usage/02_virtual_instance/01_virtual_instance_with_vcann_rt/00_description.md)） | 待填；未执行，保持未知 |

## 停止条件与恢复安排

出现以下任一情况时停止对照并保留证据：

- SLO 违约超过预先登记的失效预算，或失败率持续上升。
- 设备出现健康告警、Xid/ECC/复位类事件，或主机出现不可恢复的内存/PCIe 错误。
- 存储时延/错误超过基线，或网络出现持续重传/拥塞且无法归因。
- 队列或控制面出现异常（准入停滞、账本与实体不一致）。
- 变更共享模式后无法回退，或回退所需制品/配置缺失。
- MPS 场景无法确认客户端已同步退出、server 处于 `FAULT` 或疑似受影响状态时，不得直接终止客户端。

停止后先保护现场（时间线、对象版本、指标窗口、配置快照），再决定回退；**“恢复默认配置”不等于“应用已恢复”**，需重新做功能与进展验证。MPS 的恢复必须走文档所述的安全退出/客户端终止路径；**不能为了释放 B 而破坏仍在运行的 A**。故障轮次与正常释放轮次分开记录，不能把故障后的清理当作“可逆恢复”的证据。

## 完成判据

- 容量记录完整，能解释配额、形状、碎片、余量与故障预算。
- 单租户 A（异构设计的 B）基线自身可重复，差异在预登记噪声带内；**只有基线稳定才进入并发**。并发相对基线的变化与基线自身噪声分开报告。
- A/B 负载可比性或异构归一化口径已登记；份额比较只在可比条件下进行，不把不同模型 step 或请求直接求份额。
- 机制启用状态与初态控制已落实为门槛：Kueue 的队列映射、admissionMode、权重与 `status.fairSharing` 字段；Slurm 的真实 association、`PriorityType`/Fair Tree、QOS、`TRESBillingWeights`、`PriorityWeightFairshare` 等有效优先级权重，以及 A/B 作业的实际因子贡献；未满足或公平因子无有效贡献时，不据等待差异判公平策略。初态采用可审查方案（匹配预置历史、交换顺序的配对轮次，或按各轮历史预测准入顺序），不是仅记录后声称“已控制”。
- 所选控制路线有“参数/对象 → 生效时机/条件 → 实际生效证据 → 不满足时停止/降级”的记录；没有生效证据时，不作该层隔离的因果结论。
- 并发分析已预登记共同窗口、采样间隔、时间戳误差与各层相对基线的变化判据；超出时序分辨能力时保留并列候选或证据不足。
- 首个受影响边界的结论为以下之一：**有证据的候选边界**、**在给定负载/窗口下未观察到显著退化**、**证据不足无法排序**。后两者不得写成“全场景无争用”，候选边界也须结合干预与恢复证据，不能直接当根因。
- 公平性按预先定义的口径与分母计算，并同时报告总产出与 SLO；减少总并发带来的改善标为策略权衡，不称运行时隔离证明。
- 预计结果与实际结果分栏；未取得的证据与未验证的模式保留为 unknown。
- 回收后新任务能获得正确资源并产生持续进展；仅“调度成功”不算完成。

## 来源与验证记录

- [Kueue v0.19.0 — Admission Fair Sharing](https://github.com/kubernetes-sigs/kueue/blob/911a822a49bcfd99c9c62203a009efa4130ad604/site/content/en/docs/concepts/admission_fair_sharing.md)
- [Kueue v0.19.0 — Fair Sharing](https://github.com/kubernetes-sigs/kueue/blob/911a822a49bcfd99c9c62203a009efa4130ad604/site/content/en/docs/concepts/fair_sharing.md)
- [Slurm 24.11.7 — sshare](https://slurm.schedmd.com/archive/slurm-24.11.7/sshare.html)
- [Slurm 24.11.7 — priority/multifactor](https://slurm.schedmd.com/archive/slurm-24.11.7/priority_multifactor.html)
- [NVIDIA k8s-device-plugin v0.20.1 README](https://github.com/NVIDIA/k8s-device-plugin/blob/487d7a93894b0f3ad08097169593972eb3ca8206/README.md)
- [NVIDIA MPS — When to Use MPS](https://docs.nvidia.com/deploy/mps/when-to-use-mps.html)
- [NVIDIA MIG — Concepts](https://docs.nvidia.com/datacenter/tesla/mig-user-guide/concepts.html)
- 当前验证范围：未执行。待确认：Kueue AdmissionFairSharing 的默认参数、Slurm 站点权重与 decay、Ascend 虚拟设备的隔离语义、两租户实测数据。
