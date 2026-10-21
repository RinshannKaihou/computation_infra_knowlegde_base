# Batch 28 · T07-08 第二轮定向复核报告

## 会话元数据与结论

| 项目 | 记录 |
|---|---|
| 角色与范围 | 承接[第一轮定向复核](batch-28-t07-08-codex-recheck.md)，仅复核 OPEN 项 C01/C02/C04/C07 的剩余条件及 N01，并检查这些修订引入的问题；不重审其他已关闭项或其他任务 |
| 实际执行模型 / 档位 | `gpt-6.1-sol / xhigh` |
| 模型核验 | 读取 `CODEX_THREAD_ID` 对应本地 CLI JSONL 的本轮 `turn_context`，实见 `model=gpt-6.1-sol`、`effort=xhigh`，与 `collaboration_mode.settings` 一致；本轮未另启模型或子代理 |
| 本轮会话 ID | `01a15d61-0b47-7713-a24b-9eeb0a40da30` |
| 第一轮复核会话 ID | `01a15d52-9dc7-7f13-a262-23d72cca9158`；沿用发现编号与关闭条件 |
| 执行方式 | 本地 Codex CLI，`originator=codex_exec`、`cli_version=0.163.0`；静态定向复核 |
| 日期 / 时区 | 2026-10-21 / Asia/Shanghai |
| 工作目录 | `/Users/ywang2397/work/AI_reliability_knowledge_base` |
| 正文 | [routing-and-flow-control.md](../../knowledge/07-inference/routing-and-flow-control.md)，125 行 |
| 提交的正文 SHA-256 | `d4fe2d2d5e0fef08dec12b996eb3033222da72a136fc1f804fa567402a035f13` |
| 独立计算的正文 SHA-256 | `d4fe2d2d5e0fef08dec12b996eb3033222da72a136fc1f804fa567402a035f13`，**匹配** |
| 写入范围 | 仅新增本报告；不修改正文、来源记录、registry、导航、任务账本或审核状态 |

**结论：本轮暂不通过。指定的 5 项中，CLOSED=4（C02/C04/C07/N01），OPEN=1（C01，沿用 P2）；另有新发现 N02（P2，OPEN）。当前合计开放 P1=0、P2=2、P3=0。** C04 的原比较式问题与 N02 的缺失结果处理问题分别判定，关闭前者不代表认可后者。第一轮已经关闭的其他项不在本轮重新判定范围内。

最主要的交付差异是：作者摘要声称正文“请求身份”节已补 ID 加工链，但本次哈希匹配的正文 L95 仍保留旧句。来源记录的修订不能替代正文修订。

另两份被检文件的取样摘要：

| 文件 | SHA-256 |
|---|---|
| [T07-08 来源记录](batch-28-t07-08-sources.md) | `0e5b3c216f252978c07bade87d6ce5271afa3dad72783d3c848c23d97002320f` |
| [来源登记](../../sources/registry.yaml) | `abecd29b5c7f9527919f8bde9fc900aa9a37d73048aa558d3e272b6c99d7bd18` |

以下正文、来源记录及 registry 行号均为本轮工作区原文件坐标。

## 方法与证据边界

已读取仓库 `AGENTS.md`、[README](../../README.md)、[写作指南](../authoring-guide.md)、[内容总目录](../../content-outline.md)，并重新读取第一轮关闭条件、修订正文、来源记录主张表及相关登记条目；以修订摘要定位，不以摘要代替实际文件。

本轮重新计算并读取既有固定源码缓存。版本仍为 vLLM `b17039bccc17b94a2ea107272ad7bc93508708df` 与 production-stack `20a658044af0dea70e9e0136494bb9979cfd9fab`，锚点采用原文件坐标：

| 缓存文件 | SHA-256 前 16 位 |
|---|---|
| `/tmp/b28/vllm/api_server.py` | `dcc6b46ca859074d` |
| `/tmp/b28/vllm/serving_chat.py` | `6161fd8ec3a21f79` |
| `/tmp/b28/vllm/output_processor.py` | `381c443e029c4cd8` |
| `/tmp/b28/vllm/vllm_entrypoints_openai_serving_engine.py` | `20e18f1ea16adc9f` |
| `/tmp/b28/vllm/vllm_config_scheduler.py` | `6aaecf693bf96695` |
| `/tmp/b28/vllm/vllm_v1_core_sched_scheduler.py` | `b4e664fe7dc9ea5c` |
| `/tmp/b28/vllm/vllm_v1_engine_async_llm.py` | `818af4561b7ae54a` |
| `/tmp/b28/production-stack-vllm-stack-0.1.9/src/vllm_router/routers/routing_logic.py` | `13bd003e7e132159` |

其中来源记录取回清单已列出的 5 份文件（api_server、serving_chat、output_processor、config/scheduler、routing_logic），摘要前缀均匹配；其余为第一轮已经使用的补充缓存，未冒称它们也列在原取回清单中。

本轮尝试重新取证：网页工具返回 HTTP 429；GitHub 文件工具返回不可用；终端获取固定 `input_processor.py` 时 DNS 解析失败。因此没有本轮成功重新实开远端页面或重新下载源码的记录。为补核 ID 分配及 SRE 剩余条件，直接读取初审会话 JSONL 中保存的原始工具回包，而非只引用先前报告的结论：

| 历史证据 | 原始回包定位 |
|---|---|
| SRE per-client 重试比例、稳态线程池队列实例及紧接的突发负载区别 | `2026-10-21T07:04:49.658Z`，`call_02498ab576c94e7b9da888ff11123228`，JSONL 第 93 行；只使用回包实际可见段落 |
| `input_processor.py` 原文件 L433–444：保存 external ID 后追加随机内部后缀 | `2026-10-21T07:07:11.747Z`，`call_10a945ba48894dc69a057faa0d4a9c3b`，JSONL 第 206 行 |

历史文件为 `~/.codex/sessions/2026/10/21/rollout-2026-10-21T15-03-20-01a15d45-7de8-7832-adca-79c92b7c7997.jsonl`。上述回包支持本轮静态复核，不表示远端当前页面已复验；缓存摘要一致也不能独立证明 tag 解析或部署配套。未部署、未压测，没有硬件验证或现场故障记录。

## 指定 OPEN 项逐项判定

| 编号 | 结论 | 理由与证据 |
|---|---|---|
| C01 · P2 | **OPEN** | 来源记录 L37 已补基础 ID → `chatcmpl-` 外部 ID → 随机后缀内部 ID，但正文 L95 仍写“引擎的外部请求 ID 取自输入头或引擎默认值”，没有 `chatcmpl-` 加工、有头/无头两路径或相应锚点；仍用完整对应 unknown 遮盖已核普通 chat 路径。正文与来源表不一致，未满足第一轮要求两处同步的关闭条件。详见下节。 |
| C02 · P2 | **CLOSED** | 正文 L84、来源记录 L39 已区分三个条件：初始化调用 `verify_max_model_len`，在未启用 chunked prefill 且预算小于模型长度时抛配置 ValueError（[config L247–261](https://github.com/vllm-project/vllm/blob/b17039bccc17b94a2ea107272ad7bc93508708df/vllm/config/scheduler.py#L247-L261)）；预算耗尽或 running 达上限停止本轮 waiting 准入（[scheduler L461–465](https://github.com/vllm-project/vllm/blob/b17039bccc17b94a2ea107272ad7bc93508708df/vllm/v1/core/sched/scheduler.py#L461-L465)）；请求所需 token 超剩余预算时，未启用分块才在该分支跳出，可分块时按 `min(num_new_tokens, token_budget)` 限定本轮 token 数（[L572–582](https://github.com/vllm-project/vllm/blob/b17039bccc17b94a2ea107272ad7bc93508708df/vllm/v1/core/sched/scheduler.py#L572-L582)）。初始化/运行期定位已补齐，未重新写成逐请求入口拒绝；waiting 无长度上限的边界保留。 |
| C04 · P2 | **CLOSED** | 正文 L68、来源记录 L35 已写出实际比较式 `matched_tokens < max(len(token_ids) - threshold, 0)`，默认参数与赋值对应[构造器 L242–267](https://github.com/vllm-project/production-stack/blob/20a658044af0dea70e9e0136494bb9979cfd9fab/src/vllm_router/routers/routing_logic.py#L242-L267)，比较对应[分支 L358–373](https://github.com/vllm-project/production-stack/blob/20a658044af0dea70e9e0136494bb9979cfd9fab/src/vllm_router/routers/routing_logic.py#L358-L373)。6000/2000/3000 的代入得到 `3000 < 4000`，回退判断正确；不再将 2000 当固定最低命中数。缺结果/空结果已单独写出，但其中把 `None` 当作可正常回退的主张存在新问题，另记 N02，不计为原比较式问题未修。代入仅为静态推导。 |
| C07 · P2 | **CLOSED** | 来源记录 L27 已明确区分通用原则与来源系统数值实例，10% 标为 per-client，K=2 标为 Google 实现实例；L28 的 50% 已补较平稳流量、thread-per-request 线程池条件及突发区别。registry L6810 同步这三项限定，正文 L89 用文字说明实例边界，未泛化为推理通用阈值。与历史原始回包中的 [Deciding to Retry](https://sre.google/sre-book/handling-overload/#deciding-to-retry) 及 [Queue Management](https://sre.google/sre-book/addressing-cascading-failures/#queue-management) 剩余条件一致；本轮只复核这些限定，没有重审章节全部数值。 |
| N01 · P2 | **CLOSED** | 正文 L96 已改为重复提交“可产生”独立内部请求、“可能”重复执行，并明确 ID 分配不证明开始/完成，排队或执行前取消均可能。该边界符合 [async_llm L331–350](https://github.com/vllm-project/vllm/blob/b17039bccc17b94a2ea107272ad7bc93508708df/vllm/v1/engine/async_llm.py#L331-L350) 先分配 ID 再等待暂停解除/提交的顺序，以及 [scheduler L1470–1492](https://github.com/vllm-project/vllm/blob/b17039bccc17b94a2ea107272ad7bc93508708df/vllm/v1/core/sched/scheduler.py#L1470-L1492) 可移除 waiting 请求的路径。去重/仅一次执行继续 unknown，没有声称已观测到实际执行次数或计费行为。来源记录末尾本轮修订摘要 L70 同步；更早修订轮的历史摘要不作为现行执行保证。 |

## C01 剩余条件：来源已改，正文仍是旧句

**位置：正文 L95；来源记录 L37、L66。** 正文的“② 引擎的外部请求 ID 取自输入头或引擎默认值”仍遗漏入口加工。固定快照的实际链为：

1. [_base_request_id L1472–1481](https://github.com/vllm-project/vllm/blob/b17039bccc17b94a2ea107272ad7bc93508708df/vllm/entrypoints/openai/serving_engine.py#L1472-L1481)从输入头取基础 ID；没有头时取传入的 default，否则另生成。
2. [chat L338–357](https://github.com/vllm-project/vllm/blob/b17039bccc17b94a2ea107272ad7bc93508708df/vllm/entrypoints/openai/serving_chat.py#L338-L357)传入 `request.request_id` 作为 default，再加 `chatcmpl-`；多 prompt 另追加子请求后缀。
3. [InputProcessor L433–444](https://github.com/vllm-project/vllm/blob/b17039bccc17b94a2ea107272ad7bc93508708df/vllm/v1/engine/input_processor.py#L433-L444)保存传入引擎的 external ID，随后生成带随机后缀的 internal ID。

限定普通单 prompt、单样本 chat，启用响应中间件且输入头为 `H` 时，响应头为 `H`，引擎 external ID 为 `chatcmpl-H`；无头时，[响应中间件 L720–723](https://github.com/vllm-project/vllm/blob/b17039bccc17b94a2ea107272ad7bc93508708df/vllm/entrypoints/openai/api_server.py#L720-L723)生成响应 ID，与服务入口选择基础 ID 是不同动作。这些已知路径不应被完整跨层对应 unknown 取代。

来源表 L37 已表达主要加工链；来源记录 L66 也记述了补链、有头/无头分列的修订结果，但正文仍未体现。这是 C01 尚未落实到正文的同一问题，不另立编号。

**关闭所需最小修订：** 在正文 L95 落实上述加工链与有头/无头区别，补固定源码锚点，保留“引擎 external ID 不等于原始 HTTP 头值”的限定，并使来源记录对修订结果的描述与文件一致。未核 endpoint、代理透传及完整跨层对应可继续 unknown；不要求扩查全部入口。

## 新发现

### N02 · P2 · OPEN · 前置属性访问使“缺结果也会 fallback”不成立

**位置：正文 L68 的“查询缺结果/空结果另有 fallback”；来源记录 L35 同句。** 这是本轮相关修订的新发现，不是本仓库新增了上游代码缺陷，也不撤销 C04 比较式修订本身。

按固定 [routing_logic.py L347–373](https://github.com/vllm-project/production-stack/blob/20a658044af0dea70e9e0136494bb9979cfd9fab/src/vllm_router/routers/routing_logic.py#L347-L373) 的实际执行顺序：查询结果赋给 `instance_id` 后，L352 **先**读取 `instance_id.layout_info.keys()`；L358–361 才判断 `instance_id is None`、空 `layout_info` 或命中不足。若返回对象为 `None`，前置属性读取即会出错，无法走到后面的 None 回退条件。因此不能把后置 if 列出的三项直接解释成三种均已有效处理的路径。

两种状态需要分开：存在有效结果对象但 `layout_info` 为空时，能走到回退分支；缺少结果对象、返回 `None` 时，该局部路径不能证明正常回退。控制器是否实际返回 `None`、查询异常/超时如何向上层传播或恢复，本轮没有补充证据；不宣称观察到线上异常。

这会影响读者对 LMCache 查询失败时仍可由 session/QPS 接续路由的判断。第一轮关闭条件曾要求区分缺/空结果，但其措辞也不能代替本轮对前置执行顺序的核查。

**关闭条件：** 正文和来源记录将确定的回退限定为有效非 None 结果对象的空 `layout_info` 或比较式成立；注明代码虽列 None 条件，却在此前访问了其属性，缺失对象及查询异常/超时的端到端恢复仍 unknown。可直接删除无证据的“缺结果会回退”保证；不要求修改上游、部署控制器或编造复现结果。

除 N02 外，在本轮指定修订范围内未发现需要另立编号的新问题。

## 检查与交付边界

入场已独立执行 `make check`；报告落盘后，在临时完整文件副本 `/tmp/t07-08-recheck2-checks-jpxz0n35` 执行 `make check`、`make build`，均为 **PASS: 117 content entries; 553 sources**，成功生成两个 catalog 文件。副本带入既有 `build/catalog.json`、`build/catalog.md`，以满足仓库内原有链接；重新构建的产物只写临时副本，原工作区保持只新增本报告。

对本轮基线记录的 601 份既有文件逐项比对 SHA-256，T07-08 正文、来源记录、registry 及既有复核报告均未变；唯一新增文件为本报告。期间另检测到 `docs/research/batch-28-t07-10-sources.md` 与 `knowledge/07-inference/release-and-recovery.md` 发生变更，本轮没有写入这两个文件，未将其变更计为本轮交付。交付前再次计算正文摘要，仍与提交值匹配。

本报告不改变正文的 `draft / source_checked` 状态。结构检查与构建不能证明技术语义、远端内容或硬件行为；未修改 `src/kb/`，无需新增测试或执行 `make test`。
