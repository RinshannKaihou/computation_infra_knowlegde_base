# Batch 31 · T00-05 定向复核报告

## 会话元数据与结论

| 项目 | 记录 |
|---|---|
| 审阅角色 / 轮次 | 原初审的同一独立审阅者；初审后第一轮定向复核；只审阅、只新增报告，不承担正文修订 |
| 指定及实际模型 / 档位 | `gpt-6.1-sol / xhigh`；实际与指定一致 |
| 核验方法 | 本轮首先读取环境 `CODEX_SESSION_ID` / `CODEX_THREAD_ID`，定位当前 rollout JSONL，核对 `session_meta` 与最新 `turn_context` 的 model、effort、cwd、collaboration_mode.settings；写入前再次读取 |
| 最新 turn_context | `model=gpt-6.1-sol`、`effort=xhigh`、`cwd=/Users/ywang2397/work/AI_reliability_knowledge_base` |
| collaboration_mode | `mode=default`；`settings={model: gpt-6.1-sol, reasoning_effort: xhigh, developer_instructions: null}` |
| 核验坐标 | `/Users/ywang2397/.codex/sessions/2026/10/22/rollout-2026-10-22T01-25-50-01a15f7f-7103-74d3-8c71-fbc7e86af45c.jsonl` **L203**；时间戳 `2026-10-21T17:34:36.888Z`；L1 为 session_meta，L204 为本轮用户消息 |
| 会话 ID / turn ID | `01a15f7f-7103-74d3-8c71-fbc7e86af45c` / `01a15f87-6a59-7e22-9780-24beffdebf10` |
| 身份结论 | 模型与推理档位符合要求；本地 Codex CLI 会话直接复核，未另启模型或子代理。引用内容中的 `[frontier_llm]` 不作为回退依据，以 turn_context 为准 |
| 日期 / 时区 | 2026-10-22 / Asia/Shanghai |
| 正文基准 | `paths/roles/reading-by-role.md`；先执行 `wc -l`：111 行；SHA-256 `441ebaa9a396d878872d31b72113a815071a23f1624263ef4bf97d0914715f8e` |
| 00 首页基准 | `knowledge/00-overview/index.md`；68 行；SHA-256 `033943144b2e87731709a4eaa3269057e33c474bbf35ee0d523f3dcf0d042159` |
| 取证记录基准 | `docs/research/batch-31-t00-05-sources.md`；31 行；SHA-256 `7c67f221daa5989ddd2beb207ac1d37ded0aea3e624f9db81b8c9e14a7065490` |
| 初审报告基准 | `docs/research/batch-31-t00-05-codex-review.md`；139 行；SHA-256 `0da82777995cdbc96e1da584763e86607097dbe107705496888919ce471ee5fc`；历史报告保留 |
| 写入范围 | 仅新增 `docs/research/batch-31-t00-05-codex-recheck.md`；不修改正文、首页、取证、registry、计划、历史报告或 build |

**复核结论：C02、C03 CLOSED；C01、C04 OPEN；新增 R01（P2，OPEN）。T00-05 暂不通过。** C01 的路线、题设和记录形式已补齐，但新增回答对目标正文的概括不准确，由 R01 具体记录，因此尚未满足“回答可由目标支持”的关闭条件。C04 的正文记录已修正，来源表仍留有相反的有效口径。实际待修内容为 R01 与 C04 两处，不将 C01 对 R01 的依赖重复算作第三处内容问题。

## 范围与方法

以[初审报告](batch-31-t00-05-codex-review.md) C01–C04 的关闭条件为准，重新读取[修订角色页](../../paths/roles/reading-by-role.md)、[00 首页](../../knowledge/00-overview/index.md)和[取证记录](batch-31-t00-05-sources.md)，不以用户的修订摘要或修订日志代替实际文件。

实际解析三例各跳的普通相对链接，打开所指段落，核对回答承载与必要先修；沿 README → 00 首页 → 角色页验证接入；独立访问修订后的 AIInfra URL 并与来源 ID 核对。对角色页所有本地内链做存在性及领域检查，未重新全量审阅兄弟篇的上游实现、历史审阅或全部技术主张。

## C01–C04 逐项复核

| 原发现 | 判定 | 已核实的修订与剩余关闭条件 |
|---|---|---|
| **C01 · P2 · 演练路线、题设、回答与先修** | **OPEN，部分满足** | 正文 L100–103 已分别记录路线与回答；① 明示 CUDA/执行期假设，增加初始化期的阅读分流；经软件栈分层的中间跳转与③经 06 首页的跳转均真实可达。② 的比较/验收与③的恢复分层由目标承载，先修可按下表复核。① 新增“三类账户”概括不符所链正文，见 R01；因此原关闭条件中的回答承载仍未全部满足。取证 L28 只能说明作者作了修改，不能代替这一核对 |
| **C02 · P2 · 00 导读接入** | **CLOSED** | README L21 → 00 首页；首页 L25、L38 两处普通链接均直接解析至本角色页。L38 区分已交付三角色与 Batch 32 尚待收口的其他导航；L68 的收尾说明已同步。角色页与首页仍为 draft，未把整个 00.6 或 Batch 32 写为完成。`updated_at` 当前均为 `2026-10-21`，本项不以日期字段推导运行验证 |
| **C03 · P3 · AIInfra 延伸入口错误** | **CLOSED** | 角色页 L109 的名称/URL 已改为 [AIInfra 项目仓库](https://github.com/Infrasys-AI/AIInfra)，与 registry 的 `src.infrasys.aiinfra` 一致。本轮 GitHub 连接器独立读取成功，返回 `full_name=Infrasys-AI/AIInfra`、相同 `html_url`。取证 L14/L30 指向既有登记；角色页 L111 和取证 L24 仍保留另核版本/许可、未逐章核查边界。没有将入口访问升级为全部章节或许可核验 |
| **C04 · P3 · 检查快照与交付口径** | **OPEN，正文子项已满足** | 正文 L99 现记 `2026-10-21 快照：128 content entries / 577 sources（含本页）`，本轮实际 `make check` 也为 128/577；交付口径已区分早期批次、后续修订/复核和本批新增，且移除了笼统的全量审阅通过声明。但取证记录 L13 的有效来源映射表仍写“目标正文（Batch 13–31 交付）”，与正文及其自身 L31 的修订日志冲突。原关闭条件要求正文与取证记录一致，尚未满足 |

### C04 的剩余修订与关闭条件

- **位置**：[取证记录](batch-31-t00-05-sources.md) L13，及其 L31 的修订自述。
- **证据**：L13 仍将“路径全部条目”统称 Batch 13–31 交付；两篇端到端在[第五批来源记录](batch-05-overview-sources.md) L3、L9–10 已记录交付，恢复一致性在[第四批记录](batch-04-training-sources.md) L12 已列为 F14。正文 L99 已承认这些早期交付，不能只在修订日志写“已改”而保留相反的来源映射。
- **关闭条件**：同步有效表格的交付/修订范围，使其与正文 L99 一致；历史轮次说明如需保留，明确其历史性质。无需改动原初审报告、重写历史来源记录或重新开展实验。128/577 与结构检查的限定范围继续保留。

## 三例跟链与先修抽查

| 演练 | 本轮实际跟链 | 回答承载与先修判断 |
|---|---|---|
| **① CUDA 训练容器执行期 OOM** | 角色页 L48/L101 → [训练全流程](../../knowledge/00-overview/training-lifecycle.md) L77 → [软件栈分层](../../knowledge/02-software-stack/layers-and-boundaries.md) L315“本章入口” → [02 首页](../../knowledge/02-software-stack/index.md) L58/L85 → [GPU 内存证据](../../knowledge/02-software-stack/gpu-memory-oom-evidence.md) L49–75 | 所有跳转存在。初始化行在此作为软件栈的阅读入口，不据其认定执行期 OOM 的根因；CUDA 与失败阶段已明确为纸面假设。术语页 L66、L74–76 承载 rank/驱动/运行时等先修。主机内存充足不能排除设备侧分配失败这一回答方向成立；“三类账户”摘要的问题见 R01 |
| **② 超节点还是集群** | 角色页 L65/L102 → [参考架构](../../knowledge/00-overview/reference-architectures.md) L117–128；再按第 2 步进入[设计目标](../../knowledge/00-overview/design-targets-and-tradeoffs.md) L133–147；参考架构 L124 也有后者链接 | 约束比较、官方样板、三窗口验收模板与假设示例均存在。架构角色 L59 要求分布式系统基础，先读形态/共享依赖再读目标与验收，顺序可复核；不要求每例机械重复同一“先修核对”标签。题目是定性比较，未知环境下没有输出实际量化选型结论 |
| **③ 故障重启后是否正确续训** | 角色页 L87/L103 → [训练排障](../../paths/tasks/training-triage.md) L96“checkpoint 读取失败或恢复后状态异常” → [06 首页](../../knowledge/06-training/index.md) L71–72 → [恢复一致性](../../knowledge/06-training/checkpoint-state-consistency.md) L150–163 | 身份/结构、逻辑进度、状态内容、同输入单步、持续窗口等回答与目标相符。L103 对“训练全流程（第 2 步）”的定位是缩写：实际可在角色第 2 步的训练排障页 **L80**，按“先用训练任务全流程”补读到训练全流程 L110–119 的四条线，再回问题表。运维第 1 步本身提供证据方法，四条线的具体承载在全流程页；本轮找到实际先修入口后，不将这一缩写另立为阻塞项 |

① 新增的初始化期分流链接也存在：[框架后端适配](../../knowledge/02-software-stack/framework-backend-adaptation.md) L53–59 提供责任/能力核对，并在 L57 指向运行时初始化语义正文。它仍是阅读入口，不证明某个初始化失败已归因于后端，也不提供已验证处方。

## 新余项

### R01 · P2 · 新增 OOM 回答把观察层次和用途分类压成“三类账户”

- **状态**：OPEN；本项记录 C01 修订新引入的回答承载问题，并阻塞 C01 完全关闭。
- **位置**：角色页 L101：“该文按设备内存、分配器 reserved/碎片、workspace 三类账户区分，定位需先归账户”。
- **问题**：这不是所链正文的准确摘要。目标文区分物理设备视角、分配器统计与用途分类，并明确 workspace/graph 私有池可以已经进入 allocated/reserved aggregate；不能将用途项当作与分配器并列的独立账户。“三类账户、先归账户”的压缩既漏掉目标文强调的观察层次，也丢失了用途与统计可重叠的边界。原句没有明说可以相加，本轮也不将其曲解为已给出求和公式；问题在于它将不同性质的观察对象概括成了正文并未定义的三账户模型。
- **证据**：[GPU 内存证据](../../knowledge/02-software-stack/gpu-memory-oom-evidence.md) **L51** 明说“至少分开四层”，列出物理设备内存、框架分配器、workspace/外部库缓存、graph 私有池等，并限定“用途分类 ≠ 互斥账户”；**L63** 说明 allocated/reserved 与碎片提示；**L73–75** 明确 workspace/graph 占用与 aggregate 的包含关系。这些既有边界没有在本轮改动，无需重审上游实现即可判断本页摘要是否忠实。
- **建议修订**：保留“主机内存充足不能排除设备侧 OOM”这一纸面回答和原有逐跳链接；删除不必要的“三类账户”机制概括，或改为准确区分观察口径与用途、说明它们不能当互斥账户相加。路径无需复制目标页的完整模型，也无需扩写领域正文。
- **关闭条件**：L101 的可支持回答与目标正文一致，不再把 workspace 用途等同于独立分配器账户；不靠单值或未声明平台/阶段下结论。三例路线和已有纸面/未实测边界保留；取证修订记录如更新，应与实际文本一致。

## 校验、回归边界与结论

本轮 `PYTHONDONTWRITEBYTECODE=1 make check` 退出码 0：**128 content entries / 577 sources**。它证明结构和本地文件链接符合检查规则，不证明演练回答、来源语义、先修或远程内容。角色页本轮为 **54 处本地链接、45 个不同目标**，文件均存在，合计仍覆盖九领域；新增直接入口未引入未交付文件。三角色五要素及 `type: path / domain: overview / status: draft` 未发生相关回归；`source_refs`、`related_ids` 仍有效。

角色页 L37、L76、L95、L104 的 draft、文档样板、未实测与七方案 0/7 边界保留。既有未改内容的初审结论仅按原范围沿用；本轮没有重新执行七方案或产生任何本地 GPU/NPU、训练、安装、恢复证据，没有评价 Batch 31 其他任务是否通过。

开始时指定复核报告不存在，作者修订和既有报告全部视为输入。对 **694 个现存文件（Git 已登记/未忽略文件及既有 build 文件）**记录 SHA-256，交付时核对既存文件无改动、无删除，唯一新增为本报告；四份输入仍为头表行数和指纹。未运行会写入 build 的 `make build`；未改 `src/kb/`，未运行 `make test`。

**最终状态：C02、C03 CLOSED；C01、C04 OPEN；R01 OPEN。** 下一轮只需核对 R01 的回答修订及 C04 的来源表同步，并检查相关链接/边界无回归；本轮不宣布 T00-05 审阅闭环，不替作者修改内容。模型审阅与结构校验均不替代真实环境验证。
