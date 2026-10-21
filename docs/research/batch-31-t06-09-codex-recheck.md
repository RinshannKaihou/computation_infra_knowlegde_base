# Batch 31 · T06-09 正式定向复核报告

## 会话元数据与结论

| 项目 | 记录 |
|---|---|
| 审阅角色 / 轮次 | 同一独立批次审阅者；初审后的首次有效定向复核；此前 high 档位轮已作废，不计轮次，本轮不引用其报告作为关闭依据 |
| 实际执行模型 / 档位 | **`gpt-6.1-sol / xhigh`** |
| 模型核验方法 | 用进程环境中的 `CODEX_THREAD_ID`、`CODEX_SESSION_ID` 定位当前 rollout JSONL，核对 L1 的会话身份，再读取本轮最新 `turn_context` 的 `model`、`effort`、`cwd` 与 `collaboration_mode.settings`；写入前再次确认最新记录未变 |
| 模型核验结果 | `model=gpt-6.1-sol`、`effort=xhigh`、`cwd=/Users/ywang2397/work/AI_reliability_knowledge_base`；`collaboration_mode.mode=default`，`settings.model=gpt-6.1-sol`、`reasoning_effort=xhigh`、`developer_instructions=null`。模型、档位与目录均符合本轮要求，未发生本轮模型/档位回退 |
| 模型核验坐标 | `/Users/ywang2397/.codex/sessions/2026/10/21/rollout-2026-10-21T23-43-28-01a15f21-b9d4-7421-9a80-18dfe410cee3.jsonl` **L374**，`2026-10-21T15:58:35.410Z`；会话身份为同文件 L1。判断使用当前最新记录，不使用初审或作废轮的旧 `turn_context` |
| 会话 ID / 执行方式 | `01a15f21-b9d4-7421-9a80-18dfe410cee3`；本地 Codex CLI 当前会话直接复核，`originator=codex_exec`、CLI `0.163.0`；未另启模型或子代理 |
| 日期 / 时区 | 2026-10-21 至 2026-10-22 / Asia/Shanghai（UTC+08:00）；本轮跨午夜，报告交付日期为 2026-10-22 |
| 正文基准 | `knowledge/06-training/index.md`，129 行；SHA-256 `a992474e971d6379b1bbca3581c3b13a4ab9a72c5a76afc2dbc02ed1b777ee18` |
| 本批取证基准 | `docs/research/batch-31-t06-09-sources.md`，37 行；SHA-256 `7c00fec5b3463737244b21d31caf0417c8c98b24d6464567a2991a4574e80e39` |
| backlog 基准 | `plans/full-coverage-backlog.yaml`，7772 行；SHA-256 `53c792ea1e46cdd5eeee7a428c7ea0b431b082feeb01955f2f683ac25edc04ef` |
| 写入范围 | 本轮开始时指定报告文件不存在；仅新增本报告，不修改正文、取证、计划、registry、初审或其他历史报告、构建产物 |

**正式复核结论：初审 C01、C02 全部 CLOSED；用户指明的 R01 链接项也已落实并核实。OPEN 为 0，无需新增 R02。T06-09 在初审及本轮定向复核范围内通过。** 通过的是导航、交付账面与证据边界，不是实际训练、恢复、性能或平台验证。

`[frontier_llm]` 在本报告中仅作为引用标记的规则说明；会话历史中该字面量曾来自写作指南原文的工具输出等引用内容，不作为本轮回退事件。当前执行身份以 L374 的 `turn_context` 为准；同会话中过去作废轮的 high 记录也不冒充当前轮档位。

## 范围与方法

以[初审报告](batch-31-t06-09-codex-review.md) L103–121 的 C01/C02 关闭条件为基准，直接核对当前[正文](../../knowledge/06-training/index.md) L86–96、L129 和[本批取证](batch-31-t06-09-sources.md) L15、L29–37。R01 按用户要求独立打开两处补链及其目标报告核对，不引用已作废报告的判定。

本轮重新读取相关框架/RL 方法段、两篇实验的元数据与实际结果节，以及 T06-01～T06-08 所指最终复核的结论和范围。对 backlog 做文本 diff、完整 YAML 递归差异和开放 gap ID 集合比较；对照主题盘点与任务状态。只检查本次修订相关回归，没有重新全量审阅 40 格入口，也没有重做兄弟篇上游技术审阅或获取新外部来源。

## C01/C02 与 R01 逐项核对

| 项目 / 关闭条件 | 判定 | 当前位置、证据与关闭依据 |
|---|---|---|
| C01 · 已交付方法、未执行结果、unknown 分开，06.3/06.4 不再误报缺失 | **CLOSED：此子项满足** | 正文 L88 明列三类；L92 将 06.3 改为已有小规模执行路径验证方法、缺执行结果，与[框架正文](../../knowledge/06-training/framework-execution.md) L124–128 的连通性/恢复一致性设计及未执行声明一致。L67 的“执行验证仍缺”由 L92 明确为执行结果，不再当作方法缺失。L93 将 06.4 改为已交付 verl v0.9.1 legacy V0 同步/一步异步/完全异步样板，V1 控制流等仍 unknown、未实测，与[RL 正文](../../knowledge/06-training/rl-rollout-consistency.md) L56、L145–153、L198–204、L228 一致。L129 后续方向同步，不再称受控异步样板待补 |
| C01 · 九项账面差异逐项说明，状态与证据一致 | **CLOSED：此子项满足** | 正文 L94、取证 L31 明确列出九项未同步及本批关闭；当前 backlog 恰好九项内容 gap 的 status 从 open 改 closed，无其他语义变更；主题盘点和对应任务、最终复核证据一致，详见下节。未把未执行实验记为完成，也没有顺带提升 T06-09 或主题最终验收状态 |
| C01 · 任务来源、修订和最终复核可定位 | **CLOSED：此子项满足** | 正文 L91 的 T06-01～T06-07 七组来源/最终复核链接共 14 个，文件存在且对应任务正确；本轮重新读取其最终关闭结论，不把存在报告本身当作技术保证。T06-08 的实际定位现由下行 R01 补齐，相关保留边界可追溯 |
| R01 · T06-08 最终复核链接 | **CLOSED** | 正文 L90 的 `../../docs/research/batch-26-t06-08-codex-recheck.md` 与取证 L15 的 `batch-26-t06-08-codex-recheck.md` 均解析为同一实际文件。已打开[目标报告](batch-26-t06-08-codex-recheck.md)，标题/任务正确；L43 保留正式配套未知，L49 保留 mid-step、whl、重分片及未验证边界，L53 为 C01–C05 全部关闭的限定结论。取证 L37 记录补链，与实际修改相符；不是只补了无效路径或相邻任务报告 |
| C02 · 实验数量与对象一致，独立/内嵌/复用可区分且全部未执行 | **CLOSED** | 正文 L96 明列[精度差异](../../knowledge/06-training/gpu-npu-precision-difference-experiment.md)和[恢复状态](../../knowledge/06-training/checkpoint-state-recovery-experiment.md)两篇独立条目，并解释内嵌与复用关系；L82 慢 rank 专用实验仍待补，L83/L84 分别复用精度设计、引用性能篇内嵌设计，L129 保留慢 rank 后续补齐。内容目录中本章确实只有这两篇 `type: experiment`；两篇均为 draft / not_verified、空环境与 evidence_refs，实际结果节分别为 L151–155、L172–176，继续明确未执行。取证 L32 记录相同修订 |

**C01 综合判定 CLOSED，C02 CLOSED。** 取证 L20/L26 保留首轮旧说法，L31 已明确订正为“已有方法/样板、未执行结果及剩余 unknown”，本轮按修订历史合读，不将首轮旧描述重新当作当前缺口账面。取证 L36–37 如实记录作废过程及补链；这段过程记录不代替本轮独立证据。

## 九项 backlog 同步与回归核对

| 缺口 / backlog 位置 | 本轮核对的关闭依据与保留范围 |
|---|---|
| 06.2-G3 / L2249–2256 | [T06-06 最终复核](batch-25-t06-06-codex-recheck-4.md) L10–14 明确组合并行映射/性能验证方法的内容审阅阻塞已消除，并区分方法已交付与实验未执行；与初审已核实的候选对照、组员与判据一致 |
| 06.4-G2/G3 / L2354–2369 | [T06-04 最终复核](batch-25-t06-04-codex-recheck-4.md) L6 记录累计发现关闭、任务在既定范围通过；本轮重读的 RL V0 recipe 与单变量设计实际存在。V1 控制流和具体平台组合未知、未实测继续保留 |
| 06.5-G1/G2/G3 / L2408–2430 | [T06-05 最终复核](batch-25-t06-05-codex-recheck-3.md) L11–13 记录原发现全部关闭、既定内容范围通过；结合初审已核实的机制、质量判据及来源案例，不将此关闭扩大为真实收敛或质量实验验收 |
| 06.6-G1/G2/G3 / L2468–2490 | 方法部分由 T06-06 上述最终复核支持；[T06-07 最终复核](batch-25-t06-07-codex-recheck-3.md) L20–25 关闭来源同步余项，与初审已核实的来源案例对应。作者报告/本库未复现、修复 release 等未知条件继续保留 |

只读比较当前 backlog 与 Git HEAD，结果如下：

- 原始文本 `status: open` 数量和解析后的 open gap 数均为 **54→45**。
- 从 open 集合移除的恰好是上述 **9 个指定 gap ID**，新增开放项为 0；其余 **45 个 open gap 的 ID 和完整条目内容均未改变**。
- 文本 diff 只有九行 `open→closed` 替换（9 行增、9 行删）；整份 YAML 的语义差异也恰好 **9 个 status 叶字段**。无条目增删；gap_text、task_refs、closure_lane、validation_refs 及其他字段未变，九项仍属于 content lane。
- [主题盘点](../../plans/topic-coverage.yaml) 中八个训练主题均为 covered、`gaps: []`；T06-01～T06-08 仍为 done/delivered。九项同步有对应内容与最终复核依据，不只是从 done/covered 标签推导自动关闭。
- T06-09 自身仍为 planned/needs_content_inputs，八主题 `content_acceptance_status` 仍为 planned。本轮不代改这些字段；通过结论与后续账面登记分开，其他领域开放项未受影响。

相关历史报告中的实际模型记录（包括 unknown）及限定审阅范围按原样保留，本轮不将其追改为新模型或扩大为全面验证。

## 修订回归、校验与写入范围

正文交付小节 L86–96 的 **23 处内联链接目标全部存在**，包括七组任务记录与新增 T06-08 入口；取证中的 T06-08 链接也已单独核对目标同一性。`training.index`、index/training 主归属、draft 和 generic 未变。L95 的三组框架档案互不外推，L93 的 V0/V1 边界、L96 的来源案例/未执行实验及 L90 的重分片与 TTP 保留限制没有升级。慢 rank 专用案例/实验待补也没有被通用性能方法自动充作已交付。

本轮未发现需要新立 **R02** 的回归问题。已经关闭的是 C01/C02 及用户指明的 R01 定位项，不重新评价初审已通过的其他方面。

已执行 `PYTHONDONTWRITEBYTECODE=1 make check`，结果 **PASS：126 content entries / 575 sources**。该检查只验证结构与本地引用，不验证技术正确性、远程内容或平台兼容。遵守仅新增报告的范围，未执行 `make build`、`make test`，未执行任何上游训练、保存、恢复、profiling 或故障注入实验。

本轮开始时指定报告不存在；正文、backlog 的作者修改及已有初审/取证记录均视作输入。写入前后对 **676 个既存仓库文件（含 build 现存文件）**作 SHA-256 对照，既存文件无变化、无删除，仅新增本报告；三份输入的行数和指纹保持头表数值。没有重建、保存或引用已作废报告的旧内容。

**总体结论：全部 CLOSED，OPEN 为 0。T06-09 通过初审与本轮正式定向复核的既定范围。** 本报告不代表整个 Batch 31 通过，不关闭仍保留的 unknown 或真实验证轨道，也不改变正文、案例与实验的编辑/验证状态。
