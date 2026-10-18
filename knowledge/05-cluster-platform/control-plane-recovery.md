---
id: cluster-platform.control-plane-recovery
title: 控制面故障、平台恢复与账本核对
type: procedure
domain: cluster-platform
status: draft
platforms: [generic]
source_refs:
- src.kubernetes.etcd-backup-restore-v1-32
- src.kubernetes.controller-pattern-v1-32
- src.kubernetes.leases-v1-32
- src.kubernetes.api-concepts-v1-32
- src.kubernetes.kcm-reference-v1-32
- src.kubernetes.node-lifecycle-v1-32
- src.kubernetes.job-lifecycle-v1-32
- src.kubernetes.api-gc-v1-32
- src.kubernetes.version-skew-v1-32
- src.kubernetes.kubeadm-upgrade-v1-32
- src.kubernetes.job-controller-tests-v1.32.0
- src.kubernetes.core-v1-types-v1.32.0
- src.etcd.disaster-recovery-v3.5-docs
- src.slurm.controller-ha-24.11.7
- src.slurm.docs-24.11.7
- src.slurm.node-power-lifecycle-24.11.7
- src.slurm.upgrades-24.11.7
- src.slurm.testsuite-24-11-7-1
- src.kueue.admission-v0.19.0
- src.ascend.mind-cluster-v26.1.1
- src.ascend.mind-cluster-clusterd-v26.1.1
- src.pytorch.elastic-2.6
updated_at: "2026-10-18"
applicability:
  environment_refs: []
  notes: "未建立环境档案。Kubernetes 以 v1.32 静态快照为样板，Slurm 以 24.11.7 归档为样板；目标环境的 etcd 拓扑、StateSaveLocation 实际位置、数据库版本、MindCluster 组件与授权范围须另行补齐。"
verification:
  status: source_checked
  evidence_refs:
  - src.kubernetes.etcd-backup-restore-v1-32
  - src.slurm.controller-ha-24.11.7
  notes: "仅核对官方文档语义（锚点见 docs/research/batch-24-t05-10-sources.md）；未停/起任何 API server、未做 etcd 快照或恢复、未切换或重启任何 Slurm daemon、未执行任何 kubectl/scontrol/etcdctl 命令。"
summary: 区分 Kubernetes API/etcd/控制器与 Slurm slurmctld/slurmd/slurmdbd 的控制面故障分支，给出只读证据入口、备份恢复前提与停止门槛，以及恢复后资源账本、作业身份与持续进展的核验清单。
related_ids:
- cluster-platform.kubernetes-job-lifecycle
- cluster-platform.slurm-jobs-and-device-resources
- cluster-platform.device-resource-chain
- cluster-platform.node-drain-resource-reclamation
- cluster-platform.platform-change-and-rollback
---

# 控制面故障、平台恢复与账本核对

本页处理控制面本身失效的问题：API 服务不可用、状态存储损坏、控制器或调度器 daemon 停止、Slurm 控制器/记账服务故障。节点级摘除与变更不在本页展开，见[节点摘除、drain 与资源回收流程](node-drain-resource-reclamation.md)与[平台组件升级、发布、回退与回服](platform-change-and-rollback.md)。症状（提交无响应、作业不调度）不直接等于控制面故障，先按[空闲设备但作业等待诊断指南](idle-resource-job-waiting-triage.md)排除队列与准入层。

所有命令均为文档语义转述，本文不授予执行权限；恢复类操作（停 API server、恢复 etcd、重启控制器、`startclean`）具有破坏性，仅凭既有授权与变更窗口执行。

## 目标与触发条件

回答三个问题：控制面哪一层失效（只读证据定位）；恢复前需要保护什么（证据与恢复点）；恢复后如何确认账本与作业进展正确。触发条件是控制面组件不可用、状态疑似损坏或需要从备份重建集群身份。

## 只读证据入口与各层责任

先取只读证据，再决定是否变更。Kubernetes 侧（v1.32 快照）：

| 入口 | 观察什么 | 责任边界 |
|---|---|---|
| kube-system 中的 API server 身份 Lease | 在役 kube-apiserver 实例数与 holder 身份（v1.26 起 beta；`kubectl -n kube-system get lease -l apiserver.kubernetes.io/identity=kube-apiserver`） | 只证明 API server 进程在发布身份，不证明 etcd 或控制器健康（[Leases](https://v1-32.docs.kubernetes.io/docs/concepts/architecture/leases/) L813–827） |
| `kube-system/kube-controller-manager` Lease | 哪个实例持有领导者（`--leader-elect` 默认 true，resource-lock 默认 leases，lease-duration 15s/renew-deadline 10s/retry-period 2s） | HA 配置下仅一个实例活跃，其余 standby（[Leases](https://v1-32.docs.kubernetes.io/docs/concepts/architecture/leases/) L808–812；[kube-controller-manager 参考](https://v1-32.docs.kubernetes.io/docs/reference/command-line-tools-reference/kube-controller-manager/) 选项表） |
| 对象的 `metadata.resourceVersion` | 对象最后一次被修改时的版本；集合的 resourceVersion 表示集合构建点 | 不透明标识，只能比较相等、不能比较大小；不是时间戳（[API Concepts](https://v1-32.docs.kubernetes.io/docs/reference/using-api/api-concepts/) L1476–1484） |
| watch/410 行为 | etcd3 默认只保留最近 5 分钟变更历史；超出后 watch 返回 410 Gone，客户端应清缓存并重新 get/list | 410 是缓存过期信号，不是数据损坏信号（同上 L1015–1019） |
| 读一致性 | 请求语义由参数决定：**未设置 resourceVersion** 的 get/list（无 continue token）＝Most Recent（一致读，etcd quorum read；etcd 3.4.31+/3.5.13+ 且 K8s 1.32 时可由 API server watch cache 以 progress notification 保持一致地服务）；`resourceVersion="0"` 才是 **Any**（不强一致，分区/陈旧缓存下可能读到较旧数据，不能容忍的客户端不应使用） | 诊断"读到旧数据"先记录实际请求参数（RV/RVMatch）、响应版本、请求时间与 API server 身份，再判断是请求语义还是故障（[API Concepts](https://v1-32.docs.kubernetes.io/docs/reference/using-api/api-concepts/) L1489–1511） |
| kube-node-lease 中的节点 Lease | `spec.renewTime` 更新时间；控制面用它判定节点可用性 | 心跳停更只定位到节点/网络/心跳链，不区分原因（[Leases](https://v1-32.docs.kubernetes.io/docs/concepts/architecture/leases/) L804–808；节点默认值见 [nodes](https://v1-32.docs.kubernetes.io/docs/concepts/architecture/nodes/)） |
| etcd 快照（`etcdutl snapshot status` 输出 HASH/REVISION/TOTAL KEYS/TOTAL SIZE） | 备份文件的完整性与版本 | 快照是恢复点证据；REVISION 相对当前状态的差值提示恢复后将处于的旧版本位置（提示风险规模，不决定具体重放行为——重放取决于控制器与缓存状态，须按对象级验证核对）（[Operating etcd](https://v1-32.docs.kubernetes.io/docs/tasks/administer-cluster/configure-upgrade-etcd/) L909–923） |

Slurm 侧（24.11.7 归档）：

| 入口 | 观察什么 | 责任边界 |
|---|---|---|
| `scontrol ping` | 主/备控制器是否响应 | 不响应只说明无响应，须继续区分网络、配置或进程（[troubleshoot](https://slurm.schedmd.com/archive/slurm-24.11.7/troubleshoot.html) L131–147） |
| `SlurmctldLog`/`SlurmdLog` | daemon 失败原因 | 排查入口，不是结论（同上 L297–306） |
| StateSaveLocation 目录 | 控制器状态文件（运行/排队作业、节点 DOWN/DRAIN 与 Reason）；默认 `/var/spool` | 状态每次变化写盘；daemon 或硬件在状态落盘**之前**故障会丢状态（[quickstart_admin](https://slurm.schedmd.com/archive/slurm-24.11.7/quickstart_admin.html) L535–541、L614–615；[slurm.conf](https://slurm.schedmd.com/archive/slurm-24.11.7/slurm.conf.html) L4719–4729） |
| 记账库（slurmdbd＋MySQL/MariaDB） | 记账记录与关联数据（**含活动作业**：`sacct --state` 可查询当前 RUNNING/PENDING 记录，PENDING 记录受 EligibleTime 条件限制，[sacct](https://slurm.schedmd.com/archive/slurm-24.11.7/sacct.html) L536–556）；已结束记录按 `PurgeJobAfter` 策略清除、`ArchiveJobs` 默认 no | 记账记录与调度器**运行状态**是两套职责：恢复数据库不等于恢复 slurmctld 队列，恢复 StateSaveLocation 也不重建记账；对账时活动与完成记录要分别核对（[slurmdbd.conf](https://slurm.schedmd.com/archive/slurm-24.11.7/slurmdbd.conf.html) L375–377、L698–707、L164–169、L837–842） |
| Ascend 侧 clusterd | 集群级任务/资源/故障信息与影响范围聚合（任务、芯片、故障维度） | v26.1.1 仅 README 级职责说明；其自身故障与恢复行为无文档（unknown，不以 K8s/Slurm 机制类推） |

**资源视图正常不证明设备和应用正常**：API server 响应、节点 Ready、`scontrol` 正常返回，都只是各自责任层的证据；设备是否真正可用走[设备资源状态链](device-resource-chain.md)，应用是否恢复进展走本页最后一节与 06 章。跨层证据关联方法见 08 章可观测性主题。

## 故障分支

### Kubernetes（v1.32 快照口径）

| 故障层 | 官方前提与分支要点 |
|---|---|
| API server | 多实例经身份 Lease 可观测；单个实例故障由负载均衡与多实例承接。API server 只是访问层，etcd 与控制器健康须分别取证 |
| etcd | 快照备份是灾备前提（丢全部控制面节点场景）。恢复顺序是**硬前提**：停所有 API server 实例→恢复所有 etcd 实例→重启 API server；官方并建议重启 kube-controller-manager 与 kubelet，避免它们依赖**陈旧数据**（[Operating etcd](https://v1-32.docs.kubernetes.io/docs/tasks/administer-cluster/configure-upgrade-etcd/) L952–955）。恢复用 `etcdutl --data-dir … snapshot restore`（etcdctl 的恢复用法自 etcd 3.5.x 弃用）；恢复到原目录必须先停 etcd 并删除旧数据目录（L959–968）。etcd 不建议常规扩缩容或配置自动扩缩（L944–951）。**恢复的集群身份前提**（etcd v3.5 官方灾备指南）：恢复自快照会改写 member ID 与 cluster ID、成员失去原身份，因此从快照启动必然是一个**新逻辑集群**——全部成员必须用同一快照恢复，旧集群与旧客户端要隔离；API server 的 etcd 端点与证书边界随部署布局而不同（stacked etcd 于控制面节点与外部 etcd 集群是两种布局，具体更新步骤未核，unknown）（[etcd disaster recovery](https://etcd.io/docs/v3.5/op-guide/recovery/)）。**恢复输入工件分三类**（勿混同）：①`etcdctl snapshot save` 产生的**快照文件**（带完整性哈希，etcdutl 恢复时校验）；②从数据目录离线提取的 `member/snap/db` **单文件**（无哈希，恢复须 `--skip-hash-check`——这只是放行校验，不证明完整性；且直接取该文件可能**遗漏尚只在 WAL 中、未写入 db 的更新**，恢复点可能更旧；`--skip-hash-check` 的可用性以所选工具版本核实为前提，此处只作语义说明、不构成操作建议）；③`--data-dir` 指定的**恢复输出目录**（恢复过程新建，不是输入）。`--skip-hash-check` 只适用于第②类工件类型，不是损坏快照或整目录恢复的通用补救。所选 etcd/etcdutl patch 对上述选项的实际支持未核验（unknown） |
| 控制器 | 内建控制器运行于 kube-controller-manager，经 Lease 选主单实例活跃；控制器**设计上允许失败**，控制面另一部分会接管其工作（[Controllers](https://v1-32.docs.kubernetes.io/docs/concepts/architecture/controller/) L873–878）。控制器是"watch 状态→向 API server 发副作用"的控制循环，Job 控制器不直接运行 Pod（L812–833）。workqueue/informer 内部重试语义在 v1.32 概念文档未展开（unknown），恢复后以对象状态核对为准，不以内部队列推断 |
| 节点心跳/驱逐链 | node controller 默认 5s 检查、50s 宽限（`--node-monitor-grace-period`，须为 kubelet `nodeStatusUpdateFrequency` 的整数倍）、默认 5 分钟后才驱逐（[nodes](https://v1-32.docs.kubernetes.io/docs/concepts/architecture/nodes/)；[kube-controller-manager 参考](https://v1-32.docs.kubernetes.io/docs/reference/command-line-tools-reference/kube-controller-manager/)）。失联期删除决定无法下达 kubelet，Pod 可能在分区节点继续运行 |

### Slurm（24.11.7 归档口径）

| 故障层 | 官方前提与分支要点 |
|---|---|
| slurmctld（主） | 多条 `SlurmctldHost` 时第一条为主、其余为备；主故障后第二个接管，前两个都故障则第三个接管；主恢复后通知备机，备机保存状态回 standby，主读取保存的状态恢复运行；切换间只有短暂无响应（[quickstart_admin](https://slurm.schedmd.com/archive/slurm-24.11.7/quickstart_admin.html) L588–601）。`SlurmctldTimeout`（默认 120s）是备机等待主响应的时长（[slurm.conf](https://slurm.schedmd.com/archive/slurm-24.11.7/slurm.conf.html) L4422–4425） |
| slurmctld（无响应） | 官方排查链：`scontrol ping`→排除网络/配置→`ps -el \| grep slurmctld`→不在则重启并读 SlurmctldLog；反复失败且无失败模式指示时才考虑 stop＋`startclean`，此时**丢全部运行中作业与状态**（[troubleshoot](https://slurm.schedmd.com/archive/slurm-24.11.7/troubleshoot.html) L131–162） |
| slurmctld（重启恢复范围） | 默认 `-r`：恢复作业＋节点 DOWN/DRAIN 与 Reason，不恢复分区状态；`-R`：完整恢复作业/节点/分区/省电设置；`-c`：清除全部状态（全部作业被杀，生产极少用）；`-i`：忽略状态文件错误但会丢未恢复数据（[slurmctld(8)](https://slurm.schedmd.com/archive/slurm-24.11.7/slurmctld.html) L131–172） |
| slurmd | 节点侧 daemon 失效表现为节点失联/DOWN，处置与账本语义见[节点摘除流程](node-drain-resource-reclamation.md)与[Slurm 状态参考](slurm-jobs-and-device-resources.md)；`ReturnToService` 决定 DOWN 节点回服条件（默认 0＝需管理员显式恢复） |
| slurmdbd | `DbdBackupHost` 定义备 dbd，前提是能访问与主相同的底层 Storage 数据库；`-u` 只检查数据库版本与是否需要转换（返回 0/1），`-R` 重建关联树 lft/rgt（极少用）（[slurmdbd.conf](https://slurm.schedmd.com/archive/slurm-24.11.7/slurmdbd.conf.html) L369–377；[slurmdbd(8)](https://slurm.schedmd.com/archive/slurm-24.11.7/slurmdbd.html) L139–150）。**调度状态与记账状态不能混同**：恢复 StateSaveLocation 不重建记账历史，恢复数据库不恢复排队作业 |

## 备份、恢复与重建的前提和停止门槛

行动顺序：先保护证据与恢复点，再变更。

1. **保护在先**：固定 etcd 快照文件与 StateSaveLocation 目录的副本、daemon 日志、故障时刻的对象清单/作业清单（`kubectl get -o yaml` 类导出与 `scontrol show` 类输出的**文档语义**；实际命令须现场核实后使用）。快照含全部集群状态，属敏感数据，官方建议加密保存（[Operating etcd](https://v1-32.docs.kubernetes.io/docs/tasks/administer-cluster/configure-upgrade-etcd/) L909–913）。
2. **版本与集群身份前提**：恢复所用的组件版本、kubeadm 集群身份与证书边界按[版本偏斜与升级文档](platform-change-and-rollback.md)（K8s 无官方降级路径；Slurm 大版本状态/数据库迁移后不可原地降级）。etcd 恢复目录更换时须同步改 etcd 静态 Pod 的 `volumes.hostPath`（L966–968）。
3. **回放与重复调度风险（预期风险，须恢复后核验，不是自动正确的收敛）**：快照只含拍照时点的数据 lineage，恢复后客户端会看到 revision 回退数百到数千；etcd 文档明确指出 Kubernetes 控制器/操作器的 informer 本地缓存与 watch 通知在该场景存在专门的不一致风险（[etcd disaster recovery：Revision Difference](https://etcd.io/docs/v3.5/op-guide/recovery/)）。`--bump-revision`（64 位增量）可使 revision 不回退，但 Kubernetes 上下文还须同时标记全部旧 revision（含已压缩历史）；该选项在所选 etcd/etcdutl patch 的实际支持与语义未核验（unknown），不作为通用处方。由此，控制器基于旧对象状态重复创建/删除（如 Job 控制器按旧期望重建 Pod）是**预期风险**，其副作用是否可接受要靠恢复后核对表验证，不能靠"控制器会自己收敛"关闭。**缓存重建的可判定验证与停止门槛**：没有通用的"informer 缓存重建完成"指标（unknown）。验证分四层，各层证据不互相替代：①**证据记录（与对象比对分开）**：快照身份（文件/哈希）、故障前的全局 revision（如可取得）、恢复后的 revision（原始或已 bump）分别记录——**缺故障前全局证据时回退幅度记 unknown**，不从对象 resourceVersion 推算，也不凭"数百/数千"补值；②**对象清单比对**：恢复前后对象清单（含 resourceVersion 相等性）用于发现**身份、内容或预期副作用的差异**——它**不能**计算全局 revision 差值（未修改对象的 RV 与内容可完全相同，而全局 revision 已变），也不能证明任何消费者缓存已刷新；③**消费者记录（与读取记录分开）**：对每个纳入核验的控制器/客户端，记录其实例与启动世代、所需的缓存重建或重新 list/watch 的版本相关证据、观察窗口与预期动作——仅 API 读到预期值不等于消费者缓存已刷新；**未覆盖的消费者不能由其他对象的抽查通过代替**；④**停止门槛**：任一对象出现与快照内容无法解释的漂移（既非回放也非预期变更），或任一受核消费者的缓存状态无法用其自身证据确认（缺证/无法判断），即停止并回退到证据保护态，按 08 章假设检验展开；恢复验证记**未通过/未完成**，不得放行。resourceVersion 只能比较相等，不能用来判断"谁更新"；410 Gone 与 watch 断开是正常缓存过期，不要当作损坏处置。
4. **Slurm 双主警告（停止门槛）**：两台机器同时配置为主控制器且各自运行 slurmctld 会造成**破坏性行为**（[slurm.conf](https://slurm.schedmd.com/archive/slurm-24.11.7/slurm.conf.html) L6814–6817）；`startclean` 丢全部运行中作业与状态，执行前必须确认作业可放弃或已有 checkpoint。备机接管的前提是主备共享可读写的 StateSaveLocation（建议可靠文件系统），目录不可写时 HA 本身不成立。
5. **迁移控制器的官方五步**：停 daemon→改 slurm.conf→把 StateSaveLocation 拷到新控制器或共享→分发配置→重启；官方口径为 pending 作业不丢失、运行中作业正常完成（[slurm.conf RELOCATING CONTROLLERS](https://slurm.schedmd.com/archive/slurm-24.11.7/slurm.conf.html) L6792–6811）。
6. **unknown 边界**：MindCluster 组件（clusterd/ascend-operator/volcano 相关组件）与 Kueue/Volcano 自身的备份恢复无一手文档；正文不以 K8s/Slurm 机制类推，相关恢复行为保持 unknown。

## 恢复后账本与进展核验

恢复动作完成不等于恢复正确。按层核对：

| 核对项 | Kubernetes | Slurm |
|---|---|---|
| 重复/过期分配 | **容器级**重启计数（`ContainerStatus.restartCount`，[v1.32.0 types.go](https://github.com/kubernetes/kubernetes/blob/v1.32.0/staging/src/k8s.io/api/core/v1/types.go) L3096–3100；节点重启丢状态时可能归零），不能当作跨 Pod/跨恢复的执行计数；跨恢复的执行身份用 **Pod UID＋owner Job UID＋运行时容器 ID（containerID）＋所在节点＋采集时间**与**应用自身 attempt** 的映射对照（复用[节点摘除流程](node-drain-resource-reclamation.md)的身份账本口径），区分"原 Pod 内容器重启"与"新建替代 Pod"；torchrun 类 `max-restarts` 是策略上限，不是某次执行的身份；对象可能已被 GC（计数缺失≠未发生） | 作业的 attempt 语义（`SLURM_RESTART_COUNT`/重排计数）；COMPLETING 滞留作业（见[状态参考](slurm-jobs-and-device-resources.md)） |
| 未完成/已完成作业 | Job 终态在 `status.conditions`：成功是 **`Complete`**、失败是 **`Failed`**（[Job 概念页](https://v1-32.docs.kubernetes.io/docs/concepts/workloads/controllers/job/) L1219–1227；`Succeeded` 是 Pod phase 用语，不是 Job condition）；核对 `status.succeeded/failed` 计数与实际 Pod 数；`spec.backoffLimit` 是失败重试**限额**，实际重试按 restartPolicy 分支计算（失败 Pod 计数与 OnFailure 容器重启分别计，同页 L986–988）；终态时序按 v1.32 门控（`JobManagedBy`/`JobPodReplacementPolicy`，均默认开）：**终态 condition 延迟到全部 Job Pod 终止后才添加**（此时 `status.terminating` 应为 0；更早信号是 `FailureTarget`/`SuccessCriteriaMet`；v1.30 及以前或门控关闭时行为不同——见[作业生命周期](kubernetes-job-lifecycle.md)终态时序节及其登记的 `TestDelayTerminalPhaseCondition` 集成测试）。恢复环境未确认门取值时，终态时序与 Pod 替换行为均按 unknown 处理，不以 conditions 出现即断定全部 Pod 已终止；TTL 与 GC finalizer 是否正常收敛（[作业生命周期](kubernetes-job-lifecycle.md)） | 队列中作业与节点实际进程是否一致；`ReturnToService`/节点注册后的 NoResp 清除 |
| attempt/Checkpoint | 训练侧以 torchrun `max-restarts` 等弹性语义与 checkpoint 前提核对（[elastic](https://docs.pytorch.org/docs/2.6/elastic/train_script.html)：checkpoint 是恢复前提） | 同左；重排后的作业是否从应有进度继续 |
| 资源清理 | VolumeAttachment/PV finalizer、设备插件的分配与实际占用是否一致（[设备资源状态链](device-resource-chain.md)） | GRES/TRES 账本与实际设备占用；节点 cgroup 残留 |
| 健康/准入 | 节点心跳 Lease 恢复更新；Kueue 准入与配额状态回到一致（[Kueue 准入](admission-and-placement.md)） | HealthCheckProgram 的触发时序是 **slurmd 首次启动、注册到 slurmctld 之前**执行一次，另有按 `HealthCheckInterval`（默认 0＝禁用）的周期触发（[slurm.conf](https://slurm.schedmd.com/archive/slurm-24.11.7/slurm.conf.html) L1379–1395）；没有执行结果证据时健康项保持 unknown，不把注册成功或 NoResp 消失当作健康已验证 |
| 记账一致性 | — | sacct 记录（含活动作业的 RUNNING/PENDING 查询）与实际作业对照；恢复窗口内记账缺失或延迟要如实记录，不回填伪造；purge 策略决定已结束记录的留存范围 |

**官方故障测试与案例材料（按分支交付，均未执行）**：

| 分支 | 材料（固定版本） | 触发与断言 | 限制/缺口 |
|---|---|---|---|
| Slurm：DBD/控制器停起×新旧作业 | [`testsuite/python/tests/test_102_5.py`](https://github.com/SchedMD/slurm/blob/slurm-24-11-7-1/testsuite/python/tests/test_102_5.py) `test_qos_removal_single`（L15–23 前置：slurmdbd 记账＋qos/associations 强制；`src.slurm.testsuite-24-11-7-1` 补充核对，SHA-256 ae908d7c…，已读未运行） | 故障触发：停 slurmdbd→提交运行/等待作业→停 slurmctld 后再启 slurmdbd（作业信息只留在 slurmctld）→改数据库（删 QOS）→重启 slurmctld；断言：旧运行作业保持 RUNNING、旧等待作业转 InvalidQOS、新提交被拒——对应"控制器重启后新旧作业状态分叉"的核对分支 | 非主备切换专项；QOS 语境 |
| Slurm：记账状态×重排 | [`testsuite/expect/test37.5`](https://github.com/SchedMD/slurm/blob/slurm-24-11-7-1/testsuite/expect/test37.5) federated requeue | `check_dbd_states` 断言 REQUEUED/REVOKED/PENDING、`check_restart_cnt` 断言重启计数 | 联邦重排语义，主动 requeue 非故障注入 |
| K8s：作业中断/重试/终态时序 | v1.32.0 [`test/integration/job/job_test.go`](https://github.com/kubernetes/kubernetes/blob/v1.32.0/test/integration/job/job_test.go)：`TestJobFailedWithInterrupts` L3776、`TestDelayTerminalPhaseCondition` L1236、`TestJobPodsCreatedWithExponentialBackoff` L3686；单测 [`job_controller_test.go`](https://github.com/kubernetes/kubernetes/blob/v1.32.0/pkg/controller/job/job_controller_test.go)：`TestJobBackoff` L6993、`TestJobBackoffForOnFailure` L7041、`TestJobBackoffOnRestartPolicyNever` L7401（均经[作业生命周期](kubernetes-job-lifecycle.md)登记档案核对，已读未运行） | 覆盖恢复核验表的失败重试计数、替代 Pod 与终态时序语义 | 控制器行为级；非 etcd/API server 故障 |
| K8s/etcd：灾备 | [etcd v3.5 官方灾备指南](https://etcd.io/docs/v3.5/op-guide/recovery/)（quorum 丢失场景、End-2-End Example；`src.etcd.disaster-recovery-v3.5-docs`） | 程序性材料（含具体故障场景步骤），非自动化测试 | etcd 灾备的官方自动化测试未在固定版本定位到（负结果，该分支缺证保留）；不以指南冒充测试 |

主备切换（Slurm HA 接管/回切、K8s 多实例）与 etcd 灾备的**专项官方故障测试**未定位到（expect 目录 593 用例主题检索负结果；python 测试目录定位到 test_102_5 族涉及 daemon 停起）；这两支的验证依赖下述未执行演练方案，缺证如实保留。

**未执行的演练方案（方法设计，非实测）**：在独立受控环境（V11 类前提，见路线图验证轨道）分别演练——(a) etcd 快照→停 API server→恢复（同一快照恢复全部成员、旧集群隔离）→重启 API server 与 kube-controller-manager/kubelet，验证 revision 回退量、informer 重建与作业重放行为；(b) slurmctld 主备切换与回切，验证 StateSaveLocation 共享与短暂无响应窗口；(c) `startclean` 后作业清空语义。每项按下方验收矩阵记录：演练前对象/作业基线快照、恢复命令、恢复后逐项结果、与预期的偏差。未取得环境前不生成任何 `reproduced` 结论。

### 恢复后新旧任务验收矩阵（方法设计，未执行）

| 类别 | 身份与基线 | 预期副作用 | 资源占用/释放 | 应用正确性与观察 | 放行门槛 |
|---|---|---|---|---|---|
| 旧**已完成**作业 | 记录其终态身份（K8s Job UID/conditions；Slurm JobId/终态）与恢复前基线 | **不得被误重跑**：核对无新建的同 owner Pod/无同 JobId 重排 | 其资源应已释放：无残留分配/卷/设备占用 | 输出工件不被覆盖或重复生成（工件名/计数对照基线） | 全部一致；发现重跑痕迹即停在失败态转排查 |
| 旧**未完成**作业 | 记录恢复前进度（attempt/Checkpoint/已消费数据）与预期续跑方式 | 或续跑或按策略重排/取消；每种选择的副作用先声明 | 续跑占用与原分配一致；重排则原占用先释放 | 训练类：从 checkpoint 续跑后首步一致性与损失曲线衔接（[Checkpoint 恢复一致性](../06-training/checkpoint-state-consistency.md)）；非训练负载按各自契约（如服务探针） | 进度衔接可解释；无法解释的进度断裂不放行 |
| 恢复后**受控新任务** | 新身份（新 Job UID/JobId）＋预期输入与输出 | 只产生预期的新副作用 | 走正常分配→完成→释放链路 | 按预定义判据给出通过/失败/无法判断三态 | 仅经授权的验证入口提交；普通生产准入不受影响 |

训练之外的负载（服务、有状态）不适用 loss/Checkpoint 判据，按其自身契约验收（服务类见 07 章）。节点级受控验证的准入与停止门槛复用[节点摘除流程](node-drain-resource-reclamation.md)的三层门槛，本矩阵只补"新旧任务正确性"维度。

## 停止条件与完成判据

- 任一破坏性动作（停 API server、恢复 etcd、`startclean`、双主风险操作）前，证据与恢复点副本未固定即停止。
- 恢复后核对表存在无法解释的项（重复分配、记账缺失、进展断裂）时，不宣布恢复完成，转 08 章假设检验流程。
- 资源视图正常仅是必要条件；作业进展（应用层 attempt/Checkpoint/损失曲线）确认前，不关闭事件。

## 常见误解

- **"API server 响应就等于控制面健康。"** etcd quorum、控制器选主与节点心跳是不同责任层，须分别取证。
- **"etcd 恢复完就结束。"** 官方明确建议同时重启 kube-controller-manager 与 kubelet，因为它们可能依赖陈旧数据；且恢复到旧 REVISION 后控制器存在重放风险，须按上文的对象级验证与停止门槛核对后才能关闭。
- **"Slurm 有备份控制器就无损失。"** 状态落盘前的故障仍会丢状态；备机依赖共享 StateSaveLocation；`startclean` 路径直接丢全部作业。
- **"记账库只存历史，或能恢复排队作业。"** 记账记录包含活动作业（sacct 可查 RUNNING/PENDING），但它不是调度器运行状态的真相源：恢复数据库不重建队列，恢复 StateSaveLocation 也不重建历史。
- **"410 Gone 说明集群坏了。"** 它是 watch 历史窗口（etcd3 默认约 5 分钟）过期的正常信号，正确处置是重新 list。

## 来源与边界

本页 Kubernetes 语义固定在 v1.32 静态快照，Slurm 语义固定在 24.11.7 归档（24.11.7 归档无独立 high_availability 页，HA 口径由 quickstart_admin/slurm.conf/slurmctld(8)/troubleshoot 拼装）；MindCluster 组件恢复行为 unknown。取证记录与逐条锚点见 [batch-24-t05-10-sources](../../docs/research/batch-24-t05-10-sources.md)。跨层证据与时间线方法见 08 章；训练恢复的正确性验证见 06 章 checkpoint 一致性主题。
