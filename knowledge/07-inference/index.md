---
id: inference.index
title: 07 推理与服务系统
type: index
domain: inference
status: draft
platforms:
- generic
source_refs:
- src.ascend.vllm-ascend
- src.ascend.agent-skills
- src.stas.ml-engineering
updated_at: '2026-10-21'
summary: 组织模型推理执行、服务流量、性能指标和故障恢复；含八主题五方面入口表与缓存/SLO 边界交付核对。
related_ids:
- software-stack.index
- communication.index
- data-storage.index
- cluster-platform.index
- reliability.index
- inference.execution-and-kv-cache
- inference.model-loading-and-readiness
- inference.engine-backend-boundaries
- inference.mindie-execution-profile
- inference.latency-metrics
- inference.ascend-inference-tail-latency-triage
- inference.ascend-inference-tail-latency-source-case
- inference.ascend-inference-tail-latency-experiment
- inference.ascend-inference-oom-triage
- inference.quantization-and-quality
- inference.output-quality-evaluation
- inference.distributed-inference-layouts
- inference.pd-disaggregation
- inference.routing-and-flow-control
- inference.capacity-and-autoscaling
- inference.release-and-recovery
- inference.gpu-inference-oom-triage
---

# 07 推理与服务系统

本页是内容导航草稿。所列正文的编辑审阅已在各自批次闭环（记录见交付核对小节），但仍为 draft、未经本地环境实测；当前处于 T07-12 导航核对阶段。`generic` 表示跨平台导航，不表示所有环境兼容。

## 已有正文

- [推理执行与 KV cache](execution-and-kv-cache.md)。
- [权重加载、引擎 ready 与启动失败诊断](model-loading-and-readiness.md)：启动五阶段边界、load-format 分派与格式不可互推、模型身份固定清单、health 与 ready 的区别、三平台小模型验证计划。
- [推理引擎组件与平台功能交集档案](engine-backend-boundaries.md)：vLLM 上游/vLLM Ascend/MindIE 组件分层对照、调度与 KV 语义不互推、NVIDIA/AMD/Ascend 三份特性交集档案（支持/条件/未证实/冲突）与升级替换重核验检查表。
- [MindIE 推理执行与配置样板](mindie-execution-profile.md)：MindIE LLM 3.1.0 文档线的四层执行架构、config.json 逐段语义（Server/Model/Schedule/HealthCheck）、PD 混部/分离、日志与三态健康检查、首失败边界与 Qwen 可追溯样板。
- [推理延迟与吞吐指标字典](latency-metrics.md)。
- [推理量化与输出质量验证](quantization-and-quality.md)：量化机制（scale/粒度/校准）、格式–kernel–运行 dtype–accumulation 四层分立、优化开关≠命中、三平台支持矩阵与冲突保留、质量验证与三层归因。
- [推理输出质量的对照评估方法与案例](output-quality-evaluation.md)：输入身份固定清单、采样变化与计算差异三层归因（greedy/matmul 累加顺序/组 batch）、四层指标与预注册纪律、基线→单变量→恢复 schema、四份官方评估指南与论文证据归属。
- [分布式推理布局与并行选择](distributed-inference-layouts.md)：DP/TP/PP/EP/SP/CP 的权重与 KV 所有权、KV 复制与 dcp、选型表、三平台布局限制与跨页冲突、跨机初始化与失败的可观察证据。
- [Prefill/Decode 分离（PD 分离）与流量分配](pd-disaggregation.md)：动机与"不提升吞吐"的反面声明、vLLM connector 形态与外部代理职责、昇腾侧支持矩阵与限制。
- [请求路由、准入与流控](routing-and-flow-control.md)：入口路由/引擎调度/P/D 分配/健康发现四层职责、五种路由算法与代理层均衡的比较、预算与背压分层、请求 ID/断连取消/流式重试边界、负载对照方案。
- [容量、扩缩容与冷启动决策](capacity-and-autoscaling.md)：单副本与集群容量口径、四类触发器比较（利用率/请求率/队列/推理特有指标）、冷启动构成与 scale-to-zero 条件、缩容 drain 与 PD 双池联动、增压/阶跃/收缩对照。
- [服务版本发布、副本故障与恢复验证](release-and-recovery.md)：liveness/readiness/推理质量三层分开、版本制品身份清单、灰度发布五步（预热/递增/gate/drain/回退条件）、副本与 PD 单侧故障处置分支、exactly-once 语义边界、基线→切换→恢复验证设计。
- [GPU 推理 OOM 与状态恢复诊断](gpu-inference-oom-triage.md)：NVIDIA/AMD 按首失败阶段定位、四类错误含义区分（CUDA OOM/容量 ValueError/EngineDead/请求错误）、CUDA 与 ROCm 取证字段差异、单因素验证与状态恢复核对。

## 本章范围

覆盖一次推理请求从接收、排队、模型执行到响应的路径，以及引擎、缓存、分布式部署和服务恢复。关联工作负载特征与资源使用。

## 八主题五方面入口表

每个主题的原理与边界、设计与使用、观测与判断、故障与处置、验证与案例分别指向正文入口；同一篇可承担多个方面，链接指向正文而非目录标题。各入口的平台版本、未实测状态与未知条件以所链正文为准；vLLM 上游结论、vLLM Ascend 限制、MindIE 与 ROCm/AMD 档案各自绑定自己的来源身份——vLLM v0.14.0 与 vLLM Ascend v0.14.0rc1 为固定 commit 快照，MindIE 3.1.0 为固定仓内文档线（latest 支持表等动态页未定版），ROCm/AMD 为版本化文档或按页＋读取日期记录的页面——不互推、不给 `generic` 条目加兼容承诺。

| 主题 | 原理与边界 | 设计与使用 | 观测与判断 | 故障与处置 | 验证与案例 |
|---|---|---|---|---|---|
| **07.1 模型加载、prefill、decode 与执行路径** | [从输入到连续输出与 batch 调度原理](execution-and-kv-cache.md)；[启动序列与阶段边界](model-loading-and-readiness.md) | [权重格式与分片](model-loading-and-readiness.md)、load-format 分派与格式不可互推 | [建立可解释执行记录](execution-and-kv-cache.md)；[模型身份固定清单](model-loading-and-readiness.md) | [首失败边界分类](model-loading-and-readiness.md)（启动五阶段） | [小模型验证计划（三平台样板）](model-loading-and-readiness.md)，未执行 |
| **07.2 推理引擎及平台后端** | [组件对照](engine-backend-boundaries.md)（vLLM 上游/Ascend/MindIE 分层） | [MindIE 执行架构与 config.json 语义](mindie-execution-profile.md)；[平台能力交集档案](engine-backend-boundaries.md)（三平台支持/条件/未证实/冲突） | [MindIE 日志、指标与三态健康检查](mindie-execution-profile.md)；[调度与 KV 策略语义对照](engine-backend-boundaries.md)（参数不同名不直译） | [MindIE 首失败边界](mindie-execution-profile.md)；[引擎升级或替换的重核验检查表](engine-backend-boundaries.md) | [MindIE 最小验证设计与 Qwen 可追溯样板](mindie-execution-profile.md)；[与 vLLM 的有证据对照（有限项）](mindie-execution-profile.md) |
| **07.3 Batch、KV cache、内存与缓存管理** | [KV cache 保存什么，容量由什么决定](execution-and-kv-cache.md)（活动 KV、prefix block、权重加载是不同对象） | [容量不足、抢占重算与驱逐不是同一件事](execution-and-kv-cache.md)；[prefix cache 的复用边界](execution-and-kv-cache.md)（hash 身份与引用/驱逐） | [batch 是每次迭代的调度结果](execution-and-kv-cache.md)；[chunked prefill 的收益与代价要按指标拆开](execution-and-kv-cache.md) | KV 容量类故障分支见[两篇 OOM 诊断](gpu-inference-oom-triage.md)（[昇腾侧](ascend-inference-oom-triage.md)） | [昇腾长尾实验设计的对照方法](ascend-inference-tail-latency-experiment.md)（B0/V1/R0、冷热缓存准备与事件关联，未执行，可复用于缓存/调度对照）；[Ascend 样板只能证明自身固定范围](execution-and-kv-cache.md)；容量实测基线待补（原文已注明） |
| **07.4 量化、算子优化与输出质量验证** | [机制：scale、zero point、粒度与校准](quantization-and-quality.md) | [格式、kernel、运行 dtype 三层事实与累加精度缺口](quantization-and-quality.md)；[支持矩阵：三平台分别核](quantization-and-quality.md) | [优化开关 ≠ 实际命中](quantization-and-quality.md) | [量化相关故障的三层归因与回退](quantization-and-quality.md) | [输出质量如何验证](quantization-and-quality.md)；[对照评估方法与案例](output-quality-evaluation.md)（输入身份、预注册、基线→单变量→恢复 schema） |
| **07.5 分布式推理、PD 分离与通信依赖** | [各并行方式的所有者与同步语义](distributed-inference-layouts.md)；[PD 动机与官方反面声明](pd-disaggregation.md) | [选型表：按约束选布局](distributed-inference-layouts.md)；[按 connector 分列的兼容前提](pd-disaggregation.md) | [跨机初始化、mapping 与失败的可观察证据](distributed-inference-layouts.md)；[指标：阶段归属与实现明细](pd-disaggregation.md) | [失败链、取消与清理](pd-disaggregation.md)；[副本与 PD 单侧故障处置](release-and-recovery.md) | [单副本失败的最小证据/验证设计与三项最小验证（correctness/throughput/latency，未执行）](distributed-inference-layouts.md)；[PD 评估建议与昇腾侧/MindIE 对照](pd-disaggregation.md)；[三平台布局限制与跨页冲突](distributed-inference-layouts.md)留作支持边界 |
| **07.6 路由、流控、扩缩容与版本发布** | [四层职责与请求状态边界](routing-and-flow-control.md) | [路由算法比较](routing-and-flow-control.md)；[触发器比较与冷启动/scale-to-zero 条件](capacity-and-autoscaling.md)；[灰度发布五步与回退条件](release-and-recovery.md) | [预算、deadline、优先级与背压](routing-and-flow-control.md)；[单副本与集群容量口径](capacity-and-autoscaling.md) | [副本与引擎故障：证据与处置分支](release-and-recovery.md)；[缩容 drain 与 PD 双池联动](capacity-and-autoscaling.md) | [有限对照方案（负载阶跃/突发/长短混合）](routing-and-flow-control.md)与[基线→切换→恢复验证设计](release-and-recovery.md)，均未执行 |
| **07.7 TTFT、TPOT、吞吐、长尾与服务 SLO** | [指标口径表](latency-metrics.md)：TTFT/TPOT/ITL/E2E/throughput/goodput 的定义与分母边界 | [goodput：满足哪些 SLO 的请求](latency-metrics.md)；[warmup、ready check 与 cache 状态](latency-metrics.md) | [客户端和服务端看到的时间线](latency-metrics.md)；[percentile 与 aggregation](latency-metrics.md)（实例分位不取平均） | [昇腾推理长尾诊断](ascend-inference-tail-latency-triage.md) | [最小实验记录模板](latency-metrics.md)；[昇腾长尾来源案例](ascend-inference-tail-latency-source-case.md)与[实验设计](ascend-inference-tail-latency-experiment.md)（未执行） |
| **07.8 OOM、请求失败、副本故障与服务恢复** | [三层"健康"与版本制品身份](release-and-recovery.md)（liveness/readiness/推理质量分开） | [语义边界：不承诺 exactly-once](release-and-recovery.md)；[请求身份、幂等与重试边界](routing-and-flow-control.md) | [NVIDIA 与 AMD 的取证差异](gpu-inference-oom-triage.md)（CUDA/ROCm 字段）；[昇腾公开报告形态（未闭环，不归因）](ascend-inference-oom-triage.md) | [GPU 推理 OOM 按首失败阶段定位](gpu-inference-oom-triage.md)；[昇腾推理 OOM 诊断](ascend-inference-oom-triage.md) | [GPU 指南的单因素验证、退出/清理/再启动与接流恢复门](gpu-inference-oom-triage.md)与[昇腾指南的停止/回滚安排及诊断结束判据](ascend-inference-oom-triage.md)（各自按指南现状，均未执行）；服务层[基线→切换→恢复验证设计](release-and-recovery.md) |

## 场景指南、案例与实验

以下均为来源整理草稿；公开案例不代表本库复现，实验仅为设计。

| 主题 | 诊断指南 | 来源案例 | 实验设计 |
|---|---|---|---|
| 昇腾推理长尾 | [指南](ascend-inference-tail-latency-triage.md) | [案例](ascend-inference-tail-latency-source-case.md) | [实验设计](ascend-inference-tail-latency-experiment.md) |
| 昇腾推理 OOM | [指南](ascend-inference-oom-triage.md) | 待补充（指南内含两条未闭环公开报告形态） | 待补充 |
| GPU 推理 OOM（NVIDIA/AMD） | [指南](gpu-inference-oom-triage.md) | 待补充 | 待补充 |

## 交付核对与保留边界（T07-12，2026-10-21）

对照原目录八主题逐项核对五方面入口，并复核原 covered 主题 07.3/07.7 的缓存/SLO 边界。核对只针对已交付正文的覆盖结构，不改变任何正文的编辑/验证状态。

- **07.3（原 covered 复核·缓存身份与 batch 生命周期）**：[KV cache 保存什么](execution-and-kv-cache.md)明确活动请求 KV、请求结束后可复用的 prefix block、外部 KV load 与权重加载是不同对象；[batch 是每次迭代的调度结果](execution-and-kv-cache.md)说明 batch 组成逐迭代变化，不能当静态 batch size 解读；[调度与 KV 语义对照](engine-backend-boundaries.md)保留"参数不同名不直译"。容量实测基线仍缺，正文已注明。
- **07.7（原 covered 复核·统计分母与 SLO 边界）**：[指标字典](latency-metrics.md)逐项固定分子/分母/窗口（throughput 先说清分子和窗口、goodput 列出全部 SLO 条件、成功/失败/取消分开报告）；[percentile 与 aggregation](latency-metrics.md) 明确实例 p99 不能取平均得整体 p99。SLO 数值阈值不由本库给出，实测基线待补。
- **平台分立**：vLLM v0.14.0（上游）与 vLLM Ascend v0.14.0rc1 为固定 commit 快照；MindIE LLM 3.1.0 只采信固定仓内文档线，latest 支持/快速入门页与源码/产品包的同版关系仍未定版（见[引擎组件档案](engine-backend-boundaries.md)）；ROCm/AMD 为版本化文档（docs-10.1.0 等）或按页＋读取日期记录。引擎/模型/硬件/功能交集按版本核查，`generic` 行不构成兼容承诺，AMD/ROCm 条目不给 vLLM 上游或 Ascend 加推断。
- **来源核对与真实负载验证分开**：本章全部正文为 draft；来源核对指对照固定 commit/版本化文档或按页＋读取日期记录的动态页面（如 MindIE latest 支持表、Prometheus/Envoy latest），不代表真实负载验证。七份既有验证方案（V01–V07，含昇腾推理长尾 V07）实际执行 0/7，状态由[验证清单](../../plans/validation-backlog.yaml)管理，本页不改写；昇腾长尾实验设计与本页全部"验证设计"均未执行。
- **各任务审阅闭环定位**：T07-01（[来源](../../docs/research/batch-26-t07-01-sources.md)·[最终复核](../../docs/research/batch-26-t07-01-codex-recheck-2.md)）、T07-02（[来源](../../docs/research/batch-26-t07-02-sources.md)·[最终复核](../../docs/research/batch-26-t07-02-codex-recheck-5.md)）、T07-03（[来源](../../docs/research/batch-26-t07-03-sources.md)·[最终复核](../../docs/research/batch-26-t07-03-codex-recheck-3.md)）、T07-04（[来源](../../docs/research/batch-27-t07-04-sources.md)·[最终复核](../../docs/research/batch-27-t07-04-codex-recheck-3.md)）、T07-05（[来源](../../docs/research/batch-27-t07-05-sources.md)·[最终复核](../../docs/research/batch-27-t07-05-codex-recheck-3.md)）、T07-06（[来源](../../docs/research/batch-27-t07-06-sources.md)·[最终复核](../../docs/research/batch-27-t07-06-codex-recheck-4.md)）、T07-07（[来源](../../docs/research/batch-27-t07-07-sources.md)·[最终复核](../../docs/research/batch-27-t07-07-codex-recheck-3.md)）、T07-08（[来源](../../docs/research/batch-28-t07-08-sources.md)·[最终复核](../../docs/research/batch-28-t07-08-codex-recheck-3.md)）、T07-09（[来源](../../docs/research/batch-28-t07-09-sources.md)·[最终复核](../../docs/research/batch-28-t07-09-codex-recheck-3.md)）、T07-10（[来源](../../docs/research/batch-28-t07-10-sources.md)·[最终复核](../../docs/research/batch-28-t07-10-codex-recheck-2.md)）、T07-11（[来源](../../docs/research/batch-28-t07-11-sources.md)·[最终复核](../../docs/research/batch-28-t07-11-codex-recheck-4.md)）。
- **账面同步（本批执行）**：执行清单（full-coverage-backlog）中 07.1-G1..G3、07.2-G1..G3、07.4-G1..G3、07.5-G1..G3、07.6-G1..G3、07.8-G1..G3 共 18 项内容缺口的状态此前未随 Batch 26/27/28 交付同步——盘点清单已记关闭、对应任务 done 且上述最终复核记录存在；本批（2026-10-21）按该关闭证据将 18 项同步为 closed。同步只改状态字段，不改变技术边界或验证状态。
- **跨领域依赖**：量化/算子语义引用 02、设备分配与调度引用 05、模型文件读取引用 04、分布式通信引用 03；本页只引不复制，主归属正文未移动。

## 内容边界

- 量化与算子执行的基础语义引用 02；本章维护具体引擎行为和输出质量验证。
- 设备分配和平台调度引用 05；流量路由、请求队列和服务容量策略归本章。
- 模型文件读取引用 04，分布式通信引用 03；本章解释它们对请求路径的影响。

## NPU 内容位置

vLLM Ascend、MindIE 等引擎与后端分别建立环境和能力入口。模型、dtype、执行模式、并行方式、请求形态与版本一起界定案例的适用范围。

完整路径见[昇腾专题](../../paths/platforms/ascend.md)。其他平台入口见 [NVIDIA 专题](../../paths/platforms/nvidia.md)。

## 关联章节

- [02 系统软件与加速器执行栈](../02-software-stack/index.md)
- [03 互联网络与分布式通信](../03-communication/index.md)
- [04 数据路径与存储系统](../04-data-storage/index.md)
- [05 集群平台与资源管理](../05-cluster-platform/index.md)
- [08 可靠性与计算正确性方法](../08-reliability/index.md)

## 已收集的原始资料入口

以下链接指向厂商或项目自己的资料；引用或改编前仍需核对对应版本、来源许可和适用范围。

- [vLLM Ascend 官方仓库](https://github.com/vllm-project/vllm-ascend)：NPU 推理部署、功能支持和问题资料入口。
- [Ascend Agent Skills](https://github.com/Ascend/agent-skills)：推理生态资料与 FAQ 整理流程的组织参考。
- [ML Engineering 项目仓库](https://github.com/stas00/ml-engineering)：推理工程和性能问题资料入口。

## 成果与后续

已有执行/KV、指标字典、昇腾长尾指南/案例/实验设计、OOM 诊断（昇腾＋GPU）、量化质量验证、PD 分离说明与路由/流控、扩缩容、发布恢复，以及引擎组件/MindIE/分布式布局档案；八主题五方面入口表与缓存/SLO 边界交付核对已随 T07-12 交付（2026-10-21）。后续维护方向：昇腾侧量化实测、容量与 SLO 实测基线、两篇 OOM 指南的来源案例与实验补齐，及全部真实环境验证（V 工作包）。
