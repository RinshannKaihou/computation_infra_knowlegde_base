# 第十四批定向复核记录·第三轮（gpt-6.1-sol / xhigh）

复核日期：2026-10-09。复核者：Codex 会话（resume），模型 gpt-6.1-sol / xhigh。复核对象：B14-C10/C15 的第三轮修订。**最终结论：通过——限于已审阅范围并保留证据边界。** 复核输出全文照录如下。

---
# Batch 14 第三轮定向复核报告

## 一、复核信息

- **复核日期：2026-10-09，Asia/Shanghai。**
- **模型 / effort：用户约定 `gpt-6.1-sol / xhigh`。** 当前接口未提供可核验的实际运行模型及 effort 标识，不将约定配置写作已独立确认的运行配置。
- **范围：** B14-C15 的产品边界，以及 B14-C10 在正文、metadata、研究记录和 registry 中的证据链标注；同时核对 Batch 13 的处理先例。
- **结构检查：** `PYTHONDONTWRITEBYTECODE=1 make check` **PASS：77 content entries；210 sources**。未修改文件、未运行 `make build`、未执行硬件操作。

## 二、逐项判定

### B14-C15：CLOSED

`knowledge/01-hardware/health-evidence.md:216` 已在第五寄存器 bits 20/23/26/29 的说明旁加入 **Hopper-based products** 限定，并明确：

- 第一、第三、第四和第五寄存器的位图解释限定于 Hopper；
- 不得仅凭 Xid 74 的 A100 适用性推导 A100 使用相同位图；
- 不推广到 Blackwell 的 `WORKFLOW_NVLINK5_ERR`，后者按 Table 2 解码。

这与本轮重新打开的官方 **Xid Catalog → Table 3 → WORKFLOW_NVLINK_ERR** 的产品限定一致。([docs.nvidia.com](https://docs.nvidia.com/deploy/xid-errors/analyzing-xid-catalog.html))

`docs/research/batch-14-error-code-mapping-sources.md:13` 和 `knowledge/01-hardware/health-evidence.md:63` 也已同步。**未发现该项仍有关闭差距。**

### B14-C10：CLOSED——限定为“编写者核对记录、未独立核验”

本轮接受用户明确提出、且与 Batch 13 一致的**限定关闭方式**：保留编写者核对记录，完整披露独立审阅未取得原文，并限制其用途。**这不是将华为告警原文的独立核验任务记为完成。**

四类位置的核对结果如下：

| 类别 | 核对位置 | 结果 |
|---|---|---|
| **正文** | `knowledge/01-hardware/bmc-firmware-and-events.md:113`、`knowledge/01-hardware/health-evidence.md:433` | 总声明明确区分编写者取得与审阅者未核验，保留事件码清单，并禁止据此单独建立处置规则。BMC 文中的时钟、容量、采集失败、映射例和反例引用均有就地提示或回指该边界。 |
| **Metadata** | `knowledge/01-hardware/bmc-firmware-and-events.md:41`、`knowledge/01-hardware/health-evidence.md:63` | 已明确标注编写者核对记录、独立审阅者两轮未取得原文，以及不单独建立处置规则。没有将编写者取得升级为审阅者取得。 |
| **研究记录** | `docs/research/batch-14-bmc-firmware-sources.md:63`、`docs/research/batch-14-bmc-firmware-sources.md:114`；`docs/research/batch-14-error-code-mapping-sources.md:60`、`docs/research/batch-14-error-code-mapping-sources.md:92` | 统一记录取得方式差异和未独立核验状态。BMC 表的共同声明明确覆盖“本表所引条目”，后续“同上”条目受该限定约束，不要求逐行重复整段声明。 |
| **Registry** | `sources/registry.yaml:1718` | 明确标注所列 12 码为编写者渲染提取、逐字核对的记录；审阅者两轮未取得原文、未独立核验；引用方不得据此单独建立处置规则。 |

同时核对了 `docs/research/batch-13-codex-recheck.md:9`：该先例允许保留编写者解析记录支持的限定归纳，但不得写成独立审阅者已核验附件。**本次处理与该先例同等，没有扩大为独立正确性背书。**

未发现实质性引用遗漏或相反的独立核验声明。修订记录中仍要求补取原文的事项，继续作为**提升独立核验状态的待补证据任务**保留；在本轮用户认可的限定验收口径下，不再阻断 C10 的限定关闭。

## 三、新发现与最终结论

**本轮无新增发现；不新增 B14-C16。**

**Batch 14 最终结论：通过——限于前轮及本轮已审阅范围，并保留下列证据边界。**

累计 **B14-C01–B14-C15 均已关闭**；其中 **C10 按“编写者核对记录、未独立核验”的限定状态关闭**。该结论不表示全部来源均已独立取得，也不构成硬件验证、平台兼容性认证或现场操作授权。

## 四、仍须保留的证据边界

1. **华为告警处理 05：** `EDOC1100317321/4c88faf1` 所列 12 个事件码的含义、影响及建议，仍属于编写者核对记录；独立审阅者前两轮未取得原文、未独立核验。本轮不改变该事实，不能据此单独建立处置规则。
2. **版本与跨层映射：** 告警处理 05 不代表全册已覆盖，不能与 iBMC 用户指南其他版本直接合并；带外 iBMC 告警码与带内黑匣子/健康管理码的官方映射仍为 unknown。
3. **NVIDIA 解码边界：** 本次 NVLink 寄存器位图限定于 Hopper，不向 A100/Blackwell 外推；事件标识不是计数器读数，不得由 Xid 140 推导数量门限。
4. **平台证据范围：** A3 黑匣子附件仍仅存在性核对；GB200 管理面证据仅覆盖已声明的计算托架范围；AMD 侧 OEM/BMC 证据不代表 AMD 官方或其他 OEM 的实现。
5. **未补齐材料：** 前轮声明的 AMD 逐 AFID 处置/阈值、MI200 字段矩阵、CPER 保留条件、部分完整 OEM 维修条款及结果级基准证据等，不因发现关闭而自动变为已核验。华为保修介质保留条款仍未取得、未登记。
6. **无现场实证：** 没有真实设备操作、时钟偏差数值、完整跨层事件时间线或恢复验证；文档审阅通过不等于硬件实测通过。
