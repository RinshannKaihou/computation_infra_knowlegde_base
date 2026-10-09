---
id: hardware.bmc-firmware-and-events
title: BMC、固件身份与跨层硬件事件
type: reference
domain: hardware
status: draft
platforms: [generic, nvidia, ascend, amd]
source_refs:
  - src.dmtf.redfish-schemas-v1-2026.2
  - src.dmtf.redfish-registries-2026.2
  - src.nvidia.dgx-h100-h200-user-guide-2026-01-26
  - src.nvidia.dgx-h100-h200-fw-update-guide-2026-09-13
  - src.nvidia.dgx-gb200-user-guide-2026-09-17
  - src.huawei.atlas-800t-a2-ibmc-user-guide-2026-09-11
  - src.huawei.atlas-800t-a2-ibmc-alarm-handling-05
  - src.huawei.ibmc-redfish-interface-ref-23-2025-08-20
  - src.supermicro.redfish-user-guide-rev6.1-2026-04-03
  - src.supermicro.bmc-x13-h13-b13-manual-rev1.0b-2024-12-13
  - src.supermicro.as-8125gs-tnmr2-product-2026-10-09
updated_at: "2026-10-09"
summary: 以 DMTF Redfish 为通用角色模型，分列 NVIDIA DGX、华为 iBMC 与 Supermicro BMC（AMD 机型 OEM 支路）的固件身份清单、更新边界与事件证据记录方法；规范资源不等于设备实现，单一事件不可直接归因。
related_ids:
  - hardware.resource-topology
  - hardware.health-evidence
  - hardware.rack-power-cooling-and-failure-domains
  - reliability.dimensions-and-failure-domains
verification:
  status: source_checked
  evidence_refs:
    - src.dmtf.redfish-schemas-v1-2026.2
    - src.dmtf.redfish-registries-2026.2
    - src.nvidia.dgx-h100-h200-user-guide-2026-01-26
    - src.nvidia.dgx-h100-h200-fw-update-guide-2026-09-13
    - src.nvidia.dgx-gb200-user-guide-2026-09-17
    - src.huawei.atlas-800t-a2-ibmc-user-guide-2026-09-11
    - src.huawei.atlas-800t-a2-ibmc-alarm-handling-05
    - src.huawei.ibmc-redfish-interface-ref-23-2025-08-20
    - src.supermicro.redfish-user-guide-rev6.1-2026-04-03
    - src.supermicro.bmc-x13-h13-b13-manual-rev1.0b-2024-12-13
    - src.supermicro.as-8125gs-tnmr2-product-2026-10-09
  notes: "核对 DMTF Redfish schema 与消息注册表单文件 JSON（2026.2/2026.1 release，含 LogEntry.v1_22_0 的 OverflowErrorCount 字段复核）、NVIDIA DGX H100/H200 用户指南与固件更新指南页面、DGX GB200 用户指南计算托架 Redfish 章节、华为 Atlas 800T A2 iBMC 用户指南与告警处理 05（告警处理 05：第一轮按独立审阅 B14-C10 统一为部分取得口径；第二轮 2026-10-09 定向复核时经渲染提取取得事件类告警页原文，本文所列事件码条目逐字核对含义/说明/影响/建议一致——该页为 JS 渲染，此前两轮直接 curl 仅得页面壳，检索路径稳定性不作保证，全册未引用条目不作完整性断言；取得与核对明细以 docs/research/batch-14-bmc-firmware-sources.md 为准；iBMC 告警码与带内黑匣子/健康管理码的官方映射关系仍未取得；独立审阅者两轮（2026-10-09 初审定向复核与第二轮定向复核）均未取得该页原文，所引事件码为编写者核对记录、未独立核验，不据此单独建立处置规则）及 iBMC Redfish 接口参考 23 页面、Supermicro X13/H13/B13 BMC 手册（pdftotext 全文）与 Redfish 指南 rev 6.1 及 AS-8125GS-TNMR2 产品页。未在任何真实设备上执行查询、订阅或固件更新操作；所有 API 路径、事件码与版本约束仅为文档核对结果，不构成目标环境的支持证明。"
---

# BMC、固件身份与跨层硬件事件

## 范围与阅读方式

本文回答三个相互关联的问题：带外管理控制器（BMC）在证据链中扮演什么角色、如何记录一套机器的固件身份、如何记录和对齐 BMC 产生的硬件事件。三者关系是：BMC 是带外证据的**采集与转发方**，固件身份决定了事件语义和更新行为适用的**版本边界**，事件记录方法决定了 BMC 证据能否与驱动、作业层时间线**对齐**。

通用角色模型取自 DMTF Redfish 标准（DSP8011《Redfish Standard Registries Bundle》2026.2 与配套 DSP2065《Redfish Message Registry Guide》2026.2，版本表见 [DSP8011](https://www.dmtf.org/dsp/DSP8011)、[DSP2065](https://www.dmtf.org/dsp/DSP2065)，2026-10-09 核对）。随后给出三个独立实例：NVIDIA DGX H100/H200 与 DGX GB200、华为 Atlas 800T A2 的 iBMC、以及承载 AMD Instinct MI300X 的 Supermicro 机型（OEM BMC 支路）。

两条贯穿性约束：

- **规范不等于实现。** schema 存在不代表某台设备实现了该资源或字段。实例：DGX H100/H200 用户指南自述「The Redfish server follows the DSP0266 1.7.0 Specification and Redfish Schema 2019.1 documentation」（[redfish-api-supp.html](https://docs.nvidia.com/dgx/dgxh100-user-guide/redfish-api-supp.html)，2026-01-26 更新），其实现基线远旧于 DMTF 当前 2026.2；本文引用的较新字段（如 `OriginOfConditionUnavailable` v1_12_0、`VendorCode` v1_14_0）不能假设该机支持。
- **AMD 不假设设备原生支持。** MI300X 设备本身不宣称带外管理能力；其管理面证据全部来自 OEM（Supermicro）BMC，OEM 文档行为不代表 AMD 官方行为。

## Redfish 通用角色模型

### 事件与消息

事件载荷模型由 Event 资源定义（[Event.v1_14_0.json](https://redfish.dmtf.org/schemas/v1/Event.v1_14_0.json)，release 2026.2）：一个事件含 `Events[]`（EventRecord 数组，一次推送可含多条），每条 EventRecord 的关键字段与语义：

| 字段 | 语义与边界 |
|---|---|
| `EventId` / `MemberId` | 实例标识；`EventType`、`MessageId`、`MemberId` 为必填 |
| `EventTimestamp` | 仅要求「consistent with the Redfish service time」，不保证与 host OS 时钟一致 |
| `EventType` | 自 v1_3_0 起废弃（订阅改按 RegistryPrefix/ResourceType 过滤）；旧实现仍可能只按它分类 |
| `Severity` / `MessageSeverity` | `Severity` 自 v1_5_0 起废弃，改用 `MessageSeverity` |
| `MessageId` / `Message` / `MessageArgs` | `MessageId` 指向消息注册表条目；`MessageArgs` 填充 `%1..` 占位参数 |
| `OriginOfCondition` | 指向产生事件的资源链接；`OriginOfConditionUnavailable`（v1_12_0）为 true 表示源链接不可得 |
| `EventGroupId` | 关联同根因的多条事件；值为 0 表示不分组，且规范明示「This property value shall not imply an ordering of events」——**分组不蕴含时间顺序** |
| `VendorCode`（v1_14_0） | 「contain a vendor-defined code or identifier equivalent to this event or MessageId value」，用于映射厂商遗留错误码 |
| `LogEntry` 链接（v1_7_0）、`Resolution` / `ResolutionSteps` | 事件到日志条目的落点、修复指引 |

事件服务与订阅由 EventService（[EventService.v1_12_0.json](https://redfish.dmtf.org/schemas/v1/EventService.v1_12_0.json)）与 EventDestination（[EventDestination.v1_17_1.json](https://redfish.dmtf.org/schemas/v1/EventDestination.v1_17_1.json)）定义：EventService 含 `ServerSentEventUri`（SSE）、`Subscriptions`、`DeliveryRetryAttempts`/`DeliveryRetryIntervalSeconds`、`RegistryPrefixes`/`ResourceTypes`/`Severities` 过滤与 `SubmitTestEvent` 动作；订阅的 `SubscriptionType` 枚举为 `[RedfishEvent, SSE, SNMPTrap, SNMPInform, Syslog, OEM]`，`DeliveryRetryPolicy` 枚举为 `[TerminateAfterRetries, SuspendRetries, RetryForever, RetryForeverWithBackoff]`，`Context` 随订阅生命周期保留。重试策略是订阅级声明，不证明送达。

消息注册表结构见 MessageRegistry（[MessageRegistry.v1_9_0.json](https://redfish.dmtf.org/schemas/v1/MessageRegistry.v1_9_0.json)）：每条 Message 含 `Message`（`%1..` 参数占位）、`Description`、`Severity`、`MessageSeverity`、`NumberOfArgs`、`ParamTypes`、`Resolution`、`ClearingLogic`（`ClearsIf=SameOriginOfCondition`、`ClearsMessage[]`）、`Deprecated`/`ReplacedBy` 等。清除语义原文为「Clearing in this context deasserts the event rather than removes the event from a log」——清除是解除断言，不是从日志删除。服务可以覆盖注册表中的 Severity。

DMTF 公开注册表目录（[redfish.dmtf.org/registries/](https://redfish.dmtf.org/registries/)）当前版本包括 Base.1.23.0、ResourceEvent.1.5.0、Platform.1.4.0（含 `MemoryUncorrectableError`、`PCIeLinkDown`、`PCIeIncorrectLinkSpeed/Width`、`PowerBrake` 等）、StorageDevice.1.6.0、SensorEvent.1.2.0、Update.1.4.0（25 条固件更新生命周期消息）等（各文件 Release 均为 2026.1，2026-10-09 核对）。注意目录内**没有名为 "Event" 的注册表**，事件类消息分布在 ResourceEvent/Platform/SensorEvent 等注册表中。

日志侧模型见 LogEntry（[LogEntry.v1_22_0.json](https://redfish.dmtf.org/schemas/v1/LogEntry.v1_22_0.json)）：`EntryType` 枚举 `[Event, SEL, Oem, CXL]`（IPMI SEL 条目记为 `SEL`），字段含 `Created`、`Severity`、`MessageId`、`SensorNumber`（仅 SEL）、`Resolved`、`CPER`、`EventGroupId`、`Links.OriginOfCondition`。管理器模型见 Manager（[Manager.v1_25_0.json](https://redfish.dmtf.org/schemas/v1/Manager.v1_25_0.json)）：`ManagerType` 枚举含 `BMC`、`RackManager`、`EnclosureManager` 等；时钟字段 `DateTime`（含 UTC offset）、`DateTimeLocalOffset`、`TimeZoneName`；身份字段 `FirmwareVersion`、`Manufacturer`、`Model`、`PartNumber`、`SerialNumber`、`UUID`。时钟字段只是可读写属性，不声明与 host 的同步关系。

### 固件身份与更新

Redfish **没有独立的 FirmwareInventory schema**：固件清单是 UpdateService 下的 SoftwareInventory 集合（`/redfish/v1/UpdateService/FirmwareInventory`，类型为 `#SoftwareInventoryCollection.SoftwareInventoryCollection`）。SoftwareInventory 字段（[SoftwareInventory.v1_15_0.json](https://redfish.dmtf.org/schemas/v1/SoftwareInventory.v1_15_0.json)）含 `Version`、`AdditionalVersions`、`LowestSupportedVersion`、`SoftwareId`、`Updateable`（false 表示「for reporting purposes only」）、`WriteProtected`、`Manufacturer`、`ReleaseDate`、`VersionScheme`、`RelatedItem`（链接到该固件适用的设备资源）、`Active`/`Staged`（v1_12_0）、`Status`。清单覆盖范围取决于实现，规范不要求列出全部固件。

UpdateService（[UpdateService.v1_17_1.json](https://redfish.dmtf.org/schemas/v1/UpdateService.v1_17_1.json)）含 FirmwareInventory 与 SoftwareInventory 两个集合、`HttpPushUri`/`MultipartHttpPushUri`、`MaxImageSizeBytes`、`SupportedUpdateImageFormats`。`ForceUpdate` 语义原文：「bypass update policies when applying the HttpPushUri-provided image, such as allowing a component to be downgraded. Services may contain update policies that are never bypassed, such as minimum version enforcement.」——即「可降级」与否属实现策略，规范不统一规定回退禁区。更新生命周期消息集 Update.1.4.0（[Update.1.4.0.json](https://redfish.dmtf.org/registries/Update.1.4.0.json)）含 `TargetDetermined`、`TransferringToComponent`/`TransferFailed`、`VerifyingAtComponent`/`VerificationFailed`、`ApplyingOnComponent`/`ApplyFailed`、`AwaitToActivate`、`ActivatingOnComponent`/`ActivateFailed`、`UpdateSuccessful`、`UpdateFailed`、`UpdateSkippedSameVersion`、`UpdateSkippedVersionTooLow` 等；这些只是消息定义，实际更新结果仍以更新后 FirmwareInventory 的版本复核为准。

## NVIDIA 实例：DGX H100/H200 与 DGX GB200

### DGX H100/H200

BMC 能力面（[DGX H100/H200 用户指南 bmc.html](https://docs.nvidia.com/dgx/dgxh100-user-guide/bmc.html)，2026-01-26 更新）：Web UI 主导航含 Sensor（SSD、PSU、电压、CPU/DIMM 温度、风扇转速）、System Inventory、FRU Information、GPU Information（每 GPU 的 GUID、VBIOS version、InfoROM version、retired pages 数——GPU 固件版本在该文档中仅此一处展示路径）、Logs and Reports（IPMI event log 及 System/Audit/Video/POST Code logs，可查看/下载/擦除）、Maintenance（固件更新、配置备份/恢复/出厂重置）。开放端口含 443（Redfish https with auth）、623（RMCP+ IPMI）、123（NTP）等；NTP 端口开放不等于已配置时钟源。

Redfish 基线与固件清单（[redfish-api-supp.html](https://docs.nvidia.com/dgx/dgxh100-user-guide/redfish-api-supp.html)）：实现基线为 DSP0266 1.7.0 + Schema 2019.1（见上节版本差约束）；支持事件日志读取、Logging Service、Event Services（SSE）与固件更新。`GET /redfish/v1/UpdateService/FirmwareInventory` 文档示例返回 66 个成员（`Oem.Ami` 扩展列版本，例 `CPLDMB_0=0.2.1.6`）。可更新目标清单：`HostBMC_0`（BMC）、`HostBIOS_0`（BIOS）、`EROT_BMC_0`/`EROT_BIOS_0`（外部信任根）、`CPLDMID_0`（中板 CPLD）、`CPLDMB_0`（CPU 托架 CPLD）、`PSU_0..PSU_5`、`PCIeSwitch_0/1`、`PCIeRetimer_0/1`；GPU 托架整组以 `HGX_0` 为唯一目标。清单示例为文档快照，66 为示例时刻计数。

更新策略与双分区：默认「only updated if the incoming firmware version is newer than the existing version」，设 `ForceUpdate: true` 覆盖（PATCH 成功返回 204，重复设置同值返回 400）。固件启动后用 background copy 同步双分区镜像：`POST /redfish/v1/UpdateService/Actions/Oem/NvidiaUpdateService.CommitImage`（Targets 如 `HostBIOS_0`/`HostBMC_0`）——这是 OEM 扩展动作，非 DMTF 标准动作；激活动作返回 MessageId `UpdateService.1.0.StartActivateFirmware` 并建立 Task。

SEL 读取与丢失风险配置点：`GET /redfish/v1/Managers/BMC/LogServices/SEL/Entries` 每次返回 75 条，用 `Members@odata.nextLink`（如 `?$skip=75`）翻页。BIOS 属性可配置 SEL 满时行为（PATCH `/redfish/v1/Systems/DGX/Bios/SD`，Attributes 如 `{"IPMI002":"IPMI002DoNothing", "IPMI201":"IPMI201Donotloganymore"}`），且 BIOS 属性变更需 power cycle 生效——SEL 满后「不再记录」是官方配置项，采集方必须记录该配置状态。

更新依赖与激活分工（[DGX H100/H200 Firmware Update Guide](https://docs.nvidia.com/dgx/dgxh100-fw-update-guide/)，2026-09-13 更新，版本页至 26.07.5）：更新前停止一切 GPU 活动（含运行 `nvidia-smi`，否则可致 VBIOS 更新失败），高负载可致组件不可用；从 1.0.0/1.1.1 直升 24.09.1 必须先升 1.1.3，否则需 factory reset（阶梯升级约束为版本相关表述，后续版本可能变化）。激活分工：BMC 经 `ipmitool mc reset cold`；BIOS 与 HGX（GPU 托架）经 `ipmitool chassis power cycle`；PCIe Switch/Retimer/EROT/CPLD 需 AC 断电重启（「will activate firmware for all updated components」）。整流程约 90 分钟（两个托架）+ 约 30 分钟（CX-7）。GPU 托架更新后须确认 `"BackgroundCopyStatus": "Completed"`（`GET /redfish/v1/Chassis/HGX_ERoT_BMC_0`）再 cold reset；TPM 与 NVMe 盘带外固件更新要求最低 BMC 25.12.11 + SBIOS 1.7.8，更新后到 OS 检查 BMC SEL 成功事件并核对版本。

### DGX GB200（仅计算托架）

计算托架 BMC 运行 OpenBMC 栈（文档示例默认凭据 root/openBmc），见 [DGX GB200 用户指南 compute-tray-redfish-commands.html](https://docs.nvidia.com/dgx/dgxgb200-user-guide/compute-tray-redfish-commands.html)（2026-09-17 更新）。管理器分两级：`/redfish/v1/Managers/BMC_0`（托架 BMC）与 `/redfish/v1/Managers/HGX_BMC_0`（HMC）；另有 `Chassis/ERoT_BMC_0`、`HGX_ERoT_BMC_0` 信任根资源。固件管理：bundle 上传 `POST /redfish/v1/UpdateService/update-multipart`（UpdateParameters 含 Targets 与 `"ForceUpdate":true`）；版本清点 `GET /redfish/v1/UpdateService/FirmwareInventory?expand=.$levels=1` 列 `[Id, Version]`；镜像签名类型经 ERoT 资源查询（`/redfish/v1/Chassis/ERoT_BMC_0/Oem/NvidiaRoT/RoTProtectedComponents/BMC_0/Images/<slot>` 的 `SigningType`，多镜像槽位的回退语义文档未说明）；全局硬件写保护经 PATCH `/redfish/v1/Chassis/Chassis_0` 的 `Oem.Nvidia.HardwareWriteProtectEnable`，官方建议更新固件后启用。事件与日志：清日志 `POST .../LogServices/EventLog/Actions/LogService.ClearLog`（BMC 与 HMC 各有路径）；BMC/HMC 恢复出厂（`Manager.ResetToDefaults` ResetAll）后默认账号 admin/admin 并强制首登改密；eMMC（含 journal）可 SecureErase；`nvdebug --collect`（NVDEBUG）打包 BMC event logs、firmware versions、hardware inventory、system health data 供支持分析。带外接口面：IPMI 可经 NetworkProtocol PATCH 关闭（官方建议安全加固时关闭；关闭后的回退路径未说明）；SOL 经 `ipmitool -C 17 -I lanplus sol activate` 或 `ssh -p 2200`。NVLink 交换托架与机柜级管理面本轮未取证，保持 unknown。

## Ascend 实例：Atlas 800T A2 iBMC

iBMC 支持标准 Redfish 接口：「iBMC支持标准的Redfish接口…通过GET、PUT、PATCH、POST、DELETE等命令对服务器进行查询、配置、监控」（[iBMC 用户指南 · Redfish接口](https://support.huawei.com/enterprise/zh/doc/EDOC1100317056/611e8ddf)，文档 13），但该页未给出支持的 schema 版本号。接口细节见 [iBMC Redfish 接口参考 23](https://support.huawei.com/enterprise/zh/doc/EDOC1000126991/14033122)（2025-08-20 发布）——这是**跨机型文档**，个别接口标注「仅Atlas 800T A2和Atlas 200T A2 Box16支持」类注记，逐接口适用性须按页面标注核对，不能整册套用。其中 `/redfish/v1/UpdateService/FirmwareInventory` 集合与 `/FirmwareInventory/{softid}` 的属性表含 Id、Name、Status、Version、Updateable、SoftwareId、RelatedItem、Oem。

固件升级（[iBMC 用户指南 · 固件升级](https://support.huawei.cn/enterprise/zh/doc/EDOC1100317056/9d7b49ce)，该页出自文档 09 快照，文档族最新为 13）：iBMC 自身固件为**三分区镜像**——主用分区（当前生效）、备用分区（主用异常时自动切换并保持版本一致，升级时主备同升）、可用分区（储备版本，可经「可用分区镜像倒换」生效，倒换后主备同步、原备用转为可用）；可用分区与主用版本不一致时倒换「可能会对服务器上运行的业务产生影响」。该三分区机制描述的是 iBMC 自身固件，不等于所有部件都有主备。升级约束（官方注意事项）：升级过程不允许断电、不允许重启 iBMC；升级 iBMC 固件需重启 iBMC 生效，「但您不需要重启操作系统。因此，服务器上运行的业务不会受到影响」；升级电源固件无需重启服务器；OS 上电状态升 BIOS 时 BIOS 在下电再上电或重启后生效、CPLD 在下电后生效；OS 下电状态升 BIOS/CPLD 则上电后生效；OS 启动过程中不要重启 iBMC、镜像倒换或升级。生效条件按部件类别不同，不可合并表述。升级通道分带内/带外：带外通道文件 `.hpm`（≤90MB）；带内通道（经 Smart Provisioning）文件 `.zip`（≤499MB）+ 签名文件 `.asc`(pgp)/`.p7s`(cms)，「适用于支持通过SP升级的固件（例如网卡、RAID卡和硬盘固件）」；iBMC V2 3.05.00.00 及以上支持带内带外通道升级。用户指南固件范围（[使系统保持最新状态](https://support.huawei.com/enterprise/zh/doc/EDOC1100317202/c4fd778c)）：经 iBMC WebUI 可升级硬盘背板、主板 CPLD、硬盘背板 CPLD 和 Riser 卡 CPLD 等；驱动版本须与版本配套表一致。NPU 固件（HiLink、MCU 等）的升级步骤在《Atlas 800T A2 升级指导书》中，该文档本轮未复核，本文不引用其内容。

告警模型（[iBMC 告警处理 05 · 事件类告警](https://support.huawei.com/enterprise/zh/doc/EDOC1100317321/4c88faf1)，文档 05，2024-08-24 快照）：告警以**十六进制事件码 + 参数化消息**（`_arg1_`..）表示，按部件分段编号（0x00 CPU、0x01 内存、0x02 硬盘、0x03 PSU、0x04 风扇、0x08 PCIe 卡、0x0D NIC、0x1A iBMC 自身、0x2C 系统、0x40 xPU 板、0x56 NPU 等），每条含影响与建议。文档 05 与 iBMC 用户指南 13 版本不齐，告警码可能随版本增减，引用时必须带文档版本。**取得与核对口径**：本文引用的告警条目（0x0100000D、0x56000019、0x0D000007、0x100000C3、0x1A000029、0x1A000011、0x1A00001B、0x1A00001D、0x1A000025、0x2C00000F、0x2C000063、0x0200000F）于 2026-10-09 第二轮定向复核时取得事件类告警页原文并逐字核对（含义、说明、影响与建议与本文引用一致，核对明细见 [batch-14-bmc-firmware-sources.md](../../docs/research/batch-14-bmc-firmware-sources.md)）；该页为 JS 渲染，此前两轮直接 curl 仅取得页面壳，本轮经渲染提取取得正文，该检索路径的稳定性不作保证，全册中本文未引用的条目不作完整性断言。**证据链边界（按独立审阅第二轮结论如实标注）**：上述事件码的含义、影响与建议是**编写者经渲染提取取得并逐字核对的记录**；独立审阅者（gpt-6.1-sol / xhigh）两轮（2026-10-09 初审定向复核与第二轮定向复核）均未能取得该页原文，**未做独立核验**——本文引用这些码仅作机制性记录，不据此单独建立处置规则（处置仍以现场确认与厂商支持为准），与 Batch 13 对 0x80E20207/0x80E21007 xlsx 的处理先例一致。另注意「告警条目取得情况」与「带外—带内官方映射取得情况」是两件事：iBMC 告警码与带内黑匣子/健康管理码之间的官方对应关系仍未取得、保持 unknown（见[设备健康证据与检测边界](health-evidence.md)已知缺口）。

日志落盘与一键收集（[iBMC 用户指南 · 一键收集信息说明](https://support.huawei.com/enterprise/zh/doc/EDOC1100317056/f40a8c00)，2026-09-11 更新）：`ipmcget -d diaginfo` 生成 `/tmp/dump_info.tar.gz`，清单含 `sensor_alarm/current_event.txt`（当前健康状态与告警事件）、`cache_event_log.db`（**未上报的订阅事件数据库文件**）、`sel.db`、`sel.tar`（当前+历史 SEL 打包）、`sensor_alarm_sel.bin`（SEL 原始记录）及 .bak 与 md5/sha256 校验、`fdm.bin`/`fdm_log`/`fdm_output`/`fdm_pfae_log`（FDM 故障诊断与预告警）、`ntp_info.txt`（NTP 同步失败时的错误信息）、`time_zone.txt`、`npu_info`、`npu_ecc_info.json`、`upgrade_info`（iBMC 相关器件版本）、`kbox_info`、`ps_black_box.log`（电源黑匣子）、`systemcom.tar`（SOL 串口信息）。`cache_event_log.db` 的证据意义：订阅事件存在本地未上报缓存——**订阅通道中断不等于事件丢失**，导出前不可假定订阅端已收到全部事件。

## AMD/OEM 实例：Supermicro BMC（MI300X 机型）

选型机型为 Supermicro AS-8125GS-TNMR2（[产品页](https://www.supermicro.com/en/products/system/gpu/8u/as-8125gs-tnmr2)，2026-10-09 观察）：8U、双路 EPYC 9004/9005、8× 板载 AMD Instinct MI300X（OAM，Infinity Fabric 互连）；System BIOS 为 AMI 32MB SPI Flash；安全特性含 TPM 2.0、Silicon Root of Trust（NIST 800-193）、Cryptographically Signed Firmware、Secure Firmware Updates、Automatic Firmware Recovery、Runtime BMC Protections。MI300X 设备本身不宣称带外管理能力，管理面全部来自 OEM BMC；以下 Supermicro 证据**不代表 AMD 官方行为**。

BMC 事件日志与容量（[BMC User's Manual X13/H13/B13](https://www.supermicro.com/manuals/other/BMC_IPMI_X13_H13_B13.pdf)，AST2600，Revision 1.0b，2024-12-13，§2.5.2/§2.8）：Health Event Log 上限 **4096 条**（Maintenance Event Log 亦 4096 条）；支持启用/停用 AC Power On Event Log 与 FIFO Event Log（默认启用）；条目列 Severity（绿=info/解除、黄=warning、红=critical）、Date/Time、Sensor、Description、Event Type（Sensor-Specific/Threshold/Generic/OEM/Unspecified），可导出 Excel。4096 条满后的行为取决于 FIFO 开关。

时钟偏差（同手册 §2.6.6）：NTP 关闭时用系统时间；「before BMC successfully gets the date and time from NTP server, BMC will sync with system time (e.g., from BIOS)」；「NTP will automatically be disabled whenever NTP servers cannot be reached... Log will be sent to Maintenance Event Log」。即 BMC 时钟先在 BIOS 系统时间、后切 NTP——同一条日志流内时间基准可能切换，NTP 失效会自我降级并留 MEL 记录。

固件管理范围与断电约束（§2.8.1）：Web 固件管理覆盖 BMC、BIOS、Motherboard CPLD、BackPlane CPLD、network AOC、storage AOC 及 PFR（Platform Firmware Resiliency）选项；「Systems are required to power down all HOSTs ... prior to Motherboard CPLD, Backplane CPLD, LCMC PDB CPLD, and BIOS firmware updates」；network/storage AOC 更新后需 reboot；Motherboard CPLD 更新后可能触发 BMC reset。**不可回退**（官方表述）：BIOS 更新时「If the Rollback ID of current firmware is higher than that of the previous firmware... Flashing the new firmware will make the system incompatible with any firmware versions lower than the uploaded firmware. As a result, the Backup and Golden images will be updated to the new firmware version.」——Rollback ID 机制使降级在该机型上有明确官方禁区；备份镜像在完整性校验失败时自动恢复，Non-ROT 平台不显示 Backup existing image 选项。

Redfish 固件模型实例（[Supermicro Redfish User's Guide · Firmware Inventory and Update Service](https://www.supermicro.com/en/support/manuals/product/software/redfish-user-guide/Content/general-content/firmware-inventory-update-service.htm)，Revision 6.1，2026-04-03）：`GET /redfish/v1/UpdateService/FirmwareInventory` 示例 15 成员：BMC、BIOS、Backup_BMC、Golden_BMC、Staging_BMC、Backup_BIOS、Golden_BIOS、Staging_BIOS、Motherboard_CPLD_[num]、Golden_Motherboard_CPLD_[num]、PowerSupply1、Capsule_MCU、Capsule_BIOS、Capsule_ME、BIOS_ME；Broadcom 存储卡条目为 `#SoftwareInventory.v1_3_0`（含 Updateable/Version/Status/RelatedItem/WriteProtected）。示例含 Capsule_ME、BIOS_ME 等 Intel 平台组件，说明该指南跨平台通用，**不证明 MI300X 机型逐项一致**。固件韧性动作：Oem `SmcUpdateService.Install` 的 InstallOptions 含 `UpdateGolden`（把当前镜像写入 golden 模板）与 `Recover`（「The backup image is always used for recovery when it exists; otherwise, the golden image is used」；Recover 自 BMC FW Gen13 1.12/Gen14 1.10 起，需 SFT-DCMS-Single license）；Staged 更新仅 Gen13/Gen14，上传至 Staging Region（复位后保留），激活经 `SoftwareInventory.Activate` 或 `UpdateService.Activate`，多组件激活顺序固定「BIOS > CPLD > BMC」，「The firmware update sequence may implement system shutdown/reboot based on hardware dependencies or different RoT designs. After finishing the operation, the system should return the previous power state.」各类部件入口：SimpleUpdate 仅支持 BMC 和 BIOS；BIOS 更新「will first perform a system power off」，preserve 选项 PreserveME/PreserveNVRAM/PreserveSMBIOS/BackupBIOS；Broadcom/Marvell 存储控制器、AOC NIC（`FirmwareInventory/NIC[num]`，须先确认存在——清单存在性即能力判据）、UBB CPLD/UBB Retimer（GPU 底板）各有上传目标。

## 固件身份清单与更新边界

### 各类固件的记录字段

固件身份清单至少按下表分列记录；字段取值以对应来源的清单实例为准，清单中不存在的类别保持 unknown，不推测补全。

| 固件类别 | DGX H100/H200 | Atlas 800T A2（iBMC） | Supermicro（MI300X 机型 OEM） |
|---|---|---|---|
| BIOS | `HostBIOS_0`；激活需 power cycle | 经 FirmwareInventory；OS 上电时升级需下电再上电或重启生效 | BIOS 及 Backup/Golden/Staging_BIOS；更新前 power off，Rollback ID 决定可否回退 |
| BMC | `HostBMC_0`（+ `EROT_BMC_0` 信任根）；激活 cold reset | iBMC 自身三分区镜像；重启 iBMC 生效、不影响 OS 业务 | BMC 及 Backup/Golden/Staging_BMC；SimpleUpdate 支持 |
| 设备（GPU/NPU） | 整组 `HGX_0` 目标；VBIOS/InfoROM 版本仅在 BMC GPU Information 页展示 | NPU 固件（HiLink、MCU）升级在升级指导书（本文未引用） | MI300X OAM 侧固件是否经 BMC Redfish 暴露无公开证据，unknown |
| NIC | CX-7 经 mlxfwmanager（约 30 分钟）；`FirmwareInventory` 清单示例未单列 | 带内通道（SP，.zip+签名）适用网卡固件 | `FirmwareInventory/NIC[num]`（AOC NIC，须先确认存在）；更新后 reboot |
| 存储 | NVMe 盘带外更新需 BMC ≥25.12.11 + SBIOS ≥1.7.8 | 带内通道适用 RAID 卡和硬盘固件 | storage AOC 更新后 reboot；Broadcom/Marvell 存储控制器各有上传目标 |

通用记录字段（对齐 Redfish SoftwareInventory 模型）：`Id`/`SoftwareId`、`Version`（及 `AdditionalVersions`）、`LowestSupportedVersion`、`Updateable`、`WriteProtected`、`RelatedItem`（固件作用的设备身份）、来源文档与机型/修订、采集时间。清单是文档或某次查询的快照，不是稳定事实；DGX 示例的 66 个成员、Supermicro 示例的 15 个成员都是示例时刻计数。

### 三种回退机制分列

三种机型的回退/韧性机制**不能抽象成同一「双分区」叙述**：

- **华为 iBMC 三分区**：主用/备用/可用，备用自动接管并保持版本一致，倒换使可用分区生效后三方再同步；描述对象是 iBMC 自身固件。
- **Supermicro 四镜像**：active/Backup/Golden/Staging；Backup 完整性校验失败时自动恢复，Recover 动作优先用 Backup、否则 Golden；Rollback ID 升高后 Backup/Golden 被同步为新版本，降级成为官方禁区。
- **NVIDIA 双分区（background copy）**：更新激活后经 OEM 动作 `NvidiaUpdateService.CommitImage` 同步两个分区；GPU 托架须确认 `BackgroundCopyStatus: Completed` 后再复位。

DMTF 层只提供 `Active`/`Staged`/`Updateable`/`WriteProtected` 与 `ForceUpdate` 语义，不规定镜像布局；「最低版本强制」类策略属实现侧（ForceUpdate 说明中明示存在永不被绕过的策略）。

### 更新流程的边界

本文只记录更新的**依赖、影响、回退/不可回退与验证**：前置条件（如 DGX 停止 GPU 活动、Supermicro 更新 CPLD/BIOS 前下电全部 host）、运行影响（部件生效条件、业务影响、断电要求）、回退能力（上述三种机制与 Rollback ID 类禁区）、验证方式（更新后以 FirmwareInventory 版本复核，配合 Update 注册表生命周期消息与 SEL 成功事件）。实际的固件发布、批量编排与变更窗口操作属于集群平台领域（05），不在本文范围。

## 事件记录方法

### 事件字段与时钟偏差

记录一条 BMC 事件时至少保留：事件码/`MessageId`、参数（`MessageArgs`/`_arg1_`..原文）、Severity（注意旧实现用 `Severity`、新模型用 `MessageSeverity`，且服务可覆盖注册表值）、`OriginOfCondition`（或 `OriginOfConditionUnavailable=true` 的显式标记）、`Created`/`EventTimestamp`、事件分组（`EventGroupId`，不蕴含顺序）、订阅/日志通道与采集时间。

时钟偏差方面，三个平台只有机制性证据、**没有偏差量数值**：

- Redfish 的 `EventTimestamp` 只承诺与 Redfish 服务时间一致，不保证与 host OS 时钟一致；
- iBMC 有 RTC 获取失败事件 `0x100000C3`（影响「iBMC侧日志时间不准确」）与时间跳变事件 `0x1A000029`（「iBMC time is stepped by more than _arg1_ minutes」，「可能导致iBMC日志记录时间混乱」）——iBMC 告警码引用的证据链边界（独立审阅两轮未取得原文、未独立核验）见 Ascend 实例节「取得与核对口径」；
- Supermicro BMC 在 NTP 同步成功前先用系统（BIOS）时间，NTP 不可达自动禁用并写 Maintenance Event Log。

结论：BMC 事件时间基准可能漂移或切换，跨层对齐时必须显式记录时钟源与同步状态，不能把 BMC 时间戳直接当作 host 时间。

### 设备身份对齐

事件的部件归属依赖 `OriginOfCondition` 链接、事件码参数（如华为的内存板槽位+丝印/CPU 槽位+通道号）与固件清单的 `RelatedItem`，三者都应映射到节点资源档案（见[计算节点资源与拓扑参考](resource-topology.md)）。华为文档明示「不同型号的服务器，同一通道对应的内存数量不同」，槽位解释随机型变化，跨机型套用参数解释会误定位。

### 丢失、重复与采集失败

规范层没有覆盖**端到端投递丢失/重复**的通用计数器；但要区分：日志侧存在标准溢出计数字段。LogEntry schema（[LogEntry.v1_22_0.json](https://redfish.dmtf.org/schemas/v1/LogEntry.v1_22_0.json)，2026-10-09 复核）定义了只读整数字段 `OverflowErrorCount`（`versionAdded: v1_14_0`），语义为「该日志条目之后发生的溢出错误计数」，且**条件性出现**——该条目是日志最新条目且其后无溢出错误时不出现；非最新条目且与下一条目之间无溢出错误时也不出现。这是**日志溢出计数**，不是订阅投递的端到端丢失/重复计数：字段缺失不能解释为零丢失，schema 定义也不证明设备实现（本批各机型实现情况均为 unknown；DGX H100/H200 的实现基线为 Schema 2019.1，早于 v1_14_0，不能假设支持）。其余可用的是机制性证据，采集记录中应分别标注：

- **本地缓存与订阅中断**：iBMC `cache_event_log.db`（未上报订阅事件数据库）证明订阅中断时事件先落库，订阅端缺口不代表 BMC 侧无记录；Redfish `DeliveryRetryPolicy` 四档（TerminateAfterRetries/SuspendRetries/RetryForever/RetryForeverWithBackoff）是订阅级声明，不证明送达。
- **容量上限**：iBMC 事件记录 90% 容量告警 `0x1A000011`、操作/安全日志 90% 告警 `0x1A00001B`/`0x1A00001D`（「可能会导致…部分历史日志丢失」，建议 syslog 远程转储；证据链边界同上，独立审阅两轮未取得原文、未独立核验）；Supermicro 4096 条上限与 FIFO 开关；DGX SEL 满策略 BIOS 属性（`DoNothing`/`Donotloganymore`，变更需 power cycle）。
- **采集失败**：iBMC 与 iBMA 心跳丢失 `0x1A000025`（「带内管理监控信息无法获取或实时更新」；证据链边界同上，独立审阅两轮未取得原文、未独立核验）；Supermicro NTP 失效自动禁用写 MEL。采集通道失败时应记为「无合格样本」而非「无事件」，与[设备健康证据与检测边界](health-evidence.md)的采样失败类别一致。

### 官方事件映射例与反例

映射例（DMTF 注册表逐字，[StorageDevice.1.6.0.json](https://redfish.dmtf.org/registries/StorageDevice.1.6.0.json)，Release 2026.1）：`MessageId = StorageDevice.1.6.DriveFailure`，Message 为 "A failure condition for the drive located in '%1' was detected."，Severity=Critical，NumberOfArgs=1（参数为硬盘位置，Example 值 'Bay 1'），Resolution 为 "Ensure all cables are properly and securely connected... Replace the defective cables, drive, or both."，ClearingLogic 为 `ClearsIf=SameOriginOfCondition`、`ClearsMessage=["DrivePredictiveFailure"]`；对应清除消息 `DriveFailureCleared`（Severity=OK，`ClearsMessage=["DriveFailure"]`）。注册表给出的是**消息模板**，映射到具体部件仍靠事件实例的 `OriginOfCondition`。

映射例（华为告警手册逐字，证据链边界同上：编写者经渲染提取取得并逐字核对的记录，独立审阅两轮未取得原文、未独立核验）：`0x0100000D` "[Memory board _arg1_] _arg2_ memory correctable ECC"（arg1=内存板槽位，arg2=内存丝印或 CPU 槽位+通道号，影响「降低系统性能」）；`0x56000019` "The historical ECC count of NPU Board _arg1_ NPU _arg2_ reaches the threshold"（NPU 板号+芯片 ID）；`0x0D000007` NIC health status degradation detected by PFAE。

**反例（不能据单一事件归因）**：

- mlxfwmanager 更新 ConnectX-7 时必现 `-E- Failed to query /dev/mst/mt4129_pciconf0 device, error: MFE_ICMD_BAD_PARAM`，官方说明「This behavior is expected because this device is not one of the networking adapters used to cluster the system, but a bridge device used internally and updated using a separate process」——更新工具报错不等于网卡硬件故障（[DGX H100/H200 FW Update Guide sequence.html 步骤 9](https://docs.nvidia.com/dgx/dgxh100-fw-update-guide/sequence.html)）。
- 华为 `0x2C00000F` "The host was restarted due to unrecognized reason"——官方显式「原因不明」，不可归因。另注意 `0x2C000063` 记录 "The host was restarted by BMC _arg1_"（如 "due to PCIe switch or retimer upgrade"）：**固件升级本身会产生主机重启事件**，跨层时间线须先排除此类计划内事件再谈异常归因；`0x0200000F`（RAID 重构停止）官方明示「重构停止并不表示重构结果成功，仍需检查是否有硬盘和RAID卡相关告警」。（以上三码的证据链边界同上：独立审阅两轮未取得原文、未独立核验。）

## 与其他层的关系

- 设备侧健康证据（DCGM/DCMI/MindX、采样失败与未覆盖的区分）见[设备健康证据与检测边界](health-evidence.md)；本批 T01-07 将在该文补充三平台错误码映射，BMC 事件与该文的驱动/设备层证据是同一事件链的不同层。
- 机柜级供电、散热告警与故障域划分见[机柜供电、散热与故障域](rack-power-cooling-and-failure-domains.md)与[功率与散热证据](power-thermal-evidence.md)；BMC 是这些设施告警进入事件流的入口之一（如 DMTF Platform 注册表的 `PowerBrake`）。
- 节点验收场景下的 BMC/固件基线核对见[节点验收与分诊](node-acceptance-triage.md)。
- 事件证据到根因结论的推理边界见[可靠性维度与故障域](../08-reliability/dimensions-and-failure-domains.md)；BMC 事件是证据来源之一，不单独构成根因。

## 已知证据缺口

- AMD MI300X 机型逐项 FirmwareInventory 无公开实例：Supermicro Redfish 指南示例含 Capsule_ME、SAS3108 等 Intel 时代组件，不能当作 MI300X 机型清单；MI300X OAM 侧固件是否经 BMC Redfish 暴露保持 unknown。
- DGX GB200 取证仅覆盖计算托架 BMC/HMC；NVLink 交换托架与机柜级管理面（RackManager）未取证。
- AMD 官方《Instinct MI300 Series Cluster Reference Architecture Guide》（文档号 63916）官方 URL 于 2026-10-09 返回 404，未登记、不可用；仅有第三方镜像，不作为证据。
- 华为《Atlas 800T A2 升级指导书》（EDOC1100317200）本轮未复核，本文不引用其 NPU 固件升级步骤。
- 时钟偏差只有机制性证据，三平台均无偏差量数值。
- 事件丢失/重复：无覆盖端到端投递丢失/重复的规范级通用计数器；规范层仅有 LogEntry `OverflowErrorCount`（v1_14_0 起，只读、条件性出现）的**日志溢出计数**，本批设备实现情况 unknown；本文所列其余均为机制性证据，非实例观测。
- DSP8011 bundle zip 未下载（参照既往 403 经验），注册表引用以单文件 RegistryVersion+Release 为准。
- 华为文档族版本不齐（iBMC 用户指南分页快照跨文档 09/13，告警处理为独立文档 05）；告警码与字段不可跨版本合并引用。
- iBMC 告警处理 05：本文列出的具体事件码条目已于 2026-10-09 第二轮定向复核取得事件类告警页原文并逐字核对一致（页面为 JS 渲染，此前两轮直接 curl 仅得页面壳，本轮经渲染提取取得，检索路径稳定性不作保证；明细以 batch-14-bmc-firmware-sources.md 为准）；全册未引用条目不作完整性断言；**iBMC 告警码与带内黑匣子/健康管理码的官方映射关系仍未取得**，两套码不能互译；**证据链边界**：本文所引 iBMC 告警码的含义/影响/建议为编写者经渲染提取取得并逐字核对的记录，独立审阅者两轮（2026-10-09）均未能取得该页原文、未做独立核验，相关内容不据此单独建立处置规则（处置以现场确认与厂商支持为准）。

## 来源与更新范围

- DMTF Redfish schemas（[schemas/v1 目录](https://redfish.dmtf.org/schemas/v1/)）与[消息注册表目录](https://redfish.dmtf.org/registries/)、[DSP8011](https://www.dmtf.org/dsp/DSP8011)/[DSP2065](https://www.dmtf.org/dsp/DSP2065)：2026-10-09 逐文件核对，规范角色模型。
- [NVIDIA DGX H100/H200 用户指南 bmc.html](https://docs.nvidia.com/dgx/dgxh100-user-guide/bmc.html) 与 [redfish-api-supp.html](https://docs.nvidia.com/dgx/dgxh100-user-guide/redfish-api-supp.html)（2026-01-26 更新）、[DGX H100/H200 Firmware Update Guide](https://docs.nvidia.com/dgx/dgxh100-fw-update-guide/)（2026-09-13 更新）、[DGX GB200 用户指南 compute-tray-redfish-commands.html](https://docs.nvidia.com/dgx/dgxgb200-user-guide/compute-tray-redfish-commands.html)（2026-09-17 更新）：厂商手册，绑定文档版本。
- 华为 [iBMC 用户指南 Redfish 接口页](https://support.huawei.com/enterprise/zh/doc/EDOC1100317056/611e8ddf)、[固件升级页](https://support.huawei.cn/enterprise/zh/doc/EDOC1100317056/9d7b49ce)、[一键收集信息说明](https://support.huawei.com/enterprise/zh/doc/EDOC1100317056/f40a8c00)、[使系统保持最新状态](https://support.huawei.com/enterprise/zh/doc/EDOC1100317202/c4fd778c)、[iBMC 告警处理 05](https://support.huawei.com/enterprise/zh/doc/EDOC1100317321/4c88faf1)、[iBMC Redfish 接口参考 23](https://support.huawei.com/enterprise/zh/doc/EDOC1000126991/14033122)：跨文档版本不齐，引用须带文档号与版本。
- Supermicro [BMC User's Manual X13/H13/B13](https://www.supermicro.com/manuals/other/BMC_IPMI_X13_H13_B13.pdf)（Rev 1.0b）、[Redfish User's Guide Rev 6.1](https://www.supermicro.com/en/support/manuals/product/software/redfish-user-guide/Content/general-content/firmware-inventory-update-service.htm)、[AS-8125GS-TNMR2 产品页](https://www.supermicro.com/en/products/system/gpu/8u/as-8125gs-tnmr2)：OEM 证据，不代表 AMD 官方行为。
- 待确认：AMD 官方集群参考指南恢复后可登记；GB200 NVLink 交换托架与机柜级管理面；MI300X 机型逐项固件清单实例；三平台时钟偏差量数值。
