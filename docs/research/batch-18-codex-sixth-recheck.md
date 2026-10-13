# 第十八批第六次定向复核

**后续进展：第八次定向复核关闭 C10，累计 16 CLOSED / 0 OPEN，Batch 18 在原定有限文档范围内通过。** 见[第八次复核](batch-18-codex-eighth-recheck.md)；正文仍 draft，基线 not_verified，无实机验证。以下为本次历史输入与判定，不作为最新状态。

复核日期：2026-10-10（Asia/Shanghai；输入身份时钟取得 2026-10-10 02:26:45 UTC）。作者第六轮修订节标注 2026-10-14，保留为作者标签；以下以修订文件 SHA-256 识别输入，不据标签推导执行日期。

**结论：C10 继续 P2 OPEN，Batch 18 仍暂不通过；累计 16 项保持 15 CLOSED / 1 OPEN，无新增发现 ID。** 本轮开关/计数归类修正已接受，剩余关闭阻碍仅为原验收要求的版本化统计字段未交齐。此前 15 项 CLOSED 保持，T03-01/T03-02/T03-04 的有限文档通过范围保留。

约定模型 / effort 为 `gpt-6.1-sol / xhigh`，本会话 Codex 主助手执行，未派发子代理；实际运行标识没有可独立核验的元数据，沿用[初审说明](batch-18-codex-review.md)。依据[路线图](../full-coverage-roadmap.md)、[T03-03 验收](../../plans/full-coverage-backlog.yaml)、[写作指南](../authoring-guide.md#7-批次审阅约定)、[归属边界](../../content-outline.md)及 [AGENTS](../../AGENTS.md)，按[第五次关闭条件](batch-18-codex-fifth-recheck.md)复核 C10 与修订影响，不扩大为实机验证。

## 输入身份与变化范围

| 输入 | SHA-256 |
|---|---|
| [RDMA 基线正文](../../knowledge/03-communication/rdma-baseline-and-congestion-triage.md) | `5deed6c1b6b66fc73a6a6b80836fb7742826f00c6a9822515f6f650b0e4432ae` |
| [基线研究记录](batch-18-rdma-baseline-sources.md) | `82bb74547bc6882cd53c14462d38566a2335059a3eb15d0d36a1353ed82e2f7f` |
| [修订映射](batch-18-review-fixes.md) | `b233f8016f532d3040241448332fab8215761ecb411cd9d5f7b13f2145d60c52` |
| [来源审计](batch-18-source-audit.md) | `1b941fde57f3ed6f7da9eef8f7b1862f751176c6fd6f6603d7cd73319823149b` |
| [来源登记](../../sources/registry.yaml) | `7a2fe1e0c2bfec458e26472156adf87077be7c9c8b53647202fe242ffea4e206`（375 项） |

互联路径、机制、集合正文及对应三份研究记录与[第五次输入](batch-18-codex-fifth-recheck.md#修订输入身份) SHA 完全一致；章索引仍为 `9102358b1e7d08455114dda724b0e3bb24ecdb06118eece19b80dc9d003989e5`。基线正文删除本轮新增的两行 dropless_rq/out_of_buffer 后，SHA 恰为第五次的 `f409bdd266148b7569aa52e4ee791ffd54185400b2baba19f097fbccf6746cd9`，因此此前 host 门禁等主体未改，不重开 C12/C14 或其他已关闭项。读取当前新增行、metadata、研究 L45、修订映射、登记及原验收要求。

## 一次源复验

从已取得的官方 HTML 读取 pageTreeSource 和 QoS 实际链接，随后只读取得精确版本树、流控页与两个不同的 QoS 页。网页工具未取得 QoS 后改用默认 TLS 校验的 curl，不运行下载内容；临时证据不入库。

| 本轮取得的精确来源 | 字节数 | SHA-256 |
|---|---:|---|
| [Flow Control](https://networking-docs.nvidia.com/mlnxofedswum/24.10-5.1.6.1lts/flow-control) | 90744 | `3f2659ad47f6f333bc24793afdb598e9a7c7aab578cdb0997f4fa3658051dc6a` |
| [该版本页面树 JSON](https://networking-docs.nvidia.com/mlnxofedswum/24.10-5.1.6.1lts/__pagetree.json) | 18674 | `89dfbf674e10c2db1575d45fdc42169ce83472ff3b459ade395446dbbc8b5615` |
| [Ethernet Quality of Service (QoS)](https://networking-docs.nvidia.com/mlnxofedswum/24.10-5.1.6.1lts/quality-of-service-qos) | 105314 | `e05972a5810c055e2f50c317ed07e0770b5d82879853cd665d6531da057d2ff3` |
| [IB QoS - Quality of Service](https://networking-docs.nvidia.com/mlnxofedswum/24.10-5.1.6.1lts/qos-quality-of-service) | 68398 | `65e00862fbe82af4c88bfa536c7b93518fcc93179dbed745a024e325bde75a2e` |

Flow Control 与第五次字节一致。页面树含 99 个页面标题，没有以 counter/statistic 命名的独立页；树同时区分上述两个 QoS 页面。Ethernet 页的 mlnx_qos/tc_wrap、优先级映射、限速等是配置/属性说明；IB 页则描述 SL/VL、SM/SA 与 QoS 策略，不能把两者混作同一个页面。两页在本轮已读正文中未交付所缺三类统计字段。

这种树检查仅支持“树中未列出相应标题的独立页”，**不证明已有章节内部没有计数器语义**：同一树的 Flow Control 已有 Priority Counters 与 out_of_buffer 的局部说明。新取证范围可以采信，缺失结论必须保持为已查材料未取得，不能推广到全部官方文档。ECN、UFM 和其他已接受字段沿用前轮范围，本轮未重新宣称全部 URL 取得或全部章节核验。

## C10 — P2，OPEN：归类已纠正，原必交字段仍缺

位置：[基线正文](../../knowledge/03-communication/rdma-baseline-and-congestion-triage.md) L30/34、99–106、145、158；[基线研究记录](batch-18-rdma-baseline-sources.md) L45。

接受本轮修正：正文 L104 将 `dropless_rq` 列为默认关闭、要求 Flow Control 启用的功能开关；L105 将 `out_of_buffer` 列为 RQ 满、FW 等待后仍未补 WQE 而发生丢包时增长的计数器。研究 L45 已同步拆分，前者非计数，后者局部丢包语义已取得；不再把二者合称开关。依据 [Flow Control 的 Dropless Receive Queue](https://networking-docs.nvidia.com/mlnxofedswum/24.10-5.1.6.1lts/flow-control)。其未核定采集路径/累计范围等继续 unknown，相关门禁无法判断的限定可以保留，不将它升级为传输重试指标。

第五次的归类修正条件至此已满足。**C10 尚不能整体关闭，因为下面三类原必交证据没有新增交付：**

| 缺口 | 当前状态 | 为什么本轮材料不能替代 |
|---|---|---|
| 实际传输重试计数 | 正文 L99 仍为未取得版本化字段 | dropless 开关和 out_of_buffer 丢包计数都不是传输重试计数。 |
| ECN 逐统计字段 | 正文 L102 仍无字段名及完整测量口径 | ECN 参数/范围声明、QoS 配置和页面树不提供统计字段语义。 |
| 诊断所需 RoCE 交换机统计字段 | applicability/verification 仍为未交齐 | NIC 局部计数和客户端 QoS 页不替代交换机版本化测量资料。 |

原 [T03-03 验收](../../plans/full-coverage-backlog.yaml)要求“按版本核对丢包、重试、CQE、ECN/PFC 等指标的单位/方向/累积范围”，source_discovery 另要求 NIC/交换机的版本化官方计数器资料。未知条件应如实记录，但不能用缺口清单或同一手册树未找到独立页来关闭未交付部分。

剩余关闭条件仍为：在一个明确选定的有限文档样板中交付上述三类实际字段的版本、入口、单位、方向及作用域；使用标记率时再给同窗同作用域分子/分母和来源支持的含义。下一步需取得包含实际计数器定义的 NIC 驱动/固件、交换机等官方版本化材料。无需再次修改已接受的开关/计数拆分、ECN 双入口、PFC 限定、host 门禁或 EP 映射；本次也没有新增普适阈值、全部硬件覆盖或实机运行要求。

## 状态与交付边界

| 状态 | ID |
|---|---|
| CLOSED（15） | C01、C02、C03、C04、C05、C06、C07、C08、C09、C11、C12、C13、C14、C15、C16 |
| OPEN（1，P2） | C10 |

T03-01/T03-02/T03-04 的有限文档通过状态保持；T03-03 与整批仍暂不通过。模型审阅、来源取证与实机验证分别记录，不改变正文 draft 或基线 not_verified。仅更新审阅报告、历史最新进展、来源审计及既有来源 notes；作者正文/研究记录/修订映射、任务/主题覆盖、Batch 17 与独立审计文件保持输入。来源仍为 375 项，无新增 ID，无实机验证。

交付核对：`make check` / `make build` 均 PASS（86 篇内容、375 项来源），catalog JSON/Markdown 已重建。八份审阅/审计文件的本地文件链接与最新状态指针核对通过；16 项状态集合完整互斥，15 CLOSED / 1 OPEN。70 个受保护文件 SHA 保持输入；375 个来源 ID 与非 notes 字段均未变，仅两个既有 notes 追加本轮核对范围。结构检查不替代技术正确性、远端语义或硬件验证。
