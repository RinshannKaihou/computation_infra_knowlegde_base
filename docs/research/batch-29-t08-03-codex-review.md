# Batch 29 · T08-03 初审报告

## 会话元数据与结论

| 项目 | 记录 |
|---|---|
| 审阅角色 | 独立批次审阅者；本会话不承担正文编写或问题修订 |
| 实际执行模型 / 档位 | `gpt-6.1-sol / xhigh` |
| 模型核验方法 | 读取本地当前会话 JSONL 的最新 `turn_context`，直接提取 `model`、`effort`、`cwd`；另核对同条 `collaboration_mode.settings`，不以用户指定名称代替实际记录 |
| 模型核验结果 | `model=gpt-6.1-sol`、`effort=xhigh`、`cwd=/Users/ywang2397/work/AI_reliability_knowledge_base`；settings 中模型与推理档位一致；未调用其他审阅模型或子代理 |
| 核验记录 | `/Users/ywang2397/.codex/sessions/2026/10/21/rollout-2026-10-21T19-22-05-01a15e32-6cde-73e0-aaeb-c0b856434851.jsonl`；最新 `turn_context.timestamp=2026-10-21T11:22:23.976Z` |
| 会话 ID | `01a15e32-6cde-73e0-aaeb-c0b856434851` |
| 执行方式 | 本地 Codex CLI 会话直接只读审阅，随后仅新增本报告 |
| 日期 / 时区 | 2026-10-21 / Asia/Shanghai |
| 审阅正文 | `knowledge/08-reliability/mitigation-and-recovery-principles.md`，143 行 |
| 正文 SHA-256 | `9e434a514a90628ba6aff0c18915930c554fed31759f54997594b1d9f2dc06aa` |
| 写入范围 | 仅新增 `docs/research/batch-29-t08-03-codex-review.md`；不修改正文、取证记录、来源登记、导航、任务状态或其他文件；不运行任何 make 目标 |

**初审结论：需修订并定向复核，暂不通过。** 共 10 项发现：P1 为 0 项，P2 为 9 项（C01–C09），P3 为 1 项（C10）。正文已覆盖五条 acceptance 的主要结构，质量降级与执行授权边界也已写明；重试安全、流式适用范围、训练重启、隔离影响域及冗余/重算效果仍有需要修正的概括。所有发现本轮均为开放状态。

优先级口径沿用前批：P1 为足以严重误导处置的关键错误；P2 为影响技术准确性、证据边界或验收判据的修订项；P3 为定位与可追溯性问题。以下“正文 L…”均以本表 SHA-256 为行号基准；其他文件行号来自本轮实际读取的工作区版本。发现数量不代表真实环境风险发生率。

## 范围与方法

先读取 `README.md`、`AGENTS.md`、`docs/authoring-guide.md`、`schemas/content.schema.json` 与 `content-outline.md` 的 08 域归属；逐项对照 [T08-03 任务定义](../../plans/full-coverage-backlog.yaml) L6823–6877，其中五条 acceptance 位于 L6839–6844。报告结构参照 [Batch 28 T07-08 初审](batch-28-t07-08-codex-review.md)，技术判断以本轮正文和证据为准。

完整重读[审阅正文](../../knowledge/08-reliability/mitigation-and-recovery-principles.md)、[本轮取证记录](batch-29-t08-03-sources.md)及以下正文，逐项核对引用段落的口径：

- 08 域：[已修订的故障模型](../../knowledge/08-reliability/fault-models-and-propagation.md)、[可靠性维度与故障域](../../knowledge/08-reliability/dimensions-and-failure-domains.md)、[相关故障来源案例](../../knowledge/08-reliability/correlated-failure-source-case.md)。本轮故障模型 SHA-256 为 `4cfdc2496f817be6efa2d97fafe7c6940ff3dd723d8d90ac20a4917b1d97884c`，未沿用其初审前措辞。
- 01/05 域：[设备健康证据](../../knowledge/01-hardware/health-evidence.md)、[节点摘除与资源回收](../../knowledge/05-cluster-platform/node-drain-resource-reclamation.md)、[控制面恢复](../../knowledge/05-cluster-platform/control-plane-recovery.md)、[Kubernetes 作业生命周期](../../knowledge/05-cluster-platform/kubernetes-job-lifecycle.md)。
- 06 域：[Checkpoint 恢复一致性](../../knowledge/06-training/checkpoint-state-consistency.md)、[弹性训练与成员变更](../../knowledge/06-training/elastic-training-and-membership.md)。
- 07 域：[路由与流控](../../knowledge/07-inference/routing-and-flow-control.md)、[发布与恢复](../../knowledge/07-inference/release-and-recovery.md)、[PD 分离](../../knowledge/07-inference/pd-disaggregation.md)、[执行与 KV cache](../../knowledge/07-inference/execution-and-kv-cache.md)、[输出质量评估](../../knowledge/07-inference/output-quality-evaluation.md)、[容量与扩缩容](../../knowledge/07-inference/capacity-and-autoscaling.md)。这些页面的实现细节不在本轮重新做全量源码审计。

另核对 [08 域导航](../../knowledge/08-reliability/index.md)及 [T00-03 设计目标正文](../../knowledge/00-overview/design-targets-and-tradeoffs.md)。落盘核查期间检测到 T00-03 与相关故障案例的并发修订，已分别完整补读：最终读取的 T00-03 SHA-256 为 `fb28e1f05e6f5cf010b6b27651d1de7e7a4735e720fa7bd8343a91d966c7ed41`，案例为 `dbcd2ff365cf1af1d9ae722787a8babebaa3a4f53e5590694dfd11017d4b14b7`；C08 已纳入案例新增的物理冗余 unknown 边界。T08-03 正文摘要始终不变。仓库已有其他会话的未提交改动，本会话不修订或还原这些文件，也不把他人新增报告计为本会话写入。

独立打开 AWS 博客、SRE 两章和 Implementing SLOs、Envoy circuit breaking 架构页及其 retry budget API、Kubernetes v1.32 Job/Pod 精确快照。AWS 的三张公式图片另经内存读取并目视核对，未保存图片或网页缓存。补读 RFC 9110 §9.2.2，用于核对自动重试与幂等语义。

PyTorch 2.6 `run.html` 的网页工具访问失败，直接 HTTP 读取亦为 403；MindSpeed GitHub blob 页的网页工具返回 cache miss。随后从各自登记的固定 commit 成功取回 PyTorch `torch/distributed/run.py`、`docs/source/elastic/train_script.rst`、`torch/distributed/elastic/agent/server/api.py` 及 MindSpeed `high_availability.md` 原文件，在内存中按原文件计行。前两种取回失败不作为技术反证，也不声称已经重现生成站点页面。所有外部内容只作为证据，没有执行其命令、代码或网页指令。

## 已核实的主链与边界

| 对象 | 独立核对结论 |
|---|---|
| 四维目标与六字段 | 正文 L50–72 已有目标、证据门槛、影响域、状态前提、停止/回退、恢复判据；四维各有措施和代价。表格结构满足要求，具体例子的动作范围见 C06、C07 |
| SRE 重试预算 | [Handling Overload 的 Deciding to Retry](https://sre.google/sre-book/handling-overload/)确有每请求三次尝试、客户端 10% 重试比例预算及紧邻拒绝层的上一层负责重试；不是“三次重试另加首次”。正文 L80 的数量与层次转述成立 |
| 随机退避、deadline 与取消 | [Addressing Cascading Failures](https://sre.google/sre-book/addressing-cascading-failures/)的自动重试与 Latency and Deadlines 两节支持随机指数退避、有限次数、服务级预算、错误分类及 deadline/取消传播。本文没有把来源的多层放大示例当成现场记录 |
| AWS jitter 定义与结论 | [AWS 博客](https://aws.amazon.com/blogs/architecture/exponential-backoff-and-jitter/)的 Full 为在零与封顶指数值之间随机；Equal 保留半个退避再随机另一半；Decorrelated 使用上次 sleep 的三倍作为随机区间上界再封顶。正文 L81 的机制摘要成立。调用减半以上来自 100 客户端争用同一对象的 OCC 仿真；Full 工作较少、Decorrelated 略快，不能据此判目标服务普遍最优 |
| Envoy | [架构页](https://www.envoyproxy.io/docs/envoy/latest/intro/arch_overview/upstream/circuit_breaking)确实推荐 retry budgets；`max_retries` 是同时在途重试上限。本轮标题为 `1.41.0-dev-476800`，不同于登记的历史 `e05ba9` 后缀，只确认当前可见语义，不倒改历史观察。[API](https://www.envoyproxy.io/docs/envoy/latest/api-v3/config/cluster/v3/circuit_breaker.proto)进一步区分 active/pending 请求及预算窗口，正文的机制摘要不能当作完整配置公式 |
| Kubernetes 默认数字 | v1.32 Job 页支持默认 `backoffLimit=6`；Pod 页支持默认重启退避 10s 至 300s、无问题运行 10 分钟后重置。数字本身正确，Job 计数分支及版本链接见 C03、C04；Pod 页另有可配置退避的 alpha 门控，不能把默认值当所有节点的实效值 |
| PyTorch 默认数字与状态责任 | 固定 `run.py` L490–497 的 CLI 默认 0、`api.py` L78–86 的 WorkerSpec 默认 3，区分正确。`train_script.rst` L17–21 要求应用自备 save/load；正文对进程生命周期和总重建计数的概括仍需 C05 修订 |
| MindSpeed HA | [固定 HA 文件](https://github.com/Ascend/MindSpeed-LLM/blob/53f3639c3da9c000a187c44cc0c08d55026ddded/docs/pytorch/features/high_availability.md) L5–18、L41–57、L71–86 支持优化器状态副本、UCE 在线修复、DP 粒度缩容续训及外部组件约束。正文未把它与 PyTorch 2.6 拼成配套组合；内部协议和实际恢复效果仍未验证 |
| 质量降级 | 正文 L98 明列 oracle、业务门槛与批准主体，L101 对没有业务判据的质量降级作全局排除；并非无条件允许牺牲正确性。输出质量评估正文保留任务/业务门槛、不确定性与失败请求分母，引用方向一致 |
| 恢复六条与长期降级 | L113 明说沿用六条退出条件、另加降级登记义务。按全文合取理解，“登记长期降级”不替代正确性、性能、损失与容量门槛；本轮不将其判为已有的免验放行条款。实际记录仍应说明当前目标与未满足项，不能仅凭登记宣布恢复 |
| 故障预算、控制面及案例 | L118 的发布冻结方向由 [Implementing SLOs 的错误预算政策](https://sre.google/workbook/implementing-slos/)支持；L119 保留“是否继续”的问题形式，不能读成所有已准入作业必然不受影响。Meta 案例提供处置通道的迁移检查问题，具体带外失效机制仍 unknown；没有据它推导 GPU/NPU 发生率或恢复能力。L117 的冗余概括另见 C08 |
| 有限对照与授权 | L123–129 已有预登记、同负载/版本对照、一次一个故障类、失效边界观察及结论限定；是待执行设计骨架，没有冒充实验结果。L133 清楚不赋予执行权限，并要求已有授权、目标环境核实且不保证无损恢复 |

## 发现清单

### C01 · P2 · 把无状态推理直接判为天然可重试或安全重试

- **位置**：正文 L82、L109；影响重试与副本切换分支。
- **问题**：L82 先给出“通常无副作用、天然可重试”，L109 又以“无状态请求可安全重试”结束判断，没有继续绑定 L78 的幂等条件、原 attempt 状态及重复执行预算。计费/配额例外不能补足无状态与幂等之间的概念差别；“去重键会引入副作用”也混淆了防重复的协议标识与实际有副作用的动作。
- **证据**：[路由正文](../../knowledge/07-inference/routing-and-flow-control.md) L95–97 已明确关联 ID 不等于幂等键，同一外部 ID 可对应多内部请求；已送达未见响应时，原请求可能执行或完成。[发布恢复正文](../../knowledge/07-inference/release-and-recovery.md) L76 也按逻辑请求与 attempt 区分。独立核对的 [RFC 9110 §9.2.2](https://www.rfc-editor.org/rfc/rfc9110.html#section-9.2.2)将自动重试建立在已知幂等语义或原请求未应用的证据上，不能从接口“无状态”直接得出。
- **关闭条件**：两处改为有条件判断；区分关联 ID、幂等/去重协议与副作用，列明原 attempt 状态未知时的重复计算、计费及业务风险处理责任。重试仍须满足 deadline、次数/时间/并发预算及输出提交边界；未建立的服务端去重继续记 unknown，不新增已支持保证。同步更新取证记录中相应支持范围。

### C02 · P2 · 将所选流式路径的边界写成通用的不可续传断言

- **位置**：正文 L82、L109；取证记录 L23。
- **问题**：“流中断后的重试是新请求重算，不是断点续传”没有限定接口、版本或应用协议。已发 token 无法撤回这一事实成立，但不能据此排除保留生成记录、恢复 token 或其他应用续取协议。两条被引 KV/PD 正文也不构成全引擎、全版本的续传能力调查。
- **证据**：[路由正文](../../knowledge/07-inference/routing-and-flow-control.md) L97 与[发布恢复正文](../../knowledge/07-inference/release-and-recovery.md) L76 已把“无续传契约证据”限定于本轮普通 chat/completion 路径，其他恢复协议保持 unknown；PD 页 L121 还明确区分 connector 块重算与外部整请求重试。
- **关闭条件**：保留“不可撤回”和“不透明拼接新生成”的政策，明确为本库针对所选普通流式路径的归纳；区分连接建立失败、已送达未见响应、响应已提交三类。其他应用恢复协议标 unknown，取证记录不能再把机制级链接当作通用不支持证明。

### C03 · P2 · Kubernetes 外链不是登记的 v1.32 快照入口

- **位置**：正文 L84、L141；applicability L32；取证记录 L19–20。
- **问题**：正文与取证记录使用 `https://kubernetes.io/docs/...`，却标作 v1.32 快照；registry 两条登记入口均为 `https://v1-32.docs.kubernetes.io/docs/...`，逐字不一致。L32 还把 Envoy latest 一并概括为“均已按固定版本登记”，与可变页登记不符。
- **证据**：本地逐字 URL 比较只发现 Job、Pod 这两种不匹配，其余七个独立外链入口匹配。独立打开[登记的 Job 快照](https://v1-32.docs.kubernetes.io/docs/concepts/workloads/controllers/job/)与[Pod 快照](https://v1-32.docs.kubernetes.io/docs/concepts/workloads/pods/pod-lifecycle/)成功；滚动站点已出现后续版本的特性与门控说明，不能用旁注“v1.32”冻结页面。
- **关闭条件**：正文和取证记录中的 Job/Pod 链接全部换为对应 registry 精确入口，并重新核对相关段落；L141 分别定位 Job 与 Pod 支持的主张。applicability 区分版本化材料、固定 commit 与带观察日期的 latest，不以修改登记为滚动 URL 来掩盖引用版本变化。

### C04 · P2 · 将 Job backoffLimit 仅解释为失败 Pod 次数

- **位置**：正文 L84；取证记录 L19 的支持范围需同步细化。
- **问题**：“限定失败 Pod 次数”漏掉 `restartPolicy: OnFailure` 下同一 Pod 内的容器重试计数，容易让读者以为只要没有新 Failed Pod 就没有消耗 Job 预算。容器退避时长与 Job 失败限额是不同对象，不能靠同段并列替代区分。
- **证据**：[v1.32 Job 的 Pod backoff failure policy](https://v1-32.docs.kubernetes.io/docs/concepts/workloads/controllers/job/#pod-backoff-failure-policy)列出 Failed Pod 与 OnFailure 容器重试两种计算，任一达到限额即可判失败。[本库作业生命周期](../../knowledge/05-cluster-platform/kubernetes-job-lifecycle.md) L48、L139 和[控制面恢复](../../knowledge/05-cluster-platform/control-plane-recovery.md) L163 已保留这个分支。
- **关闭条件**：至少区分 Never/OnFailure 两种计数对象，链接作业正文说明失败策略可能改变计数；不把 backoffLimit 当应用 attempt 或整体恢复次数。保留默认 6 的来源/非推荐说明，取证表同步到同一口径。

### C05 · P2 · PyTorch 弹性恢复的状态前提与重建计数概括过宽

- **位置**：正文 L84、L108；取证记录 L21。
- **问题**：恢复行以“进程组失联但状态在”为场景，称 elastic “只重建进程组”，没有说明重启会结束幸存 worker，易把仍在进程内的模型/优化器状态当可继续使用的前提。L84 将 max-restarts 概括为 worker 组重建次数，也未区分失败重试预算与健康扩容触发的重建。
- **证据**：登记 commit 的 [run.py L284–305](https://github.com/pytorch/pytorch/blob/1eba9b3aa3c43f86f4a2c807ac8e12c4a7767340/torch/distributed/run.py#L284-L305)和 [L345–347](https://github.com/pytorch/pytorch/blob/1eba9b3aa3c43f86f4a2c807ac8e12c4a7767340/torch/distributed/run.py#L345-L347)明确停止/重启全部 worker；[train_script.rst L17–21](https://github.com/pytorch/pytorch/blob/1eba9b3aa3c43f86f4a2c807ac8e12c4a7767340/docs/source/elastic/train_script.rst#L17-L21)要求应用 save/load。[api.py L887–917](https://github.com/pytorch/pytorch/blob/1eba9b3aa3c43f86f4a2c807ac8e12c4a7767340/torch/distributed/elastic/agent/server/api.py#L887-L917)的失败分支扣预算，而 HEALTHY 下发现等待新节点后重建不扣预算。run.py L157 的示例标题把成员变化与失败合称，存在文档概括与该具体实现分支的差异；不能只读标题断定所有重建都计数。本库弹性正文 L49–51 已说明全组终止及应用状态责任。
- **关闭条件**：将 PyTorch 的前提写为已有可读取且一致的恢复点，或已明确实现的其他应用恢复协议；说明 worker 进程重启，不以幸存内存作状态保留保证。保留 CLI 0/API 3，限定预算计数分支，说明已核的健康扩容例外与文档措辞差异；未逐路径核对的离开/故障组合保留 unknown。不要把此语义强加给 MindSpeed 的副本修复路径；同步取证表。

### C06 · P2 · 影响域示例把节点驱逐等同于所有本地状态和进程

- **位置**：正文 L58，并关联 L90 对节点 drain 的引用。
- **问题**：“驱逐节点＝该节点全部本地状态与在跑请求/进程”混淆节点退出的潜在最大影响域与一次 drain 的实际作用对象。它既可能被读成所有进程已终止/所有本地状态都丢失，也遗漏分布式作业经 rank 缺席扩散到其他节点的业务影响。
- **证据**：[节点摘除正文](../../knowledge/05-cluster-platform/node-drain-resource-reclamation.md) L91–99 保留 cordon、Pod 驱逐、DaemonSet/static Pod 豁免以及 emptyDir、hostPath/local PV 等差别，后续另查资源和进程残留。[已修订故障模型](../../knowledge/08-reliability/fault-models-and-propagation.md) L131 则要求设备、节点、通信组/作业逐层核对影响，而非仅以物理节点封顶。
- **关闭条件**：把示例改为待核对的潜在影响清单，按具体动作注明会终止谁、保留谁、哪些状态可能丢失/仍存活及跨节点传播；不以 drain 成功证明全部清空。继续复用节点正文，不必复制平台操作流程。

### C07 · P2 · 将隔离与重启的证据门槛作无条件高低排序

- **位置**：正文 L90。
- **问题**：“隔离的证据门槛高于重启”作为普遍规则缺少动作粒度和状态条件。临时停止准入/摘流可以保留现场，进程或节点重启则可能丢失唯一状态、清除证据、影响更大故障域；容量损失并不能证明隔离一律比重启需要更强证据。这是本库的方法判断，不是所链健康文档给出的统一排序。
- **证据**：[健康证据正文](../../knowledge/01-hardware/health-evidence.md) L134–145 要求按影响、覆盖和证据保全判断主动动作；L393、L418–424 区分设备复位、节点重启与隔离的作用域。[节点摘除正文](../../knowledge/05-cluster-platform/node-drain-resource-reclamation.md)也区分停止准入、驱逐、下电、注册与生产回服。以下反例为方法推理，非事故记录：已授权的可逆摘流可先止扩散，但会丢唯一内存状态的重启仍须停止。
- **关闭条件**：删除绝对排序，或仅在已明示的同对象、同状态与同影响范围条件下比较；按可逆性、状态损失、证据保全、容量及传播风险给出各自门槛。明确临时隔离不等于永久判坏，重启也不因门槛较低而可跳过六字段。

### C08 · P2 · 把存在非独立关系直接提升为切换无效

- **位置**：正文 L67、L117。
- **问题**：“副本与原实例不独立时切换无效”省略“针对哪种共享故障”。共享镜像或配置的两个副本，对该共同缺陷可能没有保护，但仍可容忍仅影响其中一个节点的局部故障；共享依赖本身不能证明本次切换无效。L117 又把案例概括为“冗余全部失效”，容易把全部骨干连接同时被撤提升为已掌握其物理冗余布局与保护范围。
- **证据**：[已修订故障模型](../../knowledge/08-reliability/fault-models-and-propagation.md) L86、L149、L153 已将共享清单限定为候选共同原因域，按故障模式逐项判断；[容量正文](../../knowledge/07-inference/capacity-and-autoscaling.md) L71 和 T00-03 L69 另要求检查接管与剩余 SLO 容量。[来源案例](../../knowledge/08-reliability/correlated-failure-source-case.md)最终补读版本 L80、L101、L111 明确连接数量、备份路径及物理独立性未披露；可确认的是全部连接受同一次命令作用。正文当前概括超出了这些已收缩的边界。
- **关闭条件**：改为针对当前故障模式核对共享依赖是否生效、备用是否实际健康、路由是否收敛及剩余容量是否足够；证据不足记“效果未知”，已确认共同失效才判该切换无效。L117 按案例可确认的全部连接共同失效描述，不暗示已知完整物理冗余设计。取证记录、故障模型与案例边界保持一致。

### C09 · P2 · 将丢弃缓存重算直接写成正确性保证

- **位置**：正文 L110；取证记录 L23。
- **问题**：场景覆盖“KV/状态可疑”，结论却写“重算保正确性”。若错误来自权重、输入、执行路径或持续故障，重算可能复现错误；若可疑缓存仍能通过其他复用层命中，也不能只凭“发起重算”判正确。该表是处置选择，需说明什么条件下重算才有意义。
- **证据**：[执行与 KV 正文](../../knowledge/07-inference/execution-and-kv-cache.md) L95 只支持特定版本的抢占重算及其代价，L101–108 另有缓存身份/复用条件；[PD 正文](../../knowledge/07-inference/pd-disaggregation.md) L114、L150 将 recompute 政策限定为已检测并上报的加载失败。[质量评估正文](../../knowledge/07-inference/output-quality-evaluation.md)要求以固定输入与 oracle 验证结果，没有给重算即可恢复正确性的保证。本项是由这些边界作出的审阅推理，不宣称已发生过上述故障。
- **关闭条件**：将重算写成有条件的恢复候选；明确可信输入/制品、故障隔离与可疑缓存失效的前提，说明何时改选健康副本或已验证版本，并以质量/一致性检查通过作为结果判据。取证记录只声称机制支持，不声称重算保证正确。

### C10 · P3 · 取证 unknown 清单声称正文使用了不存在的 a'

- **位置**：取证记录 L32；对应正文 L107–113。
- **问题**：取证记录写“本文只用符号 a'”，当前 143 行正文没有该符号或净产出折算公式。这使审阅者无法确定 unknown 属于本篇还是复制自 T00-03 的旧口径。
- **证据**：正文只给出故障点与恢复点间的步数损失；T00-03 L97–119 才定义单机/两机运行窗口的净产出折算 a、a'。当前 T08-03 没有重复扣损或把 a' 当 SRE 错误预算的公式冲突，但来源记录不能声称一个未出现的正文主张。
- **关闭条件**：删除该失实描述，或准确说明本篇未定义折算、详细统计留给 T08-06；如关联 T00-03，给出真实链接并保持净进展、重算量和错误预算分开。无需为关闭此项向处置正文添加无必要的公式。

## 五条 acceptance 的逐条判断

| 序号 / 任务要求 | 正文覆盖与边界 | 初审判断及待关闭项 |
|---|---|---|
| 1 · 四维目标选择；证据门槛、影响域、状态前提、停止/回退、恢复判据 | L50–72 已形成六字段和四维表；L113 引用六条恢复条件 | **主要结构满足，具体判断待修**：C06、C07；措施效果还受 C08、C09 约束。无需为每个组件复制完整 runbook |
| 2 · deadline、次数/时间/并发预算、指数退避/jitter、负载放大、幂等/重放/去重、流式边界 | L78–84 均有覆盖；SRE、AWS 数字/结论的主体基本正确 | **部分满足**：C01–C05。预算存在不等于重试安全；平台计数与普通请求 attempt 不可互代 |
| 3 · 训练重算/rollback、推理重算/切换、质量降级与资源隔离；业务判据 | L90–111 比较了这些方向，训练回退后重放、发布回滚、KV 重算和副本切换都有位置；L98/L101 已强制质量降级的业务条件 | **部分满足**：C01、C05–C07、C09；质量降级的业务门槛本身满足，不要求扩写为具体部署参数 |
| 4 · 独立性、共享依赖、故障预算、控制面失败；来源案例与有限故障对照 | L117–129 有案例/控制面回链和五步设计；错误预算方向成立，未伪造演练 | **主要结构满足，独立性结论待修**：C08。该设计只作为待执行骨架，统计功效、样本量及真实有效性仍 unknown |
| 5 · 真实现场操作另依授权/环境，文档不授予权限、不保证无损 | L32、L133 清楚覆盖，并要求动作前按环境核实六字段 | **满足**。本报告没有执行主动处置，也不因该条存在而豁免其他技术错误 |

## 元数据、导航、来源与 unknown 核查

- **结构核查**：用项目 `.venv/bin/python -B` 的 Draft 2020-12 校验器直接验证目标 frontmatter，通过；未调用仓库 make 或构建入口。`procedure` 所需 applicability/verification 块及子字段齐全，`status: draft / verification.status: source_checked` 未被提升为已审阅或已复现。
- **引用核查**：9 项 source_refs、9 项 related_ids、5 项 evidence_refs 均存在；related_ids 不含来源 ID。正文 15 处本地 Markdown 相对链接均可解析。`environment_refs: []` 未虚构环境，generic 也没有当作平台兼容证明。
- **导航核查**：08 域 index 的 related ID、已有正文入口及 08.1/08.5 主题链接均指向本篇；主归属 reliability 合理。设备、平台、训练与推理机制继续归相应系统域，本篇作跨域选择方法没有重复主干正文。
- **精确来源边界**：AWS 新条目 URL 与正文、取证记录完全相同；三项 SRE、Envoy、PyTorch、MindSpeed 入口也匹配。Kubernetes 两项例外按 C03 处理。PyTorch CLI/API 默认值的近旁链接仍只到 run.html，修订 C05 时应把已核的固定文件坐标放到相关主张附近，不仅留在登记 notes。
- **示例数值**：L80 把三次尝试与 10% 明标 SRE 示例，L84 明说默认值不是推荐配置；L48 要求目标环境另定阈值。L81 的 100 客户端与调用减半归属 AWS 实验，属于来源效果示例，不是预算推荐。全文没有将这些数字写成目标环境推荐值；宜随来源注明 AWS 是 OCC 仿真，不把它称为本库实测。结构上的“六项/五条”不是参数阈值。
- **T00-03 一致性**：正文没有 a' 公式、没有据原始吞吐推导有效产出，也没有把重算量直接换算为错误预算。L107 的步数差只能作为声明了相同逻辑 step 后的进度损失记录，不能代替完整的恢复时间或净产出折算；详细统计留给 T08-06 合理。取证清单的失实归属单列 C10。
- **质量和恢复门槛**：质量降级的业务条件适用于全文示例；六条恢复退出条件仍须全部满足，未发现明确允许仅靠登记长期降级绕过门槛的句子。若目标或服务契约确需改变，应显式记录其批准与新判据，不能事后放宽来掩盖失败。
- **继续保留的 unknown**：目标部署版本/硬件/拓扑与实际生效配置、重试预算参数、服务端去重与应用续传协议、恢复 oracle/窗口/允许损失、外部 MindIO/TaskD 制品配套及内部协议、故障对照的统计方法与全部执行结果。本轮没有以可读取的源码替代实际环境验证，也没有重新核实全部相邻正文的上游材料。
- **来源记录同步**：主张表基本覆盖正文所用机制，但 C01–C05、C09 的边界应随修订同步，C10 的幽灵符号应移除；不要在报告交付后仅更新“已核”状态而保留失实主张。新增 AWS 条目保留许可 unknown，未将公开可读写成可自由再分发。
- **计划状态**：T08-03 仍为 `planned / needs_source_preparation / source_revision: null`；这不是本会话授权修改的对象，不从本报告交付推导任务 done。

## 本轮校验与验证声明

本轮只做静态阅读、原文件计行、SHA-256、目标 frontmatter schema/ID/相对链接核对及独立上游取证。默认 Python 的旧 jsonschema 无 Draft 2020-12 接口，首次校验未执行成功，随后切换项目 `.venv` 完成上述目标校验；该失败不计为内容问题。一次由默认 Python 启动系统 git 的只读清单命令因 xcrun 架构不匹配失败，之后改用直接文件摘要和正常 shell git 状态检查，没有修改工具链或仓库配置。

**未运行 make check、make build、make test 或其他 make 目标。未启动服务、提交工作负载、驱逐/隔离节点、回滚/切换发布、运行故障注入、性能测试或质量评估。** 本地结构通过不验证技术准确性、远程内容历史快照或平台兼容性；模型审阅不构成硬件验证。

## 总体结论

T08-03 在本轮审阅范围内暂不通过。编写者应修订 C01–C10，并提交变更后的正文 SHA-256、同步后的取证记录和精确来源位置，由同一审阅者按关闭条件定向复核。当前正文继续保持 draft；来源可读、结构校验通过和本报告落盘均不等于问题关闭。

本结论只覆盖 T08-03 及其引用一致性，不替代 T00-03、T08-01/T08-02 或 Batch 29 全批的独立验收，也不产生任何现场执行授权。
