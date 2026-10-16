# 第二十二批 T05-03 第三次定向复核（作者第三轮修订后）

复核日期：2026-10-14（实际取证日）。

**结论：不通过。范围内 4 项（B22-C14/C16/C17/C21）：CLOSED 3（C14、C16、C17），OPEN 1（C21）。B22-C12–C21 全部 10 项累计 CLOSED 9，OPEN 1。** 未新增发现 ID。C14 有一条追记，C17 有一条精度提示，均为非阻断。

C21 未关闭的原因：TRES 行（正文 L135）第三列开头已加入正确说法"PriorityWeightTRES 按 TRES 类型加权，Billing 不在其列"，但前两轮指出的错句"Billing 经 PriorityWeightTRES 才参与 priority"没有删，仍在同一格后半段。渲染后同一单元格内两句直接矛盾，后一句与 tres 页 PriorityWeightTRES 节原文相反。剩余工作只有删除这一句。

审阅者角色独立于作者修订角色。审阅模型为 `claude-opus-5-5`，由用户本次明确要求试用。这不是既有的 `gpt-6.1-sol / xhigh` 批量审阅约定，也不改写该约定。本会话内未见 `[frontier_llm]` 标记、认证失败或模型自报变化。推理等级、`modelUsage` 等运行元数据审阅者无法在会话内读取，不补造。若操作方在运行记录中发现模型不一致或认证问题，按约定本轮作废，不留档、不引用。

本轮只写本报告一个文件。未改作者正文、来源记录、修订映射、登记、索引或计划；未部署 Slurm、未提交作业、未执行任何 Slurm 命令或测试用例。模型复核不构成平台或现场验证。

## 输入（以 SHA-256 识别）

| 输入 | SHA-256 | 与任务给定前缀 |
|---|---|---|
| [T05-03 正文](../../knowledge/05-cluster-platform/slurm-jobs-and-device-resources.md)（181 行） | `a3327575e8e29c24a630d09a021a0be572312c82fe461bf1feaab5d71476831b` | 一致 |
| [作者来源记录](batch-22-t05-03-sources.md)（25 行） | `d24b51b430a8e307ef1ec23d9206a3aa659cb3ef63932bf5e303820fcf19339c` | 一致 |
| [修订映射](batch-21-review-fixes.md)（T05-03 第三轮修订节 L209–215） | 取证开始时整文件前缀 `77183321ee1196d7`；成稿前整文件 `44ca7856d265fa8ac2d2fd45a5ce34cc4e699829d2b724318618c52004716190`；L209–215 段 `5b3325167eaaf7331c848b34654a12f46a4a6ae4008dc9409a371df290b52a45` | 开始时一致；变化原因见下 |
| [来源登记](../../sources/registry.yaml)（`make check` 计 438 项；T05-03 段 L5386–5418） | `61388eb10023ff425ab83891604529b05764afbe19b478257feb62a19c1262f7`；L5386–5418 段 `c4daef07234fb152d58fceb6a98c9e028844883785d2b4ab8472b128dd0d3e62` | 一致；段哈希与前次 `56e8e74a…` 不同，系作者本轮修订（L5409 标题）所致 |
| [前次复核报告](batch-22-t05-03-claude-recheck-2.md)（剩余关闭条件权威来源） | `fbbcb3edf65a0a623116c7909ace7c11a7eeb3eeed1ce139412a437327f2a01b` | 任务未给前缀，记实值 |
| [初审报告](batch-22-t05-03-claude-review.md) | `a0830797ada7f12ae810689736c9d0ac150d1a1b045dcf50b415cbb72f21f9c6` | 任务未给前缀；与前两次复核所记相同 |
| [任务计划](../../plans/full-coverage-backlog.yaml)（T05-03 L5468–5509，acceptance L5487–5492） | `5f9bcf865b8c77e13cc8ee5f1c03140c37b86f558d8227d8bb2080249f4fcfc3` | 任务未给前缀；与初审及前两次复核所记相同，计划未变 |

修订映射在取证期间被改动，情况如下：

- 取证开始时整文件前缀为 `77183321ee1196d7`，与任务给定值一致。
- 取证期间（文件 mtime 10:49:13）并行的 T05-01 会话在文末追加了 L217–222"T05-01 第十一轮修订"节，整文件哈希因此变为 `44ca7856…`。
- T05-03 第三轮修订节 L209–215 的文字与取证开始时读到的逐行相同。开始时未单独取该段哈希，上表段哈希为成稿前值。

其余六个输入在取证开始和成稿前各哈希一次，结果相同。

## 取证方法与限制

- 方法：全部用 `curl -sSL` 默认 TLS 校验只读获取。原文放在新建临时目录 `/tmp/b22rec03e/`（取证前不存在），未入库。HTML 去标签后按文字核对，不只判可达性。
- 归档页：20 页 HTTP 均为 200，SHA-256 前 8 位与初审及前两次复核逐一相同（overview `87e97389`、job_state_codes `8a023811`、job_reason_codes `f8e4f3c9`、squeue `48e57603`、sinfo `b67afb79`、scontrol `da776891`、sbatch `132d28b4`、scancel `956cfa77`、priority_multifactor `acd6dead`、qos `f6b74df2`、reservations `ef527511`、prolog_epilog `6d83380c`、slurm.conf `f4151769`、sacct `d96f8299`、gres `4c7a5874`、gres.conf `21aeb902`、tres `2d08f826`、cgroups `49f81235`、cgroup.conf `8835c198`、resource_binding `47985fe9`）。
- 版本锚：`git ls-remote` 显示 `refs/tags/slurm-24-11-7-1` 为 tag 对象 `9d1ef1877186d8101769352831c8f0fe303df31c`，`^{}` 为 commit `defaf214db2e55326f45ab08f1bde5b2036d9f5d`，与前几轮及登记一致。
- testsuite：从 `raw.githubusercontent.com/SchedMD/slurm/slurm-24-11-7-1/testsuite/expect/` 重取 14 个文件，均为 HTTP 200。完整 SHA-256 与第一次复核所记逐一相同（如 test12.7 `4b457e86e143973aa8521e1ff049b12dbfa03c36d5ff88c0f0402b65b296a34f`、test31.2 `3fbfffea104abaac46bb4afbef33ce0a77ba815311f82e1d25c7ad1d92855ce5`）。
- 渲染核对：正文 L25 起的部分分别用 pandoc 2.12（`-f gfm`）和 markdown-it-py 4.0.0（commonmark＋table）渲染。两者一致：
  - 标题 15 个（h1 ×1、h2 ×5、h3 ×9），最长为"GRES / TRES / cgroup / 绑定"（25 字符）；"健康与节点状态职责"为独立 h3。
  - 表格 7 张、`tr` 69 个，等于源文件 76 个表格行减 7 个分隔行；69 行均为 4 列。
- `make check`：`PASS: 96 content entries; 438 sources.`，运行前后 `git status --porcelain` 相同。它只校验结构与本地链接，查不出 C21 那类单元格内的语义矛盾。`make build` 未运行，因为它会写 `build/`，超出"只写一份报告"的范围。
- 限制：
  - 测试文件只读了 test12.7 L1–6（头注释，目的句跨 L4–5）、L33–34（跳过条件）、L64 与 L77（`-D` 与 `--duplicates` 两种写法），以及 test31.2 L1–6、L120–127。断言未审计，tag 上的 CI 结果未查，所有测试都没有执行。
  - 未用 GitHub API，未枚举 `testsuite/expect` 目录。
  - gang_scheduling、heterogeneous_jobs、preempt、srun、sacctmgr、resource_limits 页本轮仍未取。
  - 正文、来源记录均未入 git（工作区 `??`），前一版正文无法取回。凡判断"本轮引入还是原本就有"处，依前次复核引述推断。
  - 作者是否用 webfetch 读过某页，审阅者无法核实，只能核对记录之间是否一致。
  - 未核对 SchedMD 站点许可与仓库根 LICENSE/DISCLAIMER。

### 关键抽查点（原文文字核对）

| 抽查点 | 原文 | 结果 |
|---|---|---|
| gres GPU Management 编号映射 | `Mapping between these two is nondeterministic and system dependent, and could vary between boots after hardware or OS changes. For the most part, this assignment seems fairly stable. However, an after-bootup check is required to guarantee that a GPU device is assigned to a specific device file.` | L133 两处反引号引文均为原文连续片段 → C16 |
| gres AutoDetect 校验失配 | `If the system-detected GPU differs from its matching GPU configuration, then the GPU is omitted from the node with an error.` | L133 `is omitted from the node with an error` 为连续片段 → C16 |
| gres `CUDA_DEVICE_ORDER` | `the CUDA_DEVICE_ORDER environmental variable must be set to CUDA_DEVICE_ORDER=PCI_BUS_ID` | L133 属实，未回退 |
| tres PriorityWeightTRES 节 | `A comma separated list of TRES Types and weights that sets the degree that each TRES Type contributes to the job's priority.` 示例后：`Applicable only if PriorityType=priority/multifactor and if AccountingStorageTRES is configured with each TRES Type. The default values are 0. The Billing TRES is not available for priority calculations because the number isn't generated until after the job has been allocated resources` | L135 第三列前句与此一致；同格后句"Billing 经 PriorityWeightTRES 才参与 priority"与此相反 → C21 |
| tres TRESBillingWeights 节 | `If TRESBillingWeights is not defined then the job is billed against the total number of allocated CPUs.`；`only used when calculating fairshare and doesn't affect job priority directly`；`If you want TRESs to play a role in the job's priority then refer to the PriorityWeightTRES option.` | L135 第二列"缺省=CPU 数，用于 fairshare"及所引原文属实 |
| squeue `-t, --states` | `Accepts a comma separated list of state names or "all". If "all" is specified then jobs of all states will be reported. If no state is specified then pending, running, and completing jobs are reported.` | L163 `-t all` 及注释属实 → C17 |
| squeue `%R` | `For terminated jobs with failure: an explanation as to why the job failed is printed within parenthesis.` | L163 属实 |
| slurm.conf `MinJobAge` | `The minimum age of a completed job before its record is cleared from the list of jobs slurmctld keeps in memory … The default value is 300 seconds. A value of zero prevents any job record purging. Jobs are not purged during a backfill cycle, so it can take longer than MinJobAge seconds to purge a job` | 默认值属实；"只在窗口内"为简化，见 C17 精度提示 |
| scontrol COMMANDS `completing` | `Display all jobs in a COMPLETING state along with associated nodes in either a COMPLETING or DOWN state.`；全页 `epilog` 出现 0 次 | L153 与 L168 一致 → C17 |
| sacct `-D, --duplicates` | 首句 `If Slurm job ids are reset, some job numbers will probably appear more than once …`；`--duplicates, in which case all records that match the selection criteria will be returned` | L165、L180 主体属实 |
| job_reason_codes `PartitionNodeLimit` / `Cleaning` | `The number of nodes required by this job is outside of its partition's current limits. Can also indicate that required nodes are DOWN or DRAINED.`；`Cleaning — The job is being requeued and still cleaning up from its previous execution.` | L72、L112 属实；L72/L73 仍重复，见 C21 非阻断 |
| prolog_epilog 重排范围 | `Only batch jobs can be requeued. Interactive jobs (salloc and srun) will be cancelled if the PrologSlurmctld fails.` | L102 新增 prolog_epilog 出处属实 |
| sinfo `-t, --states` | 可选值含 `COMP, COMPLETING, DOWN, DRAIN (for node in DRAINING or DRAINED states)` | 见 C17 非阻断 |
| test12.7 / test31.2 | test12.7 L3–5 `Validate that sacct -D shows correct job steps and states when a job is requeued`；L33–34 nosteps/nojobs 跳过；L64 `-D`、L77 `--duplicates`；test31.2 L122–125 接受 `launch_failed_requeued_held` 或 `JobHeldAdmin` | L143 引文与行区间属实 → C14 |

## 逐项判定

### B22-C14 — CLOSED（P2）

位置证据（前次三条剩余关闭条件，逐条）：

1. **自相矛盾的原句已改。** 正文 L143 已无"只读头注释"。现为"用例头注释目的（test12.7 `Validate that sacct -D shows correct job steps and states when a job is requeued` 等）为审阅者取证，作者侧未独立打开用例文件；test12.7 约 L60–120、test31.2 L122–125 行区间同样为审阅者已核对范围（含代码）；未审计断言，未查 CI，未运行"。与来源记录 L16、登记 L5413 不再矛盾。引文与 test12.7 L4–5 逐字一致。
2. **头注释目的的取证归属已写明并同步。**
   - 来源记录 L3：`用例头注释目的与行区间为审阅者取证（作者侧未独立打开用例文件）`。
   - 来源记录 L5：`testsuite 仅用例编号存在性（作者侧），头注释目的与行区间为审阅者取证`。
   - 正文 L23 `verification.notes` 保留"testsuite 用例存在性"，只陈述作者侧取证，与上两处一致。
   - 正文 L143（见上）；L179：`上文用例编号的存在性；头注释目的为审阅者取证`。
   - 登记 L5409 标题：`回归用例编号与头注释目的（头注释为审阅者取证）`；L5413、L5418 在该标题下引用头注释目的。
   - 正文 L108"转 held 见 test31.2 上游行为样本"、L165"见 test12.7 头注释目的"两处引用，其归属由 L143 统一交代。
3. **页数与清单已补。** 来源记录 L3"二十页，含 sacct"；正文 L23"二十页"、L91"所取 20 页"，三处一致。"来源与更新范围"新增 L180 sacct 条目（`-D, --duplicates` 节）。

修订映射 L211 与实际落盘一致。

追记（非阻断；本轮修订引入，起因含前次关闭条件措辞）：

- 来源记录 L3 写"作者取证轮次：首轮（Slurm 24.11.7 归档文档二十页，含 sacct）"。这与初审记录的首轮状态不符。初审输入为正文 `bfe7d6b8…` 与来源记录 `153d735a…`，当时列出 19 页、不含 sacct；sacct 页为审阅者补取（初审 L58、L121），作者在首轮修订中才加入。
- 前次关闭条件只写"页数改为二十页（含 sacct）"，没有写明 sacct 是哪一轮补入的，作者照改后就把 sacct 归到了首轮。
- 修法：L3 改为"首轮十九页；sacct 于首轮修订补入"，并写明作者是否独立打开过 sacct 页（方法与日期）。
  - 若作者确曾用 webfetch 读过 sacct，正文 L23"经 webfetch 只读核对……二十页"与登记 L5396"取证轮经 webfetch 只读核对：……sacct"成立，只需改 L3 的"首轮"。
  - 若未读过，sacct 应像 testsuite 头注释一样标为审阅者取证，并同步这三处。
- 审阅者无法核实作者的 webfetch 记录，因此不据此判定 L23/L5396 有误。

非阻断：

- L143 开头括注"（头注释目的为审阅者取证，见回归用例入口）"位于"回归用例入口"节内，指向本节自身，且与同段后文重复，可删。
- L23 页数已为"二十页"，但括号内的主题列举对应 19 页、未含 sacct，宜补"sacct"。
- 登记 L5413"用例精确到文件"清单无 test12.7（只出现在后面的行区间括注里），而 test12.7 是正文引用最多的用例，宜补入清单。
- 来源记录 L3"由只读取证角色完成"紧跟审阅者取证括注之后，读来像在说审阅者取证由该角色完成，宜调整语序。
- L165 注释仍未补 sacct `-D` 首句的限定（job ID 重置后同号可能指不同作业，按 submit 时间区分）。此项为第三次提出，仍非阻断。

### B22-C16 — CLOSED（P2）

位置证据（前次三条剩余关闭条件，逐条）：

1. **编号映射引文为原文连续片段，条件含义保留。** L133 为 `` `nondeterministic and system dependent, and could vary between boots after hardware or OS changes` ``，与 gres 页逐字一致，已无插入的 `(e.g. …)`；"硬件或 OS 变更后"恢复为限定条件。`an after-bootup check is required` 亦逐字一致。
2. **推论已标注。** L133 为"（编号不稳影响坏卡/分卡对账为本库推论，非原文）"。
3. **失配引文为原文连续片段。** L133 为"gres 页为 GPU `is omitted from the node with an error`"，与原文 `the GPU is omitted from the node with an error` 中的连续片段一致；两页口径并存的说法保留。

前几轮已满足的内容未回退：`CUDA_DEVICE_ORDER=PCI_BUS_ID`、环境变量作用范围、多于配置也 drain、MIG 条件、TRES 记账前提。修订映射 L212 与实际落盘一致。

非阻断：

- "原文要求 `an after-bootup check is required`"可补原文目的 `to guarantee that a GPU device is assigned to a specific device file`。
- 原文 `For the most part, this assignment seems fairly stable` 仍未写入（前次仅作提示）。

### B22-C17 — CLOSED（P2）

位置证据（前次两条剩余关闭条件，逐条）：

1. **L150 已同步。** 原 L150 现为 L153"清理：sinfo COMPLETING/`scontrol completing`（正在清理的作业及其 COMPLETING/DOWN 关联节点）"，与 scontrol COMMANDS 节 `completing` 条目一致，也与代码块 L168 一致。正文与来源记录全文检索"scontrol epilog"为 0 处，"epilog 状态"只剩 L168"无 scontrol 出处，不写"的声明。
2. **失败组已能看到已终止作业。** L163 为 `# squeue -t all -o "%i %T %R"`，注释写明"不带 -t 时默认只列 pending/running/completing，已终止作业须 -t all，且只在 MinJobAge 窗口内（文档默认 300 s，站点实际 unknown）可见，超出后用 sacct"。与 squeue `-t` 原文和 slurm.conf `MinJobAge` 默认值一致。

修订映射 L213 与实际落盘一致。

精度提示（非阻断；源于前次关闭条件措辞）：

- 前次关闭条件写"squeue 只在 `MinJobAge` 窗口内显示已结束作业"，作者照此落盘。按 slurm.conf 原文，`MinJobAge` 是清除前的**最短**保留时间：0 表示不清除，backfill 周期内可能保留更久。
- "只在窗口内可见"读来像上限，宜改为"至少保留 MinJobAge 秒（文档默认 300 s；0 不清除；backfill 期间可更久；站点实际 unknown），清除后用 sacct"。

非阻断（前次已提，仍未处理或部分处理）：

- L153 写"sinfo COMPLETING"，代码块清理组只有 `sinfo -R -t drain,down`，不含 COMPLETING；sinfo `-t` 可选值含 `COMPLETING`。
- L161、L163 两条 squeue 以 `# ` 注释掉，其余命令未注释，未说明原因。
- L112 条件列"前者终态为重排"：重排不是终态（REQUEUED 为 flag）；Cleaning 是 reason，COMPLETING 是状态 flag，属不同维度。
- 提交组 L160–161 注释写"参数与实分数"，但输出格式不含节点数，可补 `%D`。
- L168 注释漏了"及 COMPLETING/DOWN 关联节点"。L153 已写全，此项影响很小。

### B22-C21 — OPEN（P3）：正确说法已加入第三列，错句仍未删除

已满足：

- L135 第三列开头加入"要让 TRES 影响 priority，用 PriorityWeightTRES 按 TRES 类型（CPU/Mem/GRES 等）加权，Billing 不在其列"。与 tres 页 PriorityWeightTRES 节 `sets the degree that each TRES Type contributes to the job's priority` 及其后 `The Billing TRES is not available for priority calculations` 一致。证据列为 tres 页。
- 第二列引原文 `The Billing TRES is not available for priority calculations`，"缺省=CPU 数，用于 fairshare"属实。

未满足：**前次剩余关闭条件的前半句"删去 L132 第三列'Billing 经 PriorityWeightTRES 才参与 priority'"未做。**

- pandoc GFM 与 markdown-it 渲染后，L135 第三列整格文字为："要让 TRES 影响 priority，用 PriorityWeightTRES 按 TRES 类型（CPU/Mem/GRES 等）加权，Billing 不在其列；GRES 须写入 AccountingStorageTRES 才被记账（……）；gres/gpu 同时置 gres/gpumem 与 gres/gpuutil；**Billing 经 PriorityWeightTRES 才参与 priority**；权重站点配置"。
- 同一格前句说 Billing 不在 PriorityWeightTRES 之列，后句说 Billing 经 PriorityWeightTRES 才参与 priority，两句直接矛盾。后句与 tres 页 PriorityWeightTRES 节原文相反。这是该错句连续第三轮出现。

修订映射 L214 写"L132 第三列改 PriorityWeightTRES 按类型加权"，实际是新增而非改写，原句仍在。

剩余关闭条件：删去 L135 第三列"Billing 经 PriorityWeightTRES 才参与 priority；"一句。删除后在正文、来源记录、登记中全文检索"Billing"，确认没有其他位置写 Billing 参与 priority。本轮检索结果：正文只有 L135 一处，来源记录与登记无此说法。

非阻断（前次已提，本轮部分处理）：

- PartitionNodeLimit 重复：L71 已不再把它归入"账户或 QOS 组限额"。但本轮新增的 L72 单独行与 L73 合并行仍都列 PartitionNodeLimit，两处都释为"分区节点上限"，重复只是移了位置。宜从 L73 删去。修订映射 L214"L71/L72 去重"与此不符。
- L102 证据列已为"同上＋prolog_epilog"，原文核对属实（见抽查表）。已处理。
- 来源记录 L13（交互式取消，prolog_epilog 页）、L15（五个检测值对应四家厂商＋off）已同步。登记 L5407"AutoDetect 仅见 NVIDIA/AMD/Intel/AWS 四类字符串"未改；映射 L214 只写"记录同步"，与此相符。
- 可选：L135 第三列可补 PriorityWeightTRES 的适用前提（`Applicable only if PriorityType=priority/multifactor and if AccountingStorageTRES is configured with each TRES Type. The default values are 0.`）。

## 范围外观察复查

前次范围外观察（正文原 L88 整段渲染为 h3）已修正：现 L89 为标题"### 健康与节点状态职责"，L91 为正文段落。两种渲染器的标题列表中没有超长标题（见方法节）。C13 不在本轮范围内，未重新判定；段落文字要素与前次所记一致。

非阻断：

- L91"恢复路径见节点动作表"、L113"（见节点动作表）"、来源记录 L23"见正文节点动作表"所指的都是 L87 段落，不是表。前次已提，未处理。

## acceptance 对照

| acceptance | 判定 | 未关闭项 |
|---|---|---|
| 1 固定 release/commit 与官方文档；守护进程、Job/Step、pending/running/completing/terminal、cancel/requeue 与资源清理 | 范围内满足：清理口径统一为有出处的 `scontrol completing`，Cleaning、节点 DOWN 分支保留 | — |
| 2 GRES/TRES、autodetect/binding、cgroup、健康/节点状态职责；一种 NVIDIA GPU 条件；NPU 无证据即 unknown | 未完全满足。成立：编号映射与失配引文为原文片段、推论已标、健康职责标题结构已修、NPU unknown 保留。剩余：TRES 行第三列 Billing 错句仍在，与同格前句及原文矛盾 | C21 |
| 3 Slurm 状态、等待原因、配额/优先级/预留、节点 DRAIN/DOWN/RESUME 与成组资源条件；不套用 K8s 同名术语 | 范围内满足（PartitionNodeLimit 重复为非阻断） | — |
| 4 来源支持的提交/失败/重排队/清理观察样板与最小验证设计；不提交作业、不推断设备可用即应用成功 | 满足：失败组 `-t all`＋`%R`、清理组 `scontrol completing`、重排组 `sacct -D`，testsuite 取证归属与页数清单已统一；只读与未执行声明保留 | — |

修订映射 L209–215 中，L211、L212、L213、L215 与实际落盘一致。L214 有三处描述多于落盘：第三列是新增而非改写，原错句仍在；L71/L72 去重只是把重复移到了 L72/L73；"记录同步"只覆盖来源记录，未覆盖登记 L5407。

## 结论

**T05-03 第三次定向复核不通过。范围内 4 项：CLOSED 3（C14、C16、C17），OPEN 1（C21）。B22-C12–C21 累计 CLOSED 9，OPEN 1。** 未新增发现 ID。C14 追记一条（"首轮含 sacct"与初审记录不符，非阻断），C17 精度提示一条（`MinJobAge` 为最短保留时间，非阻断），两条都部分源于前次关闭条件的措辞。

- 阻断项只剩一处删除：L135 第三列删去"Billing 经 PriorityWeightTRES 才参与 priority；"。不需要新取证。
- 建议同轮一并处理的非阻断项（不影响本轮判定）：
  - 来源记录 L3"首轮"改写，并写明 sacct 由谁、何时读取。
  - L163 `MinJobAge` 改为"至少保留"口径。
  - L73 删去重复的 PartitionNodeLimit。
  - L143 删去自指括注；L23 括注补 sacct；登记 L5413 清单补 test12.7。
  - 三处"节点动作表"改称"节点动作段"。
- 修订后对 C21 做定向复核即可：核对 L135 渲染后的整格文字，并全文检索"Billing"。
- C21 关闭前，L135 TRES 行不宜视为已核对，正文 `verification.status: source_checked` 对该行不成立。
- 正文没有虚构命令输出或实测结果，NPU/Ascend 保留 unknown，范围声明与 `verification.notes` 写明未提交作业、未执行 Slurm 命令，这几点仍满足要求。
- 本复核只覆盖编辑与来源层面。文中的 Slurm 行为都是文档或测试源码层证据，不得标为 reproduced。
