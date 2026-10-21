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
| 引擎内弹性 EP（**已被复核轮修订取代**，现行主张）：scale_elastic_ep 先判同尺寸直接返回，否则轮询 dp_engines_running 排空（drain_timeout 默认 300s，超时抛 TimeoutError 应停止该次变更），再变更 DP core 数；扩缩容**标志为真时** ScalingMiddleware 对**新进入** HTTP 请求回 503、在途流不受影响（标志设置/清除方与异常恢复链 unknown） | 扩展 src.vllm.inference-v0-14 | async_llm.py L801-855；elastic_ep/middleware.py L28-49；core_client.py L1278-1358（Ray DP 后端约束、新 cores 创建与 ready 等待） | 该 commit；触发方（operator/控制器）不在引擎内 |
| sleep/wakeup（**已被复核轮修订取代**，现行主张）：睡眠引擎不处理请求并释放资源（教程口径，含示例日志——示例值不作本部署基线）；唤醒成本依 sleep level 与实现而异（固定 commit worker L109-155 对 level 1/2 有不同处理、wake 调 allocator——allocator 与完整恢复路径未核）；router 支持睡眠引擎服务发现 | src.vllm.production-stack-v0-1-9；扩展 src.vllm.inference-v0-14 | sleep-wakeup-mode.rst；vllm/v1/worker/gpu_worker.py L109-155 | 教程级＋worker 分支级；完整恢复路径与本部署基线 unknown |
| 冷启动构成：权重加载（load-format 分派，T07-01 已核）＋profiling/KV 容量计算＋warmup/图捕获到 ready；TP 每进程读全量权重使**读取 I/O 时间**随 TP 规模增长（转分片 checkpoint 解耦） | 既有 src.vllm.inference-v0-14；src.vllm.model-loader-v0-14；src.vllm.readiness-health-v0-14 | conserving_memory.md；T07-01 交付锚点 | 机制链；来源有示例性耗时描述但不作基线，各环境为待测变量（复核 C02 修订） |
| 容量口径（单副本并发=KV 容量/max_model_len 级别判据；日志 GPU KV cache size/Maximum concurrency）与 SLO/goodput 分母 | 既有 src.vllm.inference-v0-14；本库 latency-metrics | parallelism_scaling.md（T07-06 已核）；指标字典 | 口径框架；具体数值须实测 |

## unknown 清单

1. WVA 控制器（llm-d/workload-variant-autoscaler 仓）与 KEDA ScaledObject 的完整字段/默认值未取回；KServe 文档为集成口径。
2. vLLM sleep 模式：已核 worker 分支（level 1/2 不同处理、wake 调 allocator，gpu_worker L109-155）与教程示例；未核 allocator 恢复链与完整恢复路径；本部署三平台阶段耗时基线未取得。
3. 冷启动各阶段耗时：教程/KPA 文档有示例性描述与示例日志，但不构成可迁移基线；本部署基线未取得，正文按待测变量处理，不杜撰。
4. 缩容时 in-flight 请求的 drain 语义在 K8s 侧（preStop+宽限期，见 T07-10 证据）与引擎侧（排空 API）是两套机制，跨层组合行为未实测。
5. 未部署/未运行任何 autoscaler。

## 初审修订轮（2026-10-21，响应 batch-28-t07-09-codex-review.md 的 C01–C10；C11 已由 T07-08 修订轮的 registry 更正关闭）

- C01：扩容 ready gate 拆为两个机制——副本级 readiness/路由传播（控制面）与引擎内弹性 EP 拓扑重配置（wait_for_requests_to_drain 轮询空闲、300s 超时 TimeoutError 应停止该次变更；ScalingMiddleware 503 限新进入 HTTP 请求、在途流不受影响、标志设置方 unknown）；registry notes 同步（排空轮询/超时分支、503 边界）。
- C02：sleep 唤醒成本改按 sleep level 与实现区分（固定 commit worker 对不同 level 有不同处理），完整恢复路径未核、不预设"全量重载"或"只省进程重启"；"无任何官方数值"收窄为"未取得可用于本部署的三平台基线（教程示例不作基线）"。
- C03：minReplicas≥2 改标注为本库规划建议（故障模型/剩余容量/故障域条件），删除通用规则表述。
- C04：对照方案补记录表要素（负载身份、每档上限与时长、分母窗口、成本口径含资源占用时长）、预登记停止条件与恢复闭环（撤压、恢复配置、回基线窗口）。
- C05：判据拆分——SLO 违约记录（症状）、触顶告警（不直接判容量根因，列候选原因与资源不可得单记）、振荡判据仅限固定/已知负载且排除负载驱动。
- C06：触发器表补 token 工作量与加速器设备指标两行（标注本库机制归纳；三平台统一指标名/阈值 unknown）。
- C07：新增 KServe 模式分支段（KPA 仅 Knative；Standard/Raw 用 HPA/KEDA；WVA scaling/replicas 互斥、执行器二选一）；PD 段补"decode 与 prefill 必须同一种 actuator"约束（WVA 文档 Prefill Scaling 节）。
- C08：scale-to-zero 补"从零重新激活是未证前提"（零副本时引擎指标不可观测、重唤链路未核，缩零配置不构成完整方案）。
- C09：缩容缓存改为"被移除进程的本地 cache 不保留"，跨层缓存效果按实现核对，TTFT 退化为待验证风险；对照记录命中率与 TTFT 同窗变化不预设方向。
- C10：HPA 默认表述更正——300s 稳定窗与控制器 5min flag 为同一默认机制两视图不叠加；15s 为默认策略周期示例；容差/同步标注默认；requests 条件限定 utilization 计算。

## 复核第一轮修订·补充（2026-10-21，响应 batch-28-t07-09-codex-recheck.md 的 C01/C02/C06/C07 剩余与 N01）

- C01 剩余：来源记录 elastic EP 主张行改写为现行口径（同尺寸直接返回、轮询排空+300s 超时、标志为真时新进入 HTTP 503、在途流不受影响、触发方 unknown）并标注取代旧表述；补 core_client L1278-1358 锚点。
- C02 剩余：来源记录 sleep 行改写（已核 worker L109-155 分支＋教程示例；未核 allocator 恢复链与完整路径；示例值不作基线），unknown 第 2/3 条同步；冷启动主张行"无官方耗时数值"改为"有示例性描述但不作基线"；正文来源节补 worker 层取证范围。
- C06 剩余：token 行改三种统计对象（到达需求/在途排队/已处理速率——后者是处理结果非需求，含饱和盲区概念说明）＋聚合掩盖局部积压＋窗口长短滞后/振荡＋与队列和 SLO 同看。
- C07 剩余：新增四路径前置表（Knative/KPA、Standard+HPA（Metrics Server）、Standard/Raw+KEDA（ScaledObject，外部指标后端按类型）、LLMISvc+spec.scaling（WVA controller+CRD+Prometheus 两类指标；HPA actuator 另需 Adapter external metric、KEDA actuator 另需 KEDA+ConfigMap））；标明 spec.replicas 是另一选择。
- N01：正文"②是既有引擎进程内的拓扑变更"改为"同一逻辑服务 DP engine cores 的分布式拓扑重配置（固定实现要求 Ray DP 后端、创建新 cores 并等待 ready——core ready≠副本 readiness）"。
