# Batch 28 · T07-10 第二轮定向复核报告

## 会话元数据与结论

| 项目 | 记录 |
|---|---|
| 角色与范围 | 承接[第一轮定向复核](batch-28-t07-10-codex-recheck.md)的独立审阅者，仅复核 OPEN 项 C02/C03/C06/C07 剩余条件与 N01，并检查这些修订引入的问题；未编写或修改被审正文 |
| 实际执行模型 / 档位 | `gpt-6.1-sol / xhigh` |
| 模型核验 | 读取 `CODEX_THREAD_ID` 对应本地会话 JSONL；第 8 行 `turn_context`（`2026-10-21T08:01:29.480Z`）实见 `model=gpt-6.1-sol`、`effort=xhigh`，与 `collaboration_mode.settings` 一致；本轮未另启模型、审阅 CLI 子进程或子代理，assistant 文本未检出模型回退标记 |
| 会话 ID | `01a15d7a-8577-7d92-b2ed-f04b897798d7` |
| 执行方式 | 本地 Codex CLI，`originator=codex_exec`、`source=exec`、`cli_version=0.163.0`；静态定向复核 |
| 日期 / 时区 | 2026-10-21 / Asia/Shanghai |
| 工作目录 | `/Users/ywang2397/work/AI_reliability_knowledge_base` |
| 修订正文 | [release-and-recovery.md](../../knowledge/07-inference/release-and-recovery.md)，109 行；下文正文行号绑定此版 |
| 作者提交的正文 SHA-256 | `c5018d2c94701777f3829a54a6ad62b24660fb004ec25eba608fa48a72807eb4` |
| 独立计算的正文 SHA-256 | `c5018d2c94701777f3829a54a6ad62b24660fb004ec25eba608fa48a72807eb4`，**匹配** |
| 来源记录 SHA-256 | `7f7dfe7bf052ef527bfc3474fb1877989d4327b6f29404011560a564d63803be` |
| registry 取样 SHA-256 | `a87cd520ba611ef258ab7310359280b192b5d76721265ce4de3876e0950ab605` |
| 写入范围 | 仅新增本报告；不修改正文、来源记录、registry、导航、计划或审核状态；构建在临时副本执行 |

**结论：本轮五项全部 CLOSED（C02/C03/C06/C07/N01），OPEN=0；未发现需另立 N02 或后续编号的新问题。开放 P1=0、P2=0、P3=0。T07-10 在初审及两轮定向复核所覆盖的范围内通过。**

前轮已经关闭的 C01/C04/C05/C08/C09/C10/C11 沿用其状态，本轮不重新初审。此结论不构成 Batch 28 整批验收，不改变正文 `draft / source_checked` 状态，也不证明部署兼容、自动排空、缓存恢复契约或硬件验证。

## 方法与证据边界

已读取仓库 `AGENTS.md`、[README](../../README.md)、[写作指南](../authoring-guide.md)、[内容总目录](../../content-outline.md)、元数据 schema 和 [T07-10 验收要求](../../plans/full-coverage-backlog.yaml)；重读[初审](batch-28-t07-10-codex-review.md)中相关关闭条件、第一轮的最小剩余条件、修订正文、[来源记录](batch-28-t07-10-sources.md)及 [registry](../../sources/registry.yaml)相关摘要。修订说明用于定位，逐项判定以实际文件和证据为准。[缓存身份边界](../../knowledge/07-inference/execution-and-kv-cache.md#prefix-cache-的复用边界)仅用于核对 C06 的既有条件，不扩展为其他条目的初审。

远端复取未成功：GitHub 文件工具返回不可用；网页工具请求固定 GitHub 文件页时返回 HTTP 429；终端读取 KServe 固定 raw URL 因 DNS 解析失败未取得内容。因此本轮证据是**既有固定快照缓存的重新读取与哈希核对**，不记作本轮新取得的远端页面，也不以第一轮结论代替源码读取。

| 缓存文件 | SHA-256 前 16 位 | 本轮读取范围 |
|---|---|---|
| `/tmp/b28/vllm/api_server.py` | `dcc6b46ca859074d` | L117–143、L206–234、L1290–1306、L1340–1376；关闭责任和局部顺序 |
| `/tmp/b28/vllm/core.py` | `a7a624e0ed151f00` | L913–947；启动失败与运行期异常分支 |
| `/tmp/b28/vllm/core_client.py` | `601d375067fa724e` | L410–435、L580–625；marker 接收与 sentinel guard/监控 |
| `/tmp/b28/vllm/vllm_v1_engine_async_llm.py` | `818af4561b7ae54a` | L448–464；EngineDead 分支与准确锚点 |
| KServe generative `llmisvc/canary-rollout.md` | `89013ecf8dec6244` | L16–75、L225–295；比例权重、Ready 回退与直达路径 |

vLLM pin 为 `b17039bccc17b94a2ea107272ad7bc93508708df`；KServe 文件位于 `/tmp/b28/kserve-web/docs/model-serving/generative-inference/llmisvc/`，pin 为 `3f4067ea87dd84194bddb1b563051c84306c7997`。上述摘要均与前轮记录一致。源码定位使用缓存原文件行号，不使用网页转换行号；缓存身份一致不单独证明远端 tag 解析、完整版本配套或运行成功。本轮没有扩查完整 `serve_http`/uvicorn、KServe 控制器或 worker→core 传播实现。

## OPEN 项逐项判定

| 编号 / 原优先级 | 判定 | 理由与证据 |
|---|---|---|
| C02 · P2 | **CLOSED** | 来源记录 L25 已就地替换为四项分立事实：初始化 SIGTERM 抛 KeyboardInterrupt；lifespan 取消统计任务并清 `app.state`，不调用引擎 shutdown；外层 engine client 上下文 finally 调用 `async_llm.shutdown()`；退出 backend 上下文后才 await HTTP shutdown task。与正文 L59、verification notes L37 及 registry 的责任归属相容，来源 L41/L54 也与此一致。EngineDead 锚点为 `async_llm.py` L455–459。完整 HTTP 关闭和在途流终态继续 unknown，未把局部已知顺序全列为未知，也未从中推出自动 drain。 |
| C03 · P2 | **CLOSED** | 正文 L61 已明确“Ready 即按保留权重接流”，并说明样板未提供等待发布者预热/质量核对的额外机制。要求接流前 gate 的方案现将经核对的 readiness 准入门或入口隔离列为另行前提，要求 gate 期间阻止组内及直达路径提前选中旧版、通过后放开并核对实际流量，未实现则记录缺失；先接流的方案明确为带流验证，需预登记预算/停止条件。旧版运行/已停两分支、9:9 仍为 50/50、达到回退目标需再调权重、冷启动计入窗口及坏版本直达路径隔离均保留。未发明 KServe 字段或把待实现 gate 写成已部署能力。 |
| C06 · P2 | **CLOSED** | 来源记录 unknown 3（L34）已替换为所有者分列的现行口径：仅终止进程的本地活动 KV/prefix cache 不自动继承；外部/offload 与远端 KV 的幸存、重挂载、身份兼容和会话恢复契约按实现核对，无证据即 unknown；不把 PD/offload 路径当恢复能力边界，也不判重拉必冷。与正文 L77/L88 及来源 L45/L56 一致，实际命中与缓存身份仍需记录，TTFT 仍只作联合观察。无需用部署实测消除这些合理未知才能关闭本措辞与一致性问题。 |
| C07 · P2 | **CLOSED** | 来源记录 L25 已分列启动失败仅日志/异常、运行期异常发送 marker、突然退出由条件启用的 sentinel 监控处理三种路径。正文 L68 补出已可核 guard：`resources.engine_manager` 非空、具有 `processes` 属性且其集合非空，否则返回而不启动监控线程；随后监控可置 `engine_dead` 并关闭 client，不依赖先收到 marker。部署是否满足 guard、worker→core 完整传播仍列 unknown；缺 marker 不能排除死亡、EngineDead 不区分 OOM/驱动/内部根因的限定保留。 |
| N01 · P2 | **CLOSED** | 正文 L57 已改为“本流程不假设引擎会自动排空在途流”，同时明确完整 `serve_http`/uvicorn 关闭行为与在途流终态仍待核实。它表达流程不依赖未经证明的能力，与正文 L59/L97、来源 unknown 2（L33）一致，已消除“不自动排空”的否定事实断言；六步 drain 清单、预算和缺失部署前提仍保留。关闭不要求反向证明自动 drain 成立。 |

C02 的精确上游依据为 [lifespan L117–143](https://github.com/vllm-project/vllm/blob/b17039bccc17b94a2ea107272ad7bc93508708df/vllm/entrypoints/openai/api_server.py#L117-L143)、[engine context L229–232](https://github.com/vllm-project/vllm/blob/b17039bccc17b94a2ea107272ad7bc93508708df/vllm/entrypoints/openai/api_server.py#L229-L232)、[初始化 handler L1296–1300](https://github.com/vllm-project/vllm/blob/b17039bccc17b94a2ea107272ad7bc93508708df/vllm/entrypoints/openai/api_server.py#L1296-L1300)、[HTTP task 等待 L1371–1373](https://github.com/vllm-project/vllm/blob/b17039bccc17b94a2ea107272ad7bc93508708df/vllm/entrypoints/openai/api_server.py#L1371-L1373)及 [EngineDead L455–459](https://github.com/vllm-project/vllm/blob/b17039bccc17b94a2ea107272ad7bc93508708df/vllm/v1/engine/async_llm.py#L455-L459)。这些位置支持局部责任分工，不回答完整在途流终态。

C03 对照固定 [回退段 L241–257](https://github.com/kserve/website/blob/3f4067ea87dd84194bddb1b563051c84306c7997/docs/model-serving/generative-inference/llmisvc/canary-rollout.md#L241-L257)、[比例权重 L19–28](https://github.com/kserve/website/blob/3f4067ea87dd84194bddb1b563051c84306c7997/docs/model-serving/generative-inference/llmisvc/canary-rollout.md#L19-L28)及 [直达路径 L271–287](https://github.com/kserve/website/blob/3f4067ea87dd84194bddb1b563051c84306c7997/docs/model-serving/generative-inference/llmisvc/canary-rollout.md#L271-L287)。9:9 恢复后约一半流量是依照文档比例语义的条件推导，未声称本地测得。接流前 gate 是正文新增的部署前提，不归为已核 KServe 内置保证。

C07 对照固定 [core.py L931–943](https://github.com/vllm-project/vllm/blob/b17039bccc17b94a2ea107272ad7bc93508708df/vllm/v1/engine/core.py#L931-L943)、[marker 接收 L425–428](https://github.com/vllm-project/vllm/blob/b17039bccc17b94a2ea107272ad7bc93508708df/vllm/v1/engine/core_client.py#L425-L428)及 [monitor L583–621](https://github.com/vllm-project/vllm/blob/b17039bccc17b94a2ea107272ad7bc93508708df/vllm/v1/engine/core_client.py#L583-L621)。列出必要局部 guard 不代表所有部署均会进入该路径，也不证明所有 worker 故障都能产生同一条传播链。

## 修订引入的新问题

本轮范围内**未发现需要新增 N02 或后续编号的问题**。来源主表和 unknown 3 已实际替换，末尾摘要不再是支撑这两项修订的唯一位置；来源记录 L38–50 为“初审修订轮”的历史摘要，L52–58 为第一轮复核后的补充，现行正文 L61 明确了 Ready 与 gate 的关系。未把历史摘要中简写的“Ready/gate”作为当前实现保证，也未要求追改前轮审阅报告。

新增 guard 与源码分支相符；新增 gate 条件没有附加未经验证的命令、控制器保证或平台兼容承诺；N01 修订保留未知，没有反向宣称引擎一定能排空。来源核对缺口、部署前提与实验结果仍分别记录。本节只覆盖本次指定修订，不是其他正文或已关闭项的全量技术背书。

## 校验与写入范围

报告落盘后实跑 `PYTHONDONTWRITEBYTECODE=1 make check`，退出码为 0，结果为 **PASS: 117 content entries; 553 sources**。为遵守“只新增这一个文件”，将当前仓库复制到 `/tmp/t0710-recheck2-build-7jcskkvu/repo`，在副本中实跑 `make build`，退出码同为 0；成功生成两个 catalog，读取 JSON 确认 `documents=117`、`sources=553`。工作区 `build/` 未改写。

正文 18 处、本报告 10 处内联本地文件链接目标均存在；`git diff --check` 通过。上述检查仅验证结构、登记引用、本地链接和生成过程，不验证技术正确性、远端可达性、页内锚点语义或硬件兼容性。

取样前后文件摘要对照未见既有文件变化或删除；另观察到并行新增的 T07-09 第三轮报告，非本会话写入。本会话的仓库写操作仅新增本报告，未覆盖或回退其他工作。交付前再次计算正文与来源记录 SHA-256，均与元数据表相同；本地会话仍只见 `gpt-6.1-sol / xhigh` 的单一 `turn_context`，无另启审阅模型记录。

本轮不修改 `src/kb/`，无需新增或运行代码测试；未安装或运行上游服务代码，没有发布、重启/终止副本、修改路由或执行故障注入。环境档案仍为空，平台标签不证明共同兼容，未取得硬件实测证据。
