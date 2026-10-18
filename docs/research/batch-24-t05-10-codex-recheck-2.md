# Batch 24 / T05-10 Codex 定向复核第二轮

## 1. 复核信息与结论

- 日期：2026-10-18（Asia/Shanghai）。本轮只评价 T05-10，不评价 Batch 24 其他任务或 05.2/05.3/05.7 主题整体完成情况。
- 执行者：本会话 Codex，承担独立于作者的技术审阅角色；未派发子代理、其他模型或外部审阅 CLI。当前上下文没有可独立核验的实际底层模型及推理档位运行元数据，记录为 **unknown**，不以模型约定代替实际执行记录。
- 第一轮留下的 **7 个 OPEN 项：本轮 CLOSED 3、仍 OPEN 4**。关闭 C01、C03、R02；保留 C02、C04、C06、R01，四项均为 P2。
- 对第一轮已关闭的 5 项作关联回归抽查，均维持 CLOSED。累计原 C01–C10 为 **CLOSED 7 / OPEN 3**；加上 R01/R02 后为 **CLOSED 8 / OPEN 4**。
- 本轮独立新发现：**0 项**，不新增 B24-T10-S2-xx 编号。累计开放 **P1 0、P2 4、P3 0**。
- **结论：暂不通过。** 尚不满足“全部上一轮 OPEN 项 CLOSED”。本结论不要求本轮执行灾备演练，也不把文档修订、结构检查或上游测试存在性当作真实恢复验证。
- 本轮只新增本报告；不修改正文、作者取证、来源登记、导航、任务状态或原工作区构建产物。

## 2. 输入与取证边界

### 2.1 本地输入

先读取 `README.md`、[内容编写指南](../authoring-guide.md)及[内容归属](../../content-outline.md)，再对照[初审报告](batch-24-t05-10-codex-review.md)、[第一轮复核](batch-24-t05-10-codex-recheck.md)的原问题与关闭条件。本文使用以下简称，行号均指本轮读取的源文件，不把旧报告的正文行号直接套到新正文：

| 简称 | 文件与复核位置 |
|---|---|
| P | [修订正文](../../knowledge/05-cluster-platform/control-plane-recovery.md)，全文 L1–164；重点 L70–72、L93、L112–113、L124–146、L157 |
| A | [作者取证记录](batch-24-t05-10-sources.md)，尤其 L173–180“修订轮二补充”；结合 L29、L36、L60、L163–171 区分历史记录与本轮增补 |
| R | [来源登记](../../sources/registry.yaml)，重点 L5430–5440 的 Slurm testsuite、L5877–5890 的 API Concepts、L6089–6099 的 etcd 灾备、L6111–6121 的 core/v1 types.go |
| N | [05 章入口](../../knowledge/05-cluster-platform/index.md)，L59、L77、L82 的交付及审阅状态 |
| T | [完整覆盖任务表](../../plans/full-coverage-backlog.yaml)，T05-10 L5785–5831 的目标、四项 acceptance 与来源要求 |
| 复用规则 | [节点摘除流程](../../knowledge/05-cluster-platform/node-drain-resource-reclamation.md) L184–208 的三层门槛及身份账本；[作业生命周期](../../knowledge/05-cluster-platform/kubernetes-job-lifecycle.md) L50–54、L72 的终态时序与统计；[Checkpoint 一致性](../../knowledge/06-training/checkpoint-state-consistency.md) L126–142 的持续观察及停止规则 |

本轮输入 SHA-256：

| 文件 | SHA-256 |
|---|---|
| 第一轮复核报告 | `88ad0f5baf83102b830c0b5a77bafeda77c467020a24859114a516eb87cf018a` |
| 修订正文 | `6b86e89ac4ce11b19f18ee59711c88f4a0ded1a5aa97384e5d5b892b14ec94b4` |
| 作者取证记录 | `200eb0efe803b6d194da60e5fc2bcbf1990845ca096799acb72898b43ec361c5` |
| 来源登记 | `656c2f814bb2b0a28bd60de2c3a113f133550ae0ddd12eb1c6e4305646354d15` |
| 05 章导航 | `3d28506567fe39bec4e0e54650cdd9aea6a1a55c741ae3dd16246434b7f970b3` |
| 任务表 | `53bfc8fe47d56ab322e546c853858cbaa90cf5a5d0305b33a80bab0f39275d54` |

### 2.2 独立重开的一手证据

只实施只读 HTTP GET 和本地文本核对。以下 **9 个精确 URL 的 curl 响应均为 HTTP 200**；响应仅保存在仓库外临时目录，没有镜像进正文。网页阅读工具对 Slurm test37.5 的 GitHub 页面及 raw URL 返回 Internal Error，但 curl 对同 tag、同路径的 raw 文件成功，不能将阅读工具错误写成上游文件缺失。

| 证据 | 精确页面或固定 tag 文件、实读范围 | SHA-256 前 16 位 |
|---|---|---|
| E01 | [Kubernetes v1.32 API Concepts](https://v1-32.docs.kubernetes.io/docs/reference/using-api/api-concepts/#semantics-for-get-and-list)，get/list 参数矩阵、Most Recent/Any、Resource versions | `ca03957baf69b180` |
| E02 | [etcd v3.5 Disaster recovery](https://etcd.io/docs/v3.5/op-guide/recovery/)，Snapshotting the keyspace、Revision Difference、Restoring from snapshot、Integrity Checks、Restoring with revision bump | `477f55130af7c597` |
| E03 | [Kubernetes v1.32.0 core/v1/types.go](https://github.com/kubernetes/kubernetes/blob/v1.32.0/staging/src/k8s.io/api/core/v1/types.go#L3096-L3114)，原文件 L3096–3100 的重启计数与 L3110–3114 的容器 ID | `ecc3289051e4c011` |
| E04 | [Kubernetes v1.32 Jobs](https://v1-32.docs.kubernetes.io/docs/concepts/workloads/controllers/job/#terminal-job-conditions)，Pod backoff failure policy、Terminal Job conditions、Termination of Job pods | `b7c0928182a470c6` |
| E05 | [Slurm test37.5 / slurm-24-11-7-1](https://github.com/SchedMD/slurm/blob/slurm-24-11-7-1/testsuite/expect/test37.5)，原文件 L51–69、L139–163、L166–178、L278–301、L443–464、L666–669、L827 等 | `19a74fa204c3ce9a` |
| E06 | [Slurm test_102_5.py / 同 tag](https://github.com/SchedMD/slurm/blob/slurm-24-11-7-1/testsuite/python/tests/test_102_5.py#L71-L124)，原文件 L15–23、L71–124；重开第一轮已给出的候选旁证 | `ae908d7c1f66ad9f` |
| E07 | [Operating etcd / Kubernetes v1.32](https://v1-32.docs.kubernetes.io/docs/tasks/administer-cluster/configure-upgrade-etcd/#restoring-an-etcd-cluster)，恢复前停 API server、恢复输入/输出、版本与端点条件 | `19e528c0790d486b` |
| E08 | [Slurm 24.11.7 slurm.conf](https://slurm.schedmd.com/archive/slurm-24.11.7/slurm.conf.html#OPT_HealthCheckProgram)，HealthCheckProgram 与 HealthCheckInterval | `f4151769ed29968c` |
| E09 | [Slurm 24.11.7 sacct](https://slurm.schedmd.com/archive/slurm-24.11.7/sacct.html#OPT_state)，原始 HTML L536–556 的状态筛选、时间窗口与 EligibleTime | `d96f8299e0b778c8` |

E01/E02/E03/E04/E07/E08/E09 与既有取证哈希一致，E06 与第一轮独立取证一致。E05 本轮完整 SHA-256 为 `19a74fa204c3ce9a7eba6e00e9eab6e1f8c7f511f39809083dc6032d52e14c0e`。E02 是版本路径文档而非固定源码 commit；字节一致只证明本次读到同一材料，不能证明 unknown 的目标 etcd/etcdutl patch 支持其所有选项。

未重新检索全部 Slurm expect 用例，也不独立背书“593 个”的数量或整个 testsuite 不存在某类用例。没有运行任何 Expect/Python 上游测试、集群查询、daemon 停起、故障注入、快照或恢复命令。

## 3. 上轮 OPEN 项逐项判定

部分修正不另增编号；原实质关闭条件未完成时，保留原编号 OPEN。下列判定既核对正文，也核对 A 的本轮补充及当前 R，不能由作者的“已补”摘要代替实际落点。

| 编号 / 级别 | 本轮位置与作者补充 | 独立复核依据与剩余条件 | 判定 |
|---|---|---|---|
| B24-T10-C01 / P2 | P L70；A L175；R L5877–5890 | 未设 RV 与 RV=`"0"` 已分别改成 Most Recent、Any，明确无 continue token 的范围；补齐请求参数、响应版本、请求时间、API server 身份。E01 的 get/list 表及一致读说明支持这些修正，A/R 不再与正文的映射相冲突。本项关闭不表示已取得现场请求证据。 | **CLOSED** |
| B24-T10-C02 / P2 | P L72、L93、L112–113、L136、L157；A L176 | 已增加对象级观察和异常停止，将 L157 改成风险说明，也保留同快照、新逻辑集群及隔离条件。但 L72 仍写 REVISION 回退程度“决定恢复后要重放/丢弃的变更量”；L113 的对象 RV 比对不能算出回退幅度，也不能确认未观察到动作的 informer 已刷新，缺证/无法判断时尚无明确缓存项不通过规则。L93 仍有 patch 未核验却规定跳过校验的处方性措辞，端点/证书更新亦未区分实际布局。E01/E02/E07 支持风险与条件，不能支持上述确定性或充分性判断。详见 §3.1。 | **OPEN** |
| B24-T10-C03 / P2 | P L124；A L177；节点摘除流程 L190–208 | 已把 Pod UID、owner Job UID、运行时 containerID、节点、采集时间与应用 attempt 连成映射，并**明确复用身份账本**；所复用规则要求同期 API/CRI 关联、不能唯一连接则 unknown、重启后重新采集。容器级计数及可能归零与 E03 一致，不再以策略上限替代执行身份。满足第一轮允许的明确复用途径，无需重复抄写账本。 | **CLOSED** |
| B24-T10-C04 / P2 | P L125；A L177；作业生命周期 L54、L72 | `Complete`/`Failed`、Pod phase、成功/失败统计及限额/实际重试已经修正；本轮也写出两个门控名。但是只说“终态时序受影响”，没有落实所选 v1.32 门控下“所有 Pod 终止后才添加终态”的顺序，unknown 的限制对象却写成“Pod 替换行为”。行末链接仍附在 TTL/GC 清理语句，未明确复用生命周期的终态时序与独立核验规则。E04 及本库生命周期 L54 已有精确依据，尚须接入本恢复判定，详见 §3.2。 | **OPEN** |
| B24-T10-C06 / P2 | P L131–136；A L178；R L5430–5440 | E05 确实是联邦重排用例，有记账状态和重启计数断言；正文明确说非控制器切换专项，这个边界是正确的。但联邦主动重排不是控制面故障/恢复测试；K8s/etcd 仍只有程序性灾备指南与未逐用例核对故障触发的 Job 单测文件。两侧均未补足原关闭条件所需的相关故障测试/案例。E06 的故障候选仍未被作者纳入交付，不能用审阅者旁证代交。详见 §3.3。 | **OPEN** |
| B24-T10-R01 / P2 | P L93；A L179；R L6099 | 正文已正确区分快照文件、离线 `member/snap/db` 单文件及恢复输出目录，并补上 WAL 缺口；A 本轮补充与之相符，E02/E07 支持该工件区分。但**当前 registry notes 仍写“直接拷贝的数据目录须 --skip-hash-check”**，并未同步改正。原关闭条件要求 P/R/A 一致，故仅关闭正文缺陷不足以关闭整项。工具版本门槛另归 C02，不重复计数。 | **OPEN** |
| B24-T10-R02 / P3 | P L20、L124；A L180；R L6111–6121 | 固定 v1.32.0 的 core/v1/types.go 已有独立登记，P 的 source_refs 已加入相同 ID，A 说明补登记。URL、原文件字段及完整哈希与 E03 一致；许可仍为 unknown，未把网站文档许可套给源码。本项来源登记与依赖缺口已补齐。 | **CLOSED** |

### 3.1 C02：哪些已修正，哪些仍不足

本轮不再否认作者已把 P L157 的“会触发重放”改成风险，也接受 P L113 把 revision bump 留为非通用处方的方向。**没有现场 patch 或真实缓存指标，本身不是要求作者本轮执行恢复的理由**；可以选择固定参考工具版本，或清楚把未核实选项留为风险说明和执行前阻断项。仍需补齐的是：

1. **消除剩余确定性表述。** P L72 的“决定……重放/丢弃的变更量”仍把存储 revision 差异等同于控制器/应用重放量。E02 的 Revision Difference 说明缓存可能不能正确刷新，并不保证会重放多少业务副作用；即使得到 etcd 全局 revision 差值，也不能直接把它当作某个 Job 的重放数。
2. **把验证记录从对象抽查接到缓存结论。** P L113 要比对恢复前后对象清单及 RV 以“确认回退幅度”，但 E01 明确 RV 是不透明值；它既不是可相减的进度，也不能仅凭同一对象的最后修改版本证明该次集合读取或 informer 缓存的新鲜度。正文 L68/L113 自己也禁止 RV 大小比较。应分开记录快照身份及全局 revision 证据、恢复后的读取语义/时间/实例、被核验控制器或客户端的重建证据、观察窗口内的预期副作用。抽查没有异常可作旁证，不能自动关闭未覆盖缓存；缺证或无法解释时明确维持 unknown 并阻止完成判定。这里要求的是可填写的方法和判据，不要求伪造执行结果。
3. **使 unknown 真正约束使用。** P L93 一面说所选 patch 的选项支持 unknown，一面仍写恢复“须”跳过哈希检查。需要选择可核对的工具参考版本，或把选项改成有前提的资料说明，明确未核实不得据此实施。E07 对 API server 重配采用的是访问 URL 改变时的条件；P L93 的“API server 指向与证书边界随之更新”应按实际布局逐项核对，不能由新逻辑 cluster ID 推出必须轮换证书。无需新增可执行恢复命令。

这些均属于原 C02 的版本、身份、缓存验证及确定性重放关闭条件，不另记 S2 编号。依据为 E01 的 Resource versions/get-list 语义、E02 的 Revision Difference/恢复身份及 E07 的恢复条件。

### 3.2 C04：点出门控名不等于说明终态时序

E04 的 Terminal Job conditions/Termination of Job pods 明确区分早期成功或失败目标、Pod 终止过程以及最终条件。对其 v1.31+ 默认开启相关门控的口径，`Complete`/`Failed` 在所有 Job Pod 终止后添加；较早版本或不同门控不能无条件套用。本库[作业生命周期](../../knowledge/05-cluster-platform/kubernetes-job-lifecycle.md) L54 已有对应说明。

P L125 新增门控名和 unknown 是进步，但“无法判断 Pod 替换行为”并没有补上本项要求的**终态判断**。最小修订可直接明确复用该文终态小节：先记录有效门控，再区分早期目标、终态条件、Pod 实际终止与最终资源释放；门控或进程/资源证据未知时不据条件名宣布恢复完成。无需复制整篇生命周期文档，亦不要求提交真实门控配置。本项不把 C07 已关闭的三类任务矩阵重新判 OPEN。

### 3.3 C06：test37.5 能支持的范围与仍缺的故障材料

E05 的原文件 L51–69 要求 slurmdbd 记账、记账管理员及三集群联邦环境，并要求集群已启动；L166–178 的触发是主动 requeue。L139–163 用 sacct 查询并检查匹配状态记录的数量下限；L278–301 检查输出中的重启计数。L461、L666–669、L827 等调用点确实分别覆盖 A/R/P 所说的重排相关记账状态与计数。**因此本轮不把作者对该用例范围的诚实限定另记为错误。**

但这些断言并未把联邦重排变成 API/etcd 恢复、Slurm controller/DBD 故障恢复样本。P L133 自承 K8s Job 单测未逐用例核对控制面故障，程序性 etcd 指南也不是测试或案例。C06 的原条件是固定关键分支的相关故障材料、实际触发、观察/断言和限制，不是给邻近测试加一个准确文件名即可通过。

第一轮提供的 E06 本轮再次核对：L77–109 包含 DBD 停服、建立运行/等待作业、controller 停起及其与数据库 QOS 的状态差异；L111–124 检查旧运行作业、旧等待作业和新提交的不同结果。它是**可供作者选择的故障旁证**，不是本报告替作者登记或补写的已交付材料，也不是 HA、快照灾备或应用持续进展证明。关闭 C06 不强制用例名称必须叫“主备切换”；可以选确有故障触发且边界匹配的材料，但必须在正文/取证中完成交付，K8s/etcd 一侧仍需相应补证。没有取到材料的分支继续 OPEN，不能用 unknown 替代必交验收。

## 4. 已 CLOSED 项的关联回归抽查

本节不是重新全量初审，只检查本轮身份、Job 统计、测试及来源改动可能影响的已关闭事项。

| 编号 / 级别 | 抽查依据与结果 | 当前状态 |
|---|---|---|
| B24-T10-C05 / P2 | P L128 的 slurmd 首次启动、注册前触发与周期触发未被改回错误顺序；仍要求缺执行结果保持 unknown，不以注册成功/NoResp 消失替代健康。E08 与已明确复用的节点准入门槛支持此口径。 | **CLOSED（维持）** |
| B24-T10-C07 / P2 | P L142–146 仍区分旧完成、旧未完成、受控新任务，明确复用三层准入门槛及应用观察规则；所链节点文档 L188/L203–208 保留普通生产隔离、未知/失败不放行，Checkpoint 文档保留持续窗口。未发现由本轮修订引起的矩阵回归；Job 终态缺项仍归 C04。 | **CLOSED（维持）** |
| B24-T10-C08 / P2 | P L81/L129/L159 仍承认活动作业记录，保留 EligibleTime/查询窗口、记账缺失或延迟及调度状态分离。E09 支持该范围；test37.5 的记账断言也未被夸大成数据库恢复等于调度恢复。 | **CLOSED（维持）** |
| B24-T10-C09 / P3 | P L19/L26 的两个测试来源 ID 保留，本轮 core/v1 新来源另见 R02。22 个 source_refs 均可解析；测试证据是否足够仍归 C06，etcd notes 的内容错误仍归 R01，不混作依赖 ID 遗漏。 | **CLOSED（维持）** |
| B24-T10-C10 / P3 | N L59/L77/L82 仍为草稿已交付、审阅进行中及主题待批次闭环，导航哈希与第一轮记录相同，未改成审阅通过。 | **CLOSED（维持）** |

## 5. 新发现

**无新增独立发现，B24-T10-S2-xx 共 0 项。** 本轮新增对象级缓存说明的不充分之处落在 C02 原关闭条件内；registry 的工件口径仍是 R01 未改完；test37.5 的相关性不足仍是 C06。均保留旧编号，避免重复统计或把部分修正伪装成整个问题关闭。

## 6. 任务验收重核

对照 T05-10 原四项 acceptance；“满足”只针对文档交付，不表示真实环境验证通过。

| 原验收条目 | 本轮交付、剩余缺口与依据 | 判定 |
|---|---|---|
| 1. 只读证据入口、身份/时间戳/对象版本、leader/quorum/cache/状态存储责任；资源视图正常不证明设备和应用正常 | P L60–84 有分层入口，C01 的请求语义已修正，C03 的执行身份已补齐；“资源视图不证明应用正常”保留。但 P L72/L113 对 revision 差异与缓存验证结论仍不成立，见 C02、E01/E02。 | **部分满足，未通过** |
| 2. K8s API/etcd/控制器与 Slurm slurmctld/slurmd/slurmdbd 按官方前提分支；调度与记账状态不混同 | P L88–105 保留六类分支，C08 的记账职责修正未回归；etcd 新身份与同快照已写出。但所选工具/端点证书条件仍未形成一致的执行前门槛，C02 未闭环。未因本轮未重开其余已核 Slurm 页面而宣称完成新的全量验证。 | **部分满足，未通过** |
| 3. 备份/恢复/重建的前提、版本/集群身份、回放/重复调度风险及停止门槛，先保护证据与恢复点 | P L93、L107–116 已补工件区分、WAL 缺口与对象异常停止，证据保护/双主边界保留。但 C02 的确定性表述、缓存验证及版本适用性仍有缺口；R L6099 仍把输入单文件写成目录，R01 未同步。 | **部分满足，未通过** |
| 4. 重复/过期分配、未完成/已完成、attempt/Checkpoint、资源清理、健康/准入、新旧任务正确性及进展；官方故障测试/案例与未执行演练方案 | C03 已关闭，C05/C07 的健康与三类矩阵维持关闭，P L136 明确演练未执行。但 C04 的门控下终态时序未接入恢复判断，C06 的官方相关故障材料仍未交付；test37.5 仅可支撑限定的重排核对，不能补足该故障材料验收。 | **部分满足，未通过** |

未以来源登记存在、HTTP 200、模型审阅或构建成功替代上述技术验收，也未回填 T05-10 或主题状态为完成。

## 7. 范围保护与结构验证

- P 仍为 `draft / source_checked / platforms: [generic]`，环境档案为空；不将 generic 当作 GPU/NPU 配套证明。没有新增真实执行记录、事故史、支持矩阵或许可结论。
- 实际只读取本地材料与精确上游证据。没有执行正文中的 kubectl、etcdctl/etcdutl、scontrol、sacct 或测试用例中的停服/配置动作。
- 新增报告后在原工作区执行 `PYTHONDONTWRITEBYTECODE=1 make check`：`PASS: 103 content entries; 493 sources.`；另核对正文 22 个 source_refs，未解析 ID 为 0。
- 将工作区连同既有 `build/` 复制到仓库外临时副本，排除 `.git`、`.venv` 和字节码缓存，使用原虚拟环境解释器执行 `make build`：同为 `PASS: 103 content entries; 493 sources.`，成功生成副本的 `build/catalog.json` 与 `build/catalog.md`，未改写原工作区构建产物。
- 输入哈希与复核前清单复验通过；清单中 488 个既有文件均逐字节不变，Git 工作区状态相对复核前仅新增本报告。原有未提交修改及文件均保留。
- 未修改 `src/kb/`，不新增或运行软件测试；本轮验证不建立技术正确性或硬件恢复保证。

## 8. 结论与下一轮复核入口

**暂不通过。** 本轮待复核 7 项中 **CLOSED 3 / OPEN 4**；计入维持关闭的 5 项，累计 **CLOSED 8 / OPEN 4**。无新 OPEN P1/P2，但 C02、C04、C06、R01 四项 P2 尚未关闭。

下一轮定向复核应只围绕这四项及关联回归：C02 同步核对快照/revision/客户端缓存/版本条件与缺证停止门槛；C04 把已存在的准确终态时序接入恢复判断；C06 交付边界匹配的官方故障测试或案例，而非邻近重排用例；R01 同步改正 registry 的工件类型表述。只有全部遗留 OPEN 项 CLOSED 且无新 OPEN P1/P2，才能给出本任务文档审阅“通过”；即使通过，也不代表已在真实集群完成灾备、资源回收或应用恢复验证。
