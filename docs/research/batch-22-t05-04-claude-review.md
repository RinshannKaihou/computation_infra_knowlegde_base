# 第二十二批 T05-04 初审

审阅日期：2026-10-17（取证开始于 02:34 UTC，即本地 10:34 +0800）。正文 `updated_at: "2026-10-17"` 与审阅日相同，但输入以下表 SHA-256 识别，不以日期推导。

**结论：T05-04 需修订。新增 8 项发现（B22-C31–C38）：P1 ×1、P2 ×4、P3 ×3，全部 OPEN。** 四条 acceptance 均只部分满足；昇腾既有内容在本次修订中未被改动，抽查的两处固定 commit 行锚仍成立。

- acceptance 1：三种实现分列、明确不设计统一错误码，K8s 账本与 Slurm GRES/TRES 字段属实。缺口在"稳定设备标识"：GPU 侧把 kubelet 记录的设备 ID 与传给运行时的 ID 混为一谈，漏掉共享副本的注解 ID；Slurm 侧没有写出 cgroup 约束下作业内 `CUDA_VISIBLE_DEVICES` 是相对编号。
- acceptance 2：K8s 文档语义与 server.go/health.go 的行锚全部属实。但插件自身的重启策略（kubelet.sock 重建、SIGHUP、30 s 重试）、重启后设备以 Healthy 重建、设备发现失败的分支，都在同一 tag 中可读，正文却记为 unknown 或写成"无恢复路径"。健康标记按物理 UUID 只保留一个设备条目，这一限制没有写。Slurm 的账本刷新条件只覆盖了 INVAL 一种情形。
- acceptance 3：对照表三行×三实现齐全，并链接了生命周期指南。GPU 列的"缺设备""账实不符"两格与 C31 冲突；"重复分配"一格没有区分设计内共享（副本、shard/MPS）；"前置条件以各生命周期指南为准"一句，在 K8s 侧是循环引用。
- acceptance 4：昇腾三入口保留；GPU/Slurm 入口已给出，但 GPU 回收验证以节点 `allocatable` 为观测量，与正文 L51/L62 自己的定义矛盾；Slurm 身份核对链缺 cgroup 相对编号与 `SLURM_JOB_GPUS`。

正文没有虚构命令输出或实测结果，`verification.notes` 与 L169 如实写明未执行，推论处大多标了"本库推论"。`make check` 与 `make build` 均通过（见文末），它们只校验结构与本地链接，不说明技术正确性。

审阅者角色独立于作者，按用户本次要求以 `claude-opus-5-5` 执行。模型与运行元数据的核验结论见文末专节。本轮只做审阅和只读取证：未改作者正文、来源记录、登记、索引或计划；未部署插件、kubelet 或 Slurm，未运行任何集群/设备命令或测试。模型审阅不构成平台、硬件或现场验证。

发现编号说明：审阅开始时在仓库中检索 `B22-C`，最大号为 C30（[T05-05 初审](batch-22-t05-05-claude-review.md)及其各轮复核），没有 C31 及以上的占用，本报告从 B22-C31 续号。

## 输入（以 SHA-256 识别）

| 输入 | SHA-256 |
|---|---|
| [T05-04 正文](../../knowledge/05-cluster-platform/device-resource-chain.md)（177 行，concept / draft，revise） | `c96e362c50cb4062dcb1a751d4f1917c591a96d5083323443fe04a56dfad05aa` |
| [作者来源记录](batch-22-t05-04-sources.md)（28 行） | `b42352a4e594f8184588b00d073126cd4ae7dd0fbfed59365d9610b422909c8c` |
| [任务计划](../../plans/full-coverage-backlog.yaml)（T05-04 L5510–5551，acceptance L5527–5531，source_discovery L5540–5542） | `1dd6b549c38f4808cfb6d6d80c84e31503354a196c4cbb4c7529988af57fde71` |
| [来源登记](../../sources/registry.yaml)（`src.kubernetes.device-plugins-v1-32` L129–142、`src.ascend.mind-cluster-v26.1.1` L235–254、`src.nvidia.k8s-device-plugin-v0.20.1` L5237–5247、`src.slurm.docs-24.11.7` L5408–5418、`src.slurm.gres-tres-cgroup-24.11.7` L5419–5429） | `37b1cfb1f3a8acb7e3fb99ca49667b395cde6de12b4e8abdbea268f32e9ab3e3`；L5237–5247 段 `ef6042622d2296c9385631ffcff75c2821df3e4fa0bc46d1e37aea49a76db9f5` |

四个输入在审阅开始时取哈希（git HEAD `981b06a8d917a904b371ae4763904e426e884eb3`，工作区干净），成稿前复取一次，结果一致（见文末）。

旁证（按本库现行草稿核对，未重新取其一次源）：

- 正文全部站内链接都能解析到已有文件：`container-image-runtime-baseline.md`、`kubernetes-job-lifecycle.md`、`slurm-jobs-and-device-resources.md`、`ascend-device-visibility-triage.md`、`ascend-device-visibility-source-case.md`、`ascend-device-visibility-experiment.md`、`../01-hardware/resource-topology.md`、`../02-software-stack/layers-and-boundaries.md`、`../02-software-stack/compatibility-evidence.md`、`../../docs/research/batch-22-t05-04-sources.md`、`../../docs/research/batch-02-f11-sources.md`。
- [镜像运行时基线](../../knowledge/05-cluster-platform/container-image-runtime-baseline.md) §2"框架映射"行（L80）的 M-ID ①–⑤ 与正文 L147 的五段一致；§4 L121 的 K1 缺方法 / K2 缺采样 / K3 未执行定义与正文用法一致；§4 异常分支表存在（L137 起）。
- [Slurm 状态参考](../../knowledge/05-cluster-platform/slurm-jobs-and-device-resources.md) GRES/TRES 节（L126–139）的字段与正文 Slurm 节一致；该页 L133 引的是完整原文 `could vary between boots after hardware or OS changes`，正文 L118 却作了截断（见 C37）。
- [Kubernetes 作业生命周期](../../knowledge/05-cluster-platform/kubernetes-job-lifecycle.md) 覆盖 restartPolicy/backoff/podFailurePolicy 等 15 处，但没有节点 drain/cordon/授权类内容；它在 L132 把设备分配的证据链指回本文（见 C38）。
- [昇腾实验设计](../../knowledge/05-cluster-platform/ascend-device-visibility-experiment.md) L67、L79、L94 有资源回收步骤与观察项，可作为正文 L149"回收验证以各页记录为准"的落点。
- [索引](../../knowledge/05-cluster-platform/index.md) 的本条描述与 05.3 条目已更新为"含 NVIDIA v0.20.1 与 Slurm 24.11.7 独立视图，待审阅"，与正文一致。
- `git show 981b06a` 显示本次修订没有删改"昇腾例子"节；删除的只有 frontmatter 摘要/注记、L42 原句、适用边界四条与来源一条，均已被扩写替代。

## 一次源取证（审阅者独立获取）

方法：全部用 `curl -sSL` 默认 TLS 校验只读获取，HTTP 均为 200（404 探测见限制）。GitHub 文件经 `raw.githubusercontent.com` 按 tag 与固定 commit 各取一次；版本锚用 `git ls-remote`。HTML 按下表哈希对应的原文行号核对（未去标签渲染），不只判可达性。

**与任务约定的偏差**：本会话对 `/tmp` 的写入（`mkdir`、`mktemp`）被权限拒绝，原文未能落盘。改为每次把 curl 输出经管道直接计算 SHA-256 并读取行区间（`cat -n | sed -n`），同一 URL 的多次取回逐次比对哈希，结果一致。因此没有可供事后复查的临时目录，下表哈希是唯一留存。

作者来源记录 L3 写明 NVIDIA 两文件用 curl 字节级取回、K8s 页用 FetchURL，但记录中没有哈希与 HTTP 状态。本表哈希是本审阅的取证，不能写成作者取证。

版本锚：

- NVIDIA：`refs/tags/v0.20.1` 为 tag 对象 `03296a61aeb9943906a1789f978ac3c87e13dfdd`，`^{}` 指向 commit `487d7a93894b0f3ad08097169593972eb3ca8206`。server.go 与 health.go 经 tag 与经 commit 取回字节一致，行数分别为 557 与 363，与正文、登记一致。
- Kubernetes：版本化子域 `v1-32.docs.kubernetes.io`，页面没有固定源 commit（登记 L141 已注明）；两次取回哈希一致，只代表本次观察。
- Slurm：所取十页页头均为 `Version 24.11`，补丁级只由路径 `archive/slurm-24.11.7/` 确定；十页哈希与 [T05-03 初审](batch-22-t05-03-claude-review.md) 所记逐一相同。
- MindCluster：`refs/tags/v26.1.1` 为 tag 对象 `387a7f2b5f9ddfdbcdff0d8c85386fc68e2fe7fb`，指向 commit `44385c13d7b1d87def35f1604e8be4d16de6ca4e`，与登记一致。

### NVIDIA k8s-device-plugin v0.20.1（commit `487d7a93`，src.nvidia.k8s-device-plugin-v0.20.1）

| 文件 | SHA-256（原文） | 核对点与结果 |
|---|---|---|
| [internal/plugin/server.go](https://github.com/NVIDIA/k8s-device-plugin/blob/487d7a93894b0f3ad08097169593972eb3ca8206/internal/plugin/server.go)（557 行，18397 B） | `215f04ab2ee4cbfe8f57cbd65064930b852f0c9678b0314c4aa65f93c6c020d9` | **正文行锚全部属实**：Start L129–160（MPS 等待 L132–134；Register 失败调用 Stop L144–148；CheckHealth goroutine L151–157，出错时记 `continuing with health checks disabled` L155，`TODO: add MPS health check` L152）；Stop L163–174（`os.Remove(plugin.socket)` L169）；Serve L177–226（先删旧 socket L178；崩溃环 L186–215：`restartCount > 5` 时 `klog.Fatalf` L193–196，崩溃间隔超过 3600 s 计数归零 L206–211，否则加一 L212–214）；Register L229–256（`RegisterRequest` 字面量 L242–249：Version/Endpoint/ResourceName/`GetPreferredAllocationAvailable: true`）；ListAndWatch L267–285（首发全量 L268–270；`FIXME: there is no way to recover from the Unhealthy state.` L277；置 Unhealthy L278）；Allocate L306–320（`ValidateRequest` L309–311）；getAllocateResponse L322–366（全 CDI 时提前返回 L351–353；PassDeviceSpecs L362–364）；updateResponseForCDI L377–409；uniqueDeviceIDsFromAnnotatedDeviceIDs L456–474（uuid 分支 `rm.AnnotatedIDs(ids).GetIDs()` L458–460，index 分支 `Subset(ids).GetIndices()` L461–463）；updateResponseForDeviceListEnvVar L481–483；updateResponseForDeviceMounts L497–514（同时把 `NVIDIA_VISIBLE_DEVICES` 设为容器路径根 L498）；apiDeviceSpecs L516–557（可选项 stat 门控 L517–532）。来源记录 L9 写"RegisterRequest L241–248"，实际字面量为 L242–249（L241 是 `NewRegistrationClient`），差一行。→ C31、C33、C36、C37 |
| [internal/rm/health.go](https://github.com/NVIDIA/k8s-device-plugin/blob/487d7a93894b0f3ad08097169593972eb3ca8206/internal/rm/health.go)（363 行，12063 B） | `4a955f04be78172901308e3bdd508dc2f78931a4ee5190e2bb6db99f64f6b3b4` | **属实**：`DP_DISABLE_HEALTHCHECKS` L34、`DP_ENABLE_HEALTHCHECKS` L40（注释 L30–39）；checkHealth L44–172；全禁直接 `return nil` L45–48；NVML init 分支 L50–56；eventMask L78；启动期标记：placement 失败 L80–85、取 handle 失败 L90–95、读支持事件失败 L97–102、RegisterEvents 其他错误 L108–110（`ERROR_NOT_SUPPORTED` 只警告 L106–107）；等待错误标记全部 L125–131；跳过非 Xid L133–136；忽略清单内 XID 跳过 L138–141；UUID 失败标记全部 L144–152；意外设备忽略 L154–158；MIG GI/CI 过滤 L160–167；命中标记 L169–170；硬编码清单与 FIXME L229–240。**正文未述**：`parentToDeviceMap[uuid] = d`（L74、L88）对每个物理 UUID 只保留一个 Device；非 MIG 设备的 placement 取 `d.GetUUID()`（去副本注解）L282–285。文件头 L1–15 为 Apache License 2.0。→ C32、C36、C37 |
| [cmd/nvidia-device-plugin/main.go](https://github.com/NVIDIA/k8s-device-plugin/blob/487d7a93894b0f3ad08097169593972eb3ca8206/cmd/nvidia-device-plugin/main.go)（未登记，同 commit） | `e48449efbbc74857b66490fa95622c618cdee396b599d9e1d55c440435609d42` | 旗标默认值 L61–104：`fail-on-init-error` 默认 true，用途 `fail the plugin if an error is encountered during initialization, otherwise block indefinitely`（L68–72）；`pass-device-specs` 默认 false（L87–92）；`device-list-strategy` 默认 envvar（L93–98）；`device-id-strategy` 默认 uuid，用途 `the desired strategy for passing device IDs to the underlying runtime`（L99–104）。`c.Run` 出错即 `os.Exit(1)`（L196–200）。`start` L268–347：监视 kubelet socket 所在目录（L271–277）；`restart:` 先 `stopPlugins` 再 `startPlugins`，任一 Start 失败则 30 s 后重试（L285–304）；kubelet.sock 的 Create 事件触发重启（L314–321，注释 `Detect a kubelet restart by watching for a newly created 'pluginapi.KubeletSocket' file`）；SIGHUP 重启、其他信号退出（L330–338）。`startPlugins` L349–420：每次都调用 GetPlugins（L392）；无设备的 plugin 不启动（L402–405）；全部无设备时记 `No devices found. Waiting indefinitely.`（L415–417）。→ C31 |
| [cmd/nvidia-device-plugin/plugin-manager.go](https://github.com/NVIDIA/k8s-device-plugin/blob/487d7a93894b0f3ad08097169593972eb3ca8206/cmd/nvidia-device-plugin/plugin-manager.go)（未登记） | `1142df235c2722708dbd30c6ad207ec2edb4263f802adfdb8f9bf71de58d589d` | GetPlugins L35–90 每次调用 `plugin.New`（L73–80，传入 `WithFailOnInitError` L77），并写 CDI spec 文件（L85–87）。→ C31 |
| [internal/plugin/factory.go](https://github.com/NVIDIA/k8s-device-plugin/blob/487d7a93894b0f3ad08097169593972eb3ca8206/internal/plugin/factory.go)（未登记） | `fe77bc093ebd2f1adb3293510e92b7e58232b31cdccabe5e21dec170f010d2d1` | `New` L51–88 每次调用都重建资源管理器（L74）。`getResourceManagers` L93–128：NVML init 失败时，failOnInitError 为 true 返回错误（L104–106），为 false 返回 `nil, nil`（L107–108）；不支持的发现策略同理（L117–126）。→ C31 |
| [internal/rm/nvml_manager.go](https://github.com/NVIDIA/k8s-device-plugin/blob/487d7a93894b0f3ad08097169593972eb3ca8206/internal/rm/nvml_manager.go)（未登记） | `198291e96eec164c8f48a66cf763a471a4c231bf430252ca8aa3b6c0bb1f6f26` | NewNVMLResourceManagers L39–85：init 失败报错（L40–43）；每个资源名一个 rm，空设备集跳过（L59–62）；WSL 平台使用基础 resourceManager（L71–73）。GetDevicePaths 追加四个控制节点（L94–103）。CheckHealth 以本资源的全部设备（含副本）调用 checkHealth（L106–108）。→ C31、C32 |
| [internal/rm/rm.go](https://github.com/NVIDIA/k8s-device-plugin/blob/487d7a93894b0f3ad08097169593972eb3ca8206/internal/rm/rm.go)（未登记） | `f6dced1f504f604455315999026352d27bc8dd8607ec844b06c2080dfa321c1b` | 基础 resourceManager 的 CheckHealth 直接返回 nil（`CheckHealth is disabled on the base resourceManager.` L53–56）。ValidateRequest 对未知 ID 报 `unknown device`（L83–89）；共享副本请求数大于 1 时按配置拒绝（L91–105）。→ C32、C33 |
| [internal/rm/devices.go](https://github.com/NVIDIA/k8s-device-plugin/blob/487d7a93894b0f3ad08097169593972eb3ca8206/internal/rm/devices.go)（未登记） | `e23a3b2e7d3c9fdee9e5e754ed6c334a163bd1c03d52edf126135fc9a340b062` | `Devices` 是 map（L50–51）。BuildDevice：`dev.ID = uuid`、`dev.Index = index`、`dev.Health = pluginapi.Healthy`（L86–93）。GetPluginDevices 返回 ListAndWatch 所用对象（L180–187）。以 Index 含 ":" 判定 MIG（L228–230）。GetUUID 去掉注解（L232–235）。NewAnnotatedID 格式 `%s::%d`（L237–240）。→ C31、C32、C33 |
| [internal/rm/device_map.go](https://github.com/NVIDIA/k8s-device-plugin/blob/487d7a93894b0f3ad08097169593972eb3ca8206/internal/rm/device_map.go)（未登记） | `26d83432c1f05c66270167fd6e0744e1891851ccefebc45e1d9ebc641edac2b5` | buildGPUDeviceMap 以 `VisitDevices` 的序号 i 建立 index（L110–134）；GPU 名称不匹配任何资源模式时报错（L131）。副本构造 L320–345：ID 为注解 ID，Index 与 Health 复制自原设备（L326–342）。→ C31、C32、C33 |

### Kubernetes v1.32 Device Plugins（src.kubernetes.device-plugins-v1-32）

页面：<https://v1-32.docs.kubernetes.io/docs/concepts/extend-kubernetes/compute-storage-net/device-plugins/>，HTTP 200，490270 B，SHA-256 `c954c37a1e3533220f464f5cff88bb49a9f289ce3f8bf8dc3418dc79d04e539a`（两次一致；可变网页，只代表本次观察）。下列行号为该哈希下的 HTML 原文行。

| 核对点 | 位置 | 结果 |
|---|---|---|
| 小节 id | 全页 `<h2/h3 id=…>` | 实际为 `device-plugin-registration`、`example-pod`、`device-plugin-implementation`、`handling-kubelet-restarts`、`device-plugin-and-unhealthy-devices`、`device-plugin-deployment`、`api-compatibility`、`monitoring-device-plugin-resources`、`grpc-endpoint-list`、`grpc-endpoint-getallocatableresources`、`grpc-endpoint-get`。正文 L52 的 `#example` 与 L62 的 `#getallocatableresources-grpc-endpoint` 不存在。→ C36 |
| 扩展资源约束 | L817 | **属实**：`Extended resources are only supported as integer resources and cannot be overcommitted.` **正文未用**：同处 `Devices cannot be shared between containers.` → C33 |
| 服务定义 | L841–863 | DevicePlugin 服务只有 GetDevicePluginOptions/ListAndWatch/Allocate/GetPreferredAllocation/PreStartContainer，没有释放类回调。→ C34 |
| kubelet 重启 | L883–886 | **属实**：`A new kubelet instance deletes all the existing Unix sockets under /var/lib/kubelet/device-plugins when it starts. A device plugin can monitor the deletion of its Unix socket and re-register itself upon such an event.` |
| 不健康设备 | L886–892 | **属实**：allocatable 降低以影响新 Pod 的调度，`Capacity count for the resource will not change`；`Pods that were assigned to the failed devices will continue be assigned to this device`。 |
| Pod 级健康关联 | L892–897 | **属实**：`ResourceHealthStatus` 为 `Kubernetes v1.31 [alpha] (enabled by default: false)`，开启后加 `allocatedResourcesStatus`。原文 L892–893 为 `Before Kubernetes v1.31, the way to know whether or not a Pod is associated with the failed device is to use the PodResources API`；正文 L63 改写为"未启用时……只能用"，属于推论。→ C36 |
| 部署 | L898–905 | **属实**：`restart the daemon Pod after failure` |
| PodResources | L915–1043 | **属实**：List L929–931 `device id as it was reported by device plugins`（→ C33）；GetAllocatableResources L1004–1011 `resources initially available on the worker node`，评估空闲资源时 `should be used in conjunction with the List() endpoint`，`device health changes` 时客户端应重新调用（→ C34）；Get 端点 L1035–1043 为 v1.27 alpha，需 `KubeletPodResourcesGet` 门控（正文未用，来源记录已列）。 |

### Slurm 24.11.7 归档（src.slurm.docs-24.11.7、src.slurm.gres-tres-cgroup-24.11.7，复用）

| 页面 | SHA-256（原文，均与 T05-03 初审相同） | 核对点与结果 |
|---|---|---|
| [gres](https://slurm.schedmd.com/archive/slurm-24.11.7/gres.html) | `4c7a58746e36f07ac7bf43cde934a7342b16698068ceb61ee83debc1c6eccff9` | **属实**：默认无 GRES、GresTypes/Gres（L134–137）；资源少于配置置 DRAIN（L144–146）；AutoDetect 节（nvml/nvidia，`AutoDetect=nvidia (added in Slurm 24.11) doesn't require the nvml library … but doesn't detect MIGs or NVlinks`；`Gres=` 行仍必需）；失配时 `GPU is omitted from the node with an error`（L283）；检测到的设备多于配置时 slurmd 被 drain（L287–289）；Type 子串（L319）；`slurmd -C`/`slurmd -G`（L321、L339）；每个 step 设 `CUDA_VISIBLE_DEVICES`，sbatch 只反映 node zero（L347–354）；NVML 按 PCI bus ID、CUDA_DEVICE_ORDER（L387–393）；minor 号与映射（L395–401）。**正文未用或不准**：L369–370 `Be sure to specify the File parameters … in the increasing numeric order`；L372–384 cgroup 约束设备时，作业内 `CUDA_VISIBLE_DEVICES` 与 Prolog/Epilog 不同，例如分到 `/dev/nvidia1` 时 Prolog/Epilog 中为 "1"、作业内为 "0"；L398–399 原文是 `could vary between boots after hardware or OS changes. For the most part, this assignment seems fairly stable.`，正文 L118 截掉了条件与后句；L622–625 `SLURM_JOB_GPUS`：`The GPU IDs of GPUs in the job allocation`。全页无 ECC/Xid/health 字样，正文把"GPU 运行期健康探测"记为 unknown 是准确的。→ C35、C37 |
| [gres.conf](https://slurm.schedmd.com/archive/slurm-24.11.7/gres.conf.html) | `21aeb902c64844020cca02fe761eb53a8daec7699020d79c7f36d113f47e294e` | **属实**：AutoDetect 时以指定的 **File、Cores、Links** 作 sanity check，失配时 `node's state is set to invalid and the node is drained`（L211–215）；File↔Count 一致（L283–285）。**正文未用或不准**：正文 L129 写成 Type/Cores/Links；MPS/Sharding 例外，Count 为对应同一 GPU 的条目数（L286–290）；gpu 类 GRES 必须写 File（L295）；File 须在全部节点指定才会逐设备跟踪，否则只跟踪计数（L297–301）；`Drain a node before changing the count of records with File … Failure to do so will result in any job using those GRES being aborted.`（L303–305）。→ C35、C37 |
| [tres](https://slurm.schedmd.com/archive/slurm-24.11.7/tres.html) | `2d08f826f585d5f0c663b80406352af8565c6c84c6e675de8e6fd177508691b2` | **属实**：Billing 由 TRESBillingWeights 计算（L134–135）；AccountingStorageTRES（L152–160）；`Setting gres/gpu will also set gres/gpumem and gres/gpuutil`（L182–183）；TRESBillingWeights（L200–215） |
| [cgroup.conf](https://slurm.schedmd.com/archive/slurm-24.11.7/cgroup.conf.html) | `8835c19854a487fad4e8485cd30ffb0dc86c0bc49f87070717c20d36cafeca32` | **属实**：ConstrainDevices 按 GRES 约束设备，默认 no（L226–228） |
| [slurm.conf](https://slurm.schedmd.com/archive/slurm-24.11.7/slurm.conf.html) | `f4151769ed29968c7de408809a5acb8f0591865cd525d5f2c70925e847a1ff34` | **属实**：HealthCheckProgram（L1379–1395：非 NOT_RESPONDING 节点；动作须由脚本自己执行；60 s 未结束即被杀；slurmd 首次启动、注册前执行一次）；ReturnToService 默认 0，含"有效配置"定义（L3169–3192）；SlurmdTimeout 默认 300 s（L4628–4638）；UnkillableStepTimeout 超时 drain（L5211–5217）。**正文未用**：HealthCheckInterval `The default value is zero, which disables execution`（L1345–1346）；HealthCheckNodeState 默认 ANY（L1349–1351）；HealthCheckProgram `By default, no program will be executed`（L1395）；`Changes in node configuration … require restarting or reconfiguring all slurmctld and slurmd daemons`（L5302–5304）。→ C35、C37 |
| [sinfo](https://slurm.schedmd.com/archive/slurm-24.11.7/sinfo.html) | `b67afb7958851970875457443f05457b8262a1b4840bcbdbf4accbb792398770` | **属实**：节点 COMPLETING 在作业进程全部终止且 epilog 结束后移除（L850–855）；INVAL 为注册资源少于配置，需 slurmd 重启后有效注册（L900–903）。全页无 `AllocTRES`。 |
| [prolog_epilog](https://slurm.schedmd.com/archive/slurm-24.11.7/prolog_epilog.html) | `6d83380c65d0dcd57a598b03aa9a046e4c1aae86975a873dc9175cd01731ceac` | **属实**：`CUDA_VISIBLE_DEVICES` 在 Prolog/Epilog（cgroup 外）与作业内可不同，同样给出 "1"/"0" 的例子（L467–483）；Failure Handling：Epilog 失败→DRAIN，Prolog 失败→DRAIN＋重排＋默认 held，EpilogSlurmctld 失败只记日志，PrologSlurmctld 失败→batch 重排、交互作业取消（L833–845）。→ C35 |
| [scontrol](https://slurm.schedmd.com/archive/slurm-24.11.7/scontrol.html) | `da776891b3e6070f6e576c5b0f7bcbd62465e976919a1dd62b296050aa4e6d97` | 节点 update `Gres=`（L1438–1455）：`Modification of GRES count associated with specific files (e.g. GPUs) is not allowed other than to set their count on a node to zero. In order to change the GRES count to another value, modify your slurm.conf and gres.conf files and restart daemons.`；GPU 与 socket 的具体关联不在输出中报告，只能从 gres.conf 解析；scontrol 设置的 GRES 只在 `-R` 重启或 SIGHUP 时保留。`reconfigure` 见 L388；`-d/--details` 见 L157，details 只对 show job 生效（L778）。全页无 `AllocTRES`。→ C35、C37 |
| [sacct](https://slurm.schedmd.com/archive/slurm-24.11.7/sacct.html) | `d96f8299e0b778c8d4cd04a710969f458f118482b122bb99443716ca9ab677f4` | `AllocTres` 是 job/step 记账字段（L646 `resources allocated to the job/step`），不是节点视图字段；`-D` 语义沿用 T05-03 初审核对结论。→ C37 |
| [scancel](https://slurm.schedmd.com/archive/slurm-24.11.7/scancel.html) | `956cfa7716af5cfbdeb4eee24e888a0c129db55aa4adcc9b72b3e190da583f53` | 只核对了哈希；"取消 step 不释放分配"沿用 T05-03 初审核对结论，本轮未重读全文 |

### MindCluster v26.1.1（commit `44385c13`，src.ascend.mind-cluster-v26.1.1，抽查）

| 文件 | SHA-256（原文） | 核对点与结果 |
|---|---|---|
| [component/ascend-device-plugin/pkg/server/server.go](https://github.com/Ascend/mind-cluster/blob/44385c13d7b1d87def35f1604e8be4d16de6ca4e/component/ascend-device-plugin/pkg/server/server.go) | `6eb73b1a780296e82ad08a1e1cf2808ea76ea1de26ddf5f37c0ac03266e40a4e` | 正文 L76 锚 L144–152 属实：`NewRegistrationClient`，`RegisterRequest{Version, Endpoint, ResourceName}`，`client.Register` |
| [component/ascend-device-plugin/pkg/server/plugin.go](https://github.com/Ascend/mind-cluster/blob/44385c13d7b1d87def35f1604e8be4d16de6ca4e/component/ascend-device-plugin/pkg/server/plugin.go) | `585224e4b221fb3135e16e264b4c62e6bfb0710a69a4407d62a338aec5738a52` | 正文 L78 锚起点 L1295–1298 属实：`Allocate is called by kubelet to mount device to k8s pod`，随后 `checkAllocateRequest`。其余昇腾行锚为既有内容，本轮未逐条重核 |

### 来源差异记录核对（作者来源记录 L21–24）

- 精确行号 Allocate L306–320、getAllocateResponse L322–366、updateResponseForCDI L377–409、uniqueDeviceIDsFromAnnotatedDeviceIDs L456–474 与取回文件**一致**。
- 前轮区域锚 L280–438 覆盖前三个函数的全部行，L448–481 覆盖 uniqueDeviceIDs 的全部行（只覆盖 updateResponseForDeviceListEnvVar 的首行 L481），"松散超集"的说法对所列四个函数**成立**。
- 来源记录 L24 所引 FIXME 原文与行号（L277）**一致**。登记"忽略 XID L232–240"与来源记录"L229–240"都覆盖了切片 L233–240（注释 L229–232），可以接受。
- 小差异：来源记录 L9"RegisterRequest L241–248"应为 L242–249（见 C36）。

### 取证限制

- 原文未落盘（见上文偏差），无法事后复查原文件，只能依据所记哈希重新取回比对。
- GitHub 未认证 API 返回 403（rate limit），无法列出目录。文件按路径探测取回，其中 `internal/plugin/manager.go`、`internal/plugin/plugin.go`、`internal/rm/factory.go` 为 404。因此"同一 tag 中可读"只覆盖上表所列文件。
- 未取：go-nvlib `VisitDevices` 的序号语义（index 是否等于 nvidia-smi 序号）、kubelet devicemanager 源码（插件重启窗口内 kubelet 侧账本行为）、tegra 资源管理器、CDI handler、gpuallocator。正文 unknown #1（插件重启窗口内的 kubelet 侧账本表现）在所选来源下仍然成立。
- C31、C32 中的后果判断，是审阅者按上表代码路径作的推论。没有运行插件，没有读测试，也没有核对上游 issue。
- 许可：NVIDIA 两文件文件头为 Apache 2.0，仓库根 LICENSE 未打开；SchedMD 站点许可未核对。

## 发现

### B22-C31 — P1 / OPEN：插件重启策略、重启后健康重置与发现失败分支在同一 tag 可读，正文却记为 unknown 或写成"无恢复路径"

位置：正文 L103（"设备恢复健康在上报层的条件未给出（unknown）；插件进程重建后该状态是否重置未取证（unknown）"）、L107–108、L141 GPU"缺设备"格、L143 GPU"账实不符"格（"本版插件无 Unhealthy 恢复路径，设备修复后账本不自动回升"）、L170 待确认（"插件 NVML 设备发现层的失败场面行为"）；`verification.notes` L31；来源记录 L10、L12、unknown 第 2、3 条（L28）；登记 L5242。对应 acceptance 2"插件/daemon 重启和账本刷新条件"、acceptance 3"缺设备""账实不符"，以及 source_discovery L5542（"待核查所选 NVIDIA Device Plugin 的……重启策略"）。

证据（commit `487d7a93`，哈希见取证表）：

- **插件侧的重启触发**：main.go L268–347 中，kubelet.sock 的 Create 事件（L314–321）、SIGHUP（L332–334）、Start 失败后的 30 s 定时（L301–304、L311–312）都会 `goto restart`：先 `stopPlugins`，再 `startPlugins`。这正是 K8s 文档"Handling kubelet restarts"在 NVIDIA 实现中的落点。注意它监视的是 **kubelet.sock 的创建**，而不是文档所举的"监测自身 socket 被删除"。正文 L107 只引了文档的一般期望。
- **每次重启都从零重建设备集**：`startPlugins` 每次调用 GetPlugins（main.go L392）→ `plugin.New`（plugin-manager.go L73–80）→ `getResourceManagers`（factory.go L74、L93–114）→ `NewNVMLResourceManagers`（nvml_manager.go L39–85）→ BuildDevice（devices.go L86–93，`dev.Health = pluginapi.Healthy`）。Unhealthy 只存在于内存中的设备对象（server.go L278 修改的是 rm 设备指针），没有持久化。进程重启（`klog.Fatalf`、`os.Exit(1)`，或 DaemonSet 重建 Pod）同样从 BuildDevice 开始。
- **发现失败分支**：
  - `fail-on-init-error` 默认 true（main.go L68–72）。NVML init 失败时返回错误（factory.go L104–106），经 `start` 返回后 `os.Exit(1)`（main.go L196–200），之后依赖 DaemonSet 重启。
  - 设为 false 时返回 `nil, nil`（factory.go L107–108），没有任何 plugin，记 `No devices found. Waiting indefinitely.`（main.go L415–417），节点上没有该扩展资源。
  - 某资源名没有设备时不启动该 plugin（nvml_manager.go L59–62；main.go L402–405）。
  - GPU 名称不匹配任何资源模式时构建报错（device_map.go L131）。
  - 这些都是"驱动可见但平台无资源"的候选断点，正文 L141 只写了"注册/ListAndWatch 断点"。

推论（审阅者依据上述代码路径，未执行）：

- 正文"本版无恢复路径"只在**单次进程/单次 Serve 内**成立。任何重启路径都会把先前标为 Unhealthy 的设备重新以 Healthy 上报。
- 由此产生两个方向相反的后果：其一，修复后的设备可以经插件重启回到账本；其二，未修复的坏卡也会在重启后重新变得可调度，直到再次触发 XID 事件。health.go 只对事件作出反应（L114–171），不做轮询式状态检查。
- 这直接影响 acceptance 2"新旧任务影响"与 acceptance 3"账实不符"的处理前置条件。

仍属真 unknown（所选来源未覆盖）：插件重启窗口内 kubelet 侧 `capacity`/`allocatable` 的表现，以及与既有分配的关系，需要 kubelet devicemanager 源码。正文 L109 的这一条可以保留。

关闭条件：

- GPU 节新增"重启与重建"小表，逐行引 file@commit 与行区间，注明只读未执行。行至少包括：kubelet.sock 重建→全部 plugin 重启；SIGHUP；Start 失败 30 s 重试；进程退出→DaemonSet 重启；每次重启都重建设备集并以 Healthy 上报。
- L103、L143 改为"进程内无 Unhealthy→Healthy 路径；任何重启路径都重建设备集并以 Healthy 上报（按代码路径的推论，未执行）"，并写明坏卡可能因重启重新变得可调度。
- L141 补上述四类发现失败分支，以及 `fail-on-init-error` 的默认值。
- unknown 第 2、3 条收窄为真正未取证的项（kubelet 侧窗口行为；go-nvlib 枚举语义等）。正文 L170、来源记录、登记 revision/notes、`verification.notes` 同步更新；新增取证文件补登记或写入既有登记的覆盖范围。

### B22-C32 — P2 / OPEN：健康标记按物理 UUID 只保留一个设备条目，MIG 多实例与共享副本下"命中即标记对应设备"不成立

位置：正文 L98–101（特别是 L101"MIG 设备按父 UUID＋GI/CI 过滤……命中的 XID 把对应设备标记为 unhealthy"）、L143 GPU 格（"`capacity` 不变而 `allocatable` 下降＝健康事件之后"）。

证据：

- health.go L74 建 `parentToDeviceMap := make(map[string]*Device)`，L79–88 遍历全部设备时执行 `parentToDeviceMap[uuid] = d`。MIG 设备的 `uuid` 是父 GPU 的 UUID（getMigDeviceParts L290–329）；非 MIG 设备取 `d.GetUUID()`（L282–285），该函数去掉副本注解（devices.go L232–235）。
- 副本设备与原设备 UUID 相同、ID 为 `UUID::n`（device_map.go L326–342）。CheckHealth 传入的正是本资源的全部设备，包括副本（nvml_manager.go L106–108）。
- 事件处理先按 `eventUUID` 查出唯一的 `d`（health.go L154–158），再用该 `d` 的 GI/CI 比对（L160–165），不一致即 `continue`。
- 基础 resourceManager 的 CheckHealth 直接返回 nil（rm.go L53–56），WSL 平台使用它（nvml_manager.go L71–73）。

推论（审阅者按代码路径，未执行）：

- 同一父 GPU 上有多个 MIG 实例时，只有最后写入映射的那个实例可能被匹配。带有效 GI/CI 的事件如果属于其他实例会被丢弃；GI/CI 无效时也只标记该实例。
- 时间片/MPS 副本下，一次 XID 只把一个副本标为 Unhealthy：`allocatable` 只减 1，同一物理 GPU 的其余副本仍可调度。
- `Devices` 是 map（devices.go L50–51），保留哪个条目取决于遍历顺序，不确定。
- WSL 平台没有健康检查。tegra 资源管理器未取证。

正文 L101 的转述会让读者以为每个 MIG 实例和副本都能被单独标记。

关闭条件：

- L101 改写为"映射按物理 UUID 只保留一个设备条目"，并按 MIG 多实例与共享副本分别写出后果，标"按代码路径推论，未执行"，引 health.go L74、L88、L154–165 与 device_map.go L326–342。
- 补 WSL 平台无健康检查（rm.go L53–56；nvml_manager.go L71–73），tegra 记 unknown。
- L143 补"共享副本下 allocatable 的下降量不等于受影响的物理设备数"。

### B22-C33 — P2 / OPEN：kubelet 记录的设备 ID 与传给运行时的 ID 混为一谈；共享副本的注解 ID 与过期 ID 拒绝没有写

位置：正文 L89（"`uuid` 策略下分配 ID 即 UUID，`index` 策略下为序号……`index` 序号→UUID 的宿主侧核对方法未取源（K1）"）、L93（"把分配 ID 逗号串直写 `NVIDIA_VISIBLE_DEVICES`"）、L94、L142 GPU"重复/过期分配"格、L147。对应 acceptance 1"稳定设备标识……分配记录"、acceptance 3"重复/过期分配"。

证据：

- **账本侧 ID**：BuildDevice 令 `dev.ID = uuid`（devices.go L90）。ListAndWatch 上报的就是这个 ID（server.go L268、L476–478；devices.go L180–187）。共享副本为 `UUID::n`（devices.go L237–240；device_map.go L326–342）。K8s v1.32 L929–931：PodResources List 给出 `device id as it was reported by device plugins`。因此 **kubelet/PodResources 记录的 ID 与 deviceIDStrategy 无关**，总是 UUID 或带副本注解的 UUID。
- **运行时侧 ID**：`device-id-strategy` 的用途是 `for passing device IDs to the underlying runtime`，默认 uuid（main.go L99–104）。index 分支用 kubelet ID 查本插件的设备表并取 Index（server.go L461–463），Index 在构建时按枚举序 i 赋值（device_map.go L113–128）。所以 index↔UUID 的对应在插件设备表内是确定的；仍未取证的只是"枚举序 i 是否等于宿主侧 nvidia-smi 序号"（go-nvlib 未取）。
- **重复分配**：K8s v1.32 L817 写明 `Devices cannot be shared between containers`，这个约束针对的是设备 ID。共享副本给同一物理 GPU 生成多个不同 ID，不同 Pod 持有 `UUID::0`、`UUID::1` 属于设计内的物理共享。uuid 分支去掉注解并去重（server.go L458–460、L464–473）后，容器拿到的是同一个 UUID。"整数不可超卖"不能排除物理重复。
- **过期分配**：ValidateRequest 对不在当前设备表中的 ID 报 `unknown device`（rm.go L83–89），Allocate 随即失败（server.go L309–311）。重启或重配置后设备集变化时（见 C31），kubelet 仍持有的旧 ID 会走到这一分支（审阅者推论，未执行）。

关闭条件：

- GPU 节把"稳定设备标识"拆成两列：kubelet 记录 ID（PodResources，UUID 或 `UUID::n`）与运行时 ID（env/CDI 名，随 deviceIDStrategy 变化），逐项引 file@commit。
- K1 收窄为"插件枚举序号↔宿主侧 nvidia-smi 序号"。
- L142 补"重复分配须先按 UUID 归一化，并读取共享配置区分设计内共享"，以及 ValidateRequest 的过期 ID 拒绝。
- L93"分配 ID"改为"转换后的运行时 ID"。

### B22-C34 — P2 / OPEN：GPU 回收验证以节点 `allocatable` 为观测量，与正文自己的定义矛盾；Device Plugin API 没有释放回调这一点没有写

位置：正文 L147（"Pod 删除前后各取一次 kubelet PodResources `List` 与节点 `allocatable`"）；对照正文 L51（`allocatable` 不能推出"等于当前空闲设备数"）、L62。

证据：

- K8s v1.32 L887–889：`allocatable` 只因设备健康变化而变。L1004–1011：GetAllocatableResources 给出 `resources initially available on the worker node`，评估空闲资源时 `should be used in conjunction with the List() endpoint`。
- 分配与释放不改变 `allocatable`。在没有健康变化的情况下，Pod 删除前后 `allocatable` 相同，这项观察不提供回收信息。
- L929：List 只覆盖 `running pods`，Pod 删除后条目消失是定义使然，不能证明设备侧已释放。
- L841–863：DevicePlugin 服务没有释放回调，插件不会被告知分配已释放。释放只是 kubelet 侧的记账。

关闭条件：

- 回收验证改为：删除前后各取 `GetAllocatableResources` 的设备 ID 集与 `List` 中运行 Pod 的设备 ID 集，比较两者的差集（空闲集）是否包含原分配的 UUID；同时核对容器留存证据。
- 写明 Device Plugin API 没有释放回调、`allocatable` 不随分配变化。
- 保留"设计，未执行"与"观察记录不作释放完成的充分证明"。

### B22-C35 — P2 / OPEN：Slurm 身份核对、账本刷新条件与新旧作业影响不完整

位置：正文 L118、L123、L125、L133、L142–143 Slurm 列、L148。对应 acceptance 1"step 映射和框架视图"、acceptance 2"daemon 重启和账本刷新条件"、acceptance 3"重复分配"、acceptance 4"身份核对入口"。

证据：

- **cgroup 相对编号**：gres.html L372–384 与 prolog_epilog L467–483 写明：cgroup 约束设备时，作业内 `CUDA_VISIBLE_DEVICES` 是作业可见范围内的序号，分到 `/dev/nvidia1` 的作业内值为 "0"，Prolog/Epilog（cgroup 外）中为 "1"。正文 L148 的身份链"gres.conf `File` ↔ NVML PCI bus 枚举 ↔ `CUDA_DEVICE_ORDER=PCI_BUS_ID` 下框架编号"默认作业内编号是全局编号；在 `ConstrainDevices=yes` 下这一点不成立。
- **身份变量**：gres.html L622–625 的 `SLURM_JOB_GPUS`（`The GPU IDs of GPUs in the job allocation`，在 Prolog/Epilog 等处可用），以及 L369–370"File 按递增数字顺序填写"，都是身份核对的一手入口，正文没有用。正文 L123 的"`scontrol show job` 的 GRES/TRES 字段"在所取 scontrol 页中没有字段定义。
- **账本刷新**：正文 L133"slurmd 重启并重新有效注册是节点 GRES 账本刷新的前提"只来自 INVAL 一种情形（sinfo L900–903）。另外三条明文是：
  - scontrol L1438–1455：文件型 GRES 计数除置零外不能经 scontrol 修改，要改其他值须同时修改 slurm.conf 与 gres.conf 并重启守护进程；scontrol 设置的 GRES 只在 `-R` 重启或 SIGHUP 时保留。
  - slurm.conf L5302–5304：节点配置变更须重启或 reconfigure 全部 slurmctld 与 slurmd。
  - gres.conf L303–305：改 File 记录数前须 drain 节点，否则使用这些 GRES 的作业会被中止。
  - 第三条直接回答了 acceptance 2 的"新旧任务影响"。
- **设计内共享**：gres.conf L286–290 的 MPS/Sharding 例外中，Count 为对应同一 GPU 的条目数。Slurm 侧"重复分配"同样须区分设计内共享。

关闭条件：

- L148 身份链改为：全局身份取 Prolog/Epilog 中的 `CUDA_VISIBLE_DEVICES` 或 `SLURM_JOB_GPUS`，对应 gres.conf `File` 的 minor 号，再经 NVML PCI 顺序对账；作业内编号注明在 `ConstrainDevices=yes` 下是相对编号。
- L133 补上述三条刷新/变更路径，并写明"未先 drain 即改 File 记录数会中止作业"。
- L142 补 shard/MPS 设计内共享。
- 逐项就近引归档页与行区间。

### B22-C36 — P3 / OPEN：K8s 页内锚点失效、改写为推论，以及行锚精度

位置：正文 L52、L62（既有行，本次修订未改动，但属于本次审阅的正文）、L63、L98、L100；来源记录 L9。

证据：

- v1.32 页没有 `#example` 与 `#getallocatableresources-grpc-endpoint`，实际 id 为 `example-pod` 与 `grpc-endpoint-getallocatableresources`。`make check` 不检查远程锚点（authoring-guide §6）。
- L63"未启用时，判断 Pod 是否关联故障设备只能用 PodResources API"：原文 L892–893 是 `Before Kubernetes v1.31, the way to know … is to use the PodResources API`。"未启用门控时只能用"是本库推论，应如实转述或加标注。
- L98 的 health.go 链接没有行锚，正文其他源码链接都有。
- L100 的整句只引 L104–112，而 placement、handle、支持事件三类失败标记在 L79–102。
- 来源记录 L9"RegisterRequest L241–248"应为 L242–249。

关闭条件：改正两个锚点；L63 改为原文转述并把推论单独标注；L98 加 `#L44-L172`；L100 按三类失败分别给 L80–85、L90–95、L97–102，RegisterEvents 给 L104–111；来源记录改行号。

### B22-C37 — P3 / OPEN：NVIDIA 与 Slurm 转述的措辞精度

位置：正文 L99、L102、L108、L118、L129、L131、L143、L148。

证据与改法：

- L108"每次存活不足 1 小时计一次崩溃，累计超过 5 次"：计数在崩溃间隔超过 3600 s 时归零（server.go L206–211），首次间隔从 goroutine 启动算起（L187）。应写"连续 6 次崩溃且相邻间隔都不足 1 h"，不写"累计"。
- L99、L102：`DP_DISABLE_HEALTHCHECKS=all/xids` 时 checkHealth 直接返回 nil（health.go L45–48）；NVML init 失败且 failOnInitError=false 时同样返回 nil（L54–55）。Start 只在返回错误时记日志（server.go L153–156），这两种情形下健康检查是**静默**关闭的。正文"只记日志并继续运行"只覆盖返回错误的情形。
- L118 截断原文：原文为 `could vary between boots after hardware or OS changes. For the most part, this assignment seems fairly stable.`（gres.html L398–399）。应完整引用，或与 Slurm 参考 L133 保持一致。
- L129"`Type`/`Cores`/`Links` 作 sanity check"：gres.conf L211–215 写的是 File、Cores、Links；gres.html 是先用 Type＋File 匹配，再复核 Cores/Links 等属性。
- L131：HealthCheckInterval 默认 0 即不执行（slurm.conf L1345–1346），HealthCheckProgram 默认不配置（L1395）。"之后按间隔……定期执行"须加"配置了 HealthCheckInterval > 0 时"。
- L143 Slurm 格"→invalid+drain"与 L129"两页口径并存"不一致，应同样并列两页口径。
- L148"`scontrol show node` 的 GRES/AllocTRES"：所取 scontrol、sinfo 页中没有 `AllocTRES`（0 命中），`AllocTres` 只出现在 sacct（job/step 记账字段，L646）。"节点回 IDLE"只在没有其他作业时成立。
- L143 昇腾格"无自动对账承诺"是关于"不存在"的断言，应写为"所选来源未见自动对账说明（本库判断）"。

关闭条件：逐条修正。

### B22-C38 — P3 / OPEN：元数据、登记、取证记录、就近引用与指南指向

位置：正文 frontmatter L16–22、L137；Slurm 节 L117–133；来源记录 L3、L5–19；登记 L5242–5246。

证据：

- `related_ids` 没有正文 L137、L149 已链接的 `cluster-platform.ascend-device-visibility-triage`、`cluster-platform.ascend-device-visibility-source-case`、`cluster-platform.ascend-device-visibility-experiment`。
- 登记 `src.nvidia.k8s-device-plugin-v0.20.1` 的 revision 只写 `tag v0.20.1`，URL 用的是可变的 tag。实际 tag 对象为 `03296a61…`，指向 commit `487d7a93894b0f3ad08097169593972eb3ca8206`，可以补上（T05-05 初审 C30 对 Volcano 登记提过同样要求）。license 写"未在本轮打开核对"，而 server.go、health.go 文件头 L1–15 有 Apache 2.0 声明（审阅者同样没有打开仓库根 LICENSE，只作提示）。
- 来源记录没有逐文件哈希与 HTTP 状态；K8s 页经 FetchURL 读取，也没有观察哈希。
- Slurm 节 L117–133 的实质主张旁边没有归档页链接，只有 L113 的路径前缀、站内参考页和 L177 的 gres.html。AGENTS.md 要求在实质主张附近引用精确页面（T05-05 初审 C30 同类）。
- L137"处理动作的前置条件（授权、drain、重排/重启策略）以各生命周期指南为准"：Kubernetes 作业生命周期中没有 drain/cordon/授权类内容，其 L132 又把设备证据链指回本文，形成循环。索引 05.6"节点上下线、升级、发布与变更"仍为待建设。

关闭条件：

- frontmatter 补三个 related_ids。
- 登记补 tag 对象与 commit，URL 改用 commit，并说明 license 口径。
- 来源记录补哈希与状态。
- Slurm 节逐主张就近加归档页链接。
- L137 按指南分别写明覆盖哪项前置条件；K8s 节点 drain/cordon/授权记为"未覆盖（待 05.6 建设）"。

## acceptance 对照

| acceptance | 判定 | 相关发现 |
|---|---|---|
| 1 逐实现列稳定设备标识、capacity/allocatable 或 GRES/TRES、分配记录、容器/step 映射和框架视图，不设计统一错误码 | **部分满足**。成立的部分：三实现分列；L137 明确不设计统一错误码；K8s 账本字段、PodResources、Allocate 三策略、M-ID 引用、Slurm GRES/TRES/step 环境变量都属实。缺口：GPU 侧账本 ID 与运行时 ID 混淆、漏掉副本注解 ID，K1 范围过宽；Slurm 侧缺 cgroup 相对编号与 `SLURM_JOB_GPUS`，"scontrol show job 字段"无出处 | C33、C35（P2）；C37（P3） |
| 2 健康变化、新旧任务/分配影响、插件/daemon 重启和账本刷新条件，依据选定源码/文档逐项核对 | **部分满足**。成立的部分：K8s 文档语义（allocatable/capacity/既有 Pod、ResourceHealthStatus、kubelet 重启、DaemonSet）与 server.go/health.go 行锚逐项属实，降级路径标了推论。缺口：插件重启策略与重启后健康重置在同一 tag 可读却记为 unknown；健康映射按物理 UUID 只保留一个条目这一限制没有写；Slurm 刷新条件只覆盖 INVAL，缺配置变更路径与作业中止风险 | C31（P1）；C32、C35（P2）；C37（P3） |
| 3 对比缺设备、重复/过期分配、账实不符的证据与处理前置条件，引用对应容器/生命周期指南 | **部分满足**。成立的部分：三行×三实现的对照表齐全，链接了四份指南，Slurm 列大体属实。缺口：GPU"缺设备"漏发现失败分支，"账实不符"的"无恢复路径"与 C31 冲突；"重复分配"未区分设计内共享，未写过期 ID 拒绝；K8s 处理前置条件循环引用 | C31（P1）；C33、C35（P2）；C38（P3） |
| 4 维护已有 Ascend 指南/来源案例/方案和未知条件；为 GPU/Slurm 提供同等身份核对/回收验证入口 | **部分满足**。成立的部分：昇腾节未改动，抽查行锚成立；三个入口链接齐全，未知条件委托各页（实验设计页确有回收步骤）；GPU/Slurm 各有身份与回收入口，并标了"设计，未执行"。缺口：GPU 回收以 allocatable 为观测量，与正文定义矛盾；Slurm 身份链缺 cgroup 相对编号；`AllocTRES` 无出处；related_ids 缺三个昇腾页 | C34、C35（P2）；C37、C38（P3） |

横向问题：作者只打开了 source_discovery 明列的两个文件（server.go、health.go），把重启、重建与发现失败整体记为 unknown。这些逻辑实际分布在同一 tag 的 `cmd/nvidia-device-plugin/main.go`、`plugin-manager.go`、`internal/plugin/factory.go` 与 `internal/rm/` 下，都是可读的源码。这与 T05-03 初审横向问题、T05-05 初审 C22 指出的"可取证的内容被记为 unknown"是同一类偏差。

范围外观察（不计入本轮发现）：

- 已闭环的镜像运行时基线 §2"框架映射"行 M-ID ②（L80）同样写"uuid 策略此时分配 ID 即 UUID；若取 index 策略则分配 ID 为序号，序号→UUID 的宿主核对方法未取源，记 K1"。按 C33 的证据，kubelet 侧记录的 ID 与策略无关。修 C33 时作者可评估是否需要对基线发起单独修订；本报告不对 T05-01 提发现。
- 基线 L80 仍引区域锚 `server.go L280–438/L448–481`，作者来源记录 L23 已说明"前轮正文锚未改动"。

## 结论

**T05-04 初审不通过，需修订。B22-C31–C38 共 8 项：P1 ×1（C31），P2 ×4（C32–C35），P3 ×3（C36–C38），全部 OPEN。**

- 修订后须按各项关闭条件做定向复核。
- C31 关闭前，正文 `verification.status: source_checked` 对 NVIDIA 重启与恢复部分不应视为成立：其"无恢复路径"的结论与同一 tag 的重建路径不符，source_discovery 要求的重启策略也没有核查完。
- 正文没有虚构命令输出或实测结果；平台边界（不从 GPU 推导 NPU、不跨固定快照推导）保持得当；Slurm GPU 运行期健康探测记为 unknown 经核对准确。
- 本审阅只覆盖编辑与来源层面。文中 NVIDIA、Kubernetes、Slurm 的行为都是源码或文档层证据，C31/C32 的后果是代码路径推论；审阅者未部署、未运行，不得标为 reproduced。

## 检查记录

- `make check`：`PASS: 96 content entries; 446 sources.`，`Checked structure and local file links; not technical correctness or remote links.`
- `make build`：`PASS: 96 content entries; 446 sources.`，`Built build/catalog.json and build/catalog.md.`（`build/` 在 `.gitignore` 中，运行后 `git status --short` 无输出）。
- 成稿前复取输入哈希：正文 `c96e362c…05aa`、来源记录 `b42352a4…c8c`、计划 `1dd6b549…de71`、登记 `37b1cfb1…b3e3`，与"输入"表一致，审阅期间四个输入未变。
- 本报告是本轮唯一新增文件；未执行 git 提交。

## 模型与运行元数据核验

- 指定模型：`claude-opus-5-5`（authoring-guide §7，2026-10-13/2026-10-16 更新：claude 模型经 `claude -p` 执行）。
- 会话内可见：审阅者会话的系统提示自述模型为 Opus 5.5、模型 ID `claude-opus-5-5`。这是会话自述，**不是** CLI 输出元数据。
- 输出元数据所示实际模型是否为单一 `claude-opus-5-5`：**在审阅者会话内不可核验**。CLI 输出元数据（例如非交互输出中的模型用量字段）对审阅者不可见，须由调用方据实际输出元数据核验并补记于审计。按 §7"每轮审阅必须核验"，核验完成前本轮不宜计入有效轮次。
- 结果文本是否含 `[frontier_llm]` 等 fallback 标记：本报告正文由审阅者撰写，除本节为说明核验项而写出的标记名本身外，不含任何 fallback 标记。调用方仍须对 CLI 原始输出另行检查。
- 执行方式是否为 `claude -p`：会话内不可核验。
- 推理等级等运行元数据：不可核验，不补造。
- 认证/路由：本会话没有遇到模型认证或路由失败。遇到的是工具权限拒绝（`/tmp` 写入、若干 shell 构造需审批）与 GitHub API 403 限流，均不是模型 fallback 的迹象。

## 局限声明

- 模型审阅不构成平台、硬件或现场验证。审阅者没有在任何集群、容器、GPU 或 NPU 上执行命令，没有部署插件或 Slurm，没有运行上游测试；C31、C32 的后果是只读代码路径推论。
- 一次源取证限于上表所列文件与页面。原文未落盘，可复查性依赖所记哈希。
- 本报告的发现与关闭条件不赋予任何执行权限；修订与复核按既有授权进行。
