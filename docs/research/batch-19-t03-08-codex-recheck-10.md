# 第十九批 T03-08 第十次定向复核

审阅日期：2026-10-13（Asia/Shanghai，本机日期确认）。正文 `updated_at: 2026-10-14` 及部分来源登记日期晚于实际日期，仅视为作者交付标签，不作为本轮取证日期或历史执行证明；输入身份以下表 SHA-256 为准。

**结论：C27 仍 OPEN（1 项 P2）；C24 CLOSED 保持，不重开。本批累计 26 CLOSED / 1 OPEN（共 27 个审阅发现），T03-08 第十次定向复核未通过。** 接受当前输入“作者十轮＋审阅十份”的数量进展、第十轮标题正确引用前次 26/1，以及来源记录对第八轮 S7 倒记的清理和第三/第四轮 unknown 分列。但第九轮错误累计与八轮/八份旧自述未纠正或限定，第五轮计数仍未澄清，逐轮对象/版本/入口及首轮对应关系未闭环，新增与撤回的历史取证自述未解释，正文 verification 未精确指向账本及未解历史范围。最新标题和“已交付”自述不能替代这些落盘条件。C01–C26 均保持 CLOSED；BLOCKED-1（HCCL Test × 目标 CANN/HDK/机型官方交集）单列 `blocked_on_evidence/open`，不计入发现数量。T03-06/T03-07 有限文档/来源范围通过保持，整个 Batch 19 不因此验收。

约定配置 `gpt-6.1-sol / xhigh` 仅为用户约定，不写成已独立确认的执行模型或推理等级。执行者为当前 Codex 主会话，角色为独立审阅者，与作者修订角色分开；无子代理。只写本报告，不代作者修订，不新增发现 ID；本轮记录问题均按原 C27 追记。子条件不产生新 ID，也不单独计入累计数量。

## 输入与复核范围

| 输入 | SHA-256 |
|---|---|
| [T03-08 正文](../../knowledge/03-communication/bandwidth-degradation-triage.md)（procedure / draft） | `24ea20c8632a9e592eaf289e7da15b89f91620ac1652efdecc024adef29e9f0d` |
| [作者来源记录](batch-19-t03-08-sources.md) | `baf10b204abbbb4241f9f7bdf2982222eb4c2c41be7dec696d037f11fe944413` |
| [修订映射](batch-19-review-fixes.md)（第十轮 L153–155；历史 T03-08 节 L97–151） | `b4139d1f734188c9f2c69e140a0f672335464a9224bfb126d0c0dcfc636b178c` |
| [第九次定向复核](batch-19-t03-08-codex-recheck-9.md)（C27 L65–111；剩余关闭条件 L106–112；累计状态 L114–128） | `9d0027c03fd59529cb8d7f8e6b246d1e998e6752354df4a8c72fd510a9135b10` |
| [任务验收](../../plans/full-coverage-backlog.yaml)（T03-08 acceptance 1–4，L5006–5010） | `121826a4d499273e7f6a00735e0a53931eef5c097bd66ab6b2425fdbc36ddfe0` |

第九次报告为本轮剩余关闭条件的权威来源。本轮只复核 C27 及其已接受条件是否保持；C24 已 CLOSED 保持，不重新评审其技术契约。不重验 C22 时窗、C23 物理分支，不重新判定 #2409/#814/#209 案例原因、反证或修复结论，不重新验收 T03-06 acceptance 5。历史报告的输入 SHA 标识当时交付，不用本轮最终文件倒补历史。

| 补充只读输入 | SHA-256 |
|---|---|
| [来源登记](../../sources/registry.yaml) | `277aecb64892438a366c1729fe01210cbeae60845ff6fbefce437a7a7a96901e` |
| [T03-07 基线口径](../../knowledge/03-communication/bandwidth-baselines.md)（矩阵 L144–161） | `8c2884b63cf7b638c1df2d7de88f5fe9d2923c0d95b025548041aea203574039` |
| [T03-03 RDMA 诊断](../../knowledge/03-communication/rdma-baseline-and-congestion-triage.md) | `7f6d59752e7c74628f2c9d706ce2ec00e3031ecd36230554eb8d2680fee67412` |
| [T03-05 RCCL 档案](../../knowledge/03-communication/rccl-runtime-and-verification.md)（工具 L69–71） | `1f95d5b310726d858900e2028ab3b779f1470b03a1ba67187fbed1c6da5b19db` |
| [T03-06 三库对照](../../knowledge/03-communication/communication-library-profiles.md)（工具 L65、交集限制 L74–76） | `d4a5fb535ba78d852e070f09ff387b69dc6e1ab7cf86620c7ee08e9a99577646` |
| [第八次定向复核](batch-19-t03-08-codex-recheck-8.md)（历史清理/交付边界 L81/L86/L90；累计 L116） | `fb791dcda229dc1d3bfb8a060f17daa17180c14f56f668ecaa601a2994604071` |
| [第六次定向复核](batch-19-t03-08-codex-recheck-6.md)（历史轮次与取证记录 L101） | `2b8395444ab5236e658b3fbaa1430e6735a9ca742142bef59d70b47b2602768a` |

## 一次源取证与方法限制

采用本地只读逐行核对、默认 TLS 校验的只读 curl、允许的网页阅读器及 GitHub 连接器。curl 请求 UFM 精确端口页、RCCL docs-10.1.0 troubleshooting 页与 #2409 均 DNS 解析失败：exit 6、HTTP 000、下载 0 字节。HTTP 000 不是上游状态；未使用 `-k/--insecure`，未修改网络或 TLS 配置。

网页阅读器返回 UFM、NCCL 2.27.5 env/ACS/RAS 精确页面和 #2409 正文，抓取标记为 today；其解析文本不等同于本机直接 HTTP 实测或可留存的原始响应。RCCL HTML 阅读器仅返回 `Internal Error`，没有 HTML 正文或可独立确认的 HTTP 状态。RCCL 改用连接器读取作者所链 tag 及已登记固定 commit 的同路径源码；仅核对工具用途，不声称 HTML 成功实开、HTML 与源码全文等同，或作者历史上完成了本轮审阅取证。网页阅读器坐标仅用于本轮页面定位，不转成源码 GitHub 行锚点；源码位置采用连接器请求的原文件范围。

| 一次源 / 已登记 ID | 本轮精确定位与证据 | 支持范围 / 限制 |
|---|---|---|
| `src.nvidia.ufm-41815-port-counters` | [InfiniBand Port Counters](https://networking-docs.nvidia.com/ufmsdnappswum/41815/infiniband-port-counters)，阅读器 L121–133：`Rcv Errors`、`Symbol Errors`、`Link Error Downed`、`Xmit Discards` 四项全名；登记 L4520–4530 | 对应记录 L10 的 UFM 4.18.15 / IB 范围；收错包含 overrun，丢弃有多因。不证明 RoCE/HCCS/现场字段能力。完整后缀 `4.18.15-LTS-2024-U5` 未由本轮版本选择器独立读到，不重开已接受范围。 |
| `src.nvidia.nccl-user-guide-2.27.5`：env | [SPLIT_DATA_ON_QPS 节](https://docs.nvidia.com/deeplearning/nccl/archives/nccl_2275/user-guide/docs/env.html#nccl-ib-split-data-on-qps)，阅读器 L599–606：split/round-robin 与默认值；登记 L267 起 | 对应记录 L10/L19 的变量页映射，文档默认值不等于现场配置。 |
| 同一 NCCL 归档 ID：ACS | [troubleshooting 的 ACS 节](https://docs.nvidia.com/deeplearning/nccl/archives/nccl_2275/user-guide/docs/troubleshooting.html#pci-access-control-services-acs)，阅读器 L50–54：PCI 路径重定向 | 属 troubleshooting 页，不是 env 页；只核对来源归属，不执行页内诊断或配置命令。 |
| 同一 NCCL 归档 ID：RAS | [RAS sample-output 节](https://docs.nvidia.com/deeplearning/nccl/archives/nccl_2275/user-guide/docs/troubleshooting/ras.html#sample-output)，阅读器 L19–85：活跃通信、初始化/销毁过渡与重复查询限定 | 独立子页，不是 env 页；对应记录 L10/L19，不建立链路级硬件证据。 |
| `src.nvidia.nccl-issue-2409` | [Issue 正文](https://github.com/NVIDIA/nccl/issues/2409)，阅读器 L173–215：§1 perftest、§2 rail、§3 debug/WQE、§4 env sweep；登记 L4830–4840 | 仅核对记录 L11 的设计借鉴定位；四类轮次为本库设计归纳，不重新判定案例结论。 |
| `src.rocm.rocm-systems-therock-10.1`；关联 HTML ID `src.amd.rccl-docs-10.1.0` | [作者所链 tag 文件](https://github.com/ROCm/rocm-systems/blob/therock-10.1/projects/rccl/docs/how-to/troubleshooting-rccl.rst) L129–226；[固定 commit 文件](https://github.com/ROCm/rocm-systems/blob/7da43026e4f2ef7600433c38c820732f7a205d22/projects/rccl/docs/how-to/troubleshooting-rccl.rst) L129–203。Using the RCCL Replayer 与 Collect the TransferBench data 两节可定位；两 ref 返回 Git blob `89779e32d545fcd1f61a7dc728e0abf9113bc186` | Replayer 回放 collective 日志并用 dummy data；TransferBench 测用户指定设备间并发拷贝。记录 L11 的分列保持；不证明真实路径替代。Git blob 不是 SHA-256。 |

未取得 curl 原始远程字节，不补造远程 SHA-256；连接器返回所选范围及 Git blob 身份。未重新逐条评审案例评论，未实开未采用的 ROCm 注记、FaultDiag 候选或 HCCL 交集材料。作者历史 curl 200/锚点实测为作者自述，本轮可达性和源码读取既不能倒补其历史执行，也不能因本轮 DNS 失败而推翻它。

## B19-C27 — P2 / OPEN：当前数量推进，历史归属与 verification 仍未闭环

位置：作者记录 L3/L9–11/L19；正文 L34/L60/L74/L125–129；修订映射 L97–155，尤其 L131/L149/L151/L155。对应 acceptance 1–4 的可追溯性；以下依据权威第九次报告 L106–112，不扩大技术审阅范围。

| 子条件 | 判定 | 位置与证据 |
|---|---|---|
| 记录 L9 完整内容 ID | CLOSED（保持） | `communication.bandwidth-baselines`、`communication.rdma-baseline-and-congestion-triage` 与实际条目 ID 一致；链接可定位矩阵、计数器限定和停止/恢复入口，不将内容 ID 冒充外部来源 ID。 |
| 记录 L10 ID—URL—字段—范围 | CLOSED（保持） | NCCL env/ACS/RAS 三个精确入口分列；UFM 精确 ID/URL、四项全名、版本/IB 限定及未覆盖范围保持，本轮一次源对应可读。 |
| 记录 L11 工具用途与设计归属 | CLOSED（保持） | RCCL tag 源码两工具节、完整来源/内容 ID、#2409 URL/四节定位保持；回放与设备拷贝基准分开，四类轮次为本库设计，未固定工具仍候选。 |
| 悬空来源代号删除 | CLOSED（保持） | L19 的未采用/未固定项直接写具体对象，NCCL 三页写实际用途；“S7 代号删除”是清理说明，不是新的来源别名。历史映射里的旧代号不当成当前候选身份。 |
| 旧遥测三处原批限定 | CLOSED（保持） | 正文 L60、L74 末格、L129 与记录 L19 均区分 Batch 09 原批缺口、当前 T03-03 文档可复用及现场字段能力 unknown；不将 L74 历史中段扩解为当前全库缺源。 |
| 矩阵字段契约同步 | CLOSED（保持） | 正文 L34/L61/L126、记录 L9/L19 与 T03-07 L144–161 均为字段契约已引用、实测矩阵未交付，不声称数值已填或兼容已证。 |
| T03-06/RCCL 档案/作者记录入口 | CLOSED（保持） | 正文 L77/L125/L127 三入口及 Batch 09 历史入口存在；T03-06 的交集限制保持。入口不替代证据，不关闭 BLOCKED-1。 |
| 当前作者/审阅数量与角色 | CLOSED（数量及角色分列接受；首轮范围归下项） | 正文 L34、来源 L3、映射 L153/L155 均声明作者十轮；初审＋一至九次复核共十份报告逐项存在。第十轮标题正确引用第九次 26 CLOSED / 1 OPEN。不是独立确认作者十轮历史取证均已完成。 |
| 第九轮错误累计和旧轮次自述 | OPEN（原条件未落实） | L149 仍称第八次为 25 CLOSED / 2 OPEN，权威第八次报告 L116 与第九次 L109 均为 26/1；L151 仍把当前账本称作者八轮＋审阅八份，与本节九轮标题不一致，无上一轮限定。L155 的第十轮正确数值不纠正这些错误。 |
| 逐轮取证/复用/unknown 与首轮对应 | OPEN（接受第三/第四轮 unknown 分列） | 来源 L3 不再合并第三至六轮 unknown，但仍缺逐轮具体修订节对应；首轮写“同批来源准备”，没有说明它与 L97–104 首个修订节是否同一轮。第三/第四轮 unknown 仅限定通道，未界定对象/新增/复用的未知范围；第五/第六轮给锚点及 curl 200，却无该轮具体版本/精确入口或对应引用，亦未解释与历史记录差异。 |
| 历史交付/计数说明 | OPEN（部分补齐） | 来源 L3 已把 S7 删除归第九轮，不再倒记第八轮；对第七轮“已删除/已补齐”加目标自述/实际后续落盘说明，可接受进展。但“实际落盘在第八/九轮”仍未分清网络/存储完整契约与 C3/S5/S6 在第八轮、S7 在第九轮；正文所指旧映射 L141/L142 未加该说明的引用。第五轮 L131 四轮/四份及第九轮 L151“第五轮计数已纠正”仍无解释。 |
| verification 精确账本及未解范围 | OPEN（当前数量同步接受） | 正文 L34 仍泛称“轮次账本交付”，没有精确引用作者记录 L3/修订节，也未保留第三/第四轮 unknown 和历史差异。L127 的一般作者记录入口已通过，但不替代 verification 的明确账本/口径说明。来源 L3 在作者记录中称“本报告（第九次复核）”，却未明确链接到真正第九次审阅报告；仍须限定引用对象与作者/审阅角色。 |
| 首轮全量实开、第六轮归属、第七轮去重 | CLOSED（保持） | 未恢复 S1–S7 全量实开；L133/L135/L137 保持前次 25/2、C23 CLOSED、L9 属 C27；L139 同轮增补且来源 L3 只计一个第七轮。不因剩余账本问题重开这些已接受项。 |

### 十轮记录的交付核对

下表为审阅者对当前作者记录的判定，不代作者编写或确认历史账本。unknown 表示现有记录无法建立对应，不等于作者当时没有取证；相似修改主题不授权审阅者自行合并轮次。

| 作者轮次（当前声明口径） | 当前候选修订节 | 来源 L3 的已知进展 / 未解边界 |
|---|---|---|
| 首轮 | L97–104 | #2409/#814 全文、env/RAS、curl 200 为作者自述；“同批来源准备”与初审后首个修订节的合并关系未明。当前主张表不自动证明首轮用了哪些版本/入口。 |
| 第二轮 | L106–112 | 8 条 #2409/#814 评论、#209/#223、curl 200 自述；主张表可定位当前已引用评论，但该轮与具体修订节/采用范围未明示，#223 只列名称。不要求实开未采用候选，可直接记未采用或 unknown。 |
| 第三轮 | L114–119 | 本轮改为“具体远程通道记录不全，记 unknown”；接受 unknown，但对象/版本/新增或复用范围未明。旧 L117“troubleshooting URL 实核 200”与第九次报告 L94 当时来源串的源码 curl 200 自述未解释。 |
| 第四轮 | L121–125 | “同上类目；通道不明记 unknown”接受未知通道；“同上类目”仍不是具体对象/版本/入口及新增/复用对应。 |
| 第五轮 | L127–131 | README `user-content-arguments`、`all_reduce.cu` raw L78–84、curl 200 自述；未明确该轮 ref/精确 raw 入口或所复用记录。L131 四轮/四份未限定为上一轮；旧“已纠正”仍在。 |
| 第六轮 | L133–137 | `nccl-cross-nic`、`computeinfiniband-fabric`、`network-testing` 三锚点/curl 200 自述；可在 T03-07 当前矩阵中找到相关入口，但没有作者该轮关联或版本/新增/复用说明，不能由审阅者自行嫁接。状态和 L9 所属 ID 已正确保持。 |
| 第七轮 | L139–142 | 无新增远程取证、仅复用及去重说明接受；来源的后续落盘提示已有，但未逐项划清第八/九轮，与旧映射的“已补齐/已删除”仍须建立明确关系。 |
| 第八轮 | L144–147 | 无新增远程取证、仅复用；来源不再把 S7 删除写成本轮。网络/存储完整契约及 C3/S5/S6 清理在第八次已接受；应与来源“第八/九轮”的合并说明逐项对应，不补作新增远程执行。 |
| 第九轮 | L149–151 | S7 删除及无新增远程取证接受；账本在第九次仍 OPEN，不能保留未限定“交付”作为已闭环证明。累计 25/2、作者八轮＋审阅八份仍待纠正/历史限定。 |
| 第十轮 | L153–155 | 正确引用前次 26/1，当前十轮/十份同步，无新增远程取证、仅复用；尚未实际满足所声称“逐轮账本交付”和前次全部关闭条件。 |

历史差异仍需作者解释：[第六次报告](batch-19-t03-08-codex-recheck-6.md) L101 记录当时正文把第三/第四/第五次修订写为“无新增远程取证”；[第九次报告](batch-19-t03-08-codex-recheck-9.md) L94/L96/L102 已指出随后第三轮源码 curl 200 与第五轮 raw/锚点实测自述的变化。本轮把第三轮又改为通道 unknown，却没有说明这是撤回、回溯补记、复用还是轮次口径重新对应；第五轮实测自述继续保留。**不裁定作者历史取证真假，不要求补造当时响应、哈希或日志**；只要求按统一轮次如实界定已知/未知和旧新记录关系。

审阅计数边界：第十轮作者修订输入交付时，初审＋一至九次定向复核确为十份既有审阅报告。本报告交付后为初审＋十次复核，共十一份审阅记录；新审阅报告不产生作者第十一轮，不要求作者预先声称本次已完成。当前作者“十轮”仍是其账本口径，不是审阅者独立证实十轮历史执行范围。

### 剩余关闭条件

1. 保留已接受的精确来源映射、完整字段、工具用途/设计归属、悬空代号清理、原批遥测限定、矩阵状态、内容入口、角色分列、去重及当前十轮/十份输入口径；C24 及其余 CLOSED 不重开。
2. 第九轮 L149 据权威第八次报告纠正为 **26 CLOSED / 1 OPEN**；L151 的八轮/八份如意指上一轮，明确历史对象，否则按统一口径修正。第五轮 L131 的四轮/四份说明是上一轮旧口径还是待纠正项，并纠正/限定 L151“第五轮计数已纠正”；第十轮正确标题不能代替这些修订。
3. 首轮至第十轮逐项对应具体修订节，明确首轮来源准备与 L97–104 的关系；各轮列实际新增取证对象/版本/精确入口与已知通道，或具体复用记录，或对象/版本/新增状态/通道中哪些 unknown。尤其第三/第四轮不能只有“同类目/通道 unknown”，第五/第六轮的锚点/raw/curl 自述要可定位。未采用候选直接限定未采用，不要求补取证。
4. 逐项把第七轮目标自述与实际后续落盘对应：网络/存储完整契约、C3/S5/S6 清理在第八轮；S7 删除在第九轮。可以保留原历史节并引用明确的纠正说明，不要求抹去历史。解释第六次/第九次报告所记第三至第五轮取证自述与本轮变动的关系；如无法还原，按轮次/对象记 unknown，而非用当前文件或审阅取证倒证历史。
5. 正文 verification 精确引用该账本、统一口径和未解历史范围，与来源记录及修订映射一致；作者来源记录中“本报告（第九次复核）”须明确指向审阅报告，避免角色错指。区分十轮作者修订、输入时十份既有审阅及本报告新增后的十一份；不把历史 unknown 或作者自述写成全轮已独立实核。

## 状态集合与验收影响

| 状态 | ID / 范围 |
|---|---|
| 本轮整项新增 CLOSED | 无；仅接受 C27 子条件进展，不另计 ID |
| 既有 CLOSED（26；不重开） | C01–C26，含 C24 |
| 本轮 OPEN（1 P2） | C27 |
| 本批累计审阅发现 | **26 CLOSED / 1 OPEN**（共 27 个 ID，未新增） |
| 既有验收子项 OPEN（单列） | BLOCKED-1，`blocked_on_evidence`；不计入发现数量 |
| T03-08 | **第十次定向复核未通过**；后续仅复核 C27 剩余关闭条件及已接受条件保持 |
| T03-06/T03-07 | 有限文档/来源范围通过保持；不重新验收 T03-06 acceptance 5 |
| Batch 19 | 未完成整批验收，不因当前数量同步或来源可读而认定全部完成 |

acceptance 1 的时窗/矩阵契约保持，不重开 C22；acceptance 2 的四分支与物理门禁保持，不重验 C23；acceptance 3 的既有案例结论保持，不重开 C25/C26；acceptance 4 的完整复现契约、对照/风险/停止/恢复/资料入口在 C24 已 CLOSED 范围保持。四项作者记录的可追溯性仍受 C27 限制。来源可读、模型审阅和结构校验均不建立现场复现、字段能力或版本兼容交集；正文仍为 draft / source_checked。

## 检查边界与写入范围

- 仅新增本报告；不改作者正文、来源记录、修订映射、登记、计划、索引或来源审计。既有工作区改动不恢复、不提交、不创建分支。
- 不执行 benchmark、collective/MPI、实机采集、配置修改、故障注入或上游诊断命令；引用命令只阅读。未取得现场遥测、时钟、字段能力或实验结果。
- curl 受 DNS 限制；替代只读通道核对上述一次源，RCCL 仅核对官方 tag/固定源码，不冒充 HTML 成功或作者历史执行。未知和 blocked_on_evidence 保留。
- 为遵守“只写这一份报告”，在包含本报告及既有 `build/` 的仓库外临时快照执行 `make check` / `make build`，均 PASS（88 content entries / 389 sources）；原仓库 `build/` 不重建。不改 `src/kb/`，不执行 `make test`。结构校验不验证技术正确性、历史取证或远程语义。正文步骤表逐行五列、作者映射表逐行四列的结构检查通过，不构成 C24 的重新技术验收。
- 本报告 14 处本地链接、12 个不同目标均存在。写入前后 SHA-256 / 符号链接清单核对：原有 3484 个常规文件（含 `.git`、既有构建文件及本地环境文件）与 3 个符号链接均不变，无删除，仅新增本报告；五项任务输入与输入 SHA 表一致。临时清单与校验快照均在仓库外，不作为现场验证证据。
