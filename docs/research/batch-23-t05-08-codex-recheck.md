# Batch 23 · T05-08 定向复核报告

## 审阅元数据

| 项目 | 记录 |
|---|---|
| 任务与轮次 | T05-08「节点摘除、drain 与资源回收流程」；对上一轮 B23-T08-C01–C09 的修订作第一次定向复核 |
| 角色 | 延续上一轮独立审阅角色，不是正文作者；本轮未委派子代理 |
| 实际模型 | **unknown**。当前接口未暴露可核验的精确模型标识；不能将仓库约定模型写成实际执行模型，也不能证明两轮底层模型相同 |
| 实际 effort | **unknown**。接口未暴露实际 reasoning effort；不以约定的 `xhigh` 代填 |
| 日期与时区 | 2026-10-18，Asia/Shanghai（UTC+08:00）；本地取证、上游重读与只读检查均在该日进行 |
| 初审依据 | [上一轮初审报告](batch-23-t05-08-codex-review.md)，205 行，SHA-256 `0955d98c93aa2052e218ad743ccb32546fb0608a2c31c5cd1cae473ab31533cf` |
| 正文快照 | [节点摘除、drain 与资源回收流程](../../knowledge/05-cluster-platform/node-drain-resource-reclamation.md)，192 行，SHA-256 `e79163a3a9ef39ebda53e46bbf19a36b5dbd5d8513be96a8408f49c64816c20f` |
| 任务来源快照 | [T05-08 来源记录](batch-23-t05-08-sources.md)，144 行，SHA-256 `7123f8f71ad6c07fa689d20c2c19eb25da12d4c8b387fafd75f3cd68f5b93491` |
| 登记表取证快照 | [sources/registry.yaml](../../sources/registry.yaml)，取证及写报告前 SHA-256 `c2f1fad836ddfa72105f54f028d6a094d0bc9107c9a36bc7bbbfefdd61bf4b25`；交付前发生并发变化，后续局部复查见证据边界 |
| 唯一写入 | 新建本报告；不改正文、来源记录、登记表、初审报告、计划、代码或 `build/` |
| 执行边界 | 只读本地文件及上游材料；未连接集群，未执行 drain、驱逐、取消、重排、节点状态变更、重启、断电、设备或存储清理，也未提交验证负载 |

下文「正文 L…」「来源记录 L…」「登记表 L…」分别使用上表本地文件的原始行号，不是网页提取器行号。判定以初审关闭条件及本次明确要求为依据，不以作者说明或关键词出现次数代替语义复核。`CLOSED` 仅表示该发现的文档缺陷在本次范围内关闭，不代表实验验证或整篇通过。

## 逐项复核表

| 初审 ID | 原级别 | 判定 | 修订证据位置与上游核对 | 尚缺内容或关闭说明 |
|---|---|---|---|---|
| B23-T08-C01 | P1 | **OPEN** | 正文 L162–170 已按“保持隔离→排除冲突→基础设施门槛→受控验证→开放生产准入”排列，L167 明确失败回隔离；但 Slurm 主路径 L114 仍在清理后直接 `RESUME`，L134 新例子也直接走向可排新作业。固定版本 [scontrol 的 DRAIN/RESUME/UNDRAIN](https://github.com/SchedMD/slurm/blob/defaf214db2e55326f45ab08f1bde5b2036d9f5d/doc/man/man1/scontrol.1) 表明这些不是只读检查。 | 总恢复段的逆序已修正，但与主路径、例子的放行门槛尚未统一；还缺“保持生产隔离而允许验证”的明确入口，详见下文。 |
| B23-T08-C02 | P1 | **CLOSED** | 正文 L97 已明确分开 (a) 已确认关机/断电、不是重启途中的 out-of-service 路径，立即强删不容忍的 Pod 并卸卷；(b) 删除未成功满 6 分钟、节点当时不健康的独立超时路径，并列出 `disable-force-detach-on-timeout`、仅失联不足以确认停写及人工移除污点。与 [v1.32 Node Shutdowns 的两个独立小节](https://v1-32.docs.kubernetes.io/docs/concepts/cluster-administration/node-shutdown/) 相符。 | 不再把“等满 6 分钟”当作安全清理或断电确认。来源记录 L15/L90 支持立即 detach 与超时配置的区分；摘要不替代正文和上游的完整前置条件。CSI 驱动实测仍未完成。 |
| B23-T08-C03 | P2 | **OPEN** | 正文 L92/L101 已限定健康 Pod，加入 Running/Ready=False、零预算、AlwaysAllow 的未执行反例，并保留“不保证整次 drain 成功”；但 IfHealthyBudget 仅写成默认策略及“可能卡住”，没有其允许/拒绝条件。来源记录 L14/L76、登记表 L5559 仍保留零预算则 drain 永不完成的绝对摘要。核对 [Unhealthy Pod Eviction Policy](https://v1-32.docs.kubernetes.io/docs/tasks/run-application/configure-pdb/#unhealthy-pod-eviction-policy) 及 [v1.32.0 eviction.go](https://github.com/kubernetes/kubernetes/blob/v1.32.0/pkg/registry/core/pod/storage/eviction.go) L235–258。 | 还需补齐健康状态与两种策略的三分支，并修正当前来源摘要中的反向结论，详见下文。 |
| B23-T08-C04 | P2 | **CLOSED** | 正文 L91 明确是调度限制而非完整准入屏障，列出容忍、直接 `spec.nodeName`、DaemonSet、static Pod；L94/L99 改为原节点可重建，删除迁移到其他节点的承诺；L174 要求核对允许残留清单。与 [drain 的例外说明](https://v1-32.docs.kubernetes.io/docs/tasks/administer-cluster/safely-drain-node/)、[DaemonSet 的目标节点与容忍](https://v1-32.docs.kubernetes.io/docs/concepts/workloads/controllers/daemonset/)、[static Pod 行为](https://v1-32.docs.kubernetes.io/docs/tasks/configure-pod-container/static-pod/) 相符；来源记录 L17–19 亦无“迁移”承诺。 | 原节点 DS 补建、直接绑定两种输入均不能据此宣告节点无新负载。现场仍需记录实际过滤、跳过等待和残留管理范围；本轮没有实际 drain 参数或输出可核验。 |
| B23-T08-C05 | P2 | **CLOSED** | 正文 L112 在语义上分开默认 `scancel`、只取消 step/只发信号、`sbatch --requeue` 资格、`scontrol requeue` 动作，说明 step/信号不等于释放 job 分配；保留脚本从头执行、JobID 不变但不等于 checkpoint 自动续算及记录重排身份。独立重读 [scancel.1 NOTES](https://github.com/SchedMD/slurm/blob/defaf214db2e55326f45ab08f1bde5b2036d9f5d/doc/man/man1/scancel.1)、[sbatch.1 的 requeue](https://github.com/SchedMD/slurm/blob/defaf214db2e55326f45ab08f1bde5b2036d9f5d/doc/man/man1/sbatch.1)、[scontrol.1 的 requeue](https://github.com/SchedMD/slurm/blob/defaf214db2e55326f45ab08f1bde5b2036d9f5d/doc/man/man1/scontrol.1)。 | 不再暗示不存在的 `scancel --requeue`。资格与动作所述重排为 batch job 语义，不能据此承诺交互 allocation 可按同样方式重排；实际策略与 checkpoint 成功仍须现场确认。 |
| B23-T08-C06 | P2 | **OPEN** | 正文 L113/L149/L176 已新增 COMPLETING 分支，列出 job/step、重启计数/时点、slurmd/slurmstepd、进程/cgroup、Epilog 起止与返回状态；L147/L177 已列 Kubernetes Pod UID、容器 ID/ATTEMPT、PodResources，并区分进程退出与平台分配释放。与 [sinfo.1 COMPLETING](https://github.com/SchedMD/slurm/blob/defaf214db2e55326f45ab08f1bde5b2036d9f5d/doc/man/man1/sinfo.1)、[job_state_codes.shtml](https://github.com/SchedMD/slurm/blob/defaf214db2e55326f45ab08f1bde5b2036d9f5d/doc/html/job_state_codes.shtml)、[Device Plugins 的重启/Monitoring 节](https://v1-32.docs.kubernetes.io/docs/concepts/extend-kubernetes/compute-storage-net/device-plugins/) 一致。 | COMPLETING 本身已补齐；但“关联”仍只是待做要求，未给出初审要求的执行身份—分配 ID—实际设备身份—观察时间的对账方法，也未说明重启后必须重新取证。详见下文。 |
| B23-T08-C07 | P2 | **CLOSED** | 正文 L92 将 emptyDir、Checkpoint/备份读回、离线节点唯一副本、hostPath/local PV 归属及迁移/保留/擦除授权置于 drain 前，未确认则不进入 drain；L96/L175 区分维护卸卷与主动存储删除，禁止以删除 PVC/PV 作为设备回收条件。与 [Volumes 的 emptyDir/hostPath/local](https://v1-32.docs.kubernetes.io/docs/concepts/storage/volumes/) 及 [Persistent Volumes 的保护/回收](https://v1-32.docs.kubernetes.io/docs/concepts/storage/persistent-volumes/) 相符；来源记录 L20/L37 亦保留本地卷边界。 | “唯一 checkpoint 在 emptyDir”现在会在 L92 被拦截；保留 local PV 的维护不能因回收设备而触发删除对象/后端存储。L96 仍是事后复核，而非首次数据确认。 |
| B23-T08-C08 | P2 | **OPEN** | 正文 L130–136 已新增明确标为来源支持、未执行的 K8s 与 Slurm 状态序列。K8s 与 [PodDisruptionBudget example](https://v1-32.docs.kubernetes.io/docs/concepts/workloads/pods/disruptions/#poddisruptionbudget-example) 相符；Slurm 的 DRAINED、NoResp、注册及 COMPLETING 语义有固定版本 scontrol/sinfo 支持。L164–168/L179 将验证放在生产放行之前，并有失败回隔离。 | 状态例子这一半已完成；验证仍未形成可审定的完整方案：生产隔离下如何启动验证见 C01，测试身份/证据归属、网络验证、观察窗口及基线门槛、测试后清理对账仍不完整。详见下文。 |
| B23-T08-C09 | P3 | **CLOSED** | 正文 L93/L143 与来源记录 L13 均已区分 PDB 拒绝和 API 限流；L143 明确 PDB 有预算仍可能是限流。与 [API-initiated Eviction 的响应分支](https://v1-32.docs.kubernetes.io/docs/concepts/scheduling-eviction/api-eviction/#how-api-initiated-eviction-works) 相符。 | 不再仅凭 429 建议改预算；原因仍须结合响应和两侧证据确认，证据不足不能唯一归因。登记表的该条摘要仅枚举响应码，没有恢复成“429 唯一指向 PDB”。 |

### C01：恢复总序正确，但 Slurm 的主路径仍缺门控衔接

**已修正部分：** 正文 L164–168 的五步顺序及 L167 的失败返回隔离符合要求。把“CSI 未 detach”或“设备仍有过期分配”代入 L165–166，按该段应停在冲突排除/基础设施门槛，不能直接走到 L168。这是文档逻辑推演，不是现场执行结果。

**尚未关闭部分：** 同一文章 L110 明确 DRAIN 不启动新作业，L114 却在等待 COMPLETING 后直接进入 RESUME；L134 的新增状态例子也在注册成功后直接写“可排新作业”，没有标出受控验证和生产放行之间的门槛。与此同时 L164 要求保持 DRAIN，L167 又要求另行发起验证负载，L168 才允许 RESUME/UNDRAIN。按 [24.11.7 scontrol 源文档的 NODES—UPDATE](https://github.com/SchedMD/slurm/blob/defaf214db2e55326f45ab08f1bde5b2036d9f5d/doc/man/man1/scontrol.1)，DRAIN 阻止新 job，RESUME/UNDRAIN 则改变后续调度条件；仅限定节点/镜像/设备身份不构成排除其他生产 job 的准入控制。

因此读者仍可能在“保持 DRAIN 导致新验证 job 无法启动”与“先 RESUME，生产 job 可能抢先进入”之间选择。这里不是要求在 DRAIN 上绕过调度，而是要求把**基础设施恢复、验证专用准入、普通生产准入**三件事分开。上述风险是依据上游状态语义作出的流程推断，未做调度实验。

**关闭条件：** 为两平台说明经授权、经来源/站点配置核实的验证准入办法，明确谁批准、哪项控制持续阻断普通生产、何时可进行必要注册/状态恢复；未知则停止，不编造通用旁路命令。将 Slurm L114、L134 与 L162–170 显式衔接，所有可能改变准入的入口均受同一门槛约束。验证失败时需撤销验证例外并维持/恢复生产隔离；再次代入 CSI 未卸卷、过期分配、验证失败三个情形，均不得普通生产放行。

### C03：AlwaysAllow 已修，但 IfHealthyBudget 与来源摘要未闭合

正文 L101 的 AlwaysAllow 反例及整次 drain 不保证成功的限制应保留。然而“默认 IfHealthyBudget，可能卡住”不足以让读者区别三个分支。上游 [健康判定与两种策略](https://v1-32.docs.kubernetes.io/docs/tasks/run-application/configure-pdb/#unhealthy-pod-eviction-policy) 及 [v1.32.0 Eviction 实现](https://github.com/kubernetes/kubernetes/blob/v1.32.0/pkg/registry/core/pod/storage/eviction.go) 支持如下核对口径：

- 健康 Pod：仍受 PDB 的健康副本预算约束，不能因 AlwaysAllow 而绕过。
- Running 但未健康、IfHealthyBudget：应核对 `currentHealthy` 与 `desiredHealthy`，不能只看 `disruptionsAllowed`；该源码的直接放行分支还显式检查 `desiredHealthy > 0`。
- Running 但未健康、AlwaysAllow：不受上述健康预算条件限制；不意味着没有其他准入、删除或 drain 阻塞。

用于定向复核的未执行输入可以是：`minAvailable=2`，两个健康副本加一个 Running/Ready=False 目标，`currentHealthy=desiredHealthy=2`、`disruptionsAllowed=0`。IfHealthyBudget 不应仅因零剩余预算而拒绝这个不健康目标；若健康数降到 1，则不能照搬该放行结论。这与 `maxUnavailable=0` 等配置值是否设置为零是不同判断，不能混用“配置为零”与“当前剩余预算为零”。

**关闭条件：** 在正文补齐上述判断，保留健康 Pod 保护和不保证整次 drain 的限制；同步修订来源记录 L14/L76 与登记表 L5559 的无条件“永不完成”摘要。它们仍是当前主张/来源说明，未被标为已废弃的错误归纳，不能因正文新增反例就视为自动失效。本报告只指出位置，不改这些文件。

### C06：字段齐了，还缺可执行的跨层对账方法

Slurm 新增分支已经正确要求进程和 Epilog 收敛；[sinfo 的 COMPLETING](https://github.com/SchedMD/slurm/blob/defaf214db2e55326f45ab08f1bde5b2036d9f5d/doc/man/man1/sinfo.1) 与 [作业清理 flag](https://github.com/SchedMD/slurm/blob/defaf214db2e55326f45ab08f1bde5b2036d9f5d/doc/html/job_state_codes.shtml) 是不同观察对象，不能以单个作业状态替代整节点清理。正文也已正确禁止用 RESUME、重启 daemon 或删账本代替清理。

剩余问题不是要求伪造一份已采集账本，而是缺少读者应怎样填写、连接和更新账本的说明。正文 L78/L82/L147/L177 分散列出设备视图、时间线和身份字段，尚未规定把哪次设备分配与哪次执行对应起来，或在 kubelet/插件/daemon 重启后哪些旧观察必须作废、哪些证据必须重取。

尤其 [v1.32 PodResources 的 List 数据结构](https://v1-32.docs.kubernetes.io/docs/concepts/extend-kubernetes/compute-storage-net/device-plugins/#monitoring-device-plugin-resources) 给出 namespace、Pod/container 名称及插件 `resource_name/device_ids`，并不直接给出 Pod UID、运行时容器 ID 或 ATTEMPT；不能仅写“关联”就假定这些标识来自同一接口。上游同页 Handling kubelet restarts 也说明插件重注册边界。

**关闭条件：** 增补一份不含虚构数据的最小记录结构或核对步骤，至少连接节点身份、执行 UID/job.step 与重启计数、分配 ID、实际设备身份/映射依据、观察时间及重启边界；Kubernetes 明确用同期 API/CRI 证据把 PodResources 的名称与 UID/容器 ID/ATTEMPT 对齐，无法唯一连接时记 unknown。分别记录旧进程退出、旧平台分配释放、新验证 attempt 获得正确分配；重启后重新采集，而不是沿用旧快照。设备具体映射方法按插件/平台核实，不把 GPU 相对编号外推成 NPU 保证。

### C08：例子合格，验证目标仍需落成闭环

K8s 的三节点、三个副本、`minAvailable=2`、替代副本尚未可用时阻塞，以及资源不足导致替代 Pod Pending 的演进，与上游例子一致；“需加节点”只适用于这个容量不足的例子，不是所有 Pending 的通用处方。Slurm 新段明确是来源语义推演，未伪造本地输出；其回服入口的门控问题继续归 C01，不重复设新发现。

正文 L125–128/L167/L179 已列训练进展、请求、数据与资源释放目标，但没有把它们组织成可在执行前审定的验证记录：

- 验证身份与证据归属：谁批准/发起，使用哪个新 Pod/job/step/attempt，Checkpoint/数据版本、期望结果及证据由谁确认。
- 覆盖范围：设备获得与使用、选定网络端点/通信路径、训练恢复后的持续 step、服务请求与状态数据读回的适用检查；不适用项须说明。
- 判断门槛：观察窗口、进展/成功率/延迟或一致性基线；未知就明确 unknown 并阻止通过，而不是仅写“达标”。
- 测试结束：验证负载自己的进程、设备分配、卷/端点及账本再次收敛后，才作最终生产放行；失败或证据缺失返回隔离并保存证据。

**关闭条件：** 补齐上述可填写、可审定的最小方案，并与 C01 的验证专用准入和 C06 的身份账本相连。现场数值、镜像、驱动、CSI 行为继续保留待确认，不编造阈值或成功记录；本次仍不实际提交任务。

## 新增发现

**未发现需独立编号 B23-T08-R01 的新增根因。** 新增恢复总序与原 Slurm 主路径/新状态例子的门控不一致，属于 C01 尚未关闭的同一恢复准入问题；验证方案与对账方法的剩余缺口分别沿用 C08、C06，不用新编号掩盖旧发现未完成。

这一结论仅限本次修订及其相邻主张的定向检查，不表示对整篇或其他 T05 任务作了无缺陷保证。

## 结论

**本轮未通过，不能将 T05-08 标为 recheck passed。** 初审 9 项中：

- **CLOSED：5 项**——C02、C04、C05、C07、C09。
- **OPEN：4 项**——C01（P1）、C03/C06/C08（P2）。C01 的总序、C03 的 AlwaysAllow、C06 的 COMPLETING 和 C08 的状态例子均有实质进展，但尚未满足各项完整关闭条件。
- **新增独立发现：0 项。** 不重复计数同一缺口。

建议作者下一轮集中处理四件事：统一 Slurm/总恢复门控；补齐 IfHealthyBudget 并修正来源摘要；补全带身份、设备与时间的重启后对账；将受控验证落实为有入口、基线和结束清理的方案。之后仅对上述 OPEN 项及受影响邻接语义再次定向复核，不必重写已关闭项。

正文 `draft / not_verified`、空环境档案与空执行证据仍如实保留。来源核对、文档复核、结构检查与硬件/应用实验是不同结论，本轮不能升级运行验证状态，也不能证明约定模型/effort 已核验通过。

## 证据边界

### 独立重开的关键上游材料

以下均为本轮重新读取，不是只引用作者取证描述。Kubernetes 使用 `v1-32.docs.kubernetes.io` 静态快照，未用可变当前版本替换。页面可读不等于为其全部链接、补丁级实现或第三方控制器作了保证。

| 材料 | 本轮读取范围与用途 |
|---|---|
| [Safely Drain a Node](https://v1-32.docs.kubernetes.io/docs/tasks/administer-cluster/safely-drain-node/)；[kubectl drain](https://v1-32.docs.kubernetes.io/docs/reference/kubectl/generated/kubectl_drain/) | 完成语义、uncordon、调度绕过与 DS 例外、force/emptyDir/eviction/等待及过滤范围；支持 C01/C04/C07 |
| [API-initiated Eviction](https://v1-32.docs.kubernetes.io/docs/concepts/scheduling-eviction/api-eviction/)；[configure-pdb](https://v1-32.docs.kubernetes.io/docs/tasks/run-application/configure-pdb/)；[disruptions](https://v1-32.docs.kubernetes.io/docs/concepts/workloads/pods/disruptions/) | 响应分支、健康判定/两种 unhealthy 策略、三节点例子；支持 C03/C08/C09 |
| [Node Shutdowns](https://v1-32.docs.kubernetes.io/docs/concepts/cluster-administration/node-shutdown/) | Non-graceful node shutdown handling 与 Forced storage detach on timeout 分开重读；支持 C02 |
| [DaemonSet](https://v1-32.docs.kubernetes.io/docs/concepts/workloads/controllers/daemonset/)；[static Pods](https://v1-32.docs.kubernetes.io/docs/tasks/configure-pod-container/static-pod/)；[taints/tolerations](https://v1-32.docs.kubernetes.io/docs/concepts/scheduling-eviction/taint-and-toleration/)；[Assigning Pods to Nodes](https://v1-32.docs.kubernetes.io/docs/concepts/scheduling-eviction/assign-pod-node/) | 原节点重建、unschedulable 容忍、mirror/CRI ATTEMPT、直接绑定；支持 C04/C06 |
| [Volumes](https://v1-32.docs.kubernetes.io/docs/concepts/storage/volumes/)；[Persistent Volumes](https://v1-32.docs.kubernetes.io/docs/concepts/storage/persistent-volumes/) | emptyDir、hostPath、local、in-use protection、Retain/Delete 与删除 finalizer；支持 C07 |
| [Device Plugins](https://v1-32.docs.kubernetes.io/docs/concepts/extend-kubernetes/compute-storage-net/device-plugins/)；[v1.32.0 eviction.go](https://github.com/kubernetes/kubernetes/blob/v1.32.0/pkg/registry/core/pod/storage/eviction.go) | 插件重注册、PodResources List 标识字段及不健康 Pod 分支；后者经 GitHub 连接器读取 L235–290，只是补充实现核对，不代表所有 v1.32 补丁 |

**Slurm 访问限制：** 本轮直接打开 24.11.7 归档的 `scontrol.html`、`scancel.html`、`sbatch.html`、`sinfo.html`、`power_save.html`、`prolog_epilog.html`、`slurmd.html`、`job_state_codes.html`，网页工具均返回 `Internal Error`，没有取得可读正文。不能据此断言这些页不存在或是 HTTP 404。对同版本 GitHub/raw URL 的网页读取也出现 Cache miss/不可访问；随后改用已连接的 GitHub 只读工具成功读取官方仓库。一次内存中直接 HTTP 读取尝试亦失败，没有保存下载文件。

版本由独立读取的 [官方 tag 对象](https://api.github.com/repos/SchedMD/slurm/git/tags/9d1ef1877186d8101769352831c8f0fe303df31c) 确认：`slurm-24-11-7-1`（message 为 24.11.7 release）指向 commit `defaf214db2e55326f45ab08f1bde5b2036d9f5d`；以下全部固定到该 commit。tag 对象报告 unsigned，不声称完成签名验证；源码手册不能证明归档 HTML 的字节内容与生成时间。

| 同版本官方源文件 | 本轮成功读取的关键范围 |
|---|---|
| [doc/man/man1/scontrol.1](https://github.com/SchedMD/slurm/blob/defaf214db2e55326f45ab08f1bde5b2036d9f5d/doc/man/man1/scontrol.1) | requeue、NODES—UPDATE 的 DRAIN/DOWN/RESUME/UNDRAIN、ResumeAfter；主要定向范围 L345–399、L1720–1910 |
| [doc/man/man1/scancel.1](https://github.com/SchedMD/slurm/blob/defaf214db2e55326f45ab08f1bde5b2036d9f5d/doc/man/man1/scancel.1) | job/step/signal 范围、NOTES 与取消信号链；L184–232、L345–440 |
| [doc/man/man1/sbatch.1](https://github.com/SchedMD/slurm/blob/defaf214db2e55326f45ab08f1bde5b2036d9f5d/doc/man/man1/sbatch.1) | requeue 资格、JobRequeue、相同 JobID 与脚本从头执行；L2240–2310 |
| [doc/man/man1/sinfo.1](https://github.com/SchedMD/slurm/blob/defaf214db2e55326f45ab08f1bde5b2036d9f5d/doc/man/man1/sinfo.1)；[doc/html/job_state_codes.shtml](https://github.com/SchedMD/slurm/blob/defaf214db2e55326f45ab08f1bde5b2036d9f5d/doc/html/job_state_codes.shtml) | sinfo L1000–1120 的节点 COMPLETING/DRAINING/DRAINED 与 job_state_codes L1–115 的作业 base state/清理 flag |
| [doc/man/man8/slurmd.8](https://github.com/SchedMD/slurm/blob/defaf214db2e55326f45ab08f1bde5b2036d9f5d/doc/man/man8/slurmd.8)；[doc/html/power_save.shtml](https://github.com/SchedMD/slurm/blob/defaf214db2e55326f45ab08f1bde5b2036d9f5d/doc/html/power_save.shtml) | slurmd L1–100 的职责、测试重启报告及 slurmstepd 入口；power_save L100–180 的 ResumeProgram、BootTime、ResumeTimeout 失败处置；不是整套电源生命周期复审 |
| [doc/html/prolog_epilog.shtml](https://github.com/SchedMD/slurm/blob/defaf214db2e55326f45ab08f1bde5b2036d9f5d/doc/html/prolog_epilog.shtml) | allocation 释放时 Epilog、不同 hook/step 上下文、Failure Handling；主要范围 L295–355、L660–800；未把节点 Epilog 与 EpilogSlurmctld 的失败效果混同 |

### 本地检查与写入约束

- 已重新阅读 `README.md`、`docs/authoring-guide.md`、`content-outline.md` 及用户提供的根目录规则；`docs/`、`knowledge/`、`sources/` 下未发现更深层 AGENTS.md。
- 已运行 `PYTHONDONTWRITEBYTECODE=1 make check`：**PASS，100 content entries / 469 sources**。该命令只核对结构、引用与本地链接，不核实远程材料、技术正确性或操作效果；禁止生成字节码以避免额外写入。
- **未运行 `make build`**：它会改写 `build/catalog.json` 和 `build/catalog.md`，与本次“只创建本报告”的具体授权冲突。未运行硬件/集群测试，也未改 `src/kb/`，不声称任何实验通过。
- 初次读取与写报告前重复核对，正文、来源记录、初审报告及登记表 SHA-256 均与元数据一致。本轮工具写入仅涉及本报告，但整个工作区不是原子快照：以 16:52:13 建立的内存指纹对照 17:00:20 的文件内容，另外发现 T05-06/T05-07/T05-09 三份 codex-recheck 报告新增，以及 `docs/research/batch-23-t05-06-sources.md`、`knowledge/05-cluster-platform/accelerator-sharing-and-isolation.md`、`knowledge/05-cluster-platform/platform-change-and-rollback.md` 的内容变化。随后还检测到登记表变化（文件修改时间 17:00:28），SHA-256 为 `6b6bf70b92e9408793fabe63883ea3401440842fdcc057e4bb89c132dd072127`；重新读取其中 eviction-pdb 与 node-shutdown 两条，相关摘要和上述行号仍未变化，C03 的绝对摘要仍存在。T05-08 正文、任务来源记录、初审报告的交付前指纹仍与元数据一致。未对这些并发变化执行写入、撤销或作作者归因；不能宣称整个登记表或工作区始终未变。
- 未新建来源镜像、日志、缓存或实验记录；报告中的参数组合均明确为未执行的复核输入。Ascend/NPU 复位、CSI 实际卸卷、站点配置、网络/应用基线及真实恢复能力仍缺现场证据。
