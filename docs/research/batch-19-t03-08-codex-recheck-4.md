# 第十九批 T03-08 第四次定向复核

审阅日期：2026-10-13（Asia/Shanghai，本机日期确认）。正文 `updated_at: 2026-10-14` 及部分来源登记日期晚于本轮实际日期，只视为作者交付标签，不作为本轮取证日期或历史执行证明；输入身份以下表 SHA-256 为准。

**结论：C23、C24、C27 仍 OPEN（3 项 P2），本轮没有整项 CLOSED。本批累计 24 CLOSED / 3 OPEN（共 27 个审阅发现），T03-08 第四次定向复核未通过。** C01–C22、C25、C26 沿用既有 CLOSED，不重开。BLOCKED-1（HCCL Test × 目标 CANN/HDK/机型官方交集）仍按前次报告单列 blocked_on_evidence/open，不计入发现数量；T03-06/T03-07 的有限文档/来源范围通过保持，整个 Batch 19 不因本次局部复核而验收。

约定配置 `gpt-6.1-sol / xhigh` 仅为用户约定，不写成已独立确认的执行模型或推理等级。执行者为当前 Codex 主会话，角色为独立审阅者，与作者修订角色分开；无子代理。本轮只写本报告，不代作者修订，不新增发现 ID。下表子条件 CLOSED/OPEN 不产生新 ID，也不改变整项累计计数。

## 输入与复核范围

| 输入 | SHA-256 |
|---|---|
| [T03-08 正文](../../knowledge/03-communication/bandwidth-degradation-triage.md)（procedure / draft） | `5bd51422dfbff66c387f3ab678f0b526bea6cdc0c6a3a24eefcb0a08aedc60ff` |
| [作者来源记录](batch-19-t03-08-sources.md) | `dc469a85d8ae4d51246e3777f774de68a69d02b93a3d349ba0214431c0744884` |
| [修订映射](batch-19-review-fixes.md)（第四轮修订节 L121–125） | `9136faf9b6af5a21aa78e316b7f6dd663b1f9c422844f6d3c227797adec18594` |
| [第三次定向复核](batch-19-t03-08-codex-recheck-3.md)（剩余关闭条件权威来源：C23 L62、C24 L85、C27 L102） | `70d1fd3f96440816a5792b97b03727572421bfdf14736a2520b327c30ae94123` |
| [任务验收](../../plans/full-coverage-backlog.yaml)（T03-08 acceptance 1–4，L5006–5010） | `121826a4d499273e7f6a00735e0a53931eef5c097bd66ab6b2425fdbc36ddfe0` |

逐项核对实际正文、作者记录及一次源，不以修订映射 L123–125 的完成自述替代交付。只检查 C23 的物理支剩余门禁、C24 的出口及逐轮设计、C27 的映射与轮次；已经关闭的其余子条件保持，不重新审阅案例发现 C25/C26。对依赖条目和登记只读解析，不重开其历史发现。

| 补充只读输入 | SHA-256 |
|---|---|
| [来源登记](../../sources/registry.yaml) | `277aecb64892438a366c1729fe01210cbeae60845ff6fbefce437a7a7a96901e` |
| [T03-07 基线口径](../../knowledge/03-communication/bandwidth-baselines.md)（矩阵 L144–161） | `8c2884b63cf7b638c1df2d7de88f5fe9d2923c0d95b025548041aea203574039` |
| [T03-03 RDMA 诊断](../../knowledge/03-communication/rdma-baseline-and-congestion-triage.md)（计数器 L79–98、覆盖门禁 L137–146） | `7f6d59752e7c74628f2c9d706ce2ec00e3031ecd36230554eb8d2680fee67412` |
| [T03-05 RCCL 档案](../../knowledge/03-communication/rccl-runtime-and-verification.md)（工具 L66–71、测试覆盖 L78） | `1f95d5b310726d858900e2028ab3b779f1470b03a1ba67187fbed1c6da5b19db` |
| [T03-06 三库对照](../../knowledge/03-communication/communication-library-profiles.md)（工具 L65、交集限制 L74–76） | `d4a5fb535ba78d852e070f09ff387b69dc6e1ab7cf86620c7ee08e9a99577646` |

## 一次源取证与方法限制

采用本地只读逐行检查、默认 TLS 校验的只读 curl、允许的网页阅读器与 GitHub 连接器。curl 分别请求 UFM 4.18.15 端口计数器页、NCCL 2.27.5 env 页、RCCL docs-10.1.0 troubleshooting 页，均沙箱 DNS 失败：exit 6、HTTP 000、下载 0 字节。HTTP 000 不是上游状态；未使用 `-k/--insecure`，未修改网络或 TLS 配置。

网页阅读器取得 UFM、NCCL env/ACS/RAS 精确页及 #2409 正文。RCCL docs-10.1.0 HTML 阅读返回 Internal Error；改由 GitHub 连接器取得已登记 `therock-10.1` 官方文档源码，并用登记对应的完整 commit 再取工具节。两次返回相同 Git blob SHA；**不声称 HTML 已打开成功或与源码全文相同**。另以精确 comment API 核对 #2409 修正回复、#209 socket 绑定建议。本轮未重新打开 #814 全部评论，案例映射已 CLOSED 部分沿用前次结果，不冒充本轮全量复核。

| 一次源 / 已登记 ID | 本轮精确定位与证据 | 支持范围 / 限制 |
|---|---|---|
| `src.nvidia.ufm-41815-port-counters` | [InfiniBand Port Counters](https://networking-docs.nvidia.com/ufmsdnappswum/41815/infiniband-port-counters)，Rcv Errors、Symbol Errors、Link Error Downed、Xmit Discards 行；登记 L4520–4530 | 收错包含 overrun；Symbol/Downed 为相应 lane/训练事件；Discards 多因。仅 IB/UFM 字段语义，不证明现场字段可用、覆盖充分或硬件根因。零新增及覆盖门禁是本页判读契约，不冒充厂商提供了完整排除流程。 |
| `src.nvidia.nccl-user-guide-2.27.5` | [SPLIT_DATA_ON_QPS](https://docs.nvidia.com/deeplearning/nccl/archives/nccl_2275/user-guide/docs/env.html#nccl-ib-split-data-on-qps)、[CROSS_NIC](https://docs.nvidia.com/deeplearning/nccl/archives/nccl_2275/user-guide/docs/env.html#nccl-cross-nic)、[ACS](https://docs.nvidia.com/deeplearning/nccl/archives/nccl_2275/user-guide/docs/troubleshooting.html#pci-access-control-services-acs)、[RAS sample output](https://docs.nvidia.com/deeplearning/nccl/archives/nccl_2275/user-guide/docs/troubleshooting/ras.html#sample-output) | split 默认值及分摊方式、rail 配置意图与例外、PCI 重定向、活跃作业进度差异可为瞬态；分别支持记录 L10 对应字段，不代替 UFM 来源。 |
| `src.nvidia.nccl-issue-2409` | [Issue 正文](https://github.com/NVIDIA/nccl/issues/2409)，§1 perftest、§2 rail、§3 WQE、§4 sweep；[修正回复 5673453587](https://github.com/NVIDIA/nccl/issues/2409#issuecomment-5673453587)（精确 API 同时核对） | 报告者的跨层/配置对照与纠正后复测；只作设计借鉴和已关闭方向条件的核对，不把个案当本库实验或厂商完整四轮方案。 |
| `src.nvidia.nccl-issue-209` | [绑定建议 491475792](https://github.com/NVIDIA/nccl/issues/209#issuecomment-491475792)（精确 API 核对） | socket 驱动线程与 MPI 绑定的一线建议；不定义可重现 CPU 背景负载，也不证明通用修复。TCP 边界沿用既有 CLOSED。 |
| `src.rocm.rocm-systems-therock-10.1`（`src.amd.rccl-docs-10.1.0` HTML 未取成功） | [官方 troubleshooting 固定文件](https://github.com/ROCm/rocm-systems/blob/7da43026e4f2ef7600433c38c820732f7a205d22/projects/rccl/docs/how-to/troubleshooting-rccl.rst)，Using the RCCL Replayer / Collect the TransferBench data；commit `7da43026e4f2ef7600433c38c820732f7a205d22`，Git blob `89779e32d545fcd1f61a7dc728e0abf9113bc186` | Replayer 用 collective 日志和 dummy data 回放；TransferBench 对指定设备间并发拷贝做基准。用途区分保持；不等于实际端点/rail/transport 替代。未构建或运行。 |

未取得 curl 原始远程响应字节，不补造远程 SHA-256；Git blob SHA 是连接器返回的源码对象身份，不混作 SHA-256。未取未选版本的 FaultDiag/ROCm 注记/HCCL 工具介绍候选，也不把候选升级为已完成设计。下面对门禁、逐轮方案及记录充分性的判定属于审阅者依据前次关闭条件作出的判断。

## B19-C23 — P2 / OPEN：边界门禁已补，仍缺无新增事件这一观测条件

位置：正文 L76 的物理错误支，时窗约束 L63；来源记录 L10；修订映射 L123。对应 acceptance 2；依据前次报告 L62。

| 子条件 | 判定 | 位置与证据 |
|---|---|---|
| 同窗、同路径/作用域、采样/重置、关系与覆盖门禁 | CLOSED | L76 已明确上述条件同时成立才允许有限结论；重置/回退、采样边界不明、路径关系/掩盖条件/覆盖不足均 unknown。接受为设计层门禁，不要求现场数值。 |
| 结论强度不超过本窗所选事件 | CLOSED | L76 明示最多为“本窗未观测到这些事件”；字段未选/窗口不齐仍 unknown，不升级为健康或硬件根因。 |
| 触发“本窗未观测”的观测值条件 | OPEN | L76 的同时成立列表没有“所选事件在有效窗口内无新增事件/错误事件 delta 为零”，也未精确引用一个含该条件的判读门禁。前后值/增量被要求记录，但没有接入有限排除条件；窗口、路径、覆盖均有效而存在正增量的情形也未在该列表中被阻断。不能由结论句本身反推观测已无新增。T03-03 L87 的零增量要求不能由泛链接自动补成该支完整条件。 |
| 其余已经 CLOSED 子条件 | CLOSED（保持） | 配置纠正后恢复归支持、预期负载/历史/集中度、CPU/网/存分域对照及 TCP 边界、物理字段限定、调用实际记录不足 unknown，均按前次 L55–60 保持；本轮不重开。 |

**剩余关闭条件：**只在本支现有同时成立列表中补入有效同窗、所选同路径/同作用域事件“无新增”的观测条件，或精确链接并明确采用包含该条件的门禁；正增量不得进入“本窗未观测”，不可解释的 delta 仍 unknown。保留已满足的采样/重置、掩盖/覆盖和强度限定，不要求现场测量、统一清零全部正常流量计数器或新增健康结论。

## B19-C24 — P2 / OPEN：逐轮条目有进展，出口与完整设计仍不足

位置：正文 L75、L77–82、L92–97；来源记录 L11；修订映射 L124。对应 acceptance 4；依据前次报告 L85。

| 子条件 | 判定 | 位置与证据 |
|---|---|---|
| 步骤 7 下一步分叉 | CLOSED（保持） | L75 仍为证据齐全且满足完成判据→结束、未完成候选/缺口→8；按前次已接受结果保持。 |
| 可做对照与无法取得证据的缺口区分 | CLOSED（文字条件） | L82 新说明可做对照的缺口走 7→8→9，无法取得证据者登记 unknown 后按完成判据 4 结束。此次补充解决前次要求的缺口类别区分，但不等于出口已统一。 |
| 步骤 9 所有诊断出口统一回 7 | OPEN | L77 及 L82 仍只把“对照完成”送回 7，“未完成”留 unknown；L82 另允许无法取证者直接按判据 4 结束，没有统一经 7 汇总。并且 L77 的表格行只交付步骤与动作两列；L78–82 已转为段落/列表，运行影响、预期证据和下一步的尾部 `\|` 单元格文本落在 L82 列表项中，未形成 L67 五列表的步骤 9 完整行。旧“满足完成判据后结束”虽已删除，但不能据尾部文字认定表格出口交付完成。这是同一 C24 的出口/呈现问题追记，不新增 ID。 |
| 四类轮次逐轮七要素与判定 | OPEN | L79–82 新增逐轮输入/变更/保持/输出/判定，比只列总要求有进展；但背景、单变量轮缺明确的本轮校验/完整性/覆盖准入或共同门禁引用，隔离轮“基线有效”未说明准入条件，替代轮“其余”也未形成可核对的保持项契约。具体剩余项见下表。 |
| CPU/网/存可重现背景输入 | OPEN | L80 的 CPU 亲和设置＋计算负载声明、网络流量配置＋端点声明、存储后端负载＋数据集声明仍是字段类别。未分别规定负载/工具版本或输入身份、强度/并发与持续时间、作用对象和复现方法；新增“实际达到声明的输出”不能替代这些输入。 |
| 未选条件、工具归位、失败停止与恢复 | CLOSED（保持） | L82 保留未选版本/输入/能力→未完成/unknown，Replayer/TransferBench 不作路径替代，FaultDiag 保留候选；正确性失败、超时/异步错误、窗口失效即停，保存原值或批准修复配置恢复并同条件复测。官方固定源码工具节支持用途区分；不据 unknown 声明认定轮次已完成。 |

七要素按前次关闭条件解释为：隔离条件、背景负载、路径变量（变更/保持分开）、可比输入、原生输出、校验/完整性、判定/无法判断。允许复用正文 L51/L63 与步骤 1–3 的共同输入及门禁，但各轮须明确采用哪些共同条件，不能只靠读者推定。以下均是设计交付要求，不要求实测结果。

| 轮次 | 本轮实际新增 / 可接受部分 | 尚缺的逐轮交付 |
|---|---|---|
| 隔离基线（L79） | 工具/库、算子/消息/映射、拓扑/并发输入；停背景、路径/配置保持、原生输出、错误/覆盖/缺行声明；明确默认不代替批准配置 | 明确复用哪套固定输入及批准配置；校验开关/完整性/覆盖准入如何使基线有效或 unknown。仅列 `#wrong`、覆盖、缺行字段和“基线有效”不是准入判定。 |
| 可控背景（L80） | 每次只引入一域背景，其余两域保持；有同窗指标和背景达到声明的输出；退化/无差/无法比较分开 | CPU/网/存分别可重现输入；基线测试输入、路径/配置、隔离条件的保持关系；测试原生输出及校验/完整性/覆盖准入，或明确复用共同门禁。 |
| 单变量（L81） | 指向基线可比输入；给出 rail/NIC/transport/算法/协议候选及能力声明，保存实际配置/路径和测试原生输出 | 接通 L77 的变量名/原值/新值契约；明确隔离/背景和不变项、每轮校验/完整性/覆盖准入及判定。版本能力未知、变量未选择时的未完成声明保留，不把候选清单当已选方案。 |
| 替代端点/rail/路径（L82） | 与基线匹配的输入/背景；替代端点/HCA/端口/transport；实际替代证据、原生输出、校验/覆盖；替代未发生/能力未知→unknown | 把“其余”落实为保持的配置、测试口径和隔离条件或明确共同契约；说明校验/覆盖有效才进入性能差异判读。替代成功只是路径干预发生，不是完整性能对照已经有效。 |

**剩余关闭条件：**把步骤 9 恢复为可解析的完整五列表格行（详案可放表外并精确引用），完成与未完成/unknown 均回 7 汇总，再由 7 决定继续 8/9 或按完成判据结束；风险触发停止保持独立。逐轮补齐七要素及有效/unknown 判定，可显式复用共同固定输入和门禁；CPU/网/存分别给可重现负载输入契约，未选的版本/输入/能力如实未完成。无需执行 benchmark，也不要求为未知 HCCL 交集虚构可运行方案。

## B19-C27 — P2 / OPEN：新增两个 ID，精确定位、代号及轮次仍未闭环

位置：来源记录 L3/L9–11/L19；正文 L34/L60/L74/L123–127；修订映射 L125。对应 acceptance 1–4 的可追溯性；依据前次报告 L102。

| 子条件 | 判定 | 位置与证据 |
|---|---|---|
| L9 完整内容 ID | OPEN | L9 仍以“—（方法整理）”为 ID，正文链接仍只有 T03-07/T03-03 简称；未列 `communication.bandwidth-baselines` / `communication.rdma-baseline-and-congestion-triage`。两个完整内容 ID 确实存在于依赖正文 L2，映射 L125 自述已补与记录不符。 |
| L10 UFM 登记 ID—精确页—字段—范围 | OPEN（ID 部分满足） | L10 已新增 `src.nvidia.ufm-41815-port-counters`，登记 L4520–4530 存在；但 UFM 定位仍只链接 T03-03，不含登记的精确 NVIDIA 页面。已有 UFM 4.18.15 和字段简称，却未明确 IB 支持及不覆盖 RoCE/HCCS/目标现场能力的范围。NCCL 三个精确锚点不能代替该来源定位。 |
| L11 官方工具节与内容 ID | OPEN（内容 ID 部分满足） | 新增 `communication.rccl-runtime-and-verification`，对应档案 L2/L66–71 存在；本行仍无 #2409 精确 URL、RCCL 官方工具节 URL 或 `therock-10.1` 固定文件 URL，只给内部档案链接及“§1–§4”/工具名称。正文 L82 的 HTML 链接不能代作者记录补成完整映射；本轮取得的固定源码也不倒灌为作者历史已取得。 |
| 悬空代号定义/删除 | OPEN（部分改善） | L3 已给 C1/C2 与 #2409/#209、S1/S2/S3/S7 与具体名称的对应，可借 L10/L12–15 解析相关 ID/链接。C3 仍只是“ROCm 注记”，没有具体条目/完整 ID/精确页；S5 FaultDiag、S6 HCCL 工具介绍也未定位版本或明确来源对象，L19 继续使用。未采用候选可删除代号、用明确名称及未选择状态记录；不要求为凑齐 ID 强行采用候选。 |
| 旧遥测三处原批限定 | CLOSED（保持） | L60、步骤 6 L74 末列、待确认 L127 及记录 L19 保留原批限定，区分当前 T03-03 文档与目标现场能力 unknown；沿用前次接受。中段历史旧句不扩大解释为全库缺源。 |
| 矩阵字段契约状态 | CLOSED（保持） | 正文 L34/L124 与记录 L9/L19 均为字段契约已引用、实测矩阵未交付，依赖 T03-07 L144–161 未变化；无实测或平台兼容外推。 |
| T03-06/RCCL 档案/作者记录入口 | CLOSED（保持） | 正文 L82/L123/L125 接通三个入口，历史 Batch 09 入口也保留；目标文件存在。入口正确不替代 L9–11 的 ID—精确来源映射。 |
| verification 轮次与角色同步 | OPEN | 记录 L3 写首轮＋首次/二次/三次修订，随后又重复首次/二次修订；独立审阅只列初审＋一/二次复核，未纳入已存在的第三次复核。正文 L34 仍为首轮＋第二轮＋第三次修订，不能逐一对应首次/二次/三次修订；记录第三次“本轮”未说明新增取证或复用，与正文第三次“无新增远程取证，仅复用”也未明确同步。当前第四轮修订的范围未单列。角色分开这一原则已写出，但实际轮次不一致。 |

记录 L3 的“首轮 S1–S7 实开”与 L19 的 S6“未实开”、S4“HTML 未取成功，仅源码”还缺明确的轮次/执行角色限定；不能仅凭本轮来源可读取就证明作者历史全量实开。这仍是 C27 的记录一致性问题追记，不另立发现 ID，也不据通道失败否认可能存在的作者历史证据。

**剩余关闭条件：**补 L9 两个完整内容 ID；补 L10 已登记 UFM 精确页、完整所选字段及版本/IB/未覆盖范围；补 L11 #2409 精确定位、RCCL 官方两个工具节或固定源码文件，保留已补内容 ID，明确已采用证据与未采用候选。定义尚不可解析的 C3/S5/S6，或删除其代号并如实记录未知。按作者首轮、首次/二次/三次修订逐项说明取证或复用，去掉重复轮次；为本次第四轮另注实际范围，与正文 verification 同步，审阅初审及一/二/三次复核作为独立角色历史分开。不要为补记录而编造历史实开、模型执行元数据或现场结果。保留已经 CLOSED 的案例映射、遥测历史限定、矩阵状态及入口。

## 状态集合与验收影响

| 状态 | ID / 范围 |
|---|---|
| 本轮 CLOSED（整项） | 无 |
| 本轮 OPEN（3 P2） | C23、C24、C27 |
| 既有 CLOSED（24；不重开） | C01–C22、C25、C26 |
| 本批累计审阅发现 | **24 CLOSED / 3 OPEN**（共 27 个 ID，未新增） |
| 既有验收子项 OPEN（单列） | BLOCKED-1，blocked_on_evidence；不计入发现数量 |
| T03-08 | **第四次定向复核未通过**；下一轮只复核上述三个 ID 的剩余关闭条件 |
| T03-06/T03-07 | 有限文档/来源范围通过保持，不重新验收 T03-06 acceptance 5 |
| Batch 19 | 未完成整批验收，不由部分子条件 CLOSED 推导全部完成 |

acceptance 1 的时窗/矩阵契约保持，不重开 C22；acceptance 2 的物理支有限排除由 C23 阻挡；acceptance 3 的既有案例正文结论保持，不重开 C25/C26，来源定位和轮次仍受 C27 限制；acceptance 4 的统一出口、可重现背景及逐轮完整设计由 C24 阻挡。来源可读、模型审阅和结构校验均不建立硬件验证或版本兼容交集。

## 检查边界与写入范围

- 仅新增本报告；不改正文、作者记录、映射、登记、计划、索引或来源审计。工作区既有改动不恢复、不提交、不创建分支。
- 不执行 benchmark、collective/MPI、实机采集、配置修改、故障注入或上游诊断命令；上游示例仅作阅读。未取得现场遥测、时钟、字段能力或实验结果。
- 未补取 nccl-tests#309 的期望来源、未选 FaultDiag 候选或 HCCL Test × CANN/HDK/机型交集；相应 unknown/blocked_on_evidence 保留。新遇到的出口表格与取证记录一致性问题按 C24/C27 追记，无新发现 ID。
- curl 未取得原始远程响应；允许的替代只读通道完成上述关键语义核对。RCCL 用已登记版本线的固定官方源码，不冒充 HTML 或作者历史执行证据。
- 为遵守“只写这一份报告”，在含本报告的仓库外临时快照执行 `make check` / `make build`，均 PASS（88 content entries / 389 sources）；原仓库 `build/` 不重建。未改 `src/kb/`，不执行 `make test`。结构及本地链接通过不验证技术正确性、表格呈现或远程语义。
- 本报告 10 处本地链接、10 个不同目标均存在。写入前后 SHA-256/符号链接清单核对：原有 3478 个常规文件（含 `.git`、既有构建文件和本地环境文件）与 3 个符号链接均不变，无删除，仅新增本报告；五项任务输入与输入 SHA 表一致。临时快照与清单均在仓库外，不作为现场验证证据。
