---
id: inference.ascend-inference-tail-latency-experiment
title: 昇腾推理长尾验证实验设计
type: experiment
domain: inference
status: draft
platforms: [ascend]
source_refs:
  - src.vllm.inference-v0-14
  - src.ascend.vllm-ascend-v0-14-0rc1
updated_at: "2026-09-30"
summary: 固定负载和测量边界，以独立重复与单变量对照区分版本、缓存、排队和观测影响；尚未执行。
related_ids:
  - inference.ascend-inference-tail-latency-triage
  - inference.latency-metrics
  - inference.execution-and-kv-cache
applicability:
  environment_refs: []
  notes: 尚未选定完整可执行的 NPU 环境；须核对硬件、驱动、CANN、torch_npu、引擎/插件、模型与客户端配套。本设计首先用于单实例受控服务；P/D 需另补连接器与角色边界，不能直接套用。
verification:
  status: not_verified
  evidence_refs: []
  notes: 仅交付实验设计；无实际运行、负载生成、profiling 或性能结果。
---

# 昇腾推理长尾验证实验设计

## 问题与预先登记的判断

验证一个明确候选因素是否会在固定工作负载下稳定改变首输出/输出间隔/完成时间的分布，同时影响失败率或质量。例如比较两个已核实可部署的代码制品，或改变一个调度参数。一次实验只选择一种主要因素。

本设计不预设某机型应达到的 TTFT 或 tokens/s。执行前由业务目标和基线变异确定最小有意义差异、SLO、失败率与质量判据；没有这些定义时，只能形成探索性观察。

## 环境与输入

记录 NPU 型号数量/拓扑、CPU 与主机内存、驱动/固件、CANN 子包、torch/torch_npu、vLLM/插件 commit 和本地补丁、镜像摘要、模型与 tokenizer revision、量化/图模式/并行度，以及客户端实现与代理链。

请求集采用固定且可管理的输入，保存输入/输出长度分布、前缀重复率、采样参数、到达时间表、并发限制、timeout 和重试政策。同一 seed 不保证跨版本生成内容和长度一致；实际输出长度、完成原因与质量仍需记录。

固定 vLLM benchmark 的到达速率与 `max_concurrency` 是不同约束，实际发起速率可低于配置值（[serve.py 1202–1213](https://github.com/vllm-project/vllm/blob/b17039bccc17b94a2ea107272ad7bc93508708df/vllm/benchmarks/serve.py#L1202-L1213)、[1271–1291](https://github.com/vllm-project/vllm/blob/b17039bccc17b94a2ea107272ad7bc93508708df/vllm/benchmarks/serve.py#L1271-L1291)）。所选客户端必须同样保存实际请求发起序列，不能只记一个“并发数”。

## 基线、对照与重复

| 组 | 改变的因素 | 目的 |
|---|---|---|
| B0 | 无；固定已核实的完整环境 | 测得基线变异、失败与质量，确认观测可对应请求 |
| V1 | 仅预先选定的代码制品或参数 | 检验候选因素；若更换制品连带依赖变化，则只能归因于整个变更集 |
| R0 | 恢复 B0 的配置和缓存准备方式 | 识别节点漂移、缓存残留与不可逆状态变化 |
| O1（按需独立开展） | 仅启用所需观测工具 | 量化 profiling/trace 的测量扰动，不混入 B0/V1 的性能结果 |

重复次数、每次请求数和稳态窗口在运行前声明；至少安排多次独立运行，并按资源条件交错或随机排列 B0/V1，避免顺序与温度/缓存变化混杂。次数不足以稳定估计 p99 时直接报告样本与不确定性，不用平滑曲线掩盖不足。

冷缓存与预热后的请求是两个分层。每组采用相同且有记录的缓存准备办法；不能在在线共享服务随意清缓存。prefix cache 的身份与 token/模型条件有关，单纯“输入文本相似”不等于命中（[prefix_caching.md 5–26](https://github.com/vllm-project/vllm/blob/b17039bccc17b94a2ea107272ad7bc93508708df/docs/design/prefix_caching.md#L5-L26)）。

## 执行步骤与资源影响

1. 在已授权且容量隔离的 NPU 服务环境核对制品、输入、资源预算、恢复方式和成功/失败定义。两组环境不能共享未计入的竞争负载。
2. 按同一预热办法准备 B0，运行预先声明的请求计划；记录服务、客户端与监控的时钟类型和采样频率。
3. 逐次进行 B0/V1/R0，保存每次配置差异、实际发起序列、逐请求结果与统计窗口；除所选因素外发现其他漂移就将该次标为不可比。
4. 汇总失败/超时/取消及重试；延迟按相同输入/输出长度层和结果分类报告。成功样本分位数不代表失败请求已满足延迟目标。
5. 对齐等待、KV、抢占和阶段证据，保留无法映射的部分。需要重观测时另做 O1，不用其时长直接替代 B0/V1。
6. 撤销临时配置，结束测试客户端/服务进程，核查占用和设备状态，并按 R0 验证基线恢复。未恢复前保持环境隔离。

运行会占用 NPU/HBM、CPU/内存、网络与日志空间，并可能触发队列、拒绝或超时。预先限定设备、请求总量、最长时长、日志预算和停止条件；本设计不包含共享集群故障注入或驱动/固件变更。

## 测量口径与通过标准

客户端与服务端各自记录起止事件，不将跨时钟原始时间戳直接相减。固定 vLLM 的吞吐窗口包含主请求创建、到达等待和完成等待，但显式预热在窗口外（[serve.py 617–712](https://github.com/vllm-project/vllm/blob/b17039bccc17b94a2ea107272ad7bc93508708df/vllm/benchmarks/serve.py#L617-L712)、[763–845](https://github.com/vllm-project/vllm/blob/b17039bccc17b94a2ea107272ad7bc93508708df/vllm/benchmarks/serve.py#L763-L845)）；现场实现须重新确认。

| 结果类别 | 判据 |
|---|---|
| 候选因素得到支持 | 同负载下多次对照达到预设差异标准，R0 恢复，已记录的阶段证据与方向一致；仍只能支持本次变更范围 |
| 未支持候选因素 | 测量有足够分辨能力且差异未达到预设标准；不等于其他负载/版本永远无影响 |
| 质量或可靠性不通过 | 即使延迟改善，错误率、输出质量或资源边界不满足预设目标，也不能作为可接受优化 |
| 无法判断 | 基线失败、请求/制品漂移、样本不足、失败过滤未知、缓存不一致或恢复失败 |

出现计算正确性异常、设备严重错误、失控失败或资源预算超限时提前停止并保留证据。不能为得到“通过”而在事后删去失败、改窗口或调整 SLO。

## 实际结果与局限

**尚未执行，无测量结果。** 实验成功执行也不会自动覆盖其他模型、量化、机型、图模式、并行度或 MindIE。上游与插件的功能/版本声明另见[执行与 KV cache](execution-and-kv-cache.md)；它们不是本设计的现场兼容证明。
