# Batch 26 T07-01 独立审阅报告

## 审阅头部

- 审阅角色：与正文作者独立的知识库批次审阅者；本轮只审阅，不代作者修订正文、来源登记或计划。
- 审阅模型／推理档位：`gpt-6.1-sol / xhigh`。已核验本次本地 Codex CLI 会话的 `turn_context.model` 为 `gpt-6.1-sol`、`turn_context.effort` 为 `xhigh`；未见模型回退标记，未派发其他模型或子代理。
- 审阅日期：2026-10-20（Asia/Shanghai）。
- 验收基准：`plans/full-coverage-backlog.yaml:6215` 的 T07-01，逐项核对其五条 acceptance；编写与取证口径按 `docs/authoring-guide.md` 第 3–7 节。
- 审阅对象：
  1. `knowledge/07-inference/model-loading-and-readiness.md`：新增 procedure 全文及 frontmatter。
  2. `knowledge/07-inference/index.md`：仅新增正文条目描述、07.1 主题行及相应链接／ID，不扩展审阅其他主题。
  3. `sources/registry.yaml`：仅 `src.vllm.model-loader-v0-14`、`src.vllm.tokenizer-registry-v0-14`、`src.vllm.readiness-health-v0-14`、`src.vllm.rocm-install-doc-v0-14`、`src.ascend.mindie-llm-doc-latest`、`src.ascend.mindie-llm-repo-69e5a5dd` 六条新增登记的许可、notes 与正文对应关系。
  4. `docs/research/batch-26-t07-01-sources.md`：摘要、主张—来源定位表及 unknown 清单。

### 取证方式与限制

1. 重新打开精确上游 URL，而非只接受作者笔记：vLLM 固定 commit `b17039bccc17b94a2ea107272ad7bc93508708df` 的 16 个已登记源码文件；另补开 OpenAI 服务启动入口、GPU worker／内存检查、EngineCore、Llama 实现、分片保存／加载示例和平台接口。重新打开 v0.14.0 GPU 安装页、features 页、插件文档，以及 MindIE 文档站的两个指定 latest 页面、固定 commit README／LICENSE、safetensors v0.7.0 README。来源正文通过网页读取工具及 GitHub 文件读取工具取得；本地 `curl` 因 DNS 解析失败，未将该失败冒充取证成功。
2. vLLM tag 的 GitHub ref API 返回 v0.14.0 → 上述完整 commit。MindIE 固定 README 的配套表及文档入口已核对；不把开源仓 README 的版本表当作 latest 页与某一产品包已经同版的证明。本轮没有独立穷举 MindIE 所有 release/tag；作者关于“无 release tag”的历史性表述不作为兼容或定版依据。
3. SHA-256 核验分清两种证据：对本机可读的作者暂存包／原文件／HTML，复算取回表中全部 23 项已有摘要，前 16 位均一致；其中 vLLM 的 16 个文件另直接从 tar 成员字节复算。新开 GitHub 所得 blob SHA 与本地原文件对照抽查 `base_loader.py`、`default_loader.py`、两个 `registry.py`、MindIE README／LICENSE，六项一致。HTML 摘要一致仅证明原作者快照与记录相符，不等于本次网页渲染返回了相同原始 HTML 字节。features 页本来没有字节快照，未为其补造摘要。
4. 源码坐标使用固定快照原文件的 1-based 行号，并以 GitHub 原文件／blob 交叉抽查；网页工具的显示行号没有直接转成 GitHub 行锚点。作者所列 `default_loader.py:131`、`utils.py:181`、`tokenizers/registry.py:145`、`async_llm.py:727` 等定位均能在原文件落到相应代码，不因渲染坐标偏移报错。
5. 未运行任何 vLLM／MindIE 启动、加载、health、推理或清理操作；没有硬件验证，也没有把源码核对称为实测。保留进入本轮前工作区所有已修改／未跟踪文件。

## 发现列表

以下 11 项均为开放发现：P1 0 项、P2 10 项、P3 1 项。每项须由作者修订，再由独立审阅者定向复核；本报告不宣告任何问题已经关闭。

### T07-01-C01 — P2：load-format 摘要与实际分派、选择条件不一致

- 受影响位置：`knowledge/07-inference/model-loading-and-readiness.md:98`；`sources/registry.yaml:6571`；`docs/research/batch-26-t07-01-sources.md:46`。
- 发现：14 个内置名称的计数正确，但默认 loader 实际对应 7 个名称，不是正文的 8 个；`dummy` 有独立 loader，`runai_streamer_sharded` 映射 `ShardedStateLoader`，正文专用分派说明漏掉了这些区别。`auto` 也不是无条件等同 `hf`：发现 `consolidated*.safetensors` 时先选择 `mistral`。此外，未注册名称的拒绝点是 loader 查询，不能写成“配置校验即报 ValueError”；配置接受字符串并进行小写归一，以允许自定义注册。
- 重开证据：[model_loader/__init__.py 原文件 L31–61、L118–123](https://github.com/vllm-project/vllm/blob/b17039bccc17b94a2ea107272ad7bc93508708df/vllm/model_executor/model_loader/__init__.py#L31-L61)、[default_loader.py L100–137](https://github.com/vllm-project/vllm/blob/b17039bccc17b94a2ea107272ad7bc93508708df/vllm/model_executor/model_loader/default_loader.py#L100-L137)、[config/load.py 的 load_format 字段及 L110–112](https://github.com/vllm-project/vllm/blob/b17039bccc17b94a2ea107272ad7bc93508708df/vllm/config/load.py#L110-L112)。默认文件选择还受 `fall_back_to_pt`、`allow_patterns_overrides` 约束，不能把基础匹配模式写成所有模型的最终全集。
- 关闭条件：给出正确的内置名称—loader 对照，补齐 `auto` 的 Mistral 分支与覆盖条件，区分配置归一和未注册 loader 拒绝；同步修订正文、登记 notes、来源表，不将“14 个内置名称”写成不允许插件扩展的封闭全集。

### T07-01-C02 — P2：自动选择 Mistral tokenizer 遗漏模型文件条件

- 受影响位置：`knowledge/07-inference/model-loading-and-readiness.md:118`；`sources/registry.yaml:6585`；`docs/research/batch-26-t07-01-sources.md:52`。
- 发现：安装 `mistral_common` 并不足以使 `auto` 自动切为 Mistral。还须在当前 tokenizer 名称／revision 对应文件中匹配 `tekken.json` 或 `tokenizer.model.v*`。遗漏条件会让普通 HF tokenizer 的身份判断出错。缓存说明也应限定于缓存包装入口，不能把直接调用 `get_tokenizer` 与 `cached_get_tokenizer` 当成相同对象复用契约。
- 重开证据：[tokenizers/registry.py L145–153](https://github.com/vllm-project/vllm/blob/b17039bccc17b94a2ea107272ad7bc93508708df/vllm/tokenizers/registry.py#L145-L153) 明确检查文件匹配；同一原文件 L190–237 区分直接构造和缓存包装。
- 关闭条件：三处均补全模式、依赖、文件及 revision 条件，并明确对象缓存发生在哪个入口；不能据此把所有模型改用 Mistral tokenizer。

### T07-01-C03 — P2：五阶段叙述漏掉权重前的设备、dtype 与内存失败边界

- 受影响位置：`knowledge/07-inference/model-loading-and-readiness.md:61`、`:65`、`:68`、`:77`、`:124`。
- 发现：表格及其“启动序列”叙述把设备内存／初始化统一放在 S3 权重装载后的 S4，容易把装载前失败误分为装载后 profiling。固定上游在 worker 设备初始化时已检查 dtype、初始化通信并检查启动空闲显存。S1 的“早于任何解析”同样不能作为两条引擎线共有的严格时序保证。后文链接的既有 OOM 文本虽然保留了权重前检查，但不消除本页主序列的遗漏。
- 重开证据：[gpu_worker.py L208–234](https://github.com/vllm-project/vllm/blob/b17039bccc17b94a2ea107272ad7bc93508708df/vllm/v1/worker/gpu_worker.py#L208-L234)、[worker/utils.py L253–273](https://github.com/vllm-project/vllm/blob/b17039bccc17b94a2ea107272ad7bc93508708df/vllm/v1/worker/utils.py#L253-L273)；同一 worker 的 `load_model` 从 L269 开始，`determine_available_memory` 从 L283 开始，分别是后续权重与 profiling 入口。
- 关闭条件：区分“诊断分类”与“真实调用时序”，显式列出装载前设备／通信／dtype／空闲内存检查，以及装载后 profiling、KV 分配与 warmup；首失败分类能够接住前一种失败，不假定所有引擎按相同五步串行执行。

### T07-01-C04 — P2：由 health 函数检查项直接推导启动可见性，缺少入口前置条件

- 受影响位置：`knowledge/07-inference/model-loading-and-readiness.md:78`；`sources/registry.yaml:6599`；`docs/research/batch-26-t07-01-sources.md:53`。
- 发现：`check_health()` 不主动执行模型请求这一点正确，但“进程与引擎循环存活即可 200，不代表启动序列完成”忽略了标准服务入口先创建引擎、初始化应用，再提供 HTTP 服务的前置条件。仅看 health handler 不能据此说明标准入口在初始加载未完成时就能返回 200。应区别“函数没有重跑加载／warmup”“启动时何时可访问”“首请求和输出质量没有被探测”三种命题。
- 重开证据：[OpenAI api_server.py L1338–1353](https://github.com/vllm-project/vllm/blob/b17039bccc17b94a2ea107272ad7bc93508708df/vllm/entrypoints/openai/api_server.py#L1338-L1353)、[async_llm.py L727–730](https://github.com/vllm-project/vllm/blob/b17039bccc17b94a2ea107272ad7bc93508708df/vllm/v1/engine/async_llm.py#L727-L730)、[health.py](https://github.com/vllm-project/vllm/blob/b17039bccc17b94a2ea107272ad7bc93508708df/vllm/entrypoints/serve/instrumentator/health.py)。补开标准入口是本次独立核查，而不是作者此前“未重开”记录中的证据。
- 关闭条件：补充标准入口的初始化先后和适用范围；保留“200 不足以证明实际请求及质量”的正确边界，撤回未被入口调用链支持的初始启动推断；若要描述其他入口／生命周期例外，须分别定位，不混用 legacy、gRPC 与 OpenAI 服务。

### T07-01-C05 — P2：格式章节没有完成 TP／PP 与 dtype 条件的解释

- 受影响位置：`knowledge/07-inference/model-loading-and-readiness.md:94`、`:100`、`:117`、`:131`；对应 acceptance 第 2 条。
- 发现：目前只有文件名模式、跨 TP／PP 重分片 unknown 和“引擎×模型×硬件”原则；没有解释普通模型权重的参数映射／TP 分片／PP 层归属与预分片 `sharded_state` 的区别，也没有把文件记录的 dtype、实际加载 dtype 与硬件支持检查分开。保留跨并行重分片 unknown 是正确的，但不能替代验收要求中的已知机制解释。
- 重开证据：[sharded_state_loader.py L109–162](https://github.com/vllm-project/vllm/blob/b17039bccc17b94a2ea107272ad7bc93508708df/vllm/model_executor/model_loader/sharded_state_loader.py#L109-L162) 按 TP rank 找既有分片并向当前参数复制；[Llama 实现 L461–521](https://github.com/vllm-project/vllm/blob/b17039bccc17b94a2ea107272ad7bc93508708df/vllm/model_executor/models/llama.py#L461-L521) 展示 packed 参数映射、模型专用 `weight_loader` 与 PP 缺失层跳过；[base_loader.py L47–61](https://github.com/vllm-project/vllm/blob/b17039bccc17b94a2ea107272ad7bc93508708df/vllm/model_executor/model_loader/base_loader.py#L47-L61) 使用 `model_config.dtype`，硬件检查另见 C03。
- 关闭条件：以明确模型实现为限定，补足上述区别与保存／加载并行配置记录要求；说明量化方法／打包参数依赖专用 loader，不把 Llama 例子或任一 dtype 规则外推全平台。未证实的跨 TP／PP 重分片能力继续保持 unknown。

### T07-01-C06 — P2：模型身份固定仍可不记录权重、config 与 tokenizer 内容摘要

- 受影响位置：`knowledge/07-inference/model-loading-and-readiness.md:116`、`:118`、`:142`、`:166`；对应 acceptance 第 3 条。
- 发现：目录内容只要求文件清单／大小，把哈希放在“必要时”；tokenizer 则仅写“文件身份”，没有明确定义不可变 revision 或内容摘要。这样两个同名同大小、参数 key／shape 相同而数值不同的目录仍可被记为相同身份，达不到以模型／文件摘要固定身份的验收目标。
- 重开证据：[safetensors v0.7.0 README 的 Format 节](https://github.com/safetensors/safetensors/blob/v0.7.0/README.md#format) 说明容器布局及不检查张量数值的限制，并未提供权重内容校验和；[default_loader.py L100–184](https://github.com/vllm-project/vllm/blob/b17039bccc17b94a2ea107272ad7bc93508708df/vllm/model_executor/model_loader/default_loader.py#L100-L184) 的文件选择不能代替制品内容身份。这里的风险判断是对验收要求和现有记录字段的推论，不是声称上游自动计算摘要。
- 关闭条件：身份记录必须含实际选用权重分片、索引、config、tokenizer／模板等输入的内容摘要或可追溯不可变制品身份，并记录算法／覆盖范围；无法取得时显式记缺口，不能达到“身份已固定”的完成判据。无需虚构现场哈希结果或命令。

### T07-01-C07 — P2：输出质量判据允许用 tokenizer 自洽替代模型质量

- 受影响位置：`knowledge/07-inference/model-loading-and-readiness.md:138`、`:145`、`:149`、`:166`；对应 acceptance 第 5 条。
- 发现：“与已知参考输出或 tokenizer 重编码一致性比对”把两种不等价验证用“或”连接。错误权重产生的可编码文本也可能满足 tokenizer 自洽，不能因此认定模型输出质量正确。此外，当前小模型计划未落到具体确定输入、参考来源与比较阈值，只要求未来固定它们，尚不足以判定一次验证通过。
- 重开证据：[tokenizers/registry.py L190–237](https://github.com/vllm-project/vllm/blob/b17039bccc17b94a2ea107272ad7bc93508708df/vllm/tokenizers/registry.py#L190-L237) 是 tokenizer 构造／缓存路径，不是模型输出评估；[MindIE 快速入门的“发送请求”“精度测试”两节](https://mindie-llm-doc.readthedocs.io/zh-cn/latest/user_guide/quick_start/quick_start/) 将服务请求和任务评估分列。正文已经链接的本库 `knowledge/07-inference/quantization-and-quality.md:58` 也要求固定任务、指标、baseline 与样本量。两种验证不等价的结论属于审阅推理。
- 关闭条件：把 tokenizer 一致性降为独立的输入输出管线检查；质量必须使用明确参考／任务与阈值，不能单靠自洽通过。为三平台计划列出可记录的模型选择、确定输入、采样／模板、参考和判定字段；未选定或未取得参考时标为计划缺口，不伪造参考输出，也不要求跨硬件逐 token 完全相同。

### T07-01-C08 — P2：共享内存清理缺少对象范围与隔离前提

- 受影响位置：`knowledge/07-inference/model-loading-and-readiness.md:85`、`:146`、`:161`、`:162`；`sources/registry.yaml:6627`；`docs/research/batch-26-t07-01-sources.md:62`。
- 发现：正文从文档示例提炼出“须清理 `/dev/shm/*`”，却未限定到哪个容器／IPC 命名空间、哪些已退出实例的对象，也未要求确认无其他服务引用。末尾“不涉及对其他租户”的总声明不能保证这项清理确实只影响本服务。这里没有认定作者伪造上游命令；问题是把危险示例推广为泛化恢复步骤。
- 重开证据：[MindIE 快速入门的“容器部署”“启动服务”及启动注意事项](https://mindie-llm-doc.readthedocs.io/zh-cn/latest/user_guide/quick_start/quick_start/) 确实有切换用户后的宽泛清理示例，但其上下文是具体部署过程，并不证明任意现场共享内存均可删除。跨 IPC 范围的误用风险是本次依据操作边界作出的安全审阅判断。
- 关闭条件：明确清理是有状态变更，不是只读诊断；须确认服务停妥、目标命名空间与归属、无其他消费者及已有授权，仅处理已经识别的本实例遗留对象。来源记录可保留上游示例并标危险边界，不能把通配删除作为未限定环境的通用处方。

### T07-01-C09 — P2：ROCm 硬件列表漏掉 Ryzen AI 的最低版本例外

- 受影响位置：`knowledge/07-inference/model-loading-and-readiness.md:88`。
- 发现：正文列出通用 ROCm 6.3+、MI350 的 7.0+ 例外和 Ryzen AI gfx1151／1150，却遗漏 Ryzen AI MAX／AI 300 的 ROCm 7.0.2+ 条件。来源登记与作者来源表已经保留该条件，属于正文压缩时丢失限制，不是待确认信息。
- 重开证据：[vLLM v0.14.0 GPU 安装页，AMD ROCm 的 Requirements](https://docs.vllm.ai/en/v0.14.0/getting_started/installation/gpu/#requirements) 将 MI350 与 Ryzen AI 的额外版本下限分别列出；同页 Build wheel from source 和 features 矩阵不能冲销这个要求。
- 关闭条件：在正文硬件／版本说明附近补回 Ryzen AI 对应的 7.0.2+ 下限，或收窄硬件列表；继续保留“安装条件不证明格式／量化支持”的限制。

### T07-01-C10 — P2：MindIE 字段要求和成功日志被扩张为未经取证的必要条件／错误时点

- 受影响位置：`knowledge/07-inference/model-loading-and-readiness.md:83`、`:134`。
- 发现：快速入门只明确要求路径及 `torch_dtype`／`vocab_size` 字段存在，没有证明这些值与权重不符一定“在装载前暴露”。另把成功日志写成“未达 `Daemon start success!` 即无服务”，是把充分的观察标志倒推为必要条件；日志缺失、未采集与服务确实未就绪必须区分。
- 重开证据：[MindIE 快速入门，配置服务化参数表的 modelWeightPath 行与“启动服务”节](https://mindie-llm-doc.readthedocs.io/zh-cn/latest/user_guide/quick_start/quick_start/)：前者要求路径／字段存在，后者说明看到该日志表示启动成功，并另给请求验证；没有提供正文新增的全部失败时点和逆命题。
- 关闭条件：将字段一致性失败发生阶段保留为需日志／实现确认，不由字段表外推出装载前检查；未观察到成功日志时只写“就绪尚未证实”，结合实际请求和日志完整性判断，不能直接断言没有服务。

### T07-01-C11 — P3：MindIE 仓库许可 scope 与文档另行声明不够一致

- 受影响位置：`sources/registry.yaml:6624`、`:6637`。
- 发现：固定仓条目将 scope 写为“仓库源码与文档”并统一标 `MulanPSL-2.0`，但 notes 又识别 README 的文档 CC BY-SA 4.0 声明；对结构化 scope 的读取者仍可能得到过宽的文档许可结论。文档站条目的许可 URL 还使用可变 master，而本轮已取得可固定的 README。没有发现正文实际批量搬运外部材料，本项是登记精度问题，不作法律适用裁定。
- 重开证据：[MindIE 固定 LICENSE.md](https://github.com/Ascend/MindIE-LLM/blob/69e5a5dd4b533eaffc7e198320435350825a36f7/LICENSE.md) 为 MulanPSL 第 2 版；[同一 commit README L99–103](https://github.com/Ascend/MindIE-LLM/blob/69e5a5dd4b533eaffc7e198320435350825a36f7/README.md#L99-L103) 对文档另有 CC BY-SA 4.0 声明。README 对“本文档”的声明也不能自动解决站点所有页面／第三方材料的许可范围。
- 关闭条件：在 scope 层明确排除另有声明的文档／第三方内容，或拆列许可范围并保留未核实边界；文档声明引用固定 README revision，不将仓库根许可无条件覆盖到文档站。

## 五条 acceptance 对照

| 验收条款 | 审阅结果 |
|---|---|
| 1. 区分权重、KV、编译／profiling／warmup、health／ready，并接已有执行路径 | 部分满足。正文有分层及 prefill／decode、PD 链接，但真实启动时序与 health 可见性需 C03、C04 修订。 |
| 2. 所选引擎格式／索引／分片、TP／PP、dtype／quantization，禁止格式名推断支持 | 部分满足。格式不互推、未知跨并行重分片边界正确；分派摘要有 C01，机制解释及 dtype 条件缺口见 C05。 |
| 3. 摘要、tokenizer、结构、key／shape、平台／工具版本固定身份 | 部分满足。身份维度大体齐备，但 tokenizer 选择条件有 C02，摘要可选导致 C06，不可仅据目录清单认定固定身份。 |
| 4. 覆盖文件／权限、模型识别、权重／量化、内存、编译初始化到 ready 的首失败 | 部分满足。分类已有，但权重前初始化遗漏 C03；MindIE 未证实的失败时点／逆命题见 C10。 |
| 5. 小模型／确定输入的加载、ready、质量、清理重试计划，三平台分别取证 | 部分满足。三线有各自证据且没有本库实测冒充；质量／输入计划见 C07，清理边界见 C08，AMD 版本例外见 C09。 |

## 审阅维度逐项记录

| 维度 | 核对结论 |
|---|---|
| frontmatter 必填、稳定 ID、类型、状态、日期 | 已核对，未见问题。`procedure / inference / draft` 与标题、日期一致，未以结构通过改为 reviewed。 |
| source_refs 存在性与依赖对象语义 | 已核对，未见问题。11 个 ID 全部存在；加载、tokenizer、探针、平台／插件、格式及 MindIE 来源分工匹配。具体主张误差另列 C01–C04、C09–C10。 |
| related_ids 与本地链接 | 已核对，未见问题。5 个 related_ids 均解析到现有正文；未将外部来源 ID 放入 related_ids。 |
| platforms 与 applicability／verification 状态语义 | 已核对，未见问题。`nvidia / amd / ascend` 各有正文边界；空环境档案、latest gate、`source_checked` 与未实测声明相容。此结论仅指状态语义，不替代技术主张修订。 |
| 权重装载、量化后处理、参数／索引／分片 | 有发现：C01、C05。BaseModelLoader 的初始化→读权重→后处理→eval 顺序、非推理文件过滤与索引去重已重新核对；不能由这些事实推出所有 loader、模型、平台的统一支持。 |
| tokenizer 身份与缓存 | 有发现：C02；模式选择所需文件条件不可省略。 |
| 初始化、内存、KV、编译／warmup、health／ready | 有发现：C03、C04、C10。legacy health 无条件 200、gRPC 检查 errored 的原始代码已核对，未把这些入口等同。 |
| 身份固定、质量、失败清理与重试设计 | 有发现：C06–C08。未将请求成功或 tokenizer 自洽当成模型质量证明。 |
| NVIDIA／AMD／Ascend 版本与后端边界 | 有发现：C09。其余已核对：AMD 安装页的 wheel／源码／Docker 说明及 Feature x Hardware 的 AMD 列与作者记录相符；矩阵并不提供加载格式／量化支持全集。 |
| vLLM 上游、vllm-ascend、MindIE 三线互推禁令 | 已核对，未见问题。正文明确分线；复查插件文档与固定 Ascend 文档配置，没有把不同固定样板拼成已验证组合。 |
| MindIE latest gate 与 unknown 保留 | 已核对，未见问题。取回日期、未定版、产品线关系未核、格式硬性要求、启动内存错误形态、ROCm load-format 集合等缺口均保留；没有因本次审阅成功打开页面就关闭它们。C10 是另行发现的越证据推断。 |
| safetensors 格式与完整性边界 | 已核对，未见问题。v0.7.0 Format 节支持头部／数据区描述；没有把格式结构校验等同权重数值身份、质量或任一引擎兼容证明，摘要要求不足另见 C06。 |
| 六条新增来源的许可与 notes | 有发现：C11。vLLM 三个源码切面与文档生成站点的许可边界已区分；notes 的技术压缩误差需按 C01、C02、C04 同步修订。 |
| 来源记录 SHA-256 与原文件坐标 | 已核对，未见问题。23 个已有摘要前缀复算一致；源码坐标抽查一致；features 无字节摘要如实保留。不是对网页历史字节或全仓所有外部来源的重新证明。 |
| 索引新增条目描述与 07.1 主题行 | 已核对，未见问题。两处链接正确、描述对应本文覆盖面，未声明 reviewed／实测完成；“已有正文”不等于 acceptance 已全部通过。 |
| 虚构命令、执行结果、事故与授权 | 已核对，未见问题。未发现虚构本库运行结果或事故；MindIE 字段／启动日志、device 权限、共享内存示例确有原文。是否适宜推广为操作步骤是 C08、C10 的修订对象，上游文档不是执行授权。 |

## 结构检查与改动边界

- 当前工作区 `make check`：通过，108 content entries／534 sources；只验证结构、ID 与本地文件链接，不验证技术正确性或远程页面。
- 为遵守“只能新增本报告”，未在原仓运行会改写 `build/` 的构建。复制相同源文件、配置与本地链接目标到临时目录后执行 `make build`：通过，108 entries／534 sources，生成物仅在临时副本。副本第一次／第二次构建分别因漏拷配置和链接目标失败；补齐副本输入后通过，不把副本准备问题归咎于本批内容。
- 未改 `src/kb/`，未增加测试或运行硬件测试。唯一仓库新增交付文件为本报告；正文、索引、registry、作者来源记录和主计划均未修改。
- 收尾 SHA-256 比对显示进入检查前的 539 个既有文件均未变化。期间工作区另出现并行任务的 `docs/research/batch-26-t06-08-codex-review.md`，导致首次“全工作区仅新增一个文件”的断言不成立；该文件不是本轮写入，未读取其内容、未修改或删除，亦不纳入本报告结论。应以本轮写入范围和既有文件摘要核验区分并发交付，不能将外部新文件算作本轮修改。

## 整体结论

**需修订。** 当前有 10 项 P2、1 项 P3 开放发现；五条 acceptance 均仍有需补齐或纠正的部分，不能宣布 T07-01 审阅通过。结构检查成功、摘要一致以及来源可访问，不抵消技术表述、验收覆盖及清理安全边界的问题。

作者修订后须按 C01–C11 的关闭条件进行定向复核，并同步修正受影响的来源 notes／主张表；在完成复核前不把发现标为关闭。即使届时来源／编辑审阅通过，也不构成 NVIDIA、AMD 或 Ascend 的硬件加载、ready 或输出质量验证。
