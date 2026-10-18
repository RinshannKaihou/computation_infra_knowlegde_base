# 原设计 63 个主题的后续完整覆盖规划

规划日期：2026-10-08。沿用 9 个领域、63 个二级主题和现有稳定内容 ID，以 Batch 01–12 的覆盖盘点为基线。本文与 YAML 清单是规划产物，不增加正文覆盖率、来源核验数或实测完成数。

[逐项内容任务与批次](../plans/full-coverage-backlog.yaml)是执行清单；[补充来源工作包](../plans/followup-source-acquisition.yaml)与[独立验证工作包](../plans/validation-backlog.yaml)分别管理材料和真实证据。原始范围见[内容总目录](../content-outline.md)，当前完成情况见[覆盖盘点](topic-coverage-audit.md)。

## 交付范围与完成标准

本计划把原目录转成一个可验收的内容版本 v1。63 个主题逐项列明交付范围、平台样板、五方面要求、已有正文、补齐任务和关闭条件；“完整”指这些明确范围全部通过验收。它不表示所有机型、软件版本和任意现场组合都兼容，也不表示已经完成部署或实测。原目录中明确出现的 ROCm/RCCL、Slurm、后训练/rollout、服务控制等仍在本轮范围内；其他未命名平台依新增证据继续扩展。

每个主题总体回答原理与边界、设计与使用、观测与判断、故障与处置、验证与案例。五方面由相互链接的文章共同覆盖，不要求每篇文章重复五套章节。纯导航主题以阅读顺序、前置知识、任务目标、路径断点和导航核对验收。案例可以是有原始证据的上游案例，或明确标记的推演/反例；需要真实案例的任务无证据时保持待办，不能以合成例子替代。验证方法明确写出基线、对照、判据与无法判断条件；执行结果进入独立验证轨道。

平台与实现样板范围：

| 层次 | 本轮范围 | 使用边界 |
|---|---|---|
| 加速器 | NVIDIA/CUDA/NCCL、Ascend/CANN/HCCL；补 AMD/ROCm/HIP/RCCL 的明确分支 | 按任务选择有依据的硬件、软件和功能交集；generic 不表示兼容 |
| 物理与主机 | Linux 主机、CPU/NUMA/内存/I/O；已有 DGX/Atlas 样板及补充 AMD 资料；机柜/BMC/固件 | 通用机制和机型规格分开；Redfish 规范不等于每台设备实现 |
| 网络 | 节点内/节点间/超节点互联；Ethernet、IB、RoCE、verbs、拓扑、拥塞和基线 | 选定 NIC/固件/内核/驱动/工具与拓扑，不把一条链路结果推广到其他组合 |
| 存储 | Linux ext4/NVMe、Linux NFSv4.1、Ceph RGW/S3 接口、Lustre 四类代表实现 | 逐后端核对缓存、一致性、提交、持久性和恢复；S3 接口兼容不等于 AWS S3 语义 |
| 集群 | Kubernetes、Kueue、Volcano、MindCluster 与 Slurm 的职责、设备、作业、调度和生命周期 | 分别固定实现版本；同名调度或隔离功能不强行等价 |
| 训练 | PyTorch 共同状态/循环，Megatron/MindSpeed 平台实现；预训练、全量/参数高效微调、RL rollout 与权重同步 | 以真实官方材料和测试确认各实现责任；算法效果与系统正确性分开 |
| 推理 | vLLM、vLLM Ascend、MindIE；模型加载、量化、分布式/PD、路由、流控、扩缩容和发布恢复 | 引擎内机制与服务控制面分开；引擎/模型/硬件/功能交集按版本核查 |
| 可靠性 | 故障模型、证据关联、处置原则、正确性、测试选择、恢复损失、复盘、维护及独立评测方法 | 教学题、来源案例和真正保留集分别管理；缺测和不支持不转成正常 |

必须分开报告四种进度：

1. **规划完整性**：63 个主题和全部盘点缺口是否已分配任务；它只说明计划没有漏项。
2. **正文交付与覆盖**：新增/修订文件真实存在、主题五方面达到本轮范围后，重新盘点。任务 done 不自动把主题改为 covered。
3. **来源与审阅**：主张可追溯至精确来源、适用边界明确，批次审阅发现修订并定向复核通过。编辑状态按实际结果维护，历史 draft 不因排入计划而改变。
4. **真实证据**：环境档案、实验结果和独立评测素材实际获得并复核；方法或空模板不关闭真实证据缺口。

12 个基础已覆盖主题仍进入本轮有限范围复核/扩展。01.6 的真实验收环境、08.7 的实测结果、08.8 的独立诊断保留集等缺口保留验证任务；正文完整与证据完备分别验收。整项缺口只在相应轨道完成后关闭。

## 批次执行与来源入口

每批先做材料准备，再写作、审阅、修订、定向复核和构建。来源工作在所属批次内计入准备步骤，不另计文章数。每个任务已有目标文件、稳定 ID、问题、验收项和材料获取范围；导航任务核对已验收正文、路径目标和阅读次序，不强制新增外部来源。尚未固定的具体版本/页面不伪装成已核验资料。

进入写作前，选择与任务范围一致的 release/ref/commit 或可追溯页面版本，取得具体文档、实现和必要测试，登记精确来源与许可，形成主张—来源定位表。旧登记表的 source ID 只表示可复用入口，仍须核对本次新增主张。材料不足时标为 blocked_on_evidence，记录受阻范围和候选替代来源；unknown、独占模式或其他平台例子不能自动关闭本轮必交的共享模型/工具环境交集等子项；可推进不依赖该缺口的任务，不能将必交范围静默删除。

批次审阅沿用 **gpt-6.1-sol / xhigh**，由与写作分开的审阅角色检查技术主张、来源、版本/平台边界、元数据和导航。发现修订后做定向复核；开放高优先级问题未关闭时不声明通过。保存对应批次的来源审计、审阅、修订和复核记录；实际执行模型与角色如实记录。结构检查使用 `make check`、`make build`，只证明结构和引用。

每批最多 5 项内容任务、8 个相对工作量单位，任务按列出的顺序交付。单位 1 表示范围较小的文章/修订，单位 2 表示需要多个实现分支、来源案例或多目标文件的较大任务；单位不折算工时，也不表示技术风险。批内依赖按顺序处理，跨批依赖先通过相关验收。领域首页和现有路径的链接整合属于每批收尾；专门新增路径另列任务。

来源不足可改变实际完成顺序，但保留稳定任务 ID、依赖和基线批号。拆分/合并任务、改变本轮范围或增加批次时同步修改本文、YAML、主题映射和统计，并注明原因。每批末更新覆盖盘点；批次执行完仍需逐主题验收，不凭任务数量宣告完成。

具体等待条件见[批次依赖表、关系图与逐任务前置](batch-dependencies.md)，机器可读视图见[依赖清单](../plans/batch-dependencies.yaml)。整批前置表用于保守调度，独立任务可按自身前置和来源入口提前推进；Batch 14 不要求所有任务都等待 Batch 13。

## 批次与任务总量

本轮规划 **85 项内容任务、20 个后续批次（Batch 13–32）**；加上已交付的 12 批，当前基线合计 32 批。这是依赖与工作量拆分后的计划数，可随必要来源或任务范围变化调整。此前 20–30 个新增批次只是粗估，本表取代该估算。

任务操作数：新增 57 项、修订 21 项、导航 7 项。目标文件去重后预计新增 58 篇正文、8 个导航文件，修改 33 个已有正文或导航文件；任务数、文件数和主题数分别统计。

规划交付时所有任务和批次均为 planned；实际执行状态须由运行会话的真实交付与审阅记录更新，进入写作前仍须来源准备。七份既有方案执行状态仍为 0/7。

| Batch | 内容组合（按任务顺序） | 任务数 / 单位 |
|---|---|---|
| 13 | T00-01 统一术语、先修关系与系统责任边界；T01-01 机柜供电、散热预算与共享依赖；T01-02 供电散热观察的训练 NPU 补齐与设施告警关联；T01-03 NUMA、主机内存与 I/O 局部性及成对验证；T01-04 三平台执行单元、内存层次与数据移动机制 | 5 / 8 |
| 14 | T01-05 板卡到超节点的组成与拓扑约束扩展；T01-06 BMC、固件身份与跨层硬件事件；T01-07 三平台错误信息与健康覆盖映射；T01-08 节点选型、隔离返修、长期管理与退役 | 4 / 8 |
| 15 | T01-09 节点验收的环境档案和证据接入规范；T02-01 OS/进程资源压力与设备访问诊断；T02-02 驱动初始化、运行时执行同步与库装载；T02-03 两平台文档配套档案的完整约束交集核对 | 4 / 7 |
| 16 | T02-04 AMD ROCm 软件栈及文档样板档案；T02-05 CUDA、ROCm、CANN 三栈职责与能力对照；T02-06 算子分发、编译与计算图执行机制；T02-07 GPU 算子、编译和图执行失败的定向诊断 | 4 / 7 |
| 17 | T02-08 框架到设备后端的适配与能力核对；T02-09 GPU 分配器、保留内存与 OOM 证据；T02-10 dtype、layout、格式转换与有限精度语义；T02-11 Ascend 主机传输、stream 与同步证据补齐 | 4 / 7 |
| 18 | T03-01 节点内、节点间与超节点互联路径参考；T03-02 Ethernet、IB、RoCE 与 RDMA 机制；T03-03 RDMA 网络基线、路由与拥塞诊断；T03-04 扩展集合通信数据流、算法与工作负载映射 | 4 / 8 |
| 19 | T03-05 RCCL 运行条件、观测与最小验证档案；T03-06 三套通信库能力与版本条件档案；T03-07 扩展跨节点、rail 与拥塞性能基线口径；T03-08 带宽退化、通信热点与来源案例补齐；T04-01 扩展数据集身份、预处理、缓存与数据游标 | 5 / 7 |
| 20 | T04-02 本地与共享文件存储的版本化参考；T04-03 对象与并行存储的版本化参考；T04-04 模型制品与 Checkpoint 的传输、发布和读回；T04-05 扩展数据、制品与后端完整性校验证据 | 4 / 7 |
| 21 | T04-06 存储负载、容量与长尾基线口径；T04-07 存储客户端、后端异常与恢复验证；T04-08 对接后端基线与数据/Checkpoint 阶段诊断；T05-01 镜像制品、容器运行时与设备暴露基线 | 4 / 8 |
| 22 | T05-02 Kubernetes 作业全生命周期与控制器责任；T05-03 Slurm 作业生命周期、设备资源与状态参考；T05-04 扩展 GPU 与 Slurm 设备资源账本；T05-05 扩展 gang、配额和双平台调度策略 | 4 / 7 |
| 23 | T05-06 加速器共享与租户隔离机制；T05-07 多租户争用、公平性与容量验证；T05-08 节点摘除、drain 与资源回收流程；T05-09 平台组件升级、发布、回退与回服 | 4 / 8 |
| 24 | T05-10 控制面故障、平台恢复与账本核对；T06-01 补齐并行策略选择、专家并行与组合映射；T06-02 训练框架组件、执行循环与平台职责对照；T06-03 预训练与微调工作流和状态契约 | 4 / 7 |
| 25 | T06-04 RL rollout、权重同步与训练推理协同；T06-05 混合精度、算子适配与收敛验证；T06-06 训练性能分解、profiling 与优化验证；T06-07 训练吞吐回归的公开证据案例 | 4 / 7 |
| 26 | T06-08 核验恢复状态与弹性训练的 v1 边界；T07-01 权重加载、引擎 ready 与启动失败诊断；T07-02 推理引擎组件与平台功能交集档案；T07-03 MindIE 推理执行与配置样板 | 4 / 8 |
| 27 | T07-04 补齐量化、算子优化与支持冲突边界；T07-05 推理输出质量的对照评估方法与案例；T07-06 分布式推理布局与并行选择；T07-07 补齐 PD connector 前提、指标与失败链 | 4 / 7 |
| 28 | T07-08 请求路由、准入与流控；T07-09 容量、扩缩容与冷启动决策；T07-10 服务版本发布、副本故障与恢复验证；T07-11 GPU 推理 OOM 与状态恢复诊断；T00-02 单机、集群与超节点的参考架构及选择 | 5 / 8 |
| 29 | T00-03 容量、成本、能耗与可靠性目标的设计权衡；T08-01 故障模型、跨层传播与共享失效分析；T08-02 相关故障与冗余失效的公开案例；T08-03 隔离、重试预算、降级与恢复选择 | 4 / 7 |
| 30 | T08-04 补齐 SDC 检测、训练传播与平台证据；T08-05 统一测试选择、压力/注入与统计方法；T08-06 可靠性统计、有效产出与恢复损失；T08-07 事故复盘、来源更新与知识维护；T08-08 诊断评测方法与公开教学题组 | 5 / 8 |
| 31 | T06-09 训练主题的五方面入口与交付核对；T07-12 推理主题入口及缓存/SLO 最终边界核对；T02-12 三平台安装基线、迁移升级与回退验证；T00-04 训练与推理端到端路径的终态范围验收；T00-05 学习者、架构设计与运维角色阅读路径 | 5 / 6 |
| 32 | T00-06 选型、节点验收与环境安装任务路径；T08-09 可靠性主题五方面及状态边界核对；T00-07 性能优化、迁移升级与故障恢复任务路径；T00-08 三平台入口与现有排障路径的收口 | 4 / 4 |

## 63 个主题的交付范围与验收批次

表中批号是本轮正文范围的计划验收位置；独立验证完成另看 V 工作包。已有基础覆盖判断保留，不能因本表列满而提升完成率。各主题的完整平台边界、五方面、原缺口逐条映射与关闭条件在 YAML 的 topics 中。

| 主题 | 本轮交付范围 | 任务 / 正文验收批次 |
|---|---|---|
| **00.1 范围、核心术语与系统边界** | 统一系统术语、先修关系、职责边界和诊断入口；以原目录九领域为有限术语范围，不建立无限词典。 | T00-01 / Batch 13 |
| **00.2 一次训练任务的端到端路径** | 覆盖一轮训练从准入到保存/恢复及持续进展，并增加 pretrain/SFT/RL rollout 的入口；实现细节留主领域。 | T00-04 / Batch 31 |
| **00.3 一次推理请求的端到端路径** | 覆盖单次请求从入口到资源释放及错误/取消/副本恢复入口；用时钟和状态边界串联引擎与服务。 | T00-04 / Batch 31 |
| **00.4 单机、集群与超节点的参考架构** | 交付三种参考组织、控制/数据/管理路径、共同依赖、规模约束和选型核对方法，至少两种有官方组成依据的具体超节点样板。 | T00-02, T00-03 / Batch 29 |
| **00.5 设计目标与约束：可靠性、性能、容量、成本、能耗** | 以有限的成本/容量/能耗模型、测量口径和两项假设案例说明五类目标权衡及验收。 | T00-03 / Batch 29 |
| **00.6 按角色、任务与平台组织的阅读路径** | 提供三角色、八项任务（含已有训练/推理排障）及三平台的可达阅读路径，每条路径带先修、目标与完成检查。 | T00-05, T00-06, T00-07, T00-08 / Batch 32 |
| **01.1 机柜、供电、散热与故障域** | 机柜预算/散热机制、共享依赖、设施至设备证据链及有限容量/退化对照方法。 | T01-01, T01-02, T01-06 / Batch 14 |
| **01.2 CPU、NUMA、主机内存与 I/O** | Linux NUMA、主机内存、CPU/thread affinity 与 PCIe/NIC/NVMe 局部性机制，成对测量及故障区分方法。 | T01-03 / Batch 13 |
| **01.3 GPU/NPU 的执行单元、设备内存与数据移动** | 三平台各一有公开资料的硬件代际执行单元/内存层次与数据移动机制，配套有边界的传输/同步验证方法。 | T01-04, T02-11 / Batch 17 |
| **01.4 板卡、服务器、节点与超节点组成** | 板卡/模块/服务器/节点/超节点实体、资源和维护关系，两个具体超节点的组件/互联核对及故障域。 | T01-05 / Batch 14 |
| **01.5 BMC、固件、硬件健康与错误信息** | BMC/固件身份、事件/RAS/健康分类、三平台最小代表错误信息及带外/驱动/应用证据对齐。 | T01-02, T01-06, T01-07 / Batch 14 |
| **01.6 节点选型、验收与设备生命周期** | 节点需求/容量/成本选择、验收/隔离/返修/长期管理/退役和实际环境档案接入；真实验收档案独立由验证轨道交付。 | T01-08, T01-09 / Batch 15 |
| **02.1 OS、进程、主机资源与设备访问** | 固定 Linux 环境的调度/cgroup/内存/进程限制与设备访问机制，主机压力及权限的专项诊断/验证。 | T02-01 / Batch 15 |
| **02.2 驱动、运行时与基础库** | 驱动到 runtime 的初始化、stream/event/异步执行、基础库职责及加载身份，两现有平台样板的完整约束交集。 | T02-02, T02-03 / Batch 15 |
| **02.3 CUDA、ROCm、CANN 等平台软件栈** | 三栈组件/能力责任对照和三个独立样板档案，支持矩阵限所选硬件/软件字段与版本。 | T02-03, T02-04, T02-05 / Batch 16 |
| **02.4 算子、编译器、计算图与执行模式** | 算子分发、编译与图执行、形状/缓存/正确性和性能权衡，补齐 GPU 失败诊断与一项有依据的上游案例。 | T02-06, T02-07 / Batch 16 |
| **02.5 框架与设备后端适配** | 框架设备/算子/autograd/内存/编译与引擎插件的适配责任、三平台核对表和最小能力测试，包含一项其他框架对照。 | T02-08 / Batch 17 |
| **02.6 内存管理、数据格式与精度语义** | 三平台内存管理的对应机制/统计、dtype/layout/转换/计算精度与传输同步基础及有边界的验证。 | T02-09, T02-10, T02-11 / Batch 17 |
| **02.7 环境配套、安装验证、迁移与升级** | 三平台文档样板身份、完整安装验证梯子、迁移升级变化检查与回退门槛；实跑结果另行验证。 | T02-03, T02-04, T02-12 / Batch 31 |
| **03.1 节点内、节点间与超节点互联** | 解释节点内、节点间、超节点的物理互联和共享故障域，建立 NVIDIA 与 Ascend 的有限来源样板。; 给出路径图、选择/放置条件、拓扑观测、链路/热点候选检查与独立验证入口。 | T03-01, T03-03 / Batch 18 |
| **03.2 Ethernet、InfiniBand、RoCE 与 RDMA** | 完成 Ethernet/IB/RoCE/RDMA 协议、verbs/QP/CQ/MR 和完成/错误语义。; 为 Linux/NIC/交换机各选版本化资料，形成 IB/RoCE 独立基线、拥塞/配置异常与恢复验证方法。 | T03-02, T03-03 / Batch 18 |
| **03.3 拓扑、路由、拥塞与性能基线** | 建立实际物理路径、route/rail 与库测量层次映射。; 明确多租户争用/拥塞证据与跨节点、隔离/并发、消息大小基线矩阵及反例。 | T03-01, T03-03, T03-07, T03-08 / Batch 19 |
| **03.4 集合通信原理与通信模式** | 覆盖核心 collective/P2P 原语数据流、ring/tree 有假设的代价模型。; 将原语映射到 DP/TP/PP/EP 工作负载、观测、契约异常和正确性/性能验证。 | T03-04 / Batch 18 |
| **03.5 NCCL、RCCL、HCCL 等通信库** | 分别形成 NCCL、RCCL、HCCL 的接口、支持条件、初始化/完成/错误和观测/测试档案。; 固定所选样板资料；HCCL API、Test 与目标环境的版本交集必须独立判断，未知支持不补写。 | T03-05, T03-06, T03-07 / Batch 19 |
| **03.6 通信初始化、rank 映射与执行次序** | 维护已有通信域、rank/设备映射、调用/多组次序、进度/错误证据与两平台指南/案例/方案。; 加入 RCCL 独立契约入口并重新核对三库资料，使最终 v1 覆盖范围可追踪。 | T03-04, T03-05, T03-06 / Batch 19 |
| **03.7 超时、链路退化、通信热点与验证** | 覆盖超时、物理路径退化、热点/拥塞与库/网络/主机候选原因的区分。; 复用已有两个超时专题，补齐独立网络证据、一个上游退化案例与隔离/路径/争用对照方法。 | T03-03, T03-05, T03-07, T03-08 / Batch 19 |
| **04.1 数据集、预处理、加载与缓存** | 覆盖数据集/样本身份、变换、采样、多 worker/预取/缓存与恢复数据游标。; GPU/NPU 传输各自取证，补齐数据正确性、缓存失效和阶段等待的观察/诊断/验证。 | T04-01, T04-08 / Batch 21 |
| **04.2 本地、共享、对象与并行存储** | 四类存储采用 Linux ext4/NVMe、Linux NFSv4.1、Ceph RGW/S3、Lustre 代表实现，每项绑定版本化材料。; 比较接口、缓存、一致性、持久性、容量与选型，提供独立基线、诊断、恢复/校验方法。 | T04-02, T04-03, T04-06, T04-07 / Batch 21 |
| **04.3 模型与 Checkpoint 的读写、传输和持久化** | 覆盖模型/Checkpoint 文件集合身份、暂存/传输/发布提交/持久化/读回与失败清理。; 复用 DCP/MindIO 写入与既有慢 I/O 指南；增加 NFS/RGW 语义与选定后端验证，引擎 ready 留给 07.1。 | T04-02, T04-03, T04-04, T04-06, T04-08 / Batch 21 |
| **04.4 数据与文件完整性、版本和一致性** | 串联数据/模型/Checkpoint 的内容身份、版本、端到端校验与应用一致性。; 区分 checksum/ETag/version/signature、scrub/读路径检查和训练状态验证，补齐四类代表后端条件与反例。 | T04-01, T04-03, T04-04, T04-05, T04-07 / Batch 21 |
| **04.5 I/O 性能、数据饥饿与长尾** | 给出四类后端独立负载/容量/元数据/缓存/争用/长尾基线口径。; 关联客户端→后端→worker/队列→传输/消费和 Checkpoint 各阶段的计时证据，验证处置时同时检查正确性与性能。 | T04-02, T04-03, T04-06, T04-08 / Batch 21 |
| **04.6 存储异常、恢复与验证** | 区分挂载/客户端/后端可用性、降级/损坏和应用恢复状态错误。; 在四类实现资料支持范围内给出恢复条件、风险/停止/回服与故障域验证设计，保留一项官方案例/测试。 | T04-02, T04-03, T04-05, T04-07, T04-08 / Batch 21 |
| **05.1 容器、镜像、设备暴露与运行环境** | 覆盖镜像构建/制品身份、OCI/containerd、GPU CDI/toolkit 与 Ascend runtime/plugin 的暴露/权限/隔离职责。; 给出分别固定的运行环境清单、观测/异常、对照和已有案例入口；镜像和主机兼容独立判断。 | T05-01, T05-04, T05-06 / Batch 23 |
| **05.2 Kubernetes、Slurm 等平台与作业生命周期** | 分别覆盖 Kubernetes Job/Pod/Kueue 与 Slurm Job/Step 生命周期、控制器/daemon 责任、退出/重试/取消与清理。; 从提交到应用进展及资源回收形成状态/证据/诊断/验证闭环，术语不机械等同。 | T05-02, T05-03, T05-05, T05-08, T05-10 / Batch 24 |
| **05.3 设备发现、分配、健康上报与资源账本** | 保留现有 Kubernetes/Ascend 设备发现、健康、分配和账本链条。; 扩展 NVIDIA Plugin/CDI 与 Slurm GRES 独立视图，完成映射/健康变化/回收/平台恢复后校验的最终 v1 维护验收。 | T05-03, T05-04, T05-06, T05-08, T05-10 / Batch 24 |
| **05.4 配额、排队、gang、放置与拓扑亲和性** | 覆盖配额/排队/gang/准入/放置/拓扑，增加组启动失败/回退机制与有限配置策略例子。; Kubernetes/Kueue/Volcano/MindCluster 和 Slurm 两条路径分别说明观测、公平性/碎片权衡、异常与验证。 | T05-03, T05-05, T05-07 / Batch 23 |
| **05.5 多租户、隔离、资源争用与容量管理** | 覆盖设备独占与 NVIDIA MIG/MPS/time slicing、Ascend 可核查共享模式及租户/主机/网络/存储边界。; 建立争用/公平性/容量准入观察与两租户对照、来源案例/反例；未证实 NPU 隔离保证保留未知。 | T05-01, T05-05, T05-06, T05-07 / Batch 23 |
| **05.6 节点上下线、升级、发布与变更** | 分别定义 Kubernetes 和 Slurm 节点上下线、停止准入/drain/资源回收/重新准入。; 补齐组件版本变更、发布波次、失败停发/回退和跨层回服验收，真实演练单独推进。 | T05-02, T05-03, T05-08, T05-09 / Batch 23 |
| **05.7 调度失败、控制面异常与集群恢复** | 从调度/等待问题扩展到 Kubernetes API/etcd/控制器与 Slurm controller/worker/database 的故障。; 给出状态/证据分支、备份/恢复/作业重建风险、账本校验与应用持续进展验收。 | T05-02, T05-03, T05-04, T05-08, T05-09, T05-10 / Batch 24 |
| **06.1 训练计算过程与状态：权重、梯度、优化器、数据进度** | 训练 step、累积/更新/overflow 与状态提交；权重、梯度、optimizer/scheduler/scaler/RNG/数据及并行身份责任和完整 step 恢复契约。有限 v1 不承诺任意算法或 mid-step 无损恢复。 | T06-01, T06-08, T06-09 / Batch 31 |
| **06.2 数据、张量、流水线、专家等并行策略** | DP/ZeRO/FSDP/TP/PP/EP/CP/SP 的机制、状态与通信、规模效率/内存/负载选择，组合 mesh/group/stage/expert 映射和验证。按三组实现边界对照，不遍历所有模型配置。 | T06-01, T06-06, T06-09 / Batch 31 |
| **06.3 训练框架与执行：框架通用机制及平台实现** | PyTorch 训练 loop/autograd/分布式/编译及 NVIDIA Megatron、Ascend MindSpeed 的职责与接口；AMD PyTorch/ROCm 后端的支持条件和限制；固定文档档案与执行路径验证。 | T06-02, T06-09 / Batch 31 |
| **06.4 预训练、微调、强化学习与 rollout** | 预训练/继续预训练/全参 SFT/PEFT，以及 PPO/GRPO 在线 RL 与 DPO 离线对照；rollout/actor/reference/reward/learner 的权重版本、数据、状态/吞吐一致性；同步和一个受控异步实现样板。 | T06-03, T06-04, T06-09 / Batch 31 |
| **06.5 算子适配、混合精度、数值行为与收敛** | 算子/融合/编译适配、FP32/FP16/BF16/autocast/accumulation/loss scale，首差异/传播/有限窗口收敛和任务质量的对照方法；至少一个可追溯质量案例。 | T06-05, T06-09 / Batch 31 |
| **06.6 性能分析、慢 rank、资源不均与吞吐退化** | 固定有效产出口径的性能关键路径、分 rank/阶段 profiling、PP/EP/长度偏斜和吞吐优化；版本化 NVIDIA/Ascend/AMD 工具边界及一例公开性能回归。 | T06-06, T06-07, T06-09 / Batch 31 |
| **06.7 Checkpoint 状态、一致性、容错与弹性恢复** | 完整 step 的恢复点、checkpoint 状态/身份/布局、应用数据进度、DCP 受支持重分片、torchrun 与 MindSpeed 固定弹性样板及失败回退；未公开 NPU 内部协议不发明。 | T06-08, T06-09 / Batch 31 |
| **06.8 恢复后的正确性与持续进展验证** | 恢复身份/结构、逻辑进度、离散/浮点状态、同输入单步与持续训练窗口；旧新布局与样本重放/遗漏的验证方法，复用 CPU DCP 和精度方案。 | T06-08, T06-09 / Batch 31 |
| **07.1 模型加载、prefill、decode 与执行路径** | 权重/tokenizer/config/格式/分片加载、引擎初始化/profiling/编译/warmup 到 ready，再连接 prefill/decode/请求结束；失败清理和确定输入验证，明确权重与 KV 不同。 | T07-01, T07-03, T07-12 / Batch 31 |
| **07.2 推理引擎及平台后端** | vLLM 上游/Ascend 和 MindIE 的 frontend/scheduler/executor/worker/KV/backend 职责；NVIDIA/CUDA、AMD/ROCm、Ascend/CANN 的模型/硬件/功能交集和已知限制文档档案。 | T07-02, T07-03, T07-12 / Batch 31 |
| **07.3 Batch、KV cache、内存与缓存管理** | batch/迭代调度、KV 容量/身份/引用/抢占/重算/驱逐、prefix cache 与内存压力；保持既有 vLLM/Ascend 实现完整性并加入 MindIE/ROCm 有证据的区别。 | T07-02, T07-03, T07-12 / Batch 31 |
| **07.4 量化、算子优化与输出质量验证** | 权重/激活/KV 量化、dtype/累加与 kernel/融合路径、硬件支持冲突；同输入数值与任务输出质量/性能评估、一个来源质量案例，支持条件按引擎/版本分开。 | T07-04, T07-05, T07-12 / Batch 31 |
| **07.5 分布式推理、PD 分离与通信依赖** | TP/PP/DP/EP 的布局、选型和观测，PD P/D/KV/connector/外部代理的职责、跨机前提/指标/完整失败链，vLLM NVIDIA/ROCm、Ascend 与 MindIE 分别取证。 | T07-06, T07-07, T07-03, T07-12 / Batch 31 |
| **07.6 路由、流控、扩缩容与版本发布** | 路由/亲和/负载感知、请求准入/预算/背压/取消/重试，容量与冷启动/扩缩容，以及灰度/发布/drain/回退/服务验证；一个固定服务控制实现样板。 | T07-08, T07-09, T07-10, T07-12 / Batch 31 |
| **07.7 TTFT、TPOT、吞吐、长尾与服务 SLO** | TTFT/TPOT/ITL/E2E/吞吐/goodput、成功/失败/取消分母、负载身份和尾分位不确定性、SLO/质量联合验收；既有长尾来源/方法与新增服务控制相连。 | T07-09, T07-10, T07-12 / Batch 31 |
| **07.8 OOM、请求失败、副本故障与服务恢复** | Ascend/NVIDIA/AMD 后端启动/执行 OOM、engine/worker/副本故障和请求失败，健康摘除/重试、KV/进程/请求状态清理与服务恢复持续窗口。 | T07-08, T07-10, T07-11, T07-12 / Batch 31 |
| **08.1 可用性、正确性、性能稳定性与可恢复性** | 四维目标、观察对象/分母/窗口/恢复门槛，连接处置选择、测试覆盖和有效产出/恢复损失；概念和合成计算例，不承诺现场达标。 | T08-03, T08-05, T08-06, T08-09 / Batch 32 |
| **08.2 故障模型、故障域、传播与相关故障** | 系统故障分类、共享故障域/跨层传播图与有限 FMEA/故障树，冗余独立性/隔离假设的观察和验证，以及一篇相关故障来源案例。 | T08-01, T08-02, T08-09 / Batch 32 |
| **08.3 可观测性、时间线与跨层证据关联** | 症状/事件/观测/假设/结论，实体/工作键/时间对齐、采集质量/覆盖和跨层 timeline；通过测试/复盘规范保留证据和观测缺失，不要求部署采集系统。 | T08-05, T08-07, T08-09 / Batch 32 |
| **08.4 故障发现、假设检验、归因与下一项检查** | 支持/反驳/未知假设与有区分力的下一检查；代价/影响/停止和恢复判据；接入复盘与独立冻结评测方法，避免把规则命中当根因。 | T08-05, T08-07, T08-08, T08-09 / Batch 32 |
| **08.5 隔离、冗余、重试、降级与恢复原则** | 隔离/冗余/重试/降级/恢复的跨领域选择流程、预算/幂等/重放/流式边界与失败模式，一篇冗余失效案例和有限验证方法。 | T08-01, T08-02, T08-03, T08-09 / Batch 32 |
| **08.6 数值异常、静默错误与计算完整性的判定方法** | 数值噪声/软硬件/数据错误与 SDC 候选的分层判定；训练传播、检测覆盖/成本/假阴性/误报、原始检测研究和 NPU 证据清单；无充分公开证据保持未知。 | T08-04, T08-05, T08-09 / Batch 32 |
| **08.7 验收、基准、压力测试与故障注入方法** | 验收/benchmark/stress/故障注入的对象/覆盖/前提/预算/停止/恢复和统计方法，七份既有方案准备矩阵。真实环境结果是独立证据目标，正文完成不关闭该目标。 | T08-05, T08-09 / Batch 32 |
| **08.8 可靠性指标、恢复损失、事故复盘与知识更新** | 长期可靠性与有效产出/重算/重放/恢复损失统计，事故复盘→来源/正文修订→复核的维护方法；独立评测规范和公开教学/检索回归题组。真正独立材料/答案的外置隔离由 V12 管理，当前证据 gap 保持 open。 | T08-06, T08-07, T08-08, T08-09 / Batch 32 |

## 任务索引

具体目标、来源获取范围、验收条目和前置任务见 YAML 的 tasks；下表便于找到对应目标。planned_new 路径尚不存在，不提前创建空文章。

| 任务 | 操作 / Batch | 目标文件 |
|---|---|---|
| T00-01 统一术语、先修关系与系统责任边界 | 新增 / 13 | `knowledge/00-overview/terms-and-system-boundaries.md` |
| T01-01 机柜供电、散热预算与共享依赖 | 新增 / 13 | `knowledge/01-hardware/rack-power-cooling-and-failure-domains.md` |
| T01-02 供电散热观察的训练 NPU 补齐与设施告警关联 | 修订 / 13 | `knowledge/01-hardware/power-thermal-evidence.md` |
| T01-03 NUMA、主机内存与 I/O 局部性及成对验证 | 新增 / 13 | `knowledge/01-hardware/numa-memory-and-io-locality.md` |
| T01-04 三平台执行单元、内存层次与数据移动机制 | 新增 / 13 | `knowledge/01-hardware/accelerator-execution-and-data-movement.md` |
| T01-05 板卡到超节点的组成与拓扑约束扩展 | 修订 / 14 | `knowledge/01-hardware/resource-topology.md` |
| T01-06 BMC、固件身份与跨层硬件事件 | 新增 / 14 | `knowledge/01-hardware/bmc-firmware-and-events.md` |
| T01-07 三平台错误信息与健康覆盖映射 | 修订 / 14 | `knowledge/01-hardware/health-evidence.md` |
| T01-08 节点选型、隔离返修、长期管理与退役 | 新增 / 14 | `knowledge/01-hardware/node-selection-and-lifecycle.md` |
| T01-09 节点验收的环境档案和证据接入规范 | 修订 / 15 | `knowledge/01-hardware/node-acceptance-triage.md` |
| T02-01 OS/进程资源压力与设备访问诊断 | 新增 / 15 | `knowledge/02-software-stack/host-resource-pressure-and-device-access.md` |
| T02-02 驱动初始化、运行时执行同步与库装载 | 新增 / 15 | `knowledge/02-software-stack/runtime-execution-and-library-loading.md` |
| T02-03 两平台文档配套档案的完整约束交集核对 | 修订 / 15 | `knowledge/02-software-stack/ascend-documented-profile.md`；`knowledge/02-software-stack/nvidia-documented-profile.md`；`knowledge/02-software-stack/compatibility-evidence.md` |
| T02-04 AMD ROCm 软件栈及文档样板档案 | 新增 / 16 | `knowledge/02-software-stack/amd-rocm-documented-profile.md` |
| T02-05 CUDA、ROCm、CANN 三栈职责与能力对照 | 修订 / 16 | `knowledge/02-software-stack/layers-and-boundaries.md` |
| T02-06 算子分发、编译与计算图执行机制 | 新增 / 16 | `knowledge/02-software-stack/operators-compilers-and-graphs.md` |
| T02-07 GPU 算子、编译和图执行失败的定向诊断 | 新增 / 16 | `knowledge/02-software-stack/gpu-op-graph-failure-triage.md` |
| T02-08 框架到设备后端的适配与能力核对 | 新增 / 17 | `knowledge/02-software-stack/framework-backend-adaptation.md` |
| T02-09 GPU 分配器、保留内存与 OOM 证据 | 新增 / 17 | `knowledge/02-software-stack/gpu-memory-oom-evidence.md` |
| T02-10 dtype、layout、格式转换与有限精度语义 | 新增 / 17 | `knowledge/02-software-stack/dtype-layout-and-precision-semantics.md` |
| T02-11 Ascend 主机传输、stream 与同步证据补齐 | 修订 / 17 | `knowledge/02-software-stack/ascend-memory-oom-evidence.md` |
| T03-01 节点内、节点间与超节点互联路径参考 | 新增 / 18 | `knowledge/03-communication/interconnect-paths.md` |
| T03-02 Ethernet、IB、RoCE 与 RDMA 机制 | 新增 / 18 | `knowledge/03-communication/ethernet-ib-roce-rdma.md` |
| T03-03 RDMA 网络基线、路由与拥塞诊断 | 新增 / 18 | `knowledge/03-communication/rdma-baseline-and-congestion-triage.md` |
| T03-04 扩展集合通信数据流、算法与工作负载映射 | 修订 / 18 | `knowledge/03-communication/collectives-and-rank-progress.md` |
| T03-05 RCCL 运行条件、观测与最小验证档案 | 新增 / 19 | `knowledge/03-communication/rccl-runtime-and-verification.md` |
| T03-06 三套通信库能力与版本条件档案 | 新增 / 19 | `knowledge/03-communication/communication-library-profiles.md` |
| T03-07 扩展跨节点、rail 与拥塞性能基线口径 | 修订 / 19 | `knowledge/03-communication/bandwidth-baselines.md` |
| T03-08 带宽退化、通信热点与来源案例补齐 | 修订 / 19 | `knowledge/03-communication/bandwidth-degradation-triage.md` |
| T04-01 扩展数据集身份、预处理、缓存与数据游标 | 修订 / 19 | `knowledge/04-data-storage/training-data-path.md` |
| T04-02 本地与共享文件存储的版本化参考 | 新增 / 20 | `knowledge/04-data-storage/local-and-shared-storage.md` |
| T04-03 对象与并行存储的版本化参考 | 新增 / 20 | `knowledge/04-data-storage/object-and-parallel-storage.md` |
| T04-04 模型制品与 Checkpoint 的传输、发布和读回 | 新增 / 20 | `knowledge/04-data-storage/artifact-transfer-and-publication.md` |
| T04-05 扩展数据、制品与后端完整性校验证据 | 修订 / 20 | `knowledge/04-data-storage/checkpoint-integrity-evidence.md` |
| T04-06 存储负载、容量与长尾基线口径 | 新增 / 21 | `knowledge/04-data-storage/storage-workload-baselines.md` |
| T04-07 存储客户端、后端异常与恢复验证 | 新增 / 21 | `knowledge/04-data-storage/storage-client-backend-recovery.md` |
| T04-08 对接后端基线与数据/Checkpoint 阶段诊断 | 修订 / 21 | `knowledge/04-data-storage/data-starvation-triage.md`；`knowledge/04-data-storage/checkpoint-slow-io-triage.md` |
| T05-01 镜像制品、容器运行时与设备暴露基线 | 新增 / 21 | `knowledge/05-cluster-platform/container-image-runtime-baseline.md` |
| T05-02 Kubernetes 作业全生命周期与控制器责任 | 新增 / 22 | `knowledge/05-cluster-platform/kubernetes-job-lifecycle.md` |
| T05-03 Slurm 作业生命周期、设备资源与状态参考 | 新增 / 22 | `knowledge/05-cluster-platform/slurm-jobs-and-device-resources.md` |
| T05-04 扩展 GPU 与 Slurm 设备资源账本 | 修订 / 22 | `knowledge/05-cluster-platform/device-resource-chain.md` |
| T05-05 扩展 gang、配额和双平台调度策略 | 修订 / 22 | `knowledge/05-cluster-platform/admission-and-placement.md` |
| T05-06 加速器共享与租户隔离机制 | 新增 / 23 | `knowledge/05-cluster-platform/accelerator-sharing-and-isolation.md` |
| T05-07 多租户争用、公平性与容量验证 | 新增 / 23 | `knowledge/05-cluster-platform/contention-capacity-validation.md` |
| T05-08 节点摘除、drain 与资源回收流程 | 新增 / 23 | `knowledge/05-cluster-platform/node-drain-resource-reclamation.md` |
| T05-09 平台组件升级、发布、回退与回服 | 新增 / 23 | `knowledge/05-cluster-platform/platform-change-and-rollback.md` |
| T05-10 控制面故障、平台恢复与账本核对 | 新增 / 24 | `knowledge/05-cluster-platform/control-plane-recovery.md` |
| T06-01 补齐并行策略选择、专家并行与组合映射 | 修订 / 24 | `knowledge/06-training/parallelism-and-state.md` |
| T06-02 训练框架组件、执行循环与平台职责对照 | 新增 / 24 | `knowledge/06-training/framework-execution.md` |
| T06-03 预训练与微调工作流和状态契约 | 新增 / 24 | `knowledge/06-training/pretraining-and-finetuning.md` |
| T06-04 RL rollout、权重同步与训练推理协同 | 新增 / 25 | `knowledge/06-training/rl-rollout-consistency.md` |
| T06-05 混合精度、算子适配与收敛验证 | 新增 / 25 | `knowledge/06-training/mixed-precision-and-convergence.md` |
| T06-06 训练性能分解、profiling 与优化验证 | 新增 / 25 | `knowledge/06-training/performance-analysis.md` |
| T06-07 训练吞吐回归的公开证据案例 | 新增 / 25 | `knowledge/06-training/performance-regression-source-case.md` |
| T06-08 核验恢复状态与弹性训练的 v1 边界 | 修订 / 26 | `knowledge/06-training/checkpoint-state-consistency.md`；`knowledge/06-training/elastic-training-and-membership.md` |
| T07-01 权重加载、引擎 ready 与启动失败诊断 | 新增 / 26 | `knowledge/07-inference/model-loading-and-readiness.md` |
| T07-02 推理引擎组件与平台功能交集档案 | 新增 / 26 | `knowledge/07-inference/engine-backend-boundaries.md` |
| T07-03 MindIE 推理执行与配置样板 | 新增 / 26 | `knowledge/07-inference/mindie-execution-profile.md` |
| T07-04 补齐量化、算子优化与支持冲突边界 | 修订 / 27 | `knowledge/07-inference/quantization-and-quality.md` |
| T07-05 推理输出质量的对照评估方法与案例 | 新增 / 27 | `knowledge/07-inference/output-quality-evaluation.md` |
| T07-06 分布式推理布局与并行选择 | 新增 / 27 | `knowledge/07-inference/distributed-inference-layouts.md` |
| T07-07 补齐 PD connector 前提、指标与失败链 | 修订 / 27 | `knowledge/07-inference/pd-disaggregation.md` |
| T07-08 请求路由、准入与流控 | 新增 / 28 | `knowledge/07-inference/routing-and-flow-control.md` |
| T07-09 容量、扩缩容与冷启动决策 | 新增 / 28 | `knowledge/07-inference/capacity-and-autoscaling.md` |
| T07-10 服务版本发布、副本故障与恢复验证 | 新增 / 28 | `knowledge/07-inference/release-and-recovery.md` |
| T07-11 GPU 推理 OOM 与状态恢复诊断 | 新增 / 28 | `knowledge/07-inference/gpu-inference-oom-triage.md` |
| T00-02 单机、集群与超节点的参考架构及选择 | 新增 / 28 | `knowledge/00-overview/reference-architectures.md` |
| T00-03 容量、成本、能耗与可靠性目标的设计权衡 | 新增 / 29 | `knowledge/00-overview/design-targets-and-tradeoffs.md` |
| T08-01 故障模型、跨层传播与共享失效分析 | 新增 / 29 | `knowledge/08-reliability/fault-models-and-propagation.md` |
| T08-02 相关故障与冗余失效的公开案例 | 新增 / 29 | `knowledge/08-reliability/correlated-failure-source-case.md` |
| T08-03 隔离、重试预算、降级与恢复选择 | 新增 / 29 | `knowledge/08-reliability/mitigation-and-recovery-principles.md` |
| T08-04 补齐 SDC 检测、训练传播与平台证据 | 修订 / 30 | `knowledge/08-reliability/silent-errors-and-integrity.md` |
| T08-05 统一测试选择、压力/注入与统计方法 | 新增 / 30 | `knowledge/08-reliability/test-design-and-coverage.md` |
| T08-06 可靠性统计、有效产出与恢复损失 | 新增 / 30 | `knowledge/08-reliability/reliability-metrics-and-recovery-loss.md` |
| T08-07 事故复盘、来源更新与知识维护 | 新增 / 30 | `knowledge/08-reliability/postmortem-and-knowledge-update.md` |
| T08-08 诊断评测方法与公开教学题组 | 新增 / 30 | `knowledge/08-reliability/diagnostic-evaluation-method.md`；`knowledge/08-reliability/diagnostic-evaluation-fixtures.md` |
| T06-09 训练主题的五方面入口与交付核对 | 导航 / 31 | `knowledge/06-training/index.md` |
| T07-12 推理主题入口及缓存/SLO 最终边界核对 | 导航 / 31 | `knowledge/07-inference/index.md` |
| T02-12 三平台安装基线、迁移升级与回退验证 | 新增 / 31 | `knowledge/02-software-stack/environment-installation-and-upgrade.md` |
| T00-04 训练与推理端到端路径的终态范围验收 | 修订 / 31 | `knowledge/00-overview/training-lifecycle.md`；`knowledge/00-overview/inference-lifecycle.md` |
| T00-05 学习者、架构设计与运维角色阅读路径 | 导航 / 31 | `paths/roles/reading-by-role.md` |
| T00-06 选型、节点验收与环境安装任务路径 | 导航 / 32 | `paths/tasks/selection-and-capacity.md`；`paths/tasks/node-acceptance.md`；`paths/tasks/environment-installation.md` |
| T08-09 可靠性主题五方面及状态边界核对 | 导航 / 32 | `knowledge/08-reliability/index.md` |
| T00-07 性能优化、迁移升级与故障恢复任务路径 | 导航 / 32 | `paths/tasks/performance-optimization.md`；`paths/tasks/migration-and-upgrade.md`；`paths/tasks/fault-recovery.md` |
| T00-08 三平台入口与现有排障路径的收口 | 导航 / 32 | `paths/platforms/amd.md`；`paths/platforms/ascend.md`；`paths/platforms/nvidia.md`；`paths/tasks/training-triage.md`；`paths/tasks/inference-triage.md` |

## 独立验证工作

验证清单包含 13 个工作包：一项共同准备、七份既有验证方案，以及节点验收、RDMA、存储、隔离/变更/服务恢复和独立案例评估。它们不增加内容 Batch 数；资源、实际授权范围和证据当前均未取得/未记录，不承诺日历日期。V00 按每个验证包/子组分别准备；既有七份方案按自身实际前置推进，不等待无关平台或全部正文。CPU Checkpoint 基础组无需 Ceph/Lustre，单引擎服务组无需其他引擎，扩展组单独验收。

| 验证包 | 工作 | 条件与证据边界 |
|---|---|---|
| V00 | 真实环境与证据准备 | 所有后续验证共同准备；GPU/NPU/网络/存储/调度资源当前未知；环境、脚本、输入与操作范围可审阅；缺项逐条保留，未执行时不生成 reproduced |
| V01 | 昇腾版本配套验证 | 独立 NPU 节点与可回退软件制品；基线、单变量对照、恢复及重复证据完整，按预先判据记录假设得到支持、被反驳或无法判断；无差异不能证明全面兼容。 |
| V02 | 设备可见性与资源分配链验证 | 独立 NPU/Kubernetes/plugin/runtime 环境；区分无资源、无访问、映射错误与框架错误；回收和恢复有证据 |
| V03 | HCCL 超时验证 | 隔离多 NPU；跨节点问题另需对应网络；所有参与者结果完整；区分等待症状和最早异常，结果允许无法判断 |
| V04 | NCCL 超时验证 | 隔离多 GPU/NIC；跨节点另需对应网络；未出 RAS outlier 不作为无异常结论；可区分早退、错序与传输证据缺口 |
| V05 | GPU/NPU 精度差异验证 | 各一个独立 GPU 与 NPU 样板环境；指标、容差和样本量预先固定；允许噪声、明确差异和无法判断，不要求默认逐 bit 相同 |
| V06 | Checkpoint 恢复状态验证 | CPU 可先开始；多 rank 后续按环境补齐；状态加载、应用映射与持续进展都有证据；新优化器 placeholder 不得掩盖 missing branch |
| V07 | 昇腾推理长尾验证 | 独立 NPU 服务与负载客户端；p99 不确定性与不足样本明确记录；延迟改善同时检验失败率、质量和资源条件 |
| V08 | 新节点/返修节点真实验收档案 | 独立验收节点与管理/诊断访问；当前尚未取得；有真实环境和结果引用；模板、厂商规格与上游案例不能关闭 01.6 实测 gap |
| V09 | 跨节点网络与 RDMA 样板验证 | 独立跨节点 RDMA 网络及对等端点；配置、数据路径、计数器和性能证据一致；无法采集层不做因果推断 |
| V10 | 存储后端读写、提交与恢复样板验证 | 独立测试数据和后端资源；四类环境到位顺序未知；每后端分别记录成功/失败/无法判断，不能把一个后端结果推广到其余实现 |
| V11 | 租户隔离、节点变更与服务恢复验证 | 独立 Kubernetes 或 Slurm 环境及相应服务；不默认生产操作；调度成功不能代替租户隔离；新副本 ready 不能代替请求恢复和正确性 |
| V12 | 独立诊断案例集与方法评估 | 有授权且可脱敏的独立案例及评测资源；正文中的公开/合成教学题不能自动成为独立保留集；无真实独立材料保留缺证据，不虚构分数 |

## 续作入口与范围变化

**Batch 13 已于 2026-10-08 交付并通过验收**：T00-01 统一术语、先修关系与系统责任边界；T01-01 机柜供电、散热预算与共享依赖；T01-02 供电散热观察的训练 NPU 补齐与设施告警关联；T01-03 NUMA、主机内存与 I/O 局部性及成对验证；T01-04 三平台执行单元、内存层次与数据移动机制。来源准备、写作、`gpt-6.1-sol / xhigh` 审阅、修订与两轮定向复核（初审 15 项 + 复核新增 3 项全部关闭）、`make check`/`make build`（73 content entries / 119 sources）均完成；00.1、01.2 经主题范围复核升为已覆盖（基础），01.1-G1/G3 与 01.3-G1/G2 缺口关闭。交付与审阅记录见 [batch-13-source-audit](research/batch-13-source-audit.md)、[初审](research/batch-13-codex-review.md)与[定向复核](research/batch-13-codex-recheck.md)。

**Batch 14 已于 2026-10-09 交付并通过验收**：T01-05 板卡到超节点的组成与拓扑约束扩展；T01-06 BMC、固件身份与跨层硬件事件；T01-07 三平台错误信息与健康覆盖映射；T01-08 节点选型、隔离返修、长期管理与退役。`gpt-6.1-sol / xhigh` 审阅、修订与三轮定向复核完成，15 项发现（B14-C01–C15）全部关闭，其中 C10 以「编写者核对记录、未独立核验」限定口径关闭（iBMC 告警码保留证据链边界）；来源登记 123→163（新增 40 项、3 项取证不足未登记）；01.1、01.4、01.5 经主题范围复核升为已覆盖（基础）；01.1-G2、01.4-G1/G2、01.5-G1/G2/G3 与 01.6-G1/G2 缺口关闭（01.6 主题验收属 Batch 15）。交付与审阅记录见 [batch-14-source-audit](research/batch-14-source-audit.md)、[初审](research/batch-14-codex-review.md)、[修订](research/batch-14-review-fixes.md)与[定向复核](research/batch-14-codex-recheck.md)（[第二轮](research/batch-14-codex-recheck-round-2.md)、[第三轮](research/batch-14-codex-recheck-round-3.md)）。

**Batch 15 已于 2026-10-09 交付并通过验收**：T01-09 节点验收的环境档案和证据接入规范；T02-01 OS/进程资源压力与设备访问诊断；T02-02 驱动初始化、运行时执行同步与库装载；T02-03 两平台文档配套档案的完整约束交集核对。`gpt-6.1-sol / xhigh` 审阅、修订与两轮定向复核完成，8 项发现（B15-C01–C08）全部关闭，其中 C06 以「编写者核对记录、未独立核验」限定口径关闭（NVSM 示例图像内容保留证据链边界，同 Batch 14 C10 先例）；来源登记 163→210（新增 47 项，另有 open(2)/seccomp(2) 2 项于复核后补登至 212，Batch 16 并行交付后全仓库 277）；01.6、02.1、02.2 经主题范围复核升为已覆盖（基础），02.1-G1/G2、02.2-G1/G2/G3 与 02.3-G3 缺口关闭（01.6-G3 仍属 V08，02.3 主题验收属 Batch 16）。交付与审阅记录见 [batch-15-source-audit](research/batch-15-source-audit.md)、[初审](research/batch-15-codex-review.md)、[修订](research/batch-15-review-fixes.md)与[定向复核](research/batch-15-codex-recheck.md)（[第二轮](research/batch-15-codex-recheck-round-2.md)）。

**Batch 16 已于 2026-10-09 交付并通过验收**：T02-04 AMD ROCm 软件栈文档样板档案（ROCm Core SDK 10.1.0 × MI300X × Ubuntu 24.04.5 × amdgpu 31.60.0）；T02-05 CUDA/ROCm/CANN 三栈职责与能力对照（分层正文修订）；T02-06 算子分发、编译与计算图执行机制；T02-07 GPU 算子、编译和图执行失败的定向诊断（含 T02-06 回填互链）。`gpt-6.1-sol / xhigh` 审阅、修订与两轮定向复核完成，7 项发现（B16-C01–C07：初审 5 项含 1 P1 + 复核新增 C06/C07）全部关闭；来源登记 210→275（新增 65 项，另 1 条 T02-06/T02-07 共用页别名合并去重）+ Batch 15 复核补登 2 项并行计入（277）+ 本批复核后补登 3 项（280），全仓库 80 content entries / 280 sources；02.3、02.4 经主题范围复核升为已覆盖（基础），02.3-G1/G2、02.4-G1/G2/G3 缺口关闭（02.7-G3 的 T02-04 部分已交付，余 T02-12 属 Batch 31）。交付与审阅记录见 [batch-16-source-audit](research/batch-16-source-audit.md)、[初审](research/batch-16-codex-review.md)、[修订](research/batch-16-review-fixes.md)与[定向复核](research/batch-16-codex-recheck.md)（[第二轮](research/batch-16-codex-recheck-round-2.md)）。

**Batch 17–22 交付与审阅记录（2026-10-18 账面订正后口径）**：Batch 17（T02-08–T02-11）与 Batch 18（T03-01–T03-04）2026-10-09/10 交付并经 `gpt-6.1-sol / xhigh` 审阅，B17-C01–C13 中 12 项关闭（C08 经例外清单条件验收、长期 open 具名跟踪，见 [batch-17-t02-10-exception](research/batch-17-t02-10-exception.md)）、B18-C01–C16 全部关闭；Batch 19（T03-05–T03-08、T04-01）2026-10-13 闭环，B19-C01–C27 全部关闭（BLOCKED-1 HCCL 版本交集例外长期 open，见 [batch-19-blocked-1-exception](research/batch-19-blocked-1-exception.md)）；Batch 20（T04-02–T04-05）与 Batch 21 的 T04-06/T04-07 2026-10-13 经 `claude-opus-5-5` 审阅闭环（B20-C01–C40、B21-C01–C18 全部关闭），T05-01 经 codex `gpt-6.1-sol / xhigh` 初审与 33 轮复核于 2026-10-17 闭环（B21-C30–C34 全部关闭）；T04-08 于 2026-10-18 补交并经 `claude-opus-5-5` 初审与五轮复核闭环（B21-C35–C61 共 27 项全部关闭），Batch 21 至此完成；Batch 22（T05-02/T05-03/T05-05/T05-04）2026-10-17 经 `claude-opus-5-5` 审阅与整批验收闭环（B22-C01–C44、B22X-C01/C02 全部关闭）。Batch 17–21 的 exit_gate 主题范围复核未执行，01.3/02.5/02.6/03.1–03.7/04.1–04.6 的主题验收与缺口判定待补做。逐批记录见[覆盖盘点](topic-coverage-audit.md)头段与 docs/research/ 各批文件。

当前进展：**Batch 23 为下一批（按依赖图）**，另需补做 Batch 17–21 主题范围复核；以实际运行与验收记录为准。

知识库网站、搜索产品、API/MCP、现场适配器、自动评测执行框架和生产操作属于架构工程后续阶段，不纳入本次内容批次数。正文中的方法和有限教学题不代表上述工程已实现。

新增未命名平台或改变代表实现时先补来源/环境交集，再更新对应领域正文与平台入口。按固定版本维护历史案例，来源变更触发针对性复核；本次没有创建定时任务。

## 规划核对记录

独立规划审阅由 **gpt-6.1-sol / xhigh** 完成，8 项发现（5 P2、3 P3）经修订与定向复核全部关闭；范围与关闭证据见[独立审阅报告](research/followup-plan-review.md)。最终核对通过：63 个主题及五方面、141 条缺口、85 项任务、依赖与批次顺序、69 个既有条目的身份与文件摘要、证据/背景强度、来源/工作包引用和 411 处本地链接一致；`make check`、`make build` 均通过，仍为 69 content entries / 84 sources。结果保存在主清单的 validation 字段。核对通过只说明规划结构一致，不证明将来文章技术正确或硬件验证成功。
