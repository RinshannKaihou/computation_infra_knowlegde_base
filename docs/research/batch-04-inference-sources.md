# 第四批 F15/F16 来源核查与证据提取

本记录对应 `inference.execution-and-kv-cache` 与 `inference.latency-metrics`。它保存固定版本、实际读取位置、源码函数边界、可采用结论、未知项，以及供主任务合并到 `sources/registry.yaml` 的完整登记建议。它不是部署手册、性能报告或 GPU/NPU 兼容性声明。

交付日期为 2026-09-30。远端 tag、固定文件和动态 Prometheus 页面的实际解析/读取发生在 2026-09-29；下文保留真实观察日期，不把交付日期伪写为重新读取日期。

## 核查结论

F15/F16 的主样板固定为 vLLM `v0.14.0`，tag 解析到 commit `b17039bccc17b94a2ea107272ad7bc93508708df`。概念页使用同一提交中的 prefix caching 与 optimization 文档；指标页同时读取该提交的服务端统计、Prometheus logger 和 `bench serve` 客户端实现。这样可以把术语、默认值和函数语义约束在同一个版本，而不把 `latest` 页面或其他版本的行为拼入正文。

NPU 边界只采用 vLLM Ascend `v0.14.0rc1`，tag 解析到 commit `52d4acfa51fb868823d1070b81cbd2d97e9e4696`。该快照自己的 Sphinx 替换值是 vLLM `v0.14.1` 与 vLLM Ascend `v0.14.0rc1`，因此它**不是**本文上游 vLLM `v0.14.0` 快照的已验证配套。正文只用它说明该插件快照中 chunked prefill、automatic prefix caching 的标注及硬件/模型限制，不继承上游的全部能力，也不与其他 Ascend 案例拼成部署组合。

Prometheus histogram 聚合引用官方动态文档，读取日期为 2026-09-29。该页面没有在本轮固定到网站源 commit，因此只支持“先选窗口、对 bucket 求 rate、按保留 `le` 的维度聚合、再求 quantile；不能平均分位数”这类统计原则，不支持对未来 Prometheus 版本或任意兼容后端作无条件保证。

## backlog 身份与两页分工

| 任务 | 固定身份 | 正文职责 |
|---|---|---|
| F15 | `inference.execution-and-kv-cache`；`knowledge/07-inference/execution-and-kv-cache.md`；标题“推理执行与 KV cache” | 概念页。解释 prefill/decode、batch/scheduler、KV 容量压力、抢占重算、block 生命周期、前缀缓存与分块预填充边界；不写部署处方 |
| F16 | `inference.latency-metrics`；`knowledge/07-inference/latency-metrics.md`；标题“推理延迟与吞吐指标字典” | 参考页。固定 TTFT、TPOT、ITL、E2E、goodput 和 tokens/s 的单位、起止点、对象、窗口、失败过滤与聚合；同时列出客户端/服务端差异 |

F15 只建立执行模型。F16 引用 F15 的阶段边界，并把每个观测量绑定到具体计时器和统计对象；F16 不反过来把指标名称当作执行机制的证明。

## vLLM v0.14.0：实际读取位置

### 版本与许可证

| 文件 | 固定位置 | 核对内容 |
|---|---|---|
| release | <https://github.com/vllm-project/vllm/releases/tag/v0.14.0> | tag `v0.14.0` 指向 `b17039bccc17b94a2ea107272ad7bc93508708df` |
| repository | <https://github.com/vllm-project/vllm/tree/b17039bccc17b94a2ea107272ad7bc93508708df> | 本轮全部 vLLM 文件的共同固定快照 |
| LICENSE | <https://github.com/vllm-project/vllm/blob/b17039bccc17b94a2ea107272ad7bc93508708df/LICENSE> | 仓库根 Apache License 2.0 |
| pyproject | <https://github.com/vllm-project/vllm/blob/b17039bccc17b94a2ea107272ad7bc93508708df/pyproject.toml#L17-L20> | source package metadata 声明 `Apache-2.0` 并列出 `LICENSE`；本轮没有下载 wheel 或检查制品 notices |

### F15：执行与缓存

| 文件 | 精确范围 | 提取内容 |
|---|---|---|
| prefix caching design | [`docs/design/prefix_caching.md` 5–26](https://github.com/vllm-project/vllm/blob/b17039bccc17b94a2ea107272ad7bc93508708df/docs/design/prefix_caching.md#L5-L26) | block hash 包含 parent hash、block tokens 与 extra hashes；只缓存完整 block；哈希碰撞与 SHA256 的版本特定说明 |
| prefix caching design | [119–150](https://github.com/vllm-project/vllm/blob/b17039bccc17b94a2ea107272ad7bc93508708df/docs/design/prefix_caching.md#L119-L150) | block pool/free queue/cache mapping；新请求查已计算 block、touch 引用、分配、复用与满 block 入缓存 |
| prefix caching design | [193–203](https://github.com/vllm-project/vllm/blob/b17039bccc17b94a2ea107272ad7bc93508708df/docs/design/prefix_caching.md#L193-L203) | request 结束释放顺序；free queue 头部 cached block 的 LRU 驱逐步骤 |
| optimization | [`docs/configuration/optimization.md` 10–28](https://github.com/vllm-project/vllm/blob/b17039bccc17b94a2ea107272ad7bc93508708df/docs/configuration/optimization.md#L10-L28) | KV 空间不足时抢占；容量恢复后重算；V1 默认 `RECOMPUTE`；文档调优建议仅属于该版本 |
| optimization | [30–48](https://github.com/vllm-project/vllm/blob/b17039bccc17b94a2ea107272ad7bc93508708df/docs/configuration/optimization.md#L30-L48) | chunked prefill 可与 decode 同批；V1 “whenever possible” 默认启用；decode 优先、token budget 与自动分块；TTFT/ITL 取舍是该版本文档的调优观察 |

F15 可以采用的结论：

1. prefill 处理已有 prompt 上下文并产生首个输出边界；decode 在已有 KV 状态上继续自回归生成。调度器按迭代组成活动 batch，batch 中请求不必处于同一阶段。
2. KV cache 是有容量的运行时资源。并发序列、上下文长度、模型层数/KV 头/维度、dtype、block 粒度、其他设备内存占用和后端实现共同决定可容纳状态；固定文档只证明 vLLM 的 block 管理与配置关系，不给出跨模型、跨后端的通用容量数字。
3. 固定 vLLM V1 在 KV block 不足时可抢占并在之后重算；这里的重算与 prefix-cache 驱逐不同：前者改变请求进度和 E2E，后者使已空闲 cached block 不能再复用。
4. prefix caching 只复用完整 block；共同前缀若只落在部分 block 中，不构成该实现的完整 block 命中。命中也只省去相应 prefix 的计算，不省去新 token 的 decode。
5. 固定 vLLM V1 的 chunked prefill 会先安排 pending decode，再用 `max_num_batched_tokens` 余量安排 prefill，超出余量的 prefill 自动分块。“whenever possible” 必须保留，不能写成所有模型/配置无条件开启。

F15 不应写入：固定数值的 KV 容量公式、通用 block 大小、推荐的 `gpu_memory_utilization`/batch/token budget、可复制启动命令、任何目标硬件的性能阈值，或“启用 prefix cache 一定降低 TTFT”之类无条件结论。

### F16：服务端统计实现

| 文件 | 精确范围 | 提取内容 |
|---|---|---|
| request state/stats | [`vllm/v1/metrics/stats.py` 193–230](https://github.com/vllm-project/vllm/blob/b17039bccc17b94a2ea107272ad7bc93508708df/vllm/v1/metrics/stats.py#L193-L230) | frontend wall-clock `arrival_time`；engine-core monotonic queued/scheduled/first/last token timestamp；finished request 字段 |
| per-iteration update | [252–305](https://github.com/vllm-project/vllm/blob/b17039bccc17b94a2ea107272ad7bc93508708df/vllm/v1/metrics/stats.py#L252-L305) | TTFT 相对 frontend arrival；`len(new_token_ids)`；首次 output 与后续 engine output 间隔 |
| finished request | [319–377](https://github.com/vllm-project/vllm/blob/b17039bccc17b94a2ea107272ad7bc93508708df/vllm/v1/metrics/stats.py#L319-L377) | first QUEUED→first SCHEDULED、first SCHEDULED→first NEW_TOKEN、first→last NEW_TOKEN、first SCHEDULED→last NEW_TOKEN；TPOT 分母 `generated_tokens-1`；这些阶段包含抢占 |
| metric declarations | [`vllm/v1/metrics/loggers.py` 573–616](https://github.com/vllm-project/vllm/blob/b17039bccc17b94a2ea107272ad7bc93508708df/vllm/v1/metrics/loggers.py#L573-L616) | prompt/generation token counters；`request_success` counter 按 finish reason 分标签 |
| latency histograms | [683–885](https://github.com/vllm-project/vllm/blob/b17039bccc17b94a2ea107272ad7bc93508708df/vllm/v1/metrics/loggers.py#L683-L885) | TTFT、deprecated `time_per_output_token`、ITL、request TPOT、E2E、queue/inference/prefill/decode 均为 histogram |
| observations | [1109–1163](https://github.com/vllm-project/vllm/blob/b17039bccc17b94a2ea107272ad7bc93508708df/vllm/v1/metrics/loggers.py#L1109-L1163) | token counter 增量；TTFT/ITL 逐 observation；finish reason counter 与各 finished-request histogram |
| finish reasons | [`vllm/v1/engine/__init__.py` 26–43](https://github.com/vllm-project/vllm/blob/b17039bccc17b94a2ea107272ad7bc93508708df/vllm/v1/engine/__init__.py#L26-L43) | `STOP`、`LENGTH`、`ABORT`、`ERROR`；ABORT 为客户端取消，ERROR 示例包含 KV load failure |
| abort path | [`output_processor.py` 393–456](https://github.com/vllm-project/vllm/blob/b17039bccc17b94a2ea107272ad7bc93508708df/vllm/v1/engine/output_processor.py#L393-L456) | 外部 ID 取消产生 `FinishReason.ABORT` final output |
| finished-stat path | [696–713](https://github.com/vllm-project/vllm/blob/b17039bccc17b94a2ea107272ad7bc93508708df/vllm/v1/engine/output_processor.py#L696-L713) | 正常 processed finish 调用 `update_from_finished_request`；本轮没有证明所有取消路径都进入同一 histogram/counter |

服务端术语边界：

- TTFT 使用 engine request arrival 到 frontend 接收首批相关 outputs 后创建的 iteration wall-clock。常规 OpenAI chat/completion 默认起点晚于已完成的 HTTP/prompt/chat 预处理，终点包含 engine→frontend IPC/等待；显式 arrival 的其他路径需另查。
- 服务端 ITL 每次后续 engine output update 产生一个 observation。实现同时用 `len(new_token_ids)` 增加 token 数，所以 speculative decoding 或一次 update 含多个 token 时，ITL 不能自动解释为逐 token 间隔。
- request TPOT 是该请求 `decode_time/(num_generation_tokens-1)`；0/1 token 时为 0。旧的 `vllm:time_per_output_token_seconds` 在固定版本已标为 deprecated 且实际是 ITL；应使用 `inter_token_latency_seconds` 和 `request_time_per_output_token_seconds` 的精确名称。
- `vllm:request_success` 的名字不能替代 finish reason 语义。它按 STOP/LENGTH/ABORT/ERROR 标签计数，但外部取消是否在所有入口都进入 finished-request metrics 仍需代码追踪或实验确认。

### F16：客户端 `bench serve` 实现

| 文件 | 精确范围 | 提取内容 |
|---|---|---|
| completion endpoint | [`endpoint_request_func.py` 179–248](https://github.com/vllm-project/vllm/blob/b17039bccc17b94a2ea107272ad7bc93508708df/vllm/benchmarks/lib/endpoint_request_func.py#L179-L248) | `perf_counter` 在 POST 前开始；首个 `choices` SSE payload 设 TTFT；text 可为空；后续 payload 形成 ITL；无有效 chunk 判失败；latency 止于最后一个 `choices` payload |
| chat endpoint | [312–369](https://github.com/vllm-project/vllm/blob/b17039bccc17b94a2ea107272ad7bc93508708df/vllm/benchmarks/lib/endpoint_request_func.py#L312-L369) | HTTP 200 分支；首个 `choices` payload 设 TTFT；usage-only payload 也更新末时间；该分支未像 completion 一样要求至少一个有效 choices 才标 success |
| success filtering and token count | [`serve.py` 404–445](https://github.com/vllm-project/vllm/blob/b17039bccc17b94a2ea107272ad7bc93508708df/vllm/benchmarks/serve.py#L404-L445) | 只对 `success` 输出纳入 TTFT/ITL/TPOT/E2E；usage 缺失时 tokenizer 回算可能轻微高估；TPOT 仅 `output_len>1` 进入分布，goodput 用的 all_tpots 对 0/1 token 置 0 |
| goodput and failures | [447–489](https://github.com/vllm-project/vllm/blob/b17039bccc17b94a2ea107272ad7bc93508708df/vllm/benchmarks/serve.py#L447-L489) | 同一成功请求须满足所有已配置 SLO；失败请求单独计数 |
| throughput and percentiles | [550–583](https://github.com/vllm-project/vllm/blob/b17039bccc17b94a2ea107272ad7bc93508708df/vllm/benchmarks/serve.py#L550-L583) | request/output/total-token throughput 分子；NumPy percentile；ITL 列表是所有成功请求 interval 的扁平集合 |
| preflight/warmup | [617–712](https://github.com/vllm-project/vllm/blob/b17039bccc17b94a2ea107272ad7bc93508708df/vllm/benchmarks/serve.py#L617-L712) | 函数签名 ready-check 默认 600；ready check 与可选 warmup 都在主测量前，使用同一个 test input |
| main window | [763–845](https://github.com/vllm-project/vllm/blob/b17039bccc17b94a2ea107272ad7bc93508708df/vllm/benchmarks/serve.py#L763-L845) | benchmark window 从创建主请求前开始，到所有 tasks gather 后结束，包含合成 arrival delay 与并发等待 |
| CLI defaults | [1202–1213](https://github.com/vllm-project/vllm/blob/b17039bccc17b94a2ea107272ad7bc93508708df/vllm/benchmarks/serve.py#L1202-L1213), [1271–1307](https://github.com/vllm-project/vllm/blob/b17039bccc17b94a2ea107272ad7bc93508708df/vllm/benchmarks/serve.py#L1271-L1307), [1361–1395](https://github.com/vllm-project/vllm/blob/b17039bccc17b94a2ea107272ad7bc93508708df/vllm/benchmarks/serve.py#L1361-L1395), [1489–1496](https://github.com/vllm-project/vllm/blob/b17039bccc17b94a2ea107272ad7bc93508708df/vllm/benchmarks/serve.py#L1489-L1496) | max concurrency optional；request rate 默认 inf；warmup 默认 0；生成任务默认 percentile metrics 为 TTFT/TPOT/ITL、percentile 默认 p99；CLI ready check 默认 0 |
| CLI forwarding | [1654–1678](https://github.com/vllm-project/vllm/blob/b17039bccc17b94a2ea107272ad7bc93508708df/vllm/benchmarks/serve.py#L1654-L1678) | CLI 值显式传入 `benchmark()`；因此命令行实际默认是 ready check 0，不是函数签名 600 |

客户端术语边界：

1. “首个输出”是首个可解析且含 `choices` 的 SSE payload，不保证等于一个非空 token。payload 可以为空，也可能捆绑多个 token。
2. completion 与 chat endpoint 的结束边界不同：completion 的 latency 不随 usage-only/[DONE] 更新；chat 的 usage-only payload 会更新末时间。正文必须写明 endpoint，而不能给整个工具一个虚构的统一 E2E 边界。
3. 请求级 TTFT、TPOT、E2E 的百分位样本单位是成功请求；ITL 的百分位样本单位是扁平化的成功请求 chunk 间隔，因此长输出或 chunk 更多的请求权重更高。
4. 失败请求、HTTP 非 200 与异常不进入这些 latency 分布，也不进入 token throughput 分子。报告 latency 分位数时必须同时给出 attempted/completed/failed/cancelled 或可得的对应计数，避免幸存者偏差。
5. `num_warmups=0` 和 ready check 0 是 CLI 默认。显式开启时，它们不计入主 benchmark window，却会改变连接、编译、模型或 prefix-cache 状态；工具没有在所读路径中自动清空 prefix cache。

## Prometheus histogram：动态官方边界

实际读取：

- <https://prometheus.io/docs/practices/histograms/>：histogram bucket 可聚合，summary 的预计算 quantile 不可聚合；不能平均分位数。
- <https://prometheus.io/docs/prometheus/latest/querying/functions/#histogram_quantile>：classic histogram 的聚合示例先对目标窗口取 `rate`，再 `sum by (..., le)`，最后调用 `histogram_quantile()`；bucket 内分位数是插值估计。

F16 可以写“分位数必须同时记录窗口、样本对象、筛选条件、标签聚合和 bucket schema”。对 vLLM 服务端 classic histograms，跨实例整体 p99 需要在共同窗口内合并兼容 buckets 后计算；不能平均实例 p99。客户端 `bench serve` 的 NumPy percentile 是一次 benchmark 完成后的样本数组统计，不使用 Prometheus bucket，二者不可直接视为同一种 p99。

动态限制：以上 URL 指向 current/latest 官方文档，2026-09-29 已直接读取，但本轮没有把网页映射到 `prometheus/docs` 的固定源 commit。未来页面、native histogram 行为和兼容后端可能变化；正式条目应保留读取日期，并避免复制未固定版本的命令作为处方。

## vLLM Ascend v0.14.0rc1：实际读取与冲突记录

| 文件 | 精确范围 | 提取内容 |
|---|---|---|
| release | <https://github.com/vllm-project/vllm-ascend/releases/tag/v0.14.0rc1> | tag `v0.14.0rc1` 指向 `52d4acfa51fb868823d1070b81cbd2d97e9e4696` |
| Sphinx config | [`docs/source/conf.py` 62–80](https://github.com/vllm-project/vllm-ascend/blob/52d4acfa51fb868823d1070b81cbd2d97e9e4696/docs/source/conf.py#L62-L80) | 实际 substitution：`vllm_version=v0.14.1`、`vllm_ascend_version=v0.14.0rc1`、pip 版本 0.14.1/0.14.0rc1、CANN image tag 8.5.0、CI vLLM 0.14.1 |
| feature matrix | [`supported_features.md` 7–33](https://github.com/vllm-project/vllm-ascend/blob/52d4acfa51fb868823d1070b81cbd2d97e9e4696/docs/source/user_guide/support_matrix/supported_features.md#L7-L33) | chunked prefill 与 APC 标为 Functional；legend 说明状态；只采纳固定表格，不用其 `latest` 外链补写能力 |
| README requirements | [`README.md` 49–56](https://github.com/vllm-project/vllm-ascend/blob/52d4acfa51fb868823d1070b81cbd2d97e9e4696/README.md#L49-L56) | 固定快照列出的 Atlas A2/A3、300I Duo experimental、Python/CANN/PyTorch/torch-npu 要求 |
| release notes | [`release_notes.md` 3–12](https://github.com/vllm-project/vllm-ascend/blob/52d4acfa51fb868823d1070b81cbd2d97e9e4696/docs/source/user_guide/release_notes.md#L3-L12) | release candidate；310P 仅 basic dense/VL 且 eager mode；功能条目只属于此 RC |
| version policy | [`versioning_policy.md` 24–27](https://github.com/vllm-project/vllm-ascend/blob/52d4acfa51fb868823d1070b81cbd2d97e9e4696/docs/source/community/versioning_policy.md#L24-L27) | 同一 commit 的表格写成 `v0.14.1rc1` 对 vLLM 0.14.0/0.14.1，与 tag/conf 的 `v0.14.0rc1` 不一致 |
| package metadata | [`setup.py` 475–492](https://github.com/vllm-project/vllm-ascend/blob/52d4acfa51fb868823d1070b81cbd2d97e9e4696/setup.py#L475-L492) | package 名 `vllm_ascend`；license `Apache 2.0` 与 classifier；未下载 wheel |
| LICENSE | <https://github.com/vllm-project/vllm-ascend/blob/52d4acfa51fb868823d1070b81cbd2d97e9e4696/LICENSE> | 仓库根 Apache License 2.0 |

这里不能把 Markdown 中的替换变量当作版本字面量。本轮读取了生成 substitutions 的固定 `conf.py`，得到上述具体值。固定 version policy 又出现 `v0.14.1rc1`/`v0.14.0rc1` 标注冲突，因此正文采用更窄表述：该 tag 的文档构建变量指向 vLLM 0.14.1；本轮未安装或验证此组合。其他固定页面存在版本冲突，本轮不能据此确认与主样板 vLLM 0.14.0 的配套；保留未知，不作排除兼容性的声明。

feature matrix 的 “Functional” 只说明该插件快照的项目状态，不证明每个模型、硬件、dtype、graph/eager 模式与参数组合都支持。release notes 对 310P 的限制必须同时保留。APC 行链接到 GitHub issue；本轮没有用 issue 的 open/closed 状态作为修复或支持证据。

## F16 建议采用的指标字典骨架

| 名称 | 样本对象与单位 | 起止点 | 默认/例外必须写清 |
|---|---|---|---|
| TTFT | request，秒或毫秒 | 服务端：engine request arrival→frontend 接收首批相关 outputs 后的 iteration wall-clock；客户端：POST 前→首个含 `choices` 的 SSE payload | 首 payload 可空或多 token；客户端含网络/代理/解析，服务端不含返回网络 |
| TPOT | request，秒/token 或毫秒/token | `(E2E-TTFT)/(generated_tokens-1)` 或服务端 `decode/(tokens-1)` | 0/1 token 边界；client distribution 排除，goodput 置 0；server request histogram 置 0 |
| ITL | emission/update interval，秒或毫秒 | 相邻可观察输出之间 | client 是 chunk interval 且扁平聚合；server 是 engine output update interval；均不保证一 observation 等于一 token |
| E2E/E2EL | request，秒或毫秒 | 客户端 endpoint 特定；服务端 engine request arrival→接收 finished 相关 outputs 后的 iteration wall-clock | completion/chat 客户端终点不同；服务端与客户端窗口不可直接相减解释网络 |
| request throughput | 完成请求/秒 | 成功完成数 ÷ 主 benchmark duration | 不等于 attempted arrival rate；失败/取消的分母处理要单列 |
| output token throughput | 输出 token/秒 | 成功请求的实际/回算输出 token 总数 ÷ duration | usage 缺失时 tokenizer 回算可能偏差；失败输出长度置 0 |
| total token throughput | 输入+输出 token/秒 | 成功请求 token 总和 ÷ duration | 不等于 decode-only 吞吐，也不等于服务端 counter 的任意瞬时 rate |
| goodput | 满足全部已配置 SLO 的成功请求/秒 | good completed ÷ duration | 仅在显式配置 TTFT/TPOT/E2E 阈值时有定义；阈值单位 ms；必须报告 SLO 集合 |
| percentile | 依指标而定 | 一次客户端 run 的样本数组，或服务端某个 rate window 的 histogram buckets | 记录 p 值、窗口、对象、失败筛选、聚合标签、bucket；不能平均 p99 |

## 未知项与后续验证

- vLLM 服务端 `request_success` 是否覆盖每一种客户端取消入口、断连时机和 KV connector/load error 路径，本轮没有完整证明；固定 enum 与部分路径只能支持分类词汇。
- server frontend arrival、engine output、HTTP serialization、proxy flush 与客户端 SSE parsing 之间没有单一共享时钟；没有 tracing 时不能把两个 TTFT 相减当作精确网络时间。
- benchmark 的 prefix/model/allocator 热状态、连接池、编译状态、请求前缀重复度和 cache salt 必须由运行记录补齐；`num_warmups=0` 不能证明 cold cache，显式 warmup 也不能证明 steady state。
- speculative decoding、stream chunk coalescing、tokenizer 回算、usage payload 和非 OpenAI endpoint 可改变“一个 chunk/engine update 对应多少 token”；不能用 ITL 样本数反推 token 数。
- vLLM Ascend 的固定 feature status 没有验证本文目标模型和硬件；310P 有 release-note 限制，A2/A3/300I Duo 仍需查固定 model matrix 与目标软件栈，并在真实 NPU 上实验。
- 本轮没有吞吐、延迟、cache hit、eviction、preemption、错误、取消或 goodput 实测数据，也没有任何通用阈值。

## 完整来源登记建议

以下条目符合 `schemas/sources.schema.json`，供主任务合入共享 `sources/registry.yaml`。本任务按约束不直接修改 registry。

```yaml
- id: src.vllm.inference-v0-14
  title: vLLM v0.14.0 推理执行、指标与服务基准固定快照
  url: https://github.com/vllm-project/vllm/tree/b17039bccc17b94a2ea107272ad7bc93508708df
  kind: repository
  registered_at: "2026-09-30"
  revision: b17039bccc17b94a2ea107272ad7bc93508708df
  license:
    status: partial
    scopes:
      - scope: 固定 commit 的仓库源码与随附文档；带独立声明的文件和第三方内容另计
        identifier: Apache-2.0
        url: https://github.com/vllm-project/vllm/blob/b17039bccc17b94a2ea107272ad7bc93508708df/LICENSE
      - scope: 固定 commit 的 Python source package metadata；声明 Apache-2.0 并列入 LICENSE
        identifier: Apache-2.0
        url: https://github.com/vllm-project/vllm/blob/b17039bccc17b94a2ea107272ad7bc93508708df/pyproject.toml#L17-L20
    notes: 仓库根许可与 source package metadata 已直接核对。未下载 wheel、容器或其他发行制品，未核验其第三方 notices；docs.vllm.ai 的生成站点没有作为独立再分发许可依据。
  notes: tag v0.14.0 解析到此 commit。已读取 prefix caching、optimization、v1 metrics stats/loggers、engine finish/abort 路径及 bench serve 客户端实现；仅支持该版本的概念与口径，不构成部署建议或硬件兼容性声明，未构建、安装或运行。
```

```yaml
- id: src.ascend.vllm-ascend-v0-14-0rc1
  title: vLLM Ascend v0.14.0rc1 固定源码与文档快照
  url: https://github.com/vllm-project/vllm-ascend/tree/52d4acfa51fb868823d1070b81cbd2d97e9e4696
  kind: repository
  registered_at: "2026-09-30"
  revision: 52d4acfa51fb868823d1070b81cbd2d97e9e4696
  license:
    status: partial
    scopes:
      - scope: 固定 commit 的仓库源码与随附文档；带独立声明的文件和第三方内容另计
        identifier: Apache-2.0
        url: https://github.com/vllm-project/vllm-ascend/blob/52d4acfa51fb868823d1070b81cbd2d97e9e4696/LICENSE
      - scope: 固定 commit 的 Python source package metadata；setup.py 声明 Apache 2.0
        identifier: Apache-2.0
        url: https://github.com/vllm-project/vllm-ascend/blob/52d4acfa51fb868823d1070b81cbd2d97e9e4696/setup.py#L475-L492
    notes: 仓库根许可与 source package metadata 已直接核对。未下载 wheel、容器、CANN/HDK/torch-npu 包或其第三方 notices；生成网站和外链材料的许可另计。
  notes: tag v0.14.0rc1 解析到此 commit。固定 conf.py 的 substitutions 指向 vLLM v0.14.1、vLLM Ascend v0.14.0rc1 与 CANN image tag 8.5.0；PyTorch/torch-npu 2.9.0 来自固定 README requirements；同 commit 的 version policy 存在 v0.14.1rc1 标注冲突。仅用于插件快照的 feature/hardware/model 边界，不与本文上游 vLLM v0.14.0 拼成配套，未安装或运行。
```

```yaml
- id: src.prometheus.histograms-2026-09-29
  title: Prometheus 官方 histogram 与 quantile 聚合文档（2026-09-29 读取）
  url: https://prometheus.io/docs/practices/histograms/
  kind: documentation
  registered_at: "2026-09-30"
  revision: "retrieved 2026-09-29; dynamic current documentation"
  license:
    status: partial
    scopes:
      - scope: prometheus/docs 仓库中的网站文档源码；main 为可变定位
        identifier: Apache-2.0
        url: https://github.com/prometheus/docs/blob/main/LICENSE
    notes: 官方文档仓库 README 与 LICENSE 标为 Apache-2.0；本轮未把读取网页解析到固定源 commit。网站构建依赖、外链材料和 Prometheus 发行包不由此范围覆盖。
  notes: 同时读取 https://prometheus.io/docs/prometheus/latest/querying/functions/#histogram_quantile 。仅用于 histogram bucket、rate window、聚合维度、quantile 插值和“不可平均分位数”的统计边界；页面是动态 current/latest 文档，正式引用保留读取日期。
```

## 执行与验证边界

本轮只读取固定 GitHub 文件和官方网页。没有克隆上游仓库、下载发行包、安装依赖、构建或运行 vLLM/vLLM Ascend/Prometheus；没有访问 GPU、NPU、模型服务或集群；没有发起推理、warmup、cache load、取消、故障注入或 benchmark。因此 `source_checked` 只表示上述文件和函数语义已核对，不表示任何性能、兼容性、默认部署行为或目标环境结果已经实验验证。

## 第四批审阅后的计时调用链补查

实际入口、默认 arrival、输出接收和时钟分域的固定源码定位见[独立审阅 R2](batch-04-astra-review.md)。正文与第五批推理总览已同步，不能继续将 engine frontend arrival 简写为 HTTP 到达。
