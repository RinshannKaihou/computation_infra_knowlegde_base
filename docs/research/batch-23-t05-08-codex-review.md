# Batch 23 · T05-08 独立技术审阅报告

## 审阅元数据

| 项目 | 记录 |
|---|---|
| 任务 | T05-08「节点摘除、drain 与资源回收流程」；procedure |
| 角色与轮次 | 独立技术审阅者，首轮；不是正文作者；未委派其他代理 |
| 实际执行身份 | 当前 Codex CLI 会话。可见运行元数据没有提供精确模型标识或 reasoning effort，二者记为 **unknown**；不得把仓库约定的 `gpt-6.1-sol / xhigh` 冒充本轮实际模型。若审阅流程要求核验指定模型，本报告不能证明该要求已经满足 |
| 时间 | 2026-10-18，Asia/Shanghai（UTC+08:00）；开始读取时间 16:25:51，上游/正文取证检查记录截至 16:37:37；交付前工作区一致性复查时间 16:42:10 |
| 正文快照 | `knowledge/05-cluster-platform/node-drain-resource-reclamation.md`，170 行；SHA-256：`fee859e59f3fb4e68884e628794a81a80cd5a80fa95966af3408f211081eaaac` |
| 行号基准 | 本次读取的正文快照；下文 `正文 L…` 均指该文件，不是网页提取器行号 |
| 唯一写入 | 本报告；不修改正文、来源记录、登记表、计划或生成物 |
| 执行边界 | 仅本地只读检查和上游文档/源码读取；未执行 cordon、drain、Eviction、节点删除、Slurm 状态变更、取消、重排、重启、下电或设备清理 |

### 文件清单

- 仓库规范：`README.md`、`docs/authoring-guide.md`、`content-outline.md`、`schemas/content.schema.json`，以及用户给定的 AGENTS.md 规则。
- 审阅对象：[正文](../../knowledge/05-cluster-platform/node-drain-resource-reclamation.md)；[本任务来源记录](batch-23-t05-08-sources.md)。
- 任务与登记：[full-coverage-backlog.yaml](../../plans/full-coverage-backlog.yaml) 中 T05-08；[registry.yaml](../../sources/registry.yaml) 中用户指定的 11 个来源条目，并检查正文全部 `source_refs` 是否存在。
- 邻近正文：[Kubernetes Job 生命周期](../../knowledge/05-cluster-platform/kubernetes-job-lifecycle.md)、[Slurm 作业与设备资源](../../knowledge/05-cluster-platform/slurm-jobs-and-device-resources.md)、[设备资源状态链](../../knowledge/05-cluster-platform/device-resource-chain.md)、[平台变更与回退](../../knowledge/05-cluster-platform/platform-change-and-rollback.md)。邻文用于核对责任与内容边界，不代替上游一手证据。

### 取证方式与版本

1. 本地以带行号的源文件读取、YAML 解析、JSON Schema 校验及 ID 解析检查取证；没有把正文或来源记录里的“已核对”当成本轮独立核验结果。
2. Kubernetes 使用 `v1-32.docs.kubernetes.io` 页面；核对页头的 v1.32/static snapshot 声明，并定位下表所列正文节。未用跳转建议中的当前版本替换证据。
3. 用户指定的七个 Slurm 24.11.7 归档 URL **均逐条尝试打开，但本轮没有取得归档正文**：网页读取工具返回不可访问；对全部七个 URL 的另一 HTTP 读取尝试也失败。本地对 scontrol URL 的 curl 检查为 DNS 解析失败（退出码 6），不是 HTTP 404。不能据此断言网站宕机或页面不存在。
4. 为避免用新版手册猜旧版，另外通过 GitHub 连接器核验 SchedMD 官方仓库的发布 tag `slurm-24-11-7-1`：[annotated tag 对象][S00] `9d1ef1877186d8101769352831c8f0fe303df31c` 解引用到 commit **`defaf214db2e55326f45ab08f1bde5b2036d9f5d`**，tag 消息标明 24.11.7 release。以下 Slurm 语义结论来自该 commit 的对应 man/HTML 源文件。此补充可以核对版本语义，**不等于已读取或验证归档 HTML 字节相同**。

### 必开上游证据清单

Kubernetes 下列 12 个指定 URL 均已成功读取相应正文：

| 标记与页面 | 核对的节或关键条件 | 结果 |
|---|---|---|
| [K01 · safely-drain-node][K01] | drain 完成、unschedulable toleration、直接 `nodeName`、DaemonSet、uncordon | 有条件的安全驱逐，不是绝对停止新 Pod 或设备释放证明 |
| [K02 · kubectl drain][K02] | Synopsis；`--ignore-daemonsets`、`--force`、`--delete-emptydir-data`、`--disable-eviction`、grace/timeout、selector、skip-wait | 核对旗标；需要保留实际过滤与等待范围 |
| [K03 · api-eviction][K03] | How API-initiated eviction works；Troubleshooting stuck evictions | 200/429/500、终止过程；429 也可能是 API 限流 |
| [K04 · disruptions][K04] | PodDisruptionBudget example | 有三节点、多副本、预算与替代副本未 Ready 的状态例子，可供正文使用 |
| [K05 · configure-pdb][K05] | Healthiness；Unhealthy Pod Eviction Policy；Arbitrary selectors | 必须区分健康 Pod 的预算与 `AlwaysAllow` 下不健康 Running Pod |
| [K06 · node-shutdown][K06] | Graceful shutdown；Non-graceful handling；Forced storage detach on timeout | 核对断电确认、立即 detach、独立超时路径及禁用配置 |
| [K07 · nodes][K07] | Node name uniqueness；Manual administration；Node controller | 同名节点假设、cordon、心跳、默认检查/驱逐与限速边界 |
| [K08 · taint-and-toleration][K08] | Taint based Evictions；Taint Nodes by Condition | 默认 300 秒 toleration、可覆盖/无限容忍、分区节点 Pod 仍可能运行 |
| [K09 · daemonset][K09] | How Daemon Pods are scheduled；Taints and tolerations | 每个符合条件的节点上的目标 Pod；自动容忍 unschedulable |
| [K10 · static-pod][K10] | mirror Pod、删除 mirror、kubelet 重启容器与 manifest 变动 | mirror 删除不停止本地 static Pod；kubelet 是管理边界 |
| [K11 · persistent-volumes][K11] | Storage Object in Use Protection；Reclaiming；PV deletion protection finalizer | PVC/PV 保护、Retain/Delete 与后端删除不能混作普通维护卸卷 |
| [K12 · volumes][K12] | emptyDir、hostPath、local | Pod 离开节点的本地数据影响及 local PV 节点约束 |

Slurm 指定 URL 与同版本补充证据逐条对应如下。表中“失败”只说明本轮获取失败，不宣称服务器返回某个 HTTP 状态。

| 指定归档 URL | 归档读取 | 成功读取的 24.11.7 发布源码 | 核对范围 |
|---|---|---|---|
| [S01 · scontrol.html][S01] | 失败 | [doc/man/man1/scontrol.1][S01-src] | 节点 State/ResumeAfter、requeue、reboot、手动电源动作 |
| [S02 · slurmd.html][S02] | 失败 | [doc/man/man8/slurmd.8][S02-src] | daemon 职责、`-c`、`-b`；`-b` 的测试用途说明 |
| [S03 · power_save.html][S03] | 失败 | [doc/html/power_save.shtml][S03-src] | ResumeProgram/ResumeTimeout、注册与 BootTime、DOWN/requeue、PowerDownOnIdle 的清理条件 |
| [S04 · prolog_epilog.html][S04] | 失败 | [doc/html/prolog_epilog.shtml][S04-src] | Epilog 调用/完成、失败后 DRAIN、Prolog 失败重排与默认 held、重启计数和设备环境 |
| [S05 · scancel.html][S05] | 失败 | [doc/man/man1/scancel.1][S05-src] | 选项与 NOTES；默认信号链、job/step 取消与分配释放 |
| [S06 · job_state_codes.html][S06] | 失败 | [doc/html/job_state_codes.shtml][S06-src] | base state 与 flag；COMPLETING 包含清理/Epilog |
| [S07 · sinfo.html][S07] | 失败 | [doc/man/man1/sinfo.1][S07-src] | DRAINING/DRAINED/DOWN/NoResp；COMPLETING 的清除条件 |

补充独立读取：[K13 · v1.32 Device Plugins][K13] 的 kubelet 重启、健康与 PodResources 节；[K14 · v1.32.0 Eviction 实现][K14] L235 起的不健康 Pod 分支；[S08 · 同 commit 的 sbatch.1][S08] 的 requeue 相关说明；同 commit `doc/html/gres.shtml` 的已读取片段。PyTorch 2.6 的 `elastic/run.html` 与 `elastic/train_script.html` 网页获取失败，改读登记中固定 commit `1eba9b3aa3c43f86f4a2c807ac8e12c4a7767340` 的 [Train script 源文件][P01]，核对应用须自行保存/加载 checkpoint；没有把自动重启等同于自动续算。

## 结论

**本轮不通过，需要修订后定向复核。** 共 9 条开放发现：**P1 × 2、P2 × 6、P3 × 1**。P1 涉及未验证即重新准入，以及把非优雅关闭的立即强制卸卷与独立超时路径混为一谈；这些不是措辞润色问题。

正文明确区分了 Kubernetes `cordon/drain` 与 Slurm `DRAIN/DOWN/RESUME`，没有整篇按词形机械互译；训练、在线服务、有状态服务、批处理也已分别列行。不过，关键安全门槛、Slurm 清理完成与 attempt 对账、来源支持的具体状态例子尚未闭合。七个 Slurm 归档页的直接读取要求仍有取证限制，不能在本轮声称“全部指定网页已成功实开”。

分级口径：P1＝可能导致未隔离负载重新进入或数据破坏的安全顺序错误；P2＝影响关键操作语义或验收闭环的实质缺口；P3＝影响诊断精度但不是独立放行门槛的缺陷。**所有发现均为 OPEN，没有因为已有来源链接而自动关闭。**

## 发现表

| ID | 级别 | 正文定位 | 发现 | 状态 |
|---|---|---|---|---|
| B23-T08-C01 | P1 | L140、L150、L154 | 失败恢复路径先开放准入，再检查设备/卷/账本，顺序不安全 | OPEN |
| B23-T08-C02 | P1 | L97 | out-of-service 的断电前提和立即 detach 被遗漏，并与 6 分钟超时混写 | OPEN |
| B23-T08-C03 | P2 | L92、L101 | “零预算永远无法完成”错误覆盖了 AlwaysAllow 下不健康 Pod 的例外 | OPEN |
| B23-T08-C04 | P2 | L91、L94、L154 | cordon 被写成绝对准入屏障；DaemonSet 被误写成迁移到其他节点 | OPEN |
| B23-T08-C05 | P2 | L112 | `--requeue` 没有命令归属，紧接 scancel 容易组成不存在的用法；job/step 释放边界缺失 | OPEN |
| B23-T08-C06 | P2 | L75、L78、L81、L107、L129、L138 | 缺少 Slurm COMPLETING 的处置门槛，跨层身份/attempt 尚未形成可对账记录 | OPEN |
| B23-T08-C07 | P2 | L64、L93、L96、L126 | 本地数据保留检查排在驱逐之后，维护卸卷与存储删除回收边界不充分 | OPEN |
| B23-T08-C08 | P2 | L84、L124、L152 | 正文没有来源支持的完整状态例子；回收后检查只有目标，没有完整受控验证方案 | OPEN |
| B23-T08-C09 | P3 | L93 | 把 Eviction HTTP 429 唯一归因为 PDB，漏掉 API rate limiting | OPEN |

### B23-T08-C01 · 失败恢复不能先解除隔离

- **定位与问题：** 正文 L145–148 的停止原因包括 detach 风险、持续设备告警、重复/过期分配；L150 却统一要求“先恢复准入……再验证”。后半句提醒 Ready/IDLE 不等于回收，并不能撤销前半句已经允许新生产负载进入的影响。L154 还要求维护期间无新任务，两处流程不一致。
- **证据与影响：** [K02 Synopsis][K02] 把 uncordon 放在准备好回服时；[S01 NODES UPDATE][S01-src] 中 RESUME/UNDRAIN 会改变可分配条件，而不是只读健康探测。因而“先解除隔离后补证据”可能使旧占用与新分配重叠，是由这些语义得出的流程风险判断。邻近回退正文的“预检与回服门槛”也不支持把解除隔离当作无条件回退。
- **关闭条件：** 将失败分支改为保留隔离、保存证据、排除旧进程/设备/卷/账本冲突；基础设施门槛通过后，才允许另行授权、限制范围的验证负载，最后开放普通生产准入。分别说明 Kubernetes 和 Slurm 怎样保持隔离、由谁批准恢复；验证失败应返回隔离，不得无条件 uncordon/RESUME。定向复核必须覆盖“CSI 未 detach”和“设备过期分配”两种失败输入，确认均不会直接开放生产准入。

### B23-T08-C02 · 非优雅关闭与 force detach 是两条不同路径

- **定位与问题：** L97 的“非优雅关闭需打……污点，6 分钟后可能 force detach”会被读成同一条按时间等待的流程；“需打”也把一个有前提的恢复选择写成普遍必需动作。
- **证据与影响：** [K06 的 Non-graceful handling 与 Forced storage detach on timeout][K06] 分列两条路径：确认节点已关机/断电、不是重启途中后，out-of-service 才用于相应强删/立即卸卷；另一条是 Pod 删除未成功满 6 分钟且节点当时不健康的超时行为，还受 `disable-force-detach-on-timeout` 配置影响。只凭 NotReady/网络失联不能证明旧写入者已停止，混写可能导致双写或损坏。
- **关闭条件：** 分列两条路径的触发条件、授权与观测；给 out-of-service 加入真实关机/断电确认，说明匹配 toleration 的例外及恢复后人工移除污点。单列超时条件与禁用配置，禁止把“等满 6 分钟”当安全清理证明。优雅关闭语义应限定所用 OS/配置，不将 Linux systemd 口径推广到全部 generic 节点。定向复核须确认“仅失联但仍可能运行”时停止强删/强卸卷。

### B23-T08-C03 · 零预算结论需要限定健康状态与策略

- **定位与问题：** L101 明确说 AlwaysAllow 不改变“零自愿驱逐永远无法完成”，比 L92 的概括更进一步，排除了本应存在的例外。
- **证据：** [K05 Unhealthy Pod Eviction Policy][K05] 允许 `phase=Running` 但未健康的 Pod 在 AlwaysAllow 下不受预算条件限制。[K14 的不健康 Pod 分支][K14] 直接允许删除且不扣减 `disruptionsAllowed`，与同页较早的零预算概括必须结合阅读。
- **影响与关闭条件：** 区分健康 Pod 的预算阻塞、IfHealthyBudget 下的不健康 Pod、AlwaysAllow 下的不健康 Pod，不能由 `disruptionsAllowed=0` 单独推出所有目标都不可驱逐。加入一个明确标为来源推演、未执行的反例：单个 Running/Ready=False 目标，零预算、AlwaysAllow，且没有其他阻塞；该目标不因零预算被拒。仍需说明它不保证整次 drain 必然成功，也不允许为维护静默放宽业务策略。复核上述分支及健康 Pod 仍被保护的分支后关闭。

### B23-T08-C04 · cordon 与 DaemonSet 不是“清空并迁移”的保证

- **定位与问题：** L91 的影响栏写“不再接收新 Pod”，只在下一栏承认 DaemonSet 例外；L94 又说 DaemonSet 控制器会在“其他节点补建”。这既不完整描述准入边界，也错误解释了 DaemonSet 的每节点副本。
- **证据与影响：** [K01 的两个 Note 及 DaemonSet 段][K01] 明确列出 unschedulable toleration 和直接 `spec.nodeName` 的绕过情形，且 DaemonSet 可以在正在 drain 的原节点启动替代 Pod；[K09 调度节][K09] 的目标节点 affinity 与此一致。[K10][K10] 则说明 static Pod 由 kubelet 管理，mirror 对象不是停止入口。维护中仍可能出现新本地占用，不能从 cordon 推出 L154 的完成条件。
- **关闭条件：** 删除“其他节点补建”的迁移承诺；把 cordon 定义为普通调度限制而非完整准入控制。预检列出容忍、直接绑定、DaemonSet/static Pod 的允许残留清单、管理责任与何时可以停机；记录实际 drain 的筛选/跳过等待范围，并独立核对目标集合和本地进程，不仅看返回码。复核“原节点 DaemonSet 重建”和“直接 nodeName Pod”时仍不能宣布节点已无新负载。

### B23-T08-C05 · 取消、重排资格与重排动作必须分开

- **定位与问题：** L112 把 scancel 信号链与没有命令名的 `--requeue` 放在同一格，读者可能将其理解为 scancel 的选项。正文也没有说明只取消 step 不会释放 job 分配。
- **证据：** [S05 的选项与 NOTES][S05-src] 没有 scancel `--requeue`，并区分取消整个 job、取消 step 和只发信号；资源分配需 job 取消才释放。[S01 的 requeue 命令][S01-src] 是显式重排 batch job 的动作；[S08][S08] 的 `--requeue/--no-requeue` 属于 sbatch 的重排资格/策略，脚本从头执行不等于应用自动从 checkpoint 续算。邻近 Slurm 正文已分别说明这些边界。
- **关闭条件：** 按 `scancel` 默认取消、只发信号/只取消 step、`sbatch --requeue` 资格、`scontrol requeue` 动作单列；说明 batch 范围、站点策略、checkpoint 责任。保留 JobID 不等于同一次执行，重排记录必须与 C06 的 attempt 对账衔接。定向复核不存在 `scancel --requeue` 的暗示，也不再把 step 结束当成整个分配释放。

### B23-T08-C06 · 补上 COMPLETING 与可关联的身份/attempt 账本

- **定位与问题：** L75–82 已列 UID、attempt、PodResources 等观察名词，这是有价值的；但 Slurm 路径及异常表没有 COMPLETING 分支，L138 只有重注册/过期分配关键词，没有明确怎样把旧执行、残留进程和新设备分配对齐。L118 提到 Epilog 失败 DRAIN，仍缺少成功结束或卡住时的放行判据。
- **证据：** [S06 COMPLETING flag][S06-src] 表示作业结束/取消后的清理；[S07 COMPLETING 节][S07-src] 明确要求 job 进程全部终止且 Epilog 已结束才清除此节点状态。[S04][S04-src] 区分节点 Epilog 与控制器端 Epilog 的失败效果，并提供 `SLURM_JOB_RESTART_COUNT`。Kubernetes 的 [K13 Handling kubelet restarts 与 Monitoring][K13] 表明重新注册、设备 ID 清单和运行中分配需要重取，不能靠总数或旧快照证明没有占用。
- **关闭条件：** 增加长时间 COMPLETING 的只读证据分支：关联节点、job/step、执行重启计数/时点、slurmd/slurmstepd、进程/cgroup 和 Epilog 开始/结束/返回状态；未收敛时保留隔离并交给相应责任方，不以 RESUME、重启 daemon 或删账本代替清理。设备侧至少形成“执行身份—分配 ID—实际设备身份—观察时间”的关联记录，说明进程已退出与平台分配已释放是分别核对的条件。Kubernetes 同样应将 Pod UID、容器 ID/ATTEMPT 与 PodResources/设备视图关联；重启后重新取证，数量一致不能自动关闭。可以精确链接邻文的身份核对方法，不需复制整套厂商实现；GPU 的编号方法不得外推为 NPU 保证。

### B23-T08-C07 · 数据保留必须成为驱逐前门槛

- **定位与问题：** L64 仅问“是否有 Checkpoint”，L93 已进入可能允许删除 emptyDir 数据的 drain，直到 L96 第 7 步才要求需要保留时先迁移/备份。虽然文中有数据丢失提醒，但执行顺序没有保证在不可逆动作前完成授权与可恢复性确认。“PV 回收策略与 finalizer 决定删除时机”也没有区分维护卸卷与主动删除存储对象。
- **证据与影响：** [K02 的 delete-emptydir-data][K02] 与 [K12 emptyDir/local][K12] 支持本地数据风险；[K11 的 Reclaiming 与保护节][K11] 区分保留/删除后端和 PVC/PV 在使用时的保护。由此推得：仅存在于待摘除节点的恢复点不应未经可恢复性核验就算完成备份；普通节点维护不需要以删除 PVC/PV 作为设备回收条件。
- **关闭条件：** 在 drain 前逐负载确认 emptyDir 数据可丢弃或已持久化、checkpoint/备份可读回且不依赖即将离线的唯一副本；hostPath/local PV 分别记录归属、迁移或不可迁移决定、保留/擦除授权。分开描述保留 PVC/PV 的卸载/重挂路径和明确授权的存储删除路径，写清保护 finalizer 的等待对象，不提供通用强摘建议。复核“唯一 checkpoint 在 emptyDir”和“保留 local PV 的节点维护”两个情形不能误入破坏性回收。

### B23-T08-C08 · 状态例子没有进入正文，验证尚未形成闭环

- **定位与问题：** 正文有动作表和 L124–127/L157 的训练进展、请求成功、数据可读等目标，但没有一次带初态、状态变化、阻塞原因和结束条件的完整例子。来源记录的“状态例子”行不能代替面向读者的 procedure；回收后的验证也缺少受控放行、证据归属和失败返回路径。
- **证据：** [K04 PodDisruptionBudget example][K04] 已提供可引用的三节点/副本/PDB 状态演进；[S01][S01-src]、[S07][S07-src] 可支持 DRAINING→DRAINED 与 RESUME/NoResp/重新注册的独立推演。[P01][P01] 只保证应用需自己处理 checkpoint，不证明现场恢复成功。
- **关闭条件：** 至少加入一个来源支持、明确标为“文档例子/推演，未执行”的状态序列，写出观察证据、允许继续与停止条件；不得虚构现场输出或成功记录。把已有四类负载检查组织为可执行前审定的验证方案：限定节点/镜像/设备身份和新 attempt；说明谁发起受控新任务、观察哪个 checkpoint/step、请求/数据一致性证据以及网络路径；结束后再核对分配释放和残留。观察窗口、SLO/进展门槛由现场基线填入，缺失即 unknown，不编造通用阈值；失败必须回到 C01 的隔离分支。该方案本轮只供审阅，不能实际提交任务。

### B23-T08-C09 · HTTP 429 不能唯一指向 PDB

- **定位与问题：** L93 将 429 等同于 PDB 拒绝，下一步只有等待或调整 PDB；来源记录的 API-eviction 行也沿用了这一简化。
- **证据：** [K03 How API-initiated eviction works][K03] 明确同时列出 PDB 与 API rate limiting。
- **关闭条件：** 正文改为根据响应内容、PDB 状态及 API 限流证据区分原因，无法区分时保留 unknown；不能仅因 429 就建议修改预算。来源记录的修订由作者另行处理，本报告不改该文件。定向复核应覆盖“PDB 仍有预算但 API 限流”的诊断输入。

## 验收项覆盖表

| 验收项 | 已覆盖部分 | 缺口与相关发现 | 本轮判断 |
|---|---|---|---|
| 1. K8s 所选版本的 Eviction/PDB/DS/static/local data/finalizer；Slurm 按状态与 policy 独列 | 固定 v1.32/24.11.7；两条路径独立；DRAIN 不终止、DOWN 终止、RESUME 为动作而非状态的主区别正确；列了多个豁免与存储术语 | PDB 例外、DS/准入、force detach、requeue 归属与存储门槛需修正（C02–C05、C07、C09）；Slurm 归档直接读取未成功 | 部分覆盖，未通过 |
| 2. 训练/服务/状态负载的停止准入、等待/取消/Checkpoint、设备/卷/网络清理与重新准入责任 | L124–127 四类负载分行，平台/应用责任已有框架 | 恢复顺序错误（C01）；本地数据前置不完整（C07）；设备/网络的具体证据责任与放行方案仍需补齐（C06、C08） | 部分覆盖，未通过 |
| 3. API/daemon/进程/实际设备身份与 attempt；长 Terminating/Completing、残留/过期分配与重启账本矛盾 | 有 UID、attempt、运行时、PodResources、finalizer、重注册及残留风险提醒；没有建议直接强摘 finalizer | COMPLETING 缺席；旧/新执行与设备的证据连接和收敛判据不够，不能由注册或计数宣布释放（C06） | 部分覆盖，未通过 |
| 4. 来源支持的状态例子，停止/回退/清理门槛，新任务功能/进展验证；不执行 drain | 有停止条件、功能/进展目标；L43 及 verification 明确未执行；本轮也没有执行 | 例子留在来源记录而非正文；验证目标尚未组织成受控闭环；失败恢复门槛存在反向顺序（C01、C02、C08） | 部分覆盖，未通过 |

### 元数据、引用与关键边界检查

- JSON Schema 只读校验：正文 frontmatter **0 个校验错误**；`type: procedure`、`status: draft`、`platforms: [generic]`、applicability 的空环境引用与说明、`verification.status: not_verified` 及空 evidence_refs 均保持诚实边界。不能由这些结构字段推导技术正确或兼容性已验证。
- 正文 14 个 `source_refs` 均在登记表中存在；6 个 `related_ids` 均解析到知识内容。正文没有普通的相对路径 Markdown 链接，因而本项不存在可抽查的此类正文链接；不能把 related_ids 的解析说成“已验证所有引用语义”。本报告所链接的邻文与来源记录存在。
- node controller 默认检查/驱逐时间在 [K07][K07] 有文档依据，未将 L103 的默认值本身列为错误；[K08][K08] 还要求考虑每个 Pod 的 toleration 与分区后的实际运行状态。5 分钟不是断电、进程结束或安全卸卷承诺。
- Epilog 非零导致节点 DRAIN、Prolog 失败后默认 held，以及 ResumeTimeout 内未注册时 DOWN/requeue，在同 release 的 [S03][S03-src]、[S04][S04-src] 有支持，未列为反向语义错误；配置默认值不是现场值。节点 Epilog 与 EpilogSlurmctld 的效果不可混写。
- static Pod/mirror 的主要区分、不能直接强摘 finalizer 的提醒、emptyDir 与 local PV 的主要风险方向已经写到；发现针对错误推论和缺失门槛，不要求把全部邻近概念重复成新文章。

## unknown / 证据边界

1. **Slurm 指定归档 HTML 的原文、页内版本标记与生成时间，本轮无法直接复核。** 发布 tag/commit 的同版本源文件是补充证据，不足以声称归档内容、网页行号或历史作者哈希已经独立核对。来源记录对 `node_states.html` 的 HTTP 404 是其历史取证陈述，不是本轮复测结果。
2. 精确实际模型标识与 effort 未由运行元数据提供；审阅者不虚报与约定模型一致。若指定模型是接收前提，仍需有可核验的运行记录或由符合配置的审阅者复核。
3. 未建立目标环境档案：Kubernetes/Slurm 补丁、kubectl 与 daemon 构建、controller 配置、toleration、PDB、ReturnToService、ResumeTimeout（含分区覆盖）、KillWait、Epilog、GRES/cgroup、driver/plugin/CSI、CNI 与电源程序均不能由文档默认值代填。
4. GPU/NPU 的设备复位、残留上下文/显存清理、共享或切分设备的分配语义、硬件与驱动健康，均需对应实现与现场证据；没有证明 drain/删除对象会自动清除这些状态。MindCluster/Ascend 的 drain 专属清理与 NPU 支持没有在本轮新增验证。
5. 卷类型、CSI 实现、存储侧 fencing、真实断电、写入者停止与数据完整性未知；卷对象或 VolumeAttachment 的 API 状态不能独立证明后端安全。Windows 不由 Linux systemd 路径覆盖。
6. PyTorch 两个指定版本网页读取失败，固定源码仅支持应用 checkpoint 责任，不证明该站点框架恢复能力。Kubernetes v1.32.0 Eviction 源码补读也不等于对全部 v1.32 补丁、扩展控制器或自定义准入重复测试。
7. 状态例子、受控验证方案及关闭条件均是文档修订要求，不是已经执行的集群实验、硬件验收或本地事故历史。

## 审阅局限与交接

- 本轮为首轮静态语义审阅。没有集群、调度器、设备、网络、卷或应用实验；不能据此升级正文的实验验证状态。
- 没有修改文章来“顺手关闭”发现。作者修订后，应逐 ID 提交修改位置与支持证据，再对安全恢复顺序、卸卷两路径、PDB 健康策略、DS/直接绑定、取消/重排、COMPLETING/attempt、数据前置、例子/验证、429 分支进行定向复核；不能直接将本轮标为 passed。
- 本地执行的是只读 schema/引用检查，不是 `make check` 或技术功能测试。未运行 `make build`，避免违反只允许创建本报告的限制而改写 `build/`；未新增测试、缓存、日志或来源下载文件。
- 本轮工具写入仅涉及本报告。交付前比对确认正文、任务来源记录、四篇邻文及 backlog 的 SHA-256 与开始时相同；但工作区发生了本轮写入之外的并发变化：`sources/registry.yaml` 的 SHA-256 从 `071161e0bcaeef4466e854ad09d3f45a04892be7456d15244f05f3d62eea1e0e` 变为 `c2f1fad836ddfa72105f54f028d6a094d0bc9107c9a36bc7bbbfefdd61bf4b25`（文件修改时间 16:39:48），并出现 T05-06/T05-09 审阅报告。没有改写、撤销或归因这些变化；复查正文 14 个 source_refs 仍全部存在。整个工作区不是原子快照，不能把其他写入算作本轮产物，也不能宣称登记表在审阅期间未变。

## 证据链接

[K01]: https://v1-32.docs.kubernetes.io/docs/tasks/administer-cluster/safely-drain-node/
[K02]: https://v1-32.docs.kubernetes.io/docs/reference/kubectl/generated/kubectl_drain/
[K03]: https://v1-32.docs.kubernetes.io/docs/concepts/scheduling-eviction/api-eviction/
[K04]: https://v1-32.docs.kubernetes.io/docs/concepts/workloads/pods/disruptions/
[K05]: https://v1-32.docs.kubernetes.io/docs/tasks/run-application/configure-pdb/
[K06]: https://v1-32.docs.kubernetes.io/docs/concepts/cluster-administration/node-shutdown/
[K07]: https://v1-32.docs.kubernetes.io/docs/concepts/architecture/nodes/
[K08]: https://v1-32.docs.kubernetes.io/docs/concepts/scheduling-eviction/taint-and-toleration/
[K09]: https://v1-32.docs.kubernetes.io/docs/concepts/workloads/controllers/daemonset/
[K10]: https://v1-32.docs.kubernetes.io/docs/tasks/configure-pod-container/static-pod/
[K11]: https://v1-32.docs.kubernetes.io/docs/concepts/storage/persistent-volumes/
[K12]: https://v1-32.docs.kubernetes.io/docs/concepts/storage/volumes/
[K13]: https://v1-32.docs.kubernetes.io/docs/concepts/extend-kubernetes/compute-storage-net/device-plugins/
[K14]: https://github.com/kubernetes/kubernetes/blob/v1.32.0/pkg/registry/core/pod/storage/eviction.go#L235
[S00]: https://api.github.com/repos/SchedMD/slurm/git/tags/9d1ef1877186d8101769352831c8f0fe303df31c
[S01]: https://slurm.schedmd.com/archive/slurm-24.11.7/scontrol.html
[S02]: https://slurm.schedmd.com/archive/slurm-24.11.7/slurmd.html
[S03]: https://slurm.schedmd.com/archive/slurm-24.11.7/power_save.html
[S04]: https://slurm.schedmd.com/archive/slurm-24.11.7/prolog_epilog.html
[S05]: https://slurm.schedmd.com/archive/slurm-24.11.7/scancel.html
[S06]: https://slurm.schedmd.com/archive/slurm-24.11.7/job_state_codes.html
[S07]: https://slurm.schedmd.com/archive/slurm-24.11.7/sinfo.html
[S01-src]: https://github.com/SchedMD/slurm/blob/defaf214db2e55326f45ab08f1bde5b2036d9f5d/doc/man/man1/scontrol.1
[S02-src]: https://github.com/SchedMD/slurm/blob/defaf214db2e55326f45ab08f1bde5b2036d9f5d/doc/man/man8/slurmd.8
[S03-src]: https://github.com/SchedMD/slurm/blob/defaf214db2e55326f45ab08f1bde5b2036d9f5d/doc/html/power_save.shtml
[S04-src]: https://github.com/SchedMD/slurm/blob/defaf214db2e55326f45ab08f1bde5b2036d9f5d/doc/html/prolog_epilog.shtml
[S05-src]: https://github.com/SchedMD/slurm/blob/defaf214db2e55326f45ab08f1bde5b2036d9f5d/doc/man/man1/scancel.1
[S06-src]: https://github.com/SchedMD/slurm/blob/defaf214db2e55326f45ab08f1bde5b2036d9f5d/doc/html/job_state_codes.shtml
[S07-src]: https://github.com/SchedMD/slurm/blob/defaf214db2e55326f45ab08f1bde5b2036d9f5d/doc/man/man1/sinfo.1
[S08]: https://github.com/SchedMD/slurm/blob/defaf214db2e55326f45ab08f1bde5b2036d9f5d/doc/man/man1/sbatch.1
[P01]: https://github.com/pytorch/pytorch/blob/1eba9b3aa3c43f86f4a2c807ac8e12c4a7767340/docs/source/elastic/train_script.rst
