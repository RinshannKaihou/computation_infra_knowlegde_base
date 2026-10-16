# 第二十二批 T05-03 定向复核（作者首轮修订后）

复核日期：2026-10-14（实际取证日）。

**结论：不通过。B22-C12–C21 共 10 项：CLOSED 5（C13、C15、C18、C19、C20），OPEN 5（C12、C14、C16、C17、C21）。** 未新增发现 ID。修订后新出现或本轮查实的问题按原 ID 追记：

- C12：节点状态表被插入的段落截断，L84–86 三行不再渲染为表格。
- C14：testsuite 取证口径在三处记录中互相矛盾。
- C16：GPU 编号映射引文截掉了条件句。
- C17："scontrol epilog 状态"在所取来源中无出处。
- C21："Billing 经 PriorityWeightTRES 才参与 priority"与 tres 页原文相反。

审阅者角色独立于作者修订角色。审阅模型为 `claude-opus-5-5`，由用户本次明确要求试用。这不是既有的 `gpt-6.1-sol / xhigh` 批量审阅约定，也不改写该约定。本会话内未见 `[frontier_llm]` 标记、认证失败或模型自报变化。推理等级、`modelUsage` 等运行元数据审阅者无法在会话内读取，不补造。若操作方在运行记录中发现模型不一致或认证问题，按约定本轮作废，不留档、不引用。

本轮只写本报告一个文件。未改作者正文、来源记录、登记、索引或计划；未部署 Slurm、未提交作业、未执行任何 Slurm 命令或测试用例。模型复核不构成平台或现场验证。

## 输入（以 SHA-256 识别）

| 输入 | SHA-256 | 与任务给定前缀 |
|---|---|---|
| [T05-03 正文](../../knowledge/05-cluster-platform/slurm-jobs-and-device-resources.md)（169 行） | `78292265123927f34a4412c6db0e03b758c6e69f217f99ab04c86558d64d37c2` | 一致 |
| [作者来源记录](batch-22-t05-03-sources.md)（25 行） | `b849cb038c68017c987ac028283d21c17a3788676afd0c6876679bdf13a96309` | 一致 |
| [修订映射](batch-21-review-fixes.md)（T05-03 首轮修订节 L180–191） | `4827cc5c02b2ddb6b72c136b60198221f1c12fe95b4dd02cdfb83e2c2e17a63e` | 一致 |
| [初审报告](batch-22-t05-03-claude-review.md)（269 行；关闭条件权威来源；L27 作者补注、L50 scontrol 改写注记） | `a0830797ada7f12ae810689736c9d0ac150d1a1b045dcf50b415cbb72f21f9c6` | 任务未给前缀，记实值 |
| [任务计划](../../plans/full-coverage-backlog.yaml)（T05-03 L5468–5508，acceptance L5487–5492） | `5f9bcf865b8c77e13cc8ee5f1c03140c37b86f558d8227d8bb2080249f4fcfc3` | 任务未给前缀；与初审所记完全相同，计划未变 |
| [来源登记](../../sources/registry.yaml)（`make check` 计 438 项；T05-03 段 L5386–5418） | `3a3d536d1773c8f706db4442984577b1ef54d5411ad4965bb09ab449594d0420`；L5386–5418 段 `b8a283968bd4c499a60b5c135b14bc55db113fa189778d98924e5dacb18b1da0` | 一致；段哈希与初审 `d0380c4f…` 不同，系作者修订所致 |

六个输入在取证开始和成稿前各哈希一次，结果相同。（作者补注：成稿后修订映射与来源登记被并行 T05-01 会话改动，整体哈希变为 `71af5e2a…`/`da4af1f7…`；T05-03 所用段——映射 T05-03 节、登记 L5386–5418 段 `b8a28396…`——未变，438 项不变，判定不受影响。）初审 L50 经作者机械修正后的 reboot 表述（nextstate 只列 RESUME 与 DOWN，UNDRAIN 为 ASAP 未指定时的默认）与本轮所取原文一致。

## 取证方法与限制

- 方法：全部用 `curl -sSL` 默认 TLS 校验只读获取，20 个归档页 HTTP 均为 200。HTML 去标签后按文字核对，不只判可达性。原文放在新建临时目录 `/tmp/b22rec03c/`（取证前不存在），未入库。
- **与初审逐字节比对**：20 页 SHA-256 与初审表逐一相同：overview `87e97389…`、job_state_codes `8a023811…`、job_reason_codes `f8e4f3c9…`、squeue `48e57603…`、sinfo `b67afb79…`、scontrol `da776891…`、sbatch `132d28b4…`、scancel `956cfa77…`、priority_multifactor `acd6dead…`、qos `f6b74df2…`、reservations `ef527511…`、prolog_epilog `6d83380c…`、slurm.conf `f4151769…`、sacct `d96f8299…`、gres `4c7a5874…`、gres.conf `21aeb902…`、tres `2d08f826…`、cgroups `49f81235…`、cgroup.conf `8835c198…`、resource_binding `47985fe9…`。初审所引原文在本轮仍适用。
- 版本锚：`git ls-remote` 显示 `refs/tags/slurm-24-11-7-1` 为 tag 对象 `9d1ef1877186d8101769352831c8f0fe303df31c`，`^{}` 为 commit `defaf214db2e55326f45ab08f1bde5b2036d9f5d`，与初审、登记一致。
- testsuite：从 `raw.githubusercontent.com/SchedMD/slurm/slurm-24-11-7-1/testsuite/expect/` 取 16 个文件。14 个 HTTP 200，`test31.1`、`test8.1` 为 404，与初审一致。初审只留了前后缀，作者补注称完整哈希无法补全，下表补记完整值（审阅者取证）：

  | 文件 | SHA-256 |
  |---|---|
  | test1.62 | `50c49c3a987f0a5ae737285ef98c886eba2054a0dd1873fe309c89415f46264f` |
  | test2.21 | `09e0adce6efcb81c5d040dfa8c75df08637be860f8ecb44dff73bd98dcde1db4` |
  | test2.22 | `e2f974a77fe22de9be89940781365a6cdd9753d46b7154905b8080a98b920b5c` |
  | test3.8 | `6f5d14c76ed06ad093ebf65731fb72d309d0b10da97bf342af060b2fc784444b` |
  | test3.11 | `d3db99998646120305819984a9c704f471d180972d6f846fe897b78ea923f919` |
  | test8.12 | `d8485b34a157c2fd7c1316faad14617ab34ca45234f138cbc0eee78bbee51354` |
  | test12.7 | `4b457e86e143973aa8521e1ff049b12dbfa03c36d5ff88c0f0402b65b296a34f` |
  | test24.1 | `b8a899ec45307446a82fa0d6872f2ff1d3a6bfcf088ed6c621d05ec388926cc5` |
  | test24.2 | `a34ed289bd38215cda8153f4f2ef40b8a64c9bd6fc7ac9c32b15ce3d984f938d` |
  | test31.2 | `3fbfffea104abaac46bb4afbef33ce0a77ba815311f82e1d25c7ad1d92855ce5` |
  | test31.3 | `521547ae2b13e11125f3891e4c7c4e28a46b9b72a249da7185c079fd8ee789d6` |
  | test39.1 | `585c72ec4694ba22d8cfc4723f8c9b4771890a5e3ecefce1ee12f9ec6e833f09` |
  | test39.2 | `169ddd877771861af75b4084021de6ee4b890c9d74b163aa52efc98fac7bcfbe` |
  | test40.1 | `4df49b788c621be16e9d8178affc15a21c56a20955a750ca4911776d7fe8e72d` |

  初审记录的 11 个前后缀与上表全部吻合。
- 渲染核对：把正文 L74–90 摘到临时目录，分别用 pandoc 2.12（`-f gfm`）和 markdown-it-py 4.0.0（commonmark＋table）渲染，结果见 C12。
- `make check`：`PASS: 96 content entries; 438 sources.`，运行前后 `git status` 相同。它只校验结构与本地链接，未发现 C12 的表格截断。`make build` 未运行，因为它会写 `build/`，超出"只写一份报告"的范围。
- 限制：
  - 测试只读头注释，另读 test12.7 L30–80（跳过条件与 sacct 调用）与 test31.2 L118–128；断言未审计，tag 上的 CI 结果未查，所有测试都没有执行。
  - 未用 GitHub API，未枚举 `testsuite/expect` 目录。
  - 初审限制中未取的 gang_scheduling、heterogeneous_jobs、preempt、srun、sacctmgr、resource_limits 页本轮仍未取；"多节点分配全有或全无"仍只在 20 页内检索。
  - 原正文（初审哈希 `bfe7d6b8…`）不在 git 中，本轮无法取回。C21 追记的句子是修订引入还是原本就有，只能依初审 C21 的引述推断。
  - 未核对 SchedMD 站点许可与仓库根 LICENSE/DISCLAIMER。

### 关键抽查点（原文文字核对）

| 抽查点 | 原文 | 结果 |
|---|---|---|
| scontrol NODES UPDATE `State=` | DOWN `Stop all running and suspended jobs and make the node unavailable for new jobs`；DRAIN `Existing jobs are allowed to run to completion, leaving the node in a DRAINED state`；RESUME `Not an actual node state, but will change a node state from DRAIN, DRAINING, DOWN or REBOOT to IDLE and NoResp`；UNDRAIN `will not change the node's base state (e.g. DOWN)`；`some of them are not valid new node states given their prior state`；`Reason=` 适用 DOWN/DRAINED/DRAINING/FAILING/FAIL | L83 属实 |
| scontrol reboot | `reboot [ASAP] [nextstate={RESUME\|DOWN}]`；`will set nextstate=UNDRAIN if nextstate isn't specified`；`By default, this command does not prevent additional jobs from being scheduled`；`A node will be marked "DOWN" if it doesn't reboot within ResumeTimeout`；重启后 `HealthCheckProgram will run once` 再注册 | L88、L103 属实 |
| sinfo 节点态 | `~` `presently in powered off`，`%` `presently being powered down`，`@` `pending reboot`，`^` `reboot was issued`；FAIL `expected to fail soon and is unavailable for use per system administrator request`；INVAL `a slurmd restart is required`；COMPLETING 在 job 进程全部终止且 epilog 结束后移除；PERFORMANCE `Do not run sinfo or other Slurm client commands … from loops` | L81、L84、L85、L107、L148 文字属实；L84–86 渲染见 C12 |
| slurm.conf | ReturnToService 默认 0，1 仅 non-responsive，2 任何原因，`memory, GRES, CPU count, etc. are equal to or greater than`；SlurmdTimeout 默认 300、0 由 `some other tool`；HealthCheckProgram root、非 NOT_RESPONDING、60 秒、slurmd 启动时先跑、默认不执行；UnkillableStepTimeout 超时 `the compute node will be drained`；MaxBatchRequeue 默认 5 → JobHeldAdmin；KillWait 30；JobRequeue 1 | L80、L88、L94、L98、L106 属实 |
| scancel ARGUMENTS／`--batch`／`--full` | `If neither --batch nor --signal are used, the entire job will be terminated`；`When --batch is not used but --signal is used, then all job steps will be signaled, but the batch script itself will not be signaled`；`The child processes of the shell will not be signaled by Slurm, but the shell may forward the signal`；`srun steps are also children of the batch step` | L94–96 属实 |
| sacct `-D, --duplicates` | `sacct returns the most recent job with that number … --duplicates … all records that match the selection criteria will be returned`；首句 `If Slurm job ids are reset, some job numbers will probably appear more than once … but refer to different jobs` | L159 属实；首句见 C14 非阻断建议 |
| gres GPU Management／AutoDetect | `the environment variable set for the sbatch command only reflects … node zero of the allocation`；`could vary between boots after hardware or OS changes. For the most part, this assignment seems fairly stable. However, an after-bootup check is required`；`If not all system-detected devices are specified by the slurm.conf configuration, then the relevant slurmd will be drained`；`GPU is omitted from the node with an error`；`The sanity-check AutoDetect mode is not supported for MIGs` | L128 主体属实；引文截断见 C16 |
| gres.conf `Cores`；sbatch `--tres-bind`／`--gpu-bind`／`--gres-flags` | 协同分配按 socket 粒度；未带 enforce-binding 时 `preferred`；超绑需 disable-binding；`By default, most tres are not bound to individual tasks`；`--gpu-bind` `Equivalent to --tres-bind=gres/gpu`；enforce-binding `may result in delayed initiation of a job` | L134 属实 |
| tres | `The Billing TRES is not available for priority calculations because the number isn't generated until after the job has been allocated resources`；TRESBillingWeights `only used when calculating fairshare and doesn't affect job priority directly`；带子类型须同时写通用类型；`Setting gres/gpu will also set gres/gpumem and gres/gpuutil` | L130 记账前提属实；Billing 与 priority 的说法相反 → C21 |
| cgroup.conf | ConstrainRAMSpace `killing one or more of the processes in the step`；`This differs from the behavior of OverMemoryKill, where the whole step` 被杀；CgroupPlugin 默认 autodetect；ConstrainDevices 默认 no | L132 属实 |
| job_reason_codes | `Cleaning — The job is being requeued and still cleaning up from its previous execution`；`JobHoldMaxRequeue — … MAX_BATCH_REQUEUE limit`；PartitionNodeLimit `Can also indicate that required nodes are DOWN or DRAINED`；终止类 reason | L71、L106、L109 属实；Cleaning 未展开 → C17 |
| prolog_epilog Failure Handling | Epilog→DRAIN；EpilogSlurmctld `will only be logged`；Prolog→DRAIN＋requeue＋held `unless nohold_on_prolog_fail`；PrologSlurmctld `Only batch jobs can be requeued. Interactive jobs (salloc and srun) will be cancelled`；task prolog→task canceled；srun prolog→step canceled | L99、L105 属实 |
| gang 与预留 | overview `gang scheduling (time sharing for parallel jobs)`；slurm.conf GANG `Enables gang scheduling (time slicing)`；reservations `a reservation can not be deleted while there are jobs running in it` | L28、L108、L118、L142 属实 |
| 成组资源与观察字段 | sbatch `-N`：`The partition's node limits supersede those of the job` / 超当前范围 `left in a PENDING state` / 超配置数 `rejected`；`SLURM_JOB_NUM_NODES`、`SLURM_RESTART_COUNT`；scancel 异构作业 PENDING 只能整体取消；squeue `%R` `For terminated jobs with failure` | L109、L119、L148 属实 |
| scontrol suspend | `you may want to use suspend/resume in the following way`；scancel 发 SIGSTOP/SIGCONT `would be a preferable mechanism in many cases`；`The time a job is suspended will not count against a job's time limit` | L102、L142 属实 |
| priority_multifactor 公式 | `site_factor +` 不乘权重；`- nice_factor` | L116 属实 |
| scontrol 全页"epilog" | 出现 0 次；另有只读命令 `completing`：`Display all jobs in a COMPLETING state along with associated nodes in either a COMPLETING or DOWN state` | L148"scontrol epilog 状态"无出处 → C17 |
| testsuite 头注释 | test1.62 `Test of gres/gpu plugin`；test2.21 `scontrol requeue of failed or completed job`；test2.22 requeuehold；test3.8 batch requeue；test3.11 reservations；test8.12 FLEX；test12.7 `Validate that sacct -D shows correct job steps and states when a job is requeued`；test24.1 multifactor；test24.2 sshare；test31.2 prolog 失败转 held；test31.3 Prolog/Epilog 环境变量；test39.1/39.2 sbatch/salloc `--gpu`；test40.1 invalid gres/mps | L138 用例描述全部属实；取证口径见 C14 |

## 逐项判定

### B22-C12 — OPEN（P1）：节点动作语义已补，但插入位置截断了节点状态表；L169 未同步

已满足：

- L83 的 DRAIN/DOWN/RESUME/UNDRAIN/FAIL/`Reason=`/`ResumeAfter=` 与 scontrol NODES UPDATE 节逐项一致。前态×新态合法组合收窄为 unknown，符合原文 `some of them are not valid new node states given their prior state`。
- L81 INVAL 行与 sinfo 原文一致，含"需 slurmd 重启"，并与 GRES 节互引。L80 补了 ReturnToService 0/1/2 与"有效配置含 GRES"，与 slurm.conf 原文一致。
- 来源记录 L23 已划去 unknown 第 4 条并收窄。

追记（本轮查实）：

1. **表格被截断**。L83 段落直接插在节点状态表的 INVAL 行（L81）与 FAIL 行（L84）之间。L84–86 因此失去表头与分隔行；pandoc GFM 与 markdown-it 两个渲染器都把这三行并入 L83 段落，显示为带 `|` 的原始文本。受影响的三行是 C21 改过的 FAIL/FAILING 释义、`~`/`@`/`^` 后缀行，以及分区 AVAIL 行。`make check` 未报出。
2. L169"待确认"仍列"节点 update State 全枚举"，与 L83 和来源记录 L23 的收窄矛盾。初审关闭条件第三项要求同时处理该处（初审编号 L158）。
3. 非阻断：L80"终止该节点上运行与挂起的作业"的证据列为 sinfo＋slurm.conf，但这句出自 scontrol（`Setting a node DOWN will cause all running and suspended jobs on that node to be terminated`），证据列宜补 scontrol。修订映射 L182 称"节点动作表"，正文实为段落。

剩余关闭条件：

- 把节点动作说明移到节点状态表之后，或改为独立表格并保留 scontrol 节名，使 L84–86 重新属于表格；用 GFM 渲染器核对这三行在表内。
- L169 删去"节点 update State 全枚举"，或改为"前态×新态合法组合（unknown）"。

### B22-C13 — CLOSED（P1）

位置证据：L88 写了 slurmctld 响应探测（SlurmdTimeout 默认 300 s，=0 时由其他工具监控）和注册校验（内存/GRES/CPU ≥ 配置）。HealthCheckProgram 写了 root 执行、只在非 NOT_RESPONDING 节点上跑、60 秒、默认不执行、HealthCheckInterval，以及由脚本自己 drain；还写了 slurmd 启动时先跑一次。另有 UnkillableStepTimeout→drain，reboot 后先跑 HealthCheckProgram 再注册，ResumeTimeout→DOWN。恢复路径指向节点动作说明。GPU 运行期健康（ECC/XID 类）与 NPU 都记为 unknown。以上逐项与 slurm.conf、scontrol reboot 节原文一致。登记 L5396 已把 slurm.conf 范围扩到 HealthCheckProgram、UnkillableStepTimeout、MaxBatchRequeue 等新引参数。

非阻断：

- 关闭条件写的是"表"，正文是一段文字。要素齐全，故判关闭。
- 注册校验失败对应的节点态（INVAL 或 DRAIN）L88 内没有写出，要靠 L81、L125 拼合。
- 来源记录 L14 仍写"slurm.conf.html 片段（ReturnToService/SlurmdTimeout）"，未与登记同步。
- L88 依赖的"节点动作表"就是 C12 中截断表格的那段文字，C12 修好后这里一并受益。

### B22-C14 — OPEN（P2）：`sacct -D` 已更正；testsuite 取证口径不一致

已满足：

- L159 注释改为 `--duplicates`：返回同一 job ID 的全部记录，与 sacct 页原文一致。注明需启用记账且记录未被关闭，与 test12.7 L33–37 的跳过条件（AccountingStorageEnforce 含 nosteps/nojobs 时跳过）一致。
- sacct 页并入 `src.slurm.docs-24.11.7`，登记 L5396 notes 写明 `sacct（-D=--duplicates）`。
- L138 引用 test12.7 头注释原句，与文件 L4–5 一致。

未满足：关闭条件要求与"未读代码"的说法一致。testsuite 读到了什么，现在有三种说法：

- **只有存在性**：来源记录 L5 写"testsuite 仅目录/用例编号存在性"，正文 frontmatter L23 写"testsuite 用例存在性"，登记标题 L5409 写"（存在性）"。
- **读了头注释**：来源记录 L16、正文 L138、登记 L5413/L5418 引用各文件头注释目的。这需要打开文件内容。
- **读了代码行段**：正文 L138 与登记 L5413 写"只读头注释（test12.7 约 L60–120、test31.2 L122–125）"。这两个行段是初审审阅者的阅读范围（初审 L70），且 test12.7 L60–120 是脚本代码，不是头注释，"只读头注释"与所列行段自相矛盾。

来源记录没有写作者本人读过这些文件。登记 L5417 已把 GPL 声明标为"审阅者旁证，未独立复核"，头注释目的与行段却没有同样的标注。

同类问题：frontmatter L23 仍写"归档十九页"，正文"来源与更新范围"L166 没有列 sacct，与登记已纳入 sacct 不一致。

剩余关闭条件：

- 统一 testsuite 的取证口径。若作者没有自行打开这些文件，就在正文、来源记录与登记中标明头注释目的与行段来自审阅者取证；若作者已自行读取，就在来源记录写明方法与日期，并同步改掉三处"存在性"表述。
- 删去或改写"只读头注释（test12.7 约 L60–120…）"这句自相矛盾的话。
- L23 页数与 L166 来源清单补上 sacct。

非阻断建议：sacct 页 `-D` 首句是 `If Slurm job ids are reset, some job numbers will probably appear more than once in the accounting log file but refer to different jobs. Such jobs can be distinguished by the "submit" time stamp`。样板写"同一 job ID 的全部记录"时，宜补"可能含 ID 重置后的其他作业，按 submit 时间区分"。

### B22-C15 — CLOSED（P2）

位置证据：L94–96 按 scancel ARGUMENTS 节分为四种情形，与原文逐句一致：

- 不带 `--signal`：终止整个 job。
- 只带 `--signal`：所有 steps 收到，batch shell 收不到。
- `--signal --batch`：只有 shell 收到，子进程靠 shell 转发。
- `--full`：shell、子进程与 srun steps 都收到。

SIGKILL 例外也已写入。

非阻断：登记 L5396 notes 在 scontrol 与 scancel 两项下都写了"信号四情形"。scontrol 页没有这项内容，应只留在 scancel 下。

### B22-C16 — OPEN（P2）：绑定与 NVIDIA 条件已补；编号映射引文截掉条件句

已满足：

- L134 GRES 绑定行与 sbatch、gres.conf 原文一致：`--tres-bind` 只支持 gres，默认多数 tres 不绑定到 task；`--gpu-bind` 等价；enforce-binding 可能推迟启动（附双 GPU 单 CPU 例）；Cores 按 socket 协同分配，未带 enforce-binding 时仅为优先，超出绑定核需 disable-binding。
- L128 补了环境变量作用范围、检测设备多于配置也会 drain、两页口径并存、MIG 不支持 sanity-check。
- L130 补了 GRES 记账前提：写入 AccountingStorageTRES，带子类型时同时写通用类型，`gres/gpu` 会连带设置 gpumem/gpuutil。
- NPU 继续保留 unknown。

追记（本轮查实）：L128 引文 `nondeterministic … could vary between boots` 被截断，随后正文断言"编号不稳直接影响坏卡/分卡对账"。gres 页原文为 `Mapping between these two is nondeterministic and system dependent, and could vary between boots after hardware or OS changes. For the most part, this assignment seems fairly stable. However, an after-bootup check is required to guarantee that a GPU device is assigned to a specific device file.`

- 截断去掉了条件 `after hardware or OS changes` 和 `fairly stable` 的限定，把有条件的变化写成了一般性的不稳定。
- 原文给出的可执行要求 `an after-bootup check is required` 没有写入正文。
- "影响对账"是初审 C16 明确标为审阅者推论的内容，正文没有标为本库推论。
- 初审证据栏本身用了带省略号的引文，截断部分源于初审。
- 另：L128 反引号内的 `omitted with an error` 不是原文连续片段（原文为 `is omitted from the node with an error`）。

剩余关闭条件：L128 按原文补全条件句和 `an after-bootup check is required`，并把"影响坏卡/分卡对账"标为本库推论；反引号内的引文改为原文连续片段，或去掉反引号改成转述。

### B22-C17 — OPEN（P2）：异常分支大部分已补；Cleaning、DOWN 分支缺失，一处观察字段无出处，代码块未分组

已满足：L105–109 新增以下分支，均与原文一致：

- 重排上限：MaxBatchRequeue 默认 5，之后标 JobHeldAdmin，reason 为 JobHoldMaxRequeue。
- Prolog 失败转 held，引 test31.2 作为上游行为样本。
- EpilogSlurmctld、TaskProlog、SrunProlog 失败的处置。
- 清理卡住：节点 COMPLETING 的移除条件，以及 UnkillableStepTimeout 超时 drain。
- 预留中有运行作业时不得删除该预留。
- 终止原因与 PENDING reason 分开读；`SLURM_RESTART_COUNT`。

L148 按提交、失败、重排队、清理四类列出预期字段，并加了 PERFORMANCE 提醒。

未满足：

1. **Cleaning** 是初审关闭条件明列的分支。正文仍只在 L72 译作"清理中"，没有写原文 `The job is being requeued and still cleaning up from its previous execution`，也没有放进重排/清理分支。
2. 节点 DOWN 终止作业只出现在节点表 L80 和 L83。取消/重排/清理表里没有这个分支，也没有与 C12 互引。
3. 追记：L148"清理：sinfo COMPLETING/scontrol epilog 状态"在所取来源中无出处，scontrol 页全文"epilog"出现 0 次。同页有只读命令 `scontrol completing`（`Display all jobs in a COMPLETING state along with associated nodes in either a COMPLETING or DOWN state`），可作为有出处的替代。
4. 代码块 L155–159 仍是五条未分组的命令。四类场景只出现在 L148 的文字里，失败场景要用的 `%R` 不在代码块中。修订映射 L184 写"样板按四场景分组"，与代码块不符。

剩余关闭条件：

- 补 Cleaning 分支，写出原文释义及其与重排的关系。
- 在分支表中加入节点 DOWN 终止作业，并与 C12 处的说明互引。
- 删去"scontrol epilog 状态"，或改为有出处的 `scontrol completing`。
- 代码块按四类场景分组，或逐条标注所属场景，并补上 `%R`。

初审要求的"先看字段 × 下一项检查"两列没有单列，多数行在条件列里已有对应内容（如清理卡住行）。本轮不单凭格式判 OPEN，但补 Cleaning 与 DOWN 分支时宜写出这两项。

### B22-C18 — CLOSED（P2）

位置证据：

- L28 范围声明与 L142 写明 Slurm 的 gang scheduling 指分时（PreemptMode=GANG 时间片＋分区 OverSubscribe），与 Volcano/Kueue 不同义。这与 overview `gang scheduling (time sharing for parallel jobs)`、slurm.conf `Enables gang scheduling (time slicing)` 一致。
- L118 改为"与 gang scheduler 插件不兼容（无法准确预测作业结束时间）"。
- L119 新增成组资源条件：`-N min[-max]`、分区上限优先、超出当前范围留 PENDING、超出配置数直接拒绝、`SLURM_JOB_NUM_NODES`、异构作业 PENDING 时只能整体取消、同 socket 约束。这些与 sbatch、scancel 原文一致。全有或全无语义记为 unknown。

非阻断：L142 写"见上表"，实际所指的是 L28 范围声明，不在表中。来源记录 L14 仍写未加限定的"与 gang 调度不兼容"。

### B22-C19 — CLOSED（P3）

位置证据：文档默认值与站点实际值已分开写。各文档默认值与原文一致：L94 KillWait 30 s、L98 JobRequeue 1、L106 MaxBatchRequeue 5、L80 ReturnToService 0、L88 SlurmdTimeout 300 s 与 HealthCheckProgram 默认不执行、L132 CgroupPlugin autodetect 与 ConstrainDevices no。站点实际值记为 unknown。L145"不可抄文档默认值当结论"保留，来源记录 L24 已同步。

### B22-C20 — CLOSED（P3）

位置证据：

- 版本锚：登记 L5413 记了 tag 对象 `9d1ef187` 与 commit `defaf214`；正文 L13、L138 与来源记录 L11 记了 commit。均与本轮 `git ls-remote` 一致。
- "页内只标 24.11，补丁级由归档路径确定"见正文 L13、来源记录 L11、登记 L5391。
- 用例已改为具体文件名加头注释目的（L138）。12 个文件的头注释本轮逐一核对属实，test24.2 为 sshare 已注明。
- 许可保持 unknown，notes 已改写，并标明 GPL 声明为审阅者旁证（L5417）。

非阻断：来源记录 L11 没有写 tag 对象；`src.slurm.gres-tres-cgroup-24.11.7` 的 revision（L5402）没有写补丁级的确定方式。testsuite 读取口径的问题归入 C14。

### B22-C21 — OPEN（P3）：措辞已逐条改正；L130 新增一句与原文相反

已满足（逐条对照原文）：

- 节点表：后缀 `~`/`%`/`@`/`^`（L85）、FAIL/FAILING（L84）。两行文字正确，但目前不在表格中渲染，见 C12。
- 取消/重排：reboot nextstate（L103）；suspend 只是建议、挂起时间不计时限（L102、L142）；交互 job 只在 PrologSlurmctld 失败时被取消（L99）。
- 等待原因：Resources 标为本库推论、"非资源性等待"（L68、L70）；PartitionNodeLimit 补 DOWN/DRAINED（L71）。
- 优先级与 cgroup：公式限定（L116）；ConstrainRAMSpace 与 OverMemoryKill 的区别（L132）。
- GRES 与 TRES：五个检测值对应四家厂商、NPU 指 Ascend（L13、L127）；TRESBillingWeights 用于 fairshare（L130）。
- 观察样板：PERFORMANCE 提醒（L148）。

追记（事实错误）：L130 条件列写"Billing 经 PriorityWeightTRES 才参与 priority"，与 tres 页原文相反：

- `The Billing TRES is not available for priority calculations because the number isn't generated until after the job has been allocated resources`。
- TRESBillingWeights 节：`is only used when calculating fairshare and doesn't affect job priority directly … If you want TRESs to play a role in the job's priority then refer to the PriorityWeightTRES option`。

PriorityWeightTRES 按 TRES 类型（CPU、Mem、GRES/gpu 等）加权，Billing 不参与 priority。初审 C21 引述原正文此处为"不直接参与 priority"，据此推断这句是修订时引入的；原正文不在库内，无法逐字确认。

剩余关闭条件：L130 改为"Billing 不参与 priority（分配资源后才生成）；要让 TRES 影响 priority，用 PriorityWeightTRES 按 TRES 类型加权"，并引 tres 页 PriorityWeightTRES 节。

非阻断：

- L71 把 PartitionNodeLimit 归入"账户或 QOS 组限额"，而原文释义是分区节点数上限；L72 又重复列了一次，宜只保留 L72 一处。
- L99 的"只有 batch job 可重排…PrologSlurmctld"出自 prolog_epilog 页，证据列仍为"同上"（即 sbatch）。
- 来源记录 L13 仍写"交互式 job 重排队语义以 scontrol 为准"，L15 仍写"AutoDetect 四类字符串"，与正文修正后的口径不一致。

## acceptance 对照

| acceptance | 判定 | 未关闭项 |
|---|---|---|
| 1 固定 release/commit 与官方文档；守护进程、Job/Step、pending/running/completing/terminal、cancel/requeue 与资源清理 | 未完全满足。成立：tag/commit/归档路径固定；守护进程、Job/Step、状态码有出处；scancel 四情形；重排上限与清理卡住。剩余：Cleaning 分支缺失；"scontrol epilog 状态"无出处 | C17 |
| 2 GRES/TRES、autodetect/binding、cgroup、健康/节点状态职责；一种 NVIDIA GPU 条件；NPU 无证据即 unknown | 未完全满足。成立：健康职责、GRES 绑定、NVIDIA 条件、TRES 记账前提、NPU unknown。剩余：编号映射引文截掉条件句；Billing/priority 说法与原文相反 | C16、C21 |
| 3 Slurm 状态、等待原因、配额/优先级/预留、节点 DRAIN/DOWN/RESUME 与成组资源条件；不套用 K8s 同名术语 | 内容已具备：节点动作语义、INVAL、成组资源条件、gang 辨义。剩余：节点状态表渲染被截断；L169 未同步 | C12 |
| 4 来源支持的提交/失败/重排队/清理观察样板与最小验证设计；不提交作业、不推断设备可用即应用成功 | 部分满足。成立：`sacct -D` 已更正；四类场景的字段有文字说明；只读与未执行声明清楚；"设备可见≠应用成功"保留。剩余：代码块未分组；清理字段无出处；testsuite 取证口径不一致 | C14、C17 |

修订映射 L182–184 写的是"节点动作表""健康职责表""样板按四场景分组"，正文实际是两段文字和一个未分组的代码块。映射宜按实际落盘内容描述。

## 结论

**T05-03 定向复核不通过。B22-C12–C21 共 10 项：CLOSED 5（C13、C15、C18、C19、C20），OPEN 5（C12、C14、C16、C17、C21）。** 未新增发现 ID。

- OPEN 项剩余工作量都不大：
  - C12：调整表格位置，处理 L169 一处"待确认"。
  - C14：统一 testsuite 取证口径，同步页数与来源清单。
  - C16：补全一句引文。
  - C17：补 Cleaning 与 DOWN 分支，改一处无出处字段，代码块分组。
  - C21：改正一句 Billing/priority。
- 修订后须对这五项做定向复核。C12 须用 GFM 渲染器核对，`make check` 查不出这类问题。
- 初审指出会推翻 `source_checked` 的两处（`sacct -D` 含义、scancel 信号方向）已改正。C21 追记的 Billing 句与原文相反，改正前 L130 该行不宜视为已核对。
- 正文没有虚构命令输出或实测结果，NPU/Ascend 保留 unknown，范围声明与 `verification.notes` 写明未提交作业、未执行 Slurm 命令，这几点仍满足要求。
- 本复核只覆盖编辑与来源层面。文中的 Slurm 行为都是文档或测试源码层证据，不得标为 reproduced。
