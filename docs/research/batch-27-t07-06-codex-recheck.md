# Batch 27 · T07-06 第一轮定向复核

## 会话元数据

- 角色：AI 可靠性知识库批次审阅者；本轮只复核初审 C01–C11 的关闭条件及修订引入的问题。
- 实际执行模型：`gpt-6.1-sol`；实际推理档位：`xhigh`。
- 核验依据：当前 `CODEX_THREAD_ID=01a15af6-1aa6-72c1-8d47-442ba0b851ee` 对应本地 CLI rollout；`session_meta.originator=codex_exec`、`source=exec`、`cli_version=0.163.0`，所查 `turn_context.model/effort` 只有上述一组值。本轮未调用其他审阅模型。
- cwd：`/Users/ywang2397/work/AI_reliability_knowledge_base`。
- 日期：2026-10-21（Asia/Shanghai）。
- 写入范围：只新增本报告；不修改正文、registry、取证记录、初审报告、计划、导航或审核/验证状态。

| 受审输入 | SHA-256 |
|---|---|
| [修订正文](../../knowledge/07-inference/distributed-inference-layouts.md) | `3e1b649543c267ee54f80d47487051704a6acd9507f5c8946087f5938cc2224f` |
| [关联取证记录](batch-27-t07-06-sources.md) | `78e88cb87ac82d7f6fd5e13c66c66d4738a62323747a8d9d19508300d0251295` |
| [来源登记表](../../sources/registry.yaml)（收尾重读版本） | `a954f0582111f83af8c9ec586077c66ca7eb1b6d12c26a17e575c57374ef3b2c` |
| [初审报告](batch-27-t07-06-codex-review.md) | `ce746b5eb0dcb96e5c28d38ac8c20847a20e3ba586e80cead25ebec1544e344b` |

已读取 README、写作指南、content-outline、AGENTS.md 与元数据 schema。下文“正文 L…”指本轮 156 行修订稿，“取证 L…”指关联取证记录。未重新展开初审已通过维度，也不重新评审 acceptance 第 5 项。

核对使用 `/tmp/b27-fetch/` 原文件及 `/tmp/vllm-b17039bccc17b94a2ea107272ad7bc93508708df/`、`/tmp/MindIE-LLM-master/` 快照。初审列出的 16 个缓存文件完整摘要全部匹配；补充的 arg_utils.py、config/vllm.py、config/model.py 也与初审摘要一致。特别是两处 MindIE tensor_parallel.md 的摘要均为 `d121df6eca46276bbb69aa0d419a2b639f29a8c97187e7da01e385455cc20147`，不能把下述初审定位错误解释为版本变化。固定版本仍为 vLLM `b17039bccc17b94a2ea107272ad7bc93508708df`、vLLM Ascend `52d4acfa51fb868823d1070b81cbd2d97e9e4696`、MindIE-LLM `69e5a5dd4b533eaffc7e198320435350825a36f7`。

ROCm 安装口径另重新打开 [v0.14.0 GPU 安装页](https://docs.vllm.ai/en/v0.14.0/getting_started/installation/gpu/)，并对照固定源码 `docs/getting_started/installation/gpu.rocm.inc.md`（SHA-256：`3f0c7129c7e0834745751f161feda79dada7851a2cd6b91b41f4794645c0db95`）。GitHub 行号均取原文件，不使用网页工具转换后的行号。registry 同时核对原文与 YAML 解析值。未启动引擎、运行通信测试或注入故障。

## 逐项判定

### C01 · CLOSED

正文 L51–52 已拆成纯独立 Dense 副本与 MoE DP attention 两行，分别说明权重、KV、请求及同步。MoE 行区分 attention 的复制/组内 TP 分片与专家跨 `TP×DP` 分片；L60 又区分开启 EP 与默认专家 TP 的组语义，符合 [DP L7–17](https://github.com/vllm-project/vllm/blob/b17039bccc17b94a2ea107272ad7bc93508708df/docs/serving/data_parallel_deployment.md#L7-L17)及 [EP L35–67](https://github.com/vllm-project/vllm/blob/b17039bccc17b94a2ea107272ad7bc93508708df/docs/serving/expert_parallel_deployment.md#L35-L67)。

L62–73 的 TP=2、DP=4 示意标出入口、四个 attention/KV 责任组、八卡共享专家组及 dispatch/combine、dummy forward 路径，明确声明为本库归纳，不声称实际 rank 编号或 placement 已验证。满足本项要求。

### C02 · 仍开放（机制修订已满足，仅剩训练 SP 普通链接）

正文 L56–58 已分别列 MindIE CP、MindIE SP、vLLM DCP。ring 与 FA2 分块修正只归于 CP；SP 同步列为 unknown，权重细节未核也在 L156 保留。L122 分别写 CP/SP 不支持 BF16，并说明 PD 分离仅 P 节点开启，符合 [CP L3–22](https://github.com/Ascend/MindIE-LLM/blob/69e5a5dd4b533eaffc7e198320435350825a36f7/docs/zh/user_guide/feature/context_parallel.md#L3-L22)与 [SP L3–21](https://github.com/Ascend/MindIE-LLM/blob/69e5a5dd4b533eaffc7e198320435350825a36f7/docs/zh/user_guide/feature/sequence_parallel.md#L3-L21)。L147 已区分 MindIE KV SP 与训练激活/buffer SP。

初审关闭条件还明确要求“链接训练 SP 的不同语义”。本轮正文没有到 [训练并行正文](../../knowledge/06-training/parallelism-and-state.md)的 Markdown 链接；只有语义提醒。最小修订是在 L147 补该正文“序列维并行”节的普通链接即可，无需重写机制或补硬件实验。本项不再有 CP/SP ring 混写的技术反对。

### C03 · 仍开放（正文满足，registry 未同步）

正文 L75 正确把简式限为 PCP=1、非 external_launcher 的普通布局，引用 [parallel.py L539–547](https://github.com/vllm-project/vllm/blob/b17039bccc17b94a2ea107272ad7bc93508708df/vllm/config/parallel.py#L539-L547)的实际赋值，保留 PCP 开发中及特殊分支完整语义未核。取证 L93 也记录了更正，没有由此宣告 PCP 可部署。

但 registry L536 的 `src.vllm.inference-v0-14.notes` 的 T07-06 段末尾仍直接写 `world_size＝TP×PP、world_size_across_dp＝TP×PP×DP`，没有普通布局限定、PCP 或 external_launcher 分支。初审要求同步纠正 notes，该部分未完成。最小修订是同步本段，区分字段说明、实际赋值及 [L351–354 属性](https://github.com/vllm-project/vllm/blob/b17039bccc17b94a2ea107272ad7bc93508708df/vllm/config/parallel.py#L351-L354)，不自行解释特殊分支的预期行为。

### C04 · CLOSED

正文 L77 已把字段说明与执行断言分开，并正确引用三处实际入口：

- [arg_utils.py L1387–1395](https://github.com/vllm-project/vllm/blob/b17039bccc17b94a2ea107272ad7bc93508708df/vllm/engine/arg_utils.py#L1387-L1395)：TP 能被 DCP 整除。
- [config/vllm.py L830–854](https://github.com/vllm-project/vllm/blob/b17039bccc17b94a2ea107272ad7bc93508708df/vllm/config/vllm.py#L830-L854)：DCP>1 时，生效 interleave size 不大于 block size 且整除 block size。
- [config/model.py L1076–1098](https://github.com/vllm-project/vllm/blob/b17039bccc17b94a2ea107272ad7bc93508708df/vllm/config/model.py#L1076-L1098)：DCP>1、非 MLA 时检查 TP>H、DCP≤TP//H，以及每 KV head 的 query head 数能被 DCP 整除。

GQA/非 MLA 条件已写出，TP>H 的有效 DCP 前提也进入 L90/L144。frontmatter L33 更新了 source_checked 的核对范围，取证 L94 记录了新位置，未把这些入口扩张成完整模型支持矩阵。保留的三组案例不在本轮重新评审。

### C05 · 仍开放（主要字段已纠正，但 local TP 差异的来源归属错误）

正文 L120 已逐字段区分 `tp/dp/cp/sp`、`moe_tp/moe_ep`、`ep_level` 与 local TP；MoE 乘积等式、L122 的 ep_level=2 时 moe_tp=1 均有 [optimization_and_tuning L169–191](https://github.com/Ascend/MindIE-LLM/blob/69e5a5dd4b533eaffc7e198320435350825a36f7/docs/zh/user_guide/optimization_and_tuning.md#L169-L191)支持。EP/MoE 字段被错误统归 parallel_options 的主问题已修正。

**必须纠正初审本身的一项错误前提。** 初审 C05 称 tensor_parallel.md L75–80 示例直接把 local TP 放在 deepseekv2 下；实际 [tensor_parallel.md L75–80](https://github.com/Ascend/MindIE-LLM/blob/69e5a5dd4b533eaffc7e198320435350825a36f7/docs/zh/user_guide/feature/tensor_parallel.md#L75-L80)的 L77 明确有 `"parallel_options": {`，L78–79 才是两项 local TP。这与同页 [L17–34 参数表](https://github.com/Ascend/MindIE-LLM/blob/69e5a5dd4b533eaffc7e198320435350825a36f7/docs/zh/user_guide/feature/tensor_parallel.md#L17-L34)一致。该初审子结论应撤回；本报告不修改历史文件。

真实存在的是**两页差异**：tensor_parallel.md 参数表及示例均用 `models.deepseekv2.parallel_options`；[optimization_and_tuning.md L70–85 示例](https://github.com/Ascend/MindIE-LLM/blob/69e5a5dd4b533eaffc7e198320435350825a36f7/docs/zh/user_guide/optimization_and_tuning.md#L70-L85)将两项直接放在 `models.deepseekv2` 下。

本轮正文 L120、L156 及取证 L95 却沿用成“同页参数表与同页示例不一致”，与原文件不符。最小修订是把差异双方改为上述两页，并各给行级链接；解析实现继续 unknown。不能为满足初审措辞而保留不存在的同页冲突。此处纳入 C05，不另重复计为新发现。

### C06 · 仍开放（正文满足，registry 未同步）

正文 L105、L130、L146 已区分指南概述与实现选择，并要求记录最终生效后端；取证 L96 也补了 [parallel.py L590–631](https://github.com/vllm-project/vllm/blob/b17039bccc17b94a2ea107272ad7bc93508708df/vllm/config/parallel.py#L590-L631)。该段确实从 mp 起步，经 CUDA nnodes>1、卡数不足报错、DP Ray 与 placement group 等有先后次序的分支选择，不再仅据“多机”推断后端。

registry L536 的 T07-06 段仍写“执行后端多机默认 Ray、单机默认 mp”，没有标成指南口径，也未补实际条件。虽保留了显式覆盖和多机 mp 参数，仍未完成本项明确要求的 notes 同步。最小修订是标明指南/实现层次并补上述入口、分支优先次序和最终生效后端的记录要求。

### C07 · 仍开放（正文满足，registry 未同步）

正文 L131 已写“本节点自身可达的地址、各节点值不同、与该节点 Ray 一致”，取证 L97 也改正，符合 [distributed_troubleshooting L11](https://github.com/vllm-project/vllm/blob/b17039bccc17b94a2ea107272ad7bc93508708df/docs/serving/distributed_troubleshooting.md#L11)及 [parallelism_scaling L77–104](https://github.com/vllm-project/vllm/blob/b17039bccc17b94a2ea107272ad7bc93508708df/docs/serving/parallelism_scaling.md#L77-L104)。

registry L536 同段仍为 `VLLM_HOST_IP 统一＋ray status/ray list nodes`。这保留了初审要求消除的歧义，故不能整体关闭。最小修订是将该短语同步为正文口径，保留 ray 命令用于复核已选地址。

### C08 · CLOSED

正文 L86 已把 TP 容量区间改为“单卡放不下、单机多卡放得下”；L90 写明 TP>H 再用有效 DCP，符合 [parallelism_scaling L5–23](https://github.com/vllm-project/vllm/blob/b17039bccc17b94a2ea107272ad7bc93508708df/docs/serving/parallelism_scaling.md#L5-L23)与 [context_parallel_deployment L23–41](https://github.com/vllm-project/vllm/blob/b17039bccc17b94a2ea107272ad7bc93508708df/docs/serving/context_parallel_deployment.md#L23-L41)。

L93–97 增加通信、扩展效率与尾延迟的定性比较，覆盖 TP 同步等待、PP stage 不均/气泡、EP 专家倾斜与 DP 请求均衡；结合前面的权重/KV 所有权表及 L139 的统一模型、输入长度、负载和资源条件，达到本次允许的比较框架要求。已标本库归纳、数值 unknown，不把“近线性”等框架描述视作已测扩展效率。本项不要求补造性能数字。

### C09 · 仍开放（缺口已如实保留，验收子项仍未通过）

正文 L110–112、L156 与取证 L99 已清楚分出：①EPLB 平台门控；②ROCm 安装口径；③尚缺的布局组合/all2all/DCP/RCCL 观测证据。EPLB 的 [parallel.py L325–338](https://github.com/vllm-project/vllm/blob/b17039bccc17b94a2ea107272ad7bc93508708df/vllm/config/parallel.py#L325-L338)与 [is_cuda_alike 实现 L175–177](https://github.com/vllm-project/vllm/blob/b17039bccc17b94a2ea107272ad7bc93508708df/vllm/platforms/interface.py#L175-L177)支持 CUDA/ROCm 门控，不能证明某个布局及通信路径已经成立。安装描述另有 N01 的来源范围问题，见下节。

**仍开放的明确理由**：初审允许在客观缺证时如实保留验收项未通过；这是一种合规的未完成状态，不等于已满足“固定 ROCm 所选布局限制”的关闭条件。正文现在也明确承认布局组合级缺位，本轮沿用该判断。无需取齐所有 ROCm 组合，但至少应给出一个有明确布局、平台条件和通信后端边界的固定版本证据闭环。

**可行的最小补证路径**：选一个小范围，例如“单节点 Dense TP，PP=DP=DCP=1、EP 关闭”，沿同一 commit 的 ROCm 平台、TP communicator 选择及实际 collective/library 路径补一条主张—证据链，并列出硬件/依赖和实现分支条件。已有可继续追查的固定入口为 [rocm.py L161–169](https://github.com/vllm-project/vllm/blob/b17039bccc17b94a2ea107272ad7bc93508708df/vllm/platforms/rocm.py#L161-L169)（dist_backend 名为 nccl）、[L508–512](https://github.com/vllm-project/vllm/blob/b17039bccc17b94a2ea107272ad7bc93508708df/vllm/platforms/rocm.py#L508-L512)（communicator 类）、[cuda_communicator.py L126–174](https://github.com/vllm-project/vllm/blob/b17039bccc17b94a2ea107272ad7bc93508708df/vllm/distributed/device_communicators/cuda_communicator.py#L126-L174)（多条 all-reduce 路径）及 [utils/nccl.py L17–35](https://github.com/vllm-project/vllm/blob/b17039bccc17b94a2ea107272ad7bc93508708df/vllm/utils/nccl.py#L17-L35)（库路径覆盖项；HIP 默认 librccl.so.1）。这些入口说明有可执行的补证任务，**本报告没有替正文完成调用链、硬件组合或运行验证**。补证需继续追清分支，不得只按类名 CudaCommunicator 或 backend 字符串 nccl 判断实际库。未选 EP/all2all、多机、DCP 及 RCCL 传输判据可继续 unknown；本次不要求执行硬件实验。

### C10 · CLOSED

正文 L133 已区分传输路径命中与通信等待进展。L137 的未执行设计包含请求失败/停滞、目标进程、组参与关系、其他副本进度、collective 进入/完成及前序异常、rank—进程—节点—设备 mapping 六步，借用 [collectives 正文 L194–207 的字段设计](../../knowledge/03-communication/collectives-and-rank-progress.md)。它区分纯独立副本与 MoE 共享专家同步域，并给出“限于单副本”和“跨副本影响”两类待检验判据，要求证据支撑，符合 [DP L9–17](https://github.com/vllm-project/vllm/blob/b17039bccc17b94a2ea107272ad7bc93508708df/docs/serving/data_parallel_deployment.md#L9-L17)的同步边界。

L139 的 correctness/throughput/latency 设计共用模型/权重、输入输出长度分布、采样、负载和资源上限，并保留错误与超时。运行表现仍是 unknown，没有据未执行设计宣告故障隔离或恢复已验证。满足本项设计层面的关闭条件。

### C11 · 仍开放（部分定位已补；原文存在与有效登记需区分）

已满足的子项：正文 L106 的 async EPLB 链接确实为 parallel.py L85–88；L54 对 PP 的 KV/段间激活机制标为本库归纳；L97 已补 bandwidth-baselines 普通链接；L124 的 local TP 场景/前提冲突及 CP/SP 量化集合主要已有具体行级来源。本轮不重评这些已通过的技术内容。

尚余以下定位与登记问题：

1. **Ascend 五行的链接目标仍漏 L31。** 正文 L116 的标签写“L23–26、L31”，实际 URL 只有 `#L23-L26`。应另链 [CP L31](https://github.com/vllm-project/vllm-ascend/blob/52d4acfa51fb868823d1070b81cbd2d97e9e4696/docs/source/user_guide/support_matrix/supported_features.md#L31)，或将目标改为 L23–31；不能只改标签。
2. **MindIE 部分约束仍未有对应行级链接。** 正文 L122 的双机 EP 必须经交换机条件在 [expert_parallel.md L25](https://github.com/Ascend/MindIE-LLM/blob/69e5a5dd4b533eaffc7e198320435350825a36f7/docs/zh/user_guide/feature/expert_parallel.md#L25)，现有 L13–14 链接只覆盖模型和 >32 专家条件；CP 仅切 2 份在 [context_parallel.md L32](https://github.com/Ascend/MindIE-LLM/blob/69e5a5dd4b533eaffc7e198320435350825a36f7/docs/zh/user_guide/feature/context_parallel.md#L32)，现链 L9–25 未覆盖。L120 的层级表还应随 C05 链到真正发生差异的两页。取证 L101 的“具体行已直接链接”不能视为上述目标已全补齐。
3. **“registry 已含并行五行补记”的回应，原始文本层面成立，有效 YAML notes 层面不成立。** 直接读取 registry L555，确实可见取证 L101 所指的 T07-06 并行五行补记；初审“未见补记”若解释为原文件没有这段文字，并不准确，应在此澄清。但该物理行的 notes 是未加引号的 YAML plain scalar，同一行前面的 `issue #1608` 从 `#` 开始截为注释。实际 `yaml.safe_load` 后，该条 notes 以“页首声明最新状态见 issue”结束，`T07-06` 不在有效 notes 中，整段并行补记没有进入解析值。结构检查仍通过，因为截短后依然是合法字符串。

第 3 项的最小修订是将该条 notes 安全地改为引号字符串或块标量，保留原文并用解析后的值确认五行补记存在；只用文本搜索命中不足以关闭。C03/C06/C07 所述上游 notes 未同步另按各自 ID 跟踪，不重复计数。

## 新问题

### N01 · P2 · 新增 ROCm 段把 AITER 的自行构建选项扩张为 EP/PD 安装声明

- **位置**：正文 L112；关联取证 L99 的“ AITER/MORI 可选”摘要。
- **问题**：正文将“AITER 与 MORI 为可选组件”及“安装文档将其与 EP/PD 分离关联”并列为已固定证据。原页对两者的声明不同：AITER 条目说明可自行选择 branch/commit 构建；明确说用于 EP 或 PD 分离的是 MORI 条目。选择自行构建，不等于已证明组件在所有路径均可省略；也不能把 MORI 的布局用途声明分配给 AITER。
- **依据**：固定 [gpu.rocm.inc.md L87–115](https://github.com/vllm-project/vllm/blob/b17039bccc17b94a2ea107272ad7bc93508708df/docs/getting_started/installation/gpu.rocm.inc.md#L87-L115)，与重新打开的 [v0.14.0 GPU 安装页](https://docs.vllm.ai/en/v0.14.0/getting_started/installation/gpu/)对应两条步骤一致。
- **关闭条件**：把 AITER 的“可选择自行构建指定分支/提交”与 MORI 的“若用于 EP/PD 可按该步骤安装”分开陈述；AITER 的具体布局依赖/可省略条件继续 unknown，或另补固定实现证据。同步取证摘要，在该句旁补准确链接。该问题不要求拓展到全部 ROCm 依赖审计。

C05 中修订沿用的错误冲突归属已经在该 ID 下记录，不重复编号；C11 的 YAML 截断是本轮查明的未闭环原因，无法仅凭当前输入断言其由本次修订首次引入。本轮没有其他独立、已证实的新问题。

## 整体结论

**本轮关闭 C01、C04、C08、C10；C02、C03、C05、C06、C07、C09、C11 仍开放，另新增 N01。T07-06 尚不能声明审阅通过。** C02 仅剩训练 SP 导航；C03/C06/C07 的正文修订已满足，残项集中在 registry 同步；C05 需纠正初审带入的错误来源归属；C09 仍是布局组合级验收缺口；C11 尚有实际链接目标和有效 YAML 登记问题。

初审已通过维度及 acceptance 第 5 项沿用原判定，不重新展开。ROCm 明示待补是正确的证据边界处理，但对应验收子项仍未通过。正文保持 draft/source_checked 的边界；本轮审阅与结构校验均不建立硬件验证。

结构检查：报告落盘后执行 `PYTHONDONTWRITEBYTECODE=1 make check`，通过（111 content entries / 542 sources）。为遵守只新增报告的范围，在完整输入副本 `/tmp/b27-recheck/validation-copy/` 用原工作区虚拟环境 Python 执行同一 Makefile 的 `make build`，通过；工作区 `build/` 未写入。临时副本首试因未复制已有 build 链接目标而失败，补齐这两项原输入后完成构建。没有修改 src/kb/，未新增或运行代码测试；这些结构检查不核验远程来源或技术结论。

写入范围核对：开工记录了 572 个既有文件的摘要。本轮工具只新增本报告。收尾对比另观察到 `knowledge/07-inference/quantization-and-quality.md`、`sources/registry.yaml` 有其他变动，以及 `docs/research/batch-27-t07-04-codex-recheck.md` 新出现；本轮未创建或修改这三个文件，不将其计作本任务产出。registry 开工摘要为 `6e22a2d6e9930886f3c252aef26c1c1f5029e260d1ca0b5ce7878b2977ebd518`，收尾版本见报告头部；已重新核对两条来源的 T07-06 相关原文及有效 YAML notes，C03/C06/C07/C11 判定不变。T07-06 正文及取证记录摘要保持不变；临时构建使用的是头部记录的收尾 registry 版本。

统计：原 C01–C11 共 11 项；CLOSED=4，仍开放=7；新增=1（P1=0，P2=1，P3=0，OPEN=1）；合计待处理=8；整体=未通过，需修订后定向复核；真实硬件验证=0。
