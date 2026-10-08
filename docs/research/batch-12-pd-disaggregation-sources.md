# 第十二批 PD 分离（Prefill/Decode 分离）来源核查与证据提取

**2026-10-08 修订注记：** Codex `gpt-6.1-sol / xhigh` 按 B12-C04/C05 修正本记录并完成[定向复核](batch-10-11-12-codex-recheck.md)。下述原研究者、首次获取方式与当时任务状态为历史；修订补读和保留的未知条件见本记录及复核报告。

- 日期：2026-10-08
- 研究者：探索子代理（非 astra）
- 目标正文：`inference.pd-disaggregation`（暂名），`knowledge/07-inference/` 下 concept 页「Prefill/Decode 分离（PD 分离）与流量分配」
- 范围：仅覆盖两个已固定快照——vLLM v0.14.0（commit `b17039bccc17b94a2ea107272ad7bc93508708df`，registry id `src.vllm.inference-v0-14`）与 vLLM-Ascend v0.14.0rc1（commit `52d4acfa51fb868823d1070b81cbd2d97e9e4696`，registry id `src.ascend.vllm-ascend-v0-14-0rc1`）。只读取 GitHub 固定 commit 文件（gh api 原文件定行号）；未克隆、安装、运行任何代码；未访问 GPU/NPU。

## 主张—证据表

### A. 定义与动机

| 主张 | 来源与定位 | 版本/环境 | 证据性质 | 反例/未知 |
|---|---|---|---|---|
| A1. PD 分离把 prefill 与 decode 放进不同 vLLM 实例，用 connector 在两者间传 prefill 的 KV cache 与结果 | vllm `docs/features/disagg_prefill.md` L50-L54 @b17039b | vLLM v0.14.0 | 官方文档 | 无 |
| A2. 动机之一：TTFT 与 ITL 可分别调优（P/D 可用不同 tp/pp 并行策略） | 同上 L10-L12 | 同上 | 官方文档 | 文档措辞是该版本的功能定位，非性能承诺 |
| A3. 动机之二：控制尾部 ITL——不分离时 decode 中插入 prefill 抬高尾延迟；chunked prefill 虽可缓解但 chunk size 难调 | 同上 L13 | 同上 | 官方文档 | 无定量阈值 |
| A4. 「Disaggregated prefill DOES NOT improve throughput」——该版本官方明示不提升吞吐 | 同上 L15-L16 | 同上 | 官方文档（反面声明） | B12-C04：声明不意味着排除吞吐评估；本库建议在固定负载/资源下联合比较时延、吞吐/goodput、失败率与 KV 传输成本，属于方法判断且未实测 |
| A5. 该功能在 vLLM v0.14.0 中标为 experimental，可能变更 | 同上 L1, L5-L6 | 同上 | 官方文档 | 无 |
| A6. vLLM-Ascend 的动机表述同构：分别调 P/D 的并行策略（dp/tp/ep）与实例数以优化 TTFT/TPOT；避免 decode 中插入 prefill | vllm-ascend `docs/source/developer_guide/feature_guide/disaggregated_prefill.md` L3-L11 @52d4acf | vLLM-Ascend v0.14.0rc1 | 官方文档 | 无 |

### B. vLLM v0.14.0 实现形态

| 主张 | 来源与定位 | 版本/环境 | 证据性质 | 反例/未知 |
|---|---|---|---|---|
| B1. 全部实现位于 `vllm/distributed/kv_transfer`；抽象三层：Pipe（send_tensor/recv_tensor 单向 FIFO）、LookupBuffer（insert/drop_select，类 SQL 语义）、Connector（连接前两者到 vLLM） | `docs/features/disagg_prefill.md` L54-L63；`vllm/distributed/kv_transfer/README.md` L9-L13 @b17039b | vLLM v0.14.0 | 官方文档+源码 README | LookupBuffer/Pipe 是早期抽象措辞；V1 connector 实际接口以 `kv_connector/v1/base.py` 为准（本轮未逐行读 base.py） |
| B2. 每个 vLLM 进程各有一个 connector：scheduler 进程内 connector 调度传输，worker 进程内 connector 执行传输；KV store/load 逐层与 attention 模块配合 | `docs/features/disagg_prefill.md` L75-L86 | 同上 | 官方文档 | 无 |
| B3. `KVTransferConfig` 关键字段：`kv_connector`（connector 类名）、`kv_role` ∈ {`kv_producer`,`kv_consumer`,`kv_both`}、engine_id、kv_buffer_device（默认 "cuda"，可选 cuda/cpu）、kv_buffer_size（默认 1e9）、kv_rank、kv_parallel_size（默认 1）、kv_ip/kv_port、`kv_connector_extra_config`、`kv_connector_module_path`（自定义模块加载，仅 V1）、`kv_load_failure_policy`（默认 "recompute"，可选 "fail"） | `vllm/config/kv_transfer.py` L13-L70 @b17039b | 同上 | 源码实现 | `kv_rank` 文档字符串 L44-L45 写「Currently only 1P1D is supported」，与同 commit 的 XpYd 示例存在张力（见冲突 C1） |
| B4. 运行时校验：kv_connector 非空时 kv_role 必填，否则抛 ValueError；角色判定属性 `is_kv_transfer_instance`/`is_kv_producer`/`is_kv_consumer` | 同上 L90-L116 | 同上 | 源码实现 | 无 |
| B5. 该 commit 工厂注册的 connector 共 10 个：ExampleConnector、P2pNcclConnector、LMCacheConnectorV1、LMCacheMPConnector、NixlConnector、MultiConnector、MoRIIOConnector、OffloadingConnector、DecodeBenchConnector、MooncakeConnector | `vllm/distributed/kv_transfer/kv_connector/factory.py` L146-L203 | 同上 | 源码实现（注册表） | 文档用法条目与注册表不是同一清单（Example/LMCacheV1/Nixl/P2pNccl/Multi/Offloading，disagg_prefill.md L22–44）；**该 commit 全树无 SharedStorageConnector**（递归 tree grep 计数 0），正文不可沿用旧版概念 |
| B6. P2pNcclConnector：基于 NCCL 的点对点传输；示例为单机双卡 1P1D（CUDA_VISIBLE_DEVICES=0/1），prefill 侧 `kv_role=kv_producer,kv_rank=0`，decode 侧 `kv_consumer,kv_rank=1`，`kv_parallel_size=2` | `examples/online_serving/disaggregated_prefill.sh` L56-L74；`vllm/.../p2p/p2p_nccl_engine.py` L37-L64（设置 NCCL_MAX/MIN_NCHANNELS、NCCL_CUMEM_ENABLE=1） | 同上 | 示例脚本+源码 | 文档未声明必须同机；示例注释只说「可调整 --kv-ip/--kv-port 用于分布式推理」（脚本 L54）。「P2P 是否要求同机或 P2P 可达」在本 commit 文档中无明确表述——标 unknown |
| B7. NixlConnector：依赖 NIXL 库（`nixl>=0.7.1`，requirements/kv_connectors.txt L1-L2），全异步 send/recv；NIXL 底层默认主要传输为 UCX，可配 backends（如 UCX、GDS）；同机与跨机均有用法，跨机需 `VLLM_NIXL_SIDE_CHANNEL_HOST/PORT` 做握手 | `docs/features/nixl_connector_usage.md` L3, L9, L26-L37, L39, L86-L97, L103-L142 @b17039b | 同上 | 官方文档 | NIXL 本身是外部库（ai-dynamo/nixl），其版本行为不在本快照内 |
| B8. NixlConnector 不区分 kv_role（实际 P/D 角色由上层代理决定，kv_role 相当于占位） | `docs/features/nixl_connector_usage.md` L164-L166 | 同上 | 官方文档（tip） | 与 B3 的通用字段语义不同，正文须按 connector 分别表述 |
| B9. 路由/调度不在 vLLM 核心内：需外部代理。示例代理为 toy/benchmark 性质——`benchmarks/disagg_benchmarks/disagg_prefill_proxy_server.py`（1P1D，示例脚本 L80-L88 注明未来将引入 "vllm connect"）；`examples/online_serving/disaggregated_serving/disagg_proxy_demo.py` L3-L16 演示 XpYd 且注明「PDController（PR 15343）支持 XpYd 后本 demo 将移除」；`tests/.../nixl_integration/toy_proxy_server.py` L66-L68 用 itertools.cycle 轮询选 P/D，L163-L171 用 `do_remote_decode=True` + `max_tokens=1` 触发 prefill | 三个文件 @b17039b | 同上 | 示例/测试代码 | 这些代理不是生产组件；无内建负载感知路由的证据 |
| B10. 生产级 PD 分离依赖第三方 connector，vLLM 官方明示「highly related to infrastructure」，并给出三条扩展路径（自研 Connector / 实现 LookupBuffer / 实现 Pipe） | `docs/features/disagg_prefill.md` L88-L96 | 同上 | 官方文档 | 无 |
| B11. connector 级 Prometheus 度量存在框架支持：`KVConnectorPromMetrics`/`KVConnectorPrometheus` 基类支持按 connector 注册并记录传输统计（per-engine 标签） | `vllm/distributed/kv_transfer/kv_connector/v1/metrics.py` L109-L160 @b17039b | 同上 | 源码实现 | **无专门的 disagg 度量文档页**；docs/usage/metrics.md 全页 grep 无 disagg/kv_connector 字样。「disagg 对度量的影响」仅有代码级证据，指标清单未逐个核对——标 unknown/partial |
| B12. KV 加载失败有明确策略：`kv_load_failure_policy` 默认 "recompute"（重调度重算失败 block），可配 "fail"（以错误 finish reason 结束请求） | `vllm/config/kv_transfer.py` L67-L70 | 同上 | 源码实现 | 各 connector 实际失败路径的覆盖度未验证 |

### C. vLLM-Ascend v0.14.0rc1 支持状态

| 主张 | 来源与定位 | 版本/环境 | 证据性质 | 反例/未知 |
|---|---|---|---|---|
| C1. feature matrix：「Prefill Decode Disaggregation | 🟢 Functional | Functional, xPyD is supported.」；图例：Functional=完全可用并持续优化 | `docs/source/user_guide/support_matrix/supported_features.md` L27, L33-L37 @52d4acf | vLLM-Ascend v0.14.0rc1 | 官方文档（状态表） | 「Functional」只代表该插件快照的项目状态，不证明具体模型/硬件/参数组合 |
| C2. Ascend 侧支持两类 connector：MooncakeConnector（D 拉取 P 的 KV）与 MooncakeLayerwiseConnector（P 按层推送给 D）；架构为全局 proxy 收请求、转发 prefill 到 P、decode 到 D，P/D 间 P2P 传 KV | `docs/source/developer_guide/feature_guide/disaggregated_prefill.md` L17-L31 @52d4acf | 同上 | 官方文档 | 无 |
| C3. 规格表自述支持 A2、A3、equal/unequal TP、MLA、GQA，均标 Functional | 同上 L66-L75 | 同上 | 官方文档 | 未经实验验证 |
| C4. 明确限制：不支持异构 P/D（如 P 在 A2、D 在 A3）；非对称 TP 仅支持 P_tp > D_tp 且 P_tp % D_tp == 0 | 同上 L101-L105 | 同上 | 官方文档（限制条款） | 无 |
| C5. 存在 connector 实现：`vllm_ascend/distributed/kv_transfer/kv_p2p/mooncake_connector.py`、`mooncake_layerwise_connector.py`；另有 kv_pool/ascend_store（memcache 与 mooncake 两种 backend）及 kv_pool/cpu_offload | 仓库 tree @52d4acf | 同上 | 源码实现（存在性） | 仅核对存在性与类名，未逐行核对传输语义 |
| C6. 存在 PD 分离教程：单机 `pd_disaggregation_mooncake_single_node.md`（1P1D、Qwen2.5-VL-7B、1 台 Atlas 800T A2）；多机 `pd_disaggregation_mooncake_multi_node.md`；另有 `pd_colocated_mooncake_multi_instance.md`。前提含：hccn 链路/TLS 检查、容器挂载 NPU 设备、从源码构建 Mooncake（教程写 `v0.3.7.post2`）、kv_connector 用 "MooncakeConnectorV1"、代理用 examples 的 `load_balance_proxy_server_example.py` | `docs/source/tutorials/pd_disaggregation_mooncake_single_node.md` L1-L7, L17-L56, L95-L107, L173, L215, L240-L243 @52d4acf | 同上 | 官方教程 | 教程正文写「use vllm-ascend v0.11.0rc1 (with vLLM v0.11.0)」（L7）——**教程内版本引用落后于快照自身**；且 L240 链接指向 `blob/main`（动态链接）；`examples/.../mooncake_connector_deployment_guide.md` L5-L15 的环境依赖（CANN 8.3.rc2 / torch 2.8.0 / vllm v0.10.1）同样落后。均不可当作 v0.14.0rc1 配套处方 |
| C7. Ascend 的 DFX 设计含：启动前校验 kv_connector 类型与 module path 可加载、端口冲突 fail-fast、非对称 PD 的 P/D tp 比例校验 | feature_guide/disaggregated_prefill.md L85-L97 @52d4acf | 同上 | 官方文档 | 未验证实现落地程度 |

### D. 许可

| 主张 | 来源与定位 | 版本/环境 | 证据性质 | 反例/未知 |
|---|---|---|---|---|
| D1. vLLM 仓库根 LICENSE 为 Apache License 2.0（该 commit 直接核对） | `LICENSE` @b17039b（gh api 读取头部） | vLLM v0.14.0 | 源码 | docs 目录下无独立 LICENSE（递归 tree 无 docs/*license* 命中）；docs.vllm.ai 生成站点许可未单独核对 |
| D2. vLLM-Ascend 仓库根 LICENSE 为 Apache License 2.0（该 commit 直接核对） | `LICENSE` @52d4acf | vLLM-Ascend v0.14.0rc1 | 源码 | 全仓库仅根 LICENSE 一个许可文件；生成站点与外链材料另计 |

## 关键实现要点摘录

**kv_role 取值（vllm/config/kv_transfer.py L13-L15, L38-L40）**：
`KVProducer = Literal["kv_producer", "kv_both"]`；`KVConsumer = Literal["kv_consumer", "kv_both"]`；`KVRole = Literal[KVProducer, KVConsumer]`。字段说明原文：「Whether this vLLM instance produces, consumes KV cache, or both.」

**vLLM v0.14.0 factory 注册的 connector（factory.py L146-L203，共 10 个）**：
ExampleConnector、P2pNcclConnector、LMCacheConnectorV1、LMCacheMPConnector、NixlConnector、MultiConnector、MoRIIOConnector、OffloadingConnector、DecodeBenchConnector、MooncakeConnector。

**Ascend feature matrix 行原文（supported_features.md L27）**：
`| Prefill Decode Disaggregation | 🟢 Functional  | Functional, xPyD is supported. |`

**Ascend 限制原文（feature_guide L103-L105）**：
「Heterogeneous P and D nodes are not supported—for example, running P nodes on A2 and D nodes on A3.」「In non-symmetric TP configurations, only cases where the P nodes have a higher TP degree than the D nodes and the P TP count is an integer multiple of the D TP count are supported (i.e., P_tp > D_tp and P_tp % D_tp = 0).」

**流量分配机制（上游 toy 代理，toy_proxy_server.py）**：L66-L68 `itertools.cycle` 轮询 P/D 实例；L163-L171 请求先送 prefill 并置 `kv_transfer_params.do_remote_decode=True`、`max_tokens=1`，再送 decode。

## 冲突与未解决项

1. **kv_rank 文档字符串 vs XpYd 示例**：`kv_transfer.py` L44-L45 写「Currently only 1P1D is supported」，但同 commit 存在 XpYd 演示代理（disagg_proxy_demo.py）与 NixlConnector 多实例文档（nixl_connector_usage.md L103-L154）。合理解读是该注释针对 P2pNcclConnector 式 kv_rank 用法而非全局能力，但正文不应引用该字符串断言「vLLM 只支持 1P1D」。
2. **SharedStorageConnector 的名称证据**：固定工厂注册表无该名称，此前全树名称检索也未命中；不能因此把 OffloadingConnector/LMCache 系认作旧共享存储接口的对应物。补读 [offloading_connector.py L24–65](https://github.com/vllm-project/vllm/blob/b17039bccc17b94a2ea107272ad7bc93508708df/vllm/distributed/kv_transfer/kv_connector/v1/offloading_connector.py#L24-L65)仅确认其接入 kv_offload；跨实例 P/D 传输、具体后端和迁移兼容关系未证明。B12-C05 删除原替代关系推断，保留能力边界。
3. **P2pNcclConnector 同机要求不明**：文档与示例均未明示是否必须同机或需要特定 P2P 可达性；仅有「可调 --kv-ip/--kv-port」的示例注释。标 unknown。
4. **disagg 度量文档缺失**：仅有 connector 级 Prometheus 框架的源码证据（metrics.py L109-L160），无文档页说明 PD 分离下 TTFT/TPOT 等指标如何归属 P/D 实例。标 unknown。
5. **Ascend 教程版本漂移**：单机教程引用 v0.11.0rc1、deployment guide 引用 v0.10.1 环境；与本快照 v0.14.0rc1 不配套，只能作为「存在教程与步骤形态」的证据，不能作为该版本的可执行处方。
6. **Ascend 快照与上游配套**：同 batch-04 结论——该快照 conf.py 指向 vLLM v0.14.1，与本文主样板 vLLM v0.14.0 不构成已验证配套。
7. 未读取项（时间盒内未覆盖）：`kv_connector/v1/base.py` 的 V1 接口全文、MooncakeConnector（上游版）实现细节、moriio connector 的归属与前提、benchmarks/disagg_benchmarks 的测量方法、各 connector 单测语义。

## 实际读取清单（全部经 gh api 取固定 commit 原文件）

**vLLM @ b17039bccc17b94a2ea107272ad7bc93508708df**：
- `docs/features/disagg_prefill.md`（全文，行号以此为准）
- `docs/features/nixl_connector_usage.md`（全文）
- `docs/usage/metrics.md`（grep disagg/kv_connector 无命中）
- `vllm/config/kv_transfer.py`（全文）
- `vllm/distributed/kv_transfer/README.md`（全文）
- `vllm/distributed/kv_transfer/kv_connector/factory.py`（全文）
- `vllm/distributed/kv_transfer/kv_connector/v1/p2p/p2p_nccl_connector.py`（头部 L1-L60）、`p2p/p2p_nccl_engine.py`（L1-L80）
- `vllm/distributed/kv_transfer/kv_connector/v1/nixl_connector.py`（头部 L1-L70）
- `vllm/distributed/kv_transfer/kv_connector/v1/{example,mooncake,offloading,lmcache}_connector.py`、`moriio/moriio_connector.py`（头部/类定义 grep）
- `vllm/distributed/kv_transfer/kv_connector/v1/metrics.py`（L109-L160）
- `examples/online_serving/disaggregated_prefill.sh`（全文）
- `examples/online_serving/disaggregated_serving/README.md`（全文）、`disagg_proxy_demo.py`（L1-L100）
- `benchmarks/disagg_benchmarks/disagg_prefill_proxy_server.py`（头部 L1-L80）
- `tests/v1/kv_connector/nixl_integration/toy_proxy_server.py`（L1-L60 + 路由 grep）
- `requirements/kv_connectors.txt`（全文）
- `LICENSE`（头部）；递归 tree 查 SharedStorageConnector（0 命中）、docs 许可文件（无）
- `docs/generated/metrics`（404，构建期生成）

**vLLM-Ascend @ 52d4acfa51fb868823d1070b81cbd2d97e9e4696**：
- `docs/source/user_guide/support_matrix/supported_features.md`（全文）
- `docs/source/developer_guide/feature_guide/disaggregated_prefill.md`（全文）
- `docs/source/tutorials/pd_disaggregation_mooncake_single_node.md`（L1-L90 + 全文 grep）
- `examples/disaggregated_prefill_v1/mooncake_connector_deployment_guide.md`（头部 L1-L60）
- `vllm_ascend/distributed/kv_transfer/kv_p2p/mooncake_connector.py`（类定义 grep）
- 递归 tree：`vllm_ascend/distributed/`、tutorials、examples 清单
- `LICENSE`（头部）

未使用 FetchURL 读网页；行号均来自 gh api 原文件。

## 给正文的建议

**可以写（有固定证据）**：
1. PD 分离的定义、动机（TTFT/ITL 分别调优、尾部 ITL 控制）与「不提升吞吐」的反面声明（A1-A5）。
2. vLLM v0.14.0 的三层抽象、scheduler/worker connector 分工、KVTransferConfig 字段与角色语义、kv_load_failure_policy（B1-B4, B12）。
3. connector 清单以 factory 注册的 10 个为准；文档页 5+1 种用法示例与之并存（B5）；NixlConnector 依赖 nixl>=0.7.1/UCX、kv_role 占位语义（B7-B8）。
4. 流量分配在上游是外部代理职责，现有代理为 toy/benchmark 性质、轮询调度（B9）；生产依赖第三方 connector（B10）。
5. Ascend 侧 matrix 原文「Functional, xPyD is supported」、两类 Mooncake connector 的拉/推分工、A2/A3 与 TP 对称性限制（C1-C4）。

**只能标注 unknown/谨慎表述**：
- P2pNcclConnector 的跨机前提；「P2P 要求同机」无证据（B6）。
- PD 分离下的指标归属与 connector 指标清单（B11）。
- Ascend 教程步骤作为 v0.14.0rc1 的可执行处方（版本漂移，C6）。
- 任何吞吐/延迟改善的定量结论——固定来源中没有实测数据。
