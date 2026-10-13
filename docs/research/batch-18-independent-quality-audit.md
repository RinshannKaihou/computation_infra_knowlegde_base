# Batch 18 独立质量归因复审

评审日期：2026-10-10。执行者为本次新派发的独立评审子代理，此前未参与 Batch 18 撰写、初审或复查；本子任务显式配置为 `gpt-6.1-sol / xhigh`。配置说明不替代可独立核验的运行元数据。本报告审查初稿和原评审的准确性，不修改作者正文、来源登记、历史报告或任务状态，也不建立硬件验证结论。

**可以确认：Batch 18 初稿的交付完整性和证据核对存在明显不足，四项任务当时都未达到自己的原验收条件。** 初审 15 个 ID 中，14 项的核心问题有初稿或一次源依据，1 项（C01）的主要反证是评审误读。首次修订另引入 C16，后续没有新增 ID。多轮未通过还包含修订未落实、修订引入的新错误和记录同步问题，不能全部归因于初稿，更不能据此证明 Muse Sparks 1.3 导致质量下降。

## 1. 初稿可以恢复，归因不依赖现行正文

已读 [AGENTS](../../AGENTS.md)、[README](../../README.md)、[写作指南](../authoring-guide.md)、[内容边界](../../content-outline.md)、[T03-01–T03-04 原验收](../../plans/full-coverage-backlog.yaml)，以及初审、四次定向复核、修订映射、来源审计与四份作者研究记录。下文文件行号均注明所指版本。

Batch 18 三篇新文未提交，集合文的 HEAD 版本早于本批扩展；因此仅用 `git show HEAD` 无法还原本批初稿。但只读 `git fsck --no-reflogs --unreachable` 找到的未引用 blob 中，四篇初稿及四份初始研究记录的 SHA-256 **全部与初审报告 L17–29 完全一致**。以 `git cat-file blob <对象>` 取出后，直接读了这些初稿；临时提取位于 `/tmp/b18-independent-snapshots/`。未恢复到工作树，也未修改 Git 对象。

| 快照 | 初稿正文档案 / 对应研究记录 | Git blob | 初审输入 SHA-256 |
|---|---|---|---|
| I1 | [互联路径初稿](quality-audit-snapshots/batch-18/interconnect-paths.md.txt) | `923b701d636cbc7af5937e2c4c9f926d4c7662ab` | `f74324f886837041fc3ca111093b24663fe5e6e944a21eabce902a4b52910d58` |
| I2 | [RDMA 机制初稿](quality-audit-snapshots/batch-18/ethernet-ib-roce-rdma.md.txt) | `d9c98878d5781af9472cef45a5005f9baa33582b` | `65fed21af7eebdc86fe683d7abba6d08855e9d6daf772d25973066b84be06ac4` |
| I3 | [RDMA 基线初稿](quality-audit-snapshots/batch-18/rdma-baseline-and-congestion-triage.md.txt) | `a2f83e7108c050a0b078800a2e73bc3c064f3aa0` | `93cf4c7b31a2161b22dd7aa4fd7952a8f2bf1b88aefbcd20aebee10da9e43cae` |
| I4 | [集合扩展初稿](quality-audit-snapshots/batch-18/collectives-and-rank-progress.md.txt) | `93fe80b5f82308da9ba9b4fea96c0e05946a169e` | `a4405d656a3095afd883833ebede40b9c9cfb74aeec33f15dfd684ebcd38dc1e` |
| S1 | [互联研究记录](batch-18-interconnect-paths-sources.md) | `80cf8cf7c647ed251602ddb92664a4bfaadeb9d6` | `4df879cab7d70ca436659f6cbd6843031b95112ee305f6a82e1b7d3bd2fbc627` |
| S2 | [机制研究记录](batch-18-rdma-mechanism-sources.md) | `747dd421e893721b74e951d6ba793f7e79a8fc78` | `c691a823e24ab31c959a72e0bc1275c72cba11524675d281b11171195f80a4ad` |
| S3 | [基线研究记录](batch-18-rdma-baseline-sources.md) | `36a9cfedd54eddb4bf3647917db16421efb3bdb6` | `4f4d1c08f24d18103d29278dcc0b5cbd26251bdf85010db7166d4d6fd218fc55` |
| S4 | [集合研究记录](batch-18-collectives-extension-sources.md) | `2c5b0739c468eafb51f62e40217fd6e1e9b98db0` | `ed53bf15a3703ce08a10721b8e1f32de1df47c39a5e79f5811d7badee944c9a7` |

I1–I4 行号直接对应以上正文档案；S1–S4 链接指现行研究记录，所称初始 S 行号须按本表 blob 恢复，不对应后来追加节。主助手已将四篇正文原始字节存为 `.md.txt` 历史证据，并提供[档案说明](quality-audit-snapshots/README.md)与[清单](quality-audit-snapshots/manifest.json)。这些是“初审输入”的精确恢复，未证明它们是写作模型最早一次输出或未经集成者修改的输出。未归档的研究/修订对象未来仍可能被 Git 清理，临时目录也非永久证据库。

一次源核对复用了 `/tmp/b18-review-evidence` 至 `/tmp/b18-fourth-recheck-evidence` 的固定源码、HTML 和论文。实际重读了 CANN 表格单元格、DGX Table 5/6、verbs man/完成实现、perftest README/参数/host 校验实现、UFM 指标、OFED ECN/流控、Thakur/Patarasuk 公式页及冻结 Megatron mappings/P2P/dispatcher/permute。另只读打开 DOCA 3.5.0 与 Cumulus 4.3 精确页面核对 RR/通知和双模式；没有把全部远端链接声明为本轮重抓。

## 2. 去重计数和多轮轨迹

以 ID 为计数单位；一项可包含多个子问题。下表“通过修正关闭”与“误读撤销”分别统计，避免把 C01 的关闭计成作者修复成功。

| 历史轮次 | 当轮新 ID | 累计 CLOSED / OPEN | 本轮变化 |
|---|---:|---:|---|
| [初审](batch-18-codex-review.md) L5 | 15 | 0 / 15 | 14 P2、1 P3，包含后来撤销的 C01 |
| [第一次复核](batch-18-codex-recheck.md) L7、L58–64 | 1 | 7 / 9 | C01 撤销；C02/C07/C08/C09/C11/C15 修正关闭；新增 C16 |
| [第二次复核](batch-18-codex-rerecheck.md) L7、L39–42 | 0 | 11 / 5 | C03/C05/C06/C16 修正关闭 |
| [第三次复核](batch-18-codex-third-recheck.md) L7、L49–50 | 0 | 13 / 3 | C04/C13 修正关闭 |
| [第四次复核](batch-18-codex-fourth-recheck.md) L5、L76–77 | 0 | 13 / 3 | C10/C14 仍 P2；C12 技术主体接受，剩记录笔误 P3 |

15+9+5+3+3=35 是各轮 OPEN **状态出现次数**，不是 35 个独立缺陷。累计 16 个 ID 的归因是：**初稿核心成立 14；评审主要反证错误 1；首次修订新增 1**。13 个 CLOSED 内含 1 个误读撤销、12 个经修正关闭；最后 3 个 OPEN 的现行剩余原因也不相同。

为便于计数，按初始主因分为互斥类别：8 个事实/机制语义错误或关键条件遗漏（C02/C05/C06/C07/C09/C10/C11/C13），4 个必交范围遗漏（C03/C08/C12/C14），1 个版本/证据状态不足（C04），1 个编辑/链接问题（C15），1 个评审误读（C01），1 个修订新错误（C16）。C10/C12/C14 等还包含其他类别的子问题；上述不是把全部子问题强行视为同质，更不是 8 个完全独立的错误机制。

## 3. 逐唯一 ID 的独立归因

“原范围内”指原 acceptance 或为避免已写主张错误所需的细化，不包括补造现场结果。下表的“成立”只确认核心问题，不默认认可原报告所有措辞或优先级。

| ID | 初稿/修订直接依据 | 独立判定与后续来源 | 原验收关系、最终轨迹 |
|---|---|---|---|
| C01 | I1 L80 的“全系”、L88 的计划 | **原主要反证不成立，评审误读。** 原始 CANN HTML 六行 Supported 均为 √；斜杠在产品列。原稿“全系”措辞仍宜按产品族/RC Note 收窄，但不能据该表否定训练产品支持。 | 合理要求适用边界；“训练行不支持”错误，第一次撤销。详见案例 A。 |
| C02 | I1 L68 把单 CX 卡与双 OSFP 端口关联 | **成立：初稿事实错误。** DGX 八张单端口计算网卡、模块内重复 CX 编号不能合并；Table 5/6 可直接反证。 | T03-01 故障域/资产核对原范围；第一次关闭。 |
| C03 | I1 L45 称路径图已整理，L60–88 仅表/段落/工具组合 | **成立：必交图、资产关联和判据未交齐。** 初稿也已误述 topo/BDF 与 nvlink 两端字段（L70）；首次修订的实线/逻辑边矛盾属于修订影响。 | 两份图/核对表/最小计划是 T03-01 L4725 明文；第二次关闭。未要求填造 Ascend 未公开边。 |
| C04 | I2 L28/35/59/105 的对版状态，I3 L27/86/90 的待固定；S2/S3/S4 L3/7/15 | **成立：版本绑定未完成且核对状态不清。** 源码主页、浮动内核入口和候选版本不能证明固定语义已核对；后续 tag 选定后 verification 仍待定是同步问题。 | 固定来源是原要求；第三次关闭。第二次仅剩同步矛盾仍列 P2 偏保守，不应继续描述为尚未选 tag。 |
| C05 | I2 L55 未分 WRITE_WITH_IMM 的 RR/通知，L93 混注册与远端错误 | **成立：机制关键条件遗漏/阶段混淆。** WRITE_WITH_IMM 需远端 RR，通知与普通 WRITE 不同。首次修订又将 INLINE 例外明确置于接收 buffer（修订稿 L82）。 | T03-02 参与者/完成原范围；第二次关闭。CPU 不在数据搬运路径这句话本身不能作为错误，重点是 RR/通知条件。 |
| C06 | I2 L95 未给通知策略，L96 用发起侧 byte_len 统一观测 READ/WRITE | **成立：观察字段与通知边界错误。** 固定 mlx5 WRITE/SEND 成功分支不赋 byte_len；signaled 属 SQ。首次修订将 signaled 写到远端接收完成，是修订错误。 | T03-02 完成/错误语义原范围；第二次关闭。 |
| C07 | I2 L68 无条件写 RoCE 必需 PFC+ECN | **成立：条件泛化。** 已选 Cumulus 4.3 同时有 lossless 与 lossy RoCE；不能把前者条件外推全部网络。 | 工作负载/软硬件条件原范围；第一次关闭。 |
| C08 | I2 L46–48 是文字“图”，L70–80 缺实际比较，L101 仅称留待另一轨道 | **成立：必交图/比较/普通链接遗漏。** PD 不能当租户隔离、NPU 能力未知等边界本来正确，不能把这些正确的 unknown 也当错误。 | T03-02 L4761/4763/4764 原范围；有限隔离样板是合理细化，第一次关闭。 |
| C09 | I3 L43 泛称计数器只经 sysfs/不进以太网；L52/65 混 IB 工具和 RoCE 路径 | **成立：driver 与硬件/交换机层次混淆、路径缺口。** OFED 限定的是 offload 绕过 Ethernet driver，不否定物理 NIC/交换机指标。 | T03-03 分开 IB/RoCE 原范围；第一次关闭。 |
| C10 | I3 L53 未展开逐指标语义，L61“零增量计数器”，L77 正常响应/错误未分 | **成立：指标判读有实质问题且必交字段缺失。** 后续 Packets 单位、Constraint 单因解释、配置当统计及 ECN 参数路径错误分别来自修订；不是每轮新初稿缺陷。 | T03-03 L4802 明文要求字段单位/方向/累计范围；第四次仍缺传输重试/ECN/交换机字段，P2 OPEN 有依据。 |
| C11 | I3 L68 三选项全部互斥、外部 taskset 优先、cycle counter 无上下文切换 | **成立：初稿语义写反/扩大。** README 明确只有两对互斥，显式参数覆盖外部绑定；计时取样省开销不证明进程无切换。 | NUMA/测量口径属于原设计前提；第一次关闭。详见案例 C。 |
| C12 | I3 L54/61 的零 errors 门禁、L62 无尺寸/选择规则、L27 无有限硬件样板 | **核心成立：覆盖与可判读设计不完整。** 初审对扫描互斥指控过强；后续 1000 默认、统计聚合、跨粒度比值、研究 >0/==0 都须分期归因。 | T03-03 L4803–4804 原范围；技术主体第四次接受，仅研究记录笔误 P3 OPEN。详见案例 D。 |
| C13 | I4 L97–105 未完整定义符号/条件，ring 近似式当等式 | **成立：有限 p 因子与假设遗漏。** 初稿 Rabenseifner reduce 式并非误标 all-reduce；其 ceil 是首次修订后来引入，不能倒算初稿。 | 代价模型及假设是 T03-04 L4842 明文；第三次关闭。 |
| C14 | I4 L73–91 无要求的原创图/all-to-all 数据流，L111–119 浮动实现/消息缺口 | **成立：必交映射与冻结证据未交齐。** PP 无条件 shape 先行已在初稿；is_single_shape、TP 函数/阶段误配、EP 公式不展开、AG/排序误绑分别是后续修订问题。 | T03-04 L4841/4843 明文；逐对 shape/dtype 是合理细化；第四次剩 AG 条件 P2 OPEN 有源码依据。详见案例 E。 |
| C15 | I1 L70 与 L92 URL 不一致；I4 L121 H2 和说明拼接 | **成立：编辑/链接问题。** 本次直接确认路径不一致和标题拼接；历史 404 依初审 L191 的获取记录，未重演当时网络。 | P3 比例合适；第一次关闭，不足以单独解释技术性整批退回。 |
| C16 | 初次修订互联稿 L89 新写 Slot3 为 BlueField/DPU | **成立：首次修订引入无证资产类型。** 初稿 I1 无这一判断；DGX 原表只有该槽位接口身份与组件规格。 | 修订影响核对，非新增验收目标；第二次关闭。 |

## 4. 五个有辨别力的案例

### A. C01：错误来自审阅者，不能归为写作模型的技术错误

I1 L80 把适用表概括为 A2/A3 全系，原审阅 L51 则断言训练行 Supported 是 `/`。本次重新按 `tr/td` 解析初审保存的 CANN HTML 与首次复核 canonical HTML：两份均 12307 B，SHA-256 都是 `e0fbe17136873bafe7fac1352eb8fc06b0347df5ebaf556d640025c6a0844f39`，六行支持列均为 √。A2/A3 训练与推理名称在同一产品单元格，用斜杠连接。这个反证不存在，不能归因页面更新，也不能把“合并行没有训练单列”当另一种否定证据。[CANN 900 原页](https://www.hiascend.com/doc_center/source/en/CANNCommunityEdition/900/API/runtimeapi/aclcppdevg_03_1895.html)

原审阅者在[第一次复核](batch-18-codex-recheck.md) L36–40 明确认错并撤销，后来初审顶部、该发现节、来源审计均有纠错；后续也没有重开它。纠错是充分且必要的，但不能抵消初次错误给作者带来的转录/分歧处理成本。初稿的“全系”仍比逐产品/形态条件粗，应作为范围表述问题看待，不能保留原“训练不支持”的 P2 归因。由于 T03-01 另有 C02/C03，撤销 C01 不改变该任务初审未完成的结论。

### B. C02 与 C16：初稿资产误判、修订新误判是两件事

I1 L68 明写单 CX 卡共享双 OSFP 端口，错误关联 Table 6 的重复局部编号。独立核对 DGX 原表，模块 1 的 CX0 对应 GPU7/`dc:00.0`/`mlx5_11`，模块 0 的 CX0 对应 GPU3/`5e:00.0`/`mlx5_5`；组件说明明确是八张单端口计算网卡。这是阅读原表时应当避免的身份合并错误，修正会实际改变共享故障域判断。[DGX 指南组件表、Network Specifications、Table 5/6](https://docs.nvidia.com/dgx/dgxh100-user-guide/introduction-to-dgxh100.html)

首次修订解决了 C02，却在新增摘要 L89 把 `irdma0/1` 推为 BlueField/DPU。该修订稿可恢复为 blob `daa04017bf9eb6512d55a53a2e95b1fb2181d60a`，SHA-256 `baeb7010643badee287705e8075c027b2563ec22d369b65a6d6804f31f3cd7ff`；初稿没有此类型断言。因此 C16 的新增是合理修订影响发现，不是初稿第 16 个错误，也不是评审追加新产品要求。第一次复核关闭 C02 并另记 C16，第二次关闭 C16，这个分开记法较公平。[第一次复核](batch-18-codex-recheck.md) L59、L134–140

### C. C11：取证后的短句压缩把规则写反，不能用“诚实 unknown”解释

I3 L68 的全互斥与 taskset 优先，与同 commit README L391–396 直接冲突；参数实现 L2463–2471 只拒绝 numa_node 与另两项的两种组合。这不是无法取得证据，而是已选来源里的明确规则被错误概括。它会使测试记录的 CPU/内存放置与实际显式绑定不一致，初稿就应修复。[固定 perftest README](https://github.com/linux-rdma/perftest/blob/a31f9ea9df720ee68f941e55f75fec31349fcd35/README#L376-L401)、[固定参数检查](https://github.com/linux-rdma/perftest/blob/a31f9ea9df720ee68f941e55f75fec31349fcd35/src/perftest_parameters.c#L2463-L2471)

第一次就接受修正并关闭，无持续重开。初始作者 S3 L11 将“NUMA/校验”列为已定位主题，但不提供这条规则的逐项核对，这说明来源主题已收集与正确形成正文仍有距离。证据支持本批写作/集成核对失败，无法再分配给某一个具体模型调用。[基线研究记录](batch-18-rdma-baseline-sources.md)初始 S3 L9–15、[第一次复核](batch-18-codex-recheck.md) L63

### D. C12：一条 OPEN 下先后出现不同原因，不是一个初稿错误反复“发现”

初稿把 errors=0 纳入 G0/健康判断，却未体现校验覆盖不足的影响，工具 README L483–489 明说资源竞争会导致跳过/陈旧工作和覆盖下降，故核心发现成立。原 T03-03 也要求消息大小、隔离/争用对照和预期判据，I3 的“小/中/大”和未选硬件样板不够完整。[固定 README 校验性能与覆盖限制](https://github.com/linux-rdma/perftest/blob/a31f9ea9df720ee68f941e55f75fec31349fcd35/README#L472-L490)、[原验收](../../plans/full-coverage-backlog.yaml)

但初审 L161 的扫描互斥说法应降调：I3 L45 **已经明确 validation 与 -a 互斥**，L61 **已经说单点和全扫分开记**。可以说执行表没有清楚指定性能扫描与校验各轮的门禁，不能说初稿完全忽略互斥，或断定作者提出了同一命令组合。此子指控偏强，不足以撤销 C12 的其他缺口。

后续轨迹应按引入期拆开：

- 首次修订已收窄 errors=0、区分扫描/校验，但设计值和后端条件未交齐；第一次复核 L108–114 继续 OPEN 是原范围缺口续存。
- 第二轮加“默认 1000”和未明确 BW 原始统计/跨轮聚合，第二次复核 L76–78 才指出 WRITE BW 实际默认 5000、BW 没有单轮 median；这两条新增错误不在初稿中。[参数默认选择](https://github.com/linux-rdma/perftest/blob/a31f9ea9df720ee68f941e55f75fec31349fcd35/src/perftest_parameters.c#L1030-L1031)、[默认常量](https://github.com/linux-rdma/perftest/blob/a31f9ea9df720ee68f941e55f75fec31349fcd35/src/perftest_parameters.h#L105-L106)
- 第三轮研究记录 L35 新增 `(skips+stale)/iters` 门禁。host 源码 skips 是 marker 步，检查工作累计按 ops_per_chunk 增长，BW iters 又乘 QP 数，直接混除确有粒度问题；无数据检查量的失败分支也必须保留。要求正确解释作者新写的比值是必要核对，不是要求普适覆盖阈值。[host 跳步与累计](https://github.com/linux-rdma/perftest/blob/a31f9ea9df720ee68f941e55f75fec31349fcd35/src/host_validation.c#L585-L695)、[无数据失败](https://github.com/linux-rdma/perftest/blob/a31f9ea9df720ee68f941e55f75fec31349fcd35/src/perftest_resources.c#L7360-L7363)
- 第四轮正文门禁已被接受；现行[研究记录](batch-18-rdma-baseline-sources.md) L40 却把 `chunks_validated>0` 写成 no-data 失败，与源码 `==0` 失败相反。这是低级同步笔误，P3 与“技术主体已接受”的说明恰当；不应再称正文校验流程失败。[第四次复核](batch-18-codex-fourth-recheck.md) L42–50

因此 C12 的四轮 OPEN 既包含初始设计缺口，也包含后来两次技术修订错误及一次记录笔误。不能把后面三类全算为初稿质量；也不能由后期一个字符错误推断此前技术复查全属苛求。最后这个 P3 本身不应成为“正文仍有重大技术错误”的证据；同期 C10/C14 的 P2 足以解释整批仍未通过。

### E. C14：验收确实要求消息映射，源码存在与语义读对仍是两回事

I4 L75 称“下图”，实际 L77–82 只是六条文字，还缺单独 all-to-all 数据流；L111–119 用 latest、宽泛量级和 ep_size 代替完整消息映射。这些与 T03-04 L4841/4843 的原创图和 DP/TP/PP/EP 原语/消息大小/组要求直接对应；保留缺口是诚实的，宣布交齐则不成立。[T03-04 原验收](../../plans/full-coverage-backlog.yaml)

冻结 tag 后，首次修订把 `is_single_shape` 当 shape 先行依据；该函数 L131–137 只检查 Python 参数，实际 shape 通信 L322–328 才依 `variable_seq_lengths or mtp_standalone` 分支。第二轮又把 `_ScatterToSequenceParallelRegion` 混到 sp2hp/hp2sp all-to-all。上述都是在修订表中可以直接定位的错误，不能只因 raw 文件取到 HTTP 200 就关闭；也不是让作者覆盖所有配置。[冻结 PP 实现](https://github.com/NVIDIA/Megatron-LM/blob/core_v0.19.2/megatron/core/pipeline_parallel/p2p_communication.py#L131-L137)、[实际 shape 分支](https://github.com/NVIDIA/Megatron-LM/blob/core_v0.19.2/megatron/core/pipeline_parallel/p2p_communication.py#L322-L328)、[ScatterToSequence 实现](https://github.com/NVIDIA/Megatron-LM/blob/core_v0.19.2/megatron/core/tensor_parallel/mappings.py#L280-L297)

第三轮 EP 仍是未展开的函数式，probs 的一维结构未核算；第四轮已接受 tokens/probs 逐对字节和 combine 反向 split，剩余正文 L148 却把 `num_local_experts>1` 附在 AG 上。独立重读 dispatcher：L734–744 的 AG(tokens/probs) 仅要求 TP>1，L750 才按本地 expert 数判断排序。例如 TP=2、单本地 expert 仍有两次 AG，漏写条件会改变通信组/消息映射。这是修订新误配，当前 P2 有依据。[AG 实际分支](https://github.com/NVIDIA/Megatron-LM/blob/core_v0.19.2/megatron/core/transformer/moe/token_dispatcher.py#L734-L750)

这里使用的 dispatcher SHA-256 是 `7af2746153268f5c5f7f03d7a340092541b633fbc8faa10f666d6ddbdf98be0a`，与原第三/第四复核一致。原复核允许明确限 TP=1、将未核定分支记 unknown，且已接受字节式不重验；这说明后期要求可以在有限配置内关闭，而非不断扩成全实现穷举。[第四次复核](batch-18-codex-fourth-recheck.md) L66–70

## 5. 对原评审质量与“多轮打回”的判断

原审阅的多数核心发现与原验收吻合。两份物理图、RDMA 数据路径图、有限网络指标与测试设计、六类 collective 图和 DP/TP/PP/EP 消息映射都在开始前已写入 acceptance；本报告没有找到足以将后续轮次整体解释为“评审越过原验收不断加题”的证据。对作者已经写出的公式、比值、函数条件检查正确性，是合理细化。收窄未取得的 Ascend 边、device 校验、padding/实际路由值等范围，原复核实际允许保留 unknown，不要求补造硬件结果。

原评审仍须承担三种校准责任：

- **反证准确性：** C01 是明确误判，不能因为后来纠错就从评审质量账上消失。纠错应进入统计，不能算作者修复。
- **指控强度：** C12 对扫描互斥的叙述忽略初稿已有提醒，应描述为执行表分轮/判据不清。C05 也应聚焦 RR/通知遗漏，不将“远端 CPU 不参与数据搬运”本身判错。
- **剩余严重度与收尾：** C04 在第二次仅剩当前 metadata 同步时仍沿用 P2，较保守，可考虑 P3；C12 第四次已降 P3且明确正文接受，这种区分应保留。统计上沿用同 ID 是正确去重，但同 ID 内缺陷已经换代，摘要如果只报“3 OPEN”仍不足以解释究竟卡在初稿、技术修订还是一处研究记录。

已有记录逐轮列出接受子项、输入 SHA、剩余条件，并在第二次起确认 T03-01/T03-02 有限范围通过；C01 的全套纠错和 C12 的技术主体接受说明，能解释大部分状态变化。其不足是没有专门汇总“初稿问题与修订新问题”的归因账，容易把 OPEN ID 的续存误读成初稿持续制造新缺陷。本报告补的是这项归因，不抹去历史状态。

对多轮持续的更直接解释是：第一轮修订补了大量形式交付，却留下精确字段/配置条件；后续修订又出现 INLINE/SQ-RQ、ceil、统计分母、PP/TP/EP 分支等新误配；C10 的必交测量字段则一直缺证。**初稿不足、修订核对不足、评审的一次明确误读共同存在，不能用一个因素包办解释。** 没有逐轮耗时或每项修改工时，无法量化三者各贡献多少等待成本。

## 6. 关于模型切换，证据能支持到哪里

用户说明 Batch 17/18 切换为 Muse Sparks 1.3，本报告将其作为可信的写作流程信息。S1–S4 的初始记录只写任务、日期、来源/unknown，并无每一取证、起草、集成和修订步骤的可核验模型身份；原审阅也把配置约定与执行运行元数据分开。因此不能把某一次来源选择、哪一轮错误修订或集成核对直接锁定为同一模型生成。

证据强度分别为：

| 结论 | 强度与限制 |
|---|---|
| 本批初审输入确有明显可避免的质量/完整性问题 | **强。** 四篇初稿精确恢复，14 个核心发现成立；缺要求的图、待 drafting 占位、已选来源规则写反、未标近似的公式，都能直接定位。 |
| “只是正常补几个细节，因此大量打回全不合理” | **不支持。** 删除 C01 后仍有 13 个 P2 核心问题；至少各任务必交范围或实质语义未达标。 |
| “每轮未通过都是初稿质量差” | **不支持。** C16 和多项同 ID 后续错误是修订引入，C01 是评审错误，C12 最后是记录同步笔误。 |
| “原评审完全正确，没有过强措辞/优先级问题” | **不支持。** C01 明确误读；C12 子指控偏强，C04 后期严重度可以下调。 |
| “切换 Muse 导致相较旧模型下降” | **无法证明。** 缺同题、同来源包、同验收、同审阅程序的对照，也缺逐步骤生成身份；只能确认切换后这个批次发生了这些问题。 |

Batch 13–16 也有初审未通过与多轮复核：[Batch 13](batch-13-codex-review.md) L3/7、[Batch 14](batch-14-codex-review.md) L17、[Batch 15](batch-15-codex-review.md) L8、[Batch 16](batch-16-codex-review.md) L11。主题、正文篇数、证据难度与发现分组不同，原始发现密度不能充当模型因果证据；本次未为它们做同样的初稿复原归因审计，不给出“下降百分比”。

最直接的流程修正是让交付前检查覆盖原 acceptance 的图/表/有限样板，把“drafting 前固定”留在研究待办而非交付正文；对高风险的规则压缩、公式和源码条件做逐项主张核对；复核状态同时标“原缺口续存/修订新错/评审撤销/记录同步”，并在只剩同步问题时重新评估优先级。这些建议由本批已定位问题导出，不要求增加实机验证或全配置穷举。

## 7. 本报告的交付边界

仅新增本报告。没有修改四篇正文、四份研究记录、修订映射、来源、历史报告或任务；没有执行 perftest、verbs、集群或硬件操作。独立 source 核对不等于本地运行成功。`make check` / `make build` 由本次主助手统一执行，报告不提前宣称检查通过。
