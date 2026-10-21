# Batch 31 · T06-09 第一轮初审报告

## 会话元数据与结论

| 项目 | 记录 |
|---|---|
| 审阅角色 / 轮次 | 独立批次审阅者；第一轮初审；本会话不承担正文编写或问题修订 |
| 实际执行模型 / 档位 | `gpt-6.1-sol / xhigh`（本地当前会话运行记录） |
| 模型核验方法 | 按最新修改时间定位当日 rollout JSONL，以 L1 的会话 ID、cwd 和本轮用户任务核对身份；读取最新 `turn_context` 的 `model`、`effort`、`cwd` 及 `collaboration_mode.settings`，不以默认配置或历史报告替代 |
| 模型核验结果 | `model=gpt-6.1-sol`、`effort=xhigh`、`cwd=/Users/ywang2397/work/AI_reliability_knowledge_base`；`collaboration_mode.mode=default`，其 `settings.model=gpt-6.1-sol`、`reasoning_effort=xhigh`、`developer_instructions=null`；与指定一致，无模型回退 |
| 模型核验坐标 | `/Users/ywang2397/.codex/sessions/2026/10/21/rollout-2026-10-21T23-43-28-01a15f21-b9d4-7421-9a80-18dfe410cee3.jsonl` L8（最新且唯一 `turn_context`，`2026-10-21T15:43:37.023Z`）；身份记录为同文件 L1 |
| 会话 ID | `01a15f21-b9d4-7421-9a80-18dfe410cee3` |
| 执行方式 | 当前本地 Codex CLI 会话直接审阅；`originator=codex_exec`，CLI `0.163.0`；未另启模型或子代理 |
| 日期 / 时区 | 2026-10-21 / Asia/Shanghai（UTC+08:00） |
| 审阅正文 | `knowledge/06-training/index.md`，126 行（先执行 `wc -l`） |
| 正文 SHA-256 | `df7de5e6a4f2129e92321ef1feddc641611d208859ae7f1305a6d00c1ff13ef1`（随后执行 `shasum -a 256`） |
| 写入范围 | 仅新增 `docs/research/batch-31-t06-09-codex-review.md`；不修改正文、作者取证、来源登记、计划、历史报告或构建产物 |

**初审结论：需修订并定向复核，暂不通过。共 2 项发现：P1 0 项、P2 1 项（C01）、P3 1 项（C02），均为 OPEN。** 八主题的 40 个方面入口均能找到实际承载内容，主要技术限制未被导航升级；但交付核对中的缺口表述与正文、两份覆盖账本不一致，尚不能完成第 4 条 acceptance 的最终核对。

优先级口径：P1＝足以严重误导处置的关键错误；P2＝影响技术准确性、证据边界或验收判据的必修事项；P3＝局部措辞、定位与可追溯性问题。下文“正文 L…”均以本表 SHA-256 为基准，其他文件单独注明。

本轮工具输出中的 `[frontier_llm]` 出现在读取[写作指南 §7](../authoring-guide.md#7-批次审阅约定) L128 的原文引用中（rollout L47，`response_item/custom_tool_call_output`）；用户任务和本轮检索代码中也含该字面量。这些是被引用或检索的内容，不是模型运行事件。实际判据是 L8 的 `turn_context`；该事件没有模型不符，不能因引用了标记就将本轮判为回退。

## 范围与方法

先读 `README.md`、`AGENTS.md`、`docs/authoring-guide.md`（特别是元数据及 §7）、`schemas/content.schema.json` 和 `content-outline.md` L70–78、L139–152 的训练领域与跨域分工。完整读取[本批正文](../../knowledge/06-training/index.md)与[作者取证记录](batch-31-t06-09-sources.md)，以 [T06-09 objective 和四条 acceptance](../../plans/full-coverage-backlog.yaml) L7112–7159 为验收基准。

逐格核对正文 L65–72 的 8×5 表，独立打开其中全部 17 个不同正文目标，检查实际段落、表格、流程或案例内容；没有只凭链接文字、章节标题或作者声明判断。另抽查原 covered 主题的保留证据、两平台路径、T06-01～T06-08 的来源与最终复核记录，以及两份覆盖账本。下表记录每格实际检查的落点。

本轮为导航及交付审阅：没有重新抓取外部 URL，没有重新认证兄弟篇全部上游主张。技术限制的检查对象是所链正文与既有审阅记录是否被本页正确承接；历史取证限制继续保留。未执行文档中的训练、编译、保存、恢复、伸缩、profiling 或故障注入步骤；未新增来源或修改 registry。

### 五方面逐格核对的正文简称

| 简称 | 已独立打开的正文 |
|---|---|
| P | [并行策略与训练状态](../../knowledge/06-training/parallelism-and-state.md) |
| F | [训练框架组件、执行循环与平台职责对照](../../knowledge/06-training/framework-execution.md) |
| W | [预训练与微调工作流和状态契约](../../knowledge/06-training/pretraining-and-finetuning.md) |
| R | [RL rollout、权重同步与训练推理协同](../../knowledge/06-training/rl-rollout-consistency.md) |
| M | [混合精度、算子适配与收敛验证](../../knowledge/06-training/mixed-precision-and-convergence.md) |
| A | [训练性能分解、profiling 与优化验证](../../knowledge/06-training/performance-analysis.md) |
| AC | [训练吞吐回归来源案例](../../knowledge/06-training/performance-regression-source-case.md) |
| S | [慢 rank 诊断指南](../../knowledge/06-training/slow-rank-triage.md) |
| B | [通信带宽退化诊断指南](../../knowledge/03-communication/bandwidth-degradation-triage.md) |
| C | [Checkpoint 恢复一致性](../../knowledge/06-training/checkpoint-state-consistency.md) |
| E | [弹性训练与成员变更](../../knowledge/06-training/elastic-training-and-membership.md) |
| CT | [Checkpoint 恢复状态异常诊断指南](../../knowledge/06-training/checkpoint-state-recovery-triage.md) |
| CC | [Checkpoint 恢复异常来源案例](../../knowledge/06-training/checkpoint-state-recovery-source-case.md) |
| CX | [Checkpoint 恢复状态实验设计](../../knowledge/06-training/checkpoint-state-recovery-experiment.md) |
| GT | [GPU→NPU 精度差异诊断指南](../../knowledge/06-training/gpu-npu-precision-difference-triage.md) |
| GC | [GPU→NPU 精度差异来源案例](../../knowledge/06-training/gpu-npu-precision-difference-source-case.md) |
| GX | [GPU→NPU 精度差异实验设计](../../knowledge/06-training/gpu-npu-precision-difference-experiment.md) |

### 40 格实际内容核对表

以下坐标均为对应正文的当前原文件行号。每格均有实质内容；“验证”成立于方法、判据或来源案例层，不表示执行成功。

| 主题 / 本页位置 | 原理与边界 | 设计与使用 | 观测与判断 | 故障与处置 | 验证与案例 |
|---|---|---|---|---|---|
| 06.1 / L65 | F L50–79 有执行职责链；P L172–191 有九类状态责任 | P L208–263 区分截取暂态、累积、更新/overflow；W L95–126 有工作流状态与继承矩阵 | P L172–206 有 step/样本/RNG/逻辑身份；F L130–149 有观测挂点及测试断言边界 | F L114–128 按初始化、首步、更新、保存/加载、编译分流 | P L275–288 有映射、更新、吞吐、恢复判据及实现/合成示例；CX L31–47、L95–128、L149–176 有独立分支与端到端设计，未执行 |
| 06.2 / L66 | P L44–82 实际解释 DP/FSDP/TP/PP、EP dispatch/combine 和 SP/CP 差异 | P L84–170 有组合身份、约束及固定假设选型；A L100–132 有候选 A/B 与恢复 A 记录设计 | A L65–98 有工具取证界限、分 rank 证据及阻塞链回溯 | S L61–78 有诊断/停止分支；A L94、L134–152 区分 PP 空泡、EP 热点、长度偏斜和受害者 | A L154–161 有吞吐/质量/恢复联合判据；AC L32–50、L64–100 为单卡训练回归来源案例，不冒充组合并行实验 |
| 06.3 / L67 | F L50–93 有职责链和限定 compile(model) 的 eager/compiled 对照 | F L95–112 有三组独立版本、依赖、硬件及 unknown 档案 | F L130–149 列具名实现、挂点和测试/断言的有限范围 | F L114–128 有各阶段分界、连通性检查和恢复一致性检查 | F L124–128 确有未执行的小规模验证设计；方法入口成立，但“仍缺”的交付归类见 C01 |
| 06.4 / L68 | W L43–65、L95–126 区分目标/参数轴及状态契约；R L58–105 有在线循环与 DPO 离线对照 | W L107–135 有 adapter 装载、合并与阶段切换；R L109–175 有版本/数据契约、同步异步代价和失败重放规则 | W L137–142 有 token/质量/重复遗漏口径；R L177–187 列吞吐、滞后、队列及质量 | W L144–160 有异常区分和两类转换验证；R L189–196 有质量、同步、logprob 与异步退化分支 | R L198–204 有固定基线后单变量异步度/资源形态设计；L56、L228 限 legacy V0、未实测，不覆盖 V1 全流 |
| 06.5 / L69 | M L55–63 有 autocast、scaler/master 权重和三套实现边界 | M L76–84 有重复基线、单因素对照及质量必经流程 | M L65–74 将 finite、scale、更新、误差和质量分项记录 | M L76–94 有判断、停止与回退；GT L71–113 有首差异分流和 unknown 出口 | M L86、L96–105 有 #200537 来源案例及有限窗口判据；GC L29–48、L63–100 保留未闭环；GX L67–111、L140–162 有未执行对照设计 |
| 06.6 / L70 | A L50–63 固定有效产出、配置和重叠时间口径 | A L65–74 有应用/系统工具对照及不可得材料边界 | A L76–98、L134–143 有阶段/rank 证据、完整性门禁、受害与最早瓶颈区分 | S L61–91 有诊断和完成出口；B L55–79、L88–103 有口径、配置、链路与对照分支 | A L92–98、L154–161 有冻结状态、单因素、A/B/恢复 A 与双指标；AC L52–87、L100–106 保留 main/发行版、作者报告/本库未复现之别 |
| 06.7 / L71 | C L58–80 有状态覆盖与一致截取；E L35–54 有 rendezvous、成员变化与失败语义 | C L82–148 有保存/装载观察点、Megatron 职责和支持/不支持/未知表；E L56–93 有副本机制及有限对照 | C L82–96 明确 Future、读取、回调、对象装载、首步和持续窗口的不同完成点 | CT L63–101 有诊断步骤、strict、布局变化、停止和恢复安排 | C L150–171 有验证分层/容差；CC L36–40、L64–87 保留 CPU 与 fresh-object 未证实；CX L95–128、L172–184 为未执行设计 |
| 06.8 / L72 | C L47–80 有恢复目标、逻辑进度和状态契约；L165–171 区分离散精确与浮点规则 | C L150–163 按身份/结构→逻辑进度→状态内容→单步→持续窗口→回退设计 | C L165–171 给比较规则；CT L44–61 给恢复点、schema、对象应用及继续训练证据 | CT L63–114 有最早异常、对象后处理、数据/RNG、持续偏离的分流与判据 | C L150–171 实际提供分层方法；CX L95–128、L149–184 有 CPU 优先端到端、rank-local 和三值判据，不验证 GPU/NPU 或 world-size 变化 |

## 已核实的主链与边界

| 核对对象 | 结果与采信边界 |
|---|---|
| 原 covered 06.1 | 本页 L65/L90 的状态责任、单步边界、观测、故障分界、验证方法均有上表证据。原保留的[训练全流程](../../knowledge/00-overview/training-lifecycle.md) L91–103 仍区分执行与提交、保存与续训；P、C、CT 的保留证据未被新职责图替代成更强保证 |
| 原 covered 06.7/06.8 | 本页 L71–72/L90 所述分层验证有 C/CT/CX 实质内容。对照 [T06-08 最终复核](batch-26-t06-08-codex-recheck.md) L27–53，历史 C01–C05 已关闭，mid-step、外部 whl、完整 load/resharding 与配套 unknown 继续保留 |
| 重分片限制 | C L140–146 分别列 DCP 条件、Megatron 重分片未知、MindSpeed 仅 DP 缩扩/一次缩容、MindIO 一致性门和 torchrun 的应用状态责任。本页没有将这些行压成“统一支持重分片” |
| MindIO TTP 临终保存 | C L148、E L73–81 保留 A+K、ZeRO-1/DP、副本、严格多数、分片一致性、级联故障限制，以及直接写持久存储、保存后结束进程；未与 ACP 异步暂存路径混同。历史复核另用同版本 PDF 补证并保留 HTML 取回限制，本轮没有冒称重新取得 HTML/PDF |
| 框架与 RL 版本 | F L48、L95–112 的 PyTorch 2.6、core_v0.19.2、MindSpeed-LLM v2.2.0 互不拼装；MindSpeed 配套 Mcore 为 core_v0.12.1。R L56/L228 的 verl v0.9.1 是 legacy V0 结构样板，V1 控制流未知。本页中性入口及 L61/L92 未将其改写成任意实现可用 |
| 原理/设计与结果 | 所链训练正文全部 `draft`；两篇独立实验为 `not_verified`，案例是来源整理。M 的 dtype 案例没有整训质量证明，AC 是单卡性能证据、修复 release 未核；CC 是 CPU 来源且原脚本未证明 fresh-object 恢复。导航未把这些材料称为本库复现 |
| 跨域与平台入口 | [昇腾路径](../../paths/platforms/ascend.md) L78–98、L134–158 和 [NVIDIA 路径](../../paths/platforms/nvidia.md) L63–87、L106–132 继续链接主归属内容。本页 L97–99 保留 02 算子语义、03 通信、04 持久化、06 训练状态、07 rollout 服务分工；没有复制全文。[持久化正文](../../knowledge/04-data-storage/checkpoint-durability.md) L49–71、L100–108 仍将存储与训练验证分开 |
| 元数据与本地链接 | schema/日期校验通过；稳定 ID 与 Git HEAD 均为 `training.index`；`type=index`、`domain=training`、`status=draft`、`platforms=[generic]`。3 个来源 ID、22 个 related ID 均存在；95 处相对链接、25 个不同目标全部存在。三项原始资料外链与登记 URL 一致，来源为资料入口，不代替兄弟篇固定技术证据 |
| 保留章节一致性 | “已有正文”“场景指南、案例与实验”“内容边界”与新表的承担关系基本一致；慢 rank 专用案例/实验仍标待补，不能由通用性能案例自动认定补齐。交付小节及“成果与后续”的缺口归类、实验份数另见 C01/C02 |

### 前置任务的来源、修订和复核记录核对

下表确认记录存在并读取对应来源/unknown、修订段和最终复核结论，不重新批准历史所有主张。各报告只在其声明范围内通过；历史实际模型字段（包括 `unknown`）保持原样，本轮不替历史运行补作身份认证。

| 任务 | 来源 / 缺口与修订记录 | 最后复核及保留范围 |
|---|---|---|
| T06-01 | [来源记录](batch-24-t06-01-sources.md)，unknown L51–59、修订至 L130–142 | [第六次定向复核](batch-24-t06-01-codex-recheck-6.md) L5–9 关闭唯一余项；另有 [Batch 24 交付后复查链](batch-24-source-audit.md) L40–45，原状态矩阵/轴序等按后续修订口径读取 |
| T06-02 | [来源记录](batch-24-t06-02-sources.md)，unknown L57–64、修订至 L146–148 | [第四次定向复核](batch-24-t06-02-codex-recheck-4.md) L3–18 关闭余项；当前 F 的小规模验证方法与未执行边界见 L124–128 |
| T06-03 | [来源记录](batch-24-t06-03-sources.md)，unknown L44–52、修订至 L147–149；早期文字需与后续更正合读 | [第四次定向复核](batch-24-t06-03-codex-recheck-4.md) L3–17 关闭余项；质量等价/新目标基线、adapter-only/完整恢复仍分开 |
| T06-04 | [来源记录](batch-25-t06-04-sources.md)，unknown L57–65、修订至 L94–97；R L228 列当前剩余 unknown | [第四份定向复核](batch-25-t06-04-codex-recheck-4.md) L3–18 记录累计 15 项关闭；不把 V0 样板变成 V1 或实际平台组合已验证 |
| T06-05 | [来源记录](batch-25-t06-05-sources.md)，unknown L40–47、修订至 L65–67；后续状态机订正优先于早期未知描述 | [第三份定向复核](batch-25-t06-05-codex-recheck-3.md) L9–25 记录累计关闭；有限窗口、跳步分子分母/未确认事件、私有插桩边界保留 |
| T06-06 | [来源记录](batch-25-t06-06-sources.md)，unknown L37–45、修订至 L66–68；A L169 列当前工具缺口 | [第四份定向复核](batch-25-t06-06-codex-recheck-4.md) L8–14 记录累计 8 项关闭，并明确 06.2-G3 内容审阅阻塞已消除、未代改账本；性能结果仍未执行 |
| T06-07 | [来源记录](batch-25-t06-07-sources.md)，unknown L30–37、修订至 L56–59；“次生 issue”等旧措辞已由后续订正 | [第三份定向复核](batch-25-t06-07-codex-recheck-3.md) L18–25 关闭剩余同步项；AC L81–106 仍保留修复 release、同条件复测和质量缺证据 |
| T06-08 | [来源记录](batch-26-t06-08-sources.md)，unknown L46–54；C/E 当前状态、调用边界及未知项与之合读 | [定向复核](batch-26-t06-08-codex-recheck.md) L27–57 关闭 C01–C05，纠正初审整除方向误读，明确 HTML/PDF 补证边界；CPU DCP/精度方案保持未验证 |

这些来源及复核材料确实存在，不构成“前置任务没有审阅记录”的发现；问题是本批交付核对未把它们与实际缺口账面对应起来，见 C01。本批来源记录 L29–35 的待回填修订/复核段是首轮初审阶段的正常占位，不能预先当作本批已闭环。

## 逐项发现

### C01 · P2 · 保留缺口归类与正文及两份账本不符，最终交付核对遗漏账面差异

- **位置**：正文 L67、L86–93，重点 L91；“成果与后续”L126；本批取证记录 L20、L26。
- **问题**：本页把“06.3 具体工作负载与执行验证”“06.4 受控异步实现样板”一并写成“已登记范围缺口”，但没有区分已交付的方法、尚未执行的结果和仍未取证的特定实现。与此同时，本页未列出 backlog 仍为 open 的其他训练内容缺口与主题盘点/历史闭环的差异。这不满足第 4 条 acceptance 的最终核对要求；不是要求为导航任务补做真实实验。
- **证据**：
  1. [主题盘点](../../plans/topic-coverage.yaml) L778–809 将 06.3、06.4 均记为 `covered`、`gaps: []`；L762–877 中八个训练主题也全部为 covered、空 gaps。[backlog](../../plans/full-coverage-backlog.yaml) L2307–2313 的 `06.3-G3` 已 `closed`，T06-02 L5829 明确验收的是“小规模执行路径验证方法”。F L124–128 实际已有连通性与恢复一致性设计，并明确未执行。目标工作负载的执行结果确实尚无，但不能由此把已关闭的方法缺口重新描述成已登记的内容缺口。
  2. R L145–153 已有同步、一步异步、完全异步 legacy recipe 的机制/预算/边界，L198–204 有单变量异步度验证设计；[T06-04 最终复核](batch-25-t06-04-codex-recheck-4.md) L6 明确任务在既定范围通过。当前保留的是 V1 控制流、具体组合等 unknown 与未实测，不能笼统写成“受控异步实现样板待补”。
  3. backlog 仍有 **9 项 `closure_lane: content / status: open`**：`06.2-G3`（L2249–2256）、`06.4-G2/G3`（L2354–2369）、`06.5-G1/G2/G3`（L2408–2430）、`06.6-G1/G2/G3`（L2468–2490）。它们与主题盘点的空 gaps、T06-04～T06-07 的 `done` 及最终复核存在账面差异。本页只给两项笼统“保留缺口”，没有逐项说明这些 open 是未同步、仍有剩余内容，还是等待最终验收；本报告也不擅自选择其中一种解释。
  4. 本页 L90 只称“按当轮审阅记录”，取证 L14–15 只称“Batch 24/25 各轮审阅”“Batch 26 审阅闭环记录”，未给对应报告位置；不能用这些概括替代任务→来源/缺口→修订/最终复核的可定位核对。八主题的 `content_acceptance_status: planned` 以及 T06-09 自身 planned 在初审阶段本身正常，不能机械当作缺陷或直接改为 accepted。
- **建议修订**：在本页及本批取证中准确区分“已有设计/来源样板”“未执行结果”“特定实现/平台 unknown”；将 06.4 的 legacy V0 已交付范围和实际剩余条件写准。逐项记录上述 9 项账本差异，并提供前置任务来源、修订及最终复核的可定位链接。后续账面处理应依据对应关闭证据，不能仅因导航有链接就机械关闭，也不能把未实测等同于内容方法未交付。
- **关闭条件**：读者可由交付核对明确判断每一项是真实内容/来源缺口、验证未执行，还是待处理的账面差异；06.3 已有方法与 06.4 V0 样板不再被误报为缺失；9 项 open 全部有与两份账本、任务和复核记录相符的说明。差异未处理前明确不作最终覆盖通过判断；无需新增硬件结果。本轮审阅者不代改正文或账本。

### C02 · P3 · “三份实验设计”未能对应本章实际条目

- **位置**：正文 L93；关联 L78–84。
- **问题**：“三份实验设计”没有给出三个对象或统计口径，读者无法与场景表及内容目录对应。
- **证据**：本章 `type: experiment` 仅有 GX 与 CX 两篇，分别对应本页 L80/L81；两篇实际结果节分别在 GX L151–155、CX L172–176，均明确未执行。L82 的慢 rank 专用实验仍待补，L83 复用 GX，L84 指向 A 的内嵌验证方法。R、F、A 另有内嵌设计，CX 也分三个独立实验部分，但本页未说明“三份”是其中哪一种口径。
- **建议修订**：若统计独立条目，改为实际两篇；若统计内嵌设计，逐项命名并给定位、解释与两篇条目的关系，避免让慢 rank 的待补项看起来已有交付。
- **关闭条件**：实验数量与明确列出的对象一致；复用、内嵌方法、独立 experiment 条目可区分；全部实际未执行状态继续保留。

## 四条 acceptance 的逐条判断

| 条款 | 初审判断 | 依据与限制 |
|---|---|---|
| 1 · 八主题各有五方面实际正文入口 | **满足入口内容要求** | 40 格均已逐格检查，有正文承担；同文复用成立，验证列不以实际执行为本轮通过前提 |
| 2 · 原 covered 06.1/06.7/06.8 五方面与 T06-08 边界 | **满足本轮导航复核范围** | 保留状态矩阵、完整 step 边界、支持/不支持/未知、临终约束与分层验证；历史复核记录确实存在，未升级其取证/硬件边界 |
| 3 · 主归属、稳定 ID、不复制全文、generic 非兼容 | **满足** | 两平台路径继续链接主目录；`training.index` 未变，跨域内容只引不复制，draft/generic 限制明确 |
| 4 · 所有任务来源/缺口及修订复核的最终核对 | **未满足，C01 必修；C02 需修正交付计数** | 前置任务来源及闭环记录存在，但本批对缺口的归类不实，未交代 9 项 open 与其他账面/历史结论的差异，不能据入口齐全声明最终覆盖 |

## 校验、写入与结论

已执行 `PYTHONDONTWRITEBYTECODE=1 make check`，结果 **PASS：126 content entries / 575 sources**；另核对目标元数据、3 个 source refs、22 个 related IDs、全部本地链接及稳定 ID。结构检查不验证远程内容、技术正确性或平台兼容。

遵守本轮“只新增报告、不改构建产物”的明确范围，未执行 `make build`；未改 `src/kb/`，未新增测试或运行 `make test`。本轮没有进行任何真实环境验证。

开始时工作区已有 `knowledge/06-training/index.md` 的修改和未跟踪的 `docs/research/batch-31-t06-09-sources.md`，均为审阅输入，不归为本轮改动。报告写入前后对 675 个既存仓库文件（含 build 现存文件）进行 SHA-256 对照，既存文件无变化、无删除；本轮仅新增本报告。正文交付时仍为 126 行及头表所列 SHA-256。

**T06-09 需修订并定向复核。** 编写者处理 C01–C02 后，由同一审阅者按关闭条件复核交付核对、表格相关行、取证记录及账面解释，不能以一次结构检查或入口数量代替关闭判断。本结论只覆盖编辑、导航和证据边界，不替代真实训练、恢复、性能或平台验证。
