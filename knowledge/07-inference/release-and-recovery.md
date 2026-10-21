---
id: inference.release-and-recovery
title: 服务版本发布、副本故障与恢复验证
type: procedure
domain: inference
status: draft
platforms: [generic, nvidia, amd, ascend]
source_refs:
  - src.kubernetes.pod-lifecycle-v1-32
  - src.kubernetes.probes-v1-32
  - src.kserve.rollout-v0-20-3f4067e
  - src.vllm.inference-v0-14
  - src.envoy.overload-manager-latest-2026-10-21
  - src.envoy.outlier-detection-arch-latest-2026-10-21
  - src.google.sre-cascading-failures
  - src.google.sre-effective-troubleshooting
updated_at: "2026-10-21"
summary: 把灰度/滚动发布、健康摘除、回退与副本故障后的恢复组织成可验证流程：liveness/readiness/实际推理质量三层分开，版本制品身份按模型/tokenizer/config/adapter/量化固定；预热与流量递增、SLO/质量 gate、旧副本 drain 与终止时序（preStop/SIGTERM/端点摘除并行）按固定版本样板落地；worker/engine 死亡、副本丢失、PD 单侧失败、重试风暴与状态残留分证据与处置分支；不承诺 exactly-once，已输出 token 与 cache 身份按实现语义处理；给出基线→受控切换→摘除→恢复/回退的验证设计与核对项。
related_ids:
  - inference.routing-and-flow-control
  - inference.capacity-and-autoscaling
  - inference.model-loading-and-readiness
  - inference.pd-disaggregation
  - inference.output-quality-evaluation
  - cluster-platform.node-drain-resource-reclamation
  - cluster-platform.platform-change-and-rollback
  - cluster-platform.control-plane-recovery
applicability:
  environment_refs: []
  notes: "控制面样板为 Kubernetes v1.32 静态快照、KServe 0.20 线（InferenceService 与 LLMInferenceService 金丝雀）与 Envoy 1.41.0-dev 文档线；引擎侧为 vLLM v0.14.0。其他编排/引擎版本的语义须另行核对。"
verification:
  status: source_checked
  evidence_refs:
    - src.kubernetes.pod-lifecycle-v1-32
    - src.kserve.rollout-v0-20-3f4067e
    - src.vllm.inference-v0-14
  notes: "已核对 v1.32 Pod 终止流程原文（kubelet 本地关闭与 EndpointSlice 摘除并行、terminating 端点 ready 恒 false）与探针概念页、KServe 两类金丝雀文档（canaryTrafficPercent 与 group/weight 权重路由、weight:0 的 CDS/RDS 风险、stop 注解晋升）、vLLM v0.14.0 关闭/SIGTERM/EngineDead/取消实现。未执行任何发布或故障注入演练。逐条主张与定位见 docs/research/batch-28-t07-10-sources.md。"
---

# 服务版本发布、副本故障与恢复验证

## 三层"健康"与版本制品身份

发布与恢复的第一个纪律是把三层判据分开：**liveness**（进程活着吗——失败则重启容器，K8s 语义见[探针概念页](https://v1-32.docs.kubernetes.io/docs/concepts/configuration/liveness-readiness-startup-probes/)，死锁类问题靠它）、**readiness**（能接新流量吗——失败则从 Service 端点摘除，全生命周期运行）、**实际推理质量**（输出还正确吗——探针测不出来）。引擎的 `/health` 与 ready 语义（T07-01 已核：health 不等于完成预热）只能覆盖前两层；质量层的 gate 要靠固定输入集的输出比对（方法见[输出质量对照评估](output-quality-evaluation.md)）——升级同时换了量化格式或 kernel 路径时，"200 OK"不等于"结果没变"。

**版本制品身份**：一次"发版"变更的对象按清单固定——模型权重（来源/revision/分片格式）、tokenizer、config（含 `max_model_len` 等影响行为的字段）、LoRA adapter 集合、量化格式与 scale（格式–kernel–运行 dtype 三层分立，见[推理量化与输出质量](quantization-and-quality.md)）、镜像/依赖。KServe 对金丝雀组成员的硬约束可作参照：组内成员必须同模型名与同 LoRA adapter 集，否则标记 `MemberDivergence` 降级（[canary-rollout 文档](https://kserve.github.io/website/docs/model-serving/generative-inference/llmisvc/canary-rollout)）——即**流量组内隐含的兼容假设要显式核对**。

## 发布流程：预热→递增→gate→drain→回退条件

以固定样板拼出推理服务的一次灰度（两条官方实现路径按部署模式二选一）：

1. **新版本预热**：新副本（新修订）部署后等 ready 并完成 warmup（引擎侧五阶段见[权重加载与引擎 ready](model-loading-and-readiness.md)）。KServe LLMInferenceService 文档给出反例教训：**不要以 `weight: 0` 暗部署**——文档以条件性解释说明风险（理论：权重为 0 时网关可能未预热后端集群，之后调到非 0 会让集群发现（CDS）与路由（RDS）更新同时发生，CDS 更新可短暂破坏连接）；建议 `weight: 1` 起步——注意这不是无流量 warmup：9:1 例中 weight:1 在 Ready 后立即承接约 10% 真实流量（实际占比取决于全部活跃成员权重），恰好用于在放大前用真请求验证 vLLM/scheduler 全链（[同文档 Starting dark vs starting live](https://kserve.github.io/website/docs/model-serving/generative-inference/llmisvc/canary-rollout)）。前置条件：已安装 LLMInferenceService 控制器、Gateway API 实现支持加权 backendRef（控制器/网关实现本轮未核）。组成员身份约束：模型名或 LoRA adapter 集不一致的成员会**形成独立子组**并标 `GroupDegraded=True / reason MemberDivergence`，不再参与原组分流。
2. **流量递增**：KServe InferenceService（serverless）用 `canaryTrafficPercent` 在新修订与 `LatestRolledoutRevision` 间按百分比分流，坏修订不接流量；LLMInferenceService 用 `spec.router.route.group`+`weight` 比例权重（对称成员），控制器为组内每成员写 HTTPRoute 加权 backendRef，只 patch 变更侧即可移权重（同上文档）。
3. **质量与 SLO gate**：官方示例用 P95 TTFT 对比（`vllm:time_to_first_token_seconds_bucket` PromQL）决定是否继续递增（同上文档 Step 3）；质量 gate 叠加固定输入集输出比对与错误率/取消率观察，判据预注册（每项注明指标、单位、窗口、分母与**比较方向**），不边看边定阈值。
4. **晋升与旧副本 drain**：确认后把流量提到 100%。LLMInferenceService 的晋升方式是给旧版本打 `serving.kserve.io/stop=true`：旧 pod 缩零、GPU 释放，但**资源与声明权重保留在组状态里供回退**（保留的是资源与权重声明，不是运行中的 GPU 占用或 KV 状态；同上文档 Step 5）。通用 K8s 侧的终止时序（原文核对）：删除请求记录宽限期（默认 30s）→ Pod 转 Terminating；**kubelet 本地关闭与控制面端点摘除并行进行**——kubelet 先跑 preStop 钩子（宽限期非 0 时；**preStop 消耗同一宽限期**，超时仅一次性 2s 延展），再向容器 PID1 发停止信号（无 sidecar 时顺序任意；部分运行时尊重镜像 `STOPSIGNAL`，不能无条件写成 SIGTERM）；控制面同时评估把 Pod 从 EndpointSlice/Endpoints 摘除，terminating 端点保留但 `ready` 恒为 false（1.26 前兼容口径）、排空场景另有 `serving` 条件，负载均衡不再用于常规流量；宽限期到 SIGKILL（[Pod 生命周期](https://v1-32.docs.kubernetes.io/docs/concepts/workloads/pods/pod-lifecycle/)）。

   **在途流式请求的 drain 子流程**（待执行清单；本流程**不假设**引擎会自动排空在途流——完整 `serve_http`/uvicorn 关闭行为与在途流终态仍待核实，见下方已核事实与 unknown）：① 记录 drain 目标（副本、在途数）与剩余服务容量；② 停止该副本新准入（路由/端点摘除），**观察实际路由收敛**（入口侧无新请求到达该副本的证据，而不是假设摘除即生效）；③ 维护已接纳流的完成/取消计数；④ 在预登记期限内等待计数归零；⑤ 超时按预登记策略终止并记录**终态不确定**的请求（客户端可能已收到部分输出）；⑥ 核对进程退出与设备资源回收。preStop 的职责（如先通知引擎/入口再等待）、停止信号配置与共用宽限期预算是部署前提；未实现时明确记录缺失，**有钩子不等于排空成立**。代理层排空的对应样板：Envoy overload manager 的 `disable_http_keepalive` 动作用 GOAWAY 排空 H2/H3 连接（[配置页](https://www.envoyproxy.io/docs/envoy/latest/configuration/operations/overload_manager/overload_manager)）——GOAWAY 是连接层动作，不证明应用请求完成。

   **vLLM 关闭责任的已核事实**（固定快照，四件事分开）：初始化期 SIGTERM 处理器抛 KeyboardInterrupt（[api_server.py L1296-1300](https://github.com/vllm-project/vllm/blob/b17039bccc17b94a2ea107272ad7bc93508708df/vllm/entrypoints/openai/api_server.py#L1296-L1300)）；FastAPI lifespan 退出只取消统计任务并清理 app.state（[L117-143](https://github.com/vllm-project/vllm/blob/b17039bccc17b94a2ea107272ad7bc93508708df/vllm/entrypoints/openai/api_server.py#L117-L143)）；引擎 `async_llm.shutdown()` 在外层 engine client 上下文的 finally 调用（[L229-232](https://github.com/vllm-project/vllm/blob/b17039bccc17b94a2ea107272ad7bc93508708df/vllm/entrypoints/openai/api_server.py#L229-L232)）；HTTP shutdown task 在 backend 上下文退出后才被 await（[L1371-1373](https://github.com/vllm-project/vllm/blob/b17039bccc17b94a2ea107272ad7bc93508708df/vllm/entrypoints/openai/api_server.py#L1371-L1373)）。`serve_http`/uvicorn 的完整信号处理与在途流行为仍 unknown——以上局部顺序不能反推"引擎自动排空"。

   **回退的两个不等价分支**（旧版本状态决定）：旧版本**仍在运行**时，降低新版本权重即可把流量按权重重新分配给旧版本（部分减流）；旧版本**已被 stop** 时，须去注解重启。**样板语义是"Ready 即按保留权重接流"**（去 stop 后 v1 一旦 Ready 即承担组内份额——9:9 时约一半；文档未提供控制器等待发布者预热/质量核对后再接流的机制）。因此若回退方案要求"预热/质量通过后才接流"，须**另行**满足前提：经核对的 readiness 准入门（如探针门/自定义 gate）或入口隔离（gate 期间阻止组内与直达路径提前选中旧版，gate 通过后放开并核对实际流量）；该机制未实现时明确记为缺失。若采用"先接流再验证"，则明确为**带流验证**并预登记预算/停止条件，不声称质量 gate 在接流前完成。无论哪种：按保留权重入组后 9:9 仍是 50/50、**不是回到旧版本 100%**，需再调权重达回退目标；冷启动耗时计入回退窗口；完全隔离坏版本还要核对直达版本的路由路径（[canary-rollout 回退段](https://kserve.github.io/website/docs/model-serving/generative-inference/llmisvc/canary-rollout)）。InferenceService（serverless）回退=流量钉回 `PreviousRolledoutRevision`。
5. **回退条件**（预注册，触发即执行，逐项注明比较方向）：新版本错误率/取消率**高于上限**、延迟分位（TTFT/TPOT/E2E）**超过上限**、逐请求达标率/goodput **低于下限**、质量比对**超出容差**、或出现新版本特有的引擎错误形态。回退按旧版本状态分支（见下）。

## 副本与引擎故障：证据与处置分支

| 故障形态 | 可观察证据（固定样板） | 处置分支 |
|---|---|---|
| worker/engine 死亡（按证据链分三种，不是统一链条） | ① **启动失败**：EngineCore 只记录日志后抛出异常（[core.py L927-943](https://github.com/vllm-project/vllm/blob/b17039bccc17b94a2ea107272ad7bc93508708df/vllm/v1/engine/core.py#L927-L943) 的启动分支）——**不一定发死亡标记**；② **运行期捕获异常**：core 进程的异常分支调 `_send_engine_dead()` 发 ENGINE_CORE_DEAD 标记，客户端收 `EngineDeadError`（同文件运行期分支；[core_client.py L425-428](https://github.com/vllm-project/vllm/blob/b17039bccc17b94a2ea107272ad7bc93508708df/vllm/v1/engine/core_client.py#L425-L428)）；③ **进程突然退出**：条件启用的进程 sentinel 监控可置 `engine_dead` 并关闭 client——**不要求先收到标记**（[core_client.py L583-621](https://github.com/vllm-project/vllm/blob/b17039bccc17b94a2ea107272ad7bc93508708df/vllm/v1/engine/core_client.py#L583-L621)；已核局部 guard：`resources.engine_manager` 须存在、有 `processes` 属性且列表非空，否则不启动该监控线程，[L583-595](https://github.com/vllm-project/vllm/blob/b17039bccc17b94a2ea107272ad7bc93508708df/vllm/v1/engine/core_client.py#L583-L595)；各部署是否满足该 guard、worker→core 完整传播未核，unknown）。三种都**不区分根因**（OOM/驱动/内部错误靠更早异常、退出码/信号与 Pod 终态/事件组合判断，见[GPU 推理 OOM 诊断](gpu-inference-oom-triage.md)）；不能因缺少 marker 排除副本死亡 | 单副本死亡：入口层摘除（被动离群/主动探针），请求由路由层失败转移或客户端重试（重试边界见[请求路由与流控](routing-and-flow-control.md)）；引擎内死亡对在途请求是终止性错误（不逐请求 abort，引擎整体关停） |
| 副本丢失（pod/节点级） | K8s：节点 not-ready/lifecycle 摘除（[节点回收](../05-cluster-platform/node-drain-resource-reclamation.md)）；readiness 失败自动摘端点 | 重建副本走完整冷启动（见[容量与扩缩容](capacity-and-autoscaling.md)）；重建期间容量下降，入口层按过载策略兜底 |
| PD 单侧失败（按实现分列，不跨实现拼接） | **MindIE**：D 侧 "Pull kv failed"（ERROR＋CANN status_code 含 timeout）为该实现特定日志（[PD 分离](pd-disaggregation.md) MindIE FAQ 条目）；**上游 NIXL/Mooncake**：480s 是 P 端保留块的条件超时配置（NIXL 在 prefill 完成且延迟释放时设期限 [L770-792](https://github.com/vllm-project/vllm/blob/b17039bccc17b94a2ea107272ad7bc93508708df/vllm/distributed/kv_transfer/kv_connector/v1/nixl_connector.py#L770-L792)；Mooncake 发起传输时期限设为无穷 [L565-593](https://github.com/vllm-project/vllm/blob/b17039bccc17b94a2ea107272ad7bc93508708df/vllm/distributed/kv_transfer/kv_connector/v1/mooncake_connector.py#L565-L593)、过期清理仅遍历到期项 [L746-764](https://github.com/vllm-project/vllm/blob/b17039bccc17b94a2ea107272ad7bc93508708df/vllm/distributed/kv_transfer/kv_connector/v1/mooncake_connector.py#L746-L764)）——**进程死亡不保证执行清理**；kv_load_failure_policy 的 recompute 只作用于 connector 检测并上报的 KV 加载失败（base 默认空集、NIXL 有上报、上游 Mooncake 对应错误终态未证） | 先隔离受影响路径再按具体实现核对清理/重建；单侧摘除重建；失败落在哪一侧用 connector 指标/日志定位——**不要等 480s 后默认"已清干净"，也不默认所有传输失败都能重算恢复**（详见[PD 分离失败链](pd-disaggregation.md)） |
| 重试风暴 | SRE 形态：饱和→上游超时→重试放大→更深饱和（死亡螺旋）；多层级联重试相乘（3 层各 3 次=后端 64 次）（[Cascading Failures](https://sre.google/sre-book/addressing-cascading-failures/)） | 限重试层（只在一层重试）、重试预算与随机指数退避、过载返回可区分状态、入口断路器先行（见[请求路由与流控](routing-and-flow-control.md)）；恢复期把流量降到远低于原崩溃点再缓升 |
| 状态残留（进程死后资源/状态未清） | GPU 显存残留（`nvidia-smi`/`amd-smi`/`npu-smi` 对账）、僵尸进程、存储上的临时 KV/offload 数据 | 摘除→清理→核对设备内存账目再准入（核对项见各平台 OOM 指南）；K8s 强制删除（`--force --grace-period=0`）后 Pod 可能仍在节点运行（[Pod 生命周期](https://v1-32.docs.kubernetes.io/docs/concepts/workloads/pods/pod-lifecycle/)），必须到节点核对进程/显存 |

## 语义边界：不承诺 exactly-once

- **已输出 token**：流式响应已发出的 token 不可撤回；重试/故障转移生成的是**新**响应（本轮所选普通 chat/completion 路径无续传契约证据，其他恢复协议 unknown）。区分几件不同的事：**关联 ID**（X-Request-Id 回显/生成，仅用于串联日志）、**客户端展示层去重**（按关联 ID 去重展示——客户端自己的责任）、**服务端幂等/执行去重**（本快照无已核保证：同一外部 ID 可对应多个实际内部请求）与**外部副作用协议**（上层定义）。重试前提按[请求路由与流控](routing-and-flow-control.md)的三分边界：连接未建立（可重试）、已送达未见响应（原请求执行状态不明，可能重复执行）、响应已提交（不透明重试，交回客户端）。取消返回与资源回收是**不同事件**（前端收到取消结果≠KV 块已归还，见取消链边界）。
- **会话与 cache 身份（按所有者分列）**：被终止进程的**本地**活动 KV 与本地 prefix cache 不自动被新副本继承；**外部/offload 缓存组件**是否幸存、能否重新挂载、身份是否兼容（token/block 对齐、LoRA、多模态、隔离字段与模型版本——命中条件见[执行与 KV cache](execution-and-kv-cache.md) 的复用边界）按所选实现核对，无证据时 unknown。会话亲和的哈希环在副本集合变化时部分会话重落（机制见[请求路由与流控](routing-and-flow-control.md)）。PD connector/offload 是**请求级 KV 交接**路径（[PD 分离](pd-disaggregation.md)），不等于会话断点续传，也不证明跨版本缓存兼容。恢复核对应记录缓存身份与实际命中证据；TTFT 只作联合观察，不单独证明"缓存已恢复"。
- **外部副作用**：推理本身通常无副作用，但工具调用/检索增强类请求可能触发外部动作——这类请求的重试语义按具体上层协议定义，本库样板不含对应实现，不外推。
- **恢复 ≠ 正确**：服务恢复 200/ready 后，仍需质量抽查与错误率稳定窗确认（验证方法见下）。

## 验证设计：基线→受控切换/故障→恢复

每轮固定：负载形态与输入集、版本身份（新旧制品清单）、路由/入口配置、观测采集（错误/重复/遗漏/延迟/质量）。步骤与核对项：

1. **基线窗口**：稳定负载下记录 SLO 分位、goodput、错误分类、质量比对基准（固定输入集，方法见[输出质量对照评估](output-quality-evaluation.md)）。
2. **受控事件**（二选一或分别做）：a) 版本切换——按上文灰度流程执行到晋升；b) 故障注入——对单副本触发终止（正常删除）或 kill（异常死亡）。事件时间按**待填表**分别记录（不做单一"摘除时延"混算）：变更/故障触发时刻、发现时刻（探针/离群/日志）、控制面状态变化（EndpointSlice/修订权重）、**数据面最后一次选中旧副本**的时刻（入口侧证据）、新版本/恢复版开始接流时刻、服务回到稳定基线时刻——"数据面收敛"与"用户可见中断窗口"分开报告。
3. **重复/遗漏对账**：按**逻辑请求＋ attempt** 关联（客户端请求 ID × 重试序号），每个 attempt 记录是否被接纳、响应是否已提交、终态（完成/错误/取消/未知）与输出版本；重复＝同一逻辑请求收到多个已提交的完整响应，遗漏＝已接纳但无终态且超截止点——分母与结算截止点预登记；流式 chunk、合法重试与"发 N 收 M"的差额不混入。不能用"报告总数相等"证明请求正确恢复。
4. **恢复核对**：新副本 ready 时间（冷启动全程）、缓存身份与实际命中记录（TTFT 只作联合观察）、设备资源对账（无残留进程/显存）、错误率回到基线的稳定窗口长度（预登记本轮达标/超时判据）、质量比对回到容差内。
5. **回退演练**：从新版本按预注册条件回退（按旧版本运行/已停分支执行），核对回退耗时（含冷启动）与实际流量分配符合回退目标。
6. **停止条件与恢复闭环**：出现未预期的错误形态（如重复响应、串话——请求状态串扰的证据）立即停止，保留全量日志时间线再分析；停止后撤压、恢复配置与副本边界，核对路由、错误、SLO、质量与资源回到基线稳定窗后本轮才结束；排障方法沿用[有效排障](https://sre.google/sre-book/effective-troubleshooting/)的证据链纪律。跨域参照：平台组件回退与回服的集群侧流程见[平台变更与回退](../05-cluster-platform/platform-change-and-rollback.md)，控制面故障后的账本核对见[控制面恢复](../05-cluster-platform/control-plane-recovery.md)——它们负责平台层，本页负责请求/服务层。

平台操作（K8s 滚动更新参数、KServe 字段、Envoy 配置）按各自版本另行记录适用环境；演练须在隔离环境获得授权后执行，本文流程不构成执行授权。

## 边界与未知

- KServe 金丝雀控制器实现与 Gateway 实现的权重生效时延未核；Knative 修订模型仅 serverless 模式。
- vLLM 优雅关闭对在途流式请求的排空行为未在上游文档化（不假设自动排空）；`uvicorn` 关闭序列与 engine shutdown 的先后未逐行核。
- K8s 探针机制的具体默认值（periodSeconds 等）在本批来源页未列，本文未引用数值。
- 故障注入仅给出设计；未执行任何演练，全部处置分支为样板证据＋方法组合，非实测结论。

## 来源与验证记录

- [Kubernetes v1.32 Pod 生命周期](https://v1-32.docs.kubernetes.io/docs/concepts/workloads/pods/pod-lifecycle/)（终止时序原文核对）与[探针概念页](https://v1-32.docs.kubernetes.io/docs/concepts/configuration/liveness-readiness-startup-probes/)。
- [KServe Canary Rollout——InferenceService（predictive 页）](https://kserve.github.io/website/docs/model-serving/predictive-inference/rollout-strategies/canary)与[LLMInferenceService canary-rollout（generative 页）](https://kserve.github.io/website/docs/model-serving/generative-inference/llmisvc/canary-rollout)（网站仓 pin 3f4067e）：canaryTrafficPercent、group/weight 权重路由、weight:0 风险（条件性解释）、weight:1 带真流量、stop 注解晋升、两分支回退语义、MemberDivergence 子组。
- [vLLM v0.14.0 固定快照](https://github.com/vllm-project/vllm/tree/b17039bccc17b94a2ea107272ad7bc93508708df)：SIGTERM/lifespan 关闭链、EngineDead 传播、请求取消与资源释放。
- [Envoy overload manager（架构概览](https://www.envoyproxy.io/docs/envoy/latest/intro/arch_overview/operations/overload_manager)＋[配置参考](https://www.envoyproxy.io/docs/envoy/latest/configuration/operations/overload_manager/overload_manager)）与[outlier detection 架构页](https://www.envoyproxy.io/docs/envoy/latest/intro/arch_overview/upstream/outlier)（1.41.0-dev 线）：排空动作、离群摘除/弹出与主动健康检查交互。
- [SRE Book 第 22 章](https://sre.google/sre-book/addressing-cascading-failures/)、[有效排障](https://sre.google/sre-book/effective-troubleshooting/)：级联失效与重试纪律、排障证据链。
- 逐条主张与证据定位见[第二十八批 T07-10 来源记录](../../docs/research/batch-28-t07-10-sources.md)。
- 当前验证范围：来源核对；未执行发布或故障注入演练。
