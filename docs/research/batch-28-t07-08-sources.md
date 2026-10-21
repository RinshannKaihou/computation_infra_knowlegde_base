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
| 容量以可用资源而非 QPS 度量；线程级 utilization 信号（executor load average）；按关键度分级丢弃（CRITICAL_PLUS…SHEDDABLE）；客户端自适应限流（requests/accepts，K=2 默认）；每请求 ≤3 次尝试＋每客户端 10% 重试预算、只在上层一层重试；过载返回"don't retry" | src.google.sre-handling-overload | 章节 2026-10-21 实开 | **通用原则**（容量度量/分级丢弃/退避/一层重试）与**来源系统数值实例**（10% per-client、K=2）分列——数值是 Google 实现的实例，非推理通用阈值（复核 C07 修订） |
| 级联失效=正反馈放大；双峰延迟×长 deadline 吃线程池（5%×100s→5000 线程例）；恢复需降到远低于崩溃点；队列保持小或无队列（"≤ 线程池 50%"出自较平稳流量下 thread-per-request 线程池举例、同段紧接区分突发负载——来源系统实例，非通用阈值）、LIFO/CoDel；deadline 传播＋取消传播；重试随机指数退避＋服务级预算＋可重试区分 | src.google.sre-cascading-failures | 章节 2026-10-21 实开 | 通用原则与来源系统实例分列（复核 C07 修订） |
| Envoy 五类簇级断路器（max_connections/max_pending_requests/max_requests/max_retries/max_concurrent_connection_pools）与各自 overflow 计数器；按 cluster+priority 计数、worker 共享最终一致；溢出置 x-envoy-overloaded；推荐 retry budgets | src.envoy.circuit-breaking-arch-latest-2026-10-21 | 架构概览页 | 参数名与机制；**页面无默认值表**（仅 1024 connections 示例） |
| Envoy 被动健康检查五类型与弹出算法（已弹出比例未超 max_ejection_percent 上限才继续弹出、超过即不再弹出——初审 C10 更正初登反向表述；弹出时长=base_ejection_time×次数、panic 场景仍用被弹出主机）；主动健康检查通过会解除弹出（可关）；降级主机 x-envoy-degraded 不摘除只降优先 | src.envoy.outlier-detection-arch-latest-2026-10-21 | 架构概览页 Ejection algorithm 节 | 机制；**无具体默认数值** |
| Envoy overload manager 保护代理自身：资源监视器（fixed_heap/cgroup_memory/cpu_utilization/global_downstream_max_connections）；threshold（saturated）与 scaled（scaling/saturation 线性插值）双语义；stop_accepting_requests=新请求 503、disable_http_keepalive=GOAWAY 排空等动作；示例 heap≥92%/≥95% 两级 | src.envoy.overload-manager-latest-2026-10-21 | 架构概览＋配置参考两页 | 机制与示例阈值 |
| production-stack 路由算法枚举：roundrobin/session/kvaware/prefixaware/disaggregated_prefill | src.vllm.production-stack-v0-1-9 | routing_logic.py L53-58 | 该 tag 实现 |
| QPS 辅助分支仅比较每引擎滑动窗到达 QPS（request_stats 另有 avg_latency 等字段但该分支不读）；无统计引擎直接返回；该分支用作 session/kvaware 缺键/未命中的 fallback，不是独立可选算法 | src.vllm.production-stack-v0-1-9 | routing_logic.py L62-84（调用点 L226-228/L367-369）；request_stats.py L35-51/L106-164/L256-261 | 实现语义（初审 C03 修订）；未实测陈旧度影响 |
| session 亲和=一致性哈希环（uhashring），session_key 从请求头或体取值；endpoint 变化触发增删节点 | src.vllm.production-stack-v0-1-9 | routing_logic.py L84-120/L107-115/L182-233 | 该实现；KV 亲和只到"路由到同实例"层面 |
| kvaware 决策分支查询 LMCache 控制器最长前缀匹配，回退判据＝matched_tokens < max(len(token_ids) − threshold, 0)（构造器默认 threshold=2000，L242-267；比较式 L358-373）——随 prompt 长度变化的判据、非固定最低命中数（prompt 6000/阈值 2000/命中 3000 仍回退）；回退仅对有效非 None 结果对象证实（代码在判 None 前先访问结果属性 L347-352，结果对象缺失/查询异常超时的行为未证 unknown）；prefixaware 用 router 自维护 HashTrie 前缀历史，不查询缓存实际状态、不考虑驱逐 | src.vllm.production-stack-v0-1-9 | routing_logic.py L325-397（决策）、L358-373（比较式）、L242-267（构造器）、L400-474（prefixaware） | 决策分支级（初审 C04＋复核修订）；LMCache 控制器实现未核；session 亲和只保证同实例路由、不保证命中 |
| 引擎内 DP 负载均衡与入口路由是两层：vLLM DPLBAsyncMPClient 按 score=waiting×4+running 选引擎（TODO：大 DP 规模换 P2C），取消按 reqs_in_flight 映射路由到正确引擎 | 扩展 src.vllm.inference-v0-14 | core_client.py L1180-1275（选引擎 L1208-1245） | 该 commit 实现 |
| 请求 ID 加工链（复核 C01 补齐）：基础 ID 取自输入头或请求字段默认值/另生成（serving_engine.py L1472-1481）→普通 chat 路径加 chatcmpl- 前缀成引擎外部 ID（serving_chat.py L338-357，多 prompt 另有子请求后缀）→内部 ID 追加随机后缀（input_processor.py L433-444）；按外部 ID 取消级联全部内部请求与并行采样子请求、产生 ABORT 终止输出；X-Request-Id 响应中间件仅 --enable-request-id-headers 启用时挂载——**引擎外部 ID ≠ 原始 HTTP 头值**（chatcmpl-H vs H），未核 endpoint/代理透传的完整对应 unknown | 扩展 src.vllm.inference-v0-14 | serving_engine.py L1472-1481；serving_chat.py L338-357；input_processor.py L433-444；output_processor.py L393-456；api_server.py L698-727/L940-941 | 已核普通 chat 路径（初审 C01＋复核修订） |
| 客户端断连→引擎取消：chat/completion 路由挂 with_cancellation（api_server.py L488，取消包装监听断连）；流式生成器被取消（asyncio.CancelledError/GeneratorExit）时自动 abort（L448-454）；非流式路径捕获 CancelledError 返回 "Client disconnected"；EngineDeadError 分支不 abort——整引擎关停（L455-459，初审 C11 更正行号） | 扩展 src.vllm.inference-v0-14 | api_server.py L488；async_llm.py L448-454/L455-459/L551-566；serving_chat.py L1365-1366 | 该 commit |
| 引擎准入边界（复核 C02 细化）：max_num_seqs/max_num_batched_tokens 为每迭代调度预算；max_num_batched_tokens<max_model_len 且非 chunked prefill 时启动配置校验 ValueError（初始化调用 L247-261，非逐请求拒绝）；运行期 token 预算耗尽或 running 到上限→本轮停止准入 waiting（scheduler.py L461-465）；请求 token 超剩余预算时仅**未启用 chunked prefill** 才跳出、可分块时按剩余预算调度部分 token（L572-582）；弹性 EP 扩缩容标志为真时 ScalingMiddleware 对新进入 HTTP 请求回 503 | 扩展 src.vllm.inference-v0-14 | config/scheduler.py L50-57/L247-261；v1/core/sched/scheduler.py L461-465/L572-582；elastic_ep/middleware.py L28-49 | 该 commit；上游 HTTP 层无队列长度准入上限——如实记录 |
| 引擎侧排队/运行观测指标（vllm:num_requests_waiting/running 等 Prometheus）可作路由与流控输入 | 既有 src.vllm.inference-v0-14 | metrics 文档/实现（Batch 04/09 已核） | 指标名与窗口 |

## unknown 清单

1. Envoy 三页均为 latest 可变页（1.41.0-dev 线），具体参数默认值需查 API reference（xDS proto 文档），本轮未取。
2. production-stack 的 session/kvaware/prefixaware 各算法的压测对比、hash 环虚拟节点数、统计窗口长度未核（实现常量未逐行取）。
3. KServe LLMISvc 路由（Gateway API HTTPRoute）只用于 T07-10 金丝雀证据；其请求级准入/背压能力未核。
4. vLLM 上游 HTTP 层（uvicorn/FastAPI）自身的并发/背压行为（如 uvicorn 的限流）未核；set_ulimit 仅解除 fd 上限。
5. 未部署/未压测任何路由器或引擎；全部为文档与源码结构级证据。

## 初审修订轮（2026-10-21，响应 batch-28-t07-08-codex-review.md 的 C01–C11）

- C01：正文请求状态边界与"请求身份"节改为条件表述——XRequestIdMiddleware 仅在 `--enable-request-id-headers`（默认不启用）时挂载（挂载点 L940-941）；区分响应头 ID、引擎外部 ID（输入头/默认值）与内部 ID（随机后缀）三级生成动作；完整对应关系保持 unknown；registry notes 同步更正。
- C02：正文预算表拆分"启动配置校验 ValueError（L249-266）"与"运行期每迭代预算不足＝本轮停止准入"；删除"逐请求拒绝"表述；registry notes 同步更正。
- C03：路由表 QPS 行改为"QPS 辅助分支"——仅比较到达窗 QPS（avg_latency 可观测但该分支不读）、非独立算法、为 session/kvaware fallback；锚点更新 L62-84。
- C04：session/kvaware/prefixaware 三行拆分——session 只保证同实例（命中取决于前缀/缓存启用/驱逐，链接 execution-and-kv-cache 边界）；kvaware 决策分支 L325-397（阈值不满足回退）；prefixaware 为 router 自维护 HashTrie 历史且不考虑驱逐（历史失真为特有陈旧风险）；删除"命中率高/最大化"无条件表述；比较落点段补充"来源不含对比基准"。
- C05：幂等改为通用语义定义＋固定 vLLM 无幂等键/去重证据（同一外部 ID 多内部请求、每次新内部 ID 实际执行）；dedup/仅一次执行保持 unknown；删除"清理正确=重试安全"替代定义。
- C06：流式重试边界限定为"本轮所选 chat/completion 流式路径无断点续传契约证据"；区分连接建立失败与已送达未见响应；代理政策标注为本库归纳建议；其他恢复协议 unknown。
- C07：SRE 数字（10% 重试比例、队列≤50%）标注为来源系统实例（per-client 实现/稳态线程池举例），非推理通用阈值；本部署预算须预注册验证。
- C08：背压拆为"过载组件本地自保"与"上游按预算减少发送"两句；"入口尽早拒绝"标注为本库有条件建议（与本地保护互补）；删除"两章公共结论"归属。
- C09：判据拆为三项独立指标——窗口分位数 gate／逐请求 SLO 达标率（分母显式固定并分类）／goodput；链接 latency-metrics 的口径要求。
- C10：registry outlier 条目弹出方向更正（已弹出比例未超上限才继续弹出；初登写反）；来源记录同步。
- C11：EngineDeadError 分支锚点更正为 async_llm.py L455-459（正文两处）；registry Batch 28 notes 的取证路径改为分任务文件名；断连取消链补 api_server.py L488 with_cancellation；KV 延迟释放限定（前端 abort 返回≠资源即时回收）。

## 复核第一轮修订（2026-10-21，响应 batch-28-t07-08-codex-recheck.md 的 C01/C02/C04/C07 剩余条件与 N01）

- C01 剩余：补 ID 加工链——基础 ID（输入头/默认值/另生成，serving_engine L1472-1481）→chat 路径 `chatcmpl-` 前缀成引擎外部 ID（serving_chat L338-357，多 prompt 子后缀）→内部 ID 随机后缀；引擎外部 ID ≠ 原始 HTTP 头值；有头/无头两路径分列；未核 endpoint/代理透传 unknown。
- C02 剩余：运行期分支细化——预算耗尽/running 上限停止准入（scheduler L461-465）；请求 token 超剩余预算仅未启用 chunked prefill 才跳出、可分块时部分调度（L572-582）；初始化调用点 L247-261。
- C04 剩余：写出 kvaware 实际比较式 matched_tokens < max(len−threshold, 0)，说明阈值参与随 prompt 长度变化的判据（代入例：6000/2000/3000 仍回退），区分缺/空结果 fallback。
- C07 剩余：来源记录两行改为通用原则与来源系统数值实例分列；registry 级联条目队列数字补稳态/线程池条件与突发边界；正文数字段改为文字描述避免引号歧义。
- N01：幂等段改为"重复提交可产生独立内部请求、可能重复执行；ID 分配不证明已开始或完成（排队/执行前取消均可能）"。

## 复核第二轮修订（2026-10-21，响应 batch-28-t07-08-codex-recheck-2.md 的 C01 剩余与 N02）

- C01 剩余（首轮修订脚本因措辞不完全一致未生效，本轮按实际行文替换）：正文"请求身份"节落实 ID 加工链——基础 ID（输入头/请求字段 default/另生成，serving_engine L1472-1481）→chat 传 request.request_id 作 default＋`chatcmpl-` 前缀（serving_chat L338-357，多 prompt 子后缀）→内部 ID 随机后缀（input_processor L433-444）；"引擎外部 ID ≠ 原始 HTTP 头值"（H vs chatcmpl-H；无头时两独立生成动作）；未核 endpoint/代理透传 unknown。
- N02：正文与来源记录删除"缺结果/空结果另有 fallback"保证——回退仅对有效非 None 结果对象的空 layout_info 或比较式成立证实；代码在判 None 前先访问结果属性（L347-352），结果对象缺失/查询异常超时行为未证 unknown。
