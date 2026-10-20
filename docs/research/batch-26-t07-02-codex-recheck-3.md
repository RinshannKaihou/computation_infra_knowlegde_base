# Batch 26 T07-02 第三轮定向复核

## 复核头部

- 角色：知识库批次审阅者；仅核对[第二轮复核](batch-26-t07-02-codex-recheck-2.md)留下的 **C01、C04、R04** 及第三轮修订引入的问题。C02／C03／C05／C06／C07／R01／R02／R03 沿用 CLOSED，不重新展开审阅。
- 模型／推理档位：`gpt-6.1-sol / xhigh`。已读取本轮本地 Codex CLI 会话 `01a1582f-7e2a-79e3-bb5f-69c270d0480d` 的执行元数据：`originator: codex_exec`、`source: exec`、CLI `0.163.0`，本轮 `turn_context` 为上述单一模型与档位；未见模型回退，未调用其他模型或子代理。
- 日期：2026-10-20（Asia/Shanghai）。
- 本地对象：[正文](../../knowledge/07-inference/engine-backend-boundaries.md)第三轮改动及必要邻接语境、[作者来源记录](batch-26-t07-02-sources.md)、[registry](../../sources/registry.yaml)相关 notes；对照[原关闭条件](batch-26-t07-02-codex-review.md)与第二轮剩余条件。本报告本地行号以本轮读取位置为准。
- 独立取证：GitHub blob／raw URL 的网页读取返回 Cache miss 后，改用 GitHub 文件／Contents API 重新取回固定 ref 原文件，按保留空行的原文件坐标核对，未以作者缓存代替本轮取回。
  - vLLM `b17039bccc17b94a2ea107272ad7bc93508708df`：`vllm/v1/core/sched/scheduler.py`、`vllm/v1/core/kv_cache_manager.py`；新增引用所指的量化 `README.md`／`int8.md`、`disagg_prefill.md`，并定向补看 `nixl_connector_usage.md` 与 connector `factory.py`。
  - MindIE-LLM `69e5a5dd4b533eaffc7e198320435350825a36f7`：`src/scheduler/policy/fcfs_policy.cpp`、`src/sequence/scheduling_budget.cpp`、`src/scheduler/policy/policy_helper.cpp`；另取 `docs/zh/user_guide/model_support_list.md` 核对模型表原始标记。
  - vllm-ascend `52d4acfa51fb868823d1070b81cbd2d97e9e4696`：根 `README.md`、`tutorials/DeepSeek-R1.md`／`DeepSeek-V3.1.md`、`faqs.md`、`supported_features.md`、`disaggregated_prefill.md`；Contents API 核对 V3.2／GLM4.x／Kimi-K2-Thinking 教程文件存在。
- 取回一致性：重新计算 SHA-256 前 16 位：vLLM `scheduler.py`＝`b4e664fe7dc9ea5c`、`kv_cache_manager.py`＝`6362906d91adf7d1`；MindIE `scheduling_budget.cpp`＝`e512c6f55db58e02`、`policy_helper.cpp`＝`6acd5989b39fe8d1`，均与作者来源表一致。此次补核的 MindIE `fcfs_policy.cpp`＝`41db63a789f6371c`。
- 文档重开：MindIE [模型支持列表](https://mindie-llm-doc.readthedocs.io/zh-cn/latest/user_guide/model_support_list/)与[快速入门](https://mindie-llm-doc.readthedocs.io/zh-cn/latest/user_guide/quick_start/quick_start/)，仍仅作 **2026-10-20 取回的 latest 声明**。固定仓内模型表的相应行和图例可作交叉核对，不因此建立整个 latest 站点、源码与产品包的同版关系。
- 执行边界：仅新增本报告；未修改正文、来源登记、索引、计划或原工作区构建产物，未安装、构建或运行推理引擎，未进行硬件验证。
- 结构校验：在包含本报告与既有 `build/` 链接目标的临时工作区副本执行 `make check`、`make build`，均通过（109 content entries／537 sources）。仅验证结构与本地引用，不证明技术正确性或远程内容；原工作区 `build/` 未改动。

## C01（P2）— 未关闭：模型样板与读表修订成立，依赖身份仍未补齐

**已满足的部分：**

- 正文 L108 已实际选择 DeepSeek 系教程，不再把 README 的模型类别当作具体模型样板。固定 [DeepSeek-R1 教程 L6–18](https://github.com/vllm-project/vllm-ascend/blob/52d4acfa51fb868823d1070b81cbd2d97e9e4696/docs/source/tutorials/DeepSeek-R1.md#L6-L18)使用 R1-W8A8 样板并给出 A2／A3 节点条件；[V3.1 教程 L25–30](https://github.com/vllm-project/vllm-ascend/blob/52d4acfa51fb868823d1070b81cbd2d97e9e4696/docs/source/tutorials/DeepSeek-V3.1.md#L25-L30)分别列出 BF16 与量化变体。正文保留“教程存在不等于具体版本组合支持”，没有把这些教程自动拼成已验证栈。
- MindIE 的 Qwen2-7B-Instruct 读表值正确：128k；W8A8／LoRA 为支持，W4A8／W8A16 为不支持；atbgraph 支持、aclgraph 不支持；A2 为 1／2／4 卡、推荐 2 卡，A3 与 300I Duo 均为 1／2 卡、推荐 1 卡。[latest 模型表 Qwen 系列](https://mindie-llm-doc.readthedocs.io/zh-cn/latest/user_guide/model_support_list/)与这些逐列值一致；[固定仓内原始图例及 Qwen 行](https://github.com/Ascend/MindIE-LLM/blob/69e5a5dd4b533eaffc7e198320435350825a36f7/docs/zh/user_guide/model_support_list.md#L3-L39)进一步显示该行是绿色标记，表示充分验证支持。这里是上游文档的支持分级，不是本库实验结论。正文 L111–112 的量化／图样板值同步正确。
- [快速入门的获取权重章节](https://mindie-llm-doc.readthedocs.io/zh-cn/latest/user_guide/quick_start/quick_start/)指向 Qwen2-7B 基础版；正文已明确它与 Instruct 读表行不同，未把两种身份混用。
- NVIDIA L88 补出了 Llama 实现样板与权重／tokenizer 待现场固定的状态，wheel 变体未选也有明确记录。量化 README、Ascend 特性表与 PD 指南、[FAQ 14 L152–156](https://github.com/vllm-project/vllm-ascend/blob/52d4acfa51fb868823d1070b81cbd2d97e9e4696/docs/source/faqs.md#L152-L156)的就近链接均有改进；FAQ 的 MLA 与 TP 拆分约束确实属于所引用章节。

**仍未满足的关闭条件：**

1. **三平台的依赖身份记录仍有缺项。** NVIDIA L80–88 没有驱动版本的已知值或 unknown；AMD L94–102 没有驱动、模型权重／tokenizer revision，以及未选容器／制品身份的显式未知记录；Ascend 两条引擎线 L108–116 仍没有各自 HDK／驱动、模型权重／tokenizer revision、未选具体镜像／包身份的已知值或 unknown。CANN／ROCm 版本、镜像名称、Dockerfile 和模型名称分别不能替代这些字段。NVIDIA 新行已覆盖的“待固定”不要求重复填报，但不能据此视作另外两平台也已登记。正文 L122 的未来重建清单仍不能替代当前各档案的状态。[Ascend README L55](https://github.com/vllm-project/vllm-ascend/blob/52d4acfa51fb868823d1070b81cbd2d97e9e4696/README.md#L55)本身还单列了 HDK 参考入口，不能把 CANN 8.5.0 当成 HDK 身份已知。
2. **DeepSeek 样板与后续特性行的归属仍需落定。** L108 已选模型族，但 L109–115 仍主要是插件全局硬件／特性概览，没有说明这些状态对所选 R1／V3.1 样板是文档条件、仅全局声明还是 unknown。例如 R1 教程给出了具体 W8A8 与节点条件，不能只用 README 的全部硬件清单替代；尚未核定的图／EP／PD 组合可以逐项保留 unknown，无需补造支持结论。
3. NVIDIA L86 的新 [disagg_prefill.md](https://github.com/vllm-project/vllm/blob/b17039bccc17b94a2ea107272ad7bc93508708df/docs/features/disagg_prefill.md)能支持 experimental、吞吐声明与 connector 示例，但它不是该句所称的“connector 注册表”，NIXL 依赖也是通过另一篇指南继续定位。应分别链接实际的 [factory.py 注册段](https://github.com/vllm-project/vllm/blob/b17039bccc17b94a2ea107272ad7bc93508708df/vllm/distributed/kv_transfer/kv_connector/factory.py#L146-L204)和 [NixlConnector 前置条件](https://github.com/vllm-project/vllm/blob/b17039bccc17b94a2ea107272ad7bc93508708df/docs/features/nixl_connector_usage.md#L5-L28)，或把本行缩到当前 URL 直接支持的范围。这是原精确引用条件尚未完成，不另计新发现。

关闭仍只要求补齐有限样板的字段和证据边界，缺证据允许 unknown；不要求选出一套真实可部署组合或开展实验。**保留 C01／P2。**

## C04（P2）— 未关闭：有限链条已补实，触发边界与来源范围尚需同步

正文 L68–69 新增的源码片段及 KV 链接基本准确，已经满足此前“不能只有枚举／接口”的实质补核要求：

- vLLM [Scheduler L351–401](https://github.com/vllm-project/vllm/blob/b17039bccc17b94a2ea107272ad7bc93508708df/vllm/v1/core/sched/scheduler.py#L351-L401)在块分配返回 None 后选择抢占对象；PRIORITY 分支按 priority／arrival_time 选取，另一分支从 running 尾部取出。随后 [_preempt_request L800–819](https://github.com/vllm-project/vllm/blob/b17039bccc17b94a2ea107272ad7bc93508708df/vllm/v1/core/sched/scheduler.py#L800-L819)释放 KV／encoder cache、置 PREEMPTED、清零计算进度并将请求放回 waiting，局部链条成立。
- MindIE [FcfsPolicy L468–510](https://github.com/Ascend/MindIE-LLM/blob/69e5a5dd4b533eaffc7e198320435350825a36f7/src/scheduler/policy/fcfs_policy.cpp#L468-L510)先选择 SWAP 或 RECOMPUTE；所选 RECOMPUTE 分支对 running sequences 设置 WAITING、调用 FreeSeq 并重置计算状态。该片段没有队列插入操作，保留“完整再入队链未核”是恰当的证据边界，不要求从枚举推断或写成 MindIE 没有再入队。
- vLLM [get_computed_blocks L164–204](https://github.com/vllm-project/vllm/blob/b17039bccc17b94a2ea107272ad7bc93508708df/vllm/v1/core/kv_cache_manager.py#L164-L204)与 [free L373–381](https://github.com/vllm-project/vllm/blob/b17039bccc17b94a2ea107272ad7bc93508708df/vllm/v1/core/kv_cache_manager.py#L373-L381)支持新增的前缀命中与释放职责说明；正文没有据此宣称两引擎缓存行为等价。

**剩余两点：**

1. L68 同段先写“allocate_slots 失败时”这一已核局部触发条件，末尾又绝对写“触发条件两侧均未核”。后一表述应限定为“完整触发条件／触发路径未全面核对；当前已核 vLLM 分配返回 None 的局部条件，MindIE 此片段只到模式选择与后处理”。无需据此比较两引擎所有“何时抢占”，也无需扩审全部算法。所谓“两侧链条完整度不同”只能表示**本次取证覆盖深度不同**，不能作为实际引擎恢复链条完整性的差异结论；当前明确保留 MindIE 未核步骤的方向应维持。
2. **来源范围没有跟随新增片段更新。** 作者来源表 L37 仍把抢占路径排除在切面之外，L44 的精确定位仍未加入 `fcfs_policy.cpp L468–510`；unknown 清单 L51／L53 继续使用“只到组件职责层”或“均为头文件／目录级取证”的旧概括。registry L6691 也尚未区分本次已核局部抢占链与未核完整算法，L6719 没有记录新增模式选择／RECOMPUTE 片段。应同步列出上述有限已核路径，并把 unknown 收窄到其外的完整触发、MindIE 再入队链等范围。这是原 C04 明确要求的来源同步，不以本报告代作者完成。

R04 已按下节关闭，预算修订不再阻碍本项。**保留 C04／P2；剩余工作是边界文字与取证记录同步，不是要求补齐 MindIE 的完整再入队实现或完成运行测试。**

## R04（P2）— CLOSED：已撤回 slot 表作为有效配额机制的依据

正文 L67、作者来源表 L44、registry L6719 已一致区分数据结构初始化与实际可达控制流：

- [构造函数 L17–31](https://github.com/Ascend/MindIE-LLM/blob/69e5a5dd4b533eaffc7e198320435350825a36f7/src/sequence/scheduling_budget.cpp#L17-L31)确实初始化 slot 表；这只证明初始化事实。
- [GetPrefillSlots L44–72](https://github.com/Ascend/MindIE-LLM/blob/69e5a5dd4b533eaffc7e198320435350825a36f7/src/sequence/scheduling_budget.cpp#L44-L72)的非 chunked 分支返回剩余预算；chunked 分支按 `prefillChunkSize` 是否非零，分别返回配置切块值或 `maxPrefillTokens`，随后读取 slot 表的动态分支不可达。
- [调用方 L100–106](https://github.com/Ascend/MindIE-LLM/blob/69e5a5dd4b533eaffc7e198320435350825a36f7/src/scheduler/policy/policy_helper.cpp#L100-L106)对待计算量、剩余 token 预算及 GetPrefillSlots 返回值取最小值。因此“配置切块＋剩余共享预算裁剪”与固定实现吻合。

三处均已删除把该 slot 表动态消费当作运行差异依据的推断；正文不可直接等价的理由也未再使用此配额机制。结论仅覆盖上述函数与调用路径，不推断全仓所有 partial prefill 门控失效。**满足 R04 关闭条件。**

## 新发现

**无须另立编号的独立新发现。** 新增 PD 引用的支持范围及抢占触发措辞问题分别归入仍开放的 C01、C04，不重复累计；R04 的修订未发现新的机制误述。

## 整体结论

**未通过第三轮定向复核。** 本轮 **R04 CLOSED；C01、C04 未关闭，保留原 P2**。C02／C03／C05／C06／C07／R01／R02／R03 沿用 CLOSED。

C01 的具体模型选择、MindIE 逐列读表与主要就近链接已补实，但各平台依赖身份与样板特性归属仍有遗漏；C04 的有限抢占／释放片段和 KV 引用已补实，但绝对化触发未知声明及来源已核／未核范围尚未同步。按上述剩余条件修订后再定向复核，不要求无关扩审或硬件实验。

正文继续保持 `draft / source_checked` 的来源核对边界；本结论不建立 MindIE latest 的同版关系，也不证明任何 NVIDIA／AMD／Ascend 部署组合的硬件功能交集。

临时副本的结构检查与构建均通过，不改变上述技术审阅结论。对本轮开始时记录的 552 个既有文件逐一复核摘要，未发现变化；本轮唯一仓库新增文件为本报告。
