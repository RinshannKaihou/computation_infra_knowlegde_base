# 第十九批 T03-06 第一次定向复核

**最新状态（2026-10-12）：第三次定向复核后 C10–C15 全部 CLOSED；本批累计 15 CLOSED / 0 OPEN（审阅发现）。** T03-06 已交付文档/来源范围通过，BLOCKED-1 单列 open，任务全项及 T03-07/T03-08 前置不自动关闭；通过边界和文字校正见[第三次定向复核](batch-19-t03-06-codex-third-recheck.md)。下文保留第一次复核的历史输入和判定。

复核日期：2026-10-12（Asia/Shanghai）。作者文件中的 `2026-10-14` 保留为输入标签，不作为本轮执行日期。

**结论：C10 转 CLOSED，C11–C15 仍 OPEN。本条目 1 CLOSED / 5 OPEN；连同此前 C01–C09，累计 10 CLOSED / 5 OPEN。** 本轮无新增发现 ID；修订过程中出现的接口层次混用和 rank 定义问题仍按原 C12/C13 关闭条件处理。既有 BLOCKED-1（HCCL Test × 目标 CANN/HDK/机型）继续 blocked_on_evidence/open，单列而不重复计为审阅发现。T03-06 尚未通过，T03-07/T03-08 继续等待；T03-05/T04-01 的有限通过范围保持。

约定模型 / effort 为 `gpt-6.1-sol / xhigh`，本会话 Codex 主助手执行，与作者修订角色分开；未派发子代理。实际运行标识无可独立核验元数据，沿用[初审说明](batch-19-codex-review.md)。依据[T03-06 补充初审](batch-19-t03-06-codex-review.md)的六项关闭条件、[写作指南](../authoring-guide.md#7-批次审阅约定)和[原任务验收](../../plans/full-coverage-backlog.yaml)复核。来源审阅不建立硬件验证。

## 输入与范围

| 输入 | SHA-256 |
|---|---|
| [T03-06 正文](../../knowledge/03-communication/communication-library-profiles.md) | `63f4fa753f3a19086b360b9006ddbe1fbdd37592c5ac23a7c27829314880387f` |
| [T03-06 来源记录](batch-19-t03-06-sources.md) | `bc17670e70a0372108bdbd662962e4027f73246aff860c27586f9ef8e218f29b` |
| [修订映射](batch-19-review-fixes.md) | `49d76c92ca7e8575cbf305d0c752a278e394d35e2c1019981cabd7b8f08012fe` |
| [T03-06 初审](batch-19-t03-06-codex-review.md) | `9bb20fe61e338ebbe1b0c748f4f262ce55e3091715cc2851dd43ad35fc4b6982` |
| [来源审计](batch-19-source-audit.md) | `68827eaeada5cf7e5bd158f6806c1da88076c43e162059815c9aabae5b793f0f` |
| [来源登记](../../sources/registry.yaml)（386 项） | `e84c3b6eb61a83a46dbbfd371e5de4112def120131e0c374181e8e5acbf8f51f` |
| [任务计划](../../plans/full-coverage-backlog.yaml) | `121826a4d499273e7f6a00735e0a53931eef5c097bd66ab6b2425fdbc36ddfe0` |

本轮输入对照补充初审：T03-05、T04-01、RCCL 来源记录、03 索引、登记和计划身份相同；Batch 17/18 材料未变。读取新正文、来源表及修订映射，逐项判断实际落盘结果，不以交付消息或修订映射中的“已处理”代替正文检查。审阅者不修改作者正文、来源记录或修订映射。

## 一次源复验

默认 TLS 校验只读重取八个地址，均 HTTP 200：HCCL 8.0 API PDF、8.1 指南 PDF，NCCL 2.27.5 Types/communicators/env，PyTorch 2.8 distributed、HIP 2.6，以及 RCCL docs-10.1.0 usage-tips。两份 PDF 全文重新提取，核对本轮相关章节并渲染检查 API 物理 p10/p32/p57 的完整页。

PDF、NCCL 三页与 RCCL usage-tips 的 SHA 均与补充初审相同；两个 PyTorch HTML 原字节 SHA 有变化，去除 script/style 并归一化空白后的全部可见文本与初审相同，相关契约无变化。Test 静态正文、固定 README 的旧取证范围沿用初审，本轮不宣称重新获取了 Test 版本交集。

| 原文件 | 本轮 SHA-256 |
|---|---|
| HCCL 8.0 API PDF | `84d023900b87785b2a5c1847b6574683a5b7c13077be110e3a63c7a0159e9a0d` |
| HCCL 8.1 指南 PDF | `39eac20ceb03e4e422153f411c883562edb2f06975b47f40eb5fb54f2a629d9a` |
| NCCL Types HTML | `869e955f94ea828c02c086c389af2f9b5aa35d35d7c11cd4179bf98a824d779a` |
| NCCL communicators HTML | `aa888933f603b91a8adbc1e32a3d0bdd58b34ef35fea1cc85d3135ab1943b3ab` |
| NCCL env HTML | `748cc433bc2aa9ec61570ebc57f4e3c5e9a1845106c43ba52a6eba712f472303` |
| PyTorch distributed HTML | `7b6546154a072365459cd8daba3e2b102fc024741541d74194cda4a0575a067a` |
| PyTorch HIP 2.6 HTML | `d89aab9b9f0eb1b476b5a31e5f4a2decf227c880dc26a6bffaa863fed94df46a` |
| RCCL usage-tips HTML | `b08f3cc42534703e8bcb1c52cd12df12351bf4786f02514416e8050e3bd6ba40` |

原文、PDF 页图和抓取日志仅存临时目录，未镜像入库，无新增来源登记。

## 逐项判定

### C10 — CLOSED

正文 L63 已改为八值，按 Success/InProgress/六类错误计数，含 RemoteError，并明确七行摘要表的缺项不能代表完整类型；RCCL 九码使用一致分母。[Types / ncclResult_t](https://docs.nvidia.com/deeplearning/nccl/archives/nccl_2275/user-guide/docs/api/types.html#ncclresult-t)与 [communicators 摘要表](https://docs.nvidia.com/deeplearning/nccl/archives/nccl_2275/user-guide/docs/usage/communicators.html#error-handling-and-communicator-abort)独立复验支持该修订。来源记录 L11 同步，原关闭条件满足。

### C11 — OPEN：开关分支已补，组契约与独立导航仍未落实

位置：正文 L62/L68；修订映射 L59。

已满足部分：默认关闭与显式 stream 依赖/同步、CUDA 条件、库层/框架层区分、async 跨组 work.wait 的 stream 层级和 rank 转换成员条件均已增加，不再从 NCCL 推出 RCCL/HCCL 约束。

剩余：L68 的“new_group 创建参与者与创建顺序、多线程同步”仍只是条件名称，没有给出谁参加、各 rank 怎样保持顺序；L62/L68 也没有直接说明隐式开关启用后仍需匹配所有设备的主机发起次序。官方 [communicators 并发节](https://docs.nvidia.com/deeplearning/nccl/archives/nccl_2275/user-guide/docs/usage/communicators.html#using-multiple-nccl-communicators-concurrently)要求发起顺序匹配；[PyTorch 2.8 new_group](https://docs.pytorch.org/docs/2.8/distributed.html#torch.distributed.new_group)规定默认创建参与者、跨 rank 创建/执行一致性及多线程显式同步。原关闭条件要求的独立指南/案例/方案导航也未增加：全文本地目标仍仅 collective、RCCL、RDMA 和两份来源记录；修订映射“设独立指南导航”尚未落盘。T03-04 仍只是任务号。

剩余关闭条件：写明启用隐式次序后主机发起顺序仍须匹配；默认 new_group 由主组全部进程进入（含非成员），各进程按相同顺序建组，NCCL 多组 collective 执行保持全局一致，多线程须显式同步。若介绍 use_local_synchronization=True，则单独注明非成员例外和重叠组创建次序。补已有 NCCL/HCCL 指南、案例、实验及 T03-04 的实际普通 Markdown 链接；保持 work.wait 的已修正层级。

### C12 — OPEN：Python 的物理 ID 约束被套到 C++ P2P

位置：正文 L58；来源记录 L17。

已满足部分：补普通 Send/Recv 配对、BatchSendRecv 同卡异步与卡间配对、局部错误查询、Barrier/AlltoAllV、非穷举清单和算法/原语区别。统一主机完成边界仍 unknown，方向正确。

但 C++ `HcclSend/Recv` 后新增“跨 Server 要求物理 id 相同”。[8.0 API PDF](https://www.hiascend.com/doc_center/source/zh/CANNCommunityEdition/80RC1alpha003/apiref/hcclapiref/CANN%208.0.RC1.alpha003%20%E9%9B%86%E5%90%88%E9%80%9A%E4%BF%A1%E6%8E%A5%E5%8F%A3%E5%8F%82%E8%80%83%2001.pdf#page=32)把该条件列在 Python 图接口 send/receive（§2.4.6/2.4.7，印刷 p26–27 / 物理 p32–33）；C++ §3.4.1/3.4.2（印刷 p50–52 / 物理 p56–58）只在本项约束处说明配对同步调用，没有给出该物理 ID 条件。当前表述跨接口外推，与原关闭条件“区分 Python 与 C++”不符。不能因此反向断言 C++ 任意跨 Server 映射均受支持。

剩余关闭条件：移除该未证的 C++ 条件，或移至明确限定的 Python 图接口分支并按 send/receive 各自约束注明；若要保留为 C++ 条件，须取得同版本具体依据。同步、批量配对及局部错误查询的已修正部分保留。

### C13 — OPEN：local rank 与 local rank size 混淆，查询/设备和单卡约束未补完

位置：正文 L70；来源记录 L17；修订映射 L61。

已满足部分：Python/C++ 层次、ranktable/rootInfo 配对与串行、InitAll 的逻辑 ID 顺序/禁止重复、样例不扩通用，以及 8.0 三阶段与 8.1 四阶段的归属均已修正。

剩余：L70 把 local rank 写成“group 在本 Server 内的 rank 数量概念”。[8.0 API PDF 表 1-1](https://www.hiascend.com/doc_center/source/zh/CANNCommunityEdition/80RC1alpha003/apiref/hcclapiref/CANN%208.0.RC1.alpha003%20%E9%9B%86%E5%90%88%E9%80%9A%E4%BF%A1%E6%8E%A5%E5%8F%A3%E5%8F%82%E8%80%83%2001.pdf#page=10)区分 local rank id（编号，印刷 p4 / 物理 p10）与 local rank size（数量，印刷 p3 / 物理 p9）；“不是设备逻辑 ID”不能修复编号和数量的混淆。正文仍未给出 HCCL rank 查询/转换和设备选择的接口定位，也遗漏初审已要求的 InitAll 单卡并发限制（§3.2.4，印刷 p36 / 物理 p42）。

剩余关闭条件：把编号/数量分开；补 Python get_rank_id/get_local_rank_id 与 world↔group 转换、C++ HcclGetRankId、设备选择的接口/样例定位，明确仅样例赋值而非通用等式。补该 InitAll 样板的单卡不得同时调用多个通信操作 API 约束。来源表已有宽页段可沿用，但正文需能查询到实际契约；不要求新增可执行实验。

### C14 — OPEN：技术主体已补，HIP 来源元数据未同步

位置：正文 source_refs L8–17、L59；来源记录 L15；修订映射 L62。

RCCL 框架行现在有 [HIP 2.6 后端名](https://docs.pytorch.org/docs/2.6/notes/hip.html#torch-distributed-backends)及 [RCCL PyTorch CPX 接入](https://rocm.docs.amd.com/projects/rccl/en/docs-10.1.0/how-to/rccl-usage-tips.html#using-rccl-and-cpx-in-pytorch-on-mi300x)依据，区分实际 librccl.so/配套；HCCL 改用 8.1 框架说明，删了“最新页待复核”。这些技术修改可接受。

但正文 source_refs 没有已登记的 `src.pytorch.hip-notes-2.6`，来源表 L15 的 ID 格只写“登记已存在（审阅方引用）”。`src.pytorch.distributed-2.8` 是另一页面/版本，不能替代 HIP 2.6 身份。原关闭条件明确要求把必要来源 ID 加入正文。

剩余关闭条件：复用既有 `src.pytorch.hip-notes-2.6` 加入 source_refs，来源表补准确 ID；CPX 页对应 `src.amd.rccl-docs-10.1.0`。无需新增登记，不要求关闭实际加载或整栈配套 unknown；HCCL PDF 链接同步归 C15。

### C15 — OPEN：悬空引用与精确链接仍有明显遗漏

位置：正文 L35/L44/L50/L52/L58–64/L70/L78–81；来源记录 L3/L13/L15–18/L20/L26。

已满足部分：研究记录已改成表，补 HCCL 双页码/生命周期归属、Test 静态正文和入口异题限制；作者/审阅方角色不再合并为“本轮全部核对”。

剩余：

- L44 的“见 M13”仍在，仓库没有其定义；修订映射“删悬空引用”未落实。
- 两份 HCCL PDF 在正文和来源表均没有可打开的精确 URL，仍只是“PDF＋页码”；正文新 P2P、框架和初始化核心主张也未加对应近旁链接。
- nccl-tests 版本行仍只写“仓库固定 commit”，来源表 README/PERFORMANCE 没有固定文件链接；cann-hccl 仍只写 README，未给固定 commit 文件地址。NCCL 诊断行也仅串列文件/节名。
- 来源记录的原审报告、RCCL 来源记录仍用代码格式文件名代替实际链接；ROCm 来源 ID 未填写（同 C14）。正文还留“写作时浏览器复核”旧措辞，没有同步到已说明的静态正文取证范围。

用户本轮消息报告两份 PDF 已全文提取验证，而正文 verification 与来源记录 L26 仍写“作者仅存活/长度头校验”。可保留初稿历史，但应标明轮次并区分本轮核对范围；也可明确复用已独立核验的审阅记录，不能让历史取证限制看起来仍是当前作者核对范围。此处不要求附全文或大日志。

剩余关闭条件：删除 M13；在正文核心主张近旁和来源表补两份精确 PDF 链接、双页码及已登记 ID；补 nccl-tests README/PERFORMANCE 和 cann-hccl README 的完整固定 commit 链接/实际定位，NCCL 诊断给对应精确页节。把真实研究/审阅文件名改为普通 Markdown 链接，同步 source_refs 和作者核对轮次/角色说明，清理仍未落盘的占位。保留 Test 版本定位、实现与配套 unknown。

## 状态与后续

| 状态 | ID |
|---|---|
| CLOSED（本条目 1；本批累计 10） | C10；原 C01–C09 保持 |
| OPEN（5，仍为原 P2） | C11、C12、C13、C14、C15 |
| 证据阻塞（单列） | BLOCKED-1，blocked_on_evidence/open |

本轮不改变 BLOCKED-1：局部能力事实和排版/来源修订不能证明 HCCL Test × 目标环境的官方版本/运行交集。T03-06 需上述定向修订后再复核；T03-07/T03-08 审阅等待保持。T03-05/T04-01、T02-10/C08 例外及 T02-11 草稿边界均不升级。正文仍 draft/source_checked，无实机验证，未执行 GPU/NPU 或 MPI/collective 命令。

本轮只新增本复核报告，更新 T03-06 初审的最新结果入口及来源审计；作者正文、来源研究记录、修订映射、索引、登记、计划和 Batch 17/18 材料不由审阅者修改。knowledge/docs/plans/sources/src/schemas/paths 输入清单核对仅上述两份既有审阅记录变化与新报告新增，无删除或其他源文件变更；build 由 make 重建。

`make check` / `make build` 均 PASS（88 篇内容 / 386 项来源），本地文件链接及关键远端锚点核对完成。结构检查不证明技术正确性或环境兼容。未改 src/kb，未执行 make test；无真实 GPU/NPU、MPI/collective、配置变更或故障注入。
