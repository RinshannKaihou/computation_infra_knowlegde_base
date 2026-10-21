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
  - src.google.sre-implementing-slos
  - src.google.sre-monitoring-distributed-systems
  - src.usenix.superbench-atc24
  - src.ocp.sdc-in-ai-2025
  - src.pytorch.elastic-2.6
  - src.vllm.inference-v0-14
updated_at: "2026-10-21"
summary: 定义可靠性统计的观察对象、窗口、分母、事件起止、删失、重叠与聚合口径，给出 MTBF/MTTR 类指标的使用边界；用 Llama 3 有效训练时间与 Google MPG（调度/运行时/程序三层 goodput）区分有效产出、重算与恢复开销；提供事件表 schema 与合成计算例（同一症状在可用性/正确性/性能/可恢复性四维结论不同）；本地无任何历史数值。
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
    - src.google.sre-implementing-slos
    - src.usenix.superbench-atc24
  notes: "本批核读：Llama 3 论文（arXiv:2407.21783v3）§2 基础设施段（有效训练时间定义、54 天中断统计与 Table 5、checkpoint 规模与 Tectonic 存储口径、NCCL flight recorder）；Google MPG 论文（arXiv:2502.06982v1）§4（SG/RG/PG 定义与公式）与 §5（组件拆分用法）；SRE 两章为既有登记口径。本文不含本地测量；合成计算例明确标注，不填任何本地历史数值。"
---

# 可靠性统计、有效产出与恢复损失

“这个集群可靠性怎么样”要拆成可回答的统计问题：**对什么对象、在什么窗口、以什么为分母、把哪些事件算进去、怎么处理没观测到的部分**。本文给出训练与推理共用的记账框架，并把“有效产出”与“吞吐”分开——训练吞吐可以一切正常，而有效产出因为一次未检出的错误回滚损失三小时。四维目标（可用性/正确性/性能稳定性/可恢复性）的定义见[可靠性维度与故障域](dimensions-and-failure-domains.md)；本文是它的计量层。

## 一、先固定统计框架：对象、窗口、分母、事件

| 要素 | 必须写明的口径 | 常见错误 |
|---|---|---|
| 观察对象 | fleet / 集群 / 节点 / 作业 / 训练 run / 服务实例 / 请求，及其身份键 | 节点数在窗口内变化（扩缩容、维修）而分母固定 |
| 窗口 | 起止时刻与时区/时钟源；滑动窗口或日历窗口 | 用“最近 30 天”比较两个不同负载强度的时期 |
| 分母 | 台·时（fleet）、卡·时（芯片）、请求总数、step 总数、日历时间 | 可用性百分比与 MTBF 用了不同的事件集合 |
| 故障事件起止 | **按可观测证据定义**：开始＝首个异常观测或首个受影响请求的时刻；结束＝服务恢复判据达成时刻。根因发生时刻单独记录（可能早于首个观测，见[相关故障案例](correlated-failure-source-case.md)的“事件时刻 vs 发现时刻”） | 把根因时刻当事件开始（无法观测就不可统计）；把“进程退出”当结束（服务未恢复） |
| 恢复事件起止 | 等待/排队、处置动作、状态加载、预热各分段分别记时 | 把“重启完成”当恢复完成（预热未完成时吞吐仍异常） |
| 删失 | 窗口结束时仍在故障/恢复中的事件：计入事件数但生存时间右删失，或按窗口截断并声明 | 直接丢弃未完结事件（低估）；当作已完结（时长低估） |
| 缺失 | 采集覆盖（哪些对象/时段无数据、原因）进入统计附注 | 无数据时段按“无故障”处理 |
| 重叠故障 | 同一窗口多起事件：按主事件计数＋并集时长两种口径都报告，并标注同因/独立判定依据（[传播≠多起](fault-models-and-propagation.md)） | 把一次故障的传播记成 N 起独立故障 |
| 聚合 | 日/周/月聚合方式；百分位与均值的样本来源 | 用日均值拼出周 p99 |

## 二、MTBF / MTTR / MTBI 的使用边界

MTBF（平均故障间隔）、MTTR（平均恢复时间）、MTBI（平均中断间隔）只有在假设成立时可解释：

- **分母与事件集合先于指标**：MTTR 的“R”是 repair（修好）还是 restore（服务恢复）？MTBF 的“B”（between）与 MTTF 的“to”区别在于是否已计入修复期。两个名字不定义口径，口径由第一节的要素表定义。
- **更新过程假设**：这些均值默认故障间隔独立同分布。浴盆曲线（早期失效与磨损期故障率非常数）、共同原因事件（一次断电=多节点“同时故障”）、负载相关的故障（高温季）都会打破该假设；Llama 3 论文记录 GPU 相关问题占其意外中断的 58.7%（[§2.2](https://arxiv.org/abs/2407.21783)），若硬件族占比随采购批次变化，历史均值直接外推就不成立。
- **仿真数字不是观测数字**：SuperBench 的 MTBI 提升 22.61× 明确是仿真结果（假设全集可发现全部 incident），不是生产 A/B（其 ATC 2024 论文局限节，既有登记）。报告任何 MTB* 都应注明来自观测、仿真还是外推。
- **均值的下一步是分布**：恢复时间通常重尾（少数复杂事件拖长均值）；报告 MTTR 时至少附带事件数与最大值，否则一次 20 小时的事件会被均值掩盖。

## 三、训练侧：有效产出、重算与恢复开销

### 两个公开原始口径

**Llama 3（Meta，16K H100，405B 预训练）**：论文明确定义“**有效训练时间（effective training time）＝用于有用训练的时间 / 经过的总时间**”，并在支持自动集群维护（每天至少引起一次训练中断）的同时达到 **高于 90%**。54 天快照期共 466 次作业中断：47 次计划内（固件升级等自动维护、配置/数据集更新），419 次意外；约 78% 归因于已确认或疑似的硬件问题（含 SDC 与计划外单机维护），GPU 类合计 58.7%（Faulty GPU 30.1%、HBM3 17.2%、SRAM 4.5%、系统处理器 4.1%、SDC 1.4%、热接口+传感器 1.4%），其余为软件缺陷 12.9%、网络 8.4%、计划外主机维护 7.6%、NIC 1.7%、NCCL watchdog 超时 1.7%（Unknown 类）等；期间仅 3 次需要显著人工介入（[arXiv:2407.21783 §2.2 与 Table 5](https://arxiv.org/abs/2407.21783)）。checkpoint 每卡 1 MB–4 GB 状态，目标是**压低 checkpoint 期间的 GPU 暂停并提高频率以减少恢复后损失的工作量**；存储侧（Tectonic，240 PB、持续 2 TB/s）需承接短时打满的突发写。诊断用 NCCL flight recorder（环形缓冲记录每次 collective 元数据与栈，watchdog/心跳超时时自动转储）。

**Google MPG（TPU fleet）**：把 fleet 效率分解为三层乘积（[arXiv:2502.06982 §4](https://arxiv.org/abs/2502.06982)）：

| 分量 | 定义（原文归纳） | 记账含义 |
|---|---|---|
| Scheduling Goodput（SG） | 应用**全部所需芯片同时可用**的时间（allocated chip-time）/ fleet 容量（chip-time） | 分布式作业要求所有卡同时在线；碎片化、等待协调都扣 SG |
| Runtime Goodput（RG） | **已保存进 checkpoint 的有效 chip-time** / allocated chip-time；论文明示“最后一次 checkpoint 与失败（或抢占）之间的工作不计入 RG” | 恢复损失直接进分母；慢数据加载、慢 checkpoint、编译都扣 RG |
| Program Goodput（PG) | 按 HLO 图形状估的理想执行时间 / 实际执行时间 | 程序效率；与故障无关但与有效产出相乘 |

这两个口径互补：Llama 3 给出作业级“有用训练/总时间”的一手观测与中断分类；MPG 给出可分解的记账结构（哪一层损失的芯片时间去哪了）。共同要点：**占用率（occupancy）不区分产出**——卡被分配但卡在 I/O 等待、或算的是将被回滚的工作，占用率照样高（MPG 论文对传统 occupancy 的批评）。

### 记账时区分六类量

| 量 | 定义 | 与吞吐的区别 |
|---|---|---|
| 有效训练 token / 已保存 step | 进入最终模型状态（或已 checkpoint 保护）的训练进展 | 吞吐量是“算得多快”，此项是“留下了多少” |
| 已提交 step（committed） | 优化器已执行、尚未被回滚声明的 step | 中断后是否算数取决于回滚边界，不是执行过就算 |
| 重算 / 回放 | 从最近有效 checkpoint 起重做的工作 | 消耗全部计算资源，产出为零 |
| 丢失数据 | 加载失败/损坏/未持久化的输入与状态 | 与重算分开记（原因与补救不同） |
| 恢复等待 / 状态加载 / 预热 | 等待处置、加载 checkpoint、重建进程组、预热到稳定吞吐的分段时间 | 每段单独计时；预热完成的判据要预先定义（如 step time 回到基线带内 N 步） |
| 健康窗口 | 满足全部四维判据、可正常承接工作的连续时段 | 与“进程存活”不同；见[处置选择](mitigation-and-recovery-principles.md)恢复判据 |

checkpoint 频率的权衡由此可量化：提高频率压低单次重算损失（Llama 3 的目标），但提高 I/O 与同步开销、压低运行 goodput（OCP 白皮书 §5.3.1 对频繁 checkpoint 的代价警告，[静默错误](silent-errors-and-integrity.md)来源核对）。两条曲线的交点没有通用值，按存储带宽、checkpoint 大小、故障率与环境实测。

## 四、推理侧：不能只统计成功请求

推理服务的可靠性记账必须包含失败侧，且成功/失败/取消/超时**分列**：

- 固定 vLLM 的请求终点分 `STOP` / `LENGTH` / `ABORT`（源码描述为客户端取消）/ `ERROR`（源码描述为可重试的请求级内部错误）；Prometheus `vllm:request_success` 虽名为 success，实际**按 finish reason 建标签**对全部完成请求增量——counter 求和不能称作“成功请求数”（固定 v0.14.0 源码口径，详见[推理时延指标](../07-inference/latency-metrics.md)）。
- **goodput 必须绑定已声明的 SLO 集合**：同一请求须满足全部已提供阈值才计入；无 SLO 集合的吞吐不能改名 goodput（同上）。
- **幸存者偏差**：延迟分位只含成功请求时，失败率上升反而可能“改善” p99——每张延迟/吞吐表并列错误、取消、超时计数，并说明超时由谁判定（客户端/代理/服务端）。
- **质量与降级成本单独记账**：降级模式（较小模型、关闭某些功能、拒绝长上下文）期间的服务量、质量指标与恢复过渡期单独成行；把降级期间的请求并入正常统计会同时污染可用性与质量两个维度。
- 错误预算的口径见 SRE（[Implementing SLOs](https://sre.google/workbook/implementing-slos/)，既有登记）：SLI 定义、预算消耗速率与剩余预算的联动是“可靠性统计驱动处置”的样板；将其迁移到训练侧时，分母从请求换成有效训练时间或已保存 step。

## 五、事件表 schema

最小可用三张表（字段名为建议，落地时可增不可减语义）：

```yaml
# 事件表（每起故障/中断一行）
- event_id: <稳定ID>
  object: {kind: node|job|service|run|rank_group, id: <身份键>, version_keys: {硬件/驱动/框架/镜像版本}}
  window_tag: <所属统计窗口>
  observed_start: <时间戳+时钟源>   # 首个异常观测
  observed_end: <时间戳+时钟源>     # 服务恢复判据达成
  cause_time: <时间戳|null|unknown> # 根因时刻（区别于发现时刻）
  category: <故障分类，见 FMEA 行>
  attribution: confirmed|suspected|unknown   # 归因强度，照 Llama 3 口径保留 unknown 类
  impact: {affected_objects: n, requests_or_steps: n, degraded_dimensions: [可用性|正确性|性能|可恢复性]}
  handling: {detection_source: <>, action: <隔离|重试|回滚|重启|人工介入|null>, by_automation: bool}
  recovery: {wait_s: x, load_s: x, warmup_s: x, recompute_s: x, lost_data: <描述|null>}
  censorship: none|right_censored|window_truncated
  evidence_refs: [<来源ID或本地case/experiment ID>]

# 窗口聚合表
- window: {start: <>, end: <>, clock: <>}
  denominator: {kind: chip_hours|node_hours|requests|steps|calendar_s, value: x}
  events: {count: n, primary_cause_breakdown: <>, overlapping_sets: <口径>}
  yield: {effective_training_s: x|n/a, committed_steps: x|n/a, goodput_slo_set: <名称|n/a>}
  coverage: {unobserved_spans: <列表|null>, reason: <>}
```

记录规则：所有时间量带单位；`recovery` 四段之和不必等于事件时长（等待可能先于事件结束判据）；`attribution` 保持三值，**不为了报表整洁把 unknown 强行归入硬件或软件**（Llama 3 的 Unknown 类即此纪律的公开样板）。

## 六、合成计算例：同一症状，四维结论不同

以下数字全部为**合成示例**（标注：非任何本地或来源系统的真实数值），只演示量纲与口径。

设定：单作业观察窗口 7 天＝168.0 h；窗口内发生一次“作业崩溃并自动重启”事件。时间线分解：计划内维护停机 2.0 h；意外事件：异常检测＋等待处置 0.5 h，恢复（加载 checkpoint 1.0 h＋重建进程组与预热 0.5 h）1.5 h，重算（从最近 checkpoint 回滚）3.0 h——重算期间 GPU 满速运行但产出作废。健康窗口＝168.0−2.0−0.5−1.5−3.0＝161.0 h（量纲：各项均为小时，直接加减）。

| 维度 | 该事件的记账 | 结论 |
|---|---|---|
| 可用性 | 在线（可承接工作）161.0/168.0≈95.8%；若“在线”定义为进程存在，则 165.5/168.0≈98.5%（重算期进程在跑） | 同一事件，在线判据不同，可用性差 2.7 个百分点 |
| 正确性 | 本例错误被检出并回滚：正确性无损；**同症状若是未检出的 SDC 污染 checkpoint，则 3.0 h 重算变 0 h 且污染固化**——丢失的不是时间而是模型状态 | 症状相同（崩溃重启），正确性结论相反 |
| 性能稳定性 | 预热 0.5 h 内 step time 高于基线带，仅影响该窗口 step 时间分布的尾部；均值几乎不动 | 性能维度“基本无恙”的结论不适用于依赖尾分位的 SLO |
| 可恢复性 | RTO＝0.5+1.5＝2.0 h；重算损失 3.0 h；由 checkpoint 间隔决定（间隔减半则重算≈1.5 h，但 I/O 开销上升） | 恢复维度给出可优化的杠杆，其他维度不给 |

把这个例子放大到 fleet 统计：若 168 h 内 32 张卡各有一起同类事件，按“卡·时”分母损耗＝32×(0.5+1.5+3.0) h＝160 卡·时；按 SG 口径，若该作业需要全部 512 卡同时在线，则作业级损失＝512×5.0 h（全体等一台恢复）——**分母与对象定义不同，同一批事件的统计相差一个并 factor**。这就是第一节要素表必须先于指标的原因。

## 七、适用边界与待确认

- 本文全部数字中，Llama 3 与 MPG 的数字是**来源方在其环境的一手观察**（16K H100 54 天快照；Google 内部 TPU fleet），限各自平台、规模与归因口径，不外推为任何集群的预期值；第六节为合成示例。
- 本地（本库所辖任何环境）**没有**长期事件数据；建立真实统计需按第五节 schema 现场采集，且采集系统部署不在本文范围。
- MTBF/MTTR 的分布检验方法（如更新过程检验）未登记原始统计来源，需要时另行取证，本文只给使用边界。
- 推理指标的字段级口径（TTFT/TPOT/ITL、finish reason、goodput SLO）以[推理时延指标](../07-inference/latency-metrics.md)为准，本文不重复定义。
- 指标间联动（错误预算政策、预算耗尽后的发布冻结）属 SLO 工程实践，本库仅登记口径来源。

## 来源核对范围

- [The Llama 3 Herd of Models, arXiv:2407.21783v3](https://arxiv.org/abs/2407.21783)：本批核读 §2 基础设施段——有效训练时间定义与 >90%、54 天 466/47/419 中断统计、Table 5 逐行百分比（GPU 类合计 58.7% 自洽核对）、3 次人工介入、checkpoint 每卡 1 MB–4 GB 与 Tectonic 240 PB/2 TB/s（峰值 7 TB/s）、NCCL flight recorder。表内“Faulty GPU 148 次”的绝对计数与 30.1% 在 HTML 渲染中不能自洽核对（148/419≈35.3%），本文只引用百分比。
- [ML Fleet Efficiency / ML Productivity Goodput, arXiv:2502.06982v1](https://arxiv.org/abs/2502.06982)：本批核读 §1–§5——SG/RG/PG 定义（§4.3，含“最后 checkpoint 到失败间工作不计入 RG”的原文）、occupancy 批评（§4.1）、按分量定位优化（§5、Table 2）。示例 fleet 数字未引用。
- [SRE Workbook: Implementing SLOs](https://sre.google/workbook/implementing-slos/) 与 [SRE Book: Monitoring Distributed Systems](https://sre.google/sre-book/monitoring-distributed-systems/)（既有登记）：SLI/错误预算口径与症状/观测区分。
- [SuperBench, USENIX ATC 2024](https://www.usenix.org/conference/atc24/presentation/xiong)（既有登记）：MTBI 22.61× 为仿真的边界声明。
- [OCP SDC in AI 2025](https://www.opencompute.org/documents/sdc-in-ai-ocp-whitepaper-final-pdf)（本批补读 §5.3.1）：频繁 checkpoint 的 goodput 代价与编排开销。
- [PyTorch elastic 2.6](https://docs.pytorch.org/docs/2.6/elastic.html)（既有登记）、[vLLM v0.14.0](https://github.com/vllm-project/vllm/tree/b17039bccc17b94a2ea107272ad7bc93508708df)（既有登记，经[推理时延指标](../07-inference/latency-metrics.md)转引）：重启/终点语义的版本化口径。
- 逐条主张与读取范围见[第三十批 T08-06 来源记录](../../docs/research/batch-30-t08-06-sources.md)。
- 待确认：本库辖内环境的长期事件采集启动条件；分布检验方法的原始统计来源；MPG 论文示例 fleet 的具体数值（未引用，如需另读）。
