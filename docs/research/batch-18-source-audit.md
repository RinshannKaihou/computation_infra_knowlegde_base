# 第十八批来源与交付记录

**审阅状态（2026-10-10）：第八次定向复核完成，C10 转 CLOSED，累计 16 CLOSED / 0 OPEN，Batch 18 在原定有限文档范围内通过。** 两条 out_of_buffer 入口、per-QP/API 区分、本机标记占比、Cumulus 统计引用与刷新范围及现行注记已修订复验；T03-01–T03-04 的有限文档范围通过。C01 的初审反证已撤销，六行 Supported 都是 `√`；所选目标形态没有实测。详见[第八次复核](batch-18-codex-eighth-recheck.md)，前七次复核与初审保留历史及纠错提示。约定模型 / effort 为 `gpt-6.1-sol / xhigh`，实际运行标识未独立核验，限制见报告。本批为 full-coverage 路线图 Batch 18（T03-01/T03-02/T03-03/T03-04），前置 T01-05（Batch 14）、T01-03（Batch 13）、T02-01（Batch 15）均已有有限范围验收。全部保持 draft；基线仍 not_verified，无 reproduced。

## 本批正文

| 任务 | 正文 | 类型 | 备注 |
|---|---|---|---|
| T03-01 | [节点内、节点间与超节点互联路径参考](../../knowledge/03-communication/interconnect-paths.md) | reference | 新增（DGX H100 与 800T A2/A3 SuperPoD 双样板） |
| T03-02 | [Ethernet、IB、RoCE 与 RDMA 机制](../../knowledge/03-communication/ethernet-ib-roce-rdma.md) | concept | 新增（verbs 主干、完成语义、原语映射） |
| T03-03 | [RDMA 网络基线、路由与拥塞诊断](../../knowledge/03-communication/rdma-baseline-and-congestion-triage.md) | procedure | 新增（独立对照流程，not_verified，待执行） |
| T03-04 | [集合通信与 rank 进度](../../knowledge/03-communication/collectives-and-rank-progress.md) | concept | 修订（加法：原语数据流、代价模型、DP/TP/PP/EP 映射；既有契约未动） |

来源记录：[互联路径](batch-18-interconnect-paths-sources.md)、[RDMA 机制](batch-18-rdma-mechanism-sources.md)、[RDMA 基线](batch-18-rdma-baseline-sources.md)、[集合扩展](batch-18-collectives-extension-sources.md)。任务清单：[plans/full-coverage-backlog.yaml](../../plans/full-coverage-backlog.yaml)。

## 起草时来源变化

新增 26 项登记（340→366），初审新增 8 项（→374），修订轮新增冻结 Megatron 1 项（→375）：T03-01 计 9 项（NVLink/Hopper/H100 产品页、SuperPOD RA 架构与 fabric、nvidia-smi 手册、aclrtGetDevicesTopo、MindCluster 730 亲和原则、HCCL 简介），T03-02 计 10 项（rdma-core v65.0、verbs man 页组、内核 v6.16 IB 文档、OFED RoCE/IB/ECN/流控/Secure Host、GDR 13.4、IBTA 规范存在性），T03-03 计 3 项（perftest 26.07.8、UFM 计数器、Cumulus RoCE），T03-04 计 4 项（Thakur/Patarasuk 论文、Open MPI man、Megatron 指南）。

复用既有登记：dgx-h100-h200-user-guide、atlas-800t-a2-product、nccl-user-guide-2.27.5、mind-cluster-v26.1.1、A3 SuperPoD 用户指南组、lingqu 指南、distributed-2.8、hccl-api、cann-hccl。

## 起草时集成者核对（历史记录）

以下保留起草时的核对记录，不代替独立审阅结论；其中版本绑定、对版状态与远端链接问题按 C04/C15 要求修订。

- 候选 URL 全部 HTTP 200 复核（Cumulus RoCE 页经 Network-Solutions 路径修正）；GitHub blob 偶发 503 未影响本批（引用 raw/文档页）。
- 集成者实开全文复核 2 项：MindCluster 730 亲和原则（HCCS 环与 A2 否定句逐字确认）、NCCL 2.27.5 collectives（六原语语义与 root-is-rank 确认）；其余按取证轮实开记录采信，登记 notes 区分核对深度。
- Cumulus 4.3 与 5.x 二选一、内核 v6.16 沿用、man 页与 v65.0 对版、perftest/rdma-core 行号固定均留待 drafting/审阅确认。

## 起草时待审阅与已知边界（历史记录）

- 初审已执行（15 项发现）；修订映射见 batch-18-review-fixes.md，定向复核待执行。
- 范围注记：`make check` 只检查结构及本地文件链接，不检查远端链接可用性；本轮远端 URL 逐条复核（含 Cumulus 路径修正、NCCL troubleshooting 去 `usage/` 一处 404 修复、OFED canonical 确认、v6.16/Megatron raw 200 确认），旧 HTTP 抽查记录保留为历史，不冒充全量远端可用证明。
- T03-04 的 Megatron latest 未冻结、MPI 规范页码、HCCL 主机返回边界、RCCL 留后批均如实保留。

## 2026-10-09 初审交付

- [初审报告](batch-18-codex-review.md)记录输入 SHA-256、独立取证范围、15 项发现和逐项关闭条件；三篇新文与集合增量未修订，尚无 CLOSED 项。
- 审阅者补登记八项固定文件或精确文档证据（366→374）；原作者登记和历史取证记录保留，固定 ref 取得不等于作者当时已完成对版。来源原文、PDF 与运行日志未镜像到仓库。
- 四任务仍暂不通过：T03-01 API/故障域及图表计划，T03-02 完成机制/模式及设计范围，T03-03 路径/计数器/校验判据，T03-04 有限 p 模型/图及冻结框架映射。来源准确性与必交范围均需修订后由同一审阅者定向复核。
- `make check` / `make build`：均 PASS（86 篇内容、374 项来源），构建目录已重建；结构通过不代表上述发现关闭，不建立硬件兼容或实机验证。
- 未更新本批任务为完成，未升级主题覆盖，未改变知识正文的 draft / verification 状态；模型审阅与硬件验证分开。

## 第一次定向复核交付

- [复核报告](batch-18-codex-recheck.md)以修订输入 SHA-256 记录判定；C01/C02/C07/C08/C09/C11/C15 CLOSED，C03/C04/C05/C06/C10/C12/C13/C14 OPEN，新增 C16 OPEN。四任务仍暂不通过。
- C01 原始与本轮 canonical / :6066 HTML 均为 12307 B、SHA-256 `e0fbe17136873bafe7fac1352eb8fc06b0347df5ebaf556d640025c6a0844f39`；审阅者纠正 Product 内斜杠错读，不归因网页变动，也不要求作者证明训练产品不支持。
- 独立复验 Megatron core_v0.19.2 三文件及实际调用分支、DGX Table 5/6、UFM 指标、nvidia-smi 命令字段、NCCL 远端链接；OFED 另外四页 canonical 也确认 24.10-5.1.6.1lts。HTTP 200 与语义正确分别判断。
- 本轮没有新增来源（375 项）；CANN 登记追加审阅者纠错注记，其余作者修订与 Batch 17 工作树保留。知识正文、作者研究记录、修订映射未由复核者修改，没有实机验证。
- `make check` / `make build`：均 PASS，86 篇内容、375 项来源；本轮报告本地文件链接及 CLOSED/OPEN 总数另行核对通过，不以结构通过关闭 OPEN 项。

## 第二次定向复核交付

- [第二次复核报告](batch-18-codex-rerecheck.md)按修订输入 SHA-256 核对全部九项 OPEN，C03/C05/C06/C16 转 CLOSED，C04/C10/C12/C13/C14 继续 OPEN；此前七项 CLOSED 保持，累计 11 CLOSED / 5 OPEN，无新增发现 ID。
- 接受图例/独立型号片段、发现查询入口、INLINE 发送侧边界、SQ/RQ 通知归属、Slot3 字段摘要、PP shape 条件、完整原语图及部分基线设计修订。剩余为版本状态矛盾、选定 NIC/交换机测量语义、基线统计和覆盖门禁、Rabenseifner 条件、逐调用消息与 EP 证据；unknown 不关闭必交项。
- 本轮重读前轮精确来源文件，新增只读取同一 perftest commit 的参数头文件：WRITE/WRITE_IMM BW 默认 5000，其余默认 1000，已将定位追加既有参数来源条目；无新增来源 ID，仍为 375 项。没有重新宣称全部远端链接已逐条抓取。
- T03-01/T03-02 有限文档/机制范围通过，T03-03/T03-04 暂不通过；未修改任务执行状态、主题覆盖或知识正文。原文、日志不入库，无实机验证，Batch 17 修订保留。
- `make check` / `make build` 均 PASS：86 篇内容、375 项来源；报告链接与 16 项状态集合核对通过。32 个 Batch 17/软件栈文件及 Batch 18 正文/作者研究记录/修订映射/索引 SHA 均保持本轮输入，未进行实机验证。

## 第三次定向复核交付（2026-10-10）

- [第三次复核报告](batch-18-codex-third-recheck.md)按当前文件 SHA 复核五项 OPEN，C04/C13 转 CLOSED，C10/C12/C14 继续 OPEN；累计 13 CLOSED / 3 OPEN，无新增发现 ID。
- 接受现行版本注记、Rabenseifner 无 ceil 及二次幂边界、显式迭代与 BW 聚合、TP 函数阶段、FSDP payload/buffer 与 PP 条件。剩余为传输重试/ECN 等版本化测量字段和采集路径、覆盖统计粒度及无数据失败门禁、EP tokens/probs 字节和 combine 分支；不是要求补造实际路由值或测试结果。
- 只读重抓 OFED ECN/Flow Control canonical、Megatron token_dispatcher/moe_utils、perftest host_validation 与 resources 固定文件；来源 SHA 和具体行见报告，补到既有条目，无新增登记 ID（375 项）。HTTP 获取与语义核对分别记录，GitHub tree API 的失败不冒充成功取证。
- 保留作者正文/研究记录/修订映射与 Batch 17 工作树，不更新任务或主题为完成，无实机验证。`make check` / `make build` 均 PASS（86 篇 / 375 项来源）；报告本地链接、13 CLOSED / 3 OPEN 状态集合及 32 个 Batch 17/软件栈文件和 Batch 18 知识输入的结束 SHA 守护通过。

## 第四次定向复核交付（2026-10-10）

- [第四次复核报告](batch-18-codex-fourth-recheck.md)以当前修订文件 SHA 判定三项 OPEN，C10/C14 继续 P2 OPEN，C12 技术主体已接受、研究记录失败条件倒置降为 P3 OPEN；累计 13 CLOSED / 3 OPEN，无新增发现 ID。
- 接受 ECN 配置双入口/PFC 型号限定、host 操作计数与独立 marker 步比较、零校验量失败和 G0 有效性门禁、EP tokens/probs 各自逐对字节、combine 反向 split 与 metadata 边界。C10 缺版本化传输重试/ECN/交换机统计；C12 研究记录 L40 的 >0 失败须改成 ==0；C14 现行 AG 条件错误地附 `num_local_experts>1`，实际 AG(tokens/probs) 条件为 TP>1，该 expert 条件仅限排序。
- 本轮重抓固定 host_validation.c 和 token_dispatcher.py，SHA 与第三次一致；重读前轮固定实现及 OFED canonical 快照，不声明所有远端链接本轮重抓。既有来源 notes 追加本轮核对范围，来源仍 375 项。
- T03-01/T03-02 有限范围通过保持，T03-03/T03-04 暂不通过。作者正文、研究记录、修订映射、索引与 Batch 17 文件保持输入，未改变任务或主题覆盖状态，无实机验证。
- `make check` / `make build` 均 PASS（86 篇 / 375 项来源）；六份审阅/审计文件的本地链接、13 CLOSED / 3 OPEN 的完整互斥状态集合（2 P2、1 P3）核对通过。56 个受保护文件 SHA 未变，含 32 个 Batch 17/软件栈文件、Batch 18 知识输入及路线图/任务/约定文件。

## 第五次定向复核交付（2026-10-10）

- [第五次复核报告](batch-18-codex-fifth-recheck.md)按修订输入 SHA 复核三项 OPEN，C12/C14 转 CLOSED，C10 继续 P2 OPEN；累计 15 CLOSED / 1 OPEN，无新增发现 ID。
- C12 研究记录已改成零校验量才失败，与正文/固定资源实现一致；C14 AG(tokens/probs) 的 TP>1 条件与本地 expert 数>1 的排序条件已分开，已接受的公式和分支保持。T03-01/T03-02/T03-04 在有限文档范围内通过，T03-03 仍缺必交统计字段。
- 只读重抓 OFED ECN/Flow Control/IB 父页 canonical；前两页与前轮 SHA 一致，IB 父页仅为索引。重读前轮固定 dispatcher/resources，未宣称两份源码或所有远端 URL 本轮重抓；来源 notes 追加已有条目，仍 375 项。
- C10 的取证尝试记录说明了已查范围，但未补齐传输重试、ECN 逐统计和所需交换机字段；研究记录将 dropless_rq 开关与 out_of_buffer 丢包计数混归“非计数语义”，还须纠正。这两部分沿用 C10，不新增 ID，也不要求现场实机结果。
- 本轮不修改作者正文/研究记录/修订映射/索引、独立审计文件、Batch 17 工作树或任务/主题覆盖状态，无实机验证。
- `make check` / `make build` 均 PASS（86 篇 / 375 项来源）；七份审阅/审计文件的本地链接与最新指针、15 CLOSED / 1 OPEN 的完整互斥状态集合核对通过。70 个受保护文件 SHA 未变；375 个来源 ID 与非 notes 字段未变，仅五个既有 notes 追加本轮核对范围。

## 第六次定向复核交付（2026-10-10）

- [第六次复核报告](batch-18-codex-sixth-recheck.md)按修订输入 SHA 复核 C10，接受正文和研究记录将 dropless_rq 功能开关与 out_of_buffer 局部丢包计数拆分，前轮归类修正条件已满足。
- C10 继续 P2 OPEN：传输重试计数、ECN 逐统计字段、所需 RoCE 交换机统计字段仍未交付。页面树/QoS 排查记录不能替代原 T03-03 验收要求；累计保持 15 CLOSED / 1 OPEN，无新增发现 ID。T03-01/T03-02/T03-04 的有限文档通过范围保留。
- 本轮只读取得 OFED 24.10-5.1.6.1lts 的 Flow Control、页面树及 Ethernet/IB 两个不同的 QoS 页。树含 99 个标题，无以 counter/statistic 命名的独立页；这不证明其他章节内部不存在计数语义。源链接与 SHA 见报告，复核定位追加既有 notes，来源仍 375 项。
- 作者正文、研究记录、修订映射、索引、任务/主题覆盖、Batch 17 与独立审计文件保持本轮输入，无实机验证。
- `make check` / `make build` 均 PASS（86 篇 / 375 项来源）；八份审阅/审计文件的本地链接与最新指针、15 CLOSED / 1 OPEN 的完整互斥状态集合核对通过。70 个受保护文件 SHA 未变；375 个来源 ID 与非 notes 字段未变，仅两个既有 notes 追加本轮核对范围。


## 第七次定向复核交付（2026-10-10）

- [第七次复核报告](batch-18-codex-seventh-recheck.md)按输入 SHA 核对 C10；接受新增三项 v6.16 驱动/ABI 登记（375→378）及三类实际字段存在性，不再沿用“无实际字段”的当前缺口表述。累计仍为 15 CLOSED / 1 OPEN，C10 继续 P2 OPEN，无新增发现 ID。
- 两处错误采集映射仍阻碍关闭：mlx5e rx_out_of_buffer 由 ethtool 导出，IB vport 实际名附 vport_ 前缀；per-QP cc_* opcounters 的 RDMA counter/QP 绑定路径不能等同 ib_counters 的 create/read API。需同步正文、H1、研究记录及受影响登记。
- 同 tag 官方 counters.rst 确认 marked/packets 均按 L2 priority，不能仅由 PPCNT 组名判错；marked 是本机因 per-host 拥塞执行的标记，应明确 delta/有效分母和观察点。Cumulus 4.3 官方统计页能支持 netdev 入口，但需补引用及内核汇总/物理统计刷新范围，不能把 v6.16 ABI 写成该交换机实际内核版本。verification 的旧“字段待补”注记也须同步。
- 本轮只读取得三个作者主文件、四个同 tag 的语义/API/ABI 辅助文件及两个 Cumulus 4.3 统计页，均 HTTP 200，SHA 与定位见报告；原文不入库，不编译或执行外部源码。取证定位追加既有来源 notes，来源保持 378 项。
- T03-01/T03-02/T03-04 的有限文档通过范围保持；作者正文、研究记录、修订映射、索引、任务/主题覆盖、Batch 17 与独立审计文件保持本轮输入，无实机验证。
- `make check` / `make build` 均 PASS（86 篇 / 378 项来源）；九份审阅/审计文件的 172 个本地文件链接、最新指针与 15 CLOSED / 1 OPEN 完整互斥状态集合通过。70 个受保护文件 SHA 未变；378 个来源 ID 与非 notes 字段未变，仅五个既有 notes 追加本轮定位与限定。


## 第八次定向复核交付（2026-10-10）

- [第八次复核报告](batch-18-codex-eighth-recheck.md)按输入 SHA 复核 C10，四项修正与现行注记同步已完成，C10 CLOSED；累计 16 CLOSED / 0 OPEN，Batch 18 在原定有限文档范围内通过，无新增阻断项或发现 ID。
- out_of_buffer 的 IB vport/sysfs 与 mlx5e qcounter/ethtool 已拆分；rdma_counter QP 绑定与 ib_counters create/read API 已区分，per-QP 用户态入口待核定且不参与已交付判读；本机标记占比已限定同设备/端口/priority/窗口及有效 delta 分母；Cumulus 两页/通用 ABI 引用、汇总和刷新范围及旧字段待补注记已同步。pause_duration 微秒单位有同 tag 文档依据。
- 五份精确来源本轮只读重抓均 HTTP 200，SHA 与第七次一致；四份同 tag 辅助实现/ABI 快照重读，未写成重新抓取。作者新增 counters.rst 和 Cumulus 两个统计页登记（378→381）；复核不新增来源 ID，仅既有 notes 追加定位与有限关闭范围，原文不入库。
- 具体型号/固件、FW 细则、累计位宽、ASIC 内部和 per-QP 用户态入口继续 unknown，rdma-core 完整九页差分仍未完成；缺字段/不可比窗口的分支仍无法判断。该状态与有限文档审阅通过相容，不建立任意平台/版本组合支持或真实网络健康结论。
- 报告另给非阻断定位提示：cc_rx_ce/cc_rx_cnp/cc_tx_cnp 三字段分在 basic_op_cnts/rdmarx_cnp_op_cnts/rdmatx_cnp_op_cnts，不把 basic_op_cnts 括注当作三者共用同一 cap 条件。明确待核定的 per-QP 分支不因此升级。
- 作者正文、研究记录、修订映射、索引、任务/主题覆盖、Batch 17 与独立审计文件保持本轮输入；全部仍 draft，基线 not_verified，无实机验证。
- `make check` / `make build` 均 PASS（86 篇 / 381 项来源）；十份审阅/审计文件的 187 个本地文件链接、最新指针及 16 CLOSED / 0 OPEN 状态集合通过。70 个受保护文件 SHA 未变，381 个来源 ID 与非 notes 字段未变，仅五个既有 notes 追加本轮定位与有限关闭范围。
