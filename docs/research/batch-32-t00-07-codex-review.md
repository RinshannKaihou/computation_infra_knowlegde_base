# Batch 32 · T00-07 第一轮初审报告

## 会话元数据与结论

| 项目 | 记录 |
|---|---|
| 角色 / 轮次 | 独立批次审阅者；第一轮初审；本会话仅交付发现，不承担正文编写、问题修订或关闭 |
| 指定 / 实际模型与档位 | 指定 `gpt-6.1-sol / xhigh`；当前 rollout 最新 `turn_context` 实际为 `model=gpt-6.1-sol`、`effort=xhigh`，一致 |
| rollout 文件 | `/Users/ywang2397/.codex/sessions/2026/10/22/rollout-2026-10-22T09-31-43-01a1613c-47de-76c2-a2e1-264ad5e32bee.jsonl` |
| 归属核对 | L1 `session_meta.id/session_id`、环境 `CODEX_SESSION_ID` 与 `CODEX_THREAD_ID` 均为 `01a1613c-47de-76c2-a2e1-264ad5e32bee`；L10 的 user 消息以“你是 AI 可靠性知识库的独立批次审阅者”起头，包含本次 Batch 32 / T00-07、三页及唯一报告路径 |
| turn_context 核验 | 最新且唯一记录在 L8，时间 `2026-10-22T01:31:55.897Z`；`turn_id=01a1613c-4946-7641-b88b-cd4686f8fefa`；`cwd=/Users/ywang2397/work/AI_reliability_knowledge_base` |
| 交叉字段 | L8 `collaboration_mode.mode=default`；`settings.model=gpt-6.1-sol`、`settings.reasoning_effort=xhigh`、`developer_instructions=null`；未用配置默认值、正文自述或历史报告代替核验；写报告前重新读取，结果不变 |
| 执行方式 | 当前本地 Codex CLI 会话直接审阅；L1 `originator=codex_exec`、`cli_version=0.163.0`、`model_provider=custom`；未另启模型或子代理 |
| 日期 / 时区 | 2026-10-22 / Asia/Shanghai（UTC+08:00） |
| Git 基准 | HEAD 为 `90c38f7592137eeb2b1862983822fe415cf471c5`；三份新页与 T00-07 取证记录均与该提交一致，未发现这四份输入的工作区差异 |
| 写入范围 | 仅新增 `docs/research/batch-32-t00-07-codex-review.md`；不修改正文、导航、取证、registry、计划、历史报告或 build；本报告中的修订建议由编写者处理 |

审阅正文前先执行 `wc -l` 与 `shasum -a 256`，随后再次核对，四份输入的行数与指纹均未变化：

| 输入 | 行数 | SHA-256 |
|---|---:|---|
| [性能优化任务路径](../../paths/tasks/performance-optimization.md)（下称 P） | 82 | `de0b5bff2dbd8826e33e77a89da55acca3b9b57665ca0b75990a2a380d224278` |
| [迁移与升级任务路径](../../paths/tasks/migration-and-upgrade.md)（下称 M） | 94 | `92e58f2f830ffa16cd37c6ed0a942c79cd61ec1fcd911ffd376051f18d9061d9` |
| [故障恢复任务路径](../../paths/tasks/fault-recovery.md)（下称 F） | 77 | `fe44b9902d8a7fae37128bb614b921dac565537e19da3063184d3aab85fe2690` |
| [作者取证记录](batch-32-t00-07-sources.md)（下称 S） | 30 | `28859a729e880965e7e8e04943b7746aaa56abd558d5a2f092fd6d94a6d9146d` |

任务及主题依据为 [full-coverage-backlog.yaml](../../plans/full-coverage-backlog.yaml)，初始 `wc -l=7774`，SHA-256 `abffb0eaff9a825ac37ff1921acfa7a2d1fb73289d85f9d8d88a24febec71530`；T00-07 位于 L7534–7602，主题 00.6 位于 L291–340。

**初审结论：需修订并定向复核，暂不通过。共 4 项发现：P1 0 项、P2 3 项（C01–C03）、P3 1 项（C04），全部 OPEN。** 三条主链、六个恢复分支及全部本地链接总体可达；主要阻塞是停止条件未逐页补齐，以及两处对目标正文门槛的错误转述。角色页另缺两个运行阶段入口。

优先级采用本轮指定口径：P1＝足以严重误导处置的关键错误；P2＝影响任务交付、导航功能或验收证据的必修事项；P3＝局部入口、记录或可追溯性问题。下文 P/M/F/S 行号均以以上指纹为准；其他文件行号单独注明。结构通过不表示内容审阅通过，也不表示任何平台或硬件已验证。

## 范围与方法

先读取 [README](../../README.md)、[AGENTS.md](../../AGENTS.md)、[写作指南](../authoring-guide.md)（§3/§5/§6/§7）、[metadata schema](../../schemas/content.schema.json) 与 [内容边界](../../content-outline.md)。按 T00-07 objective、三条 acceptance 和主题 00.6 的导航边界审阅，不把导航当成操作工单，也不重新验收主题 00.6 的其他任务。

完整读取 P/M/F/S；独立解析三页全部内联 Markdown 内链，逐目标读取 frontmatter，核对存在性、稳定 ID、类型、状态、related ID 及 source ID。对关键描述读取目标正文实际段落，而非只认标题或 `make check` 声明；具体坐标见下表和六分支表。入链扫描范围为 README、knowledge 与 paths；统计实际 Markdown 链接，不把 frontmatter 的 ID 或裸文件名计为入链。

外部来源核对限定于本任务要求的“页尾 URL 与本地 registry 逐字比对”、版本和支持范围承接；本轮未重新抓取外部网页，也未重新认证所链正文全部上游主张。三项外链是既有资料入口，本页技术依据主要是库内正文。未执行所链文档中的 profiling、调参、安装、升级、drain、重试、故障注入、训练续训或服务恢复操作。

## 已核实的主链与边界

### 三条路径与描述抽查

| 路径 / 描述 | 实际正文定位与核对结果 |
|---|---|
| P：先负载、基线，再硬件/主机/数据/通信/训练/推理 | P L42–55 六层均有实际正文；[训练性能分解](../../knowledge/06-training/performance-analysis.md) L52–63 固定有效产出、配置与时间重叠口径；L91–98 给窗口、重复基线、阻塞边、单因素与恢复复测；“受害慢 rank / 最早瓶颈”确实在 L94，不是导航自造术语 |
| P：硬件与主机证据 | [供电散热](../../knowledge/01-hardware/power-thermal-evidence.md) L62–97 区分位图、历史 violation 与健康监测，L108–134 保留 NPU 观测边界；[NUMA](../../knowledge/01-hardware/numa-memory-and-io-locality.md) L86–103 有局部/远端成对测量及实际驻留核对；[主机资源压力](../../knowledge/02-software-stack/host-resource-pressure-and-device-access.md) L59–68 明确物理内存、cgroup 与设备 OOM 三分 |
| P：数据、通信与多租户 | [数据流水线](../../knowledge/04-data-storage/training-data-path.md) L50–77、L125–139 提供相邻边界；[数据饥饿](../../knowledge/04-data-storage/data-starvation-triage.md) L74–92 与 [Checkpoint I/O](../../knowledge/04-data-storage/checkpoint-slow-io-triage.md) L72–97 承接等待分解；[带宽退化](../../knowledge/03-communication/bandwidth-degradation-triage.md) L43–53 确有“测量口径/配置映射/真实链路”三分；[RDMA](../../knowledge/03-communication/rdma-baseline-and-congestion-triage.md) L49–77 分开 IB 与 RoCE。共享和争用两篇正文分别承担隔离边界与公平性/容量验证，不把“已分配”当“已隔离” |
| P：训练/推理分流 | [慢 rank](../../knowledge/06-training/slow-rank-triage.md) L61–72 回溯谁先慢；[吞吐回归来源案例](../../knowledge/06-training/performance-regression-source-case.md) L38–50、L77–106 保留单卡、release/同条件复测及质量缺证据边界；[执行与 KV](../../knowledge/07-inference/execution-and-kv-cache.md) L43–97 实有 batch、容量、抢占重算和驱逐的区分；[指标字典](../../knowledge/07-inference/latency-metrics.md) L33–46、L159–247 承担分母与窗口；[容量与冷启动](../../knowledge/07-inference/capacity-and-autoscaling.md) L40–97 及 [路由流控](../../knowledge/07-inference/routing-and-flow-control.md) L45–108 承担执行外的容量/入口因素 |
| M：三类变化与 B0/N/R | M L35–38、L50–67 显式分软件环境、平台节点、模型语义。所链[安装升级正文](../../knowledge/02-software-stack/environment-installation-and-upgrade.md) L157–174 确有变化矩阵，L176–186 确有 B0/N/R：变更前基线、变更后、回退执行后，要求同负载同判据；R 不是计划或“回退路径已确认”。L188–210 给制品保全、不可逆与各平台不同的恢复边界。准入门禁的转述问题见 C03 |
| M：模型语义分支 | [GPU→NPU 诊断](../../knowledge/06-training/gpu-npu-precision-difference-triage.md) L55–81 先固定身份和重复性背景；[混合精度与收敛](../../knowledge/06-training/mixed-precision-and-convergence.md) L78–84 有平台内重复→每配置单因素重复→有限窗口质量验收；[质量评估](../../knowledge/07-inference/output-quality-evaluation.md) L44–54 固定模型/tokenizer/输入身份，L76–115 预注册判据及 baseline/单变量/recover。没有把跨平台逐位一致作为通用要求 |
| F：处置、重试、恢复与记账 | [处置选择正文](../../knowledge/08-reliability/mitigation-and-recovery-principles.md) L75–85 确有可重试性、deadline、预算、jitter 与幂等边界；L104–114 分重算/回退/切换。[可靠性记账](../../knowledge/08-reliability/reliability-metrics-and-recovery-loss.md) L83–92 确有六类量，L106–155 提供事件、尝试/进展等表结构，不能把全部重放一概当作零产出。F L49/L56 未给虚构结果 |
| F：恢复验证与复盘 | F L48 的“身份/结构→逻辑进度→状态内容→同输入单步→持续窗口”逐项对应 [恢复一致性](../../knowledge/06-training/checkpoint-state-consistency.md) L150–161；同表另有“终止与回退”行，仍须按正文执行。F L50 的复盘与更新对应 [复盘正文](../../knowledge/08-reliability/postmortem-and-knowledge-update.md) L55–67、L83–114、L125–129 的记录、追溯、复核及完成门槛 |

P 的“性能＋质量”、F 的“正确性＋持续进展”是导航层摘要，使用时仍须满足各目标正文额外门槛：训练性能正文 L95–98、L146–161 要求可恢复等价起点、噪声带及 A→B→A 或等效设计；处置正文 L114 沿用 [可靠性退出门槛](../../knowledge/08-reliability/dimensions-and-failure-domains.md) L104–115，包含性能包络、允许损失、容量/冗余/隔离及未知项，并要求登记残余降级。本轮没有把导航摘要解释成免除这些门槛的授权；其中性能路径未列“无法回退”分支属于 C01。

### F 的六分支覆盖与状态责任

| 分支 / F 位置 | 链接与实际落点 | 责任及不能替代的证据 |
|---|---|---|
| 单请求/输出异常，L43 | [证据与假设](../../knowledge/08-reliability/evidence-and-hypotheses.md) L33–45、L69–112；[静默错误](../../knowledge/08-reliability/silent-errors-and-integrity.md) L131–162；质量评估 L44–84 | 先辨输入/计算/输出证据；结果可疑不能凭健康摘要放行，也不能自动改判成平台故障 |
| 推理副本/服务，L44 | [服务发布与恢复](../../knowledge/07-inference/release-and-recovery.md) L64–90；[加载与 ready](../../knowledge/07-inference/model-loading-and-readiness.md) L59–93、L117–141 | L74–79 确有“不承诺 exactly-once”专节；关联 ID、客户端展示去重、服务端执行去重、外部副作用分开。请求、缓存、路由和资源责任各自核对，启动 ready 不等于服务恢复完成 |
| 单节点/单设备，L45 | [节点摘除](../../knowledge/05-cluster-platform/node-drain-resource-reclamation.md) L158–176、L210–218；[健康证据](../../knowledge/01-hardware/health-evidence.md)；[节点生命周期](../../knowledge/01-hardware/node-selection-and-lifecycle.md) L91–133、L187–207 | 节点注册、生产排除、验证准入、实际进程/设备/卷与分配账本不同；不能因节点 Ready 或 drain 返回而宣布状态已清空。单节点动作的影响可扩展到通信组，仍须按动作影响域核对 |
| 平台/控制面，L46 | [控制面恢复](../../knowledge/05-cluster-platform/control-plane-recovery.md) L60–84、L128–145、L147–196；[平台变更](../../knowledge/05-cluster-platform/platform-change-and-rollback.md) L146–166 | Kubernetes 对象/消费者缓存与 Slurm StateSaveLocation/记账库分别有责任。资源视图、账本核验与应用进展不互相替代；MindCluster 未取证行为不以 K8s/Slurm 类推 |
| 存储，L47 | [存储客户端与后端恢复](../../knowledge/04-data-storage/storage-client-backend-recovery.md) L45–73；[Checkpoint 完整性](../../knowledge/04-data-storage/checkpoint-integrity-evidence.md) L52–84、L116–146 | 客户端/网络/文件系统/后端按实现分列；先保护证据与最后恢复点，存储侧完成后才进入训练侧。字节完整性不证明 optimizer、RNG 或数据进度正确 |
| 训练状态，L48 | [恢复诊断](../../knowledge/06-training/checkpoint-state-recovery-triage.md) L36–41、L55–83、L97–114；恢复一致性 L107–119、L150–171；[弹性训练](../../knowledge/06-training/elastic-training-and-membership.md) L47–52、L83–93 | “状态恢复是应用责任”对 PyTorch elastic 成立；MindSpeed HA 的副本恢复另有实现条件。导航未把 launcher 重建进程组等同于恢复训练状态，也未保证任意缩扩容可续训 |

六分支均有实际承载正文，本轮未发现必须新增第七分支才能弥补的范围缺口，亦未发现将存储、平台与训练状态误合为单一责任方的链接。F L37 对“六项”的错误转述独立记为 C02，不能由六分支存在抵消。

### 元数据、取证与页尾来源

三页均为 `type=path / domain=overview / status=draft / platforms=[generic] / updated_at=2026-10-22`；ID 与计划 targets 一致。20/13/15 个 related IDs 均存在，三项 source refs 均已登记。schema 不要求 path 强填 procedure 的 applicability/verification；三页未声称 reproduced，generic 限定分别见 P L38、M L31、F L33。

| 页 / registry 位置 | source ID 与逐字相等的 URL | 承接边界 |
|---|---|---|
| P L76 / registry L84–97 | `src.stas.ml-engineering`；`https://github.com/stas00/ml-engineering` | 仓库入口；registry 固定 revision `fb75494c0d9e536f048e27be2869a77fe65ad9f4`，不替代具体章节、版本或许可核查 |
| M L88 / registry L475–488 | `src.pytorch.numerical-verification-2.6`；`https://docs.pytorch.org/docs/2.6/notes/numerical_accuracy.html` | PyTorch 2.6 文档线，登记源码 commit `1eba9b3aa3c43f86f4a2c807ac8e12c4a7767340`；不提供模型验收容差或跨平台确定性保证 |
| F L71 / registry L421–431 | `src.google.sre-effective-troubleshooting`；`https://sre.google/sre-book/effective-troubleshooting/` | 既有章节入口，观察日期 2026-09-29；通用诊断原则不构成 GPU/NPU 操作指南 |

T00-07 的 existing_source_ids 仅列后两项（L7565–7567）；额外复用 Stas 既有登记作为延伸入口并未构成未登记新来源。S L7/L13–16 的“无新增来源、路径以本库正文为依据”与 frontmatter/页尾一致。S L24–26 如实保留只读导航、未实测及既有七份方案执行 0/7 的口径；[独立验证计划](../../plans/validation-backlog.yaml) L6 仍写七份既有方案未执行，不能把此分母误读为该计划全部 V00–V12 工作包的数量。S L30“待审阅后追记”是初审阶段正常占位，本轮不将它当作已修订/已复核，也不要求审阅者代填。

### 全部内链解析结果

计数含同页重复出现的链接；类型统计按该页不同目标去重。未出现引用式链接或带片段的本地链接。

| 页 | 内链出现数 / 不同目标 | 不同目标类型 | 状态 / 缺失 |
|---|---:|---|---|
| P | 26 / 25 | procedure 10、reference 4、concept 5、case 1、path 5 | 25 draft；不存在的目标 0；未知 ID 0 |
| M | 16 / 16 | procedure 9、reference 1、concept 2、path 4 | 16 draft；不存在的目标 0；未知 ID 0 |
| F | 29 / 28 | procedure 11、reference 3、concept 5、case 1、path 8 | 28 draft；不存在的目标 0；未知 ID 0 |
| 三页并集 | 71 次 / 56 个目标 | procedure 25、reference 7、concept 11、case 2、path 11 | 56 draft；45 篇 knowledge 正文中 source_checked 38、not_verified 7；11 个 path 未设 verification |

完整的目标路径、ID、类型及来源页行号列在附录 A。source_checked 仅是目标正文的声明状态，不代表本轮重新审定全部证据或完成实验。

### 入链检查

下表每格为该入口页指向 P/M/F 的实际链接次数及行号，不计算 related_ids。

| 入口 | P | M | F |
|---|---|---|---|
| README | 1（L33） | 1（L33） | 1（L33） |
| 00 首页 | 1（L26） | 1（L26） | 1（L26） |
| NVIDIA 平台 | 1（L198） | 1（L198） | 1（L198） |
| Ascend 平台 | 1（L185） | 1（L185） | 1（L185） |
| AMD 平台 | 1（L112） | 1（L112） | 1（L112） |
| 训练排障 | 2（L113/L130） | 1（L130） | 1（L130） |
| 推理排障 | 2（L93/L108） | 1（L108） | 2（L95/L108） |
| 角色页 | **0** | **0** | 1（L89） |
| README＋knowledge＋paths 全域总计 | 12 次 / 10 页 | 11 次 / 10 页 | 12 次 / 11 页 |

三页都不是全库孤立页；角色这一类入口对 P/M 为 0，按本轮要求记 C04。总计还包括三页之间互链、环境安装路径及节点验收路径。它们中部分输入已有其他会话未提交修订，快照指纹见附录 B。

## 逐项发现

### C01 · P2 · OPEN · 三页未完整列出“证据不足／无回退／权限不足”的停止与升级矩阵

- **位置**：P L40–45、L69–72；M L33–41、L81–84；F L33–37、L64–67；验收依据为 backlog L7558。
- **问题**：第三条 acceptance 要求每条路径分别列出三类触发及停止/升级动作。P 已列无基线、权限不足及证据不足，但没有“优化状态/配置无法回退”的触发；M 已有缺证、回退准备及高危操作另行授权，但没有普通变更/取证权限不足时的明确停止分支；F 写了执行依已有授权，且有缺证/缺恢复点分支，却没有权限不足时的触发→动作。笼统声明“文档不授权”不等于逐页列出的停止条件。
- **证据**：P L72 完整停止列表未出现回退缺失；[性能正文](../../knowledge/06-training/performance-analysis.md) L95–98、L150–151 明确可回退配置、冻结起点恢复与 A 复测，起点不可恢复时不得宣布优化通过。M L84 仅对不可逆/高危操作写“升级授权”；其[平台变更正文](../../knowledge/05-cluster-platform/platform-change-and-rollback.md) L63 则明确升级、drain、CRD 与回退均有授权边界。F L67 未列权限不足；[处置正文](../../knowledge/08-reliability/mitigation-and-recovery-principles.md) L132–134 要求实际处置依既有授权。
- **建议修订**：逐页补齐三类触发→停止的具体活动→登记的缺口→升级至对应授权/状态责任方。P 应区分缺可回退配置与缺可恢复实验起点；两者不足时只保留只读分析或探索性结论。M/F 应明确缺执行权限时停止相应变更、保护现有证据并交由有权责任方，不因重试预算耗尽或需要恢复而默认取得新权限。已有授权仍按其真实范围使用，不要求无理由重复授权。
- **关闭条件**：三页都能直接定位九个单元格的触发和动作；P 的无回退分支与性能正文“不宣布优化通过”一致，M/F 的权限不足分支明确可执行；S 同步记录修订。由编写者处理后定向复核，本轮不修订。

### C02 · P2 · OPEN · F 将正文“动手前固定六项”错误改写为另一组六项

- **位置**：F L37、L54；S L20 的前置结构归纳与该页合读。
- **问题**：F 明确声称“按……的‘动手前固定六项’”，却列为“影响范围、目标维度、状态责任方、证据保全安排、重试预算与授权边界”。这不是所链正文的六字段，缺少动作证据门槛、状态前提、停止/回退条件和恢复判据等门禁。状态责任方与保全安排本身有用，但不能替代这些字段。
- **证据**：[处置正文](../../knowledge/08-reliability/mitigation-and-recovery-principles.md) L51–62 的原表逐项为：**目标维度、证据门槛、影响域、状态前提、停止/回退条件、恢复判据**；L53 明说动作前缺任何一项即是盲操作。其影响域问的是“动作本身会中断谁”，与已发生故障的影响范围还需分别判断。重试预算在 L75–85，授权边界在 L132–134，二者不是该六项表的替代字段。F L54 继续要求记录“六项固定项”，会让错误清单进入产出。
- **建议修订**：准确承接正文六字段，并将状态责任方、证据保全、重试预算、授权边界列为补充前置材料；若保留原创清单，则明确它是本页扩展，并给出与原六字段的完整对应，不能继续将不同清单归为原表。
- **关闭条件**：F 的“六项”与原表逐项一致，或存在不丢门禁的清晰映射；目标产出随之对应，动作影响域与故障影响范围可区分；S 的结构/修订记录与实际页面一致。无需新增运行结果。

### C03 · P2 · OPEN · M 对“三类准入门禁”的来源概括与正文不符

- **位置**：M L39–48、L84；S L13 的“B0/N/R 与准入门禁引自 T02-12”。
- **问题**：M L47 将源文门禁概括为“环境身份/回退准备/结果判据三类缺一即停”，L84 再引用这“三类”。源文实际的三类是完整依赖交集、有效 baseline、恢复路径。页面前置材料虽提 B0、后续也链接兼容性方法，不能证明这句标为源文结构的转述正确；特别是“有环境档案、尚无可复跑结果”与“有有效 B0”必须区别。
- **证据**：[安装升级正文](../../knowledge/02-software-stack/environment-installation-and-upgrade.md) L65–75 的准入表明确列出：①完整依赖交集缺失，②有效 baseline 缺失，③恢复路径未落实。L72 特别规定“已有环境的升级没有 baseline 即停止”，首次安装另有例外；L176–186 定义 B0 为变更前环境实际跑出的验证结果，R 为回退执行后的结果。结果契约要求另在 L93–111；它重要，但不是该三行门禁表的原名或有效 baseline 的替代。
- **建议修订**：按原表准确命名三类门禁，明确缺可复跑 B0 的升级应停；环境/制品身份与冻结结果契约作为独立要求承接，不能借此替换依赖交集或 baseline。S 如继续声称引自原文，应能定位准入表与 B0/N/R 小节。
- **关闭条件**：M L47/L84 的三类与目标正文对应；仅有版本档案、缺可复跑 baseline 的情形可被明确拦截；首次安装例外不泛化到升级。取证记录同步后按相关段落定向复核。

### C04 · P3 · OPEN · 角色页缺少性能优化、迁移升级两条直接入口

- **位置**：[角色页](../../paths/roles/reading-by-role.md) L57–78、L80–97，特别 L74/L89；目标为 P 与 M。
- **问题**：本轮指定检查的 README、00 首页、三平台与两排障页均已接入三页，角色页只接入 F，对 P/M 的直接入链均为 0。架构路径已讨论升级门槛，运维路径覆盖运行问题，却不能从相应角色段落直接进入这两条完整运行阶段路径。
- **证据**：角色页 L74 只列准备阶段三页，L89 运行阶段只补“故障恢复”；全文相对链接解析确认不存在指向 `performance-optimization.md` 或 `migration-and-upgrade.md` 的链接。两页全库入链分别为 12/11，并非全库孤立；发现只针对角色入口接入这一局部要求，不追改历史审阅结论。
- **建议修订**：由导航维护者在适合的架构/运维段落补上性能与迁移路径及其任务目的，沿用三条路径的已有文件，不复制正文。
- **关闭条件**：角色页到 P/M 均有至少一条可解析且语义合适的直接链接；F 入口保留；定向检查链接与短说明，不要求各角色机械重复全部三页。本会话不改角色页。

## acceptance 逐条判断

| 条款（backlog 原文） | 判断 | 依据与待办 |
|---|---|---|
| 1 · 性能串联硬件/主机/数据/通信/训练/推理，先负载与基线；迁移显式区分软件环境、平台节点、模型语义 | **入口与分流结构满足；关联门禁表述需修订** | P L42–55、M L35–67 有实际承载正文；M 的原表归属错误须按 C03 纠正，不能据入口齐全宣告整条路径通过 |
| 2 · 恢复按影响范围和状态责任连接隔离、重试、训练续训、服务恢复；验收同时正确性和持续进展 | **主链满足；前置处置字段尚不合格** | F 六分支、状态责任及双判据有正文依据；C02 错误“六项”影响动作前门禁，需修订后定向复核 |
| 3 · 每条路径列出缺证、无回退、权限不足的停止/升级条件；只引用正文、不执行操作 | **未满足** | 三类触发未逐页补齐，见 C01；F/M 的被引用门禁又有 C02/C03。只读导航及本轮不执行操作部分满足 |

主题 00.6 要求只链接已存在且已核对正文、先修与完成检查、保留真实验证状态。三页的 draft/generic、单一正文归属、无未来文件假链接基本符合；C04 是角色接入待补。主题 L335 还要求修订、定向复核及结构/构建检查后重新验收；本轮不把主题、T00-07 的 planned 或 00.6-G2 的 open 机械改为完成，也不把初审阶段尚未变更这些状态当作额外缺陷。

## 校验、写入与结论

已执行 `PYTHONDONTWRITEBYTECODE=1 make check`，实际结果 **PASS：135 content entries / 577 sources**。另完成三页全部内链、目标 metadata/ID、related IDs、来源 URL 与入链核对。检查器读取本地结构和文件链接，不验证远程网页、正文技术正确性或平台兼容性。

遵守本轮“只新增报告”的明确授权，**未运行 make build**，未改 src/kb，未新增测试或运行 make test；未进行硬件、训练、安装、变更或恢复验证。S 的初审后占位保持原样，全部发现保持 OPEN。

开始时工作区已有修改：`docs/research/batch-32-t00-06-sources.md`、`paths/roles/reading-by-role.md`、`paths/tasks/environment-installation.md`、`paths/tasks/node-acceptance.md`，以及两份未跟踪的 T00-06/T08-09 初审报告。只读取证期间后续状态还出现 `docs/research/batch-32-t08-09-sources.md`、`knowledge/08-reliability/index.md` 的既有修改；本会话没有写入这些文件，不将其他会话变更归为本轮产物。建立 709 个非忽略既存文件的 SHA-256 快照后，至报告写入前对照无修改、无删除、无新增；四份主输入的指纹亦再次一致。本轮唯一写入为本报告。

**T00-07 暂不通过。** 由编写者处理 C01–C04 后，按各关闭条件定向复核三页门禁、S 及角色接入。结构检查成功、既有 source_checked、导航组织和模型审阅均不代替真实环境验证。

## 附录 A：全部内链目标清单

以下按三页并集去重；“出现”用 P/M/F 加原页行号标识，重复行号表示同页存在重复引用。所有目标内容状态均为 `draft`；“验证”仅摘录目标 metadata，`—` 表示 path 未设置该字段。

| 实际目标 / 稳定 ID | 类型 | 验证 | 出现 |
|---|---|---|---|
| [hardware.health-evidence](../../knowledge/01-hardware/health-evidence.md) | reference | source_checked | F:45 |
| [hardware.node-acceptance-triage](../../knowledge/01-hardware/node-acceptance-triage.md) | procedure | not_verified | M:57 |
| [hardware.node-selection-and-lifecycle](../../knowledge/01-hardware/node-selection-and-lifecycle.md) | procedure | not_verified | M:59、F:45 |
| [hardware.numa-memory-and-io-locality](../../knowledge/01-hardware/numa-memory-and-io-locality.md) | procedure | source_checked | P:50 |
| [hardware.power-thermal-evidence](../../knowledge/01-hardware/power-thermal-evidence.md) | reference | source_checked | P:50、F:45 |
| [software-stack.compatibility-evidence](../../knowledge/02-software-stack/compatibility-evidence.md) | reference | source_checked | M:48 |
| [software-stack.dtype-layout-and-precision-semantics](../../knowledge/02-software-stack/dtype-layout-and-precision-semantics.md) | concept | source_checked | M:64 |
| [software-stack.environment-installation-and-upgrade](../../knowledge/02-software-stack/environment-installation-and-upgrade.md) | procedure | source_checked | M:47 |
| [software-stack.host-resource-pressure-and-device-access](../../knowledge/02-software-stack/host-resource-pressure-and-device-access.md) | procedure | not_verified | P:51 |
| [communication.bandwidth-baselines](../../knowledge/03-communication/bandwidth-baselines.md) | reference | source_checked | P:53 |
| [communication.bandwidth-degradation-triage](../../knowledge/03-communication/bandwidth-degradation-triage.md) | procedure | source_checked | P:53 |
| [communication.rdma-baseline-and-congestion-triage](../../knowledge/03-communication/rdma-baseline-and-congestion-triage.md) | procedure | not_verified | P:53 |
| [data-storage.checkpoint-integrity-evidence](../../knowledge/04-data-storage/checkpoint-integrity-evidence.md) | concept | source_checked | F:47 |
| [data-storage.checkpoint-slow-io-triage](../../knowledge/04-data-storage/checkpoint-slow-io-triage.md) | procedure | source_checked | P:52 |
| [data-storage.data-starvation-triage](../../knowledge/04-data-storage/data-starvation-triage.md) | procedure | source_checked | P:52 |
| [data-storage.storage-client-backend-recovery](../../knowledge/04-data-storage/storage-client-backend-recovery.md) | procedure | source_checked | F:47 |
| [data-storage.storage-workload-baselines](../../knowledge/04-data-storage/storage-workload-baselines.md) | reference | source_checked | P:49 |
| [data-storage.training-data-path](../../knowledge/04-data-storage/training-data-path.md) | concept | source_checked | P:52 |
| [cluster-platform.accelerator-sharing-and-isolation](../../knowledge/05-cluster-platform/accelerator-sharing-and-isolation.md) | concept | source_checked | P:55 |
| [cluster-platform.contention-capacity-validation](../../knowledge/05-cluster-platform/contention-capacity-validation.md) | procedure | not_verified | P:55 |
| [cluster-platform.control-plane-recovery](../../knowledge/05-cluster-platform/control-plane-recovery.md) | procedure | source_checked | M:58、F:46 |
| [cluster-platform.node-drain-resource-reclamation](../../knowledge/05-cluster-platform/node-drain-resource-reclamation.md) | procedure | not_verified | M:58、F:45 |
| [cluster-platform.platform-change-and-rollback](../../knowledge/05-cluster-platform/platform-change-and-rollback.md) | procedure | not_verified | M:52、F:46 |
| [training.checkpoint-state-consistency](../../knowledge/06-training/checkpoint-state-consistency.md) | concept | source_checked | F:48 |
| [training.checkpoint-state-recovery-triage](../../knowledge/06-training/checkpoint-state-recovery-triage.md) | procedure | source_checked | F:48 |
| [training.elastic-training-and-membership](../../knowledge/06-training/elastic-training-and-membership.md) | concept | source_checked | F:48 |
| [training.gpu-npu-precision-difference-triage](../../knowledge/06-training/gpu-npu-precision-difference-triage.md) | procedure | source_checked | M:63 |
| [training.mixed-precision-and-convergence](../../knowledge/06-training/mixed-precision-and-convergence.md) | procedure | source_checked | M:64 |
| [training.performance-analysis](../../knowledge/06-training/performance-analysis.md) | procedure | source_checked | P:49、P:72 |
| [training.performance-regression-source-case](../../knowledge/06-training/performance-regression-source-case.md) | case | source_checked | P:54 |
| [training.slow-rank-triage](../../knowledge/06-training/slow-rank-triage.md) | procedure | source_checked | P:54 |
| [inference.capacity-and-autoscaling](../../knowledge/07-inference/capacity-and-autoscaling.md) | procedure | source_checked | P:54 |
| [inference.execution-and-kv-cache](../../knowledge/07-inference/execution-and-kv-cache.md) | concept | source_checked | P:54 |
| [inference.latency-metrics](../../knowledge/07-inference/latency-metrics.md) | reference | source_checked | P:49 |
| [inference.model-loading-and-readiness](../../knowledge/07-inference/model-loading-and-readiness.md) | procedure | source_checked | F:44 |
| [inference.output-quality-evaluation](../../knowledge/07-inference/output-quality-evaluation.md) | procedure | source_checked | M:65、F:43 |
| [inference.quantization-and-quality](../../knowledge/07-inference/quantization-and-quality.md) | concept | source_checked | M:65 |
| [inference.release-and-recovery](../../knowledge/07-inference/release-and-recovery.md) | procedure | source_checked | F:44 |
| [inference.routing-and-flow-control](../../knowledge/07-inference/routing-and-flow-control.md) | concept | source_checked | P:54 |
| [reliability.correlated-failure-source-case](../../knowledge/08-reliability/correlated-failure-source-case.md) | case | source_checked | F:41 |
| [reliability.evidence-and-hypotheses](../../knowledge/08-reliability/evidence-and-hypotheses.md) | concept | source_checked | P:67、F:43 |
| [reliability.mitigation-and-recovery-principles](../../knowledge/08-reliability/mitigation-and-recovery-principles.md) | procedure | source_checked | F:37、F:41 |
| [reliability.postmortem-and-knowledge-update](../../knowledge/08-reliability/postmortem-and-knowledge-update.md) | procedure | source_checked | F:50 |
| [reliability.reliability-metrics-and-recovery-loss](../../knowledge/08-reliability/reliability-metrics-and-recovery-loss.md) | reference | source_checked | F:49 |
| [reliability.silent-errors-and-integrity](../../knowledge/08-reliability/silent-errors-and-integrity.md) | concept | source_checked | F:43 |
| [path.platform.amd](../../paths/platforms/amd.md) | path | — | P:66、F:62 |
| [path.platform.ascend](../../paths/platforms/ascend.md) | path | — | P:66、F:62 |
| [path.platform.nvidia](../../paths/platforms/nvidia.md) | path | — | P:66、F:62 |
| [path.task.environment-installation](../../paths/tasks/environment-installation.md) | path | — | M:39 |
| [path.task.fault-recovery](../../paths/tasks/fault-recovery.md) | path | — | P:66、M:78 |
| [path.task.inference-triage](../../paths/tasks/inference-triage.md) | path | — | F:62 |
| [path.task.migration-and-upgrade](../../paths/tasks/migration-and-upgrade.md) | path | — | P:65、F:61 |
| [path.task.node-acceptance](../../paths/tasks/node-acceptance.md) | path | — | M:57 |
| [path.task.performance-optimization](../../paths/tasks/performance-optimization.md) | path | — | M:77、F:60 |
| [path.task.selection-and-capacity](../../paths/tasks/selection-and-capacity.md) | path | — | F:61 |
| [path.task.training-triage](../../paths/tasks/training-triage.md) | path | — | F:62 |

## 附录 B：附带核对的既有导航页快照

本表记录本次读取的工作区状态，部分页面包含其他会话已存在的未提交修订；不是本会话修订清单。行数按换行符计，SHA-256 按原始字节计算。

| 页面 | 行数 | SHA-256 |
|---|---:|---|
| [README.md](../../README.md) | 158 | `4c2e54298f2693173dae66377124c90c4481fc4d5d01fe7efde09621c9a71874` |
| [knowledge/00-overview/index.md](../../knowledge/00-overview/index.md) | 69 | `365231c7cc00790fc3bde9064f0ddf7513c22429f87ed5337e272dde829a8a3f` |
| [paths/platforms/nvidia.md](../../paths/platforms/nvidia.md) | 208 | `fe49690a0ffe68e8ad5eef7c8e1e361e4adfe10b7870b0fdc2c5bddf2e9c05c6` |
| [paths/platforms/ascend.md](../../paths/platforms/ascend.md) | 228 | `79a8e5e9a325dd8d9b655cebbcde3694357d510fc913090ae59ec9a48c887fea` |
| [paths/platforms/amd.md](../../paths/platforms/amd.md) | 125 | `842715335cbd95ab56926a52d2e8af968157065b693211c07bfc13ab66e214a1` |
| [paths/tasks/training-triage.md](../../paths/tasks/training-triage.md) | 169 | `ec072b7b433c88e5d9d24a95e3ac15383b164a761a8aab8088c37589f838b1f4` |
| [paths/tasks/inference-triage.md](../../paths/tasks/inference-triage.md) | 143 | `569e212bf7d4348651d3e1247ff4b706a963806b362b4303162cc1162a2e86e7` |
| [paths/roles/reading-by-role.md](../../paths/roles/reading-by-role.md) | 113 | `ae0d71db96c1ce143d41da146a15e8a49c04c198e0dcf6dd5d7fbe63f3109ce8` |
| [paths/tasks/environment-installation.md](../../paths/tasks/environment-installation.md) | 79 | `b27323432b1ec86f892a91122d681a8af382f08be36fcebe2ee3b17cf6ca3e6e` |
| [paths/tasks/node-acceptance.md](../../paths/tasks/node-acceptance.md) | 78 | `e9053d8d0efa5f9f6ec7684b9f86a67e188f6349299e9acc7038b12150d79d2c` |

