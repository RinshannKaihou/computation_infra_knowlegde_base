# Batch 26 T07-02 独立审阅报告

## 审阅头部

- 角色：与正文作者独立的知识库批次审阅者；只记录发现，不代作者修订正文、来源登记或计划。
- 模型／推理档位：`gpt-6.1-sol / xhigh`。本轮本地会话 `01a15801-6dd8-7912-8be6-1fd820b99f86` 的执行记录为 `originator: codex_exec`、`source: exec`、CLI `0.163.0`；全部 `turn_context` 只有上述单一模型与档位，未见审阅输出中的模型回退标记。未派发其他模型或子代理。
- 日期：2026-10-20（Asia/Shanghai）。
- 验收基准：`plans/full-coverage-backlog.yaml:6264` 的 T07-02，五条 acceptance 逐项核对；来源与行号按 [authoring-guide 第 5 节](../authoring-guide.md#5-来源证据与许可)处理。
- 审阅对象：
  1. `knowledge/07-inference/engine-backend-boundaries.md` 全文与 frontmatter。
  2. `knowledge/07-inference/index.md` 仅 T07-02 新增条目、对应 related ID、07.2／07.3 主题行；不重审 T07-01 的新增内容。
  3. `sources/registry.yaml` 仅三个新增 ID：`src.vllm.core-components-v0-14`、`src.vllm.platforms-cuda-rocm-v0-14`、`src.ascend.mindie-llm-src-69e5a5dd`，以及 `src.ascend.vllm-ascend-v0-14-0rc1` notes 的第二十六批平台／组件覆盖扩展。
  4. `docs/research/batch-26-t07-02-sources.md` 作者来源记录。

### 取证方式与限制

1. 独立通过 GitHub 文件／目录读取工具重新打开固定原文件，未以作者缓存代替上游取证：vLLM `b17039bccc17b94a2ea107272ad7bc93508708df` 的 `vllm/v1/core/`、`sched/` 目录及 `scheduler.py`、`interface.py`、`request_queue.py`、`async_scheduler.py`、`kv_cache_manager.py`、`platforms/cuda.py`、`rocm.py`；补开同 commit 的调度配置、参数默认值入口、平台接口与一个使用 simple compile backend 的调用点。
2. 重新打开 vllm-ascend `52d4acfa51fb868823d1070b81cbd2d97e9e4696` 的根目录、`vllm_ascend/`、`core/`、`platform.py`、根 `README.md`、两个调度覆盖件，另核对 `compilation/compiler_interface.py` 与插件注册入口。正文列举的 Python 子目录及 `Dockerfile.310p`／`Dockerfile.a3` 均在对应目录清单中；目录存在性不作为功能已启用的证明。
3. 重新打开 MindIE-LLM `69e5a5dd4b533eaffc7e198320435350825a36f7` 的 `src/`、`scheduler/`、`scheduler/policy/`、`block_manager/`、`engine/` 目录，以及作者所列调度／策略／块管理／引擎头文件和 CoW 文件。另补开 `policy_factory.cpp`、`fcfs_policy.cpp`、`config_info.h`、`scheduling_budget.h` 与根 README，分别检查可构造策略、批预算和声明范围。
4. 重新打开 vLLM v0.14.0 GPU 安装页、Feature × Hardware／Feature × Feature 页面及 MindIE latest 模型支持页。复用 registry 既有 notes 核对 W8A8 Functional／W4A8 在研、xPyD／Mooncake／异构限制、block_size 128、Turing 量化冲突、Volta 矩阵限制；这些历史主张没有全部重新下载上游。不把 MindIE latest 的本次可访问性当作版本 gate 已关闭。
5. GitHub 返回的原文件内容保留空行；源码坐标使用其 1-based 原文件行号。抽查包括 vLLM Scheduler L65／L252／L572–578、RequestQueue L13／L75／L131、KVCacheManager L144／L164／L206／L373／L383、NPUPlatform L95／L99／L104，以及 MindIE scheduler.h L33／L61、policy.h L22／L67／L75、pdds_policy.h L27／L38。未将网页阅读工具行号直接拼成 GitHub 锚点。
6. 作者清单中 17 份源码／README 的 SHA-256 前 16 位与本次 GitHub 重新取回内容全部一致；另对已有 `/private/tmp/vllm-ascend-52d4acf.tar.gz` 复算，得到 `98b138527766be0b`，与记录一致。该压缩包没有重新下载，摘要一致只证明本机已有包与作者记录相符。README 清单路径错误另见 C07。
7. 部分 raw／tree URL 的网页读取最初返回 Cache miss，两次 GitHub 目录调用发生传输错误；改用 GitHub 文件／Contents API 后，要求的文件和目录均已取得。额外启动的一层嵌套 CLI 在模型调用前因 `Operation not permitted` 退出，未产生审阅结果、未计入审阅轮次；有效审阅由上述已经运行的本地 CLI 会话完成。
8. 未安装、构建或启动任何推理引擎，未执行模型请求、硬件测试、配置变更或清理操作。以下“支持”核对仅涉及来源声明／代码条件，不是本库硬件验证。

## 发现列表

共 **7 项开放发现：P1 0 项、P2 6 项、P3 1 项**。关闭须经作者修订和独立定向复核，本次不将任何发现标为已关闭。

### T07-02-C01 — P2：平台概览尚未形成验收要求的有限条件档案

- 位置：`knowledge/07-inference/engine-backend-boundaries.md:69`、`:75`–`:89`、`:95`–`:101`；对应 acceptance 第 2、3 条。
- 发现：NVIDIA 表没有模型、并行、KV 特性记录，AMD 表没有模型、并行与 PD 记录；Ascend 表的“逐模型矩阵”仍只描述外部表的形式，没有选定有限模型／模型族及其条件。“量化支持（按方法）”“代码层清单”“大规模 EP 教程存在”也未落实到所选方法／并行方式的支持条件。档案没有逐一登记组件制品、驱动／运行库和模型身份的已知值或 unknown；NVIDIA 硬件行甚至未带安装页的最低计算能力条件。升级检查表要求未来重建身份，不能代替当前样板的身份记录。
- 证据：[T07-02 acceptance](../../plans/full-coverage-backlog.yaml) 明确要求上述特性与依赖字段；[v0.14.0 GPU 安装页 Requirements](https://docs.vllm.ai/en/v0.14.0/getting_started/installation/gpu/#requirements) 给出 NVIDIA compute capability 7.0+ 及 AMD 的分硬件版本要求，并在安装部分说明二进制与 CUDA／PyTorch 构建的关系；[Ascend 固定 README L49–57](https://github.com/vllm-project/vllm-ascend/blob/52d4acfa51fb868823d1070b81cbd2d97e9e4696/README.md#L49-L57) 还明确列出 Python、PyTorch／torch-npu 条件。本项是验收覆盖不足，不是认定正文虚构了一个已验证部署组合；正文的“未实测／不拼接”声明正确。
- 关闭条件：为三平台选定有限的文档模型／硬件样板，逐项列出模型、硬件、量化、并行、图、PD、KV 的状态、条件与精确来源。记录各自 ref、制品身份／构建方式、驱动／运行库和模型条件；缺证据的字段显式写 unknown，并限制对应支持结论。无需补造环境、摘要或测试结果，也无需穷举支持全集。补充的关键条件附近应有可直接追溯的 URL／章节，不能仅写“见登记 notes”。

### T07-02-C02 — P2：simple compile backend 的 eager 被扩大为整个引擎默认关闭编译

- 位置：`knowledge/07-inference/engine-backend-boundaries.md:56`、`:97`、`:108`；`sources/registry.yaml:555` 的本轮扩展；`docs/research/batch-26-t07-02-sources.md:38`。
- 发现：`simple_compile_backend = "eager"` 字段和其注释确实存在，但不足以推出粗体的“torch.compile 默认关闭”，更不足以把整个引擎的 eager 默认写成升级时可继承核验的已知事实。同一平台实现另有自定义 compiler 入口、`VLLM_COMPILE`／PIECEWISE 分支及 `enforce_eager`／图模式条件，不能把 simple backend、Inductor 代码生成、模型编译与 ACL graph 混为一个开关。
- 证据：[固定 platform.py L95–136](https://github.com/vllm-project/vllm-ascend/blob/52d4acfa51fb868823d1070b81cbd2d97e9e4696/vllm_ascend/platform.py#L95-L136) 同时定义 simple backend 与 `get_compile_backend()`；[L234–246](https://github.com/vllm-project/vllm-ascend/blob/52d4acfa51fb868823d1070b81cbd2d97e9e4696/vllm_ascend/platform.py#L234-L246)、[L282–307](https://github.com/vllm-project/vllm-ascend/blob/52d4acfa51fb868823d1070b81cbd2d97e9e4696/vllm_ascend/platform.py#L282-L307) 区分 eager、compilation mode、OOT compiler 与 `use_inductor`；[同快照 AscendCompiler L109–139](https://github.com/vllm-project/vllm-ascend/blob/52d4acfa51fb868823d1070b81cbd2d97e9e4696/vllm_ascend/compilation/compiler_interface.py#L109-L139) 有实际编译后端分派。本次不反向宣称任意未锁定配套的模型默认一定启用编译。
- 关闭条件：将现有结论收窄到该字段的 simple backend 范围，分开说明模型编译、Inductor 与 ACL graph。若要给出完整默认执行路径，须锁定同线配套与配置入口后取证；未取得时保留 unknown。同步修订正文、登记扩展和作者来源表，升级检查表不再沿用未经证明的全局默认。

### T07-02-C03 — P2：pooling 门控注释被推广为通用 chunked prefill 开启规则

- 位置：`knowledge/07-inference/engine-backend-boundaries.md:53`、`:63`；`sources/registry.yaml:6691`；`docs/research/batch-26-t07-02-sources.md:34`。
- 发现：反复使用“chunked prefill 显式开启”，却没有区分用户显式设置、配置最终取值与模型能力推导出的默认值。作者取证点 L572–573 的“显式”注释限定 pooling 请求；它不能被直接提炼成全体生成模型都须手工开启的规则。
- 证据：[scheduler.py L572–582](https://github.com/vllm-project/vllm/blob/b17039bccc17b94a2ea107272ad7bc93508708df/vllm/v1/core/sched/scheduler.py#L572-L582) 是最终配置门控；[EngineArgs L1900–1934](https://github.com/vllm-project/vllm/blob/b17039bccc17b94a2ea107272ad7bc93508708df/vllm/engine/arg_utils.py#L1900-L1934) 在参数未设置时根据 `model_config.is_chunked_prefill_supported` 决定默认值，并分别处理 generate／pooling 的手工覆盖；[SchedulerConfig L78–83](https://github.com/vllm-project/vllm/blob/b17039bccc17b94a2ea107272ad7bc93508708df/vllm/config/scheduler.py#L78-L83) 的 dataclass 默认也注明实际使用应由 EngineArgs 决定。
- 关闭条件：明确“是否分块由最终配置及模型条件控制”，区分自动默认与显式覆盖，将 pooling 注释限定在原上下文；不把测试用 dataclass 默认直接当全部服务入口默认。三处记录同步修正，并在相关主张旁补参数默认值入口。

### T07-02-C04 — P2：不直译的原则尚未落实为参数与调度／KV 语义比较

- 位置：`knowledge/07-inference/engine-backend-boundaries.md:61`–`:65`、`:120`；`docs/research/batch-26-t07-02-sources.md:48`–`:53`；索引 `knowledge/07-inference/index.md:41`、`:64` 的覆盖描述；对应 acceptance 第 4 条。
- 发现：本节正确禁止跨引擎参数直译，但实际内容主要是组件名、策略名与“另一套参数体系”。没有说明选定参数控制的预算单位／迭代范围、调度先后、缓存命中如何改变待计算量、抢占／块释放与重新排队的关系。保留完整算法未核是合理的，不能因此把已要求的有限语义比较整体留待以后。现有观测／诊断链接正确，但不能补足引擎之间尚未写出的区别。
- 证据：[vLLM SchedulerConfig L50–61](https://github.com/vllm-project/vllm/blob/b17039bccc17b94a2ea107272ad7bc93508708df/vllm/config/scheduler.py#L50-L61) 区分每迭代 token 数和 sequence 数；[Scheduler L252–289](https://github.com/vllm-project/vllm/blob/b17039bccc17b94a2ea107272ad7bc93508708df/vllm/v1/core/sched/scheduler.py#L252-L289) 明示按 token 进度统一调度、先处理 running 请求。[MindIE SchedulerConfig L399–427](https://github.com/Ascend/MindIE-LLM/blob/69e5a5dd4b533eaffc7e198320435350825a36f7/src/include/config/config_info.h#L399-L427) 有阶段选择、动态 batch、`maxPrefillBatchSize`／`maxPrefillTokens`／`maxBatchSize` 等不同字段；[FcfsPolicy L37–111](https://github.com/Ascend/MindIE-LLM/blob/69e5a5dd4b533eaffc7e198320435350825a36f7/src/scheduler/policy/fcfs_policy.cpp#L37-L111) 按阶段优先级分派，并在 MIX 路径先调 running／swapped、再 waiting。KV 方面，[vLLM get_computed_blocks L164–204](https://github.com/vllm-project/vllm/blob/b17039bccc17b94a2ea107272ad7bc93508708df/vllm/v1/core/kv_cache_manager.py#L164-L204) 与 [MindIE SelfAttnBlockManager L27–35、L57–65](https://github.com/Ascend/MindIE-LLM/blob/69e5a5dd4b533eaffc7e198320435350825a36f7/src/block_manager/self_attn_block_manager.h#L27-L65) 已提供可限定比较的不同职责入口；接口存在不证明所有运行条件。
- 关闭条件：选取少量有源码／文档支持的参数及 batch／KV 场景，分别解释单位、作用阶段、调度顺序、命中／抢占／释放边界和比较时须固定的条件；列“不可直接等价”的具体原因，不要求构造一一映射。Ascend 覆盖件未核部分继续明确保留。新增解释须就近引用，来源表应区分已补核与仍未知的范围；索引描述与实际交付一致。

### T07-02-C05 — P2：未定版 MindIE 模型表被放入“每行固定 ref”的源码档案

- 位置：`knowledge/07-inference/engine-backend-boundaries.md:69`、`:91`、`:95`–`:98`、`:118`。
- 发现：frontmatter、范围声明和冲突行保留 latest gate，这点正确；但“每行锚定固定 ref”及 `MindIE-LLM（69e5a5dd）` 列又直接承载 latest 模型支持表的硬件、量化、图和卡数声明，未在这些行区分“固定源码事实”与“未定版网页的取回时声明”。这会把尚未建立的网页—源码版本对应关系隐式回填。正文链接旁也没有写明该 latest 页的取回日期。
- 证据：[固定 README L59–76](https://github.com/Ascend/MindIE-LLM/blob/69e5a5dd4b533eaffc7e198320435350825a36f7/README.md#L59-L76) 分别给软件／CANN 表和 latest 外链，没有把外链内容固定到该 commit；[模型支持列表](https://mindie-llm-doc.readthedocs.io/zh-cn/latest/user_guide/model_support_list/) 本次仍是 latest 地址。既有 `src.ascend.mindie-llm-doc-latest` 的 revision 明确要求引用带 2026-10-20 取回日期，定版关系待核。报告没有因重新打开页面而撤销这一限制，也未外推到 hiascend 产品包。
- 关闭条件：修改“每行固定 ref”的总述，给每行／分组明确证据身份；latest 模型表单列为“2026-10-20 取回的文档声明，未与 69e5a5dd／具体产品包核同版”。只有取得可验证版本映射才合并成该源码档案的支持结论；此前继续保留对应关系 unknown。源码类存在性等已固定事实可以原样保留。

### T07-02-C06 — P2：将 PRIORITY 枚举提升为 MindIE 已实现的调度策略族成员

- 位置：`knowledge/07-inference/engine-backend-boundaries.md:63`。组件表 `:53` 对“枚举”的区分本来正确。
- 发现：将 `FCFS/PRIORITY/Layerwise/PDDS` 并列为 MindIE 调度策略族，容易读成与 vLLM PriorityRequestQueue 相对应的可用实现。固定头文件只有 `PolicyType::PRIORITY` 枚举；补查工厂时，普通 PnD／Flex 分支构造 FCFS 或 LayerwiseFCFS，P／D 分支构造 PDDS，没有在该工厂建立 PRIORITY 的实现分派。枚举存在不能证明策略可用。
- 证据：[policy.h L22](https://github.com/Ascend/MindIE-LLM/blob/69e5a5dd4b533eaffc7e198320435350825a36f7/src/scheduler/policy/policy.h#L22) 为枚举；[policy_factory.cpp L26–54](https://github.com/Ascend/MindIE-LLM/blob/69e5a5dd4b533eaffc7e198320435350825a36f7/src/scheduler/policy/policy_factory.cpp#L26-L54) 的实际构造路径及注释限定当前 prefill／decode 为 FCFS。相较之下，[vLLM request_queue.py L131–146](https://github.com/vllm-project/vllm/blob/b17039bccc17b94a2ea107272ad7bc93508708df/vllm/v1/core/sched/request_queue.py#L131-L146) 确有 PriorityRequestQueue 实现。本项只限定已检查的工厂路径，不声称完成 MindIE 全仓不存在性证明。
- 关闭条件：把枚举声明和可构造策略分开，撤回 PRIORITY 已可用的暗示；若保留运行支持主张，应补其具体实现、注册／构造路径及触发条件。不得因两边都出现 PRIORITY 字符串而建立语义等价关系。

### T07-02-C07 — P3：作者来源表有两处原文件路径／层级定位错误

- 位置：`docs/research/batch-26-t07-02-sources.md:18`、`:41`；`sources/registry.yaml:6719` 的层级表述需一并明确。
- 发现：取回清单把 README 写为 `vllm_ascend/README.md`，实际摘要对应仓库根 `README.md`，`vllm_ascend/` 目录没有该文件。MindIE 主张表又把 `latency_predictor` 放进 `policy/ 目录（dynamic_batch_size、latency_predictor、stage_policy）`，实际它是 `scheduler/latency_predictor/`，与 `policy/` 同级。摘要均吻合，问题是定位，不是伪造文件内容。
- 证据：[Ascend 根 README](https://github.com/vllm-project/vllm-ascend/blob/52d4acfa51fb868823d1070b81cbd2d97e9e4696/README.md)、[vllm_ascend 目录](https://github.com/vllm-project/vllm-ascend/tree/52d4acfa51fb868823d1070b81cbd2d97e9e4696/vllm_ascend)；[MindIE scheduler 目录](https://github.com/Ascend/MindIE-LLM/tree/69e5a5dd4b533eaffc7e198320435350825a36f7/src/scheduler)、[policy 目录](https://github.com/Ascend/MindIE-LLM/tree/69e5a5dd4b533eaffc7e198320435350825a36f7/src/scheduler/policy)。本次均以 Contents API 独立核对目录成员。
- 关闭条件：使用仓库相对路径 `README.md` 与 `src/scheduler/latency_predictor/`，将 policy 下的 dynamic_batch／stage_policy 与同级 latency_predictor 分开；消除 registry notes 对该层级的歧义，保留正确摘要和原始取证范围。

## 五条 acceptance 对照

| 验收条款 | 审阅结果 |
|---|---|
| 1. 比较三条引擎线的架构／实际组件，区分产品包与源码仓 | 基本具备。源码组件、Python／C++ 边界及产品包未知范围有明确声明；策略摘要中的枚举／实现混淆见 C06，证据路径见 C07。没有把产品包功能自动写成开源仓能力。 |
| 2. 三平台有限样板，按模型／硬件／量化／并行／图／PD／KV 记录状态与条件 | 部分满足。已有三平台表和部分约束，但缺失维度／有限条件见 C01，编译默认及 MindIE 文档身份见 C02、C05。不能仅凭表格已建认定验收完成。 |
| 3. 固定 release/ref、组件制品、驱动／运行库和模型条件；缺依赖不写支持组合 | 部分满足。三条源码 ref 明确且没有拼成已验证栈；当前档案依赖／模型字段不足见 C01，latest 与固定源码关系见 C05。需逐档案保留 unknown，不能由升级清单替代。 |
| 4. 比较参数与调度／KV／缓存语义，并链接主归属的观测／诊断／验证入口 | 部分满足。链接正确、不直译原则正确；具体语义覆盖不足见 C04，开启规则与策略可用性见 C03、C06。 |
| 5. 升级替换后重核功能、质量／服务指标与回退条件的检查表 | 已核对，未见问题。六项清单覆盖身份、功能、质量／服务基线、版本冲突、回退对象／判据／演练及能力移除；其中被当作既知默认值的例子须随 C02 修订。清单是待执行核验要求，未冒充完成记录。 |

## 审阅维度逐项记录

| 维度 | 核对结论 |
|---|---|
| frontmatter、稳定 ID、类型／领域／状态、标题／日期 | 已核对，未见问题。`reference / inference / draft`，标题一致；三个具体平台均有正文范围，未用 `generic` 推导兼容。 |
| source_refs、evidence_refs、related_ids 与本地链接 | 已核对，未见问题。12 个 source_refs、3 个 evidence_refs、6 个 related_ids 均存在且类型／用途合理；未混入虚构证据或把源 ID 写成相关正文 ID。 |
| 适用性／验证状态 | 已核对，未见问题。环境引用为空，`source_checked` 明示仅源码／文档核对，未写 reproduced。技术摘要仍须按发现修订，状态字段本身不免除修订义务。 |
| 产品包／开源仓范围与三条源码版本线 | 已核对，未见问题。产品门户未取证、产品包范围 unknown、两条 Ascend 线独立、上游 v0.14.0 不与插件线拼栈均保留；latest 文档到源码的局部归属问题另见 C05。 |
| vLLM Scheduler／接口／队列／AsyncScheduler 与 KV 分层 | 组件存在性、继承关系与方法坐标已核对，未见问题。chunked prefill 摘要问题见 C03；调度／KV 的比较深度见 C04。 |
| CUDA／ROCm 平台责任面与条件声明 | 代码切面已核对，未见问题。ROCm 量化列表被标为代码层清单，bitsandbytes 条件、V0 后端移除、ViT 支持集／断言均有源码；未把代码清单当实测全集。有限档案的缺项见 C01。 |
| vllm-ascend OOT 平台、覆盖件与子目录 | 组件存在性已核对，未见问题。NPUPlatform、两个 scheduler 覆盖件及列举子目录存在，README 版本线与专用 Dockerfile 存在；全局编译默认推断见 C02，README 路径见 C07。覆盖件与上游语义差异没有因本次打开文件被擅自关闭。 |
| MindIE scheduler／policy／block_manager／engine 实际组件 | 类与文件清单基本相符；PreemptionMode 三值、Policy／KVTransferPolicy、FCFS 派生类、CoW／引用计数／块表、引擎输出处理等已核对。PRIORITY 运行策略的暗示见 C06，目录层级见 C07；pre/post 头文件中的信息共享／批同步辅助职责不等同完整调度算法。 |
| 三平台模型／硬件／量化／并行／图／PD／KV 交集 | 有发现：C01、C02、C05。缺失字段不能通过省略变成“均已支持”；单个平台特性打勾也不建立全部特性同时启用的组合证明。 |
| batch／KV／缓存参数与调度语义 | 有发现：C03、C04、C06。未发现已给出错误的一一参数翻译，但“禁止直译”尚不足以完成参数作用域与调度差异的解释。 |
| 复用历史主张与冲突 | 按允许的 registry 既有 notes 已核对，未见问题。量化在研、PD 异构与 TP 限制、block_size 128、Turing 冲突、Volta 限制均未被抹平；同线 conf.py／version policy 冲突仍保留。 |
| latest gate 与其他 unknown | MindIE latest 归属有 C05；其余已核对，未见问题。MindIE 算法／触发条件、产品包范围、PD 材料、llm_manager／v2 关系、覆盖件差异及 tag 时间序没有被回填。源码可见接口不替代运行验证。 |
| 三条新增来源及一条 notes 扩展的许可范围 | 已核对，未见问题。vLLM 源码 SPDX Apache-2.0 与已登记根许可口径一致；MindIE 所检文件头声明 Mulan PSL v2，src 范围排除另有声明／第三方内容；未把源码根许可自动覆盖到生成站点或产品包。notes 的技术摘要仍需 C02、C03、C07 修订。 |
| 作者来源记录的摘要与原文件坐标 | 摘要及所抽查源码行号已核对，未见问题；文件路径／层级有 C07。压缩包本机摘要与独立重开源码的证据强度已经分开。 |
| 主张附近的证据定位 | 当前可由文末来源列表与作者定位表追溯主要组件；平台条件及新增语义的就近精确引用须按 C01、C03、C04 补齐。`source_refs` 和“登记 notes”文字不应代替这些新增主张的定位。 |
| 索引新增 related ID、条目与 07.2／07.3 行 | 链接／ID／主归属已核对，未见问题。内容覆盖描述随 C01、C04 补齐或收窄；没有在索引中宣称审阅已通过或硬件验证完成。 |
| 升级、质量／指标、回退与能力移除 | 已核对，未见问题。检查表有明确核验对象与证据记录要求，不以一次回退成功替代全部条件；C02 涉及的默认值例子须修订。 |
| 虚构参数／组件／命令／实测、缺依赖支持、跨引擎直译 | 未发现虚构命令、测试结果、现场事故或缺依赖的已验证组合，也未发现把上游文档当执行授权。默认语义扩大及枚举到实现的越证据推断分别见 C02、C03、C06。 |

## 结构检查与改动边界

- 原仓 `PYTHONDONTWRITEBYTECODE=1 make check`：通过，**109 content entries／537 sources**。这是结构、ID 与本地链接检查，不是技术正确性／远程内容验证。
- `make build` 只在 `/private/tmp/t07-02-review-28of0pvq/snapshot` 的临时副本执行，使用原仓 `.venv` Python：通过，同为 109 entries／537 sources，已核对新正文在清单中的元数据。副本第一次构建因未复制已被现有文档链接的 `build/catalog.json`／`catalog.md` 而失败；补齐这两个既有链接目标后重建通过。这是临时副本准备问题，不记为正文发现，原仓 `build/` 未重建。
- 未修改 `src/kb/`，未新增测试或执行硬件测试。进入审阅时记录的 547 个既有源／文档文件摘要在写报告前复核均未变化；现有未提交改动保留。本轮唯一仓库新增交付文件是本报告。

## 整体结论

**需修订，T07-02 当前不通过。** 三条源码线的组件目录、主要继承关系和大部分来源摘要有可靠依据，产品包／源码仓及未实测边界也已明确；但三平台有限条件档案和参数／调度语义比较尚未满足全部 acceptance，另有编译默认、chunked prefill 规则、MindIE PRIORITY 策略及 latest 归属的表述需要纠正。

作者须按 C01–C07 的关闭条件修订，并同步受影响的 registry notes、来源表和索引描述；之后由独立审阅者进行定向复核，才可判断是否通过。即使后续来源／编辑审阅通过，也不构成 NVIDIA、AMD 或 Ascend 的部署兼容性、功能交集、数值质量或服务指标的硬件验证。
