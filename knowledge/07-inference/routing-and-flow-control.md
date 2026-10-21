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

请求在固定 vLLM v0.14.0 语义下的状态边界：**进入**（HTTP 请求带客户端请求 ID 到 API server，[XRequestIdMiddleware](https://github.com/vllm-project/vllm/blob/b17039bccc17b94a2ea107272ad7bc93508708df/vllm/entrypoints/openai/api_server.py#L698-L727) 回显或生成 `X-Request-Id`；引擎内生成内部 ID，外部→内部映射在 OutputProcessor 维护）→ **排队**（waiting 队列）→ **准入**（scheduler 组 batch 进入 running）→ **执行**（prefill/decode 迭代）→ **取消/完成**（finish_reason=STOP/ABORT 等；取消产生显式 ABORT 终止输出，[output_processor.py L393-456](https://github.com/vllm-project/vllm/blob/b17039bccc17b94a2ea107272ad7bc93508708df/vllm/v1/engine/output_processor.py#L393-L456)）。弹性 EP 扩缩容期间引擎对**所有**新 HTTP 请求回 503（[ScalingMiddleware](https://github.com/vllm-project/vllm/blob/b17039bccc17b94a2ea107272ad7bc93508708df/vllm/entrypoints/serve/elastic_ep/middleware.py#L28-L49)）——这是引擎自带的最小准入控制，但不构成入口级过载保护：上游 v0.14.0 的 waiting 队列本身不设长度上限。

另有一个容易误认的"负载均衡"：vLLM 单实例多 DP 引擎时的**引擎内**分配（DPLBAsyncMPClient 按 `score = waiting×4 + running` 最小选引擎，[core_client.py L1208-1245](https://github.com/vllm-project/vllm/blob/b17039bccc17b94a2ea107272ad7bc93508708df/vllm/v1/engine/core_client.py#L1208-L1245)，代码 TODO 注明大 DP 规模拟换 P2C）。它与入口路由是两层：前者在同一进程组内选引擎核，后者跨副本/机器。取消请求按 `reqs_in_flight` 映射路由回正确的引擎（[同文件 L1256-1275](https://github.com/vllm-project/vllm/blob/b17039bccc17b94a2ea107272ad7bc93508708df/vllm/v1/engine/core_client.py#L1256-L1275)）。

## 路由算法比较

production-stack v0.1.9 提供同一框架下的五种算法（[routing_logic.py L53-58](https://github.com/vllm-project/production-stack/blob/20a658044af0dea70e9e0136494bb9979cfd9fab/src/vllm_router/routers/routing_logic.py#L53-L58)），加上 Envoy 的代理层均衡与 vLLM 引擎内均衡，可按下表比较。"可见状态"指路由器做决策时实际读到的信号——它永远是**观测窗口内的近似**，这是所有负载感知算法的共同陈旧风险。

| 算法 | 可见状态 | 陈旧/热点风险 | cache 亲和 | 公平与多租户代价 | 样板证据 |
|---|---|---|---|---|---|
| 无状态轮询（round-robin） | 无 | 均摊请求**数**而非请求**成本**；长短请求混合时轻者闲重者堵 | 无（打散 prefix 命中） | 最简单；对等价请求近似公平 | production-stack `roundrobin`；vLLM toy proxy 的 `itertools.cycle`（[pd-disaggregation](pd-disaggregation.md)） |
| QPS/负载感知 | router 侧滑动窗 QPS、avg latency（每引擎） | 窗口内统计陈旧；对 token 长度不敏感（同 QPS 不同 token 量不可见） | 无 | 需要每副本统计通道 | production-stack `_qps_routing`（[L60-82](https://github.com/vllm-project/production-stack/blob/20a658044af0dea70e9e0136494bb9979cfd9fab/src/vllm_router/routers/routing_logic.py#L60-L82)；[request_stats.py](https://github.com/vllm-project/production-stack/blob/20a658044af0dea70e9e0136494bb9979cfd9fab/src/vllm_router/stats/request_stats.py)） |
| 引擎队列感知 | 引擎侧 waiting/running 计数 | 依赖指标上报周期；跨副本比较需同时钟 | 无 | 需要引擎 metrics 暴露 | vLLM DPLBAsyncMPClient（waiting×4+running） |
| session 亲和 | 请求头/体的 session_key | 副本消失→会话重落；哈希环增删节点扰动 | 会话级（同会话同副本，KV 命中率高） | 会话倾斜→热点；需配健康摘除 | production-stack `session`（一致性哈希 uhashring，[L107-120/L182-233](https://github.com/vllm-project/production-stack/blob/20a658044af0dea70e9e0136494bb9979cfd9fab/src/vllm_router/routers/routing_logic.py#L182-L233)） |
| prefix/KV 亲和 | 前缀→实例的命中查询 | 依赖 LMCache 控制器视图；阈值以下退化 | 显式最大化 KV 复用 | 基础设施较重；命中查询本身有时延 | production-stack `kvaware`（阈值默认 2000 token，[L236-275](https://github.com/vllm-project/production-stack/blob/20a658044af0dea70e9e0136494bb9979cfd9fab/src/vllm_router/routers/routing_logic.py#L236-L275)）/`prefixaware`（[教程](https://github.com/vllm-project/production-stack/blob/20a658044af0dea70e9e0136494bb9979cfd9fab/docs/source/use_cases/prefix-aware-routing.rst)） |
| PD 分配路由 | P/D 角色池与 KV 传输状态 | 单侧池失衡；connector 前提不满足即失败 | KV 传输替代亲和 | 双池容量需独立规划 | production-stack `disaggregated_prefill`；vLLM toy proxy（演示件）；详见[pd-disaggregation](pd-disaggregation.md) |
| 代理层均衡＋被动摘除 | 连接/请求/重试计数器、每主机错误率 | 计数器最终一致（worker 共享限值，瞬时可能超限）；统计剔除需最小样本量 | 无（L4/L7 通用） | 与具体推理语义无关，保护代理自身与上游 | Envoy circuit breaker/outlier detection |

比较的落点：**亲和类算法用"状态"换 KV 命中，负载类算法用"状态"换均衡，两者都会因状态陈旧而失准**；无状态轮询没有陈旧问题但浪费 KV 复用。选择时先明确优化对象（TTFT 均值、尾延迟、KV 命中率还是公平性），再用对照方案（见下）验证，不预设某种算法普遍最优。

## 预算、deadline、优先级与背压

各层可用的预算与背压机制（引用样板实现；**具体数值须按 SLO 与压测确定，来源不给通用参数**）：

| 机制 | 层 | 样板语义 | 边界 |
|---|---|---|---|
| 入口并发/ pending/重试上限 | 代理 | Envoy 簇级断路器五类（max_connections/max_pending_requests/max_requests/max_retries/max_concurrent_connection_pools），按 cluster＋priority 计数，溢出置 `x-envoy-overloaded`（[架构页](https://www.envoyproxy.io/docs/envoy/latest/intro/arch_overview/upstream/circuit_breaking)）；推荐 retry budgets 替代静态重试上限 | 文档未列默认值表；worker 共享限值最终一致 |
| 代理自我保护 | 代理 | Envoy overload manager：资源压力 [0,1]→触发器→动作；`stop_accepting_requests`＝新请求 503、`disable_http_keepalive`＝GOAWAY 排空（[配置页](https://www.envoyproxy.io/docs/envoy/latest/configuration/operations/overload_manager/overload_manager)）；示例两级映射 heap≥92%/≥95% | 与保护上游的断路器互补，不互相替代 |
| 请求关键度分级 | 服务/代理 | SRE：CRITICAL_PLUS…SHEDDABLE 分级，过载先丢低关键度（[Handling Overload](https://sre.google/sre-book/handling-overload/)） | 推理服务需先定义自己的分级，样板不代给 |
| 引擎并发/token 预算 | 引擎 | vLLM `max_num_seqs`（running 准入）与 `max_num_batched_tokens`（每迭代 token 预算）（[config/scheduler.py L50-57](https://github.com/vllm-project/vllm/blob/b17039bccc17b94a2ea107272ad7bc93508708df/vllm/config/scheduler.py#L50-L57)）；输入超 `max_num_batched_tokens`（非 chunked prefill）直接拒绝 | 上游 v0.14.0 waiting 队列无长度上限——入口排队上限须由代理/路由层提供 |
| deadline 与超时 | 全链 | SRE：每请求设 deadline、逐级检查剩余时间、deadline 与取消沿调用链传播（[Cascading Failures](https://sre.google/sre-book/addressing-cascading-failures/)） | 引擎侧对首 token/总长没有内置 deadline 语义（按 v0.14.0），须由入口层超时＋取消实现 |
| 重试责任 | 入口层为主 | SRE：每请求重试次数有限、重试比例预算（约 10% 量级原则）、随机指数退避、只在一层重试、过载返回明确"don't retry"信号 | 对推理请求重试还要叠加流式边界（见下） |
| 队列规模纪律 | 服务 | SRE：队列相对线程池保持小（≤50% 原则）或无队列、避免 FIFO 积压陈旧请求 | 推理的"工作单元"是流式请求，排队时长直接进 TTFT/尾延迟 SLO |

背压的层次原则：越靠近过载源的层越应先丢弃（入口 503/限流优于引擎内抢占重算）；被丢弃请求应收到可区分的状态（过载≠错误），使客户端退避而不是立即重试（SRE 两章的公共结论）。

## 请求身份、幂等与重试边界

- **请求 ID**：vLLM HTTP 层对每个响应设 `X-Request-Id`（请求头已有则回显，否则生成随机 uuid4.hex，[api_server.py L698-727](https://github.com/vllm-project/vllm/blob/b17039bccc17b94a2ea107272ad7bc93508708df/vllm/entrypoints/openai/api_server.py#L698-L727)）；引擎内另有内部请求 ID，外部→内部映射由 OutputProcessor 维护，按外部 ID 取消会级联其全部内部请求与并行采样子请求（[output_processor.py L393-456](https://github.com/vllm-project/vllm/blob/b17039bccc17b94a2ea107272ad7bc93508708df/vllm/v1/engine/output_processor.py#L393-L456)）。路由器侧的 ID 传递（如 production-stack/代理透传）是排障时串联三层日志的关键字段；HTTP ID 与引擎内部 ID 的完整映射关系未在上游文档化（unknown）。
- **幂等**：推理生成默认带采样随机性，同一请求重发不保证相同输出（采样参数控制）；"重试安全"指的是**服务端状态清理正确**（无泄漏），不是**输出可重放**。
- **流式已输出 token 后的重试边界**：一旦流式响应已向客户端输出 token，重试只能生成**新**响应，不能续传旧流。已输出的 token、客户端已消费的内容与服务端成本都不可回收；入口层对流式请求的重试应只发生在**首字节之前**（如连接失败），否则把重试决定权交回客户端。此边界为机制性结论（HTTP 流式语义＋引擎无断点续传实现），不依赖特定版本。
- **断连与取消的资源释放**：vLLM 固定快照下，客户端断连使流式生成器被取消，`asyncio.CancelledError`/`GeneratorExit` 触发自动 `abort`（[async_llm.py L448-458](https://github.com/vllm-project/vllm/blob/b17039bccc17b94a2ea107272ad7bc93508708df/vllm/v1/engine/async_llm.py#L448-L458)）；非流式路径捕获断连返回错误响应（[serving_chat.py L1365-1366](https://github.com/vllm-project/vllm/blob/b17039bccc17b94a2ea107272ad7bc93508708df/vllm/entrypoints/openai/serving_chat.py#L1365-L1366)）；取消清理包含 KV 块归还、LoRA 计数与在途集合移除；引擎死亡（EngineDeadError）分支**不**逐请求 abort——引擎整体关停（[同文件 L460-463](https://github.com/vllm-project/vllm/blob/b17039bccc17b94a2ea107272ad7bc93508708df/vllm/v1/engine/async_llm.py#L460-L463)）。PD 场景的取消清理另有 connector 侧超时（480s 保留期，见[pd-disaggregation](pd-disaggregation.md)）。

## 有限对照方案（负载阶跃/突发/长短混合）

目的：为给定部署选定路由算法与预算参数提供可复现依据。设计要点（与[长尾对照实验](ascend-inference-tail-latency-experiment.md)同构，判据口径见[延迟与吞吐指标字典](latency-metrics.md)）：

1. **固定身份**：引擎/插件/后端版本、模型与 dtype、副本数与布局、代理/路由器版本与配置、负载生成器与输入集、采样参数（评估质量时 greedy）。缺一项则结论不可比。
2. **矩阵**：负载形态至少三类——阶跃（低→高并发跳变）、突发（短时尖峰叠加在稳态上）、长短混合（固定比例长/短 prompt＋长短输出）。每类负载 × 候选路由算法（≥2，如轮询 vs session 亲和）× 副本数≥2。
3. **判据**（同窗采集）：SLO 达标率（TTFT/TPOT/E2E 分位对目标）、goodput（成功且达标的请求速率）、错误分类计数（拒绝/超时/取消/引擎错误分开）、输出质量（固定输入集上与基线的差异，方法见[输出质量对照评估](output-quality-evaluation.md)）、资源侧（每副本 waiting/running、KV 使用率、代理 overflow 计数器）。
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
