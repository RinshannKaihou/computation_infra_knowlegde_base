# 第十八批第一次定向复核

**后续进展：第八次定向复核关闭 C10，累计 16 CLOSED / 0 OPEN，Batch 18 在原定有限文档范围内通过。** 见[第八次复核](batch-18-codex-eighth-recheck.md)；正文仍 draft，基线 not_verified，无实机验证。以下为本次历史输入与判定，不作为最新状态。

复核日期：2026-10-09（Asia/Shanghai，时钟取得 14:35:37 UTC）。修订节沿用作者标注的 2026-10-10；本轮以文件 SHA-256 确认输入，不用作者日期标签推导执行时间。

**结论：Batch 18 仍暂不通过。原 15 项中 7 项 CLOSED、8 项 OPEN；新增 B18-C16（P2，OPEN），累计 16 项为 7 CLOSED、9 OPEN。** C01 的初审反证是审阅者错读，已撤销并纠正；不是网页版本变化，也不是作者需要证明训练产品不支持。原有机制、流程和映射缺口不能因补上标题、图或 HTTP 200 自动关闭。

约定模型 / effort 为 `gpt-6.1-sol / xhigh`，本会话 Codex 主助手执行，未派发子代理；实际运行标识没有可独立核验的元数据，口径沿用[初审报告](batch-18-codex-review.md)。依据同一[路线图](../full-coverage-roadmap.md)、[T03-01–T03-04 验收项](../../plans/full-coverage-backlog.yaml)、[写作指南](../authoring-guide.md#7-批次审阅约定)与 [AGENTS](../../AGENTS.md)。未修改知识正文，未运行硬件或网络测试。

## 修订输入身份

| 输入 | SHA-256 |
|---|---|
| [互联路径](../../knowledge/03-communication/interconnect-paths.md) | `baeb7010643badee287705e8075c027b2563ec22d369b65a6d6804f31f3cd7ff` |
| [RDMA 机制](../../knowledge/03-communication/ethernet-ib-roce-rdma.md) | `18cf41451ba6a97bdc4d329d76aa09d7d52615c2d57181e37615467e0d6f221b` |
| [RDMA 基线](../../knowledge/03-communication/rdma-baseline-and-congestion-triage.md) | `a862f8ef9cda0691bd62b1eef4f008cd467d3edb40babf75df6b49686673283d` |
| [集合通信](../../knowledge/03-communication/collectives-and-rank-progress.md) | `5eb18e001deb5cecf4b2b8ce5c98bd27ad6619a91a23cf5eba7c4050bdf6a69e` |
| [修订映射](batch-18-review-fixes.md) | `a53a40411c8a71e9090844aa630078763285b2ab4d00cffce26e8f081c9f271f` |
| [互联研究记录](batch-18-interconnect-paths-sources.md) | `960408605356cb2c1a53859df073e94cc34d219b615d249b9a6d2c5f96e96828` |
| [机制研究记录](batch-18-rdma-mechanism-sources.md) | `cdd1018a25b76c9e21358ab8f68a06869da0e206b5636dae11d815605bb44d72` |
| [基线研究记录](batch-18-rdma-baseline-sources.md) | `10691d4fed053bb9495af35b71bf3306f88be0e8a133ba3a3494f359295e7bdb` |
| [集合研究记录](batch-18-collectives-extension-sources.md) | `03353b025d65ae49de1468f012bac83f7dff09d12e57f7fe8a837b84abb1cace` |
| [来源审计](batch-18-source-audit.md) | `3bca666fd4fa861b19da543ec9e3c2b4a6973a5290d9626838bc8211762bcadd` |
| [来源登记](../../sources/registry.yaml) | `b1736e3a30f80d3b6be215abc8fb06620ac4842a83c1954afef4613f57533f29`（375 项） |

章索引与初审相同：`9102358b1e7d08455114dda724b0e3bb24ecdb06118eece19b80dc9d003989e5`。本轮完整读取四篇修订正文、四份追加记录及修订映射；历史集合通信的 HCCL 原文和已通过范围不重新扩大验收。

## C01 分歧复验与审阅者纠错

网页阅读工具不能打开该地址，先用 Python 抓取遇证书信任链错误，后改用系统 curl（默认 TLS 校验，无关闭校验），重新取得两个精确地址，均 HTTP 200：

- [canonical 静态页](https://www.hiascend.com/doc_center/source/en/CANNCommunityEdition/900/API/runtimeapi/aclcppdevg_03_1895.html)
- [:6066 静态页](https://www.hiascend.com:6066/doc_center/source/en/CANNCommunityEdition/900/API/runtimeapi/aclcppdevg_03_1895.html)

两页均 **12307 B**，SHA-256 均为 `e0fbe17136873bafe7fac1352eb8fc06b0347df5ebaf556d640025c6a0844f39`。更关键的是，本会话初审临时保存的两份原始 HTML 也是同一大小、同一 SHA；不是当前页面改版产生了不同表。

按 `tr/td` 单元格解析，而不是把扁平文本换行当作列边界，Applicability 是六行：Atlas 350 加速卡；A3 训练/推理产品合并行；A2 训练/推理产品合并行；200I/500 A2 推理产品；Atlas 推理产品；Atlas 训练产品。六行 Supported 都是 `√`。斜杠在 **Product** 单元格中，连接 training/inference 两个产品名称，不是 Supported 的否定值。

**初审 C01 把产品列的斜杠错读成 Supported 值，相关反证撤销。** 合并行按原文包含两个名称；不能再以“不是训练单列”作为否定其文档支持声明的理由。产品族声明仍不证明所有具体 SKU、部署形态或现场调用；RC Note 和所选目标形态的未执行边界继续有效。修订 L134–149 的逐行转录正确，计划 A 已以可调用性为条件分支，**C01 CLOSED**。初审正文保留为历史并加纠错提示，来源登记追加审阅者纠错记录。

## 其余独立取证

重新取得并解析 DGX 指南 Table 5/6、nvidia-smi 手册、UFM 4.18.15 指标页、NCCL 2.27.5 正确 troubleshooting URL，以及 Megatron `core_v0.19.2` 三个 raw 文件；HTTP 200 只用于证明获取，源码语义另核对。复用初审的固定 rdma-core/perftest 文件和论文文本/公式核对，不执行原文件。

| Megatron 修订引用文件 | 本轮取得的 SHA-256 |
|---|---|
| [tensor_parallel/mappings.py](https://github.com/NVIDIA/Megatron-LM/blob/core_v0.19.2/megatron/core/tensor_parallel/mappings.py) | `a91d34138309d7873d7d58914f8082c89546b4222183b165c2d001ed41968641` |
| [pipeline_parallel/p2p_communication.py](https://github.com/NVIDIA/Megatron-LM/blob/core_v0.19.2/megatron/core/pipeline_parallel/p2p_communication.py) | `d34aff2655a452e312aa24e93d0576bf7c0c94ca31173ff1b8e5af4e088622c4` |
| [parallel_state.py](https://github.com/NVIDIA/Megatron-LM/blob/core_v0.19.2/megatron/core/parallel_state.py) | `1f6e23a01022c06be3b67f930095898e5032f6ff93695f8da5aae3b5a546dcf0` |

OFED 另外四个入口也重新取得并检查 HTML canonical：IB 索引、ECN、flow-control、Secure Host 均为 `24.10-5.1.6.1lts`。作者“未逐页确认”的历史注记保留；本轮补足审阅者的页面身份确认，不把它冒充作者当时的动作。相关登记已存在，本轮没有新增来源或原文镜像。

## CLOSED 项

| ID | 复核结果与限定范围 |
|---|---|
| C01 | CLOSED，审阅者错读已纠正；正确适用表、RC Note 和条件计划见上文。 |
| C02 | CLOSED，L78–95 八个计算网络端口与模块内 CX 联合身份对照 Table 5/6 正确，L97–103 删除“一张卡两个 OSFP”的错误域。新加 Slot3 类型无依据另记 C16，不重开原 CX 故障域项。 |
| C07 | CLOSED，机制文 L114–124 分列 Cumulus lossless/lossy、Spectrum、ECN/PFC 与传输保证；没有将 lossy 泛化为任意环境的性能保证。 |
| C08 | CLOSED，L50–74 有两幅原创图，L126–144 有有限工作负载/设计比较和 PKey 检查失败的指标样板，L171 有独立流程普通链接；该有限隔离观察不升级为租户/加密方案。图中的完成错误由 C05/C06 继续追踪，链接不等于诊断流程已通过。 |
| C09 | CLOSED，诊断文 L45–56、64–69、104 已把 IB 工具、SM 主备、RoCE L3/GID/模式快照及 driver/NIC/switch 三层分开；不再用 IB 路由工具判断 RoCE。具体设备指标和可执行矩阵未完成的范围仍由 C10/C12 追踪。 |
| C11 | CLOSED，L107–109 已按固定 README 与参数检查正确说明两对互斥、显式/外部/自动优先级、libnuma 和 raw Ethernet 条件，并区分时间戳取样开销与进程上下文切换。 |
| C15 | CLOSED，互联文 L185 正确 URL 重新取得 HTTP 200，集合文 L146–148 H2/段落分开；审计已说明远端检查与 make check 的范围，旧抽查保留为历史。 |

证据：[DGX Table 5/6](https://docs.nvidia.com/dgx/dgxh100-user-guide/introduction-to-dgxh100.html)、[Cumulus 4.3 模式](https://docs.nvidia.com/networking-ethernet-software/cumulus-linux-43/Network-Solutions/RDMA-over-Converged-Ethernet-RoCE/)、[UFM Constraint 指标](https://networking-docs.nvidia.com/ufmsdnappswum/41815/infiniband-port-counters)、[perftest README L376–401](https://github.com/linux-rdma/perftest/blob/a31f9ea9df720ee68f941e55f75fec31349fcd35/README#L376-L401)、[参数检查 L2463–2471](https://github.com/linux-rdma/perftest/blob/a31f9ea9df720ee68f941e55f75fec31349fcd35/src/perftest_parameters.c#L2463-L2471)、[NCCL troubleshooting](https://docs.nvidia.com/deeplearning/nccl/archives/nccl_2275/user-guide/docs/troubleshooting.html)。

## OPEN 项与剩余关闭条件

### C03 — P2，OPEN：图表已补，物理/逻辑边与发现字段仍未准确对应

互联文 L63–72 把 GPU→CX 画成 PCIe 实线，又说 GPU/CX 归属仅是逻辑关联、没有直连证据，图与图例矛盾。A-1 的 A2 和 A3 范围也应拆成独立片段，不能用连续竖线将类型候选集画成物理设备；未公开边可保持 unknown，不要求补造走线。

更直接的问题在 L111–112：`topo -m` 给连接矩阵和 CPU/内存亲和，不是完整 BDF 身份表；`nvlink --status` 给状态及 Active 链路带宽，远端 PCI bus/NVLink ID 是另外的 remote 子命令，不能说此命令取得“两端”。[nvidia-smi 当前手册](https://docs.nvidia.com/deploy/nvidia-smi/index.html)的 Topology 和 Query Nvlink Status/remote node/remote link info 分列这些接口。

剩余条件：有证边与 Table 6 逻辑归属采用一致图例；A2/A3 片段保留各自型号。资产表按实际命令输出列字段、身份连接及缺失处理，引用正确的身份/远端查询入口并先固定目标工具版本。N/A 计划须采用这些准确观察点；不能以发现表目前的字段承诺验收。

### C04 — P2，OPEN：来源版本大部分已对齐，但流程工具仍待定

man7 的入口定位、v6.16 固定文件、perftest 行号和 OFED 实际版本已修；本轮也确认另外四页 canonical。**诊断文 L30、34、138 仍明确 rdma-core 稳定 tag 待定**，却把相应工具列入流程；修订研究记录仍说待定。诚实标注正确，但初审要求固定流程工具 ref 的子项尚未交齐。

剩余条件：在保留的有限诊断样板中选定并核对 rdma-core/诊断工具 ref 和具体页面/文件定位；或者明确哪些仅为候选工具、不能作为当前可执行步骤，并保持对应必交分支未通过。研究记录分清原取证与当前修订状态，不再以“版本对齐完成”覆盖尚待选择的工具。不要通过降为 unknown 关闭整个必交项。

### C05 — P2，OPEN：IMM 四分已修，接收 buffer 的 INLINE 例外及 RNR 范围仍错

机制文 L82 在“远端 CQE/接收 buffer”一格写 buffer 取回 CQE 前不可复用、INLINE 除外。INLINE 例外只允许**本地发送 buffer**在 `ibv_post_send` 返回后复用，不能允许远端接收 buffer 提前复用。L163 又把 SEND 无 RR 一概写为 RNR，同时 L78 容许 UD/UC；RNR 应限定所选可靠连接语义，不能覆盖所有 SEND 传输。

证据：[固定 post_send L164–168](https://github.com/linux-rdma/rdma-core/blob/58e40801bfed5a8befc0881594820fa0a0baa4a1/libibverbs/man/ibv_post_send.3#L164-L168)、[post_recv L51–54](https://github.com/linux-rdma/rdma-core/blob/58e40801bfed5a8befc0881594820fa0a0baa4a1/libibverbs/man/ibv_post_recv.3#L51-L54)、[DOCA 3.5.0 Glossary RNR（RC QP）](https://networking-docs.nvidia.com/doca/archive/3-5-0/rdma-aware-networks-programming-guide)。

剩余条件：分开发送/接收 buffer 生命周期与 SQ/RQ 完成；INLINE 例外只写在发送侧。给无 RR/RNR 分支明确 QP 服务类型和接收资源前提，其余传输不套用 RC 的错误判据；同步图、表、误解和错误映射。

### C06 — P2，OPEN：发送策略与 WRITE 字段已修，却把 signaled 套到接收完成

机制文 L73 明写“远端完成证据：CQE（signaled 前提）”，L72/L85 的 READ 完成仍未限定发起侧通知策略。`IBV_SEND_SIGNALED/sq_sig_all` 是 SQ 发送 WR 的通知配置，不控制远端 RQ 的成功接收 CQE。图这样表述会把合法的未显式 signaled 发送与远端接收完成混为一谈。mlx5 的 byte_len 边界段已满足，不重报该部分。

证据：[固定 create_qp L28–33（send_cq/recv_cq 与 sq_sig_all 的 SQ 范围）](https://github.com/linux-rdma/rdma-core/blob/58e40801bfed5a8befc0881594820fa0a0baa4a1/libibverbs/man/ibv_create_qp.3#L28-L33)、[post_send L140–150](https://github.com/linux-rdma/rdma-core/blob/58e40801bfed5a8befc0881594820fa0a0baa4a1/libibverbs/man/ibv_post_send.3#L140-L150)。

剩余条件：每行明确发起侧 SQ / 远端 RQ、成功/错误状态和各自 CQ；成功 SQ 的逐条通知写清 signaled 条件，成功接收不套该条件。同步 M-2 与四分表，使“仅发起侧有通知机制”和“每次一定产生 CQE”不混用。

### C10 — P2，OPEN：三类判读已修，单位/原因及必交 RoCE 指标仍不完整

诊断文 L79–80 的 Packets 行“同上”继承 Data 行 `octets/4` 的单位，应是 packet 数，不是四字节计数。L86 将 Constraint Error 全部解释为分区/PKey 失败，但 UFM 还包括 FilterRaw、IP version 检查；它不能单独证明 PKey 错。L75 将 reset/窗口留给未选工具，L34/138 仍明确 RoCE 交换机侧逐项语义待补；重试、CQE、ECN/PFC 的单位/方向/范围等必交项尚未完成。零新增仅用于错误列、XmitWait 不换秒、Discards 多因与保存原始证据均已修。

证据：[UFM 4.18.15 的 Packets、Constraint 与 Calculated Counters](https://networking-docs.nvidia.com/ufmsdnappswum/41815/infiniband-port-counters)。

剩余条件：消除跨单位“同上”，分列 packet/byte/tick/event、端口/VL/优先级范围与可能原因；保留 Constraint 的多因。给有限 NIC/交换机样板补重试/CQE/ECN/PFC 指标及同窗 delta、重置/回绕处理；无 tick 时间基准时继续不换算，不能把未核定的 calculated 指标公式当作通用可计算量。

### C12 — P2，OPEN：校验覆盖已修，对照矩阵仍是填参提示

诊断文 L100/111–116 已分开扫描/校验并限定 errors=0 的覆盖范围，符合固定 README。L101 的大小仍是“如 64B/64KB/4MB，drafting 时…”；迭代/时长只有“固定/预定义”，未给当前设计值或选择规则。L30 NIC/固件/交换机未选型，L102/116 只要求声明 host/device 条件，没有给具体 buffer、校验 build/runtime、SIMD/CUDA 依赖和失败/覆盖不足的分支。流程仍不能按现有输入判读有限基线，不要求实际执行，但设计须交齐。

证据：[固定 README L429–459 的 host/CUDA/构建和 runtime 前提](https://github.com/linux-rdma/perftest/blob/a31f9ea9df720ee68f941e55f75fec31349fcd35/README#L429-L459)、[L472–490 校验竞争](https://github.com/linux-rdma/perftest/blob/a31f9ea9df720ee68f941e55f75fec31349fcd35/README#L472-L490)、[T03-03 验收](../../plans/full-coverage-backlog.yaml)。

剩余条件：选一个明确的文档级 IB/RoCE 硬件/工具样板，给当轮输入大小、迭代或时长、统计窗及基线带定义/推导规则；固定 host 与 device 校验分支的依赖、资源隔离和覆盖判据。未知目标环境可以继续为空，但不能代替样板选型与待执行设计。

### C13 — P2，OPEN：ring 精确式已修，非二次幂的精确适用条件仍未交齐

集合文 L130 的 ring 式和推导/近似区分正确，p/n 符号已补。L122 总体说 lg“实现中取 ceil”，L129 却把 Rabenseifner 表的 `lg p` 统一换成 `⌈lg p⌉`，仍未把递归减半/等分式明确限于适用的 p 和分块条件。非二次幂不是把 log 取 ceil 就获得同一精确模型；L128 虽指出另有处理，不能据此把表头“精确代价”推广到该分支。

证据：[Thakur 等 §4.1.1（文件 p3，非二次幂有额外通信）与 §4.5/§5（文件 p9 起）](https://fs.hlrs.de/projects/par/rab/publ/HPCA_collectives.pdf)。本项继续承认 reduce 的两阶段公式有依据，不改称 all-reduce。

剩余条件：逐行明确该等式的 p/分块/消息口径及操作前提；p 为二次幂的式与非二次幂未知或另行推导分开。保留 binomial tree 原文本身支持的 ceil；不要把这一取整规则迁移到其他算法。ring 均分也写明分块条件，不用泛化“实现另有分支”代替条件。

### C14 — P2，OPEN：tag 冻结成立，但 PP 调用解释错误，消息与图的缺口仍在

tag 三文件均已独立取得，DeepSpeed 已删除，all-to-all 转置图正确。**PP L143 把 `is_single_shape` 当成 shape 先行通信/检查是错误的**：固定源码 L131–137 只检查 Python 参数是否是一个 shape；是否真正跨 rank 通信 shape，取决于 L322–328 的 `variable_seq_lengths or mtp_standalone`，否则直接用已有 `tensor_shape`。HTTP 200 或函数存在不能证明已完成该语义核对。

EP L144 明确字节/路由仍 OPEN，因此本项不能关闭。TP/FSDP 的消息栏仍主要是量级或“按签名核算”指令，没有所选调用的输入/输出 shape 与 dtype bytes 核算；变长部分只说 splits/v 后缀，未补逐对匹配。send/recv 的块内是模式文字而非小规模参与者数据流；all-reduce/reduce-scatter 图标题为 n=4 却只画两个输入 rank，也需明确省略或补齐。in-place 行解释两个 API 的输出签名，不是已核对的别名/原地条件；可移除该未交付承诺，不能把签名差异当作 in-place 验收。

证据：[PP 固定文件 L131–137](https://github.com/NVIDIA/Megatron-LM/blob/core_v0.19.2/megatron/core/pipeline_parallel/p2p_communication.py#L131-L137)、[L322–328 的真实 shape 通信分支](https://github.com/NVIDIA/Megatron-LM/blob/core_v0.19.2/megatron/core/pipeline_parallel/p2p_communication.py#L322-L328)、[TP mappings](https://github.com/NVIDIA/Megatron-LM/blob/core_v0.19.2/megatron/core/tensor_parallel/mappings.py)、[T03-04 验收](../../plans/full-coverage-backlog.yaml)。

剩余条件：按实际配置修 PP 分支，至少展开选定 DP/TP/PP/EP 调用的 group、shape、dtype bytes 与 per-rank/split 大小；EP 必交缺证仍 OPEN。补上述数据流/逐对参数与所保留 in-place 的真实条件，同步登记 notes/研究记录/verification，不能将 frozen 路径存在性升级为映射全部 source_checked。

### B18-C16 — P2，新增 OPEN：Slot3 的 RDMA 名被误推为 BlueField/DPU 类型

位置：互联文 L89，新加 Table 5 转录摘要。

该行把 Slot3 写为“BlueField/DPU 类，irdma0/irdma1”。所引 [DGX Table 5](https://docs.nvidia.com/dgx/dgxh100-user-guide/introduction-to-dgxh100.html)只给 Slot3 P1/P2 的 BDF、ens6f0/f1、irdma0/1 等接口身份，组件表只声明 Slot3 双口 100GbE；没有这条 BlueField/DPU 类型证据。不能由 RDMA 设备名推导资产类型或管理面职责，也不在此替作者猜另一个卡型号。

关闭条件：移除无依据类型，保留原表字段；若要补卡型号/职责，取得该机型精确 BOM/组件或接口文档并单独登记定位。区分原表转录、功能归属和方法推断，不称未完整展开的 Slot 摘要为全量转录。

## 任务判定、检查与边界

| 任务 | 判定 | 仍 OPEN 的本轮范围 |
|---|---|---|
| T03-01 | 暂不通过 | C03 的图/发现对应；C16 的新资产类型误推 |
| T03-02 | 暂不通过 | C05/C06 的 buffer、传输和 SQ/RQ 完成边界；C04 流程工具固定关联 |
| T03-03 | 暂不通过 | C04/C10/C12 的工具、指标与可判读矩阵 |
| T03-04 | 暂不通过 | C13 的算法条件、C14 的 PP/消息大小/EP 等 |

- `make check` / `make build`：均 PASS，86 篇内容、375 项来源；构建已生成 catalog JSON/Markdown。仅证明结构和本地文件链接，不证明技术正确性或远端可用性。
- 未改四篇知识正文、四份作者研究记录和修订映射；正文保持 draft，诊断保持 not_verified。没有把任务、主题覆盖或平台兼容升为完成。
- 本轮只修改审阅报告、批次审计和 CANN 来源纠错注记；临时抓取原文和失败日志不入库，无新增来源，计数仍应为 375。
- 不修改 Batch 17 工作树，不进行实机验证。下一轮只复核 OPEN 项及修订引入的必要影响；本轮 CLOSED 项不无故重开。
