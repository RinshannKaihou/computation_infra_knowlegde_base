# Batch 28 · T07-11 初审报告

## 会话元数据与结论

| 项目 | 记录 |
|---|---|
| 审阅角色 | 独立批次审阅者；本会话未编写或修订被审正文 |
| 实际执行模型 / 推理档位 | `gpt-6.1-sol / xhigh` |
| 模型核验 | 读取当前本地会话 JSONL 的 `session_meta` 与全部 `turn_context`；模型/档位组合仅有 `gpt-6.1-sol / xhigh`，assistant 消息未检出 `[frontier_llm]` 回退标记；未另启模型或子代理 |
| 会话 ID | `01a15d60-4479-7dd2-bc81-3f9311fddff9` |
| 执行方式 | 本地 Codex CLI，`originator=codex_exec`、`source=exec`、CLI 0.163.0；直接读取源码缓存与仓库文件 |
| 日期 / 时区 | 2026-10-21 / Asia/Shanghai |
| 工作目录 | `/Users/ywang2397/work/AI_reliability_knowledge_base` |
| 审阅正文 | `knowledge/07-inference/gpu-inference-oom-triage.md`，113 行 |
| 正文 SHA-256 | `c9f1642583bff307b2f2065d750e83a6ba5fc9d1c30c6b211d6ce3a4dca9ee7e` |
| 作者取证记录 SHA-256 | `bd431e12059a6068f311f035be26d0134fa9d9307c505aa54e19f157bfea2aa3` |
| 写入范围 | 仅新增本报告；不修改正文、作者取证记录、registry、导航、任务状态或历史审阅记录。构建在临时源码副本执行 |

**初审结论：需修订并定向复核，暂不通过。** 共 11 项开放发现：0 P1、8 P2（C01–C08）、3 P3（C09–C11）。四类错误的主要分层、启动链主干与不迁移昇腾字段的原则已有依据；请求错误示例、启动容量处置、阶段判别细节、ROCm 取证和恢复闭环仍影响验收。

沿用仓库口径：P1 为严重误导处置的关键错误；P2 为影响技术准确性、适用边界或验收完整性的必修项；P3 为措辞、定位和追溯问题。正文行号绑定上述指纹；上游行号均为原文件坐标。报告落盘不等于发现关闭。

## 范围与方法

先读 `README.md`、`docs/authoring-guide.md`、`AGENTS.md`、`schemas/content.schema.json`，再按 `content-outline.md` 核对 02/07 域分工。逐项对照 [T07-11 任务与五条 acceptance](../../plans/full-coverage-backlog.yaml) L6687–6707，重读[正文](../../knowledge/07-inference/gpu-inference-oom-triage.md)、[作者取证记录](batch-28-t07-11-sources.md)及 [07 域导航](../../knowledge/07-inference/index.md)。

核对 [registry](../../sources/registry.yaml) 中 `src.vllm.inference-v0-14` 的 Batch 28 与第九批历史 notes、`src.vllm.rocm-install-doc-v0-14`、正文列出的四项 PyTorch memory/allocator 登记、`src.pytorch.hip-notes-2.6`、`src.amd.pytorch-rocm-fork`、NVIDIA SMI 与 AMD SMI 指定登记。沿链接和 related ID 对照昇腾 OOM、发布恢复、路由、执行/KV、加载/ready、GPU/昇腾内存证据、GPU 图失败诊断、AMD 配套档案和昇腾长尾页；关联页只用于边界与导航核对，不作新的整篇验收。

工作区已有其他任务的修订和报告；本轮未改动这些文件。发布恢复页按本轮重读版本使用，SHA-256 为 `a3c16f4c1eaffd9855a941ca5063d3507e5a69eb5a1430a1447804695b574b69`；不把该页存在或已修订当作 T07-11 的问题已关闭。

独立计算给定缓存指纹，并与 `/tmp/vllm-b17039bccc17b94a2ea107272ad7bc93508708df/` 的既存完整源码缓存交叉比较，以下六份文件全字节相同，哈希前缀与作者记录一致：

| `/tmp/b28/vllm/` 文件 | SHA-256 前 16 位 |
|---|---|
| `utils.py` | `c0758a66a105e72e` |
| `gpu_worker.py` | `eb33b5f2bd389ac3` |
| `core.py` | `a7a624e0ed151f00` |
| `core_client.py` | `601d375067fa724e` |
| `conserving_memory.md` | `895bc42beb0ff505` |
| `troubleshooting.md` | `dc679401e1078852` |

从上述完整缓存补读以下文件，均按其目录标识的同一固定 commit 核对；本轮未独立重取该源码归档或解析远端 tag：

| 补充文件 | SHA-256 前 16 位 | 核对点 |
|---|---|---|
| `vllm/v1/core/kv_cache_utils.py` | `208abc23e1cbaebe` | L609–645 两个 KV 容量 ValueError 分支 |
| `vllm/v1/worker/gpu_model_runner.py` | `7eaa9eb78cb99f9f` | dummy/profile 请求规模、sampler OOM、图捕获测量 |
| `vllm/platforms/rocm.py` | `b7fcec9a5263d8f9` | `torch.cuda` 分发、设备变量、默认 worker；与 T07-06 历史取证指纹一致 |
| `docs/configuration/optimization.md` | `b3aac342f2435e22` | 抢占重算、chunked prefill、gmu 调整方向 |
| `docs/getting_started/installation/gpu.rocm.inc.md` | `3f0c7129c7e08347` | ROCm / torch 安装边界；与 T07-06 历史取证指纹一致 |
| `vllm/v1/executor/abstract.py` | `706b38531d30b04b` | KV 实际初始化在 compile/warmup RPC 前 |

另读取同批缓存 `vllm_config_scheduler.py` L249–267、`vllm_entrypoints_openai_serving_engine.py` L1065–1085、`vllm_v1_core_sched_scheduler.py` L349–405/L800–819；读取完整缓存 `uniproc_executor.py` L47–48、`compilation/cuda_graph.py` L185–192/L285–308。HIP 文档使用既存 `/tmp/b24-t063-s3.AfgWGe/hip-2.6.html`，HTML 标题为 PyTorch 2.6，SHA-256 为 `c544cb55f21a9578a4239114ef5b905286e1b1a763c1f2280a9ef2a2ead522f8`；独立检查接口复用、HIP 判别、Memory management 与 hipBLAS workspaces 小节。

**网络限制**：尝试打开固定 commit 的 `kv_cache_utils.py`、PyTorch HIP、AMD SMI 固定版 CLI 与 NVIDIA SMI 精确 URL，网页工具返回 HTTP 429；GitHub 连接器不可用，备用只读 HTTP 请求因域名解析失败未取得 HIP 页。故本轮为缓存原文独立核对加登记记录交叉核对，不能记作本轮已重新下载远端证据。尤其 SMI 的现场字段/版本，本轮不据既有登记宣称已独立重取全文。网络失败本身不计为作者错误。

## 已核实的主干与边界

| 对象 | 结果 |
|---|---|
| 四类错误与精确锚点 | `utils.py` L253–273 的启动预算检查、`kv_cache_utils.py` L609–645 的 KV 检查、`core.py` L927–943 的启动/运行异常分支、`core_client.py` L425–428 的死亡标记传播均与链接坐标相符。EngineDead 不独立证明 OOM 或阶段的主张可保留；请求错误行见 C01。 |
| 启动顺序与历史缓冲 | request_memory 早于权重加载，随后 profile、KV 配置、warmup/图捕获，主顺序正确；缺少实际 KV 分配边界，见 C03。第九批 notes 已更正：150MiB 是 warmup 后 KV 配置建议日志的经验缓冲，非 `determine_available_memory` 固定减项，图内存另测。本正文没有重新把 150MiB 加入 profiling 公式。 |
| 抢占重算与 OOM | 固定 V1 文档 L8–28 支持 KV 压力可触发抢占重算、默认 RECOMPUTE 及延迟代价；scheduler 缓存支持释放并重新排队的实现。不能把这类事件单独认作 allocator OOM。“warning”应保留为文档给出的可能观测，不要求每次抢占必有同一条 warning；本次未发现必须以 OOM 解释抢占的倒置。 |
| 两个“修复”的边界 | L84 与 02 域内存页 L98 的表述一致：`empty_cache()` 不能清掉仍被持有的张量/workspace/graph 资源；重启成功不建立根因结论。02 域 F2 的对象处理、同步、采样、复跑与持久爬升核对尚未在本文形成操作闭环，见 C08。 |
| 同构、不互迁 | L45/L103 明确不迁移 NPU 配置变量、NPUWorkspaceAllocator 与 EL0004；GPU workspace/graph 已含在 allocator aggregate 的说法与 02 域一致，没有照搬 NPU 独立 workspace 账户。L80 引用 Ascend block_size 时仍应保留姊妹篇的条件与 qwen3_next 例外，不把“默认/强制 128”读成无例外规则。 |
| 元数据、导航 | `procedure` 必填字段完整；`draft / source_checked`、空环境档案和未运行验证的声明符合 schema。10 个 source ID、7 个 related ID 均可解析。正文 16 处本地内联链接、7 个唯一目标均存在；07.8 行、场景表 GPU 行及已有正文入口有效。部分要求的对照页尚无正文链接，见 C11。 |

## 发现清单

### C01 · P2 · 请求级错误误用 batch token 上限，且被无条件排除为服务故障

- **位置**：正文 L54；取证记录 L24 与四类错误表的对应范围。
- **证据**：固定 [scheduler.py L249–267](https://github.com/vllm-project/vllm/blob/b17039bccc17b94a2ea107272ad7bc93508708df/vllm/config/scheduler.py#L249-L267) 在未启用 chunked prefill 且 token 预算小于模型长度时做**启动配置校验**；这不证明逐请求按 `max_num_batched_tokens` 拒绝超长输入。实际普通 completion/chat 输入验证以 `max_model_len` 和输入/输出 token 合计为边界（[serving_engine.py L1065–1085](https://github.com/vllm-project/vllm/blob/b17039bccc17b94a2ea107272ad7bc93508708df/vllm/entrypoints/openai/serving_engine.py#L1065-L1085)）；启用 chunked prefill 时，超过每轮 token 预算的 prefill 可分块（optimization L30–34）。此外 400、取消与超时属于不同原因链，单请求的错误观测不证明服务健康；持续超时仍可能来自容量或引擎故障。
- **建议**：分别写输入验证、主动取消/断连、deadline/代理超时的证据与转诊条件；把启动配置 ValueError 放回启动链。将“不是什么”改为单个请求状态不单独证明 allocator OOM、也不单独证明或排除副本故障。
- **关闭条件**：请求表不再把 batch 预算当通用输入拒绝阈值；能将请求错误与同窗服务/引擎证据关联，既不一概升级，也不一概排除服务问题。

### C02 · P2 · 启动容量支路的处置被绝对化，并遗漏手工 KV 预算分支

- **位置**：正文 L52、L58/L69、L76、L80–81、L103；取证记录 L23/L26。
- **证据**：“改并发救不了它”把启动检查和 KV 可用预算计算合为一条禁令。request_memory 本身确不读取在线到达并发，但启动配置 `max_num_seqs` 会影响 dummy/profile 规模（[gpu_model_runner.py L4281–4308](https://github.com/vllm-project/vllm/blob/b17039bccc17b94a2ea107272ad7bc93508708df/vllm/v1/worker/gpu_model_runner.py#L4281-L4308)、L4693–4755）；不能据此排除降低批规模对 profiling 与后续可用预算的影响。两种预算检查的 gmu 方向也不同：utils L262–270 建议降低目标比例或减少他进程占用，KV 检查 L615–642 则建议提高 gmu，或在相应分支降低模型长度。正文只写“调 gmu”，没有按错误分支给方向。更重要的是 [gpu_worker.py L295–313](https://github.com/vllm-project/vllm/blob/b17039bccc17b94a2ea107272ad7bc93508708df/vllm/v1/worker/gpu_worker.py#L295-L313) 的显式 `kv_cache_memory_bytes` 分支仍运行 profile，但 KV 预算直接采用指定值，不按 profiling 结果套用 L80 公式。
- **建议**：区分在线负载并发与引擎批规模配置；将 request_memory、profile、非正 KV 预算、单请求最大长度不足分列。记录显式 KV 字节配置及最终生效值；公式注明适用的自动预算路径，方向调整按首错与现有空闲量约束决定。
- **关闭条件**：不再统一宣称改并发无效或不分方向调比例；手工预算不被自动公式覆盖，不承诺任一参数一定修复问题。

### C03 · P2 · 五步启动链漏掉实际 KV 分配，运行期阶段仍只有名称

- **位置**：正文 L65、L75–80、L98；acceptance 1。
- **证据**：当前第④步只有容量计算，第⑤步直接进入 warmup；但 [core.py L254–270](https://github.com/vllm-project/vllm/blob/b17039bccc17b94a2ea107272ad7bc93508708df/vllm/v1/engine/core.py#L254-L270) 在生成配置后调用 executor，后者依次发 `initialize_from_config`、`compile_or_warm_up_model` RPC（[abstract.py L110–116](https://github.com/vllm-project/vllm/blob/b17039bccc17b94a2ea107272ad7bc93508708df/vllm/v1/executor/abstract.py#L110-L116)），worker L398–415 才实际创建 KV。容量 ValueError 与该分配过程中可能出现的 allocator OOM 不能并成同一类。此外运行期只有一个“查内存账”的分支，未说明如何以请求/迭代证据区别首次 prefill、后续 decode 与混合并发。未启用 chunked prefill、启用后与 decode 混批两种情形也未分开；profiling 本身可执行编译，不能把全部编译错误都排到第⑤步。
- **建议**：保留五步主序，在第④步内明确“容量/配置→实际初始化”及各自错误；给运行期增加请求 ID、输入/已计算 token、输出进度、该轮调度形态和失败栈的记录项。区分单请求阶段与同轮混合 batch，无法拆开则保留 unknown；指向加载/ready 和执行/KV 页。
- **关闭条件**：读者能区分 KV 检查失败与 KV 分配失败；prefill/decode/并发阶段有实际可收集的判别证据，而非只出现在摘要与完成判据中。

### C04 · P2 · profiling 断言被写成对所有共享显存变动的检测

- **位置**：正文 L76；取证记录 L23。
- **证据**：[gpu_worker.py L329–339](https://github.com/vllm-project/vllm/blob/b17039bccc17b94a2ea107272ad7bc93508708df/vllm/v1/worker/gpu_worker.py#L329-L339) 实际要求初始化 free **大于** profile 后 free；只有终值大于等于初值才失败。他进程释放显存若未抵消本进程增长，不必触发；他进程增加占用也不会被该断言直接识别。因此“他进程变动会触发显式断言”扩大了实现能力；通过断言也不证明共享占用不变。异常文本举同容器释放显存为解释，不代表跨容器共享 GPU 不会干扰。
- **建议**：照录实际比较关系，解释释放/新增占用均可能干扰测量，但此断言只捕获部分形态；独占性和同窗进程读数另行证明。
- **关闭条件**：正文与取证表均不再把断言当通用共享干扰检测器；无断言不用于排除干扰。

### C05 · P2 · eager 对照被直接判为容量根因，reserved 回落被写成正常保证

- **位置**：正文 L78；取证记录 L25、unknown 2。
- **证据**：troubleshooting L78–81 针对 graph replay 附近的 CUDA 错误建议用 eager 隔离具体操作，不专指显存容量；conserving_memory L48–76 另支持减少捕获规模/关图降低内存。两页合起来仍不支持“eager 后消失→图捕获容量问题”的唯一归因。`capture_model` 在结束时测 free 差值作为图占用（[gpu_model_runner.py L4838–4862](https://github.com/vllm-project/vllm/blob/b17039bccc17b94a2ea107272ad7bc93508708df/vllm/v1/worker/gpu_model_runner.py#L4838-L4862)），wrapper 保持 graph 用于 replay；02 域也明确区分 graph 活跃量与保留高水位，不能给出 capture 后 reserved 必然回落的形态保证。作者尚将 capture workspace 路径列为未核。
- **建议**：eager 生效仅支持问题与原图/编译执行路径有关；结合首个 OOM 文本、请求字节数、同窗分配记录和捕获规模对照再支持容量解释。分别记录 current/peak、active/reserved 与阶段，不把保留量持续存在直接判异常，也不预期必然回落。
- **关闭条件**：删除唯一归因箭头和无来源的回落保证；图内存已核范围与 workspace 未核范围一致，继续不外推 CUDA 图结论到 HIP 图实现。

### C06 · P2 · ROCm 仍是工具名索引，缺少各自字段与版本证据的可执行对照

- **位置**：正文 L31、L58、L66–69、L88–90；取证记录 L27–28/unknown 1；acceptance 2。
- **证据**：L89 用“观测字段换套”概括，却未明确 HIP 仍复用 `torch.cuda` 名称、如何判别构建，也未落到 AMD 的 allocator 与进程显存取证列。[HIP 2.6 文档](https://docs.pytorch.org/docs/2.6/notes/hip.html#memory-management)直接列有 allocated/reserved/current/peak、memory_stats/snapshot；接口复用和 `torch.version.hip` 在同页相应小节，hipBLAS workspace 也有已知边界，不应全部混入 AITER/MIOpen unknown。02 域已给 `list_gpu_processes` 的 CUDA `usedGpuMemory` / ROCm `vram_mem` 分支及来源工具列，可复用但不直接对齐数值。与此同时本文固定的 vLLM ROCm 安装文档要求 torch 2.8+，分配器证据却是 2.6；两者可作为不同资料样板，不能被 L31 的“＋”和“两平台一致”概括成已核部署组合或全部分支的同一行为。`rocm.py` 默认 worker 确实共享 gpu_worker（L443–444），但有 auto 等配置前提。
- **建议**：给 CUDA/HIP 分别填写采集 API、字段、单位、进程/设备身份、backend、同步窗口和缺失处理；明确 HIP 的共享接口名与独立运行时/SMI 口径。将 PyTorch 2.6 语义参考、vLLM 支持下界和目标实际 torch/HIP 构建分列；后者字段与选项集合待目标版本复核，不合成已支持组合。已核 hipBLAS 与未核 MIOpen/AITER 分开。
- **关闭条件**：两平台均有可填写的字段表；HIP 选项支持集合、默认 backend、fork 差异和目标版本仍可保持 unknown，但不能用这些 unknown 替代已取得的 HIP 基础语义，也不能把 2.6 字段自动授予 vLLM 所需的 2.8+ 构建。

### C07 · P2 · 进程死亡被当作所有 KV、缓存身份和取消链均已清除

- **位置**：正文 L82；取证记录 L30；acceptance 5。
- **证据**：L82 无条件写 KV/请求/缓存身份随进程消失、重启必为冷 cache，并把“取消链已清”作为前提。EngineCore、API frontend、worker、connector/offload 与上游客户端不是同一个所有者。固定 async_llm 缓存 L455–459 的 EngineDead 分支不逐请求 abort，而是依靠整体关闭；本轮没有验证所有进程和外部组件均已退出。当前[发布与恢复](../../knowledge/07-inference/release-and-recovery.md) L76–77 已区分进程本地 KV 与外部/offload 缓存，且说明取消响应与资源归还不同；[执行/KV](../../knowledge/07-inference/execution-and-kv-cache.md) L82/L99 起列出缓存层级与身份条件。链接到这些页不能覆盖本文相反的绝对化判断。
- **建议**：仅对已终止所有者的本地活动状态说明不自动继承；外部缓存/远端 KV、旧 frontend 请求、重试 attempt 与已提交输出各自核对。记录模型/tokenizer/adapter/量化、token/block、隔离字段等身份与实际命中证据；无证据时 unknown，不以“重启”证明缓存必冷或取消已完成。
- **关闭条件**：正文和来源记录不再承诺全局清空；旧请求终态、重试身份、本地/外部缓存的生存与兼容条件可分别核查。

### C08 · P2 · 查询—终止—清理—再启动尚未形成闭环，完成判据可绕过恢复核对

- **位置**：正文 L75–82、L92–103；acceptance 3/5。
- **证据**：步骤 8 只有残留查询及 ready 后观察，缺少隔离目标流量、确认终止对象与分布式成员、等待退出/超时处理、对象清理与保留、同步采样、再启动准入的有序分支。L82 要求“显存账目归零”也没有限定对象：02 域 L59/L122 明确 SMI、运行时与框架口径不能直接互减，驱动/固件常驻和未测量项不等于零；应核对本实例残留与同条件基线。L96 的“任一”又允许仅定位阶段或列出 unknown 就结束整个状态恢复流程，与 L82/L103 的不关闭承诺冲突。持续稳定窗未给出预登记长度、基线、分母或超时终态。
- **建议**：添加按版本与部署形态待执行的子流程：保存现场/请求账→隔离流量→确认目标及退出范围→核对退出与残留→仅清理已识别且无其他消费者的本实例对象→采样对账→同身份重启、ready/确定输入与质量检查→同负载观察至预登记窗口。复用 02 域 F2 的窗口方法；不能逐项证明时保持 unknown 或不准回服，不提供臆造的一键清理命令。将“本轮诊断结束”与“恢复完成/允许接流”设为两组判据。
- **关闭条件**：四类错误均有查询与下一步处置或转诊；终止、清理、重启有对象/影响/超时分支；恢复必须同时满足无未解释残留、旧请求/缓存身份、ready、质量/SLO/错误与持续窗核对，不能以单个 OR 条件跳过。无需为关闭内容缺口实际操作服务。

### C09 · P3 · “官方清单”未交代选取范围，gmu 的来源归属不准确

- **位置**：正文 L81；取证记录 L26；registry vLLM Batch 28 notes。
- **证据**：缓存 conserving_memory 确实有 TP、量化、模型长度/批规模、图捕获；TP 读取全量再切分及分片 checkpoint 的说明是**加载 I/O 时间**注记，不是每 GPU 必驻全量权重。该页全文没有 gmu 调整条目；其依据在 request_memory/KV 错误建议及 optimization 的抢占节。该页还按适用范围给多模态输入数量/尺寸和 processor 配置，CPU RAM/cache 项则不能移作 GPU 显存处方。正文没有说明只选取了其中部分 GPU 项。
- **建议**：将该行标为按阶段选取的候选项，补精确节链接；说明 TP 注记的 I/O 归属。gmu 回链到各自证据（方向按 C02）；多模态适用时补候选或明确本轮清单仅覆盖所列负载，不混入 CPU-only 项。
- **关闭条件**：正文、来源表和 registry 摘要均能区分官方原有项、本库验证方法与清单取舍；不再把 gmu 归给不含该项的页面。

### C10 · P3 · 取证 ID、AMD SMI 版本 URL 与 unknown 清单未同步

- **位置**：取证记录 L28、L32–38；正文 L110/L113。
- **证据**：取证记录写 `src.pytorch.pytorch-rocm-fork`，登记与正文实际为 `src.amd.pytorch-rocm-fork`。正文 AMD SMI 链接为 `projects/amd-smi/en/latest/`，登记固定的是 [projects/amdsmi/en/docs-10.1.0/](https://rocm.docs.amd.com/projects/amdsmi/en/docs-10.1.0/index.html)，项目路径拼写和版本均不同；本轮受网络限制未判定前者 HTTP 状态，但不能当作同一固定来源。正文列出的 HIP allocator 选项集合和目标真实峰值未在作者 unknown 清单中分别列明；作者列出的 capture workspace 未核则与 L78 确定形态说法冲突（技术部分见 C05）。
- **建议**：修正来源 ID，按登记的固定项目/版本和具体 CLI/字段页引用；统一 unknown 清单，分别列部署组合、HIP 支持集合/默认 backend/fork diff、capture workspace、真实峰值及外部缓存/取消链等仍缺证据项。保留公开案例本轮未取、未运行引擎的事实。
- **关闭条件**：每条来源能按 ID 与精确版本回溯；正文、取证表和 unknown 清单覆盖一致，不把“登记过”或“缓存存在”写作本轮远端已核。

### C11 · P3 · 多个要求的对照页只有元数据入口，缺少正文可点击互链

- **位置**：正文 L21–28、L45/L76–89；姊妹篇与 07 域导航。
- **证据**：现有内联链接全部有效，07.8 和 GPU 场景行无断链；但 `execution-and-kv-cache`、`model-loading-and-readiness`、`amd-rocm-documented-profile` 只有 related ID，没有正文 Markdown 链接。02 域 GPU 内存页已链接，Ascend 内存页未给直接对照；图/编译失败也未转到既有 GPU 定向指南。昇腾 OOM 姊妹篇尚无反向 GPU 入口。读者无法从表内直接到达这些边界依据。
- **建议**：在对应阶段/平台行加加载/ready、执行/KV、AMD 档案链接；在不迁移账户/API 的说明中链接 02 域两篇内存证据，图类非 OOM 错误转 GPU 图失败指南；补姊妹篇反向入口。继续只链接，不复制正文。
- **关闭条件**：上述入口可从正文对应论断直接访问、反向对照可达，stable ID 不变；所有新增路径再通过本地链接检查。

## 五条 acceptance 逐项判断

| 验收项（任务原文范围） | 判断 | 已有依据与待关闭项 |
|---|---|---|
| 1. 按权重加载、profiling、KV 初始化、图/编译、prefill、decode、并发运行的首失败阶段定位 | **部分满足，需修订** | 启动五步主顺序与 EngineDead 阶段边界正确；C03 补实际 KV 初始化与运行期阶段证据，C04 修 profiling 条件，C05 修图分支解释。 |
| 2. 区分物理显存、allocated/reserved、workspace/KV、碎片和他进程；CUDA/ROCm 各自字段与 allocator 取证 | **部分满足，需修订** | 分账和禁单值确诊原则正确，GPU workspace/graph 不作为互斥账户相加；C06 补 HIP 已知接口、字段及版本分线，C04/C05/C08 修断言、图窗口和“归零”口径。 |
| 3. 区分 CUDA OOM、capacity ValueError、engine failure 与请求错误，依版本设计查询/终止/清理/再启动检查 | **部分满足，需修订** | 三组源码错误锚点准确；C01 改请求错误，C02 分容量预算路径，C08 补生命周期顺序与终态，C07 不预设取消/缓存已清。 |
| 4. 减负载/改配置单因素验证质量、SLO、吞吐、错误，不把重启或 empty_cache 当通用修复 | **主体已有，尚不通过** | L81 要求单因素及同窗 SLO/goodput/错误/质量，L84 与 02 域 empty_cache 语义一致；C02/C05 修参数方向和错误归因，C08 补恢复对照与窗口判据，C09 修官方项归属/取舍。未要求补造实测结果。 |
| 5. 与 Ascend OOM、release-and-recovery 对照，验证残留进程/显存、旧请求/缓存身份、ready 和持续窗口 | **部分满足，需修订** | 已有对照链接和核对关键词，NPU 字段未迁移；C07/C08 是实质缺口，须区分所有者、旧请求终态、缓存身份、实例残留基线和完整恢复门禁；C10/C11 同步未知及导航。 |

五项未整体通过；这不表示任一平台或配置“不支持”，也不要求用虚构环境结果消除 unknown。

## 校验与验证声明

`make check` 已通过：117 content entries / 553 sources。`make build` 在包含本报告的临时源码副本通过（同为 117 / 553），并已核对新 catalog 的正文 SHA-256、`procedure`、`draft / source_checked`、平台、来源与关联 ID 均与本次对象相符。临时副本沿用工作区已存在的 `build/catalog.md` 与 `build/catalog.json` 以满足既有链接，再由构建重建；第一次临时构建因复制范围遗漏 `config/taxonomy.yaml` 失败，补齐原样 `config/` 后重跑通过，未修改检查规则或配置。报告准备前记录的 599 个既有源文件指纹在构建后均未改变。结构检查与构建仅验证结构和本地引用，不验证技术正确性、远端内容或硬件行为。

本轮仅新增本报告，不关闭发现、不变更任务状态。修订后须按 C01–C11 的关闭条件重新记录正文 SHA-256 并由同一审阅者定向复核，再决定是否在相应范围通过。

**模型审阅不替代真实环境验证。** 本会话未启动推理引擎、执行 GPU/NPU 命令、构造负载、终止进程、清理缓存或注入 OOM；没有产生 CUDA/ROCm/Ascend 实测结果。正文继续保持 `draft / source_checked`，不得据本报告宣称硬件兼容、OOM 修复或恢复演练成功。
