# 第十九批 T03-07 第二次定向复核

**最新状态（2026-10-13）：第三次定向复核 C21 CLOSED、C17 保持 CLOSED；T03-07 六项发现全部关闭，本批累计 21 CLOSED / 0 OPEN（审阅发现）。** 有限通过范围、BLOCKED-1 open 与审阅方记录校正见[第三次定向复核](batch-19-t03-07-codex-third-recheck.md)。T03-08 对 T03-07 文档审阅的等待解除，其他前置按原计划维护；整个 Batch 19 未验收。以下保留本报告当轮证据与状态，不以历史结论覆盖最新判定。

复核日期：2026-10-13（Asia/Shanghai）。作者正文 `updated_at: 2026-10-14` 保留为输入标签，不作为本轮实际日期。

**结论：C17 转 CLOSED；C21 仍 OPEN。** T03-07 为 5 CLOSED / 1 OPEN，本批累计 20 CLOSED / 1 OPEN，无新增发现 ID。BLOCKED-1（HCCL Test × 目标 CANN/HDK/机型官方交集）继续单列 blocked_on_evidence/open。T03-07 尚未通过，T03-08 继续等待；T03-06 的有限文档/来源通过保持，整个 Batch 19 未验收。

按[第一次定向复核](batch-19-t03-07-codex-recheck.md)剩余关闭条件核对[作者修订映射](batch-19-review-fixes.md)。约定配置为 `gpt-6.1-sol / xhigh`，执行者为当前 Codex 主会话，无子代理；实际运行元数据的可核验限制沿用初审。历史模型、作者/审阅方取证角色不追改。本轮只写审阅记录，不代作者修改正文或取证记录。

## 输入身份与范围

| 输入 | SHA-256 |
|---|---|
| [T03-07 正文](../../knowledge/03-communication/bandwidth-baselines.md) | `8f192436233881571e5114938bdd28082160caa3e5dc6acf39535cabc5241355` |
| [T03-07 来源记录](batch-19-t03-07-sources.md) | `284cb07783d311d411f1f9ab8eba7954ca942e648004df6881827eec03303d27` |
| [修订映射](batch-19-review-fixes.md) | `bc59bc56ddfed32f9730256b3e515f2538ebd7afb6724e20df13598022a51852` |
| [初审](batch-19-t03-07-codex-review.md)（更新入口前） | `24c4e0e583b849758aa0152a1018851c0f6ae1a58b51b5d8fe5049f98ab42c19` |
| [第一次复核](batch-19-t03-07-codex-recheck.md)（更新入口前） | `376961aac7bc6af27418a02abe30b176ef5d7e9e868391ae15d7f541c88d9d58` |
| [来源审计](batch-19-source-audit.md)（更新前） | `5f78991fa77d18a05f8414db1ad85c2b47db8a9c11cff6cba2279a6fb56ddedd` |
| [来源登记](../../sources/registry.yaml)（386 项） | `e84c3b6eb61a83a46dbbfd371e5de4112def120131e0c374181e8e5acbf8f51f` |
| [任务计划](../../plans/full-coverage-backlog.yaml) | `121826a4d499273e7f6a00735e0a53931eef5c097bd66ab6b2425fdbc36ddfe0` |

T03-05/T04-01、T03-06 正文/来源记录、登记/计划及 Batch 17 输入与上轮一致。对当前 Git HEAD 既有正文的比较仍只有六个 insert 块，没有 replace/delete；本轮不重审已关闭的 C16/C18/C19/C20 技术范围。

## 一次源与链接复验

重新获取四个精确官方地址，全部 HTTP 200：HCCL 0005 参数页、固定 AllReduce raw、固定 README raw，以及 README tag blob HTML。前三个原字节 SHA 与初审/第一次复核一致；HTML 的 `currentOid` 为 `7da43026e4f2ef7600433c38c820732f7a205d22`，与原文件身份相同。

| 原文件 | SHA-256 |
|---|---|
| AllReduce raw | `46af4db07ef2a676b9cbfd01c6ef39e0534432d700cf60f53b96177e0d65f67c` |
| README raw | `7b2dbdab28a619a47c8ac685704fc6a1432fc7d42ce4c87c71ab82a7b905e2cc` |
| README blob HTML（本轮观察） | `c21f1f192f7b37e49633689010a619af87b7092944ee0b852a461fe5c90a9fb0` |
| HCCL 0005 HTML | `85dfdd58f53d37d5428d0559a057228526d5ccbee233a095887c12aacc8006fe` |

独立读取 AllReduce 原文件 L78–84、README 参数/分组广播节和 HCCL MPI/工具参数表；README blob 实际含 `id="user-content-arguments"` 与 `id="user-content-grouped-broadcast-allgatherv-mode"`，本轮新锚点有效。web 阅读器未取得 GitHub blob 正文时，审阅者改为只读获取其完整 HTML 核验，没有把阅读器错误判成页面 404。

正文和作者来源记录的本地文件链接均可解析。已加入的 GPU Node Triage ID 存在于既有登记，正文 source_refs 已包含该 ID。原文/HTML 仅存临时目录，不镜像入库；HCCL 静态页仍不证明目标工具包/环境交集。

## C17 — CLOSED

正文 L193–195 已消除“工具 `-n`＝总 NPU 数”的错误归属：launcher `mpirun -n <number>`、单节点工具 `-p <npus>`、工具迭代参数 `-n <iters_count>` 分开说明。来源映射 L19 与工具表不再给出相反定义；没有把 MPI 进程数与 `-p` 再相乘为总规模的公式。

与[官方 0005 命令格式及参数三表](https://www.hiascend.com/doc_center/source/zh/CANNCommunityEdition/910/devaids/hccltool/HCCLpertest_16_0005.html)一致：该指南的启动规模位于 MPI 参数表，工具 `-p` 是单节点参与 NPU 数，工具 `-n` 是迭代次数。上轮已接受的计时/校验/设备例外、示例超时建议及实现 unknown 保持，C17 剩余条件满足。

## C21 — OPEN（仅余来源节和导航/记录同步）

本轮已满足的部分：

- 正文 L86 和来源记录 L12 的 AllReduce 链接已变为[固定 blob L78–84](https://github.com/ROCm/rocm-systems/blob/7da43026e4f2ef7600433c38c820732f7a205d22/projects/rccl-tests/src/all_reduce.cu#L78-L84)，原文件坐标与公式一致。
- A1 默认参数 L89、记录 L17 的 README 已指向有效[Arguments 锚点](https://github.com/ROCm/rocm-systems/blob/therock-10.1/projects/rccl-tests/README.md#user-content-arguments)，grouped-broadcast 新锚点同样有效。
- GPU Node Triage ID 已进入正文 source_refs；A5 的 HCCL 分布描述已限定为所选文档未定义，与工具表一致。
- 主机路径行已补 T03-01 正文入口、RCCL/T03-06 的来源记录链接；这些已补链接可解析，保持接受。

但上轮要求尚未全页同步，剩余均属于原 C21：

1. **正文 L232 的“rccl-tests README 参数节”仍指向 `tree/therock-10.1/projects/rccl-tests` 目录**。A1 与研究记录改对了，来源范围节的同名引用未改；用上述已核验的 README blob/Arguments 地址替换这一处即可，不需重新换锚点。
2. **作者来源记录 L25 的 T03-01 行仍只有 “Table 6” 与命令名，没有实际链接**。补到[互联路径正文](../../knowledge/03-communication/interconnect-paths.md)的入口，使记录与正文 L226 对应。
3. **正文 L226 的 “T03-05/T03-06 档案”仍是裸任务号；本页作者来源记录没有实际入口**。现有两个链接指向 RCCL/T03-06 取证记录，不能代替[受引用的 RCCL 档案](../../knowledge/03-communication/rccl-runtime-and-verification.md)、[三库档案](../../knowledge/03-communication/communication-library-profiles.md)及[本页作者来源映射](batch-19-t03-07-sources.md)。补普通 Markdown 链接即可，不要求复制正文或添加新内容。

来源记录 L3 还把“本轮”作者核对清单与审阅方说明串接后重复一遍。现有作者/审阅方角色标注保留，但该行应整理为各轮与执行者各一段，避免把重复串当成另一轮取证；这属于 C21 原轮次/角色同步要求，不新增发现，也不以本轮新证据追记作者历史核对。

下一轮只需补上述漏改位置与清理重复轮次串；AllReduce 公式/行号、新 README 锚点、source_refs 和 A5 已接受，不需重复推翻。C21 未完全满足原关闭条件，保持 OPEN。

## 状态与后续范围

| 状态 | ID / 范围 |
|---|---|
| T03-07 CLOSED（5） | C16–C20 |
| T03-07 OPEN（1） | C21 |
| 本批累计 CLOSED（20） | C01–C20 |
| 本批审阅发现 OPEN（1） | C21 |
| 验收子项 OPEN（单列） | BLOCKED-1 |

T03-07 尚未通过，T03-08 继续等待；T03-06 有限文档/来源通过与其原 acceptance 5 open 边界保持，整个 Batch 19 未完成。其他条目通过范围、T02-10/C08 例外、T02-11 草稿边界不变。

本轮仅新增本报告并更新 T03-07 两份旧报告的最新入口与来源审计；不修改作者正文/来源记录/修订映射、索引、登记、计划或 Batch 17/18 文件。无真实 GPU/NPU、MPI/collective、配置变更或故障注入；模型审阅不建立硬件验证。


`make check` / `make build` 均 PASS（88 篇内容 / 386 项来源）。源文件清单核对仅本轮报告新增、两份旧报告最新入口和来源审计修改，无删除；作者正文/来源记录/修订映射、索引、登记、计划和 Batch 17/18 输入 SHA 不变。本地文件链接核对完成；未改 src/kb，未执行 make test；无实机验证。
