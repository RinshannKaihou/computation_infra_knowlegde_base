# Batch 24 / T05-10 Codex 技术审阅报告

## 1. 审阅信息与结论摘要

- 审阅日期：2026-10-18（Asia/Shanghai）。
- 任务：T05-10「控制面故障、平台恢复与账本核对」，新建 `procedure`。
- 执行角色：本会话 Codex，独立于正文编写者；本轮未调用子代理、其他模型或外部审阅 CLI。运行上下文未提供可独立核验的底层模型名称及推理档位，因此记为 **unknown**，不据文件名或约定冒称已经核验 `gpt-6.1-sol / xhigh` 的实际运行元数据。
- 结论：**暂不通过**。共 **10 项 OPEN 发现：P1 0 项、P2 8 项、P3 2 项**。P2 必须经作者修订及定向复核关闭，不能以结构检查通过或保留 `draft` 替代关闭。
- 本轮仅新增本报告；不修改正文、导航、来源登记、取证记录或任务状态。工作区原有的其他修改不属于本轮审阅交付，也未据此评定 Batch 24 其他任务。

## 2. 范围、方法与限制

### 2.1 本地输入

已读取 `README.md`、[编写指南第 7 节](../authoring-guide.md#7-批次审阅约定)、`content-outline.md` 相关归属规则，以及以下对象：

| 对象 | 本轮范围 |
|---|---|
| [任务定义](../../plans/full-coverage-backlog.yaml) | 原文件 L5785–5831；读取 objective、4 项 acceptance、source_packages（A08/A09/A15/A16/S22/S24）、existing_source_ids、source_discovery、depends_on、context_topic_refs（08.3/08.5）及 targets；不将 planned 当成审阅通过或未创建文件的证明 |
| [正文](../../knowledge/05-cluster-platform/control-plane-recovery.md) | 全文 L1–147，含 front matter、全部表格、恢复前提、核验清单及演练声明 |
| [作者取证记录](batch-24-t05-10-sources.md) | 全文 L1–161，含 curl/SHA-256、逐项定位、unknown 与未执行声明 |
| [来源登记](../../sources/registry.yaml) | 正文 18 个 source_refs 的对应条目，以及正文 L127 引用的两项测试来源；核对 URL、revision、许可边界、notes 与登记 ID |
| [领域导航](../../knowledge/05-cluster-platform/index.md) | front matter 与全文，重点为 L32、L59、L77、L82、L114 |
| 关联内容 | 定向读取 Kubernetes 作业生命周期、Slurm 作业/设备资源、设备状态链、节点摘除与平台升级回退的有关字段、身份及恢复门槛；不对这些已交付文章重新作整篇验收 |

本轮正文输入 SHA-256：`9522e18960fda92439323b595da018280b8c4c0f50480505e43bffa94a32b703`。作者取证记录输入 SHA-256：`d53c1f8ac5e241ccc8e4b47980773100fff3cd73a314a5c7269bef4682e3025b`。以下正文行号均对应这个审阅快照。

### 2.2 独立上游核对

采用只读 HTTP GET：重开正文全部 15 个去重外部链接，并补查登记页、被引页面直接关联的恢复/字段资料及固定 tag 源码。共取回 31 个 URL：30 个 HTTP 200、1 个 HTTP 404。原始响应字节与比对缓存仅放在临时目录，不加入仓库。未对生产集群发起任何查询或变更。

网页阅读工具对部分 SchedMD 归档返回 `Internal Error`，随后用 curl 对同一精确 URL 成功取得 HTTP 200，并与作者记录的 SHA-256 一致；因此没有将网页工具错误误判为上游文档不可访问。作者本轮登记的 11 份 K8s/Slurm 核心文档，完整 SHA-256 **11/11 相同**；下表只缩写显示前 16 位，实际比对使用完整 64 位值。

| 取回对象 | SHA-256 前 16 位 | 与作者完整记录比对 |
|---|---|---|
| K8s Leases | `ec68b97369247821` | 相同 |
| K8s kube-controller-manager reference | `344a05192c36149e` | 相同 |
| K8s API Concepts | `ca03957baf69b180` | 相同 |
| K8s Operating etcd | `19e528c0790d486b` | 相同 |
| K8s Controllers | `a6aecfb049400117` | 相同 |
| Slurm troubleshoot | `78f519e4e98c869e` | 相同 |
| Slurm quickstart_admin | `d7e9c31bac0fe920` | 相同 |
| Slurm slurm.conf | `f4151769ed29968c` | 相同 |
| Slurm slurmdbd.conf | `6d2529a81316317d` | 相同 |
| Slurm slurmctld | `67e677b6d0dd57a0` | 相同 |
| Slurm slurmdbd | `5a81ba6e817a1a83` | 相同 |

**独立重开限制：** `https://slurm.schedmd.com/archive/slurm-24.11.7/high_availability.html` 未能独立重开为文档正文，原因是 **HTTP 404**；归档索引可读取。此结果支持“该归档 URL 不存在”，不表示 Slurm 没有 HA 文档或机制；本轮 HA 判断使用已取回的 quickstart_admin/slurm.conf 等精确页面。MindCluster tag 与既有 commit 的字节等同性未核验，继续保留 unknown。Kueue/Volcano 专属灾备未专项取证，不扩展为平台兼容或恢复能力结论；也未穷尽所有官方资料来证明“绝无此类文档”。

### 2.3 证据索引

下列行号为本轮 curl 取得的**原始文件坐标**，不是网页工具转换后的行号；长 HTML 单行同时给章节或字段定位。新增字段旁证用于审阅，不代表已经替作者更新来源登记。

| 证据 | 精确上游与定位 | 本轮用途 |
|---|---|---|
| E01 | `https://v1-32.docs.kubernetes.io/docs/tasks/administer-cluster/configure-upgrade-etcd/`，原始 L909–923、L952–973，`Restoring an etcd cluster` | 快照与停全部 API server 的恢复前提、组件重启建议、目录和访问地址调整 |
| E02 | `https://v1-32.docs.kubernetes.io/docs/reference/using-api/api-concepts/`，L1015–1019、L1475–1511，`Semantics for get and list` | opaque resourceVersion、watch 历史、Any 与 Most Recent 的读语义 |
| E03 | `https://v1-32.docs.kubernetes.io/docs/concepts/architecture/leases/`，L800–827 | 节点心跳、组件选主、API server 身份 Lease |
| E04 | `https://v1-32.docs.kubernetes.io/docs/reference/command-line-tools-reference/kube-controller-manager/`，Options 表；`--leader-elect` 字节偏移 486752、`--node-monitor-grace-period` 偏移 494561（从 0 开始） | 选主与节点监测默认值；不推定现场值 |
| E05 | `https://v1-32.docs.kubernetes.io/docs/concepts/architecture/controller/`，L812–833、L873–881 | 经 API server 的控制循环与内建控制器宿主、HA 设计边界 |
| E06 | `https://v1-32.docs.kubernetes.io/docs/concepts/architecture/nodes/`，`Node heartbeats`、`Node controller` | 心跳与默认监测/驱逐责任，不将失联直接归因于设备 |
| E07 | `https://v1-32.docs.kubernetes.io/docs/concepts/workloads/controllers/job/`，L958–988、L1217–1239 | 新 Pod 与容器重启区别、失败重试计算、Job 终态 conditions |
| E08 | `https://raw.githubusercontent.com/kubernetes/kubernetes/v1.32.0/staging/src/k8s.io/api/core/v1/types.go`，L3096–3100 的 ContainerStatus.RestartCount；并查 `https://v1-32.docs.kubernetes.io/docs/concepts/workloads/pods/pod-lifecycle/` | 容器重启字段的确切范围与节点重启后可能归零的限制 |
| E09 | `https://slurm.schedmd.com/archive/slurm-24.11.7/quickstart_admin.html`，L527–541、L586–620 | StateSaveLocation、接管/回切、状态未落盘风险 |
| E10 | `https://slurm.schedmd.com/archive/slurm-24.11.7/slurm.conf.html`，L1379–1395、L3169–3193、L4422–4425、L4719–4729、L6788–6820 | HealthCheckProgram 时序、ReturnToService、超时、状态目录、迁移与双主警告 |
| E11 | `https://slurm.schedmd.com/archive/slurm-24.11.7/troubleshoot.html`，L131–162、L297–306 | 主备探测、进程/日志排查及 startclean 的破坏性边界 |
| E12 | `https://slurm.schedmd.com/archive/slurm-24.11.7/slurmctld.html`，L121–172 | -r/-R/-c/-i 的准确恢复范围与失态风险 |
| E13 | `https://slurm.schedmd.com/archive/slurm-24.11.7/slurmdbd.conf.html`，L164–169、L369–377、L698–707、L837–842；`https://slurm.schedmd.com/archive/slurm-24.11.7/slurmdbd.html`，L123–124、L139–150 | DBD 同库前提、归档/purge 及 -u/-R 的非灾备含义 |
| E14 | `https://slurm.schedmd.com/archive/slurm-24.11.7/slurmd.html`，DESCRIPTION/OPTIONS；`https://slurm.schedmd.com/archive/slurm-24.11.7/upgrades.html`，`Reverting an Upgrade`、`Minor Upgrades`、`Create Backups` | 节点 daemon 与版本迁移/备份边界 |
| E15 | `https://v1-32.docs.kubernetes.io/releases/version-skew-policy/`；`https://v1-32.docs.kubernetes.io/docs/tasks/administer-cluster/kubeadm/kubeadm-upgrade/`，支持偏斜与失败恢复章节 | 核对正文复用的升级入口；不将升级资料当成完整灾备身份方案 |
| E16 | `https://docs.pytorch.org/docs/2.6/elastic/train_script.html`，L591–601 | 训练脚本保存/加载 checkpoint 的职责与丢进展边界；不构成恢复实测 |
| E17 | `https://raw.githubusercontent.com/Ascend/mind-cluster/v26.1.1/component/clusterd/README.md`，L3–5；同 tag `component/ascend-operator/README.md` 的组件介绍 | clusterd/AscendJob 职责；两份 README 不证明整栈灾备行为 |
| E18 | `https://github.com/kubernetes/kubernetes/tree/v1.32.0/pkg/controller/job`；`https://github.com/SchedMD/slurm/tree/slurm-24-11-7-1/testsuite`；定向取回前者的 `job_controller_test.go`（v1.32.0） | 确认正文引用的是目录；抽查控制器单测名称，未将目录存在性提升为控制面灾备覆盖 |
| E19 | `https://etcd.io/docs/v3.5/op-guide/recovery/`，原始 HTML L13–14，`Revision Difference`、`Restoring from snapshot`、`Restoring with revision bump` | 从 E01 直接链接补读的 etcd 官方恢复旁证；读旧 revision 的缓存风险及新逻辑集群身份，不强行给未知 patch 版本套命令 |
| E20 | `https://slurm.schedmd.com/archive/slurm-24.11.7/sacct.html`，L536–550 | 记账查询可以涉及 RUNNING/PENDING，不仅是已结束作业 |

补充旁证完整 SHA-256：E07 Job 页为 `b7c0928182a470c6b19d86c8e832377121b838777bbcce08d7e0b3c1807cf0d9`；E08 固定 tag 的 types.go 为 `ecc3289051e4c011c8d15089f820d1a03ba7a5400719a7abda0ce58caf33f842`；E19 为 `477f55130af7c597fcd094c206600f7a1860377b84311ade6c3db78aa7418739`；E20 为 `d96f8299e0b778c8d4cd04a710969f458f118482b122bb99443716ca9ab677f4`。E19 是版本路径文档而非固定 commit 源码；正文若采用其具体恢复选项，还必须核验所选 etcd/etcdutl patch 的实际支持情况。

## 3. 发现表

本表全部为 **OPEN**。P2 是影响技术判断、程序性恢复门槛或必交验收的实质问题；P3 是来源依赖可追踪性或导航一致性问题。位置如未另指文件，均在本次正文。

| 编号 | 优先级 | 位置 | 发现与证据 | 建议关闭条件 |
|---|---|---|---|---|
| B24-T10-C01 | P2 | L66「读一致性」 | 将“HA 分区下读到较旧缓存是预期行为、不必处置”直接接在未指定 resourceVersion 的 list / Most Recent 后，混淆不同一致性契约。E02 原始 L1500–1504 的旧数据风险属于 **Any**；L1504–1509 的 Most Recent 即使由 watch cache 提供，也要求一致性，使用 progress notification 维持与 etcd 的一致。不能把所有缓存读取都解释成可接受的陈旧读。 | 分开列明 Any 与 Most Recent 的请求条件、保证和风险；诊断时保留实际 resourceVersion/resourceVersionMatch、请求时间及 API server 身份。删除对陈旧读一概“不需处置”的结论，重新核对该行与取证/登记 notes 是否一致。 |
| B24-T10-C02 | P2 | L68、L89、L108–109、L129(a)、L140 | 将旧 REVISION 恢复写成控制器“会重新收敛/重放”的确定结果，同时把集群身份前提外包给升级文档，缺少灾备本身的缓存与成员身份约束。E01 要求停全部 API server，并建议重启依赖陈旧数据的组件；E19 明确旧 revision 可能使 informer 缓存不能正确刷新，恢复会改写 etcd member/cluster ID、建立新逻辑集群，所有成员须用同一快照。升级偏斜与 kubeadm 资料不能替代这些灾备条件。本文现有泛化核对表不足以证明缓存已经重建，也没有说明旧/新 etcd 集群如何避免误连。 | 固定目标 etcd/恢复工具版本、快照身份与各成员恢复的一致性、旧集群隔离及 API server 指向/证书边界；补充旧 revision/watch/cache 的专门风险与验证/停止门槛，将自动重放改成需验证的风险/预期。若采用 revision bump/缓存失效方案，先为选定 patch 找精确依据并登记；未核实的选项、拓扑和客户端行为保留 unknown，不新增通用可执行命令。 |
| B24-T10-C03 | P2 | L120，Kubernetes「重复/过期分配」 | 将 `restartCount` 称为“Pod 重建序号”。E08 固定 v1.32.0 源码 L3096–3100 定义的是 **ContainerStatus 的容器重启次数**，并明确节点重启丢状态时可能归零；E07 也区分原 Pod 内重启与新建替代 Pod。它不能作为跨 Pod/跨恢复的 attempt 或新旧执行唯一计数。 | 改为确切字段路径及容器级语义；把 Pod UID、owner Job UID、容器身份、节点、采集时间和应用 attempt 的映射列入核对，区分原 Pod 内重启与替代 Pod。保留计数丢失/对象已 GC 的 unknown，不以计数相同推定执行同一或无重复。 |
| B24-T10-C04 | P2 | L121，Kubernetes「未完成/已完成作业」 | 将 Job conditions 写成 `Succeeded/Failed`，并把 `backoffLimit` 描述为重试计数。E07 L1219–1227 明确 Job 成功终态 condition 为 **Complete**，失败为 **Failed**；Succeeded 是这里的成功状态描述，也可作为 Pod phase，但不是 Job condition type。`spec.backoffLimit` 是失败重试限额，不是实际重试次数；E07 L986–988 分别定义失败 Pod 与 OnFailure 容器重试的计算。按现表检索会找不到成功条件或混算 attempt。 | 用实际字段区分 Job `status.conditions` 的 Complete/Failed、Pod phase、成功/失败统计与 `spec.backoffLimit` 配置限额；说明 v1.32 所选门控下终态与 Pod 终止的时序，实际重试按 restartPolicy 分支核对，而非从 backoffLimit 推导。 |
| B24-T10-C05 | P2 | L124，Slurm「健康/准入」 | 写成 HealthCheckProgram“在节点重注册后执行”，倒置官方启动链。E10 L1393–1395 明确是在 slurmd 首次启动且**注册到 slurmctld 之前**执行；另有按 HealthCheckInterval 等条件触发的周期路径。不能据此假设每次重注册后自动完成健康验证。 | 改正首次启动/注册前与周期运行两类触发；对故障恢复窗口记录实际执行时间、结果、有效配置与节点身份。没有执行证据时健康项为 unknown，不把注册成功或 NOT_RESPONDING 消失当作已通过健康门禁。 |
| B24-T10-C06 | P2 | L127；取证记录 L60；任务 acceptance 第 4 项 | 必交的“官方故障测试/案例”仍未交付。这里只给 Job 控制器目录与 Slurm testsuite 目录，并明确没有逐用例核对控制面故障；E18 的目录和单测名称存在不证明覆盖 API/etcd 恢复、主备切换或 DBD 故障。作者诚实披露缺口是正确的，但不能因此判该验收完成。 | 至少为所覆盖的 K8s/etcd 与 Slurm 关键分支提供真正相关的官方故障测试或案例，固定文件/tag/节及触发条件、观察/断言、限制，明确本库未执行；不能把 HA 操作说明或普通 Job 失败单测充作已验证灾备案例。找不到的分支继续 OPEN/缺证，不得宣称已覆盖。 |
| B24-T10-C07 | P2 | L114–135，尤其 L129 与 L135；任务 acceptance 第 4 项 | 恢复核验停在项目名和“有无法解释项则不完成”的原则，未给出**恢复前旧作业基线、恢复后受控新任务、普通生产准入**之间的实际验收闭环。没有明确已完成旧作业不得被误重跑的对照、未完成旧作业与新任务各自的输入/预期/通过失败未知判据，也未把现有节点摘除文章的受控验证准入门槛接入此流程。演练只有操作名与“记录逐项结果”，不足以判断新旧任务正确性及持续进展；泛用 loss/Checkpoint 还不能替代服务或其他负载的契约。 | 补一个方法设计级、明确未执行的验收矩阵：旧已完成/旧未完成/恢复后新任务分别绑定身份、基线、预期副作用、资源占用/释放、应用正确性与连续观察条件；训练/服务等不适用项说明原因。普通生产仍受既有授权的排除/准入控制约束，仅经授权的验证入口运行新探针；unknown/失败均不放行。可精确链接复用 T05-08 的三层门槛，不必复制正文，也不要求本轮执行演练。 |
| B24-T10-C08 | P2 | L77、L142「记账库只存历史」 | 调度状态与记账状态应分离，这个结论成立；但将记账库限定为**只含已结束作业历史**过窄。E20 同版本 sacct 手册 L536–550 明确支持当前运行中及满足条件的 PENDING 记录查询，不能由归档/purge 对已结束作业的描述推出记账库只存完成记录。这样会误导恢复窗口内活动作业与记账记录的对账范围。 | 改为记账记录/关联数据与调度器运行状态的职责区别，承认活动作业记录也可能存在；对恢复窗口分别核对活动与完成记录、缺失/延迟/重复及查询时间范围。保留“恢复数据库不等于恢复 slurmctld 队列”的正确边界，不反向把 DB 当实时分配真相。 |
| B24-T10-C09 | P3 | front matter L8–26；正文 L127 | 正文引用了已登记的 `src.kubernetes.job-controller-tests-v1.32.0`、`src.slurm.testsuite-24-11-7-1`，但两者均未进入本页 `source_refs`。ID 有效不等于依赖清单完整；当前工具只校验列出的 ID，不能自动发现漏列。 | 在 C06 选择/核实实际测试材料后，将最终使用的测试来源补入 source_refs；若替换或删除无效入口，同步正文和依赖清单。再次做 ID/链接检查，勿把登记存在性写成测试覆盖。 |
| B24-T10-C10 | P3 | 导航 `knowledge/05-cluster-platform/index.md` L77，另见 L59、L82、L114 | L77 仍写“T05-10 等未交付”，但同页已列出本篇审阅中的草稿正文，且文件实际存在；混淆“草稿已交付、审阅未通过、主题验收未完成”三种状态。 | 统一为草稿已交付但审阅/主题验收未闭环的实际状态；不要直接改成审阅已通过，也不要因本报告出现就回填任务 done。 |

## 4. 逐节抽查结果

| 正文小节 | 至少一处已独立核对的主张—证据 | 判断 |
|---|---|---|
| 目标与触发条件 | 控制器承担排队、节点监测及资源分配（E09 Controller Node）；与 T05-10 objective 对照 | 归属与问题范围合理；触发症状没有直接充作根因 |
| 只读证据入口与各层责任 | API server 身份/组件选主/节点 renewTime（E03/E04）；scontrol ping、状态目录（E09/E11） | 多数可追溯；缓存一致性及记账范围分别见 C01/C08 |
| 故障分支 / Kubernetes | 停 API server 后恢复全部 etcd、组件重启建议（E01）；内建控制器宿主（E05） | 这些原文口径可核；旧 revision 与恢复身份的缺项见 C02 |
| 故障分支 / Slurm | 主备共享状态与回切（E09）；-r/-R/-c/-i（E12）；DBD -u/-R（E13） | 主要机制与破坏性提示有依据；未把 DBD -u/-R 误写成完整灾备方案 |
| 备份、恢复与重建的前提和停止门槛 | 快照敏感性/目录更换（E01）、迁移五步/双主破坏性（E10）、升级迁移不可任意降级（E14/E15） | 保护证据、授权和双主警告成立；灾备身份/cache 尚未形成足够的专门前提，见 C02 |
| 恢复后账本与进展核验 | Job 终态（E07）、容器 restartCount（E08）、HealthCheckProgram（E10）、训练脚本 checkpoint（E16） | 有跨层意图，但 C03/C04/C05 是字段/时序实质错误；C06/C07 为必交范围缺口 |
| 停止条件与完成判据 | 与 E10 的破坏性边界及 E01 恢复前提对照；“未验证进展不关闭”为作者的方法设计 | 未声称实际执行；仍需 C07 的可判定验收与准入闭环 |
| 常见误解 | 410 的重新 list（E02）、Slurm 落盘前丢状态（E09）、etcd 组件重启建议（E01） | 多项澄清有据；自动重放与“只存历史”分别受 C02/C08 影响 |
| 来源与边界 | 版本化 K8s 页面、Slurm 归档与取回 SHA-256；MindCluster 组件职责（E17） | 固定边界基本清楚；404 和未做的专项取证按限制记录，不凭记忆作事实判定 |

## 5. 验收条目逐项核对

| 任务原验收条目 | 当前交付与缺口 | 结果 |
|---|---|---|
| 1. 列出只读证据入口、身份/时间戳/对象版本、leader/quorum/cache/状态存储责任；资源视图正常不证明设备和应用正常 | L56–80 提供 Lease、RV、快照、ping、日志与状态目录，明确资源视图不证明应用正常。时间/身份线索存在，但缓存保证被混淆，恢复后身份键误用容器计数，记账范围偏窄。 | **部分满足，未通过**：C01、C03、C08 |
| 2. K8s API/etcd/控制器与 Slurm slurmctld/slurmd/slurmdbd 故障按官方前提分支；调度与记账状态不混同 | L84–101 结构上覆盖六类，Slurm 恢复选项及同库备 DBD 有精确依据。slurmd 复用既有参考并非机械套 K8s。调度/记账分离方向正确，但数据库“只有完成历史”的限定不正确；etcd 的 cache/身份条件欠缺。 | **部分满足，未通过**：C02、C08 |
| 3. 说明备份/恢复/重建前提、版本/集群身份、回放/重复调度风险及停止门槛，先保护证据与恢复点 | L103–112/L133 具备证据保护、版本入口、双主警告和破坏性动作前的停止条件；没有伪造站点版本。仅提“集群身份”和“会重放”不足以覆盖 etcd 新逻辑成员、旧客户端缓存及恢复端点前提。 | **部分满足，未通过**：C02 |
| 4. 检查重复/过期分配、未完成/已完成、attempt/Checkpoint、资源清理、健康/准入、新旧任务正确性与进展；给官方故障测试/案例和未执行演练 | L118–129 已列多数核对主题，标注演练未执行且未冒称 reproduced。但核验字段和健康时序有误，测试只给目录且承认未核验，缺受控新任务与旧完成/未完成任务的分类验收及放行门槛。 | **未满足**：C03、C04、C05、C06、C07；来源依赖完善见 C09 |

任务 source_discovery 的 controller workqueue/cache 与故障测试缺口不能仅靠 unknown 自动转为 covered。可以明确保留未知实现细节，但不能同时对依赖该细节的恢复行为作确定性承诺，也不能视为完成原必交验收。

## 6. 元数据、来源、导航与硬规则

- **主归属/稳定 ID：** `cluster-platform.control-plane-recovery` 唯一，匹配任务 target；`type: procedure`、`domain: cluster-platform`、标题匹配。未重复建立 paths 正文。
- **编辑/验证状态：** `draft / source_checked` 不等于本轮通过；`environment_refs: []` 与缺环境档案说明一致。`verification.evidence_refs` 两项均存在，notes 明确未执行恢复、快照、切换或命令；本轮也不将其提升为 reproduced。受 C01–C08 影响的来源核对结论须修订后重新确认。
- **版本/日期：** `updated_at: "2026-10-18"` 是本轮日期，未填未来日期。K8s v1.32、Slurm 24.11.7 是有限语义样板，不是当下推荐版本或端到端兼容组合。`generic` 没有被拿来证明 NVIDIA/Ascend 整栈通用适用。
- **引用结构：** 18 个 source_refs、5 个 related_ids、2 个 verification 引用均能解析；正文 12 处本地相对链接目标存在。外部测试依赖漏列见 C09。上游许可 partial/unknown 沿用其边界，不因本轮阅读而擅自变更许可结论；本报告不搬入上游长段正文。
- **导航互链：** 领域入口的正文链接和 related_id 均存在；正文也链接既有生命周期、回收和升级文章。交付状态不一致见 C10；对 06/08 章节的泛称不视为已完整覆盖训练一致性/证据方法，C07 可用精确链接复用已有门槛。
- **unknown/合成/性能：** 保留现场参数、MindCluster/Kueue/Volcano 专属灾备及真实演练未知。未发现把厂商性能数字写成通用结论；正文没有冒充真实事故的合成日志或测量结果，演练明确为未执行的方法设计。后续若增加示例记录，必须另标“合成”，不能伪装为本地事件。

### 结构检查

本轮实际执行：`PYTHONDONTWRITEBYTECODE=1 make check`。

结果：`PASS: 103 content entries; 489 sources.` 工具同时声明仅检查结构和本地文件链接，不检查技术正确性或远程链接。该输出是本次当前工作区的结构结果，不是恢复演练结果，也不证明上述 OPEN 发现已关闭。

未执行 `make build`，以遵守本次“只新增报告一个文件、不改写生成物”的交付范围；没有修改 `src/kb/`，未运行软件测试。所有主动故障、控制面/daemon 生命周期操作、快照、恢复与硬件验证均未执行。

## 7. 最终判定与定向复核门槛

**暂不通过（T05-10 本轮范围）。** 开放发现为 **P1 0、P2 8、P3 2**，其中 C01–C08 为阻断项；不对 Batch 24 其他任务、05.2/05.3/05.7 主题整体或真实环境恢复能力作通过声明。

作者修订后，定向复核至少应重新打开受影响的 API/etcd 恢复、Pod/Job 字段、Slurm 健康/记账页面及实际选用的官方故障用例，逐项确认关闭条件与新旧任务验收矩阵。来源登记、正文、导航及依赖 ID 应保持一致。只有开放 P1/P2 清零且验收条目重新核对后，才能给出本任务通过结论；即使模型审阅通过，真实环境验证仍保持未完成，不能据此宣布灾备成功。
