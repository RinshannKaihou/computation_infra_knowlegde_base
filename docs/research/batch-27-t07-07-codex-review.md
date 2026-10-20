# Batch 27 · T07-07 修订交付初审

## 会话元数据

- 审阅角色：AI 可靠性知识库批次审阅者；本轮审阅工作区未提交的 T07-07 修订交付，不替代 Batch 12 历史审阅。
- 实际执行模型：`gpt-6.1-sol`；实际推理档位：`xhigh`。
- 核验依据：`CODEX_THREAD_ID=01a15b23-445e-7891-bc37-a81b144c335f` 对应 CLI rollout 的 `session_meta.originator=codex_exec`、`source=exec`、`cli_version=0.163.0`；本轮 `turn_context.model=gpt-6.1-sol`、`effort=xhigh`、cwd 与下列目录一致，所查运行记录只有这一组模型/档位。依据实际 turn 元数据记录，未用全局配置缺省值或用户期望值代填；本轮未调用其他审阅模型，未观察到执行模型回退事件。
- 工作目录：`/Users/ywang2397/work/AI_reliability_knowledge_base`。
- 日期：2026-10-21（Asia/Shanghai）。
- 任务：[T07-07](../../plans/full-coverage-backlog.yaml)，`operation: revise`，主题 07.5；审阅正文：[pd-disaggregation.md](../../knowledge/07-inference/pd-disaggregation.md)。
- 审阅正文 SHA-256：`cc458cdaf87e7380f3542caff0117743fccb5084b27dbac89de6f42d2572670a`；下文正文行号均为该版 118 行原文件坐标。
- 写入范围：只新增本报告；不修改正文、来源记录、registry、导航或计划，不改变编辑/验证状态。

## 范围与方法

先读取 [README](../../README.md)、[写作指南](../authoring-guide.md)、[内容总目录](../../content-outline.md)、仓库 `AGENTS.md` 与 [metadata schema](../../schemas/content.schema.json)。按任务 L6515–6520 的五项 acceptance，重新核对正文、[Batch 27 取证基线](batch-27-t07-07-sources.md)、[Batch 12 原版取证](batch-12-pd-disaggregation-sources.md)及 [registry](../../sources/registry.yaml) 三项对应 notes；用 `git diff` 区分新增主张与原版保留内容，并检查布局、加载、质量三页的关系和普通 Markdown 链接。

证据固定为 vLLM `b17039bccc17b94a2ea107272ad7bc93508708df`、vLLM Ascend `52d4acfa51fb868823d1070b81cbd2d97e9e4696`、MindIE-LLM `69e5a5dd4b533eaffc7e198320435350825a36f7`。网络工具重新打开原文件/GitHub 固定 URL 返回 cache miss，未据此宣称远程链接已验证；实际证据来自用户指定的 `/tmp/b27-fetch/` 原文件，以及既存完整快照补查。上游行号来自这些原文件，不使用网页转换后的行号。来源记录和 registry notes 是审计线索，不替代实际文档/源码。

判定口径：**来源结论**限于文档明示或已读执行分支；**作者归纳**须标明建议/推断和起止事件；**待核实**可以保留，但不得一面写 unknown、一面在表格或常见误解中给出无条件保证。没有安装依赖、启动服务、读取现场集群状态或执行 GPU/NPU、故障注入、性能与输出质量实验。源码分支核对不建立硬件兼容或恢复成功结论。

### 文件身份与补查范围

取证基线列出的 12 个文件 SHA-256 前 16 位全部匹配，完整摘要如下。vLLM 九个缓存文件还与 `/tmp/vllm-b17039bccc17b94a2ea107272ad7bc93508708df/` 对应文件逐字节一致；MindIE FAQ 与 `/tmp/MindIE-LLM-master/` 一致。

| 缓存文件（相对 `/tmp/b27-fetch/`） | SHA-256 |
|---|---|
| vl-disagg_prefill.md | `e68ad65fee967a0078a451db2303aeaeac1da8ae5ce3cd527401b3d33e9810c5` |
| vl-nixl_usage.md | `675eb4152d4151409b63f265d493d55938af77b357f1d778475d78e1d78125b2` |
| vl-mooncake_usage.md | `d60a7cbfdd3e87bea66e39712446a135dd17e2002716bafe6b38ff76b9a29ea2` |
| vl-kv-connectors-req.txt | `de6fc6c8d01542dcfae313949ce1ee402206b136155910b6e9238ecfed38f525` |
| vl-kv-factory.py | `09b87c0e47b618ab1e89f9bd94a098890f7b89086f95cdbde167594d40e1b48a` |
| vl-kv-base.py | `00fc529df6dc944f01bcf0a0573434c5b2388df4f26b3f6428a182d1b028b71c` |
| vl-kv-metrics.py | `a14f705cfa13ef8f26b9e567b7a1d5b0bf9f01e9a282544e340d7d2247021c2d` |
| vl-nixl-connector.py | `bcf8980a73c239451eb5f3fb87aeccd37bae3b21099a95e02f744932ad5af999` |
| vl-mooncake-connector.py | `dd7d60072bfd64bad3e89914e3b51d34d4f78f9b32ff20e1f6f75f2a124aaa5b` |
| va-disagg_prefill.md | `b9c9772f7ec08fb9c10daa0b2bc8da353b368234af2839ef596adf084abf846d` |
| va-pd-mooncake-tutorial.md | `b0bb305495a53c4b39931fe78158f7489bca6e838a339d29bd4f9b4ccc67f343` |
| mi-faq.md | `3c4f5db3c425f4010fd02513971125cd8221995d4491fb6615e2eba78952b0e7` |

补查同一 vLLM 快照的 `kv_transfer.py`、`envs.py`、connector `utils.py`、scheduler、request enum、toy proxy、XpYd demo 和原单机示例；同一 MindIE 快照的服务配置、release notes，以及 KV 传输封装/回调的局部源码（既有登记 `src.ascend.mindie-llm-src-69e5a5dd`，用于 C10）。关键补查文件摘要如下；MindIE 服务配置摘要与 [T07-03 基线](batch-26-t07-03-sources.md)一致。Ascend 完整压缩快照补查 `supported_features.md`（`9c576fc4063ad9718aa76e91aeb602ed7d835ee4a121afc7df9ccc215801ae42`）和 `conf.py`（`ebfca1add56a4d237cf107684c7a7c59ddae4963a456c04ec9432eff96f19657`）；后者 L68/L80 确为 vLLM v0.14.1。目录名或压缩包名本身未被作为版本证明。

| 补查文件（相对各快照根目录） | SHA-256 |
|---|---|
| vllm/config/kv_transfer.py | `28adbd93f24f163cc014c088857762895eadd4b06ec7ed3904a95cc48f5317a6` |
| vllm/envs.py | `edbc5a89f456a59f4173caf0eab838b8d3ecc3e590162a385a0939046dccd9d7` |
| vllm/distributed/kv_transfer/kv_connector/utils.py | `05d4662772368549dfc863df6b2c073a6c1caead3ff44112f98cb6f6725bd66d` |
| vllm/v1/core/sched/scheduler.py | `b4e664fe7dc9ea5c20b2466ad9348d492f9ee7ad19e1e02329fe4e890527d18a` |
| vllm/v1/request.py | `2e4ef2afdfedb245e7e23492ce41f9847f2d514f9f14a639454d0ca5c0fb6e93` |
| tests/v1/kv_connector/nixl_integration/toy_proxy_server.py | `f9cbd61ada30965046a7c6a6c6acab2e37e28e95eb1d6d4684faa7fc0adf1fd4` |
| examples/online_serving/disaggregated_serving/disagg_proxy_demo.py | `cd7d49a99551aec0b5c81896e78b5a9e3447dbc7bbe21bb128125fb1b1437a5e` |
| examples/online_serving/disaggregated_prefill.sh | `1007682e4c650ec86112642b88d3e0d492b7c51ea3ba0a1084a00a65de8589c7` |
| docs/zh/user_guide/user_manual/service_parameter_configuration.md | `59f1dd120399191f251ff9cdc338669f32728a042a1acd254be16bfa76a7b613` |
| docs/zh/release_notes.md | `f4dddd5a096b4f68564fae44e5340018dbce479d89334294aa609958f1d280c4` |
| mindie_llm/distributed/kv_transfer/kv_transfer_agent.py | `76e29c21bed9e1146fe8b1c860481802fbab75d0d0da91d6739ffd8541f810c0` |
| mindie_llm/text_generator/utils/separate_deployment_engine.py | `021cdfa78ef61743da44b55cabf090988de0b6d044fe5a330f3a7e31472a7f3b` |
| src/engine/transfer_output_handler.cpp | `524e413b95832e3d114b1e501a022502e0e34204e00411a281e4f3038985e324` |

## 发现清单

本轮发现 **10 项：0 P1、8 P2、2 P3**。下列均为 OPEN；P2 是影响验收的技术边界或证据覆盖问题，P3 是准确命名、定位及导航问题。C01–C10 为本报告局部编号。

### C01 · P2 · 上游 P/D 模型、并行与内存兼容条件尚未交付完整

**位置**：正文 L49–50、L58、L90、L94；acceptance 1/5。

**陈述**：安装库、UCX 变量和端口说明基本正确，Ascend 的异构/非对称 TP 限制也正确；但上游 NIXL 的 P/D 模型、dtype、attention backend、TP、block size 和 buffer 条件几乎缺席，不能以“P/D 可用不同并行策略”及 HND→NHD 实验特性代替。这些条件已在取得的源码中，并非全部无证据。L94 把 NVIDIA/AMD 与多个 connector 并列，未逐项区分“该平台有直接证据”和“注册存在、平台组合未知”，仍可能被读成整族可用。

**上游证据**：NIXL 的 [兼容 hash 因子 L161–215](https://github.com/vllm-project/vllm/blob/b17039bccc17b94a2ea107272ad7bc93508708df/vllm/distributed/kv_transfer/kv_connector/v1/nixl_connector.py#L161-L215)含 vLLM/connector 版本、model、模型 dtype、KV heads/head size/layers、attention backend、cache dtype；[L1044–1059](https://github.com/vllm-project/vllm/blob/b17039bccc17b94a2ea107272ad7bc93508708df/vllm/distributed/kv_transfer/kv_connector/v1/nixl_connector.py#L1044-L1059)为受开关控制的实际 mismatch 失败分支。TP 整除及 D/P block size 条件见 [utils.py L349–386](https://github.com/vllm-project/vllm/blob/b17039bccc17b94a2ea107272ad7bc93508708df/vllm/distributed/kv_transfer/kv_connector/utils.py#L349-L386)，布局、KV 复制、P_tp>D_tp 与 block 长度的额外约束见 [握手校验 L1677–1756](https://github.com/vllm-project/vllm/blob/b17039bccc17b94a2ea107272ad7bc93508708df/vllm/distributed/kv_transfer/kv_connector/v1/nixl_connector.py#L1677-L1756)。设备/buffer 支持及 VRAM/DRAM、host staging 分支见 [L861–894](https://github.com/vllm-project/vllm/blob/b17039bccc17b94a2ea107272ad7bc93508708df/vllm/distributed/kv_transfer/kv_connector/v1/nixl_connector.py#L861-L894)。这些检查不等于权重内容校验或现场兼容验证。

**关闭条件**：增加按 connector 分列的已核条件/unknown，覆盖上述模型、KV、TP/block、buffer 边界；明确 NIXL/RIXL 的直接平台证据与其余未核组合。上游 Mooncake 的异构/非对称 TP 未核处应明确 unknown，不能继承 NIXL 或 Ascend 限制；库本体版本矩阵和具体 RDMA 环境仍可保留 unknown。不得把 hash 一致写成权重内容一致或所有组合可运行。

### C02 · P2 · 请求身份只列类名和标志，且把跨端 ZMQ 写成 Scheduler/Worker 通道

**位置**：正文 L55–57；acceptance 2/4。

**陈述**：`do_remote_decode/do_remote_prefill` 是行为标志，不能作为 request/transfer ID。正文没有追踪 proxy request ID、P/D request ID、remote engine/block ID 与 transfer handle 的关联；`RecvReqMeta/SendBlockMeta` 的名字也不提供这条链。L57 所称“经 ZMQ 队列在 Scheduler/Worker 两层间传递”与所引源码不符：该 ZMQ listener/queue 位于跨 P/D worker 的请求处理中。

**上游证据**：NIXL [RemoteMeta/ReqMeta L218–280](https://github.com/vllm-project/vllm/blob/b17039bccc17b94a2ea107272ad7bc93508708df/vllm/distributed/kv_transfer/kv_connector/v1/nixl_connector.py#L218-L280)分别保存 local request 字典键、`remote_request_id`、`remote_engine_id`、remote block IDs/host/port；[P 返回 L794–803](https://github.com/vllm-project/vllm/blob/b17039bccc17b94a2ea107272ad7bc93508708df/vllm/distributed/kv_transfer/kv_connector/v1/nixl_connector.py#L794-L803)提供实际交接字段，[L2283–2299](https://github.com/vllm-project/vllm/blob/b17039bccc17b94a2ea107272ad7bc93508708df/vllm/distributed/kv_transfer/kv_connector/v1/nixl_connector.py#L2283-L2299)把 handle 记录到本地 request 对应的在途列表。toy proxy [L212–240](https://github.com/vllm-project/vllm/blob/b17039bccc17b94a2ea107272ad7bc93508708df/tests/v1/kv_connector/nixl_integration/toy_proxy_server.py#L212-L240)生成请求 ID、转交 P 响应内的参数并转发 D，两个发送函数通过 `X-Request-Id` 携带 ID。Mooncake [L64–110](https://github.com/vllm-project/vllm/blob/b17039bccc17b94a2ea107272ad7bc93508708df/vllm/distributed/kv_transfer/kv_connector/v1/mooncake_connector.py#L64-L110)用请求 ID 作字典键，ZMQ 的 P worker listener 见 [L512–557](https://github.com/vllm-project/vllm/blob/b17039bccc17b94a2ea107272ad7bc93508708df/vllm/distributed/kv_transfer/kv_connector/v1/mooncake_connector.py#L512-L557)，D worker 构造并发送元数据见 [L798–852](https://github.com/vllm-project/vllm/blob/b17039bccc17b94a2ea107272ad7bc93508708df/vllm/distributed/kv_transfer/kv_connector/v1/mooncake_connector.py#L798-L852)。

**关闭条件**：用一条字段链或小表解释每种身份的产生/传递/消费位置，区分 request ID、engine ID、block ID 和进程内 transfer handle；未有独立稳定 transfer ID 的实现如实注明。修正 ZMQ 通道端点；不用“同名类”推导上游和 Ascend 共享身份协议。HTTP ID 到各引擎内部 ID 的映射未逐层核实部分保留 unknown。

### C03 · P2 · 本地 tensor 尺寸断言被扩大成跨 P/D dtype/shape/layout 保证

**位置**：正文 L58；acceptance 1/2/4。

**陈述**：所引 Mooncake 断言核对的是本 worker 注册的 KV tensor 字节数、kernel block size 和可整除性，不验证远端 dtype/shape/layout。由此写“匹配由实现断言与两侧一致性保证”缺少跨端检查证据。同时，“缺块/错块的显式检测与报错形态未在……已核实现中出现”过宽：已取得的文件存在请求不存在提示与块数量断言，应与语义错块、内容损坏或完整性校验 unknown 分开。

**上游证据**：Mooncake [L682–718](https://github.com/vllm-project/vllm/blob/b17039bccc17b94a2ea107272ad7bc93508708df/vllm/distributed/kv_transfer/kv_connector/v1/mooncake_connector.py#L682-L718)只遍历本地 `kv_caches`；[AgentMetadata L64–74](https://github.com/vllm-project/vllm/blob/b17039bccc17b94a2ea107272ad7bc93508708df/vllm/distributed/kv_transfer/kv_connector/v1/mooncake_connector.py#L64-L74)无远端 dtype/shape 字段。[L565–571](https://github.com/vllm-project/vllm/blob/b17039bccc17b94a2ea107272ad7bc93508708df/vllm/distributed/kv_transfer/kv_connector/v1/mooncake_connector.py#L565-L571)有 request 不在 `reqs_need_send` 的 warning；[L608–642](https://github.com/vllm-project/vllm/blob/b17039bccc17b94a2ea107272ad7bc93508708df/vllm/distributed/kv_transfer/kv_connector/v1/mooncake_connector.py#L608-L642)断言请求/块数量并使用本地 `block_len` 计算两端地址。NIXL 也有 [块数量断言 L2220–2224](https://github.com/vllm-project/vllm/blob/b17039bccc17b94a2ea107272ad7bc93508708df/vllm/distributed/kv_transfer/kv_connector/v1/nixl_connector.py#L2220-L2224)。这些结构性检查均不能证明块内容属于正确请求。

**关闭条件**：明确本地断言的范围，把两端 dtype/shape/layout 一致写成待满足的兼容前提；分列已见的结构检查/日志与未证实的错请求、错内容、checksum 等检测。不得以等字节数替代跨端类型或语义一致性验证，也不得把上述 warning/断言解释成完整的可恢复错误政策。

### C04 · P2 · 指标表的发起端、时间窗口和首 token 观察者不明确

**位置**：正文 L63–72；acceptance 3。

**陈述**：表格没有完整给出 P 创建、KV 就绪、D 预分配/复用、首个对外输出的独立事件；“request_finished 前后”“WAITING 阶段”“引擎日志/指标”不是可定位的起止字段。“P 发起到 D 接收完成”也不能统一代表 NIXL 传输窗口；NIXL 实际由 D 发起 READ。最后一行给出“D 侧 TTFT”，与段末 TTFT/TPOT 跨实例归属 unknown 的边界不清。即使是建议口径，也需要说明客户端、proxy、P、D 各自的观察范围，不能让 D 局部 TTFT 代替端到端 TTFT。

**上游证据**：NIXL 的 [READ 发起 L2283–2299](https://github.com/vllm-project/vllm/blob/b17039bccc17b94a2ea107272ad7bc93508708df/vllm/distributed/kv_transfer/kv_connector/v1/nixl_connector.py#L2283-L2299)与 [DONE 后采集 telemetry L1973–1991](https://github.com/vllm-project/vllm/blob/b17039bccc17b94a2ea107272ad7bc93508708df/vllm/distributed/kv_transfer/kv_connector/v1/nixl_connector.py#L1973-L1991)并非 P request_finished 到 D 输出的整个窗口；[完整 prefix 命中 L2199–2218](https://github.com/vllm-project/vllm/blob/b17039bccc17b94a2ea107272ad7bc93508708df/vllm/distributed/kv_transfer/kv_connector/v1/nixl_connector.py#L2199-L2218)甚至只通知、不读远端块。toy proxy [P 端 max_tokens=1 L161–173](https://github.com/vllm-project/vllm/blob/b17039bccc17b94a2ea107272ad7bc93508708df/tests/v1/kv_connector/nixl_integration/toy_proxy_server.py#L161-L173)，随后读取 P 响应并由 D 流式输出（L225–240），需要区分 P 的局部首输出与客户端首个合格 payload。仓内[延迟指标字典](../../knowledge/07-inference/latency-metrics.md)也明确不同观察者窗口不能直接相减或互换。

**关闭条件**：按观察者/阶段列出起点事件、终点事件、时间源、实现字段或 unknown；补上 P 创建与 D 复用/无需传输情形。将 NIXL telemetry 限定为实际传输样本，不冒充完整 P→D 阶段耗时。跨实例 TTFT/TPOT 官方拆分口径继续 unknown；建议 trace 字段明确属于作者设计，不写成已有日志。

### C05 · P2 · NIXL 指标尚缺采样范围、实际导出名及失败样本缺口

**位置**：正文 L68、L72；acceptance 3。

**陈述**：六个 stats 数据键和时间 us→s 的描述正确，Mooncake 缺少 Stats override 的结论也有依据；但“完整的实现”一段混合了 raw stats、CLI reduce 标签与 Prometheus 框架，尚未说明哪些字段实际导出、统计粒度与缺失条件。CLI 的 MB 标签按 `2**20` 换算，Throughput 也不是采样墙钟区间的吞吐。尤其仅发生失败、没有成功样本时，这个版本的 stats getter 不导出数据；不能据无指标认定无失败。

**上游证据**：[NixlKVConnectorStats L2483–2566](https://github.com/vllm-project/vllm/blob/b17039bccc17b94a2ea107272ad7bc93508708df/vllm/distributed/kv_transfer/kv_connector/v1/nixl_connector.py#L2483-L2566)显示 bytes 用字节，descriptor/失败项为计数；CLI 以 MiB 换算但标签称 MB，Throughput＝总 MiB/成功传输 duration 之和，并另输出 Avg number of descriptors。`is_empty()` 只看成功 transfer 数；[getter L2406–2413](https://github.com/vllm-project/vllm/blob/b17039bccc17b94a2ea107272ad7bc93508708df/vllm/distributed/kv_transfer/kv_connector/v1/nixl_connector.py#L2406-L2413)在该谓词为真时返回 None，因此失败数据可能等到后续成功样本才导出。

[NixlPromMetrics L2594–2688](https://github.com/vllm-project/vllm/blob/b17039bccc17b94a2ea107272ad7bc93508708df/vllm/distributed/kv_transfer/kv_connector/v1/nixl_connector.py#L2594-L2688)实际注册四个 histogram（`vllm:nixl_xfer_time_seconds`、`vllm:nixl_post_time_seconds`、`vllm:nixl_bytes_transferred`、`vllm:nixl_num_descriptors`）和两个失败 counter（`vllm:nixl_num_failed_transfers`、`vllm:nixl_num_failed_notifications`）；不能只用基类存在证明这些具体指标及其完整性。成功样本在每个完成 transfer handle 上采集，见 C04 所引 DONE 路径，并非天然“一请求一条”。

**关闭条件**：用紧凑映射表分清数据键/单位、CLI 标签/计算、Prometheus 名称/类型与采样粒度；补齐 descriptor 汇总、MiB 标签差异、失败项不在 reduce 输出及纯失败区间的 getter 缺口。不要求修复上游或开展硬件实测；应把该实现限制记录为已核分支，而非无条件可观察保证。

### C06 · P2 · 配置层失败政策被扩大为所有 connector 异常的恢复保证

**位置**：正文 L47、L59、L79、L109；acceptance 2/4。

**陈述**：`KVTransferConfig` 的默认值和枚举正确；但“请求失败策略由……决定”及“只有配置 fail 才直接失败”省略了失败块必须被 connector 检测并上报给 scheduler 的条件。原 Batch 12 取证已明确各 connector 失败路径覆盖未验证；修订版没有以实际代码闭合该范围，反而写成了通用保证。连接/初始化失败、未上报的传输错误和进程故障都不能从这个配置推导结果。

**上游证据**：基类 [get_block_ids_with_load_errors L358–376](https://github.com/vllm-project/vllm/blob/b17039bccc17b94a2ea107272ad7bc93508708df/vllm/distributed/kv_transfer/kv_connector/v1/base.py#L358-L376)默认返回空集，要求异步错误连同完成信号上报。NIXL [L2020–2033](https://github.com/vllm-project/vllm/blob/b17039bccc17b94a2ea107272ad7bc93508708df/vllm/distributed/kv_transfer/kv_connector/v1/nixl_connector.py#L2020-L2033)和 L2415–2424 实际上报 invalid blocks；scheduler [L1116–1123](https://github.com/vllm-project/vllm/blob/b17039bccc17b94a2ea107272ad7bc93508708df/vllm/v1/core/sched/scheduler.py#L1116-L1123)以此进入处理，[L1872–1936](https://github.com/vllm-project/vllm/blob/b17039bccc17b94a2ea107272ad7bc93508708df/vllm/v1/core/sched/scheduler.py#L1872-L1936)才区分 fail/recompute。上游 Mooncake 没有 override 该错误块接口；其 [receive_kv L818–836](https://github.com/vllm-project/vllm/blob/b17039bccc17b94a2ea107272ad7bc93508708df/vllm/distributed/kv_transfer/kv_connector/v1/mooncake_connector.py#L818-L836)在超时/错误响应时记日志并 return，只有正常走到末尾才加入 finished receiving。不能据此证明同样进入上述恢复分支，也不应擅自断言其最终一定挂死或失败。

**关闭条件**：把配置语义与已核 connector 上报路径分开；限定“已检测并上报给 scheduler 的 KV 加载失败”适用政策，删除“只有 fail 才会失败”的排他保证。Mooncake 错误后的请求终态、D 资源回收与重试结果没有证据处保持 unknown，并与 NIXL 分列。

### C07 · P2 · 480s 保留超时被当成 D 故障/断链后的统一清理兜底

**位置**：正文 L59、L80–81、L86；acceptance 2/4。

**陈述**：两份 usage 文档的默认 480s 正确，但这是 P 端保留块超时，不是所有传输/取消分支完成清理的上限。“D 不可用”及“断链/取消”当前都直接落到该兜底，掩盖传输已开始后的区别。L59 的正常路径“D 接收后通知 P 释放”也把 NIXL/Ascend 拉式说明套到了上游 Mooncake 的实际写入实现。外部 router 的取消传播、请求重试与旧 KV 身份处置尚未说明，不能由连接域建立重试或 block recompute 替代。

**上游证据**：NIXL [L757–792](https://github.com/vllm-project/vllm/blob/b17039bccc17b94a2ea107272ad7bc93508708df/vllm/distributed/kv_transfer/kv_connector/v1/nixl_connector.py#L757-L792)分别处理调度前取消通知、P 未完成立即释放与已完成后的保留期限；[L1908–1970](https://github.com/vllm-project/vllm/blob/b17039bccc17b94a2ea107272ad7bc93508708df/vllm/distributed/kv_transfer/kv_connector/v1/nixl_connector.py#L1908-L1970)有轮询过期及按 TP consumer 数等待通知的分支。

Mooncake [L565–593](https://github.com/vllm-project/vllm/blob/b17039bccc17b94a2ea107272ad7bc93508708df/vllm/distributed/kv_transfer/kv_connector/v1/mooncake_connector.py#L565-L593)在开始处理 D 请求时把 `expire_time` 改为无穷，`batch_transfer_sync_write` 成功后由 P 标记发送完成；异常响应见 L547–557。其 [清理 L746–764](https://github.com/vllm-project/vllm/blob/b17039bccc17b94a2ea107272ad7bc93508708df/vllm/distributed/kv_transfer/kv_connector/v1/mooncake_connector.py#L746-L764)只遍历期限已过的发送项，[L856–865](https://github.com/vllm-project/vllm/blob/b17039bccc17b94a2ea107272ad7bc93508708df/vllm/distributed/kv_transfer/kv_connector/v1/mooncake_connector.py#L856-L865)设置普通保留期限；已进入发送而后失败的路径，不能保证仍由 480s 回收。C06 所引 ZMQ 接收还单独设置了 60000ms，不能与 480s 混为一类超时。

**关闭条件**：分别描述“D 未取/未发起”“传输在途”“失败/取消”“正常完成”的 P/D 清理责任、信号和 unknown；纠正上游 Mooncake 的正常释放触发点，明确 480s 的计时/适用边界且不保证进程故障下执行。把 connector 重算、MindIE 通信域建连重试、外部 router 的整请求重试/取消分开，说明后者是待设计验证的责任边界，无须在本页实现生产路由策略。

### C08 · P3 · 精确参数名、状态名和证据定位有退化

**位置**：正文 L48、L57、L59、L69、L86、L90；acceptance 1/3 及来源可追溯性。

**陈述与上游证据**：L48 的 `extra_config.connecters` 拼写不对，文档实际为 [kv_connector_extra_config.connectors，L28–32](https://github.com/vllm-project/vllm/blob/b17039bccc17b94a2ea107272ad7bc93508708df/docs/features/disagg_prefill.md#L28-L32)。L69/L90 归于 Ascend 的状态应为 [`RequestStatus.WAITING_FOR_REMOTE_KVS`，特性指南 L45/L51](https://github.com/vllm-project/vllm-ascend/blob/52d4acfa51fb868823d1070b81cbd2d97e9e4696/docs/source/developer_guide/feature_guide/disaggregated_prefill.md#L41-L53)，缺少末尾 S 不能当作精确日志/状态字段。L59 写“两份 usage 文档 L98–101”，但 Mooncake 全文只有 58 行，相关位置为 [L43–52](https://github.com/vllm-project/vllm/blob/b17039bccc17b94a2ea107272ad7bc93508708df/docs/features/mooncake_connector_usage.md#L43-L52)。L57 的链接文字含 L64–113，实际仅跳到 L449–552。修订还移除了 L86 原有 toy proxy/XpYd demo 的近旁精确链接；其事实仍成立，但核对成本增加。L90 把机制、限制、DFX 和编译压在一段，所给 L38–99 不覆盖 L103–105 限制或另一文件的编译前提。

**关闭条件**：修正键名和状态名；按实际文件分别补齐元数据类、ABORT、Ascend 限制/编译与 toy proxy 的固定锚点。DFX 仅核到设计指南时保留“文档设计声明/实现未验证”的性质。以上无需改变已有版本选择或删除有效的原版结论。

### C09 · P3 · 输出质量页缺少普通 Markdown 返回 PD 页的链接

**位置**：正文 L14–21、L35、L55、L101；[输出质量页](../../knowledge/07-inference/output-quality-evaluation.md) L17–22、L107。

**陈述**：PD 与布局、加载、质量三页的 `related_ids` 均已双向存在；布局与加载两页也有普通正文链接返回 PD。PD→质量有链接，但质量页只在 frontmatter 引用 PD ID，在 L107 提及 PD 时没有链接回正文。机器引用双向与 Markdown 阅读路径双向应分开记录；本项是用户要求的双向可达性收尾，不是 dangling link。

**证据性质**：本项不涉及上游实现；依据仓内四页原文与[写作指南第 6 节](../authoring-guide.md#6-链接正文和操作边界)的普通 Markdown 链接约定。当前构建只保留 JSON 的 related_ids，不在知识正文中自动生成返回链接。

**关闭条件**：后续修订在质量页相关句增加指向 `pd-disaggregation.md` 的普通 Markdown 链接，并复核三对关系两种路径均可达；本轮遵守只新增报告的限制，不代改该页。

### C10 · P2 · MindIE 的“未核实”被升级成“实现不在开源仓”

**位置**：正文 L92、L111；Batch 27 来源记录的对应主张与 unknown；acceptance 4/5。

**陈述**：正文用“KV connector 实现不在开源仓”作为不写内部机制的理由，并称 T07-03 已记此结论；但 T07-03 实际记录是“实现与传输路径未从源码核”。这两种证据状态不同。即使 `KvTransferAgent` 同名类只有占位实现，也不能从该文件推导整个仓库不存在 KV 传输实现；本轮局部补查已见实际拉取封装、边界检查与回调。仍不应由这些局部代码反推底层协议、所有恢复行为或产品包配套。

**上游证据**：固定快照的 [KvTransferAgent L10–17](https://github.com/Ascend/MindIE-LLM/blob/69e5a5dd4b533eaffc7e198320435350825a36f7/mindie_llm/distributed/kv_transfer/kv_transfer_agent.py#L10-L17)是占位类；另一个实际文件 [separate_deployment_engine.py L432–452](https://github.com/Ascend/MindIE-LLM/blob/69e5a5dd4b533eaffc7e198320435350825a36f7/mindie_llm/text_generator/utils/separate_deployment_engine.py#L432-L452)调用 `cache_manager.pull_blocks` 并处理 CANN 异常，[L575–603](https://github.com/Ascend/MindIE-LLM/blob/69e5a5dd4b533eaffc7e198320435350825a36f7/mindie_llm/text_generator/utils/separate_deployment_engine.py#L575-L603)检查远端 instance 是否已链接、目标 block ID 是否越界并返回错误码。底层 `LLMDataDist` 等来自外部 `llm_datadist`（L18–21），其内部实现本轮未核。C++ [TransferOutputHandler L24–58](https://github.com/Ascend/MindIE-LLM/blob/69e5a5dd4b533eaffc7e198320435350825a36f7/src/engine/transfer_output_handler.cpp#L24-L58)处理请求 ID、取消后结果和失败回调，进一步反证“没有可核 KV 路径”的笼统理解。[T07-03 来源记录](batch-26-t07-03-sources.md) L41 仅声明未核实，未证明实现不存在。

**关闭条件**：改为“底层传输实现/协议及完整路径未核”，承认已有开源封装/局部检查，不把占位类视作全仓缺位证据；作者来源记录与相关 notes 同步收窄。可引用上述局部事实，也可只修正证据状态，不要求在本轮完整逆向 MindIE。错块内容检测、底层协议/指标与部署可用组合仍按各自证据保留 unknown。

## acceptance 逐条判定

| 验收项 | 判定 | 通过部分及依据 | 未关闭范围 |
|---|---|---|---|
| 1. connector、协议/传输、网络/设备/内存/制品和 P/D 并行/模型兼容 | 部分满足，需修订 | `nixl>=0.7.1` 由 requirements 文件确认；NIXL usage L9–37 的 NVIDIA/RIXL/UCX 和 NCCL 变量边界，L86–96 的侧信道默认 5600、P/D、base+dp_rank 与跨机 HOST 语义均吻合。Mooncake usage L43–48 的 P 端 8998、base+dp_rank*tp_size+tp_rank 及通知用途吻合。Ascend 教程 L100–141 的 v0.3.7.post2、mpich、ASCEND_DIRECT 和库路径是教程证据，正文保留其旧版本引用限制。Ascend 异构禁止与 P_tp>D_tp 且整除符合特性指南 L103–105。 | C01、C03；上游模型/TP/buffer 条件不足，不能把 Mooncake 的本地断言当跨端保证。精确键名/锚点见 C08。 |
| 2. 权重与 KV 分离，request/transfer ID、dtype/shape/layout、取消清理及重算/失败 | 部分满足，需修订 | 权重启动链与请求级 KV 路径分开，有加载页交叉入口；这是结合两类代码路径的作者归纳。ABORT 480s 和 failure policy 的配置层定义有来源。HND→NHD 明确为实验特性。 | C02、C03、C06、C07：身份链未追踪、通道端点错误、本地与跨端检查混淆、政策与清理过度保证。 |
| 3. P 创建→传输→D 接收/复用→首 token 的归属、起止及缺失字段 | 未满足 | NIXL 六个 raw stats 键、us→s 与 worker→logger 框架已核；Mooncake 未 override stats、基类默认 None，故该 commit 的 connector Stats 缺位结论成立。TTFT/TPOT 官方跨实例拆分未证，继续 unknown 合理。 | C04、C05：阶段/观察者与事件未闭合，NIXL 发起方向和表内 TTFT 边界有误；实际导出、单位计算和纯失败区间缺口未说明。不能用泛称“日志/引擎指标”补齐。 |
| 4. 超时、断链、缺块/错块、D 不可用、取消/重试、清理与 router | 部分满足，需修订 | MindIE FAQ L270–280 以 ERROR 加 CANN timeout 定位 P→D 传输超时，“网络质量差”保留为上游高可能判断而非现场根因。服务配置 L133–134 的 kv_trans_timeout=10s、kv_link_timeout=1080s 和建连重试语义准确；外部 router/toy 边界正确。 | C03、C06、C07：结构性缺块检查与语义错块 unknown 未分开，已开始发送后清理和政策上报条件不完整，整请求重试/取消责任仍缺；C10：MindIE 已有局部检查不可用“无开源实现”略过。 |
| 5. NVIDIA/AMD vLLM、Ascend Mooncake、MindIE 所选版本对照 | 部分满足；机制与版本隔离维度通过 | Ascend pull/push 两式符合指南 L39–54；NVIDIA NIXL 与 AMD RIXL 的文档分支有依据。MindIE standard/dmi、3.1.0 三特性同时开启限制分别对应服务配置 L55、release notes L99；底层传输与 Motor 外链未取证可保持 unknown。“同名不互推”、插件 conf.py 指向 v0.14.1 与上游 v0.14.0 不构成已验证配套的边界保留正确。 | C01：不能以 NVIDIA/AMD 合并列举承接未经核实的整族 connector 组合。C08：Ascend 精确状态名与定位需改。C10：未核实不等于整个实现不在开源仓。 |

### 其余通过维度及依据

| 维度 | 结论与依据 |
|---|---|
| 原 Batch 12 的定义、动机和吞吐反面声明 | 保留准确：disagg_prefill.md L5–16 仍为 experimental、TTFT/ITL 分别调优、尾 ITL 动机及不提升吞吐的版本声明；L43 联合评估时延、吞吐/goodput、失败率与 KV 成本明确是作者方法建议，没有冒充实测。 |
| 原 KVTransferConfig / 注册表 / toy proxy | 配置取值、角色必填和默认 failure policy 与 kv_transfer.py L13–70/L90–104 一致；政策覆盖范围另见 C06。factory.py L146–203 确有 10 个注册项，无 SharedStorageConnector，未再推导与 Offloading 等价。toy 的轮询、max_tokens=1 和 do_remote_decode，以及 demo 将移除的声明均与固定源码一致；没有把这些演示件写成生产负载感知路由。 |
| frontmatter / 来源登记 / 本地目标 | 稳定 ID、concept/inference、draft/source_checked、updated_at 和三项 source/evidence refs 均有效；新增三个 related IDs 存在且反向 IDs 均存在。正文全部本地链接目标存在。registry 三项版本与新增 notes 已对上，未将没有取回的 NIXL/Mooncake 库本体虚报为已核；notes 中同类过宽表述应随正文修订收紧，不能独立替正文背书。普通 Markdown 返回路径缺口单列 C09。 |
| 与 T07-06、T07-01、T07-05 的主归属 | 没有实质重复：布局页负责 TP/PP/DP/EP/CP/SP 的所有权和组通信，本页负责 P/D KV 交接与 connector；加载页提供启动/ready 主线，质量页提供输出对照方法。布局页 L116 已把 PD 非对称 TP 指回本页。补 C01 的“交接兼容条件”仍属 07.5，生产路由策略保留 07.6 边界即可，无需复制通用布局长表。 |
| unknown 的合理保留 | NIXL/RIXL 库与 UCX 版本矩阵、Mooncake 引擎本体 API、Ascend 独立 stats、语义错块/内容完整性、MindIE 内部协议/指标与 Motor 指南、P2pNccl 跨机条件、量化效果和性能数字继续 unknown；现有实现已经可见的结构检查、ID、失败分支不应统称未出现。 |

## 整体结论

**本轮初审不通过，需修订并定向复核。** 修订稿已经补齐多处有效的版本化证据，安装/端口参数、Ascend 两式机制与限制、MindIE 超时配置、Stats 有无和外部路由边界均有可保留依据；但 P/D 兼容与身份链、指标阶段窗口、failure policy 上报条件、在途失败后的资源清理及 MindIE 实现的证据状态仍影响五项验收。优先处理 C01–C07、C10，再关闭 C08–C09；正文、来源基线与 registry notes 的同类结论应保持一致。本报告没有代为修订，也没有因结构检查通过而改变 `draft / source_checked` 状态。

执行 `make check`、`make build` 均通过：**112 content entries / 542 sources**；只验证结构及本地文件链接，不验证本文技术结论、远端 URL、真实平台兼容或恢复效果。未修改 `src/kb/`，未新增实现或测试，未执行硬件验证。交付前逐文件摘要比对，审阅前已有源文件全部不变；本轮仅写入本报告并按规范重建忽略目录 `build/`。期间另有 `batch-27-t07-05-codex-review.md` 出现在工作区，本轮未写入或改动它。

统计：审阅正文 1 篇；acceptance 5 项（完整通过 0、部分满足 4、未满足 1）；发现 10 项（P1=0，P2=8，P3=2；OPEN=10，CLOSED=0）；make check=PASS；make build=PASS；硬件验证=未执行；整体=需修订并定向复核。
