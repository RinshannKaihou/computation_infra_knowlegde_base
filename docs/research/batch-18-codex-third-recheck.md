# 第十八批第三次定向复核

**后续进展：第八次定向复核关闭 C10，累计 16 CLOSED / 0 OPEN，Batch 18 在原定有限文档范围内通过。** 见[第八次复核](batch-18-codex-eighth-recheck.md)；正文仍 draft，基线 not_verified，无实机验证。以下为本次历史输入与判定，不作为最新状态。

复核日期：2026-10-10（Asia/Shanghai；本轮时钟取得 2026-10-09 17:30:11 UTC）。作者第三轮追加节标注 2026-10-12，保留为作者标签；修订输入按下表 SHA-256 识别，不据标签推导执行日期。

**结论：Batch 18 仍暂不通过。本次五项 OPEN 中 C04/C13 转 CLOSED，C10/C12/C14 继续 OPEN；累计 16 项为 13 CLOSED / 3 OPEN，无新增发现 ID。** 此前 11 项 CLOSED 保持。T03-01/T03-02 的有限文档/机制范围通过状态保留，T03-03/T03-04 尚未交齐。

约定模型 / effort 为 `gpt-6.1-sol / xhigh`，本会话 Codex 主助手执行，未派发子代理；实际运行标识没有可独立核验的元数据，沿用[初审说明](batch-18-codex-review.md)。依据[路线图](../full-coverage-roadmap.md)、[T03-01–T03-04 验收](../../plans/full-coverage-backlog.yaml)、[写作指南](../authoring-guide.md#7-批次审阅约定)和 [AGENTS](../../AGENTS.md)。本次是修订后定向复核，不以 HTTP 200、公式标签或 unknown 关闭必交项，不要求填未执行的现场结果。

## 修订输入身份

| 输入 | SHA-256 |
|---|---|
| [互联路径](../../knowledge/03-communication/interconnect-paths.md) | `871bea985ebf8655b3dd827b3a0aac60b2bd1251f4059263f188e8e95bbd7db7` |
| [RDMA 机制](../../knowledge/03-communication/ethernet-ib-roce-rdma.md) | `ad135bfdf7fc801010ae008f2e0039fa9229aa1be47602b5e604f40cd56c32ff` |
| [RDMA 基线](../../knowledge/03-communication/rdma-baseline-and-congestion-triage.md) | `2cb90118495ff02b4d6b327e21446b97dd0269f9d066ca4ea7a738a2435a2a63` |
| [集合通信](../../knowledge/03-communication/collectives-and-rank-progress.md) | `18ba673f112bbf58e86df6d512c8c364418278cb69c2729822c41f08bbe0a700` |
| [修订映射](batch-18-review-fixes.md) | `852c2931abb4eb173d81321e8bbb289957719465c47c08198c4453eb6faf4f3c` |
| [互联研究记录](batch-18-interconnect-paths-sources.md) | `6f905a305cb592a77d497ba2867abdcff5d01c80a668a63938a653e03b839a4c` |
| [机制研究记录](batch-18-rdma-mechanism-sources.md) | `d9147dbcccfa65c37deb49fd741b7a1b646d3d23a3e575c8962774b382ea666c` |
| [基线研究记录](batch-18-rdma-baseline-sources.md) | `9f4c8f0c73d8b448b09c2d6dc39808fb7e43c8946d210e60274819056d184664` |
| [集合研究记录](batch-18-collectives-extension-sources.md) | `15ac30ce0364c86d6c2a4838d02b527bb65e0a59a7c8a6321657082ee8dca725` |
| [来源审计](batch-18-source-audit.md) | `37d11e61d16bf852318448689af7ecc0ebf139c5e190f86bd6a565d99ab49203` |
| [来源登记](../../sources/registry.yaml) | `a28874a1f4751f2b1a35016a259dd7fb1846c66ec4cf00cb1d0114a59fb9ed76`（375 项） |

章索引仍为 `9102358b1e7d08455114dda724b0e3bb24ecdb06118eece19b80dc9d003989e5`。互联路径和机制正文与第二次复核输入完全相同，不重开对应关闭项。读取当前基线全文、集合全文、第三轮研究追加与修订映射，并复查前轮关闭条件；历史 HCCL 全文和其他主题不扩大为本轮全部重新取证。

## 独立来源复验

重新只读取得 OFED 两个精确 canonical 页、Megatron 冻结 dispatcher/utils 与 perftest 固定校验实现；系统 curl 使用默认 TLS 校验，不执行下载内容。网页工具取得 PyTorch 2.8 FSDP Notes；未能取得 raw dispatcher 后改用 curl。GitHub tree API 返回 403，未将它作为成功取证；实际文件按已读源码的 include/调用路径直接取得。复用前轮 rdma-core/perftest 参数文件、Megatron mappings/P2P 文件及 Thakur PDF 文本 p9–10，不称所有远端链接本轮重抓。

| 本轮取得文件 | SHA-256 |
|---|---|
| [OFED ECN canonical](https://networking-docs.nvidia.com/mlnxofedswum/24.10-5.1.6.1lts/explicit-congestion-notification-ecn) | `9f73ad85ddff6b50397eb11ffae2e3524035b7f3179700c2e310b676a7f11979` |
| [OFED Flow Control canonical](https://networking-docs.nvidia.com/mlnxofedswum/24.10-5.1.6.1lts/flow-control) | `3f2659ad47f6f333bc24793afdb598e9a7c7aab578cdb0997f4fa3658051dc6a` |
| [Megatron token_dispatcher.py](https://github.com/NVIDIA/Megatron-LM/blob/core_v0.19.2/megatron/core/transformer/moe/token_dispatcher.py) | `7af2746153268f5c5f7f03d7a340092541b633fbc8faa10f666d6ddbdf98be0a` |
| [Megatron moe_utils.py](https://github.com/NVIDIA/Megatron-LM/blob/core_v0.19.2/megatron/core/transformer/moe/moe_utils.py) | `b20192e71b54ed07b00f9e3d0bbd7daf470cb9ea3dc3037c20f544528e56f14f` |
| [perftest host_validation.h](https://github.com/linux-rdma/perftest/blob/a31f9ea9df720ee68f941e55f75fec31349fcd35/src/host_validation.h) | `ee14b6ea013d0e9e2701e3555b03cd0533a5c82903f0d0710ade89a3d720afe6` |
| [perftest host_validation.c](https://github.com/linux-rdma/perftest/blob/a31f9ea9df720ee68f941e55f75fec31349fcd35/src/host_validation.c) | `c53f23f73e9a015740bc5990d77e18566cc4a86e6fc88e75edcdc33f1110a199` |
| [perftest perftest_resources.c](https://github.com/linux-rdma/perftest/blob/a31f9ea9df720ee68f941e55f75fec31349fcd35/src/perftest_resources.c) | `d2db8a306e22144930d26d33818e19b8c0b62494282740548ff5eea0bf496eb5`（与初审取得文件一致） |

这些文件补充到既有来源条目，不新增 ID；原文、PDF 与临时日志不入库。实现存在、接口语义、可计算模型、配套支持和实机结果分别判断。

## 本轮关闭项

| ID | 判定与限定范围 |
|---|---|
| C04 | **CLOSED**。基线文 L30/34/156 已一致注明 v65.0 本体已选、未完成的是九页完整差分；研究第三轮状态说明把旧待定句限定为历史。固定 man 语义准绳与完整快照差分分开，未用不同组件版本清单声称配套。 |
| C13 | **CLOSED**。集合文 L133 回到 Thakur §4.5 无 ceil 的 reduce 两阶段原式；明确递归结构要求二次幂，并将 §5.1 的非二次幂 p0/额外开销分支分开。ring 等分与 tree ceil 边界保留；其中列出的 allreduce 非二次幂量级也明确标为 allreduce，不当作 reduce 精确式。 |

依据：[Thakur §4.5/§5.1，文件 p9–10](https://fs.hlrs.de/projects/par/rab/publ/HPCA_collectives.pdf)与当前修订正文。未实际运行算法，历史 cutoff 不移植为 NCCL/HCCL 阈值。此前 C01/C02/C03/C05/C06/C07/C08/C09/C11/C15/C16 均保持 CLOSED，无发现要求重开。

## 继续 OPEN 的三项

### C10 — P2，OPEN：配置/统计已分开，必交重试与 ECN 统计字段仍缺

位置：基线文 L30、99–106、143、156。

接受参数/计数/率分类、validator retries 与传输重试分开、ECN/PFC 移到 RoCE、缺率字段时不判停止/恢复、负 delta 进入 unknown，以及 PFC 收发/优先级与 duration 不换秒。这些避免了前轮的错误判读，但 **L99/L102/L156 仍明确传输重试与 ECN 逐统计字段未取得**，交换机侧统计也未交齐。T03-03 验收要求按版本核对这些指标的单位/方向/范围，不能因关掉该判据而关闭必交项。

另有现行采集路径错误：L101 用 `/ecn/{roce_rp,roce_np}/{enable,params}/X` 统一表达。canonical 页 Enabling ECN 区分 `enable/<X>`（X=0..7）与 `params/<requested attribute>`；参数名不是优先级数字 X。须分开入口，不能让读者按 `/params/0` 等不存在的页内示例取配置。Flow Control 又将“Configuring PFC on ConnectX-4 and above”与“ConnectX-4 Counters”分节，H1 的“及更新”配置范围不能自动证明所有后续型号逐项字段一致。

依据：[ECN canonical 的 Enabling ECN](https://networking-docs.nvidia.com/mlnxofedswum/24.10-5.1.6.1lts/explicit-congestion-notification-ecn)、[Flow Control 的 Configuring PFC/Priority Counters](https://networking-docs.nvidia.com/mlnxofedswum/24.10-5.1.6.1lts/flow-control)及 [T03-03 验收](../../plans/full-coverage-backlog.yaml)。本轮接受参考硬件文档已补入，不要求当前真实集群或现场固件结果；指标语义仍需有限样板的来源。

剩余关闭条件：给选定文档样板补实际传输重试计数、ECN 统计和所需交换机指标的版本字段/单位/方向/范围；率给同作用域的分子分母，分开配置入口。PFC 计数声明限已证型号/页内字段，缺失部分继续 unknown；这种诚实缺口记录不等于整个必交指标项已通过。

### C12 — P2，OPEN：聚合已可计算，覆盖门禁混用计数粒度且漏掉无数据失败

位置：基线文 L114–115、129–134。

**接受** BW 5000/latency 1000 的显式设计值、bw_avg 与 peak 分开、三轮 median/[min,max] 的统计层次，以及 host/device 构建和资源条件。覆盖规则 L134 仍不能作为正确的覆盖门禁：

- BW 的报告 `iters` 来自操作数，固定参数实现 L4802 在迭代模式还乘 `num_qps`。host validator 的 `skips` 则来自 marker 跳步：`host_validation.c` L600–602 累加 `delta-1`；一次 marker 对应 `ops_per_chunk` 个操作（resources L7302、host L681–695）。该 chunk 大小按 payload/tx_depth 推导（参数 L1625–1637），不是固定一操作。因此直接 `(skips+stale)/iters` 缺少粒度换算，不能称未校验操作/块的占比。host/GPU 的统计项也须按其实际字段解释，不将不同工作计数直接相加称覆盖率。
- 门禁只要求 errors==0 与丢失比在 G0 带内，没有要求确实检查过数据。固定 `data_validation_stop_and_report` L7360–7363 对 `chunks_validated==0` 明确打印 no data validated 并返回失败。若未检查且计数均为零，现行公式可得比值零；不能据此判健康或把该轮建成 G0。这里是静态失败分支核对，没有构造或执行测试结果。

依据：[host marker 跳步](https://github.com/linux-rdma/perftest/blob/a31f9ea9df720ee68f941e55f75fec31349fcd35/src/host_validation.c#L585-L602)、[一个 marker 的操作数/字节数](https://github.com/linux-rdma/perftest/blob/a31f9ea9df720ee68f941e55f75fec31349fcd35/src/host_validation.c#L681-L695)、[配置中的 ops_per_chunk](https://github.com/linux-rdma/perftest/blob/a31f9ea9df720ee68f941e55f75fec31349fcd35/src/perftest_resources.c#L7297-L7307)、[无数据失败与实际输出字段](https://github.com/linux-rdma/perftest/blob/a31f9ea9df720ee68f941e55f75fec31349fcd35/src/perftest_resources.c#L7360-L7379)、[BW 报告操作数](https://github.com/linux-rdma/perftest/blob/a31f9ea9df720ee68f941e55f75fec31349fcd35/src/perftest_parameters.c#L4802-L4828)。特别注意 `chunks_validated` 是实现输出字段名，[host 的累计赋值](https://github.com/linux-rdma/perftest/blob/a31f9ea9df720ee68f941e55f75fec31349fcd35/src/host_validation.c#L1127-L1154)采用 `work_items_processed`，不能仅按名字推定为物理 chunk 数。

剩余关闭条件：先固定校验后端、实际输出字段与 chunk/操作/字节的换算，选择有依据的同粒度覆盖统计；若只是遗漏代理指标，明确其局限，另给有效校验的门禁。工具初始化/停止失败、WARNING/no data validated、分母缺失或零验证量一律不能进入健康或 G0 基线；G0 也须满足同一有效性门禁。无需规定普适数值阈值或执行硬件测试。

### C14 — P2，OPEN：冻结来源与工作流成立，EP 的字节结构尚未展开

位置：集合文 L144–148 与 verification L35。

**接受** TP 各函数 forward/backward 修正、`_ScatterToSequenceParallelRegion` 移出 all-to-all、sp2hp/hp2sp 两种 shape、FSDP Notes 的 payload/unit/buffer 区分与 PP 条件。独立取得 dispatcher 的 SHA 与作者一致，`ep_group=pg_collection.ep`、`tp_group=pg_collection.expt_tp` 和 dispatch 的两次 A2A 也正确。EP 路由本来就是变量，不要求现场固定 token 数；但 L148 的 `f(路由后 token 数,hidden,dtype)` 仍没有交付可代入的消息表达式，“probs 同结构”不能替代它的 shape/dtype。

同 tag `moe_utils.py` 非 fused `permute` 分支 L423–467 显示：路由后 tokens 为 `[m,H]`，probs 是一维 `[m]`，不是 tokens 的 hidden 宽度张量；两次 A2A 共享 split 向量，但应分别以 token dtype 与 prob dtype 核算。以这条有限分支为例，若 `m_ij` 为 rank i 向 j 的路由行数、H 为 hidden、b_t/b_p 为两张量各自元素字节数，则其**每对逻辑输入 payload**可由源码推导为 `m_ij·H·b_t` 与 `m_ij·b_p`，不能以一条未展开的 f 或同一 dtype 代替。这个表达式不冒充物理网络总字节，也不覆盖 fused/padded 的未核定布局。

流程还有未列的条件步骤：dispatcher L817–826 在 TP>1 时 combine 前做 RS(TP)；L857–862 的 combine A2A 将 dispatch 的 input/output splits 交换。现行表只写 AG(TP)/sort→combine A2A，尚未体现这两个会改变组/输入大小的条件。路由 metadata 通信与 tokens/probs payload 也应明确统计边界；可以选 TP=1 等有限条件，但须声明所选分支。

依据：[同 tag permute 输出](https://github.com/NVIDIA/Megatron-LM/blob/core_v0.19.2/megatron/core/transformer/moe/moe_utils.py#L423-L467)、[dispatch tokens/probs 两次 A2A](https://github.com/NVIDIA/Megatron-LM/blob/core_v0.19.2/megatron/core/transformer/moe/token_dispatcher.py#L698-L719)、[combine 前 RS(TP)](https://github.com/NVIDIA/Megatron-LM/blob/core_v0.19.2/megatron/core/transformer/moe/token_dispatcher.py#L817-L826)、[combine 交换 split](https://github.com/NVIDIA/Megatron-LM/blob/core_v0.19.2/megatron/core/transformer/moe/token_dispatcher.py#L855-L863)。FSDP 有限归纳由[PyTorch 2.8 Notes](https://docs.pytorch.org/docs/2.8/notes/fsdp.html#communication-payload-size)支持，未扩大为所有分片配置的固定网络量。

剩余关闭条件：选明有限 dispatcher/config 分支，给出 tokens/probs 的各自 shape、dtype bytes、每 rank/split 输入输出以及 combine 反向 split；TP>1 的 AG/RS 和 metadata 计量边界分开。具体路由值、未执行组合或未核定 padding 可以继续 unknown，但不能把未展开的 f 记作已核验完整字节公式；同步正文/verification/研究记录和登记的当前核对范围。

## 任务判定与交付边界

| 任务 | 判定 | 当前范围 |
|---|---|---|
| T03-01 | 有限文档范围通过，保持 | C01/C02/C03/C16 关闭；不证明真实互联或目标工具版本可用。 |
| T03-02 | 有限机制范围通过，保持 | 来源版本、verbs 完成/错误与模式条件；T03-03 链接不等于可执行流程已通过。 |
| T03-03 | 暂不通过 | C10 的必交测量字段与采集定位；C12 的覆盖粒度和零验证量门禁。 |
| T03-04 | 暂不通过 | C13 已关闭；C14 的 EP 分支/消息大小仍需可计算表达式。 |

- 本轮只修改复核报告、历史报告最新进展、审计与既有来源定位；不修改四篇知识正文、作者研究记录或修订映射，不调整任务/主题覆盖为完成。
- 来源仍为 375 项，正文仍为 draft，基线仍为 not_verified；无实机验证。Batch 17 文件与本轮知识输入采用 SHA 守护。
- `make check` / `make build` 均 PASS：86 篇内容、375 项来源；catalog JSON/Markdown 已重建。结构通过不关闭以上技术发现，不证明远端内容正确性或硬件适用。
- 下一轮仅需定向复核 C10/C12/C14 及修订影响，已接受的子项不无故重开。

交付核对：16 个 ID 的状态集合完整互斥（13 CLOSED / 3 OPEN），本轮及历史报告的本地文件链接可解析；32 个 Batch 17/软件栈文件、Batch 18 正文/作者研究记录/修订映射/索引结束 SHA 均与本轮输入一致。来源登记只追加已有条目的核对范围，未新增 ID。
