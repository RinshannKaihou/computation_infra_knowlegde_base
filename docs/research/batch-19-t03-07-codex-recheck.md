# 第十九批 T03-07 第一次定向复核

**最新状态（2026-10-13）：第三次定向复核 C21 CLOSED、C17 保持 CLOSED；T03-07 六项发现全部关闭，本批累计 21 CLOSED / 0 OPEN（审阅发现）。** 有限通过范围、BLOCKED-1 open 与审阅方记录校正见[第三次定向复核](batch-19-t03-07-codex-third-recheck.md)。T03-08 对 T03-07 文档审阅的等待解除，其他前置按原计划维护；整个 Batch 19 未验收。以下保留本报告当轮证据与状态，不以历史结论覆盖最新判定。

复核日期：2026-10-13（Asia/Shanghai）。作者正文 `updated_at: 2026-10-14` 保留为输入标签，不作为本轮实际日期。

**结论：C16、C18、C19、C20 转 CLOSED；C17、C21 仍 OPEN。** T03-07 为 4 CLOSED / 2 OPEN，本批累计 19 CLOSED / 2 OPEN，无新增发现 ID。BLOCKED-1（HCCL Test × 目标 CANN/HDK/机型官方交集）继续单列 blocked_on_evidence/open。T03-07 尚未通过，T03-08 继续等待；T03-06 的有限文档/来源范围通过保持，不等于任务全项或整个 Batch 19 验收。

按[加法初审](batch-19-t03-07-codex-review.md)逐项关闭条件复核[作者修订映射](batch-19-review-fixes.md)。约定审阅配置为 `gpt-6.1-sol / xhigh`；执行者为当前 Codex 主会话，无子代理。实际运行元数据的可核验限制沿用初审，不追改历史模型或作者取证角色。本轮不修改正文、作者来源记录或修订映射。

## 输入身份与保护范围

| 输入 | SHA-256 |
|---|---|
| [T03-07 正文](../../knowledge/03-communication/bandwidth-baselines.md) | `48930e3873e316f6b964ed58961bb044c612e2b30d2bdacdf5a12d13a99e6da6` |
| [T03-07 作者来源记录](batch-19-t03-07-sources.md) | `ba4c0258d70687692a5ab0dba1841fad483998172f2b993a5bebdb0e5112dbfa` |
| [修订映射](batch-19-review-fixes.md) | `f9fc49450e775ea21b3a4ec1a6c71f279c0dd9a517207318dc45906bcbabef38` |
| [加法初审](batch-19-t03-07-codex-review.md)（加最新入口前） | `eddf909997aa1a50d5f45d117b288e3ceaa90bbfac123d0b0ce96bacbe4564b6` |
| [来源审计](batch-19-source-audit.md)（本轮更新前） | `356937b504d45d2737337febe0a8aad468315393e768dd63a82886f02507ece7` |
| [来源登记](../../sources/registry.yaml)（386 项） | `e84c3b6eb61a83a46dbbfd371e5de4112def120131e0c374181e8e5acbf8f51f` |
| [任务计划](../../plans/full-coverage-backlog.yaml) | `121826a4d499273e7f6a00735e0a53931eef5c097bd66ab6b2425fdbc36ddfe0` |

T03-06 正文/来源记录 SHA 仍分别为 `d4a5fb535ba78d852e070f09ff387b69dc6e1ab7cf86620c7ee08e9a99577646` / `91ed2af03140ef259c999102347f6e4e314032407c88c7d491277db098626a81`，与其[第三次复核](batch-19-t03-06-codex-third-recheck.md)一致。登记、计划、T03-05/T04-01 和 Batch 17/18 文件保持本轮输入。

本轮正文与当前 Git HEAD 既有正文比较仍只有六个 insert 块，没有 replace/delete；修订发生在新增范围。新加法不建立硬件兼容或本地性能验证。

## 一次源复验

重新获取 18 个官方精确文件/页面，全部 HTTP 200，原字节 SHA 与初审对应文件全部一致：RCCL README/PERFORMANCE、common/util、AllReduce/Broadcast、AllGather policy/device-time host 辅助头（8）；NCCL-tests README/common 与 NCCL 2.27.5 env（3）；CANN 910 的 HCCLpertest_16_0001/0004/0005/0006/0007（5）；SuperPOD fabric 与 GPU Node Triage（2）。重新读取相关函数、参数表和路径小节，没有把存活校验代替语义核对。

固定源码坐标仍按 ROCm `7da43026e4f2ef7600433c38c820732f7a205d22` 与 NCCL-tests `b4d5beebca8a76cf01335f724d154b9b9d394d96` 的原文件行号。三个官方 HTML id `nccl-cross-nic`、`computeinfiniband-fabric`、`network-testing` 实测存在。作者正文/记录/修订映射中的本地文件链接均可解析；“目录可达”与“精确文件定位成立”分别判定。

| 关键原文件 | SHA-256 |
|---|---|
| RCCL common.cu | `1339f9535d68b748677bd817e88d02002a71ff27b7f2b7ce41fcaccaa505f9d7` |
| RCCL AllReduce | `46af4db07ef2a676b9cbfd01c6ef39e0534432d700cf60f53b96177e0d65f67c` |
| RCCL README | `7b2dbdab28a619a47c8ac685704fc6a1432fc7d42ce4c87c71ab82a7b905e2cc` |
| HCCL 参数说明 0005 | `85dfdd58f53d37d5428d0559a057228526d5ccbee233a095887c12aacc8006fe` |
| HCCL 结果说明 0006 | `ad4f33978cecba4179e2ab39cfa82bbca06cd1783d012879825c274c28479fc1` |

完整初审哈希保留在初审报告；本轮原文/提取文本只存临时目录，未镜像入库。HCCL Test 静态页仍只支持局部指南契约，不证明工具包、CANN/HDK/机型交集。T03-01/T03-03 的计数器/路径及恢复限定按已审阅正文复用，本轮未重新核验其全部远端材料。

## C16 — CLOSED

正文 L81–88 已限定默认 host 模式，普通 Broadcast 与 `RCCL_TESTS_ALLGATHERV_ENABLE=1` 的分子/系数分开；计时写明 `iters×agg_iters` 归一化、graph 缩放、rank 聚合，以及 CPU 显示条件、device-only 时间替换和 `-z 3` barrier 排除。页脚方向纠正为平均 busbw 与 `NCCL_TESTS_MIN_BW×0.9` 比较，未设环境值取 -1。固定 [Broadcast L82–93](https://github.com/ROCm/rocm-systems/blob/7da43026e4f2ef7600433c38c820732f7a205d22/projects/rccl-tests/src/broadcast.cu#L82-L93)、[common L1070–1128](https://github.com/ROCm/rocm-systems/blob/7da43026e4f2ef7600433c38c820732f7a205d22/projects/rccl-tests/src/common.cu#L1070-L1128)、[显示 L1259–1266](https://github.com/ROCm/rocm-systems/blob/7da43026e4f2ef7600433c38c820732f7a205d22/projects/rccl-tests/src/common.cu#L1259-L1266)、[页脚 L2757–2788](https://github.com/ROCm/rocm-systems/blob/7da43026e4f2ef7600433c38c820732f7a205d22/projects/rccl-tests/src/common.cu#L2757-L2788)支持这些修正。

AllGather 系数引用固定 helper，并明确初审审阅方取证角色；余算子未逐一回查保持诚实边界。us/ms 冲突仍在来源范围 L231 及记录 L11 单列。C16 技术条件满足；AllReduce/README 目录链接的残余由原 C21 继续追踪，不重复计数。

## C17 — OPEN（仅剩跨节点段的 `-n` 错归属）

已接受正文 L192/L194 的修正：launcher 与 executable 两处参数角色已解释；`-t` 的默认/排除项与三条件已列出；校验三值、NULL 两类未校验分支及 success 准入已说明；`-p` 常规选择与 `HCCL_TEST_USE_DEVS` 例外分开；3K/5K 为指南示例建议。计时实现未知收窄为具体计时点和 rank 归约，不再覆盖文档契约。

但 L193 仍写 **“工具 `-n`＝节点数×每节点 NPU 数（与 MPI `-n` 区分）”**，把总规模再次归给工具参数，与 L192 矛盾。[官方 0005](https://www.hiascend.com/doc_center/source/zh/CANNCommunityEdition/910/devaids/hccltool/HCCLpertest_16_0005.html)命令格式及表 1/2/3明确：`mpirun -n <number>` 是本指南启动总规模，工具 `-n <iters_count>` 是迭代次数；同页工具 `-p` 为单节点参与 NPU 数。按当前 L193 设置会改变迭代口径，不能 CLOSED。

下一轮关闭条件：仅纠正跨节点段的归属，使 `mpirun -n <number>`、工具 `-n <iters_count>`、`-p <npus>` 在本节、工具矩阵及来源映射保持一致；保留已接受的条件。无需重复推翻已正确的 `-t/-c` 等修订，也不以参数事实关闭 BLOCKED-1。

## C18 — CLOSED

正文 L145–160 已区分请求配置、实际端点/映射、IB/RoCE 路径和同窗端口遥测；补入 CROSS_NIC 成员例外、HCCL bootstrap 与设备 RDMA 路径的区别、同 SU 一跳及跨 SU 条件。对应 [CROSS_NIC 定义](https://docs.nvidia.com/deeplearning/nccl/archives/nccl_2275/user-guide/docs/env.html#nccl-cross-nic)与 [SuperPOD compute fabric](https://docs.nvidia.com/dgx-superpod/reference-architecture-scalable-infrastructure-h100/latest/network-fabrics.html#computeinfiniband-fabric)核对成立。

四类候选表已给输入、同窗/隔离背景对照与无法判断条件，区分链路重试和 validator retries，不以 busbw 或吞吐下降单独定位；T03-03 限定及 [Network Testing 方法](https://docs.nvidia.com/deploy/gpu-debug-guidelines/gpu-node-triage.html#network-testing)已有正文入口。这是文档级最小判据，不是实测归因；方法的 source_refs 追踪残余归 C21。

## C19 — CLOSED

正文 L220–225 已一工具一行，NCCL/RCCL/HCCL 的原字段、`-a` 同名异义、RCCL 本次快照的 `-A/-X/-Z`、SPLIT 范围均已分清；HCCL 表内逐次分布限定为本次所选文档未定义。perftest 门禁注明 host 后端和操作数口径，RDMA/物理/主机测量层级保留。

固定 [NCCL 参数解析 L1198–1238](https://github.com/NVIDIA/nccl-tests/blob/b4d5beebca8a76cf01335f724d154b9b9d394d96/src/common.cu#L1198-L1238)、[RCCL README Arguments](https://github.com/ROCm/rocm-systems/blob/7da43026e4f2ef7600433c38c820732f7a205d22/projects/rccl-tests/README.md#arguments)及 HCCL 0005 支持本表接口归属；不再把三个工具的选项合为共同接口。T03-01 等精确导航未补的部分集中由 C21 追踪，不把同一来源残余计作两项 OPEN。

## C20 — CLOSED

正文 L176 已定义完成数/计划尝试数，列出运行、矩阵单元、操作的记录粒度及未完成/未校验分支；进程清理不代替计划完成，缺分母/证据为 unknown。该字段是按基线计划填写的记录契约，不是本库已取得的比率；实际比较须沿用同一计划粒度和测试窗口。

恢复已记录起止事件/观察窗，将零新增限定为错误列，正常流量/流控响应按同窗基线带解释，并明确校验覆盖门禁与 RDMA 分支边界；不以进程退出或单一计数器代替 collective/应用恢复。与[T03-03 停止/恢复安排](../../knowledge/03-communication/rdma-baseline-and-congestion-triage.md#停止条件与恢复安排)的既有条件一致，C20 原错误范围已修正。

## C21 — OPEN（精确链接与依赖登记仍未完整同步）

已接受：Broadcast、计时/归一化/页脚、HCCL 精确静态页、CROSS_NIC、compute fabric 和 Network Testing 的近旁链接已加入；研究记录已成为分列映射表，GPU Node Triage URL/可变页日期已纠正，作者与初审审阅方取证角色有区分。三处页节锚点真实存在，不需再次“修正”已正确的地址。

剩余仍为初审范围内事项：

1. 正文 L85 的 AllReduceGetBw 仍指向 `tree/.../src`；来源记录 L12 仅写文件/函数名，没有精确链接或行段。应使用固定 [all_reduce.cu L78–84](https://github.com/ROCm/rocm-systems/blob/7da43026e4f2ef7600433c38c820732f7a205d22/projects/rccl-tests/src/all_reduce.cu#L78-L84)。正文 L231 的“README 参数节”仍为目录链接，来源记录 L17 亦只有普通文字；应指向本快照 README 参数节或原文件对应行段。
2. 正文已使用 GPU Node Triage 方法（L160），来源表也写了已有 ID，但 frontmatter `source_refs` L8–14 仍未列 `src.nvidia.gpu-node-triage-2026-10-08`。该 ID 已登记；只需把正文依赖同步进去，无需新增登记。
3. 主机路径行 L225、研究记录 L25 仍是 “T03-01 / Table 6” 泛称，没有到[互联路径正文](../../knowledge/03-communication/interconnect-paths.md)的实际入口；T03-05/T03-06 档案和作者来源记录入口也未补。正文目前的研究链接指向审阅报告，不能代替作者来源映射。补可解析的条目/研究记录链接即可，不要求复制已审阅原文。

下一轮关闭条件：把上述目录/裸文件定位替换成精确固定文件/页节；补已有 GPU Node Triage ID 到正文 source_refs；补 T03-01/05/06 和作者来源记录导航，并使正文/映射表/verification 对应同一范围。A5 的“ HCCL 无逐次分布”旧简写宜与工具表“所选文档未定义”的明确限定同步，避免将未取证实现写成普遍不存在；不另增发现 ID。保持已正确的链接、角色和 unknown，不追记作者历史取证。

## 当前状态与下一轮范围

| 状态 | ID / 范围 |
|---|---|
| T03-07 CLOSED（4） | C16、C18、C19、C20 |
| T03-07 OPEN（2） | C17、C21 |
| 本批累计 CLOSED（19） | C01–C16、C18–C20 |
| 本批审阅发现 OPEN（2） | C17、C21 |
| 既有验收子项 OPEN（单列） | BLOCKED-1，HCCL Test 目标环境官方交集 |

下一轮只需复核 C17/C21 的剩余条件及必要联动；已关闭的模式/判据/参数归属/恢复条件保持接受。T03-07 尚未通过，T03-08 继续等待；T03-06 原 acceptance 5 不因本轮四项 CLOSED 而验收。T03-05/T04-01、T02-10/C08 例外与 T02-11 草稿边界保持；整个 Batch 19 未完成。

本轮仅新增本报告、更新加法初审最新入口与来源审计；不改作者正文/来源记录/修订映射、索引、登记、计划或 Batch 17/18 文件。无真实 GPU/NPU、MPI/collective、配置变更或故障注入；source_checked、模型审阅及结构校验均不构成硬件验证。


`make check` / `make build` 均 PASS（88 篇内容 / 386 项来源）。源文件输入清单确认仅本轮复核报告新增、加法初审最新入口与来源审计修改，无删除；作者正文/来源记录/修订映射、索引、登记、计划和 Batch 17/18 输入 SHA 不变。本地文件链接核对完成；未改 src/kb，未执行 make test；无实机验证。
