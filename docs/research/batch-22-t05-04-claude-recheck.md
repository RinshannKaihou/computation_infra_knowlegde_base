# 第二十二批 T05-04 定向复核（作者第 1 轮修订后）

复核日期：2026-10-17（成稿前复取哈希时为 03:23 UTC；开始时刻未单独记录）。

**结论：定向复核不通过。初审 8 项（B22-C31–C38）全部 CLOSED；本轮新增 3 项（B22-C39–C41），均为 P3，均 OPEN。B22-C31–C41 共 11 项：CLOSED 8，OPEN 3。没有开放的 P1/P2。**

初审的 P1（C31）已经实质解决。GPU 节新增"重启与账本刷新"表，包括重建链、发现失败分支，"恢复"一条也改成了"进程内无恢复路径、重启即以 Healthy 重建（推论）"，并写出了坏卡重新可调度的反向后果。审阅者取回原文件，逐条核对了 main.go、plugin-manager.go、factory.go、nvml_manager.go、devices.go、server.go 的 20 余个新增行锚，全部属实。C32–C38 的关闭条件也逐项落实。

**作者勘误判定：成立。** 审阅者独立取回 gres.html（`4c7a5874…`，与初审、作者同哈希），全文 742 行，`SLURM_JOB_GPUS` 0 命中；sbatch.html L2926–2928 的措辞与作者引文逐字一致（`132d28b4…`，与作者记录同哈希）。错因经审阅者自查确认：初审所引原文与行区间 L622–625 实际出自 **prolog_epilog.html**（`6d83380c…`，初审取证表同哈希），初审把页面名误记成了 gres.html。详见"初审引证勘误判定"。

新增的三项都是措辞或记录精度问题，没有改变主干结论：

- C39：GPU 侧 index 的赋值位置出处不完整，"NVML 枚举序"一词预设了 K1 尚未取证的语义；回收比较仍以"UUID"为键。后者源自初审 C34 关闭条件的措辞，是审阅者初审写得不严。
- C40：Slurm 入口写成"scontrol 输出无 AllocTRES 字段"，这是超出证据的缺失断言；`SLURM_JOB_GPUS` 在 Prolog/Epilog 中同样可用，正文没有写。
- C41：sbatch 在初审中并无取证记录，来源记录与 `verification.notes` 却写"哈希与初审一致"；勘误说明也没有交代初审引文的真实出处。

按 AGENTS.md 与 authoring-guide §7，发现记录后须经修订与定向复核才能声明通过，所以本轮不判通过。下一轮只需复核 C39–C41。

审阅者角色独立于作者，按用户本次要求以 `claude-opus-5-5` 执行；模型与元数据核验见文末专节。本轮只做只读取证与复核：只新增本报告；未改作者正文、来源记录、登记、审计、计划或初审报告；未执行 git 提交；未部署插件、kubelet 或 Slurm，未运行任何集群/设备命令或上游测试。模型审阅不构成平台、硬件或现场验证。

## 输入（以 SHA-256 识别）

| 输入 | SHA-256 |
|---|---|
| [T05-04 正文](../../knowledge/05-cluster-platform/device-resource-chain.md)（198 行，concept / draft，revise） | `23059f956dd073f0986518b0e2b6177b698849884568a2705d5df53c6d0c489b` |
| [作者来源记录](batch-22-t05-04-sources.md)（56 行，含第 2 轮取证与作者侧哈希表） | `41bd2bda10f445b763e0107ba1a139ff37cdf5752840735577d04d964f663ad0` |
| [来源登记](../../sources/registry.yaml)（446 项；`src.nvidia.k8s-device-plugin-v0.20.1` L5237–5247，`src.slurm.docs-24.11.7` L5408–5418） | `f4769726b5e323b35cd7aad1a1efe0105a45e4b854f3e522a1ff5b47419caa2c`；L5237–5247 段 `8d27aa7af32375b7c87312450aaf8347b5e93bf55d936ae37e8e593ebdcbdf16`；L5408–5418 段 `af86f1e439a57b0c79d728eb5adde20367cc94b4e6055ee615d7c696312da175` |
| [批次来源审计](batch-22-source-audit.md)（33 行；任务状态表 T05-04 行 L13） | `8004bfde7aec5de9a972b0849b774272358985c5280b218b308f16e745828ddb` |
| [初审报告](batch-22-t05-04-claude-review.md)（332 行，随 741fa93 入库） | `626edfdd4b4e7e4d9b83e9d3a9082c79a8245350765ed829c1a87aebededa934` |
| [任务计划](../../plans/full-coverage-backlog.yaml)（T05-04 L5510–5551，acceptance L5527–5531） | `1dd6b549c38f4808cfb6d6d80c84e31503354a196c4cbb4c7529988af57fde71`（与初审相同） |

git HEAD `741fa93d12ddf01013bb5e70d9aa3513018b8071`，开始时工作区干净。输入在开始时与成稿前（03:23 UTC）各取一次哈希，结果一致。初审报告由调用方随修订一并入库；本会话没有初审 Write 原稿可比，只确认其 C31–C38 的内容与本任务所述一致。

## 本轮实际改动（`git diff 981b06a 741fa93`）

共改动五个文件：初审报告（新增）、来源记录、正文、登记、审计。正文的改动：

- frontmatter：`related_ids` 新增三个昇腾页；`verification.notes` 重写。
- L55、L65 两处锚点改正；L66 改为原文转述并单列推论。
- GPU 节 L87–130 整体扩写：取证范围改为九文件、链接改用 commit；ID 拆成两列；新增 ValidateRequest；健康粒度、平台差异、静默关闭与恢复各自成条；新增"重启与账本刷新"表、重建链、发现失败分支。
- Slurm 节 L134–154：逐条加上归档页链接；新增相对编号、MPS/Sharding、File 约束、四条刷新路径。
- 对照表：前置条件句 L158 与三行 L162–164 改写。
- 入口节 L168–169、矛盾观察表 L177–179、适用边界 L189–191、来源 L196/L198 同步更新。

"昇腾例子"节（L71–83）无 diff。

## 一次源抽查（审阅者独立获取）

方法：全部用 `curl -sSL` 默认 TLS 校验只读获取，HTTP 均为 200。GitHub 文件经 `raw.githubusercontent.com` 按固定 commit `487d7a93894b0f3ad08097169593972eb3ca8206` 取回。HTML 按下表哈希对应的原文行号核对（未去标签渲染）。

**与任务约定的偏差**：与初审相同，`mktemp`、`git ls-remote` 和含 shell 变量展开的命令在本会话需要审批，未执行。原文没有落盘，每次都把 curl 输出经管道直接计算 SHA-256，并读取行区间（`cat -n | sed -n`）。因此本轮没有重新解析 tag 对象，版本锚 `03296a61…`→`487d7a93…` 沿用初审记录；内容身份由 commit 固定 URL 的哈希确定。

### NVIDIA k8s-device-plugin v0.20.1（commit `487d7a93`）

九文件哈希与初审取证表、作者来源记录 L11–19 **逐一一致**。

| 文件 | SHA-256 | 核对点与结果 |
|---|---|---|
| [cmd/nvidia-device-plugin/main.go](https://github.com/NVIDIA/k8s-device-plugin/blob/487d7a93894b0f3ad08097169593972eb3ca8206/cmd/nvidia-device-plugin/main.go) | `e48449efbbc74857b66490fa95622c618cdee396b599d9e1d55c440435609d42` | **全部属实**：`fail-on-init-error` Value true、Usage 原文（L68–73）；`pass-device-specs` false（L87–92）；`device-id-strategy` 默认 uuid，Usage "the desired strategy for passing device IDs to the underlying runtime"（L99–104）；`c.Run` 出错 `os.Exit(1)`（L196–200）；`start` L268–347；`restart:` 先 stop 后 start（L285–299）；`restartPlugins` 时 30 s（L301–304），超时 `goto restart`（L311–312）；kubelet.sock Create（L314–321，注释原文一致）；SIGHUP 重启、其余信号 `goto exit`（L330–338）；GetPlugins（L392）；无设备 continue（L402–405）；Start 失败返回 `true`（L408–410）；`No devices found. Waiting indefinitely.`（L415–417）。另读 L203–257 的 validateFlags，见"非阻断观察"3 |
| [cmd/nvidia-device-plugin/plugin-manager.go](https://github.com/NVIDIA/k8s-device-plugin/blob/487d7a93894b0f3ad08097169593972eb3ca8206/cmd/nvidia-device-plugin/plugin-manager.go) | `1142df235c2722708dbd30c6ad207ec2edb4263f802adfdb8f9bf71de58d589d` | **属实**：`plugin.New` L73–80（`WithFailOnInitError` L77），出错包装返回（L81–83）；`CreateSpecFile` L85–87。`cdi.New` 在其前（L52–71），正文未述 |
| [internal/plugin/factory.go](https://github.com/NVIDIA/k8s-device-plugin/blob/487d7a93894b0f3ad08097169593972eb3ca8206/internal/plugin/factory.go) | `fe77bc093ebd2f1adb3293510e92b7e58232b31cdccabe5e21dec170f010d2d1` | **属实**：`New` 调用 `getResourceManagers`（L74）；L93–128；NVML init 失败时 true 返回错误（L104–106），false 返回 `nil, nil`（L107–108）；tegra（L115–116）；无效策略同理（L117–126） |
| [internal/rm/nvml_manager.go](https://github.com/NVIDIA/k8s-device-plugin/blob/487d7a93894b0f3ad08097169593972eb3ca8206/internal/rm/nvml_manager.go) | `198291e96eec164c8f48a66cf763a471a4c231bf430252ca8aa3b6c0bb1f6f26` | **属实**：L39–85；空设备集 continue（L59–62）；WSL 用基础 resourceManager（L71–73）；CheckHealth 传入全部设备（L106–108） |
| [internal/rm/rm.go](https://github.com/NVIDIA/k8s-device-plugin/blob/487d7a93894b0f3ad08097169593972eb3ca8206/internal/rm/rm.go) | `f6dced1f504f604455315999026352d27bc8dd8607ec844b06c2080dfa321c1b` | **属实**：基础 CheckHealth 返回 nil（L53–56）；`unknown device`（L83–89）；副本请求数限制，以 `FailRequestsGreaterThanOne` 为条件（L91–105）。另读 `AddDefaultResourcesToConfig`（L109–150）：只在 `mig-strategy=mixed` 时触及 NVML，并遵守 `FailOnInitError`（L126–131） |
| [internal/rm/devices.go](https://github.com/NVIDIA/k8s-device-plugin/blob/487d7a93894b0f3ad08097169593972eb3ca8206/internal/rm/devices.go) | `e23a3b2e7d3c9fdee9e5e754ed6c334a163bd1c03d52edf126135fc9a340b062` | **属实**：`Devices` 为 map（L50–51）；`dev.ID = uuid`、`dev.Index = index`、`dev.Health = pluginapi.Healthy`（L86–93）；GetPluginDevices（L180–187）；GetUUID 去注解（L232–235）；`%s::%d`（L237–240） |
| [internal/rm/device_map.go](https://github.com/NVIDIA/k8s-device-plugin/blob/487d7a93894b0f3ad08097169593972eb3ca8206/internal/rm/device_map.go)（348 行） | `26d83432c1f05c66270167fd6e0744e1891851ccefebc45e1d9ebc641edac2b5` | **属实**：buildGPUDeviceMap L110–134（`VisitDevices` 回调序号 i 在 L113，`b.newGPUDevice(i, gpu)` 在 L127，名称不匹配报错在 L131）；`setEntry` 调用 `BuildDevice`（L203–204，补全了重建链中间环节，正文未引，但链条成立）；副本构造 L326–342。WSL 平台 `newGPUDevice = newWslAllGPUsDevice`（L45–47）。→ C39 |
| [internal/plugin/server.go](https://github.com/NVIDIA/k8s-device-plugin/blob/487d7a93894b0f3ad08097169593972eb3ca8206/internal/plugin/server.go) | `215f04ab2ee4cbfe8f57cbd65064930b852f0c9678b0314c4aa65f93c6c020d9` | **属实**：Start 中 CheckHealth goroutine 只在出错时记日志（L151–157）；崩溃环 L186–215（L193 `restartCount > 5`，L206–214 超 3600 s 归零、否则加一）；RegisterRequest L242–249；ListAndWatch L268、L277–278；ValidateRequest L309–311；uniqueDeviceIDs L456–474 |
| [internal/rm/health.go](https://github.com/NVIDIA/k8s-device-plugin/blob/487d7a93894b0f3ad08097169593972eb3ca8206/internal/rm/health.go) | `4a955f04be78172901308e3bdd508dc2f78931a4ee5190e2bb6db99f64f6b3b4` | **属实**：L34/L40；全禁 return nil（L45–48）；init 两分支（L50–56）；`parentToDeviceMap` 建立与写入（L74、L88）；启动期标记 L80–85/L90–95/L97–102，RegisterEvents 分支 L104–111（其他错误标记 L108–110）；等待错误 L125–131；UUID 失败 L144–152；意外设备 L154–158；GI/CI L160–167；命中 L169–170；忽略清单 L229–240；placement L282–285 |
| [internal/rm/nvml_devices.go](https://github.com/NVIDIA/k8s-device-plugin/blob/487d7a93894b0f3ad08097169593972eb3ca8206/internal/rm/nvml_devices.go)（审阅者新取，未登记，不在九文件内） | `6a0c4968a16235e7482d5caabda542f9c1bf1dc1f71d434cb7a7c6f35958591d` | `newNvmlGPUDevice`：`index := fmt.Sprintf("%v", i)`（L47–49）；`newWslAllGPUsDevice` 返回 `"all"`（L52–54）；MIG `"%v:%v"`（L56–58）。→ C39 |

### Kubernetes v1.32 Device Plugins

页面 <https://v1-32.docs.kubernetes.io/docs/concepts/extend-kubernetes/compute-storage-net/device-plugins/>，SHA-256 `c954c37a1e3533220f464f5cff88bb49a9f289ce3f8bf8dc3418dc79d04e539a`，与初审相同（可变网页，只代表本次观察）。

- 全页 `<h2/h3 id=…>`（Hugo 输出无引号）：`device-plugin-registration`、`example-pod`、`device-plugin-implementation`、`handling-kubelet-restarts`、`device-plugin-and-unhealthy-devices`、`device-plugin-deployment`、`api-compatibility`、`monitoring-device-plugin-resources`、`grpc-endpoint-list`、`grpc-endpoint-getallocatableresources`、`grpc-endpoint-get`，另有 topology-manager、examples、what-s-next、feedback。
- 正文 10 处页内锚点（L53、L54、L55、L56、L64、L65、L66、L100、L115、L124）**全部可解析**。
- 原文核对：L817 两条约束（整数不可超卖、`Devices cannot be shared between containers.`）；L883 `A device plugin is expected to detect kubelet restarts and re-register itself`，正文 L115 的"要求"属实；L887–889 allocatable/capacity；L892–893 `Before Kubernetes v1.31, …`；L929–931 List。

### Slurm 24.11.7 归档

| 页面 | SHA-256 | 核对点与结果 |
|---|---|---|
| [gres](https://slurm.schedmd.com/archive/slurm-24.11.7/gres.html)（33331 B，742 行） | `4c7a58746e36f07ac7bf43cde934a7342b16698068ceb61ee83debc1c6eccff9` | `SLURM_JOB_GPUS` **0 命中**，`JOB_GPUS` 也是 0 命中；L618–628 为 Sharding 节正文。**属实**：L134–137、L144–146、L283、L288–289、L318–321、L347–354、L369–370（File 递增顺序）、L372–386（Prolog/Epilog 中 "1"、作业内 "0"）、L388–393、L395–401（完整原文含 "For the most part, this assignment seems fairly stable."） |
| [sbatch](https://slurm.schedmd.com/archive/slurm-24.11.7/sbatch.html)（163081 B） | `132d28b42e5cb4f9124734b339a9093707d46e30f0b412d2ec12d11f4a10a00f`（与作者记录一致） | L2926–2928 逐字："The global GPU IDs of the GPUs allocated to this job. The GPU IDs are not relative to any device cgroup, even if devices are constrained with task/cgroup. Only set in batch and interactive jobs." |
| [srun](https://slurm.schedmd.com/archive/slurm-24.11.7/srun.html)（审阅者新取） | `85292ed04c891e084808f174bb90fdb0d32fb2ce49ded874876a3d7257a7cf7b` | L3661 有同一定义（1 处），与作者"srun.html 亦有 1 处"一致 |
| [prolog_epilog](https://slurm.schedmd.com/archive/slurm-24.11.7/prolog_epilog.html) | `6d83380c65d0dcd57a598b03aa9a046e4c1aae86975a873dc9175cd01731ceac`（与初审相同） | L622–625：`SLURM_JOB_GPUS` "The GPU IDs of GPUs in the job allocation (if any). Available in the Prolog, SrunProlog, TaskProlog, Epilog, SrunEpilog and TaskProlog."；L467–485 CUDA_VISIBLE_DEVICES 相对编号，L484 "See also SLURM_JOB_GPUS"。→ 勘误判定、C40 |
| [gres.conf](https://slurm.schedmd.com/archive/slurm-24.11.7/gres.conf.html) | `21aeb902c64844020cca02fe761eb53a8daec7699020d79c7f36d113f47e294e` | **属实**：L211–215（File/Cores/Links，invalid and drained）；L283–290（MPS/Sharding 例外）；L295；L297–301；L303–305 |
| [slurm.conf](https://slurm.schedmd.com/archive/slurm-24.11.7/slurm.conf.html) | `f4151769ed29968c7de408809a5acb8f0591865cd525d5f2c70925e847a1ff34` | **属实**：L1345–1346（默认 0 即不执行）；L1349–1351；L1379–1395（默认不执行程序 L1395）；L5302–5304 |
| [scontrol](https://slurm.schedmd.com/archive/slurm-24.11.7/scontrol.html) | `da776891b3e6070f6e576c5b0f7bcbd62465e976919a1dd62b296050aa4e6d97` | **属实**：L1443–1446；L1452–1456（原文含 "and state files preserved"）。`AllocTRES` 0 命中。→ C40 |
| [sacct](https://slurm.schedmd.com/archive/slurm-24.11.7/sacct.html) | `d96f8299e0b778c8d4cd04a710969f458f118482b122bb99443716ca9ab677f4` | **属实**：`AllocTres` L646–648（job/step、启动后、pending 为空） |
| [sinfo](https://slurm.schedmd.com/archive/slurm-24.11.7/sinfo.html) | `b67afb7958851970875457443f05457b8262a1b4840bcbdbf4accbb792398770` | **属实**：COMPLETING L850–855；INVAL L900–903。无 `AllocTRES`/`CfgTRES` |
| [tres](https://slurm.schedmd.com/archive/slurm-24.11.7/tres.html)、[cgroup.conf](https://slurm.schedmd.com/archive/slurm-24.11.7/cgroup.conf.html) | `2d08f826f585d5f0c663b80406352af8565c6c84c6e675de8e6fd177508691b2`、`8835c19854a487fad4e8485cd30ffb0dc86c0bc49f87070717c20d36cafeca32` | 与初审相同；ConstrainDevices 默认 no（cgroup.conf L226–228）；tres 无 `AllocTRES`/`CfgTRES` |

### 取证限制

- 原文未落盘，可复查性依赖所记哈希。tag 对象→commit 本轮未重新解析（见上文偏差）。
- 未取：go-nvlib `VisitDevices` 序号语义、kubelet devicemanager、tegra 资源管理器、CDI handler（含 `cdi.New` 的失败行为）、gpuallocator。正文 L191 所列 unknown 在所选来源下仍然成立。
- 关于 MIG/副本粒度、重启后以 Healthy 重建的后果，正文与本报告都是只读代码路径推论；未运行插件，未读测试，未核对上游 issue。

## 初审引证勘误判定（`SLURM_JOB_GPUS`）

**判定：作者勘误成立。初审 C35 的引证页名有误。**

1. gres.html（`4c7a5874…`，三方同哈希）全文 742 行，`SLURM_JOB_GPUS` 与 `JOB_GPUS` 均 0 命中。初审所称的 L622–625 在该页是 Sharding 节正文。
2. 作者定位的 sbatch.html L2926–2928 措辞与正文 L169、来源记录 L52 的引文逐字一致；srun.html L3661 有同一定义。
3. **错因（审阅者自查）**：初审引文"The GPU IDs of GPUs in the job allocation"与行区间 L622–625，与 prolog_epilog.html（`6d83380c…`，初审取证表中同哈希）L622–625 完全吻合。原文是 "SLURM_JOB_GPUS The GPU IDs of GPUs in the job allocation (if any). Available in the Prolog, SrunProlog, TaskProlog, Epilog, SrunEpilog and TaskProlog."。初审 C35 括注"在 Prolog/Epilog 等处可用"转述的也是这一条。错的只是页面名，引文与行号本身无误。
4. **权威更正**：初审 C35 证据"身份变量"一条，以及初审取证表 gres 行中"L622–625 `SLURM_JOB_GPUS`"一句，应读作 **prolog_epilog.html L622–625**。按本轮"只新增一个文件"的约定，不改初审文件，以本节为准。
5. 作者勘误不完整：只指向 sbatch/srun，没有追溯到 prolog_epilog 的同名条目。正文因此缺少"Prolog/Epilog 中可用"这一点（→ C40），勘误记录也没有写明初审引文的真实出处（→ C41）。

## 逐项判定

### B22-C31 — P1 / CLOSED

- **重启表**（L117–124）六行齐全，满足关闭条件要求的五类：kubelet.sock 重建、SIGHUP、Start 失败 30 s 重试、进程退出→DaemonSet 重启、每次重启重建设备集。另有 Serve 崩溃环与 `c.Run` 出错两行。表中行锚经上表逐一核对属实。
- **重建链**（L126）：GetPlugins L392 → plugin.New L73–80 → getResourceManagers L93–128 → NewNVMLResourceManagers L39–85 → BuildDevice L86–93。逐环属实。中间环节 `setEntry`→`BuildDevice`（device_map.go L203–204）正文未引，审阅者已核对，链条成立。
- **"恢复"**（L111）：已改为单次进程内无恢复路径、Unhealthy 无持久化、任何重启都以 Healthy 重建（标了推论），双向后果写全。对照表 L164 同步。
- **缺设备**（L128、L162、L177）：补齐四类发现失败分支与 `fail-on-init-error` 默认 true。审阅者另核对 `AddDefaultResourcesToConfig`（rm.go L109–150）：默认旗标下它不会先于 factory 截断 false 分支，正文"false→无插件、无限等待"成立。
- **unknown 收窄**（L130、L191）：只剩 kubelet devicemanager 窗口行为、go-nvlib 枚举语义、tegra、CDI handler。来源记录 L35–36/L56、登记 L5242/L5247、`verification.notes` 同步。
- 抽查新增行锚：main.go 11 处、plugin-manager.go 2 处、factory.go 2 处、nvml_manager.go 2 处、devices.go 1 处、server.go 1 处，全部属实，超过"至少三处"的要求。

### B22-C32 — P2 / CLOSED

- L108 写明映射按物理 UUID 只保留一个条目（health.go L74、L88），先查唯一条目再比 GI/CI（L154–167）；MIG 取父 UUID，副本 GetUUID 去注解（devices.go L232–235）。
- MIG 多实例、共享副本的后果，以及 map 遍历顺序不确定，都标为"按代码路径的推论（未执行）"。
- L109 补 WSL 无健康检查（rm.go L53–56；nvml_manager.go L71–73），tegra 记 unknown。
- L164、L178 补"共享副本下 allocatable 的下降量不等于受影响的物理设备数"。
- 副本构造 device_map.go L326–342 引在 L93 而不在 L108，同节可达，接受。

### B22-C33 — P2 / CLOSED

- L92–94 拆为账本侧 ID 与运行时 ID 两列，逐项引 file@commit 与行号：devices.go L86–93/L237–240、device_map.go L326–342、main.go L99–104、server.go L456–474。
- K1 收窄为"枚举序↔宿主 nvidia-smi 序号"。该句"按 NVML 枚举序"的预设另见 C39。
- L163 补 UUID 归一化、设计内共享区分与 `unknown device` 拒绝；L98 补 ValidateRequest（rm.go L83–89、L91–105）。
- L99 改为"转换后的运行时 ID"；L168 提示两侧 ID 分开记录。

### B22-C34 — P2 / CLOSED

L168 已改为删除前后取 `GetAllocatableResources` 的设备 ID 集与 `List` 运行中 Pod 的设备 ID 集，比较差集。正文写明了：Device Plugin API 没有释放回调（服务清单五项，与初审核对的 K8s 页 L841–863 一致）、`allocatable` 只随健康变化、`List` 只覆盖运行中 Pod、条目消失是定义使然。"设计，未执行""不作充分证明"保留。比较键的 ID 口径残留见 C39。

### B22-C35 — P2 / CLOSED

- **身份链**（L169）：已改为全局身份（`SLURM_JOB_GPUS` 或 Prolog/Epilog 中的 `CUDA_VISIBLE_DEVICES`）→ gres.conf `File` minor 号 → NVML PCI 对账，并注明作业内编号在 `ConstrainDevices=yes` 下是相对编号。L146 有 gres L372–386 与 prolog_epilog L467–483 的出处。
- **刷新四路径**（L154）：scontrol L1443–1456、slurm.conf L5302–5304、gres.conf L303–305、sinfo L900–903，逐项就近链接。"未先 drain 会中止在用作业"已写明。
- **重复格**（L163）：补 MPS/Sharding。
- 勘误判定见上节。`SLURM_JOB_GPUS` 的 Prolog/Epilog 可用性残留见 C40。

### B22-C36 — P3 / CLOSED

- L55 `#example-pod`、L65 `#grpc-endpoint-getallocatableresources` 已改正，并经页内 id 核对。
- L66 原文转述后单列"本库按原文语义的推论"。
- L104 health.go 链接已加 `#L44-L172`。
- L106 分 L80–85/L90–95/L97–102，RegisterEvents 给 L104–112。L112 是循环右括号，与初审建议的 L104–111 相差一行，覆盖实质，接受。
- 来源记录 L33、L50 已改为 L242–249。

### B22-C37 — P3 / CLOSED

八条逐一落实：

1. L122 写"相邻崩溃间隔超 1 小时计数归零……连续第 6 次崩溃 Fatalf"，不再用"累计"；与 server.go L186–215 的逻辑一致（首个间隔从 goroutine 启动算起）。
2. L110 写出两种静默关闭情形，日志条件引 L151–157。
3. L139 引全 NVML 映射原文，与 gres L397–401 逐字一致。
4. L150 sanity check 改为 File/Cores/Links。
5. L152 写明 HealthCheckInterval 默认 0 与"仅当 >0 时"。
6. L162、L164 的 Slurm 格并列两页口径。
7. L169 节点观察已去掉 AllocTRES，改指 sacct `AllocTres`（job/step 字段），并加"无其他作业时回 IDLE"。同句新加的"scontrol 输出无 AllocTRES 字段"属于新引入的缺失断言，单列为 C40。
8. L164 昇腾格改为"所选来源未见……（本库判断）"。

### B22-C38 — P3 / CLOSED

- frontmatter L23–25 补三个昇腾 ID。
- 登记 L5239 的 URL 改用 commit；L5242 补 tag 对象与 commit；L5246 说明 license 口径（文件头 Apache 2.0、根 LICENSE 未开、status 保持 unknown）。
- 来源记录 L9–25 补哈希表。HTTP 状态没有逐行记录，但 15 个哈希都与审阅者本轮 200 响应的哈希逐字一致，内容身份已确定，接受。K8s 页作者侧无哈希，L27 如实说明。
- Slurm 节实质主张均已就近链接归档页。
- L158 前置条件按实现分写，K8s 节点 drain/cordon/授权记为"该页未覆盖，待 05.6 建设"。

## 新发现

### B22-C39 — P3 / OPEN：GPU 侧 index 赋值的出处不全，"NVML 枚举序"预设了 K1；回收比较以"UUID"为键

位置：正文 L94；L168。

证据：

- L94 写"序号在 device_map.go L110–134 按 NVML 枚举序赋值"。device_map.go 只把 `VisitDevices` 的回调序号 i 交给 `b.newGPUDevice`（L113、L127），index 的字符串化在 nvml_devices.go L47–49（`index := fmt.Sprintf("%v", i)`）。该文件由审阅者取回（`6a0c4968…`），不在正文声明的九文件取证范围内，也不在登记 revision 内。WSL 平台换用 `newWslAllGPUsDevice`，index 为 `"all"`（device_map.go L45–47；nvml_devices.go L52–54）。
- "NVML 枚举序"预设了 i 就是 NVML index，而同一句又声明 go-nvlib `VisitDevices` 语义未取（K1）。如果 i 等于 NVML index，nvidia-smi 又按 NVML 编号，K1 就基本被预先回答了。gres.html L389–390 "NVML (which powers the nvidia-smi tool)…" 是 Slurm 页的说法，不能跨来源套到 NVIDIA 插件上。措辞与本句自己的 unknown 声明相抵触。
- L168 写"比较差集（空闲集）是否包含原分配 UUID"。按 L93 本页的口径，`GetAllocatableResources` 与 `List` 给出的是账本侧 ID，共享副本下为 `UUID::n`；以 UUID 为键做集合比较，在共享配置下会查不到。这一措辞直接沿用了初审 C34 关闭条件的原文"原分配的 UUID"，是审阅者初审写得不严；C33 的两列口径落地后应一并改正。

关闭条件：

- L94 改为"index 取 `VisitDevices` 回调序号 i 的十进制串（device_map.go L113、L127；nvml_devices.go L47–49）"。把 nvml_devices.go 写入取证范围、来源记录与登记；或者删去关于字符串化的断言，只引 device_map.go 的传参。
- 去掉"NVML 枚举序"的预设，把 i 与 NVML index、nvidia-smi 序号的关系统一归入 K1。WSL 下 index 为 `"all"` 可选补记。
- L168 改为"原分配的账本侧 ID（UUID 或 `UUID::n`）"。

### B22-C40 — P3 / OPEN：Slurm 入口两处措辞：scontrol 输出字段的缺失断言；`SLURM_JOB_GPUS` 在 Prolog/Epilog 的可用性未写

位置：正文 L169。

证据：

- L169 括注"scontrol 输出无 AllocTRES 字段"。所取 scontrol.html（`da776891…`）`AllocTRES` 0 命中，tres、gres、sinfo 页也是 0 命中；所取页面都没有定义 `scontrol show node` 的输出字段。证据只能支持"所取页面无该字段定义"，不能支持"输出中没有该字段"。同页 L144 对 `scontrol show job` 写的是"所取 scontrol 页没有 GRES 输出字段定义，按现场输出读取"，口径恰当，L169 与之不一致。这是修正 C37 时新引入的缺失断言，与初审 C37 指出的昇腾格"无自动对账承诺"同类。
- L169 身份链对 `SLURM_JOB_GPUS` 只引 sbatch 的 "Only set in batch and interactive jobs"。prolog_epilog.html L622–625 写明该变量在 Prolog、SrunProlog、TaskProlog、Epilog、SrunEpilog 中可用；同页 L484 紧接在 `CUDA_VISIBLE_DEVICES` 相对编号说明之后写 "See also SLURM_JOB_GPUS"。身份链正是要在 Prolog/Epilog 这种 cgroup 外环境中取全局编号，只写"只设于 batch/交互作业"，会让读者以为 Prolog/Epilog 内取不到。两页措辞也不同：prolog_epilog 只写 "GPU IDs"，"global""not relative to any device cgroup"出自 sbatch/srun。

关闭条件：

- L169 括注改为"所取 scontrol 页无 AllocTRES 字段定义，现场输出以实际为准"，或删去该括注。
- 身份链补上 prolog_epilog L622–625 的可用范围并就近链接；保留 sbatch 的 global/非 cgroup 相对措辞及其出处，两页措辞差异如实并列。

### B22-C41 — P3 / OPEN：勘误记录不完整；"哈希与初审一致"的说法对 sbatch 不成立

位置：来源记录 L5、L52；正文 `verification.notes`（L34）；批次审计 L3、L13。

证据：

- 初审取证表只有十页：gres、gres.conf、tres、cgroup.conf、slurm.conf、sinfo、prolog_epilog、scontrol、sacct、scancel，没有 sbatch。
- 来源记录 L5 的表头写"与初审取证表逐一一致"，与 L25 sbatch 行标的"2（新开）"矛盾。`verification.notes` 写"重开 gres/gres.conf/slurm.conf/scontrol/sacct/sbatch……（哈希与初审一致）"，同样把 sbatch 包括在内。
- 审阅者本轮独立取回 sbatch 得 `132d28b4…`，与作者记录一致，所以哈希本身无误，只是"与初审一致"这一说法对 sbatch 不成立。
- 来源记录 L52 与审计 L3/L13 的勘误说明只写了"实际定义在 sbatch.html"，没有交代初审引文的真实出处 prolog_epilog.html L622–625（见"初审引证勘误判定"）。读者会因此以为初审引文没有出处。

关闭条件：

- 来源记录表头与 `verification.notes` 改为"gres/gres.conf/slurm.conf/scontrol/sacct 五页哈希与初审一致；sbatch 为新开（`132d28b4…`）"。
- 勘误说明补"初审引文与行区间出自 prolog_epilog.html L622–625，页名误记为 gres.html"，审计同步。

## 非阻断观察（不计入发现）

1. health.go 事件循环有两处既有行锚偏一行：L107 的"L124–131"实为 L125–131（L124 是超时分支的右括号），"L145–153"实为 L144–152。范围覆盖实质，不影响结论。
2. L106 的启动期标记没有写 `RegisterEvents` 返回其他错误时同样标记（health.go L108–110）。初审取证表列过这一行，但关闭条件未单列。
3. 有一条发现失败旁支，初审与修订都没有覆盖：`validateFlags` 在启用 CDI 设备列表策略而 `HasNvml` 为假时无条件报错（main.go L209–212），经 `start` 返回后 `os.Exit(1)`，不受 `fail-on-init-error` 影响。此外 GetPlugins 中 `cdi.New` 先于 `plugin.New`（plugin-manager.go L52–71），其失败行为属于未取证的 CDI handler。可选补入 L128。
4. L119"与文档所举'监测自身 socket 删除'是同一信号链的不同侧重"是解释性判断，却放在"均为只读源码证据"的表头之下，建议标为"本库判断"。
5. L154 ② 转述 scontrol 持久性时省略了原文 "and state files preserved"（L1453），以及 L1455–1456 关于持久化须更新 slurm.conf 的句子。不改变结论。
6. 镜像运行时基线 §2 M-ID② 的"分配 ID"措辞与本文两列口径之间的张力，已由审计 L32 列为范围外跟进候选，处理得当。

## acceptance 对照

| acceptance | 判定 | 相关发现 |
|---|---|---|
| 1 逐实现列稳定设备标识、capacity/allocatable 或 GRES/TRES、分配记录、容器/step 映射和框架视图，不设计统一错误码 | **满足**。GPU 账本侧/运行时 ID 分列；Slurm 相对/全局编号与 `SLURM_JOB_GPUS` 出处属实；`AllocTres` 改为 sacct job/step 字段；不设计统一错误码（L158）。残留只是 index 出处与预设的措辞 | C39（P3） |
| 2 健康变化、新旧任务/分配影响、插件/daemon 重启和账本刷新条件，依据选定源码/文档逐项核对 | **满足**。NVIDIA 重启六路径、重建链、健康粒度、静默关闭均有行锚；Slurm 刷新四路径与 drain 前置均有归档页；剩余 unknown 都是所选来源确实未覆盖的项 | — |
| 3 对比缺设备、重复/过期分配、账实不符的证据与处理前置条件，引用对应容器/生命周期指南 | **满足**。三行 × 三实现补全（发现失败分支、设计内共享、过期 ID 拒绝、重建推论、下降量≠物理数）；前置条件按实现分写，K8s 缺口如实记为待 05.6 建设 | — |
| 4 维护已有 Ascend 指南/来源案例/方案和未知条件；为 GPU/Slurm 提供同等身份核对/回收验证入口 | **基本满足**。昇腾节未改动，related_ids 已补；GPU 回收改为集合差集比较；Slurm 身份链改为全局身份。残留：比较键 ID 口径；Prolog/Epilog 中 `SLURM_JOB_GPUS` 未写；scontrol 输出的缺失断言 | C39、C40（P3） |

## 结论

**定向复核不通过。B22-C31–C38 全部 CLOSED（8/8）；新增 B22-C39–C41 三项 P3，均 OPEN。没有开放的 P1/P2。**

- C31 关闭后，初审"`verification.status: source_checked` 对 NVIDIA 重启与恢复部分不应视为成立"的保留意见解除。该状态只覆盖来源层核对，不代表 reproduced。
- 正文没有虚构命令输出或实测结果。平台边界保持得当：没有从 GPU 推导 NPU（L134、L163–164），没有跨固定快照推导（L189）；新增的推论都有标注，非阻断观察 4 那一句除外。
- 作者勘误成立；初审页名误记的权威更正见"初审引证勘误判定"。
- 建议作者按 C39–C41 做文字级修订。除可选地把 nvml_devices.go 纳入取证外，不需要新的来源。之后只对 C39–C41 定向复核。

## 检查记录

- `make check`：`PASS: 96 content entries; 446 sources.`，`Checked structure and local file links; not technical correctness or remote links.`
- `make build`：`PASS: 96 content entries; 446 sources.`，`Built build/catalog.json and build/catalog.md.`（`build/` 在 `.gitignore` 中，运行后 `git status --short` 无输出）。两者只说明结构与本地链接通过，不说明技术正确性，也不检查远程锚点。
- 成稿前复取输入哈希：正文 `23059f95…489b`、来源记录 `41bd2bda…3ad0`、登记 `f4769726…caa2c`、审计 `8004bfde…ddb`、初审 `626edfdd…a934`、计划 `1dd6b549…de71`，与"输入"表一致，复核期间输入未变。
- 本报告是本轮唯一新增文件；未执行 git 提交。

## 模型与运行元数据核验

- 指定模型：`claude-opus-5-5`（authoring-guide §7，2026-10-13/2026-10-16 更新：claude 模型经 `claude -p` 执行）。
- 会话内可见：审阅者会话的系统提示自述模型为 Opus 5.5、模型 ID `claude-opus-5-5`。这是**会话自述**，不是 CLI 输出元数据。
- 输出元数据中的实际模型是否只有 `claude-opus-5-5`：**在审阅者会话内不可核验**。CLI 输出元数据（例如非交互输出中的 `modelUsage`）对审阅者不可见，须由调用方依据实际输出元数据核验，并补记于审计。审计 L13 记载初审一轮已由调用方核验（`modelUsage` 仅 `claude-opus-5-5`）；本轮须另行核验，核验完成前不宜计入有效轮次。
- 结果文本是否含 `[frontier_llm]` 等 fallback 标记：本报告由审阅者撰写，除本节为说明核验项写出的标记名外，不含任何 fallback 标记。调用方仍须检查 CLI 原始输出。
- 执行方式是否为 `claude -p`：会话内不可核验。推理等级等运行元数据不可核验，不补造。
- 认证/路由：本会话没有遇到模型认证或路由失败。遇到的是工具权限审批（`mktemp`、`git ls-remote`、shell 变量展开、`--word-diff` 管道），以及本会话无关的 MCP 连接提示，都不是模型 fallback 的迹象。

## 局限声明

- 模型审阅不构成平台、硬件或现场验证。审阅者没有在任何集群、容器、GPU 或 NPU 上执行命令，没有部署插件或 Slurm，没有运行上游测试。重启后以 Healthy 重建、MIG/副本粒度等后果都是只读代码路径推论。
- 一次源取证限于上表所列文件与页面。原文没有落盘，可复查性依赖所记哈希；tag 对象到 commit 的解析本轮未重做。
- 本报告的发现与关闭条件不赋予任何执行权限；修订与复核按既有授权进行。
