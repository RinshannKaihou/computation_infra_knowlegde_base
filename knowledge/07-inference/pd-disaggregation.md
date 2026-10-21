---
id: inference.pd-disaggregation
title: Prefill/Decode 分离（PD 分离）与流量分配
type: concept
domain: inference
status: draft
platforms: [nvidia, amd, ascend]
source_refs:
  - src.vllm.inference-v0-14
  - src.ascend.vllm-ascend-v0-14-0rc1
  - src.ascend.mindie-llm-docs-69e5a5dd
  - src.ascend.mindie-llm-repo-69e5a5dd
  - src.ascend.mindie-llm-src-69e5a5dd
updated_at: "2026-10-21"
summary: PD 分离把 prefill 与 decode 放进不同实例、用 KV connector 传递 cache，换取 TTFT 与 ITL 的分别调优；vLLM 官方明示它不提升吞吐；按 connector 分列的兼容前提（NIXL 握手 hash 因子与运行时校验、Mooncake 引擎依赖、Ascend 异构/非对称限制）、请求/KV 身份链与本地断言边界、指标阶段与 NIXL 实现明细（Mooncake 该版本缺位）、失败政策上报条件与清理责任、三线对照与"同名不互推"；流量分配是外部代理职责。
related_ids:
  - inference.execution-and-kv-cache
  - inference.latency-metrics
  - inference.ascend-inference-tail-latency-triage
  - inference.quantization-and-quality
  - inference.distributed-inference-layouts
  - inference.model-loading-and-readiness
  - inference.output-quality-evaluation
verification:
  status: source_checked
  evidence_refs:
    - src.vllm.inference-v0-14
    - src.ascend.vllm-ascend-v0-14-0rc1
    - src.ascend.mindie-llm-docs-69e5a5dd
    - src.ascend.mindie-llm-repo-69e5a5dd
    - src.ascend.mindie-llm-src-69e5a5dd
  notes: "已核对 vLLM v0.14.0 的 disagg_prefill/nixl/mooncake 文档、KVTransferConfig、connector 注册表、kv_connector/v1 的 base/metrics/nixl_connector/mooncake_connector 实现、utils/scheduler/request/toy proxy 补查与 requirements/kv_connectors.txt，vLLM Ascend v0.14.0rc1 的功能矩阵、PD 特性指南（两式流程）与 Mooncake 教程（钉 v0.3.7.post2），MindIE-LLM@69e5a5dd FAQ PD 条目与 KV 传输封装局部源码（separate_deployment_engine/TransferOutputHandler）；未部署或运行任何 PD 分离服务。逐条主张与行号锚点见 docs/research/batch-12-pd-disaggregation-sources.md 与 batch-27-t07-07-sources.md（含初审修订轮）。"
---

# Prefill/Decode 分离（PD 分离）与流量分配

## 定义与要解决的问题

PD 分离（disaggregated prefill）把 prefill 与 decode 放进**不同的引擎实例**：prefill 实例产出 KV cache，经 connector 传给 decode 实例继续生成（[vLLM v0.14.0 disagg_prefill 文档](https://github.com/vllm-project/vllm/blob/b17039bccc17b94a2ea107272ad7bc93508708df/docs/features/disagg_prefill.md)）。它帮助回答两类问题：TTFT 与 ITL 能否分别调优（P/D 可用不同的并行策略，见[分布式布局](distributed-inference-layouts.md)），以及长尾 ITL 是否与"decode 中插入 prefill"有关。

读本文前需要的背景：执行阶段与 KV cache 见[推理执行与 KV cache](execution-and-kv-cache.md)，TTFT/TPOT/ITL 的口径见[延迟与吞吐指标字典](latency-metrics.md)。各引擎的支持状态必须按实现单独核对（见下）。

## 动机与官方反面声明

vLLM v0.14.0 文档给出的动机是 TTFT 与 ITL 的分别调优，以及控制尾部 ITL——不分离时 decode 批次中插入 prefill 会抬高尾延迟，chunked prefill 虽可缓解但 chunk size 难调（[disagg_prefill.md L10–13](https://github.com/vllm-project/vllm/blob/b17039bccc17b94a2ea107272ad7bc93508708df/docs/features/disagg_prefill.md#L10-L13)）。同一文档明示：**"Disaggregated prefill DOES NOT improve throughput"**（[L15–16](https://github.com/vllm-project/vllm/blob/b17039bccc17b94a2ea107272ad7bc93508708df/docs/features/disagg_prefill.md#L15-L16)），且该功能在此版本标为 experimental、可能变更。这限定了该版本的功能定位，不能据此承诺吞吐改善。

**本库的评估建议**：在固定请求负载、资源预算、模型与输出长度口径下，联合比较 TTFT/ITL 分布、总吞吐/goodput、失败率及 KV 传输成本。吞吐变化仍是评估项；只改善时延不单独证明同等成本下的服务能力提高。该建议属于本库的方法判断，没有本环境实测结果。

## vLLM v0.14.0 的实现形态

- **配置入口**：`KVTransferConfig`（[vllm/config/kv_transfer.py L13–70](https://github.com/vllm-project/vllm/blob/b17039bccc17b94a2ea107272ad7bc93508708df/vllm/config/kv_transfer.py#L13-L70)）：`kv_connector` 指定 connector 类；`kv_role` ∈ {`kv_producer`, `kv_consumer`, `kv_both`}（配置了 connector 时角色必填，否则 ValueError）；`kv_load_failure_policy` 默认 `recompute`、可配 `fail`——该政策的适用范围见"失败链"节（只作用于**已被 connector 检测并上报**的 KV 加载失败）。
- **connector 清单以源码注册表为准**：[factory.py L146–203](https://github.com/vllm-project/vllm/blob/b17039bccc17b94a2ea107272ad7bc93508708df/vllm/distributed/kv_transfer/kv_connector/factory.py#L146-L203) 注册了 10 个 connector（Example、P2pNccl、LMCacheV1、LMCacheMP、Nixl、Multi、MoRIIO、Offloading、DecodeBench、Mooncake），其中没有 SharedStorageConnector。文档页另述 OffloadingConnector 的 CPU 卸载参数与 MultiConnector 的有序组合（`kv_connector_extra_config.connectors` 列表，[disagg_prefill.md L28–32](https://github.com/vllm-project/vllm/blob/b17039bccc17b94a2ea107272ad7bc93508708df/docs/features/disagg_prefill.md#L28-L32)）。注册名不等于能力等价。
- **平台直接证据与未核组合分记**：NVIDIA 的直接文档证据是 NIXL（`nixl>=0.7.1`，[requirements/kv_connectors.txt](https://github.com/vllm-project/vllm/blob/b17039bccc17b94a2ea107272ad7bc93508708df/requirements/kv_connectors.txt)；另有 lmcache）；**ROCm 的文档分支是 RIXL**（rocm 基础 docker 内置，另有 kv_connectors_rocm.txt，[nixl_connector_usage.md L14–18](https://github.com/vllm-project/vllm/blob/b17039bccc17b94a2ea107272ad7bc93508708df/docs/features/nixl_connector_usage.md#L14-L18)）；其余 connector（P2pNccl/LMCache/MoRIIO/DecodeBench 等）的平台组合未逐一核对，保持 unknown——"上游 connector 族"不是整族可用的声明。

## 按 connector 分列的兼容前提

**NixlConnector（已核条件最全）**：

- **握手兼容 hash**：两侧实例计算兼容 hash，因子＝vLLM 版本、NIXL connector 版本、model 名、模型 dtype、总 KV heads、head size、层数、attention backend、cache dtype（[nixl_connector.py L161–215](https://github.com/vllm-project/vllm/blob/b17039bccc17b94a2ea107272ad7bc93508708df/vllm/distributed/kv_transfer/kv_connector/v1/nixl_connector.py#L161-L215)）——**hash 一致是这些因子一致，不等于权重内容一致或组合必然可运行**；tensor_parallel_size、block_size、kv_cache_layout 故意不入 hash（为支持异构部署），由运行时握手校验；hash 因子集合"likely to evolve"（原注释）。
- **运行时校验（已核条件，非仅入口）**：hash mismatch 失败分支受开关控制（[L1044–1059](https://github.com/vllm-project/vllm/blob/b17039bccc17b94a2ea107272ad7bc93508708df/vllm/distributed/kv_transfer/kv_connector/v1/nixl_connector.py#L1044-L1059)）。并行与块尺寸（[utils.py L349–386](https://github.com/vllm-project/vllm/blob/b17039bccc17b94a2ea107272ad7bc93508708df/vllm/distributed/kv_transfer/kv_connector/utils.py#L349-L386)）：**TP 大值须能被小值整除**（单向，不是任一方向）；**D 侧 local block size 须能被 P 侧 remote block size 整除**。握手布局校验（[L1686–1756](https://github.com/vllm-project/vllm/blob/b17039bccc17b94a2ea107272ad7bc93508708df/vllm/distributed/kv_transfer/kv_connector/v1/nixl_connector.py#L1686-L1756)）：**P_tp>D_tp 且 KV 复制的组合被断言拒绝**；非 MLA 且两侧布局不同时须走实验 HND→NHD 分支；MLA/复制 KV 的 block 长度校验与非复制分支分开——非复制分支在 P_tp>D_tp 时要求 block size 比率＝1。设备/buffer（[设备表 L113–125](https://github.com/vllm-project/vllm/blob/b17039bccc17b94a2ea107272ad7bc93508708df/vllm/distributed/kv_transfer/kv_connector/v1/nixl_connector.py#L113-L125)与[初始化 L861–894](https://github.com/vllm-project/vllm/blob/b17039bccc17b94a2ea107272ad7bc93508708df/vllm/distributed/kv_transfer/kv_connector/v1/nixl_connector.py#L861-L894)）：内置 device→buffer 类别映射＋平台扩展入口；非 CPU 设备选 CPU buffer 时使用 host staging；**无法取得有效 NIXL memory type 时初始化失败**。源码接受某设备类别不构成真实平台支持证明。
- **传输/网络前提**：UCX 为主默认传输（UCX_TLS/UCX_NET_DEVICES 配置；**NCCL 变量不适用**）；侧信道 VLLM_NIXL_SIDE_CHANNEL_PORT 默认 5600（P/D 两侧都要；TP/DP 按 base_port+dp_rank 分配）、VLLM_NIXL_SIDE_CHANNEL_HOST（跨机）；连接信息经 KVTransferParams 从 P 传 D 完成握手（[nixl_connector_usage.md L26–101](https://github.com/vllm-project/vllm/blob/b17039bccc17b94a2ea107272ad7bc93508708df/docs/features/nixl_connector_usage.md#L26-L101)）。
- **kv_role 是占位**：实际 P/D 角色由上层 proxy 决定（toy_proxy_server 的 --prefiller-hosts/--decoder-hosts）（[L157–165](https://github.com/vllm-project/vllm/blob/b17039bccc17b94a2ea107272ad7bc93508708df/docs/features/nixl_connector_usage.md#L157-L165)）。异构 KV 布局（P 用 HND、D 用 NHD）为实验特性（`enable_permute_local_kv`，[L167–175](https://github.com/vllm-project/vllm/blob/b17039bccc17b94a2ea107272ad7bc93508708df/docs/features/nixl_connector_usage.md#L167-L175)）。
- **未知**：NIXL/RIXL 库本体版本矩阵与具体 RDMA 环境。

**MooncakeConnector（上游）**：`pip install mooncake-transfer-engine`；定位是多级缓存池（DRAM/SSD）＋(GPUDirect) RDMA 零拷贝＋多 NIC（[mooncake_connector_usage.md L3–7](https://github.com/vllm-project/vllm/blob/b17039bccc17b94a2ea107272ad7bc93508708df/docs/features/mooncake_connector_usage.md#L3-L7)）；VLLM_MOONCAKE_BOOTSTRAP_PORT 默认 8998（仅 P 侧；TP/DP 端口＝base+dp_rank*tp_size+tp_rank，D 通知 P 用；[L43–48](https://github.com/vllm-project/vllm/blob/b17039bccc17b94a2ea107272ad7bc93508708df/docs/features/mooncake_connector_usage.md#L43-L48)）；**上游 Mooncake 的模型/dtype/TP/block 兼容条件未核（unknown）——不继承 NIXL 或 Ascend 侧的限制表**；Mooncake 引擎本体（kvcache-ai/Mooncake）API 未核。

**P2pNcclConnector**：官方示例为单机双卡 1P1D；是否要求同机/特定 P2P 可达性 unknown。其余 connector 细节未展开。

## KV 传输与权重加载是两条路径

PD 场景下 P/D 两侧**各自走完整的权重加载**（加载链与失败分层见[权重加载](model-loading-and-readiness.md)）；KV 传输是**请求级**的增量数据路径，不经模型加载。

**请求/KV 身份链（按实现分列）**：

| 身份 | NIXL | Mooncake（上游） | 边界 |
|---|---|---|---|
| 代理层请求 ID | toy proxy 生成请求 ID，两个发送函数经 `X-Request-Id` 携带（[toy_proxy_server.py L212–240](https://github.com/vllm-project/vllm/blob/b17039bccc17b94a2ea107272ad7bc93508708df/tests/v1/kv_connector/nixl_integration/toy_proxy_server.py#L212-L240)） | 复用同一 toy proxy | 演示件；生产 router 的 ID 传递属 07.6 |
| 引擎间身份链 | P 在完成时返回 `remote_request_id=request.request_id`、`remote_engine_id=self.engine_id`、`remote_block_ids` 等交接字段（[L794–803](https://github.com/vllm-project/vllm/blob/b17039bccc17b94a2ea107272ad7bc93508708df/vllm/distributed/kv_transfer/kv_connector/v1/nixl_connector.py#L794-L803)）→D 把它们放入 RemoteMeta、**以 D 本地 request ID 为 `reqs_to_recv` 的字典键**（[L266–280](https://github.com/vllm-project/vllm/blob/b17039bccc17b94a2ea107272ad7bc93508708df/vllm/distributed/kv_transfer/kv_connector/v1/nixl_connector.py#L266-L280)）→D 把进程内 transfer handle 关联到本地 request（[L2283–2299](https://github.com/vllm-project/vllm/blob/b17039bccc17b94a2ea107272ad7bc93508708df/vllm/distributed/kv_transfer/kv_connector/v1/nixl_connector.py#L2283-L2299)），完成通知使用 **P 侧的** remote request ID（[L2195–2197](https://github.com/vllm-project/vllm/blob/b17039bccc17b94a2ea107272ad7bc93508708df/vllm/distributed/kv_transfer/kv_connector/v1/nixl_connector.py#L2195-L2197)）——本地 request ID、remote_request_id、engine_id、block_ids 是不同身份，不能以"request_id"一词合并 | D 侧以请求 ID 作字典键（MooncakeConnectorMetadata，[L64–110](https://github.com/vllm-project/vllm/blob/b17039bccc17b94a2ea107272ad7bc93508708df/vllm/distributed/kv_transfer/kv_connector/v1/mooncake_connector.py#L64-L110)） | **无独立稳定的 transfer ID**：传输以本地 request 关联的在途 handle 表达 |
| 元数据传递 | 经 KVTransferParams/响应字段 | **线上负载是 MooncakeAgentMetadata**：D worker 编码发送（[L798–820](https://github.com/vllm-project/vllm/blob/b17039bccc17b94a2ea107272ad7bc93508708df/vllm/distributed/kv_transfer/kv_connector/v1/mooncake_connector.py#L798-L820)）、P worker ZMQ listener 解码消费（[L493–495](https://github.com/vllm-project/vllm/blob/b17039bccc17b94a2ea107272ad7bc93508708df/vllm/distributed/kv_transfer/kv_connector/v1/mooncake_connector.py#L493-L495) 起的跨 P/D worker listener）——RecvReqMeta/SendBlockMeta 是 connector **本地**元数据类（SendBlockMeta 含本地 asyncio.Event 与期限，[L77–110](https://github.com/vllm-project/vllm/blob/b17039bccc17b94a2ea107272ad7bc93508708df/vllm/distributed/kv_transfer/kv_connector/v1/mooncake_connector.py#L77-L110)），不是跨端序列化负载 | 同名类不推出上游与 Ascend 共享身份协议；HTTP ID→引擎内部 ID 的逐层映射未核（unknown） |

**KV 形态与断言（本地范围）**：Mooncake 实现对本 worker 注册的 KV tensor 字节数做**等字节断言**、按 kernel block size 整除并推 block_len（[L682–718](https://github.com/vllm-project/vllm/blob/b17039bccc17b94a2ea107272ad7bc93508708df/vllm/distributed/kv_transfer/kv_connector/v1/mooncake_connector.py#L682-L718)）——**这只核本地注册张量的尺寸一致性，不验证远端 dtype/shape/layout**（AgentMetadata 无远端 dtype/shape 字段）；跨端一致性是**待满足的兼容前提**（NIXL 侧由握手 hash＋运行时校验承担，见上节）。已见的结构检查：请求不在发送清单的 warning（[L565–571](https://github.com/vllm-project/vllm/blob/b17039bccc17b94a2ea107272ad7bc93508708df/vllm/distributed/kv_transfer/kv_connector/v1/mooncake_connector.py#L565-L571)）、两端块数量断言与本地 block_len 寻址（[L608–642](https://github.com/vllm-project/vllm/blob/b17039bccc17b94a2ea107272ad7bc93508708df/vllm/distributed/kv_transfer/kv_connector/v1/mooncake_connector.py#L608-L642)）、NIXL 块数量断言（[L2220–2224](https://github.com/vllm-project/vllm/blob/b17039bccc17b94a2ea107272ad7bc93508708df/vllm/distributed/kv_transfer/kv_connector/v1/nixl_connector.py#L2220-L2224)）——这些是结构性检查；**错请求块、内容损坏、checksum 级完整性检测未在已核实现中出现（unknown）**，等字节数不替代语义一致性验证。

## 指标：阶段归属与实现明细

**阶段×观察者框架（本库建议的观察设计；各行为实现字段）**：

| 阶段（独立事件） | 观察者 | 起点事件→终点事件 | 时间源（建议新增，本地单调时钟；跨主机须先对齐再相减） | 实现字段/证据 | 未决 |
|---|---|---|---|---|---|
| 请求提交 | 客户端 | 客户端发出请求→收到首个合格 payload | 客户端时钟 | 客户端计时 | 端到端 TTFT 的唯一完整窗口 |
| P 创建/prefill | P | 请求入 P→prefill 完成 | P 进程时钟 | P 侧请求日志（字段级时间戳未核，unknown） | P 局部首输出（max_completion_tokens=1）≠客户端首个 payload |
| KV 就绪 | P | prefill 完成→KV 块可传（request_finished 延迟释放前） | P 进程时钟 | P 侧请求状态 | 字段级时间戳未核（unknown） |
| KV 传输 | 传输链路 | NIXL：**D 发起 READ**→轮询发现 DONE 后采集 telemetry | 库内计时 | NixlKVConnectorStats（下表）；READ 调用到 DONE 的墙钟差≠库返回的 xferDuration（库计时边界未核） | telemetry 不覆盖"P 就绪到 D 发起"间隙；完整 prefix 命中时只通知不读块（[L2199–2218](https://github.com/vllm-project/vllm/blob/b17039bccc17b94a2ea107272ad7bc93508708df/vllm/distributed/kv_transfer/kv_connector/v1/nixl_connector.py#L2199-L2218)） |
| D 预分配 | D | 置 RequestStatus.WAITING_FOR_REMOTE_KVS→预分配完成 | D 进程时钟 | D 侧状态 | 通用字段级时间戳未核（unknown） |
| D 接收/复用 | D | 发起接收→接收完成进入 decode（或 prefix 命中免传输） | D 进程时钟 | D 侧状态 | 免传输路径的 D 观察记录未核（unknown） |
| 首 token | D | D decode 首 token | D 进程时钟 | D 侧指标 | **D 侧局部 TTFT 不能替代端到端 TTFT**（观察者窗口不可互换，见[延迟指标](latency-metrics.md)） |

跨实例 TTFT/TPOT 的官方拆分口径无文档页（unknown）；上表 trace 字段属本库设计，不是已有日志。

**NIXL 指标实现明细（b17039bc）——raw→CLI→Prometheus 对照**（[L2483–2566](https://github.com/vllm-project/vllm/blob/b17039bccc17b94a2ea107272ad7bc93508708df/vllm/distributed/kv_transfer/kv_connector/v1/nixl_connector.py#L2483-L2566)、[NixlPromMetrics L2594–2688](https://github.com/vllm-project/vllm/blob/b17039bccc17b94a2ea107272ad7bc93508708df/vllm/distributed/kv_transfer/kv_connector/v1/nixl_connector.py#L2594-L2688)）：

| raw 数据键（单位） | CLI reduce 输出（计算） | Prometheus（类型） |
|---|---|---|
| transfer_duration（秒，采集时 µs→s） | Avg xfer time (ms)／P90 xfer time (ms)（秒→毫秒） | vllm:nixl_xfer_time_seconds（histogram，秒） |
| post_duration（秒） | Avg post time (ms)／P90 post time (ms) | vllm:nixl_post_time_seconds（histogram） |
| bytes_transferred（字节） | Avg MB per transfer（MiB＝2^20 换算但标签写 MB）；Throughput (MB/s)＝总 MiB/成功 duration 之和（非采样墙钟区间） | vllm:nixl_bytes_transferred（histogram） |
| num_descriptors（计数） | Avg number of descriptors | vllm:nixl_num_descriptors（histogram） |
| （成功样本数派生） | Num successful transfers（＝样本数） | — |
| num_failed_transfers / num_failed_notifications（计数） | **不进 CLI reduce 输出** | vllm:nixl_num_failed_transfers／vllm:nixl_num_failed_notifications（counter） |

采样粒度＝每个完成的 transfer handle（非一请求一条）；`is_empty()` 只看成功传输数，纯失败区间 getter 返回 None（[L2406–2413](https://github.com/vllm-project/vllm/blob/b17039bccc17b94a2ea107272ad7bc93508708df/vllm/distributed/kv_transfer/kv_connector/v1/nixl_connector.py#L2406-L2413)）——**无指标输出不能推断无失败**。框架侧：KVConnectorStats 从 worker 序列化送 logger（[metrics.py L19–107](https://github.com/vllm-project/vllm/blob/b17039bccc17b94a2ea107272ad7bc93508708df/vllm/distributed/kv_transfer/kv_connector/v1/metrics.py#L19-L107)）。**MooncakeConnector 在此 commit 无 Stats 实现（已核）**——其传输指标只能靠引擎/系统侧观测；vllm_ascend 侧是否有独立 stats 未核。

## 失败链、取消与清理

**失败政策的作用条件**：`kv_load_failure_policy`（默认 recompute/可配 fail）只作用于**已被 connector 检测并上报给 scheduler 的 KV 加载失败**——基类 `get_block_ids_with_load_errors` 默认返回空集（[base.py L358–376](https://github.com/vllm-project/vllm/blob/b17039bccc17b94a2ea107272ad7bc93508708df/vllm/distributed/kv_transfer/kv_connector/v1/base.py#L358-L376)）；NIXL 实际上报 invalid blocks（[L2020–2033](https://github.com/vllm-project/vllm/blob/b17039bccc17b94a2ea107272ad7bc93508708df/vllm/distributed/kv_transfer/kv_connector/v1/nixl_connector.py#L2020-L2033)），scheduler 据此进入处理并区分 fail/recompute（[scheduler.py L1116–1123、L1872–1936](https://github.com/vllm-project/vllm/blob/b17039bccc17b94a2ea107272ad7bc93508708df/vllm/v1/core/sched/scheduler.py#L1872-L1936)）；**上游 Mooncake 无该 override**，其 receive_kv 在超时/错误响应时记日志并 return（[L818–836](https://github.com/vllm-project/vllm/blob/b17039bccc17b94a2ea107272ad7bc93508708df/vllm/distributed/kv_transfer/kv_connector/v1/mooncake_connector.py#L818-L836)）——错误后的请求终态、D 资源回收与重试结果**unknown**（不据无上报断言挂死，也不断言进入恢复分支）。连接/初始化失败与进程故障不由此配置推导。

**清理责任按阶段分（已核分支）**：

- **调度前取消/未发起**：NIXL 区分调度前取消通知、P 未完成立即释放、已完成后的保留期限（[L757–792](https://github.com/vllm-project/vllm/blob/b17039bccc17b94a2ea107272ad7bc93508708df/vllm/distributed/kv_transfer/kv_connector/v1/nixl_connector.py#L757-L792)）；轮询过期与按 TP consumer 数等待通知见 [L1908–1970](https://github.com/vllm-project/vllm/blob/b17039bccc17b94a2ea107272ad7bc93508708df/vllm/distributed/kv_transfer/kv_connector/v1/nixl_connector.py#L1908-L1970)。
- **保留超时（P 端兜底）**：VLLM_NIXL/VLLM_MOONCAKE_ABORT_REQUEST_TIMEOUT 默认 480s（[NIXL usage L98–101](https://github.com/vllm-project/vllm/blob/b17039bccc17b94a2ea107272ad7bc93508708df/docs/features/nixl_connector_usage.md#L98-L101)、[Mooncake usage L50–52](https://github.com/vllm-project/vllm/blob/b17039bccc17b94a2ea107272ad7bc93508708df/docs/features/mooncake_connector_usage.md#L50-L52)）——请求中止且对端未读取/未通知时 P 侧释放 KV 块。**计时起点按实现**：NIXL 在 P 已完成且延迟释放的 request_finished 分支设 `perf_counter()+timeout` 并按轮询检查（[L770–792、L1908–1970](https://github.com/vllm-project/vllm/blob/b17039bccc17b94a2ea107272ad7bc93508708df/vllm/distributed/kv_transfer/kv_connector/v1/nixl_connector.py#L770-L792)）；Mooncake 在 worker 接到完成后的非空 block 列表时设期限（[L856–872](https://github.com/vllm-project/vllm/blob/b17039bccc17b94a2ea107272ad7bc93508708df/vllm/distributed/kv_transfer/kv_connector/v1/mooncake_connector.py#L856-L872)）——不是从"请求中止"事件统一计时。**在途失败的 D 侧责任（已核信号）**：NIXL 释放失败 handle 并标记 invalid blocks（见失败政策节）——这不等同于已证明 D 预分配 KV 全部回收，D 侧 KV 清理链 unknown。**边界**：480s 是 P 端保留块超时，不是所有分支的清理上限——Mooncake 在开始处理 D 请求时把 expire_time 改为无穷、`batch_transfer_sync_write` 成功后才由 P 标记发送完成（[L565–593](https://github.com/vllm-project/vllm/blob/b17039bccc17b94a2ea107272ad7bc93508708df/vllm/distributed/kv_transfer/kv_connector/v1/mooncake_connector.py#L565-L593)），其清理只遍历期限已过的发送项（[L746–764](https://github.com/vllm-project/vllm/blob/b17039bccc17b94a2ea107272ad7bc93508708df/vllm/distributed/kv_transfer/kv_connector/v1/mooncake_connector.py#L746-L764)；普通保留期限 [L856–865](https://github.com/vllm-project/vllm/blob/b17039bccc17b94a2ea107272ad7bc93508708df/vllm/distributed/kv_transfer/kv_connector/v1/mooncake_connector.py#L856-L865)）——**已进入发送而后失败的路径不保证由 480s 回收**；Mooncake D 侧 receive_kv 的 ZMQ 接收另有 60000ms 超时（`sock.setsockopt(zmq.RCVTIMEO, 60000)`，[L814–821](https://github.com/vllm-project/vllm/blob/b17039bccc17b94a2ea107272ad7bc93508708df/vllm/distributed/kv_transfer/kv_connector/v1/mooncake_connector.py#L814-L821)），与 480s 不同类。进程故障下的任何清理都不保证执行。
- **正常完成**：NIXL/Ascend 拉式＝D 接收后通知 P 释放（前文两式流程）；**上游 Mooncake 写入式＝传输成功后由 P 标记发送完成**——正常释放触发点按实现分记。
- **三层重试不要合并**：connector 内块重算（kv_load_failure_policy）、MindIE 通信域建连重试（kv_link_timeout 重试至成功或超时退出）、外部 router 的整请求重试/取消传播——后者是引擎外待设计验证的责任边界（见下节）。

**MindIE 失败证据**：PD 分离 D 节点 "Pull kv failed"（ERROR 级，CANN status_code 含 timeout）＝P→D KV 传输超时，官方 FAQ 判定极可能网络质量差（[faq.md L270–280](https://github.com/Ascend/MindIE-LLM/blob/69e5a5dd4b533eaffc7e198320435350825a36f7/docs/zh/faq/faq.md#L270-L280)）；kv_trans_timeout（D 拉 KV，默认 10s）与 kv_link_timeout（通信域建立，默认/建议 1080s）见[MindIE 执行档案](mindie-execution-profile.md)。**MindIE 传输实现状态**：开源仓内已有 KV 传输封装与局部检查——`separate_deployment_engine.py` 调用 `cache_manager.pull_blocks` 并处理 CANN 异常（[L432–452](https://github.com/Ascend/MindIE-LLM/blob/69e5a5dd4b533eaffc7e198320435350825a36f7/mindie_llm/text_generator/utils/separate_deployment_engine.py#L432-L452)）、检查远端 instance 已链接与 block ID 越界并返回错误码（[L575–603](https://github.com/Ascend/MindIE-LLM/blob/69e5a5dd4b533eaffc7e198320435350825a36f7/mindie_llm/text_generator/utils/separate_deployment_engine.py#L575-L603)），C++ TransferOutputHandler 处理请求 ID、取消后结果与失败回调（[L24–58](https://github.com/Ascend/MindIE-LLM/blob/69e5a5dd4b533eaffc7e198320435350825a36f7/src/engine/transfer_output_handler.cpp#L24-L58)）；`kv_transfer_agent.py` 的 KvTransferAgent 为占位类（[L10–17](https://github.com/Ascend/MindIE-LLM/blob/69e5a5dd4b533eaffc7e198320435350825a36f7/mindie_llm/distributed/kv_transfer/kv_transfer_agent.py#L10-L17)）；底层 `LLMDataDist` 来自外部 llm_datadist 依赖——**底层传输协议、完整路径与指标未核（unknown），占位类不证明全仓缺位**。

## 流量分配是外部职责

vLLM v0.14.0 核心**不含** P/D 路由与负载分配：文档明确生产级 PD 分离"highly related to infrastructure"，需要自研 connector 或第三方组件。仓库内可得的代理均为 toy/benchmark 性质：测试用代理用 `itertools.cycle` 轮询选实例，以 `max_tokens=1`＋`do_remote_decode=True` 触发远端 decode（[toy_proxy_server.py L66–68、L161–173](https://github.com/vllm-project/vllm/blob/b17039bccc17b94a2ea107272ad7bc93508708df/tests/v1/kv_connector/nixl_integration/toy_proxy_server.py#L161-L173)）；XpYd 演示代理（[disagg_proxy_demo.py](https://github.com/vllm-project/vllm/blob/b17039bccc17b94a2ea107272ad7bc93508708df/examples/online_serving/disaggregated_serving/disagg_proxy_demo.py)）注明 PDController 就绪后将移除。因此"引擎开了 PD 分离"不等于"流量已被合理分配"——路由策略、负载感知与故障摘除是引擎之外需要单独设计和验证的一层（见[请求路由、准入与流控](routing-and-flow-control.md)与[容量与扩缩容](capacity-and-autoscaling.md)）。

## 昇腾侧（vLLM Ascend）与 MindIE 对照

**vLLM Ascend v0.14.0rc1**：功能矩阵将 Prefill Decode Disaggregation 标为 "Functional, xPyD is supported"。特性指南给出两类 connector 的完整请求流（[disaggregated_prefill.md L38–99](https://github.com/vllm-project/vllm-ascend/blob/52d4acfa51fb868823d1070b81cbd2d97e9e4696/docs/source/developer_guide/feature_guide/disaggregated_prefill.md#L38-L99)）：**MooncakeConnector＝D 拉式**——proxy select_prefiller 转发（do_remote_decode=True、max_completion_tokens=1、min_tokens=1）→P 完成后 request_finished 延迟 KV 释放并回 do_remote_prefill=True→proxy select_decoder→D 置 `RequestStatus.WAITING_FOR_REMOTE_KVS`（指南 L45/L51 原文，词尾带 S）→预分配 KV、kv_connector_no_forward 拉远端 KV、通知 P 释放、decode 返回；**MooncakeLayerwiseConnector＝P 逐层推式**——D 先等待并向 metaserver 请求，proxy 的 metaserver 端点选 P，P 逐层推送完成后释放并通知 D。明确限制：不支持异构 P/D；非对称 TP 仅 P_tp>D_tp 且整除（[L103–105](https://github.com/vllm-project/vllm-ascend/blob/52d4acfa51fb868823d1070b81cbd2d97e9e4696/docs/source/developer_guide/feature_guide/disaggregated_prefill.md#L103-L105)）；启动期 DFX 校验（kv_connector 可加载、端口冲突 fail-fast、TP 比例校验——设计声明，实现落地未验证）。部署前提（[教程编译节 L100–141](https://github.com/vllm-project/vllm-ascend/blob/52d4acfa51fb868823d1070b81cbd2d97e9e4696/docs/source/tutorials/pd_disaggregation_mooncake_single_node.md#L100-L141)）：Mooncake 钉 **v0.3.7.post2** 源码编译（mpich/dependencies.sh、`cmake -DUSE_ASCEND_DIRECT=ON`、LD_LIBRARY_PATH 指向 site-packages/mooncake，L100–141）；P/D 两侧 HCCL_IF_IP=节点 IP、GLOO/TP/HCCL_SOCKET_IFNAME=网卡名等（L141–201）；教程内 vLLM 版本引用落后于快照，只作步骤形态证据。

**MindIE（文档线 3.1.0）**：PD 分离（inferMode=dmi）与 PD 混部（standard）两式；失败证据与超时配置见上节；底层传输实现/协议及完整路径未核（unknown），dmi 部署示例指向的 MindIE Motor 指南未取证。PD 混部叠加约束见[MindIE 执行档案](mindie-execution-profile.md)。

三线对照：NVIDIA 有 NIXL 直接文档证据、ROCm 有 RIXL 分支（其余组合 unknown）；Ascend 走 vLLM Ascend 的 Mooncake 两式或 MindIE 自有机制；**注册名相同的 connector（如 Mooncake）在上游与插件侧的实现与前提不互推**。

## 适用边界

- 动机与"不提升吞吐"的声明来自 vLLM v0.14.0 文档；该功能标 experimental，跨版本不可直接沿用。
- connector 清单、兼容校验、失败政策、指标实现均按固定 commit（b17039bc）；Mooncake 版本线按 vLLM Ascend 教程钉 v0.3.7.post2，与上游 pip 包的对应关系未核。
- 昇腾侧结论只适用于 vLLM Ascend v0.14.0rc1 快照与 MindIE 文档线 3.1.0；上游 vLLM v0.14.0 与插件快照不构成已验证配套（插件 conf.py 指向 vLLM v0.14.1）。
- 本文没有任何实测性能数据；TTFT/ITL 改善的有无与幅度必须以固定负载实测为准（[昇腾长尾实验设计](ascend-inference-tail-latency-experiment.md)的方法部分）；PD 输出一致性对照入口见[输出质量评估](output-quality-evaluation.md)。

## 常见误解

- **"PD 分离提升吞吐"**：与官方反面声明直接冲突；它改变的是时延构成与资源解耦。
- **"配置了 kv_transfer 就完成了 PD 分离"**：流量分配、健康摘除与扩缩容在引擎之外；toy 代理不是生产组件。
- **"connector 字段语义通用"**：NixlConnector 的 kv_role 是占位，P2pNcclConnector 的 kv_rank/parallel_size 另有含义，须按 connector 读文档。
- **"NCCL 调优变量对 KV 传输有效"**：NixlConnector 走 UCX，NCCL 变量不适用。
- **"KV 加载失败一定走 recompute"**：政策只作用于已检测并上报的失败；上报路径按 connector 分列（Mooncake 无该 override）。
- **"480s 会清理一切"**：它是 P 端保留块超时；在途失败、进程故障下的清理不保证。
- **"KV 传输慢查模型加载"**：权重加载与 KV 传输是两条路径；前者启动期一次性，后者请求级、走 connector/网络栈。
- **"MindIE 与 vLLM 的 Mooncake 是同一实现"**：同名不互推；MindIE 底层协议未核。

## 来源与待确认问题

- vLLM v0.14.0：[disagg_prefill](https://github.com/vllm-project/vllm/blob/b17039bccc17b94a2ea107272ad7bc93508708df/docs/features/disagg_prefill.md)、[nixl_connector_usage](https://github.com/vllm-project/vllm/blob/b17039bccc17b94a2ea107272ad7bc93508708df/docs/features/nixl_connector_usage.md)、[mooncake_connector_usage](https://github.com/vllm-project/vllm/blob/b17039bccc17b94a2ea107272ad7bc93508708df/docs/features/mooncake_connector_usage.md)、[KVTransferConfig](https://github.com/vllm-project/vllm/blob/b17039bccc17b94a2ea107272ad7bc93508708df/vllm/config/kv_transfer.py)、[connector 注册表](https://github.com/vllm-project/vllm/blob/b17039bccc17b94a2ea107272ad7bc93508708df/vllm/distributed/kv_transfer/kv_connector/factory.py#L146-L203)、[v1/metrics.py](https://github.com/vllm-project/vllm/blob/b17039bccc17b94a2ea107272ad7bc93508708df/vllm/distributed/kv_transfer/kv_connector/v1/metrics.py)、[nixl_connector.py](https://github.com/vllm-project/vllm/blob/b17039bccc17b94a2ea107272ad7bc93508708df/vllm/distributed/kv_transfer/kv_connector/v1/nixl_connector.py)、[mooncake_connector.py](https://github.com/vllm-project/vllm/blob/b17039bccc17b94a2ea107272ad7bc93508708df/vllm/distributed/kv_transfer/kv_connector/v1/mooncake_connector.py)、[utils.py](https://github.com/vllm-project/vllm/blob/b17039bccc17b94a2ea107272ad7bc93508708df/vllm/distributed/kv_transfer/kv_connector/utils.py)、[scheduler.py](https://github.com/vllm-project/vllm/blob/b17039bccc17b94a2ea107272ad7bc93508708df/vllm/v1/core/sched/scheduler.py)、[toy_proxy_server.py](https://github.com/vllm-project/vllm/blob/b17039bccc17b94a2ea107272ad7bc93508708df/tests/v1/kv_connector/nixl_integration/toy_proxy_server.py)。
- vLLM Ascend v0.14.0rc1：[功能矩阵](https://github.com/vllm-project/vllm-ascend/blob/52d4acfa51fb868823d1070b81cbd2d97e9e4696/docs/source/user_guide/support_matrix/supported_features.md#L27)、[PD 特性指南](https://github.com/vllm-project/vllm-ascend/blob/52d4acfa51fb868823d1070b81cbd2d97e9e4696/docs/source/developer_guide/feature_guide/disaggregated_prefill.md)、[Mooncake 单机教程](https://github.com/vllm-project/vllm-ascend/blob/52d4acfa51fb868823d1070b81cbd2d97e9e4696/docs/source/tutorials/pd_disaggregation_mooncake_single_node.md)；MindIE：[FAQ](https://github.com/Ascend/MindIE-LLM/blob/69e5a5dd4b533eaffc7e198320435350825a36f7/docs/zh/faq/faq.md)、[separate_deployment_engine.py](https://github.com/Ascend/MindIE-LLM/blob/69e5a5dd4b533eaffc7e198320435350825a36f7/mindie_llm/text_generator/utils/separate_deployment_engine.py)、[transfer_output_handler.cpp](https://github.com/Ascend/MindIE-LLM/blob/69e5a5dd4b533eaffc7e198320435350825a36f7/src/engine/transfer_output_handler.cpp)。
- 逐条主张与证据定位见[第十二批 PD 来源记录](../../docs/research/batch-12-pd-disaggregation-sources.md)与[第二十七批 T07-07 来源记录](../../docs/research/batch-27-t07-07-sources.md)（含初审修订轮）。
- 待确认：NIXL/RIXL 库本体与 UCX 版本矩阵；Mooncake 引擎仓（v0.3.7.post2）API 与上游兼容条件；vllm_ascend 侧独立 stats；错请求/内容损坏/checksum 检测；Mooncake 错误后的请求终态与 D 资源回收；HTTP ID→引擎内部 ID 映射；跨实例 TTFT/TPOT 官方拆分；P2pNccl/LMCache/Offloading 细节；MindIE LLMDataDist 底层与 Motor 指南；任何定量效果（需实测）。
