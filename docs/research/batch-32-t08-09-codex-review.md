# Batch 32 · T08-09 第一轮初审报告

## 会话元数据与结论

| 项目 | 记录 |
|---|---|
| 角色 / 轮次 | 独立批次审阅者；第一轮初审；本会话仅交付发现，不承担正文编写、问题修订或关闭 |
| 指定 / 实际模型与档位 | `gpt-6.1-sol / xhigh`；实际值由当前会话 rollout 的最新 turn_context 核验，与指定一致 |
| rollout 定位 | `/Users/ywang2397/.codex/sessions/2026/10/22/rollout-2026-10-22T09-20-56-01a16132-6b6d-7302-8de8-11ace1c8a3af.jsonl` |
| 会话归属互核 | JSONL L1 的 session_meta.id、环境 CODEX_SESSION_ID 和 CODEX_THREAD_ID 均为 `01a16132-6b6d-7302-8de8-11ace1c8a3af`；L10 的用户消息明确指定 Batch 32、T08-09、commit 90c38f7、同一仓库和本报告路径 |
| turn_context 坐标 | 全会话当前共 1 条，最新为 L8；时间戳 `2026-10-22T01:21:05.892Z`；turn_id 为 `01a16132-6c65-7622-a42e-90a3444573f8`；写报告前再次核验一致 |
| turn_context 实际字段 | model=`gpt-6.1-sol`；effort=`xhigh`；cwd=`/Users/ywang2397/work/AI_reliability_knowledge_base` |
| 嵌套设置互核 | collaboration_mode.mode=default；settings.model=`gpt-6.1-sol`、reasoning_effort=`xhigh`、developer_instructions=null；未使用配置默认值或正文自述代替运行记录 |
| 执行方式 | 当前本地 Codex CLI 会话直接审阅；session_meta.originator=codex_exec、cli_version=0.163.0；未另启模型或子代理。核验限于本地运行记录，不声称独立认证服务端路由 |
| 日期 / 时区 / Git 基准 | 2026-10-22 / Asia/Shanghai；HEAD=`90c38f7592137eeb2b1862983822fe415cf471c5`，与指定提交一致 |
| 交付页快照 | knowledge/08-reliability/index.md：116 行；SHA-256 `366eca7c64c9468407d2c3e2139d7b9bcd4b84a47d628e04eda575d3911daba3` |
| 取证记录快照 | docs/research/batch-32-t08-09-sources.md：28 行；SHA-256 `59cfd4eadd1422fe73e2b238c64277fd3b9223ce5bdeeaae6834db4769097587` |
| 快照方法 | 开始实质审阅前执行 wc -l 与 shasum -a 256；后续补读材料在读取前同样取数，写报告前复算。完整清单见文末；交付页与本任务取证记录均未变化 |
| 唯一写入范围 | 仅新增 docs/research/batch-32-t08-09-codex-review.md；不修订正文、作者取证、计划、来源登记、历史报告或构建产物，不运行 make build |

**结论：需修订并定向复核，暂不通过。共 4 项发现：P1 0 项、P2 2 项（C01、C02）、P3 2 项（C03、C04），全部 OPEN。** 40 格均有可访问的实际正文，主要方法及状态边界有承接；但实体/工作键检查项未完成其功能，08.7 的处置格用执行状态替代方法入口，另有交付计数与原主题题名偏差。

优先级按本轮用户口径：P1＝足以严重误导处置的关键错误；P2＝影响任务交付、导航功能或验收证据的必修事项；P3＝局部入口、记录或可追溯性问题。下文“入口 L…”指上述交付页快照，其他文件单独标识。本报告不把任何发现记为 CLOSED。

## 范围与方法

先读 README.md、AGENTS.md、docs/authoring-guide.md（§3/§5/§6/§7）、schemas/content.schema.json 与 content-outline.md；以 [T08-09 objective 和四条 acceptance](../../plans/full-coverage-backlog.yaml) L7489–7533，以及同文件八主题 L3009–3438 的 title、delivery_scope、closure_criteria 为标准。报告格式参照 [Batch 31 T06-09](batch-31-t06-09-codex-review.md)。

完整读取本任务[入口页](../../knowledge/08-reliability/index.md)、[作者取证记录](batch-32-t08-09-sources.md)及矩阵全部 11 篇不同正文，核对实际表格、流程、例子和边界；不以标题或链接存在替代内容判断。另读取 Batch 29 三份来源及指定最终复核、Batch 30 五份来源的任务/unknown/修订记录、批次汇总及各任务最后复核的范围和结论，核对 validation-backlog；抽查设备健康证据与 08 入口的入链。

本轮审阅的是导航和交付承接，没有重新抓取外部 URL，也没有重新认证兄弟篇全部上游技术主张。历史来源的精确 revision、许可和未取证范围，按对应正文与既有审阅记录保留；报告中的历史“通过”只转述其声明范围。本轮没有执行任何训练、推理、采集部署、主动诊断、处置、压力、注入或评测操作。

### 正文简称

| 简称 | 实际读取的正文 |
|---|---|
| D | [可靠性维度与故障域](../../knowledge/08-reliability/dimensions-and-failure-domains.md) |
| E | [诊断中的证据、假设与结论](../../knowledge/08-reliability/evidence-and-hypotheses.md) |
| F | [故障模型、跨层传播与共享失效分析](../../knowledge/08-reliability/fault-models-and-propagation.md) |
| C | [相关故障与冗余失效来源案例](../../knowledge/08-reliability/correlated-failure-source-case.md) |
| M | [隔离、重试预算、降级与恢复选择](../../knowledge/08-reliability/mitigation-and-recovery-principles.md) |
| S | [静默错误与计算完整性判定](../../knowledge/08-reliability/silent-errors-and-integrity.md) |
| T | [统一测试选择、压力/注入与统计方法](../../knowledge/08-reliability/test-design-and-coverage.md) |
| R | [可靠性统计、有效产出与恢复损失](../../knowledge/08-reliability/reliability-metrics-and-recovery-loss.md) |
| P | [事故复盘、来源更新与知识维护](../../knowledge/08-reliability/postmortem-and-knowledge-update.md) |
| Q | [诊断评测方法规范](../../knowledge/08-reliability/diagnostic-evaluation-method.md) |
| X | [诊断评测公开题组](../../knowledge/08-reliability/diagnostic-evaluation-fixtures.md) |

### 8 × 5 逐格核对

坐标均为各正文的原文件行号。链接到整篇文件的复用方式本身成立，不要求把所有入口改成页内锚点；但链接文字仍应表达该格所需的方法，不能由目标文件恰好还有其他章节来替代该格映射。

| 主题 / 入口位置 | 原理与边界 | 设计与使用 | 观测与判断 | 故障与处置 | 验证与案例 |
|---|---|---|---|---|---|
| 08.1 / L42 | D L36–47 的四维表及 L51–62 八项指标字段真实存在 | M L51–73 有处置六字段、四维选择表 | R L43–55 有对象/窗口/分母/事件及缺失、删失、重叠、聚合 | D L104–115 有退出门槛；M L104–114 有恢复候选及条件 | R L83–94 有六类量；T L44–81 有选择矩阵、统计与停止记录 |
| 08.2 / L43 | F L47–87 有三概念、故障分类和传播纪律；D L83–102 有共享故障域 | F L89–139 实有训练/推理两图和九行有限 FMEA | C L46–63 分列运营方机制顺序、外部发现时间和证据类型 | F L143–153 有时间/身份对齐、依赖清单、反向对照、有限验证及冗余独立性核对 | C L90–112 有迁移检查问题、不可外推条件和未解项 |
| 08.3 / L44 | E L33–45 的五类是症状/观测/假设/证据/结论；清单转述错误见 C01 | E L47–65 有运行、进程、设备、工作、来源五轴及时间域；R L106–155 有三张 schema | E L59–65、L91–95 有时钟、采集覆盖和缺日志的边界；设备侧边界另在 01 域 | E L138–150 有结论范围、竞争假设、缓解/根因分离、恢复验证和下一检查 | P L42–81 有事故记录及公开复盘映射；R L157–188 有显式合成计算例 |
| 08.4 / L45 | E L69–95 区分支持/反驳/未知，并保留混杂与缺日志问题 | E L97–112 有判别收益、代价、运行影响、可逆性及执行前提 | Q L57–68 确有 A/B/C/U 四级，规则命中只能支持候选 | E L114–136 的两个例子确为原创合成且未执行；Q L47–55 有评审角色和污染控制 | X L48–122 实有十条输入/oracle/判据条目；公开用途和非 holdout 边界成立，“九条”失实见 C03 |
| 08.5 / L46 | M L116–120 有独立性、共享依赖与 error budget | M L75–102 有重试预算、退避、幂等、流式边界、隔离与降级 | R L83–92、L108–155 给恢复分段、attempt/phase/outcome 与进展记账位置；不把成功重放一概计作零产出 | M L104–114 按训练/推理/发布分恢复候选及结果门槛 | M L122–130 有有限对照设计；C L76–88 有冗余、运维通道与恢复节奏边界 |
| 08.6 / L47 | S L53–73 区分 SDC、灰色退化、软件数值错误及“静默”三层 | S L131–150 的检测方法表比较覆盖、成本与假阴性/误报 | S L152–162 有合法浮点差异、dtype/开关、容差与候选判定流程 | S L102–129 不只有传播数据，L125–129 还给可信恢复点、optimizer/checkpoint 污染与观测副作用；L206 有完整怀疑与恢复链 | S L86–100 确有 Fleetscanner/Ripple 同分母对比；L164–181 实有三平台版本化清单及 unknown |
| 08.7 / L48 | T L44–65 有四类测试的问题、故障模型、覆盖、资源与恢复差异 | T L85–109 有注入六字段、压力预算、停止/恢复及共享依赖保护 | T L67–83 有重复层级、预热、次序、对照、均值/尾分位、预注册及停止记录 | **入口不满足该格功能，见 C02**：标签只写执行 0/7 与结果留白；实际停止/恢复/回退方法在 T L104–109，未被此格标识 | T L111–125 确有七行准备矩阵及设计→冻结→执行→复核分层，全部未执行 |
| 08.8 / L49 | R L57–65 分对象、时间轴、事件集、模型假设、仿真/观测和均值/分布 | P L42–103 有事故证据与登记→定位→修订→审阅→导航→检查/重建六步链 | R L96–104、L129–155 分列成功、失败、取消、超时及质量、goodput、缺测 | P L107–114 有版本变更、上游冲突、链接失效、验证反例四类复核触发 | P L116–129 有弃用与流程完成判据；Q L86–94 有公开题组/独立评测角色及未实现边界 |

矩阵表头、分隔行和八条数据行（入口 L40–49）**均为 7 个未转义管道符、6 列**，无串列。每格多链接用“与”或中文分号连接，解析边界清楚；无须为缺少空格单列发现。题名逐字比较为 6/8 一致，08.6/08.7 差异见 C04。

### 七项阅读检查清单

| 检查项 / 入口位置 | 正文承接与判断 |
|---|---|
| 时间 / L55 | R L43–55 支持统计框架；E L47–65 支持先关联对象再比较时间，并要求时钟域、偏移/不确定度、发生/记录/采集时间分开。入口概括不与正文相反，但统计窗口不能代替时钟对齐 |
| 实体/工作键 / L56 | **不满足，C01**。记录类型与实体关联键是两个轴；本条既没有工作键检查内容，又把 E 的五类错误转述为含“事件”、不含“证据” |
| 采集质量 / L57 | [01 域健康证据](../../knowledge/01-hardware/health-evidence.md) L76–86 实有摘要、事件、计数、采样失败和未覆盖的区分；设备具体机制未复制入 08，作为边界指引合适 |
| 覆盖 / L57–58 | T L46–65 规定声明对象、故障模型、观测点和实际覆盖；S L131–150 区分覆盖/成本/假阴性/误报。部署采集系统不等于方法已覆盖，与 T 一致；也不意味着一次检测 PASS 证明无故障 |
| 假设反驳/未知 / L59 | E L69–95 支持三分及缺测不转为反驳；S L164–181 支持平台按版本记录与 NPU unknown。入口的三分摘要没有宣称正文不存在混杂状态 |
| 下一项检查 / L60 | E L97–112 的收益/代价/影响与 M L51–85 的六字段、目标维度、预算相符 |
| 终止门槛 / L61 | D L104–115、T L81/L104–109、P L125–129 分别提供退出门槛、停止记录和流程完成判据；复盘完成仍可保留 unknown |

清单只有采集质量条目直接给了一个链接，其余主要依赖前面的矩阵定位；这增加查找成本，但本轮不单独把所有条目补锚点列为必修。C01 要求实体/工作键本身可检查，并给出与其内容相符的正文入口。

## 已核实的主链与边界

| 对象 | 核对结果与保留范围 |
|---|---|
| 08.1 原 covered 链 | D 的四维目标、指标字段、退出门槛 → M 六字段与按维度选措施 → T 选择/覆盖/统计 → R 六类量和合成四维结论，正文间有相互链接。入口 L42/L67 的方法链有实质内容，不承诺现场达标 |
| 08.3 原 covered 链 | E 的身份/工作/时间/来源关联与覆盖缺失 → R 三表记账 → P 复盘证据及追溯链成立；不要求部署采集系统。入口 L44/L67 有承接，L56 的错误概括需修正 |
| 08.4 原 covered 链 | E 支持/反驳/未知与下一检查 → Q 答案强度、角色隔离及七维 rubric → X 公开教学题组成立。Q L43/L88 仍说明本库没有独立评测集或运行中的评测系统 |
| NPU SDC unknown | S L170–181 明确现有 Ascend 工具证据支持 ECC、离线比对和规则诊断，未取得发生率、fleet 检测实践与保障能力的一手材料；不以 CPU/GPU 数字代填。入口 L70/L81 及本批取证 L24 没有越过该边界；AMD 硬件观测与发生率 unknown 也未被改为已证 |
| 七方案 0/7 | T L111–125 的七份方案均为设计；validation-backlog L6/L9–12 及 V01–V07 的 status=planned、evidence_refs=[]、executed_at=null 一致。七份方案对应 V01–V07，不是把全部 V00–V12 工作包误算成七项 |
| V12 | validation-backlog L465–489 明确独立案例、授权/脱敏、外置输入答案、冻结及执行证据均待取得；Q L31–43、X L42/L124–129 与入口 L70/L83 一致；公开、合成材料不关闭独立 holdout 目标 |
| 文档与验证状态 | 入口 L16/L65/L70 与 AGENTS.md L8–11、写作指南 §3/§4 一致。11 篇正文全部 draft，其 verification 均为 source_checked；不能由 draft 推导未验证，也不能由 source_checked 推导 reproduced。本文明确没有本地实测，各状态分别维护 |
| 维护与原始资料入口 | P L83–129 有责任链、复核触发、弃用和完成判据；入口 L71 指向该方法。页尾三项为既有资料入口，非新增技术证据；source_refs 三 ID 均存在。NCCL URL 的目录根与 index.html 是两种字符串形态，本轮未在线认证其等价性，未以主页证明具体技术主张 |
| 11 条“已有正文”描述 | D/E/S/T/R/P/Q/F/C/M 的描述均有上表内容承接；X 的 U 级、合成、固定输入/oracle/判据及非 holdout 边界真实存在，数量错误见 C03。没有把 Meta 来源案例或原作者硬件研究改称本库复现 |
| 元数据与地图 | 稳定 ID reliability.index 与父提交相同；type=index、domain=reliability、status=draft、platforms=[generic] 均保留。17 个 related IDs 全部存在，3 个 source refs 存在；updated_at=2026-10-22、summary 新增矩阵及交付核对描述与改动相符。二级地图 L76–83 的承担关系与正文一致；08.6/08.7 的地图保留全题名，但矩阵没有，见 C04 |
| 本地链接与入链 | 本页 116 处相对链接、33 个不同目标均存在。README、knowledge/ 与 paths/ 搜索到指向本页的 19 处链接、分布于 14 个文件，均指向未变的文件路径；重点抽查 README L29、00 首页 L58、角色页 L51/L88、训练排障 L90/L103/L107–108、推理排障 L74/L95，目标仍有效且无新增锚点依赖 |
| 本批取证一致性 | 取证 L7“无新增来源”与提交中 registry 无差异相符；L13 的 11 篇取材与实际目标一致，L18 七项清单/三分边界为本页原创组织，L22–24 三项状态边界与正文一致。它不能代替本轮对原创措辞的审阅；C01/C02 的问题仍需作者修订并追记 |
| 初稿标记 | 入口 L72/L116 明确是交付时初稿、审阅待做；本批取证 L26–28 为初审后的待追记段。在指定提交和本轮初审起点，这些是诚实阶段标记，不构成预先宣布通过；本报告产生后由维护者更新后续状态，本会话不代改 |

### 来源、修订与最终复核链

| 任务 | 来源/修订记录 | 已定位的最终复核及边界 |
|---|---|---|
| T08-01 | [来源](batch-29-t08-01-sources.md) L9–23、L27–34 | [recheck-2](batch-29-t08-01-codex-recheck-2.md) L19–20、L30–44：累计十项关闭；永久存在/间歇表现/可复现性、F1 影响域、共享依赖候选和 NPU unknown 均保留 |
| T08-02 | [来源](batch-29-t08-02-sources.md) L9–10、L27–35 | [recheck](batch-29-t08-02-codex-recheck.md) L18、L30–55：七项关闭；运营方顺序与外部发现时刻、全球口径、带外依赖和恢复验收 unknown 不升级 |
| T08-03 | [来源](batch-29-t08-03-sources.md) L15–24、L28–35 | [recheck-3](batch-29-t08-03-codex-recheck-3.md) L19–28、L41–45：累计十一项关闭；最后处理固定源码链接及来源同步，不扩大到未核重启/成员组合 |
| T08-04 | [来源](batch-30-t08-04-sources.md) L29–69，保留历次修订 | [recheck-5](batch-30-t08-04-codex-recheck-5.md) L73：N11 关闭、此前关闭未回归；[批次审计](batch-30-source-audit.md) L15/L21 汇总 14/14。检测数字、两类时间、版本和 unknown 均在正文保留 |
| T08-05 | [来源](batch-30-t08-05-sources.md) L27–51 | [recheck-3](batch-30-t08-05-codex-recheck-3.md) L15–16/L65：累计 10/10；准备实例、字段未冻结与真实执行缺口保留 |
| T08-06 | [来源](batch-30-t08-06-sources.md) L27–67 | [recheck-4](batch-30-t08-06-codex-recheck-4.md) L82：最后 5/5；批次审计 L17 汇总 16/16。来源冲突、合成例、成功重放/丢弃尝试及 unknown 不因通过消失 |
| T08-07 | [来源](batch-30-t08-07-sources.md)的 unknown 与修订段 | [recheck-3](batch-30-t08-07-codex-recheck-3.md) L55：累计 6/6；流程含结构检查/catalog 重建，不宣称实现自动化或完成真实事故复盘 |
| T08-08 | [来源](batch-30-t08-08-sources.md) L37–54，特别 L45 的新增 PTF-10/总数十条 | [recheck-3](batch-30-t08-08-codex-recheck-3.md) L22–23/L66–70：最后 3/3，V12 继续缺证据；批次审计 L19/L30 汇总 11/11、题组十条 |

入口 L68 指定的三份 Batch 29 最终复核文件存在且任务正确；L69 的五份 Batch 30 sources 和批次汇总也存在、任务正确。批次汇总是本地审计文件，不是逐任务复核文件本身；本轮继续定位上表最终报告核对，未因汇总的概括性题名判断缺少历史审阅。未重新核验历史每个会话的实际运行字段，未改写历史模型记录。

八主题的 content_acceptance_status 及 T08-09 自身仍为 planned，属于当前最终验收尚未完成的账面状态；本报告不自动改为 accepted/done。08.7-G3 的实测目标、08.8-G3 的外置独立材料目标仍按其 closure_criteria 保持开放，不能以本轮方法导航齐全关闭。

## 逐项发现

### C01 · P2 · OPEN · “实体/工作键”被记录类型和分母替代，且五类转述不符正文

- **位置**：入口 L53–56；关联 L44、L67；作者取证 L18。
- **问题**：L56 标题承诺检查实体/工作键，正文却只列五种记录对象和统计对象/共同分母。记录类型回答“这句话是什么性质”，实体/工作键回答“是否属于同一次运行、进程、设备和工作”，后者没有实际检查内容；同时所列“症状/事件/观察/假设/结论”把 E 的“证据”漏掉，加入了并非该五类表成员的“事件”。这不满足 acceptance 第 2 条，而不是要求部署采集系统。
- **证据**：E L33–41 的五类明确为症状、观测、假设、证据、结论；L49–65 独立列出 run/attempt/重启代次、global/local rank/进程/容器/主机、物理设备/运行时序号、step/microbatch/请求/collective/checkpoint/数据游标，以及观测来源和时钟。P L63 同样要求实体/版本/工作键。D L55–62 的统计对象和分母不能替代这些关联键。backlog L3108 虽将事件列入主题覆盖内容，也没有把它定义为 E 的“五种记录对象”，不能以规划中的概括列表替代当前正文的分类。
- **建议修订**：把记录类型分类与身份/工作键检查分开，按 E 的真实分类转述；在实体/工作键条目中明确运行尝试、进程/rank、设备映射及实际工作键的对齐要求，并链接到承载这些字段的 E/P 正文。更新取证记录中的本轮修订说明，不必改写已经具备这些内容的 E/P。
- **关闭条件**：清单本身能让读者检查“是否同一次运行/同一实体/同一项工作”，不再把记录类型或共同分母当关联键；五类名称与所链正文一致，入口可定位。由同一审阅者核对修订后的 L44/L55–56/L67 及取证同步。

### C02 · P2 · OPEN · 08.7 的“故障与处置”格用未执行状态替代停止/恢复方法入口

- **位置**：入口 L48 第五列（“故障与处置”）；关联 L38、L61、L65。
- **问题**：该格唯一链接标为“适用边界：真实执行 0/7 与结果留白”。0/7 说明证据尚未取得，不回答压力/注入发生异常时何时停止、如何保留现场、如何恢复或回退。正文有相应内容，但当前入口文字没有把该方面映射出来，因此不能仅以同一文件还含其他章节认定该格已完成五方面导航。
- **证据**：T L113 记录 0/7，L138–141 说明方法/登记状态；真正与故障处置相应的是 L81 的中途停止与放弃记录、L104–109 的有限预算、任一停止条件命中即停/保留现场、健康窗口与回退、共享依赖保护，L130 还指向 M 的恢复选择。backlog L3303 的 delivery_scope 明确含预算、停止、恢复，L7512 要求五方面都有正文入口。
- **建议修订**：将此格明确指向测试异常的停止、证据保留、恢复/回退及共享依赖保护方法；可复用 T，必要时关联 M。0/7 与结果留白继续留在验证格、状态边界或附注，不需要新增正文或执行实验。
- **关闭条件**：读者从“故障与处置”格能识别并进入真实处置方法，且 0/7/未冻结/未复核边界继续可见；矩阵行仍保持六列。定向核对 L48/L61/L70 与 T 原有方法，不能以改成“已执行”关闭本项。

### C03 · P3 · OPEN · 题组条数和 Batch 30 新增篇数与现有交付不符

- **位置**：入口 L31、L45、L69。
- **问题**：L31 和 L45 都称公开题组“九条”，实际已有十条；L69 称 Batch 30“四篇新增与一篇修订”，按篇统计实际是五篇新增与一篇修订。前者一处继承旧描述、一处在本轮矩阵再次写入，后者为本轮交付核对新增；均在本任务要求核对的现有导航与计数范围内。
- **证据**：X L22 写十条，实际题目标题 L48/55/62/69/76/83/90/97/106/115 对应 PTF-01–10；PTF-10 是存储完整性情境，不是已有九条中的重复标题。T08-08 sources L45 已记“新增 PTF-10、总数十条”，Batch 30 审计 L30 同口径。Batch 30 审计 L3 列 T08-04 修订 S，T08-05 新增 T、T08-06 新增 R、T08-07 新增 P、T08-08 新增 Q/X，即五篇新增、一篇修订；把新任务数四项计成新正文篇数四篇会漏算一个交付物。
- **建议修订**：按明确的条目/篇数口径同步三处计数；若改按任务计数，应明确“四项新增任务，其中一项交付两篇”，不能继续写“四篇”。结合已有来源与最终复核记录同步取证说明。
- **关闭条件**：入口中题目数与 X 十个不同题目一致，Batch 30 计数能逐篇对应 T/R/P/Q/X 加 S 修订；保留公开/合成、非 holdout、未评测边界。复核不需要重新开展上游研究或真实评测。

### C04 · P3 · OPEN · 矩阵缩写了 08.6/08.7 的原主题题名

- **位置**：入口 L47–48；对照同页 L81–82。
- **问题**：08.6 在矩阵写成“数值异常、静默错误与计算完整性”，漏“的判定方法”；08.7 漏题名末尾“方法”。同页二级主题地图保留全名，两处导航对同一主题使用不同题名，未满足本轮逐字核对与原题名保留约定。
- **证据**：backlog L3240/L3300 的 title 分别为“数值异常、静默错误与计算完整性的判定方法”“验收、基准、压力测试与故障注入方法”；content-outline.md L96–97 与入口 L81–82 一致。各主题 closure_criteria 的首条要求原目录题名保留。其他六行题名逐字一致，稳定 ID 没有发生变化。
- **建议修订**：矩阵两行恢复原主题全题名；无需重命名文件或更改稳定 ID。
- **关闭条件**：矩阵、二级地图、backlog 与原目录中这两个主题的题名逐字一致，其他六行及表格列数不受影响。

## acceptance 逐条判断

| T08-09 条款 | 初审判断 | 依据与限制 |
|---|---|---|
| 1 · 八主题五方面入口；08.1/08.3/08.4 完整链 | **部分满足，C02 必修，C04 需同步** | 11 篇目标实际承载大部分 40 格概念，三条原 covered 方法链有内容；08.7 处置格的入口功能未完成，两个矩阵题名偏离原定义。不是因缺硬件结果判失败 |
| 2 · 七项检查；采集部署不冒充覆盖 | **未满足，C01 必修** | 七个标题齐全；时间、质量、覆盖、假设、下一检查与终止有正文承接，部署/覆盖边界正确；实体/工作键没有实际检查内容并误述五类 |
| 3 · SDC、七方案等剩余限制入口可见；文档不改变 reproduced | **满足本轮导航范围** | NPU unknown、AMD/Ascend 版本边界、0/7、V12、公开题组非 holdout、draft/source_checked 与现场结果分离均保留 |
| 4 · 稳定 IDs、来源、维护、审阅修订复核；必要修订归原任务 | **前置链与状态边界可核；本轮最终验收未完成** | 稳定 ID/17 related、来源记录及最终复核存在、维护方法可定位；C01–C04 尚 OPEN，C03 的交付计数需订正。按修订→定向复核完成后再判断，不把“审阅待做”本身列为缺陷 |

## 校验、写入与结论

已执行 `PYTHONDONTWRITEBYTECODE=1 make check`，实际结果 **PASS：135 content entries / 577 sources**。另以只读脚本核对 17 个 related IDs、3 个 source refs、116 处本地链接/33 个目标、矩阵各行管道符、十个题号，以及 V00–V12 的状态/执行/证据字段。结构通过不验证远程内容、技术正确性、目标平台兼容性或真实测试成功。

遵守本轮明确范围，未运行 make build；未修改 src/kb/，未新增测试或运行 make test。只用无字节码方式执行仓库 Python 校验和本地 YAML 读取，没有创建日志、临时脚本或下载缓存。

工作区初始已有未跟踪的 docs/research/batch-32-t00-06-codex-review.md，未由本会话创建或修改。本轮在内存中保存了 710 个既存仓库文件（含现有 build 文件）的 SHA-256；期间对照发现其他任务的 docs/research/batch-32-t00-06-sources.md、paths/roles/reading-by-role.md、paths/tasks/environment-installation.md、paths/tasks/node-acceptance.md 发生变化。本会话没有对这些文件执行写操作，也未回滚。角色页入链抽查采用文末所列读取快照（113 行、SHA-256 ae0d71db…），08 两处入口仍有效；核心审阅页、本任务取证、11 篇方法正文和两份 backlog 哈希保持不变。因此不声称整个共享工作区在审阅期间静止。

报告写入后再次执行同一 make check，仍为 PASS：135 content entries / 577 sources；git diff --check 通过。文件对照共 711 个，唯一新增路径为本报告，无删除；文末 45 个审阅快照均与报告写入后的哈希一致。除上述四处并行工作变化外，既存文件没有额外变化。

**T08-09 暂不通过；C01–C04 全部 OPEN。** 作者完成修订并追记后，由同一审阅者按各关闭条件定向复核。所需改动主要在本导航页及本任务记录；现有 E/P/T 已有缺失入口所需的方法，不要求本轮额外实施现场采集、处置或实验。即使后续文档审阅通过，NPU SDC unknown、0/7 和 V12 的证据缺口仍分别保留。

## 输入行数与 SHA-256 清单

下表保存实际执行 wc -l 与 shasum -a 256 的结果。它覆盖本轮交付/修订页、本任务取证、全部矩阵目标、规范、计划、历史承接与入链抽查材料；历史报告仅按上述声明范围读取。角色页为实际抽查时快照，不冒称为审阅开始时的未变版本。

| 文件 | 行数 | SHA-256 |
|---|---:|---|
| [AGENTS.md](../../AGENTS.md) | 22 | `69262a5db32adfac46f6ab28d48d9670f2e1700cb2b946155ad3f3ccfe6f6454` |
| [README.md](../../README.md) | 158 | `4c2e54298f2693173dae66377124c90c4481fc4d5d01fe7efde09621c9a71874` |
| [docs/authoring-guide.md](../../docs/authoring-guide.md) | 132 | `75ee28d1aca7a4ac1d56ae493856037770a14fcdac27fa9b662451cee169a801` |
| [content-outline.md](../../content-outline.md) | 191 | `ed9033d2f53fa504fc05e55b221697dd7a1d14c5adaf58f8cc0a6613f8fe7046` |
| [schemas/content.schema.json](../../schemas/content.schema.json) | 52 | `b60b8d9ccb8728f034607901124c4206f5dc705ca824e31ce0ab5615523d0147` |
| [knowledge/08-reliability/correlated-failure-source-case.md](../../knowledge/08-reliability/correlated-failure-source-case.md) | 112 | `dbcd2ff365cf1af1d9ae722787a8babebaa3a4f53e5590694dfd11017d4b14b7` |
| [knowledge/08-reliability/diagnostic-evaluation-fixtures.md](../../knowledge/08-reliability/diagnostic-evaluation-fixtures.md) | 133 | `4bcd451e76559cc6ce6bd68adbfa355be51c80abf8230ca4444d88276b7ad8b1` |
| [knowledge/08-reliability/diagnostic-evaluation-method.md](../../knowledge/08-reliability/diagnostic-evaluation-method.md) | 102 | `35561b63bf98e94c2a8967c8a2d6877d2325dd8d804c60b8c7248f043b9894da` |
| [knowledge/08-reliability/dimensions-and-failure-domains.md](../../knowledge/08-reliability/dimensions-and-failure-domains.md) | 130 | `a98853a413ec6c397eb49e1f657d26c6ac4dc35a6ae8e2535e69b3691685add5` |
| [knowledge/08-reliability/evidence-and-hypotheses.md](../../knowledge/08-reliability/evidence-and-hypotheses.md) | 158 | `f3a3de664250892bcf2101205b2aa17e65ba2cca63b67d5e7fd2b01942a3aaa5` |
| [knowledge/08-reliability/fault-models-and-propagation.md](../../knowledge/08-reliability/fault-models-and-propagation.md) | 168 | `4cfdc2496f817be6efa2d97fafe7c6940ff3dd723d8d90ac20a4917b1d97884c` |
| [knowledge/08-reliability/index.md](../../knowledge/08-reliability/index.md) | 116 | `366eca7c64c9468407d2c3e2139d7b9bcd4b84a47d628e04eda575d3911daba3` |
| [knowledge/08-reliability/mitigation-and-recovery-principles.md](../../knowledge/08-reliability/mitigation-and-recovery-principles.md) | 145 | `c3dea4fb4974e92d7d0df32a6063dad425583d4c57fb5abe5cf5d4b155bd09b6` |
| [knowledge/08-reliability/postmortem-and-knowledge-update.md](../../knowledge/08-reliability/postmortem-and-knowledge-update.md) | 146 | `7ec8bb89866e3564a3ba1ea97959823aedc5cb75f6dd45c7244a445968358c33` |
| [knowledge/08-reliability/reliability-metrics-and-recovery-loss.md](../../knowledge/08-reliability/reliability-metrics-and-recovery-loss.md) | 209 | `411d40a9423a94a203effb098f0f183e1fe3fffd964c1c0eb76ba5011b0d167b` |
| [knowledge/08-reliability/silent-errors-and-integrity.md](../../knowledge/08-reliability/silent-errors-and-integrity.md) | 218 | `3ccb429f0bd98c9a0f312925dc158b358af73bf49a21feed3b829020375d33e5` |
| [knowledge/08-reliability/test-design-and-coverage.md](../../knowledge/08-reliability/test-design-and-coverage.md) | 153 | `a4cdd8c05e4c42abb737e1a9f0c1ad8f5edeeb000b6e385c4c46203aa482351e` |
| [plans/full-coverage-backlog.yaml](../../plans/full-coverage-backlog.yaml) | 7774 | `abffb0eaff9a825ac37ff1921acfa7a2d1fb73289d85f9d8d88a24febec71530` |
| [plans/validation-backlog.yaml](../../plans/validation-backlog.yaml) | 496 | `82f46abcf490e286dec747626d73ec9472ee8a4605ae18fff2c79e1a2a11115f` |
| [docs/research/batch-32-t08-09-sources.md](batch-32-t08-09-sources.md) | 28 | `59cfd4eadd1422fe73e2b238c64277fd3b9223ce5bdeeaae6834db4769097587` |
| [docs/research/batch-31-t06-09-codex-review.md](batch-31-t06-09-codex-review.md) | 140 | `ab68d30cf6560b580f622ed6225251ed3b8e1e8fd1efb60db8a0c96d6edb1dff` |
| [docs/research/batch-31-t00-05-codex-review.md](batch-31-t00-05-codex-review.md) | 139 | `0da82777995cdbc96e1da584763e86607097dbe107705496888919ce471ee5fc` |
| [docs/research/batch-29-t08-01-sources.md](batch-29-t08-01-sources.md) | 34 | `df327dff020ba8655c2932e18be08283835570f50a76627ae6cdbb3dc8913a3a` |
| [docs/research/batch-29-t08-02-sources.md](batch-29-t08-02-sources.md) | 35 | `ed59e237449c65553eabf8d9687f56c8863d55ff5406fc00b2ab43d46bfe0a11` |
| [docs/research/batch-29-t08-03-sources.md](batch-29-t08-03-sources.md) | 35 | `c69d7f388ba66c35dc6aaa3343a214f6be776a2d5913864d9b9c09326ad96ce1` |
| [docs/research/batch-29-t08-01-codex-recheck-2.md](batch-29-t08-01-codex-recheck-2.md) | 60 | `d99b0e5b66547c84e955edada7a41843b3a7a8648eb199d435178e0bcaa0b352` |
| [docs/research/batch-29-t08-02-codex-recheck.md](batch-29-t08-02-codex-recheck.md) | 57 | `3b91ab14ba3c34f6949e2408f5ab4a3ef818787349da5ce655ea21e1813a4712` |
| [docs/research/batch-29-t08-03-codex-recheck-3.md](batch-29-t08-03-codex-recheck-3.md) | 45 | `973cae501115d50450cf4017745a3f4b566f96c9cdc2afe234c51ff398ab5df2` |
| [docs/research/batch-30-t08-04-sources.md](batch-30-t08-04-sources.md) | 69 | `0cdd1c664108003cdf617c072ba41c6957f7942477c5a614179978304677beb2` |
| [docs/research/batch-30-t08-05-sources.md](batch-30-t08-05-sources.md) | 51 | `8a79f9b25af152402a797b30614e230141711e2df3fab4e3593b70dfe3f30d71` |
| [docs/research/batch-30-t08-06-sources.md](batch-30-t08-06-sources.md) | 67 | `7bf58328a76c22cffe153a97cbf1acf0b19b80c6ffb85c4adece2a0d129facec` |
| [docs/research/batch-30-t08-07-sources.md](batch-30-t08-07-sources.md) | 37 | `2a272ccf0088088ea4ef40d8fc718b3a3be146230a6ab89908f41209df5025cf` |
| [docs/research/batch-30-t08-08-sources.md](batch-30-t08-08-sources.md) | 54 | `e9beb7548d31824f7059ff25dce4f9021714386840d815de063053f33f1859fc` |
| [docs/research/batch-30-source-audit.md](batch-30-source-audit.md) | 33 | `b9af20e0e8683563ae0753d70f9440ab2464637a49779edceac2117a20b05254` |
| [knowledge/01-hardware/health-evidence.md](../../knowledge/01-hardware/health-evidence.md) | 455 | `415abe367d185f51e696f0f6fb2861b8b565ee5fc58c809c4080697c0a54c9b6` |
| [knowledge/00-overview/index.md](../../knowledge/00-overview/index.md) | 69 | `365231c7cc00790fc3bde9064f0ddf7513c22429f87ed5337e272dde829a8a3f` |
| [paths/roles/reading-by-role.md](../../paths/roles/reading-by-role.md) | 113 | `ae0d71db96c1ce143d41da146a15e8a49c04c198e0dcf6dd5d7fbe63f3109ce8` |
| [paths/tasks/training-triage.md](../../paths/tasks/training-triage.md) | 169 | `ec072b7b433c88e5d9d24a95e3ac15383b164a761a8aab8088c37589f838b1f4` |
| [paths/tasks/inference-triage.md](../../paths/tasks/inference-triage.md) | 143 | `569e212bf7d4348651d3e1247ff4b706a963806b362b4303162cc1162a2e86e7` |
| [sources/registry.yaml](../../sources/registry.yaml) | 7249 | `78ee35bbb0bd602d200deb5a1370af894d4765f723aeaa1970543f4be90adeed` |
| [docs/research/batch-30-t08-04-codex-recheck-5.md](batch-30-t08-04-codex-recheck-5.md) | 73 | `bfad22a042ba1e10535cf4c07c815a08cf81f0eff798ddba8e0fa97d150c0689` |
| [docs/research/batch-30-t08-05-codex-recheck-3.md](batch-30-t08-05-codex-recheck-3.md) | 65 | `fa7aabf60802c6ddf3d0afa807ff8e2233759d4206817a32ac50f5a1fd32e88e` |
| [docs/research/batch-30-t08-06-codex-recheck-4.md](batch-30-t08-06-codex-recheck-4.md) | 84 | `843897774361bb8daee5671fbcbb1763edb229e38bbc93f7832487fe15dd123d` |
| [docs/research/batch-30-t08-07-codex-recheck-3.md](batch-30-t08-07-codex-recheck-3.md) | 55 | `4b7960bbdc22ae0721b39d81584a97ea4da66e5b85260ca7f8a39c6c5388a958` |
| [docs/research/batch-30-t08-08-codex-recheck-3.md](batch-30-t08-08-codex-recheck-3.md) | 70 | `a2224e50be25e987140faae85f0a2425bdd6c0a8253675fe7d6b9b1a82c6c26e` |

