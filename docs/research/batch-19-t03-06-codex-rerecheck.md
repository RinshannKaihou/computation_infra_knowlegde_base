# 第十九批 T03-06 第二次定向复核

**最新状态（2026-10-12）：第三次定向复核后 C11/C15 转 CLOSED，六项审阅发现全部关闭；本批累计 15 CLOSED / 0 OPEN。** T03-06 已交付文档/来源范围通过，BLOCKED-1 仍为单列 open，任务全项未验收，T03-07/T03-08 仍等待；通过边界及审阅方两个字的文字校正见[第三次定向复核](batch-19-t03-06-codex-third-recheck.md)。下文保留第二次复核的历史输入和判定。

复核日期：2026-10-12（Asia/Shanghai）。作者文件中的 `2026-10-14` 保留为输入标签，不作为本轮执行日期。

**结论：C12、C13、C14 转 CLOSED；C11、C15 仍 OPEN。T03-06 累计 4 CLOSED / 2 OPEN，本批累计 13 CLOSED / 2 OPEN。** C10 与原 C01–C09 保持 CLOSED，无新增发现 ID。BLOCKED-1（HCCL Test × 目标 CANN/HDK/机型）继续 blocked_on_evidence/open，单列而不重复计为发现。T03-06 尚未通过，T03-07/T03-08 继续等待；T03-05/T04-01 的既有有限通过范围保持。

约定模型 / effort 为 `gpt-6.1-sol / xhigh`，由本会话 Codex 主助手执行，与作者修订角色分开；未派发子代理。实际运行标识无可独立核验元数据，沿用[初审说明](batch-19-codex-review.md)。本轮按[第一次定向复核](batch-19-t03-06-codex-recheck.md)的剩余关闭条件复核，不将交付摘要当作实际落盘结果，不将来源核对升级为硬件验证。

## 输入与变更范围

| 输入 | SHA-256 |
|---|---|
| [T03-06 正文](../../knowledge/03-communication/communication-library-profiles.md) | `b2f0c549146eb44da3f663831ebc63feb20301facb154f54d920842ef9350bb1` |
| [T03-06 来源记录](batch-19-t03-06-sources.md) | `c184f46993929869d39b66a5055554fd2d498d71f745c43730c8e53841ce5edb` |
| [修订映射](batch-19-review-fixes.md) | `aaa6945feda4d4a81be6006b4b938e62efd9bf835238eb0631de81ea45297986` |
| [T03-06 初审](batch-19-t03-06-codex-review.md) | `672c4fbd44ffb63d44f34bd75b991d588f98eadaf762869f3698875fd27e54c3` |
| [第一次复核](batch-19-t03-06-codex-recheck.md) | `51bea5da8054059312aff1d41d5caf99e36bba8ac7f933bf5808b53ede4f953e` |
| [来源审计](batch-19-source-audit.md) | `1cb3866ac270fdc2e5cc04d0e451133ac98bd6807e75b90828bd4ef2fc3e3056` |
| [来源登记](../../sources/registry.yaml)（386 项） | `e84c3b6eb61a83a46dbbfd371e5de4112def120131e0c374181e8e5acbf8f51f` |
| [任务计划](../../plans/full-coverage-backlog.yaml) | `121826a4d499273e7f6a00735e0a53931eef5c097bd66ab6b2425fdbc36ddfe0` |

T03-05/T04-01、RCCL 来源记录、03 索引、登记、计划及 Batch 17/18 输入对照上次复核未变。本轮审阅者只写审阅报告和当前状态入口，不修改作者正文、来源表、修订映射、索引或任务状态。

## 一次源复验

默认 TLS 校验重取 11 个地址，均 HTTP 200：两份 HCCL PDF，NCCL 2.27.5 communicators/env/troubleshooting、PyTorch 2.8 distributed，nccl-tests 固定 README/PERFORMANCE 的 blob 页面与 PERFORMANCE raw，以及正文使用的 cann-hccl 短 SHA README blob/raw。精确 PDF 地址及正文定位沿用[补充初审证据表](batch-19-t03-06-codex-review.md)。

两份 PDF 全文重新提取，核对本轮接口/编号/InitAll 章节并渲染检查 API 物理 p33/p42 的完整页；PDF 与三份 NCCL 页面 SHA 与初审相同。PyTorch HTML 原字节变动，去 script/style 并归一化空白后的全部可见文本与初审相同。四个 troubleshooting 锚点 `errors`、`ras`、`gpu-direct`、`topology-detection` 均存在，Topology 修正已接受。

新增 [nccl-tests README](https://github.com/NVIDIA/nccl-tests/blob/b4d5beebca8a76cf01335f724d154b9b9d394d96/README.md) 和 [PERFORMANCE](https://github.com/NVIDIA/nccl-tests/blob/b4d5beebca8a76cf01335f724d154b9b9d394d96/doc/PERFORMANCE.md) 链接定位到固定文件；[cann-hccl 短 SHA README](https://gitee.com/ascend/cann-hccl/blob/2d685b08/README.md) 的 raw 文件与已登记完整 commit `2d685b084a60366b47ad8e50a563ee5c4dbef7fe` 的原文件字节相同，接受这一快照定位。Test 静态页和计时实现不在本轮新增复验范围，BLOCKED-1 不变。

| 关键原文件 | SHA-256 |
|---|---|
| HCCL 8.0 API PDF | `84d023900b87785b2a5c1847b6574683a5b7c13077be110e3a63c7a0159e9a0d` |
| HCCL 8.1 指南 PDF | `39eac20ceb03e4e422153f411c883562edb2f06975b47f40eb5fb54f2a629d9a` |
| NCCL communicators HTML | `aa888933f603b91a8adbc1e32a3d0bdd58b34ef35fea1cc85d3135ab1943b3ab` |
| NCCL env HTML | `748cc433bc2aa9ec61570ebc57f4e3c5e9a1845106c43ba52a6eba712f472303` |
| NCCL troubleshooting HTML | `ae26c111602e8d2dcc2327bb19ac1688dccb3932f698ee868c45e9d60ee8898d` |
| PyTorch distributed HTML | `c18f40914564a76abe14fcf5d7f0d055696f440a480036f09f9a87fd0ed9de7c` |
| nccl-tests PERFORMANCE raw | `2242493053a6f9d5db1c6542a8ce7740be919778645125b94eeae440efd31edf` |
| cann-hccl 短 SHA README raw | `9e9507c4a64b61a3544043566f510c0ce0ee03310ce12a4993c7fa3db1264699` |

原文、PDF 页图和抓取日志只存临时目录，无新增来源登记，无 MPI/collective 或硬件命令执行。

## 逐项判定

### C11 — OPEN：恢复默认关闭分支，并把案例/实验提示落实为链接

位置：正文 L63/L69–70；来源记录 L12/L14；修订映射“第二轮修订”C11 行。

已满足部分：启用隐式次序后主机发起顺序匹配、单线程确定性次序、graph 捕获/launch 同规则，new_group 全体进入/相同创建顺序、多组全局执行次序、多线程同步、async 跨组 work.wait 层级和查询成员资格均已增加；T03-04 与 HCCL 超时指南现在有实际链接。不从 NCCL 推出另两库约束的边界保留。

但上一轮已接受的“默认关闭时显式 stream 依赖/同步不可省”说明在本轮正文中被删掉：L63 只记录默认 0，L69 只讲启用后的发起次序。仍需保留关闭分支下由调用方维护一致总序的说明。[communicators 并发节](https://docs.nvidia.com/deeplearning/nccl/archives/nccl_2275/user-guide/docs/usage/communicators.html#using-multiple-nccl-communicators-concurrently)与[开关定义](https://docs.nvidia.com/deeplearning/nccl/archives/nccl_2275/user-guide/docs/env.html#nccl-launch-order-implicit)支持原关闭条件中的分支区分，不能只保留开关数字。

L70 标为“指南/案例/实验导航”，但只链接指南/档案；案例/实验仍写不可点击的 `source-case/experiment` 泛称。已有 [NCCL 超时指南](../../knowledge/03-communication/nccl-timeout-triage.md)、[NCCL 案例](../../knowledge/03-communication/nccl-timeout-source-case.md)、[NCCL 实验](../../knowledge/03-communication/nccl-timeout-experiment.md)、[HCCL 案例](../../knowledge/03-communication/hccl-timeout-source-case.md)、[HCCL 实验](../../knowledge/03-communication/hccl-timeout-experiment.md)均可直接复用，不需新增正文。原任务 acceptance 4 与第一次复核要求的实际链接尚未全部落实。

剩余关闭条件：补回“隐式次序关闭时，通过显式 CUDA stream 依赖/同步维持跨 communicator 一致总序”的限定；保持启用后的已修正条件。将现成 NCCL/HCCL 指南、案例、实验写成普通 Markdown 链接，替换泛称。无需扩大实验或取证范围。

### C12 — CLOSED

正文 L59 已把物理 ID 条件移到 Python 图接口 §2.4.6/2.4.7，保留印刷 p26–27 / 物理 p32–33；C++ Send/Recv 不再承受该外推，也未反向断言任意跨 Server 映射受支持。8.0 API 的相关原页及 C++ §3.4.1–3.4.3 独立核对与此一致。原同步、批量配对、局部错误查询及统一完成语义 unknown 保持，原剩余条件满足；精确近旁链接同步仍按 C15 跟踪，不重复计入本项。

### C13 — CLOSED

正文 L72 已区分 local rank id 编号与 size 数量，列 Python 查询/转换、HcclGetRankId、逻辑 devices 选择与列表次序、rootInfo 配对/串行、InitAll 单机范围及单卡多操作禁止；样例等式没有扩成通用映射。8.0 API 表 1-1、§2.2.5–2.2.8、§3.2.4/3.2.7 支持这些主张，8.0/8.1 生命周期归属保持。

多线程的 `HCCL_CONNECT_TIMEOUT` 简写按原页“不同线程调用的前后时间差”理解，不能扩为通信操作完成时限；本轮不作完成边界升级。接口/双页码的来源链接仍按 C15 同步。本项原技术剩余要求已满足。

### C14 — CLOSED

正文 source_refs L12 已加入已登记 `src.pytorch.hip-notes-2.6`；来源记录 L15 写准确 ID，并把 CPX 接入归到 `src.amd.rccl-docs-10.1.0`。框架后端名、实际加载/配套、HCCL 8.1 适配说明的上轮可接受范围保持，未新增登记或跨版本支持组合，原剩余条件满足。

### C15 — OPEN：正文已有链接，来源表与近旁引用未同步完成

位置：正文 L36/L59–60/L63/L65/L72/L82；来源记录 L3/L13/L16–18/L20/L26；修订映射第二轮 C15 行。

已满足部分：删除 M13；补固定 nccl-tests README/PERFORMANCE、cann-hccl 快照及 troubleshooting 精确页节；两份 PDF 在正文 L82 的来源汇总已有可打开链接。verification 已区分首轮 HEAD 与本轮作者全文提取，普通 Test 入口异常和配套限制继续保留。

剩余仍直接对应上轮关闭条件：

1. HCCL 新原语/P2P、框架与初始化/映射主张（L59/L60/L63/L72）依然只有 API 名、节号或页码，没有近旁的 PDF 链接；L82 的末尾汇总不能替代这些核心主张的精确出处。来源表 L17/L18 同样仍只写“PDF＋双页码”，没有 URL。
2. 来源表 L13/L20 未跟正文同步：NCCL 诊断仅串节名，nccl-tests README/PERFORMANCE 与 cann-hccl README 仍无固定文件链接/定位。正文已取得并接受的链接可以直接复用。
3. 来源记录 L3/L16 的审阅报告、RCCL 记录仍是代码格式文件名；L26 仍写“作者仅存活/长度头校验”，没有区分历史首轮与本轮全文提取，与正文角色说明未同步。

本轮修订映射 C15 又列 PR/Stateful/游标/NPU、CHANGELOG/RegisterTests/dataloader/state_dict_loader 等 T03-05/T04-01 的旧关闭对象；它们不能替代当前 T03-06 的 PDF、固定 README 和取证角色清单。正文 verification 中的 CANN 0106/0083/0086/0091 也应按实际任务范围归位或说明其旁查身份，不作为本页能力表已核对的依据。本轮不重开已通过的 T03-05/T04-01。

剩余关闭条件：在上述 HCCL 核心单元/映射段近旁添加两份 PDF 链接和相应页码，来源表同步 PDF URL；把正文已有 NCCL 诊断、固定 README/PERFORMANCE/cann-hccl 链接复制到对应映射行并补实际定位；把真实审阅/研究文件名改为普通 Markdown 链接，L26 明记“首轮作者 HEAD／本轮作者全文提取／审阅方独立核验”的轮次与角色。修订映射只列本页实际完成项；保留已接受的入口异常与 BLOCKED-1。无需重复修改其他条目或新增登记。

## 状态与后续

| 状态 | ID |
|---|---|
| T03-06 CLOSED（4） | C10、C12、C13、C14 |
| T03-06 OPEN（2，原 P2） | C11、C15 |
| 本批累计 CLOSED（13） | C01–C10、C12–C14 |
| 证据阻塞（单列） | BLOCKED-1，blocked_on_evidence/open |

T03-06 尚未通过；T03-07/T03-08 按原前置继续等待。BLOCKED-1 不因本轮局部技术修正或新增链接而关闭，不证明不存在官方配套材料；本轮只确认尚未取得目标交集。T03-05/T04-01、T02-10/C08 例外及 T02-11 草稿边界保持，正文仍 draft/source_checked，无实机验证。

本轮仅新增本报告，更新 T03-06 初审/第一次复核的最新入口和来源审计；knowledge/docs/plans/sources/src/schemas/paths 输入清单确认只有上述三份旧记录变化及本报告新增，无删除或其他源文件变更。作者正文、来源表、修订映射、索引、登记、计划和 Batch 17/18 文件保持本轮输入；build 由 make 重建。

`make check` / `make build` 均 PASS（88 篇内容 / 386 项来源），本地文件链接和当前状态入口核对完成。结构检查不证明技术正确性或版本交集；未改 src/kb，未执行 make test；无真实 GPU/NPU、MPI/collective、配置变更或故障注入。
