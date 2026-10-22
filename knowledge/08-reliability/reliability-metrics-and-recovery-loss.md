---
id: reliability.reliability-metrics-and-recovery-loss
type: reference
domain: reliability
status: draft
title: 可靠性统计、有效产出与恢复损失
platforms: [generic]
source_refs:
  - src.arxiv.llama3-infrastructure
  - src.arxiv.mpg-tpu-goodput-2025
  - src.nist.empo-handbook-reliability-sections
  - src.nist.csrc-glossary-rto
  - src.google.sre-implementing-slos
  - src.google.sre-monitoring-distributed-systems
  - src.usenix.superbench-atc24
  - src.ocp.sdc-in-ai-2025
  - src.pytorch.elastic-2.6
  - src.vllm.inference-v0-14
updated_at: "2026-10-22"
summary: 定义可靠性统计的观察对象、窗口、分母、事件起止、删失、重叠与聚合口径；按可修复/不可修复对象与模型假设给出 MTBF/MTTR 类指标的使用边界（描述性均值与更新过程推断分列）；用 Llama 3 有效训练时间与 Google MPG（调度/运行时/程序三层 goodput）区分有效产出、被丢弃的重算与恢复开销；提供事件表/尝试表/窗口表 schema 与合成计算例（同一症状在四维目标下结论不同、各段口径显式声明）；本地无任何历史数值。
related_ids:
  - reliability.dimensions-and-failure-domains
  - reliability.mitigation-and-recovery-principles
  - reliability.postmortem-and-knowledge-update
  - training.checkpoint-state-consistency
  - training.elastic-training-and-membership
  - inference.latency-metrics
verification:
  status: source_checked
  evidence_refs:
    - src.arxiv.llama3-infrastructure
    - src.arxiv.mpg-tpu-goodput-2025
    - src.nist.empo-handbook-reliability-sections
    - src.google.sre-implementing-slos
    - src.usenix.superbench-atc24
  notes: "本批核读：Llama 3 论文（arXiv:2407.21783v3）§3.3.1 基础设施与 §3.3.4 可靠性段（有效训练时间定义、54 天中断统计与 Table 5、checkpoint 规模与 Tectonic 存储口径、NCCL flight recorder；Table 5 计数列与百分比列的来源冲突经逐行复算照录）；Google MPG v1（arXiv:2502.06982v1 固定入口，CC BY 4.0；v2 已存在未读）§4（SG/RG/PG 定义与公式）与 §5；NIST e-Handbook 可靠性章节（复核轮登记）；SRE 两章为既有登记口径。本文不含本地测量；合成计算例明确标注，不填任何本地历史数值。 2026-10-22 IQ-04 重算固定 3h 故障时刻、4h→2h 与 8h→4h 两组合成对照，分别为 3h→1h 与 3h→3h；这不是 checkpoint 实验。"
---

# 可靠性统计、有效产出与恢复损失

“这个集群可靠性怎么样”要拆成可回答的统计问题：**对什么对象、在什么窗口、以什么为分母、把哪些事件算进去、怎么处理没观测到的部分**。本文给出训练与推理共用的记账框架，并把“有效产出”与“吞吐”分开——训练吞吐可以一切正常，而有效产出因为一段未保存的尝试被丢弃而损失三小时。四维目标（可用性/正确性/性能稳定性/可恢复性）的定义见[可靠性维度与故障域](dimensions-and-failure-domains.md)；本文是它的计量层。

## 一、先固定统计框架：对象、窗口、分母、事件

| 要素 | 必须写明的口径 | 常见错误 |
|---|---|---|
| 观察对象 | fleet / 集群 / 节点 / 作业 / 训练 run / 服务实例 / 请求，及其身份键 | 节点数在窗口内变化（扩缩容、维修）而分母固定 |
| 窗口 | 起止时刻与时区/时钟源；滑动窗口或日历窗口；**观察截止点**（删失记账用，见下） | 用“最近 30 天”比较两个不同负载强度的时期 |
| 分母 | 台·时（fleet）、卡·时（芯片）、请求总数、step 总数、日历时间 | 可用性百分比与 MTBF 用了不同的事件集合 |
| 故障事件起止 | **按可观测证据定义**：开始＝首个异常观测或首个受影响请求的时刻；结束＝服务恢复判据达成时刻（**未恢复的事件该字段为空**，另记观察截止与删失状态）。根因发生时刻单独记录（可能早于首个观测，见[相关故障案例](correlated-failure-source-case.md)的“事件时刻 vs 发现时刻”） | 把根因时刻当事件开始（无法观测就不可统计）；把“进程退出”当结束（服务未恢复） |
| 恢复事件起止 | 等待/排队、处置动作、状态加载、预热各分段分别记时 | 把“重启完成”当恢复完成（预热未完成时吞吐仍异常） |
| 删失 | 窗口结束时仍在故障/恢复中的事件：右删失——真实终点未知，只知不早于观察截止；按事件计数保留、时长按窗口截断并声明，或用删失感知方法（未登记来源，待定） | 直接丢弃未完结事件（低估）；当作已完结（时长低估） |
| 缺失 | 采集覆盖（哪些对象/时段无数据、原因）进入统计附注 | 无数据时段按“无故障”处理 |
| 重叠故障 | 同一窗口多起事件：**用事件关联键＋影响区间并集**去重——按主事件计数与按并集时长两种口径都报告，并标注同因/独立判定依据（[传播≠多起](fault-models-and-propagation.md)） | 把一次故障的传播记成 N 起独立故障 |
| 聚合 | 日/周/月聚合方式；百分位与均值的样本来源 | 用日均值拼出周 p99 |

## 二、MTBF / MTTR / MTBI 的使用边界

先按对象区分，再谈模型（依据 [NIST e-Handbook 可靠性章节](https://www.itl.nist.gov/div898/handbook/apr/section1/apr121.htm)）：

- **对象区分**：**MTBF 用于可修复系统**（两次失效之间的运行时间），**MTTF 用于不可修复对象**（寿命）——区别在对象是否修复后继续服役，不是“是否计入修复期”这一个记账细节。本文口径：每个 MTB* 指标写明对象、时间轴（运行时间还是日历时间）、事件集合与停机处理；MTTR 的样本是**恢复时长**（各事件的恢复分段之和），与故障间隔是两类样本。
- **本文采用的计算式（对同一事件表可唯一重算）**：MTBF＝窗口内对象运行时间合计 ÷ 故障事件数（NIST [apr451](https://www.itl.nist.gov/div898/handbook/apr/section4/apr451.htm) 的 HPP 点估计量；另一常见口径＝完整间隔的样本均值，截断窗口下两者可不同——报告时声明选用哪者）；MTBI 同式，但分母事件集合须声明是否含计划内中断（本文口径：不含，另列）；MTTR＝各事件恢复时长（分段之和）的样本均值；零事件窗口报告“0 事件”，均值不定义；未完结事件不计入间隔、按删失字段另记（生存类方法未登记，待定）。
- **描述性均值与模型推断分列**：对事件表总能算出样本均值——这只回答“这段窗口平均多久一次”。要外推（置信区间、趋势检验）需要过程模型：**一般更新过程**只要求失效间隔独立同分布（可为非指数）；**齐次泊松过程（HPP）再附加事件率恒定（等价于指数间隔）**（[HPP/指数模型](https://www.itl.nist.gov/div898/handbook/apr/section4/apr451.htm)；apr171 亦为 HPP 页，本库未登记一般更新过程的完整方法来源——待定）。三种假设分别需要证据：独立性（间隔之间）、同分布（同一失效机制）、恒定率（仅 HPP 需要）。**非常数 hazard 不等于非独立同分布**——同一寿命分布内部的年龄相关 hazard（如浴盆形曲线，[apr124 可修复/不可修复与 ROCOF](https://www.itl.nist.gov/div898/handbook/apr/section1/apr124.htm)）不改变跨样本 i.i.d.；破坏外推的是**跨样本的分布变化**——按系统日历时间/批次维度度量的事件率变化（ROCOF 意义）与共同原因事件、负载相关故障（如高温季，即不同时段抽取自不同分布）。Llama 3 记录 GPU 相关问题占其意外中断的 58.7%（论文报告值，见下节），若硬件族占比随采购批次变化，历史均值直接外推不成立。
- **仿真数字不是观测数字**：SuperBench 的 MTBI 提升 22.61×（262.05/11.59，其 Table 4）明确是仿真结果且假设全集可发现全部 incident，不是生产 A/B（[ATC 2024 PDF §5.2，印刷页 845](https://www.usenix.org/system/files/atc24-xiong.pdf)）。报告任何 MTB* 都应注明来自观测、仿真还是外推。
- **均值的下一步是分布**：恢复时间通常重尾；报告 MTTR 时至少附带事件数与最大值。

## 三、训练侧：有效产出、重算与恢复开销

### 两个公开原始口径

**Llama 3（Meta，16K H100，405B 预训练）**：论文明确定义“**有效训练时间（effective training time）＝用于有用训练的时间 / 经过的总时间**”，并在支持自动集群维护（每天至少引起一次训练中断）的同时达到 **高于 90%**。54 天快照期共 466 次作业中断：47 次计划内（固件升级等自动维护、配置/数据集更新），419 次意外（Table 5 的 18 行绝对计数合计恰为 419，可复核）；约 78% 归因于“已确认或疑似的硬件问题”（confirmed or suspected，口径含未证实归因）。**Table 5 的计数列与百分比列存在来源自身未解冲突**（本库逐行复算：百分比列合计 94.9%；GPU 六行计数合计 268 即 64.0%，而其报告百分比相加为 58.7%；Faulty GPU 行 148 次＝35.3% 而表写 30.1%；HTML 与 PDF 同此）——下文只引用**论文报告的百分比**并统一标注“计数未能共同核实”：GPU 类合计 58.7%（Faulty GPU 30.1%、HBM3 17.2%、SRAM 4.5%、系统处理器 4.1%、SDC 1.4%、热接口＋传感器 1.4%），软件缺陷 12.9%、网络 8.4%、计划外主机维护 7.6%、NIC 1.7%、NCCL watchdog 超时 1.7%（Unknown 类）；期间仅 3 次需要显著人工介入（[arXiv:2407.21783v3 §3.3.1/§3.3.4 与 Table 5](https://arxiv.org/abs/2407.21783v3)）。checkpoint 每卡 1 MB–4 GB 状态，目标是**压低 checkpoint 期间的 GPU 暂停并提高频率以减少恢复后损失的工作量**；存储侧（Tectonic，240 PB、持续 2 TB/s）需承接短时打满的突发写。诊断用 NCCL flight recorder（环形缓冲记录每次 collective 元数据与栈，watchdog/心跳超时时自动转储）。

**Google MPG（TPU fleet）**：把 fleet 效率分解为三层乘积（[arXiv:2502.06982v1 §4](https://arxiv.org/abs/2502.06982v1)）：

| 分量 | 定义（原文归纳） | 记账含义 |
|---|---|---|
| Scheduling Goodput（SG） | 应用**全部所需芯片同时可用**的时间（allocated chip-time）/ fleet 容量（chip-time） | 分布式作业要求所有卡同时在线；碎片化、等待协调都扣 SG。**资源已齐备之后的加载/编译（及被丢弃的未保存重试）属运行时层，扣 RG 不扣 SG；成功保存的重放是有效进展，不扣 RG**（与下表 RG 行及第六节口径一致） |
| Runtime Goodput（RG） | **已保存进 checkpoint 的有效 chip-time** / allocated chip-time；论文明示“最后一次 checkpoint 与失败（或抢占）之间的工作不计入 RG” | 初始化、数据加载、慢 checkpoint、编译在这里扣；**只有被丢弃的未保存尝试在这里损失**——成功保存的重放是有效进展，不扣 RG（与第六节口径一致） |
| Program Goodput（PG） | 按 HLO 图形状估的理想执行时间 / 实际执行时间 | 程序效率的度量分层；这**不构成**“PG 与故障无关”的因果保证——实际执行时间同样受故障期间表现影响，只是该指标的用途在程序效率比较 |

两个口径互补：Llama 3 给出作业级“有用训练/总时间”的一手观测与中断分类；MPG 给出可分解的记账结构（哪一层损失的芯片时间去哪了）。共同要点：**占用率（occupancy）不区分产出**——卡被分配但卡在 I/O 等待，占用率照样高（MPG 论文对传统 occupancy 的批评）。

### 记账时区分六类量

| 量 | 定义 | 与吞吐的区别 |
|---|---|---|
| 有效训练 token / 已保存 step | 进入最终模型状态（或已被有效 checkpoint 保护）的训练进展 | 吞吐量是“算得多快”，此项是“留下了多少” |
| 已提交 step（committed） | 优化器已执行、尚未被回滚声明的 step | 中断后是否算数取决于回滚边界 |
| **被丢弃的重算/回放尝试** | 失败或污染时未（有效）保存的那段工作 | **产出为零的是被丢弃的尝试**；从有效 checkpoint 成功重放并保存会推进恢复后的状态（计入有效产出，不扣 RG）——不能把“回放”一概记为零产出，须按结局分别记账 |
| 丢失数据 | 加载失败/损坏/未持久化的输入与状态 | 与重算分开记（原因与补救不同） |
| 恢复等待 / 状态加载 / 预热 | 等待处置、加载 checkpoint、重建进程组、预热到稳定吞吐的分段时间 | 每段单独计时；预热完成的判据要预先定义（如 step time 回到基线带内 N 步） |
| 健康窗口 | 满足全部四维判据、可正常承接工作的连续时段；**追平故障前进度之前的时段算不算健康窗口按声明的口径记录**（见第六节示例） | 与“进程存活”不同；见[处置选择](mitigation-and-recovery-principles.md)恢复判据 |

checkpoint 频率的权衡由此可量化：提高频率压低单次丢失的未保存工作（Llama 3 的目标），但提高 I/O 与同步开销、压低运行 goodput（OCP 白皮书 §5.3.1 的代价警告）。两条曲线的交点没有通用值，按存储带宽、checkpoint 大小、故障率与环境实测。

## 四、推理侧：不能只统计成功请求

推理服务的可靠性记账必须包含失败侧，且成功/失败/取消/超时**分列**：

- 固定 vLLM 的请求终点分 `STOP` / `LENGTH` / `ABORT`（源码描述为客户端取消）/ `ERROR`（源码描述为可重试的请求级内部错误）；Prometheus `vllm:request_success` 虽名为 success，实际**按 finish reason 建标签**对全部完成请求增量——counter 求和不能称作“成功请求数”（固定 v0.14.0 源码口径，详见[推理时延指标](../07-inference/latency-metrics.md)）。该枚举覆盖的是引擎内完成路径；“每种取消/断连/上游超时都进入同一服务端统计”未经证明，跨层口径另行核对。
- **goodput 必须绑定已声明的 SLO 集合**：同一请求须满足全部已提供阈值才计入；无 SLO 集合的吞吐不能改名 goodput（同上）。
- **幸存者偏差**：延迟分位只含成功请求时，失败率上升反而可能“改善” p99——每张延迟/吞吐表并列错误、取消、超时计数，并说明超时由谁判定（客户端/代理/服务端）。
- **质量与降级成本单独记账**：降级模式（较小模型、关闭某些功能、拒绝长上下文）期间的服务量、质量指标与恢复过渡期单独成行；把降级期间的请求并入正常统计会同时污染可用性与质量两个维度。
- **训练侧迁移 SLI 时保持“好事件/总事件”结构**（SRE [Implementing SLOs](https://sre.google/workbook/implementing-slos/)）。一个完整的**合成**示例（单位/阈值/消耗规则齐备）：SLI＝窗口内有效保留训练小时 ÷ 考核总小时（同单位相消；考核含计划维护与失败尝试）；SLO＝≥95%；错误预算＝5%×168 h＝8.4 h/周；预算消耗按坏时间计＝（168−161.0）＝7.0 h → 7.0/8.4＝**83.33%**（不得从舍入后的 4.2% 再算）。**统一规则**：坏时间＝一切非有效保留时间（维护、检测等待、恢复、丢弃尝试都计入，不从分母剔除）——因此无故障但含 2 h 维护的周消耗＝2/8.4＝23.8%，不存在“无故障周消耗 0%”的例外；条件性质量 SLI（合格已保存 step/已保存 step 总数）在已保存 step 为 0 的窗口报告“**无样本**”（不定义为 0% 或 100%），另按上一 SLI 记产出损失。若只考核已保存 step 的正确性，这是**条件性质量 SLI**（分子＝合格已保存 step，分母＝已保存 step 总数），产出损失另按上一 SLI 记——不能用“有效时间/有效时间”自除，也不能把无产出窗口静默排除后报 100%。

## 五、记账 schema：三张表

**表 1 事件表**（每起故障/中断一行；`observed_end` 为空＝未恢复，删失字段记录观察截止）：

```yaml
- event_id: <稳定ID>
  object: {kind: node|job|service|run|rank_group, id: <身份键>, version_keys: {硬件/驱动/框架/镜像版本}}
  window_tag: <所属统计窗口>
  observed_start: <时间戳+时钟源>      # 首个异常观测
  observed_end: <时间戳+时钟源|null>   # 服务恢复判据达成；null＝尚未恢复
  observation_cutoff: <时间戳|null>    # 删失记账的窗口观察截止
  censorship: none|right_censored|window_truncated
  cause_time: <时间戳|null|unknown>
  category: <故障分类，见 FMEA 行>
  related_event_ids: [{id: <事件ID>, relation: same_cause|independent_overlap}]  # same_cause＝共同原因组（组内最早 observed_start 为主事件，主事件计数按组归一）；independent_overlap＝仅时间重叠的独立事件（只参与影响区间并集，不归一、不并成一起事件）
  attribution: confirmed|suspected|unknown
  impact: {affected_objects: n, affected_interval: <起止区间>, requests_or_steps: n, degraded_dimensions: [可用性|正确性|性能|可恢复性]}
  handling: {detection_source: <>, action: <隔离|重试|回滚|重启|人工介入|null>, by_automation: bool}
  recovery: {wait_s: x, load_s: x, warmup_s: x, catchup_s: x, discarded_attempt_s: x, lost_data: <描述|null>}
  progress_boundary: <恢复所依据的 checkpoint/进度身份>   # 去重与回放归属
  evidence_refs: [<来源ID或本地case/experiment ID>]
```

**表 2 尝试/请求表**（训练的“尝试”或推理的“请求”各一行，支撑结果分类、SLO 与去重）：

```yaml
- attempt_id: <稳定ID>
  object_key: <run/job/service 身份键>        # 尝试归属（与事件表 object 对齐；缺它则同名 step 无法区分并行 run）
  parent_event: <关联 event_id|null>          # 归属故障事件
  parent_attempt: <前次尝试ID|null>           # 重放/重试从属于被丢弃尝试
  phase: <原始尝试|重放|重试|降级服务>
  outcome: success|failed|cancelled|timeout|discarded   # 训练侧 discarded＝未有效保存
  slo: {set_name: <名称>, checks: [{metric: <指标名与观察端>, value: <观测值+单位>, threshold: <阈值+单位>, passed: bool|null}]}   # 每阈值一条，可由观测值重验；好请求＝outcome=success 且全部 check 通过（先按结果筛选，与 serve.py 口径一致）；任一 check 缺测（passed=null）→ 该请求记"不可判"单列，不入 goodput 分子/分母；goodput＝好请求数÷窗口秒数
  quality: <质量指标值|null>; degraded_mode: <名称|null>
  progress: {start_step, end_step, saved: bool}         # 训练侧进展归属与去重键
  spans: [{start, end, kind: 等待|加载|预热|计算|降级}]
```

**表 3 窗口聚合表**：

```yaml
- window: {start, end, clock}
  denominator: {kind: chip_hours|node_hours|requests|steps|calendar_s, value: x}
  events: {count, primary_count, primary_cause_breakdown, overlap_union_hours}   # primary_count 只对 relation=same_cause 的组归一（组内最早 observed_start 为主事件；independent_overlap 事件各自计数、只进并集）；overlap_union_hours 按影响区间并集
  outcomes: {success: n, failed: n, cancelled: n, timeout: n, discarded_attempts: n}
  yield: {effective_training_s, saved_steps, goodput_slo_set: {name, good_count, total_count, indeterminate_count, window_seconds}}   # goodput＝good_count÷window_seconds（分母始终为窗口秒数，缺测请求不缩减时间分母）；total_count＝全部请求；indeterminate_count＝不可判单列；如需"可判样本中的合格比例"另名报告并注明覆盖
  coverage: {unobserved_spans, reason}
```

记录规则：时间量带单位；`recovery` 各段不必拼成单一“恢复时长”（不同终点见下节）；`attribution` 三值，不为报表把 unknown 强行归类（Llama 3 的 Unknown 类是公开样板）；由表 1–3 应能重算四类结果计数、SLO goodput、保留/丢弃进展与删失、重叠影响。

## 六、合成计算例：同一症状，四维结论不同

以下数字全部为**合成示例**（非任何本地或来源系统的真实数值），只演示量纲、口径与终点的选择。

**设定**：单作业（512 卡），观察窗口 7 天＝168.0 h。时间线（各段为窗口内的显式分段，不重叠）：

| 分段 | 时长 | 记账归属 |
|---|---|---|
| 计划内维护停机 | 2.0 h | 非故障；**本例口径：维护计入考核范围**（分母保持 168 h，维护只从分子扣除）——如另设“排除计划维护”口径，须整体换分母（166 h）重算全表，不得两种规则并用 |
| 故障尝试（崩溃前的运行） | 3.0 h **（含在运行时段内，非额外时段）** | 见下：本例设定其最后有效 checkpoint 之后的工作未保存——该 3.0 h 尝试按 discarded 记（产出为零），但**占用的是运行时段** |
| 异常检测＋等待处置 | 0.5 h | 恢复段 1（服务不可用） |
| 恢复：加载 checkpoint 1.0 h＋重建进程组/预热 0.5 h | 1.5 h | 恢复段 2（资源已齐备，属 RG 类开销，不扣 SG） |
| 从有效 checkpoint 重放并**保存成功** | 3.0 h | 重放尝试结局 success——推进并保存了状态，**不是零产出**；但与被丢弃的 3.0 h 原尝试合计消耗 6.0 h 计算资源去换取一次 3.0 h 的进展 |

**按选定口径计算**（每个量写明分子分母）：

- **有效训练时间（Llama 3 口径：有用训练/经过总时间）**：取“未被丢弃的进展时段”。运行时段＝168−2（维护）−0.5（检测等待）−1.5（恢复）＝164.0 h，其中含被丢弃的原尝试 3.0 h 与成功重放 3.0 h；扣除被丢弃尝试后＝**161.0 h（该数已包含成功重放的 3.0 h——重放保存了进展，不再另加）**；161.0/168≈**95.8%**。重复计算资源＝6.0 h（原尝试＋重放各 3.0 h）换取一次 3.0 h 的进展，冗余成本 3.0 h。
- **服务可承接工作的在线时间**：168−2−0.5−1.5＝164.0 h（重放期间服务在线）；164.0/168≈**97.6%**。若“在线”另指进程存在，须由进程创建/退出时刻的并集另行计算（本例合成设定与在线一致，无额外差异）。
- **追平口径**：从恢复完成到重放追平故障前进度高水位，又经 3.0 h——若健康窗口定义为“追平之后”，则健康窗口再减 3.0 h。**三种终点语义**：服务恢复（本例 2.0 h）、重放完成（本例 5.0 h）、追平故障前高水位（本例亦为 5.0 h——本例重放恰以原速重做等量工作，故后两者重合；其他场景如重放更快或目标更高时可不同）。三者语义不同，报告时分别命名。
- **目标与观测分列**：本例**实际恢复时长**（检测等待＋恢复）＝2.0 h；**RTO 是目标量**（业务可容许的恢复期，[NIST CSRC 定义](https://csrc.nist.gov/glossary/term/Recovery_Time_Objective)），不是单次观测之和——报“RTO=2h”是把目标与观测混同。
- **checkpoint 间隔的效果是有条件的**：损失取决于故障时刻与当时最近的有效 checkpoint，须检查缩短间隔后新增的保存点是否已成功完成。不能无条件断言“间隔减半则重算减半”。下表为独立的合成对照：共同起点 0h 已有有效 checkpoint，故障固定在 3h；忽略保存耗时、假设到期保存均成功，且重放速度与原运行相同。

  | 原间隔 → 新间隔 | 原最近有效点 → 新最近有效点 | 丢失工作对应的运行时长 |
  |---|---|---|
  | 4h → 2h | 0h → 2h | 3h → 1h |
  | 8h → 4h | 0h → 0h | 3h → 3h |

  “期望损失减半”还需要相位分布等假设：若故障相对于有效保存周期 `T` 的相位均匀分布、保存耗时忽略且保存均成功，则期望未保存工作时长为 `T/2`，周期减半才使该期望减半；这不是任一次故障的保证，也未计入更频繁保存的开销。

**四维结论不同**：

| 维度 | 该事件的记账（按上表口径） | 结论 |
|---|---|---|
| 可用性 | 在线 164.0/168≈97.6%（或有效训练 95.8%，二选一并声明） | 数字随口径差 1.8 个百分点 |
| 正确性 | 本例**设定**：错误被检出、恢复点经核对早于污染、恢复后校验通过——在这些前提下正确性无损。**同症状另一分支**：若 SDC 未检出且污染了所依据的 checkpoint，则恢复后校验失败、须回退更早恢复点——**污染与耗时是两个独立记账量**：污染分支的重放耗时可能同样存在，“检出并回滚”也不自动等于正确性恢复（恢复判据见[Checkpoint 状态一致性](../06-training/checkpoint-state-consistency.md)与[处置选择](mitigation-and-recovery-principles.md)） | 症状相同（崩溃重启），正确性结论取决于恢复点/校验证据，不由症状推出 |
| 性能稳定性 | 预热 0.5 h 内 step time 高于基线带，只影响窗口 step 时间分布尾部；均值几乎不动 | “基本无恙”的结论不适用于依赖尾分位的 SLO |
| 可恢复性 | 实际恢复 2.0 h（到服务恢复）/5.0 h（到重放完成）；被丢弃尝试 3.0 h；重复计算资源 3.0 h（原尝试）＋3.0 h（重放）换取 3.0 h 进展 | 恢复维度给出可优化杠杆（checkpoint 频率、恢复流水线），且能把“重复消耗”与“净损失”分开 |

（**独立于上面单作业时间线的抽象区间集合对比**：若把 32 起完整事件（丢弃尝试 3.0 h＋不可承接 2.0 h＋追平 3.0 h）串行嵌入同一作业至少需 32×8＋2＝258 h＞168 h，故本子例不是上例的可实现延伸，仅演示重叠口径的算术）：设 512 卡作业 fleet 的 32 张卡各有一起同类事件。**先声明区间种类**（按作业视角分三种，物理硬件“缺失”时段本合成例未定义——需现场硬件级计时，此处不假设）：**作业不可承接区间**＝检测等待＋恢复＝每起 2.0 h（资源在位但作业不能正常工作）；**追平区间**＝重放至追平＝每起 3.0 h（资源在位、作业运行但只补进度）；两者合计**有效进展中断区间**每起 5.0 h；被丢弃尝试发生于崩溃前（资源在位、产出废弃），单独按 3.0 h×32 记冗余成本。**作业级损失按“有效进展中断区间”的并集计算（前提：任一所需卡缺席即整作业停摆）**：互不重叠时并集＝32×5.0＝160 h，损失＝512×160＝81920 卡·时＝容量的 **95.2%**（容量 512×168＝86016 卡·时）；完全重合时并集＝5.0 h，损失＝2560 卡·时＝**3.0%**。同一批事件，重叠设定不同，损失相差 32 倍——这就是第一节要求事件关联键＋影响区间并集的原因。卡级（按有效进展中断口径）两种设定都是 160 卡·时（86016 容量的 0.186%）。加载/预热属 RG；SG 按“**任一所需资源缺席**的区间”扣减——512 卡中缺 1 卡，其余 511 卡可用时 all-allocated 时间同样中断（一张卡缺失即扣 SG，无须全体同时不可用）。

## 七、适用边界与待确认

- 本文全部数字中，Llama 3 与 MPG 的数字是**来源方在其环境的一手观察**（16K H100 54 天快照；Google 内部 TPU fleet），限各自平台、规模与归因口径；Llama 3 Table 5 计数/百分比冲突照录未裁定。第六节为合成示例。
- 本地（本库所辖任何环境）**没有**长期事件数据；建立真实统计需按第五节 schema 现场采集，且采集系统部署不在本文范围。
- 分布检验方法（更新过程/HPP 检验、删失感知估计）未登记可执行的原始方法来源，本文只给使用边界与 NIST 定义；需要执行检验时另行取证。
- 推理指标的字段级口径以[推理时延指标](../07-inference/latency-metrics.md)为准。
- 尾分位与效应量区间的统计方法见[统一测试方法](test-design-and-coverage.md)第二节（均值与尾分位分列）。

## 来源核对范围

- [The Llama 3 Herd of Models, arXiv:2407.21783v3](https://arxiv.org/abs/2407.21783v3)：本批核读 §3.3.1（Training Infrastructure，印刷页 9）与 §3.3.4（Reliability and Operational Challenges，印刷页 13，Table 5）——有效训练时间定义与 >90%、466/47/419（计数合计复核）、约 78% confirmed-or-suspected、报告百分比（计数冲突照录：百分比合计 94.9%、GPU 六行计数 268=64.0% vs 报告 58.7%、148=35.3% vs 30.1%，HTML/PDF 同）、3 次人工介入、checkpoint 每卡 1 MB–4 GB 与 Tectonic 240 PB/2 TB/s（峰值 7 TB/s）、NCCL flight recorder。
- [ML Fleet Efficiency / ML Productivity Goodput, arXiv:2502.06982v1](https://arxiv.org/abs/2502.06982v1)（固定 v1 入口，CC BY 4.0；v2 2025-04-20 已存在未读）：核读 §1–§5——SG/RG/PG 定义（§4.3，含“最后 checkpoint 到失败间工作不计入 RG”）、occupancy 批评（§4.1）、按分量定位优化（§5、Table 2）。示例 fleet 数值未引用。
- [NIST/SEMATECH e-Handbook 可靠性章节](https://www.itl.nist.gov/div898/handbook/apr/section1/apr121.htm)（复核轮登记：apr121 可修复/不可修复、apr451 HPP/指数、apr162 Weibull）与 [NIST CSRC RTO 术语](https://csrc.nist.gov/glossary/term/Recovery_Time_Objective)：指标对象区分、模型假设与目标/观测区分的定义依据。
- [SRE Workbook: Implementing SLOs](https://sre.google/workbook/implementing-slos/)（既有登记）：好事件/总事件 SLI 结构与错误预算口径。
- [SRE Book: Monitoring Distributed Systems](https://sre.google/sre-book/monitoring-distributed-systems/)（既有登记）：症状/观测区分与成功/失败分别观测。
- [SuperBench, USENIX ATC 2024](https://www.usenix.org/system/files/atc24-xiong.pdf)（既有登记）：MTBI 22.61× 为仿真（ATC PDF §5.2，印刷页 845；Table 4 复算 262.05/11.59）；此前批次的 arXiv 版读取记录保留原文不追改。
- [OCP SDC in AI 2025](https://www.opencompute.org/documents/sdc-in-ai-ocp-whitepaper-final-pdf)（本批补读 §5.3.1）：频繁 checkpoint 的 goodput 代价与编排开销。
- [PyTorch elastic 2.6 文档](https://docs.pytorch.org/docs/2.6/elastic/run.html)（既有登记）、[vLLM v0.14.0](https://github.com/vllm-project/vllm/tree/b17039bccc17b94a2ea107272ad7bc93508708df)（既有登记，经[推理时延指标](../07-inference/latency-metrics.md)转引）：重启/终点语义的版本化口径。
- 逐条主张与读取范围见[第三十批 T08-06 来源记录](../../docs/research/batch-30-t08-06-sources.md)。
- 待确认：本库辖内环境的长期事件采集启动条件；分布检验与删失感知估计的方法来源；MPG v2 变更（未读）；Llama 3 Table 5 计数/百分比冲突的上游澄清。
