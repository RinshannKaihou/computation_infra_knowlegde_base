主执行者集成说明（2026-10-09，Asia/Shanghai）：以下保存原审阅者第一轮报告。实际运行发生于 UTC 2026-10-08（对应本地 2026-10-09），报告中的日期基准原文保留。原会话 ID 为 `01a11c1a-4fb4-7f73-a0a3-d97e5f379dff`；实际 turn_context 为 `gpt-6.1-sol / xhigh / read-only`，本轮进程正常结束、退出码 0，11 份输入指纹与交付时一致。此前恢复入口未继承只读设置的运行已主动中断，仅执行读取、未形成结论；本报告来自显式只读设置后的完整运行。当前累计状态见[复核汇总](batch-13-codex-rerecheck.md)。

# Batch 13：B13-R01–R05 定向复核报告

## 1. 日期、配置与独立性声明

- **审阅日期：2026-10-08，按本会话适用日期基准记录。** 用户提供的环境信息、修订清单及部分更新元数据标注为 **2026-10-09**；本报告保留该输入日期，不将其混作本轮实际取证日期。
- **会话配置：`gpt-6.1-sol / xhigh`。** 按用户明确指定的配置记录；现有工具不能独立认证底层模型身份，不据此臆测或改写模型名称。
- **角色：原独立审阅者，独立、只读定向复核。** 未参与本轮正文修订，未以编写者自查、结构检查或历史通过状态代替技术关闭证据。
- 本轮使用显式只读沙箱；未编辑仓库文件、提交、创建分支或生成子代理，未读取凭据，未执行设备查询、硬件／集群／供电／绑定／负载实验。
- 前次中断运行没有最终复核结论。本报告完成五项实际判定，不追认前次运行已经通过。
- 历史 **B13-C01–C18** 的原文、编号及状态保留；初始补充审阅中 **B13-R01–R05 的 OPEN 和旧行号**仍是历史记录，本报告不要求重写它们。

## 2. 结论摘要

**当前修订范围：暂不通过。**

| 条目 | 原优先级 | 本轮状态 | 判定 |
|---|---|---|---|
| B13-R01 | P2 | **CLOSED** | npu-smi 负面结论已限定；DCMI 当前原因接口、支持场景及历史边界与官方表格一致 |
| B13-R02 | P2 | **CLOSED** | 允许集、已安装策略、线程／子进程范围、CPU 样本与驻留证据已分开，流程和判据一致 |
| B13-R03 | P2 | **OPEN** | 原 violation-only／WARN 误释已修复；新增的 thermal“窗口首末”表述仍未精确对应固定实现，见 B13-R06 |
| B13-R04 | P3 | **CLOSED** | 数组字段、废弃版本、兼容及设备实现边界与精确 schema 一致 |
| B13-R05 | P3 | **CLOSED** | 技术引用已替换为实际支持机制的 PyTorch 2.6 页面，AIInfra 占位章节不再承担该技术主张 |

- 原五项：**4 项 CLOSED、1 项 OPEN、0 项 BLOCKED**。
- 本轮新增可行动问题：**1 项，B13-R06，P3／OPEN**。
- R03 尚未关闭与 R06 指向**同一个剩余缺口**，不是两个独立技术问题，不重复计算。
- 未取得的健康定义 XLSX、已明确限定的现场 unknown，不是此次暂不通过的原因。
- 四篇修改正文仍为 **`draft` / `source_checked`**，没有升级为硬件复现或现场验证状态。

## 3. 输入范围及 SHA-256

### 3.1 实际核对范围

先读取修订清单，再读取原补充审阅报告中 R01–R05 的发现与关闭条件，随后核对当前修订文本及上游：

| 输入 | 本轮核对内容 |
|---|---|
| `docs/research/batch-13-rereview-revisions.md:1` | 完整修订清单、关闭前提及 11 个输入指纹 |
| `docs/research/batch-13-codex-rereview.md:57` | R01–R05 各节及关闭条件，至第 265 行 |
| `knowledge/00-overview/terms-and-system-boundaries.md:1` | 元数据；第 151 行 checkpoint 区分及来源组织边界 |
| `knowledge/01-hardware/rack-power-cooling-and-failure-domains.md:1` | 元数据；第 81、87、89 行 Redfish 字段与实现边界 |
| `knowledge/01-hardware/power-thermal-evidence.md:1` | 元数据；第 89、91、124、126、128 行及相关关联表、误解总结、来源与未知条件 |
| `knowledge/01-hardware/numa-memory-and-io-locality.md:1` | 元数据；线程策略说明、证据表、步骤、分支、停止及完成条件 |
| 五份对应研究记录 | R01–R05 的主张—证据行、支持范围、修订说明和限制 |
| `sources/registry.yaml:1` | 解析登记表并核对九项相关登记：AIInfra、DCGM、DMTF、A2 npu-smi、NUMA policy、numactl、A2 DCMI、proc/cpuset、PyTorch checkpoint |
| `knowledge/01-hardware/accelerator-execution-and-data-movement.md:1` | **仅核对指纹保持不变**，未重新启动全文技术审阅 |
| `Makefile:1` | 确认 `check` 与写入 `build` 的构建目标分开 |

原审阅已读取的 `AGENTS.md`、README、编写指南、内容大纲及 schema 上下文继续适用；本轮没有据此扩大为全批重新审阅。读取正文差异仅用于确认 R03 修订引入的表述变化，不以仓库历史通过状态证明关闭。

### 3.2 指纹结果

独立重新计算修订清单中的全部 SHA-256；结束前再次核对，**11/11 MATCH，无不一致**。

| 文件 | 实际 SHA-256 |
|---|---|
| `knowledge/00-overview/terms-and-system-boundaries.md` | `055bd82e176f9534cc719fe448dcfed73c712dbbddfd588a959ebfed89a43b91` |
| `knowledge/01-hardware/rack-power-cooling-and-failure-domains.md` | `11ea7e42e1454635659b6a44490055b563817d43c7aaaa8ec6af7e3059cfd7b0` |
| `knowledge/01-hardware/power-thermal-evidence.md` | `6bbea31bb15ee3373437d5943700f01776b8dddfd7c603d0b622b7e26eda5346` |
| `knowledge/01-hardware/numa-memory-and-io-locality.md` | `b815f35bf4b20eb5065f90eb68c9508fa60b24566b8223852c07c79771ab5f40` |
| `knowledge/01-hardware/accelerator-execution-and-data-movement.md` | `242bdbaf8d0d3d9eaa929b45ea7ef0f309a5ac08a61420307f1584902a80bf14` |
| `docs/research/batch-13-training-npu-power-sources.md` | `4f777a78cefd0d55ab024b99eba6d8b91bc24b5a736e0db6b97501ec2f7e7357` |
| `docs/research/batch-13-numa-locality-sources.md` | `36a5feecd367b92d00e2f537566efb296c55ef72ffc26749020c05b83985cf4b` |
| `docs/research/batch-13-terms-sources.md` | `6712529b7af7aaedb5c234667e4b283a7faaa9ab5fba38728bed601646a9f07b` |
| `docs/research/batch-13-rack-power-sources.md` | `36d6664cc39131162fc9e7f80905c2c10da2c36c394c6b740ddaea3dae58137b` |
| `docs/research/batch-10-power-thermal-sources.md` | `9e97af42e98285cf02663e85bda2ef0b2ec2c1a01f14337058079a5d05d68eca` |
| `sources/registry.yaml` | `8056554995bfa8b4a95f5c2e42d71b0e22a1f2c83cdbb4b7ae47de1b4c1430f4` |

accelerator 正文指纹也与上一轮一致。以上只固定本次输入，**不证明工作区干净或内容技术正确**。

## 4. R01–R05 逐项判定

### B13-R01 — CLOSED

**修订位置**

- `knowledge/01-hardware/power-thermal-evidence.md:124`：npu-smi 限定扫描结论。
- 同文第 126、128、145、157 行：DCMI 格式、原因、支持矩阵及当前／历史边界。
- `docs/research/batch-13-training-npu-power-sources.md:30`：限定扫描；第 31、37 行：DCMI 与关联路径。
- `sources/registry.yaml:1191`、`sources/registry.yaml:1515`：npu-smi／DCMI 登记同步。

**独立证据**

本轮重新取得 [HDK 26.1.x A2 `dcmi_077`，约束及表 1–3](https://www.hiascend.com/doc_center/source/zh/HDK/2610/A2/A2DCMI/dcmi_077.html)，核对：

- `DCMI_MAIN_CMD_LP` / `DCMI_LP_SUB_CMD_AICORE_FREQREDUC_CAUSE`；
- 8Byte、64 位原因值，每 100ms 更新，不能查询历史原因；
- 位号为 IDLE 0、THERMAL 2、SW_EDP 3、HW_EDP 4、POWER_BREAK 5、SVFD 8、POWERCAPPING 10；
- Atlas 800T A2／900 A2 PoD 的四个所列部署场景均为 Y。

**关闭依据**

正文不再由 npu-smi 页面的未发现推出“平台无接口”；明确 IDLE 为空闲节能而非故障，当前原因不能证明历史，文档支持不保证现场可用。npu-smi、DCMI、健康事件／日志与 exporter 未被混作同一证据路径。

本轮**没有独立重做 npusmi_0002–0181 全量扫描**；当前正文明确归属为编写者扫描，且不再用其承担平台级负面保证。R01 关闭条件满足，B13-C07 等历史记录不变。

### B13-R02 — CLOSED

**修订位置**

- `knowledge/01-hardware/numa-memory-and-io-locality.md:74`：目标范围与允许集。
- 同文第 75–77、90–94、98、108、114–116 行：策略、采样、驻留与流程判据。
- `docs/research/batch-13-numa-locality-sources.md:15`、第 16、17、26 行。
- `sources/registry.yaml:1235`、`sources/registry.yaml:1288`、`sources/registry.yaml:1526`。

**独立证据**

重新取得 Linux 固定 commit `038d61fd642278bab63ee8ef722c50d10ab01e8f`：

- [NUMA policy L15–69](https://github.com/torvalds/linux/blob/038d61fd642278bab63ee8ef722c50d10ab01e8f/Documentation/admin-guide/mm/numa_memory_policy.rst#L15-L69)：cpuset 与策略不同；task policy 的线程作用域。
- [策略 API L429–481](https://github.com/torvalds/linux/blob/038d61fd642278bab63ee8ef722c50d10ab01e8f/Documentation/admin-guide/mm/numa_memory_policy.rst#L429-L481)：`get_mempolicy` 查询调用任务，或依 flags 查询指定地址的策略／位置。
- [CPU 允许集实现 L406–412](https://github.com/torvalds/linux/blob/038d61fd642278bab63ee8ef722c50d10ab01e8f/fs/proc/array.c#L406-L412)及 [内存允许集实现 L4395–4402](https://github.com/torvalds/linux/blob/038d61fd642278bab63ee8ef722c50d10ab01e8f/kernel/cgroup/cpuset.c#L4395-L4402)。
- [numa_maps L683–715](https://github.com/torvalds/linux/blob/038d61fd642278bab63ee8ef722c50d10ab01e8f/Documentation/filesystems/proc.rst#L683-L715)：映射策略标签与节点页计数是不同字段。

另取得官方 numactl 仓库，并固定到此次返回的 commit `09fc1874fdeb3836d7ea08c57299e9763a49028c`：

- [`numactl.8` L199–207](https://github.com/numactl/numactl/blob/09fc1874fdeb3836d7ea08c57299e9763a49028c/numactl.8#L199-L207)：`--show` 是当前调用进程。
- [`numastat.8` L52–92](https://github.com/numactl/numactl/blob/09fc1874fdeb3836d7ea08c57299e9763a49028c/numastat.8#L52-L92)：选项输出以 MB 表示，`-p` 指定目标 PID，内存使用反映驻留页。

此次官方仓库 revision **不冒称登记中的 man7 2026-08-04 镜像快照**。

**关闭依据**

允许集没有被用作 MPOL_BIND／interleave 或 VMA 策略证明；目标内查询明确任务／地址范围。主线程、关键 TID 和 loader 子进程分别取证。最近 CPU 样本未被当作连续轨迹；策略标签、页数和 MB 分开。

证据不足时，步骤、分支和停止条件均禁止宣称完整绑定成立；完成条件要求目标覆盖、策略、驻留和应用指标。R02 关闭条件满足，无需执行绑定或负载。

### B13-R03 — OPEN

**修订位置**

- `knowledge/01-hardware/power-thermal-evidence.md:89`、第 91、153 行。
- `docs/research/batch-10-power-thermal-sources.md:22`。
- `sources/registry.yaml:584`。

**已经独立确认的修复**

重新读取 [DCGM 固定源码 L1550–1798](https://github.com/NVIDIA/DCGM/blob/b0ec3c624ea21e688b0d93cf9b214ae0eeb6fe52/modules/health/DcgmHealthWatch.cpp#L1550-L1798)，并核对实体分派路径：

- GPU power 的不可读 WARN 确实要求 `ret == DCGM_ST_OK`、值为 blank、且不等于 `DCGM_FP64_NOT_SUPPORTED`，错误为 `DCGM_FR_POWER_UNREADABLE`。
- 该 WARN 不是任意查询失败，也不能一律解释为功率节流。
- GPU thermal violation 分支的结论没有再扩张为整个健康模块；同文件 CPU thermal 使用温度阈值路径。
- “被动”与“所有规则 violation-only”已分开。

**尚未满足的关闭条件**

第 89 行及来源记录新增的“窗口首末”表述仍未精确对应 `MonitorThermal` 的末样本读取方式。详见 **B13-R06**。因此，原错误概括虽已消除，本轮仍不把“与固定实现一致”的关闭条件判为全部满足。

### B13-R04 — CLOSED

**修订位置**

- `knowledge/01-hardware/rack-power-cooling-and-failure-domains.md:81`、第 87、89 行。
- `docs/research/batch-13-rack-power-sources.md:31`。
- `sources/registry.yaml:1133`。

**独立证据**

本轮取得精确 [PowerSupplyMetrics.v1_3_0.json](https://redfish.dmtf.org/schemas/v1/PowerSupplyMetrics.v1_3_0.json)，直接核对两个属性：

- `FanSpeedsPercent` 为数组，`versionAdded: v1_1_0`；
- `FanSpeedPercent` 的 `versionDeprecated: v1_1_0`，废弃说明明确为支持多个 PSU 风扇而改用数组；
- 单数字段仍存在于该 schema 中，并允许 null。

**关闭依据**

字段表采用数组；单数字段只作为旧实现兼容背景。正文明确 schema 不证明设备实现，缺失／null 不当作 0% 或无故障。正文、研究记录与登记同步，R04 关闭条件满足。

### B13-R05 — CLOSED

**修订位置**

- `knowledge/00-overview/terms-and-system-boundaries.md:151`，以及 source_refs／evidence_refs 元数据。
- `docs/research/batch-13-terms-sources.md:22`。
- `sources/registry.yaml:98`、`sources/registry.yaml:1540`。

**独立证据**

本轮重新取得 [PyTorch 2.6 `torch.utils.checkpoint.checkpoint`](https://docs.pytorch.org/docs/2.6/checkpoint.html#torch.utils.checkpoint.checkpoint)。实际机制段明确：前向少保存用于反向的张量，反向重算，以计算换取内存。

**关闭依据**

近旁引用指向实际机制正文，不再以 AIInfra 占位章节标题充当证据。“该机制本身不提供持久化训练状态”被限定为机制区别，研究记录明确其为术语归纳；没有扩张为“用户函数绝不会进行任何磁盘操作”。

AIInfra 仍可作为章节组织入口，元数据保留该来源不构成继续用它证明 checkpoint 技术机制。R05 关闭条件满足。

## 5. 本轮直接回归

### B13-R06 — P3／OPEN：GPU thermal 的“窗口首末”表述遗漏末样本不受指定 endTime 约束的边界

**位置**

- `knowledge/01-hardware/power-thermal-evidence.md:89`。
- `docs/research/batch-10-power-thermal-sources.md:22`。

**触发主张**

两处均将固定 v3.3.9 GPU thermal 分支描述为检查计数器“窗口首末”非零差值，未说明它与 GPU power 的末端取样不同。

**精确证据与原文语义**

[固定 `MonitorThermal` L1574–1607](https://github.com/NVIDIA/DCGM/blob/b0ec3c624ea21e688b0d93cf9b214ae0eeb6fe52/modules/health/DcgmHealthWatch.cpp#L1574-L1607)：

- 起始样本通过带 `startTime`、`endTime` 的升序 `GetSamples` 取得；
- 末样本通过 `GetLatestSample` 取得，该调用没有传入 `endTime`；
- 随后比较这两个计数器值的差值。

对照 [同文件 GPU power L1649–1687](https://github.com/NVIDIA/DCGM/blob/b0ec3c624ea21e688b0d93cf9b214ae0eeb6fe52/modules/health/DcgmHealthWatch.cpp#L1649-L1687)，其两端分别用同一范围内升序／降序 `GetSamples` 取得。

因此，thermal 不能无条件概括成**任意指定历史窗口内严格受两端约束的首末比较**。本发现不是宣称默认当前查询都会计算错误，也不是对上游代码作缺陷认定。

**影响**

读者对齐设施日志、设备事件及指定历史窗口时，可能把查询上界之后的最新 thermal 样本当作窗口内末样本，扩大该窗口所能支持的事件归属。

**建议**

将 thermal 说明改为实际两步取样语义：范围内起始样本与缓存最新样本比较；明确默认起点与最新样本边界，不保证指定 `endTime` 限定末样本。将 GPU power 的范围内双端取样另行描述，关联分析核对实际样本时间戳。

**关闭条件**

正文第 89 行及来源记录第 22 行同步修订；必要的登记说明不得继续暗示两条路径具有相同的严格窗口端点语义。再对固定源码上述两段作定向复核后，才可关闭 R06，并完成 R03 的关闭判定。**无需运行 DCGM 或任何负载。**

**关系**

这是 R03 修订引入的直接表述缺口；不撤销已确认的 GPU power 不可读 WARN、实体范围及 passive 含义修复。除 R06 外，本轮未发现其他可行动直接回归。

## 6. 来源取得范围与限制

| 正文 | 本轮独立重新取得 | 沿用前轮独立证据 | 未取得／仅编写者记录支持 |
|---|---|---|---|
| 供电散热 | A2 DCMI 约束、表 1–3；DCGM 固定 GPU thermal／power、CPU thermal 和实体分派路径 | 原审阅中的既有字段、采样间隔及部分 npu-smi／exporter 固定来源核查 | **健康定义 XLSX 未独立取得**；npusmi_0002–0181 全量负面扫描仍是编写者记录 |
| NUMA | Linux 五个固定文档／源码区段；官方 numactl／numastat man 源并固定此次 revision | 最近 CPU 采样及既有拓扑等未改内容的原审阅证据 | 没有现场 PID/TID、策略、驻留或设备归属实测 |
| 机柜 | 精确 PowerSupplyMetrics v1.3.0 的两风扇属性及版本标记 | 未改预算、冗余、冷却规格的原审阅证据 | 没有 BMC 实际实现或现场枚举证据；本轮未重取整机 PDF |
| 术语 | PyTorch 2.6 checkpoint 实际机制段 | 原审阅实际读取的 AIInfra 固定占位章节 | 没有框架运行或训练状态持久化实验 |

补充边界：

- 对 `hma2_01.xlsx` 中 **0x80E20207／0x80E21007**，本轮没有取得原始工作表，也不声称重新核验其事件定义。
- 原审阅中 CANN 架构／ACL、Atlas HCCS、Supermicro 等来源的既有取得状态或限制，不因本轮而升级；本轮没有重新启动这些未修改内容的取证。
- 本轮用于 R01–R05 判定的关键新增接口、固定源码、schema 和机制段均取得了可用原文。未把仅有 URL、搜索片段、编写者摘录或旧结论算作本轮重新取得。
- A3 事件、未公开门限、未列部署场景、现场版本／权限、exporter 对应关系和机房实测继续保留为限制；它们没有被用作保证，**不另泛化为阻塞发现**。

## 7. 结构检查与未执行项

本轮实际执行：

```text
PYTHONDONTWRITEBYTECODE=1 make check
退出码：0
PASS: 73 content entries; 122 sources.
```

工具同时报告只读环境不能创建 `/tmp/xcrun_db-*` 缓存的警告／错误信息；知识库检查命令仍实际运行并返回 PASS。该结果确认结构及本地链接，**不证明远程内容、技术正确性或硬件兼容性**。

未执行：

- `make build`；
- 设备／集群查询、供电散热操作、NUMA 绑定、负载或诊断实验；
- 子代理、另派模型、文件修订及提交。

## 8. 最终判定

**当前修订范围暂不通过：R01、R02、R04、R05 关闭；R03 因与新增 R06 相同的时间窗证据缺口保持 OPEN。**

主执行者须修订该缺口并完成定向复核后，才可关闭 R03／R06并宣告本次修订范围通过。本报告不提前宣称修复完成，不替代历史报告，也不将 `source_checked` 转换为硬件验证结论。