# 第十八批第二次定向复核

**后续进展：第八次定向复核关闭 C10，累计 16 CLOSED / 0 OPEN，Batch 18 在原定有限文档范围内通过。** 见[第八次复核](batch-18-codex-eighth-recheck.md)；正文仍 draft，基线 not_verified，无实机验证。以下为本次历史输入与判定，不作为最新状态。

复核日期：2026-10-09（Asia/Shanghai，输入身份记录时钟为 15:46:43 UTC）。作者追加节标注 2026-10-11，保留该标签作为作者记录；本次判定以实际修订文件 SHA-256 为准，不据标签推导执行日期。

**结论：Batch 18 仍暂不通过。本次复核 9 项 OPEN，4 项转 CLOSED（C03/C05/C06/C16），5 项继续 OPEN（C04/C10/C12/C13/C14）；此前 7 项 CLOSED 保持关闭，累计 16 项为 11 CLOSED / 5 OPEN，无新增发现 ID。** C01 的审阅者误读已撤销，第二轮纠错注记正确，不重开。T03-01/T03-02 在下述有限文档范围内通过；T03-03/T03-04 尚未交齐。

约定模型 / effort 为 `gpt-6.1-sol / xhigh`，由本会话 Codex 主助手执行，未派发子代理；实际模型与 effort 的运行标识没有可独立核验的元数据，沿用[初审说明](batch-18-codex-review.md)。依据[路线图](../full-coverage-roadmap.md)、[T03-01–T03-04 清单](../../plans/full-coverage-backlog.yaml)、[写作指南](../authoring-guide.md#7-批次审阅约定)和 [AGENTS](../../AGENTS.md)，不以 unknown 关闭必交范围，不以文档版本清单声明软件配套或实机适用。

## 修订输入身份

| 输入 | SHA-256 |
|---|---|
| [互联路径](../../knowledge/03-communication/interconnect-paths.md) | `871bea985ebf8655b3dd827b3a0aac60b2bd1251f4059263f188e8e95bbd7db7` |
| [RDMA 机制](../../knowledge/03-communication/ethernet-ib-roce-rdma.md) | `ad135bfdf7fc801010ae008f2e0039fa9229aa1be47602b5e604f40cd56c32ff` |
| [RDMA 基线](../../knowledge/03-communication/rdma-baseline-and-congestion-triage.md) | `cd52615c0a459b1aae72158409c382619afee95b92ef5b051a2199858eb07e91` |
| [集合通信](../../knowledge/03-communication/collectives-and-rank-progress.md) | `a0f8ac9ca04c4457341f719964b0276d3c065567dd9ae4f3d3f482cd5f565e08` |
| [修订映射](batch-18-review-fixes.md) | `90bee9aaa5c3a6114b27d8225fb61a0958bb043b2b2dd27ceb7a02e57cace9bf` |
| [互联研究记录](batch-18-interconnect-paths-sources.md) | `6f905a305cb592a77d497ba2867abdcff5d01c80a668a63938a653e03b839a4c` |
| [机制研究记录](batch-18-rdma-mechanism-sources.md) | `d9147dbcccfa65c37deb49fd741b7a1b646d3d23a3e575c8962774b382ea666c` |
| [基线研究记录](batch-18-rdma-baseline-sources.md) | `13e559d6f0ad40a45676389a694e9181ba3ce9b2b30ed11fd5abfed4f85b4b3b` |
| [集合研究记录](batch-18-collectives-extension-sources.md) | `46ff48e73eb5e019d90e7abcc5637ffc0daf486cd007a98f2ef684f9fb62e3c2` |
| [来源审计](batch-18-source-audit.md) | `2d1800897dd257e630db76a859e5f2a8296c0991399ae3d757abec063b908d48` |
| [来源登记](../../sources/registry.yaml) | `7ccc62503fdb453668732f8fb79d2db5949953bc023c4af2e8eb14ecd3552d2c`（375 项） |

章索引仍为 `9102358b1e7d08455114dda724b0e3bb24ecdb06118eece19b80dc9d003989e5`。上述为复核输入；审计和登记追加本轮记录后的文件不冒充输入身份。完整读取四篇正文、四份研究记录和修订映射，重点核对原 OPEN 与修订影响；历史 HCCL 原文及其他已通过范围不扩大为本轮重新取证。

## 证据范围

复用本会话前两轮保存的精确来源原文件，重新读取对应段落：DGX Table 5/6、nvidia-smi Topology 与 nvlink 查询小节、UFM/OFED 指标页、固定 rdma-core man 源、perftest README/参数实现、Thakur 文件 p3/p9/p10，以及 Megatron tag 三文件。来源身份与前轮远端获取范围见[第一次复核](batch-18-codex-recheck.md)，本次不称全部远端 URL 重新抓取。

新增只读取得同一 perftest commit 的 [src/perftest_parameters.h](https://github.com/linux-rdma/perftest/blob/a31f9ea9df720ee68f941e55f75fec31349fcd35/src/perftest_parameters.h#L103-L106)，系统 curl 默认 TLS 校验；网页工具未能获取该文件，未关闭 TLS 校验。SHA-256 为 `0f2622cd9e4230e68bb2e315d5532238ed1192be84e87b3c619d92da8b5d6638`。与已取得的参数 `.c`（SHA `78f2e358bbf5960541d6db12ff47b12b2d2171e83ff5ccde4df916e30812ecc2`）联合核对默认值和 BW 统计；登记追加到既有固定参数条目，不新增来源 ID。原文和临时日志不入库，没有编译或运行这些实现。

## 本轮关闭项

| ID | 判定与关闭依据 |
|---|---|
| C03 | **CLOSED**。互联文 L63–73 统一实线/逻辑虚线，未再断言 GPU—CX 直连；L152–169 将 A2/A3 画为独立片段。L108–116 正确分列 topo 矩阵/亲和、本端 status、remote PCI/link 信息，L124–129 的计划采用这些观察点。目标工具版本未固定明确进入无法判断分支，当前只验收来源整理与待执行方法，不认定命令已在目标环境可用；无需为此补造现场驱动版本。 |
| C05 | **CLOSED**。机制文 L83–85、92、104、156、166–168 将 INLINE 例外限于发送 buffer；接收 buffer 没有例外。无 RR/RNR 判据明确限定 RC，并排除 UD/UC 的套用；没有对未取证的其他传输行为补写结论。 |
| C06 | **CLOSED**。机制文 L69–74、83–94 分开发起侧 SQ/send_cq、远端 RQ/recv_cq 与成功 SQ 的 signaled/sq_sig_all 条件；READ 行也限定发起侧通知。mlx5 byte_len 边界与失败 WC 四字段保留，状态机/CQ 主干已恢复。 |
| C16 | **CLOSED**。互联文 L75–90 以八个计算网络端口全量与 Slot/板载摘要分开，不再把 `irdma0/1` 推定为 BlueField/DPU；保留接口字段及卡型号缺证。 |

依据：[nvidia-smi 查询小节](https://docs.nvidia.com/deploy/nvidia-smi/index.html)、[DGX Table 5/6](https://docs.nvidia.com/dgx/dgxh100-user-guide/introduction-to-dgxh100.html)、[post_send 生命周期](https://github.com/linux-rdma/rdma-core/blob/58e40801bfed5a8befc0881594820fa0a0baa4a1/libibverbs/man/ibv_post_send.3#L164-L168)、[post_recv 生命周期](https://github.com/linux-rdma/rdma-core/blob/58e40801bfed5a8befc0881594820fa0a0baa4a1/libibverbs/man/ibv_post_recv.3#L51-L54)、[create_qp 的 SQ/RQ 归属](https://github.com/linux-rdma/rdma-core/blob/58e40801bfed5a8befc0881594820fa0a0baa4a1/libibverbs/man/ibv_create_qp.3#L28-L33)与 [DOCA RC/RNR 边界](https://networking-docs.nvidia.com/doca/archive/3-5-0/rdma-aware-networks-programming-guide)。

此前 C01/C02/C07/C08/C09/C11/C15 保持 CLOSED。C01 当前注记正确承认 Product 合并行包含 training/inference，六行 Supported 为 √；RC 形态例外和实际调用未知保留。C08/C09 随多因口径修改未破坏有限隔离与三层计数器边界；未发现需要重开上述项的回归。

## 继续 OPEN 的五项

### C04 — P2，OPEN：当前版本状态仍有矛盾

位置：基线文 L30、34；基线研究记录的历史节和第二轮追加节。

D-IB/D-RoCE 已选 rdma-core v65.0，固定 perftest、内核文件与 OFED 文档版本，本项中上述选型动作接受；机制文以固定 man 文件为准绳的范围也已满足。但当前 `verification.notes` L34 仍把 **rdma-core tag** 列为待补，与 L30 的已选 tag 冲突。作者历史研究节可以保留，但正文现行状态须一致，不能让读者无法判断当前版本到底是否选定。NIC/交换机缺口由 C10/C12 追踪，不要求本项证明不同版本可以组成可运行系统。

剩余关闭条件：同步正文现行 verification 和当前修订定位，明确 v65.0 已选及用途，留下真实未完成的工具/硬件字段；历史节标为当时状态，不把尚未完成的完整差分写成已完成。

### C10 — P2，OPEN：新增的是参数/事件入口，必交测量指标仍未核定

位置：基线文 L30、75、94、131。

Packets 包数、Constraint 多因、Normalized 仅 UFM 显示口径均接受。L94 将“QP 超时/重试参数”“CQE 错误入口”“ECN/PFC 配置快照”并列为指标，却没有给出重试计数、ECN 标记率和 PFC 各指标的实际字段、单位、方向及累积范围。**配置参数不等于事件计数，也不等于标记率**。特别是把 ECN 标记率/PFC prio 计数器统称经 OFED sysfs 参数取得，没有支持这个合并采集口径；所引流控页的 ConnectX-4 Priority Counters 是 `ethtool -S` 入口，ECN 页区分配置和统计。L94 把 ECN/PFC 放入“IB 分支”也应改为对应的 RoCE 分支。

L30/94/144 明确 NIC/固件/交换机逐项语义仍 unknown，符合诚实记录，但未交齐 T03-03 的版本化指标要求；同窗快照相减不能自动解决同一窗口内的回绕或重置。没有字段/分母/窗口就不能判读 L131 的“ECN 标记率突变”，也不能把 validator 的 retries 当成传输重试。

依据：[OFED ECN 的 Enabling ECN、参数与统计范围](https://networking-docs.nvidia.com/mlnxofedswum/24.10-5.1.6.1lts/explicit-congestion-notification-ecn)、[Flow Control 的 Priority Counters/ConnectX-4](https://networking-docs.nvidia.com/mlnxofedswum/24.10-5.1.6.1lts/flow-control)、[UFM 指标](https://networking-docs.nvidia.com/ufmsdnappswum/41815/infiniband-port-counters)。本项只是文档级样板核对，不要求真实采集结果。

剩余关闭条件：为有限 NIC/交换机样板逐项登记实际测量字段与版本页，分开重试参数、WC status、计数、率和配置；给率的分子/分母及同窗单位，PFC 分收发/优先级，明确重置/回绕处理或无法比较分支。把适用 IB/RoCE 分支写对，缺字段的停止/恢复门槛维持无法判断。

### C12 — P2，OPEN：设计值已补，但迭代默认与基线统计仍不能照表核算

位置：基线文 L30、102–103、119–122。

三档消息设计值、host SIMD 重建、CUDA 插件构建/dlopen、扫描/校验分轮和资源隔离已补，接受这些修订。剩余问题如下：

- “迭代默认 1000”沿用 README 概述，实际固定参数实现 L1030–1031 对 BW 的 WRITE/WRITE_IMM 选择 `DEF_ITERS_WB`；同 commit 头文件 L105–106 为 `DEF_ITERS=1000`、`DEF_ITERS_WB=5000`。本流程正包含 `ib_write_bw`，不能称默认统一为 1000。可以把 1000 明确设为作者选择、两端显式固定的设计值，或按测试分列真实默认，需与来源记录同步。
- G0 三轮取 median 得到一个聚合值，G1 却把“G0 同档三轮 median 的 [min,max]”当基线带。latency 单轮有 median；默认 BW 输出为 peak/average，参数实现 L4809、4829–4831 未提供单轮 BW median。须明确三次 BW 的哪个统计量参与 median/min/max，或定义额外重复/原始数据的计算层次，不能从一个 median 得出三点区间。
- “skips/stale 占比高”仍没有占比分母或当前设计的接受规则；记录计数不等于可判读的覆盖门禁。NIC/固件/交换机文档级样板也尚未选定（L30），软件资料清单不替代该硬件范围。

依据：[固定参数选择 L1030–1031](https://github.com/linux-rdma/perftest/blob/a31f9ea9df720ee68f941e55f75fec31349fcd35/src/perftest_parameters.c#L1030-L1031)、[固定默认常量 L105–106](https://github.com/linux-rdma/perftest/blob/a31f9ea9df720ee68f941e55f75fec31349fcd35/src/perftest_parameters.h#L105-L106)、[BW 报告赋值 L4829–4831](https://github.com/linux-rdma/perftest/blob/a31f9ea9df720ee68f941e55f75fec31349fcd35/src/perftest_parameters.c#L4829-L4831)、[README 校验覆盖与竞争](https://github.com/linux-rdma/perftest/blob/a31f9ea9df720ee68f941e55f75fec31349fcd35/README#L472-L490)。

剩余关闭条件：明确文档级硬件/工具样板；把测试类型、明确迭代/时长、每轮原始统计和跨轮聚合规则写成可计算设计，覆盖门禁给可执行规则及不足分支。所有参数/带宽/覆盖阈值只能标设计，不填未执行的结果。

### C13 — P2，OPEN：Rabenseifner 行仍迁移 ceil 且没有完整适用条件

位置：集合文 L130–134；集合研究记录第二轮 C13。

tree 的 ceil、recursive-doubling 二次幂分支及 ring 等分要求已接受。**L133 仍写 `2⌈lg p⌉α`，附“ceil 限本算法两阶段结构”不能提供来源依据或处理非二次幂的额外代价。** Thakur 文件 p9 的 reduce 两阶段式是 `2 lg p α + 2((p−1)/p)nβ + ((p−1)/p)nγ`；p10 §5.1 明确递归结构要求二次幂，非二次幂先缩到较小二次幂并产生额外通信与不同代价。当前行只有“长消息 reduce”，没有具体 p/分块条件，仍可被读作任意 p 的精确模型。

依据：[Thakur §4.5/§5.1，文件 p9–10](https://fs.hlrs.de/projects/par/rab/publ/HPCA_collectives.pdf)。本轮继续承认该式属于 reduce 的两阶段模型，不错误改称 all-reduce；不要求交付所有非二次幂算法。

剩余关闭条件：该行明确二次幂、递归等分/消息及操作前提，采用有依据的 log 精确式；非二次幂另列有证推导或 unknown，不以 ceil 直接推广。同步正文、研究记录与修订映射。

### C14 — P2，OPEN：PP 与图已修，逐调用消息映射及 EP 仍缺证

位置：集合文 L144–148，重点 L146、148。

PP 的 `variable_seq_lengths or mtp_standalone` 分支与 `is_single_shape` 区分正确；四 rank 原语图、send/recv 基本对、逐对变长匹配及取消 in-place 承诺均接受。EP 明示消息字节/路由 OPEN，T03-04 必交项未关闭。

TP 行仍把多个调用合并为“切分张量/量级/按 split 核算”，没有所选调用的明确输入输出维度、dtype 字节及 forward/backward 阶段。更具体地，把 `_ScatterToSequenceParallelRegion` 列为 sp2hp/hp2sp all-to-all 变体不符合冻结实现：其 L289–297 为 forward 本地 first-dim split / backward all-gather；真正 `all_to_all_sp2hp`/`all_to_all_hp2sp` 在 L566–621，给出 `[num_tokens/TP,H] ↔ [num_tokens,H/TP]` 并调用 all-to-all。`copy_to_tensor_model_parallel_region` 也是 forward 返回输入、backward 才约简（L201–218），必须按阶段核算，不能只归到笼统 all-reduce 一行。FSDP 已正确区分 chunk 输入/完整输出，但还需所选样板的分片、dtype、padding 条件来核算，而非泛称“unit 内参数子集”。

依据：[冻结 mappings.py 的 ScatterToSequence 分支](https://github.com/NVIDIA/Megatron-LM/blob/core_v0.19.2/megatron/core/tensor_parallel/mappings.py#L280-L297)、[sp2hp/hp2sp](https://github.com/NVIDIA/Megatron-LM/blob/core_v0.19.2/megatron/core/tensor_parallel/mappings.py#L566-L621)、[copy 的 forward/backward](https://github.com/NVIDIA/Megatron-LM/blob/core_v0.19.2/megatron/core/tensor_parallel/mappings.py#L201-L218)、[PP 实际 shape 分支](https://github.com/NVIDIA/Megatron-LM/blob/core_v0.19.2/megatron/core/pipeline_parallel/p2p_communication.py#L322-L328)、[PyTorch 2.8 FSDP Notes](https://docs.pytorch.org/docs/2.8/notes/fsdp.html)与 [T03-04 验收](../../plans/full-coverage-backlog.yaml)。

剩余关闭条件：纠正 TP 函数/阶段对应，展开有限 DP/TP/PP/EP 样板的 group、具体符号 shape、dtype bytes、每 rank/split 大小与 padding/变长条件，分清 buffer 字节与网络总传输量；补 EP dispatcher 的冻结来源和路由字节，缺证继续 OPEN。不会因 tag 取得或取消可选 in-place 承诺关闭必交映射。

## 任务判定与验证边界

| 任务 | 本次判定 | 范围 |
|---|---|---|
| T03-01 | 有限文档范围通过 | 机型来源、图、联合身份与条件计划；未知 Ascend 边、目标工具版本及作业带宽不升级为已验证。 |
| T03-02 | 有限机制范围通过 | 固定 verbs/完成/错误/模式/隔离说明；外链 T03-03 仍未通过，不据链接声明可执行网络流程。 |
| T03-03 | 暂不通过 | C04/C10/C12：现行版本一致性、选定设备的测量语义、可核算基线与覆盖设计。 |
| T03-04 | 暂不通过 | C13/C14：Rabenseifner 条件、逐调用映射与 EP 必交证据。 |

- `make check` / `make build` 均 PASS：86 篇内容、375 项来源，catalog JSON/Markdown 已重建。结构和本地链接通过不关闭技术发现，也不证明远端内容或硬件正确性。
- 复核者不修改四篇知识正文、四份作者研究记录或修订映射；正文仍为 draft，诊断仍为 not_verified。报告中的有限通过不提升平台兼容、全主题覆盖或硬件验证状态。
- 本轮只交付复核报告、历史报告最新状态、来源审计和既有 perftest 参数来源的补充定位；无新增来源 ID，无实机验证。Batch 17 文件按输入/结束 SHA 比对，不触碰其修订。
- 下一轮只需定向复核五项 OPEN 及修订影响；本次已接受的修订不无故重开。

补充核对：16 个 ID 的 CLOSED/OPEN 集合完整且互斥，本报告本地文件链接均可解析；32 个 Batch 17/软件栈文件的结束 SHA 与本轮输入一致。Batch 18 四篇正文、四份作者研究记录、修订映射及章索引结束 SHA 也均与上表输入一致。
