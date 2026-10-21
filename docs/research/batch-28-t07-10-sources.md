# 第二十八批 T07-10 来源记录

任务：T07-10（服务版本发布、副本故障与恢复验证；**new** `knowledge/07-inference/release-and-recovery.md`，主题 07.6/07.7/07.8）。取证轮次：主会话作者角色首轮（2026-10-21；前置 T07-07 done、T07-08/T07-09 同批先行）。未部署/未演练。

版本线：Kubernetes v1.32 静态快照；KServe 网站仓 main@`3f4067e`（0.20 线）；vLLM v0.14.0＝`b17039bc`；Envoy 文档 latest（1.41.0-dev 线）。

## 本轮取回清单

| 文件/页面 | 定位 |
|---|---|
| K8s v1.32 Pod 生命周期页（终止流程段原文抽取，/tmp 快照 pod-lifecycle.html） | v1-32.docs.kubernetes.io/docs/concepts/workloads/pods/pod-lifecycle/ |
| K8s v1.32 探针概念页 | v1-32.docs.kubernetes.io/docs/concepts/configuration/liveness-readiness-startup-probes/ |
| KServe canary.md（21 行，sha fee7893a614ebab8）＋ llmisvc/canary-rollout.md（310 行，sha 89013ecf8dec6244） | kserve/website@3f4067e |
| vLLM api_server.py（sha dcc6b46ca859074d）、async_llm.py（818af4561b7ae54a）、core.py（a7a624e0ed151f00）、core_client.py（601d375067fa724e）、serving_chat.py（6161fd8ec3a21f79） | b17039bc |

## 主张—来源定位表

| 主张 | 登记 ID | 精确位置 | 支持范围 / 未覆盖 |
|---|---|---|---|
| Pod 终止时序（原文核对）：删除记录宽限期（默认 30s）→Terminating；kubelet 本地关闭（preStop 先跑、超时一次性 2s 延展；SIGTERM→各容器 PID1、无 sidecar 任意顺序）**与**控制面 EndpointSlice 摘除**并行**；terminating 端点保留但 ready 恒 false（1.26 前兼容）、LB 不再用于常规流量；宽限期到 SIGKILL；强制删除后 Pod 可能仍在节点运行 | src.kubernetes.pod-lifecycle-v1-32 | pod-lifecycle 终止流程段（原文抽取核对） | v1.32 语义 |
| 探针分工：liveness 失败→重启容器（死锁类）；readiness 失败→从 Service 端点摘除（全生命周期）；startup 成功前禁用 liveness/readiness；liveness 不等 readiness | src.kubernetes.probes-v1-32 | 概念页 | 概念分工；各机制默认值在任务页（未取，未引用具体默认值） |
| InferenceService 金丝雀：仅 serverless；canaryTrafficPercent 按百分比在新修订与 LatestRolledoutRevision 间分流；坏修订不分流；晋升/回退为修订字段语义 | src.kserve.rollout-v0-20-3f4067e | canary.md 全文 | Knative 修订模型 |
| LLMInferenceService 金丝雀：spec.router.route.group+weight 比例权重（对称成员、无主从）；控制器为组内每成员写 HTTPRoute 加权 backendRef（Gateway API）；**weight:0 暗部署有 CDS+RDS 同时更新引发瞬时连接失败风险，建议 weight:1 起步**；灰度门=P95 TTFT 对比 PromQL；晋升=stop 注解（pod 缩零释放 GPU、保留资源与权重供回退）；回退=降权重或去 stop；组成员须同模型名与 LoRA 集（否则 MemberDivergence） | src.kserve.rollout-v0-20-3f4067e | llmisvc/canary-rollout.md L16-58（机制）、L60-75（dark/live）、步骤 1-6 | v0.20 线文档口径；控制器实现未取 |
| Envoy 排空：overload manager 动作 disable_http_keepalive=H2/H3 GOAWAY＋H1 idle 计时；stop_accepting_requests=新请求 503；离群弹出与主动健康检查交互（通过即解除弹出） | src.envoy.overload-manager-latest-2026-10-21；src.envoy.outlier-detection-arch-latest-2026-10-21 | 配置参考页/架构页 | 代理层排空与摘除 |
| vLLM 关闭语义：SIGTERM 处理器在初始化期抛 KeyboardInterrupt；lifespan 退出时经 build_async_engine_client 上下文管理器调 async_llm.shutdown()；引擎死亡（EngineCore failed to start / encountered a fatal error）传播 ENGINE_CORE_DEAD、客户端收 EngineDeadError，此时单个 generate 不再 abort（整引擎关停） | 扩展 src.vllm.inference-v0-14 | api_server.py L117-143/L164-233（shutdown L232）/L1296-1300；core.py L927-943；core_client.py L425-428；async_llm.py L460-463 | 该 commit；**uvicorn 优雅关闭对在途流式请求的行为未核**（shutdown_task 等待逻辑在 L1351-1373，未逐行分析） |
| 请求取消→资源释放链：断连/取消→abort（外部/内部 ID 级联、子请求取消、finish_reason=ABORT 终止输出、LoRA 计数清理、_requests_drained 事件） | 扩展 src.vllm.inference-v0-14 | async_llm.py L448-458/L551-566；output_processor.py L393-456 | 该 commit；**不承诺 exactly-once 或断点续传**：流式已输出 token 不因重试恢复（正文按此边界写） |
| 版本制品身份（模型/tokenizer/config/量化）：模型身份固定清单与 load-format 不可互推（T07-01 交付）；量化身份＝格式–kernel–运行 dtype 三层分立（T07-04 交付） | 既有 src.vllm.model-loader-v0-14、src.vllm.tokenizer-registry-v0-14 等 | T07-01/T07-04 交付正文 | 复用 |
| PD 单侧失败：kv_load_failure_policy（默认 recompute）、connector 中止清理超时（480s）等失败链 | 既有 src.vllm.inference-v0-14（T07-07 登记） | pd-disaggregation.md 交付正文 | 复用 |

## unknown 清单

1. KServe LLMISvc canary 控制器（kserve 仓 CRD/controller）实现未取回；HTTPRoute/Gateway 实现后（如 Envoy Gateway）对权重变更的生效时延未核。
2. vLLM 收到 SIGTERM 后在途流式请求是否被排空（uvicorn graceful shutdown 与 engine shutdown 的先后）未逐行核——正文以"须用 preStop/宽限期显式排空"为方法边界，不声称引擎自动排空。
3. 副本故障后的 KV/prefix cache 身份：缓存内容随进程消失，重拉副本为冷 cache；跨副本 cache 恢复只有 PD connector/offload 路径（T07-07 证据），常规副本不继承——正文按此写，无实测。
4. 重试风暴定量：SRE 章节给的是通用原则与比例（10% 预算等），推理场景的数值须各环境压测。
5. 未执行任何发布/故障注入演练；全部为文档与源码级证据。
