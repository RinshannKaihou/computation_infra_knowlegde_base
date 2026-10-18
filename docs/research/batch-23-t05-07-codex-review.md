# Batch 23 · T05-07 独立技术审阅（Codex，首轮）

## 1. 审阅元数据

| 项 | 记录 |
|---|---|
| 任务 | T05-07「多租户争用、公平性与容量验证」，procedure |
| 角色 | 独立技术审阅者；不是本文作者；本轮不修订正文 |
| 实际模型 / 推理档位 | **`gpt-6.1-sol / xhigh`** |
| 模型核验 | 读取本次本地 Codex CLI 会话的 `turn_context`：`model=gpt-6.1-sol`、`effort=xhigh`；不是把约定模型抄作实际模型。本轮未调用子代理，也未另行路由模型；审阅输出无 `[frontier_llm]` 标记 |
| 日期 / 时区 | 2026-10-18，Asia/Shanghai（UTC+08:00）；会话始于约 16:25，取证及首次校验截至 16:39，报告落盘后于 16:43 复验；均为本轮实际执行时间 |
| 轮次 | 首轮独立审阅；未开展修订复核；发现均为 open |
| 写入范围 | 仅新增本报告；不修改正文、来源记录、登记表、计划或仓库构建产物 |
| 取证方式 | 本地文件只读检查；GitHub 连接器取得固定提交文档/API 原文及 tag 对象；网页工具实开 NVIDIA 官方页面；Slurm 归档访问失败后，以官方同版本仓库文档作明确标识的补充证据 |
| 实验边界 | 未连接集群、未提交负载、未改变队列/配额、未配置共享模式、未执行 GPU/NPU 对照；模型审阅不构成硬件或安全验证 |

### 1.1 文件清单

主审文件与材料：

- [正文](../../knowledge/05-cluster-platform/contention-capacity-validation.md)，186 行；下文简称 **P**，行号均为该文件本轮快照的原始行号。
- [作者侧来源记录](batch-23-t05-07-sources.md)，62 行。
- [来源登记表](../../sources/registry.yaml)：逐项读取任务要求的十个登记条目，即四个 Kueue 条目、三个 Slurm 条目和三个 NVIDIA 条目；另检查正文全部 `source_refs` 的存在性。
- [验收清单](../../plans/full-coverage-backlog.yaml)，T05-07，L5648–5694。

邻近正文：

- [作业准入、调度与拓扑放置](../../knowledge/05-cluster-platform/admission-and-placement.md)。
- [空闲设备但作业等待诊断指南](../../knowledge/05-cluster-platform/idle-resource-job-waiting-triage.md)。
- [Kubernetes 作业全生命周期与控制器责任](../../knowledge/05-cluster-platform/kubernetes-job-lifecycle.md)。
- [Slurm 作业生命周期、设备资源与状态参考](../../knowledge/05-cluster-platform/slurm-jobs-and-device-resources.md)。
- [加速器共享与租户隔离机制](../../knowledge/05-cluster-platform/accelerator-sharing-and-isolation.md)。

规范及校验入口：[README](../../README.md)、[编写指南](../authoring-guide.md)、[内容总目录](../../content-outline.md)、[元数据 schema](../../schemas/content.schema.json)、`Makefile`、`src/kb/cli.py`。邻文只用于检查边界和已有入口，不能替代上游证据；本轮不对邻文作整篇通过认定。

快照 SHA-256（用于后续复核识别本轮输入，不是上游网页哈希）：

| 文件 | SHA-256 |
|---|---|
| P | `13bb10da07528b8d2305baf7aec40a0c7d27bc75eef56cd0d6900ae39158b451` |
| `docs/research/batch-23-t05-07-sources.md` | `a613060cf3466938a51472c2b8a37b8cd4371ea5d034859e91e5739feed9a047` |
| `sources/registry.yaml` | `071161e0bcaeef4466e854ad09d3f45a04892be7456d15244f05f3d62eea1e0e` |
| `plans/full-coverage-backlog.yaml` | `581c9079b9c864f3877e615290fe8116a3fe60667c7256336e244c8c14f62de9` |

并行变更说明：16:43 复验确认 P、作者侧 T05-07 来源记录和验收计划仍与上表哈希一致；登记表则在其他并行工作中追加四项来源，总数由 465 变为 469，上表登记表哈希保留为取证时快照而非末次状态。工作区还出现其他任务的报告；本审阅未写入这些文件，亦未据其结论替代独立取证。邻文的行号定位以本轮读取时版本为准，不声称工作区为原子快照。

## 2. 结论

**需修订后定向复核，本轮不通过。发现 7 项：P1 0 项、P2 7 项、P3 0 项。** 不是因为缺少现场实验而否定一篇明确标注“未执行”的验证设计；开放问题在于设计本身的判断门槛、试验可比性、机制适用条件和安全恢复约束尚不闭合。

已确认的优点：

- 容量记录覆盖资源向量、队列/配额、拓扑/碎片、保留/余量、任务需求和失效预算，明确反对以设备利用率或总卡数表示可用容量（P L74–95）。
- 分列 Kueue 与 Slurm 观察入口，没有直接把两者对象名互译（P L68、L109–119）；四类公平性口径及主要误用已有框架（P L123–137）。
- 前置条件、证据表、步骤、停止和完成条件均存在；未虚构命令执行记录、性能数字或本地事故；预计与实际分栏，实际均标为未执行（P L149–154）。
- 元数据保持 `draft / not_verified`，`applicability` 与 `verification` 齐全，空环境及验证引用未冒充已验证环境。

尚不能通过的核心原因：MIG 被写成不受边界限制的“互不影响”，同租户重复的进入条件反向；A/B 缺少可比性约束和公平共享初态控制；限额试验没有区分准入控制与运行期隔离；“首个受影响边界”的取证规则及 MPS 安全退出分支不足。Slurm 原始归档本轮未取得，另有独立的证据访问边界，不能声称所有必查 URL 已成功复核。

## 3. 上游实开记录与证据索引

以下均于 **2026-10-18** 取证。E 编号仅在本报告内使用，不是新增登记 ID。未把搜索摘要当成原文，也未以可变主站替代 Slurm 24.11.7 归档。

### 3.1 Kueue：固定提交与功能范围

已通过官方 GitHub `refs/tags/v0.19.0` 及其 annotated-tag 对象核对：tag 对象 `7b3cad14a540cd256dc9c658be5a23fff809ff68` 指向 commit **`911a822a49bcfd99c9c62203a009efa4130ad604`**。这里只确认版本映射，不声称签名验证或运行兼容性。

| 证据 | 实开位置 | 核对结果 |
|---|---|---|
| E01 | [admission_fair_sharing.md@911a822a](https://github.com/kubernetes-sigs/kueue/blob/911a822a49bcfd99c9c62203a009efa4130ad604/site/content/en/docs/concepts/admission_fair_sharing.md)，全文，重点 How it works / Configuration / Observability | 对同一 ClusterQueue 下的多个 LocalQueue 排序；历史使用量衰减和 entry penalty 与 P L119 基本相符。feature gate 默认开不等于目标 CQ 已选用该准入模式；CQ 还需 `admissionScope.admissionMode: UsageBasedAdmissionFairSharing`。文中的 `168h`、`5m` 是示例，不应称为默认值 |
| E02 | [fair_sharing.md@911a822a](https://github.com/kubernetes-sigs/kueue/blob/911a822a49bcfd99c9c62203a009efa4130ad604/site/content/en/docs/concepts/fair_sharing.md)，全文 | Admission Fair Sharing 与基于抢占的 Fair Sharing 是两部分。防循环证明有借用及 DRS 单调变化等假设，分层情形仍列为 Limitations；不能推广为任意租户拓扑的无循环保证。页内实现链接确实指向另一 commit `efc4a1bc…`，本轮没有把它当作 `911a822a` 实现证据 |
| E03 | [localqueue_types.go@911a822a](https://github.com/kubernetes-sigs/kueue/blob/911a822a49bcfd99c9c62203a009efa4130ad604/apis/kueue/v1beta2/localqueue_types.go)，`LocalQueueSpec` / `LocalQueueFairSharingStatus` / `LocalQueueAdmissionFairSharingStatus` | `spec.clusterQueue` 明确归属；历史资源量和更新时间位于 `status.fairSharing.admissionFairSharingStatus` 下。`weightedShare` 的 API 注释是超 nominal quota 相对 cohort 可借资源的加权份额，不应直接解释为历史用量标量或应用公平分数 |
| E04 | [admission.md@911a822a](https://github.com/kubernetes-sigs/kueue/blob/911a822a49bcfd99c9c62203a009efa4130ad604/site/content/en/docs/concepts/admission.md)，全文；[cluster_queue.md@911a822a](https://github.com/kubernetes-sigs/kueue/blob/911a822a49bcfd99c9c62203a009efa4130ad604/site/content/en/docs/concepts/cluster_queue.md)，原文件 L330–455；[jobs.md@911a822a](https://github.com/kubernetes-sigs/kueue/blob/911a822a49bcfd99c9c62203a009efa4130ad604/site/content/en/docs/tasks/run/jobs.md)，L1–70 | 补查准入、借用/借出/抢占及 Job→LocalQueue 归属。配额是准入账本，不构成已运行任务的 GPU 算力、网络或存储带宽隔离。该轮没有审计完整调度实现 |

### 3.2 Slurm：原归档失败与同版本补充证据分开

| 必查 URL | 本轮状态 |
|---|---|
| `https://slurm.schedmd.com/archive/slurm-24.11.7/sshare.html` | **未取得正文**；网页工具返回该 URL 不可访问，Node HTTP 读取返回 `getaddrinfo ENOTFOUND slurm.schedmd.com`。没有取得 HTTP 状态，不将其写作 404 |
| `https://slurm.schedmd.com/archive/slurm-24.11.7/priority_multifactor.html` | **未取得正文**；网页工具返回该 URL 不可访问 |
| `https://slurm.schedmd.com/archive/slurm-24.11.7/overview.html` | **未取得正文**；同上 |
| `https://slurm.schedmd.com/archive/slurm-24.11.7/gres.html` | **未取得正文**；同上 |

本地 shell 的 GitHub raw 请求亦因 DNS 失败；随后 GitHub 连接器可用。浏览器控制入口没有可用浏览器。搜索返回的 Slurm 裸域名可变页面没有用于证明 24.11.7 行为。

作为补充，通过官方 GitHub `refs/tags/slurm-24-11-7-1` 和 tag 对象确认：`9d1ef1877186d8101769352831c8f0fe303df31c` 指向 **`defaf214db2e55326f45ab08f1bde5b2036d9f5d`**，tag message 为 24.11.7 release。然后读取以下同版本原文件；**不声称它们与不可访问的 HTML 归档逐字相同**：

| 证据 | 同版本补充原文 | 核对结果与边界 |
|---|---|---|
| E05 | [doc/man/man1/sshare.1@defaf214](https://github.com/SchedMD/slurm/blob/defaf214db2e55326f45ab08f1bde5b2036d9f5d/doc/man/man1/sshare.1)，L1–240（通过已核对的 release tag 读取） | `sshare` 依赖 `priority/multifactor`；Fair Tree 默认及 `Level FS = Norm Shares / Effectv Usage` 与 P L119 相符。Level FS 需 `-l`；Raw Usage 无 `TRESBillingWeights` 时退为 CPU-seconds，并按配置衰减；PERFORMANCE 明确警告客户端 RPC 及循环调用风险 |
| E06 | [doc/html/priority_multifactor.shtml@defaf214](https://github.com/SchedMD/slurm/blob/defaf214db2e55326f45ab08f1bde5b2036d9f5d/doc/html/priority_multifactor.shtml)，L1–200、L270–345 | Fair-share 是多因子之一；其他优先决策含抢占、预留及 partition tier；配置和历史衰减影响解释。支持 P L119 的概括，不证明任意站点已启用相关权重，也不证明设备物理占用已按 GPU 记账 |

来源记录所称归档 man2html 生成时间 **2025-11-11 GMT** 未能在归档原页面独立确认；tag 对象日期不能替代 HTML 页脚的生成日期。`src.slurm.gres-tres-cgroup-24.11.7` 本轮完成登记项和邻文阅读，但未独立重开其整组 cgroup/GRES 归档页面。

### 3.3 NVIDIA：固定 README 与可变文档

已核对 device-plugin `v0.20.1` 的 annotated-tag 对象 `03296a61aeb9943906a1789f978ac3c87e13dfdd` 指向 commit **`487d7a93894b0f3ad08097169593972eb3ca8206`**。

| 证据 | 实开位置 | 核对结果 |
|---|---|---|
| E07 | [README@487d7a93](https://github.com/NVIDIA/k8s-device-plugin/blob/487d7a93894b0f3ad08097169593972eb3ca8206/README.md)，原文件 L350–590，Shared Access to GPUs / With CUDA Time-Slicing / With CUDA MPS | time slicing 不增加显存/故障隔离，多个 replica 请求不保证比例算力；它与 MPS 互斥，共享方式按节点而非逐卡配置。该固定 README 仍将插件 MPS 标为 experimental，且 MIG-enabled 设备不支持该插件 MPS 路线；没有用于本文的实测性能数据 |
| E08 | [When to Use MPS](https://docs.nvidia.com/deploy/mps/when-to-use-mps.html)，System / Application Considerations、Memory Protection and Error Containment、资源限额相关节；[MPS Overview](https://docs.nvidia.com/deploy/mps/index.html) | 单用户活动 server、默认同 UID、监控归到 server、有限错误遏制和非预留式资源上限均有原文。Application Considerations 明确警告：尚有 GPU 工作未同步即终止客户端，可能影响 server/其他客户端并产生挂起、失败或损坏。Overview 跳转到 `latest/index.html`，本轮显示更新于 2026-09-09；这是可变文档，不是固定 CUDA/驱动版本 |
| E09 | [MIG Concepts](https://docs.nvidia.com/datacenter/tesla/mig-user-guide/concepts.html)，GI / CI、Profile Placement、Table 3；另实开 [Supported GPUs](https://docs.nvidia.com/datacenter/tesla/mig-user-guide/supported-gpus.html) 和 [Guide 入口](https://docs.nvidia.com/datacenter/tesla/mig-user-guide/) | GI 的显存 QoS 与同 GI 下 CI 共享显存/引擎均有明文；布局可能产生碎片。Table 3 的 GPU 机制隔离不能扩展为整个应用跨层互不影响。页面显示更新于 **2026-10-13**，观察日期为 **2026-10-18**；Guide 入口跳转 `latest/`，未固定驱动或完整支持组合 |

## 4. 发现表

分级：P1 为直接高风险错误或严重误导；P2 为会改变技术判断、试验结论或关键执行安全的实质问题；P3 为不改变主要结论的局部可用性/追溯改进。本轮所有发现均须修订并按关闭条件复核，不能仅靠 `make check` 关闭。

| ID | 优先级 | 位置 | 问题及影响 | 证据 | 明确关闭条件 |
|---|---|---|---|---|---|
| **B23-T07-C01** | **P2 / open** | P L145、L149–154，尤其 L153「MIG 两租户：分区内互不影响」 | 把有边界的硬件隔离扩成无条件的互不影响。如果“分区内”指同一 GI 内多个 CI，显存和引擎仍共享；如果指不同 GI 上的两个租户，也不能据此消除主机、PCIe/网络或存储层争用。该预计结果会把正常的跨层干扰误判成 MIG 失效，或反向作为应用 SLO 已受保护的依据。 | E09 的 GI / CI 明确定义共享与分割范围，Table 3 仅比较 GPU 内机制；邻文 `accelerator-sharing-and-isolation.md` L81–87 已明确 CI 共享及主机/网络/存储边界。P 把这些限定压缩掉了。 | 将预计结论限制到经过核对的 **不同 GI** 及对应资源/错误范围；说明同 GI 的 CI 不提供独立显存/引擎份额，主机/网络/存储仍需对照。删除或限定「互不影响」，实际列继续保持未执行；复核时检查本行、正文叙述和完成判据没有再次推出端到端零干扰。 |
| **B23-T07-C02** | **P2 / open** | P L103–104，步骤 3–4；L171 | 同租户重复的推进条件反向：表中要求「差异超出噪声才进入下一步」，同时下一列又说噪声过大应继续重复，完成判据则要求基线可重复。按原文严格执行，稳定基线反而无法进入并发阶段；不稳定基线可能被放行，随后把漂移误认作租户争用。 | P L103–104 与 L171 的内部矛盾；这是流程逻辑发现，不依赖不能访问的上游页面，也不是声称某种统计方法已有实验效果。 | 明确只有基线重复满足预登记的稳定性/噪声判据才进入并发；超出时固定条件、补重复或停止。将“并发相对基线超出噪声”与“基线自身可重复”分开，并统一步骤表两列和完成判据。无需编造统一重复次数或阈值。 |
| **B23-T07-C03** | **P2 / open** | P L63、L101–107；L125–137 | 只有 A-alone 和 A-repeat，没有 B-alone，也没有把 A/B 限制为等价负载与等价资源请求，却要比较吞吐份额和受损情况。对不同模型、step 工作量或请求成本的租户，直接比较有效产出占比无法区分固有速度差异与争用；B 自身是否退化也没有参照。固定各自镜像/模型不等于两租户工作单位可相加。 | 步骤 3–4 仅出现 A；步骤 5 首次引入 B；P L127 允许样本/step/请求等产出单位，未规定它们可比的条件。验收项 2–3 要求可解释的两租户公平性和对照。 | 二选一明确设计：限定 A/B 为可比较的镜像负载、相同有效工作单位和已登记的目标份额；或分别取得 A、B 单独运行及重复基线，用各自归一化退化/SLO 指标评价异构负载，不将不同模型 step 或请求直接求份额。登记两方提供需求、实际重叠执行窗口和样本口径，保留实际结果待填。 |
| **B23-T07-C04** | **P2 / open** | P L75、L88、L103–119；L173 | 两个平台虽分栏，但租户归属、机制是否启用及历史记账初态没有成为试验门槛。Kueue 下未区分两个 LQ 进入同一 CQ 的 AFS 与不同 CQ 的 cohort/抢占公平；表中还并列历史量和 `weightedShare` 而不解释其不同含义。先跑 A 基线会改变历史用量，随后新 B 被优先准入可能正是策略预期，不能直接据等待差异判不公平。Slurm 的 share 层级、计费资源及有效优先级权重也未进入对照记录。 | E01 的同 CQ、显式 admissionMode、衰减和 entry penalty；E02 的另一类公平机制；E03 的字段层级/DRS 注释；E05 的历史量和 CPU-seconds 回退；E06 的多因子及历史衰减。作者来源记录 L15 已有部分启用条件，但 P 未落成检查分支。 | 为两平台分别登记 A/B 的真实租户→队列/association 映射和有效配置。Kueue 核验 gate、目标 CQ admissionMode、LQ 权重及完整历史字段路径，跨 CQ 则转相应机制，不能套 AFS；Slurm 核验 PriorityType/Fair Tree、关联层级、相关权重及资源计费口径。记录基线前后与并发前的历史状态并采用可审查的初态/轮次控制；不要求也不授权清零生产账本。明确观察到的是准入公平、资源记账还是应用公平。 |
| **B23-T07-C05** | **P2 / open** | P L79、L82、L105–106；L171 | 「隔离/限额」一步把 MIG、MPS、time slicing 和队列限额并列，却没有指明改变哪一层、验证哪种强制约束生效。减少访问名额或准入任务数能因实际并发下降而改善 SLO，但这不是已运行租户获得了显存/算力隔离。切换共享路线还可能改变 profile、资源名和放置，因此无法直接沿用之前的基线并声称单变量隔离对照。 | E07 明确 time slicing 的名额性质、无隔离、MPS 不同语义、节点级影响及路线互斥；E04 是逻辑准入配额；E09 的分区资源形状和 idle 重配置范围。P L82 的一般单变量提醒不足以确定本步骤的实验自变量。 | 拆分准入/并发上限、GPU 运行期上限/硬件分区以及主机/网络/存储控制的适用分支，给出所选控制已生效的可观察证据。每轮只改变已登记的参数并记录实际并发、设备身份及资源形状；如切换模式或 profile，重建相应单租户基线，并将减少总并发带来的改善标为策略权衡，不当作运行时隔离证明。无可用控制的边界保持 unknown。 |
| **B23-T07-C06** | **P2 / open** | P L81、L105；L134；L168–175，尤其 L172 | 只列出要看 GPU/NPU、CPU/内存、网络和存储，没有定义“首个”如何从同一试次的时间线与指标判定，也没有区分两任务同时提交与真正同时产生设备负载。完成判据又强制要求指出一个受影响边界：若并发没有可检出的退化，或多个层在采样分辨率内同时变化，就被迫猜一个边界或永不完成。 | P 的证据表/步骤表没有共同时间基准、run/attempt 与实际放置映射、开始/就绪/稳态时间点和异常阈值；邻文 `kubernetes-job-lifecycle.md` L90–103 明确对齐 UID/attempt，且状态事件列出顺序不等于发生顺序。上述缺口是设计可审查性问题，不是本轮已经发现某层争用。 | 预登记统一窗口、采样/时间误差、试次身份、实际设备/节点映射、应用活动重叠及各层相对基线的变化判据；首个可见异常只作为候选，需结合已控制的干预和恢复证据限制因果表述。完成结果至少容纳：有证据的边界候选、在给定负载/窗口下未观察到显著退化、证据不足/无法排序的 unknown；不得把后两者写成全场景无争用或强行根因。 |
| **B23-T07-C07** | **P2 / open** | P L106–107、L144、L158–166、L175 | 包含 MPS 两租户路线，却把「释放 B、确认 A 回到基线」统一标为「可逆」，停止/回退分支没有 MPS 的同步退出条件。不是说正文已经要求强杀，而是它没有排除直接取消/终止 B 的危险实现：该动作本身可能破坏 A 或 server，使所谓恢复对照成为新的故障注入。只要求事后验证应用不能替代事前安全退出约束。 | E08 Application Considerations 明确列举未同步终止客户端可能造成 server/其他客户端挂起、失败或损坏；错误遏制节说明 FAULT 后需等待受影响客户端退出再恢复上下文。邻文 `accelerator-sharing-and-isolation.md` L94–98 已提及该限制，P 的恢复步骤未引用或展开。 | 为 MPS 增加正常结束/同步退出的前置条件、退出及 server/client 状态确认、不能安全释放时的停止分支；取消、重配和故障后的清理只按已有授权及适配版本操作，不给通用强杀/复位处方。去掉无条件「可逆」，若发生故障须将该轮与正常释放恢复对照分开，并明确不得为了恢复 B 破坏仍运行的 A。 |

## 5. 验收项覆盖表

| 验收项 | 本轮判断 | 已有覆盖 | 缺口 / 对应发现 |
|---|---|---|---|
| 1. 容量资源向量、队列/配额、拓扑/碎片、保留/余量、需求和失效预算；利用率/总卡数不等于容量 | **设计字段覆盖**，不是容量数值已验证 | P L74–95，六组记录字段齐全，利用率/卡数反例清楚；未给虚构容量值 | 现场资源及任务需求仍 unknown；不得用本轮通过结构检查承诺可用容量。没有仅因未实测而另开问题 |
| 2. 双平台租户/队列分配和观测；四类公平性定义及误用 | **部分覆盖，待修订** | P L68、L109–137，平台分栏、四种口径、窗口/失败样本/总产出权衡均有说明；Slurm FairShare/Level FS 概括获同版本源码文档支持 | C03 的负载可比性；C04 的租户映射、AFS 启用及历史/计费初态；Slurm 两个指定原归档页面本轮访问仍未闭环 |
| 3. 基线→重复→两租户并发→隔离/限额→恢复，并观测首个受影响边界 | **形式完整，执行判断未闭合** | P L99–107 五阶段顺序都有，L158–175 有停止和完成条件 | C02 反向门槛；C03 双方参照；C04 历史偏置；C05 控制变量与强制边界；C06 时间线及合法无退化/unknown 结果；C07 MPS 安全退出 |
| 4. 官方共享/隔离限制或上游性能案例，缺失支持/安全证据、预计与实际分开 | **限制案例成立，但解释待修订** | E07–E09 实开支持 time slicing/MPS 的官方限制；P L147–154 明确是机制预期且全部未执行，未虚构性能数字或本地事故；Ascend 保持未知 | C01 的 MIG 过度承诺；C05/C07 的模式支持和安全执行边界。此验收可用“官方限制”满足，不要求作者编造或补成已执行性能案例 |

## 6. 元数据、引用与本地检查

- P 的稳定 ID、`type: procedure`、`domain: cluster-platform`、`status: draft`、`updated_at` 符合 schema；`applicability.environment_refs: []` 及缺环境说明、`verification.status: not_verified` / 空证据列表与“未执行”的定位一致。**不应因为本报告核对了来源而自动改为 `reviewed` 或 `reproduced`。**
- P 的 13 个 `source_refs` 全部存在；8 个 `related_ids` 均可解析。十个必读登记条目在本轮材料中存在，固定 Kueue/device-plugin tag 与 commit 映射已独立核对；NVIDIA 可变页按观察日期处理。
- P 本身没有内联相对 Markdown 链接，因而没有该类坏链可修；邻近关系由 `related_ids` 表达。需要让读者执行邻文特定安全分支时，应在相应步骤放可用入口，不能把“ID 存在”当成操作边界已经写清；此点已纳入 C07 关闭范围，不另重复计数。
- 在仓库根以 `PYTHONDONTWRITEBYTECODE=1 make check` 执行结构及本地链接检查：首次 **PASS，100 content entries / 465 sources**；16:43 报告落盘后复验为 **PASS，100 / 469**，来源数变化见并行变更说明。这不检查技术正确性、远程可达性或源页支持强度。
- 为遵守只新增报告的限制，没有在仓库内执行会重写 `build/` 的构建；复制输入到自动清理的临时镜像后执行 `make build`，补齐输入后首次 **PASS，100 / 465**，16:43 再次 **PASS，100 / 469**；生成目录仅在临时镜像内。首次镜像遗漏了 `plans/`、`templates/` 和已有 `build/` 链接目标，因镜像不完整失败；补齐输入后通过，不能把首次失败记作仓库缺陷。
- 未改动 `src/kb/`，未添加测试；未运行集群、硬件或性能测试。仓库开始时已有未提交/未跟踪材料；本轮没有回滚、覆盖或整理这些材料。

## 7. unknown / 证据边界

1. **Slurm 原归档仍有访问缺口。** 补充的官方 release-tag 原文足以核对所列语义，但不能证明归档 HTML 当前可访问、生成日期正确或与仓库文档逐字一致。后续应补开指定两页，并保留版本、页内定位和访问结果；本轮不把连接失败推定为 URL 已失效。
2. **现场公平策略及历史初态未知。** Kueue gate、CQ admissionMode、权重、采样和衰减的实际配置；Slurm PriorityType、Fair Tree、association、QOS、计费资源、decay 和优先因子均不能由示例/默认值替代。E01 的配置示例不是默认参数证据；本轮未读取默认化实现。
3. **NVIDIA 支持组合未验证。** 可变 MPS 文档含 Legacy MPS v2 / MPS v3 区分，不能与固定 plugin README 拼成已验证组合。MIG 的具体 GPU/profile/驱动、MPS 服务方式/UID、插件支持状态及现场安全配置仍须确认；性能隔离说明不是完整多租户安全认证。
4. **Ascend 分支仍缺一手隔离保证。** 本轮没有新增 vNPU 规格、显存/算力限额、故障/安全隔离或回收证据；也没有核实 Slurm 与 Ascend 接入支持。GPU/MIG/MPS 规则不外推给 NPU。
5. **跨层指标与容量值均无现场证据。** 没有实际 CPU/内存/网络/存储测量、工作负载重叠证明、SLO 预算值、重复分布或容量准入包络。首个变化点不自动是根因，预计互相影响也不是保证必然失败。
6. **正文另引来源的独立核验范围有限。** MLCommons Storage、MindCluster、Ascend Device Plugin 相关 ID 完成存在性检查；本轮未重新审计其完整上游材料，不据此认证缓存基准规则或 NPU 支持矩阵。登记许可说明只作阅读，本轮未开展新的许可证审计，也未复制上游图表或长段原文。

## 8. 审阅局限与复核要求

本报告是固定文件快照上的文档/设计审阅，不是控制器实现审计、渗透测试、隔离强度测量或容量验收。GitHub 连接器返回原文及 blob 标识，但没有取得 Slurm 归档原始 HTML 字节；NVIDIA 网页读取结果也不是可永久重放的内容快照。网页工具展示坐标不作为 GitHub 源码行号。

所有 C01–C07 在本轮均为 **open**。作者完成修订后，应由独立审阅者按相同 ID 核验变更及关闭条件，并补做 Slurm 指定原归档页的访问核对；未取得的部分继续明确保留证据缺口。结构检查通过不关闭技术发现；技术发现关闭也不把未执行实验改成实际结果。
