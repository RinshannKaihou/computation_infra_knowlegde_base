---
id: inference.ascend-inference-tail-latency-triage
title: 昇腾推理长尾诊断指南
type: procedure
domain: inference
status: draft
platforms: [ascend]
source_refs:
  - src.vllm.inference-v0-14
  - src.ascend.vllm-ascend-v0-14-0rc1
updated_at: "2026-09-30"
summary: 先固定请求与指标口径，再区分失败、负载、排队、执行、KV 和返回路径；给出证据分支而不预设调参结论。
related_ids:
  - inference.latency-metrics
  - inference.execution-and-kv-cache
  - reliability.evidence-and-hypotheses
applicability:
  environment_refs: []
  notes: 以 vLLM v0.14.0 的指标实现和 vLLM Ascend v0.14.0rc1 的功能声明分别作为阅读样板；两者未形成经验证的整栈环境。目标硬件、驱动、CANN、torch_npu、模型和客户端须另行核对。高级 P/D、nightly 和 MindIE 不继承样板参数。
verification:
  status: source_checked
  evidence_refs:
    - src.vllm.inference-v0-14
    - src.ascend.vllm-ascend-v0-14-0rc1
  notes: 已对照固定版本指标、benchmark、调度与功能文档组织诊断分支；流程未在 NPU 服务运行，未执行 benchmark 或 profiling。
---

# 昇腾推理长尾诊断指南

## 触发条件与范围

当业务侧 TTFT、输出间隔或完成时间的尾部恶化时进入本流程。目标是把异常缩小到可检验的阶段，并决定下一项检查。没有正常负载基线时，只能描述延迟分布，不能直接判为性能回归。

本文先处理已运行服务的证据。启动失败、设备不可访问、模型输出错误需分别调查；大量失败或超时也不能仅用“成功请求 p99”表示服务质量。

版本先核对：插件快照的 [conf.py](https://github.com/vllm-project/vllm-ascend/blob/52d4acfa51fb868823d1070b81cbd2d97e9e4696/docs/source/conf.py#L62-L80)使用 vLLM 0.14.1，本文指标样板为 0.14.0；这不是本库验证过的部署组合。功能矩阵里的 [Functional](https://github.com/vllm-project/vllm-ascend/blob/52d4acfa51fb868823d1070b81cbd2d97e9e4696/docs/source/user_guide/support_matrix/supported_features.md#L7-L33)也不保证任意模型、机型和图模式可用。进入现场前，把对应实现重新定位到实际制品。

## 最小证据包

| 证据 | 必需范围 | 缺失时的处理 |
|---|---|---|
| 环境身份 | NPU/服务器/拓扑；驱动、固件、CANN、torch_npu、vLLM、插件、镜像摘要、补丁；每个角色分别记录 | 版本未知先补齐，不把 pip 标签当作实际代码树 |
| 请求身份与结果 | 请求 ID、endpoint、流式模式、发起/首有效输出/结束事件、状态、错误、取消/重试关联 | 无法对齐时分别报告聚合，不拼接一条虚假 trace |
| 工作负载 | 模型/tokenizer revision、输入与输出 token 分布、到达过程、并发限制、采样、前缀复用、冷热状态 | 不同长度或缓存比例分层；不把总体均值当同负载比较 |
| 引擎与节点 | 对应窗口的运行/等待请求、KV、抢占、阶段统计；CPU、内存、设备和通信事件 | 标记采样频率与缺口，不从低利用率直接归因 |
| 测量工具 | 客户端版本、成功规则、token 计数、timeout、分位数方法、窗口、排除规则 | 未知口径不能直接与另一工具比较 |

实际请求文本和输出可以敏感；长期条目只保留受控证据的定位、统计及必要脱敏样例。

## 步骤与判断分支

### 1. 先核对失败与统计对象

并列报告发起、成功、失败、超时、取消和重试请求数。重试还需同时保留“业务请求”与“尝试”的对应关系。尾部延迟只基于成功样本时明确标注；不能给超时请求填一个看似精确的完成时间。

固定 vLLM benchmark 只用成功请求计算主要延迟/吞吐；TPOT 分布还排除输出不超过一个 token 的请求（[serve.py 404–445](https://github.com/vllm-project/vllm/blob/b17039bccc17b94a2ea107272ad7bc93508708df/vllm/benchmarks/serve.py#L404-L445)）。其他客户端必须查自己的规则。

### 2. 区分哪一个窗口变慢

先读[指标字典](latency-metrics.md)，不要按名称猜起止点。固定服务端 TTFT 从 engine request arrival 计到 frontend 接收首批相关输出后的统计时刻；客户端 TTFT 则从 POST 前计到合格流式 payload。两者差值不是纯网络时间。服务端阶段统计来自 engine-core 的 monotonic 事件，而 TTFT/E2E 使用 frontend wall-clock（[stats.py 252–305](https://github.com/vllm-project/vllm/blob/b17039bccc17b94a2ea107272ad7bc93508708df/vllm/v1/metrics/stats.py#L252-L305)、[331–377](https://github.com/vllm-project/vllm/blob/b17039bccc17b94a2ea107272ad7bc93508708df/vllm/v1/metrics/stats.py#L331-L377)）。

客户端变慢、服务端聚合稳定时，优先补请求关联与 frontend/proxy/client 证据；也可能是聚合样本不同，不能立即归因于网络。TPOT 平均值稳定时继续看 ITL/请求级分布，避免漏掉少数长停顿。

### 3. 按证据选择候选分支

下表是调查方法，不是源码保证的因果关系。先使用已有日志和指标；任何补充采样、调试或配置变更另行记录运行影响。

| 观察 | 候选解释 | 下一项能区分假设的检查 | 尚不能下的结论 |
|---|---|---|---|
| 输入/输出长度、并发或缓存比例变化 | 负载组成改变 | 在相同长度分层、到达过程与缓存条件下比较 | 版本回归 |
| 同负载下初始 queue 区间和等待请求上升 | 到达压力、可用容量、放置或调度限制 | 对齐实际发起速率、活动实例、每实例队列与执行进度 | 全部 TTFT 都是排队 |
| prefill 区间长、decode 仍有进展 | 分块调度、长输入、抢占或执行路径 | 对齐每轮 token 预算、首输出前的调度/抢占与 rank 事件 | 单个算子慢或 decode 无异常 |
| KV 使用与抢占同时上升 | 活动状态压力、前缀组成、重算 | 固定模型/长度/并发，关联请求生命周期与抢占记录 | 内存泄漏；提高内存比例必然有效 |
| 个别实例或 rank 停顿 | 进程、CPU、设备、通信或数据分支 | 找最早异常，保留其他 rank 的成功/失败时间线 | HCCL 或网卡已被证明为根因 |
| 服务端相关请求及时完成，客户端长停顿 | 返回、代理、客户端解析或测量问题 | 对齐输出事件和 chunk，确认时钟/请求匹配 | 服务端完全正常或差值全是网络 |
| P/D 服务首输出慢 | prefill、KV 传输、decode 接纳及连接器等待 | 依实际版本补角色与传输 trace，分别记录排队、搬运和消费 | 单实例调度指标可直接解释所有 P/D 等待 |

固定 vLLM V1 的 prefill/decode 区间可包含抢占；KV 不足时的默认重算会影响延迟，不能把 phase duration 当纯 kernel 时间（[optimization.md 10–48](https://github.com/vllm-project/vllm/blob/b17039bccc17b94a2ea107272ad7bc93508708df/docs/configuration/optimization.md#L10-L48)、[stats.py 331–377](https://github.com/vllm-project/vllm/blob/b17039bccc17b94a2ea107272ad7bc93508708df/vllm/v1/metrics/stats.py#L331-L377)）。这些机制在现场插件版本是否同样实现，仍须核对。

### 4. 用受控对照收窄，避免一次修改多项

已有证据不足时，先设计一次只改变一个因素的对照。先固定请求集合、随机性、到达过程、并发、缓存预热和版本，再选择版本、单个调度参数或单个角色配置作为变量。修改并行方式通常还会改变资源与通信，不能把结果叫作纯参数效应。

观测工具也作为变量记录：启用 profiling 的运行与无 profiler 运行分别报告。没有必要的 trace 和容量预算时不在在线服务临时加重观测；本页不提供未验证的一键调参或 profiling 命令。

## 停止与完成判据

出现计算错误、设备不可恢复错误、失败率持续扩大、证据无法对应同一实例/时点，或测试可能超出既定资源范围时停止性能对照，保留证据并处理相应故障。配置变更只能在已有执行授权与恢复安排覆盖的范围内进行；本轮仅编写文档。

一次诊断交付应包含：异常的精确定义、同口径基线、失败分类、版本与负载身份、最先异常阶段、支持与反对证据、剩余假设和下一项检查。性能恢复还需在相同负载下重复满足约定 SLO，同时检查结果质量与失败率。暂时未复现、单次 p99 下降或服务重启成功均不等于根因确认。

当前未完成实际 NPU 环境验证，也未提供型号通用的阈值。
