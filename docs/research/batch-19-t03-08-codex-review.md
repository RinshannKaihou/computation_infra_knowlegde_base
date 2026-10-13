# 第十九批 T03-08 加法初审

审阅日期：2026-10-13（Asia/Shanghai）。正文、作者来源记录及两项 Issue 登记中的 `2026-10-14` 保留为交付标签，不作为本轮实际取证日期。

**结论：T03-08 需要修订，新增 6 项 P2（B19-C22–C27），全部 OPEN。** 本批累计 21 CLOSED / 6 OPEN（审阅发现）。T03-06/T03-07 的已交付有限文档/来源范围通过保持，并非待重新初审；BLOCKED-1（HCCL Test × 目标 CANN/HDK/机型官方交集）继续单列 blocked_on_evidence/open。整个 Batch 19 未验收。

约定审阅配置为 `gpt-6.1-sol / xhigh`；由当前 Codex 主会话执行，无子代理。实际运行模型/推理等级的可核验限制沿用此前报告，不补造运行元数据，不追改历史模型。本轮只审阅交付的 G1–G5、来源/元数据/导航及必要依赖边界，不执行实验或代作者修订。

## 输入与加法范围

| 输入 | SHA-256 |
|---|---|
| [T03-08 正文](../../knowledge/03-communication/bandwidth-degradation-triage.md) | `6cd54715e1368d8f3df7689d6e69f63f8ee0f370951fdd649b26c49896e1328d` |
| [T03-08 作者来源记录](batch-19-t03-08-sources.md) | `5df88b7e0e30da8220e5049cfba822184e84477bd9e8225897d5dd482c59035c` |
| [03 索引](../../knowledge/03-communication/index.md) | `a531a9298df7825823c369dd987a3f8e15388725dbe77f7c286f826bc80530ff` |
| [来源登记](../../sources/registry.yaml)（388 项） | `98ee63eff28c055c7d5fca71f16c28b308cef21a772f0e48ba75945dea58d614` |
| [任务计划](../../plans/full-coverage-backlog.yaml) | `121826a4d499273e7f6a00735e0a53931eef5c097bd66ab6b2425fdbc36ddfe0` |
| [来源审计](batch-19-source-audit.md)（本轮更新前） | `bfb6120fc01a337207e06ef6a9d2c013067d927db8eb84dd0d17734c2df9f475` |

正文与当前 Git HEAD 的原正文比较只有四个 insert 块，没有 replace/delete；既有步骤、停止/完成判据未被改写。旧正文 SHA 为 `b4b12f1a6812481e595415ddee5befad599d1b60a42c0fb483013bbe2c2f6f89`。G1–G5 分组不等于文本插入块数量，四块不构成缺项。

登记确为末尾追加两个 Issue：去掉 #2409/#814 两项后，字节 SHA 精确恢复上轮 `e84c3b6eb61a83a46dbbfd371e5de4112def120131e0c374181e8e5acbf8f51f`。来源总数 386→388，无其他登记变动。

T03-06 正文 SHA `d4a5fb535ba78d852e070f09ff387b69dc6e1ab7cf86620c7ee08e9a99577646`、T03-07 正文 SHA `8c2884b63cf7b638c1df2d7de88f5fe9d2923c0d95b025548041aea203574039` 与各自通过报告一致，来源记录、T03-05/T04-01 与计划保持既有身份。[T03-06 第三次复核](batch-19-t03-06-codex-third-recheck.md)、[T03-07 第三次复核](batch-19-t03-07-codex-third-recheck.md)的有限通过不重新打开；HCCL Test 配套子项仍未验收。

## 一次源取证与角色

通过 GitHub 连接器独立获取 #2409/#814 的完整 body 和全部评论，分别 4/6 条，与网页正文对照；读取开帖、后续测量、修正/关闭及较晚的适用性说明，未把 Issue 关闭当作独立验证。正文作者的“已实开”与本轮审阅者取证分别记录。

关键精确评论：

- #2409 的[首个粒度对照](https://github.com/NVIDIA/nccl/issues/2409#issuecomment-5660150852)、[QP/深度对照](https://github.com/NVIDIA/nccl/issues/2409#issuecomment-5660232470)、[报告者修正归因与修后表](https://github.com/NVIDIA/nccl/issues/2409#issuecomment-5673453587)、[维护者按请求关闭](https://github.com/NVIDIA/nccl/issues/2409#issuecomment-5699369631)。
- #814 的[AMD CPU 多流解释](https://github.com/NVIDIA/nccl/issues/814#issuecomment-1493802672)、[作者未验证替代 CPU 即关闭](https://github.com/NVIDIA/nccl/issues/814#issuecomment-1496450442)、[NCCL 2.23 的 P2P 避让建议](https://github.com/NVIDIA/nccl/issues/814#issuecomment-2283482549)、[较晚 GeForce P2P 边界澄清](https://github.com/NVIDIA/nccl/issues/814#issuecomment-2825666454)。

重新获取 NCCL 2.27.5 env/troubleshooting 和 RCCL docs-10.1.0 troubleshooting 三个精确 HTML，均 HTTP 200，并读取相关参数/ACS/工具说明。web 阅读器对 AMD 页曾返回 429，改用只读获取取得完整正文，不把失败响应算成证据。T03-03/05/06/07 的已通过内容按限定范围复用，本轮不声称重抓其全部来源；FaultDiag 未固定到本条目可追溯的工具样板，不从搜索片段推定可执行能力。

| 临时证据 | SHA-256 |
|---|---|
| #2409 body（连接器数据的规范化 JSON） | `5e43e0806a403ee69a4e2c0269af94a97eb8850223d1c32ca832044e590931e6` |
| #2409 全部评论（规范化 JSON） | `433d4e5aa20dac59aab2f206aa0529a7dd3af93de9204cdb4256a0b224ad6f88` |
| #814 body（规范化 JSON） | `72c4375b5fcae7f5ae55112ea99b28f2d4413ec415476a18abb13595ccc33faa` |
| #814 全部评论（规范化 JSON） | `41cedeb1afcb794627f2842de6e798901460d81bde6fb2b289fc8a8d8c96bbfe` |
| NCCL env 原 HTML | `748cc433bc2aa9ec61570ebc57f4e3c5e9a1845106c43ba52a6eba712f472303` |
| NCCL troubleshooting 原 HTML | `ae26c111602e8d2dcc2327bb19ac1688dccb3932f698ee868c45e9d60ee8898d` |
| RCCL troubleshooting 原 HTML | `967476eb7ddc66dd21932cc45a1318ded513947e0542819b4658a6f93965e8c8` |

规范化 JSON 是可复核的连接器输出整理，不冒充 HTTP 原字节；省略 avatar/HTML 重复字段，保留正文、作者和评论 URL。外部全文仅存临时目录，未镜像入库，未执行工具或采集现场数据。

## B19-C22 — P2 / OPEN：时间窗对齐缺可判定的输入与跨节点降级范围

位置：正文 L60（G1）、L73–74；来源记录 L11/L15。

新行要求日志、计数器、测试输出“可对齐”，但没有规定窗起止、时间基准、节点间偏差/精度、采样更新周期如何登记；缺时钟条件只降级“慢 rank 判定”。这样仍可能把不能确认同期的跨节点计数器/热点证据写成支持路径或争用的结论。来源记录同时承认跨节点时钟方法未知，不能仅用“对齐包”名称完成原 acceptance 1。

关闭条件：增加最小字段/判定契约，至少包含 run/节点/rank 身份、测试与采样窗起止、日志时钟基准及跨节点对齐依据/不确定性、计数器更新边界、端口/rail 映射；不要求填真实数值或虚构时钟方法。说明何时可以比较同期增量，何时只能保留单节点/静态证据；时钟条件缺失须限制所有依赖跨节点先后/同期关系的支路，不只慢 rank。可复用[T03-03 的窗口/计数器限定](../../knowledge/03-communication/rdma-baseline-and-congestion-triage.md)与[T03-07 的记录契约](../../knowledge/03-communication/bandwidth-baselines.md)，把设计与现场已取得证据分开。

## B19-C23 — P2 / OPEN：热点四分支混淆配置条件与物理错误

位置：正文 L73（G2）。

“物理错误”分支仅列 ACS/IOMMU/GDR/注册限制，这些是路径配置或运行前提，不能当硬件错误信号；[NCCL ACS 节](https://docs.nvidia.com/deeplearning/nccl/archives/nccl_2275/user-guide/docs/troubleshooting.html#pci-access-control-services-acs)说明的是 DMA 被重定向及性能影响，#2409 的解决也属于平台/配置侧修正。共享干扰分支没有网络/存储争用的独立检查，调用/消息分支则主要列算法、QP 配置和设备顺序。三态标签本身不能区分四类原因，原 acceptance 2 仍未完成。

关闭条件：在新增范围把 ACS/IOMMU/GDR/注册放回配置/映射条件；物理错误使用已核对含义和作用域的错误/链路事件，缺字段或版本能力时 unknown，不用吞吐低证明硬件故障。共享干扰覆盖 CPU/网络/存储的输入与隔离/背景对照；调用/消息变化回链实际 collective、datatype/count/root/rank/次序及消息记录，设备顺序仍按映射解释。每项给最小输入、支持/排除条件与 unknown 条件；可链接既有步骤和 T03-03/04/07，不需重写旧步骤 1–7，也不把个案理论直接当普遍事实。

## B19-C24 — P2 / OPEN：对照设计缺实际路径变量、失败停止与原值恢复

位置：正文 L72–74（G3）及原停止/完成节的联动。

新增步骤排在步骤 7 的汇总/完成出口之后，没有说明如何进入；“基线→单变量→替代路径”只列工具名，没有指明隔离、背景负载、路径变量及各轮的可比输入/观察/判定。相同 rail 的 perftest 是跨测量层对照，Replayer/TransferBench 也不会仅因名称存在就构成替代路径。[RCCL 官方工具说明](https://rocm.docs.amd.com/projects/rccl/en/docs-10.1.0/how-to/troubleshooting-rccl.html)分别描述 collective 日志回放和设备间拷贝基准，作用不能互换；FaultDiag 版本/输入未选定，当前只能是未完成方法候选。

步骤 9 还把“任一完成判据 1–4”当测试停止条件，没有明确正确性失败、超时/异步错误或观测失效的处理；恢复要求“改回默认值”，与原文记录原值/回滚以及同口径基线相冲突。默认配置不一定是该环境原先批准的配置，正常诊断结束也不同于风险触发停止。

关闭条件：在新增说明里给步骤 8/9 的入口与步骤 7 的关系；为隔离、可控背景、单变量、替代端点/rail/路径列输入、变更项、保持项、原生输出、校验/完整性和无法判断条件，不填实验结果。把独立测量/回放/解析工具与真实路径替代分列，未固定版本/输入的工具保留候选，不算可执行设计完成。单列失败/超时/错误/窗口失效停止条件和诊断完成出口；恢复以保存的原值或经批准的修复配置为准，明确同条件正确性/覆盖及复测要求，不能无条件回默认值。保持“不执行实验”，不添加现场执行授权。

## B19-C25 — P2 / OPEN：主案例把已撤回的“排除 fabric”推断变成可复用规则

位置：正文 L95–101，尤其 L97/L100；来源记录与 #2409 登记的原因强度定位。

#2409 的[最终回复](https://github.com/NVIDIA/nccl/issues/2409#issuecomment-5673453587)明确修正开帖结论：perftest 的深流水可掩盖平台路径问题，NCCL 的浅流水暴露它。当前“同条件线速→先排除 fabric”及检查清单仍过强；一个 rail/一种 buffer/深度的 perftest 成功不等于整个 collective 所用路径在同一负载下都被排除。当前还把开帖 1 MiB 的 392.6 Gb/s 与首个跟帖的单 QP/128 KiB 线速简写为同条件；[后续深度对照](https://github.com/NVIDIA/nccl/issues/2409#issuecomment-5660232470)中单 QP/depth 8 的 128 KiB 并未线速，需保留 QP/深度、buffer 和阶段。

已接受：源中确有平台组合修正后及 QP 配置再修正后的测量表；本库无复现，交换机计数器/约 470 的期望来源未核验已如实注明。维护者是按报告者请求关闭，不是独立验证这两项根因。

关闭条件：把开帖假说、粒度/深度对照、报告者修后证据、维护者关闭分别定位并标角色；收窄 perftest 反证为其覆盖的路径/参数/窗口，不保留普遍“先排除 fabric”规则。环境不要用“driver/CUDA/Ubuntu 全部记录”代替实际值或精确定位表；保留不同 NCCL/测试快照身份。复用约 97% 时注明报告者相对未独立核验期望的估算，不作验收门槛；配置变量首次给完整名称 `NCCL_IB_SPLIT_DATA_ON_QPS`，不得把简称当可设置变量。原因强度限报告者自述和所列比较，配置修复不等于库发布修复版本。

## B19-C26 — P2 / OPEN：#814 不支持被归给它的整组机制与配置建议

位置：正文 L73/L102；作者来源记录 L7/L11/L15。

已读取[原始报告](https://github.com/NVIDIA/nccl/issues/814)与全部六条评论。原作者尝试修改 ring 顺序但未奏效；[首个维护者回复](https://github.com/NVIDIA/nccl/issues/814#issuecomment-1493802672)讨论 AMD CPU 上双向/多流交织与流水受影响。正文却将“最慢链路决定 ring 吞吐、socket/CPU 干扰与 `--bind-to none`、tree/ring 流量解释”整组归给此例；原 body/评论没有 `--bind-to none` 或 tree 解释，也没有最慢链路的因果证明。“个案不泛化”不能弥补引用本身不支持主张。

关闭条件：删去或另找精确一次源支持这些归属，并同步步骤 8、相关索引、来源映射。保留 #814 的实际拓扑/矩阵及维护者解释的推断强度，不把作者失败的 ring 调整当修复。若引用后续版本建议，分清[2.23 的 P2P 避让说明](https://github.com/NVIDIA/nccl/issues/814#issuecomment-2283482549)与[后续 GeForce P2P 支持边界澄清](https://github.com/NVIDIA/nccl/issues/814#issuecomment-2825666454)，不推导通用 RTX 4090 能力或已验证修复。相关索引可以保持简短，不要求扩写成第二个完整案例。

## B19-C27 — P2 / OPEN：新增主张仍缺可解析来源映射，且把字段契约称作已交付数值

位置：正文 L33/L59/L71/L74/L110–114；作者来源记录 L7/L11/L15。

研究记录“主张—来源定位表”仍是一段 S1/S2/M3/C1/C2/C3 等未定义代号；没有评论 URL、完整 ID、字段/段落和支持范围。正文的逐条定位入口仍指向 Batch 09 旧记录，新的 T03-08 作者记录未接入；“NCCL/HCCL/RCCL 资料见来源节”没有实际 Replayer/TransferBench/FaultDiag、T03-03/05/06 导航。候选出处未固定，不能据此声称完成逐项一次源核对。

来源记录还写“跨节点矩阵数值已由 T03-07 交付”，而 T03-07 明确交付的是字段/判定契约，没有测量数值。旧正文中的“本库尚无遥测来源”是旧批范围，但新材料声称复用已有 T03-03 计数器；必须用新增限定说明历史范围与当前可复用资料，不能让两种当前状态并存。

关闭条件：研究记录改成可解析的完整 ID—精确页面/评论 URL—字段/支持范围表，替换悬空代号或链接其实际定义；正文核心新主张近旁放对应证据。接入本页作者记录、T03-03/05/06/07 与实际工具资料；直接使用外部资料时复用已有登记 ID，未选工具版本/能力继续 unknown，避免混成部署组合。把“数值已填”改为“字段契约已引用、实测矩阵未交付”；在新增注记中限定旧遥测缺口为原批核对范围，当前文档来源可复用但现场机型/字段能力未证实。verification 与作者/审阅方轮次同步，不能把本轮新证据追记为作者早已完成，也不关闭 BLOCKED-1。

## 已接受内容、状态与下一轮范围

已接受：新增内容的四个 insert 块及旧判据逐字保护；两个真实 Issue 登记且旧登记字节未变；#2409 最终平台/配置修正测量的存在、无库修复版本承诺和未核验期望/计数器边界；不执行对照测试、不填本库实测数值；T03-07 引用已接通且其文档范围已通过。

| 状态 | ID / 范围 |
|---|---|
| 本轮 OPEN（6 P2） | C22、C23、C24、C25、C26、C27 |
| 既有 CLOSED（21） | C01–C21 |
| 本批累计 | 21 CLOSED / 6 OPEN（审阅发现） |
| 既有验收子项 OPEN（单列） | BLOCKED-1 |
| T03-08 | 初审未通过，修订后按上述条件定向复核 |
| T03-06/T03-07 | 已交付有限文档/来源范围通过保持；T03-06 acceptance 5 未验收 |

不因用户待审队列列出 T03-06/T03-07 而丢失已完成复核；本轮已比对其身份，没有新交付变动可重开。整个 Batch 19 未完成，后续判定需区分审阅发现、未交付/未验收子项和现场验证。

本轮仅新增本报告并更新来源审计当前入口/交付表，不改作者正文、来源记录、修订映射、索引、登记、计划或 Batch 17/18 文件。原始材料只存临时目录；无真实 GPU/NPU、MPI/collective、配置变更或故障注入，模型审阅和结构校验不建立硬件验证。


`make check` / `make build` 均 PASS（88 篇内容 / 388 项来源）。源文件输入清单确认仅本报告新增与来源审计修改，无删除；作者正文/来源记录/修订映射、索引、登记、计划、T03-06/T03-07 和 Batch 17/18 输入 SHA 不变。本地文件链接与当前状态入口核对完成；未改 src/kb，未执行 make test；无实机验证。
