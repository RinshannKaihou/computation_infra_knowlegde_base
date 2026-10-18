# Batch 24 / T05-10 Codex 定向复核第三轮

## 1. 复核信息与结论

- 日期：2026-10-19（Asia/Shanghai）。范围仅为第二轮遗留的 **B24-T10-C02、C04、C06、R01**，以及关联修订可能影响的已关闭项；不评价 Batch 24 其他任务，也不宣告 05.2/05.3/05.7 主题整体完成。
- 执行者：本会话 Codex，承担独立于作者的技术审阅角色；未派发子代理、其他模型或外部审阅 CLI。当前上下文没有可独立核验的实际底层模型与推理档位运行元数据，实际模型/档位记录为 **unknown**；不以仓库约定或导航标签代替实际执行记录，不改写历史报告。
- 上轮 **4 项 OPEN：本轮 CLOSED 3 / 仍 OPEN 1**。关闭 C04、C06、R01；C02 仍为 **OPEN / P2**。
- 无独立新发现，**B24-B24-T10-S3-xx 共 0 项**。累计原 C01–C10 与 R01/R02 为 **CLOSED 11 / OPEN 1**；开放级别为 **P1 0、P2 1、P3 0**。累计关闭数沿用前轮结论，不表示本轮重新全量审阅全部已关闭项。
- **结论：暂不通过。** C02 的对象版本/缓存验证方法仍存在实质缺口，尚不满足“全部上一轮 OPEN 项 CLOSED”。
- 本轮只新增本报告；不修改正文、作者取证、来源登记、导航、计划或原工作区构建产物。没有执行恢复、集群查询、故障注入或任何上游测试。

## 2. 输入与独立取证

### 2.1 本地输入

先读取 `README.md`、[内容编写指南](../authoring-guide.md)与[内容归属](../../content-outline.md)，再按[第二轮报告](batch-24-t05-10-codex-recheck-2.md)核对剩余关闭条件；仅为解释 C06 原验收下限，回看[初审](batch-24-t05-10-codex-review.md)与[第一轮复核](batch-24-t05-10-codex-recheck.md)，不重开其余问题。

| 简称 | 当前输入及定位 |
|---|---|
| P | [修订正文](../../knowledge/05-cluster-platform/control-plane-recovery.md)，L1–170；重点 L68–72、L93、L112–113、L124–142、L148–158 |
| A | [作者取证记录](batch-24-t05-10-sources.md)，L182–187“修订轮三补充”；历史补充与本轮新证据分开使用 |
| R | [来源登记](../../sources/registry.yaml)，K8s 测试 L5397–5407、Slurm testsuite L5430–5440、etcd L6089–6099、字段源码 L6111–6121 |
| T | [任务表](../../plans/full-coverage-backlog.yaml)，T05-10 L5785–5831；四项 acceptance 位于 L5803–5806 |
| 复用内容 | [作业生命周期](../../knowledge/05-cluster-platform/kubernetes-job-lifecycle.md) L48–54 的计数与终态时序；[节点摘除流程](../../knowledge/05-cluster-platform/node-drain-resource-reclamation.md)的身份账本与三层门槛；[05 章入口](../../knowledge/05-cluster-platform/index.md)的交付/审阅状态 |

本轮读取时的 SHA-256：

| 文件 | SHA-256 |
|---|---|
| 第二轮复核报告 | `bd4ad4c8856b6681e72f1382eb90bc0a611e68e0c64f6126422c8c106d9bceb2` |
| 修订正文 | `a8d317aa496bc4517f45b455fb9aecfb575205541ee8e46c2139f65bff59996c` |
| 作者取证记录 | `c4040bb6a8cc467551abbf81ba6874338aeb55e17e344543abea75242612006d` |
| 来源登记 | `3ea07202e7e0573c8ff8089bc5fcdd142b5a51269dc1f646a9d4a08d065215a2` |
| 05 章导航 | `3d28506567fe39bec4e0e54650cdd9aea6a1a55c741ae3dd16246434b7f970b3` |
| 任务表 | `53bfc8fe47d56ab322e546c853858cbaa90cf5a5d0305b33a80bab0f39275d54` |

### 2.2 精确上游证据

只对下列官方版本页、固定 tag 原文件实施只读 HTTP GET。**curl 取回均为 HTTP 200**，文件仅存于仓库外临时目录。网页阅读工具打开 Slurm raw 文件返回 Internal Error，随后 curl 对同一 URL 成功；不将阅读工具错误解释为上游文件不存在。源码行号来自下载的原文件，不用网页渲染行号拼接源码锚点。

| 证据 | 精确材料与实读范围 | SHA-256 前 16 位 |
|---|---|---|
| E01 | [Kubernetes v1.32 API Concepts](https://v1-32.docs.kubernetes.io/docs/reference/using-api/api-concepts/#resource-versions)：Resource versions、对象/集合 RV、get/list 请求语义及返回新鲜度 | `ca03957baf69b180` |
| E02 | [etcd v3.5 Disaster recovery](https://etcd.io/docs/v3.5/op-guide/recovery/)：快照输入/WAL 缺口、Revision Difference、恢复成员身份、完整性校验、revision bump、End-2-End Example | `477f55130af7c597` |
| E03 | [Kubernetes v1.32 Jobs](https://v1-32.docs.kubernetes.io/docs/concepts/workloads/controllers/job/#terminal-job-conditions)：终态条件、Pod 终止、门控与 terminating 字段 | `b7c0928182a470c6` |
| E04 | [Operating etcd / Kubernetes v1.32](https://v1-32.docs.kubernetes.io/docs/tasks/administer-cluster/configure-upgrade-etcd/#restoring-an-etcd-cluster)：恢复顺序、工具/目录与访问 URL 改变时的条件 | `19e528c0790d486b` |
| E05 | [Slurm test_102_5.py / slurm-24-11-7-1](https://github.com/SchedMD/slurm/blob/slurm-24-11-7-1/testsuite/python/tests/test_102_5.py#L71-L124)：L15–23、L71–124 的前提、DBD/ctld 停起与新旧作业断言 | `ae908d7c1f66ad9f` |
| E06 | [K8s job_test.go / v1.32.0](https://github.com/kubernetes/kubernetes/blob/v1.32.0/test/integration/job/job_test.go)：L1236–1619、L3686–3822，以及 L4445–4478 的测试服务/控制器/缓存同步辅助逻辑 | `76ab4c0f580c396b` |
| E07 | [K8s job_controller_test.go / v1.32.0](https://github.com/kubernetes/kubernetes/blob/v1.32.0/pkg/controller/job/job_controller_test.go)：L6993–7041、OnFailure 测试的配置/期望字段、L7401 起的 Never 分支；区分队列退避与作业失败重试语义 | `b78d06e36bc9562a` |

E01–E05 的字节哈希与第二轮实读记录一致；E05/E07 与 A L186 的完整哈希一致。E06 本轮完整哈希为 `76ab4c0f580c396bad803ae72249bf341e6111d9618d3e52bde261bc4e734da6`。etcd v3.5 页面仍是版本路径文档而非固定源码 commit；取得该页不证明目标 etcd/etcdutl patch 支持全部选项。

没有重跑作者的“593 个 expect 用例”检索，不独立背书该数量或某类用例在整个上游仓库不存在；“未定位到”仅按作者已经披露的取证边界保留。未运行 Go、pytest、Expect 用例，也未执行材料中的 daemon 停起、QOS 修改、快照或恢复动作。

## 3. 第二轮 OPEN 项逐项判定

| 编号 / 原级别 | 本轮对应位置 | 判定与依据 |
|---|---|---|
| **B24-T10-C02 / P2** | P L72、L93、L113、L142、L163；A L184 | **OPEN。** 已撤销 L72“revision 差值决定重放量”的表述，增加缺证不放行，并将工具选项和端点/证书处理降为有前提的说明。但是 L113 仍两次把恢复前后对象清单及 RV 比对说成能够确认/证明“回退幅度与快照一致”，没有落实第二轮要求的全局 revision、恢复读取与受核控制器/客户端缓存证据的分离；详见 §3.1。 |
| **B24-T10-C04 / P2** | P L125；A L185；生命周期 L54 | **CLOSED。** 已把 v1.32 默认开启相关门控时“所有 Job Pod 终止后才添加 Complete/Failed”的顺序接入恢复核对；补早期条件、terminating 与门取值未知时的限制，且明确复用生命周期终态说明。E03/E06 支持，不再只是点出门控名。 |
| **B24-T10-C06 / P2** | P L131–142，尤其 L135、L137；A L186；R 的既有测试来源 | **CLOSED（限原问题要求的相关关键分支材料交付）。** Slurm 新交付用例确有 DBD/ctld 停起与三类作业断言；K8s 新列的 TestJobFailedWithInterrupts 确有取消并重建 Job controller 后检查 JobFailed，不只是普通 Pod 失败单测。固定路径/版本/函数与边界已可定位，详见 §3.3。此关闭不扩展成 etcd 灾备、API server 故障或 HA 专项测试已覆盖。 |
| **B24-T10-R01 / P2** | P L93；A L187；R L6099 | **CLOSED。** 当前 registry notes 已与正文一起区分快照文件、离线 member/snap/db 单文件和恢复输出目录，并记录 WAL 缺口；不再把输入单文件误写为整个数据目录。工具 patch 支持仍是未核前提，不因工件修正宣告可执行。详见 §3.4。 |

### 3.1 C02：停止规则已补，但错误的“可证明”关系仍在

接受本轮已经完成的三类修订，不要求作者本轮做现场恢复：

1. **风险量不再等同重放量。** P L72 已把 etcd 全局 REVISION 差异改为提示旧版本位置/风险规模，不再说它决定业务重放量。
2. **未核选项与拓扑不再一律处方化。** P L93 对 `--skip-hash-check` 增加所选工具版本核实前提和非操作建议的边界；端点/证书按 stacked/external 布局分别核对，未核步骤保留 unknown。P L113 对 revision bump 同样未声称已验证可用。
3. **缺证不放行已经明说。** P L113 第③点新增未通过/未完成，不能因没有观察到异常就默认完成。这一进步成立，不再沿用“完全没有缺证停止条件”的旧评价。

仍未完成的是第二轮 §3.1 第 2 点明确提出的证据分离。P L113 第①点仍要求对象清单/RV 比对“确认回退幅度与预期快照一致”；第③点又称它“只能证明”同一结论。句末虽禁止比较 RV 大小，却没有撤销前面的充分性判断。

E01 明确对象 `metadata.resourceVersion` 是该对象最后一次修改的版本，不表示该次读取的新鲜度；RV 按不透明值处理，只可比较相等。**本轮审阅推理的反例（不是本地事故记录）**：某对象在快照前后均未修改时，对象内容与 RV 可以相同，而其他键及全局 revision 已变化；因此这个对象的相等结果不能量出全局回退幅度，更不能证明某个未观测客户端的缓存刷新。依据为 E01 的 Resource versions / get-list 语义与 E02 的 Revision Difference。

当前第②点仍只是观察窗口内动作抽查，第③点仍将证明责任落在泛化的“对象行为”。没有说明本次覆盖哪些控制器/客户端、哪一实例/启动世代、哪次 list/watch 重建，或如何排除仅 API 读到预期值、实际消费者仍持有旧缓存的情形。新增 fail-closed 限制有助于防误放行，但它不使原先的证据能力判断变正确，也未给出可填写的覆盖记录。

**维持 OPEN / P2 的影响：** 读者仍可能把对象清单及 RV 一致当作存储回退幅度证据，再用少量动作抽查代替具体消费者缓存核验；这正是原 C02 的证明链缺口，不另编 S3 新问题。

**最小关闭条件：**

- 删除或改正 L113 两处“对象清单/RV 证明回退幅度”的结论。对象核对可以发现身份、内容或预期副作用差异，不能据此计算全局 revision 差值。
- 将快照身份、快照/故障前全局 revision、恢复后原始或已 bump 的 revision 分别记录；缺少故障前证据时将幅度记 unknown，不从对象 RV 推算，也不凭固定“数百/数千”补值。
- 将恢复后的读取记录与消费者记录分开：前者复用 L70 的参数/时间/API server/集合信息；后者记录受核控制器或客户端、实例/启动世代、所需缓存重建或重新 list/watch 的版本相关证据、观察窗口和预期动作。可以明确复用已有方法，无需增加通用恢复命令。
- 保留第③点缺证不放行，并明确未覆盖消费者或无法解释的证据不能由其他对象抽查通过代替。该条件要求方法设计，不要求伪造现场运行结果或证明不存在的通用完成指标。

### 3.2 C04：终态时序现已接入恢复判断

P L125 在保留正确的 Job condition、Pod phase、成功/失败统计及配置限额区分之外，明确写出门控前提、终态延迟顺序和 `FailureTarget`/`SuccessCriteriaMet` 早期信号；未知有效门值时不据 conditions 断言所有 Pod 已终止。终态说明与生命周期引用不再仅附着在 TTL/GC 清理上。

E03 的 Terminal Job conditions / Termination of Job pods 支持该顺序。E06 的 `TestDelayTerminalPhaseCondition` 还对不同门控设置、早期/最终状态分别建预期，并在 L1598–1616 先检查中间状态，再模拟剩余 Pod 进入终态，最后检查终态状态。`terminating` 字段的存在性仍受相应门控约束，不能把未知/缺失值自动当 0；正文已经把门值未知情形留为 unknown。

因此本项 **CLOSED**。这只关闭终态时序的文档缺陷；Job/Pod 的 API 终态、进程实际停止与设备/卷释放仍按 P L124/L127 及复用流程分别取证，不由本轮源码阅读建立现场资源释放保证。

### 3.3 C06：接受真实控制器重建材料，不把所有测试等同灾备

与第二轮不同，本轮关键测试已经由作者列入 P/A，不再是仅由审阅者发现、尚未纳入交付的候选材料。

| 已交付材料 | 本轮独立核对到的实际触发与断言 | 接受范围 |
|---|---|---|
| Slurm `test_qos_removal_single`，E05 | L15–23 要求自动配置、slurmdbd 记账与 associations/qos enforcement；L77–109 先停 DBD，建立运行/等待作业，再停 ctld、启 DBD、删除 QOS、重启 ctld；L111–124 检查旧作业仍 RUNNING、旧等待作业仍 **PENDING 且 reason=InvalidQOS**、新提交被拒 | 是调度器重启与数据库状态差异的相关恢复样本；InvalidQOS 是等待原因，不是额外作业状态。不是主备切换、状态目录灾备或应用进展保证 |
| K8s `TestJobFailedWithInterrupts`，E06 L3774–3822 | 设置 10 个并行 Pod、backoffLimit=0，模拟一个失败和其余成功；L3818–3821 取消当前 controller、调用辅助函数重建 controller，检查 JobFailed。L4466–4478 的辅助函数新建 informer factory 并等待缓存同步 | 有实际的控制器取消/重建触发，不是仅凭测试名推断有控制面中断；接受为 Job controller 重建后终态核对的上游行为样本，不是进程崩溃、leader failover、API server/etcd 回滚验证 |
| 终态/退避辅助材料，E06/E07 | TestDelayTerminalPhaseCondition 核验门控下中间/终态；指数退避集成测试模拟 Pod 失败；TestJobBackoff 族覆盖队列退避及两种 restartPolicy 计数 | 仅支撑对应字段/时序/重试核对。它们本身不是 etcd 灾备故障测试，也不能证明 C02 的恢复缓存验证充分 |

据此，本轮满足原 C06“至少为 K8s/etcd 与 Slurm 关键分支提供真正相关、可定位的官方故障材料”的最低交付：K8s 取控制器重建分支，Slurm 取 DBD/ctld 停起分支。**不新增“每个故障分支都必须有自动化用例”的关闭条件。** P L137 已将材料限定为控制器行为级且排除 etcd/API server 故障；P L138–142 也如实保留 HA/etcd 专项测试缺证和未执行演练。

E02 的灾备指南及 End-2-End Example 仍只是程序性材料；正文未把它伪装成自动化测试或真实事故案例，本轮不借其关闭“etcd 专项测试已覆盖”。**C06 的 CLOSED 不消除这些显式缺证，也不把源码中的 WaitForCacheSync 直接移植为目标恢复环境的完成证明。**

### 3.4 R01：登记中的工件口径已同步

R L6099 现与 P L93、A L187 一致：①snapshot save 生成的带完整性哈希快照文件；②数据目录中离线提取的 `member/snap/db` 单文件，可能缺少只在 WAL 的更新；③恢复创建的输出目录。E02 的 Snapshotting the keyspace、Restoring from snapshot 与 Integrity Checks 支持该区分。

原来的“直接拷贝的数据目录须 skip-hash-check”已不在本轮 registry notes 中；现在明确第②类是单文件，而非整个 data directory。选项仅放行相应哈希校验、不证明数据完整的限制也保留。R 的 revision 字段继续要求按目标工具 patch 核对具体选项，正文同样保留未核版本前提。**R01 CLOSED**，不与 C02 剩余缓存证明缺口混算。

## 4. 已 CLOSED 项的关联回归抽查

只抽查与本轮缓存、终态、测试依赖改动直接相连的关闭项，不重做其他 Slurm/设备/训练分支的全量审阅。

| 既有项 | 本轮抽查理由及结果 | 状态 |
|---|---|---|
| B24-T10-C01 / P2 | L72/L113 改动涉及 RV 与缓存，故复查 P L70。未设 RV 的 get/list 与 RV=0 仍分别为 Most Recent/Any，保留无 continue token 的范围、请求参数/时间/API server 身份，与 E01 一致。L113 错误的证明关系归 C02，不把原参数映射问题重开 | **CLOSED（维持）** |
| B24-T10-C03 / P2；R02 / P3 | 终态行 L125 与身份行 L124 相邻，复查容器级 restartCount、Pod/owner Job UID、containerID、节点/时间/应用 attempt 映射及身份账本引用；未退回跨 Pod 重建序号。core/v1 来源仍登记并列入 source_refs；本轮未重新下载其上游文件，不宣称做了新一轮字段源码全审 | **CLOSED（维持）** |
| B24-T10-C09 / P3 | 测试表扩展后复查依赖：仍使用已登记的 K8s Job 测试来源与 Slurm testsuite 来源，K8s 集成路径也在该登记覆盖范围；正文 22 个 source_refs 均能解析，没有因新增精确用例而漏列新的独立来源 ID | **CLOSED（维持）** |

C05、C07、C08、C10 等不另做独立技术重审，累计状态沿用第二轮。导航与任务表哈希和第二轮记录一致，仍未把本任务改成审阅通过或计划完成。

## 5. 新问题与剩余问题统计

**本轮无独立新问题，B24-B24-T10-S3-xx：0 项。** L113 的错误证明链是第二轮已明确指出、尚未完整消除的 C02，不重复登记新 P2。C06 关闭后的 HA/etcd 专项证据限制继续明示，不把缺证说成已覆盖或实际失败。

| 统计对象 | CLOSED | OPEN P1 | OPEN P2 | OPEN P3 |
|---|---:|---:|---:|---:|
| 本轮待复核的 4 项 | 3 | 0 | 1 | 0 |
| 累计 C01–C10、R01/R02 | 11 | 0 | 1 | 0 |
| 本轮独立新发现 | 0 | 0 | 0 | 0 |

## 6. T05-10 任务验收重核

对照 T 的原四项 acceptance。“满足”仅指本文档交付与所声明边界，不代表真实环境恢复验证通过。

| 验收条目 | 本轮依据与剩余限制 | 判定 |
|---|---|---|
| 1. 只读证据入口、身份/时间戳/对象版本、leader/quorum/cache/状态存储责任；资源视图不证明设备和应用正常 | P L60–84 保留分层入口、请求语义和跨层边界，身份映射未回归。但 L113 仍将对象/RV 比对说成能证明全局回退幅度，缓存结论的专门证据链未闭环，见 C02 | **部分满足，未通过** |
| 2. K8s API/etcd/控制器与 Slurm ctld/slurmd/dbd 分支按官方前提；不混同调度与记账 | P L88–105 的分支仍在。etcd 同快照/新逻辑身份/隔离条件保留，端点/证书按布局核对，未核步骤与 patch 不再声称已验证；Slurm 调度/数据库职责不互替。本轮未对其余已关闭 Slurm 机制重新全量取证 | **在已声明的文档/unknown 边界内满足；不等于可直接执行** |
| 3. 备份/恢复/重建前提、版本/集群身份、回放/重复调度风险、保护证据与停止门槛 | P L93、L107–116 已修正工件与选项条件，R01 同步完成，缺证不放行也已增加；但 C02 的“如何判定”仍含错误证明能力，不能仅因有停止语句就通过 | **部分满足，未通过** |
| 4. 重复/过期分配、未完成/已完成、attempt/Checkpoint、资源清理、健康/准入、新旧任务正确性与进展；官方故障材料与未执行演练 | P L124–150 保留分类核验矩阵，C04 时序已接入，C06 已交付 K8s 控制器重建与 Slurm 停起的限定故障样本；P L142 明示方法未执行，HA/etcd 专项测试缺证不冒充已覆盖。整体恢复放行仍受第 3 项 C02 约束 | **满足本项最低文档交付；非全部故障模型覆盖或实测通过** |

## 7. 操作边界与结构验证

- P 保持 `draft / source_checked / platforms: [generic]`，环境档案为空；没有把 generic、版本化资料或源码测试存在性当作 GPU/NPU 配套或真实恢复证明。
- 本轮没有执行 kubectl、etcdctl/etcdutl、scontrol、sacct、daemon 停起、上游测试或其他集群操作；网络取证仅为精确官方证据的只读 GET。
- 报告落盘后在原工作区执行 `PYTHONDONTWRITEBYTECODE=1 make check`：`PASS: 103 content entries; 493 sources.`；另独立解析 P 的 22 个 source_refs，未解析 ID 为 0。
- 将工作区连同既有 build 复制到仓库外临时副本，排除 `.git`、`.venv` 与字节码缓存；使用原虚拟环境解释器执行 `make build`，同为 `PASS: 103 content entries; 493 sources.`，成功生成副本的 `build/catalog.json` 与 `build/catalog.md`，未改写原工作区 build。这些检查仅验证结构及本地引用，不证明技术正确性、远程证据完备或硬件恢复。
- 复核前建立既有文件 SHA-256 清单；报告落盘与检查后复验，清单中的 **500 个既有文件逐字节不变**，新增文件只有本报告。Git 状态与复核前相比也只有本报告一项新增，原有未提交修改/未跟踪文件均保留。
- 未修改 `src/kb/`，不新增软件测试，不运行 `make test`。保持原有未提交修改与未跟踪文件，不提交 Git，不更新任务/导航状态。

## 8. 最终结论与下一轮入口

**暂不通过。** 第二轮遗留 4 项本轮 **CLOSED 3 / OPEN 1**；C04、C06、R01 关闭，**B24-T10-C02 / P2** 继续 OPEN，无新 OPEN P1/P2。

下一轮仅需围绕 C02 及关联回归：撤销对象 RV 能证明全局回退幅度的结论，区分快照/全局 revision、恢复后 API 读取和具体消费者缓存重建证据，并让缺证不放行落到明确的覆盖记录。满足这些关闭条件且无新 OPEN P1/P2 后，才可给出 T05-10 文档审阅“通过”。即使后续通过，也不代表本库已在真实集群完成灾备、HA、资源回收或应用恢复验证。
