# 第十九批来源与交付记录

**审阅状态（2026-10-13）：T03-08 加法初审完成，新增 6 项 P2（B19-C22–C27），全部 OPEN；本批累计 21 CLOSED / 6 OPEN（审阅发现）。** 证据与关闭条件见[T03-08 加法初审](batch-19-t03-08-codex-review.md)。T03-06/T03-07 当前输入与各自通过报告一致，有限文档/来源通过保持，见[T03-06 第三次复核](batch-19-t03-06-codex-third-recheck.md)、[T03-07 第三次复核](batch-19-t03-07-codex-third-recheck.md)；不因用户待审队列重复列出而丢失已完成闭环。T03-05/T04-01 通过范围保持。HCCL Test 配套 BLOCKED-1 继续单列 blocked_on_evidence/open，T03-06 全项未验收。T03-08 需修订并定向复核，整个 Batch 19 未完成；历史报告保留各轮当时状态。作者文件和新增登记中的 2026-10-14 保留为交付标签，不作为实际审阅日期。

## 本批已交付正文

| 任务 | 正文 | 类型 | 备注 |
|---|---|---|---|
| T03-05 | [RCCL 运行条件、观测与最小验证档案](../../knowledge/03-communication/rccl-runtime-and-verification.md) | reference | 新增（RCCL 2.30.7 独立样板 + PR #9745 案例 + 两节点设计；第三次复核后通过） |
| T03-06 | [三套通信库能力与版本条件档案](../../knowledge/03-communication/communication-library-profiles.md) | reference | 新增（已交付文档/来源范围通过，六项审阅发现全部 CLOSED；HCCL Test 交集仍 blocked，非任务全项验收） |
| T03-07 | [通信带宽与性能基线口径](../../knowledge/03-communication/bandwidth-baselines.md) | reference | 修订（六个加法块，既有正文未改写；第三次定向复核六项全部 CLOSED，有限文档/来源范围通过） |
| T03-08 | [通信带宽退化诊断指南](../../knowledge/03-communication/bandwidth-degradation-triage.md) | procedure | 修订（G1–G5 加法；初审 6 项 P2 OPEN，未执行实验） |
| T04-01 | [训练数据供给路径与等待](../../knowledge/04-data-storage/training-data-path.md) | concept | 修订（加法 §A/§B/§C + NPU 分列 + 一处标注替换；C08 联动 unknown） |

T03-05 的有限文档范围已通过，T03-06/T03-07 的六项文档/加法修订各自复核关闭；本轮按请求审阅已交付的 T03-08，新增六项待修订。HCCL Test 目标环境交集仍为必交 open 子项，T03-06 不能据此标为全项完成。T03-07 有限通过与其他前置边界保持；审阅方未启动写作、改变任务计划或验收未交付范围。

来源记录：[RCCL](batch-19-rccl-sources.md)、[T03-06](batch-19-t03-06-sources.md)、[T03-07](batch-19-t03-07-sources.md)、[T03-08](batch-19-t03-08-sources.md)、[T04-01](batch-19-t04-01-sources.md)。任务清单：[plans/full-coverage-backlog.yaml](../../plans/full-coverage-backlog.yaml)。

## 来源变化

本批最初新增 5 项登记（381→386）：rocm-systems-therock-10.1、rocm-systems-pr-9745、sampler-source-v2.6.0、distributed-sampler-source-v2.6.0、stateful-dataloader-0.11.0。T03-08 再追加 nccl-issue-2409 / nccl-issue-814 两项（386→388）；本批累计新增 7 项，去掉这两个末尾 Issue 登记可精确恢复上轮登记字节 SHA。

## 集成者核对

- 候选 URL 全部 HTTP 200 复核（sampler/distributed 原 commit 猜测 404，已改 tag 引用并复核 200；RCCL docs-10.1.0 别名 5 页复核 200）。
- T04-01 修订只做加法 + L122 一处明确标注替换（旧"没有选定资料"句删除， caution 句保留）；既有契约表述未动。
- T04-01 精度前提联动 T02-10 例外清单（C08），正文 verification/§C 两处指向。

## 初审记录（2026-10-10）

审阅执行角色、约定模型与实际运行元数据限制、输入 SHA-256、独立取证范围及逐项关闭条件见[初审报告](batch-19-codex-review.md)。发现涵盖 RCCL group/non-blocking/Abort 前提、time 微秒与文档毫秒冲突、校验默认值、单节点/跨节点性能与路径判据、日志变量名，以及数据身份/对照设计、StatefulDataLoader 默认状态、NPU 分支和精确来源定位。9 项均 OPEN，尚无修订后复核。

原集成者 HTTP 200 检查保留为历史可达性记录，不作为主张已成立的证据。本轮部分 CANN 普通 URL 返回站点壳，审阅者取得同版本官方静态正文；不把新取证冒充作者当时已取得。未改动知识正文、研究记录、登记或任务完成状态；无实机验证。`make check` / `make build` 均 PASS（87 篇内容 / 386 项来源）。

## 第一次定向复核（2026-10-12）

[首轮修订映射](batch-19-review-fixes.md)已交付，由本会话审阅者按原关闭条件复核。C02 的微秒口径、C04 的有限路径/基线/等待设计、C07 的状态来源转 CLOSED。六项仍 OPEN：非阻塞创建 API 与条件分支、最终校验参数/计划行、B-hang 初始化日志、缓存阶段/数据顺序预期、NPU 错误分支/等待方向/完成状态、正文近旁链接和余下映射。逐项位置、一次源证据及下一轮关闭条件见[复核报告](batch-19-codex-recheck.md)，无新增发现 ID。

来源登记仍 386 项，无新增来源。复核者只更新审阅记录与本审计，不修改作者正文、研究记录、修订映射、索引或任务状态；T03-06 继续等待 T03-05 复核通过。`make check` / `make build` 均 PASS（87 篇内容 / 386 项来源），没有实机验证。

## 第二次定向复核（2026-10-12）

第二轮修订经[第二次复核](batch-19-codex-rerecheck.md)判定：C01/C05/C06/C08 转 CLOSED，累计 7 CLOSED / 2 OPEN，无新增 ID。T04-01 的来源同步和有限内容范围通过。T03-05 仅剩：C03 的 `-O both` 被整数解析为 0、只启用 in-place，需省略该选项使用默认双 placement 或分开 0/1；C09 的 timer 链接缺 `src/`，blob/raw 均 HTTP 404，正确固定文件已 HTTP 200 核对。

登记无变化（386 项），`make check` / `make build` 均 PASS（87 篇内容 / 386 项来源）。本轮不改作者正文/取证/修订映射或任务状态，不启动 T03-06；无实机验证。T04-01 通过不升级 T02-11 前置或 T02-10/C08 例外范围，整个 Batch 19 尚未验收。

## 第三次定向复核（2026-10-12）

第三轮两处修正经[第三次复核](batch-19-codex-third-recheck.md)均 CLOSED：设计与最终命令省略 `-O`，默认双 placement 与固定源码/README 一致；timer 精确 blob/raw 地址均 HTTP 200，原文与固定 commit 一致。累计 9 CLOSED / 0 OPEN，T03-05/T04-01 在原定有限内容/来源范围通过，无新增发现或来源 ID。

`make check` / `make build` 均 PASS（87 篇内容 / 386 项来源）；作者正文、研究记录、修订映射、索引、登记和任务计划未由复核者修改。T03-06 对 T03-05 的审阅等待解除，其他前置与未交付子项按原任务表维护；T03-06/T03-07/T03-08 本轮未审阅。正文仍 draft/source_checked，unknown 和前置例外保留，无实机验证，不声明整个 Batch 19 完成。

## T03-06 补充初审（2026-10-12）

新增正文经[补充初审](batch-19-t03-06-codex-review.md)判定需要修订：6 项 P2（B19-C10–C15）均 OPEN，涵盖 NCCL 完整返回码计数、库层/框架层并发次序条件、HCCL 已知 P2P/错误查询、初始化与 rank/device 接口契约、待填框架后端行，以及精确来源定位和作者/审阅方核对范围。原 C01–C09 保持 CLOSED；HCCL Test × 目标 CANN/HDK/机型交集延续 BLOCKED-1，不因局部文档事实已取证而关闭。

审阅方只读获取 21 个精确地址，读取两份 HCCL PDF 正文并核对相关页、NCCL/PyTorch 页节、固定 README 和 HCCL Test 官方 910 静态页。Test 普通入口虽 HTTP 200，但 title 与请求主题不符；静态页支持局部字段，不证明精确发行配套。精确地址、PDF 双页码、输入与关键原文件 SHA、适用范围见报告；新取证不冒充作者此前已完成。RCCL 双向链接已接通，T03-05/T04-01 的有限通过范围保持。

本轮仅新增审阅报告并更新本审计，来源登记仍 386 项，作者正文、来源研究记录、修订映射、索引、计划和 Batch 17/18 文件均受写入保护；无实机验证。`make check` / `make build` 均 PASS（88 篇内容 / 386 项来源），源文件清单核对只有本审计修改和新报告新增。T03-06 未通过，T03-07/T03-08 继续按原前置等待，不声明整批完成。

## T03-06 第一次定向复核（2026-10-12）

[六项修订映射](batch-19-review-fixes.md)经[定向复核](batch-19-t03-06-codex-recheck.md)判定：C10 的八值计数与来源摘要差异 CLOSED；C11–C15 仍 OPEN，无新增发现 ID。剩余为具体组创建/执行条件和独立导航、Python 物理 ID 条件不能外推 C++、local rank 编号/数量及查询/单卡约束、HIP 2.6 来源元数据、仍残留的 M13 和精确 PDF/固定文件链接等。新功能说明已修正的部分在复核报告逐项保留，不要求重新推翻。

八个精确官方地址重抓 HTTP 200；两份 HCCL PDF 全文提取并核对相关页，SHA 与补充初审相同。PyTorch 两个 HTML 原字节有变化，但归一化可见文本相同。原始证据仍只存临时目录；新取证不冒充作者历史核对，亦不关闭 Test 配套 BLOCKED-1。

累计 10 CLOSED / 5 OPEN，BLOCKED-1 单列；T03-06 未通过，T03-07/T03-08 等待保持。T03-05/T04-01、登记/计划及 Batch 17/18 输入未变，无实机验证。本轮只新增复核报告、更新 T03-06 初审最新入口和本审计；`make check` / `make build` 均 PASS（88 篇内容 / 386 项来源），源文件清单确认仅上述记录变更，其余受保护输入不变。

## T03-06 第二次定向复核（2026-10-12）

第二轮修订经[第二次定向复核](batch-19-t03-06-codex-rerecheck.md)判定：C12/C13/C14 CLOSED，C10 保持 CLOSED；本条目 4 CLOSED / 2 OPEN，本批累计 13 CLOSED / 2 OPEN，无新增 ID。C11 仍需恢复默认关闭时的显式总序说明并补实际案例/实验导航；C15 仍需把已添加的正文链接同步到来源表及 HCCL 主张近旁，补实际研究文件链接、统一作者核对轮次。报告保留已接受的接口/映射/元数据修正，剩余要求不指向已通过的 T03-05/T04-01。

11 个精确地址重抓 HTTP 200，两份 PDF 全文提取及相关原页核对，SHA 与初审相同；NCCL 三页原字节相同，PyTorch 可见文本相同。troubleshooting 四个锚点存在，固定 README/PERFORMANCE 可达，cann-hccl 短 SHA raw 与已登记完整 commit 字节一致。临时证据未镜像入库，无新增登记，也未取得 HCCL Test 配套交集。

BLOCKED-1 继续单列 open，T03-06 尚未通过，T03-07/T03-08 等待保持。审阅者只新增复核报告并更新两份旧报告的最新入口及本审计；作者正文、来源记录、修订映射、索引、登记、计划及 Batch 17/18 输入受保护，无实机验证。`make check` / `make build` 均 PASS（88 篇内容 / 386 项来源），输入清单确认只有上述审阅记录变更，当前状态入口一致。

## T03-06 第三次定向复核（2026-10-12）

第三轮两项修订经[第三次定向复核](batch-19-t03-06-codex-third-recheck.md)均 CLOSED：默认关闭分支与六个实际指南/案例/实验链接已补齐；近旁 PDF、来源表的精确诊断/固定文件/研究记录链接及角色轮次同步成立。T03-06 六项审阅发现全部关闭，本批累计 15 CLOSED / 0 OPEN，无新增 ID。

作者来源记录末尾仍有未限定首轮的 HEAD 旧尾句，审阅方仅插入“首轮”两个字，与作者已明确的本轮全文提取记录一致；这一校正及输入/输出 SHA 已在报告明记，不冒充作者交付时已改。知识正文与修订映射保持输入。四个精确官方地址重抓 HTTP 200，PDF/NCCL 原文件 SHA 与初审相同；物理页入口按相应连续小节核对，本地导航均存在。临时原文/页图未镜像入库，无新增登记。

T03-06 在已交付文档/来源范围内通过，BLOCKED-1（目标 CANN/HDK/机型 × HCCL Test 官方交集）继续 blocked_on_evidence/open，原 acceptance 5 未验收；T03-07/T03-08 不自动解锁，整个 Batch 19 未完成。T03-05/T04-01、Batch 17/18、登记及计划边界保持，无实机验证。本轮仅写审阅报告/入口/本审计，另作上述来源记录文字校正；`make check` / `make build` 均 PASS（88 篇内容 / 386 项来源），输入清单确认无其他源文件变更，审阅发现的当前状态入口一致。


## T03-07 加法初审（2026-10-12）

六个加法块经[初审](batch-19-t03-07-codex-review.md)判定需要修订：新增 6 项 P2（B19-C16–C21）全部 OPEN，涵盖 RCCL 模式/计时/页脚条件、HCCL launcher 与工具参数及已知计时/校验契约、rail 与 SU/实际路径条件及四类对照判据、各工具参数归属、完成率/恢复统计定义，以及精确来源映射。既有正文对当前 Git HEAD 只有 insert，无 replace/delete；本轮未重审未修改的旧口径，未修改作者正文或取证记录。

审阅方独立获取 22 个精确文件/页面，全部 HTTP 200，并读取相关函数/参数/路径正文。AllGather helper 的固定源码换算、Broadcast grouped 分支、设备实现的 CPU 显示抑制、页脚环境比较方向、HCCL 参数同名与已知计时条件、CROSS_NIC 例外/SU 限定均有具体定位。GPU Node Triage 正确 URL 已有登记且本轮正文核对成立，无需新增来源。原始证据只存临时目录；审阅方新取证不冒充作者当时核对，HCCL Test 静态页仍不证明目标环境配套。

T03-06 当前正文和来源记录与第三次定向复核身份一致，有限文档/来源范围通过保持，BLOCKED-1 继续单列 blocked_on_evidence/open；C01–C15 保持 CLOSED，本批累计 15 CLOSED / 6 OPEN。T03-07 未通过，修订后需定向复核；T03-08 继续等待，整个 Batch 19 未完成。T03-05/T04-01、Batch 17/18、来源登记（386 项）和计划状态保持本轮输入；没有实机验证。

2026-10-13 完成最终校验与交付：`make check` / `make build` 均 PASS（88 篇内容 / 386 项来源）；源文件清单只见本审计修改及 T03-07 初审报告新增，无删除，所有作者/其他批/登记/计划输入 SHA 不变。本地链接与报告三个官方页节锚点核对完成；未改 src/kb，未执行 make test。


## T03-07 第一次定向复核（2026-10-13）

作者六项修订经[定向复核](batch-19-t03-07-codex-recheck.md)判定：C16/C18/C19/C20 转 CLOSED，C17/C21 仍 OPEN，无新增发现 ID。本条目 4 CLOSED / 2 OPEN，本批累计 19 CLOSED / 2 OPEN。RCCL 模式/计时/页脚方向、rail/SU 边界与四类候选判据、逐工具参数归属、完成率与错误项零增量恢复限定已接受；C17 仅余跨节点段误将总 NPU 数归给工具 `-n`，C21 余 AllReduce/README 目录链接、GPU Node Triage source_refs 缺项及档案/作者记录入口等同步残余。已正确的 HCCL 计时/校验契约和精确页节链接保持接受。

审阅者重抓 18 个精确官方文件/页面，全部 HTTP 200、原字节 SHA 与初审对应文件一致，并读取相关函数/参数/路径正文。CROSS_NIC、compute fabric、Network Testing 三个 HTML id 实测存在，当前本地文件链接均可解析；目录可达不等于精确主张定位。临时证据未镜像入库，新审阅取证不冒充作者历史核对。没有新增登记或 HCCL Test 目标配套交集证据。

T03-06 身份与已通过的第三次定向复核一致，有限文档/来源通过保持；BLOCKED-1 继续 blocked_on_evidence/open。T03-07 尚未通过，下一轮只复核 C17/C21 剩余条件和必要联动，T03-08 继续等待，整个 Batch 19 未完成。审阅方只写本轮报告/初审最新入口/本审计，不改作者正文、来源记录、修订映射、登记、索引、计划或其他批文件；无实机验证。


`make check` / `make build` 均 PASS（88 篇内容 / 386 项来源）。源文件输入清单确认仅本轮复核报告新增、加法初审最新入口与来源审计修改，无删除；作者正文/来源记录/修订映射、索引、登记、计划和 Batch 17/18 输入 SHA 不变。本地文件链接核对完成；未改 src/kb，未执行 make test；无实机验证。


## T03-07 第二次定向复核（2026-10-13）

第二轮两项修订经[定向复核](batch-19-t03-07-codex-rerecheck.md)判定：C17 转 CLOSED，C21 仍 OPEN，无新增发现 ID。T03-07 为 5 CLOSED / 1 OPEN，本批累计 20 CLOSED / 1 OPEN。HCCL 参数归属冲突已消除；AllReduce 固定行号、README 参数/分组广播新锚点、GPU Node Triage source_refs、A5 分布限定及部分导航已接受。C21 仅余来源范围节的 README 目录链接、来源表 T03-01 裸定位、T03-05/06 正文与本页作者记录入口，以及 L3 重复轮次串；具体漏改位置与关闭条件见报告，不要求重复改动已正确的内容。

四个精确官方地址重新获取 HTTP 200，AllReduce/README raw 与 HCCL 0005 原字节 SHA 同上轮；README blob HTML 的 currentOid 与固定 commit 一致，user-content-arguments / user-content-grouped-broadcast-allgatherv-mode 两个 id 实测存在。本地文件链接可解析，三项导航漏项是尚未添加，非新加链接失效；原始证据只存临时目录，无新增登记或 HCCL 目标配套证据。

T03-07 尚未通过，T03-08 等待保持；BLOCKED-1 单列 blocked_on_evidence/open，T03-06 有限通过和全项验收边界、T03-05/T04-01、Batch 17/18、登记和计划保持本轮输入。审阅者仅写本轮报告、两份旧报告最新入口和本审计，不改作者正文、来源记录或修订映射；无实机验证。


`make check` / `make build` 均 PASS（88 篇内容 / 386 项来源）。源文件清单核对仅本轮报告新增、两份旧报告最新入口和来源审计修改，无删除；作者正文/来源记录/修订映射、索引、登记、计划和 Batch 17/18 输入 SHA 不变。本地文件链接核对完成；未改 src/kb，未执行 make test；无实机验证。


## T03-07 第三次定向复核（2026-10-13）

第三轮四个残留点经[定向复核](batch-19-t03-07-codex-third-recheck.md)全部满足：来源节 README 已为精确 blob/Arguments 地址；来源表 T03-01 链接、主机路径行 T03-05/T03-06 正文及本页作者来源记录入口均已补；L3 轮次说明已去重并保留角色。C21 CLOSED，C17 保持 CLOSED，T03-07 六项发现全部关闭，本批累计 21 CLOSED / 0 OPEN，无新增 ID。修订映射最新标题误写上轮 4/2，审阅方仅校正为实际 5/1 两个数字；输入/输出 SHA 与可逆恢复在报告记录，不冒充作者修改。

固定 README raw 重新获取 HTTP 200，字节 SHA 与上轮一致；GitHub blob 首次与一次重试均返回 503，失败页不作为取证。精确锚点复用第二次复核同地址、同 commit 的已取得 HTML，来源节本次改为该已核验地址；不误报本轮 blob 成功。正文/来源记录已无目录链接，本地文件链接均可解析，原始证据仍只存临时目录，无新增来源登记。

T03-07 在本次加法/来源范围通过，解除 T03-08 对其文档审阅的等待，其他前置按原计划维护；未启动 T03-08 写作。BLOCKED-1 继续 blocked_on_evidence/open，T03-06 原 acceptance 5 未验收，整个 Batch 19 未完成。正文仍 draft/source_checked，无实机验证；T03-05/T04-01、登记、计划和 Batch 17/18 输入保持。


`make check` / `make build` 均 PASS（88 篇内容 / 386 项来源）。源文件清单确认仅本轮报告新增、三份旧报告入口与来源审计修改，另含上述可逆的修订映射标题两个数字校正，无删除；知识正文、作者来源记录、索引、登记、计划和 Batch 17/18 输入 SHA 不变。本地文件链接与当前状态入口核对完成；未改 src/kb，未执行 make test；无实机验证。


## T03-08 加法初审（2026-10-13）

G1–G5 经[初审](batch-19-t03-08-codex-review.md)判定需要修订：6 项 P2（B19-C22–C27）全部 OPEN，涵盖时间窗对齐/跨节点降级契约、配置与物理错误及共享干扰/消息支路分类、对照设计入口/路径变量/失败停止/原值恢复、#2409 反证与归因阶段、#814 不支持的机制/参数归属，以及悬空代号/作者记录/工具来源和字段契约与实测数值的区别。四个 insert 块证明既有正文未改写，不要求重审未修改的旧步骤；修订可在新增范围完成。

GitHub 连接器取得两个 Issue 的完整 body 与全部评论（4/6 条），与官方网页对照读取；#2409 后续修正及关闭、#814 维护者解释与较晚适用性说明均有精确评论 URL。三个固定文档 HTML 重抓 HTTP 200（NCCL env/troubleshooting、RCCL troubleshooting）；规范化连接器证据与 HTML 原字节 SHA 分开记录。外部全文只存临时目录，不镜像入库，新审阅取证不冒充作者历史核对。

T03-06/T03-07 当前正文及相关输入与已通过报告一致，C01–C21 保持 CLOSED；BLOCKED-1 继续单列 open，T03-06 原 acceptance 5 未验收。新登记确为末尾追加两项，来源总数 388；T03-08 初审未通过，整个 Batch 19 未完成。本轮只新增报告、更新本审计，不改作者正文、来源记录、修订映射、索引、登记、计划或 Batch 17/18 文件；无实机验证。


`make check` / `make build` 均 PASS（88 篇内容 / 388 项来源）。源文件输入清单确认仅本报告新增与来源审计修改，无删除；作者正文/来源记录/修订映射、索引、登记、计划、T03-06/T03-07 和 Batch 17/18 输入 SHA 不变。本地文件链接与当前状态入口核对完成；未改 src/kb，未执行 make test；无实机验证。


## T03-08 第十四次定向复核通过与 Batch 19 整批验收（2026-10-13）

第十三轮三项补记经[第十四次定向复核](batch-19-t03-08-codex-recheck-14.md)判定：C27 CLOSED，无新增发现 ID。本批 T03-08 累计 27 CLOSED / 0 OPEN，T03-08 在既有文档/来源审阅及账本同步范围内通过；C01–C26 不重开。第十三轮账本行已补三项补记及"无新增远程取证/仅复用"，第十二轮行"本轮"已去除；作者十三轮、输入既有审阅十三份（初审＋一至十二次复核）口径一致，本报告不计入输入、不产生作者第十四轮。

Batch 19 整批状态：T03-05 通过、T03-06 有限文档/来源范围通过（BLOCKED-1：HCCL Test × 目标 CANN/HDK/机型官方交集，继续 blocked_on_evidence/open；原 acceptance 5 未验收）、T03-07 通过、T03-08 通过、T04-01 通过。除 BLOCKED-1 单列 open 外，本批无其他 OPEN 发现或验收子项；整个 Batch 19 按"BLOCKED-1 长期 open 并具名跟踪"验收，其余任务视为完成。本轮只新增复核报告与本审计，不改作者正文、来源记录、修订映射、索引、登记、计划或 Batch 17/18 文件；无实机验证。


`make check` / `make build` 均 PASS（88 篇内容 / 389 项来源）。源文件输入清单确认仅本报告新增与来源审计修改，无删除；作者正文/来源记录/修订映射、索引、登记、计划和 Batch 17/18 输入 SHA 不变。本地文件链接核对完成；未改 src/kb，未执行 make test；无实机验证。


## BLOCKED-1 例外清单批准与 backlog 收尾（2026-10-13）

[Batch 19 条件验收与 BLOCKED-1 例外清单](batch-19-blocked-1-exception.md)获用户批准生效：除 BLOCKED-1（长期 open 具名跟踪）与 T03-06 acceptance 5（未验收）外，本批视为完成。backlog 最小改动已执行：T03-06 加 `acceptance_exception`、T03-07 加 `depends_on_note`；T03-07/T03-08 此前在 BLOCKED-1 open 状态下的有限通过追认为条件满足。后续任务引用 HCCL 交集一律 unknown 并指向例外清单。无实机验证。
