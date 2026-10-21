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
  - src.nvidia.dcgm-diag-user-guide-latest-2026-10-08
updated_at: "2026-10-21"
summary: 给出验收/基准/压力/故障注入四类测试的选择与覆盖矩阵（对象、故障模型、所问问题、检测覆盖、按层级分列的资源与风险、恢复），统一重复/随机化/warmup/样本量与置信区间/多重比较等统计纪律与预注册判据（均值规划与尾分位估计分列），并按环境档案、脚本/输入、预先判据、执行/采集/恢复、结果复核五类汇总本库七份实验方案的准备状态——真实环境执行仍为 0/7。
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
  notes: "本批核读 SRE Book 第 17 章 Testing for Reliability 全文（CC BY-NC-ND 4.0，仅归纳）、Kalibera & Jones arXiv:2007.10899v1 全文（CC BY 4.0；重复层级、均值效应量置信区间、warm-up 成本与最优重复公式 Eq.13–14、bootstrap CI 章节；复核轮核正许可与提交日期）、MLPerf Storage v2.0 固定 commit 规则（计次/缓存条款及其正文-示例冲突照录）、nccl-tests 固定快照计时/校验实现与 HCCL 9.1.X 性能测试指南（既有登记口径）。本文是方法框架，没有任何本地执行；七份方案的真实执行状态以 plans/validation-backlog.yaml 为准。"
---

# 统一测试选择、压力/注入与统计方法

同一条“测试通过”结论在验收、基准、压力与注入四类活动中含义不同。本文回答三个问题：给定一个可靠性疑问，**选哪类测试、怎么声明它的覆盖**；**结果怎么统计才可比较**；**注入和压力怎么设计才既有效又可恢复**。测试对象的具体机制（设备诊断、通信基线、精度比对）归各域正文；本文提供统一的选择与判读框架。SRE 对测试的经典定位可作为总纲：测试量化对可靠性的信心，**通过的测试不证明可靠，失败的测试一般证明不可靠**（[Testing for Reliability](https://sre.google/sre-book/testing-reliability/)）。

`generic` 表示框架跨平台通用；各平台工具与字段按已登记版本在对应正文查询，环境未知时不假设任何测试可运行。

## 一、选择矩阵：先声明对象与所问问题

选测试前先填表。填不出来的格子就是该测试尚不能声称的覆盖——不是事后补的理由。**资源成本与风险不随类别统一**：同一类“验收”里，只读健康查询与整机主动诊断（如 DCGM diagnostic 的 stress/power/memtest 级别，其 Run Levels and Tests 节区分长短级别，[登记来源](https://docs.nvidia.com/datacenter/dcgm/latest/user-guide/dcgm-diagnostics.html)）的耗时与影响差别巨大（[节点验收](../01-hardware/node-acceptance-triage.md)按层级登记了影响分级）；通信/存储基准要独占计算、内存、网络或存储资源（nccl-tests 方案要求隔离实际计算/网络资源）。每格按“所选层级＋具体工具/负载＋持续时间＋波及共享域”填写，预算未知保持 unknown。

| 维度 | 验收（acceptance） | 基准（benchmark） | 压力（stress） | 注入（injection） |
|---|---|---|---|---|
| 典型对象 | 新到/修复后的节点、环境变更后的栈 | 已验收环境的性能特征（带宽、吞吐、时延） | 系统与组件的极限与降级方式 | 显式构造的故障模型 |
| 所问问题 | “这台设备/这套栈现在能否交付约定的服务” | “在此负载定义下性能是多少，与基线差多少” | “到哪里会坏、坏成什么样、是否优雅降级” | “这个故障被观测到吗、检测机制响应正确吗、传播与处置假设成立吗” |
| 对应故障模型 | 按验收层级覆盖（部件/驱动/通信/端到端，见[节点验收](../01-hardware/node-acceptance-triage.md)） | 无故障前提下的性能口径 | 资源耗尽类（SRE 章节的 stress test 即“数据库写到多满开始失败”一类极限问题） | 按目标故障模型逐项声明（位置/强度/时序，见第三节） |
| 检测覆盖的声明方式 | 通过＝覆盖到的检查项当次通过；**不得表述为“无故障”** | 结果只在固定口径内可比（消息、rank、单位，见[带宽基线](../03-communication/bandwidth-baselines.md)） | 覆盖到实际触发的极限路径；未触发的退化模式不声称 | 覆盖＝被注入的故障模型×观测点；检出≠发生率 |
| 资源成本（按层级分列） | 只读查询层：低成本；主动诊断/整机验收层：按 run level 与负载从分钟到小时级（DCGM diagnostic 的 Run Levels and Tests 节，[登记来源](https://docs.nvidia.com/datacenter/dcgm/latest/user-guide/dcgm-diagnostics.html)），须排空生产负载 | 占计算/内存/网络或存储资源，须声明独占范围与时长 | 有破坏风险，需预算与隔离环境 | 需可牺牲环境或预算的合成注入 |
| 风险与恢复 | 只读层低；诊断/整机验收层的影响与恢复按[节点验收](../01-hardware/node-acceptance-triage.md)分级登记（整机基准属高影响），结束后核对资源/配置状态 | 占用计算/内存/网络或存储并须独占（范围与时长须声明），需防缓存/后台负载污染；结束时核对资源与配置状态——影响随占用范围升级，不预设"低" | 高：可能压垮共享依赖，见第三节停止条件 | 高：可能触发未预期的传播/处置，见第三节字段 |
| 与真实健康的关系 | 必要不充分 | 性能≠正确性 | 极限≠日常 | **合成注入检出不构成真实故障证据，只评估检测/处置方法**（见[静默错误](silent-errors-and-integrity.md)注入地位一节） |

SRE 章节对生产环境测试的两点提醒同样适用于集群：**rollout 会让生产环境“不属于任何一个版本”**（测试可能拿新配置打旧二进制，结论只在该组合内成立）；**canary 不是测试而是“结构化的用户验收”**——它把新版本暴露给真实流量，不保证捕获新引入的故障，其指数放量节奏（0.1%→1%→10%→100%）是风险控制而非覆盖声明（[同章](https://sre.google/sre-book/testing-reliability/)）。

**“测试通过”的四条边界**（汇总，避免重复犯错）：

1. 通过的测试不证明可靠（SRE）；
2. 通过的验收不排除未覆盖故障模式（本库[节点验收](../01-hardware/node-acceptance-triage.md)同口径）；
3. 主动检测（如 DCGM diagnostic、SDC 扫描）通过不等于无 SDC（覆盖取决于输入与触发条件，见[静默错误](silent-errors-and-integrity.md)）；
4. 注入环境里的检出/恢复成功不证明生产同型故障必然同样表现（环境差异与观测者效应）。

## 二、统计纪律：比较之前先固定口径

以下纪律适用于所有四类活动中的量化结论。方法依据为 Kalibera & Jones 对性能量化的系统方法（[arXiv:2007.10899v1](https://arxiv.org/abs/2007.10899)）：

1. **重复与层级**：明确重复发生在哪一层（同一进程内多次迭代 / 多次执行 / 多次构建或多次环境实例）。各层方差不同，混层平均会低估不确定性；论文给出按各层方差与成本分配最优重复次数的公式（Eq. 13–14，**优化对象是均值的置信区间精度**）；至少应记录实际采用的每层次数。
2. **warm-up 与稳态**：预热期样本应从汇总中剔除并单独记录剔除规则（论文把 warm-up 计为执行成本 `c1`，稳态样本数随预热成本升高而升高）。集群语境的对应物：首个 epoch/首批请求、缓存冷热（MLPerf Storage 对 checkpoint 负载按固定规则规定缓存处理与强制 fsync——把缓存与校验状态写进规则的样板；注意其固定规则的正文与示例在缓存比较条件上不一致——正文按每客户端 checkpoint 大小 `S` 与客户端内存 `M` 比较 `S<3M`、示例却按 `3S` 与 `M` 比较——该冲突本库照录待上游澄清，不自行择一，见[固定规则](https://github.com/mlcommons/storage/blob/7e71ca162d8f9e7ae4b5b698d7d79b0883817f25/Submission_guidelines.md) L167–180；nccl-tests 用 `-w` 预热且 `-c` 校验不进计时）。
3. **随机化与次序效应**：多配置实验应随机化执行顺序或显式交换次序并重复，否则把漂移（温度、后台任务、缓存）误记为配置差异；Kalibera & Jones §2.1 列举了虚拟-物理页映射等需要随机化处理的随机效应因素。
4. **单因素与对照**：一次只变一个声明过的因素，其余固定并记录；需要多因素时用全因子/部分因子设计并写明哪些交互不检验。无对照组的“改前改后”在长周期集群上不可解释（负载自身在变）。
5. **样本量与置信区间（均值与尾分位分列）**：
   - **均值类对象**（平均吞吐、平均操作耗时）：报告效应量（如前后均值之比）及其置信区间；论文对执行时间比给出 bootstrap 区间方法（§7.3.1），其规划公式（§7.4）按初始实验方差反推**均值区间**所需重复数——公式只在其模型假设（各层独立同分布的随机效应结构）下使用。
   - **尾分位类对象**（p99/p999 时延）：Kalibera & Jones 的区间与规划方法针对均值，**不构成 p99 的样本量或区间算法**；尾分位估计须另行声明估计对象、抽样/重复单位、层内与层间依赖（一般请求流与同一进程内的迭代不能自动视为独立样本）与失败请求口径，并选用支持该对象的区间方法（本库尚未登记该方法来源，保持待定）。**本库不给任何通用的“p99 至少 N 个样本”硬阈值**。
   - 正态性等分布假设在多数量化方法中常被省略但并不自动成立（论文 §3.2 的批评）。
6. **多重比较**：同一批数据上检验多个阈值/多个算子/多个指标时，逐个按名义水平判读会放大假阳性；预注册判据（见下）限定主判据数量，次要指标只作描述或做多重性校正后再判读。
7. **预注册判据与无结果记录**：执行前写下主判据、通过/失败阈值、停止条件与计划样本量。SuperBench 是“**离线学习判据、校准后固定、再用于后续验证**”的样板——其判据由集群 build-out 全集结果**学习得出**（无监督 CDF 相似度、单向距离、Algorithm 2 迭代剔除取中位样本，§3.4），后续验证才与该离线判据比较，且判据按周期更新（§3.1）；它证明的是“定判据的数据与被评价的数据分离、判据身份与冻结时点可追踪”，**不是**测量前预注册——预注册是本库自己的要求，不能由该论文推得。**“无差异”也是结果，按原判据记录**，不得事后改成“看起来好一些”。
8. **停止与放弃记录**：中途停止（预算用尽、环境失稳、注入触发未预期影响）时记录已跑部分与停止原因；不得把停止前样本当作完整实验判读。

一个可复用的记录骨架：`{对象与环境档案, 所问问题, 声明的故障模型/因素, 每层重复数与随机化方式, warm-up/缓存处理, 主判据与预注册阈值, 实际执行范围, 效应量与区间（注明均值/尾分位口径）, 无结果/停止记录}`。

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

以下七份方案均为**设计文档**（`verification: not_verified`），真实环境执行状态 **0/7**；执行与证据采集由 [plans/validation-backlog.yaml](../../plans/validation-backlog.yaml) 的 V 工作包按各自环境推进，**本文或任何正文完成都不改变该状态**。准备状态分四层记录：**设计**（方案中已有文字设计）→ **冻结**（具体值/脚本/输入已按环境定死）→ **执行**（已运行）→ **复核**（结果已按 V00 的实例与证据复核要求重读）。当前七份方案普遍处于“设计”层：环境档案、脚本/输入制品与具体阈值均属执行前冻结项。

| 方案 | 环境档案 | 脚本/输入 | 预先判据 | 执行/采集/恢复 | 结果复核 |
|---|---|---|---|---|---|
| [NCCL 超时实验](../03-communication/nccl-timeout-experiment.md) | 缺（待建） | 设计有命令与输入要求；脚本制品未冻结 | 判读规则已设计；超时窗口等具体值待冻结 | 设计有（隔离环境、逐 rank 采集、清理）；实例未准备 | 未开始；复核须按 V00 准备实例（原始记录＋判读方法＋偏差/停止记录＋复核责任）另立 |
| [HCCL 超时实验](../03-communication/hccl-timeout-experiment.md) | 缺 | 同上 | 同上（HCCL 口径） | 同上 | 未开始 |
| [昇腾版本失配实验](../02-software-stack/ascend-version-mismatch-experiment.md) | 缺 | 核对清单已设计；制品未冻结 | 预期错误类别已列 | 设计有 | 未开始 |
| [昇腾设备可见性实验](../05-cluster-platform/ascend-device-visibility-experiment.md) | 缺 | 四层检查点已设计 | 已设计 | 设计有 | 未开始 |
| [GPU→NPU 精度差异实验](../06-training/gpu-npu-precision-difference-experiment.md) | 缺 | 采集流程已设计 | **已定义必须预注册的字段与判读规则**（dtype/开关/容差/指标的字段框架）；具体容差与配置值为执行前冻结项，当前未定 | 设计有 | 未开始 |
| [checkpoint 状态恢复实验](../06-training/checkpoint-state-recovery-experiment.md) | 缺 | 恢复核对项已设计 | 已设计 | 设计有 | 未开始 |
| [推理长尾实验](../07-inference/ascend-inference-tail-latency-experiment.md) | 缺 | 负载档位已设计 | 尾分位判读口径已设计 | 设计有 | 未开始 |

三行共同结论：**环境档案全部为空、脚本/输入制品未冻结、结果复核未开始**——这是执行前的共同缺口；各方案补齐环境档案与冻结值之前不得声称可运行。结果复核是独立于编辑审阅的环节：须能定位原始记录、判读方法、偏差/停止记录与复核责任安排（按 [V00 准备实例要求](../../plans/validation-backlog.yaml)），不以本批编辑初审代替。

## 五、与相邻正文的分工

- 故障模型与传播路径：[故障模型与传播](fault-models-and-propagation.md)（注入用例的“位置/故障域”两字段从其 FMEA 行取值）；
- 处置与恢复的选择：[隔离、重试预算、降级与恢复选择](mitigation-and-recovery-principles.md)（压力/注入的“恢复条件”字段从其恢复选择表取值；其“有限故障对照设计”即本文注入字段的一个已登记应用）；
- SDC 检测方法的覆盖与假阴性：[静默错误](silent-errors-and-integrity.md)；
- 指标口径与统计记账（事件损失、可用性与有效产出的合成计算例）：[可靠性指标与恢复损失](reliability-metrics-and-recovery-loss.md)；
- 节点验收层级与设备侧工具：[节点验收](../01-hardware/node-acceptance-triage.md)、[设备健康证据](../01-hardware/health-evidence.md)；
- 通信基线口径：[带宽基线](../03-communication/bandwidth-baselines.md)。

## 六、适用边界

- 本文是**方法框架与登记状态**，不是执行结果；不含任何本地测量、注入或压力数据。
- 统计方法引 Kalibera & Jones 与 SRE 章节的原文范围；论文示例为软件系统性能量化，迁移到 GPU/NPU 集群时方差结构与成本模型需按第二节的骨架重新估计，公式不可照搬数值；尾分位区间方法来源未登记，保持待定。
- 不给通用最小样本量、通用“正常波动范围”或跨平台阈值；这些只能由固定环境档案下的初始实验估计并随环境变更复核。
- MLPerf/nccl-tests/HCCL 的规则条款是**各家基准的定义**，引用其条款不等于本库执行了这些基准；MLPerf 缓存条款的正文-示例冲突照录待上游澄清。

## 来源核对范围

- [Google SRE Book, Ch.17 Testing for Reliability](https://sre.google/sre-book/testing-reliability/)（CC BY-NC-ND 4.0）：本批全文核读——测试与 MTTR/MTBF 关系、传统测试（unit/integration/system：smoke/performance/regression）、生产测试（configuration/stress）、rollouts entangle tests、canary 为结构化用户验收及 0.1%→100% 放量、break-glass、production probes。仅归纳链接。
- [Kalibera & Jones, Quantifying Performance Changes with Effect Size Confidence Intervals, arXiv:2007.10899v1](https://arxiv.org/abs/2007.10899)（CC BY 4.0）：本批全文核读——对统计显著性的批评与效应量区间（§1–§2）、重复层级与既有推荐（§2.3）、随机效应模型与最优重复公式（§7.4，Eq.13–14，**均值区间**的规划）、bootstrap 置信区间（§7.2.1/§7.3.1）、正态性假设批评（§3.2）。
- [MLPerf Storage v2.0 规则（固定 commit 7e71ca1）](https://github.com/mlcommons/storage/blob/7e71ca162d8f9e7ae4b5b698d7d79b0883817f25/Submission_guidelines.md)（既有登记）：计次取平均、缓存条件（L167–180，正文与示例冲突照录）、强制 fsync。
- [nccl-tests 固定快照 b4d5beeb](https://github.com/NVIDIA/nccl-tests/tree/b4d5beebca8a76cf01335f724d154b9b9d394d96)（既有登记）：`-w` 预热、`-c` 校验不进计时。
- [HCCL 性能测试工具指南 CANN 9.1.X](https://www.hiascend.com/document/detail/zh/CANNCommunityEdition/910/devaids/hccltool/HCCLpertest_16_0001.html)（既有登记）与 [SuperBench ATC 2024](https://www.usenix.org/conference/atc24/presentation/xiong)（既有登记）：判据学习/校准与统计口径的既有样板（§3.1/§3.4/Algorithm 2 复核轮补核）。
- [Google SRE Book, Ch.12 Effective Troubleshooting](https://sre.google/sre-book/effective-troubleshooting/)（既有登记）：主动测试的副作用与证据保全。
- [DCGM Diagnostics User Guide（Run Levels and Tests）](https://docs.nvidia.com/datacenter/dcgm/latest/user-guide/dcgm-diagnostics.html)（既有登记 src.nvidia.dcgm-diag-user-guide-latest-2026-10-08）：主动诊断分级与负载前提的选择矩阵依据。
- 逐条主张与读取范围见[第三十批 T08-05 来源记录](../../docs/research/batch-30-t08-05-sources.md)。
- 待确认：各方案执行时的环境档案与冻结值；注入工具链在昇腾侧的可控注入面（当前仅 FaultDiag 诊断侧登记，注入能力未登记）；尾分位区间方法的原始统计来源。
