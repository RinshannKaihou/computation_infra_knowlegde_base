# 第十九批 T03-08 第十一次定向复核

审阅日期：2026-10-13（Asia/Shanghai，本机日期确认）。正文 `updated_at: 2026-10-14` 及部分登记日期晚于本机日期，仅视为作者交付标签，不作为本轮取证日期或历史执行证明；输入身份以下表 SHA-256 为准。

**结论：C27 仍 OPEN（1 项 P2）；C01–C26 均保持 CLOSED，含 C24，不重开。本批累计 26 CLOSED / 1 OPEN（共 27 个审阅发现），T03-08 第十一次定向复核未通过。** 接受第五轮 L131 的五轮/五份计数纠正、当前输入“作者十一轮＋审阅十一份”的数量同步，以及来源 L3 对“本报告（第九次复核）”所指审阅文件的澄清。但第九轮 L149 的前次累计仍为错误的 25/2，L151 八轮/八份未限定历史对象；逐轮取证对象、版本、入口、复用及首轮对应仍未闭环；第七轮目标自述与第八/九轮实际落盘仍合并，历史取证自述的变动未解释；正文 verification 仍无精确账本及未解历史范围引用。第十一轮 L159 的“确认/复核/同步”自述不能替代相应落盘修订。BLOCKED-1（HCCL Test × 目标 CANN/HDK/机型官方交集）单列 `blocked_on_evidence/open`，不计入发现数量；T03-06/T03-07 有限文档/来源范围通过保持，整个 Batch 19 不因此验收。

约定配置 `gpt-6.1-sol / xhigh` 仅为用户约定，不写成已独立确认的执行模型或推理等级。执行者为当前 Codex 主会话，角色为独立审阅者，与作者修订角色分开；无子代理。只写本报告，不代作者修订，不新增发现 ID；本轮记录差异均按原 C27 追记。子条件不产生新 ID，也不单独计入累计数量。

## 输入与复核范围

| 输入 | SHA-256 |
|---|---|
| [T03-08 正文](../../knowledge/03-communication/bandwidth-degradation-triage.md)（procedure / draft） | `da58c5a410f620bad98487ce2a3a66c63900030e9ac71cabbc4f3807b29be4b9` |
| [作者来源记录](batch-19-t03-08-sources.md) | `7d08f8e275e8e0d47400c8eb723a08107a0d26fdadff2686ef717dcb1b93bc39` |
| [修订映射](batch-19-review-fixes.md)（第十一轮 L157–159；历史 T03-08 节 L97–155） | `944a18b7d5073d0a952f034464e8beda341296836b8d03a2c58e39d98b259f41` |
| [第十次定向复核](batch-19-t03-08-codex-recheck-10.md)（C27 L48–95；剩余关闭条件 L89–95；累计状态 L97–110） | `6d52df81f494232d2bcf0e9ca20de234f1b40b8ee9051da2e708ff3f7526c0bb` |
| [任务验收](../../plans/full-coverage-backlog.yaml)（T03-08 acceptance 1–4，L5006–5010） | `121826a4d499273e7f6a00735e0a53931eef5c097bd66ab6b2425fdbc36ddfe0` |

第十次报告为本轮剩余关闭条件的权威来源。本轮只复核 C27 及其已接受条件是否保持；C24 已 CLOSED 保持，不重新评审其技术契约。不重验 C22 时窗、C23 物理分支，不重新判定 #2409/#814/#209 案例原因、反证或修复结论，不重新验收 T03-06 acceptance 5。历史报告的输入 SHA 标识当时交付，不用本轮最终文件倒补历史。

| 补充只读输入 | SHA-256 |
|---|---|
| [来源登记](../../sources/registry.yaml) | `277aecb64892438a366c1729fe01210cbeae60845ff6fbefce437a7a7a96901e` |
| [T03-07 基线口径](../../knowledge/03-communication/bandwidth-baselines.md)（矩阵 L144–161；第五轮同类入口 L86/L89） | `8c2884b63cf7b638c1df2d7de88f5fe9d2923c0d95b025548041aea203574039` |
| [T03-03 RDMA 诊断](../../knowledge/03-communication/rdma-baseline-and-congestion-triage.md) | `7f6d59752e7c74628f2c9d706ce2ec00e3031ecd36230554eb8d2680fee67412` |
| [T03-05 RCCL 档案](../../knowledge/03-communication/rccl-runtime-and-verification.md)（工具 L69–71） | `1f95d5b310726d858900e2028ab3b779f1470b03a1ba67187fbed1c6da5b19db` |
| [T03-06 三库对照](../../knowledge/03-communication/communication-library-profiles.md)（工具 L65；交集限制 L74–76） | `d4a5fb535ba78d852e070f09ff387b69dc6e1ab7cf86620c7ee08e9a99577646` |
| [第八次定向复核](batch-19-t03-08-codex-recheck-8.md)（清理/交付边界 L81/L90；累计 L116） | `fb791dcda229dc1d3bfb8a060f17daa17180c14f56f668ecaa601a2994604071` |
| [第九次定向复核](batch-19-t03-08-codex-recheck-9.md)（历史取证差异 L94–102；关闭条件 L106–112） | `9d0027c03fd59529cb8d7f8e6b246d1e998e6752354df4a8c72fd510a9135b10` |
| [第六次定向复核](batch-19-t03-08-codex-recheck-6.md)（历史轮次与取证记录 L101） | `2b8395444ab5236e658b3fbaa1430e6735a9ca742142bef59d70b47b2602768a` |

## 一次源取证与方法限制

采用本地只读逐行核对、默认 TLS 校验的只读 curl、允许的网页阅读器及 GitHub 连接器。curl 请求 UFM 精确端口页、RCCL docs-10.1.0 troubleshooting 页与 #2409 均 DNS 解析失败：exit 6、HTTP 000、下载 0 字节。HTTP 000 不是上游状态；未使用 `-k/--insecure`，未修改网络或 TLS 配置。

网页阅读器返回 UFM、NCCL 2.27.5 env/ACS/RAS、#2409、SuperPOD fabric 和 GPU Node Triage 精确页面的解析文本，抓取标记为 today；这不等同于本机直接 HTTP 实测或原始响应。RCCL troubleshooting HTML 与 rccl-tests README blob 锚点页均只返回 `Internal Error`，没有可独立确认的 HTTP 状态。RCCL 工具改用连接器读取作者所链 tag 及已登记固定 commit 的同路径源码；README/AllReduce 也仅核对源码对象，不冒充 HTML 锚点 id、raw 响应或作者历史 curl 200 已独立确认。网页阅读器坐标只用于本轮定位，不转成 GitHub 源码行锚点；源码位置采用连接器请求的原文件范围。

| 一次源 / 已登记 ID | 本轮精确定位与证据 | 支持范围 / 限制 |
|---|---|---|
| `src.nvidia.ufm-41815-port-counters` | [InfiniBand Port Counters](https://networking-docs.nvidia.com/ufmsdnappswum/41815/infiniband-port-counters)，阅读器 L121–133：`Rcv Errors`、`Symbol Errors`、`Link Error Downed`、`Xmit Discards` 四项全名；登记 L4520–4530 | 对应记录 L10 的 UFM 4.18.15 / IB 范围；收错包括 overrun，丢弃有多因。不证明 RoCE/HCCS/目标现场字段能力；完整版本后缀未由本轮选择器独立读到，不重开已接受范围。 |
| `src.nvidia.nccl-user-guide-2.27.5`：env | [SPLIT_DATA_ON_QPS 节](https://docs.nvidia.com/deeplearning/nccl/archives/nccl_2275/user-guide/docs/env.html#nccl-ib-split-data-on-qps)，阅读器 L599–606：split/round-robin 与默认值 | 对应记录 L10/L19 的变量页映射；文档默认值不等于现场配置。 |
| 同一 NCCL 归档 ID：ACS | [troubleshooting 的 ACS 节](https://docs.nvidia.com/deeplearning/nccl/archives/nccl_2275/user-guide/docs/troubleshooting.html#pci-access-control-services-acs)，阅读器 L50–54：PCI 路径重定向 | 属 troubleshooting 页，不是 env 页；只核对来源归属，不执行页内命令。 |
| 同一 NCCL 归档 ID：RAS | [RAS sample-output 节](https://docs.nvidia.com/deeplearning/nccl/archives/nccl_2275/user-guide/docs/troubleshooting/ras.html#sample-output)，阅读器 L19–85：活跃通信与初始化/销毁过渡的瞬态、重复查询限定 | 独立子页，不是 env 页；不建立链路级硬件证据。 |
| `src.nvidia.nccl-issue-2409` | [Issue 正文](https://github.com/NVIDIA/nccl/issues/2409)，阅读器 L173–215：§1 perftest、§2 rail、§3 debug/WQE、§4 env sweep | 仅核对记录 L11 的设计借鉴定位；四类轮次为本库设计归纳，不重新判定案例结论。 |
| `src.rocm.rocm-systems-therock-10.1`；关联 HTML ID `src.amd.rccl-docs-10.1.0` | [作者所链 tag 文件](https://github.com/ROCm/rocm-systems/blob/therock-10.1/projects/rccl/docs/how-to/troubleshooting-rccl.rst) L129–226；[固定 commit 文件](https://github.com/ROCm/rocm-systems/blob/7da43026e4f2ef7600433c38c820732f7a205d22/projects/rccl/docs/how-to/troubleshooting-rccl.rst) L129–203；两 ref 均返回 Git blob `89779e32d545fcd1f61a7dc728e0abf9113bc186` | Using the RCCL Replayer 与 Collect the TransferBench data 两节可定位；前者回放 collective 日志并用 dummy data，后者测用户指定设备间并发拷贝。只支持用途区分，不证明真实路径替代或 HTML 全文等同。Git blob 不是 SHA-256。 |

第五/第六轮历史定位的辅助核对：连接器读取 [rccl-tests README](https://github.com/ROCm/rocm-systems/blob/therock-10.1/projects/rccl-tests/README.md) L1–150（含 Arguments 标题，Git blob `2258db761fb1e0316cd6f67ce0483ada04113aa5`），以及[固定 commit 的 all_reduce.cu](https://github.com/ROCm/rocm-systems/blob/7da43026e4f2ef7600433c38c820732f7a205d22/projects/rccl-tests/src/all_reduce.cu#L78-L84) L78–84（Git blob `7adb1494ef56ee4b8dd9751c6288aee6c6f2d515`）。T03-07 L86/L89 现有对应入口，但 T03-08 来源 L3 未把第五轮自述绑定到这些版本/对象；本轮不能替作者嫁接。网页阅读器另返回 [NCCL CROSS_NIC](https://docs.nvidia.com/deeplearning/nccl/archives/nccl_2275/user-guide/docs/env.html#nccl-cross-nic) L87–98、[SuperPOD Compute IB fabric](https://docs.nvidia.com/dgx-superpod/reference-architecture-scalable-infrastructure-h100/latest/network-fabrics.html#computeinfiniband-fabric) L35–37、[GPU Node Triage Network Testing](https://docs.nvidia.com/deploy/gpu-debug-guidelines/gpu-node-triage.html#network-testing) L99–102；仅确认当前可定位，不能倒证第六轮实际做过锚点实测或使用了哪个历史版本。后两项为可变页。

未取得 curl 原始远程字节，不补造远程 SHA-256；连接器仅提供请求范围和 Git blob 身份。未重新逐条评审案例评论，未实开未采用的 ROCm 注记、FaultDiag、HCCL 交集或 #223 候选。作者历史 curl 200/锚点实测仍是作者自述；本轮可读性不补作者历史，本轮 DNS 失败也不推翻其历史自述。

## B19-C27 — P2 / OPEN：第五轮计数补齐，剩余历史归属与 verification 未闭环

位置：作者来源 L3/L9–11/L19；正文 L34/L60/L74/L125–129；修订映射 L97–159，尤其 L131/L141–142/L149/L151/L159。对应 acceptance 1–4 的记录可追溯性；以下逐项对应权威第十次报告 L89–95，不扩大技术审阅范围。

| 子条件 | 判定 | 位置与证据 |
|---|---|---|
| 记录 L9 完整内容 ID | CLOSED（保持） | `communication.bandwidth-baselines`、`communication.rdma-baseline-and-congestion-triage` 与实际条目 L2 一致；链接定位矩阵、计数器语义和停止/恢复入口，不将内容 ID 冒充外部来源 ID。 |
| 记录 L10 ID—URL—字段—范围 | CLOSED（保持） | NCCL env/ACS/RAS 三入口分列；UFM 精确 ID/URL、四项全名、版本/IB 与未覆盖范围保持；本轮一次源对应可读。 |
| 记录 L11 工具用途与设计归属 | CLOSED（保持） | RCCL tag 文件两工具节、完整来源/内容 ID、#2409 URL/四节定位保持；回放与设备拷贝基准分开，四类轮次为本库设计，未固定工具仍候选。 |
| 悬空来源代号删除 | CLOSED（保持） | 来源 L19 以具体对象记录未采用/未固定范围，NCCL 三页列实际用途；“S7 代号删除”是清理说明，不是新的别名。历史映射旧代号不作为当前候选身份。 |
| 旧遥测三处原批限定 | CLOSED（保持） | 正文 L60、L74 末格、L129 与来源 L19 均区分 Batch 09 原批缺口、当前 T03-03 文档可复用及现场能力 unknown；不将 L74 历史中段扩解为当前全库缺源。 |
| 矩阵字段契约同步 | CLOSED（保持） | 正文 L34/L61/L126、来源 L9/L19 与 T03-07 L144–161 均为字段契约已引用、实测矩阵未交付；未声称数值已填或兼容已证。 |
| T03-06/RCCL 档案/作者记录入口 | CLOSED（保持） | 正文 L77/L125/L127 的三入口和 Batch 09 历史入口均存在；T03-06 L74–76 交集限制保持。入口不替代证据，不关闭 BLOCKED-1。 |
| 当前作者/审阅数量与角色 | CLOSED（数量同步接受；历史范围另列） | 正文 L34、来源 L3、映射 L157/L159 的当前作者十一轮相合；初审＋一至十次复核确为十一份既有报告，已逐项核对文件与标题。只接受作者声明口径，不独立认证十一轮历史执行范围。 |
| 第五轮旧四轮/四份计数 | CLOSED（本轮补齐该子条件） | 映射 L131 明写作者五轮、初审＋一至四次复核五份，明确原“四轮/四份”为旧计数口径错误；满足前次 L92 的计数澄清要求。L151“第五轮计数已纠正”的历史时点仍归下项，不否认当前纠正。 |
| 第九轮错误累计及旧轮次自述 | OPEN（原条件未落实） | L149 仍称第八次为 25 CLOSED / 2 OPEN，而第八次报告 L116、第十次 L92 为 26/1；L151 仍称账本“作者八轮＋审阅八份”，无上一轮限定。L159 虽声称第九轮累计引用已确认 26/1、审阅十份口径确认，未纠正 L149/L151，也未明确十份所指历史对象。 |
| 逐轮取证/复用/unknown 与首轮对应 | OPEN（原剩余项保持） | 来源 L3 仍以一段列各轮主题，没有逐项对应具体修订节，首轮“同批来源准备”与 L97–104 的关系未明；第三/第四轮只限定通道 unknown/“同上类目”，对象、版本、新增或复用范围未交付；第五/第六轮保留锚点/raw/curl 200 自述但无该轮精确版本/入口或复用引用。L159“逐轮账本复核”不补这些字段。 |
| 第七轮历史交付及取证差异说明 | OPEN（部分说明保持，未全部落实） | 来源 L3 仍把网络/存储完整契约、C3/S5/S6 清理和 S7 删除合并为“实际落盘在第八/九轮”，没有逐项分清第八与第九轮；L141/L142 未引用纠正说明。第六次 L101、第九次 L94/L96/L102 所记第三至第五轮取证自述变动仍无解释；L151“第五轮计数已纠正”未注明实际纠正在本轮，或只是后续状态增补。 |
| verification 精确账本与未解范围 | OPEN（当前数量同步接受） | 正文 L34 只列轮次和当前“账本复核”，无精确引用来源 L3/对应修订节，也未保留第三/第四轮未知及历史差异。L127 的一般来源入口已接受，但不替代 verification 的账本/口径/unknown 明确关联。映射 L159“含本报告”指向不明；不能用它计算尚未交付的第十一次审阅，也不能把作者映射算为审阅报告。 |
| 作者记录的“本报告（第九次复核）”角色错指 | CLOSED（本轮补齐该子条件） | 来源 L3 现明确写“指审阅报告 batch-19-t03-08-codex-recheck-9.md（历史表述保留）”，且当前交付至第十次复核；文件存在、标题对应。角色及历史对象已澄清，不因采用文件名而非 Markdown 链接继续扣留此子条件。 |
| 首轮全量实开、第六轮归属、第七轮去重 | CLOSED（保持） | 未恢复 S1–S7 全量实开；L133/L135/L137 保持前次 25/2、C23 CLOSED、L9 属 C27；L139 同轮增补且来源 L3 只计一个第七轮，不因剩余账本问题重开。 |

### 十一轮记录的交付核对

下表的修订节为审阅者按标题作出的候选对应，**不是作者已交付的逐轮关联账本**，不代作者确认历史执行。unknown 表示现有记录无法建立对应，不等于作者当时没有取证；不因同类事项或本轮可读页面而自行合并轮次或补入历史对象。

| 作者轮次（当前声明口径） | 当前候选修订节 | 来源 L3 / 映射的已知进展与未解边界 |
|---|---|---|
| 首轮 | L97–104 | #2409/#814 全文、env/RAS、curl 200 为作者自述；“同批来源准备”是否与首个修订节合为同一轮未说明，不能由当前主张表倒补该轮版本/入口。 |
| 第二轮 | L106–112 | 8 条 #2409/#814 评论、#209/#223、curl 200 自述；当前表可定位采用评论，但未绑定该轮修订节/具体版本/采用范围，#223 未解释采用状态。不要求补实开未采用候选。 |
| 第三轮 | L114–119 | 当前写具体远程通道记录不全/unknown；对象、版本、新增/复用也未界定。L117“troubleshooting URL 实核 200”、第九次 L94 所记随后源码 curl 200 自述与当前 unknown 的关系未解释。 |
| 第四轮 | L121–125 | “同上类目；通道不明记 unknown”仅接受未知通道；没有具体对象、版本、入口及新增/复用对应，不用相邻轮次替代。 |
| 第五轮 | L127–131 | 本轮五轮/五份计数已纠正；README 锚点、all_reduce.cu raw L78–84/curl 200 仍无本轮历史 ref/精确入口或具体复用记录。T03-07 当前同类入口不自动属于此轮。 |
| 第六轮 | L133–137 | 三处文档锚点/curl 200 自述保持；未绑定第六轮的版本/观察入口/新增或复用状态，不用本轮读取倒证。C23/L9 归属及前次累计正确保持。 |
| 第七轮 | L139–142 | 无新增远程取证、仅复用及去重说明接受；来源 L3 的目标自述提示仍未逐项分清后续落盘，旧映射未关联纠正。 |
| 第八轮 | L144–147 | 无新增远程取证、仅复用；网络/存储完整契约及 C3/S5/S6 清理实际第八轮接受，S7 此时仍未清理（第八次 L81/L90）。须与来源 L3 的合并说明逐项对应。 |
| 第九轮 | L149–151 | S7 当前删除与无新增远程取证接受；25/2 累计错误、八轮/八份和未限定“账本交付”仍在。第五轮现已纠正不能倒证第九轮当时已纠正。 |
| 第十轮 | L153–155 | 正确引用前次 26/1、历史十轮/十份及无新增远程取证接受；该轮“逐轮账本交付”在第十次未通过，不能由第十一轮“复核”倒记已闭环。 |
| 第十一轮 | L157–159 | 前次 26/1、当前作者十一轮正确；来源 L3 声明无新增远程取证、仅复用。第五轮计数实际补齐；第九轮累计/轮次和逐轮账本其余条件未落盘。L159“审阅十份”“含本报告”须明确历史/当前对象。 |

历史差异证据：[第六次报告](batch-19-t03-08-codex-recheck-6.md) L101 记当时正文把第三/第四/第五次修订写为无新增远程取证；[第九次报告](batch-19-t03-08-codex-recheck-9.md) L94/L96/L102 记随后第三轮源码 curl 200、第五轮 raw/锚点实测自述；[第十次报告](batch-19-t03-08-codex-recheck-10.md) L76/L85 又指出第三轮改为通道 unknown，未解释撤回、回溯补记、复用或轮次重新对应。本轮仍未解释。**不裁定历史取证真假，不要求补造当时响应、哈希或日志**；只要求按统一轮次及对象界定已知/未知与旧新记录关系。

审阅计数边界：第十一轮作者修订输入交付时，[加法初审](batch-19-t03-08-codex-review.md)＋第一次至第十次定向复核，确为十一份既有审阅报告。本报告交付后为初审＋十一次复核，共十二份审阅记录；新增审阅报告不产生作者第十二轮，也不要求作者预先把尚未交付的本次审阅算入。正文/来源当前十一份输入口径可以保留，需澄清 L159“审阅十份”“含本报告”的具体对象。

### 剩余关闭条件

1. 保留已接受的精确来源映射、完整字段、工具用途/设计归属、悬空代号清理、原批遥测限定、矩阵状态、三内容入口、角色分列及去重；保留本轮第五轮五轮/五份计数纠正和来源“第九次复核”角色澄清。C01–C26（含 C24）不重开。
2. 第九轮 L149 据权威第八次报告 L116 纠正为 **26 CLOSED / 1 OPEN**；L151 八轮/八份如指上一轮，明确历史对象，否则按第九轮输入口径纠正为作者九轮、初审＋一至八次复核九份。限定 L151“第五轮计数已纠正”是本轮后续增补，而非当时已完成。L159“第九轮累计引用已确认”“审阅十份”须与实际修改及所指历史轮次一致，不只添加正确的新标题。
3. 首轮至第十一轮逐项对应具体修订节，明确首轮来源准备与 L97–104 的关系。各轮列新增取证对象/版本/精确入口与已知通道，或具体复用记录，或逐项标明对象/版本/新增状态/通道中哪些 unknown；第三/第四轮不得仅用“同类目/通道 unknown”，第五/第六轮保留的锚点/raw/curl 自述须可定位或界定未知范围。未采用候选直接限定未采用，不要求补取证或补造历史响应。
4. 把第七轮目标自述逐项对应实际落盘：网络/存储完整契约与 C3/S5/S6 清理在第八轮，S7 删除在第九轮；历史映射节可保留，但应关联明确纠正说明。解释第三至第五轮取证自述与第六/九/十次报告所记历史差异；无法还原的按轮次/对象记 unknown，不用当前文件或审阅取证倒证历史。
5. 正文 verification 精确引用上述账本、统一口径与未解历史范围，与来源及映射一致；保持作者十一轮、输入十一份既有审阅与本报告交付后十二份审阅的角色/时点区分。明确 L159“含本报告”的文件对象，不把历史 unknown 或作者自述写成全轮已独立实核。来源 L3 的第九次报告角色澄清已接受，无须再当作未完成条件。

## 状态集合与验收影响

| 状态 | ID / 范围 |
|---|---|
| 本轮整项新增 CLOSED | 无；仅接受 C27 子条件进展，不另计 ID |
| 既有 CLOSED（26；不重开） | C01–C26，含 C24 |
| 本轮 OPEN（1 P2） | C27 |
| 本批累计审阅发现 | **26 CLOSED / 1 OPEN**（共 27 个 ID，未新增） |
| 既有验收子项 OPEN（单列） | BLOCKED-1，`blocked_on_evidence`；不计入发现数量 |
| T03-08 | **第十一次定向复核未通过**；后续仅复核 C27 剩余关闭条件及已接受条件保持 |
| T03-06/T03-07 | 有限文档/来源范围通过保持；不重新验收 T03-06 acceptance 5 |
| Batch 19 | 未完成整批验收，不因数量同步或来源可读而认定全部完成 |

acceptance 1 的时窗/矩阵契约保持，不重开 C22；acceptance 2 的四分支与物理门禁保持，不重验 C23；acceptance 3 的既有案例结论保持，不重开 C25/C26；acceptance 4 的完整复现契约、对照/风险/停止/恢复/资料入口在 C24 已 CLOSED 范围保持。四项作者记录的可追溯性仍受 C27 限制。来源可读、模型审阅和结构校验均不建立现场复现、字段能力或版本兼容交集；正文仍为 draft / source_checked。

## 检查边界与写入范围

- 仅新增本报告；不改作者正文、来源记录、修订映射、登记、计划、索引或来源审计。既有工作区改动不恢复、不提交、不创建分支。
- 不执行 benchmark、collective/MPI、实机采集、配置修改、故障注入或上游诊断命令；引用命令只阅读。未取得现场遥测、时钟、字段能力或实验结果。
- curl 受 DNS 限制；替代只读通道核对上述一次源，RCCL/README 仅核对源码，不冒充 HTML/锚点实测成功或作者历史执行；unknown 与 blocked_on_evidence 保留。
- 为遵守“只写这一份报告”，在包含本报告及既有 `build/` 的仓库外临时快照执行 `make check` / `make build`，均 PASS（88 content entries / 389 sources）；原仓库 `build/` 不重建。不改 `src/kb/`，不执行 `make test`。结构校验不验证技术正确性、历史取证或远程语义。正文步骤表逐行五列、作者映射表逐行四列的结构检查通过，不构成 C24 的重新技术验收。
- 本报告 17 处本地链接、14 个不同目标均存在。写入前后 SHA-256 / 符号链接清单核对：原有 3485 个常规文件（含 `.git`、既有构建文件及本地环境文件）与 3 个符号链接均不变，无删除，仅新增本报告；五项任务输入与输入 SHA 表一致。临时清单与校验快照均在仓库外，不作为现场验证证据。
