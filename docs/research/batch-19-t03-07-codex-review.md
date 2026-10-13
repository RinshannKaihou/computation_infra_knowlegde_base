# 第十九批 T03-07 加法初审

**最新状态（2026-10-13）：第三次定向复核 C21 CLOSED、C17 保持 CLOSED；T03-07 六项发现全部关闭，本批累计 21 CLOSED / 0 OPEN（审阅发现）。** 有限通过范围、BLOCKED-1 open 与审阅方记录校正见[第三次定向复核](batch-19-t03-07-codex-third-recheck.md)。T03-08 对 T03-07 文档审阅的等待解除，其他前置按原计划维护；整个 Batch 19 未验收。以下保留本报告当轮证据与状态，不以历史结论覆盖最新判定。

审阅取证日期：2026-10-12；最终校验与交付日期：2026-10-13（Asia/Shanghai）。作者正文及研究记录中的 `2026-10-14` 保留为交付标签，不作为本轮实际取证日期。

**结论：T03-07 需要修订，新增 6 项 P2（B19-C16–C21），全部 OPEN。** 本批累计 15 CLOSED / 6 OPEN（审阅发现）；既有 BLOCKED-1（HCCL Test × 目标 CANN/HDK/机型官方交集）继续单列 blocked_on_evidence/open。T03-06 本轮输入与[第三次定向复核](batch-19-t03-06-codex-third-recheck.md)相同，其已交付文档/来源范围通过保持，任务全项仍未验收。T03-08 等待 T03-07 修订并定向复核；不声明整个 Batch 19 完成。

当前约定审阅配置为 `gpt-6.1-sol / xhigh`（用户 2026-10-08 更新）。本报告由当前 Codex 主会话执行，无子代理；工具输出不能独立证明实际运行模型/推理等级，因此区分约定配置与可核验的执行角色，不补造运行元数据。历史报告模型记录保持原样。

## 范围与输入身份

审阅 T03-07 的 A1–A6、元数据和[作者来源记录](batch-19-t03-07-sources.md)，参照原任务四项 acceptance 与已审阅的 T03-01/03/05/06 边界。未审阅尚未交付的 T03-08 / NCCL #2409 案例，也没有修改正文或代作者修订。

与当前 Git HEAD 的既有正文逐行比较，frontmatter 之外只有 **6 个 insert 块，没有 replace/delete**；既有正文 SHA 为 `b24b7922856dce0c1c5059d22b5f9c50c4a5e3437e591833efc50d1ed52a3e13`。元数据新增四个 source_refs 并改日期/核对注记。这支持“加法、既有正文未改写”的交付声明；不把旧正文重新计为本轮新发现。

| 输入 | SHA-256 |
|---|---|
| [T03-07 正文](../../knowledge/03-communication/bandwidth-baselines.md) | `15b2a48ee5114568f3bf4071832a5a0278d403fe3c9f4105a6f5b34d112de827` |
| [T03-07 作者来源记录](batch-19-t03-07-sources.md) | `c6e8af9cc1941fe412bad3870b05c553e11a3535261562041bd82b711204d0ff` |
| [T03-06 正文](../../knowledge/03-communication/communication-library-profiles.md) | `d4a5fb535ba78d852e070f09ff387b69dc6e1ab7cf86620c7ee08e9a99577646` |
| [T03-06 来源记录](batch-19-t03-06-sources.md)（含上轮审阅方“首轮”校正） | `91ed2af03140ef259c999102347f6e4e314032407c88c7d491277db098626a81` |
| [来源登记](../../sources/registry.yaml)（386 项） | `e84c3b6eb61a83a46dbbfd371e5de4112def120131e0c374181e8e5acbf8f51f` |
| [任务计划](../../plans/full-coverage-backlog.yaml) | `121826a4d499273e7f6a00735e0a53931eef5c097bd66ab6b2425fdbc36ddfe0` |
| [来源审计](batch-19-source-audit.md)（更新前） | `3854470bf82020eb8562c28a65c8e451d16f9a7cf48dd5d4dede0ba1f2d77042` |

## 独立一次源核对

审阅者重新获取 22 个精确上游文件/页面，全部 HTTP 200；读取相关参数表、函数/分支与路径小节，核对正文，而非只判断可达性。原文件与 HTML 文本只存临时目录，未镜像入库。固定源码行号以下均为原文件坐标；HTML 表项用页名/字段定位，临时提取行号不冒充上游锚点。

- ROCm `7da43026e4f2ef7600433c38c820732f7a205d22`：rccl-tests README、PERFORMANCE、common/util、六算子文件，以及 AllGather policy 和 device-time host 辅助头（12 个）。
- NVIDIA nccl-tests `b4d5beebca8a76cf01335f724d154b9b9d394d96`：README、common 参数解析（2 个）。
- CANN 官方 `doc_center/source/zh/CANNCommunityEdition/910/devaids/hccltool/`：HCCLpertest_16_0001、0004、0005、0006、0007（5 个）。这些静态页证明局部指南契约，不证明具体工具包、CANN/HDK/机型可运行交集；普通入口的既有异题限制不变。
- NCCL 2.27.5 env、DGX H100 SuperPOD Network Fabrics、GPU Node Triage（3 个）。后两项是可变官方页，观察日期为本轮日期；不扩为所有 fabric/机型事实。

| 关键原文件 | SHA-256 |
|---|---|
| RCCL common.cu | `1339f9535d68b748677bd817e88d02002a71ff27b7f2b7ce41fcaccaa505f9d7` |
| RCCL broadcast.cu | `bba8541491d1361f54a03c23e07880befc85ebb5e47e46d355f10b82d3c05965` |
| RCCL gin_sdma_allgather_policy.h | `851eb0588ac02b486501408cd7c0e38daae76163cb02945c654e73c547678b6b` |
| RCCL gin_sdma_devtime_host.h | `d1c1a59adb5a58d8f3f8b6797a8634ac6c08f3e672403c37131e4ffc872e8e35` |
| NCCL common.cu | `74cecb9591aeeadbabef6967af2ccb1ec4507f163cc7119c5e9299c470232626` |
| HCCL 参数说明 0005 | `85dfdd58f53d37d5428d0559a057228526d5ccbee233a095887c12aacc8006fe` |
| HCCL 结果说明 0006 | `ad4f33978cecba4179e2ab39cfa82bbca06cd1783d012879825c274c28479fc1` |
| NCCL env | `748cc433bc2aa9ec61570ebc57f4e3c5e9a1845106c43ba52a6eba712f472303` |
| SuperPOD fabric | `e8426756298eaeb5da9cef49d7232fb8acb869a3d153e5f63743930f413da25f` |
| GPU Node Triage | `bc4d3364f19ec822b2ca2e3ac214b1418ad84f85a181d7bd872e2da1045b5aa1` |

T03-01/T03-03 的已审阅资料按当前正文链接与限定范围复用，不声称本轮重新获取其所有远端来源。T03-05/T04-01 和 Batch 17/18 保持既有有限通过及例外边界。

## B19-C16 — P2 / OPEN：RCCL 换算和计时缺少模式分支，页脚判据方向不清

位置：T03-07 正文 L85–87（A1）。

`-C 1` 被无条件解释为 cputime，但固定 common.cu 只有 `report_cputime && deviceImpl==0` 才显示 CPU 列；设备实现分支仍显示 deltaSec。默认 host 计时还先按 `iters×agg_iters` 归一化，再按 graph launch 数缩放和 rank 选项聚合；device-only 分支则会以设备 hook 返回的时间替换 deltaSec，不能把所有模式读成相同分母。见固定 [common.cu L1070–1128](https://github.com/ROCm/rocm-systems/blob/7da43026e4f2ef7600433c38c820732f7a205d22/projects/rccl-tests/src/common.cu#L1070-L1128)、[显示分支 L1259–1266](https://github.com/ROCm/rocm-systems/blob/7da43026e4f2ef7600433c38c820732f7a205d22/projects/rccl-tests/src/common.cu#L1259-L1266)及[归一化辅助函数 L41–51](https://github.com/ROCm/rocm-systems/blob/7da43026e4f2ef7600433c38c820732f7a205d22/projects/rccl-tests/src/gin_sdma_devtime_host.h#L41-L51)。

六系数目前虽声明来自 PERFORMANCE，仍不能覆盖该快照全部 `broadcast_perf` 模式：`RCCL_TESTS_ALLGATHERV_ENABLE=1` 时，源码使用 `count×nranks×typesize` 和 `(n-1)/n`；普通 Broadcast 才使用 `count×typesize` 和系数 1。见[broadcast.cu L11–15、L82–93](https://github.com/ROCm/rocm-systems/blob/7da43026e4f2ef7600433c38c820732f7a205d22/projects/rccl-tests/src/broadcast.cu#L82-L93)及[README grouped-broadcast 节](https://github.com/ROCm/rocm-systems/blob/7da43026e4f2ef7600433c38c820732f7a205d22/projects/rccl-tests/README.md#grouped-broadcast-allgatherv-mode)。另外页脚实际比较的是 `平均 busbw < NCCL_TESTS_MIN_BW×0.9`，不是平均值乘 0.9；环境值未设时采用 -1。见[common.cu L2757–2788](https://github.com/ROCm/rocm-systems/blob/7da43026e4f2ef7600433c38c820732f7a205d22/projects/rccl-tests/src/common.cu#L2757-L2788)。当前概括不足以让读者复算和解释不同模式。

关闭条件：限定 PERFORMANCE 的普通算子模型，补上述 Broadcast 环境分支；按 host/default、CPU 显示、graph 和 device-only 分列或明确限定本节仅覆盖默认 host 模式并列出例外；写出单操作归一化和页脚实际比较方向/环境条件。保留 us/ms 来源冲突、工具门槛非部署门槛的界限。作者未核对的实现可如实保留，不能将普通分支推广。

补充取证（不单独计发现）：AllGather 的[辅助函数 L145–155](https://github.com/ROCm/rocm-systems/blob/7da43026e4f2ef7600433c38c820732f7a205d22/projects/rccl-tests/src/gin_sdma_allgather_policy.h#L145-L155)明确采用 `perRankCount×typeSize×n` 和 `(n-1)/n`。这是审阅者新取得的固定源码事实；作者输入的“未核对”本身不冒充已核对，也不作为另一个 P2。

## B19-C17 — P2 / OPEN：HCCL 的已知参数/计时契约被压成存在性或误归 unknown

位置：正文 L180–182（A2）。

同一段把 `-n` 写成默认 20 次，又写成节点数×NPU 数，没有注明二者分别属于 executable 后的工具参数与前面的 MPI launcher 参数。[0005 参数说明](https://www.hiascend.com/doc_center/source/zh/CANNCommunityEdition/910/devaids/hccltool/HCCLpertest_16_0005.html)的命令格式和 MPI/工具两表明确区分；混用会改变测试规模或迭代口径。

“Host/Device 边界未在指南给出”也过宽：该页 `-t/--onlydevicetime` 已给默认 0 的全耗时语义和开启后的排除项，并列出 AIV/CCU、BUFFSIZE>100MB、warm-up/iters≤100 三个条件。缺的是实现中的具体计时点与跨 rank 归约，不能把文档契约一起归 unknown。`-c 0/1/2` 和 success/failed/NULL 目前只说“存在三条件”，读者无法识别校验未开或数值范围导致的 NULL；后者已由[0006 结果说明](https://www.hiascend.com/doc_center/source/zh/CANNCommunityEdition/910/devaids/hccltool/HCCLpertest_16_0006.html)明示，不能以开启 `-c 1` 单独准入。

关闭条件：明确 `mpirun -n <number>`、工具 `-n <iters_count>`、`-p` 的不同角色；把 `-t` 已知契约/三条件写出来，将未知收窄为实现计时点、rank 聚合等；说明 `-c` 三值与 NULL 两类未校验分支，不把 NULL 洗为正确性通过。`-p` 从 0 连续选择应限定为[0007 规格约束](https://www.hiascend.com/doc_center/source/zh/CANNCommunityEdition/910/devaids/hccltool/HCCLpertest_16_0007.html)所述常规分支，另记[0004 使用方法](https://www.hiascend.com/doc_center/source/zh/CANNCommunityEdition/910/devaids/hccltool/HCCLpertest_16_0004.html)的 `HCCL_TEST_USE_DEVS` 指定设备例外；3K/5K 超时值标明为指南示例建议。实现未知与 BLOCKED-1 保持。

## B19-C18 — P2 / OPEN：rail 条件被简化为路径事实，缺少可区分的对照判据

位置：正文 L144–148（A3）。

`NCCL_CROSS_NIC=0` 不能无条件简化为“同 rail”：[NCCL 2.27.5 定义](https://docs.nvidia.com/deeplearning/nccl/archives/nccl_2275/user-guide/docs/env.html#nccl-cross-nic)明确给出各节点 communicator GPU 成员不同仍可能跨 NIC 的例外。`NCCL_IB_HCA` 过滤、CROSS_NIC 意图、algo/proto/channel 数也不能代替实际选中 NIC/端口及其 fabric 映射。HCCL 的 host socket 选择只能记录 bootstrap 路径，不证明设备侧 RDMA rail。

[SuperPOD Network Fabrics / Compute InfiniBand Fabric](https://docs.nvidia.com/dgx-superpod/reference-architecture-scalable-infrastructure-h100/latest/network-fabrics.html#computeinfiniband-fabric)的一跳事实限同一 SU 的对应 rail；跨 SU 的同 rail 也可能经过 spine，当前“RA 同 rail 一跳/跨 rail 过 spine”漏了 SU 边界。L148 虽名为四类“区分规则”，只重述单组/总量及缺遥测边界，没有说明如何区分均衡、热点、多租户争用与协议重试；原 acceptance 2 尚未满足。

关闭条件：把请求配置、实际库端点/映射证据、IB 或 RoCE 路径、同窗端口计数器分列，并保留实际路径缺失时的 unknown；补 CROSS_NIC 例外与 SU 条件。给四类候选的最小输入/观察/对照/无法判断表：按已映射 rail 的预期负载比较方向一致的遥测；热点不由单列 busbw 证明；争用需要与同条件隔离/背景负载对照；重试只使用已核对含义/范围的计数器，不能凭吞吐下降推出。复用[T03-03](../../knowledge/03-communication/rdma-baseline-and-congestion-triage.md)具体小节，不需重复其全部内容或填造数值，也不凭单一响应计数判定根因。

## B19-C19 — P2 / OPEN：工具矩阵没有标明各参数归属

位置：正文 L208（A4，应用/库行）。

三套工具并列后统一列 `-a/-I/-K/-A/SPLIT/-X/-Z`，会被读成共享接口。固定 NCCL-tests 的[common.cu L1198–1238 参数表](https://github.com/NVIDIA/nccl-tests/blob/b4d5beebca8a76cf01335f724d154b9b9d394d96/src/common.cu#L1198-L1238)没有 `-A/-X/-Z`；RCCL 的[README Arguments](https://github.com/ROCm/rocm-systems/blob/7da43026e4f2ef7600433c38c820732f7a205d22/projects/rccl-tests/README.md#arguments)才给出这些参数。HCCL 0005 的 `-a` 是特定产品的 accelerator 选择，不能按 NCCL/RCCL 的 rank average 解释。声明“各不互拼”不足以消除同一字段列的歧义。

关闭条件：一工具一行或用逐工具列标出参数/原生输出/缺失字段；确认 `-a` 同名异义，`-A/-X/-Z` 属本次 RCCL 快照，NCCL/RCCL 的 `NCCL_TESTS_SPLIT` 不外推 HCCL。HCCL 逐次分布应写为本次所选文档未定义，不能宣称所有实现都不存在；缺字段记 unknown/本快照不提供。RDMA、物理、主机路径行保留分层，给可解析的已审阅条目/来源入口，并明确 perftest 校验覆盖门禁所属后端与粒度，避免把它当三个 collective 工具的通用输出。

## B19-C20 — P2 / OPEN：六信号缺完成率定义，恢复的零增量范围过宽

位置：正文 L164（A5）。

“完成率（超时/退出/残留进程清理）”只有事件名，没有统计单位、分子、分母及窗口；清理残留进程不代表计划测试已完成。恢复写成“新窗零新增 counts”还会涵盖正常 bytes/packets 和拥塞响应，可能把没有测试流量误判为恢复。

[T03-03 的计数器与停止恢复安排](../../knowledge/03-communication/rdma-baseline-and-congestion-triage.md#停止条件与恢复安排)明确：零新增仅用于已定义错误列；正常流量/流控响应按同窗基线带比较，校验须满足覆盖门禁；缺字段/分母/窗口时无法判断。不能在本页浓缩后丢掉这些限定。

关闭条件：预先选择运行、矩阵单元或操作的完成粒度，给计划/尝试数、按计划完成数及其比率定义；超时、缺行、跳过、不支持、未校验分开记录，分母/证据缺失记 unknown。恢复记录起止事件/观察窗口、错误项零新增、同条件复测与正确性/覆盖条件；仅适用 RDMA 分支的门槛明确限定并链接，collective/应用恢复不由进程退出或计数器一项代替。六信号无需通用数值阈值或实际测量结果。

## B19-C21 — P2 / OPEN：新增核心主张与研究记录缺精确来源映射

位置：正文 L26、L85–87、L146、L180–182、L208–217；来源记录 L3、L7、L11、L16。

AllReduce 函数链接落到 `tree/.../src`，README 参数链接落到目录；RCCL 计时/页脚、HCCL 参数/结果/跨节点条件多处只有文件简称或 000x 数字。研究记录“主张—来源定位表”实际为一段名单，没有完整 ID、精确 URL、固定源码行段、支持范围，也未给“同批来源准备报告”的可解析入口。“T03-03 已审阅”不替代关联小节和本页复用范围。

GPU Node Triage 的“URL 未确认，不链接”与登记现状不符：既有 `src.nvidia.gpu-node-triage-2026-10-08` 已登记正确路径和 10-09 复核，本轮再次取得[官方 Network Testing 节](https://docs.nvidia.com/deploy/gpu-debug-guidelines/gpu-node-triage.html#network-testing)，支持逐对/换节点/rail 隔离方法。正文使用该方法却无该 ID 或精确链接。无需新增来源登记。

关闭条件：把 A1–A5 核心主张的近旁链接指向精确 blob/页节，研究记录改为真实“完整 ID—精确地址—行段/字段—支持范围/未覆盖”表，与正文一致；补 T03-01/03/05/06/研究记录的实际入口。若保留 GPU Node Triage 方法，复用已有 ID/正确 URL 并注明可变页观察日期；若删方法则同步删依赖。verification 区分作者核对与本报告新取证，收窄 unknown 与计时文档契约，不将审阅方证据追记为作者此前完成。源码辅助头也复用现有 rocm-systems ID，不需为每文件新增来源。

## 已接受内容与待复核状态

已接受：六个加法块和既有正文保护；RCCL us/ms 冲突单列、普通 PERFORMANCE 模型与 NCCL 不互换；HCCL data_size/avg_time/算法带宽独立原字段；不填跨节点测量结果、不提供全局带宽门槛；三层路径和四层工具的组织方向；BLOCKED-1 未被参数表关闭。未核对的实现可以如实保留，不能用泛化的 unknown 覆盖已经给出的文档契约。

| 状态 | 范围 |
|---|---|
| 本轮 OPEN（6 P2） | B19-C16、C17、C18、C19、C20、C21 |
| 既有 CLOSED（15） | B19-C01–C15，原通过范围保持 |
| 验收子项单列 OPEN | BLOCKED-1，非重复新发现 |
| T03-07 | 初审未通过，修订后按以上关闭条件定向复核 |
| T03-06 | 已交付文档/来源范围通过保持，原 acceptance 5 未验收 |
| T03-08 / 整批 | 本轮未交付审阅 / 未声明整批完成 |

本轮只新增本报告并更新来源审计的当前入口/交付表；不改作者正文、来源记录、修订映射、索引、登记、计划或其他批文件。构建产物按 make 重建。真实 GPU/NPU、MPI/collective、故障注入或配置变更均未执行；模型审阅和结构检查不建立硬件验证。


2026-10-13 最终校验：`make check` / `make build` 均 PASS（88 篇内容 / 386 项来源）。来源清单确认只有本报告新增及来源审计更新，无删除，其他输入 SHA 不变；本地文件链接均可解析，NCCL CROSS_NIC、SuperPOD compute fabric、GPU Node Triage Network Testing 三个远端锚点与取得的 HTML id 一致。未改 src/kb，不需 make test；无实机验证。
