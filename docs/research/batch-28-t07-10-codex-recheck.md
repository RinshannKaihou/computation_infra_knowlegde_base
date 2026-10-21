# Batch 28 · T07-10 定向复核报告

## 会话元数据与结论

| 项目 | 记录 |
|---|---|
| 审阅角色 | 承接[初审](batch-28-t07-10-codex-review.md)的独立审阅者，复核 C01–C11 全部关闭条件及修订引入的问题；本会话未编写或修订被审正文 |
| 实际执行模型 / 档位 | `gpt-6.1-sol / xhigh` |
| 模型核验 | 读取 `CODEX_THREAD_ID` 对应本地 JSONL 的 `session_meta` 和全部 `turn_context`；本轮仅见 `model=gpt-6.1-sol`、`effort=xhigh`，与 `collaboration_mode.settings` 一致；assistant 消息未检出 fallback 标记。本轮没有另启模型或子代理 |
| 本轮会话 ID | `01a15d6c-b144-7aa2-9d22-0fcd9efa73fa` |
| 初审会话 ID | `01a15d55-154e-78a2-9501-47c240e15641`；沿用其发现编号、优先级和关闭条件 |
| 执行方式 | 本地 Codex CLI，`originator=codex_exec`、`source=exec`、`cli_version=0.163.0`；静态定向复核 |
| 日期 / 时区 | 2026-10-21 / Asia/Shanghai |
| 工作目录 | `/Users/ywang2397/work/AI_reliability_knowledge_base` |
| 修订正文 | [release-and-recovery.md](../../knowledge/07-inference/release-and-recovery.md)，109 行 |
| 提交的正文 SHA-256 | `a3c16f4c1eaffd9855a941ca5063d3507e5a69eb5a1430a1447804695b574b69` |
| 独立计算的正文 SHA-256 | `a3c16f4c1eaffd9855a941ca5063d3507e5a69eb5a1430a1447804695b574b69`，**匹配** |
| 作者来源记录 SHA-256 | `4d6348ced07cff9fa17daf9d5c124e40439ac6cb8fa8de27577f94f07dfab354` |
| 写入范围 | 仅新增本报告；不修改正文、来源记录、registry、导航、计划或审核状态。`make build` 只重建忽略的生成物 |

**结论：本轮暂不通过。C01–C11 中，CLOSED=7（C01/C04/C05/C08/C09/C10/C11），OPEN=4（C02/C03/C06/C07，均沿用 P2）；新增 N01（P2，OPEN）。合计开放 P1=0、P2=5、P3=0。**

正文的大部分修订已落实；但来源记录的现行主张表、unknown 与末尾修订摘要仍有冲突。另一个执行边界是：KServe 文档规定旧版 Ready 后即按保留权重重新接流，正文尚未说明怎样保证所要求的预热/质量 gate 先于接流。报告交付和结构检查通过均不代表这些问题关闭。

## 方法与证据边界

已读取仓库 `AGENTS.md`、[README](../../README.md)、[写作指南](../authoring-guide.md)、[内容总目录](../../content-outline.md)及元数据 schema；重读初审全部关闭条件、修订正文、[来源记录](batch-28-t07-10-sources.md)的主张表与 unknown、[registry](../../sources/registry.yaml)的相关条目和 T07-10 acceptance。沿链接核对路由、PD、缓存身份及 05 域责任边界；关联页仅用于本轮问题定位，不重新初审其他任务。

本轮重新计算并实际读取固定缓存，源码坐标采用原文件行号：

| 文件 | 本轮计算的 SHA-256 前 16 位 |
|---|---|
| `/tmp/b28/vllm/api_server.py` | `dcc6b46ca859074d` |
| `/tmp/b28/vllm/vllm_v1_engine_async_llm.py` | `818af4561b7ae54a` |
| `/tmp/b28/vllm/core.py` | `a7a624e0ed151f00` |
| `/tmp/b28/vllm/core_client.py` | `601d375067fa724e` |
| `/tmp/b28/vllm/output_processor.py` | `381c443e029c4cd8` |
| KServe predictive `rollout-strategies/canary.md` | `fee7893a614ebab8` |
| KServe generative `llmisvc/canary-rollout.md` | `89013ecf8dec6244` |
| `/tmp/b28/pod-lifecycle.html` | `3b6cd176dbbf06cb` |
| vLLM `kv_connector/v1/base.py` | `00fc529df6dc944f` |
| vLLM `kv_connector/v1/nixl_connector.py` | `bcf8980a73c23945` |
| vLLM `kv_connector/v1/mooncake_connector.py` | `dd7d60072bfd64ba` |
| vLLM `v1/core/sched/scheduler.py` | `b4e664fe7dc9ea5c` |

KServe 缓存根目录为 `/tmp/b28/kserve-web/docs/model-serving/`，pin 为 `3f4067ea87dd84194bddb1b563051c84306c7997`；后四份 vLLM 文件位于 `/tmp/vllm-b17039bccc17b94a2ea107272ad7bc93508708df/vllm/`。vLLM 版本仍为 `b17039bccc17b94a2ea107272ad7bc93508708df`，未导入、安装或运行服务代码。前八份缓存摘要与初审所记录的一致；其余为本轮从既有完整源码缓存读取的补充证据，不冒称都列于 T07-10 原取回清单。

尝试重新打开 K8s/Envoy 精确页时，网页工具返回 HTTP 429；GitHub 文件工具返回不可用；终端访问 K8s URL 时 DNS 解析失败。因此本轮没有成功重取远端页面的记录。K8s/KServe/vLLM 的技术判断以实际重读的缓存原文为依据；Envoy/SRE 仅核对本轮涉及的引用定位与原有边界，不宣称独立重验其完整远端内容。缓存一致性也不单独证明远端 tag 解析或部署兼容。

下文正文行号绑定上述正文哈希；来源记录行号绑定上述来源记录哈希。末尾修订摘要并未把前面的主张表或 unknown 标成已废弃历史，因此不能仅据摘要认定旧主张已被替换。

## C01–C11 逐项判定

| 编号 / 原优先级 | 判定 | 理由与证据 |
|---|---|---|
| C01 · P2 | **CLOSED** | 正文 L55–57 已加入目标/剩余容量、新准入停止与入口收敛观察、在途完成/取消核对、预登记等待期限、超时终止与终态不确定记录、进程/设备回收六步；区分端点变化、连接层 GOAWAY、请求终态和资源回收。preStop 共用宽限期、一次性延展和镜像 `STOPSIGNAL` 的运行时差异已补，与缓存 [K8s v1.32 终止流程](https://v1-32.docs.kubernetes.io/docs/concepts/workloads/pods/pod-lifecycle/#pod-termination-flow)一致。原“缺少 drain 执行闭环”已修；新加括号把未知写成否定事实，另记 N01，不重复计入原缺项。 |
| C02 · P2 | **OPEN** | 正文 L59 已正确分写四项职责，EngineDead 锚点也已改为 L455–459；但来源记录 L25 仍写“lifespan 退出时经 build_async_engine_client……调 async_llm.shutdown()”，并仍把已经可见的外层 shutdown task 等待逻辑统称“未逐行分析”。与正文 L59、同记录 L41 的修订摘要不一致，未满足初审明确要求的正文、verification notes 与取证记录一致。见剩余条件。 |
| C03 · P2 | **OPEN** | 正文 L55/L61/L89 已正确区分旧版运行/已停、声明权重/运行态、9:9 恢复后的 50/50、完全隔离需核对直达路径及冷启动计时；但“等 Ready/预热/质量 gate 后按保留权重重新入组”缺少阻止提前接流的前提。[固定回退段 L250–257](https://github.com/kserve/website/blob/3f4067ea87dd84194bddb1b563051c84306c7997/docs/model-serving/generative-inference/llmisvc/canary-rollout.md#L250-L257)规定 Ready 后即按保留权重入组，不提供独立质量 gate。未说明如何把 gate 纳入准入/路由隔离，就不能保证正文所述次序。仍落在原 C03 对“旧版可服务、gate 与实际流量达到目标”的关闭条件内，不另立 N 编号。 |
| C04 · P2 | **CLOSED** | 正文 L70 已按 MindIE 与上游 connector 分开证据，将 480s 限定于 P 侧保留项的条件超时，并保留进程死亡不保证清理、Mooncake 错误终态未证。重读 [NIXL L770–792](https://github.com/vllm-project/vllm/blob/b17039bccc17b94a2ea107272ad7bc93508708df/vllm/distributed/kv_transfer/kv_connector/v1/nixl_connector.py#L770-L792)、[Mooncake L565–593](https://github.com/vllm-project/vllm/blob/b17039bccc17b94a2ea107272ad7bc93508708df/vllm/distributed/kv_transfer/kv_connector/v1/mooncake_connector.py#L565-L593)与 [L746–764](https://github.com/vllm-project/vllm/blob/b17039bccc17b94a2ea107272ad7bc93508708df/vllm/distributed/kv_transfer/kv_connector/v1/mooncake_connector.py#L746-L764)，期限/无穷/轮询限定成立。base L358–376 默认空集、NIXL L2415–2424 上报、scheduler L1116–1123 按 invalid blocks 处理也支持 recompute 的作用条件；与[PD 失败链](../../knowledge/07-inference/pd-disaggregation.md#失败链取消与清理)一致，不再给出通用清理或恢复保证。 |
| C05 · P2 | **CLOSED** | 正文 L68/L76/L78 已删除“唯一防线”，区分关联 ID、展示去重、服务端幂等和外部副作用协议；引入未建连/送达后未知/响应已提交三分重试边界，并限定本轮普通 chat/completion 无续传契约证据。取消返回与资源回收分开。重读 [OutputProcessor L393–424](https://github.com/vllm-project/vllm/blob/b17039bccc17b94a2ea107272ad7bc93508708df/vllm/v1/engine/output_processor.py#L393-L424)及 [async_llm L448–459](https://github.com/vllm-project/vllm/blob/b17039bccc17b94a2ea107272ad7bc93508708df/vllm/v1/engine/async_llm.py#L448-L459)，未再从 ID 或 abort 推出执行一次保证。 |
| C06 · P2 | **OPEN** | 正文 L77/L88 已按本地与外部所有者限定缓存生命周期、身份与实际命中，TTFT 仅为联合观察；但来源记录 unknown 3（L34）原样保留“缓存内容随进程消失，重拉副本为冷 cache”“跨副本 cache 恢复只有 PD connector/offload 路径”。它仍把全部缓存统一归入进程状态，并把传输路径当恢复范围，与正文及同记录 L45 相冲突；未满足原关闭条件要求的正文与来源 unknown 一致。 |
| C07 · P2 | **OPEN** | 正文 L68 已正确区分启动失败、运行期异常与突然退出，且不会因缺 marker 排除死亡；但来源记录 L25 仍把两种 EngineCore 日志统一连到 ENGINE_CORE_DEAD。正文还把已引用函数中可直接看到的 sentinel 局部条件全留 unknown，没有列出最低限度的适用条件。固定 [core.py L931–943](https://github.com/vllm-project/vllm/blob/b17039bccc17b94a2ea107272ad7bc93508708df/vllm/v1/engine/core.py#L931-L943)与 [core_client.py L583–621](https://github.com/vllm-project/vllm/blob/b17039bccc17b94a2ea107272ad7bc93508708df/vllm/v1/engine/core_client.py#L583-L621)支持现有正文的主要修订，但仍需同步取证记录、补可核 guard；完整 worker→core 传播继续 unknown。 |
| C08 · P2 | **CLOSED** | 正文 L54 要求各 gate 预登记指标、单位、窗口、分母与方向；L62 明确错误/取消率高于上限、延迟分位超过上限、达标率/goodput 低于下限、质量超容差。延迟改善不再被当作回退触发，未补造通用阈值；L85/L88/L89 的观察与回退沿用这些判据。 |
| C09 · P2 | **CLOSED** | 正文 L86 已分列触发、发现、控制面、数据面最后选中旧副本、恢复版接流与回稳定时刻，明确收敛和用户中断分别报告；L87 按逻辑请求＋attempt 记录接纳、提交、终态与版本，并定义重复完整响应、超截止点无终态及预登记分母/截止点；L88/L90 补达标/超时判据与停止后撤压、恢复配置、副本、路由、SLO/质量/资源的闭环。原混算与“发 N 收 M”推断已移除。该对账仍不证明重复执行被排除或具有 exactly-once，正文也未作此承诺；真实参数与结果仍待授权演练填写。 |
| C10 · P3 | **CLOSED** | 正文 L52 已将 weight:0 风险归为文档的条件性理论，明确 weight:1 的真流量及对全部活跃权重的依赖；补控制器/Gateway 前置与实现未核。成员差异形成独立子组及 `GroupDegraded=True / MemberDivergence` 已补，分别符合固定 [dark/live L61–67](https://github.com/kserve/website/blob/3f4067ea87dd84194bddb1b563051c84306c7997/docs/model-serving/generative-inference/llmisvc/canary-rollout.md#L61-L67)及[成员约束 L152–156](https://github.com/kserve/website/blob/3f4067ea87dd84194bddb1b563051c84306c7997/docs/model-serving/generative-inference/llmisvc/canary-rollout.md#L152-L156)。 |
| C11 · P3 | **CLOSED** | 正文 L90 新增[平台变更与回退](../../knowledge/05-cluster-platform/platform-change-and-rollback.md)、[控制面恢复](../../knowledge/05-cluster-platform/control-plane-recovery.md)两个普通链接并说明平台/请求责任；L104 分列 predictive/generative canary，L106 分列 overload 架构、配置及 outlier 架构页。目标与登记 URL、标签范围对应，本地文件链接均存在。关闭的是导航/精确页面定位问题，不表示本轮成功重新访问了这些远端页面。 |

## OPEN 项的最小剩余条件

### C02：同步现行来源主张表的关闭责任

**位置：来源记录 L25；正文 L59；来源记录 L41。** 源码实际分工已经核清：

- [lifespan L117–143](https://github.com/vllm-project/vllm/blob/b17039bccc17b94a2ea107272ad7bc93508708df/vllm/entrypoints/openai/api_server.py#L117-L143)取消统计任务并删除 `app.state`；它不调用 `async_llm.shutdown()`。
- [engine context L229–232](https://github.com/vllm-project/vllm/blob/b17039bccc17b94a2ea107272ad7bc93508708df/vllm/entrypoints/openai/api_server.py#L229-L232)在 finally 调用引擎 shutdown；[L1371–1373](https://github.com/vllm-project/vllm/blob/b17039bccc17b94a2ea107272ad7bc93508708df/vllm/entrypoints/openai/api_server.py#L1371-L1373)在 backend context 退出后等待 HTTP shutdown task。

**关闭所需：** 就地改来源记录 L25 的责任归属和已知顺序；保持正文 L59、verification notes 与现行取证表一致。`serve_http`/uvicorn 完整行为和在途流终态继续 unknown。本项不需要扩查整个 HTTP 关闭实现，也不要求实测。

### C03：Ready 自动接流与发布者要求的 gate 必须分开

**位置：正文 L61，关联 L52/L89。** 文档明确 Ready 后即以保留权重重新加入加权路由。正文没有证据表明控制器会额外等待发布者的预热或质量核对，也没有说明接流前的隔离/准入机制。静态代入同一示例：v1/v2 均为 9，去 stop 后 v1 一旦 Ready 即可承担约一半组内流量；随后执行质量核对不能追溯成“核对完成后才接流”。这是从固定文档顺序作出的条件推导，未声称本地观测到该流量。

**关闭所需：** 明确“Ready 即按保留权重接流”的样板语义。若要求预热/质量通过后才接流，必须把经核对的 readiness 准入门或入口隔离列为前提，说明 gate 期间如何阻止组内及直达路径提前选中旧版，gate 通过后再放开并核对实际流量；机制未实现时标为缺失。若采用先接流再验证的方案，则明确是带流验证及其预登记预算/停止条件，不声称质量 gate 已在接流之前完成。保留现有部分回退/完全隔离、权重目标和冷启动计时。

不要求发明新的 KServe 字段或给出未验证命令；仅写“去注解后再等 gate”仍不足以关闭。

### C06：替换来源 unknown 3 中的缓存绝对结论

**位置：来源记录 L34；正文 L77/L88。** 来源 unknown 仍以“正文按此写”指向已被替换的旧结论，末尾 L45 的修订摘要不能让该现行条目自动消失。[缓存身份边界](../../knowledge/07-inference/execution-and-kv-cache.md#prefix-cache-的复用边界)要求分清所有者、精确 token/block、LoRA、多模态与隔离条件；找到外部缓存或具备 PD 交接路径均不证明跨版本恢复。

**关闭所需：** 就地将 unknown 3 改成与正文一致的限定：仅被终止进程的本地状态不自动继承；外部/offload 的幸存、重挂载、身份兼容与会话恢复契约按实现核对，无证据即 unknown。去掉“只有 PD/offload”作为恢复能力边界的断言。无需通过新增部署证据消除这些合理未知。

### C07：修来源统一链，补 sentinel 已可核的局部条件

**位置：来源记录 L25；正文 L68。** `core.py` L934–940 在 `engine_core is None` 时仅记录启动失败并抛异常；只有另一个运行期异常分支发送 marker。来源表仍将两者合并，须就地拆开。

同时，[监控函数 L583–595](https://github.com/vllm-project/vllm/blob/b17039bccc17b94a2ea107272ad7bc93508708df/vllm/v1/engine/core_client.py#L583-L595)已经显示：`resources.engine_manager` 必须存在、具有 `processes` 属性且列表非空，否则直接返回、不启动该监控线程。该局部 guard 可以直接记录；它并不证明每种部署均满足，也不补全 worker→core 传播。

**关闭所需：** 来源记录将启动失败/运行期 marker/突然退出 sentinel 三种路径分列；正文至少补以上可核 guard，再把尚未核对的部署可达条件、完整 worker→core 传播与根因区分继续列 unknown。保留缺 marker 不能排除死亡的限定，不要求所有故障产生同一组日志。

## 新发现

### N01 · P2 · OPEN：新增 drain 括号把“不假设自动排空”写成已知“不自动排空”

- **位置：正文 L57**，新增“引擎不自动排空在途流——该不假设保留”。
- **问题：** 前半句是否定实现行为的事实断言。它不同于“本流程不依赖自动 drain”，也不同于“尚无自动排空保证的证据”。正文 L59/L97 同时承认完整 `serve_http`/uvicorn 关闭与在途流行为未核，所读 `api_server.py` 局部顺序也不足以证明一定不会自动排空。后半句“该不假设保留”不能消除前半句的事实含义。
- **影响：** 读者可能把证据缺口当作引擎确定没有的能力，混淆人工 drain 的部署要求与 HTTP/引擎实现事实。这是本轮新增语句的问题；C01 原缺少分阶段流程的修订仍成立。
- **关闭条件：** 改为“本流程不假设引擎会自动排空；完整在途流行为仍待核实”或等价限定，与 L59/L97 一致。无需反向证明引擎一定能 drain，也无需为该措辞项执行演练。

未将同一处来源记录冲突或 C03 的 gate 剩余条件另立 N 编号，避免重复计数。除 N01 外，本轮未确认其他需要独立编号的新增问题；这不代表对关联页或其他批次作了全量技术背书。

## 检查与验证声明

本轮实跑 `make check` 与 `make build`，均成功，退出码为 0：**117 content entries / 553 sources**；构建生成 `build/catalog.json` 与 `build/catalog.md`。另行解析正文 18 处及本报告 11 处内联本地文件链接，全部目标存在；`git diff --check` 通过。检查只覆盖结构、登记引用及本地文件目标，不验证技术正确性、远端可达性、页内锚点语义或真实环境行为。

落盘后再次计算正文 SHA-256，仍与提交值一致，作者来源记录摘要也未变。本会话的仓库写操作只有新增本报告。基线对比另观察到容量页及其他任务报告的并行变更，本会话未对其写入；以上结构检查数字为命令运行时的结果。

本轮未修改 `src/kb/`，不新增或运行其回归测试。正文仍为 `draft / source_checked`，没有建立真实环境档案；`generic/nvidia/amd/ascend` 标签不证明共同兼容。没有启动推理服务、修改集群、发布、终止副本或执行故障注入，没有硬件实测结果。

开放的 C02/C03/C06/C07/N01 仍须修订并定向复核。在此之前，不将 T07-10 或 Batch 28 宣告为审阅通过。
