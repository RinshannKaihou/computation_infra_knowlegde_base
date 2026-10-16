# 第二十二批 T05-03 第四次定向复核（作者第四轮修订后，仅 C21）

复核日期：2026-10-14（实际取证日）。

**结论：通过。范围内 1 项（B22-C21）CLOSED。B22-C12–C21 全部 10 项累计 CLOSED 10，OPEN 0。** 未新增发现 ID。顺带确认了两处：
- `MinJobAge` 精度提示已处理。
- 来源记录"首轮页数"的表述已处理，但正文 L23 与登记 L5396 未同步。属非阻断，见下文。

审阅者角色独立于作者修订角色。审阅模型为 `claude-opus-5-5`，由用户本次明确要求试用。这不是既有的 `gpt-6.1-sol / xhigh` 批量审阅约定，也不改写该约定。本会话内未见 `[frontier_llm]` 标记、认证失败或模型自报变化。推理等级、`modelUsage` 等运行元数据审阅者无法在会话内读取，不补造。若操作方在运行记录中发现模型不一致或认证问题，按约定本轮作废，不留档、不引用。

本轮只写本报告一个文件。未改作者正文、来源记录、修订映射、登记、索引或计划；未部署 Slurm、未提交作业、未执行任何 Slurm 命令或测试用例。模型复核不构成平台或现场验证。

## 输入（以 SHA-256 识别）

| 输入 | SHA-256 | 与任务给定前缀 |
|---|---|---|
| [T05-03 正文](../../knowledge/05-cluster-platform/slurm-jobs-and-device-resources.md)（181 行） | `0e82205bcf30b082c234f3adcdbc8b9baa3e6efbea285323b020c7a8bc7e66c5`；L135 单行 `925194266073e5e48ae269716b3bce3a308b51e4cb404052209ff787fdfbf682` | 一致 |
| [作者来源记录](batch-22-t05-03-sources.md)（25 行） | `25aecdc446720c2ea26840647e46054b608604fcbba5eb90138793e614044a75` | 一致 |
| [修订映射](batch-21-review-fixes.md)（226 行；T05-03 第四轮修订节 L224–226） | 整文件 `61a394f468b5c043d1d7aec5b378475d44689a2106cf977961976fb77cc3b3e9`；L224–226 段 `fcca8a387de5974761a79a5e0957e6002c3da134edc9a49d73c1f6c5480c8a21` | 一致 |
| [来源登记](../../sources/registry.yaml)（`make check` 计 438 项；T05-03 段 L5386–5418） | `61388eb10023ff425ab83891604529b05764afbe19b478257feb62a19c1262f7`；L5386–5418 段 `c4daef07234fb152d58fceb6a98c9e028844883785d2b4ab8472b128dd0d3e62` | 一致；段哈希与第三次复核所记相同，登记本轮未变 |
| [前次复核报告](batch-22-t05-03-claude-recheck-3.md)（C21 剩余关闭条件唯一权威来源） | `0a5f0e528e7f00fcd4ec9870c99fe8aa16c0af8c5d93f66888d99bcc16bc5642` | 任务未给前缀，记实值 |
| [初审报告](batch-22-t05-03-claude-review.md)（核对"首轮页数"用） | `a0830797ada7f12ae810689736c9d0ac150d1a1b045dcf50b415cbb72f21f9c6` | 任务未给前缀；与前三次复核所记相同 |
| [任务计划](../../plans/full-coverage-backlog.yaml) | `5f9bcf865b8c77e13cc8ee5f1c03140c37b86f558d8227d8bb2080249f4fcfc3` | 任务未给前缀；与前三次复核所记相同，计划未变 |

全部输入在取证开始时和成稿后各哈希一次，两次结果相同。取证期间未见并行会话改动。

## 取证方法与限制

- **原文重取**：用 `curl -sSL`（默认 TLS 校验）只读重取与本轮判定直接相关的两页，放在新建临时目录 `/tmp/b22rec04e/`（取证前不存在），未入库。
  - tres：HTTP 200，`2d08f826`。
  - slurm.conf：HTTP 200，`f4151769`。
  - 两页 SHA-256 前 8 位与初审及前三次复核相同。HTML 去标签后按文字核对。
- **渲染核对**：正文 L25 起的部分分别用 pandoc 2.12（`-f gfm`）和 markdown-it-py 4.0.0（commonmark＋table）渲染。
  - 两者都得到标题 15 个（h1 ×1、h2 ×5、h3 ×9）、表格 7 张、`tr` 69 个，69 行均为 4 列，与第三次复核所记相同。
  - TRES 行四列文字在两种渲染器下逐字相同。两者唯一的单元格差异在 L134：pandoc 在 `↔` 后多插入 U+FE0E 变体选择符。这与本项无关。
- **`make check`**：结果为 `PASS: 96 content entries; 438 sources.`，运行前后 `git status --porcelain` 相同。它只校验结构与本地链接，不校验单元格语义。`make build` 未运行，因为它会写 `build/`，超出"只写一份报告"的范围。
- **限制**：
  - 其余 18 页归档与 testsuite 本轮未重取，依据第三次复核所记哈希。
  - 正文与来源记录均未入 git（工作区 `??`），前一版无法取回。"错句已删"的判断以第三次复核 L151 引述的整格文字为对照。
  - 作者是否用 webfetch 读过某页，审阅者无法核实，只能核对记录之间是否一致。

### 原文核对点

| 抽查点 | 原文（tres / slurm.conf 归档页） | 对应正文 |
|---|---|---|
| PriorityWeightTRES 节 | `A comma separated list of TRES Types and weights that sets the degree that each TRES Type contributes to the job's priority.` 示例 `PriorityWeightTRES=CPU=1000,Mem=2000,GRES/gpu=3000`；`Applicable only if PriorityType=priority/multifactor and if AccountingStorageTRES is configured with each TRES Type. The default values are 0. The Billing TRES is not available for priority calculations because the number isn't generated until after the job has been allocated resources` | L135 第三列"按 TRES 类型（CPU/Mem/GRES 等）加权，Billing 不在其列"；第二列引文 |
| TRESBillingWeights 节 | `If TRESBillingWeights is not defined then the job is billed against the total number of allocated CPUs.`；`TRESBillingWeights is only used when calculating fairshare and doesn't affect job priority directly`；`If you want TRESs to play a role in the job's priority then refer to the PriorityWeightTRES option.` | L135 第二列"缺省=CPU 数，用于 fairshare"；第三列开头"要让 TRES 影响 priority，用 PriorityWeightTRES" |
| AccountingStorageTRES 节 | `When including a specific GRES with a subtype, it is also recommended to include its generic type, otherwise a request with only the generic one won't be accounted for.`；`Setting gres/gpu will also set gres/gpumem and gres/gpuutil.`；`By default Billing, CPU, Energy, Memory, Node, FS/Disk, Pages and VMem are tracked. These default TRES cannot be disabled, but only appended to.` | L135 第三列记账前提、子类型、gpumem/gpuutil；第二列默认跟踪 |
| slurm.conf `MinJobAge` | `The minimum age of a completed job before its record is cleared from the list of jobs slurmctld keeps in memory … The default value is 300 seconds. A value of zero prevents any job record purging. Jobs are not purged during a backfill cycle, so it can take longer than MinJobAge seconds to purge a job if using the backfill scheduling plugin.` | L163 |

## 逐项判定

### B22-C21 — CLOSED（P3）

前次剩余关闭条件（第三次复核 L156）共两条，逐条核对如下。

1. **错句已删。**
   - 前次的错句是"Billing 经 PriorityWeightTRES 才参与 priority；"。两种渲染器下，L135 第三列整格文字现为："要让 TRES 影响 priority，用 PriorityWeightTRES 按 TRES 类型（CPU/Mem/GRES 等）加权，Billing 不在其列；GRES 须写入 AccountingStorageTRES 才被记账（带子类型建议同时写通用类型，否则只求 gpu:1 的作业不计入）；gres/gpu 同时置 gres/gpumem 与 gres/gpuutil；权重站点配置"。
   - 与第三次复核 L151 的引述对照，前段与后段都未变，只少了"Billing 经 PriorityWeightTRES 才参与 priority；"一句。
   - 在两种渲染结果的全文中检索"经 PriorityWeightTRES"和"参与 priority"，均为 0 处。
2. **全文检索"Billing"，没有其他位置写 Billing 参与 priority。**
   - 正文：只有 L135 一处。第二列有三处，分别是类型列举、默认跟踪列表、"Billing 由分区 TRESBillingWeights 算"（附原文引文 `The Billing TRES is not available for priority calculations`）；第三列一处，即"Billing 不在其列"。
   - 来源记录：只有 L15 一处，"tres.html（类型与 Billing 权重）"，属中性描述。
   - 登记：只有 L5407 一处，"tres（类型与 Billing 权重站点配置）"，属中性描述。
   - 三个文件中都没有"Billing 参与 priority"一类说法。

行内一致性（本轮要求确认）：

- 第二列"Billing 由 TRESBillingWeights 算，用于 fairshare，不可用于 priority 计算"，第三列"PriorityWeightTRES 按类型加权，Billing 不在其列"，两列方向一致，与 tres 页两节原文一致。
- 第三列其余三个分句都与原文相符（见核对表）：记账前提与子类型、`gres/gpu` 连带 gpumem/gpuutil、权重站点配置（原文 `The default values are 0`）。
- 同页 L121"multifactor 九因子……TRES 加权"未提 Billing，与 L135 不冲突。
- 渲染后整行无自相矛盾。

修订映射 L226"删 L135 第三列错误原句"与实际落盘一致。

可选，不影响判定：第三次复核已提过，第三列可补 PriorityWeightTRES 的适用前提（`Applicable only if PriorityType=priority/multifactor …`；`The default values are 0`）。本轮仍未补。

## 一并确认（非阻断项，不改变判定）

### `MinJobAge` 表述（第三次复核 C17 精度提示）— 已处理

- L163 现为："且只在 slurmctld 内存保留期内（`MinJobAge`，最短保留时间，文档默认 300 s，0 表示不清除，站点实际 unknown）可见，超出后用 sacct"。
- 与原文逐点对照：
  - "最短保留时间"对应 `minimum age … before its record is cleared`。
  - "文档默认 300 s"对应 `The default value is 300 seconds`。
  - "0 表示不清除"对应 `A value of zero prevents any job record purging`。
- 可见期改为以内存保留期界定，MinJobAge 明确是下限，原来"只在 MinJobAge 窗口内"那种读成上限的问题已消除。
- backfill 周期内可能保留更久（`it can take longer than MinJobAge seconds`）一句未写。"最短"已隐含这层意思，可不补。
- 修订映射 L226"MinJobAge 改最短保留时间"与落盘一致。

### 来源记录首轮页数（第三次复核 C14 追记）— 记录本身已处理；跨文件归属未同步

- 来源记录 L3 现为："首轮（Slurm 24.11.7 归档文档十九页）＋testsuite 用例编号存在性；sacct 页与用例头注释目的为审阅者补取（作者侧未独立打开），后补入二十页口径"。
- 这与初审记录一致：初审 L121"正文与来源记录列出的 19 页不含 sacct"，L58"sacct（未登记，审阅者补取）"。"首轮"已不再包含 sacct。修订映射 L226"记录首轮十九页＋sacct 审阅者补取诚实表述"与落盘一致。
- **未同步处（非阻断）**：作者现已声明 sacct 页"作者侧未独立打开"。按第三次复核追记中"若未读过……同步这三处"，另外两处仍把 sacct 写作作者 webfetch 核对的结果，与作者自己的来源记录 L3 不一致：
  - 正文 L23 `verification.notes`："经 webfetch 只读核对 24.11.7 归档二十页"。按 L3，作者侧 webfetch 只覆盖十九页；括号内的主题列举也仍不含 sacct。
  - 登记 L5396：在"取证轮经 webfetch 只读核对："之下列出"/sacct（-D=--duplicates）"。登记本轮未改（段哈希与前次相同）。
  - 另外，正文 L180 的 sacct 条目没有像 L179 testsuite 条目那样注明"审阅者取证"。
  - 修法：L23 改为"经 webfetch 只读核对十九页……；sacct 页为审阅者补取"；L5396 把 sacct 移出"取证轮经 webfetch 只读核对"的列举，另标审阅者取证；L180 补同样的归属说明。
  - 这三处都是取证归属的表述问题。sacct `-D, --duplicates` 的内容本身已由初审及前三次复核按原文核对（页面哈希 `d96f8299` 未变），不影响 C14 的 CLOSED 判定。
- L3 文字问题（非阻断）："用例头注释目的"在同一句中出现两次。"由只读取证角色完成"仍紧跟审阅者取证括注，读来像在说审阅者取证由该角色完成，前次已提。

### 前次其余非阻断建议

以下各项本轮未见处理，仍为非阻断，均不影响判定：

- L72/L73 PartitionNodeLimit 仍重复列出。
- L143 开头的自指括注仍在。
- 登记 L5413 用例清单仍无 test12.7。
- L91、L113、来源记录 L23 仍称"节点动作表"，所指实为 L87 段落。
- L165 仍未补 sacct `-D` 首句的 job ID 重置限定。
- 登记 L5407 仍写"四类字符串"。

## acceptance 对照

| acceptance | 判定 | 未关闭项 |
|---|---|---|
| 1 固定 release/commit 与官方文档；守护进程、Job/Step、状态与资源清理 | 满足（前次已满足，本轮未回退） | — |
| 2 GRES/TRES、autodetect/binding、cgroup、健康职责；一种 NVIDIA GPU 条件；NPU 无证据即 unknown | 满足。TRES 行第三列错句已删，整行与 tres 页原文一致；NPU/Ascend unknown 保留 | — |
| 3 状态、等待原因、配额/优先级/预留、节点状态与成组资源条件；不套用 K8s 术语 | 满足（PartitionNodeLimit 重复为非阻断） | — |
| 4 观察样板与最小验证设计；不提交作业 | 满足；L163 `MinJobAge` 口径已改为最短保留时间 | — |

## 结论

**T05-03 第四次定向复核通过。B22-C21 CLOSED，位置证据见上：L135 第三列错句已删，两种渲染下整格无矛盾，三个文件全文检索"Billing"无参与 priority 的说法。B22-C12–C21 全部 10 项累计 CLOSED 10，OPEN 0，T05-03 本批审阅可视为通过。** 未新增发现 ID。

- C21 关闭后，正文 `verification.status: source_checked` 对 L135 TRES 行成立。这只是文档与源码层面的核对，不得标为 reproduced；`status: draft` 是否推进由作者与集成者决定。
- 建议后续一并处理的非阻断项：
  - 正文 L23、登记 L5396、正文 L180 的 sacct 取证归属与来源记录 L3 同步。这是本轮唯一新确认的不一致，附于 C14 追记，不另立 ID。
  - 前次其余非阻断建议（见上）。
- 正文没有虚构命令输出或实测结果。NPU/Ascend 保留 unknown，范围声明与 `verification.notes` 写明未提交作业、未执行 Slurm 命令。
- 本复核只覆盖编辑与来源层面，不构成硬件或平台验证。
