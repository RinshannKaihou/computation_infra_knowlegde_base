# 第十九批 T03-08 第三次定向复核

审阅日期：2026-10-13（Asia/Shanghai，本机日期确认）。正文 `updated_at: 2026-10-14` 及相关登记日期为作者交付标签，不作为本轮实际取证日期；输入身份以下表 SHA-256 为准。

**结论：C23、C24、C27 仍 OPEN（3 项 P2），本轮没有整项 CLOSED。本批累计 24 CLOSED / 3 OPEN（审阅发现），T03-08 未通过。** C01–C22、C25、C26 沿用既有 CLOSED，不重开。BLOCKED-1（HCCL Test × 目标 CANN/HDK/机型官方交集）仍按前次报告单列 blocked_on_evidence/open，不计入发现数量；T03-06/T03-07 已交付有限文档/来源范围的通过保持，整个 Batch 19 不因本次局部复核而验收。

约定配置 `gpt-6.1-sol / xhigh` 仅为用户约定，不写成已独立确认的执行模型或推理等级。执行者为当前 Codex 主会话，角色为独立审阅者，与作者修订角色分开；无子代理。本轮只写本报告，不代作者修订，不新增发现 ID。下表子条件的 CLOSED/OPEN 仅表示对应关闭条件是否满足，不产生新 ID 或改变累计计数。

## 输入与复核范围

| 输入 | SHA-256 |
|---|---|
| [T03-08 正文](../../knowledge/03-communication/bandwidth-degradation-triage.md)（procedure / draft） | `9afee1c8ace90e11bb80d3a0057a2e31aec48fda7f3bd86df77fe3be881d7e24` |
| [作者来源记录](batch-19-t03-08-sources.md) | `5f09113d1ae7edb82226cb16fedbc4163f2dcf9ae2b3b200b05ff463a950de34` |
| [修订映射](batch-19-review-fixes.md)（第三轮修订节 L114–119） | `56e89492b79d57d823b8012317b72d664113e7b89cee95b636c7df8eaf55b16f` |
| [第二次定向复核](batch-19-t03-08-codex-recheck-2.md)（C23/C24/C27 剩余关闭条件权威来源，L65/L79/L118） | `1c4725584f25a469a85c2c9e5bbac17ab6168cecabde49cd3a310903f046d169` |
| [任务验收](../../plans/full-coverage-backlog.yaml)（T03-08 acceptance 1–4，L5006–5010） | `121826a4d499273e7f6a00735e0a53931eef5c097bd66ab6b2425fdbc36ddfe0` |

逐项核对实际正文、记录和一次源，不以修订映射 L116–119 的“七要素”“映射表”“轮次同步”等完成自述替代交付证据。来源记录仍为七条主张行，本轮检查每行的 ID、定位、字段和支持范围；案例取证仅用于 C23 的判据方向及 C27 的来源映射，不重新审阅 C25/C26。

必要依赖只读核对，不重开其历史发现；来源登记仅用于解析 C27 引用。

| 补充只读输入 | SHA-256 |
|---|---|
| [来源登记](../../sources/registry.yaml) | `277aecb64892438a366c1729fe01210cbeae60845ff6fbefce437a7a7a96901e` |
| [T03-07 基线口径](../../knowledge/03-communication/bandwidth-baselines.md)（跨节点矩阵 L144–161） | `8c2884b63cf7b638c1df2d7de88f5fe9d2923c0d95b025548041aea203574039` |
| [T03-03 RDMA 诊断](../../knowledge/03-communication/rdma-baseline-and-congestion-triage.md)（计数器与边界 L68–98/L120） | `7f6d59752e7c74628f2c9d706ce2ec00e3031ecd36230554eb8d2680fee67412` |
| [T03-05 RCCL 档案](../../knowledge/03-communication/rccl-runtime-and-verification.md)（工具 L66–71） | `1f95d5b310726d858900e2028ab3b779f1470b03a1ba67187fbed1c6da5b19db` |
| [T03-06 三库对照](../../knowledge/03-communication/communication-library-profiles.md)（诊断工具 L65、交集限制 L74–76） | `d4a5fb535ba78d852e070f09ff387b69dc6e1ab7cf86620c7ee08e9a99577646` |

## 一次源取证与方法限制

采用本地只读逐行检查、默认 TLS 校验的只读 curl、允许的网页阅读器与 GitHub 连接器。curl 分别请求 UFM 4.18.15 端口计数器页、NCCL 2.27.5 env 页、RCCL docs-10.1.0 troubleshooting 页，均为沙箱 DNS 失败：exit 6、HTTP 000、下载 0 字节。HTTP 000 不是上游状态；未使用 `-k/--insecure`，未调整网络或 TLS 配置。

网页阅读器取得 NCCL env/ACS/RAS、UFM 精确页面及三个 Issue 正文；精确 GitHub comment API 取得 #2409 四条、#814 四条和 #209 一条所引用评论。#814 的 2283482549 首次连接器读取出现 RemoteProtocolError，随后同一只读请求成功。RCCL docs-10.1.0 HTML 阅读返回 Internal Error；改取已登记 `therock-10.1` 的官方文档源码核对工具用途，**不声称该 HTML 已打开成功或与源码全文相同**。作者映射 L117 的“实核 200”属于作者自述，本轮不能独立重现该 HTTP 结果，也不据本轮通道失败否认作者此前取证。

| 一次源 / 已登记 ID | 本轮精确定位与证据 | 支持范围 / 限制 |
|---|---|---|
| `src.nvidia.ufm-41815-port-counters` | [InfiniBand Port Counters](https://networking-docs.nvidia.com/ufmsdnappswum/41815/infiniband-port-counters)，Rcv Errors、Symbol Errors、Link Error Downed、Xmit Discards 行 | 收错包括物理错、畸形包及 overrun；Symbol/Downed 为对应 lane/训练事件；Discards 多因。仅 IB/UFM 字段语义，不证明目标机型具备字段、无漏报或硬件根因。 |
| `src.nvidia.nccl-user-guide-2.27.5` | [SPLIT_DATA_ON_QPS](https://docs.nvidia.com/deeplearning/nccl/archives/nccl_2275/user-guide/docs/env.html#nccl-ib-split-data-on-qps)、[CROSS_NIC](https://docs.nvidia.com/deeplearning/nccl/archives/nccl_2275/user-guide/docs/env.html#nccl-cross-nic)、[ACS](https://docs.nvidia.com/deeplearning/nccl/archives/nccl_2275/user-guide/docs/troubleshooting.html#pci-access-control-services-acs)、[RAS sample output](https://docs.nvidia.com/deeplearning/nccl/archives/nccl_2275/user-guide/docs/troubleshooting/ras.html#sample-output) | split 默认 0 及分摊语义、rail 配置意图与例外、PCI 路径重定向、进度差异可为正常瞬态；不把配置或进度响应当物理错误计数。 |
| `src.nvidia.nccl-issue-2409` | [Issue 正文](https://github.com/NVIDIA/nccl/issues/2409)，Environment、§1 perftest、§2 rail、§3 WQE、§4 sweep | 对应记录 L12 的环境/开帖证据；属于报告者数据及当时假说，不直接当本库复现或最终根因。 |
| `src.nvidia.nccl-issue-2409` | [5660150852](https://github.com/NVIDIA/nccl/issues/2409#issuecomment-5660150852)、[5660232470](https://github.com/NVIDIA/nccl/issues/2409#issuecomment-5660232470)、[5673453587](https://github.com/NVIDIA/nccl/issues/2409#issuecomment-5673453587)、[5699369631](https://github.com/NVIDIA/nccl/issues/2409#issuecomment-5699369631) | 分别对应粒度、QP/深度、修正比较和按请求关闭；记录 L12–13 的阶段链接成立。修正后恢复用于支持原平台/配置原因，不作普遍排除规则。 |
| `src.nvidia.nccl-issue-814` | [Issue 正文](https://github.com/NVIDIA/nccl/issues/814)，拓扑 XML、P2P/pairwise 矩阵及 ring 调整；[1493802672](https://github.com/NVIDIA/nccl/issues/814#issuecomment-1493802672)、[1496450442](https://github.com/NVIDIA/nccl/issues/814#issuecomment-1496450442)、[2283482549](https://github.com/NVIDIA/nccl/issues/814#issuecomment-2283482549)、[2825666454](https://github.com/NVIDIA/nccl/issues/814#issuecomment-2825666454) | 对应记录 L14：多流解释保持推断强度，作者未验证替代 CPU；2.23 避让与 GeForce 支持澄清分开。仅确认映射，不重开 C26。 |
| `src.nvidia.nccl-issue-209` | [Issue 正文](https://github.com/NVIDIA/nccl/issues/209)的 no RDMA / NET/Socket；[491475792](https://github.com/NVIDIA/nccl/issues/209#issuecomment-491475792)的 socket 驱动线程与 MPI 绑定建议 | 对应记录 L15；TCP 个案的一线检查建议，不外推 IB，不当已验证通用修复。 |
| `src.rocm.rocm-systems-therock-10.1`（`src.amd.rccl-docs-10.1.0` HTML 未取成功） | [官方 troubleshooting 源码](https://github.com/ROCm/rocm-systems/blob/therock-10.1/projects/rccl/docs/how-to/troubleshooting-rccl.rst)，Using the RCCL Replayer / Collect the TransferBench data；Git blob `89779e32d545fcd1f61a7dc728e0abf9113bc186` | Replayer 用 collective 日志与 dummy data 回放；TransferBench 对指定设备间并发拷贝做基准。用途分开，不等于真实端点/rail/transport 替代；未构建或运行。 |

没有 curl 返回的原始远程 HTTP 字节，故不补造远程 SHA-256；官方 Git blob SHA 仅是连接器返回的源码对象身份。未打开候选 FaultDiag 的未选版本页面，也不将候选算作已完成设计。以下物理支有限排除和逐轮方案的充分性属于审阅者对证据契约的判断，不声称上游提供了本页的完整实验设计。

## B19-C23 — P2 / OPEN：支持方向已纠正，物理支有限排除仍只有范围声明

位置：正文 L76（步骤 8），共同输入与时窗约束 L51/L58–63；来源记录 L10；修订映射 L116。对应 acceptance 2；关闭条件依据前次报告 L65。

| 子条件 | 判定 | 位置与证据 |
|---|---|---|
| 配置/映射支持与排除方向 | CLOSED | L76 已将“配置不一致纠正后复测恢复”归支持，并明示配置不一致与热点集中分开判读；#2409 修正评论 5673453587 的分步比较与此方向一致。不是排除整个配置分支。 |
| 预期负载、历史对照、端口集中度 | CLOSED | L76 已列入最小输入并引用 T03-07；依赖正文 L146/L148/L156–157 说明请求配置不等于实际路径、热点须同窗端口定位、缺遥测不定位链路/rail。接受为设计层契约，不要求现场数值。 |
| 三域隔离/背景比较与 TCP 边界 | CLOSED | L76 保持 CPU/网/存分别比较、背景退化/隔离恢复、两轮无差以及缺轮/无同窗负载证据不判争用；#209 路径限定正确。各轮具体交付仍归 C24。 |
| 物理支最小字段及限定强度 | CLOSED | L76 新列所选端口/字段、前后值/增量、窗口/重置、路径、掩盖/覆盖声明及 UFM 版本；明确仅陈述事件，Rcv Errors 含 overrun，Discards 多因，ACS 等移回配置支。T03-03 与 UFM 对应字段语义支持这些限定；不把它扩展到未证实 RoCE/HCCS 字段。 |
| 物理支支持、有限排除与 unknown 的完整门禁 | OPEN | L76 的增量/路径关联和字段未选/窗口不齐 unknown 已有进展，但“有限排除（仅排除已观测范围）”没有写何种观测可触发排除。它只限制结论范围，未建立无新增事件、采样/重置有效、路径及覆盖足够时如何判读的条件。列出“重置边界”“掩盖/覆盖声明”也未说明边界不明或覆盖不足时应阻断排除。 |
| 调用/消息实际记录不足 | CLOSED | L76 已写实际 collective、datatype/count/root/rank/次序与消息序列对齐；记录缺失或未能对齐记 unknown。参数差异纠正后恢复归支持、参数一致归该类差异的排除，方向保持正确。 |

**剩余关闭条件：**只补足物理事件支的可判读门禁，不重复已满足的方向修正。明确有效同窗、已选同路径/同作用域字段在覆盖声明允许范围内无新增事件时，最多只能说本窗未观测到这些事件；重置/回退或采样边界无法解释、路径关系/掩盖条件/覆盖不足则保留 unknown，不能凭“已观测范围”一语就进入排除。允许精确链接已有门禁并说明本支如何采用，无需现场数值、命令执行或新增健康/根因结论；继续受 L63 的时窗限制约束，不重开 C22。

## B19-C24 — P2 / OPEN：7→8 已补，9 的出口和四类逐轮方案仍未交付完整

位置：正文 L75–77/L81–94；来源记录 L11；修订映射 L117。对应 acceptance 4；关闭条件依据前次报告 L79。

| 子条件 | 判定 | 位置与证据 |
|---|---|---|
| 步骤 7 下一步分叉 | CLOSED | L75 已有证据齐全且满足完成判据→结束、未完成候选/口径/映射/遥测缺口→8；L76→9 入口也明确。 |
| 步骤 9 返回/结束一致性 | OPEN | L77 动作栏说“对照完成→回步骤 7”“未完成→留 unknown”，但末列仍“满足完成判据后结束”；“步骤 7 末列已同步”不消除本行两个出口。完成判据 L92 又允许记录缺口后结束，未区分可做对照的缺口与本轮无法取得证据、记录 unknown 后结束的缺口。 |
| 四类轮次各自七要素 | OPEN | L77 仍先写“四类轮次各列”七类字段，再在 (i)–(iv) 中各列少数要求；不是逐轮输入、变更/保持、输出、校验/覆盖及判定的完整方案，详见下表。 |
| CPU/网/存背景可重现输入 | OPEN | L77 的“亲和设置/流量配置/后端负载声明”只列类别，没有分别固定负载/工具版本或输入身份、强度与持续时间、作用端点/数据集及复现方式；亲和设置本身不定义 CPU 负载。不能据此声称背景轮可重现。 |
| 测量/回放/解析/真实替代的归位 | CLOSED | L77 明确 Replayer 回放、TransferBench 拷贝基准均不是路径替代，FaultDiag 仅候选；真实替代列端点/HCA/端口/transport，RCCL 档案入口可读。官方源码工具说明支持该用途区分。 |
| 未选工具/版本/输入/能力与平台条件 | CLOSED（降级规则） | L77 已规定未选轮次未完成/unknown，L118 已接通 T03-06 与 RCCL 档案；不能据此认定所有轮次已选定或可执行。缺逐轮具体条件仍计入本项 OPEN，不要求验证未知 HCCL 交集。 |
| 失败停止、恢复与复测边界 | CLOSED | L77 单列正确性失败、超时/异步错误、窗口失效即停；恢复保存原值或批准修复配置，并有同条件正确性/覆盖复测、不新增授权。L81–83 风险边界保持。 |

| 轮次（均只设计不执行） | L77 已给内容 | 尚缺的逐轮交付 |
|---|---|---|
| 隔离基线 | 独占/停背景声明、默认配置全量记录、原生输出存档 | 本轮可比测试输入与批准基线的关系、保持的路径/配置、校验开关和完整性/覆盖准入、基线有效或 unknown 的明确判定。默认配置不能自动代替原批准配置。 |
| 可控背景 | 背景重现类别、同窗同配置与基线比较 | CPU/网络/存储各自可重现负载输入；每次只引入哪一域背景、其余保持什么；背景实际达到声明条件的输出、测试原生输出与校验/完整性、无差/退化/无法比较的本轮判定。 |
| 单变量 | 变量名/原值/新值、其余保持 | 选择哪一类路径/配置变量及版本能力门禁、复用哪套可比输入、应保存哪些实际配置/路径与测试输出、校验/覆盖/unknown 判定；“其余保持”未展开为本轮契约。未选择时须明确未完成。 |
| 替代端点/rail/路径 | 换 rail/NIC/transport、列出端点/HCA/端口/transport 身份 | 被替代项与保持项分别列出、实际替代成功的库/路径证据、与基线匹配的输入/背景、原生输出和校验/覆盖；替代未发生或版本能力未证实时如何 unknown。工具用途列表不能代替此轮。 |

**剩余关闭条件：**把 9 的末列与动作栏统一为回 7 汇总，明确可做对照的未完成候选从 7 进 8/9、无法取得证据的缺口登记 unknown 后如何结束。分别交付四类轮次的七要素与判定，CPU/网/存各有可重现负载输入；可明确复用共同固定字段，但需逐轮指明引用、变更项和保持项。无需测量值，也不要求执行；未选定的轮次如实未完成，不能用“可执行才算完成”这一要求句替代设计交付。保留本轮接受的工具归位、失败停止和恢复边界。

## B19-C27 — P2 / OPEN：案例链接和状态同步已改善，记录仍缺完整映射与第三轮身份

位置：正文 L34/L60/L74/L77/L118–122；来源记录 L3/L9–15/L19；修订映射 L119。对应 acceptance 1–4 的可追溯性；关闭条件依据前次报告 L118。

| 子条件 | 判定 | 位置与证据 |
|---|---|---|
| 案例阶段的 ID—URL—字段—范围 | CLOSED | 记录 L12–15 现有完整 Issue ID、#2409 四条关键评论、#814 四条所采用评论与 #209 绑定评论，字段/阶段/强度已分开；本轮逐条 comment API 与正文核对。L13 不再用“同上”；L12 的“同页”有本行明确 Issue 正文 URL 可解析，但改成 §1–§4 名称会更清楚，不以此单独阻挡关闭。 |
| 时间窗与计数器依赖的完整 ID 映射 | OPEN | L9 仍以“—（方法整理）”作 ID，仅给 T03-07/T03-03 简称和整页链接，未列 `communication.bandwidth-baselines` / `communication.rdma-baseline-and-congestion-triage`。L10 新采用 UFM 字段仍未列已登记 `src.nvidia.ufm-41815-port-counters` 及其精确页/字段/IB 范围。NCCL 三个精确锚点不覆盖 UFM。 |
| 对照/工具的来源定位 | OPEN | L11 已改“RCCL 档案工具节”，不再错称两节点设计节，完整 RCCL 登记 ID 也存在；但本行仍无 #2409 精确 URL、RCCL 官方工具节 URL 或 `therock-10.1` 具体文件 URL，档案链接也未列内容 ID `communication.rccl-runtime-and-verification`。未形成全部主张的完整映射。FaultDiag 未选候选的降级接受，不要求把它算作已采用来源。 |
| 悬空代号的定义/删除 | OPEN | L3 的 C1/C2/C3/S1–S7，L19 的 C2 修复 release、C3 独立测量、C1 期望及 S4/S5/S6/S7，仍无本记录内完整 ID—具体来源映射；仅给“未采用”“候选”不能让这些代号可解析。允许删除未采用代号并用明确名称记录 unknown。 |
| 旧遥测缺口三处原批限定 | CLOSED | L60、步骤 6 L74 末列、待确认 L122 均显式限定原批 Batch 09，区分当前 T03-03 UFM/mlx5/Cumulus 文档已核对与目标现场能力 unknown；记录 L19 同步。L74 中段旧句仍在，但同行末列已限定其范围，不再按全库尚无来源解读。 |
| 矩阵字段契约状态 | CLOSED | 正文 L34/L119、记录 L9/L19 与 T03-07 L144–161 一致为字段契约/判据，实测矩阵未交付。没有用“数值已填”或结构通过推导实测。 |
| T03-06、RCCL 档案及作者记录入口 | CLOSED | 正文 L77/L118 接通 T03-06 与 RCCL 档案，L120 接通本页作者记录并保留 Batch 09 历史入口；文件及所引用章节存在。入口有效不代替记录表的完整内容 ID 和精确来源定位。 |
| verification 轮次与角色 | OPEN | 记录 L3 现为作者首轮＋第一次修订＋第二次修订、审阅初审＋一/二次定向复核；没有本次第三轮作者修订的取证范围或“未新增取证、仅复用”声明。正文 L34 仍“首轮＋第二轮＋本轮”三阶段，未与明确的首次/第二次/第三次修订逐一对应；映射 L119 的“三轮次/角色同步”不能证明实际轮次已同步。 |

**剩余关闭条件：**补 L9 的完整内容 ID、L10 的 UFM 登记 ID—精确页—字段/版本/IB 及未覆盖范围、L11 的官方工具节/固定源码文件与对应内容 ID，区分已采用证据和未采用候选；定义或删除悬空代号。按实际作者首轮、第一次修订、第二次修订、第三次修订分别说明取证或复用范围，正文 verification 与作者记录同步，并继续把独立审阅者取证分开，不能代作者补造历史实开或模型执行元数据。保留已满足的案例映射、三处遥测历史限定、矩阵字段契约及入口。

## 状态集合与验收影响

| 状态 | ID / 范围 |
|---|---|
| 本轮 CLOSED（整项） | 无 |
| 本轮 OPEN（3 P2） | C23、C24、C27 |
| 既有 CLOSED（24；不重开） | C01–C22、C25、C26 |
| 本批累计审阅发现 | **24 CLOSED / 3 OPEN**（共 27 个 ID，未新增） |
| 既有验收子项 OPEN（单列） | BLOCKED-1，blocked_on_evidence；不计入发现数量 |
| T03-08 | **第三次定向复核未通过**；下一轮仅复核本文三项剩余关闭条件 |
| T03-06/T03-07 | 已交付有限文档/来源范围通过保持，不重新验收 T03-06 acceptance 5 |
| Batch 19 | 未完成整批验收，不由本次已满足子条件推导全部完成 |

acceptance 1 的时窗/矩阵字段契约保持既有接受，不重开 C22；acceptance 2 的物理支有限排除仍由 C23 阻挡；acceptance 3 的既有案例正文结论保持，不重开 C25/C26，但完整来源/轮次记录仍受 C27 限制；acceptance 4 的逐轮设计和统一出口仍由 C24 阻挡。模型审阅、来源可读和结构校验均不建立硬件验证或版本兼容交集。

## 检查边界与写入范围

- 仅新增本报告；不改正文、作者记录、映射、登记、计划、索引或来源审计。工作区既有改动不恢复、不提交、不创建分支。
- 不执行 benchmark、collective/MPI、实机采集、配置修改、故障注入或上游诊断命令；所有上游示例均仅作阅读。未取得现场遥测、跨节点时钟、字段能力或测试结果。
- 未核验 nccl-tests#309 的期望来源、未补取 FaultDiag 候选、未验证 HCCL Test × CANN/HDK/机型交集；这些 unknown 保留。本轮剩余问题沿用 C23/C24/C27，不新增发现 ID。
- curl 未取得原始远程响应；允许的替代只读通道完成所列关键语义核对。RCCL 使用已登记 tag 官方源码，不冒充 HTML 访问或作者历史执行证据。
- 为遵守“只写这一份报告”，在含本报告的临时仓库快照执行 `make check` / `make build`，均 PASS（88 content entries / 389 sources）。构建产物仅写临时快照，原仓库 `build/` 不重建；未修改 `src/kb/`，不执行 `make test`。结构和本地链接通过不验证技术正确性或远程语义。
- 本报告 10 处本地链接、10 个不同目标均存在。写入前后 SHA-256 清单核对：原有 2488 个受保护文件（含既有构建文件及本地环境文件）均不变、无删除，仅新增本报告；五项任务输入与输入 SHA 表一致。临时快照与清单位于仓库外，不作为现场验证证据。
