# 第二十八批 T07-10 来源记录

任务：T07-10（服务版本发布、副本故障与恢复验证；**new** `knowledge/07-inference/release-and-recovery.md`，主题 07.6/07.7/07.8）。取证轮次：主会话作者角色首轮（2026-10-21；前置 T07-07 done、T07-08/T07-09 同批先行）。未部署/未演练。

版本线：Kubernetes v1.32 静态快照；KServe 网站仓 main@`3f4067e`（0.20 线）；vLLM v0.14.0＝`b17039bc`；Envoy 文档 latest（1.41.0-dev 线）。

## 本轮取回清单

| 文件/页面 | 定位 |
|---|---|
| K8s v1.32 Pod 生命周期页（终止流程段原文抽取，/tmp 快照 pod-lifecycle.html） | v1-32.docs.kubernetes.io/docs/concepts/workloads/pods/pod-lifecycle/ |
| K8s v1.32 探针概念页 | v1-32.docs.kubernetes.io/docs/concepts/configuration/liveness-readiness-startup-probes/ |
| KServe canary.md（21 行，sha fee7893a614ebab8）＋ llmisvc/canary-rollout.md（310 行，sha 89013ecf8dec6244） | kserve/website@3f4067e |
| vLLM api_server.py（sha dcc6b46ca859074d）、async_llm.py（818af4561b7ae54a）、core.py（a7a624e0ed151f00）、core_client.py（601d375067fa724e）、serving_chat.py（6161fd8ec3a21f79） | b17039bc |

## 主张—来源定位表

| 主张 | 登记 ID | 精确位置 | 支持范围 / 未覆盖 |
|---|---|---|---|
| Pod 终止时序（原文核对）：删除记录宽限期（默认 30s）→Terminating；kubelet 本地关闭（preStop 先跑、超时一次性 2s 延展；SIGTERM→各容器 PID1、无 sidecar 任意顺序）**与**控制面 EndpointSlice 摘除**并行**；terminating 端点保留但 ready 恒 false（1.26 前兼容）、LB 不再用于常规流量；宽限期到 SIGKILL；强制删除后 Pod 可能仍在节点运行 | src.kubernetes.pod-lifecycle-v1-32 | pod-lifecycle 终止流程段（原文抽取核对） | v1.32 语义 |
| 探针分工：liveness 失败→重启容器（死锁类）；readiness 失败→从 Service 端点摘除（全生命周期）；startup 成功前禁用 liveness/readiness；liveness 不等 readiness | src.kubernetes.probes-v1-32 | 概念页 | 概念分工；各机制默认值在任务页（未取，未引用具体默认值） |
| InferenceService 金丝雀：仅 serverless；canaryTrafficPercent 按百分比在新修订与 LatestRolledoutRevision 间分流；坏修订不分流；晋升/回退为修订字段语义 | src.kserve.rollout-v0-20-3f4067e | canary.md 全文 | Knative 修订模型 |
| LLMInferenceService 金丝雀：spec.router.route.group+weight 比例权重（对称成员、无主从）；控制器为组内每成员写 HTTPRoute 加权 backendRef（Gateway API）；**weight:0 暗部署有 CDS+RDS 同时更新引发瞬时连接失败风险，建议 weight:1 起步**；灰度门=P95 TTFT 对比 PromQL；晋升=stop 注解（pod 缩零释放 GPU、保留资源与权重供回退）；回退=降权重或去 stop；组成员须同模型名与 LoRA 集（否则 MemberDivergence） | src.kserve.rollout-v0-20-3f4067e | llmisvc/canary-rollout.md L16-58（机制）、L60-75（dark/live）、步骤 1-6 | v0.20 线文档口径；控制器实现未取 |
| Envoy 排空：overload manager 动作 disable_http_keepalive=H2/H3 GOAWAY＋H1 idle 计时；stop_accepting_requests=新请求 503；离群弹出与主动健康检查交互（通过即解除弹出） | src.envoy.overload-manager-latest-2026-10-21；src.envoy.outlier-detection-arch-latest-2026-10-21 | 配置参考页/架构页 | 代理层排空与摘除 |
| vLLM 关闭语义（**已被复核轮修订取代**，现行主张）：四件已核事实分立——初始化 SIGTERM→KeyboardInterrupt（L1296-1300）；FastAPI lifespan 只取消统计任务并清 app.state、**不**调引擎 shutdown（L117-143）；async_llm.shutdown() 在外层 engine client 上下文 finally（L229-232）；HTTP shutdown task 在 backend 上下文退出后才被 await（L1371-1373）。引擎死亡三种路径分列——启动失败仅日志+异常（core.py L931-943 启动分支，不发 marker）；运行期异常发 ENGINE_CORE_DEAD、客户端收 EngineDeadError；突然退出走条件启用的 sentinel 监控（guard：engine_manager 存在且 processes 非空，L583-595，不需 marker） | 扩展 src.vllm.inference-v0-14 | api_server.py L117-143/L229-232/L1296-1300/L1371-1373；core.py L931-943；core_client.py L425-428/L583-621；async_llm.py L455-459 | 该 commit；`serve_http`/uvicorn 完整信号处理与在途流终态未核 |
| 请求取消→资源释放链：断连/取消→abort（外部/内部 ID 级联、子请求取消、finish_reason=ABORT 终止输出、LoRA 计数清理、_requests_drained 事件） | 扩展 src.vllm.inference-v0-14 | async_llm.py L448-458/L551-566；output_processor.py L393-456 | 该 commit；**不承诺 exactly-once 或断点续传**：流式已输出 token 不因重试恢复（正文按此边界写） |
| 版本制品身份（模型/tokenizer/config/量化）：模型身份固定清单与 load-format 不可互推（T07-01 交付）；量化身份＝格式–kernel–运行 dtype 三层分立（T07-04 交付） | 既有 src.vllm.model-loader-v0-14、src.vllm.tokenizer-registry-v0-14 等 | T07-01/T07-04 交付正文 | 复用 |
| PD 单侧失败：kv_load_failure_policy（默认 recompute）、connector 中止清理超时（480s）等失败链 | 既有 src.vllm.inference-v0-14（T07-07 登记） | pd-disaggregation.md 交付正文 | 复用 |

## unknown 清单

1. KServe LLMISvc canary 控制器（kserve 仓 CRD/controller）实现未取回；HTTPRoute/Gateway 实现后（如 Envoy Gateway）对权重变更的生效时延未核。
2. vLLM 收到 SIGTERM 后在途流式请求是否被排空（uvicorn graceful shutdown 与 engine shutdown 的先后）未逐行核——正文以"须用 preStop/宽限期显式排空"为方法边界，不声称引擎自动排空。
3. 副本故障后的缓存（**已被复核轮修订取代**，现行口径）：仅被终止进程的**本地**活动 KV/prefix cache 不自动被继承；外部/offload 缓存与远端 KV 的幸存、重新挂载、身份兼容与会话恢复契约按所选实现核对，无证据即 unknown——不把 PD connector/offload 路径当作跨副本恢复能力边界，也不判"重拉必为冷 cache"（正文按所有者分列写）。
4. 重试风暴定量：SRE 章节给的是通用原则与比例（10% 预算等），推理场景的数值须各环境压测。
5. 未执行任何发布/故障注入演练；全部为文档与源码级证据。

## 初审修订轮（2026-10-21，响应 batch-28-t07-10-codex-review.md 的 C01–C11）

- C01：新增 drain 子流程六步（停止新准入→观察路由收敛→在途计数→预登记期限→超时策略与终态不确定记录→资源核对）；preStop 消耗同一宽限期、部分运行时尊重 STOPSIGNAL（不无条件写 SIGTERM）；GOAWAY 是连接层动作不证明请求完成；"有钩子≠排空成立"。
- C02：vLLM 关闭责任拆四件已核事实（初始化 SIGTERM→KeyboardInterrupt；lifespan 只清统计任务与 app.state L117-143；async_llm.shutdown() 在外层 engine context finally L229-232；HTTP shutdown task 在 backend 退出后 await L1371-1373）；uvicorn/serve_http 完整行为保留 unknown；来源记录 EngineDead 锚点改 L455-459。
- C03：回退拆两分支（旧版运行=降权重部分减流；旧版已停=去注解重启、Ready/gate 后按保留权重入组——9:9 重启仍 50/50 非 100% 回旧版，完全隔离须核对直达路径）；stop 保留的是资源与声明权重非运行态。
- C04：PD 行按实现分列（MindIE "Pull kv failed" 为该实现日志；480s 为 NIXL/Mooncake P 端条件超时，Mooncake 传输期设无穷、清理仅遍历到期项、进程死亡不保证清理；recompute 仅限 connector 上报的加载失败）；不跨实现拼接、不等 480s 默认已清理。
- C05：删"唯一防线"；区分关联 ID/客户端展示去重/服务端幂等（无已核保证）/外部副作用协议；引入路由页三分重试边界；取消返回与资源回收分立；续传限定本轮 chat/completion 路径。
- C06：缓存按所有者分列（被终止进程本地 KV/prefix 不自动继承；外部/offload 幸存与身份兼容按实现核对 unknown；PD 交接≠会话续传≠跨版本兼容）；TTFT 只作联合观察。
- C07：worker/engine 死亡证据链拆三种（启动失败仅日志+异常不一定发标记；运行期异常发 ENGINE_CORE_DEAD；突然退出走条件启用的 sentinel 监控 L583-621 不需标记）；不能因缺 marker 排除死亡。
- C08：回退条件逐项注明比较方向（延迟分位超上限、达标率/goodput 低于下限、质量超容差）。
- C09：验证设计改事件时间表（触发/发现/控制面/数据面最后选中旧副本/接流/回稳定——收敛与中断窗口分开报告）；逻辑请求+attempt 对账（重复/遗漏定义分母与截止点）；停止后撤压恢复闭环。
- C10：weight:0 风险改条件性表述（文档标注理论）；weight:1=带约 10% 真流量非纯 warmup；MemberDivergence=独立子组+GroupDegraded；控制器/Gateway 前置与未核声明。
- C11：正文补 05 域两篇普通链接（平台变更与回退、控制面恢复）；来源节两类 canary 分列链接、overload/outlier 精确页分开。

## 复核第一轮修订·补充（2026-10-21，响应 batch-28-t07-10-codex-recheck.md 的 C02/C03/C06/C07 剩余与 N01）

- C02 剩余：来源记录 vLLM 关闭主张行改写（四件已核事实分立＋三种死亡路径分列）并标注取代旧表述。
- C03 剩余：正文补"Ready 即按保留权重接流"的样板语义；要求 gate 的方案须另行满足 readiness 准入门/入口隔离前提（gate 期间阻止组内与直达路径），先接流再验证则明确为带流验证＋预登记预算。
- C06 剩余：来源记录 unknown 3 改为所有者分列的现行口径（本地不自动继承；外部/offload 按实现核对；不把 PD 路径当恢复能力边界）。
- C07 剩余：来源记录死亡路径三分列；正文补 sentinel 已核局部 guard（engine_manager 存在且 processes 非空否则不启动监控，L583-595）。
- N01：drain 子流程导语改为"本流程不假设引擎会自动排空在途流——完整 serve_http/uvicorn 关闭行为与在途流终态仍待核实"。
