# 第二十二批 T05-03 来源记录

任务：T05-03（新建 `knowledge/05-cluster-platform/slurm-jobs-and-device-resources.md`，reference）。作者取证轮次：首轮（Slurm 24.11.7 归档文档十九页）＋testsuite 用例编号存在性；sacct 页与用例头注释目的为审阅者补取（作者侧未独立打开），后补入二十页口径；用例头注释目的与行区间为审阅者取证（作者侧未独立打开用例文件），由只读取证角色完成，作者抽查归档 `job_state_codes.html` 确认 base states/flags 与证据表一致。

版本声明：固定 **Slurm 24.11.7**，全部 Slurm URL 使用 `https://slurm.schedmd.com/archive/slurm-24.11.7/` 前缀；主站当时已为 26.05，裸域名页为可变页，正文禁用。取证方式：`webfetch` 只读读取归档页正文；curl 字节级取回未执行；testsuite 仅用例编号存在性（作者侧），头注释目的与行区间为审阅者取证。

## 主张—来源定位表（ID—精确页面/节—字段/支持范围）

| 主张 | 登记 ID | 精确页面/节 | 支持范围 / 未覆盖 |
|---|---|---|---|
| 架构与实体 | src.slurm.docs-24.11.7 | [overview.html](https://slurm.schedmd.com/archive/slurm-24.11.7/overview.html)（slurmctld/slurmd/slurmdbd/slurmrestd；node/partition/job/job-step；分区字段；gang 分时） | tag slurm-24-11-7-1→commit defaf214；页内只标 24.11，补丁级由归档路径确定；故障切换细节不在此页 |
| 作业/节点状态 | src.slurm.docs-24.11.7 | [job_state_codes.html](https://slurm.schedmd.com/archive/slurm-24.11.7/job_state_codes.html)（base states＋COMPLETING 等 flags）/[job_reason_codes.html](https://slurm.schedmd.com/archive/slurm-24.11.7/job_reason_codes.html)（Resources/Priority/Dependency/QOS/Assoc 系列；多原因只显示命中者）/[squeue.html](https://slurm.schedmd.com/archive/slurm-24.11.7/squeue.html)（%t/%T/%r/%R）/[sinfo.html](https://slurm.schedmd.com/archive/slurm-24.11.7/sinfo.html)（DRAINED/DRAINING/DOWN 等节点态，-R 原因为管理员自填） | PENDING→RUNNING 调度判定细节不在此页；COMPLETING 清理时长无承诺；reason 字符串站点自填 |
| 取消/重排/清理 | src.slurm.docs-24.11.7 | [scontrol.html](https://slurm.schedmd.com/archive/slurm-24.11.7/scontrol.html)（requeue/requeuehold/suspend/resume/hold/release/reboot nextstate）/[sbatch.html](https://slurm.schedmd.com/archive/slurm-24.11.7/sbatch.html)（--requeue/--no-requeue：脚本从头跑、ID 不变）/[scancel.html](https://slurm.schedmd.com/archive/slurm-24.11.7/scancel.html)（默认 SIGCONT→SIGTERM→KillWait→SIGKILL；--signal/--batch/--full/--state）/[prolog_epilog.html](https://slurm.schedmd.com/archive/slurm-24.11.7/prolog_epilog.html)（四件套时机与失败处置：Epilog 非零→DRAIN；Prolog 非零→DRAIN＋重排默认 held） | KillWait/JobRequeue 文档默认与站点实际分开；只有 batch job 可重排，交互式在 PrologSlurmctld 失败时直接取消（prolog_epilog 页） |
| 分区/QOS/优先级/预留 | src.slurm.docs-24.11.7 | [priority_multifactor.html](https://slurm.schedmd.com/archive/slurm-24.11.7/priority_multifactor.html)（评估序与九因子）/[qos.html](https://slurm.schedmd.com/archive/slurm-24.11.7/qos.html)（priority/抢占/限额三作用）/[reservations.html](https://slurm.schedmd.com/archive/slurm-24.11.7/reservations.html)（root 创建、使用须完全落入、超时 cancel）/[slurm.conf.html](https://slurm.schedmd.com/archive/slurm-24.11.7/slurm.conf.html) 片段（ReturnToService/SlurmdTimeout） | 权重/限额/抢占表全站点配置；与 gang 调度不兼容 |
| GRES/TRES/cgroup | src.slurm.gres-tres-cgroup-24.11.7 | [gres.html](https://slurm.schedmd.com/archive/slurm-24.11.7/gres.html)（声明、请求、AutoDetect 五个检测值（对应四家厂商＋off）、CUDA_VISIBLE_DEVICES 在 Prolog 与 job 内可不同、MIG）/[gres.conf.html](https://slurm.schedmd.com/archive/slurm-24.11.7/gres.conf.html)（File-Count 一致性、失配节点 invalid+drain）/[tres.html](https://slurm.schedmd.com/archive/slurm-24.11.7/tres.html)（类型与 Billing 权重）/[cgroups.html](https://slurm.schedmd.com/archive/slurm-24.11.7/cgroups.html)＋[cgroup.conf.html](https://slurm.schedmd.com/archive/slurm-24.11.7/cgroup.conf.html)（插件三分、Constrain 系列，ConstrainDevices=yes 为硬隔离前提）/[resource_binding.html](https://slurm.schedmd.com/archive/slurm-24.11.7/resource_binding.html)（CPU bind 生效序） | 无 Ascend/NPU 一手证据（unknown）；cgroup 与内核/systemd 对应矩阵未取（unknown） |
| 回归用例入口 | src.slurm.testsuite-24-11-7-1 | [testsuite](https://github.com/SchedMD/slurm/tree/slurm-24-11-7-1/testsuite)（test1.62；test39.1/39.2；test40.1；test2.21/2.22/3.8；test31.2/31.3；test3.11/8.12；test24.1；test12.7）＋[sacct.html](https://slurm.schedmd.com/archive/slurm-24.11.7/sacct.html)（-D=--duplicates） | 用例头注释目的为上游行为样本；test12.7 约 L60–120、test31.2 L122–125 行区间为审阅者已核对范围（含代码，不仅头注释），作者侧不冒充已读；未审计断言/CI/运行，非本文验证 |

## unknown 清单

1. Ascend/NPU Slurm 接入：无一手支持证据（AutoDetect 仅见 `nrt`=AWS Trainium/Inferentia 一行命名）。
2. 通用 NPU GRES 插件/计费/绑定：无证据；不得把 GPU 章节套用于 NPU。
3. cgroup 版本与内核/systemd 对应矩阵：无证据。
4. ~~节点 update State 全枚举~~（已补：scontrol State=DOWN/DRAIN/RESUME/UNDRAIN/FAIL 等，见正文节点动作表；前态×新态合法组合未列出，unknown）。
5. 站点实际数值（DRAIN reason、QOS/分区权重、KillWait、JobRequeue 等）：unknown，须读现场配置；文档默认值见正文各行（KillWait 30 s、JobRequeue 1、MaxBatchRequeue 5、ReturnToService 0、SlurmdTimeout 300 s、ConstrainDevices no、CgroupPlugin autodetect）。
6. 全部实测（未提交作业；设备可用≠应用成功）。
