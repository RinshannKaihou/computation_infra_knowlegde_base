# Batch 28 · T00-02 第二轮定向复核报告

## 会话元数据与结论

| 项目 | 记录 |
|---|---|
| 角色与范围 | 承接[第一轮定向复核](batch-28-t00-02-codex-recheck.md)的独立审阅者角色，仅复核 OPEN 项 C02/C05/C06 剩余条件与 N01，并检查这些修订引入的问题；本会话未编写或修改被审正文 |
| 实际执行模型 / 推理档位 | `gpt-6.1-sol / xhigh` |
| 模型核验 | 读取 `CODEX_THREAD_ID` 对应本地会话 JSONL：第 1 行 `session_meta`、第 8 行 `turn_context`（`2026-10-21T08:14:03.297Z`）；实际模型/档位仅见 `gpt-6.1-sol / xhigh`，与 `collaboration_mode.settings` 一致；assistant 消息未检出回退标记；本轮未另启模型、审阅 CLI 子进程或子代理 |
| 本轮会话 ID | `01a15d85-fb23-7a10-8456-aa3ba5dfb094` |
| 第一轮复核会话 ID | `01a15d7a-8578-7b30-9883-2751b534f128`；沿用其发现编号、优先级和最小剩余条件 |
| 执行方式 | 本地 Codex CLI，`originator=codex_exec`、`source=exec`、`cli_version=0.163.0`；静态定向复核 |
| 日期 / 时区 | 2026-10-21 / Asia/Shanghai |
| 工作目录 | `/Users/ywang2397/work/AI_reliability_knowledge_base` |
| 修订正文 | [reference-architectures.md](../../knowledge/00-overview/reference-architectures.md)，157 行 |
| 作者提交的正文 SHA-256 | `5b1842db54d52cb35b3e5ccd5da09d1ae64f9527785082d68ff80f872d7f1d30` |
| 独立计算的正文 SHA-256 | `5b1842db54d52cb35b3e5ccd5da09d1ae64f9527785082d68ff80f872d7f1d30`，**匹配** |
| 作者来源记录 SHA-256 | `54052337ded7e6bd2069cb693f8774331a53e45fbb4b7534dea4e8e43f42a6f5`，39 行 |
| 术语页 SHA-256 | `b3236bfaf3415edff43074ff3141c1872f81a302c1072cb38785e7ae9baebeba`，165 行 |
| 上游 resource-topology SHA-256 | `69daf8568a2170da42e367e3253eac8b9a6384e4373db12f9c1e29864e8b805a`，与第一轮记录一致 |
| 写入范围 | 仅新增本报告；不修改正文、来源记录、registry、术语页、导航、计划或审核状态；构建在临时源码副本执行 |

**结论：本轮 CLOSED=3（C02/C06/N01），OPEN=1（C05，P3）；未发现需新增 N02 或后续编号的问题。开放 P1=0、P2=0、P3=1，T00-02 暂未完成审阅闭环。**

第一轮已经关闭的 C01/C03/C04 沿用其状态，本轮不重新初审。候选瓶颈、术语范围与机柜共享边界已满足对应剩余条件；C05 的现行取证条目仍未与修订摘要一致，不能据摘要宣布关闭。此结论不构成 Batch 28 整批验收，不改变正文 `draft / source_checked` 状态，不建立真实硬件验证或平台兼容性结论。

## 方法与证据边界

已读取 [AGENTS.md](../../AGENTS.md)、[README](../../README.md)、[写作指南](../authoring-guide.md)、[内容总目录](../../content-outline.md)及[元数据 schema](../../schemas/content.schema.json)；对照[第一轮报告](batch-28-t00-02-codex-recheck.md)的最小剩余条件，重读修订正文、[作者来源记录](batch-28-t00-02-sources.md)、[术语页](../../knowledge/00-overview/terms-and-system-boundaries.md)、[来源登记](../../sources/registry.yaml)相关记录及 [T00-02 验收要求](../../plans/full-coverage-backlog.yaml)。定向核对[资源拓扑](../../knowledge/01-hardware/resource-topology.md) L179/L185/L216/L218/L222/L276–281，以及[机柜供电散热](../../knowledge/01-hardware/rack-power-cooling-and-failure-domains.md)的设施依赖与冗余边界；历史取证复用 [Batch 14 组成记录](batch-14-supernode-composition-sources.md)和 [Batch 18 互联记录](batch-18-interconnect-paths-sources.md)。关联页只作本轮条件的证据入口，不重新验收整篇。

为区分残留与新增问题，读取第一轮留存的源码副本 `/private/tmp/t0710-recheck2-build-7jcskkvu/repo`，核验其正文、来源记录和术语页哈希分别为 `b0ebacbf7eaefb98d51011cbf42465181e302e97f780d4db72e74489bb37dea9`、`4ea870c663222577223f9a97116c829f36e9a68472d7d8d18739b91f4b3cb05b`、`579fe1827610bc6ffce0f5134d79f26e31c9d2acd983d72afafaaea2675329e0`，均与第一轮报告一致。差异为正文 L121/L122、术语页 L60、来源记录 L9–12 及新增 L34–39；来源 L13–16/L21 与正文 L106/L110/L114 均未修改。该副本仅用于版本比较，不当作厂商原文缓存。

本轮成功重新打开 [GB 硬件页](https://docs.nvidia.com/dgx/dgxgb200-user-guide/hardware.html)与 [NVLink Networking 页](https://docs.nvidia.com/dgx/dgxgb200-user-guide/networking.html)，页脚均标 2026-09-17：核对机柜组成、柜内供电/供液、NVLink 连接与管理范围；亦打开指南目录、[H100 RA 架构页](https://docs.nvidia.com/dgx-superpod/reference-architecture-scalable-infrastructure-h100/latest/dgx-superpod-architecture.html)和 [fabric 页](https://docs.nvidia.com/dgx-superpod/reference-architecture-scalable-infrastructure-h100/latest/network-fabrics.html)，核对现有定位对应的架构/网络章节。没有把此次读取追改为 2026-10-09 的历史观察，也没有重新核验所有产品页、OEM 文档或维护指南。A3 [产品概述](https://support.huawei.com/enterprise/zh/doc/EDOC1100401572/bd23f260)与[组网拓扑](https://support.huawei.com/enterprise/zh/doc/EDOC1100401572/d975beba)均返回 HTTP 403，未取得本轮正文；A3 对照限于既有 Batch 14 取证与资源拓扑，不宣称重新核验了厂商原文。访问受限本身不另立发现。

下文“正文 L…”、“来源记录 L…”与“术语页 L…”均绑定元数据表中对应哈希。判定依据实际条目，修订摘要仅用于定位。

## OPEN 项逐项判定

| 编号 / 原优先级 | 判定 | 理由与证据 |
|---|---|---|
| C02 · P2 | **CLOSED** | 正文 L121 行名已统一为“数据路径候选瓶颈（待核，非定论）”，覆盖三种形态；集群列明确网络只是候选之一，列出负载与并行布局、通信量与重叠、实际拓扑/拥塞、端到端存储条件，并要求测量主导瓶颈和扩展收益。单机、超节点列因共同行名而同属候选口径，不再保留“网络主导”定论。关闭的是无依据的瓶颈断言，无须为措辞修订补造性能数据。 |
| C05 · P3 | **OPEN** | 来源 L10 两个裸 ID 已补全，本轮提取主张表 L9–16 的 21 个来源 ID，全部存在于 registry；L9 已加 GB 硬件页/指南入口，L12 已加 RA 两页，L11 支持范围栏也限定了检索范围。但 L10 仍无 A3 产品概述/组网拓扑链接；L13–16 仍只写“既有登记”或“某域交付正文”，L11 也未链接实际节点/平台档案。L11 主张栏仍写“无官方同构超节点公开样板”，L21 仍写“无官方公开样板，比较表中相应单元格保持 unknown”。正文 L106/L110/L114 的数字附近仍只有仓库页或不可点击章节名，未完成第一轮要求的就近上游定位。L37 所称已补 A3 链接、已删除单元格承诺与实际条目不符；这些均为原 C05 剩余条件，不另编号。 |
| C06 · P3 | **CLOSED** | 术语页 L60 名称栏改为 `supernode`，短定义涵盖“柜内或跨柜”“多台服务器/托盘”，并明确 Huawei SuperPoD、NVIDIA DGX SuperPOD 是具体产品名，不能作通用概念同义替换。与正文 L51/L81/L110 的范围一致；正文 L51 与术语页 L60 的双向链接保留，历史验收 L142 及历史口径说明 L165 未被追改。列出产品名用于区分命名，不构成把 DGX SuperPOD 集群样板改判为单一超节点域。 |
| N01 · P2 | **CLOSED** | 正文 L122 将 power shelf/busbar/manifold 限于该机柜的柜内共享组；另列 rPDU/CDU/供液干管，要求按实际接线/供液成员核对是否多柜共用，无映射即 unknown，并链接设施共享依赖方法。互联保留 L1 节点内、L2 跨节点/跨柜按组网形态核对；按部件、冗余前提和失效模式列候选组，没有把 N+N 当作全部故障情形的保证。物理受损、通信依赖与应用影响继续区分，实际影响映射仍 unknown。与资源拓扑 L179/L185/L216/L218/L222/L281 的组成层次相容，也与本轮重读的 GB 硬件页柜内配电/供液描述一致。无需执行故障注入才能关闭该物理共享范围错误。 |

## C05 的最小剩余条件

本轮已完成的 ID 修复、GB/RA 链接及版本边界应保留；无需新增 AMD 超节点资料，也无需重做已关闭问题。

| 位置 | 仍需修订 | 关闭判据 |
|---|---|---|
| 来源 L11 主张栏、L21 unknown 2 | 就地将 AMD 范围统一为“本库本轮未取得”，注明检索/复用范围限已登记的 OEM 节点资料与平台档案；删除“比较表中相应单元格保持 unknown”的不存在承诺 | 主张栏、支持范围栏、unknown 清单与正文 L114/L145 一致，不声称 AMD 普遍不存在此类官方材料 |
| 来源 L10 | 在现行 A3 主张行加入产品概述与组网拓扑的官方逐页入口 | 链接实际出现在主张表，可沿其追溯边界条款、柜内组成和 L1/L2；不只出现在 L37 修订摘要 |
| 来源 L11/L13–16 | 为节点样板补官方具体页或可追溯的机型段入口；为调度、存储、互联行链接对应 05/04/03 域实际条目 | 不再仅写裸文件名、“既有登记”或“某域交付正文”；例如可复用正文已链接的 K8s/Slurm、本地与共享/对象与并行存储、互联路径，以及 AMD 平台档案，无需新增正文 |
| 正文 L106/L110/L114 | 在 GB200、A3、H100 RA 的关键组成/互联数字附近补对应的可点击上游定位 | GB 对应 hardware 页与 NVLink Networking 节；A3 对应产品页、产品概述/组网拓扑；RA 对应架构/fabric 页。保留章节/表号、GB UG 2026-09-17、产品页 2026-10-09 观察、A3 用户指南 13/维护指南 14 与 RA 历史观察范围 |
| 来源 L31/L37 | 使修订记录与现行条目一致 | 可保留标明轮次的历史记录，但不能用“已删除”“已补链接”替代实际修订；完成后以主表、unknown 和正文重新定向核对 |

上述均沿用第一轮条件。正文已经链接资源拓扑、文末已有汇总来源，以及 `make check` 能通过，都不能代替这些自由文本取证条目的一致性与就近定位。远端访问受限时应记录限制，不必声称本轮重新取得 A3 原文。

## 修订引入的新问题

本轮指定范围内**未发现需要新增 N02 或后续编号的问题**。C02 的统一候选行名没有新增瓶颈排序；N01 没有反向声称上层设施一定跨柜或一定不跨柜；术语页没有继续把通用名与产品名用斜线等同。正文此次只改 L121/L122，没有新增执行命令、兼容组合、成本数据或实测结果。

来源 L37 与主表/unknown 的不一致属于 C05 原有追溯与一致性问题的延续，继续按 C05 计数，不把同一未完成修订重复立为 N02。本轮不扩大到关联正文、已关闭项或其他批次的全量初审。

## 验收边界

比较表相关的 C02/N01 已关闭，术语同步 C06 已关闭；C05 仍阻止取证追溯与修订一致性完成闭环。不能据本轮报告宣布 T00-02 evidence_blocker 或任务整体验收已完成，需完成上述剩余修订后定向复核。模型审阅与结构检查均不建立硬件、供电/互联故障影响或部署兼容性验证。

## 校验与写入范围

报告落盘后，工作区实跑 `PYTHONDONTWRITEBYTECODE=1 make check`，退出码 0：**PASS: 117 content entries; 553 sources**。为遵守“只新增这一个文件”，在临时源码副本 `/private/var/folders/bk/3f4npkcs6l30twg9ph23c2jh0000gn/T/t0002-recheck2-vlc9u7bh/repo` 执行 `make build`，使用工作区现有虚拟环境的 Python，退出码 0；成功重新生成两个 catalog，读取 JSON 确认 `documents=117`、`sources=553`。初次临时复制省略 `build/`，校验器因此报历史交付页的两个 catalog 链接缺失；补复制工作区现有构建产物后重跑通过。这是临时副本的准备缺项，没有据此修改源文件或新增内容发现；工作区 `build/` 未写入。

独立核对正文 31 处、术语页 35 处、本报告 16 处内联本地文件链接，目标均存在；`git diff --check` 与本报告空白检查通过。这些检查只验证结构、登记引用、本地文件路径及生成过程，不验证技术正确性、远端可达性、页内锚点语义或硬件兼容性。

写入前留存的 611 个既有源文件指纹在交付核对时均未改变或删除；本会话仅新增本报告，基线对比另观察到并行新增的 T07-11 第三轮报告，非本会话写入或验收。交付前再次核验正文、来源记录、术语页与资源拓扑哈希，均与元数据表一致。本轮未修改 `src/kb/`，未新增或运行代码回归测试；未访问真实设备/集群，未执行拓扑探测、性能测试、供电/互联故障注入、调度作业或发布，没有新增真实环境验证结果。
