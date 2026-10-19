# Batch 25 T06-04 第二轮定向复核报告

- 日期：2026-10-20（Asia/Shanghai）。
- 审阅对象：[修订正文](../../knowledge/06-training/rl-rollout-consistency.md)、[来源记录](batch-25-t06-04-sources.md)及[来源登记](../../sources/registry.yaml)；对照[初审 C01–C11](batch-25-t06-04-codex-review.md)与 [T06-04 验收条款](../../plans/full-coverage-backlog.yaml)。正文位置均指本轮读取的 **204 行版本**，SHA-256 为 `94b2f1711c0581918fa018801a0a01afabc8a71c70a1aa0f03162464bdbfc975`；来源记录为 82 行，SHA-256 为 `62898bebbe79e4b921ece36523db0e0be35690a496aaf4fe827f24f7516a96f8`。
- 执行角色：本地 Codex CLI 定向复核者；仅新增本报告，不修改正文、来源记录、登记或导航。约定模型为 `gpt-6.1-sol / xhigh`；本会话无法独立读取实际模型路由与推理档位元数据，实际执行标识记为 unknown，不把约定标识冒充运行核验结果。
- 结论摘要：初审 **4 项 CLOSED、7 项 OPEN**；另发现 **3 项新增 P2**（R01–R03）。修订显著改善了结构和证据边界，但仍不能宣布 T06-04 审阅通过。

## 一、初审发现逐项判定

### 取证方法与固定位置

重新读取仓库约定和修订材料，并重新打开上游，不以初审摘要或作者补充表代替原文。[tag 接口](https://api.github.com/repos/verl-project/verl/git/ref/tags/v0.9.1)本轮仍将 verl v0.9.1 解析为 `1876b06d0a3e4e71e06230be10af14492ca8a75b`。下列 verl 源码/文档链接均使用该 commit 的原文件坐标，而非网页工具重排的行号。

本轮通过 GitHub 连接工具重开 **24 个 verl 文件、两个 MindSpeed-LLM 文件**，取得各完整文件的 blob SHA；对 `/private/tmp/b25/` 已有取回物独立计算 Git blob SHA，26 项全部相符，随后据原文件阅读相关段落。另重开 docker 目录、release 说明和四篇 arXiv 摘要。不是仅凭缓存目录名认定版本；本轮未重新下载源码包或论文 XML，也未把既有包的完整性等同于新一次网络下载。

| 证据组 | 本轮重新核对的位置与用途 |
|---|---|
| E01：样本预算与一步异步 | [fully_async.md L94–146](https://github.com/verl-project/verl/blob/1876b06d0a3e4e71e06230be10af14492ca8a75b/docs/advance/fully_async.md#L94-L146)、[fully_async_rollouter.py L491–507](https://github.com/verl-project/verl/blob/1876b06d0a3e4e71e06230be10af14492ca8a75b/verl/experimental/fully_async_policy/fully_async_rollouter.py#L491-L507)、[one_step_off.md L11–48](https://github.com/verl-project/verl/blob/1876b06d0a3e4e71e06230be10af14492ca8a75b/docs/advance/one_step_off.md#L11-L48)：同步周期、历史超额样本及 trainer step 的单位。 |
| E02：logprob 与优势 | [ray_trainer.py L218–279](https://github.com/verl-project/verl/blob/1876b06d0a3e4e71e06230be10af14492ca8a75b/verl/trainer/ppo/ray_trainer.py#L218-L279)、[L1570–1597](https://github.com/verl-project/verl/blob/1876b06d0a3e4e71e06230be10af14492ca8a75b/verl/trainer/ppo/ray_trainer.py#L1570-L1597)、[L1638–1674](https://github.com/verl-project/verl/blob/1876b06d0a3e4e71e06230be10af14492ca8a75b/verl/trainer/ppo/ray_trainer.py#L1638-L1674)、[rollout_correction.yaml L5–20](https://github.com/verl-project/verl/blob/1876b06d0a3e4e71e06230be10af14492ca8a75b/verl/trainer/config/algorithm/rollout_correction.yaml#L5-L20)：默认非 bypass、校正开关、GAE/GRPO 输入与 optimal-token-baseline 分支。 |
| E03：发布与恢复 | [ray_trainer.py L983–1050](https://github.com/verl-project/verl/blob/1876b06d0a3e4e71e06230be10af14492ca8a75b/verl/trainer/ppo/ray_trainer.py#L983-L1050)、[L1052–1115](https://github.com/verl-project/verl/blob/1876b06d0a3e4e71e06230be10af14492ca8a75b/verl/trainer/ppo/ray_trainer.py#L1052-L1115)、[L1426–1491](https://github.com/verl-project/verl/blob/1876b06d0a3e4e71e06230be10af14492ca8a75b/verl/trainer/ppo/ray_trainer.py#L1426-L1491)、[L1690–1716](https://github.com/verl-project/verl/blob/1876b06d0a3e4e71e06230be10af14492ca8a75b/verl/trainer/ppo/ray_trainer.py#L1690-L1716)：检查点保存条件、恢复步号、uid、更新/保存/发布顺序。 |
| E04：两跳传输与 delta | [delta_checkpoint_engine.py L14–42](https://github.com/verl-project/verl/blob/1876b06d0a3e4e71e06230be10af14492ca8a75b/verl/checkpoint_engine/delta_checkpoint_engine.py#L14-L42)、[delta_weight_transfer.py L216–240](https://github.com/verl-project/verl/blob/1876b06d0a3e4e71e06230be10af14492ca8a75b/verl/workers/rollout/vllm_rollout/delta_weight_transfer.py#L216-L240)、[vllm_async_server.py L1141–1168](https://github.com/verl-project/verl/blob/1876b06d0a3e4e71e06230be10af14492ca8a75b/verl/workers/rollout/vllm_rollout/vllm_async_server.py#L1141-L1168)、[FSDP transformer_impl.py L918–958](https://github.com/verl-project/verl/blob/1876b06d0a3e4e71e06230be10af14492ca8a75b/verl/workers/engine/fsdp/transformer_impl.py#L918-L958)。另重读 [vllm_rollout.py L194–260](https://github.com/verl-project/verl/blob/1876b06d0a3e4e71e06230be10af14492ca8a75b/verl/workers/rollout/vllm_rollout/vllm_rollout.py#L194-L260)。 |
| E05：实现线 | [ppo_trainer.yaml L38–40](https://github.com/verl-project/verl/blob/1876b06d0a3e4e71e06230be10af14492ca8a75b/verl/trainer/config/ppo_trainer.yaml#L38-L40)、[L228–238](https://github.com/verl-project/verl/blob/1876b06d0a3e4e71e06230be10af14492ca8a75b/verl/trainer/config/ppo_trainer.yaml#L228-L238)、[main_ppo.py L183–192](https://github.com/verl-project/verl/blob/1876b06d0a3e4e71e06230be10af14492ca8a75b/verl/trainer/main_ppo.py#L183-L192)及 [v0.9.1 release](https://github.com/verl-project/verl/releases/tag/v0.9.1)：V1 默认入口与 legacy recipe 的分立。 |
| E06：Ascend | [install_guidance.rst L9–17](https://github.com/verl-project/verl/blob/1876b06d0a3e4e71e06230be10af14492ca8a75b/docs/ascend_tutorial/zh/get_start/install_guidance.rst#L9-L17)、[L84–108](https://github.com/verl-project/verl/blob/1876b06d0a3e4e71e06230be10af14492ca8a75b/docs/ascend_tutorial/zh/get_start/install_guidance.rst#L84-L108)、[ascend_backend_features.md L10–39](https://github.com/verl-project/verl/blob/1876b06d0a3e4e71e06230be10af14492ca8a75b/docs/ascend_tutorial/zh/feature_support/ascend_backend_features.md#L10-L39)：post2/post4 差异及推理后端、参数映射。 |
| E07：NVIDIA 安装与容器边界 | [install.rst L4–27](https://github.com/verl-project/verl/blob/1876b06d0a3e4e71e06230be10af14492ca8a75b/docs/start/install.rst#L4-L27)、[L50–76](https://github.com/verl-project/verl/blob/1876b06d0a3e4e71e06230be10af14492ca8a75b/docs/start/install.rst#L50-L76)、[固定 docker 目录](https://github.com/verl-project/verl/tree/1876b06d0a3e4e71e06230be10af14492ca8a75b/docker)、[docker/README.md L1–59](https://github.com/verl-project/verl/blob/1876b06d0a3e4e71e06230be10af14492ca8a75b/docker/README.md#L1-L59)、[Dockerfile.stable.vllm L1–22](https://github.com/verl-project/verl/blob/1876b06d0a3e4e71e06230be10af14492ca8a75b/docker/Dockerfile.stable.vllm#L1-L22)：最低要求不等于选定的锁定环境。 |
| E08：AMD 细节 | [amd_quick_start.rst L15–42](https://github.com/verl-project/verl/blob/1876b06d0a3e4e71e06230be10af14492ca8a75b/docs/amd_tutorial/amd_quick_start.rst#L15-L42)、[L83–142](https://github.com/verl-project/verl/blob/1876b06d0a3e4e71e06230be10af14492ca8a75b/docs/amd_tutorial/amd_quick_start.rst#L83-L142)、[docker/rocm/Dockerfile.rocm L1–54](https://github.com/verl-project/verl/blob/1876b06d0a3e4e71e06230be10af14492ca8a75b/docker/rocm/Dockerfile.rocm#L1-L54)：硬件/模式表、示例，以及自建镜像另有源代码 ref。 |
| E09：算法与论文证据分工 | 重开 [PPO 实现文档](https://github.com/verl-project/verl/blob/1876b06d0a3e4e71e06230be10af14492ca8a75b/docs/algo/ppo.md)、[GRPO 实现文档](https://github.com/verl-project/verl/blob/1876b06d0a3e4e71e06230be10af14492ca8a75b/docs/algo/grpo.md)、[HybridFlow 指南](https://github.com/verl-project/verl/blob/1876b06d0a3e4e71e06230be10af14492ca8a75b/docs/hybrid_flow.rst)、[Online DPO L28–41](https://github.com/verl-project/verl/blob/1876b06d0a3e4e71e06230be10af14492ca8a75b/docs/advance/dpo_extension.rst#L28-L41)、[最佳实践](https://github.com/verl-project/verl/blob/1876b06d0a3e4e71e06230be10af14492ca8a75b/docs/perf/best_practices.rst)；论文仅重开 [PPO 摘要](https://arxiv.org/abs/1707.06347)、[DeepSeekMath 摘要](https://arxiv.org/abs/2402.03300)、[DPO 摘要](https://arxiv.org/abs/2305.18290)、[HybridFlow 摘要](https://arxiv.org/abs/2409.19256)，没有补做论文全文核验。 |

MindSpeed-LLM 的两个文件另以初审固定 commit `53f3639c3da9c000a187c44cc0c08d55026ddded` 重开：[TrlPPOTrainer.py](https://github.com/Ascend/MindSpeed-LLM/blob/53f3639c3da9c000a187c44cc0c08d55026ddded/mindspeed_llm/tasks/posttrain/trl_ppo/TrlPPOTrainer.py)、[TrlPPOEngine.py](https://github.com/Ascend/MindSpeed-LLM/blob/53f3639c3da9c000a187c44cc0c08d55026ddded/mindspeed_llm/tasks/posttrain/trl_ppo/TrlPPOEngine.py)。正文仍把它与 verl 分立，未扩大到已核实采样后端，本轮未发现该段新增问题。

新增安装文件的 SHA-256 复算为 `8ca5ce30c91222bc9b894b8cba25d69b44c64234ab7e185b20750127e29a33b3`，与登记一致；AMD quick start 为 `f7cbcab68c3e05c7aa50d40cbbe5491765d95b792e2da15f6f6314458bd18163`，也与记录一致。新增登记存在、摘要正确覆盖安装页开头，不代表其后不同安装路径已合并成确定配套。

### 逐项判定表

“优先级”保留初审级别；C01 的主要 P1 误保证已纠正，当前剩余问题按 P2 处理。CLOSED 指本轮原发现的关闭条件已满足，不表示硬件验证通过；OPEN 不因新增了一段说明而自动关闭。

| 初审 ID | 初审优先级 | 判定 | 修订位置 | 理由与剩余关闭条件 |
|---|---|---|---|---|
| B25-T04-C01 | P1 | **OPEN** | 正文 L127–130、L157、L195；来源记录 L41、L76；登记 `src.verl.fully-async-v0.9.1` | 已撤回“阈值等于逐样本版本硬上限”，并区分发布与训练计数，核心安全误保证已修正。但 L128 把扣减项改成未限定窗口的“已产出样本”；E01 原文特指**上一轮超额产生、携入的旧样本**。L127 又把 one-step 定为 optimizer 更新轮次，而 E01 的 step 是一次采样/训练轮次，内部可含多个 mini-batch/epoch 的 optimizer 更新。须明确这两个单位，给出同步滞后归一化定义，并将登记“新鲜度控制”补充为预算控制边界。 |
| B25-T04-C02 | P1 | **OPEN** | 正文 L136–149、L178 | 已覆盖六类失败位置、合法 epoch 重用和 delta 整作业重启，方向正确。但仍未定义停止更新/发布与隔离进行中请求的条件，也未定义 sample/attempt/update 的持久提交边界。L145 假定总有“更新后的 checkpoint”；E03 显示保存受 `save_freq` 等条件限制，更新成功后可能还没有可恢复检查点。必须补足“更新结果未知/未持久化”时的回退和账本一致恢复规则；详见本节剩余问题说明。 |
| B25-T04-C03 | P2 | **OPEN** | 正文 L99、L167；来源记录 L45、L78；登记 `src.verl.ray-trainer-source-v0.9.1` | GAE/GRPO 直接输入、reward KL 与 actor KL loss 已分开，但“V0 默认（bypass）”是新增错误（R01）。登记仍保留“old_log_probs 参与优势计算（GAE path-variance 代理）”，与 E02 中该分支属于 optimal-token-baseline 的事实冲突；来源记录原表也仍是泛化说法。须修正默认值与校正启用条件，并在登记及来源记录中明确哪些旧摘要已被替代。 |
| B25-T04-C04 | P2 | **OPEN** | 正文 L113–119、L134；来源记录 L44、L77；登记 `src.verl.vllm-rollout-source-v0.9.1` | 两跳、分离式 delta、稀疏位置/值及布局转换成本已补齐。但把 vLLM **推理侧** DP/PP 限制写成“训练侧”是新增错误（R02）；“不预设 LoRA 之外的适用范围”仍容易保留 LoRA 已支持的暗示，而 E04 的 FSDP shard 路径明确为 Non-LoRA base path。登记还沿用未区分两跳的“要求共置 CUDA IPC”，未把新增 delta/server/FSDP 文件及适用范围纳入可追踪登记。须更正限制作用域、去除 LoRA 预设并补齐来源追踪。 |
| B25-T04-C05 | P2 | **CLOSED** | 正文 L187、L202；来源记录 L79；登记 `src.verl.ascend-install-v0.9.1` | E06 再次确认更新条目 post2 与组件表 post4 的差异。正文现已明确标冲突、实际 post 选择 unknown，并与 v0.14.0rc1 线分立；来源补充表明确记录该冲突，登记亦保留两处不同值，不再由正文拼成确定配套。保留首轮历史记录可以，但后续汇总应以本轮明确的 unknown 为准。此项关闭不表示 Ascend 配套已消解。 |
| B25-T04-C06 | P2 | **OPEN** | 正文 L186、L189；来源记录 L73–74；登记 `src.verl.install-v0.9.1`、`src.verl.amd-quickstart-v0.9.1` | AMD 硬件、后端、模式、镜像、驱动与设备访问声明已按 E08 正确补入，新增安装来源也有效。NVIDIA 仍只摘安装页开头最低要求，未选定具体安装/硬件架构线或记录页内版本差异；“本页全部机制证据来自该组合”仍超出所建证据。docker 路径另含独立代码 ref，不能直接当作相同 v0.9.1 栈，详见后文。剩余要求是来源级配套边界，不是补硬件实测。 |
| B25-T04-C07 | P2 | **OPEN** | 正文 L105–109、L144–149、L157；来源记录 L78 | verifier 代码/配置身份、上游 uid 与建议自建账本的区分已补充。但仍只提到 `sample_id`/`attempt`，没有定义 prompt/group/response/request/attempt 的键关系及 reward/logprob 如何关联，也没有 run/恢复代次与 update 提交键。L109 的“恢复后首发布 0”还是新增错误（R03）。须给出最小记录示例或等价字段契约，并定义同步模式中按实际权重身份归一化的零滞后；不能只要求观察“恒定”。 |
| B25-T04-C08 | P2 | **CLOSED** | 正文 L30、L52、L95、L120、L122、L202；来源记录 L75 | E05 确认 V1 默认入口和模式名、legacy 分流及 recipe 迁出说明。正文已选择 V0 结构样板，显式排除 V1 控制流取证及参数直接拼用，模式表也标为 V0 recipe；来源补充表同步标识。无需为了关闭本项扩查 V1 全部控制流。bypass 的错误另归 C03/R01，不改变此项实现线声明已补齐的判断。 |
| B25-T04-C09 | P2 | **CLOSED** | 正文 L128–130、L155–161、L172–180、L194；来源记录 L80 | 现已要求固定总资源、prompt/组数、有效训练 token、每样本更新次数、采样/校正及评估预算，明确 streaming 不用 `train_batch_size`、需由同步周期参数对齐，并分开阶段/端到端计时；不再断言“吞吐最高/一定提高”。E01 的工作量对齐关系和完全异步文档的重叠收益说明支持该方法。此为验证设计的关闭，不宣称实际比较已完成；C01 的单位修正仍须落实。 |
| B25-T04-C10 | P2 | **OPEN** | 正文 L64；来源记录 L49–52、L82；四篇论文登记 notes | GRPO 与 HybridFlow 的正文机制已主要转引实现文档，但 L64 仍把 clipped surrogate objective 直接归于“PPO 摘要”。E09 中该摘要只展开 surrogate objective、多 epoch minibatch 等概述，未给出 clipped 细节。登记仍有 PPO“免二阶导”、DeepSeekMath“组均值 baseline/免 critic”等超出已取摘要的表述；L82 所称“登记 notes 已分列”与实际文件不符。须把这些细节转给已核实实现文档，或另补固定论文全文证据，并纠正修订记录。 |
| B25-T04-C11 | P3 | **CLOSED** | 正文 L58–89 | 已有五阶段及新 policy 回边图；“数据从哪来”章节实际存在，静态 SFT/离线 DPO 与在线 RL、Online DPO 的边界已交代；PPO critic 与 GRPO 无 critic 也标明。E09 的实现文档支持这些结构性对照。图中文字排版可继续优化，但不再构成本项阻塞。 |

### 未关闭项的关键剩余问题

**C02：不能用一个去重键替代恢复事务。** L144 的“跳过已消费样本”必须限定账本与所恢复 checkpoint 一致；若恢复了旧权重/优化器状态，却保留更新后才写入的消费记录，就会跳过实际已被回滚的更新。反过来，更新已持久化却回退账本会重复更新。L145 还缺“更新后未落盘或提交结果未知”的分支。最少应明确：停止新采样/新更新/新发布的触发条件；冻结或隔离 in-flight/队列；以 run、attempt、update、checkpoint/发布身份关联提交记录；已持久提交则只重发，不确定则回到同一完整边界并重放相应输入。重放需说明复用哪些 tokens、采样策略、reward/verifier 身份与计数，reward 重试不得重复计入；GRPO 还要保持组归属。没有证据时不能承诺 exactly-once。E03 的条件式 checkpoint 与 E04 的 delta 整作业重启要求共同限定这条规则。

**C06：需要选择来源路径，而不是继续罗列最低版本。** 重新打开安装页后，同页开头的 `core_v0.13.1` 声明与 uv 路径的 `core_v0.18.0` / megatron-bridge 0.5.2 并存；uv 段还具体限定 Linux、Python 3.12、x86_64/aarch64，以及 cu130/torch 2.11 的轮子线。docker README 提醒 GB200/aarch64 当时没有预构建镜像；固定 `Dockerfile.stable.vllm` 又列 CUDA 13.0.2、Torch 2.11.0、vLLM 版本/架构差异，且另设 `VERL_VERSION=v0.7.1`。不能把这些当成同一个由“CUDA>=12.8、vLLM>=0.18.0”即可充分描述的可复现组合。

AMD quick start 的支持表和示例已核实，不应再说“仅确认入口存在”。但正文“或 docker/rocm 自建”也须说明：固定 Dockerfile 的默认 `VERL_TAG=7b19203c52503760f92e0368067c7eb744236274` 并不是本页 v0.9.1 commit，vLLM 也有独立 ref（E08）。保留镜像内精确引擎/代码组合未核实为 unknown 即可，不要求运行镜像；若把自建路径作为所选 v0.9.1 样板，则须核清覆盖参数和实际 checkout，而非由 Dockerfile 所在 tag 推导其安装代码的 tag。

**登记与历史来源表的处理边界。** 不要求涂改首轮历史证据，但应明确被修订覆盖的主张及当前有效表述。`src.verl.ray-trainer-source-v0.9.1` 的 GAE/path-variance 错误和论文 notes 的摘要越界仍是当前登记内容，不能由追加一行“正文已改”消除。delta 新增关键文件也应以独立来源项或扩充现有分组登记的方式记录具体路径、版本和适用范围；只在初审报告里有链接不足以让正文的依赖登记完整。

## 二、新发现列表

下列均为修订新增的具体错误。它们与 C03/C04/C07 的未关闭原因交叉，保留新 ID 便于下一轮定向复核，不把同一错误另算成新的独立根因。

### B25-T04-R01 — P2 / OPEN：把 bypass 写成 V0 默认，且未保留校正的启用条件

- **位置**：正文 L99。
- **问题**：新增“V0 默认（bypass）路径”与所选固定配置相反。`ppo_trainer.yaml` 引入 `algorithm.rollout_correction`，其 `bypass_mode` 默认 **false**；`ray_trainer.py` 缺省取值也为 false，走训练侧重算 `old_log_probs` 的分支。与此同时，decoupled 的 rollout 校正不是无条件发生：需相应数据/配置，重要性权重与拒绝采样各有开关，默认 `rollout_is`、`rollout_rs` 为 null。
- **证据**：E02、E05；重点为 [rollout_correction.yaml L5–20](https://github.com/verl-project/verl/blob/1876b06d0a3e4e71e06230be10af14492ca8a75b/verl/trainer/config/algorithm/rollout_correction.yaml#L5-L20)及 [ray_trainer.py L1574–1586](https://github.com/verl-project/verl/blob/1876b06d0a3e4e71e06230be10af14492ca8a75b/verl/trainer/ppo/ray_trainer.py#L1574-L1586)。
- **影响/关闭条件**：默认实验可能被误判为必须满足 `old_log_probs == rollout_log_probs`，也可能在校正关闭时误以为分布偏移已被处理。改为“显式启用 bypass 时”的条件叙述，或明确选用一个确实覆盖为 true 的固定 recipe；明确当前 actor 为 ratio 分子、proximal-old 为分母，decoupled 的校正按配置启用，不把另一条合法路径判成异常。同步修正 C03 的登记摘要。

### B25-T04-R02 — P2 / OPEN：将 vLLM rollout 的 DP/PP 限制错安到训练侧

- **位置**：正文 L116。
- **问题**：新增“训练侧 DP=1 且 PP=1”不由被引用限制建立。`delta_weight_transfer.py` 的 `parallel_config` 属 vLLM 消费端，配合 `vllm_async_server.py` 检查的是 **rollout 的 data/pipeline parallel size**，不是训练引擎的 DP/PP。跨组 delta 发送路径还显式汇聚训练分片；不能由消费端限制推导 trainer 必须 DP=1，也不能反向承诺任意 trainer 布局均受支持。
- **证据**：E04；特别是 [vllm_async_server.py L1153–1164](https://github.com/verl-project/verl/blob/1876b06d0a3e4e71e06230be10af14492ca8a75b/verl/workers/rollout/vllm_rollout/vllm_async_server.py#L1153-L1164)与 [delta_checkpoint_engine.py L14–42](https://github.com/verl-project/verl/blob/1876b06d0a3e4e71e06230be10af14492ca8a75b/verl/checkpoint_engine/delta_checkpoint_engine.py#L14-L42)。
- **影响/关闭条件**：会错误排除训练 DP>1 的布局，或遗漏 rollout DP>1 的真正限制。分别记录 producer 与 consumer 的限制，把此处改为 vLLM rollout DP=1/PP=1、BF16、无量化/投机/PD 分离；训练后端的导出、分片汇聚及 LoRA 支持另以所选实现证据界定。不得把本轮发现解读成已核实所有训练布局可用。

### B25-T04-R03 — P2 / OPEN：把从零启动的 0/1 步号例子误写成恢复后的恒定规则

- **位置**：正文 L109；来源记录 L78。
- **问题**：修订写“恢复后的首次发布用步号 0，而训练循环的 trace 步号从 1 起”。实际 `fit()` 虽先初始化为 0，但紧接着 `_load_checkpoint()` 会从 `global_step_K` 恢复 `self.global_steps=K`，首次同步使用 K，之后循环才递增为 K+1。**0/1 只是从零启动的特例**，不是所有恢复都会重置发布身份。
- **证据**：E03；[ray_trainer.py L1081–1084](https://github.com/verl-project/verl/blob/1876b06d0a3e4e71e06230be10af14492ca8a75b/verl/trainer/ppo/ray_trainer.py#L1081-L1084)及 [L1426–1451](https://github.com/verl-project/verl/blob/1876b06d0a3e4e71e06230be10af14492ca8a75b/verl/trainer/ppo/ray_trainer.py#L1426-L1451)。
- **影响/关闭条件**：可能导致恢复后的版本归一化、旧队列过滤和去重账本使用错误偏移。改为“首次发布为 0 或恢复步 K；下一次采样 trace 为 1 或 K+1”，再说明步号标签与实际权重身份不同，加入 run/恢复代次，不能仅凭标签差值计算策略滞后；来源补充表也须一并纠正。

## 三、总体判定

**本轮定向复核不通过；不能将 T06-04 或 Batch 25 据此标为审阅通过。**

初审 11 项中，C05/C08/C09/C11 共 **4 项关闭**，C01/C02/C03/C04/C06/C07/C10 共 **7 项仍开放**；新增 R01–R03 共 **3 项 P2**。C01 的错误硬上限保证已移除，剩余按 P2 处理；C02 的失败恢复与持久提交边界仍属 P1 阻塞。新增项与旧项存在上述交叉，不按 ID 数量推断独立根因数量。

| 验收条款 | 本轮整体判定 | 依据与剩余条件 |
|---|---|---|
| 1. 五阶段闭环，区分在线 RL / 离线偏好 / SFT | **展示已满足，来源边界未完全满足** | 闭环图、回边与 DPO 对照使 C11 关闭；PPO 摘要归因及登记越界仍需按 C10 修正。无需为关闭此项强制新增硬件或论文全文实验。 |
| 2. 同步/受控异步样板与样本数据关联 | **未满足** | V0/V1 选择已明确；但 C03/C07、R01/R03 的默认 logprob 路径、样本键和恢复版本规则仍错误或不完整，C01 的轮次单位也未闭合。 |
| 3. 权重同步、陈旧策略、随机性、TP/DP 与共置/分离代价 | **部分满足，未通过** | 两跳、布局转换成本及随机性检查已补充；C01/C04、R02 的单位与限制作用域仍须修正，不能以泛化并行度说明替代所选导出路径的支持边界。 |
| 4. 吞吐/质量/有效样本指标及停止、重放、重复计算 | **未满足，P1 阻塞** | 指标类别与合法 epoch 重用已区分，delta 整作业重启也正确；C02 仍缺停止/隔离和 checkpoint—账本—更新提交一致性，尤其未覆盖“更新已执行但未持久化/结果未知”。 |
| 5. 单变量方法、公开样板与 NVIDIA/Ascend/AMD 支持条件 | **方法已改善，平台配套尚未闭合** | C09 的可比预算与有条件收益说明通过；C05 的 Ascend 冲突处理通过，AMD 声明已补实；C06 的 NVIDIA 安装路径/架构/版本分立及 docker 内部代码 ref 仍须说明。 |

### 校验与变更边界

- 报告落盘后执行 `make check`：通过，**107 content entries / 523 sources**；在临时仓库快照执行 `make build`：通过，同为 **107 / 523**，生成两份 catalog。用户仓库已有的 `build/` 未修改。这些结果只证明结构、ID、登记引用与本地文件链接，不证明技术正确性、远程内容或平台兼容。
- 本轮不修改 `src/kb/`，不新增测试，不执行 RL、rollout、参数同步、故障重放、容器安装或 GPU/NPU 基准；`draft / source_checked` 与模型审阅、真实环境验证继续分开。
- 后续应只针对仍开放的旧项和 R01–R03 修订并定向复核；不能以结构校验、来源 hash 相符或补充取证表中的“已改”替代技术关闭判定。
