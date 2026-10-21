---
id: reliability.test-design-and-coverage
type: reference
domain: reliability
status: draft
title: 统一测试选择、压力/注入与统计方法
platforms: [generic]
source_refs:
  - src.google.sre-testing-reliability
  - src.paper.kalibera-jones-effectsize-2020
  - src.mlcommons.storage-rules-v2.0
  - src.nvidia.nccl-tests-b4d5beeb
  - src.huawei.hccl-perf-test-guide-cann-9.1.x
  - src.usenix.superbench-atc24
  - src.ocp.sdc-in-ai-2025
  - src.google.sre-effective-troubleshooting
updated_at: "2026-10-21"
summary: 给出验收/基准/压力/故障注入四类测试的选择与覆盖矩阵（对象、故障模型、所问问题、检测覆盖、资源、风险、恢复），统一重复/随机化/warmup/样本量与置信区间/多重比较等统计纪律与预注册判据，并汇总本库七份实验方案的准备状态——真实环境执行仍为 0/7。
related_ids:
  - reliability.silent-errors-and-integrity
  - reliability.fault-models-and-propagation
  - reliability.mitigation-and-recovery-principles
  - hardware.node-acceptance-triage
  - communication.bandwidth-baselines
  - reliability.reliability-metrics-and-recovery-loss
verification:
  status: source_checked
  evidence_refs:
    - src.google.sre-testing-reliability
    - src.paper.kalibera-jones-effectsize-2020
    - src.mlcommons.storage-rules-v2.0
    - src.nvidia.nccl-tests-b4d5beeb
    - src.huawei.hccl-perf-test-guide-cann-9.1.x
  notes: "本批核读 SRE Book 第 17 章 Testing for Reliability 全文（CC BY-NC-ND 4.0，仅归纳）、Kalibera & Jones arXiv:2007.10899 全文（重复层级、效应量置信区间、warm-up 成本与最优重复公式 Eq.13–14、bootstrap CI 章节）、MLPerf Storage v2.0 计次/缓存条款、nccl-tests 固定快照计时/校验实现与 HCCL 9.1.X 性能测试指南（既有登记口径）。本文是方法框架，没有任何本地执行；七份方案的真实执行状态以 plans/validation-backlog.yaml 为准。"
---

# 统一测试选择、压力/注入与统计方法

同一条“测试通过”结论在验收、基准、压力与注入四类活动中含义不同。本文回答三个问题：给定一个可靠性疑问，**选哪类测试、怎么声明它的覆盖**；**结果怎么统计才可比较**；**注入和压力怎么设计才既有效又可恢复**。测试对象的具体机制（设备诊断、通信基线、精度比对）归各域正文；本文提供统一的选择与判读框架。SRE 对测试的经典定位可作为总纲：测试量化对可靠性的信心，**通过的测试不证明可靠，失败的测试一般证明不可靠**（[Testing for Reliability](https://sre.google/sre-book/testing-reliability/)）。

`generic` 表示框架跨平台通用；各平台工具与字段按已登记版本在对应正文查询，环境未知时不假设任何测试可运行。

## 一、选择矩阵：先声明对象与所问问题

选测试前先填表。填不出来的格子就是该测试尚不能声称的覆盖——不是事后补的理由。

| 维度 | 验收（acceptance） | 基准（benchmark） | 压力（stress） | 注入（injection） |
|---|---|---|---|---|
| 典型对象 | 新到/修复后的节点、环境变更后的栈 | 已验收环境的性能特征（带宽、吞吐、时延） | 系统与组件的极限与降级方式 | 显式构造的故障模型 |
| 所问问题 | “这台设备/这套栈现在能否交付约定的服务” | “在此负载定义下性能是多少，与基线差多少” | “到哪里会坏、坏成什么样、是否优雅降级” | “这个故障被观测到吗、检测机制响应正确吗、传播与处置假设成立吗” |
| 对应故障模型 | 未指明单点；按验收层级覆盖（部件/驱动/通信/端到端，见[节点验收](../01-hardware/node-acceptance-triage.md)） | 无故障前提下的性能口径 | 资源耗尽类（SRE 章节的 stress test 即“数据库写到多满开始失败”一类极限问题） | 按目标故障模型逐项声明（位置/强度/时序，见第三节） |
| 检测覆盖的声明方式 | 通过＝覆盖到的检查项当次通过；**不得表述为“无故障”** | 结果只在固定口径内可比（消息、rank、单位，见[带宽基线](../03-communication/bandwidth-baselines.md)） | 覆盖到实际触发的极限路径；未触发的退化模式不声称 | 覆盖＝被注入的故障模型×观测点；检出≠发生率 |
| 资源成本 | 分钟级，随验收层级上升 | 有限、可重复 | 有破坏风险，需预算与隔离环境 | 需可牺牲环境或预算的合成注入 |
| 风险与恢复 | 低（只读查询为主，主动诊断另计） | 低（需防缓存/后台负载污染） | 高：可能压垮共享依赖，见第三节停止条件 | 高：可能触发未预期的传播/处置，见第三节字段 |
| 与真实健康的关系 | 必要不充分 | 性能≠正确性 | 极限≠日常 | **合成注入检出不构成真实故障证据，只评估检测/处置方法**（见[静默错误](silent-errors-and-integrity.md)注入地位一节） |

SRE 章节对生产环境测试的两点提醒同样适用于集群：**rollout 会让生产环境“不属于任何一个版本”**（测试可能拿新配置打旧二进制，结论只在该组合内成立）；**canary 不是测试而是“结构化的用户验收”**——它把新版本暴露给真实流量，不保证捕获新引入的故障，其指数放量节奏（0.1%→1%→10%→100%）是风险控制而非覆盖声明（[同章](https://sre.google/sre-book/testing-reliability/)）。

**“测试通过”的四条边界**（汇总，避免重复犯错）：

1. 通过的测试不证明可靠（SRE）；
2. 通过的验收不排除未覆盖故障模式（本库[节点验收](../01-hardware/node-acceptance-triage.md)同口径）；
3. 主动检测（如 DCGM diagnostic、SDC 扫描）通过不等于无 SDC（覆盖取决于输入与触发条件，见[静默错误](silent-errors-and-integrity.md)）；
4. 注入环境里的检出/恢复成功不证明生产同型故障必然同样表现（环境差异与观测者效应）。

## 二、统计纪律：比较之前先固定口径

以下纪律适用于所有四类活动中的量化结论。方法依据为 Kalibera & Jones 对性能量化的系统方法（[arXiv:2007.10899](https://arxiv.org/abs/2007.10899)）：

1. **重复与层级**：明确重复发生在哪一层（同一进程内多次迭代 / 多次执行 / 多次构建或多次环境实例）。各层方差不同，混层平均会低估不确定性。论文给出按各层方差与成本分配最优重复次数的公式（Eq. 13–14：最优重复数只依赖相邻两层的方差比与成本比）；至少应记录实际采用的每层次数。
2. **warm-up 与稳态**：预热期样本应从汇总中剔除并单独记录剔除规则（论文把 warm-up 计为执行成本 `c1`，稳态样本数随预热成本升高而升高）。集群语境的对应物：首个 epoch/首批请求、缓存冷热（MLPerf Storage 对 checkpoint 负载规定客户端内存不足 3 倍须 `drop_caches`，nccl-tests 用 `-w` 预热且 `-c` 校验不进计时——这些是“把缓存与校验状态写进规则”的样板）。
3. **随机化与次序效应**：多配置实验应随机化执行顺序或显式交换次序并重复，否则把漂移（温度、后台任务、缓存）误记为配置差异；Kalibera & Jones §2.1 列举了虚拟-物理页映射等需要随机化处理的随机效应因素。
4. **单因素与对照**：一次只变一个声明过的因素，其余固定并记录；需要多因素时用全因子/部分因子设计并写明哪些交互不检验。无对照组的“改前改后”在长周期集群上不可解释（负载自身在变）。
5. **样本量与置信区间**：报告效应量（如前后均值之比）及其置信区间，而不是只报告均值或“更快了”。论文推荐对执行时间比构造效应量置信区间（其 §7.3.1 给出 bootstrap 区间方法）；**本库不给任何通用的“p99 至少 N 个样本”硬阈值**——分位数估计的不确定性取决于分布形状与样本量，正确做法是报告区间或按目标区间宽度用初始实验方差反推需要的重复数（论文 §7.4 的规划公式），并写明假设（如正态性假设在多数量化方法中常被省略但并不自动成立）。
6. **多重比较**：同一批数据上检验多个阈值/多个算子/多个指标时，逐个按名义水平判读会放大假阳性；预注册判据（见下）限定主判据数量，次要指标只作描述或做多重性校正后再判读。
7. **预注册判据与无结果记录**：执行前写下主判据、通过/失败阈值、停止条件与计划样本量（SuperBench 是把判据完全前置的样板：以集群 build-out 全集的无监督 CDF 相似度作判据、单向只判更差、迭代剔除后取中位样本，见其 ATC 2024 论文）。**“无差异”也是结果，按原判据记录**，不得事后改成“看起来好一些”。
8. **停止与放弃记录**：中途停止（预算用尽、环境失稳、注入触发未预期影响）时记录已跑部分与停止原因；不得把停止前样本当作完整实验判读。

一个可复用的记录骨架：`{对象与环境档案, 所问问题, 声明的故障模型/因素, 每层重复数与随机化方式, warm-up/缓存处理, 主判据与预注册阈值, 实际执行范围, 效应量与区间, 无结果/停止记录}`。

## 三、注入与压力的设计字段

### 注入模型（合成故障）

每个注入用例必须写明六字段，缺一即不可执行：

| 字段 | 说明 | 反例（缺字段时不可声称的结论） |
|---|---|---|
| 位置 | 故障注入在栈的哪一层、哪个实体（链路/设备/进程/算子输出/数据文件/配置） | 不写位置则无法解释“检出/未检出”是哪一层的覆盖 |
| 持续时间 | 单次、有限时长、间歇（含周期与占空比）还是持续到停止条件 | 一次性注入不能声称覆盖间歇故障 |
| 强度 | 损坏位数/丢包率/延迟量/降频幅度等，及强度序列 | 单一强度不能声称覆盖“随强度变化的检测边界” |
| 故障域 | 波及范围与隔离边界（哪张卡/哪个 rank 组/哪个 namespace 之外不受影响是**待验证的隔离假设**） | 见[故障模型](fault-models-and-propagation.md)：隔离假设要用注入验证，不是默认成立 |
| 预期证据 | 各观测点应出现的信号（日志、计数器、应用侧表现），以及**应保持不变的对照点** | 无预期证据则“没有反应”不可判读 |
| 非预期影响 | 可能被误触发的处置机制（重试风暴、驱逐、告警外溢到值班）、污染的共享状态及恢复方法 | 未声明非预期影响的注入在共享环境上不可执行 |

三类必须区分的结论：**合成注入的检出**只证明该检测方法对该位置/强度/时序有覆盖；**真实事故**是生产发生的独立证据，二者不可互相冒充；**对真实案例的复盘**（如[相关故障案例](correlated-failure-source-case.md)）是第三类证据。注入评估 SDC 检测方法时的专门边界见[静默错误](silent-errors-and-integrity.md)。

### 压力测试

SRE 章节的定位是“找到系统与组件的极限”，并提醒许多组件越过某点后不是优雅降级而是灾难性失败（[同章](https://sre.google/sre-book/testing-reliability/)）。执行压力测试前必须声明：

- **有限预算**：最大并发/数据量/时长/迭代数的上界，以及资源成本归属；
- **停止条件**：达到目标指标、错误率/延迟越过阈值、或触发预期外的处置动作——任一命中即停并保留现场；
- **恢复条件**：结束后如何确认系统回到健康窗口（不只是“进程还在跑”，见[可靠性指标](reliability-metrics-and-recovery-loss.md)的健康窗口定义），以及失败时如何回退（清理数据、重置计数器、重启受影响组件）；
- **共享依赖保护**：压测目标的上游/下游（共享存储、生产网络、控制面）是否被波及，波及时谁负责通知与止损。

## 四、本库七份验证方案的准备矩阵

以下七份方案均为**设计文档**（`verification: not_verified`），真实环境执行状态 **0/7**；执行与证据采集由 [plans/validation-backlog.yaml](../../plans/validation-backlog.yaml) 的 V 工作包按各自环境推进，**本文或任何正文完成都不改变该状态**。准备矩阵按第二节的记录骨架核对：

| 方案 | 所问问题（摘要） | 预先判据与停止条件 | 执行/采集/恢复安排 | 真实执行 |
|---|---|---|---|---|
| [NCCL 超时实验](../03-communication/nccl-timeout-experiment.md) | 慢 rank/缺席 rank 如何表现为 watchdog 超时与日志证据 | 已定义超时窗口与逐 rank 证据采集点 | 有（可牺牲环境、日志采集、清理） | 0 |
| [HCCL 超时实验](../03-communication/hccl-timeout-experiment.md) | Ascend 侧同类症状的 HCCL 表现与诊断路径 | 同上（HCCL 口径） | 有 | 0 |
| [昇腾版本失配实验](../02-software-stack/ascend-version-mismatch-experiment.md) | 版本组合失配的错误形态与最小定位证据 | 已定义核对清单与预期错误类别 | 有 | 0 |
| [昇腾设备可见性实验](../05-cluster-platform/ascend-device-visibility-experiment.md) | 物理存在→驱动可见→可分配→容器可用的断链定位 | 已定义四层检查点 | 有 | 0 |
| [GPU→NPU 精度差异实验](../06-training/gpu-npu-precision-difference-experiment.md) | 固定口径下数值差异的量化与容差判读 | 已固定 dtype/开关/容差（预注册） | 有 | 0 |
| [checkpoint 状态恢复实验](../06-training/checkpoint-state-recovery-experiment.md) | 恢复后优化器/数据进度一致性的验证判据 | 已定义逐状态核对项 | 有 | 0 |
| [推理长尾实验](../07-inference/ascend-inference-tail-latency-experiment.md) | 负载定义与长尾时延的对照测量 | 已定义负载档位与尾分位判读口径 | 有 | 0 |

环境档案（`environment_refs`）目前全部为空——这是执行前的共同缺口；各方案补充环境档案前不得声称可运行。结果复核遵循第七节“来源核对、报告交付、问题修订、定向复核分别记录”的批次约定。

## 五、与相邻正文的分工

- 故障模型与传播路径：[故障模型与传播](fault-models-and-propagation.md)（注入用例的“位置/故障域”两字段从其 FMEA 行取值）；
- 处置与恢复的选择：[隔离、重试预算、降级与恢复选择](mitigation-and-recovery-principles.md)（压力/注入的“恢复条件”字段从其恢复选择表取值；其“有限故障对照设计”即本文注入字段的一个已登记应用）；
- SDC 检测方法的覆盖与假阴性：[静默错误](silent-errors-and-integrity.md)；
- 指标口径与效应量计算例：[可靠性指标与恢复损失](reliability-metrics-and-recovery-loss.md)；
- 节点验收层级与设备侧工具：[节点验收](../01-hardware/node-acceptance-triage.md)、[设备健康证据](../01-hardware/health-evidence.md)；
- 通信基线口径：[带宽基线](../03-communication/bandwidth-baselines.md)。

## 六、适用边界

- 本文是**方法框架与登记状态**，不是执行结果；不含任何本地测量、注入或压力数据。
- 统计方法引 Kalibera & Jones 与 SRE 章节的原文范围；论文示例为软件系统性能量化，迁移到 GPU/NPU 集群时方差结构与成本模型需按第二节的骨架重新估计，公式不可照搬数值。
- 不给通用最小样本量、通用“正常波动范围”或跨平台阈值；这些只能由固定环境档案下的初始实验估计并随环境变更复核。
- MLPerf/nccl-tests/HCCL 的规则条款是**各家基准的定义**，引用其条款不等于本库执行了这些基准。

## 来源核对范围

- [Google SRE Book, Ch.17 Testing for Reliability](https://sre.google/sre-book/testing-reliability/)（CC BY-NC-ND 4.0）：本批全文核读——测试与 MTTR/MTBF 关系、传统测试（unit/integration/system：smoke/performance/regression）、生产测试（configuration/stress）、rollouts entangle tests、canary 为结构化用户验收及 0.1%→100% 放量、break-glass、production probes。仅归纳链接。
- [Kalibera & Jones, Quantifying Performance Changes with Effect Size Confidence Intervals, arXiv:2007.10899](https://arxiv.org/abs/2007.10899)：本批全文核读——对统计显著性的批评与效应量区间（§1–§2）、重复层级与既有推荐（§2.3）、随机效应模型与最优重复公式（§7.4，Eq.13–14）、bootstrap 置信区间（§7.2.1/§7.3.1）、warm-up 成本处理。
- [MLPerf Storage v2.0 规则](https://github.com/mlcommons/storage)（既有登记）：计次取平均、缓存与 `drop_caches` 条款、强制 fsync。
- [nccl-tests 固定快照 b4d5beeb](https://github.com/NVIDIA/nccl-tests/tree/b4d5beebca8a76cf01335f724d154b9b9d394d96)（既有登记）：`-w` 预热、`-c` 校验不进计时。
- [HCCL 性能测试工具指南 CANN 9.1.X](https://www.hiascend.com/document/detail/zh/CANNCommunityEdition/910/devaids/hccltool/HCCLpertest_16_0001.html)（既有登记）与 [SuperBench ATC 2024](https://www.usenix.org/conference/atc24/presentation/xiong)（既有登记）：判据前置与统计口径的既有样板。
- [Google SRE Book, Ch.12 Effective Troubleshooting](https://sre.google/sre-book/effective-troubleshooting/)（既有登记）：主动测试的副作用与证据保全。
- 逐条主张与读取范围见[第三十批 T08-05 来源记录](../../docs/research/batch-30-t08-05-sources.md)。
- 待确认：各方案执行时的环境档案；注入工具链在昇腾侧的可控注入面（当前仅 FaultDiag 诊断侧登记，注入能力未登记）。
