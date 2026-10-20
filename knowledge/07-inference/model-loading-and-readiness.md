---
id: inference.model-loading-and-readiness
title: 权重加载、引擎 ready 与启动失败诊断
type: procedure
domain: inference
status: draft
platforms: [nvidia, amd, ascend]
source_refs:
- src.vllm.model-loader-v0-14
- src.vllm.tokenizer-registry-v0-14
- src.vllm.readiness-health-v0-14
- src.vllm.rocm-install-doc-v0-14
- src.ascend.mindie-llm-doc-latest
- src.ascend.mindie-llm-repo-69e5a5dd
- src.vllm.inference-v0-14
- src.vllm.platform-interface-0.14
- src.vllm.plugin-system-v0-14
- src.ascend.vllm-ascend-v0-14-0rc1
- src.hf.safetensors-v0.7.0
updated_at: "2026-10-20"
applicability:
  environment_refs: []
  notes: "未建立环境档案。vLLM 以 v0.14.0 固定 commit（b17039bc）源码为样板；MindIE 以官方文档站 2026-10-20 取回的 latest 页与开源仓 master@69e5a5dd 为样板（文档站未定版）；ROCm 侧为 v0.14.0 安装文档口径。三平台各自的具体机型、驱动/运行库版本与容器组合须现场补齐，本文不构成部署建议。"
verification:
  status: source_checked
  evidence_refs:
  - src.vllm.model-loader-v0-14
  - src.vllm.readiness-health-v0-14
  - src.ascend.mindie-llm-doc-latest
  notes: "仅核对固定 commit 源码与官方文档语义（锚点见 docs/research/batch-26-t07-01-sources.md）；未启动任何引擎、未加载任何权重、未调用任何 health/ready 探针。"
summary: 区分权重加载、KV 建立、编译/warmup 与 health/ready 探针四类启动阶段，给出 vLLM 与 MindIE 的装载链、模型身份固定清单、首失败边界分类与小模型验证计划。
related_ids:
- inference.execution-and-kv-cache
- inference.ascend-inference-oom-triage
- inference.quantization-and-quality
- inference.pd-disaggregation
- inference.latency-metrics
---

# 权重加载、引擎 ready 与启动失败诊断

本页处理推理引擎从静止到可服务的启动路径：模型/权重/tokenizer 的解析与装载、内存判定与图捕获、就绪标志与健康探针，以及这条链上的第一失败证据。装载完成之后的执行行为（prefill/decode、KV 生命周期、批调度）见[推理执行与 KV 缓存](execution-and-kv-cache.md)；PD 分离部署下的权重/KV 交接见[PD 分离](pd-disaggregation.md)；本页只在启动边界与两者相接。

引擎证据分三条线，互不外推：vLLM 上游 v0.14.0 固定 commit（引擎机制，NVIDIA/AMD 为其官方支持后端）；vllm-ascend v0.14.0rc1（Ascend 侧插件线，已在既有登记固定）；MindIE（昇腾官方推理引擎，本文档站快照口径）。三线的装载实现各自独立，任一线支持某格式不构成其他线的支持结论。

所有配置字段与命令均为文档/源码语义转述，本文不授予执行权限；启动、终止与探测操作的影响见各节说明。

## 目标与触发条件

回答四个问题：

1. 一次启动失败发生在装载链的哪一层（文件与权限、模型识别、权重内容、设备内存、编译/初始化、探针）；
2. 如何在对照实验之前固定"加载了哪个模型"（目录、结构、tokenizer、参数与平台版本的身份）；
3. health 探针与 ready 的区别——进程活着不等于可服务；
4. 如何用小模型与确定输入验证一次启动成功且输出质量成立。

触发条件：首次部署、更换模型或引擎版本、扩缩副本、启动失败、探针异常或"看似就绪但首请求失败"。

## 启动序列与阶段边界

把启动拆成五个阶段。**这是诊断分类，不是断言所有引擎按同一时序串行执行**——先定位失败属于哪一类，再谈修复；各引擎的真实调用顺序见下方分线说明（vLLM 在权重装载前还有一批设备与内存检查）。

| 阶段 | 内容 | 典型首失败证据 | 说明 |
|---|---|---|---|
| S1 目录与文件 | 权重目录存在、文件齐全、权限/属组正确 | 路径不存在、权限拒绝、属组不符 | 引擎在此做安全与存在性校验（MindIE 在配置解析时即校验；不作为两线共有的严格时序保证） |
| S2 身份解析 | config/结构/tokenizer 读取，架构映射 | 架构不支持、字段缺失、tokenizer 加载失败 | 决定"这是哪个模型、哪个实现" |
| S3 权重装载 | 按格式选 loader、流式读入、必要时重打包 | 格式/键/形状不匹配、分片索引错误、校验失败 | 量化处理多发生在装载后（见下） |
| S4 内存与编译 | profile run、内存判定、图捕获/算子编译 | 设备内存不足、图捕获失败、算子缺失 | 决定能否进入服务状态；**设备内存类失败也可能早于 S3 发生**（见 vLLM 分线） |
| S5 就绪与探针 | 服务进程完成启动序列，暴露 health/ready | 探针 503、假就绪（探针 200 但首请求失败） | health 多为死活探针，不等于 ready |

### 各阶段在两条引擎线上的证据形态

**vLLM（v0.14.0 固定 commit）**：

- **装载前的设备与内存检查**：worker 初始化先于任何权重装载完成设备绑定、dtype 硬件支持检查（`check_if_supports_dtype`）、分布式环境初始化（注释明确 NCCL buffer 先于内存快照分配）与启动期内存快照/申请检查（`request_memory`）——设备、通信或空闲内存不足的首失败可能发生在 S3 之前，不应一律归入"装载后 profiling"（[gpu_worker.py](https://github.com/vllm-project/vllm/blob/b17039bccc17b94a2ea107272ad7bc93508708df/vllm/v1/worker/gpu_worker.py)）。
- S2：`config.json` 的 `architectures` 列表经模型注册表解析；无对应实现时抛出"Model architectures … are not supported for now"（含候选列表与近似名提示），历史上支持后移除的架构另有版本化报错；模型在注册表标记为无 vLLM 实现且允许回退时，会回退 Transformers 实现并打 warning（功能与性能可能受限）——对照实验中若看到该 warning，两实现的结果不可混排（[registry.py](https://github.com/vllm-project/vllm/blob/b17039bccc17b94a2ea107272ad7bc93508708df/vllm/model_executor/models/registry.py)）。
- S3：加载顺序为 `initialize_model`（架构解析＋量化配置注入）→ `load_weights`（按 loader 流式读权重）→ `process_weights_after_loading`（量化方法的重打包/重排、CPU offload 场景的设备往返、attention 权重后处理）→ `model.eval()`；**量化转换发生在权重读入之后**，因此"权重文件能读"不等于"量化配置可用"（[base_loader.py](https://github.com/vllm-project/vllm/blob/b17039bccc17b94a2ea107272ad7bc93508708df/vllm/model_executor/model_loader/base_loader.py)）。worker 侧入口带内存剖面与计时，LoRA、投机解码 drafter、EPLB 专家重排在主模型装载后依次进行；另有 `reload_weights` 原地重载路径用于权重热更新（[gpu_model_runner.py](https://github.com/vllm-project/vllm/blob/b17039bccc17b94a2ea107272ad7bc93508708df/vllm/v1/worker/gpu_model_runner.py)）。
- S4：profile run 与启动期内存判定（`gpu_memory_utilization` 默认 0.9、KV 容量不足 ValueError、约 150MiB CUDAGraph 冗余、`enforce_eager` 关系）已在[推理 OOM 诊断](ascend-inference-oom-triage.md)与本库 vLLM 既有登记固定，此处不重复；判定失败在服务暴露端口之前发生。
- S5：`/health` 的语义要分三层看。函数层：`check_health()` 只反映引擎错误标志（置位时 EngineDeadError → 503），它不重跑加载或 warmup，也不探测请求质量（[health.py](https://github.com/vllm-project/vllm/blob/b17039bccc17b94a2ea107272ad7bc93508708df/vllm/entrypoints/serve/instrumentator/health.py)）。入口层：标准 OpenAI 入口在引擎构建与应用状态初始化完成后才开始提供 HTTP 服务（`run_server` 的构建顺序），因此该入口下 `/health` 在启动序列完成前不可达；**legacy API server 是另一进程形态**，其 `/health` 无条件返回 200，只证明那个 HTTP 进程存活。判据层：即便探针 200，也不构成首请求成功或输出质量的证据——就绪判据用"启动序列完成＋确定输入请求成功"。gRPC 健康检查的语义同为"未出错"；uvicorn 的"Application startup complete"横幅属 uvicorn 标准行为，本库未单独取证，不作判据。

**MindIE（官方文档站 2026-10-20 快照）**：

- S1：`modelWeightPath` 指向的权重目录会被做属组与权限安全校验；服务化 `config.json` 自身要求权限 640；`npuDeviceIds` 用芯片逻辑 ID（受 `ASCEND_RT_VISIBLE_DEVICES` 影响的编号口径）；`worldSize` 必须与实际使用的 NPU 数相等。
- S2：引擎读取权重目录 `config.json` 的 `torch_dtype` 与 `vocab_size` 字段——官方要求这两个字段与路径存在；**字段值与权重实际不符会在哪个阶段失败，文档未证实（unknown，需日志或实现核对）**；`trustRemoteCode` 默认 false。
- S3：权重文件格式的硬性要求（是否仅 safetensors、其他格式如何转换）官方快速入门未逐字声明，本库标 unknown；社区 FAQ 提及非 safetensors 权重需人工转换，但论坛帖不作为本库证据。
- S4：算子编译在服务启动目录生成 `kernel_meta` 系目录——`bin` 目录按安全要求为 550 只读，**必须在当前用户可写的目录拉起服务**，否则算子编译写入即失败；容器场景 `--device` 挂载须为 `rwm`：`rw` 时进入容器与一般业务可能正常，但被占用卡上 `npu-smi` 报错且 `torch.npu.set_device()` 失败（Atlas 800I A3 上 rw 必现）；`--shm-size` 随数据并行度增大（文档给出 DP=2/4/8/16 对应至少 2/3/5/9g）。切换执行用户后文档示例会清理 `/dev/shm` 下旧用户创建的共享文件（属组不符会导致推理失败）——该示例属特定容器部署语境的**有状态变更操作**，沿用前须确认服务确已停止、目标命名空间与文件归属、无其他消费者且具备既有授权，只处理已识别的本实例遗留对象（见"停止条件与恢复安排"）。容器内组件栈（CANN、CANN-NNAL-ATB、MindIE、ATB Models）路径与 whl/run 两种安装形态的路径差异见来源登记。
- S5：标准输出出现 **`Daemon start success!`** 是官方声明的启动成功标志（看到它即可判定启动成功——充分条件）；**未观察到该行只说明"就绪尚未证实"**（日志缺失、未采集与服务确实未就绪是三种情形），须结合实际请求与日志完整性判断，不能反推"必然无服务"。验证用确定输入的 `POST /generate` 请求返回文本。

**ROCm（AMD）侧**：vLLM 无预编译 ROCm wheel，须源码编译（文档并声明 `pip install .` 对 ROCm 不可用），官方推荐 docker（`rocm/vllm`）；ROCm 6.3+ 配 torch 2.8.0+，MI350 需 ROCm 7.0+，**Ryzen AI MAX / AI 300 系列需 ROCm 7.0.2+**；支持 gfx90a/942/950、Radeon gfx1100/1101/1200/1201、Ryzen AI gfx1151/1150。Feature x Hardware 矩阵给出 ROCm 行的特性支持（chunked prefill/prefix caching/LoRA/speculative decoding/CUDA graph/multimodal 为 ✅，encoder-decoder 与 async output 为 ❌），但**矩阵不覆盖加载格式与量化方法**——ROCm 上某 load-format 是否可用只能按引擎实现与实测取证，不能从"支持 safetensors"这类通用格式名推断（[GPU 安装页](https://docs.vllm.ai/en/v0.14.0/getting_started/installation/gpu/)、[Feature x Hardware](https://docs.vllm.ai/en/v0.14.0/features/)）。

### 与 KV 加载的边界

权重加载（S3）建立模型参数；KV 缓存容量在 S4 判定、条目在首个 prefill 请求时才建立——"启动成功"不预置任何请求级 KV 状态。PD 分离部署中预填充到解码的 KV 交接是另一条链（见[PD 分离](pd-disaggregation.md)），不在启动判据内。

## 权重格式与分片

### vLLM 的 load-format 分派

v0.14.0 内置 14 种 load-format 名称，分派关系分三组：映射到默认 loader 的有 `auto`/`hf`/`safetensors`/`fastsafetensors`/`mistral`/`npcache`/`pt` 七种；`dummy`、`bitsandbytes`、`gguf`、`runai_streamer`、`tensorizer` 各有专用 loader 类；`runai_streamer_sharded` 与 `sharded_state` 同映射 ShardedStateLoader。未注册的名称在 **loader 查询时**（`get_model_loader`）报 ValueError，配置层只做小写归一——这是为 `register_model_loader` 注册自定义 loader 留出的口子，"14 种"因此不是封闭全集。默认 loader 的文件选择按格式给出匹配模式，且 **`auto` 并非无条件等同 `hf`**：目录中存在 `consolidated*.safetensors`（mistral 官方格式）时自动改走 `mistral` 分支；`hf`/`auto` 匹配 `*.safetensors` 与 `*.bin`（部分量化模型以 `.pt` 存权重）；`safetensors`/`fastsafetensors` 仅 `*.safetensors`；`mistral` 匹配 `consolidated*.safetensors`＋`consolidated.safetensors.index.json`；基础模式之上另有 `fall_back_to_pt` 与模式覆盖项影响最终文件集。分片与合并 safetensors 并存时，引擎会下载索引文件做去重，避免同时加载两份导致键重复（[model_loader/__init__.py](https://github.com/vllm-project/vllm/blob/b17039bccc17b94a2ea107272ad7bc93508708df/vllm/model_executor/model_loader/__init__.py)、[default_loader.py](https://github.com/vllm-project/vllm/blob/b17039bccc17b94a2ea107272ad7bc93508708df/vllm/model_executor/model_loader/default_loader.py)）。

与训练侧的衔接：`sharded_state` 格式按 `model-rank-{rank}-part-{part}.safetensors` 模式读取 vLLM 自有保存脚本产出的分片（支持 s3 路径）；该模式与训练框架的 checkpoint 目录结构不同，**跨 TP/PP 规模直接重分片加载的能力未从源码证实**，world size 或并行度变化时的装载须按保存侧口径另行验证。非推理文件（`optimizer.bin`、`scheduler.pt`、`scaler.pt`、`training_args.bin` 等）在文件筛选阶段被排除，不进入装载。

### TP/PP 装载机制与 dtype 的三层含义（以固定 commit 实现为限，不外推全部模型/平台）

- **普通 HF 格式的重分配发生在读取映射层**：模型实现为参数声明各自的 `weight_loader`，打包参数（如 fused QKV）在装载时按目标 shard 拆分映射；PP 布局下每个 stage 只装载自己拥有的层，缺失层在映射时跳过（以固定 commit 的 [llama.py weight_loader](https://github.com/vllm-project/vllm/blob/b17039bccc17b94a2ea107272ad7bc93508708df/vllm/model_executor/models/llama.py) 为样板；量化方法的打包参数依赖对应 quant 方法的专用 loader）。
- **`sharded_state` 要求文件按保存时的 TP rank 预分片**：loader 用**当前** TP rank 匹配 `model-rank-{rank}-part-*.safetensors`，匹配不到分片直接报错"仅支持预分片 checkpoint"（[sharded_state_loader.py](https://github.com/vllm-project/vllm/blob/b17039bccc17b94a2ea107272ad7bc93508708df/vllm/model_executor/model_loader/sharded_state_loader.py)）——保存侧记录的并行配置是该格式可读性的前提，也是"跨并行重分片 unknown"的具体含义。
- **dtype 是三层概念**：权重文件头记录的 dtype、装载时由 `model_config.dtype` 指定的目标 dtype（经 `set_default_torch_dtype` 上下文生效）、平台的硬件 dtype 支持检查（`check_if_supports_dtype`）互相独立，任一层通过不能代替另一层。

### 制品格式基线（safetensors）

safetensors v0.7.0 格式为 8 字节头长＋JSON header（仅 `dtype`/`shape`/`data_offsets`/`__metadata__` 字段）＋连续数据区；**格式本身无校验和字段**，跨文件分片索引（`model.safetensors.index.json`）的语义属 HF/transformers 侧，vLLM 只做索引下载与文件去重。"文件是 safetensors"只说明容器格式，键名/形状与模型实现的匹配由引擎装载阶段判定（[safetensors v0.7.0](https://github.com/safetensors/safetensors/tree/v0.7.0)；完整性语义另见[数据与制品完整性证据](../04-data-storage/checkpoint-integrity-evidence.md)）。

### 引擎×格式支持不能互推

三条引擎线各自取证：vLLM 的格式集合如上；vllm-ascend 线的装载行为以其固定 commit 为准（本页不展开）；MindIE 的格式要求官方未逐字声明（unknown）。任何"引擎 A 支持 X 格式"的表述都必须锚定引擎与版本；从格式名（safetensors/GGUF/…）或安装文档推断全部引擎支持是本库明确禁止的推断。

## 模型身份固定清单

对照实验、故障复盘与升级验证共用同一张身份表；在装载前固定，装载失败时它也是"到底试图加载什么"的证据。

| 身份维度 | 固定内容 | vLLM/MindIE 取证点 |
|---|---|---|
| 目录内容 | 实际选用的权重分片、索引、config、tokenizer/模板等输入的**内容摘要或可追溯的不可变制品身份**（记录算法与覆盖范围；文件清单/大小只是最低限度，同名同大小而数值不同的目录不能凭清单判同） | S1 阶段的路径与权限证据；摘要工具与口径属现场 |
| 模型结构 | `config.json` 的 `architectures`、`torch_dtype`、`vocab_size`、量化配置字段 | vLLM 架构解析报错形态；MindIE 明确读取 `torch_dtype`/`vocab_size` |
| tokenizer | tokenizer 文件身份（不可变 revision 或内容摘要）、`tokenizer_mode`、fast/slow | vLLM tokenizer 注册表：`auto` 切 `mistral` 须同时满足装 `mistral_common` 且文件匹配 `tekken.json`/`tokenizer.model.v*`；慢 tokenizer 有显著性能警告 |
| 参数抽样 | 首尾若干参数的 key 与 shape（与结构声明比对） | 装载阶段的键/形状不匹配报错 |
| 平台与工具 | 引擎版本/commit、后端插件版本、驱动与运行库、容器镜像摘要 | 本库来源登记的固定 ref 即为此用 |

tokenizer 解析在 vLLM 中独立于权重装载（`get_tokenizer` 走 HF/ModelScope 与模式注册表），两者可分别失败：权重装载成功而 tokenizer 模式错误的组合存在，排查时不要互证。模式选择有文件条件：`auto` 切到 `mistral` 需要**同时**满足安装了 `mistral_common` 且当前 tokenizer 名称/revision 对应文件中存在 `tekken.json` 或 `tokenizer.model.v*`（另有匹配 `tokenizer.tok.json` 的 tiktoken 分支）；对象复用缓存发生在缓存包装入口（`cached_get_tokenizer`），直接调用 `get_tokenizer` 不共享该契约（[tokenizers/registry.py](https://github.com/vllm-project/vllm/blob/b17039bccc17b94a2ea107272ad7bc93508708df/vllm/tokenizers/registry.py)）。

## 首失败边界分类

| 类别 | vLLM 证据 | MindIE 证据 | 排查要点 |
|---|---|---|---|
| 文件/权限 | 路径不存在、下载失败、格式筛选后无文件 | 权重目录属组/权限校验失败；config.json 权限非 640；不可写目录中算子编译失败 | 先核 S1/S2，再谈内容 |
| 模型识别 | 架构不支持 ValueError（含候选提示）；Transformers 回退 warning | `torch_dtype`/`vocab_size` 缺失或读取失败 | 回退实现的结果不与原生实现混排 |
| 权重内容 | 未知 load-format ValueError；键/形状不匹配；分片索引错误 | 官方未逐字声明（unknown） | 格式名≠支持；按引擎版本取证 |
| 量化条件 | 未知量化方法 ValueError；量化处理在装载后（重打包失败晚于读取） | 量化矩阵见模型支持列表（W8A8/W4A8/W8A16 按模型分级） | 量化可用性看引擎×模型×硬件三方，见[量化与质量](quantization-and-quality.md) |
| 设备内存 | 启动期内存判定失败、KV 容量不足 ValueError | 文档未给启动内存判定的统一报错形态（unknown） | 见[推理 OOM 诊断](ascend-inference-oom-triage.md) |
| 平台/挂载 | ROCm 源码编译失败面；gfx 架构不匹配 | device 挂载 rw（非 rwm）时 `npu-smi` 报错且 `torch.npu.set_device()` 失败；`/dev/shm` 跨用户残留 | 平台层失败常伪装成引擎失败，先看设备与挂载 |
| 探针/假就绪 | `/health` 200 但首请求失败（死活探针语义） | 未观察到 `Daemon start success!`——就绪尚未证实（须结合日志完整性与实际请求判断，不能反推无服务） | ready 判据用启动序列完成＋确定输入请求，不用探针单独证明 |

## 小模型验证计划（三平台样板）

以下为验证设计，本库未执行；每平台按同一骨架，只替换引擎与后端样板。

**共同骨架**：

1. **固定身份**：按上表记录目录、结构、tokenizer、参数抽样、版本五元组；此记录同时是失败复盘的基线。
2. **最小加载**：用小模型（参数量级以显存/内存宽裕为准）走完整启动序列，记录 S1–S5 各阶段的官方成功标志或日志锚点；不跳过 warmup。
3. **ready 判定**：以启动序列完成的官方标志（vLLM：服务监听且无错误标志；MindIE：`Daemon start success!`）**加上**一条确定输入请求成功为准；health 探针只作辅助观察。
4. **输出质量**：固定 prompt 与采样参数（温度 0 或确定性配置），记录首 token 与完整输出。质量判据必须锚定**明确的参考输出或任务指标与阈值**（口径见[量化与质量](quantization-and-quality.md)：固定任务、指标、baseline 与样本量）；tokenizer 重编码一致性只是输入输出管线的独立自检——错误权重产生的可编码文本也可能自洽，不能单独作为质量通过的证据。三平台计划须先记录模型选择、确定输入、采样/模板、参考来源与判定字段；未取得参考时该项标为计划缺口，不伪造参考输出，也不要求跨硬件逐 token 完全相同。
5. **失败清理**：按引擎语义终止进程，确认设备内存回收并记录清理后空闲证据；涉及共享内存文件时（MindIE 场景），先确认服务确已停止、目标容器/IPC 命名空间与文件归属、无其他消费者且具备既有授权，只清理已识别的本实例遗留对象——这是有状态变更操作而非只读诊断，上游示例的通配删除不作为未限定环境的通用处方。
6. **重试一次**：同一环境重复加载，验证结果可重复且资源状态回到基线；不可重复本身就是发现。

**平台样板替换**：

- NVIDIA：vLLM v0.14.0 上游语义即本文档取证口径；引擎从 wheel/容器安装。
- AMD：同一 vLLM 版本按 ROCm 安装文档走 docker（`rocm/vllm`）或源码编译样板（MI300/gfx942 为文档示例架构）；预期安装阶段本身是一类失败面。
- Ascend：MindIE 官方快速入门样板（Atlas 800I A2 容器路径、`config.json` 字段、`mindieservice_daemon` 拉起）；vllm-ascend 线按其固定 commit 另行设计，不与 MindIE 混排。

**判据与停止条件**：步骤 3 或 4 失败即停止并按首失败分类定位，不叠加其他变更；同一样板连续两次不可重复时，怀疑环境身份漂移（驱动/镜像/tokenizer 变化），回到步骤 1 重核身份后再试。验证通过只覆盖该次记录的组合，不外推版本或机型。

## 停止条件与恢复安排

- 任一阶段报架构不支持、量化不支持或格式不支持时停止：这类是能力边界，不是故障，改配置重试只会掩盖证据。
- 探针 200 而首请求失败：停止扩容/放量，先按假就绪处理——核对启动序列日志是否完整、错误标志是否置位。
- 装载中途失败后的重试：先确认设备资源已回收；MindIE 场景的跨用户 `/dev/shm` 残留共享文件是文档明确的失败源，按"失败清理"步骤的限定（停妥、归属、无他者、授权）处理后再重试，否则重试结果不可信。
- 本页操作均为只读诊断或服务自身生命周期；不涉及对其他租户的设备操作。

## 完成判据

一次启动验证完成须同时满足：身份五元组已记录，且权重/config/tokenizer 等装载输入有内容摘要或可追溯的不可变制品身份（无法取得时显式记缺口，不宣称身份已固定）；启动序列各阶段标志达成（或失败阶段已定位并分类）；ready 判据（序列完成＋确定输入成功）成立；清理后设备状态回到基线；全程无证据缺口。装载成功与输出质量正确是两个判据，分别记录；仍有 unknown 的项（如 MindIE 权重格式硬性要求、字段不一致的失败阶段）如实保留，不因启动成功而回填。

## 来源与验证记录

- vLLM v0.14.0 固定 commit `b17039bc`：[loader 分派](https://github.com/vllm-project/vllm/blob/b17039bccc17b94a2ea107272ad7bc93508708df/vllm/model_executor/model_loader/__init__.py)、[加载顺序](https://github.com/vllm-project/vllm/blob/b17039bccc17b94a2ea107272ad7bc93508708df/vllm/model_executor/model_loader/base_loader.py)、[文件选择与去重](https://github.com/vllm-project/vllm/blob/b17039bccc17b94a2ea107272ad7bc93508708df/vllm/model_executor/model_loader/default_loader.py)、[架构解析报错](https://github.com/vllm-project/vllm/blob/b17039bccc17b94a2ea107272ad7bc93508708df/vllm/model_executor/models/registry.py)、[health 探针](https://github.com/vllm-project/vllm/blob/b17039bccc17b94a2ea107272ad7bc93508708df/vllm/entrypoints/serve/instrumentator/health.py)、[tokenizer 注册表](https://github.com/vllm-project/vllm/blob/b17039bccc17b94a2ea107272ad7bc93508708df/vllm/tokenizers/registry.py)。
- vLLM v0.14.0 文档：[GPU（AMD ROCm）安装](https://docs.vllm.ai/en/v0.14.0/getting_started/installation/gpu/)、[Feature x Hardware 矩阵](https://docs.vllm.ai/en/v0.14.0/features/)（矩阵不覆盖加载格式/量化）。
- MindIE 官方文档站（2026-10-20 取回，latest 未定版）：[模型支持列表](https://mindie-llm-doc.readthedocs.io/zh-cn/latest/user_guide/model_support_list/)、[快速入门](https://mindie-llm-doc.readthedocs.io/zh-cn/latest/user_guide/quick_start/quick_start/)；开源仓 master@69e5a5dd（MindIE 软件 2.3.0↔CANN 8.5.0 配套表）。
- safetensors [v0.7.0](https://github.com/safetensors/safetensors/tree/v0.7.0)（格式基线：无校验和字段）。
- 当前验证范围：仅源码与文档语义核对（锚点与 SHA-256 见 [batch-26-t07-01-sources](../../docs/research/batch-26-t07-01-sources.md)）；未运行任何引擎、加载或探测命令。
- 待确认：MindIE 权重文件格式的官方硬性要求；MindIE 启动期内存判定报错形态；vLLM `sharded_state` 跨并行重分片能力；ROCm 各 load-format 的实际可用集；vllm-ascend 线装载行为（待 T07-03 深化）。
