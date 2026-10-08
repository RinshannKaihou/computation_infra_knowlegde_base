---
id: inference.pd-disaggregation
title: Prefill/Decode 分离（PD 分离）与流量分配
type: concept
domain: inference
status: draft
platforms: [generic]
source_refs:
  - src.vllm.inference-v0-14
  - src.ascend.vllm-ascend-v0-14-0rc1
updated_at: "2026-10-08"
summary: PD 分离把 prefill 与 decode 放进不同实例、用 KV connector 传递 cache，换取 TTFT 与 ITL 的分别调优；vLLM 官方明示它不提升吞吐；流量分配是外部代理职责，昇腾侧支持范围只按插件自己的矩阵与限制核对。
related_ids:
  - inference.execution-and-kv-cache
  - inference.latency-metrics
  - inference.ascend-inference-tail-latency-triage
  - inference.quantization-and-quality
verification:
  status: source_checked
  evidence_refs:
    - src.vllm.inference-v0-14
    - src.ascend.vllm-ascend-v0-14-0rc1
  notes: "已核对 vLLM v0.14.0 的 disagg_prefill/nixl 文档、KVTransferConfig、connector 注册表与 toy 代理，以及 vLLM Ascend v0.14.0rc1 的功能矩阵、PD 特性指南与教程存在性；未部署或运行任何 PD 分离服务。"
---

# Prefill/Decode 分离（PD 分离）与流量分配

## 定义与要解决的问题

PD 分离（disaggregated prefill）把 prefill 与 decode 放进**不同的引擎实例**：prefill 实例产出 KV cache，经 connector 传给 decode 实例继续生成（[vLLM v0.14.0 disagg_prefill 文档 L50–54](https://github.com/vllm-project/vllm/blob/b17039bccc17b94a2ea107272ad7bc93508708df/docs/features/disagg_prefill.md#L50-L54)）。它帮助回答两类问题：TTFT 与 ITL 能否分别调优（P/D 可用不同的并行策略），以及长尾 ITL 是否与"decode 中插入 prefill"有关。

读本文前需要的背景：执行阶段与 KV cache 见[推理执行与 KV cache](execution-and-kv-cache.md)，TTFT/TPOT/ITL 的口径见[延迟与吞吐指标字典](latency-metrics.md)。`generic` 指问题框架通用；各引擎的支持状态必须按实现单独核对（见下）。

## 动机与官方反面声明

vLLM v0.14.0 文档给出的动机是 TTFT 与 ITL 的分别调优，以及控制尾部 ITL——不分离时 decode 批次中插入 prefill 会抬高尾延迟，chunked prefill 虽可缓解但 chunk size 难调（[disagg_prefill.md L10–13](https://github.com/vllm-project/vllm/blob/b17039bccc17b94a2ea107272ad7bc93508708df/docs/features/disagg_prefill.md#L10-L13)）。同一文档明示：**"Disaggregated prefill DOES NOT improve throughput"**（[L15–16](https://github.com/vllm-project/vllm/blob/b17039bccc17b94a2ea107272ad7bc93508708df/docs/features/disagg_prefill.md#L15-L16)），且该功能在此版本标为 experimental、可能变更（L1–6）。这限定了该版本的功能定位，不能据此承诺吞吐改善。

**本库的评估建议**：在固定请求负载、资源预算、模型与输出长度口径下，联合比较 TTFT/ITL 分布、总吞吐/goodput、失败率及 KV 传输成本。吞吐变化仍是评估项；只改善时延不单独证明同等成本下的服务能力提高。该建议属于本库的方法判断，没有本环境实测结果。

## vLLM v0.14.0 的实现形态

- **配置入口**：`KVTransferConfig`（[vllm/config/kv_transfer.py L13–70](https://github.com/vllm-project/vllm/blob/b17039bccc17b94a2ea107272ad7bc93508708df/vllm/config/kv_transfer.py#L13-L70)）：`kv_connector` 指定 connector 类；`kv_role` ∈ {`kv_producer`, `kv_consumer`, `kv_both`}（配置了 connector 时角色必填，否则 ValueError，L90–116）；`kv_load_failure_policy` 默认 `recompute`（KV 加载失败时重调度重算失败 block），可配 `fail`（以错误 finish reason 结束请求，L67–70）。
- **connector 清单以源码注册表为准**：[factory.py L146–203](https://github.com/vllm-project/vllm/blob/b17039bccc17b94a2ea107272ad7bc93508708df/vllm/distributed/kv_transfer/kv_connector/factory.py#L146-L203) 注册了 10 个 connector（Example、P2pNccl、LMCacheV1、LMCacheMP、Nixl、Multi、MoRIIO、Offloading、DecodeBench、Mooncake），其中没有 SharedStorageConnector。此前研究记录的全树名称检索也未命中；这不证明 Offloading/LMCache 与旧共享存储接口有替代或兼容关系。OffloadingConnector 的入口接入 `kv_offload`（[L24–65](https://github.com/vllm-project/vllm/blob/b17039bccc17b94a2ea107272ad7bc93508708df/vllm/distributed/kv_transfer/kv_connector/v1/offloading_connector.py#L24-L65)）；缓存卸载、跨实例 P/D 传输和接口迁移须分别核对，不能从名称注册推出能力等价。
- **传输前提按 connector 分别理解**：NixlConnector 依赖外部库 `nixl>=0.7.1`（[requirements/kv_connectors.txt](https://github.com/vllm-project/vllm/blob/b17039bccc17b94a2ea107272ad7bc93508708df/requirements/kv_connectors.txt)），默认走 UCX，跨机需 side-channel 握手配置，且其 `kv_role` 是占位、实际 P/D 角色由上层代理决定（[nixl_connector_usage.md L164–166](https://github.com/vllm-project/vllm/blob/b17039bccc17b94a2ea107272ad7bc93508708df/docs/features/nixl_connector_usage.md#L164-L166)）——**connector 之间字段语义不通用**。P2pNcclConnector 的官方示例是单机双卡 1P1D（[disaggregated_prefill.sh](https://github.com/vllm-project/vllm/blob/b17039bccc17b94a2ea107272ad7bc93508708df/examples/online_serving/disaggregated_prefill.sh)）；该版本文档没有声明它是否要求同机或特定 P2P 可达性，此项保留 unknown。
- **观测**：存在 connector 级 Prometheus 框架（[v1/metrics.py L109–160](https://github.com/vllm-project/vllm/blob/b17039bccc17b94a2ea107272ad7bc93508708df/vllm/distributed/kv_transfer/kv_connector/v1/metrics.py#L109-L160)，按 connector 注册、per-engine 标签），但该版本**没有文档页**说明 PD 分离下 TTFT/TPOT 等指标如何归属 P/D 实例；指标归属结论保留 unknown。

## 流量分配是外部职责

vLLM v0.14.0 核心**不含** P/D 路由与负载分配：文档明确生产级 PD 分离"highly related to infrastructure"，需要自研 connector 或第三方组件（[disagg_prefill.md L88–96](https://github.com/vllm-project/vllm/blob/b17039bccc17b94a2ea107272ad7bc93508708df/docs/features/disagg_prefill.md#L88-L96)）。仓库内可得的代理均为 toy/benchmark 性质：测试用代理用 `itertools.cycle` 轮询选实例，并以 `max_tokens=1` + `do_remote_decode=True` 触发远端 decode（[toy_proxy_server.py L66–68、L163–171](https://github.com/vllm-project/vllm/blob/b17039bccc17b94a2ea107272ad7bc93508708df/tests/v1/kv_connector/nixl_integration/toy_proxy_server.py#L66-L68)）；XpYd 演示代理注明 PDController 就绪后将移除（[disagg_proxy_demo.py](https://github.com/vllm-project/vllm/blob/b17039bccc17b94a2ea107272ad7bc93508708df/examples/online_serving/disaggregated_serving/disagg_proxy_demo.py)）。因此"引擎开了 PD 分离"不等于"流量已被合理分配"——路由策略、负载感知与故障摘除是引擎之外需要单独设计和验证的一层。

## 昇腾侧的支持声明与限制

vLLM Ascend v0.14.0rc1 的功能矩阵将 Prefill Decode Disaggregation 标为 **"🟢 Functional, xPyD is supported"**（[supported_features.md L27](https://github.com/vllm-project/vllm-ascend/blob/52d4acfa51fb868823d1070b81cbd2d97e9e4696/docs/source/user_guide/support_matrix/supported_features.md#L27)）。插件侧的特性指南（[feature_guide/disaggregated_prefill.md](https://github.com/vllm-project/vllm-ascend/blob/52d4acfa51fb868823d1070b81cbd2d97e9e4696/docs/source/developer_guide/feature_guide/disaggregated_prefill.md)）给出：

- 两类 connector：MooncakeConnector（D 拉取 P 的 KV）与 MooncakeLayerwiseConnector（P 逐层推送）；架构为全局 proxy 收请求、分别转发 P/D。
- **明确限制**：不支持异构 P/D（如 P 在 A2、D 在 A3）；非对称 TP 仅支持 P_tp > D_tp 且 P_tp % D_tp == 0（该页 L101–105）。
- 启动期 DFX 校验：kv_connector 类型与 module path 可加载、端口冲突 fail-fast、非对称 PD 的 TP 比例校验（实现落地程度未验证）。

读这些声明的边界：矩阵的 Functional 是该插件快照的项目状态，不证明具体模型/硬件/参数组合；教程（如[单机 Mooncake 教程](https://github.com/vllm-project/vllm-ascend/blob/52d4acfa51fb868823d1070b81cbd2d97e9e4696/docs/source/tutorials/pd_disaggregation_mooncake_single_node.md)）内部引用 v0.11.0rc1 等更早版本环境，与 v0.14.0rc1 快照不配套，只能证明步骤形态存在，不能当作该版本的可执行处方；上游 vLLM v0.14.0 与该插件快照不构成已验证配套（插件 conf.py 指向 vLLM v0.14.1）。

## 适用边界

- 动机与"不提升吞吐"的声明来自 vLLM v0.14.0 文档；其他引擎/版本的立场需各自核对。
- connector 清单、字段语义、失败策略均按固定 commit；vLLM 该功能标为 experimental，跨版本不可直接沿用。
- 昇腾侧结论只适用于 vLLM Ascend v0.14.0rc1 快照；MindIE 等其他 NPU 引擎未研究，不继承本文任何结论。
- 本文没有任何实测性能数据；TTFT/ITL 改善的有无与幅度必须以固定负载实测为准（负载口径见[昇腾长尾实验设计](ascend-inference-tail-latency-experiment.md)的方法部分）。

## 常见误解

- **"PD 分离提升吞吐"**：与官方反面声明直接冲突；它改变的是时延构成与资源解耦。
- **"配置了 kv_transfer 就完成了 PD 分离"**：流量分配、健康摘除与扩缩容在引擎之外；toy 代理不是生产组件。
- **"connector 字段语义通用"**：NixlConnector 的 kv_role 是占位，P2pNcclConnector 的 kv_rank/parallel_size 另有含义，须按 connector 读文档。
- **"上游矩阵/字段可直接搬到 NPU"**：昇腾支持状态只看插件矩阵与限制条款；异构 P/D、非对称 TP 有明示约束。
- **"KV 传输出错等于请求失败"**：默认 `kv_load_failure_policy=recompute` 会重算失败 block；只有配置 `fail` 才直接失败——诊断时要先确认策略。

## 例子与相关知识

- 执行阶段与 KV cache 的基础：[推理执行与 KV cache](execution-and-kv-cache.md)；指标口径：[延迟与吞吐指标字典](latency-metrics.md)。
- 长尾诊断中"decode 被 prefill 干扰"的假设与 PD 分离的动机同源：[昇腾推理长尾诊断指南](ascend-inference-tail-latency-triage.md)。
- KV 传输故障的请求级表现与 OOM/失败分层：[昇腾推理 OOM 诊断指南](ascend-inference-oom-triage.md)。

## 来源与待确认问题

- [vLLM v0.14.0 disagg_prefill 文档](https://github.com/vllm-project/vllm/blob/b17039bccc17b94a2ea107272ad7bc93508708df/docs/features/disagg_prefill.md)、[KVTransferConfig](https://github.com/vllm-project/vllm/blob/b17039bccc17b94a2ea107272ad7bc93508708df/vllm/config/kv_transfer.py)、[connector 注册表](https://github.com/vllm-project/vllm/blob/b17039bccc17b94a2ea107272ad7bc93508708df/vllm/distributed/kv_transfer/kv_connector/factory.py#L146-L203)、[NIXL 用法](https://github.com/vllm-project/vllm/blob/b17039bccc17b94a2ea107272ad7bc93508708df/docs/features/nixl_connector_usage.md)。
- [vLLM Ascend v0.14.0rc1 功能矩阵](https://github.com/vllm-project/vllm-ascend/blob/52d4acfa51fb868823d1070b81cbd2d97e9e4696/docs/source/user_guide/support_matrix/supported_features.md#L27)与[PD 特性指南](https://github.com/vllm-project/vllm-ascend/blob/52d4acfa51fb868823d1070b81cbd2d97e9e4696/docs/source/developer_guide/feature_guide/disaggregated_prefill.md)。
- 逐条主张与证据定位见[第十二批 PD 分离来源记录](../../docs/research/batch-12-pd-disaggregation-sources.md)。
- 待确认：P2pNcclConnector 的跨机前提；PD 分离下指标归属与 connector 指标清单；上游 Mooncake/MoRIIO connector 的实现语义；各 connector 的失败路径覆盖度；MindIE-LLM 等其他引擎的对应机制；任何定量效果（需实测）。
