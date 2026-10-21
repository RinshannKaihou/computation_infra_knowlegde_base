# Batch 28 · T07-08 定向复核报告

## 会话元数据与结论

| 项目 | 记录 |
|---|---|
| 角色与范围 | 承接 [T07-08 初审](batch-28-t07-08-codex-review.md)，只复核 C01–C11 的修订及修订引入的问题；不代改正文或来源记录，不重审其他任务 |
| 实际执行模型 / 档位 | `gpt-6.1-sol / xhigh` |
| 模型核验 | 从 `CODEX_THREAD_ID` 对应的本地 CLI JSONL 读取本轮 `turn_context`，实见 `model=gpt-6.1-sol`、`effort=xhigh`，与 `collaboration_mode.settings` 一致；未另启审阅模型或子代理 |
| 本轮会话 ID | `01a15d52-9dc7-7f13-a262-23d72cca9158` |
| 初审会话 ID | `01a15d45-7de8-7832-adca-79c92b7c7997`；本轮是新会话，沿用其发现编号与关闭条件 |
| 执行方式 | 本地 Codex CLI，`originator=codex_exec`，`cli_version=0.163.0`；静态复核后只新增本报告 |
| 日期 / 时区 | 2026-10-21 / Asia/Shanghai |
| 工作目录 | `/Users/ywang2397/work/AI_reliability_knowledge_base` |
| 正文 | [routing-and-flow-control.md](../../knowledge/07-inference/routing-and-flow-control.md)，125 行 |
| 提交的正文 SHA-256 | `b5c279e1093f08299b1c60e6f363d2ba676bcebc4b5c83941647b401114a448d` |
| 独立计算的正文 SHA-256 | `b5c279e1093f08299b1c60e6f363d2ba676bcebc4b5c83941647b401114a448d`，**匹配** |
| 写入范围 | 仅新增 `docs/research/batch-28-t07-08-codex-recheck.md`；保留入场时已有的正文、来源记录、registry 及初审报告状态 |

**结论：本轮暂不通过。C01–C11 中 CLOSED=7、OPEN=4；另有修订引入的新问题 N01（P2，OPEN）。** 既有开放项为 C01、C02、C04、C07，均沿用初审 P2；C11（P3）已关闭。合计开放 P1=0、P2=5、P3=0。以下正文、来源记录和 registry 行号均为本轮工作区原文件坐标。

另两份被检文件的入场取样 SHA-256：

| 文件 | SHA-256 |
|---|---|
| [T07-08 来源记录](batch-28-t07-08-sources.md) | `5c8599fcf69b7e79e1c6caa2742b3483ab8b441916b48beec2f406b1a5c6ec4a` |
| [来源登记](../../sources/registry.yaml) | `816e40f516b7f3c16f32ed4c070a2716bf20b2c1b789a69f5cc66fc5847b2a0e` |

期间检测到 T07-09 相关文件及共享 registry 发生非本轮写入的变动。稍后 registry 取样摘要为 `25d41b074dce594406d6d1ef4486786ab3f02ce48b34cc3bd42a2a99e3e51993`；已重读 vLLM Batch 28 notes、SRE 队列条目及 Envoy outlier 条目，本轮 C01/C02/C07/C10/C11 所依据的相应内容和行号没有变化。T07-08 正文及来源记录仍保持上表摘要。本报告不把共享文件整体摘要固定不变作为结论前提。

## 方法与证据边界

先读仓库 `AGENTS.md`、[README](../../README.md)、[写作指南](../authoring-guide.md)及[内容总目录](../../content-outline.md)，重读初审关闭条件、修订正文、来源记录和相关 registry notes；以作者摘要定位，不以摘要代替证据。

重新计算并重读初审使用的九份已登记源码缓存，其 SHA-256 前 16 位 **9/9 与来源记录一致**：`/tmp/b28/vllm/` 下的 `api_server.py`、`serving_chat.py`、`vllm_v1_engine_async_llm.py`、`output_processor.py`、`core_client.py`、`vllm_config_scheduler.py`、`elastic_ep_middleware.py`，以及 `/tmp/b28/production-stack-vllm-stack-0.1.9/` 下的 `src/vllm_router/routers/routing_logic.py`、`src/vllm_router/stats/request_stats.py`。另读同目录的 `vllm_entrypoints_openai_serving_engine.py`、`vllm_v1_core_sched_scheduler.py`、`core.py` 和 prefix-aware 教程。源码版本仍为 vLLM `b17039bccc17b94a2ea107272ad7bc93508708df`、production-stack `20a658044af0dea70e9e0136494bb9979cfd9fab`。缓存摘要一致不能单独证明远端 tag 解析或部署配套。

本轮重新取网页时，网页工具返回 HTTP 429，GitHub 文件工具不可用；终端取页发生 DNS 解析失败，浏览器工具也没有可用浏览器。因此**没有本轮重新实开远端页面的成功记录**。为继续定向核对，读取初审会话 JSONL 中已保存的官方页面/固定源码原始工具回包，而非仅引用初审报告的判断：

| 静态证据 | 初审回包时间（UTC）与定位 |
|---|---|
| Envoy outlier 精确页面，Ejection algorithm 第 2 步 | `2026-10-21T07:04:32.789Z`；`call_6c4ed948de9c4ab3b1aa2f5c750ffaf0`；页面标题为 `1.41.0-dev-476800` |
| SRE 两章的 per-client 重试比例及稳态/突发队列段落 | `2026-10-21T07:04:49.658Z`；`call_02498ab576c94e7b9da888ff11123228`，相关段落可见，未把回包中截断的其他部分视作已读 |
| RFC 9110 §9.2.2 | `2026-10-21T07:06:51.733Z`；`call_942ca6cd6ac24838ae67f1c93ec27ac9` |
| `entrypoints/utils.py` 断连包装、`input_processor.py` ID 分配 | 前者回包 `call_3f5b6b42cbcd4cb99e65834253456862`；后者原文件 L433–444 的回显见 `call_10a945ba48894dc69a057faa0d4a9c3b` |

上述回包位于 `~/.codex/sessions/2026/10/21/rollout-2026-10-21T15-03-20-01a15d45-7de8-7832-adca-79c92b7c7997.jsonl`，只作为历史证据读取。Envoy 对应 JSONL 整行 SHA-256 为 `2e88b1260c7e00d7bf65ba312dae1c9bb59e4ab6e4668fa789c42b3c84aac567`。它支持对既有方向错误的静态复核，不代表当前 latest 页已复验，也不重建作者记录的 `e05ba9` 历史快照。所有 GitHub 锚点继续使用原文件坐标，不使用网页工具转换后的行号。

## C01–C11 逐项判定

| 编号 | 结论 | 本轮位置与理由 |
|---|---|---|
| C01 · P2 | **OPEN** | 正文 L54/L95 已补中间件启用条件，并分开响应头与引擎 ID；来源记录 L37、registry L536 的门控也已同步。但 L95 及来源记录 L37 仍将引擎 external ID 简写为“取自输入头或默认值”，遗漏已核普通 chat 路径的 `chatcmpl-` 加工；已知路径仍被完整映射 unknown 掩盖。见下方剩余条件。 |
| C02 · P2 | **OPEN** | 正文 L84、来源记录 L39、registry L536 已正确将 ValueError 定位为启动配置校验。但“运行期预算不足只是本轮停止准入新请求”仍缺 chunked prefill 条件；运行期分支与初始化调用点也未补入正文/来源定位。见下方剩余条件。 |
| C03 · P2 | **CLOSED** | 正文 L65 已只列到达窗 QPS，把 avg_latency 放回未参与决策的统计字段，明确非第六种可选算法；来源记录 L33 已补 L226–228/L367–369 调用点。[辅助分支 L62–84](https://github.com/vllm-project/production-stack/blob/20a658044af0dea70e9e0136494bb9979cfd9fab/src/vllm_router/routers/routing_logic.py#L62-L84)仅比较 `request_stat.qps`，无统计 endpoint 直接返回；[session fallback](https://github.com/vllm-project/production-stack/blob/20a658044af0dea70e9e0136494bb9979cfd9fab/src/vllm_router/routers/routing_logic.py#L220-L233)与 [KV fallback](https://github.com/vllm-project/production-stack/blob/20a658044af0dea70e9e0136494bb9979cfd9fab/src/vllm_router/routers/routing_logic.py#L358-L373)一致。 |
| C04 · P2 | **OPEN** | 正文 L67–69 已拆分 session、kvaware、prefixaware，去掉命中保证，并注明 HashTrie 不考虑驱逐；L73/L113 已收缩为无比较基准的机制归纳。但 L68 及来源记录 L35 仍用“matched_tokens 低于阈值”描述回退，未准确解释 2000 参数。实际阈值依赖 prompt 长度，见下方剩余条件。 |
| C05 · P2 | **CLOSED** | 正文 L96 已恢复“重复请求的预期服务端效果”这一幂等概念，删除“清理正确＝重试安全”的替代定义；关联 ID、输出随机性、清理与去重分开，幂等键/去重/仅一次执行没有被宣称为已支持。此处按原问题关闭；新增的“每次提交……实际执行”断言单独记 N01，不因本项关闭而认可整句。通用定义对照 [RFC 9110 §9.2.2](https://www.rfc-editor.org/rfc/rfc9110.html#section-9.2.2)。 |
| C06 · P2 | **CLOSED** | 正文 L97 已限定本轮普通 chat/completion 路径，删除跨版本保证；把代理政策标为本库建议，区分连接建立失败与已送达但未见响应，后者明确受 L96 的幂等边界约束。结合两条阅读，“响应提交之前”是必要边界，没有被写成已送达请求的充分重试条件。所选接口的 StreamingResponse 返回点为 [chat L488–516](https://github.com/vllm-project/vllm/blob/b17039bccc17b94a2ea107272ad7bc93508708df/vllm/entrypoints/openai/api_server.py#L488-L516)、[completion L529–556](https://github.com/vllm-project/vllm/blob/b17039bccc17b94a2ea107272ad7bc93508708df/vllm/entrypoints/openai/api_server.py#L529-L556)；其他应用恢复协议仍 unknown。 |
| C07 · P2 | **OPEN** | 正文 L86–89 已删除通用数字原则，注明 per-client、稳态线程池和部署预注册验证，正文修订有效。但来源记录 L27–28 仍将含数值主张统称“原则层”，L28 和 registry L6810 的 50% 仍缺稳态条件与突发例外；不能仅靠正文新增解释认为取证登记已同步。见下方剩余条件。 |
| C08 · P2 | **CLOSED** | 正文 L91 已分开组件本地保护与上游收到信号后的减载；删去矛盾的统一层次排序及“两章公共结论”归属。入口尽早拒绝被明确标为本库有条件建议，并注明观测滞后及与本地保护互补，符合本项关闭条件。依据仍为 [SRE Handling Overload](https://sre.google/sre-book/handling-overload/) 与 [Cascading Failures](https://sre.google/sre-book/addressing-cascading-failures/) 的相关段落，本轮只复读历史回包。 |
| C09 · P2 | **CLOSED** | 正文 L106 已分开窗口分位 gate、逐请求达标率、goodput，要求同窗记录、显式固定分母并分类 attempted/failed/cancelled/rejected，保留错误与质量判据；[指标字典](../../knowledge/07-inference/latency-metrics.md) L177–189 补充同一 SLO 集合及组合、good completed 数和窗口时长。按这些要求记录后，达标率可由达标请求数/预先选定分母复算，goodput 可由达标成功数/时长复算；不要求为关闭本项实际压测。 |
| C10 · P2 | **CLOSED** | registry L6838 与来源记录 L30 已把“超过上限才弹出”改成上限限制继续弹出，并保留初登更正记录及 panic 边界。本轮将修订与已保存的[精确官方页面 Ejection algorithm 第 2 步](https://www.envoyproxy.io/docs/envoy/latest/intro/arch_overview/upstream/outlier#ejection-algorithm)原始回包逐项对照，方向一致。只关闭原反向门控错误；不确认等于上限时的行为、取整、API 默认值或当前 latest 内容。 |
| C11 · P3 | **CLOSED** | 正文实际可见的 EngineDeadError 精确分支链接位于 L98，现为 [async_llm.py L455–459](https://github.com/vllm-project/vllm/blob/b17039bccc17b94a2ea107272ad7bc93508708df/vllm/v1/engine/async_llm.py#L455-L459)，不再落到 ValueError；来源记录 L38 和 registry L536 同步正确。registry 原不存在的聚合文件名已换为 T07-08 至 T07-11 分任务记录，四份文件实际存在。断连补链及 KV 非即时释放限定与代码一致，详见后文。 |

## 既有开放项的剩余条件

### C01 · 已核路径的 external ID 仍不能等同原始 HTTP 头

**位置：正文 L95；来源记录 L37/L52。** 中间件门控已修好；剩余问题是引擎 ID 的加工链。固定快照的 [_base_request_id L1472–1481](https://github.com/vllm-project/vllm/blob/b17039bccc17b94a2ea107272ad7bc93508708df/vllm/entrypoints/openai/serving_engine.py#L1472-L1481)从输入头取基础值，缺头时使用请求字段提供的 default 或另生成随机值；[serving_chat.py L338–357](https://github.com/vllm-project/vllm/blob/b17039bccc17b94a2ea107272ad7bc93508708df/vllm/entrypoints/openai/serving_chat.py#L338-L357)再加 `chatcmpl-`，多 prompt 还会产生子请求后缀。[InputProcessor L433–444](https://github.com/vllm-project/vllm/blob/b17039bccc17b94a2ea107272ad7bc93508708df/vllm/v1/engine/input_processor.py#L433-L444)保存的是传入引擎的 ID，随后才追加随机内部后缀。

限定普通单 prompt、单样本 chat，可清楚区分两种路径：有头值 `H` 时，启用中间件的响应头为 `H`，引擎 external ID 则为 `chatcmpl-H`；没有头时，中间件生成响应 ID，与服务入口选取基础 ID 是不同动作。`output_processor` 的 external→internal 映射不能直接当作原始 HTTP 头→internal 映射。

**关闭所需最小修订：** 在正文和来源记录注明基础 ID 与引擎 external ID 之间的已核加工，明确有头/无头两种路径，补上述固定锚点。未核 endpoint、代理透传及完整跨层对应仍可 unknown；不要求扩查全部入口。

### C02 · 运行期停止准入仍需区分预算耗尽与可分块执行

**位置：正文 L84；来源记录 L39/L53。** [配置初始化调用 L247](https://github.com/vllm-project/vllm/blob/b17039bccc17b94a2ea107272ad7bc93508708df/vllm/config/scheduler.py#L247-L261)确认 ValueError 是配置校验，该旧错误已纠正。剩余运行期表述不能覆盖所有“请求所需 token 多于剩余预算”的情况：

- [scheduler L461–465](https://github.com/vllm-project/vllm/blob/b17039bccc17b94a2ea107272ad7bc93508708df/vllm/v1/core/sched/scheduler.py#L461-L465)：token 预算耗尽或 running 数到上限，本轮不再准入 waiting 请求。
- [scheduler L572–582](https://github.com/vllm-project/vllm/blob/b17039bccc17b94a2ea107272ad7bc93508708df/vllm/v1/core/sched/scheduler.py#L572-L582)：请求所需 token 超过剩余预算时，**禁用 chunked prefill** 才在该分支 `break`；可分块时按 `min(num_new_tokens, token_budget)` 调度部分 token。

**关闭所需最小修订：** 收紧“预算不足只是停止准入”的条件，区分预算耗尽、并发上限与可分块 prefill；将初始化调用点和运行期分支坐标补入正文或来源定位。继续保留“这不是逐请求入口拒绝”及 waiting 无长度上限的边界，不需要新增拒绝机制主张。

### C04 · 2000 参数不是 matched_tokens 的固定下限

**位置：正文 L68；来源记录 L35。** [构造器 L242–267](https://github.com/vllm-project/production-stack/blob/20a658044af0dea70e9e0136494bb9979cfd9fab/src/vllm_router/routers/routing_logic.py#L242-L267)将 `kv_aware_threshold` 默认 2000 赋给 `self.threshold`，但[决策 L358–373](https://github.com/vllm-project/production-stack/blob/20a658044af0dea70e9e0136494bb9979cfd9fab/src/vllm_router/routers/routing_logic.py#L358-L373)比较的是：

```python
matched_tokens < max(len(token_ids) - self.threshold, 0)
```

在查找结果有效且非空的前提下，静态代入 prompt 长度 6000、参数 2000、命中 3000，实际比较为 `3000 < 4000`，仍回退；若误解成“命中低于 2000 才回退”便会得到相反判断。此为代码条件代入，未运行路由器或压测。

**关闭所需最小修订：** 正文及来源记录写出实际比较式，说明该参数参与的是随 prompt 长度变化的判据，区分缺结果/空结果与命中不足的 fallback；不要保留固定最低命中数的读法。session 与 prefixaware 的拆分、无驱逐假设和无比较基准限定已满足，无需重做。

### C07 · 正文中的数值限定尚未同步到取证登记

**位置：来源记录 L27–28；registry L6799/L6810。** 正文 L89 已正确收缩。历史官方回包中，[Handling Overload 的 Deciding to Retry](https://sre.google/sre-book/handling-overload/#deciding-to-retry)明确是 Google 的 per-client 比例实现；[Cascading Failures 的 Queue Management](https://sre.google/sre-book/addressing-cascading-failures/#queue-management)将 50% 放在较稳态流量、相对线程池大小的例子中，紧接着区分突发负载。

来源记录两行仍把这些数值与通用原则混列为“原则层”；registry 的重试条目已有 per-client，但队列条目仍只有“≤50%”，没有稳态条件与突发区别。仅更新来源记录末尾的“C07 已修订”摘要，不能替代主张表和登记条目自身的限定。

**关闭所需最小修订：** 将主张表中的通用原则与来源系统数值实例分开注明，并在 registry 队列实例处同步稳态/线程池条件及突发边界；或删除这两处无必要的具体数字。无需为本部署编造阈值或执行实验。

## 修订引入的新问题

### N01 · P2 · OPEN · 从独立内部 ID 推出“每次提交都实际执行”

**位置：正文 L96 新增句“每次提交都生成新内部 ID 并实际执行”。** 同一 external ID 可关联多个 internal ID，只能说明 ID 关联不是去重承诺；不能由此断言每次提交都实际计算。即使请求已通过输入处理，[async_llm.py L331–350](https://github.com/vllm-project/vllm/blob/b17039bccc17b94a2ea107272ad7bc93508708df/vllm/v1/engine/async_llm.py#L331-L350)也先分配内部 ID，再等待暂停状态解除并提交请求；其后请求还可能排队。[scheduler L1470–1492](https://github.com/vllm-project/vllm/blob/b17039bccc17b94a2ea107272ad7bc93508708df/vllm/v1/core/sched/scheduler.py#L1470-L1492)允许 waiting 请求在执行前被取消移除。

修订已正确提醒**可能**重复执行/计费，这个风险判断可以保留；但不能把 ID 分配、接受入队、开始执行和完成混成同一事实。该断言是本轮新增，另立 N01，不重复登记 C05 已删除的幂等替代定义。

**关闭条件：** 改成“重复提交可产生独立内部请求，未建立去重证据，因此可能重复执行”等有限表述；明确不由 ID 分配证明请求已执行或完成。实际执行次数、计费行为继续按现场证据判断，不补写运行结果。

除 N01 外，在本轮修订范围未发现需要另立编号的新问题。

## 取消链补核与检查结果

C11 补入的取消包装在 chat 的 `api_server.py` L488，completion 的对应挂载实际为 L529；正文只链接 L488 不妨碍已核两个路由，但两者不是同一个挂载点。历史 `entrypoints/utils.py` 回包区分 handler 阶段监听与返回 StreamingResponse 后由响应对象监听。取消进入 [async_llm.py L448–454](https://github.com/vllm-project/vllm/blob/b17039bccc17b94a2ea107272ad7bc93508708df/vllm/v1/engine/async_llm.py#L448-L454)，有 collector 时调用 abort；[L551–560](https://github.com/vllm-project/vllm/blob/b17039bccc17b94a2ea107272ad7bc93508708df/vllm/v1/engine/async_llm.py#L551-L560)先清 OutputProcessor 再向 EngineCore 发送取消。[scheduler L1494–1512](https://github.com/vllm-project/vllm/blob/b17039bccc17b94a2ea107272ad7bc93508708df/vllm/v1/core/sched/scheduler.py#L1494-L1512)按 `delay_free_blocks` 决定即时或延迟归还 KV；正文 L98 新增的“前端取消结果不等于全部资源即时回收”限定成立，不建立任何回收时延保证。

已执行 `make check`，结果为 **PASS: 117 content entries; 553 sources**。报告落盘后检查本地链接，并在临时完整源文件副本运行 `make check`、`make build`；构建产物只写临时副本，以遵守原工作区只新增本报告的限制。首次副本检查因没有复制被 `docs/first-fill-status.md` 链接的既有 `build/catalog.json`、`build/catalog.md` 而失败；带入这两个已有产物后，副本检查及重新构建均通过，未改源文件修补该问题。检查与构建不能证明技术语义、远程链接可达性或硬件行为。未修改 `src/kb/`，未新增或执行测试。

交付前对入场记录的 596 份既有源文件逐文件比对 SHA-256：T07-08 正文、来源记录及初审报告未变；检测到 `docs/research/batch-28-t07-09-sources.md`、`knowledge/07-inference/capacity-and-autoscaling.md`、`sources/registry.yaml` 发生期间变更，并另见 T07-09 初审报告出现，本轮没有写入这些文件。本轮文件写入只针对本报告，正文摘要再次核验仍为提交值。未修改导航、任务账本或审核状态，未将正文的 `draft / source_checked` 升级。

**本轮没有部署服务、启动引擎、发起推理负载或执行 GPU/NPU 验证。** 模型审阅、缓存源码、历史网页回包与结构检查都不构成实际资源回收、恢复、性能或质量验证。后续只需修订并定向复核 C01、C02、C04、C07、N01；已关闭的七项不因本报告自动扩大其适用范围，也不代表 Batch 28 其他任务通过。
