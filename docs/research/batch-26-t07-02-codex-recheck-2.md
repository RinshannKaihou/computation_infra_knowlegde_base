# Batch 26 T07-02 第二轮定向复核

## 复核头部

- 角色：知识库批次审阅者；仅核对[第一轮复核](batch-26-t07-02-codex-recheck.md)留下的 C01–C04、R01–R03 的第二轮修订与相关关闭条件，并检查这些修订引入的问题。C05／C06／C07 沿用 CLOSED，不重新审阅。
- 模型／推理档位：`gpt-6.1-sol / xhigh`。已读取本轮本地 Codex CLI 会话 `01a15824-ddec-7220-bd36-1e6809468f8e` 的执行元数据：`originator: codex_exec`、`source: exec`、CLI `0.163.0`；本轮 `turn_context` 为上述单一模型与档位，未发生模型回退，未调用其他模型或子代理。
- 日期：2026-10-20（Asia/Shanghai）。
- 本地对象：[正文](../../knowledge/07-inference/engine-backend-boundaries.md)的修订及必要邻接语境、[作者来源记录](batch-26-t07-02-sources.md)、[registry](../../sources/registry.yaml)相关 notes；对照[初审关闭条件](batch-26-t07-02-codex-review.md)与第一轮剩余条件。另只读核对章节索引的原相关描述。本报告本地行号按本轮读取时位置。
- 上游取证：部分 GitHub blob URL 经网页读取返回 Cache miss，改用 GitHub 文件 API 重新取得固定 ref 原文件，保留空行核对原文件坐标，未以作者缓存代替独立取回。
  - MindIE-LLM `69e5a5dd4b533eaffc7e198320435350825a36f7`：`src/scheduler/scheduler.cpp`、`src/sequence/scheduling_budget.cpp`、`src/scheduler/policy/fcfs_policy.cpp`／`policy_helper.cpp`、`src/block_manager/self_attn_block_manager.h`。重新计算前三份新增哈希对应文件：`scheduler.cpp` 为 `2a46338316abe4ad`、`scheduling_budget.cpp` 为 `e512c6f55db58e02`、`policy_helper.cpp` 为 `6acd5989b39fe8d1`（SHA-256 前 16 位），均与作者来源表 L29–31 一致；registry 通过“文件 SHA-256 见来源记录”引用该表，没有另列摘要。
  - vLLM `b17039bccc17b94a2ea107272ad7bc93508708df`：`vllm/config/scheduler.py`、`vllm/engine/arg_utils.py`、`vllm/v1/core/sched/scheduler.py`、`docs/getting_started/installation/gpu.cuda.inc.md`。
  - vllm-ascend `52d4acfa51fb868823d1070b81cbd2d97e9e4696`：`vllm_ascend/platform.py`、根 `README.md`、`supported_features.md`、`disaggregated_prefill.md`。
- 文档重开：[vLLM v0.14.0 GPU 安装页](https://docs.vllm.ai/en/v0.14.0/getting_started/installation/gpu/)、MindIE [快速入门](https://mindie-llm-doc.readthedocs.io/zh-cn/latest/user_guide/quick_start/quick_start/)与[模型支持列表](https://mindie-llm-doc.readthedocs.io/zh-cn/latest/user_guide/model_support_list/)。MindIE 两页仍仅作 2026-10-20 取回的 `latest` 声明，不建立与固定源码／产品包的同版关系。
- 执行边界：只新增本报告；未修改正文、来源、索引、计划或原工作区构建产物，未安装、构建或运行推理引擎，未做硬件验证。
- 结构校验：在包含本报告及既有 `build/` 链接目标的临时工作区副本执行 `make check`、`make build`，均通过（109 content entries／537 sources）。检查仅验证结构与本地引用，不证明技术正确性或远程内容；原工作区 `build/` 未改动。

## C01–C04＋R01–R03 逐项结论

| 发现 | 结论 | 本轮核对与剩余关闭条件 |
|---|---|---|
| **C01（P2）** 有限平台条件档案 | **未关闭** | AMD L95 已选上游 Llama 实现为样板，L100–101 补 PD／KV 未证实行；Ascend L107 的 MindIE Qwen2-7B 装载样板也有[快速入门“环境准备／获取模型权重”](https://mindie-llm-doc.readthedocs.io/zh-cn/latest/user_guide/quick_start/quick_start/)支持。但同一行的 vllm-ascend 只引用 [README L47](https://github.com/vllm-project/vllm-ascend/blob/52d4acfa51fb868823d1070b81cbd2d97e9e4696/README.md#L47)的模型类别概述，并直写“有限样板未选定，未证实”；Transformer-like／MoE／Embedding／多模态类别不是选定的具体模型或模型族。MindIE 各特性也仍是“逐模型矩阵”的总述，没有落实到所选 Qwen2-7B 读表样板的条件或 unknown。三平台仍未逐档案登记驱动／HDK、模型权重／tokenizer 身份及未选制品的已知值或 unknown（NVIDIA wheel unknown 已补）；升级清单不能代替当前档案。就近链接只部分完成：Ascend 量化／PD、EP 新闻行已有固定 URL，但 L111 的 FAQ 14 仍只有“登记”，NVIDIA L83／L86 的量化／PD 也仍依赖 notes。**剩余条件**：实际选定有限模型／硬件样板，逐项填写该样板的特性状态与依赖身份，缺证据可明确 unknown；补齐关键条件的精确 URL。无需补造兼容组合或实测结果。 |
| **C02（P2）** eager 范围 | **CLOSED** | registry L555 已删除“torch.compile 默认关闭”的整体推断，限定为 `simple_compile_backend` 字段的 simple backend 范围，并保留完整默认执行路径未核。与正文 L56／L111／L122、来源表 L41 一致。重开 [platform.py L95–136](https://github.com/vllm-project/vllm-ascend/blob/52d4acfa51fb868823d1070b81cbd2d97e9e4696/vllm_ascend/platform.py#L95-L136)及 [L234–307](https://github.com/vllm-project/vllm-ascend/blob/52d4acfa51fb868823d1070b81cbd2d97e9e4696/vllm_ascend/platform.py#L234-L307)，字段值、独立 compiler 入口、编译模式／Inductor／ACL graph 分派均支持此范围限定。第一轮仅剩的登记摘要问题已修；不据此推断完整默认路径一定开启或关闭编译。 |
| **C03（P2）** chunked prefill 规则 | **CLOSED** | 正文 L63 已将“保留显式值”限定在 `_set_default_chunked_prefill_and_prefix_caching_args` 内，并说明后续模型校验可覆盖，列明 encoder-decoder 反例。重开 [arg_utils.py L1900–1934](https://github.com/vllm-project/vllm/blob/b17039bccc17b94a2ea107272ad7bc93508708df/vllm/engine/arg_utils.py#L1900-L1934)、[配置传入 L1631–1647](https://github.com/vllm-project/vllm/blob/b17039bccc17b94a2ea107272ad7bc93508708df/vllm/engine/arg_utils.py#L1631-L1647)与 [SchedulerConfig L214–223](https://github.com/vllm-project/vllm/blob/b17039bccc17b94a2ea107272ad7bc93508708df/vllm/config/scheduler.py#L214-L223)，显式值保留与后续强制置 False 的区分成立。原有自动默认、测试用 dataclass 默认及 pooling 注释边界保持正确；registry L6691、来源表 L37 没有残留“显式输入无条件优先”的表述。 |
| **C04（P2）** 有限调度／KV 语义比较 | **未关闭** | 预算修订及 MindIE 预算／块接口的就近链接有进展，原“抢占边界不同”的无依据断言已撤回。但 L68 标为“抢占→块处理→再入队的受限对照”的内容，仍只有 MindIE 枚举／接口与 vLLM 路径未核的声明，没有说明任何一个受限场景的触发、释放／状态重置与重新排队关系，未满足上轮明确留下的条件。作为补核定位，[vLLM Scheduler L351–401](https://github.com/vllm-project/vllm/blob/b17039bccc17b94a2ea107272ad7bc93508708df/vllm/v1/core/sched/scheduler.py#L351-L401)可见分配失败后的抢占选择，[L800–819](https://github.com/vllm-project/vllm/blob/b17039bccc17b94a2ea107272ad7bc93508708df/vllm/v1/core/sched/scheduler.py#L800-L819)明确释放 KV／encoder cache、重置计算进度并放回 waiting；[MindIE FcfsPolicy L468–510](https://github.com/Ascend/MindIE-LLM/blob/69e5a5dd4b533eaffc7e198320435350825a36f7/src/scheduler/policy/fcfs_policy.cpp#L468-L510)可见模式选择及 RECOMPUTE 下 WAITING／FreeSeq／状态重置，但完整再入队链须继续定位，不能由枚举补写。L69 的 vLLM 命中／释放说明仍未就近链接对应 KV 实现。**剩余条件**：写出有源码支持的有限场景与比较条件，明确已核和未知步骤，补齐对应链接并同步来源范围；另修 R04 的配额机制依据。未知声明可保留，但不能替代原验收要求的有限比较。 |
| **R01（P2）** maxPrefillTokens 被错限为 prefill | **CLOSED** | 正文 L67、来源表 L44、registry L6719 均已撤回该错误，区分非 chunked 的初始 `max(maxSeqLen, maxPrefillTokens)` 与 chunked 下共享预算覆盖；MIX 同预算、decode 同样计入的事实已在后两处明确登记，正文也不再用“不计 decode”论证差异。独立核对 [scheduler.cpp L297–308](https://github.com/Ascend/MindIE-LLM/blob/69e5a5dd4b533eaffc7e198320435350825a36f7/src/scheduler/scheduler.cpp#L297-L308)、[scheduling_budget.cpp L17–34](https://github.com/Ascend/MindIE-LLM/blob/69e5a5dd4b533eaffc7e198320435350825a36f7/src/sequence/scheduling_budget.cpp#L17-L34)、[FcfsPolicy MIX L92–111](https://github.com/Ascend/MindIE-LLM/blob/69e5a5dd4b533eaffc7e198320435350825a36f7/src/scheduler/policy/fcfs_policy.cpp#L92-L111)及 [decode 预算累计 L325–337](https://github.com/Ascend/MindIE-LLM/blob/69e5a5dd4b533eaffc7e198320435350825a36f7/src/scheduler/policy/fcfs_policy.cpp#L325-L337)、[PolicyHelper L48–55](https://github.com/Ascend/MindIE-LLM/blob/69e5a5dd4b533eaffc7e198320435350825a36f7/src/scheduler/policy/policy_helper.cpp#L48-L55)，修订与所核路径相符。结论仅限这些路径，不推广到所有策略／PD 角色；新添 slot 配额解释的问题独立列为 R04，不否定此次共享预算订正。 |
| **R02（P2）** 显式值被当作最终配置 | **CLOSED** | L63 已明确后续模型覆盖不受用户是否显式开启限制。固定 [SchedulerConfig.__post_init__ L214–223](https://github.com/vllm-project/vllm/blob/b17039bccc17b94a2ea107272ad7bc93508708df/vllm/config/scheduler.py#L214-L223)在 `is_encoder_decoder` 成立时直接置 `enable_chunked_prefill = False`，同时设置 `disable_chunked_mm_input = True`、长 prefill 阈值为 0，支持所列反例。与 C03 共用修订，满足本项关闭条件。 |
| **R03（P2）** CUDA 制品声明冲突 | **CLOSED** | L81 已并列概述 12.8、Pre-built wheels 默认 12.9 与 12.8／13.0 变体，未选变体前保留制品身份 unknown。重开[版本化安装页概述及 Pre-built wheels](https://docs.vllm.ai/en/v0.14.0/getting_started/installation/gpu/#pre-built-wheels)与固定 [gpu.cuda.inc.md L1–38](https://github.com/vllm-project/vllm/blob/b17039bccc17b94a2ea107272ad7bc93508708df/docs/getting_started/installation/gpu.cuda.inc.md#L1-L38)，确有同一页面／原文件中的两种声明。修订没有任选一种作为实际 wheel 身份，也未冒称驱动配套验证。C01 所需的其他档案字段／就近引用仍另行保留。 |

## 新发现

### T07-02-R04 — P2：slot 预算表的初始化被用作已生效配额机制的差异依据

- 位置：正文 L67 的“并另设 partial prefill slot 配额”及紧随其后的“partial prefill 配额机制各自不同”；来源表 L44、registry L6719 的相应摘要需同步限定。
- 问题：新修订引用构造函数 L17–34，能够证明共享上限覆盖及 `partialPrefillOccupiedBudgetPerSlot_` 的初始化，却未证明该 slot 表实际参与分配。将它直接列入两引擎运行机制不可等价的依据，仍有从数据结构存在／初始化扩大到有效路径的问题。
- 固定源码证据：[SchedulingBudget::GetPrefillSlots L44–72](https://github.com/Ascend/MindIE-LLM/blob/69e5a5dd4b533eaffc7e198320435350825a36f7/src/sequence/scheduling_budget.cpp#L44-L72)中，非 chunked 路径返回剩余预算；chunked 路径在 L53–57 按 `prefillChunkSize != 0` 返回该值，否则返回 `maxPrefillTokens`，两分支都直接返回。其后 L59–72 根据统计量读取 slot 表的动态分配代码，在此固定实现中不可达。实际调用方 [PolicyHelper L100–106](https://github.com/Ascend/MindIE-LLM/blob/69e5a5dd4b533eaffc7e198320435350825a36f7/src/scheduler/policy/policy_helper.cpp#L100-L106)取 `min(待计算 token, 剩余 token 预算, GetPrefillSlots())`。
- 审阅判断：构造函数初始化的事实本身正确，问题在于据此说明有效分配机制差异。上述控制流不能支持“按该 slot 表动态分配配额已生效”的解释。这不否认同文件另有长 partial prefill 的并发门控，也不推断全仓所有配额机制失效；它们须与这张 slot 预算表分开说明。
- 关闭条件：将相关表述明确限定为“slot 表被初始化，但所核 GetPrefillSlots 的动态读取分支不可达”，或改用已经核实的固定／配置切块与剩余共享预算裁剪规则解释该路径；不得继续用该表的初始化证明运行差异。若保留其他 partial prefill 门控作为比较依据，应定位实际消费路径，并分别说明两侧已核条件；同步正文、来源表和登记摘要。无需修改上游代码或进行硬件实验。

## 整体结论

**未通过本轮定向复核。** 本轮 **C02、C03、R01、R02、R03 为 CLOSED**；**C01、C04 未关闭**，保留原 P2。修订新增 **R04（P2）**，涉及 slot 预算表初始化与实际可达分配路径的区分。C04 与 R04 的修订范围有交集，不把它们累计成互不相关的根因。C05／C06／C07 沿用第一轮 CLOSED，本轮没有重开。

剩余工作是完成有限平台样板的身份／条件记录，补足受限的抢占—释放／重置—再入队场景，并修正配额机制依据，再作定向复核。正文继续保持 `draft / source_checked` 的来源核对边界；MindIE `latest` 同版关系、实际部署组合和硬件功能交集均未因此证实。

临时副本的 `make check`、`make build` 均通过，不改变上述技术审阅结论。写报告前后核对原工作区文件摘要，本轮仅新增本报告，既有文件保持不变。
