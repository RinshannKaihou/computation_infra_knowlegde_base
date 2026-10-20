# 第二十六批 T07-01 来源记录

任务：T07-01（权重加载、引擎 ready 与启动失败诊断；**new** procedure `knowledge/07-inference/model-loading-and-readiness.md`，主题 07.1）。取证轮次：主会话作者角色首轮（2026-10-20，Batch 25 尚未收尾期间的并行来源准备轮）。

执行边界：本轮仅做来源准备（下载固定 ref 源码包、直读官方文档站），未运行任何 vLLM/MindIE 加载、服务化或推理命令；**未修改 `sources/registry.yaml`、领域索引与主计划**——Batch 25 当前占用这些串行集成资源（工作区存在其未提交改动），下文 NEW 登记号均为建议 ID，待集成轮统一登记。本轮是来源记录，不构成 T07-01 交付完成。

版本选择口径：vLLM 锚定既有登记 `src.vllm.inference-v0-14` 的固定 commit `b17039bccc17b94a2ea107272ad7bc93508708df`（tag v0.14.0 解析结果），不新开版本线；文档站页面对应 v0.14.0。safetensors 复用既有 `src.hf.safetensors-v0.7.0`，不重复取证格式层。MindIE 侧：开源仓 Ascend/MindIE-LLM 截至 2026-10-20 无 release tag，固定为 master commit `69e5a5dd4b533eaffc7e198320435350825a36f7`（codeload 快照＋commits atom 钉扎）；其官方文档站 mindie-llm-doc.readthedocs.io 仅提供 latest（未定版）——此为来源 gate，见 unknown 清单。hiascend 产品文档门户（mindie/310 线）为 JS 渲染，本轮 curl 直读为空，未采用。

## 本轮取回清单（2026-10-20）

| 对象 | 版本/ref | SHA-256（前 16 位） |
|---|---|---|
| vLLM codeload 源码包 | b17039bc（v0.14.0） | 6b34734aa4cb6f40 |
| vllm/model_executor/model_loader/\_\_init\_\_.py | 同上 | 2c77c81293e30a1d |
| vllm/model_executor/model_loader/base_loader.py | 同上 | a3fc7d2404151441 |
| vllm/model_executor/model_loader/default_loader.py | 同上 | abd0a03619010094 |
| vllm/model_executor/model_loader/utils.py | 同上 | a071e8cea1d39d4a |
| vllm/model_executor/model_loader/sharded_state_loader.py | 同上 | 2b1842cbad28c29c |
| vllm/model_executor/model_loader/weight_utils.py | 同上 | 57e7de9ef6764691 |
| vllm/model_executor/models/registry.py | 同上 | a96adc7f6b73f45c |
| vllm/v1/worker/gpu_model_runner.py | 同上 | 7eaa9eb78cb99f9f |
| vllm/config/load.py | 同上 | 077a47c1a2b38da2 |
| vllm/v1/engine/async_llm.py | 同上 | 818af4561b7ae54a |
| vllm/entrypoints/serve/\_\_init\_\_.py | 同上 | f3024ad12d019962 |
| vllm/entrypoints/serve/instrumentator/health.py | 同上 | 52688514a0a38dc7 |
| vllm/entrypoints/api_server.py（legacy） | 同上 | 254336c6ae720cb2 |
| vllm/entrypoints/grpc_server.py | 同上 | e09dddb0068abefb |
| vllm/tokenizers/registry.py | 同上 | ee1e4059ffabbf29 |
| vllm/transformers_utils/tokenizer.py（deprecation shim） | 同上 | 50435b002803191a |
| docs.vllm.ai GPU 安装页（含 AMD ROCm 节） | v0.14.0 文档站 | 4854e448034189f6 |
| docs.vllm.ai features 页（Feature x Hardware 矩阵） | v0.14.0 文档站 | 无字节快照（见 unknown #3） |
| MindIE-LLM codeload 源码包 | master@69e5a5dd | 1b67d0215ffc8dd0 |
| MindIE-LLM README.md | 同上 | 1f030a9e43ad6a89 |
| MindIE-LLM LICENSE.md（木兰宽松许可证第 2 版） | 同上 | 1b783a52f139dfb8 |
| mindie-llm-doc 模型支持列表页 | latest（2026-10-20 取回） | 3d5c6434abc25827 |
| mindie-llm-doc 快速入门页 | latest（2026-10-20 取回） | 11d8f5ce8ad446d0 |

vLLM 各文件 hash 均对 codeload 快照包内路径计算；与既有登记 `src.vllm.inference-v0-14`（同一 commit）为同一来源的不同文件切面。

## 主张—来源定位表

| 主张 | 登记 ID | 精确位置 | 支持范围 / 未覆盖 |
|---|---|---|---|
| load-format 分派（14 个内置值：auto/hf/bitsandbytes/dummy/fastsafetensors/gguf/mistral/npcache/pt/runai_streamer/runai_streamer_sharded/safetensors/sharded_state/tensorizer；默认 loader 对应其中 7 种，dummy/bitsandbytes/gguf/runai_streamer/tensorizer 专用类，runai_streamer_sharded 与 sharded_state 同映射 ShardedStateLoader）；未注册名称在 get_model_loader 查询时报 ValueError（配置层仅小写归一），`register_model_loader` 自定义注册（14 值非封闭全集）；auto 存在 consolidated*.safetensors 时自动改走 mistral 分支；TP/PP 读取映射（llama.py weight_loader 样板、PP 缺失层跳过）与 dtype 三层（文件记录/目标 dtype/硬件检查） | NEW src.vllm.model-loader-v0-14 | model_loader/\_\_init\_\_.py（LoadFormats、\_LOAD\_FORMAT\_TO\_MODEL\_LOADER L55–71、get_model_loader L118–123、register_model_loader）；default_loader.py auto→mistral 分支 L101–114、fall_back_to_pt/模式覆盖 L57–60；llama.py L461+；gpu_worker.py check_if_supports_dtype | 分派、注册与映射机制；各 loader 内部质量/性能行为未逐一核对（bitsandbytes/tensorizer/gguf/runai 仅登记入口） |
| LoadConfig 字段语义（load_format 小写归一、download_dir、model_loader_extra_config、ignore_patterns 默认 `original/**/*`） | NEW src.vllm.model-loader-v0-14 | vllm/config/load.py L25–124 | 配置面；与 CLI 参数的映射未核 |
| 权重文件准备：未知格式 ValueError；auto/hf=`*.safetensors`+`*.bin`；mistral=`consolidated*.safetensors`＋index；量化模型可能用 .pt；分片/合并并存时下载 index 去重 | NEW src.vllm.model-loader-v0-14 | default_loader.py \_prepare_weights（L80–184：ValueError L131、allow_patterns、download_safetensors_index_file_from_hf、filter_duplicate_safetensors_files） | 文件选择逻辑；权重内容校验（key/shape 匹配错误）在模型各自 load_weights，未逐一核 |
| 加载顺序与边界：initialize_model（arch 解析＋量化配置注入＋旧式类 Deprecation）→ load_weights → process_weights_after_loading（quant repack、CPU offload device_loading_context 往返、attention 后处理）→ eval()；量化发生在 load_weights **之后** | NEW src.vllm.model-loader-v0-14 | base_loader.py load_model L38–61；utils.py initialize\_model/process\_weights\_after\_loading L27–118 | 顺序与异常面；各 quant_method 的 repack 细节不在本切面 |
| 架构解析失败路径：`Model architectures … are not supported for now` ValueError；历史架构移出版本提示；无 vLLM 实现时回退 Transformers 实现的 warning | NEW src.vllm.model-loader-v0-14 | models/registry.py L812–847；utils.py \_get\_model\_architecture L181–189 | 错误形态；Transformers 回退路径的功能差异未核 |
| 非推理权重文件过滤（optimizer.bin/scheduler.pt/scaler.pt/training\_args.bin 等） | NEW src.vllm.model-loader-v0-14 | weight_utils.py filter\_files\_not\_needed\_for\_inference L579+ | 过滤名单；HF 侧文件生成规则不在此源 |
| sharded\_state 格式：`model-rank-{rank}-part-{part}.safetensors` 模式、save\_sharded\_state.py 示例、s3 支持 | NEW src.vllm.model-loader-v0-14 | sharded_state_loader.py L28–56 | vLLM 自有保存格式；**TP/PP 跨度重分片能力未从此文件证实**（unknown #6） |
| worker 侧调用点：load\_model（DeviceMemoryProfiler＋计时、LoRA 叠加、drafter/spec-decode、EPLB/eep\_scale\_up）；reload\_weights 原地权重重载 | NEW src.vllm.model-loader-v0-14 | gpu_model_runner.py L3803+、L4000–4006 | 调用链；GPU worker 内存画像链复用既有登记 notes |
| tokenizer 解析：vllm/tokenizers/registry.get\_tokenizer（HF/ModelScope、tokenizer\_mode 注册表；auto 切 mistral 须同时满足装 mistral\_common 且 tokenizer 名称/revision 文件匹配 tekken.json 或 tokenizer.model.v\*，另有 tokenizer.tok.json tiktoken 分支；慢 tokenizer 警告；lru\_cache 对象复用仅在 cached\_get\_tokenizer 缓存包装入口）；旧路径为 deprecation shim | NEW src.vllm.tokenizer-registry-v0-14 | tokenizers/registry.py L190+、L36/L145–160；transformers\_utils/tokenizer.py | 解析与模式选择；各 tokenizer 类正确性不在范围 |
| `/health` 语义（OpenAI server）：register\_vllm\_serve\_api\_routers → attach\_health\_router → `check_health()`；EngineDeadError → 503，否则 200。函数层只反映 errored 标志（不重跑加载/warmup、不探测请求质量）；**标准入口在引擎构建与应用状态初始化后才开始 HTTP 服务**（run_server 顺序，启动序列完成前 /health 不可达）；legacy api_server 为另一进程形态，/health 无条件 200 | NEW src.vllm.readiness-health-v0-14 | serve/\_\_init\_\_.py L79–83；instrumentator/health.py；async\_llm.py check\_health L727；openai/api\_server.py run\_server L1338–1353 | 引擎死活探针＋入口生命周期边界；**不是 ready 探针**，就绪判据为启动序列完成＋确定输入请求成功 |
| legacy API server `/health` 无条件 200（仅进程存活）；gRPC HealthCheck healthy=!errored | NEW src.vllm.readiness-health-v0-14 | entrypoints/api\_server.py L40–44；grpc\_server.py L153–167 | 两类旁路入口的语义差异 |
| 启动就绪序列（加载→profile run/内存判定→CUDA graph 捕获）与 OOM 首失败边界 | 复用 src.vllm.inference-v0-14 | （既有 notes：gpu\_worker determine\_available\_memory/profile\_run/150MiB 冗余、cache\_config gpu\_memory\_utilization、KV 不足 ValueError、EngineDeadError 形态） | 本轮未重开；与 loader 链拼成完整 ready 路径 |
| 平台能力面（check\_and\_update\_config/verify\_model\_arch/verify\_quantization）与插件扩展点 | 复用 src.vllm.platform-interface-0.14、src.vllm.plugin-system-v0-14 | （既有） | 模型/量化校验的平台责任面 |
| 制品格式基线（8 字节头＋JSON header、仅 dtype/shape/data\_offsets/\_\_metadata\_\_、无校验和字段） | 复用 src.hf.safetensors-v0.7.0 | （既有） | 格式层；引擎侧支持以 loader 实现为准 |
| ROCm 安装与支持条件：ROCm 6.3+/torch 2.8.0+（MI350 需 7.0+、Ryzen AI 需 7.0.2+）；gfx90a/942/950、Radeon gfx1100/1101/1200/1201、gfx1151/1150；**无预编译 wheel**（须源码编译，`pip install .` 声明不可用）；docker（rocm/vllm）为推荐方式；ROCm Triton 指定 commit、ROCm flash-attn v2.8.0 可选、AITER/MORI（EP/PD）可选；PYTORCH\_ROCM\_ARCH | NEW src.vllm.rocm-install-doc-v0-14 | docs.vllm.ai v0.14.0 getting\_started/installation/gpu（AMD ROCm 节） | 安装/组合条件；**不证明任何加载格式或量化在 ROCm 可用**（矩阵不含该维度） |
| Feature x Hardware 矩阵（ROCm 行）：✅ chunked prefill/prefix caching/LoRA/spec decode/CUDA graph/multimodal 等；❌ encoder-decoder、async output；❔ prompt-embeds；Volta 无 chunked prefill/prefix caching | NEW src.vllm.rocm-install-doc-v0-14 | docs.vllm.ai v0.14.0 features 页（#feature-x-hardware） | 特性×硬件覆盖；矩阵明确不覆盖加载格式与量化方法，禁止外推 |
| MindIE 模型支持分级：充分验证支持/仅功能支持两级；逐模型量化矩阵（W8A8/W4A8/W8A16/LoRA/atbgraph/aclgraph）与 Atlas 800I A2/A3/300I Duo 卡数；DeepSeek/Qwen/Llama/ERNIE/KIMI/GLM/Baichuan＋多模态；页脚更新 2026-04-21 | NEW src.ascend.mindie-llm-doc-latest | mindie-llm-doc.readthedocs.io user\_guide/model\_support\_list | 支持面分级；**latest 未定版**（gate）；具体模型×量化×固件组合以产品文档为准 |
| MindIE 装载与启动链：modelWeightPath 读取权重目录 config.json 的 torch\_dtype/vocab\_size 字段并做属组/权限安全校验；worldSize 必须等于使用 NPU 数；trustRemoteCode 默认 false；服务化 config.json 权限 640 | NEW src.ascend.mindie-llm-doc-latest | 快速入门页（配置服务化参数表） | 配置语义与校验；**权重文件格式要求（safetensors 与否）该页未逐字声明**（unknown #4） |
| MindIE 启动成功标志与首失败边界：`Daemon start success!`（充分观察标志，未观察到只代表就绪未证实）；bin 目录 550 只读须在可写目录拉起（kernel\_meta 生成）；device 挂载须 rwm（rw 时 npu-smi 报错/torch.npu.set\_device 失败，A3 必现）；切换用户后文档在特定容器部署语境给出清理 /dev/shm 旧用户共享文件的示例（有状态变更，须停妥/归属/无他者/授权并只处理本实例遗留，非通用通配处方）；`curl POST /generate` 验证 | NEW src.ascend.mindie-llm-doc-latest | 快速入门页（启动服务/发送请求节） | 文档口径的启动边界；未实测 |
| MindIE 组件栈与安装路径：CANN/CANN-NNAL-ATB/MindIE/ATB Models 容器路径；whl 包（{site\_packages}/mindie\_llm＋/usr/local/Ascend/atb\_llm）与 run 包（/usr/local/Ascend/mindie/latest/…）两种安装形态 | NEW src.ascend.mindie-llm-doc-latest | 快速入门页（表 2 及说明） | 路径口径；与产品包版本对应关系未核 |
| MindIE-LLM 配套版本表：MindIE 软件 2.3.0 ↔ CANN 8.5.0；许可木兰 PSL-2（LICENSE.md），文档站内容 CC BY-SA 4.0（README 声明） | NEW src.ascend.mindie-llm-repo-69e5a5dd | README.md 版本说明表；LICENSE.md | 开源仓 master@69e5a5dd 快照口径；与 hiascend 产品文档版本线（如 mindie/310）**不互推** |
| 推理执行/插件边界背景 | 复用 src.vllm.inference-v0-14、src.ascend.vllm-ascend-v0-14-0rc1 | （既有） | 本轮未重开 |

## unknown 清单

1. **MindIE 来源 gate**：MindIE-LLM 开源仓无 release tag，固定为 master@69e5a5dd（2026-10-20 快照）；其文档站仅 latest 未定版。T07-03 深化前需选定固定版本线，并理清开源仓版本（README 表 2.3.0↔CANN 8.5.0）与 hiascend 产品文档线（310 等）的关系，两者不互推。
2. hiascend 产品文档门户为 JS 渲染，本轮直读为空未采用；MindIE 产品包（非开源仓）的安装/支持文档未取证。
3. docs.vllm.ai features 页两次 curl 直连 SSL 失败，仅经渲染取回文本（Feature x Hardware 矩阵内容已核对），无字节快照与 SHA；集成轮复核时可重试直读。
4. MindIE 权重格式硬性要求（是否仅 safetensors、bin/pt 转换流程）在快速入门页未逐字声明；论坛 FAQ 提到非 safetensors 需人工转换，但论坛帖不作为登记来源。T07-01 正文引用前须从官方模型支持列表/开发指南再取证，否则标 unknown。
5. vLLM ROCm 平台是否存在加载路径实现差异（专用 loader/权重处理分支）未逐文件核对；Feature x Hardware 矩阵不含加载格式行，不得从安装文档推断 ROCm 加载格式支持全集。
6. `sharded_state` 格式的跨 TP/PP 重分片（保存与加载 world size/并行不同）能力未从源码证实，仅登记格式模式与示例入口。
7. safetensors 跨文件分片索引（model.safetensors.index.json）的语义归 HF/transformers 侧，既有登记的 unknown 仍开放；本轮仅核到 vLLM 侧 index 下载与去重行为。
8. uvicorn「Application startup complete」横幅属 uvicorn 标准行为，未单独取证；vLLM ready 与该横幅的先后关系按启动序列描述，未实测。
9. 全部行为均为源码/文档口径；未运行任何加载、服务化、health 探针或推理命令，无本库实测结果。

## 集成轮结果（2026-10-20 已执行）

- `sources/registry.yaml` 已登记本轮 6 个 NEW ID：src.vllm.model-loader-v0-14、src.vllm.tokenizer-registry-v0-14（决定保持分立，与 loader 机制分开引用）、src.vllm.readiness-health-v0-14、src.vllm.rocm-install-doc-v0-14、src.ascend.mindie-llm-doc-latest、src.ascend.mindie-llm-repo-69e5a5dd（许可：vLLM Apache-2.0 沿既有核验；MindIE-LLM 木兰 PSL-2 已直核 LICENSE.md、文档站 CC BY-SA 4.0 按 README 声明登记）。registry 由 525 增至 534（含 T06-08 轮 3 项）。
- T07-01 正文进入撰写轮（07-inference 域已存在，索引由集成角色更新）。
