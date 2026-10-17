# 第二十二批 T05-04 第 2 次定向复核（作者第 2 轮修订后）

复核日期：2026-10-17（开始取哈希 03:43 UTC，成稿前复取 03:47 UTC）。

**结论：第 2 次定向复核不通过。B22-C39–C41 三项全部 CLOSED；本轮新增 B22-C42 一项（P3，OPEN）。B22-C31–C42 共 12 项：CLOSED 11，OPEN 1。没有开放的 P1/P2。**

正文对 C39–C41 的修订逐字落实了关闭条件。审阅者独立取回以下文件与页面：nvml_devices.go（`6a0c4968…`）、device_map.go、health.go、main.go、prolog_epilog.html（`6d83380c…`）、scontrol.html、sbatch.html。哈希与前两轮及作者记录一致，本轮所涉行锚全部属实。第 1 次定向复核的非阻断观察在正文中全部落实。C31–C38 的关闭成果没有被破坏。

新增的 C42 是记录层问题：第 2 轮正文改动没有完整同步到伴随记录。

- 来源记录 unknown 清单第 2 项仍写"NVML 枚举序（go-nvlib `VisitDevices`）"，保留了 C39 要求去除的预设。
- 登记 `src.slurm.docs-24.11.7` 的 revision 没有记 prolog_epilog 重开（该段哈希与上一轮逐字相同），与 `verification.notes` 和来源记录的"六页重开"不一致。
- 来源记录主张表没有收录本轮正文新增的三处主张：prolog_epilog L622–625、validateFlags main.go L209–212、RegisterEvents 其他错误 L108–110。

正文本身无需再改。按前两轮约定，无 OPEN 方可通过，所以本轮不判通过。下一轮只需复核 C42。C42 只涉及文字同步，不需要新来源。

审阅者角色独立于作者，按用户本次要求以 `claude-opus-5-5` 执行；模型与元数据核验见文末专节。本轮只做只读取证与复核：

- 只新增本报告；未改作者正文、来源记录、登记、审计、计划、初审报告或第 1 次定向复核报告。
- 未执行 git 提交。
- 未部署插件、kubelet 或 Slurm，未运行任何集群/设备命令或上游测试。

模型审阅不构成平台、硬件或现场验证。

## 输入（以 SHA-256 识别）

| 输入 | SHA-256 |
|---|---|
| [T05-04 正文](../../knowledge/05-cluster-platform/device-resource-chain.md)（198 行，concept / draft） | `a6c16a3dd3df5e69882103b0ba5feb32195d6e3dc58c1060ca6c512eda599162` |
| [作者来源记录](batch-22-t05-04-sources.md)（58 行） | `475a8966e31632bddae22c52cd73dd1a325147ea1a1116751f93ac3c2a8a515c` |
| [来源登记](../../sources/registry.yaml)（446 项） | `ce6fc28a6b2cc0bc6bebf0957a5ff8fd9521c02e07fd98b145be24bd2ac26c61`；`src.nvidia.k8s-device-plugin-v0.20.1` L5237–5247 段 `d3fcf63d53eac4fd962c4b4354326f0499f8de69590640bce8686a511c0230a2`（本轮已改）；`src.slurm.docs-24.11.7` L5408–5418 段 `af86f1e439a57b0c79d728eb5adde20367cc94b4e6055ee615d7c696312da175`（**与第 1 次定向复核逐字相同，本轮未改**） |
| [批次来源审计](batch-22-source-audit.md)（33 行；T05-04 行 L13） | `234d00ed171c79f2a520ae8b1a1dee1bb269a8ff1945cd34f5c921cad8bbe7df` |
| [初审报告](batch-22-t05-04-claude-review.md) | `626edfdd4b4e7e4d9b83e9d3a9082c79a8245350765ed829c1a87aebededa934`（与第 1 次定向复核时相同） |
| [第 1 次定向复核报告](batch-22-t05-04-claude-recheck.md)（270 行，随 0318bcd 入库） | `88136e299b460bf7570c9ce43ca2fed920aef6e9fc450870dc76863f57ccb8cb` |
| [任务计划](../../plans/full-coverage-backlog.yaml)（T05-04 acceptance L5527–5531） | `1dd6b549c38f4808cfb6d6d80c84e31503354a196c4cbb4c7529988af57fde71`（与前两轮相同） |

git HEAD 为 `0318bcd573d253bf76e626bada8061e495acfb29`，开始时工作区干净。输入哈希在开始（03:43:25 UTC）与成稿前（03:47:43 UTC）各取一次，结果一致，复核期间输入未变。第 1 次定向复核报告由调用方随第 2 轮修订一并入库。本会话没有该报告的 Write 原稿可比，只确认 C39–C41 的证据与关闭条件与本任务所述一致。

## 本轮实际改动（`git diff 741fa93 0318bcd`）

共五个文件：第 1 次定向复核报告（新增）、来源记录（±14 行）、正文（±36 行）、登记（1 行，只改 NVIDIA 条目）、审计（±8 行）。

正文的改动：

- frontmatter `verification.notes`（L34）：改为十文件，并分列哈希口径。
- GPU 节：
  - L87 取证范围改为十文件，加 nvml_devices.go 链接；
  - L94 改写序号赋值；
  - L106–107 修正 health.go 行锚并补 RegisterEvents 其他错误分支；
  - L115 改表头措辞；
  - L119 加"本库判断"；
  - L123、L128 补 validateFlags CDI 分支。
- Slurm 节 L154：② 完整转述 scontrol 持久性。
- 对照表 L162、矛盾观察表 L177：补 CDI 分支。
- 入口节：L168 改比较键，L169 改身份链与 scontrol 括注。
- 适用边界 L189、L191，来源 L196、L198：同步更新。

登记只改了 `src.nvidia.k8s-device-plugin-v0.20.1` 的 revision（L5242，末尾补 nvml_devices.go）。`src.slurm.docs-24.11.7` 没有改动。

## 一次源抽查（审阅者独立获取）

方法：全部用 `curl -sSL` 默认 TLS 校验只读获取。GitHub 文件经 `raw.githubusercontent.com` 按固定 commit `487d7a93894b0f3ad08097169593972eb3ca8206` 取回；HTML 按原文行号核对，未去标签渲染。HTTP 状态码只对 nvml_devices.go、prolog_epilog、scontrol 三项显式打印，均为 200。其余各项未单独打印状态码，但哈希与前两轮 200 响应的哈希逐字一致，内容身份已经确定。

**与任务约定的偏差**：与前两轮相同，原文没有落盘，每次都把 curl 输出经管道直接计算 SHA-256，并读取行区间（`cat -n | sed -n`）。本轮没有重新解析 tag 对象，版本锚 `03296a61…`→`487d7a93…` 沿用初审记录。

### NVIDIA k8s-device-plugin v0.20.1（commit `487d7a93`）

| 文件 | SHA-256 | 核对点与结果 |
|---|---|---|
| [internal/rm/nvml_devices.go](https://github.com/NVIDIA/k8s-device-plugin/blob/487d7a93894b0f3ad08097169593972eb3ca8206/internal/rm/nvml_devices.go)（5825 B，HTTP 200） | `6a0c4968a16235e7482d5caabda542f9c1bf1dc1f71d434cb7a7c6f35958591d`（与第 1 次定向复核、作者记录 L20 一致） | **属实**：`func newNvmlGPUDevice(i int, gpu nvml.Device)`，`index := fmt.Sprintf("%v", i)`（L47–49）；`newWslAllGPUsDevice` 返回 `"all"`（L52–54）；`newMigDevice(i int, j int, …)` 返回 `fmt.Sprintf("%v:%v", i, j)`（L56–58）。→ C39 |
| [internal/rm/device_map.go](https://github.com/NVIDIA/k8s-device-plugin/blob/487d7a93894b0f3ad08097169593972eb3ca8206/internal/rm/device_map.go) | `26d83432c1f05c66270167fd6e0744e1891851ccefebc45e1d9ebc641edac2b5`（同前） | **属实**：WSL 平台 `newGPUDevice = newWslAllGPUsDevice`（L45–47）；`b.VisitDevices(func(i int, gpu device.Device) error {`（L113）；`index, info := b.newGPUDevice(i, gpu)`（L127）；名称不匹配报错（L131）。另读 buildMigDeviceMap（L136–153）：MIG 序号来自 `VisitMigDevices` 回调 (i, j)（L139），`newMigDevice(i, j, mig)` 在 L146；buildGPUDeviceMap 在 MIG 启用且策略非 none 时跳过该 GPU（L122–124）。→ 非阻断观察 1 |
| [internal/rm/health.go](https://github.com/NVIDIA/k8s-device-plugin/blob/487d7a93894b0f3ad08097169593972eb3ca8206/internal/rm/health.go) | `4a955f04be78172901308e3bdd508dc2f78931a4ee5190e2bb6db99f64f6b3b4`（同前） | **属实**：RegisterEvents L104；`ERROR_NOT_SUPPORTED` 只警告（L106–107）；其他错误 `Marking device … as unhealthy` 并送入 unhealthy（L108–110）；L112 为循环右括号。超时 continue 在 L122–124，L124 为其右括号；非超时等待错误标记全部在 L125–131。UUID 解析失败标记全部在 L144–152，L153 为空行。→ 正文 L106–107 新行锚全部准确 |
| [cmd/nvidia-device-plugin/main.go](https://github.com/NVIDIA/k8s-device-plugin/blob/487d7a93894b0f3ad08097169593972eb3ca8206/cmd/nvidia-device-plugin/main.go) | `e48449efbbc74857b66490fa95622c618cdee396b599d9e1d55c440435609d42`（同前） | **属实**：validateFlags 中 `deviceListStrategies.AnyCDIEnabled() && !hasNvml` 返回错误（L209–212）。调用链：startPlugins L371–374 → start L295–298 返回错误 → c.Run 出错 `os.Exit(1)`（L196–200）。正文 L123 把该分支归入"`c.Run` 返回错误"一行，链条成立。kubelet.sock Create 分支 L314–321，L314–316 注释原文为 "Detect a kubelet restart by watching for a newly created 'pluginapi.KubeletSocket' file" |

### Slurm 24.11.7 归档

| 页面 | SHA-256 | 核对点与结果 |
|---|---|---|
| [prolog_epilog](https://slurm.schedmd.com/archive/slurm-24.11.7/prolog_epilog.html)（30707 B，HTTP 200） | `6d83380c65d0dcd57a598b03aa9a046e4c1aae86975a873dc9175cd01731ceac`（与初审、第 1 次定向复核、作者记录 L27 一致） | **属实**：L622–625 `SLURM_JOB_GPUS`："The GPU IDs of GPUs in the job allocation (if any). Available in the Prolog, SrunProlog, TaskProlog, Epilog, SrunEpilog and TaskProlog."（原文 TaskProlog 重复出现）。L467–485 为 `CUDA_VISIBLE_DEVICES` 相对编号说明，L484 为 "See also SLURM_JOB_GPUS"，L485 为 "Available in Prolog and Epilog only." → C40、C41 |
| [scontrol](https://slurm.schedmd.com/archive/slurm-24.11.7/scontrol.html)（151465 B，HTTP 200） | `da776891b3e6070f6e576c5b0f7bcbd62465e976919a1dd62b296050aa4e6d97`（同前） | `AllocTRES` 大小写不敏感 **0 命中**。L1443–1446 为 GRES 计数修改限制；L1452–1456 原文为 "Generic resources assigned via scontrol will only persist across the restart of the slurmctld daemon with the -R option and state files preserved or slurmctld's receipt of a SIGHUP. Update slurm.conf with any changes meant to be persistent across normal restarts of slurmctld or the execution of scontrol reconfig."；命令全名 `reconfigure` 见 L388。→ C40、非阻断观察 2 |
| [sbatch](https://slurm.schedmd.com/archive/slurm-24.11.7/sbatch.html) | `132d28b42e5cb4f9124734b339a9093707d46e30f0b412d2ec12d11f4a10a00f`（与第 1 次定向复核、作者记录 L26 一致） | **属实**：L2926–2928 逐字为 "The global GPU IDs of the GPUs allocated to this job. The GPU IDs are not relative to any device cgroup, even if devices are constrained with task/cgroup. Only set in batch and interactive jobs." |

另核对初审报告：取证表中 prolog_epilog 行（初审报告 L93）为 `6d83380c…`；初审报告中**没有** sbatch 与 nvml_devices.go 的哈希。这是判定 C41 新表述成立的依据。

### 取证限制

- 原文没有落盘，可复查性依赖所记哈希；tag 对象到 commit 的解析本轮没有重做。
- 本轮只取与 C39–C41 及非阻断观察相关的文件与页面。K8s v1.32 页、gres、gres.conf、slurm.conf、sacct、sinfo、tres、cgroup.conf，以及 server.go、plugin-manager.go、factory.go、nvml_manager.go、rm.go、devices.go，本轮正文相关句未改，没有重取，沿用第 1 次定向复核的核对结果。
- go-nvlib `VisitDevices`/`VisitMigDevices` 序号语义、kubelet devicemanager、tegra、CDI handler 仍未取证。正文 L191 所列 unknown 在所选来源下仍然成立。

## 逐项判定

### B22-C39 — P3 / CLOSED

- **L94 序号出处**：已改为"`buildGPUDeviceMap` 把 `VisitDevices` 的回调序号 i 传给 `newGPUDevice`（device_map.go L110–134，传参在 L113、L127），字符串化为十进制串（nvml_devices.go L47–49）"，与关闭条件措辞一致，四处行锚经上表核对属实。
- **取证范围与记录**：nvml_devices.go 已写入正文各处与两份记录：
  - 正文：L87 取证范围改为十文件并附链接，标注"序号字符串化"；L189 改为十份；L196 来源列表已列入；`verification.notes` L34 改为十文件。
  - 来源记录：L3 记"定向复核后补充取证"，哈希表 L20 记 `6a0c4968…`，轮次注"复核后（与定向复核一致）"。
  - 登记：L5242 末句补取 nvml_devices.go 的三处行锚。
- **作者是否独立取回**：作者侧取回操作在审阅者会话内无法核验。来源记录写的是"与定向复核一致"，没有写"与初审一致"，口径符合要求；本轮审阅者再次取回，得到同一哈希。
- **"NVML 枚举序"预设**：
  - 正文已去掉：L94 改称"构建期序号"，并写明"回调序号 i 与 NVML index、宿主 nvidia-smi 序号的关系未取源（go-nvlib `VisitDevices` 语义未取，K1），不因十进制串形式推定一致"。
  - L191 待确认项与来源记录主张表 L41 同步改正。
  - 来源记录 unknown 清单 L58 第 2 项仍有残留。它不在 C39 所列位置（正文 L94、L168）内，单列为 C42。
- **WSL 与 MIG**：WSL 平台的 `"all"` 已补记（L45–47；L52–54），对应原先的可选项。作者另补了 MIG `i:j` 形式，形式断言属实，出处的精度见非阻断观察 1。
- **L168 比较键**：已改为"原分配的账本侧 ID（UUID 或 `UUID::n`）"，与 L93 的两列口径一致。

### B22-C40 — P3 / CLOSED

- **scontrol 括注**：L169 改为"所取 scontrol 页无 AllocTRES 字段定义，现场输出以实际为准"，逐字采用关闭条件措辞，与 L144 对 `scontrol show job` 的口径一致。审阅者复核：scontrol 页 `AllocTRES` 大小写不敏感 0 命中，"无字段定义"有据，缺失断言已去除。
- **身份链**：
  - sbatch 页措辞完整保留并就近链接：global ID、"not relative to any device cgroup, even if devices are constrained with task/cgroup"、"Only set in batch and interactive jobs"。
  - prolog_epilog 页的可用范围逐字引出，同样就近链接："Available in the Prolog, SrunProlog, TaskProlog, Epilog, SrunEpilog and TaskProlog"。重复的 TaskProlog 是原文如此，照录无误。
  - 措辞差异如实并列：prolog_epilog 原文为 "The GPU IDs of GPUs in the job allocation (if any)"，正文写明它没有 global 或"非 cgroup 相对"的限定。
  - 引文与 L622–625 逐字一致。
- L484 "See also SLURM_JOB_GPUS" 核对属实。正文没有单独引这一句，关闭条件也没有要求，不影响关闭。
- 来源侧：来源记录 L3、L27 已记 prolog_epilog 重开。主张表 L48 与登记 Slurm 条目没有同步，见 C42。

### B22-C41 — P3 / CLOSED

- **来源记录表头 L5**：改为"NVIDIA 前九文件与 Slurm gres/gres.conf/slurm.conf/scontrol/sacct/prolog_epilog 的哈希与初审取证表一致；nvml_devices.go 与 sbatch 为初审后新开，哈希与定向复核一致"。审阅者对照初审报告取证表，这一说法逐项成立。哈希表 L20、L26、L27 的轮次注记与表头一致。
- **`verification.notes`（L34）**：同口径，写"前九份哈希与初审一致，nvml_devices.go 哈希与定向复核一致"，以及"重开 gres/gres.conf/slurm.conf/scontrol/sacct/prolog_epilog（六页哈希与初审一致）并新开 sbatch（哈希与定向复核一致）"。
- **勘误说明**：来源记录 L54 补写"初审引文的真实出处……为 prolog_epilog.html L622–625（`6d83380c…`，初审取证表同哈希）……页名误记为 gres.html，引文与行号本身无误"，并保留 sbatch 定位与两页措辞差异。审计 L3 同步记载"初审引文真实出处为 prolog_epilog.html L622–625（页名误记为 gres.html）"。

## 新发现

### B22-C42 — P3 / OPEN：第 2 轮正文改动未完整同步到来源记录与登记

位置：

- 来源记录 L58（unknown 清单第 2 项）、L38、L43、L48；
- 登记 `src.slurm.docs-24.11.7` revision（L5413）；
- 可选：登记 `src.nvidia.k8s-device-plugin-v0.20.1` revision（L5242）。

证据：

1. **unknown 清单残留 C39 的预设。** 来源记录 L58 第 2 项仍是"NVML 枚举序（go-nvlib `VisitDevices`）与宿主 nvidia-smi 序号的关系"。这句把 `VisitDevices` 回调序号等同于 NVML 枚举序，正是 C39 要求去除的预设。正文 L94、L191 与同一记录的主张表 L41 都已改为"回调序号 i 与 NVML index、宿主 nvidia-smi 序号的关系"，同一份记录前后口径不一。审计 L13 说"K1 不再预设 NVML 枚举序"，这一说法目前只对正文和主张表成立。
2. **登记 Slurm 条目的页面清单与其他记录矛盾。** 登记 L5413 仍写"作者侧 curl 重开 gres/gres.conf/slurm.conf/scontrol/sacct 并新开 sbatch"，没有 prolog_epilog。L5408–5418 段哈希 `af86f1e4…` 与第 1 次定向复核逐字相同，说明本轮没有改。`verification.notes`（L34）与来源记录 L3、L5、L27 都写本轮重开了六页，含 prolog_epilog；正文 L169 新增的"Prolog/Epilog 等处可用"主张依赖的正是这一页。对照之下，NVIDIA 条目已为 nvml_devices.go 补记（L5242 末句），Slurm 条目没有对应处理。
3. **主张—来源定位表漏收本轮正文新增的三处主张。**
   - L48 Slurm 行的 `SLURM_JOB_GPUS` 只列"全局 ID"与 sbatch.html L2926–2928，没有 prolog_epilog L622–625 的可用范围与措辞差异。
   - L38 发现失败分支没有 validateFlags CDI 无 NVML 分支（main.go L209–212）；正文 L123、L128、L162、L177 已写。
   - L43 健康检查机制没有 RegisterEvents 其他错误标记（L108–110），仍写"ERROR_NOT_SUPPORTED 只警告 L104–112"和"L124–131""L145–153"。正文 L106–107 已改为 L104–107、L108–110、L125–131、L144–152。登记 L5242 的"启动期标记 L80–112、全设备标记 L124–131/L145–153"同此。
4. 这些都是记录层不一致，不影响正文的技术结论。但来源记录与登记是本库说明"核对过什么"的依据，应与正文和 `verification.notes` 一致，问题性质与 C41 相同。审计 L13 的"第 2 轮修订"摘要因此也略有高估。

关闭条件：

- 来源记录 L58 第 2 项改为与正文 L191 同口径（`VisitDevices` 回调序号与 NVML index、宿主 nvidia-smi 序号的关系）。
- 登记 `src.slurm.docs-24.11.7` 的 revision 补记 T05-04 复核后重开 prolog_epilog（`SLURM_JOB_GPUS` 可用范围 L622–625；哈希见来源记录），使登记、来源记录与 `verification.notes` 的页面清单一致。
- 来源记录主张表补三处定位：L48 加 prolog_epilog L622–625；L38 加 main.go L209–212；L43 加 RegisterEvents 其他错误 L108–110。
- 可选：L43 与登记 L5242 的 health.go 行锚同步为 L104–107、L108–110、L125–131、L144–152。

## 非阻断观察（不计入发现）

1. **MIG 序号的出处。** 正文 L94 写"MIG 为 `i:j` 形式"，只引 nvml_devices.go L56–58，并且放在 buildGPUDeviceMap/`VisitDevices` 那句的括注里。实际上 MIG 设备在 buildMigDeviceMap 中构建：(i, j) 来自 `VisitMigDevices` 回调（device_map.go L139），`newMigDevice(i, j, mig)` 在 L146。buildGPUDeviceMap 遇到 MIG 已启用且策略非 none 的 GPU 会直接跳过（L122–124）。形式断言本身属实。可选补 device_map.go L139、L146，并在 K1 注明 `VisitMigDevices` 的语义同样未取。
2. **第 1 次定向复核非阻断观察的落实情况**：

   | # | 观察 | 落实情况 |
   |---|---|---|
   | 1 | health.go 行锚偏一 | 正文 L107 已改为 L125–131、L144–152，属实。来源记录 L43 与登记 L5242 未改，并入 C42 可选项 |
   | 2 | RegisterEvents 其他错误标记 | 正文 L106 已补（L104–107 只警告；L108–110 同样标记），属实 |
   | 3 | validateFlags CDI 无 NVML 分支 | 正文 L123（重启表 `c.Run` 行）、L128、L162、L177 已补；调用链 startPlugins L371–374 → start L295–298 → c.Run L196–200 成立 |
   | 4 | "本库判断"标注 | L119 已标"与文档所举'监测自身 socket 删除'的关系为本库判断"；L115 表头改为"表中实现位置为只读源码证据"，与表内推断性说明不再冲突 |
   | 5 | scontrol 持久性完整转述 | L154 ② 已写入"`-R` 重启且状态文件保留、或收到 SIGHUP 后保留"和"跨普通重启或 `scontrol reconfigure` 的持久化须写回 slurm.conf"，与 L1452–1456 一致。原文作 `scontrol reconfig`，正文用的是命令全名 `reconfigure`（同页 L388），无实质差异 |
   | 6 | M-ID② 张力 | 审计 L32 仍列为范围外跟进候选，未变 |

3. **审计中的核验表述。** 审计 L13 写"两轮审阅模型元数据均经调用方核验"。第 1 次定向复核报告本身写明该项须由调用方核验；审阅者在会话内无法确认调用方的核验，这里只记录审计中有此表述。

## 波及检查

- **C31**：重启表 L117–124 仍为六行。第 5 行只扩写了触发条件；第 6 行的"上两行"仍指 Serve 崩溃与 `c.Run` 出错，指代没有错位。重建链 L126 与"恢复" L111 未改。
- **C32**：健康粒度 L108 未改。
- **C33**：L93–94 账本侧 ID 与运行时 ID 两列保留，L94 只改了序号出处。
- **C34**：L168 比较键改正后与 L93 口径一致。
- **C35**：L146 相对编号未改；L154 刷新四路径中只扩写了 ②，其余未改；L169 身份链扩写后，全局身份 → `File` minor 号 → NVML PCI 对账的主干不变。
- **C36–C38**：页内锚点、frontmatter `related_ids`、登记 URL 与 license 注记都没有回退。
- **对照表三行 L162–164**：只有 L162 增加了 CDI 分支，L163、L164 未改。
- 没有发现新引入的错误断言、虚构命令或越界推论；新增推论均已标注。
- `make check` 与 `make build` 均通过（见检查记录）。

## acceptance 对照

| acceptance | 判定 | 相关发现 |
|---|---|---|
| 1 逐实现列稳定设备标识、capacity/allocatable 或 GRES/TRES、分配记录、容器/step 映射和框架视图，不设计统一错误码 | **满足**。GPU 序号出处与 K1 边界已理清；账本侧 ID 与运行时 ID 两列口径一致；Slurm 全局与相对编号、`SLURM_JOB_GPUS` 两页口径如实并列；不设计统一错误码（L158） | — |
| 2 健康变化、新旧任务/分配影响、插件/daemon 重启和账本刷新条件，依据选定源码/文档逐项核对 | **满足**。health.go 行锚已修正并补 RegisterEvents 其他错误分支；重启表补 validateFlags 分支；scontrol 持久性完整转述；刷新四路径保持 | — |
| 3 对比缺设备、重复/过期分配、账实不符的证据与处理前置条件，引用对应容器/生命周期指南 | **满足**。缺设备一行补 CDI 无 NVML 分支（L162、L177）；其余两行与前置条件未变 | — |
| 4 维护已有 Ascend 指南/来源案例/方案和未知条件；为 GPU/Slurm 提供同等身份核对/回收验证入口 | **正文满足**。GPU 回收比较键改为账本侧 ID；Slurm 身份链补 Prolog/Epilog 可用范围；scontrol 缺失断言已去除；正文 L191 的未知条件口径正确。来源记录 unknown 清单仍有残留，属记录层问题 | C42（P3，记录层） |

## 结论

**第 2 次定向复核不通过。B22-C39–C41 全部 CLOSED（3/3）；新增 B22-C42（P3）一项，OPEN。累计 B22-C31–C42 共 12 项：CLOSED 11，OPEN 1；没有开放的 P1/P2。**

- 正文没有待改项，acceptance 四项在正文层面均满足。
- C42 只要求来源记录与登记做文字同步，不需要新来源。修订后只对 C42 定向复核；如果修订只涉及 C42 所列位置，不需要重开 C31–C41。
- 正文没有虚构命令输出或实测结果，平台边界保持得当。`verification.status: source_checked` 仍只覆盖来源层核对，不代表 reproduced。

## 检查记录

- `make check`：`PASS: 96 content entries; 446 sources.`，`Checked structure and local file links; not technical correctness or remote links.`
- `make build`：`PASS: 96 content entries; 446 sources.`，`Built build/catalog.json and build/catalog.md.`（`build/` 在 `.gitignore` 中，运行后 `git status --short` 无输出）。两者只说明结构与本地链接通过，不说明技术正确性，也不检查远程锚点。
- 成稿前复取输入哈希：正文 `a6c16a3d…9162`、来源记录 `475a8966…515c`、登记 `ce6fc28a…6c61`、审计 `234d00ed…bbe7df`、初审 `626edfdd…a934`、第 1 次定向复核 `88136e29…cb8cb`、计划 `1dd6b549…de71`，与"输入"表一致。
- 本报告是本轮唯一新增文件；未执行 git 提交。

## 模型与运行元数据核验

- 指定模型：`claude-opus-5-5`（authoring-guide §7，2026-10-13 与 2026-10-16 更新：claude 模型经 `claude -p` 执行）。
- 会话内可见：审阅者会话的系统提示自述模型为 Opus 5.5、模型 ID `claude-opus-5-5`。这是**会话自述**，不是 CLI 输出元数据。
- 输出元数据中的实际模型是否只有 `claude-opus-5-5`：**在审阅者会话内不可核验**。CLI 输出元数据（例如非交互输出中的 `modelUsage`）对审阅者不可见，须由调用方依据实际输出元数据核验，并补记于审计；核验完成前，本轮不宜计入有效轮次。
- 结果文本是否含 `[frontier_llm]` 等 fallback 标记：本报告由审阅者撰写，除本节为说明核验项写出的标记名外，不含任何 fallback 标记。调用方仍须检查 CLI 原始输出。
- 执行方式是否为 `claude -p`：会话内不可核验。推理等级等运行元数据同样不可核验，不补造。
- 认证/路由：本会话没有遇到模型认证或路由失败。遇到的只有一次工具权限审批（含多段 shell 操作的复合命令），已改用单段只读命令完成；另有与本任务无关的 MCP 连接提示。两者都不是模型 fallback 的迹象。

## 局限声明

- 模型审阅不构成平台、硬件或现场验证。审阅者没有在任何集群、容器、GPU 或 NPU 上执行命令，没有部署插件或 Slurm，也没有运行上游测试。重启后以 Healthy 重建、MIG/副本粒度等后果都是只读代码路径推论。
- 本轮一次源取证限于上表所列文件与页面，其余来源沿用前两轮的核对结果。原文没有落盘，可复查性依赖所记哈希；tag 对象到 commit 的解析本轮没有重做。
- 作者侧是否独立取回 nvml_devices.go 与 prolog_epilog，审阅者无法核验，只核对了记录口径与哈希。
- 本报告的发现与关闭条件不赋予任何执行权限；修订与复核按既有授权进行。
