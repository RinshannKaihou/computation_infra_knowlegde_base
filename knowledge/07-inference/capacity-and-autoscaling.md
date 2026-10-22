---
id: inference.capacity-and-autoscaling
title: 容量、扩缩容与冷启动决策
type: procedure
domain: inference
status: draft
platforms: [generic, nvidia, amd, ascend]
source_refs:
  - src.kubernetes.hpa-v1-32
  - src.kserve.autoscaling-v0-20-3f4067e
  - src.vllm.production-stack-v0-1-9
  - src.vllm.inference-v0-14
  - src.vllm.model-loader-v0-14
  - src.google.sre-implementing-slos
  - src.keda.scaledobject-spec-2.18
updated_at: "2026-10-22"
summary: 把请求/token 需求、SLO/goodput 目标、模型加载时间与资源预算连成可验证的扩缩容决策：先建立单副本与集群容量口径，再比较请求率、队列、并发/token/KV 与设备指标四类触发器的滞后、振荡与冷启动代价；覆盖最小冗余、scale-to-zero 条件、扩容 ready gate、缩容 drain 与 PD 双池联动，并给出有限增压/阶跃/收缩的对照与容量不足判据。
related_ids:
  - inference.routing-and-flow-control
  - inference.latency-metrics
  - inference.model-loading-and-readiness
  - inference.pd-disaggregation
  - inference.distributed-inference-layouts
  - cluster-platform.node-drain-resource-reclamation
  - cluster-platform.contention-capacity-validation
applicability:
  environment_refs: []
  notes: "控制面样板为 Kubernetes v1.32 静态快照、KServe 0.20 线（KPA/WVA）与 production-stack v0.1.9（KEDA）；引擎侧为 vLLM v0.14.0。具体机型/模型/版本的容量与冷启动数值均为待测变量，本文不给通用参数。"
verification:
  status: source_checked
  evidence_refs:
    - src.kubernetes.hpa-v1-32
    - src.kserve.autoscaling-v0-20-3f4067e
    - src.vllm.production-stack-v0-1-9
    - src.vllm.inference-v0-14
    - src.keda.scaledobject-spec-2.18
  notes: "已核对 v1.32 HPA 任务页（公式/容差/稳定窗/behavior 默认）、KServe kpa-autoscaler 与 llmisvc-autoscaling（WVA）文档、production-stack autoscaling-keda 教程与 helm 模板、vLLM v0.14.0 弹性扩缩容与排空实现。2026-10-22 补核 KEDA v2.18 ScaledObject 规范的 idleReplicaCount/cooldownPeriod（IQ-07/08），不构成与上述集成样板的版本配套声明。未部署任何 autoscaler、未压测容量。逐条主张与定位见 docs/research/batch-28-t07-09-sources.md 与 independent-quality-audit-2026-10-22-fixes.md。"
---

# 容量、扩缩容与冷启动决策

## 目标与前置

扩缩容决策回答：**给定负载画像与 SLO 目标，当前副本数是否够、不够先加谁、够了何时减、减到零是否安全**。它由四块输入组成——负载（到达率、长度分布、并发形态）、单副本容量、副本启动时间（冷启动）、资源供给上限；任何一块缺失时只能保守运行。进入决策前先固定模型/引擎/后端版本、dtype、量化、`max_model_len`、`max_num_seqs`、KV 配置与并行布局（这些直接决定单副本容量，见[分布式推理布局](distributed-inference-layouts.md)）。

## 单副本与集群容量口径

1. **按瓶颈定容量**：推理副本的瓶颈可能是 KV 容量（可并发 token 数）、算力（token 生成速率）或入口并发（连接/队列）。vLLM 启动日志给出 `GPU KV cache size` 与 `Maximum concurrency`（=KV 容量 / `max_model_len` 量级）作为容量上界的直接证据（[parallelism_scaling 文档口径，T07-06 已核](distributed-inference-layouts.md)）。上界不等于 SLO 内的有效容量。
2. **按 SLO 定有效容量**：固定负载分布（到达过程、prompt/completion 长度分布、并发）后，单副本有效容量 = 该负载下仍满足 TTFT/TPOT/E2E 分位目标的最大到达率；判据与统计口径（分母、窗口、goodput 定义）沿用[延迟与吞吐指标字典](latency-metrics.md)与 SRE 的 SLO 方法（[Implementing SLOs](https://sre.google/workbook/implementing-slos/)）。**有效容量必须实测**，来源不给数值。
3. **集群口径**：集群容量 ≠ 单副本容量 × 副本数。路由层的均衡效率（见[请求路由与流控](routing-and-flow-control.md)）、长短混合下的副本倾斜、共享入口的排队都会折损；容量核算要带折损系数（各环境实测），并区分"总吞吐容量"与"尾延迟 SLO 容量"（后者通常先到顶）。

## 触发器比较：请求率、队列、并发/KV、设备指标

| 触发信号 | 反映什么 | 滞后与振荡 | 样板证据 |
|---|---|---|---|
| CPU/内存利用率（Resource metrics） | 副本进程资源压力 | 对推理常不敏感（GPU 是瓶颈时 CPU 低而服务已过载）；K8s 资源指标要求 requests 已设置 | K8s HPA（v1.32：容差 0.1、同步周期 15s，[任务页](https://v1-32.docs.kubernetes.io/docs/tasks/run-application/horizontal-pod-autoscale/)）；production-stack router 自身用 CPU utilization 模板（[hpa-router.yaml](https://github.com/vllm-project/production-stack/blob/20a658044af0dea70e9e0136494bb9979cfd9fab/helm/templates/hpa-router.yaml)） |
| 请求率/并发（QPS、concurrency） | 入口负载强度 | 请求成本不均时（长/短请求）QPS 与容量错位；KServe KPA 用 60s 稳定窗＋2×目标并发进 6s panic 窗缓解滞后（[KPA 文档](https://kserve.github.io/website/docs/model-serving/predictive-inference/autoscaling/kpa-autoscaler)） | KServe KPA：scaleMetric 默认 concurrency，target 软限 vs containerConcurrency 硬限 |
| 排队深度（queue depth） | 过载的**结果**信号，直接关联尾延迟 | 已排队才触发 → 天然滞后；阈值与轮询间隔决定响应速度 | production-stack KEDA 教程：`vllm:num_requests_waiting` 阈值 5、pollingInterval 15s、cooldownPeriod 360s、min/max 1-3（[autoscaling-keda.rst](https://github.com/vllm-project/production-stack/blob/20a658044af0dea70e9e0136494bb9979cfd9fab/docs/source/use_cases/autoscaling-keda.rst)）——教程示例值，非推荐值 |
| token 信号（须先选定统计对象） | 三种不同对象：**到达 token 需求**（到达请求的 prompt/期望输出量）、**在途/排队工作量**（waiting token、并发 token）、**已处理 prompt/output token 速率**（处理**结果**，非需求——引擎达处理上限后已处理 token/s 可基本不变而积压持续增长，概念推演非实测） | 饱和盲区（只用处理速率会漏需求增长）；跨副本聚合可掩盖局部积压；长窗口平滑突发延迟触发、短窗口受阶段/批次波动影响需配稳定策略；prefill 与 decode token 成本不同需分列或加权（本库机制归纳，口径参照[指标字典](latency-metrics.md)的 arrival/attempted/completed 区分与 token counter 转速率要求） | 概念级条目；可经 custom/external metrics 通道接入（通道见 K8s HPA 行）；与队列深度、SLO 同看；三平台统一指标名与阈值 unknown |
| 加速器设备指标（GPU/NPU 利用率、设备内存） | 设备侧压力；主机 CPU/内存不能替代（KPA 文档亦提示 GPU 利用率随任务波动） | 采集粒度与窗口影响判读；静态权重占用高≠无服务容量（可用容量看 KV/并发余量） | 概念级条目（本库归纳）；版本化 exporter/指标名按平台档案核对，未取得前保留 unknown，不发明统一阈值 |
| 推理特有指标（KV 利用率、请求饱和度） | 引擎内部压力，最贴近真实瓶颈 | 依赖指标暴露与采集链路（Prometheus）；各引擎指标名/口径按版本核对 | KServe LLMInferenceService×WVA：按 KV cache 利用率、队列深度、请求饱和度算副本数，发布 `wva_desired_replicas`，HPA（经 Prometheus Adapter）/KEDA 直通执行（[llmisvc-autoscaling](https://kserve.github.io/website/docs/model-serving/generative-inference/llmisvc/autoscaling/llmisvc-autoscaling)） |

振荡控制按作用范围区分：**稳定窗**（K8s 缩容默认 stabilizationWindow 300s，窗口内取最高建议——与控制器 flag `--horizontal-pod-autoscaler-downscale-stabilization` 默认 5min 是同一默认机制的两个视图，**不叠加**计算）、**缩至零的冷却期**（[KEDA v2.18 `cooldownPeriod`](https://keda.sh/docs/2.18/reference/scaledobject-spec/#cooldownperiod)，从最后一次触发器报告活跃后计时，只作用于缩至 0；普通 1↔N 副本变化由 HPA 控制）、**变化率限制**（K8s behavior 策略，默认缩容 Percent 100 / periodSeconds 15s——15s 是默认策略的周期，非所有策略固定值）。上表 HPA 行的容差 0.1 与 15s 同步周期也均为**默认值**（可配置）；资源指标要求 Pod 设置 requests 的条件限定于 utilization 类计算。指标出错时的方向不对称是通用设计：K8s 在某指标出错时**跳过缩容、允许扩容**（保守放大而非保守缩小）。

## 冷启动与资源供给

- **冷启动构成**：新副本从调度到可服务 = 镜像拉取＋调度等待 → 权重加载（load-format 分派、分片/量化影响读取量；TP 每进程读全量权重使读取时间随 TP 规模增长，官方建议转分片 checkpoint 解耦，[conserving_memory.md](https://github.com/vllm-project/vllm/blob/b17039bc/docs/configuration/conserving_memory.md)）→ profiling/KV 容量计算 → warmup/图捕获 → ready（五阶段边界见[权重加载与引擎 ready](model-loading-and-readiness.md)）。来源中有**示例性**耗时/冷启动描述（如 sleep-wakeup 教程的样例日志、KPA 文档的冷启动解释），但均不构成可迁移基线——本文目标部署的各阶段耗时是待测变量（教程示例不作为本部署性能预期）；readiness 探针/ready gate 决定流量何时进来（机制见[服务发布与恢复](release-and-recovery.md)）。
- **扩容 ready gate（两个不同机制，勿混用）**：① 副本级——新副本须经 readiness/预热并计入路由可服务集合（控制面机制，见[服务发布与恢复](release-and-recovery.md)）；② 引擎内**弹性 EP 拓扑重配置**——`scale_elastic_ep` 先轮询现有 DP 引擎空闲（`wait_for_requests_to_drain`，默认 300s，超时抛 TimeoutError——该次变更应停止并保留证据），再增减 DP core 数（[async_llm.py L801-855](https://github.com/vllm-project/vllm/blob/b17039bccc17b94a2ea107272ad7bc93508708df/vllm/v1/engine/async_llm.py#L801-L855)）；扩缩容标志为真时，已挂载的 ScalingMiddleware 对**新进入**的 HTTP 请求回 503，在途流继续排空（标志的设置/清除方与异常恢复链未核，unknown）。② 是**同一逻辑服务的 DP engine cores 分布式拓扑重配置**（固定实现要求 Ray DP 后端：向现有 cores 发分布式重配置请求、创建新 cores 并等待其 ready 与既有 cores 完成重配置，[core_client.py L1278-1358](https://github.com/vllm-project/vllm/blob/b17039bccc17b94a2ea107272ad7bc93508708df/vllm/v1/engine/core_client.py#L1278-L1358)）——不是 K8s 副本层面的变更；新 core ready 也不等于副本 readiness/路由传播成立，② 不检查也不替代 ① 。
- **缩容 drain**：缩掉的副本先从路由/端点摘除、排空在途流式请求再退出（K8s 侧 preStop＋宽限期语义见[服务发布与恢复](release-and-recovery.md)）；**被移除进程的本地 KV/prefix cache 不保留**——缩容后的缓存效果取决于缓存所在层（外部缓存/offload 路径按所选实现核对，见[PD 分离](pd-disaggregation.md)）与路由变化、前缀命中、负载的共同作用；TTFT 是否变差是**待验证风险**，不预设必然恶化或必然恢复。
- **scale-to-zero 的配置与适用条件**：KServe KPA 置 `minReplicas: 0` 且无流量时缩零（仅 Knative/serverless 模式，见下节模式分支）；production-stack KEDA 教程用 `minReplicaCount: 0`＋流量保活触发器（该触发器的作用是**有流量时防止缩零**）。低峰流量需能接受冷启动时延，入口层需能把冷启动期的请求排队或返回明确状态；P99 严格且流量突增时须另外验证容量与时延预算。
- **KEDA 的空闲副本限制**：[v2.18 `idleReplicaCount`](https://keda.sh/docs/2.18/reference/scaledobject-spec/#idlereplicacount) 仅支持 **0**，且设置时须小于 `minReplicaCount`；不能因为 `2 < 5` 就把 `minReplicaCount: 5`、`idleReplicaCount: 2` 当成受支持配置。若要保留 n 个常驻副本，应省略 `idleReplicaCount` 并设置 `minReplicaCount: n`。这些是 KEDA v2.18 规范边界，未确认上述集成样板的实际 KEDA 版本，不能据此宣布版本配套。
- **从零重新激活**：零副本时引擎自身的 waiting 类指标不再可观测，谁继续观测新流量、产生可用指标并触发从零扩容须单独核查。该集成样板的指标可用性与保活触发器之外的重唤链路仍未验证（unknown），缩零配置不构成完整可用方案。
- **睡眠模式变体**：vLLM sleep/wakeup 让引擎驻留进程但释放资源（如 GPU 内存，production-stack [sleep-wakeup 教程](https://github.com/vllm-project/production-stack/blob/20a658044af0dea70e9e0136494bb9979cfd9fab/docs/source/use_cases/sleep-wakeup-mode.rst)）；唤醒成本依 sleep level 与实现而异（固定 commit 的 worker 对不同 level 有不同处理），本文未核完整恢复路径，不预设"唤醒=全量权重重载"或"只省进程重启"任一结论（须测）。
- **资源不可得**：扩容请求可能因集群资源不足悬置（调度等待语义见[配额、排队与准入](../05-cluster-platform/admission-and-placement.md)）；容量规划必须包含"扩不上去"分支——入口层降级/排队/拒绝策略（见[请求路由与流控](routing-and-flow-control.md)）。
- **PD 双池联动**：PD 分离时 prefill 池与 decode 池分别触发、分别扩缩，且 KV 传输链路（connector 前提）必须与两侧拓扑同步；单侧扩容改变不了另一侧瓶颈。双池容量联动无通用公式，按[PD 分离](pd-disaggregation.md)的指标与失败链分别规划。**KServe/WVA 样板的额外约束**：LLMInferenceService 的 `spec.scaling` 与 `spec.replicas` 互斥；执行器 HPA/KEDA 二选一；PD 场景 decode 与 prefill 组件**必须使用同一种 actuator**（WVA 文档 Prefill Scaling 节），不可混搭（[llmisvc-autoscaling](https://kserve.github.io/website/docs/model-serving/generative-inference/llmisvc/autoscaling/llmisvc-autoscaling)）。
- **最小冗余（本库规划建议，非通用规则）**：对故障期间仍须服务的部署，缩容下限应按故障模型与恢复窗口确定冗余（例如无共享故障域、剩余副本仍有足够 SLO 容量时取 ≥2）；副本数量本身不构成可用性保证——共享故障域、剩余容量不足、或控制器/空闲策略使实际 ready 数低于配置下限时仍会中断。未实测条件下的具体下限为待定变量。

**KServe 样板的模式分支（选用前先定位路径；字段与必需组件逐路径对应，不可跨模式搬用）**：

| 路径 | 关键字段 | 必需前置（文档口径） |
|---|---|---|
| InferenceService＋Knative（KPA） | `minReplicas`/`scaleTarget`/`scaleMetric`/containerConcurrency | Knative/KPA 路径本身（[KPA L8-23](https://github.com/kserve/website/blob/3f4067ea87dd84194bddb1b563051c84306c7997/docs/model-serving/predictive-inference/autoscaling/kpa-autoscaler.md#L8-L23)）；Prometheus/Grafana 为可选观测组件，非必要指标链 |
| InferenceService＋Standard（HPA） | `deploymentMode: Standard`＋`autoscalerClass: hpa`＋predictor 的 `scaleMetric`/`scaleTarget` | Metrics Server（资源指标样板；[HPA 文档 L17-43](https://github.com/kserve/website/blob/3f4067ea87dd84194bddb1b563051c84306c7997/docs/model-serving/predictive-inference/autoscaling/hpa-autoscaler.md#L17-L43)） |
| InferenceService＋Standard/Raw（KEDA） | `autoscalerClass: keda`＋`spec.predictor.autoScaling.metrics` | KEDA 与 ScaledObject 路径；外部指标后端按所选触发类型配置，不一概要求 Prometheus（[KEDA 文档 L18-89](https://github.com/kserve/website/blob/3f4067ea87dd84194bddb1b563051c84306c7997/docs/model-serving/predictive-inference/autoscaling/keda-autoscaler.md#L18-L89)） |
| LLMInferenceService＋`spec.scaling`（WVA） | `spec.scaling`（与 `spec.replicas` 互斥——固定 replicas 是另一种选择，不因资源类型自动启用 WVA） | WVA controller＋VariantAutoscaling CRD＋Prometheus（采集推理 Pod 指标与 WVA 指标两类）；HPA actuator 另需 Prometheus Adapter 的 `wva_desired_replicas` external metric 规则，KEDA actuator 另需 KEDA＋集群 ConfigMap（[WVA 文档 L13-80](https://github.com/kserve/website/blob/3f4067ea87dd84194bddb1b563051c84306c7997/docs/model-serving/generative-inference/llmisvc/autoscaling/llmisvc-autoscaling.md#L13-L80)） |

## 有限对照与判据

对固定部署，用三组对照标定扩缩容参数（判据口径同[路由对照](routing-and-flow-control.md)；**本对照设计为本库方法**，实际执行依既有授权与现场条件）。每轮先固定记录表：部署/负载身份（引擎/模型/副本数/布局、负载生成器与输入集、候选扩缩容策略与参照配置）、每档负载上限与预热/观察时长、各判据的分母与窗口。

1. **增压曲线**：从低到高**有界**步进负载（预设终点档位与单档时长），记录每档的逐请求 SLO 达标率（分母分类：attempted/failed/cancelled/rejected）、waiting 深度、KV 利用率、goodput——得到触发阈值与容量缺口的先导信号；任一档达预设负载上限、错误预算或质量阈即停。
2. **阶跃响应**：稳态→突增（超当前容量），记录从触发到新副本 ready 且分流生效的全链路时延（触发延迟＋冷启动＋传播），校验冷启动窗口内入口层的排队/拒绝是否在预算内。
3. **收缩**：高负载→撤流，记录缩容稳定窗、缓存命中率与 TTFT 的同窗变化（不预设方向）、副本数曲线，校验 cooldown 与稳定窗是否造成控制环振荡。

每轮同窗记录：错误分类（拒绝/超时/取消）、排队分位、副本数曲线（期望/当前/ready 三线）、资源水位、质量抽查（固定输入集）、**成本口径**（资源占用时长×单价或每单位 goodput 成本——实际价格未知时留空并保留资源占用时长记录）。

**判据（预登记，区分症状与归因）**：
- **SLO 违约记录**＝逐请求达标率或分位 gate 未达标（症状，非根因）；
- **触顶告警**＝已达 maxReplicas 且 SLO 未达标——这是"配置上限内无法缓解"的告警，**不直接判定容量根因**（路由不均、故障副本、指标失真、共享瓶颈均可能；扩容悬置/资源不可得单独记录原因）；
- **振荡判据**（仅在固定或已知负载形态下判定）＝预登记观察窗内副本数变向次数/幅度超阈**且**排除负载驱动（正常撤流缩容、周期负载不计）；负载未知时只记录曲线不下振荡结论。

停止与恢复闭环：预登记过载（错误率/尾延迟超阈）、副本不健康、采集失败的停止条件；停止后撤压、恢复配置与副本边界，核对流量、资源、错误率与 SLO 回到基线窗口后才算本轮结束。

## 边界与未知

- WVA 控制器（llm-d/workload-variant-autoscaler）实现未取回，本文按 KServe 文档集成口径引用；KEDA ScaledObject 完整字段未核。
- vLLM sleep 模式：已核 worker 层分支（sleep level 1/2 不同处理、wake 调 allocator，固定 commit gpu_worker L109-155）与 production-stack 教程口径（示例值不作基线）；allocator 恢复链与完整唤醒路径未核（unknown）。
- 冷启动各阶段耗时与容量数值：未取得适用于本部署的三平台容量/阶段耗时基线（教程示例值不作基线），一律待测；本文所有阈值（KEDA 5 等）为样板示例或配置项，不是推荐值。
- K8s 侧缩容 drain 与引擎侧排空 API 是两套机制，跨层组合（pod 删除信号→引擎排空）未实测。
- 未部署任何 autoscaler，未执行对照。

## 来源与验证记录

- [Kubernetes v1.32 HPA 文档](https://v1-32.docs.kubernetes.io/docs/tasks/run-application/horizontal-pod-autoscale/)：控制环参数、公式与容差、稳定窗、behavior 默认。
- [KServe 0.20 线](https://kserve.github.io/website/docs/model-serving/predictive-inference/autoscaling/kpa-autoscaler)（网站仓 pin 3f4067e）：KPA 语义、WVA 集成；KEDA 字段限制另按下项核对。
- [KEDA v2.18 ScaledObject 规范](https://keda.sh/docs/2.18/reference/scaledobject-spec/)：`idleReplicaCount` 仅支持 0、与 `minReplicaCount` 的关系，以及 `cooldownPeriod` 只作用于缩至零。
- [vLLM Production Stack v0.1.9](https://github.com/vllm-project/production-stack/tree/vllm-stack-0.1.9)：KEDA 教程（waiting 深度触发）、router HPA 模板、sleep/wakeup 教程。
- [vLLM v0.14.0 固定快照](https://github.com/vllm-project/vllm/tree/b17039bccc17b94a2ea107272ad7bc93508708df)：弹性扩缩容排空实现、KV 容量日志口径、conserving_memory、sleep 分支的 worker 层实现（level 1/2 不同处理、wake 调 allocator，L109-155——allocator 与完整恢复路径未核）。
- [SRE Workbook Implementing SLOs](https://sre.google/workbook/implementing-slos/)：SLO 口径与误差预算背景。
- 逐条主张与证据定位见[第二十八批 T07-09 来源记录](../../docs/research/batch-28-t07-09-sources.md)。
- 当前验证范围：来源核对；未部署、未压测。
