# Batch 27 · T07-07 第二轮定向复核

## 会话元数据

- 审阅角色：AI 可靠性知识库批次审阅者；仅核对[第一轮复核](batch-27-t07-07-codex-recheck.md)仍开放的 C01、C02、C04、C05、C07、C08、C10、N01 及本轮修订引入的问题。C03、C06、C09 的 CLOSED 结论沿用，不重做初审。
- 实际执行模型：`gpt-6.1-sol`；实际推理档位：`xhigh`。
- 核验依据：`CODEX_THREAD_ID=01a15b34-d254-73d3-a661-bad334bbe929` 对应本地 CLI rollout；`session_meta` 为 `originator=codex_exec`、`source=exec`、`cli_version=0.163.0`，本轮已查 `turn_context` 只有 `model=gpt-6.1-sol / effort=xhigh`，cwd 与下列目录一致。按实际运行元数据记录，未用用户期望或全局配置代填；未调用其他审阅模型，所查记录未见模型切换，助手输出未见回退标记。
- 工作目录：`/Users/ywang2397/work/AI_reliability_knowledge_base`；日期：2026-10-21（Asia/Shanghai）。
- 被检对象：工作区当前的 [PD 正文](../../knowledge/07-inference/pd-disaggregation.md)、[T07-07 来源记录](batch-27-t07-07-sources.md)、[registry](../../sources/registry.yaml)。以下行号均为本轮原文件坐标。
- 写入范围：只新增本报告；不代改被检对象、导航、计划或审核状态。按仓库规范重建忽略目录 `build/`。

| 被检文件 | 行数 | SHA-256 |
|---|---|---|
| knowledge/07-inference/pd-disaggregation.md | 159 | `4251168e5d96d0652b57ca053503bcc75ca21d24b094d1251fb8eb5468a9ac57` |
| docs/research/batch-27-t07-07-sources.md | 67 | `df2bce6dfb44d3c6a1f053827a8e7ee0153f6fe9ae570f9ea20619d30a41856e` |
| sources/registry.yaml | 6788 | `9410454cb0d1a19a7ad87a18742a265d03891d4b6abc82500045193e6d4b2652` |

已读取仓库 `AGENTS.md`、[README](../../README.md)、[写作指南](../authoring-guide.md)、[内容总目录](../../content-outline.md)与[元数据 schema](../../schemas/content.schema.json)。证据版本沿用 vLLM `b17039bccc17b94a2ea107272ad7bc93508708df`、vLLM Ascend `52d4acfa51fb868823d1070b81cbd2d97e9e4696`、MindIE-LLM `69e5a5dd4b533eaffc7e198320435350825a36f7`。

本轮重新计算[初审](batch-27-t07-07-codex-review.md)列出的 12 个缓存文件与 13 个补查文件摘要，**25/25 匹配**；vLLM 九份缓存与完整快照逐字节一致。逐项证据来自 `/tmp/b27-fetch/`、`/tmp/vllm-b17039bccc17b94a2ea107272ad7bc93508708df/`、`/tmp/MindIE-LLM-master/` 的原文件。必要重取尝试打开固定 commit 的 connector `utils.py` 与 Ascend PD 指南，网络工具均返回 cache miss；不宣称远程 URL 可达性已通过。下列 GitHub 行号锚点按本地原文件核对，不使用网页转换坐标。

作者修订清单仅作定位线索，关闭以当前文件与源码证据为准。未安装依赖、启动服务或执行 GPU/NPU、故障注入、性能及输出质量实验；源码核对不建立平台兼容或恢复成功结论。

## 逐项判定

### C01 · P2 · 满足，CLOSED

**位置**：正文 L54–64，尤其 L59；来源记录 L58。

本轮已经把第一轮要求的兼容条件写成可读陈述：TP 大值须能被小值整除；D local block size 须能被 P remote block size 整除；P_tp>D_tp 且 KV 复制被握手断言拒绝；非 MLA 布局不同时须走实验 HND→NHD 分支；MLA/复制 KV 与非复制分支分开，后者 P_tp>D_tp 时要求 block ratio=1。分别与 [utils.py L349–386](https://github.com/vllm-project/vllm/blob/b17039bccc17b94a2ea107272ad7bc93508708df/vllm/distributed/kv_transfer/kv_connector/utils.py#L349-L386)、[握手 L1686–1756](https://github.com/vllm-project/vllm/blob/b17039bccc17b94a2ea107272ad7bc93508708df/vllm/distributed/kv_transfer/kv_connector/v1/nixl_connector.py#L1686-L1756)一致，没有把 block 条件反向放宽。

设备/buffer 映射及平台扩展、非 CPU 设备选 CPU buffer 时使用 host staging、无法取得有效 NIXL memory type 时初始化失败，也与[设备表 L113–125](https://github.com/vllm-project/vllm/blob/b17039bccc17b94a2ea107272ad7bc93508708df/vllm/distributed/kv_transfer/kv_connector/v1/nixl_connector.py#L113-L125)和[初始化 L861–894](https://github.com/vllm-project/vllm/blob/b17039bccc17b94a2ea107272ad7bc93508708df/vllm/distributed/kv_transfer/kv_connector/v1/nixl_connector.py#L861-L894)吻合。hash、权重内容与可运行组合仍分开；平台直接证据及 Mooncake/库本体 unknown 边界保留。第一轮剩余条件满足。

### C02 · P2 · 满足，CLOSED

**位置**：正文 L72–78；来源记录 L59。

身份链现已明确区分：P 返回 `remote_request_id=request.request_id`、`remote_engine_id`、`remote_block_ids`（[L794–803](https://github.com/vllm-project/vllm/blob/b17039bccc17b94a2ea107272ad7bc93508708df/vllm/distributed/kv_transfer/kv_connector/v1/nixl_connector.py#L794-L803)）；D 将远端字段放入 `RemoteMeta`，以 **D 本地 request ID** 为 `reqs_to_recv` 的键（[L266–280](https://github.com/vllm-project/vllm/blob/b17039bccc17b94a2ea107272ad7bc93508708df/vllm/distributed/kv_transfer/kv_connector/v1/nixl_connector.py#L266-L280)）；进程内 handle 关联到本地 request（[L2283–2299](https://github.com/vllm-project/vllm/blob/b17039bccc17b94a2ea107272ad7bc93508708df/vllm/distributed/kv_transfer/kv_connector/v1/nixl_connector.py#L2283-L2299)），通知使用 P 的 remote request ID（[L2195–2197](https://github.com/vllm-project/vllm/blob/b17039bccc17b94a2ea107272ad7bc93508708df/vllm/distributed/kv_transfer/kv_connector/v1/nixl_connector.py#L2195-L2197)）。所引 [toy proxy L225–240](https://github.com/vllm-project/vllm/blob/b17039bccc17b94a2ea107272ad7bc93508708df/tests/v1/kv_connector/nixl_integration/toy_proxy_server.py#L225-L240)实际取出 P 响应的 `kv_transfer_params` 放入发往 D 的 `req_data`，与表内交接字段和代理层引用相接。

Mooncake 线上负载已改为 `MooncakeAgentMetadata`：D [L798–820](https://github.com/vllm-project/vllm/blob/b17039bccc17b94a2ea107272ad7bc93508708df/vllm/distributed/kv_transfer/kv_connector/v1/mooncake_connector.py#L798-L820)编码发送，P [L493–495](https://github.com/vllm-project/vllm/blob/b17039bccc17b94a2ea107272ad7bc93508708df/vllm/distributed/kv_transfer/kv_connector/v1/mooncake_connector.py#L493-L495)声明解码类型、[L547–554](https://github.com/vllm-project/vllm/blob/b17039bccc17b94a2ea107272ad7bc93508708df/vllm/distributed/kv_transfer/kv_connector/v1/mooncake_connector.py#L547-L554)实际解码消费。`RecvReqMeta/SendBlockMeta` 已标本地类，`SendBlockMeta` 的 `asyncio.Event` 与期限不再冒充线上序列化字段。HTTP→引擎内部 ID 映射 unknown、无独立稳定 transfer ID 及同名协议不互推的边界均保留。

### C04 · P2 · 满足，CLOSED

**位置**：正文 L84–96；来源记录 L61。

表格已增加时间源列，标明建议新增本地单调时钟及跨主机先对齐的前提；客户端提交→首个合格 payload 的完整窗口已给出。请求提交、P 创建/prefill、KV 就绪、传输、D 预分配、D 接收/复用、首 token 现各有一行；现成字段级时间戳与免传输观察记录未核处标为 unknown，段末也明确 trace 属本库设计，不把泛称日志当成现成字段。

NIXL 的 D 发起 READ、DONE 后采集 telemetry 与[调用 L2283–2299](https://github.com/vllm-project/vllm/blob/b17039bccc17b94a2ea107272ad7bc93508708df/vllm/distributed/kv_transfer/kv_connector/v1/nixl_connector.py#L2283-L2299)、[采样 L1973–1991](https://github.com/vllm-project/vllm/blob/b17039bccc17b94a2ea107272ad7bc93508708df/vllm/distributed/kv_transfer/kv_connector/v1/nixl_connector.py#L1973-L1991)吻合；已明确 READ 调用到轮询 DONE 的墙钟差不等同库返回的 `xferDuration`，库计时边界仍未核。完整 prefix 命中免传输与 D 局部 TTFT 不替代端到端窗口的限定保留。D 预分配行的状态拼写仍属 C08，单独判定，不重复计入本项。

### C05 · P2 · 满足，CLOSED

**位置**：正文 L98–109；来源记录 L62。

raw→CLI→Prometheus 三列映射已交付，具体时间 Avg/P90 标签、成功数派生项、bytes/descriptor 汇总、失败计数的映射均可识别。对照 [record/reduce L2494–2566](https://github.com/vllm-project/vllm/blob/b17039bccc17b94a2ea107272ad7bc93508708df/vllm/distributed/kv_transfer/kv_connector/v1/nixl_connector.py#L2494-L2566)：raw 两种 duration 均为秒，CLI 两种 Avg/P90 均输出毫秒；成功数取 `len(transfer_duration)`；bytes 按 `2**20` 换算 MiB 但标签称 MB；Throughput 分母为成功传输 duration 之和；descriptors 输出均值。失败项不进入 reduce。

四个 histogram 与两个失败 counter 的名称和类型符合 [L2594–2688](https://github.com/vllm-project/vllm/blob/b17039bccc17b94a2ea107272ad7bc93508708df/vllm/distributed/kv_transfer/kv_connector/v1/nixl_connector.py#L2594-L2688)。每完成 handle 采样、纯失败区间 getter 返回 None、无输出不证明无失败，以及 Mooncake 此 commit 无 Stats 实现的版本限定均保留，没有新增无条件可观察保证。

### C07 · P2 · 满足，CLOSED

**位置**：正文 L115–120，尤其 L118；来源记录 L64。

两种计时起点已明确：NIXL 在 P 完成且延迟释放的 `request_finished` 分支设 `perf_counter()+timeout`（[L770–792](https://github.com/vllm-project/vllm/blob/b17039bccc17b94a2ea107272ad7bc93508708df/vllm/distributed/kv_transfer/kv_connector/v1/nixl_connector.py#L770-L792)），由 [get_finished L1908–1927](https://github.com/vllm-project/vllm/blob/b17039bccc17b94a2ea107272ad7bc93508708df/vllm/distributed/kv_transfer/kv_connector/v1/nixl_connector.py#L1908-L1927)轮询检查；Mooncake 在 worker 接到完成后的非空 block 列表时设期限（[L856–872](https://github.com/vllm-project/vllm/blob/b17039bccc17b94a2ea107272ad7bc93508708df/vllm/distributed/kv_transfer/kv_connector/v1/mooncake_connector.py#L856-L872)），过期清理由 [L746–764](https://github.com/vllm-project/vllm/blob/b17039bccc17b94a2ea107272ad7bc93508708df/vllm/distributed/kv_transfer/kv_connector/v1/mooncake_connector.py#L746-L764)执行。没有把起点统一写成请求中止时刻或精确定时回调。

在途失败的 D 侧新增“释放失败 handle＋标记 invalid blocks”，与 [L2020–2033](https://github.com/vllm-project/vllm/blob/b17039bccc17b94a2ea107272ad7bc93508708df/vllm/distributed/kv_transfer/kv_connector/v1/nixl_connector.py#L2020-L2033)一致；D 预分配 KV 的完整回收链明确 unknown。未发起/取消、正常完成、Mooncake 在途期限改无穷、进程故障不保证清理，以及三层重试责任仍分开。默认值/文档语义已分别近旁锚定 [NIXL usage L98–101](https://github.com/vllm-project/vllm/blob/b17039bccc17b94a2ea107272ad7bc93508708df/docs/features/nixl_connector_usage.md#L98-L101)、[Mooncake usage L50–52](https://github.com/vllm-project/vllm/blob/b17039bccc17b94a2ea107272ad7bc93508708df/docs/features/mooncake_connector_usage.md#L50-L52)。第一轮剩余条件满足。

### C08 · P3 · 部分满足，OPEN

**位置**：正文 L92、L118、L130；来源记录 L65。

**已满足**：60000ms 已正确锚定 D `receive_kv` 的 [L814–821](https://github.com/vllm-project/vllm/blob/b17039bccc17b94a2ea107272ad7bc93508708df/vllm/distributed/kv_transfer/kv_connector/v1/mooncake_connector.py#L814-L821)；Ascend 编译补了[教程 L100–141](https://github.com/vllm-project/vllm-ascend/blob/52d4acfa51fb868823d1070b81cbd2d97e9e4696/docs/source/tutorials/pd_disaggregation_mooncake_single_node.md#L100-L141)锚点；ABORT 两份 usage 已分别定位。身份链的几段新增证据也已有各自链接。

**未满足**：状态名没有全量修正，且出现代码跨度内的 Markdown 标记残留。

- 正文 L92 的实际状态仍写 `RequestStatus.WAITING_FOR_REMOTE_KV`；括号中补“指南原文 WAITING_FOR_REMOTE_KV**S**”没有改正前面的状态。
- 正文 L130 写成字面量 `RequestStatus.WAITING_FOR_REMOTE_KV**S**`。星号位于反引号内，会成为代码字符串的一部分，不会把 S 加粗；该字符串仍不是精确标识符。
- 来源记录 L65 仍称“状态名按指南原文 WAITING_FOR_REMOTE_KV（指南 L41–53 原文，正文注明原文形态）”，错误的原文归因未撤回，也未标为已废止历史结论。

实际指南 [L45](https://github.com/vllm-project/vllm-ascend/blob/52d4acfa51fb868823d1070b81cbd2d97e9e4696/docs/source/developer_guide/feature_guide/disaggregated_prefill.md#L45)与 [L51](https://github.com/vllm-project/vllm-ascend/blob/52d4acfa51fb868823d1070b81cbd2d97e9e4696/docs/source/developer_guide/feature_guide/disaggregated_prefill.md#L51)均为 `RequestStatus.WAITING_FOR_REMOTE_KVS`，本轮摘要与第一轮一致。

**剩余关闭条件**：正文两处统一使用不含星号的完整标识符 `RequestStatus.WAITING_FOR_REMOTE_KVS`；来源记录 L65 同步更正或明确标记旧说明已撤回。无需再补运行实验。星号残留属于本项修订未完成，不另分新 ID。

### C10 · P2 · 部分满足，OPEN

**位置**：正文 L122、L132、L152、L159；来源记录 L38、L46、L67。

**已满足**：来源记录 unknown 4（L46）已直接改成底层协议与完整路径未核，明确撤回初稿“不在开源仓”及错误的 T07-03 归因。正文关于 `pull_blocks`、CANN 异常、远端 instance/目标 block 越界检查、`TransferOutputHandler`、占位类和外部依赖的保守边界继续成立；本轮重读 [Python L432–452](https://github.com/Ascend/MindIE-LLM/blob/69e5a5dd4b533eaffc7e198320435350825a36f7/mindie_llm/text_generator/utils/separate_deployment_engine.py#L432-L452)、[L575–603](https://github.com/Ascend/MindIE-LLM/blob/69e5a5dd4b533eaffc7e198320435350825a36f7/mindie_llm/text_generator/utils/separate_deployment_engine.py#L575-L603)与 [C++ L24–58](https://github.com/Ascend/MindIE-LLM/blob/69e5a5dd4b533eaffc7e198320435350825a36f7/src/engine/transfer_output_handler.cpp#L24-L58)，未见正文恢复全仓缺位或完整协议保证。

**未满足**：同一来源记录的**主张—来源定位表 L38**仍以当前支持范围写“FAQ＋配置口径；connector 实现不在开源仓（unknown）”，没有将该单元格改正或标为旧结论已撤回。unknown 4 的撤回说明虽已补上，当前主表仍直接给出相反断言；第一轮要求处理的两处旧结论只在其中一处落地。unknown 括注不能把“全仓不存在”变成“尚未核实”。

**剩余关闭条件**：直接更正主表 L38，或在该单元格明确标注旧断言已撤回并指向当前局部取证/unknown。保留已修正的 L46 与正文即可；不要求扩查底层依赖。源码登记关系另属 N01，不重复计入 C10。

### N01 · P3 · 部分满足，OPEN（沿用第一轮新增项）

**位置**：正文 frontmatter L8–13、L24–31；来源记录 L52–53、L67；registry L6630–6643、L6708–6721。

**已满足**：`source_refs` 已同时增加 `src.ascend.mindie-llm-repo-69e5a5dd` 与 `src.ascend.mindie-llm-src-69e5a5dd`；`evidence_refs` 增加了后者。registry 的 mindie-src notes（L6721）新增本轮局部取证及底层 `LLMDataDist` unknown，且源码与 docs 的许可条目继续分开。

**未满足**：验证证据与来源 scope 尚未完整对齐。

1. `evidence_refs` L26–30 仍没有 `src.ascend.mindie-llm-repo-69e5a5dd`；新增的 mindie-src 来源 URL 与许可 scope 均限定 **`src/`**（registry L6710、L6717），不能自动覆盖正文 L122 及 verification notes 声称已核的 `mindie_llm/.../separate_deployment_engine.py`、`kv_transfer_agent.py`。`source_refs` 已建立来源依赖，但对应 Python 验证证据关联尚未补齐。
2. Python 取证说明全部追加在 mindie-src notes；覆盖仓库 Python 路径的 mindie-repo notes（L6643）仍限定“本条仅锚定仓库身份与 README 口径”。需按各自登记范围记录此次证据，或明确跨来源引用关系，不能依靠相同 commit 将 `src/` scope 扩成整个仓库。
3. 来源记录“集成轮结果”L52–53 仍以现行汇总称全部文件落在既有三个 scope、只扩展三个 notes，没有区分原集成轮与本轮新增源码来源关联；L67 也未补足按 scope 的当前登记说明。若保留历史应明确其轮次覆盖范围，并补当前关联结果。

**剩余关闭条件**：给 Python 局部取证补 mindie-repo 的验证证据关联及相应 notes；mindie-src 保留 C++ 取证，并可交叉指向 Python 所在来源；来源记录补清本轮实际使用的登记项及范围。无需新建 ID、合并许可或取回 `llm_datadist`。

## 新问题

**未发现需要另立 ID 的新问题。** 状态名中新增的字面星号及来源同步遗漏均已纳入 C08、C10、N01 的剩余关闭条件，不重复计数；N01 是第一轮新增、本轮复核的既有项。C03、C06、C09 沿用 CLOSED，不以本轮未重审扩大其原有通过范围。

## 整体结论

**本轮定向复核不通过，仍需修订并复核。** 本轮八项中，C01、C02、C04、C05、C07 关闭；C08、C10、N01 部分满足，保持 OPEN。连同沿用的 C03、C06、C09，累计 11 个既有问题中 CLOSED=8、OPEN=3（P2=1、P3=2）。

剩余工作集中在状态标识符的完整更正、来源主表旧断言撤回、Python/C++ 取证关联与登记范围对齐。正文继续保持 `draft / source_checked`；本轮没有建立硬件兼容、资源回收完成、恢复成功或输出质量等价的验证结论。

已执行 `make check`、`make build`，均通过：**112 content entries / 542 sources**。检查只验证结构和本地文件链接，不验证技术正确性、远程链接或真实平台行为。未修改 `src/kb/`，未新增测试或执行硬件验证。

逐文件 SHA-256 比对确认，入场取样的 578 个既有源文件均未变化。本轮只写入本报告并重建忽略目录 `build/`；期间另有 `batch-27-t07-05-codex-recheck-2.md` 出现在工作区，本轮未写入或修改该文件。

统计：本轮定向复核 8 项（CLOSED=5，OPEN=3）；沿用 CLOSED=3；累计既有问题 11 项（CLOSED=8，OPEN=3；开放 P1=0、P2=1、P3=2）；本轮新问题=0；make check=PASS；make build=PASS；硬件验证=未执行；整体=需继续修订并定向复核。
