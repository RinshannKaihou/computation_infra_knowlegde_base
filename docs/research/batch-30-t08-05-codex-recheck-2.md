# Batch 30 · T08-05 第三轮定向复核报告

## 会话元数据

| 项目 | 记录 |
|---|---|
| 审阅角色 / 轮次 | 独立批次审阅者；第三轮定向复核（第二轮修订后）；本会话不承担正文编写或问题修订 |
| 约定 / 实际执行模型 | `gpt-6.1-sol / xhigh`；按用户本轮指令及[写作指南 §7](../authoring-guide.md#7-批次审阅约定)核验 |
| turn_context 核验方法 | 由环境变量 `CODEX_SESSION_ID` 定位本会话 rollout JSONL，读取最新 `turn_context` 的 `model`、`effort`、`cwd`，并核对 `collaboration_mode.settings`；不以默认配置或其他会话代替 |
| 核验结果 | 本会话只有 1 条 `turn_context`；`model=gpt-6.1-sol`、`effort=xhigh`、`cwd=/Users/ywang2397/work/AI_reliability_knowledge_base`；嵌套设置为同一模型及档位；未另启模型或子代理，未见 fallback 标记 |
| 核验坐标 | `/Users/ywang2397/.codex/sessions/2026/10/21/rollout-2026-10-21T21-38-26-01a15eaf-4099-7e43-bdb1-0f0402d2bc54.jsonl` L8；时间戳 `2026-10-21T13:38:49.976Z` |
| 会话 ID / turn ID | `01a15eaf-4099-7e43-bdb1-0f0402d2bc54` / `01a15eaf-42ae-7620-bedd-4069e972c48a` |
| 执行方式 / 日期 | 当前本地 Codex CLI 会话直接复核；本地只读检查、上游网页及 GitHub 连接器取证；2026-10-21 / Asia/Shanghai |
| 判定基准 | [初审报告](batch-30-t08-05-codex-review.md) C03、C07 原始关闭条件；[第一轮复核](batch-30-t08-05-codex-recheck.md)同两项剩余差距及 N01 关闭条件 |
| 正文快照 | [修订后正文](../../knowledge/08-reliability/test-design-and-coverage.md)，153 行；SHA-256 `34b2027ef56fd92738679875a3a80f81de59ddc1c68840201eec32a81812fe19` |
| 修订记录快照 | [来源记录](batch-30-t08-05-sources.md)，50 行，第二轮修订记录 L46–50；SHA-256 `8f7f1366af18d7858266b358e84c247d7d98f2aa03d3ebe1c4638d052e5944d0` |
| registry 快照 | [来源登记](../../sources/registry.yaml)，7226 行；SHA-256 `334b739bf47e5032bc702f87b3c23d53199dc6b8d6cd6181e35c30c37cda7536` |
| 写入范围 | 仅新增本报告；不修改正文、来源记录、registry、历史报告、计划、导航或构建产物 |

## 范围与重新取证

先读 `README.md`、`AGENTS.md`、写作指南、元数据 schema 及内容总目录。只判定 C03、C07、N01；不重审已经关闭的其他初审项。完整重读本篇现文和来源记录，按原始关闭条件核查受影响段落；作者“已关闭”的自述不代替独立判定。

| 证据 | 本轮实际读取与用途 |
|---|---|
| E1 · DCGM | 2026-10-21 分别打开[登记入口](https://docs.nvidia.com/datacenter/dcgm/latest/user-guide/dcgm-diagnostics.html)及[带 fragment 的现文链接](https://docs.nvidia.com/datacenter/dcgm/latest/user-guide/dcgm-diagnostics.html#run-levels-and-tests)，均取得 DCGM Diagnostics 正文，定向核对 Run Levels and Tests 表及其邻文。表头限定 Hopper GPU systems，并区分 4/8 卡；r1 software 为秒级，r2–r4 包含不同主动负载、时长不同。该 `latest` 页可变；本轮观察不能追记成 registry 的 2026-10-08 历史核验。用于 C03/C07/N01 |
| E2 · MLPerf | 网页工具打开[登记的固定规则文件](https://github.com/mlcommons/storage/blob/7e71ca162d8f9e7ae4b5b698d7d79b0883817f25/Submission_guidelines.md)返回 cache miss；改用 GitHub 连接器按同一 commit 重新读取原文件 L160–185，返回 blob SHA `bdd2397f5e57b708fc096744660676e27662ede4`。核对 §2.2.2.1：每客户端 `S<3M` 正文与按 `3S` 对比 `M` 的示例冲突仍存在，另有 fsync 条款；未以搜索摘要替代原件。用于确认 C07 修链没有换文件或丢失 C06 的保留边界，不重新裁定缓存处方 |
| E3 · 库内影响与恢复 | 重读[节点验收](../../knowledge/01-hardware/node-acceptance-triage.md) L43、L88–93，以及 [NCCL 实验](../../knowledge/03-communication/nccl-timeout-experiment.md) L104–123，核查只读、整机主动诊断、通信基准的资源/隔离/收尾区别；仅核查 C03 所调用的边界 |
| E4 · 登记与字符串 | 原样提取正文全部外链，与 registry 顶层 `url` 精确比较，保留 fragment，不做 URL 归一化；同时核对 `source_refs` 和来源记录。登记中的许可子链接或 notes 内链接不冒充该来源的入口 |

registry 的其他 Batch 30 修订没有被当作本篇的核验成果。新增 `src.arxiv.sdc-llm-training-2502-v1`（L7213–7226）是另一预印本修订的独立入口；本篇没有引用该 ID 或 URL，它不能补齐 DCGM 的字符串或读取记录缺口。本轮未重审该论文或兄弟篇的技术结论。

## 逐项状态

以下正文行号均对应元数据表的 SHA-256；优先级沿用原报告。

| 编号 | 优先级 | 状态 | 原关闭条件与本轮核对 |
|---|---|---|---|
| C03 | P2 | **CLOSED**（时间量级另作 P3 附注） | 原条件要求被动验收与整机主动诊断/通信基准能代入不同资源、风险、隔离和恢复要求，不能由类别名推低风险或固定耗时。正文 L46 要求逐项声明层级/工具/负载/时长/共享域，未知预算保持 unknown；L54 区分只读与主动资源，基准声明独占范围和时长；L55 基准格已删除统一“低”，补上影响随占用范围升级、防污染及结束后的资源/配置核对，验收格也明确整机基准高影响。第一轮指出的基准风险和收尾缺口已关闭；代入核查见下表 |
| C07 | P2 | **OPEN** | 原条件为正文每个外链逐字匹配登记入口，并保持 MLPerf 固定文件与冲突边界。现文共 **15 处 / 9 个唯一 URL，14 处逐字匹配**。L72、L147 的 MLPerf 链接均与固定登记完全相同，L72/L141/L147 保留冲突；L54、L151 的 DCGM 入口也匹配。但 L46 原有 `#run-levels-and-tests` 仍在，不能匹配 registry L1037 的无 fragment 入口。第一轮指出的两类字符串差异只消除一类，不能宣布全篇通过 |
| N01 | P3 | **OPEN**（部分修复） | 原条件除加入既有 ID 外，还要求在本任务来源记录/核对范围写明精确页、章节、读取日期和 latest 可变边界。正文 L17 已关联原有 DCGM ID，L151 已增加精确页与章节，依赖遗漏已修；但来源记录无 DCGM 取证行，L49–50 只说链接/依赖已登记并自判关闭，未记录本轮读取日期或 latest 边界；正文 L151 也缺这两项。registry L1035–1045 仍是 2026-10-08 历史观察，不能替代本任务的新读取记录。故完整关闭条件未满足 |

### C03 的两类代入核查

| 代入对象 | 资源与风险 | 隔离与结束核对的现有落点 |
|---|---|---|
| 被动验收：规格、状态与事件查询 | 正文 L54–55 的只读层为低成本/低影响；与节点验收 L88–89 的只读检查一致，不等同于主动负载覆盖 | 按正文 L46 记录所选查询、时长与共享域，未知条件保留 unknown；L55 验收格要求结束后核对资源/配置状态，不套用整机基准的负载预算 |
| 整机主动诊断 / 通信基准 | 正文 L54–55 明确主动资源、排空、基准独占及高影响边界；节点验收 L90/L92 和 NCCL L111 支持其计算、显存、供电散热或互联占用 | 正文 L46/L54/L55 要求明确独占范围与时长、结束核对；NCCL L108/L112/L122–123 提供独占 GPU/节点和 NIC/rail、撤销覆盖、清理进程/端口及恢复基线的具体落点。未将这些设计写成已经执行 |

P3 措辞附注：第一轮 C03 已提到，L54 仍把主动诊断/整机验收概括为“按 run level 与负载从分钟到小时级”，没有明确排除 r1 software 的秒级检查；该量级不能当成所有 run level 的预算。E1 的表头机型/卡数限制也继续适用。此处是已有措辞限制，不是第二轮修订新引入的问题；本轮考虑到现文已有按所选级别/负载声明时长与未知预算的约束，将其作为 P3 附注保留，不否定已落实的风险分级与基准收尾要求。

### 两个未闭项的最小剩余条件

- **C07**：继续处理正文 L46 的原有 DCGM 链接，保留 Run Levels and Tests 章节定位信息，同时按既定门槛使入口字符串与登记值一致；再提取全篇外链逐一比较。现有 fragment 能打开正确章节，本项不是坏链或技术反证，不应另建重复 DCGM 来源或改换文档版本来消除差异。来源记录 L49 的“DCGM Run Levels 链接对齐”尚不能覆盖全篇现状。
- **N01**：在本任务来源记录或正文来源核对范围补齐有依据的 DCGM 读取日期、章节和 latest 可变边界，区分实际新读与历史复用，不能把本报告 E1 的独立重读冒充作者此前已完成的记录。已补齐的 `source_refs` 和 L151 入口无需重复登记；来源记录 L50 的关闭自述不足以替代缺失证据。

## 新发现

无新增 N10 及后续编号。本轮 C07 的残留 fragment、N01 的读取记录缺项及 C03 的时间量级附注均已在第一轮复核中提出，不重编号，也不将其他已关闭项的附注升级成本轮新问题。

## 校验与写入边界

- 已运行 `PYTHONDONTWRITEBYTECODE=1 make check`，退出码 0：`PASS: 126 content entries; 575 sources.` 它验证结构和本地链接，不验证技术正确性或远程内容。
- 另对正文 frontmatter 执行 Draft 2020-12 schema/日期格式校验，通过；9 个 `source_refs` 均已登记，28 处本地相对链接目标存在。N01 剩余的是读取记录完整性，结构检查不会自动识别。
- 按用户“只新增该报告文件”的限定，未运行会重写 `build/` 的 `make build`；未改 `src/kb/`，未运行 `make test`。没有执行诊断、基准、清缓存、压力、注入或恢复动作。
- 开始时工作区已有作者修订及五组初审/首轮复核报告，均保留。写入前对 659 个既有非忽略文件建立路径及内容摘要，交付时这些文件不变；聚合 SHA-256 为 `bf2de0d731fe51224fac8d819f45c892a38d6de6f0eb892e01c4b2a2c3c21c69`。交付检查曾因并发新增报告引起的文件数变化而中止；已观察到其他任务新增 `docs/research/batch-30-t08-07-codex-recheck-2.md` 和 `docs/research/batch-30-t08-08-codex-recheck-2.md`。将本报告及并发新增报告单列后，原 659 个文件的数量和聚合摘要均与快照一致。本会话未创建或修改其他报告，唯一仓库写入为新增本报告。
- 只核查验证账本 V01–V07 的现有状态：均为 `planned`、`executed_at: null`、`evidence_refs: []`、`preparation_instance_ref: null`；真实执行继续 **0/7**。未重开初审 HCCL 页面读取缺口或其他已关闭项，也未补记为已核实。

**结论：本轮 1/3 CLOSED；OPEN：C07、N01；无新增发现。沿用第一轮其余 7 项已关闭状态，累计 8/10 CLOSED，T08-05 暂不通过，须完成剩余修订后再定向复核。模型审阅不替代真实环境验证。**
