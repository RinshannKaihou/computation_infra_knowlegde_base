# Batch 28 · T07-09 定向复核报告

## 会话元数据与结论

| 项目 | 记录 |
|---|---|
| 角色与范围 | 独立审阅者，承接[初审](batch-28-t07-09-codex-review.md)的 C01–C10 关闭条件，检查相关修订引入的问题；未编写或修改被审正文 |
| 实际执行模型 / 档位 | `gpt-6.1-sol / xhigh` |
| 模型核验 | 读取 `CODEX_THREAD_ID` 对应本地会话 JSONL 的最新 `turn_context`，实见 `model=gpt-6.1-sol`、`effort=xhigh`，与 `collaboration_mode.settings` 一致；本轮未另启模型、审阅 CLI 子进程或子代理，无模型 fallback 轮次 |
| 本轮会话 ID | `01a15d69-d068-7b01-ab36-cbd8d86fe603` |
| 执行方式 | 本地 Codex CLI，`originator=codex_exec`、`cli_version=0.163.0`；直接读取正文、固定源码缓存及历史原始工具回包 |
| 日期 / 时区 | 2026-10-21 / Asia/Shanghai |
| 工作目录 | `/Users/ywang2397/work/AI_reliability_knowledge_base` |
| 修订正文 | [capacity-and-autoscaling.md](../../knowledge/07-inference/capacity-and-autoscaling.md)，108 行 |
| 作者提交的正文 SHA-256 | `2e30ebbfed03c7886a551da3bf22213f3e47acdebb584b1fa77e4962a612c113` |
| 独立计算的正文 SHA-256 | `2e30ebbfed03c7886a551da3bf22213f3e47acdebb584b1fa77e4962a612c113`，**匹配** |
| 写入范围 | 仅新增本报告；不修改正文、来源记录、registry、导航、任务账本或审核状态 |

**结论：暂不通过。C01–C10 中 CLOSED=6（C03/C04/C05/C08/C09/C10），OPEN=4（C01/C02/C06/C07，均沿用 P2）；新增 N01（P2，OPEN）。合计开放 P1=0、P2=5、P3=0。** C11 沿用初审收尾的 CLOSED 状态，本轮不重新判定。

正文已完成大部分关键收缩，但来源主张表仍与修订后正文冲突，token 触发器比较和 KServe 前置分支仍有缺口；新增的“进程内”限定也不符合固定实现。以下正文行号均以本表哈希为准。

另两份被检文件的取样摘要如下；这是本轮读取的字节身份，不代表本轮修改这些文件：

| 文件 | SHA-256 |
|---|---|
| [T07-09 来源记录](batch-28-t07-09-sources.md) | `74e51b700f18e7c6ad5a1d576cde903c26253416b90832d9a6cfbe08a1db75ab` |
| [来源登记](../../sources/registry.yaml) | `abecd29b5c7f9527919f8bde9fc900aa9a37d73048aa558d3e272b6c99d7bd18` |

## 方法与证据边界

已读取仓库 `AGENTS.md`、[README](../../README.md)、[写作指南](../authoring-guide.md)、[内容总目录](../../content-outline.md)、元数据 schema、[T07-09 任务验收](../../plans/full-coverage-backlog.yaml)及初审关闭条件；完整重读修订正文、来源记录和相关 registry 条目。修订摘要仅用作定位，不替代文件内容。沿链接核对延迟指标、路由对照、ready/发布及 PD 的相关边界，没有重审 T07-08/10/11 全文。

重新计算并读取以下既有缓存，SHA-256 前缀均与作者记录或初审取样相符。vLLM 固定于 `b17039bccc17b94a2ea107272ad7bc93508708df`，KServe 网站仓固定于 `3f4067ea87dd84194bddb1b563051c84306c7997`，production-stack 固定于 `20a658044af0dea70e9e0136494bb9979cfd9fab`。上游锚点使用原文件坐标。

| 本地缓存 | SHA-256 前 16 位 |
|---|---|
| `/tmp/b28/vllm/vllm_v1_engine_async_llm.py` | `818af4561b7ae54a` |
| `/tmp/b28/vllm/elastic_ep_middleware.py` | `46da705bc65f83c8` |
| `/tmp/b28/vllm/gpu_worker.py` | `eb33b5f2bd389ac3` |
| `/tmp/b28/vllm/core_client.py` | `601d375067fa724e` |
| `/tmp/b28/vllm/conserving_memory.md` | `895bc42beb0ff505` |
| KServe `kpa-autoscaler.md` | `b8f04c9dad91aa14` |
| KServe `hpa-autoscaler.md` | `a554223d86ac0880` |
| KServe `keda-autoscaler.md` | `e71de56eb95d6af8` |
| KServe `llmisvc-autoscaling.md` | `880fb8a6c1e57c91` |
| production-stack `autoscaling-keda.rst` | `391c98658ab19d2c` |
| production-stack `sleep-wakeup-mode.rst` | `d62f16d2ac62184d` |

KServe 缓存根目录为 `/tmp/b28/kserve-web/docs/model-serving/`，production-stack 教程位于 `/tmp/b28/production-stack-vllm-stack-0.1.9/docs/source/use_cases/`。`core_client.py` 的取回哈希可在同批 [T07-08 来源记录](batch-28-t07-08-sources.md)中定位；本轮只补读与 N01 有关的调用实现。哈希一致证明缓存字节身份，不单独证明远端 tag 解析、完整版本配套或运行成功。

本轮网络复取未成功：网页工具返回 HTTP 429；GitHub 文件工具返回不可用；终端读取 Kubernetes 精确 URL 时 DNS 解析失败。为复核 C10，读取初审会话 `01a15d4c-78f0-7053-956e-7f69e52e2c75` JSONL 中保存的**原始工具回包**，没有把先前报告的结论当成重新打开网页：

| 历史原始证据 | 定位与本轮使用范围 |
|---|---|
| Kubernetes v1.32 HPA 页面回包 | JSONL 第 77 行，`2026-10-21T07:13:58.534Z`，`call_1c5e272659ef47dbb8664045842a075d`；实际可见的算法、利用率/原始值区别、稳定窗与默认 behavior 段 |
| HPA 算法补充回包 | JSONL 第 145 行，`2026-10-21T07:15:59.285Z`，`call_81e47f85dd1948c9b54d7f77c6dfd7b5`；实际可见的同步默认、指标与 requests 相关段 |

以上是对历史取证内容的复核，不是本轮新取得的远端响应，也不据此证明远端页面当前未变。WVA 控制器内部、KEDA 完整激活语义及 sleep 完整恢复链仍未取证。

## C01–C10 逐项判定

| 编号 / 原优先级 | 判定 | 理由与证据 |
|---|---|---|
| C01 · P2 | **OPEN** | 正文 L66 已拆开副本 ready 与 EP 排空，300s 超时、停止保据、新进入 HTTP 请求/在途流边界和标志 unknown 均已落实；registry L536 也同步，并保留同尺寸直接返回分支。但来源记录 L25 仍把“扩缩容期间 HTTP 请求被 503”列为主张，没有状态条件、新请求边界及超时分支。L40 追加回应没有将主张表标为已取代，原“正文、取证及 registry 摘要一致”的关闭条件尚未满足。新引入的“进程内”问题另记 N01，不与此处残留重复计数。 |
| C02 · P2 | **OPEN** | 正文 L65/L68/L96 已取消统一重载保证，并把未知数值收窄为本部署基线未取得；但来源记录 L26 仍写“唤醒需重载／唤醒耗时数值未给”，L27/L34 仍写无官方耗时数值，L41 的修订摘要没有消除现行主张表与 unknown 清单的相反断言。正文 L95 也仍称“仅引用教程”，与 L68 已引用固定 worker 分支不一致。原关闭条件明确要求正文与取证 unknown 一致，尚未完成。 |
| C03 · P2 | **CLOSED** | 正文 L71 已标为本库规划建议，以故障模型、恢复窗口、剩余 SLO 容量与故障域为输入；≥2 是有条件示例，明确数量不保证可用性、实际 ready 数可能低于配置下限，具体下限待定。未把来源或配置下限当作故障容错证明。 |
| C04 · P2 | **CLOSED** | 正文 L77–90 已要求记录部署/负载身份、参照与候选策略、负载终点及单档时长、预热/观察窗、SLO/goodput 分母、错误/排队/质量/副本与资源；成本可按资源占用时长×单价复算，价格未知保留占用记录。L79 的质量/错误停止条件与 L90 的过载、健康、采集失败条件合读，已形成撤压、恢复配置/副本边界并回基线窗口的闭环。沿用指标字典与路由对照即可填写待执行记录，不要求本轮实际压测。 |
| C05 · P2 | **CLOSED** | 正文 L86–88 分开 SLO 违约症状、触顶告警与振荡；触顶不直接归因容量，列出候选原因，资源不可得另记。期望/当前/ready 三线和资源悬置分支见 L69/L83，可记录未触顶短缺。振荡须有固定或已知负载、预登记窗口与变向次数/幅度阈值并排除负载驱动；L81 的收缩曲线须按该条件解释，不能由一次正常撤流判振荡。 |
| C06 · P2 | **OPEN** | L57/L58 已补 token 与设备信号，区分 prefill/decode、静态权重占用及平台指标 unknown，这些修改有效。但 token 行仍把“吞吐/生成速率”概括为真实计算负载，只写依赖窗口/分母，没有区分到达需求与已处理 token/s，也未解释饱和、聚合和窗口对触发滞后/振荡的影响。原要求的实质比较仍不完整，不能仅因增加两行而关闭；不要求补造指标名或阈值。 |
| C07 · P2 | **OPEN** | L68/L70/L73 已落实 Knative/KPA、Standard/Raw、scaling/replicas 互斥、执行器二选一和 PD 同 actuator 约束。仍只笼统写组件“依赖不同”，没有把控制器/CRD、指标链和字段按路径对应；读者无法从本篇判断哪些是普通 HPA、KEDA、WVA 两种执行器各自的前置。L73 的 LLMInferenceService 路径还应明确限定为选择 `spec.scaling` 的情形。见下列最小补齐要求。 |
| C08 · P2 | **CLOSED** | 正文 L68 明确保活触发器只防有流量时缩零，要求另核零副本时仍可观测的触发来源和请求处理链；重新激活链未证，缩零配置不构成完整方案。该限定与[教程 L219–244](https://github.com/vllm-project/production-stack/blob/20a658044af0dea70e9e0136494bb9979cfd9fab/docs/source/use_cases/autoscaling-keda.rst#L219-L244)的证据范围相符。关闭的是缺失前提问题，不是确认样板能够从零唤起，也不据未取证推断其必定不能唤起。 |
| C09 · P2 | **CLOSED** | 正文 L67 已把损失限定为被移除进程本地 KV/prefix cache，外部/offload 及存活副本的缓存复用按实现核对；TTFT 为待验证风险。L81 同窗记录命中率与 TTFT、不预设方向，已取消缩容必然使后续 TTFT 变差的保证。 |
| C10 · P3 | **CLOSED** | 正文 L61 已明确 300s 与 flag 默认 5min 是同一默认机制、不相加；15s 为默认策略周期，容差/同步均可配置，requests 条件限 utilization 计算。与上述历史原始 [v1.32 HPA 页面](https://v1-32.docs.kubernetes.io/docs/tasks/run-application/horizontal-pod-autoscale/#default-behavior)可见段相符。L54 的简写须按 L61 的明确限定阅读；本轮不再把这些默认值或分母条件视为通用固定要求。 |

## OPEN 项的剩余关闭条件

### C01 · 来源主张表仍未同步

固定 [AsyncLLM L801–845](https://github.com/vllm-project/vllm/blob/b17039bccc17b94a2ea107272ad7bc93508708df/vllm/v1/engine/async_llm.py#L801-L845)确实先检查同尺寸返回，再调用排空；排空超时抛异常，在该调用未完成时不会继续执行后面的 core 扩缩容调用。[Middleware L34–49](https://github.com/vllm-project/vllm/blob/b17039bccc17b94a2ea107272ad7bc93508708df/vllm/entrypoints/serve/elastic_ep/middleware.py#L34-L49)只在 HTTP scope 进入时检查标志。正文与 registry 的这些修改可接受，不要求为关闭旧项补查完整控制器恢复链。

**最小修订：** 将来源记录 L25 的主张行同步为有条件的新进入 HTTP 请求分支，补排空超时和同尺寸返回的定位，保留标志调用方及异常恢复 unknown。若要保留首轮原话作为历史，应明确标识已被取代，并提供清楚的现行主张/unknown；仅在末尾声称“已修改”尚不足以使主表保持一致。N01 另按下文修订。

### C02 · 数值及恢复语义的旧断言仍可被当作当前证据

固定 [worker L109–155](https://github.com/vllm-project/vllm/blob/b17039bccc17b94a2ea107272ad7bc93508708df/vllm/v1/worker/gpu_worker.py#L109-L155)显示 level 1/2 的处理不同，wake 调 allocator 并有 buffer 恢复分支；这支持区分 level，不证明任一部署的完整恢复成本。[sleep 教程 L115–120](https://github.com/vllm-project/production-stack/blob/20a658044af0dea70e9e0136494bb9979cfd9fab/docs/source/use_cases/sleep-wakeup-mode.rst#L115-L120)及 [L169–175](https://github.com/vllm-project/production-stack/blob/20a658044af0dea70e9e0136494bb9979cfd9fab/docs/source/use_cases/sleep-wakeup-mode.rst#L169-L175)有示例日志，足以否定“上游无任何数值”，但不能充当本部署性能基线。

**最小修订：** 同步来源记录 L26/L27/L33/L34，明确已经核到的是 worker 分支、未核的是 allocator/完整恢复路径与本部署基线；正文 L95 改成同一范围。无需补测耗时，也无需得出统一重载或不重载结论。历史原话可保留，但须明确失效并给出现行表述。

### C06 · token 处理速率不能直接代替需求及余量

本库[指标字典](../../knowledge/07-inference/latency-metrics.md) L173–175 已区分 arrival、attempted、completed throughput，并要求 token counter 转速率时固定窗口、重启处理和标签聚合。新增行中的“吞吐/生成速率”是处理结果；“真实计算负载”还需具体统计对象及成本模型，单列 prefill/decode 不会自动完成这一转换。

一个用于检验表述的**概念反例（本轮推理，非实测）**是：引擎达到处理上限后，到达需求和积压继续增加，已处理 token/s 可以基本不变。因此处理速率本身不足以确定需求增长或剩余容量。跨副本汇总也可能掩盖局部积压；较长 rate 窗口会平滑突发并延迟触发，较短窗口与阶段/批次波动则需要结合稳定策略判断。这些均不依赖假设某个平台已有统一 exporter。

**最小修订：** token 行明确选用到达 token 需求、在途/排队工作量，还是已处理 prompt/output token 速率；说明所选量的饱和盲区、每副本/集群聚合及窗口引入的滞后或反复触发风险，并与队列和 SLO 同看。设备行保留已有静态内存、采集窗口及平台 unknown 边界即可；不要求补全三平台实现。

### C07 · 路径名称已经补齐，前置和字段对应尚未补齐

固定文档提供了可直接收缩整理的前置条件，无须扩查控制器内部：

- **InferenceService + Knative/KPA：** 以 Knative/KPA 路径为前提；教程的 Prometheus/Grafana 是可选观测组件，不能统写成所有路径的必要指标链。[KPA L8–23](https://github.com/kserve/website/blob/3f4067ea87dd84194bddb1b563051c84306c7997/docs/model-serving/predictive-inference/autoscaling/kpa-autoscaler.md#L8-L23)
- **InferenceService + Standard/HPA：** CPU/内存资源指标样板要求 Metrics Server；文档用 `deploymentMode: Standard`、`autoscalerClass: hpa` 与 predictor 的 `scaleMetric/scaleTarget`。这不是 WVA 的 Prometheus Adapter 前置。[HPA L17–43](https://github.com/kserve/website/blob/3f4067ea87dd84194bddb1b563051c84306c7997/docs/model-serving/predictive-inference/autoscaling/hpa-autoscaler.md#L17-L43)
- **InferenceService + Standard/Raw KEDA：** 要求 KEDA 及 ScaledObject 路径，样板字段为 `autoscalerClass: keda` 和 `spec.predictor.autoScaling.metrics`；外部指标后端按所选类型配置，不能一概推成必须 Prometheus。[KEDA L18–54](https://github.com/kserve/website/blob/3f4067ea87dd84194bddb1b563051c84306c7997/docs/model-serving/predictive-inference/autoscaling/keda-autoscaler.md#L18-L54)、[指标类型 L70–89](https://github.com/kserve/website/blob/3f4067ea87dd84194bddb1b563051c84306c7997/docs/model-serving/predictive-inference/autoscaling/keda-autoscaler.md#L70-L89)
- **LLMInferenceService 选择 `spec.scaling` 的 WVA 集成：** 公共前置为 WVA controller/VariantAutoscaling CRD 和采集推理 Pod、WVA 两类指标的 Prometheus；HPA actuator 另需 Adapter 的 `wva_desired_replicas` external metric 规则；KEDA actuator 另需 KEDA 和集群 ConfigMap 配置。固定 `spec.replicas` 是另一种选择，不能把资源类型本身当作已启用 WVA。[WVA L13–25](https://github.com/kserve/website/blob/3f4067ea87dd84194bddb1b563051c84306c7997/docs/model-serving/generative-inference/llmisvc/autoscaling/llmisvc-autoscaling.md#L13-L25)、[前置 L65–80](https://github.com/kserve/website/blob/3f4067ea87dd84194bddb1b563051c84306c7997/docs/model-serving/generative-inference/llmisvc/autoscaling/llmisvc-autoscaling.md#L65-L80)、[CRD 缺失 L361](https://github.com/kserve/website/blob/3f4067ea87dd84194bddb1b563051c84306c7997/docs/model-serving/generative-inference/llmisvc/autoscaling/llmisvc-autoscaling.md#L361)

**最小修订：** 用一份简表或等价文字把上述资源/模式、字段与必需组件逐路径对应，并补固定来源锚点；保留 L70 已正确写明的同 actuator 约束。不要求部署这些组件、补完整 YAML，或把未核版本组合宣称为兼容。

## 新发现

### N01 · P2 · OPEN · 将逻辑引擎拓扑重配置限定为既有进程内部

**位置：正文 L66 末句“② 是既有引擎进程内的拓扑变更”。** 这是本次为区分两类扩容而新增的错误限定，与 C01 来源摘要未同步分别记录。

同一固定快照的 [AsyncLLM L131–139](https://github.com/vllm-project/vllm/blob/b17039bccc17b94a2ea107272ad7bc93508708df/vllm/v1/engine/async_llm.py#L131-L139)通过多进程 client 连接后台 EngineCore；[core_client.py L1278–1334](https://github.com/vllm-project/vllm/blob/b17039bccc17b94a2ea107272ad7bc93508708df/vllm/v1/engine/core_client.py#L1278-L1334)的弹性 EP 实现要求 Ray DP 后端，向现有 cores 发送分布式重配置请求，并调用 `CoreEngineActorManager` 创建新 cores；[L1343–1358](https://github.com/vllm-project/vllm/blob/b17039bccc17b94a2ea107272ad7bc93508708df/vllm/v1/engine/core_client.py#L1343-L1358)还等待新 cores 的 ready 消息和既有 cores 完成重配置。因此可以区分“同一逻辑服务的 DP engine core 拓扑”和“Kubernetes 服务副本的就绪/路由传播”，不能据此称前者局限在一个既有进程内部。

这一区别影响读者对执行主体、资源新增和 ready 责任的理解：源码中的新 core ready 等待，也不等于 Kubernetes 副本 readiness 已成立。此处补读只证明局部实现及后端约束，不代表已经核清全部 Ray 资源生命周期、异常恢复或控制器集成。

**关闭条件：** 删除“进程内”限定，改为逻辑服务内部 DP engine cores 的分布式拓扑重配置；如描述本快照实现，注明所核路径要求 Ray DP 后端，并保留其不替代副本 readiness/路由传播的边界。可以继续将未核的完整异常恢复链列为 unknown，不必为关闭本项运行伸缩。

除 N01 外，本轮修订范围内没有另立编号的新发现。C02 的 unknown 冲突、C06 的 token 信号比较不足及 C07 的分支前置缺口均归入原项，未重复计数。

## 校验、写入范围与完成边界

报告落盘后执行 `PYTHONDONTWRITEBYTECODE=1 make check`，结果为 **PASS: 117 content entries; 553 sources**。未修改 `src/kb/`，未运行 `make test`。

为遵守“只新增这一个文件”，没有改写工作区 `build/`。另将仓库复制到临时目录，在副本中执行 `make build`，最终 **PASS: 117 content entries; 553 sources**，成功重建 `build/catalog.json` 与 `build/catalog.md`，并读取生成清单确认计数。临时副本首轮未带入既有 `build/`，导致 `docs/first-fill-status.md` 的两个生成文件链接无法通过前置校验；复制既有生成文件后重跑通过，该失败来自副本准备，不是本次内容的新缺陷。

上述检查只验证结构、本地链接与生成过程，不验证技术语义、远端内容或硬件兼容性。交付前再次核对正文哈希，仍与提交值一致。本会话写入工具仅操作本报告；工作区有既有修改，取样期间还观察到 T00-02 初审报告新增、T07-08 第三轮复核报告变化，这些不属于本会话写入，未回退或覆盖。

本轮没有部署 HPA/KPA/KEDA/WVA、启动推理服务、调用排空/睡眠/唤醒接口或执行负载对照；没有生成容量、冷启动、成本、扩缩容响应或三平台兼容性的实测结论。正文 `draft / source_checked` 和环境档案缺失的状态不因本报告改变。

后续定向复核只需覆盖 C01/C02/C06/C07 的剩余条件与 N01，以及相关修订引入的问题；C11 及本轮关闭项不因仍有其他开放项而自动重开。开放项关闭前，不声明 T07-09 或 Batch 28 审阅通过。
