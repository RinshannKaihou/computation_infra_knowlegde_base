# Batch 31 · T00-05 第二轮定向复核报告

## 会话元数据与结论

| 项目 | 记录 |
|---|---|
| 审阅角色 / 轮次 | 原独立审阅者；第二轮定向复核；仅核对 R01、C04 关闭条件与相关回归，不承担正文修订 |
| 指定及实际模型 / 档位 | `gpt-6.1-sol / xhigh`；实际与指定一致 |
| 核验方法 | 本轮首先由环境 `CODEX_SESSION_ID` / `CODEX_THREAD_ID` 定位当前 rollout JSONL，读取最新 turn_context 的 model、effort、cwd 与 collaboration_mode.settings，并核对 session_meta |
| 最新 turn_context | `model=gpt-6.1-sol`、`effort=xhigh`、`cwd=/Users/ywang2397/work/AI_reliability_knowledge_base` |
| collaboration_mode | `mode=default`；`settings={model: gpt-6.1-sol, reasoning_effort: xhigh, developer_instructions: null}` |
| 核验坐标 | `/Users/ywang2397/.codex/sessions/2026/10/22/rollout-2026-10-22T01-25-50-01a15f7f-7103-74d3-8c71-fbc7e86af45c.jsonl` **L285**；时间戳 `2026-10-21T17:39:33.914Z`；L1 为 session_meta，L286 为本轮用户消息 |
| 会话 ID / turn ID | `01a15f7f-7103-74d3-8c71-fbc7e86af45c` / `01a15f8b-f29d-79d3-b707-b432270f68c1` |
| 身份结论 | 符合本轮模型与档位要求；本地 Codex CLI 会话直接复核，未另启模型或子代理。引用文字中的 `[frontier_llm]` 不构成回退，以 turn_context 为准 |
| 日期 / 时区 | 2026-10-22 / Asia/Shanghai |
| 正文基准 | `paths/roles/reading-by-role.md`，先执行 `wc -l`：111 行；SHA-256 `5813e26248f6e3af27f85c2e5fcadc9d7630b45e91c684f241b747001044ee98` |
| 取证记录基准 | `docs/research/batch-31-t00-05-sources.md`，32 行；SHA-256 `a59bbec83efa0e7851b84a8ae6bbb9b68f755379513a4383564a212d8947b02d` |
| 第一轮复核基准 | `docs/research/batch-31-t00-05-codex-recheck.md`，74 行；SHA-256 `8d0058d38409306ae9478fe42779ce21f9e7c239008c1483c4c8406808485bc0` |
| 00 首页指纹 | `knowledge/00-overview/index.md` SHA-256 `033943144b2e87731709a4eaa3269057e33c474bbf35ee0d523f3dcf0d042159`，与第一轮复核一致 |
| 写入范围 | 仅新增 `docs/research/batch-31-t00-05-codex-recheck-2.md`；其他文件不修改 |

**结论：R01 CLOSED、C04 CLOSED；C01 的最后阻塞随 R01 关闭。结合此前 C02、C03 的关闭记录，初审 C01–C04 与新增 R01 已全部 CLOSED，OPEN 为 0。本轮无新增余项，无 R02。T00-05 在初审及两轮定向复核的限定内容审阅范围内通过。** 不代表整个 Batch 31 通过，也不代表 GPU/NPU 或恢复实验验证通过。

## 范围与核对依据

只对照[第一轮复核](batch-31-t00-05-codex-recheck.md)中 R01 和 C04 的关闭条件，读取[角色页](../../paths/roles/reading-by-role.md) L99–111、[取证记录](batch-31-t00-05-sources.md) L13、L28–32，以及被调用的 [GPU 内存证据](../../knowledge/02-software-stack/gpu-memory-oom-evidence.md) L51、L63、L73–75。既有三例路线、首页接入与未实测边界仅检查相关回归，不重新全量审阅兄弟篇或获取新的上游技术来源。

为核对实际修改范围，在内存中将当前正文的新回答换回上一轮原句，所得 SHA-256 精确恢复为第一轮正文基准 `441ebaa9a396d878872d31b72113a815071a23f1624263ef4bf97d0914715f8e`；将取证表 L13 换回原行并移除新增 L32，所得 SHA-256 精确恢复为第一轮取证基准 `7c67f221daa5989ddd2beb207ac1d37ded0aea3e624f9db81b8c9e14a7065490`。因此，两份输入相对上一轮分别仅有该处回答替换，以及来源表同步和一条修订记录新增；未向磁盘写入还原副本。

## 逐项关闭判定

| 项目 | 判定 | 证据与关闭条件核对 |
|---|---|---|
| **R01 · P2 · OOM 回答的账户概括** | **CLOSED** | 正文 L101 已改为“至少分开四层观察”，列出物理设备内存、框架分配器统计、workspace/外部库缓存、graph 私有池；明确用途分类不是互斥账户、占用可已计入 allocated/reserved 聚合、不能跨口径相加。该摘要与目标正文 L51、L63、L73–75 的观察层次和包含关系一致，不再建立“三类账户”模型。CUDA/执行期题设、初始化期分流和“不以主机内存单值排除设备侧问题”的边界保留；取证 L32 与实际修订一致 |
| **C04 · P3 · 来源映射的交付口径** | **CLOSED** | 取证 L13 的有效表格现已区分早期 Batch 01–12 交付、其中多篇经 Batch 13–31 修订/复核、本批新增见 Batch 31 记录，与正文 L99 一致；不再仅在修订日志声称已改。取证 L31–32 与有效表格相符，L3 仍是明确标注“作者角色首轮”的历史轮次说明，不再与有效映射表混淆。正文 L99 的 128/577（含本页）及结构检查限定保留，本轮实际检查计数一致 |
| **C01 · 原 P2 · 演练验收的最后阻塞** | **CLOSED，随 R01 解除** | 第一轮已核实三例的路线、题设、先修与②③回答，仅①新回答的承载受 R01 阻塞。本轮 R01 满足关闭条件，且三例路线未改、实际跳转仍存在，因此 C01 的最后余项关闭；不重复计为新的发现 |

C02、C03 沿用第一轮 CLOSED 结论；本轮没有重新声称完成远程仓库全部章节或许可核验。

## 相关无回归检查

- **演练①**：角色页 → [训练全流程](../../knowledge/00-overview/training-lifecycle.md) L77 → [软件栈分层](../../knowledge/02-software-stack/layers-and-boundaries.md) L315 → [02 首页](../../knowledge/02-software-stack/index.md) → GPU 内存证据；各跳仍有真实链接，新增回答没有改变平台/阶段假设或阅读分流。
- **演练②③**：角色页 → [参考架构](../../knowledge/00-overview/reference-architectures.md) → [设计目标](../../knowledge/00-overview/design-targets-and-tradeoffs.md)，以及角色页 → [训练排障](../../paths/tasks/training-triage.md) → [06 首页](../../knowledge/06-training/index.md) → [恢复一致性](../../knowledge/06-training/checkpoint-state-consistency.md)，各跳仍存在。其回答与先修的既有判断按第一轮范围沿用。
- **接入及边界**：README → 00 首页 → 角色页仍可达；首页两处角色链接、Batch 32 待收口边界及页尾 AIInfra 登记 URL 未变。角色页全部 **54 处本地链接、45 个不同目标**仍指向现存文件。正文 L37、L76、L95、L104 的 draft、文档样板、未实测、纸面演练和七方案 0/7 边界保留。

## 校验、写入与结论

`PYTHONDONTWRITEBYTECODE=1 make check` 通过：**128 content entries / 577 sources**。该结果只验证结构和本地文件链接，不证明技术正确性、远程内容或环境兼容性。未执行正文中的命令或实验，未运行会写入 build 的 `make build`；未改代码，未运行 `make test`。

开始时指定报告不存在；对 **695 个现存文件（Git 已登记/未忽略文件及既有 build 文件）**记录 SHA-256，交付时核对既存文件无改动、无删除，唯一新增为本报告。正文、取证和历史复核报告保持头表行数及指纹，未代改任何输入。

**T00-05 审阅闭环：C01–C04、R01 全部 CLOSED，OPEN 为 0，本轮无新增发现。** 通过的是角色导航、演练记录、来源映射与证据边界的既定审阅范围；正文仍为 draft，真实验证轨道及七方案 0/7 保持原状态。
