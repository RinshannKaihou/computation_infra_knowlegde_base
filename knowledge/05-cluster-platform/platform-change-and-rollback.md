---
id: cluster-platform.platform-change-and-rollback
title: 平台组件升级、发布、回退与回服
type: procedure
domain: cluster-platform
status: draft
platforms: [generic]
source_refs:
- src.kubernetes.version-skew-v1-32
- src.kubernetes.kubeadm-upgrade-v1-32
- src.kubernetes.device-plugins-v1-32
- src.kubernetes.node-drain-v1-32
- src.slurm.upgrades-24.11.7
- src.slurm.docs-24.11.7
- src.nvidia.gpu-operator-upgrade-25.3
- src.nvidia.gpu-operator-platform-support-25.3
- src.nvidia.k8s-device-plugin-v0.20.1
- src.ascend.mind-cluster-upgrade-v26.1.1
- src.ascend.mind-cluster-v26.1.1
- src.nvidia.gpu-node-triage-2026-10-08
- src.huawei.mindx-dl-60rc2-ascend-dmi-2026-09-29
updated_at: "2026-10-18"
applicability:
  environment_refs: []
  notes: "未建立环境档案。有限样板：Kubernetes v1.32 快照、kubeadm 升级文档、Slurm 24.11.7 归档、NVIDIA GPU Operator 25.3 文档树、MindCluster v26.1.1（commit 44385c13）。目标环境版本、制品与配套须另行固定。"
verification:
  status: not_verified
  evidence_refs: []
  notes: "仅核对官方升级/版本偏差/回退语义；未执行任何升级、回退或回服，未起集群。文档审阅不能替代演练。"
summary: 以 Kubernetes/Slurm 与 NVIDIA/Ascend 有限版本样板，规划控制面、节点/runtime、driver/plugin 与调度组件变更的预检、波次、观测、失败停发、回退与回服证据；明确可回退与不可直接回退的边界。
related_ids:
- cluster-platform.kubernetes-job-lifecycle
- cluster-platform.slurm-jobs-and-device-resources
- cluster-platform.node-drain-resource-reclamation
- cluster-platform.container-image-runtime-baseline
- hardware.node-acceptance-triage
- software-stack.compatibility-evidence
- training.elastic-training-and-membership
---

# 平台组件升级、发布、回退与回服

> 范围：Kubernetes v1.32 静态快照、Slurm 24.11.7 归档、NVIDIA GPU Operator 25.3 文档树、MindCluster v26.1.1（commit `44385c13`）。本文是变更规划与证据框架，**未执行任何升级或回退**；在版本、制品与配套未固定前，不得据此生成可直接执行的命令序列。

## 目标与触发条件

平台变更通常同时涉及控制面、节点、容器运行时、驱动、设备插件与调度组件。风险不在于“某条命令失败”，而在于：组件之间的版本偏差越界、状态/数据库格式已迁移而无法回退、节点升级后设备不可用、任务在无恢复点的情况下被终止。

本流程回答：**这次变更的当前态与目标态是什么、允许的版本偏差与顺序是什么、哪些步骤可逆、失败时在哪里停下、什么证据才算回服。**

触发条件：Kubernetes/Slurm 版本升级、GPU Operator 或 MindCluster 升级、驱动/固件/插件变更、调度组件（Kueue/Volcano）升级、节点池分批维护。

## 适用范围与前置条件

| 项 | 要求 |
|---|---|
| 版本固定 | 每个组件记录当前版本、目标版本、补丁级与制品来源；未固定的占位版本不得变成命令 |
| 配套矩阵 | NVIDIA GPU Operator 按 25.3 文档树的 K8s/OS/驱动/运行时表核对；MindCluster 按 release notes 的 CANN/HDK/TorchNPU/MindSpore 配套表核对 |
| 备份 | Kubernetes 控制面证书/manifests/etcd 备份路径；Slurm `StateSaveLocation`、配置目录、账目库 dump |
| 维护窗口 | 停机范围、最长中断、允许的作业损失与重跑预算 |
| 回退资产 | 旧镜像/包、旧 CRD、旧 values、旧二进制、数据库/状态快照；没有回退资产就不承诺可回退 |
| 观测 | 节点/组件状态、设备分配、作业进展、网络与存储基线、应用功能/质量/性能 |
| 授权 | 升级、drain、CRD 变更与回退均为高影响操作；本文不授予执行权限 |

**“官方支持升级”不等于“官方支持回退”，两类证据强度还要分开。** Slurm 文档明确写出：**大版本升级中，daemon 首次启动并发生状态文件/数据库 schema 迁移后**，回退（降级）不受支持，只能靠备份/快照恢复；**同一 major 的维护补丁按 `Minor Upgrades` 逐 release 判断，是这条主句的例外，不能推广成“所有补丁一律禁止降级”**。Kubernetes 文档**未提供降级流程**，只有失败恢复（幂等重跑、同版本强制协调、从备份恢复），这是“证据缺失”，不能写成“官方明确禁止降级”，也不能反推支持。NVIDIA 与 MindCluster 文档也没有给出完整的算子/驱动回退步骤。

## 需要的证据（变更档案）

每次变更先建立一份档案，至少包含：

```text
当前/目标制品: {组件, 版本, 补丁级, 镜像/包 digest, CRD/values 版本}
配置差异: {配置项, 旧值, 新值, 是否影响默认行为}
配套/版本偏差: {K8s skew, Slurm 兼容窗口, CANN/HDK/TorchNPU, GPU Operator 矩阵}
硬件/拓扑: {机型, 驱动/固件, 网卡, 存储, 超节点/rail}
作业/恢复点: {在跑作业, Checkpoint, 可重排队, 最长中断}
回退资产: {旧制品, 旧 CRD, 备份路径, 快照时间, 恢复演练记录}
波次与门槛: {批次, 每批节点/组件, 观测窗口, 停发条件}
```

| 证据 | 采集范围或定位 | 用途 | 缺失时如何处理 |
|---|---|---|---|
| 版本偏差 | K8s 各组件版本；Slurm daemon/客户端/插件版本；GPU Operator/驱动/CUDA；MindCluster 组件/CANN/HDK | 判断是否越过官方 skew/兼容窗口 | 越界即停，不靠“试一下” |
| 官方变更说明 | Kubernetes release notes、Slurm `RELEASE_NOTES`/`NEWS`、GPU Operator release notes、MindCluster release notes | 发现配置变更、移除项、已知问题 | 未读变更说明不进入波次 |
| 备份与快照 | etcd/manifests、`StateSaveLocation`、`slurmdbd` 数据库、CRD/values | 提供恢复点 | 无备份不承诺回退 |
| 当前健康基线 | 节点 Ready、设备 allocatable、作业成功率、网络/存储指标 | 与升级后对比 | 基线缺失则回服判断降级为未知 |
| 升级过程状态 | 组件 condition、事件、驱动升级状态机、Helm revision | 判断停发或继续 | 只看“pod running”不足 |
| 应用证据 | 训练 step、推理请求、数据读回、通信测试 | 证明功能与进展 | 不用“组件启动成功”替代 |

## 步骤与判断分支

### 1. 预检

| 平台 | 必查项 | 证据 | 不通过时 |
|---|---|---|---|
| Kubernetes | version skew（含 HA 混版交集）、节点全 Ready、控制面健康、swap 关闭、证书与备份、etcd 部署形态 | `kubeadm upgrade plan` 类预检、节点状态、备份目录、local/stacked vs external etcd 记录 | 修正偏差或推迟；external etcd 无匹配备份时停 |
| Slurm | 兼容窗口、`RELEASE_NOTES`/`NEWS`、配置变更、OpenAPI 变更、备份三件套、升级前在跑作业 | [Upgrade Guide](https://slurm.schedmd.com/archive/slurm-24.11.7/upgrades.html) | 分步升级或先补备份；旧 stepd 作业未清时不能宣布完成 |
| GPU Operator | 生命周期（同 major 或下一 major）、K8s/OS/驱动/运行时矩阵、CRD 处理方式、驱动归属（容器化/宿主预装） | [Platform Support 25.3](https://docs.nvidia.com/datacenter/cloud-native/gpu-operator/25.3/platform-support.html) | 跨两个 major 或宿主预装驱动无匹配方案时停 |
| MindCluster | 版本配套表、组件混用禁令、Helm/手动管理方式、CRD 顺序 | [release notes](https://github.com/Ascend/mind-cluster/blob/44385c13d7b1d87def35f1604e8be4d16de6ca4e/docs/zh/release_notes.md) | 配套不符，停 |

Kubernetes 的 skew 规则（[version skew policy v1.32](https://v1-32.docs.kubernetes.io/releases/version-skew-policy/)）：apiserver HA 内 ±1 minor；kubelet 不得新于 apiserver、可旧 3 个 minor；kcm/scheduler/ccm 不得新于 apiserver、可旧 1；kubectl ±1；**kube-proxy 有两类独立约束：不得新于 apiserver、最多旧 3 个 minor，同时与同节点 kubelet 相差不超过 3 个 minor（上下界）**。升级顺序为 apiserver → kcm/scheduler/ccm（三者间无顺序）→ kubelet（可选）→ kube-proxy（可选）；kubelet minor 升级前必须 drain，且不支持原地 minor 升级；kubelet/kube-proxy 持续落后 3 个 minor 会阻塞后续控制面升级。**这里的顺序是 policy 的组件依赖顺序，不等于 kubeadm 的节点级执行单元**；部署工具可能施加更严格条件，不能把两者合成为可任意拆分的执行清单。

**混版期间要取所有可达 apiserver 的允许交集，不能按某一台已升级实例判断。** 官方示例：apiserver 为 1.31/1.32 时，kubelet/kube-proxy 不能升到 1.32；经负载均衡访问两版 apiserver 的 kcm/scheduler/ccm 仍只能为 1.31。规则反例（用于定向验证，不是现场记录）：apiserver 为 1.31/1.32、同节点 kubelet 为 1.31 时，kube-proxy 1.28 虽满足“与 kubelet 相差不超过 3 版”，却不满足“不新于 apiserver、最多旧 3 个 minor”的 apiserver 约束；允许集合是 1.29/1.30/1.31。升级前应把“当前可达 apiserver 版本集合”写进档案，并据此限制提前升级的组件。

Slurm 的兼容窗口与不可回退边界：24.11 起兼容前三个大版本；不兼容版本启动即失败，须分步升级。**大版本升级中，daemon 首次启动通常会迁移状态文件/数据库结构（具体以该 release 的 Upgrade Guide 为准）；一旦发生迁移，回退旧版不识别新状态，只能靠备份/镜像/快照恢复，且会丢失备份后的变更**（[Upgrade Guide](https://slurm.schedmd.com/archive/slurm-24.11.7/upgrades.html)）。升级顺序为 slurmdbd → slurmctld → slurmd → 客户端 → 重编译插件；slurmd 可分组滚动，升级期间应调大 `SlurmdTimeout`/`SlurmctldTimeout` 并 reconfig，避免节点被标 DOWN 杀作业。**完成门槛还要等升级前已运行的作业结束**：这些作业仍使用旧 `slurmstepd`，不能仅凭 daemon/客户端版本清单和新作业能启动就宣布升级完成。同一 major 内的维护补丁按 `Minor Upgrades` 逐 release 判断，不套用大版本“不可原地降级”的绝对结论。

### 2. 波次与观测

| 平台 | 波次形态 | 停发/观测点 | 备注 |
|---|---|---|---|
| Kubernetes | 首台控制面 → 其余控制面 → 工作节点逐台或小批 | 每台后看节点 Ready、组件版本、核心 Pod、CNI | CNI 需手动升级；kubelet 升级前 drain |
| Slurm | slurmdbd → slurmctld → slurmd 分组 → 客户端 → 插件 | 每批后看节点注册、作业启动、`sacct`、DBD 队列 | slurmdbd 先升且同/高于 slurmctld |
| GPU Operator | 容器化驱动升级控制器按 `maxParallelUpgrades`/`maxUnavailable`；非 controller 路径（如 `OnDelete`）单独说明 | 状态机 `upgrade-failed`/`validation`、GPUDriverUpgrade 事件、指标 | 宿主预装驱动不在 controller 覆盖范围；已 cordon 节点占 `maxUnavailable` 额度 |
| MindCluster | Helm 整 Release 或手动逐组件 | CRD 组件先升（可能中断负载）、组件状态、任务 | 官方无金丝雀/分批说明；Helm 是整 Release 粒度 |

GPU Operator 的驱动升级有十一个状态（含 `Unknown` 空态），流转链为：`upgrade-required` → cordon → wait-for-jobs → pod-deletion →（可选 drain）→ pod-restart → validation → uncordon → done/failed。**该机制只管理 GPU Operator 部署的容器化驱动，不管理宿主预装驱动**；宿主预装驱动需另立方案，未知时停止。波次前门禁必须记录实际生效值：`maxParallelUpgrades=1`；`maxUnavailable=25%`（已 cordon 节点占额度）；`waitForCompletion` 的 `podSelector` 与超时（默认空选择器＝不等待任何 Pod）；`gpuPodDeletion` 的 300 秒超时、`force` 与 `deleteEmptyDir`（默认 `false`；改为 `true` 会删除 emptyDir 数据）及其超时后的强删后果；`drain` 是否启用及其有效配置；每个作业的恢复点。`force=false` 表示不处理无控制器管理的 Pod，**不是“永不强删”的总开关**；等待超时后仍可能强删。失败节点落到 `upgrade-failed`；**排障后由人工**把它置回 `upgrade-required` 才会重试，控制器不会自动重试；任一阶段失败都进入停发/调查分支，不要求 validation 连败（[GPU Driver Upgrades 25.3](https://docs.nvidia.com/datacenter/cloud-native/gpu-operator/25.3/gpu-driver-upgrades.html)）。非 controller 的 `OnDelete` 或 `k8s-driver-manager` 路径能力不同，不能当作同一状态机使用。

MindCluster 的 Helm 升级可跨大版本（7.x→26.x），但 CRD 三组件（Ascend Operator、Volcano、Infer Operator）先升且 CRD 变更可能中断工作负载。手动升级要按组件与方式区分：**全量跨版本升级要求停止训练/推理任务**；**同版本镜像升级不停任务，但只允许同版本，不改变权限与启动参数，且不适用于 TaskD**（TaskD 在训练镜像内用 pip 换装并提交新镜像 tag）。Ascend Docker Runtime 是唯一支持 `--upgrade` 的组件；**Container Manager 在 26.1.0+ 用 `deploy.sh upgrade` 保留配置，官方明确警告不要用 `install`（会覆盖配置）**；Device Plugin 的推荐前提是先升 Runtime 至 26.1.0+，但在未升级/未使用 Runtime/非默认挂载路径时另有配置 mounts 的条件分支。“其余组件按卸载旧、安装新处理”只适用于相应组件章节且条件成立的常规路径；运行断点续训任务时 ClusterD 有特殊处理，本文不覆盖该场景，须另立方案。手动回退也不统一承诺“卸新装旧”，需按组件与制品逐项确认（[Helm 升级](https://github.com/Ascend/mind-cluster/blob/44385c13d7b1d87def35f1604e8be4d16de6ca4e/docs/zh/scheduling/03_installation_guide/04_upgrade/02_helm_upgrade.md)、[手动升级](https://github.com/Ascend/mind-cluster/blob/44385c13d7b1d87def35f1604e8be4d16de6ca4e/docs/zh/scheduling/03_installation_guide/04_upgrade/01_manual_upgrade.md)、[开发者指南升级](https://github.com/Ascend/mind-cluster/blob/44385c13d7b1d87def35f1604e8be4d16de6ca4e/docs/zh/scheduling/05_developer_guide/00_installation_deployment/01_upgrade.md)）。

### 3. 失败停发与恢复

| 平台 | 停止条件 | 可用的恢复路径 | 不可承诺的能力 |
|---|---|---|---|
| Kubernetes | skew 越界、控制面不健康、节点升级后不 Ready、CNI 异常 | 幂等重跑、`apply --force` 同版本恢复、从 `/etc/kubernetes/tmp` 恢复 `kubeadm-backup-etcd`（**仅 local/stacked etcd**）与 `kubeadm-backup-manifests`；external etcd 需另有匹配备份 | 官方无 downgrade 流程；不得写“可回退到旧 minor”；external etcd 的空备份目录不能当恢复点 |
| Slurm | 兼容窗口外、配置/插件不兼容、DB 迁移后异常、作业损失超预算 | 从未启动新 daemon 的备份/快照恢复；恢复 `StateSaveLocation` 与账目库；同一 major 维护补丁按 `Minor Upgrades` 逐 release 判断 | **大版本或已发生状态/schema 迁移后**无原地降级；维护补丁逐 release 核验；Seamless 只回切二进制，不回迁状态 |
| GPU Operator | 跨两个 major、任一阶段进入 `upgrade-failed`、validation 失败、节点不可用 | 排障后**人工**置回 `upgrade-required` 重试；`autoUpgrade=false` 暂停；按节点 skip | 官方无算子本体回退节；驱动降级只有已知问题绕行措辞，无通用步骤 |
| MindCluster | 配套不符、CRD 升级中断负载、组件状态异常 | Helm `history`+`rollback`（先 `mindcluster-crds` 再应用）：**两个 Release 分别核对 history、目标 revision、对应版本/配置/可用制品，以及与升级前状态的匹配证据；两个 revision 号不能仅凭数字相同就认定配套**。首次纳管/无历史时转备份恢复或重建；手动回退按组件逐项确认 | 官方无波次/灰度说明；不能假定 Helm 回退会回迁 CRD 数据；不统一承诺“卸新装旧” |

### 4. 回服门槛

回服不是“组件进程起来”，而是跨层证据齐备。每一层都必须给出**通过 / 失败 / 未知**三态：

| 层 | 通过门槛 | 未通过/未知处置 | 证据入口 |
|---|---|---|---|
| 节点/设备 | 节点 Ready/IDLE；设备 allocatable；插件在 kubelet/runtime 重启后已重新注册；受控新任务完成一次“请求→分配→容器可见稳定身份→使用→释放”的账本核对 | 未重注册、分配身份不一致或无法核对 → 失败/未知，保持隔离 | 节点状态、设备插件、PodResources、`nvidia-smi`/`npu-smi`、GRES |
| 数据/存储 | 卷可挂载、Checkpoint/数据集可读回、校验通过 | 读回失败或校验缺失 → 失败/未知，不开放生产准入 | PVC/VolumeAttachment、读回记录、校验和 |
| 网络/通信 | 链路与集合通信基线恢复，无持续重传/超时 | 基线缺失或测试未完成 → 记未知，不得计入通过 | NIC 计数、通信测试、拓扑 |
| 应用功能 | 训练 step 持续推进、推理请求成功、输出质量达标 | 未跑受控任务或无质量对照 → 未知 | 训练日志/step、请求成功率、质量对照 |
| 性能 | 吞吐/尾延迟回到基线噪声带内 | 无基线或样本不足 → 未知；不得用“组件正常”代替 | 基线对照、SLO |
| 变更一致性 | 所有节点/组件版本与档案一致，无混合残留；升级前旧 `slurmstepd` 作业已结束 | 存在混合残留 → 失败，停发下一波次 | 版本清单、组件状态、作业/stepd 清单 |

节点级验收入口可复用[节点验收与首启排查](../01-hardware/node-acceptance-triage.md)与[兼容性与版本边界证据](../02-software-stack/compatibility-evidence.md)；GPU 侧可复用 DCGM 诊断与 NCCL 基线的既有登记（`src.nvidia.gpu-node-triage-2026-10-08`），Ascend 侧可复用 ascend-dmi 诊断（`src.huawei.mindx-dl-60rc2-ascend-dmi-2026-09-29`）。节点回收与设备释放证据见[节点摘除、drain 与资源回收流程](node-drain-resource-reclamation.md)，变更后应接收其“旧执行退出、分配释放、账本一致”的记录。这些入口只提供检查方法，**不构成官方统一的回服门槛**，阈值须由本库基线或现场 SLO 决定。

**三态判定规则**：通过＝证据齐备且与基线对比；失败＝有明确异常，保持隔离并停发；未知＝必需证据缺失、基线不存在、检查被跳过或无法解释。**未知项不得计入通过，也不得宣布回服**；受控验证（限定节点/镜像/设备身份的探针任务）通过后，才允许另行开放全面生产准入。

## 停止条件与恢复安排

立即停止发布并保留现场的条件：

- 版本偏差越过官方 skew/兼容窗口，或组件出现不兼容错误。
- 控制面/调度器/数据库不可用，或备份不可用。
- Slurm daemon 已启动并迁移状态，但回退资产不完整。
- GPU Operator 驱动升级在任一阶段进入 `upgrade-failed`（不要求 validation 连败），或节点不可用。
- MindCluster CRD 升级导致工作负载中断超出预算。
- 设备、卷、网络或应用 SLO 出现不可接受的退化。

停止后先冻结波次、保存版本/事件/日志/状态快照，再决定“重试、回退或重建”。**任何回退都要重新走预检与回服门槛**，不能因为“回到了旧版本”就宣布恢复。“重建”不是回退的默认替代：只有在回退资产不完整且状态/格式已迁移、无法可靠恢复时，才进入重建；重建后必须重走节点验收与完整回服门槛，并说明数据/作业恢复点。

## 完成判据

- 变更档案完整：当前/目标制品、配置差异、配套矩阵、硬件拓扑、作业恢复点、回退资产（含 etcd 类型与 Helm revision 历史）、波次与门槛。
- 每个波次都有观测窗口与停发记录；失败项有明确的停止/重试/回退/重建分支。
- 回服证据覆盖节点/设备、数据、网络、应用功能与性能，且与基线对比；**每一层都有通过/失败/未知三态，未知不计入通过**。
- 设备门槛包含“受控新任务请求→分配→容器可见身份→使用→释放”的账本核对；升级前旧 `slurmstepd` 作业已结束，无混合残留。
- 明确记录“不可回退/无官方 downgrade/需人工重试”的边界与已知未知项；不把模型审阅、文档核对或组件启动当作演练成功。
- 真实演练结果另立证据；本文与审阅报告都不构成“已升级/已回退/已回服”的证明。

## 来源与验证记录

- [Kubernetes v1.32 — Version Skew Policy](https://v1-32.docs.kubernetes.io/releases/version-skew-policy/)
- [Kubernetes v1.32 — Upgrading kubeadm clusters](https://v1-32.docs.kubernetes.io/docs/tasks/administer-cluster/kubeadm/kubeadm-upgrade/)
- [Slurm 24.11.7 — Upgrade Guide](https://slurm.schedmd.com/archive/slurm-24.11.7/upgrades.html)
- [NVIDIA GPU Operator 25.3 — Upgrade](https://docs.nvidia.com/datacenter/cloud-native/gpu-operator/25.3/upgrade.html)
- [NVIDIA GPU Operator 25.3 — GPU Driver Upgrades](https://docs.nvidia.com/datacenter/cloud-native/gpu-operator/25.3/gpu-driver-upgrades.html)
- [NVIDIA GPU Operator 25.3 — Platform Support](https://docs.nvidia.com/datacenter/cloud-native/gpu-operator/25.3/platform-support.html)
- [MindCluster v26.1.1 — Release Notes](https://github.com/Ascend/mind-cluster/blob/44385c13d7b1d87def35f1604e8be4d16de6ca4e/docs/zh/release_notes.md)
- 当前验证范围：未执行。待确认：GPU Operator 算子回退与驱动降级步骤、K8s 官方降级指引、Ascend HDK/CANN 自身升级回退、Slurm 分步升级组合、各平台统一回服门槛。
