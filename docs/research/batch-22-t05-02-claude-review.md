# 第二十二批 T05-02 初审

审阅日期：2026-10-14（实际取证日）。正文 `updated_at: "2026-10-14"` 与审阅日相同，但输入以下表 SHA-256 识别，不以日期推导。

**结论：T05-02 需修订。新增 11 项发现（B22-C01–C11）：P1 ×4、P2 ×6、P3 ×1，全部 OPEN。** 四条 acceptance 均只部分满足。

- acceptance 1：Job↔Workload 的命名关系写错（"同名 Workload"与正文自己引用的排障页相反）；`-attempt<N>` 被当作 Workload 的 attempt，实际属于 ProvisioningRequest；generation/attempt 没有列出；状态转移没有成链。
- acceptance 2：v1.31 起的终止条件语义写反；replacement 的官方注释被转述成相反结论，`podReplacementPolicy` 全文缺失；Kueue 侧撤销/清理口径有误或缺失。
- acceptance 3：对齐表与排查表都有，但一行把正常状态当成异常，调度事件归错视图，并缺少删除传播、节点失联等分支。
- acceptance 4：资源账本口径记为 unknown，但固定 commit 中可以取得；官方测试只列了目录。

正文没有虚构命令输出或实测结果，训练恢复归应用写得明确，也没有把内容写成已验证的部署指南，这几点满足要求。`make check` 通过，结果见文末；它只校验结构与本地链接，不说明技术正确性。

审阅者角色独立于作者。审阅模型为 `claude-opus-5-5`，由用户本次明确要求试用。这不是既有的 `gpt-6.1-sol / xhigh` 批量审阅约定，也不改写该约定。本轮未出现 `[frontier_llm]` 标记、模型不一致或认证失败；推理等级等运行元数据没有可核验记录，不补造。本轮只做审阅和只读取证：未改作者正文、来源记录、登记、索引或计划；未部署集群、未提交 Job、未运行任何测试。模型审阅不构成平台或现场验证。

## 输入（以 SHA-256 识别）

| 输入 | SHA-256 |
|---|---|
| [T05-02 正文](../../knowledge/05-cluster-platform/kubernetes-job-lifecycle.md)（140 行，concept / draft） | `afac3e2ed2247b86e1a7494383eb73ff80ae531817a14056c59baa9db4e27fe4` |
| [作者来源记录](batch-22-t05-02-sources.md)（25 行） | `a7988a7bdb6b386602e41e410d08893db391f636c4d52590f5b0fb1136bcb89f` |
| [任务计划](../../plans/full-coverage-backlog.yaml)（T05-02 L5431–5467，acceptance L5449–5452，existing_source_ids L5456–5458） | `5f9bcf865b8c77e13cc8ee5f1c03140c37b86f558d8227d8bb2080249f4fcfc3` |
| [来源登记](../../sources/registry.yaml)（新登记 L5347–5385；计划列出的已有来源 src.kubernetes.device-plugins-v1-32 L129–142、src.kueue.admission-v0.19.0 L559–572） | 审阅开始时 `842d6b25aaa11d75a074054c32e2f171d71f271f10cb3cc4f62d24135bb36c28`；成稿前复核为 `b33acc3964761d2cb314cd36f4645acae470e5df9deb0d513137928c237838ab` |

来源登记在审阅期间被并行会话修改（文件时间 09:52，工作区新增 T05-01 相关条目，如 `src.ascend.docker-runtime-44385c13`）。本审阅引用的 L5347–5385、L129–142、L559–572 三段，在两次读取时文字一致，行号未变；成稿时 L5347–5385 段的 SHA-256 为 `9a06719c0fb9de814d860a2b287b58bbac6938f5627db102ee5d49227a749ccc`。正文、来源记录与计划两次哈希一致。

旁证（按本库现行草稿核对，未重新取其一次源）：[空闲设备但作业等待诊断指南](../../knowledge/05-cluster-platform/idle-resource-job-waiting-triage.md) L40、L48、L58（Workload 识别方法与 v1beta1/v1beta2 说明）；[作业准入、调度与拓扑放置](../../knowledge/05-cluster-platform/admission-and-placement.md)；`knowledge/05-cluster-platform/index.md` 的工作区 diff（新增本文导航条目，标"草稿，待审阅"）；[第二十二批来源审计](batch-22-source-audit.md) L9、L26。正文 `related_ids` 的三个 ID 都能解析到已有文件。

## 一次源取证（审阅者独立获取）

方法：全部用 `curl -sSL` 默认 TLS 校验只读获取，HTTP 均为 200。版本锚用 `git ls-remote`。目录存在性用未认证的 GitHub contents/trees API，trees 返回 `truncated: False`。HTML 去标签后按文字核对，不只判可达性。原文只放在临时目录 `/tmp/b22rev02c/`，未入库。同机 `/tmp/b22rev02/` 中有来源不明的早先文件（09:36–09:38 生成），本轮没有使用。K8s 文档页取了两次，字节一致。

作者来源记录 L5 写 curl 对 `raw.githubusercontent.com` 解析失败（exit 6）。本轮同一主机在 2026-10-14 解析成功，这是运行环境差异，不判为作者缺陷。下表哈希是本审阅的取证，不能写成作者取证。

版本锚：Kueue `refs/tags/v0.19.0` 为 tag 对象 `7b3cad14…`，`^{}` 指向 commit `911a822a49bcfd99c9c62203a009efa4130ad604`，与登记一致。Kubernetes `refs/tags/v1.32.0` 为 tag 对象 `7e247d1a…`，`^{}` 指向 commit `70d3cc986aa8221cd1dfb1121852688902d3bf53`。

| 来源（登记 ID） | 位置 | SHA-256（原文） | 核对点与结果 |
|---|---|---|---|
| K8s v1.32 Job 页（src.kubernetes.job-lifecycle-v1-32） | [job](https://v1-32.docs.kubernetes.io/docs/concepts/workloads/controllers/job/) | `b7c0928182a470c6b19d86c8e832377121b838777bbcce08d7e0b3c1807cf0d9` | 页头 `Kubernetes v1.32 documentation is no longer actively maintained … static snapshot`。**属实**：completions/parallelism 均不设时默认 1；`backoffLimit` 默认 6，`(10s, 20s, 40s ...) capped at six minutes`，两种计数口径，`OnFailure` 达上限时运行 Pod 被终止；`activeDeadlineSeconds … takes precedence over its .spec.backoffLimit`；suspend 时 `startTime` 重置、SIGTERM 终止非 Completed Pod、`Suspended`/`Resumed` 事件与 `Suspended` 条件；podFailurePolicy v1.31 stable、四个动作、只匹配 Failed phase；successPolicy v1.31 beta；managedBy v1.32 beta 且外部控制器不得用 `batch.kubernetes.io/job-tracking`；tracking finalizer v1.26 stable，`removes the finalizer only after the Pod has been accounted for`；`job-completion-index` label 自 v1.28；应用须处理 `temporary files, locks, incomplete output`。**与正文不符或正文未用**：Terminal Job conditions 节 `In Kubernetes v1.31 and later the Job controller delays the addition of the terminal conditions, Failed or Complete, until all of the Job Pods are terminated`，受 JobManagedBy 与 JobPodReplacementPolicy 门控（均默认开）；`When a Job completes … the Pods are usually not deleted either`；podFailurePolicy 节 Note `Starting with Kubernetes v1.28, when Pod failure policy is used, the Job controller recreates terminating Pods only once these Pods reach the terminal Failed phase`；"Delayed creation of replacement pods"（v1.29 beta），默认 `TerminatingOrFailed` 时 `creates replacement Pods immediately upon Pod deletion`；五类失败原因；示例中 `generation: 1`。→ C01/C02/C03/C06/C09 |
| K8s v1.32 Pod 生命周期页（同上） | [pod-lifecycle](https://v1-32.docs.kubernetes.io/docs/concepts/workloads/pods/pod-lifecycle/) | `3b6cd176dbbf06cb8a6d3cb6d385ec28f68ec5205683f79c3994064878adc173` | **属实**：五个 phase；`The phase is not intended to be a comprehensive rollup … nor … a comprehensive state machine`；kubectl Status 不等于 phase；容器重启退避 `capped at 300 seconds`、运行 10 分钟后重置；1.27 起 kubelet 先把已删 Pod 转为 terminal phase；失联节点上 Pod 置 Failed 的策略；readinessGates 缺失默认 False；删除时自动 unready；startup probe 期间禁用其他探针。**正文未用**：kubelet 管理的 `PodScheduled`、`PodReadyToStartContainers`（`sandbox has been successfully created and networking configured`）、`Initialized`、`ContainersReady`、`Ready`。Pending 原文只含 `waiting to be scheduled` 与 `downloading container images`。→ C05 |
| K8s v1.32 TTL 页（同上） | [ttlafterfinished](https://v1-32.docs.kubernetes.io/docs/concepts/workloads/controllers/ttlafterfinished/) | `e2f40f3e761fd338fd805748be010e0cc90c0b795ed7fe0b4d37036ffda95be3` | 全部属实：v1.23 stable；`only supported for Jobs`；从 Complete/Failed 条件起计时、级联删除并等待 finalizer；到期后再延长 `doesn't guarantee to retain`；`sensitive to time skew` |
| K8s v1.32 finalizers 页（同上） | [finalizers](https://v1-32.docs.kubernetes.io/docs/concepts/overview/working-with-objects/finalizers/) | `de96f53cbbb734c3c11e44414996fde34fd277b6e0bec96d475e2ffdacc6b94a` | 全部属实：写 `deletionTimestamp` 并返回 202；finalizers 清空后删除；`you cannot add a new finalizer` 于删除开始后；pv-protection 例；`avoid manually removing finalizers` |
| K8s v1.32 owners-dependents 页（同上） | [owners-dependents](https://v1-32.docs.kubernetes.io/docs/concepts/overview/working-with-objects/owners-dependents/) | `462bf102c9f6fdff9500798e0830428f31a61fda0aa5cd21e022245cc185e8a4` | `Cross-namespace owner references are disallowed by design. Namespaced dependents can specify cluster-scoped or namespaced owners.`；`OwnerRefInvalidNamespace` 用于无效跨 namespace 引用，或 `a cluster-scoped dependent with an ownerReference referencing a namespaced kind`。正文把"集群级 owner"写成非法。→ C08 |
| K8s v1.32 Job v1 API（同上） | [job-v1](https://v1-32.docs.kubernetes.io/docs/reference/kubernetes-api/workload-resources/job-v1/) | `c98f84c2bd6bf5fb01b333d40a1abc72f3dd2e7e2a54c82fab3d358907acaa16` | **属实**：`active`、`ready`、`succeeded`（弹性缩容可降）、`failed`、`completedIndexes`/`failedIndexes` 区间格式、Complete 与 Failed 互斥。`terminating`：`(in phase Pending or Running and have a deletionTimestamp)`，beta，受 JobPodReplacementPolicy 门控。`podReplacementPolicy` 字段：`TerminatingOrFailed` / `Failed`，用 podFailurePolicy 时只能为 Failed。**不符**：`uncountedTerminatedPods` 的三步是 `Add the pod UID to the arrays … 2. Remove the pod finalizer. 3. Remove the pod UID from the arrays while increasing the corresponding counter`。→ C02/C08 |
| K8s v1.32 ObjectMeta（未登记，旁证） | [object-meta](https://v1-32.docs.kubernetes.io/docs/reference/kubernetes-api/common-definitions/object-meta/) | `74abd6c2e1ddf0ce54524c86182a0a4b4777197378b3a92c9b8cf39c88f83e4a` | `generation (int64) A sequence number representing a specific generation of the desired state. Populated by the system. Read-only.` → C03 |
| K8s v1.32 Garbage Collection（未登记，旁证） | [garbage-collection](https://v1-32.docs.kubernetes.io/docs/concepts/architecture/garbage-collection/) | `3bb19013164b1f061e8f1b5f06cbb74dffe02fba42e5885e0766635f71528488` | 前台删除：`the controller deletes dependents it knows about`；`the only dependents that block owner deletion are those that have the ownerReference.blockOwnerDeletion=true field and are in the garbage collection controller cache`。→ C08 |
| K8s v1.32 Resource Quotas（未登记，旁证） | [resource-quotas](https://v1-32.docs.kubernetes.io/docs/concepts/policy/resource-quotas/) | `1ad3c80407467d29fd4db1dfe225ef3e647f6fe4c37c74205ea5ccbdb9d97b41` | `requests.cpu` 等口径为 `Across all pods in a non-terminal state`。→ C04 |
| K8s v1.32.0 源码与测试（src.kubernetes.job-controller-tests-v1.32.0；registry 源码未登记） | [test/integration/job/job_test.go](https://github.com/kubernetes/kubernetes/blob/v1.32.0/test/integration/job/job_test.go)；[pkg/registry/batch/job/strategy.go](https://github.com/kubernetes/kubernetes/blob/v1.32.0/pkg/registry/batch/job/strategy.go)；[storage.go](https://github.com/kubernetes/kubernetes/blob/v1.32.0/pkg/registry/batch/job/storage/storage.go) | job_test.go `76ab4c0f580c396bad803ae72249bf341e6111d9618d3e52bde261bc4e734da6`（4620 行）；strategy.go `6059189196fcef8b1e49eb618ef02531cac9962aa586da2499bf3fc66f8e7116`；storage.go `bf36a996c0478bcb396aea1397fc9a06e0439148ed5a10c7c2286e5e68d72e44` | contents API 列出 `pkg/controller/job`（含正文所列五个 .go 及各自 `_test.go`）与 `test/integration/job`（`job_test.go`、`main_test.go`），存在性主张属实。job_test.go 中与本文直接对应的函数：`TestJobPodFailurePolicy` L260、`TestDelayTerminalPhaseCondition` L1236、`TestBackoffLimitPerIndex` L1623、`TestJobPodReplacementPolicy` L2889、`TestJobPodReplacementPolicyFeatureToggling` L3154、`TestOrphanPodsFinalizersClearedWithGC` L3594、`TestFinalizersClearedWhenBackoffLimitExceeded` L3641、`TestJobPodsCreatedWithExponentialBackoff` L3686、`TestJobFailedWithInterrupts` L3776、`TestSuspendJob` L3884。strategy.go L62–74：`batch/v1` 删除默认 `OrphanDependents`（`for back compatibility`）；storage.go L56–57 警告 `child pods are preserved by default when jobs are deleted`。→ C04/C06 |
| Kueue jobs.md（src.kueue.job-lifecycle-v0.19.0） | [tasks/run/jobs.md@911a822a](https://github.com/kubernetes-sigs/kueue/blob/911a822a49bcfd99c9c62203a009efa4130ad604/site/content/en/docs/tasks/run/jobs.md) | `9ff23de31ca910fa689ab74a75133b3f79092ea07accd9d6f2595ea8afcd09b7`（312 行） | **属实**：L50 queue-name label；L53–54 只写 limits 时按 requests 处理；L206–212 Partial admission v0.5 beta，`completions count will not be changed`；L222–240 ElasticJob v0.13 alpha，扩容新建 Workload、旧的标 Finished，L285 缩容不建新 Workload。**需注意**：L56–57 原文为 `you do not need to create the Job in a suspended state`；L71–72 `with a matching name`，示例 L82 同名，但同页 L261 为 `job-sample-elastic-job-615b3`；L81/L128 `RESERVED IN`、`ADMITTED` 是 get 输出列；L145 Workload 事件 `Admitted`；L189–198 事件列表，L201–202 提示顺序可能与发生顺序不同。→ C03/C11 |
| Kueue workload.md / admission.md / admission_check（同上） | [workload.md](https://github.com/kubernetes-sigs/kueue/blob/911a822a49bcfd99c9c62203a009efa4130ad604/site/content/en/docs/concepts/workload.md)；[admission.md](https://github.com/kubernetes-sigs/kueue/blob/911a822a49bcfd99c9c62203a009efa4130ad604/site/content/en/docs/concepts/admission.md)；[admission_check/_index.md](https://github.com/kubernetes-sigs/kueue/blob/911a822a49bcfd99c9c62203a009efa4130ad604/site/content/en/docs/concepts/admission_check/_index.md) | workload `b6a40f7092a7f6b417408088c17efabf6318acbb223579ad91c1a5491659e6b1`；admission `69eb59b931d12f0013f1ea0afdc94507a07e6d057f9abd233d556d34a1e7d8ae`；admission_check `6b95a63f7a4edcb99062b9f0bbff03790736fa120110c6fe3d53e8e777f8def4` | **属实**：workload L18–21 `Kueue does not directly manipulate Job objects … syncs the decisions and statuses`；L80–94 配额计算与调整；L58–59 `.spec.Active` false 时驱逐且不重排；L124–140 reclaimablePods；L147–163 requeueState；L169–183 maximumExecutionTimeSeconds。admission L17–24 两阶段；L34–38 永久失败。**正文未用或转述有误**：workload L23–27 Concurrent Admission（Parent 与多个 Variant Workload）；admission L28–32 `retryStrategy` 属 ProvisioningRequestConfig，`Kueue creates new ProvisioningRequest with -attempt<N> suffix`；admission_check L89–92 四种状态，L119–128 Retry 时驱逐并释放配额、不去活，只有 Rejected 才去活。→ C03/C07 |
| Kueue troubleshooting_jobs.md 等（同上） | [troubleshooting_jobs.md](https://github.com/kubernetes-sigs/kueue/blob/911a822a49bcfd99c9c62203a009efa4130ad604/site/content/en/docs/tasks/troubleshooting/troubleshooting_jobs.md)；[troubleshooting_delete_clusterqueue.md](https://github.com/kubernetes-sigs/kueue/blob/911a822a49bcfd99c9c62203a009efa4130ad604/site/content/en/docs/tasks/troubleshooting/troubleshooting_delete_clusterqueue.md)；[cluster_queue.md](https://github.com/kubernetes-sigs/kueue/blob/911a822a49bcfd99c9c62203a009efa4130ad604/site/content/en/docs/concepts/cluster_queue.md) | jobs `fe6dfefb2e5a3d228102549d4ff51b24895b062b3b88dafe2937b4db1eb2e244`；delete_cq `589677b8a6c7375c17bc000f120364d9464076f192e8318e20809d23b899d532`；cluster_queue `7b35c9f7e8caee0815ca506f463975a09202412422c03c1f63dd91224510b346` | troubleshooting_jobs L16–63：事件 `Created Workload: my-namespace/job-my-job-19797`，job-uid 反查，名称格式 `<api-name>-<job-name>-<hash>`；L107–121 suspend 含义；L136–178 已准入与缺配额判读；L243–248 StrictFIFO 无条件；L250–263 Inadmissible；L268–296 抢占；L323 `the ready field shows how many of them are running`；L352–357 `FailedScheduling` 来自 `default-scheduler`，`NotTriggerScaleUp` 来自 `cluster-autoscaler`。delete_cq L25–32：ClusterQueue 的 `kueue.x-k8s.io/resource-in-use` finalizer。cluster_queue L532–548 stopPolicy 与正文一致。→ C03/C05/C07/C11 |
| Kueue API 与控制器源码（同上） | [v1beta1 workload_types.go](https://github.com/kubernetes-sigs/kueue/blob/911a822a49bcfd99c9c62203a009efa4130ad604/apis/kueue/v1beta1/workload_types.go)；[v1beta2 workload_types.go](https://github.com/kubernetes-sigs/kueue/blob/911a822a49bcfd99c9c62203a009efa4130ad604/apis/kueue/v1beta2/workload_types.go)；v1beta2 `constants.go`、`clusterqueue_types.go`、`localqueue_types.go`；`pkg/controller/jobs/job/job_controller.go` | v1beta1 `feea64aa94bb4e0362635c3a890a2ce0cac20a332a7e01c6482230283fb99755`；v1beta2 `50b9523e7ad0cb8c59fbb9133c03bb2e74a293f369b8333cda816c4c0dd44dc1`；constants `30cae6eecf5ca6bab3633071b07e6ca925903336e6c6274f9f5f5c923efafee9`；cq_types `6092ac24e01b5e5546cc21c71fd626c1f0b35ca1249aac971029a0093de3dad9`；lq_types `b0f3766070f59acf23c370b7f098df50605152812391e449f3d40d3b6749d8c5`；job_controller `007cd3877cfe8358e1952478c551fc7f5c0e5f44392c75d1260515fa99a5fd14` | v1beta1 L631–667 的八个条件常量与正文列表一致；L779 `deprecatedversion:warning="This version is deprecated. Use v1beta2 instead."`。v1beta2 L1179 `storageversion`；比 v1beta1 多出 `BlockedOnPreemptionGates`（L936）、`WaitingForReplacementPods`（L1023），并有 QuotaReserved/Admitted 细分 reason（L945–986）；PodsReady reason `WaitForStart`/`WaitForRecovery`/`Started`/`Recovered`（L1148–1159）。constants L20 `ResourceInUseFinalizerName = "kueue.x-k8s.io/resource-in-use"`。cq_types L132–144 stopPolicy 三值，非 None 即 Inactive；L362–392 `flavorsReservation`/`flavorsUsage`/`pendingWorkloads`/`reservingWorkloads`/`admittedWorkloads`。lq_types L39–51 LocalQueue stopPolicy 属实。job_controller L459–461 `GetWorkloadNameForJob(jobName, jobUID)`。→ C03/C04/C07 |
| Kueue 运维文档（同上，未单独登记） | [metrics.md](https://github.com/kubernetes-sigs/kueue/blob/911a822a49bcfd99c9c62203a009efa4130ad604/site/content/en/docs/reference/metrics.md)；[setup_wait_for_pods_ready.md](https://github.com/kubernetes-sigs/kueue/blob/911a822a49bcfd99c9c62203a009efa4130ad604/site/content/en/docs/tasks/manage/setup_wait_for_pods_ready.md)；[setup_object_retention_policy.md](https://github.com/kubernetes-sigs/kueue/blob/911a822a49bcfd99c9c62203a009efa4130ad604/site/content/en/docs/tasks/manage/setup_object_retention_policy.md)；[setup_failure_recovery.md](https://github.com/kubernetes-sigs/kueue/blob/911a822a49bcfd99c9c62203a009efa4130ad604/site/content/en/docs/tasks/manage/setup_failure_recovery.md) | metrics `cd42760a27887720a9900baec9056b2fab7aa4ba9737dfa7ea06e1e1b4cc2c85`；wfpr `c57c86c1f033de96b5d01776cb34d0be9b0e79323ad275ea6554bdf410f92d39`；retention `4c688b6504b9fbc1ba000eb46e0fc9da298bd98a3db93ad0037644488d39a447`；failure_recovery `499ea5b7531e85654a7003de2e6532eb3b0887f7ca8c421a3153868d5776c022` | metrics L59 `kueue_evicted_workloads_total`（reason/underlying_cause），L121–122 `kueue_cluster_queue_resource_reservation`/`_usage`。wfpr L85–118 requeuingStrategy，L107–110 达到 `backoffLimitCount` 后去活。retention L10–14 `By default, Kueue leaves all Workload objects in cluster indefinitely`，L34–41 `afterFinished`/`afterDeactivatedByKueue`，L183–200 场景 B 中 Workload 与 Job 都被删除，L202 起 Notes 说明可能级联。failure_recovery L9–24：节点失联后 Pod 卡 Terminating，`podReplacementPolicy: Failed` 的 Job 无法推进，L16 60 秒宽限，L22 数据损坏警告，L26–29 需 v0.15+ 与 `FailureRecoveryPolicy` 门控，L177 默认 5 分钟 unreachable 容忍。→ C04/C06/C07 |
| Kueue 测试与安装说明（同上） | [singlecluster job_controller_test.go](https://github.com/kubernetes-sigs/kueue/blob/911a822a49bcfd99c9c62203a009efa4130ad604/test/integration/singlecluster/controller/jobs/job/job_controller_test.go)；`pkg/controller/jobs/job/job_controller_test.go`；README；getting-started/installation.md | 集成测试 `cc9a477eb76ed0ad7c0110f6e40da3c8a8618f402a08ae4a36102a3d0a23b019`（5523 行）；单测 `887aa769e5b95271419b04c5c9fdff4358774e2eb2851acfe6fb45eed8bef88d`；README `f508b57efe2e88650c1ce0dcad655e4a9f04d5e786677b6b27c90e09e9135e5e`；installation `5260d45537be94a8e2e983c6774f790f4378928aa19eb7ba12946867e0acdc17` | 两条测试路径存在，正文的存在性主张属实。集成测试 L132 以 `GetWorkloadNameForJob(job.Name, job.UID)` 取 Workload；`Its workload finalizer should be removed` L2365（L2398 断言有 finalizer，L2410 断言删 Job 后移除）；`Should allow reclaim of resources that are no longer needed` L2416；`Should not readmit a job to the queue after Active is changed to false` L2707；`should re-queue a workload evicted due to PodsReady timeout after the backoff elapses` L3388；ObjectRetentionPolicies 组 L3916，含 `should delete orphaned Workload after finishing if the Job is deleted with PropagationPolicy=DeletePropagationOrphan` L4042；`Should handle rapid scale cycles without quota leaks` L5306。README L95 与 installation L39 均为 `Requires Kubernetes 1.29 or newer`。→ C03/C04/C09 |

取证限制：

- K8s 文档是网站渲染的 v1.32 快照，未固定 kubernetes/website 的源提交。本轮按 HTML 去标签后的文字核对。
- 测试文件只读了函数名或 It 名，以及 K8s L1236–1262、Kueue L2340–2440 两段；其余断言未审计，也未确认这些测试在对应 tag 上的 CI 结果。所有测试都没有执行。
- 未读 Kueue `provisioning_request.md` 中 retryStrategy 的参数细节、`elastic_workload.md`、`concurrent_admission.md`；Concurrent Admission 只依据 workload.md L23–27。
- 未打开 Job 页 "My pod stays terminating" 链接的目标页。
- Kueue 只见到 "K8s 1.29 or newer" 的下限声明，未查 CI 测试矩阵。
- 本轮未检索"应用结果核对"的官方例子，也没有找到。
- 未复核两侧的 LICENSE。

## 发现

### B22-C01 — P1 / OPEN：v1.31 起的终止条件语义写反；"Complete 后 Pod 残留"被当作异常排查

位置：正文 L48 粗体句；关键事件表 L101；acceptance 2、3。

证据：

- Job 页 "Terminal Job conditions" 节原文：`In Kubernetes v1.31 and later the Job controller delays the addition of the terminal conditions, Failed or Complete, until all of the Job Pods are terminated`，并说明由 JobManagedBy 与 JobPodReplacementPolicy 两个门控控制（`both enabled by default`）。"terminal condition 已加而仍有 Pod running/terminating"只在 v1.30 及以前出现。
- 同节："When a Job completes, no more Pods are created, but the Pods are usually not deleted either. Keeping them around allows you to still view the logs"。Job 对象也保留，由用户或 TTL 删除。
- Job v1 API 的 `terminating` 字段计的是"Pending 或 Running 且带 deletionTimestamp"的 Pod。
- 因此在本文固定的 v1.32 默认门控下，`Complete`/`Failed` 出现时 Pod 都已到达 terminal phase，`status.terminating` 应为 0；此后还能看到的 Pod 对象是设计上保留的终态 Pod。L48 把"已终止"与"已删除"混为一谈：粗体结论"条件出现不等于 Pod 已全清"与同句后半"v1.31 起须等 Pod 全部终止"自相矛盾。L101 对 v1.32 默认配置下的正常状态给出了排障动作（等待 Pod 全终止、查 tracking finalizer 常驻）。
- 固定 tag 上有对应的官方测试 `TestDelayTerminalPhaseCondition`（v1.32.0 `test/integration/job/job_test.go` L1236，用测试 finalizer 阻塞 Pod 删除），正文没有引用。

关闭条件：

- 改写 L48：分清"Pod 终止（terminal phase）"与"Pod 对象删除"。写明 v1.32 默认门控下，`Complete`/`Failed` 在全部 Pod 终止后才添加；`FailureTarget`/`SuccessCriteriaMet` 是更早的信号，此时 Pod 可能仍在 terminating；门控关闭或版本 ≤1.30 时行为不同。
- 把 L101 拆成两行。一行是"`SuccessCriteriaMet`/`FailureTarget` 已出现，`Complete`/`Failed` 迟迟不出"，先看 `status.terminating`、Pod `deletionTimestamp`、所在节点状态和 tracking finalizer。另一行是"`Complete` 后 Pod 对象仍在"，属正常现象，按 TTL 或删除策略清理（删除传播见 C06）。
- 在"官方测试入口"引用 `TestDelayTerminalPhaseCondition`（文件、函数名、行号）。

### B22-C02 — P1 / OPEN：替换 Pod 语义与官方注释相反；`podReplacementPolicy` 缺失

位置：正文 L48"删除中的 Pod 在进入 terminal phase 前不计为失败，但替换 Pod 会提前创建（同页 podFailurePolicy 注）"；L100"Pod 反复重建"行；L66 状态字段；acceptance 2 中的 replacement。

证据：

- Job 页 podFailurePolicy 节第二条 Note 写道："Starting with Kubernetes v1.28, when Pod failure policy is used, the Job controller recreates terminating Pods only once these Pods reach the terminal Failed phase"。正文以这条注释为出处，却得出"替换 Pod 会提前创建"，方向相反。
- Job 页 "Delayed creation of replacement pods"（`FEATURE STATE: Kubernetes v1.29 [beta]`，门控 JobPodReplacementPolicy 默认开启）：未设 podFailurePolicy 时默认 `TerminatingOrFailed`，原文为 `the control plane creates replacement Pods immediately upon Pod deletion`，因此运行中的 Pod 数可能超过 parallelism，Indexed Job 的同一 index 可能多于一个 Pod。`.spec.podReplacementPolicy: Failed` 改为等 Pod 进入终态再建；设了 podFailurePolicy 时默认且只能为 `Failed`。Job v1 API 的 `podReplacementPolicy` 字段说明一致。
- 正文全文没有出现 `podReplacementPolicy`。acceptance 2 把 replacement 与 backoff、deadline、retry 并列，而 v1.32 中控制替换时机的就是这个字段。
- 审阅者推论（非原文）：对分布式训练，默认策略下旧 Pod 仍在优雅终止时新 Pod 已经启动，可能出现同一 rank/index 两个进程并存、资源双占。这直接涉及本文的进程视图与资源账本。
- Kueue 同 commit 的 setup_failure_recovery.md L9–24 说明：节点失联、Pod 卡 Terminating 时，`podReplacementPolicy: Failed` 的 Job 无法推进（见 C06）。
- 固定 tag 测试：`TestJobPodReplacementPolicy`（L2889）、`TestJobPodReplacementPolicyFeatureToggling`（L3154）。

关闭条件：在"Job 控制器"节加入 `podReplacementPolicy`，写明取值、默认值如何随 podFailurePolicy 变化、v1.29 beta 与门控；改正 L48 的转述；L100 行加入 `status.terminating` 与替换策略判断；新旧 Pod 并存的影响标为本库推论；引用上述测试。

### B22-C03 — P1 / OPEN：Job↔Workload 身份写错，attempt 来源错位，generation/attempt 未列出

位置：正文 L70"同名 Workload"；L72"`retryStrategy` 建 `-attemptN` 新对象"；L109 核对方法第 1 步"attempt（`requeueState.count`、`retryStrategy -attemptN`）"；L92 对齐键；L122；L140；来源记录 unknown 第 1 条（L19）；登记 L5374 notes"同名 Workload"；acceptance 1。

证据：

- 正文自己引用的 troubleshooting_jobs.md L16–63 给出：Job 事件 `Created Workload: my-namespace/job-my-job-19797`；按 `kueue.x-k8s.io/job-uid` 反查；名称格式 `<api-name>-<job-name>-<hash>`。Kueue 同 commit `pkg/controller/jobs/job/job_controller.go` L459–461 的 `GetWorkloadNameForJob(jobName, jobUID)` 用 Job 名与 UID 生成名称，集成测试 L132 也这样取 Workload。
- jobs.md L71–72 写 `with a matching name`，示例 L82 中名称与 Job 相同（`sample-job-sl4bm`）；同页 ElasticJob 示例 L261 却是 `job-sample-elastic-job-615b3`。Kueue 文档内部不一致，应以排障页和代码为准：Workload 名不等于 Job 名。按"同名"执行 `kubectl get workload <job-name>` 会找不到对象。
- admission.md L28–32：临时失败时 `retryStrategy` 是 ProvisioningRequestConfig 的字段，原文为 `Kueue creates new ProvisioningRequest with -attempt<N> suffix each retry`。`-attempt<N>` 是 ProvisioningRequest 的名字后缀，不是 Workload 或 Job 的 attempt。正文 L72 省略了对象类型，L109 又把它列为 Workload 的身份核对项。
- 一个 Job 可能对应多个 Workload：jobs.md L237–240、L306–312（ElasticJob 扩容新建 Workload，旧的标 Finished）；workload.md L23–27（Concurrent Admission 下有 Parent Workload 与多个 Variant Workload，原文 `each Variant is an internal admission attempt`）。正文 L92 的对齐键默认一对一，按 job-uid 反查可能返回多个对象。
- generation/attempt 并非都没有官方字段：
  - ObjectMeta `generation` 是"A sequence number representing a specific generation of the desired state. Populated by the system. Read-only."，Job 页示例也显示 `generation: 1`。它记录 spec 修订，不是重试次数。
  - Pod 替换会产生新 Pod（新名称、新 UID）；容器重启数见 Pod 生命周期页 RESTARTS 列示例；Job 有 `status.failed`。
  - Workload 有 `status.requeueState.count`（workload.md L147–160）；达到 `waitForPodsReady.requeuingStrategy.backoffLimitCount` 后去活（setup_wait_for_pods_ready.md L107–110）。

  "没有官方统一计数器"可以成立，但 acceptance 1 要求把这些列出来；正文和来源记录目前只写 unknown。

关闭条件：

- L70 改为"对应的 Workload，名称格式 `<api-name>-<job-name>-<hash>`（排障页），用 `CreatedWorkload` 事件或 `job-uid` label 反查"，并注明 jobs.md 的 "matching name" 示例与此不一致。
- L72、L109 把 `-attempt<N>` 归到 ProvisioningRequest，并注明只在配置了 ProvisioningRequest AdmissionCheck 时出现。
- 增加一张身份/代次小表：Job/Pod/Workload UID、`metadata.generation`（spec 修订）、Pod 替换（新 UID）、容器重启数、`status.failed`/`failedIndexes`、`requeueState.count`、ProvisioningRequest attempt、ElasticJob/Concurrent Admission 的多 Workload。每项写来源，确实没有来源的保留 unknown。
- 同步修订来源记录 unknown 第 1 条与登记 L5374 的 notes。

### B22-C04 — P1 / OPEN：资源账本核对没有落到字段与指标；官方测试只列了目录

位置：正文"官方测试入口" L78–80；"核对方法" L107–111（特别是 L110"本轮未读 cluster_queue/metrics 口径页…unknown 保留"）；L140；来源记录 L15 与 unknown 第 5、6 条；登记 L5375–5385；plan `existing_source_ids` L5456–5458；acceptance 4。

证据：

- acceptance 4 要求"设计终止/重试/取消后资源账本和应用结果核对方法并引用官方测试/例子"。正文第 2 步只写"用 admission/reclaimablePods/resourceRequests 核对"，没有分终止、重试、取消三种情形写出各自应看到的变化，也没有写在 Workload、ClusterQueue 还是指标中查看。
- 账本口径在同一固定 commit 中可以取得：
  - v1beta2 `clusterqueue_types.go` L362–392 定义了 `flavorsReservation`（已为分配到该队列的 Workload 预留的配额）、`flavorsUsage`（已准入 Workload 正在使用的配额）、`pendingWorkloads`、`reservingWorkloads`、`admittedWorkloads`（已准入且未结束）。
  - metrics.md L121–122 有 `kueue_cluster_queue_resource_reservation` 与 `_usage`；L59 的 `kueue_evicted_workloads_total` 带 `reason` 与 `underlying_cause` 标签，取值含 `Deactivated`、`RequeuingLimitExceeded`、`MaximumExecutionTimeExceeded`。
  - plan 列出的已有来源 `src.kueue.admission-v0.19.0`（登记 L559–572）已记录读过 cluster_queue.md 与 clusterqueue_types.go，正文既未复用，也未说明原因。
- 有官方测试可以直接对应三类核对，正文只给了目录，并声明"仅为存在性入口"：
  - K8s v1.32.0 `test/integration/job/job_test.go`：`TestJobPodFailurePolicy` L260、`TestDelayTerminalPhaseCondition` L1236、`TestJobPodReplacementPolicy` L2889、`TestOrphanPodsFinalizersClearedWithGC` L3594、`TestFinalizersClearedWhenBackoffLimitExceeded` L3641、`TestJobPodsCreatedWithExponentialBackoff` L3686、`TestJobFailedWithInterrupts` L3776、`TestSuspendJob` L3884。
  - Kueue 911a822a `test/integration/singlecluster/controller/jobs/job/job_controller_test.go`：
    - `Its workload finalizer should be removed` L2365：先断言 Workload 带 `kueue.x-k8s.io/resource-in-use`，删 Job 后断言该 finalizer 已移除（L2398、L2410）；
    - `Should allow reclaim of resources that are no longer needed` L2416：用 pending/admitted 指标核对；
    - `Should not readmit a job to the queue after Active is changed to false` L2707；
    - `should re-queue a workload evicted due to PodsReady timeout after the backoff elapses` L3388；
    - ObjectRetentionPolicies 组 L3916，含 L4042 `DeletePropagationOrphan` 场景；
    - `Should handle rapid scale cycles without quota leaks` L5306。
- K8s 原生 ResourceQuota（审阅者旁证，未登记）的 `requests.cpu` 等口径是 `Across all pods in a non-terminal state`。如果本文只讨论 Kueue 配额，需要写明 ResourceQuota 不在范围内；否则应补上。
- 审阅者同样没有找到"应用结果核对"的官方例子，保留 unknown 可以接受。L111 引 Job 页 `temporary files, locks, incomplete output`，写明训练恢复归应用，满足 acceptance 4 的后半句。

关闭条件：

- 把第 2 步改为分"终止 / 重试（重排）/ 取消（删除、`active=false`、stopPolicy）"三种情形，逐项写出预期变化与不一致时的判断，并引固定 commit 行号：Workload 侧看 `status.admission`、`reclaimablePods` 与条件；ClusterQueue 侧看 `flavorsReservation`、`flavorsUsage`、`reservingWorkloads`、`admittedWorkloads`；指标看 reservation/usage 与 evicted reason。同时说明复用或不用 `src.kueue.admission-v0.19.0` 的理由。
- 每类核对至少对应一个固定 tag/commit 上的测试，写明文件、函数名或 It 名与行号，措辞为"上游行为样本，不是现场验证"。
- 删去 L110"本轮未读…unknown 保留"，或在补读后改写为具体口径；写明 ResourceQuota 在不在范围内。

### B22-C05 — P2 / OPEN：状态转移与控制器责任没有成链；API 接收与调度绑定缺证据；视图归属有误

位置：正文 L32–34、Pod 生命周期节 L52–56、对齐表 L84–92（特别是 L89）；acceptance 1 后半句、acceptance 3。

证据：

- acceptance 1 要求列出"控制器责任及状态转移"，并区分 API 接收、admitted、Running、应用 ready 和持续进展。正文按组件分节叙述，没有从创建到清理的转移链，也没有逐跳写出负责组件：API server 与 admission webhook、Kueue job reconciler 与 scheduler、job-controller、kube-scheduler、kubelet、TTL controller、garbage collector。
- "API 接收"只在 L32 出现一次，没有对应证据。可用证据有：对象的 `uid`、`creationTimestamp`、`generation`（ObjectMeta 页）；Kueue webhook 设置 `suspend`（jobs.md L56–57）；job-controller 的 `Suspended` 事件与条件（jobs.md L191；Job 页 Suspending a Job 节）。
- admitted 与 Running 之间缺少调度绑定这一跳。Pod 生命周期页列出了 `PodScheduled`、`PodReadyToStartContainers`（beta）、`Initialized`、`ContainersReady`、`Ready` 五个条件，正文只用了 `Ready` 与 `DisruptionTarget`，全文也没有出现 kube-scheduler。
- 对齐表"节点（kubelet/运行时）"行（L89）把 `FailedScheduling`、`NotTriggerScaleUp` 列为节点视图证据。troubleshooting_jobs.md L352–357 的 From 列分别是 `default-scheduler` 与 `cluster-autoscaler`，都是控制面组件。对齐表的作用就是分开三层视图，这两项放错了层。
- L52 把"卷挂载、沙箱联网"写进 Pending 定义。原文 Pending 只包括等待调度与下载镜像；沙箱联网属于 `PodReadyToStartContainers` 条件。

关闭条件：

- 补一张"状态转移 × 负责组件 × 证据字段/事件"的链表，覆盖：创建/接收 → Workload 创建 → QuotaReserved → AdmissionChecks → Admitted/unsuspend → Pod 创建 → PodScheduled → 沙箱/Initialized → Running → ContainersReady/Ready → Kueue PodsReady → 应用进展 → 终止条件 → 清理。各跳引版本化来源。
- 把 `FailedScheduling`、`NotTriggerScaleUp` 移到控制面行；节点行改用 Pod 条件、容器状态与重启数。
- Pending 定义按原文收窄。

### B22-C06 — P2 / OPEN：卡住、重试、清理的排查表缺关键分支

位置：关键事件与下一项检查 L96–105；L56；acceptance 3。

证据：

- **删除 Job 后 Pod 残留**（L102）只检查 finalizer。v1.32.0 `pkg/registry/batch/job/strategy.go` L62–74 中，对 `batch/v1` 的删除请求 `DefaultGarbageCollectionPolicy` 返回 `OrphanDependents`（注释 `for back compatibility`）；`storage/storage.go` L56–57 的警告文案为 `child pods are preserved by default when jobs are deleted; set propagationPolicy=Background to remove them ...`。Job 页只写了 `When you delete the job using kubectl, all the pods it created are deleted too`。因此通过 API 客户端或控制器删除 Job 且未带 propagationPolicy 时，Pod 默认被孤立。第一项检查应是删除传播策略与 Pod 的 `ownerReferences`，然后才是 finalizer。Kueue 测试 L4042 也专门覆盖了 `DeletePropagationOrphan` 场景。
- **节点失联，Pod 卡 Terminating**：Kueue 同 commit setup_failure_recovery.md L9–24、L175–200 写明，`node.kubernetes.io/unreachable` 默认容忍 5 分钟，之后 Pod 被标记终止；没有 failure recovery 时，Pod 一直停在 Terminating，直到节点恢复或人工干预，`podReplacementPolicy: Failed` 的 Job 因此无法推进。Kueue `FailureRecoveryPolicy`（v0.15+，需开启门控，Pod 需带注解 `kueue.x-k8s.io/safe-to-forcefully-delete`）会在 60 秒后把 Pod 强制置为 Failed。L22 警告原文为 `make sure the affected workloads will not cause any data corruption if re-scheduled without cleanup`。Job 页 tracking finalizer 节也有 `See My pod stays terminating` 的指引。正文 L56 只写"节点失联的 Pod 置 Failed"，需要与 Kueue 文档的描述协调。这条警告也可以加强"训练恢复归应用"的论证。
- **Workload 驱逐与重排循环**：PodsReadyTimeout → `requeueState` 退避 → 达到 `backoffLimitCount` 后去活（workload.md L147–163；setup_wait_for_pods_ready.md L85–118）。正文 L76 提到了 requeueState，排查表中没有对应的行。
- **Job 以 Failed 结束**：Job 页 "Terminal Job conditions" 节列出五类失败原因：backoffLimit、activeDeadlineSeconds、backoffLimitPerIndex 下的失败索引、maxFailedIndexes、podFailurePolicy 的 FailJob。排查表缺少按失败原因分流的一行。

关闭条件：

- 补上四行：删除传播、节点失联卡 Terminating、驱逐与重排循环、按 Job 失败原因分流。每行写先看的证据与下一项检查，并引来源。
- 让 L56 与 Kueue failure recovery 文档的说法一致。
- FailureRecoveryPolicy 标为 Kueue v0.15+ 的可选特性，需开启门控并给 Pod 加注解。

### B22-C07 — P2 / OPEN：Kueue 侧撤销、清理与条件口径有误或缺失

位置：正文 L70、L74、L76、L105、L110；完成清理节 L58–66；acceptance 2。

证据：

- **驱逐与去活**：L110"`Evicted/Rejected` 后应见释配额与去活"说得过宽。
  - admission_check/_index.md L119–128：AdmissionCheck 为 `Retry` 时，Workload 被驱逐（reason `AdmissionCheck`）并释放 QuotaReservation，但不去活；只有 `Rejected` 才把 `spec.active` 置为 false。
  - 被抢占后，Workload 重新排队并再次尝试准入（troubleshooting_jobs.md L268–296）；PodsReadyTimeout 驱逐在 `backoffLimitCount` 以内也会重排。
  - 去活只出现在以下情形：`spec.active=false`（workload.md L58–59）、AdmissionCheck Rejected、重排超限（setup_wait_for_pods_ready.md L107–110）、`maximumExecutionTimeSeconds` 超时（workload.md L178）。

  按正文的判据，正常的"抢占后重排"会被误判为"控制器未收敛"。
- **Workload finalizer 缺失**：v1beta2 `constants.go` L20 定义 `ResourceInUseFinalizerName = "kueue.x-k8s.io/resource-in-use"`。Kueue 集成测试 L2365–2414 断言已准入的 Workload 带该 finalizer，删 Job 后被移除。troubleshooting_delete_clusterqueue.md L25–32 说明 ClusterQueue 也用同名 finalizer，资源释放前不能删除。正文的删除与 finalizer 部分只讲了 K8s 侧。
- **Workload 对象生命周期缺失**：setup_object_retention_policy.md L10–14 原文为 `By default, Kueue leaves all Workload objects in cluster indefinitely`；L34–41 定义了可选的 `objectRetentionPolicies.workloads.afterFinished` 与 `afterDeactivatedByKueue`；场景 B（L183–200）显示被 Kueue 去活的 Workload 回收后，Job 也不存在了；L202 起的 Notes 说明删除可能级联到非 Kueue 创建的对象。L70"Kueue 不直接操作 Job"引自 workload.md L18–21，应补上同段后半 `syncs the decisions and statuses`，并写明上述删除情形，否则读者会以为 Kueue 不会改变 Job 的存续。
- **条件"全集"取自弃用版本**：
  - v1beta1 `workload_types.go` L779 标有 `deprecatedversion:warning="This version is deprecated. Use v1beta2 instead."`；v1beta2 L1179 为 `storageversion`；正文所引文档的示例都用 `kueue.x-k8s.io/v1beta2`（jobs.md L101、troubleshooting_jobs.md L87 等）。
  - v1beta2 比 v1beta1 多出条件类型 `BlockedOnPreemptionGates`、`WaitingForReplacementPods`（L936、L1023），并为 QuotaReserved/Admitted 定义了细分 reason，如 `WaitingForQuota`、`Misconfigured`、`Suspended`、`NoReservation`、`UnsatisfiedAdmissionChecks`（L945–986），正好可以用于"长期无 Pod"的排查。
  - 因此 L74"条件全集以 v1beta1 常量为准"不成立；reason 列表也漏了 `Deactivated`、`LocalQueueStopped`、`RequeuingLimitExceeded`、`OwnerNotFound` 等。
  - 已有登记 `src.kueue.admission-v0.19.0`（L572）已记录 v1beta1 弃用，本文没有沿用。

关闭条件：

- 改正 L110 的驱逐/去活判据，按原因分别列出。
- 清理节补上 Workload 与 ClusterQueue 的 `resource-in-use` finalizer，以及 Workload 保留策略：默认一直保留；可选的回收可能级联删除 Job。
- 条件与 reason 以 v1beta2 为准，并说明 v1beta1 已弃用；把"全集"改为"本文用到的子集"，或者给出完整列表并引行号。

### B22-C08 — P2 / OPEN：K8s 属主关系、前台删除与 Job 记账的转述有误

位置：正文 L64、L66；acceptance 2。

证据：

- L64 写"跨 namespace 或集群级 owner 非法并报 `OwnerRefInvalidNamespace`"。owners-dependents 页原文为 `Cross-namespace owner references are disallowed by design. Namespaced dependents can specify cluster-scoped or namespaced owners.`；报该事件的情形是"无效的跨 namespace 引用"，或"集群级依赖对象引用了命名空间级 kind"。命名空间级依赖对象指向集群级 owner 是允许的，正文把这半条规则说反了。
- L64 写"foreground 删除先清 `blockOwnerDeletion=true` 的 dependents"。GC 页写的是：owner 进入删除中状态后，`the controller deletes dependents it knows about`；只有 `blockOwnerDeletion=true` 且在 GC 控制器缓存中的依赖对象会阻塞 owner 删除。被删除的是全部已知依赖对象，`blockOwnerDeletion` 只决定哪些依赖会阻塞 owner 的删除。
- L66 把 `uncountedTerminatedPods` 写成"finalizer→终止→计数三步记账"。Job v1 API 原文的三步是：把 Pod UID 加入该字段的数组；摘除 Pod finalizer；从数组移除该 UID，同时增加对应计数。正文的顺序和内容都与原文不符。

关闭条件：按原文改正这三处；如果以 GC 页为依据，需先登记，或在来源记录中写明（目前未登记）。

### B22-C09 — P2 / OPEN：版本绑定不完整：未写 K8s×Kueue 交集，若干特性缺 feature state 与门控

位置：正文 L28、L44、L46、L76、L115–116；plan closure_criteria 第 2 条（L1933）；acceptance 2。

证据：

- 正文固定了两边的版本，但没有说明两者能否组合，只写了 Kueue 与 Volcano/MindCluster 共同部署未知。Kueue 911a822a 的 README L95 写 `Requires Kubernetes 1.29 or newer`，getting-started/installation.md L39 意思相同。v1.32 在这一下限之上，但这只是下限声明，不是测试矩阵。
- 以下特性缺少 feature state，Job 页均有标注：`backoffLimitPerIndex`（v1.29 beta）、`podReplacementPolicy`（v1.29 beta）、`managedBy`（v1.32 beta，门控 JobManagedBy）、Elastic Indexed Job（v1.31 stable）、tracking finalizer（v1.26 stable）。
- v1.31 起的终止条件延迟依赖 JobManagedBy 与 JobPodReplacementPolicy 两个门控（见 C01）。
- Kueue 侧：ElasticJob 需要 `ElasticJobsViaWorkloadSlices` 门控与 `kueue.x-k8s.io/elastic-job` 注解（jobs.md L226–229）；FailureRecoveryPolicy 需要 v0.15+ 并开启门控（见 C06）。

关闭条件：在"适用边界"写明："Kueue v0.19.0 文档声明要求 K8s ≥1.29，v1.32 在声明范围内；未见测试矩阵，两者组合的运行状态为 unknown"。正文提到的 beta/alpha 特性逐个标出版本与门控，并写明门控默认开还是关。

### B22-C10 — P2 / OPEN：来源登记与引用不一致

位置：frontmatter L8–11、L23；正文 L72、L80；来源记录 L5、L14–15；登记 L5361–5385；plan L5456–5458。

证据：

- plan 的 `existing_source_ids` 为 `src.kubernetes.device-plugins-v1-32` 与 `src.kueue.admission-v0.19.0`，本次任务说明也写了"复用 src.kubernetes.device-plugins-v1-32"。但正文的 `source_refs`、正文链接和来源记录都没有这两个 ID，也没有说明为什么不用。设备侧只用站内链接转到 device-resource-chain.md 可以接受，但要写明。
- 新登记的 `src.kueue.job-lifecycle-v0.19.0` 与已有的 `src.kueue.admission-v0.19.0` 指向同一 commit，范围大面积重叠（workload、admission、troubleshooting_jobs、workload_types.go）。新条目的 notes 重复了"同名 Workload"的错误（C03），也没有沿用旧条目中已记录的 v1beta1 弃用事实（C07）。
- L72 的链接文字是"workload 与 admission 页"，但只链接了 workload.md。两阶段准入及临时/永久失败处理的原文在 admission.md（L17–38），正文没有链接。
- 正文 L80 与登记 L5385 提到的 Kueue 测试路径没有具体文件链接；`src.kubernetes.job-controller-tests-v1.32.0` 的 URL 只指向 K8s。

关闭条件：

- 让 `source_refs` 与正文的实际依据一致。新增的依据（admission.md、ObjectMeta 页与 GC 页、setup_* 文档、K8s registry 源码）先登记，或并入已有条目。
- 说明 plan 中两个已有 ID 复用或不用的理由。
- 合并两个 Kueue 条目，或者明确划分范围，并更正 notes。
- L72 补上 admission.md 的链接；测试路径写到具体文件与行号。

### B22-C11 — P3 / OPEN：措辞与精确度

位置：正文 L70、L88、L98、L105、L126。

证据：

- L70"不要手动 suspend Job"：jobs.md L56–57 原文为 `you do not need to create the Job in a suspended state`，意思是"不必"，不是"不要"。
- L98"`RESERVED IN/ADMITTED` 事件"：这两项是 `kubectl get workloads` 的输出列（jobs.md L81、L128），不是事件；Workload 的准入事件是 `Admitted`（jobs.md L145）。
- L88 用箭头把事件链写成先后顺序。jobs.md L201–202 提示事件时间戳只精确到秒，列出顺序可能与实际发生顺序不同；示例中第一个 `SuccessfulCreate` 就排在 Kueue 的 `Started` 之前。应注明不能据此推断因果。
- L105"`Are Pods running` 一节明确 `ready` 不等于全部运行"：troubleshooting_jobs.md L323 原文为 `the ready field shows how many of them are running`，把 ready 与 running 混用，与 Job v1 API 对 `ready` 的定义（带 Ready 条件且不在 terminating）口径不同。正文应说明这里的文档用语较松，而不是说它"明确"做了区分。
- L126"Kueue `PodsReady`（`Started`）"：`Started` 是 PodsReady=True 时的 reason（v1beta2 L1156）。jobs.md L194 另有一个由 kueue-job-controller 发出的 Job 事件也叫 `Started`，意思是"已准入"。两者同名不同义，需要区分。

关闭条件：逐条改正措辞或补充说明。

## acceptance 对照

| acceptance | 判定 | 相关发现 |
|---|---|---|
| 1 Job/Pod/Workload UID、generation/attempt、控制器责任与状态转移；区分 API 接收/admitted/Running/应用 ready/持续进展 | 部分满足。成立的部分：UID 对齐键；"Ready≠Running≠持续进展"的区分。缺口：Workload 命名写错；attempt 来源错位；generation/attempt 未列出；状态转移没有成链，缺 API 接收与调度绑定 | C03（P1）、C05（P2） |
| 2 backoff/deadline/retry/replacement、删除/finalizer、退出/回收与配额撤销；行为绑定版本 | 部分满足。backoff、deadline、TTL、K8s finalizer 的主体正确。缺口：终止条件语义写反；replacement 缺字段且转述与原文相反；Kueue 撤销与清理口径有误或缺失；属主关系与记账转述有误；版本交集与 feature state 不全 | C01、C02（P1）；C07、C08、C09（P2） |
| 3 三视图对齐表、关键事件、卡住/重试/清理的下一项检查 | 部分满足。对齐表与事件都有。缺口：一行把正常状态当成异常；调度事件放错视图；缺删除传播、节点失联、重排循环、按失败原因分流 | C01（P1）；C05、C06（P2）；C11（P3） |
| 4 终止/重试/取消后的账本与应用结果核对方法、官方测试/例子；训练恢复归应用 | 部分满足。训练恢复归应用写得明确，也没有把文档当作已验证的部署指南。缺口：账本口径记为 unknown，但固定 commit 中可以取得；测试只列了目录 | C04（P1） |

横向问题：C10（来源一致性，P2）。

范围外观察（不计入本轮发现）：[空闲设备但作业等待诊断指南](../../knowledge/05-cluster-platform/idle-resource-job-waiting-triage.md) L40 写 v1beta1 与 v1beta2"两者条件集合相同"。本轮比对发现，v1beta2 多出 `BlockedOnPreemptionGates` 与 `WaitingForReplacementPods` 两个条件类型（见上表 Kueue API 行）。该页不在本轮审阅范围内，留待其后续复核处理。

## 结论

**T05-02 初审不通过，需修订。B22-C01–C11 共 11 项：P1 ×4（C01、C02、C03、C04），P2 ×6（C05–C10），P3 ×1（C11），全部 OPEN。**

- 修订后须按各项关闭条件做定向复核。
- C01–C03 关闭前，正文 `verification.status: source_checked` 不应视为成立：其中几处转述与所引原文相反。
- 正文没有虚构命令输出或实测结果；"适用边界"与 `verification.notes` 如实写明未部署集群、未提交 Job，这一点满足要求。
- 本审阅只覆盖编辑与来源层面，未部署集群、未提交 Job、未运行任何测试。文中的 Kubernetes/Kueue 行为都是文档或源码层证据，不得标为 reproduced。

`make check`（写入本报告后运行）：`PASS: 96 content entries; 437 sources.`，即 `Checked structure and local file links; not technical correctness or remote links.`（报告初稿误记 436；作者按审阅者要求机械修正：基线 436，多出的 1 条来自并行 T05-01 会话的登记追加，与 T05-02 无关。）
