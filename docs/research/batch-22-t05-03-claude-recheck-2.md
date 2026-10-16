# 第二十二批 T05-03 第二次定向复核（作者第二轮修订后）

复核日期：2026-10-14（实际取证日）。

**结论：不通过。范围内 5 项（B22-C12/C14/C16/C17/C21）：CLOSED 1（C12），OPEN 4（C14、C16、C17、C21）。B22-C12–C21 全部 10 项累计 CLOSED 6（C12、C13、C15、C18、C19、C20），OPEN 4。** 未新增发现 ID。

四项 OPEN 的共同原因：修订落在了来源记录、登记或正文的一处，同一说法在正文其他位置没有同步，有两处仍是原句：

- C14：正文 L140 自相矛盾的"只读头注释（test12.7 约 L60–120…）"原句未改；L23"十九页"与 L174 来源清单未补 sacct；头注释目的由谁读取仍未写明。
- C16：引文补全时在反引号内插入 `(e.g. …)`，把原文的条件句改成了举例；"影响坏卡/分卡对账"仍未标为本库推论；`omitted with an error` 仍非原文连续片段。
- C17：代码块已删"scontrol epilog 状态"，L150 仍保留原句。另追记：失败组的 `squeue` 不加 `-t` 时，默认不列已终止作业。
- C21：L132 第二列已改对，第三列仍保留"Billing 经 PriorityWeightTRES 才参与 priority"，与 tres 页 PriorityWeightTRES 节原文相反。

审阅者角色独立于作者修订角色。审阅模型为 `claude-opus-5-5`，由用户本次明确要求试用。这不是既有的 `gpt-6.1-sol / xhigh` 批量审阅约定，也不改写该约定。本会话内未见 `[frontier_llm]` 标记、认证失败或模型自报变化。推理等级、`modelUsage` 等运行元数据审阅者无法在会话内读取，不补造。若操作方在运行记录中发现模型不一致或认证问题，按约定本轮作废，不留档、不引用。

本轮只写本报告一个文件。未改作者正文、来源记录、修订映射、登记、索引或计划；未部署 Slurm、未提交作业、未执行任何 Slurm 命令或测试用例。模型复核不构成平台或现场验证。

## 输入（以 SHA-256 识别）

| 输入 | SHA-256 | 与任务给定前缀 |
|---|---|---|
| [T05-03 正文](../../knowledge/05-cluster-platform/slurm-jobs-and-device-resources.md)（177 行） | `9b276def0a3666c6c1c2540f000261136282177371b91eeb6d5fd12e29c8c5f9` | 一致 |
| [作者来源记录](batch-22-t05-03-sources.md)（25 行） | `5455ce752d161cb3171527796a90d422a1ee5af6b7d4dc249275e736b3d943fa` | 一致 |
| [修订映射](batch-21-review-fixes.md)（T05-03 第二轮修订节 L201–207） | `9618c55c6d70a6019d0c106fdc6d961cde13a29cdea09191302fd527dab4e1f5`；L201–207 段 `b2137489d805a76949a0d0a9b14917d077ba477d9c7ef692541a8d5d613d25ba` | 一致 |
| [来源登记](../../sources/registry.yaml)（`make check` 计 438 项；T05-03 段 L5386–5418） | `54197389a41fa9d4325dc87d175990d864f581c8af3b9da878e8118956e5d846`；L5386–5418 段 `56e8e74a374560f3caf5049c8bce50c98e4aa887454117a88ca11b72e4fa4030` | 一致；段哈希与前次 `b8a28396…` 不同，系作者本轮修订（L5413）所致 |
| [前次复核报告](batch-22-t05-03-claude-recheck.md)（剩余关闭条件权威来源） | `b1eaf6d3f8f0ed2fa89ac1236996be8b17192b1c927011a1e673f594d5778109` | 任务未给前缀，记实值 |
| [初审报告](batch-22-t05-03-claude-review.md) | `a0830797ada7f12ae810689736c9d0ac150d1a1b045dcf50b415cbb72f21f9c6` | 任务未给前缀；与前次复核所记相同 |
| [任务计划](../../plans/full-coverage-backlog.yaml)（T05-03 L5468–5509，acceptance L5487–5492） | `5f9bcf865b8c77e13cc8ee5f1c03140c37b86f558d8227d8bb2080249f4fcfc3` | 任务未给前缀；与初审、前次复核所记相同，计划未变 |

全部输入在取证开始和成稿前各哈希一次，结果相同。

## 取证方法与限制

- 方法：全部用 `curl -sSL` 默认 TLS 校验只读获取。20 个归档页 HTTP 均为 200；HTML 去标签后按文字核对，不只判可达性。原文放在新建临时目录 `/tmp/b22rec03d/`（取证前不存在），未入库。
- 与前两轮逐字节比对：20 页 SHA-256 前 8 位与初审、前次复核逐一相同（overview `87e97389`、job_state_codes `8a023811`、job_reason_codes `f8e4f3c9`、squeue `48e57603`、sinfo `b67afb79`、scontrol `da776891`、sbatch `132d28b4`、scancel `956cfa77`、priority_multifactor `acd6dead`、qos `f6b74df2`、reservations `ef527511`、prolog_epilog `6d83380c`、slurm.conf `f4151769`、sacct `d96f8299`、gres `4c7a5874`、gres.conf `21aeb902`、tres `2d08f826`、cgroups `49f81235`、cgroup.conf `8835c198`、resource_binding `47985fe9`）。前两轮所引原文本轮仍适用。
- 版本锚：`git ls-remote` 显示 `refs/tags/slurm-24-11-7-1` 为 tag 对象 `9d1ef1877186d8101769352831c8f0fe303df31c`，`^{}` 为 commit `defaf214db2e55326f45ab08f1bde5b2036d9f5d`，与前两轮及登记一致。
- testsuite：从 `raw.githubusercontent.com/SchedMD/slurm/slurm-24-11-7-1/testsuite/expect/` 重取 14 个文件，均为 HTTP 200。SHA-256 与前次复核所记完整值逐一相同（如 test12.7 `4b457e86e143973a…`、test31.2 `3fbfffea104abaac…`）。
- 渲染核对：正文 L25 起的正文部分分别用 pandoc 2.12（`-f gfm`）和 markdown-it-py 4.0.0（commonmark＋table）渲染。两者结果一致：7 张表、68 个 `tr`，等于源文件 75 个表格行减 7 个分隔行，即全部表格行都在表内。标题列表见"范围外观察"。
- `make check`：`PASS: 96 content entries; 438 sources.`，运行前后 `git status --porcelain` 相同。它只校验结构与本地链接，查不出下文的标题渲染问题。`make build` 未运行，因为它会写 `build/`，超出"只写一份报告"的范围。
- 限制：
  - 测试文件只读了 test12.7 头注释（L3–4）、L33–34（跳过条件）、L64 与 L77（`-D` 与 `--duplicates` 两种写法），以及 test31.2 L120–127。断言未审计，tag 上的 CI 结果未查，所有测试都没有执行。
  - 未用 GitHub API，未枚举 `testsuite/expect` 目录。
  - 前两轮未取的 gang_scheduling、heterogeneous_jobs、preempt、srun、sacctmgr、resource_limits 页本轮仍未取。
  - 正文、来源记录均未入 git（工作区 `??`），前一版正文无法取回。凡判断"本轮引入还是原本就有"处，只能依前次复核引述推断，或注明无法判定。
  - 未核对 SchedMD 站点许可与仓库根 LICENSE/DISCLAIMER。

### 关键抽查点（原文文字核对）

| 抽查点 | 原文 | 结果 |
|---|---|---|
| scontrol COMMANDS 节 `completing`（作者自述已独立复核） | COMMANDS 节（去标签文本 L207 起）条目：`completing` — `Display all jobs in a COMPLETING state along with associated nodes in either a COMPLETING or DOWN state.`；全页 `epilog` 出现 0 次 | 作者自述属实；L165 可用。L150 未同步 → C17 |
| scontrol NODES UPDATE `State=` | DOWN `Stop all running and suspended jobs and make the node unavailable for new jobs`；DRAIN `… leaving the node in a DRAINED state once all the jobs have completed`；RESUME `Not an actual node state, but will change a node state from DRAIN, DRAINING, DOWN or REBOOT to IDLE and NoResp`；UNDRAIN `will not change the node's base state (e.g. DOWN)`；`Setting a node DOWN will cause all running and suspended jobs on that node to be terminated`；`some of them are not valid new node states given their prior state`；`Reason=` 适用 DOWN/DRAINED/DRAINING/FAILING/FAIL；`ResumeAfter=` | L86 属实 → C12 |
| gres GPU Management 编号映射 | `Mapping between these two is nondeterministic and system dependent, and could vary between boots after hardware or OS changes. For the most part, this assignment seems fairly stable. However, an after-bootup check is required to guarantee that a GPU device is assigned to a specific device file.` | L130 反引号内插入 `(e.g. …)`，不是原文 → C16 |
| gres AutoDetect 校验失配 | `If the system-detected GPU differs from its matching GPU configuration, then the GPU is omitted from the node with an error.` | L130 `omitted with an error` 仍非连续片段 → C16 |
| tres PriorityWeightTRES 节 | 示例 `PriorityWeightTRES=CPU=1000,Mem=2000,GRES/gpu=3000` 后紧接：`The Billing TRES is not available for priority calculations because the number isn't generated until after the job has been allocated resources — since the number can change for different partitions.` | 该句就在 PriorityWeightTRES 节内。L132 第三列"Billing 经 PriorityWeightTRES 才参与 priority"与之相反 → C21 |
| tres TRESBillingWeights 节 | `TRESBillingWeights is only used when calculating fairshare and doesn't affect job priority directly … If you want TRESs to play a role in the job's priority then refer to the PriorityWeightTRES option.` | L132 第二列"用于 fairshare……Billing 本身不直接参与 priority"可成立（经 fairshare 间接影响） |
| job_reason_codes `Cleaning` | `Cleaning — The job is being requeued and still cleaning up from its previous execution.` | L109 释义属实 → C17 |
| job_state_codes `COMPLETING` | `job has finished or been cancelled and is performing cleanup tasks, including the epilog script if present` | L109"后者为结束/取消"有出处 |
| squeue `%R` 与 `-t` | `%R` `For terminated jobs with failure: an explanation as to why the job failed is printed within parenthesis`；`-t, --states` `If no state is specified then pending, running, and completing jobs are reported`；`If "all" is specified then jobs of all states will be reported` | L160 不带 `-t` 时看不到已终止作业 → C17 追记 |
| slurm.conf `MinJobAge` | `The minimum age of a completed job before its record is cleared from the list of jobs slurmctld keeps in memory … The default value is 300 seconds.` | squeue 只能在此窗口内看到已结束作业 → C17 追记 |
| sinfo `-t, --states` | 可选值含 `COMP, COMPLETING, DOWN, DRAIN (for node in DRAINING or DRAINED states)` | L163–164 可改用 `-t completing`（非阻断） |
| squeue `%D` | `Number of nodes allocated to the job or the minimum number of nodes required by a pending job` | L157–158 提交组可补（非阻断） |
| sacct `-D, --duplicates` | 首句 `If Slurm job ids are reset, some job numbers will probably appear more than once … Such jobs can be distinguished by the "submit" time stamp`；`--duplicates … all records that match the selection criteria will be returned` | L162 主体属实；首句未补（前次非阻断建议，仍非阻断） |
| test12.7 / test31.2 | test12.7 L3–4 `Validate that sacct -D shows correct job steps and states`；L33–34 nosteps/nojobs 跳过；L64 `-D`、L77 `--duplicates`；test31.2 L123–125 接受 `launch_failed_requeued_held` 或 `JobHeldAdmin` | 头注释与行段内容属实；取证归属见 C14 |

## 逐项判定

### B22-C12 — CLOSED（P1）

位置证据：

- 节点状态表 L76–84 与节点动作段 L86 之间有空行 L85 分隔，动作段已在表后另立段落，并写明 [scontrol] NODES UPDATE 节。pandoc GFM 与 markdown-it 均把 L82（FAIL/FAILING）、L83（后缀）、L84（分区 AVAIL）渲染在"节点状态"表内（该表 7 个 `tr`：表头＋6 行）。全文表格行 68/68 在表内。
- L86 动作语义与 scontrol 原文逐项一致（见抽查表），前态×新态组合记 unknown。
- L177"待确认"已无"节点 update State 全枚举"，改为"节点前态×新态合法组合（文档称部分组合无效但未列出）"。

非阻断：

- L80"终止该节点上运行与挂起的作业"的证据列仍为 sinfo＋slurm.conf，未补 scontrol（前次非阻断，未处理）。
- L88"恢复路径见节点动作表"、L110"（见节点动作表）"、来源记录 L23"见正文节点动作表"所指的是 L86 段落，不是表。宜统一称"节点动作段"或"节点状态动作说明"。

### B22-C14 — OPEN（P2）：来源记录与登记已部分同步；正文原句未改，页数与清单未补

已满足：

- 来源记录 L16 写明"test12.7 约 L60–120、test31.2 L122–125 行区间为审阅者已核对范围（含代码，不仅头注释），作者侧不冒充已读"。
- 登记 L5413 同样把行区间标为"审阅者已核对行区间……含代码"。

未满足（前次复核三条剩余关闭条件，逐条）：

1. **"删去或改写'只读头注释（test12.7 约 L60–120…）'这句自相矛盾的话"——未做。** 正文 L140 仍为原句"只读头注释（test12.7 约 L60–120、test31.2 L122–125），未审计断言……"，与来源记录 L16、登记 L5413 新写的"含代码，不仅头注释"在同一事实上直接矛盾。
2. **统一 testsuite 取证口径——未做完。**
   - 行区间已标为审阅者取证。但**头注释目的**由谁读取，三处都没有写明。
   - 仍只写"存在性"的位置：来源记录 L3"testsuite 用例存在性"与 L5"testsuite 仅目录/用例编号存在性"；正文 frontmatter L23"testsuite 用例存在性"、L140"存在性见 testsuite"、L176"上文用例编号的存在性"；登记 L5409 标题"（存在性）"。
   - 引用头注释目的原句的位置：正文 L140、L162"见 test12.7 头注释目的"；来源记录 L16；登记 L5418"头注释目的可引用为上游行为样本"。
   - 作者若未自行打开文件，这些引用须标为审阅者取证；若已打开，须在来源记录写明方法与日期，并改掉上列"存在性"表述。两种处理都未落盘。
3. **"L23 页数与 L166 来源清单补上 sacct"——未做。** 正文 L23 仍为"归档十九页"，"来源与更新范围"L174 列表仍无 sacct；来源记录 L3 也仍为"十九页"。正文 L88 却写"所取 20 页"，页数在正文内部也不一致。sacct 已在 L162 引用、登记 L5396 已纳入。

修订映射 L204 写"测试读取范围诚实表述（头注释＋审阅者行区间）；记录/登记同步"，与正文实际未改不符。

剩余关闭条件：

- 改写正文 L140 那句：删去"只读头注释"，或改为"头注释目的（及 test12.7 约 L60–120、test31.2 L122–125 含代码的行区间）为审阅者取证"。
- 写明头注释目的的取证归属，并按此同步来源记录 L3/L5、正文 L23/L140/L176、登记 L5409/L5418。
- 正文 L23 与来源记录 L3 的页数改为二十页（含 sacct），L174 清单补 sacct。

非阻断：L162 注释宜补 sacct 页首句的限定"可能含 job ID 重置后的其他作业，按 submit 时间区分"（前次已提，未处理）。

### B22-C16 — OPEN（P2）：`an after-bootup check is required` 已补；引文被改写，推论未标，另一处引文仍非原文片段

已满足：L130 写入原文 `an after-bootup check is required`，逐字一致。前次已满足的绑定、环境变量范围、drain 口径、MIG、TRES 记账前提均未回退。

未满足：

1. **反引号内的引文不是原文。** L130 为 `` `nondeterministic and system dependent, and could vary between boots (e.g. after hardware or OS changes)` ``。原文为 `… and could vary between boots after hardware or OS changes.`，没有 `(e.g.` 与括号。插入 "e.g." 后，"硬件或 OS 变更后"从限定条件变成了举例，意思成了"重启之间都可能变，硬件/OS 变更只是一例"。前次关闭条件要求"按原文补全条件句"，修订反而把条件句改成了举例，并且仍放在反引号里冒充原文。原文随后的 `For the most part, this assignment seems fairly stable` 也未写入；这一句前次未列为关闭条件，此处只作提示。
2. **"（编号不稳直接影响坏卡/分卡对账）"仍未标为本库推论。** 这是初审 C16 明确标为"审阅者推论（非原文）"的内容，前次剩余关闭条件第二项要求标注，L130 原样保留。
3. **`omitted with an error` 仍在反引号内，仍非原文连续片段。** 原文为 `the GPU is omitted from the node with an error`。前次剩余关闭条件第三项，未处理。

修订映射 L205 写"编号映射引文补全（硬件/OS 变更＋bootup 检查要求）"，第 2、3 项在映射中没有提及。

剩余关闭条件：

- L130 引文改为原文连续片段（`nondeterministic and system dependent, and could vary between boots after hardware or OS changes`），或去掉反引号改为转述，并保留"硬件或 OS 变更后"的条件含义。
- "编号不稳直接影响坏卡/分卡对账"标为本库推论。
- `omitted with an error` 改为原文连续片段 `is omitted from the node with an error`，或去掉反引号改为转述。

### B22-C17 — OPEN（P2）：Cleaning、节点 DOWN 分支与代码块分组已补；L150 仍保留无出处字段；失败组命令看不到已终止作业

已满足（前次四条剩余关闭条件中的三条）：

- **Cleaning**：L109 新增"重排清理中（Cleaning）"行，释义"作业正被重排、仍在清理上一次执行"与原文一致，写出了与重排的关系，证据列为 reason 页。
- **节点 DOWN 终止作业**：L110 新增，写"先看节点态与 `Reason=`，再看作业终止原因"，与 C12 的节点动作段互引，证据列为 scontrol＋sinfo。
- **代码块分组与 `%R`**：L157–167 按"提交 / 失败 / 重排队 / 清理"四组加注释，失败组有 `squeue -o "%i %T %R"`；清理组改用 `scontrol completing`，有出处（见抽查表）。

未满足：

1. **"删去'scontrol epilog 状态'，或改为有出处的 `scontrol completing`"——只改了代码块，正文 L150 未改。** L150 仍为"清理：sinfo COMPLETING/scontrol epilog 状态"。L165 的注释写"epilog 状态无 scontrol 出处，不写"，与 L150 在同一页内直接矛盾。scontrol 页全文"epilog"出现 0 次（本轮复核）。

追记（本轮查实，修订引入）：

2. **失败组命令看不到已终止作业。** L160 `squeue -o "%i %T %R"` 未带 `-t`。squeue 页 `-t, --states`：`If no state is specified then pending, running, and completing jobs are reported`。因此 `%R` 对 `terminated jobs with failure` 的失败说明，按样板写法不会出现；须加 `-t all`（原文 `If "all" is specified then jobs of all states will be reported`）或显式列出终止态。另外，已结束作业只在 slurmctld 内存保留 `MinJobAge`（slurm.conf 文档默认 300 s，站点实际 unknown）。超出该窗口后要靠 sacct。这影响 acceptance 4"来源支持的失败观察样板"。

剩余关闭条件：

- L150 删去"scontrol epilog 状态"，改为与 L165 一致的 `scontrol completing`。
- L160 加 `-t all`（或列出终止态），并注明 squeue 只在 `MinJobAge` 窗口内显示已结束作业，超出后用 sacct。

非阻断：

- 提交组 L157–158 注释写"参数与实分数"，但 `-o "%i %T %r %q %P"` 不含节点数；可补 `%D`（`Number of nodes allocated to the job …`）。
- 两条 squeue 命令以 `# ` 注释掉，其余命令未注释，未说明原因。宜统一，或注明原因。
- 清理组注释为"节点 COMPLETING 与未完成作业"，但 `sinfo -R -t drain,down` 不含 COMPLETING；sinfo `-t` 可选值含 `COMPLETING`。
- L109 条件列"前者终态为重排"：重排不是终态（REQUEUED 为 flag），宜改"去向"。Cleaning 是 reason，COMPLETING 是状态 flag，属于不同维度，宜点明。
- L165 `scontrol completing` 注释"查看正在清理中的作业"漏了原文"及处于 COMPLETING 或 DOWN 的关联节点"。

修订映射 L206 写"样板按四场景分组＋`scontrol completing`"，代码块属实；L150 未同步，映射未提及。

### B22-C21 — OPEN（P3）：Billing 的正确说法已加入第二列；错误原句仍留在第三列

已满足：L132 第二列加入原文 `The Billing TRES is not available for priority calculations`，并转述"Billing 本身不直接参与 priority"。按 TRESBillingWeights 节 `only used when calculating fairshare and doesn't affect job priority directly`，Billing 经 fairshare 间接影响 priority，"不直接"可以成立。

未满足：**L132 第三列仍为"Billing 经 PriorityWeightTRES 才参与 priority"。** 前次追记的正是这一句。tres 页中 `The Billing TRES is not available for priority calculations` 一句紧接在 PriorityWeightTRES 示例之后、同属 PriorityWeightTRES 节，原文的意思正是 Billing 不能经 PriorityWeightTRES 参与 priority。现在同一行的第二列与第三列互相矛盾，第三列与原文相反。

前次剩余关闭条件的后半句"要让 TRES 影响 priority，用 PriorityWeightTRES 按 TRES 类型加权，并引 tres 页 PriorityWeightTRES 节"也未写入。

修订映射 L207 写"Billing TRES 纠正（不直接参与 priority）"，未提第三列。

剩余关闭条件：删去 L132 第三列"Billing 经 PriorityWeightTRES 才参与 priority"，改为"要让 TRES 影响 priority，用 PriorityWeightTRES 按 TRES 类型（CPU/Mem/GRES 等）加权；Billing 不在其列"，引 tres 页 PriorityWeightTRES 节。

非阻断（前次已提，均未处理）：

- L71 与 L72 重复列 PartitionNodeLimit，且 L71 将其归入"账户或 QOS 组限额"。
- L99"只有 batch job 可重排……PrologSlurmctld"的证据列仍为"同上"（sbatch），实出 prolog_epilog 页。
- 来源记录 L13"交互式 job 重排队语义以 scontrol 为准"、L15"AutoDetect 四类字符串"与正文修正后口径不一致；登记 L5407"仅见 NVIDIA/AMD/Intel/AWS 四类字符串"同此。

## 范围外观察（不计入本轮判定；下轮须一并修正）

**正文 L88 整段被渲染为三级标题。** L88 以 `### ` 开头，后接约 570 字符的健康职责全文。pandoc GFM 与 markdown-it 都把整段渲染为一个 `<h3>`：markdown-it 计标题内容 574 字符；pandoc 生成同样长的锚点 id。目录与页面中会出现一个整段长的标题，正文里没有对应段落。`make check` 未报出。

- 这段属于 B22-C13（已 CLOSED，不在本轮范围）的位置证据；它也紧挨 C12 本轮重排的节点动作段。
- 前一版正文不在 git 中，无法判定 `### ` 是本轮修订引入还是原本就有。前次复核 C13 判定的依据是文字要素，没有记录该段的渲染形态。
- 按任务要求不新增发现 ID，也不重开范围外的 C13。理由：这不是事实错误，内容要素完整，C13 的关闭条件仍满足；问题只是 Markdown 结构，一处机械修改即可修好。
- 修法：把 L88 拆为标题行"### 健康与节点状态职责"与下方段落。下轮复核用 GFM 渲染器核对标题列表。

## acceptance 对照

| acceptance | 判定 | 未关闭项 |
|---|---|---|
| 1 固定 release/commit 与官方文档；守护进程、Job/Step、pending/running/completing/terminal、cancel/requeue 与资源清理 | 未完全满足。成立：tag/commit/归档路径固定；Cleaning 分支、节点 DOWN 分支、`scontrol completing` 有出处。剩余：L150"scontrol epilog 状态"仍无出处 | C17 |
| 2 GRES/TRES、autodetect/binding、cgroup、健康/节点状态职责；一种 NVIDIA GPU 条件；NPU 无证据即 unknown | 未完全满足。成立：after-bootup check 已写入、NPU unknown 保留。剩余：编号映射引文被改写成举例、推论未标、引文非连续；Billing 第三列与原文相反。另：健康职责段渲染为标题（范围外观察） | C16、C21 |
| 3 Slurm 状态、等待原因、配额/优先级/预留、节点 DRAIN/DOWN/RESUME 与成组资源条件；不套用 K8s 同名术语 | 范围内满足：节点状态表完整渲染，动作语义有出处，待确认已收窄 | — |
| 4 来源支持的提交/失败/重排队/清理观察样板与最小验证设计；不提交作业、不推断设备可用即应用成功 | 未完全满足。成立：代码块四组分组、`%R`、`scontrol completing`、只读与未执行声明。剩余：失败组 squeue 不带 `-t` 看不到已终止作业；L150 未同步；testsuite 取证口径与页数清单未统一 | C14、C17 |

修订映射 L203–207 中，C12 与实际落盘一致。C14、C16、C17、C21 的映射描述都比实际落盘多：正文 L140、L130 后两处、L150、L132 第三列均未改。映射宜按实际落盘内容描述。

## 结论

**T05-03 第二次定向复核不通过。范围内 5 项：CLOSED 1（C12），OPEN 4（C14、C16、C17、C21）。B22-C12–C21 累计 CLOSED 6，OPEN 4。** 未新增发现 ID；C17 有一条本轮追记（squeue 默认不列已终止作业）。

- 剩余工作都是逐句修改，不需要新取证：
  - C14：改 L140 一句；写明头注释目的的取证归属并同步三处"存在性"；页数改二十、清单补 sacct。
  - C16：L130 两处反引号引文改为原文连续片段或转述，推论加标注。
  - C17：L150 与 L165 统一；L160 加 `-t all` 并注 `MinJobAge` 窗口。
  - C21：删 L132 第三列错误原句，补 PriorityWeightTRES 按类型加权的说法。
  - 范围外：L88 拆出标题行。
- 建议作者修订时对上列每条主张在正文、来源记录、登记中全文检索同义表述再提交。本轮四项 OPEN 中有三项是"改了一处、漏了另一处"。
- 修订后须对 C14/C16/C17/C21 做定向复核，并用 GFM 渲染器核对 L88。
- C21 第三列的错误原句改正前，L132 该行不宜视为已核对。
- 正文没有虚构命令输出或实测结果，NPU/Ascend 保留 unknown，范围声明与 `verification.notes` 写明未提交作业、未执行 Slurm 命令，这几点仍满足要求。
- 本复核只覆盖编辑与来源层面。文中的 Slurm 行为都是文档或测试源码层证据，不得标为 reproduced。
