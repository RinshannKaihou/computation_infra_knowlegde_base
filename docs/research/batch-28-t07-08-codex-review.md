# Batch 28 · T07-08 初审报告

## 会话元数据与结论

| 项目 | 记录 |
|---|---|
| 审阅角色 | 独立批次审阅者；本会话不承担该篇正文编写或问题修订 |
| 实际执行模型 / 档位 | `gpt-6.1-sol / xhigh` |
| 模型核验 | 读取本地当前会话 JSONL 的最新 `turn_context`：`model=gpt-6.1-sol`、`effort=xhigh`，与 `collaboration_mode.settings` 一致；未另启其他模型或审阅子代理 |
| 会话 ID | `01a15d45-7de8-7832-adca-79c92b7c7997` |
| 执行方式 | 本地 Codex CLI 会话直接只读审阅，随后新增本报告 |
| 工作目录 | `/Users/ywang2397/work/AI_reliability_knowledge_base` |
| 日期 / 时区 | 2026-10-21 / Asia/Shanghai |
| 审阅正文 | `knowledge/07-inference/routing-and-flow-control.md`，122 行 |
| 正文 SHA-256 | `bd9dcbb2619b949ab8d824ba2a388a3f0ec2e1f5125bc2d589380e7766425ef4` |
| 写入范围 | 仅新增 `docs/research/batch-28-t07-08-codex-review.md`；不修改正文、来源登记、导航、任务状态或其他文件 |

**初审结论：需修订并定向复核，暂不通过。** 共 11 项发现：P1 为 0 项，P2 为 10 项（C01–C10），P3 为 1 项（C11）。正文已形成 T07-08 所需结构，但请求身份、预算拒绝、亲和路由与重试语义存在证据边界问题。来源登记另有一处 Envoy 门控方向错误。所有发现本轮均为开放状态，报告交付不代表关闭。

优先级口径：P1 为足以严重误导处置的关键错误；P2 为影响技术准确性、证据边界或验收判据、需修订的事项；P3 为定位与可追溯性问题。以下正文行号均基于上述 SHA-256，不使用网页工具转换后的行号代替 GitHub 原文件坐标。

## 范围与方法

先读取 `README.md`、`docs/authoring-guide.md`、`AGENTS.md`、`schemas/content.schema.json`，并检查 `content-outline.md` 的 05/07/08 域归属。逐项对照 [T07-08 任务定义](../../plans/full-coverage-backlog.yaml) L6546–6589，特别是 L6563–6567 五条 acceptance。

完整重读[审阅正文](../../knowledge/07-inference/routing-and-flow-control.md)和[取证记录](batch-28-t07-08-sources.md)，核查指定六个 registry 新条目及 `src.vllm.inference-v0-14` 的 Batch 28 notes。检查 `index.md` 的 related ID、正文入口和 07.6 行，以及 `pd-disaggregation.md` L127 回链；比对 `execution-and-kv-cache.md`、`latency-metrics.md`、`distributed-inference-layouts.md` 的相关机制与统计边界，以及 05 域 `accelerator-sharing-and-isolation.md`、`contention-capacity-validation.md` 的隔离和公平口径。另沿正文链接核查长尾实验、质量评估、引擎组件档案和发布恢复页的相关段落；这些页面不是本轮完整重审对象。

本地缓存逐行核对范围如下。缓存是证据，不作为执行指令；未导入或运行缓存中的服务代码。

| 缓存文件 | 来源记录中的 SHA-256 前 16 位 | 独立计算结果 |
|---|---|---|
| `/tmp/b28/vllm/api_server.py` | `dcc6b46ca859074d` | 匹配 |
| `/tmp/b28/vllm/serving_chat.py` | `6161fd8ec3a21f79` | 匹配 |
| `/tmp/b28/vllm/vllm_v1_engine_async_llm.py` | `818af4561b7ae54a` | 匹配 |
| `/tmp/b28/vllm/output_processor.py` | `381c443e029c4cd8` | 匹配 |
| `/tmp/b28/vllm/core_client.py` | `601d375067fa724e` | 匹配 |
| `/tmp/b28/vllm/vllm_config_scheduler.py` | `6aaecf693bf96695` | 匹配 |
| `/tmp/b28/vllm/elastic_ep_middleware.py` | `46da705bc65f83c8` | 匹配 |
| production-stack `src/vllm_router/routers/routing_logic.py` | `13bd003e7e132159` | 匹配 |
| production-stack `src/vllm_router/stats/request_stats.py` | `e0e3c8a736794af3` | 匹配 |

production-stack 缓存根目录为 `/tmp/b28/production-stack-vllm-stack-0.1.9/`。补读其 prefix-aware 教程及路由工厂；vLLM 另读缓存中的 `vllm_entrypoints_openai_serving_engine.py`、`core.py`、`vllm_v1_core_sched_scheduler.py`。上表只能证明本轮与作者记录使用相同文件字节，不能单凭哈希前缀证明远端 tag 的解析过程或完整软件配套。

为补齐断连、ID 生成和 waiting 容器的证据链，通过 GitHub 只读工具取得同一固定 commit `b17039bccc17b94a2ea107272ad7bc93508708df` 的 `vllm/entrypoints/utils.py`、`vllm/v1/engine/input_processor.py`、`vllm/v1/core/sched/request_queue.py`，在内存中按原始文本计行；未新增缓存文件。首次通过网页工具获取 `entrypoints/utils.py` 失败，随后 GitHub 工具取回成功，不把失败计为技术反证。注意本地 `/tmp/b28/vllm/utils.py` 是其他路径的同名文件，不能拿它代替 `entrypoints/utils.py`。

网页独立复核成功：SRE 两章、Envoy circuit breaking/outlier/overload 架构页及 overload 配置页、Kubernetes v1.32 探针页。另核对 RFC 9110 §9.2.2 作为幂等判断依据。Envoy 本轮网页标题分别出现 `1.41.0-dev-476800` 和 `1.41.0-dev-ec0f57`，与作者登记的 `e05ba9` 后缀不同：本轮确认当前可见内容的语义，不声称重现作者历史页面快照，也不据此判作者历史观察错误。

## 已核实的主链与边界

| 对象 | 独立核对结论 |
|---|---|
| XRequestIdMiddleware | `api_server.py` L698–727 的回显/生成实现成立；L940–941 的启用门控被正文遗漏，见 C01 |
| 断连 → abort | `api_server.py` L488 挂 `with_cancellation`；补取的 `entrypoints/utils.py` L54–111 监听断连并取消 handler，返回 StreamingResponse 后交由响应对象监听；`async_llm.py` L445–453 在已有 collector 时 abort；L551–560 先清 OutputProcessor，再向 EngineCore 发送取消。此处是已核实现路径，未实测网络断连、代理转发或取消时延 |
| 外部/内部 ID 级联 | `output_processor.py` L393–456 支持外部 ID 对应多个内部请求、父请求取消子请求、ABORT 最终输出、LoRA 计数清理；L486–487 登记映射。逻辑成立，但 HTTP 响应头 ID 不能无条件视作引擎 ID，见 C01 |
| KV 与队列清理 | `core.py` L316–322 → scheduler L1452–1512：移除 waiting/running 请求，进入 `_free_request`；`delay_free_blocks` 为真时延后释放 KV。因此不能把前端 abort 返回当作全部资源即时回收的实测证据。PD 页 L119 已明确 P 端 480s 保留期不覆盖一切失败路径 |
| DPLBAsyncMPClient | `core_client.py` L1211–1235：未指定 `data_parallel_rank` 时使用 `waiting*4+running`，选后增加本地等待估计；TODO P2C 只是计划。L1256–1276 按 `reqs_in_flight` 将取消发回对应 core。正文公式与两层职责区分成立；显式指定 rank 的分支宜在修订时保留 |
| ScalingMiddleware | L34–49：仅 HTTP scope、且扩缩容状态为真时，所有经过该中间件的新 HTTP 请求返回 503。正文此处条件成立，不证明其他过载准入能力 |
| scheduler 预算/队列 | `config/scheduler.py` L50–62 是每轮 token/sequence 上限；scheduler L463–465 控制 running 准入，L1446–1450 加入 waiting；补取的 request_queue L75–83、L141–146、L201–206 为 deque/heap 队列，未设置长度上限。配置校验不能误写成入口运行时拒绝，见 C02 |
| production-stack 枚举 | L53–57 为 roundrobin/session/kvaware/prefixaware/disaggregated_prefill，五项枚举准确；QPS 是辅助分支，见 C03 |
| 请求统计 | `request_stats.py` L111–114 区分到达窗口与完成样本窗口，L145–164 更新到达计数，L256–261 以窗口计数除以窗口长度得到 QPS；统计字段存在不等于路由决策使用它 |

## 发现清单

### C01 · P2 · 将按开关启用的响应 ID 中间件写成无条件行为

- **受影响正文位置**：L54、L92；来源记录 L37，registry 的 vLLM Batch 28 notes。
- **证据**：固定缓存 `api_server.py` L940–941 只有在 `args.enable_request_id_headers` 为真时才挂载中间件；L720–723 仅在发出响应头时取请求头 ID 或另生成 UUID，不把新 UUID 写回请求。另核到 `serving_engine.py` L1472–1481 从输入头或 default 取基础 ID，`serving_chat.py` L338–340 添加 `chatcmpl-`；补取的 `input_processor.py` L433–444 保存 external ID 并追加随机后缀形成 internal ID。没有输入头时，响应中间件的 UUID 与引擎基础 ID 不是同一个生成动作。[中间件挂载条件](https://github.com/vllm-project/vllm/blob/b17039bccc17b94a2ea107272ad7bc93508708df/vllm/entrypoints/openai/api_server.py#L936-L944)。
- **建议修订**：将“HTTP 层对每个响应设”改为“启用该中间件时”，并区分客户端携带的 HTTP ID、响应生成的 ID、引擎 external/internal ID；可以补上已核的普通 chat 路径，其他入口完整映射继续 unknown。不要把外部 ID 映射一概解释为原始 HTTP 头值。
- **关闭条件**：正文与两处证据记录同步补启用条件；至少区分输入头存在/不存在两种路径，引用上述固定文件坐标，不再暗示所有响应都有可关联的同一 ID。

### C02 · P2 · 将配置初始化校验混作运行时请求拒绝

- **受影响正文位置**：L83；来源记录 L39，registry 的 vLLM Batch 28 notes。
- **证据**：正文写“输入超 `max_num_batched_tokens`（非 chunked prefill）直接拒绝”。实际 `config/scheduler.py` L214–247 在初始化中调用 `verify_max_model_len`，L249–261 对 `max_num_batched_tokens < max_model_len` 且未启用 chunked prefill 的配置抛 ValueError。这里不接收单个请求。运行中本轮剩余预算不足时，scheduler L574–580 是停止本轮准入；输入合法性又有单独的 model length 检查。字段定义 L50–57 本身不支持“运行时直接拒绝”这一表述。[配置校验](https://github.com/vllm-project/vllm/blob/b17039bccc17b94a2ea107272ad7bc93508708df/vllm/config/scheduler.py#L247-L267)。
- **建议修订**：明确分开配置有效性、每迭代调度预算、请求长度校验、入口过载拒绝四种机制；保留 waiting 无长度上限的限定事实。若要描述具体运行时拒绝，应另取实际入口校验及响应分支。
- **关闭条件**：正文和取证/registry 不再将此 ValueError 当作逐请求准入策略；补上初始化调用点与 running 准入坐标。

### C03 · P2 · QPS 辅助路由被写成同时读取 QPS 与平均延迟的独立策略

- **受影响正文位置**：L60、L65。
- **证据**：正文先把可见状态定义为决策时实际读取的信号，L65 却列 `QPS、avg latency`。`routing_logic.py` L62–84 只比较 `request_stat.qps`；无统计的 endpoint 直接返回。L226–228、L367–369 表明它用于 session/KV fallback；L53–57 的枚举及 L524–550 的工厂没有独立 QPS 选项。`RequestStats.avg_latency` 存在并不表示该路由使用它。[实际比较分支](https://github.com/vllm-project/production-stack/blob/20a658044af0dea70e9e0136494bb9979cfd9fab/src/vllm_router/routers/routing_logic.py#L62-L84)。
- **建议修订**：将该行标为“最小观测 QPS 辅助分支”，决策信号仅写到达窗口 QPS；把 avg latency 放在可观测但未参与此分支决策的说明中。明确 session 缺 ID/KV 回退何时调用，避免误以为可独立配置第六种算法。
- **关闭条件**：算法枚举、可见状态与 fallback 调用关系一致；引用覆盖 L62–84 及实际调用位置。

### C04 · P2 · 合并不同亲和实现，并将同实例路由提升为 KV 命中保证

- **受影响正文位置**：L67–68、L72、L110；来源记录 L34–35。
- **证据**：来源记录 L34 已限定 session 只保证路由到同实例，正文却写“KV 命中率高”；这还取决于相同可复用前缀、缓存启用、驱逐与隔离身份，既有 `execution-and-kv-cache.md` L99–108 有相应边界。`kvaware` 的实际查找/回退在 `routing_logic.py` L325–397，判据是 `matched_tokens < max(len(token_ids)-self.threshold, 0)` 时回退 session/QPS；2000 是该构造器参数默认值，不是通用最低命中数。正文所引 L236–275 只有初始化，未覆盖此决策。`prefixaware` 在 L400–474 使用 router 自己的 HashTrie 和历史插入，明确不考虑缓存驱逐，未查询 LMCache 控制器。合并行把它们写成相同可见状态/陈旧来源，漏掉真正的 prefix 历史失真风险。[KV 分支](https://github.com/vllm-project/production-stack/blob/20a658044af0dea70e9e0136494bb9979cfd9fab/src/vllm_router/routers/routing_logic.py#L325-L397)、[prefix 分支](https://github.com/vllm-project/production-stack/blob/20a658044af0dea70e9e0136494bb9979cfd9fab/src/vllm_router/routers/routing_logic.py#L400-L474)。
- **建议修订**：拆分 session、kvaware、prefixaware，分别列实际状态、fallback、热点/公平代价；写明 prefixaware 的无驱逐假设。把“命中率高”“最大化”等效果收缩为可能收益或算法意图，并注明没有本轮比较基准；精确解释 KV threshold，补到决策行锚点。
- **关闭条件**：三种亲和的状态来源和失真风险不再混用；没有无条件命中收益；正文、来源记录与 unknown 清单保持一致。

### C05 · P2 · 以资源无泄漏替代幂等与重试安全的定义

- **受影响正文位置**：L93，并影响 L92–94 的重试责任解释。
- **证据**：正文把“重试安全”定义为服务端清理正确。资源清理只能说明生命周期处理，不能证明同一逻辑请求被去重、只执行一次或具有相同预期效果；采样输出相同与否也不能单独定义幂等。固定 `output_processor.py` L400–424 允许同一 external ID 关联多个内部请求，补取的 `InputProcessor.assign_request_id` 又为每次请求生成随机内部后缀，均不是幂等键/结果账本证据。[RFC 9110 §9.2.2](https://www.rfc-editor.org/rfc/rfc9110.html#section-9.2.2)将幂等定义为重复调用的预期服务端效果，并给出非幂等请求自动重试的限制。
- **建议修订**：分开关联 ID、取消清理、输出确定性和应用幂等；将 dedup/exactly-once 支持明确为本轮未建立证据。入口重试策略应说明原请求可能已经执行、取消可能尚未完成，以及重复计算/返回结果的处理责任，不能仅以“清理正确”判安全。
- **关闭条件**：删除该替代定义；给出准确概念及有限证据边界，未核的幂等键与去重机制保留 unknown，不新增已支持承诺。

### C06 · P2 · 将所选流式接口的重试政策外推为跨版本机制保证

- **受影响正文位置**：L94。
- **证据**：首 token 已对用户可见后，代理不应静默拼接一次新的生成，这一设计方向合理；但该段进一步断言“只能生成新响应”“引擎无断点续传实现”“不依赖特定版本”。固定 `api_server.py` L488–516 证明的是所选 chat 路径返回 StreamingResponse，不足以证明任意版本、其他 endpoint 或带应用恢复协议的服务均不能续取。HTTP 流式传输本身也不是已核实的全引擎功能矩阵。RFC 9110 §9.2.2 同样不把“尚未收到响应”当作无条件自动重试授权。
- **建议修订**：改为“本轮所选普通 chat/completion 路径未建立可续传契约的证据；本库建议代理在响应已提交/内容已输出后不透明重试”。区分连接建立失败与请求已送达但未见响应；后者仍受 C05 的幂等及执行状态约束。其他恢复协议保持 unknown。
- **关闭条件**：删除跨版本无条件断言；将代理政策标为本库归纳，限定接口/快照，并明确首字节之前只是必要边界之一、不是充分的重试安全条件。

### C07 · P2 · 将 SRE 特定系统的数字示例写成可迁移原则

- **受影响正文位置**：L85–86；对应来源记录 L27–28、registry 两章 notes。
- **证据**：10% 来自 Google 的 per-client 重试实现；50% 来自较平稳流量下 thread-per-request 线程池队列的举例，同一段还区分突发场景。正文将两者分别称为“量级原则”“≤50% 原则”，没有保留适用前提；异步推理调度器也没有可直接替代该线程池分母的工作单元。[Handling Overload 的 Deciding to Retry](https://sre.google/sre-book/handling-overload/)、[Cascading Failures 的 Queue Management](https://sre.google/sre-book/addressing-cascading-failures/)。
- **建议修订**：明确为来源系统中的实例，不作为本库推理部署阈值；或删除数字，只保留有限预算/小队列的原则。若保留，完整注明 per-client、线程池和稳态条件，推理准入预算需另行预注册和验证。
- **关闭条件**：正文及取证登记不再把两个数字称作推理通用原则；数值、分母与来源适用条件能逐一对应。

### C08 · P2 · 背压方向表述自相矛盾，且把作者策略归为来源公共结论

- **受影响正文位置**：L88，并关联 L85。
- **证据**：“越靠近过载源的层越应先丢弃”与紧接的“入口 503/限流优于引擎内抢占重算”给出的层次方向不一致。[Cascading Failures 的 Preventing Server Overload](https://sre.google/sre-book/addressing-cascading-failures/)同时讨论前端/后端就地保护及上层限流，并未建立该二选一优先定理；[Handling Overload 的 Handling Overload Errors](https://sre.google/sre-book/handling-overload/)还区分局部与广泛过载的重试反应。将整句归为“两章公共结论”过强。
- **建议修订**：分开写“过载组件用本地证据自保”和“上游收到背压后减少发送/按预算处理”；入口尽早拒绝以减少浪费可以作为本库有条件建议，明确其观测滞后与局部保护的互补关系。重试反应须考虑错误类别、剩余预算和过载范围。
- **关闭条件**：删除矛盾方向和未获来源支持的统一排序；来源原意与本库归纳分别标识。

### C09 · P2 · 将分位数达标与请求级 SLO 达标率混为一项判据

- **受影响正文位置**：L103。
- **证据**：该行称“SLO 达标率（TTFT/TPOT/E2E 分位对目标）”。分位数与阈值比较得到窗口分布是否达标，不能直接得到满足全部 SLO 的请求比例；只看成功样本分位还会漏掉拒绝/超时。被引用的 `latency-metrics.md` L177–189 已要求逐成功请求按同一 SLO 集合判断，再除以窗口时长，并记录 attempted/failed/cancelled 等数量。05 域争用验证页 L131–143 也提醒完成率分母不能随成功样本变化。
- **建议修订**：将“窗口分位数 gate”“逐请求 SLO 达标率”“goodput”分列。预先声明达标率分母、失败/拒绝/超时/取消的归类、逐请求 AND/OR 条件及窗口；保留现有质量评估链接。到达率/实际发起率与并发按所引实验模板分别固定，避免以并发阶跃自动代表同等 offered load。
- **关闭条件**：三项指标可独立计算，同一记录能复算分母、达标请求数与 goodput；不把 percentile gate 命名为请求达标率。无需为关闭本项实际发起压测。

### C10 · P2 · Envoy 来源登记将弹出比例上限的门控方向写反

- **受影响正文位置**：L52、L70 的健康发现证据依赖；错误直接位于 `sources/registry.yaml` L6838（`src.envoy.outlier-detection-arch-latest-2026-10-21` notes）。
- **证据**：registry 写“超过 max_ejection_percent 才弹出”。本轮独立打开的官方页 Ejection algorithm 第 2 步说明已弹出数量受允许阈值约束，超过阈值时不再弹出，作用方向相反。正文没有直接复述这条比较式，因此本项属于配套来源登记错误，不能说成正文已有反向配置指令。[Envoy Ejection algorithm](https://www.envoyproxy.io/docs/envoy/latest/intro/arch_overview/upstream/outlier#ejection-algorithm)。
- **建议修订**：改为“最大弹出比例限制继续弹出；超过允许阈值时不再弹出”，保留 panic 例外。这里只按架构页修正方向，不补写尚未核对的边界取整或 API 默认值；修订时记录 latest 当前可见版本与历史观察的区别。
- **关闭条件**：registry 反向语句修正，并由同一审阅者对该精确页面定向复核；正文/来源记录没有再引入相反语义。

### C11 · P3 · EngineDeadError 锚点和 Batch 28 取证路径无法准确定位证据

- **受影响正文位置**：L95、L117、L121；来源记录 L38；registry 的 vLLM Batch 28 notes（L536）。
- **证据**：本地哈希匹配的 `async_llm.py` 中，EngineDeadError 分支在 L455–459；正文引用的 L460–463 已进入 ValueError 校验分支。registry notes 还将 Batch 28 文件哈希指向不存在的 `docs/research/batch-28-tasks-sources.md`；本轮实际报告分散在各 `batch-28-t07-XX-sources.md`。正文 L121 自己的 T07-08 链接是有效的，不能因此把整条引用链都判失效。
- **建议修订**：EngineDeadError 统一锚到 L455–459；将不存在的聚合取证路径替换为真实的分任务记录，或清楚说明各文件哈希实际登记位置。C02、C04 所需语义补证分别按对应项处理。
- **关闭条件**：正文、取证表和 registry 的相关坐标/路径均能打开并定位所述分支或哈希；不得仅靠结构检查通过关闭。

## 五条 acceptance 的逐条判断

| 序号 / 任务要求 | 正文覆盖与边界 | 初审判断及待关闭项 |
|---|---|---|
| 1 · 四层职责及进入/排队/准入/执行/取消/完成 | L45–56 已区分入口、scheduler、P/D、健康发现，并有状态序列；没有把入口 LB 与 DP 内部分配当作同一控制面 | **主要结构满足，表述及配套证据待修**：C01、C10、C11；资源清理仅认已核路径 |
| 2 · 可见/陈旧状态、热点、cache 与多租户公平代价 | L58–72 有比较表，L112 将租户准入配额保持 unknown，没有宣称平台调度提供请求级公平 | **部分满足**：C03、C04；QPS 决策信号和三类亲和的真实状态需纠正 |
| 3 · 并发/token/队列预算、deadline、优先级、背压、拒绝/取消/重试责任，无无据通用参数 | L74–88 已列各层机制，waiting 与入口保护也有区分；SRE 与具体实现原则上分开引用 | **部分满足**：C02、C07、C08；配置校验阶段、数字示例条件和背压归纳尚不准确 |
| 4 · 请求 ID、幂等、流式重试、断连/取消释放 | L90–95 覆盖全部题项，取消级联主链已从源码核实；未声称本仓库实测清理 | **部分满足**：C01、C05、C06、C11；幂等定义与跨版本流式断言需修 |
| 5 · 阶跃/突发/长短混合有限对照及 SLO/goodput/错误/质量，按部署区分平台 | L97–105 已有三类负载、至少两种算法、多个副本、固定环境/预热/时长与停止原则，质量评估有链接；没有虚构实测参数或合并三引擎结果 | **主要方案满足，判据待修**：C09；分位 gate、请求达标率与 goodput 必须分别定义 |

范围未发现需要扩写到 T07-09/10 的要求：扩缩容算法、发布回退和硬件 OOM 处置可继续由相邻任务承担。这里对预算、取消、健康摘除的交叉引用合理；不能因任务名含 07.8 就要求本篇重复整套故障恢复流程。

## 元数据、导航与 unknown 核查

- **元数据结构**：稳定 ID、标题、`type: concept`、主域 `inference`、`status: draft`、日期均符合 schema；七项 `source_refs` 和所有 related/evidence ID 均可解析。概念篇主动填写 verification/applicability 合理；`source_checked` 与未部署声明没有被写成 `reproduced`。本轮发现要求收缩或修订具体核对结论，不据此改成已完成审阅。
- **平台边界**：`generic/nvidia/amd` 可用于这里的概念与上游实现证据范围；本文没有提供 AMD 硬件实测或完整 production-stack 配套证明，不应据平台标签推导这些结论。Ascend 内容通过 PD 页转接、不同引擎分开记录，未直接把上游实现写成 Ascend 已支持。相关标签本轮不列为错误。
- **版本边界**：vLLM 正文源码 URL 固定完整 commit；production-stack tag 与正文固定 commit 一致记录，未借教程宣称与 vLLM v0.14.0 已配套运行。Envoy L109 已明确 latest 可变页，当前独立观察不能作为作者历史 e05ba9 快照。除 C06 的跨版本推断外，未发现把所有版本/平台一律判兼容的声明。
- **导航**：`index.md` L34/L55/L82 均指向新正文；PD L127 回链有效。正文到 execution、latency、PD 和 05 域两篇的 Markdown 相对链接目标正确，语义分工合理。`distributed-inference-layouts` 在 frontmatter related ID 中可解析，但正文没有单独的可点击链接；可在 L56 附近补充，作为导航改善，不单列阻断项。
- **unknown 与已知的关系**：uvicorn 自身背压、LMCache 控制器内部实现、未测路由收益与租户准入配额继续 unknown 合理。C04 的命中收益措辞与现有机制级/未基准声明不一致；C06 的跨版本保证超出所选证据。C01 中 HTTP 到引擎映射不能以“尚未文档化”掩盖已有代码可见的条件分支。正文所称 PD 480s 仅可沿 PD 页限定为所选 connector 的 P 端保留兜底，不能扩大成所有取消资源回收上限。
- **来源许可**：新增项区分 SRE 未明确再分发许可与 Envoy/production-stack 仓库许可范围，本篇以链接和摘要为主，未发现借仓库许可统一授权所有材料的表述；本轮未做完整许可法律审查。
- **计划状态**：T07-08 当前仍为 `planned / needs_source_preparation`，`source_revision: null`。这是计划账本尚未更新的状态，不能从正文存在或本报告交付自动升级为 done；本轮按授权不修改它，也不将其混同为技术内容发现。

## 本轮校验与验证声明

执行 `make check`，结果为 **PASS: 117 content entries; 553 sources**；报告落盘后再次执行以检查报告内本地链接。结构检查只验证元数据、引用和本地文件链接，不验证上述技术语义、远程页面或硬件兼容性。未修改 `src/kb/`，未运行 `make test`。本轮只新增审阅报告、未修改知识正文或来源；为遵守只写这一个文件的范围，未运行会写入 `build/` 的 `make build`。

**模型审阅不替代真实环境验证。本轮未运行任何服务或负载，未部署路由器、Envoy、vLLM、production-stack 或 Kubernetes 工作负载，未进行性能、故障注入、断连清理时延或输出质量实验。** 哈希计算、静态读取、网页核查与仓库结构检查不构成这些实验。

后续由编写者按 C01–C11 修订，再提交变更后的正文 SHA-256 与实际证据位置，由同一审阅者定向复核；关闭条件满足前不宣称 T07-08 或 Batch 28 审阅通过。本报告只覆盖 T07-08，不代表 T07-09/10/11 已审阅。
