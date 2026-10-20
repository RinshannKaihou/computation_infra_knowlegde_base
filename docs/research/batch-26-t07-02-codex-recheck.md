# Batch 26 T07-02 修订后定向复核

## 复核头部

- 角色：知识库批次审阅者；逐项核对[初审 C01–C07](batch-26-t07-02-codex-review.md)的关闭条件，并检查修订引入的问题。不代作者修改正文、来源登记或计划。
- 模型／推理档位：`gpt-6.1-sol / xhigh`。已读取本轮本地会话 `01a15816-69a1-7f81-87b4-d63f87c07c24` 的执行元数据：`originator: codex_exec`、`source: exec`、CLI `0.163.0`；本轮 `turn_context` 为上述单一模型与档位，未见模型回退标记，未调用其他模型或子代理。
- 日期：2026-10-20（Asia/Shanghai）。
- 本地范围：[正文](../../knowledge/07-inference/engine-backend-boundaries.md)全文、[作者来源记录](batch-26-t07-02-sources.md)、[registry](../../sources/registry.yaml)中本轮相关条目，以及[章节索引](../../knowledge/07-inference/index.md)的 T07-02 描述；按 T07-02 原 acceptance 和原关闭条件复核。本报告中的本地行号为本轮读取时位置。
- 上游重开：通过 GitHub 文件／Contents API 重新取回以下固定 ref 的原文件，使用保留空行的原文件坐标；未以作者缓存或初审结论代替本轮源码核对。
  - vLLM `b17039bccc17b94a2ea107272ad7bc93508708df`：`engine/arg_utils.py`、`config/scheduler.py`、`v1/core/sched/scheduler.py`／`request_queue.py` 的 FCFS／Priority 相关实现、`v1/core/kv_cache_manager.py`，以及 GPU 安装页对应的 `docs/getting_started/installation/gpu.md`／`gpu.cuda.inc.md`。
  - vllm-ascend `52d4acfa51fb868823d1070b81cbd2d97e9e4696`：根 `README.md`、`vllm_ascend/platform.py` 编译分派、`compilation/compiler_interface.py`，以及 `vllm_ascend/` 目录成员。
  - MindIE-LLM `69e5a5dd4b533eaffc7e198320435350825a36f7`：`src/scheduler/policy/policy_factory.cpp`、`policy.h`、`fcfs_policy.cpp`、`policy_helper.cpp`、`src/include/config/config_info.h`、`src/block_manager/self_attn_block_manager.h`；为核对新增预算解释，补开 `src/scheduler/scheduler.cpp`、`src/include/dataclass/scheduling_budget.h`、`src/sequence/scheduling_budget.cpp`；另核对 `scheduler/`、`policy/` 目录成员。
- 文档重开：[vLLM v0.14.0 GPU 安装页](https://docs.vllm.ai/en/v0.14.0/getting_started/installation/gpu/)与[MindIE 模型支持列表](https://mindie-llm-doc.readthedocs.io/zh-cn/latest/user_guide/model_support_list/)。后者仍是 2026-10-20 取回的 `latest` 声明，不因此与固定源码或产品包建立同版关系。部分 raw URL 的网页读取返回错误，已改用 GitHub 文件 API 取得所需源码；本轮未重新验证全部历史功能声明或复算作者清单全部 SHA-256。
- 执行边界：仅新增本报告；未安装、构建或运行推理引擎，未执行模型请求、硬件测试或运行环境变更。
- 结构校验：在包含本报告的临时工作区副本中执行 `make check`、`make build`，均通过（109 content entries／537 sources）。首次副本未带入既有 `build/`，两命令因 `docs/first-fill-status.md` 的两个目录链接缺失而失败；补入原工作区既有生成目录后重新执行通过。仅证明结构和本地文件链接符合检查要求，不证明技术正确性或远程链接；原工作区构建产物未改动。

## C01–C07 逐项结论

“未关闭”保留原发现 ID 与优先级；修订引入的独立问题另列 R01–R03，不以新增编号替代原关闭条件。

| 原发现 | 结论 | 本轮核对及剩余关闭条件 |
|---|---|---|
| **C01（P2）** 平台有限条件档案 | **未关闭** | 正文 L80–87 已补 NVIDIA 计算能力、机型例、OS／Python、Llama 实现样板及 EP／block 默认未知；L93–97 已补 AMD 制品、模型与并行行；L105 的 Ascend Prerequisites 与[固定 README L49–57](https://github.com/vllm-project/vllm-ascend/blob/52d4acfa51fb868823d1070b81cbd2d97e9e4696/README.md#L49-L57)一致。但 Ascend 表 L103–112 **仍没有选定任何有限模型／模型族**，MindIE 各行仍只说“按模型给出矩阵”，vllm-ascend 的 EP 仍停留在教程／子模块存在性。AMD 没有明确 KV 状态行，PD 只提可选组件，未登记所选样板的功能状态和限制；“模型集同上游”也没有选定 AMD 模型样板。三平台仍未逐档案登记驱动／HDK、具体制品与模型身份的已知值或 `unknown`；关键量化／并行／PD 条件多仍指向“登记 notes”，没有就近精确 URL。补字段是进展，尚未满足原有限样板及依赖身份条件。应选少量明确样板、补齐上述维度和证据；缺证据可明确写 `unknown`，不要求虚构部署组合。CUDA 制品新增问题另见 R03。 |
| **C02（P2）** eager 范围扩大 | **未关闭** | 正文 L56、L108、L119 及作者来源表 L38 已将结论收窄为 `simple_compile_backend` 字段，并保留完整默认路径未知；与[platform.py L95–136](https://github.com/vllm-project/vllm-ascend/blob/52d4acfa51fb868823d1070b81cbd2d97e9e4696/vllm_ascend/platform.py#L95-L136)、[L234–307](https://github.com/vllm-project/vllm-ascend/blob/52d4acfa51fb868823d1070b81cbd2d97e9e4696/vllm_ascend/platform.py#L234-L307)及[AscendCompiler L109–139](https://github.com/vllm-project/vllm-ascend/blob/52d4acfa51fb868823d1070b81cbd2d97e9e4696/vllm_ascend/compilation/compiler_interface.py#L109-L139)的分派边界一致。**registry L555 本轮扩展仍原样保留 `simple_compile_backend 默认 "eager"（torch.compile 默认关闭）`**，用户所述“registry 同步”未落实。只需同步该条登记摘要，撤回全局默认关闭推断，保留字段范围及完整默认路径未知；无需反向声称默认一定开启编译。 |
| **C03（P2）** chunked prefill 默认／pooling 门控 | **未关闭** | 正文 L53／L63、registry L6691、作者来源表 L34 已正确区分模型能力推导默认与测试用 dataclass 默认，来源表也将 pooling 注释限定在原上下文；[EngineArgs L1900–1934](https://github.com/vllm-project/vllm/blob/b17039bccc17b94a2ea107272ad7bc93508708df/vllm/engine/arg_utils.py#L1900-L1934)及[调度门控 L572–582](https://github.com/vllm-project/vllm/blob/b17039bccc17b94a2ea107272ad7bc93508708df/vllm/v1/core/sched/scheduler.py#L572-L582)支持这些修订。但正文新增“用户显式设置时以用户值为准”仍把中间参数当最终配置，未覆盖同一配置类的 encoder-decoder 强制关闭分支（R02）。应限定为该默认值推导函数内保留显式值，最终仍受后续模型／平台校验与覆盖约束；原 pooling 误推广已修正，但完整关闭须同时消除这一新绝对化表述。 |
| **C04（P2）** 参数／调度／KV 有限语义比较 | **未关闭** | 正文 L65–70 已有 token／sequence 预算、阶段分派、前缀命中和块职责的有限对照；[vLLM Scheduler L252–289](https://github.com/vllm-project/vllm/blob/b17039bccc17b94a2ea107272ad7bc93508708df/vllm/v1/core/sched/scheduler.py#L252-L289)、[MindIE FcfsPolicy L37–111](https://github.com/Ascend/MindIE-LLM/blob/69e5a5dd4b533eaffc7e198320435350825a36f7/src/scheduler/policy/fcfs_policy.cpp#L37-L111)与[SelfAttnBlockManager L27–65](https://github.com/Ascend/MindIE-LLM/blob/69e5a5dd4b533eaffc7e198320435350825a36f7/src/block_manager/self_attn_block_manager.h#L27-L65)支持其中有限职责／顺序说明。但新增“`maxPrefillTokens` 只限 prefill”被实际 MIX 预算路径反驳（R01）；L68 仍在两侧触发条件未核的情况下直接说抢占／重新排队边界不同，未解释原关闭条件要求的任何受限“抢占→块释放／状态重置→再入队”场景。预算和 KV 段也未就近链接其具体源码。应修正 R01，并补一个有边界的抢占／释放／重新排队比较及精确链接，同步来源表已核／未核范围；不要求逐行审完整算法或进行硬件实测。 |
| **C05（P2）** latest 与固定源码身份混合 | **CLOSED** | 正文 L74 已撤回“每行固定 ref”，明确 `latest` 为 **2026-10-20 取回声明、未与 69e5a5dd 或产品包核同版**；Ascend 表 L103 的 MindIE 列不再将 commit 放在列名上，L105–109 的硬件／制品／量化／图／卡数行均标注 latest 身份，L111 的块接口事实另标固定源码，L112 继续保留版本 gate。重开[模型支持表](https://mindie-llm-doc.readthedocs.io/zh-cn/latest/user_guide/model_support_list/)未取得同版映射；当前修订没有借本次访问关闭 gate，满足原身份分层条件。C01 的模型样板覆盖不足另行保留。 |
| **C06（P2）** PRIORITY 枚举与可构造策略混淆 | **CLOSED** | 正文 L53、registry L6719、作者来源表 L41 均已分开枚举与工厂路径，并明确 PRIORITY 枚举不证明可用。重开[policy.h L22](https://github.com/Ascend/MindIE-LLM/blob/69e5a5dd4b533eaffc7e198320435350825a36f7/src/scheduler/policy/policy.h#L22)与[PolicyFactory L26–54](https://github.com/Ascend/MindIE-LLM/blob/69e5a5dd4b533eaffc7e198320435350825a36f7/src/scheduler/policy/policy_factory.cpp#L26-L54)：PnD／Flex 按 layerwise 配置构造 FCFS 系，P／D 构造 PDDS，其他角色抛错；工厂注释的当前 FCFS 限定已准确保留。结论仅限所核工厂路径，未写成全仓不存在性证明。 |
| **C07（P3）** README 与 latency_predictor 路径 | **CLOSED** | 作者来源表 L18 已显式将错误路径订正为仓库根 `README.md`，并说明 `vllm_ascend/` 中无该文件；L41、registry L6719 与正文 L53 已将 `latency_predictor` 放在 `scheduler/` 下，与 `policy/` 同级。独立重开[根 README](https://github.com/vllm-project/vllm-ascend/blob/52d4acfa51fb868823d1070b81cbd2d97e9e4696/README.md)、[插件目录](https://github.com/vllm-project/vllm-ascend/tree/52d4acfa51fb868823d1070b81cbd2d97e9e4696/vllm_ascend)、[scheduler 目录](https://github.com/Ascend/MindIE-LLM/tree/69e5a5dd4b533eaffc7e198320435350825a36f7/src/scheduler)与[policy 目录](https://github.com/Ascend/MindIE-LLM/tree/69e5a5dd4b533eaffc7e198320435350825a36f7/src/scheduler/policy)，层级与修订一致；保留旧路径加箭头的形式已明确表示勘误，不再把旧路径列为真实文件。 |

## 新发现

### T07-02-R01 — P2：新增预算对照把 maxPrefillTokens 错限为 prefill 专用

- 位置：正文 L67；registry L6719、作者来源表 L41 的“按阶段分立”摘要须一并限定。
- 问题：正文以“vLLM 的迭代 token 预算含 decode，MindIE 的 `maxPrefillTokens` 只限 prefill”为不可等价的具体理由。配置头文件的字段名无法证明此运行边界；固定实现中存在相反的 MIX 路径。该解释会误导混合调度下 token 预算和吞吐对照。
- 固定源码证据：
  1. [Scheduler L297–308](https://github.com/Ascend/MindIE-LLM/blob/69e5a5dd4b533eaffc7e198320435350825a36f7/src/scheduler/scheduler.cpp#L297-L308)按优先阶段选择 batch 上限，但初始 token 预算取 `max(maxSeqLen, maxPrefillTokens)`，没有把 token 预算参数限定为 prefill 分支。
  2. [SchedulingBudget 构造函数 L17–34](https://github.com/Ascend/MindIE-LLM/blob/69e5a5dd4b533eaffc7e198320435350825a36f7/src/sequence/scheduling_budget.cpp#L17-L34)在 `enableChunkedPrefill` 为真时，将共享 `maxNumBatchedTokens_` 设为 `maxPrefillTokens`、sequence 上限设为 `maxBatchSize`；`CanSchedule` 检查该共享预算。
  3. [FcfsPolicy MIX L92–111](https://github.com/Ascend/MindIE-LLM/blob/69e5a5dd4b533eaffc7e198320435350825a36f7/src/scheduler/policy/fcfs_policy.cpp#L92-L111)先运行 running／有条件的 swapped，再处理 waiting，传递同一个 budget。[running 输出 L325–337](https://github.com/Ascend/MindIE-LLM/blob/69e5a5dd4b533eaffc7e198320435350825a36f7/src/scheduler/policy/fcfs_policy.cpp#L325-L337)将 decode 工作同样累计进 budget；[PolicyHelper L48–55](https://github.com/Ascend/MindIE-LLM/blob/69e5a5dd4b533eaffc7e198320435350825a36f7/src/scheduler/policy/policy_helper.cpp#L48-L55)对非 prefill sequence 计一个新 token。
- 审阅推论：在上述 chunked／MIX 条件下，decode 先消耗由 `maxPrefillTokens` 限定的共享 token 预算，waiting prefill 使用其剩余部分。因此两侧虽不能据此建立一一映射，也不能用“MindIE 不计 decode”来证明差异。
- 关闭条件：撤回“只限 prefill”，分别说明已核的非 chunked 初始预算及 chunked／MIX 覆盖和共享消耗关系；用真实的阶段选择、预算初始化／覆盖、缓存计数或准入规则说明不可直接等价，并同步正文、来源表和登记摘要。只按本次源码路径作有限判断，不扩大为所有策略／PD 角色的统一规则。

### T07-02-R02 — P2：新增“显式设置以用户值为准”漏掉后续模型强制覆盖

- 位置：正文 L63。
- 问题：该句将 EngineArgs 默认推导函数保留显式值，写成了整体启用规则。用户显式值不是最终调度配置的无条件优先值。
- 证据：[EngineArgs L1631–1647](https://github.com/vllm-project/vllm/blob/b17039bccc17b94a2ea107272ad7bc93508708df/vllm/engine/arg_utils.py#L1631-L1647)将 `enable_chunked_prefill` 与 `model_config.is_encoder_decoder` 一起传入 `SchedulerConfig`；[SchedulerConfig.__post_init__ L214–223](https://github.com/vllm-project/vllm/blob/b17039bccc17b94a2ea107272ad7bc93508708df/vllm/config/scheduler.py#L214-L223)在 encoder-decoder 条件成立时直接将 `self.enable_chunked_prefill = False`。这条覆盖不以用户参数是否显式提供为条件。
- 关闭条件：把“以用户值为准”限定为 `_set_default_chunked_prefill_and_prefix_caching_args` 内的处理，并说明后续模型／平台校验或覆盖仍可改变配置；至少列明上述 encoder-decoder 反例。保持“最终配置与模型条件决定”的总述、自动默认与 pooling 注释的正确区分，不再把显式输入当作已启用证明。

### T07-02-R03 — P2：新增 CUDA 12.8 制品身份未保留同页默认构建声明的冲突

- 位置：正文 L81。
- 问题：新增“pip wheel 含预编译 C++ 与 CUDA 12.8 二进制（同页声明）”只采用了安装页概述，作为该档案的制品／运行库字段，却未注明同页默认 wheel 构建说明与之不一致，也没有锁定一个 CUDA 12.8 wheel 变体。
- 证据：本轮重开的[v0.14.0 安装页概述](https://docs.vllm.ai/en/v0.14.0/getting_started/installation/gpu/)确有 CUDA 12.8；同页[Pre-built wheels](https://docs.vllm.ai/en/v0.14.0/getting_started/installation/gpu/#pre-built-wheels)又声明默认 CUDA 12.9，并另提供 12.8／13.0 变体。固定到 `b17039bc` 的[同一原文件 L1–38](https://github.com/vllm-project/vllm/blob/b17039bccc17b94a2ea107272ad7bc93508708df/docs/getting_started/installation/gpu.cuda.inc.md#L1-L38)同时保留这两种说法，故不能只归因于本轮网页与固定 ref 不同。
- 审阅判断：这不是认定 CUDA 12.8 wheel 不存在，而是现有证据不能把未选定的 pip wheel 记成单一 CUDA 12.8 制品身份；默认构建声明与概述差异尚未解释。
- 关闭条件：标注概述 12.8／默认构建段 12.9 的声明差异，将已选变体与具体制品身份分别登记；未核实际 wheel 时保留 `unknown`。如选 CUDA 12.8 文档变体作为有限样板，应明确它的变体身份和证据范围，不能用版本化安装页概述代替具体 wheel／驱动配套验证。

## 整体结论

**未通过本轮定向复核。** C05、C06、C07 为 **CLOSED**；C01、C02、C03、C04 **未关闭**（原 P2 级别保留）。修订另引入 **3 项新 P2：R01–R03**，分别涉及 MindIE 混合调度预算、vLLM 显式参数的后续覆盖和 CUDA 制品声明冲突；它们与原关闭条件有交集，不作为互不相关的七个根因相加。

下一轮应完成四项剩余关闭条件并修正 R01–R03，再对改动位置和相关来源记录定向复核。已关闭三项无需无关扩审。结构检查通过也不改变本结论；正文继续保持 `draft / source_checked` 的来源核对边界，MindIE `latest` 同版关系及各真实部署组合仍未证实，本轮没有硬件验证。
