# 第十九批 T03-06 补充初审

**最新状态（2026-10-12）：第三次定向复核后 C10–C15 全部 CLOSED；本批累计 15 CLOSED / 0 OPEN（审阅发现）。** T03-06 已交付文档/来源范围通过，BLOCKED-1 继续 blocked_on_evidence/open，任务全项未验收，T03-07/T03-08 仍等待；通过边界及审阅方两个字的文字校正见[第三次定向复核](batch-19-t03-06-codex-third-recheck.md)。以下为补充初审的历史输入和判定，不作为当前六项状态。

审阅日期：2026-10-12（Asia/Shanghai）。作者正文和来源记录中的 `2026-10-14` 保留为输入标签，不作为本轮执行日期。

**结论：T03-06 需要修订，本轮新增 6 项 P2（B19-C10–C15），全部 OPEN；已有 HCCL Test 配套子项 BLOCKED-1 继续 blocked_on_evidence/open，单列而不重复计为新发现。** T03-05/T04-01 的既有有限通过范围和 C01–C09 CLOSED 保持。本轮未通过 T03-06，T03-07/T03-08 的审阅等待不解除，不声明整个 Batch 19 完成。

约定模型 / effort 为 `gpt-6.1-sol / xhigh`，由本会话 Codex 主助手执行，与作者写作角色分开；未派发子代理。实际运行标识无可独立核验元数据，沿用[初审说明](batch-19-codex-review.md)。依据 [AGENTS](../../AGENTS.md)、[写作指南](../authoring-guide.md#7-批次审阅约定)和[原任务验收](../../plans/full-coverage-backlog.yaml)审阅。文档审阅与硬件验证分开。

## 输入身份与范围

| 输入 | SHA-256 |
|---|---|
| [T03-06 正文](../../knowledge/03-communication/communication-library-profiles.md) | `07fef009ae5f7351b3b6406149bad7de6dd042360d6b27a09b8f0e105e75c804` |
| [T03-06 来源记录](batch-19-t03-06-sources.md) | `018a2543275d5702106ea2970dff1676b2b222ae18d9da877284725991f2810e` |
| [T03-05 当前正文](../../knowledge/03-communication/rccl-runtime-and-verification.md) | `1f95d5b310726d858900e2028ab3b779f1470b03a1ba67187fbed1c6da5b19db` |
| [T03-05 来源记录](batch-19-rccl-sources.md) | `891c737e94dcfc4d1c40e5a7ed9cf6f96847ba56fdecb46482a8c3394b8b50c2` |
| [T04-01 正文](../../knowledge/04-data-storage/training-data-path.md) | `f703eba9a49f545e7e62ec3864c3e0b176b313f9fcdcbdfffc565200c2cbcb81` |
| [03 索引](../../knowledge/03-communication/index.md) | `e935b8cd81d7a0b271833a4c6598cdc909293b87061e62c3191f7363ff4565da` |
| [来源审计](batch-19-source-audit.md) | `41d77067a66359575dba2f019a749919e931861773e4c11d5e34f76fc6abcffd` |
| [来源登记](../../sources/registry.yaml)（386 项） | `e84c3b6eb61a83a46dbbfd371e5de4112def120131e0c374181e8e5acbf8f51f` |
| [任务计划](../../plans/full-coverage-backlog.yaml) | `121826a4d499273e7f6a00735e0a53931eef5c097bd66ab6b2425fdbc36ddfe0` |

本轮检查新正文、来源记录、版本边界、能力行和 rank/group/设备/次序验收。RCCL 列沿用[第三次复核](batch-19-codex-third-recheck.md)接受的接口、错误、日志和测试口径；新增框架行另审。双向正文链接及 related_ids 已接通。当前 T03-05 全文 SHA 与上次输入不同，本轮不声称字节冻结相同，也不重做其完整审阅；T04-01 与 RCCL 来源记录身份保持。

## 审阅方一次源核对

默认 TLS 校验只读获取 21 个地址，均 HTTP 200，但分别检查正文和版本定位，不将可达性当作证据。包括两份 HCCL PDF 全文、NCCL 2.27.5 八个具体页面、PyTorch 2.8 distributed、固定 nccl-tests/cann-hccl README、910 路径 HCCL Test 五个官方静态正文及普通入口，另取 PyTorch HIP 2.6 和 RCCL usage-tips。

两份 PDF 提取正文并渲染核对相关完整页；页码下文区分印刷页和 PDF 物理页。主要定位如下，均为审阅方此次取证，不能写成作者当时已完成：

| 证据 | 精确来源与定位 | 支持范围 |
|---|---|---|
| E1 | [NCCL 2.27.5 Types / ncclResult_t](https://docs.nvidia.com/deeplearning/nccl/archives/nccl_2275/user-guide/docs/api/types.html#ncclresult-t) | 0–7 共八个返回值，含 ncclRemoteError；Success/InProgress 不属于错误 |
| E2 | [communicators / 多 communicator 并发](https://docs.nvidia.com/deeplearning/nccl/archives/nccl_2275/user-guide/docs/usage/communicators.html#using-multiple-nccl-communicators-concurrently)、[env / NCCL_LAUNCH_ORDER_IMPLICIT](https://docs.nvidia.com/deeplearning/nccl/archives/nccl_2275/user-guide/docs/env.html#nccl-launch-order-implicit) | 2.26 起新增可启用的隐式次序；2.27.5 默认关闭；CUDA runtime/driver 条件影响重叠执行 |
| E3 | [PyTorch 2.8 new_group](https://docs.pytorch.org/docs/2.8/distributed.html#torch.distributed.new_group)、[get_group_rank](https://docs.pytorch.org/docs/2.8/distributed.html#torch.distributed.get_group_rank)、[get_global_rank](https://docs.pytorch.org/docs/2.8/distributed.html#torch.distributed.get_global_rank) | 组创建、全局次序、多线程同步、async 跨组 work.wait；两个 rank 转换 API 的成员资格条件 |
| E4 | [HCCL 8.0.RC1.alpha003 API PDF](https://www.hiascend.com/doc_center/source/zh/CANNCommunityEdition/80RC1alpha003/apiref/hcclapiref/CANN%208.0.RC1.alpha003%20%E9%9B%86%E5%90%88%E9%80%9A%E4%BF%A1%E6%8E%A5%E5%8F%A3%E5%8F%82%E8%80%83%2001.pdf)；表 1-1，§2.2.1/2.2.5–2.2.8，§3.1–3.5 | 印刷 p3–4 / 物理 p9–10：rank 概念；印刷 p8–15 / 物理 p14–21：Python group 与转换；印刷 p32–38 / 物理 p38–44：C++ 通信域与设备；印刷 p50–53 / 物理 p56–59：P2P 与局部异步错误查询 |
| E5 | [HCCL 8.1.RC1.alpha001 用户指南 PDF](https://www.hiascend.com/doc_center/source/zh/CANNCommunityEdition/81RC1alpha001/devguide/hccl/hcclug/CANN%E7%A4%BE%E5%8C%BA%E7%89%88%208.1.RC1.alpha001%20%E9%9B%86%E5%90%88%E9%80%9A%E4%BF%A1%E7%94%A8%E6%88%B7%E6%8C%87%E5%8D%97%2001.pdf)；§1、§4、§9.1.2 | 印刷 p1–4 / 物理 p7–10：产品/链路、框架接口、四阶段；印刷 p11 / 物理 p17：AlltoAllV；印刷 p83–84 / 物理 p89–90：EI0002 |
| E6 | HCCL Test 官方静态[介绍 0001](https://www.hiascend.com/doc_center/source/zh/CANNCommunityEdition/910/devaids/hccltool/HCCLpertest_16_0001.html)、[环境 0004](https://www.hiascend.com/doc_center/source/zh/CANNCommunityEdition/910/devaids/hccltool/HCCLpertest_16_0004.html)、[参数 0005](https://www.hiascend.com/doc_center/source/zh/CANNCommunityEdition/910/devaids/hccltool/HCCLpertest_16_0005.html)、[结果 0006](https://www.hiascend.com/doc_center/source/zh/CANNCommunityEdition/910/devaids/hccltool/HCCLpertest_16_0006.html)、[规格 0007](https://www.hiascend.com/doc_center/source/zh/CANNCommunityEdition/910/devaids/hccltool/HCCLpertest_16_0007.html) | 910 路径当前可读正文支持算法带宽和 b/e=64M、n=20、w=10；输出/校验有条件；不证明精确工具制品版本、计时实现或与目标 HDK 的交集 |
| E7 | [cann-hccl README @2d685b08](https://gitee.com/ascend/cann-hccl/blob/2d685b084a60366b47ad8e50a563ee5c4dbef7fe/README.md)、[nccl-tests README @b4d5beeb](https://github.com/NVIDIA/nccl-tests/blob/b4d5beebca8a76cf01335f724d154b9b9d394d96/README.md) | 算法/源码配套警告/库自测，与测试工具分别取证；nccl-tests 参数仅限固定快照 |
| E8 | [PyTorch HIP 2.6 / distributed backends](https://docs.pytorch.org/docs/2.6/notes/hip.html#torch-distributed-backends)、[RCCL docs-10.1.0 / PyTorch CPX](https://rocm.docs.amd.com/projects/rccl/en/docs-10.1.0/how-to/rccl-usage-tips.html#using-rccl-and-cpx-in-pytorch-on-mi300x) | ROCm 上后端名 nccl/gloo；官方 PyTorch 使用 RCCL 的说明，并要求核对实际 librccl.so；不能拼为 PyTorch 2.8 × RCCL 2.30.7 已测组合 |

普通 HCCL Test 入口本轮 HTTP 200，但 HTML title 为 MindCluster6.0.RC3 日志采集页，与所请求的 Test 页面不符；五个官方静态正文没有同样的顶层版本标题。故保留原登记的“2026-09-30 观察”身份与当前 910 路径取证的区别，不声称复现了当时 title 或已得到精确 release 配套。静态正文足以核对上述局部字段，无需用浮动 redirect 代替；仍不能关闭 BLOCKED-1。

| 主要原文件 | 字节数 | SHA-256 |
|---|---:|---|
| HCCL 8.0 API PDF（79 页） | 1112154 | `84d023900b87785b2a5c1847b6574683a5b7c13077be110e3a63c7a0159e9a0d` |
| HCCL 8.1 用户指南 PDF（115 页） | 2263907 | `39eac20ceb03e4e422153f411c883562edb2f06975b47f40eb5fb54f2a629d9a` |
| NCCL Types HTML | 67857 | `869e955f94ea828c02c086c389af2f9b5aa35d35d7c11cd4179bf98a824d779a` |
| NCCL env HTML | 148973 | `748cc433bc2aa9ec61570ebc57f4e3c5e9a1845106c43ba52a6eba712f472303` |
| PyTorch distributed 2.8 HTML | 577144 | `0a31347c4a0cedf879b56c61ed7a2c8330b627c9eb7d12ba40883cbd51054fcb` |
| HCCL Test 0005 静态 HTML | 48709 | `85dfdd58f53d37d5428d0559a057228526d5ccbee233a095887c12aacc8006fe` |
| cann-hccl 固定 README | 14099 | `9e9507c4a64b61a3544043566f510c0ce0ee03310ce12a4993c7fa3db1264699` |
| nccl-tests 固定 README | 9717 | `7e1aef831b6bcd0befec250e82333d58dd71078730bafda03c7a99532f452895` |

原文、PDF 页图和抓取日志只保存在临时目录，未镜像入库。E8 两个来源已在登记表中存在；审阅发现不新增来源登记，不修改 Batch 17 文件或将其草稿变成已验收前置。

## 新发现及关闭条件

### B19-C10 — P2：NCCL 返回码计数口径不完整

位置：T03-06 L63。

“7 类返回码”与 E1 的完整 `ncclResult_t` 不一致：0–7 共八值，含 `ncclRemoteError`。communicators 的摘要表确实只有七行，但漏了 Types 中的 RemoteError；不能把该摘要行数当完整返回类型计数。若只计非零值也须说清，其中 InProgress 是进展状态，并非错误；否则与 RCCL“9 码”比较的分母不同，网络/远端失败类别也不可见。

关闭条件：按 Types 明列或链接八个值，说明 Success/InProgress 与六类错误的关系，保留摘要表缺项这一来源差异；RCCL 比较使用一致的计数口径，不从摘要表推导错误类型不存在。

### B19-C11 — P2：多 communicator / process group 次序只剩名称，缺少关键条件

位置：T03-06 L62、L68。

正文只说“2.26+ 主机发起次序匹配”和“全局次序约束”，没有说明 E2 的隐式总序需要启用 `NCCL_LAUNCH_ORDER_IMPLICIT`，且选定 2.27.5 默认值为 0。由文档给出的启用条件可知，不能将主机调用一致当成默认配置下显式 stream 依赖/同步的替代。E3 另规定默认组创建的参与者与创建顺序、多线程同步，以及 async 操作后切换 process group 前 `work.wait()` 的 stream 同步义务；这些属于框架契约，不能用 NCCL communicator 页概括。

关闭条件：把库层启用/关闭分支与 PyTorch 2.8 的创建/执行/async 跨组条件分列并近旁链接；写明 work.wait 的同步层级，不把它统一解释成 CPU 等待设备全部完成。不要由 NCCL 文档推出 RCCL/HCCL 的相同约束。补本条目到已有 NCCL/HCCL 独立指南、案例和方案的导航，满足 acceptance 4，而非仅用任务号代指。

### B19-C12 — P2：HCCL 列未呈现已取得的 P2P 与错误查询能力

位置：T03-06 L58、L63。

NCCL/RCCL 均列 P2P，HCCL 却只列概述中的五个 collective 和算法名。E4 的 C++ 接口已列 Reduce、AlltoAllV、Barrier、Send/Recv、BatchSendRecv 和 GetCommAsyncError；E5 也说明 AlltoAllV。尤其 E4 §3.4.1–3.4.3 明确普通 Send/Recv 的配对同步调用，以及批量接口“同卡任务互不阻塞、卡间仍需配对”的限定；§3.5.1 还给出该版本只返回 HCCL_E_REMOTE 的错误查询范围。统一主机完成边界 unknown 不等于这些具体接口能力也未知。

关闭条件：用 8.0 的具体接口补齐 P2P、已知错误查询和同步范围；collective 清单补主要遗漏或明确其非穷举范围，避免与另两库的不对称展示产生“不支持”的误读。区分 Python 与 C++ 接口、算法与原语；不要把 BatchSendRecv 的局部“异步”提升为统一主机返回语义。保留未证实完成边界和版本适用限制。

### B19-C13 — P2：HCCL 初始化与设备/rank 映射尚未落到接口契约

位置：T03-06 L62、L70。

四阶段是生命周期概述，world/group/local 三个名称是概念分类；当前 HCCL 列未说明 C++ 通信域如何初始化和映射设备，却把 Python group 重新编号与其并列压成一句。E4 区分 ranktable 初始化、rootInfo 的获取/广播/初始化，以及单机 InitAll 的逻辑 device 列表、顺序和禁止重复；还规定 RootInfo 初始化只能串行、InitAll 单卡并发调用限制。local rank 是指定 group 在本 Server 内的编号，不能据“三层”直接当作设备逻辑 ID。仅有“同名不等价”不足以完成 acceptance 4 的映射与次序核对。

关闭条件：补一张小表或等量说明，分清 Python world/custom/local 与 C++ comm/rank/device 的接口层次；给出选定版本初始化输入、rank 查询/转换、设备选择和上述串行/单卡约束的来源定位。样例中 rank=device 的赋值只作样例，不扩成通用映射。生命周期四阶段另归正确的 8.1 来源，不将各版本组合成目标环境。

### B19-C14 — P2：框架后端行仍是待写占位

位置：T03-06 L59。

RCCL 栏“PyTorch ROCm 后端另行取证”没有提供必交的框架后端说明；HCCL 栏则引用未登记在本文 source_refs 的“社区最新页，待复核”，尽管 E5 印刷 p2 已直接给出 C 单算子 / Python 图模式框架适配。E8 的已登记材料亦可支持 ROCm 后端名及官方 PyTorch/RCCL 使用关系的有限说明。保留实际发行包加载路径、版本交集 unknown 是正确的，但不能代替已可取得的接口/接入层证据。

关闭条件：按独立框架版本样板填 RCCL 行并引用官方依据，明确后端名与底层库、二进制实际加载和版本配套是不同事实；HCCL 采用已核对的 8.1 页，或另固定并登记真实使用来源，删“最新页待复核”占位。必要的来源 ID 加入正文 source_refs；不要求借此证明 TorchNPU 动态加载或 PyTorch 2.8 × RCCL 2.30.7 配套，也不将 Batch 17 草稿升级为验收依据。

### B19-C15 — P2：主张—来源记录仍不可逐项复核，各版本出处未就近区分

位置：T03-06 L35、L44、L50–52、L58–64、L68–70、L78–81；来源记录 L3、L9–11、L17。

“见 M13”“取证报告 §3 草案（M1–M14）”“同批来源准备报告”均没有可打开的报告或相应表，当前仓库检索未找到这些定义。所谓定位表仍是一段文件名/节号串；正文 HCCL 多处没有普通 Markdown 精确来源链接，nccl-tests 仅写“固定 commit”。更具体地，四阶段流程实际在 E5 印刷 p4 / 物理 p10，8.0 API 物理 p10 则是 rank 概念续表；8.0 API 物理 p8 的流程为三阶段。L62 句末“8.0 p10”可支持后半句 rank 概念，却不能支持未单独注明出处的四阶段；来源记录笼统列“8.0 PDF（执行流程）”也不足以区分二者，需要逐主张落实三线分立。

作者记录也明确本轮两份 PDF 只做 HEAD/长度检查、Test 只取得外壳，却在 verification 声称按固定来源核对，并留“写作时须复核”未完成项。本审阅者取得的正文和局部事实核对不能追记为作者当时完成。

关闭条件：把记录改成真实映射表，逐项含主张、已登记 ID、精确页面/固定文件、PDF 双页码或源码行号、支持范围与未证条件；链接真实准备报告或删悬空引用。正文在关键主张近旁补链接，分别标明四阶段和 rank 概念的文档版本/页码，统一双页码口径。区分历史登记、作者此次核对和审阅方新取证；若复用本报告，明确角色和限定范围。核对可读官方静态页与当前入口异常后记录版本定位限制，保持 Test 配套和实现 unknown；不以 HTTP 200、路径数字或缺标题证明完整版本交集。

## 原验收项与后续状态

| 验收项 | 本轮判定 |
|---|---|
| 1：逐库能力行 | PARTIAL：C10/C12/C14；RCCL 已接受的运行/测试口径保持 |
| 2：独立版本档案 | 文档线分开可接受；框架样板与精确来源尚待 C14/C15，HCCL 目标环境未固定 |
| 3：不拼接 8.x API / 9.1.X Test，列未证配套 | 边界表述可接受；不等于获得自洽交集 |
| 4：rank/group/device/次序与独立资料互链 | PARTIAL：C11/C13/C15；RCCL 双向链接已存在 |
| 5：Test 与目标环境的官方交集 | BLOCKED-1：blocked_on_evidence/open，不能因修正文档或登记测试工具关闭 |

BLOCKED-1 延续作者清单，是已知证据缺口：需要固定目标 CANN、HDK 驱动/固件、机型、Test 制品或发行版本，再取得明确支持这些版本与运行前提的官方材料，并逐条件核对。不要求执行实机实验；现有 PDF/静态页/源码警告不证明不存在任何官方交集，也不证明当前已取得一个交集。接受三线分立和库自测/Test 分离，不把该子项降格为可自动关闭的备注。

| 状态集合 | ID |
|---|---|
| 原审 CLOSED（9） | B19-C01–C09，原有限通过范围保持 |
| 本轮新增 OPEN（6，均 P2） | B19-C10–C15；修订后逐项定向复核 |
| 既有证据阻塞（单列） | BLOCKED-1（HCCL Test × 目标 CANN/HDK/机型） |

T03-06 未通过；T03-07 继续等待，T03-08 按 T03-07 前置顺序等待。本文仍 draft/source_checked，硬件验证为未执行；NCCL/CUDA/驱动实际配套、TorchNPU 加载、HCCL 统一完成语义及 Test 计时实现保留未知。T02-10/C08 例外和 T02-11 草稿边界不升级。

本轮仅新增本审阅报告并更新来源审计的当前入口和状态，未修改作者正文、研究记录、修订映射、索引、登记、任务计划或 Batch 17/18 材料。输入清单覆盖 knowledge/docs/plans/sources/src/schemas/paths，核对仅本审计发生修改、新增本报告，无删除或其他源文件变更；生成 build 由 make 重建。

`make check` / `make build` 均 PASS（88 篇内容 / 386 项来源）；本地文件链接及上述关键远端锚点核对完成。结构检查不证明技术正确性、全部远端链接或环境兼容。未改 src/kb，未执行 make test；无真实 GPU/NPU、MPI/collective 执行或配置变更。
