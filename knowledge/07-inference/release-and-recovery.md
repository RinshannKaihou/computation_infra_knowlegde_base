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

1. **新版本预热**：新副本（新修订）部署后等 ready 并完成 warmup（引擎侧五阶段见[权重加载与引擎 ready](model-loading-and-readiness.md)）。KServe LLMInferenceService 文档给出反例教训：**不要以 `weight: 0` 暗部署**——从 0 调到非 0 会同时触发网关的集群发现（CDS）与路由（RDS）更新，CDS 更新可短暂破坏连接；建议 `weight: 1` 起步让后端预热（[同文档 Starting dark vs starting live](https://kserve.github.io/website/docs/model-serving/generative-inference/llmisvc/canary-rollout)）。
2. **流量递增**：KServe InferenceService（serverless）用 `canaryTrafficPercent` 在新修订与 `LatestRolledoutRevision` 间按百分比分流，坏修订不接流量；LLMInferenceService 用 `spec.router.route.group`+`weight` 比例权重（对称成员），控制器为组内每成员写 HTTPRoute 加权 backendRef，只 patch 变更侧即可移权重（同上文档）。
3. **质量与 SLO gate**：官方示例用 P95 TTFT 对比（`vllm:time_to_first_token_seconds_bucket` PromQL）决定是否继续递增（同上文档 Step 3）；质量 gate 叠加固定输入集输出比对与错误率/取消率观察，判据预注册，不边看边定阈值。
4. **晋升与旧副本 drain**：确认后把流量提到 100%。LLMInferenceService 的晋升方式是给旧版本打 `serving.kserve.io/stop=true`：旧 pod 缩零、GPU 释放，但**资源与权重保留在组状态里供回退**（同上文档 Step 5）。通用 K8s 侧的终止时序（原文核对）：删除请求记录宽限期（默认 30s）→ Pod 转 Terminating；**kubelet 本地关闭与控制面端点摘除并行进行**——kubelet 先跑 preStop 钩子（宽限期非 0 时；超时仅一次性 2s 延展），再向各容器 PID1 发 SIGTERM（无 sidecar 时顺序任意）；控制面同时评估把 Pod 从 EndpointSlice/Endpoints 摘除，terminating 端点保留但 `ready` 恒为 false（1.26 前兼容口径），负载均衡不再用于常规流量；宽限期到 SIGKILL（[Pod 生命周期](https://v1-32.docs.kubernetes.io/docs/concepts/workloads/pods/pod-lifecycle/)）。流式推理服务的含义：**preStop 钩子＋足够宽限期是在途流式请求排空的通用手段**；引擎收到 SIGTERM 的行为按版本核对（vLLM v0.14.0 的 SIGTERM 处理器在初始化期抛 KeyboardInterrupt，正常期经 lifespan 退出链调 `shutdown()`，[api_server.py L1296-1300/L164-233](https://github.com/vllm-project/vllm/blob/b17039bccc17b94a2ea107272ad7bc93508708df/vllm/entrypoints/openai/api_server.py#L1296-L1300)；在途流是否被排空未在上游文档化——不假设引擎自动排空，以显式 drain 设计为准）。代理层排空的对应样板：Envoy overload manager 的 `disable_http_keepalive` 动作用 GOAWAY 排空 H2/H3 连接（[配置页](https://www.envoyproxy.io/docs/envoy/latest/configuration/operations/overload_manager/overload_manager)）。
5. **回退条件**（预注册，触发即执行）：新版本错误率/取消率超阈、SLO 分位跌破目标、质量比对超容差、或出现新版本特有的引擎错误形态。LLMInferenceService 回退=降新版本权重，或对已 stop 的旧版本去注解重启（冷启动耗时计入回退窗口）；InferenceService 回退=流量钉回 `PreviousRolledoutRevision`。

## 副本与引擎故障：证据与处置分支

| 故障形态 | 可观察证据（固定样板） | 处置分支 |
|---|---|---|
| worker/engine 死亡（进程内不可恢复错误） | vLLM：EngineCore 记录 "failed to start"（启动期）或 "encountered a fatal error"（运行期），传播 ENGINE_CORE_DEAD，客户端收 `EngineDeadError`（[core.py L927-943](https://github.com/vllm-project/vllm/blob/b17039bccc17b94a2ea107272ad7bc93508708df/vllm/v1/engine/core.py#L927-L943)、[core_client.py L425-428](https://github.com/vllm-project/vllm/blob/b17039bccc17b94a2ea107272ad7bc93508708df/vllm/v1/engine/core_client.py#L425-L428)）；此信号**不区分根因**（OOM/驱动/内部错误要靠更早日志，见[GPU 推理 OOM 诊断](gpu-inference-oom-triage.md)） | 单副本死亡：入口层摘除（被动离群/主动探针），请求由路由层失败转移或客户端重试；引擎内死亡对在途请求是终止性错误（不逐请求 abort，引擎整体关停） |
| 副本丢失（pod/节点级） | K8s：节点 not-ready/lifecycle 摘除（[节点回收](../05-cluster-platform/node-drain-resource-reclamation.md)）；readiness 失败自动摘端点 | 重建副本走完整冷启动（见[容量与扩缩容](capacity-and-autoscaling.md)）；重建期间容量下降，入口层按过载策略兜底 |
| PD 单侧失败 | P 侧或 D 侧死亡：D 侧 "Pull kv failed"/传输超时链、connector 保留期超时（480s）释放 KV（[PD 分离](pd-disaggregation.md)） | 单侧摘除重建；KV 传输失败政策按引擎配置（默认 recompute 重算）——失败落在哪一侧用 connector 指标/日志定位 |
| 重试风暴 | SRE 形态：饱和→上游超时→重试放大→更深饱和（死亡螺旋）；多层级联重试相乘（3 层各 3 次=后端 64 次）（[Cascading Failures](https://sre.google/sre-book/addressing-cascading-failures/)） | 限重试层（只在一层重试）、重试预算与随机指数退避、过载返回可区分状态、入口断路器先行（见[请求路由与流控](routing-and-flow-control.md)）；恢复期把流量降到远低于原崩溃点再缓升 |
| 状态残留（进程死后资源/状态未清） | GPU 显存残留（`nvidia-smi`/`amd-smi`/`npu-smi` 对账）、僵尸进程、存储上的临时 KV/offload 数据 | 摘除→清理→核对设备内存账目再准入（核对项见各平台 OOM 指南）；K8s 强制删除（`--force --grace-period=0`）后 Pod 可能仍在节点运行（[Pod 生命周期](https://v1-32.docs.kubernetes.io/docs/concepts/workloads/pods/pod-lifecycle/)），必须到节点核对进程/显存 |

## 语义边界：不承诺 exactly-once

- **已输出 token**：流式响应已发出的 token 不可撤回；重试/故障转移生成的是**新**响应，不能续传。客户端侧的幂等与去重（请求 ID 关联，见[请求路由与流控](routing-and-flow-control.md)）是唯一防线。
- **会话与 cache 身份**：KV/prefix cache 随进程消失，新副本为冷 cache；会话亲和的哈希环在副本集合变化时部分会话重落（机制见[请求路由与流控](routing-and-flow-control.md)）。跨副本恢复 cache 只有 PD connector/offload 一类显式传输路径（[PD 分离](pd-disaggregation.md)），常规副本故障**不继承**缓存。
- **外部副作用**：推理本身通常无副作用，但工具调用/检索增强类请求可能触发外部动作——这类请求的重试语义按具体上层协议定义，本库样板不含对应实现，不外推。
- **恢复 ≠ 正确**：服务恢复 200/ready 后，仍需质量抽查与错误率稳定窗确认（验证方法见下）。

## 验证设计：基线→受控切换/故障→恢复

每轮固定：负载形态与输入集、版本身份（新旧制品清单）、路由/入口配置、观测采集（错误/重复/遗漏/延迟/质量）。步骤与核对项：

1. **基线窗口**：稳定负载下记录 SLO 分位、goodput、错误分类、质量比对基准（固定输入集，方法见[输出质量对照评估](output-quality-evaluation.md)）。
2. **受控事件**（二选一或分别做）：a) 版本切换——按上文灰度流程执行到晋升，核对流量切换期间错误/重复（同请求 ID 多响应）/遗漏（发 N 收 M）；b) 故障注入——对单副本触发终止（正常删除）或 kill（异常死亡），观察摘除时延（请求错误开始→恢复）、路由收敛、在途请求终态（ABORT/错误/正常完成）。
3. **恢复核对**：新副本 ready 时间（冷启动全程）、KV/cache 冷热状态（TTFT 对比）、设备资源对账（无残留进程/显存）、错误率回到基线的稳定窗口长度、质量比对回到容差内。
4. **回退演练**：从新版本按预注册条件回退，核对回退耗时（含冷启动）与流量钉回的正确性。
5. **停止条件**：出现未预期的错误形态（如重复响应、串话——请求状态串扰的证据）立即停止，保留全量日志时间线再分析；排障方法沿用[有效排障](https://sre.google/sre-book/effective-troubleshooting/)的证据链纪律。

平台操作（K8s 滚动更新参数、KServe 字段、Envoy 配置）按各自版本另行记录适用环境；演练须在隔离环境获得授权后执行，本文流程不构成执行授权。

## 边界与未知

- KServe 金丝雀控制器实现与 Gateway 实现的权重生效时延未核；Knative 修订模型仅 serverless 模式。
- vLLM 优雅关闭对在途流式请求的排空行为未在上游文档化（不假设自动排空）；`uvicorn` 关闭序列与 engine shutdown 的先后未逐行核。
- K8s 探针机制的具体默认值（periodSeconds 等）在本批来源页未列，本文未引用数值。
- 故障注入仅给出设计；未执行任何演练，全部处置分支为样板证据＋方法组合，非实测结论。

## 来源与验证记录

- [Kubernetes v1.32 Pod 生命周期](https://v1-32.docs.kubernetes.io/docs/concepts/workloads/pods/pod-lifecycle/)（终止时序原文核对）与[探针概念页](https://v1-32.docs.kubernetes.io/docs/concepts/configuration/liveness-readiness-startup-probes/)。
- [KServe Canary Rollout（InferenceService 与 LLMInferenceService）](https://kserve.github.io/website/docs/model-serving/predictive-inference/rollout-strategies/canary)（网站仓 pin 3f4067e）：canaryTrafficPercent、group/weight 权重路由、weight:0 风险、stop 注解晋升、回退语义。
- [vLLM v0.14.0 固定快照](https://github.com/vllm-project/vllm/tree/b17039bccc17b94a2ea107272ad7bc93508708df)：SIGTERM/lifespan 关闭链、EngineDead 传播、请求取消与资源释放。
- [Envoy overload manager / outlier detection](https://www.envoyproxy.io/docs/envoy/latest/intro/arch_overview/operations/overload_manager)（1.41.0-dev 线）：排空动作、离群摘除与主动健康检查交互。
- [SRE Book 第 22 章](https://sre.google/sre-book/addressing-cascading-failures/)、[有效排障](https://sre.google/sre-book/effective-troubleshooting/)：级联失效与重试纪律、排障证据链。
- 逐条主张与证据定位见[第二十八批 T07-10 来源记录](../../docs/research/batch-28-t07-10-sources.md)。
- 当前验证范围：来源核对；未执行发布或故障注入演练。
