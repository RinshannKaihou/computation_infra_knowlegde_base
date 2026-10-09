# 第十四批来源与交付记录

**最新审阅状态（2026-10-09）：通过——限于已审阅范围并保留证据边界。** 用户约定的 `gpt-6.1-sol / xhigh` 会话完成[初审](batch-14-codex-review.md)（12 项发现：3 P1、8 P2、1 P3，结论暂不通过）、[第一轮定向复核](batch-14-codex-recheck.md)（关闭 9 项，B14-C01/C06/C10 保持 OPEN，新增 C13/C14）、[第二轮定向复核](batch-14-codex-recheck-round-2.md)（关闭 C01/C06/C13/C14，C10 待独立核验，新增 C15）与[第三轮定向复核](batch-14-codex-recheck-round-3.md)（关闭 C15；**C10 按用户认可的限定口径关闭**——所引华为告警码为编写者经渲染提取取得并逐字核对的记录，独立审阅者两轮未取得原文、未独立核验，不据此单独建立处置规则，处理方式与 Batch 13 对 0x80E20207/0x80E21007 xlsx 附件的先例一致）。累计 **B14-C01–C15 共 15 项发现全部关闭**，最终结论为「通过——限于前轮及本轮已审阅范围」。三轮修订记录见 [batch-14-review-fixes.md](batch-14-review-fixes.md)。正文仍为 draft/source_checked，未执行硬件实验；通过文档审阅不构成硬件验证或现场操作授权。

仍保留的证据边界（按[第三轮复核](batch-14-codex-recheck-round-3.md)第四节）：iBMC 告警处理 05 所列 12 个事件码未独立核验、全册不代表已覆盖、不与 iBMC 用户指南跨版本合并；带外 iBMC 告警码与带内黑匣子/健康管理码的官方映射 unknown；NVLink 寄存器位图限定 Hopper、事件标识不是计数器读数；A3 黑匣子附件仅存在性核对；GB200 管理面证据仅覆盖计算托架范围；AMD 逐 AFID 处置/阈值、MI200 字段矩阵、部分 OEM 维修条款、结果级基准证据与华为保修介质保留条款未取得；无真实设备操作、时钟偏差数值、完整跨层时间线或恢复验证。

集成日期：2026-10-09。本批为 full-coverage 路线图 Batch 14（full-coverage-backlog 的 T01-05/T01-06/T01-07/T01-08），由 Kimi（主会话）组织，四路探索子代理完成取证、修订子代理完成三轮审阅发现修订。全部保持 draft；两篇新正文与两篇修订均为限定来源范围的 source_checked，无 reproduced。

## 本批正文

| 任务 | 正文 | 类型 | 备注 |
|---|---|---|---|
| T01-05 | [计算节点资源与拓扑参考](../../knowledge/01-hardware/resource-topology.md) | reference | 修订（板卡到超节点的组成与拓扑约束扩展） |
| T01-06 | [BMC、固件身份与跨层硬件事件](../../knowledge/01-hardware/bmc-firmware-and-events.md) | reference | 新增 |
| T01-07 | [设备健康证据与检测边界](../../knowledge/01-hardware/health-evidence.md) | reference | 修订（三平台错误信息与健康覆盖映射） |
| T01-08 | [节点选型、隔离返修、长期管理与退役](../../knowledge/01-hardware/node-selection-and-lifecycle.md) | procedure | 新增 |

来源记录：[超节点组成](batch-14-supernode-composition-sources.md)、[BMC 与固件](batch-14-bmc-firmware-sources.md)、[错误码映射](batch-14-error-code-mapping-sources.md)、[节点生命周期](batch-14-node-lifecycle-sources.md)。任务清单：[plans/full-coverage-backlog.yaml](../../plans/full-coverage-backlog.yaml)。

## 来源变化

新增 40 项登记（总计 123→163；84→123 为 Batch 13），按取证组分布：

- **超节点组成（T01-05，10 项）**：src.nvidia.gb200-nvl72-product-page-2026-10-09、src.huawei.atlas-900-a3-superpod-product-2026-10-09、src.huawei.atlas-900-a3-superpod-user-guide-13-2026-06-25、src.huawei.atlas-900-a3-superpod-maintenance-guide-14-2026-08-18、src.huawei.lingqu-630-v1-user-guide-03-2026-01-30、src.huawei.atlas-900-a3-superpod-brochure-26h1、src.supermicro.as-8125gs-tnmr2-manual-mnl-2671-r1.0b、src.supermicro.as-8125gs-tnmr2-datasheet-2024、src.amd.instinct-mi300x-platform-datasheet-2023、src.ocp.oai-wiki-2026-10-09。
- **BMC/固件（T01-06，8 项）**：src.dmtf.redfish-registries-2026.2、src.nvidia.dgx-h100-h200-fw-update-guide-2026-09-13、src.huawei.atlas-800t-a2-ibmc-user-guide-2026-09-11、src.huawei.atlas-800t-a2-ibmc-alarm-handling-05、src.huawei.ibmc-redfish-interface-ref-23-2025-08-20、src.supermicro.redfish-user-guide-rev6.1-2026-04-03、src.supermicro.bmc-x13-h13-b13-manual-rev1.0b-2024-12-13、src.supermicro.as-8125gs-tnmr2-product-2026-10-09。
- **错误码（T01-07，10 项）**：src.nvidia.xid-errors-docs-2026-09-09、src.nvidia.gpu-mem-error-mgmt-2026-09-09、src.nvidia.dgx-gb200nvl72-2-release-notes-2026-10-07、src.huawei.hdk-26.1x-a2-blackbox-errorcode-02-2026-10-09、src.huawei.hdk-26.1x-a3-blackbox-errorcode-02-2026-10-09、src.huawei.hdk-26.1x-a2-dcmi-returncode-2026-10-09、src.amd.amd-smi-docs-10.1.0、src.amd.afid-event-list-70122-v1.0、src.kernel.amdgpu-ras-v6.16、src.ocp.gpu-accelerator-ras-requirements-v1.0。
- **生命周期（T01-08，12 项）**：src.nvidia.dgx-h100-h200-service-manual-2026-10-09、src.nvidia.rma-process-deploy-latest-2026-10-09、src.nvidia.dgx-os-7-user-guide-reimaging-2026-10-09、src.nvidia.nvsm-user-guide-25.03、src.nvidia.dgx-superpod-deployment-guide-v16-2024-12-11、src.nist.sp-800-88r2-2025-09、src.supermicro.sys-821ge-tnhr-manual-mnl-2596-1.0c、src.supermicro.as-2124gq-nart-manual-mnl-2356-1.0a、src.dell.system-erase-idrac9-poweredge-2020、src.dell.kb-000186133-data-wipe-2026-10-09、src.huawei.atlas-800t-a2-maintenance-guide-26-2026-10-09、src.mlcommons.mlperf-training-results-v6.0-2026-10-09。

排除 3 条取证不足未登记：`atlas-800t-a2-upgrade-guide-07`（仅核对单页搜索快照与片段，登记前应复核目录页）、`openbmc.docs-repo`（未逐篇核对、许可未查）、`enterprise-warranty-overview`（页面为 JS 壳、PDF 附件未下载成功，介质保留/故障件保留条款仅搜索片段级证据）。待补取后按需登记。

复用/扩充既有登记（不计数）：src.dmtf.redfish-schemas-v1-2026.2（补核 Event/EventService/EventDestination/MessageRegistry/SoftwareInventory/UpdateService/LogEntry/Manager 等 schema）、src.nvidia.dgx-h100-h200-user-guide-2026-01-26（补核 bmc 与 redfish-api-supp 章节）、src.nvidia.dgx-gb200-user-guide-2026-09-17（补核计算托架 Redfish 命令页）、src.nvidia.gpu-node-triage-2026-10-08（B14-C11 链接复核：旧路径 404、登记 URL 200）、src.nvidia.dcgm-diag-user-guide-latest-2026-10-08（退出码复核）、src.huawei.atlas-800t-a2-user-guide-26-2026-10-08 与 Batch 13 的 HDK 26.1.x npu-smi/健康管理故障定义等。

## 修订后的重点边界（2026-10-09）

- **Xid 表**：按 2026-09-09 官方目录（HTML Table 1–3 + Xid-Catalog.xlsx 逐行解析交叉）整表重建；四列 YES/NO 为 A100/H100/B100/GB200 **产品适用性列、非归因列**（旧版 HW/Driver Error 归因列结构已废弃）；144–150 为 NVLink 5 事件族、按 Table 2 Subcode 位图解码；Table 3 第五寄存器阈值位（bits 20/23/26/29）及一/三/四/五寄存器位图**限定 Hopper**，不外推 A100/Blackwell；140 删除数量因果解释（错误以某种方式中断驱动页离线/行重映射标记能力）、155 仅陈述 intentional 标记并保留非预期时 INVESTIGATE_SW_USER 分支；区分「事件标识」与「计数/阈值证据」——目录含阈值分支（WORKFLOW_NVLINK_ERR/WORKFLOW_XID_48），但不得由 Xid 140 推导计数门限。
- **DCGM 退出码**：恢复符号与原始含义——226=`DCGM_ST_NVVS_ERROR`（诊断执行完成但报告错误，不得单独推出节点重启）、205=`DCGM_ST_NVVS_ISOLATE_ERROR`（需要隔离）、237=`DCGM_ST_RESET_REQUIRED`（GPU 需要复位）；动作列只写有精确上游依据的分诊分支。
- **AMD**：reset **三重影响范围**分列——XGMI hive 全体 GPU、共享上游 PCIe switch 的 Secondary Bus Reset（不受 hive 边界限制）、持有 `/dev/kfd` 句柄的进程可能被终止（即使未使用被复位的 GPU）；AFID 19=坏页退休门限（Fatal）/22=片内 ECC 不可纠正非致命修正，Device Internal 与 Unidentified 分类对齐 Table 1，不从码值推导未公开门限；`monitor -e` 为计数采样非事件流、`-V/--violation` 与 `-v/--vram-usage` 大小写区分、持续采样须含 `--watch`；N/A 三分（Not Applicable/Not Available/Empty Section）语义分层——Not Available 本身记数据不可用不赋失败类别，CSV 全设备缺报时整组省略列、仅部分缺失才填 N/A，原因不明记 unknown。
- **Redfish**：区分「日志溢出计数」（`LogEntry.OverflowErrorCount`，v1_14_0 起、只读、条件性出现）与「覆盖端到端投递丢失/重复的通用计数器」（规范无）；字段缺失≠零丢失；本批设备实现 unknown。
- **DGX 重镜像**：两安装分支分列——默认分支重分区并重格式化 OS 与数据盘、显式 Without Reformatting Data RAID 分支保留数据盘；删除「默认不覆盖数据盘」「只覆盖 OS 盘」与「接近 Clear 级覆写」表述；重镜像与介质 sanitization 分开，无技术与验证证据不赋予 Clear/Purge 等级（NIST SP 800-88 Rev.2）。
- **退役凭据关闭门槛**：新增独立凭据处置关闭项——BMC 账户、证书、管理面权限（远程管理入口、API 令牌、许可证绑定）逐项清单 + 处置方式 + 责任人 + 证据；未解决项阻止正常关闭，或进入明确授权、可审计、有期限/复审点的残余风险接受流程。
- **iBMC 告警码限定口径**：统一「部分取得」——所引 12 个事件码为编写者经渲染提取取得并逐字核对的记录，独立审阅者两轮未取得原文、**未独立核验**，不据此单独建立处置规则；告警处理 05（文档 05，2024-08-24 快照）与 iBMC 用户指南 13 不跨版本合并；带外—带内官方映射 unknown，两套码不能互译。
- **MLPerf**：改称跨版本基准索引，逐基准保留 Latest Version Available（DeepSeek v3/GPT-OSS 20B/Llama3.1 等为 v6.0，RetinaNet 为 v5.1 等）；v6.0 专属套件清单未另取，结果比较须同版本同规则。
- 组成与生命周期边界：E1.S 数量（NVIDIA 4×/HPE 8×/Supermicro up to 8）、昇腾算力档位（307.2/288.7/240.3 PFLOPS@FP16）、「物理 384 与实际部署」等冲突口径按来源分列保留；AMD 无超节点样板、BMC 证据全部来自 OEM。全部正文未执行真实环境验证。

## 集成时检查

各轮审阅/修订时点的结构检查（照录自审阅与修订记录）：初审与第一轮修订记录 `make check` / `make build` **PASS（75 content entries / 163 sources，Batch 14 单批时点口径）**；第二、三轮定向复核 `make check` **PASS（77 content entries / 210 sources）**。77/210 为当前全仓库统计——Batch 15 与本批并行交付，该数字不全是 Batch 14 的产物；本批单批时点为 75/163。本批收尾集成（本文与 plans/docs 状态更新）后主执行者运行 `PYTHONDONTWRITEBYTECODE=1 make check`：**PASS（77 content entries / 210 sources）**，未运行 `make build`（本次仅改 plans 与 docs，不影响 catalog）。结构检查只证明结构与本地引用，不代表技术正确性或远程内容有效性。
