# 第十九批 T03-08 来源记录

任务：T03-08（修订 `bandwidth-degradation-triage.md`，只做加法；既有步骤 1–7、停止条件、完成判据逐字保留，步骤 7 下一步分叉与步骤 9 出口为例外协调）。作者共十三轮：首轮（同批来源准备）＋第二/三/四/五/六/七/八/九/十次修订＋第十一次修订（映射同步）＋第十二次修订（账本表交付）＋第十三次修订（本轮：第四轮复用列明、#223 未采用交代、L19 定位改稳定节名；无新增远程取证，仅复用已核对来源）。第三至六轮中未能从现存记录逐项还原取证通道的部分记 unknown（不补造历史实开）。第五轮“作者四轮＋审阅四轮”为旧计数口径错误，已纠正为作者五轮（首轮＋第二至第五次修订）＋审阅五份（初审＋一至四次复核）。第七轮节内目标自述逐项落盘：网络/存储完整复现契约→第八轮（映射第八轮节＋正文步骤 9 轮次明细），C3/S5/S6 清理→第八轮（映射第八轮节＋本记录 unknown 清单“未采用候选”条目），S7 删除→第九轮（映射第九轮节＋本记录 unknown 清单第 9 项“NCCL 三页已用”）；第七轮节本身为增补目标，非落盘记录。审阅方独立取证轮次：加法初审＋Codex 定向复核（一/二/三/四/五/六/七/八/九/十/十一/十二次）——见加法初审与复核报告，不冒充作者当时已完成；输入时既有十三份，后续新增复核报告不计入本轮输入。

### 逐轮账本（作者轮次—修订节—新增取证/复用/unknown；通道无原始响应留存处记 unknown，不补造）

| 作者轮次 | 修订节 | 新增取证对象/版本/入口与通道，或复用，或 unknown |
|---|---|---|
| 首轮 | T03-08 修订（处理 C22–C27 全部 6 项） | 新增取证对象：#2409 全文、#814 全文、NCCL env SPLIT_DATA_ON_QPS 页、T03-07 矩阵引用、#209 注册；入口/版本见主张表精确 URL；通道为作者自述远程实开，现存记录无逐条原始响应留存，通道细节记 unknown。 |
| 第二轮 | T03-08 第二轮修订 | 新增取证：8 条 #2409/#814 评论 URL 逐条定位（见主张表）、#209 注册引用；通道为作者自述 curl 200，原始字节未入库留存，通道记 unknown。内容交付：四分支逐支门禁、C26 三处删除、记录映射表重写。#223（第九次复核所记与 #209 并列提及的候选）：未在登记/主张表/正文采用，无精确 URL/版本记录，现明确为未采用候选，不引用；历史是否实开不能还原，记 unknown。 |
| 第三轮 | T03-08 第三轮修订 | 内容交付：支持/排除方向纠正、步骤 7 分叉、四类轮次七要素、UFM 限定强度、记录精确 URL；troubleshooting-rccl.rst URL 核对自述 curl 200（原始响应未留存）。具体对象/版本/新增或复用范围未能从现存记录逐项还原，记 unknown。 |
| 第四轮 | T03-08 第四轮修订 | 内容交付：物理支有限排除门禁、步骤 9 出口统一、四轮明细、UFM 精确页。具体复用记录：#2409/#814 评论 URL（8 条，见主张表案例行）、NCCL env/ACS/RAS 三锚点（见主张表热点行）、UFM 精确页（版本 UFM 4.18.15，见主张表）、RCCL troubleshooting 源码节（therock-10.1，见主张表对照行）、T03-07 跨节点矩阵节、T03-06 三库对照与 RCCL 档案入口（见正文步骤 9）；版本与入口以主张表/登记为准。无新增远程取证主张，不追加远程取证。 |
| 第五轮 | T03-08 第五轮修订 | 内容交付：无新增观测条件、步骤 9 五列表格＋明细、UFM 精确页版本范围；取证自述：README user-content-arguments 锚点实测、all_reduce.cu raw L78–84（curl 200 自述），未绑定本轮历史 ref/精确入口，入口与复用范围记 unknown（T03-07 现有同类入口不自动归属本轮）。计数口径见映射第五轮节现文（作者五轮＋审阅五份）。 |
| 第六轮 | T03-08 第六轮修订 | 内容交付：L9 落盘核对、步骤 9 五列与明细、UFM 精确页、官方工具节源码 URL；取证自述：三处文档锚点（nccl-cross-nic、computeinfiniband-fabric、network-testing）curl 200，未绑定本轮版本/观察入口/新增或复用状态，记 unknown（本轮可读不倒证历史）。 |
| 第七轮 | T03-08 第七轮修订 | 无新增远程取证，仅复用；内容为出口统一、四轮明细、映射同步。节内“已删除/已补齐”系增补目标，实际落盘见第八/九轮拆分（本记录 L3 段）。 |
| 第八轮 | T03-08 第八轮修订 | 无新增远程取证，仅复用；实际落盘：网络/存储完整复现契约、C3/S5/S6 清理记未选（映射第八轮节＋本记录 unknown 清单“未采用候选”条目）。S7 此时仍未清理（第八次复核 L81/L90）。 |
| 第九轮 | T03-08 第九轮修订 | 无新增远程取证，仅复用；实际落盘：S7 删除（映射第九轮节＋本记录 unknown 清单第 9 项“NCCL 三页已用”）。L149 当时累计 25/2 为错误（第十二轮已纠正为 26/1）；L151“作者八轮＋审阅八份”系沿用第八轮输入口径未更新（见映射第九轮节现文限定）。 |
| 第十轮 | T03-08 第十轮修订 | 无新增远程取证，仅复用；S7 删除落盘确认、前次累计 26/1 引用、轮次同步（映射第十轮节）。该轮“逐轮账本交付”在第十次复核未通过，不能倒记已闭环。 |
| 第十一轮 | T03-08 第十一轮修订 | 无新增远程取证，仅复用；实际落盘：第五轮计数纠正（映射第五轮节现文）、第九轮累计 26/1 确认梗概。“审阅十份”指第十轮输入口径；“含本报告”指待交付的第十一次复核报告（见映射第十一轮节现文限定）。 |
| 第十二轮 | T03-08 第十二轮修订 | 无新增远程取证，仅复用已核对来源；交付：L151/L159 对象限定、逐轮账本表（首轮–第十一轮行）创建、第七轮落盘拆分、历史差异解释、verification 精确引用（见映射第十二轮节）。 |
| 第十三轮 | T03-08 第十三轮修订（本轮） | 无新增远程取证，仅复用已核对来源；交付：第十二次复核第 3 条三项补记（第四轮复用列明、#223 未采用交代、L19 定位改稳定节名；见映射第十三轮节）。 |

注：上表“作者自述”指修订映射各轮节及本记录主张表可定位的内容；历史取证差异（第六次复核 L101 所记第三/四/五次“无新增远程取证”、第九次复核 L94/L96/L102 所记第三轮源码 curl 200 与第五轮 raw/锚点自述、第十次复核 L76/L85 所指第三轮改通道 unknown）系回溯补记口径演进所致，无法还原处已按轮次记 unknown，不判定历史真假，不补造响应/哈希/日志，不用当前可读倒证历史。

## 主张—来源定位表（完整 ID—精确页面/评论 URL—字段/支持范围）

| 主张 | 已登记 ID | 精确页面/评论 URL 与字段 | 支持范围 / 未覆盖 |
|---|---|---|---|
| 时间窗对齐与降级 | communication.bandwidth-baselines / communication.rdma-baseline-and-congestion-triage | 跨节点矩阵见 [T03-07 正文](../../knowledge/03-communication/bandwidth-baselines.md)跨节点矩阵节；计数器限定见 [T03-03](../../knowledge/03-communication/rdma-baseline-and-congestion-triage.md)“计数器语义”与“停止条件与恢复安排” | **字段契约已引用，实测矩阵未交付**（"数值已填"旧措辞已纠正） |
| 热点四分支 | src.nvidia.nccl-user-guide-2.27.5 / src.nvidia.nccl-issue-2409 / src.nvidia.nccl-issue-814 / src.nvidia.nccl-issue-209 / src.nvidia.ufm-41815-port-counters | [env SPLIT_DATA_ON_QPS](https://docs.nvidia.com/deeplearning/nccl/archives/nccl_2275/user-guide/docs/env.html#nccl-ib-split-data-on-qps)（默认值/分摊语义）；[ACS 节](https://docs.nvidia.com/deeplearning/nccl/archives/nccl_2275/user-guide/docs/troubleshooting.html#pci-access-control-services-acs) DMA 重定向（配置路径，非错误计数）；[RAS sample-output](https://docs.nvidia.com/deeplearning/nccl/archives/nccl_2275/user-guide/docs/troubleshooting/ras.html#sample-output) MISMATCH 瞬态（须重复查询）；#2409 rail 扫描（同条件对照）；#814 拓扑矩阵（个案）；#209 socket/CPU（TCP 个案） | 物理错误仅已核对事件：[UFM `Rcv Errors`/`Symbol Errors`/`Link Error Downed`/`Xmit Discards`](https://networking-docs.nvidia.com/ufmsdnappswum/41815/infiniband-port-counters)（版本 UFM 4.18.15，IB 范围；不覆盖 RoCE/HCCS/目标现场能力；口径经 T03-03）；个案不泛化 |
| 对照设计 | src.nvidia.nccl-issue-2409 / src.amd.rccl-docs-10.1.0 / src.rocm.rocm-systems-therock-10.1 / communication.rccl-runtime-and-verification | [#2409](https://github.com/NVIDIA/nccl/issues/2409)（§1 perftest/§2 rail/§3 WQE/§4 sweep 为上游观察，四类轮次“隔离基线→可控背景→单变量→替代路径”方案为本库设计归纳）；Replayer（rank 日志回放定位：[官方 troubleshooting 源码](https://github.com/ROCm/rocm-systems/blob/therock-10.1/projects/rccl/docs/how-to/troubleshooting-rccl.rst) Using the RCCL Replayer 节）/TransferBench（设备间拷贝基准：同文件 Collect the TransferBench data 节）分列（用途见 [RCCL 档案工具节](../../knowledge/03-communication/rccl-runtime-and-verification.md)）；FaultDiag parse 方法存在性（版本/输入未选定，仅候选） | 只设计不执行；未固定版本/输入的工具保留候选 |
| 主案例环境/证据 | src.nvidia.nccl-issue-2409 | [Issue #2409](https://github.com/NVIDIA/nccl/issues/2409)（环境表）；[粒度跟帖](https://github.com/NVIDIA/nccl/issues/2409#issuecomment-5660150852)（1/8 QP、16/128 KiB 表；handoff 假说阶段）；nccl-tests 多算子表、WQE monitor、perftest 对照表、30+ sweep表（同页）；[维护者关闭](https://github.com/NVIDIA/nccl/issues/2409#issuecomment-5699369631)（按请求关闭，非独立复现） | 报告者自述＋关闭记录；非本库复现；交换机计数器/期望值 unknown |
| 主案例反证/原因 | src.nvidia.nccl-issue-2409 | [QP/深度跟帖](https://github.com/NVIDIA/nccl/issues/2409#issuecomment-5660232470)（1 QP/depth 8 未线速；8 QP/depth 8 线速；depth 1 推算）；[修正回复](https://github.com/NVIDIA/nccl/issues/2409#issuecomment-5673453587)（修后双表；ADAPTIVE 无差复测；深流水掩盖/浅流水暴露）；普遍排除规则已删除 | 报告者自述；非本库复现 |
| 相关案例 #814 | src.nvidia.nccl-issue-814 | [Issue #814](https://github.com/NVIDIA/nccl/issues/814)（AMD CPU topo XML、p2p/pairwise 矩阵）；[首个维护者回复](https://github.com/NVIDIA/nccl/issues/814#issuecomment-1493802672)（双向/多流交织，推断强度）；[作者关闭](https://github.com/NVIDIA/nccl/issues/814#issuecomment-1496450442)（ring 调整未果，未验证替代 CPU）；[2.23 评论](https://github.com/NVIDIA/nccl/issues/814#issuecomment-2283482549)（P2P 避让，不超 PHB 效果）；[GeForce 澄清](https://github.com/NVIDIA/nccl/issues/814#issuecomment-2825666454)（不表示近期支持 P2P） | `--bind-to none`/tree/最慢链路归属已删除；两评论不合成修复/支持结论 |
| 相关案例 #209 | src.nvidia.nccl-issue-209 | [Issue #209](https://github.com/NVIDIA/nccl/issues/209)（TCP 开帖，无 RDMA）；[绑定建议](https://github.com/NVIDIA/nccl/issues/209#issuecomment-491475792)（socket 驱动线程/绑定一线检查） | TCP 路径个案，不外推 IB；不作通用验证修复 |

## unknown 清单

1. 跨节点矩阵字段契约已由 T03-07 引用，实测矩阵未交付；2. T03-03/T03-05/06 具体输出引用；3. #209 修复 release（未核对，unknown）；4. ROCm 注记独立测量（未采用候选，不引用）；5. #2409 期望值（未核验，unknown）；6. NIC/交换机/HCCS 计数器：旧正文"本库尚无遥测来源"为**原批（Batch 09）核对范围**，当前 T03-03 计数器文档可复用但现场机型/字段能力未证实（新增限定）；7. 跨节点时钟方法；8. HCCL Test 计时实现；9. NCCL env 页（SPLIT_DATA_ON_QPS 默认值/分摊语义）、ACS 节（DMA 重定向，配置路径）、RAS sample-output（MISMATCH 瞬态须重复查询）已用（S7 代号删除）；10. HCCL 工具介绍页（未实开，未采用候选，不引用）；11. RCCL troubleshooting（HTML 未取成功，仅 therock-10.1 源码用途区分）；12. FaultDiag ref（未固定，仅候选，不引用）；13. 新页面许可 unknown；14. 机型应达带宽 unknown；15. #2408 根因未取证；16. 二手转述排除。
