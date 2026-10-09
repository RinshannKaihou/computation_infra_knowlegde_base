# 第十四批定向复核记录（gpt-6.1-sol / xhigh）

复核日期：2026-10-09。复核者：Codex 会话（resume），模型 gpt-6.1-sol / xhigh。复核对象为[初审记录](batch-14-codex-review.md)的 12 项发现及[修订记录](batch-14-review-fixes.md)。复核输出全文照录如下。

---
# Batch 14 定向复核报告

## 一、复核信息

- **复核日期：2026-10-09，Asia/Shanghai。**
- **模型 / effort：用户指定 `gpt-6.1-sol / xhigh`。** 当前接口未提供可核验的实际运行模型及 effort 标识，不能将指定配置写作已独立确认的运行配置。
- **角色：独立审阅者。** 修订摘要用于定位修改，未作为关闭发现的唯一依据。
- **结果：原 12 项中，9 项 CLOSED、3 项 OPEN；新增 2 项发现。最终结论：暂不通过。**

本轮核对了三份修订正文、对应研究记录、`sources/registry.yaml` 相关条目及原始关闭条件；重新打开了 Xid 目录、DCGM Exit Codes、AMD SMI CLI/reset/AFID、DGX OS 7 Reimaging、LogEntry schema、GPU Node Triage 和 MLPerf Benchmarks 表。

结构检查执行结果：

```text
PYTHONDONTWRITEBYTECODE=1 make check
PASS: 75 content entries; 163 sources.
```

未修改仓库，未运行 `make build`，未执行设备查询、诊断、复位、重镜像或介质清除操作。

## 二、逐项判定表

以下位置均为**修订后当前行号**。CLOSED 仅表示对应发现的关闭条件已满足，不等于整篇文档或目标硬件已验证。

| 编号 | 初审优先级 | 判定 | 当前正文位置 | 复核依据与结果 |
|---|---|---|---|---|
| B14-C01 | P1 | **OPEN** | `knowledge/01-hardware/health-evidence.md:239`、`knowledge/01-hardware/health-evidence.md:243` | 主体码义、产品适用性及动作桶已修正；Xid 140 的数量因果解释、155 的“不是异常故障”判断仍超出原文。详见下一节。 |
| B14-C02 | P1 | **CLOSED** | `knowledge/01-hardware/health-evidence.md:257` | 226 恢复为诊断执行完成但报告错误，205 保留需要隔离，237 恢复为 GPU 需要复位；不再由 226 单独推出节点重启。研究记录同步。上游定位：DCGM Diagnostics → **Exit Codes** 对应三行。([docs.nvidia.com](https://docs.nvidia.com/datacenter/dcgm/latest/user-guide/dcgm-diagnostics.html)) |
| B14-C03 | P1 | **CLOSED** | `knowledge/01-hardware/health-evidence.md:347` | 已分别列出 XGMI hive、共享 PCIe switch/SBR、持有 `/dev/kfd` 句柄的进程三类影响范围，并同步处置入口及研究记录、来源登记。固定文档树的 CLI → **amd-smi reset → Warning** 可独立支持这些修订。([rocm.docs.amd.com](https://rocm.docs.amd.com/projects/amdsmi/en/docs-10.1.0/how-to/amdsmi-cli-tool.html)) |
| B14-C04 | P2 | **CLOSED** | `knowledge/01-hardware/health-evidence.md:338` | AFID 19–34 的编号、类别与严重性重新对齐；19 为页退休阈值事件，22 不再被错写成该阈值事件。研究记录与来源条目未继续保留原错误映射。上游定位：UG-70122 v1.0 → **AFID Event List → Table 1**。([docs.amd.com](https://docs.amd.com/r/en-US/AMD_Field_ID_70122_v1.0/AFID-Event-List)) |
| B14-C05 | P2 | **CLOSED** | `knowledge/01-hardware/health-evidence.md:325`、`knowledge/01-hardware/health-evidence.md:365` | `monitor -e` 改为计数采样而非事件流；连续采样明确需要 watch；`monitor -V/--violation` 与小写 `-v/--vram-usage`、MI300+ 门控均与 CLI 原文一致。([rocm.docs.amd.com](https://rocm.docs.amd.com/projects/amdsmi/en/docs-10.1.0/how-to/amdsmi-cli-tool.html)) |
| B14-C06 | P2 | **OPEN** | `knowledge/01-hardware/health-evidence.md:362`、`knowledge/01-hardware/health-evidence.md:387` | Empty Section 的双重原因已补充，但 Not Available 仍被归入“采样失败或版本错配”，并作为“诊断失败”示例。详见下一节。 |
| B14-C07 | P2 | **CLOSED** | `knowledge/01-hardware/bmc-firmware-and-events.md:179` | 已区分日志溢出计数与端到端投递丢失/重复计数，记录 `OverflowErrorCount` 的条件性出现、版本和实现边界；研究记录同步。上游定位：`LogEntry.v1_22_0` → `definitions.LogEntry.properties.OverflowErrorCount`，只读 integer，新增于 v1.14.0。([redfish.dmtf.org](https://redfish.dmtf.org/schemas/v1/LogEntry.v1_22_0.json)) |
| B14-C08 | P2 | **CLOSED** | `knowledge/01-hardware/node-selection-and-lifecycle.md:167`、`knowledge/01-hardware/node-selection-and-lifecycle.md:191` | 正常安装与显式保留 Data RAID 分支、各自数据破坏范围已分清；删除“只覆盖 OS 盘”及未经证明的 Clear 等级推断。研究记录和来源登记同步。上游定位：DGX OS 7 → **Reimaging → 两个安装分支**。([docs.nvidia.com](https://docs.nvidia.com/dgx/dgx-os-7-user-guide/reimaging.html)) |
| B14-C09 | P2 | **CLOSED** | `knowledge/01-hardware/node-selection-and-lifecycle.md:185` | 新增独立凭据关闭门槛，含清单、处置方式、责任人与证据；未解决项阻止正常关闭，或进入明确授权、可审计且有期限/复审点的风险接受流程。满足该项原关闭条件，未编造 OEM 命令。 |
| B14-C10 | P2 | **OPEN** | `knowledge/01-hardware/bmc-firmware-and-events.md:113`、`sources/registry.yaml:1718` | “部分取得”口径、具体条目范围及带外—带内映射缺口已统一；但原关闭条件要求补取所列告警原文，本轮仍未独立取得。详见下一节。 |
| B14-C11 | P3 | **CLOSED** | `knowledge/01-hardware/health-evidence.md:249`、`knowledge/01-hardware/health-evidence.md:416` | 当前处置入口及来源链接已对齐 `/deploy/gpu-debug-guidelines/gpu-node-triage.html`，该官方页本轮可读。旧地址仅作为历史说明保留，不再充当有效处置入口。未把作者的 HTTP 状态测量当作本轮独立测量。([docs.nvidia.com](https://docs.nvidia.com/deploy/gpu-debug-guidelines/gpu-node-triage.html)) |
| B14-C12 | P2 | **CLOSED** | `knowledge/01-hardware/node-selection-and-lifecycle.md:76`、`sources/registry.yaml:2016` | 已改称跨版本基准索引，研究记录及登记同步；官方 **Benchmarks → RetinaNet → Latest Version Available** 为 v5.1，正文不再整体归入 v6.0。未取得 v6.0 专属结果表的限制仍保留。([mlcommons.org](https://mlcommons.org/benchmarks/training/)) |

## 三、仍开放项与新的关闭条件

### B14-C01｜OPEN｜Xid 140、155 的边界解释仍越界

**剩余差距：**

- `knowledge/01-hardware/health-evidence.md:239` 仍写“不可纠正错误**多到**无法完成……标记”；`docs/research/batch-14-error-code-mapping-sources.md:15` 同样保留“UE 多到”。上游 Table 1 的 Xid 140 只描述错误以某种方式中断驱动的页离线/行重映射标记能力，不支持数量过多这一因果解释。
- `knowledge/01-hardware/health-evidence.md:243` 将 Xid 155 概括为“不是异常故障”。Table 1 的 intentional 标记不能证明行为符合预期；Table 3 的 `INVESTIGATE_SW_USER` 明确保留非预期时调查软件或用户动作的分支。([docs.nvidia.com](https://docs.nvidia.com/deploy/xid-errors/analyzing-xid-catalog.html))

**关闭条件：**

1. 删除 140 的“多到”等数量因果措辞，正文与研究记录同步。
2. 155 仅陈述 intentional 标记及触发条件，保留非预期时的调查分支，不直接判为无异常。
3. 保留已正确照录的立即动作、调查动作和产品适用性，针对两行重新核对。

### B14-C06｜OPEN｜Not Available 仍被当作失败类别

**剩余差距：**

`knowledge/01-hardware/health-evidence.md:362` 已列出硬件不上报、驱动不支持和 metrics 版本错配三种原因，却仍归结为“采样失败或版本错配”；第 387 行又把这些情况放入“诊断失败”栏。后文的“原因未定记 unknown”不能消除该表的错误分类。

上游定位：AMD SMI 27.1.0、`docs-10.1.0` 文档树 → **Interpreting the output → About N/A values → Not Available**。原文给出多种不可取回数据的原因，并不将它们统一定义为诊断失败。([rocm.docs.amd.com](https://rocm.docs.amd.com/projects/amdsmi/en/docs-10.1.0/how-to/amdsmi-cli-tool.html))

**关闭条件：**

1. 将 Not Available 本身记录为数据不可用，不直接赋予失败类别。
2. 联合支持说明、设备/驱动/库版本及调用状态判定：不支持或不提供属于覆盖边界，查询失败属于采集失败，解析错配单独记录；原因不明保留 unknown。
3. 从“诊断失败”示例中移除仅凭 Not Available 作出的归类，改用有明确执行失败证据的示例；同步检查研究记录与来源说明。

### B14-C10｜OPEN｜口径已统一，但告警原文补取条件未满足

**已完成部分：** 正文、metadata、研究记录和 registry 已统一“部分取得”，列明所引事件码，并区分告警条目与官方跨层映射。这部分修订有效。

**剩余差距：** 精确目标 **`EDOC1100317321` 告警处理 05、分页 `4c88faf1`** 本轮仍未取得告警正文。作者修订记录也说明此次只取得页面壳，具体码义及建议继续依赖首次取证记录。该记录不能代替原始告警条目。

这不是认定所列代码错误，而是**原文补取关闭条件尚未满足**。

**关闭条件：**

- 提供可独立读取的官方 PDF、原始正文或保留文档版本与分页身份的原文存档，覆盖当前所引事件码的含义、条件、影响及处理建议，再逐项复核；或
- 在原文取得前，将未验证的代码特定影响/建议从确定性技术证据降为待核对记录，不据此建立处置规则。

带外—带内官方映射仍可保留为 unknown，无须为关闭本项编造映射。

## 四、新发现

### B14-C13｜P2｜对整个 Xid 目录作“无计数阈值关联”的绝对断言

- **位置：** `knowledge/01-hardware/health-evidence.md:216`
- **问题：** “目录不将任何 Xid 直接绑定到计数器阈值”否定了目录中实际存在的阈值解码和调查分支，也与本文第 225 行的 SRAM 阈值描述冲突。事件码不是计数器，并不意味着相关工作流没有阈值语义。
- **精确上游证据：** Xid Catalog **Table 3 → `WORKFLOW_NVLINK_ERR` → Fifth register bits 20/23/26/29** 明确表示 ECC 错误阈值超过；**`WORKFLOW_XID_48`** 要求检查 SRAM Error Threshold 标志。([docs.nvidia.com](https://docs.nvidia.com/deploy/xid-errors/analyzing-xid-catalog.html))
- **关闭条件：** 改为区分“事件标识”和“计数/阈值证据”；明确个别工作流包含阈值条件，须按条目解码。不得从 Xid 140 推导计数门限，也不得否定整个目录的阈值分支。

### B14-C14｜P2｜CSV 空节表示规则遗漏决定性条件

- **位置：** `knowledge/01-hardware/health-evidence.md:363`
- **问题：** “CSV 中该节字段补 N/A”被写成通用规则，遗漏所有设备均不报告该节时**整组列被省略**的情况，可能误导采集器对缺列和缺值的解释。
- **精确上游证据：** AMD SMI CLI → **About N/A values → Empty Section 最后一段**：本次运行无设备报告该节时，CSV 删除相应列；仅部分设备缺失时才填 N/A。([rocm.docs.amd.com](https://rocm.docs.amd.com/projects/amdsmi/en/docs-10.1.0/how-to/amdsmi-cli-tool.html))
- **关闭条件：** 分别写明两种 CSV 行为及设备集合条件；不能将缺列自动解释为零值、正常状态或已覆盖。

## 五、本轮未独立取得的材料与覆盖限制

| 材料 | 本轮状态及影响 |
|---|---|
| 华为 `EDOC1100317321/4c88faf1` 所列告警原文 | 已尝试获取，未取得正文；**直接阻止 C10 关闭**。不对作者所列码义、影响和建议作独立背书。 |
| AMD `docs-10.1.0` 的 `conceptual/gpu-reset-behavior.html`、`conceptual/ras.html` | 原页获取失败。已取得同版本 CLI，足以支持本轮 reset/参数/N/A 核对，但不能替代 conceptual 页全部内容。 |
| 同源 `Xid-Catalog.xlsx` 及 PDF | 本轮未独立下载解析；核对依据是可读取的官方 HTML Tables 1–3。作者声明的 XLSX 交叉核对不计入本轮审阅工作。 |
| MLPerf v6.0 专属结果表及相关补充文件 | 未取得，不对结果数值、系统成绩或专属套件完整性作结论；C12 仅关闭混合版本索引的错误命名。 |
| 初审其他未覆盖材料 | 本轮未全面重开 Atlas A3 细部指南/码表附件、Supermicro 完整手册、其他 iBMC/DMTF 单文件、GPU Memory Error Management 实际正文及 DGX 具体维修章节。初审的相应限制继续有效。 |
| NIST、完整生命周期及硬件实证 | 本轮未重新逐章复核 NIST Rev.2 或 OEM 凭据政策；C09 仅关闭本地流程门槛遗漏。没有设备支持矩阵、实际复位影响范围、跨层完整时间线或介质清除实测。 |

获取失败仅表示本轮没有取得原文，**不等于已确认 HTTP 404，也不证明材料不存在**。

## 六、最终结论

**暂不通过。**

原发现 **B14-C01、B14-C06、B14-C10** 仍开放；新增 **B14-C13、B14-C14** 待修订。其余九项可以关闭，不要求重复返工。

下一轮应针对这五项完成正文及证据记录同步修订，并按上述条件定向复核。结构检查通过、修订摘要声明完成，均不能替代技术发现关闭；本报告也不构成硬件验证或现场操作授权。
