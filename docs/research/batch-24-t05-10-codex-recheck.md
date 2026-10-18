# Batch 24 / T05-10 Codex 定向复核报告

## 1. 复核信息与结论

- 日期：2026-10-18（Asia/Shanghai）。范围仅为 T05-10，不评价 Batch 24 其他任务或 05.2/05.3/05.7 主题整体完成情况。
- 执行者：本会话 Codex，审阅角色独立于作者；未派发子代理、外部模型或其他审阅 CLI。上下文没有可独立核验的实际底层模型名称及推理档位，记为 **unknown**，不据约定或报告文件名冒称已确认指定模型的运行元数据。
- 初审 C01–C10：**CLOSED 5 项、OPEN 5 项**；仍 OPEN 的 C01、C02、C03、C04、C06 均为 P2。
- 本轮新发现：**OPEN 2 项，P2 1 项、P3 1 项**，编号 B24-T10-R01、R02。合计开放 **P1 0、P2 6、P3 1**。
- 结论：**暂不通过**。既不满足“全部初审发现 CLOSED”，也不满足“无新 OPEN P1/P2”。本结论不要求本轮实际实施灾备演练，更不将未执行演练包装成已验证恢复能力。
- 本轮仅新增本报告；不修改正文、取证记录、registry、导航、任务状态或原工作区生成物。

## 2. 输入、方法与证据范围

### 2.1 本地输入

先读 `README.md`、[编写指南](../authoring-guide.md)、[内容归属](../../content-outline.md)，再逐项重读[初审报告](batch-24-t05-10-codex-review.md) L83–94 的编号、原位置和建议关闭条件。以下位置使用本轮修订快照的原文件行号：

| 简称 | 对象与重点 |
|---|---|
| P（正文） | [control-plane-recovery.md](../../knowledge/05-cluster-platform/control-plane-recovery.md)，全文 L1–163 |
| A（取证） | [batch-24-t05-10-sources.md](batch-24-t05-10-sources.md)，尤其 L163–171“修订轮补充取证”；同时检查此前口径是否仍与正文冲突 |
| R（登记） | [registry.yaml](../../sources/registry.yaml)，正文全部 21 个 source_refs，重点为 L5369–5407、L5408–5440、L5877–5890、L6089–6099 |
| N（导航） | [05 章入口](../../knowledge/05-cluster-platform/index.md)，尤其 L59、L77、L82、L114 |
| 任务 | [full-coverage-backlog.yaml](../../plans/full-coverage-backlog.yaml) L5785–5831，目标、四项 acceptance、source_discovery 与边界 |
| 复用门槛 | [节点摘除流程](../../knowledge/05-cluster-platform/node-drain-resource-reclamation.md) L168–208；[作业生命周期](../../knowledge/05-cluster-platform/kubernetes-job-lifecycle.md) L48–72；[Checkpoint 一致性](../../knowledge/06-training/checkpoint-state-consistency.md) L126–142 |

输入 SHA-256：

| 文件 | SHA-256 |
|---|---|
| 初审报告 | `9a8cb289fc51c9b71a2243c6587e37a151cda3061f6f07b81c6224f2adb32b5e` |
| 修订正文 | `a9ec46e220eb623c105e24a06dec6d8a054337b16c3e201cba975094a62602c7` |
| 作者取证记录 | `1cd1e45b02307d8c159cd047781d785874aafd3c198654d2d520d0961fdc9598` |
| 05 章导航 | `3d28506567fe39bec4e0e54650cdd9aea6a1a55c741ae3dd16246434b7f970b3` |
| 来源登记 | `cfb95b9746f8405bf2c9f8d0101090fb9086a5a663c31d1d261693d3d700e59a` |

初审记录的旧正文哈希与本轮不同；没有将初审行号直接套到修订正文。未取得旧正文完整字节快照，因此新编号表示本轮首次记录的问题，不额外声称已经完成新旧正文的逐字回归归因。

### 2.2 独立重开

仅实施只读 HTTP GET 与本地文本核对：取得 **14 个精确文档/源码 URL 和 1 个固定 tag 源码包，均 HTTP 200**。12 份有初审或作者完整 SHA-256 可比的核心材料均一致；另两份为 Job 单测文件及本轮找到的 Slurm 候选测试。原始响应及解包材料仅置于仓库外临时目录，没有镜像到知识正文。

网页工具打开 Slurm `slurm.conf.html` 时返回 `Internal Error`，随后 curl 对**同一归档 URL**返回 200，完整哈希与作者记录一致，因此本轮没有将其记成上游页面不可访问。下表材料均已实读；GitHub 文件以同 tag、同路径的 raw 响应读取，表中 blob 链接用于展示原文件及行号，不以 GitHub 渲染行号替代源码坐标。未重新验证先前记录的 `high_availability.html` 404，也不据旧记录新增“整个上游不存在 HA 资料”的断言。MindCluster/Kueue/Volcano 专属灾备不在本轮补证范围，仍为 unknown。

| 证据 | 精确上游、原始坐标或章节 | SHA-256 前 16 位 |
|---|---|---|
| E01 | [Kubernetes v1.32 API Concepts](https://v1-32.docs.kubernetes.io/docs/reference/using-api/api-concepts/#semantics-for-get-and-list)，原始 HTML L1489–1511，get/list 参数表及 Any/Most Recent 定义 | `ca03957baf69b180` |
| E02 | [etcd v3.5 Disaster recovery](https://etcd.io/docs/v3.5/op-guide/recovery/)，`Snapshotting the keyspace`、`Revision Difference`、`Restoring from snapshot`、`Integrity Checks`、`Restoring with revision bump`；HTML 为长行，按章节定位 | `477f55130af7c597` |
| E03 | [Operating etcd / v1.32](https://v1-32.docs.kubernetes.io/docs/tasks/administer-cluster/configure-upgrade-etcd/#restoring-an-etcd-cluster)，原始 HTML L952–973 | `19e528c0790d486b` |
| E04 | [Kubernetes v1.32.0 types.go](https://github.com/kubernetes/kubernetes/blob/v1.32.0/staging/src/k8s.io/api/core/v1/types.go#L3096-L3114)，原文件 L3096–3100、L3110–3114，容器重启计数及容器身份 | `ecc3289051e4c011` |
| E05 | [Kubernetes v1.32 Jobs](https://v1-32.docs.kubernetes.io/docs/concepts/workloads/controllers/job/)，原始 HTML L958–988、L1219–1239，重试分支、终态与特性门控 | `b7c0928182a470c6` |
| E06 | [Slurm 24.11.7 slurm.conf](https://slurm.schedmd.com/archive/slurm-24.11.7/slurm.conf.html#OPT_HealthCheckProgram)，原始 HTML L1379–1395；并读 HealthCheckInterval、StateSaveLocation、RELOCATING CONTROLLERS | `f4151769ed29968c` |
| E07 | [Slurm 24.11.7 sacct](https://slurm.schedmd.com/archive/slurm-24.11.7/sacct.html#OPT_state)，原始 HTML L536–556，状态筛选、时间窗口及 EligibleTime | `d96f8299e0b778c8` |
| E08 | [Job 控制器单测 v1.32.0](https://github.com/kubernetes/kubernetes/blob/v1.32.0/pkg/controller/job/job_controller_test.go)，原文件 L6993、L7041、L7401 等重试测试入口 | `b78d06e36bc9562a` |
| E09 | [Slurm test_102_5.py / slurm-24-11-7-1](https://github.com/SchedMD/slurm/blob/slurm-24-11-7-1/testsuite/python/tests/test_102_5.py#L71-L124)，原文件 L15–23、L71–124；源码包与独立 raw 文件逐字节一致 | `ae908d7c1f66ad9f` |
| E10 | [Slurm quickstart_admin 归档](https://slurm.schedmd.com/archive/slurm-24.11.7/quickstart_admin.html)，Controller Node / High Availability | `d7e9c31bac0fe920` |
| E11 | [Slurm slurmdbd.conf 归档](https://slurm.schedmd.com/archive/slurm-24.11.7/slurmdbd.conf.html)，DbdBackupHost / ArchiveJobs / PurgeJobAfter | `6d2529a81316317d` |
| E12 | [Slurm slurmdbd 归档](https://slurm.schedmd.com/archive/slurm-24.11.7/slurmdbd.html)，DESCRIPTION / OPTIONS | `5a81ba6e817a1a83` |
| E13 | [Slurm slurmctld 归档](https://slurm.schedmd.com/archive/slurm-24.11.7/slurmctld.html)，原始 HTML L121–172 | `67e677b6d0dd57a0` |
| E14 | [Slurm troubleshoot 归档](https://slurm.schedmd.com/archive/slurm-24.11.7/troubleshoot.html)，原始 HTML L131–162、L297–306 | `78f519e4e98c869e` |
| E15 | [Slurm 固定 tag 源码包](https://codeload.github.com/SchedMD/slurm/tar.gz/refs/tags/slurm-24-11-7-1)，只解包并检索 testsuite，不执行任何测试 | `f0912d85a9a9b417` |

E02 完整哈希为 `477f55130af7c597fcd094c206600f7a1860377b84311ade6c3db78aa7418739`，与新增登记 R L6094 相同。这证明本轮读到同一份文档字节，**不证明其所有选项都适用于一个尚未选定的 etcd/etcdutl patch**。固定 tag 证据也不等于本库已运行相应用例。

## 3. 初审发现逐项判定

“已修正部分”不会另增一个发现编号；只要同一发现的实质关闭条件仍未满足，即保留原编号 OPEN。允许明确复用已有章节，但不把一个未说明所复用规则的泛链接自动当成恢复步骤已经落实该规则。

| 初审编号 / 级别 | 初审位置与关闭条件要点 | 修订后位置、证据与判定依据 | 判定 |
|---|---|---|---|
| B24-T10-C01 / P2 | 原 L66；分清 Any/Most Recent 的请求条件与保证，保留请求参数、时间、API server 身份，消除正文与取证冲突 | P L69 虽分出两类，却写 **Any“未指定 resourceVersion 的多数场景”**。E01 的 get 表及无 continue token 的通常 list 明确是：未设置 RV 对应 Most Recent，RV=`"0"` 才对应 Any。A L36、R L5890 仍保留“未设 RV 的 list 需一致读”的正确口径，与 P L69 相冲突。新增响应版本/实例身份记录值得保留，但未纠正请求条件，也未明确本行的请求时间记录。 | **OPEN** |
| B24-T10-C02 / P2 | 原 L68、L89、L108–109、L129(a)、L140；限定恢复版本与身份，补 cache 风险、验证/停止门槛，撤销确定性重放结论 | P L92 已加入新逻辑集群、同一快照与隔离条件；L112 已声明 informer 风险并把部分表述降为需核验风险，A L167/R L6089–6099 登记 E02，方向正确。但工具 patch 仍 unknown，L135 只要求“验证 informer 重建”，没有可判断缓存重建成功/失败/未知的证据与停止门槛；P L71 及 L156 仍把回退与重放直接挂钩，L156 仍写“会触发控制器重放”。E02 的 Revision Difference 并不保证正确重放；E03 的停服/重启建议也不能替代验证。 | **OPEN** |
| B24-T10-C03 / P2 | 原 L120；修正容器级 restartCount，并连接 Pod/owner UID、容器身份、节点、时间及应用 attempt，保留缺失证据 unknown | P L123 已按 E04 改为容器级计数，写明可能归零、GC 及不能跨 Pod 计数，原字段错误已修正。但跨恢复身份核对只明确 Pod UID/owner Job UID、节点与采集时间，没有把**运行时容器 ID 与应用 attempt**接到该映射。P L125 的 `max-restarts` 是策略上限，不是某次执行身份；L142 的 attempt 基线也没有与容器连接。P L145 明确复用的是节点文档“三层门槛”，并未明确复用其 L190–201 的身份账本。不能由同一组对象 UID 推定同一次容器/应用执行。 | **OPEN** |
| B24-T10-C04 / P2 | 原 L121；纠正 Job condition/Pod phase/统计/配置限额，按 restartPolicy 计数并说明 v1.32 门控下终态时序 | P L124 已改为 `Complete`/`Failed`，正确区分 `Succeeded` 的 Pod 用语、`spec.backoffLimit` 限额与两种实际重试口径；这些修正与 E05 相符。但本恢复核验仍未接入 Job 成功/失败统计及**JobManagedBy/JobPodReplacementPolicy 有效门控、Job 终态与所有 Pod 终止的时序**。所链生命周期 L54/L72 确有正确说明，P L124 只以 TTL/GC 清理名义引用，未指定恢复时采用的门控前提或未知时停止规则；不能仅据 condition 名已改正确就关闭全部条件。 | **OPEN** |
| B24-T10-C05 / P2 | 原 L124；纠正注册前/周期两类触发，不以注册成功替代健康验证 | P L127 已改为 slurmd 首次启动、注册前执行，另列 HealthCheckInterval 周期触发及默认禁用，符合 E06；明确缺执行结果证据则 unknown，注册成功/NoResp 清除不算健康通过。P L145 复用节点准入门槛，相关身份、观察窗口与证据缺失时隔离规则见节点文档 L188–208。本轮仅接受方法与时序修正，**没有把尚不存在的健康执行记录认定为通过**。A L171 的补证与正文一致。 | **CLOSED** |
| B24-T10-C06 / P2 | 原 L127、A L60；交付真正相关的官方故障测试/案例，给固定文件/版本、触发、观察/断言和限制 | P L130–133/A L169–170 仍未交付合格材料：etcd 恢复指南是程序性资料；E08 的普通 Job 单测只做文件级定位；Slurm 仍以 expect 目录负检索及 unknown 代替实际用例。三者都不能满足原关闭条件。E09 是本轮独立找到的 **DBD 停服＋controller 重启＋新旧作业断言候选**，但作者尚未纳入正文与登记，也不是 HA 切换或 etcd 灾备测试，不能由审阅者补查代替作者完成交付。 | **OPEN** |
| B24-T10-C07 / P2 | 原 L114–135；给旧完成/旧未完成/受控新任务验收矩阵，并接入授权、生产隔离、持续观察与失败/未知不放行 | P L137–145 已新增三类矩阵：L141 旧完成不得误重跑并对照工件/资源；L142 旧未完成按预声明策略续跑/重排/取消，链接 Checkpoint 一致性；L143 新身份、预期输入/输出、资源释放及通过/失败/无法判断三态。L145 **明确复用“三层门槛”**，节点文档 L184–188/L203–208 要求生产持续阻断、先审定观察窗口与基线、缺证/失败不放行；Checkpoint 文档 L130–142 提供单步和持续窗口区分。接受这种明确复用，不要求复制方法或伪造站点阈值。非训练负载不套 loss/Checkpoint。上述完成语义还需服从 E05；C04 的字段/时序缺口独立保留，不重复计作 C07。 | **CLOSED** |
| B24-T10-C08 / P2 | 原 L77、L142；撤销“记账库只含完成历史”，区分活动/完成记录与调度状态、恢复窗口和缺证 | P L80/L128/L158 已承认活动记录，注明 PENDING 的 EligibleTime 限制，分别核对活动与完成数据、恢复窗口内缺失/延迟；不再把数据库当作调度器实时分配真相，且保留数据库/StateSaveLocation 不能互替。E07 及 E11/E12 支持该职责边界；A L168 与 R L5408–5418 的 sacct 覆盖范围可追踪。查询时间窗口与实际记录仍需依所链手册和节点观察记录采集，不把“可查询”升级为记账完整性保证。 | **CLOSED** |
| B24-T10-C09 / P3 | 原 front matter 与 L127；使最终测试引用与 source_refs 一致 | P L19、L25 已补入两个测试 ID，L20 补入 etcd 新来源；L132–133 仍使用相应测试材料，未把其升级为已执行或已覆盖灾备。21 个 source_refs 均能解析。C06 的证据充分性仍 OPEN，但“两个既用测试依赖漏列”本身已修正。新增字段源码的另一项登记缺口见 R02，不把 C09 扩大为所有未来引用的兜底项。 | **CLOSED** |
| B24-T10-C10 / P3 | 原 N L77；区分草稿交付、审阅及主题验收状态 | N L59/L77/L82 已统一为 T05-10 草稿已交付、审阅中，05.2 验收待批次闭环；L114 不再称本文未交付。没有改成审阅通过，也未据报告回填任务 done。此项是本地导航一致性核对，不依赖上游技术机制。 | **CLOSED** |

### 3.1 仍 OPEN 项的最小补齐范围

1. **C01：** 按 E01 修正请求参数映射，明确 RV=`"0"` 与未设置 RV 的差别，保留适用的 list 分页例外；将请求时间、参数、响应版本和 API server 身份一起记录，并同步正文、A、R 的口径。
2. **C02：** 选择可核对的 etcd/etcdutl 参考 patch，或明确将恢复选项完全留在非处方性风险说明；不能把 unknown 当成该版本方案已完成核验。把快照身份、恢复成员、端点/证书条件、客户端缓存重建及失败/未知停止条件连成可填写的检查记录。同步撤销 L71/L156 的确定性重放表述。是否需要更换端点或证书必须依具体恢复布局判断，不因新逻辑 cluster ID 就泛化为一律轮换证书。
3. **C03：** 在 P 的恢复核对中明确复用节点文档“身份账本”，或直接加入 Pod UID、owner Job UID、容器 ID、应用 attempt、节点及采集时间的关联；不能唯一连接、计数归零或对象 GC 时记 unknown，不推断无重复执行。
4. **C04：** 接入 `status.succeeded`/`status.failed` 等统计与有效门控记录，说明所选 v1.32 门控前提下的终态时序、Pod 实际终止和最终资源释放分别取证；可以明确复用生命周期相应小节，无需复制全文。有效门控或进程/资源证据未知时不作完成判断。
5. **C06：** 为关键分支选择实际相关的官方故障测试/案例，记录固定路径、触发、断言与不覆盖范围，并补来源依赖。不能因暂未找到而将必交验收关闭。

### 3.2 C06 的候选旁证及搜索边界

E15 解包后仅做文本检索，未运行 `pytest`、Expect 或 Slurm 命令。在同一 `slurm-24-11-7-1` 的 **python** 测试目录找到 E09 的 `test_qos_removal_single`：

- L15–23 要求自动配置、slurmdbd 记账与关联/QOS enforcement 等测试环境。
- L77–109 在 DBD 停服时建立 RUNNING/PENDING 作业，停 controller、恢复 DBD 并删除 QOS，然后重启 controller。
- L111–124 分别断言原运行作业继续运行、原等待作业保持 PENDING 且为 InvalidQOS、新提交使用已删 QOS 被拒绝。

这是一个与状态差异及新旧作业核对有关的**具体官方测试样本**，不是主备接管测试，更不证明快照灾备、应用正确性或持续业务进展已通过。它说明只检索 expect 子树不足以作整个 testsuite 的不存在性结论。没有复用作者“593 个用例”作为已独立核验的覆盖统计，也没有把本轮候选直接计入作者的已交付测试材料。

## 4. 本轮新发现

### B24-T10-R01 — P2 — 恢复输入的快照文件与整个数据目录混同

- **状态：OPEN。**
- **位置：** P L92 新补的完整性分支：“直接拷贝的数据目录没有哈希，须 `--skip-hash-check`”；R L6099 重复该口径。A L167 是该补证的来源记录。
- **证据：** E02 的 Snapshotting/Restoring/Integrity Checks 区分从数据目录提取的 **`member/snap/db` 单文件**、快照文件和恢复生成的数据目录；并提示直接取该 db 文件可能遗漏只在 WAL 中的更新。E03 亦区分输入 `snapshot.db` 与 `--data-dir` 指定的输出目录。
- **问题与影响：** 正文把“从数据目录复制出的数据库快照文件”缩成“复制的数据目录”，随后直接附加跳过哈希检查要求，误导恢复工件选择；该新分支还缺少 WAL 恢复点差距说明。`--skip-hash-check` 不能修正输入工件类型，也不能证明数据完整。标注 patch unknown 不能使这条通用工件描述变正确。
- **关闭条件：** 同步 P/R/A，区分快照输入、离线提取的 db 文件和恢复输出目录，记录 WAL/恢复点限制；只在所选工具版本及工件类型有依据时讨论跳过快照哈希检查，不将其写成整目录恢复或损坏快照的通用补救。无需增加或执行恢复命令。
- **与 C02 的关系：** C02 保留的是恢复版本、缓存及确定性重放缺口；本项单列修订补证中的工件类型错误，不重复给缓存问题编号。

### B24-T10-R02 — P3 — 新用的 ContainerStatus 源码没有进入来源登记与依赖清单

- **状态：OPEN。**
- **位置：** P L123 直接引用 v1.32.0 `staging/src/k8s.io/api/core/v1/types.go`；A L171 引用初审 E08；P L8–29/R 相应条目。
- **证据：** 本轮确实重开 E04，语义及哈希与初审相同。但登记全文没有该原文件或覆盖该文件的来源范围；`src.kubernetes.job-lifecycle-v1-32`（R L5369–5382）覆盖网站 Job/Pod/清理文档及 API 文档，`src.kubernetes.job-controller-tests-v1.32.0`（R L5395–5407）覆盖 Job 控制器/测试等路径，都未登记该 core/v1 源码。报告中的 E08/E04 是审阅证据编号，不是 registry ID。
- **影响：** 字段修订的核心证据只存在于直链和审阅记录，结构检查只能确认已列 ID 存在，不能发现这个遗漏；网站文档的许可范围也不能不加核对地套到该源码文件。
- **关闭条件：** 新增该固定 tag 文件的来源条目，或显式扩展一个合适既有登记的取证/许可范围，并使 P 的 source_refs 与 A 的原文件坐标一致；保留未核实的许可状态。本轮只记录问题，由作者在后续修订正文与登记，审阅者不代改。

## 5. 验收条目重新核对

对照任务原四项 acceptance，而非用“新增了若干表格”替代任务验收：

| 验收条目 | 修订后证据与剩余差距 | 结果 |
|---|---|---|
| 1. 只读证据、身份/时间戳/对象版本、leader/quorum/cache/状态存储责任；资源正常不等于设备/应用正常 | P L59–83 保留分层入口和边界，L69 的请求语义仍错误且与 A/R 冲突；C01 未关 | **部分满足，未通过** |
| 2. K8s API/etcd/控制器与 Slurm 三 daemon 按官方前提分支；调度/记账不能混同 | P L85–104 保留六类分支，C08 的职责修正通过；etcd 的版本/缓存方案及新增恢复输入错误分别见 C02/R01 | **部分满足，未通过** |
| 3. 备份/恢复/重建前提、版本/集群身份、回放/重复调度和停止门槛，先保护证据与恢复点 | P L92/L106–115/L149 已加入同快照、隔离及保护顺序；缺可判定的缓存重建门槛，L156 仍确定性重放，R01 的输入工件表述错误 | **部分满足，未通过** |
| 4. 重复/过期、完成/未完成、attempt/Checkpoint、资源、健康/准入及新旧任务正确性/进展；官方故障测试/案例和未执行演练 | P L123–145 的健康时序、三类验收矩阵及明确复用的生产隔离门槛可接受，演练仍如实标未执行；容器/应用执行身份映射、Job 门控/统计时序和官方故障用例仍缺，见 C03/C04/C06 | **部分满足，未通过** |

保留 unknown、draft 和“未执行”是正确的证据边界，但不将必交测试或尚未落实的恢复判断门槛自动转为已覆盖。仍为 `planned` 的任务状态也不是本轮判定的替代依据。

## 6. 元数据、边界与交付约束

- 稳定 ID 仍为 `cluster-platform.control-plane-recovery`，主归属 05、`type: procedure`、`status: draft`、`platforms: [generic]` 与 `verification.status: source_checked` 保持；没有把跨平台概念写成 GPU/NPU 整栈兼容结论。
- 全部 21 个 source_refs 均可解析；5 个 related_ids 与 2 个 verification 引用由结构检查核对。ID 可解析不代表引用齐全，R02 即为这种结构检查不能自动发现的遗漏。
- N 的草稿/审阅状态已修正；未修改任务 done、主题覆盖状态、许可结论或真实环境验证状态。
- 本轮没有执行集群查询、快照、恢复、daemon 生命周期动作、故障注入或设备验证；只读取上游测试代码，不运行其停服与配置步骤。未向报告引入本地事故、合成结果、性能数据或未授权操作承诺。

### 6.1 结构检查与隔离构建

- 新增报告后在原工作区运行 `PYTHONDONTWRITEBYTECODE=1 make check`，结果：`PASS: 103 content entries; 491 sources.`
- 为同时遵守“只新增报告”与构建要求，将包含既有 `build/` 的工作区复制到仓库外临时目录，排除 `.git`、`.venv` 和字节码缓存；使用原工作区虚拟环境解释器，在副本执行 `make build`。结果同为 `PASS: 103 content entries; 491 sources.`，并成功生成副本的两份 catalog；未改写原工作区 `build/`。
- 未修改 `src/kb/`，未运行软件测试。上述检查只验证结构、本地链接和生成流程，不能证明技术问题关闭、上游测试通过或真实环境恢复成功。

## 7. 结论与下一轮复核入口

**暂不通过。** 初审 **5 CLOSED / 5 OPEN**；本轮另有 **2 个新 OPEN**。下轮至少重读修订后的 C01/C02/C03/C04/C06 和 R01/R02 对应位置，核对请求语义、恢复版本/缓存门槛、完整执行身份、Job 门控/统计时序、真正相关的故障用例，以及快照工件与来源依赖。已经 CLOSED 的项目若发生关联改动，仍需检查是否回归。

只有全部初审发现 CLOSED 且没有新 OPEN P1/P2，才能给出本任务文档审阅通过结论；即便将来通过，也不等于在真实集群完成灾备或应用恢复验证。
