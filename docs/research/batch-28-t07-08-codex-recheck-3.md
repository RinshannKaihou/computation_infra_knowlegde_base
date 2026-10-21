# Batch 28 · T07-08 第三轮定向复核报告

## 会话元数据与结论

| 项目 | 记录 |
|---|---|
| 角色与范围 | 承接[第二轮定向复核](batch-28-t07-08-codex-recheck-2.md)，仅复核 OPEN 项 C01 的剩余条件与 N02，并检查这两项修订引入的问题；不重审已关闭项或其他任务 |
| 实际执行模型 / 档位 | `gpt-6.1-sol / xhigh` |
| 模型核验 | 读取 `CODEX_THREAD_ID` 对应本地 CLI JSONL 的本轮 `turn_context`，实见 `model=gpt-6.1-sol`、`effort=xhigh`，与 `collaboration_mode.settings` 一致；未另启模型或子代理 |
| 本轮会话 ID | `01a15d69-d069-7db0-80b3-b200af1f0fc4` |
| 第二轮复核会话 ID | `01a15d61-0b47-7713-a24b-9eeb0a40da30`；沿用发现编号、优先级与关闭条件 |
| 执行方式 | 本地 Codex CLI，`originator=codex_exec`、`cli_version=0.163.0`；静态定向复核 |
| 日期 / 时区 | 2026-10-21 / Asia/Shanghai |
| 工作目录 | `/Users/ywang2397/work/AI_reliability_knowledge_base` |
| 正文 | [routing-and-flow-control.md](../../knowledge/07-inference/routing-and-flow-control.md)，125 行 |
| 提交的正文 SHA-256 | `13a5d2282fe3dda55b773b2acfbac3d2fffb9dd98c06f7f54ae1be387c916899` |
| 独立计算的正文 SHA-256 | `13a5d2282fe3dda55b773b2acfbac3d2fffb9dd98c06f7f54ae1be387c916899`，**匹配** |
| 写入范围 | 仅新增本报告；不修改正文、来源记录、registry、既有报告、导航、任务账本或审核状态 |

**结论：本轮定向复核通过。CLOSED=2（C01 剩余条件、N02），OPEN=0；未发现需要登记为 N03 或后续编号的新问题。指定范围内剩余开放 P1=0、P2=0、P3=0。** 已关闭项沿用前两轮结论，不在本轮重新判定；本结论不代表完成部署、压测或硬件验证。

另两份关联文件的入场 SHA-256：

| 文件 | SHA-256 |
|---|---|
| [T07-08 来源记录](batch-28-t07-08-sources.md) | `fa5b6a71534687b58d7f2d66175095b0d816a9fbebfc46741739855c9cb43a2b` |
| [来源登记](../../sources/registry.yaml) | `abecd29b5c7f9527919f8bde9fc900aa9a37d73048aa558d3e272b6c99d7bd18` |

以下正文及来源记录行号均为本轮工作区原文件坐标。

## 方法与证据边界

已读取仓库 `AGENTS.md`、[README](../../README.md)、[写作指南](../authoring-guide.md)及[内容总目录](../../content-outline.md)，以第二轮关闭条件定位正文 L68/L95 和来源记录 L35/L37/L74–75；同时检查相邻现行表述是否重新引入相同保证。修订摘要仅用于定位，判定依据为实际文件及原始源码证据。

本轮重新计算摘要并读取以下既有源码缓存。固定版本沿用 vLLM `b17039bccc17b94a2ea107272ad7bc93508708df` 与 production-stack `20a658044af0dea70e9e0136494bb9979cfd9fab`；GitHub 锚点使用原文件坐标。

| 缓存文件 | SHA-256 前 16 位 | 本轮核对范围 |
|---|---|---|
| `/tmp/b28/vllm/api_server.py` | `dcc6b46ca859074d` | L698–727、L940–941：响应头处理与中间件挂载条件 |
| `/tmp/b28/vllm/vllm_entrypoints_openai_serving_engine.py` | `20e18f1ea16adc9f` | L1472–1481：基础 ID 选择顺序 |
| `/tmp/b28/vllm/serving_chat.py` | `6161fd8ec3a21f79` | L338–357、L386–427：chat 前缀、子请求 ID 与传入引擎的 ID |
| `/tmp/b28/vllm/output_processor.py` | `381c443e029c4cd8` | L393–456：external/internal ID 的取消映射语义 |
| `/tmp/b28/production-stack-vllm-stack-0.1.9/src/vllm_router/routers/routing_logic.py` | `13bd003e7e132159` | L325–397：查询结果属性访问顺序与回退分支 |

其中 `serving_engine.py` 为前轮补充缓存，其余四份文件的摘要前缀与来源记录取回清单一致；五份均与第二轮报告所记缓存摘要一致。摘要一致只能确认本轮读取的缓存内容未变，不能独立证明远端 tag 解析或部署配套。

本轮尝试重新打开四个固定 GitHub 文件 URL，网页工具返回 HTTP 429；GitHub 文件工具返回不可用；终端下载固定 `input_processor.py` 及补核用 `protocol.py` 时 DNS 解析失败。**本轮没有成功重新实开远端页面或下载源码的记录，也未将未取得的 `protocol.py` 视为证据。**

`input_processor.py` 的 ID 分配另据初审保存的原始工具回包复读：`~/.codex/sessions/2026/10/21/rollout-2026-10-21T15-03-20-01a15d45-7de8-7832-adca-79c92b7c7997.jsonl` 第 206 行，时间 `2026-10-21T07:07:11.747Z`，调用 `call_10a945ba48894dc69a057faa0d4a9c3b`。该回包直接显示原文件 L433–447；包含此代码的文本块 SHA-256 为 `2f8b9c9ac0e9b79a12be5af2d00ae91f741b1a2381ae9e6c124f469c20c68532`。这是历史代码片段的指纹，不是完整源码文件摘要；本轮没有仅以先前报告结论代替代码核对。

## 指定 OPEN 项逐项判定

| 编号 | 判定 | 理由与定位 |
|---|---|---|
| C01 · P2 · 剩余条件 | **CLOSED** | 正文 L95 已实际补入基础 ID → 普通 chat 的 `chatcmpl-` 外部 ID → 随机后缀内部 ID 加工链，注明 `request.request_id` 作为 default、多 prompt 的子请求后缀，并以 `H` / `chatcmpl-H` 区分原始头值与引擎外部 ID；有头与无头处理分开。来源记录 L37 与本轮修订摘要 L74 一致，前轮“来源已改而正文未改”的交付差异已消除。固定源码支持这条已核路径，详见下文。 |
| N02 · P2 | **CLOSED** | 正文 L68 已删除“缺结果/空结果另有 fallback”的保证，明确只有有效非 None 结果对象的空 `layout_info` 或比较式成立得到分支级证实，并指出判 None 前已有属性访问；缺失对象及查询异常/超时的端到端行为保留 unknown。来源记录 L35 与修订摘要 L75 同步，不再把后置 None 条件当作已有效处理的回退路径。详见下文。 |

### C01：正文已落实可证的 ID 加工链

[_base_request_id L1472–1481](https://github.com/vllm-project/vllm/blob/b17039bccc17b94a2ea107272ad7bc93508708df/vllm/entrypoints/openai/serving_engine.py#L1472-L1481)优先返回非 None 的输入头值；否则使用传入 default，只有 default 为 None 才另生成。正文现在将这一层称为基础 ID，并在[chat L338–357](https://github.com/vllm-project/vllm/blob/b17039bccc17b94a2ea107272ad7bc93508708df/vllm/entrypoints/openai/serving_chat.py#L338-L357)的范围内说明 `request.request_id` 及前缀加工，不再把基础 ID 直接当作引擎外部 ID。后续[调用 L386–427](https://github.com/vllm-project/vllm/blob/b17039bccc17b94a2ea107272ad7bc93508708df/vllm/entrypoints/openai/serving_chat.py#L386-L427)使用加工后的子请求 ID；多 prompt 时附加索引后缀的限定也保留。

[InputProcessor L433–444](https://github.com/vllm-project/vllm/blob/b17039bccc17b94a2ea107272ad7bc93508708df/vllm/v1/engine/input_processor.py#L433-L444)先保存传入 ID 为 external ID，再追加随机后缀形成 internal ID。正文 L95 据此补出的第三级与原始回包一致；[OutputProcessor L393–456](https://github.com/vllm-project/vllm/blob/b17039bccc17b94a2ea107272ad7bc93508708df/vllm/v1/engine/output_processor.py#L393-L456)的 external→internal 映射也没有被误写成原始 HTTP 头→internal 的直接映射。

对普通单 prompt、单样本 chat，在[响应中间件启用](https://github.com/vllm-project/vllm/blob/b17039bccc17b94a2ea107272ad7bc93508708df/vllm/entrypoints/openai/api_server.py#L940-L941)且输入头为 `H` 时，响应头为 `H`，引擎外部 ID 为 `chatcmpl-H`。无输入头时，[中间件 L715–726](https://github.com/vllm-project/vllm/blob/b17039bccc17b94a2ea107272ad7bc93508708df/vllm/entrypoints/openai/api_server.py#L715-L726)生成响应头 ID，服务入口则独立选取基础 ID；不能假定响应中间件生成值已被传入引擎。正文已明确两处处理有别，且没有用末尾完整对应关系的 unknown 替代前述已知路径。

本项关闭不扩展到其他 endpoint、代理透传或所有跨层日志字段的对应关系；这些仍未取证，不要求为关闭 C01 补查全部入口。

### N02：按实际执行顺序收缩回退保证

固定[routing_logic.py L347–373](https://github.com/vllm-project/production-stack/blob/20a658044af0dea70e9e0136494bb9979cfd9fab/src/vllm_router/routers/routing_logic.py#L347-L373)在 L349 获得查询结果，L352 就读取其 `layout_info.keys()`，L358–361 才判断 None、空布局或命中不足。结果为 None 时，前置属性访问已不能正常通过，后面的 None 条件不证明正常回退。

有效结果对象且 `layout_info` 为空时，前置检查可以通过，后续空布局条件进入 session/QPS 回退；有效非空布局则可计算命中数，命中数比较式成立时进入同一分支。这是对局部控制流的静态判断，不是对控制器查询失败、路由成功或端到端可用性的保证。正文 L68 已按此限定，来源记录 L35 虽简写为“回退仅对有效非 None 结果对象证实”，同一行仍保留实际比较式及前置属性访问说明，未重新声称一切非 None 结果都会回退。

缺失结果对象、查询异常或超时最终如何传播、恢复，正文与来源记录均保留 unknown；本轮未修改上游代码、部署控制器或声称复现了故障，满足第二轮 N02 的关闭条件。

## 修订引入的新问题

在本轮指定修改及其相邻表述中，**未发现需要登记为 N03 或后续编号的新问题**。正文 L68 的空布局/缺失对象边界与来源记录 L35 一致；正文 L95 的已核 chat 加工链与来源记录 L37/L74 一致，原始 HTTP 头值、基础 ID、引擎外部 ID、内部 ID 的责任没有重新混淆。

来源记录 L52/L66/L68 等更早修订轮摘要保留历史措辞；其后 L72–75 明确记录本次更正，现行主张表与正文已同步。未把历史摘要当作当前行为保证，也未因其保留而重开已关闭项。

## 检查与交付边界

入场独立执行 `make check`；报告落盘后，在临时完整文件副本 `/var/folders/bk/3f4npkcs6l30twg9ph23c2jh0000gn/T/t07-08-recheck3-56h5i44o/checks` 执行 `make check`、`make build`，均为 **PASS: 117 content entries; 553 sources**，两条命令退出码均为 0，并成功生成两个 catalog 文件。副本保留既有 `build/` 文件以满足仓库原有链接，重新生成的产物仅写临时副本。

对入场记录的 603 份既有文件逐项比较 SHA-256，T07-08 正文、来源记录、registry 与既有复核报告均未变；唯一新增文件为本报告。期间检测到 `docs/research/batch-28-t07-11-sources.md`、`knowledge/07-inference/gpu-inference-oom-triage.md`、`knowledge/07-inference/ascend-inference-oom-triage.md` 发生非本轮写入的变动，本轮没有修改这些文件，也未将其变更纳入交付。正文复算摘要仍与提交值一致。

本报告不改变正文的 `draft / source_checked` 状态。结构检查与构建不证明技术语义、远端内容或硬件行为；本轮未部署、未压测，未修改 `src/kb/`，无需新增测试或执行 `make test`。
