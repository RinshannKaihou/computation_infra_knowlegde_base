---
id: cluster-platform.node-drain-resource-reclamation
title: 节点摘除、drain 与资源回收流程
type: procedure
domain: cluster-platform
status: draft
platforms: [generic]
source_refs:
- src.kubernetes.node-drain-v1-32
- src.kubernetes.eviction-pdb-v1-32
- src.kubernetes.node-shutdown-v1-32
- src.kubernetes.node-lifecycle-v1-32
- src.kubernetes.daemonset-static-pod-v1-32
- src.kubernetes.storage-reclaim-v1-32
- src.kubernetes.device-plugins-v1-32
- src.kubernetes.job-lifecycle-v1-32
- src.kubernetes.api-gc-v1-32
- src.slurm.docs-24.11.7
- src.slurm.gres-tres-cgroup-24.11.7
- src.slurm.node-power-lifecycle-24.11.7
- src.ascend.mind-cluster-v26.1.1
- src.pytorch.elastic-2.6
updated_at: "2026-10-18"
applicability:
  environment_refs: []
  notes: "未建立环境档案。Kubernetes 以 v1.32 静态快照为样板，Slurm 以 24.11.7 归档为样板；目标环境的版本、PDB、节点参数、设备插件与存储驱动须另行补齐。"
verification:
  status: not_verified
  evidence_refs: []
  notes: "仅核对官方文档语义；未执行 cordon/drain/驱逐、未操作节点、未取消或重排 Slurm 作业。"
summary: 分别组织 Kubernetes cordon/drain/删除与 Slurm DRAIN/DOWN/RESUME 流程，按训练、服务、有状态负载说明停止准入、等待/取消/Checkpoint、设备与卷清理及重新准入的责任边界。
related_ids:
- cluster-platform.kubernetes-job-lifecycle
- cluster-platform.slurm-jobs-and-device-resources
- cluster-platform.device-resource-chain
- cluster-platform.platform-change-and-rollback
- training.elastic-training-and-membership
- hardware.node-acceptance-triage
---

# 节点摘除、drain 与资源回收流程

> 范围：Kubernetes v1.32 静态快照与 Slurm 24.11.7 归档。本文整理“节点退出服务—工作负载结束—资源回收—重新准入”的责任边界，**不执行 drain、驱逐或节点操作**；命令与参数只作为已核对语义的引用，具体执行仍需现场授权。

## 目标与触发条件

当需要把节点从可调度池中移出（维护、升级、硬件告警、返修、缩容）时，团队通常只检查“节点是否 NotReady”或“Pod 是否消失”。这不足以证明资源已回收：设备可能仍被残留进程占用，卷可能仍挂着，账本可能仍保留过期分配。

本流程回答：**停止准入后，谁负责让负载结束、让设备/卷/网络状态清理、让账本与实体一致，以及凭什么判定可以重新准入。**

触发条件包括：

- 计划内维护/升级（先 drain，再停机或换组件）。
- 设备或主机健康告警，需要隔离节点。
- 缩容或节点退役。
- 变更后发现调度仍把任务放到“已摘除”的节点，或账本显示有卡但容器不可用。

## 适用范围与前置条件

| 项 | 要求 |
|---|---|
| Kubernetes | 明确版本（本文以 v1.32 快照为例）；确认 `kubectl drain` 行为、PDB、DaemonSet、static Pod、存储驱动与 CSI 版本 |
| Slurm | 明确版本（本文以 24.11.7 归档为例）；确认分区、节点状态、`ReturnToService`、`SlurmdTimeout`、`KillWait`、Epilog 配置 |
| 工作负载 | 区分训练、在线服务、有状态服务与批处理；确认是否可中断、是否有 Checkpoint、是否可重排队 |
| 权限 | cordon/drain/删除节点、`scontrol`/`scancel` 均属高影响操作；本文不授予权限 |
| 证据 | 能读取节点/Pod/Job 状态、事件、kubelet 与容器运行时视图、设备插件与 Slurm 节点/作业状态 |
| 环境档案 | 当前为空；缺少设备与存储信息时，回收结论只能停留在“平台状态”，不能证明设备可用 |

Kubernetes 与 Slurm 的术语**不互译**：`cordon` 只是标记不可调度；`drain` 是“标记 + 驱逐”的组合流程；Slurm 的 `DRAIN` 是节点不再接收新作业、既有作业继续跑完，`DOWN` 则会终止运行与挂起作业。把 `DRAIN` 直接当成 `drain` 会误判既有作业是否会被终止。

## 需要的证据

| 证据 | 采集范围或定位 | 用途 | 缺失时如何处理 |
|---|---|---|---|
| 节点对象与状态 | Node 名称、conditions、unschedulable、Lease 心跳、创建/删除时间 | 判断节点是否仍被控制面视为同一实体 | 名称冲突或重建时先核对 UID |
| Pod/Job 状态 | phase、conditions、deletionTimestamp、OwnerReferences、finalizer、attempt/重启计数 | 区分“正在终止”“已失败”“仍被控制器重建” | 只看 `kubectl get pods` 会漏掉 terminating 与 mirror Pod |
| PDB | minAvailable/maxUnavailable、当前健康 Pod 数、unhealthyPodEvictionPolicy | 解释驱逐为何被拒或 drain 为何不结束 | 无 PDB 记录时不能假定“可以随时驱逐” |
| 设备视图 | 插件上报的 capacity/allocatable、PodResources、容器内设备节点、Slurm GRES | 判断分配是否真正释放 | 只看到“卡在节点上”不等于“已分配” |
| 卷与 CSI | PVC/PV、VolumeAttachment、finalizer、回收策略、CSI 驱动日志 | 判断卷是否已卸载/删除 | 缺 CSI 证据时保留“可能仍挂着” |
| 容器运行时 | `crictl ps`（含 ATTEMPT）、残留进程、容器日志 | 发现 kubelet 之外的残留 | 只看 API 会漏掉 static/mirror 与运行时残留 |
| Slurm 节点/作业 | `sinfo`/`scontrol show node` 的 State 与 Reason、作业状态/reason、requeue 记录 | 判断 drain/down 与作业是否重排 | 站点 reason 为管理员自填，不能当自动根因 |
| 时间线 | 操作、状态变化、事件、指标窗口 | 关联“谁先变化” | 缺时间线时不做因果判断 |

## 步骤与判断分支

### Kubernetes 路径

| 步骤 | 检查或动作 | 运行影响 | 预期证据与解释 | 下一步 |
|---|---|---|---|---|
| 1 | 记录节点身份（名称、UID）、当前负载、PDB 与设备分配 | 只读 | 确认要摘除的是同一节点对象；同名重建会被视为同一对象 | 名称冲突则先处理对象身份 |
| 2 | `cordon`：标记 unschedulable | 普通 Pod 不再被调度到该节点；既有 Pod 不受影响 | 这是**调度限制，不是完整准入屏障**：容忍 unschedulable 的 Pod、直接写 `spec.nodeName` 的 Pod、DaemonSet 与 static Pod 仍可能出现在节点上 | 不能把 cordon 当成“节点已无新负载” |
| 3 | 预检 PDB、不可驱逐对象、本地数据与恢复点 | 只读 | 零自愿驱逐（`maxUnavailable=0` 或 `minAvailable=100%`）会让**健康** Pod 无法驱逐；`AlwaysAllow` 下不健康 Pod 有例外；重叠 PDB 会拒绝驱逐。同时确认 emptyDir 可丢弃或已持久化、Checkpoint/备份可读回且不依赖即将离线的唯一副本；hostPath/local PV 记录归属、迁移/保留或擦除授权 | 数据或恢复点未确认时不进入 drain；不能静默绕过预算 |
| 4 | `kubectl drain`：标记并驱逐 | 触发 Eviction API；Pod 按优雅期终止 | 200 允许 / 429 可能为 PDB 拒绝，也可能是 API 限流 / 500 配置错误；有 DaemonSet Pod 时须显式 `--ignore-daemonsets`；无控制器 Pod 须 `--force`；emptyDir 数据须显式 `--delete-emptydir-data` | 429 需结合响应内容、PDB 状态与限流证据分支；500 先修配置 |
| 5 | 区分 Pod 类型 | 只读或等待 | DaemonSet Pod 不会被 drain 删除，且可在**正在 drain 的原节点**重建（每节点一个），不是“迁移到其他节点”；static Pod 的 mirror Pod 不经 API 删除；`--disable-eviction` 会绕过 PDB 直接删除，须避免 | 不把“Pod 还在”误判为 drain 失败，也不把返回码当节点清空证明 |
| 6 | 等待 graceful termination | 有优雅期与超时 | `--grace-period` 默认 -1（用 Pod 自带值）；`--timeout` 0 表示无限；drain 完成前不应操作机器 | 超时则查卡住的 Pod 与 PDB |
| 7 | drain 后核对卷与本地数据 | 只读 | emptyDir 随 Pod 离开节点永久删除；hostPath 无生命周期管理；local PV 绑定节点，节点不可用即不可访问；PV 回收策略与 finalizer 决定删除时机。**维护卸卷与主动删除 PVC/PV 是两条路径**：前者保留存储对象，后者需明确授权并受 in-use finalizer 保护 | 需保留的数据已在 drain 前完成迁移/读回；不得把删除 PVC/PV 当作设备回收条件 |
| 8 | 节点关闭/删除 | 高影响 | **两条路径分开**：(a) 非优雅关闭仅在确认节点已关机/断电、不是重启途中后，才用 `out-of-service` 污点强删 Pod 并立即卸卷，需处理容忍例外、恢复后人工移除污点；(b) Pod 删除未成功满 6 分钟且节点当时不健康时可能触发 force detach 超时，受 `disable-force-detach-on-timeout` 配置影响。仅 NotReady/网络失联不能证明旧写入者已停止 | 两条路径分别授权与观测；“等满 6 分钟”不是安全清理证明 |

Kubernetes 的关键语义（[drain 文档](https://v1-32.docs.kubernetes.io/docs/tasks/administer-cluster/safely-drain-node/)、[kubectl drain 参考](https://v1-32.docs.kubernetes.io/docs/reference/kubectl/generated/kubectl_drain/)）：drain 返回成功表示非豁免 Pod 已按优雅期与 PDB 安全驱逐；之后才可关机或删 VM。**drain 不是“立即删除所有 Pod”，cordon 也不是“绝对不再有新 Pod”**：DaemonSet Pod 可在原节点重建、mirror Pod 不删、容忍与直接绑定可绕过调度、无控制器 Pod 需 `--force`、emptyDir 数据需显式允许删除。

Eviction 的六步链（[API-initiated Eviction](https://v1-32.docs.kubernetes.io/docs/concepts/scheduling-eviction/api-eviction/)）：写入 deletionTimestamp 与优雅期 → kubelet 优雅停止 Pod → 控制面从 Endpoint/EndpointSlice 摘除 → 优雅期满强杀 → kubelet 上报 → API 删除对象。PDB 的 `unhealthyPodEvictionPolicy` 必须按三个分支核对（[configure-pdb](https://v1-32.docs.kubernetes.io/docs/tasks/run-application/configure-pdb/)、[disruptions](https://v1-32.docs.kubernetes.io/docs/concepts/workloads/pods/disruptions/)）：

- **健康 Pod**：始终受 `minAvailable`/`maxUnavailable` 的健康副本预算约束，`AlwaysAllow` 不能绕过。
- **Running 但未健康、`IfHealthyBudget`（默认）**：需核对 `currentHealthy` 与 `desiredHealthy`，不能只看 `disruptionsAllowed`；放行分支还显式检查 `desiredHealthy > 0`。未执行反例：`minAvailable=2`、两个健康副本加一个 Running/Ready=False 目标、`currentHealthy=desiredHealthy=2`、`disruptionsAllowed=0` 时，IfHealthyBudget 不应仅因“剩余预算为零”拒绝该不健康目标；若健康数降到 1，则不能照搬该放行结论。区分“配置值为零”与“当前剩余预算为零”。
- **Running 但未健康、`AlwaysAllow`**：不受上述健康预算条件限制，且不扣减 `disruptionsAllowed`；仍可能存在其他准入、删除或 drain 阻塞。

因此 **`disruptionsAllowed=0` 不能推出所有目标都不可驱逐**，健康 Pod 仍受保护；零预算 + `AlwaysAllow` + 单个 Running/Ready=False 的来源推演反例说明该目标不会因零预算被拒，但不保证整次 drain 必然成功。

节点身份与账本：Node 名唯一，同名即视为同一对象；替换节点应先删后建，否则状态、标签与分配可能混在一起（[nodes](https://v1-32.docs.kubernetes.io/docs/concepts/architecture/nodes/)）。node controller 默认 5 秒检查节点，Ready=Unknown 后默认 5 分钟才发起驱逐，并有限速；失联期间删除决定无法送达 kubelet，Pod 可能继续在分区节点运行（[taint-and-toleration](https://v1-32.docs.kubernetes.io/docs/concepts/scheduling-eviction/taint-and-toleration/)）。

### Slurm 路径

| 步骤 | 检查或动作 | 运行影响 | 预期证据与解释 | 下一步 |
|---|---|---|---|---|
| 1 | 记录节点 State、Reason、运行/挂起作业 | 只读 | DRAIN/DRAINING/DOWN 语义不同；Reason 为管理员填写 | 选择 DRAIN 或 DOWN |
| 2 | `scontrol update NodeName=<node> State=DRAIN` | 不再启动新作业；既有作业跑完后节点呈 DRAINED | 作业继续运行；节点状态可查 | 等待作业结束或按策略取消 |
| 3 | 需要立即终止时用 `State=DOWN` | 终止全部运行与挂起作业 | 作业被终止，节点不收新作业 | 确认是否可重排队与 Checkpoint |
| 4 | 取消与重排（分开处理） | 高影响 | `scancel` 默认 SIGCONT→SIGTERM→`KillWait`→SIGKILL；只取消 step 或只发信号不释放整个 job 分配；`sbatch --requeue` 是**重排资格**，`scontrol requeue` 是**重排动作**；重排后脚本从头执行、JobID 不变，但不等于应用自动从 Checkpoint 续算 | 训练先确认 Checkpoint 与数据游标；记录重排次数与执行身份 |
| 5 | 等待 COMPLETING 收敛 | 只读/等待 | 节点 `COMPLETING` 需 job 进程全部终止且 Epilog 已结束才清除；关联 job/step、重启计数/时点、slurmd/slurmstepd、进程/cgroup 与 Epilog 起止/返回状态 | 未收敛保持隔离；不以 RESUME、重启 daemon 或删账本代替清理 |
| 6 | 注册/状态恢复（不开放生产） | `State=RESUME` 使节点回到 IDLE + NoResp 并触发 slurmd 重注册；该动作会改变后续调度条件 | **执行前必须先启用并核实生产排除控制**（站点已配置、可覆盖 `DRAIN` 的维护 reservation、专用分区或允许清单）；注册成功后清 NoResp，普通生产仍被该控制阻断；无可用控制则不得 `RESUME`，停止并记 unknown | 验证通过后撤销验证例外并开放普通生产；失败则恢复/维持生产隔离 |
| 7 | 定时恢复 | `ResumeAfter=<秒>`，-1 取消 | 用于计划维护窗口；同样受生产准入门槛约束 | 与 `ReturnToService` 区分：后者是节点启动后自动恢复策略 |
| 8 | 重启节点 | `scontrol reboot [ASAP] [nextstate=RESUME\|DOWN]` | 节点加 REBOOT flag，空闲后经 RebootProgram 重启；ASAP 同时 DRAIN；ResumeTimeout 内未重启会标 DOWN | 确认 nextstate 与作业影响 |
| 9 | 电源管理场景 | `power_down`/`power_down_asap`/`power_down_force` | ASAP = drain + 下电；FORCE = 取消全部作业 + 下电；ResumeTimeout 默认 60 秒，未注册则 DOWN 并重排 | 核对分区与电源程序 |

Slurm 的关键语义（[scontrol 24.11.7](https://slurm.schedmd.com/archive/slurm-24.11.7/scontrol.html)、[power_save](https://slurm.schedmd.com/archive/slurm-24.11.7/power_save.html)、[slurmd](https://slurm.schedmd.com/archive/slurm-24.11.7/slurmd.html)）：`DRAIN` 不终止既有作业；`DOWN` 会终止运行与挂起作业；`RESUME` 不是实际节点状态，而是把 DRAIN/DRAINING/DOWN/REBOOT 改为 IDLE + NoResp，随后依赖 slurmd 重注册；`UNDRAIN` 只清 drain，若基态是 DOWN 仍需有效注册才排新作业。Epilog 非零会让节点 DRAIN；Prolog 非零会 DRAIN 并重排（默认 held）。`slurmd -c` 用于异常终止后清系统锁，`-b` 上报节点已重启；`ResumeTimeout` 超时会标 DOWN 并重排其上作业。

### 按负载类型的责任边界

| 负载 | 停止准入后的动作 | 平台责任 | 应用责任 | 重新准入前检查 |
|---|---|---|---|---|
| 训练 | 等待 Checkpoint 或按预算取消 | 保留作业/容器状态，按 `KillWait`/优雅期终止 | 落 Checkpoint、记录数据游标与 step；弹性训练处理成员变更 | 新任务从 Checkpoint 恢复并产生持续进展 |
| 在线服务 | 按 PDB 逐个驱逐 | 维护 Endpoint 摘除、优雅期与副本预算 | 完成在途请求、释放设备 | 新副本 ready 且请求成功率/延迟达标 |
| 有状态服务 | 完全终止后再重建 | 卷 detach/attach、PVC 保护 | 刷盘、释放锁、确认数据一致性 | 数据可读、副本关系正确 |
| 批处理 | 可取消或等待完成 | Job TTL/GC、重试策略 | 幂等、可重跑 | 输出完整、账本无重复分配 |

## 状态序列例子（来源支持，未执行）

**Kubernetes（来源例子）**：[disruptions 页的 PodDisruptionBudget example](https://v1-32.docs.kubernetes.io/docs/concepts/workloads/pods/disruptions/) 给出 node-1..3 与 pod-a/b/c，PDB `minAvailable=2`；drain node-1 可成功；pod-d 尚未 Ready 时，drain node-2/node-3 会被阻塞；pod-e 处于 Pending 时需要新节点。这个例子说明“驱逐被预算与健康状态阻塞”的状态变化，**不是本库执行记录**。

**Slurm（来源语义推演）**：`State=DRAIN` → 既有作业继续运行至完成 → `DRAINED` → **启用并核实生产排除控制** → `State=RESUME` / slurmd 重注册 → `IDLE` + NoResp → 受控验证 → **撤销验证例外后才排普通生产作业**。若 Epilog 返回非零，节点转 `DRAIN`；若作业长期 `COMPLETING`，节点在该状态停留，直到进程全部终止且 Epilog 结束。

两个序列都只作为来源支持的状态例子；现场的时间顺序、输出与结果须以实际证据为准，不能把推演写成已执行。

## 观测与异常

| 现象 | 首先看什么 | 不能据此下什么结论 |
|---|---|---|
| Pod 长时间 `Terminating` | finalizer、PDB、kubelet 是否可达、VolumeAttachment | 不能直接强删；强摘 finalizer 可能留下卷或设备残留 |
| 驱逐返回 429 | 响应内容、PDB 状态、API 限流证据 | 不能唯一归因 PDB；PDB 有预算时仍可能是 API 限流 |
| drain 一直不结束 | PDB 零预算、unhealthy Pod、DaemonSet/static Pod、`--timeout` | 不能把“命令没返回”当成“节点已清空” |
| 节点显示空闲但新任务仍等待 | 插件 allocatable、污点/容忍、设备健康、账本与实体差异 | 不能只看 `nvidia-smi`/`npu-smi` 的“空闲” |
| 容器仍能访问设备 | 残留进程、device cgroup、运行时 hook、static Pod | 不能把“Pod 已删”当成“设备已释放” |
| Pod/容器身份与账本不一致 | Pod UID、容器 ID/ATTEMPT、PodResources、设备分配记录 | 数量一致不等于同一执行，也不等于分配已释放 |
| Slurm 作业在 DRAIN 后仍运行 | DRAIN 与 DOWN 的语义差异 | 不能把 DRAIN 当成立即终止 |
| Slurm 节点长期 `COMPLETING` | job/step 进程、Epilog 起止与返回码、slurmd/slurmstepd、重启计数 | 不能以 RESUME、重启 daemon 或删账本代替清理 |
| 节点重启后账本矛盾 | 同名节点是否重建、slurmd 重注册、ResumeTimeout、过期分配 | 不能直接删节点对象“修复”账本 |

## 停止条件与恢复安排

出现以下情况时停止摘除并保留现场：

- drain 被 PDB 长期阻塞，且继续等待会超出维护窗口。
- 卷无法 detach、CSI 报错，或出现 force detach 风险。
- 设备插件上报与实际设备不一致，或设备健康告警持续。
- Slurm 节点在 RESUME 后长期 NoResp/注册失败，或作业重排循环。
- 控制面/账本出现重复分配、过期分配或对象身份冲突。

恢复安排（**普通生产准入只能在验证通过后开放，但注册/状态恢复可在生产排除控制生效后先发生**）：

1. **保持隔离并保存证据**：Kubernetes 保持 cordon（或相应污点），Slurm 保持 `DRAIN`；保存节点、Pod/Job、设备、卷、运行时与账本状态。
2. **排除冲突**：确认旧进程/容器已退出、设备分配与实体一致、卷已卸载或明确保留、没有过期/重复分配。
3. **基础设施门槛与注册**：完成设备/卷/网络与控制器检查。若注册/状态恢复需要 `RESUME` 或其他改变调度条件的动作，**必须先启用并核实生产排除控制**（见下节），再执行该动作；无法同时保持普通生产阻断时停止并记 unknown。
4. **受控验证**：在普通生产仍被阻断的前提下，由授权方发起限定节点/镜像/设备身份的验证负载，观察 Checkpoint/step、请求成功、数据读回与账本释放；失败则回到隔离。
5. **开放生产准入（按当前状态分支）**：验证通过后先撤销验证例外与独立生产排除控制。若节点在注册阶段已经 `RESUME`/`uncordon`，**只解除剩余生产排除控制，不重复执行 `RESUME`/`UNDRAIN`**；若节点仍处于 `DRAIN`/cordon，才执行 `RESUME`/`UNDRAIN`/`uncordon`。两种分支都要记录当前状态、解除了哪项控制及核实证据。

**“节点回到 Ready/IDLE”不等于“资源已回收”，也不等于“可以开放生产准入”。** 不得先放开普通生产准入再补验证；`RESUME` 若在验证前用于注册，必须处于已验证的生产排除控制之下。

## 验证准入与对账记录（最小方案）

### 三层门槛必须分开

| 层 | 目的 | 允许的动作 | 不允许的替代 |
|---|---|---|---|
| 基础设施恢复 | 让节点/daemon/插件回到可检查状态 | 先启用生产排除控制，再完成注册、状态恢复与只读检查 | 在无生产排除控制时 `RESUME`/`UNDRAIN`/`uncordon` |
| 验证专用准入 | 只让受控验证负载进入 | Kubernetes：cordon + **指定 effect 的污点**（如 `NoSchedule`/`NoExecute`）；验证 Pod 必须容忍相应污点。`nodeName` 只绕过调度器，**不豁免未容忍的 `NoExecute`**；专用 namespace 只是组织边界，不能单独阻断生产 Pod。Slurm：站点已配置并核实、可覆盖 `DRAIN` 的维护 reservation、专用分区或允许清单 | 编造通用旁路命令；以“专用 namespace”或单独 `nodeName` 代替节点级准入控制；放开生产后再“碰运气” |
| 普通生产准入 | 恢复常规调度 | 验证通过后撤销验证例外与独立生产排除控制；已恢复的节点不重复 `RESUME`/`UNDRAIN`，仍隔离的节点才执行 `uncordon`/`RESUME`/`UNDRAIN` | 把“节点 Ready/IDLE”或“注册成功”当作验证通过；对已恢复节点重复状态变更 |

验证专用入口必须在执行前记录：谁批准、哪项控制持续阻断普通生产作业、注册/状态恢复何时允许。**若站点无法在保持普通生产被阻断的同时完成注册或启动验证作业，停止并记 unknown**，不自行设计绕过调度的办法。验证失败时撤销验证例外并恢复生产隔离；再次代入“CSI 未卸卷”“设备仍有过期分配”“验证失败”三种情形，均不得放行普通生产。

### 身份账本（最小字段）

| 字段 | Kubernetes | Slurm |
|---|---|---|
| 节点身份 | Node 名称/UID、创建时间 | NodeName、启动/注册标识 |
| 执行身份 | Pod UID、容器 ID、ATTEMPT | JobID/StepID、重启计数 |
| 分配 ID | 插件上报的资源名与设备 ID | GRES/TRES 分配记录 |
| 实际设备身份 | PodResources 的 `device_ids`、容器内设备节点及映射依据 | `SLURM_JOB_GPUS`、cgroup 与设备节点 |
| 观察时间 | 与其他层同一时间窗口 | 与其他层同一时间窗口 |
| 重启边界 | kubelet/插件重启后旧观察作废 | slurmd/slurmctld 重启后旧观察作废 |

PodResources 的 List 结构只给出 namespace、Pod/container 名称与插件的 `resource_name`/`device_ids`，**不直接给出 Pod UID、运行时容器 ID 或 ATTEMPT**；必须用同期的 API/CRI 证据把名称与 UID/容器 ID/ATTEMPT 对齐，无法唯一连接时记 unknown。设备的具体映射方法按插件/平台核实，不把 GPU 相对编号外推成 NPU 保证。旧进程退出、旧平台分配释放、新验证 attempt 获得正确分配是三项分别核对的条件；重启后必须重新采集，不能沿用旧快照。

### 验证记录（执行前审定）

- **身份与归属**：批准人/发起人、验证 Pod/Job/Step/attempt、镜像与数据/Checkpoint 版本、期望结果、证据确认人。
- **覆盖范围**：设备获得与使用、选定网络端点/通信路径、训练恢复后的持续 step、服务请求成功率/延迟、状态数据读回；不适用项须说明原因。
- **判断门槛**：观察窗口与进展/成功率/延迟/一致性基线；无基线记 unknown 并阻止通过，不只写“达标”。
- **结束与清理**：验证负载退出后，设备分配、卷、网络端点与账本再次收敛，才作最终生产放行；失败或证据缺失返回隔离并保存证据。

## 完成判据

- 停止准入已生效，且维护期间的允许残留清单（DaemonSet、static Pod、容忍/直接绑定等）已核对；不能把 cordon/DRAIN 当作“没有新负载”的证明。
- drain/终止前已完成本地数据与恢复点确认：emptyDir 可丢弃或已持久化，Checkpoint/备份可读回且不依赖即将离线的唯一副本；hostPath/local PV 的保留、迁移或擦除有授权记录。
- 目标负载按类型完成终止：训练有 Checkpoint/恢复点，服务满足 PDB 与优雅期，有状态负载完成刷盘与卷处理；Slurm 作业/step 已退出且 Epilog 已结束，节点不再停留 `COMPLETING`。
- 身份与账本可对账：Kubernetes 以 Pod UID、容器 ID/ATTEMPT、PodResources 与设备分配记录关联；Slurm 以 job/step、重启计数、slurmd/slurmstepd 与 Epilog 状态关联。旧执行退出与平台分配释放是分别核对的条件，数量一致不能代替身份一致。
- 设备、卷、网络端点与运行时残留均已核对；账本与实体一致，没有过期/重复分配。
- 已按[验证准入与对账记录](#验证准入与对账记录最小方案)的三层门槛执行：验证专用入口经授权且可核实，身份账本按节点/执行/分配/实际设备/时间/重启边界连接；验证负载退出后设备、卷、端点与账本再次收敛，才开放普通生产准入。已恢复的节点只解除剩余生产排除控制，不重复 `RESUME`/`UNDRAIN`；仍隔离的节点才执行状态变更。
- 未执行的验证、缺失的驱动/CSI 证据与站点参数保留为 unknown；不以“命令成功”替代应用成功。

## 来源与验证记录

- [Kubernetes v1.32 — Safely Drain a Node](https://v1-32.docs.kubernetes.io/docs/tasks/administer-cluster/safely-drain-node/)
- [Kubernetes v1.32 — kubectl drain](https://v1-32.docs.kubernetes.io/docs/reference/kubectl/generated/kubectl_drain/)
- [Kubernetes v1.32 — API-initiated Eviction](https://v1-32.docs.kubernetes.io/docs/concepts/scheduling-eviction/api-eviction/)
- [Kubernetes v1.32 — Pod Disruption Budgets](https://v1-32.docs.kubernetes.io/docs/concepts/workloads/pods/disruptions/)
- [Kubernetes v1.32 — Node Shutdown](https://v1-32.docs.kubernetes.io/docs/concepts/cluster-administration/node-shutdown/)
- [Kubernetes v1.32 — Nodes](https://v1-32.docs.kubernetes.io/docs/concepts/architecture/nodes/)
- [Slurm 24.11.7 — scontrol](https://slurm.schedmd.com/archive/slurm-24.11.7/scontrol.html)
- [Slurm 24.11.7 — power_save](https://slurm.schedmd.com/archive/slurm-24.11.7/power_save.html)
- 当前验证范围：未执行。待确认：站点 PDB/超时/`ReturnToService` 参数、CSI 驱动 detach 行为、Ascend 节点摘除时的设备复位与残留清理（无一手文档）。
