---
id: cluster-platform.admission-and-placement
title: 作业准入、调度与拓扑放置
type: concept
domain: cluster-platform
status: draft
platforms: [generic]
source_refs:
  - src.kueue.admission-v0.19.0
  - src.kueue.cluster-queue-v0.19.0
  - src.volcano.podgroup-gang-v1.15.0
  - src.volcano.gang-plugin-v1.15.0
  - src.ascend.mind-cluster-v26.1.1
  - src.slurm.docs-24.11.7
  - src.slurm.gres-tres-cgroup-24.11.7
updated_at: "2026-10-14"
summary: 区分配额、准入、组调度、节点放置与设备分配，按状态证据判断等待位置，并保留 GPU/NPU 拓扑和实现边界。
related_ids:
  - cluster-platform.kubernetes-job-lifecycle
  - cluster-platform.slurm-jobs-and-device-resources
  - cluster-platform.idle-resource-job-waiting-triage
  - cluster-platform.device-resource-chain
  - hardware.resource-topology
  - communication.collectives-and-rank-progress
  - reliability.dimensions-and-failure-domains
verification:
  status: source_checked
  evidence_refs:
    - src.kueue.admission-v0.19.0
    - src.kueue.cluster-queue-v0.19.0
    - src.volcano.podgroup-gang-v1.15.0
    - src.volcano.gang-plugin-v1.15.0
    - src.volcano.scheduler-actions-v1.15.0
    - src.volcano.job-controller-v1.15.0
    - src.slurm.docs-24.11.7
    - src.slurm.gres-tres-cgroup-24.11.7
    - src.ascend.mind-cluster-v26.1.1
  notes: "核对固定 Kueue 文档/API（含 ClusterQueue 借用/抢占样板）、MindCluster 文档及 Volcano 版本化概念页与 gang 插件实现（valid/preempt/ready/pipelined/条件上报），复用 T05-03 Slurm 归档；未部署调度器、提交任务、修改集群或执行 GPU/NPU 验证；Volcano job 控制器 handler 事件路径未覆盖（unknown）；调度动作与控制器 running/restarting/policy 已读。"
---

# 作业准入、调度与拓扑放置

“集群还有空卡”不足以解释一个作业为什么能或不能运行。队列可能没有配额，作业可能等待外部准入条件，单个 Pod 的需求可能超过任一节点的剩余资源，也可能无法组成满足设备互联要求的组合。资源总量、放置可行性、设备分配成功与应用开始计算需要分别判断。

本页组织这些判断的边界。Kueue、上游 Volcano 和 MindCluster 中适配的 Volcano 是三个独立来源样板；它们的版本和状态不能拼成一个已验证系统。`generic` 是概念范围，不表示任意 GPU/NPU 插件或调度配置都受支持。

## 沿着状态找等待位置

下图是本库的观察模型。不同系统可能合并阶段、延迟部分决策或重新排队，不保证每个箭头对应一个独立控制器。

```mermaid
flowchart LR
    A[对象被接受] --> B[队列与资源配额]
    B --> C[准入条件满足]
    C --> D[节点和拓扑放置]
    D --> E[设备分配与容器启动]
    E --> F[进程与通信组初始化]
    F --> G[应用持续进展]
    C -. 等待或撤销 .-> B
    D -. 约束不满足 .-> B
```

| 观察层 | 需要读取的证据 | 尚不能推出什么 |
|---|---|---|
| 对象接受 | 作业/Workload/Pod 身份、generation、控制器是否接管 | 已有配额或已经排上节点 |
| 配额预留 | 队列、资源类型、请求量、flavor、配额条件 | 物理节点有合适组合；设备可访问 |
| 准入 | 当前准入条件和外部检查结果，及相应对象版本 | 全部 Pod 已启动、全部 rank 已进入训练 |
| 节点放置 | Pod 的目标节点、约束匹配、组级最小要求、调度事件 | 设备挂载和框架初始化成功 |
| 设备分配/容器启动 | Allocate、实际映射、容器状态与运行环境 | collective 契约匹配、模型或数据可用 |
| 应用就绪与进展 | 实际进程成员、通信组、step/request 进度及结果验证 | 其他任务或故障条件也正常 |

设备分配后的详细证据链见[从物理设备到容器资源的状态链](device-resource-chain.md)；组内 rank 和通信进度见[集合通信与 rank 进度](../03-communication/collectives-and-rank-progress.md)。不要把控制面上的一个 `Running` 替代这两段检查。

## 配额与准入：Kueue 的一个固定样板

Kueue v0.19.0 用 Workload 表达准入对象及 PodSet 资源需求；逻辑配额由队列/flavor 管理，启用相应拓扑功能时还检查物理放置条件，外部 AdmissionCheck 则可以继续推迟准入。其 API 分开定义 `QuotaReserved`、`Admitted` 和 `PodsReady`；这些条件的对象和含义不同。`PodsReady` 的定义还包含已经成功结束的 Pod，不能读成“所有副本此刻都在运行”。参见固定 [admission.md](https://github.com/kubernetes-sigs/kueue/blob/911a822a49bcfd99c9c62203a009efa4130ad604/site/content/en/docs/concepts/admission.md)与 [Workload API 条件定义](https://github.com/kubernetes-sigs/kueue/blob/911a822a49bcfd99c9c62203a009efa4130ad604/apis/kueue/v1beta1/workload_types.go#L628-L643)。

资源请求的对象也要明确：PodSet 的副本数乘每 Pod 需求，用于作业级配额核算；单 Pod 需求仍需在实际节点上满足。不能只保留作业总设备数而丢掉 PodSet/Pod 粒度（[固定 Workload 文档](https://github.com/kubernetes-sigs/kueue/blob/911a822a49bcfd99c9c62203a009efa4130ad604/site/content/en/docs/concepts/workload.md)）。

拓扑判断不总发生在同一个阶段。这个固定版本的 TAS 文档对 Provisioning AdmissionCheck 另列了配额预留、等待外部资源检查、再完成 topology assignment 的流程。因此，调查应看实际条件和配置，不强制把上图作为控制器的执行顺序（[固定 TAS 文档的 ClusterAutoscaler support](https://github.com/kubernetes-sigs/kueue/blob/911a822a49bcfd99c9c62203a009efa4130ad604/site/content/en/docs/concepts/topology_aware_scheduling.md#clusterautoscaler-support)）。

## Gang 约束不是应用同步屏障（Volcano 实现样板，以实现为准，文档差异另注）

Volcano v1.15.0 的 PodGroup 以 `minMember`、`minResources` 等字段表达组级最低条件（[PodGroup](https://volcano.sh/docs/v1.15.0/concepts/podgroup/)、[Gang](https://volcano.sh/docs/v1.15.0/scheduler/plugins/gang/)）。这个最低规模不必等于作业定义中的全部副本数。满足它也不保证进程同时执行到同一行代码，或都成功加入了应用通信组。



Volcano v1.15.0 gang 插件（[`gang.go@v1.15.0`](https://github.com/volcano-sh/volcano/blob/8fc394c11e8db0d0ada5c17816b58bced9d7213d/pkg/scheduler/plugins/gang/gang.go)，只读未执行）按会话阶段做成组决策：`validJobFn` 按任务有效性（`CheckTaskValid`/`CheckSubJobValid`，`ValidTaskNum < MinAvailable`）拒绝并给出 `NotEnoughPodsOfTaskReason`/`NotEnoughPodsReason`（后者表示作业已有 Pod 对象不够，如控制器尚未创建或重建，不等于资源不足）；`AddJobReadyFn`/`AddJobPipelinedFn`（[`gang.go` L191–211@`8fc394c1`](https://github.com/volcano-sh/volcano/blob/8fc394c11e8db0d0ada5c17816b58bced9d7213d/pkg/scheduler/plugins/gang/gang.go)）决定作业可调度与可放行；会话关闭时对未就绪作业写 `PodGroupUnschedulableType` 条件（reason `NotEnoughResourcesReason`，消息 `x/y tasks in gang unschedulable` 中 x 为 `MinAvailable` 减可调度数，y 为全部任务数），就绪则写 `PodGroupScheduled`（reason 为 `tasks in gang are ready to be scheduled`，只表示可调度，不表示已运行）。调度器 Ready 实现口径（[`job_info.go` L877–886、L1202–1204@`8fc394c1`](https://github.com/volcano-sh/volcano/blob/8fc394c11e8db0d0ada5c17816b58bced9d7213d/pkg/scheduler/api/job_info.go)：`ReadyTaskNum` 计 Bound/Binding/Running/Allocated/Succeeded，不计 Pipelined；`IsReady` 另加 Pending 的 BestEffort 任务；Gang 文档把 Pipelined 列入 Ready，与实现不一致，以实现为准。注意 `minMember` 由 gang 插件在会话内判定，`minResources` 不在该插件内（全文无引用），而在入队阶段由 enqueue 动作与配额类插件使用（`enqueue.go` 已核；proportion/capacity/overcommit 判定公式未审计，unknown）；job 控制器按 `minAvailable` 计算并同步 PodGroup 的 `minMember`/`minResources`（[`job_controller_actions.go` L813–816、L877–880@`8fc394c1`](https://github.com/volcano-sh/volcano/blob/8fc394c11e8db0d0ada5c17816b58bced9d7213d/pkg/controllers/job/job_controller_actions.go)）。抢占保护按动作分：旧 preempt/reclaim 动作（[`gang.go` L97–137@`8fc394c1`](https://github.com/volcano-sh/volcano/blob/8fc394c11e8db0d0ada5c17816b58bced9d7213d/pkg/scheduler/plugins/gang/gang.go) `preemptableFn`，统一驱逐入口 `AddUnifiedEvictableFn` 对 GangReclaim/GangPreempt 直接放行）只在被抢作业 ready 数高于 `MinAvailable` 时逐个放行；gangpreempt/gangreclaim 采用 bundle 模型，`allowWholeBundle` 默认 `true`（[`gangpreempt.go` L32–52、L248](https://github.com/volcano-sh/volcano/blob/8fc394c11e8db0d0ada5c17816b58bced9d7213d/pkg/scheduler/actions/gangpreempt/gangpreempt.go) 与 [`gangreclaim.go` L32–52、L247](https://github.com/volcano-sh/volcano/blob/8fc394c11e8db0d0ada5c17816b58bced9d7213d/pkg/scheduler/actions/gangreclaim/gangreclaim.go) 同默认值，仅显式关闭时跳过 whole bundle），被抢作业可能整体被驱逐；启用哪些动作取决于站点调度器配置（unknown）。

### 失败与回退分层（只读未执行；job 控制器重排队逻辑的 handler 事件路径未覆盖，unknown）

| 层 | 行为 | 证据位置 |
|---|---|---|
| 入队 | `MinResources == nil` 或 `JobEnqueueable` 时转 `PodGroupInqueue`；由哪些插件提供判定取决于调度器配置 | [`enqueue.go` L95–99@`8fc394c1`](https://github.com/volcano-sh/volcano/blob/8fc394c11e8db0d0ada5c17816b58bced9d7213d/pkg/scheduler/actions/enqueue/enqueue.go) |
| 会话内成组决策 | `JobValid` 不通过则跳过 allocate；配置了 enqueue 动作时仍 Pending 的作业跳过 allocate（L152–169），未配置时就地转 Inqueue 继续；只有 `JobReady` 才 `Commit`（L313–336，pipelined 不提交），`minAvailable < replicas` 时放回队列；SubJob 不 ready 不 pipelined 则 `Discard`（L832–844） | [`allocate.go`@`8fc394c1`](https://github.com/volcano-sh/volcano/blob/8fc394c11e8db0d0ada5c17816b58bced9d7213d/pkg/scheduler/actions/allocate/allocate.go) |
| 会话关闭 | 写 Unschedulable/Scheduled 条件；对 gang 不可调度作业计调度重试（`RegisterJobRetries`，非控制器 `RetryCount`） | [`gang.go` L229–297](https://github.com/volcano-sh/volcano/blob/8fc394c11e8db0d0ada5c17816b58bced9d7213d/pkg/scheduler/plugins/gang/gang.go) |
| 控制器 | Pod 事件/退出码按 task/job 级 policy 映射到 Restart*/Abort（默认只 `SyncJobAction`，`PodPendingEvent` 须配 `Timeout`）；Restart* 杀 Pod 转 Restarting，`RetryCount++`；达 `maxRetry` 转 Failed，否则回 Pending（`restarting.go` L35–49，`total − Terminating >= MinAvailable` 才回 Pending）；Running 中 Pending 超 `replicas − minAvailable` 回落 Pending | [`running.go` L35–46/L107–110](https://github.com/volcano-sh/volcano/blob/8fc394c11e8db0d0ada5c17816b58bced9d7213d/pkg/controllers/job/state/running.go)/[`restarting.go` L35–49](https://github.com/volcano-sh/volcano/blob/8fc394c11e8db0d0ada5c17816b58bced9d7213d/pkg/controllers/job/state/restarting.go)/[`job_controller_util.go` L182–196/L286–288](https://github.com/volcano-sh/volcano/blob/8fc394c11e8db0d0ada5c17816b58bced9d7213d/pkg/controllers/job/job_controller_util.go)（`applyPolicies`） |
| 应用 rendezvous | 不在 Volcano 范围 | — |

Kueue 侧对应机制：PodsReady 超时驱逐与指数退避重排（`requeueState`），见 [T05-02](kubernetes-job-lifecycle.md) L115 与 workload.md。

读到“all or nothing”时，应明确 all 指什么：全部资源请求、最低成员集合、一个 PodSet，还是特定实现中的调度决策。调度器内部的 Ready、Pod condition 与应用 rendezvous 不共享同一语义。启动失败、拉取镜像失败、设备分配失败和进程退出仍需在对应层观察。

## 数量足够，为什么仍放不下

下面是原创资源示例，不是现场事故：两台节点各剩 4 个同类型完整设备，总量为 8。一个要求单 Pod 使用 8 个设备的任务，不能仅凭总量证明可放置；两个各需 4 个设备的 Pod 也还要分别满足 CPU、主机内存、标签、污点、卷和拓扑条件。

再看节点内的组合：剩余 4 个设备不一定满足一个四设备通信域的连接、成组或隔离要求。需要检查设备身份与互联图，不能把设备数压缩成唯一调度维度。资源布局的记录方法见[计算节点资源与拓扑参考](../01-hardware/resource-topology.md)。

这类等待至少可能来自三种不同证据：队列账本没有足够份额；节点资源碎片无法满足单 Pod；有足够数量却没有满足拓扑约束的组合。三者的处置前提不同，不能都归为“调度器没发现空卡”。

## 拓扑有不同层级，也有不同目标

| 约束或目标 | 应记录的对象 | 需要保留的限制 |
|---|---|---|
| 节点间通信局部性 | block/rack/交换机域、节点标签和网络路径 | 同标签不是实际带宽测量；路径健康与拥塞还需单独观测 |
| 节点内设备亲和 | CPU/NUMA、PCIe、设备互联、成对或成组规则 | 必须绑定具体产品与插件版本，不能从另一型号继承 |
| 降低碎片 | 每 Pod 资源向量、剩余容量和允许组合 | 总利用率高可能降低后续大作业的可放置性 |
| 故障域分散 | 副本/角色、节点、机架、电源与网络共同依赖 | 通信靠近与故障隔离可能有取舍，需按工作负载恢复目标决定 |

Kueue 的固定 TAS 文档用分层节点标签描述拓扑，区分 required 与 preferred：前者是必须满足的放置条件，后者允许向更高拓扑层级寻找位置。物理容量统计还受节点 Ready/可调度状态、已准入负载和其他 Pod 资源占用影响。标签层级并不提供 NVLink/HCCS 或实际网络链路的健康证明（[固定 TAS 文档](https://github.com/kubernetes-sigs/kueue/blob/911a822a49bcfd99c9c62203a009efa4130ad604/site/content/en/docs/concepts/topology_aware_scheduling.md)）。

故障域取舍参考[可靠性维度与故障域](../08-reliability/dimensions-and-failure-domains.md)。本页不给所有训练或推理服务规定统一的集中/分散策略。

## NPU 调度的具体边界

MindCluster v26.1.1 固定[调度流程](https://github.com/Ascend/mind-cluster/blob/44385c13d7b1d87def35f1604e8be4d16de6ca4e/docs/zh/scheduling/04_usage/03_basic_scheduling/02_scheduling_process_of_the_ascend_ai_processor.md)说明其 Volcano 是适配修改的版本，并按 `self-maintain-available-card` 分开两条资源维护路径。调查需要确认实际配置、可用设备账本、调度注解和最终 Allocate 映射，不能把“上游 Volcano 支持 gang”替代 NPU 设备选择的证据。

同一版本的[芯片亲和性文档](https://github.com/Ascend/mind-cluster/blob/44385c13d7b1d87def35f1604e8be4d16de6ca4e/docs/zh/scheduling/04_usage/03_basic_scheduling/01_affinity_scheduling/03_ascend_ai_processor_based_affinity.md)按产品分别说明：旧 Atlas 训练系列的双 HCCS 环、Box16 和 A3 HiAM 模组有不同条件；同页明确 Atlas 800T A2/Atlas 900 A2 PoD 不采用前述芯片亲和性调度。故不能把“同环”写成全部昇腾型号的统一要求，也不能将没有该项调度规则理解为没有互联或其他放置约束。

节点间的[交换机亲和性](https://github.com/Ascend/mind-cluster/blob/44385c13d7b1d87def35f1604e8be4d16de6ca4e/docs/zh/scheduling/04_usage/03_basic_scheduling/01_affinity_scheduling/04_node_based_affinity.md)又是另一层功能，需核对任务类型和配置。本页没有确认这些 MindCluster 组件与前述 Kueue/上游 Volcano 版本可共同部署，也没有验证目标 NPU 的硬件、驱动、固件或框架。

## 一次调查需要留下什么

保留作业与 attempt 身份、Workload/Pod UID 和对象版本、队列/flavor、实际生效的资源请求、组级最低条件、约束及拓扑标签来源，再关联同一时间窗口的配额条件、准入检查、调度事件、节点状态和设备分配映射。随后用应用日志核对哪些进程真正到达初始化和计算阶段。

这些信息应来自同一次调度尝试。历史事件与当前状态可能属于不同 generation，实时资源占用也会变化。下一项检查应先区分等待发生在哪层，不因一个 Pending 或 Running 状态直接修改资源申请、亲和规则或驱逐其他作业。

尚缺目标环境、实际调度配置、物理拓扑与运行证据。本文没有提交任务、变更队列或运行验证；来源差异、固定版本见[本批 T05-05 来源记录](../../docs/research/batch-22-t05-05-sources.md)，许可范围见来源登记条目。

## 两个独立的配额/调度样板（不互套）

### 样板 A：Kueue quota/flavor/cohort/borrow（v0.19.0，只读未执行）

适用前提：工作负载在 Kubernetes 上，已有 Kueue 队列/账户体系，需要配额借用或抢占语义（两平台共有的能力如抢占不作区分依据；不是产品推荐）。公平性代价：`reclaimWithinCohort` 非 `Never` 时借用方在对方需要时被收回（三个抢占字段默认全 `Never`，此时 cohort 只优先接纳 nominalQuota 内新负载）；Fair Sharing 与 `borrowWithinCohort` 互斥；启用 Fair Sharing 后 cohort 内回收改按 Fair Sharing 抢占策略执行（cluster_queue.md L444–452，具体策略未取证，unknown）；`StrictFIFO` 队头阻塞后续，默认 `BestEffortFIFO` 不阻塞。

| 维度 | 观测字段/命令 | 来源 | 不能推出什么 | 失败或不适用反例 |
|---|---|---|---|---|
| 资源向量 | PodSet count × 每 Pod 多资源请求；resourceGroup `coveredResources` 要求同组同 flavor | [cluster_queue.md](https://github.com/kubernetes-sigs/kueue/blob/911a822a49bcfd99c9c62203a009efa4130ad604/site/content/en/docs/concepts/cluster_queue.md) | 节点无碎片 | 本 CQ 名额被借出且在使用＋`lendingLimit` 未设→新负载 Pending（`reclaimWithinCohort=Never` 时等待，否则可回收抢占；细分 reason 需开门控 `UnadmittedWorkloadsObservability`（v0.19 Beta，默认关），否则只见 `Pending`，unknown） |
| 拓扑 | TAS required/preferred 标签层级；`TopologyPlacementFailed`（[v1beta2 workload_types.go L956–958](https://github.com/kubernetes-sigs/kueue/blob/911a822a49bcfd99c9c62203a009efa4130ad604/apis/kueue/v1beta2/workload_types.go#L956-L958)，需开门控 `UnadmittedWorkloadsObservability`（v0.19 Beta，默认关）才可见） | 同上＋TAS 文档 | NVLink/HCCS 健康 | required 不满足→不准入；preferred 退到上层 |
| 碎片 | 配额 fit ≠ 节点无碎片（见本页数量示例节） | 本页例子 | 可放置 | 名额够但无满足拓扑的组合→Pending |
| 配额 | `flavorsReservation`/`flavorsUsage`、指标 reservation/usage、evicted reason | [metrics.md](https://github.com/kubernetes-sigs/kueue/blob/911a822a49bcfd99c9c62203a009efa4130ad604/site/content/en/docs/reference/metrics.md) | 物理容量 | 请求超 nominal＋borrowingLimit→永不满足（`ExceedsMaxQuota`，开门控可见，否则只见 `Pending`）；已借＋本次超限→等待（`WaitingForQuota`，同上门控条件） |
| 运行进展 | `PodsReady` 条件；Admitted ≠ 运行 | workload.md | 训练进展 | Admitted 后 Pod 长期不 Ready→PodsReadyTimeout 驱逐重排 |

对照验收（设计，未执行）：同配置请求不超过 nominalQuota 的负载应得 `QuotaReserved=True`、`Admitted=True`（正例）；请求超过本 CQ 该 flavor 的 `nominalQuota + borrowingLimit`→持续 Pending（开门控时 reason 为 `ExceedsMaxQuota`，关闭时只见 `Pending`）（反例）。判定方式：读 Workload 条件与 ClusterQueue 账本字段。

### 样板 B：Slurm partition/QOS/priority/reservation（24.11.7，只读未执行）

适用前提：工作负载在 Slurm 单集群，已有账户/QOS/预留体系（不是产品推荐）。公平性代价：评估顺序为可抢占作业→带预留作业→分区 PriorityTier→job priority→提交时间→job ID（最高 priority 不一定先评估）；fair-share 让 under-serviced 账户先调度（非固定配额）；预留核/节点他作业不可用（`no other jobs can use those resources`），但预留不改 priority。

| 维度 | 观测字段/命令 | 来源 | 不能推出什么 | 失败或不适用反例 |
|---|---|---|---|---|
| 资源向量 | TRES/GRES 请求向量（`--gres`、`--cpus-per-gpu` 等） | [gres](https://slurm.schedmd.com/archive/slurm-24.11.7/gres.html) | 拓扑满足 | 请求超分区上限→拒绝或 Pending |
| 拓扑 | `topology/tree`＋`--switches`（未登记本页，unknown） | — | 链路健康 | 越层放置性能未知 |
| 碎片 | 单节点剩余 vs 单 Pod 需求（本库推论：总量够但单节点放不下） | [job_reason_codes](https://slurm.schedmd.com/archive/slurm-24.11.7/job_reason_codes.html)（Resources 原文仅“资源不可用”，推论已标注） | 根因证明 | Resources＋节点有空→查碎片/约束 |
| 配额 | QOS/Assoc 限额系列 reason；squeue `%r` | 同上 | 优先级 | 限额命中→对应 QOS*/Assoc* reason |
| 运行进展 | `R` 状态；squeue `%R` 失败说明 | [squeue](https://slurm.schedmd.com/archive/slurm-24.11.7/squeue.html) | 应用成功 | `R` 且无进度→查应用日志 |

对照验收（设计，未执行）：同一 QOS、同一分区、该 QOS 未设 `DenyOnLimit`（设了则提交时即被拒，不进 Pending）、分区未挂优先于作业 QOS 的 Partition QOS（除非作业 QOS 设了 `OverPartQOS`）、站点实际执行 QOS 限额（站点配置 unknown）；请求不超过 QOS 每作业 GRES 上限时，`squeue %r` 不应为 `QOSMax*PerJob`（正例）；只把 GRES 请求提高到超过该上限时，`%r` 应为 `QOSMaxGRESPerJob`（反例）（job_reason_codes、qos 页）。指定节点（`--nodelist`）不可用→`ReqNodeNotAvail`为另一对，配“同作业不指定节点”的正例。判定方式：squeue/sinfo/scontrol 只读命令。

配置/状态参数：`PriorityWeight*`、分区 `PriorityTier`、`PreemptType=preempt/qos`、QOS `GrpTRES` 等限额字段、预留 `FLEX` 等 flags（见 [priority_multifactor](https://slurm.schedmd.com/archive/slurm-24.11.7/priority_multifactor.html)、[qos](https://slurm.schedmd.com/archive/slurm-24.11.7/qos.html)、[reservations](https://slurm.schedmd.com/archive/slurm-24.11.7/reservations.html)，只读未执行；站点值 unknown）。预留仅 root 或配置的 SlurmUser 可建。

两样板术语不互套：Kueue（Workload 整体配额预留＋可选 waitForPodsReady 超时驱逐与退避重排，见 [T05-02](kubernetes-job-lifecycle.md) L115）≠ Slurm gang scheduling（分时）≠ Volcano gang（最小规模放行）。

## MindCluster 边界与等待定位入口

NPU 侧以 MindCluster 固定实现为准（见上文 NPU 节），型号/调度路径（`self-maintain-available-card` 两条资源路径、芯片亲和差异）不得从上游 Volcano 或 Kueue 样板推导。有空闲设备但作业等待时，先按[空闲设备但作业等待诊断指南](idle-resource-job-waiting-triage.md)定位等待层，再用本页样板确认配额/放置两层。本文示例不是推荐所有平台的统一策略。
