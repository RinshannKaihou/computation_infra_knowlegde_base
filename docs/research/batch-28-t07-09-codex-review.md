# Batch 28 · T07-09 初审报告

## 会话元数据与结论

| 项目 | 记录 |
|---|---|
| 审阅角色 | 独立批次审阅者；本会话未编写或修订被审正文 |
| 实际执行模型 / 档位 | `gpt-6.1-sol / xhigh` |
| 模型核验 | 读取当前本地会话 JSONL 的最新 `turn_context`，确认 `model=gpt-6.1-sol`、`effort=xhigh`，与 `collaboration_mode.settings` 一致；本轮未另启模型、CLI 审阅进程或子代理，无 fallback 轮次 |
| 会话 ID | `01a15d4c-78f0-7053-956e-7f69e52e2c75` |
| 执行方式 | 本地 Codex CLI 会话直接读取仓库与缓存，网络只读抽查，随后新增本报告 |
| 工作目录 | `/Users/ywang2397/work/AI_reliability_knowledge_base` |
| 日期 / 时区 | 2026-10-21 / Asia/Shanghai |
| 审阅正文 | `knowledge/07-inference/capacity-and-autoscaling.md`，97 行 |
| 正文 SHA-256 | `6161a0f0c78507f5b282f4d6419c940cd65ec4206c65f129473d7a223a5f37bb` |
| 写入范围 | 仅新增 `docs/research/batch-28-t07-09-codex-review.md`；不修改正文、取证记录、registry、导航、计划或其他文件 |

**初审结论：需修订并定向复核，暂不通过。** 共记录 11 项发现：P1 为 0 项，P2 为 9 项（C01–C09），P3 为 2 项（C10–C11）。报告收尾时，C11 的共享 registry 路径已由其他工作修正，经本会话定向核对关闭；**仍开放 10 项：9 P2、1 P3（C01–C10）**。容量框架与教程值的归属基本清楚，但 ready、sleep、冗余、缩零及缓存效果存在边界缺失，对照方案和判据尚未满足完整验收要求。

优先级：P1 为严重误导处置的关键错误；P2 为影响技术准确性、适用边界或验收完整性的必修项；P3 为措辞、定位与追溯问题。下文正文行号以本表 SHA-256 为准；GitHub 锚点使用缓存原文件坐标，不使用网页转换行号。

## 范围与方法

先读取 `README.md`、`docs/authoring-guide.md`、`AGENTS.md`、`schemas/content.schema.json`，并按 `content-outline.md` 确认 05/07 域分工。逐项对照 [T07-09 任务定义](../../plans/full-coverage-backlog.yaml) L6590–6611，重点核查五条 acceptance（L6607–6611）。

完整重读[正文](../../knowledge/07-inference/capacity-and-autoscaling.md)、[作者取证记录](batch-28-t07-09-sources.md)和 [registry](../../sources/registry.yaml) 中指定三项新增来源及 `src.vllm.inference-v0-14` 的 Batch 28 notes；核查 [07 域导航](../../knowledge/07-inference/index.md) L35/L56/L82–83。沿正文链接读取路由、延迟字典、模型加载/ready、PD 分离、分布式布局、05 域节点回收/争用验证与同批发布恢复页的相关边界；这些关联页没有在本轮接受完整重审。

逐行读取本地缓存，不导入、不执行其中服务代码。独立计算以下 SHA-256 前 16 位，均与作者取证记录或 registry 登记一致：

| 缓存根目录 / 文件 | 独立计算的 SHA-256 前 16 位 |
|---|---|
| `/tmp/b28/vllm/vllm_v1_engine_async_llm.py` | `818af4561b7ae54a` |
| `/tmp/b28/vllm/elastic_ep_middleware.py` | `46da705bc65f83c8` |
| KServe `kpa-autoscaler.md` | `b8f04c9dad91aa14` |
| KServe `hpa-autoscaler.md` | `a554223d86ac0880` |
| KServe `keda-autoscaler.md` | `e71de56eb95d6af8` |
| KServe `llmisvc-autoscaling.md` | `880fb8a6c1e57c91` |
| production-stack `docs/source/use_cases/autoscaling-keda.rst` | `391c98658ab19d2c` |
| production-stack `docs/source/use_cases/sleep-wakeup-mode.rst` | `d62f16d2ac62184d` |
| production-stack `helm/values.yaml` | `d879b85b83e9d1b0` |
| production-stack `helm/templates/hpa-router.yaml` | `d29be85957dfb192` |

KServe 缓存根目录为 `/tmp/b28/kserve-web/docs/model-serving/`，production-stack 为 `/tmp/b28/production-stack-vllm-stack-0.1.9/`。另读 vLLM `conserving_memory.md`（本轮哈希前缀 `895bc42beb0ff505`）、`troubleshooting.md`（`dc679401e1078852`）、`api_server.py` 的中间件挂载点及 `gpu_worker.py` L109–155；后者前缀 `eb33b5f2bd389ac3` 与同批 T07-11 来源记录相符。补读 chart 的 `scaledobject-vllm.yaml`，只核对模板结构，不声称渲染、安装或运行成功。

哈希匹配证明所读缓存与作者记录的字节一致，不单独证明 tag 的远端解析或完整软件配套。KServe/WVA 本轮限于固定网站仓文档口径，没有取回 WVA 控制器实现或 KEDA 完整版本契约。

网络抽查成功打开 [Kubernetes v1.32 HPA 静态页](https://v1-32.docs.kubernetes.io/docs/tasks/run-application/horizontal-pod-autoscale/)的算法、稳定窗与默认 behavior 段，及 [SRE Workbook Implementing SLOs](https://sre.google/workbook/implementing-slos/)。前者可独立复核 registry 的网页观察记录，本轮不记为“未复核”。网页工具标题/正文确认是 v1.32 静态文档；没有将当前网络可达性当作历史原始响应的哈希证明。

工作区另有 T07-08 正文/取证及共享 registry 的并行修订，均非本会话写入。本轮末尾重读 registry 的 Batch 28 相关片段以核对 C11；该次 registry SHA-256 为 `816e40f516b7f3c16f32ed4c070a2716bf20b2c1b789a69f5cc66fc5847b2a0e`。被审 T07-09 正文哈希保持不变；本报告不承接 T07-08 其余发现的关闭工作。

## 关键主张核对结果

| 对象 | 核对结论 |
|---|---|
| HPA 公式与默认 | registry 的 `ceil(currentReplicas × currentMetricValue / desiredMetricValue)`、默认容差 0.1、同步 15s，以及缺指标/多指标保守处理，与网页相符。默认 behavior 为缩容稳定窗 300s、Percent 100/15s；扩容稳定窗 0、Percent 100 与 Pods 4/15s、Max。300s 与控制器默认 5min 的关系见 C10。[算法与默认 behavior](https://v1-32.docs.kubernetes.io/docs/tasks/run-application/horizontal-pod-autoscale/#default-behavior) |
| KPA | 缓存 L29 支持 target 软限，L356–358 支持 containerConcurrency 硬限及超限缓冲；L374–385 支持默认 minReplicas=1、置 0 缩零；L424 支持 scaleMetric 默认 concurrency。L262 是“6s 窗平均达到 2×目标则进 panic，退出条件连续 60s 不再满足”，正文数字没有杜撰；部署模式遗漏见 C07。[固定 KPA 文档](https://github.com/kserve/website/blob/3f4067ea87dd84194bddb1b563051c84306c7997/docs/model-serving/predictive-inference/autoscaling/kpa-autoscaler.md#L262) |
| WVA | 文档 L11–25、L35–61 支持指标→WVA 决策→`wva_desired_replicas`→HPA/Adapter 或 KEDA 执行，target=1、scaling/replicas 互斥；L224 明示无活动触发器时 idleReplicaCount 可低于 minReplicas 且须更小。这是集成文档结论，不能扩成已核 WVA/KEDA 内部算法或任意组合兼容。[固定 WVA 文档](https://github.com/kserve/website/blob/3f4067ea87dd84194bddb1b563051c84306c7997/docs/model-serving/generative-inference/llmisvc/autoscaling/llmisvc-autoscaling.md#L35-L61) |
| KEDA 教程与 chart | 教程 L135–148 确有 waiting 阈值 5、pollingInterval 15、cooldownPeriod 360、min/max 1–3；正文 L56 明确为教程示例，未写成通用推荐。router HPA 模板 L16–22 是 CPU Utilization，且 L1 有启用门控，不能当成默认已运行。`scaledobject-vllm.yaml` L3–4 还要求启用 keda 且没有 raySpec；不外推 Ray 部署。[教程配置](https://github.com/vllm-project/production-stack/blob/20a658044af0dea70e9e0136494bb9979cfd9fab/docs/source/use_cases/autoscaling-keda.rst#L135-L162) |
| vLLM elastic EP | `async_llm.py` L801–815 轮询 `dp_engines_running()`，超时抛 TimeoutError；L828–834 同尺寸直接返回，否则 L839 先排空、L844 才改变 DP core 数。Middleware L34–49 仅在 HTTP scope 且 scaling 标志为真时回 503，挂载在 `api_server.py` L944。主链存在，不等于通用副本 ready gate，也不把已经开始的流改回 503，见 C01。[排空与扩缩容实现](https://github.com/vllm-project/vllm/blob/b17039bccc17b94a2ea107272ad7bc93508708df/vllm/v1/engine/async_llm.py#L801-L845) |
| 加载与睡眠 | `conserving_memory.md` L23–26 支持该文档所述 TP 读取及分片 checkpoint 建议；不能据此给所有 loader/平台统一加载时长。sleep 教程支持不接请求、释放资源、显式 sleep/wake 操作，不能单凭教程证明统一的权重重载成本，见 C02。[TP 加载说明](https://github.com/vllm-project/vllm/blob/b17039bccc17b94a2ea107272ad7bc93508708df/docs/configuration/conserving_memory.md#L23-L26) |

## 发现清单

### C01 · P2 · 将弹性 EP 拓扑变更排空混作扩容 ready gate

- **位置**：正文 L63–64；取证记录 L25；registry L536 的对应扩缩容摘要。
- **证据**：L64 用“对应机制”把新副本就绪与 `scale_elastic_ep` 接在一起。固定源码实际更改现有引擎的 data-parallel core 数，并先等待现有 DP 引擎 idle；它不检查 Kubernetes 新副本 readiness、路由发现或质量 gate。HTTP 503 是已挂载 Middleware 在 scaling 标志为真时对新进入 HTTP 请求的分支，`scale_elastic_ep` 本身没有设置该标志；在途流继续排空，不能概括为全部在途请求收到 503。排空还有 300s 超时异常分支。[AsyncLLM](https://github.com/vllm-project/vllm/blob/b17039bccc17b94a2ea107272ad7bc93508708df/vllm/v1/engine/async_llm.py#L801-L845)、[Middleware](https://github.com/vllm-project/vllm/blob/b17039bccc17b94a2ea107272ad7bc93508708df/vllm/entrypoints/serve/elastic_ep/middleware.py#L34-L49)。
- **建议修订**：分别描述副本扩容的 ready/预热/路由传播与弹性 EP 的拓扑重配置；503 写明中间件、状态条件及新请求边界。排空超时应停止该次变更并保留证据；尚未核查的标志设置/清除和异常恢复链继续 unknown，不能补写自动恢复保证。
- **关闭条件**：正文、取证及 registry 的摘要条件一致；ready gate 不再以 EP 排空作为实现证明，且超时/新请求/在途流三个分支清楚。

### C02 · P2 · sleep 唤醒成本超出已取证范围，且与 unknown 冲突

- **位置**：正文 L66、L84–85；取证记录 L26–27、L33–34。
- **证据**：正文称“唤醒仍需重载”“省的……不是权重加载”，而 L84 承认 sleep level/唤醒语义未核。教程 L4 只概述释放资源，L143–175 展示 wake 操作及样例日志，没有证明每种 sleep 都重新从 checkpoint 加载权重。补读同 commit 的 `gpu_worker.py` L109–145，可见 level 1 使用 weights offload tag，level 2 有不同处理，wake 调 allocator；本轮未继续核 allocator 和完整 reload 链，不能给统一成本结论。此外，教程 L119–120、L173–175 存在示例耗时，KPA 文档 L123 也有示例冷启动解释，“无任何官方耗时数值”这个绝对否定不成立；这些样例仍不能当作本文三平台部署基线。[sleep 教程](https://github.com/vllm-project/production-stack/blob/20a658044af0dea70e9e0136494bb9979cfd9fab/docs/source/use_cases/sleep-wakeup-mode.rst#L143-L175)、[worker 分支](https://github.com/vllm-project/vllm/blob/b17039bccc17b94a2ea107272ad7bc93508708df/vllm/v1/worker/gpu_worker.py#L109-L155)。
- **建议修订**：收缩为“唤醒成本依 sleep level、状态保留与后端实现，本文未核完整恢复路径，须测”；若保留加载成本结论，补取固定实现并区分 CPU offload 恢复、丢弃后权重重载和进程冷启动。将数值 unknown 改为“未取得可用于本部署的三平台容量/阶段耗时基线”，不引用示例日志作性能推荐。
- **关闭条件**：无无条件重载或节省项目断言；正文与取证 unknown 一致，且不再声称上游完全没有数值。

### C03 · P2 · 无来源的 minReplicas≥2 被写成严格 SLO 服务的通用规则

- **位置**：正文 L69，与 L27“本文不给通用参数”相冲突。
- **证据**：指定来源没有建立“严格 SLO→最小副本 2”的通用结论。两个副本若共享故障域，或剩余副本无足够 SLO 容量，都不能据数量保证故障期间仍可服务；实际冗余下限还受负载、故障预算、放置和可用资源约束。05 域争用验证明确区分容量、形状与故障预算，本条不能用 minReplicas 配置替代这些证据。
- **建议修订**：标为本库规划建议，按故障模型、剩余 ready 容量、故障域与恢复窗口确定下限。若举两个副本的例子，明确其假设与非充分性，并说明空闲策略、故障和控制器行为可能使实际 ready 数低于配置下限。
- **关闭条件**：删除通用数字处方及数量即保障的暗示；冗余下限有可检查的输入和约束，未实测条件保留 unknown。

### C04 · P2 · 有限对照缺成本记录、明确停止与恢复闭环

- **位置**：正文 L71–79；acceptance 4（任务 L6610）。
- **证据**：三类负载、错误/排队/质量观察已列，但没有成本记录、每档负载上限/持续窗口、失效预算、停止动作、回退/恢复基线与恢复完成条件。L73 的路由对照链接不能补齐这些：关联页的停止原则不等于本篇扩缩容配置与副本/cache 状态的恢复方案。L75“从低到低调步进”也未说明有限增压的终点。资源水位或副本数曲线本身不能代替有单位的成本记录。
- **建议修订**：补一份待执行记录表：固定部署/负载身份、固定副本参照与候选策略、预热/观察时长和最大负载、尾延迟与请求达标率/goodput 各自分母、错误/质量、资源占用时长或每单位 goodput 成本（实际价格未知可留空）。预登记过载/健康/质量/采集失败的停止条件；停止后撤压、恢复配置/副本边界，核对流量、资源、错误和 SLO 回到基线。明确这是本库方法设计，实际执行依既有授权及现场条件。
- **关闭条件**：仅凭正文与所链接记录模板即可执行一次有界对照并审查停止/恢复；成本有可复算口径，无需为关闭本项实际压测。

### C05 · P2 · 容量不足与振荡判据混淆症状、控制边界和归因

- **位置**：正文 L77、L79。
- **证据**：“SLO 达标率跌破目标且已处 maxReplicas”只能说明目标未达且触及配置上限，不能排除路由不均、故障副本、指标失真或其他共享瓶颈；扩容滞后/资源不可得时尚未达到 maxReplicas，也可能已出现服务容量缺口。L77 将副本上下翻动直接当振荡证据，L79 又称变向次数超阈值；正常高→低撤流或周期负载也会变向，两条口径没有排除负载驱动变化。以上是作者诊断设计，不是上游已给的充分判据。
- **建议修订**：分开记录 SLO 违约、期望/当前/ready 副本、扩容受限原因与瓶颈证据；将触顶状态命名为触顶告警，不直接判定容量根因。振荡在固定或已知负载下，预登记观察窗、变化幅度/次数及 SLO/成本影响，区分正常跟随负载和控制环反复变向。
- **关闭条件**：判据不再由单个症状直接推出容量归因；可区分未触顶短缺、触顶但非容量根因、正常撤流缩容与异常反复伸缩。

### C06 · P2 · 触发器比较未覆盖 token 与加速器设备指标

- **位置**：正文 L50–59；acceptance 2（任务 L6608）。
- **证据**：表中有 QPS/concurrency、waiting、KV/请求饱和度和主机 CPU/内存，但没有解释输入/输出 token 工作量信号，也没有 GPU/NPU 利用率、设备内存等设备信号的适用与误判边界。CPU/内存 Resource metrics 不能替代推理加速器指标比较；KPA 来源本身 L264–266 还提示 GPU 利用率随任务波动。现有四行不足以覆盖任务指定的完整比较范围。
- **建议修订**：补 token 与设备指标的概念级比较，明确统计对象、采集/聚合窗口、prefill/decode 成本差异、静态权重占用与可服务容量的区别，以及触发滞后和振荡风险。比较解释标为作者机制归纳；尚无版本化 exporter/指标/控制器证据时保留 unknown，不发明三平台统一指标名或阈值。
- **关闭条件**：请求率、队列、并发/token/KV、设备指标均有实质比较，实际实现证据与本库建议分开标注。

### C07 · P2 · KServe 部署模式与 PD 执行器约束未带入 procedure

- **位置**：正文 L27、L55、L57、L66、L68。
- **证据**：KPA 文档 L12 明示仅 Knative；HPA 文档 L8–15/L28 区分 Standard/Raw，不能套 KPA 缩零配置；WVA 文档 L20–25 限 LLMInferenceService，且 scaling/replicas 互斥，L88 要求两种执行器二选一。更直接的是 L280 明示 PD 的 decode/prefill 必须用同一种 actuator，L365 列相应验证错误。正文仅写“两池分别触发、分别扩缩”，没有保留该样板的约束，前置也未帮助读者选择正确资源与模式。[KPA 模式](https://github.com/kserve/website/blob/3f4067ea87dd84194bddb1b563051c84306c7997/docs/model-serving/predictive-inference/autoscaling/kpa-autoscaler.md#L8-L14)、[WVA Prefill Scaling](https://github.com/kserve/website/blob/3f4067ea87dd84194bddb1b563051c84306c7997/docs/model-serving/generative-inference/llmisvc/autoscaling/llmisvc-autoscaling.md#L278-L280)。
- **建议修订**：加一段前置分支，区分 InferenceService+Knative/KPA、Standard 的 HPA/KEDA 与 LLMInferenceService+WVA；将控制器/CRD、Prometheus/Adapter 等必需组件按路径列明。PD 段写明固定 KServe 样板的同 actuator 约束，同时说明通用双池规划是本库归纳。
- **关闭条件**：字段与模式可唯一对应，不能把 KPA 参数套到 Standard/WVA；PD 独立边界不再暗示执行器可随意混搭。

### C08 · P2 · scale-to-zero 条件没有覆盖从零重新激活

- **位置**：正文 L66；取证记录 L24、L32。
- **证据**：production-stack 教程 L222–244 确有 minReplicaCount=0 加 keepalive，注释明确该触发器用于“有流量时防止缩零”。该片段没有证明引擎全停后谁继续观测新流量、产生可用指标并触发从零扩容；引擎自身 waiting 指标不能在零个引擎时被无条件假定为可观测。入口能排队/返回状态及能接受冷启动，仍不足以证明重新激活链存在。本轮也没有核 KEDA 完整字段/激活语义，不能用 unknown 旁注替代这一关键适用条件。
- **建议修订**：把教程保活示例与 scale-from-zero 分开，增加“零副本时仍存活、可观测的触发来源及请求处理链”前置核查。没有已核实现时明确此样板的重新激活链未证，不将缩零配置当完整可用方案；无需为了补齐而假设某种 HTTP add-on 已存在。
- **关闭条件**：缩零、保活与重新激活的责任各自清楚；能定位已核唤起来源，或明确列为缺失前提并限制方案适用性。[教程原片段](https://github.com/vllm-project/production-stack/blob/20a658044af0dea70e9e0136494bb9979cfd9fab/docs/source/use_cases/autoscaling-keda.rst#L219-L244)。

### C09 · P2 · 本地缓存损失被扩大为缩容后的必然 TTFT 退化

- **位置**：正文 L65、L77。
- **证据**：被删除进程的本地 KV 消失，不等于所有仍服务副本或外部缓存都消失。缩容后路由变化、前缀命中、缓存是否启用及负载变化，才共同决定后续 TTFT；现有来源未给“回升后 TTFT 会短暂变差”的无条件结果。正文还覆盖 PD/production-stack，不能省去缓存所在层和复用路径。既有 `execution-and-kv-cache.md` L99–108 已明确身份、完整 block 和命中条件。
- **建议修订**：限定为被移除进程的本地缓存不保留；外部缓存、存活副本及恢复可用性按所选实现核对。TTFT 退化写成待验证风险/作者假设，收缩对照分别记录命中率、路由、负载、TTFT，不预设一定恶化或一定可在某时间恢复。
- **关闭条件**：缓存所有权与作用范围明确，观测设计不把未测性能方向写成结果保证。

### C10 · P3 · HPA 默认控制参数被压缩成可能叠加的固定时间

- **位置**：正文 L54、L59。
- **证据**：L59 写缩容默认 300s 后又称控制器“还有”5min，容易被读成两道串联等待；来源默认 behavior 段明确 300s 与控制器 flag 的默认/配置关系。L59 的“每 15s”也应是默认策略示例，不是所有 behavior 策略固定周期。L54 的容差/同步应标“默认”；requests 要求宜限定到 Utilization 计算，避免从这一行推成所有 raw Resource metric 的前提。[HPA 默认 behavior](https://v1-32.docs.kubernetes.io/docs/tasks/run-application/horizontal-pod-autoscale/#default-behavior)。
- **建议修订**：明确默认值与可配置项，不把 300s 与 5min 累加；保留已有准确的 registry notes，不必重写成新的控制机制。
- **关闭条件**：读者不会据此计算双重稳定等待，也不会把默认周期/利用率分母条件当作通用固定要求。

### C11 · P3 · Batch 28 registry 的哈希取证路径不存在（收尾定向核对已关闭）

- **位置**：`sources/registry.yaml` L536，`src.vllm.inference-v0-14` Batch 28 notes；影响本篇 L12/L34/L94 的证据追溯。
- **证据**：notes 将文件 SHA-256 指向 `docs/research/batch-28-tasks-sources.md`，该文件不存在；实际取证分布在各 `batch-28-t07-XX-sources.md`。本篇自己的 T07-09 来源链接有效，不能据此判所有来源失效。此项与 T07-08 初审 C11 的共享 registry 路径问题相同，本轮独立确认，不视为另一处独立上游错误。
- **建议修订**：将聚合路径替换为实际存在、覆盖对应文件的分任务取证记录，并保留已核哈希；正文 EP helper 与 Middleware 如补锚点，应使用实际原文件行号。
- **关闭条件**：registry 的取证指向可解析且能找到对应哈希/范围；不靠未检查普通字符串路径的结构校验结果关闭。
- **本轮收尾状态**：共享 registry 已由其他工作改为 T07-08 至 T07-11 的分任务来源记录。独立重读确认旧路径不再出现，四份目标均存在，T07-09 可定位 `async_llm.py` 哈希 `818af4561b7ae54a`、T07-08 可定位 Middleware 哈希 `46da705bc65f83c8`，本项关闭。仅关闭路径与追溯缺陷，不据此关闭 C01 的技术边界问题，也不代替 T07-08 自身复核。

## 五条 acceptance 逐条判断

| 序号 / 要求 | 覆盖情况与初审判断 |
|---|---|
| 1 · 固定负载/模型平台配置，按瓶颈和 SLO/goodput 定单副本/集群容量 | **主要满足口径框架**。L42、L46–48 固定模型/引擎/后端及负载，并区分 KV 上界与实测 SLO 容量、路由折损。这里的有效容量定义、折损核算属于本库方法，应显式标注；有限对照如何据此形成可靠判断仍依 C04/C05 修订。 |
| 2 · 请求率、队列、并发/token/KV、设备指标，滞后/稳定/冷启动/资源不可得/振荡 | **部分满足**。请求/队列/KV 比较及冷启动、资源悬置分支已有；token/加速器信号缺失，振荡判据及默认控制措辞需修，见 C05/C06/C10。 |
| 3 · 最小冗余、缩零条件、ready、drain/在途/cache、PD 联动 | **部分满足**。各题项有入口，但不能以存在标题代替准确边界；C01/C02/C03/C07/C08/C09 均需关闭。idleReplicaCount 的文档语义已核，完整 KEDA/WVA 实现仍未核。 |
| 4 · 有限增压/阶跃/收缩，错误/排队/尾延迟/质量/成本，停止/恢复与容量不足判据 | **未满足完整验收**。三类对照已列，成本、有限边界与停止/恢复不完整，容量/振荡判据不能直接用于归因，见 C04/C05；不要求本轮执行实验。 |
| 5 · 三平台资源/加载时延只取来源或待测，不杜撰容量性能 | **满足“不杜撰三平台数值”的数值纪律，来源措辞待修**。未编造 NVIDIA/AMD/Ascend 的容量、吞吐或冷启动基准，L79 明确分列不换算。C02 要把“官方完全无数值”收窄为本部署基线未取得；C03 的通用副本处方及 C09 的无条件效果仍应按各项关闭，不能由此条单独判全篇通过。 |

## 元数据、导航与 unknown 核查

- **procedure 字段**：`id/type/domain/status` 正确，标题一致；新正文保持 `draft`。`applicability.environment_refs: []` 与 `verification.status: source_checked`、非空来源证据 ID 符合 schema，没有伪造环境档案或写成 reproduced。L27 已声明机型/模型/版本容量未知，但仍宜补明缺失的驱动、运行库、插件与拓扑，控制面样板不构成三平台已兼容证明。
- **ID 与本地链接**：七个 related ID 均存在，所有正文内联本地链接均能定位文件。05 域两个 ID 分别指向节点回收与争用容量验证，职责没有被复制到本篇。模型加载、延迟、PD、路由与分布式布局引用目标均正确。
- **互链实际状态**：本篇列出的七个 related ID 暂无反向 `related_ids`；PD L127 有正文回链，其余关联页没有容量页回链。schema 只要求引用有效，不要求所有旧页双向关系，因此不把这些缺少反向元数据一概判为结构错误。`release-and-recovery.md` 已存在，L21 有本篇 related ID 且 L63 有正文回链；本篇 L63/L65 的前向链接有效，但自己的 related_ids 未列 release ID，可补齐同批关系。没有把该同批文件误判为断链或未来占位。
- **导航**：07 域 index 的相关 ID、已有正文入口及 07.6/07.7 两行均已整合容量页，没有据此声称有真实容量基线或网站实现。index 日期较正文旧不影响链接有效性。
- **unknown 一致性**：WVA 控制器内部、KEDA 完整字段、跨层 Pod 删除→引擎排空、未部署/未压测均合理保持未知；不能因此抹去已核的 WVA 集成或 idleReplicaCount 文档语义。sleep 的未知与重载保证冲突见 C02；缩零唤起链缺口见 C08；缓存效果应保留为假设见 C09。容量定义、折损、对照设计和诊断判据是本库归纳，不能把邻近 SRE/控制器引文作为这些具体设计的上游背书。
- **版本与许可**：各样板未声称 production-stack v0.1.9 与 vLLM v0.14.0 已配套运行；KServe 0.20 线仅代表已钉网站仓口径。正文以链接与原创归纳为主，未统一改写第三方许可；本轮未重做完整许可审查。
- **计划状态**：T07-09 当前仍为 `planned / needs_source_preparation`。本报告不把正文存在、取证完成或初审交付当作 done/审阅通过，也不更改账本。

## 校验与真实环境验证边界

报告落盘后执行 `PYTHONDONTWRITEBYTECODE=1 make check`，结果为 **PASS: 117 content entries; 553 sources**。检查覆盖元数据、引用与本地文件链接，不验证技术语义、远程内容或硬件兼容性。本会话仅新增审阅报告，没有修改知识正文、来源、导航或 `src/kb/`；未运行 `make test`。为遵守“只新增这一个文件”的明确写入范围，未运行会写入 `build/` 的 `make build`。

**模型审阅不替代真实环境验证。** 本轮没有部署 HPA/KPA/KEDA/WVA、启动 vLLM/production-stack、运行负载或调用排空/睡眠/唤醒接口，没有测量容量、冷启动、伸缩响应、成本、资源回收或三平台兼容性。静态源码可见的分支、网页主张、结构检查与待执行方法，均不能登记为本地实验成功。

后续由编写者按仍开放的 C01–C10 修订并提交新的正文 SHA-256 与证据位置，再由同一审阅者定向复核。关闭条件满足前，不声明 T07-09 或 Batch 28 审阅通过；本报告也不代替 T07-08/10/11 的独立审阅。
