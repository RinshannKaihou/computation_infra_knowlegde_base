# Batch 32 · T00-07 定向复核报告

## 会话元数据与结论

| 项目 | 核验记录 |
|---|---|
| 角色 / 范围 | 独立批次审阅者；按[初审报告](batch-32-t00-07-codex-review.md) C01–C04 的关闭条件定向复核，并核对本轮增量语义；不承担正文编写 |
| 指定 / 实际模型与档位 | 指定 `gpt-6.1-sol / xhigh`；当前 rollout 最新 `turn_context` 为 `model=gpt-6.1-sol`、`effort=xhigh`，一致，核验通过 |
| rollout 文件 | `/Users/ywang2397/.codex/sessions/2026/10/22/rollout-2026-10-22T10-20-41-01a16169-1c87-74a0-a9b1-224a4053432d.jsonl` |
| 会话归属互核 | 环境 `CODEX_SESSION_ID`、`CODEX_THREAD_ID` 与 rollout L1 的 `session_meta.id`、`session_meta.session_id` 均为 `01a16169-1c87-74a0-a9b1-224a4053432d` |
| 最新 turn_context | 共 1 条，在 rollout L8；时间 `2026-10-22T02:20:44.964Z`；`turn_id=01a16169-1d1d-7583-b863-80568bdc82de`；`cwd=/Users/ywang2397/work/AI_reliability_knowledge_base`，与工作目录及 L1 一致 |
| 交叉字段 | L8 `collaboration_mode.mode=default`，`settings.model=gpt-6.1-sol`、`settings.reasoning_effort=xhigh`、`developer_instructions=null`；开始审阅前与写报告前重新读取，核验结果一致，未以默认配置或历史报告代替实际记录 |
| 执行方式 | 当前本地 Codex CLI 会话直接审阅；L1 `originator=codex_exec`、`cli_version=0.163.0`、`model_provider=custom`；未另启模型或子代理 |
| 日期 / 时区 | 2026-10-22 / Asia/Shanghai（UTC+08:00） |
| 唯一写入 | 新增本报告 `docs/research/batch-32-t00-07-codex-recheck.md`；正文、导航、来源记录、计划、历史报告和 build 均不由本会话修改 |
| 判定汇总 | **C01–C04 全部 CLOSED：3 项 P2、1 项 P3；OPEN 0 项。增量核对未发现新的待修订项。该项任务在本审阅范围内通过。** |

开始审阅修订内容前已实际执行下列命令；写报告前再次执行，四份文件的行数与 SHA-256 均一致。行数按换行符计，指纹按原始字节计算；后文 P/M/F/R 坐标均对应此快照。

```bash
wc -l paths/tasks/performance-optimization.md paths/tasks/migration-and-upgrade.md paths/tasks/fault-recovery.md paths/roles/reading-by-role.md
shasum -a 256 paths/tasks/performance-optimization.md paths/tasks/migration-and-upgrade.md paths/tasks/fault-recovery.md paths/roles/reading-by-role.md
```

| 修订后文件 | 行数 | SHA-256 |
|---|---:|---|
| [性能优化任务路径](../../paths/tasks/performance-optimization.md)（P） | 82 | `44199951d9465892ebaeb5aaa62559ce11a459a6030f142fe492483e7fd2de6f` |
| [迁移与升级任务路径](../../paths/tasks/migration-and-upgrade.md)（M） | 94 | `fc3f9bb14c0380207c58350c8923d4fddaa3447234a4edbca356c3158da47c03` |
| [故障恢复任务路径](../../paths/tasks/fault-recovery.md)（F） | 77 | `e9b2668c8ffd09bb85178d09bc2e888152026fd27499f05658805733f754727f` |
| [角色页](../../paths/roles/reading-by-role.md)（R，仅审 T00-07 接入行） | 113 | `3dc6a7165bfa721c72f1382e0b9288450343b909601c124f881eb480d0b8356f` |

另记录两份审计输入的指纹：[初审报告](batch-32-t00-07-codex-review.md)为 247 行、SHA-256 `b118bf115fc09ec3fc08d1d034eefaec52442da5268a5eb8edc57af4f8fdd228`；[编写者修订记录](batch-32-t00-07-sources.md)（S）为 33 行、SHA-256 `6cfd57a3291f395fc3fe150efe22afd86906418344eb954140ee44d8247f12dc`，复核轮记录位于 L28–33。

## 复核依据与增量范围

已读取 README、AGENTS、写作指南、内容边界及 metadata schema。逐项重读初审 L116–146 的发现和关闭条件、修订后三页的相关段落及所链正文实际内容，并对照 S L30–33。用 `git diff` 界定改动：P L72；M L47–48、L84；F L37、L54、L67；R L89 的 P/M 接入部分。三份任务页的 HEAD 字节指纹与初审快照一致，因此该差异可用于定位初审后的正文修订。

角色页同时含其他任务的修改，本轮只判断 R L89 指向 P/M/F 的运行阶段入口，不重审其余修改。正文依据限于与本轮修订相关的性能验证、处置六项、升级门禁和兼容性方法；未重审整个 T00-07 或全部上游资料，也未重新抓取页尾外部入口。

## 逐项判定

| 发现 | 初审优先级 | 判定 | 关闭条件核对结果 |
|---|---|---|---|
| C01 · 三页停止/升级矩阵不完整 | P2 | **CLOSED** | 九个单元格均可直接定位触发与动作；P 区分配置回退和实验状态恢复，M/F 补权限不足分支；S L30 同步 |
| C02 · F 错误转写“动手前固定六项” | P2 | **CLOSED** | F L37 六字段与原表逐项一致，区分动作影响域与故障影响范围；L54 产出同步，补充材料另列；S L31 同步 |
| C03 · M 错误概括三类准入门禁 | P2 | **CLOSED** | M L47/L84 对应完整依赖交集、有效 baseline、恢复路径；缺可复跑 B0 的升级被拦截，首次安装例外未泛化；S L32 同步 |
| C04 · 角色页缺 P/M 直接入口 | P3 | **CLOSED** | R L89 到 P/M 各 1 条直接链接可解析，F 入口保留，位于语义合适的运维运行阶段；S L33 同步 |

### C01 · CLOSED

初审关闭条件要求逐页可定位“证据不足／无回退／权限不足”的九格触发和动作，并核对 P 的“不宣布优化通过”、M/F 的权限不足分支及 S 的记录。

| 页面 / 单元格 | 修订后实际行号与关键原文 | 判定 |
|---|---|---|
| P · 证据不足 | L72：“无基线且无法建立……→ 先补基线，不开始调参”；“证据不足以区分受害方与最早瓶颈……不宣布结论” | CLOSED |
| P · 无回退 | L72：“优化改动无可回退配置或实验起点不可恢复……→ 只保留只读分析与探索性结论，**不得宣布优化通过**” | CLOSED |
| P · 权限不足 | L45：“权限不足时先登记缺口”；L72：“profiling/采集权限不足 → 登记缺口并升级，不用推测代替证据” | CLOSED |
| M · 证据不足 | L84：“依赖交集补不到依据即停止”；“目标组合配套证据不足且无法降级 → 登记 unknown 并停” | CLOSED |
| M · 无回退 | L84：“回退路径未落定不执行变更”；L40 仍要求回退路径、保全安排与不可逆操作清单 | CLOSED |
| M · 权限不足 | L84：“变更/取证操作权限不足……→ 停止相应变更、保全现有证据并交由有权责任方” | CLOSED |
| F · 证据不足 | L67：“证据不足以支撑任何处置选择 → 先收集证据（保留现场），不用试错代替诊断” | CLOSED |
| F · 无回退 | L67：“回退点缺失或操作不可逆 → 立即升级授权，不先动手” | CLOSED |
| F · 权限不足 | L67：“处置动作超出既有授权或权限不足 → 停止相应动作、保护现有证据并交由有权责任方，不因重试预算耗尽或需要恢复而默认取得新权限” | CLOSED |

P 新增分支明确使用“配置”与“实验起点”两个对象。所链[性能正文](../../knowledge/06-training/performance-analysis.md) L95–96 要求可回退配置及从冻结起点复测；L150 明确“回退配置不撤销已发生的参数/优化器更新”，L151 要求起点不可恢复或 A 复测失败时“结论降级为探索性，不宣布优化通过”。P L72 承接一致，没有把恢复配置写成恢复训练状态。

M L84 新增链接实际指向[平台变更正文](../../knowledge/05-cluster-platform/platform-change-and-rollback.md)，其 L63 明确升级、drain、CRD 变更和回退均有授权边界；F 的[处置正文](../../knowledge/08-reliability/mitigation-and-recovery-principles.md) L134 同样要求按既有授权及现场六项字段执行。新增分支均停止权限不足的相应活动并交给有权责任方，未要求已有授权一律重新申请。S L30 记录了本项三处修订，与页面相符。**C01 无剩余缺口。**

### C02 · CLOSED

F L37 现为：“**目标维度、证据门槛、影响域（动作本身会中断谁，与故障已发生的影响范围分开判断）、状态前提、停止/回退条件、恢复判据**”。与[处置正文](../../knowledge/08-reliability/mitigation-and-recovery-principles.md) L51–62 的原表对应如下：

| 原表字段 / 实际行号 | F L37 对应项 | 核对 |
|---|---|---|
| 目标维度，L57 | 目标维度 | 一致 |
| 证据门槛，L58 | 证据门槛 | 一致，未被证据保全安排替换 |
| 影响域，L59 | 影响域，并解释为动作本身会中断谁 | 一致，与既有故障范围分开 |
| 状态前提，L60 | 状态前提 | 一致 |
| 停止/回退条件，L61 | 停止/回退条件 | 一致 |
| 恢复判据，L62 | 恢复判据 | 一致 |

F L37 后半以“**本页另需补充材料**”列出状态责任方、证据保全、重试预算与授权边界，未再冒充原表六项；“缺任何一项的动作都是盲操作”对应原文 L53，未增加新的成功保证。F L54 目标产出也改为“处置六项（目标维度/证据门槛/影响域/状态前提/停止回退条件/恢复判据）”，并单列影响范围。S L20 的原创结构归纳未声称另一组六项，L31 则准确记录字段纠正、影响域区分与产出同步。**C02 无剩余缺口，无需新增运行结果。**

### C03 · CLOSED

M L47 现明确列出“**完整依赖交集**”“**有效 baseline**”“**恢复路径**”，L84 再逐项写出停止条件。与所链[安装升级正文](../../knowledge/02-software-stack/environment-installation-and-upgrade.md)的对应为：

| 原门禁 / 实际行号 | M 的修订后原文与位置 | 核对 |
|---|---|---|
| 完整依赖交集缺失，L71 | L47：“硬件×OS×驱动×运行时×框架/引擎逐环节配套依据”；L84：“依赖交集补不到依据即停止” | 一致 |
| 有效 baseline 缺失，L72 | L47：“已有环境的升级无可复跑的 B0 即停”；L84：“已有环境无可复跑 B0 的升级必须停止” | 一致，版本档案本身不能替代结果 |
| 恢复路径未落实，L73 | L47：“含制品保全与不可逆确认”；L84：“回退路径未落定不执行变更” | 一致 |

专门核验了三种边界：

1. **只有版本档案、没有可复跑结果的升级**：M L39 的环境档案需与 L47/L84 合读；后两处已明确以可复跑 B0 为门槛，因此该情形被拦截。源文 L182 将 B0 定义为变更前环境实际跑出的验证结果，须记录环境/负载身份、判据、输出和日期，不能仅以版本清单充当 B0。
2. **首次安装**：M L47 将例外限定为“记录‘安装前状态’与清理目标，不泛化到升级”，L84 再写“首次安装例外不适用”于已有环境升级。对应源文 L72 及 L186 的安装前状态、安装目标和清理恢复目标；未为升级豁免 baseline。
3. **结果契约**：M L47 明确“结果契约字段冻结是独立的验收前提”，L84 写“未冻结 → 不得记变更验收通过”，对应源文 L101–111，特别 L109。它没有再替代原三项门禁。源文 L178–186 的同负载同判据及 R 为回退执行后结果也继续由 M L47、L67、L72–83 承接，未将回退路径确认冒充 R 的运行结果。

S L13 保留 B0/N/R 与准入门禁引自 T02-12 的出处说明；现可精确落到上述源文 L65–75、L176–186。S L32 已同步三项、首次安装例外、契约冻结和兼容性枚举的修订。**C03 无剩余缺口。**

### C04 · CLOSED

R L89 的运维/可靠性人员阅读顺序第 2 步，现写：“**运行阶段另见[性能优化](../../paths/tasks/performance-optimization.md)、[迁移与升级](../../paths/tasks/migration-and-upgrade.md)与[故障恢复](../../paths/tasks/fault-recovery.md)任务路径**”。实际相对路径独立解析如下：

| R L89 原始链接 | 解析目标 / 稳定 ID | 结果 |
|---|---|---|
| `../tasks/performance-optimization.md` | `paths/tasks/performance-optimization.md` / `path.task.performance-optimization` | 存在；本行 1 条直接入口 |
| `../tasks/migration-and-upgrade.md` | `paths/tasks/migration-and-upgrade.md` / `path.task.migration-and-upgrade` | 存在；本行 1 条直接入口 |
| `../tasks/fault-recovery.md` | `paths/tasks/fault-recovery.md` / `path.task.fault-recovery` | 存在；本行 1 条直接入口，原入口保留 |

“运行阶段”与三页性能退化、计划内变更、非计划故障的任务定位一致，放在运维角色段落语义合适；没有复制正文或要求所有角色重复三条路径。S L33 对本项接入的记录与实际一致。**C04 无剩余缺口。**本判断不覆盖同文件内其他任务修订。

## 增量语义核对

| 增量位置 | 目标正文实际依据 / 核对结论 |
|---|---|
| P L72：配置回退与实验起点恢复 | 实际链接仍为[性能分解正文](../../knowledge/06-training/performance-analysis.md)，L92、L95–98、L150–151 分别区分冻结训练状态、配置回退、主动复跑与探索性结论。新增措辞只保留只读分析及探索性结论，没有把重复基线或恢复实验说成只读，也未宣称优化已成功 |
| M L47/L84：三项门禁和契约 | [安装升级正文](../../knowledge/02-software-stack/environment-installation-and-upgrade.md) L65–75、L109、L176–196 实际承载三项、契约冻结、B0/N/R 和回退准备；[平台变更正文](../../knowledge/05-cluster-platform/platform-change-and-rollback.md) L63 承载新增授权链接。未新增平台通用回退能力或无条件支持断言 |
| M L48：兼容性依据改写 | [兼容性方法](../../knowledge/02-software-stack/compatibility-evidence.md) L47–50 的四类确为发行包矩阵/发行说明、源码分支/构建配置、项目测试声明/CI、本地验证；L34–41 要求官方声明与本地验证两轴分开。新增“按依据类型分别记录”与原文一致，未再排成单一强弱等级；逐环节有依据也未被提升为整栈官方支持（源文 L67–83 保留该边界） |
| F L37/L54/L67：六项、产出和权限 | [处置正文](../../knowledge/08-reliability/mitigation-and-recovery-principles.md) L51–62、L75–85、L132–134 分别承载六项、重试预算及授权；影响域区分、补充材料和不默认取得新权限均一致，未把预算耗尽写成自动获权 |
| R L89：P/M 新增入口、F 保留 | 三条链接实际落到上述既有任务页；短说明保持导航含义，不构成已执行或已验证的声称 |

上述关键链接均实际解析并读取目标内容；本轮没有只凭链接标题或页尾“make check 通过”自述判定语义。未发现修订引入新的无条件断言、状态责任混淆或平台/版本边界丢失。P L38、M L31、F L33 的导航草稿与 generic 边界仍在；模型审阅、`source_checked` 和导航可达均不等于硬件验证。

## 结构校验、写入范围与结论

已运行 `PYTHONDONTWRITEBYTECODE=1 make check`，退出码 0，实际输出：

```text
PYTHONPATH=src .venv/bin/python -m kb.cli check
PASS: 135 content entries; 577 sources.
Checked structure and local file links; not technical correctness or remote links.
```

只执行结构和本地链接检查。按本轮明确要求未运行 `make build`；未改 `src/kb/`，未新增或运行测试；未执行所链正文中的 profiling、调参、安装、升级、drain、重试、故障注入、续训或恢复操作。

工作区开始时已有多项他人修订与未跟踪审阅报告，本会话保留原状。只读阶段建立 713 个非忽略既存文件的 SHA-256 快照，写报告前对照无修改、无删除、无新增；四个修订文件亦再次执行行数和 SHA-256 检查，结果与开头表格一致。本轮唯一新增文件为本报告，未回填 S 或更改计划与历史审阅状态。

**C01、C02、C03、C04 全部 CLOSED，OPEN 0 项。该项任务在本审阅范围内通过。** 此结论限定于初审关闭条件及本轮增量语义，不代替其他任务验收或真实环境兼容性、性能、数值正确性与恢复验证。
