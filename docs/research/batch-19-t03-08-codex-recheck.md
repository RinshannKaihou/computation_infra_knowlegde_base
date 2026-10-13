# 第十九批 T03-08 定向复核

审阅日期：2026-10-13（Asia/Shanghai，以本机日期确认）。输入中的 `2026-10-14` 是作者交付标签，不作为本轮取证日期或文件身份；本轮识别依据为下表 SHA-256。

**结论：本轮 C22 CLOSED；C23–C27 OPEN（5 项 P2）。本批累计 22 CLOSED / 5 OPEN（审阅发现），T03-08 未通过。** C01–C21 沿用既有 CLOSED，不重新审阅。BLOCKED-1（HCCL Test × 目标 CANN/HDK/机型官方交集）仍单列 blocked_on_evidence/open，不计入上述发现数量；T03-06/T03-07 的已交付有限文档/来源范围通过保持，整个 Batch 19 未验收。

约定配置 `gpt-6.1-sol / xhigh` 仅记录为用户约定，不写成已独立确认的执行模型/推理等级。执行者为当前 Codex 主会话，角色是独立审阅者而非作者修订者；无子代理。本轮只写本报告，不代作者修订，不新增发现 ID。

**方法限制：远程 curl 实开要求未完成。** 默认 TLS 校验的只读 curl 请求因沙箱内 DNS 解析失败而未取得远程正文；本轮另经允许的 GitHub 连接器和网页阅读器核对关键一次源语义，不把替代通道写成 curl 成功。以下 CLOSED/OPEN 是取得证据范围内的内容判定，不表示用户指定的远程 curl 方法已全部满足。

## 输入与复核范围

| 输入 | SHA-256 |
|---|---|
| [T03-08 正文](../../knowledge/03-communication/bandwidth-degradation-triage.md)（procedure / draft） | `9db1e258654e433481b23c328cc34c8c8441040b6f66061f85aa7ab8662cd209` |
| [作者来源记录](batch-19-t03-08-sources.md) | `2bbf21dc81d15c1357e5b9874a39cb12f7a4738234309b5df503341fc71e4e5b` |
| [修订映射](batch-19-review-fixes.md) | `4fb637a44c4351321ff9c597b014a0c678a3e835664ffb577fa7ba686e7148c9` |
| [加法初审报告](batch-19-t03-08-codex-review.md)（C22–C27 关闭条件权威来源） | `a037c2be9116bce802617a2de0c3e2169fe16bd9199443d463cbbd36722f9a7f` |
| [任务验收](../../plans/full-coverage-backlog.yaml)（T03-08 acceptance 1–4） | `121826a4d499273e7f6a00735e0a53931eef5c097bd66ab6b2425fdbc36ddfe0` |
| [来源登记](../../sources/registry.yaml)（实数 389 项；末尾为 #2409/#814/#209） | `a3dd8247e971888c958d8e43fb1415b274c40f18ba4465367c598b070ce2aaad` |

判定按初审 L49–100 的逐项关闭条件，不以修订映射的“已删除”“已分列”等自述代替正文证据。当前映射的 T03-08 内容位于 L97–104；该输入没有另一个独立标题的“T03-08 第二轮 C22–C27”节，不凭任务措辞推造额外修订轮次。

必要依赖仅用于核对当前引用和字段契约：[T03-07 基线口径](../../knowledge/03-communication/bandwidth-baselines.md)、[T03-03 RDMA 诊断](../../knowledge/03-communication/rdma-baseline-and-congestion-triage.md)、[T03-05 RCCL 档案](../../knowledge/03-communication/rccl-runtime-and-verification.md)及[T03-06 通信库对照](../../knowledge/03-communication/communication-library-profiles.md)。不重新判断这些条目的既有发现或硬件适用性。

## 一次源取证与角色

远程请求使用 `curl --location --fail --silent --show-error --connect-timeout ... --max-time ...`，没有 `-k/--insecure`、关闭校验、修改配置或写远端的操作。GitHub API 的 #2409/#814/#209 body 与 comments，以及 NCCL env 请求均返回 curl exit 6、HTTP 000、下载 0 字节；另外直接请求 #2409 深度评论网页、#814 网页和 env 参数锚点，结果相同（`Could not resolve host`）。HTTP 000 不是上游 HTTP 状态，也不能据此判页面失效。

GitHub 连接器取得 #2409 body 和 4 条评论、#814 body 和 6 条评论；#2409 深度评论另用精确 comment API 读取，避免长输出遮蔽关键表格。#814 同时用网页正文检查三项被撤销归属；词检索只是辅助，判定依据是实际报告、维护者解释及后续评论的内容。#209 的 TCP 前提、绑定建议另查精确评论。NCCL 2.27.5 env 与 ACS 页通过网页阅读器取得正文；RCCL docs-10.1.0 troubleshooting 本轮阅读器返回 Internal Error，不能算重新实开成功，工具作用的本地依赖只复用既有有限审阅范围。

| 已登记 ID / 本地依赖 | 精确页面或评论与字段 | 本轮获取、语义核对与支持边界 |
|---|---|---|
| `src.nvidia.nccl-issue-2409` | [开帖](https://github.com/NVIDIA/nccl/issues/2409)：Environment、§1、§3/§4 | 连接器 body；环境值与正文 L98 一致。开帖把同 rail perftest 成功解释为 NCCL 侧限制，这是报告者当时假说，不是最终归因。 |
| `src.nvidia.nccl-issue-2409` | [首个粒度跟帖](https://github.com/NVIDIA/nccl/issues/2409#issuecomment-5660150852)：1/8 QP、16/128 KiB 表 | 报告者 Ndministrator；单 QP 128 KiB 为 392.1 Gb/s，该阶段不能与开帖 1 MiB 392.6 Gb/s 合并为同条件。 |
| `src.nvidia.nccl-issue-2409` | [QP/深度跟帖](https://github.com/NVIDIA/nccl/issues/2409#issuecomment-5660232470)：两张测量表和阶段性解释 | 同 mlx5_0、host memory、单向、每点 3 s；默认 tx depth 128。128 KiB 的 1 QP/depth 8 为 293.4，8 QP/depth 8 为 392.1，8 QP/depth 64 为 392.0 Gb/s；depth 1 的约 8.8 us 是推算值。该评论仍在提出 NCCL handoff 假说，不是修后结论。 |
| `src.nvidia.nccl-issue-2409` | [修正回复](https://github.com/NVIDIA/nccl/issues/2409#issuecomment-5673453587)：双因、状态表、ADAPTIVE 复测 | 报告者主动撤回开帖解释；平台侧组合修正及 QP 配置侧修正分列，13.1→29.6、358→456 GB/s 与正文一致。深流水掩盖/浅流水暴露及约 97% 都是报告者解释/估算；不是本库验证或库 release 修复证据。 |
| `src.nvidia.nccl-issue-2409` | [关闭回复](https://github.com/NVIDIA/nccl/issues/2409#issuecomment-5699369631) | stephenmsachs，CONTRIBUTOR，按报告者请求关闭；不是维护者独立复现双因。 |
| `src.nvidia.nccl-issue-814` | [开帖](https://github.com/NVIDIA/nccl/issues/814)及[首个维护者回复](https://github.com/NVIDIA/nccl/issues/814#issuecomment-1493802672) | 6×RTX 4090、PHB/SYS、拓扑 XML、P2P/pairwise 矩阵及 ring 调整未果有原文。sjeaugey 讨论 AMD CPU 上双向/多流交织与流水受影响；没有给出最慢链路决定 ring 吞吐的因果证明，也没有 `--bind-to none` 或 tree 流量解释。 |
| `src.nvidia.nccl-issue-814` | [作者关闭](https://github.com/NVIDIA/nccl/issues/814#issuecomment-1496450442)、[2.23 评论](https://github.com/NVIDIA/nccl/issues/814#issuecomment-2283482549)、[GeForce 澄清](https://github.com/NVIDIA/nccl/issues/814#issuecomment-2825666454) | 作者尚未验证替代 CPU 即关闭；2024-08-12 的 2.23 评论说更积极避让 P2P（并非超出设 `NCCL_P2P_LEVEL=PHB` 的效果）；2025-04-23 的澄清不表示近期 GeForce 支持 P2P。两条不能合成为 RTX 4090 修复/支持结论。 |
| `src.nvidia.nccl-issue-209` | [TCP 开帖](https://github.com/NVIDIA/nccl/issues/209)、[绑定建议](https://github.com/NVIDIA/nccl/issues/209#issuecomment-491475792) | body 明确无 RDMA、NET/Socket；kwen2501 将 `--bind-to none` 作为 socket 驱动线程/绑定的一线检查建议。本轮正文已限定 TCP 个案，不外推 IB；不把建议视为所有配置的验证修复。 |
| `src.nvidia.nccl-user-guide-2.27.5` | [env 的完整变量节](https://docs.nvidia.com/deeplearning/nccl/archives/nccl_2275/user-guide/docs/env.html#nccl-ib-split-data-on-qps)及 Values accepted | 阅读器确认 `NCCL_IB_SPLIT_DATA_ON_QPS` 存在，自 2.18 引入；1 为按消息分摊到多个 QP，0 为逐消息 round-robin；2.20 起默认 0，2.18/2.19 默认 1。正文当前固定的 2.27.5 样板不能被用于证明所有版本默认相同。 |
| `src.nvidia.nccl-user-guide-2.27.5` | [troubleshooting ACS](https://docs.nvidia.com/deeplearning/nccl/archives/nccl_2275/user-guide/docs/troubleshooting.html#pci-access-control-services-acs)、GPU-to-NIC / InfiniBand 节 | 阅读器正文支持 ACS/IOMMU 的配置路径影响、GDR 前提和内存注册限制，不能当作物理错误计数器定义。没有执行页内配置命令。 |
| `communication.bandwidth-baselines`（T03-07，本地依赖，非外部一次源） | [正文 L144–161 跨节点矩阵节](../../knowledge/03-communication/bandwidth-baselines.md) | 正文 L61/L116 相对链接解析到实际文件；另用 curl 的 FILE 读取取得 38,053 字节，SHA 为 `8c2884b63cf7b638c1df2d7de88f5fe9d2923c0d95b025548041aea203574039`，与初审记录身份一致。该节给字段与判据，明确“记录项，非测量值”；FILE 成功不算远程 TLS 实开成功。 |

一次源语义摘要为本轮独立核对，不追记成作者以前已完成。临时 curl 文件只保存在临时目录；失败的远程下载不生成有效证据 SHA，也不拿初审的 HTML/规范化 JSON SHA 冒充本轮新证据。

## B19-C22 — P2 / CLOSED：最小时间窗契约与全面降级已补齐

位置：正文 L61–63；来源记录 L9；修订映射 L99；T03-07 L144–161。对应 acceptance 1。

正文 L63 已明确 run、节点/rank、测试与采样窗起止、日志时钟基准、跨节点对齐依据/不确定度、计数器更新边界及端口/rail 映射。同期增量限同窗同基准或已量化偏差；不具备条件时只留单节点/静态证据。时钟缺失对**所有**依赖跨节点先后/同期关系的路径归属、争用、慢 rank 支路降级，不再只限制慢 rank；设计要求与现场实际取得证据分开登记。

L61 旧简写仍只提慢 rank，但 L63 的明确全面限定已覆盖该范围，不再据该旧简写授权其他跨节点结论。来源记录和 T03-07 都未声称交付实测矩阵。关闭是字段/判定契约已满足，不是时钟方法、遥测可用性或窗口实测已验证；无剩余关闭条件。

## B19-C23 — P2 / OPEN：四分支改类已做，逐支判据仍停留在要求句

位置：正文 L76；来源记录 L10；修订映射 L100；初审关闭条件 L63。对应 acceptance 2。

已接受：ACS/IOMMU/GDR/注册明确移出硬件错误；网络/存储独立观测和 collective、datatype/count/root/rank/次序已加入；缺字段/能力时 unknown、不凭低吞吐判硬件故障的限制已出现。#209 的 TCP/socket 前提和绑定建议与所取一次源一致，登记 ID 确实存在。

仍不足：L76 最后写“每项给最小输入、支持/排除条件与 unknown 条件”，但没有实际给四项逐支的支持/排除门禁。共享干扰列 NIC/交换机计数器和存储后端负载，却未落实同条件隔离轮与背景轮怎样比较、缺哪个输入时不能判争用；调用/消息只列要回链的参数，没有怎样支持/排除变化的比较条件。物理分支列 IB 异步事件、Downed/恢复、LLR/重传，未接通字段来源/适用域，不能仅靠“已核对”四字说明哪些是错误事件、哪些仅是多因响应。既有 T03-03 已区分这些口径，但正文没有把该限定链接到这组新增事件；字段名清单不能代替区分检查。

剩余关闭条件：补四支的实际最小输入、比较对象、支持/排除和 unknown 条件（可精确链接既有判据，不要求现场数值）；为所选错误/链路事件接通含义、作用域及版本来源，未选字段保留 unknown，不把泛称“重传”自动当物理故障。共享 CPU/网络/存储分别具有隔离/背景对照，调用支路回到实际参数/次序记录的同口径比较。#814 错误因果归属另按 C26 处理，不重复新增 ID。

## B19-C24 — P2 / OPEN：停止/恢复纠正，但每轮对照与入口仍未交付

位置：正文 L75–77、L81–92；来源记录 L11；修订映射 L101；初审关闭条件 L73。对应 acceptance 4。

已接受：步骤 9 说明自己是完成判据 2/3 的证据生产环节，步骤 7 待证据齐全再汇总；正确性失败、超时/异步错误、窗口失效与诊断完成出口分开；恢复按保存原值或批准修复配置，不再无条件回默认值；不新增执行授权。

仍不足：步骤 7 的默认下一步仍是结束，新增说明没有明确何种未完成诊断转入步骤 8，只有“8 状态齐全→9”及 9 与 7 的说明。L77 的“每轮列隔离条件、背景负载、路径变量……”仍是待填写的要求，没有给隔离基线、可控背景、单变量、替代端点/rail/路径各轮的变更项、保持项、输入、原生输出与判定。因此不能用末列“每轮输入/判定齐全”认定方案已经可执行。工具分组把 TransferBench 设备间拷贝基准也放进“回放解析”括号，测量与回放/解析未真正逐项归属；“见来源节”也未提供已有 RCCL/HCCL 对照资料的实际入口。

剩余关闭条件：新增明确的 7→8→9→7 流程入口/出口（不要求改旧步骤），为上述各轮给出具体记录/判定契约；未选版本、输入或能力的轮次明确未完成/unknown。把独立测量、日志回放、解析候选和真正端点/rail/transport 替代分列，TransferBench 按设备间拷贝基准归属；接通已有 NCCL/HCCL/RCCL 资料。保留已纠正的失败停止、原值/批准配置恢复与同条件正确性/覆盖复测要求，不要求运行实验。

## B19-C25 — P2 / OPEN：主案例主要边界已收窄，阶段假说与参数定位尚不足

位置：正文 L98–106；来源记录 L12–13；修订映射 L102；初审关闭条件 L85。对应 acceptance 3。

已接受：实际环境值及独立 NCCL/nccl-tests 快照身份与开帖一致；不再把 1 MiB 392.6 与首个跟帖的单 QP/128 KiB 线速说成同条件；单 QP/depth 8 非线速、depth 1 的约 8.8 us 均有原文依据。正文给出完整 `NCCL_IB_SPLIT_DATA_ON_QPS`，约 97% 明确为相对未核验期望的报告者估算，不作验收门槛；perftest 成功仅限所测路径/参数/窗口，普遍“先排除 fabric”规则已去除。报告者平台/配置修正与维护者按请求关闭已区别，不承诺库发布修复版本。

仍不足：L99 虽冠以“开帖假说”，实际只列 perftest 数值，未记录报告者当时的 NCCL 侧限制假说及其被最终回复纠正的关系。L100 将后续两轮跟帖压为一句；`293.4 vs 392.1` 未明确后一值对应 **8 QP/depth 8**，host buffer、单向/同 rail 和深度列身份也没有保留定位。末尾“QP/深度/buffer/阶段必须保留”是要求，不是已经交付这些条件。开帖、粒度跟帖、深度跟帖、修正、关闭没有逐阶段精确评论链接；来源记录 L12–13 仍只给 Issue 首页/“同页”，不足以实现初审要求的分别定位。

剩余关闭条件：补开帖假说内容、后续假说的阶段/角色及最终修正关系；至少把采用的 293.4/392.1 对照列、depth 1 估算的 buffer/方向/rail/深度定位交代清楚，不能暗示是同一单 QP 条件的两个数。分别链接已取到的四条评论与 body，保留已正确的环境、完整变量、反证范围、估算性质与配置修复边界。定位缺口也关联 C27，但本项保留为案例阶段身份的原关闭条件，未新增事实错误 ID。

## B19-C26 — P2 / OPEN：索引已撤销，步骤 8 与登记仍保留最慢链路归属

位置：正文 L76/L107；来源记录 L14；来源登记 L4851；修订映射 L103。对应 acceptance 2/3。

已接受：正文 L107、来源记录 L14 已声明三项无原文支持；`--bind-to none` 在步骤 8 改归有 TCP 边界的 #209。实际拓扑/矩阵、维护者多流解释、作者 ring 调整未果均有依据；2.23 P2P 避让与 GeForce 边界是不同评论，不推导 RTX 4090 通用能力/已验证修复的限制正确。

但正文 L76 仍明确写“**环受最慢链路限制为 #814 个案解释**”；来源登记 L4851 也仍写“**最慢链路决定 ring 吞吐**”。这与 L107/来源记录的“已删除归属”直接冲突，且 #814 原文没有该因果证明。加上“个案”不产生缺失的证据。三项中的 `--bind-to none`/tree 归属已修正，不因此把残留的第三项也算关闭。

剩余关闭条件：真正删除或另给精确一次源支持步骤 8 和登记中的最慢链路因果归属，同步正文索引、来源记录及修订映射；保持 #814 实际观察、维护者推断强度与两条后续边界的区别，不把失败调整、作者关闭或版本避让写成验证修复。

## B19-C27 — P2 / OPEN：表格形式已有，但精确映射、正文入口及状态同步未齐

位置：正文 L34/L60/L74/L77/L116–119；来源记录 L3/L9–19；修订映射 L104。对应 acceptance 1–4 的来源/状态可追溯性。

已接受：来源记录确已改为表格；L9/L19 与 verification L34 已用“字段契约已引用、实测矩阵未交付”，T03-07 引用有效。verification 及来源记录分开作者首轮/本轮与审阅者初审取证，未把审阅取证冒充作者早已完成，也未声称本轮已通过。

仍不足：表格 L10 的 env/ACS/RAS 和事件没有精确 URL/字段定位；L11 的“T03-05/06 有限范围”不是完整登记/内容 ID，Replayer/TransferBench 只有本地 RCCL 档案入口，FaultDiag 未固定来源；L12–14 没有评论 URL；L13 用“同上”而非可独立解析的 ID。unknown 清单仍保留 C1/C2/C3、S4/S5/S6/S7 等无实际定义的代号。正文 L117 仍只指 Batch 09 来源记录，本轮作者记录没有接入，T03-03/05/06 与所选工具资料也未接通到新增检查。

来源记录 L19 已把旧遥测缺口限定为 Batch 09 范围，但正文 L60/L74/L119 仍呈现“本库尚无遥测来源”的当前状态，没有新增历史范围/当前文档可复用而现场能力未证实的注记。正文 L116 的“跨节点矩阵数值口径……T03-07 已交付”也未与 L34 和来源记录的“字段契约、非实测”显式协调；不能由读者自行选一个状态版本。角色分开已经成立，精确来源映射和正文状态同步仍未成立。

剩余关闭条件：将每个实质主张映射到完整登记/内容 ID—精确页面/评论 URL—字段/段落—支持/未覆盖范围，删除或实际定义悬空代号；接入本轮作者记录及 T03-03/05/06/07、已选择的工具资料，未选工具保留候选。新增正文注记同步旧遥测缺口的原批范围、当前可复用文档及现场 unknown，并明确矩阵交付仅字段/判据。verification 如追加后续取证须继续按真实轮次/角色记录，不预写通过，不关闭 BLOCKED-1。

## 已接受内容、状态集合与下一轮范围

| 状态 | ID / 范围 |
|---|---|
| 本轮 CLOSED（1） | C22 |
| 本轮 OPEN（5 P2） | C23、C24、C25、C26、C27 |
| 既有 CLOSED（21；不重开） | C01–C21 |
| 本批累计 | **22 CLOSED / 5 OPEN**（审阅发现） |
| 既有验收子项 OPEN（单列） | BLOCKED-1，blocked_on_evidence |
| T03-08 | **定向复核未通过**；修订后只复核 C23–C27 的剩余关闭条件 |
| T03-06/T03-07 | 已交付有限文档/来源范围通过保持；T03-06 acceptance 5 未验收 |
| 方法边界 | 远程 curl 默认 TLS 实开未完成；本地 FILE 引用核对完成，关键远程语义由替代只读通道核对 |

验收影响：acceptance 1 的字段契约层面可接受；acceptance 2 的逐支判据及残留因果归属、acceptance 3 的阶段/参数定位、acceptance 4 的每轮对照契约/入口仍未满足。C27 的可追溯性继续跨这些项；不将内容结构 PASS 等同技术验收。

## 检查边界与写入范围

- 只新增本报告；不改作者正文、作者记录、修订映射、来源登记、计划、来源审计或索引。工作区已有的其他改动不属于本轮，不恢复、不提交、不创建分支。
- 全程只读取源/比对；不执行 benchmark、MPI/collective、实机采集、配置变更、故障注入或库升级。模型审阅、上游作者测量与本地硬件验证分开；正文仍为 draft / source_checked。
- 不核验 #2409 引用的 nccl-tests#309 期望值，也未获得交换机原始计数器、现场时钟对齐或兼容交集；这些 unknown 不因来源可读而消失。RCCL 本轮阅读失败不等于原文或既有有限审阅失效。
- 为遵守“只写一份报告”，在包含本报告的临时仓库快照运行 `make check` / `make build`，二者均 PASS（88 篇内容 / 389 项来源），构建产物仅写临时快照，原仓库 `build/` 未重建。首次快照未带入既有 `build/catalog.*`，被 `docs/first-fill-status.md` 的两条本地链接检查拦下；补入原有构建文件后重跑通过，该次失败不是作者输入的新增结构错误。
- 报告的 11 处本地链接（10 个不同目标）独立核对均存在。基于取证前的文件 SHA 清单，原有 304 个仓库源文件全部不变，无删除，仅新增本报告；六项任务输入 SHA 与输入表一致。没有修改 `src/kb/`，未执行 `make test`；结构校验和构建不核验远程语义或技术正确性。
