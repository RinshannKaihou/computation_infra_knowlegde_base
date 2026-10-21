# 第二十八批 T07-09 来源记录

任务：T07-09（容量、扩缩容与冷启动决策；**new** `knowledge/07-inference/capacity-and-autoscaling.md`，主题 07.6/07.7）。取证轮次：主会话作者角色首轮（2026-10-21；前置 T07-01 done、T07-08 同批先行）。未部署/未压测。

版本线：Kubernetes v1.32 静态快照；KServe 网站仓 main@`3f4067e`（0.20 线）；vLLM v0.14.0＝`b17039bc`；production-stack tag `vllm-stack-0.1.9`（`20a65804`）。

## 本轮取回清单

| 文件/页面 | 定位 |
|---|---|
| K8s v1.32 HPA 任务页 | https://v1-32.docs.kubernetes.io/docs/tasks/run-application/horizontal-pod-autoscale/ |
| KServe kpa-autoscaler.md（424 行，sha b8f04c9dad91aa14） | kserve/website@3f4067e |
| KServe llmisvc-autoscaling.md（394 行，sha 880fb8a6c1e57c91） | 同上 |
| vLLM v1/engine/async_llm.py（sha 818af4561b7ae54a） | b17039bc |
| production-stack autoscaling-keda.rst（sha 391c98658ab19d2c）、helm/values.yaml（d879b85b83e9d1b0）、helm/templates/hpa-router.yaml（d29be85957dfb192）、sleep-wakeup-mode.rst（d62f16d2ac62184d） | 20a65804 |

## 主张—来源定位表

| 主张 | 登记 ID | 精确位置 | 支持范围 / 未覆盖 |
|---|---|---|---|
| HPA 控制环 15s 同步；公式 ceil(current×metric/desired)、容差 0.1；指标类型（资源/容器资源 v1.30 稳定/自定义/外部/多指标取最大）；缺指标 pod 缩容按 100% 计；指标出错跳过缩容允许扩容；initial-readiness-delay 30s、cpu-initialization-period 5min、downscale-stabilization 5min（窗口取最高建议）；behavior 策略与默认（缩容 300s 稳定窗） | src.kubernetes.hpa-v1-32 | v1.32 静态快照任务页 | K8s 通用机制；推理特有指标须 custom/external metrics 另接 |
| KServe KPA：scaleMetric 默认 concurrency（concurrency/rps/cpu/memory）；target 软限 vs containerConcurrency 硬限；minReplicas 默认 1、置 0 可缩零；60s 稳定窗、2x 目标并发进 6s panic 窗 | src.kserve.autoscaling-v0-20-3f4067e | kpa-autoscaler.md | Knative/serverless 模式边界 |
| LLMInferenceService×WVA：按 KV cache 利用率/队列深度/请求饱和度等推理特有指标算副本数，发布 wva_desired_replicas，HPA（Prometheus Adapter）或 KEDA 直通执行（target=1）；spec.scaling 与 spec.replicas 互斥；KEDA 路径 idleReplicaCount 可低于 minReplicas | src.kserve.autoscaling-v0-20-3f4067e | llmisvc-autoscaling.md L11-13/L35-93/L224/L271 | 控制器实现（llm-d/workload-variant-autoscaler）未取回，按文档口径 |
| production-stack 引擎侧 KEDA 官方教程：vllm:num_requests_waiting 触发、threshold 5、pollingInterval 15s、cooldownPeriod 360s、min/max 1-3；scale-to-zero 置 minReplicaCount 0＋流量保活触发器；router 自身 HPA 为 CPU utilization 模板 | src.vllm.production-stack-v0-1-9 | autoscaling-keda.rst 步骤 1-7；helm/templates/hpa-router.yaml；values.yaml | 教程口径；阈值是示例非推荐值 |
| 引擎内弹性扩缩容（elastic EP）：先 wait_for_requests_to_drain(drain_timeout 默认 300s) 排空在途请求，再 engine_core.scale_elastic_ep(new_size)；扩缩容期间 HTTP 请求被 ScalingMiddleware 503 | 扩展 src.vllm.inference-v0-14 | async_llm.py L801/L817-855/L839；elastic_ep/middleware.py | 该 commit；触发方（operator/控制器）不在引擎内 |
| sleep/wakeup：睡眠引擎不处理请求并释放资源（如 GPU 内存），唤醒需重载；production-stack router 支持睡眠引擎的服务发现——缩容到零/睡眠与冷启动成本的官方实现口径 | src.vllm.production-stack-v0-1-9 | sleep-wakeup-mode.rst；（vLLM 侧 sleep 模式为 V1 特性） | 教程级；唤醒耗时数值未给 |
| 冷启动构成：权重加载（load-format 分派，T07-01 已核）＋profiling/KV 容量计算＋warmup/图捕获到 ready；TP 每进程读全量权重使读取时间随 TP 规模增长（转分片 checkpoint 解耦） | 既有 src.vllm.inference-v0-14；src.vllm.model-loader-v0-14；src.vllm.readiness-health-v0-14 | conserving_memory.md；T07-01 交付锚点 | 机制链；**无官方耗时数值**，各环境为待测变量 |
| 容量口径（单副本并发=KV 容量/max_model_len 级别判据；日志 GPU KV cache size/Maximum concurrency）与 SLO/goodput 分母 | 既有 src.vllm.inference-v0-14；本库 latency-metrics | parallelism_scaling.md（T07-06 已核）；指标字典 | 口径框架；具体数值须实测 |

## unknown 清单

1. WVA 控制器（llm-d/workload-variant-autoscaler 仓）与 KEDA ScaledObject 的完整字段/默认值未取回；KServe 文档为集成口径。
2. vLLM sleep 模式在 b17039bc 的实现细节（sleep level、唤醒重载语义）未核，仅 production-stack 教程口径。
3. 冷启动各阶段耗时：无任何官方数值（NVIDIA/AMD/Ascend 三平台均未给），正文按待测变量处理，不杜撰。
4. 缩容时 in-flight 请求的 drain 语义在 K8s 侧（preStop+宽限期，见 T07-10 证据）与引擎侧（排空 API）是两套机制，跨层组合行为未实测。
5. 未部署/未运行任何 autoscaler。
