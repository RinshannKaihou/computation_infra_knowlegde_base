# Batch 25 T06-04 第五轮定向复核报告

- 日期：2026-10-20（Asia/Shanghai）。本报告对应作者第五轮修订，是初审后的第四份定向复核报告。
- 审阅对象：[正文](../../knowledge/06-training/rl-rollout-consistency.md)第五轮版本，重点为 L109–130 的数据契约表与入口配置完整性检查；对照[第四轮复核](batch-25-t06-04-codex-recheck-3.md)、[第三轮复核](batch-25-t06-04-codex-recheck-2.md)、[第二轮复核](batch-25-t06-04-codex-recheck.md)、[初审](batch-25-t06-04-codex-review.md)、[来源记录](batch-25-t06-04-sources.md)、[来源登记](../../sources/registry.yaml)与 [T06-04 验收条款](../../plans/full-coverage-backlog.yaml)。正文行号均按本轮输入。
- 执行角色：本地 Codex CLI 定向复核者。约定审阅标识为 `gpt-6.1-sol / xhigh`；本会话无法独立读取实际模型路由及推理档位元数据，实际执行标识记为 unknown，不把约定标识冒充运行核验结果。
- **结论：B25-T04-S2-01（P2）CLOSED；C01–C11、R01–R03 全部维持 CLOSED，包括上轮关闭的 C07、C10。未发现需新立 B25-T04-S4-xx 的独立问题。累计 15 项发现全部关闭、开放项为 0；T06-04 通过既定审阅范围。** 此结论不扩展为整个 Batch 25 通过，也不代表真实环境验证通过。

## 一、输入指纹、差异与取证边界

先读取 README、写作指南与内容边界，再核对修订正文和历史关闭条件；不以作者的修订说明代替源码分支判断。

| 本轮输入 | SHA-256 |
|---|---|
| `knowledge/06-training/rl-rollout-consistency.md` | `b5868c6d8a5f7024833b9ddad9f8f3aaa2666129a97ae2f9ddabb5d1fd7389ef` |
| `sources/registry.yaml` | `99b81d2047b01fc2ed7885143d062e6e0d7b44a0415db22dd63d1d9dd474857b` |
| `docs/research/batch-25-t06-04-sources.md` | `11bc1b1a28934012681779fee740c405d8367186244d28cde088b949f31b8c41` |

第四轮快照 `/private/tmp/b25-t06-04-recheck3.LLoby4/repository/` 的上述三份输入指纹与第四轮报告逐一一致，故可作差异基线。本轮正文仅数据契约段变化：重构列名、拆分 old/rollout、列出当前 actor 计算产物、展开 reference/critic 条件，并增加入口检查；其余正文未变。登记与来源记录均与第四轮逐字节一致。来源记录末段仍是历史第四轮修订说明，不把它当作第五轮已经核验的凭据；本报告记录本轮的独立关闭依据。

重新查询 [verl v0.9.1 tag](https://api.github.com/repos/verl-project/verl/git/ref/tags/v0.9.1)，仍解析为 `1876b06d0a3e4e71e06230be10af14492ca8a75b`。网页工具取回的 raw 文本行号会重排，部分文件取回失败，因此以 GitHub 连接工具重开固定 commit 文件，取得完整文件 blob SHA，并逐一与 `/private/tmp/b25/verl-0.9.1/` 原文件的 `git hash-object` 结果比对；下表九份文件全部相符，位置使用原文件坐标。

| 证据 | 本轮重新核对的位置与用途 | Git blob SHA |
|---|---|---|
| E01 | [ray_trainer.py L1570–1628](https://github.com/verl-project/verl/blob/1876b06d0a3e4e71e06230be10af14492ca8a75b/verl/trainer/ppo/ray_trainer.py#L1570-L1628)、[L1650–1658](https://github.com/verl-project/verl/blob/1876b06d0a3e4e71e06230be10af14492ca8a75b/verl/trainer/ppo/ray_trainer.py#L1650-L1658)：old 的两种生产路径及 L1617 断言；reference/values 门控；缺 rollout 数值时校正分支不会进入。另按同一原文件核对 L343–348 的角色开关和 L1327–1369 的 actor 更新入口。 | `9352bcfa4d56bda8e70fc7df183e588a65afb43d` |
| E02 | [utils.py L75–79、L96–108](https://github.com/verl-project/verl/blob/1876b06d0a3e4e71e06230be10af14492ca8a75b/verl/trainer/ppo/utils.py#L75-L108)：reference 为两个 KL 开关取或；critic 优先读取显式 enable，否则由 GAE 决定。 | `e0ed14111f80f85b9ecfdbb8581caef9f6d14e13` |
| E03 | [rollout_corr_helper.py L1109–1146](https://github.com/verl-project/verl/blob/1876b06d0a3e4e71e06230be10af14492ca8a75b/verl/trainer/ppo/rollout_corr_helper.py#L1109-L1146)：bypass 缺 `rollout_log_probs` 报错，并以该数值建立 `old_log_probs`。 | `eed6de70d9696fb78753b73e9edfebebba8b6f98` |
| E04 | [agent_loop.py L1065–1086](https://github.com/verl-project/verl/blob/1876b06d0a3e4e71e06230be10af14492ca8a75b/verl/experimental/agent_loop/agent_loop.py#L1065-L1086)：仅当返回的 response logprobs 非空才加入 rollout 字段；prompt/response/mask 的实际产物。 | `d0e3038ec30881534ca2236a4a662b4ab5324832` |
| E05 | [rollout_correction.yaml L5–25](https://github.com/verl-project/verl/blob/1876b06d0a3e4e71e06230be10af14492ca8a75b/verl/trainer/config/algorithm/rollout_correction.yaml#L5-L25)：默认 decoupled，IS/RS 默认 null。 | `60cc00e9265f8e5f8eeb44789de5cf2c6e169511` |
| E06 | [rollout.yaml L235–237](https://github.com/verl-project/verl/blob/1876b06d0a3e4e71e06230be10af14492ca8a75b/verl/trainer/config/rollout/rollout.yaml#L235-L237)：默认采集配置与需要该数值的校正说明，不等于任意覆盖配置都实际返回字段。 | `99ca1864931b2c7d8aaa0dd3ae46d0a1b4fdd9ea` |
| E07 | [losses.py L57–112](https://github.com/verl-project/verl/blob/1876b06d0a3e4e71e06230be10af14492ca8a75b/verl/workers/utils/losses.py#L57-L112)、[L132–135](https://github.com/verl-project/verl/blob/1876b06d0a3e4e71e06230be10af14492ca8a75b/verl/workers/utils/losses.py#L132-L135)：当前 logprob 来自 model output，old 从输入取出，分别传入策略损失；actor KL loss 启用时读取 reference。仅补查此薄层调用，不扩成 `core_algos.py` 损失实现的完整审阅。 | `ebaa4e4d8b759db980f62bf96f83be305f54847e` |
| E08 | [fully_async_rollouter.py L491–507](https://github.com/verl-project/verl/blob/1876b06d0a3e4e71e06230be10af14492ca8a75b/verl/experimental/fully_async_policy/fully_async_rollouter.py#L491-L507)，并据同一原文件抽查 L594–605、L1155–1162：样本预算、携入任务/队列计数及暂停条件，未变成逐样本版本硬上限。 | `818dbd59ac0ac977b16d6377edc36bc31609419f` |
| E09 | [delta_weight_transfer.py L216–240](https://github.com/verl-project/verl/blob/1876b06d0a3e4e71e06230be10af14492ca8a75b/verl/workers/rollout/vllm_rollout/delta_weight_transfer.py#L216-L240)：消费端限制及上次 delta 未完成时整作业重启、重收 dense seed 的回归抽查。 | `e05e47518fa1d6c1a519751cb50410b1a0163b5d` |

本轮没有重取论文 PDF/XML、安装镜像或源码压缩包，也没有重新验证三平台组合。未变更项的维持关闭依据为：已核验的第四轮基线、正文与登记的差异检查、当前文字重读及上述定向源码抽查；不冒充对全部外部来源重新开展一次全量初审。

## 二、B25-T04-S2-01：P2 / CLOSED

第五轮不再用一个 ◇ 同时代表“实际存在”“消费必需”与“模式相关”。逐项对照第四轮列出的最小关闭条件，均已满足：

| 子条件 | 当前正文位置 | 复核判定与依据 |
|---|---|---|
| old 锚点是更新必需量，模式只改变生产方式 | L119，合读 L103 | **满足**。所选路径中不能缺 `old_log_probs`；decoupled 重算、bypass 从 rollout 建立，分别对应 E01 与 E03。L1617 的断言位于模式分支之后，不能把“模式条件”解释为某模式可不提供 old。 |
| rollout 的实际产出与消费必需性分开 | L120、L130 | **满足**。E04/E06 支持采样配置与实际返回值的条件性；decoupled 且依赖该量的 IS/RS 关闭时允许缺失，不误判关联故障；bypass 或启用依赖校正时必须取得，缺失则停止进入相应路径/更新，并记录模式与开关。 |
| 不再把当前 actor 数值当作持久化采样字段 | L121，合读 L103 | **满足**。明确是训练侧更新时的计算产物与 ratio 分子；E07 区分 model output 的当前量与输入 old。这里关闭的是“是否为最小持久化样本字段”的混淆，不禁止另行保存调试产物。 |
| reference 的两个可判定分支及不适用状态 | L123 | **满足**。E02 与 E01 对应 `algorithm.use_kl_in_reward` 或 `actor_rollout_ref.actor.use_kl_loss` 任一启用即需要 reference；两者都关闭才将数值/身份记为 `not_applicable` 并保留开关，不虚构 reference 数据。 |
| values 不再声称只有 PPO＋GAE 才可能由上游产出 | L124 | **满足**。正文明确只描述默认 PPO＋GAE/无 critic 的 GRPO 样板，点出 `critic.enable` 覆盖及 `need_critic()`，并排除覆盖配置的适用性。E02 的显式覆盖优先级与 E01 的 `self.use_critic` 门控一致，未把默认样板写成固定实现的排他保证。 |

**重点重开的 L1650–1658 没有被修订误读**：E01 的 decoupled 校正分支同时要求配置存在、batch 含 `rollout_log_probs`、且非 bypass。故“启用依赖该量的校正，但实际未返回数值”可能直接不进入此分支，不能假定上游会普遍自动报错。正文 L130 正是为此增加**本库前置校验规则**，没有宣称改写了上游行为；E03 的显式缺字段报错仍只证明 bypass 分支。

静态分支核对的结果为：decoupled＋依赖校正关闭＋缺 rollout 数值，可继续该样板但 old 仍必需；decoupled＋依赖校正启用＋缺数值，由本库入口规则停止；bypass＋缺数值，停止且上游 helper 也有报错。与 reference 的“两个 KL 开关任一启用”、values 的默认样板边界合读，已区分合法不适用与所选路径缺少必需输入。这里是源码与文档规则的静态核对，不是执行这些配置所得的测试结果。

因此 **S2-01 CLOSED**。不再要求强制所有配方持久化全部数值，也不新增采集器、事务或上游自动校验保证作为本项关闭条件。

## 三、已关闭项回归检查

| 发现 ID | 本轮状态 | 当前正文位置与回归检查 |
|---|---|---|
| B25-T04-C01 | **CLOSED（维持）** | L132、L150–153、L183：预算、轮次与 optimizer 更新单位分立；没有恢复为逐样本版本硬上限。相关段落未改，E08 抽查未否定原关闭依据。 |
| B25-T04-C02 | **CLOSED（维持）** | L161–175：更新结果未知/未持久化时冻结与隔离、checkpoint—账本一致回退、确认持久后只重发、reward 重试与合法 epoch 重用规则保留；L169 必须与 L168 合读，未假定每次更新都有新 checkpoint。E09 的整作业重启边界保留。 |
| B25-T04-C03、B25-T04-R01 | **CLOSED（维持）** | L103、L119–124：默认 decoupled、显式 bypass、IS/RS 默认关闭、四类 logprob 与 KL/优势输入角色未回退；本轮拆表反而使其条件可判定。E01–E07 支持。 |
| B25-T04-C04、B25-T04-R02 | **CLOSED（维持）** | L136–143：跨组传输与 rollout 本地 IPC 两跳、消费端 DP/PP 限制、训练侧分片汇聚、Non-LoRA 边界和布局转换代价均未改；E09 抽查消费端限制。未把 rollout DP=1 推到 trainer。 |
| B25-T04-C05、B25-T04-C06 | **CLOSED（维持）** | L210–215：NVIDIA 多安装路径与容器内代码 ref 分列；Ascend post2/post4 冲突仍 unknown；AMD 镜像/自建代码线独立，未拼接成已验证组合。正文与登记均未改变原证据口径。 |
| B25-T04-C07 | **CLOSED（维持）** | L115–118、L122、L125–128、L167–175：prompt 可回取、uid 组归属、`sample_id=(uid, i)`、递增 attempt、reward/logprob 绑定二元键及消费提交键保留。新增数值行仍受表内同一关联规则约束，不引入脱离 attempt 的第二套身份。未将本库建议账本冒充上游持久化能力。 |
| B25-T04-R03 | **CLOSED（维持）** | L132 未改：恢复后首次发布 K、随后 K+1，步号与权重身份分开。按 E01 同一原文件复核 L1083、L1426–1430 的恢复与首次同步，没有退回通用 0/1 说法。 |
| B25-T04-C08 | **CLOSED（维持）** | L32、L56、L99、L145、L228：V0 机制样板、V1 默认入口与未核对控制流的边界保留；新表没有外推到 V1。 |
| B25-T04-C09 | **CLOSED（维持）** | L198–206：总资源、prompt/组数、有效 token、每样本重用、采样/校正及质量评估预算先固定；阶段/端到端计时分开；收益只归来源作者环境。全文相应段落未改。 |
| B25-T04-C10 | **CLOSED（维持）** | L68、登记 L6356/L6367 与来源记录 L97 未改：PPO/GRPO 摘要主张和实现机制归因仍分立，没有恢复“免除全部 PPO 内存开销”或摘要未建立的实验比较。本轮以第四轮已核验摘要及逐字节一致基线作回归判定，不冒称重读论文全文。 |
| B25-T04-C11 | **CLOSED（维持）** | L60–93 未改：SFT/离线 DPO/在线 RL 对照、五阶段图、发布回边与数据来源说明保留。 |

## 四、新问题检查

**本轮新增独立问题：0 项；未建立 B25-T04-S4-01 或后续 S4 编号。** 检查覆盖新增字段行及前置规则是否与模式默认值、上游门控、样本关联、失败恢复和实现线边界冲突，未发现新的实质问题。未修改的历史来源记录保留当时说法，由后续明确更正和本轮报告承接，不因其未回写第五轮文字另立重复发现。

此处的“未发现”限本轮修订、已关闭项回归及上述源码抽查，不表示所有配方、后端、损失变体或部署组合均已审阅。

## 五、验收条款 1–5 与最终整体判定

| 验收条款 | 第五轮判定 | 依据与边界 |
|---|---|---|
| 1. 五阶段闭环，区分在线 RL / 离线偏好 / SFT | **满足** | C11/C10 维持关闭；闭环、数据来源与论文/实现的归因边界保持，范围为文档证据。 |
| 2. 同步/受控异步样板及数据关联 | **满足** | C07 的关联契约保留，S2-01 已关闭；模式、采样实际产出、消费必需、不适用及缺失入口处置可区分。范围限所选 V0 样板。 |
| 3. 权重同步、陈旧策略、随机性、TP/DP 与资源形态代价 | **满足** | C01/C04/R02/R03 关闭状态保持；预算和版本身份、两跳与端侧限制、布局转换、随机性基线及共置/分离代价均保留，不外推任意布局、LoRA 或 V1。 |
| 4. 吞吐、质量、有效样本及停止/重放/重复计算 | **满足** | C02 的恢复与计数规则、C07 的样本关联和 S2-01 的必需输入门槛共同闭合；生成/训练吞吐、队列、滞后和质量口径仍在。规则是本库建议，不是上游 exactly-once 或事务实现保证。 |
| 5. 单变量验证、公开样板与三平台支持条件 | **满足** | C05/C06/C08/C09 维持关闭；可比工作量与公开实现分立、三平台官方证据线及 unknown 边界保留。满足的是文档核实要求，不是三平台实测支持认证。 |

**最终整体判定：T06-04 通过既定审阅范围。** 初审 C01–C11 共 11 项、第二轮新增 R01–R03 共 3 项、第三轮新增 S2-01 共 1 项，累计 **15 项 CLOSED、0 项 OPEN**；第五轮无新增独立发现。无需再因 S2-01 阻塞 T06-04，但本报告不代替其他 Batch 25 任务的验收，不自动变更计划状态、正文 `draft / source_checked` 或任何硬件验证状态。

## 六、校验与变更边界

- 本轮只新增本报告；不修改正文、来源登记、来源记录、导航、计划、历史报告或 `src/kb/`，不提交、不建分支。既有未提交工作保留。
- 执行 `make check`：通过，**107 content entries / 525 sources**。为不改写原工作区生成物，在完整临时副本（包含已有 `build/` 链接目标）执行 `make build`：通过，同为 **107 / 525**，生成两份 catalog。两项检查只验证结构、引用与本地链接，不验证技术正确性、远程来源或平台兼容。
- 本轮输入快照、工作区文件指纹与校验日志保留在 `/private/tmp/b25-t06-04-recheck4.F7b6Pu/`。未改 `src/kb/`，未增加或运行代码测试；分支核对是静态审阅。
- 三份审阅输入的前后指纹一致，执行前已有的文件未观察到变化；期间另观察到其他任务新增 `batch-25-t06-05-codex-recheck-2.md`、`batch-25-t06-06-codex-recheck-2.md`，本轮未写入、回滚或改写它们，不把这些并行变化计作 T06-04 的产出。
- 未运行 RL 训练、rollout、权重发布、容器安装、失败注入或 GPU/NPU 测试；模型审阅、来源核对、结构校验与真实环境验证仍分别成立。
