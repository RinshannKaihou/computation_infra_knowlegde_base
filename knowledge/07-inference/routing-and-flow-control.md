---
id: inference.routing-and-flow-control
title: 请求路由、准入与流控
type: concept
domain: inference
status: draft
platforms: [generic, nvidia, amd]
source_refs:
  - src.vllm.inference-v0-14
  - src.vllm.production-stack-v0-1-9
  - src.envoy.circuit-breaking-arch-latest-2026-10-21
  - src.envoy.outlier-detection-arch-latest-2026-10-21
  - src.envoy.overload-manager-latest-2026-10-21
  - src.google.sre-handling-overload
  - src.google.sre-cascading-failures
updated_at: "2026-10-21"
summary: 把"请求往哪送、放不放进队列、超载时丢谁"拆成入口路由、引擎调度、P/D 分配与健康发现四层职责；比较无状态轮询、QPS/负载感知、session/prefix 亲和与 PD 路由的可见状态、陈旧风险、热点与公平代价；定义并发/token/队列预算、deadline、优先级与背压的分层责任，请求 ID/断连取消/流式已输出 token 的重试边界；给出负载阶跃/突发/长短混合的有限对照方案与 SLO/goodput/错误/质量判据。
related_ids:
  - inference.execution-and-kv-cache
  - inference.latency-metrics
  - inference.pd-disaggregation
  - inference.distributed-inference-layouts
  - inference.engine-backend-boundaries
  - cluster-platform.contention-capacity-validation
  - reliability.dimensions-and-failure-domains
verification:
  status: source_checked
  evidence_refs:
    - src.vllm.inference-v0-14
    - src.vllm.production-stack-v0-1-9
    - src.envoy.circuit-breaking-arch-latest-2026-10-21
    - src.google.sre-handling-overload
  notes: "已核对 vLLM v0.14.0 固定 commit 的请求取消/断连/引擎内 DP 负载均衡/扩缩容 503 中间件实现、production-stack v0.1.9 路由算法源码与 KEDA/HPA 模板、Envoy 1.41.0-dev 文档线（断路器/离群/过载管理三页）与 SRE Book 第 21/22 章。未部署任何路由器、代理或引擎。逐条主张与行号锚点见 docs/research/batch-28-t07-08-sources.md。"
applicability:
  environment_refs: []
  notes: "服务控制样板为 Envoy（latest 可变页，1.41.0-dev 线）与 vLLM Production Stack tag vllm-stack-0.1.9；引擎侧证据为 vLLM v0.14.0 上游（CUDA/ROCm 构建线）。昇腾侧 PD 路由证据见 pd-disaggregation；其他引擎/代理版本的字段与默认值须另行核对，本文不构成部署建议。"
---

# 请求路由、准入与流控

## 要回答的问题

推理服务在单副本之上必然引入三个流量决策点：请求**送到哪个副本**（路由）、**放不放进队列/放进哪个预算**（准入与流控）、**副本不健康或过载时怎么办**（摘除与背压）。这三个决策点分布在不同的层，混淆它们会把"引擎慢"误诊为"路由错"，或把"队列积压"误诊为"引擎故障"。本文按层拆开职责，给出可比较的路由算法与预算机制，并以固定版本样板（vLLM v0.14.0、production-stack v0.1.9、Envoy 1.41.0-dev 文档线、SRE Book 章节）锚定每个主张；通用原则与具体实现选项分别引用，不写无依据的通用参数。

## 四层职责与请求状态边界

| 层 | 决策对象 | 样板证据 | 不负责 |
|---|---|---|---|
| 入口负载均衡/路由（L7 proxy 或 router） | 请求→副本映射；入口级并发/队列/重试上限；被动/主动健康摘除 | Envoy circuit breaker/outlier detection/overload manager（[架构文档](https://www.envoyproxy.io/docs/envoy/latest/intro/arch_overview/upstream/circuit_breaking)）；production-stack router 五种路由算法（[routing_logic.py L53-58](https://github.com/vllm-project/production-stack/blob/20a658044af0dea70e9e0136494bb9979cfd9fab/src/vllm_router/routers/routing_logic.py#L53-L58)） | 模型内 batch 组成；KV 命中 |
| 引擎 batch scheduler | 已进入引擎的请求如何组 batch、何时抢占重算 | vLLM waiting/running 队列与 `max_num_seqs`/`max_num_batched_tokens`（[execution-and-kv-cache](execution-and-kv-cache.md)） | 跨副本选择；入口过载保护 |
| P/D 分配 | prefill/decode 角色分配与 KV 传输归属 | PD 分离的外部代理与 connector（[pd-disaggregation](pd-disaggregation.md)；上游 disagg_prefill.md 明确生产路由在引擎外） | 入口准入 |
| 健康发现 | 副本何时不再接收新流量、何时回归 | Envoy outlier detection 弹出/回归；K8s readiness 摘除（见[服务发布与恢复](release-and-recovery.md)） | 请求级错误处理 |

请求在固定 vLLM v0.14.0 语义下的状态边界：**进入**（HTTP 请求到达 API server；启用 `--enable-request-id-headers` 时挂载的 [XRequestIdMiddleware](https://github.com/vllm-project/vllm/blob/b17039bccc17b94a2ea107272ad7bc93508708df/vllm/entrypoints/openai/api_server.py#L698-L727) 在响应头回显请求自带的 `X-Request-Id` 或生成随机 uuid4——该开关默认不启用，[挂载点 L940-941](https://github.com/vllm-project/vllm/blob/b17039bccc17b94a2ea107272ad7bc93508708df/vllm/entrypoints/openai/api_server.py#L940-L941)；引擎侧另有外部/内部两级请求 ID，外部→内部映射在 OutputProcessor 维护）→ **排队**（waiting 队列）→ **准入**（scheduler 组 batch 进入 running）→ **执行**（prefill/decode 迭代）→ **取消/完成**（finish_reason=STOP/ABORT 等；取消产生显式 ABORT 终止输出，[output_processor.py L393-456](https://github.com/vllm-project/vllm/blob/b17039bccc17b94a2ea107272ad7bc93508708df/vllm/v1/engine/output_processor.py#L393-L456)）。弹性 EP 扩缩容期间引擎对**所有**新 HTTP 请求回 503（[ScalingMiddleware](https://github.com/vllm-project/vllm/blob/b17039bccc17b94a2ea107272ad7bc93508708df/vllm/entrypoints/serve/elastic_ep/middleware.py#L28-L49)）——这是引擎自带的最小准入控制，但不构成入口级过载保护：上游 v0.14.0 的 waiting 队列本身不设长度上限。

另有一个容易误认的"负载均衡"：vLLM 单实例多 DP 引擎时的**引擎内**分配（DPLBAsyncMPClient 按 `score = waiting×4 + running` 最小选引擎，[core_client.py L1208-1245](https://github.com/vllm-project/vllm/blob/b17039bccc17b94a2ea107272ad7bc93508708df/vllm/v1/engine/core_client.py#L1208-L1245)，代码 TODO 注明大 DP 规模拟换 P2C）。它与入口路由是两层：前者在同一进程组内选引擎核，后者跨副本/机器。取消请求按 `reqs_in_flight` 映射路由回正确的引擎（[同文件 L1256-1275](https://github.com/vllm-project/vllm/blob/b17039bccc17b94a2ea107272ad7bc93508708df/vllm/v1/engine/core_client.py#L1256-L1275)）。

## 路由算法比较

production-stack v0.1.9 提供同一框架下的五种算法（[routing_logic.py L53-58](https://github.com/vllm-project/production-stack/blob/20a658044af0dea70e9e0136494bb9979cfd9fab/src/vllm_router/routers/routing_logic.py#L53-L58)），加上 Envoy 的代理层均衡与 vLLM 引擎内均衡，可按下表比较。"可见状态"指路由器做决策时实际读到的信号——它永远是**观测窗口内的近似**，这是所有负载感知算法的共同陈旧风险。

| 算法 | 可见状态 | 陈旧/热点风险 | cache 亲和 | 公平与多租户代价 | 样板证据 |
|---|---|---|---|---|---|
| 无状态轮询（round-robin） | 无 | 均摊请求**数**而非请求**成本**；长短请求混合时轻者闲重者堵 | 无（打散 prefix 命中） | 最简单；对等价请求近似公平 | production-stack `roundrobin`；vLLM toy proxy 的 `itertools.cycle`（[pd-disaggregation](pd-disaggregation.md)） |
| QPS 辅助分支 | router 侧滑动窗到达 QPS（仅此一项参与该分支比较） | 窗口统计陈旧；对 token 长度不敏感（同 QPS 不同 token 量不可见） | 无 | 需要每副本统计通道；**不是独立可选的第六种算法**，用作 session/kvaware 缺键/未命中时的 fallback | production-stack `_qps_routing`（[L62-84](https://github.com/vllm-project/production-stack/blob/20a658044af0dea70e9e0136494bb9979cfd9fab/src/vllm_router/routers/routing_logic.py#L62-L84)；统计另含 avg_latency 等字段但该分支不读，[request_stats.py](https://github.com/vllm-project/production-stack/blob/20a658044af0dea70e9e0136494bb9979cfd9fab/src/vllm_router/stats/request_stats.py)） |
| 引擎队列感知 | 引擎侧 waiting/running 计数 | 依赖指标上报周期；跨副本比较需同时钟 | 无 | 需要引擎 metrics 暴露 | vLLM DPLBAsyncMPClient（waiting×4+running） |
| session 亲和 | 请求头/体的 session_key（一致性哈希 uhashring） | 副本消失→会话重落；哈希环增删节点扰动；会话倾斜→热点 | 会话级：同会话路由到同实例，**只是提高 KV 复用机会，不保证命中**（命中还取决于可复用前缀、缓存启用与驱逐，边界见[执行与 KV cache](execution-and-kv-cache.md)）；无 key 时走 QPS fallback | 需配健康摘除 | production-stack `session`（[L107-120/L182-233](https://github.com/vllm-project/production-stack/blob/20a658044af0dea70e9e0136494bb9979cfd9fab/src/vllm_router/routers/routing_logic.py#L182-L233)） |
| KV 命中查询（kvaware） | LMCache 控制器的最长前缀匹配结果 | 依赖控制器视图；判据为 `matched_tokens < max(len(token_ids) - threshold, 0)`——阈值（构造器默认 2000）参与的是**随 prompt 长度变化**的回退判据，不是固定最低命中数（如 prompt 6000、阈值 2000、命中 3000 仍回退）；回退分支仅对**有效非 None 结果对象**的空 layout_info 或比较式成立得到证实——代码在判 None 前先访问结果属性，结果对象缺失（None）或查询异常/超时的端到端行为未证（unknown） | 显式按前缀命中选实例 | 基础设施较重（LMCache）；命中查询有时延 | production-stack `kvaware`（决策分支 [L325-397](https://github.com/vllm-project/production-stack/blob/20a658044af0dea70e9e0136494bb9979cfd9fab/src/vllm_router/routers/routing_logic.py#L325-L397)，比较式在 [L358-373](https://github.com/vllm-project/production-stack/blob/20a658044af0dea70e9e0136494bb9979cfd9fab/src/vllm_router/routers/routing_logic.py#L358-L373)，构造器 [L242-267](https://github.com/vllm-project/production-stack/blob/20a658044af0dea70e9e0136494bb9979cfd9fab/src/vllm_router/routers/routing_logic.py#L242-L267)） |
| prefix 历史亲和（prefixaware） | router 自维护的前缀 HashTrie 历史（**不查询缓存实际状态、不考虑驱逐**） | 前缀历史失真是该算法特有陈旧风险（曾命中≠仍在缓存） | 以前缀历史近似 KV 位置 | 历史与真实缓存状态可偏离 | production-stack `prefixaware`（[L400-474](https://github.com/vllm-project/production-stack/blob/20a658044af0dea70e9e0136494bb9979cfd9fab/src/vllm_router/routers/routing_logic.py#L400-L474)；[教程](https://github.com/vllm-project/production-stack/blob/20a658044af0dea70e9e0136494bb9979cfd9fab/docs/source/use_cases/prefix-aware-routing.rst)） |
| PD 分配路由 | P/D 角色池与 KV 传输状态 | 单侧池失衡；connector 前提不满足即失败 | KV 传输替代亲和 | 双池容量需独立规划 | production-stack `disaggregated_prefill`；vLLM toy proxy（演示件）；详见[pd-disaggregation](pd-disaggregation.md) |
| 代理层均衡＋被动摘除 | 连接/请求/重试计数器、每主机错误率 | 计数器最终一致（worker 共享限值，瞬时可能超限）；统计剔除需最小样本量 | 无（L4/L7 通用） | 与具体推理语义无关，保护代理自身与上游 | Envoy circuit breaker/outlier detection |

比较的落点：**亲和类算法用"状态"换 KV 复用机会，负载类算法用"状态"换均衡，两者都会因状态陈旧而失准**（prefixaware 的历史失真、QPS 窗口陈旧、引擎指标上报周期是三种不同的陈旧来源）；无状态轮询没有陈旧问题但不利用 KV 复用。选择时先明确优化对象（TTFT 均值、尾延迟、KV 命中率还是公平性），再用对照方案（见下）验证，不预设某种算法普遍最优；本轮来源不含各算法的对比基准。

## 预算、deadline、优先级与背压

各层可用的预算与背压机制（引用样板实现；**具体数值须按 SLO 与压测确定，来源不给通用参数**）：

| 机制 | 层 | 样板语义 | 边界 |
|---|---|---|---|
| 入口并发/ pending/重试上限 | 代理 | Envoy 簇级断路器五类（max_connections/max_pending_requests/max_requests/max_retries/max_concurrent_connection_pools），按 cluster＋priority 计数，溢出置 `x-envoy-overloaded`（[架构页](https://www.envoyproxy.io/docs/envoy/latest/intro/arch_overview/upstream/circuit_breaking)）；推荐 retry budgets 替代静态重试上限 | 文档未列默认值表；worker 共享限值最终一致 |
| 代理自我保护 | 代理 | Envoy overload manager：资源压力 [0,1]→触发器→动作；`stop_accepting_requests`＝新请求 503、`disable_http_keepalive`＝GOAWAY 排空（[配置页](https://www.envoyproxy.io/docs/envoy/latest/configuration/operations/overload_manager/overload_manager)）；示例两级映射 heap≥92%/≥95% | 与保护上游的断路器互补，不互相替代 |
| 请求关键度分级 | 服务/代理 | SRE：CRITICAL_PLUS…SHEDDABLE 分级，过载先丢低关键度（[Handling Overload](https://sre.google/sre-book/handling-overload/)） | 推理服务需先定义自己的分级，样板不代给 |
| 引擎并发/token 预算 | 引擎 | vLLM `max_num_seqs`（running 准入）与 `max_num_batched_tokens`（每迭代 token 预算，[config/scheduler.py L50-57](https://github.com/vllm-project/vllm/blob/b17039bccc17b94a2ea107272ad7bc93508708df/vllm/config/scheduler.py#L50-L57)）。注意这是多个不同机制：`max_num_batched_tokens < max_model_len` 且未启用 chunked prefill 时，**启动配置校验**即抛 ValueError（初始化调用 [L247-261](https://github.com/vllm-project/vllm/blob/b17039bccc17b94a2ea107272ad7bc93508708df/vllm/config/scheduler.py#L247-L261)，不是逐请求拒绝）；运行期 token 预算耗尽或 running 到上限时本轮停止准入 waiting 请求（[scheduler.py L461-465](https://github.com/vllm-project/vllm/blob/b17039bccc17b94a2ea107272ad7bc93508708df/vllm/v1/core/sched/scheduler.py#L461-L465)）；请求所需 token 超过剩余预算时，**仅未启用 chunked prefill** 才在该分支跳出、可分块时按剩余预算调度部分 token（[scheduler.py L572-582](https://github.com/vllm-project/vllm/blob/b17039bccc17b94a2ea107272ad7bc93508708df/vllm/v1/core/sched/scheduler.py#L572-L582)） | 上游 v0.14.0 waiting 队列无长度上限——入口排队上限须由代理/路由层提供 |
| deadline 与超时 | 全链 | SRE：每请求设 deadline、逐级检查剩余时间、deadline 与取消沿调用链传播（[Cascading Failures](https://sre.google/sre-book/addressing-cascading-failures/)） | 引擎侧对首 token/总长没有内置 deadline 语义（按 v0.14.0），须由入口层超时＋取消实现 |
| 重试责任 | 入口层为主 | SRE：每请求重试次数有限、重试比例预算、随机指数退避、只在一层重试、过载返回明确"don't retry"信号（[Handling Overload](https://sre.google/sre-book/handling-overload/)） | 对推理请求重试还要叠加流式边界（见下） |
| 队列规模纪律 | 服务 | SRE：队列相对线程池保持小、或无队列、避免 FIFO 积压陈旧请求（[Cascading Failures 队列管理节](https://sre.google/sre-book/addressing-cascading-failures/)） | 推理的"工作单元"是流式请求，排队时长直接进 TTFT/尾延迟 SLO |

SRE 两章中的具体数字（如 per-client 10% 重试比例预算，以及出自较平稳流量下 thread-per-request 线程池举例的队列比例数字——同段紧接区分突发负载的不同处理）是**来源系统（Google 的实现）中的实例与经验值**，不是推理部署的通用阈值；本文档所在部署的准入与重试预算须按自身 SLO 预注册并经对照验证（见下）。

背压的两个方向要分开表述：其一，**过载组件用本地证据自我保护**（引擎内抢占/预算停止、代理断路与过载管理——来源各实现的既有机制）；其二，**上游收到可区分的过载信号后按预算减少发送**（SRE：过载返回明确状态使客户端退避）。"入口层尽早拒绝可减少无效排队与已完成即弃的工作"是本库的**有条件建议**（归纳自上述机制，非来源定理）：入口拒绝依赖其观测（有滞后），与组件本地保护互补而非替代，两者都应配置。

## 请求身份、幂等与重试边界

- **请求 ID**：vLLM 侧存在多级 ID，生成动作互相独立：① 启用 `--enable-request-id-headers` 时（默认不启用），响应中间件回显请求头 `X-Request-Id` 或生成随机 uuid4（[api_server.py L698-727，挂载 L940-941](https://github.com/vllm-project/vllm/blob/b17039bccc17b94a2ea107272ad7bc93508708df/vllm/entrypoints/openai/api_server.py#L940-L941)）；② 引擎侧基础 ID 取自输入头或请求字段默认值（缺省时另生成，[serving_engine.py L1472-1481](https://github.com/vllm-project/vllm/blob/b17039bccc17b94a2ea107272ad7bc93508708df/vllm/entrypoints/openai/serving_engine.py#L1472-L1481)），普通 chat 路径传入 `request.request_id` 作 default 再加 `chatcmpl-` 前缀（[serving_chat.py L338-357](https://github.com/vllm-project/vllm/blob/b17039bccc17b94a2ea107272ad7bc93508708df/vllm/entrypoints/openai/serving_chat.py#L338-L357)，多 prompt 另有子请求后缀）形成引擎外部 ID——**引擎外部 ID 不等于原始 HTTP 头值**（启用响应中间件且输入头为 H 时：响应头为 H、引擎外部 ID 为 `chatcmpl-H`；无头时响应中间件与服务入口是两个独立生成动作）；③ 内部请求 ID 在传入引擎的 ID 基础上追加随机后缀生成（[input_processor.py L433-444](https://github.com/vllm-project/vllm/blob/b17039bccc17b94a2ea107272ad7bc93508708df/vllm/v1/engine/input_processor.py#L433-L444)）。外部→内部映射由 OutputProcessor 维护，按外部 ID 取消会级联其全部内部请求与并行采样子请求（[output_processor.py L393-456](https://github.com/vllm-project/vllm/blob/b17039bccc17b94a2ea107272ad7bc93508708df/vllm/v1/engine/output_processor.py#L393-L456)）。响应头 ID 与引擎外部/内部 ID 的完整对应关系未在上游文档化（unknown）；排障时以客户端侧与各层日志的实际字段串联为准。
- **幂等**：按通用语义，幂等指重复同一请求时服务端预期效果不变（HTTP 语义下非幂等请求不应被自动重试）。固定 vLLM v0.14.0 **没有**幂等键或去重机制的证据：同一外部 ID 可关联多个内部请求，重复提交可产生独立的内部请求（未建立去重证据，因此**可能**重复执行——但 ID 分配本身不证明请求已开始或完成，排队等待与执行前取消均可能）；推理输出默认带采样随机性，重复请求的响应内容不保证相同。因此入口层对已送达请求的重试意味着**重复执行与重复计费的可能**，去重/仅一次执行语义保持 unknown；本库不建议把"取消清理正确"当作幂等成立的依据。
- **流式已输出 token 后的重试边界**（本轮所选普通 chat/completion 流式路径无断点续传契约的证据）：一旦响应已向客户端提交/输出 token，代理不能透明地重试拼接——重试只能生成**新**响应。区分两种失败：连接建立失败（可安全重试）与请求已送达但未见响应（受上条幂等边界约束，原请求可能已在执行或已完成）。**本库归纳建议**：入口对流式请求的自动重试只发生在响应提交之前，之后把重试决定权交回客户端；其他带应用层恢复协议的部署不在本轮证据内（unknown）。
- **断连与取消的资源释放**：vLLM 固定快照下，chat/completion 路由挂载取消包装（[api_server.py L488](https://github.com/vllm-project/vllm/blob/b17039bccc17b94a2ea107272ad7bc93508708df/vllm/entrypoints/openai/api_server.py#L488)），客户端断连使流式生成器被取消，`asyncio.CancelledError`/`GeneratorExit` 触发自动 `abort`（[async_llm.py L448-454](https://github.com/vllm-project/vllm/blob/b17039bccc17b94a2ea107272ad7bc93508708df/vllm/v1/engine/async_llm.py#L448-L454)）；非流式路径捕获断连返回错误响应（[serving_chat.py L1365-1366](https://github.com/vllm-project/vllm/blob/b17039bccc17b94a2ea107272ad7bc93508708df/vllm/entrypoints/openai/serving_chat.py#L1365-L1366)）；取消链清理 OutputProcessor 映射与 LoRA 计数并向 EngineCore 发送取消（KV 块按调度器的延迟释放安排归还——前端收到取消结果不等于全部资源已即时回收）；引擎死亡（EngineDeadError）分支**不**逐请求 abort——引擎整体关停（[async_llm.py L455-459](https://github.com/vllm-project/vllm/blob/b17039bccc17b94a2ea107272ad7bc93508708df/vllm/v1/engine/async_llm.py#L455-L459)）。PD 场景的取消清理另有 connector 侧超时（480s 保留期，见[pd-disaggregation](pd-disaggregation.md)，且该保留期不覆盖一切失败路径）。

## 有限对照方案（负载阶跃/突发/长短混合）

目的：为给定部署选定路由算法与预算参数提供可复现依据。设计要点（与[长尾对照实验](ascend-inference-tail-latency-experiment.md)同构，判据口径见[延迟与吞吐指标字典](latency-metrics.md)）：

1. **固定身份**：引擎/插件/后端版本、模型与 dtype、副本数与布局、代理/路由器版本与配置、负载生成器与输入集、采样参数（评估质量时 greedy）。缺一项则结论不可比。
2. **矩阵**：负载形态至少三类——阶跃（低→高并发跳变）、突发（短时尖峰叠加在稳态上）、长短混合（固定比例长/短 prompt＋长短输出）。每类负载 × 候选路由算法（≥2，如轮询 vs session 亲和）× 副本数≥2。
3. **判据**（同窗采集，三项指标分别计算、不互相替代，口径见[延迟与吞吐指标字典](latency-metrics.md)）：① **窗口分位数 gate**——TTFT/TPOT/E2E 的窗口分位值对目标的达标情况；② **逐请求 SLO 达标率**——每个成功请求按同一 SLO 集合逐项判定后计算达标请求比例，分母显式固定并分类记录 attempted/failed/cancelled/rejected（不能只用成功样本分位替代）；③ **goodput**——成功且达标的请求速率。另记录：错误分类计数（拒绝/超时/取消/引擎错误分开）、输出质量（固定输入集上与基线的差异，方法见[输出质量对照评估](output-quality-evaluation.md)）、资源侧（每副本 waiting/running、KV 使用率、代理 overflow 计数器）。
4. **停止与恢复**：每轮固定时长与预热；发现错误率异常或副本不健康即停，先保存证据再变更。
5. **结论边界**：只对所测矩阵负责；算法选择对"长请求占比""会话集中度"敏感，换负载画像须重测。引擎/部署差异（上游 vLLM vs vLLM Ascend vs MindIE）按各自版本分开记录，不合并结论。

## 边界与未知

- Envoy 样板为 latest 可变文档页（1.41.0-dev 线，2026-10-21 观察）；断路器/离群检测的参数默认值在 API reference（本轮未取），本文未引用具体默认数值。
- production-stack 的 session/kvaware/prefixaware 未做官方对比基准引用；表中比较为机制层归纳。
- vLLM 上游 HTTP 层（uvicorn）自身的并发限制行为未核；本文只声明引擎 waiting 队列无上限这一事实。
- 多租户公平：现有样板没有推理级的租户配额实现证据；租户隔离与争用的平台机制见[加速器共享与租户隔离](../05-cluster-platform/accelerator-sharing-and-isolation.md)与[多租户争用验证](../05-cluster-platform/contention-capacity-validation.md)，入口层的每租户准入预算为待建项（unknown）。
- 未部署、未压测；全部为固定版本源码/文档级证据。

## 来源与验证记录

- [vLLM v0.14.0 固定快照](https://github.com/vllm-project/vllm/tree/b17039bccc17b94a2ea107272ad7bc93508708df)：请求 ID 中间件、断连→abort 链、外部/内部 ID 级联取消、引擎内 DP 负载均衡、弹性扩缩容 503、调度器预算字段。
- [vLLM Production Stack v0.1.9](https://github.com/vllm-project/production-stack/tree/vllm-stack-0.1.9)：五种路由算法、QPS 滑动窗统计、一致性哈希 session 亲和。
- [Envoy 文档](https://www.envoyproxy.io/docs/envoy/latest/intro/arch_overview/upstream/circuit_breaking)（1.41.0-dev 线）：断路器、离群检测、overload manager。
- [SRE Book 第 21 章 Handling Overload](https://sre.google/sre-book/handling-overload/)、[第 22 章 Addressing Cascading Failures](https://sre.google/sre-book/addressing-cascading-failures/)：过载与级联失效原则（容量度量、关键度分级、重试预算、队列纪律、deadline 传播）。
- 逐条主张与证据定位见[第二十八批 T07-08 来源记录](../../docs/research/batch-28-t07-08-sources.md)。
- 当前验证范围：来源核对；未部署路由器/代理/引擎，未执行对照方案。
