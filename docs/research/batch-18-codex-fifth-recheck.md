# 第十八批第五次定向复核

**后续进展：第八次定向复核关闭 C10，累计 16 CLOSED / 0 OPEN，Batch 18 在原定有限文档范围内通过。** 见[第八次复核](batch-18-codex-eighth-recheck.md)；正文仍 draft，基线 not_verified，无实机验证。以下为本次历史输入与判定，不作为最新状态。

复核日期：2026-10-10（Asia/Shanghai；输入身份时钟取得 2026-10-10 02:01:23 UTC）。作者第五轮追加节标注 2026-10-14，保留为作者标签；实际修订输入由下表 SHA-256 识别，不据标签推导执行日期。

**结论：Batch 18 仍暂不通过。本次 C12/C14 转 CLOSED，C10 继续 P2 OPEN；累计 16 项为 15 CLOSED / 1 OPEN，无新增发现 ID。** 此前 13 项 CLOSED 保持。T03-01/T03-02 的有限文档/机制范围通过状态保留，T03-04 在已声明的有限映射范围内通过；T03-03 尚缺版本化统计字段。

约定模型 / effort 为 `gpt-6.1-sol / xhigh`，本会话 Codex 主助手执行，未派发子代理；实际运行标识没有可独立核验的元数据，沿用[初审说明](batch-18-codex-review.md)。依据[路线图](../full-coverage-roadmap.md)、[T03-01–T03-04 验收](../../plans/full-coverage-backlog.yaml)、[写作指南](../authoring-guide.md#7-批次审阅约定)、[归属边界](../../content-outline.md)及 [AGENTS](../../AGENTS.md)。本次按[第四次复核关闭条件](batch-18-codex-fourth-recheck.md)核对修订与影响，不扩大为全部配置或实机验证。

## 修订输入身份

| 输入 | SHA-256 |
|---|---|
| [互联路径](../../knowledge/03-communication/interconnect-paths.md) | `871bea985ebf8655b3dd827b3a0aac60b2bd1251f4059263f188e8e95bbd7db7` |
| [RDMA 机制](../../knowledge/03-communication/ethernet-ib-roce-rdma.md) | `ad135bfdf7fc801010ae008f2e0039fa9229aa1be47602b5e604f40cd56c32ff` |
| [RDMA 基线](../../knowledge/03-communication/rdma-baseline-and-congestion-triage.md) | `f409bdd266148b7569aa52e4ee791ffd54185400b2baba19f097fbccf6746cd9` |
| [集合通信](../../knowledge/03-communication/collectives-and-rank-progress.md) | `7b1341c2e6802dc0726d7b9a693bac97d3ad8d29b2642fbc24e8031b6f23aad6` |
| [修订映射](batch-18-review-fixes.md) | `a56dc6c9046dd8540242af0699e84b8b3eef535d63228a292ece269016d3eada` |
| [互联研究记录](batch-18-interconnect-paths-sources.md) | `6f905a305cb592a77d497ba2867abdcff5d01c80a668a63938a653e03b839a4c` |
| [机制研究记录](batch-18-rdma-mechanism-sources.md) | `d9147dbcccfa65c37deb49fd741b7a1b646d3d23a3e575c8962774b382ea666c` |
| [基线研究记录](batch-18-rdma-baseline-sources.md) | `ac4fee33717853ae24c9e46603ca0d30bf54941cc1f34fb9886730b52c57b762` |
| [集合研究记录](batch-18-collectives-extension-sources.md) | `f5ccfed4cbb46c78da875214c732c8d06cb937d5e5d702e8724371b5f2879e47` |
| [来源审计](batch-18-source-audit.md) | `64f78632d49f675157d8e696b3b570c2dfd18f65c0cb0d02aa311d08b4f49526` |
| [来源登记](../../sources/registry.yaml) | `a53454e797eff695f31d7c1e053f6312fe3af17a7c14bc0b1252484a0a16e262`（375 项） |

章索引仍为 `9102358b1e7d08455114dda724b0e3bb24ecdb06118eece19b80dc9d003989e5`。互联路径、机制、基线正文和对应未修订研究记录与第四次输入一致，不重开已接受主体。读取集合修订、verification、两份研究追加、修订映射和登记；既有 HCCL 全文与其他主题未全部重新取证。

## 精确来源复验

网页工具未取得 OFED 页面，随后以默认 TLS 校验只读抓取三个精确 canonical 页。ECN/Flow Control 与第三次抓取字节一致；IB 父页本轮独立取得，仅核对其索引内容，不把子页未读内容算作已核对。

| 本轮重新取得的页面 | 字节数 | SHA-256 |
|---|---:|---|
| [OFED ECN canonical](https://networking-docs.nvidia.com/mlnxofedswum/24.10-5.1.6.1lts/explicit-congestion-notification-ecn) | 66959 | `9f73ad85ddff6b50397eb11ffae2e3524035b7f3179700c2e310b676a7f11979` |
| [OFED Flow Control canonical](https://networking-docs.nvidia.com/mlnxofedswum/24.10-5.1.6.1lts/flow-control) | 90744 | `3f2659ad47f6f333bc24793afdb598e9a7c7aab578cdb0997f4fa3658051dc6a` |
| [OFED InfiniBand Network canonical](https://networking-docs.nvidia.com/mlnxofedswum/24.10-5.1.6.1lts/infiniband-network) | 57634 | `5af8ca90f3091721106abbf5451d799ab1e45c19609049d27cfece9b666476a6` |

复用第四次取得的 `token_dispatcher.py@core_v0.19.2`（SHA `7af2746153268f5c5f7f03d7a340092541b633fbc8faa10f666d6ddbdf98be0a`）和第三次固定 `perftest_resources.c@a31f9ea`（SHA `d2db8a306e22144930d26d33818e19b8c0b62494282740548ff5eea0bf496eb5`），本轮重读对应行，不称两份源码重新抓取。UFM 已接受语义与 EP 已接受公式沿用前轮范围，不声明全量远端 URL 重抓。原文和临时日志不入库，无新增来源 ID。

## 本轮关闭项

| ID | 判定与限定范围 |
|---|---|
| C12 | **CLOSED**。基线研究记录 L40 与第五轮说明 L44 均已改为 `chunks_validated==0` 才触发 no data validated/FAILURE，与正文 L134 及固定资源实现 L7360–7363 一致。基线正文 SHA 未变，第四次已接受的 host 门禁设计保持，不重审 device unknown 或要求实跑。 |
| C14 | **CLOSED**。集合文 L35/L148、集合研究第五轮追加及修订映射已将 AG(tokens/probs) 的 TP>1 条件与 sort 的本地 expert 数>1 条件分开；combine 前 RS 仍为 TP>1。实际源码中 output_split_sizes 为 None 或由 output_splits_tp 转列表，两次 AG 采用同一 split 条件，修订与此一致。登记本轮追加当前复核定位，保留此前第四次 OPEN 的带日期历史。 |

依据：[perftest 无数据失败 L7360–7363](https://github.com/linux-rdma/perftest/blob/a31f9ea9df720ee68f941e55f75fec31349fcd35/src/perftest_resources.c#L7360-L7363)、[dispatcher AG/排序 L734–750](https://github.com/NVIDIA/Megatron-LM/blob/core_v0.19.2/megatron/core/transformer/moe/token_dispatcher.py#L734-L750)、[combine 前 RS L817–826](https://github.com/NVIDIA/Megatron-LM/blob/core_v0.19.2/megatron/core/transformer/moe/token_dispatcher.py#L817-L826)。TP=2 且每 rank 一个本地 expert 时仍有 tokens/probs 两次 AG，这一静态分支已能由现行文字准确表达；没有执行该配置。

C14 关闭限已声明的冻结实现/有限分支及逻辑 payload，具体路由值、fused/padding 布局和物理总通信量继续 unknown；C12 不证明全部原始操作或字节均已可靠检查。此前其他 CLOSED 保持，C01 初审误读已撤销，不重新要求作者证明训练产品不支持。

## C10 — P2，OPEN：取证范围已记录，必交字段仍缺且一处归类需纠正

位置：[基线文](../../knowledge/03-communication/rdma-baseline-and-congestion-triage.md) L30/34、99–104、143、156；[基线研究记录](batch-18-rdma-baseline-sources.md) L45。

接受本轮将取证尝试和缺口明确记录。ECN 静态正文给配置入口与设备/端口/优先级范围，未取得可转录的逐统计字段；“Next Slide” 未附可用的统计表静态载荷。IB 父页是章节链接索引，不能以父页可达证明子页计数器已核对。已接受的 UFM 指标与 PFC 型号限制不重开。

**正文仍未交付版本化的传输重试计数、ECN 逐统计字段和所需 RoCE 交换机统计字段。** [T03-03 验收](../../plans/full-coverage-backlog.yaml)要求按版本核对指标单位、方向、累计范围，并为 NIC/交换机准备官方计数器资料。补取证记录解释了所查入口的局限，不能代替这些必交字段。因此 C10 继续 OPEN；这里没有要求真实集群或现场固件结果，也不将原验收临时扩大为所有硬件/字段。

本轮研究记录还有一处错误归类：L45 将“dropless/out_of_buffer”一并描述为 `ethtool --set-priv-flags` 特性开关、“非计数语义”。实际 [Flow Control 的 Dropless Receive Queue](https://networking-docs.nvidia.com/mlnxofedswum/24.10-5.1.6.1lts/flow-control) 将 **`dropless_rq`** 用作功能开关；随后明确说明，收到包而 RQ 已满、等待后仍未补 WQE 时，**`out_of_buffer` counter 增长表示包已丢弃**。它是丢包计数语义，不是开关，也不是传输重试计数。该节未在此给齐这个字段的具体采集路径、累计范围等，缺失项仍须逐项记录，不能因局部语义存在而冒充完整字段交付。

剩余关闭条件：

- 为一个明确选定的有限文档样板补齐实际传输重试、ECN 统计和诊断所需交换机字段的版本、入口、单位、方向、作用域；使用标记率时给同窗同作用域的分子/分母及来源支持的含义。不能用 QP 配置或 validator retries 替代。
- 纠正研究 L45 的开关/计数归类；将已取得的局部丢包语义与尚缺采集信息分开，不将该页概括为没有计数语义。

未查到当前页面字段只支持“本次已查范围未取得”，不支持全部官方资料均不存在的结论。可继续如实记录 unknown，但原必交项尚未通过；无需重新修订已接受的 ECN 配置双入口、PFC 范围、host 门禁或 EP 公式。

## 状态与交付边界

| 状态 | ID |
|---|---|
| CLOSED（15） | C01、C02、C03、C04、C05、C06、C07、C08、C09、C11、C12、C13、C14、C15、C16 |
| OPEN（1，P2） | C10 |

| 任务 | 判定 | 范围 |
|---|---|---|
| T03-01 | 有限文档范围通过，保持 | 未证明真实互联和目标工具适用。 |
| T03-02 | 有限机制范围通过，保持 | 不升级为运行验证。 |
| T03-03 | 暂不通过 | C10 的版本化必交字段及补取证归类待修订；C12 已关闭。 |
| T03-04 | 有限文档范围通过 | 原语图、假设模型和有限 DP/TP/PP/EP 映射已接受；未知分支不扩充为已验证配置。 |

本轮只修改复核报告、历史报告最新进展、来源审计及既有来源 notes；正文、作者研究记录、修订映射、索引及独立审计文件保持输入。任务/主题覆盖不直接改为完成，来源仍 375 项；正文仍 draft，基线仍 not_verified，无实机验证，Batch 17 工作树保留。

交付核对：`make check` / `make build` 均 PASS（86 篇内容、375 项来源），catalog JSON/Markdown 已重建。七份审阅/审计文件的本地文件链接与最新状态指针核对通过；16 项状态集合完整互斥，15 CLOSED / 1 OPEN。70 个受保护文件 SHA 保持输入；来源登记 375 个 ID、各条目非 notes 字段完全不变，仅五个既有条目的 notes 追加本轮核对范围。结构检查不替代技术正确性、远端语义或硬件验证。
