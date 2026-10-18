# Batch 23 · T05-09 独立技术审阅

## 审阅元数据

| 项 | 记录 |
|---|---|
| 任务 | T05-09「平台组件升级、发布、回退与回服」，procedure |
| 角色 | 本会话 Codex，独立审阅者；不是正文作者，不重写正文 |
| 实际模型 | **精确底层模型 ID 与推理档位：unknown。** 当前接口及可读的模型环境变量未暴露该信息；不能把仓库约定的 `gpt-6.1-sol / xhigh` 冒记为实际执行模型。本轮未另启 CLI 模型或子代理 |
| 模型审计边界 | 未取得执行器返回的模型/路由元数据，不能完成“实际为单一指定模型、无 fallback”的核验；本报告不作为该模型身份验收已通过的证明 |
| 时间 | 2026-10-18，Asia/Shanghai（UTC+08:00）；本轮首个显式时钟记录为 16:26:03，收尾输入哈希核对为 16:42:09 |
| 轮次 | 第 1 轮独立技术初审；尚无作者修订、定向复核或关闭项 |
| 取证方式 | 本地文件只读检查、原文件行号定位、远程精确 URL 实开；网页读取无正文时改用可用的网页连接器；GitHub 连接器读取官方仓库固定 commit 的原文件与 tag 对象。不以搜索摘要或来源记录代替上游原文 |
| 写入范围 | 只新增本报告；正文、来源记录、登记表、计划、邻近正文均不修改；不操作集群、节点、数据库或制品 |

### 文件清单与审阅对象

- 主审：[platform-change-and-rollback.md](../../knowledge/05-cluster-platform/platform-change-and-rollback.md)，本文以下“正文”均指此文件；初审共 172 行。
- 来源记录：[batch-23-t05-09-sources.md](batch-23-t05-09-sources.md)。
- 任务及规范：[full-coverage-backlog.yaml](../../plans/full-coverage-backlog.yaml) 的 T05-09、[README.md](../../README.md)、[authoring-guide.md](../authoring-guide.md)、[content-outline.md](../../content-outline.md)、[content.schema.json](../../schemas/content.schema.json)。
- 登记核对：[registry.yaml](../../sources/registry.yaml) 中用户指定的八项：`src.kubernetes.version-skew-v1-32`、`src.kubernetes.kubeadm-upgrade-v1-32`、`src.slurm.upgrades-24.11.7`、`src.nvidia.gpu-operator-upgrade-25.3`、`src.nvidia.gpu-operator-platform-support-25.3`、`src.ascend.mind-cluster-upgrade-v26.1.1`、`src.nvidia.gpu-node-triage-2026-10-08`、`src.huawei.mindx-dl-60rc2-ascend-dmi-2026-09-29`；另检查正文全部 `source_refs`、`related_ids`。
- 邻近正文：[T05-08 节点摘除与资源回收](../../knowledge/05-cluster-platform/node-drain-resource-reclamation.md)、[容器镜像与运行时基线](../../knowledge/05-cluster-platform/container-image-runtime-baseline.md)、[节点验收](../../knowledge/01-hardware/node-acceptance-triage.md)、[兼容性证据](../../knowledge/02-software-stack/compatibility-evidence.md)，重点对照生命周期、设备分配、证据缺项和回服判定。

主审输入 SHA-256：

| 文件 | SHA-256 |
|---|---|
| `knowledge/05-cluster-platform/platform-change-and-rollback.md` | `6e3b9f4f86b4276144baadbbce2fc9c2e205363154bb330bd5bab3d0d8ca952a` |
| `docs/research/batch-23-t05-09-sources.md` | `307103073b53db235a8b307933841cfc39e2760a4f464b69fba3393eeb4eaec8` |

工作树开始时已有 Batch 23 正文、来源记录等未跟踪文件，以及 `knowledge/05-cluster-platform/index.md`、`sources/registry.yaml` 的既有修改；这些不是本次审阅产生的修改，不回退、不覆盖。收尾时另观察到其他任务的报告文件及登记表变化；本轮工具写入仍只有本报告。16:42:09 核对时，主审正文、来源记录和任务计划哈希未变；登记表哈希由 `071161e0bcaeef4466e854ad09d3f45a04892be7456d15244f05f3d62eea1e0e` 变为 `c2f1fad836ddfa72105f54f028d6a094d0bc9107c9a36bc7bbbfefdd61bf4b25`，不把此外部变化归因于本次审阅，也不宣称整个工作树静止。

## 结论

**需修订后定向复核，不通过本轮技术审阅。** 共 9 项开放发现：**P1 0 项、P2 8 项、P3 1 项**。优先修正驱动失败重试语义、MindCluster 路径前提及恢复/回服门禁。模型身份审计另有未完成项，见元数据与局限。

已满足或基本准确的部分：

- 变更档案已包含当前/目标制品、配置、配套、硬件/拓扑、作业恢复点、回退资产和波次字段；正文没有成段可直接执行的升级/回退命令序列。第 71–79 行是明确的档案字段结构，不是漏填模板。`apply --force`、`--upgrade` 等为语义片段，不能据此认定已提供完整执行处方。
- Kubernetes 只给失败恢复、不承诺旧 minor 降级的保守边界合理；Slurm 大版本升级后 daemon 启动即涉及状态/数据库结构更新、恢复备份会丢失之后变更的主线有官方证据。维护补丁级限定见 C08。
- GPU Operator 同一 major 内或到下一 major 的升级范围与 25.3 支持页一致；不能把这个范围改写成支持跨多个 major 或支持降级。MindCluster 的 CRD Release 先于应用 Release 回退顺序与固定源码一致。
- 正文已经覆盖预检、波次、观测、停发、恢复以及数据/网络/通信、应用功能/质量/性能的检查维度；也明确模型审阅、文档核对不能代替真实演练。问题在于若干路径前提和门禁尚未闭合，而非完全没有流程。

## 逐条上游取证

本节所有“本轮观察”日期均为 **2026-10-18**。URL 含版本不等于获取了不可变网页字节；页面内最后修改日期、tag 日期与本轮访问日期分别记录。

### Kubernetes

- **U01 — [Version Skew Policy · v1.32](https://v1-32.docs.kubernetes.io/releases/version-skew-policy/)**：实开成功，页面自述 v1.32 静态快照、停止维护。核对各组件 skew、HA 混版收窄、升级顺序与 kubelet drain 要求。正文示例为 1.31→1.32；页面 Supported versions 行却列 1.36/1.35/1.34，不能据此把 v1.32 当当前受维护版本。另实开[可变主页](https://kubernetes.io/releases/version-skew-policy/)，其维护分支为 1.37/1.36/1.35，与来源记录本轮观察一致；本报告技术规则仍取 v1.32 页。
- **U02 — [Upgrading kubeadm clusters · v1.32](https://v1-32.docs.kubernetes.io/docs/tasks/administer-cluster/kubeadm/kubeadm-upgrade/)**：实开成功。核对 1.31.x→1.32.x / 1.32.x→1.32.y 的范围、控制面与节点顺序、CNI、恢复节。恢复节允许重跑、同版本强制协调及特定备份恢复；没有在该页取得通用 downgrade 流程。特别核实 local etcd 备份与 external etcd 空目录的区别。
- **U15 — [Device Plugins · v1.32](https://v1-32.docs.kubernetes.io/docs/concepts/extend-kubernetes/compute-storage-net/device-plugins/)**：补充实开成功。核对 Handling kubelet restarts、Allocate/注册次序、unhealthy 对 allocatable 的影响及 PodResources 的职责；这支持 C09 的设备分配门禁，不构成某个厂商插件版本已配套的证明。

### Slurm

- **U03 — [Upgrade Guide · 24.11.7 归档](https://slurm.schedmd.com/archive/slurm-24.11.7/upgrades.html)**：已按精确 URL 尝试实开，网页连接器返回 `Internal Error`；本地 `curl` 返回 `Could not resolve host: slurm.schedmd.com`。**未读到该站归档页，不能记录为 HTTP 200 或已核验其部署字节。**
- **U04 — [Quick Start Administrator Guide · 24.11.7 归档](https://slurm.schedmd.com/archive/slurm-24.11.7/quickstart_admin.html)**：精确 URL 实开同样返回 `Internal Error`；独立 HTTP 读取亦失败。该 URL 的网页层证据仍为 unknown。
- **U03-S / U04-S — 同 release 官方源码补证**：通过 SchedMD 官方仓库 tag 查询取得 `slurm-24-11-7-1`，tag 对象 `9d1ef1877186d8101769352831c8f0fe303df31c` 指向 commit `defaf214db2e55326f45ab08f1bde5b2036d9f5d`；tag 消息明确为 24.11.7 release，tagger 日期为 2025-11-11。随后实读固定 commit 的 [doc/html/upgrades.shtml](https://github.com/SchedMD/slurm/blob/defaf214db2e55326f45ab08f1bde5b2036d9f5d/doc/html/upgrades.shtml) 与 [doc/html/quickstart_admin.shtml](https://github.com/SchedMD/slurm/blob/defaf214db2e55326f45ab08f1bde5b2036d9f5d/doc/html/quickstart_admin.shtml)，不是用当前 master 替代旧版本。
  - upgrades 源文件核对 Compatibility Window、Reverting an Upgrade、Minor Upgrades、Upgrade Procedure、备份、各 daemon、custom plugins、Seamless Upgrades；文件页脚确为 2025-01-15。
  - quickstart 源文件核对 Configuration/StateSaveLocation、Starting the Daemons 的状态恢复与清状态风险、Upgrades 回链；文件页脚确为 2024-11-14。
  - 以上能独立支持 release 文档内容判断，**不能证明不可访问的归档网页与该 commit 字节完全一致**。所列页脚日期是源码内声明，不是本轮访问时间或 24.11.7 发布日期。

### NVIDIA GPU Operator

- **U05 — [Upgrade · 25.3](https://docs.nvidia.com/datacenter/cloud-native/gpu-operator/25.3/upgrade.html)**：实开成功。核对手动更新 CRD / Helm pre-upgrade hook 两路径与 PSA 条件；当前示例为 `RELEASE_TAG=v25.3.4`。这些是上游示例，不是已为本地环境选定的版本。
- **U06 — [GPU Driver Upgrades · 25.3](https://docs.nvidia.com/datacenter/cloud-native/gpu-operator/25.3/gpu-driver-upgrades.html)**：实开成功。核对容器化驱动管理范围、controller 状态、波次参数、等待/删除/drain 默认值、暂停/跳过、故障处理与非 controller 路径；关键定位为 About Upgrading、Configuration Options、Upgrade State Machine、Troubleshooting、Upgrades without the Upgrade Controller。
- **U07 — [Platform Support · 25.3](https://docs.nvidia.com/datacenter/cloud-native/gpu-operator/25.3/platform-support.html)**：实开成功。核对生命周期、同/下一 major 限制及 OS/K8s/runtime 矩阵。Supported Container Runtimes 表列 containerd 1.6–2.1，不能与邻近正文其他 runtime 样板自动拼成已支持组合。
- **U08 — [Release Notes · 25.3](https://docs.nvidia.com/datacenter/cloud-native/gpu-operator/25.3/release-notes.html)**：实开成功，首条为 25.3.4，默认驱动列 580.82.07；抽核 25.3.2/25.3.1 的组件与已知问题。25.3 树未锁到网页内容哈希，观察结论不外推为永久状态。

### MindCluster

- **U09 — [release_notes.md · 固定 commit](https://github.com/Ascend/mind-cluster/blob/44385c13d7b1d87def35f1604e8be4d16de6ca4e/docs/zh/release_notes.md)**：通过官方仓库原文件实开成功。独立解析 `v26.1.1` annotated tag，其 tag 对象 `387a7f2b5f9ddfdbcdff0d8c85386fc68e2fe7fb` 指向 `44385c13d7b1d87def35f1604e8be4d16de6ca4e`，tagger 日期 2026-09-15。**该 tag 下版本说明的产品版本仍写 26.1.0**；配套表、组件混用禁令与升级影响均按该原文读取，不把 tag 名偷偷替换进表格。
- **U10 — [使用 Helm 升级 · 同 commit](https://github.com/Ascend/mind-cluster/blob/44385c13d7b1d87def35f1604e8be4d16de6ca4e/docs/zh/scheduling/03_installation_guide/04_upgrade/02_helm_upgrade.md)**：实开成功，重点复读升级说明、管理方式判断、单组件 values 保留要求和“版本回退”。确认 Helm 回退有 Release 升级历史前提，且 CRD/应用分别选 revision。
- **U11 — [手动升级入口 · 同 commit](https://github.com/Ascend/mind-cluster/blob/44385c13d7b1d87def35f1604e8be4d16de6ca4e/docs/zh/scheduling/03_installation_guide/04_upgrade/01_manual_upgrade.md)**：实开成功，明确全量跨版本升级须停任务，升级镜像只限同版本、不能变更权限/启动参数。
- **U12 — [开发者指南：手动升级 · 同 commit](https://github.com/Ascend/mind-cluster/blob/44385c13d7b1d87def35f1604e8be4d16de6ca4e/docs/zh/scheduling/05_developer_guide/00_installation_deployment/01_upgrade.md)**：实开成功；另按原文件第 200–360 行定向核对 Container Manager 与 Device Plugin，确认存在 C03 所列例外，不能只采用章节开头的概括句。

### 既有诊断入口

- **U13 — [NVIDIA GPU Node Triage](https://docs.nvidia.com/deploy/gpu-debug-guidelines/gpu-node-triage.html)**：精确登记 URL 本轮实开成功，核对 Running DCGM Diagnostics、Network Testing。当前页面可见更新日期 2026-10-04；登记描述的是 2026-10-08 的历史观察，不据当前显示倒推当时必然有该字段。
- **U14 — [MindX DL 6.0.RC2 ascend-dmi 故障诊断](https://www.hiascend.com/doc_center/source/zh/mindx-dl/60rc2/toolbox/ascenddmi/toolboxug_0020.html)**：精确登记 URL 本轮实开返回诊断页面正文；未重新完成历史记录中依赖动态渲染的全部表格与 PRBS 冲突裁断。只将其作为带产品/版本限制的诊断入口，不与 MindCluster 26.1.x 自动合并为配套或统一回服标准。

## 发现表

分级：P1＝足以造成重大错误操作或数据损失的高优先级问题；P2＝影响技术边界、操作决策或验收闭环的实质问题；P3＝限定、表达或导航问题。**以下全部为 open，关闭须作者修订后按对应证据定向复核；报告本身不修改正文。**

| ID | 级别 | 可定位位置 | 发现、证据及影响 | 明确关闭条件 |
|---|---|---|---|---|
| B23-T09-C01 | P2 | 正文第 114 行；第 124、149 行关联分支 | **把驱动失败后的人工重试写成自动状态迁移。** 第 114 行称失败后节点“会被重新打上 `upgrade-required`”；U06 的 Troubleshooting 则是失败先进入 `upgrade-failed`，排除故障后才由操作者重新置为 `upgrade-required`。第 124 行虽提重打标签，却没消除前文的自动重试含义；第 149 行又把失败和 validation 连续失败并列为联合条件，容易漏掉等待/删除/重启阶段的失败。 | 改清失败停留、定位/修复、受控重试的责任与前提；任一阶段进入 `upgrade-failed` 均进入停发/调查分支，不要求同时满足 validation 连败。保留事件、失败阶段及重试授权/记录，不给未绑定节点与版本的执行命令。 |
| B23-T09-C02 | P2 | 正文第 98、111、114、124 行 | **GPU 驱动波次缺少适用分支及破坏性默认值。** U06 明确 Operator 只管理容器化驱动，不管理宿主预装驱动；非 controller 路径也不是同等的暂停/跳过状态机。默认 `waitForCompletion.podSelector` 为空即不等待任何选定 Pod，`gpuPodDeletion.timeoutSeconds` 为 300，`drain.enable` 为 false。正文把三者统称“门槛”，不足以保证任务会先完成或保存恢复点；`OnDelete` 也不能在未明确管理路径时当成通用波次替代。 | 预检先记录驱动归属、controller 开关/版本与实际生效路径；宿主预装驱动另走匹配来源/现场方案，未知则停止。波次前要求记录等待选择器、删除/超时/force/emptyDir/drain 策略及作业恢复点，解释默认空选择器不等于等待全部作业；只在对应非 controller 路径下介绍 `OnDelete`，不混用控制能力。 |
| B23-T09-C03 | P2 | 正文第 116、125 行；来源记录第 33 行可对照 | **MindCluster 手动路径被过度概括为“一律卸载重装”，Device Plugin 前提也被绝对化。** U12“升级 Container Manager”规定 26.1.0+ 用 `deploy.sh upgrade` 保留配置，并警告重复 install 会覆盖配置；U11/U12 还区分全量升级与同版本镜像升级。U12 的 Device Plugin 注意事项在要求先升级 Runtime 后，紧接着列出未升级/未使用 Runtime/非默认挂载路径时配置 mounts 的条件分支。正文“其余组件”及“必须”抹去了这些例外。 | 按实际组件和升级方式限定概括：至少保留 Container Manager 脚本升级、TaskD 镜像内处理、同版本镜像路径与其限制；把 Device Plugin 的推荐前提和替代挂载分支分开。若本文只选 Runtime 26.1.0+ 单一路径，明确这是本文缩小的适用范围，而不是官方唯一可行路径；手动回退也不能统一承诺卸新装旧。 |
| B23-T09-C04 | P2 | 正文第 112、125 行 | **Helm 回退缺少“曾升级且保留可用历史 revision”的必要边界。** U10“版本回退”仅适用于通过 `helm upgrade` 升级过的 Release；从 kubectl 纳管后首次安装 Release，不会自动获得纳管前版本的可回退 revision。正文按 Helm/手动二分，容易把“现在受 Helm 管理”误当作“能够恢复任意旧版”。CRD 数据不自动回迁的警告是正确的，但不能替代历史资产前提。 | 在恢复分支明确逐一核查两个 Release 的 history、目标 revision 对应版本/配置/可用制品及升级前状态；首次纳管或无历史时不许承诺 Helm 回退，进入有证据的重建/备份恢复分支。保留先 CRD 后应用的顺序，并要求组合匹配、恢复后复验。 |
| B23-T09-C05 | P2 | 正文第 96、101、109 行 | **K8s 混版控制面的 skew 门禁未落实到整个通信集合。** U01 的 HA 示例明确：apiserver 为 1.31/1.32 时，kubelet/kube-proxy 不能升到 1.32；经负载均衡访问两版 apiserver 的 kcm/scheduler/ccm 仍只能为 1.31。正文只列简写规则和逐台控制面波次，未指出应取所有可达 apiserver 的允许交集；还没列 kube-proxy 对 apiserver 及同节点 kubelet 的独立约束。按某一已升级实例判断会误放行。 | 增加混版期的集合检查与禁止提前升级条件，包含 kube-proxy 的两类 skew；明确 policy 的组件顺序与 kubeadm 实际升级单元不是可随意拆开的同一张执行清单，并保留部署工具可能更严格的条件。用固定 v1.32 文档中的混版示例定向验证判定，不产生执行序列。 |
| B23-T09-C06 | P2 | 正文第 59、85、122 行 | **`/etc/kubernetes/tmp` 恢复路径未限定 local etcd。** U02“Recovering from a failure state”说明 `kubeadm-backup-etcd` 只含当前控制面节点的 local etcd member 数据，external etcd 时该目录为空。正文把该目录中的 etcd/manifests 备份合并成通用恢复资产，没有防止外置 etcd 场景把空目录误记成可用备份。 | 变更档案区分 local/stacked 与 external etcd，写清目录备份覆盖对象和不覆盖对象；external etcd 必须另有与该部署匹配且已验证可恢复的备份证据，未取得时停止/记 unknown。不得把单 member 目录等同于通用全集群或旧 minor 降级恢复点。 |
| B23-T09-C07 | P2 | 正文第 103、110、138、155–161 行 | **Slurm 完成门槛遗漏旧 `slurmstepd` 仍随作业存活的窗口。** U03-S“Upgrade Procedure”要求在认定升级完成前等待升级前已运行的作业结束；在 slurmd 升级前启动的作业仍使用旧 slurmstepd，不能仅凭 daemon/客户端版本清单与新作业能启动就再次升级或启用新特性。正文支持滚动升级，却未将该项加入“无混合残留”的证据定义。 | 档案关联升级前作业与 stepd 版本/生命周期；区分“允许的滚动混版观测期”和“升级完成”。完成前确认旧作业/旧 stepd 已退出，并有新版本作业成功启动和结束的证据；未完成时阻止下一轮升级或依赖新版本的特性切换。 |
| B23-T09-C08 | P3 | 正文第 65、103、123 行；来源记录第 24 行 | **Slurm 大版本保守回退规则被表述成覆盖所有维护版本的绝对结论。** U03-S 的 Reverting an Upgrade 给出启动后的不支持回退警告，但同页 Minor Upgrades 又说明维护版更能容忍混版和原地 downgrade，仍要求备份。来源记录提到了这一节，却仍总结为只存在两条恢复路；正文没有说明大版本与维护补丁的差别。现有表达偏保守，不据此反向承诺任意补丁能降级，故列 P3。 | 限定大版本/状态或 schema 变更的边界，单列同一 major 内维护补丁须逐 release 判断的条件；或明确“本文采用不依赖原地降级的更严格本地策略”，不把该策略冒充完整官方结论。保留备份要求，不给出未经核验的可降级组合。 |
| B23-T09-C09 | P2 | 正文第 34–37、86、127–140、153–161 行 | **回服门禁仍缺“分配可用”的闭环和 unknown 的明确阻断。** 设备门槛主要列 Ready/IDLE、allocatable、健康工具/GRES；没有写 kubelet/runtime 重启后插件重注册、实际新分配→容器可见稳定身份→作业使用与释放后的账本一致性。U15 区分注册、Allocate、健康上报；邻近容器基线 §4 与 T05-08 第 135–150 行也明确数量或空闲不等于分配/释放。第 86 行虽将无基线降为 unknown，却没有完整的通过/失败/未知→继续波次/隔离/回服分支；节点验收第 127–139 行则明确 unknown、必需检查跳过时不回服。T05-08 已在 `related_ids` 关联，不能说完全未引用，但正文没有可点击入口及回收证据移交点。 | 补齐受控新作业的设备请求/分配身份、插件重注册与运行时注入、使用/释放后账本核对门槛；给出三态判定及动作，必需项缺证、无基线或未解释 skip 不允许宣布回服。明确受控探针验证与全面恢复生产准入的先后/责任、观察窗和现场阈值的登记要求；加入 T05-08 正文链接并说明何时接收其回收证据。无需编造通用阈值或执行结果。 |

## 验收项覆盖表

| 验收项 | 本轮判定 | 已覆盖证据 | 未闭合项 / 关闭依据 |
|---|---|---|---|
| 1. 当前/目标制品、配置、配套/skew、硬件/拓扑、作业/恢复点、回退资产；版本未定不提供执行序列 | **方法层满足** | 正文第 43、55–88、157 行；无升级/回退 shell 命令块，档案字段已明确为填写结构 | 真实档案仍为空，不能升级为可执行处方；特定资产覆盖条件随 C04/C06 修正。不是要求作者虚构现场版本 |
| 2. K8s 按 skew/职责及插件条件，Slurm 按 release/状态/DB 说明回退边界 | **部分满足，需修订** | 正文第 96–125 行；U01/U02、U03-S/U04-S、U05–U12 | C02–C08；大版本迁移与不可直接降级主线正确，HA 交集、etcd、厂商组件条件及维护补丁限定不足 |
| 3. 预检→波次→观测→停发→恢复/重建→回服，覆盖设备、数据、网络/通信和应用功能/质量/性能 | **框架覆盖，门禁未通过** | 正文第 90–161 行；六层回服表覆盖数据、网络、应用质量/性能 | C01/C02/C07/C09；需使失败状态、作业保护、旧 stepd 和设备分配证据真正驱动停发/完成 |
| 4. 引用节点验收、兼容证据与 T05-08，明确基线、通过/失败/未知及模型不代替演练 | **部分满足，需修订** | 第 140 行已有节点验收/兼容证据普通 Markdown 链接；第 34 行已关联 T05-08 ID；第 29、160–161 行明确审阅不等于演练 | C09：T05-08 人读入口/交接点与三态门禁缺失。没有现场验证是已披露的边界，不是要求本次审阅执行演练 |

### 元数据、引用与本地校验

- `type: procedure`、`status: draft`、`applicability.environment_refs: []`、`verification.status: not_verified`、空 `evidence_refs` 与“未执行”的正文声明一致；没有据来源实开擅自标为 reviewed/reproduced。`generic` 在这里是流程概念范围，不当作多平台兼容认证。
- 正文全部 13 个 `source_refs` 与 7 个 `related_ids` 均可解析；两个节点验收/兼容性本地正文链接存在。T05-08 是已存在的元数据关系，但不是已完成的人读流程串接，见 C09。
- 实际执行只读检查：首次 `PYTHONDONTWRITEBYTECODE=1 make check` 返回 **PASS：100 content entries / 465 sources**；报告落盘后再次执行返回 **PASS：100 content entries / 469 sources**。来源计数变化对应上述外部工作树变化，不是本报告新增来源。另已校验报告发现 ID 连续、8 P2 / 1 P3、本地链接存在及无行尾空白；主审正文、来源记录和计划输入哈希未变。检查只覆盖结构及本地文件链接，不代表技术正确或远程链接可达。
- **未运行 `make build`**：本次用户仅允许创建指定报告；默认构建会写入 `build/`。未为满足通用构建约定而越权创建构建产物，也未运行集群/升级/回退命令。没有修改 `src/kb/`，本次不新增或运行代码测试。

## unknown 与证据边界

1. **Slurm 网页层仍不可访问。** U03/U04 已按要求逐条尝试，失败如实记录；本轮官方固定 release 源码补证不与站点实开成功混记。后续若要求“归档网页逐字一致”验收，须重新获得这两个精确 URL 的正文并比对；不能只拿本报告推定站点已恢复。
2. **缺少某页 downgrade 小节不等于证明全球不存在官方资料。** U02、U05–U08 未取得通用 K8s 降级、GPU Operator 本体回退或任意驱动降级的完整流程，只能保持这些能力/步骤 unknown。Slurm 启动后回退限制则有 U03-S 的明示警告，两类证据强度不同。
3. **NVIDIA 已知问题的 driver 降级绕行不是通用回退方案。** 支持页脚注与 release notes 对特定驱动/MIG 问题有不同版本动作；不得脱离问题和补丁上下文，把 570.86.15 或 570.172.08 当成本环境既定目标。也未把同/下一 major 的“升级”窗口外推成降级授权。
4. **MindCluster tag、文档产品版本与部署制品须分层。** `v26.1.1`→固定 commit 的关联已独立核对，release notes 写 26.1.0 的事实保留；这不是本地包/镜像配套已验证。CRD 的 schema/存储数据回迁、HDK/CANN 本身的升级回退、实际 Helm chart 资产与版本配对均未演练。
5. **相邻样板不自动组成一套环境。** GPU Operator 25.3 文档树、单独登记的 device-plugin v0.20.1、容器基线的 Toolkit/runtime 样板，以及 MindX DL 6.0.RC2 诊断入口，都不能凭同时被引用就成为同一受支持/已验证的完整组合。精确硬件、OS、内核、运行时、驱动、固件、插件及目标负载的联合条件仍须另立档案。
6. **调度扩展与波次能力未获完整证据。** 正文把 Kueue/Volcano 列为触发条件，但本轮只有 MindCluster 内置 Volcano 的相应升级入口；没有据此确认独立 Kueue 或任意上游 Volcano 版本的升级/回退路径，也没有给 MindCluster 推测出官方金丝雀机制。
7. **本地状态均未采集。** etcd/Slurm 备份可恢复性、实际作业与 checkpoint、DB 迁移耗时、网络/通信基线、设备分配/释放、应用质量和吞吐/尾延迟阈值均未实测。它们是执行与回服前的必要证据，不由模型审阅补齐。

## 审阅局限

- 本轮只对上述输入快照与取得的精确文档提出技术意见；没有安装软件、拉取镜像、验签发行制品、启动集群或进行硬件/升级/回退/回服演练。Git tag 对象关联检查也不等于独立密码学验签。
- 两个 Slurm 站点 URL 不可访问；原文件补证来源、commit 与网站失败已分别记录，未猜测 HTTP 状态、网页字节或站点恢复情况。其他网页也没有做字节哈希留存，读取服务可能使用缓存；访问日期不是其内容发布时间。
- 远程长页采用章节定位与定向复读；未审完 NVIDIA 全部历史 release notes、所有 OS/GPU 子表、operator-validator 内部测试、Helm chart 实现或厂商工具内部判据。不能据“未在所读章节发现”断言其他实现中绝不存在某能力。
- 精确实际模型与推理档位缺少可验证运行时元数据，故本轮不能声称完成仓库指定模型的身份/路由验收；不能以后补约定字符串的方式伪造。需要满足该流程验收时，应由可返回实际模型元数据的执行器重新执行或提供可核验会话元数据。
- 本报告没有关闭任何发现。作者修订后应按 C01–C09 定向复核并记录变化；文档通过后也仍不等于真实平台演练通过。
