# Batch 28 · T00-02 第三轮定向复核报告

## 会话元数据与结论

| 项目 | 记录 |
|---|---|
| 角色与范围 | 承接[第二轮定向复核](batch-28-t00-02-codex-recheck-2.md)，仅核对 C05 最后剩余的取证条目与定位，并检查本次修订引入的问题；本会话未编写或修改被审正文、来源记录 |
| 实际执行模型 / 推理档位 | `gpt-6.1-sol / xhigh` |
| 模型核验 | 读取 `CODEX_THREAD_ID` 对应本地会话 JSONL：第 1 行 `session_meta`、第 8 行 `turn_context`（`2026-10-21T08:21:15.384Z`）；实际模型/档位唯一为 `gpt-6.1-sol / xhigh`，与 `collaboration_mode.settings` 一致；assistant 消息未检出回退标记；未另启模型、审阅 CLI 子进程或子代理 |
| 本轮会话 ID | `01a15d8c-b177-7052-8ec9-cdb473821383` |
| 第二轮复核会话 ID | `01a15d85-fb23-7a10-8456-aa3ba5dfb094` |
| 执行方式 | 本地 Codex CLI；`originator=codex_exec`、`source=exec`、`cli_version=0.163.0`；静态定向复核与官方链接核对 |
| 日期 / 时区 | 2026-10-21 / Asia/Shanghai |
| 工作目录 | `/Users/ywang2397/work/AI_reliability_knowledge_base` |
| 修订正文 | [reference-architectures.md](../../knowledge/00-overview/reference-architectures.md)，157 行 |
| 作者提交的正文 SHA-256 | `4e94e12f5a9b956c5e48e539b219d576eafee423c5b742dc17726697d462ef03` |
| 独立计算的正文 SHA-256 | `4e94e12f5a9b956c5e48e539b219d576eafee423c5b742dc17726697d462ef03`，**匹配** |
| 本轮来源记录 SHA-256 | `5e5ef5612c16927c1ae303c59be5bfe1877d37b6f6ff80b8f582add73c6d1078`，43 行 |
| 术语页 / 资源拓扑 SHA-256 | 分别为 `b3236bfaf3415edff43074ff3141c1872f81a302c1072cb38785e7ae9baebeba` / `69daf8568a2170da42e367e3253eac8b9a6384e4373db12f9c1e29864e8b805a`；与第二轮一致 |
| 写入范围 | 仅新增本报告；不修正文、来源记录、registry、术语页、导航、计划或审核状态；构建在临时源码副本执行 |

**判定：C05 · P3 = OPEN。本轮 CLOSED=0、OPEN=1；未发现需要新增 N02 或后续编号的问题。**

正文三处就近链接已有实际修改，但来源记录的主张表与 unknown 清单未落实本次回应所列修订：第二轮所审的前 39 行原样保留，仅追加 L41–43 修订摘要。故不能据修订摘要关闭 C05。此前已关闭的 C01/C02/C03/C04/C06/N01 沿用原状态，本轮不重新初审。T00-02 仍未完成审阅闭环；本报告不构成整批验收，也不改变 `draft / source_checked` 或真实环境验证状态。

## 方法与版本证据

已读取 [README](../../README.md)、[写作指南](../authoring-guide.md)、[AGENTS](../../AGENTS.md)、[内容总目录](../../content-outline.md)和[元数据 schema](../../schemas/content.schema.json)，按第二轮 C05 的最小剩余条件核对[现行正文](../../knowledge/00-overview/reference-architectures.md)、[作者来源记录](batch-28-t00-02-sources.md)及[来源登记](../../sources/registry.yaml)相关条目。关联的[资源拓扑](../../knowledge/01-hardware/resource-topology.md)仅用于确认已登记机型、章节和历史取证边界，不重新验收整篇。

使用第二轮报告所留临时源码副本 `/private/var/folders/bk/3f4npkcs6l30twg9ph23c2jh0000gn/T/t0002-recheck2-vlc9u7bh/repo` 比较版本；先核验其中正文 SHA-256 为 `5b1842db54d52cb35b3e5ccd5da09d1ae64f9527785082d68ff80f872d7f1d30`、来源记录为 `54052337ded7e6bd2069cb693f8774331a53e45fbb4b7534dea4e8e43f42a6f5`，均与第二轮报告一致。差异只有：

- 正文 L106/L110/L114 添加官方链接；其他正文内容未变。
- 来源记录原 L1–39 完全未变，新增空行及 L41–43“复核第二轮修订”摘要；主张表 L9–16、unknown L21 均未修改。

这份副本只证明版本差异，不作为厂商原文缓存。下文“正文 L…”与“来源 L…”均绑定本报告元数据中的现行哈希；判定依据实际条目，修订摘要只作作者回应。

## C05 剩余条件逐项核对

| 第二轮要求 / 位置 | 本轮核验 | 判定依据 |
|---|---|---|
| 来源 L10：A3 主张行补逐页官方入口 | **未完成** | 精确位置仍为裸文本 `resource-topology.md（T01-05 交付）§A3 样板`，支持范围仍为“组成/互联/故障域”；整行没有产品概述或组网拓扑链接。正文 L110 的新增链接不能代替该行修订。 |
| 来源 L11：AMD 主张范围、OEM/平台定位 | **未完成** | 主张栏仍以“无官方同构超节点公开样板”起句，只有支持范围栏写“本库本轮未取得”；位置仍是裸文本 `resource-topology.md 四层表`，没有 MNL-2671 手册、MI300X 数据表或平台档案链接。范围与可点击入口两项均未落实。 |
| 来源 L13：单机样板具体入口 | **未完成** | 精确位置仍为“既有登记”，未添加 DGX H100/H200 UG 或 Atlas 800T A2 产品页链接。 |
| 来源 L14–16：调度、存储、互联实际正文 | **未完成** | 仍分别写“05 域交付正文”“04 域交付正文”“03 域交付正文”，未出现 Kubernetes 架构页或相应仓库正文链接。整份来源记录没有任何内联本地文件链接。 |
| 来源 L21：unknown 范围与不存在单元格承诺 | **未完成** | 原句仍为“无官方公开样板，比较表中相应单元格保持 unknown”；尚未改为“本库本轮未取得”“相应维度不作断言”。正文 L145 已用后一种范围口径，二者仍不一致。 |
| 正文 L106/L110/L114：关键数字附近上游定位 | **已有实质进展** | L106 加硬件页及指南入口；L110 加产品概述/组网拓扑；L114 加 RA 架构/fabric 页。GB 的 `UG §2.1` 链接实际落在指南目录，可再经 `NVLink Networking` 到具体网络节，不能记成已经直达该节。A3 与 RA 的逐页入口已落地；本轮远端核验边界见下节。 |
| 来源 ID 与版本边界 | **保持满足** | 从主张表 L9–16 提取的 21 个唯一来源 ID 均在 registry 中存在；原有 ID 修复保留。正文及复用档案继续区分 GB UG 日期、产品页观察、A3 指南版本与 RA 历史取证，没有把补链接写成硬件验证。 |
| 来源 L31/L37/L43：修订摘要与现行条目一致 | **未完成** | L43 再次声称已补 A3/AMD/单机/跨域链接并删单元格承诺，而实际主表与 unknown 原样保留。属于 C05 原有修订一致性问题的延续，不另立发现。 |

### 最小剩余修订

仅需落实第二轮已列出的条目修订，无需新增 AMD 超节点资料或正文：

1. **来源 L10/L11/L13–16**：把本次回应描述的链接写入主张表本身。AMD 行可用已登记的 MNL-2671 §1.1/§1.2、MI300X 数据表及[AMD 平台档案](../../knowledge/02-software-stack/amd-rocm-documented-profile.md)；调度、存储、互联可链接现有 [Kubernetes 生命周期](../../knowledge/05-cluster-platform/kubernetes-job-lifecycle.md)、[Slurm 作业资源](../../knowledge/05-cluster-platform/slurm-jobs-and-device-resources.md)、[本地与共享存储](../../knowledge/04-data-storage/local-and-shared-storage.md)、[对象与并行存储](../../knowledge/04-data-storage/object-and-parallel-storage.md)及[互联路径](../../knowledge/03-communication/interconnect-paths.md)。
2. **来源 L11/L21**：就地统一为“本库本轮未取得”，保留限于已登记 OEM 节点资料与平台档案的检索/复用范围；删去比较表相应单元格的承诺，改为相应维度不作断言。
3. **正文 L106、来源 L9 的 NVLink 定位**：可将指南目录入口收敛为下节已核的 `Networking` 页面及 `NVLink Networking` 节，保留 §2.1 标识，避免把目录称为具体网络页。这仍属原 C05 定位要求，不另编号。
4. **修订记录一致性**：以主表、unknown 与正文的实际修改为关闭依据；L31/L37/L43 保留轮次时，应明确此前完成声明与实际条目的偏差及最终纠正，避免继续用摘要替代修订。

## 官方链接核验与新增问题检查

本轮重新打开 [GB 硬件页的 Rack Configuration](https://docs.nvidia.com/dgx/dgxgb200-user-guide/hardware.html)：机柜组成段与正文所列托盘、管理交换机和供电组成对应；另从[指南目录](https://docs.nvidia.com/dgx/dgxgb200-user-guide/)沿 `NVLink Networking` 打开 [Networking 页](https://docs.nvidia.com/dgx/dgxgb200-user-guide/networking.html)，核对每 GPU 双向带宽、cable cartridge、fabric 管理及 SHARP 的所在段落。两章页脚均为 2026-09-17。正文新增 `UG §2.1` 的目标是目录，并非失效或无关 URL，但报告不把它记成直接节定位。

正文 L114 两个新增链接分别落在 [RA 架构页的规模表](https://docs.nvidia.com/dgx-superpod/reference-architecture-scalable-infrastructure-h100/latest/dgx-superpod-architecture.html)及 [Network Fabrics 的四网络、计算 fabric、存储 fabric 段](https://docs.nvidia.com/dgx-superpod/reference-architecture-scalable-infrastructure-h100/latest/network-fabrics.html)，与所复用的 SU/rail/超配主张相应；页脚均为 2025-11-19，与登记的可变网页历史观察口径相容。本次读取不追改为 2026-10-09 的历史观察，也不扩大为 RA 全文验收。

A3 [产品概述](https://support.huawei.com/enterprise/zh/doc/EDOC1100401572/bd23f260)与[组网拓扑](https://support.huawei.com/enterprise/zh/doc/EDOC1100401572/d975beba)本轮均返回 HTTP 403，未取得正文。其 URL 与资源拓扑既有逐页入口一致，只能确认链接已写入正文，不能声称本轮重新核验了官方内容。未重新打开没有实际新增的 OEM/单机产品文档；远端访问限制本身不另立问题。

**本轮未发现修订引入的、需要新增编号的问题。** 与第二轮的正文差异仅为链接插入，未改动数字、故障域候选条件、性能/成本判断、兼容组合或实测声明。来源主表未修、unknown 未统一及摘要失实均为 C05 既有剩余，不重复计为 N02。关联正文、其他批次与已关闭发现不在本轮重审范围。

本轮仅进行模型审阅、静态追溯和链接核对；未访问真实设备/集群，未执行拓扑探测、调度作业、性能测试或故障注入。结构检查与模型结论均不建立硬件验证或部署兼容性结论。

## 校验与写入范围

报告落盘后，工作区执行 `PYTHONDONTWRITEBYTECODE=1 make check`，退出码 0：**PASS: 117 content entries; 553 sources**。在包含本报告的临时源码副本 `/private/var/folders/bk/3f4npkcs6l30twg9ph23c2jh0000gn/T/t0002-recheck3-43y6kste/repo` 执行 `make build`（使用工作区现有虚拟环境的 Python），退出码 0，成功生成两个 catalog；读取 JSON 确认 `documents=117`、`sources=553`。副本保留原有 build 链接目标后重建；工作区 `build/` 未写入。

独立检查正文 31 处、本报告 17 处内联本地文件链接，目标均存在；来源记录没有内联本地链接，这也对应主表的实际定位缺口。`git diff --check` 与报告空白检查通过。上述工具不核验取证条目语义、远端内容、页内锚点或技术正确性，结构通过不能关闭 C05。未修改 `src/kb/`，未新增或运行代码回归测试。

写入前记录的 613 个既有源文件中，交付核对时 611 个指纹不变、无文件删除；另观察到 `plans/full-coverage-backlog.yaml`、`plans/topic-coverage.yaml` 的并行修改，以及新增 `docs/research/batch-28-t07-11-codex-recheck-4.md`，均非本会话写入或验收。本会话仅新增本报告，未修改任何既有文件；被审正文与来源记录交付前复算仍与元数据哈希一致。
