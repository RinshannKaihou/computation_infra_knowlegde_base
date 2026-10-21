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
updated_at: '2026-10-20'
summary: 组织模型推理执行、服务流量、性能指标和故障恢复。
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

本页是内容导航草稿。下方已有基础正文，其余主题继续建设；新正文正在轮末审阅，未经本地环境实测。`generic` 表示跨平台导航，不表示所有环境兼容。

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

## 场景指南、案例与实验

以下均为来源整理草稿；公开案例不代表本库复现，实验仅为设计。

| 主题 | 诊断指南 | 来源案例 | 实验设计 |
|---|---|---|---|
| 昇腾推理长尾 | [指南](ascend-inference-tail-latency-triage.md) | [案例](ascend-inference-tail-latency-source-case.md) | [实验设计](ascend-inference-tail-latency-experiment.md) |
| 昇腾推理 OOM | [指南](ascend-inference-oom-triage.md) | 待补充（指南内含两条未闭环公开报告形态） | 待补充 |
| GPU 推理 OOM（NVIDIA/AMD） | [指南](gpu-inference-oom-triage.md) | 待补充 | 待补充 |


## 二级主题地图

- **07.1 模型加载、prefill、decode 与执行路径** — 已有[prefill/decode 基础草稿](execution-and-kv-cache.md)与[权重加载、ready 与启动失败诊断](model-loading-and-readiness.md)（vLLM v0.14.0 固定 commit＋MindIE 文档快照）。
- **07.2 推理引擎及平台后端** — 已有[vLLM 与 vLLM Ascend 固定样板边界](execution-and-kv-cache.md)与[引擎组件与平台功能交集档案](engine-backend-boundaries.md)（三线组件对照＋三平台特性矩阵）。
- **07.3 Batch、KV cache、内存与缓存管理** — 已有[KV cache、前缀复用与抢占说明](execution-and-kv-cache.md)与[引擎组件档案](engine-backend-boundaries.md)的调度/KV 语义对照；具体容量验证待补。
- **07.4 量化、算子优化与输出质量验证** — 已有[推理量化与输出质量验证](quantization-and-quality.md)（机制、格式–kernel–dtype 分层、三平台矩阵与冲突保留）与[输出质量对照评估方法与案例](output-quality-evaluation.md)（输入身份、差异分层、预注册与对照 schema、官方评估例）；昇腾侧量化实测待补。
- **07.5 分布式推理、PD 分离与通信依赖** — 已有[分布式推理布局与并行选择](distributed-inference-layouts.md)（DP/TP/PP/EP/SP/CP 所有权与三平台限制）与[PD 分离与流量分配](pd-disaggregation.md)（connector 前提、KV 传输与失败链、指标实现、三线对照）；PD 流量分配与服务控制联动见 07.6 各篇。
- **07.6 路由、流控、扩缩容与版本发布** — 已有[请求路由、准入与流控](routing-and-flow-control.md)、[容量、扩缩容与冷启动决策](capacity-and-autoscaling.md)与[服务版本发布、副本故障与恢复验证](release-and-recovery.md)（vLLM v0.14.0＋Envoy/K8s v1.32/KServe/production-stack 固定样板）。
- **07.7 TTFT、TPOT、吞吐、长尾与服务 SLO** — 已有[延迟与吞吐指标字典](latency-metrics.md)，已有[昇腾长尾诊断](ascend-inference-tail-latency-triage.md)、公开案例和负载实验设计；扩缩容/SLO 联动见[容量与扩缩容](capacity-and-autoscaling.md)；实测基线待补。
- **07.8 OOM、请求失败、副本故障与服务恢复** — 已有[昇腾推理 OOM 诊断指南](ascend-inference-oom-triage.md)与[GPU 推理 OOM 诊断](gpu-inference-oom-triage.md)（按启动/图编译/prefill/decode/并发分阶段）；请求失败、副本与服务恢复见[服务发布与恢复](release-and-recovery.md)。

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

## 首轮成果与后续

已有执行/KV、指标字典、昇腾长尾指南/案例/实验设计、OOM 诊断（昇腾＋GPU）、量化质量验证、PD 分离说明与路由/流控、扩缩容、发布恢复；后续积累负载实测并推进独立验证轨道。
