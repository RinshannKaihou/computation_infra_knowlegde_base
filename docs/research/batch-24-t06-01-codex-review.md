# Batch 24 · T06-01 Codex 技术审阅报告

- 审阅日期：2026-10-18。
- 结论：**暂不通过**。
- 发现：**P1 0 项、P2 7 项、P3 2 项，共 9 项，均为 OPEN**。存在 OPEN P2，不能声明本任务审阅通过。
- 执行者：本会话 Codex，技术审阅角色；未派发子代理，未修改正文、导航、来源登记或计划。
- 模型记录边界：本会话未提供可独立核验的实际模型标识、推理档位及路由元数据，记为 `unknown`；不把导航中的 `gpt-6.1-sol/xhigh` 声明当作本轮实际模型证明，也不声称完成写作指南第 7 节的模型路由验真。本报告记录实际完成的内容审阅，不虚构额外 CLI 审阅轮次。

## 1. 审阅范围与方法

### 1.1 输入与基线

已读取 `README.md`、`docs/authoring-guide.md`、`content-outline.md`、`schemas/content.schema.json`，并按写作指南第 7 节区分来源核对、报告交付、修订及定向复核。

本轮对象：

| 对象 | 范围 |
|---|---|
| 任务 | `plans/full-coverage-backlog.yaml` L5832–5879 的 T06-01，全文读取 `objective`、五条 `acceptance`、`source_packages`、`existing_source_ids`、`source_discovery`、`context_topic_refs`、`targets` |
| 正文 | `knowledge/06-training/parallelism-and-state.md` L1–212，含既有内容与所有新增小节 |
| 作者取证 | `docs/research/batch-24-t06-01-sources.md` L1–106 |
| 来源登记 | `sources/registry.yaml` 中正文引用的全部 11 个来源条目；额外核对正文引用的 PyTorch 后端实际登记 URL |
| 导航 | `knowledge/06-training/index.md`；检查正文关联的通信、存储、训练恢复页面及已有回链 |
| 修订基线 | Git HEAD `bce9d978f58d71e180e46ca81069a152fb646ea0` 与审阅开始时的工作树差异，不把本轮原有未提交改动归为审阅者修改 |

任务目标是保持单篇主归属和稳定 ID，在既有状态责任矩阵上补齐 DP/ZeRO/FSDP/TP/PP/EP/CP 的机制、通信与选型。任务来源工作包为 A05/A10/A18/S21/S25，既有来源为 PyTorch parallel-training-state、DCP 与 MindSpeed-LLM HA；`context_topic_refs` 为 01.4/03.1/03.3/03.6。`source_discovery` 要求分别锁定 Megatron 与 MindSpeed 资料，按需核对 AMD/ROCm，不能混成支持组合。计划中 `status: planned`、`readiness: needs_source_preparation`、`source_revision: null` 是已观察到的计划状态，本轮不替作者推进状态。

正文审阅快照 SHA-256：`5c29923c0971f2caea0a9b6285019487610e4bd9993a4f944cd2643d9890b0a3`。

### 1.2 独立重开与判定尺度

1. 从正文精确 URL 出发，GitHub `blob/<ref>/...` 以同一 ref 的 `raw.githubusercontent.com` 文件独立重开；版本化 PyTorch 页面直接取回，不用搜索摘要替代正文。
2. 使用只读 HTTP 请求取回字节，记录 HTTP 状态与 SHA-256。原始文件按 LF 行坐标核对，不使用网页工具的转换行号拼 GitHub 锚点。未安装或执行上游训练代码。
3. 共核对 36 个 URL：正文中的 31 个不同 URL，以及来源登记/取证记录关联的 README、VPP、模型表、安装指导与正确的后端页。35 个返回 HTTP 200；正文后端 URL 返回 HTTP 404，见 C08。附录 U01–U36 保留本轮取回清单。
4. 网页阅读工具初次读取 MindSpeed 脚本及 DDP 页返回内部错误，随后直接 curl 均为 HTTP 200，已完成独立重开；不把工具内部错误误记成上游页面不存在。
5. 固定 raw 文件的哈希与作者记录可比时一致，包括 EP dispatcher/utils、两组 arguments、DeviceMesh、CP、训练循环和 MindSpeed 特性文档。PyTorch TP HTML 本次哈希与作者所记不同；HTML 字节差异不单独证明技术内容变化，本轮按实际取回内容核对，不以哈希不同直接判错。
6. 厂商吞吐表只核对“存在该来源记录及其配置”，不当成通用性能结论；合成内容按静态约束检查，不伪造启动结果、日志或故障复现。正文未引用具体上游测试文件，本轮也未把源码静态阅读说成测试通过。

## 2. 发现表

位置中的“正文”均指本轮 `knowledge/06-training/parallelism-and-state.md` 快照；U 编号对应附录的精确上游文件。所有条目的关闭均要求作者修订后定向复核，不能仅以结构校验通过关闭。

| 编号 | 优先级 / 状态 | 位置 | 发现与证据 | 建议关闭条件 |
|---|---|---|---|---|
| B24-T061-C01 | P2 / OPEN | 正文 L101–115，尤其 L103、L107–109 | **选型表没有完成“固定设备拓扑及候选配置”的验收，且混入无依据的性能泛化。** 64 张同构卡不等于固定节点数、节点内/间互联及放置；没有逐行给并行度、micro-batch/累积数，无法解释 PP bubble 或扩展效率。L107 把梯度 all-reduce 写为“随卡数线性增长”，未定义总字节、每 rank 字节或时延；又断言“64 卡下通信占比高”。L109 的“每层两次”“通常组内 ≤8”没有所选实现/拓扑依据。U01 只支持 DDP 梯度同步职责，不能推出这些性能结论；U03 支持 TP API/布局，但不提供通用 8 卡上限。U02 对参数/梯度/optimizer 全分片明确限定 `FULL_SHARD`，表中笼统的 FSDP/ZeRO 行也应保留相应策略边界。 | 补齐明确标“合成”的固定拓扑、可比较的模型/精度与候选并行配置、micro-batch/累积和适用实现；将全分片行限定到有证据的策略，或补分阶段 ZeRO 来源。删除无依据的线性增长/8 卡/通信占比断言，或定义指标、限定实现并给精确来源；无测量的效率保持分析预期或 `unknown`。 |
| B24-T061-C02 | P2 / OPEN | 正文 L82–88 | **组合身份“样例”实际上只有字段清单，缺少可核算映射。** 只给 64 ranks、TP2/CP2/PP2/EP4，没有任一具体 global rank 的 mesh coordinate、有序组成员及组内 rank、stage/layers、expert 集合、FQN/shard offset，也没有 DP/expert-DP。U15 L381–408 的 mesh 示例有实际 rank 布局；U12 L479–482、L859–895 分别建立 dense 与 expert rank grid，不能把 EP/CP 简单当成同一个额外正交维度。现有段落无法据此核对 rank→expert→shard 是否自洽。 | 给一个完整、明确标“合成”的具体映射实例，说明 rank 排列、dense-DP/expert-DP、expert-TP 和 EP/CP 关系，列出至少一个进程的全部实际身份值及对应组成员；展示覆盖/唯一性、组内编号和 shard 归属冲突检查。静态推导不写成已成功启动。 |
| B24-T061-C03 | P2 / OPEN | 正文 L86 末句、L188；与 L140–151、L191 衔接 | **把原布局完全相等误写成恢复正确性的必要条件。** “任何一项在 checkpoint 与重启后不一致……就会错位”以及组成员/stage/expert 与 checkpoint“不一致即布局错位”，会把合法重分片或 rank 重编号也判为故障。U24 的 DCP `get_state_dict` 明确限定其支持范围内可跨 trainer 数/并行方式重分片；正文原有 L151 也保留了这一边界，L191 又要求检查改变并行度后的加载。新增判据与原文发生实质冲突。 | 区分同布局原样恢复与有支持证据的布局转换：前者比较原映射，后者验证旧→新逻辑身份/覆盖/唯一性及受支持的重分片结果，而非要求物理 rank/placement 相同；未受支持的第三方转换继续 `unknown`。同步修改 L86、L188，与 L151、L191 保持一致。 |
| B24-T061-C04 | P2 / OPEN | 正文 L88、L96、L204 | **性能 warning 被纳入“不通过即拒绝启动”的硬约束表。** U07 L1413–1435 中 Hopper 及以前的 TP/CP 与 MoE overlap 分支调用的是 `warn_rank_0`，并说明可按优先级选择连接设置；不是该分支的拒绝启动断言。正文 L68 的“不建议”接近来源，但表格总述和 L204 的“冲突”升级了语义。 | 把硬断言、功能不支持、性能建议/warning 分栏或分表；将该行明确写成条件化性能提醒，不声称必然拒绝启动，保留硬件代际与配置条件；定向复核实际分支而非只核对参数名称。 |
| B24-T061-C05 | P2 / OPEN | 正文 L97、L204；对照 L68、L80、L94 | **整除关系写反，GQA 条件还漏掉一个分支。** U07 L1600–1603 是 `num_experts % EP == 0`，L204 却说“专家数必须整除 EP”。U13 L247–253 要求 heads 可被 ulysses×TP 整除、query groups 可被 TP 整除，L97 的两处“须整除”方向相反；U13 L255–263 进一步要求未启用 KV head repeat 时，query groups 也可被 ulysses×TP 整除，表格没有说明。 | 统一改用不会歧义的取模等式/“被……整除”表述，补齐 GQA 的 KV head repeat 条件。用源码静态代入核对至少一组满足与一组不满足的合成值，不能把这些代入写成训练测试。 |
| B24-T061-C06 | P2 / OPEN | 正文 L155–172，尤其 L161、L163–170、L172 | **“合法跳步”被收缩为 checkpoint 中可不保存哪些暂态，没有覆盖真正的 no-update/overflow 跳步及计数分叉。** U20 L355–365 明确 inf/NaN 时不调用 optimizer 更新，L467–480、L613–614 仍有 scaler 更新及保存边界；U27 L2474、L2503、L2518–2531 区分更新成功、scheduler 推进与 skipped iteration，L3941–3942 则另行推进已消费样本。现有表没有说明尝试迭代、成功更新、scaler、scheduler、数据提交/重放之间的关系，无法满足验收中执行边界与合法跳步的要求。 | 将“合法不更新/不推进”与“合法不序列化暂态”分开，按选定实现说明累积尚未提交、overflow/no-update、成功更新三类边界，以及各逻辑计数、scheduler/scaler 与数据进度是否推进；应用层 data commit 没有来源的部分保留为显式恢复契约/`unknown`，不从 sampler 或样本计数反推。 |
| B24-T061-C07 | P2 / OPEN | 正文 L195，引用 L103 的“同一合成场景” | **合成反例没有隔离待证明约束，且凭空确定绕过校验后的故障表现。** 在固定 64 ranks 下取 CP6，已不能满足 U07 L422–431 的 world-size 整除约束，会先违反该约束；不能把首个拒绝点直接归到 L1295–1298 的序列断言。这是源码顺序与整数关系的静态核对，不是启动日志。后半句既说“不会表现为显式报错”，又说会有“形状错误或静默错位”，而未读绕过后的完整执行路径、未做复现，来源只能证明合法性断言，不能证明这种必然故障模式。 | 选用其余前置约束可满足的合成配置，明确只验证所针对的约束；或说明 CP6 同时违反多项约束，不归因到单一首次报错。删除绕过后的确定性现象，改为行为未核实/`unknown`；如需具体故障结论，另补固定实现证据或经授权的实验记录。 |
| B24-T061-C08 | P3 / OPEN | 正文 L115 的 `distributed backend` 链接；`sources/registry.yaml` L3575–3588 | **AMD/ROCm 边界指向不存在的版本化页。** 正文 URL `https://docs.pytorch.org/docs/2.6/distributed.backend.html` 本轮 HTTP 404（U17），而 `src.pytorch.distributed-backend-2.6` 实际登记的是 `distributed.html`，本轮 HTTP 200（U35）。**未能独立重开（精确正文 URL 返回 HTTP 404）**；不能用相邻页面替代并声称原链接已核实。这里不据 404 判定 AMD/ROCm 技术语义对错。 | 换成实际重开、与登记一致且支持所述边界的精确 URL/章节；如果要新增具体 ROCm 支持语义，另外核对相应官方一手页面，不能仅用泛后端名称推定。 |
| B24-T061-C09 | P3 / OPEN | 正文 L64 的 dispatcher 主语 | **把 router 的目标选择职责归给 dispatcher。** U05 L618–640 的 `dispatch_preprocess` 接收已经产生的 `routing_map` 与 `probs`，后续按映射排列并通信；U05 L698–716 执行 A2A，不能支持“`MoEAlltoAllTokenDispatcher` 先按概率选出目标专家”的职责归属。作者复用的登记条目也明确具体路由由调用方决定。其余关于非 fused tokens/probs 形状、TP>1 combine 前 RS 与 split 交换，已重开 U05/U06 核对。 | 改成 router 先形成路由/概率、dispatcher 消费该映射完成重排与通信；若要展开 router 的选择/均衡算法，应另给该固定 tag 的 router 实现证据，不从 dispatcher 推导。 |

## 3. 分节主张—证据抽查

下表记录“实际抽查了什么”，不把其中一条成立扩张为该节无误。源码/文档有效与正文表达准确分别判定。

| 正文小节 / 位置 | 独立重开与抽查点 | 判定 |
|---|---|---|
| 导言与“并行改变了什么”，L40–58 | U01 DDP 输入切分归应用、梯度 all-reduce 和参数更新；U02 `ShardingStrategy.FULL_SHARD`；U03 TP 只接受 1-D submesh；U04 pipeline 的 stage/micro-batch 与 alpha 标记 | 原有核心概述得到支持；不支持新增表中的无条件性能规律 |
| 专家并行，L60–68 | U05 L372–383、L618–640、L698–716、L817–826、L857–862；U06 L423–467；U08 L16–18、L28–45 | dispatch/combine、tokens/probs 形状和实例参数基本有据；路由职责见 C09，硬/软限制见 C04 |
| SP/CP/TP，L70–80 | U03 `SequenceParallel` 的参数复制与序列维输入分片；U09 导出面；U11 L1222–1247 的 experimental CP、SDPA patch、buffer 切分；U14 Ring Attention 与 FlashAttention 前提；U13 L242–286 | 区分方向基本成立；实际约束必须保留 GQA 分支，见 C05。PyTorch CP 在 NPU 的可用性未获证明，继续 `unknown` |
| 组合身份与冲突检查，L82–99 | U15 L381–408；U12 L479–491、L859–907；U07 L562–567、L997–1009、L1295–1298、L1413–1435、L1600–1603；U10/U31 特性约束 | 来源有具体映射/条件，但正文样例与判定不足，见 C02–C05 |
| 固定假设选型，L101–115 | U01/U02/U03 机制边界；U16 的 Llama2-7B 32k TP2/PP1/CP4 来源表；U33 的 VPP 16 层 TP1/PP4/VPP2 示例 | 厂商表确实存在，不是本库结果；固定拓扑及配置比较不完整，见 C01。AMD 原链接见 C08 |
| 状态责任矩阵，L117–136 | U18 optimizer parameter ID 装载不额外验证；U19 scheduler 独立状态；U20 L599–614 的 scale/tracker 与更新后保存；U21/U22/U23 的 RNG 与 sampler 语义 | 既有核心内容保留并有来源支撑；没有发现把 seed/epoch 升格为精确 worker 恢复保证 |
| 超过 global rank 的身份，L138–151 | U24 `get_state_dict` 的 canonical FQN、目标对象与支持范围内重分片 | 原有边界成立，但新增 L86/L188 与之冲突，见 C03 |
| 截取边界，L153–157 | U20 L613–614；U04 schedule 与 micro-batch 暂态；U30 保存 wrapper 的外部依赖边界 | 原段落保留；通用 mid-step 协议维持 `unknown`，没有补造跨框架格式 |
| 单步所有权与合法跳步，L159–172 | U25 forward/backward schedule；U27 更新成功/跳步分支；U28 L113–124 的 distributed optimizer；U20 scaler skip/update | 角色分解有基础，但未完成合法 no-update 与提交计数语义，见 C06。U26 的 autograd/图释放不单独证明 checkpoint 梯度可省略 |
| MindSpeed 样板，L174–182 | U29 L5、L18、L72–84；U30 L210–213、L253–279；U32 依赖表；U36 L56–71；U10/U16/U31 | HA/DP、外部 `generate_state_dict` 边界、PyTorch 2.7.1 与 Mcore core_v0.12.1 档案得到支持；未把它们拼到 PyTorch 2.6 或 core_v0.19.2 上 |
| 验证判据与示例，L184–195 | U24 支持范围内的重分片；U08 官方脚本；U34 L3 的 Pass/Test 定义；U07 两类断言 | 检查类别与官方脚本存在；布局判据及合成反例有问题，见 C03/C07。认证分级是来源口径，不是本库认证 |
| 常见误解，L197–206 | U01 的副本边界、U20 scaler、U23 sampler、U07/U13 整除与 warning 条件 | 既有误解段保留；新增 EP 整除方向、硬/软冲突应随 C04/C05 修订 |
| 适用边界与待确认，L208–212 | U32/U36 依赖档案；作者取证 unknown 清单；U24 重分片范围 | `generic` 不作兼容声明、未做硬件实验、厂商数字非通用预期等说明保留。没有发现虚构本地事故史或执行结果 |

## 4. 任务验收逐条核对

| 验收条目 | 核对结果 | 未关闭项 |
|---|---|---|
| 1. EP dispatch/combine、专家负载与通信；CP/SP 与 TP 使用实现精确来源 | **部分满足**。EP A2A/RS、非 fused 形状和 PyTorch CP 源码已独立核对；有实现来源，不是只写概念名 | C05 的约束错误影响组合条件；C09 的路由职责待澄清。负载不均会影响工作量，但本轮没有测量证明其在任意环境都是“首要”长尾来源 |
| 2. 固定模型/序列/全局 batch/设备拓扑，比较状态内存、通信、bubble、偏斜与扩展效率，无无条件最优 | **未满足**。有合成模型、序列、global batch 和卡数，但没有固定拓扑及逐行候选配置；若干性能断言超出来源 | C01；厂商实例仅按来源记录接受，不作为表格通用性能证明 |
| 3. 组合 global/group rank、mesh、stage、expert、shard 身份样例及冲突检查 | **未满足**。字段目录存在，完整实际值样例缺失；检查表混淆 warning/硬拒绝，整除关系有误 | C02、C04、C05；恢复映射检查还须按 C03 区分支持的布局转换 |
| 4. forward/backward/accumulation/optimizer/scaler/data commit 边界、所有权与合法跳步 | **部分满足**。既有状态矩阵和截取边界保留，新增阶段表覆盖名目；合法 no-update 与各计数推进契约未完成 | C06；不能以 sampler epoch 或已消费样本计数替代应用 data commit 的证明 |
| 5. 映射、梯度/更新、吞吐扩展、负载与恢复判据；一个有来源实现例和一个明确合成反例 | **部分满足**。判据类别、GLM4.5-MoE 官方脚本与明确“合成”标识均存在；判据及反例技术内容尚需修正 | C03、C07；实现例是静态脚本配置，不代表本地运行成功或恢复验证 |

`source_discovery` 另记：已核对三组独立固定版本档案，不混用版本；MindSpeed 核心仓外链、上游测试执行、目标 NPU 组件配套、CP 在 TorchNPU 的实际可用性仍未独立验证。本轮不把这些未知项写成支持组合；AMD 精确链接缺口按 C08 处理。

## 5. 元数据、导航与既有内容保全

- 稳定 ID 仍为 `training.parallelism-and-state`，`type: concept`、`domain: training`，只有一个主归属；没有为新增 EP/CP 内容复制第二篇主干。
- 标题与 H1 一致；`status: draft` 保留。`updated_at: "2026-10-18"` 与本轮日期一致，不是未来日期。
- 11 个 `source_refs`、3 个 `related_ids` 及 6 个 `verification.evidence_refs` 均可解析到已登记对象；无悬空 ID。对正文引用到但未单列的页面，继续按已登记来源的覆盖范围核对，不把引用 ID 存在视为证据已经充分。
- `verification.status: source_checked` 及“未运行训练/保存/加载/GPU/NPU 实验”的声明没有被升级为 `reproduced`；本报告的 OPEN 问题说明若干具体表述仍需修订，不认可将整个新增范围笼统宣称技术核验完成。
- 导航 L42、L64–65 指回同一正文，`related_ids` 含稳定 ID；通信文档和 checkpoint 恢复一致性文档有回链。正文到通信、持久化、恢复一致性及两轮取证记录的本地链接存在。没有因本轮审阅改写其他 Batch 24 条目。
- 与 HEAD 基线逐节比较：**状态责任矩阵、超过 global rank 的身份章节完全不变**；**原截取边界与 MindSpeed 样板文本均完整保留，只追加内容**。原有五条“常见误解”也未删除。保全并不自动保证新增段落与它们一致，C03 是本轮发现的衔接冲突。
- 来源条目区分固定 raw、版本化 HTML 与未核验外部依赖；未引入新的整体再分发许可，报告只记录定位与原创判断，没有搬运上游整段代码、图或性能表。

## 6. 结构检查与写入范围

本轮实际执行：

| 检查 | 执行位置与结果 | 能证明什么 |
|---|---|---|
| `PYTHONDONTWRITEBYTECODE=1 make check` | 原工作树，退出 0：103 content entries / 489 sources | Schema、ID、引用、本地 Markdown 文件目标；不检查远程 URL 或技术结论 |
| `make build` | `/private/tmp/b24-t061-review/snapshot` 隔离副本，沿用现有项目解释器，退出 0：103 entries / 489 sources；生成仅落在临时副本 | 可生成目录及元数据清单，不是训练/恢复验证 |

隔离副本最初只复制纳入工作树清单的文件，遗漏被 Git 忽略但当前工作树已有的 `build/catalog.json`、`build/catalog.md`，首次 build 的链接预检因此退出 2。补拷贝这两个已有生成文件以还原原工作树输入状态后，重跑成功。此过程没有修正文或构建脚本，也没有把首次失败隐去或作为 T06-01 技术发现。

没有改 `src/kb/`，未运行 `make test`；没有执行上游脚本、训练、分布式初始化、checkpoint 保存/加载、主动硬件诊断或性能实验。原仓库 `build/` 不重写。唯一新增的仓库文件为本报告。

## 7. 结论与关闭规则

**T06-01 本轮暂不通过。** 已确认原 ID、原状态责任矩阵、身份和截取边界主体得到保全，关键固定源码可重开，版本隔离及多数 unknown 声明合理；但选型比较、可核算组合映射、合法重分片判据、硬/软约束、整除方向、合法跳步和合成反例存在 7 项 OPEN P2。

作者应按 C01–C07 修订，C08–C09 也建议一并关闭；随后由审阅者读取改后正文与对应精确上游位置定向复核。未有复核记录前不得改称通过。即使之后所有审阅发现关闭，也只表示来源与文字边界的审阅通过，不证明硬件兼容、吞吐收益或恢复正确性。

## 附录：本轮独立取回索引

以下 URL 均是本轮实际读取目标；GitHub raw 保留正文的同一 tag/commit。SHA-256 为实际响应字节摘要，U17 的摘要只标识 404 响应，**不构成有效技术证据**。精确源码行号在正文发现表与分节核对中给出，HTML 使用 API/小节名定位。

| 编号 | 实际取回 URL | HTTP | SHA-256 |
|---|---|---|---|
| U01 | `https://docs.pytorch.org/docs/2.6/generated/torch.nn.parallel.DistributedDataParallel.html` | 200 | `234b86e52bb85067e3c5181af8725e1fc21db09340dba974eaa42cace7ac7c37` |
| U02 | `https://docs.pytorch.org/docs/2.6/fsdp.html` | 200 | `a5ea697c5c73a839564c56cf2a1439ab33ee77193935eefa11eae5e66d5d6e45` |
| U03 | `https://docs.pytorch.org/docs/2.6/distributed.tensor.parallel.html` | 200 | `3389b2834a94f140b3e94cc5fea2191adcf791bd6d27a0bbee05abab46d7512d` |
| U04 | `https://docs.pytorch.org/docs/2.6/distributed.pipelining.html` | 200 | `523b998dca942362f0942489e7a090a92986f3dda29084328a6e46ccedc215ea` |
| U05 | `https://raw.githubusercontent.com/NVIDIA/Megatron-LM/core_v0.19.2/megatron/core/transformer/moe/token_dispatcher.py` | 200 | `7af2746153268f5c5f7f03d7a340092541b633fbc8faa10f666d6ddbdf98be0a` |
| U06 | `https://raw.githubusercontent.com/NVIDIA/Megatron-LM/core_v0.19.2/megatron/core/transformer/moe/moe_utils.py` | 200 | `b20192e71b54ed07b00f9e3d0bbd7daf470cb9ea3dc3037c20f544528e56f14f` |
| U07 | `https://raw.githubusercontent.com/NVIDIA/Megatron-LM/core_v0.19.2/megatron/training/arguments.py` | 200 | `f7fad20bc0e0cd9ba4b9ba7e70fa1a1b77030dfd020a7edb50b1d3b3aa41ebf6` |
| U08 | `https://raw.githubusercontent.com/Ascend/MindSpeed-LLM/v2.2.0/examples/mcore/glm45-moe/pretrain_glm45_moe_106b_4k_A3_ptd.sh` | 200 | `5f065dbb1adb044c1224c4826653a56c8c1d0f581bd009c12d51d47403d3a028` |
| U09 | `https://raw.githubusercontent.com/pytorch/pytorch/v2.6.0/torch/distributed/tensor/parallel/__init__.py` | 200 | `877f1578fe013f22d37aea8665a971442123dc0be5eca7741a3c9ba341bdc058` |
| U10 | `https://raw.githubusercontent.com/Ascend/MindSpeed-LLM/v2.2.0/docs/pytorch/features/tensor_parallel_2d.md` | 200 | `fcc3dab563fcf7205e75b1be8b192b25260a33e370ef3953690ada3f635bd164` |
| U11 | `https://raw.githubusercontent.com/pytorch/pytorch/v2.6.0/torch/distributed/tensor/experimental/_attention.py` | 200 | `325e6a434113d42ae4742545bb926215b8a8f7013bf0348091088b7c3ae3fb12` |
| U12 | `https://raw.githubusercontent.com/NVIDIA/Megatron-LM/core_v0.19.2/megatron/core/parallel_state.py` | 200 | `1f6e23a01022c06be3b67f930095898e5032f6ff93695f8da5aae3b5a546dcf0` |
| U13 | `https://raw.githubusercontent.com/Ascend/MindSpeed-LLM/v2.2.0/mindspeed_llm/training/arguments.py` | 200 | `fd64204269ad1749159d9b98f47c91f92cb17de5075cb92670f8ab1d5df42a38` |
| U14 | `https://raw.githubusercontent.com/Ascend/MindSpeed-LLM/v2.2.0/docs/pytorch/features/ring-attention-context-parallel.md` | 200 | `c15aa4faecb39cdb9c28bf9bd00f6c2e980180671d62a40f3ab106db5b7304bf` |
| U15 | `https://raw.githubusercontent.com/pytorch/pytorch/v2.6.0/torch/distributed/device_mesh.py` | 200 | `d16e1975093c53fd6e5415adf6c3f98093b7a03cc8123b905f5c8dfa13246012` |
| U16 | `https://raw.githubusercontent.com/Ascend/MindSpeed-LLM/v2.2.0/docs/pytorch/features/fine-tuning-with-context-parallel.md` | 200 | `f899c7292961f6c5cd69eb9e46ccb9e2099c9c86e9fb5ca7fbcd77cb810bdc51` |
| U17 | `https://docs.pytorch.org/docs/2.6/distributed.backend.html` | 404 | `9a2651e9b6d2ec25319835c5f01e8eeb733e69ebdcddf815083a15132f50baec` |
| U18 | `https://docs.pytorch.org/docs/2.6/generated/torch.optim.Optimizer.state_dict.html` | 200 | `e4e63f4c2257ad7d78e98b63af9c34573a032db497acd3f3c316efd5eeb2f8af` |
| U19 | `https://docs.pytorch.org/docs/2.6/generated/torch.optim.lr_scheduler.LRScheduler.html` | 200 | `d59ac56af42a697bdcd7228ebd25e468b95e6afd3b5416ef015369edd9bcdbd7` |
| U20 | `https://raw.githubusercontent.com/pytorch/pytorch/1eba9b3aa3c43f86f4a2c807ac8e12c4a7767340/torch/amp/grad_scaler.py` | 200 | `eb4bc91fda9815ba40206e2dbb68f9845b85622fee3a92611f227b5845b20780` |
| U21 | `https://docs.pytorch.org/docs/2.6/random.html` | 200 | `219fc921e1e15bd28ecf2fd20f5be678c79dac742a5be9d2a766e41a09c95367` |
| U22 | `https://docs.pytorch.org/docs/2.6/notes/randomness.html` | 200 | `efca3c65f678c434a2f170dee424c13771f459119fe707d3924aebf29f224b5c` |
| U23 | `https://docs.pytorch.org/docs/2.6/data.html#torch.utils.data.distributed.DistributedSampler` | 200 | `8ac5a162de9adc1c4ab3a7ce304adc59735ae32049b39e3f1e1720a44e4a01cf` |
| U24 | `https://docs.pytorch.org/docs/2.6/distributed.checkpoint.html` | 200 | `0621220c541154c2a344ba9f1d7f77bc6db8062456c27f02c9d23011f960960f` |
| U25 | `https://raw.githubusercontent.com/NVIDIA/Megatron-LM/core_v0.19.2/megatron/core/pipeline_parallel/schedules.py` | 200 | `9d3624f4b1bc8e9e4747f339587b3dab2560e0fc5faa9fecd736e4eed2d5f1b7` |
| U26 | `https://docs.pytorch.org/docs/2.6/notes/autograd.html` | 200 | `42a3e5996f330bc7ac19de17bfd116e784e9e556fb2d3f821e3acbdb146f61bc` |
| U27 | `https://raw.githubusercontent.com/NVIDIA/Megatron-LM/core_v0.19.2/megatron/training/training.py` | 200 | `d968ef8216f63d6373372190ac895fc905234c116bba3e804d2951876e6ad98c` |
| U28 | `https://raw.githubusercontent.com/NVIDIA/Megatron-LM/core_v0.19.2/megatron/core/optimizer/distrib_optimizer.py` | 200 | `40cae307ccb2a3f484ebd5d28ee8549eb572d1b0ba6e91dc5661c137bf560907` |
| U29 | `https://raw.githubusercontent.com/Ascend/MindSpeed-LLM/53f3639c3da9c000a187c44cc0c08d55026ddded/docs/pytorch/features/high_availability.md` | 200 | `83b6b6d8e3590f0ea158b0d6f40f22606c466dfbf19db6c344246cd55b68ca9f` |
| U30 | `https://raw.githubusercontent.com/Ascend/MindSpeed-LLM/53f3639c3da9c000a187c44cc0c08d55026ddded/mindspeed_llm/training/checkpointing.py` | 200 | `beaa6057ac72f74fbc0fe1e2a82a9f6acc5c34e3591d6f526b6fcce5f4535069` |
| U31 | `https://raw.githubusercontent.com/Ascend/MindSpeed-LLM/v2.2.0/docs/pytorch/features/mc2.md` | 200 | `1de465bde728e1d51c49df2341d3df7f7fd6985c2183928d5767e76023585e5e` |
| U32 | `https://raw.githubusercontent.com/Ascend/MindSpeed-LLM/v2.2.0/README.md` | 200 | `7b4893c93e8884d18eb0ff5eee5291bd93eced52dd91572d6a2566c4a7b12f99` |
| U33 | `https://raw.githubusercontent.com/Ascend/MindSpeed-LLM/v2.2.0/docs/pytorch/features/virtual_pipeline_parallel.md` | 200 | `126e2895b8f4499d72185d7dc47acc4e2aadf20f6cc4f92a02118b5cecb740c3` |
| U34 | `https://raw.githubusercontent.com/Ascend/MindSpeed-LLM/v2.2.0/docs/pytorch/models/moe_model.md` | 200 | `5119b6e207cf832844478be4665ddd544c53c01886ccef2d814f756666a0653a` |
| U35 | `https://docs.pytorch.org/docs/2.6/distributed.html` | 200 | `fa9373af30052007a27baa648bd652e2dc15e6d1954b636bcc3ee14d9944a1b7` |
| U36 | `https://raw.githubusercontent.com/Ascend/MindSpeed-LLM/v2.2.0/docs/pytorch/install_guide.md` | 200 | `8dd60a6cc0983ffcf1e1aaa84da2cba054d1362a7b53a6bffacd665c0bdad423` |
