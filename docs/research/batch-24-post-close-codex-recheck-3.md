# Batch 24 遗留处理：第三次 Codex 定向复核

日期：2026-10-19（Asia/Shanghai）。基线：`0e8ff0f5348ce8197fc9fc692ede1aee9675dcc8`，加开始复核时工作区已有的九个文件的未提交修订。本文位置均指本轮工作区源文件；`HEAD` 位置另行标明。

## 1. 结论

**暂不通过。** B24-PC-07、B24-PC-08、B24-PC-10 为 **CLOSED**；B24-PC-09 为 **OPEN**。本轮新增 **2 项 OPEN P3**（B24-PC-R3-01、B24-PC-R3-02），没有新增 OPEN P1/P2。当前主题及 catalog 统计正确，四篇正文的可读性重排未发现技术含义损失；未通过的原因是批次计数字段仍未收尾、旧统计被新文字错误地称为“首次盘点”。按本轮“PC-07–10 全部 CLOSED”的通过条件，不能因这两项仅为 P3 而声明通过。

| 原问题 | 原优先级 | 本轮判定 | 依据 |
|---|---|---|---|
| B24-PC-07 | P3 | **CLOSED** | 来源审计两处、路线图一处均为“初审＋6 轮”；实际一份初审、六份定向复核，见第 3 节。 |
| B24-PC-08 | P2 | **CLOSED** | 05.2 的两个原缺口 closed、五项主题任务 done、主题验收 accepted，新增证据确有对应正文；63 主题独立对照未发现新的缺口状态矛盾，见第 4 节。 |
| B24-PC-09 | P3 | **OPEN** | 43/18/2、followup 20、未映射 0 及 catalog 统计均复算一致；但 `planned_followup_batches: 19` 无当前有效口径，“首次盘点 22/34/7”与原基线冲突，见第 5、7 节。 |
| B24-PC-10 | P3 | **CLOSED** | 四篇逐个 diff hunk 核对，适用范围、限制、来源与坐标保留；表下说明仍对应原行，超长单元格/段落均为 0，见第 6 节。 |

本次不撤销[第一次交付后复核](batch-24-post-close-codex-recheck.md)和[第二次交付后复核](batch-24-post-close-codex-recheck-2.md)已经关闭的技术事项；不重做未改动内容的正确性审阅，不把本报告或结构检查当作真实环境验证。

## 2. 角色、证据与执行边界

- 承担同一 Codex 技术审阅角色，未派发子代理，未启动另一模型调用。用户指定模型/档位为 `gpt-6.1-sol / xhigh`。
- 本轮实际读取的本地会话记录是 `~/.codex/sessions/2026/10/19/rollout-2026-10-19T11-03-28-01a1521d-35f2-7640-8079-385a0511ebf0.jsonl`：L1 的 `session_meta` 为本仓库 cwd、`originator=codex_exec`、`cli_version=0.157.1`、`model_provider=custom`；L6 的 `turn_context` 为 `model=gpt-6.1-sol`、`effort=xhigh`、`approval_policy=never`、workspace-write 且 `network_access=false`。这能核验**本地 CLI 记录的模型/档位一致**，不能独立认证自定义服务端实际执行的模型权重或推理档位；后者仍 unknown，不以用户指定值替代证明。
- 已读取 `README.md`、`docs/authoring-guide.md`、`content-outline.md`、本轮修订记录和相关计划/历史报告；未发现 `docs/`、`plans/`、`knowledge/` 下更深的 AGENTS.md。核对全部 `git diff HEAD`，没有把已有未提交修订归为本轮产出。
- 范围以[“遗留处理（2026-10-19，第二轮）”](batch-24-post-close-review.md) L39–48 为准。独立解析两个 YAML 的全部 63 个主题、141 个 gap assignment 和相应 task refs；独立解析盘点 Markdown 的 63 行及隔离构建的新 catalog，不使用原工作区旧 catalog 充当复算结果。
- 本轮没有新下载远端源码。仅为辨别重排中“两个测试均不验证数值”的限定范围，读取既有缓存原文件并重算摘要，方法与限制见第 6.3 节。其余判断为本地修订前后语义/引用对照，不声称重新核实全部上游技术结论。

## 3. B24-PC-07：CLOSED

`docs/research/batch-24-source-audit.md:10` 的任务表、`:36` 的总轮次和 `docs/full-coverage-roadmap.md:276` 的 Batch 24 段已分别改为 T06-01“初审＋6 轮”。实际文件清单如下，每份标题的轮次亦相符：

| 类型 | 文件 |
|---|---|
| 初审 | [batch-24-t06-01-codex-review.md](batch-24-t06-01-codex-review.md) |
| 第 1 轮 | [batch-24-t06-01-codex-recheck.md](batch-24-t06-01-codex-recheck.md) |
| 第 2 轮 | [batch-24-t06-01-codex-recheck-2.md](batch-24-t06-01-codex-recheck-2.md) |
| 第 3 轮 | [batch-24-t06-01-codex-recheck-3.md](batch-24-t06-01-codex-recheck-3.md) |
| 第 4 轮 | [batch-24-t06-01-codex-recheck-4.md](batch-24-t06-01-codex-recheck-4.md) |
| 第 5 轮 | [batch-24-t06-01-codex-recheck-5.md](batch-24-t06-01-codex-recheck-5.md) |
| 第 6 轮 | [batch-24-t06-01-codex-recheck-6.md](batch-24-t06-01-codex-recheck-6.md) |

第六轮报告 L5–9 对第五轮唯一开放项作关闭判定，同时保留当时对模型身份的 unknown 表述。本次只核对文件与轮次数，不改写历史身份记录，也不把两轮交付后复查或本轮算进上述六轮。四任务原链合计为 4 份初审＋18 份复核＝22 份，与来源审计口径相符。

## 4. B24-PC-08：CLOSED

### 4.1 05.2 的覆盖升级有实际依据

`plans/full-coverage-backlog.yaml:1889` 的 05.2：

- L1913 起两项缺口中，05.2-G1“Slurm 正文与来源”由 T05-03 承担，05.2-G2“双平台完整作业生命周期等”由 T05-02/T05-03 承担，均为 `closure_lane: content / status: closed`。
- L1907 起主题任务为 T05-02、T05-03、T05-05、T05-08、T05-10；五项均 `done`，目标文件及稳定 ID 均能在隔离 catalog 中找到。
- L1937–1938 为 `content_acceptance_batch: 24 / content_acceptance_status: accepted`。任务完成、原缺口关闭和主题验收三层证据齐全，不是仅按新增篇数推断 covered。

`plans/topic-coverage.yaml:635` 已为 `covered / maintain`、`gaps: []`，八项 evidence refs 全部存在；`docs/topic-coverage-audit.md:103` 的同主题行为“已覆盖（基础）”。新增四项 evidence refs 的实质内容如下：

| 新增证据 | 正文位置与实际覆盖 |
|---|---|
| `cluster-platform.kubernetes-job-lifecycle` | `knowledge/05-cluster-platform/kubernetes-job-lifecycle.md:44` 的 Job 控制器、完成/失败计数与重试；`:64` 的 TTL/finalizer/属主清理；`:90` 的多视图状态表；`:105` 的事件分支；`:122` 的终止/重试/取消核对及测试入口。不是只有 K8s 名称或导航。 |
| `cluster-platform.slurm-jobs-and-device-resources` | `knowledge/05-cluster-platform/slurm-jobs-and-device-resources.md:38` 的 daemon 与 Job/Step 责任，`:49` 的状态/标志、`:93` 的取消/重排/清理、`:126` 的设备资源和`:141`、`:153` 的测试/观察入口。明确 Slurm Job 不等于 K8s Job，NPU 支持仍 unknown（`:151`）。 |
| `cluster-platform.node-drain-resource-reclamation` | `knowledge/05-cluster-platform/node-drain-resource-reclamation.md:86`、`:111` 的 K8s/Slurm 两路回收，`:178` 的三层准入门槛、`:190` 的身份账本、`:210` 的完成判据，补足退出后实际资源/执行状态核验。 |
| `cluster-platform.control-plane-recovery` | `knowledge/05-cluster-platform/control-plane-recovery.md:147` 的跨恢复作业/分配/记账核验，`:182` 的新旧任务验收矩阵，`:192` 的停止与完成判据；保留 etcd 灾备、主备切换专项测试未定位及演练未执行的边界。 |

这些证据支持的是本主题限定的基础内容和方法层覆盖，不建立任意平台组合兼容性，不把方法设计、来源测试或模型审阅升级为本地 reproduced。

### 4.2 全部 63 主题的独立一致性检查

不是只查 05.2。以 topic_id 连接两个 YAML 与盘点 Markdown，核对覆盖状态、未关闭缺口的含义、已关闭缺口所依赖任务、主题验收与已交付目标 ID：

- 三处主题集合一致，各有 63 个不同 ID；Markdown 逐行状态与 YAML **63/63 相符**。
- backlog 的 141 项缺口为 **87 closed / 54 open**；所有 closed 缺口对应任务均 done，没有已完成任务目标缺失于 catalog 的情况。
- 43 个 covered 中，32 个最终内容验收 accepted，11 个最终验收仍 planned。两者不是同一字段，不能机械要求所有 covered 都 accepted：其中 10 个本来就是 `baseline_coverage_status: covered`；另一个 06.3 的三个原内容缺口已由 T06-02 关闭，剩余 T06-09 是 Batch 31 导航/终态映射任务，不能把其 planned 当作已 accepted。
- covered 与仍 open 的原缺口相遇，只有 **01.6-G3**。`plans/full-coverage-backlog.yaml:624` 明确其为 `closure_lane: both`、V08 真实验收环境档案仍 open，主题的 acceptance note 与额外 closure criteria 明确保留该例外；`plans/topic-coverage.yaml:259` 保持基础内容 covered，不表示 V08 已执行。不是本轮新关闭的真实证据缺口。
- 03.5 保留 BLOCKED-1 对应的唯一 open 缺口；06.2 保留性能验证缺口；06.4 保留 RL 与其一致性/吞吐缺口。清单对这些 gap_text 增补限定或换用具名阻塞项，与 backlog 原缺口语义相同，不能按字符串不完全相等误报状态冲突。分别见两份 YAML 的 03.5、06.2、06.4 条目。

因此，修订者“除 01.6-G3 外无其他不一致”的说法，**在主题覆盖与开放内容缺口的对应口径下成立**；不应解释成“63 主题最终 v1 验收全部完成”，也不覆盖第 7 节发现的批次/历史统计表述问题。

下表是逐主题核对结果。“任务 done/总数”按该主题 task_refs 计，同一任务可服务多个主题，不可跨行相加当作唯一任务总数。

| 主题 | 清单 | backlog 验收 | 缺口 closed/open | 主题任务 done/总数 |
|---|---|---|---:|---:|
| 00.1 | covered | accepted | 2/0 | 1/1 |
| 00.2 | covered | planned | 0/0 | 0/1 |
| 00.3 | covered | planned | 0/0 | 0/1 |
| 00.4 | missing | planned | 0/2 | 0/2 |
| 00.5 | partial | planned | 0/3 | 0/1 |
| 00.6 | partial | planned | 0/2 | 0/4 |
| 01.1 | covered | accepted | 3/0 | 3/3 |
| 01.2 | covered | accepted | 2/0 | 1/1 |
| 01.3 | covered | accepted | 3/0 | 2/2 |
| 01.4 | covered | accepted | 2/0 | 1/1 |
| 01.5 | covered | accepted | 3/0 | 3/3 |
| 01.6 | covered | accepted | 2/1 | 2/2 |
| 02.1 | covered | accepted | 2/0 | 1/1 |
| 02.2 | covered | accepted | 3/0 | 2/2 |
| 02.3 | covered | accepted | 3/0 | 3/3 |
| 02.4 | covered | accepted | 3/0 | 3/3 |
| 02.5 | covered | accepted | 2/0 | 1/1 |
| 02.6 | covered | accepted | 3/0 | 3/3 |
| 02.7 | partial | planned | 0/3 | 2/3 |
| 03.1 | covered | accepted | 2/0 | 2/2 |
| 03.2 | covered | accepted | 2/0 | 2/2 |
| 03.3 | covered | accepted | 3/0 | 4/4 |
| 03.4 | covered | accepted | 3/0 | 1/1 |
| 03.5 | partial | planned | 2/1 | 3/3 |
| 03.6 | covered | accepted | 0/0 | 3/3 |
| 03.7 | covered | accepted | 3/0 | 4/4 |
| 04.1 | covered | accepted | 3/0 | 2/2 |
| 04.2 | covered | accepted | 2/0 | 4/4 |
| 04.3 | covered | accepted | 3/0 | 5/5 |
| 04.4 | covered | accepted | 3/0 | 5/5 |
| 04.5 | covered | accepted | 3/0 | 4/4 |
| 04.6 | covered | accepted | 3/0 | 5/5 |
| 05.1 | covered | accepted | 3/0 | 3/3 |
| 05.2 | covered | accepted | 2/0 | 5/5 |
| 05.3 | covered | accepted | 0/0 | 5/5 |
| 05.4 | covered | accepted | 3/0 | 3/3 |
| 05.5 | covered | accepted | 3/0 | 4/4 |
| 05.6 | covered | accepted | 3/0 | 4/4 |
| 05.7 | covered | accepted | 2/0 | 6/6 |
| 06.1 | covered | planned | 0/0 | 1/3 |
| 06.2 | partial | planned | 2/1 | 1/3 |
| 06.3 | covered | planned | 3/0 | 1/2 |
| 06.4 | partial | planned | 1/2 | 1/3 |
| 06.5 | partial | planned | 0/3 | 0/2 |
| 06.6 | partial | planned | 0/3 | 0/3 |
| 06.7 | covered | planned | 0/0 | 0/2 |
| 06.8 | covered | planned | 0/0 | 0/2 |
| 07.1 | partial | planned | 0/3 | 0/3 |
| 07.2 | partial | planned | 0/3 | 0/3 |
| 07.3 | covered | planned | 0/0 | 0/3 |
| 07.4 | partial | planned | 0/3 | 0/3 |
| 07.5 | partial | planned | 0/3 | 0/4 |
| 07.6 | missing | planned | 0/3 | 0/4 |
| 07.7 | covered | planned | 0/0 | 0/3 |
| 07.8 | partial | planned | 0/3 | 0/4 |
| 08.1 | covered | planned | 0/0 | 0/4 |
| 08.2 | partial | planned | 0/3 | 0/3 |
| 08.3 | covered | planned | 0/0 | 0/4 |
| 08.4 | covered | planned | 0/0 | 0/4 |
| 08.5 | partial | planned | 0/3 | 0/4 |
| 08.6 | partial | planned | 0/3 | 0/3 |
| 08.7 | partial | planned | 0/3 | 0/2 |
| 08.8 | partial | planned | 0/3 | 0/4 |

## 5. B24-PC-09：OPEN，当前计数正确但记录未完全闭环

### 5.1 当前主题及 catalog 计数

复算输入：当前 `plans/topic-coverage.yaml`，以及在隔离副本重新 `make build` 得到的 `build/catalog.json`。先按唯一内容 ID 分类，再取全部 topics.evidence_refs 的并集计算正文映射；background_refs 不充当正向覆盖。来源数另与当前 registry 的 sources 列表独立对照。

| 项目 | 独立结果 | 对照结果 |
|---|---:|---|
| 主题总数 | 63 | YAML summary 相符 |
| covered / partial / missing | 43 / 18 / 2 | YAML summary 与盘点 L9 相符 |
| followup_topics | 20＝18＋2 | YAML summary 相符；不是剩余批次数 |
| 未映射实质正文 | 0 | 90 个实质内容 ID 均出现于 evidence_refs，并且所有 evidence refs 均存在于 catalog |
| catalog / 实质正文 / 导航 | 103 / 90 / 13 | 盘点 L11 相符 |
| 来源 | catalog 493 / registry 493 | 盘点 L11 相符 |
| 实质正文类型 | concept 28、reference 22、procedure 26、case 7、experiment 7 | 合计 90，盘点 L11 相符 |
| 导航类型 | index 9、path 4 | 合计 13 |
| 实质正文 verification | source_checked 75、not_verified 15、reproduced 0 | 盘点 L13 相符 |
| not_verified 的类型 | experiment 7、procedure 8 | 盘点 L13 相符 |
| 全 catalog verification | 上述 90 项＋not_recorded 13 | 13 个导航条目未记录 verification，不能计为 not_verified 或实测 |
| 编辑状态 | draft 103 | “所有内容仍 draft”相符 |

逐领域结果与 `docs/topic-coverage-audit.md:15` 的领域小计表全部相符：

| 领域 | 主题数 | covered | partial | missing |
|---|---:|---:|---:|---:|
| 00 | 6 | 3 | 2 | 1 |
| 01 | 6 | 6 | 0 | 0 |
| 02 | 7 | 6 | 1 | 0 |
| 03 | 7 | 6 | 1 | 0 |
| 04 | 6 | 6 | 0 | 0 |
| 05 | 7 | 7 | 0 | 0 |
| 06 | 8 | 4 | 4 | 0 |
| 07 | 8 | 2 | 5 | 1 |
| 08 | 8 | 3 | 5 | 0 |
| 合计 | 63 | 43 | 18 | 2 |

### 5.2 batch_planning 与历史快照

`plans/topic-coverage.yaml:51` 的 completed_batches 01–24、next_batch 25、planned_last_batch 32、planned_total_batches 32 与当前执行清单及交付记录一致。backlog 的 Batch 13–24 共 12 批均 done，25–32 共 8 批 planned；本轮没有重新认证前 12 批技术验收。`final_batch_count: null / planning_status: in_progress / execution_started: true` 没有宣称全部完工，保留成立。

但同组的 `planned_followup_batches: 19` 未更新或界定口径：若指当前后续待执行数应为 8，若指本轮完整覆盖规划的后续批次总数应为 20。19 不能由当前批次集合推出；不在 notes 指定保留的三组历史快照内。此项为 **B24-PC-R3-01**。

对 `input_snapshot`、`validation`、`documents`，分别解析后与 HEAD、首次入库提交 `b89abb9` 对照，**三组均完全相同**。它们仍保留 73 catalog / 60 实质正文 / 13 导航、119 来源、旧正文类型和 53/7 verification 及 73 个 documents 摘要；validation.checked_at 仍为 2026-10-08。将它们与当前 103/493 分开并明确“未重新生成”，如实揭示其历史性，可以保留；不能将其中旧 sha256 或旧 passed 标记当作当前文件身份/本轮校验。

本轮只能确认“与既存历史快照一致，内部登记日期为 2026-10-08”；首个入库提交实际日期为 2026-10-09，不能仅凭 created_at/checked_at 独立证明每个摘要的采集时刻。**该三组快照的保留策略不是本轮阻塞点。** 问题是新增 `summary.notes` 与盘点 L9 又把旧 summary 的 22/34/7 称为“2026-10-08 首次盘点”，而不是区分初始基线与后续滚动更新，详见 **B24-PC-R3-02**。

## 6. B24-PC-10：CLOSED

### 6.1 自动对照与度量口径

逐篇比较 `git diff HEAD`，并独立抽取“链接目标”“L 开头的原文件行号/范围”“行内代码”“围栏代码块正文”“frontmatter.source_refs”的**多重集合**，不是只比较去重集合。四篇五类结果均无删除、无新增；代码块未改，引用 revision 和坐标未丢。除三篇 updated_at 从 2026-10-18 改到 2026-10-19 外，frontmatter 完全不变；parallelism-and-state 的 frontmatter 未变。draft、verification 与 applicability 没有因重排升级。

| 文件简称 | 链接目标出现次数 | L 坐标出现次数 | 行内代码次数 | 围栏代码块数 | source_refs 数 |
|---|---:|---:|---:|---:|---:|
| control-plane-recovery | 54 | 43 | 80 | 0 | 22 |
| parallelism-and-state | 55 | 60 | 185 | 0 | 11 |
| framework-execution | 32 | 53 | 46 | 1 | 17 |
| pretraining-and-finetuning | 40 | 19 | 57 | 0 | 13 |

这些计数只是辅助，不能自行证明限定词作用范围不变；下节另作人工对应核对。

长度度量使用 Unicode 字符数，包含行内 Markdown 标记、URL 和代码，不按字节数或显示宽度计；表格以未转义 `|` 分栏，去除外围空白、排除分隔行。段落排除 YAML、标题、表格和围栏代码；同一段的续行合并，每个列表项单独计段，缩进子列表另计，不把整张表或整个列表误算成一个段落。严格采用“大于 300 / 大于 600”，不是大于等于。

| 文件简称 | HEAD 超 300 单元格 | 当前超 300 单元格 | HEAD 超 600 段落 | 当前超 600 段落 | 当前最大单元格 | 当前最大段落 | 当前最长物理行 |
|---|---:|---:|---:|---:|---|---|---|
| control-plane-recovery | 8 | 0 | 1 | 0 | 297（L154） | 357（L165） | 471（L171） |
| parallelism-and-state | 5 | 0 | 5 | 0 | 290（L119） | 590（L187） | 590（L187） |
| framework-execution | 4 | 0 | 3 | 0 | 285（L135） | 585（L127） | 587（L127） |
| pretraining-and-finetuning | 1 | 0 | 5 | 0 | 218（L100） | 564（L157） | 566（L157） |
| 合计 | 18 | **0** | 14 | **0** | — | — | 471–590 |

原 etcd 单元格 1,066 字符，原 NVIDIA 列表项正文 1,520 字符、含列表标记的物理行 1,522 字符；与修订记录“约 1,522”不冲突。未复用修订者的脚本，独立重算仍得到 18/14→0/0。列表拆分确实改变文本块粒度，这是本项可读性整理的预期效果，不是把未改的超长段落藏到代码块。

### 6.2 control-plane-recovery：保留风险、门槛与行对应

- `knowledge/05-cluster-platform/control-plane-recovery.md:97` 的“etcd 恢复要点”紧随故障层表，etcd 行明确指向它。恢复顺序、同快照/新逻辑集群/隔离旧集群、输入文件与输出目录三分法均保留；`--skip-hash-check` **只适用于第二类工件**，不是损坏快照通用补救；选项 patch 支持 unknown 与“不构成操作建议”未删。
- `:108` 的控制器/节点补充与原两行有具名对应，保留内部队列语义 unknown、宽限整数倍和失联 Pod 可能继续执行；`:123` 的 Slurm 表补充分别对应 slurmctld 等待时长和 slurmdbd/调度与记账分离。没有把一行的平台条件推广到另一行。
- `:134` 的回放风险改成嵌套列表，四层核验仍处于编号 3 下；缺全局证据不补值、对象 RV 不能推算 revision、逐消费者自身证据、任一缺证即停止/未完成/不得放行均保留。不是把风险说明变成已确认收敛结果。
- `:160` 明称“核验表补充（Kubernetes 列）”，执行身份对“重复/过期分配”行，重试限额/condition/门控对“未完成/已完成作业”行；v1.32 两门默认开及未知门取值时的 unknown 限定仍作用于终态时序，未变成看到 conditions 就能放行。
- `:176` 的 K8s 作业行单测说明明确与上表集成测试对应，保留“均经登记核对，已读未运行”；etcd 灾备与主备切换专项测试负结果、未执行演练边界未消失。未新增本地故障或恢复成功记录。

### 6.3 framework-execution：保留 only/不验证与独立版本线

- `knowledge/06-training/framework-execution.md:67` 把 autograd、retain_graph、optimizer 拆列。原“**只有**同图再次求导且依赖中间量，才在会释放它们的先前 backward 中保留”的条件完整；没有变成每一步 retain_graph，或后补设置能恢复旧图。
- `:103` 的 Megatron CLI 依据具名对应 NVIDIA 档案行，仍是 dataclass/工厂生成旗标、CLI 未运行；三组档案不能拼成同一环境的段落保留。`:107` 的 AMD 列表仍把 2.6 文档原文、独立 ROCm 7.1.1 版本线和“不声明迁移”分开，没有因标题的“均”吞掉“另注”的独立版本限定。
- `:143` 的测试说明明确对应上表三行。onlyCUDA 仍**只限定 CUDA 参数用例**；optimizer 等价性没有扩成完整 checkpoint/RNG 恢复；调度测试的 CUDA/NCCL 多进程前提、只验证选择且不验证数值/通信/完整 step 都保留。
- `:146` 把 compile 两个测试概括成“两者不验证完整训练 step、编译数值或 optimizer/scheduler 路径”。为防止把原第二个括号的限制错误扩大，额外读了既有 `/private/tmp/b24-t062-s4.GPvX0z/pytorch-test-compile.py`：SHA-256 为 `36745171714b59a3ac313ac9b8a80e5423fd95f7abb538933e6731cdbd074d3d`，与 `sources/registry.yaml:6127` 及第四轮报告登记一致。原文件 L24–32 的第一个测试只有单次 model 调用和 frame_count＝1 断言，L149–173 的第二个是签名一致性。此处“两者”是对所列断言边界的真实澄清，未新增数值验证能力或删去有效测试覆盖。本轮未新从远端取得该文件，也未运行 PyTorch 测试。

### 6.4 parallelism-and-state：保留合成前提及两套 scaler

- `knowledge/06-training/parallelism-and-state.md:80` 明指 CP 行的 Megatron 来源；`:106` 明指参数身份示例，保留合成 MHA、query-group 交错存储和不能换算成顺次 Q/K/V 布局。专家编号覆盖检查移到表后 `:123`，仍是同一 EP 组、每专家 ETP 两片与稠密/专家两套布局的比较，没有重写 rank、组员、offset 或计算公式。
- `:147` 起列表仍由“全部为合成假设、本库无测量”统领，节点放置、重算 stride、占满 64 rank 和每候选完整分解均保留；没有把某样例 stride 搬给全部候选。
- `:224` 起四类计数分叉仍明确：成功才推进 scheduler，失败不推进，两路都推进 consumed samples；“合法不序列化暂态”与“合法不更新”未合并。
- `:238` 的三情形表仍区分 PyTorch 与 Megatron，Megatron 列限定 fp16 且未设显式 loss scale；`:246` 的状态机紧随该表，成功有限步与 overflow 的更新规则、非连续 overflow、min-scale 下界均保留；`:253` 的 bf16 无 scaler/ConstantGradScaler 例外没有被挪走或消失。
- `:255`、`:257`、`:261` 的“仍须 update”“累积中途不得更新”“只有完整 step 边界才允许不保存暂态”作用范围未改变。合成反例 `:284`–`:286` 仍先列全部前置条件，再说只违反 ulysses 头数约束及绕过后行为 unknown；没有把条件失败写成已运行的事故。

### 6.5 pretraining-and-finetuning：保留阶段、平台和加载分支

- `knowledge/06-training/pretraining-and-finetuning.md:77` 明指数据混合行来源；三种权重/size 条件、预生成索引、超 epoch 的重复消费、样本比例不等于有效 token 比例仍完整。三类操作的游标/RNG 决策拆列后仍分别是推理不适用、同阶段 resume 恢复、新阶段重置，没有相互串用。
- `:130` 起 MindSpeed 两种微调脚本、预训练脚本与 HF Trainer 为分列对照，仍各有独立来源，未把 HF 条件归给 MindSpeed。
- `:164` 起 NVIDIA 父列表仍包住两个固定档案，最小合成循环不证明性能/恢复；模型级 SFT 仍仅多模态 NVLM。FINETUNE_DIR 与 CHECKPOINT_DIR、输出目录有/无 checkpoint 的两路首次微调/resume、纯文本 SFT 未逐目录定位、脚本存在不等于可运行的限定全部保留。
- Ascend 与 AMD 各自父列表的范围不变。AMD 的“均为官方页面原文口径”后仍分别写两条独立版本线，不把 PyTorch 2.6 限制外推永久规则；具体机型/驱动/外部扩展/固定 HF 组合的可执行性 unknown 和本库未执行 AMD 验证完整保留。

**综合判断：四篇均未发现重排引入的技术含义、适用范围或否定/全称限定漂移；未丢失或新增实质技术主张、来源、行号坐标，也未由本轮改动暴露出须另列的原有技术错误。** 新增摘要、具名标签和过渡文字属于导航/拆分，不能以链接/code 计数相同替代上述逐段判断。

## 7. 新问题与关闭条件

### B24-PC-R3-01 — P3 — OPEN：batch_planning 遗留 19，口径未界定

- **位置**：`plans/topic-coverage.yaml:55`；相关处理声明 `docs/research/batch-24-post-close-review.md:47`。
- **证据**：同组 next_batch＝25、last＝32，当前剩余 planned 批次为 25–32 共 **8**；`plans/full-coverage-backlog.yaml` 的 batches 实际有 13–32 共 **20** 个，`docs/full-coverage-roadmap.md:51` 及 `docs/topic-coverage-audit.md:185` 亦为完整规划 20 批。19 既非当前剩余数，也非完整后续规划总数。字段在本次 diff 未修订，属于 PC-09 要求核对的旧值遗留；新的快照保留说明没有包含 batch_planning，无法把它自动视作已标注历史值。
- **影响**：机器读取批次摘要会得到与执行清单不一致的后续数量；不影响已经复算正确的 43/18/2、103/493 或正文技术边界。
- **关闭条件**：明确该字段的含义并按其含义重算，若表示剩余批次改为 8，若表示完整规划规模改为 20；若坚持保留历史 19，则把它放在有可核对日期/范围的历史快照中并另给当前值。同步处理记录，定向复核字段、说明与 batches 一致后关闭。不能只把“已更新 batch_planning”写进报告而留下无口径旧值。

### B24-PC-R3-02 — P3 — OPEN：把滚动旧统计写成“2026-10-08 首次盘点”

- **位置**：`plans/topic-coverage.yaml:50` 新增 summary.notes；`docs/topic-coverage-audit.md:9` 新增括号历史比较。
- **证据**：两处新文字都把 22 covered / 34 partial / 7 missing、followup 41 称为 2026-10-08“首次盘点”。但 `plans/full-coverage-backlog.yaml:48` 的原基线明确为 **12/44/7**，独立按全部 topics.baseline_coverage_status 重算仍是 12/44/7；`README.md:13` 和盘点文档自身 `:185` 保留相同原基线。盘点 `:3` 的滚动历史则记载 Batch 13、14、15、16 分别升级 2、3、3、2 个主题，12＋2＋3＋3＋2＝22，且 Batch 14–16 登记为 **2026-10-09**。22/34/7 是此次重算前保留下来的旧 summary，不能据其创建日期改称 10 月 8 日首次结果。
- **影响**：当前计数并未算错，但新旧对比抹掉初始 51 个待补主题与后续滚动更新的区别；也使“历史快照如实保留”的说明混入新的错误时间归因。这不是要求重写旧 input_snapshot/validation/documents。
- **关闭条件**：区分首次基线 **12/44/7、followup 51** 和旧滚动统计 **22/34/7、followup 41**。可将后者称为“本轮重算前保留的 summary（含 Batch 13–16 更新）”，不要附没有证据的“首次/2026-10-08”归因；同步 YAML notes、Markdown 括号及处理记录，定向核验历史语义后关闭。

两项均是 PC-09 的未完成子项，不重复记成新增 P2；也不因此重新打开 PC-08 的主题覆盖修正或 PC-10 的正文重排。

## 8. 隔离检查、可重复性与文件保护

隔离目录：`/private/tmp/b24-recheck3.dwYLN6/repo`。复制当前工作区（含既有未提交修订），排除 `.git`、`.venv`、`.agents`、`.codex`、Python 缓存和 `.DS_Store`；把现有 `build/catalog.json`、`build/catalog.md` 一并作为副本的起始链接目标。随后只在副本运行 build，catalog 统计使用的是副本**重新生成**的结果，不是起始文件。

使用原工作区 `/Users/ywang2397/work/AI_reliability_knowledge_base/.venv/bin/python`，实测为 **Python 3.11.15**；没有安装或升级依赖。副本不存在 `.venv`，Makefile 的输出确认使用所给绝对解释器。实际命令（cwd 为上述隔离 repo）：

```bash
make check PYTHON=/Users/ywang2397/work/AI_reliability_knowledge_base/.venv/bin/python
make build PYTHON=/Users/ywang2397/work/AI_reliability_knowledge_base/.venv/bin/python
```

| 执行阶段 | make check | make build | 输出 |
|---|---|---|---|
| 报告写入前 | PASS，exit 0 | PASS，exit 0 | 103 content entries / 493 sources；副本 build/catalog.json、build/catalog.md 生成成功 |
| 含本报告 | PASS，exit 0 | PASS，exit 0 | 同为 103 content entries / 493 sources；副本 catalog 摘要与首轮构建一致 |

一次额外的会话元数据读取曾因在隔离 cwd 使用相对 `.venv/bin/python` 而报“文件不存在”；随后在原仓库读取成功。这不是 make 失败：两条 make 从首次执行即明确使用原工作区绝对解释器，均退出 0。

复算程序与结果保留在仓库外：`/private/tmp/b24-recheck3.dwYLN6/audit.py`、`audit-results.json`、`audit-output.txt`；工作区初始文件摘要为 `workspace-before.json`，make 日志为该目录下 `make-check-before-report.log`、`make-build-before-report.log` 及含报告阶段的相应日志。这些临时材料未加入仓库。

| 复算输入 | SHA-256 |
|---|---|
| 当前 plans/topic-coverage.yaml | `68190af537a482ec39f842ed9ed865ad9b945efa3ec057f232c741b626c06f25` |
| 当前 plans/full-coverage-backlog.yaml | `5a98b4224b1947e735ef4ca28697d5082e89840ec80ffe833508db4159b64b37` |
| 当前 docs/topic-coverage-audit.md | `f916d791ac004e2660f3d4c66f365f1955418863c899937574e2a745af65dc2a` |
| 隔离重新生成 build/catalog.json | `05f565352b1f06ffabaa0af128601dbfe52a131b9cb4e06bbbda814fc386f9ca` |

报告落盘后的工作区保护核验：逐项比较既有文件 SHA-256，**变更 0、删除 0，唯一新增为本报告**；原工作区 build/catalog.json、build/catalog.md 亦包含在摘要对照内且未变，HEAD 仍为上述 0e8ff0f。完整结果保留在隔离目录的 workspace-protection.json。没有创建分支或提交，也没有改写九个既有未提交修订文件。

本次未改 src/kb/，未运行 make test，未执行任何 GPU/NPU、训练、进程组、集群、灾备或 checkpoint 操作。make 的 PASS 仅验证结构和本地文件链接，不验证远程链接、技术正确性或现场效果；本报告的暂不通过亦不表示既有硬件验证失败。
