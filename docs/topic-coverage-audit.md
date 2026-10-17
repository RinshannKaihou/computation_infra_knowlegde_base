# 63 个二级主题覆盖盘点

盘点日期：2026-10-08；输入范围：Batch 01–12 交付并修订后的源文件。**2026-10-08 Batch 13 更新**：T00-01/T01-01/T01-02/T01-03/T01-04 交付并经 `gpt-6.1-sol / xhigh` 审阅与两轮定向复核（18 项发现全部关闭）；00.1、01.2 经本批主题范围复核升为已覆盖（基础），01.1、01.3 缺口部分关闭。**2026-10-09 Batch 14 更新**：T01-05/T01-06/T01-07/T01-08 交付并经 `gpt-6.1-sol / xhigh` 审阅与三轮定向复核（15 项发现 B14-C01–C15 全部关闭，C10 按「编写者核对记录、未独立核验」限定口径关闭）；01.1、01.4、01.5 经本批主题范围复核升为已覆盖（基础），01.6-G1/G2 缺口关闭、主题验收属 Batch 15。**2026-10-09 Batch 15 更新**：T01-09/T02-01/T02-02/T02-03 交付并经 `gpt-6.1-sol / xhigh` 审阅与两轮定向复核（8 项发现 B15-C01–C08 全部关闭，C06 按「编写者核对记录、未独立核验」限定口径关闭）；01.6、02.1、02.2 经本批主题范围复核升为已覆盖（基础），02.3-G3 缺口关闭（02.3 主题验收属 Batch 16）。**2026-10-09 Batch 16 更新**：T02-04/T02-05/T02-06/T02-07 交付并经 `gpt-6.1-sol / xhigh` 审阅与两轮定向复核（7 项发现 B16-C01–C07 全部关闭）；02.3、02.4 经本批主题范围复核升为已覆盖（基础）。**2026-10-09/14 Batch 17 更新（账面订正回填）**：T02-08/T02-09/T02-10/T02-11 交付并经 `gpt-6.1-sol / xhigh` 初审与六轮定向复核（13 项发现 B17-C01–C13 中 12 项关闭；C08 逐算子累加精度与 TorchNPU cubeMathType 透传证据未关闭，2026-10-14 经例外清单条件验收、长期 open 具名跟踪，见 docs/research/batch-17-t02-10-exception.md）；本批未执行主题范围复核——01.3、02.5、02.6 保持基线口径，缺口 01.3-G3、02.5-G1/G2、02.6-G1/G2/G3 保持 open，主题验收待补做。**2026-10-09/10 Batch 18 更新（账面订正回填）**：T03-01/T03-02/T03-03/T03-04 交付并经 `gpt-6.1-sol / xhigh` 初审与八轮定向复核（16 项发现 B18-C01–C16 全部关闭，C01 为审阅误读撤销、C16 为首轮修订引入）；本批未执行主题范围复核——03.1、03.2、03.4 保持基线口径，缺口 03.1-G1/G2、03.2-G1/G2、03.4-G1/G2/G3 保持 open，主题验收待补做。**2026-10-13 Batch 19 更新（账面订正回填）**：T03-05/T03-06/T03-07/T03-08/T04-01 交付并经 `gpt-6.1-sol / xhigh` 初审与多轮定向复核（27 项发现 B19-C01–C27 全部关闭；BLOCKED-1 HCCL Test×目标 CANN/HDK/机型版本交集无关闭路径，经例外清单条件验收、长期 open 具名跟踪，T03-06 acceptance 5 未验收，见 docs/research/batch-19-blocked-1-exception.md）；本批未执行主题范围复核——03.3、03.5、03.6、03.7 保持基线口径，缺口 03.3-G1/G2/G3、03.5-G1/G2/G3、03.7-G1/G2/G3 与 04.1 各缺口保持 open（04.1 验收属 Batch 21），主题验收待补做。**2026-10-13 Batch 20 更新（账面订正回填）**：T04-02/T04-03/T04-04/T04-05 交付并经 `claude-opus-5-5` 初审与逐任务定向复核（40 项发现 B20-C01–C40 全部关闭，无例外；每轮核验 modelUsage 单一模型、无 fallback，effort 无可核验记录）；本批未关闭主题缺口——04.2/04.3/04.4 等主题保持基线口径，04.x 主题验收属 Batch 21。**2026-10-13/17 Batch 21 更新（账面订正回填）**：T04-06/T04-07 交付并经 `claude-opus-5-5` 审阅闭环（B21-C01–C18 全部关闭）；T05-01 经两轮作废初审（模型核验不符，按 fallback 条款弃用不计数）后改 codex `gpt-6.1-sol / xhigh` 初审与 33 轮定向复核（B21-C30–C34 全部关闭、acceptance 4/4），2026-10-17 闭环；**T04-08 从未启动**（无交付提交、无来源/审阅记录，batch-21-source-audit 的整批完成声明为时过早），Batch 21 批次保持未完成、T04-08 待补交；本批未执行主题范围复核——04.1–04.6 保持基线口径，各缺口保持 open，主题验收待补做。**2026-10-17 Batch 22 更新**：T05-02/T05-03/T05-05/T05-04 交付并审阅闭环（初审＋定向复核：B22-C01–C11、C12–C21、C22–C30、C31–C44 各批发现全部 CLOSED；前置 Batch 21 补交 T05-01 同日闭环）；本批审阅模型 claude-opus-5-5（claude -p 执行；T05-04 初审＋五次定向复核共六轮经调用方核验 CLI modelUsage 单一模型、无 fallback，T05-02/03/05 各轮按其报告记录）。主题范围复核：05.1-G1/G2、05.2-G1/G2、05.4-G1/G3 共 6 个缺口对照交付内容关闭；05.1-G3、05.4-G2、05.5-G1/G2/G3、05.7-G1/G2 因 T05-06–T05-10 未交付保持 open；本批无主题升为已覆盖（05.1/05.4/05.5 验收属 Batch 23，05.2/05.3/05.7 属 Batch 24，05.3 基线 covered 不变）。其余行仍为基线口径，覆盖判断由人工对照正文作出，机器可读记录见[盘点清单](../plans/topic-coverage.yaml)。

范围依据：[最初内容总目录](../content-outline.md)。后续变更应同步更新这两份盘点文件。

## 统计与结论

原设计的 9 个领域、63 个二级主题中，**22 个已覆盖基础范围，34 个部分覆盖，7 个未覆盖**。共 41 个主题有内容缺口。此分布是主题盘点，不是项目完工百分比。

现有 60 篇正文/验证方案与 13 个导航/路径条目，共 73 个 catalog entries、119 项外部来源。60 篇中包括 21 篇概念、9 篇参考、16 篇指南、7 篇来源案例、7 篇待执行验证方案；同一篇可支撑多个主题，不能逐行相加当作文章产量。

53 篇正文为 `source_checked`，7 篇方案为 `not_verified`，所有内容仍为 `draft`，本地 `reproduced` 为 0。没有把方案、上游案例、模型审阅或结构检查记作本地实测。

| 领域 | 主题数 | 已覆盖（基础） | 部分覆盖 | 未覆盖 |
|---|---:|---:|---:|---:|
| 00 导读与系统全景 | 6 | 3 | 2 | 1 |
| 01 物理设施与计算节点 | 6 | 5 | 1 | 0 |
| 02 系统软件与加速器执行栈 | 7 | 5 | 2 | 0 |
| 03 互联网络与分布式通信 | 7 | 1 | 5 | 1 |
| 04 数据路径与存储系统 | 6 | 0 | 5 | 1 |
| 05 集群平台与资源管理 | 7 | 1 | 4 | 2 |
| 06 训练与后训练系统 | 8 | 3 | 4 | 1 |
| 07 推理与服务系统 | 8 | 2 | 5 | 1 |
| 08 可靠性与计算正确性方法 | 8 | 3 | 5 | 0 |
| 合计 | 63 | 22 | 34 | 7 |

## 判断口径

- **已覆盖（基础）**：本行限定的核心问题已有实质说明和可串联的方法入口，能够解释原理/边界、使用条件、观测、异常判断与验证。它不表示该主题的全部深度、平台、版本或现场组合均已完成。
- **部分覆盖**：正文直接回答了主题的一部分，但尚不足以覆盖本行核心范围。新增文章和修订已有正文都可以补齐，不强制一题一篇或每题复制指南/案例/方案三件套。
- **未覆盖**：只有背景词句、字段、源码/来源入口或相邻主题；这些放在背景栏，不作为正向覆盖。领域首页列出的主题名也不作为正文交付。
- 以原设计的五方面检查主题总体：原理与边界、设计与使用、观测与判断、故障与处置、验证与案例。表中“核心范围”是本轮基础覆盖的验收对象，不缩减原目录的长期范围。
- 平台未知条件可以作为明确的边界知识；不能据此宣称平台兼容。尚无专门材料的 ROCm/RCCL、Slurm、其他 NPU 或引擎分支作为范围缺口保留。
- 本次核对源文件的范围、章节和验证元数据，没有重新审阅全部 84 项上游来源，不改变任何正文的编辑/验证状态。链接表用于追溯盘点依据。

## 逐主题盘点

每行保留原目录的编号与名称。已有条目的关键核对章节和 SHA-256 在 YAML 的 `documents` 中；表中范围说明用于识别条目哪部分支撑本主题。

### 00 导读与系统全景

| 编号与主题 | 覆盖判断与核心范围 | 已有内容及依据 | 缺口与补齐方向 |
|---|---|---|---|
| **00.1 范围、核心术语与系统边界** | **已覆盖（基础）**（Batch 13 复核）<br>界定算力系统的层次、核心术语、任务边界和可靠性维度 | [统一术语、先修关系与系统责任边界](../knowledge/00-overview/terms-and-system-boundaries.md)；[主机到模型执行的软件栈分层](../knowledge/02-software-stack/layers-and-boundaries.md)；[可靠性维度与故障域](../knowledge/08-reliability/dimensions-and-failure-domains.md)；[一次训练任务的端到端路径](../knowledge/00-overview/training-lifecycle.md)；[一次推理请求的端到端路径](../knowledge/00-overview/inference-lifecycle.md)<br>已有统一术语表（含同名异义与错误归属反例）、系统责任边界图、先修关系与按症状定位责任领域的方法及路径可达性验收 | **维护**：超节点等术语主归属在 T01-05/T00-02 交付后迁移到专题正文；新同名异义回本页登记。 |
| **00.2 一次训练任务的端到端路径** | **已覆盖（基础）**<br>串联资源准入、数据、初始化、训练 step、保存和恢复的职责与观察点 | [一次训练任务的端到端路径](../knowledge/00-overview/training-lifecycle.md)；[训练数据供给路径与等待](../knowledge/04-data-storage/training-data-path.md)；[并行策略与训练状态](../knowledge/06-training/parallelism-and-state.md)；[Checkpoint 恢复一致性](../knowledge/06-training/checkpoint-state-consistency.md)<br>已有端到端图、阶段入口、四条状态线、指标边界及恢复验证入口 | **维护**：基础范围暂无必补内容项；真实环境验证与平台/版本扩展另记。 |
| **00.3 一次推理请求的端到端路径** | **已覆盖（基础）**<br>串联请求入口、引擎排队、prefill/decode、输出与状态释放的职责和计时边界 | [一次推理请求的端到端路径](../knowledge/00-overview/inference-lifecycle.md)；[推理执行与 KV cache](../knowledge/07-inference/execution-and-kv-cache.md)；[推理延迟与吞吐指标字典](../knowledge/07-inference/latency-metrics.md)<br>已有请求图、状态/资源表、客户端与服务端计时差异及执行/指标入口 | **维护**：基础范围暂无必补内容项；真实环境验证与平台/版本扩展另记。 |
| **00.4 单机、集群与超节点的参考架构** | **未覆盖**<br>比较单机、集群和超节点的组成、数据/控制路径、共享依赖及选择条件 | 无直接正文。背景：[计算节点资源与拓扑参考](../knowledge/01-hardware/resource-topology.md)；[一次训练任务的端到端路径](../knowledge/00-overview/training-lifecycle.md)；[一次推理请求的端到端路径](../knowledge/00-overview/inference-lifecycle.md)<br>现有材料提供机型字段和流程背景，尚无三种架构的实质比较 | **后续补齐**：缺少参考架构图与组件部署关系；缺少规模、拓扑、故障域和成本约束下的选择与验收方法 |
| **00.5 设计目标与约束：可靠性、性能、容量、成本、能耗** | **部分覆盖**<br>把可靠性、性能、容量、成本和能耗转成可比较的设计目标及权衡 | [可靠性维度与故障域](../knowledge/08-reliability/dimensions-and-failure-domains.md)；[供电、散热与性能退化证据](../knowledge/01-hardware/power-thermal-evidence.md)；[推理延迟与吞吐指标字典](../knowledge/07-inference/latency-metrics.md)<br>已有可靠性目标、性能统计和功耗/散热证据；尚未组成设计决策方法 | **后续补齐**：缺少容量与成本口径；缺少能耗/有效产出度量；缺少五类目标的权衡案例与验收表 |
| **00.6 按角色、任务与平台组织的阅读路径** | **部分覆盖**<br>按角色、任务和平台给出有先修顺序、完成目标及主题入口的阅读路径 | [昇腾平台知识路径](../paths/platforms/ascend.md)；[NVIDIA 平台知识路径](../paths/platforms/nvidia.md)；[训练排障知识路径](../paths/tasks/training-triage.md)；[推理排障知识路径](../paths/tasks/inference-triage.md)<br>已有昇腾/NVIDIA 与训练/推理排障四条路径 | **后续补齐**：缺少学习者、架构设计与运维角色路径；缺少选型、验收、安装、优化、升级和恢复等任务路径 |

### 01 物理设施与计算节点

| 编号与主题 | 覆盖判断与核心范围 | 已有内容及依据 | 缺口与补齐方向 |
|---|---|---|---|
| **01.1 机柜、供电、散热与故障域** | **已覆盖（基础）**（Batch 14 复核）<br>说明机柜供电/散热依赖、故障域、容量约束和性能退化的证据链 | [机柜供电、散热预算与共享依赖](../knowledge/01-hardware/rack-power-cooling-and-failure-domains.md)；[供电、散热与性能退化证据](../knowledge/01-hardware/power-thermal-evidence.md)；[BMC、固件身份与跨层硬件事件](../knowledge/01-hardware/bmc-firmware-and-events.md)；[计算节点资源与拓扑参考](../knowledge/01-hardware/resource-topology.md)；[可靠性维度与故障域](../knowledge/08-reliability/dimensions-and-failure-domains.md)<br>已有机柜级功率预算四种口径与参数化例子、风冷/液冷观察点、设施到设备影响链、GPU 降频证据、训练 NPU（HDK 26.1.x）字段与事件级降频机制、四层证据关联表，以及 BMC/固件身份、事件链与三平台错误码到部件的映射 | **维护**：iBMC 告警码按「编写者核对记录、未独立核验」限定口径使用、带外—带内官方映射保持 unknown；时钟偏差数值与完整跨层时间线仍无实测，真实环境验证另行推进。 |
| **01.2 CPU、NUMA、主机内存与 I/O** | **已覆盖（基础）**（Batch 13 复核）<br>解释 CPU、NUMA、主机内存和 I/O 局部性对数据、计算与设备访问的影响 | [NUMA、主机内存与 I/O 局部性的成对验证](../knowledge/01-hardware/numa-memory-and-io-locality.md)；[计算节点资源与拓扑参考](../knowledge/01-hardware/resource-topology.md)；[训练数据供给路径与等待](../knowledge/04-data-storage/training-data-path.md)；[慢 rank 诊断指南](../knowledge/06-training/slow-rank-triage.md)；[训练数据加载饥饿诊断指南](../knowledge/04-data-storage/data-starvation-triage.md)<br>已有 first-touch/策略族/亲和语义、设备 NUMA 归属 ABI、topology→进程→内存→I/O 证据链与局部/远端成对测量方法（含线程迁移、NUMA 无感、数据饥饿反例） | **维护**：远端访问带宽的可引用数字、Ascend/鲲鹏主机侧 NUMA 官方文档、cgroup-v2 固定 commit 行号补齐后复核。 |
| **01.3 GPU/NPU 的执行单元、设备内存与数据移动** | **部分覆盖**<br>解释 GPU/NPU 执行单元、内存层次和主机/设备数据移动的机制及差异 | [加速器执行单元、内存层次与数据移动机制](../knowledge/01-hardware/accelerator-execution-and-data-movement.md)；[计算节点资源与拓扑参考](../knowledge/01-hardware/resource-topology.md)；[昇腾 NPU 内存与 OOM 证据](../knowledge/02-software-stack/ascend-memory-oom-evidence.md)；[训练数据供给路径与等待](../knowledge/04-data-storage/training-data-path.md)<br>已有三平台（H100/MI200/Atlas A2）执行组织与内存层次真实术语、统一观察点数据移动图（四层路径、两层同步）、计算强度选择条件与验证方法入口 | **优先补齐**：NPU 主机传输/同步语义待补（T02-11，Batch 17）；Ascend 各 buffer 容量与「架构规格」数值表仍无官方来源 |
| **01.4 板卡、服务器、节点与超节点组成** | **已覆盖（基础）**（Batch 14 复核）<br>说明板卡、服务器、节点与超节点的组件关系、互联和共享故障域 | [计算节点资源与拓扑参考](../knowledge/01-hardware/resource-topology.md)；[供电、散热与性能退化证据](../knowledge/01-hardware/power-thermal-evidence.md)；[BMC、固件身份与跨层硬件事件](../knowledge/01-hardware/bmc-firmware-and-events.md)<br>已有四组成层次的实体/资源单位/互联/供电散热/可替换边界比较；GB200 NVL72（DGX GB UG + HPE/Supermicro OEM 口径）、Atlas 900 A3 SuperPoD 与 AMD OEM 节点（AS-8125GS-TNMR2 + MI300X）三个机型绑定样板；BOM/文档/现场枚举三方核对清单与共享故障隔离假设 | **维护**：E1.S 数量、算力档位、「物理 384 与实际部署」等 OEM/版本冲突按来源分列保留；A3 细部手册条款、FRU 清单与 CloudMatrix 384 官方文档未取得，补充后再复核。 |
| **01.5 BMC、固件、硬件健康与错误信息** | **已覆盖（基础）**（Batch 14 复核）<br>关联 BMC、固件、设备身份、健康事件、计数器与检测覆盖 | [设备健康证据与检测边界](../knowledge/01-hardware/health-evidence.md)；[BMC、固件身份与跨层硬件事件](../knowledge/01-hardware/bmc-firmware-and-events.md)；[新节点与返修节点验收](../knowledge/01-hardware/node-acceptance-triage.md)；[计算节点资源与拓扑参考](../knowledge/01-hardware/resource-topology.md)<br>已有五类健康证据分类与统一记录格式、机型绑定错误码最小代表集（NVIDIA Xid 目录逐行重建/DCGM 退出码、昇腾黑匣子/DCMI/npu-smi、AMD AFID/amd-smi/RAS）、BMC/固件身份与事件链（Redfish 事件/固件模型 + DGX/iBMC/Supermicro OEM 三实例）、N/A 语义分层与带外—带内时间线对齐方法 | **维护**：iBMC 告警码限定口径（编写者核对记录、未独立核验）、A3 黑匣子码表仅存在性核对、带外—带内官方映射 unknown 等证据边界保留；端到端时间线对齐仍为未执行的匹配方法（官方双通道案例为 GB200 RN），真实环境验证归 V08。 |
| **01.6 节点选型、验收与设备生命周期** | **已覆盖（基础）**（Batch 15 复核）<br>覆盖节点选型、验收、隔离、返修与退役的条件和验证 | [新节点与返修节点验收](../knowledge/01-hardware/node-acceptance-triage.md)；[节点选型、隔离返修、长期管理与退役](../knowledge/01-hardware/node-selection-and-lifecycle.md)；[设备健康证据与检测边界](../knowledge/01-hardware/health-evidence.md)；[供电、散热与性能退化证据](../knowledge/01-hardware/power-thermal-evidence.md)<br>已有新节点/返修节点四层验收、停止条件及回服门槛；节点选型与容量/成本比较方法、采购到退役状态机与退役完成判据（含独立凭据处置门槛）；Batch 15 补齐节点验收的环境档案字段（OCP SDC Test Input/Output 规范 + NERSC-10 ATP 样板锚定）、真实档案登记、证据脱敏/外置、首次测试/修订后复验与回服确认纪律 | **维护**：真实验收环境档案（01.6-G3）未取得、仍属 V08 授权验证轨道，方法交付与模板不关闭该缺口；NVSM 示例图像内容按「编写者核对记录、未独立核验」限定口径使用，DURATION 单位与当前具体机型 NIC 压测支持保持 unknown。 |

### 02 系统软件与加速器执行栈

| 编号与主题 | 覆盖判断与核心范围 | 已有内容及依据 | 缺口与补齐方向 |
|---|---|---|---|
| **02.1 OS、进程、主机资源与设备访问** | **已覆盖（基础）**（Batch 15 复核）<br>说明 OS/进程资源、设备权限、容器访问及主机异常的观察边界 | [OS/进程资源压力与设备访问诊断](../knowledge/02-software-stack/host-resource-pressure-and-device-access.md)；[主机到模型执行的软件栈分层](../knowledge/02-software-stack/layers-and-boundaries.md)；[从物理设备到容器资源的状态链](../knowledge/05-cluster-platform/device-resource-chain.md)；[训练数据加载饥饿诊断指南](../knowledge/04-data-storage/data-starvation-triage.md)<br>Batch 15 交付固定 Linux v6.16（固定 commit）的调度/亲和、cpuset、cgroup v2（cpu/memory/pids/device）、PSI、OOM（cgroup 与全局分列）、rlimit 与 namespace 机制正文；物理内存不足/cgroup limit/设备 OOM 分列判断；三平台设备节点与容器访问模型（NVIDIA per-GPU+caps、Ascend 按产品分表挂载集、AMD kfd/renderD）；进程/容器/节点三层采集路径与成对隔离对照方法 | **维护**：memory.events 归因、FDSize 槽位语义、EMFILE/ENFILE/EPERM 三候选与设备访问 errno 候选层提示按审阅修订口径使用；cgroup v2 设备规则枚举（bpftool/eBPF 工具链）、mountinfo/cgroup 解析与设备 OOM 系统级判据取证后复核；正文 not_verified，真实系统实测归验证轨道。 |
| **02.2 驱动、运行时与基础库** | **已覆盖（基础）**（Batch 15 复核）<br>说明驱动、运行时、基础库的职责、装载路径和故障边界 | [驱动初始化、运行时执行同步与库装载](../knowledge/02-software-stack/runtime-execution-and-library-loading.md)；[主机到模型执行的软件栈分层](../knowledge/02-software-stack/layers-and-boundaries.md)；[昇腾软件栈的文档配套档案](../knowledge/02-software-stack/ascend-documented-profile.md)；[NVIDIA 软件栈的文档配套档案](../knowledge/02-software-stack/nvidia-documented-profile.md)；[昇腾版本配套失败诊断指南](../knowledge/02-software-stack/ascend-version-mismatch-triage.md)<br>Batch 15 交付 CUDA 12.8/CANN 8.2.RC1.alpha001/HIP 6.3.42134 三栈初始化、primary/默认 Context、stream/event/同步与异步错误语义（API 不等价点分列）、cuBLAS/cuDNN/NCCL、rocBLAS/MIOpen/RCCL、aclnn 基础库职责与 ld.so/ldd//proc maps 装载身份分层、官方最小示例；两平台配套档案完成约束交集核对与制品身份分层 | **维护**：R545/Python 冲突（conflict）、CANN 8.3.RC1 精确 HDK/OS 交集（blocked）、NGC manifest/abi1 wheel 身份等保留，取得后再补；HCCL 职责页与 HIP↔ROCR 版本对应未取证；正文限所选文档样板、未实测。 |
| **02.3 CUDA、ROCm、CANN 等平台软件栈** | **已覆盖（基础）**（Batch 16 复核）<br>比较 CUDA、ROCm、CANN 的组成、接口与适用条件，并保留各平台证据边界 | [主机到模型执行的软件栈分层](../knowledge/02-software-stack/layers-and-boundaries.md)；[昇腾软件栈的文档配套档案](../knowledge/02-software-stack/ascend-documented-profile.md)；[NVIDIA 软件栈的文档配套档案](../knowledge/02-software-stack/nvidia-documented-profile.md)；[AMD ROCm 软件栈的文档配套档案](../knowledge/02-software-stack/amd-rocm-documented-profile.md)<br>Batch 16 交付 ROCm Core SDK 10.1.0 × MI300X × Ubuntu 24.04.5 × amdgpu 31.60.0 文档样板档案（版本线/兼容矩阵/组件职责/TheRock 合并打包/PyTorch 构建关系与双分发渠道/安装验证入口/许可）与三栈六职责域对照（编译/运行时/算子与数学库/通信/框架后端/引擎插件，证据态分列、三栈实测均 not_run） | **维护**：CANN 编译器组件职责页缺口、CANN 8.3.RC1 精确 HDK/OS 交集（blocked）、ROCm 10.1.0 兼容矩阵选择器页未逐条件块独立核对、ROCm torch.compile 专项文档缺失、HIP/llvm 文档站标与组件表冲突等边界保留；档案为 documented 样板、未实测。 |
| **02.4 算子、编译器、计算图与执行模式** | **已覆盖（基础）**（Batch 16 复核）<br>说明算子分发、编译、图捕获与执行模式，区分失败层并验证切换效果 | [算子分发、编译与计算图执行机制](../knowledge/02-software-stack/operators-compilers-and-graphs.md)；[GPU 算子、编译和图执行失败的定向诊断](../knowledge/02-software-stack/gpu-op-graph-failure-triage.md)；[昇腾算子不支持与图编译失败诊断指南](../knowledge/02-software-stack/ascend-op-graph-failure-triage.md)；[主机到模型执行的软件栈分层](../knowledge/02-software-stack/layers-and-boundaries.md)<br>Batch 16 交付 GPU 编译/图捕获/缓存机制正文（固定 PyTorch 2.6 文档与 v2.6.0 源码、TorchNPU 7.2.0 与 CANN 8.2.RC1.alpha001、ROCm docs-10.1.0）与 NVIDIA/AMD 诊断指南（调试工具链、捕获错误码 900–908、901 先前错误致失效定义、编译缓存观测、主案例 pytorch#188355/#188641 与对照案例 #193735） | **维护**：GPU 路径未实测（诊断文 not_verified）、ROCm torch.compile 专项官方文档缺失、TorchAir 试验特性与产品矩阵限定、主案例回归测试 @skipIfRocm（ROCm 侧保持 unknown）等边界保留；CUDA Graphs 约束两档、冷缓存两维度、Mega-Cache 非 2.6、guard 复合变化观察按 Batch 16 审阅修订口径使用。 |
| **02.5 框架与设备后端适配** | **部分覆盖**<br>说明框架抽象、设备后端注册、算子覆盖及推理平台插件的适配责任 | [主机到模型执行的软件栈分层](../knowledge/02-software-stack/layers-and-boundaries.md)；[昇腾算子不支持与图编译失败诊断指南](../knowledge/02-software-stack/ascend-op-graph-failure-triage.md)；[昇腾软件栈的文档配套档案](../knowledge/02-software-stack/ascend-documented-profile.md)；[一次推理请求的端到端路径](../knowledge/00-overview/inference-lifecycle.md)<br>已有 TorchNPU 后端/注册边界与 vLLM 平台插件说明 | **后续补齐**：缺少框架到设备后端的适配流程与能力核对表；缺少 GPU/其他框架实现对照和适配验证方法 |
| **02.6 内存管理、数据格式与精度语义** | **部分覆盖**<br>说明分配/保留、workspace、dtype/layout、有限精度与同步语义 | [昇腾 NPU 内存与 OOM 证据](../knowledge/02-software-stack/ascend-memory-oom-evidence.md)；[GPU 到 NPU 的精度差异诊断指南](../knowledge/06-training/gpu-npu-precision-difference-triage.md)；[静默错误与计算完整性判定](../knowledge/08-reliability/silent-errors-and-integrity.md)<br>已有 NPU 内存分层和碎片观测、dtype/layout 比对与浮点容差纪律 | **优先补齐**：缺少 CUDA 内存管理对应正文；缺少数据格式转换、混合精度与精度语义基础；NPU 传输/同步接口证据待补 |
| **02.7 环境配套、安装验证、迁移与升级** | **部分覆盖**<br>用制品/环境身份判断配套，完成安装基线、迁移/升级对照和回退验证 | [如何判断版本配套是否有依据](../knowledge/02-software-stack/compatibility-evidence.md)；[昇腾版本配套失败诊断指南](../knowledge/02-software-stack/ascend-version-mismatch-triage.md)；[昇腾版本配套失败来源案例](../knowledge/02-software-stack/ascend-version-mismatch-source-case.md)；[昇腾版本配套失败验证实验设计](../knowledge/02-software-stack/ascend-version-mismatch-experiment.md)；[昇腾软件栈的文档配套档案](../knowledge/02-software-stack/ascend-documented-profile.md)；[NVIDIA 软件栈的文档配套档案](../knowledge/02-software-stack/nvidia-documented-profile.md)<br>配套证据两轴、固定档案、错配诊断/案例/验证方案已经串联 | **后续补齐**：缺少完整安装验证流程；缺少迁移/升级的变化清单、兼容检查和回退方法；已有样板不是可直接部署的整套环境 |

### 03 互联网络与分布式通信

| 编号与主题 | 覆盖判断与核心范围 | 已有内容及依据 | 缺口与补齐方向 |
|---|---|---|---|
| **03.1 节点内、节点间与超节点互联** | **部分覆盖**<br>解释节点内、节点间与超节点的物理互联、数据路径及故障域 | [计算节点资源与拓扑参考](../knowledge/01-hardware/resource-topology.md)；[通信带宽与性能基线口径](../knowledge/03-communication/bandwidth-baselines.md)；[通信带宽退化诊断指南](../knowledge/03-communication/bandwidth-degradation-triage.md)<br>已有 PCIe/互联/NIC 归属字段、机型例子和拓扑相关性能边界 | **优先补齐**：缺少 NVLink/NVSwitch、HCCS 及超节点互联机制；缺少节点间物理路径图与拓扑核对实例 |
| **03.2 Ethernet、InfiniBand、RoCE 与 RDMA** | **未覆盖**<br>解释 Ethernet、IB、RoCE、RDMA 的协议与队列/内存机制，并给出独立基线与排障证据 | 无直接正文。背景：[通信带宽退化诊断指南](../knowledge/03-communication/bandwidth-degradation-triage.md)；[NCCL 超时诊断指南](../knowledge/03-communication/nccl-timeout-triage.md)；[HCCL 超时诊断指南](../knowledge/03-communication/hccl-timeout-triage.md)<br>现有指南提及接口、CQE、链路或配置，尚未解释网络/RDMA 主干机制 | **优先补齐**：缺少协议与 verbs/QP/CQ/MR 基础；缺少 IB/RoCE 配置、拥塞和独立验证的版本化方法 |
| **03.3 拓扑、路由、拥塞与性能基线** | **部分覆盖**<br>把物理拓扑、路由、拥塞和并发条件关联到可比较的性能基线 | [通信带宽与性能基线口径](../knowledge/03-communication/bandwidth-baselines.md)；[通信带宽退化诊断指南](../knowledge/03-communication/bandwidth-degradation-triage.md)；[计算节点资源与拓扑参考](../knowledge/01-hardware/resource-topology.md)；[作业准入、调度与拓扑放置](../knowledge/05-cluster-platform/admission-and-placement.md)<br>已有测量口径、rank/拓扑/并发字段及带宽退化诊断 | **优先补齐**：缺少路由/rail 选择机制；缺少拥塞与多租户争用的指标、对照和来源案例；缺少跨节点网络基线 |
| **03.4 集合通信原理与通信模式** | **部分覆盖**<br>解释主要集合与点对点通信模式、数据移动、匹配契约及性能成本 | [集合通信与 rank 进度](../knowledge/03-communication/collectives-and-rank-progress.md)；[通信带宽与性能基线口径](../knowledge/03-communication/bandwidth-baselines.md)；[并行策略与训练状态](../knowledge/06-training/parallelism-and-state.md)<br>已有 collective 契约、进度语义和 NCCL-tests 算子换算表 | **后续补齐**：缺少各原语的数据流解释；缺少 ring/tree 等算法与代价；缺少与 DP/TP/PP/EP 工作负载的系统映射 |
| **03.5 NCCL、RCCL、HCCL 等通信库** | **部分覆盖**<br>说明 NCCL、RCCL、HCCL 的接口/支持边界、观测与验证能力 | [集合通信与 rank 进度](../knowledge/03-communication/collectives-and-rank-progress.md)；[NCCL 超时诊断指南](../knowledge/03-communication/nccl-timeout-triage.md)；[HCCL 超时诊断指南](../knowledge/03-communication/hccl-timeout-triage.md)；[通信带宽与性能基线口径](../knowledge/03-communication/bandwidth-baselines.md)<br>已有 NCCL/HCCL 固定语义、诊断支路和基线口径 | **后续补齐**：缺少 RCCL 独立正文与来源；缺少通信库能力/运行条件比较；HCCL 测试版本与目标环境需分别固定 |
| **03.6 通信初始化、rank 映射与执行次序** | **已覆盖（基础）**<br>关联初始化的通信域、成员/设备映射和 group/collective 次序，识别契约分叉 | [集合通信与 rank 进度](../knowledge/03-communication/collectives-and-rank-progress.md)；[NCCL 超时诊断指南](../knowledge/03-communication/nccl-timeout-triage.md)；[HCCL 超时诊断指南](../knowledge/03-communication/hccl-timeout-triage.md)；[NCCL 超时验证实验设计](../knowledge/03-communication/nccl-timeout-experiment.md)；[HCCL 超时验证实验设计](../knowledge/03-communication/hccl-timeout-experiment.md)<br>已有 communicator/rank 定义、参数契约、进度时间线、两平台诊断与错序对照方案；未知 API 边界显式保留 | **维护**：基础范围暂无必补内容项；真实环境验证与平台/版本扩展另记。 |
| **03.7 超时、链路退化、通信热点与验证** | **部分覆盖**<br>区分超时、链路退化和通信热点，依据时间线、路径与对照验证原因 | [NCCL 超时诊断指南](../knowledge/03-communication/nccl-timeout-triage.md)；[NCCL Broadcast 超时来源案例：PyTorch #118369](../knowledge/03-communication/nccl-timeout-source-case.md)；[NCCL 超时验证实验设计](../knowledge/03-communication/nccl-timeout-experiment.md)；[HCCL 超时诊断指南](../knowledge/03-communication/hccl-timeout-triage.md)；[HCCL 启动期超时来源案例：vLLM Ascend #14296](../knowledge/03-communication/hccl-timeout-source-case.md)；[HCCL 超时验证实验设计](../knowledge/03-communication/hccl-timeout-experiment.md)；[通信带宽退化诊断指南](../knowledge/03-communication/bandwidth-degradation-triage.md)<br>超时有两套指南/来源案例/方案，带宽退化也已有指南 | **后续补齐**：缺少通信热点与拥塞专项方法；缺少带宽退化的独立来源案例和路径对照；跨节点链路证据仍需补齐 |

### 04 数据路径与存储系统

| 编号与主题 | 覆盖判断与核心范围 | 已有内容及依据 | 缺口与补齐方向 |
|---|---|---|---|
| **04.1 数据集、预处理、加载与缓存** | **部分覆盖**<br>说明数据集身份、预处理、加载、采样与缓存的生命周期和性能/正确性边界 | [训练数据供给路径与等待](../knowledge/04-data-storage/training-data-path.md)；[训练数据加载饥饿诊断指南](../knowledge/04-data-storage/data-starvation-triage.md)<br>已有存储到消费的流水线、PyTorch DataLoader 等待/硬失败诊断 | **优先补齐**：缺少数据集版本和预处理正确性；缺少缓存一致性/失效机制；NPU 数据传输与精确数据游标恢复仍有缺口 |
| **04.2 本地、共享、对象与并行存储** | **未覆盖**<br>比较本地、共享、对象和并行存储的接口、缓存、一致性、持久性与选择条件 | 无直接正文。背景：[计算节点资源与拓扑参考](../knowledge/01-hardware/resource-topology.md)；[Checkpoint 写入与持久化边界](../knowledge/04-data-storage/checkpoint-durability.md)；[Checkpoint 完整性与校验证据](../knowledge/04-data-storage/checkpoint-integrity-evidence.md)<br>现有记录涉及存储入口、通用 fsync 和 Ceph scrub，尚无存储类型主干正文 | **优先补齐**：缺少各类存储机制与语义比较；缺少版本绑定的后端访问/诊断/基线方法与选型条件 |
| **04.3 模型与 Checkpoint 的读写、传输和持久化** | **部分覆盖**<br>区分模型/Checkpoint 的状态截取、暂存、读写、传输、提交和持久化 | [Checkpoint 写入与持久化边界](../knowledge/04-data-storage/checkpoint-durability.md)；[Checkpoint 慢写与恢复 I/O 诊断指南](../knowledge/04-data-storage/checkpoint-slow-io-triage.md)；[Checkpoint 完整性与校验证据](../knowledge/04-data-storage/checkpoint-integrity-evidence.md)<br>已有 DCP/MindIO 保存完成语义、慢写/读路径诊断与校验证据 | **优先补齐**：缺少模型制品分发与加载路径；缺少网络文件系统/对象存储的传输和提交语义；缺少选定存储后端的读写验证 |
| **04.4 数据与文件完整性、版本和一致性** | **部分覆盖**<br>关联数据/文件身份、版本、字节完整性、提交一致性与应用状态一致性 | [Checkpoint 完整性与校验证据](../knowledge/04-data-storage/checkpoint-integrity-evidence.md)；[Checkpoint 写入与持久化边界](../knowledge/04-data-storage/checkpoint-durability.md)；[Checkpoint 恢复一致性](../knowledge/06-training/checkpoint-state-consistency.md)<br>已有 Checkpoint 格式/metadata/scrub/应用校验分层及训练恢复一致性 | **优先补齐**：缺少数据集/模型制品版本与内容身份方案；缺少传输端到端校验；其他存储后端及应用自检实现证据待补 |
| **04.5 I/O 性能、数据饥饿与长尾** | **部分覆盖**<br>把 I/O 吞吐/延迟、供给不足和长尾定位到相邻边界并验证处置 | [训练数据供给路径与等待](../knowledge/04-data-storage/training-data-path.md)；[训练数据加载饥饿诊断指南](../knowledge/04-data-storage/data-starvation-triage.md)；[Checkpoint 慢写与恢复 I/O 诊断指南](../knowledge/04-data-storage/checkpoint-slow-io-triage.md)<br>已有加载饥饿、Checkpoint staging/writeback/fsync 与读路径分支及完成判据 | **后续补齐**：缺少后端独立 I/O 基线与容量口径；缺少共享/对象存储长尾和争用对照；缺少可引用的阶段计时实现 |
| **04.6 存储异常、恢复与验证** | **部分覆盖**<br>区分后端故障、数据损坏和应用恢复异常，选择恢复点并验证结果 | [Checkpoint 慢写与恢复 I/O 诊断指南](../knowledge/04-data-storage/checkpoint-slow-io-triage.md)；[Checkpoint 完整性与校验证据](../knowledge/04-data-storage/checkpoint-integrity-evidence.md)；[Checkpoint 恢复状态异常诊断指南](../knowledge/06-training/checkpoint-state-recovery-triage.md)<br>已有 Checkpoint 慢读写、损坏检测和恢复候选选择边界 | **后续补齐**：缺少挂载/客户端/后端可用性异常流程；缺少存储恢复、修复与故障域演练；不得由训练恢复指南代替存储恢复 |

### 05 集群平台与资源管理

| 编号与主题 | 覆盖判断与核心范围 | 已有内容及依据 | 缺口与补齐方向 |
|---|---|---|---|
| **05.1 容器、镜像、设备暴露与运行环境** | **部分覆盖**<br>说明镜像、runtime、设备暴露、权限与依赖怎样构成容器运行环境 | [从物理设备到容器资源的状态链](../knowledge/05-cluster-platform/device-resource-chain.md)；[容器内 NPU 不可见诊断指南](../knowledge/05-cluster-platform/ascend-device-visibility-triage.md)；[容器内 NPU 不可见来源案例](../knowledge/05-cluster-platform/ascend-device-visibility-source-case.md)；[容器内 NPU 不可见验证实验设计](../knowledge/05-cluster-platform/ascend-device-visibility-experiment.md)；[NVIDIA 软件栈的文档配套档案](../knowledge/02-software-stack/nvidia-documented-profile.md)<br>Ascend 设备注入有指南/案例/方案，NVIDIA 容器栈已有文档档案 | **后续补齐**：缺少镜像构建、制品身份与供应链管理；缺少 GPU runtime/CDI 专项流程；缺少容器隔离/运行环境基线 |
| **05.2 Kubernetes、Slurm 等平台与作业生命周期** | **部分覆盖**<br>说明 Kubernetes/Slurm 的作业对象、提交/运行/退出/重试与资源生命周期 | [作业准入、调度与拓扑放置](../knowledge/05-cluster-platform/admission-and-placement.md)；[从物理设备到容器资源的状态链](../knowledge/05-cluster-platform/device-resource-chain.md)；[空闲设备但作业等待诊断指南](../knowledge/05-cluster-platform/idle-resource-job-waiting-triage.md)；[一次训练任务的端到端路径](../knowledge/00-overview/training-lifecycle.md)<br>已有 Kubernetes/Kueue 准入到 Pod 启动的状态与训练导航 | **后续补齐**：缺少 Slurm 正文与来源；缺少完整作业生命周期、控制器责任、退出/重试与状态清理机制 |
| **05.3 设备发现、分配、健康上报与资源账本** | **已覆盖（基础）**<br>区分设备发现、健康上报、资源账本与具体分配，关联各层实体和异常 | [从物理设备到容器资源的状态链](../knowledge/05-cluster-platform/device-resource-chain.md)；[设备健康证据与检测边界](../knowledge/01-hardware/health-evidence.md)；[容器内 NPU 不可见诊断指南](../knowledge/05-cluster-platform/ascend-device-visibility-triage.md)；[容器内 NPU 不可见来源案例](../knowledge/05-cluster-platform/ascend-device-visibility-source-case.md)；[容器内 NPU 不可见验证实验设计](../knowledge/05-cluster-platform/ascend-device-visibility-experiment.md)<br>已有 K8s Device Plugin 接口、健康变化对新旧 Pod 的作用、Ascend 实现例子及分配/映射验证方案 | **维护**：基础范围暂无必补内容项；真实环境验证与平台/版本扩展另记。 |
| **05.4 配额、排队、gang、放置与拓扑亲和性** | **部分覆盖**<br>说明配额、排队、gang、准入、放置和拓扑亲和的责任与诊断 | [作业准入、调度与拓扑放置](../knowledge/05-cluster-platform/admission-and-placement.md)；[空闲设备但作业等待诊断指南](../knowledge/05-cluster-platform/idle-resource-job-waiting-triage.md)；[计算节点资源与拓扑参考](../knowledge/01-hardware/resource-topology.md)<br>已有 Kueue 配额/条件/TAS 及 MindCluster 芯片亲和边界和等待诊断 | **后续补齐**：缺少 gang 的成组启动/失败/回退机制；缺少配额配置与调度策略权衡实例；其他平台调度方法需独立来源 |
| **05.5 多租户、隔离、资源争用与容量管理** | **未覆盖**<br>说明租户边界、计算/内存/网络隔离、争用和容量准入，验证公平性与性能 | 无直接正文。背景：[作业准入、调度与拓扑放置](../knowledge/05-cluster-platform/admission-and-placement.md)；[容器内 NPU 不可见验证实验设计](../knowledge/05-cluster-platform/ascend-device-visibility-experiment.md)；[推理执行与 KV cache](../knowledge/07-inference/execution-and-kv-cache.md)<br>现有配额、测试隔离前提与 cache salt 是背景；尚无多租户系统设计/诊断正文 | **优先补齐**：缺少 GPU/NPU 共享与隔离模型；缺少争用检测、公平性及容量管理；缺少租户隔离验证和来源案例 |
| **05.6 节点上下线、升级、发布与变更** | **未覆盖**<br>定义节点上下线、drain/准入、组件升级与发布波次，验证回退和回服 | 无直接正文。背景：[新节点与返修节点验收](../knowledge/01-hardware/node-acceptance-triage.md)；[如何判断版本配套是否有依据](../knowledge/02-software-stack/compatibility-evidence.md)；[弹性训练与成员变更](../knowledge/06-training/elastic-training-and-membership.md)<br>验收提供回服门槛、其他文章提供配套/成员背景，尚无平台变更生命周期正文 | **优先补齐**：缺少节点上下线/drain 状态与资源回收流程；缺少升级/发布/回退策略；缺少变更后验收和失败恢复 |
| **05.7 调度失败、控制面异常与集群恢复** | **部分覆盖**<br>区分调度失败、资源视图失真和控制面故障，恢复平台并验证作业进展 | [空闲设备但作业等待诊断指南](../knowledge/05-cluster-platform/idle-resource-job-waiting-triage.md)；[作业准入、调度与拓扑放置](../knowledge/05-cluster-platform/admission-and-placement.md)；[从物理设备到容器资源的状态链](../knowledge/05-cluster-platform/device-resource-chain.md)<br>已有等待层定位、账本与分配矛盾核对 | **后续补齐**：缺少控制器/API/状态存储故障与一致性诊断；缺少控制面恢复、作业重建和资源账本校验流程 |

### 06 训练与后训练系统

| 编号与主题 | 覆盖判断与核心范围 | 已有内容及依据 | 缺口与补齐方向 |
|---|---|---|---|
| **06.1 训练计算过程与状态：权重、梯度、优化器、数据进度** | **已覆盖（基础）**<br>解释一次训练 step 的计算和状态提交，区分权重、梯度、优化器与数据进度 | [一次训练任务的端到端路径](../knowledge/00-overview/training-lifecycle.md)；[并行策略与训练状态](../knowledge/06-training/parallelism-and-state.md)；[Checkpoint 恢复一致性](../knowledge/06-training/checkpoint-state-consistency.md)；[Checkpoint 恢复状态异常诊断指南](../knowledge/06-training/checkpoint-state-recovery-triage.md)<br>已有 forward/backward/update 导航、状态责任矩阵、截取边界和恢复核对；算法细节在本行基础范围之外 | **维护**：基础范围暂无必补内容项；真实环境验证与平台/版本扩展另记。 |
| **06.2 数据、张量、流水线、专家等并行策略** | **部分覆盖**<br>比较 DP/状态分片/TP/PP/EP 等策略的状态、通信、内存、效率与组合条件 | [并行策略与训练状态](../knowledge/06-training/parallelism-and-state.md)；[集合通信与 rank 进度](../knowledge/03-communication/collectives-and-rank-progress.md)；[弹性训练与成员变更](../knowledge/06-training/elastic-training-and-membership.md)<br>已有 DDP/FSDP/TP/PP 状态布局和组合身份；EP/CP 仅列入维度 | **后续补齐**：缺少专家并行机制；缺少各策略选型和规模效率权衡；缺少组合并行的映射/性能验证 |
| **06.3 训练框架与执行：框架通用机制及平台实现** | **部分覆盖**<br>说明训练框架的执行循环、分布式封装、平台适配与观测接口 | [并行策略与训练状态](../knowledge/06-training/parallelism-and-state.md)；[弹性训练与成员变更](../knowledge/06-training/elastic-training-and-membership.md)；[主机到模型执行的软件栈分层](../knowledge/02-software-stack/layers-and-boundaries.md)<br>已有 PyTorch 并行/state-dict 与 MindSpeed HA 样板及框架分层 | **后续补齐**：缺少完整训练循环、执行/编译及框架组件关系；缺少 PyTorch/Megatron/MindSpeed 等实现责任对照；缺少执行路径验证 |
| **06.4 预训练、微调、强化学习与 rollout** | **未覆盖**<br>比较预训练、微调、RL 的工作流，并解释 rollout、权重同步与数据/状态一致性 | 无直接正文。背景：[GPU 到 NPU 的精度差异来源案例：Ascend PyTorch #17](../knowledge/06-training/gpu-npu-precision-difference-source-case.md)；[一次训练任务的端到端路径](../knowledge/00-overview/training-lifecycle.md)<br>SFT 来源案例与总览只是背景，尚无这些工作流的机制正文 | **优先补齐**：缺少预训练/微调类型与工作流；缺少 RL rollout、训练/推理协同及权重同步；缺少一致性/吞吐验证 |
| **06.5 算子适配、混合精度、数值行为与收敛** | **部分覆盖**<br>关联算子适配、混合精度、数值差异和收敛，区分合法误差与错误 | [GPU 到 NPU 的精度差异诊断指南](../knowledge/06-training/gpu-npu-precision-difference-triage.md)；[GPU 到 NPU 的精度差异来源案例：Ascend PyTorch #17](../knowledge/06-training/gpu-npu-precision-difference-source-case.md)；[GPU 到 NPU 的精度差异验证实验设计](../knowledge/06-training/gpu-npu-precision-difference-experiment.md)；[昇腾算子不支持与图编译失败诊断指南](../knowledge/02-software-stack/ascend-op-graph-failure-triage.md)；[静默错误与计算完整性判定](../knowledge/08-reliability/silent-errors-and-integrity.md)<br>GPU→NPU 精度专题已串联首差异、重复性、传播/质量对照与容差纪律 | **后续补齐**：缺少混合精度/loss scale 机制；缺少收敛与训练质量判断方法；算子适配与精度策略的端到端案例待补 |
| **06.6 性能分析、慢 rank、资源不均与吞吐退化** | **部分覆盖**<br>按阶段与 rank 分解性能，区分数据/计算/通信/主机/设备等待和负载不均 | [慢 rank 诊断指南](../knowledge/06-training/slow-rank-triage.md)；[训练数据加载饥饿诊断指南](../knowledge/04-data-storage/data-starvation-triage.md)；[通信带宽退化诊断指南](../knowledge/03-communication/bandwidth-degradation-triage.md)；[供电、散热与性能退化证据](../knowledge/01-hardware/power-thermal-evidence.md)<br>已有慢 rank 指南和数据、通信、供电散热交叉入口 | **后续补齐**：缺少系统 profiling 方法与工具边界；缺少并行负载不均/热点与吞吐优化权衡；缺少性能回归来源案例 |
| **06.7 Checkpoint 状态、一致性、容错与弹性恢复** | **已覆盖（基础）**<br>说明恢复点、状态一致性、容错/成员变更责任和受支持重分片的验证边界 | [Checkpoint 恢复一致性](../knowledge/06-training/checkpoint-state-consistency.md)；[Checkpoint 恢复状态异常诊断指南](../knowledge/06-training/checkpoint-state-recovery-triage.md)；[Checkpoint 恢复状态异常来源案例](../knowledge/06-training/checkpoint-state-recovery-source-case.md)；[Checkpoint 恢复状态异常验证实验设计](../knowledge/06-training/checkpoint-state-recovery-experiment.md)；[弹性训练与成员变更](../knowledge/06-training/elastic-training-and-membership.md)；[Checkpoint 写入与持久化边界](../knowledge/04-data-storage/checkpoint-durability.md)<br>已有持久化/训练状态分工、DCP 恢复专题和两套弹性样板；未明确的 NPU 协议与 mid-step 能力保持未知 | **维护**：基础范围暂无必补内容项；真实环境验证与平台/版本扩展另记。 |
| **06.8 恢复后的正确性与持续进展验证** | **已覆盖（基础）**<br>用身份/结构、逻辑进度、状态内容、同输入单步与持续窗口验证恢复 | [Checkpoint 恢复一致性](../knowledge/06-training/checkpoint-state-consistency.md)；[Checkpoint 恢复状态异常诊断指南](../knowledge/06-training/checkpoint-state-recovery-triage.md)；[Checkpoint 恢复状态异常来源案例](../knowledge/06-training/checkpoint-state-recovery-source-case.md)；[Checkpoint 恢复状态异常验证实验设计](../knowledge/06-training/checkpoint-state-recovery-experiment.md)；[GPU 到 NPU 的精度差异验证实验设计](../knowledge/06-training/gpu-npu-precision-difference-experiment.md)<br>已有分层验证、离散/浮点比较、数据进度、单步/持续窗口与 CPU DCP 分支/端到端/多 rank 方案 | **维护**：基础范围暂无必补内容项；真实环境验证与平台/版本扩展另记。 |

### 07 推理与服务系统

| 编号与主题 | 覆盖判断与核心范围 | 已有内容及依据 | 缺口与补齐方向 |
|---|---|---|---|
| **07.1 模型加载、prefill、decode 与执行路径** | **部分覆盖**<br>说明权重加载、引擎 ready、prefill/decode 及请求结束的执行和状态边界 | [一次推理请求的端到端路径](../knowledge/00-overview/inference-lifecycle.md)；[推理执行与 KV cache](../knowledge/07-inference/execution-and-kv-cache.md)；[昇腾推理 OOM 诊断指南](../knowledge/07-inference/ascend-inference-oom-triage.md)<br>prefill/decode/请求状态路径与启动期内存异常已说明 | **后续补齐**：缺少模型权重加载/格式/分片机制；缺少加载失败到 ready 的完整诊断与验证；不能把 KV 加载当权重加载 |
| **07.2 推理引擎及平台后端** | **部分覆盖**<br>说明推理引擎组件、平台后端、模型能力与支持条件，并比较实现边界 | [主机到模型执行的软件栈分层](../knowledge/02-software-stack/layers-and-boundaries.md)；[一次推理请求的端到端路径](../knowledge/00-overview/inference-lifecycle.md)；[推理执行与 KV cache](../knowledge/07-inference/execution-and-kv-cache.md)；[昇腾推理 OOM 诊断指南](../knowledge/07-inference/ascend-inference-oom-triage.md)<br>已有 vLLM 平台插件及 vLLM Ascend 固定功能/启动样板 | **后续补齐**：缺少引擎组件和后端执行基础；缺少 MindIE 等引擎实质内容与比较；缺少模型/硬件/功能交集档案 |
| **07.3 Batch、KV cache、内存与缓存管理** | **已覆盖（基础）**<br>解释迭代 batch、KV 容量、prefix 身份、引用/驱逐和内存压力的观测与验证 | [推理执行与 KV cache](../knowledge/07-inference/execution-and-kv-cache.md)；[昇腾推理 OOM 诊断指南](../knowledge/07-inference/ascend-inference-oom-triage.md)；[昇腾 NPU 内存与 OOM 证据](../knowledge/02-software-stack/ascend-memory-oom-evidence.md)；[昇腾推理长尾验证实验设计](../knowledge/07-inference/ascend-inference-tail-latency-experiment.md)<br>已有 vLLM KV 生命周期、抢占/重算、chunked prefill、NPU OOM 分支及冷/热缓存对照；结论限固定实现 | **维护**：基础范围暂无必补内容项；真实环境验证与平台/版本扩展另记。 |
| **07.4 量化、算子优化与输出质量验证** | **部分覆盖**<br>说明量化表示/算子路径、支持条件、优化代价与输出质量对照 | [推理量化与输出质量验证](../knowledge/07-inference/quantization-and-quality.md)；[GPU 到 NPU 的精度差异诊断指南](../knowledge/06-training/gpu-npu-precision-difference-triage.md)；[静默错误与计算完整性判定](../knowledge/08-reliability/silent-errors-and-integrity.md)<br>已有量化支持声明的读取、三层故障归因与固定任务评估原则 | **后续补齐**：缺少量化与算子优化机制；缺少评估指南正文/可执行方案及质量案例；KV 量化与 dtype 组合、部分硬件支持冲突待核 |
| **07.5 分布式推理、PD 分离与通信依赖** | **部分覆盖**<br>说明分布式推理布局、PD 角色、KV connector、通信依赖和失败语义 | [Prefill/Decode 分离（PD 分离）与流量分配](../knowledge/07-inference/pd-disaggregation.md)；[推理执行与 KV cache](../knowledge/07-inference/execution-and-kv-cache.md)；[推理延迟与吞吐指标字典](../knowledge/07-inference/latency-metrics.md)；[集合通信与 rank 进度](../knowledge/03-communication/collectives-and-rank-progress.md)<br>已有 PD 动机、connector 配置职责、重算/失败边界与 Ascend 限制 | **后续补齐**：缺少 TP/PP/DP 等分布式推理布局与选择；缺少跨机连接器前提/指标及完整失败链；其他引擎 PD 机制待补 |
| **07.6 路由、流控、扩缩容与版本发布** | **未覆盖**<br>定义路由、准入/流控、扩缩容、版本发布与回退，维持服务质量和容量 | 无直接正文。背景：[Prefill/Decode 分离（PD 分离）与流量分配](../knowledge/07-inference/pd-disaggregation.md)；[昇腾推理长尾诊断指南](../knowledge/07-inference/ascend-inference-tail-latency-triage.md)；[一次推理请求的端到端路径](../knowledge/00-overview/inference-lifecycle.md)<br>现有正文说明外部代理职责和请求排队，尚无服务控制策略正文 | **优先补齐**：缺少路由/流控算法与请求生命周期；缺少扩缩容和容量决策；缺少版本发布、摘除、回退与验证流程 |
| **07.7 TTFT、TPOT、吞吐、长尾与服务 SLO** | **已覆盖（基础）**<br>定义 TTFT/TPOT/ITL/吞吐/goodput/SLO 的观察点、统计和长尾验证 | [推理延迟与吞吐指标字典](../knowledge/07-inference/latency-metrics.md)；[昇腾推理长尾诊断指南](../knowledge/07-inference/ascend-inference-tail-latency-triage.md)；[昇腾推理长尾来源案例](../knowledge/07-inference/ascend-inference-tail-latency-source-case.md)；[昇腾推理长尾验证实验设计](../knowledge/07-inference/ascend-inference-tail-latency-experiment.md)<br>已有指标字典、失败过滤与聚合规则、长尾诊断/来源案例/负载对照；各后端实际指标可用性另核 | **维护**：基础范围暂无必补内容项；真实环境验证与平台/版本扩展另记。 |
| **07.8 OOM、请求失败、副本故障与服务恢复** | **部分覆盖**<br>区分 OOM、请求失败与副本故障，验证请求/状态/质量/性能恢复 | [昇腾推理 OOM 诊断指南](../knowledge/07-inference/ascend-inference-oom-triage.md)；[昇腾推理长尾诊断指南](../knowledge/07-inference/ascend-inference-tail-latency-triage.md)；[推理延迟与吞吐指标字典](../knowledge/07-inference/latency-metrics.md)；[Prefill/Decode 分离（PD 分离）与流量分配](../knowledge/07-inference/pd-disaggregation.md)<br>已有 NPU OOM 阶段诊断、错误/取消统计与 KV load failure 策略 | **后续补齐**：缺少副本故障、健康摘除与请求重试语义；缺少服务恢复与状态清理验证；缺少 GPU 对应 OOM/恢复专题 |

### 08 可靠性与计算正确性方法

| 编号与主题 | 覆盖判断与核心范围 | 已有内容及依据 | 缺口与补齐方向 |
|---|---|---|---|
| **08.1 可用性、正确性、性能稳定性与可恢复性** | **已覆盖（基础）**<br>分别定义可用性、正确性、性能稳定性、可恢复性的对象、指标及退出条件 | [可靠性维度与故障域](../knowledge/08-reliability/dimensions-and-failure-domains.md)；[Checkpoint 恢复一致性](../knowledge/06-training/checkpoint-state-consistency.md)；[推理延迟与吞吐指标字典](../knowledge/07-inference/latency-metrics.md)<br>已有四维框架、八项统计条件和恢复门槛，并连接训练状态及服务指标 | **维护**：基础范围暂无必补内容项；真实环境验证与平台/版本扩展另记。 |
| **08.2 故障模型、故障域、传播与相关故障** | **部分覆盖**<br>建模故障种类、共享依赖、传播链和相关故障，检验冗余与隔离假设 | [可靠性维度与故障域](../knowledge/08-reliability/dimensions-and-failure-domains.md)；[计算节点资源与拓扑参考](../knowledge/01-hardware/resource-topology.md)；[集合通信与 rank 进度](../knowledge/03-communication/collectives-and-rank-progress.md)；[静默错误与计算完整性判定](../knowledge/08-reliability/silent-errors-and-integrity.md)<br>已有故障域、共同原因/相关/独立边界及同步传播/灰色退化例子 | **后续补齐**：缺少故障模型的系统分类；缺少跨层传播图与失效模式分析；缺少关联故障/冗余失效的完整来源案例 |
| **08.3 可观测性、时间线与跨层证据关联** | **已覆盖（基础）**<br>区分症状/观测并对齐身份、工作键、时钟、覆盖与采集质量，形成跨层时间线 | [诊断中的证据、假设与结论](../knowledge/08-reliability/evidence-and-hypotheses.md)；[集合通信与 rank 进度](../knowledge/03-communication/collectives-and-rank-progress.md)；[训练数据供给路径与等待](../knowledge/04-data-storage/training-data-path.md)；[设备健康证据与检测边界](../knowledge/01-hardware/health-evidence.md)<br>已有五种记录对象、实体与时钟表、覆盖纪律、跨 rank 时间线和相邻边界证据；采集系统部署不在本行基础方法范围 | **维护**：基础范围暂无必补内容项；真实环境验证与平台/版本扩展另记。 |
| **08.4 故障发现、假设检验、归因与下一项检查** | **已覆盖（基础）**<br>维护支持/反驳/未知假设，选择有区分力的下一项检查并限制结论范围 | [诊断中的证据、假设与结论](../knowledge/08-reliability/evidence-and-hypotheses.md)；[慢 rank 诊断指南](../knowledge/06-training/slow-rank-triage.md)；[NCCL 超时诊断指南](../knowledge/03-communication/nccl-timeout-triage.md)；[HCCL 超时诊断指南](../knowledge/03-communication/hccl-timeout-triage.md)<br>已有假设检验、收益/代价/影响比较、两个明确合成例子和具体诊断分支 | **维护**：基础范围暂无必补内容项；真实环境验证与平台/版本扩展另记。 |
| **08.5 隔离、冗余、重试、降级与恢复原则** | **部分覆盖**<br>比较隔离、冗余、重试、降级与恢复的目标、代价和失败边界 | [可靠性维度与故障域](../knowledge/08-reliability/dimensions-and-failure-domains.md)；[弹性训练与成员变更](../knowledge/06-training/elastic-training-and-membership.md)；[Checkpoint 恢复一致性](../knowledge/06-training/checkpoint-state-consistency.md)；[Prefill/Decode 分离（PD 分离）与流量分配](../knowledge/07-inference/pd-disaggregation.md)<br>已有相关故障域/恢复门槛、训练副本与重启、KV 重算/失败的局部机制 | **优先补齐**：缺少跨领域处置原则与选择流程；缺少重试预算、幂等/重放和降级策略；缺少冗余/隔离失效案例与验证 |
| **08.6 数值异常、静默错误与计算完整性的判定方法** | **部分覆盖**<br>区分数值噪声、软件/数据错误和硬件 SDC，用覆盖明确的校验与对照推进判定 | [静默错误与计算完整性判定](../knowledge/08-reliability/silent-errors-and-integrity.md)；[GPU 到 NPU 的精度差异诊断指南](../knowledge/06-training/gpu-npu-precision-difference-triage.md)；[GPU 到 NPU 的精度差异验证实验设计](../knowledge/06-training/gpu-npu-precision-difference-experiment.md)；[Checkpoint 完整性与校验证据](../knowledge/04-data-storage/checkpoint-integrity-evidence.md)<br>已有误差背景、SDC 候选门槛、检测方法分层和字节/应用完整性边界 | **后续补齐**：缺少 NPU SDC 一手依据；缺少训练侧更完整的检测/传播与校验方法正文；部分检测分类目前只有目录级证据 |
| **08.7 验收、基准、压力测试与故障注入方法** | **部分覆盖**<br>设计验收、基准、压力和故障注入的对象、对照、统计、预算与恢复判据 | [新节点与返修节点验收](../knowledge/01-hardware/node-acceptance-triage.md)；[通信带宽与性能基线口径](../knowledge/03-communication/bandwidth-baselines.md)；[NCCL 超时验证实验设计](../knowledge/03-communication/nccl-timeout-experiment.md)；[HCCL 超时验证实验设计](../knowledge/03-communication/hccl-timeout-experiment.md)；[昇腾版本配套失败验证实验设计](../knowledge/02-software-stack/ascend-version-mismatch-experiment.md)；[容器内 NPU 不可见验证实验设计](../knowledge/05-cluster-platform/ascend-device-visibility-experiment.md)；[GPU 到 NPU 的精度差异验证实验设计](../knowledge/06-training/gpu-npu-precision-difference-experiment.md)；[Checkpoint 恢复状态异常验证实验设计](../knowledge/06-training/checkpoint-state-recovery-experiment.md)；[昇腾推理长尾验证实验设计](../knowledge/07-inference/ascend-inference-tail-latency-experiment.md)<br>已有节点四层验收、通信基线及七份有停止/恢复条件的验证方案 | **优先补齐**：缺少统一测试选择与覆盖矩阵；缺少压力测试/注入模型与统计方法；缺少基于真实环境的结果证据，实测另行推进 |
| **08.8 可靠性指标、恢复损失、事故复盘与知识更新** | **部分覆盖**<br>定义可靠性/恢复损失指标，记录事故时间线与复盘，并把新证据转成修订 | [可靠性维度与故障域](../knowledge/08-reliability/dimensions-and-failure-domains.md)；[Checkpoint 恢复一致性](../knowledge/06-training/checkpoint-state-consistency.md)；[弹性训练与成员变更](../knowledge/06-training/elastic-training-and-membership.md)；[推理延迟与吞吐指标字典](../knowledge/07-inference/latency-metrics.md)<br>已有指标记录、进度损失/恢复门槛和来源案例的调查记录结构 | **后续补齐**：缺少有效训练产出、重算/回放损失和长期可靠性统计；缺少正式事故复盘与知识更新方法；缺少独立诊断评测集 |

## 尚无主干正文的主题与优先依赖

以下 7 个主题需要建立主干内容。相关背景可复用，但不能替代本主题正文：

| 主题 | 首个可验收补齐目标 | 主要依赖 |
|---|---|---|
| 00.4 参考架构 | 单机/集群/超节点图，包含组成、路径、故障域与选择条件 | 01.4、03.1，已有资源拓扑 |
| 03.2 网络与 RDMA | 协议/队列/内存机制、IB/RoCE 差异及独立基线 | 01.2、03.1 |
| 04.2 存储实现 | 四类存储接口/缓存/一致性/持久性及选型比较 | 02.1、03.2，已有持久化边界 |
| 05.5 多租户与容量 | 隔离/共享模型、争用证据、容量准入与验证 | 01.2、02.6、05.4、07.3 |
| 05.6 平台变更 | 上下线/drain/回收、升级/发布/回退与回服验证 | 已有 01.6/02.7/05.3，补充 05.2 |
| 06.4 训练/后训练工作流 | 预训练/微调/RL 关系，rollout 与权重同步的一致性及性能边界 | 06.1、06.2、06.3、07.1/07.2 |
| 07.6 服务控制 | 路由/流控、扩缩容、发布/摘除/回退及服务验收 | 05.5、05.6、07.1/07.2/07.7 |

内容补齐建议先处理主机/内存与软件执行基础（01.2、01.3、02.1、02.2、02.6），再推进网络/RDMA 与存储主干（03.1–03.3、04.1–04.4）。平台隔离/变更、RL 和服务控制随后按依赖推进。已存在较完整的 Checkpoint、通信进度和指标内容可直接复用。

这只是内容优先级建议，来源、实现版本、文件边界及单批验收还需在任务拆分时固定。高优先级不代表已有正文存在高优先级审阅缺陷。

## 七份验证方案的独立证据缺口

七份方案都是待执行的验证方法。它们可支撑“如何验证”的文字覆盖，当前均不能支撑“已实测通过”。

| 方案 | 执行环境与首要补齐项 |
|---|---|
| [昇腾版本配套失败验证实验设计](../knowledge/02-software-stack/ascend-version-mismatch-experiment.md) | 独立 NPU 节点；完整硬件/HDK/OS/软件制品基线、单变量版本组、脚本与回退记录。 |
| [容器内 NPU 不可见验证实验设计](../knowledge/05-cluster-platform/ascend-device-visibility-experiment.md) | 独立 NPU/Kubernetes 环境；插件/runtime/资源名、Pod 规格、设备身份链与清理/回收记录。 |
| [HCCL 超时验证实验设计](../knowledge/03-communication/hccl-timeout-experiment.md) | 多 NPU，跨机问题另需对应网络；配套 HCCL Test、rank/group/时钟、全参与者结果检查及恢复。 |
| [NCCL 超时验证实验设计](../knowledge/03-communication/nccl-timeout-experiment.md) | 多 GPU，跨机问题另需对应网络；构建与版本、观测可用性、全 rank 时间线、进程回收及恢复。 |
| [GPU 到 NPU 的精度差异验证实验设计](../knowledge/06-training/gpu-npu-precision-difference-experiment.md) | GPU 与 NPU 独立环境；相同输入/状态、各平台重复基线、指标/容差及有限传播/任务质量判据。 |
| [Checkpoint 恢复状态异常验证实验设计](../knowledge/06-training/checkpoint-state-recovery-experiment.md) | 可先用 CPU；固定 parent/commit 同构建对照、脚本、真实 missing-FQN 输入、DCP 回调快照及多 rank 身份映射。 |
| [昇腾推理长尾验证实验设计](../knowledge/07-inference/ascend-inference-tail-latency-experiment.md) | 独立 NPU 服务/负载客户端；模型/请求身份、冷热缓存、实际到达序列、重复/样本量、SLO 与质量判据。 |

实测任务与正文补齐分别排期。先完成环境档案、脚本/输入、预先判据与资源/恢复安排，再运行基线/对照/恢复、保存真实证据并复核。结果可支持或反驳假设，也可能无法判断；不为了关闭盘点项而要求结果符合预期。

## 后续 Batch 数如何确定

**后续规划更新（2026-10-08）：** 本盘点已用于[完整覆盖路线图](full-coverage-roadmap.md)与[执行清单](../plans/full-coverage-backlog.yaml)，排定 85 项内容任务、Batch 13–32 共 20 批。63 个主题和 141 条缺口已有逐项映射，所有执行状态仍 planned；原 12/44/7 的覆盖快照保持不变。下文保留盘点时的估算方法。

盘点时的 51 个待补主题是**主题缺口**，尚不是同样数量的新增文章：一题可需多个任务，一篇可复用到多题，部分缺口适合修订已有正文。不能用 63−56 或待补主题数÷3 得出最终 Batch 数。

本次后续规划已将这些缺口拆成具体新增/修订任务，列明目标文件、来源获取范围、依赖与关闭条件，并合并共同内容按每批 3–5 项分组；具体来源版本仍须在所属批次准备阶段固定。排定批次基线见上方链接；实际必要的来源/范围变化可调整批次数，本盘点本身不承诺固定最终总数。网站、API、现场适配与独立评测工程另按架构阶段管理。

后续批次审阅沿用 `gpt-6.1-sol / xhigh`，问题修订后做定向复核；内容覆盖、编辑审阅、来源核对与实测验证分别维护。

## 输入追溯与核对

全部 56 篇正文/方案都已映射到至少一个主题（直接证据或背景），没有遗漏的正文。四条路径仅用于 00.6 的导航覆盖；九个领域首页保留在输入清单中，不计作技术正文。

逐文件身份、平台、编辑/验证状态、核对章节和 SHA-256 见 YAML 的 `documents`；原目录、registry 与 catalog 摘要见 `input_snapshot`。本文与 YAML 是规划记录，放在 docs/plans，不新增知识正文或来源，也不纳入正文产量。

2026-10-08 交付核对：`make check` 与 `make build` 均通过，仍为 69 content entries / 84 sources。另核对原目录的 63 个编号与题名、每行唯一性、覆盖分类/领域小计、全部 69 个输入条目的 ID/元数据/文件摘要/核对章节、56 篇正文的映射，以及盘点表/README/填充计划的 371 处本地文件链接，全部一致。YAML 的 `validation` 保留核对结果。

这些检查确认编号、引用、摘要和统计，不证明覆盖判断之外的技术正确性、远程资料或现场兼容性；本次没有修改校验工具或执行硬件实验。
