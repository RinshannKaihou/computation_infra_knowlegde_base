# Batch 30 · T08-05 第四轮定向复核报告

## 会话元数据

| 项目 | 记录 |
|---|---|
| 角色 / 轮次 | 独立批次审阅者；第四轮定向复核（第三轮修订后）；不承担正文编写或问题修订 |
| 约定 / 实际模型 | `gpt-6.1-sol / xhigh`，与本轮用户指令一致 |
| turn_context 核验方法 | 用环境变量 `CODEX_SESSION_ID` 定位本会话 rollout JSONL，读取最新 `turn_context` 的 `model`、`effort`、`cwd`，同时核对 `collaboration_mode.settings`；不以默认配置或其他会话代替 |
| 核验结果 | 共 1 条 `turn_context`；`model=gpt-6.1-sol`、`effort=xhigh`、`cwd=/Users/ywang2397/work/AI_reliability_knowledge_base`；嵌套模型与推理档位一致；本轮未另启模型或子代理 |
| 核验坐标 | `/Users/ywang2397/.codex/sessions/2026/10/21/rollout-2026-10-21T21-50-05-01a15eb9-d724-7312-990f-a6f07a1365db.jsonl` L8；时间戳 `2026-10-21T13:50:14.767Z` |
| 会话 ID / turn ID | `01a15eb9-d724-7312-990f-a6f07a1365db` / `01a15eb9-ec0f-74c1-8108-2dd38e782be6` |
| 执行方式 / 日期 | 当前本地 Codex CLI 会话直接复核；本地只读检查、上游网页及 GitHub 连接器取证；2026-10-21 / Asia/Shanghai |
| 判定依据链 | [初审](batch-30-t08-05-codex-review.md) C07 关闭条件 → [第一轮复核](batch-30-t08-05-codex-recheck.md) C07 剩余差距、N01 关闭条件 → [第二轮复核](batch-30-t08-05-codex-recheck-2.md) C07/N01 的最小剩余条件 |
| 正文快照 | [修订后正文](../../knowledge/08-reliability/test-design-and-coverage.md)，153 行；SHA-256 `a4cdd8c05e4c42abb737e1a9f0c1ad8f5edeeb000b6e385c4c46203aa482351e` |
| 来源记录快照 | [修订与来源记录](batch-30-t08-05-sources.md)，51 行；SHA-256 `8a79f9b25af152402a797b30614e230141711e2df3fab4e3593b70dfe3f30d71`；重点 L46–51，最新 DCGM 补录在 L50 |
| registry 快照 | [来源登记](../../sources/registry.yaml)，7227 行；SHA-256 `0e0defed4ec29acd3722f8f78dd4926b3e88441c7a48e59a4db96e0b976275b5` |
| 写入范围 | 仅新增本报告；正文、来源记录、registry、历史报告、计划、导航和构建产物均不由本会话修改 |

## 范围与定向取证

已读 `README.md`、`AGENTS.md`、[写作指南](../authoring-guide.md)、元数据 schema 和内容总目录。仅裁定 C07、N01，不重审已关闭项；作者的关闭自述不作为独立通过证据。以下本地行号均对应上表快照。

| 证据 | 本轮读取与边界 |
|---|---|
| E1 · DCGM | 2026-10-21 重新打开[登记的精确页](https://docs.nvidia.com/datacenter/dcgm/latest/user-guide/dcgm-diagnostics.html)，取得 DCGM Diagnostics 正文，定向核对 Run Levels and Tests 表。四级表及 stress/power/memtest 对应项存在，表头仍限定 Hopper 与 4/8 卡条件。本轮观察是当前可变页的独立重读，不追记为 2026-10-08 的历史核验，也不将其等同于 v3.3.9 固定源码版本 |
| E2 · MLPerf | 网页工具打开[固定 commit 规则文件](https://github.com/mlcommons/storage/blob/7e71ca162d8f9e7ae4b5b698d7d79b0883817f25/Submission_guidelines.md)返回 cache miss；改用 GitHub 连接器按同一 commit 取得原文件 L160–185，blob SHA 为 `bdd2397f5e57b708fc096744660676e27662ede4`。§2.2.2.1 正文按每客户端 `S<3M`，示例按 `3S` 与 `M` 比较的冲突仍在；仅核查修链保留原文件及既有冲突边界，不重开 C06 或执行清缓存 |
| E3 · 字符串与依赖 | 提取正文全部 15 处外链，按原始 URL 与 registry 各来源顶层 `url` 比较；不去 fragment、不作归一化，也不拿许可子链接或 notes 中的 URL 代替登记入口。另核对本文 `source_refs` 及来源记录 L49–51 |

registry 中 DCGM user-guide 条目（L1035–1045）仍保留 `latest page observed 2026-10-08`，URL 与稳定 ID 未改；固定源码条目 `src.nvidia.dcgm-v3.3.9`（L597–610）另立，支持补录所述的版本区分。其他批次条目变更不计作本篇取证成果。

## 逐项状态

| 编号 | 优先级 | 状态 | 对照关闭条件与剩余差距的判定 |
|---|---|---|---|
| C07 | P2 | **CLOSED** | 初审要求全部正文外链逐字匹配登记入口，MLPerf 指向固定文件并保留 C06 边界。第一轮剩余 MLPerf/DCGM fragment，第二轮仅余 L46 的 DCGM fragment。本轮 L46 已改为登记原串，Run Levels and Tests 节名保留在邻文；L54/L151 同样匹配。MLPerf L72/L147 继续使用原固定 commit，行号留在文字，L72/L141/L147 保留冲突待澄清。15/15 处、8/8 个唯一 URL 全部精确匹配，未靠改换登记入口消除差异 |
| N01 | P3 | **CLOSED** | 原条件要求复用 DCGM 稳定 ID，并在本任务来源记录/核对范围补齐精确页、章节、读取日期与 latest 边界，区分新读和历史复用。L17 的依赖与 L151 的精确页/章节继续保留；来源记录 L50 新补 2026-10-08 历史观察、2026-10-21 本轮日期、Run Levels and Tests、latest 可变及与固定源码不同版本的限制。记录明确作者为按登记入口引用、独立重读属于复核审阅方；前两份复核报告的 E4/E1 均记录同日实际重读，本轮 E1 再次核实。没有把审阅方取证冒充作者此前已读；关闭依据是补录与证据链，非 L51 的自判关闭 |

### C07 全篇入口核对

| 对应登记 ID | 正文位置 | 原字符串精确匹配 |
|---|---|---|
| `src.google.sre-testing-reliability` | L40、L58、L104、L145 | 4/4 |
| `src.nvidia.dcgm-diag-user-guide-latest-2026-10-08` | L46、L54、L151 | 3/3 |
| `src.paper.kalibera-jones-effectsize-2020` | L69、L146 | 2/2 |
| `src.mlcommons.storage-rules-v2.0` | L72、L147 | 2/2 |
| `src.nvidia.nccl-tests-b4d5beeb` | L148 | 1/1 |
| `src.huawei.hccl-perf-test-guide-cann-9.1.x` | L149 | 1/1 |
| `src.usenix.superbench-atc24` | L149 | 1/1 |
| `src.google.sre-effective-troubleshooting` | L150 | 1/1 |

8 个唯一 URL 少于上一轮的 9 个，是去掉残留 fragment 后同一 DCGM 页面合并计数；没有删除外链。对应 ID 均在本文依赖中，全部 9 个 `source_refs` 均已登记。本轮远程重读仅限 E1/E2；字符串匹配不表示对其他来源重新完成技术核验。

## 新发现

无本次修订引入的新问题，不设 N20 及后续编号。沿用既有关闭状态、附注和未决读取边界；不重编号历史问题，也不把 HCCL 等既有读取缺口补记为本轮已核实。

## 校验与写入边界

- 已运行 `PYTHONDONTWRITEBYTECODE=1 make check`，退出码 0：`PASS: 126 content entries; 575 sources.` 另核对正文 28 处本地相对链接，目标均存在；这些检查不证明技术正确性或真实环境适用。
- 按用户“仅新增这一个文件”的限定，未运行会重写 `build/` 的 `make build`；未改 `src/kb/`，未运行 `make test`。未执行诊断、基准、压力、注入、清缓存或恢复操作。
- 写入前对 664 个既有非忽略文件建立路径/内容摘要，聚合 SHA-256 为 `877c2df3b2a295b826244246b91a604abfe6ac80da209a1b3e11e0d86ecf5274`；交付前复核其内容不变。另观察到并发新增的 `docs/research/batch-30-t08-07-codex-recheck-3.md`，不计作本会话成果。工作区已有的作者修订与其他审阅报告均保留，本会话唯一仓库写入为本报告。
- 正文仍为 `draft / source_checked`，七份方案执行仍记 **0/7**；本轮只关闭来源入口与可追溯性发现，不产生硬件或实验验证证据。

**结论：本轮 2/2 CLOSED（C07、N01）；OPEN：无；新增发现：无。沿用此前 8 项已关闭判定，T08-05 已知发现累计 10/10 CLOSED，在既定问题清单范围内通过定向复核。既有附注与验证缺口继续保留，模型审阅不替代真实环境验证。**
