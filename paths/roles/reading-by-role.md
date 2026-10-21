---
id: path.role.reading-by-role
title: 按角色组织的阅读路径
type: path
domain: overview
status: draft
platforms:
- generic
source_refs:
- src.stas.ml-engineering
- src.infrasys.aiinfra
updated_at: '2026-10-21'
summary: 为学习者、架构设计者与运维/可靠性人员分别给出进入条件、阅读顺序、可回答问题与完成检查。
related_ids:
- overview.index
- overview.terms-and-system-boundaries
- overview.training-lifecycle
- overview.inference-lifecycle
- overview.reference-architectures
- overview.design-targets-and-tradeoffs
- hardware.index
- software-stack.index
- communication.index
- data-storage.index
- cluster-platform.index
- training.index
- inference.index
- reliability.index
- path.task.training-triage
- path.task.inference-triage
- path.platform.ascend
- path.platform.nvidia
---

# 按角色组织的阅读路径

本页为三类读者安排阅读顺序：每条路径有进入条件、知识目标、可回答的问题与完成检查。路径只链接已交付正文，不保存重复解释；`generic` 表示导航意图，不表示任何平台兼容。全部正文均为 draft、未经本地环境实测——路径中出现的操作、样板与验证方法都带有各自的适用条件，进入正文后先读其边界。

## 学习者：建立系统全景

**进入条件**：熟悉 Linux 命令行与 Python；不需要并行计算或集群经验。

**知识目标**：能说清一次训练任务和一次推理请求分别穿过哪些层、每层负责什么；掌握本库统一术语；知道去哪里继续深入。

**阅读顺序**（先后有序，每步的先修是前一步）：

1. [统一术语、先修关系与系统责任边界](../../knowledge/00-overview/terms-and-system-boundaries.md)：设备/节点/超节点、rank/worker/副本、驱动/运行时/框架后端等易混概念的同名异义与错误归属反例。
2. [一次训练任务的端到端路径](../../knowledge/00-overview/training-lifecycle.md)：准入→初始化→step→保存恢复的四条线。
3. [一次推理请求的端到端路径](../../knowledge/00-overview/inference-lifecycle.md)：请求→排队→prefill/decode→释放，以及客户端/服务端计时差异。
4. [主机到模型执行的软件栈分层](../../knowledge/02-software-stack/layers-and-boundaries.md)：驱动、运行时、基础库、框架后端的职责与调用关系。
5. [02 软件栈总览](../../knowledge/02-software-stack/index.md)与其余领域入口按需浏览：[01 硬件](../../knowledge/01-hardware/index.md)、[03 通信](../../knowledge/03-communication/index.md)、[04 数据与存储](../../knowledge/04-data-storage/index.md)、[05 集群平台](../../knowledge/05-cluster-platform/index.md)、[06 训练](../../knowledge/06-training/index.md)、[07 推理](../../knowledge/07-inference/index.md)、[08 可靠性](../../knowledge/08-reliability/index.md)。

**能回答的问题**：训练和推理分别卡在"资源已分配但框架未就绪"时，问题可能在哪几层？"rank 3 timeout"与"step 100"可能来自不同对象吗？checkpoint 保存完成为什么还不等于能正确续训？

**完成检查**：能沿两篇端到端路径复述每个阶段的观察点；能从[术语页](../../knowledge/00-overview/terms-and-system-boundaries.md)按症状找到责任领域入口。

## 架构设计者：选型与设计权衡

**进入条件**：有分布式系统基础；正负责训练/推理平台的选型、容量或架构设计。

**知识目标**：把可靠性、性能、容量、成本、能耗五类目标转成可比较的设计决策；知道每个平台结论的证据边界。

**阅读顺序**：

1. [单机、集群与超节点的参考架构及选择](../../knowledge/00-overview/reference-architectures.md)：三类组织、控制/数据/管理路径与官方超节点样板。
2. [容量、成本、能耗与可靠性目标的设计权衡](../../knowledge/00-overview/design-targets-and-tradeoffs.md)：五类目标的度量口径、假设计算示例与验收表。
3. [机柜供电、散热预算与共享依赖](../../knowledge/01-hardware/rack-power-cooling-and-failure-domains.md)与[节点资源与拓扑](../../knowledge/01-hardware/resource-topology.md)：故障域与局部性约束。
4. [互联路径参考](../../knowledge/03-communication/interconnect-paths.md)与[存储版本化参考](../../knowledge/04-data-storage/local-and-shared-storage.md)：网络与存储的选型条件。
5. [容器与设备暴露基线](../../knowledge/05-cluster-platform/container-image-runtime-baseline.md)与[作业生命周期](../../knowledge/05-cluster-platform/kubernetes-job-lifecycle.md)：平台层职责。
6. [并行策略与选型表](../../knowledge/06-training/parallelism-and-state.md)与[分布式推理布局](../../knowledge/07-inference/distributed-inference-layouts.md)：并行决定的资源形态。
7. [三平台安装基线、迁移升级与回退验证](../../knowledge/02-software-stack/environment-installation-and-upgrade.md)与[兼容性证据方法](../../knowledge/02-software-stack/compatibility-evidence.md)：变更的准入门槛与证据判定。
8. [可靠性维度与故障域](../../knowledge/08-reliability/dimensions-and-failure-domains.md)与[故障模型与传播](../../knowledge/08-reliability/fault-models-and-propagation.md)：把失效模式纳入设计。

**能回答的问题**：超节点相对集群换来了什么、付出了什么共享故障域？某"官方支持"的平台组合证据是文档声明、源码状态还是实测？升级某层组件前必须先确认哪些回退条件？

**完成检查**：能对给定场景（节点数、模型规模、可用性目标）写出五类目标的主次与验收表；能指出任一选型结论的证据类型与边界（很多为文档样板、未实测）。

## 运维/可靠性人员：排障、观测与恢复验证

**进入条件**：负责训练/推理集群的日常运行、故障处置或复盘；了解本库术语页内容。

**知识目标**：按证据分支定位故障而不跳到结论；掌握跨层时间线与指标分母；恢复后有可判定的验证。

**阅读顺序**：

1. [可靠性方法总览](../../knowledge/08-reliability/index.md)与[证据与假设](../../knowledge/08-reliability/evidence-and-hypotheses.md)：症状/事件/观察/假设/结论的纪律。
2. [训练排障路径](../tasks/training-triage.md)与[推理排障路径](../tasks/inference-triage.md)：按现象找首要入口（平台分支见[昇腾](../platforms/ascend.md)/[NVIDIA](../platforms/nvidia.md)专题）。
3. 领域分诊按需进入：[HCCL 超时](../../knowledge/03-communication/hccl-timeout-triage.md)、[NCCL 超时](../../knowledge/03-communication/nccl-timeout-triage.md)、[慢 rank](../../knowledge/06-training/slow-rank-triage.md)、[数据饥饿](../../knowledge/04-data-storage/data-starvation-triage.md)、[推理 OOM（GPU/昇腾）](../../knowledge/07-inference/gpu-inference-oom-triage.md)、[版本错配](../../knowledge/02-software-stack/ascend-version-mismatch-triage.md)。
4. [隔离、重试预算、降级与恢复选择](../../knowledge/08-reliability/mitigation-and-recovery-principles.md)与[可靠性统计、有效产出与恢复损失](../../knowledge/08-reliability/reliability-metrics-and-recovery-loss.md)：处置选择与损失记账。
5. [静默错误与计算完整性](../../knowledge/08-reliability/silent-errors-and-integrity.md)：健康全绿但结果异常时的分层判定。
6. [测试选择、压力注入与统计方法](../../knowledge/08-reliability/test-design-and-coverage.md)与[事故复盘与知识更新](../../knowledge/08-reliability/postmortem-and-knowledge-update.md)：验收方法与复盘闭环。

**能回答的问题**：最先打印 timeout 的 rank 是根因吗？恢复后除了"服务起来了"还要验证什么、分母怎么取？一次复盘应该更新哪些来源与正文？

**完成检查**：能从任一现象出发走完"现象→证据→假设→下一项检查→停止判据"链；能列出自己环境里尚未验证的操作与样板条件（本库全部实验设计未执行、验证方案 0/7）。

## 逐链检查与纸面演练（T00-05 验收记录，2026-10-21）

- **逐链检查**：本页全部内链经 `make check` 通过——**2026-10-21 快照：128 content entries / 577 sources（含本页）**。三条路径引用的目标正文均为已交付正文：早期批次（Batch 01–12）交付、其中多篇经 Batch 13–31 修订/复核，本批新增正文见 Batch 31 各记录；未引用未交付正文。
- **纸面演练**（三问三答，逐跳记录；题设假设显式声明）：
  - **①"训练容器报 OOM 但节点内存充足"**（题设假设：NVIDIA/CUDA 语境、报错出现在框架完成初始化后的首个大算子执行阶段——若实际失败在初始化期，分流见下）。路线：学习者路径第 2 步 → [端到端路径](../../knowledge/00-overview/training-lifecycle.md)"每个阶段应进入哪层知识"表 → "框架初始化"行（目标为 [软件栈分层](../../knowledge/02-software-stack/layers-and-boundaries.md)）→ 经该文文末领域入口到 [02 域](../../knowledge/02-software-stack/index.md) → [GPU 内存与 OOM 证据](../../knowledge/02-software-stack/gpu-memory-oom-evidence.md)。可支持的回答：节点（主机）内存充足不排除**设备内存** OOM——该文要求至少分开四层观察（物理设备内存、框架分配器统计、workspace/外部库缓存、graph 私有池），且用途分类不是互斥账户（workspace/graph 占用可已计入 allocated/reserved 聚合，不能跨口径相加），定位先明确观察口径；失败在初始化而非执行期时，另走 [框架后端适配](../../knowledge/02-software-stack/framework-backend-adaptation.md)。先修核对：rank/驱动/运行时概念已由路径第 1 步术语页覆盖。
  - **②"超节点还是集群"**。路线：架构路径第 1 → 2 步直达 [参考架构及选择](../../knowledge/00-overview/reference-architectures.md)与[设计目标与权衡](../../knowledge/00-overview/design-targets-and-tradeoffs.md)。可支持的回答：三类组织在控制/数据/管理路径与共享故障域上的差异、两个官方超节点样板的约束比较；五类目标的取舍口径与验收表模板见第二篇。纸面待确认项：具体量化结论依赖环境，正文标注为假设示例（未实测）。
  - **③"故障重启后训练是否正确续训"**。路线：运维路径第 2 步 → [训练排障](../tasks/training-triage.md)"checkpoint 读取失败或恢复后状态异常"行（首要入口 06 域）→ [06 首页](../../knowledge/06-training/index.md) → [Checkpoint 恢复一致性](../../knowledge/06-training/checkpoint-state-consistency.md)"恢复后验证"节。可支持的回答：恢复验证分层（身份/结构→逻辑进度→状态内容→同输入单步→持续窗口）；状态恢复是应用责任，文件可读与 load 返回只是链路一部分。先修核对：四条状态线由路径第 1 步与训练全流程（第 2 步）覆盖。
- **边界**：演练是纸面导航检查，不是实测，不产生任何运行结果；各路径中"未验证/未实测"标注以所链正文为准。

## 原始资料入口

- [ML Engineering](https://github.com/stas00/ml-engineering)：训练/推理工程实践经验入口（学习者与运维路径的延伸阅读）。
- [AIInfra 项目仓库](https://github.com/Infrasys-AI/AIInfra)：全栈主题组织与中文资料索引入口（架构路径的延伸阅读）。

以上为外部入口，引用前需核对各自版本与许可。
