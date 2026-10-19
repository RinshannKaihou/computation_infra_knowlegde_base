# Batch 25 T06-04 第三轮定向复核报告

- 日期：2026-10-20（Asia/Shanghai）。本报告是初审后的第二份定向复核报告，对应第三轮修订。
- 审阅对象：[正文](../../knowledge/06-training/rl-rollout-consistency.md)、[来源登记](../../sources/registry.yaml)、[来源记录及第三轮修订段](batch-25-t06-04-sources.md)；对照[初审 C01–C11](batch-25-t06-04-codex-review.md)、[第二轮复核及 R01–R03](batch-25-t06-04-codex-recheck.md)与 [T06-04 验收条款](../../plans/full-coverage-backlog.yaml)。下文正文、登记与来源记录的行号均指本轮输入，不沿用前两份报告的行号。
- 执行角色：本地 Codex CLI 定向复核者，仅新增本报告，不改正文、登记、来源记录或导航。约定审阅标识为 `gpt-6.1-sol / xhigh`；本会话无法独立读取实际模型路由及推理档位元数据，实际执行标识记为 unknown，不将约定标识当作运行核验凭据。
- 结论摘要：C01–C11 中 **9 项 CLOSED、2 项 OPEN（C07/C10）**；R01–R03 **全部 CLOSED**。另发现第三轮字段表引入的 **1 项 P2：B25-T04-S2-01**。原有两个 P1 的关闭条件已满足，但 T06-04 整体验收仍不通过。

## 一、逐项判定表

### 取证范围与固定位置

先读取 README、写作指南和内容边界，再核对完整修订正文、登记与历次报告；不以作者的“已改”说明替代技术判定。输入指纹如下，供后续修订区分版本：

| 输入 | SHA-256 |
|---|---|
| `knowledge/06-training/rl-rollout-consistency.md` | `1923b166bf893170da9e7710a32ec0efe95493cf0a80b0809b2c0b364b96daec` |
| `sources/registry.yaml` | `f923a3a713c5a5ecceb2e82d9becb1602dd98606b1bbde883e3d9ae1bd7fb7aa` |
| `docs/research/batch-25-t06-04-sources.md` | `3cb538fcc95fb8553ad1b387d99273e68d25678aa2b328802e6eb1678e12bda9` |

本轮重新查询 [verl v0.9.1 tag](https://api.github.com/repos/verl-project/verl/git/ref/tags/v0.9.1)，仍解析为 `1876b06d0a3e4e71e06230be10af14492ca8a75b`。网页工具对两份 raw 文件返回 cache miss，随后改用 GitHub 连接工具：重新打开该固定 commit 的 **27 个文档/源码文件**，取得完整文件 blob SHA，与 `/private/tmp/b25/verl-0.9.1/` 既有文件逐一计算的 Git blob SHA 核对，再依据相同原文件读取完整相关段落。下列链接使用原文件行号，不使用网页转换后的行号。

新增两条登记涵盖的五个文件另重算 SHA-256，均与登记相符：`rollout_correction.yaml` 的 `25e3a347…`，以及 delta 源码组的 `3c04a12b… / 8ffd1904… / 45818f36… / 79d8779f…`。本轮没有重新下载源码包或论文 XML；四篇论文重新打开的是摘要页，不冒充论文全文核验。未重新扩查 MindSpeed-LLM 的采样后端或 V1 控制流。

| 证据组 | 重新核对的位置与用途 |
|---|---|
| E01：预算与轮次 | [fully_async.md L118–146](https://github.com/verl-project/verl/blob/1876b06d0a3e4e71e06230be10af14492ca8a75b/docs/advance/fully_async.md#L118-L146)、[fully_async_rollouter.py L491–507](https://github.com/verl-project/verl/blob/1876b06d0a3e4e71e06230be10af14492ca8a75b/verl/experimental/fully_async_policy/fully_async_rollouter.py#L491-L507)、[one_step_off.md L11–48](https://github.com/verl-project/verl/blob/1876b06d0a3e4e71e06230be10af14492ca8a75b/docs/advance/one_step_off.md#L11-L48)：样本生产预算、历史超额样本、采样/训练轮次。 |
| E02：logprob 与优势 | [rollout_correction.yaml L5–25](https://github.com/verl-project/verl/blob/1876b06d0a3e4e71e06230be10af14492ca8a75b/verl/trainer/config/algorithm/rollout_correction.yaml#L5-L25)、[ray_trainer.py L218–279](https://github.com/verl-project/verl/blob/1876b06d0a3e4e71e06230be10af14492ca8a75b/verl/trainer/ppo/ray_trainer.py#L218-L279)、[L1570–1598](https://github.com/verl-project/verl/blob/1876b06d0a3e4e71e06230be10af14492ca8a75b/verl/trainer/ppo/ray_trainer.py#L1570-L1598)、[L1638–1674](https://github.com/verl-project/verl/blob/1876b06d0a3e4e71e06230be10af14492ca8a75b/verl/trainer/ppo/ray_trainer.py#L1638-L1674)：默认 decoupled、校正开关、直接优势输入与 KL 分支。 |
| E03：恢复、提交与样本关联 | [ray_trainer.py L1081–1092](https://github.com/verl-project/verl/blob/1876b06d0a3e4e71e06230be10af14492ca8a75b/verl/trainer/ppo/ray_trainer.py#L1081-L1092)、[L1426–1491](https://github.com/verl-project/verl/blob/1876b06d0a3e4e71e06230be10af14492ca8a75b/verl/trainer/ppo/ray_trainer.py#L1426-L1491)、[L1539–1548](https://github.com/verl-project/verl/blob/1876b06d0a3e4e71e06230be10af14492ca8a75b/verl/trainer/ppo/ray_trainer.py#L1539-L1548)、[L1677–1716](https://github.com/verl-project/verl/blob/1876b06d0a3e4e71e06230be10af14492ca8a75b/verl/trainer/ppo/ray_trainer.py#L1677-L1716)：恢复 K、trace K+1、uid 重复到组内响应、batch 对齐及条件式保存。 |
| E04：delta 两端边界 | [delta_weight_transfer.py L216–240](https://github.com/verl-project/verl/blob/1876b06d0a3e4e71e06230be10af14492ca8a75b/verl/workers/rollout/vllm_rollout/delta_weight_transfer.py#L216-L240)、[delta_checkpoint_engine.py L14–47](https://github.com/verl-project/verl/blob/1876b06d0a3e4e71e06230be10af14492ca8a75b/verl/checkpoint_engine/delta_checkpoint_engine.py#L14-L47)、[vllm_async_server.py L1141–1168](https://github.com/verl-project/verl/blob/1876b06d0a3e4e71e06230be10af14492ca8a75b/verl/workers/rollout/vllm_rollout/vllm_async_server.py#L1141-L1168)、[FSDP transformer_impl.py L918–959](https://github.com/verl-project/verl/blob/1876b06d0a3e4e71e06230be10af14492ca8a75b/verl/workers/engine/fsdp/transformer_impl.py#L918-L959)：消费端限制、生产端分片汇聚、Non-LoRA 路径及部分写入后的重启边界。 |
| E05：实现线与缓存 | [ppo_trainer.yaml L228–238](https://github.com/verl-project/verl/blob/1876b06d0a3e4e71e06230be10af14492ca8a75b/verl/trainer/config/ppo_trainer.yaml#L228-L238)、[main_ppo.py L183–192](https://github.com/verl-project/verl/blob/1876b06d0a3e4e71e06230be10af14492ca8a75b/verl/trainer/main_ppo.py#L183-L192)、[vllm_rollout.py L194–260](https://github.com/verl-project/verl/blob/1876b06d0a3e4e71e06230be10af14492ca8a75b/verl/workers/rollout/vllm_rollout/vllm_rollout.py#L194-L260)：V1 默认入口、legacy 分流、sleep/wake-up、KV 清理和发布步号。 |
| E06：独立平台条件 | [install.rst L4–27](https://github.com/verl-project/verl/blob/1876b06d0a3e4e71e06230be10af14492ca8a75b/docs/start/install.rst#L4-L27)、[L50–76](https://github.com/verl-project/verl/blob/1876b06d0a3e4e71e06230be10af14492ca8a75b/docs/start/install.rst#L50-L76)、[docker/README.md L50–59](https://github.com/verl-project/verl/blob/1876b06d0a3e4e71e06230be10af14492ca8a75b/docker/README.md#L50-L59)、[Dockerfile.stable.vllm L1–22](https://github.com/verl-project/verl/blob/1876b06d0a3e4e71e06230be10af14492ca8a75b/docker/Dockerfile.stable.vllm#L1-L22)、[AMD quick start L15–42](https://github.com/verl-project/verl/blob/1876b06d0a3e4e71e06230be10af14492ca8a75b/docs/amd_tutorial/amd_quick_start.rst#L15-L42)、[Dockerfile.rocm L30–54](https://github.com/verl-project/verl/blob/1876b06d0a3e4e71e06230be10af14492ca8a75b/docker/rocm/Dockerfile.rocm#L30-L54)、[Ascend 安装页 L9–17](https://github.com/verl-project/verl/blob/1876b06d0a3e4e71e06230be10af14492ca8a75b/docs/ascend_tutorial/zh/get_start/install_guidance.rst#L9-L17)、[L84–108](https://github.com/verl-project/verl/blob/1876b06d0a3e4e71e06230be10af14492ca8a75b/docs/ascend_tutorial/zh/get_start/install_guidance.rst#L84-L108)及[后端特性 L10–39](https://github.com/verl-project/verl/blob/1876b06d0a3e4e71e06230be10af14492ca8a75b/docs/ascend_tutorial/zh/feature_support/ascend_backend_features.md#L10-L39)。 |
| E07：算法与摘要分工 | [PPO 文档 L5–26](https://github.com/verl-project/verl/blob/1876b06d0a3e4e71e06230be10af14492ca8a75b/docs/algo/ppo.md#L5-L26)、[GRPO 文档 L5–25](https://github.com/verl-project/verl/blob/1876b06d0a3e4e71e06230be10af14492ca8a75b/docs/algo/grpo.md#L5-L25)、[HybridFlow 指南 L27–68](https://github.com/verl-project/verl/blob/1876b06d0a3e4e71e06230be10af14492ca8a75b/docs/hybrid_flow.rst#L27-L68)、[Online DPO L28–42](https://github.com/verl-project/verl/blob/1876b06d0a3e4e71e06230be10af14492ca8a75b/docs/advance/dpo_extension.rst#L28-L42)、[最佳实践](https://github.com/verl-project/verl/blob/1876b06d0a3e4e71e06230be10af14492ca8a75b/docs/perf/best_practices.rst)；四篇摘要：[PPO](https://arxiv.org/abs/1707.06347)、[DeepSeekMath](https://arxiv.org/abs/2402.03300)、[DPO](https://arxiv.org/abs/2305.18290)、[HybridFlow](https://arxiv.org/abs/2409.19256)。 |
| E08：字段的条件式产出 | [utils.py L75–79](https://github.com/verl-project/verl/blob/1876b06d0a3e4e71e06230be10af14492ca8a75b/verl/trainer/ppo/utils.py#L75-L79)、[ray_trainer.py L1617–1628](https://github.com/verl-project/verl/blob/1876b06d0a3e4e71e06230be10af14492ca8a75b/verl/trainer/ppo/ray_trainer.py#L1617-L1628)、[agent_loop.py L1063–1089](https://github.com/verl-project/verl/blob/1876b06d0a3e4e71e06230be10af14492ca8a75b/verl/experimental/agent_loop/agent_loop.py#L1063-L1089)、[rollout.yaml L235–237](https://github.com/verl-project/verl/blob/1876b06d0a3e4e71e06230be10af14492ca8a75b/verl/trainer/config/rollout/rollout.yaml#L235-L237)：reference 按 KL 配置启用，rollout logprob 可选；默认计算不等于所有配置强制产出。 |

### C01–C11 与 R01–R03

优先级保留初审记录；CLOSED 只表示对应发现的关闭条件满足，不表示目标环境已验证。新表的条件式字段问题另列 S2-01，不把它误算为 bypass 默认值仍错误。

| ID | 原优先级 | 判定 | 当前修订位置 | 理由与剩余条件 |
|---|---|---|---|---|
| B25-T04-C01 | P1（上轮剩余按 P2） | **CLOSED** | 正文 L126、L143–147、L177；来源记录 L89；登记 L6191 | E01 支持扣减“上轮超额携入的旧样本”，一步单位已改为采样/训练轮次而非 optimizer 次数；正文明确预算不是逐样本版本硬上限，发布轮次与本地更新分别观测。同步零滞后的权重身份原则也已补入，不再用 0/1 标签直减。样本键如何落地仍归 C07，不再重计本项。 |
| B25-T04-C02 | P1 | **CLOSED** | 正文 L155–169；来源记录 L90 | 已增加“更新已执行但结果未知/未持久化”的停止/隔离分支、checkpoint 与账本一致回退、已持久提交才只重发、reward 重试不重复计入、重放复用范围和 GRPO 组保持。E03 确认保存是条件式；正文 L163 的“更新后发布前”规则必须与 L162 合读，仅用于已确认持久的更新，否则执行 L162，不能假定存在新 checkpoint。delta 整作业重启边界保留且符合 E04。这些是本库规则，不是上游 exactly-once 承诺；无需实现恢复事务才能关闭概念稿的本项。 |
| B25-T04-C03 | P2 | **CLOSED** | 正文 L103；登记 L6247、L6543–6556；来源记录 L86、L92 | 默认 decoupled、显式 bypass、当前 actor/proximal-old/rollout/reference 的角色和 ratio 位置均已分清；IS/RS 默认 null，不再暗示自动校正。GAE/GRPO 直接输入及 reward KL/actor KL loss 分支正确，登记明确撤回 GAE path-variance 误读。E02 支持；旧来源表 L45 的泛化表述应以明确更正段为准。 |
| B25-T04-C04 | P2 | **CLOSED** | 正文 L130–137；登记 L6529–6542；来源记录 L87 | 已区分跨组 NCCL 与 rollout 本地 IPC 两跳；vLLM 消费端 CUDA/BF16/DP=1/PP=1 及排除项、训练生产端分片汇聚分列，未再要求 trainer DP=1。Non-LoRA base path 与 LoRA 未建证据明确。新增源码组有四文件指纹，覆盖此前未追踪文件。E04 支持；“支持非 DP=1”只限有相应导出/汇聚路径，不扩展为所有训练布局或 LoRA 均可用。 |
| B25-T04-C05 | P2 | **CLOSED（维持）** | 正文 L207、L222；来源记录 L79 | E06 再次确认 torch_npu post2/post4 两处冲突。正文仍保留实际 post 选择 unknown，与其他 vllm-ascend 版本线分立，没有把差异拼成确定配套。关闭的是冲突披露缺陷，不是消解了平台兼容问题。 |
| B25-T04-C06 | P2 | **CLOSED** | 正文 L206、L209；来源记录 L91 | 已分列安装页的最低要求、uv 路径、GB200/aarch64 镜像缺口、Dockerfile 的 v0.7.1 代码 ref，以及 AMD 自建的独立 `VERL_TAG`。E06 与这些事实相符；撤回“机制证据来自该已验证组合”，明确安装路径仍须另选。对本页非执行处方的范围，这已满足来源级支持边界；不要求运行镜像或补造一个已验证组合。 |
| B25-T04-C07 | P2 | **OPEN** | 正文 L111–126、L161、L165–169；来源记录 L88 | 字段表已补 run/恢复代次、sample_id/attempt 和 update 提交键，R03 也已纠正；但仍只命名各字段，没有定义 prompt uid 与 n 个 response/sample_id 的关系、attempt 是否改变 sample_id、reward/logprob 绑定哪个响应/attempt，以及输入 prompt 的可回取身份。重放与去重规则因而仍缺等价的最小关联契约。详见下文；字段的条件式产出另归 S2-01。 |
| B25-T04-C08 | P2 | **CLOSED（维持）** | 正文 L32、L56、L99、L139、L222；来源记录 L75 | E05 确认 V1 默认入口及 legacy 分流。正文仍清楚选择 V0 机制样板，不把旧 fully-async/one-step 参数用于 V1；本轮默认 logprob 修订没有破坏这一实现线声明。 |
| B25-T04-C09 | P2 | **CLOSED（维持）** | 正文 L192–200 | 总资源、prompt/组数、有效 token、每样本更新次数、采样/校正和评估预算均先固定；streaming 下对齐同步周期参数，并分阶段/端到端计时。收益数字保持作者环境限定，不再作性能排序保证。E01/E07 支持方法层面判断，不证明比较已执行。 |
| B25-T04-C10 | P2 | **OPEN** | 正文 L68；登记 L6356–6367；来源记录 L49–50、L82、L92 | PPO 正文已收窄到 surrogate objective＋多 epoch minibatch；登记也明确 clipped/免二阶导与 GRPO baseline/免 critic 转由实现文档承载，这部分通过。但 PPO notes 仍有摘要未建立的“连续控制任务上与信任域方法的样本效率对比”，正文又把 DeepSeekMath 摘要的优化内存使用写成“免除 PPO 的内存开销”。不能以机制归因的括注覆盖这两处剩余越界；详见下文。 |
| B25-T04-C11 | P3 | **CLOSED（维持）** | 正文 L60–93 | 五阶段图、发布回边和数据来源章节仍存在；SFT、离线 DPO、在线 RL 与 Online DPO 的对照保持清楚。E07 支持；不因图的字符对齐问题重开此项。 |
| B25-T04-R01 | P2 | **CLOSED** | 正文 L103；登记 L6543–6556；来源记录 L86 | E02 配置为 `bypass_mode: false`、`rollout_is: null`、`rollout_rs: null`，训练循环缺省同样走重算 proximal-old；修订一致，不再把 bypass 写成默认，也未承诺校正默认启用。 |
| B25-T04-R02 | P2 | **CLOSED** | 正文 L133；登记 L6542；来源记录 L87 | E04 的 `parallel_config`/rollout config 限制已正确落到 vLLM 消费端；生产端分片汇聚另述，未把该限制移植给训练 DP/PP。LoRA 未支持的证据边界明确。 |
| B25-T04-R03 | P2 | **CLOSED** | 正文 L126；来源记录 L88 | E03 确认 `_load_checkpoint()` 设置 K，首次同步 K，随后循环递增到 K+1；正文已将 0/1 限为从零启动特例，并与实际权重身份区分。来源记录 L78 的旧说法被 L88 的明确更正覆盖，不需涂改历史审阅记录。 |

### 仍开放项的最小关闭条件

**C07：字段名清单还不是关联契约。** E03 的 uid 在 prompt 级生成，随后随 `rollout.n` 重复到多个响应；它用于组归一化，不能单独充当响应去重键。当前 L115–123 没有规定这些响应如何分别获得 sample_id、一次 reward 重试或重新采样如何与原记录关联。仅说“样本级与重试级唯一键”不能判断迟到 reward 是否属于已被替换的响应，也不能判断同 uid 的 n 条响应是否被错误去重成一条。表中只有 prompt uid，没有 prompt tokens 或不可变内容引用，亦不足以兑现重放输入可回取。

最少补一个关系示例或等价短规则：`run/恢复代次 → prompt uid/组 → 多个响应 sample_id → 生成或打分 attempt → 所选响应的 reward 与各类 logprob → update 提交键`；明确哪些重试复用 sample_id、重新采样是否产生新响应身份、同组响应不能因共享 uid 去重、prompt/response tokens 与对应 mask 如何取回。将消费时的轮次锚与行为策略发布身份分列。**不要求新增名为 request_id/group_id 的字段**，现有键能表达上述关系即可；这些是本库建议，不声称上游自动持久化。已有零滞后原则与恢复 K 规则无需重做。

**C10：已纠正机制出处，但还留有两处摘要越界。**

1. 登记 L6356 仍写“论文在连续控制任务上报告与信任域方法的样本效率对比”。重新打开的 [PPO 摘要](https://arxiv.org/abs/1707.06347)分别谈到 TRPO 的一些优点、样本复杂度和包括机器人运动/Atari 的实验，但没有建立这个特定比较对象、任务子集和指标的组合；[verl PPO 文档 L5–26](https://github.com/verl-project/verl/blob/1876b06d0a3e4e71e06230be10af14492ca8a75b/docs/algo/ppo.md#L5-L26)也不补足该实验对比。删除/收窄这一句，或另补固定论文全文的对应实验位置；本报告不是断言论文全文不存在相关结果。
2. 正文 L68 写“摘要报告其免除 PPO 的内存开销”。[DeepSeekMath 摘要](https://arxiv.org/abs/2402.03300)只报告优化 PPO 的内存使用；[verl GRPO 文档 L5–19](https://github.com/verl-project/verl/blob/1876b06d0a3e4e71e06230be10af14492ca8a75b/docs/algo/grpo.md#L5-L19)支持免除独立 critic 的开销，不支持免除 PPO 的全部内存开销。改为“改善/降低内存使用”；若保留“免除”，限定为独立 critic 的那部分并归因实现文档。

登记中 clipped/免二阶导、组 baseline/免 critic 的“摘要未展开、由实现文档承载”括注已有效区分证据层次，不要求为关闭本项强制核验全部论文。来源记录 L49–50 可保留为历史，但应明确只承载当前更正后的范围，不能再把 L82/L92 的“已收窄”当作剩余句子也已通过的证据。

## 二、新发现

### B25-T04-S2-01 — P2 / OPEN：新增最小字段表把条件式产出写成无条件上游字段

- **位置**：正文 L111–119，尤其 `ref_log_prob＋reference 权重身份` 的“数值上游产出”；同表 `rollout logprob / old_log_prob` 也未标明 rollout 数值的存在条件。
- **问题**：表头是“一条样本必须绑定什么”的最小契约，但未区分必填、按配置启用及不适用。E08 中 `need_reference_policy()` 仅在 reward KL 或 actor KL loss 启用时为真；`ray_trainer.py` 仅在该条件下计算 `ref_log_prob`。两种 KL 均关闭的合法配置没有 reference 数值，不能据此判为缺字段或关联失败。rollout logprob 也以实际返回值为条件加入 batch；默认 `calculate_log_probs: True` 不等于所有 recipe/覆盖配置都保证该字段存在。
- **上游证据**：[utils.py L75–79](https://github.com/verl-project/verl/blob/1876b06d0a3e4e71e06230be10af14492ca8a75b/verl/trainer/ppo/utils.py#L75-L79)、[ray_trainer.py L1617–1628](https://github.com/verl-project/verl/blob/1876b06d0a3e4e71e06230be10af14492ca8a75b/verl/trainer/ppo/ray_trainer.py#L1617-L1628)、[agent_loop.py L1071–1073](https://github.com/verl-project/verl/blob/1876b06d0a3e4e71e06230be10af14492ca8a75b/verl/experimental/agent_loop/agent_loop.py#L1071-L1073)、[rollout.yaml L235–237](https://github.com/verl-project/verl/blob/1876b06d0a3e4e71e06230be10af14492ca8a75b/verl/trainer/config/rollout/rollout.yaml#L235-L237)。
- **影响**：会把合法的无 reference、无 rollout logprob 配置误判为一致性故障；反过来也可能只看“上游产出”而未检查显式 bypass/校正所需数值是否实际存在。这与 R01 默认值是否正确是两个判断。
- **关闭条件**：字段表增加“存在/必需条件”：reference 数值与身份按实际启用的 reference 路径记录；不启用时记录 `not_applicable` 及相关开关，而不是虚构数值。分别列出 rollout/old/current/reference logprob 的生产者与模式条件；显式 bypass 或所启用校正所需的 rollout 数值缺失应停止该路径，decoupled 且校正关闭时不能无条件要求它。若本库额外要求全量采集，明确这是自建审计要求及需验证的采集能力，不写成上游普遍保证。

本项是第三轮字段表引入的条件性问题；C07 是既有键关系与输入关联仍未闭合，C03/R01 是已纠正的模式与默认值问题。编号分别保留以便定向复核，不把相邻修改点当作多个独立高优先级根因。

## 三、总体判定

**第三轮定向复核仍不通过。** 初审 11 项中 C01/C02/C03/C04/C05/C06/C08/C09/C11 共 **9 项关闭**，C07/C10 共 **2 项开放**；第二轮新增 R01/R02/R03 共 **3 项全部关闭**；本轮新增 S2-01 **1 项 P2 开放**。原有 P1 阻塞已解除，剩余问题不应继续标为“两个 P1 未修复”，但也不足以将 T06-04 或整个 Batch 25 标为审阅通过。

| 验收条款 | 本轮整体判定 | 依据与剩余条件 |
|---|---|---|
| 1. 五阶段闭环，区分在线 RL / 离线偏好 / SFT | **展示满足，证据口径尚未完全满足** | C11 维持关闭；PPO/GRPO 的主要机制出处已经分流，但 C10 的摘要实验归因与内存表述须收窄。 |
| 2. 同步/受控异步样板与数据关联 | **未满足** | C01/C03/R01/R03 已关闭；C07 仍缺 prompt—组—响应—重试—reward/logprob—update 的关系，S2-01 需补字段条件。不能用“已有字段表”替代关联与适用性检查。 |
| 3. 权重同步、陈旧策略、随机性、TP/DP 与共置/分离代价 | **本轮范围满足** | C01/C04/R02 关闭；预算单位、两跳、生产/消费限制、布局转换及随机性基线已说明。只承认所选 V0 样板的证据，不扩展到任意布局、LoRA、V1 或其他平台。 |
| 4. 吞吐/质量/有效样本及停止、重放、重复计算 | **恢复规则和指标已满足；端到端关联仍未闭合** | C02 的 P1 关闭：已覆盖未知提交、停止/隔离、checkpoint—账本一致点与合法 epoch 重用。作为概念规则不要求实现事务；但依赖的样本/重试键仍受 C07 阻塞，不能宣称已可据表可靠去重。 |
| 5. 单变量方法、公开样板与三平台支持条件 | **文档证据层面满足** | C05/C06/C08/C09 均关闭；NVIDIA 多路径和容器内代码 ref 已分立，Ascend 冲突明确 unknown，AMD 范围为官方声明而非本地兼容验证。无需伪造某一安装组合的实测结果。 |

后续仅需围绕 **C07、C10、S2-01** 修订并定向复核：补足键关系与输入引用、标明字段条件、删减或补证两处摘要越界。已关闭的恢复 K、默认 decoupled、delta 两端限制和预算公式不应再次改回旧说法。

### 校验与变更边界

- 本报告不修改 `src/kb/`，不新增测试，不执行 RL、rollout、参数发布、容器安装、失败注入或 GPU/NPU 基准。正文 `draft / source_checked` 不变；模型审阅、来源核对和硬件验证继续分开。
- 已执行 `make check`：通过，**107 content entries / 525 sources**；在完整临时仓库快照执行 `make build`：通过，同为 **107 / 525**，生成两份 catalog。原工作区 `build/catalog.json` 与 `build/catalog.md` 的执行前后 SHA-256 均未变化；三份审阅输入的指纹亦未变化。这些检查只验证结构、引用与本地链接，不验证技术正确性、远程内容或平台兼容。
- 本轮只写入本报告；工作区已有修改和并行产生的其他任务文件均未编辑，不提交、不建分支。
