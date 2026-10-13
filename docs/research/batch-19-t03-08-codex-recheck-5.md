# 第十九批 T03-08 第五次定向复核

审阅日期：2026-10-13（Asia/Shanghai，本机日期确认）。正文 `updated_at: 2026-10-14` 及部分来源登记日期晚于本轮实际日期，只视为作者交付标签，不作为本轮取证日期或历史执行证明；输入身份以下表 SHA-256 为准。

**结论：C23 CLOSED；C24、C27 仍 OPEN（2 项 P2）。本批累计 25 CLOSED / 2 OPEN（共 27 个审阅发现），T03-08 第五次定向复核未通过。** C01–C22、C25、C26 沿用既有 CLOSED，不重开。BLOCKED-1（HCCL Test × 目标 CANN/HDK/机型官方交集）仍按前次报告单列 blocked_on_evidence/open，不计入发现数量；T03-06/T03-07 的有限文档/来源范围通过保持，整个 Batch 19 不因本次局部复核而验收。

约定配置 `gpt-6.1-sol / xhigh` 仅为用户约定，不写成已独立确认的执行模型或推理等级。执行者为当前 Codex 主会话，角色为独立审阅者，与作者修订角色分开；无子代理。本轮只写本报告，不代作者修订，不新增发现 ID。下表子条件 CLOSED/OPEN 不产生新 ID，也不改变整项累计计数。

## 输入与复核范围

| 输入 | SHA-256 |
|---|---|
| [T03-08 正文](../../knowledge/03-communication/bandwidth-degradation-triage.md)（procedure / draft） | `c2694fdb089d4c4b6fa84dc1ef1dac96551f92cecb20e3d22140c025dfa90ff0` |
| [作者来源记录](batch-19-t03-08-sources.md) | `3d870ef3999438e999dba1942a21f7c66380c0bd3d2d6cc9d4fd00712abd044d` |
| [修订映射](batch-19-review-fixes.md)（第五轮修订节 L127–131） | `ad1884be99e61469a8486418ebfbcce7da80b990f0f04e2f48e569a5659b5dce` |
| [第四次定向复核](batch-19-t03-08-codex-recheck-4.md)（剩余关闭条件权威来源：C23 L56、C24 L80、C27 L99） | `80a9860817beca3ce65cf6b83acadb519350d343d9d2b898d7d3e4988eea29c3` |
| [任务验收](../../plans/full-coverage-backlog.yaml)（T03-08 acceptance 1–4，L5006–5010） | `121826a4d499273e7f6a00735e0a53931eef5c097bd66ab6b2425fdbc36ddfe0` |

逐项核对实际正文、作者记录与一次源，不以映射 L129–131 的完成自述代替交付。只检查 C23 的无新增观测条件、C24 的五列表格/统一出口/逐轮设计、C27 的来源映射与轮次同步；其余已关闭子条件保持。依赖正文、登记和历史报告只读解析，不重新验收其历史发现。

| 补充只读输入 | SHA-256 |
|---|---|
| [来源登记](../../sources/registry.yaml) | `277aecb64892438a366c1729fe01210cbeae60845ff6fbefce437a7a7a96901e` |
| [T03-07 基线口径](../../knowledge/03-communication/bandwidth-baselines.md)（矩阵 L144–161） | `8c2884b63cf7b638c1df2d7de88f5fe9d2923c0d95b025548041aea203574039` |
| [T03-03 RDMA 诊断](../../knowledge/03-communication/rdma-baseline-and-congestion-triage.md)（计数器 L79–98、覆盖门禁 L137–146） | `7f6d59752e7c74628f2c9d706ce2ec00e3031ecd36230554eb8d2680fee67412` |
| [T03-05 RCCL 档案](../../knowledge/03-communication/rccl-runtime-and-verification.md)（工具节） | `1f95d5b310726d858900e2028ab3b779f1470b03a1ba67187fbed1c6da5b19db` |
| [T03-06 三库对照](../../knowledge/03-communication/communication-library-profiles.md)（工具及交集限制 L65/L74–76） | `d4a5fb535ba78d852e070f09ff387b69dc6e1ab7cf86620c7ee08e9a99577646` |

## 一次源取证与方法限制

采用本地只读逐行检查、默认 TLS 校验的只读 curl、允许的网页阅读器与 GitHub 连接器。curl 请求 UFM 4.18.15 端口计数器页、RCCL docs-10.1.0 troubleshooting 页、NCCL 2.27.5 env 页，均 DNS 解析失败：exit 6、HTTP 000、下载 0 字节。HTTP 000 不是上游状态；未使用 `-k/--insecure`，未修改网络或 TLS 配置。

网页阅读器取得 UFM、NCCL env/ACS/RAS 精确页及 #2409 正文。RCCL docs-10.1.0 HTML 返回读取错误（工具显示 429），固定源码网页读取也失败；改由 GitHub 连接器读取作者 L11 所链的 `therock-10.1` 官方文件和已登记完整 commit 下的工具节，返回相同 Git blob SHA。**不声称 RCCL HTML 已打开成功或与源码全文相同，不把本轮审阅取证倒写成作者历史实开。** 本轮不重新审阅 #814/#209 的已关闭案例结论，也不将 #2409 开帖的待纠正假说当作最终结论。

| 一次源 / 已登记 ID | 本轮精确定位与证据 | 支持范围 / 限制 |
|---|---|---|
| `src.nvidia.ufm-41815-port-counters` | [InfiniBand Port Counters](https://networking-docs.nvidia.com/ufmsdnappswum/41815/infiniband-port-counters)，Rcv Errors、Symbol Errors、Link Error Downed、Xmit Discards 行；登记 L4520–4530 | 收错含 overrun，Symbol/Downed 分别描述 lane 错误/训练恢复失败事件，Discards 含多种原因。IB 文档不证明目标 RoCE/HCCS 现场能力；零新增有限结论是本库门禁设计，不是 UFM 的健康保证。 |
| `src.nvidia.nccl-user-guide-2.27.5` | [SPLIT_DATA_ON_QPS](https://docs.nvidia.com/deeplearning/nccl/archives/nccl_2275/user-guide/docs/env.html#nccl-ib-split-data-on-qps)、[CROSS_NIC](https://docs.nvidia.com/deeplearning/nccl/archives/nccl_2275/user-guide/docs/env.html#nccl-cross-nic)、[ACS](https://docs.nvidia.com/deeplearning/nccl/archives/nccl_2275/user-guide/docs/troubleshooting.html#pci-access-control-services-acs)、[RAS sample output](https://docs.nvidia.com/deeplearning/nccl/archives/nccl_2275/user-guide/docs/troubleshooting/ras.html#sample-output) | 分摊方式/默认值、rail 意图与例外、PCI 重定向及进度差异的瞬态边界分别可核对；不代替 UFM 精确来源或逐轮输入契约。 |
| `src.nvidia.nccl-issue-2409` | [Issue 正文](https://github.com/NVIDIA/nccl/issues/2409)，§1 perftest、§2 rail、§3 WQE、§4 sweep | 是报告者跨层及配置对照的来源，足以定位作者所称 §1–§4；不是厂商完整四轮设计或本库实验结果。L11 的“基线→单变量→替代路径”属于作者设计归纳，不能代替该行精确 URL。 |
| `src.rocm.rocm-systems-therock-10.1`（HTML 通道未成功） | [作者所链的官方文件](https://github.com/ROCm/rocm-systems/blob/therock-10.1/projects/rccl/docs/how-to/troubleshooting-rccl.rst)及[固定 commit 文件](https://github.com/ROCm/rocm-systems/blob/7da43026e4f2ef7600433c38c820732f7a205d22/projects/rccl/docs/how-to/troubleshooting-rccl.rst)，Using the RCCL Replayer / Collect the TransferBench data；Git blob `89779e32d545fcd1f61a7dc728e0abf9113bc186` | 两个工具节确实存在，分别为 collective 日志/dummy data 回放和设备间并发拷贝基准，不是实际端点/rail/transport 替代。源码对象身份不混作 SHA-256；未构建、运行。 |

未取得 curl 原始响应字节，不补造远程 SHA-256。未打开未选的 ROCm 注记/FaultDiag 候选或 HCCL Test 版本交集，不用本轮通道成败判定作者过去一定做过或没做过取证。以下 CLOSED/OPEN 是按第四次复核剩余条件作出的文档审阅判断，不是硬件验证。

## B19-C23 — P2 / CLOSED：无新增事件条件已接入有限排除

位置：正文 L76 的物理错误支，时窗契约 L63；修订映射 L129。对应 acceptance 2；依据前次报告 L56。

| 子条件 | 判定 | 位置与证据 |
|---|---|---|
| 有效同窗内所选错误事件无新增 | CLOSED | L76 的“同时成立”列表已明确“所选同路径/同作用域事件在本窗无新增（错误事件 delta 为零，正增量不得进入本分支）”。与前后值/增量记录、有效窗口及路径范围直接相连，不再由结论句反推观测值。 |
| 正增量及不可解释 delta 的出口 | CLOSED | 正增量被明文阻断；重置/回退、采样边界不可解释、关系/掩盖/覆盖不足仍 unknown。没有要求正常流量 Data/Packets 统一零增量，依赖 T03-03 L85–90 也区分正常流量与错误事件。 |
| 强度与既有门禁 | CLOSED（保持） | 同路径同作用域、采样/重置、关系/覆盖限制均保留；最多陈述“本窗未观测到这些事件”，不推出硬件健康、硬件根因或全路径排除。其余此前 CLOSED 子条件不重开。 |

**剩余关闭条件：无。** 接受为设计层修订；本轮没有实际采样或零增量实测证据，不把 C23 关闭写成现场物理支已排除。

## B19-C24 — P2 / OPEN：表格仍缺第五列，出口与设计契约未闭环

位置：正文 L67–77、L79–84、L93–102；来源记录 L11；修订映射 L130。对应 acceptance 4；依据前次报告 L80。

| 子条件 | 判定 | 位置与证据 |
|---|---|---|
| 步骤 7 下一步分叉及缺口类别 | CLOSED（保持） | L75 仍为证据齐全且满足判据→结束，未完成候选/缺口→8；L77 区分可做对照与无法取得证据的缺口。该区分不等于所有出口已统一。 |
| 步骤 9 完整五列表格行 | OPEN（由两列改善为四列） | 按未转义的竖线分隔逐行核对：L67 表头与 L69–76 各为 5 个单元格；L77 只有 4 个，依次是步骤、动作、运行影响、预期证据与解释。末尾将“对照完成→回步骤 7……”并入第四格，没有独立的第五格“下一步”。详案已移至 L79–84，不再散落为表尾段落，但映射 L130 的“五列”自述仍不成立。 |
| 所有正常诊断出口统一回 7 | OPEN | L77 动作格和末格仍为“对照完成→回步骤 7 汇总，未完成→留 unknown”，并允许无法取得证据的缺口登记 unknown 后按判据 4 直接结束；没有明确未完成/unknown 也先回 7。动作格提到步骤 7 按判据 2/3 或 4 汇总，不消除另一个直接结束出口。风险触发停止继续独立，保持接受。 |
| 四轮输入/门禁/保持项的新增 | CLOSED（部分子条件） | L81 新增复用步骤 1–3 输入与 T03-03 host 覆盖门禁；L83 接入变量名/原值/新值及其余配置/负载逐项记录；L84 将保持项具体到配置/测试口径/隔离条件，并要求校验/覆盖有效才进入性能差异判读。这些修订予以承认，但不代替下表仍缺的共同准入与背景输入。 |
| CPU/网/存可重现背景输入契约 | OPEN | L82 的 CPU 已增加工具/版本/强度/持续时间和作用进程，网络/存储增加强度/持续时间及端点/数据集或访问模式；但三域均缺明确并发及复现方法/完整参数或配置身份，CPU 计算输入身份未定，网络/存储没有负载工具或生成方法/版本约束，存储作用后端/对象仍仅为类别。只写“实际达到声明的输出”不能补齐可重现输入。 |
| 未选 unknown、工具分域、停止与恢复 | CLOSED（保持） | L77/L81–84 保留未选变量/版本能力/输入的 unknown 或未完成；Replayer/TransferBench 仍与真实替代分列，FaultDiag 为候选；正确性失败、超时/异步错误、窗口失效即停，恢复保存原值或批准修复配置后同条件复测。 |

七要素沿用前次报告 L71：隔离条件、背景负载、路径变量（变更/保持分开）、可比输入、原生输出、校验/完整性、判定/无法判断。可显式复用共同输入和有效性门禁；需要的是设计契约，不要求实际选择工具值、执行命令或填实测结果。

| 轮次 | 已交付 / 本轮可接受进展 | 尚缺的逐轮交付 |
|---|---|---|
| 隔离基线（L81） | 停背景、路径/配置保持、原生输出；已明确步骤 1–3 输入与 T03-03 host 覆盖门禁；默认不代替批准配置的限定保留 | 仍把 `#wrong`/覆盖/缺行写为声明，再写“基线有效，或缺输入 unknown”；未明确测试自身校验与输出完整性、同窗有效性全部通过才形成有效基线，失败/缺行/无法解释时如何退出判读。T03-03 的 host 门禁可用于所选 host 独立测试，不自动替代 NCCL/HCCL 测试自身判读。将现有步骤 3/L63 的有效性条件明确接入即可，不要求新造门禁。 |
| 可控背景（L82） | 一次引入一域、其余两域保持，同窗指标/背景达成输出，同基线门禁，退化/无差/无法比较 | 三域输入补齐上表可重现字段；明确固定基线的测试输入/实际路径/计时口径与隔离条件（只改选定背景域），交付测试原生输出，而不只背景和同窗指标；完整性与有效性准入明确采用修订后的基线共同门禁。 |
| 单变量（L83） | 变量名/原值/新值已补；其余配置/负载逐项记录要求已补；实际配置/路径与原生输出、同基线门禁、恢复/无变化/unknown | 明确采用哪一组隔离/背景及同窗共同条件；性能判读显式依赖有效基线/本轮校验和完整性准入。“同基线门禁”可以复用，但上行基线门禁须先闭环，不能把候选变量或未选能力当已完成轮。 |
| 替代端点/rail/路径（L84） | 匹配输入/背景、替代身份、实际替代与原生输出；保持项已具体到配置/测试口径/隔离条件；校验/覆盖有效才进入性能差异判读，未发生/能力未证实 unknown | 前次对“其余”保持项及校验/覆盖前置的两项剩余要求已补（C24 子条件 CLOSED）。与基线共同使用的输入完整性/同窗准入仍须在共同契约闭环；替代成功仍只说明干预发生，不说明整套四轮性能对照有效。 |

**剩余关闭条件：**给 L77 独立第五格“下一步”，完成、未完成和 unknown 均先回 7 汇总，再由 7 决定继续 8/9 或按完成判据结束；风险停止不并入正常出口。给四轮明确采用的完整固定输入、同窗与校验/完整性/覆盖准入，以及无效/unknown 判定；保留已补变更/保持项和原新值契约。CPU/网/存分别补负载/工具版本或输入身份、强度/并发/持续时间、作用对象和可重现配置/方法要求，测试原生输出与背景输出分开。未知或未选条件继续标未完成/unknown；不要求 benchmark 或虚构 HCCL 版本交集。

## B19-C27 — P2 / OPEN：源码工具节已补，完整映射与轮次仍不一致

位置：来源记录 L3/L9–11/L19；正文 L34/L60/L74/L76/L126–130；修订映射 L131。对应 acceptance 1–4 的可追溯性；依据前次报告 L99。

| 子条件 | 判定 | 位置与证据 |
|---|---|---|
| L9 完整内容 ID | OPEN | 仍为“—（方法整理）”，未列 `communication.bandwidth-baselines` / `communication.rdma-baseline-and-congestion-triage`；两个完整 ID 可在所链依赖正文 L2 核对。映射 L131 自述补齐，不能替代记录。 |
| L10 UFM 精确页及范围 | OPEN（ID 保持满足） | 已有 `src.nvidia.ufm-41815-port-counters` 与 UFM 4.18.15/字段简称，但定位仍为 T03-03 内部链接，不含登记 L4522 的精确 NVIDIA 页；也未明确 IB 及不覆盖 RoCE/HCCS/目标现场能力。正文 L76 的“UFM 语义”同样只链接 T03-03，映射 L131 的“正文已链”不能补成精确上游页。 |
| L11 官方工具文件/两个工具节 | CLOSED（本轮新增） | L11 已加入已登记 `therock-10.1` 官方 troubleshooting 文件 URL，并分别指明两个工具节；连接器读回与固定 commit 的 Git blob 一致。既有 `communication.rccl-runtime-and-verification` 内容 ID 保留，用途分列正确；只接受源码证据，不记为 HTML 已实开。 |
| L11 #2409 精确定位及归纳强度 | OPEN（局部剩余） | 本行仍只写“#2409 §1–§4”，没有该行精确 Issue URL/章节对应定位。L12–13 的案例 URL 不替代本行主张映射；§1–§4 实际是 perftest/rail/debug/sweep，四轮设计属于方法整理，应说明借鉴范围，不把上游段落写成完整替代路径方案。 |
| 悬空代号定义/删除 | OPEN（原剩余项保持） | L3 虽列代号字典，但 C3 仍仅“ROCm 注记”，S5 仅 FaultDiag，S6 仅 HCCL 工具介绍；L19 继续沿用，未定位具体来源对象/版本或删掉代号后明确未采用/未选择。C1/C2/S1/S2/S3/S7 的可解析对应保持接受。不要求采用这些候选来凑齐来源。 |
| 旧遥测三处原批限定 | CLOSED（保持） | 正文 L60、L74 末格、L130 与记录 L19 仍限定原批 Batch 09，区别当前 T03-03 文档可用与现场能力未知。不将中段历史旧句扩解为全库缺源。 |
| 矩阵字段契约同步 | CLOSED（保持） | 正文 L34/L127 与记录 L9/L19 均为字段契约已引用、实测矩阵未交付；T03-07 L144–161 保持，不宣称填了实测值或证明兼容。 |
| T03-06/RCCL 档案/作者记录入口 | CLOSED（保持） | 正文 L77/L126/L128 接通三入口，历史 Batch 09 入口保留；目标存在。入口不能代替 L9/L10 精确映射。 |
| verification 作者轮次与审阅历史 | OPEN（部分进展） | 记录 L3 的审阅历史已补至一/二/三/四次，且作者“第四次修订”说明无新增远程取证；但仍重复作者第一次/第二次修订，第三次仍写“本轮”且无取证/复用限定。正文 L34 仍为首轮＋第二轮＋第三/第四次修订，独立审阅只到一/二/三次，与记录及已存在第四次复核不同步。映射 L127/131 是第五轮/“作者四轮”，正文和记录却仍把第四次修订标“本轮”；第五轮实际范围未单列。 |

记录 L3 的“首轮 S1–S7 实开”与 L19 的 S6“未实开”、S4“HTML 未取成功，仅源码”仍没有可解释的轮次/角色/来源范围限定。本轮官方源码可读不能证明作者过去 S1–S7 全量实开；也不能由本轮 HTML 失败倒推作者过去没取过。此一致性问题按 C27 保留，不新增 ID。

**剩余关闭条件：**实际在记录 L9 写两个完整内容 ID；L10 写已登记 UFM 精确页、完整所选字段、版本/IB/未覆盖范围；L11 保留新补源码工具节与内容 ID，补 #2409 精确 URL/章节映射并标清设计归纳和未采用候选。对 C3/S5/S6 定义具体来源对象，或删代号并如实记录未选/未采用。作者首轮与第一至第五轮修订逐项去重、注明本轮范围及远程取证/复用/未知，与正文 verification 同步；独立初审和已存在一至四次复核分列，不虚构执行元数据或历史实开。保留已 CLOSED 的案例映射、原批遥测限定、矩阵状态、工具节和入口。

## 状态集合与验收影响

| 状态 | ID / 范围 |
|---|---|
| 本轮 CLOSED（整项） | C23（1 P2） |
| 本轮 OPEN（2 P2） | C24、C27 |
| 既有 CLOSED（24；不重开） | C01–C22、C25、C26 |
| 本批累计审阅发现 | **25 CLOSED / 2 OPEN**（共 27 个 ID，未新增） |
| 既有验收子项 OPEN（单列） | BLOCKED-1，blocked_on_evidence；不计入发现数量 |
| T03-08 | **第五次定向复核未通过**；下一轮只复核 C24/C27 剩余条件 |
| T03-06/T03-07 | 有限文档/来源范围通过保持，不重新验收 T03-06 acceptance 5 |
| Batch 19 | 未完成整批验收，不由一个 ID CLOSED 推导全部完成 |

acceptance 1 的时窗/矩阵契约保持，不重开 C22；acceptance 2 的 C23 物理支剩余门禁本轮关闭，仅限设计文档，不是现场排除结果；acceptance 3 的既有案例结论保持，不重开 C25/C26，来源定位和历史记录仍受 C27 限制；acceptance 4 的表格/统一出口/逐轮契约由 C24 阻挡。来源可读、模型审阅与结构校验都不建立硬件验证或版本兼容交集。

## 检查边界与写入范围

- 仅新增本报告；不改作者正文、来源记录、映射、登记、计划、索引或来源审计。既有工作区改动不恢复、不提交、不创建分支。
- 不执行 benchmark、collective/MPI、实机采集、配置修改、故障注入或上游诊断命令；上游示例仅阅读。未取得现场遥测、时钟、字段能力或实验结果。
- curl 原始远程读取失败，允许的替代只读通道完成上述核对；RCCL 用官方固定源码，不冒充 HTML 或作者历史取证。未补未选候选及 HCCL 交集证据，unknown/blocked_on_evidence 保留。
- 为遵守“只写这一份报告”，在含本报告的仓库外临时快照执行 `make check` / `make build`，最终均 PASS（88 content entries / 389 sources）；原仓库 `build/` 不重建。第一次快照检查因未带入既有 `build/catalog.json` / `build/catalog.md` 而报两个本地链接缺失，复制既有构建目录到快照后重新 check/build 通过；这是快照准备缺项，不认定为作者内容新发现。不改 `src/kb/`，不执行 `make test`。结构校验不验证技术正确性、五列呈现或远程语义。
- 本报告 10 处本地链接、10 个不同目标均存在。写入前后 SHA-256/符号链接清单核对：原有 3479 个常规文件（含 `.git`、既有构建文件和本地环境文件）与 3 个符号链接均不变，无删除，仅新增本报告；五项任务输入与输入 SHA 表一致。临时快照与清单均在仓库外，不作为现场验证证据。
