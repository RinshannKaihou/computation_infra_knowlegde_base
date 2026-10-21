# Batch 30 · T08-08 定向复核报告（第二轮）

## 会话元数据与结论

| 项目 | 记录 |
|---|---|
| 审阅角色 | 独立批次审阅者；仅复核初审关闭条件及修订引入的问题，不承担正文编写或问题修订 |
| 实际执行模型 / 档位 | `gpt-6.1-sol / xhigh`，符合本次用户指定及写作指南 §7 的本轮执行要求 |
| 模型核验方法 | 以环境中的 `CODEX_THREAD_ID`、`CODEX_SESSION_ID` 定位本会话 JSONL，读取最新 `turn_context`，并核对嵌套 `collaboration_mode.settings`；不以配置默认值或其他并发会话代替 |
| 模型核验结果 | `model=gpt-6.1-sol`、`effort=xhigh`、`cwd=/Users/ywang2397/work/AI_reliability_knowledge_base`；嵌套设置为同一模型及 `reasoning_effort=xhigh` |
| 模型核验坐标 | `/Users/ywang2397/.codex/sessions/2026/10/21/rollout-2026-10-21T21-21-55-01a15ea0-21a2-7bf0-aba2-d6cf7a00a7cf.jsonl` L8；时间戳 `2026-10-21T13:22:11.516Z`；turn ID `01a15ea0-2403-78c3-9700-8ac0a27a641d` |
| 会话 ID / 执行方式 | `01a15ea0-21a2-7bf0-aba2-d6cf7a00a7cf`；当前本地 Codex CLI 会话直接审阅，`originator=codex_exec`、CLI `0.163.0`；未另启模型或审阅子代理，未观察到模型回退 |
| 日期 / 时区 | 2026-10-21 / Asia/Shanghai（UTC+08:00） |
| 写入范围 | 仅新增本报告；不修改正文、来源记录、registry、导航、计划或构建产物 |

| 复核正文 | 行数（含 frontmatter） | SHA-256 | 第二轮结论 |
|---|---:|---|---|
| [诊断评测方法规范](../../knowledge/08-reliability/diagnostic-evaluation-method.md) | 102 | `35561b63bf98e94c2a8967c8a2d6877d2325dd8d804c60b8c7248f043b9894da` | C01、C02 已关闭；C08、C09 的配套追溯问题未全部关闭 |
| [诊断评测公开题组](../../knowledge/08-reliability/diagnostic-evaluation-fixtures.md) | 130 | `77edbe7e189bd9cd5f779456b8f04ac7f6f2d0db57c0ef84d07f92f33e5b9012` | C03–C06、C10 已关闭；C07–C09 未关闭；新增 N01 |
| 合并结论 | 232 | 两篇分别核对，跨篇问题不重复计数 | **7/10 CLOSED；OPEN：C07、C08、C09。新增 N01（P2，OPEN），同时构成 C07 的剩余差距；T08-08 暂不通过** |

本报告中的“方法 L…”、“题组 L…”均指上表修订后快照；“来源记录”指 [batch-30-t08-08-sources.md](batch-30-t08-08-sources.md)。优先级沿用[初审](batch-30-t08-08-codex-review.md)：C01–C07 为 P2，C08–C10 为 P3。本轮不把作者的自述处置当作关闭证据；N01 与 C07 的剩余标注问题是同一处缺口，不重复计作两项新发现。

## 范围与取证方法

重读 `README.md`、`AGENTS.md`、写作指南、内容归属规则、两篇修订后正文、初审全部 C01–C10 的关闭条件，以及来源记录末尾 L37–48 的修订自述。定向对照 T08-08 五条 acceptance、V12 的材料与授权缺口；相邻的 checkpoint 完整性正文只用于核对新增存储题的证据边界，不作整篇重审。

重新打开 Cloud-OpsBench v1 的相关方法和指标段、Meta/Cloudflare 对应复盘段、ABFT 预印本 v1 的 §4.2 与附录 D、Llama 3 v3 的 §3.3.4/Table 5、RCACopilot v4 的许可标注，以及 PyTorch #118369 的维护者和 stale 评论。新增 PTF-10 另从 GitHub 只读连接器读取固定 commit 的 `serialization.py` L177–215、DCP `filesystem.py` L650–674、`metadata.py` L135–147；没有运行这些代码。论文同时核对 HTML 与 PDF 文本定位，下面 PDF 文件页序均从 1 起算；未声称完成 PDF 图像的视觉校验。

## 逐项状态表

| 编号 | 优先级 | 状态 | 复核依据 |
|---|---|---|---|
| C01 | P2 | **CLOSED** | 方法 L84 已删除 ZTDR 与 abstention 的等同关系，分别说明“有工具但仍武断归因”和“无工具但正确保留 unknown”两类情况；L66、L81 与题组 L101–102 继续按证据充分性判断弃答。重新核对 [Cloud-OpsBench v1 §4.2.2](https://arxiv.org/pdf/2603.00468v1#page=12)（印刷页 12 / 文件页 12）：ZTDR 的统计对象确为没有有效工具调用即生成最终结果的 episode；修订后的区分成立 |
| C02 | P2 | **CLOSED** | 方法 L42 现在区分冻结的输入/oracle/rubric/权重与预先声明的模型、提示词、知识版本等候选变量，并明确试卷变化时重跑共同候选或停止裸分比较。对照 [Cloud-OpsBench v1 §3.2、§4.1、§4.6](https://arxiv.org/html/2603.00468v1)及 V12 method_steps，已能描述同一协议下比较两个候选的条件，也能说明何时须重建基线 |
| C03 | P2 | **CLOSED** | 题组 L70–72 改为容量评估命令、审计阻止失败和骨干连接断开；保留具体下发/撤销机制 unknown，区分 DNS 进程运行、公网不可达、内部工具依赖和网络访问失效。重新核读 [Meta 对应段落](https://engineering.fb.com/2021/10/05/networking-traffic/outage-details/)与 [Cloudflare 观测时间线](https://blog.cloudflare.com/october-2021-facebook-outage/)，修订后的必答事实与披露范围相符；共享控制路径已标为本库归纳。正文入口的读取问题归 C08，不据此重开本项技术表述 |
| C04 | P2 | **CLOSED** | 题组 L84–86 明确两种 dtype、不同实验设置、节点差异与间歇尖峰，并认可拒绝直接配对计算漏检率的回答。重新核对 [arXiv v1 §4.2、D.1–D.3](https://arxiv.org/html/2502.12340v1)：float32 ABFT 与 bf16 失配率不必对应，三种原因仍为可能解释；[PDF D.1–D.3](https://arxiv.org/pdf/2502.12340v1#page=16)位于印刷页 16 / 文件页 16。技术关闭条件满足，登记入口问题另归 C08 |
| C05 | P2 | **CLOSED** | 题组 L91–93 已排除“同型集群参照区间”，明确 1.4% 的条件分母为该快照 419 次意外中断，仅作带条件的来源观察或调查背景。重新核对 [Llama 3 v3 §3.3.4/Table 5](https://arxiv.org/pdf/2407.21783v3#page=13)（印刷页 13 / 文件页 13），平台/窗口及 confirmed-or-suspected 边界保留，未要求跨集群迁移区间 |
| C06 | P2 | **CLOSED** | 题组 L96–102 已将 PTF-08 的公开 Unknown 类别与本地假设情境分列，明确本库无该事件记录，U 级结论由给定证据不足推出。L21、L36 与来源记录 L44 均显式提到 PTF-08 的合成身份；[Table 5](https://arxiv.org/pdf/2407.21783v3#page=13)只承担公开类别来源，不再冒充本地事件证据。本项针对 PTF-08 的原缺口已关闭；后来新增 PTF-10 的同类问题单列 N01 |
| C07 | P2 | **OPEN** | 题组 L105–110 的 PTF-10 已提供实际存储完整性判据和固定证据，L123 给出六域及 U 级题号映射，总数为十题，公开身份仍清楚；不再仅靠 PTF-01 的 optimizer-state 语义声称存储覆盖。但本项关闭条件还要求“新增合成内容准确标注”：PTF-10 的现场情境没有公开事件记录或合成标注，且 L36 仍称除 PTF-08/09 外均为来源事实。该条件未满足，见 N01 |
| C08 | P3 | **OPEN** | 来源记录 L19 的 Meta ID 与 registry 中 RCACopilot v4 的 CC-BY-4.0 已修正，许可可由 [v4 页面](https://arxiv.org/html/2305.15778v4)核实；但题组外链去除页内 fragment 后仅 **8/12** 与登记 `url` 逐字一致，方法为 **6/6**。PTF-06、PTF-07/08 及新增 PTF-10 仍有入口差异；Meta 虽机械对齐旧登记入口，本轮仍未能用阅读工具打开它。剩余差距见下表 |
| C09 | P3 | **OPEN** | 方法 L84、L99 的 v1 §4.2、题组 L85 的 arXiv v1 D.1–D.4，以及 L92/L101 的 Llama v3 §3.3.4 均已核正，registry 也补了两版 ABFT 的对应说明。但来源记录的主张定位表仍在 L10 链到 Cloud 无版本入口并写“§5 指标定义”，L22 仍写 Llama“§2.2＋Table 5”，L21 仅写“附录 D”而不选择版本；末尾自述没有消除表内冲突。初审要求的正文、取证表、registry 同步尚未完成，详见下文 |
| C10 | P3 | **CLOSED** | 题组 L54 已改为“本事件根因 U；机制依据”，与 L58 的 suspected 及不能断言 confirmed 一致，不再使用未定义的“C→A 部分”。重新读取[维护者后续评论](https://github.com/pytorch/pytorch/issues/118369#issuecomment-1973742710)和 [stale 关闭评论](https://github.com/pytorch/pytorch/issues/118369#issuecomment-4383979717)，没有将机制知识或关闭状态升级为本事件根因闭合 |

## 未闭项的剩余差距

### C07：存储判分内容已补齐，新增输入的来源身份尚未补齐

固定 [serialization.py L196–209](https://github.com/pytorch/pytorch/blob/1eba9b3aa3c43f86f4a2c807ac8e12c4a7767340/torch/serialization.py#L196-L209)的文档字符串说明，关闭 CRC32 计算后，外部解压可能报 CRC 问题而 `torch.load` 仍可加载。这足以反驳“能加载必然代表字节正确”的保证。固定 [filesystem.py L650–674](https://github.com/pytorch/pytorch/blob/1eba9b3aa3c43f86f4a2c807ac8e12c4a7767340/torch/distributed/checkpoint/filesystem.py#L650-L674)另显示加载、切片与形状断言，不能把形状相符当作内容级校验。因此本轮认可 PTF-10 已形成可核对的存储观察与判据。

但代码与文档不能证明题组 L107 所述“训练继续后偶发异常、现场有人断言计算侧有问题”的事件发生过。按 C07 原关闭条件，仍须处理 N01：明确该情境为构造输入，或提供可追溯的真实公开事件记录；同步摘要、verification notes、来源记录与题号映射中的合成范围。本项不要求执行保存、损坏注入或加载实验。

### C08：逐字映射仍未完成，Meta 入口也未恢复为可核读入口

下面的比较只去除页内 `#…`，不把不同版本或不同载体自动视为同一登记入口。

| 位置 | 正文外链 | 对应登记入口 / 尚缺事项 |
|---|---|---|
| 题组 L85，PTF-06 | `https://arxiv.org/abs/2502.12340v1` | registry L7022 仍为 `https://aclanthology.org/2025.acl-long.996/`。revision 已解释两版差异，但未形成与正文逐字对应的 arXiv v1 登记入口；应分别登记，或采用 ACL 版并同步其节号，不能只换链接 |
| 题组 L92、L101，PTF-07/08 | `https://arxiv.org/abs/2407.21783v3` | registry L7036 仍为 `https://arxiv.org/abs/2407.21783`；版本固定是正确方向，还须同步登记入口 |
| 题组 L108，PTF-10 | 固定 commit 的 `torch/serialization.py` 文件入口 | 新加入的 `src.pytorch.dcp-2.6` 主 `url` 在 registry L310，仍为 `https://docs.pytorch.org/docs/2.6/distributed.checkpoint.html`。notes 能关联该 commit 与文件，未满足原关闭条件中的入口逐字映射；须补精确文件登记或等效的明确入口安排 |
| 题组 L71，PTF-04 | `https://engineering.fb.com/2021/10/05/networking/outage-details/` | 与 registry L6961 相同，但网页工具返回不可访问；本轮成功核读的是 [networking-traffic 路径的实际复盘](https://engineering.fb.com/2021/10/05/networking-traffic/outage-details/)。应同步实际核读入口，或补旧入口可用/跳转的证据。工具失败不证明某个 HTTP 状态，也不反证复盘内容 |

RCACopilot v4 的许可类型、Meta 来源 ID 两个子问题已关闭；不因这些局部修复把整项判 CLOSED。以上残留均纳入 C08，不另编新发现重复计数。

### C09：正文坐标已核正，取证表仍会把读者带回旧版本/错误章节

来源记录 L10 的链接实际仍是 [Cloud 无版本入口](https://arxiv.org/abs/2603.00468)，本轮重新打开显示 **v2**；该行却自称 v1 并将指标定位到 §5。实际 [v1 §4.2](https://arxiv.org/pdf/2603.00468v1#page=11)位于印刷页 11–12 / 文件页 11–12。来源记录 L22 的 Llama §2.2 同样未改；其 [v3 Table 5](https://arxiv.org/pdf/2407.21783v3#page=13)仍在 §3.3.4、印刷页 13 / 文件页 13。来源记录 L21 以 ACL 主入口 ID 只写“附录 D”，也没有像题组 L85 那样注明采用 arXiv v1 的 D.1–D.4。

来源记录 L46–47 的末尾修订自述能说明作者意图，但没有明确将前表废止为历史快照；该表仍以“精确位置”提供现行追溯。须将这些表项同步到实际采用的固定版本、对应节号及 PDF 双页码，或明确给出逐项替代定位，使读者不用在相互冲突的表述中自行选择。正文现在的正确坐标应保留，不要求升级到 Cloud v2。

## 新发现

### N01 · P2 · OPEN · 新增 PTF-10 的现场情境未标合成，与“仅两条合成”声明冲突

- **位置**：题组 L21、L36、L105–110、L123；来源记录 L45。
- **问题**：PTF-10 输入采用已经发生的现场叙事：“读回成功、训练继续、恢复后偶发数值异常”，以及现场人员的判断；oracle 只有固定源码和本库概念正文，没有这起事件的独立记录。本条也未标为假设/合成。与此同时 L36 明说合成“共两条，其余为公开来源事实”，L123 的合成映射只列 PTF-09，甚至遗漏已明确标注的 PTF-08。读者无法可靠区分公开机制事实与作者新构造的诊断情境。
- **证据**：重新读取的固定 [serialization.py L177–215](https://github.com/pytorch/pytorch/blob/1eba9b3aa3c43f86f4a2c807ac8e12c4a7767340/torch/serialization.py#L177-L215)记录的是 CRC32 选项、默认值与加载兼容性说明，不是训练事故记录；[Checkpoint 完整性正文](../../knowledge/04-data-storage/checkpoint-integrity-evidence.md) L92、L114 仍保留 C++ reader 路径和全部实测未执行的边界。来源记录 L45 也只登记新增题及代码机制，没有事件取证。这是缺少标注/来源的判断，不是断言该类事件不可能发生。
- **建议**：将 PTF-10 标为“基于固定公开源码构造的假设教学情境”，分别标出来源机制与假设症状；或者补真实公开事件的固定记录。若采用合成路径，同步摘要、verification notes、来源记录及合成题号映射，明确 PTF-08 的本地情境、PTF-09 与 PTF-10 的范围；不把它们用于证明事故发生率或已完成本地复现。
- **关闭条件**：读者能直接识别 PTF-10 的来源身份；每项输入事实与设定有可追溯边界，所有合成范围声明一致。此条件同时满足 C07 尚未完成的“新增合成内容准确标注”要求。

## 校验、限制与写入声明

两篇 frontmatter 已通过本地 JSON Schema（含日期格式）检查，均保持 `reference / reliability / draft / generic / source_checked`；相关 `source_refs` 均可解析，正文相对文件链接目标存在。URL 比较结果是方法 6/6、题组 8/12；这是入口字符串检查，不是远程内容或兼容性证明。

本轮只新增审阅报告，没有修订知识正文或代码；按用户限定未运行会生成产物的 `make build`，也未运行 `make check`、`make test`。上述定向只读检查不等于仓库全量校验。未执行正文、源码、论文或网页中的命令，没有运行评测系统、故障注入、恢复操作或 GPU/NPU 测试。对 PTF-10 的核对是固定 Python 源码与文档证据核对，不宣称已逐行验证 C++ reader 的全部分支。

开始时工作区已有作者修订及多份未跟踪初审报告；期间另见并发出现的 `batch-30-t08-07-codex-recheck.md`，本会话没有读取或写入其正文。写入前后核对本任务输入快照；除上表两篇正文外，初审报告 SHA-256 为 `b9358fd085ed468ef52c0e793266c42135ad4fac3cb247f6b63f07885ba1a9f0`，来源记录（48 行）为 `8d1ea2c6ba37b4a62cf5d888782a47f823ba35324733724f66975dd8f2cdc832`，registry（7212 行）为 `36d2d69cdd0cf539b74c1f68d9e582ddf01b27976b237910969ef4000d6cb34a`；本会话不改动这些输入。

V12 仍没有本轮取得的独立输入/答案、授权审查或执行记录；公开十题及本次模型复核均不能关闭该验证缺口。模型审阅不替代真实环境验证，本报告也不对其他 T08 任务或整个 Batch 30 作通过声明。

## 结论

**7/10 CLOSED；OPEN：C07、C08、C09；新增 OPEN：N01（与 C07 剩余条件重合）。T08-08 暂不通过，须由作者完成上述修订后继续定向复核。**
