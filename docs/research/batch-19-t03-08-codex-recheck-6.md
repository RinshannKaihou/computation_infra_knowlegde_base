# 第十九批 T03-08 第六次定向复核

审阅日期：2026-10-13（Asia/Shanghai，本机日期确认）。正文 `updated_at: 2026-10-14` 及部分来源登记日期晚于本轮实际日期，只视为作者交付标签，不作为本轮取证日期或历史执行证明；输入身份以下表 SHA-256 为准。

**结论：C23 保持 CLOSED；C24、C27 仍 OPEN（2 项 P2）。本批累计 25 CLOSED / 2 OPEN（共 27 个审阅发现），T03-08 第六次定向复核未通过。** 本轮接受步骤 9 五列行、共同准入和部分逐轮契约，以及记录 L9 完整内容 ID、L10 精确 UFM 页及版本/IB/未覆盖范围的补充，但不据此关闭整项。C01–C22、C25、C26 沿用既有 CLOSED，不重开。BLOCKED-1（HCCL Test × 目标 CANN/HDK/机型官方交集）仍按前次报告单列 blocked_on_evidence/open，不计入发现数量；T03-06/T03-07 的有限文档/来源范围通过保持，整个 Batch 19 不因本次局部复核而验收。

约定配置 `gpt-6.1-sol / xhigh` 仅为用户约定，不写成已独立确认的执行模型或推理等级。执行者为当前 Codex 主会话，角色为独立审阅者，与作者修订角色分开；无子代理。本轮只写本报告，不代作者修订，不新增发现 ID。下表子条件 CLOSED/OPEN 不产生新 ID，也不改变整项累计计数。

## 输入与复核范围

| 输入 | SHA-256 |
|---|---|
| [T03-08 正文](../../knowledge/03-communication/bandwidth-degradation-triage.md)（procedure / draft） | `b6d07d1d720fae61473827560cc01d4521b3fc9fe16cd8a2c396377b3c3e0cdd` |
| [作者来源记录](batch-19-t03-08-sources.md) | `868e908b39aff1f13904e6979b570f57afc54e4b78b1ac9efe020407ccc0712d` |
| [修订映射](batch-19-review-fixes.md)（第六轮修订节 L133–137） | `b7fb94032f43f1553f048391483fcd849f7b7aaaf008b6c3d98606e5fd541217` |
| [第五次定向复核](batch-19-t03-08-codex-recheck-5.md)（剩余关闭条件权威来源：C23 L54、C24 L78、C27 L98；累计状态 L100–113） | `f54bff372b66ec6f9503c0e91d3dba915f9fa11e03cfd18626224f5ba4027a41` |
| [任务验收](../../plans/full-coverage-backlog.yaml)（T03-08 acceptance 1–4，L5006–5010） | `121826a4d499273e7f6a00735e0a53931eef5c097bd66ab6b2425fdbc36ddfe0` |

逐项核对实际正文、作者记录与一次源，不以修订映射 L135–137 的完成自述代替交付。只检查 C23 的无新增观测条件、C24 的五列表格/统一出口/四类轮次七要素、C27 的精确映射与轮次同步；其余已关闭项不重新审阅。依赖正文和登记只读解析，历史案例结论不重新验收。

| 补充只读输入 | SHA-256 |
|---|---|
| [来源登记](../../sources/registry.yaml) | `277aecb64892438a366c1729fe01210cbeae60845ff6fbefce437a7a7a96901e` |
| [T03-07 基线口径](../../knowledge/03-communication/bandwidth-baselines.md)（矩阵 L144–161） | `8c2884b63cf7b638c1df2d7de88f5fe9d2923c0d95b025548041aea203574039` |
| [T03-03 RDMA 诊断](../../knowledge/03-communication/rdma-baseline-and-congestion-triage.md)（计数器 L79–98、host 覆盖门禁 L137–146） | `7f6d59752e7c74628f2c9d706ce2ec00e3031ecd36230554eb8d2680fee67412` |
| [T03-05 RCCL 档案](../../knowledge/03-communication/rccl-runtime-and-verification.md)（工具节） | `1f95d5b310726d858900e2028ab3b779f1470b03a1ba67187fbed1c6da5b19db` |
| [T03-06 三库对照](../../knowledge/03-communication/communication-library-profiles.md)（工具及交集限制 L65/L74–76） | `d4a5fb535ba78d852e070f09ff387b69dc6e1ab7cf86620c7ee08e9a99577646` |

## 一次源取证与方法限制

采用本地只读逐行检查、未转义竖线的表格单元格检查、默认 TLS 校验的只读 curl、允许的网页阅读器与 GitHub 连接器。curl 请求 UFM 4.18.15 端口计数器页、RCCL docs-10.1.0 troubleshooting 页、NCCL 2.27.5 env 页，均 DNS 解析失败：exit 6、HTTP 000、下载 0 字节。HTTP 000 不是上游状态；未使用 `-k/--insecure`，未修改网络或 TLS 配置。

网页阅读器取得 UFM、NCCL env/ACS/RAS 精确页及 #2409 正文。RCCL docs-10.1.0 HTML 和固定 commit 的 GitHub 文件网页读取均返回工具内部读取错误，未取得可核对正文或可信上游 HTTP 状态；改由 GitHub 连接器分别读取作者 L11 所链 `therock-10.1` 文件与已登记完整 commit 文件中的工具节，返回相同 Git blob SHA。**不声称 RCCL HTML 已打开成功或与源码全文相同，不把本轮审阅取证倒写成作者历史实开。** 本轮不重新审阅 #814/#209 的已关闭案例结论，也不将 #2409 开帖的待纠正假说当作最终结论。

| 一次源 / 已登记 ID | 本轮精确定位与证据 | 支持范围 / 限制 |
|---|---|---|
| `src.nvidia.ufm-41815-port-counters` | [InfiniBand Port Counters](https://networking-docs.nvidia.com/ufmsdnappswum/41815/infiniband-port-counters)，Rcv Errors、Symbol Errors、Link Error Downed、Xmit Discards 行；登记 L4520–4530 | 收错包含 overrun；Symbol/Downed 分别记录 lane 错误和训练恢复失败 down 事件；Discards 为多因。页路径固定 `41815`，登记 revision 为 `4.18.15-LTS-2024-U5`；本轮阅读器只显示选择器占位，未独立读到完整版本后缀。IB 页不证明目标 RoCE/HCCS 现场能力；零新增有限结论是本库门禁设计，不是上游健康保证。 |
| `src.nvidia.nccl-user-guide-2.27.5` | [SPLIT_DATA_ON_QPS](https://docs.nvidia.com/deeplearning/nccl/archives/nccl_2275/user-guide/docs/env.html#nccl-ib-split-data-on-qps)、[CROSS_NIC](https://docs.nvidia.com/deeplearning/nccl/archives/nccl_2275/user-guide/docs/env.html#nccl-cross-nic)、[ACS](https://docs.nvidia.com/deeplearning/nccl/archives/nccl_2275/user-guide/docs/troubleshooting.html#pci-access-control-services-acs)、[RAS sample output](https://docs.nvidia.com/deeplearning/nccl/archives/nccl_2275/user-guide/docs/troubleshooting/ras.html#sample-output) | 分摊方式/默认值、rail 意图及例外、PCI 重定向、进度差异正常瞬态的边界均可核对；这些页不提供本库完整四轮背景输入契约，也不代替 UFM 映射。 |
| `src.nvidia.nccl-issue-2409` | [Issue 正文](https://github.com/NVIDIA/nccl/issues/2409)，§1 perftest、§2 rail 扫描、§3 debug/WQE、§4 env sweep | 足以核对作者 L11 所称章节，但不是上游按“隔离基线/可控背景/单变量/替代路径”完整交付的四轮方案。设计归纳应与报告者观察分开；不重新判定该案例原因或修复。 |
| `src.rocm.rocm-systems-therock-10.1`（HTML 通道未成功） | [作者所链官方文件](https://github.com/ROCm/rocm-systems/blob/therock-10.1/projects/rccl/docs/how-to/troubleshooting-rccl.rst)及[固定 commit 文件](https://github.com/ROCm/rocm-systems/blob/7da43026e4f2ef7600433c38c820732f7a205d22/projects/rccl/docs/how-to/troubleshooting-rccl.rst)，Using the RCCL Replayer / Collect the TransferBench data；Git blob `89779e32d545fcd1f61a7dc728e0abf9113bc186` | 两个工具节存在：Replayer 使用 collective 日志和 dummy data 回放；TransferBench 测设备间并发拷贝。均不自动构成实际端点/rail/transport 替代；源码对象身份不混作 SHA-256，未构建、运行。 |

未取得 curl 原始响应字节，不补造远程 SHA-256。未打开未选的 ROCm 注记/FaultDiag 候选或 HCCL Test 版本交集，不用本轮通道成败证明作者过去做过或没做过取证。以下 CLOSED/OPEN 是设计文档与来源可追溯性判断，不是硬件验证。

## B19-C23 — P2 / CLOSED（保持）：无新增条件及有限排除门禁保留

位置：正文 L76 的物理错误支，时窗契约 L63；前次报告 L44–54。对应 acceptance 2。

| 子条件 | 判定 | 位置与证据 |
|---|---|---|
| 有效同窗内所选错误事件无新增 | CLOSED（保持） | L76 “同时成立”列表仍明确所选同路径/同作用域事件在本窗无新增、错误事件 delta 为零、正增量不得进入有限排除分支；前后值/增量及采样/重置边界同时记录。 |
| 正增量、不可解释 delta 及范围缺失 | CLOSED（保持） | 正增量被阻断；重置/回退、采样边界不可解释、路径关系/掩盖条件/覆盖不足继续 unknown。不要求正常流量 Data/Packets 零增长，与 T03-03 L85–90 区分一致。 |
| 结论强度 | CLOSED（保持） | 最多陈述“本窗未观测到这些事件”，不推出硬件健康、硬件根因或全路径排除；字段未选/窗口不齐仍 unknown。UFM 一次源的多因语义与本轮有限范围相容。 |

**剩余关闭条件：无。** C23 是前次已关闭项的定向保持核对，不算本轮新增 CLOSED；没有零增量实测或现场物理支排除结果。

## B19-C24 — P2 / OPEN：五列与共同准入已补，统一出口和背景输入仍缺

位置：正文 L67–84、L92–101；修订映射 L136。对应 acceptance 4；依据前次报告 L78。

| 子条件 | 判定 | 位置与证据 |
|---|---|---|
| 步骤 9 完整五列表格行 | CLOSED（本轮新增子条件） | 按未转义竖线分隔，L67 表头、L68 分隔行及 L69–77 九个步骤均为 5 个单元格。L77 已将“预期证据：四类轮次输入/判定齐全……”和末尾“下一步”分为第四、第五格；明细在 L79–84，不再破坏表格。 |
| 步骤 7 分叉及风险停止 | CLOSED（保持） | L75 保留齐全且满足判据→结束、未完成候选/缺口→8；L77 正确性失败、超时/异步错误、观测窗口失效即停，与正常诊断出口分开。 |
| 所有正常诊断出口统一回 7 | OPEN | L77 第五格只对“对照完成”明确回 7；“未完成/unknown”仍先写“留 unknown”，其中无法取得证据的缺口仍可登记后按判据 4 直接结束。可做对照的缺口写了 7→8→9，不能覆盖另一条直接结束出口。L136 自述“出口统一回 7”与实际交付不符。 |
| 四轮共同固定输入与有效性准入 | CLOSED（本轮新增子条件） | L79 明确复用步骤 1–3、L63 时窗契约和 T03-03 host 覆盖门禁；L81 新增测试自身正确性、输出完整性、同窗有效性全部通过才成有效基线，失败/缺行/无法解释退出判读记 unknown。L82–84 分别复用基线共同门禁/本轮准入。T03-03 的门禁限已声明的 host 独立测试，不能取代步骤 3/L81 的库测试自身校验，不能证明未核定后端或版本交集。 |
| 变更/保持、原新值、未选处理、恢复 | CLOSED（保持） | L83 保留变量名/原值/新值和其余配置/负载逐项记录；L84 保留替代身份及配置/口径/隔离保持项；未选变量或能力未证实不算完成轮。L77 恢复保存原值或经批准修复配置并同条件复测，不以默认配置代替原批准配置。 |
| CPU/网/存可重现背景输入 | OPEN | L82 三域仍未补前次要求的明确并发及可复现完整参数/配置身份；CPU 未固定计算输入身份；网络/存储未要求生成工具或方法及版本，存储作用后端/对象仍仅类别。测试原生输出与背景实际达成输出已分列，这是进展，不补齐缺失输入。 |

七要素沿用前次报告：①隔离条件；②背景负载；③路径变量（变更/保持分开）；④可比输入；⑤原生输出；⑥校验/完整性；⑦判定/无法判断。允许显式复用共同契约；不要求实际选工具值、执行命令或填实测结果。

| 轮次 | 七要素核对与可接受交付 | 判定 / 剩余条件 |
|---|---|---|
| 隔离基线（L79/L81） | ①停背景；②并发/停背景声明；③无变更，路径/配置/基线保持；④步骤 1–3 固定输入及本轮版本/算子/消息/映射；⑤原生输出；⑥测试自身正确性/完整性/同窗准入及适用的 host 覆盖门禁；⑦有效基线或 unknown，失败不进判读 | CLOSED（本轮闭环）；仅设计层，不认定基线已测得。 |
| 可控背景（L82） | ①固定基线隔离条件；②一次只引入一域，其余两域保持；③只改选定背景，保持实际路径/配置；④明确固定基线测试输入/计时口径；⑤测试原生输出、同窗指标和背景达成输出分列；⑥复用已补基线共同门禁；⑦退化/无差/无法比较、缺轮 unknown | OPEN（②/④背景可重现输入仍不完整）；其余本轮补充接受。 |
| 单变量（L83） | ①②明确采用基线可比输入及隔离/背景共同条件；③变量名/原值/新值、版本能力及其余配置/负载保持分列；④复用固定输入；⑤实际配置/路径及测试原生输出；⑥性能判读依赖有效基线和本轮校验/完整性；⑦恢复/无变化/unknown，未选或能力未证实为未完成 | CLOSED（本轮闭环）；不将候选变量当作已执行干预。 |
| 替代端点/rail/路径（L84） | ①②匹配基线输入/背景并保持隔离；③替代身份与配置/口径保持项；④共同完整性/同窗准入；⑤实际替代及原生输出；⑥校验/覆盖有效才判性能差异；⑦替代成功/未发生/能力未证实 unknown，显式区分干预发生与性能对照有效 | CLOSED（本轮闭环）；Replayer/TransferBench 的工具存在性不代替实际路径替代。 |

| 背景域（均位于 L82） | 已有字段 | 剩余关闭条件 |
|---|---|---|
| CPU | 亲和设置、工具/版本、强度/持续时间、作用进程 | 明确计算输入/任务身份、并发线程或进程配置，以及可复现完整参数/配置/方法要求。 |
| 网络 | 流量配置、端点/数据集、强度/持续时间 | 明确生成工具或方法及版本、并发/流配置、作用端点与路径，以及可复现完整参数/配置要求。 |
| 存储 | 后端负载类别、数据集/访问模式、强度/持续时间 | 明确工具或生成方法及版本、并发、具体作用后端/对象身份，以及可复现完整参数/配置要求。 |

**剩余关闭条件：**完成、未完成和 unknown 的正常出口均先回步骤 7 汇总，再由 7 决定继续 8/9 或按完成判据结束；风险触发停止保持独立。给 CPU/网/存补齐上述可重现背景输入契约，并要求未选/缺输入时该背景轮为未完成/unknown。保留本轮已接受的五列行、共同准入、测试与背景输出分列，以及变更/保持和原新值契约；不要求 benchmark、实测值或虚构 HCCL 交集。

## B19-C27 — P2 / OPEN：L9 与 UFM 定位已补，设计归属和轮次仍不同步

位置：来源记录 L3/L9–11/L19；正文 L34/L60/L74/L76/L125–129；修订映射 L133–137。对应 acceptance 1–4 的可追溯性；依据前次报告 L98。

| 子条件 | 判定 | 位置与证据 |
|---|---|---|
| L9 完整内容 ID | CLOSED（本轮新增子条件） | 已实际写入 `communication.bandwidth-baselines` 与 `communication.rdma-baseline-and-congestion-triage`，均与所链目标 L2 的完整 ID 一致；不再只有“方法整理”。 |
| L10 UFM 精确页、登记 ID、版本/范围 | CLOSED（本轮新增子条件） | L10 已有 `src.nvidia.ufm-41815-port-counters`、登记 L4522 的 NVIDIA 精确 URL、UFM 4.18.15、IB 范围及不覆盖 RoCE/HCCS/目标现场能力的限制。本轮精确页可读，接受此定位进展；不要求未知现场字段值。 |
| L10 完整所选字段 | OPEN（收窄） | L10 仍以“Rcv Errors/Symbol/Downed/XmitDiscards”缩写所选字段，未完整列出一次源的 `Rcv Errors`、`Symbol Errors`、`Link Error Downed`、`Xmit Discards`，前次“完整所选字段”要求未全部落盘。正文 L76 仍经内部 T03-03 引用 UFM；不把记录新链接倒写成正文已直链，但不另加正文直链的关闭条件。 |
| L11 官方工具文件、两个工具节及内容 ID | CLOSED（保持） | `communication.rccl-runtime-and-verification`、官方 `therock-10.1` 文件及 Using the RCCL Replayer / Collect the TransferBench data 两节保留。连接器读回 tag 与固定 commit 的同一 Git blob；只认定源码证据，不认定 HTML 成功或作者过去已取证。 |
| L11 #2409 精确定位及设计归纳强度 | OPEN | 本行仍只有“#2409 §1–§4 表格结构（基线→单变量→替代路径）”，未补该行精确 Issue URL及章节—主张对应。一次源 §1–§4 是 perftest、rail 扫描、debug/WQE、env sweep；不是完整四轮替代路径方案。L12–13 的案例 URL 不替代 L11 的设计归属。应标明借鉴范围与本库方法归纳。 |
| 悬空代号定义/删除 | OPEN（原剩余项保持） | L3 仍把 C3 定义为“ROCm 注记”、S5 为“FaultDiag”、S6 为“HCCL 工具介绍”；L19 沿用，却未定义具体来源对象/版本或删除代号并明确未选/未采用。C1/C2/S1/S2/S3/S7 的既有可解析对应保持接受。候选未采用不必强行实开，但不得保留不可定位的“已实开”对象。 |
| 旧遥测三处原批限定 | CLOSED（保持） | 正文 L60、L74 末格、L129 与记录 L19 都保留原批 Batch 09 范围，区别当前 T03-03 文档可复用和现场能力 unknown。不把中段历史旧句扩解为当前全库缺源。 |
| 矩阵字段契约同步 | CLOSED（保持） | 正文 L34/L126、记录 L9/L19 与 T03-07 L144–161 一致为字段契约已引用、实测矩阵未交付，不声称数值已填或现场兼容已证明。 |
| T03-06/RCCL 档案/作者记录入口 | CLOSED（保持） | 正文 L77/L125/L127 三入口及历史 Batch 09 入口均存在；入口不代替本行精确映射，也不关闭 BLOCKED-1。 |
| verification 作者轮次与审阅历史 | OPEN（部分进展） | 正文 L34 审阅历史已列一至五次，作者第三/四/五次修订写了无新增远程取证；但记录 L3 审阅历史仍只到四次，第一次/第二次修订重复两遍，第三次仍称“本轮”且未限定取证/复用；第五次也称“本轮”。映射是第六轮，正文/记录却止于第五次，计数对应及本次范围未说明。不能由相似取证事项自行合并作者轮次。 |
| 作者首轮“实开”范围一致性 | OPEN（保持） | 记录 L3 仍声称首轮 S1–S7 实开；同一记录 L19 却写 S6 未实开/未用、S4 HTML 未成功仅源码、S5 未固定仅候选，没有角色/轮次/来源对象限定解释。本轮源码可读不能证明作者过去全量实开；本轮通道失败也不能证明作者过去没读过。 |
| 第六轮映射的状态/ID 事实同步（按 C27 追记） | OPEN | L133 称第五次复核为“24 CLOSED / 3 OPEN”，而权威第五次报告 L5/L107 是 25 CLOSED / 2 OPEN，C23 已 CLOSED。L135 把“L9 内容 ID 落盘”归在 C23，实际属于 C27。L137 称“作者五轮＋审阅五轮”同步，但记录审阅仍到四次；这些是本 ID 的追溯记录错误，不新增发现 ID，不重开 C23。 |

**剩余关闭条件：**保留已交付的 L9、L10 精确 URL/版本/IB/未覆盖范围和 L11 工具节/内容 ID；在 L10 补全所选 UFM 字段名称，不要求全表转录或未知现场字段值。L11 补 #2409 精确 URL和章节对应，明确四轮方案是本库设计归纳、上游提供哪些观察，不把未选候选写成已采用。对 C3/S5/S6 定义具体来源对象，或删代号并如实记录未选/未采用。去重并统一作者首轮与历次修订的计数口径，明确映射“第六轮”对应范围；逐轮记录远程取证/复用/未知，与正文 verification 同步，独立初审及已存在一至五次复核另列；解释或纠正 S1–S7“实开”与 L19 的矛盾，不臆造历史取证。第六轮映射据权威第五次报告纠正累计状态、L9 所属 ID 及轮次自述。保留已 CLOSED 的案例映射、原批遥测限定、矩阵状态、工具节和入口。

## 状态集合与验收影响

| 状态 | ID / 范围 |
|---|---|
| 本轮 CLOSED（整项保持） | C23（1 P2；前次已关闭，本轮不重复新增计数） |
| 本轮新增整项 CLOSED | 无；新接受的是 C24/C27 的部分子条件 |
| 本轮 OPEN（2 P2） | C24、C27 |
| 既有 CLOSED（24；不重开） | C01–C22、C25、C26 |
| 本批累计审阅发现 | **25 CLOSED / 2 OPEN**（共 27 个 ID，未新增） |
| 既有验收子项 OPEN（单列） | BLOCKED-1，blocked_on_evidence；不计入发现数量 |
| T03-08 | **第六次定向复核未通过**；后续只复核 C24/C27 剩余条件 |
| T03-06/T03-07 | 有限文档/来源范围通过保持，不重新验收 T03-06 acceptance 5 |
| Batch 19 | 未完成整批验收，不由局部子条件 CLOSED 推导全部完成 |

acceptance 1 的时窗/矩阵契约保持，不重开 C22；acceptance 2 的 C23 无新增物理事件门禁保持关闭，仅限设计文档，不是现场排除结果；acceptance 3 的既有案例结论保持，不重开 C25/C26，精确来源定位和轮次记录仍受 C27 限制；acceptance 4 的五列行、共同准入进展接受，但统一出口及可重现背景输入仍由 C24 阻挡。来源可读、模型审阅与结构校验都不建立硬件验证或版本兼容交集。

## 检查边界与写入范围

- 仅新增本报告；不改作者正文、来源记录、映射、登记、计划、索引或来源审计。既有工作区改动不恢复、不提交、不创建分支。
- 不执行 benchmark、collective/MPI、实机采集、配置修改、故障注入或上游诊断命令；上游示例仅阅读。未取得现场遥测、时钟、字段能力或实验结果。
- curl 原始远程读取失败，允许的替代只读通道完成上述核对；RCCL 使用官方固定源码，不冒充 HTML 或作者历史取证。未补未选候选及 HCCL 交集证据，unknown/blocked_on_evidence 保留。
- 为遵守“只写这一份报告”，在含本报告及既有 `build/` 的仓库外临时快照执行 `make check` / `make build`，均 PASS（88 content entries / 389 sources）；原仓库 `build/` 不重建。不改 `src/kb/`，不执行 `make test`。结构校验不验证技术正确性、正常诊断出口、背景可重现性或远程语义。
- 本报告 10 处本地链接、10 个不同目标均存在。写入前后 SHA-256/符号链接清单核对：原有 3480 个常规文件（含 `.git`、既有构建文件和本地环境文件）与 3 个符号链接均不变，无删除，仅新增本报告；五项任务输入与输入 SHA 表一致。临时快照及清单均在仓库外，不作为现场验证证据。
