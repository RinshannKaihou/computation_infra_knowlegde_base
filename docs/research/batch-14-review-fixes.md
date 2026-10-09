# 第十四批独立审阅发现修订记录（B14-C01–C12）

修订日期：2026-10-09。修订者：修订子代理（按主会话指派）。审阅原文见 [batch-14-codex-review.md](batch-14-codex-review.md)。纪律：每项修订均基于本轮重新打开的精确上游证据（FetchURL 或 curl 取原始 HTML/JSON/XLSX 解析）；取不到的部分如实保留限定。修订未在任何真实设备上执行查询、诊断、复位、重镜像或介质清除。`make check` 与 `make build` 结果：**PASS（75 内容条目，163 来源）**。

## 逐项关闭情况

### B14-C01（P1，Xid 表重建）→ 已修订

- **修改位置**：`knowledge/01-hardware/health-evidence.md`「代表性 Xid 的最小集合」整表重建；`docs/research/batch-14-error-code-mapping-sources.md` NVIDIA 主张行加复核注记。
- **依据**：2026-10-09 重新打开 [Analyzing Xid Errors with the Xid Catalog](https://docs.nvidia.com/deploy/xid-errors/analyzing-xid-catalog.html)（FetchURL 全文 + curl 原始 HTML），并下载同源 [Xid-Catalog.xlsx](https://docs.nvidia.com/deploy/xid-errors/_downloads/4586dadb59119a55d1e93a181caa4272/Xid-Catalog.xlsx)（55,673 字节）逐行解析交叉核对；Table 2（Xid 144-150 Decode）经原始 HTML 复核；另复读 [Working with Xid Errors](https://docs.nvidia.com/deploy/xid-errors/working-with-xid-errors.html)。
- **修正要点**（逐条对照审阅指出的错误映射）：31=GPU memory page fault（MMU fault，非 push buffer）；43=ResetChannel Verif Error，立即动作 IGNORE（"The GPU remains in a healthy state"）；45=Preemptive cleanup，WORKFLOW_XID_45 桶（Solo: RESTART_FM，否则随其他 Xid）；62=Internal micro-controller halt（非 NVLink）；74=NVLINK Error 且 A100/H100 YES、B100/GB200 NO；92=High single-bit ECC error rate（非遏制级别）；94/95=Contained/Uncontained memory error（RESTART_APP 与 RESET_GPU 分别配 IGNORE sympathetic）；110=Security Fault Error（非热相关，A100 NO）；121=C2C Error（仅 GB200 YES，Grace C2C 已纠正错误）；140=ECC Unrecovered Error（驱动无法完成页离线/重映射标记，**删除无依据的「ECC 计数门限」解释**）；143=GPU Initialization Error（A100 NO，CUDA 12.9/R575 起）；144–150=NVLink 5 错误族（SAW/RLW/TLW/TREX/NVLPW_CTRL/NETIR/MSE，仅 B100/GB200，WORKFLOW_NVLINK5_ERR，按 Table 2 的 Subcode **V1 <R575 IntrInfo[9:5] / V2 ≥R575 IntrInfo[6:0]** 与 Error Status 解码；145 子码桶含 IGNORE/RESET_GPU/XID_154_EVAL，**删除「145 空桶」示例**——空桶只适用于 162–172 等新行）；155=NVLINK SW Defined Error（intentional 链路下线）；156=Resource Retirement Event（A100 NO）；158=GPU Fatal Timeout。
- **表格结构**：按关闭条件分列码义、产品适用性（A100/H100/B100/GB200 四列 YES/NO）、立即动作、调查动作；144–150 的子码版本条件写入该行边界列。

### B14-C02（P1，DCGM 退出码）→ 已修订

- **修改位置**：`health-evidence.md`「DCGM diag 退出码」表与段落、「五种含义的区分」表（诊断失败行）与 reset 对照条目；研究记录 DCGM 行加复核注记。
- **依据**：[DCGM Diagnostics User Guide — Exit Codes](https://docs.nvidia.com/datacenter/dcgm/latest/user-guide/dcgm-diagnostics.html)（2026-10-09 复核）：226 `DCGM_ST_NVVS_ERROR`="DCGM GPU Diagnostic was successfully executed, but reported an error"；205 `DCGM_ST_NVVS_ISOLATE_ERROR`="The diagnostic returned an error that indicates the need for isolation"；237 `DCGM_ST_RESET_REQUIRED`="GPU requires a reset"；242 `DCGM_ST_NO_DATA`；240 `DCGM_ST_NOT_WATCHED`。
- **修正要点**：226 删除「重启节点并复查」，恢复「诊断执行完成但报告错误」原义，明示不能由该码单独推出节点重启；205 恢复「需要隔离」语义；237 恢复「GPU 需要复位」的设备状态语义，删除「检测链前置条件」弱化表述。动作列只写有上游依据的分支（处置链以 GPU Node Triage 与现场授权为准）。

### B14-C03（P1，AMD reset 影响范围）→ 已修订

- **修改位置**：`health-evidence.md`「GPU reset 语义与影响范围核对」节（原「XGMI hive 爆炸半径」节扩写）、reset 跨平台对照条目、「高影响处置入口与现场授权」段；研究记录 AMD reset 行。
- **依据**：[amd-smi CLI — reset Warning](https://rocm.docs.amd.com/projects/amdsmi/en/docs-10.1.0/how-to/amdsmi-cli-tool.html)（curl 取原始 HTML 逐字复核）与 [GPU reset behavior on XGMI systems](https://rocm.docs.amd.com/projects/amdsmi/en/docs-10.1.0/conceptual/gpu-reset-behavior.html)。
- **修正要点**：三项影响范围分别列出——① XGMI hive（复位波及同 hive 全部 GPU，用 `amd-smi xgmi`/`topology` 或 `xgmi_hive_id` 确认）；② 共享上游 PCIe switch 的 Secondary Bus Reset（"affecting all GPUs behind the same switch, independent of XGMI hive membership"）；③ 持有 `/dev/kfd` 句柄的进程可能被终止（即使未使用被复位 GPU，ROCR/HIP_VISIBLE_DEVICES 不能阻止）。授权、负载退出、证据保全与恢复安排与三项范围绑定；明示影响范围无法确认时不得据 hive 清单推断安全复位。

### B14-C04（P2，AFID）→ 已修订

- **修改位置**：`health-evidence.md`「AFID 15–34」表、「五种含义的区分」表（错误事件行 AFID 22→19）；研究记录 AFID 行。
- **依据**：[AMD Field ID 70122 v1.0 — AFID Event List](https://docs.amd.com/r/en-US/AMD_Field_ID_70122_v1.0/AFID-Event-List) Table 1（FetchURL 逐行复核，2026-10-09）。
- **修正要点**：19=Bad Page Retirement Threshold（Fatal）；22=On-die ECC（Uncorrected, Non-fatal）；28/29/30（Device Internal All Others 的 Uncorrected Non-fatal/Corrected/Fatal 三行）归入 Device Internal Errors，不再错置于 Unidentified；Unidentified 类只有 34 一行。15–34 全行数字/Category/Type/Severity 复核一致；保留「阈值数值未取得，不从码值推导未公开门限」。

### B14-C05（P2，amd-smi 参数）→ 已修订

- **修改位置**：`health-evidence.md` ECC 计数节（monitor -e）、N/A 节与五义对照表（-V/--violation）；`docs/research/batch-14-error-code-mapping-sources.md` ECC 行与代际门控行；`sources/registry.yaml` src.amd.amd-smi-docs-10.1.0 notes。
- **依据**：同一 CLI 页 monitor 参数表（curl 原始 HTML）：`-e, --ecc` = "Monitor ECC single bit, ECC double bit, and PCIe replay error counts"（计数采样）；`-v, --vram-usage` = 显存用量 MB；`-V, --violation` = 功耗/温度违例状态（"Only available for MI300 or newer ASICs"）；watch 参数 `-w/--watch INTERVAL`、`-W/--watch_time`、`-i/--iterations`。
- **修正要点**：`monitor -e/--ecc` 改述为计数采样快照，删除「事件流」；持续采样示例须含 `--watch` 并保持未执行标识（正文示例形态 `amd-smi monitor --ecc --watch 1`，标注未执行）；violation 全部改用大写 `-V/--violation` 长参数优先；区分计数值/差值/采样窗口与真正事件记录（CPER）。

### B14-C06（P2，N/A 语义）→ 已修订

- **修改位置**：`health-evidence.md`「N/A 三分与代际门控」节重写、五义对照表两行；研究记录 N/A 行。
- **依据**：同一 CLI 页「About N/A values」（curl 逐字复核）：Not Applicable（字段级，硬件/配置不适用）；Not Available（字段级，三种原因：硬件不上报、驱动不支持查询、gpu_metrics 版本比 AMD SMI 新——ROCm 7.13 起支持 v1.9 动态布局）；Empty Section（节级，两种情形：节内无条目，如 RDMA_DEVICES；或整节查询失败被 N/A 替代，官方举例 amd-smi static 的 NIC/SMU/IFWI 与 amd-smi firmware 的 FW_LIST）。
- **修正要点**：字段级与节级分开；不能确定原因时记 unknown，不得仅凭 N/A 自动归类「空结果/未覆盖」；记录保留原始输出与调用状态。

### B14-C07（P2，Redfish 计数器）→ 已修订

- **修改位置**：`knowledge/01-hardware/bmc-firmware-and-events.md`「丢失、重复与采集失败」节首句、已知缺口条目；`docs/research/batch-14-bmc-firmware-sources.md` 事件记录方法行与缺口节。
- **依据**：[LogEntry.v1_22_0.json](https://redfish.dmtf.org/schemas/v1/LogEntry.v1_22_0.json)（curl 直取 JSON）：`OverflowErrorCount` 为只读整数、`versionAdded: v1_14_0`、条件性出现（最新条目且其后无溢出错误时不出现；非最新条目且与下一条目间无溢出错误时不出现）。
- **修正要点**：「规范没有丢失计数器」改为区分「日志溢出计数」（OverflowErrorCount）与「覆盖端到端投递丢失/重复的通用计数器」（不存在）；字段缺失不等于零丢失；本批设备实现保持 unknown（DGX H100/H200 基线为 Schema 2019.1，不假设支持）。

### B14-C08（P2，DGX 重镜像）→ 已修订

- **修改位置**：`knowledge/01-hardware/node-selection-and-lifecycle.md` 退役节 DGX 重镜像条、停止条件节、已知缺口第 1 条、来源节；`docs/research/batch-14-node-lifecycle-sources.md` 对应主张行、候选登记行与缺口第 2 条；`sources/registry.yaml` src.nvidia.dgx-os-7-user-guide-reimaging-2026-10-09 notes。
- **依据**：[DGX OS 7 User Guide — Reimaging the System](https://docs.nvidia.com/dgx/dgx-os-7-user-guide/reimaging.html)「DGX OS ISO Boot Options」（FetchURL 复核，2026-10-09）：默认「Install DGX OS \<version\>」分支 "repartitions all drives, including the OS and the data drives … overwrites all the data and file systems that might exist on the OS and data drives"；显式「Install DGX OS \<version\>: Without Reformatting Data RAID (does not mount /raid)」分支保留数据盘（cache daemon 默认禁用、fstab 注释 /raid、不格式化）。
- **修正要点**：删除「默认不覆盖数据盘」「只覆盖 OS 盘」；删除「至多接近 Clear 级覆写」，改为「文档未作 sanitization 合规声明，不赋予 Clear/Purge 等级；按 NIST Rev.2 §4.5 验证/确认框架，重装或重格式化不构成清除等级证据」；重镜像与介质 sanitization 明确分开。

### B14-C09（P2，退役凭据门槛）→ 已修订

- **修改位置**：`knowledge/01-hardware/node-selection-and-lifecycle.md` 退役完成判据新增第 6 项、凭据处置条。
- **依据**：验收标准 `plans/full-coverage-backlog.yaml` T01-08（退役含数据/凭据处置及完成判据）；NIST SP 800-88 Rev.2 §4.6（介质清除证书字段——不覆盖外部账户/管理面权限，正文如实注明该判断边界，不声称 NIST 提供服务器凭据清单）。
- **修正要点**：新增独立凭据处置关闭项——BMC 账户、证书、管理面权限（远程管理入口、API 令牌、许可证绑定）逐项清单 + 处置方式（撤销/轮换/保留并记录理由）+ 责任人 + 证据；未解决项阻止正常关闭，或进入明确授权、可审计的残余风险接受流程（授权人、范围、期限、复审点），不能仅留 unknown 后关闭。未编造任何 OEM 命令。

### B14-C10（P2，iBMC 部分取得口径）→ 已修订

- **修改位置**：`knowledge/01-hardware/bmc-firmware-and-events.md`（告警模型节、verification notes、已知缺口）、`health-evidence.md`（已知缺口 iBMC 条、verification notes）、`docs/research/batch-14-bmc-firmware-sources.md`（告警模型行、缺口节）、`docs/research/batch-14-error-code-mapping-sources.md`（昇腾对齐素材行、不登记行、缺口节）、`sources/registry.yaml` src.huawei.atlas-800t-a2-ibmc-alarm-handling-05 notes。
- **统一口径**：**部分取得**。实际取得范围以 batch-14-bmc-firmware-sources.md 记录为准：事件类告警页（EDOC1100317321，文档 05，分页 4c88faf1）的部件分段编号结构与所列事件码条目（0x0100000D、0x56000019、0x0D000007、0x100000C3、0x1A000029、0x1A000011/0x1A00001B/0x1A00001D、0x1A000025、0x2C00000F、0x2C000063、0x0200000F）；不代表全册条目已核对。「告警条目取得情况」与「带外—带内官方映射取得情况」分离：iBMC 告警码（0x56 NPU 段等）与带内黑匣子/健康管理码的官方对应关系未取得，两套码不能互译。
- **如实记录**：该页为 JS 渲染，2026-10-09 复核（curl）仅取得约 386 字节页面壳，所列条目以首次取得记录为准；与审阅方本次未能取得原页的观察一致，所列华为告警码及建议未获本轮独立复核背书。

### B14-C11（P3，GPU Node Triage 链接）→ 已修订

- **修改位置**：`health-evidence.md` 三处（代表性 Xid 表后、DCGM 退出码段、高影响处置入口节）及来源节；`sources/registry.yaml` src.nvidia.gpu-node-triage-2026-10-08 notes 加复核记录。
- **依据**：2026-10-09 curl 实测——`https://docs.nvidia.com/deploy/gpu-node-triage/introduction.html` 返回 **HTTP 404**；已登记的 `https://docs.nvidia.com/deploy/gpu-debug-guidelines/gpu-node-triage.html` 返回 **HTTP 200**，FetchURL 全文复核（常见 Xid 动作表、reset 能力矩阵、Running DCGM/Field Diagnostics、Network Testing 各节）。旁证：`docs/research/batch-15-node-acceptance-sources.md` 同样记录任务书所给 URL 实测 404、有效地址为 gpu-debug-guidelines 路径。registry 中该来源 URL 本已正确，无需改址，已在 notes 中记录复核结果与章节锚点。

### B14-C12（P2，MLPerf 版本）→ 已修订

- **修改位置**：`knowledge/01-hardware/node-selection-and-lifecycle.md` 选型节 MLPerf 条与来源节；`docs/research/batch-14-node-lifecycle-sources.md` MLPerf 主张行与候选登记行；`sources/registry.yaml` src.mlcommons.mlperf-training-results-v6.0-2026-10-09 notes。
- **依据**：[MLPerf Training](https://mlcommons.org/benchmarks/training/) Benchmarks 表（2026-10-09 curl 桌面 UA 取回 HTML 解析逐行；FetchURL 403）。逐行 Latest Version Available：DeepSeek v3、GPT-OSS 20B、Llama3.1 8b、Llama3.1 405b、Llama 2 70B（finetuning）、DLRM-dcnv2、FLUX.1 = v6.0；RetinaNet（Open Images，34.0% mAP）= **v5.1**；另有 NLP Llama3.1 8b、GNN R-GAT 等 v5.1 行，BERT-large、Stable Diffusion v2（v5.0），GPT3、resnet-50（v4.1），3D U-Net（v4.0），Mask R-CNN（v3.1）等更老行。
- **修正要点**：正文改称「跨版本基准索引」，保留逐基准版本边界，不再整体称为 v6.0 基准集；结果比较须同版本、同规则；若要列举 v6.0 专属套件清单，仍需另取版本专属 results sheet（保留为限制）。

## 仍有保留的缺口（未借修订扩大结论）

- iBMC 告警处理 05 原页 JS 渲染，本轮复核仅得页面壳；所列事件码以首次取得记录为准，未获本轮独立背书。
- NVIDIA GPU Memory Error Management 仍仅核对目录结构；Atlas A3 码表仍仅存在性核对；AMD 逐 AFID 处置/阈值、MI200 字段矩阵、内核 GPU recovery 独立文档等原有缺口全部保留。
- Xid 目录与 GPU Node Triage、MLPerf 页、DGX OS 指南均为可变页面，引用继续带观察日期；v6.0 专属 MLPerf 套件清单未另取。
- 全部修订为文档层修订，不构成硬件验证或现场操作授权。

---

## 第二轮（定向复核后）：B14-C01 剩余、B14-C06、B14-C10、B14-C13、B14-C14

修订日期：2026-10-09。修订者：修订子代理（按主会话指派）。复核原文见 [batch-14-codex-recheck.md](batch-14-codex-recheck.md)（gpt-6.1-sol / xhigh，结论：原 12 项中 9 项 CLOSED、3 项 OPEN，新增 2 项）。本轮修订前重新打开了三处上游：NVIDIA Analyzing with the Xid Catalog（FetchURL 全文 + curl 原始 HTML 复核 Table 1 与 Table 3 Guidance Classes）、AMD SMI docs-10.1.0 CLI 页 About N/A values（curl 原始 HTML 逐字复核）、华为 iBMC 告警处理 05 事件类告警页（EDOC1100317321/4c88faf1，本轮经渲染提取取得正文）。`make check` 结果：**PASS（75 内容条目，163 来源）**。

### B14-C01 剩余（Xid 140/155）→ 已修订

- **修改位置**：`knowledge/01-hardware/health-evidence.md` 代表性 Xid 表 140 行与 155 行的「影响解释的边界」列；`docs/research/batch-14-error-code-mapping-sources.md` 最小代表性集合行（140/155 两处）。
- **依据**：[Analyzing Xid Errors with the Xid Catalog](https://docs.nvidia.com/deploy/xid-errors/analyzing-xid-catalog.html) Table 1 原文（2026-10-09 第三轮复核）：Xid 140 = "observed uncorrectable errors in GPU memory, in such a way as to interrupt the GPU driver's ability to mark the pages for dynamic page offlining or row remapping"——只说错误以某种方式中断了标记能力，无数量因果；Xid 155 = 'Link down events which are flagged as "intentional" (including transitions to SLEEP) will trigger this Xid'，Investigatory 桶为 INVESTIGATE_SW_USER。
- **修正要点**：140 删去「多到/数量过多」因果措辞，改为「其方式中断了驱动将这些页标记为动态页离线或行重映射的能力」；155 删去「不是异常故障」判断，只陈述 intentional 标记与触发条件，保留非预期时按 INVESTIGATE_SW_USER 调查软件/用户动作的分支。立即动作、调查动作与产品适用性照录未动。

### B14-C06（Not Available 分类）→ 已修订

- **修改位置**：`health-evidence.md`「N/A 三分与代际门控」节 Not Available 条、「五种含义的区分」表「诊断失败」行 AMD 例；`docs/research/batch-14-error-code-mapping-sources.md` N/A 主张行与「AMD 版本错配」缺口条。
- **依据**：[amd-smi CLI — About N/A values](https://rocm.docs.amd.com/projects/amdsmi/en/docs-10.1.0/how-to/amdsmi-cli-tool.html)（2026-10-09 curl 原始 HTML 逐字复核）：Not Available = "The information cannot be retrieved by the amd-smi tool at this time"，三种原因（硬件不上报、驱动不支持查询、gpu_metrics 版本错配）；原文不将它们统一定义为诊断失败。
- **修正要点**：Not Available 本身记为「数据不可用（此刻无法取回）」，不直接赋予失败类别；归类须联合支持说明、设备/驱动/库版本与调用状态——不支持/不提供=覆盖边界、查询失败=采集失败、gpu_metrics 解析错配单独记录、原因不明=unknown。「诊断失败」示例栏移除仅凭字段级 N/A 的归类，改用有明确执行失败证据的示例（`ras --cper` 无 sudo 权限；官方明示的「整节查询失败被 N/A 替代」：`amd-smi static` 的 NIC/SMU/IFWI、`amd-smi firmware` 的 FW_LIST）。

### B14-C10（iBMC 告警原文）→ 已按第一关闭路径处理（原文取得并逐项复核）

- **修改位置**：`knowledge/01-hardware/bmc-firmware-and-events.md`（告警模型段、verification notes、已知缺口）、`knowledge/01-hardware/health-evidence.md`（已知缺口 iBMC 条、verification notes）、`docs/research/batch-14-bmc-firmware-sources.md`（告警模型行、缺口节）、`docs/research/batch-14-error-code-mapping-sources.md`（昇腾对齐素材行、缺口节）、`sources/registry.yaml` src.huawei.atlas-800t-a2-ibmc-alarm-handling-05 notes。
- **依据**：2026-10-09 本轮重试 FetchURL（渲染提取）取得 [EDOC1100317321/4c88faf1](https://support.huawei.com/enterprise/zh/doc/EDOC1100317321/4c88faf1) 事件类告警页正文，覆盖本文所引全部 12 个事件码。逐字核对结果：0x0100000D（"[Memory board _arg1_] _arg2_ memory correctable ECC"，arg1=内存板槽位、arg2=内存丝印或 CPU 槽位号+通道号，影响「降低系统性能」）、0x56000019（"The historical ECC count of NPU Board _arg1_ NPU _arg2_ reaches the threshold"，arg1=NPU 板编号、arg2=NPU 芯片 ID，影响「可能影响NPU业务功能」）、0x0D000007（NIC PFAE 健康退化，arg1=网卡槽位号）、0x100000C3（"Failed to obtain the RTC Time on the mainboard"，影响「iBMC侧日志时间不准确」，建议重启 iBMC/更换 RTC 电池/更换主板）、0x1A000029（"iBMC time is stepped by more than _arg1_ minutes"，影响「可能导致iBMC日志记录时间混乱」）、0x1A000011（事件记录 90% 容量，影响「继续增长将会导致记录空间填满」）、0x1A00001B/0x1A00001D（操作/安全日志 90%，「可能会导致…部分历史日志丢失」，建议导出并开启远程 syslog 转储）、0x1A000025（iBMC 与 iBMA 心跳丢失，「带内管理监控信息无法获取或实时更新」，建议重装 iBMA）、0x2C00000F（"The host was restarted due to unrecognized reason"，影响「可能导致服务器业务中断」）、0x2C000063（"The host was restarted by BMC _arg1_"，arg1 例含 "due to PCIe switch or retimer upgrade"）、0x0200000F（RAID 重构停止，原文「重构停止并不表示重构结果成功，仍需检查是否有硬盘和RAID卡相关告警」）——与正文及研究记录引用一致。
- **如实记录**：该页为 JS 渲染，此前两轮直接 curl 仅取得约 386 字节页面壳；本轮经渲染提取取得正文，该检索路径的稳定性不作保证；全册未引用条目不作完整性断言。**带外—带内官方映射仍未取得、保持 unknown**（两套码不能互译），未为关闭本项编造映射。

### B14-C13（Xid 目录阈值断言）→ 已修订

- **修改位置**：`health-evidence.md`「代表性 Xid 的最小集合」节首段（约 216 行）；`docs/research/batch-14-error-code-mapping-sources.md` Guidance Classes 行（WORKFLOW_NVLINK_ERR 补第五寄存器细节）。
- **依据**：Xid Catalog **Table 3 Guidance Classes**（2026-10-09 curl 原始 HTML 逐字复核）：WORKFLOW_NVLINK_ERR「Fifth register: Bits 20, 23, 26, 29: These errors represent a threshold of ECC errors being exceeded. There was no uncorrectable error at this time. Continue operation. If desired, Field Diags can be run to check for link integrity」；WORKFLOW_XID_48「All other SRAM: check SRAM Error Threshold flag (nvidia-smi \<sram_threshold_exceeded\> or NSM Msg Type 0x3, Cmd Code 0x7D, bit 0). If set RUN_FIELDDIAG」。
- **修正要点**：「目录不将任何 Xid 直接绑定到计数器阈值」改为区分「事件标识」与「计数/阈值证据」——Xid 码本身是事件标识不是计数器读数，但个别工作流带阈值条件须按条目解码；明确不得从 Xid 140 推导计数门限，也不得否定目录的阈值分支；与正文 Xid 48 行的 SRAM 阈值描述（阈值标志读取方式）保持一致。

### B14-C14（CSV 空节规则）→ 已修订

- **修改位置**：`health-evidence.md` Empty Section 条（约 363 行）；`docs/research/batch-14-error-code-mapping-sources.md` N/A 主张行。
- **依据**：About N/A values → Empty Section 末段原文（2026-10-09 curl 逐字复核）："CSV drops the section's columns when no device in the run reports it, and fills them with N/A when only some do."
- **修正要点**：补全两种 CSV 行为及设备集合条件——本次运行所有设备均不报告该节时整组省略该节的列，仅部分设备缺失时才填 N/A；明示缺列不能解释为零值、正常状态或「已覆盖」，须先区分整节省略与单设备缺值。

### 第二轮保留的边界

- iBMC 告警页正文虽已取得并逐条核对，但取得路径（渲染提取）稳定性不作保证，文档版本仍按「文档 05（2024-08-24 快照）」引用，与用户指南 13 不可跨版本合并；带外—带内官方映射仍为 unknown。
- Xid 140/155 只按 Table 1 原文收窄解释，未新增任何处置动作；Table 3 阈值分支仅照录目录原文，不代表任何计数门限数值可得。
- 其余第一轮「仍有保留的缺口」全部继续有效（GPU Memory Error Management 仅目录结构、A3 码表仅存在性、AMD 逐 AFID 处置/阈值与 MI200 矩阵等）。
- 全部修订为文档层修订，不构成硬件验证或现场操作授权。

---

## 第三轮（第二轮定向复核后）：B14-C15、B14-C10 证据链边界标注

修订日期：2026-10-09。修订者：修订子代理（按主会话指派）。复核原文见 [batch-14-codex-recheck-round-2.md](batch-14-codex-recheck-round-2.md)（gpt-6.1-sol / xhigh，结论：B14-C01/C06/C13/C14 CLOSED，B14-C10 保持 OPEN——待独立核验，非认定代码错误；新增 B14-C15）。`make check` 结果：**PASS（77 内容条目，210 来源）**。

### B14-C15（P2，NVLink 寄存器位图遗漏 Hopper 适用性限定）→ 已修订

- **修改位置**：`knowledge/01-hardware/health-evidence.md`「代表性 Xid 的最小集合」节首段（约 216 行，第二轮新增的第五寄存器说明旁）；`docs/research/batch-14-error-code-mapping-sources.md` Guidance Classes 行（WORKFLOW_NVLINK_ERR 条，原文已含「Hopper 有效位」，本轮补全限定与禁止外推说明）。
- **依据**：[Xid Catalog Table 3 → WORKFLOW_NVLINK_ERR](https://docs.nvidia.com/deploy/xid-errors/analyzing-xid-catalog.html)（第二轮 curl 原始 HTML 已逐字取得）：位解释前明示 "The first, third, fourth and fifth registers are valid for Hopper-based products"。
- **修正要点**：在第五寄存器 bits 20/23/26/29 说明旁加入 Hopper 产品限定（第一/三/四/五寄存器位图仅适用 Hopper）；明示不得仅凭 Xid 74 的产品适用性（A100 YES）推导 A100 使用相同位图，也不推广到 Blackwell 的 WORKFLOW_NVLINK5_ERR（其解码按 Table 2 的 Subcode/Error Status 位图）。

### B14-C10（iBMC 告警原文：独立核验边界标注）→ 已按先例标注（事件码清单保留）

- **修改位置**：`knowledge/01-hardware/bmc-firmware-and-events.md`（告警模型段「取得与核对口径」、时钟偏差条 0x100000C3/0x1A000029、容量上限条 0x1A000011/01B/01D、采集失败条 0x1A000025、映射例 0x0100000D/0x56000019/0x0D000007、反例 0x2C00000F/0x2C000063/0x0200000F、已知证据缺口、verification notes）；`knowledge/01-hardware/health-evidence.md`（已知缺口 iBMC 条、verification notes）；`docs/research/batch-14-bmc-firmware-sources.md`（告警模型行、缺口节）；`docs/research/batch-14-error-code-mapping-sources.md`（昇腾对齐素材行、缺口节）；`sources/registry.yaml` src.huawei.atlas-800t-a2-ibmc-alarm-handling-05 notes（记录两轮取得方式差异与未独立核验状态）。
- **依据**：第二轮定向复核结论——独立审阅者两轮（初审定向复核与第二轮定向复核）均未能取得 EDOC1100317321/4c88faf1 原文，判定 C10 保持 OPEN 且「是独立核验未完成，不是认定作者未取得或代码错误」；处理先例为 [batch-13-codex-recheck.md](batch-13-codex-recheck.md) 对 0x80E20207/0x80E21007 xlsx 的处置（保留为编写者解析记录支持的限定归纳，不得写成独立审阅者已核验）。
- **修正要点**：在所有引用 iBMC 告警码的位置、已知缺口、metadata notes、研究记录与 registry 统一标注证据链边界——这些码的含义/影响/建议为**编写者经渲染提取取得并逐字核对的记录**，独立审阅者两轮均未取得原文、**未独立核验**；相关内容不据此单独建立处置规则（处置仍以现场确认与厂商支持为准）。**事件码清单保留未删**（与 Batch 13 先例一致）；带外—带内官方映射继续保持 unknown，未编造。

### 第三轮保留的边界

- C10 的关闭仍需要可供审阅读取的官方导出或原始页面存档（保留文档号、版本、分页身份及所引码完整消息/参数/影响/建议）；在此之前，所引华为告警码一律按「编写者核对记录、未独立核验」使用。
- C15 只补产品边界，未改动任何阈值分支的技术内容；WORKFLOW_NVLINK5_ERR 的解码仍仅指向 Table 2，不引入本文未核对的位图。
- 前两轮记录的全部保留缺口继续有效。全部修订为文档层修订，不构成硬件验证或现场操作授权。
