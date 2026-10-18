# 第二十三批 T05-09 来源记录

任务：T05-09 平台组件升级、发布、回退与回服（procedure 类新文章的知识材料；双平台有限版本样板）。取证轮次：只读取证角色首轮，2026-10-18 完成。取证方式：全部经 FetchURL 只读读取；未做 curl 字节级取回（本轮 GitHub 经 FetchURL 读取 raw.githubusercontent.com 成功，未复现历史本地 curl DNS 失败）；未使用 WebSearch 片段作为主张证据（仅用于定位 GPU Operator upgrade 页 URL 形态）。

版本声明：

- Kubernetes version skew：实开两形态。可变主页 https://kubernetes.io/releases/version-skew-policy/（2026-10-18 观察，当时最新 1.37、维护分支 1.37/1.36/1.35，示例以 1.36→1.37 写）；固定对应物 v1.32 静态快照 https://v1-32.docs.kubernetes.io/releases/version-skew-policy/（自述 "static snapshot"，维护分支行文停在 1.36/1.35/1.34，示例以 1.31→1.32 写）。正文引用以 v1.32 快照为准，主页只作「可变页」对照。
- kubeadm：v1.32 静态快照 https://v1-32.docs.kubernetes.io/docs/tasks/administer-cluster/kubeadm/kubeadm-upgrade/（内容覆盖 1.31.x→1.32.x 与 1.32.x→1.32.y）。
- Slurm：固定 24.11.7 归档前缀 https://slurm.schedmd.com/archive/slurm-24.11.7/；upgrades.html 页脚 "Last modified 15 January 2025"，quickstart_admin.html 页脚 "Last modified 14 November 2024"。
- NVIDIA GPU Operator：固定 25.3 次版本文档树 https://docs.nvidia.com/datacenter/cloud-native/gpu-operator/25.3/（URL 级别固定到次版本；2026-10-18 观察时该树 release notes 顶条为 25.3.4、upgrade 页示例 RELEASE_TAG=v25.3.4）。/latest/ 可变树当时 release notes 顶条为 26.7.2（2026-10-18 观察），仅用于确认 latest 指针位置，不引正文。
- MindCluster/Ascend：固定 commit 44385c13d7b1d87def35f1604e8be4d16de6ca4e（annotated tag v26.1.1，与既有登记 src.ascend.mind-cluster-v26.1.1 同 commit）；docs/zh/release_notes.md 产品版本字段写 "26.1.0"。

## 主张—来源定位表（主张—登记 ID—精确页面/节—支持范围/未覆盖）

| 主张 | 登记 ID | 精确页面/节 | 支持范围 / 未覆盖 |
|---|---|---|---|
| 变更档案须含备份与回退资产（StateSaveLocation、slurm 配置目录、MySQL dump；先读 RELEASE_NOTES/NEWS、配置变更、OpenAPI data_parser 兼容、停机计划） | src.slurm.upgrades-24.11.7（NEW） | [upgrades.html](https://slurm.schedmd.com/archive/slurm-24.11.7/upgrades.html) 节 Create Backups / Preparation（RELEASE_NOTES and NEWS、Configuration Changes、Plan for Downtime、OpenAPI Changes 含 v0.0.x 插件移除表与 --json=v0.0.41+spec_only 对比手法） | 备份三件套最小集明确（StateSaveLocation 可用 `scontrol show config \| grep StateSaveLocation` 查询）；具体备份工具/流程官方不提供（"procedures are not provided here"） |
| 变更档案须含 kubeadm 侧回退资产与预检（备份建议、kubeadm upgrade plan 检查、失败后备份目录） | src.kubernetes.kubeadm-upgrade-v1-32（NEW） | [kubeadm-upgrade v1.32](https://v1-32.docs.kubernetes.io/docs/tasks/administer-cluster/kubeadm/kubeadm-upgrade/) 节 Before you begin（备份最佳实践、swap 关闭）/ Recovering from a failure state（幂等重跑、`apply --force` 同版本恢复、/etc/kubernetes/tmp 下 kubeadm-backup-etcd-<date>-<time> 与 kubeadm-backup-manifests-<date>-<time> 手动恢复路径）/ How it works（apply 预检：API 可达、节点全 Ready、控制面健康、强制 skew 策略） | 页面无 downgrade/回滚节；K8s 控制面「不可直接回退」的证据边界到此（只支持幂等重跑与备份恢复 manifests/etcd），不得引申出官方降级流程 |
| 版本未固定时命令不可直接执行（各平台官方文档命令均含版本占位） | 本表全部 NEW 条目 | Slurm 无整段命令但要求按 RELEASE_NOTES 逐步；kubeadm 页命令含 `1.32.x-*`/`v1.32.x` 占位；GPU Operator upgrade 页 `export RELEASE_TAG=v25.3.4` 后再 helm；MindCluster helm/手动升级页 `{version}` 占位并明示「请用户自行将命令中的{version}替换为对应版本号」 | 支持「档案固定版本后才给可执行序列」的写作规则；各页占位形式不同，引用时保留原样 |
| K8s 组件版本偏差规则与升级顺序（apiserver HA 内 ±1 minor；kubelet 不得新于 apiserver、可旧至 3 个 minor；kcm/scheduler/ccm 不得新于 apiserver、可旧 1；kubectl ±1；kube-proxy 同 kubelet 规则） | src.kubernetes.version-skew-v1-32（NEW） | [version-skew-policy v1.32](https://v1-32.docs.kubernetes.io/releases/version-skew-policy/) 节 Supported version skew 各组件小节（含 HA 内 apiserver 混版收窄 kubelet/kube-proxy/kubectl 允许范围的示例） | 组件升级顺序：apiserver→kcm/scheduler/ccm（三者间无顺序）→kubelet（可选，可留旧）→kube-proxy（可选）；kubelet minor 升级前必须 drain、不支持原地 minor 升级；kubelet/kube-proxy 持续落后 3 minor 会阻塞后续控制面升级（Warning 段） |
| kubeadm 控制面先升、其余控制面、再工作节点；逐台进行；kubelet 升级前 drain、升后 uncordon；CNI 插件手动升级；全部容器因 spec hash 变化重启 | src.kubernetes.kubeadm-upgrade-v1-32（NEW） | 同页节 The upgrade workflow at high level / Upgrading control plane nodes（首台 `kubeadm upgrade apply`、其余 `kubeadm upgrade node`、手动升级 CNI、drain、升 kubelet/kubectl、重启 kubelet、uncordon）/ Upgrade worker nodes（"one node at a time or few nodes at a time, without compromising the minimum required capacity"）/ Verify the status of the cluster（kubectl get nodes 全 Ready 且版本更新） | 支持「控制面→节点」顺序与逐台/小批波次形态；worker 页细节（Linux/Windows 子页）本轮未开 |
| 设备插件运行条件（kubelet 重启删除 sockets、插件重注册、unhealthy 设备 allocatable 变化、PodResources 端点） | src.kubernetes.device-plugins-v1-32（复用）＋src.nvidia.k8s-device-plugin-v0.20.1（复用） | 复用既有登记核对范围（v1.32 device-plugins 页 Handling kubelet restarts / Device plugin and unhealthy devices / Monitoring 节） | 本轮未重开；NVIDIA 插件与 kubelet/CUDA 的版本配套矩阵无证据（unknown） |
| Slurm 兼容窗口与分步升级（24.11 起兼容前三个大版本；表列 23.02–25.11 各版本兼容集；不兼容版本启动即失败、须分步且每步验证；窗口外升级杀作业丢账目） | src.slurm.upgrades-24.11.7（NEW） | [upgrades.html](https://slurm.schedmd.com/archive/slurm-24.11.7/upgrades.html) 节 Release Cycle / Compatibility Window（兼容表；24.11 兼容 24.05/23.11/23.02；分步示例 20.11→22.05→23.11） | 分步仅见 20.11→22.05→23.11 一例；到 24.11 的具体跨度组合未逐一验证 |
| Slurm 不可直接回退边界（任一 daemon 启动即迁移状态文件/数据库结构；回退旧版不识别新状态→状态/账目丢失损坏、daemon 拒启；只能靠备份/镜像/快照回退且丢失备份后一切；至少恢复 StateSaveLocation 与账目库） | src.slurm.upgrades-24.11.7（NEW） | 同页节 Reverting an Upgrade；Minor Upgrades（维护版升级流程同大版本、混合版本与原地降级更宽容但仍须当前备份） | 明确「可回退」只存在于未启动新 daemon 或完整备份恢复两条路；状态迁移后无原地 downgrade |
| Slurm 升级顺序与停机/波次形态（顺序 slurmdbd→slurmctld→slurmd→登录节点/客户端→重编译插件→测试→归档；slurmdbd 先升且同/高于 slurmctld；slurmd 可与 slurmctld 同升或分组滚动；调大 SlurmdTimeout/SlurmctldTimeout 并 reconfig 防节点 DOWN 杀作业；slurmdbd 升级期间 sacct/sacctmgr 不可用、监控 slurmctld 内存与 DBD Agent 队列 MaxDBDMsgs；等旧 slurmstepd 作业全部结束才算完成） | src.slurm.upgrades-24.11.7（NEW） | 同页节 Upgrade Procedure 摘要 / slurmdbd (Accounting)（首次启动以 SlurmUser 前台跑防 systemd 超时杀进程、备库同升、验证 sacct）/ Database Server（MariaDB 10.2.1+ 需 slurmdbd ≥22.05.7）/ slurmctld (Controller) / slurmd (Compute Nodes) / Other Slurm Commands / Customized Slurm Plugins（libslurm.so.X.0.0 每个大版本 soname 递增、自研插件须重编译；PMI-1/PMI-2 永久固定例外；ldd 查 libslurm 引用法；MPICH+Hydra 例外）/ Seamless Upgrades（独立目录+符号链接切换，仅解决二进制层回切，不回迁状态） | slurmd 滚动升级官方表述为 "any number of groups"（波次）；无逐台健康门禁细节；Seamless 节不构成状态回退 |
| Slurm 状态/恢复点补充（daemon 默认恢复既有状态；-c 清除状态；StateSaveLocation 低时延本地盘、HA 共享盘勿用 NFS；控制器起不来且无状态→排队与运行中作业取消） | src.slurm.upgrades-24.11.7（NEW，quickstart_admin 补充核对） | [quickstart_admin.html](https://slurm.schedmd.com/archive/slurm-24.11.7/quickstart_admin.html) 节 Starting the Daemons（-c 语义）/ Configuration（StateSaveLocation 部署建议）/ Upgrades（仅回链 Upgrade Guide） | quickstart 的 Upgrades 节无独立内容；本条作为状态恢复点旁证 |
| GPU Operator 升级边界与算子升级步骤（仅支持同一大版本内或到下一大版本；生命周期：前一 major 维护、更早 EOL；calVer YY.MM.PP） | src.nvidia.gpu-operator-platform-support-25.3（NEW） | [platform-support.html@25.3](https://docs.nvidia.com/datacenter/cloud-native/gpu-operator/25.3/platform-support.html) 节 NVIDIA GPU Operator Versioning / Life Cycle（"Upgrades are only supported within a major release or to the next major release"；25.3.x GA、24.9.x Maintenance、24.6.x 及以下 EOL）/ GPU Operator Component Matrix 指引 | 跨两个及以上 major 的升级路径无官方说明（unknown） |
| GPU Operator 25.3 配套矩阵（K8s 1.29—1.33、OS/内核、容器运行时 containerd 1.6–2.1/CRI-O、预编译驱动分支 R535/R570/R580、支持 GPU 型号表） | src.nvidia.gpu-operator-platform-support-25.3（NEW） | 同页节 Supported Operating Systems and Kubernetes Platforms / Supported Precompiled Drivers / Supported Container Runtimes / Supported NVIDIA Data Center GPUs and Systems | 表内脚注含已知问题（570.124.06 等 MIG 混合调度 Pending，建议降级 570.86.15）；vGPU/KubeVirt/GDS 等子表未逐条展开 |
| GPU Operator 算子升级流程（Helm 升级；CRD 不能由 Helm 自动升→手动 apply 三 CRD（clusterpolicies/nvidiadrivers/NFD）或 pre-upgrade hook（v22.09 起有、v24.9.0 起默认开）；hook 用算子镜像、拉取失败则 hook 失败需 --no-hooks 删除；ClusterPolicy 支持 kubectl edit 动态更新；PSA 命名空间需 privileged） | src.nvidia.gpu-operator-upgrade-25.3（NEW） | [upgrade.html@25.3](https://docs.nvidia.com/datacenter/cloud-native/gpu-operator/25.3/upgrade.html) 节 Prerequisites / Using Helm（Option 1/Option 2）/ Cluster Policy Updates / Additional Controls for Driver Upgrades（指向 GPU Driver Upgrades）/ Using OLM in OpenShift | 算子本体 helm rollback/回退节该页无（unknown）；示例 RELEASE_TAG=v25.3.4 |
| GPU 驱动容器化升级的滚动条件与观测（驱动 daemonset 特殊：须停客户端→卸载内核模块→换新 pod→加载新模块→恢复客户端；只管容器化驱动不管宿主预装；upgrade controller 默认开；状态机 upgrade-required→cordon→wait-for-jobs→pod-deletion→（drain）→pod-restart→validation（operator-validator）→uncordon→done/failed；maxParallelUpgrades 默认 1、maxUnavailable 默认 25%（含已 cordon 节点占额度）；waitForCompletion/gpuPodDeletion（300s 后强删）/drain（默认关）三门槛；autoUpgrade=false 暂停、节点标签 skip；Prometheus 指标六项与 GPUDriverUpgrade 事件；失败后置 upgrade-required 重试；备选 k8s-driver-manager（initContainer，无状态机观测）；daemonsets.updateStrategy=OnDelete 手工控波次） | src.nvidia.gpu-operator-upgrade-25.3（NEW） | [gpu-driver-upgrades.html@25.3](https://docs.nvidia.com/datacenter/cloud-native/gpu-operator/25.3/gpu-driver-upgrades.html) 节 About Upgrading the GPU Driver / Upgrades with the Upgrade Controller（Procedure、Configuration Options、Upgrade State Machine、Pausing、Skipping、Metrics and Events、Troubleshooting）/ Upgrades without the Upgrade Controller | 驱动「回退/降级」无专门节；仅 platform-support 脚注以 downgrade 570.86.15 作已知问题绕行措辞；validation 具体内容（operator-validator 检查项）未展开 |
| MindCluster 版本配套与混用禁令（26.1.0↔CANN 9.1.0↔HDK 分产品 25.7.RC1/25.1.RC1/25.6.RC1/其他 26.1.0↔MindSpeed-LLM 26.1.0↔TorchNPU 26.1.0↔MindSpore 2.10.0；「各组件需要配套使用，请勿跨版本混用」；兼容表 CANN 8.5.X/9.0.X/9.1.X 与 HDK 25.5.X/26.0.X/26.1.X 等） | src.ascend.mind-cluster-upgrade-v26.1.1（NEW） | [docs/zh/release_notes.md@44385c13](https://github.com/Ascend/mind-cluster/blob/44385c13d7b1d87def35f1604e8be4d16de6ca4e/docs/zh/release_notes.md) 节 版本配套说明（表 1–6）/ 版本使用注意事项（无）/ 更新说明（关键特性变更：deviceResetTimeout 60s→600s 等）/ 升级影响（升级过程影响「无」；升级后 Infer Operator 日志目录需 root 权限）/ 遗留问题（gloo 段错误概率约 0.00125 等） | 文档产品版本字段为 26.1.0（tag 为 v26.1.1）；配套表不含 K8s/OS 内核矩阵 |
| MindCluster Helm 升级与回退（可跨大版本 7.x→26.x；仅 Helm 3.x；Helm 可升组件八款清单，Docker Runtime/Container Manager/TaskD/MindIO 走手动；先查 helm list -A 判断是否 Helm 管理；CRD 三组件（Ascend Operator/Volcano/Infer Operator）先升、CRD 变更可能中断工作负载；--dry-run 预检；升级后组件状态确认；异常三选：版本回退/改配置重升/卸载重装（后者中断工作负载）；回退=helm history+helm rollback mindcluster-crds 再 mindcluster（REVISION 递增可追溯）；kubectl 装的先 helm_tool.sh --add-helm-meta-all 纳入管理） | src.ascend.mind-cluster-upgrade-v26.1.1（NEW） | [04_upgrade/menu_upgrade.md](https://github.com/Ascend/mind-cluster/blob/44385c13d7b1d87def35f1604e8be4d16de6ca4e/docs/zh/scheduling/03_installation_guide/04_upgrade/menu_upgrade.md)（目录）＋[02_helm_upgrade.md](https://github.com/Ascend/mind-cluster/blob/44385c13d7b1d87def35f1604e8be4d16de6ca4e/docs/zh/scheduling/03_installation_guide/04_upgrade/02_helm_upgrade.md) 节 升级说明/升级前准备/Helm部署Release实例/Helm升级Release实例/版本回退 | 官方无金丝雀/分批波次说明（Helm 为整 Release 粒度，unknown）；26.1.0 镜像 tag 坑（默认配置只写 v26.1.0、仓库实际为 v26.1.0-ubuntu22.04 等，须自定义配置）为该页明示证据点；values 只升单组件时其他组件 Enabled 须保持否则被删除（NOTICE） |
| MindCluster 手动升级形态与组件级先后（全量升级可跨版本须停训练/推理任务 vs 升级镜像仅同版本不停任务不改权限与启动参数；预检：kubectl get pods -A 查任务、（可选）关 pingmesh、查组件状态；Ascend Docker Runtime 唯一支持 --upgrade 命令行升级（root、升级后重启 docker/containerd、恢复旧版=下载旧包重跑同步骤）；Device Plugin 升级须先将 Docker Runtime 升至 26.1.0+，卸载旧 YAML+DaemonSet 再装新；其余组件（NPU Exporter/Volcano/RDMA plugin/ClusterD/Ascend Operator/Infer Operator/NodeD）卸载重装，回退=卸新装旧；ClusterD 在断点续训任务运行时的例外处理；升级镜像=保持镜像名一致+rollout restart deployment/ds） | src.ascend.mind-cluster-upgrade-v26.1.1（NEW） | [04_upgrade/01_manual_upgrade.md](https://github.com/Ascend/mind-cluster/blob/44385c13d7b1d87def35f1604e8be4d16de6ca4e/docs/zh/scheduling/03_installation_guide/04_upgrade/01_manual_upgrade.md)（两种方式摘要）＋[05_developer_guide/00_installation_deployment/01_upgrade.md](https://github.com/Ascend/mind-cluster/blob/44385c13d7b1d87def35f1604e8be4d16de6ca4e/docs/zh/scheduling/05_developer_guide/00_installation_deployment/01_upgrade.md) 节 升级说明/升级环境检查/升级Ascend Docker Runtime/升级TaskD/升级Container Manager（deploy.sh upgrade，勿用 install 覆盖配置，26.1.0+）/升级Ascend Device Plugin/升级其他组件/升级镜像/Elastic Agent（已日落）升级TaskD | Container Manager 升级脚本示例输出显示 v26.0.0→v26.1.0；TaskD 装在训练镜像内（pip 卸载/安装+docker commit 新 tag）；用户改过源码的场景明示不适用 |
| 硬件代际/拓扑变更档案样例（A3→950 代际：资源名 huawei.com/Ascend910→huawei.com/npu、ring-controller.atlas、schedule_policy/sp-block/ra-block、ASCEND_VISIBLE_DEVICES 字段引用同步变更） | src.ascend.mind-cluster-upgrade-v26.1.1（NEW） | [04_usage/03_basic_scheduling/07_Intergenerational_upgrade.md](https://github.com/Ascend/mind-cluster/blob/44385c13d7b1d87def35f1604e8be4d16de6ca4e/docs/zh/scheduling/04_usage/03_basic_scheduling/07_Intergenerational_upgrade.md) 表 1（YAML 变更参数说明）/ 表 2（YAML 样例链接，指向 gitcode mindcluster-deploy branch_v26.1.0） | 支持「硬件/拓扑变化进变更档案」；样例 YAML 在另一仓库分支（可变定位），本轮未开 |
| 节点验收/回服门槛入口（GPU：dcgmi diag 级别 1–3 作收工前/回服检查、nccl-tests 投产基线；Ascend：ascend-dmi 诊断/压测与产品版本限制） | src.nvidia.gpu-node-triage-2026-10-08（复用）＋src.huawei.mindx-dl-60rc2-ascend-dmi-2026-09-29（复用） | 复用既有登记核对范围（gpu-node-triage 的 Running DCGM Diagnostics/Network Testing 节；ascend-dmi 故障诊断页参数表与限制） | 本轮未重开；两入口均为 latest/厂商页口径，回服阈值本库自定，官方无统一门槛 |
| MindCluster 组件清单与版本维护策略（组件说明、分支维护阶段、版本维护表 v26.0.0/v7.3.0 等、免责声明：开发分支勿用于生产、正式版走 gitcode releases） | src.ascend.mind-cluster-v26.1.1（复用；本轮补充核对） | 本轮经 FetchURL 实开 [README.md@44385c13 raw](https://raw.githubusercontent.com/Ascend/mind-cluster/44385c13d7b1d87def35f1604e8be4d16de6ca4e/README.md)（提取链接目标：版本配套详情=/docs/zh/release_notes.md、集群调度用户指南=docs/zh/scheduling/menu_scheduling_user_guide.md）与 [docs/zh 目录](https://github.com/Ascend/mind-cluster/tree/44385c13d7b1d87def35f1604e8be4d16de6ca4e/docs/zh)（文档目录结构表） | 对既有条目的补充核对记录：README 版本维护表未列 v26.1.1（仅到 v26.0.0/v7.3.0）；blob 渲染页链接目标经 raw 文件确认 |

## unknown 清单

1. GPU Operator 25.3 算子本体回退：所开 upgrade/gpu-driver-upgrades/platform-support/release-notes 四页均无算子回退节；驱动降级仅见 platform-support 脚注 1 的「downgrade the driver to version 570.86.15」绕行措辞，无步骤；驱动升级失败恢复仅见 upgrade-failed 状态＋重打 upgrade-required 标签。
2. K8s 官方降级（downgrade）指引：kubeadm v1.32 页无 downgrade 节；只有失败恢复（幂等重跑、--force、/etc/kubernetes/tmp 备份恢复）。version-skew 页亦未述降级。不得引申出「K8s 支持直接回退」。
3. NVIDIA device plugin / toolkit 与 kubelet、CUDA、驱动的版本配套矩阵（插件侧升级窗口条件）：未取；复用条目 src.nvidia.k8s-device-plugin-v0.20.1 仅 README 级。
4. Ascend 侧 HDK 驱动/固件升级与回退官方资料：本轮未取（hiascend document/detail 动态页有 cookie 墙风险；doc_center/source 静态路径未定位到 HDK 升级章节）；MindCluster 文档只覆盖集群调度组件，不含 HDK/CANN 自身升级。
5. MindCluster 组件升级的波次/灰度能力：官方文档无金丝雀或分批说明；Helm 为整 Release 粒度，手动升级为逐组件卸载重装。不得推测出官方分批机制。
6. Slurm 分步升级中间版本组合到 24.11 的具体验证（除 20.11→22.05→23.11 示例外）：未做。
7. Volcano 上游自身的版本升级/回退资料：未取；MindCluster 内置 Volcano 经 Helm 管理见 MindCluster 升级文档。
8. 各平台「回服」官方验收门槛：均无统一官方门槛；只能引用节点级诊断入口（复用条目）＋本库自定基线。
9. 全部实测（未执行任何升级、未起集群；所有命令为文档引用，非本库验证）。

## 建议登记条目

```yaml
- id: src.kubernetes.version-skew-v1-32
  title: Kubernetes v1.32 Version Skew Policy（静态快照；另观察可变主页）
  url: https://v1-32.docs.kubernetes.io/releases/version-skew-policy/
  kind: documentation
  registered_at: '2026-10-18'
  revision: v1.32 documentation snapshot（页面自述 "no longer actively maintained ... static snapshot"）；2026-10-18 经 FetchURL 实开；同日实开可变主页 https://kubernetes.io/releases/version-skew-policy/（当时最新 1.37、维护分支 1.37/1.36/1.35，示例 1.36→1.37），正文引用以 v1.32 快照为准
  license:
    status: partial
    scopes:
    - scope: Kubernetes website 仓库文档许可声明；main 链接为可变定位
      identifier: CC-BY-4.0
      url: https://github.com/kubernetes/website/blob/main/LICENSE
    notes: 沿用既有 k8s 文档条目（如 src.kubernetes.device-plugins-v1-32）已核对的许可口径，本轮未重开 website LICENSE；仅链接并原创归纳。
  notes: Batch 23（T05-09）取证：Supported versions（维护分支窗口）与 Supported version skew 全组件规则（apiserver HA ±1 minor、kubelet 不新于 apiserver 且可旧 3 minor（<1.25 为 2）、kube-proxy 同 kubelet 且与同节点 kubelet ±3、kcm/scheduler/ccm 不新于 apiserver 且可旧 1、kubectl ±1；HA 混版收窄示例）；Supported component upgrade order（1.31→1.32 示例：apiserver→kcm/scheduler/ccm 无相互顺序→kubelet 可选留旧→kube-proxy 可选留旧；kubelet minor 升级前必须 drain、不支持原地 minor 升级；持续落后 3 minor 阻塞控制面升级的 Warning）。未覆盖：各部署工具的额外限制（页面自述存在）。
- id: src.kubernetes.kubeadm-upgrade-v1-32
  title: Kubernetes v1.32 Upgrading kubeadm clusters（静态快照）
  url: https://v1-32.docs.kubernetes.io/docs/tasks/administer-cluster/kubeadm/kubeadm-upgrade/
  kind: documentation
  registered_at: '2026-10-18'
  revision: v1.32 documentation snapshot；2026-10-18 经 FetchURL 实开；内容覆盖 1.31.x→1.32.x 与 1.32.x→1.32.y，跨 minor 跳过不支持
  license:
    status: partial
    scopes:
    - scope: Kubernetes website 仓库文档许可声明；main 链接为可变定位
      identifier: CC-BY-4.0
      url: https://github.com/kubernetes/website/blob/main/LICENSE
    notes: 同上沿用既有口径；仅链接并原创归纳。
  notes: Batch 23（T05-09）取证：workflow（primary CP→additional CP→workers）；Before you begin（读 release notes、备份、swap 关）；kubeadm upgrade plan/apply/node 分工；首台 CP 后手动升 CNI；drain/uncordon 与 kubelet 重启验证（systemctl status/journalctl）；workers "one node at a time or few nodes at a time"；Verify（kubectl get nodes 全 Ready）；Recovering from a failure state（幂等重跑、apply --force、/etc/kubernetes/tmp 下 kubeadm-backup-etcd 与 kubeadm-backup-manifests 手动恢复 /var/lib/etcd 与 /etc/kubernetes/manifests）；How it works（apply 预检含 skew 强制、控制面组件失败回滚、CoreDNS/kube-proxy/RBAC、证书 180 天续期）；etcd 升级期间 apiserver 请求停顿的规避（先 SIGTERM kube-apiserver）。页面无 downgrade 节（unknown 边界）。未覆盖：Linux/Windows worker 子页细节。
- id: src.slurm.upgrades-24.11.7
  title: Slurm 24.11.7 Upgrade Guide（归档）与 Quick Start Admin 状态节
  url: https://slurm.schedmd.com/archive/slurm-24.11.7/upgrades.html
  kind: documentation
  registered_at: '2026-10-18'
  revision: 24.11.7 archive（upgrades.html 页脚 Last modified 15 January 2025；quickstart_admin.html 页脚 Last modified 14 November 2024）；2026-10-18 经 FetchURL 实开
  license:
    status: unknown
    scopes: []
    notes: SchedMD 站点许可未核对；只链接并原创归纳，未复制手册长段。
  notes: Batch 23（T05-09）取证：Release Cycle（24.05 起 6 个月周期）/ Compatibility Window（24.11 起兼容前三个大版本；23.02–25.11 兼容表；不兼容版本启动即失败须分步，窗口外升级杀作业丢账目）/ EPEL 排除建议 / Pre-Release 风险 / Reverting an Upgrade（daemon 启动即迁移状态与库；回退不识别新状态、拒启；只能备份/镜像/快照恢复且丢失后续；至少恢复 StateSaveLocation 与账目库）/ Minor Upgrades（维护版更宽容但仍须备份）/ Upgrade Procedure（顺序 slurmdbd→slurmctld→slurmd→客户端→重编译插件→测试→归档；等旧 slurmstepd 作业结束；同机多 daemon 须同升）/ Preparation（RELEASE_NOTES/NEWS、配置变更测试环境先行、停机计划、OpenAPI data_parser 移除表与 spec_only 对比）/ Create Backups（StateSaveLocation、sysconfdir、mysqldump 含 --single-transaction 限制）/ slurmdbd（先升、同/高于 slurmctld、首启前台 -D 防 systemd 超时、purge 缩短停机、sacct/sacctmgr 停机期间不可用、MaxDBDMsgs）/ Database Server（MariaDB 10.2.1+ 需 slurmdbd ≥22.05.7）/ slurmctld（调大 SlurmdTimeout/SlurmctldTimeout 并 reconfig 防 DOWN 杀作业）/ slurmd（可与 ctld 同升或分组滚动）/ Customized Plugins（libslurm soname 每大版本递增须重编译、PMI-1/2 例外、ldd 检查法）/ Seamless Upgrades（独立目录+符号链接仅回切二进制）。另开 quickstart_admin.html：Upgrades 节仅回链 Upgrade Guide；Starting the Daemons 的 -c 清状态语义；Configuration 的 StateSaveLocation 部署建议（低时延本地盘、HA 共享盘勿用 NFS、无状态启动取消作业）。未执行任何 Slurm 命令。
- id: src.nvidia.gpu-operator-upgrade-25.3
  title: NVIDIA GPU Operator 25.3 升级文档（upgrade 与 GPU Driver Upgrades 页）
  url: https://docs.nvidia.com/datacenter/cloud-native/gpu-operator/25.3/upgrade.html
  kind: documentation
  registered_at: '2026-10-18'
  revision: 25.3 次版本文档树（URL 级固定；2026-10-18 观察时 upgrade 页示例 RELEASE_TAG=v25.3.4）；同树 gpu-driver-upgrades.html 同轮实开；/latest/ 可变树当时为 26.7.2（仅定位指针，不引正文）
  license:
    status: unknown
    scopes: []
    notes: 公开可读不等于允许全文再分发；本库只链接并作原创归纳，Operator 软件与镜像许可另行核验。
  notes: Batch 23（T05-09）取证：upgrade.html（PSA privileged 前提；Helm 升级两选项——手动 apply clusterpolicies/nvidiadrivers/NFD 三 CRD 或 pre-upgrade hook（v22.09 起、v24.9.0 起默认开、用算子镜像、拉取失败需 --no-hooks 删除）；ClusterPolicy kubectl edit 动态更新；OpenShift 走 OLM）＋ gpu-driver-upgrades.html（驱动升级五步骤（停客户端→卸模块→新 pod→装驱动加载模块→恢复客户端）；只管容器化驱动；upgrade controller 默认开；driver.version patch 触发；状态机十一态含 validation-required（operator-validator）与 upgrade-failed；maxParallelUpgrades 默认 1、maxUnavailable 默认 25% 且已 cordon 节点占额度；waitForCompletion/gpuPodDeletion（默认 300s 强删）/drain（默认关）门槛；autoUpgrade=false 暂停、nvidia.com/gpu-driver-upgrade.skip=true 跳过；六项 Prometheus 指标与 GPUDriverUpgrade 事件；失败重试=重打 upgrade-required 标签；备选 k8s-driver-manager（initContainer、无状态机观测、不再加新特性）；daemonsets.updateStrategy=OnDelete 手工控波次）。未覆盖：算子本体回退节（无，unknown）；driver 降级步骤（无专门节）；operator-validator 具体检查项。
- id: src.nvidia.gpu-operator-platform-support-25.3
  title: NVIDIA GPU Operator 25.3 Platform Support 与 Release Notes（配套矩阵/生命周期/已知问题）
  url: https://docs.nvidia.com/datacenter/cloud-native/gpu-operator/25.3/platform-support.html
  kind: documentation
  registered_at: '2026-10-18'
  revision: 25.3 次版本文档树；2026-10-18 观察时 release notes 顶条 25.3.4（树内最新补丁）；platform-support 与同树 release-notes.html 同轮实开
  license:
    status: unknown
    scopes: []
    notes: 公开可读不等于允许全文再分发；本库只链接并作原创归纳。
  notes: Batch 23（T05-09）取证：Versioning（calVer YY.MM.PP）/ Life Cycle（前一 major 维护、更早 EOL；"Upgrades are only supported within a major release or to the next major release"；25.3.x GA/24.9.x Maintenance/24.6.x- EOL）/ Component Matrix 指引 / 支持 GPU 与系统表（含 GH200 需 open kernel 模块等注）/ OS×K8s 表（裸金属/直通 1.29—1.33；OpenShift 4.12—4.19；各 OS 行）/ 预编译驱动表（Ubuntu 22.04/24.04 × R535/R570/R580）/ 容器运行时表（containerd 1.6–2.1、CRI-O）/ GPUDirect RDMA/Storage 配套（Network Operator 版本）/ KubeVirt/vGPU 表；release-notes.html（25.3.4 顶条：默认驱动 580.82.07；25.3.2 已知问题 CDMM 与 MIG/GDS 不兼容、570.124.06 等 MIG 混合 Pending 建议升 570.172.08；25.3.1 组件版本清单 toolkit v1.17.8/DCGM v4.2.3/device plugin v0.17.2/NFD v0.17.3/GDRCopy v2.5.0）。platform-support 脚注 1 另载 570.x MIG 混合问题绕行建议「downgrade the driver to version 570.86.15」。未逐条展开 vGPU/KubeVirt 子表与全部 Known Issues。
- id: src.ascend.mind-cluster-upgrade-v26.1.1
  title: MindCluster v26.1.1（commit 44385c13）升级与版本配套文档（release_notes 与安装/开发者指南升级章）
  url: https://github.com/Ascend/mind-cluster/blob/44385c13d7b1d87def35f1604e8be4d16de6ca4e/docs/zh/release_notes.md
  kind: repository
  registered_at: '2026-10-18'
  revision: commit 44385c13d7b1d87def35f1604e8be4d16de6ca4e（annotated tag v26.1.1）；2026-10-18 经 FetchURL 实开 raw 与 blob 页；docs/zh/release_notes.md 产品版本字段写 26.1.0
  license:
    status: partial
    scopes:
    - scope: 固定 commit 的 docs 目录文档；第三方素材按各自声明核查
      identifier: CC-BY-4.0
      url: https://github.com/Ascend/mind-cluster/blob/44385c13d7b1d87def35f1604e8be4d16de6ca4e/docs/LICENSE
    notes: docs/LICENSE 由既有条目 src.ascend.mind-cluster-v26.1.1 在同 commit 核对，本轮未重开；仅链接并原创归纳。
  notes: Batch 23（T05-09）取证（全部固定 commit）：release_notes.md（配套表 1–6：26.1.0↔CANN 9.1.0↔HDK 分产品↔MindSpeed-LLM 26.1.0↔TorchNPU 26.1.0↔MindSpore 2.10.0；各组件勿跨版本混用；关键特性变更 deviceResetTimeout 60s→600s 等；升级影响：过程「无」、Infer Operator 日志目录 root 权限；遗留问题 gloo 段错误概率约 0.00125）；scheduling/03_installation_guide/04_upgrade/menu_upgrade.md＋02_helm_upgrade.md（可跨大版本 7.x→26.x；仅 Helm 3.x；八款可 Helm 升级组件清单；helm list -A 判断管理方式；CRD 三组件先升且可能中断工作负载；--dry-run；升级后组件状态确认；异常三选（回退/重升/卸载重装）；版本回退=helm history+helm rollback 先 mindcluster-crds 后 mindcluster；kubectl 安装的以 helm_tool.sh --add-helm-meta-all 纳入管理；26.1.0 镜像 tag 坑；单组件升级时其他 Enabled 须保持）＋01_manual_upgrade.md 与 05_developer_guide/00_installation_deployment/01_upgrade.md（全量升级可跨版本须停任务 vs 升级镜像仅同版本不停任务；预检 kubectl get pods -A/关 pingmesh/查组件；Ascend Docker Runtime 唯一 --upgrade（root、重启 docker/containerd、旧版=旧包重跑）；Device Plugin 须先升 Docker Runtime 至 26.1.0+ 再卸载重装；其余组件卸载重装、回退=卸新装旧；ClusterD 断点续训例外；升级镜像=镜像名一致+rollout restart；Container Manager deploy.sh upgrade（26.1.0+，勿用 install）；TaskD 镜像内 pip 换装+docker commit；用户改过源码不适用）＋04_usage/03_basic_scheduling/07_Intergenerational_upgrade.md（A3→950 代际 YAML 变更表：资源名/schedule_policy/sp-block/ra-block/ASCEND_VISIBLE_DEVICES）。另：README.md raw 实开（版本配套详情=/docs/zh/release_notes.md；版本维护表止于 v26.0.0/v7.3.0；免责声明与 gitcode releases 指针）——对既有条目 src.ascend.mind-cluster-v26.1.1 的补充核对记录。未覆盖：官方波次/灰度说明（无）；Helm 默认 values 全文（02_installation/00_helm_installation.md 未开）；样例 YAML 所在 mindcluster-deploy 仓库（可变分支，未开）。
```
