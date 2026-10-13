# 第十九批 T03-06 第三次定向复核

复核日期：2026-10-12（Asia/Shanghai）。作者文件中的 `2026-10-14` 保留为输入标签，不作为本轮执行日期。

**结论：C11、C15 转 CLOSED，T03-06 六项审阅发现全部 CLOSED；本批累计 15 CLOSED / 0 OPEN（审阅发现）。** T03-06 在已交付文档/来源范围内通过。既有 BLOCKED-1（HCCL Test × 目标 CANN/HDK/机型）仍为 blocked_on_evidence/open，不能用六项审阅发现关闭代替该子项验收；T03-06 全项及整个 Batch 19 尚未完整验收，T03-07/T03-08 的前置等待保持。

本轮只复核[第二次定向复核](batch-19-t03-06-codex-rerecheck.md)剩余的 C11/C15 及链接/记录同步，不重开此前十三项，无新增发现 ID。约定模型 / effort 为 `gpt-6.1-sol / xhigh`，本会话 Codex 主助手执行，与作者修订角色分开，未派发子代理；实际运行标识无可独立核验元数据，沿用[初审说明](batch-19-codex-review.md)。审阅范围依据[写作指南](../authoring-guide.md#7-批次审阅约定)和[原任务验收](../../plans/full-coverage-backlog.yaml)，不构成硬件验证。

## 输入与审阅方文字校正

| 输入 | SHA-256 |
|---|---|
| [T03-06 正文](../../knowledge/03-communication/communication-library-profiles.md) | `d4a5fb535ba78d852e070f09ff387b69dc6e1ab7cf86620c7ee08e9a99577646` |
| [T03-06 来源记录](batch-19-t03-06-sources.md)（作者交付输入） | `455fb999ca67140a4dfab35385b2332945e68bcdca512814a022491c0f7bc9a7` |
| [修订映射](batch-19-review-fixes.md) | `871bd4624f18f26947ec481f8c64d8c57c6422a5c54a0e83b1a279f83b9c4a7a` |
| [第二次复核](batch-19-t03-06-codex-rerecheck.md) | `4323cd8e9e82633aa401e4e243129a639123de8c61f7e788a76842f81c59b62b` |
| [来源审计](batch-19-source-audit.md) | `4f1a75f31d3e262df3670ff685755de56cb42525c5727dbf113daf5d9417c709` |
| [来源登记](../../sources/registry.yaml)（386 项） | `e84c3b6eb61a83a46dbbfd371e5de4112def120131e0c374181e8e5acbf8f51f` |
| [任务计划](../../plans/full-coverage-backlog.yaml) | `121826a4d499273e7f6a00735e0a53931eef5c097bd66ab6b2425fdbc36ddfe0` |

作者已在正文 verification、来源记录 L3/L26 写明首轮 HEAD 与本轮全文提取、审阅方独立渲染的区别，剩余 L27 的旧尾句却仍写“作者仅存活/长度头校验”。审阅方在该尾句中仅插入 **“首轮”两个字**，使历史取证限制与前文现轮记录一致；这处文字校正归审阅方，不追记为作者交付时已修改，不新增作者取证事实。

来源记录校正后 SHA 为 `91ed2af03140ef259c999102347f6e4e314032407c88c7d491277db098626a81`。逆向删除这两个字可精确恢复上述作者输入 SHA；本轮知识正文和修订映射未由审阅方修改。T03-05/T04-01、RCCL 来源记录、03 索引、登记/计划及 Batch 17/18 输入对照第二次复核未变。

## 一次源与链接核对

默认 TLS 校验重新获取四个精确地址：两份 HCCL PDF，以及 NCCL 2.27.5 communicators/env；全部 HTTP 200，SHA 均与初审固定证据相同。两份 PDF 全文重新提取，逐个读取本轮 #page 入口及连续小节，渲染检查 API 物理 p8、指南物理 p10 的完整页。固定 README/PERFORMANCE、cann-hccl 快照和 troubleshooting 锚点沿用[第二次复核的独立取证](batch-19-t03-06-codex-rerecheck.md#一次源复验)，本轮没有声称重新执行测试工具或取得 Test 配套材料。

| 原文件 | SHA-256 |
|---|---|
| HCCL 8.0 API PDF | `84d023900b87785b2a5c1847b6574683a5b7c13077be110e3a63c7a0159e9a0d` |
| HCCL 8.1 指南 PDF | `39eac20ceb03e4e422153f411c883562edb2f06975b47f40eb5fb54f2a629d9a` |
| NCCL communicators HTML | `aa888933f603b91a8adbc1e32a3d0bdd58b34ef35fea1cc85d3135ab1943b3ab` |
| NCCL env HTML | `748cc433bc2aa9ec61570ebc57f4e3c5e9a1845106c43ba52a6eba712f472303` |

PDF 的 #page 是物理入口页，按正文节号和来源表的连续页段核对，不能理解为整段所有主张都在入口单页。例如 8.0 的流程引导段在物理 p7，三阶段正文在 p8；8.1 的流程引导段在 p9，四阶段正文在 p10。C++ 接口索引入口在 p38，通信域管理正文在 p40–44；框架概述从 p7 开始，接口适配说明在 p8。均处于该版本正确小节及已列页段，不混同印刷/物理页码，也不把流程名称跨版本拼接。

正文与来源记录中的本地链接全部解析到现存文件；NCCL/HCCL 六个指南/案例/实验链接逐个核对存在。原文、PDF 页图和日志只存临时目录，未镜像入库，无新增登记。

## C11 — CLOSED

正文 L63 恢复默认关闭时由调用方经显式 CUDA stream 依赖/同步维持跨 communicator 一致总序的说明；L69 保留启用后的主机发起次序、graph 捕获/launch、多组创建/执行和 work.wait 层级等已接受条件。[NCCL communicator 并发节](https://docs.nvidia.com/deeplearning/nccl/archives/nccl_2275/user-guide/docs/usage/communicators.html#using-multiple-nccl-communicators-concurrently)与[隐式次序开关定义](https://docs.nvidia.com/deeplearning/nccl/archives/nccl_2275/user-guide/docs/env.html#nccl-launch-order-implicit)的分支区分保持一致。

L70 的泛称已替换成六个实际普通 Markdown 链接：NCCL 指南/来源案例/实验与 HCCL 指南/来源案例/实验；T03-04 和 RCCL 档案入口保留。它们是独立资料/待执行设计导航，不作为本库已执行实验的声明。第二次复核的两项剩余要求均满足。

## C15 — CLOSED

正文 L59、L60、L63、L72 已在 HCCL 原语/P2P/局部错误查询、框架、初始化/映射主张近旁加入正确版本 PDF 链接，并以节号和双页码表明确支持范围；新增物理页入口按连续小节核对成立。统一主机完成边界、Test 计时实现和整栈配套 unknown 保留。

来源记录 L13/L16–20 现有精确 NCCL 诊断页节、固定 nccl-tests README/PERFORMANCE、cann-hccl README、两份 PDF URL 与双页码、RCCL 研究记录链接；L3 的审阅报告入口和 L26 的取证轮次/角色已同步。修订映射将本页事项单列，正文作者核对范围不再夹入 0106/0083/0086/0091 等 T04-01 具体页。HCCL Test 的官方静态页及当前入口异题限制仍按原角色记录，不以此关闭配套子项。

唯一旧尾句的历史轮次遗漏已由上述审阅方两个字校正消除，当前作者全文提取与审阅方渲染的区别不再冲突。C15 在这一明确记录的校正后关闭；原精确链接、定位和角色同步要求均满足。

## 状态与通过边界

| 状态 | ID / 范围 |
|---|---|
| T03-06 审阅发现 CLOSED（6） | C10、C11、C12、C13、C14、C15 |
| 本批累计 CLOSED（15） | C01–C15 |
| 审阅发现 OPEN（0） | 无 |
| 既有验收子项 OPEN（单列） | BLOCKED-1，HCCL Test × 目标环境官方交集 |

T03-06 已交付能力对照、独立文档样板、已知接口/映射/次序、诊断和来源追溯的有限文档范围通过；这是审阅发现的闭环，不是整个任务完成。原 acceptance 5 要求的目标 CANN/HDK/机型与 HCCL Test 官方交集未证实，因此该子项继续 blocked_on_evidence/open，T03-07/T03-08 不自动解锁。本轮未推进后续写作，未改变任务计划状态。

T03-05/T04-01 的既有有限通过范围、T02-10/C08 例外和 T02-11 草稿边界保持。正文仍 draft/source_checked，无真实环境验证；版本交集、TorchNPU 实际加载和其他既有 unknown 不因文字校正或链接可访问而关闭。

本轮新增本报告并更新 T03-06 三份旧审阅报告及来源审计的最新入口；另对作者来源记录仅作上述两个字的审阅方文字校正。knowledge/docs/plans/sources/src/schemas/paths 输入清单核对仅上述五份既有记录变化和新报告新增，无删除；来源记录逆向去掉“首轮”可恢复输入身份。知识正文、修订映射、索引、登记、计划、Batch 17/18 材料保持本轮输入，build 由 make 重建。

`make check` / `make build` 均 PASS（88 篇内容 / 386 项来源），本地文件链接、状态入口和受保护输入核对完成。结构检查不证明技术正确性、全部远端链接或环境交集。未改 src/kb，未执行 make test；无真实 GPU/NPU、MPI/collective、配置变更或故障注入。
