# Batch 28 · T07-11 定向复核报告

## 会话元数据与结论

| 项目 | 记录 |
|---|---|
| 角色与范围 | 承接 [T07-11 初审](batch-28-t07-11-codex-review.md)，逐项复核 C01–C11 的关闭条件，并检查相关修订引入的问题；本会话未编写或修订被审正文 |
| 实际执行模型 / 推理档位 | `gpt-6.1-sol / xhigh` |
| 模型核验 | 读取 `CODEX_THREAD_ID` 对应本地会话 JSONL 的 `session_meta` 与全部 `turn_context`；实见唯一组合 `model=gpt-6.1-sol`、`effort=xhigh`，与 `collaboration_mode.settings` 一致；assistant 消息未检出 `[frontier_llm]` 回退标记；未另启模型或子代理 |
| 本轮会话 ID | `01a15d6c-b144-7ab0-80ee-7ab332fb3e5b` |
| 初审会话 ID | `01a15d60-4479-7dd2-bc81-3f9311fddff9`；保留原发现编号、优先级及关闭条件 |
| 执行方式 | 本地 Codex CLI；`originator=codex_exec`、`source=exec`、CLI 0.163.0；静态定向复核 |
| 日期 / 时区 | 2026-10-21 / Asia/Shanghai |
| 工作目录 | `/Users/ywang2397/work/AI_reliability_knowledge_base` |
| 修订后正文 | [gpu-inference-oom-triage.md](../../knowledge/07-inference/gpu-inference-oom-triage.md)，119 行 |
| 用户提供的正文 SHA-256 | `c5376ca1309497dc1b3e3515fff80ae1c8390629fa6c7a22aa8eb7363af502cc` |
| 独立计算的正文 SHA-256 | `c5376ca1309497dc1b3e3515fff80ae1c8390629fa6c7a22aa8eb7363af502cc`，**匹配** |
| 写入范围 | 仅新增本报告；不修改正文、来源记录、registry、导航、任务状态或历史报告；构建在临时源码副本执行 |

**结论：本轮暂不通过。CLOSED=3（C01、C03、C05）；OPEN=8（C02、C04、C06、C07、C08、C09、C10、C11）。开放项为 0 P1、5 P2、3 P3。没有另立 N 编号的独立新发现。** 原有问题的修订不完整、同一问题在正文或来源表中的遗漏，以及 C04 修订解释方向写反，均计入对应 C 项，不重复编号。

主要差异是：正文新增了正确说明，但部分原句和现行来源表仍与之矛盾；附加“初审修订轮”摘要不能代替修改当前主张。以下行号均绑定本报告记录的文件指纹；源码行号为固定 commit 的原文件坐标。

| 关联文件 | 本轮 SHA-256 |
|---|---|
| [作者来源记录](batch-28-t07-11-sources.md) | `5b7de27b71d550734d2366639ea05fe779e8c5b759471ea5ad76f65f19314b8e` |
| [昇腾姊妹篇](../../knowledge/07-inference/ascend-inference-oom-triage.md) | `40ad98f473ba16b385cc6bd9a5049e0b4e0d5a8648ed66524b5f70856754ab1c` |
| [发布与恢复](../../knowledge/07-inference/release-and-recovery.md) | `a3c16f4c1eaffd9855a941ca5063d3507e5a69eb5a1430a1447804695b574b69` |
| [来源登记表](../../sources/registry.yaml) | `abecd29b5c7f9527919f8bde9fc900aa9a37d73048aa558d3e272b6c99d7bd18` |

## 复核方法与证据边界

先读 `README.md`、`docs/authoring-guide.md`、`AGENTS.md`、`content-outline.md` 和元数据 schema，再对照初审 C01–C11、作者回应、修订后正文、现行主张—来源表、unknown 清单及相关 registry notes。关联页只核对本次所需的取证、所有者、恢复和导航边界，不重新验收其他任务。

本轮尝试通过网页工具打开固定 `gpu_worker.py`、PyTorch HIP 2.6 和 AMD SMI docs-10.1.0 CLI 精确页，工具调用整体返回 HTTP 429，未取得网页内容；随后 GitHub `fetch_file` 返回工具不可用。故采用既存原文缓存独立重读，**不记为本轮重新下载远端证据**，也不以网络失败认定作者主张错误。

vLLM 原文使用 `/tmp/vllm-b17039bccc17b94a2ea107272ad7bc93508708df/`。独立计算下列文件指纹；其中 utils、gpu_worker、core、core_client、conserving_memory、troubleshooting、serving_engine 和 config/scheduler 又与 `/tmp/b28/vllm/` 对应缓存逐字节比较，均一致。未在本轮重新解析远端 tag 或下载完整归档。

| 固定快照内文件 | SHA-256 前 16 位 | 本轮核对范围 |
|---|---|---|
| `vllm/v1/worker/utils.py` | `c0758a66a105e72e` | L253–273，启动预算与调参方向 |
| `vllm/v1/worker/gpu_worker.py` | `eb33b5f2bd389ac3` | L295–343，手工预算与断言；L398–415，KV 实际创建 |
| `vllm/v1/engine/core.py` | `a7a624e0ed151f00` | L254–270，配置生成到初始化入口 |
| `vllm/v1/executor/abstract.py` | `706b38531d30b04b` | L110–116，两次 RPC 的顺序 |
| `vllm/v1/core/kv_cache_utils.py` | `208abc23e1cbaebe` | L609–642，非正预算与单请求长度容量不足分支 |
| `vllm/v1/worker/gpu_model_runner.py` | `7eaa9eb78cb99f9f` | L4281–4308、L4693–4755，dummy/profile 规模；L4838–4862，图占用测量 |
| `vllm/entrypoints/openai/serving_engine.py` | `20e18f1ea16adc9f` | L1058–1085，普通 chat/completion 输入验证 |
| `vllm/platforms/rocm.py` | `b7fcec9a5263d8f9` | L443–444，auto worker 分支 |
| `vllm/compilation/cuda_graph.py` | `1fefbd5cab00fea9` | L185–192、L285–308，wrapper 保存 graph 与 replay |
| `docs/configuration/conserving_memory.md` | `895bc42beb0ff505` | TP I/O 注记、批规模、图、CPU RAM 与多模态候选 |
| `docs/configuration/optimization.md` | `b3aac342f2435e22` | L8–34，抢占、gmu 与 chunked prefill |
| `docs/usage/troubleshooting.md` | `dc679401e1078852` | L78–81，eager 隔离具体 CUDA 操作 |
| `docs/getting_started/installation/gpu.rocm.inc.md` | `3f0c7129c7e08347` | L3、L24，torch/ROCm 下界与无预编译 ROCm wheel |

PyTorch HIP 使用 `/tmp/b24-t063-s3.AfgWGe/hip-2.6.html`，SHA-256 为 `c544cb55f21a9578a4239114ef5b905286e1b1a763c1f2280a9ef2a2ead522f8`，与初审所记相同；重读接口复用、Checking for HIP、Memory management、hipBLAS workspaces 原文。AMD SMI 本轮仅核对固定版本 URL 与现有登记的一致性，没有重新取得 CLI 全文。

## C01–C11 逐项判定

| 编号 / 原优先级 | 判定 | 理由与定位 |
|---|---|---|
| C01 · P2 | **CLOSED** | 正文 L54 已拆输入验证、主动取消/断连、deadline/代理超时三条原因链；逐请求边界改为 `max_model_len` 与输入/输出合计，并明确 `max_num_batched_tokens` 是迭代预算、chunked prefill 可分块；单请求错误不再单独证明 OOM 或证明/排除副本故障，且要求关联同窗错误率、waiting/running、引擎日志。符合 [serving_engine L1065–1085](https://github.com/vllm-project/vllm/blob/b17039bccc17b94a2ea107272ad7bc93508708df/vllm/entrypoints/openai/serving_engine.py#L1065-L1085) 与 [optimization L30–34](https://github.com/vllm-project/vllm/blob/b17039bccc17b94a2ea107272ad7bc93508708df/docs/configuration/optimization.md#L30-L34)。来源记录 L42 同步。 |
| C02 · P2 | **OPEN** | L76 已补①/④的 gmu 方向、批规模与到达并发的区别、显式 KV 字节路径；但错误分类表 L52 原句“改并发救不了它”仍在，与新解释冲突。④内仍将非正预算与最大长度容量不足的建议合并；未满足初审要求按错误子分支说明的条件。详见下节。 |
| C03 · P2 | **CLOSED** | L76 已将 KV 容量检查与实际创建分开，并指出 profiling 可编译；core L254–270 → executor L110–116 → worker L398–415 的链与源码顺序一致。L79 已列请求 ID、输入/已计算 token、输出进度、chunked prefill/混批形态、失败栈，并在混合 batch 无法拆分时保留 unknown；L58 补加载/ready 与执行/KV 链接。来源记录 L44 同步；不要求为关闭文档缺口实际制造 OOM。 |
| C04 · P2 | **OPEN** | L76 比较式正确，但紧接的“只捕获他进程释放显存抵消不了本进程增长的形态”解释反向；释放量尚未抵消增长时，结束 free 较小，断言会通过。来源记录 L23 仍泛称“共享容器会触发断言错误”，L45 又重复反向解释。通过断言不证明无干扰的修订可保留，尚不能关闭该项。 |
| C05 · P2 | **CLOSED** | L78 已取消 eager 生效即确诊容量的推断，要求首个 OOM/请求字节、同窗分配与捕获规模对照；删除 capture 后 reserved 必然回落的保证，保留量持续存在不再直接判异常，图类非 OOM 已转 GPU 图失败指南。free 差值来自 [runner L4838–4862](https://github.com/vllm-project/vllm/blob/b17039bccc17b94a2ea107272ad7bc93508708df/vllm/v1/worker/gpu_model_runner.py#L4838-L4862)，graph 持有与 replay 另由 [wrapper L285–308](https://github.com/vllm-project/vllm/blob/b17039bccc17b94a2ea107272ad7bc93508708df/vllm/compilation/cuda_graph.py#L285-L308) 证实。L119③仍仅将未逐行核的 workspace/私有池分配路径列 unknown，与已核的测量及持有事实不矛盾。 |
| C06 · P2 | **OPEN** | L89–93 已补 HIP 接口名复用、构建判别、SMI 文档线、进程字段、版本分线和 auto 前提；但“hipBLAS workspace 有已知边界（已核）”尚未写出任何实际边界，CUDA/HIP 取证项也没有形成初审要求的可填写映射。链接通用表仍未说明各列在目标 HIP 构建的支持、单位/窗口和缺失处置。详见下节。 |
| C07 · P2 | **OPEN** | 正文 L82 的所有者分立已落实，不再承诺全局清空；但现行来源主张表 L30 仍无条件写“进程死亡后 KV/请求/缓存身份随进程消失”。L48 的修订摘要未撤换该主张，未满足初审明确要求的正文与来源记录同时消除承诺。此项正文已修，剩余为来源表同步。 |
| C08 · P2 | **OPEN** | L82 已补有序步骤、同条件残留基线和稳定窗字段，L100–107 也拆两组判据；但终止/等待退出/到期未退的处置仍缺失，L107 允许“终态不明者有记录”计入接流核对，未要求相应隔离或重试控制。记录未知不能独立完成旧请求/缓存身份核对。详见下节。 |
| C09 · P3 | **OPEN** | 正文 L81 已正确解释候选范围、TP 的 I/O 注记、gmu 的其他来源、多模态及 CPU 边界；来源表 L26 仍将含 gmu 的“官方缓解清单”定位到 conserving_memory/troubleshooting，registry 的 vLLM Batch 28 notes 也仍将 gmu 列为 conserving_memory 原有项。L50 的回应摘要未替换当前表与登记摘要，未满足三处同步条件。 |
| C10 · P3 | **OPEN** | 来源 ID 已更正，正文 L91/L116 已切固定 docs-10.1.0，L119 六项 unknown 也已分列；但来源记录 L32–38 的实际 unknown 清单未更新，仍缺部署组合、HIP 选项/默认 backend/fork diff、目标峰值、外部缓存/取消链等独立条目。L51 声称“unknown 清单重列”与该文件现有清单不符；正文与取证表覆盖尚未一致。 |
| C11 · P3 | **OPEN** | 已验证 L58 的加载/ready、执行/KV，L78 的 GPU 图失败，L93 的 AMD 档案及姊妹篇首段反向链接均有效，stable ID 未变；但初审同时要求在不迁移账户/API 的说明中直接链接 02 域两篇内存证据，正文仍没有 `ascend-memory-oom-evidence.md` 内联链接。其余导航修订已落实，仅此要求待补。 |

## OPEN 项的剩余条件

### C02：删除残留禁令，并分开④内两个容量错误

**位置：正文 L52、L76；来源记录 L43。** L52 仍把启动预算与 KV 检查合并为“改并发救不了它”。初审已明确区别：在线到达并发不参与 request_memory，但 `max_num_seqs` 等引擎批规模配置参与 dummy/profile，可能改变后续自动 KV 预算。L76 新增正确解释不能消除读者在分类表得到的相反判断。[runner L4281–4308](https://github.com/vllm-project/vllm/blob/b17039bccc17b94a2ea107272ad7bc93508708df/vllm/v1/worker/gpu_model_runner.py#L4281-L4308)直接使用 `max_num_seqs` 构造 dummy 请求分布。

另外，[KV 检查 L615–642](https://github.com/vllm-project/vllm/blob/b17039bccc17b94a2ea107272ad7bc93508708df/vllm/v1/core/kv_cache_utils.py#L615-L642)分为：`available_memory <= 0` 的错误仅建议增加 gmu；需要的单请求 KV 大于可用值时才同时建议增加 gmu 或降低 `max_model_len`。L76 把两者概括为同一建议仍不够准确。显式 `kv_cache_memory_bytes` 的当前 KV 预算来自指定值，不能把提高 gmu 当作扩大这个指定值的方法；已补“不套自动公式”应保留。

**最小关闭条件：** 修改 L52 的绝对表述；分别给出 request_memory、profile、非正 KV 预算、最大长度容量不足的证据与适用调整方向；在手工预算支路指明核对指定字节值和实际空闲量。无需承诺调参必然修复。

### C04：比较式与文字必须表达同一关系

**位置：正文 L76；来源记录 L23、L45。** [gpu_worker L329–339](https://github.com/vllm-project/vllm/blob/b17039bccc17b94a2ea107272ad7bc93508708df/vllm/v1/worker/gpu_worker.py#L329-L339)要求 `initial_free > after_profile_free`。若以 G 表示本进程净增长、R 表示他进程释放量，且暂不计其他变化，则结束 free = 初始 free − G + R；断言失败对应 R ≥ G，非 R < G。

仅作静态代入：初始 free 为 16、本进程增长 4、他进程释放 3 时，结束 free 为 15，断言通过；释放 4 时，结束 free 为 16，断言才失败。这些是比较式示例，不是现场读数或复现结果。

**最小关闭条件：** 将“释放显存抵消不了本进程增长”改为释放净效应足以抵消或超过增长、导致终值≥初值的部分形态；不要将其写成失败的唯一成因检测。同步修改来源表 L23 与回应 L45，继续保留增加占用不由该断言检出、无断言不证明无干扰的边界。

### C06：已核事实需要写出内容，字段需要能落到记录

**位置：正文 L66–69、L88–94；来源记录 L27–28、L47。** 本项不因没有实际 ROCm 环境而保持 OPEN，也不要求把 PyTorch 2.6 与 torch 2.8+ 拼成已核组合。版本分线和默认 worker 条件已经修好。

尚缺两部分：第一，L90 只声明 hipBLAS 已核，没有给读者可使用的边界。缓存中的 [HIP 2.6 hipBLAS workspaces](https://docs.pytorch.org/docs/2.6/notes/hip.html#hipblas-workspaces)实际说明 workspace 按 handle/stream 组合建立、可持续持有，并有专门清理接口和配置项；这与 MIOpen/AITER 未核属于不同证据状态。至少需要说明已核的持有/归属边界及精确节定位，而非仅写“有已知边界”。这里无需执行任何清理接口。

第二，初审要求的可填写对照尚未形成：目前通用表列若干统计名，平台段列 `vram_mem` / `usedGpuMemory`，但仍未逐列说明采集 API/工具、current/peak 与计数器、字节单位及换算、PID/rank/设备身份、实际 backend、峰值重置与同步窗口、字段不支持/工具查询失败的记录方法。可以复用 [02 域记录表与窗口](../../knowledge/02-software-stack/gpu-memory-oom-evidence.md)，无需复制全文；但应明确哪些列用于 CUDA、哪些 HIP 基础语义由 2.6 支持、哪些须在目标构建重核，不能让用户自行假定通用表的全部选项和统计限制均适用于目标 HIP 构建。

**最小关闭条件：** 补实际的 hipBLAS 已核边界；用表或等价可填写结构落实上述两平台字段映射，保留字段来源工具、单位/窗口和 unknown 处置。不得把 `list_gpu_processes` 的 amdsmi 分支字段未经核对就当成任意版本 AMD SMI CLI 的同名输出或直接对齐数值。

### C07：正文已改，现行来源表仍保留全局清空承诺

**位置：来源记录 L30、L48；正文 L82。** [发布与恢复](../../knowledge/07-inference/release-and-recovery.md) L75–77 与 [执行/KV](../../knowledge/07-inference/execution-and-kv-cache.md)的所有者边界支持修订后正文的分法。问题不是缺少新的源码证明，而是现行主张表仍给出相反结论。

**最小关闭条件：** 更新来源表 L30：仅对已终止所有者的本地活动状态说明不自动继承；外部/offload、远端 KV、旧 frontend 请求、重试 attempt、已提交输出分别核对。若保留旧表作历史，应明确标为已被替代的旧结论并指向现行条目，不能只在末尾追加“已修”的摘要。

### C08：终止失败的分支与未知终态的门禁仍缺失

**位置：正文 L82、L107。** 八步顺序、无未解释残留的基线口径及诊断/恢复两组判据均是有效修订，予以保留。但③目前只是确认“终止对象与退出范围”，④直接核对退出，尚未说明发起终止、等待退出的时限，以及到期未退或成员退出不完整时停止清理/重建并继续隔离的分支。⑧的“超时终态预登记”是稳定观察窗字段，不能替代③/④的退出失败处置。源文件没有给出已核的一键命令，本项也不要求补造此类命令。

L107 的“旧请求/缓存身份已核对（终态不明者有记录）”还可能将“记下未知”计作接流条件满足。L82 所说 unknown 不据缓存重建结论，也没有说明未知旧请求如何隔离、透明重试如何控制。与该页要求的恢复闭环相比，已提交输出、原请求和新 attempt 之间仍需要明确的处置边界；单纯记录不能证明取消完成或排除重复执行。

**最小关闭条件：** 在③/④补版本/部署相关的终止、等待、超时或部分退出的终态与影响范围；未确认安全退出时继续隔离，不进入对象清理和正常接流。旧请求/缓存 unknown 若未解决，应给出相应隔离、禁用未经验证的复用/透明重试或其他具体受控处置，不能仅以“有记录”满足恢复核对；相应条件不满足时不得宣称恢复完成。诊断仍可按 unknown 结束，与接流门禁分开。

### C09：来源表和 registry 仍把 gmu 归给错误页面

**位置：来源记录 L26、L50；registry 的 `src.vllm.inference-v0-14` Batch 28 notes（L536）；正文 L81。** 正文修订正确；但来源表仍写“官方缓解清单”，列含 gmu，定位仍只有 conserving_memory 和 troubleshooting。registry 也仍写 conserving_memory 提供“gpu_memory_utilization 调整等缓解项”。[conserving_memory](https://github.com/vllm-project/vllm/blob/b17039bccc17b94a2ea107272ad7bc93508708df/docs/configuration/conserving_memory.md)全文无该项；gmu 的依据为 [utils L262–270](https://github.com/vllm-project/vllm/blob/b17039bccc17b94a2ea107272ad7bc93508708df/vllm/v1/worker/utils.py#L262-L270)、KV 检查错误建议与 [optimization L19–24](https://github.com/vllm-project/vllm/blob/b17039bccc17b94a2ea107272ad7bc93508708df/docs/configuration/optimization.md#L19-L24)。

**最小关闭条件：** 按正文 L81 同步当前来源表及 registry 摘要，区分各页面原有项与本库单因素验证方法；保留候选范围、TP I/O、多模态和 CPU 项边界。无需新增来源 ID。

### C10：正文六项 unknown 尚未同步到实际取证清单

**位置：正文 L119；来源记录 L32–38、L51。** ID 拼写与 AMD SMI URL 已改正，不再作为开放的技术问题；固定 docs-10.1.0 是文档线，不能凭本轮核对宣称 CLI 现场字段已重新验证。

来源文件的实际 unknown 清单仍是原五项：ROCm 案例/引擎证据、capture 路径、NVIDIA 公开案例未取、MindIE/Ascend 不适用、未运行负载。末尾回应称重列部署组合等缺口，却未落实到这张清单。原有“公开案例未取得”和“未运行”的限制也应继续保留。

**最小关闭条件：** 使来源文件实际 unknown 清单覆盖正文 L119 的六类条件，分别写清“未固定部署组合”“HIP 选项/默认 backend/fork diff”“capture 分配路径”“目标真实峰值”“外部缓存与取消链”“ROCm 引擎行为/案例”，同时保留其他尚未补证的旧缺口。不把修订摘要或既有登记写成本轮远端重取记录。

### C11：只余 Ascend 内存证据的直接入口

**位置：正文 L45 及平台差异说明。** 本轮逐一核对正文 11 个唯一本地链接目标均存在，姊妹篇首段也已有返回 GPU 指南的链接；原来的四个缺失对照页均已补齐。仍缺初审建议明确列出的 [昇腾 NPU 内存与 OOM 证据](../../knowledge/02-software-stack/ascend-memory-oom-evidence.md)直接入口。

**最小关闭条件：** 在不迁移 NPU 字段/账户/API 的对应说明中补该页的普通 Markdown 链接，再运行本地链接检查；不要求复制姊妹篇内容或修改 stable ID。

## 新发现与验收范围

**新增独立发现：0；本轮不创建 N01。** 已检查请求错误行、KV 分配链、profiling 比较关系、eager 与图保留量、HIP/SMI 版本线、所有者划分、恢复门禁、来源摘要和新增互链。C04 的反向文字解释仍属于该断言原发现，C08 的未知终态门禁仍属于原恢复判据问题；来源表未同步分别归原 C07/C09/C10。没有将同一缺口换编号重复计数。

| 原验收范围 | 本轮判断 |
|---|---|
| 首失败阶段，含权重/profile/KV/图/prefill/decode/并发 | 阶段证据和 KV 实际分配已补；profiling 解释仍待 C04 |
| 内存分账与 CUDA/ROCm 字段/allocator 取证 | 基础分线已改善；C06 仍未满足可填写取证与已核边界要求 |
| 四类错误与查询/终止/清理/再启动 | C01 已关闭；C02 的分类表/容量子分支、C08 的退出失败分支仍待补 |
| 单因素验证质量/SLO/吞吐/错误，重启及 empty_cache 边界 | C05 已关闭；调参适用边界 C02 和来源归属 C09 尚未闭环 |
| 姊妹篇/发布恢复对照、残留、旧请求/缓存身份、ready 与稳定窗 | 已有八步框架与两组判据；C07/C08/C10/C11 的剩余条件仍开放 |

本报告只对指定修订范围给出编辑和来源核对结论。正文继续保持 `draft / source_checked`；尚无真实环境验证，不宣称 CUDA/ROCm/Ascend 配套、OOM 修复或恢复演练成功。

## 结构校验与写入核对

`make check` 通过：117 content entries / 553 sources。包含本报告的临时源码副本中 `make build` 通过，同为 117 / 553，并生成 `build/catalog.md` 与 `build/catalog.json`；核对新 catalog 中本篇 `sha256` 与用户提供值一致，`procedure`、`draft / source_checked`、平台、source_refs 和 related_ids 均与本轮正文相符。临时副本原样保留既有 `build/` 以满足已有链接，再由构建重建；使用仓库现有虚拟环境，不安装依赖，不改检查规则。工作区内没有执行本轮 `make build`。

为核对写入范围，写报告前记录了 605 个既有文件的指纹（排除 `.git`、虚拟环境和解释器/测试缓存）。会话期间发现其他并发变化：`docs/research/batch-28-t00-02-codex-review.md`、`docs/research/batch-28-t07-09-sources.md`、`knowledge/07-inference/capacity-and-autoscaling.md`、`build/catalog.json` 有变化，另出现 T07-09/T07-10 复核报告。因此不宣称整个工作区所有文件均未变化，也未覆盖或回滚这些变动。本轮写入动作仅针对本报告；被审正文、T07-11 来源记录、昇腾姊妹篇、发布恢复页和 registry 末次核验仍与上表指纹一致。

本轮未启动引擎、运行 GPU/NPU 命令、构造负载、注入故障、终止服务或清理缓存。结构检查与构建仅验证结构和本地引用，不替代技术审阅、远端来源验证或硬件验证。
