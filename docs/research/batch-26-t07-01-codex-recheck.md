# Batch 26 T07-01 修订后定向复核（第二轮）

## 复核头部

- 审阅模型／推理档位：`gpt-6.1-sol / xhigh`。已核对本轮本地 Codex CLI 会话的 `turn_context.model` 与 `turn_context.effort`；记录与约定一致，未调用其他模型或子代理。
- 日期：2026-10-20（Asia/Shanghai）。
- 角色与基准：独立批次审阅者，按[初审报告](batch-26-t07-01-codex-review.md)的 C01–C11 关闭条件逐项复核，并检查修订产生的技术错误、过度声明及未标注推断；不代作者修改原文。
- 对象：[正文](../../knowledge/07-inference/model-loading-and-readiness.md)、[来源登记](../../sources/registry.yaml)的相关条目、[作者来源记录](batch-26-t07-01-sources.md)。下表本地行号均指本轮读取的修订稿。
- 执行边界：只新增本报告。遵照本轮要求，不重跑 `make check`／`make build`；作者报告的 108 entries／534 sources 不作为技术正确性证据。未执行引擎启动、权重加载、请求、探针或清理操作，无硬件验证。

本轮重新打开精确上游资料。GitHub 网页读取出现 cache miss 后，改用 GitHub 文件读取工具取得固定 ref 原文：vLLM `b17039bccc17b94a2ea107272ad7bc93508708df` 的 loader、配置、tokenizer、worker、TP/PP、服务入口与 health 相关文件，以及 MindIE `69e5a5dd4b533eaffc7e198320435350825a36f7` 的 README／LICENSE 和 safetensors v0.7.0 README。15 个重开的 vLLM 源文件与本机同 commit 副本逐字节一致；下表 GitHub 行锚点使用原文件坐标，不使用网页渲染坐标。

另重开 docs.vllm.ai **v0.14.0** 的 GPU 安装页、features 页，以及 mindie-llm-doc 的快速入门页。MindIE 页面仍是 **latest，2026-10-20 重新读取，未固定文档 commit**；不将其冒充固定产品版本，不关闭原有版本 gate。本轮不重复确认作者全部历史快照摘要。

## C01–C11 逐项复核

| 发现／原优先级 | 结论 | 修订位置 | 本轮重开证据 | 备注与关闭条件核对 |
|---|---|---|---|---|
| **C01／P2** | **CLOSED** | 正文 L99；登记 L6571；来源记录 L44–46 | [loader 分派 L31–62](https://github.com/vllm-project/vllm/blob/b17039bccc17b94a2ea107272ad7bc93508708df/vllm/model_executor/model_loader/__init__.py#L31-L62)、[查询拒绝点 L118–123](https://github.com/vllm-project/vllm/blob/b17039bccc17b94a2ea107272ad7bc93508708df/vllm/model_executor/model_loader/__init__.py#L118-L123)、[文件选择 L100–137](https://github.com/vllm-project/vllm/blob/b17039bccc17b94a2ea107272ad7bc93508708df/vllm/model_executor/model_loader/default_loader.py#L100-L137)、[配置归一 L110–112](https://github.com/vllm-project/vllm/blob/b17039bccc17b94a2ea107272ad7bc93508708df/vllm/config/load.py#L110-L112)。 | 三处已同步：默认 loader 为 7 个名称，5 个名称各有专用类，另外 2 个同映射 `ShardedStateLoader`；补回 `auto` 检测 consolidated 文件后选 `mistral`，并保留 `.pt` 回退与模式覆盖。配置归一、查询拒绝和自定义注册已分开，未把 14 个内置名称写成封闭全集。 |
| **C02／P2** | **CLOSED** | 正文 L125、L129；登记 L6585；来源记录 L52 | [tokenizer 模式条件 L145–168](https://github.com/vllm-project/vllm/blob/b17039bccc17b94a2ea107272ad7bc93508708df/vllm/tokenizers/registry.py#L145-L168)、[构造及缓存 L190–237](https://github.com/vllm-project/vllm/blob/b17039bccc17b94a2ea107272ad7bc93508708df/vllm/tokenizers/registry.py#L190-L237)。 | 三处均补足依赖、文件匹配及 tokenizer 名称／revision 条件；没有要求所有模型改用 Mistral。对象复用明确限定 `cached_get_tokenizer`；直接 `get_tokenizer` 虽使用参数解析缓存，但每次仍调用 tokenizer 类构造入口，不能据此宣称复用同一 tokenizer 对象。 |
| **C03／P2** | **CLOSED** | 正文 L61–79、L139–140；登记 L6571 | [装载前设备初始化 L208–234](https://github.com/vllm-project/vllm/blob/b17039bccc17b94a2ea107272ad7bc93508708df/vllm/v1/worker/gpu_worker.py#L208-L234)、[空闲内存拒绝 L253–273](https://github.com/vllm-project/vllm/blob/b17039bccc17b94a2ea107272ad7bc93508708df/vllm/v1/worker/utils.py#L253-L273)、[后续装载／profiling L269–298](https://github.com/vllm-project/vllm/blob/b17039bccc17b94a2ea107272ad7bc93508708df/vllm/v1/worker/gpu_worker.py#L269-L298)、[warmup／图捕获 L443–455](https://github.com/vllm-project/vllm/blob/b17039bccc17b94a2ea107272ad7bc93508708df/vllm/v1/worker/gpu_worker.py#L443-L455)。 | 已声明五阶段是诊断分类，撤回两线共有的严格串行时序；显式补入权重前设备绑定、dtype、通信与空闲内存检查，和装载后 profiling／KV／warmup 区分。首失败表保留“启动期内存判定失败”入口，不再只能接住装载后 OOM。 |
| **C04／P2** | **CLOSED** | 正文 L79；登记 L6599；来源记录 L53–54 | [标准入口 L1338–1353](https://github.com/vllm-project/vllm/blob/b17039bccc17b94a2ea107272ad7bc93508708df/vllm/entrypoints/openai/api_server.py#L1338-L1353)、[health handler L22–29](https://github.com/vllm-project/vllm/blob/b17039bccc17b94a2ea107272ad7bc93508708df/vllm/entrypoints/serve/instrumentator/health.py#L22-L29)、[错误标志 L727–730](https://github.com/vllm-project/vllm/blob/b17039bccc17b94a2ea107272ad7bc93508708df/vllm/v1/engine/async_llm.py#L727-L730)；另核[legacy L40–43](https://github.com/vllm-project/vllm/blob/b17039bccc17b94a2ea107272ad7bc93508708df/vllm/entrypoints/api_server.py#L40-L43)、[gRPC L162–167](https://github.com/vllm-project/vllm/blob/b17039bccc17b94a2ea107272ad7bc93508708df/vllm/entrypoints/grpc_server.py#L162-L167)。 | 三处已区分 handler 检查项、初始 HTTP 服务可访问时点、请求／质量判据。标准入口先构建引擎并初始化应用状态，再调用 `serve_http`；没有继续推断初始加载未完成就能返回 health 200。legacy 和 gRPC 已分别限定。这里的 HTTP 可服务不等同于 socket 提前绑定，后者见同文件 L1283–1290。 |
| **C05／P2** | **CLOSED** | 正文 L101–107；登记 L6571；来源记录 L44、L50 | [Llama 映射及 PP 跳过 L461–521](https://github.com/vllm-project/vllm/blob/b17039bccc17b94a2ea107272ad7bc93508708df/vllm/model_executor/models/llama.py#L461-L521)、[线性层按 TP rank 取片 L551–578](https://github.com/vllm-project/vllm/blob/b17039bccc17b94a2ea107272ad7bc93508708df/vllm/model_executor/layers/linear.py#L551-L578)、[预分片装载 L109–162](https://github.com/vllm-project/vllm/blob/b17039bccc17b94a2ea107272ad7bc93508708df/vllm/model_executor/model_loader/sharded_state_loader.py#L109-L162)、[目标 dtype 上下文 L47–59](https://github.com/vllm-project/vllm/blob/b17039bccc17b94a2ea107272ad7bc93508708df/vllm/model_executor/model_loader/base_loader.py#L47-L59)、[硬件检查 L208–211](https://github.com/vllm-project/vllm/blob/b17039bccc17b94a2ea107272ad7bc93508708df/vllm/v1/worker/gpu_worker.py#L208-L211)。 | 新小节补出普通权重经模型参数 loader 映射／TP 取片、PP 缺失层跳过与按当前 TP rank 读取预分片文件的区别，要求保存侧并行配置记录。文件 dtype、配置目标 dtype 与硬件检查已分层，量化打包依赖专用处理；样板限定到具体实现，跨 TP／PP 重分片继续为 unknown，未外推全平台支持。 |
| **C06／P2** | **CLOSED** | 正文 L123–129、L149、L173 | [实际文件选择 L150–182](https://github.com/vllm-project/vllm/blob/b17039bccc17b94a2ea107272ad7bc93508708df/vllm/model_executor/model_loader/default_loader.py#L150-L182)、[safetensors v0.7.0 Format](https://github.com/safetensors/safetensors/blob/v0.7.0/README.md#format)。 | 实际选用权重、索引、config、tokenizer／模板的内容摘要或可追溯不可变制品身份改为必需，要求算法／覆盖范围，并明确同名同大小不足以判同。无法取得时必须记缺口，不能宣称身份已固定。此项是身份验收设计；未宣称上游自动计算摘要，也未虚构现场摘要结果。 |
| **C07／P2** | **CLOSED** | 正文 L152、L162、L173 | [tokenizer 构造／缓存 L190–237](https://github.com/vllm-project/vllm/blob/b17039bccc17b94a2ea107272ad7bc93508708df/vllm/tokenizers/registry.py#L190-L237)、[MindIE 快速入门“发送请求”与“精度测试”](https://mindie-llm-doc.readthedocs.io/zh-cn/latest/user_guide/quick_start/quick_start/)；并对照[本库质量判据](../../knowledge/07-inference/quantization-and-quality.md)。 | 已撤销“参考输出或 tokenizer 自洽”的替代关系；tokenizer 自检与模型质量分开。质量要求明确参考／任务指标与阈值，并列出三平台须记录的模型、确定输入、采样／模板、参考来源和判定字段；参考缺失须记计划缺口。此结论只关闭计划约束缺陷，不表示已选定具体实验或完成质量评估；两种验证不等价是审阅推理。 |
| **C08／P2** | **未关闭** | 正文 L86、L153、L168 已修；**登记 L6627、来源记录 L62 仍残留** | [MindIE 快速入门“启动服务”注意事项及其容器部署上下文](https://mindie-llm-doc.readthedocs.io/zh-cn/latest/user_guide/quick_start/quick_start/)。 | 正文已具备停妥、容器／IPC 命名空间、归属、无其他消费者、既有授权与本实例对象限定，并明确清理属于有状态变更。但另外两处仍写“切换用户须 `rm -f /dev/shm/*`”，没有标示上游特定部署示例与危险边界。初审关闭条件明确覆盖这些来源记录，故不能全项关闭。**剩余要求：**在登记 notes 与来源表将其标为上游示例，同步上述对象／隔离前提，明确不得当作未限定环境的通用通配删除处方；可保留示例作证据，不应保留无条件要求。风险判断为审阅推理，不是声称上游没有该示例。 |
| **C09／P2** | **CLOSED** | 正文 L89；登记 L6613；来源记录 L58 | [vLLM v0.14.0 GPU 安装页 Requirements](https://docs.vllm.ai/en/v0.14.0/getting_started/installation/gpu/#requirements)、[Feature x Hardware](https://docs.vllm.ai/en/v0.14.0/features/#feature-x-hardware)。 | 正文已在硬件／版本说明附近补回 Ryzen AI MAX／AI 300 的 ROCm 7.0.2+ 下限，与另外两处一致；MI350 的 7.0+ 例外和通用 6.3+ 条件仍分开。继续明确安装条件及特性矩阵不证明加载格式／量化方法支持全集。 |
| **C10／P2** | **未关闭** | 正文 L84、L87 已修；**正文 L141 仍残留** | [MindIE 快速入门“配置服务化参数”与“启动服务／发送请求”](https://mindie-llm-doc.readthedocs.io/zh-cn/latest/user_guide/quick_start/quick_start/)。 | 字段值与权重不符的失败时点已改为 unknown；L87 也正确说明成功日志是充分观察标志，未观察到只代表就绪未证实。但首失败分类表仍逐字写“**未达 `Daemon start success!` 即无服务**”，与修订后的同页说明矛盾，继续把充分条件倒推成必要条件。**剩余要求：**将 L141 改为未观察到日志时就绪尚未证实，结合日志完整性与实际请求判断；不得以未采集到一行日志断言没有服务。上游没有给出该逆命题，逻辑判定属审阅推理。 |
| **C11／P3** | **CLOSED** | 登记 L6623–6626、L6637–6640 | [MindIE 固定 LICENSE.md](https://github.com/Ascend/MindIE-LLM/blob/69e5a5dd4b533eaffc7e198320435350825a36f7/LICENSE.md)、[同 commit README L99–103](https://github.com/Ascend/MindIE-LLM/blob/69e5a5dd4b533eaffc7e198320435350825a36f7/README.md#L99-L103)。 | 仓库源码的结构化 scope 已排除 README 另有声明的文档与第三方内容；文档声明 URL 已固定完整 commit。文档站条目保留 partial，notes 明确 README 对“本文档”的声明不自动覆盖站点所有页面及第三方内容，未将根许可无条件覆盖到文档站。此为登记边界核对，不作法律适用裁定。 |

## 新发现问题

**未发现需另立 T07-01-Rxx 的独立新技术问题。** 本轮重点核对了新补的默认 loader 三组映射、tokenizer 文件条件、装载前设备检查、health 三层语义、TP／PP 与 dtype 小节，以及身份／质量／清理边界。C08、C10 是原发现修订不完整的残留，沿用原 ID 与 P2 优先级，不重复计为新发现。

本结论限于本次定向复核范围，不扩大为所有 loader、量化方法、平台或生命周期分支均正确。MindIE latest 版本对应关系、跨 TP／PP 重分片及实际平台可用集等原有 unknown 继续保留；来源／编辑核对不构成实验验证。

## 整体结论

**未通过，仍需修订。** 11 项中 **9 项 CLOSED（8 P2＋1 P3）**，**2 项 P2 未关闭**：

- **C08**：来源登记 L6627 和作者来源记录 L62 尚未同步共享内存清理的对象与隔离边界。
- **C10**：正文 L141 仍保留“未达成功日志即无服务”的不成立逆命题。

完成上述剩余修订并定向复核后，才能宣布 T07-01 通过；本轮未修改正文、来源登记或作者来源记录。
