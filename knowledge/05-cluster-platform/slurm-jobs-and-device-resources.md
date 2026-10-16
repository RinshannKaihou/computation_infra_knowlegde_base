---
id: cluster-platform.slurm-jobs-and-device-resources
title: Slurm 作业生命周期、设备资源与状态参考
type: reference
domain: cluster-platform
status: draft
platforms: [generic]
source_refs:
- src.slurm.docs-24.11.7
- src.slurm.gres-tres-cgroup-24.11.7
- src.slurm.testsuite-24-11-7-1
updated_at: "2026-10-14"
summary: 固定 Slurm 24.11.7 归档文档（页内只标 24.11，补丁级由归档路径确定；tag slurm-24-11-7-1→commit defaf214），查询控制器/守护进程、Job/Step、GRES/TRES、分区/QOS/优先级/预留、cgroup 与状态的职责与字段；NPU（指 Ascend）接入无一手证据。
related_ids:
- cluster-platform.kubernetes-job-lifecycle
- cluster-platform.device-resource-chain
- cluster-platform.admission-and-placement
verification:
  status: source_checked
  evidence_refs:
  - src.slurm.docs-24.11.7
  - src.slurm.gres-tres-cgroup-24.11.7
  notes: "经 webfetch 只读核对 24.11.7 归档二十页（架构、作业/原因/节点状态码、squeue/sinfo/scontrol/sbatch/scancel、优先级/QOS/预留、Prolog-Epilog、slurm.conf 片段、GRES/TRES/cgroup/绑定）与 testsuite 用例存在性；curl 字节级取回未执行，未提交作业、未执行任何 Slurm 命令。"
---

# Slurm 作业生命周期、设备资源与状态参考

> 范围：Slurm **24.11.7** 归档文档（`https://slurm.schedmd.com/archive/slurm-24.11.7/` 前缀）。主站当时已为 26.05，裸域名页为可变页，本文禁用。本页是查询参考，不是操作手册；所有限额、权重、超时与原因字符串以站点配置为准，文档不给阈值。`generic` 仅为导航聚合；K8s/Kueue/Volcano 同名术语不得套用于 Slurm——Slurm 自带的 gang scheduling 指分时（PreemptMode=GANG 时间片＋分区 OverSubscribe），与 Volcano/Kueue 的全有或全无成组调度不同义。

## 范围与阅读方式

查询对象：slurmctld/slurmd/slurmdbd 职责、Job/Step 定义、作业与节点状态码、等待原因、分区/QOS/优先级/预留、GRES/TRES/cgroup/绑定、取消/重排/清理语义。不覆盖：具体站点的 slurm.conf 数值、账单与计费实现、Ascend/NPU 接入（无一手证据，unknown）、cgroup 与内核/systemd 版本对应矩阵（unknown）。凡写“站点配置”处，均表示文档把该值留给管理员，引用者须实地读取。

## 参考内容

### 架构与实体

| 条目 | 含义 | 条件或限制 | 证据位置 |
|---|---|---|---|
| slurmctld | 中央管理者，监控资源与作业；可配备份 | 故障切换细节不在概述页 | [overview](https://slurm.schedmd.com/archive/slurm-24.11.7/overview.html#architecture) |
| slurmd | 每计算节点守护进程，等待→执行→回状态→再等待；容错分层通信 | 类比远程 shell，不定义状态机 | 同上 |
| slurmdbd | 可选，多集群记账库；sacctmgr 管理库对象 | 未启用时限额/历史能力不存在 | 同上 |
| slurmrestd | 可选 REST API 守护进程 | 接口细节不在概述页 | 同上 |
| node | 计算资源；属性含处理器数、内存、临时盘、状态、weight、features | features 为任意站点字符串，不可跨站点比较 | 同上 |
| partition | 节点逻辑分组即作业队列；字段 name/nodes/state/MaxTime/MaxNodes/AllowGroups/priority/shared | 节点可重叠归属多分区；≠ namespace | 同上 entities 与配置示例 |
| job | 一次资源分配（用户在一段时间内独占/共享节点的许可） | ≠ K8s Job；无 completions 语义 | 同上 |
| job step | 分配内的并行 task 集；一个 job 可跑一个用满分配的 step，也可跑多个各用一部分的 steps；处理器资源管理允许多 steps 在分配内排队 | step ≠ job；取消 step 不释放分配 | 同上 |

### 作业状态与标志

| 条目 | 含义 | 条件或限制 | 证据位置 |
|---|---|---|---|
| PENDING | 已排队待启动；必看 reason 码 | 多原因并存只显示命中者 | [job_state_codes](https://slurm.schedmd.com/archive/slurm-24.11.7/job_state_codes.html) |
| RUNNING | 已分配资源并执行 | 不证应用进展 | 同上 |
| SUSPENDED | 已分配但被挂起（抢占或授权用户直接请求） | 恢复可能涉 CPU 冲突，见 scontrol 节 | 同上 |
| COMPLETING | 已结束或已取消，正在清理（含 epilog） | 清理时长无承诺；取消≠已清理完 | 同上 flags |
| COMPLETED | 全节点 exit 0 | 仅表进程退出码，不证结果正确 | 同上 |
| FAILED / TIMEOUT / NODE_FAIL / OUT_OF_MEMORY / BOOT_FAIL / DEADLINE / PREEMPTED / CANCELLED | 非零退出/达时限/节点故障/OOM/启动失败/达最晚可启动时间/被抢占/被取消 | PREEMPTED 后续状态随 PreemptMode 与作业特征而定 | 同上 |
| REQUEUED / REQUEUE_HOLD / RESV_DEL_HOLD / SPECIAL_EXIT | 重排队中/重排后 hold/预留删除致 hold/特殊 hold | 释配额与重调度语义见重排队节 | 同上 flags |
| CONFIGURING / POWER_UP_NODE / LAUNCH_FAILED / SIGNALING / STOPPED / STAGE_OUT 等 | 节点启动中/上电中/启动失败/信号发送中/已 SIGSTOP/数据 stage-out 中 | 存在性证据，细节各归所属页 | 同上 flags |

squeue/sacct 只报单一状态：base 全识，flag 只识部分，命中已识 flag 时报 flag 不报 base。紧凑码（BF/CA/CD/CG/DL/F/NF/OOM/PD/R/S/TO 等）与 `%t/%T/%r/%R` 格式见 [squeue](https://slurm.schedmd.com/archive/slurm-24.11.7/squeue.html)。

### 等待原因（PENDING reason）

| 条目 | 含义 | 条件或限制 | 证据位置 |
|---|---|---|---|
| Resources | 无满足请求的空闲资源组合 | 总量够≠可放置为本库推论（单节点/拓扑约束另算） | [job_reason_codes](https://slurm.schedmd.com/archive/slurm-24.11.7/job_reason_codes.html) |
| Priority | 优先级不足被更高作业压住 | 最高 priority 不一定先被评估（Tier/预留优先） | 同上 |
| Dependency / BeginTime | 依赖未满足/未到开始时间 | 非资源性等待 | 同上 |
| AssocGrp*/AssocMax*/QOSGrp*/QOSMax*/Max*PerAccount | 账户或 QOS 组限额 | 数值全站点配置 | 同上 |
| PartitionNodeLimit | 分区节点上限；还可表示所需节点 DOWN/DRAINED | 数值站点配置 | 同上 |
| PartitionDown / PartitionNodeLimit / ReqNodeNotAvail / Reservation / NodeDown / Cleaning / Prolog | 分区不可用/分区节点上限/请求节点不可用/等预留/节点故障/清理中/Prolog 中 | 预留等待须 job 完全落入预留 | 同上全表 |

### 节点状态

| 条目 | 含义 | 条件或限制 | 证据位置 |
|---|---|---|---|
| IDLE / MIXED / ALLOCATED | 空闲/部分分配/全分配 | 不证设备健康 | [sinfo](https://slurm.schedmd.com/archive/slurm-24.11.7/sinfo.html) |
| DRAINED / DRAINING | 管理员停用（DRAINED）/有活 job 只出不进、走完转 DRAINED | 节点态拼写；`sinfo -t drain` 为过滤简写 | 同上 |
| DOWN | 管理员/故障设置，**终止该节点上运行与挂起的作业**；回归受 ReturnToService/SlurmdTimeout 控制 | ReturnToService 默认 0（须人工恢复）；=1 仅无响应致 DOWN 且重注册合法才自动回；=2 任何原因 DOWN 在有效配置注册后都自动恢复；“有效配置”指内存、GRES、CPU ≥ slurm.conf 配置 | 同上＋[slurm.conf](https://slurm.schedmd.com/archive/slurm-24.11.7/slurm.conf.html) 片段 |
| INVAL | 注册资源少于配置，需 slurmd 重启后有效注册才清除 | 与 gres.conf 失配 invalid+drain 互引（见 GRES 节） | [sinfo](https://slurm.schedmd.com/archive/slurm-24.11.7/sinfo.html) |
| FAIL / FAILING / FUTURE / RESERVED / UNKNOWN / MAINT 等 | FAIL 为管理员认定的即将故障（`expected to fail soon … unavailable for use per system administrator request`）；FAILING 为运行作业中且预计将故障 | `-R` 原因字符串为管理员自填，无标准枚举 | 同上 |
| 后缀 `*`/`~`/`#`/`!`/`$`/`-`/`@`/`^` | 无响应/已关机（`~`；`%` 才是关机中）/上电中/待关机/维护预留/被 backfill 高优规划/待重启/已发重启 | 展示层标记，非状态本身 | 同上 |
| 分区 AVAIL up/down/drain/inact | 分区可用性 | 与节点态分开判断 | 同上 |

节点状态动作（字段与语义参考，非操作步骤，均见 [scontrol](https://slurm.schedmd.com/archive/slurm-24.11.7/scontrol.html) NODES UPDATE 节）：DRAIN（不再接受新作业，现有跑完转 DRAINED）→DRAINING→DRAINED；DOWN（终止运行与挂起作业，不再接受新作业）；RESUME（**不是状态**；DRAIN/DRAINING/DOWN/REBOOT→IDLE＋NoResp，需 slurmd 重新注册才去 NoResp）；UNDRAIN（只清 drain，不改 base state 如 DOWN，需有效注册）；FAIL；`Reason=`（DOWN/DRAINED/DRAINING/FAILING/FAIL 适用）/`ResumeAfter=`（定时恢复）。前态×新态合法组合文档称部分无效但未列出（unknown）。

### 健康与节点状态职责

职责划分见 [slurm.conf](https://slurm.schedmd.com/archive/slurm-24.11.7/slurm.conf.html) 与 scontrol reboot 节：slurmctld 响应探测（SlurmdTimeout 默认 300 s，等不到响应置 DOWN；=0 则由其他工具负责监控）＋注册校验（内存/GRES/CPU ≥ 配置才为有效配置）；slurmd 启动时 HealthCheckProgram 跑一次再注册；HealthCheckProgram（root 定期执行于非 NOT_RESPONDING 节点，60 秒未结束被杀，默认不执行，间隔 HealthCheckInterval；发现问题由脚本自己执行 drain/发信）；UnkillableStepTimeout（SIGKILL 后仍未退出超限执行 UnkillableStepProgram，节点 drain）；重启后 HealthCheckProgram 先跑，随后注册清 REBOOT 旗，ResumeTimeout 内未重启则置 DOWN。恢复路径见节点动作表。GPU 运行期健康探测（ECC/XID 类）在所取 20 页中无条目（unknown），站点脚本检查内容不可推定；NPU 同为 unknown。

### 取消、重排与清理

| 条目 | 含义 | 条件或限制 | 证据位置 |
|---|---|---|---|
| scancel 默认（不带 `--signal`） | 先 SIGCONT 唤醒，再 SIGTERM，等 KillWait（文档默认 30 s，站点实际 unknown），再 SIGKILL，终止整个 job | KillWait 站点配置 | [scancel](https://slurm.schedmd.com/archive/slurm-24.11.7/scancel.html) |
| scancel --signal | 只带 `--signal`：所有 job steps 收到信号，batch shell（脚本本身）收不到；`--signal=KILL` 只杀活动 steps 不取消 job | 信号≠取消；SIGKILL 例外 | 同上 |
| scancel --batch / --full | `--signal --batch`：只 batch shell 收到（子进程靠 shell 转发，shell 运行子命令期间多不能处理信号）；`--full`：shell、子进程与 steps 都收到（srun steps 也是 batch step 的子进程） | `--batch`/`--full` 只在发信号时有意义；训练靠 SIGTERM/SIGUSR 存盘时决定信号能否到达计算进程 | 同上 |
| scancel --state / job.step | 限 PENDING/RUNNING/SUSPENDED；`scancel job.step` 只取消 step 不释放分配 | step 与 job 严格区分 | 同上 |
| sbatch --requeue | 管理员显式/节点故障/高优抢占后重排队；脚本从头执行、job ID 不变 | 应用能否续算文档不承诺；`JobRequeue` 文档默认 1（站点实际 unknown，须读现场配置；文档默认值不可当结论） | [sbatch](https://slurm.schedmd.com/archive/slurm-24.11.7/sbatch.html) |
| sbatch --no-requeue | 禁一切重排队（含重启/故障/抢占）；`PrologFlags=ForceRequeueOnFail` 可覆盖；默认由 `JobRequeue` 定 | 只有 batch job 可重排；交互式（salloc/srun）在 PrologSlurmctld 失败时直接取消 | 同上＋[prolog_epilog](https://slurm.schedmd.com/archive/slurm-24.11.7/prolog_epilog.html) |
| scontrol requeue [Incomplete] | 运行/挂起/已结束 batch job 回 pending；Incomplete 仅 CONFIGURING/RUNNING/STOPPED/SUSPENDED | 语义以 scontrol 页为准 | [scontrol](https://slurm.schedmd.com/archive/slurm-24.11.7/scontrol.html) |
| scontrol requeuehold / State=SpecialExit | 加 hold（priority 0）/显式特殊态 | 释放前不参与调度 | 同上 |
| scontrol suspend/resume | 释 CPU；resume 可能与他 job 同 CPU；维护场景建议先 drain 节点或关分区（`you may want to`，非必需），多数情况改用 scancel SIGSTOP/SIGCONT | 不是 K8s 的 suspend | 同上 |
| scontrol reboot … nextstate | nextstate 只可显式指定 RESUME 或 DOWN；UNDRAIN 是 ASAP 未指定 nextstate 时的默认值；不带 ASAP 不阻止新作业调度；ResumeTimeout 内未重启则置 DOWN | 只用已证值 | 同上 |
| Prolog/Epilog 四件套 | Prolog（slurmd，首 step 前；Alloc 旗则分配即跑）/PrologSlurmctld/Epilog（slurmd，释放时每节点必跑）/EpilogSlurmctld；TaskProlog/Epilog 走用户环境 | 脚本须短、禁调 Slurm 命令；Prolog/Epilog 外于 cgroup，`CUDA_VISIBLE_DEVICES` 可与 job 内不同 | [prolog_epilog](https://slurm.schedmd.com/archive/slurm-24.11.7/prolog_epilog.html) |
| Prolog/Epilog 失败 | Epilog 非零→节点 DRAIN；Prolog 非零→节点 DRAIN＋job 重排（缺省 held，除非 `SchedulerParameters=nohold_on_prolog_fail`；转 held 见 test31.2 上游行为样本）；PrologSlurmctld 非零→batch 重排、交互 job（salloc/srun）直接取消；EpilogSlurmctld 失败只记日志；task prolog 失败取消该 task；srun prolog 失败取消该 step | 默认 held，注意反转参数 | 同上 |
| 重排上限 | `MaxBatchRequeue`（文档默认 5）次后标 `JobHeldAdmin`（reason `JobHoldMaxRequeue`） | 上限站点配置 | [slurm.conf](https://slurm.schedmd.com/archive/slurm-24.11.7/slurm.conf.html)＋reason 页 |
| 清理卡住 | 节点 COMPLETING 迟迟不消失→查未退出进程/Epilog；`UnkillableStepTimeout` 超时 drain 节点 | COMPLETING 移除条件：job 进程全终止且 Epilog 结束 | sinfo＋slurm.conf |
| 预留约束 | 预留中有运行作业时不得删除该预留 | 结束 pending 转 held（`NO_HOLD_JOBS_AFTER_END` 反转） | [reservations](https://slurm.schedmd.com/archive/slurm-24.11.7/reservations.html) |
| 重排清理中（Cleaning） | 作业正被重排、仍在清理上一次执行（reason `Cleaning`） | 与 COMPLETING 区分：前者终态为重排，后者为结束/取消 | reason 页 |
| 节点 DOWN 终止作业 | 节点 DOWN 时其上运行与挂起作业被终止（见节点动作表） | 先看节点态与 `Reason=`，再看作业终止原因 | scontrol＋sinfo 互引 |
| 终止原因 | `NonZeroExitCode`/`OutOfMemory`/`TimeLimit`/`JobLaunchFailure`/`SystemFailure`（终止态）与 PENDING reason 分开读；squeue `%R` 对失败终止作业显示说明 | 应用侧重排计数见 `SLURM_RESTART_COUNT` | reason 页＋squeue＋sbatch |

### 分区 / QOS / 优先级 / 预留

| 条目 | 含义 | 条件或限制 | 证据位置 |
|---|---|---|---|
| 调度评估序 | 可抢占 > 有预留 > 分区 PriorityTier > job priority > 提交时间 > JobID | 不是单一 priority 排序 | [priority_multifactor](https://slurm.schedmd.com/archive/slurm-24.11.7/priority_multifactor.html) |
| multifactor 九因子 | age/assoc/fairshare/jobsize/nice/partition/qos/site/TRES 加权（因子 0..1，权重 32 位，`site_factor` 不乘权重、`nice_factor` 为减项；总值 0..4294967295）；sprio 看分项，squeue %p/%Q 看综合 | 权重全站点配置 | 同上 |
| QOS 三作用 | priority 因子（需 PriorityWeightQOS>0）、抢占（PreemptType=preempt/qos，按 QOS 抢占表）、限额（覆盖 assoc 限额；分区 QOS 只给限额不给 priority/抢占，除非 job 另求同名 QOS；OverPartQOS 反转）；Relative QOS（23.11+）按百分比 | QOS≠PriorityClass；名/限额/抢占表站点配置；经 sacctmgr 定义、`--qos` 请求 | [qos](https://slurm.schedmd.com/archive/slurm-24.11.7/qos.html) |
| 预留 | 仅 root/SlurmUser 经 scontrol 创建/改/删；资源 cores/nodes/licenses/burst buffers；节点/核预留绑定单分区（显式节点除外）；使用须 `--reservation=name` 且完全落入，超时即 cancel（ResvOverRun 可延）；不改变 priority，但同分区内有预留 job 先被考虑；结束默认 purged，pending 去预留转 held（NO_HOLD_JOBS_AFTER_END 可反转） | reservation≠Reservation CRD；与 gang scheduler 插件不兼容（无法准确预测作业结束时间） | [reservations](https://slurm.schedmd.com/archive/slurm-24.11.7/reservations.html) |
| 成组资源条件 | 作业先获一组节点（`-N min[-max]`，分区上限优先；超当前范围留 PENDING，超配置数直接拒绝；`SLURM_JOB_NUM_NODES` 为实分数），再在分配内起 steps；异构作业 PENDING 时只能整体取消；同 socket 约束见 GRES 绑定行 | 多节点分配是否全有或全无无一手明文（unknown，不据概述叙述推定） | sbatch＋overview＋scancel＋gres.conf |

### GRES / TRES / cgroup / 绑定

| 条目 | 含义 | 条件或限制 | 证据位置 |
|---|---|---|---|
| GRES 声明 | 默认无 GRES，须 slurm.conf `GresTypes/Gres` 声明；资源不足节点置 DRAIN | 声明缺失≠设备缺失，先查配置 | [gres](https://slurm.schedmd.com/archive/slurm-24.11.7/gres.html) |
| GRES 请求 | `--gres=name[:type:count]`；`--gpus/--gpus-per-node/socket/task` 仅 select/cons_tres；`--cpus-per-gpu/--gpu-bind/--gpu-freq/--mem-per-gpu` 同限 | 请求语法与选择插件绑定 | 同上 |
| AutoDetect | 五个检测值对应四家厂商（nvml/nvidia：NVIDIA；rsmi：AMD；oneapi：Intel；nrt：AWS Trainium/Inferentia；另有 off）；nvidia 为 24.11+（无需 nvml 库但不检 MIG/NVLink）；仍需 slurm.conf Gres 行声明期望数；Type 须为检测名子串（空格转下划线，`slurmd -C/-G` 查看）；nrt 是唯一见到的非 GPU 加速器检测值，不构成 Ascend 证据 | NPU 在本文指 Ascend，无一手证据 | 同上＋[gres.conf](https://slurm.schedmd.com/archive/slurm-24.11.7/gres.conf.html) |
| GPU 条件例子（NVIDIA） | 每 step 设 `CUDA_VISIBLE_DEVICES`（只反映该 step 所在节点的分配，sbatch 环境变量只反映 node zero）；NVML 按 PCI bus ID 编号，`/dev/nvidia*` 按 minor 号，映射 `nondeterministic and system dependent, and could vary between boots after hardware or OS changes`，原文要求 `an after-bootup check is required`，须 `CUDA_DEVICE_ORDER=PCI_BUS_ID` 才与 CUDA 编号一致（编号不稳影响坏卡/分卡对账为本库推论，非原文）；检测设备多于配置时 slurmd 同样被 drain；校验失配 gres 页为 GPU `is omitted from the node with an error`、gres.conf 页为 invalid+drain（两页口径并存）；MIG 用 `AutoDetect=nvml`＋按 MIG Profile 子串设 Gres type，不支持动态分区，sanity-check 不支持 MIG | 设备可见≠应用成功 | 同上 GPU/MIG 节 |
| gres.conf 一致性 | File↔Count 一致；Type/Cores/Links 作 sanity check，失配节点 invalid+drain；MIG 用 MultipleFiles（与 File 互斥）；Flags 含 CountOnly/explicit/环境变量旗 | Cores 为逻辑编号（lstopo Core L#），不可当物理核号 | [gres.conf](https://slurm.schedmd.com/archive/slurm-24.11.7/gres.conf.html) |
| TRES | Type+Name；类型 BB/Billing/CPU/Energy/FS/GRES/IC/License/Mem/Node/Pages/VMem；默认跟踪 Billing/CPU/Energy/Memory/Node/FS-Disk/Pages/VMem 不可关，只能追加；Billing 由分区 TRESBillingWeights 算（缺省=CPU 数，用于 fairshare；`The Billing TRES is not available for priority calculations`） | 要让 TRES 影响 priority，用 PriorityWeightTRES 按 TRES 类型（CPU/Mem/GRES 等）加权，Billing 不在其列；GRES 须写入 `AccountingStorageTRES` 才被记账（带子类型建议同时写通用类型，否则只求 `gpu:1` 的作业不计入）；`gres/gpu` 同时置 `gres/gpumem` 与 `gres/gpuutil`；权重站点配置 | [tres](https://slurm.schedmd.com/archive/slurm-24.11.7/tres.html) |
| cgroup 插件 | v1 多层级 vs v2 统一层级＋top-down＋no-internal-process＋systemd Delegate 约束；hybrid 不支持；proctrack/cgroup（freezer 跟踪/发信号）、task/cgroup（唯一能硬约束：cpuset/memory/devices，含 GRES/GPU）、jobacct_gather/cgroup（cpuacct/memory 统计） | 与内核/systemd 版本对应矩阵未取 | [cgroups](https://slurm.schedmd.com/archive/slurm-24.11.7/cgroups.html) |
| cgroup.conf | CgroupPlugin=v1/v2/autodetect/disabled（文档默认 autodetect）；ConstrainCores/ConstrainDevices（文档默认 no）/ConstrainRAMSpace（原文 `killing one or more of the processes in the step`，非只杀超限进程；与 OverMemoryKill 整 step 被杀区分）/ConstrainSwapSpace/AllowedRAMSpace；slurm.conf 需 ProctrackType/TaskPlugin/JobAcctGatherType 配合 | **ConstrainDevices=yes 是 GRES device 硬隔离前提**，不可默认已开 | [cgroup.conf](https://slurm.schedmd.com/archive/slurm-24.11.7/cgroup.conf.html) |
| CPU bind 生效序 | srun --cpu-bind > 节点 CpuBind（全分配节点一致才用）> 分区 CpuBind > TaskPluginParam | 见 resource_binding | [resource_binding](https://slurm.schedmd.com/archive/slurm-24.11.7/resource_binding.html) |
| GRES 绑定 | `--tres-bind`（仅 gres 受支持；默认多数 tres 不绑定到 task；类型 closest/map 等）/`--gpu-bind` 等价；`--gres-flags=enforce-binding`（作业只能用绑定 CPU，`may result in delayed initiation`，如双 GPU 单 CPU 作业等同 socket 两卡空闲）；gres.conf `Cores` 按 socket 协同分配，未带 enforce-binding 时仅优先，超绑需 disable-binding | 绑定≠分配，延迟启动为正常代价 | [sbatch](https://slurm.schedmd.com/archive/slurm-24.11.7/sbatch.html)＋[gres.conf](https://slurm.schedmd.com/archive/slurm-24.11.7/gres.conf.html) |

### 回归用例入口

testsuite（tag `slurm-24-11-7-1`→commit `defaf214`）相关用例（头注释目的为审阅者取证，见回归用例入口）：expect test1.62（gres/gpu 插件）、test39.1（sbatch `--gpu` 全集）/test39.2（salloc）、test40.1（invalid gres/mps）、test2.21（requeue 失败/完成作业）/test2.22（requeuehold）/test3.8（batch 重排）、test31.2（Prolog 失败转 held）/test31.3（Prolog/Epilog 环境变量）、test3.11（reservation 增删改）、test8.12（预留 FLEX 标志）、test24.1（multifactor；test24.2 为 sshare 非 multifactor）、test12.7。用例头注释目的（test12.7 `Validate that sacct -D shows correct job steps and states when a job is requeued` 等）为审阅者取证，作者侧未独立打开用例文件；test12.7 约 L60–120、test31.2 L122–125 行区间同样为审阅者已核对范围（含代码）；未审计断言，未查 CI，未运行，需起服 Slurm 才能执行。

## 使用与解释注意事项

- **禁套 K8s 术语**：partition≠namespace，QOS≠PriorityClass，reservation≠Reservation CRD；Slurm 无 Pod/Phase/Taint-Toleration/Queue（Kueue）/queue-gang 概念（但 Slurm 自带 gang scheduling 指分时，见上表）；`suspend`（释 CPU；维护建议先 drain/关分区，或用 scancel 发 SIGSTOP/SIGCONT，挂起时间不计入时限）≠ K8s Job `suspend`（删活动 Pod）。
- Job vs Job Step 严格区分：分配（job）与步（step）资源继承/独占按 gres 页；`scancel job.step` 只取消 step 不释放分配。
- 状态解读：squeue 单状态可被 flag 覆盖（COMPLETING 等）；PENDING 必须连 reason 一起读，且多原因只显示命中者，reason≠根因证明。
- 数值一律站点化：QOS/分区权重、限额、KillWait、JobRequeue 默认、DRAIN reason（`-R` 自填无枚举）都不可抄文档默认值当结论。
- NPU/Ascend：全页无一手支持证据，只可写“未找到一手支持证据（unknown）”，禁写“Slurm 原生支持 NPU/需某插件”、禁把 GPU 章节套用于 NPU。
- 设备可见≠应用成功：`CUDA_VISIBLE_DEVICES` 在 Prolog/Epilog 与 job 内可因 cgroup device 约束而不同；GRES 已分配不证框架初始化成功。
- 观察样板与最小验证只给只读命令＋预期字段（提交：sbatch 参数与 `SLURM_JOB_NUM_NODES` 实分数；失败：squeue `%R` 终止说明＋reason 终止类；重排队：sacct `-D` 全部记录＋`SLURM_RESTART_COUNT`；清理：sinfo COMPLETING/`scontrol completing`（正在清理的作业及其 COMPLETING/DOWN 关联节点）），禁写“提交作业验证通过”类结论；终止态 reason 与 PENDING reason 分开读。sinfo PERFORMANCE 节要求勿在循环中调用向 slurmctld 发 RPC 的客户端命令，只读命令同样增加控制器负载。

## 示例

只读观察样板（不提交作业；字段含义见上表，输出随站点配置而异）：

```bash
# 提交：参数与实分数（只读核对，不提交）
# squeue -o "%i %T %r %q %P"        # jobid、状态、原因、QOS、分区
# 失败：终止说明与原因类（PENDING reason 与终止态 reason 分开读）
# squeue -t all -o "%i %T %R"        # %R 对失败终止作业显示说明；不带 -t 时默认只列 pending/running/completing，已终止作业须 -t all，且只在 slurmctld 内存保留期内（`MinJobAge`，最短保留时间，文档默认 300 s，0 表示不清除，站点实际 unknown）可见，超出后用 sacct
# 重排队：全部记录与重启计数
sacct -D -j <jobid>              # `--duplicates`：返回同一 job ID 的全部记录（含重排前的运行），见 test12.7 头注释目的（需启用记账，记录未被关闭）
# 清理：节点 COMPLETING 与未完成作业
sinfo -R -t drain,down           # 处于 drain/down 的节点及管理员填写的原因
scontrol completing              # 查看正在清理中的作业（scontrol 页有出处；epilog 状态无 scontrol 出处，不写）
scontrol show job <jobid>        # 作业分配、step、GRES/TRES、预留与限制
scontrol show node <nodename>    # 节点状态、GRES、drain 原因
```

最小验证设计（未执行）：在可支配的测试分区内，用只读命令核对同一 job 的 squeue 状态/reason、scontrol 分配与 sacct 历史三者一致；用 `sinfo -R` 核对 DRAIN/DOWN 节点原因；用 `slurmd -C/-G` 输出核对 GRES 声明与检测名。以上均需真实 Slurm 环境，本文未执行。

## 来源与更新范围

- [Slurm 24.11.7 归档](https://slurm.schedmd.com/archive/slurm-24.11.7/overview.html)：overview、job_state_codes、job_reason_codes、squeue、sinfo、scontrol、sbatch、scancel、priority_multifactor、qos、reservations、prolog_epilog、slurm.conf 片段。
- [GRES/TRES/cgroup 归档](https://slurm.schedmd.com/archive/slurm-24.11.7/gres.html)：gres、gres.conf、tres、cgroups、cgroup.conf、resource_binding。
- [testsuite（tag slurm-24-11-7-1）](https://github.com/SchedMD/slurm/tree/slurm-24-11-7-1/testsuite)：上文用例编号的存在性；头注释目的为审阅者取证。
- [sacct](https://slurm.schedmd.com/archive/slurm-24.11.7/sacct.html)：`-D, --duplicates` 节。
- 待确认：Ascend/NPU 一手支持证据；cgroup 与内核/systemd 对应矩阵；节点前态×新态合法组合（文档称部分组合无效但未列出）；多节点分配全有或全无一手明文；全部站点实际数值（文档默认值见各行）；全部实测（未执行）。
