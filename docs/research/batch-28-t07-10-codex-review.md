# Batch 28 · T07-10 初审报告

## 会话元数据与结论

| 项目 | 记录 |
|---|---|
| 审阅角色 | 独立批次审阅者；本会话未编写或修订被审正文 |
| 实际执行模型 / 档位 | `gpt-6.1-sol / xhigh` |
| 模型核验 | 读取当前本地会话 JSONL 的 `session_meta` 与全部 `turn_context`；执行模型/档位组合仅有 `gpt-6.1-sol / xhigh`，assistant 消息未检出 fallback 标记；没有另启模型或子代理 |
| 会话 ID | `01a15d55-154e-78a2-9501-47c240e15641` |
| 执行方式 | 本地 Codex CLI，`originator=codex_exec`、`source=exec`、CLI 0.163.0；直接读取仓库与缓存并新增本报告 |
| 日期 / 时区 | 2026-10-21 / Asia/Shanghai |
| 工作目录 | `/Users/ywang2397/work/AI_reliability_knowledge_base` |
| 审阅正文 | `knowledge/07-inference/release-and-recovery.md`，102 行 |
| 正文 SHA-256 | `9683aa24c09d33560d26615b86fa18bba3e7769efd46a2e980d08917e944a2a1` |
| 作者取证记录 SHA-256 | `4308f10c042e47ea54309e1fa1c74cd20c7143d6fe7edbd151bcda12fee20079` |
| 写入范围 | 仅新增 `docs/research/batch-28-t07-10-codex-review.md`；不修正文、来源记录、registry、导航或计划。`make build` 仅重建忽略的生成物 |

**初审结论：需修订并定向复核，暂不通过。** 共 11 项发现，全部开放：0 P1、9 P2（C01–C09）、2 P3（C10–C11）。三层健康、制品身份和验证流程已有主干；排空的执行闭环、关闭链、回退终态、PD 失败条件以及请求/缓存恢复边界仍需修订。

优先级沿用仓库口径：P1 为严重误导处置的关键错误；P2 为影响技术准确性、适用边界或验收完整性的必修项；P3 为措辞、定位与追溯问题。正文行号绑定上述 SHA-256；上游代码行号使用缓存原文件坐标。报告交付不等于问题关闭。

## 范围与方法

先读取 `README.md`、`docs/authoring-guide.md`、`AGENTS.md`、`schemas/content.schema.json`，再按 `content-outline.md` 核对 05/07 域分工。逐条对照 [T07-10 定义与 acceptance](../../plans/full-coverage-backlog.yaml) L6637–6659，完整重读[正文](../../knowledge/07-inference/release-and-recovery.md)、[取证记录](batch-28-t07-10-sources.md)、[07 域导航](../../knowledge/07-inference/index.md)和 [registry](../../sources/registry.yaml) 指定条目：

- `src.kubernetes.pod-lifecycle-v1-32`、`src.kubernetes.probes-v1-32`。
- `src.kserve.rollout-v0-20-3f4067e`。
- `src.envoy.overload-manager-latest-2026-10-21`、`src.envoy.outlier-detection-arch-latest-2026-10-21`。
- `src.google.sre-cascading-failures`、`src.vllm.inference-v0-14` 的 Batch 28 notes。

沿正文读取路由、容量/扩缩容、加载/ready、PD、输出质量、GPU OOM 和 05 域节点回收/平台变更/控制面恢复的有关段落；关联页仅用于边界与链接核对，不在本轮重新作完整初审。工作区存在其他任务的并行修订，路由和容量页按本轮实际读取版本使用；本报告不承接它们的发现关闭工作。

独立读取缓存并计算 SHA-256；没有导入或运行服务代码：

| 缓存文件 | 独立计算的 SHA-256 前 16 位 |
|---|---|
| `/tmp/b28/vllm/api_server.py` | `dcc6b46ca859074d` |
| `/tmp/b28/vllm/vllm_v1_engine_async_llm.py` | `818af4561b7ae54a` |
| `/tmp/b28/vllm/core.py` | `a7a624e0ed151f00` |
| `/tmp/b28/vllm/core_client.py` | `601d375067fa724e` |
| `/tmp/b28/vllm/output_processor.py` | `381c443e029c4cd8` |
| `/tmp/b28/vllm/serving_chat.py` | `6161fd8ec3a21f79` |
| KServe predictive `rollout-strategies/canary.md` | `fee7893a614ebab8` |
| KServe generative `llmisvc/canary-rollout.md` | `89013ecf8dec6244` |
| `/tmp/b28/pod-lifecycle.html` | `3b6cd176dbbf06cb` |

KServe 根目录为 `/tmp/b28/kserve-web/docs/model-serving/`，网站仓 pin 为 `3f4067ea87dd84194bddb1b563051c84306c7997`；vLLM pin 为 `b17039bccc17b94a2ea107272ad7bc93508708df`。以上代码/Markdown 哈希与作者记录或同批记录相符；Pod HTML 的完整哈希为 `3b6cd176dbbf06cb8a6d3cb6d385ec28f68ec5205683f79c3994064878adc173`，本轮另行计算，作者没有登记该 HTML 哈希。缓存一致性不单独证明远端 tag 解析或环境兼容。

为复核 PD 条件，补读 `/tmp/b27-fetch/` 中 `vl-kv-base.py`、`vl-nixl-connector.py`、`vl-mooncake-connector.py`、`vl-nixl_usage.md`、`vl-mooncake_usage.md`、`mi-faq.md`、`vl-disagg_prefill.md`；哈希前缀依次为 `00fc529df6dc944f`、`bcf8980a73c23945`、`dd7d60072bfd64ba`、`675eb4152d415140`、`d60a7cbfdd3e87be`、`3c4f5db3c425f401`、`e68ad65fee967a00`，均与 [T07-07 来源记录](batch-27-t07-07-sources.md)相符。另对照 Batch 28 缓存 scheduler 的 invalid-block 处理分支。

**网络核验限制**：尝试打开 K8s 探针/生命周期、Envoy overload 配置/架构及 outlier、SRE 级联失效/有效排障精确页面；网页工具返回 HTTP 429，随后只读 HTTP 抽查因 DNS 解析失败未取得页面。本轮没有独立重取探针、Envoy、SRE 原文；这些部分只能核对 registry 与作者记录的一致性，不能记作本轮网页已核。Pod 生命周期由给定 HTML 原文独立核对，KServe/vLLM 由固定缓存独立核对。未把网络失败判为作者技术错误，也未用搜索摘要代替正文。

## 重点核对结果

| 对象 | 核对结果 |
|---|---|
| Pod 终止时序 | HTML 的 “Pod termination flow” 支持：kubelet 本地关闭与控制面处理端点并行；已定义且宽限期非零的 preStop 先执行；钩子耗尽宽限期仍运行时请求一次 2s 延展；terminating 端点不立即从 EndpointSlice 删除，`ready:false` 用于兼容 1.26 之前客户端，排空时另有 `serving` 条件。正文这一主干没有写反。信号及排空执行边界见 C01。 |
| KServe 两类 API | InferenceService 的百分比字段与 serverless 限制，LLMInferenceService 的 group/比例权重、对称成员和每成员 HTTPRoute backendRef，均与缓存相符。stop 保留的是资源及声明权重，不是运行中的 GPU 权重或 KV 状态。回退完成条件见 C03；dark/live 与 MemberDivergence 的精确限定见 C10。 |
| vLLM 关闭与错误 | 初始化 SIGTERM handler 抛 KeyboardInterrupt、外层 engine context finally 调 shutdown、EngineDead 的运行期分支均有源码依据；lifespan 归属、启动失败与运行期死亡被混写，见 C02/C07。 |
| 不假设自动 drain | 正文 L55/L90 与来源记录 unknown 2 均显式不假设引擎自动排空；本轮没有发现正文偷偷承诺这一行为。该保留应继续存在，但不能替代显式 drain 的待实现条件，见 C01。 |
| exactly-once 与取消 | 标题和外部副作用段没有承诺 exactly-once；取消链只证明所核分支的中止/清理动作，不证明去重、服务端执行一次或客户端收到终态。正文的“唯一防线”和缓存绝对化仍需修，见 C05/C06。 |
| 元数据 | `procedure` 的必填字段齐全，`draft / source_checked`、空 `environment_refs` 和来源 ID 引用均通过结构检查；没有标为 `reproduced`。实际硬件、驱动、插件、容器、网关组合仍未建立环境档案，不能从 platforms 列表推出三平台兼容。 |
| 本地引用与导航 | 正文全部 13 个内联本地链接出现位置均可解析；8 个 related ID 均存在。路由、容量、加载、PD、质量、GPU OOM 的正文链接有效；05 域节点回收有正文链接，平台变更/控制面恢复仅有 related ID，见 C11。07 域 index 的 related ID、已有正文与 07.6/07.8 入口有效；07.7 经容量/延迟入口导航。 |

## 发现清单

### C01 · P2 · 排空仍是原则描述，缺少可检查的执行顺序和超时终态

- **位置**：正文 L48–55、L80–85；acceptance 2。
- **证据**：L55 用 preStop＋足够宽限期概括在途流排空，却没有定义谁停止新请求、怎样确认入口/网关收敛、如何处理既有连接上的新请求、怎样观察在途请求归零，以及排空超时后取消/失败的终态。EndpointSlice 的并行变化不是“preStop 开始前全入口已经摘除”的屏障；GOAWAY 是代理连接层动作，也不是所有应用请求完成的证明。[K8s v1.32 原文](https://v1-32.docs.kubernetes.io/docs/concepts/workloads/pods/pod-lifecycle/#pod-termination)还明确 preStop 消耗同一宽限期，且某些 runtime 尊重镜像 `STOPSIGNAL`，不能无条件把实际停止信号写成 SIGTERM。
- **建议修订**：增加待执行的 drain 子流程：记录目标与剩余容量→停止该副本新准入并观察实际路由收敛→维护已接纳流的完成/取消计数→在预登记期限内等待→超时按明确策略终止并记录不确定请求→核对进程与资源回收。把 preStop 的具体职责、信号配置和共用时间预算列为部署前提；未实现时明记缺失，不把“有钩子”当作排空成立。
- **关闭条件**：读者能区分停止新流量、连接关闭、请求终态和资源回收，并有各阶段证据、超时分支及完成判据；继续显式不假设引擎自动 drain。无需为关闭本项实际演练。

### C02 · P2 · lifespan 与外层 engine context 的关闭责任混写

- **位置**：正文 L37/L55/L90；来源记录 L25。
- **证据**：固定 `api_server.py` L117–143 的 FastAPI lifespan 只取消统计任务并删除 `app.state`；真正的 `async_llm.shutdown()` 在 engine client 上下文的 finally（L229–232）。`run_server_worker` 在外层 context 中调用 `serve_http`，退出 backend context 后才在 L1371–1373 await `shutdown_task`。这不能写成 lifespan 自身调用引擎 shutdown，也不能把已经看得见的外层代码顺序全列为未知。[lifespan](https://github.com/vllm-project/vllm/blob/b17039bccc17b94a2ea107272ad7bc93508708df/vllm/entrypoints/openai/api_server.py#L117-L143)、[context 与 server 收尾](https://github.com/vllm-project/vllm/blob/b17039bccc17b94a2ea107272ad7bc93508708df/vllm/entrypoints/openai/api_server.py#L1338-L1375)。来源 L25 的 `async_llm.py L460–463` 已进入 ValueError 分支，EngineDead 实际在 L455–459。
- **建议修订**：分写初始化 SIGTERM handler、应用 lifespan 清理、外层 engine context shutdown、等待 HTTP shutdown task 四个已核事实；完整 `serve_http`/uvicorn 信号与在途流行为继续留 unknown，不能由局部顺序反推自动排空。同步修来源表和锚点。
- **关闭条件**：正文、verification notes 与取证记录的关闭责任一致，已知顺序与未核链条分开，EngineDead 锚点准确。

### C03 · P2 · stop 后的回退被压缩成两个并不等价的动作

- **位置**：正文 L55–56、L82；来源记录 L23、registry KServe notes。
- **证据**：KServe 缓存 L243–257 明确：仅当 v1 仍运行时，降低 v2 权重才把流量重新分给 v1；被 stop 的 v1 需去注解、等待 Ready，随后按保留权重重新加入。示例晋升前为 9:9，重启 v1 后仍是 50/50，不能据“去 stop”认定已全部回到旧版本；旧版仍 stop 时仅降低新版正权重也不能让旧版承接请求。[固定回退段](https://github.com/kserve/website/blob/3f4067ea87dd84194bddb1b563051c84306c7997/docs/model-serving/generative-inference/llmisvc/canary-rollout.md#L241-L257)。正文“降权重，或……去注解重启”没有给出这些前提与最终流量目标。
- **建议修订**：按旧版运行/已停两种状态分支；旧版已停时先恢复资源、Ready/预热/质量 gate，再按预登记目标调整相对权重并验证实际流量。明确回退是部分减流还是完全隔离坏版本；后者还须核对直达版本路径，不能只看组内权重。新旧权重与资源保留应区别于模型已驻留内存。
- **关闭条件**：每一分支均能证明目标旧版本可服务、新版本残余流量符合回退目标；去注解或单次 patch 不再等同于回退完成，冷启动仍计入回退窗口。

### C04 · P2 · PD 失败表跨实现拼接，并把 480s 与 recompute 写成通用兜底

- **位置**：正文 L64；来源记录 L28。
- **证据**：`Pull kv failed` 是 MindIE FAQ 的 D 侧特定日志；480s 则是上游 NIXL/Mooncake 的 P 侧保留块配置，不能合并为任意 P/D 死亡后的证据与清理保证。NIXL 在 prefill 完成且延迟释放时设期限（L770–792）；Mooncake 发起传输时将期限设为无穷（L565–593），过期清理仅遍历到期项（L746–764），进程已死更不保证执行。默认 recompute 只作用于 connector 检测并上报的 invalid blocks；base 默认空集，NIXL 有上报，上游 Mooncake 的对应错误后终态未证。[NIXL 分支](https://github.com/vllm-project/vllm/blob/b17039bccc17b94a2ea107272ad7bc93508708df/vllm/distributed/kv_transfer/kv_connector/v1/nixl_connector.py#L770-L792)、[Mooncake 发送分支](https://github.com/vllm-project/vllm/blob/b17039bccc17b94a2ea107272ad7bc93508708df/vllm/distributed/kv_transfer/kv_connector/v1/mooncake_connector.py#L565-L593)、[现有 PD 失败边界](../../knowledge/07-inference/pd-disaggregation.md#失败链取消与清理)。
- **建议修订**：按引擎/connector、P/D、失败阶段分列证据与动作；将 480s 限定为所核 P 侧保留项的条件超时，把 recompute 限定为已上报 KV 加载失败。进程死亡、D 资源清理、Mooncake 错误终态和其他平台路径继续保留 unknown；先隔离受影响路径，再按具体实现核对清理/重建。
- **关闭条件**：本篇与已修订 PD 正文的限定一致，不再让读者等待 480s 后默认“已清干净”，也不默认所有传输/单侧死亡都能重算恢复。

### C05 · P2 · 请求 ID 与客户端去重被称为“唯一防线”，取消与重试条件未落到本流程

- **位置**：正文 L62、L68–73；来源记录 L26。
- **证据**：L70 的“客户端侧的幂等与去重（请求 ID 关联）是唯一防线”缺乏实现依据。`XRequestIdMiddleware` 仅回显/生成关联 ID，且受开关控制；OutputProcessor L400–424 明确同一外部 ID 可以对应多个实际内部请求。`generate` L448–459 的取消/死亡分支不提供幂等或执行一次保证；内部 ABORT 输出也不等于断连客户端已收到终态。当前[路由页](../../knowledge/07-inference/routing-and-flow-control.md#请求身份幂等与重试边界)已区分连接未建立、送达后响应未知、流式响应提交后的重试边界，本篇“失败转移或客户端重试”未带入这些条件。[取消与死亡分支](https://github.com/vllm-project/vllm/blob/b17039bccc17b94a2ea107272ad7bc93508708df/vllm/v1/engine/async_llm.py#L445-L459)、[ID 映射](https://github.com/vllm-project/vllm/blob/b17039bccc17b94a2ea107272ad7bc93508708df/vllm/v1/engine/output_processor.py#L393-L424)。
- **建议修订**：删“唯一防线”，区分关联 ID、客户端展示去重、服务端幂等/执行去重与外部副作用协议；本快照后两者无已核保证。将重试前提、响应已提交后的处理及原请求执行状态不明列入故障分支；补取消传播和资源回收观察，明确取消返回与全部资源回收是不同事件。把“不能续传”限定到本轮普通 chat/completion 路径，其他恢复协议保持未知。
- **关闭条件**：全文不把关联 ID 或取消链当作去重保证；已输出 token 不透明拼接，不确定请求与外部动作有明确处置/保留未知的路径。

### C06 · P2 · 缓存恢复边界超出证据，未区分缓存所有者与身份兼容

- **位置**：正文 L71、L81；来源记录 unknown 3。
- **证据**：“KV/prefix cache 随进程消失，新副本为冷 cache”只对被终止进程的本地状态成立，不能覆盖存活副本、独立缓存组件或外部存储。列出 connector/offload 也不能证明跨副本故障恢复契约；PD 的请求级交接不等于会话断点恢复。取证记录将这一绝对结论放在 unknown 内，实际却写成已知规则。[既有缓存身份边界](../../knowledge/07-inference/execution-and-kv-cache.md#prefix-cache-的复用边界)要求核对 token/block、LoRA、多模态与隔离字段；模型版本变化更不能由“找到 cache”推出可安全复用。
- **建议修订**：按本地活动 KV、本地 prefix、外部/offload、上层会话状态分清所有者、生命周期与恢复责任；仅声明普通独立进程本地状态不自动继承。外部缓存是否幸存、能否重挂载和身份兼容没有证据时列 unknown；恢复核对记录身份及实际命中，TTFT 只作联合观察，不能单独证明缓存恢复。
- **关闭条件**：正文与来源 unknown 一致，既不承诺自动继承，也不把所有缓存统一判为必然消失；PD/offload 不被当作无缝续传或任意版本缓存兼容的证明。

### C07 · P2 · 启动失败、运行期 fatal 与进程突然死亡的证据链被合并

- **位置**：正文 L62；来源记录 L25。
- **证据**：`core.py` L934–940 仅在 `engine_core` 已建立的运行期异常分支调用 `_send_engine_dead()`；启动失败分支只记录日志后抛出异常。`core_client.py` L425–428 证明收到 marker 时抛 EngineDeadError，不能证明所有启动/worker 死亡都会发 marker。另有条件启用的进程 sentinel 监控（L583–621），可在突然死亡时置 `engine_dead` 并关闭 client；该分支不要求先收到 marker。[运行期分支](https://github.com/vllm-project/vllm/blob/b17039bccc17b94a2ea107272ad7bc93508708df/vllm/v1/engine/core.py#L931-L943)、[进程监控](https://github.com/vllm-project/vllm/blob/b17039bccc17b94a2ea107272ad7bc93508708df/vllm/v1/engine/core_client.py#L583-L621)。
- **建议修订**：分列启动失败、运行期捕获异常、突然退出的可用证据，监控分支标明适用条件；worker 到 core 的完整传播未核就保留 unknown。结合最早异常、退出码/信号、Pod 终态/事件，而非要求每次都具备同一组日志。
- **关闭条件**：不再把启动日志→marker→客户端异常写成统一链，也不会因缺少 marker 排除副本死亡；继续保留 EngineDead 不区分 OOM/驱动/内部根因的准确边界。

### C08 · P2 · 延迟分位的回退条件方向写反

- **位置**：正文 L54、L56、L79。
- **证据**：正文以 P95 TTFT 为 SLO gate 样板，随后却以“SLO 分位跌破目标”触发回退。对 TTFT/TPOT/E2E 这类延迟分位，通常是超过预登记上限才违约；跌破下限适用于达标率/goodput 一类另外定义的指标。现有[延迟指标字典](../../knowledge/07-inference/latency-metrics.md)也没有将这些指标合成同一方向。
- **建议修订**：逐项注明指标、单位、观察窗口、样本/分母和比较方向，例如延迟分位超过上限、达标率低于下限、质量超出容差；阈值由环境预登记，不补造通用数值。
- **关闭条件**：每个继续发布/回退 gate 均可机械判断，延迟改善不会被当成回退条件，延迟恶化也不会漏报。

### C09 · P2 · 验证把故障恢复时长当摘除时延，重复/遗漏口径不足以核对恢复

- **位置**：正文 L77–83；acceptance 5。
- **证据**：L80 的“摘除时延（请求错误开始→恢复）”是服务受影响窗口，混合发现、路由、重建与冷启动，不能衡量端点/数据面何时停止选择旧副本；无可见错误时更无法计算。单凭“同请求 ID 多响应”和“发 N 收 M”也无法区分逻辑请求、重试 attempt、合法流式 chunk、已知失败、取消及终态未知。L81 提到稳定窗口，但缺少本轮达标/超时的完成判据；L83“停止”后也没有撤压、恢复配置和复核服务的动作。
- **建议修订**：用待填写记录表区分事件时间：变更/故障触发、发现、控制面状态、数据面最后一次选中旧副本、新版/恢复版接流、服务回到稳定基线。按逻辑请求＋attempt 关联，记录是否接纳、响应是否提交、完成/错误/取消/未知及输出版本，定义重复与遗漏的分母和结算截止点。预登记有限负载/观察期限、停止后的撤压/恢复动作，以及路由、错误、SLO、质量、资源在稳定窗内的完成标准。
- **关闭条件**：可以分别报告摘除收敛与用户可见中断；失败、重复、遗漏和未知可对账；停止后有恢复闭环，未实际执行的参数/结果保持空缺，不用报告总数相等证明请求正确恢复。

### C10 · P3 · KServe dark/live 风险与成员分歧的来源限定被压缩

- **位置**：正文 L46、L52–53；来源记录 L23、registry KServe notes。
- **证据**：固定 canary-rollout L64 将 CDS/RDS 原因标为理论，使用条件性描述：网关可能未预热，增权可能造成短暂连接失败。正文“会同时触发”把该解释写成确定机制。L66 的 `weight:1` 在 9:1 例中立即承接约 10% 真流量，不是统一百分比或纯离线预热。L155 则明确成员分歧会形成独立子组，并标 `GroupDegraded=True / MemberDivergence`，不只是原共享组中的一个降级标志。[固定 dark/live 段](https://github.com/kserve/website/blob/3f4067ea87dd84194bddb1b563051c84306c7997/docs/model-serving/generative-inference/llmisvc/canary-rollout.md#L61-L67)、[成员约束](https://github.com/kserve/website/blob/3f4067ea87dd84194bddb1b563051c84306c7997/docs/model-serving/generative-inference/llmisvc/canary-rollout.md#L152-L156)。
- **建议修订**：保留风险/理论的条件性和文档归属；明确非零相对权重会在 Ready 后引入真流量，实际占比取决于全部活跃成员。补子组后果与组状态核对；前置注明已安装控制器、Gateway 支持加权 backendRef，控制器/网关实现本轮未核。
- **关闭条件**：不把理论写成已核实现，也不让读者将 weight:1 当作无流量 warmup；成员身份不一致时不能假设仍参与同一分流。

### C11 · P3 · 两个 05 域入口仅有元数据，来源标签与精确页面不完全对应

- **位置**：正文 L25–27、L63、L97、L99；07 域 index 的新入口。
- **证据**：三个 05 域 related ID 均有效，但正文仅给节点回收的普通 Markdown 链接；平台变更/回退、控制面恢复没有可点击的正文入口。L97 标签声称覆盖两类 KServe canary，目标仅 predictive 页；L99 标签含 outlier detection，目标为 overload 架构页。LLM canary 已在前文正确链接，outlier 的正确 URL 已登记在 registry，因此这是导航/定位缺口，不是整组来源失效。
- **建议修订**：在平台/服务责任边界处补 05 域另外两篇普通链接，分别解释平台回退与请求恢复、控制面账本恢复与服务正确性的差别；来源表分别链接两类 canary、overload 配置与 outlier 精确页。正文的被动摘除分支可就近指向 outlier 页。
- **关闭条件**：所要求的跨域入口可直接阅读，标签与页面支持范围相符；保留已有有效导航，不为“互链”机械复制正文或要求全库每篇新增反链。

## 五条 acceptance 逐条判断

| 序号 / 要求 | 本轮判断与待关闭项 |
|---|---|
| 1 · 三层健康与版本制品身份 | **主体满足，细节待修**。L42–46 区分 liveness/readiness/质量，并列模型、tokenizer、config、adapter、量化/scale、镜像依赖；未用探针代替质量。组成员分歧后果与适用前置按 C10 补齐，platforms 不代表实测兼容。 |
| 2 · 预热、递增、质量/SLO gate、drain、连接/流式/在途及回退 | **部分满足**。五步流程和不假设自动排空已具备；drain 缺执行闭环（C01），关闭责任混写（C02），回退动作/终态不等价（C03），SLO 方向错误（C08）；补齐 C10 的带流预热和条件性。 |
| 3 · 五类故障的证据与处置 | **部分满足**。表格五类均在；PD 拼接与兜底外推（C04）、启动/运行/突然死亡证据链（C07）须修。重试预算/退避与状态残留核对方向合理，但 Envoy/SRE 精确页未由本轮独立重取，相关原文复核仍受网络限制。 |
| 4 · 不承诺 exactly-once/无缝重试，明确 token/cache/外部副作用 | **部分满足**。已输出 token 不撤回、外部动作按上层协议定义和恢复不等于正确的主旨合理；客户端“唯一防线”与重试条件按 C05 修，缓存所有权/恢复身份按 C06 修。取消链不证明执行一次或客户端收到终态。 |
| 5 · 基线→受控→摘除→恢复/回退及错误/重复/遗漏/回收/质量/稳定窗 | **部分满足**。L75–85 覆盖全部题项并明确隔离演练与环境记录；事件测量、逻辑请求/attempt 对账、停止后的恢复与完成条件按 C09 补齐。回退正确性还依赖 C03，判据依赖 C08。 |

## unknown 保留、检查与验证声明

正文与作者记录共同保留：KServe 控制器/Gateway 实现及生效时延未核；vLLM 全部 HTTP/uvicorn 关闭与在途流行为未核；探针参数默认值未引用；未做任何发布或故障注入。上述未知不能以模型推测消除。C02 要求将局部源码已能确认的顺序从笼统 unknown 中分出；C04/C06 要求把 PD 清理、cache 所有权/恢复条件重新纳入明确 unknown。SRE 数值须按来源系统实例与本地待定阈值分开，本文 3 层各重试 3 次到后端 64 次的算术只有在每层总尝试数为 4 时成立，不能解释为每层总共尝试 3 次；本轮未独立重取该章节原文，不记作已完成来源复核。

`make check` 与 `make build` 均成功：**117 content entries / 553 sources**，退出码均为 0，构建生成 `build/catalog.json` 与 `build/catalog.md`。另行解析正文的相对文件链接与 related IDs，未发现断链。检查和构建只验证结构、登记引用与本地文件目标，不验证远程页面、页内锚点语义或真实部署行为；本轮没有改 `src/kb/`，没有新增或运行其回归测试。

本次为独立模型初审，不替代真实 GPU/NPU、网关、编排与推理引擎环境验证；没有执行服务启动、发布、缩容、终止、重试或故障注入，没有产生硬件实测结果。11 项开放发现须经作者修订，再由同一审阅者对修改与相关证据定向复核；在此之前不将 T07-10 或 Batch 28 宣告为审阅通过。
