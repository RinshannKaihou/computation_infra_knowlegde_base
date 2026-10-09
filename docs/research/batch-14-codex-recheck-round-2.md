# 第十四批定向复核记录·第二轮（gpt-6.1-sol / xhigh）

复核日期：2026-10-09。复核者：Codex 会话（resume），模型 gpt-6.1-sol / xhigh。复核对象：B14-C01/C06/C10/C13/C14 的第二轮修订。复核输出全文照录如下。

---
# Batch 14 第二轮定向复核报告

## 一、复核信息

- **复核日期：2026-10-09，Asia/Shanghai。**
- **模型 / effort：用户约定 `gpt-6.1-sol / xhigh`。** 当前接口未提供可核验的实际运行模型及 effort 标识，不将约定配置写作已独立确认的运行配置。
- **范围：** B14-C01、C06、C10、C13、C14 的修订正文、对应研究记录和相关来源登记；重新读取 NVIDIA Xid Catalog 与 AMD SMI 固定文档树的 CLI 原文，并独立尝试取得华为指定告警页。
- **结果：4 项 CLOSED，1 项 OPEN；新增 B14-C15。最终结论：暂不通过。**

本轮执行 `PYTHONDONTWRITEBYTECODE=1 make check`，结果 **PASS：77 content entries；210 sources**。这是当前全仓库统计，不是 Batch 14 单批统计。未修改文件，未运行 `make build`，未执行硬件操作。

## 二、逐项判定

| 编号 | 判定 | 当前位置 | 理由及精确上游定位 |
|---|---|---|---|
| **B14-C01** | **CLOSED** | `knowledge/01-hardware/health-evidence.md:239`、`knowledge/01-hardware/health-evidence.md:243` | 140 已删除数量因果解释，改为错误中断页标记能力；155 仅陈述 intentional 标记，并保留非预期时的 `INVESTIGATE_SW_USER` 调查分支。研究记录第 15 行同步。与 **Xid Catalog Table 1 → 140/155，以及 Table 3 → INVESTIGATE_SW_USER** 一致。([docs.nvidia.com](https://docs.nvidia.com/deploy/xid-errors/analyzing-xid-catalog.html)) |
| **B14-C06** | **CLOSED** | `knowledge/01-hardware/health-evidence.md:362`、`knowledge/01-hardware/health-evidence.md:387` | Not Available 已改记“数据不可用”，不再仅凭字段级 N/A 归为诊断失败，并区分覆盖边界、采集失败、解析错配与 unknown。替换示例中的“整节查询失败”有官方明确条件依据，见下方说明。研究记录第 48、91 行同步。上游：AMD SMI 27.1.0、`docs-10.1.0` → **About N/A values**。([rocm.docs.amd.com](https://rocm.docs.amd.com/projects/amdsmi/en/docs-10.1.0/how-to/amdsmi-cli-tool.html)) |
| **B14-C10** | **OPEN：待独立核验** | `knowledge/01-hardware/bmc-firmware-and-events.md:113`、`sources/registry.yaml:1718` | 作者已声明取得正文并核对 12 个事件码，正文、metadata、研究记录与 registry 的口径已同步；但本轮仍未独立取得指定页，不能判定代码含义、影响及建议已通过独立复核。详见第三节。 |
| **B14-C13** | **CLOSED** | `knowledge/01-hardware/health-evidence.md:216` | 原绝对否定断言已删除，改为区分事件标识与计数/阈值证据。第五寄存器 bits 20/23/26/29 的阈值含义，以及 SRAM Error Threshold 标志分支，均与 **Table 3 → WORKFLOW_NVLINK_ERR / WORKFLOW_XID_48** 对齐；未编造阈值数值。新增的产品适用性遗漏另列 C15。([docs.nvidia.com](https://docs.nvidia.com/deploy/xid-errors/analyzing-xid-catalog.html)) |
| **B14-C14** | **CLOSED** | `knowledge/01-hardware/health-evidence.md:363` | 已写全 CSV 两种行为：本次运行没有设备报告该节时省略整组列；仅部分设备缺失时填 N/A。研究记录第 48、91 行同步，也明确缺列不是零值、正常或已覆盖。上游：**About N/A values → Empty Section 末段**。([rocm.docs.amd.com](https://rocm.docs.amd.com/projects/amdsmi/en/docs-10.1.0/how-to/amdsmi-cli-tool.html)) |

### C06 替换示例的核对边界

官方原文确实说明：`amd-smi static` 的 NIC/SMU/IFWI，以及 `amd-smi firmware` 的 FW_LIST，在**该节查询失败**时会将整节替换为 N/A。因此，新示例有明确的查询执行失败条件，不再是“看到 N/A 就判失败”。但节头 N/A 也可能表示没有条目，仍须保留调用状态，不能倒推查询失败。([rocm.docs.amd.com](https://rocm.docs.amd.com/projects/amdsmi/en/docs-10.1.0/how-to/amdsmi-cli-tool.html))

`ras --cper`“无 sudo 权限”在正文已限定为**执行前提不满足**；它不是本地执行失败日志，也不是 GPU 硬件诊断不通过的证据。本轮据有明确查询失败条件的厂商示例关闭 C06，**没有将权限前提或文档示例认定为现场失败实证**。

## 三、C10：独立获取结果与判定建议

### 获取结果

本轮进行了以下独立尝试：

- 两个网页读取入口均未取得 `EDOC1100317321/4c88faf1` 正文。
- 尝试官方域名变体及指定事件码检索，未获得该文档目标行的可核对原文。
- 浏览器控制没有可用浏览器会话；尝试选择本地 Edge 被工具权限拒绝，未继续绕过限制。
- 检索出现的其他机型或案例材料，**未用来替代 Atlas 800T A2 告警处理 05**。

因此，本轮状态应记录为：

> **编写者报告已取得并逐字核对；审阅者未独立取得该页原文，未独立核验所列事件码的含义、影响及建议。**

### 四个指定事件码

以下只核对了**交付物内部引用的一致性**，不表示上游技术主张已获独立确认。

| 事件码 | 作者记录及当前引用 | 独立复核状态 |
|---|---|---|
| `0x0100000D` | 内存可纠正 ECC；影响“降低系统性能”。正文见 `knowledge/01-hardware/bmc-firmware-and-events.md:189`。 | 未取得原文，不能确认含义、影响及处理建议。 |
| `0x56000019` | NPU 历史 ECC 计数达到阈值；修订记录补充“可能影响 NPU 业务功能”。正文同见第 189 行。 | 未取得原文，不能确认条目条件、影响及建议。 |
| `0x2C00000F` | 主机因未识别原因重启；正文不据此归因。见 `knowledge/01-hardware/bmc-firmware-and-events.md:194`。 | 内部引用一致；指定版本原文及建议未核验。 |
| `0x100000C3` | 主板 RTC 时间获取失败，影响 iBMC 日志时间准确性；修订记录列出相关处理建议。正文见 `knowledge/01-hardware/bmc-firmware-and-events.md:168`。 | 未取得原文，不能确认建议的完整条件及顺序。 |

**判定建议：C10 保持 OPEN，但明确是独立核验未完成，不是认定作者未取得或代码错误。**

关闭所需材料：可供审阅读取的官方导出或原始页面存档，保留文档号、版本、分页身份，以及上述四码完整的消息、参数、影响和建议。研究摘要或“逐字一致”的声明本身不能替代原文。无需因此编造带外—带内映射，该映射继续保持 unknown。

## 四、新发现

### B14-C15｜P2｜新增 NVLink 寄存器解码遗漏 Hopper 适用性限定

- **位置：** `knowledge/01-hardware/health-evidence.md:216`
- **问题：** 新段落准确引用了第五寄存器 bits 20/23/26/29，但没有保留该寄存器解释的产品边界。该段位于跨 A100/H100/B100/GB200 的代表性目录说明中，容易被当作通用解码规则。研究记录 `docs/research/batch-14-error-code-mapping-sources.md:13` 已写“Hopper 有效位”，正文未同步。
- **精确上游证据：** Xid Catalog **Table 3 → WORKFLOW_NVLINK_ERR**，在寄存器位解释之前明确限定第一、第三、第四和第五寄存器适用于 **Hopper-based products**。第五寄存器阈值位应在该限定内引用。([docs.nvidia.com](https://docs.nvidia.com/deploy/xid-errors/analyzing-xid-catalog.html))
- **关闭条件：** 正文在位图说明旁加入 Hopper 产品限定，并同步相关元数据说明；不得仅凭 Xid 74 的产品适用性就推导 A100 使用相同位图，也不得推广到 Blackwell 的 `WORKFLOW_NVLINK5_ERR` 解码。

本轮未另列其他新发现。

## 五、未独立取得的材料与最终结论

**本轮未独立取得：**

1. 华为 `EDOC1100317321/4c88faf1` 原文，包括上述四个指定事件码及作者声称核对的其余八码完整条目。
2. 作者用于交叉核对的 `Xid-Catalog.xlsx`；本轮 NVIDIA 结论依据官方 HTML Tables 1、3，不将作者的附件解析计入审阅工作。
3. 本地执行失败日志、设备权限测试及寄存器解码实测；本轮仅作文档核对。前轮其他未覆盖材料不因本轮四项关闭而自动获得背书。

**最终结论：暂不通过。**

- **已关闭：** B14-C01、C06、C13、C14。
- **待独立核验：** B14-C10。
- **新增待修订：** B14-C15。

下一轮只需处理 C10 的原文核验和 C15 的产品边界，不要求重复返工已关闭项。本结论不构成硬件验证或现场操作授权。
