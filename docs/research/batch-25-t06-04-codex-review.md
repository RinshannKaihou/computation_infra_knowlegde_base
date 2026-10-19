# Batch 25 T06-04 初审报告（gpt-6.1-sol / xhigh）

- 日期：2026-10-20（Asia/Shanghai）。
- 审阅对象：[RL rollout、权重同步与训练推理协同](../../knowledge/06-training/rl-rollout-consistency.md)，下述正文行号对应本轮读取的 161 行版本。
- 关联材料：[来源记录](batch-25-t06-04-sources.md)、[来源登记](../../sources/registry.yaml)、[T06-04 验收条款](../../plans/full-coverage-backlog.yaml)、06 章导航与预训练/微调正文。
- 执行范围：本地 Codex CLI 独立初审，只新增本报告；未修改正文、导航或登记表，未运行 RL、rollout、参数同步、故障注入或硬件基准。实际模型路由与推理档位的运行元数据无法由本会话独立读取，记为 unknown；标题采用任务指定标识，不把标题当作模型路由核验凭据。

## 核对方法与证据边界

1. 重新读取 README、写作指南、内容边界、目标正文和来源记录，逐项核对机制、参数、适用范围与验收条款；未以作者的来源摘要代替上游正文。
2. 重新打开 12 个 T06-04 verl 文档/源码文件、四篇 arXiv 摘要页、MindSpeed-LLM 的 `TrlPPOTrainer.py` / `TrlPPOEngine.py` 和两仓库 LICENSE；对疑点进一步打开参数同步实现、V1 入口/配置和安装文档。
3. GitHub API 确认旧仓库地址重定向至 `verl-project/verl`。重新解析 [verl v0.9.1 tag](https://api.github.com/repos/verl-project/verl/git/ref/tags/v0.9.1)，commit 为 `1876b06d0a3e4e71e06230be10af14492ca8a75b`；[MindSpeed-LLM v2.2.0 tag](https://api.github.com/repos/Ascend/MindSpeed-LLM/git/ref/tags/v2.2.0)，commit 为 `53f3639c3da9c000a187c44cc0c08d55026ddded`。以下 GitHub 行号均按原文件字节核对，不采用网页工具重排后的坐标。
4. 终端直连 raw.githubusercontent.com 的 DNS 解析失败，因此经连接工具重新打开上游，并从 GitHub 固定 commit 文件接口取得完整文件的 blob SHA。对 `/private/tmp/b25/` 中已有的 12 个 verl 文件、两个 MindSpeed 文件及两个 LICENSE，独立计算 Git blob SHA，与上游返回的 SHA 全部一致；在此基础上阅读完整缓存原文件并重算 SHA-256。不是只凭本地目录名认定它属于指定 tag。
5. 来源记录表中的 20 个对象（两个源码包、14 个仓库文件、四个 arXiv XML）的本地 SHA-256 均与记录/登记的完整值或前缀一致。两个包分别为 `cef878a5ccc98491dd33af8aed0572ce44bae8e81d95897d8c4ba23e2b68a218`、`693f619a8b608726c23dc53a7e0d283684883149fb140951f169a297fe72936e`。包与 XML 本轮未重新下载；其摘要核对属于已有取回物的完整性复算，不冒充独立网络下载验证。四篇摘要页已另外重新打开核对语义。
6. 来源记录所称 2026-09-20 发布 v0.9.1，与本轮 GitHub release 返回的 `published_at=2026-09-20T07:24:43Z` 一致；查询时 `/releases/latest` 也返回该正式版本。不将这个时点观察写成永久的“最新版”。

## 发现列表

### B25-T04-C01 — P1：把样本超前预算误写成策略版本滞后硬上限

- **受影响位置**：正文第 99、117、130、136 行；来源记录第 41 行；登记项 `src.verl.fully-async-v0.9.1` 的新鲜度说明。
- **问题描述**：正文将 `staleness_threshold` 解释成“允许的版本滞后”，并要求版本差对照该参数的“上限”。但引用的 fully-async 样板用它控制每次参数同步周期内允许超前产生的样本预算，不是逐样本 `learner_version - behavior_version <= threshold` 的硬过滤器。小数阈值也不能直接解释为小数个已发布权重版本。这样观测和调参会把预算控制误当成版本安全保证。
- **重新打开的证据**：[fully_async.md 原文件 L118–146](https://github.com/verl-project/verl/blob/1876b06d0a3e4e71e06230be10af14492ca8a75b/docs/advance/fully_async.md#L118-L146) 区分本地更新次数与参数同步周期，并给出 `(1 + staleness_threshold) * (trigger_parameter_sync_step * require_batches * ppo_mini_batch_size) - num_staleness_sample`。实现 [fully_async_rollouter.py L491–507](https://github.com/verl-project/verl/blob/1876b06d0a3e4e71e06230be10af14492ca8a75b/verl/experimental/fully_async_policy/fully_async_rollouter.py#L491-L507) 据此计算 `max_required_samples`、并发量和队列容量。
- **建议关闭条件**：按该 recipe 的真实语义定义参数及计数单位；分开记录本地 optimizer 更新、发布轮次和样本行为策略版本；版本滞后分布单独观测。若本库建议额外的版本硬上限，明确标为本库建议并说明超限样本的处理，不声称此参数已经实现它。同步/一步异步的“0/一步”也须声明所用版本单位。

### B25-T04-C02 — P1：缺少停止、失败重放和重复计算规则，增量发布失败尤其危险

- **受影响位置**：正文“异常区分检查与验证”第 123–138 行，权重同步第 87–91 行，观察口径第 115–120 行。
- **问题描述**：保存 checkpoint 和样本记录并不自动“保证可回放”。全文没有定义哪些异常必须停止更新/发布、队列与进行中请求如何处理、reward/更新重试是否可重复计入、如何区分合法 `ppo_epochs` 重用与故障导致的重复消费，也没有说明部分权重已写入后的恢复边界。这直接遗漏验收条款 4，而非要求作者补一份运行结果。
- **重新打开的证据**：[delta_weight_transfer.py L234–240](https://github.com/verl-project/verl/blob/1876b06d0a3e4e71e06230be10af14492ca8a75b/verl/workers/rollout/vllm_rollout/delta_weight_transfer.py#L234-L240) 明确规定：上次 delta 更新未完成时，须重启整个作业并重新接收 dense seed；仅重启 vLLM worker 不安全。现有 [ray_trainer.py L1030–1050](https://github.com/verl-project/verl/blob/1876b06d0a3e4e71e06230be10af14492ca8a75b/verl/trainer/ppo/ray_trainer.py#L1030-L1050) 保存 dataloader 状态/检查点标记，不能据此证明异步消息消费和参数发布已具备 exactly-once 事务。
- **建议关闭条件**：增加最小状态/处置表，覆盖采样失败、reward 失败、更新前失败、更新后发布失败、部分 delta 写入、重启后队列残留。明确样本/attempt/update 的标识、去重账本、成功提交边界、重放应复用哪些权重/token/reward、计数是否回滚，以及必须停止的条件。将这些标为本库一致性建议；不能把未取证的运行时保证写成框架已有特性，并保留该 delta 实现的整作业重启限制。

### B25-T04-C03 — P2：混淆 rollout、proximal-old、reference logprob 与优势计算

- **受影响位置**：正文第 73、81、101、127、129 行；来源记录第 45 行；登记项 `src.verl.ray-trainer-source-v0.9.1`，尤其“GAE path-variance 代理”。
- **问题描述**：正文把 `old_log_probs` 无条件等同于实际采样策略 logprob，并把 `old_log_probs` / `ref_log_prob` 泛称为优势计算输入。固定源码实际上包含 bypass 与 decoupled 两种路径：后者允许训练侧重算 proximal anchor，并另外利用 rollout logprob 做校正。GAE 的直接输入是 rewards、values 和 mask；GRPO 还按组 ID 归一化。reference 通过启用的 reward KL 路径可以间接影响 advantage，但 GRPO 的 actor KL loss 不是这个直接输入关系。登记中的 path-variance 分支也不属于 GAE。
- **重新打开的证据**：[ray_trainer.py L218–245](https://github.com/verl-project/verl/blob/1876b06d0a3e4e71e06230be10af14492ca8a75b/verl/trainer/ppo/ray_trainer.py#L218-L245) 是 GAE/GRPO 调用；[L264–279](https://github.com/verl-project/verl/blob/1876b06d0a3e4e71e06230be10af14492ca8a75b/verl/trainer/ppo/ray_trainer.py#L264-L279) 的 path-variance 注释属于 optimal-token-baseline 分支；[L1570–1586](https://github.com/verl-project/verl/blob/1876b06d0a3e4e71e06230be10af14492ca8a75b/verl/trainer/ppo/ray_trainer.py#L1570-L1586) 明列两策略/三策略；[L1638–1674](https://github.com/verl-project/verl/blob/1876b06d0a3e4e71e06230be10af14492ca8a75b/verl/trainer/ppo/ray_trainer.py#L1638-L1674) 区分 reward KL、rollout correction 和 advantage。
- **建议关闭条件**：限定本页选用的模式，分别定义 `rollout_log_probs`、`old_log_probs`、当前 actor logprob 和 `ref_log_prob` 的生产者/版本/用途；给出 reward KL 与 actor KL loss 的分支关系。修正正文、来源记录和登记摘要的优势计算表述；若只讲 bypass 样板，明确排除 decoupled，不能把另一条合法路径判成一致性错误。

### B25-T04-C04 — P2：把推理侧 IPC 共置误当成训练/推理整组必须共置，且遗漏 delta 支持边界

- **受影响位置**：正文第 88、105、128、153 行，涉及权重转换与 TP/DP 的第 105 行。
- **问题描述**：“共置才有 IPC 增量更新”将最后一跳的同设备 IPC 与训练组/rollout 组的资源形态混为一谈。该版本另有分离式 delta checkpoint engine，跨组走 NCCL，到 rollout 侧再经本地 IPC 加载；delta 也不是简单地只传“变化张量”，而是变化位置和值。“LoRA 类训练天然适合”未由引用文件建立，FSDP 的对应 shard 导出还注明 Non-LoRA base path。正文只用一张参数映射表说明 TP/DP 独立，未解释分片导出/组装和重映射的同步代价。
- **重新打开的证据**：[delta_checkpoint_engine.py L14–36](https://github.com/verl-project/verl/blob/1876b06d0a3e4e71e06230be10af14492ca8a75b/verl/checkpoint_engine/delta_checkpoint_engine.py#L14-L36) 明写 disaggregated rollout、跨组传输及本地 IPC 两跳。[delta_weight_transfer.py L216–229](https://github.com/verl-project/verl/blob/1876b06d0a3e4e71e06230be10af14492ca8a75b/verl/workers/rollout/vllm_rollout/delta_weight_transfer.py#L216-L229) 限定 CUDA、BF16、DP=1、PP=1，并排除量化和 speculative decoding；[vllm_async_server.py L1141–1168](https://github.com/verl-project/verl/blob/1876b06d0a3e4e71e06230be10af14492ca8a75b/verl/workers/rollout/vllm_rollout/vllm_async_server.py#L1141-L1168) 另排除 PD 分离。[transformer_impl.py L918–948](https://github.com/verl-project/verl/blob/1876b06d0a3e4e71e06230be10af14492ca8a75b/verl/workers/engine/fsdp/transformer_impl.py#L918-L948) 给出 Non-LoRA shard 导出边界。[vllm_rollout.py L15–26](https://github.com/verl-project/verl/blob/1876b06d0a3e4e71e06230be10af14492ca8a75b/verl/workers/rollout/vllm_rollout/vllm_rollout.py#L15-L26) 也提示 FSDP 与 Megatron 权重布局转换不是同一条路径。
- **建议关闭条件**：画清 trainer → checkpoint worker → rollout engine 的传输/布局边界，区分跨组通信与本地 IPC，纠正“分离不可增量”。列出所选 delta 样板的必要限制；删除或补证 LoRA 适用性，不能外推支持。补一个注明示意性质的训练分片到 rollout TP/副本布局转换说明，记录 gather/转换/传输成本及不支持的映射；新增依赖须同步登记。

### B25-T04-C05 — P2：将 Ascend 更新日志与组件表的冲突拼成确定配套

- **受影响位置**：正文第 145 行；来源记录第 5、60 行；登记项 `src.verl.ascend-install-v0.9.1`。
- **问题描述**：正文将 torch_npu `2.10.0.post2` 与 CANN `9.1.0` 表述为安装指南“固定配套线”。同一个固定文件的组件表却写 `2.10.0.post4`。登记 notes 虽同时保留两个值，正文和来源记录未明确冲突，也未说明为何采信更新日志而不是组件表。这不是本库是否做过硬件验证的问题，而是来源自身尚未消解的版本差异。
- **重新打开的证据**：[install_guidance.rst L9–17](https://github.com/verl-project/verl/blob/1876b06d0a3e4e71e06230be10af14492ca8a75b/docs/ascend_tutorial/zh/get_start/install_guidance.rst#L9-L17) 的 2026-08-03 更新条目为 post2；同文件 [L84–101](https://github.com/verl-project/verl/blob/1876b06d0a3e4e71e06230be10af14492ca8a75b/docs/ascend_tutorial/zh/get_start/install_guidance.rst#L84-L101) 的环境表为 post4、HDK 26.0.rc1、CANN 9.1.0。
- **建议关闭条件**：正文、来源记录和登记均显式记录两处位置及冲突；在未进一步核对安装脚本/镜像前把实际应选 post 版本记为 unknown。若继续取证，说明选定路径及其固定版本，不能把不同路径拼成已确认组合；保留与既有 v0.14.0rc1 线分立的边界。

### B25-T04-C06 — P2：NVIDIA/AMD 平台支持条件尚未完成验收要求的独立核实

- **受影响位置**：正文第 144、147、159 行；来源记录第 47、62 行；相关 NVIDIA/AMD 来源登记。
- **问题描述**：NVIDIA 只写“默认文档路径”，没有给出所选 RL 组合的执行栈条件。AMD 只确认 quick start 存在并把整条支持线留作 unknown，诚实但不足以完成条款 5；被引用页面本身已经列出硬件、训练后端、推理后端、资源形态、镜像和驱动条件。应区分“上游文档声明支持”“所选组合尚待核实”与“本库未实测”，不能用第三者替代前两者的资料核对。
- **重新打开的证据**：[AMD quick start L15–42](https://github.com/verl-project/verl/blob/1876b06d0a3e4e71e06230be10af14492ca8a75b/docs/amd_tutorial/amd_quick_start.rst#L15-L42) 列出 Fully Async/Colocate、vLLM/SGLang、FSDP/FSDP2/Megatron、gfx942/gfx950 目标，以及 `amdagi/verl-dev:rocm7.14_torch2.12_release_0724` 和 ROCm 7.14 宿主要求；[L83–125](https://github.com/verl-project/verl/blob/1876b06d0a3e4e71e06230be10af14492ca8a75b/docs/amd_tutorial/amd_quick_start.rst#L83-L125) 有支持表和 RL 范例。[NVIDIA 路径安装页 L4–25](https://github.com/verl-project/verl/blob/1876b06d0a3e4e71e06230be10af14492ca8a75b/docs/start/install.rst#L4-L25) 声明 CUDA >=12.8、训练后端及 vLLM >=0.18.0；不能把本库 vLLM v0.14.0 的背景来源当成这套 RL 环境的兼容证明。
- **建议关闭条件**：分别选定并核对 NVIDIA、Ascend、AMD 的官方 RL/后端样板，至少记录硬件范围、软件/镜像线、训练与 rollout 后端、同步/异步模式、支持声明出处和剩余 unknown。上游表格不自动证明任意笛卡尔积可用；镜像中的具体引擎版本、驱动配套等未查到时继续细项标 unknown。不得把上述作者/项目声明改成已在本库验证，也不得从 vLLM 能启动推导 RL 支持。

### B25-T04-C07 — P2：步号不等于完整 policy 身份，样本关联契约仍缺可落地键

- **受影响位置**：正文第 81、89、117、138 行。
- **问题描述**：字段清单已有 tokenizer、输入输出、reward 和模型身份，但没有定义贯穿生成、打分、组归一化、消费与重试的 `sample_id` / `request_id` / `group_id` 关系；规则 reward 也不应只有“模型权重身份”，还需 verifier 代码/配置版本。`set_global_steps` 只是发布侧步号锚点，不能证明每条请求已绑定该权重版本，尤其不能直接与训练日志步号相减。
- **重新打开的证据**：[ray_trainer.py L1426–1451](https://github.com/verl-project/verl/blob/1876b06d0a3e4e71e06230be10af14492ca8a75b/verl/trainer/ppo/ray_trainer.py#L1426-L1451) 先按 step 0/恢复步发布，再递增训练循环步号；[L1481–1491](https://github.com/verl-project/verl/blob/1876b06d0a3e4e71e06230be10af14492ca8a75b/verl/trainer/ppo/ray_trainer.py#L1481-L1491) 才生成 uid 和当前 trace 步号。因此首次同步采样时，发布标签 0 与 trace 步号 1 可以同时出现，这不等于真实落后一版。GRPO 按 [L239–244](https://github.com/verl-project/verl/blob/1876b06d0a3e4e71e06230be10af14492ca8a75b/verl/trainer/ppo/ray_trainer.py#L239-L244) 的 uid 分组；[vllm_rollout.py L245–250](https://github.com/verl-project/verl/blob/1876b06d0a3e4e71e06230be10af14492ca8a75b/verl/workers/rollout/vllm_rollout/vllm_rollout.py#L245-L250) 的 `set_global_steps` 本身没有提供完整样本账本。
- **建议关闭条件**：给出最小样本记录示例或字段表，明确 prompt/group/response/attempt 的键及 reward/logprob 的关联；将行为策略的权重身份/发布版本、训练消费步号、运行/恢复代次分列，并规定“同步滞后为 0”的归一化定义。规则 verifier 记录代码与配置身份。标明哪些字段是上游实际产出，哪些是本库建议额外采集；不可暗示 `set_global_steps` 已自动完成这些工作。

### B25-T04-C08 — P2：固定 tag 内的 legacy 样板与 V1 默认入口未分开

- **受影响位置**：正文第 69、73、91、97–105、144、159 行；来源记录的版本/训练循环说明。
- **问题描述**：固定为 v0.9.1 仍不足以确定实现线。正文用 `ray_trainer.py` 和旧 fully-async/one-step recipe 解释整体默认流程，却没有声明这些是 legacy/V0 样板；同一 tag 默认入口已经选择 V1，异步模式的配置名与控制方式也不同。读者很容易将 `async_training.staleness_threshold` 当作 V1 的通用配置，或把旧 `fit()` 顺序当成默认入口的已核实行为。
- **重新打开的证据**：[ppo_trainer.yaml L228–238](https://github.com/verl-project/verl/blob/1876b06d0a3e4e71e06230be10af14492ca8a75b/verl/trainer/config/ppo_trainer.yaml#L228-L238) 默认为 `use_v1: true`，V1 模式列为 sync/colocate_async/separate_async；[main_ppo.py L183–192](https://github.com/verl-project/verl/blob/1876b06d0a3e4e71e06230be10af14492ca8a75b/verl/trainer/main_ppo.py#L183-L192) 将 V1 与 legacy 分流；[ray_trainer.py L285](https://github.com/verl-project/verl/blob/1876b06d0a3e4e71e06230be10af14492ca8a75b/verl/trainer/ppo/ray_trainer.py#L285) 标注 legacy deprecated。v0.9.1 release 还声明旧 experimental fully-async/one-step 将在下一版迁出；这不表示本 tag 已删除它们。
- **建议关闭条件**：明确选择“固定 tag 中的 legacy 机制样板”或补核 V1 实际控制流。若保留 legacy，在定义、模式表、验证方法和来源记录统一标识，说明不能直接拼接 V1 参数/默认值；若切换 V1，重新定位关键调用和适用条件，不能仅改标题。

### B25-T04-C09 — P2：单变量验证未固定可比工作量，且把性能收益写成排序结论

- **受影响位置**：正文第 59、71、99、101、115–120、134–138、151–152 行。
- **问题描述**：验证只说“其余不变”“固定步数”，但同步、一步异步和 streaming fully-async 的 batch/更新/发布单位并不相同；共置改分离也会改变资源分配。若直接照写法比较，样本量、总设备数、每样本更新次数和同步频率可能同时变化，无法归因于异步度。`train_batch_size` 决定 rollout batch、“每步同步”和 batch 增大带来的漂移也不是所有模式共有。表中的“吞吐最高”及“异步提高的是资源利用率”超出限定环境数字所能支持的范围。
- **重新打开的证据**：[fully_async.md L94–107](https://github.com/verl-project/verl/blob/1876b06d0a3e4e71e06230be10af14492ca8a75b/docs/advance/fully_async.md#L94-L107) 明确 streaming 下 `data.train_batch_size` 不生效，改由其他参数控制；[L118–125](https://github.com/verl-project/verl/blob/1876b06d0a3e4e71e06230be10af14492ca8a75b/docs/advance/fully_async.md#L118-L125) 给出与共置比较时的工作量对齐关系；[L79–83](https://github.com/verl-project/verl/blob/1876b06d0a3e4e71e06230be10af14492ca8a75b/docs/advance/fully_async.md#L79-L83) 解释分离后各阶段可能更慢、靠重叠降低端到端时间。2.35–2.67× 的 [L7–10](https://github.com/verl-project/verl/blob/1876b06d0a3e4e71e06230be10af14492ca8a75b/docs/advance/fully_async.md#L7-L10) 仅为 Qwen2.5-7B、128 GPU 下的作者报告。
- **建议关闭条件**：按所选实现线给出对照表，固定总资源、prompt/组数、有效训练 token、每样本更新次数、采样/校正方式及质量评估预算；明确阶段吞吐与端到端吞吐的计时边界，以及发布次数与样本量怎样对齐。将“最高/提高”改成有条件的可能收益，并列出应实测的同步成本和质量代价。把通用描述限定为同步样板；保留作者数字的原环境、比较基线和未复现标注，不给出未经验证的阈值或结果。

### B25-T04-C10 — P2：论文摘要不能支持被归入其下的全部机制细节

- **受影响位置**：正文第 61、63 行及第 44、159 行的取证范围；来源记录第 49–52 行；四篇论文登记 notes。
- **问题描述**：PPO 的 clipped objective/免二阶导、GRPO 的组均值 baseline/移除 critic 被写成“论文摘要”已建立的机制事实。重新打开的 PPO 摘要只描述 surrogate objective 与多 epoch minibatch；DeepSeekMath 摘要只说提出 GRPO 及改善 PPO 内存使用，没有展开 baseline/critic。HybridFlow 摘要说明混合编程模型，并非对单控制器实现细节的完整取证。相关结论可由本批已有的固定 verl 文档支持，但不能把摘要级核对夸大为原论文机制复核。DPO 摘要对无需显式 reward 建模和训练中采样的结构性描述则有支持。
- **重新打开的证据**：[PPO 摘要](https://arxiv.org/abs/1707.06347)、[DeepSeekMath 摘要](https://arxiv.org/abs/2402.03300)、[HybridFlow 摘要](https://arxiv.org/abs/2409.19256)、[DPO 摘要](https://arxiv.org/abs/2305.18290)。与之相比，[ppo.md L14–22](https://github.com/verl-project/verl/blob/1876b06d0a3e4e71e06230be10af14492ca8a75b/docs/algo/ppo.md#L14-L22)、[grpo.md L7–19](https://github.com/verl-project/verl/blob/1876b06d0a3e4e71e06230be10af14492ca8a75b/docs/algo/grpo.md#L7-L19) 和 [hybrid_flow.rst L45–68](https://github.com/verl-project/verl/blob/1876b06d0a3e4e71e06230be10af14492ca8a75b/docs/hybrid_flow.rst#L45-L68) 才分别展开相应机制。
- **建议关闭条件**：把机制主张附近的证据改为已核实的具体实现文档；论文摘要只承载其确实写出的内容。若要断言原论文公式/设计细节，另取固定论文版本对应章节/公式并更新登记。同步收窄来源记录和 notes 的“摘要取证”范围，不必为关闭此项强制扩展到全文评述。

### B25-T04-C11 — P3：验收要求的闭环图仍缺失，且存在不存在的章节承诺

- **受影响位置**：正文第 61、67–77、155 行。
- **问题描述**：五环节以编号说明，但未实际画出采样、reward、advantage、更新和新 policy 发布后的回边；第 61 行承诺在“数据从哪来”一节对照 DPO，全文没有该节。DPO 扩展直到常见误解才简略出现，未在主循环旁展示“静态偏好对”与“在线生成并配对”的边界。
- **重新打开的证据**：[hybrid_flow.rst L27–48](https://github.com/verl-project/verl/blob/1876b06d0a3e4e71e06230be10af14492ca8a75b/docs/hybrid_flow.rst#L27-L48) 采用 RL 数据流解释；[dpo_extension.rst L28–41](https://github.com/verl-project/verl/blob/1876b06d0a3e4e71e06230be10af14492ca8a75b/docs/advance/dpo_extension.rst#L28-L41) 明确 online DPO 的生成、verifier 配对、DPO 更新与 reference 角色。验收条款 1 另明确要求“画出”循环。
- **建议关闭条件**：增加简洁 ASCII 或 Mermaid 闭环图，标出策略版本、reward/advantage/更新/发布和回边，PPO critic 与 reference 依赖分清；用旁注或小表区分普通 SFT、离线 DPO、online DPO 范例。补上所承诺的章节或删除该指代，不需要复制外部图。

## 已核对且未另立发现的事项

- **元数据与导航**：稳定 ID、`concept / training / draft`、`platforms: [generic]`、`updated_at: "2026-10-20"` 与 schema 一致。19 个 `source_refs` 均有登记，6 个 `related_ids` 均存在；`generic` 没被当成平台兼容证明。06 章索引的正文入口与 06.4 地图均指向目标文件，预训练/微调正文也已有反向 Markdown 入口；没有发现本任务相关死链或重复主归属。
- **来源完整性**：本次没有发现记录值与取回物的 SHA-256 不一致。来源内容/版本语义的问题是 C03、C05、C06、C08、C10，不能因为 hash 一致就视为这些问题已关闭。本任务的 12 条 verl 来源均核对；`src.verl.*` 中另三条 profiling 来源属于 T06-06，仅核对其任务归属，不将其算作 T06-04 完整技术审阅。
- **许可标注**：固定 verl 根 LICENSE 的 Apache-2.0、MindSpeed-LLM 根 LICENSE 的默认 BSD 三条款及第三方例外说明，与本任务登记范围未见直接冲突；论文保留许可 unknown、仅链接和原创归纳。该观察不扩展成对全部第三方附件或外链图片的许可审计。
- **受支持的局部主张**：GRPO 无独立 critic、组采样与默认 token-mean 聚合相对论文口径的差异，均有固定文档支持；全量更新后的缓存清理、条件式 sleep/wake-up、legacy `fit()` 恢复后先同步权重，也能在相应源码中找到。MindSpeed-LLM 的 Megatron 日志/计时复用和 rollout 字段/优势计算由两份源码支持；其采样后端仍为 unknown，没有据此声明与 verl 相同。
- **证据纪律已有基础**：2.35–2.67× 与 rollout 约 70% 均标为来源作者报告，未发现虚构执行命令或本地结果。需修正的是这些局部限定与 C09 中无条件比较措辞之间的不一致，而非要求提供不存在的硬件实测。

## 结构校验与变更边界

- 已执行 `make check`：通过，107 content entries / 522 sources。此结果仅证明结构、ID、登记引用与本地文件链接，不证明本报告涉及的技术正确性或平台兼容性。
- `make build` 在临时仓库快照通过：107 content entries / 522 sources，成功生成两份 catalog，用户仓库已有 `build/` 未修改。首次快照排除 `build/` 时，因现有文档链接到两份 catalog 而检查失败；补齐快照中的既有构建文件后重新执行通过，这是快照准备问题，不是正文缺陷。
- 本轮不修改 `src/kb/`，不新增测试、不运行硬件实验。用户工作区原有的 Batch 25 未提交修改保留。

## 总体判断

**当前初审不通过；经修订后可以达到 T06-04 的验收范围。** 共 11 项发现：2 项 P1、8 项 P2、1 项 P3。没有要求把概念草稿变成硬件验证报告，但也不能用 `source_checked`、结构检查通过或宽泛 unknown 代替必要的来源边界核对。

| 验收条款 | 本轮判断 | 尚需关闭的缺口 |
|---|---|---|
| 1. 在线 RL / 离线偏好 / SFT 与五阶段循环 | 基本概念已有，展示未完整 | C03、C10、C11：优势依赖、引用范围、闭环图及 DPO 指代 |
| 2. 同步/受控异步与数据关联 | 部分满足 | C01、C03、C07、C08：阈值单位、logprob 角色、版本/样本键、实现线 |
| 3. 权重同步、陈旧策略、随机性、并行与资源代价 | 部分满足 | C01、C04、C07、C08：两跳传输、delta 限制、布局转换、计数与实现边界 |
| 4. 吞吐/质量/有效样本及停止、重放、重复计算 | 指标类别已有，失败一致性明显缺项 | C02、C07、C09，尤其两个 P1 中的安全保证与失败恢复 |
| 5. 单变量验证、公开样板与三平台支持条件 | 有方法框架，条件未闭合 | C05、C06、C08、C09：Ascend 冲突、三平台资料、所选实现线与可比预算 |

作者修订时须同时处理正文、来源记录和相关登记摘要之间的语义一致性；修订后按上述 ID 做定向复核，P1 未关闭前不得宣布本任务审阅通过。真实环境验证与编辑审阅继续分开，正文保持 draft。
