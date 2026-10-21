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
updated_at: "2026-10-21"
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
  notes: "已核对 v1.32 HPA 任务页（公式/容差/稳定窗/behavior 默认）、KServe kpa-autoscaler 与 llmisvc-autoscaling（WVA）文档、production-stack autoscaling-keda 教程与 helm 模板、vLLM v0.14.0 弹性扩缩容与排空实现。未部署任何 autoscaler、未压测容量。逐条主张与定位见 docs/research/batch-28-t07-09-sources.md。"
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
| 推理特有指标（KV 利用率、请求饱和度） | 引擎内部压力，最贴近真实瓶颈 | 依赖指标暴露与采集链路（Prometheus）；各引擎指标名/口径按版本核对 | KServe LLMInferenceService×WVA：按 KV cache 利用率、队列深度、请求饱和度算副本数，发布 `wva_desired_replicas`，HPA（经 Prometheus Adapter）/KEDA 直通执行（[llmisvc-autoscaling](https://kserve.github.io/website/docs/model-serving/generative-inference/llmisvc/autoscaling/llmisvc-autoscaling)） |

振荡控制的三板斧（各样板均有实现）：**稳定窗**（K8s 缩容默认 stabilization 300s，窗口内取最高建议；HPA 控制器还有 5min downscale-stabilization）、**冷却期**（KEDA cooldownPeriod）、**变化率限制**（K8s behavior 策略 Percent/Pods 每 15s）。指标出错时的方向不对称是通用设计：K8s 在某指标出错时**跳过缩容、允许扩容**（保守放大而非保守缩小）。

## 冷启动与资源供给

- **冷启动构成**：新副本从调度到可服务 = 镜像拉取＋调度等待 → 权重加载（load-format 分派、分片/量化影响读取量；TP 每进程读全量权重使读取时间随 TP 规模增长，官方建议转分片 checkpoint 解耦，[conserving_memory.md](https://github.com/vllm-project/vllm/blob/b17039bc/docs/configuration/conserving_memory.md)）→ profiling/KV 容量计算 → warmup/图捕获 → ready（五阶段边界见[权重加载与引擎 ready](model-loading-and-readiness.md)）。**各阶段耗时无官方数值**，是每个部署的待测变量；readiness 探针/ready gate 决定流量何时进来（机制见[服务发布与恢复](release-and-recovery.md)）。
- **扩容 ready gate**：扩上去的副本必须等 ready 才计入可服务集合；vLLM 侧的对应机制是弹性 EP 扩缩容先 `wait_for_requests_to_drain`（默认 drain_timeout 300s）排空在途请求再切换拓扑，期间 HTTP 请求直接 503（[async_llm.py L801/L817-855](https://github.com/vllm-project/vllm/blob/b17039bccc17b94a2ea107272ad7bc93508708df/vllm/v1/engine/async_llm.py#L817-L855)）。
- **缩容 drain**：缩掉的副本先从路由/端点摘除、排空在途流式请求再退出（K8s 侧 preStop＋宽限期语义见[服务发布与恢复](release-and-recovery.md)）；KV/prefix cache 随进程消失，缩容即丢缓存——回升后 TTFT 会短暂变差，这是缩容的隐性成本。
- **scale-to-zero**：KServe KPA 置 `minReplicas: 0` 且无流量时缩零；production-stack KEDA 用 `minReplicaCount: 0`＋流量保活触发器；KEDA 路径另有 `idleReplicaCount` 允许低于 minReplicas（须小于 minReplicas）。适用条件：低峰流量可接受冷启动时延（权重加载全程）、且入口层能把冷启动期的请求排队或返回明确状态；**不适合** P99 严格且流量突增的模式。睡眠模式的变体：vLLM sleep/wakeup 让引擎驻留进程但释放资源（如 GPU 内存），唤醒仍需重载（production-stack [sleep-wakeup 教程](https://github.com/vllm-project/production-stack/blob/20a658044af0dea70e9e0136494bb9979cfd9fab/docs/source/use_cases/sleep-wakeup-mode.rst)）——省的是"进程重启/重初始化"那部分，不是权重加载。
- **资源不可得**：扩容请求可能因集群资源不足悬置（调度等待语义见[配额、排队与准入](../05-cluster-platform/admission-and-placement.md)）；容量规划必须包含"扩不上去"分支——入口层降级/排队/拒绝策略（见[请求路由与流控](routing-and-flow-control.md)）。
- **PD 双池联动**：PD 分离时 prefill 池与 decode 池分别触发、分别扩缩，且 KV 传输链路（connector 前提）必须与两侧拓扑同步；单侧扩容改变不了另一侧瓶颈。双池容量联动无通用公式，按[PD 分离](pd-disaggregation.md)的指标与失败链分别规划。
- **最小冗余**：SLO 严格的服务的 minReplicas ≥ 2（单副本故障期间仍可服务），缩容下限就是冗余下限，不由负载决定。

## 有限对照与判据

对固定部署，用三组对照标定扩缩容参数（判据口径同[路由对照](routing-and-flow-control.md)）：

1. **增压曲线**：从低到低调步进负载，记录每档的 SLO 达标率、waiting 深度、KV 利用率、goodput——得到触发阈值与"容量不足"的先导信号。
2. **阶跃响应**：稳态→突增（超当前容量），记录从触发到新副本 ready 且分流生效的全链路时延（触发延迟＋冷启动＋传播），校验冷启动窗口内入口层的排队/拒绝是否在预算内。
3. **收缩**：高负载→撤流，记录缩容稳定窗、缓存丢失后的 TTFT 回升幅度与恢复时间，校验 cooldown 与稳定窗是否造成振荡（ replicas 上下翻动即振荡证据）。

每轮同窗记录：错误分类（拒绝/超时/取消）、排队分位、副本数曲线、资源水位、质量抽查（固定输入集）；**容量不足判据**＝SLO 达标率跌破目标且已处 maxReplicas（资源不可得单独记录）；**振荡判据**＝观察窗内副本数变向次数超阈值。NVIDIA/AMD/Ascend 的资源供给差异（GPU/NPU 分配粒度、MIG/虚拟实例等）与模型加载时延按各自平台档案分列，不互相换算。

## 边界与未知

- WVA 控制器（llm-d/workload-variant-autoscaler）实现未取回，本文按 KServe 文档集成口径引用；KEDA ScaledObject 完整字段未核。
- vLLM sleep 模式在固定 commit 的实现细节（sleep level、唤醒语义）未核，仅引用教程口径。
- 冷启动各阶段耗时与容量数值：三平台均无可引用官方数值，一律待测；本文所有阈值（KEDA 5、WVA 无默认值等）为样板示例或配置项，不是推荐值。
- K8s 侧缩容 drain 与引擎侧排空 API 是两套机制，跨层组合（pod 删除信号→引擎排空）未实测。
- 未部署任何 autoscaler，未执行对照。

## 来源与验证记录

- [Kubernetes v1.32 HPA 文档](https://v1-32.docs.kubernetes.io/docs/tasks/run-application/horizontal-pod-autoscale/)：控制环参数、公式与容差、稳定窗、behavior 默认。
- [KServe 0.20 线](https://kserve.github.io/website/docs/model-serving/predictive-inference/autoscaling/kpa-autoscaler)（网站仓 pin 3f4067e）：KPA 语义、WVA 集成、idleReplicaCount。
- [vLLM Production Stack v0.1.9](https://github.com/vllm-project/production-stack/tree/vllm-stack-0.1.9)：KEDA 教程（waiting 深度触发）、router HPA 模板、sleep/wakeup 教程。
- [vLLM v0.14.0 固定快照](https://github.com/vllm-project/vllm/tree/b17039bccc17b94a2ea107272ad7bc93508708df)：弹性扩缩容排空实现、KV 容量日志口径、conserving_memory。
- [SRE Workbook Implementing SLOs](https://sre.google/workbook/implementing-slos/)：SLO 口径与误差预算背景。
- 逐条主张与证据定位见[第二十八批 T07-09 来源记录](../../docs/research/batch-28-t07-09-sources.md)。
- 当前验证范围：来源核对；未部署、未压测。
