# Batch 30 · T08-07 定向复核报告（第二轮）

## 会话元数据与结论

| 项目 | 记录 |
|---|---|
| 审阅角色 | 独立批次审阅者；仅复核初审关闭条件及修订引入的问题，不承担正文编写或修订 |
| 约定 / 实际执行模型 | 本次用户指定 `gpt-6.1-sol / xhigh`；实际核验一致 |
| turn_context 核验方法 | 由环境变量 `CODEX_THREAD_ID` 定位本会话 JSONL，核对 `session_meta.id` 与本会话首条进度消息，再读取该文件最新 `turn_context`；未使用配置默认值或其他会话记录代替 |
| turn_context 核验结果 | `model=gpt-6.1-sol`、`effort=xhigh`、`cwd=/Users/ywang2397/work/AI_reliability_knowledge_base`；`collaboration_mode.settings.model/reasoning_effort` 同值；核验时该文件共 1 条 `turn_context` |
| 核验坐标 | `/Users/ywang2397/.codex/sessions/2026/10/21/rollout-2026-10-21T21-21-55-01a15ea0-21a3-79e2-80e2-e58fc455837c.jsonl` L8；时间戳 `2026-10-21T13:22:11.334Z`；本会话首条进度消息在 L13（`2026-10-21T13:22:16.361Z`） |
| 会话 ID / turn ID | `01a15ea0-21a3-79e2-80e2-e58fc455837c` / `01a15ea0-2402-7072-9258-2ba650c5de57` |
| 执行方式 | 当前本地 Codex CLI 会话直接复核，`session_meta.originator=codex_exec`，`workspace-write`；未另启模型、OpenCode 或审阅子代理；初审的实际模型及会话坐标原样保留 |
| 日期 / 时区 | 2026-10-21 / Asia/Shanghai（UTC+08:00） |
| 初审基准 | [初审报告](batch-30-t08-07-codex-review.md)，127 行；SHA-256 `8fd2233be0103de03f7d6de0cbe1ee86ee9a2cee8da7ba12633164d75d28e6ec` |
| 修订正文基准 | [事故复盘、来源更新与知识维护](../../knowledge/08-reliability/postmortem-and-knowledge-update.md)，146 行；SHA-256 `1d5ed2c1eeb4a35b56eb63c69394ce87cc0a7f483a6fa60bd368718f3f50da1c` |
| 修订记录基准 | [本任务来源记录](batch-30-t08-07-sources.md)，37 行；SHA-256 `dcf12593bc9a2d208532bcda8ec55419d511c56b2ab67c136e161820bf308a8d`；作者逐项处置在 L31–37 |
| registry 基准 | [来源登记](../../sources/registry.yaml)，7212 行；SHA-256 `36d2d69cdd0cf539b74c1f68d9e582ddf01b27976b237910969ef4000d6cb34a` |
| 适用范围 | 本轮只检查 C01–C05 的证据链及其修订后果；不重复整篇初审，不审核 Batch 30 其他任务 |
| 写入范围 | 仅新增本报告；保留会话开始前已有的工作区变更，不修改正文、来源记录、registry、计划或生成清单 |

**复核结论：初审 4/5 CLOSED，C04 OPEN；新增 N01（P3）OPEN。合计 4/6 CLOSED，T08-07 本轮暂不通过。** C04 的 ID 和 URL 字符串失配已修正，剩余的是所选精确入口的独立访问证据。C02 按 CLOSED-with-note 处理，其 P3 建议不计为未闭项。来源核对、模型审阅与真实环境验证分别记录；本报告不建立 GPU/NPU 环境验证结论。

优先级沿用初审：P1 为关键错误，P2 为影响技术准确性、证据边界或验收的必修事项，P3 为局部措辞与可追溯性问题。下文正文、来源记录及 registry 行号均对应上表摘要。

## 逐项关闭状态

| 编号 | 初审优先级 | 状态 | 关闭条件复核与依据 |
|---|---|---|---|
| C01 | P2 | **CLOSED** | 正文 L81 已分列运营方机制与外部发现时刻，删除撤销失败和第二起独立事故，区分 BGP 撤告、服务器运行与互联网不可达；命令细节保持 unknown，confirmed 限定为运营方自述。独立重开 Meta 可读入口与 Cloudflare 原页，核对命令/审计工具、撤告、恢复风险和两个发现时刻；与库内来源案例 L42、L48–63、L88 一致。具体证据见下文。 |
| C02 | P2 | **CLOSED** | 正文 L53 将保全动作限定为现场工具已具备采集/导出条件时保存可获取证据，删除普遍的“转储前先拷贝”，明确未配置/未采到要记缺口、无文件不能推出无异常。新增 `src.arxiv.llama3-infrastructure` 已列入正文 L16 并能解析；其固定 v3 §3.3.4 确有环形缓冲与自动转储实践。配置文档未登记的缺口已明示，现场先核对配置，未承诺任意环境自动转储。保留一条 P3 措辞建议，见下文。 |
| C03 | P2 | **CLOSED** | 正文 L85、L89–105 将 source/release/patch/case 更新追到来源登记、受影响 ID、修订、独立技术审阅、导航与第六步结构检查/catalog 重建；L99–102 明确从源文件生成、核对受影响 ID 的路径/元数据/摘要、登记者确认和失败阻断。L129 完成判据同步包含第六步。符合任务 acceptance 第三条（任务表 L7039）；本轮不以执行构建替代对流程文本的判断。来源记录遗留的五步概括另记 N01。 |
| C04 | P3 | **OPEN** | 来源记录 L19 已统一为存在的 `src.meta.oct4-2021-postmortem`；正文 L144 与 registry L6961 的 `/networking/outage-details/` 逐字一致，正文全部 7 处远程内联链接也均匹配登记入口。但本轮网页工具无法读取所选精确入口，本地直连 DNS 失败，浏览器补证通道亦未能使用；可读的 `/networking-traffic/` 原文不足以证明登记入口的响应或重定向。正文 L144 新写“两路径形态均可达”，本轮无法独立确认。关闭所需的入口核验仍缺证，详见下文。 |
| C05 | P3 | **CLOSED** | 正文 L57 已将一周内写成并流转、拖四个月分别绑定好坏案例，明确上游没有统一时限、本库若设时限须另行规定。来源记录 L9 只记发布时机、L37 准确说明收窄；registry L7103 为“一周内 vs 四个月反例”，未再声称模板统一规定七天。独立重读 Workbook 的 Promptness 与 Delayed publication 两处，支持上述处理。 |

## 定向证据核对与剩余差距

### C01：示例事实与时间线已纠正

重开 [Meta 原文的可读入口](https://engineering.fb.com/2021/10/05/networking-traffic/outage-details/)，核对命令/审计工具段（以 `During one of these routine maintenance jobs` 定位）、DNS 撤告段（以 `To ensure reliable operation` 定位）与恢复部分。原文支持容量评估命令造成骨干断连、保护工具未正确阻止、DNS 撤告而服务器仍运行；恢复期担忧与实际恢复结果分别叙述。正文 L81 的修订与这些边界相符，未增加命令内容或内部时刻。

[Cloudflare 原文](https://blog.cloudflare.com/october-2021-facebook-outage/)的开事故单段及 BGP 小节分别支持 15:51 UTC 的内部事故单、15:58 UTC 注意到 DNS 前缀已停止宣告。正文将其标成观测方发现时刻，并与运营方机制顺序分列。库内[相关故障来源案例](../../knowledge/08-reliability/correlated-failure-source-case.md)的相应边界未被修订示例突破。上述事实核对可关闭 C01；Meta 登记入口的访问核验单列于 C04。

### C02：原则与实践示例已有各自依据，保留 P3 注记

[Effective Troubleshooting 的 Triage 小节](https://sre.google/sre-book/effective-troubleshooting/)支持在缓解期间保留日志等后续分析证据；[Llama 3 固定 v3 §3.3.4](https://arxiv.org/html/2407.21783v3)的 Flight Recorder 段描述 PyTorch 内置记录器、环形缓冲，以及其 NCCLX 训练实践中的 watchdog/心跳超时转储。registry L7039 已定位固定 v3 与正确章节，L7047 将材料边界限定在论文环境。正文当前将这段作为论文实践举例，并要求先核对现场配置，故无条件操作预设已消除。

本轮也重开 [PyTorch 官方教程的启用小节](https://docs.pytorch.org/tutorials/unstable/flight_recorder_tutorial.html#enabling-flight-recorder)及 [PyTorch 2.14 ProcessGroupNCCL 变量页](https://docs.pytorch.org/docs/2.14/torch_nccl_environment_variables.html)，确认采集、转储和持久保存应区分，转储开关需与正的 trace buffer 大小配套。这只用于核对修订中的配置依赖提醒，不为作者补登记，也不建立论文内部栈与 PyTorch 2.14 的版本对应关系。

**P3 注记（CLOSED-with-note）**：正文 L53 可直接标明“PyTorch 内置 NCCL Flight Recorder；论文的 NCCLX 实践”，并把 §3.3.4 做成精确链接，便于读者识别工具所属层次和论文后端语境。现有“Llama 3 论文描述的实践”与现场配置限制已足以满足本项关闭条件；本注记不要求扩写组件配置指南或执行训练。

### C04：字符串已对齐，精确入口仍缺独立访问证据

本轮实际观察如下：

- 网页工具打开登记的 [Meta `/networking/` 精确入口](https://engineering.fb.com/2021/10/05/networking/outage-details/)返回不可访问，未取得该入口的正文、HTTP 状态或重定向链；打开 [另一个 `/networking-traffic/` 入口](https://engineering.fb.com/2021/10/05/networking-traffic/outage-details/)能读取同题原文。
- 本地 `urllib` 对两个入口的只读请求均因 DNS 解析失败而未取回页面，不能据此认定任何一个入口在公网失效。
- 按 `kimi-webbridge` 技能（本机路径 /Users/ywang2397/.agents/skills/kimi-webbridge/SKILL.md）检查补证通道，状态为 `running:false`；未启动守护程序或更改配置。Computer Use 的 IAB 不可用，Edge 只读访问请求返回 `Computer Use was not approved to use Microsoft Edge`，没有取得浏览器页面证据。

因此，C04 保留为**部分修正、证据未闭合**。作者需提供所选精确入口实际到达该原文的可复查响应或重定向证据，并保留工具、日期及访问结果；或经核实后由编写/登记角色同步采用可读入口。正文 L144 关于两个入口均可达的观察也需有相应依据。下一轮只复核这一剩余条件即可，不需重复整篇事实审阅。本轮不判断登记 URL 是否全局失效。

### C05：时效表述回归案例评价

独立重读 [Workbook 原章](https://sre.google/workbook/postmortem-culture/)的 Promptness 与 Delayed publication：两处分别评价好案例的及时写成/流转和坏案例的延迟发布。正文、取证表与 registry 目前均未将它们提升为统一七天时限，关闭条件满足。

## 修订引入的新发现

### N01 · P3 · 来源记录仍把现行六步流程概括为五步

- **状态**：OPEN。
- **位置**：[来源记录](batch-30-t08-07-sources.md) L23；对照同文件 L35、[正文](../../knowledge/08-reliability/postmortem-and-knowledge-update.md) L89–102/L129。
- **证据与影响**：正文为关闭 C03 新增第六步“结构检查与 catalog 重建”，修订记录 L35 也说明已补第六步，但“本文原创部分”仍写“五步追溯链（登记→反查→修订→定向审阅→导航）”。该处没有历史轮次标签，仍作为现行内容概括，遗漏新增的完成门槛，与正文 L94 要求正文和来源记录同步的规则不一致。这是本次扩展流程后形成的记录矛盾；正文中的 C03 实质修订已满足，故不重开 C03。
- **建议**：由作者将该现行概括同步为包含结构检查/catalog 重建的六步链；若保留五步旧描述，应明确标为初审前历史记录，并给出现行六步口径。
- **关闭条件**：来源记录的现行流程概括与正文及复核轮修订记录一致，不再将停在导航的五步称为本次交付的完整追溯链。无需增加新系统或实验。

## 检查与写入边界

只读定向检查结果：正文 frontmatter 通过 Draft 2020-12 schema 与日期格式校验；8 个 `source_refs` 全部可解析；来源记录中的来源 ID 全部存在；7 处远程内联链接（5 个唯一 URL）均与 registry 某条 `url` 逐字匹配；7 处正文相对链接目标均存在。此类本地匹配不证明远程入口可读，C04 仍按独立访问结果判断。

本轮只新增研究审阅报告，未修改知识正文或构建输入，未运行 `make check`、`make build` 或 `make test`；按本次仅新增一份报告的写入范围，不重建或改写生成清单。C03 的关闭依据是维护流程文本已补齐，不能据此宣称作者已完成一次实际维护链执行。本轮没有诊断、负载、恢复或故障注入，也没有现场采集或硬件验证。

写入后比对会话基准：除本报告外，已登记的工作区文件内容未改变。正文保持 `draft / source_checked`；本报告不修改计划、导航或 Batch 30 的总体结论。

**T08-07 第二轮结论：4/5 初审发现 CLOSED；OPEN：C04。新增 OPEN：N01（P3）。合计 4/6 CLOSED，暂不通过；修订/补证后仅对 C04、N01 再作定向复核。**
