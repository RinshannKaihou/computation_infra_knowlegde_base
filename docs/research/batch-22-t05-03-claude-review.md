# 第二十二批 T05-03 初审

审阅日期：2026-10-14（实际取证日）。正文 `updated_at: "2026-10-14"` 与审阅日相同，但输入以下表 SHA-256 识别，不以日期推导。

**结论：T05-03 需修订。新增 10 项发现（B22-C12–C21）：P1 ×2、P2 ×5、P3 ×3，全部 OPEN。** 四条 acceptance 均只部分满足。

- acceptance 1：版本固定、守护进程与 Job/Step、作业状态码、cancel/requeue 的主体转述属实；`scancel` 的信号投递语义写反，清理卡住与重排上限分支缺失，tag 的 commit 未记录。
- acceptance 2：GRES 声明/请求、AutoDetect、cgroup、TRES 主体属实，NPU 如实保留 unknown；"健康"职责整体缺失，设备绑定只讲了 CPU，NVIDIA 条件缺编号映射等关键限制。
- acceptance 3：状态、原因、QOS/优先级/预留基本属实，K8s 术语对照有；节点 RESUME/DOWN 动作语义在已登记页面中可取，却被记为 unknown；"成组资源条件"未写，且 Slurm 自身的 "gang scheduling"（分时）与 K8s 同名术语未区分。
- acceptance 4：观察样板只读、未执行声明清楚、"设备可见≠应用成功"成立；`sacct -D` 的注释含义是虚构的，样板没有按提交/失败/重排队/清理分组。

正文没有虚构命令输出或实测结果，没有写成已验证的部署指南，NPU/Ascend 一律保留 unknown，这几点满足要求。`make check` 结果见文末；它只校验结构与本地链接，不说明技术正确性。

审阅者角色独立于作者。审阅模型为 `claude-opus-5-5`，由用户本次明确要求试用。这不是既有的 `gpt-6.1-sol / xhigh` 批量审阅约定，也不改写该约定。本轮未出现 `[frontier_llm]` 标记、模型不一致或认证失败；推理等级等运行元数据没有可核验记录，不补造。本轮只做审阅和只读取证：未改作者正文、来源记录、登记、索引或计划；未部署 Slurm、未提交作业、未执行任何 Slurm 命令或测试用例。模型审阅不构成平台或现场验证。

发现编号说明：[T05-02 初审](batch-22-t05-02-claude-review.md) 已占用 B22-C01–C11（审阅开始时在 `docs/research/` 中检索 `B22-C` 的最大号为 C11），本报告从 B22-C12 续号。

## 输入（以 SHA-256 识别）

| 输入 | SHA-256 |
|---|---|
| [T05-03 正文](../../knowledge/05-cluster-platform/slurm-jobs-and-device-resources.md)（158 行，reference / draft） | `bfe7d6b8216eb5b5116eda6135f2d0af6c31702b8710e1620238f85c6311c0f9` |
| [作者来源记录](batch-22-t05-03-sources.md)（25 行） | `153d735ad5fbda19677e7c1c0af4e719e85f84bd7b835f51aa058c756240a2e9` |
| [任务计划](../../plans/full-coverage-backlog.yaml)（T05-03 L5468–5507，acceptance L5487–5492，source_discovery L5498–5500） | `5f9bcf865b8c77e13cc8ee5f1c03140c37b86f558d8227d8bb2080249f4fcfc3` |
| [来源登记](../../sources/registry.yaml)（T05-03 新登记 L5386–5418：`src.slurm.docs-24.11.7`、`src.slurm.gres-tres-cgroup-24.11.7`、`src.slurm.testsuite-24-11-7-1`） | `7f64bf94474248b5edfed8ea671bb5950abd63e3721e39e7b6f749f2f559a9d4`；L5386–5418 段 `d0380c4f0c96af94591ef58a432b7b51b15c1bb42bac5121870307e03e6de54d` |

四个输入在审阅开始与成稿前各取一次哈希，结果一致。（作者补注：报告成稿后 `sources/registry.yaml` 被并行 T05-01 会话改动，整体哈希变为 `65ad00a…`；T05-03 相关段当时仍为 `d0380c4f…` 未变。测试文件完整哈希审阅者未留档在库内，作者侧无法补全，不虚构。`make check` 见审计。）

旁证（按本库现行草稿核对，未重新取其一次源）：正文 `related_ids` 的三个 ID（`cluster-platform.kubernetes-job-lifecycle`、`cluster-platform.device-resource-chain`、`cluster-platform.admission-and-placement`）都能解析到已有文件；`knowledge/05-cluster-platform/index.md` 的工作区 diff 新增本文导航条目，标"T05-03 草稿，待审阅"。

## 一次源取证（审阅者独立获取）

方法：全部用 `curl -sSL` 默认 TLS 校验只读获取，HTTP 均为 200（例外见下）。HTML 去标签后按文字核对，不只判可达性。版本锚用 `git ls-remote`。原文只放在临时目录 `/tmp/b22rev03c/`，未入库。

作者来源记录 L5 写明用 `webfetch` 读取、curl 字节级取回未执行。本表哈希是本审阅的取证，不能写成作者取证。

版本锚：

- `refs/tags/slurm-24-11-7-1` 为 tag 对象 `9d1ef1877186d8101769352831c8f0fe303df31c`，`^{}` 指向 commit `defaf214db2e55326f45ab08f1bde5b2036d9f5d`。
- 所取 20 个归档页的页头均为 `Version 24.11`，页内不出现 `24.11.7`；man 页由 man2html 生成，时间戳 `November 11, 2025`。补丁级版本只由 URL 路径 `archive/slurm-24.11.7/` 确定。
- 主站 `https://slurm.schedmd.com/overview.html` 页头为 `Version 26.05`，与正文 L28"主站当时已为 26.05"一致。

| 来源（登记 ID） | 位置 | SHA-256（原文） | 核对点与结果 |
|---|---|---|---|
| overview（src.slurm.docs-24.11.7） | [overview](https://slurm.schedmd.com/archive/slurm-24.11.7/overview.html) | `87e973899e508c139b62bff212990be9498b5ad9c99f5a6f6176662d92794094` | **属实**：slurmctld 与可选 backup；slurmd `waits for work, executes that work, returns status, and waits for more work`、`fault-tolerant hierarchical communications`；可选 slurmdbd 多集群记账库、可选 slurmrestd；accounting storage `When used with SlurmDBD, it can also supply a limits based system`；node/partition/job/job step 定义、分区字段、step 在分配内排队。**正文未用**：功能列表 `gang scheduling (time sharing for parallel jobs)`；分区 `over-subscription level for gang scheduling`。→ C18 |
| job_state_codes（同上） | [job_state_codes](https://slurm.schedmd.com/archive/slurm-24.11.7/job_state_codes.html) | `8a023811fa5a598045115b08e3285b4be5ecff290c8bfddf627f76b5ff21fa8f` | **全部属实**：13 个 base state 与 flag 释义；`If a recognized flag is present, it will be reported instead of the base state`；PREEMPTED 随 PreemptMode 转移；COMPLETING `performing cleanup tasks, including the epilog script`。正文以"等"省略 RECONFIG_FAIL、REQUEUE_FED、RESIZING、REVOKED、UPDATE_DB，可接受 |
| job_reason_codes（同上） | [job_reason_codes](https://slurm.schedmd.com/archive/slurm-24.11.7/job_reason_codes.html) | `f8e4f3c93113f0278d676d1177642b2e613223ca4f9905decf7e1b436281592a` | **属实**：`only the reason that was encountered by the attempted scheduling method will be displayed`；Resources/Priority/Dependency/BeginTime/Assoc*/QOS*/Max*PerAccount 等释义。**正文未用**：`JobHoldMaxRequeue`、`JobHeldAdmin`/`JobHeldUser`；`Cleaning — The job is being requeued and still cleaning up from its previous execution`；`PartitionNodeLimit … Can also indicate that required nodes are DOWN or DRAINED`；终止类 `NonZeroExitCode`/`OutOfMemory`/`TimeLimit`/`JobLaunchFailure`/`SystemFailure`。→ C17、C21 |
| squeue（同上） | [squeue](https://slurm.schedmd.com/archive/slurm-24.11.7/squeue.html) | `48e576039a8fb2904a08e911085c2f8e5b201924355f3adb757374e0903ba214` | **属实**：紧凑码 BF/CA/CD/CF/CG/DL/F/NF/OOM/PD/PR/R/RD/RF/RH/RQ/RS/RV/SI/SE/SO/ST/S/TO；`%t`/`%T`/`%r`/`%p`/`%Q`/`%q`/`%P`。**正文未用**：`%R` 对 `terminated jobs with failure` 显示失败说明。→ C17 |
| sinfo（同上） | [sinfo](https://slurm.schedmd.com/archive/slurm-24.11.7/sinfo.html) | `b67afb7958851970875457443f05457b8262a1b4840bcbdbf4accbb792398770` | **属实**：DRAINED/DRAINING/DOWN 释义；DOWN 指向 ReturnToService/SlurmdTimeout；`-R` 原因由管理员填写；`-t` 中 `DRAIN (for node in DRAINING or DRAINED states)`；AVAIL `up, down, drain, or inact`。**与正文不符**：`~` 为 `presently in powered off`（`%` 才是 powering down）；FAIL 为 `expected to fail soon and is unavailable for use per system administrator request`。**正文未用**：`INVAL`（注册资源少于配置，需 slurmd 重启后有效注册）、节点级 `COMPLETING`/`ALLOCATED+`、`@`/`^`/`REBOOT_*`；PERFORMANCE 节 `Do not run sinfo or other Slurm client commands that send remote procedure calls to slurmctld from loops`。→ C12、C17、C21 |
| scontrol（同上） | [scontrol](https://slurm.schedmd.com/archive/slurm-24.11.7/scontrol.html) | `da776891b3e6070f6e576c5b0f7bcbd62465e976919a1dd62b296050aa4e6d97` | **属实**：requeue/requeuehold（priority zero）、Incomplete 限 CONFIGURING/RUNNING/STOPPED/SUSPENDED、State=SpecialExit；suspend 释放 CPU、resume 可能同 CPU、权限限协调员以上。**与正文不符或正文未用**：reboot 语法为 nextstate 只列 RESUME 与 DOWN 两值（报告初稿此处系审阅者改写，非原文逐字；作者按审阅者要求机械修正），UNDRAIN 只是 ASAP 未指定 nextstate 时的默认；`A node will be marked "DOWN" if it doesn't reboot within ResumeTimeout`；suspend 的"先 drain/关分区"是维护场景建议；`If a suspended job is requeued, it will be placed in a held state`；**节点 update `State=`**：DOWN `Stop all running and suspended jobs`、DRAIN、FAIL、RESUME `Not an actual node state`、UNDRAIN `will not change the node's base state`、`Reason=`、`ResumeAfter=`。→ C12、C13、C17、C21 |
| sbatch（同上） | [sbatch](https://slurm.schedmd.com/archive/slurm-24.11.7/sbatch.html) | `132d28b42e5cb4f9124734b339a9093707d46e30f0b412d2ec12d11f4a10a00f` | **属实**：`--requeue` 脚本从头执行、同 job ID；`--no-requeue` 与 `ForceRequeueOnFail` 覆盖；JobRequeue 决定默认。**正文未用**：`--tres-bind`（`By default, most tres are not bound to individual tasks`）、`--gpu-bind` 等价写法、`--gres-flags=enforce-binding`（`may result in delayed initiation`）、`-N min[-max]` 与分区上限、`SLURM_RESTART_COUNT`。→ C16、C17、C18 |
| scancel（同上） | [scancel](https://slurm.schedmd.com/archive/slurm-24.11.7/scancel.html) | `956cfa7716af5cfbdeb4eee24e888a0c129db55aa4adcc9b72b3e190da583f53` | **属实**：默认 SIGCONT→SIGTERM→KillWait→SIGKILL；`--signal=KILL` 只取消活动 step；取消 step 不释放分配；`--state` 三值。**与正文不符**：`When --batch is not used but --signal is used, then all job steps will be signaled, but the batch script itself will not be signaled`；`--full` 时 `srun steps are also children of the batch step`。→ C15 |
| priority_multifactor（同上） | [priority_multifactor](https://slurm.schedmd.com/archive/slurm-24.11.7/priority_multifactor.html) | `acd6dead998a88f63b06aa090571d29bd49f20449bcc9b811e5d69a63720f58d` | **全部属实**：评估序六项；九因子；因子 0.0–1.0、权重 32 位无符号、priority 0–4294967295。公式中 `site_factor` 不乘权重、`nice_factor` 为减项（见 C21） |
| qos（同上） | [qos](https://slurm.schedmd.com/archive/slurm-24.11.7/qos.html) | `f6b74df28881e89b2e056bd2f15c0059247f78a7dc979063b16f77b062e2ba5f` | **全部属实**：三作用；`PriorityWeightQOS` 须大于 0；`preempt/qos` 以 job QOS 而非分区 QOS 判定；QOS 限额优先于 association；分区 QOS 不给 priority/抢占、OverPartQOS 反转；Relative QOS `Starting in Slurm 23.11` |
| reservations（同上） | [reservations](https://slurm.schedmd.com/archive/slurm-24.11.7/reservations.html) | `ef52751124e893ee6de3eb69f8cb013952b9b02e33cd5fa402d856e66ab0e9a8` | **全部属实**：仅 root/SlurmUser；cores/nodes/licenses/burst buffers；节点/核预留单分区；`contained completely`、EndTime 后取消、ResvOverRun；不改 priority 但同分区先考虑；结束后 pending 去预留转 held、NO_HOLD_JOBS_AFTER_END；与 gang scheduler 插件不兼容。**正文未用**：`a reservation can not be deleted while there are jobs running in it`。→ C17、C18 |
| prolog_epilog（同上） | [prolog_epilog](https://slurm.schedmd.com/archive/slurm-24.11.7/prolog_epilog.html) | `6d83380c65d0dcd57a598b03aa9a046e4c1aae86975a873dc9175cd01731ceac` | **属实**：Prolog 首个 step 时运行、PrologFlags=Alloc；Epilog 释放时每节点运行；`should not call Slurm commands`；`CUDA_VISIBLE_DEVICES` 在 Prolog/Epilog 与 job 内可不同（cgroup 约束设备时）；Failure Handling 中 Epilog→DRAIN、Prolog→DRAIN＋重排＋默认 held、PrologSlurmctld→batch 重排/交互取消。**正文未用**：EpilogSlurmctld 失败只记日志；task prolog 失败取消 task；srun prolog 失败取消 step。→ C17 |
| slurm.conf（同上，正文称"片段"） | [slurm.conf](https://slurm.schedmd.com/archive/slurm-24.11.7/slurm.conf.html) | `f4151769ed29968c7de408809a5acb8f0591865cd525d5f2c70925e847a1ff34` | **属实**：ReturnToService 0/1；SlurmdTimeout 默认 300 s、0 表示由其他工具监控。**正文未用**：ReturnToService 默认 0 与值 2、"有效配置"含 GRES；KillWait 默认 30 s；JobRequeue 默认 1；MaxBatchRequeue 默认 5（达到后 JobHeldAdmin）；HealthCheckProgram；UnkillableStepTimeout（超时 drain 节点）；PreemptMode `GANG … (time slicing)`；TRESBillingWeights 未定义时按 CPU 计费。→ C12、C13、C17、C18、C19 |
| sacct（未登记，审阅者补取） | [sacct](https://slurm.schedmd.com/archive/slurm-24.11.7/sacct.html) | `d96f8299e0b778c8d4cd04a710969f458f118482b122bb99443716ca9ab677f4` | `-D, --duplicates`：默认 `--jobs` 只返回该号最近一条，`--duplicates` 返回全部匹配记录。与正文 L148"-D 显示 daemon 相关条目"不符。→ C14 |
| gres（src.slurm.gres-tres-cgroup-24.11.7） | [gres](https://slurm.schedmd.com/archive/slurm-24.11.7/gres.html) | `4c7a58746e36f07ac7bf43cde934a7342b16698068ceb61ee83debc1c6eccff9` | **属实**：默认无 GRES、GresTypes/Gres；资源少于配置置 DRAIN；`--gpus*` 等限 select/cons_tres；AutoDetect 五个检测值，nvidia 为 24.11 新增、不需 nvml、不检 MIG/NVLink；Type 为检测名子串、空格转下划线、`slurmd -C`/`slurmd -G`；每 step 设 `CUDA_VISIBLE_DEVICES`；MIG 用 nvml、按 MIG Profile 子串、`does not support dynamic MIG partitioning`。**正文未用**：检测到的设备多于配置时 slurmd 也被 drain；校验失配 GPU `is omitted from the node with an error`；sbatch 环境变量只反映 node zero；NVML 编号与 `/dev` minor 号映射 `nondeterministic … could vary between boots`、需 `CUDA_DEVICE_ORDER=PCI_BUS_ID`；`The sanity-check AutoDetect mode is not supported for MIGs`。→ C13、C16 |
| gres.conf（同上） | [gres.conf](https://slurm.schedmd.com/archive/slurm-24.11.7/gres.conf.html) | `21aeb902c64844020cca02fe761eb53a8daec7699020d79c7f36d113f47e294e` | **属实**：`nrt` 为 `AWS Trainium/Inferentia`；AutoDetect 时 File/Cores/Links 作 sanity check，失配 `node's state is set to invalid and the node is drained`；Cores 为逻辑核号（`Core L#`）；File/MultipleFiles 互斥；Flags。**正文未用**：Cores 的协同分配按 socket 粒度，未带 enforce-binding 时仅为 preferred；`Drain a node before changing the count of records with File`。→ C16 |
| tres（同上） | [tres](https://slurm.schedmd.com/archive/slurm-24.11.7/tres.html) | `2d08f826f585d5f0c663b80406352af8565c6c84c6e675de8e6fd177508691b2` | **属实**：TRES 类型清单；默认跟踪集不可关只能追加；Billing 由 TRESBillingWeights 计算；不直接参与 priority。**正文未用**：GRES 须写入 `AccountingStorageTRES` 才被记账，带子类型时建议同时写通用类型；`Setting gres/gpu will also set gres/gpumem and gres/gpuutil`；TRESBillingWeights 用于 fairshare。→ C16、C21 |
| cgroups（同上） | [cgroups](https://slurm.schedmd.com/archive/slurm-24.11.7/cgroups.html) | `49f81235373b262807f863b20a069a893c36c9b63de350c93b20981200ebfc3d` | **全部属实**：v1/v2、hybrid 不支持；三插件职责；task/cgroup `the only plugin that can ensure that the boundaries of an allocation are not violated`，含 GRES/GPU；v2 top-down、no-internal-process、systemd Delegate 约束 |
| cgroup.conf（同上） | [cgroup.conf](https://slurm.schedmd.com/archive/slurm-24.11.7/cgroup.conf.html) | `8835c19854a487fad4e8485cd30ffb0dc86c0bc49f87070717c20d36cafeca32` | **属实**：CgroupPlugin 四值、默认 autodetect；ConstrainDevices 基于 GRES、默认 no；ConstrainRAMSpace OOM 时 step 标 OOM 并继续运行。措辞差异：原文为 `killing one or more of the processes in the step`（见 C21） |
| resource_binding（同上） | [resource_binding](https://slurm.schedmd.com/archive/slurm-24.11.7/resource_binding.html) | `47985fe91aab1343b87e667304b965ff744221df60867f5c7c10d1fd7fab1749` | **全部属实**：CPU bind 生效序四级，节点 CpuBind 仅在全分配节点一致时使用 |
| testsuite（src.slurm.testsuite-24-11-7-1） | [testsuite/expect@slurm-24-11-7-1](https://github.com/SchedMD/slurm/tree/slurm-24-11-7-1/testsuite/expect) | test1.62 `50c49c3a…264f`；test2.21 `09e0adce…1db4`；test2.22 `e2f974a7…b5c`；test3.8 `6f5d14c7…444b`；test3.11 `d3db9999…f923f919`；test12.7 `4b457e86…a34f`；test39.1 `585c72ec…3f09`；test40.1 `4df49b78…e72d`；test31.2 `3fbfffea…5ce5`；test24.1 `b8a899ec…cc5`；test8.12 `d8485b34…bee51354`（均为前 8 位…后 4–8 位） | 用 raw.githubusercontent.com 逐文件取回并读头注释 `Purpose`。**属实**：test1.62 `Test of gres/gpu plugin`；test2.21 `scontrol requeue of failed or completed job`；test2.22 `scontrol requeuehold`；test3.8 `batch job requeue`；test3.11 reservations create/delete/update；test39.1/39.2 sbatch/salloc `--gpu` 全集；test40.1 `invalid gres/mps job option`；test24.1 multifactor。**需注意**：`test31.1`、`test8.1` 返回 404；test31.2 为 `job is held and reason is set to launch failed requeued held when the prolog fails`（L122–125 接受 `launch_failed_requeued_held` 或 `JobHeldAdmin`）；test31.3 为 Prolog/Epilog 环境变量；test24.2 为 sshare；test8.12 为预留 FLEX 标志；test12.7 为 `Validate that sacct -D shows correct job steps and states when a job is requeued`，用 `--job=<id>.batch -D`，AccountingStorageEnforce 含 nosteps/nojobs 时跳过。→ C14、C17、C20 |

取证限制：

- GitHub 未认证 API 返回 403（rate limit），未能列出 `testsuite/expect` 完整目录，因此"8.x""test39""test40"等通配编号无法逐一核对，只核对了上表文件。
- 测试文件只读了头注释，另读 test12.7 约 L60–120、test31.2 L122–125；其余断言未审计，未确认 tag 上的 CI 结果。所有测试都没有执行。
- HTML 按去标签文字核对；man 页由 man2html 生成，未固定其源 commit 与归档页的对应关系。
- 未取 `gang_scheduling.html`、`heterogeneous_jobs.html`、`preempt.html`、`srun.html`、`sacctmgr.html`、`resource_limits.html`。C18 中"多节点分配全有或全无"的明文因此只在本轮 20 页内检索，未找到。
- 未核对 SchedMD 站点许可与仓库根 LICENSE/DISCLAIMER；只看到 man 页 COPYING 节与 testsuite 文件头中的 GPL v2 or later 声明。

## 发现

### B22-C12 — P1 / OPEN：节点 DRAIN/DOWN/RESUME 动作语义在已登记页面中可取，正文却记为 unknown；节点表缺 INVAL

位置：正文节点状态表 L76–83（特别是 L80）、L98、L134、L158"节点 update State 全枚举"；来源记录 unknown 第 4 条（L23）；登记 L5396（scontrol 已在范围内）；acceptance 3。

证据：

- scontrol 页 "NODES - SPECIFICATIONS FOR UPDATE COMMAND" 的 `State=<state>`：
  - `DOWN`：`Stop all running and suspended jobs and make the node unavailable for new jobs`；同节末 `Setting a node DOWN will cause all running and suspended jobs on that node to be terminated`。
  - `DRAIN`：`no new jobs may be started on this node. Existing jobs are allowed to run to completion, leaving the node in a DRAINED state`。
  - `RESUME`：`Not an actual node state, but will change a node state from DRAIN, DRAINING, DOWN or REBOOT to IDLE and NoResp`；随后 slurmctld 请求 slurmd 注册，注册后才去掉 NoResp。
  - `UNDRAIN`：`Clears the node from being drained (like RESUME), but will not change the node's base state (e.g. DOWN)`，且需要有效注册。
  - 另有 `FAIL`、`IDLE`、`NoResp`、`CANCEL_REBOOT`、`FUTURE`；`While all of the above states are valid, some of them are not valid new node states given their prior state`。`Reason=` 适用于 DOWN/DRAINED/DRAINING/FAILING/FAIL；`ResumeAfter=` 可定时恢复。
- 该页已在 `src.slurm.docs-24.11.7` 范围内，作者来源记录却把"节点 update State 全枚举"列为未取证。acceptance 3 明列 RESUME；正文只在 reboot `nextstate` 中出现 RESUME，没有解释 RESUME 本身。
- sinfo 页 NODE STATE CODES 有 `INVAL`：`did not register correctly with the controller. This happens when a node registers with less resources than configured in the slurm.conf file. The node will clear from this state with a valid registration (i.e. a slurmd restart is required)`。正文 L119 写了 gres.conf 失配 → invalid+drain，节点表却没有 INVAL，前后没接上。
- slurm.conf 页 ReturnToService：默认 0；值 2 为任何原因的 DOWN 在有效配置注册后都自动恢复；`A node registers with a valid configuration if its memory, GRES, CPU count, etc. are equal to or greater than the values configured in slurm.conf`。正文 L80 只列 0 和 1，也没写"有效配置"包含 GRES 数量。
- 审阅者提示（非原文结论）：DOWN 会终止节点上运行与挂起的作业，这是可靠性参考里最需要显式写出的副作用；正文目前只写"故障或管理员设置"。

关闭条件：

- 新增"节点状态动作"小表：DRAIN→DRAINING→DRAINED、DOWN（终止运行与挂起作业）、RESUME（不是状态；DRAIN/DRAINING/DOWN/REBOOT→IDLE+NoResp，需重新注册）、UNDRAIN（只清 drain，不改 base state）、FAIL、`Reason=`/`ResumeAfter=`，逐行引 scontrol 节名。措辞保持"字段与语义参考"，不写成操作步骤。
- 节点表补 INVAL（含"需 slurmd 重启后有效注册"），并与 L119 的 GRES 失配互引；L80 补 ReturnToService 默认 0、值 2，以及"有效配置含 GRES"。
- 删去来源记录 unknown 第 4 条与 L158 对应项，或收窄为真实未知项："前态 × 新态的合法组合（文档称部分组合无效但未列出）"。

### B22-C13 — P1 / OPEN：acceptance 2 的"健康"职责整体缺失

位置：acceptance 2"健康/节点状态的职责"；正文 L78、L80、L115、L121–122；全文没有 HealthCheckProgram、SlurmdTimeout 的探测职责或 UnkillableStepTimeout。

证据：

- slurm.conf 页 HealthCheckProgram：`execute as user root periodically on all compute nodes that are not in the NOT_RESPONDING state`；`may be used to verify the node is fully operational and DRAIN the node or send email if a problem is detected`；`Any action to be taken must be explicitly performed by the program`（示例为 `scontrol update NodeName=foo State=drain Reason=tmp_file_system_full`）；60 秒内未正常结束会被杀；`also be executed when the slurmd daemon is first started and before it registers`；默认不执行任何程序；间隔由 HealthCheckInterval 控制。
- scontrol 页 reboot：重启后 slurmd 启动时 HealthCheckProgram 运行一次，随后注册并清除 REBOOT 旗；`A node will be marked "DOWN" if it doesn't reboot within ResumeTimeout`。
- slurm.conf 页 SlurmdTimeout：slurmctld 等不到 slurmd 响应即置 DOWN，默认 300 s；值 0 时 `some other tool will take responsibility for monitoring`。sinfo 后缀 `*`：无响应、不再分配，持续无响应则转 DOWN（COMPLETING/DRAINED/DRAINING/FAIL/FAILING 除外）。
- 注册校验：ReturnToService 节的"有效配置"（内存、GRES、CPU ≥ 配置）；gres 页 `Nodes which are found to have fewer resources than configured will be placed in a DRAIN state` 与 `If not all system-detected devices are specified by the slurm.conf configuration, then the relevant slurmd will be drained`；gres.conf 页 AutoDetect 校验失配 → invalid+drain。
- slurm.conf 页 UnkillableStepTimeout：SIGKILL 后进程仍未退出超过时限即执行 UnkillableStepProgram，`the compute node will be drained`。
- 据此可以写出职责划分：slurmctld 负责响应探测与注册校验；节点与设备的运行期健康由站点 HealthCheckProgram 判定，并由脚本自己执行 drain。本轮 20 页中没有看到 Slurm 自带的 GPU 运行期健康探测条目（如 ECC、XID），应记为 unknown，而不是不写。正文只写了"IDLE/MIXED/ALLOCATED 不证设备健康"和 GRES 不足置 DRAIN。

关闭条件：

- 新增"健康与节点状态职责"表：探测者（slurmctld ping 与 SlurmdTimeout、slurmd 注册校验、HealthCheckProgram、UnkillableStepTimeout）、触发条件、导致的节点态、恢复路径（ReturnToService/RESUME，见 C12），逐行引页面与参数名。
- 写明 GPU 运行期健康探测不在所取 Slurm 文档中（unknown），站点脚本的检查内容不可推定；NPU 同为 unknown。
- `src.slurm.docs-24.11.7` 的 notes 把 slurm.conf 取证范围从"ReturnToService/SlurmdTimeout 片段"扩到新引用的参数。

### B22-C14 — P2 / OPEN：观察样板中 `sacct -D` 的含义是虚构的；sacct 页未登记

位置：正文 L148 示例注释（`-D 显示 daemon 相关条目，按 test12.7 用法`）、L127"test12.7（sacct -D 看重排）"、L137、L151；来源记录 L16；登记 L5418。正文与来源记录列出的 19 页不含 sacct。

证据：

- 24.11.7 归档 sacct 页（审阅者补取）`-D, --duplicates`：`When data for specific jobs are requested with the --jobs option, sacct returns the most recent job with that number. This behavior can be overridden by specifying --duplicates, in which case all records that match the selection criteria will be returned.` `-D` 指 duplicates，与 daemon 无关。
- test12.7 头注释：`Validate that sacct -D shows correct job steps and states when a job is requeued`；脚本用 `--job=<id>.batch -D`；`AccountingStorageEnforce` 含 nosteps 或 nojobs 时跳过，且须以 SlurmUser 运行。用 `-D` 看重排历史的方向成立，但注释给出的含义没有出处。来源记录说 testsuite"未读代码"，正文却引用其"用法"。
- sacct 依赖记账存储。正文 L42 写了 slurmdbd"未启用时限额/历史能力不存在"，观察样板却没有把这个前提写给 sacct。

关闭条件：L148 注释改为"`--duplicates`：返回同一 job ID 的全部记录（含重排前的运行）"；登记 sacct 页，或并入 `src.slurm.docs-24.11.7` 并在 notes 中写明 `-D` 节；样板注明 sacct 需要启用记账，且 job/step 记录未被关闭；test12.7 改为引用头注释所述目的，并与"未读代码"的说法一致。

### B22-C15 — P2 / OPEN：`scancel` 的信号投递语义写反

位置：正文 L91"`scancel --batch / --full` … 默认不管子进程"；L89–90；acceptance 1 的 cancel。

证据（scancel 页）：

- `-b, --batch`：`By default, signals other than SIGKILL are not sent to the batch step (the shell script). With this option scancel signals only the batch step, but not any other steps.`；`Children of the batch step are not signaled with this option`；大多数 shell 在子命令运行期间无法处理信号。
- `-f, --full`：同时向 batch 脚本及其子进程发信号；`srun steps are also children of the batch step, so steps are also signaled`。
- ARGUMENTS 节：`If neither --batch nor --signal are used, the entire job will be terminated.`；`When --batch is not used but --signal is used, then all job steps will be signaled, but the batch script itself will not be signaled.`
- 因此只带 `--signal` 时，收不到信号的是 batch shell，所有 step 都会收到。正文"默认不管子进程"方向相反，也没说明 `--batch`/`--full` 只在发信号时有意义。训练进程靠 SIGTERM/SIGUSR 触发保存时，这决定了信号能否到达实际计算进程。

关闭条件：按 ARGUMENTS 节重写 L91，分四种情形：不带 `--signal`（终止整个 job）；只带 `--signal`（所有 step 收到，batch shell 收不到）；`--signal --batch`（只 batch shell，子进程靠 shell 转发）；`--full`（shell、子进程与 step 都收到）。补上"SIGKILL 例外"。

### B22-C16 — P2 / OPEN：设备绑定只讲 CPU；NVIDIA GPU 条件例子缺关键限制

位置：正文 L115–123，特别是 L115、L118、L119、L120、L123；acceptance 2"设备 autodetect/binding""一种 NVIDIA GPU 条件以官方证据为例"。

证据：

- sbatch 页 `--tres-bind`：`Currently gres are the only supported tres for this options`；`By default, most tres are not bound to individual tasks`；绑定类型有 closest、map 等。`--gpu-bind` 等价于 `--tres-bind=gres/gpu:…`。
- sbatch 页 `--gres-flags=enforce-binding`：作业只能使用 gres.conf 中与所选 GRES 绑定的 CPU，`This option may result in delayed initiation of a job`（例：两 GPU 一 CPU 的作业会等到同一 socket 上两张卡都空闲）；`disable-binding` 取消该约束。
- gres.conf 页 `Cores`：GRES 与 CPU 的协同分配按 socket 粒度；未带 enforce-binding 时，列出的核只作为优先选择；需要超出绑定核的 CPU 时须用 disable-binding。正文 L119 只写了 Cores 是逻辑核号。
- gres 页 GPU Management：`CUDA_VISIBLE_DEVICES` 只在任务启动到某节点时设置；`the environment variable set for the sbatch command only reflects the GPUs allocated to that job on that node, node zero of the allocation`；NVML 按 PCI bus ID 编号，`/dev/nvidia*` 按 minor 号，`Mapping between these two is nondeterministic and system dependent, and could vary between boots … an after-bootup check is required`；须设 `CUDA_DEVICE_ORDER=PCI_BUS_ID` 才与 CUDA 编号一致。
- gres 页 AutoDetect：检测到的设备多于 slurm.conf 配置时 slurmd 也会被 drain（正文 L115 只写"不足"）。校验失配时，gres 页写 GPU `is omitted from the node with an error`，gres.conf 页写 `node's state is set to invalid and the node is drained`，两页说法不同，正文只取后者。另有 `The sanity-check AutoDetect mode is not supported for MIGs`。
- tres 页：GRES 不在默认跟踪集中，须写入 `AccountingStorageTRES`；带子类型时建议同时写通用类型，否则只请求 `gpu:1` 的作业不会被计入；`Setting gres/gpu will also set gres/gpumem and gres/gpuutil`。
- 审阅者推论（非原文）：编号映射不稳定，直接影响"哪张卡坏了、哪张卡分给了哪个作业"的对账，是与本库资源账本关系最大的 NVIDIA 条件。

关闭条件：增"GRES 绑定"行（`--tres-bind`/`--gpu-bind` 默认不绑定到 task、enforce-binding 可能推迟启动、Cores 按 socket 协同分配）；GPU 条件例子补编号映射与 `CUDA_DEVICE_ORDER`、环境变量作用范围、多于配置也会 drain、两页口径差异、MIG 不做 sanity-check；TRES 行补 GRES 记账前提。以上仍只限 NVIDIA，NPU 继续保留 unknown。

### B22-C17 — P2 / OPEN：失败、重排队与清理的异常分支不全；观察样板未按场景分组

位置：正文"取消、重排与清理" L89–100、等待原因 L66–72、L133；示例 L141–151；acceptance 1"资源清理"、acceptance 4。

证据：

- **重排循环的终点**：slurm.conf 页 `MaxBatchRequeue`：`Maximum number of times a batch job may be automatically requeued before being marked as JobHeldAdmin`，默认 5；job_reason_codes 页 `JobHoldMaxRequeue — Job has been requeued enough times to reach the MAX_BATCH_REQUEUE limit`。正文 L100 写了 Prolog 失败重排默认 held，但没有写重排上限与对应 reason。
- **held 的观察口径**：
  - job_reason_codes 页有 `JobHeldAdmin`、`JobHeldUser`。
  - test31.2 头注释 `Validate that a job is held and reason is set to launch failed requeued held when the prolog fails`，脚本接受 `launch_failed_requeued_held` 或 `JobHeldAdmin`（L122–125）。前者不在 reason 页，属测试层证据。
  - scontrol suspend 节：`If a suspended job is requeued, it will be placed in a held state`。
  - `Cleaning — The job is being requeued and still cleaning up from its previous execution`，正文 L72 只译为"清理中"。
- **清理卡住**：sinfo 页节点级 `COMPLETING`：`This node state will be removed when all of the job's processes have terminated and the Slurm epilog program (if any) has terminated`；另有 `ALLOCATED+`。slurm.conf 页 `UnkillableStepTimeout`（默认 60 s 与 5×MessageTimeout 取大）超时后 drain 节点。正文 L56 只写了"清理时长无承诺"。
- **其他失败处置**（prolog_epilog Failure Handling）：EpilogSlurmctld 失败只记日志；task prolog 失败则取消该 task；srun prolog 失败则取消该 step。正文 L100 只列了三项。
- **预留**：结束后 pending 作业转 held（正文已写）；`a reservation can not be deleted while there are jobs running in it`（正文未写）。
- **终止原因**：squeue `%R` 对 `terminated jobs with failure` 显示失败说明；reason 页有 `NonZeroExitCode`、`OutOfMemory`、`TimeLimit`、`JobLaunchFailure`、`SystemFailure`。正文 L133 把 reason 只与 PENDING 绑定。
- **应用侧可见的重排计数**：sbatch 页 `SLURM_RESTART_COUNT`，记录因系统故障重启或被显式重排的次数。
- 观察样板（L143–149）只列状态查询，没有按"提交/失败/重排队/清理"给出各场景应看到的字段变化。

关闭条件：

- 补一张"分支 × 先看字段 × 下一项检查"表，至少包含：重排上限与 JobHoldMaxRequeue/JobHeldAdmin；Prolog 失败转 held（引 test31.2 作上游行为样本，不是现场验证）；Cleaning；节点 COMPLETING 迟迟不消失 → Unkillable → drain；Epilog 失败 drain；EpilogSlurmctld、TaskProlog、SrunProlog 的处置；节点 DOWN 终止作业（与 C12 互引）。
- 观察样板按四类场景分组，并注明只读、未执行；终止态的 reason 与 PENDING reason 分开说明。

### B22-C18 — P2 / OPEN："成组资源条件"未写；Slurm 自身的 "gang scheduling" 与 K8s 同名术语未区分

位置：正文 L109"与 gang 调度不兼容"、L131"Slurm 无 Pod/Phase/Taint-Toleration/Queue（Kueue）/queue-gang 概念"；acceptance 3"成组资源条件""不能套用 K8s/Kueue/Volcano 同名术语"。

证据：

- overview 页功能列表 `gang scheduling (time sharing for parallel jobs)`；分区字段 `shared node access policy with optional over-subscription level for gang scheduling (e.g. YES, NO or FORCE:2)`。
- slurm.conf 页 PreemptMode `GANG`：`Enables gang scheduling (time slicing) of jobs in the same partition, and allows the resuming of suspended jobs`；`Heterogeneous jobs are excluded from GANG scheduling operations`。
- reservations 页：预留与 gang scheduler 插件不兼容，因为无法准确预测运行作业的结束时间。
- 由此可见 Slurm 自带名为 gang scheduling 的机制，含义是分时，不是 Volcano/Kueue 的全有或全无成组调度。正文 L131 说 Slurm 没有 gang 概念，L109 又直接写"与 gang 调度不兼容"，读者容易按 K8s 含义理解。这正是 acceptance 3 要防止的同名术语混用。
- 成组资源条件正文没有单独写。可用证据有：
  - sbatch `-N min[-max]`：分区节点上限优先；超出分区当前范围的作业留在 PENDING，超出分区配置节点数则直接拒绝；`SLURM_JOB_NUM_NODES` 为实际分配数。
  - overview：作业先获得一组节点，再在分配内启动 step。
  - scancel 页：异构作业 PENDING 时只能整体取消。
  - `--gres-flags=enforce-binding` 的同 socket 约束（见 C16）。

  审阅者在本轮 20 页中没有找到"多节点分配全有或全无"的明文，不能凭 overview 的叙述推定。

关闭条件：在"禁套 K8s 术语"一条写明 Slurm gang scheduling 指分时（PreemptMode=GANG 与分区 OverSubscribe），与 Volcano/Kueue 的 gang 不同义，并相应改写 L109、L131；新增"成组资源条件"条目，引上述字段；全有或全无语义若找不到一手明文，记 unknown。

### B22-C19 — P3 / OPEN：文档默认值被并入 unknown

位置：来源记录 unknown 第 5 条（L24）；正文 L89"KillWait 站点配置"、L94、L134、L158。

证据：slurm.conf 页给出了文档默认值：KillWait 30 s；JobRequeue 1；MaxBatchRequeue 5；ReturnToService 0；SlurmdTimeout 300 s；HealthCheckProgram 默认不执行。cgroup.conf 页：ConstrainDevices 默认 no，CgroupPlugin 默认 autodetect。文档默认值是已知的，站点实际值才是 unknown；现写法把两者合成了一个 unknown。

关闭条件：分开写"文档默认（引参数节）"与"站点实际（unknown，须读取现场配置）"。正文"不可把文档默认值当结论"的提醒保留。

### B22-C20 — P3 / OPEN：版本锚、用例引用与许可记录不够精确

位置：正文 L28、L127、L157；来源记录 L11"无 release/commit hash"、L16；登记 L5391、L5413、L5414–5417。

证据：

- `git ls-remote` 显示 `refs/tags/slurm-24-11-7-1` 为 tag 对象 `9d1ef1877186d8101769352831c8f0fe303df31c`，指向 commit `defaf214db2e55326f45ab08f1bde5b2036d9f5d`。来源记录写"无 release/commit hash"，这一项可以补上。
- 所取页面的页头只有 `Version 24.11`，补丁级版本只由归档 URL 路径确定（见取证节），正文与登记没有写明这一点。
- 用例引用：
  - `test31`：tag 上没有 `test31.1`（raw 404），相关文件是 test31.2（Prolog 失败转 held）与 test31.3（Prolog/Epilog 环境变量）。
  - `test8.x` 是通配写法，审阅者只确认了 test8.12（预留 FLEX 标志），test8.1 为 404。
  - `test24` 中 test24.2 是 sshare，不是 multifactor。
  - `test39` 实为 test39.1（sbatch `--gpu` 全集）、test39.2（salloc）等多个文件。
- 许可：testsuite README、各用例文件头与 man 页 COPYING 节都带 GPL v2 or later 声明；登记的 license 仍为 unknown，并写"未打开核对许可"。仓库根 LICENSE/DISCLAIMER 未核，本条只作提示。

关闭条件：登记与来源记录补上 tag 对象与 commit；写明"页内只标 24.11，补丁级由归档路径确定"；用例改为具体文件名加头注释目的；许可字段按已见声明补充，或保持 unknown 并改写 notes。

### B22-C21 — P3 / OPEN：措辞与精确度

位置：正文 L68、L70、L72、L81、L82、L94、L97、L98、L107、L117、L120、L122、L13、示例 L141–149。

证据与改法：

- L82：`~` 为 `presently in powered off`（已关机），`%` 才是关机中；漏 `@`（待重启）、`^`（已发重启）。
- L81：FAIL 为 `expected to fail soon and is unavailable for use per system administrator request`，不是"故障"；FAILING 为运行作业中且预计将故障。
- L98：reboot 的 `nextstate` 只能显式指定 RESUME 或 DOWN；UNDRAIN 是 ASAP 未指定 nextstate 时的默认值。不带 ASAP 时不会阻止新作业调度；超过 ResumeTimeout 未重启则置 DOWN。
- L97："需先 drain 节点或关分区"是 scontrol 页维护场景下的建议（`you may want to`），不是必需步骤；同页建议多数情况下改用 scancel 发 SIGSTOP/SIGCONT，且挂起时间不计入时限。
- L94："交互式 job 以 scontrol 语义为准"不准确：scontrol requeue 只针对 batch job；prolog_epilog 页为 `Only batch jobs can be requeued. Interactive jobs (salloc and srun) will be cancelled if the PrologSlurmctld fails`。
- L68："总量够≠可放置（单节点/拓扑约束另算）"不在 reason 页，应标为本库推论。L70："与调度器无关的等待"无出处，建议改为"非资源性等待"。L72：PartitionNodeLimit 还可能表示所需节点 DOWN 或 DRAINED。
- L107：公式中 `site_factor` 不乘权重，`nice_factor` 为减项，"九因子加权求和"需加限定。
- L122：原文为 `killing one or more of the processes in the step`，不是"只杀超限进程"；还可补上与 OverMemoryKill（整个 step 被杀）的区别。
- L117："只证四类字符串"应为"五个检测值，对应四家厂商（nvml/nvidia：NVIDIA；rsmi：AMD；oneapi：Intel；nrt：AWS Trainium/Inferentia），另有 off"。L13 摘要"NPU 接入无一手证据"建议写明 NPU 在本文指 Ascend；nrt 是唯一见到的非 GPU 加速器检测值，不构成 Ascend 证据。
- L120：TRESBillingWeights 用于 fairshare，正文只写了"不直接参与 priority"。
- 示例 L141–149：sinfo 页 PERFORMANCE 节要求不要在循环中调用会向 slurmctld 发 RPC 的客户端命令。只读命令也会给控制器增加负载，样板应加这条提醒。

关闭条件：逐条改正措辞或补充说明。

## acceptance 对照

| acceptance | 判定 | 相关发现 |
|---|---|---|
| 1 固定 release/commit 与官方文档；slurmctld/slurmd/slurmdbd、Job/Step、pending/running/completing/terminal、cancel/requeue 与资源清理 | 部分满足。成立的部分：归档路径与 tag 固定；守护进程、Job/Step、状态码、requeue 主体属实。缺口：scancel 信号语义写反；清理卡住、重排上限分支缺失；commit 未记录 | C15、C17（P2）；C20（P3） |
| 2 GRES/TRES、autodetect/binding、cgroup、健康/节点状态职责；一种 NVIDIA GPU 条件；NPU 无证据即 unknown | 部分满足。成立的部分：GRES 声明与请求、AutoDetect、cgroup、TRES 主体属实；NPU 保留 unknown。缺口：健康职责整体缺失；设备绑定只讲 CPU；GPU 条件缺编号映射等限制 | C13（P1）；C16（P2）；C21（P3） |
| 3 Slurm 状态、等待原因、配额/优先级/预留、节点 DRAIN/DOWN/RESUME 与成组资源条件；不套用 K8s 同名术语 | 部分满足。成立的部分：状态、原因、QOS/优先级/预留基本属实，有术语对照。缺口：节点动作语义可取却记为 unknown，缺 INVAL；成组资源条件未写；gang 同名混用 | C12（P1）；C18（P2）；C21（P3） |
| 4 来源支持的提交/失败/重排队/清理观察样板与最小验证设计；不提交作业、不推断设备可用即应用成功 | 部分满足。成立的部分：只读样板、未执行声明、"设备可见≠应用成功"。缺口：`sacct -D` 注释虚构；样板未按四类场景分组 | C14、C17（P2） |

横向问题：unknown 的使用方向有两类偏差。一类是可取证据被记为 unknown（C12 的节点 State、C19 的文档默认值）；另一类是 unknown 项该写而未写（C13 的 GPU 运行期健康、C18 的全有或全无语义）。NPU/Ascend 的 unknown 保留得当。

范围外观察（不计入本轮发现）：gres 页 Sharding 节写 `it does not fence the processes running on the GPU`，与 05.5 多租户隔离主题直接相关，可留给后续任务引用。

## 结论

**T05-03 初审不通过，需修订。B22-C12–C21 共 10 项：P1 ×2（C12、C13），P2 ×5（C14–C18），P3 ×3（C19–C21），全部 OPEN。**

- 修订后须按各项关闭条件做定向复核。
- C14、C15 关闭前，正文 `verification.status: source_checked` 不应视为成立：其中一处与所引原文相反，另一处的出处页未在来源范围内。
- 正文没有虚构命令输出或实测结果；范围声明与 `verification.notes` 如实写明未提交作业、未执行 Slurm 命令，这一点满足要求。
- 本审阅只覆盖编辑与来源层面，未部署 Slurm、未提交作业、未运行任何测试用例。文中的 Slurm 行为都是文档或测试源码层证据，不得标为 reproduced。
