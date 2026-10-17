# 第二十二批 T05-04 第 3 次定向复核（C42 记录层同步后）

复核日期：2026-10-17（开始取哈希 03:55:34 UTC，成稿前复取 03:58:43 UTC）。

**结论：第 3 次定向复核不通过。B22-C42 CLOSED；本轮新增 B22-C43 一项（P3，OPEN）。B22-C31–C43 共 13 项：CLOSED 12，OPEN 1。没有开放的 P1/P2。**

C42 的三项必需关闭条件全部落实：

- 来源记录 unknown 清单第 2 项已去掉"NVML 枚举序"预设，与正文 L191 同口径；
- 登记 `src.slurm.docs-24.11.7` 已补记 prolog_epilog 重开；
- 主张表已补收 prolog_epilog L622–625、validateFlags main.go L209–212、RegisterEvents 其他错误 L108–110 三处。

可选项中，来源记录 L43 的 health.go 行锚已同步；登记 L5242 未同步，因为是可选项，不影响关闭。正文唯一改动（L94 MIG 句补 `VisitMigDevices` 出处）经审阅者独立取回 device_map.go 核实属实，没有其他正文改动。

新增的 C43 也是记录层问题。审计文件 L1 标题与 L13 状态行已改为"待第 3 次定向复核"，但同一文件 L3（更新日期段）仍写"作者第 2 轮修订……已完成，待第 2 次定向复核"，L31（待办 2）仍写"待第 2 次定向复核关闭 B22-C39–C41"，而且两处都没有记第 2 次定向复核的结果。同一份状态记录前后矛盾。上一轮提交 0318bcd 曾同步更新 L1/L3/L13/L31 四处，本轮只改了 L1/L13。

正文与来源记录、登记无需再改。按前几轮约定，无 OPEN 方可通过，所以本轮不判通过。下一轮只需复核 C43。C43 只涉及审计文件两句文字，不需要新来源，也不需要重开 C31–C42。

审阅者角色独立于作者，按用户本次要求以 `claude-opus-5-5` 执行；模型与元数据核验见文末专节。本轮只做只读取证与复核：

- 只新增本报告；未改作者正文、来源记录、登记、审计、计划或此前任何审阅报告。
- 未执行 git 提交。
- 未部署插件、kubelet 或 Slurm，未运行任何集群/设备命令或上游测试。

模型审阅不构成平台、硬件或现场验证。

## 输入（以 SHA-256 识别）

| 输入 | SHA-256 |
|---|---|
| [T05-04 正文](../../knowledge/05-cluster-platform/device-resource-chain.md)（198 行，concept / draft） | `f2b933842cca3b6b5f943b25a3261530aaf09404813c7687f8b69fde25c91449` |
| [作者来源记录](batch-22-t05-04-sources.md)（58 行） | `3e1b47262a3b356f462017aee892c25a29d5c67f8e880901dd093d26d6bbfc7d` |
| [来源登记](../../sources/registry.yaml)（446 项） | `0a40323ac4c63b7b565d27716a1d6d6856a3880d1797c4341e283cafc89d4700`；`src.nvidia.k8s-device-plugin-v0.20.1` L5237–5247 段 `37fd4b941badeec06d78e47452a130b681b37369714d7cca277a54c5b25db225`（上一轮 `d3fcf63d…`，本轮已改）；`src.slurm.docs-24.11.7` L5408–5418 段 `dde5967008aa4121f035dc0b605e3f86c3cbab1a93ec636c6cf92540dd96f43a`（上一轮 `af86f1e4…`，本轮已改） |
| [批次来源审计](batch-22-source-audit.md)（33 行；T05-04 行 L13） | `4e19c31c7d5d34b63bccdf3ca779723ac00e68d5d08758d6c09c1d73e4430db4` |
| [初审报告](batch-22-t05-04-claude-review.md) | `626edfdd4b4e7e4d9b83e9d3a9082c79a8245350765ed829c1a87aebededa934`（与前两轮相同） |
| [第 1 次定向复核报告](batch-22-t05-04-claude-recheck.md) | `88136e299b460bf7570c9ce43ca2fed920aef6e9fc450870dc76863f57ccb8cb`（与第 2 次定向复核时相同） |
| [第 2 次定向复核报告](batch-22-t05-04-claude-recheck-2.md)（218 行，随 4b4c077 入库） | `1b39e5f1c637f613617d7aeb7c96ee31b2f3abfd559da6b7e94c41ffb3798fac` |
| [任务计划](../../plans/full-coverage-backlog.yaml)（T05-04 acceptance L5527–5531） | `1dd6b549c38f4808cfb6d6d80c84e31503354a196c4cbb4c7529988af57fde71`（与前三轮相同） |

git HEAD 为 `4b4c077376b0f7f96c70a78f5b009a30432e209f`，开始时 `git status --short` 无输出。输入哈希在开始（03:55:34 UTC）与成稿前（03:58:43 UTC）各取一次，两个登记段哈希也一并复取，结果全部一致，复核期间输入未变。第 2 次定向复核报告由调用方随 C42 同步一并入库。本会话没有该报告的 Write 原稿可比，只确认其所列 C42 三项内容与本任务所述一致。

## 本轮实际改动（`git show 4b4c077`）

共五个文件：第 2 次定向复核报告（新增 218 行）、来源记录（±4 行）、正文（±1 行）、登记（±2 行）、审计（±2 行）。

- **来源记录**：主张表 L38（发现失败分支）、L43（健康检查机制）、L48（Slurm 行）改写；unknown 清单 L58 第 2 项改写。
- **登记**：NVIDIA 条目 L5242 revision 末句补 MIG `i:j` 的 i、j 出处；Slurm 条目 L5413 revision 末尾补 prolog_epilog 重开。
- **正文**：只改 L94（"运行时 ID"条 MIG 句）。`git diff 0318bcd 4b4c077 -- knowledge/` 为 1 个文件、1 行增 1 行删，没有其他正文改动；frontmatter（含 `updated_at: "2026-10-17"`、`verification.notes`）未变。
- **审计**：L1 标题与 L13 T05-04 状态行改写；L3 与 L31 未改（见 C43）。

## 一次源抽查（审阅者独立获取）

方法：全部用 `curl -sSL` 默认 TLS 校验只读获取。GitHub 文件经 `raw.githubusercontent.com` 按固定 commit `487d7a93894b0f3ad08097169593972eb3ca8206` 取回；HTML 按原文行号核对，未去标签渲染。HTTP 状态码对 device_map.go 与 prolog_epilog 显式打印，均为 200。main.go 与 health.go 未单独打印状态码，但哈希与前三轮 200 响应的哈希逐字一致，内容身份已经确定。

**与任务约定的偏差**：与前几轮相同，原文没有落盘，每次都把 curl 输出经管道直接计算 SHA-256，并读取行区间（`cat -n | sed -n`）。本轮没有重新解析 tag 对象，版本锚 `03296a61…`→`487d7a93…` 沿用初审记录。

| 文件 / 页面 | SHA-256 | 核对点与结果 |
|---|---|---|
| [internal/rm/device_map.go](https://github.com/NVIDIA/k8s-device-plugin/blob/487d7a93894b0f3ad08097169593972eb3ca8206/internal/rm/device_map.go)（HTTP 200） | `26d83432c1f05c66270167fd6e0744e1891851ccefebc45e1d9ebc641edac2b5`（与前几轮、来源记录 L19 一致） | **属实**：buildMigDeviceMap（L136–153）中 `b.VisitMigDevices(func(i int, d device.Device, j int, mig device.MigDevice) error {` 在 L139；`index, info := newMigDevice(i, j, mig)` 在 L146。buildGPUDeviceMap 的 `VisitDevices` 回调（L113）、`newGPUDevice(i, gpu)`（L127）、MIG 启用且策略非 none 时跳过（L122–124）同前。→ 正文 L94、登记 L5242 |
| [prolog_epilog](https://slurm.schedmd.com/archive/slurm-24.11.7/prolog_epilog.html)（30707 B，HTTP 200） | `6d83380c65d0dcd57a598b03aa9a046e4c1aae86975a873dc9175cd01731ceac`（与初审、前两次定向复核、来源记录 L27 一致） | **属实**：L622–625 `SLURM_JOB_GPUS` 原文 "The GPU IDs of GPUs in the job allocation (if any). Available in the Prolog, SrunProlog, TaskProlog, Epilog, SrunEpilog and TaskProlog."；L484 为 `CUDA_VISIBLE_DEVICES` 条目内的 "See also SLURM_JOB_GPUS"，L485 "Available in Prolog and Epilog only."。L622–625 条目内**没有**反向引用 `CUDA_VISIBLE_DEVICES`（见非阻断观察 3）。→ 登记 L5413、主张表 L48 |
| [cmd/nvidia-device-plugin/main.go](https://github.com/NVIDIA/k8s-device-plugin/blob/487d7a93894b0f3ad08097169593972eb3ca8206/cmd/nvidia-device-plugin/main.go) | `e48449efbbc74857b66490fa95622c618cdee396b599d9e1d55c440435609d42`（同前） | **属实**：L209 `hasNvml, _ := infolib.HasNvml()`；L210–212 `deviceListStrategies.AnyCDIEnabled() && !hasNvml` 时返回 "CDI --device-list-strategy options are only supported on NVML-based systems"。→ 主张表 L38 |
| [internal/rm/health.go](https://github.com/NVIDIA/k8s-device-plugin/blob/487d7a93894b0f3ad08097169593972eb3ca8206/internal/rm/health.go) | `4a955f04be78172901308e3bdd508dc2f78931a4ee5190e2bb6db99f64f6b3b4`（同前） | **属实**：L104 `RegisterEvents`，L106–107 `ERROR_NOT_SUPPORTED` 只警告，L108–110 其他错误标记并送入 unhealthy；L122–124 超时 continue（L124 为右括号）；L125–131 非超时等待错误标记全部；L144–152 UUID 解析失败标记全部（L153 为空行）；启动期另三处标记 L80–85/L90–95/L97–102。→ 主张表 L43 的 L104–107、L108–110、L125–131、L144–152 全部准确 |

### 取证限制

- 原文没有落盘，可复查性依赖所记哈希；tag 对象到 commit 的解析本轮没有重做。
- 本轮只取与 C42 新增行锚及正文 L94 改动直接相关的四个文件与页面。其余来源本轮正文与记录相关句未改，没有重取，沿用前几轮的核对结果。
- go-nvlib `VisitDevices`/`VisitMigDevices` 序号语义、kubelet devicemanager、tegra、CDI handler 仍未取证。正文 L191 与来源记录 L58 所列 unknown 在所选来源下仍然成立。

## 逐项判定

### B22-C42 — P3 / CLOSED

按第 2 次定向复核所列关闭条件逐条核对：

1. **来源记录 unknown 清单第 2 项**：L58 已改为"`VisitDevices` 回调序号与 NVML index、宿主 nvidia-smi 序号的关系（go-nvlib 未取，不以十进制串形式推定一致）"，与正文 L191"`VisitDevices` 回调序号与 NVML index、宿主 nvidia-smi 序号的关系（go-nvlib 未取）"及主张表 L41 同口径。来源记录全文 grep"枚举序"为 **0 命中**，正文全文同为 0 命中。**满足**。
2. **登记 Slurm 条目补 prolog_epilog**：L5413 revision 末尾补"定向复核后再重开 prolog_epilog（L622–625 SLURM_JOB_GPUS 可用范围、L484 互引，哈希与初审一致）"；同一字段前文已写"SHA-256 见 batch-22-t05-04-sources.md"，来源记录 L27 为 `6d83380c…`，与初审取证表、本轮取回一致。页面清单核对如下，三处所指 Slurm 页集合一致，均为七页：
   - 登记：第 2 轮重开 gres/gres.conf/slurm.conf/scontrol/sacct、新开 sbatch，复核后重开 prolog_epilog；
   - 来源记录：L3 写"第 2 轮……重开 Slurm 归档六页"，另写"定向复核后……重开 prolog_epilog.html"；哈希表 L21–27 共七行；
   - `verification.notes`（L34）：写"重开 gres/gres.conf/slurm.conf/scontrol/sacct/prolog_epilog（六页哈希与初审一致）并新开 sbatch"。

   "六页"在来源记录 L3 与 `verification.notes` 中的分组口径不同，前者含 sbatch，后者含 prolog_epilog。但页面集合与轮次说明可以互相推出，不构成矛盾，属于 C42 范围之外的既有措辞，不重开。"L484 互引"的措辞见非阻断观察 3。**满足**。
3. **主张表补三处定位**：
   - L48 Slurm 行：主张栏补"SLURM_JOB_GPUS 全局 ID（sbatch 措辞 global/非 cgroup 相对）与 Prolog/Epilog 可用范围（prolog_epilog 措辞无 global 限定，两页差异并列）"，定位栏补"prolog_epilog.html L622–625/L484"。与正文 L169 的并列表述一致，行锚经本轮取回属实。
   - L38 发现失败分支：主张栏补"CDI 策略无 NVML 时 validateFlags 无条件报错"，定位栏补"main.go L209–212"，属实。
   - L43 健康检查机制：主张栏补"RegisterEvents 的 ERROR_NOT_SUPPORTED 只警告 L104–107、其他错误同样标记 L108–110"，与正文 L106 一致。

   **满足**。
4. **可选项**：
   - 来源记录 L43 定位栏的 health.go 行锚已同步：L124–131→L125–131、L145–153→L144–152，主张栏 L104–112→L104–107/L108–110。经本轮取回全部属实。
   - 登记 L5242 仍写"启动期标记 L80–112、全设备标记 L124–131/L145–153"，**未同步**。这是关闭条件明确标"可选"的一项，不影响关闭，见非阻断观察 1。

**作者侧"已核实"device_map.go L139/L146**（审计 L13）：作者侧取回操作在审阅者会话内无法核验。审阅者本轮独立取回同一哈希的 device_map.go，两处行锚属实。

C42 的必需关闭条件全部满足，判 **CLOSED**。

### 正文 L94 改动（第 2 次定向复核非阻断观察 1 的落实）

- 改动后原文："MIG 为 `i:j` 形式，i、j 来自 `VisitMigDevices` 回调（device_map.go L139/L146），格式串在 nvml_devices.go L56–58"。
- 与源码核对：L139 为 `VisitMigDevices` 回调签名 `(i int, d device.Device, j int, mig device.MigDevice)`，L146 把 (i, j) 传给 `newMigDevice`；nvml_devices.go L56–58 的格式串第 2 次定向复核已核实（`6a0c4968…`）。出处与形式断言都成立。
- 新增句没有对 j 与宿主 nvidia-smi MIG 设备序号的关系作任何断言，没有引入新的预设。
- 原观察的可选后半句"在 K1 注明 `VisitMigDevices` 的语义同样未取"没有采纳，见非阻断观察 2。
- 没有改动链接、frontmatter 或其他句子。

## 新发现

### B22-C43 — P3 / OPEN：审计文件 L3、L31 的 T05-04 状态未随本轮同步，与 L1、L13 矛盾

位置：[批次来源审计](batch-22-source-audit.md) L3（更新日期段末句）、L31（待办 2 括注）。

证据：

1. **同一文件内状态矛盾。** L1 标题写"T05-04 C42 记录层同步完成、待第 3 次定向复核"，L13 状态栏写"C42 记录层同步完成，待第 3 次定向复核（2026-10-17）"。但：
   - L3 末句仍为"作者第 2 轮修订（C39–C41 关闭条件＋六条非阻断观察）已完成，待第 2 次定向复核。"
   - L31 仍为"（2026-10-17 已交付；初审＋两轮修订完成，待第 2 次定向复核关闭 B22-C39–C41）"。

   第 2 次定向复核已经完成，报告 `batch-22-t05-04-claude-recheck-2.md` 也随本次提交入库，所以这两句的现时状态已不成立。
2. **L3 的时间线缺第 2 次定向复核的结果。** L3 按时间顺序叙述了初审、第 1 轮修订、第 1 次定向复核与第 2 轮修订，但没有记"第 2 次定向复核：C39–C41 CLOSED，新增 C42（P3）"和"C42 同步完成"。这些只出现在 L13。
3. **与既有做法不一致。** 上一轮提交 0318bcd 同时更新了审计 L1、L3、L13、L31 四处（`git show 0318bcd -- docs/research/batch-22-source-audit.md`），本轮提交 4b4c077 只改了 L1、L13。说明这是同步遗漏，不是有意保留历史措辞。
4. 本问题不影响正文的技术结论，也不影响来源记录与登记。但审计文件是本批任务状态的汇总依据，L33 还要求"T05-04 审阅闭环前不得宣布本批完成"，状态句必须前后一致。问题性质与 C41、C42 相同，都是记录层同步问题。

关闭条件：

- L3 末句改为与 L1、L13 一致的现时状态：补记第 2 次定向复核结果（`batch-22-t05-04-claude-recheck-2.md`：C39–C41 全部 CLOSED，新增 C42，P3，记录层）与 C42 同步完成，以"待第 3 次定向复核"或本轮之后的实际状态结尾。
- L31 括注同步为当前状态，例如"初审＋三轮修订完成，待第 3 次定向复核关闭 B22-C43"，或按下一轮结论改写。
- 修订时 L1、L13 一并更新为下一轮的实际状态，四处保持一致。只涉及审计文字，不需要新来源。

## 非阻断观察（不计入发现）

1. **登记 L5242 的 health.go 行锚（C42 可选项，未同步）。** "全设备标记 L124–131/L145–153"与本轮取回的 L125–131、L144–152 各偏一行：L124 是超时分支的右括号，L145–153 漏了 L144 的 `GetUUID` 调用，且含 L153 空行。"启动期标记 L80–112"作为区域超集锚仍然成立，但它包含 L106–107 只警告的分支。来源记录 L43 已改正，建议以后改动登记时顺带同步，使两处一致。
2. **K1 未注明 `VisitMigDevices` 语义同样未取。** 正文 L94 现在点名 i、j 来自 `VisitMigDevices` 回调，K1（L94 句末、L191）与来源记录 L58 只写 go-nvlib `VisitDevices`。正文没有对 j 作任何映射断言，所以不构成预设，可选补注。
3. **登记 L5413"L484 互引"措辞。** 原文 L484 是 `CUDA_VISIBLE_DEVICES` 条目指向 `SLURM_JOB_GPUS` 的**单向** "See also"，L622–625 的 `SLURM_JOB_GPUS` 条目没有反向引用。写"互见"或"单向 See also"更准确。不影响页面清单的一致性。
4. **登记中残留的"枚举序"字样。** NVIDIA 条目 L5242"device_map.go（枚举序传参 L110–134 经 L113/L127…）"与 L5247 notes"go-nvlib 枚举序……未取（unknown）"仍用"枚举序"。两处都没有冠 NVML，也没有把回调序号等同于 NVML index，不属于 C39 去除的预设，也不在 C42 关闭条件所列位置内。为与正文"回调序号"统一，可选改写。
5. **审计 L13 的核验表述。** L13 写"三轮审阅模型元数据均经调用方核验：CLI 输出 `modelUsage` 仅 `claude-opus-5-5` 单一模型、无 fallback 标记"。前几轮报告均写明该项须由调用方核验；审阅者在会话内无法确认调用方的核验，这里只记录审计中有此表述。

## 波及检查

- **C39**：正文 L94 的 `VisitDevices` 序号出处、十进制串、WSL `"all"`、K1 声明均未改，只在 MIG 括注内补了出处；L168 比较键未改；"NVML 枚举序"预设在正文、来源记录中均 0 命中。
- **C40**：正文 L169 的 scontrol 括注与 `SLURM_JOB_GPUS` 两页并列未改；来源记录 L48 与登记 L5413 现在与之对应。
- **C41**：来源记录 L5 表头、哈希表 L20/L26/L27 轮次注记、L54 勘误说明、`verification.notes` 均未改；登记 L5413 新增的"哈希与初审一致"与来源记录 L5、L27 同口径。
- **C31–C38**：正文只改 L94 一行，重启表、重建链、健康粒度、账本/运行时 ID 两列、相对编号、刷新四路径、页内锚点、`related_ids`、登记 URL 与 license 注记都没有被触及。
- 没有发现新引入的错误断言、虚构命令或越界推论。
- `make check` 与 `make build` 均通过（见检查记录）。

## acceptance 对照

| acceptance | 判定 | 相关发现 |
|---|---|---|
| 1 逐实现列稳定设备标识、capacity/allocatable 或 GRES/TRES、分配记录、容器/step 映射和框架视图，不设计统一错误码 | **满足**。MIG `i:j` 序号出处补全（device_map.go L139/L146）；账本侧 ID 与运行时 ID 两列口径未变；不设计统一错误码 | — |
| 2 健康变化、新旧任务/分配影响、插件/daemon 重启和账本刷新条件，依据选定源码/文档逐项核对 | **满足**。正文未变；来源记录主张表已补 RegisterEvents 其他错误（L108–110）与 validateFlags（L209–212），行锚经本轮取回属实，正文与记录的"逐项核对"依据一致 | — |
| 3 对比缺设备、重复/过期分配、账实不符的证据与处理前置条件，引用对应容器/生命周期指南 | **满足**。正文未变；"缺设备"候选断点的 CDI 无 NVML 分支已同步入主张表 L38 | — |
| 4 维护已有 Ascend 指南/来源案例/方案和未知条件；为 GPU/Slurm 提供同等身份核对/回收验证入口 | **满足**。来源记录 unknown 清单第 2 项已与正文 L191 同口径；Slurm 身份链所依赖的 prolog_epilog 已入登记与主张表 | — |

四项 acceptance 在正文与来源记录、登记层面均满足。C43 位于批次审计的状态记录，不属于任何一项 acceptance 的内容要求，但按"无 OPEN 方可通过"的约定，它仍阻止本轮判通过。

## 结论

**第 3 次定向复核不通过。B22-C42 CLOSED（1/1）；新增 B22-C43（P3）一项，OPEN。累计 B22-C31–C43 共 13 项：CLOSED 12，OPEN 1；没有开放的 P1/P2。**

- 正文、来源记录与登记没有待改项，acceptance 四项均满足。
- C43 只要求审计文件 L3、L31 两句与 L1、L13 同步，不需要新来源。修订后只对 C43 定向复核；如果修订只涉及审计文件的状态句，不需要重开 C31–C42。
- 正文没有虚构命令输出或实测结果，平台边界保持得当。`verification.status: source_checked` 仍只覆盖来源层核对，不代表 reproduced。

## 检查记录

- `make check`：`PASS: 96 content entries; 446 sources.`，`Checked structure and local file links; not technical correctness or remote links.`
- `make build`：`PASS: 96 content entries; 446 sources.`，`Built build/catalog.json and build/catalog.md.`（运行后 `git status --short` 无输出）。两者只说明结构与本地链接通过，不说明技术正确性，也不检查远程锚点。
- `git grep -n '枚举序' 4b4c077`，范围为正文、来源记录、登记、审计：正文 0、来源记录 0；登记 2 处（L5242、L5247，见非阻断观察 4）；审计 1 处（L13，为引述 C42 问题描述）。
- 成稿前复取输入哈希：正文 `f2b93384…1449`、来源记录 `3e1b4726…bfc7d`、登记 `0a40323a…d4700`（两段 `37fd4b94…5225`、`dde59670…f43a`）、审计 `4e19c31c…0db4`、初审 `626edfdd…a934`、第 1 次定向复核 `88136e29…cb8cb`、第 2 次定向复核 `1b39e5f1…8fac`、计划 `1dd6b549…de71`，与"输入"表一致。
- 本报告是本轮唯一新增文件；未执行 git 提交。

## 模型与运行元数据核验

- 指定模型：`claude-opus-5-5`（authoring-guide §7，2026-10-13 与 2026-10-16 更新：claude 模型经 `claude -p` 执行）。
- 会话内可见：审阅者会话的系统提示自述模型为 Opus 5.5、模型 ID `claude-opus-5-5`。这是**会话自述**，不是 CLI 输出元数据。
- 输出元数据中的实际模型是否只有 `claude-opus-5-5`：**在审阅者会话内不可核验**。CLI 输出元数据（例如非交互输出中的 `modelUsage`）对审阅者不可见，须由调用方依据实际输出元数据核验，并补记于审计；核验完成前，本轮不宜计入有效轮次。
- 结果文本是否含 `[frontier_llm]` 等 fallback 标记：本报告由审阅者撰写，除本节为说明核验项写出的标记名外，不含任何 fallback 标记。调用方仍须检查 CLI 原始输出。
- 执行方式是否为 `claude -p`：会话内不可核验。推理等级等运行元数据同样不可核验，不补造。
- 认证/路由：本会话没有遇到模型认证或路由失败，也没有工具权限被拒。会话中出现的 MCP 服务连接提示（若干服务未连接或需授权）与本任务无关，本轮没有使用这些服务，也不是模型 fallback 的迹象。

## 局限声明

- 模型审阅不构成平台、硬件或现场验证。审阅者没有在任何集群、容器、GPU 或 NPU 上执行命令，没有部署插件或 Slurm，也没有运行上游测试。MIG 序号、重启后以 Healthy 重建等后果都是只读代码路径推论。
- 本轮一次源取证限于上表所列四个文件与页面，其余来源沿用前几轮的核对结果。原文没有落盘，可复查性依赖所记哈希；tag 对象到 commit 的解析本轮没有重做。
- 作者侧是否独立核实 device_map.go L139/L146，审阅者无法核验，只核对了记录口径与哈希。
- 第 2 次定向复核报告由调用方入库，本会话无原稿可比，只记录其入库哈希。
- 本报告的发现与关闭条件不赋予任何执行权限；修订与复核按既有授权进行。
