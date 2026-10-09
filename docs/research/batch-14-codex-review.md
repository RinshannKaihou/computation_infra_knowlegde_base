# 第十四批审阅记录（gpt-6.1-sol / xhigh）

审阅日期：2026-10-09。审阅者：Codex 会话，模型 gpt-6.1-sol，reasoning effort xhigh（用户当前约定）；正文编写者：Kimi（主会话），取证与撰写：探索/撰写子代理。审阅输出全文照录如下。

---
# Batch 14 独立技术审阅报告

## 一、审阅信息与结论

- **审阅日期：2026-10-09，Asia/Shanghai。**
- **模型 / effort：用户指定 `gpt-6.1-sol / xhigh`。** 当前接口未提供可核验的运行时模型与 effort 标识，不能将指定配置写作已经独立确认的实际运行配置。
- **角色：独立审阅者。** 编写者的四份取证记录用于定位主张，不代替上游核对。
- **执行边界：只读审阅。** 未修改仓库，未执行设备查询、固件更新、复位、诊断、基准或介质清除操作。

**结论：暂不通过。**

发现 **12 项问题：P1 三项、P2 八项、P3 一项**。主要阻断项不是一般性的证据缺失，而是错误码含义、诊断退出码处置和复位影响范围的实质性偏差。另有部分精确上游材料未能取得，不能对这些主张作“全部独立核对完成”的声明。

本结论属于文档技术审阅，**不构成硬件验证、平台兼容性认证或现场操作授权**。

## 二、已完成核对范围

| 范围 | 已完成工作 | 不能据此宣称完成的部分 |
|---|---|---|
| 仓库规范与验收 | 阅读 `README.md`、`docs/authoring-guide.md`、`content-outline.md`、内容 schema，以及 T01-05 至 T01-08 的 acceptance、evidence_blockers；核对五份交付正文、四份研究记录及新增来源登记 | 任务中的空 `evidence_blockers` 不等于所有外部证据已经独立核验 |
| T01-05：组成与拓扑 | 重新核对 GB200 NVL72 硬件章节、Atlas A3 产品页、AMD MI300X 平台数据表和 Supermicro AS-8125GS-TNMR2 数据表中的主要组成、容量、接口及功率口径。citeturn12view0turn18view1turn17view5turn17view6 | Atlas A3 用户指南的细部结构与规格表、MNL-2671 的完整手册条款未完成独立核对 |
| T01-06：BMC、固件与事件 | 核对可取得的 Redfish Event、EventService、EventDestination、SoftwareInventory、UpdateService、MessageRegistry、LogEntry schema；核对 DGX H100/H200 管理与更新章节、GB200 **计算托架** Redfish 章节及 Supermicro Redfish 指南相关段落。citeturn16view0turn16view1turn16view2turn16view3turn16view4turn16view5turn1view2turn10view0turn10view5turn4view0turn4view2 | 华为 iBMC 原文、部分 DMTF 单文件、Supermicro BMC 完整手册仍有获取缺口 |
| T01-07：错误与健康语义 | 逐项核对代表性 Xid 表、DCGM Exit Codes、AMD AFID 表、AMD SMI 固定文档树的 CLI 参数、N/A 与 reset 警告；核对固定 Linux 快照的部分 RAS 文档/实现及 OCP RAS 跨通道要求。citeturn1view0turn2view1turn7view0turn1view3turn10view4 | Ascend 错误码附件、部分 AMD conceptual 页面、完整平台支持矩阵及端到端实例未完成 |
| T01-08：生命周期 | 核对 NIST SP 800-88 Rev.2、DGX OS 7 重镜像分支、DGX Service Manual 总则、NVSM、SuperPOD 验证文档、SuperBench v2、MLPerf Training 索引及所引 Dell 擦除资料的适用范围。citeturn10view3turn4view3turn14view2turn15view0turn14view4turn7view1turn18view16turn15view3turn15view4 | OEM 具体维修章节、部分华为生命周期材料及结果级基准证据未完成 |
| 结构检查 | 执行 `PYTHONDONTWRITEBYTECODE=1 make check`，结果：**PASS，75 个内容条目，163 条来源** | 检查不验证远端链接可用性或技术正确性；按要求未运行 `make build` |

补充取证：同一篇 SuperBench `arXiv:2402.06194v2` 的 **§4、Table 2** 本次可以读取。因此，它不再属于本次审阅的获取缺口；但这不能反推编写者此前一定成功取得，也不证明表中项目在目标机器上已验证。citeturn7view1

## 三、声明的未覆盖项与复核补取要求

以下项目**没有获得独立审阅通过**。复核时，若继续保留依赖这些材料的实质性主张，必须取得精确版本原文；不能以产品页、研究记录或邻近版本代替。

| 未覆盖项 | 复核必须补取的材料或定位 |
|---|---|
| **Atlas A3 细部组成** | `EDOC1100401572` 用户指南 13：产品概述、物理结构、计算柜表 9-2、节点/总线/供电相关页；`EDOC1100401573` 维护与服务指南 14；`EDOC1100463086` LingQu 630 V1 用户指南 03。产品页不能替代抽屉、板卡、端口、部件数量和维护条款 |
| **华为 iBMC 与 A2 生命周期条款** | `EDOC1100317056` 所引 Redfish、升级、一键收集分页；`EDOC1100317321` 告警处理 05 中正文实际列出的事件码；`EDOC1000126991` 接口参考 23；`EDOC1100317202`、`EDOC1100317204` 的所引条款。须记录实际取得的分页/行，特别是日志容量、时间事件、缓存及维修凭据说明 |
| **Ascend 错误码与返回码** | HDK 26.1.0 A2 黑匣子错误码附件、健康管理故障定义附件及所引 DCMI/npu-smi 页面，核对表名、码值、级别、检测条件和建议。A3 至少补核附件身份与存在性；若要扩展到 A3 逐码解释，必须取得并解析原始附件，不能复用 A2 行 |
| **Supermicro 完整手册** | MNL-2671 Rev.1.0b、X13/H13/B13 BMC 手册及生命周期所引 MNL-2596、MNL-2356 的具体章节。数据表或通用 Redfish 指南不能证明日志 FIFO、时间同步、特定热插拔、维修或 RMA 条款 |
| **DMTF 尚未取得的单文件** | `Manager.v1_25_0`、`Update.1.4.0`、`StorageDevice.1.6.0` 等所引精确字段/消息。若单文件已足以定位版本与内容，不必为了形式强制取得 bundle ZIP |
| **AMD 固定版本 conceptual 与内核边界** | `docs-10.1.0` 的 `conceptual/ras`、`conceptual/gpu-reset-behavior` 原页，核对 CPER/AFID 数量、恢复及保留条件；补核固定 Linux 快照中相关 RAS 接口的完整生成文档/实现。`develop` 页面只能作为补充，不能证明固定版本一致 |
| **其他所引正文条款** | NVIDIA GPU Memory Error Management 的实际正文及适用产品/RMA 条款；DGX Service Manual 中被引用的具体更换前后步骤；OCP 版本索引与所引版本身份；若要列举 MLPerf v6.0 套件，补取版本专属清单或结果表 |

以下边界应继续保留，而不是为了“完整”编造补齐：

- 没有真实设备、时钟偏差数值、完整跨层时间线或现场恢复验证。
- 华为保修介质保留条款尚未取得、未登记；除非正文要据此作处置决定，否则应继续保留为缺口。
- A3 码表逐行内容、AMD 官方生命周期/RMA 资料等未取得项目，不能默认转化为已覆盖能力。

## 四、发现列表

### B14-C01｜P1｜代表性 Xid 表存在成组的错误映射与错误处置

**位置：** `knowledge/01-hardware/health-evidence.md:216`、`knowledge/01-hardware/health-evidence.md:220`

**问题：** 多行不是简化表达，而是将不同事件机制、适用产品或处置语义对应到了错误码：

| 正文条目 | 独立核对结果 |
|---|---|
| 31：非法/损坏 push buffer | 31 是 GPU 内存页故障 |
| 43/45：立即动作同为复位 GPU 加重启应用 | 43 的目录立即动作是忽略，说明应用故障后 GPU 仍可保持健康；45 需按其工作流及伴随事件解释 |
| 62/74：均属 NVLink | 62 是内部微控制器/PMU 停止，不是 NVLink 事件 |
| 92/94/95：错误遏制三部曲 | 92 是单比特 ECC 错误率过高，不是遏制级别 |
| 110：Ampere 异步热相关 | 110 是安全故障 |
| 121：GSP/RC 错误 | 121 是 Grace C2C 已纠正错误，目录中的产品适用性也不同 |
| 140/143：ECC 计数门限/未纠错 SBE | 140 是未恢复的 ECC 错误；143 是 GPU 初始化错误 |
| 144–150：SRAM、页表、PMU、QMD 等；145 处置桶为空 | 该组属于 NVLink 5 事件；145 的目录处置并非空白 |
| 155/156/158：重启未清除/RL/SXM 存在性 | 分别对应有意的软件定义 NVLink 下线、资源退休事件和 GPU 致命超时 |

这些错误会直接影响归因、故障域判断和恢复动作。

**证据：** NVIDIA *Analyzing Xid Errors with Xid Catalog*，**Table 1 对应码行**；144–150 还需对照 **Table 2 子码及版本解码**。GPU Node Triage 的常见 Xid 表也与正文的 62、92 等解释不一致。citeturn1view0turn3view0turn17view0

**关闭条件：**
- 从精确目录逐行重建整张表，而非只修上述例子。
- 分开记录码义、产品 YES/NO、立即动作、调查动作和子码版本条件。
- 删除无依据的 140 阈值解释和 145 空桶示例。
- 同步核对研究记录及所有依赖该表的处置说明，完成整表定向复核。

---

### B14-C02｜P1｜DCGM 退出码被改写成未经支持的处置动作

**位置：** `knowledge/01-hardware/health-evidence.md:243`、`knowledge/01-hardware/health-evidence.md:367`

**问题：**
- **226** 被写成“重启节点并复查”，但所引 Exit Codes 的含义是诊断运行后报告错误，不支持从该码单独推出无条件节点重启。
- **205** 被写成“联系支持”，遗漏其**需要隔离**的关键语义。
- **237** 被归为“检测链状态/诊断前置条件”，弱化了**GPU 需要复位**的设备状态含义。

这会造成不必要的重启，或遗漏隔离要求。

**证据：** DCGM Diagnostics User Guide，**Exit Codes**：226 对应 `DCGM_ST_NVVS_ERROR`，205 对应 `DCGM_ST_NVVS_ISOLATE_ERROR`，237 对应 `DCGM_ST_RESET_REQUIRED`。编写者研究记录 `docs/research/batch-14-error-code-mapping-sources.md:20` 及既有登记已保留较正确的语义，正文发生了偏移。citeturn2view1

**关闭条件：**
- 恢复退出码的符号与原始含义，另列有精确分诊分支支持的动作。
- 保留 205 的隔离要求；不得由 226 单独推出节点重启。
- 修正五义对照、reset 对照及相关处置链说明。
- 若动作另有上游依据，必须补上对应条件和精确流程定位。

---

### B14-C03｜P1｜AMD GPU reset 的影响范围只强调 hive，遗漏已公开的更大范围

**位置：** `knowledge/01-hardware/health-evidence.md:333`、`knowledge/01-hardware/health-evidence.md:398`

**问题：** 正文将复位前核对集中在 XGMI hive，未明确列出同一固定 CLI 文档已经警告的两种扩大影响：
1. 共享上游 PCIe switch 的 Secondary Bus Reset 可能影响其后的其他 GPU，**不受 hive 边界限制**；
2. 持有 `/dev/kfd` 打开句柄的进程可能被终止，即使未使用被复位的 GPU。

一般性的“现场确认影响范围”不足以替代这些已知检查项。

**证据：** AMD SMI 27.1.0、`docs-10.1.0`，CLI 文档 **`amd-smi reset` → Warning**。citeturn9view2

**关闭条件：**
- 将 hive、共享 PCIe reset 域和 KFD 进程/负载分别列为影响范围核对项。
- 将授权、负载退出、证据保全及恢复安排与上述范围绑定。
- 无法确认影响范围时不得据 hive 清单推断安全复位；同步修正跨平台 reset 和操作前提段落。

---

### B14-C04｜P2｜AFID 数字、严重度与分类错配

**位置：** `knowledge/01-hardware/health-evidence.md:324`、`knowledge/01-hardware/health-evidence.md:358`

**问题：** 正文两处将 **AFID 22** 写为坏页退休门限事件、Fatal。另将设备内部错误的“All Others Corrected/Fatal”放入 Unidentified 类。

**证据：** AMD **UG70122 v1.0，AFID Event List，Table 1**：
- **19**：坏页退休门限，Fatal；
- **22**：片内 ECC，不可纠正但非致命；
- 设备内部类的剩余错误行与 **34：Unidentified** 是不同分类。citeturn7view0

**关闭条件：**
- 若要举坏页门限例，改用 19；若保留 22，修正事件类型和严重度。
- 按 Table 1 复核 15–34 的数字、Category、Type、Severity。
- 同步修正对照表和研究记录，不从码值另行推导未公开的数值门限或处置动作。

---

### B14-C05｜P2｜AMD SMI 命令参数错误，计数采样被写成事件流

**位置：** `knowledge/01-hardware/health-evidence.md:311`、`knowledge/01-hardware/health-evidence.md:339`

**问题：**
- `amd-smi monitor -e` 输出 ECC/PCIe replay **计数采样**，不是独立事件流；未给出 watch 参数也不能表述为持续采集。
- 小写 **`-v` 是 VRAM**，不是 violation；violation 是大写 **`-V` / `--violation`**。

错误也被带入未覆盖对照表和 `sources/registry.yaml:1842`。

**证据：** 同一固定 CLI 文档，**`amd-smi monitor` 参数表**及 `--watch`、ECC、VRAM、violation 说明。citeturn2view3

**关闭条件：**
- 优先使用不易混淆的长参数，修正所有 violation 示例。
- 分开记录计数值、差值、采样窗口和真正事件记录。
- 持续采样示例必须包含其持续采样参数，并保持“未执行”标识。
- 同步修正 registry 和研究记录。

---

### B14-C06｜P2｜N/A 被机械映射为“采样失败/空结果/未覆盖”

**位置：** `knowledge/01-hardware/health-evidence.md:339`、`knowledge/01-hardware/health-evidence.md:361`

**问题：** Not Available 不只表示暂时采样失败；Empty Section 也不能直接认定为空结果或未覆盖。当前映射可能把支持性问题、解析问题或整段查询失败错误分类。

**证据：** AMD SMI CLI **About N/A values**：无值可以来自硬件/驱动不提供字段、metrics 版本解析不匹配；整段 N/A 还可能来自查询失败。citeturn2view4

**关闭条件：**
- 保留字段级和 section 级区别、原始输出及 API/调用状态。
- 联合设备、驱动、库版本和支持说明判定类别。
- 不能确定原因时记录 unknown，不能仅凭 N/A 自动分配“空结果”或“未覆盖”。

---

### B14-C07｜P2｜“Redfish 规范没有丢失计数器”的绝对断言不成立

**位置：** `knowledge/01-hardware/bmc-firmware-and-events.md:179`、`knowledge/01-hardware/bmc-firmware-and-events.md:210`

**问题：** 正文及研究记录宣称没有规范级丢失/重复计数器，遗漏了与日志溢出相关的标准字段。虽然没有由此得到覆盖所有投递丢失与重复的通用计数器，但不能将局部标准计数能力一并否定。

**证据：** **`LogEntry.v1_22_0` → `definitions.LogEntry.properties.OverflowErrorCount`**，只读整数字段，`versionAdded` 为 v1.14.0，定义了日志条目间的溢出错误计数及条件性出现规则。citeturn2view2

**关闭条件：**
- 改为区分“日志溢出计数”和“覆盖所有投递丢失/重复的端到端计数”。
- 记录 schema 版本、字段可选性与设备实现 unknown。
- 不把字段缺失解释为通用零丢失，也不声称本批设备已实现该字段。
- 同步修正研究记录的对应断言。

---

### B14-C08｜P2｜DGX 重镜像默认行为解释错误，并暗示未经证明的清除等级

**位置：** `knowledge/01-hardware/node-selection-and-lifecycle.md:167`、`knowledge/01-hardware/node-selection-and-lifecycle.md:190`

**问题：** “存在保留数据 RAID 选项”被错误推导为“默认流程不覆盖数据盘”。已知缺口段还写成“重镜像只覆盖 OS 盘”。此外，“至多接近 Clear 级覆写”没有足够证据支撑，容易作为退役处置依据被复用。

**证据：**
- DGX OS 7 **Reimaging → DGX OS ISO Boot Options** 分列正常的重新格式化数据 RAID 安装，以及显式的 **Without Reformatting Data RAID** 保留分支；前一分支会重新分区 OS 和数据驱动器。citeturn5view4
- NIST Rev.2 **§3.1.1、§4.5** 要求按清除范围、技术及验证/确认判断，不能仅凭重装或格式化推定清除等级。citeturn11view5

**关闭条件：**
- 准确描述两个安装分支及其数据破坏范围。
- 删除“默认不覆盖数据盘”“只覆盖 OS 盘”的概括。
- 将重镜像与介质 sanitization 分开；没有技术和验证证据时不赋予 Clear/Purge 等级。
- 同步修正已知缺口、研究记录和 `sources/registry.yaml:1914`。

---

### B14-C09｜P2｜退役关闭条件遗漏凭据处置，unknown 可能随状态关闭

**位置：** `knowledge/01-hardware/node-selection-and-lifecycle.md:170`、`knowledge/01-hardware/node-selection-and-lifecycle.md:178`

**问题：** 凭据清单被要求列出并保留 unknown，但“全部满足才可关闭”的五项判据没有凭据处置门槛。因此，数据介质证书、资产更新和签名齐全时，仍可能在 BMC 账户、证书或其他权限问题未处理的情况下关闭退役状态。

**证据：**
- 本批验收 `plans/full-coverage-backlog.yaml:4149` 明确包括**数据/凭据处置及完成判据**。
- NIST Rev.2 **§4.6** 的介质清除证书不能单独证明外部账户或管理面权限已经撤销；这是本报告对现有关闭条件充分性的判断，并非声称 NIST 提供了完整服务器凭据清单。citeturn11view6

**关闭条件：**
- 增加独立的凭据处置关闭项，包含清单、适用处置方式、责任人和证据。
- 不编造 OEM 命令或未取得的许可证政策。
- 未解决项应阻止正常关闭，或进入明确授权、可审计的残余风险接受流程，不能仅留下 unknown 后关闭。

---

### B14-C10｜P2｜iBMC 告警处理材料的取得范围在交付物间不一致

**位置：** `knowledge/01-hardware/bmc-firmware-and-events.md:41`、`knowledge/01-hardware/health-evidence.md:407`

**问题：** BMC 文档记录已核对告警处理 05 并引用具体事件码；健康文档却称本轮告警处理正文未取得。用户声明的实际边界是**只取得部分**。目前无法从交付物明确辨认哪些条目已取得、哪些仍缺失，以及是否缺的是告警正文还是跨层对应关系。

**证据：** 交付物间的上述矛盾及用户声明；精确目标为 **`EDOC1100317321` 告警处理 05、分页 `4c88faf1`**。该原页本次也未能取得，因此本报告不对所列华为告警码及处理建议作独立正确性背书。

**关闭条件：**
- 统一批次口径为“部分取得”，列出实际取得的分页/条目/事件码。
- 区分“告警条目取得情况”和“带外—带内官方映射取得情况”。
- 在 metadata、研究记录、来源登记和已知缺口中保持一致。
- 复核所列事件码时补取对应原文，不能以主张—证据表本身关闭。

---

### B14-C11｜P3｜三处 GPU Node Triage 引用与已登记、可读取的上游地址不一致

**位置：** `knowledge/01-hardware/health-evidence.md:235`、`sources/registry.yaml:1035`

**问题：** 健康文档三处使用 `/deploy/gpu-node-triage/introduction.html`，本次无法打开；而登记来源使用另一条路径，且该页本次可读取。这些引用位于错误码到处置动作的关键入口，影响可追溯性。

**证据：** 已登记并读取的 NVIDIA **GPU Node Triage** 位于 `/deploy/gpu-debug-guidelines/gpu-node-triage.html`，含常见 Xid、诊断和复位条件表。这里报告的是地址不一致与本次访问结果，不将访问失败冒充已确认的 HTTP 404。citeturn17view0

**关闭条件：**
- 将同文三处链接对齐到精确登记来源及相关章节。
- 逐处重新打开确认；不能用本地链接检查通过代替远端核验。

---

### B14-C12｜P2｜MLPerf 混合版本索引被整体称为 v6.0 基准集

**位置：** `knowledge/01-hardware/node-selection-and-lifecycle.md:76`、`sources/registry.yaml:2016`

**问题：** 正文将所列模型整体归为“当前结果版本 v6.0 的基准集”，包括 RetinaNet，但所引页面的基准表并非所有行都属于 v6.0。正文没有保留逐基准的版本边界。

**证据：** MLPerf Training 官方页面 **Benchmarks 表 → RetinaNet 行 → Latest Version Available** 标为 **v5.1**，不支持将该行直接归入 v6.0。此处不据该表进一步断言所有历史结果或退役状态。citeturn18view16

**关闭条件：**
- 按官方表保留逐基准版本，或改称跨版本基准索引。
- 若要列举 v6.0 套件，取得版本专属清单/结果表。
- 同步修正研究记录和 registry；后续结果比较仍须同版本、同规则。

## 五、无发现项

以下是**限定在已经取得证据范围内**的无发现结论，不是对未取得材料的默认认可：

1. **元数据与结构：** 未发现本批造成的 ID 重复、失效 `source_refs` / `related_ids` 或本地文件链接问题；新增内容及索引维持 draft，未将审阅等同于实测。
2. **已核对的组成口径：** 未发现 GB200 主要托架/交换层组成、Atlas A3 产品页总量，以及 AMD/OEM 数据表主要配置口径需要另列错误发现。不同 OEM 配置未被强行统一。citeturn12view0turn18view1turn17view5turn17view6
3. **规范与实现分离：** 正文保留了新 Redfish schema 与 DGX H100/H200 较旧实现基线的区别，没有据规范字段存在就普遍宣称设备支持。此结论不覆盖 B14-C07 的计数器断言。citeturn10view0turn16view0turn16view3
4. **关键取证边界：** A3 码表仅存在性核对、GB200 仅计算托架管理面、AMD BMC 证据来自 OEM、时钟偏差无数值、华为保修介质保留材料未登记，这些边界基本保留；iBMC 部分取得口径例外见 B14-C10。
5. **跨层事件边界：** OCP 跨通道要求与官方案例未被写成目标设备已经实现的完整时间线；未执行的匹配方法未冒充本地实证。citeturn10view4
6. **生命周期适用范围：** 所引旧 NVIDIA RMA 资料及 Dell 客户端擦除 KB 的范围限制被保留，未直接作为现行全部 DGX/PowerEdge 的统一步骤。citeturn14view3turn15view4

## 六、验收判断与复核要求

| 任务 | 本次判断 |
|---|---|
| **T01-05** | 已核对部分无新增实质错误发现；关键手册条款尚未全部独立取得，**不能确认整项通过** |
| **T01-06** | Redfish 计数能力断言错误，iBMC 取证范围不一致且有未覆盖原文，**暂不通过** |
| **T01-07** | Xid、DCGM、AMD AFID/CLI/reset 影响范围存在实质错误，**暂不通过** |
| **T01-08** | 重镜像范围、清除等级、凭据关闭门槛及基准版本边界需修订，**暂不通过** |

重新申请通过前，需要：

- 关闭全部 **P1/P2**，并修复关键处置入口的 P3 链接。
- 对正文、研究记录、registry 做同一轮一致性修订，不能只修改正文。
- 补取仍支撑实质性主张的精确上游材料，针对错误码、参数、严重度、动作前提和版本边界进行**定向复核**。
- 内容修改后运行 `make check`；在可写环境运行 `make build`。两者都不能替代技术复核。

**最终结论：Batch 14 暂不通过。修订完成后必须进行定向复核，不能仅凭编写者声明“已修复”转为通过；通过文档审阅仍不代表硬件验证完成。**
