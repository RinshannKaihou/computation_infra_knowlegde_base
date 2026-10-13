# 第十九批 T03-07 第三次定向复核

复核日期：2026-10-13（Asia/Shanghai）。作者正文 `updated_at: 2026-10-14` 保留为输入标签，不作为实际复核日期。

**结论：C21 转 CLOSED，C17 保持 CLOSED；T03-07 六项审阅发现全部关闭，本批累计 21 CLOSED / 0 OPEN（审阅发现）。** T03-07 在本次加法与来源追溯范围通过，解除 T03-08 对 T03-07 文档审阅的等待。BLOCKED-1（HCCL Test × 目标 CANN/HDK/机型官方交集）继续单列 blocked_on_evidence/open；其他前置按原任务表维护，不据此声明整个 Batch 19 验收或启动 T03-08 写作。

按[第二次定向复核](batch-19-t03-07-codex-rerecheck.md)的四个残留点复核[作者修订映射](batch-19-review-fixes.md)。约定审阅配置为 `gpt-6.1-sol / xhigh`，执行者为当前 Codex 主会话，无子代理；实际运行元数据的可核验限制沿用初审，历史模型与作者/审阅方取证角色不追改。

## 输入身份与审阅方记录校正

| 输入 | SHA-256 |
|---|---|
| [T03-07 正文](../../knowledge/03-communication/bandwidth-baselines.md) | `8c2884b63cf7b638c1df2d7de88f5fe9d2923c0d95b025548041aea203574039` |
| [T03-07 作者来源记录](batch-19-t03-07-sources.md) | `ef9b66fbdd37e07789f909fbcd89a2a0c82674d7ced4fcad9f8dba15cc437158` |
| [修订映射](batch-19-review-fixes.md)（作者交付输入） | `0102457b6edd30e06707347ae0465132cddfec970030a17f68956d6c955d278b` |
| [第二次复核](batch-19-t03-07-codex-rerecheck.md)（更新入口前） | `237c34181f36b905f1795571a4fa96dbc2dc83ae1fe869d8406b2d86b0366509` |
| [来源审计](batch-19-source-audit.md)（更新前） | `9ccc801c274700306c625508c7550d1dfbcba74c2e9f9d119d16731214e86a76` |
| [来源登记](../../sources/registry.yaml)（386 项） | `e84c3b6eb61a83a46dbbfd371e5de4112def120131e0c374181e8e5acbf8f51f` |
| [任务计划](../../plans/full-coverage-backlog.yaml) | `121826a4d499273e7f6a00735e0a53931eef5c097bd66ab6b2425fdbc36ddfe0` |

作者修订映射最新标题仍把“第二次复核”写为 `4 CLOSED / 2 OPEN`，实际报告为 `5 CLOSED / 1 OPEN`。审阅方仅将标题中 **4→5、2→1 两个数字校正**，不改作者修订事项，不追记为作者交付时已改。校正后 SHA 为 `baa29be65d794f0700a866367de54f88cc6ebd570c18084b6733a4d1bff9512d`；逆向恢复这两个数字可精确恢复上述作者输入 SHA。C17 上轮已关闭，本轮只是核对保持一致，不重复计算新 CLOSED。

T03-06 正文/来源记录、T03-05/T04-01、登记/计划及 Batch 17/18 输入保持上轮身份。正文对当前 Git HEAD 的既有范围仍只有六个 insert 块，没有 replace/delete；本轮不修改知识正文或作者来源记录。

## 一次源与链接核对

本轮固定 README raw 重新获取 HTTP 200，SHA 为 `7b2dbdab28a619a47c8ac685704fc6a1432fc7d42ce4c87c71ab82a7b905e2cc`，与前两次复核一致。GitHub tag blob 本轮首次获取及一次重试均返回 HTTP 503（错误页 SHA `5ea81d0616df061a931781c3bd05697a347da318f9871b9ca82e04a6b2467e0f`）；失败响应不作为正文/锚点取证，也不误报为 HTTP 200。

README 锚点依据[第二次复核](batch-19-t03-07-codex-rerecheck.md)已独立获取的同地址 blob HTML：SHA `c21f1f192f7b37e49633689010a619af87b7092944ee0b852a461fe5c90a9fb0`，`currentOid=7da43026e4f2ef7600433c38c820732f7a205d22`，`user-content-arguments` 与 `user-content-grouped-broadcast-allgatherv-mode` 两个 id 均已核验。新加来源节引用与这个已核验精确地址完全一致；本轮 raw 内容未变。明确复用已取得的固定证据，不把瞬时网站可达性当成来源事实变化。

C17 的 HCCL 参数事实沿用上轮已重新取得的官方 0005；本轮正文 L193–195、工具矩阵和来源映射保持上轮已接受定义，不声称重新抓取全部 HCCL 页面。源材料仅存临时目录，没有镜像入库。

正文、作者来源记录及修订映射的本地文件链接均可解析；正文和来源记录已无 `tree/...` 目录链接。GPU Node Triage 的既有 ID 仍在 source_refs 中，未新增来源登记。

## C21 — CLOSED

| 上轮残留 | 本轮位置与判定 |
|---|---|
| 来源节 README 仍为目录 | 正文 L232 已改为 [README blob Arguments](https://github.com/ROCm/rocm-systems/blob/therock-10.1/projects/rccl-tests/README.md#user-content-arguments)，与 A1/来源表同一已核验快照地址 |
| 来源表 T03-01 裸定位 | 作者来源记录 L25 已补[互联路径正文](../../knowledge/03-communication/interconnect-paths.md)链接，Table 6 与路径命令说明保持原范围 |
| 档案与本页作者记录缺入口 | 正文 L226 已实际链接 [T03-05](../../knowledge/03-communication/rccl-runtime-and-verification.md)、[T03-06](../../knowledge/03-communication/communication-library-profiles.md)和[本页作者来源记录](batch-19-t03-07-sources.md)，目标存在，不再以他页取证记录代替正文档案 |
| 来源记录 L3 重复轮次串 | 已去重为首轮作者准备、第二轮作者核对、初审审阅方独立取证三段；初审 22 文件和 helper 核对归审阅方，不冒充作者历史取证 |

AllReduce 固定行号、新 README 锚点、source_refs、A5 的所选文档限定和前轮已接受的精确来源保持。上述四个剩余关闭条件满足，C21 CLOSED，无新增发现 ID。

## 当前状态与通过边界

| 状态 | ID / 范围 |
|---|---|
| T03-07 CLOSED（6） | C16–C21 |
| T03-07 审阅发现 OPEN（0） | 无 |
| 本批累计 CLOSED（21） | C01–C21 |
| 本批审阅发现 OPEN（0） | 无 |
| 既有验收子项 OPEN（单列） | BLOCKED-1，HCCL Test × 目标环境官方交集 |

T03-07 加法正文与来源追溯范围通过；文档范围覆盖原测量层级/工具矩阵、跨节点/rail 对照、独立计时换算和六信号记录契约，但不证明工具可在目标环境运行。T03-08 对 T03-07 的文档审阅等待解除，其他依赖、案例取证和未交付范围按原任务表维护；本轮未启动后续写作，也未改变任务计划状态。

T03-06 已交付文档/来源范围通过保持，其原 acceptance 5 仍未验收；BLOCKED-1、其他实现/现场映射 unknown、T02-10/C08 例外、T02-11 草稿边界均不因审阅发现清零而关闭。整个 Batch 19 未完成。

本轮新增本报告并更新 T03-07 三份旧报告的最新入口与来源审计；另作上述修订映射标题两个数字的审阅方校正。知识正文、作者来源记录、索引、登记、计划及 Batch 17/18 文件保持输入；无真实 GPU/NPU、MPI/collective、配置变更或故障注入，正文仍 draft/source_checked，模型审阅不建立硬件验证。


`make check` / `make build` 均 PASS（88 篇内容 / 386 项来源）。源文件清单确认仅本轮报告新增、三份旧报告入口与来源审计修改，另含上述可逆的修订映射标题两个数字校正，无删除；知识正文、作者来源记录、索引、登记、计划和 Batch 17/18 输入 SHA 不变。本地文件链接与当前状态入口核对完成；未改 src/kb，未执行 make test；无实机验证。
