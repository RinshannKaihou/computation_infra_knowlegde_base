# Batch 30 · T08-07 初审报告

## 会话元数据与结论

| 项目 | 记录 |
|---|---|
| 审阅角色 | 独立批次审阅者；本会话不承担正文编写或问题修订 |
| 实际执行模型 / 档位 | `gpt-6.1-sol / xhigh` |
| 模型核验方法 | 读取环境变量 `CODEX_THREAD_ID` / `CODEX_SESSION_ID` 定位本会话 JSONL，并以本会话首条审阅进度消息交叉确认；读取该文件最新 `turn_context` 的 `model`、`effort`、`cwd`，不以配置默认值或其他同时运行的会话代替 |
| 模型核验结果 | `model=gpt-6.1-sol`、`effort=xhigh`、`cwd=/Users/ywang2397/work/AI_reliability_knowledge_base`；同条记录的 `collaboration_mode.settings.model/reasoning_effort` 一致，未观察到模型切换或回退 |
| 模型核验坐标 | `/Users/ywang2397/.codex/sessions/2026/10/21/rollout-2026-10-21T20-49-27-01a15e82-6922-76f3-9ae2-45caa968f18f.jsonl` L8；时间戳 `2026-10-21T12:49:57.914Z`；本会话首条进度消息位于 L13 |
| 会话 ID / turn ID | `01a15e82-6922-76f3-9ae2-45caa968f18f` / `01a15e82-6aa6-7041-84c3-426b924a4035` |
| 执行方式 | 当前本地 Codex CLI 会话直接审阅，`workspace-write`；未另启模型、OpenCode 或审阅子代理 |
| 日期 / 时区 | 2026-10-21 / Asia/Shanghai（UTC+08:00） |
| 审阅正文 | `knowledge/08-reliability/postmortem-and-knowledge-update.md`，`wc -l` 为 141 行 |
| 正文 SHA-256 | `7ebb951ff525d4ac04a11217e6ed6c089259ccde8c1a83d77eff0a751f356c52`（`shasum -a 256`） |
| 取证记录基准 | `docs/research/batch-30-t08-07-sources.md`，29 行；SHA-256 `68a7dca2e99ae5cd8701e51248128b54a1c46670e323b86f9376c926c2d83208` |
| 验收基准 | `plans/full-coverage-backlog.yaml` L7019–7059，五条 acceptance 位于 L7037–7041 |
| 写入范围 | 仅新增 `docs/research/batch-30-t08-07-codex-review.md`；不修改正文、取证记录、registry、导航、计划或构建产物 |

**初审结论：需修订并定向复核，暂不通过。** 共 5 项发现：P1 为 0 项，P2 为 3 项（C01–C03），P3 为 2 项（C04–C05）。主要问题是公开复盘映射包含无证据的事件、组件级证据保全描述缺少配套依据，以及维护链遗漏 catalog 的更新与检查闭环。所有发现均为开放状态。

优先级口径：P1＝足以严重误导处置的关键错误；P2＝影响技术准确性、证据边界或验收判据的必修事项；P3＝局部措辞、定位与可追溯性问题。以下正文行号均以上述 SHA-256 为基准。

## 审阅范围与独立取证

已先读 README、AGENTS、写作指南、内容 schema 与总目录 08 域划分，再完整重读正文和取证记录。独立打开用户列出的五条精确上游 URL；另打开本篇实际依赖的 Monitoring Distributed Systems、Cloudflare 外部观测及 registry 登记的 Meta 入口。GitHub 文件优先通过连接器按固定 commit 读取；网页只作证据。没有执行正文或上游材料中的命令。

| source_ref / 上游 | 本轮独立核对、revision 与许可边界 |
|---|---|
| `src.google.sre-postmortem-culture` | [Workbook 第 10 章](https://sre.google/workbook/postmortem-culture/)可读；核对无责文化、好坏复盘、负责人/优先级/跟踪与可验证行动项、及时发布和工具化参考。页面为 2018 年书籍章节、观察日期按本轮记录；页脚明示 CC BY-NC-ND 4.0，与新增 registry 口径一致。发布时限的转述需按 C05 收窄 |
| `src.google.sre-managing-incidents` | [Managing Incidents](https://sre.google/sre-book/managing-incidents/)可读；核对职责分离、实时事件文档、交接、宣布条件和优先恢复/保全证据。2017 年章节及页脚 CC BY-NC-ND 4.0 与 registry 一致 |
| `src.google.sre-effective-troubleshooting` | [Effective Troubleshooting](https://sre.google/sre-book/effective-troubleshooting/)可读；核对假设检验、证据保全、主动测试副作用和调查留痕；不支持正文新增的 NCCL 机制，见 C02。registry 保留 2026-09-29 的观察记录；其许可仍为保守的 unknown，本轮页面页脚可见 CC BY-NC-ND 4.0，不倒推作者历史读取情况 |
| `src.google.sre-monitoring-distributed-systems` | [Monitoring Distributed Systems](https://sre.google/sre-book/monitoring-distributed-systems/)可读；黑盒/白盒、症状/原因与观测局限可支撑字段设计的基础，具体“采集覆盖”表属于本文扩展。registry 的 2026-09-29 观察与 unknown 许可不构成已授权再分发声明；本轮页脚同样可见 CC BY-NC-ND 4.0 |
| `src.ascend.faultdiag-v26.1.1` | [固定文件](https://github.com/Ascend/mind-cluster/blob/44385c13d7b1d87def35f1604e8be4d16de6ca4e/docs/zh/faultdiag/ascend-faultdiag/05_usage/04_fault_diagnosis.md)可读，核对报告字段、性能诊断与展示上限。另沿 [v26.1.1 tag 对象](https://api.github.com/repos/Ascend/mind-cluster/git/tags/387a7f2b5f9ddfdbcdff0d8c85386fc68e2fe7fb)确认其指向登记 commit；固定 [LICENSE](https://github.com/Ascend/mind-cluster/blob/44385c13d7b1d87def35f1604e8be4d16de6ca4e/LICENSE)为 Apache-2.0。registry 只将根许可证登记为 partial，未把它扩大为所有附属材料的统一许可 |
| `src.meta.oct4-2021-postmortem` | 用户指定及正文使用的 [networking-traffic 入口](https://engineering.fb.com/2021/10/05/networking-traffic/outage-details/)可读，日期为 2021-10-05。registry 的 `/networking/` 入口本轮网页工具未能打开；两入口字符串不一致，见 C04。registry notes 的命令/审计工具、主动撤告、恢复风险与 unknown 边界较正文示例准确；未找到正文宣称的撤销失败或第二起事故。许可 unknown，保持链接与原创归纳 |
| `src.cloudflare.oct-2021-facebook-outage` | [Cloudflare 原页](https://blog.cloudflare.com/october-2021-facebook-outage/)可读；核对 15:51 UTC 开事故单、15:58 注意到 DNS 前缀撤告，以及恢复观测。其外部 BGP/DNS 观察与运营方内部机制分别取证；不把该页转述的运营方原因当成独立根因验证。registry 的单一事件与外部视角边界适当，许可 unknown |

为核实 C02，另打开 [PyTorch Flight Recorder 官方教程](https://docs.pytorch.org/tutorials/unstable/flight_recorder_tutorial.html)的启用及数据获取小节，以及 [PyTorch 2.14 ProcessGroupNCCL 环境变量页](https://docs.pytorch.org/docs/2.14/torch_nccl_environment_variables.html)相应表行；仅用作本轮补充反证，不替正文新增来源登记或平台配套声明。本地 Python 直接访问 SRE 页曾因 DNS 解析失败而未取回，随后网页工具读取成功；不把该工具失败判为原页失效。

## 已核实的主链与边界

| 对象 | 独立核对结论 |
|---|---|
| 事故记录主链 | L60–66 覆盖影响、时间线、身份与版本、采集覆盖、假设支持/反驳/未知、处置恢复及遗留风险。L64/L124 明确缓解成功与根因确认分开；这与 SRE 排障中的因果证据边界及相邻证据方法篇一致 |
| SRE 事件组织 | L45/L49–51 对指挥、操作、沟通、规划、实时文档和尽早宣布的概括可由 [Managing Incidents](https://sre.google/sre-book/managing-incidents/)职责分离、实时文档与宣布条件小节支持。“一小时”是原作者团队的广义宣布指南，不能成为本库或 GPU/NPU 环境的统一处置超时 |
| 无责与行动项 | L39/L66 的无责、单一责任与行动跟踪方向有 [Workbook 原章](https://sre.google/workbook/postmortem-culture/)依据；字段表是本库扩展，不是上游原封不动的模板。未把原文匿名化容量占位符搬成实测数值 |
| 自动化输出 | L68 将 FaultDiag 输出限定为候选假设，与固定文件“诊断报告解读”的字段、示例疑似节点及后续排查建议相容；不由工具所用“根因节点”字段名授予 confirmed。固定文档示例显示的组件版本为 26.1.0，属于 v26.1.1 仓库快照中的示例，不能据此声称本库运行过 26.1.1 |
| 三类材料及数据管理 | L74–76 区分本地、公开来源与合成材料，明确脱敏和管理引用；没有把公开复盘改成本库现场经历，也没有把合成题组当成发生率证据 |
| 更新触发与弃用 | L106–109 四类触发齐全，版本替换与同版本入口修复分开；L115–118 保留 ID、替代说明与历史实际模型，符合写作指南。固定历史环境不应因新版本出现而被改写；历史记录也不能替当前已失效结论背书 |
| 原创设计与实施状态 | L100/L131 区分本库维护设计和 SRE 方法，模型审阅、来源核对、实测分别记录。L32/L126 明确无真实事故执行、无自动化/网站/API 实现；不将 source_checked 等同于 reproduced |
| 公开案例与统计 | 这是 Web/网络服务的单一公开事件，不含可用于 GPU/NPU 的发生率、恢复能力或兼容性统计。正文未引入这类数值外推；其映射的具体事实仍需按 C01 修正 |

## 编号发现

### C01 · P2 · 公开复盘映射混入无证据事件并混淆机制与观测

- **位置**：正文 L80；交叉对照 L61/L64 与所链接的来源案例。
- **问题**：示例把时间线写成“配置命令下发→撤销未生效→全球 DNS 服务器停播”，并将遗留风险写成“维护期期间第二起故障叠加（复盘自述）”。Meta 披露的是容量评估命令未被审计工具正确阻止，并非下发后尝试撤销失败；DNS 服务器撤回 BGP 宣告后仍在运行。原文的后续问题是该事件的传播与恢复风险，没有披露第二起独立事故叠加。另将“DNS 服务器停播”直接标成外部发现时刻、把 BGP 写入“解析失败”，也混淆了运营方机制、路由观测和 DNS 解析结果。这些正是本篇示例应当演示如何分开的边界。
- **证据**：[Meta 原文](https://engineering.fb.com/2021/10/05/networking-traffic/outage-details/)中以 `During one of these routine maintenance jobs` 定位命令/审计工具段，以 `To ensure reliable operation` 定位撤告机制段；恢复部分在 `In the end` 段明确未再出现系统性故障，前面的流量/供电风险是预防性担忧。[Cloudflare 原文](https://blog.cloudflare.com/october-2021-facebook-outage/)“The Internet - A Network of Networks”之后的开事故单段与“BGP”小节，分别给出 15:51 UTC、15:58 UTC 的观测活动。[库内案例](../../knowledge/08-reliability/correlated-failure-source-case.md) L42、L48–63、L88 已明确命令具体内容/下发机制未知、两类时间线不精确对齐、渐进恢复且无再发系统性故障。
- **建议修订**：按原始证据重核这一映射，删除撤销失败和第二起事故的断言；将容量评估命令、审计保护失效、骨干断连、主动撤告、外部 DNS/BGP 观测及恢复风险分别归类。运营方未披露的绝对时刻与细节保留 unknown；confirmed 保持“运营方自述”的证据层次。
- **关闭条件**：示例每个事实及风险都能定位到相应原文；机制顺序与外部发现时刻分列；不再把撤告等同于进程停止、把风险当成已发生事故或为未公开命令补写撤销过程；与链接的库内案例边界一致。

### C02 · P2 · 用通用 SRE 依据承载缺少条件的 Flight Recorder 机制

- **位置**：正文 L52；关联来源核对范围 L134–140、取证记录 L17。
- **问题**：保全证据一行提出“转储前先拷贝环形缓冲/飞行记录”，并以“如 NCCL flight recorder 在 watchdog 超时自动转储的机制”为例，依据却只有 Effective Troubleshooting。本篇既未登记这一组件机制的一手来源，也未说明已启用记录和转储的条件；“转储前先拷贝”还将内存记录、导出/转储和保存副本混为一个普遍顺序。读者不能据此判断超时后是否存在可保存文件，或如何在清缓存/重启前保全已有证据。
- **证据**：[SRE 排障章](https://sre.google/sre-book/effective-troubleshooting/)“Triage”支持尽快缓解同时保留日志等证据，“Test and Treat”支持考虑主动测试副作用、记录动作与结果；没有给出 NCCL 转储机制。补充打开的 [PyTorch 官方教程启用小节](https://docs.pytorch.org/tutorials/unstable/flight_recorder_tutorial.html#enabling-flight-recorder)及数据获取小节将采集、超时转储和按需获取分开；[ProcessGroupNCCL 官方变量表](https://docs.pytorch.org/docs/2.14/torch_nccl_environment_variables.html)的 `TORCH_NCCL_DUMP_ON_TIMEOUT`、`TORCH_NCCL_TRACE_BUFFER_SIZE` 行要求转储开关与正的缓冲大小配套。这证明该行为有实现与配置条件，不能由 SRE 通用原则推出。
- **建议修订**：本篇可收缩为按现场已经部署的工具，在会丢失易失状态的动作前保全可获取的证据，并记录未采集/未配置项。若保留 Flight Recorder 例子，补精确来源登记和框架/版本/启用条件，清楚区分内存记录、导出与持久保存；不把组件配置指南扩写进通用复盘流程。
- **关闭条件**：通用保全原则与组件级机制各自有适当证据；不存在无条件自动转储或普遍“转储前拷贝”的操作预设；缺少数据时记采集缺口，不以无文件推导无异常。无需执行诊断、改环境变量或启动训练验证。

### C03 · P2 · 追溯链未到 catalog，完成判据可在清单未更新时成立

- **位置**：正文 L84–100，尤其 L96–97；完成判据 L124。
- **问题**：第五步只列域 index、topic-coverage、roadmap/batch 审计和统计，没有 catalog、重建与检查；L124 又以完成这五步作为全链路完成。本任务 acceptance 第三条明确要求到“导航/catalog”。只同步人工账面，无法使面向 Human/Agent 的生成清单取得修订后的路径、元数据与摘要。正文虽命名了编写者、审阅者和登记者，仍未明确最后一步由谁确认生成结果与源文件一致。
- **证据**：[任务定义](../../plans/full-coverage-backlog.yaml) L7039；[AGENTS](../../AGENTS.md) L17/L19 规定 build 为生成物，内容修改后运行结构检查与构建；[写作指南](../authoring-guide.md) L39–47 要求检查、构建并检查导航和 Agent 清单，同时限定这些检查不代表技术审核通过。本文未提供任何替代 catalog 更新步骤。
- **建议修订**：补上由维护/登记角色负责的结构检查、从源文件重建 catalog、核对受影响 content IDs 的记录及失败时的完成阻断；生成产物不手工编辑。保持技术审阅发现的修订和定向复核，与结构/清单检查分开记录。
- **关闭条件**：第三条验收可从 source/release/patch/case 更新一路追到受影响 ID、修订、独立技术审阅及发现关闭、导航和 catalog；每段可识别责任角色与完成证据。清单未同步或检查失败时不得按 L124 宣告流程完成；不因此要求本轮审阅者执行构建。

### C04 · P3 · Meta 来源在正文 URL 与取证 ID 上失配

- **位置**：正文 L14/L139；取证记录 L19；registry L6959–6961。
- **问题**：正文 source_ref 使用存在的 `src.meta.oct4-2021-postmortem`，取证表却写不存在的 `src.meta.oct-2021-facebook-outage`。正文唯一 Meta 内联 URL 路径为 `/networking-traffic/outage-details/`，registry 登记为 `/networking/outage-details/`，不满足本轮逐字对齐要求。这是来源追溯失配，不是本篇 frontmatter 引用了不存在的来源。
- **证据**：只读比对共 7 处远程链接、5 个唯一 URL，6 处与 registry 某一 `url` 完全一致，仅 L139 的 Meta URL 不一致。用户指定的 [networking-traffic 原页](https://engineering.fb.com/2021/10/05/networking-traffic/outage-details/)本轮可读；登记入口本轮网页工具未能打开，不能只因内容标题相同就略过精确入口核对。不存在的取证 ID 在完整 registry 中无匹配。
- **建议修订**：取证记录统一使用已登记稳定 ID；编写/登记角色核实两个 URL 的同篇关系和可访问入口，再同步正文、来源记录及必要的 registry 入口。不要为同一材料另造来源 ID。
- **关闭条件**：取证 ID 可解析，正文所有内联上游 URL 与对应 registry 登记入口逐字一致，且 Meta 所选精确入口能定位已核实的同篇原文；保留本轮工具可达性的实际观察。

### C05 · P3 · 将好复盘案例的发布时间写成模板统一时限

- **位置**：正文 L56；关联取证记录 L9、registry L7103。
- **问题**：“SRE 模板：一周内发布”把案例中受到肯定的发布时间压成了模板规定的时限。原文确实批评四个月后才发布，但没有据此为所有事故规定七天发布期限。本库可自行设定时效目标，需与来源事实分开。
- **证据**：[Workbook 原章](https://sre.google/workbook/postmortem-culture/)“Why Is This Postmortem Better?”下的“Promptness”描述好案例在事故关闭后一周以内写成并流转；坏案例的“Delayed publication”批评四个月拖延。章末模板部分允许按组织需要定制；这些位置支持及时编写，不能推出统一期限。
- **建议修订**：准确标明这是好案例的时间表现和作者对及时性的评价；如要规定本库时限，单独标为本库规则并给出适用与延期口径，不归为 SRE 模板的强制要求。
- **关闭条件**：一周/四个月仍各自绑定原案例，正文、取证记录与 registry 的摘要不再暗示上游统一规定七天时限。

## 五条 acceptance 的逐条判断

| 序号 / 任务要求 | 覆盖与边界 | 初审判断 |
|---|---|---|
| 1 · 影响/范围/时间线、实体/版本/工作键、采集覆盖、假设三分、处置/恢复与遗留风险；不倒推根因 | L60–66 字段齐全，L64/L124 的根因纪律明确，L65 链接处置六字段 | **结构满足，证据应用待修**：C01/C02；不因有字段就认定示例事实或具体采集机制正确 |
| 2 · 本地/公开/合成区分，敏感材料用管理引用 | L74–76 明确分类、脱敏、附件引用及不复制现场可变状态 | **满足本轮文本验收**；未要求本轮创建真实事故或采集敏感日志 |
| 3 · 更新→受影响 content IDs→修订→定向技术审阅→导航/catalog，明确责任 | L84–100 有主链、角色、来源反查和独立审阅要求 | **部分满足**：C03 阻断 catalog 终点与完成判据；C04 影响本篇来源追溯的实际可解析性 |
| 4 · 四类复核触发，弃用保留 ID、替代说明、历史实际模型 | L106–118 四类齐全，固定版本和换版本明确区分；实际模型记录按既有约定维护 | **满足核心要求**；导航/清单最终一致性仍随 C03 复核，不将历史环境/模型记录改成新版本结果 |
| 5 · 填写示例或公开复盘映射，三类核验分别记录，无自动化/网站/API 实现 | L78–80 有公开映射；L100/L126 分开模型/来源/实测并限定实现状态 | **部分满足**：映射准确性须按 C01 关闭，当前不能作为合格示例；C05 需收缩上游时限归因 |

## 元数据、引用与相邻边界核查

- **Frontmatter**：用 `schemas/content.schema.json` 的 Draft 2020-12 校验器及日期格式检查只读校验通过。稳定 ID 全库唯一；`procedure / reliability / draft`、`platforms: [generic]`、`updated_at: "2026-10-21"` 合法。7 个 source_refs、4 个 related_ids、3 个 verification.evidence_refs 均可解析。空 environment_refs 与未有环境档案的说明一致；source_checked 没有被改成 reproduced，但其事实核对范围需按发现修正。
- **本地链接与导航**：正文 7 处相对链接均存在。08 域 index L11/L29/L45 分别登记 ID、已有正文入口与 08.8 主归属，与总目录 L90–98 一致；08.3/08.4 是方法关联，不必再复制一份正文。
- **兄弟篇检查范围**：只查交叉引用及分工。可靠性统计提供记账入口，证据方法提供结论边界，处置选择提供六字段，静默错误篇提供平台证据，题组被标为合成/公开教学材料；不因这些链接存在而替这些篇目作技术审核背书。所链接的公开案例已保留正确的机制/观测边界，不能为本篇 L80 的旧说法作证。
- **历史记录与许可**：正文关于实际模型如实保留、弃用不删除稳定 ID 的方向正确。对旧来源采用保守 unknown 许可，不等于有再分发授权；本轮没有镜像上游全文、复制原图或补写统一许可。计划仍为 planned / needs_source_preparation，本报告不更新任务状态，也不由报告存在推导其验收通过。

## 未决 / 超出本轮范围

1. C01–C05 尚未修订、尚未定向复核。编写者需提供修订后的正文摘要与证据坐标，由同一审阅者核对关闭条件；本会话不代为修订。
2. 没有本地事故、环境档案或流程执行证据；实际采集覆盖、Clock/ID 对齐能力、工具配置、行动项关闭效果及恢复判据仍待真实记录，模型审阅不能补齐。
3. Meta 未披露的命令内容、内部绝对时间、实现与修复细节继续 unknown。登记入口的工具访问失败不证明网站全局失效或不存在重定向；需要后续入口核实，不能替换成关于事故的新结论。
4. 外部行动跟踪系统、跨厂商联合复盘、法律责任、客户通报不在本任务已交付范围。本文不要求为通过文字验收而实现自动化、部署网站/API 或定时任务。
5. 未对相邻正文、Batch 30 其他任务或整库开展完整技术重审；下游题组等条目如复用本例，应在修订时按追溯链定位影响，本报告不宣告这些条目通过。

## 本轮检查与写入声明

执行了本地只读行号/摘要、schema/日期、ID、内联 URL 精确比对与相对链接检查，并独立读取上游证据。未运行 `make check`、`make build` 或 `make test`；此次只新增审阅报告，不修改知识正文，并遵守用户不改构建产物的限制。定向检查不等价于仓库全量检查通过，更不等价于真实环境验证。

审阅开始及报告写入前 Git 工作区均无变更；正文与取证记录的 SHA-256 在写入前复查不变。本会话唯一仓库写入为本报告。未执行诊断、探测、负载、恢复、故障注入或任何正文/网页中的示例命令。

**T08-07 第一轮结论：需修订并定向复核。发现 5 项（P1=0，P2=3，P3=2）；当前不宣布 T08-07 或 Batch 30 审阅通过。**
