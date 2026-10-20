# Batch 27 · T07-04 第三轮定向复核

## 会话元数据

| 项目 | 实际记录 |
|---|---|
| 角色与范围 | AI 可靠性知识库批次审阅者；仅核对[第二轮复核](batch-27-t07-04-codex-recheck-2.md)仍开放的 C09 及此次修订引入的问题；其余 12 项 CLOSED 沿用，不重查 |
| 实际执行模型 | `gpt-6.1-sol` |
| 实际推理档位 | `xhigh` |
| 元数据依据 | 当前 Codex 会话 JSONL 的 `turn_context.model`、`turn_context.effort` 与 `session_meta.cwd`；会话 ID 同环境变量 `CODEX_THREAD_ID` 一致，未按要求值反填 |
| 模型核验 | 本会话已记录的模型、档位字段分别为单一 `gpt-6.1-sol`、`xhigh`；助手文本未见模型回退标记，与用户要求相符 |
| 会话 ID | `01a15b04-7cd9-7ff1-9543-1940e828bdf4` |
| 运行记录 | `/Users/ywang2397/.codex/sessions/2026/10/21/rollout-2026-10-21T04-33-03-01a15b04-7cd9-7ff1-9543-1940e828bdf4.jsonl`；provider=`custom`，CLI=`0.163.0`，source=`exec` |
| cwd | `/Users/ywang2397/work/AI_reliability_knowledge_base` |
| 日期与时区 | 2026-10-21，Asia/Shanghai（UTC+08:00）；会话启动于当地 04:33:03 |
| 复核基点 | Git HEAD `d5bef70a40e2210c223467de17c035829179cd05` 加当前工作区；以下正文、registry 与来源记录行号均为原文件坐标 |
| 正文 | [quantization-and-quality.md](../../knowledge/07-inference/quantization-and-quality.md)，176 行；SHA-256 `7544da1bdad2a174572cd4d16b1747d70112d4d43599ef428c5425410ce1a99b` |
| registry | [registry.yaml](../../sources/registry.yaml)，6788 行；SHA-256 `5b5dd30a8fe1747a68115588f6e27a7a90b39aa1f0defcb925817c04bddf1715` |
| 来源记录 | [batch-27-t07-04-sources.md](batch-27-t07-04-sources.md)，127 行；SHA-256 `9adfa58641a4055a90640b302e3ab3c6a9561ac45f5b3142ff35b4f49564cb3f` |
| 执行边界 | 本会话直接复核，未调用其他审阅模型或子代理；未运行量化、推理、质量评估或硬件实验；本会话只新增本报告 |

先读取 README、写作指南、内容分工及第二轮关闭条件。以 `/tmp/b27-fetch/vl-gpu_worker.py`、`/tmp/b27-r2-evidence/` 原文件核对控制流和行号，并经 GitHub 连接器按固定 commit 重取下列三份关键文件；重取文件保存在 `/tmp/b27-r3-pykpgyut/`，逐字节及哈希均与第二轮证据一致。

| 固定快照与文件 | SHA-256 |
|---|---|
| vLLM `b17039bccc17b94a2ea107272ad7bc93508708df` · `vllm/v1/worker/gpu_worker.py` | `eb33b5f2bd389ac32785772ba596e5aecfaaaec281e3edfd804b993b4b1d7495` |
| vLLM Ascend `52d4acfa51fb868823d1070b81cbd2d97e9e4696` · `docs/source/faqs.md` | `ea0c8e6b8107c45f3c5427043e05137e0c83fac5999f01c063c0d53068cd3c39` |
| 同 Ascend 快照 · `vllm_ascend/platform.py` | `94be9c24fa206819c430d3afa7df7233eda0eda7e8a758bae1e43014c4d16fc1` |

融合例证使用 `/tmp/b27-fetch/` 的 Quark、MindIE EP 原文件；`conserving_memory.md`、MindIE 架构原文件沿用第二轮证据并核对其已记录哈希。来源记录 L123–127 按本轮更正读取，不将被更正覆盖的历史摘要重复计为问题。

## C09 判定

**C09 · CLOSED：第二轮的三处残留均已处理，未发现阻止关闭的新问题。**

### ① 150MiB 的阶段、条件与用途已分清

正文 L87 已撤回“启动期为 CUDAGraph 预留 150MiB”的表述，改为 `compile_or_warm_up_model` 内的 KV 配置建议。逐行核对 [`gpu_worker.py` L453–487](https://github.com/vllm-project/vllm/blob/b17039bccc17b94a2ea107272ad7bc93508708df/vllm/v1/worker/gpu_worker.py#L453-L487)：`cuda_graph_memory_bytes` 先置零，非 `enforce_eager` 时调用 `capture_model()` 取得图内存值；建议分支的准确条件是 `kv_cache_memory_bytes is None` **且** `hasattr(self, "peak_activation_memory")`。正文的“未显式指定……而依赖 memory profiling”与此相符；峰值激活记录确由前面的 [L326–327](https://github.com/vllm-project/vllm/blob/b17039bccc17b94a2ea107272ad7bc93508708df/vllm/v1/worker/gpu_worker.py#L326-L327)建立。

该分支以权重、峰值激活、非 torch 内存和实测图内存之和为非 KV 用量，再另减 `150 * (1 << 20)` 经验缓冲，分别从初始空闲内存及 requested memory 算出两种建议值；[L489–511](https://github.com/vllm-project/vllm/blob/b17039bccc17b94a2ea107272ad7bc93508708df/vllm/v1/worker/gpu_worker.py#L489-L511)仅组装并输出 debug 日志，没有回写 `available_kv_cache_memory_bytes` 或分配这块缓冲。建议分支独立于图捕获条件，`enforce_eager` 时图内存值为零，也可进入建议分支。正文没有再把图内存固定为 150MiB，或将该缓冲解释成实际图内存预留。

[`determine_available_memory` L320–343](https://github.com/vllm-project/vllm/blob/b17039bccc17b94a2ea107272ad7bc93508708df/vllm/v1/worker/gpu_worker.py#L320-L343)仍是 profiling 后计算初始可用 KV 内存，没有上述缓冲。registry L536 的第九批旧简写已紧接更正括注，明确阶段、日志用途、实测图内存及初始判定无此缓冲；来源记录 L125 同步更正。现行解释不再与源码控制流矛盾。

### ② FAQ 路径与三类证据归属已正确

正文 L87 的两个 FAQ 链接均已改为固定 commit 下的 `docs/source/faqs.md`，并与来源记录 L126 一致：

- [FAQ 14 L152–160](https://github.com/vllm-project/vllm-ascend/blob/52d4acfa51fb868823d1070b81cbd2d97e9e4696/docs/source/faqs.md#L152-L160)确为 MLA 与 NPU graph 同开时的 head 比例限制；DeepSeek-V3/R1 在 TP 切分后要求 `num_heads/num_kv_heads` 属于 `{32, 64, 128}`。
- [FAQ 18 L210–224](https://github.com/vllm-project/vllm-ascend/blob/52d4acfa51fb868823d1070b81cbd2d97e9e4696/docs/source/faqs.md#L210-L224)确为捕获配置 sizes 时 stream 资源耗尽，不能当作 full graph OOM/挂起警告的出处。
- full graph 捕获过多 batch sizes 可导致 OOM 或推理挂起的警告，已单独归到 [`vllm_ascend/platform.py` L308–326](https://github.com/vllm-project/vllm-ascend/blob/52d4acfa51fb868823d1070b81cbd2d97e9e4696/vllm_ascend/platform.py#L308-L326)，对应 `FULL_DECODE_ONLY` 或 `FULL` 分支。

正文另明示 [FAQ 13 L140–150](https://github.com/vllm-project/vllm-ascend/blob/52d4acfa51fb868823d1070b81cbd2d97e9e4696/docs/source/faqs.md#L140-L150)是一般 OOM/碎片建议，不再用它证明图模式特有警告。registry L556 原有的 platform 警告、FAQ 13/14/18 分列口径仍一致；错误路径及归属问题已消除。

### ③ 未获证的内存布局总括已收缩

正文 L86 与来源记录 L127 已撤回“融合类优化改变内存布局”的普遍断言，改为按例证分别记录执行路径与内存影响，不再由融合名称推导具体布局变化。

保留例证与原文件相符：[Quark L271](https://github.com/vllm-project/vllm/blob/b17039bccc17b94a2ea107272ad7bc93508708df/docs/features/quantization/quark.md#L271)支持无原生 OCP MX 能力设备上的融合 kernel 在线反量化；MindIE [EP L5–9](https://github.com/Ascend/MindIE-LLM/blob/69e5a5dd4b533eaffc7e198320435350825a36f7/docs/zh/user_guide/feature/expert_parallel.md#L5-L9)分别支持 level 1 AllGather、level 2 AllToAll＋通算融合，[L13–14](https://github.com/Ascend/MindIE-LLM/blob/69e5a5dd4b533eaffc7e198320435350825a36f7/docs/zh/user_guide/feature/expert_parallel.md#L13-L14)仍保留 Grouped MatMul 的 DeepSeek-V3/R1 与专家并行数>32 限定。正文要求从日志/profiling 确认实际执行路径，未把选项配置当作命中证据。

图优化段现有的执行与内存机制证据已覆盖原缺口：vLLM 的捕获开关由 [conserving_memory.md L48–75](https://github.com/vllm-project/vllm/blob/b17039bccc17b94a2ea107272ad7bc93508708df/docs/configuration/conserving_memory.md#L48-L75)支持，内存边界见子点①；MindIE 的两种图后端与 eager→graph 整图下发由 [architecture_overview.md L28–31](https://github.com/Ascend/MindIE-LLM/blob/69e5a5dd4b533eaffc7e198320435350825a36f7/docs/zh/developer_guide/architecture_design/architecture_overview.md#L28-L31)支持。正文 L87/L176 仍将图捕获/重放的数值影响、量化×图模式组合与量化权重在图下的实际执行路径列为 unknown；没有把支持矩阵的独立支持行或上述源码分支提升为本库运行验证。

## 新问题

**未发现。** 本轮仅检查 C09 三处修订及其在正文、registry、来源记录中的关联表述。正文对 profiling 条件的概括、registry 紧邻旧简写的更正括注及来源记录的更正节可以一致读取，未形成新的阶段混淆、错误定位或兼容性保证；不另立发现编号。其余 12 项 CLOSED 沿用第二轮结论，未重新审核。

## 整体结论

**C09 关闭，C01–C13 全部 CLOSED；T07-04 在原审阅范围内通过。** 本轮关闭的是内容与证据归属问题，不改变正文 `draft / source_checked` 状态，也不形成硬件、数值结果或量化×图模式兼容性的验证结论。

`make check` 通过（111 content entries / 542 sources）；`make build` 在包含本报告及既有 `build/catalog.*` 的临时源码副本通过，构建输出仅写入临时副本。`git diff --check` 通过。对开始时记录的 570 个既有文件作 SHA-256 比较，未发现改动，包含原有构建产物；本会话在仓库中仅新增本报告。核对期间另有并行会话新增 `batch-27-t07-06-codex-recheck-3.md`，不属于本轮编辑。结构与构建检查不验证技术正确性或远程链接，不替代上述原文件语义核对。

C01–C13：CLOSED 13、OPEN 0（本轮核对 1 项：CLOSED 1、OPEN 0；其余 12 项 CLOSED 沿用；新问题 0）
