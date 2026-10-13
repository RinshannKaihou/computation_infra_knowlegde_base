# 第十八批技术审阅记录

**最新进展（2026-10-10）：第八次定向复核完成，C10 转 CLOSED，累计 16 CLOSED / 0 OPEN，Batch 18 在原定有限文档范围内通过。** 两条采集路径、per-QP/API 分支、本机标记占比、Cumulus 引用与现行注记已修订复验；T03-01–T03-04 的有限通过范围见[第八次复核](batch-18-codex-eighth-recheck.md)，前轮报告保留历史。正文仍 draft，基线 not_verified，无实机验证。C01 的初审反证为审阅者把 Product 单元格的斜杠错读成 Supported 值，已撤销：原始和复验 HTML 的六行 Supported 都是 `√`，并非页面改版。下列输入和判定保留为初审历史，不能作为最新状态或否定训练产品文档支持的依据。

审阅日期：2026-10-09（Asia/Shanghai）。**结论：暂不通过；B18-C01–C15 共 15 项发现，14 项 P2、1 项 P3，全部 OPEN。** 本记录为初审交付，未修订四篇知识正文，未进行修订后的定向复核。修订及定向复核完成前，不关闭本批任务或主题缺口。

约定模型 / effort 为 `gpt-6.1-sol / xhigh`。执行者为本会话 Codex 主助手，与本批既有取证、撰写记录分开；未派发子代理。本会话没有提供可独立核验的实际模型与 effort 运行标识，故将该配置记为用户约定，不写成已独立确认的执行元数据。模型审阅、来源核对与硬件验证分别记录。

依据：[完整覆盖路线图](../full-coverage-roadmap.md)、[T03-01–T03-04 验收清单](../../plans/full-coverage-backlog.yaml)、[依赖视图](../batch-dependencies.md)、[写作指南第 7 节](../authoring-guide.md#7-批次审阅约定)、[主归属目录](../../content-outline.md)及 [AGENTS](../../AGENTS.md)。Batch 13/14/15 已验收前置的有限范围保留；Batch 17 的未关闭发现不作为本批的直接依赖阻断，也不据此扩大前置验收范围。

## 审阅范围与输入身份

读取三篇新正文、集合通信全文及相对 HEAD 的增量、通信领域索引、四份研究记录、来源审计、相关登记和 metadata schema。独立取证重点为本批新增路径、RDMA、诊断和算法内容；集合通信已有 HCCL PDF、主机返回与多组次序段未全部重新取证，不把历史 `source_checked` 扩大成全篇重新核验。

| 任务 | 正文 | 初审输入 SHA-256 |
|---|---|---|
| T03-01 | [interconnect-paths.md](../../knowledge/03-communication/interconnect-paths.md) | `f74324f886837041fc3ca111093b24663fe5e6e944a21eabce902a4b52910d58` |
| T03-02 | [ethernet-ib-roce-rdma.md](../../knowledge/03-communication/ethernet-ib-roce-rdma.md) | `65fed21af7eebdc86fe683d7abba6d08855e9d6daf772d25973066b84be06ac4` |
| T03-03 | [rdma-baseline-and-congestion-triage.md](../../knowledge/03-communication/rdma-baseline-and-congestion-triage.md) | `93cf4c7b31a2161b22dd7aa4fd7952a8f2bf1b88aefbcd20aebee10da9e43cae` |
| T03-04 | [collectives-and-rank-progress.md](../../knowledge/03-communication/collectives-and-rank-progress.md) | `a4405d656a3095afd883833ebede40b9c9cfb74aeec33f15dfd684ebcd38dc1e` |

领域索引输入 SHA-256：`9102358b1e7d08455114dda724b0e3bb24ecdb06118eece19b80dc9d003989e5`。来源登记输入 SHA-256：`900b22e6b540a9af313f95abcce15ffdfaa2b21c37e3efd5497a35b49886a54a`（366 项）。来源审计输入 SHA-256：`5eb6e1cd6f56d57a7daf6982e8ea795be2136b2a68fcc256212abdee648619e5`。

| 研究记录 | 初审输入 SHA-256 |
|---|---|
| [互联路径](batch-18-interconnect-paths-sources.md) | `4df879cab7d70ca436659f6cbd6843031b95112ee305f6a82e1b7d3bd2fbc627` |
| [RDMA 机制](batch-18-rdma-mechanism-sources.md) | `c691a823e24ab31c959a72e0bc1275c72cba11524675d281b11171195f80a4ad` |
| [RDMA 基线](batch-18-rdma-baseline-sources.md) | `4f4d1c08f24d18103d29278dcc0b5cbd26251bdf85010db7166d4d6fd218fc55` |
| [集合扩展](batch-18-collectives-extension-sources.md) | `ed53bf15a3703ce08a10721b8e1f32de1df47c39a5e79f5811d7badee944c9a7` |

## 独立取证范围

- NVIDIA：DGX H100/H200 指南 Introduction 的组件表、System Topology 与 Table 5/6；H100/NVLink 产品页；SuperPOD H100 RA 架构与 fabric 页；nvidia-smi 当前手册；NCCL 2.27.5 collectives、P2P、env 与 troubleshooting。产品页和无版本手册只作观察日期范围，不建立硬件兼容组合。
- Ascend：CANN 900 `aclrtGetDevicesTopo` 静态页（带 6066 端口与无端口正文相同）；MindCluster 730 亲和原则正文及 A3 产品页。A3 用户指南组、LingQu 630 的原有 Batch 14 核对范围沿用，不宣称本轮重新取得全部支持站内容。
- rdma-core v65.0：解析并读取固定 commit `58e40801bfed5a8befc0881594820fa0a0baa4a1` 的九个 verbs man 源文件、mlx5 `cq.c` 和 COPYING；man7 快照不等于该 commit，本轮未做九页完整逐字差分。
- perftest 26.07.8：解析并读取固定 commit `a31f9ea9df720ee68f941e55f75fec31349fcd35` 的 README、参数检查、资源实现与 COPYING。下文源码行号按 raw 原文件计数，没有运行 benchmark。
- Linux v6.16：读取固定 tag 下 `Documentation/infiniband/user_verbs.rst` 和 `Documentation/ABI/stable/sysfs-class-infiniband`；当前 docs.kernel.org 入口不等于固定版本证据。
- 网络文档：UFM 4.18.15 端口计数器、Cumulus 4.3 RoCE lossless/lossy 模式、OFED RoCE/SM/Secure Host 页面及实际 canonical 版本；DOCA 3.5.0 归档 RDMA-aware Guide 的局部 RR/RNR 与 SM 主备机制。没有把上述不同产品线拼成可运行环境。
- 算法与框架：取得 Thakur 等 2005 的 18 页 PDF 与 Patarasuk/Yuan 的 24 页作者稿，提取文本并渲染核对公式页（Thakur 文内 p9、Patarasuk 文内 p13）。下文页码为所链接文件内页码，后者不冒充期刊页码 117–124。读取 Open MPI 4.1 Allreduce/Alltoallv、PyTorch 2.8 FSDP Notes、Megatron latest 的 TP mapping/PP P2P 精确页面；latest 尚不能作为被冻结实现。

新增八项审阅证据登记于 [sources/registry.yaml](../../sources/registry.yaml)：固定 verbs man、mlx5 CQ、perftest README/参数实现、v6.16 user_verbs/sysfs ABI、DOCA 3.5.0 局部机制、PyTorch 2.8 FSDP Notes。原作者登记保留，版本错误由下列发现要求修订；临时原文、PDF 和日志没有镜像到仓库。

## 发现与关闭条件

### B18-C01 — P2：拓扑 API 被扩大为 A2/A3 全系，验证计划用于未证支持的训练型号

**纠错：本节“训练行 Supported 为 `/`”的反证错误，已撤销，C01 CLOSED。** 按原始 HTML 的 tr/td 复验，training/inference 在同一 Product 单元格，Supported 为 `√`。完整抓取身份和条件计划判定见[第一次复核的 C01 纠错](batch-18-codex-recheck.md#c01-分歧复验与审阅者纠错)。下文只保留初审错读的历史，不用于当前技术判断。

位置：`interconnect-paths.md:80、88`；`src.ascend.cann-aclrt-devices-topo-2026-10-09` 的 notes。

正文称适用表“含 A2/A3 全系”，并把全对矩阵用于所选训练节点。实际表中 A2/A3 training product 的 Supported 为 `/`，对应 inference product 才为 `√`；另有 Atlas 200I/500 A2 的 Ascend RC 形态例外。表中的其他通用 training 行不能覆盖型号专属行。这份材料不能支持全部 A2/A3 训练产品可用，计划按此执行会首先碰到 API 适用性问题。

证据：[CANN 900 aclrtGetDevicesTopo 的 Applicability 与 Note](https://www.hiascend.com/doc_center/source/en/CANNCommunityEdition/900/API/runtimeapi/aclcppdevg_03_1895.html)。`/` 的具体解释未另取得图例，本次仅否定“已证全系支持”，不补造另一个支持矩阵。

关闭条件：按产品与形态转录适用表，移除全系断言，同步登记与研究记录；所选 A2/A3 训练样板另取明确支持的观察接口，或将这一验证分支标为证据不足、不能执行。不能用其他产品的肯定行补齐。

### B18-C02 — P2：把重复的 CX 编号误当一张卡，DGX 共享故障域判断反了

位置：`interconnect-paths.md:64、68`；互联路径研究记录的端口映射项。

“单 CX 卡（双 OSFP 端口共享，Table 6 CX0/CX1 复用行）”不符合所引指南。DGX 的计算网络是八张单端口 ConnectX-7 卡，分属两个网络模块；一个 OSFP/DensiLink 组合承载两张卡的连接。Table 6 的 CX0–3 在两个模块内各编号一次，重复 CX0 不是同一卡：例如 CPU1/module1 的 CX0 是 GPU7、`dc:00.0`、`mlx5_11`，CPU0/module0 的 CX0 是 GPU3、`5e:00.0`、`mlx5_5`。以 CX 标签单独合并资产会错误划分故障域。

证据：[DGX 指南 Network Specifications、DensiLink 与 Table 5/6](https://docs.nvidia.com/dgx/dgxh100-user-guide/introduction-to-dgxh100.html)。

关闭条件：以模块/槽位/BDF 联合身份展开端口映射，分别列卡、OSFP 连接器、线缆与网络模块的共享候选；只把原图明确共用的组件写成共享域，不由重复局部编号推断。同步资产核对表与来源记录。

### B18-C03 — P2：两套物理路径图、资产对照表及可判读的最小验证计划未交付

位置：`interconnect-paths.md:45、60–88`；T03-01 acceptance 第三项。

verification 说“路径图为来源整理示意”，正文实际上只有段落表，没有两份物理路径图。软件发现部分列命令名，未把一个软件设备身份、物理端口、模块、rail 与资产记录字段对齐；Table 5/6 的“逐行引用”也没有展开。最小计划只有工具组合，缺少固定输入、比较对象、观察点和通过/失败/无法判断条件，尚不能用于辨别走错 rail、缺边或链路异常。A2 未公开边可以画为 unknown，但不能因此省略整个样板图和方法。

证据：[T03-01 验收要求](../../plans/full-coverage-backlog.yaml)；[DGX 拓扑与映射原文](https://docs.nvidia.com/dgx/dgxh100-user-guide/introduction-to-dgxh100.html)。

关闭条件：补两份原创、带来源定位的路径图；有证边、逻辑关联与 unknown 明确区别；至少展开一组软件身份到物理资产的核对行。给出两样板的待执行最小对照、前提与判据，接口适用性先按 C01 修正；同步 verification，不能描述尚不存在的图为已核对。

### B18-C04 — P2：版本绑定和来源核对状态互相矛盾，浮动入口被写成固定证据

位置：`ethernet-ib-roce-rdma.md:20、28、35、59–60、105–110`；`rdma-baseline-and-congestion-triage.md:27、31、68、86–91`；三份路径/RDMA 研究记录及相关登记。

机制文先说 man7 已与 v65.0 对版，后又说待对版；docs.kernel.org 浮动入口直接标 v6.16。诊断文保留“drafting 时固定”的 rdma-core tag、内核选择和源码行号，已经进入正文仍未完成。OFED 五项登记把 `586042lts / 24.10-5.1.6.1 LTS` 合写为一版；本轮取得 RoCE、SM、Secure Host 的 canonical 实际指向 `24.10-5.1.6.1lts`。旧 URL 字符串与 HTTP 200 不能证明取得了声称的旧版本。研究记录所谓“主张—来源定位表”仅为短句串，未给出关键小节/固定行，难以复核哪条已证。

证据：[固定 v65.0 man 源文件](https://github.com/linux-rdma/rdma-core/blob/58e40801bfed5a8befc0881594820fa0a0baa4a1/libibverbs/man/ibv_post_send.3)、[v6.16 user_verbs](https://github.com/torvalds/linux/blob/v6.16/Documentation/infiniband/user_verbs.rst)、[实际 OFED RoCE canonical](https://networking-docs.nvidia.com/mlnxofedswum/24.10-5.1.6.1lts/rdma-over-converged-ethernet-roce)、[实际 SM canonical](https://networking-docs.nvidia.com/mlnxofedswum/24.10-5.1.6.1lts/nvidia-sm)。Megatron 的独立范围问题见 C14。

关闭条件：选定实际取得的文档版本并逐条对齐正文/登记/研究记录；固定 GitHub 文件 ref 与小节/行号。未完成的对版明确为未完成，收窄 source_checked 的 notes；保留旧获取记录为历史，不把本轮固定原文件取得冒充作者当时完成。不同组件版本只作分别取证，不声明配套。

### B18-C05 — P2：WRITE_WITH_IMM 被并入无需远端接收资源的普通单边操作

位置：`ethernet-ib-roce-rdma.md:55、93–96`。

普通 WRITE/READ 与 WRITE_WITH_IMM 一并写为远端 CPU 不参与，未说明后者消耗远端预投 RR 并产生接收通知。数据仍写到 remote_addr，而不是普通 SEND 的接收 buffer；但没有 RR 时会产生 RNR。遗漏该条件会把接收资源不足误判为链路或远端内存问题。MR 本地注册失败和后续远端访问错误也不应落在同一注册返回阶段。

证据：[RDMA-aware Guide §4.1.4、§4.3.2 及 ibv_post_recv 节](https://networking-docs.nvidia.com/doca/archive/3-5-0/rdma-aware-networks-programming-guide)。这里引用局部机制，不采用其整套旧 API 为 v65.0 保证。

关闭条件：分列 SEND、WRITE、WRITE_WITH_IMM、READ 的远端资源、数据落点、通知与完成；将注册 errno、post 提交错误、WC、异步事件分阶段映射，给出 RNR/权限不足的不同候选与下一检查，不以本地注册失败直接推导远端 ACCESS_ERR。

### B18-C06 — P2：成功 WR 未必逐条有发送 CQE，WRITE 的 byte_len 不能作通用字节证据

位置：`ethernet-ib-roce-rdma.md:59、95–96`。

故障表把发送 CQE 缺失直接列为异常，没有 signaled/sq_sig_all 与 CQ 消费前提；成功的 unsignaled WR 本来就不要求逐条通知。READ/WRITE 又统一观察发起侧 byte_len：固定 mlx5 provider 的 WRITE/WRITE_IMM 和 SEND 成功分支只设置 opcode，不填 byte_len，READ 分支才填。将这个字段拿来验收 WRITE 大小可能读取未赋值或遗留字段。

证据：[post_send L140–150](https://github.com/linux-rdma/rdma-core/blob/58e40801bfed5a8befc0881594820fa0a0baa4a1/libibverbs/man/ibv_post_send.3#L140-L150)、[mlx5 cq.c L164–182](https://github.com/linux-rdma/rdma-core/blob/58e40801bfed5a8befc0881594820fa0a0baa4a1/providers/mlx5/cq.c#L164-L182)。非 SUCCESS 时四字段有效的原文表述是正确的，本项不撤销它。

关闭条件：逐原语/方向/状态列有效观察字段和通知配置；字节数采用请求长度及有明确语义的接收/端口证据，不能把一个 provider 的 READ 字段赋值扩为通用 WRITE 保证。无 CQE 先核对通知策略、消费及时间窗，再进入故障分支。

### B18-C07 — P2：把 PFC 无损模式写成全部 RoCE 可靠运行的必要条件

位置：`ethernet-ib-roce-rdma.md:68`；OFED RoCE/流控登记 notes。

正文无条件要求 PFC+ECN，混淆传输可靠性与特定网络的无损设计。已登记的 Cumulus 4.3 文档同时定义 lossless（PFC+ECN）和 lossy（ECN）RoCE 模式，且限 Spectrum ASIC。不能从 lossless 设计页推成所有 RoCE 必须启用 PFC，也不能反向保证任意 lossy 网络的性能。

证据：[Cumulus 4.3 RoCE 的模式及硬件限制](https://docs.nvidia.com/networking-ethernet-software/cumulus-linux-43/Network-Solutions/RDMA-over-Converged-Ethernet-RoCE/)。

关闭条件：分开 RC 等传输保证、丢包重试、PFC 流控、ECN 拥塞响应和工作负载目标；按选定 NIC/交换机/模式给出条件，对其他网络保留未知。同步机制文与诊断文的停止/恢复规则，不写成通用部署处方。

### B18-C08 — P2：RDMA 机制的必交图、工作负载/设计/隔离比较与独立流程链接缺失

位置：`ethernet-ib-roce-rdma.md:46–48、70–79、101`；T03-02 acceptance 第一、第三、第四项。

“三柱图”只有封装文字，没有数据路径图与参与者/完成证据。工作负载节列参数和依赖，未比较实际工作负载为何选择不同通信方式、网络设计与安全/隔离条件；仅将全部 fabric 隔离标 unknown 不能关闭该必交子项。独立验证写“留 T03-03/V 轨”，没有指向现有诊断正文的普通链接，related_ids 不能替代阅读路径。NPU 直连未知记录本身正确，不要求从 GPU 能力推断它。

证据：[T03-02 验收清单](../../plans/full-coverage-backlog.yaml)及[路线图来源门槛](../full-coverage-roadmap.md)。

关闭条件：补协议承载与 verbs 数据路径的原创图；给出有限工作负载/依赖/设计/安全比较，并取得一个明确版本的隔离机制样板，其余继续 unknown。链接可判读的独立验证流程，尚缺证的必交范围保持 OPEN，不能用待补计划代替交付。

### B18-C09 — P2：IB 路由工具与驱动计数器限制被泛化到 RoCE，实际路径取证不足

位置：`rdma-baseline-and-congestion-triage.md:42–44、52–53、65`。

前文虽说 IB/RoCE 分开，后续路径表却混列 ibtracert/ibdiagpath/ibroute 与 ibnetdiscover，G4 只有 IB 路由快照，缺少 RoCE L3 下一跳/ECMP/rail 的实际路径字段。“计数器只经 sysfs，RoCE 流量不进以太网计数器”扩大了原文：RoCE offload 流量不关联 Ethernet **device driver** 的 counters，不等于 NIC 硬件或物理交换机 Ethernet/PFC/ECN 计数器没有该流量。SM“每子网一个”也需明确 active master 与 standby 的区别。

证据：[所取得 OFED RoCE 章的 RoCE Traffic 小节](https://networking-docs.nvidia.com/mlnxofedswum/24.10-5.1.6.1lts/rdma-over-converged-ethernet-roce)、[UFM 端口计数器](https://networking-docs.nvidia.com/ufmsdnappswum/41815/infiniband-port-counters)、[RDMA-aware Guide Glossary 的 SM](https://networking-docs.nvidia.com/doca/archive/3-5-0/rdma-aware-networks-programming-guide)。

关闭条件：分别列 IB、RoCE 的路径与计数器来源、管理对象和缺证处理；给出选定 IB/RoCE 示例及 G4 对应快照设计。区分 driver/netdev、RDMA NIC 硬件、交换机计数器；只在固定工具/平台资料范围内写命令，不能用 IB 路由成功替代 RoCE 路由已确认。

### B18-C10 — P2：计数器语义未逐项完成，停止/恢复门槛把正常活动和异常混在一起

位置：`rdma-baseline-and-congestion-triage.md:53、61、76–80`；T03-03 acceptance 第二项。

正文仅列 Data 4 字节、Wait tick 和 normalized 名称，未逐项绑定方向、端口/优先级/VL 范围、累积/reset、采样窗口及 tick 时长，也未完成重试/CQE/PFC/ECN 表。G0 要“零增量计数器”，正常收发字节计数本来应增长；拥塞恢复又同时要求回到基线带内与零增量，正常 ECN/PFC 活动未必应为零。XmitDiscards 有多种原因，不单独证明拥塞；XmitWait 是信用不足或仲裁导致等待的 tick，不是通用丢包数。“事件清零后”也未说明保存原始证据与重建窗口。

证据：[UFM 4.18.15 的原始与归一化指标定义](https://networking-docs.nvidia.com/ufmsdnappswum/41815/infiniband-port-counters)、[Cumulus 4.3 RoCE](https://docs.nvidia.com/networking-ethernet-software/cumulus-linux-43/Network-Solutions/RDMA-over-Converged-Ethernet-RoCE/)。未知 tick 时长不可换算等待秒数；归一化指标还须保留各自计算与适用端口条件。

关闭条件：选定 NIC/固件和交换机文档样板，按指标展开单位/方向/范围/累积/重置/窗口/来源；缺失项不算完成。将正常流量、流控/拥塞响应和错误计数分列；零增量只用于有依据的错误项，其余与同窗口基线比较。停止是风险控制而非根因证明，恢复前保留证据，不要求无依据地清零设备计数器。

### B18-C11 — P2：perftest NUMA 互斥关系和外部绑定优先级写错

位置：`rdma-baseline-and-congestion-triage.md:68`；RDMA 基线研究记录的 NUMA 项。

正文说 pin_cores/numa_node/disable_numa 全部互斥且外层 taskset 优先。固定 README 和参数检查只拒绝 numa_node 与另两项的组合；自动 NUMA 检测遇外部 CPU 限制时跳过，但显式 pin_cores 或 numa_node 会覆盖外部绑定。按现文准备对照，实际 CPU/内存放置可能与记录相反。CPU cycle timestamp 避免的是计时 syscall 的开销，也不能表述成整个被测进程不会发生上下文切换。

证据：[README L376–401](https://github.com/linux-rdma/perftest/blob/a31f9ea9df720ee68f941e55f75fec31349fcd35/README#L376-L401)、[参数检查 L2463–2471](https://github.com/linux-rdma/perftest/blob/a31f9ea9df720ee68f941e55f75fec31349fcd35/src/perftest_parameters.c#L2463-L2471)、[计时方法 L59–81](https://github.com/linux-rdma/perftest/blob/a31f9ea9df720ee68f941e55f75fec31349fcd35/README#L59-L81)。

关闭条件：按默认检测、外部限制、显式参数、libnuma/未知 NIC NUMA 分列优先级；区分请求配置与实际绑定证据。修正计时句的范围，同步研究记录，未运行不填实际放置结果。

### B18-C12 — P2：零 validation errors 未证明覆盖充分，对照矩阵缺少测量与校验分支

位置：`rdma-baseline-and-congestion-triage.md:45、54、61–68`。

引用“只有 errors 是真问题”后，把 errors=0 作为健康/基线门禁，未记录 skips/stale work 对覆盖率的影响。固定 README 明示并发校验器竞争 CPU/GPU/内存/PCIe 会降低覆盖率，并影响正确性结果可靠性；校验自身也会降低带宽。G0 的全尺寸扫描与 validation 不兼容，虽然前置段提醒 `-a` 互斥，执行表没有分开性能扫描和逐尺寸校验；消息档仅“小/中/大”，没有固定值、时长/迭代与 host/CUDA 校验路径的版本前提。NIC/交换机样板也仍未选定，尚不是可判读的有限 procedure。

证据：[README L472–490 的开销/竞争限制](https://github.com/linux-rdma/perftest/blob/a31f9ea9df720ee68f941e55f75fec31349fcd35/README#L472-L490)、[L515–523 不兼容选项](https://github.com/linux-rdma/perftest/blob/a31f9ea9df720ee68f941e55f75fec31349fcd35/README#L515-L523)、[L536–563 的计数器解释](https://github.com/linux-rdma/perftest/blob/a31f9ea9df720ee68f941e55f75fec31349fcd35/README#L536-L563)。固定 README 允许多 QP 校验示例，本项不把 `-q 4/8` 判为不支持。

关闭条件：给出固定工具/有限硬件文档样板下的两节点/多节点矩阵；明确性能扫描、逐尺寸校验、host/device buffer、单进程多 QP 与多进程背景的不同条件。预定义输入大小、迭代/时长、统计口径、校验覆盖记录和无法判断条件；不足覆盖时 errors=0 只能说明已检查部分未报错。不得把含校验与不含校验的吞吐差直接归因网络。

### B18-C13 — P2：ring all-reduce 公式省略有限 p 因子，符号和算法前提也不完整

位置：`collectives-and-rank-progress.md:97–105`。

表把 ring 成本写为等式 `2(p−1)α+2nβ+nγ`。按两阶段各 p−1 轮、每轮 n/p 数据及本文 α–β–γ 模型，应为 `2(p−1)α+2((p−1)/p)nβ+((p−1)/p)nγ`；现式仅是大 p 近似，例如 p=2 的字节项相差一倍。该式是把论文环轮次接入代价模型的推导，不是 Patarasuk 定理原文的完整延迟公式。表还未定义 p、lg，混用 N；all-gather 的 n 应为每 rank 最终总输出字节数，recursive-doubling/二项树需说明 p/取整条件，最优性需保留无竞争与操作限制。

证据：[Patarasuk/Yuan 作者稿 §4.1、定理 1（文件内 p13）](https://cs.fsu.edu/~xyuan/paper/09jpdc.pdf#page=13)、[Thakur 等 §3、§4.1、§4.5（文件内 p2–3、p9）](https://fs.hlrs.de/projects/par/rab/publ/HPCA_collectives.pdf)。**Rabenseifner reduce 行的现有公式在论文相应条件下有依据，不作为误标 all-reduce 报错。**

关闭条件：逐行定义消息量口径、p、log/ceil、power-of-two/非二次幂分支、单端口/距离/竞争/可结合或交换等前提；精确式与近似式明确区别。保留理论模型、特定实现与实际选中算法三层边界，不用历史 cutoff 代替当前运行证据。

### B18-C14 — P2：集合扩展的原创图和 all-to-all 数据流未交齐，框架映射未冻结且缺消息大小

位置：`collectives-and-rank-progress.md:73–91、111–119`；集合扩展研究记录；T03-04 acceptance。

“下图/每格”之后只有列表，没有原创图；六条里加入 reduce，却没有单独 all-to-all 的分块转置数据流，P2P 可表达它不等于已经解释。DP/TP/PP/EP 表仍引用 Megatron latest 首页并写“drafting 前固定”；EP 引入范围外的 DeepSpeed E+D/E+Z，没有准确链接或独立登记，“消息形态”栏实际上填 ep_size 组身份而非消息大小。TP 一条 tokens×hidden/TP 不能代表表内所有原语，PP 的 shape 先行需条件实现；FSDP 的分片输入公式也须注明 unit、dtype 字节及输入 chunk，不能当所有通信总量。in-place 标题承诺但没有相应说明。

证据：[T03-04 验收清单](../../plans/full-coverage-backlog.yaml)、[NCCL 2.27.5 collective/P2P](https://docs.nvidia.com/deeplearning/nccl/archives/nccl_2275/user-guide/docs/usage/collectives.html)、[PyTorch 2.8 FSDP Notes](https://docs.pytorch.org/docs/2.8/notes/fsdp.html)。本轮看到 [Megatron TP mapping](https://docs.nvidia.com/megatron-core/developer-guide/latest/apidocs/core/core.tensor_parallel.mappings.html) 和 [PP P2P 页面](https://docs.nvidia.com/megatron-core/developer-guide/latest/apidocs/core/core.pipeline_parallel.p2p_communication.html)仍属浮动线，不将其提升为已冻结实现。

关闭条件：补要求的六类小规模原创图，明确变长的逐对匹配、root 与所保留的 in-place API 条件。选定可核对的框架 tag/commit 和精确调用路径，逐 DP/TP/PP/EP 列逻辑 shape、dtype bytes、每 rank 输入/输出或分段消息、通信组与条件；DeepSpeed 若保留须独立登记取证，或回到所选实现。EP 必交大小/路由信息未取得时该子项继续 OPEN。

### B18-C15 — P3：来源链接 404 与标题拼接导致阅读和核对退化

位置：`interconnect-paths.md:92`、`collectives-and-rank-progress.md:121`、来源审计“候选 URL 全部 HTTP 200”记录。

互联文 L70 用正确的 NCCL `docs/troubleshooting.html`，L92 却多插 `usage/`，本轮后者返回 404。集合文把原说明段拼进“## 四种进度不能互相代替”的 H2，破坏章节标题与正文边界。这些问题不会被本地引用校验发现，不能以 make check 通过证明远端来源都可用。

证据：[可读的 NCCL 2.27.5 troubleshooting](https://docs.nvidia.com/deeplearning/nccl/archives/nccl_2275/user-guide/docs/troubleshooting.html)及上述初审文件行。

关闭条件：统一精确来源 URL，修复 H2/说明段落；审计注明旧 HTTP 检查的范围与本轮例外，定向检查修订链接和渲染结构，不抹去历史获取记录。

## 任务验收与后续复核

| 任务 | 当前已有的有限交付 | 未关闭范围 | 本轮判定 |
|---|---|---|---|
| T03-01 | 两平台分段来源、标称/可用带宽边界、A2 unknown、基线入口 | API 适用性、网卡身份/故障域、物理图、资产表和最小计划（C01–C04） | 暂不通过 |
| T03-02 | MR/PD/QP/CQ 主干、错误字段有效性、持久与 GPU 可见性边界 | 固定证据、IMM/完成映射、RoCE 模式、必交图和设计/隔离比较（C04–C08） | 暂不通过 |
| T03-03 | 隔离/争用框架、四分法、无虚构实测、not_verified | IB/RoCE 独立路径、计数器、NUMA、覆盖率及可执行设计（C04、C09–C12） | 暂不通过 |
| T03-04 | 保留 rank/次序/进度契约，理论与实现分层、部分原语及映射 | 有限 p 模型、六类图、冻结框架和逐消息映射（C13–C14）；标题修复（C15） | 暂不通过 |

建议先修版本/适用范围及机制事实（C01、C02、C04–C07、C11、C13），再补各任务图、表和验证判据（C03、C08–C10、C12、C14），最后核对链接/渲染（C15）。修订记录须逐项映射 B18-C01–C15，并同步相关研究记录、登记和 verification；本审阅者再按修订文件身份执行定向复核，记录 CLOSED/OPEN 及证据。报告交付、unknown 标注或结构校验本身不关闭发现。

## 检查与限制

- `make check`：PASS，86 篇内容、374 项来源；只检查结构及本地文件链接，不检查技术正确性或远端链接。
- `make build`：PASS，同一计数；已生成 `build/catalog.json` 和 `build/catalog.md`，未手工修改构建产物。
- 未改动 `src/kb/`；未添加内容镜像或实现同义测试。
- 本轮没有运行 GPU/NPU、verbs 程序、perftest、交换机配置、故障注入或硬件验证；未取得真实环境档案，未改变 draft 或 not_verified。
- 稳定 ID、主归属与章入口已核对；没有将本批任务状态、主题覆盖或未来实现升为完成。现有工作区 Batch 17 及本批作者未提交内容保留。
