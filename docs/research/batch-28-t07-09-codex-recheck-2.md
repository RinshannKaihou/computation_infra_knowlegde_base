# Batch 28 · T07-09 第二轮定向复核报告

## 会话元数据与结论

| 项目 | 记录 |
|---|---|
| 角色与范围 | 独立审阅者，仅承接[第一轮定向复核](batch-28-t07-09-codex-recheck.md)的 OPEN 项 C01/C02/C06/C07 剩余条件与 N01，并检查相关修订引入的问题；未编写或修改被审正文 |
| 实际执行模型 / 档位 | `gpt-6.1-sol / xhigh` |
| 模型核验 | 读取 `CODEX_THREAD_ID` 对应本地会话 JSONL，第 8 行 `turn_context`（`2026-10-21T07:55:21.781Z`）实见 `model=gpt-6.1-sol`、`effort=xhigh`，与 `collaboration_mode.settings` 一致；本轮未另启模型、审阅 CLI 子进程或子代理，无模型 fallback 轮次 |
| 会话 ID | `01a15d74-ceef-7873-b833-f101dea79b4c` |
| 执行方式 | 本地 Codex CLI，`originator=codex_exec`、`cli_version=0.163.0`；直接读取工作区文件及固定快照缓存 |
| 日期 / 时区 | 2026-10-21 / Asia/Shanghai |
| 工作目录 | `/Users/ywang2397/work/AI_reliability_knowledge_base` |
| 修订正文 | [capacity-and-autoscaling.md](../../knowledge/07-inference/capacity-and-autoscaling.md)，115 行；下文正文行号均对应此版 |
| 作者提交的正文 SHA-256 | `2e2bff94edb430df2fb1183ea3f5c7086a8b7ca4d5dd23b7641561c52bdb217c` |
| 独立计算的正文 SHA-256 | `2e2bff94edb430df2fb1183ea3f5c7086a8b7ca4d5dd23b7641561c52bdb217c`，**匹配** |
| 写入范围 | 仅新增本报告；不修改正文、来源记录、registry、导航、任务账本或审核状态 |

**结论：暂不通过。本轮五项中 CLOSED=4（C01/C06/C07/N01），OPEN=1（C02，沿用 P2）。无新增 N02 及后续编号；开放 P1=0、P2=1、P3=0。**

C02 的来源记录、数值边界与正文来源节已完成修订，但正文 L102 仍保留第一轮明确要求消除的“实现细节未核，仅引用教程”断言。已关闭项 C03/C04/C05/C08/C09/C10 及 C11 沿用前轮状态，不在本轮重审，也不因 C02 尚开放而重开。本结论不构成 Batch 28 整批验收或硬件验证。

## 方法与证据边界

已读取仓库 `AGENTS.md`、[README](../../README.md)、[写作指南](../authoring-guide.md)、[内容总目录](../../content-outline.md)、元数据 schema、[T07-09 任务验收](../../plans/full-coverage-backlog.yaml)和第一轮剩余关闭条件；重读修订正文、[来源记录](batch-28-t07-09-sources.md)与相关 registry 摘要，并核对[指标字典](../../knowledge/07-inference/latency-metrics.md) L159–175。修订摘要仅用于定位，以文件实际内容为判定依据。

本轮取样的来源记录 SHA-256 为 `45a576659c61191ef18bfc6bb6ef6b7a82f7f79db964ef7373c0f9398efff175`，registry 为 `abecd29b5c7f9527919f8bde9fc900aa9a37d73048aa558d3e272b6c99d7bd18`；两者均只读。

远端复取未成功：GitHub 文件工具返回不可用，网页工具返回 HTTP 429，终端读取固定 raw URL 时 DNS 解析失败。本轮实际证据为以下**既有固定快照缓存的重新读取与哈希核对**，不是本轮新取得的远端响应，也未以第一轮结论代替源码核对。哈希前缀均与前轮记录相符。

| 缓存文件 | SHA-256 前 16 位 | 本轮读取范围 |
|---|---|---|
| vLLM `vllm_v1_engine_async_llm.py` | `818af4561b7ae54a` | L801–855，同尺寸返回、轮询排空、超时与调用顺序 |
| vLLM `elastic_ep_middleware.py` | `46da705bc65f83c8` | 全 49 行，HTTP scope 与状态标志分支 |
| vLLM `gpu_worker.py` | `eb33b5f2bd389ac3` | L109–155，sleep level 分支与 wake 调用边界 |
| vLLM `core_client.py` | `601d375067fa724e` | L1278–1367，Ray 后端约束、扩容分支与 ready/重配置等待 |
| KServe `kpa-autoscaler.md` | `b8f04c9dad91aa14` | L8–23，Knative 范围与可选观测组件 |
| KServe `hpa-autoscaler.md` | `a554223d86ac0880` | L8–65，Standard 路径、Metrics Server 与字段 |
| KServe `keda-autoscaler.md` | `e71de56eb95d6af8` | L8–97，Raw/Standard 样板、ScaledObject 与指标类型 |
| KServe `llmisvc-autoscaling.md` | `880fb8a6c1e57c91` | L13–97、L228–262、L278–280、L357–366，WVA 前置、执行器与互斥条件 |
| production-stack `sleep-wakeup-mode.rst` | `d62f16d2ac62184d` | L1–4、L115–120、L169–175，教程范围与示例日志 |

vLLM 缓存位于 `/tmp/b28/vllm/`，对应 `b17039bccc17b94a2ea107272ad7bc93508708df`；KServe 缓存位于 `/tmp/b28/kserve-web/docs/model-serving/`，对应 `3f4067ea87dd84194bddb1b563051c84306c7997`；production-stack 教程位于 `/tmp/b28/production-stack-vllm-stack-0.1.9/docs/source/use_cases/`，对应 `20a658044af0dea70e9e0136494bb9979cfd9fab`。这些缓存字节身份不证明远端 tag 当前解析、完整版本兼容或运行成功；本轮未补核 WVA 内部实现、KEDA 完整激活语义或 allocator 完整恢复链。

## OPEN 项逐项判定

| 编号 / 原优先级 | 判定 | 理由与证据 |
|---|---|---|
| C01 · P2 | **CLOSED** | 来源记录 L25 已同步为现行主张：同尺寸直接返回，否则轮询排空、默认 300s 超时抛 `TimeoutError` 后不继续该次变更；503 限于标志为真时新进入的 HTTP 请求，在途流不受该中间件分支影响，标志设置/清除及异常恢复仍为 unknown。与正文 L66、registry 相关摘要一致，另补 core client 锚点。固定 [AsyncLLM L801–845](https://github.com/vllm-project/vllm/blob/b17039bccc17b94a2ea107272ad7bc93508708df/vllm/v1/engine/async_llm.py#L801-L845)及 [Middleware L34–49](https://github.com/vllm-project/vllm/blob/b17039bccc17b94a2ea107272ad7bc93508708df/vllm/entrypoints/serve/elastic_ep/middleware.py#L34-L49)支持此范围。旧的无条件 503 主张已不再作为主表内容；无需为关闭本项补证完整控制器恢复链。 |
| C02 · P2 | **OPEN** | 来源记录 L26–27/L33–34 已明确 worker 层已核、allocator/完整恢复链未核，并承认示例日志而不作为本部署基线；正文 L65/L68/L103/L112 也已相应收窄。但正文 L102 仍称固定 commit 的 sleep level、唤醒实现“未核，仅引用教程”，与 L68/L112 及来源记录直接冲突。第一轮已明确要求同步该处（前轮 L95，本轮 L102），只补来源节未满足全部剩余条件。此为原项残留，不另编号 N02。 |
| C06 · P2 | **CLOSED** | 正文 L57 已区分到达 token 需求、在途/排队工作量、已处理 prompt/output token 速率，明确处理结果不等于需求；以概念推演说明处理饱和后速率可不变而积压增长，没有冒充实测。还覆盖跨副本聚合掩盖局部积压、长窗口滞后、短窗口波动与稳定策略，保留 prefill/decode 成本差异，并要求与队列和 SLO 同看。所链指标字典 L173–175 确有 arrival/attempted/completed 和 counter 转速率的窗口、重启、聚合要求；概念归纳及三平台指标名/阈值 unknown 标识清楚。 |
| C07 · P2 | **CLOSED** | 正文 L73–80 已按四路径对应字段和必需组件：Knative/KPA 的 Prometheus/Grafana 可选；Standard/HPA 的资源指标样板需 Metrics Server；Standard/Raw KEDA 用 ScaledObject，外部指标后端按类型；选择 `spec.scaling` 的 LLMInferenceService/WVA 用 controller/CRD、采集 Pod 与 WVA 两类指标的 Prometheus，并区分 HPA Adapter external metric 与 KEDA/集群 ConfigMap 前置。固定 `spec.replicas` 作为另一选择已明确，不因资源类型自动启用 WVA。表中锚点与固定文档相符，正文 L70 的执行器二选一、PD 同 actuator 约束也保留。 |
| N01 · P2 | **CLOSED** | 正文 L66 已删“既有引擎进程内”限定，改为同一逻辑服务 DP engine cores 的分布式拓扑重配置；注明固定路径要求 Ray DP 后端，描述向现有 cores 发重配置、创建新 cores、等待其 ready 与现有 cores 完成重配置，并明确 core ready 不等于 K8s 副本 readiness/路由传播。固定 [core_client.py L1278–1358](https://github.com/vllm-project/vllm/blob/b17039bccc17b94a2ea107272ad7bc93508708df/vllm/v1/engine/core_client.py#L1278-L1358)支持；创建新 cores/等待 ready 是其中的扩容分支，在本段“扩容 ready gate”语境下成立，不代表缩容也创建 cores。 |

C07 的具体支持页为固定 [KPA L8–23](https://github.com/kserve/website/blob/3f4067ea87dd84194bddb1b563051c84306c7997/docs/model-serving/predictive-inference/autoscaling/kpa-autoscaler.md#L8-L23)、[HPA L17–43](https://github.com/kserve/website/blob/3f4067ea87dd84194bddb1b563051c84306c7997/docs/model-serving/predictive-inference/autoscaling/hpa-autoscaler.md#L17-L43)、[KEDA L18–89](https://github.com/kserve/website/blob/3f4067ea87dd84194bddb1b563051c84306c7997/docs/model-serving/predictive-inference/autoscaling/keda-autoscaler.md#L18-L89)、[WVA L13–80](https://github.com/kserve/website/blob/3f4067ea87dd84194bddb1b563051c84306c7997/docs/model-serving/generative-inference/llmisvc/autoscaling/llmisvc-autoscaling.md#L13-L80)及 [CRD 缺失说明 L361](https://github.com/kserve/website/blob/3f4067ea87dd84194bddb1b563051c84306c7997/docs/model-serving/generative-inference/llmisvc/autoscaling/llmisvc-autoscaling.md#L361)。本项关闭仅确认前置分支表述补齐，不证明这些组件已经部署或版本组合已经验证。

## C02 剩余关闭条件

**位置：正文 L102，“vLLM sleep 模式在固定 commit 的实现细节（sleep level、唤醒语义）未核，仅引用教程口径。”**

固定 [gpu_worker.py L109–155](https://github.com/vllm-project/vllm/blob/b17039bccc17b94a2ea107272ad7bc93508708df/vllm/v1/worker/gpu_worker.py#L109-L155)可见 level 2 保存 buffers、level 1 与其他 level 向 allocator 传递不同 offload tags、wake 调 allocator 与恢复 buffers 等分支。这足以支持“已核 worker 分支”，不足以证明 allocator 内部或完整恢复成本。正文 L112 已正确表达这一证据边界，L102 的绝对未知断言仍会让读者误判已取证范围。

数值方面，[sleep 教程 L115–120](https://github.com/vllm-project/production-stack/blob/20a658044af0dea70e9e0136494bb9979cfd9fab/docs/source/use_cases/sleep-wakeup-mode.rst#L115-L120)和 [L169–175](https://github.com/vllm-project/production-stack/blob/20a658044af0dea70e9e0136494bb9979cfd9fab/docs/source/use_cases/sleep-wakeup-mode.rst#L169-L175)确有示例日志；现行来源记录及正文已把它们与本部署基线分开，**该部分不再开放**，也不要求补测才能关闭 C02。

**最小修订：** 仅将正文 L102 与 L112、来源记录 L33 对齐。例如改为：“vLLM sleep 模式已核固定 commit 的 worker 层分支（level 1/2 处理与 wake 调 allocator）；allocator 内部恢复链、完整恢复路径及本部署耗时未核，教程示例不作基线。”不要求新增源码取证、部署、唤醒测试或统一重载结论。修订后只需定向复核该句及其一致性，确认未引入新问题后才能关闭 C02。

## 修订引入的新问题

本轮范围内**未发现需要另立 N02 或后续编号的新问题**。token 行已把概念反例与实测分开；四路径表未将可选观测组件推成全部路径的必要组件，也未将 WVA 文档口径升级为实现或兼容性证明；N01 修订仍保留 core ready 与副本 readiness 的责任边界。

正文 L102 的冲突属于第一轮 C02 明列但未完成的关闭条件，继续沿用 C02，不作重复计数。

## 校验与写入范围

报告落盘后执行 `PYTHONDONTWRITEBYTECODE=1 make check`，结果为 **PASS: 117 content entries; 553 sources**。为遵守“只新增这一个文件”，将当前仓库（含已有 `build/`）复制到临时目录 `/tmp/t0709-recheck2-build-s65w8c_0/repo`，在副本中执行 `make build`，结果同为 **PASS: 117 content entries; 553 sources**，成功重建两个 catalog 文件；读取生成的 JSON 确认 `documents=117`、`sources=553`。工作区 `build/` 未改写。这些检查仅覆盖结构、本地链接与生成过程，不验证技术语义、远端内容或硬件兼容性。

本会话写入工具仅操作本报告。取样前后文件摘要对照发现，工作区另有 T07-10/T07-11 来源记录、GPU OOM 正文及 registry 的并行变化，均非本会话写入，未覆盖或回退；上文 registry 哈希记录的是本轮读取时的取样身份。交付前再次核验被审正文，SHA-256 仍与提交值一致。

本轮未修改 `src/kb/`，无需新增或运行代码测试；没有部署 autoscaler、启动推理服务、调用扩缩容/排空/sleep/wakeup 接口或执行负载对照。正文 `draft / source_checked`、环境档案缺失及未取得三平台实测基线的状态不因本报告改变。C02 关闭前不声明 T07-09 审阅通过。
