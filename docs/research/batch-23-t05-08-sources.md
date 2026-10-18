# 第二十三批 T05-08 来源记录

任务：T05-08（节点摘除、drain 与资源回收流程，procedure 类新文章的知识材料）。取证轮次：只读取证子代理首轮（2026-10-18）。FetchURL 只读打开 Kubernetes v1.32 静态快照 10 页＋Slurm 24.11.7 归档 3 页（slurmd/power_save 为本轮新开，scontrol 为重开核对节点 State/reboot 精确措辞）。`https://slurm.schedmd.com/archive/slurm-24.11.7/node_states.html` 返回 HTTP 404（该归档无此页，节点状态口径以 sinfo/scontrol/power_save 页为准）。curl 字节级取回未执行；未执行任何 drain/驱逐/scontrol 命令，仅取官方语义材料。scontrol 页体量超上限，FetchURL 提取文本落盘后用 Grep 检索核对，下文所注行号为提取文本文件行号、非 HTML 源行号。

版本声明：固定 **Kubernetes v1.32**（全部 K8s URL 使用 `https://v1-32.docs.kubernetes.io/` 静态快照，页头自带 "no longer actively maintained… static snapshot" 声明；未使用 kubernetes.io 可变当前页）与 **Slurm 24.11.7**（`https://slurm.schedmd.com/archive/slurm-24.11.7/` 静态归档，man2html 生成时间 2025-11-11 GMT）。取证方式全部为 FetchURL 只读。

## 主张—来源定位表（ID—精确页面/节—字段/支持范围）

| 主张 | 登记 ID | 精确页面/节 | 支持范围 / 未覆盖 |
|---|---|---|---|
| cordon→drain 流程与完成语义 | NEW src.kubernetes.node-drain-v1-32 | [safely-drain-node](https://v1-32.docs.kubernetes.io/docs/tasks/administer-cluster/safely-drain-node/)（"Use kubectl drain…" 节） | drain 成功返回＝非豁免 Pod 已按优雅期与 PDB 安全驱逐，此后才可关机/删 VM；维护后 `kubectl uncordon` 恢复调度；多节点并行 drain 仍受 PDB 约束；drain 建议先配 PDB 且 PDB 宜设 `AlwaysAllow` unhealthyPodEvictionPolicy。未覆盖：站点实际 PDB 配置 |
| kubectl drain 旗标语义 | NEW src.kubernetes.node-drain-v1-32 | [kubectl_drain 参考页](https://v1-32.docs.kubernetes.io/docs/reference/kubectl/generated/kubectl_drain/)（Synopsis/Options，自动生成页） | drain 先把节点标 unschedulable 再驱逐；mirror Pod 不经 API 删除故不在 drain 范围；有 DaemonSet Pod 时不带 `--ignore-daemonsets` 不继续，且任何情况下不删 DS Pod（DS 控制器立即重建并无视 unschedulable）；无控制器 Pod 须 `--force`；`--delete-emptydir-data` 才继续删 emptyDir 本地数据；`--grace-period` 默认 -1（用 Pod 自带值）；`--timeout` 0＝无限；`--disable-eviction` 绕过 PDB 直接 DELETE（须慎用）；`--skip-wait-for-delete-timeout`；"drain waits for graceful termination. You should not operate on the machine until the command completes." |
| API-initiated Eviction 语义 | NEW src.kubernetes.eviction-pdb-v1-32 | [api-eviction](https://v1-32.docs.kubernetes.io/docs/concepts/scheduling-eviction/api-eviction/)（全页） | policy/v1 Eviction 对象（v1beta1 并列展示）；准入三响应：200 允许（≈受策略控制的 DELETE）/429 可能为 PDB 不允许，也可能为 API 限流（需结合响应与限流证据）/500 配置错误（如多 PDB 选中同一 Pod）；无 PDB 的 Pod 一律 200；允许后六步：打 deletionTimestamp＋优雅期→kubelet 优雅停 Pod→控制面从 Endpoint/EndpointSlice 摘除→优雅期满 kubelet 强杀→kubelet 上报→API 删 Pod；stuck eviction 处置（中止自动化或改为直接删 Pod）。未覆盖：具体集群速率限制配置 |
| PDB 条件与语义 | NEW src.kubernetes.eviction-pdb-v1-32 | [disruptions](https://v1-32.docs.kubernetes.io/docs/concepts/workloads/pods/disruptions/)＋[configure-pdb](https://v1-32.docs.kubernetes.io/docs/tasks/run-application/configure-pdb/)（全页） | minAvailable/maxUnavailable 整数或百分比（min 向上取整、max 可取整超出）；健康判定＝`.status.conditions[type=Ready]=True`；`unhealthyPodEvictionPolicy` 默认 IfHealthyBudget（需核对 currentHealthy/desiredHealthy，不能只看 disruptionsAllowed；CrashLoopBackOff 等可卡住 drain），AlwaysAllow 可驱逐不健康 Pod 且不扣减 disruptionsAllowed；maxUnavailable=0 或 minAvailable=100% 时**健康 Pod** 的零自愿驱逐会使 drain 无法完成，但不健康 Pod 在 AlwaysAllow 下有例外；任意/重叠选择器：被多 PDB 覆盖的 Pod 驱逐被拒；involuntary 不计入可阻止范围但占预算；滚动更新不受 PDB 限制；DisruptionTarget condition 五种 reason（PreemptionByScheduler/DeletionByTaintManager/EvictionByEvictionAPI/DeletionByPodGC/TerminationByKubelet）；批作业建议不配 PDB（Job 控制器自补 Pod） |
| 优雅/非优雅节点关闭 | NEW src.kubernetes.node-shutdown-v1-32 | [node-shutdown](https://v1-32.docs.kubernetes.io/docs/concepts/cluster-administration/node-shutdown/)（全页） | 优雅关闭依赖 systemd inhibitor；`shutdownGracePeriod`/`shutdownGracePeriodCriticalPods` 默认 0＝不启用；触发后 Node 置 NotReady reason="node is shutting down"，调度器不排新 Pod，kubelet 在 PodAdmission 阶段亦拒绝；两阶段终止（常规→关键）与按 PriorityClass 分桶；kubelet 指标 graceful_shutdown_start/end_time_seconds；非优雅：人工打 `node.kubernetes.io/out-of-service`（NoExecute 或 NoSchedule）污点→无匹配容忍的 Pod 强删＋卷立即 detach；StatefulSet Pod 否则卡 terminating 且 VolumeAttachments 不删；6 分钟未删 Pod→force detach（可用 kube-controller-manager `disable-force-detach-on-timeout` 关闭），强摘违背 CSI 规范顺序（ControllerUnpublish 须在 NodeUnstage/NodeUnpublish 成功之后）可能数据损坏；Windows 优雅关闭 v1.32 为 alpha 默认关 |
| 节点身份、心跳与 node controller | NEW src.kubernetes.node-lifecycle-v1-32 | [nodes](https://v1-32.docs.kubernetes.io/docs/concepts/architecture/nodes/)（Management/Node name uniqueness/heartbeats/Node controller 节） | Node 名唯一且同名即视为同一对象（含状态/标签），替换节点须先删后建，否则账本不一致；kubelet `--register-node` 自注册与 `--register-with-taints`；`kubectl cordon`＝标 unschedulable（维护预备步骤，不影响既有 Pod）；心跳＝Node status 更新＋kube-node-lease Lease；node controller 默认 5 s 检查节点、Ready=Unknown 后默认 5 分钟才发起驱逐、限速 `--node-eviction-rate` 默认 0.1/s、不健康区阈值 0.55 时降速 0.01/s、≤50 节点小集群整区不健康停驱逐、全区不健康不驱逐 |
| 污点驱逐语义 | NEW src.kubernetes.node-lifecycle-v1-32 | [taint-and-toleration](https://v1-32.docs.kubernetes.io/docs/concepts/scheduling-eviction/taint-and-toleration/)（Taint based Evictions 节） | NoExecute 立即驱逐不容忍 Pod；`tolerationSeconds` 限时绑定；七个内建污点（not-ready/unreachable/三种 pressure/network-unavailable/unschedulable 等）；节点失联期间删除决定无法下达 kubelet，Pod 可能继续在分区节点运行；DaemonSet Pod 自动带 not-ready/unreachable 无超时 NoExecute 容忍（不因此类问题被驱逐）；手动指定 `.spec.nodeName` 绕过调度器 |
| DaemonSet 语义 | NEW src.kubernetes.daemonset-static-pod-v1-32 | [daemonset](https://v1-32.docs.kubernetes.io/docs/concepts/workloads/controllers/daemonset/)（How Daemon Pods are scheduled/Taints and tolerations/Updating 节） | DS 控制器为每个合格节点建 Pod 并立即补建缺失 Pod；自动容忍表（含 `node.kubernetes.io/unschedulable:NoSchedule`，故 drain/cordon 节点上 DS Pod 仍调度）；节点移出集群时 DS Pod 被 GC；删除 DS 清理其 Pod（`--cascade=orphan` 例外且可被同名新 DS 收养）；DS 重启策略恒 Always |
| static Pod 语义 | NEW src.kubernetes.daemonset-static-pod-v1-32 | [static-pod](https://v1-32.docs.kubernetes.io/docs/tasks/configure-pod-container/static-pod/)（全页） | kubelet 直接管理、apiserver 观测但不可控；mirror Pod 名带节点主机名后缀，`kubectl delete` mirror 后 kubelet 不删 static Pod；manifest 目录（staticPodPath）扫描动态增删；`crictl ps` 输出含 ATTEMPT 列（重启计数观测入口）；停容器后 kubelet 自动重启 |
| 卷/CSI 回收边界 | NEW src.kubernetes.storage-reclaim-v1-32 | [persistent-volumes](https://v1-32.docs.kubernetes.io/docs/concepts/storage/persistent-volumes/)（Reclaiming/finalizer/in-use protection 节）＋[volumes](https://v1-32.docs.kubernetes.io/docs/concepts/storage/volumes/)（emptyDir/hostDir/local 节） | 回收策略 Retain（人工三步）/Delete（连后端存储一起删，动态供给继承 StorageClass 默认 Delete）/Recycle（v1.32 仅 nfs 与 hostPath 支持）；in-use protection：Pod 在用的 PVC 与已绑定 PV 删除被推迟，finalizer 分别为 `kubernetes.io/pvc-protection`/`kubernetes.io/pv-protection`；CSI 卷（动态与静态）自 v1.31 起加 `external-provisioner.volume.kubernetes.io/finalizer`，确保 Delete 策略下后端删完才删 PV 对象；emptyDir 随 Pod 以任何原因离开节点而永久删除；hostPath 无生命周期管理；local 卷节点不健康即不可访问、应用须容忍数据丢失；PV 四 phase（Available/Bound/Released/Failed）与 lastPhaseTransitionTime |
| kubelet 重启后设备插件行为 | 复用 src.kubernetes.device-plugins-v1-32 | device-plugins 页 Handling kubelet restarts / Device plugin and unhealthy devices / Monitoring 节（Batch 21 与 T05-04 轮已核对） | 新 kubelet 启动删除 device-plugins 目录下 socket、插件监测自身 socket 删除并重注册；不健康设备 allocatable 降/capacity 不变/既有 Pod 保持分配；PodResources List/GetAllocatableResources/Get 观测端点。本轮未重开 |
| Slurm 节点 DRAIN/DOWN/RESUME/UNDRAIN | 复用 src.slurm.docs-24.11.7（本轮重开 scontrol 补充核对，见建议登记条目说明） | [scontrol.html](https://slurm.schedmd.com/archive/slurm-24.11.7/scontrol.html) NODES - UPDATE `State=` 节（提取文本约 L1362–1411） | DRAIN：不再启动新作业，既有作业跑完后节点呈 DRAINED；DOWN：终止全部运行与挂起作业且不收新作业；RESUME 非实际节点状态：把 DRAIN/DRAINING/DOWN/REBOOT 改为 IDLE＋NoResp，slurmctld 随后要求 slurmd 重注册，注册成功后清 NoResp；UNDRAIN 清 drain 但不改基态（如 DOWN），需有效节点注册后才排新作业；`ResumeAfter=<秒>` 可定时恢复（-1 取消）；`Reason=` 为 DOWN/DRAINED/DRAINING/FAILING/FAIL 记原因 |
| Slurm reboot 程序与账本 | 复用 src.slurm.docs-24.11.7（本轮重开 scontrol 补充核对） | [scontrol.html](https://slurm.schedmd.com/archive/slurm-24.11.7/scontrol.html) `reboot` 命令节（提取文本约 L227–264） | `reboot [ASAP] [nextstate={RESUME|DOWN}] [reason=]`：节点加 REBOOT flag，空闲后经 RebootProgram 重启；ASAP 加 DRAIN flag 阻止新作业且 nextstate 默认 UNDRAIN；重启后 slurmd 起来先跑一次 HealthCheckProgram 再向 slurmctld 注册并清 REBOOT；reason 依次追加 "reboot issued"/"reboot complete"/"reboot timed out"；ResumeTimeout 内未重启→标 DOWN；FUTURE/POWER_DOWN/POWERED_DOWN/POWERING_DOWN/REBOOT_ISSUED/REBOOT_REQUESTED 状态忽略 reboot；`scontrol cancel_reboot` 或 State=CANCEL_REBOOT 撤销 |
| Slurm slurmd 节点 daemon | NEW src.slurm.node-power-lifecycle-24.11.7 | [slurmd.html](https://slurm.schedmd.com/archive/slurm-24.11.7/slurmd.html)（DESCRIPTION/OPTIONS/SIGNALS 节） | slurmd 监视本节点任务、接受/启动/按要求杀掉任务；SIGTERM/SIGINT/SIGQUIT 干净关闭，SIGHUP 重读配置（同 `scontrol reconfigure`）；`-c` 异常终止后清系统锁；`-b` 上报节点已重启（测试用）；`-M` mlockall 防重 swap 期被标 DOWN；`--systemd` 支持 reconfigure 换 PID |
| Slurm power_save 生命周期与手动电源态 | NEW src.slurm.node-power-lifecycle-24.11.7 | [power_save.html](https://slurm.schedmd.com/archive/slurm-24.11.7/power_save.html)（Overview/Configuration/Node Lifecycle/Manual Power Saving/Fault Tolerance 节） | IDLE 超 SuspendTime→SuspendProgram 挂起；ResumeTimeout（默认 60 s）内 slurmd 未以新 BootTime 注册→节点 DOWN＋其上作业重排，此后再重启的节点标 DOWN 且 reason="Node unexpectedly rebooted"；状态符号 POWER_DOWN(!)/POWER_UP/POWERED_DOWN(~)/POWERING_DOWN(%)/POWERING_UP(#)；手动 `state=power_down/power_down_asap/power_down_force/power_up`：ASAP＝drain＋标下电（作业先跑完、不再分新作业），FORCE＝取消全部作业＋下电＋回 IDLE；ResumeProgram/SuspendProgram 以 SlurmUser 在 slurmctld 所在节点运行、无时限但须自行容错，ctld 优雅退出最多等 10 s；SLURM_RESUME_FILE（JSON 作业↔节点映射）须在程序启动 10 s 内使用；分区委派 PowerDownOnIdle 的 COMPLETING→IDLE 三条件 |
| Slurm 作业结束/清理/信号 | 复用 src.slurm.docs-24.11.7 | [job_state_codes](https://slurm.schedmd.com/archive/slurm-24.11.7/job_state_codes.html)（COMPLETING flag）/[prolog_epilog](https://slurm.schedmd.com/archive/slurm-24.11.7/prolog_epilog.html)（Epilog 非零→DRAIN；Prolog 非零→DRAIN＋重排默认 held）/[scancel](https://slurm.schedmd.com/archive/slurm-24.11.7/scancel.html)（默认 SIGCONT→SIGTERM→KillWait→SIGKILL）/[sinfo](https://slurm.schedmd.com/archive/slurm-24.11.7/sinfo.html)（DRAINED/DRAINING/DOWN 节点态显示）（Batch 22 已核对） | 支撑"任务结束流程"与"drain 由 Prolog/Epilog 失败触发"主张；COMPLETING 清理时长无承诺。本轮未重开这些页 |
| 训练负载 Checkpoint/弹性入口 | 复用 src.pytorch.elastic-2.6 | elastic/train_script.html（checkpoint 是恢复前提）、elastic/run.html 与 run.py L490–497（torchrun max-restarts CLI 默认 0，WorkerSpec API 默认 3）（前轮已核对） | 支撑"训练负载停止准入须先落 checkpoint、重准入后从 checkpoint 恢复验证进展"主张；未覆盖各训练框架自定义 ckpt 语义。本轮未重开 |
| K8s Job/属主/GC 账本 | 复用 src.kubernetes.job-lifecycle-v1-32＋src.kubernetes.api-gc-v1-32 | Job 概念页（backoffLimit/TTL/finalizer）/garbage-collection（级联删除）（Batch 22 已核对） | 支撑"训练/批负载删除后由 TTL/GC 收尾、finalizer 卡住则对象滞留"主张。本轮未重开 |
| Ascend/MindCluster 设备账本 | 复用 src.ascend.mind-cluster-v26.1.1 | ascend-device-plugin Register/ListAndWatch/Allocate 实现（第二批/第十批已核对） | 支撑"设备账本以插件注册/上报为准"主张；节点摘除时的设备复位、NPU 进程残留清理无文档（unknown）。本轮未重开 |
| 状态例子（来源支持） | NEW src.kubernetes.eviction-pdb-v1-32＋复用 src.slurm.docs-24.11.7 | disruptions 页 "PodDisruptionBudget example" 节；scontrol State= 节 | K8s：node-1..3、pod-a/b/c＋PDB minAvailable=2，drain node-1 成功、pod-d 未 Ready 前 drain node-2/node-3 被阻塞、pod-e Pending 时需加节点——drain 阻塞/恢复的状态序列；Slurm：State=DRAIN→作业完成→DRAINED→State=RESUME→IDLE＋NoResp→注册成功恢复——drain/重准入状态序列 |

## unknown 清单

1. Slurm 24.11.7 归档无 `node_states.html`（HTTP 404，2026-10-18 实开确认）；节点状态口径只能由 sinfo/scontrol/power_save 页拼装，无单页状态机图（power_save 页有含电源态的生命周期图，但非全量状态机）。
2. MindCluster/Ascend 在节点摘除时的设备复位、NPU 侧残留进程/显存清理：无一手文档；既有 src.ascend.mind-cluster-v26.1.1 仅核对插件注册/分配路径，不含 drain 专属行为。禁止把 NVIDIA 或其他平台机制套用过来。
3. 站点实际参数（ResumeTimeout/KillWait/PDB 值/集群污点与容忍/超时配置）：unknown，须读现场配置；文档默认值见上表各行。
4. kubectl drain 对 hostPath 与 local PV 数据的处置：文档只承诺 emptyDir 由 `--delete-emptydir-data` 把关；hostPath 无生命周期管理、local 卷随节点不可用而不可访问，节点删除后 local 数据如何处置无文档承诺。
5. Windows 节点优雅关闭在 v1.32 为 alpha 且默认关；本材料全部为 Linux 语义。
6. 具体 CSI 驱动的 detach/Unmount 超时与重试交互（除通用 6 分钟 force detach 外）：无驱动级文档。
7. Slurm 动态节点（`-Z`/`-F`/FUTURE/CLOUD）在 drain/回收路径上的额外细节未展开（仅 slurmd 页选项说明）。
8. K8s 节点删除（删 Node 对象）后 kubelet 侧残留卷目录/镜像的清理时序：本轮未取专项页（仅 node-shutdown 页覆盖 VolumeAttachment/force detach 侧）。
9. 全部实测未做：未执行 drain/驱逐/scontrol/断电；设备可用≠应用成功。

## 建议登记条目

以下 7 条为新增建议（本轮均实开）；另对既有 `src.slurm.docs-24.11.7` 有一条**补充核对记录**（2026-10-18 本轮重开 scontrol.html，核对 `State=` 节 DOWN/DRAIN/RESUME/UNDRAIN/CANCEL_REBOOT 与 `ResumeAfter=`/`Reason=` 原文、`reboot` 命令节 ASAP/nextstate/REBOOT flag/HealthCheckProgram/reason 追加串/ResumeTimeout→DOWN/忽略状态清单/cancel_reboot，FetchURL 只读，提取文本行区间约 L227–264 与 L1347–1417，哈希未做字节级校验）。

```yaml
- id: src.kubernetes.node-drain-v1-32
  title: Kubernetes v1.32 节点 drain 文档与 kubectl drain 参考（静态快照）
  url: https://v1-32.docs.kubernetes.io/docs/tasks/administer-cluster/safely-drain-node/
  kind: documentation
  registered_at: '2026-10-18'
  revision: v1.32 documentation snapshot（静态快照页，页头标不再积极维护）；FetchURL 只读核对 2026-10-18；另实开同快照 kubectl_drain 自动生成参考页 https://v1-32.docs.kubernetes.io/docs/reference/kubectl/generated/kubectl_drain/
  license:
    status: partial
    scopes:
    - scope: Kubernetes website 仓库文档许可声明；main 链接为可变定位
      identifier: CC-BY-4.0
      url: https://github.com/kubernetes/website/blob/main/LICENSE
    notes: 沿用既有 K8s 文档条目（src.kubernetes.device-plugins-v1-32、src.kubernetes.job-lifecycle-v1-32）已登记的许可口径，本轮未重新打开 LICENSE 页；仅链接并原创归纳。
  notes: Batch 23（T05-08）取证：safely-drain-node（drain 完成语义、uncordon、并行 drain 与 PDB、建议 AlwaysAllow）与 kubectl_drain 参考（--ignore-daemonsets/--delete-emptydir-data/--force/--grace-period 默认 -1/--timeout 0 无限/--disable-eviction/--skip-wait-for-delete-timeout、mirror Pod 不经 API、DS Pod 不删）。未执行任何 drain 命令。
- id: src.kubernetes.eviction-pdb-v1-32
  title: Kubernetes v1.32 API-initiated Eviction 与 PodDisruptionBudget 文档（静态快照）
  url: https://v1-32.docs.kubernetes.io/docs/concepts/scheduling-eviction/api-eviction/
  kind: documentation
  registered_at: '2026-10-18'
  revision: v1.32 documentation snapshot；FetchURL 只读核对 2026-10-18；同轮实开 disruptions 与 configure-pdb 两页
  license:
    status: partial
    scopes:
    - scope: Kubernetes website 仓库文档许可声明；main 链接为可变定位
      identifier: CC-BY-4.0
      url: https://github.com/kubernetes/website/blob/main/LICENSE
    notes: 沿用既有 K8s 文档条目许可口径，本轮未重新打开 LICENSE 页；仅链接并原创归纳。
  notes: Batch 23（T05-08）取证：api-eviction（policy/v1 Eviction、200/429/500、删除六步序列、stuck eviction 处置）、disruptions（自愿/非自愿分类、PDB 语义、DisruptionTarget 五 reason、三节点 drain 状态例子）、configure-pdb（取整、健康判定 Ready=True、unhealthyPodEvictionPolicy 两策略及 IfHealthyBudget 的 currentHealthy/desiredHealthy 判断、零剩余预算对健康 Pod 的阻塞与 AlwaysAllow 不健康 Pod 例外、重叠选择器拒驱逐、任意负载限制）。未配置或触发任何 PDB。
- id: src.kubernetes.node-shutdown-v1-32
  title: Kubernetes v1.32 Graceful/Non-graceful Node Shutdown 文档（静态快照）
  url: https://v1-32.docs.kubernetes.io/docs/concepts/cluster-administration/node-shutdown/
  kind: documentation
  registered_at: '2026-10-18'
  revision: v1.32 documentation snapshot；FetchURL 只读核对 2026-10-18
  license:
    status: partial
    scopes:
    - scope: Kubernetes website 仓库文档许可声明；main 链接为可变定位
      identifier: CC-BY-4.0
      url: https://github.com/kubernetes/website/blob/main/LICENSE
    notes: 沿用既有 K8s 文档条目许可口径，本轮未重新打开 LICENSE 页；仅链接并原创归纳。
  notes: Batch 23（T05-08）取证：优雅关闭（systemd inhibitor、shutdownGracePeriod 系列默认 0、NotReady reason、两阶段与按优先级分桶、指标名）、非优雅关闭（out-of-service 污点→强删＋立即 detach、StatefulSet 卡 terminating 与 VolumeAttachment 滞留）、6 分钟 force detach 与 disable-force-detach-on-timeout、CSI 顺序违背与数据损坏风险、Windows alpha。未执行任何关机。
- id: src.kubernetes.node-lifecycle-v1-32
  title: Kubernetes v1.32 Node 架构与污点驱逐文档（静态快照）
  url: https://v1-32.docs.kubernetes.io/docs/concepts/architecture/nodes/
  kind: documentation
  registered_at: '2026-10-18'
  revision: v1.32 documentation snapshot；FetchURL 只读核对 2026-10-18；同轮实开 taint-and-toleration 页
  license:
    status: partial
    scopes:
    - scope: Kubernetes website 仓库文档许可声明；main 链接为可变定位
      identifier: CC-BY-4.0
      url: https://github.com/kubernetes/website/blob/main/LICENSE
    notes: 沿用既有 K8s 文档条目许可口径，本轮未重新打开 LICENSE 页；仅链接并原创归纳。
  notes: Batch 23（T05-08）取证：nodes（Node 名唯一性与同名同对象假设、自注册、cordon、心跳 Lease、node controller 5 s 检查/默认 5 分钟驱逐/限速 0.1/s/区域降级 0.01/s/小集群阈值 50）与 taint-and-toleration（NoExecute 语义、tolerationSeconds、七内建污点、失联期 Pod 续跑、DaemonSet 自动容忍）。未操作任何节点。
- id: src.kubernetes.daemonset-static-pod-v1-32
  title: Kubernetes v1.32 DaemonSet 与 Static Pod 文档（静态快照）
  url: https://v1-32.docs.kubernetes.io/docs/concepts/workloads/controllers/daemonset/
  kind: documentation
  registered_at: '2026-10-18'
  revision: v1.32 documentation snapshot；FetchURL 只读核对 2026-10-18；同轮实开 static-pod 任务页
  license:
    status: partial
    scopes:
    - scope: Kubernetes website 仓库文档许可声明；main 链接为可变定位
      identifier: CC-BY-4.0
      url: https://github.com/kubernetes/website/blob/main/LICENSE
    notes: 沿用既有 K8s 文档条目许可口径，本轮未重新打开 LICENSE 页；仅链接并原创归纳。
  notes: Batch 23（T05-08）取证：daemonset（逐节点建 Pod/立即补建/自动容忍表含 unschedulable:NoSchedule/删除级联与 orphan 收养）与 static-pod（kubelet 直管、mirror Pod 可见不可删、manifest 目录扫描增删、crictl ATTEMPT 列、kubelet 自动重启）。未创建或删除任何 Pod。
- id: src.kubernetes.storage-reclaim-v1-32
  title: Kubernetes v1.32 PV/PVC 回收与卷生命周期文档（静态快照）
  url: https://v1-32.docs.kubernetes.io/docs/concepts/storage/persistent-volumes/
  kind: documentation
  registered_at: '2026-10-18'
  revision: v1.32 documentation snapshot；FetchURL 只读核对 2026-10-18；同轮实开 volumes 概念页 emptyDir/hostPath/local 节
  license:
    status: partial
    scopes:
    - scope: Kubernetes website 仓库文档许可声明；main 链接为可变定位
      identifier: CC-BY-4.0
      url: https://github.com/kubernetes/website/blob/main/LICENSE
    notes: 沿用既有 K8s 文档条目许可口径，本轮未重新打开 LICENSE 页；仅链接并原创归纳。
  notes: Batch 23（T05-08）取证：persistent-volumes（Retain/Delete/Recycle 三策略与 v1.32 仅 nfs/hostPath 支持 Recycle、pvc-protection/pv-protection in-use finalizer、CSI external-provisioner finalizer 自 v1.31、PV 四 phase）与 volumes（emptyDir 随 Pod 离开节点永久删除、hostPath 无生命周期管理、local 卷节点绑定与数据丢失容忍）。未删除任何卷。
- id: src.slurm.node-power-lifecycle-24.11.7
  title: Slurm 24.11.7 slurmd 节点 daemon 与 power_save 生命周期（归档）
  url: https://slurm.schedmd.com/archive/slurm-24.11.7/slurmd.html
  kind: documentation
  registered_at: '2026-10-18'
  revision: 24.11.7 archive（静态归档，man2html 生成时间 2025-11-11 GMT）；FetchURL 只读核对 2026-10-18
  license:
    status: unknown
    scopes: []
    notes: SchedMD 站点许可未核对；只链接并原创归纳，未复制手册长段。
  notes: Batch 23（T05-08）取证：slurmd.html（daemon 职责、SIGTERM/SIGINT/SIGQUIT 干净关闭、SIGHUP 重读配置、-c 异常后清系统锁、-b 上报重启、-M mlockall、--systemd）与 power_save.html（SuspendTime/Timeout、ResumeTimeout 默认 60 s 未注册→DOWN＋重排＋"Node unexpectedly rebooted"、电源五态与 sinfo 符号、手动 power_down/power_down_asap/power_down_force/power_up 语义、ResumeProgram/SuspendProgram 运行身份与容错要求、SLURM_RESUME_FILE 10 s 窗口、PowerDownOnIdle 的 COMPLETING→IDLE 条件）。24.11.7 归档无 node_states.html（404 实开确认）。未执行任何 Slurm 命令。
```
