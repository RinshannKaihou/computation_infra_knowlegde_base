# 第四批独立验证审阅

审阅日期：2026-09-30。审阅者：独立 `gpt-6-astra / xhigh`。范围为 F13、F14、F15、F16，以及第四批来源记录、registry、相关导航和获取计划。以下行号是审阅时定位，修订后以所引语句和章节为准。

**初审结论：需要修订后定向复核。发现 0 项 P1、2 项 P2、2 项 P3。** 两项 P2 分别涉及 DCP 默认 planner 的写入者与去重语义，以及 vLLM 服务端 TTFT/E2E 的计时边界。没有发现把草稿标成实测、拼接 GPU/NPU 支持组合、伪造恢复实验或性能数值的情况。

本次只新增本报告，未修改正文、来源登记、计划或导航；未运行 `make`、上游代码、安装、服务、训练、推理或硬件实验。外部证据通过官方版本化页面与固定 commit 的原始文件只读核对，源码行号由原始文件实际计数。它是技术来源审阅，不能提升为 `reproduced`。

## R1 — P2：DCP 非 tensor 状态不保证由协调 rank 保存，同名 rank-local 状态可能被去重

**定位：** [F14 状态覆盖与截取一致性](../../knowledge/06-training/checkpoint-state-consistency.md)，初审第 66 行，“非 tensor 对象由协调 rank 保存”。相关影响包括 F13/F14 对 RNG、数据游标和其他 rank-local 应用状态的保存责任解释。

**证据：** 固定 PyTorch v2.6.0 commit `1eba9b3aa3c43f86f4a2c807ac8e12c4a7767340` 的文档字符串与实际默认实现存在冲突：

- [`default_planner.py` 390–414](https://github.com/pytorch/pytorch/blob/1eba9b3aa3c43f86f4a2c807ac8e12c4a7767340/torch/distributed/checkpoint/default_planner.py#L390-L414) 的 docstring 仍称非协调 rank 不写普通 tensor/非 tensor；实际循环却为所有 rank 的普通 tensor 和非 tensor 生成写入项，`is_coordinator` 不参与该分支判断。
- [`DefaultSavePlanner` 69–85、100–113](https://github.com/pytorch/pytorch/blob/1eba9b3aa3c43f86f4a2c807ac8e12c4a7767340/torch/distributed/checkpoint/default_planner.py#L69-L113) 的默认 `dedup_save_to_lowest_rank=False`，全局计划调用 `dedup_save_plans`；`dedup_replicated_tensors` 参数在该版本已经无效。
- [`_dedup_save_plans.py` 15–58](https://github.com/pytorch/pytorch/blob/1eba9b3aa3c43f86f4a2c807ac8e12c4a7767340/torch/distributed/checkpoint/_dedup_save_plans.py#L15-L58) 按相同 `MetadataIndex` 归组，只为其中一个候选 plan 保留写入项。默认按照计划存储量选择；显式选项才改为最低候选 rank。这个过程没有比较各 rank 的对象内容是否相同。
- 非 tensor 的写入 index 是 `MetadataIndex(fqn)`，没有自动附加 rank 身份，见 [`planner_helpers.py` 116–120](https://github.com/pytorch/pytorch/blob/1eba9b3aa3c43f86f4a2c807ac8e12c4a7767340/torch/distributed/checkpoint/planner_helpers.py#L116-L120) 与 [221–233](https://github.com/pytorch/pytorch/blob/1eba9b3aa3c43f86f4a2c807ac8e12c4a7767340/torch/distributed/checkpoint/planner_helpers.py#L221-L233)。

**影响：** 现有句子把“协调 rank 规划”误写成“协调 rank 保存全部非 tensor”。读者还可能把“每 rank 都显式传入 RNG/游标”理解为每份都会保留；在默认 planner 下，同名 index 的不同 rank-local 值可能只保留一份。这直接影响恢复状态完整性。

**建议修正：** 明确默认 planner 先收集各 rank 写入项，再按 metadata identity 去重并分配写入者，不能固定为协调 rank。单独指出：应用需要为 rank-local 状态设计不冲突的逻辑身份、可验证的聚合表示或自定义保存方案，并验证恢复映射；不能只给每个 rank 放置相同 key。记录上游 docstring 与固定实现不一致，避免继续把旧 docstring 当实际行为。本结论来自源码推理，未进行多进程保存实验，不提供未经验证的实现处方。

## R2 — P2：服务端计时图混淆 HTTP 入口、engine frontend arrival 与输出接收时间

**定位：** [F16 客户端和服务端时间线及固定服务端 TTFT](../../knowledge/07-inference/latency-metrics.md)，初审第 29、54–66、71、79–81 行；[推理侧来源记录](batch-04-inference-sources.md)中服务端术语边界和 F16 指标骨架也沿用“frontend arrival→engine 首次 output”的简写。

正文的详细公式已接近实现，但图把“请求到达 server frontend”之后的校验/tokenize 一并放入服务端窗口，文字又把终点简化为引擎产出。这两个边界都需要收窄。

**起点证据：** 固定 vLLM commit `b17039bccc17b94a2ea107272ad7bc93508708df` 的常规 OpenAI chat 路径先调用 [`_preprocess_chat`，`serving_chat.py` 300–327](https://github.com/vllm-project/vllm/blob/b17039bccc17b94a2ea107272ad7bc93508708df/vllm/entrypoints/openai/serving_chat.py#L300-L327)。其中 chat template 和 tokenizer 处理在 [`serving_engine.py` 1209–1275](https://github.com/vllm-project/vllm/blob/b17039bccc17b94a2ea107272ad7bc93508708df/vllm/entrypoints/openai/serving_engine.py#L1209-L1275) 可直接定位。随后才在 [`serving_chat.py` 407–428](https://github.com/vllm-project/vllm/blob/b17039bccc17b94a2ea107272ad7bc93508708df/vllm/entrypoints/openai/serving_chat.py#L407-L428) 调用 `_process_inputs`。该 helper 调用 `InputProcessor.process_inputs` 时没有传入 `arrival_time`，见 [`serving_engine.py` 1293–1320](https://github.com/vllm-project/vllm/blob/b17039bccc17b94a2ea107272ad7bc93508708df/vllm/entrypoints/openai/serving_engine.py#L1293-L1320)；因此走 [`input_processor.py` 470–471](https://github.com/vllm-project/vllm/blob/b17039bccc17b94a2ea107272ad7bc93508708df/vllm/v1/engine/input_processor.py#L470-L471) 的 `time.time()` 默认起点。completion 同样先 render prompt，后创建 engine request，见 [`serving_completion.py` 127–140](https://github.com/vllm-project/vllm/blob/b17039bccc17b94a2ea107272ad7bc93508708df/vllm/entrypoints/openai/serving_completion.py#L127-L140) 和 [227–247](https://github.com/vllm-project/vllm/blob/b17039bccc17b94a2ea107272ad7bc93508708df/vllm/entrypoints/openai/serving_completion.py#L227-L247)。

所以这里的 engine frontend arrival 不是 HTTP 收到请求的时刻，默认窗口不包含此前已经完成的 HTTP 校验、chat template/tokenization 等工作。其他调用路径可显式传入 arrival，不能反向概括为任何路径都排除所有预处理。

**终点与时钟证据：** [`IterationStats.__init__`，`stats.py` 233–237](https://github.com/vllm-project/vllm/blob/b17039bccc17b94a2ea107272ad7bc93508708df/vllm/v1/metrics/stats.py#L233-L237) 使用 frontend 的 `time.time()`。在 [`AsyncLLM.output_handler` 498–519](https://github.com/vllm-project/vllm/blob/b17039bccc17b94a2ea107272ad7bc93508708df/vllm/v1/engine/async_llm.py#L498-L519) 中，先 `await engine_core.get_output_async()`，随后创建该 iteration stats。TTFT 使用这个 wall-clock 减 `arrival_time`，而 ITL/phase intervals 使用独立的 engine-core timestamp，见 [`stats.py` 252–305](https://github.com/vllm-project/vllm/blob/b17039bccc17b94a2ea107272ad7bc93508708df/vllm/v1/metrics/stats.py#L252-L305)。[`EngineCoreOutputs` 191–193](https://github.com/vllm-project/vllm/blob/b17039bccc17b94a2ea107272ad7bc93508708df/vllm/v1/engine/__init__.py#L191-L193) 的默认 timestamp 则来自 `time.monotonic()`。E2E 同样取 iteration wall-clock 减 arrival，见 [`stats.py` 331–350](https://github.com/vllm-project/vllm/blob/b17039bccc17b94a2ea107272ad7bc93508708df/vllm/v1/metrics/stats.py#L331-L350)。

**影响：** 现有图可能让人以为服务端 TTFT 覆盖整个 HTTP frontend 预处理，或者排除 engine→frontend 返回与调度等待，从而把实际 frontend 瓶颈归到网络、排队或 prefill。正文已有“不能直接相减得到网络延迟”的限制，但没有消除计时边界本身的错误示意。

**建议修正：** 图中拆出 HTTP serving frontend 和 engine frontend/统计器，或明确标注 HTTP 预处理后才设置默认 engine arrival；把 TTFT 终点写成“frontend 收到首批相关 engine outputs 后创建的 iteration timestamp”。同时列出 TTFT/E2E 的 wall-clock 与 ITL、queue/prefill/decode/inference 的 engine-core monotonic 时间源；E2E 同样沿用修正后的起点。保留显式 arrival override 与不同入口需单独追踪的边界。同步修改研究记录和附近引用，补上当前引用未覆盖的 `stats.py` 233–237 以及实际入口调用链。

## R3 — P3：Ascend 版本数值的来源归属和兼容性措辞需准确

**定位：** [来源登记](../../sources/registry.yaml)中 `src.ascend.vllm-ascend-v0-14-0rc1` 的 notes，初审第 527 行；[推理来源记录](batch-04-inference-sources.md)初审第 122、190 行。

**证据：** 固定 [`conf.py` 63–80](https://github.com/vllm-project/vllm-ascend/blob/52d4acfa51fb868823d1070b81cbd2d97e9e4696/docs/source/conf.py#L63-L80) 确实定义 vLLM 0.14.1、插件 0.14.0rc1 和 CANN image tag，但没有 PyTorch/torch-npu 2.9.0 的 substitution；这两项来自 [`README.md` 49–57](https://github.com/vllm-project/vllm-ascend/blob/52d4acfa51fb868823d1070b81cbd2d97e9e4696/README.md#L49-L57)。固定 [`versioning_policy.md` 24–27](https://github.com/vllm-project/vllm-ascend/blob/52d4acfa51fb868823d1070b81cbd2d97e9e4696/docs/source/community/versioning_policy.md#L24-L27) 还包含已记录的插件版本标注冲突，并在对应行同时列出上游 0.14.0/0.14.1。

**影响：** registry 的“固定 conf.py 将其文档栈替换为……PyTorch/torch-npu 2.9.0”归错了证据来源。研究记录的“它与主样板 vLLM 0.14.0 不配套”又把未建立配套证明写成了排除兼容性的结论；当前正文的“未安装或配套验证”更准确。

**建议修正：** notes 分别标明 conf substitutions 与 README requirements。将研究记录改为“该文档构建变量指向 0.14.1，且其他固定页面存在冲突，本轮不能据此确认与主样板 0.14.0 的配套”，保留 unknown；不需要改变现有 RC、硬件与 310P 限制。

## R4 — P3：来源获取计划仍将第四批已核对的目标写成未执行

**定位：** [来源获取工作包](../../plans/source-acquisition.yaml)，A11 `progress_notes`（初审附近第 277 行）与 A19 文档构建配置目标（初审附近第 474、482 行）。

**证据与影响：** A11 的 selected revision 已扩展为 KV、metrics、bench serve，但 progress_notes 仍说只为 F05 核对 plugin，执行/指标等目标尚未执行，与本批来源记录和 F15/F16 的 `source_checked` 不一致。A19 仍把展开文档宏限定为 `mkdocs.yml`，本次实际采用并核验的是 Sphinx `docs/source/conf.py`。后续按获取计划推进时，容易重复已完成的来源工作或寻找错误构建配置。

**建议修正：** 更新为“第四批已只读核对执行/KV、指标与 benchmark 源码；负载实验、真实服务与硬件验证未执行”，无需将整个 A11 标为完成；A19 将配置定位改为实际 Sphinx conf 或“所选版本实际文档构建配置”。A10 也可一并补充第四批训练状态与恢复资料的已读范围。保留工作包未完成部分。

## 抽查确认和未列为缺陷的事项

| 范围 | 实际核对 | 结论 |
|---|---|---|
| F13 并行责任 | PyTorch 2.6 FSDP `FULL_SHARD`、TP 1-D DeviceMesh、PP alpha；固定 DDP docstring 与 GradScaler 599–624 | 参数/梯度/optimizer 分片、输入切分责任和 scaler 在 `update()` 后截取的描述有依据；mid-step 与 DataLoader 精确恢复保留未知是合理的 |
| F14 API/重分片 | DCP 2.6 save/load、Stateful、canonical FQN、`set_state_dict` 和 `broadcast_from_rank0` 条件 | 目标对象预分配、FQN、DTensor 与 legacy ShardedTensor 限制、跨版本不保证兼容已保留；API 返回不能替代训练语义验证。R1 是默认 planner 的具体错误 |
| MindSpeed | 固定 HA 文档 5–84，checkpoint wrapper 168–279、外部 import 21–33，README 60–96 | DP 粒度与缩扩次数限制、异步仅 distributed `torch_dist`、同步 barrier 与异步 finalize 位置符合来源；没有从 wrapper 虚构外部 Megatron schema/load 保证 |
| F15 KV 与抢占 | 固定 prefix caching 文档 5–26、136–150、193–203；optimization 10–48 | 完整 block、父 hash/额外隔离、touch/free/evict、默认 RECOMPUTE 和 chunked-prefill “whenever possible”均有对应内容；未把调优示例值写成通用阈值 |
| F16 客户端 | 固定 endpoint 179–248、312–369；serve 415–470、550–583、617–712、762–841 和 CLI 默认/转发 | completion/chat 成功和 E2E 差异、成功过滤、TPOT 0/1 token、ITL 扁平样本、SLO 的 AND 条件、throughput 主窗口、ready=0/warmup=0 默认均有依据 |
| F16 服务端 | 固定 stats 193–377、loggers 498–515、573–616、683–885、1109–1163，output_processor 393–456、693–714 | request TPOT 与 ITL 区分、错误/取消分类和取消覆盖未知保留正确；R2 需要修正计时边界，而非把现有公式替换为跨时钟相减 |
| Prometheus | 官方 histogram 页面与 `histogram_quantile` current 页面于本次复读 | classic buckets 先 rate、保留 le 聚合后取 quantile、插值和不可平均分位数有依据；动态来源限制继续保留 |
| Ascend 支持 | 固定 feature matrix 7–33、README 49–57、release notes 3–12、conf 63–80、version policy 24–27 | Functional 状态未被外推到全部模型/硬件；310P basic dense/VL 与 eager 限制有来源；版本内部冲突已记录，需按 R3 收窄研究记录措辞 |
| 许可 | MindSpeed 根 LICENSE 与 checkpointing 文件头；vLLM/Ascend 根 LICENSE、pyproject 17–20、setup 475–492 | 文档/独立代码头/源码包元数据/未读制品范围已拆分；未借仓库许可概括未知 wheel、容器或外链材料 |
| 元数据与导航 | 四正文、章节/平台/任务入口、backlog 和 source audit | 四篇保留 draft/source_checked；单一主归属和相互引用合理。尚未有实验、网站/API 或诊断处方的边界未被夸大 |

表中不代表全量兼容性审查，也不表示所有分支已追踪。未知的目标模型、外部依赖、rank-local 恢复设计、取消覆盖和真实 GPU/NPU 行为未因本次审阅自动解决。

## 定向复核入口

修订后重点复核：R1 是否写明文档/实现冲突和 rank-local 去重风险；R2 的图、正文、来源表是否统一为实际入口及两类时间源；R3 是否恢复为可追溯且不排除未知组合的表述；R4 是否清楚区分来源阅读完成与实测未执行。修订和结构检查由主任务完成，本报告不以结构检查通过替代上述语义复核。

## 修订后定向复核（2026-09-30）

**复核结论：R1–R4 全部闭合；本次修订范围内未发现新增 P1/P2/P3 问题。第四批来源审阅通过。** 本结论针对初审发现及相关同步改动，保留上方初审记录，不代表实际恢复、性能或硬件兼容性得到验证。

| 发现 | 复核结果与闭合依据 |
|---|---|
| R1 — P2 | 已闭合。F14 和训练来源记录均改为各 rank 生成写入项、按 `MetadataIndex` 去重并选择写入者；明确默认行为与旧 docstring 冲突、非 tensor FQN 不自动带 rank、同 key 不保证保存所有 rank-local 值。固定实现、去重函数及 index 构造引用与初审实际核对的源码位置一致；保留“源码推理、尚未多进程实验”的边界。 |
| R2 — P2 | 已闭合。F16 图区分 HTTP serving frontend、engine frontend/stats 与 engine core；文字明确常规 chat/completion 预处理后设置默认 arrival，允许其他入口显式覆盖。TTFT/E2E 终点改为 frontend 接收相关 outputs 后的 iteration wall-clock，并与 engine-core monotonic 及客户端 `perf_counter()` 分开。研究记录的术语、指标骨架和补查链接已同步，未再把默认窗口等同 HTTP 接收至 core 产出。 |
| R3 — P3 | 已闭合。registry 与研究记录的 YAML notes 将 conf substitutions 和 README 的 PyTorch/torch-npu requirements 分开；研究记录把上游 0.14.0 配套保留为未知，移除了无依据的排除兼容性结论。固定 version policy 的内部冲突仍保留。 |
| R4 — P3 | 已闭合。A10/A11 记录第四批已完成的来源阅读和源码核对，同时保留本地训练、推理、负载和 GPU/NPU 验证未执行；A19 改为所选版本实际构建配置，并明确本批为 Sphinx `docs/source/conf.py`。未将整个获取工作包误标完成。 |

另定向检查了第五批 [F02 推理端到端总览](../../knowledge/00-overview/inference-lifecycle.md) 的计时图及相关两段文字：默认 arrival、输出接收后的 iteration 终点、三类时钟及显式 arrival 例外已与 F16 一致，没有继续继承 R2。此次未全面审阅第五批，也不代替第五批独立轮末审阅。

本次仅追加本报告；复核以已逐行读取的固定外部证据和修订后的文件为依据，没有重跑全量来源审查、`make check`、`make build` 或任何上游代码/硬件实验。主任务报告的 33 entries / 51 sources 结构检查通过属于独立的结构验证，未用作四项技术发现闭合的证明。正文继续保持 `draft` / `source_checked`。
