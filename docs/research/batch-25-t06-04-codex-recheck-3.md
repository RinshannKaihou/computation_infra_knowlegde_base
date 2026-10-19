# Batch 25 T06-04 第四轮定向复核报告

- 日期：2026-10-20（Asia/Shanghai）。本报告是初审后的第三份定向复核报告，对应作者第四轮修订。
- 审阅对象：[正文](../../knowledge/06-training/rl-rollout-consistency.md)、[来源登记](../../sources/registry.yaml)中两条论文 notes、[来源记录第四轮修订段](batch-25-t06-04-sources.md)。对照[第三轮复核](batch-25-t06-04-codex-recheck-2.md)、[初审](batch-25-t06-04-codex-review.md)、[第二轮复核](batch-25-t06-04-codex-recheck.md)与 [T06-04 验收条款](../../plans/full-coverage-backlog.yaml)。下文行号均指本轮输入。
- 执行角色：本地 Codex CLI 定向复核者。约定审阅标识为 `gpt-6.1-sol / xhigh`；本会话无法独立读取实际模型路由与推理档位元数据，实际执行标识记为 unknown，不把约定标识冒充运行核验结果。
- **结论：C07、C10 CLOSED；B25-T04-S2-01 仍为 P2 / OPEN。其余已关闭项未发现本轮回归。C01–C11 全部 CLOSED，R01–R03 全部 CLOSED；尚有 S2-01 一项开放，T06-04 整体验收仍不通过。** 本轮未确认需要另立 `B25-T04-S3-xx` 的独立新问题。

## 一、取证与版本边界

先读取 README、写作指南、内容边界、历次报告与完整正文，再核对修订差异及精确上游；不以作者的修订说明代替关闭判定。

| 本轮输入 | SHA-256 |
|---|---|
| `knowledge/06-training/rl-rollout-consistency.md` | `0f982c7071cf8e73640aca48c6755949def364a16ff126bb3b32cb68b18bb8ce` |
| `sources/registry.yaml` | `99b81d2047b01fc2ed7885143d062e6e0d7b44a0415db22dd63d1d9dd474857b` |
| `docs/research/batch-25-t06-04-sources.md` | `11bc1b1a28934012681779fee740c405d8367186244d28cde088b949f31b8c41` |

本机保留了第三轮构建快照 `/private/tmp/b25-t06-04-recheck2-final.q1sYAQ/`。先确认该快照三份输入的 SHA-256 与第三轮报告所列指纹逐一一致，再用于文本差异比较：正文只改 L68 与数据契约表，来源记录只追加第四轮修订段；本篇引用的来源条目仅两条论文的 `notes` 改变。登记文件还含 T06-05 的两处 notes 变化，不归入 T06-04 的修订或验收结论，也不编辑这些变化。

重新打开两篇 arXiv 摘要及其固定版本：[PPO v2，2017-08-28](https://arxiv.org/abs/1707.06347v2)、[DeepSeekMath v3，2024-04-27](https://arxiv.org/abs/2402.03300v3)。本轮核对的是摘要原文，不是论文 PDF 全文，也未重算登记中先前 API XML 的字节指纹。

本轮重新查询 [verl v0.9.1 tag](https://api.github.com/repos/verl-project/verl/git/ref/tags/v0.9.1)，仍解析为 `1876b06d0a3e4e71e06230be10af14492ca8a75b`。网页工具对部分 raw 文件取回失败后，改用 GitHub 连接工具读取该 commit 的相关片段及文件 blob SHA；以下十份文件的 blob SHA 均与 `/private/tmp/b25/verl-0.9.1/` 原文件的 Git blob SHA 一致，再使用原文件行号定位：

| 重新核对的文件与位置 | 用途 |
|---|---|
| [ray_trainer.py L1481–1548](https://github.com/verl-project/verl/blob/1876b06d0a3e4e71e06230be10af14492ca8a75b/verl/trainer/ppo/ray_trainer.py#L1481-L1548)、[L1570–1660](https://github.com/verl-project/verl/blob/1876b06d0a3e4e71e06230be10af14492ca8a75b/verl/trainer/ppo/ray_trainer.py#L1570-L1660)、[L1690–1716](https://github.com/verl-project/verl/blob/1876b06d0a3e4e71e06230be10af14492ca8a75b/verl/trainer/ppo/ray_trainer.py#L1690-L1716) | uid、重复响应与重排；logprob/reference/critic 条件；条件式保存与发布。 |
| [utils.py L75–79、L96–108](https://github.com/verl-project/verl/blob/1876b06d0a3e4e71e06230be10af14492ca8a75b/verl/trainer/ppo/utils.py#L75-L108) | reference 的两个启用开关；critic 的显式覆盖与 GAE 默认条件。 |
| [agent_loop.py L1065–1086](https://github.com/verl-project/verl/blob/1876b06d0a3e4e71e06230be10af14492ca8a75b/verl/experimental/agent_loop/agent_loop.py#L1065-L1086) | prompt/response/mask 实际字段；rollout logprob 只在返回值非空时加入 batch。 |
| [rollout_corr_helper.py L1109–1146](https://github.com/verl-project/verl/blob/1876b06d0a3e4e71e06230be10af14492ca8a75b/verl/trainer/ppo/rollout_corr_helper.py#L1109-L1146) | bypass 缺 rollout logprob 时明确报错，并以该数值建立 old 锚点。 |
| [rollout_correction.yaml L5–25](https://github.com/verl-project/verl/blob/1876b06d0a3e4e71e06230be10af14492ca8a75b/verl/trainer/config/algorithm/rollout_correction.yaml#L5-L25)、[rollout.yaml L235–237](https://github.com/verl-project/verl/blob/1876b06d0a3e4e71e06230be10af14492ca8a75b/verl/trainer/config/rollout/rollout.yaml#L235-L237) | decoupled 默认、IS/RS 默认关闭；采样 logprob 的配置条件。 |
| [fully_async_rollouter.py L491–507](https://github.com/verl-project/verl/blob/1876b06d0a3e4e71e06230be10af14492ca8a75b/verl/experimental/fully_async_policy/fully_async_rollouter.py#L491-L507)、[delta_weight_transfer.py L216–240](https://github.com/verl-project/verl/blob/1876b06d0a3e4e71e06230be10af14492ca8a75b/verl/workers/rollout/vllm_rollout/delta_weight_transfer.py#L216-L240) | 异步样本预算、rollout 消费端限制及 delta 失败边界回归抽查。 |
| [ppo.md L5–26](https://github.com/verl-project/verl/blob/1876b06d0a3e4e71e06230be10af14492ca8a75b/docs/algo/ppo.md#L5-L26)、[grpo.md L5–19](https://github.com/verl-project/verl/blob/1876b06d0a3e4e71e06230be10af14492ca8a75b/docs/algo/grpo.md#L5-L19) | clipped/免二阶导、组 baseline/免独立 critic 的实现文档归因。 |

## 二、本轮三项判定

| ID | 优先级 | 判定 | 当前位置与理由 |
|---|---|---|---|
| B25-T04-C07 | P2 | **CLOSED** | 正文 L115–128、L161–171；来源记录 L96。已定义 prompt 可回取身份、uid 的组归属、每个响应的 `(uid, i)`、稳定 sample_id 与递增 attempt、reward/logprob 的二元关联及 update 提交键；运行/恢复代次和权重身份仍分列。达到概念稿最小关联契约的关闭条件。 |
| B25-T04-C10 | P2 | **CLOSED** | 正文 L68；登记 L6356、L6367；来源记录 L97。两处上轮残留越界均已收窄到重新打开的摘要原文；机制细节继续归因固定 verl 文档，不冒充摘要或全文核验。 |
| B25-T04-S2-01 | P2 | **OPEN** | 正文 L111、L119–122；来源记录 L96。◇ 已纠正“所有字段都无条件产出”的表象，但把 rollout 与 old 合并标为模式条件，仍未区分实际存在条件、消费必需条件与缺失处置；没有完整落实第三轮列出的关闭条件。详见下文。 |

### C07：最小关联关系已补齐

正文现在区分了两个层级：`uid` 用于一条 prompt 的组归属，`sample_id=(uid, i)` 区分该组的多个响应；重试保持 sample_id 而递增 attempt，reward/logprob 明确挂到 `(sample_id, attempt)`。配合 response tokens/mask、prompt 回取要求、run/恢复代次与 update 提交键，可以表达“输入—组—响应—重试—数值—消费”的最小关系，不再把同 uid 的多个响应误当同一样本。上游确实先生成 uid、再重复 n 份并合并响应，之后可重排；因此本库自建响应序号必须随记录保留，不能在后续重排后另造身份，参见上表 ray_trainer 与 agent_loop 证据。

这里关闭的是**文档契约缺失**，不是宣称上游已经持久化该账本或哈希自动提供存储：正文已把索引/哈希、sample_id、attempt、身份采集标为本库建议，并要求输入可回取。重放时复用/重采范围仍须预注册（L169），按同一记录的 attempt 对齐 tokens 与数值；本轮不要求再实现采集器、事务或增加指定名称的 request_id/group_id。数值在什么配置下应有、何时可不适用，独立归 S2-01，不再重复计入 C07。

### C10：逐项对照摘要通过

- **PPO**：登记 L6356 现在分别归纳策略梯度方法族、surrogate 目标、多 epoch minibatch、TRPO 的部分益处与经验上的样本复杂度，以及模拟机器人运动/Atari 等实验中优于其他在线策略梯度方法。这些分别对应 [PPO v2 摘要](https://arxiv.org/abs/1707.06347v2)的三个句组，已删除上轮不受摘要直接支持的特定“连续控制 × 信任域方法 × 样本效率”比较组合。
- **DeepSeekMath/GRPO**：正文 L68 与登记 L6367 均改为 PPO 变体、增强数学推理并优化 PPO 内存使用，与 [DeepSeekMath v3 摘要](https://arxiv.org/abs/2402.03300v3)一致；不再声称免除 PPO 的全部内存开销。独立 critic 的开销与组 baseline 另归上述固定 GRPO 实现文档。
- 来源记录 L97 明确指出第四轮更正的对象；旧轮次说明不再被当作未改句子已经通过的证据。无须为关闭本项扩成论文全文评述，也不由此建立性能或硬件兼容结论。

### S2-01：◇ 不是完整的存在/必需条件

**已修部分**：正文 L111 明示条件式产出，reference 与 values 不再列成所有样本必有，L103 的四类 logprob 角色与默认模式说明也保持正确。不能因此重开已关闭的 C03/R01。

**仍开放的实质问题**：L119 把 `rollout logprob / old_log_prob` 共用一个 ◇，仅让读者参照 bypass/decoupled。这两个量的条件并不相同：在所选训练循环中，old 锚点无论哪个模式都须存在（L1617 显式断言）；rollout 数值是否实际返回还受采样配置与后端结果影响，而 decoupled 下是否必须采集它，又取决于是否启用需要该数值的校正。正文没有给出这些交集，也没有补齐“不适用如何记、启用路径缺数值如何停”的门槛。全局的“更新结果未知则冻结”不能替代入口配置/字段完整性检查。

尤其 [ray_trainer.py L1650–1658](https://github.com/verl-project/verl/blob/1876b06d0a3e4e71e06230be10af14492ca8a75b/verl/trainer/ppo/ray_trainer.py#L1650-L1658)在 decoupled 模式下先检查 batch 中有 rollout logprob 才调用校正；不能假定“配置启用了校正但没收集数值”一定会由上游自动报错。bypass 的缺字段报错见上述 helper，只覆盖 bypass 分支。此处需要的是本库明确的前置校验规则，而不是虚构上游普遍保证。

**最小关闭条件**：在字段表或紧邻短规则中分开下面条件即可，不要求实现采集代码或强制所有配方记录全部数值。

| 字段/路径 | 必须区分的条件与处置 |
|---|---|
| `old_log_probs` | 在本文所选更新路径中是必需锚点；decoupled 由训练侧重算，bypass 从 rollout 数值建立。模式改变的是生产方式，不是允许在更新时缺失。 |
| rollout logprob | 实际返回是条件式；decoupled 且 IS/RS 等依赖该量的校正关闭时，可缺失，不应判关联故障。bypass 或启用依赖该量的校正时必须取得；缺失则拒绝该路径/停止进入更新，不能静默按校正已生效继续。记录模式、相关开关与不适用原因。 |
| 当前 actor logprob | 更新时由训练侧计算，正文 L103 已说明其 ratio 角色；不要与采样产物或 old 锚点混为一列，也不冒称它天然是持久化样本字段。 |
| `ref_log_prob` 与 reference 身份 | 明确 `algorithm.use_kl_in_reward` 或 `actor_rollout_ref.actor.use_kl_loss` 任一启用才需要 reference；两者均关闭时数值/身份记为 `not_applicable` 或等价状态并保留开关，不要求虚构数值。当前“reference/in-reward KL”需展开为这两个可判定分支。 |
| `values` | 若声明的是上游存在条件，应对应 `use_critic`：`need_critic()` 允许 `critic.enable` 显式覆盖，否则按 GAE 决定；不能把“仅 PPO＋GAE”写成整个固定实现的排他保证。也可明确只描述默认 PPO＋GAE/无 critic 的 GRPO 样板并排除覆盖配置。 |

这些都是同一个条件字段契约问题，继续沿用 **B25-T04-S2-01**；不因增加 ◇ 或补入 values 就拆成重复的 S3 问题。

## 三、已关闭项的回归确认

本轮用指纹匹配的第三轮快照逐段比较。以下“未改”指段落内容一致，行号平移不算内容变化；不是只凭作者声称“未改”。

| 原发现 | 判定 | 本轮回归证据与边界 |
|---|---|---|
| C01 | **CLOSED（维持）** | 正文 L128、L143–149、L179：权重身份归一化、一步按采样/训练轮次计数、预算扣减携入旧样本、预算非逐样本硬上限均未改；另抽查预算源码。 |
| C02 | **CLOSED（维持）** | 正文 L157–171 整段未改：条件式 checkpoint、未知提交先冻结/隔离、checkpoint—账本一致回退、已持久更新才只重发、reward 重试不重复计数、GRPO 组保持及声明内 epoch 重用均保留。L165 仍与 L164 合读；delta 整作业重启边界另抽查源码。 |
| C03 | **CLOSED（维持）** | 正文 L103 未改；默认 decoupled、显式 bypass、old/current/rollout/reference 角色、GAE 与 GRPO 直接输入及 KL 分支未被改回。登记中对应说明也未改。S2-01 是字段条件不完整，不是默认值再次错误。 |
| C04 | **CLOSED（维持）** | 正文 L132–139 整段未改：跨组传输/本地 IPC 两跳、rollout 消费端限制、训练端分片汇聚及 Non-LoRA 边界、布局转换代价保留；消费端限制另抽查源码。未把 DP=1 扩成训练端限制。 |
| C05、C06 | **CLOSED（维持）** | 正文 L204–211 的平台证据线未改；Ascend post2/post4 仍 unknown，NVIDIA 多安装路径及容器代码 ref、AMD 独立镜像/代码线不互拼。本轮不冒称重新验证了平台组合。 |
| C08 | **CLOSED（维持）** | 正文 L32、L56、L99、L141、L224 的 V0 样板/V1 入口边界未改，未将 legacy 配置移用于 V1。 |
| C09 | **CLOSED（维持）** | 正文 L194–202 验证方法未改；资源、prompt/组数、有效 token、每样本重用、采样/校正及评估预算先固定，阶段与端到端计时分开，收益数字仍限作者环境。 |
| C11 | **CLOSED（维持）** | 正文 L60–93 的工作流对照、五阶段图、发布回边与数据来源说明保留；L68 只收窄 GRPO 摘要归因，没有破坏闭环。 |
| R01、R02、R03 | **CLOSED（维持）** | 分别对应 L103 默认模式、L135 生产/消费端限制、L128 恢复后 K/K+1 与权重身份；相关段落及本篇来源条目未改，没有把修订回退为旧说法。 |

## 四、新问题检查与整体验收

**本轮新增独立问题：0 项。** 未发现需另立 `B25-T04-S3-01` 的本轮回归；剩余的 old/rollout 条件、reference 分支和 critic 覆盖条件统一计入既有 S2-01，不重复编号。此判断限本轮变更及上述定向抽查，不是对整个 Batch 25 的重新全量审阅。

| 验收条款 | 第四轮判定 | 依据与剩余条件 |
|---|---|---|
| 1. 五阶段闭环，区分在线 RL / 离线偏好 / SFT | **满足（文档证据层面）** | C11 维持关闭，C10 的两处摘要越界已关闭；论文摘要与实现机制的归因分立。 |
| 2. 同步/受控异步样板及数据关联 | **未完全满足** | C07 的输入—组—响应—attempt—数值—消费关系已闭合；S2-01 仍缺配置条件、必需/不适用及缺失处置，不能仅以字段有 ◇ 宣告完整契约通过。 |
| 3. 权重同步、陈旧策略、随机性、TP/DP 与资源形态代价 | **本轮范围满足** | C01/C04/R02 关闭状态保持；未扩成所有布局、LoRA、V1 或跨平台兼容保证。 |
| 4. 吞吐、质量、有效样本及停止/重放/重复计算 | **既有规则与指标满足；字段前置条件仍待补** | C02 规则未回退，C07 关联已补；但进入 bypass/校正路径时缺必需数值的停止门槛仍须随 S2-01 落实。 |
| 5. 单变量验证、公开样板与三平台支持条件 | **满足（文档证据层面）** | C05/C06/C08/C09 维持关闭，公开样板及版本未知边界保留；没有真实设备结果，也未要求补造支持组合。 |

**最终整体判定：第四轮定向复核仍不通过，唯一剩余开放发现为 P2 / B25-T04-S2-01。** 后续只需补清字段的生产/存在/必需条件与缺失门槛，再对 S2-01 定向复核；不要求重做 C07/C10，也不应恢复已纠正的预算、默认模式、恢复 K 或 delta 端侧限制错误。T06-04 与整个 Batch 25 均不能由本报告标为审阅通过。

## 五、校验与变更边界

- 本轮仅新增本报告；不改正文、来源登记、来源记录、计划、导航或 `src/kb/`，不提交、不建分支。原工作区包含其他任务的未提交变化，均保留。
- 已执行 `make check`：通过，**107 content entries / 525 sources**；完整临时副本中执行 `make build`：通过，同为 **107 / 525**，生成两份 catalog。首次临时副本漏带既有 `build/`，被本地链接检查以两条 catalog 链接缺失拒绝；补齐副本后重跑通过，不涉及正文修复。上述检查只验证结构、引用与本地链接，不验证技术正确性、远程内容或平台兼容。
- 三份审阅输入的执行前后指纹均未变化。本轮写入只指向本报告与 `/private/tmp/`；期间还观察到其他任务新增 `batch-25-t06-06-codex-recheck.md` 及原工作区 `build/catalog.json` 的指纹变化，未回滚或改写这些并行状态，不宣称整个工作区没有其他变化。本轮构建明确在临时副本执行。
- 未执行 RL、rollout、权重发布、容器安装、失败注入或 GPU/NPU 测试；正文仍为 `draft / source_checked`。模型审阅、来源核对、结构校验与真实环境验证分别成立。
