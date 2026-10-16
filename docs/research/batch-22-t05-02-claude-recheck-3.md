# 第二十二批 T05-02 第三次定向复核（作者第三轮修订后）

复核日期：2026-10-14（实际取证日）。

**结论：不通过。范围内 3 项（B22-C04、C09、C10）：CLOSED 1（C09），OPEN 2（C04、C10）。连同前两轮已关闭的 8 项（C01–C03、C05–C08、C11），B22-C01–C11 合计 CLOSED 9 / OPEN 2。** 未新增发现 ID。按原 ID 追记两条：

- C04：L68 与 L125 对"删 Job 后 Workload 去留"的说法相互矛盾。这是前次复核的遗漏，本次一并纠正。
- C10：本轮新写入的前提"Workload 是 Job 的依赖对象"没有出处。

前次列出的剩余关闭条件中，C04 三条、C09 一条已全部落实，C10 只落实了一部分。

审阅者角色独立于作者修订角色。审阅模型为 `claude-opus-5-5`，由用户明确要求试用；这不是既有的 `gpt-6.1-sol / xhigh` 批量审阅约定，也不改写该约定。本会话内未见 `[frontier_llm]` 标记、认证失败或模型自报变化。审阅者无法在会话内读取 `modelUsage` 等运行元数据，也不补造。若操作方在运行记录中发现多键或模型不一致，按约定本轮作废，不留档、不引用。

本轮只写本报告一个文件。未改作者正文、来源记录、登记、索引或计划；未部署集群、未提交 Job、未运行任何测试。模型审阅不构成平台或现场验证。

## 输入（以 SHA-256 识别）

| 输入 | SHA-256 | 与任务给定前缀 |
|---|---|---|
| [T05-02 正文](../../knowledge/05-cluster-platform/kubernetes-job-lifecycle.md)（155 行） | `13c255934877bedd2a6d942bf66e675c507705e5a9ca3ecd878e9e0c27564d88` | 一致 |
| [作者来源记录](batch-22-t05-02-sources.md)（26 行，前次 25 行） | `ba311dfee366da39c37a8e3ac4e8e07bf655f9e2f6febf119935c822f2b0cc4c` | 一致 |
| [修订映射](batch-21-review-fixes.md)（T05-02 第三轮修订节 L340–344） | `b51dff7dafe06442268d12f21282888191fe9e75de46b4eac7b5fe01b9115b1a` | 一致 |
| [前次复核报告](batch-22-t05-02-claude-recheck-2.md)（剩余关闭条件权威来源） | `e1d5e767f4fbc3bf9b1a66349766b59dda7d3954de5656fd1295936e6c8fadd4` | 任务未给前缀，记实值 |
| [初审报告](batch-22-t05-02-claude-review.md) | `082ad71dcf190c6846bd3de87f632f02f083eb28b80146a8b11c4a44406e1420` | 任务未给前缀；与前两轮所记相同 |
| [任务计划](../../plans/full-coverage-backlog.yaml)（T05-02 L5431–5467，acceptance L5448–5452） | `5f9bcf865b8c77e13cc8ee5f1c03140c37b86f558d8227d8bb2080249f4fcfc3` | 任务未给前缀；与前三轮相同，计划未变 |
| [来源登记](../../sources/registry.yaml)（440 项；本文相关条目 L129、L559–572、L5347–5385、L5430–5440） | `8d59b5c88cacc70432b93e0b1763ad89d83821bebe53d4964d3a66027b7c5f8a` | 任务未给前缀；与前次复核所记逐字节相同，即本轮修订未改登记 |

七个输入在取证开始和成稿前各哈希一次，结果相同。作者来源记录与正文是未跟踪文件，没有上一轮副本可做 diff。本轮按落盘现状对照前次剩余关闭条件判定，修订映射只用作核对线索。

## 取证方法与限制

- **取证方式**：全部用 `curl -sSL` 只读获取，默认 TLS 校验（`ssl_verify_result=0`），下列原文 HTTP 均为 200。
  - 版本锚用 `git ls-remote`：Kueue `refs/tags/v0.19.0^{}` 为 `911a822a49bcfd99c9c62203a009efa4130ad604`，Kubernetes `refs/tags/v1.32.0^{}` 为 `70d3cc986aa8221cd1dfb1121852688902d3bf53`，与登记和前三轮一致。
  - HTML 去标签后按文字核对，不只判可达性。
  - 原文放在新建临时目录 `/tmp/b22rec3c/`（取证前不存在），未入库。
  - 未使用 GitHub API。
- **与前次复核逐字节比对**：前次已记哈希的 28 个文件重取后全部字节一致，因此前次报告中的行号在本轮仍有效。
  - K8s 侧：Job 页 `b7c09281…`、Pod 生命周期 `3b6cd176…`、ObjectMeta `74abd6c2…`、GC `3bb19013…`、owners-dependents `462bf102…`、Feature Gates `7c308138…`、`job_test.go` `76ab4c0f…`、`strategy.go` `60591891…`、`storage.go` `bf36a996…`。
  - Kueue 侧：jobs.md `9ff23de3…`、workload.md `b6a40f70…`、admission.md `69eb59b9…`、admission_check `6b95a63f…`、troubleshooting_jobs `fe6dfefb…`、cluster_queue.md `7b35c9f7…`、metrics `cd42760a…`、setup_failure_recovery `499ea5b7…`、setup_wait_for_pods_ready `c57c86c1…`、setup_object_retention_policy `4c688b65…`、v1beta2 workload_types `50b9523e…`、v1beta2 clusterqueue_types `6092ac24…`、v1beta2 constants `30cae6ee…`、kube_features `225c13d6…`、workload.go `ccbff32a…`、`jobframework/reconciler.go` `f92d8294…`、集成测试 `cc9a477e…`、installation.md `5260d455…`、README `f508b57e…`。
- **本轮新增取证**：

  | 来源 | 位置 | SHA-256 | 用途 |
  |---|---|---|---|
  | Kueue `apis/kueue/v1beta2/localqueue_types.go`@911a822a | [链接](https://github.com/kubernetes-sigs/kueue/blob/911a822a49bcfd99c9c62203a009efa4130ad604/apis/kueue/v1beta2/localqueue_types.go) | `b0f3766070f59acf23c370b7f098df50605152812391e449f3d40d3b6749d8c5` | L51 `StopPolicy` → C10（L80 stopPolicy 出处候选） |
  | Kueue 集成测试 L4036–4090 测试体 | 同上集成测试文件 | 同 `cc9a477e…` | L4042 的 retention 配置与 ownerReferences 处理 → C04 非阻断 |

- **链接可达性**：正文与来源记录共有 28 个不重复外链，逐个用 curl 打开，最终全部 HTTP 200。其中 3 个 github.com blob 页（v1beta2 `clusterqueue_types.go`、workload.md、metrics.md）首次返回 503，间隔 20 秒内重试后为 200，判为瞬时限流；对应 raw 文件首次即为 200。
- 限制：
  - 测试只读了下表列出的 It 名、`By` 步骤与断言，其余断言未审计；CI 结果未查；所有测试都没有执行。
  - Kueue 集成测试环境是否运行 GC 控制器，本轮未核实。L4072–4074 的注释只能作旁证，不能用来推断真实集群行为。
  - K8s 文档网站的源提交未固定，按 v1.32 快照 HTML 文字核对。
  - 未运行 `make build`，因为它会写 `build/`，与"只写本报告"冲突。

### 关键抽查点（原文文字核对）

| 抽查点 | 原文 | 结果 |
|---|---|---|
| Kueue 集成测试 It/Describe 名 | L2365 `Its workload finalizer should be removed`；L2416 `Should allow reclaim of resources that are no longer needed`；L2707 `Should not readmit a job to the queue after Active is changed to false`；L3388 `should re-queue a workload evicted due to PodsReady timeout after the backoff elapses`；L3916 `Describe("Job controller with ObjectRetentionPolicies")`；L4042 `should delete orphaned Workload after finishing if the Job is deleted with PropagationPolicy=DeletePropagationOrphan`；L4307 `Describe("Job with elastic jobs via workload-slices support")`；L5306 `Should handle rapid scale cycles without quota leaks` | 正文 L88、L125 引用的 It 名与原文逐字一致 → C04 |
| L2416 测试体 | L2419–2420 `Completions(5)`/`Parallelism(2)`；L2454 `createdJob1.Status.Succeeded = 4`；L2462–2465 `ReclaimablePods` 为 `{Name: kueue.DefaultPodSetName, Count: 1}`；v1beta2 `constants.go` L21 `DefaultPodSetName PodSetReference = "main"`；L2471 job2 `Spec.Suspend` 为 false | 正文 L125"Completions(5)/Succeeded=4 后 `ReclaimablePods=[{main,1}]`，job2 解挂"属实 → C04 |
| L2365 测试体 | `By("deleting the job")` 中 `k8sClient.Delete(ctx, job)` 未带传播策略；`By("checking that its workloads finalizer is removed")` 中 Get 成功，且 `ShouldNot(ContainElement(kueue.ResourceInUseFinalizerName))` | 只断言 finalizer 移除；未带策略删除时按 `batch/v1` 默认 Orphan，与正文一致 → C04 |
| L4042 测试体 | L4036–4039 `When("tiny finish retention period")`，`afterFinished = TinyTimeout`；L4072–4074 注释 `In a real scenario, it should be cleared after deletion. … To reproduce that exact scenario, we should make the Workload orphaned.`；L4075–4080 `By("Clear ownerReferences")`，`wl.OwnerReferences = nil`；随后以 `DeletePropagationOrphan` 删除 Job；L4087 `Checking that the Workload is deleted` | 支撑"孤立 Workload 可由 `afterFinished` 回收" → C04 非阻断 |
| `jobframework/reconciler.go` L1476 | `ctrl.SetControllerReference(object, wl, c.Scheme())` | L125 的 GC 前提属实，但正文、来源记录、登记均无此出处 → C10 追记 |
| GC 页 | `By default, Kubernetes uses background cascading deletion unless you manually use foreground deletion or choose to orphan the dependent objects.`；`By default, Kubernetes deletes dependent objects.` | C04 |
| v1.32.0 `strategy.go` L62–74；`storage.go` L56–57 | `case batchv1.SchemeGroupVersion: // for back compatibility return rest.OrphanDependents`；`child pods are preserved by default when jobs are deleted; set propagationPolicy=Background to remove them …` | 正文 L117、L125 属实；L117 链接可达 → C10 |
| setup_object_retention_policy L10–14、L202–208 | `By default, Kueue leaves all Workload objects in cluster indefinitely`；Notes：`deleting the parent Workload owner (e.g. JobSet) can trigger garbage-collection of dependent resources` | 原文主语是 Kueue（Kueue 不主动删除），不是对象寿命 → C04 追记（L68） |
| K8s v1.32 Feature Gates 表 | `PodReadyToStartContainersCondition` true Beta 1.29–；`JobBackoffLimitPerIndex` true Beta 1.29–；`JobSuccessPolicy` true Beta 1.31–；`JobPodReplacementPolicy` true Beta 1.29–；`JobManagedBy` true Beta 1.32– | L130 门控名与默认值属实 → C09 |
| Pod 生命周期页 | `If the PodReadyToStartContainersCondition feature gate is enabled (it is enabled by default for Kubernetes 1.32)` | 正文已链接的页面本身即可支撑 L130 → C09 |
| Job 页 feature-state | Backoff limit per index 只标 `v1.29 [beta]`，未写默认值；Success policy `v1.31 [beta] (enabled by default: true)`；`JobPodReplacementPolicy feature gate (enabled by default)`；managedBy `v1.32 [beta] (enabled by default: true)` | C09 非阻断 |
| `kube_features.go` | L479–480 注释与 L481 常量声明；L788–789 `UnadmittedWorkloadsObservability` 0.19 Beta，默认 false；L547 `PartialAdmission` 0.5 Beta，默认 true；L602–603 `ElasticJobsViaWorkloadSlices` 0.13 Alpha 默认 false、0.18 Beta 默认 true；L683 `FailureRecoveryPolicy` 0.15 Alpha，默认 false；L758 `ConcurrentAdmission` 0.18 Alpha，默认 false | L80 所标行号属实；L84、L130 的门控状态在近处无出处 → C10 |
| `workload.go` L1559–1575 | `IsElasticWorkload` 要求门控开启且注解为 `"true"`（L1561–1566）；`UnadmittedWorkloadReasonWithFallback`（L1568–1575） | L80 所标行号属实；L84 的注解要求在近处无出处 → C10 |
| v1beta2 `clusterqueue_types.go` L132–144、L362–392；`localqueue_types.go` L51；cluster_queue.md L532–548 | stopPolicy 注释：`HoldAndDrain - Admitted workloads are evicted …`、`Hold - Admitted workloads will run to completion …`、`Enum=None;Hold;HoldAndDrain`；状态字段 `flavorsReservation`/`flavorsUsage`/`pendingWorkloads`/`reservingWorkloads`/`admittedWorkloads`；LocalQueue `StopPolicy` | L125 的链接指向状态字段；L80 的 stopPolicy 无出处 → C10 |
| setup_wait_for_pods_ready L107–110；admission_check L119–128；metrics L59、L121–122；installation L39；README L95 | `re-queue … until the number of re-queues reaches backoffLimitCount`、`deactivates the Workload`；Retry 释放 QuotaReservation、Rejected 以 `Deactivated` 驱逐；`kueue_evicted_workloads_total`、`kueue_cluster_queue_resource_reservation`/`_usage`；`A Kubernetes cluster with version 1.29 or newer is running.`；`**Requires Kubernetes 1.29 or newer**.` | 本轮新增链接的所标行号均属实 → C10 |

## 逐项判定

### B22-C04 — OPEN

已落实（对照前次三条剩余关闭条件）：

1. **L88 的 It 名**：L88 已改为 `Should not readmit a job to the queue after Active is changed to false`（L2707），与原文逐字一致。
2. **L2416 归类与全名**：
   - L88 已按原文全名引用 `Should allow reclaim of resources that are no longer needed`，并注明"运行期部分释放 Dynamic Reclaim 样本，非取消"。
   - L125 的"取消见…"只剩 L2707 与 L2365。L2416 单列为"运行期部分释放"，所写测试细节（Completions(5)、Succeeded=4、`ReclaimablePods=[{main,1}]`、job2 解挂）经核对属实。原先"reclaimablePods 非终止后账本信号"与把它列为取消样本之间的矛盾已消除。
3. **删 Job 分支**：L125 已按传播策略分别写出 Workload 的去留：
   - Background/Foreground 下由 GC 删除；Orphan 下保留，可由 `afterFinished` 回收（L4042）。
   - 经 `batch/v1` 删除且未带策略时，默认为 Orphan。
   - 已注明"Kueue 默认不主动删已完成/去活 Workload"不是 GC 行为。
   - "Job 已删但 `resource-in-use` 仍在"一条已改为先区分该 Workload 是否本应被 GC 删除。

   以上与 GC 页、`strategy.go` L62–74、`reconciler.go` L1476 一致。

剩余关闭条件：

1. **追记（前次复核遗漏）：L68 与 L125 矛盾**。L68 写"已准入 Workload 带 `kueue.x-k8s.io/resource-in-use` finalizer（删 Job 后移除…）…；Workload 对象默认一直保留（`leaves all Workload objects in cluster indefinitely`）"。原文（retention 页 L12–13）是 `By default, Kueue leaves all Workload objects in cluster indefinitely`，主语是 Kueue，意思是 Kueue 默认不主动删除。L68 把主语换成了"Workload 对象"，又紧跟在"删 Job 后移除"之后，读者会得出"删 Job 后 Workload 默认一直保留"。这与 L125"Background/Foreground 下 Workload 作为依赖被 GC 删除"直接矛盾。`kubectl delete` 默认使用 background 级联，所以最常见的删除路径恰好落在矛盾的一侧。

   前次复核在 C04 第 3 条已经指出该引文"说的是 Kueue 默认不主动删除…不是 GC 行为"，但只定位到 L125，漏了 L68。需把 L68 改为以 Kueue 为主语的说法，例如"Kueue 默认不主动删除 Workload（非 GC 行为；Job 删除后 Workload 的去留按传播策略，见核对方法第 2 步）"。只需改一处短语。

非阻断：L4042 测试先手动清空 Workload 的 `ownerReferences`（L4075–4080；注释 L4072–4074 说明这是在模拟"真实场景中删除后应被清除"），再以 Orphan 删除 Job。因此该测试支撑的是"孤立的 Workload 可由 `afterFinished` 回收"，并没有实际演示 GC 的孤立处理。L125 的写法可以接受；如果想更准确，可在"测试 L4042"后注明"测试以手动清空 ownerReferences 模拟孤立"。

### B22-C09 — CLOSED

位置证据：L130 已改为"`PodReadyToStartContainers`（Beta，门控 `PodReadyToStartContainersCondition` 默认开）"，有两处来源支撑：

- v1.32 Feature Gates 表：`PodReadyToStartContainersCondition` true Beta 1.29–。
- 正文已在 L58、L82 链接的 Pod 生命周期页：`If the PodReadyToStartContainersCondition feature gate is enabled (it is enabled by default for Kubernetes 1.32)`。

同一行中其他 K8s 门控名与阶段经本轮重新核对仍然属实（见上表）。L58 未标 beta，前次已定为由作者决定。

非阻断：L130"`backoffLimitPerIndex`（v1.29 Beta，门控 JobBackoffLimitPerIndex 默认开）"中的"默认开"只能由 Feature Gates 表支撑。Job 页该节只标 `v1.29 [beta]`，未写默认值，而 Feature Gates 页在正文中没有链接，也不在任何登记条目的范围内。事实本身属实，建议在 L130 链接 v1.32 Feature Gates 页，并把它并入 `src.kubernetes.job-lifecycle-v1-32` 的范围说明。

### B22-C10 — OPEN

已落实（对照前次两条剩余关闭条件）：

- **第 1 条前半**：来源记录 L13 新增 `src.kubernetes.api-gc-v1-32` 一行，ObjectMeta、GC、owners-dependents 三页均有链接。
- **第 2 条大部分**：以下正文链接已补齐，均固定到 v1.32 文档、v1.32.0 tag 或 `911a822a`，并经 curl 确认可达：
  - setup_failure_recovery（L62、L114）
  - setup_wait_for_pods_ready（L115）
  - setup_object_retention_policy（L68）
  - GC 页（L70）
  - `strategy.go`、`storage.go`（L117）
  - admission_check/_index.md（L103）
  - v1beta2 `clusterqueue_types.go` 与 metrics.md（L125）
  - README 与安装页（L130）
  - `kube_features.go` 与 `workload.go`（L80，所标 L479–481、L788–789、L1568–1575 属实）
- 来源记录 L16 已带 Kueue 测试行号。

剩余关闭条件：

1. **来源记录仍未写 `strategy.go`/`storage.go` 的归属**（前次第 1 条后半）。来源记录中检索 `strategy`、`storage.go` 均为 0 命中。这两个文件只出现在登记 L5380（`src.kubernetes.job-controller-tests-v1.32.0` 的 revision 字段），正文 L117 用到了它们。需在来源记录中写明它们归属的登记条目。
2. **正文链接仍有两处未补**（前次第 2 条）：
   - **L80 stopPolicy 无出处**。"`stopPolicy` 是 ClusterQueue/LocalQueue 的字段…只有 `None`/`Hold`/`HoldAndDrain` 三值；非 `None` 即 Inactive"，并直接引了原文 `Admitted workloads will run to completion`，但近处既无链接也无页名，正文全文也未提及 cluster_queue.md。L125 虽然链接了 `clusterqueue_types.go`，但标注的是 "v1beta2 L362–392" 状态字段，不是 stopPolicy 所在的 L132–144。需在 L80 链接 v1beta2 `clusterqueue_types.go` L132–144 或 cluster_queue.md L532–548。LocalQueue 一侧可加挂 `localqueue_types.go` L51，由作者决定。
   - **L84 与 L130 的 Kueue 门控状态无出处**。L84 写 `PartialAdmission`（v0.5 Beta，默认开）、ElasticJob（v0.18 Beta 默认开，仍需逐个 Job 加注解）、Concurrent Admission（v0.18 Alpha，默认关）；L130 还写了 FailureRecoveryPolicy（v0.15 Alpha，默认关）。`kube_features.go` 的链接只出现在 L80，且所标行号只对应 `UnadmittedWorkloadsObservability`。读者无法从 L84、L130 找到这些阶段与默认值的出处。需在 L84 引 `kube_features.go` L547、L602–603、L758 和 `workload.go` L1561–1566（注解判定）；L130 可指回 L84 或补 L683。
3. **追记（本轮新写入的前提无出处）**：L125"Background/Foreground 下 Workload 作为依赖被 GC 删除"成立的前提是 Kueue 把 Job 设为 Workload 的 controller owner（`jobframework/reconciler.go` L1476 `ctrl.SetControllerReference(object, wl, …)`）。该出处在正文、来源记录、登记中都没有出现：
   - 登记 `src.kueue.job-lifecycle-v0.19.0` 的 revision（L5366）只覆盖 `pkg/workload`，不含 `pkg/controller/jobframework`，且登记文件与前次复核时逐字节相同。
   - 正文已链接的 retention 页 Notes（L207–208）只间接写到 `parent Workload owner (e.g. JobSet)`，不能支撑"Job 是 Workload 的属主"。

   需在 L125 链接 `reconciler.go` L1476，并把 `pkg/controller/jobframework/reconciler.go` 写入登记范围与来源记录。该前提由前次复核提供，作者采用了结论但没有挂出处。按 AGENTS.md "cite exact supporting pages or revisions near substantive claims"，本条与本项其余链接要求同一标准。

非阻断：

- L82"达 `backoffLimitCount` 后去活见 setup_wait_for_pods_ready L107–110"仍是纯文本。该页在 L115 已有链接，可以接受；顺手可在 L82 也加链接。
- frontmatter `verification.notes`（L29）列出的核对范围仍未包括 setup_* 三页、metrics、`kube_features.go`、`workload.go`（以及补登后的 `reconciler.go`），与正文实际依据不同步。
- 前次已记、仍未改：
  - 登记 `src.kubernetes.job-controller-tests-v1.32.0` 的标题（L5376）仍为"（存在性）"，license notes（L5384）仍写"只链接并记录存在性"，而 revision（L5380）已写"上游行为样本"。
  - 同一 K8s 条目的 revision 还收录了 Kueue `job_controller_test.go` 的 It 行号（来源记录 L16 也把 Kueue 测试归在该 ID 下），而 Kueue 条目 L5366 同样声称覆盖测试行号。建议把 Kueue 测试统一归到 Kueue 条目。

## 修订映射核对

映射 L340–344 与落盘状态对照：

- C04"L88 It 名按原文；L2416 改运行期部分释放样本＋全名；删 Job 分支按传播策略…；不一致判读加 GC 区分"：与正文 L88、L125 一致。映射未提 L68，前次复核也未点名，不算映射失实。
- C09"PodReadyToStartContainersCondition 门控名"：与 L130 一致。
- C10"metrics/clusterqueue/setup 三文档/retention/GC/strategy-storage/admission_check/README-安装页/kube_features-workload 链接补齐"：大部分属实，但有两处不完整：
  - "clusterqueue"只有 L125 指向状态字段的链接，L80 的 stopPolicy 仍无出处。
  - "kube_features-workload"只落在 L80，L84、L130 未补。
- C10"来源记录 api-gc 行＋测试行号＋unknown 同步"：api-gc 行与测试行号已落盘。unknown 清单现状与正文一致，但来源记录无上一轮副本，无法确认本轮具体改了哪一条。`strategy`/`storage` 的归属未补，映射也未声称已补。
- 登记哈希与前次复核所记相同，本轮未改登记，映射未声称改登记，二者一致。

## acceptance 对照

| acceptance | 判定 | 未关闭发现 |
|---|---|---|
| 1 UID、generation/attempt、控制器责任与状态转移；区分 API 接收/admitted/Running/应用 ready/持续进展 | 满足。与前次相同，本轮未改动相关段落 | —（C10 横向） |
| 2 backoff/deadline/retry/replacement、删除/finalizer、退出/回收与配额撤销；行为绑定版本 | 基本满足。K8s 门控名已补齐（C09 关闭）；删 Job 后 Workload 的去留在 L125 已按传播策略区分，但 L68 仍有相反表述；Kueue 门控阶段与默认值属实，但 L84、L130 近处无出处 | C04、C10 |
| 3 三视图对齐表、关键事件、卡住/重试/清理的下一项检查 | 满足。与前次相同 | —（C10 横向） |
| 4 终止/重试/取消后账本与应用结果核对、官方测试/例子；训练恢复归应用 | 基本满足。四种取消触发、不一致判读、测试归类与 It 名均已改正，"训练恢复归应用"仍写明（L126）；只剩 L68 与取消分支矛盾 | C04 |

横向问题：C10（来源记录归属与正文出处）。

## 结论

**T05-02 第三轮修订后第三次定向复核不通过：范围内 CLOSED 1/3（C09），OPEN 2/3（C04、C10）；B22-C01–C11 合计 CLOSED 9/11、OPEN 2/11。**

- 前次 C04 的三条剩余关闭条件（L88 It 名、L2416 归类与全名、删 Job 分支按传播策略）与 C09 的门控名均已按原文落实，经本轮独立重取核对属实。
- 仍需修订的事实问题只剩一处：C04 追记的 L68，即"Workload 对象默认一直保留"与 L125 的 GC 分支矛盾，改一处短语即可。
- C10 剩余的是出处问题，所涉事实本身均已核实属实：
  - 来源记录补 `strategy.go`/`storage.go` 的归属；
  - L80 补 stopPolicy 出处；
  - L84（及 L130）补 `kube_features.go`/`workload.go` 行号链接；
  - L125 补 `reconciler.go` L1476 链接，并把该文件写入登记范围与来源记录。
- 建议修订顺序：先改 L68（C04），再一次性处理 C10 的四处出处；非阻断项（L4042 模拟孤立注记、Feature Gates 页链接、L82 链接、frontmatter notes 同步、测试条目标题与 Kueue 测试归属）可在同一轮顺手处理。
- 修订后需按上列剩余关闭条件做定向复核。
- 本复核只覆盖编辑与来源层面。文中 Kubernetes/Kueue 行为都是文档或源码层证据，不得标为 reproduced；正文 `verification.status: source_checked` 在上述问题修订前只能视为部分成立。
