# 第二十七批 T07-07 来源记录

任务：T07-07（补齐 PD connector 前提、指标与失败链；**revise** 既有 `knowledge/07-inference/pd-disaggregation.md`，主题 07.5）。取证轮次：主会话作者角色首轮（2026-10-21；前置 T07-03/T07-06 均已 done）。目标：实际 connector 与前提、KV 身份与失败链、指标归属与实现、三平台对照。

版本线（沿用既有钉扎）：vLLM v0.14.0＝`b17039bc`；vLLM Ascend v0.14.0rc1＝`52d4acfa`；MindIE-LLM＝master@`69e5a5dd`。Mooncake 在 vLLM Ascend 教程中钉 **v0.3.7.post2**（`-DUSE_ASCEND_DIRECT=ON` 源码编译）；NIXL 需求钉 `nixl>=0.7.1`（requirements/kv_connectors.txt）。

## 本轮取回清单（2026-10-21，固定 commit 原文件；SHA-256 前 16 位）

| 文件 | SHA-256 前 16 位 |
|---|---|
| vLLM docs/features/disagg_prefill.md（96 行） | e68ad65fee967a00 |
| vLLM docs/features/nixl_connector_usage.md（183 行） | 675eb4152d415140 |
| vLLM docs/features/mooncake_connector_usage.md（58 行） | d60a7cbfdd3e87be |
| vLLM requirements/kv_connectors.txt | de6fc6c8d01542dc |
| vLLM vllm/distributed/kv_transfer/kv_connector/factory.py（203 行） | 09b87c0e47b618ab |
| vLLM …/kv_connector/v1/base.py（607 行） | 00fc529df6dc944f |
| vLLM …/kv_connector/v1/metrics.py（186 行） | a14f705cfa13ef8f |
| vLLM …/kv_connector/v1/nixl_connector.py | bcf8980a73c23945 |
| vLLM …/kv_connector/v1/mooncake_connector.py | dd7d60072bfd64ba |
| vllm-ascend …/feature_guide/disaggregated_prefill.md（105 行） | b9c9772f7ec08fb9 |
| vllm-ascend …/tutorials/pd_disaggregation_mooncake_single_node.md（277 行） | b0bb305495a53c4b |
| MindIE docs/zh/faq/faq.md（PD 条目，与 T07-05 共用） | 3c4f5db3c425f401 |

## 主张—来源定位表

| 主张 | 登记 ID | 精确位置 | 支持范围 / 未覆盖 |
|---|---|---|---|
| PD 动机与反面声明（上游）：experimental 特性；动机＝TTFT/ITL 分别调优＋控制尾 ITL（chunked prefill 难定最优 chunk 尺寸）；**"Disaggregated prefill DOES NOT improve throughput"** | 扩展 src.vllm.inference-v0-14 | disagg_prefill.md L3–19（既有登记复核） | 该快照口径 |
| 上游 connector 清单：Example、LMCacheConnectorV1（NIXL 传输）、NixlConnector（全异步 send/recv）、P2pNcclConnector、MultiConnector（extra_config. connectors 有序列表组合）、OffloadingConnector（CPU offload，block_size/cpu_bytes_to_use）——6 种；NixlConnector 可指定 backends（如 UCX、GDS） | 扩展 src.vllm.inference-v0-14 | disagg_prefill.md L21–57 | 文档清单；各 connector 支持矩阵未逐个核 |
| NIXL 前提与传输：`uv pip install nixl`（NVIDIA）；版本见 requirements/kv_connectors.txt＝**nixl>=0.7.1**＋lmcache；ROCm 用 RIXL（docker 内置，requirements/kv_connectors_rocm.txt）；非 CUDA 平台源码安装脚本；**UCX 为主默认传输**——UCX_TLS/UCX_NET_DEVICES 配置，**NCCL 环境变量（NCCL_IB_HCA 等）对 NixlConnector 不适用** | 扩展 src.vllm.inference-v0-14 | nixl_connector_usage.md L5–37、kv_connectors.txt | 前提与传输口径 |
| NIXL 侧信道与超时：VLLM_NIXL_SIDE_CHANNEL_PORT（默认 5600，P/D 两侧都要，TP/DP 按 base_port+dp_rank 分配，握手用）；VLLM_NIXL_SIDE_CHANNEL_HOST（跨机）；**VLLM_NIXL_ABORT_REQUEST_TIMEOUT（默认 480s）：请求中止且 D 未读取 KV 时，P 侧超时后释放 KV 块避免无限占用**；kv_role 为占位——实际 P/D 角色由上层 proxy 决定（toy_proxy_server 的 --prefiller-hosts/--decoder-hosts） | 扩展 src.vllm.inference-v0-14 | nixl_connector_usage.md L84–101、L157–165 | 语义与默认值 |
| NIXL 异构 KV 布局（实验）：P 用 HND、D 用 NHD 时 `enable_permute_local_kv:True` | 扩展 src.vllm.inference-v0-14 | nixl_connector_usage.md L167–175 | 实验特性 |
| **NIXL 指标实现**：NixlKVConnectorStats 记录 transfer_duration/post_duration（us→s）、bytes_transferred、num_descriptors、num_failed_transfers、num_failed_notifications；reduce() 输出 Num successful transfers、Avg/P90 xfer time (ms)、Avg/P90 post time (ms)、Avg MB per transfer、Throughput (MB/s)、Avg descriptors——worker 侧采集、可序列化送 logger 进程（KVConnectorStats 框架） | 扩展 src.vllm.inference-v0-14 | nixl_connector.py L2475–2560（Stats 类）；metrics.py L19–107（框架：reset/aggregate/reduce/is_empty＋KVConnectorLogging.observe/log＋KVConnectorPromMetrics 每 engine 注册） | 该实现的字段与单位；**MooncakeConnector 在 b17039bc 无 Stats 实现（grep 0 命中）——Mooncake 传输指标此版本缺位** |
| Mooncake 上游口径：定位＝慢对象存储场景的多级缓存池（DRAM/SSD）＋(GPUDirect) RDMA 零拷贝＋多 NIC；`pip install mooncake-transfer-engine`；P/D 命令样例；proxy 复用 nixl_integration 的 toy proxy（自研 proxy 计划中）；VLLM_MOONCAKE_BOOTSTRAP_PORT 默认 8998（仅 P 侧；TP/DP 端口＝base+dp_rank*tp_size+tp_rank，D 通知 P 用）；VLLM_MOONCAKE_ABORT_REQUEST_TIMEOUT 默认 480s（中止且 D 未通知时 P 释放 KV） | 扩展 src.vllm.inference-v0-14 | mooncake_connector_usage.md 全文（L1–58） | 文档口径 |
| MooncakeConnector 实现结构：MooncakeAgentMetadata/RecvReqMeta/SendBlockMeta 元数据类；Scheduler/Worker 两层；tensor_size_bytes 断言块等长、block_len＝tensor_size//num_blocks；ZMQ sock recv_multipart 队列传递元数据 | 扩展 src.vllm.inference-v0-14 | mooncake_connector.py L64–113（元数据类）、L682–718（块长断言）、L449–552（ZMQ 队列） | 结构级取证；传输引擎调用细节未逐行核 |
| **vLLM Ascend PD 机制（pull/push 两式）**：MooncakeConnector＝D 拉——proxy select_prefiller 转发（do_remote_decode=True、max_completion_tokens=1、min_tokens=1）→P 完成后 request_finished 延迟 KV 释放并回 do_remote_prefill=True →proxy select_decoder →D 置 RequestStatus.WAITING_FOR_REMOTE_KVS、预分配 KV、kv_connector_no_forward 拉远端 KV、通知 P 释放、decode 返回。MooncakeLayerwiseConnector＝P 逐层推——D 先 WAITING_FOR_REMOTE_KVS 并向 metaserver 请求；proxy metaserver 端点 select_prefiller；P 逐层推送完成后释放并通知 D 开始 decode | 扩展 src.ascend.vllm-ascend-v0-14-0rc1 | disaggregated_prefill.md L38–99（两式逐步流程） | 文档口径的请求/状态流 |
| vLLM Ascend PD 教程（单机样板）：Mooncake 源码编译（**钉 v0.3.7.post2**、mpich/dependencies.sh、`cmake -DUSE_ASCEND_DIRECT=ON`、make install、LD_LIBRARY_PATH 指向 site-packages/mooncake）；P/D 两侧环境变量（ASCEND_RT_VISIBLE_DEVICES、HCCL_IF_IP=节点 IP、GLOO/TP/HCCL_SOCKET_IFNAME=网卡名、OMP_*）；教程内 vLLM 版本引用 v0.11.0rc1 落后于本快照（B12 已记，只作步骤形态证据）；多机版链接 docs.vllm.ai ascend tutorials | 扩展 src.ascend.vllm-ascend-v0-14-0rc1 | pd_disaggregation_mooncake_single_node.md L100–141（编译）、L141–201（环境变量）、L60–95（docker） | 教程口径；未运行 |
| MindIE PD 失败链（FAQ）：PD 分离 D 节点 "Pull kv failed"（ERROR 日志＋CANN status_code 含 timeout）＝P→D KV 传输超时，极可能网络质量差；配套 T07-03 已核的 kv_trans_timeout（D 拉 KV 超时，默认 10s）与 kv_link_timeout（通信域建立，默认/建议 1080s，重试至成功或超时退出）；PD 混部 chat 接口劣化条目（A3、精度差异场景） | 扩展 src.ascend.mindie-llm-docs-69e5a5dd | faq.md L270–280；service_parameter_configuration（T07-03 登记） | FAQ＋配置口径；connector 底层协议/完整路径未核（修订轮撤回初稿"不在开源仓"——开源仓已见封装，见正文与 unknown 4） |
| 权重加载与 KV 传输的区分：PD 场景 P/D 两侧仍各自走完整权重加载（[T07-01 交付](../../knowledge/07-inference/model-loading-and-readiness.md)）；KV 传输是请求级增量数据，经 connector 元数据（RecvReqMeta/SendBlockMeta）与块句柄传递，不经模型加载路径 | 本库归纳（依据上述来源＋T07-01 交付） | — | 归纳标注 |

## unknown 清单

1. NIXL/RIXL 库本体（ai-dynamo/nixl、rocm/rixl 仓）未取回——握手协议、UCX 版本兼容矩阵 unknown；Mooncake 引擎（kvcache-ai/Mooncake@v0.3.7.post2）仓未取回，传输引擎 API 未核。
2. MooncakeConnector 在 b17039bc 无 KVConnectorStats 实现（已核 grep 0 命中）——Mooncake 的传输指标在此版本只能靠引擎侧/系统侧观测；vllm_ascend 侧 connector 是否有独立 stats 未核。
3. P2pNcclConnector、LMCacheConnectorV1、OffloadingConnector 的细节未展开（清单级证据）；MultiConnector 组合语义仅文档一句话。
4. MindIE PD 分离（dmi）的底层传输协议与完整路径未核（T07-03 原记"实现与传输路径未从源码核"；修订轮撤回初稿"不在开源仓"的说法——开源仓已见 separate_deployment_engine/TransferOutputHandler 等封装，见正文）；PD 分离部署专页在 docs/ 检索范围内未取得（仅混部页＋FAQ＋Motor 外链未取证）。
5. 请求取消/重试在 proxy 层的完整策略（toy proxy 为轮询演示件，非生产路由）——生产 router 职责仍属 07.6 主题。
6. 未运行任何 PD 部署或传输；全部为文档/源码结构级口径。

## 集成轮结果（2026-10-21 已执行）

- 来源条目维持 542：新增的 MindIE 源码取证按 scope 关联既有条目——separate_deployment_engine.py/kv_transfer_agent.py（Python 路径）记入 src.ascend.mindie-llm-repo-69e5a5dd 关联、transfer_output_handler.cpp（src/ 路径）记入 src.ascend.mindie-llm-src-69e5a5dd notes；Mooncake v0.3.7.post2 与 nixl>=0.7.1 仍为教程/需求内钉扎（两仓本体未取回，实际引用时再登记）。
- 扩展 3 项 notes：src.vllm.inference-v0-14（disagg/nixl/mooncake 三页＋factory/base/metrics/nixl_connector/mooncake_connector 实现＋kv_connectors.txt）、src.ascend.vllm-ascend-v0-14-0rc1（disaggregated_prefill 两式流程＋教程 Mooncake v0.3.7.post2）、src.ascend.mindie-llm-docs-69e5a5dd（FAQ PD 条目）。
- registry 维持 542 sources；T07-07 正文进入撰写轮。

## 初审修订轮（2026-10-21，响应 batch-27-t07-07-codex-review.md 的 C01–C10）

- C01：新增"按 connector 分列的兼容前提"节——NIXL 握手兼容 hash 因子（vLLM/NIXL connector 版本、model、dtype、KV heads/head size/layers、attention backend、cache dtype；TP/block_size/layout 故意不入 hash、由运行时校验，L161–215）、mismatch 失败分支（L1044–1059）、TP/block 条件（utils.py L349–386）、握手校验（L1677–1756）、buffer 分支（L861–894）；平台直接证据分记（NIXL=NVIDIA、RIXL=ROCm 分支，其余 connector 组合 unknown）；上游 Mooncake 兼容条件 unknown 不继承他侧限制表；hash 一致≠权重一致≠组合可运行。
- C02：新增身份链小表——NIXL RemoteMeta/ReqMeta（L218–280）＋P 交接字段（L794–803）＋handle 记入在途列表（L2283–2299）；Mooncake 请求 ID 字典键（L64–110）；toy proxy X-Request-Id（L212–240）；**修正**：Mooncake ZMQ 是跨 P/D worker 的 listener（P worker L512–557、D worker L798–852），非 Scheduler/Worker 层间；无独立稳定 transfer ID 如实注明；HTTP ID→引擎内部 ID 映射 unknown。
- C03：Mooncake 断言范围收窄为本 worker 注册张量的等字节断言（L682–718）；跨端 dtype/shape/layout 一致改写为待满足前提（NIXL 由握手承担）；已见结构检查（请求不存在 warning L565–571、块数量断言 L608–642/NIXL L2220–2224）与未证实检测（错请求/内容损坏/checksum）分列。
- C04：指标表重做为阶段×观察者（起止事件/时间源/实现字段/未决四列）；NIXL 传输由 D 发起 READ（L2283–2299）、telemetry 为 DONE 后实际传输样本（L1973–1991）；完整 prefix 命中只通知不读（L2199–2218）；P 局部首输出与客户端首 payload 区分；D 侧局部 TTFT 不替代端到端。
- C05：NIXL 指标明细分列——数据键/单位（bytes、计数）、CLI 标签（MiB 按 2^20 标 MB、Throughput＝总 MiB/成功 duration 和、descriptors 均值）、Prometheus 实名（4 histogram＋2 失败 counter，L2594–2688）、采样粒度＝每完成 handle、is_empty 只看成功数→纯失败区间 getter 返回 None（L2406–2413，无指标≠无失败）、失败计数不进 reduce。
- C06：失败政策限定"已检测并上报给 scheduler 的 KV 加载失败"（base 默认空集 L358–376；NIXL 上报 L2020–2033；scheduler L1116–1123/L1872–1936）；Mooncake 无该 override、receive_kv 错误记日志 return（L818–836）→终态 unknown；删"只有 fail 才直接失败"排他保证。
- C07：清理责任按阶段分列——调度前取消/未发起（NIXL L757–792、L1908–1970）；480s＝P 端保留块超时非统一兜底（Mooncake 处理时 expire 改无穷 L565–593、清理只遍历过期发送项 L746–764/L856–865——在途失败不保证回收；ZMQ 60000ms 另一类）；正常完成按实现分记（NIXL/Ascend 拉式 D 通知；上游 Mooncake 写入式传输成功后 P 标记）；三层重试分列；进程故障下不保证。
- C08：键名改 kv_connector_extra_config.connectors（L28–32）；状态名按指南原文 WAITING_FOR_REMOTE_KVS（指南 L45/L51，词尾带 S——修订轮更正）；Mooncake usage 引用改 L43–48；toy proxy/XpYd 补近旁锚点；Ascend 限制（L103–105）与编译前提（教程 L100–141）分锚；DFX 保留设计声明性质。
- C09：output-quality-evaluation.md 的 PD 提及处补本页普通链接。
- C10：MindIE 表述收窄为"底层传输实现/协议及完整路径未核"；补已见局部事实（separate_deployment_engine pull_blocks＋CANN 异常 L432–452、远端链接/block 越界检查 L575–603；TransferOutputHandler 请求 ID/取消/失败回调 L24–58；kv_transfer_agent 占位类 L10–17；LLMDataDist 为外部依赖）——占位类不证明全仓缺位；registry notes 同步收窄。
