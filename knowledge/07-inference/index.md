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
updated_at: '2026-10-08'
summary: 组织模型推理执行、服务流量、性能指标和故障恢复。
related_ids:
- software-stack.index
- communication.index
- data-storage.index
- cluster-platform.index
- reliability.index
- inference.execution-and-kv-cache
- inference.latency-metrics
- inference.ascend-inference-tail-latency-triage
- inference.ascend-inference-tail-latency-source-case
- inference.ascend-inference-tail-latency-experiment
- inference.ascend-inference-oom-triage
- inference.quantization-and-quality
- inference.pd-disaggregation
---

# 07 推理与服务系统

本页是内容导航草稿。下方已有基础正文，其余主题继续建设；新正文正在轮末审阅，未经本地环境实测。`generic` 表示跨平台导航，不表示所有环境兼容。

## 已有正文

- [推理执行与 KV cache](execution-and-kv-cache.md)。
- [推理延迟与吞吐指标字典](latency-metrics.md)。
- [推理量化与输出质量验证](quantization-and-quality.md)：支持矩阵读法、质量验证证据与量化故障三层归因。
- [Prefill/Decode 分离（PD 分离）与流量分配](pd-disaggregation.md)：动机与"不提升吞吐"的反面声明、vLLM connector 形态与外部代理职责、昇腾侧支持矩阵与限制。

## 本章范围

覆盖一次推理请求从接收、排队、模型执行到响应的路径，以及引擎、缓存、分布式部署和服务恢复。关联工作负载特征与资源使用。

## 场景指南、案例与实验

以下均为来源整理草稿；公开案例不代表本库复现，实验仅为设计。

| 主题 | 诊断指南 | 来源案例 | 实验设计 |
|---|---|---|---|
| 昇腾推理长尾 | [指南](ascend-inference-tail-latency-triage.md) | [案例](ascend-inference-tail-latency-source-case.md) | [实验设计](ascend-inference-tail-latency-experiment.md) |
| 昇腾推理 OOM | [指南](ascend-inference-oom-triage.md) | 待补充（指南内含两条未闭环公开报告形态） | 待补充 |


## 二级主题地图

- **07.1 模型加载、prefill、decode 与执行路径** — 已有[prefill/decode 基础草稿](execution-and-kv-cache.md)，模型加载专题待补。
- **07.2 推理引擎及平台后端** — 已有[vLLM 与 vLLM Ascend 固定样板边界](execution-and-kv-cache.md)，其他引擎待补。
- **07.3 Batch、KV cache、内存与缓存管理** — 已有[KV cache、前缀复用与抢占说明](execution-and-kv-cache.md)，具体容量验证待补。
- **07.4 量化、算子优化与输出质量验证** — 已有[推理量化与输出质量验证](quantization-and-quality.md)；各量化方法的细节约束与实测待补。
- **07.5 分布式推理、PD 分离与通信依赖** — 已有[PD 分离与流量分配](pd-disaggregation.md)（vLLM v0.14.0 与 vLLM Ascend v0.14.0rc1 固定样板）；扩缩容与生产级路由待补。
- **07.6 路由、流控、扩缩容与版本发布** — 待建设。
- **07.7 TTFT、TPOT、吞吐、长尾与服务 SLO** — 已有[延迟与吞吐指标字典](latency-metrics.md)，已有[昇腾长尾诊断](ascend-inference-tail-latency-triage.md)、公开案例和负载实验设计；实测基线待补。
- **07.8 OOM、请求失败、副本故障与服务恢复** — 已有[昇腾推理 OOM 诊断指南](ascend-inference-oom-triage.md)（按启动/图编译/prefill/decode/并发分阶段）；请求失败与副本恢复专题待补。

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

已有执行/KV、指标字典、昇腾长尾指南/案例/实验设计、OOM 诊断、量化质量验证与 PD 分离说明；后续补服务发布与恢复，并积累负载实测。
