---
id: reliability.mitigation-and-recovery-principles
title: 隔离、重试预算、降级与恢复选择
type: procedure
domain: reliability
status: draft
platforms: [generic]
source_refs:
  - src.google.sre-implementing-slos
  - src.google.sre-cascading-failures
  - src.google.sre-handling-overload
  - src.aws.backoff-jitter-2015
  - src.envoy.circuit-breaking-arch-latest-2026-10-21
  - src.kubernetes.job-lifecycle-v1-32
  - src.kubernetes.pod-lifecycle-v1-32
  - src.pytorch.elastic-2.6
  - src.ascend.mindspeed-llm-ha-v2.2.0
  - src.ietf.rfc9110
updated_at: "2026-10-21"
summary: 给出跨训练与推理的处置选择流程：按可靠性目标维度选隔离、冗余、重试、降级或恢复，并为每类措施固定证据门槛、影响域、状态前提、停止/回退与恢复判据；重试须带 deadline、预算与 jitter 退避；降级需显式业务判据；含冗余独立性检查与有限故障对照设计。
related_ids:
  - reliability.fault-models-and-propagation
  - reliability.dimensions-and-failure-domains
  - reliability.correlated-failure-source-case
  - training.checkpoint-state-consistency
  - training.elastic-training-and-membership
  - inference.routing-and-flow-control
  - inference.release-and-recovery
  - inference.pd-disaggregation
  - cluster-platform.control-plane-recovery
applicability:
  environment_refs: []
  notes: "跨平台方法框架。引用的平台机制分别登记：K8s v1.32 静态快照、PyTorch 2.6 固定 commit、MindSpeed-LLM v2.2.0 固定 tag、Envoy latest（带 2026-10-21 观察日期的可变页）；本文不构成对任何目标环境的适用性判断，真实现场执行须另依已有授权与目标环境核实（见授权边界）。"
verification:
  status: source_checked
  evidence_refs:
    - src.google.sre-cascading-failures
    - src.google.sre-handling-overload
    - src.aws.backoff-jitter-2015
    - src.pytorch.elastic-2.6
    - src.ascend.mindspeed-llm-ha-v2.2.0
  notes: "已对照所引 Google SRE 两章、AWS 退避抖动博客、PyTorch 2.6 elastic 文档与 MindSpeed-LLM v2.2.0 HA 文档核对各机制表述；选择流程与对照设计为本库原创整理，未在任何环境执行故障注入或处置演练。"
---

# 隔离、重试预算、降级与恢复选择

## 要回答的问题

故障确认后（模型与传播分析见[故障模型、跨层传播与共享失效分析](fault-models-and-propagation.md)），下一个问题是**选哪种处置、按什么顺序、何时停**。隔离、冗余、重试、降级、恢复不是同义手段：它们各自优化不同的可靠性维度，各有代价与失效边界。本文给出跨训练/推理/平台的选择流程与每类措施的记录字段；不提供任何"照抄可用"的参数值，所有阈值须按目标环境设定。

## 第一步：动手前固定六项

对任何处置动作，先写下六项再执行。缺任何一项的动作都是盲操作：

| 字段 | 问题 | 示例 |
|---|---|---|
| **目标维度** | 这次动作优先守住四维（可用性/正确性/性能稳定性/可恢复性）中的哪一维？ | 重试守可用性；隔离守可恢复性；降级可能牺牲正确性换可用性 |
| **证据门槛** | 什么证据支持这个动作？动手前必须已观察到什么？ | 隔离节点前：设备错误事件＋作业失败关联；不是单次性能抖动 |
| **影响域** | 动作本身会中断谁？ | 节点驱逐的**潜在**影响清单：被驱逐的 Pod 与在跑请求/进程、emptyDir/本地状态、经 rank 缺席向通信组与其他节点的传播（逐层核对，见[故障模型](fault-models-and-propagation.md) F1 行）；cordon 范围与驱逐豁免对象、残留资源按[节点摘除正文](../05-cluster-platform/node-drain-resource-reclamation.md)核对——不以 drain 成功证明全部清空 |
| **状态前提** | 动作成立要求系统处于什么状态？ | 回滚发布前提＝旧版本配置仍存在且兼容当前数据格式 |
| **停止/回退条件** | 什么信号说明动作无效或恶化，如何撤销？ | 重试 N 次仍失败→停止并升级；隔离后集群容量跌破下限→回补 |
| **恢复判据** | 怎样判定"恢复完成"并能撤离降级状态？ | 见下文恢复门槛，不是命令退出 0 |

## 按目标维度选措施

| 症状主导维度 | 首选方向 | 原因与代价 | 失效边界 |
|---|---|---|---|
| 可用性（服务/作业不可用） | 重试（暂态）、副本切换、重启 | 恢复服务最快；但重试放大负载、切换可能丢本地状态 | 无预算的重试引发风暴；切换是否有效按当前故障模式核对共享依赖是否实际生效、备用是否健康、路由是否收敛、剩余容量是否足够——共享域命中只是候选，证据不足时切换效果未知 |
| 正确性（输出/状态可疑） | **停止扩散**：隔离＋回退到已验证状态 | 错误状态重试只会复制错误 | 重试对错值无效；降级不能替代正确性门槛 |
| 性能稳定性（长尾/退化） | 限流、准入控制、扩容 | 保护剩余容量与延迟包络 | 过度限流把性能问题变成可用性问题 |
| 可恢复性（恢复慢/损失大） | 隔离故障对象、保住 checkpoint/状态副本 | 缩小下次恢复的范围与时间 | 隔离动作本身消耗容量；未验证的 checkpoint 不是可恢复保证 |

降级与隔离可以组合（隔离坏副本＋降级服务质量），但每个组合都要分别写六项字段。

## 重试：预算、退避与幂等

重试是最容易写错的方向。设计边界按五条核对：

1. **先判可重试性**。按四维判断：目标故障是暂态吗（[故障模型](fault-models-and-propagation.md)持续性分类）？请求幂等吗？错误信号是否显式标记不可重试？Google SRE 要求区分可重试/不可重试错误，过载的后端应返回明确状态让上层退避（[Addressing Cascading Failures](https://sre.google/sre-book/addressing-cascading-failures/)）。
2. **deadline 先于重试**。每个请求有截止时间，且 deadline 沿调用链传播、超时触发取消传播；重试必须在剩余预算内。没有 deadline 的重试是在给级联失效供弹药（同章）。
3. **预算三件套：次数、时间、并发**。次数：每请求上限（SRE 示例每请求最多 3 次尝试）；比例：客户端重试占其总请求的比例上限（SRE 示例 10%），并只在紧邻的上一层重试，避免多层相乘（[Handling Overload](https://sre.google/sre-book/handling-overload/)）；服务级：Envoy 推荐**重试预算**（retry budget，按活跃请求的比例动态允许重试）替代静态最大重试数（[Circuit Breaking](https://www.envoyproxy.io/docs/envoy/latest/intro/arch_overview/upstream/circuit_breaking)，其 `max_retries` 断路器即是并发上限的一种）。
4. **退避必须加 jitter**。纯指数退避保留同步聚簇：AWS 的实验显示退避后"there are still clusters of calls"、竞争未实质下降，而 jitter 使 100 竞争客户端的调用次数减半以上；Full Jitter（sleep 在 0 到 min(cap, base·2^attempt) 间均匀随机）工作量最少，Equal Jitter 避免极短睡眠，Decorrelated Jitter 上限随上次值扩大（[Exponential Backoff and Jitter](https://aws.amazon.com/blogs/architecture/exponential-backoff-and-jitter/)）。SRE 同样要求"随机指数退避"（[级联失效章](https://sre.google/sre-book/addressing-cascading-failures/)）。
5. **幂等、重放与重复**。接口"无服务端持久状态"不等于可自动重试：重试的正当性建立在**幂等语义**或"原请求未应用"的证据上（[RFC 9110 §9.2.2](https://www.rfc-editor.org/rfc/rfc9110.html#section-9.2.2)：非幂等请求不应自动重试，除非确知语义幂等或确认原请求从未被应用）；关联/请求 ID 是追踪标识不是幂等键——同一外部 ID 可对应多个内部请求（见[请求路由正文](../07-inference/routing-and-flow-control.md)）。**已送达未见响应**时原请求可能正在执行或已完成，重试是重复计算的风险决策：计费/配额、重复副作用与业务级去重的责任须显式指定；服务端去重未建立时保持 unknown。**流式输出边界**（按本库已核的普通 chat/completion 流式路径归纳）：已发送的 token 无法靠重试收回，续接须应用层协议。三类中断分开处理——连接建立失败（原请求可能未应用）、已送达未见响应（可能已执行/完成）、响应已部分提交（不可撤回，新请求重算时不得与已发部分不透明拼接）；其他引擎/版本的 KV/状态恢复协议未调查（unknown），不宣称全引擎无续传能力——KV 缓存与重算的机制边界见[推理执行与 KV Cache](../07-inference/execution-and-kv-cache.md)与[PD 分离](../07-inference/pd-disaggregation.md)（后者区分 connector 块重算与外部整请求重试）。

**训练侧的"重启预算"是同构概念**：Kubernetes Job 的 `backoffLimit`（默认 6，指数退避）限定 Job 失败重试预算——`restartPolicy: Never` 下计**失败 Pod 次数**，`OnFailure` 下**同一 Pod 内的容器重试也计入**，失败策略可改变计数对象（[Job 快照](https://v1-32.docs.kubernetes.io/docs/concepts/workloads/controllers/job/)，计数分支另见[作业生命周期](../05-cluster-platform/kubernetes-job-lifecycle.md)）；容器重启退避 10s 起封顶 300s、运行 10 分钟后重置（[Pod 生命周期快照](https://v1-32.docs.kubernetes.io/docs/concepts/workloads/pods/pod-lifecycle/)）；PyTorch elastic 的 `max-restarts`（torchrun CLI 默认 0，`WorkerSpec` API 默认 3）限定**失败重试**预算。注意文档概括与实现分支的差异：`run.py` 的 elastic 示例标题把"最多三次成员变化或失败"合在一起概括，而固定 commit 的 `api.py` 实现按状态分支——UNHEALTHY/FAILED 在剩余预算大于零时扣减再重启，HEALTHY 且等待新节点的重建不扣减（[PyTorch 2.6 elastic 文档](https://docs.pytorch.org/docs/2.6/elastic/run.html)；固定 commit 的 [run.py L157–165](https://github.com/pytorch/pytorch/blob/1eba9b3aa3c43f86f4a2c807ac8e12c4a7767340/torch/distributed/run.py#L157-L165) 为示例概括、[api.py L887–917](https://github.com/pytorch/pytorch/blob/1eba9b3aa3c43f86f4a2c807ac8e12c4a7767340/torch/distributed/elastic/agent/server/api.py#L887-L917) 为扣/不扣预算的状态分支；本文按实现分支表述，未逐路径核对的离开/故障组合 unknown）。这些默认值只说明机制存在，不是推荐配置，也不把它们当应用 attempt 或整体恢复次数。

## 隔离与降级

**隔离**分两类，先分清对象：

- **资源隔离**（把疑似故障对象移出服务/调度域）：节点驱逐（drain）与设备隔离的前提是"该对象不再承载不可牺牲的状态"，流程与恢复边界见[节点驱逐与资源回收](../05-cluster-platform/node-drain-resource-reclamation.md)；设备级隔离（如 DCGM 诊断返回 isolate 类错误后移出）的判定边界见[硬件健康证据](../01-hardware/health-evidence.md)。隔离与重启的证据门槛**不作无条件排序**，按动作粒度分别评估两组独立属性：**控制/电源状态能否撤销**（摘流/停止准入可撤销；下电可再上电——但电源可恢复不等于应用状态可恢复）与**应用/证据状态能否重建**（重启或驱逐会终止进程、驱逐还删除 emptyDir 等易失状态；已持久化/导出的证据不受影响）。证据保全按动作与载体分别评估：仅摘流/停止准入不触碰进程现场，驱逐/终止/复位会清除进程与易失状态——执行前先固定需保留的证据（内存快照、日志导出）；不把任何隔离或重启方式一律判为保留或清除全部现场。临时隔离≠永久判坏，隔离≠修复（复役前要重新验收），重启也不因单次代价小而免六字段核对。
- **流量隔离**（把流量从坏对象/坏路径移开）：端点摘除、路由切换、准入拒绝；推理侧机制见[请求路由、准入与流控](../07-inference/routing-and-flow-control.md)。摘除的判据是探针/健康信号，但探针有假阳假阴——摘除窗口与恢复窗口要成对设计。

**降级**按牺牲什么分三层，越往下越需要业务判据：

| 层 | 做法 | 必须显式登记的判据 |
|---|---|---|
| 功能降级 | 关闭非关键功能（日志采样、诊断开关、可观测采样率下调） | 每项功能的关闭对正确性/合规的影响 |
| 质量降级 | 换更小模型/更低精度/更短上下文 | **业务判据**：输出质量必须过的门槛（用什么 oracle、谁批准低于平时质量的输出继续服务）；评估方法见[推理输出质量对照评估](../07-inference/output-quality-evaluation.md) |
| 容量降级 | 拒绝部分流量（按关键度分级丢弃、队列上限） | 哪些流量可丢、丢多久、谁决定 |

质量降级没有业务判据时只能当故障处理，不能当处置手段。

## 恢复选择：重算、回退还是切换

| 场景 | 选项 | 关键边界 |
|---|---|---|
| 训练：故障前有 checkpoint | 回退到最近一致 checkpoint 重算 | checkpoint 一致性（优化器/数据进度/RNG）是前提，恢复核验方法见[Checkpoint 状态一致性](../06-training/checkpoint-state-consistency.md)；丢失步数＝故障点减恢复点，是恢复损失的口径 |
| 训练：已有可读取且一致的恢复点（或已明确实现的其他恢复协议） | 弹性重建成员后从恢复点继续 | PyTorch 2.6 elastic 重启会终止并重建**全部** worker 进程（幸存 worker 的内存状态不作保留前提），**状态恢复是应用责任**（save/load，[elastic 文档](https://docs.pytorch.org/docs/2.6/elastic/run.html)）；MindSpeed-LLM v2.2.0 以副本机制支持缩容续训与 UCE 在线修复（[HA 文档](https://github.com/Ascend/MindSpeed-LLM/blob/53f3639c3da9c000a187c44cc0c08d55026ddded/docs/pytorch/features/high_availability.md)，依赖其外部组件约束；不把 PyTorch 的预算语义强加于该副本路径） |
| 推理：单副本故障 | 切换到健康副本 | 前提＝路由能摘除并重定向（见路由正文）；请求重试仍须过幂等/重复计算判定与预算（见重试一节，关联 ID≠幂等键）；流中断按三类情形处理（未应用/已送达未见响应/已部分提交，见流式输出边界） |
| 推理：KV/状态可疑 | 丢弃缓存重算（**有条件的恢复候选**） | 前提＝可疑缓存确实失效（不再被其他复用层命中）且错误源不在权重/输入/执行路径（否则重算复现错误）；结果判据＝质量/一致性检查通过，不成立时改选健康副本或已验证版本；与副本切换的取舍见[服务发布、副本故障与恢复验证](../07-inference/release-and-recovery.md) |
| 发布缺陷 | 回滚到上一版本 | 回滚不是恢复完成的证明；回滚后的正确性与性能须按恢复门槛复验（同上） |

**恢复门槛**沿用[可靠性维度与故障域](dimensions-and-failure-domains.md)的六条退出条件；另加一条：处置引入的降级（隔离掉的容量、降过的质量）要么恢复要么显式登记为"长期降级"，不允许无声留存。

## 冗余独立性、共享依赖与故障预算

- **冗余独立性检查**在建设期完成：副本/路由/供电/存储/控制面/配置批次的共享核对清单见[故障模型](fault-models-and-propagation.md)末节；一个"全部骨干连接被同一次命令撤除"的完整公开案例见[相关故障与冗余失效的公开案例](correlated-failure-source-case.md)（其物理冗余布局未披露）。
- **故障预算（error budget）**把"还能承受多少不可用"变成显式额度：SLO 与剩余预算驱动"快烧完时冻结发布、优先可靠性"的决策（[Implementing SLOs](https://sre.google/workbook/implementing-slos/)）。预算的存在不改变本文任何措施的边界，只给"现在该不该冒险"提供依据。
- **控制面失败的处置**单独设计：控制面不可用时数据面是否继续（已准入作业继续跑、新作业不能进）、恢复积压如何排队，见[控制面恢复](../05-cluster-platform/control-plane-recovery.md)；处置通道本身（堡垒机、DNS、认证）与被管系统的共享依赖按 Meta 案例的检查问题核对。

## 有限故障对照设计

处置措施的有效性要有**事前设计的对照**，不能等真实故障来检验。最小设计（可牺牲环境或演练窗口执行）：

1. **预登记**：处置对象、期望指标（如"重试风暴不再放大"）、通过判据、停止条件；先写后测。
2. **对照条件**：同一负载与版本下，有/无该措施各跑一轮（或 A/B 副本），差异只在措施本身。
3. **注入范围有限**：一次注入一个故障类（对应[故障模型](fault-models-and-propagation.md) FMEA 表的一行），注入点在预登记清单内。
4. **观察放大与残余**：记录措施生效期间的重试率、延迟、正确性样本；特别记录**措施失效的边界**（预算烧尽后发生了什么）。
5. **结论限定**：只对"该环境该版本该负载"有效；注入结果不是真实故障率的证据。

## 授权与执行边界

本文是方法文档，**不赋予执行权限**。其中任何处置（驱逐节点、隔离设备、切换路由、回滚发布、注入故障）都是对目标环境的主动变更：实际执行须依据用户已有授权、按当时环境核实六项字段；文档引用的任何工具语义（K8s/PyTorch/MindSpeed/Envoy 的版本与默认值）不构成对目标集群的适用性判断，也不保证无损恢复。

## 来源核对范围

- [Google SRE Book：Addressing Cascading Failures](https://sre.google/sre-book/addressing-cascading-failures/)：核对随机退避、每请求重试上限、服务级重试预算示例、可重试/不可重试区分、deadline 传播。
- [Google SRE Book：Handling Overload](https://sre.google/sre-book/handling-overload/)：核对每请求 3 次尝试、客户端 10% 重试比例预算、仅在上一层重试、按关键度丢弃。
- [AWS 架构博客：Exponential Backoff and Jitter](https://aws.amazon.com/blogs/architecture/exponential-backoff-and-jitter/)：核对纯退避聚簇问题、Full/Equal/Decorrelated Jitter 定义与实验结论；未取具体数值建议。
- [Envoy Circuit Breaking 架构页](https://www.envoyproxy.io/docs/envoy/latest/intro/arch_overview/upstream/circuit_breaking)：核对五类断路器与 retry budgets 推荐（latest 可变页，2026-10-21 观察）。
- [Kubernetes v1.32 Job 快照](https://v1-32.docs.kubernetes.io/docs/concepts/workloads/controllers/job/)与 [Pod 生命周期快照](https://v1-32.docs.kubernetes.io/docs/concepts/workloads/pods/pod-lifecycle/)：核对 backoffLimit 默认 6 及 Never/OnFailure 计数对象、重启退避 10s–300s 与 10 分钟重置。
- [RFC 9110 §9.2.2](https://www.rfc-editor.org/rfc/rfc9110.html#section-9.2.2)：核对幂等定义、幂等只覆盖所请求的效果、非幂等请求自动重试的两个例外条件与代理禁令。
- [PyTorch 2.6 elastic](https://docs.pytorch.org/docs/2.6/elastic/run.html)：核对 max-restarts 两处默认值（CLI 0/API 3）、重启终止全部 worker、状态恢复是应用责任；失败分支扣预算与 HEALTHY 扩容不扣的实现分支按登记 commit 的 run.py/api.py/train_script 口径。
- [MindSpeed-LLM v2.2.0 HA 文档](https://github.com/Ascend/MindSpeed-LLM/blob/53f3639c3da9c000a187c44cc0c08d55026ddded/docs/pytorch/features/high_availability.md)：核对副本/缩容续训/UCE 在线修复的表述边界与其外部组件约束。
