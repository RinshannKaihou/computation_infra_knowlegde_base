# Batch 27 · T07-07 第一轮定向复核

## 会话元数据

- 审阅角色：AI 可靠性知识库批次审阅者；仅复核[初审报告](batch-27-t07-07-codex-review.md) C01–C10 的关闭条件及修订引入的问题，不重做整篇初审。
- 实际执行模型：`gpt-6.1-sol`；实际推理档位：`xhigh`。
- 核验依据：`CODEX_THREAD_ID=01a15b2d-c9e3-70d1-92ee-0acf5a286122` 对应本地 CLI rollout；`session_meta` 为 `originator=codex_exec`、`source=exec`、`cli_version=0.163.0`，本轮 `turn_context` 只有 `model=gpt-6.1-sol / effort=xhigh`，cwd 与下列目录一致。未以用户期望或全局配置代填；未调用其他审阅模型，所查运行记录未见模型切换，助手输出未见回退标记。
- 工作目录：`/Users/ywang2397/work/AI_reliability_knowledge_base`；日期：2026-10-21（Asia/Shanghai）。
- 被检对象：工作区当前的 [PD 正文](../../knowledge/07-inference/pd-disaggregation.md)、[输出质量页](../../knowledge/07-inference/output-quality-evaluation.md)（只核 C09 链接）、[registry](../../sources/registry.yaml)、[T07-07 来源记录](batch-27-t07-07-sources.md)。布局、加载页只读核对 C09 所需的三对关系，不扩展其技术审阅范围。
- 写入范围：只新增本报告；不代改正文、来源记录、registry、导航、计划或审核状态。按仓库规范重建忽略目录 `build/`。

本轮被检文件身份如下。下文“正文 L…”均指这版 PD 正文的原文件行号；来源记录行号也按表中版本计算。

| 文件 | SHA-256 |
|---|---|
| knowledge/07-inference/pd-disaggregation.md（142 行） | `5303ca189c7de1bd89771f8f1a9ba8656704f20e99bc19e6b93306705c6173a7` |
| knowledge/07-inference/output-quality-evaluation.md | `41e674c32350cf1151b3051df847a65ef49bbae2ebb75a4c222b6694db51f4a4` |
| sources/registry.yaml | `30435a08607d0207cbef085d665060dd9575a65b32f89bb2927730110453bf42` |
| docs/research/batch-27-t07-07-sources.md | `89e1db014aeda5651818dc933955e3f6aabb4aae1e1dd77da3171a08f459bd3a` |

已读取仓库 `AGENTS.md`、[README](../../README.md)、[写作指南](../authoring-guide.md)、[内容总目录](../../content-outline.md)与[元数据 schema](../../schemas/content.schema.json)。取证沿用 vLLM `b17039bccc17b94a2ea107272ad7bc93508708df`、vLLM Ascend `52d4acfa51fb868823d1070b81cbd2d97e9e4696`、MindIE-LLM `69e5a5dd4b533eaffc7e198320435350825a36f7`。本轮重新计算初审列出的 12 个基线文件与 13 个补查文件摘要，**25/25 与初审一致**；vLLM 九份缓存还与完整快照逐字节一致。实际核对 `/tmp/b27-fetch/`、`/tmp/vllm-b17039bccc17b94a2ea107272ad7bc93508708df/`、`/tmp/MindIE-LLM-master/` 中的原文件，不把作者修订清单当成关闭证据。

必要重取尝试打开固定 commit 的 Ascend 特性指南与 NIXL 原文件，网络阅读工具均返回 cache miss；本报告不宣称已验证远程 URL 可达性。技术判定来自上述已核摘要的本地快照，GitHub 锚点使用原文件坐标。未安装依赖、启动推理服务或执行 GPU/NPU、故障注入、性能、输出质量实验。以下 OPEN 沿用初审 ID 与优先级；“部分满足”不计为关闭。

## C01–C10 逐项判定

### C01 · P2 · 部分满足，OPEN

**位置**：正文 L49、L53–61、L117；来源记录 L58。

**已满足**：按 connector 分节；hash 的实际因子与 [NIXL L189–202](https://github.com/vllm-project/vllm/blob/b17039bccc17b94a2ea107272ad7bc93508708df/vllm/distributed/kv_transfer/kv_connector/v1/nixl_connector.py#L189-L202)一致，没有把注释中的 sliding window 误加进实际字典；区分 hash、权重内容与可运行结论。NVIDIA/NIXL、ROCm/RIXL 的直接文档分支与其他未核组合分开，上游 Mooncake 的未核条件也没有继承 NIXL 或 Ascend 的限制。

**未满足**：L56 仍只说“TP 整除与 D/P block size 条件在…；额外约束在…；设备/buffer 支持见…”，没有把条件本身交付出来。初审要求补的是可读的兼容前提，不能由数个源码入口替代。至少以下已核内容仍未写明：

- [utils.py L349–386](https://github.com/vllm-project/vllm/blob/b17039bccc17b94a2ea107272ad7bc93508708df/vllm/distributed/kv_transfer/kv_connector/utils.py#L349-L386)：TP 大值须能被小值整除；D 侧 local block size 须能被 P 侧 remote block size 整除，并非任一方向整除均可。
- [握手 L1686–1756](https://github.com/vllm-project/vllm/blob/b17039bccc17b94a2ea107272ad7bc93508708df/vllm/distributed/kv_transfer/kv_connector/v1/nixl_connector.py#L1686-L1756)：P_tp>D_tp 且 KV 复制的组合被断言拒绝；非 MLA 的布局不同时须满足实验 HND→NHD 分支；MLA/复制 KV 的 block 长度校验与非复制分支分开，后者 P_tp>D_tp 时要求 block size ratio=1。这些不能由“有额外约束”表达。
- [设备表 L113–125](https://github.com/vllm-project/vllm/blob/b17039bccc17b94a2ea107272ad7bc93508708df/vllm/distributed/kv_transfer/kv_connector/v1/nixl_connector.py#L113-L125)与[初始化 L861–894](https://github.com/vllm-project/vllm/blob/b17039bccc17b94a2ea107272ad7bc93508708df/vllm/distributed/kv_transfer/kv_connector/v1/nixl_connector.py#L861-L894)：内置 device→buffer 映射及平台扩展入口、非 CPU 设备选 CPU buffer 时使用 host staging、无法取得有效 NIXL memory type 时失败；当前只点名 VRAM/DRAM，未说明这些边界。源码接受某设备类别仍不构成真实平台支持证明。

**剩余关闭条件**：用短表或短句写出上述条件、适用分支与失败形态，保留现有版本/平台/unknown 限定；不要求穷举库本体或现场 RDMA 矩阵。

### C02 · P2 · 部分满足，OPEN

**位置**：正文 L71–75；来源记录 L59。

**已满足**：区分 proxy ID、引擎/block 元数据与在途 handle；注明 HTTP→内部 ID 映射 unknown；修正 ZMQ 的跨 P/D worker 端点，未以同名类推导 Ascend 协议相同。

**未满足**：小表仍主要列 `RemoteMeta/ReqMeta` 成员，没有说明本地 request 字典键与 P 的 `remote_request_id` 如何产生、交接和消费。P 返回字段仅用“P 响应携带交接字段”概括；所写“L218–280、L794–803”的单个链接实际只跳到前一段。可见的具体链是：P 在 [L794–803](https://github.com/vllm-project/vllm/blob/b17039bccc17b94a2ea107272ad7bc93508708df/vllm/distributed/kv_transfer/kv_connector/v1/nixl_connector.py#L794-L803)返回 `remote_request_id=request.request_id`、`remote_engine_id=self.engine_id`、`remote_block_ids` 等；D 在 [L266–280](https://github.com/vllm-project/vllm/blob/b17039bccc17b94a2ea107272ad7bc93508708df/vllm/distributed/kv_transfer/kv_connector/v1/nixl_connector.py#L266-L280)把这些放进 `RemoteMeta`，以 D 本地 request ID 为 `reqs_to_recv` 的键；D 在 [L2283–2299](https://github.com/vllm-project/vllm/blob/b17039bccc17b94a2ea107272ad7bc93508708df/vllm/distributed/kv_transfer/kv_connector/v1/nixl_connector.py#L2283-L2299)把进程内 handle 关联到本地 request，而通知使用 P 的 remote request ID（[L2195–2197](https://github.com/vllm-project/vllm/blob/b17039bccc17b94a2ea107272ad7bc93508708df/vllm/distributed/kv_transfer/kv_connector/v1/nixl_connector.py#L2195-L2197)）。这几种身份不可仅以 `request_id` 一词合并。

**修订引入的同项错误**：L75 仍称 `RecvReqMeta/SendBlockMeta 经 ZMQ 传递`。实际 [D receive_kv L798–820](https://github.com/vllm-project/vllm/blob/b17039bccc17b94a2ea107272ad7bc93508708df/vllm/distributed/kv_transfer/kv_connector/v1/mooncake_connector.py#L798-L820)编码发送的是 `MooncakeAgentMetadata`；[L493–495](https://github.com/vllm-project/vllm/blob/b17039bccc17b94a2ea107272ad7bc93508708df/vllm/distributed/kv_transfer/kv_connector/v1/mooncake_connector.py#L493-L495)指定该解码类型，P listener 解码消费它。`RecvReqMeta` 是 connector 本地接收元数据，`SendBlockMeta` 含本地 `asyncio.Event` 与期限（[L77–110](https://github.com/vllm-project/vllm/blob/b17039bccc17b94a2ea107272ad7bc93508708df/vllm/distributed/kv_transfer/kv_connector/v1/mooncake_connector.py#L77-L110)），不能把它们写成跨端序列化负载。

**剩余关闭条件**：把 P 返回→proxy 转交→D 本地 request 键/远端身份→handle/通知消费串成实际字段链；Mooncake 分清本地类和线上 `MooncakeAgentMetadata`。没有独立稳定 transfer ID、HTTP 映射未核的边界继续保留。

### C03 · P2 · 满足，CLOSED

**位置**：正文 L77；来源记录 L60。

本地尺寸断言、跨端兼容前提、结构检查与内容语义检测已分开。逐段核对 Mooncake [L682–718](https://github.com/vllm-project/vllm/blob/b17039bccc17b94a2ea107272ad7bc93508708df/vllm/distributed/kv_transfer/kv_connector/v1/mooncake_connector.py#L682-L718)、[请求 warning L565–571](https://github.com/vllm-project/vllm/blob/b17039bccc17b94a2ea107272ad7bc93508708df/vllm/distributed/kv_transfer/kv_connector/v1/mooncake_connector.py#L565-L571)、[数量断言/寻址 L608–642](https://github.com/vllm-project/vllm/blob/b17039bccc17b94a2ea107272ad7bc93508708df/vllm/distributed/kv_transfer/kv_connector/v1/mooncake_connector.py#L608-L642)及 NIXL [L2220–2224](https://github.com/vllm-project/vllm/blob/b17039bccc17b94a2ea107272ad7bc93508708df/vllm/distributed/kv_transfer/kv_connector/v1/nixl_connector.py#L2220-L2224)，当前没有再把本地等字节数当成远端 dtype/shape/layout 校验，也未把 warning/断言当成恢复保证。错请求内容、损坏与 checksum 保留 unknown 合理；本项关闭不补足 C01 尚未写明的具体兼容条件。

### C04 · P2 · 部分满足，OPEN

**位置**：正文 L81–90；来源记录 L61。

**已满足**：NIXL 改为 D 发起 READ；完整 prefix 命中只通知、不产生远端读样本；区分 P 局部首输出、客户端合格 payload 与 D 局部 TTFT；把建议观察设计和官方跨实例拆分 unknown 分开。

**未满足**：当前五列表实际为“阶段/观察者/起终点/实现字段证据/未决”，**没有时间源**，与来源记录所称已补时间源不符。P 行仍用“请求入 P→P 返回”覆盖创建、prefill、KV 就绪几个不同事件，“P 侧请求日志”没有已核字段或时间戳；没有独立的 KV 就绪事件。客户端行只有收到 payload 的终点，没有请求提交起点。D 行把等待状态→decode 合并，没有为预分配完成、接收完成、复用/免传输分别给事件或标 unknown；prefix 免传输虽已出现于邻行备注，仍未形成可关联的 D 观察记录。

NIXL [READ 调用 L2283–2299](https://github.com/vllm-project/vllm/blob/b17039bccc17b94a2ea107272ad7bc93508708df/vllm/distributed/kv_transfer/kv_connector/v1/nixl_connector.py#L2283-L2299)和 [DONE 后取 telemetry L1973–1991](https://github.com/vllm-project/vllm/blob/b17039bccc17b94a2ea107272ad7bc93508708df/vllm/distributed/kv_transfer/kv_connector/v1/nixl_connector.py#L1973-L1991)证明调用和采样位置；不能因此把 READ 调用到轮询发现 DONE 的墙钟差直接等同库返回的 `xferDuration`。库本体精确计时边界未核部分仍须留白。

**剩余关闭条件**：按原条件补独立事件、观察进程/时间源、字段/unknown；可以设计 trace 事件与本地单调时钟，但必须标“建议新增”，不能用泛称日志补成现成字段。客户端提交→首个合格 payload 的窗口须完整；跨主机时间不可未经对齐直接相减。状态拼写另见 C08。

### C05 · P2 · 部分满足，OPEN

**位置**：正文 L92；来源记录 L62。

**已满足**：六个 raw 数据键及单位、四个 histogram/两个 counter 的实际注册名、MiB 被标为 MB、Throughput 的成功 duration 分母、每完成 handle 采样、失败计数不进 reduce、纯失败 getter 返回 None，均与 NIXL [L2406–2413](https://github.com/vllm-project/vllm/blob/b17039bccc17b94a2ea107272ad7bc93508708df/vllm/distributed/kv_transfer/kv_connector/v1/nixl_connector.py#L2406-L2413)、[L2483–2566](https://github.com/vllm-project/vllm/blob/b17039bccc17b94a2ea107272ad7bc93508708df/vllm/distributed/kv_transfer/kv_connector/v1/nixl_connector.py#L2483-L2566)、[L2594–2688](https://github.com/vllm-project/vllm/blob/b17039bccc17b94a2ea107272ad7bc93508708df/vllm/distributed/kv_transfer/kv_connector/v1/nixl_connector.py#L2594-L2688)吻合。没有以无指标推导无失败；Mooncake 无 stats override 的版本限定也保留。

**未满足**：仍未给出原关闭条件要求的 raw→CLI→Prometheus 对照；正文写“CLI reduce 标签”后只交代 MB 换算、Throughput 和 descriptors 均值，实际 `Num successful transfers`、`Avg xfer time (ms)`、`P90 xfer time (ms)`、`Avg post time (ms)`、`P90 post time (ms)`、`Avg MB per transfer`、`Avg number of descriptors` 的具体映射缺失。读者无法据这段识别成功数派生项、两个 duration 各自的 Avg/P90 毫秒输出，以及它们与秒级 histogram 的区别。缺口是字段/计算的完整对照，并非仅因没有使用 Markdown 表格。

**剩余关闭条件**：补紧凑映射表，注明 stats 中 duration 已是秒、CLI 两种时间 Avg/P90 转毫秒、成功数派生自样本数、bytes/descriptor 的汇总与 Prometheus 对应；保留当前已经核准的采样和失败缺口。无需修改上游实现或新增实测。

### C06 · P2 · 满足，CLOSED

**位置**：正文 L47、L96、L132；来源记录 L63。

政策已限定为 connector 检测并上报给 scheduler 的 KV 加载失败，排他保证已删除。基类[默认空集及完成信号契约 L358–376](https://github.com/vllm-project/vllm/blob/b17039bccc17b94a2ea107272ad7bc93508708df/vllm/distributed/kv_transfer/kv_connector/v1/base.py#L358-L376)、NIXL [invalid blocks 记录 L2020–2033](https://github.com/vllm-project/vllm/blob/b17039bccc17b94a2ea107272ad7bc93508708df/vllm/distributed/kv_transfer/kv_connector/v1/nixl_connector.py#L2020-L2033)及[取出上报 L2415–2424](https://github.com/vllm-project/vllm/blob/b17039bccc17b94a2ea107272ad7bc93508708df/vllm/distributed/kv_transfer/kv_connector/v1/nixl_connector.py#L2415-L2424)、scheduler [L1116–1123](https://github.com/vllm-project/vllm/blob/b17039bccc17b94a2ea107272ad7bc93508708df/vllm/v1/core/sched/scheduler.py#L1116-L1123)与 [L1872–1936](https://github.com/vllm-project/vllm/blob/b17039bccc17b94a2ea107272ad7bc93508708df/vllm/v1/core/sched/scheduler.py#L1872-L1936)支持此限定。

Mooncake 未 override 该接口，错误响应/接收异常的 [return 分支 L818–836](https://github.com/vllm-project/vllm/blob/b17039bccc17b94a2ea107272ad7bc93508708df/vllm/distributed/kv_transfer/kv_connector/v1/mooncake_connector.py#L818-L836)不被擅自解释为进入 recompute、必定挂死或必定失败；请求终态、D 资源回收与重试结果保持 unknown。连接/初始化与进程故障不再由配置推出结果。本项关闭不代表恢复过程经过运行验证。

### C07 · P2 · 部分满足，OPEN

**位置**：正文 L98–103、L133；来源记录 L64。

**已满足**：撤回 480s 统一兜底，明确 Mooncake 开始处理后期限改无穷，失败不能保证超时回收；正常完成区分 NIXL/Ascend 拉式通知与上游 Mooncake 写入成功后 P 标记完成；区分三层重试；进程故障不保证清理执行。

**未满足**：仍未说明 **480s 从何时开始计时**。NIXL 在 P 已完成且延迟释放的 `request_finished` 分支设置 `perf_counter()+timeout`（[L770–792](https://github.com/vllm-project/vllm/blob/b17039bccc17b94a2ea107272ad7bc93508708df/vllm/distributed/kv_transfer/kv_connector/v1/nixl_connector.py#L770-L792)）；Mooncake 在 worker 接到完成后的非空 block 列表时设置期限（[L856–872](https://github.com/vllm-project/vllm/blob/b17039bccc17b94a2ea107272ad7bc93508708df/vllm/distributed/kv_transfer/kv_connector/v1/mooncake_connector.py#L856-L872)），不是从“请求中止”事件统一计时。正文只有“已完成后的保留期限”和代码链接，未把这个区别写出。

阶段清单也仍缺 NIXL 在途失败时 D 的 handle/元数据与 KV 块的不同责任：源码会释放失败 handle 并标 invalid blocks（C06 证据），[get_finished L1861–1906](https://github.com/vllm-project/vllm/blob/b17039bccc17b94a2ea107272ad7bc93508708df/vllm/distributed/kv_transfer/kv_connector/v1/nixl_connector.py#L1861-L1906)另处理完成与元数据；这不等同于已证明 D 预分配 KV 全部回收。当前主要列了 P 端分支，未给这一阶段的 D 信号/责任或明确 unknown。原关闭条件允许 unknown，并不要求本轮完整逆向回收链。

**剩余关闭条件**：补两种计时起点和按轮询执行的性质；对未发起/在途失败/取消/正常完成分别简述 P、D 已见信号及资源责任，未闭合的 D KV 清理直写 unknown。保留现有保守边界，不恢复统一恢复保证。新增 60000ms 的错误锚点并入 C08。

### C08 · P3 · 部分满足，OPEN

**位置**：正文 L74、L86–87、L101、L109、L113；来源记录 L65。

**已满足**：`kv_connector_extra_config.connectors` 正确；Mooncake bootstrap 说明已指向 L43–48；元数据类与跨端 listener 有分开的固定链接；toy proxy、XpYd 已恢复近旁入口；Ascend 限制有 L103–105 锚点；DFX 保留设计声明/实现未验证。

**仍有明确错误**：正文 L87/L113 继续写 `RequestStatus.WAITING_FOR_REMOTE_KV`，L113 与来源记录 L65 还新增“指南原文为此”的说明。已核 SHA-256 为 `b9c9772f7ec08fb9c10daa0b2bc8da353b368234af2839ef596adf084abf846d` 的指南 [L45](https://github.com/vllm-project/vllm-ascend/blob/52d4acfa51fb868823d1070b81cbd2d97e9e4696/docs/source/developer_guide/feature_guide/disaggregated_prefill.md#L45)和 [L51](https://github.com/vllm-project/vllm-ascend/blob/52d4acfa51fb868823d1070b81cbd2d97e9e4696/docs/source/developer_guide/feature_guide/disaggregated_prefill.md#L51)均为 **`RequestStatus.WAITING_FOR_REMOTE_KVS`**。registry 的 Ascend notes 与来源记录主表 L36 也保留带 S 的正确形态；不存在可用“原文照录”解释的快照差异。

**修订新增的定位错误**：L101 的 Mooncake ZMQ `60000ms` 链接跳到 P `_sender_worker` 的 L547–557，那里没有超时设置；实际是 D `receive_kv` 的 [`sock.setsockopt(zmq.RCVTIMEO, 60000)`，L818](https://github.com/vllm-project/vllm/blob/b17039bccc17b94a2ea107272ad7bc93508708df/vllm/distributed/kv_transfer/kv_connector/v1/mooncake_connector.py#L814-L821)。L74、L86 等单链接文字列两段行号时只锚定其中一段；Ascend 编译虽写了 L100–141，教程 URL 仍无该段锚点。ABORT 默认值/文档语义也宜分别近旁锚定 NIXL usage L98–101 与 [Mooncake usage L50–52](https://github.com/vllm-project/vllm/blob/b17039bccc17b94a2ea107272ad7bc93508708df/docs/features/mooncake_connector_usage.md#L50-L52)，不能把已经修好的 bootstrap L43–48 当成 ABORT 证据。

**剩余关闭条件**：改为带 S 的状态名并撤回错误“原文”说明，来源记录同步；修正 60000ms 的 D 端锚点，将多段证据及[编译教程 L100–141](https://github.com/vllm-project/vllm-ascend/blob/52d4acfa51fb868823d1070b81cbd2d97e9e4696/docs/source/tutorials/pd_disaggregation_mooncake_single_node.md#L100-L141)分别定位。

### C09 · P3 · 满足，CLOSED

**位置**：输出质量页 L110；来源记录 L66。

质量页 PD 提及处已增加指向 `pd-disaggregation.md` 的普通 Markdown 链接，目标存在。本轮按 YAML 实际解析核对 PD 与布局、加载、质量三页，**三对关系的双向 related_ids 与双向普通正文链接全部存在**。本项仅确认导航可达，不重审质量页其余修订。

### C10 · P2 · 部分满足，OPEN

**位置**：正文 L105、L115、L135、L142；来源记录 L38、L46、L67。

**正文已满足**：改为底层传输协议/完整路径/指标未核，承认开源封装与局部检查；`pull_blocks`/CANN 异常、远端 instance 与目标 block 越界检查、`TransferOutputHandler` 的 request ID/取消后结果/失败回调，分别与 [Python L432–452](https://github.com/Ascend/MindIE-LLM/blob/69e5a5dd4b533eaffc7e198320435350825a36f7/mindie_llm/text_generator/utils/separate_deployment_engine.py#L432-L452)、[L575–603](https://github.com/Ascend/MindIE-LLM/blob/69e5a5dd4b533eaffc7e198320435350825a36f7/mindie_llm/text_generator/utils/separate_deployment_engine.py#L575-L603)、[C++ L24–58](https://github.com/Ascend/MindIE-LLM/blob/69e5a5dd4b533eaffc7e198320435350825a36f7/src/engine/transfer_output_handler.cpp#L24-L58)相符。外部 `llm_datadist` 导入与占位类的边界也正确，没有由局部代码推出完整协议或部署保证。

**来源记录未满足同步撤回条件**：L38 仍写“connector 实现不在开源仓（unknown）”；L46 仍写“KV connector 实现不在开源仓（T07-03 已记）”。L67 仅在修订清单声明已收窄，并未将主表/unknown 的旧断言标为撤回或被替代。当前阅读者仍会同时取得两个冲突结论；括注 unknown 也不消除“全仓缺位”的实体断言。若要保留原取证历史，应明确划分“旧结论已撤回/当前结论”，不能依赖读者猜测末尾清单覆盖前文。

**剩余关闭条件**：同步更正或明确废止这两处旧结论与错误 T07-03 归因。registry 当前 MindIE notes 未再出现“全仓无实现”的直接断言，但也未补本轮局部源码取证范围；新增代码证据的登记/关联缺口单列 N01，不重复计入本项。

## 新问题

### N01 · P3 · OPEN · 新增 MindIE 源码证据未关联到对应源码来源

**位置**：正文 frontmatter L8–11、L24–28、L105/L140；来源记录 L52–53/L67；registry 的 `src.ascend.mindie-llm-docs-69e5a5dd`、`src.ascend.mindie-llm-src-69e5a5dd` notes。

本次修订首次在正文实质引用 `mindie_llm/.../separate_deployment_engine.py`、`kv_transfer_agent.py` 与 `src/engine/transfer_output_handler.cpp`，但 `source_refs` 与 `evidence_refs` 仍只有原来的三项，MindIE 仍只挂 **docs 树登记**；verification notes 已声称核了源码，来源关系却没有跟进。docs 登记的 URL/scope 与文档许可口径不能自动覆盖这些源码文件。已存在的仓库源码来源 `src.ascend.mindie-llm-repo-69e5a5dd` 可覆盖 Python 路径，`src.ascend.mindie-llm-src-69e5a5dd` 可覆盖 C++ `src/` 路径；无需因此认定要新建来源 ID。

来源记录还称“全部文件落在既有三个固定快照 scope”“registry notes 同步收窄”，实际对应 notes 没有新增的 `separate_deployment_engine/TransferOutputHandler/LLMDataDist` 取证说明。固定 commit 相同不代表 docs/source 的登记范围和许可自动合并。按[写作指南第 5 节](../authoring-guide.md#5-来源证据与许可)，近旁 URL 与机器可追踪的来源关系应配套。

**关闭条件**：给新增源码主张关联适当的既有源码来源 ID，按各自 scope 补 notes/来源记录，区分源码和文档许可；无需取回底层依赖、扩大 MindIE 逆向范围或宣称库本体已经验证。

其余修订新增问题中，Mooncake 本地类被误作 ZMQ 负载已纳入 C02；错误的 Ascend“原文”说明和 60000ms 锚点已纳入 C08，均不重复分配新 ID。未将初审通过部分重新计为本轮发现。

## 整体结论

**本轮定向复核不通过，需继续修订并复核。** C03、C06、C09 关闭；C01、C02、C04、C05、C07、C08、C10 部分满足，保持 OPEN；另新增 N01。修订已消除本地断言、失败政策与统一超时的多处过度保证，但可执行的兼容条件、身份字段链、观察事件/时间源、指标映射、分阶段清理说明仍未完整交付，精确状态名和来源记录也未全部对齐。

后续只需围绕上述剩余关闭条件处理，不要求重做整篇初审、补库本体兼容矩阵或立即开展硬件实验。保留 `draft / source_checked`，已关闭项仅代表对应文字与源码/导航证据满足本轮条件，不代表平台可运行、恢复成功或输出质量等价。

已执行 `make check`、`make build`，均通过：**112 content entries / 542 sources**。这些检查只验证结构及本地文件链接，不验证技术正确性、远程链接或真实平台行为。未修改 `src/kb/`，未新增测试，未执行硬件验证。

交付前逐文件 SHA-256 比对确认，入场时已有的全部源文件均未变化。本轮只新增本报告并重建忽略目录 `build/`；期间另有 `batch-27-t07-05-codex-recheck.md` 出现在工作区，本轮未写入或修改它。

统计：初审项复核 10 项（CLOSED=3，OPEN=7；开放 P2=6、P3=1）；新问题 1 项（P1=0，P2=0，P3=1；OPEN=1）；当前开放合计 8 项（P1=0，P2=6，P3=2）；make check=PASS；make build=PASS；硬件验证=未执行；整体=需继续修订并定向复核。
