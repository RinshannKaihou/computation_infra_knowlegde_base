# 第十八批第四次定向复核

**后续进展：第八次定向复核关闭 C10，累计 16 CLOSED / 0 OPEN，Batch 18 在原定有限文档范围内通过。** 见[第八次复核](batch-18-codex-eighth-recheck.md)；正文仍 draft，基线 not_verified，无实机验证。以下为本次历史输入与判定，不作为最新状态。

复核日期：2026-10-10（Asia/Shanghai；输入身份时钟取得 2026-10-10 01:02:32 UTC）。作者第四轮追加节标注 2026-10-13，保留为作者标签；实际修订输入由下表 SHA-256 识别，不据标签推导执行日期。

**结论：Batch 18 仍暂不通过。本次三项继续 OPEN：C10/C14 为 P2，C12 技术主体已接受，剩余研究记录条件倒置降为 P3；累计 16 项为 13 CLOSED / 3 OPEN，无新增发现 ID。** 此前 13 项 CLOSED 保持。T03-01/T03-02 的有限文档/机制范围通过状态保留，T03-03/T03-04 仍有下列缺口。

约定模型 / effort 为 `gpt-6.1-sol / xhigh`，本会话 Codex 主助手执行，未派发子代理；实际运行标识没有可独立核验的元数据，沿用[初审说明](batch-18-codex-review.md)。依据[路线图](../full-coverage-roadmap.md)、[T03-01–T03-04 验收](../../plans/full-coverage-backlog.yaml)、[写作指南](../authoring-guide.md#7-批次审阅约定)、[归属边界](../../content-outline.md)及 [AGENTS](../../AGENTS.md)。本次只复核修订与影响，不要求补造实机结果。

## 修订输入身份

| 输入 | SHA-256 |
|---|---|
| [互联路径](../../knowledge/03-communication/interconnect-paths.md) | `871bea985ebf8655b3dd827b3a0aac60b2bd1251f4059263f188e8e95bbd7db7` |
| [RDMA 机制](../../knowledge/03-communication/ethernet-ib-roce-rdma.md) | `ad135bfdf7fc801010ae008f2e0039fa9229aa1be47602b5e604f40cd56c32ff` |
| [RDMA 基线](../../knowledge/03-communication/rdma-baseline-and-congestion-triage.md) | `f409bdd266148b7569aa52e4ee791ffd54185400b2baba19f097fbccf6746cd9` |
| [集合通信](../../knowledge/03-communication/collectives-and-rank-progress.md) | `8afb357edfce3cfcb265eda897227049a39b6773eb01b99ff002134a85485a28` |
| [修订映射](batch-18-review-fixes.md) | `b2f88a657331d2e92977cfb32597b9ce32cf351d02ab9e8be2b979b2f6b0c56e` |
| [互联研究记录](batch-18-interconnect-paths-sources.md) | `6f905a305cb592a77d497ba2867abdcff5d01c80a668a63938a653e03b839a4c` |
| [机制研究记录](batch-18-rdma-mechanism-sources.md) | `d9147dbcccfa65c37deb49fd741b7a1b646d3d23a3e575c8962774b382ea666c` |
| [基线研究记录](batch-18-rdma-baseline-sources.md) | `4557ea15824024fe92886e7c3499bae20f7b6cdfad5394fd9e0091515be50905` |
| [集合研究记录](batch-18-collectives-extension-sources.md) | `84d456fdece379526eab749b84e6add77da98ac6e684fa64970216e6e8bf95cd` |
| [来源审计](batch-18-source-audit.md) | `8345db9702ef06620c5c9c496b024a37e01ee38baa57b2b191691d2850cd39d1` |
| [来源登记](../../sources/registry.yaml) | `156cd248f57b53bbba82b23f07283627723fa4ecb69905eb8278fdb6048381d8`（375 项） |

章索引仍为 `9102358b1e7d08455114dda724b0e3bb24ecdb06118eece19b80dc9d003989e5`；互联路径、机制正文和两份研究记录与第三次输入一致。读取现行基线全文、集合修订、作者第四轮追加节和当前登记，核对前轮关闭条件。没有将集合既有 HCCL 全文或所有远端链接声明为本轮重新取证。

## 来源复验范围

网页工具未取得 raw 文件；受限网络 curl 初次解析失败，之后以只读网络调用取得两个固定文件，默认 TLS 校验，未执行下载内容。两文件与第三次取得的 SHA 完全一致：

| 本轮重新取得的一次源 | SHA-256 |
|---|---|
| [Megatron token_dispatcher.py@core_v0.19.2](https://github.com/NVIDIA/Megatron-LM/blob/core_v0.19.2/megatron/core/transformer/moe/token_dispatcher.py) | `7af2746153268f5c5f7f03d7a340092541b633fbc8faa10f666d6ddbdf98be0a` |
| [perftest host_validation.c@a31f9ea](https://github.com/linux-rdma/perftest/blob/a31f9ea9df720ee68f941e55f75fec31349fcd35/src/host_validation.c) | `c53f23f73e9a015740bc5990d77e18566cc4a86e6fc88e75edcdc33f1110a199` |

本轮重读第三次已取得的 ECN/Flow Control canonical、同 tag `moe_utils.py`、固定 `host_validation.h`/`perftest_resources.c`，以及前轮 perftest 参数实现。沿用[第三次报告](batch-18-codex-third-recheck.md#独立来源复验)的精确链接和 SHA，不称这些文件本轮重新抓取。原文和临时日志不入库，无新增来源 ID。

## C12 — P3，OPEN：技术主体已接受，研究记录失败条件倒置

位置：[基线文](../../knowledge/03-communication/rdma-baseline-and-congestion-triage.md) L114、129–134、142；[基线研究记录](batch-18-rdma-baseline-sources.md) L40。

接受有限 host 后端的覆盖设计：`chunks_validated` 的实际累计是 `work_items_processed` 操作数，BW 报告 `iters` 在迭代模式已乘 QP 数；marker 的 `skipped_steps` 单独与同设计 G0 带比较，不再与操作数分母混除。`ops_per_chunk=validation_chunk_size` 与 `chunk_bytes=ops_per_chunk×payload_size` 已列出，host 的 queue/stale 零值不再与其他后端相加。

门禁要求 errors 为零且验证量为正，初始化/停止失败、WARNING/no data validated、缺分母均停止并拒绝作为健康/G0；G0 也受同一有效性规则约束。源码 [host 累计 L1127–1156](https://github.com/linux-rdma/perftest/blob/a31f9ea9df720ee68f941e55f75fec31349fcd35/src/host_validation.c#L1127-L1156)、[marker/操作/字节 L600–602/L681–695](https://github.com/linux-rdma/perftest/blob/a31f9ea9df720ee68f941e55f75fec31349fcd35/src/host_validation.c#L600-L695)、[配置 L7297–7307](https://github.com/linux-rdma/perftest/blob/a31f9ea9df720ee68f941e55f75fec31349fcd35/src/perftest_resources.c#L7297-L7307)及[失败分支 L7339–7363](https://github.com/linux-rdma/perftest/blob/a31f9ea9df720ee68f941e55f75fec31349fcd35/src/perftest_resources.c#L7339-L7363)支持这些修订；[BW 计数 L4802–4828](https://github.com/linux-rdma/perftest/blob/a31f9ea9df720ee68f941e55f75fec31349fcd35/src/perftest_parameters.c#L4802-L4828)支持分母粒度。

接受范围限文档设计与字段核对。该比值比较 host 实现报告的检查工作量，不能单凭它证明每个原始操作或每个字节均已可靠检查；正文已保留 errors=0 仅说明已检查部分及 races/retries 的同期记录。G0 仍待实际有效轮建立，device 字段未映射继续 unknown，不将其纳入已通过门禁。未执行校验或评价实测覆盖水平。

最终一致性核对发现第四轮研究记录 L40 写的是“`chunks_validated>0` 即 no data validated FAILURE”，与正文和源码的 **`chunks_validated==0` 才失败** 相反。作者本轮用户说明写的是正确条件，这一矛盾位于现行研究追加节，不是已注明的历史状态。门禁技术主体已修正，故剩余问题降为 P3 并沿用 C12，不新增 ID。

剩余关闭条件仅为把该研究记录失败条件改成 `==0`，与正文及固定资源实现 L7360–7363 一致。下一轮只需定向核对这一处同步，不要求重新设计 host 门禁、验证 device 分支或提供实机结果。

## C10 — P2，OPEN：采集路径已修正，必交指标字段仍未交齐

位置：[基线文](../../knowledge/03-communication/rdma-baseline-and-congestion-triage.md) L30/34、99–104、143、156。

接受 `enable/<X>`（优先级 0..7）与 `params/<requested attribute>`（属性名）分开，接受 PFC “及更新”配置范围不自动证明后续型号逐字段一致的限定。对应 [ECN 的 Enabling ECN](https://networking-docs.nvidia.com/mlnxofedswum/24.10-5.1.6.1lts/explicit-congestion-notification-ecn)与 [Flow Control 的配置/ConnectX-4 Counters](https://networking-docs.nvidia.com/mlnxofedswum/24.10-5.1.6.1lts/flow-control)。这些子项本轮已接受，下次不必重复修订。

**L99 的传输重试字段、L102 的 ECN 逐统计字段，以及 H1/verification 的 RoCE 交换机侧统计仍明确未取得。** [T03-03 验收](../../plans/full-coverage-backlog.yaml)要求按版本核对丢包、重试、CQE、ECN/PFC 等指标的单位、方向和累计范围，并为 NIC/交换机准备版本化官方计数器资料。现行表把这些必交部分记 unknown、禁用相关率判据，避免了误判，但没有交付要求的字段语义，故 C10 继续 OPEN。

剩余关闭条件：在一个明确选定的有限文档样板中补齐实际传输重试、ECN 统计和诊断所需交换机字段的精确版本/入口/单位/方向/作用域；若使用标记率，给出同窗、同作用域分子分母及该来源支持的率含义。不能用 validator retries、配置参数或统计范围声明替代实际字段。页内没有字段时应继续如实记缺口并补取对应官方资料，不能据缺口记录宣布此必交项通过。无需现场集群、真实固件结果或实机运行才能完成这项文档取证。

## C14 — P2，OPEN：EP 字节结构已接受，AG 与排序条件仍混淆

位置：[集合文](../../knowledge/03-communication/collectives-and-rank-progress.md) L35、148。

接受非 fused、非 padding 的有限分支：路由后 tokens `[m,H]`、probs `[m]`，dispatch 每对逻辑 payload 分别为 `m_ij·H·b_t` 与 `m_ij·b_p`；两次 A2A 共享 split 向量并分别核算 dtype。tokens/probs shape 来自 [moe_utils L446–467](https://github.com/NVIDIA/Megatron-LM/blob/core_v0.19.2/megatron/core/transformer/moe/moe_utils.py#L446-L467)，dispatch 来自 [dispatcher L698–717](https://github.com/NVIDIA/Megatron-LM/blob/core_v0.19.2/megatron/core/transformer/moe/token_dispatcher.py#L698-L717)。combine 前 RS(TP)、combine A2A 反向 split 及 metadata 不计入这两条 payload 公式均正确。实际路由值、fused/padded 分支和物理总网络字节可继续 unknown，不构成这里的关闭阻碍。

但 L148 现行句为“TP>1 时 dispatch 后接 AG(TP)（`num_local_experts>1`，类工作流 L372–383）”。这把类注释里的 `sort_chunk(if num_local_experts>1)` 条件附到了 AG 上。**实际 `dispatch_postprocess` L734–744 仅按 `tp_size>1` 为 tokens 和 probs 各做一次 AG；L750 才按 `num_local_experts>1` 进入排序。** 例如 TP=2、每 rank 只有一个本地 expert，仍执行这两次 AG，按现行条件读法会漏掉通信。AG 也不只作用于 tokens，probs 同样进入 TP gather。依据：[AG 实际分支 L734–744](https://github.com/NVIDIA/Megatron-LM/blob/core_v0.19.2/megatron/core/transformer/moe/token_dispatcher.py#L734-L744)、[排序分支 L746–750](https://github.com/NVIDIA/Megatron-LM/blob/core_v0.19.2/megatron/core/transformer/moe/token_dispatcher.py#L746-L750)、[类工作流 L376–382](https://github.com/NVIDIA/Megatron-LM/blob/core_v0.19.2/megatron/core/transformer/moe/token_dispatcher.py#L376-L382)。

这是原 C14 的条件映射问题，未新增发现 ID。剩余关闭条件：把 AG 与排序条件分别绑定实际代码——AG(tokens/probs) 条件为 TP>1，sort/unsort 条件为本地 expert 数>1；combine 前 RS 仍限 TP>1。同步正文、当前 source_checked 注记、研究/修订说明和登记定位，避免继续把错误条件记为已核对。也可将已交付映射明确限 TP=1，将未核定 TP>1 子分支记 unknown，但已写出的 TP>1 条件必须准确。无需扩大到全部配置或重新证明已接受的逐对字节公式。

## 状态与交付边界

| 状态 | ID |
|---|---|
| CLOSED（13） | C01、C02、C03、C04、C05、C06、C07、C08、C09、C11、C13、C15、C16 |
| OPEN（3） | C10（P2）、C12（P3）、C14（P2） |

| 任务 | 判定 | 范围 |
|---|---|---|
| T03-01 | 有限文档范围通过，保持 | 不证明真实路径或目标工具版本适用。 |
| T03-02 | 有限机制范围通过，保持 | 不把来源核对升级为运行验证。 |
| T03-03 | 暂不通过 | C10 的版本化必交测量字段仍缺；C12 仅剩研究记录失败条件同步。 |
| T03-04 | 暂不通过 | EP 字节结构已接受；C14 的 TP gather/排序条件尚须修正。 |

本轮只修改复核报告、历史报告最新进展、审计与既有来源 notes；四篇知识正文、作者研究记录、修订映射和索引保持输入，任务/主题覆盖不改为完成。来源仍 375 项，正文仍 draft，基线仍 not_verified；未编译或运行外部源码，无实机验证，Batch 17 工作树保留。

交付核对：`make check` / `make build` 均 PASS（86 篇内容、375 项来源），catalog JSON/Markdown 已重建。六份审阅/审计文件的本地文件链接可解析；16 项状态集合完整互斥，13 CLOSED / 3 OPEN（2 P2、1 P3）。56 个受保护文件 SHA 保持输入，其中包括 32 个 Batch 17/软件栈文件、Batch 18 正文/作者研究记录/修订映射/索引及路线图/任务/约定文件。结构检查与这些守护不替代技术正确性、远端来源语义或实机验证。
