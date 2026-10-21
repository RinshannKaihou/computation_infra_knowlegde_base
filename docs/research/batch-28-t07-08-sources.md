# 第二十八批 T07-08 来源记录

任务：T07-08（请求路由、准入与流控；**new** `knowledge/07-inference/routing-and-flow-control.md`，主题 07.6/07.8）。取证轮次：主会话作者角色首轮（2026-10-21；前置 T07-02/T07-06 均 done）。取证方式：固定 commit 文件级下载（SHA-256）＋官方文档页实开核对；未部署任何路由器/代理。

版本线：vLLM v0.14.0＝`b17039bc`；vLLM Production Stack＝tag `vllm-stack-0.1.9`（`20a65804`）；Envoy 文档＝latest（页标 1.41.0-dev-e05ba9，2026-10-21 观察）；SRE Book 章节＝2026-10-21 观察；KServe 未用（归 T07-09/10）。

## 本轮取回清单（固定 commit 原文件；SHA-256 前 16 位）

| 文件 | SHA-256 前 16 位 |
|---|---|
| vLLM vllm/entrypoints/openai/api_server.py | dcc6b46ca859074d |
| vLLM vllm/entrypoints/openai/serving_chat.py | 6161fd8ec3a21f79 |
| vLLM vllm/v1/engine/async_llm.py | 818af4561b7ae54a |
| vLLM vllm/v1/engine/output_processor.py | 381c443e029c4cd8 |
| vLLM vllm/v1/engine/core_client.py | 601d375067fa724e |
| vLLM vllm/config/scheduler.py | 6aaecf693bf96695 |
| vLLM vllm/entrypoints/serve/elastic_ep/middleware.py | 46da705bc65f83c8 |
| production-stack src/vllm_router/routers/routing_logic.py | 13bd003e7e132159 |
| production-stack src/vllm_router/stats/request_stats.py | e0e3c8a736794af3 |

文档页（实开核对，登记见 registry）：SRE ch.21/22；Envoy circuit breaking / outlier detection / overload manager（架构概览＋配置参考两页）。

## 主张—来源定位表

| 主张 | 登记 ID | 精确位置 | 支持范围 / 未覆盖 |
|---|---|---|---|
| 容量以可用资源而非 QPS 度量；线程级 utilization 信号（executor load average）；按关键度分级丢弃（CRITICAL_PLUS…SHEDDABLE）；客户端自适应限流（requests/accepts，K=2 默认）；每请求 ≤3 次尝试＋每客户端 10% 重试预算、只在上层一层重试；过载返回"don't retry" | src.google.sre-handling-overload | 章节 2026-10-21 实开 | 原则层；无具体队列长度/目标利用率数值（页面未给） |
| 级联失效=正反馈放大；双峰延迟×长 deadline 吃线程池（5%×100s→5000 线程例）；恢复需降到远低于崩溃点；队列 ≤ 线程池 50% 或无队列、LIFO/CoDel；deadline 传播＋取消传播；重试随机指数退避＋服务级预算＋可重试区分 | src.google.sre-cascading-failures | 章节 2026-10-21 实开 | 原则层 |
| Envoy 五类簇级断路器（max_connections/max_pending_requests/max_requests/max_retries/max_concurrent_connection_pools）与各自 overflow 计数器；按 cluster+priority 计数、worker 共享最终一致；溢出置 x-envoy-overloaded；推荐 retry budgets | src.envoy.circuit-breaking-arch-latest-2026-10-21 | 架构概览页 | 参数名与机制；**页面无默认值表**（仅 1024 connections 示例） |
| Envoy 被动健康检查五类型与弹出算法（max_ejection_percent 门控、base_ejection_time×次数、panic 场景仍用被弹出主机）；主动健康检查通过会解除弹出（可关）；降级主机 x-envoy-degraded 不摘除只降优先 | src.envoy.outlier-detection-arch-latest-2026-10-21 | 架构概览页 | 机制；**无具体默认数值** |
| Envoy overload manager 保护代理自身：资源监视器（fixed_heap/cgroup_memory/cpu_utilization/global_downstream_max_connections）；threshold（saturated）与 scaled（scaling/saturation 线性插值）双语义；stop_accepting_requests=新请求 503、disable_http_keepalive=GOAWAY 排空等动作；示例 heap≥92%/≥95% 两级 | src.envoy.overload-manager-latest-2026-10-21 | 架构概览＋配置参考两页 | 机制与示例阈值 |
| production-stack 路由算法枚举：roundrobin/session/kvaware/prefixaware/disaggregated_prefill | src.vllm.production-stack-v0-1-9 | routing_logic.py L53-58 | 该 tag 实现 |
| QPS 最小路由基于 router 侧滑动窗统计（每引擎 QPS/avg_latency，窗口外引擎按无请求处理）——路由决策使用的是**观测到的**负载，存在陈旧窗 | src.vllm.production-stack-v0-1-9 | routing_logic.py L60-82；request_stats.py L35-51/L106-164/L256-261 | 实现语义；未实测陈旧度影响 |
| session 亲和=一致性哈希环（uhashring），session_key 从请求头或体取值；endpoint 变化触发增删节点 | src.vllm.production-stack-v0-1-9 | routing_logic.py L84-120/L107-115/L182-233 | 该实现；KV 亲和只到"路由到同实例"层面 |
| kvaware 路由依赖 LMCache 控制器查询最长前缀命中实例（kv_aware_threshold 默认 2000 token）；prefixaware 为同前缀尽量同实例（教程级） | src.vllm.production-stack-v0-1-9 | routing_logic.py L236-275；docs use_cases/prefix-aware-routing.rst | 结构级；LMCache 控制器实现未核 |
| 引擎内 DP 负载均衡与入口路由是两层：vLLM DPLBAsyncMPClient 按 score=waiting×4+running 选引擎（TODO：大 DP 规模换 P2C），取消按 reqs_in_flight 映射路由到正确引擎 | 扩展 src.vllm.inference-v0-14 | core_client.py L1180-1275（选引擎 L1208-1245） | 该 commit 实现 |
| 外部/内部请求 ID 两套：客户端请求 ID→引擎内部 ID 映射；按外部 ID 取消会级联其全部内部请求与并行采样子请求，产生 finish_reason=ABORT 终止输出；HTTP 层 X-Request-Id 中间件回显或生成 uuid4 | 扩展 src.vllm.inference-v0-14 | output_processor.py L393-456；api_server.py L698-727 | 语义与实现；HTTP ID→引擎 ID 的映射细节未逐行核 |
| 客户端断连→引擎取消：流式生成器被取消（asyncio.CancelledError/GeneratorExit）时自动 abort；非流式路径捕获 CancelledError 返回 "Client disconnected"；EngineDeadError 时不 abort（整引擎关停） | 扩展 src.vllm.inference-v0-14 | async_llm.py L448-463/L551-566；serving_chat.py L1365-1366 | 该 commit |
| 引擎准入边界：waiting 队列受 max_num_seqs/max_num_batched_tokens 间接限制（running 准入），超长输入在 max_num_batched_tokens<max_model_len 且非 chunked prefill 时拒绝（ValueError）；弹性 EP 扩缩容期间 ScalingMiddleware 对全部 HTTP 请求回 503 | 扩展 src.vllm.inference-v0-14 | config/scheduler.py L50-57/L251-266；elastic_ep/middleware.py L28-49 | 该 commit；上游 HTTP 层无队列长度准入上限（waiting 队列不设上限）——如实记录 |
| 引擎侧排队/运行观测指标（vllm:num_requests_waiting/running 等 Prometheus）可作路由与流控输入 | 既有 src.vllm.inference-v0-14 | metrics 文档/实现（Batch 04/09 已核） | 指标名与窗口 |

## unknown 清单

1. Envoy 三页均为 latest 可变页（1.41.0-dev 线），具体参数默认值需查 API reference（xDS proto 文档），本轮未取。
2. production-stack 的 session/kvaware/prefixaware 各算法的压测对比、hash 环虚拟节点数、统计窗口长度未核（实现常量未逐行取）。
3. KServe LLMISvc 路由（Gateway API HTTPRoute）只用于 T07-10 金丝雀证据；其请求级准入/背压能力未核。
4. vLLM 上游 HTTP 层（uvicorn/FastAPI）自身的并发/背压行为（如 uvicorn 的限流）未核；set_ulimit 仅解除 fd 上限。
5. 未部署/未压测任何路由器或引擎；全部为文档与源码结构级证据。
