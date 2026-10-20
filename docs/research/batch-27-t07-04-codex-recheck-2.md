# Batch 27 · T07-04 第二轮定向复核

## 会话元数据

| 项目 | 实际记录 |
|---|---|
| 角色与范围 | AI 可靠性知识库批次审阅者；仅核对[第一轮复核](batch-27-t07-04-codex-recheck.md)仍开放的 C01、C02、C09、C13 及本轮修订引入的问题；其余 9 项 CLOSED 沿用，不重查 |
| 实际执行模型 | `gpt-6.1-sol` |
| 实际推理档位 | `xhigh` |
| 元数据依据 | 当前 Codex 会话 JSONL 的 `turn_context.model`、`turn_context.effort` 与 `session_meta.cwd`；与用户要求相符，未按要求值反填 |
| 会话 ID | `01a15aff-2f93-7143-8187-1e2636f2c992` |
| 运行记录 | `/Users/ywang2397/.codex/sessions/2026/10/21/rollout-2026-10-21T04-27-15-01a15aff-2f93-7143-8187-1e2636f2c992.jsonl`；provider=`custom`，CLI=`0.163.0`，source=`exec` |
| cwd | `/Users/ywang2397/work/AI_reliability_knowledge_base` |
| 日期与时区 | 2026-10-21，Asia/Shanghai（UTC+08:00）；会话启动于当地 04:27:15 |
| 复核基点 | Git HEAD `d5bef70a40e2210c223467de17c035829179cd05` 加当前工作区；以下正文与 registry 行号为本轮原文件坐标 |
| 正文 | [quantization-and-quality.md](../../knowledge/07-inference/quantization-and-quality.md)，176 行；SHA-256 `bb0418623c322bb4ebd50a1abce8fce6c73f9889b969cdccb8ced2c95117c24d` |
| registry | [registry.yaml](../../sources/registry.yaml)，6788 行；SHA-256 `19bf6fd6fbb59a319b9f604a4d50e53ff8a103b13e63b6d1506f9c3f3eb405f3` |
| 来源记录 | [batch-27-t07-04-sources.md](batch-27-t07-04-sources.md)，121 行；SHA-256 `d0906c31f0e0cb77ceb5edf5d66159e31b2b1ad2d31354a3d7caeecd57530a96` |
| 执行边界 | 本会话直接复核，未调用其他审阅模型或子代理；未运行量化、推理、质量评估或硬件实验；本会话只新增本报告 |

先读取 README、写作指南、内容分工与第一轮关闭条件。C01/C02/EP 定位优先使用 `/tmp/b27-fetch/` 原文件，GPTQ override 使用第一轮重取的 `/tmp/b27-recheck-evidence/vl-gptq_marlin.py`；核对哈希与既有记录一致。新增图优化段的必要证据经 GitHub 连接器按固定 commit 重取，原文件保存在 `/tmp/b27-r2-evidence/`，以原文件计算行号，不使用网页重排坐标：

| 固定快照与文件 | SHA-256 |
|---|---|
| vLLM `b17039bccc17b94a2ea107272ad7bc93508708df` · `vllm/v1/worker/gpu_worker.py` | `eb33b5f2bd389ac32785772ba596e5aecfaaaec281e3edfd804b993b4b1d7495` |
| 同快照 · `docs/configuration/conserving_memory.md` | `895bc42beb0ff505d78fea4d34b964bda278ea609328c24bbdc2ec898d93a32e` |
| vLLM Ascend `52d4acfa51fb868823d1070b81cbd2d97e9e4696` · `docs/source/faqs.md` | `ea0c8e6b8107c45f3c5427043e05137e0c83fac5999f01c063c0d53068cd3c39` |
| 同快照 · `vllm_ascend/platform.py` | `94be9c24fa206819c430d3afa7df7233eda0eda7e8a758bae1e43014c4d16fc1` |
| MindIE-LLM `69e5a5dd4b533eaffc7e198320435350825a36f7` · `docs/zh/developer_guide/architecture_design/architecture_overview.md` | `069f3c6ad68d8c22e2f16b1ebeb43ff7bea2d68c784de5e3f2825bcb8d118548` |

另打开 CC BY 4.0 官方说明核对许可范围。来源记录 L108–121 仍作为对早期摘要的更正读取；本轮不重新审查其余已关闭项，也不把被该节覆盖的历史表述重复计为发现。CLOSED 只表示相应内容关闭条件满足，不是硬件或组合兼容性验证。

## C01/C02/C09/C13 逐项判定

### C01 · CLOSED：Marlin 的 OR 启用项与后续清除顺序已正确

正文 L72 和 registry L536 均已改为：先由 capability<89 **或** `VLLM_TEST_FORCE_FP8_MARLIN` 置位，再由 ROCm 或 batch invariant 清除。与 [`Fp8LinearMethod.__init__` 的 fp8.py L315–325](https://github.com/vllm-project/vllm/blob/b17039bccc17b94a2ea107272ad7bc93508708df/vllm/model_executor/layers/quantization/fp8.py#L315-L325) 的赋值顺序一致；测试开关已不再误写为排除项。

该描述仍属于类初始化中的标志逻辑，没有提升为实际 kernel 命中保证。AITER 的谓词门控、不命中时路径 unknown 及回退候选边界仍保留；来源记录 L110 未与此修正冲突。第一轮剩余关闭条件已满足。

### C02 · CLOSED：GPTQ 登记中的“默认切”残留已清除

`src.arxiv.gptq-2210.17323` 的现行 notes（registry L6763）已改为 buggy 警告建议、override 需要兼容性与用户选项条件，并指向同表 vLLM 的条件说明。正文 L72、registry L536 与来源记录 L110 的口径一致。

[`gptq.py` L96–102](https://github.com/vllm-project/vllm/blob/b17039bccc17b94a2ea107272ad7bc93508708df/vllm/model_executor/layers/quantization/gptq.py#L96-L102) 执行的是告警，不能把其中的默认路径注释当作无条件切换；[`gptq_marlin.py` L215–240](https://github.com/vllm-project/vllm/blob/b17039bccc17b94a2ea107272ad7bc93508708df/vllm/model_executor/layers/quantization/gptq_marlin.py#L215-L240) 与 [L272–295](https://github.com/vllm-project/vllm/blob/b17039bccc17b94a2ea107272ad7bc93508708df/vllm/model_executor/layers/quantization/gptq_marlin.py#L272-L295)支持兼容性及用户选项限制、显式 `gptq` 保留原实现。该登记不再与正文矛盾，第一轮剩余关闭条件已满足。

### C09 · OPEN（仍开放，P2）：EP 定位已改正，图优化补文仍有机制与证据归属错误

**已满足部分**：正文 L86 已将 EP 两级分开：`ep_level=1` 的 AllGather 指向 [expert_parallel.md L5–7](https://github.com/Ascend/MindIE-LLM/blob/69e5a5dd4b533eaffc7e198320435350825a36f7/docs/zh/user_guide/feature/expert_parallel.md#L5-L7)，`ep_level=2` 的 AllToAll＋通算融合指向 [L9](https://github.com/Ascend/MindIE-LLM/blob/69e5a5dd4b533eaffc7e198320435350825a36f7/docs/zh/user_guide/feature/expert_parallel.md#L9)。Grouped MatMul 的 L13–14、DeepSeek-V3/R1 与专家并行数>32 限定仍正确。新增 L87 的 `enforce_eager` 关闭图捕获由 [conserving_memory.md L48–75](https://github.com/vllm-project/vllm/blob/b17039bccc17b94a2ea107272ad7bc93508708df/docs/configuration/conserving_memory.md#L48-L75)支持；MindIE 的 ACLGraph/ATBGraph 与 eager→graph、整图下发执行由 [architecture_overview.md L28–31](https://github.com/Ascend/MindIE-LLM/blob/69e5a5dd4b533eaffc7e198320435350825a36f7/docs/zh/developer_guide/architecture_design/architecture_overview.md#L28-L31)支持。数值影响与量化×图组合继续 unknown，未冒充验证结果。

**本轮新引入、尚需修正的部分**：

1. **150MiB 的控制流与用途被误述（正文 L87）**。正文写成“启动期内存判定为 CUDAGraph 预留 150MiB”，并归于 `determine_available_memory/profile_run`。原文件中 [`determine_available_memory` L320–343](https://github.com/vllm-project/vllm/blob/b17039bccc17b94a2ea107272ad7bc93508708df/vllm/v1/worker/gpu_worker.py#L320-L343)计算初始可用 KV 内存，没有该缓冲。150MiB 实际在 `compile_or_warm_up_model` 的 [L453–510](https://github.com/vllm-project/vllm/blob/b17039bccc17b94a2ea107272ad7bc93508708df/vllm/v1/worker/gpu_worker.py#L453-L510)：先按 `enforce_eager` 决定是否捕获并取得 `cuda_graph_memory_bytes`，再在未指定 `kv_cache_memory_bytes` 且有峰值激活记录时，将实际图内存与其他非 KV 内存、150MiB 经验缓冲分别扣入**日志中的 KV cache 配置建议值**。该段没有用 150MiB 执行图内存预留，也没有回写初始可用 KV 内存；图内存并非固定 150MiB，经验缓冲也不以已执行图捕获为前提。registry L536 的第九批旧摘要有相同简写，不能据此替代本轮重读源码后的区分。
2. **FAQ 路径失效且 full graph 警告归错来源（正文 L87）**。新增 URL 的 `docs/source/user_guide/faq/faqs.md` 在该固定 commit 重取返回 404；实际文件是 [`docs/source/faqs.md`](https://github.com/vllm-project/vllm-ascend/blob/52d4acfa51fb868823d1070b81cbd2d97e9e4696/docs/source/faqs.md)。其中 [FAQ 13 L140–150](https://github.com/vllm-project/vllm-ascend/blob/52d4acfa51fb868823d1070b81cbd2d97e9e4696/docs/source/faqs.md#L140-L150)是一般 OOM/碎片建议，没有 full graph OOM 警告；[FAQ 14 L152–160](https://github.com/vllm-project/vllm-ascend/blob/52d4acfa51fb868823d1070b81cbd2d97e9e4696/docs/source/faqs.md#L152-L160)支持 MLA 的 head 比例限制，[FAQ 18 L210–224](https://github.com/vllm-project/vllm-ascend/blob/52d4acfa51fb868823d1070b81cbd2d97e9e4696/docs/source/faqs.md#L210-L224)支持 capture sizes 的 stream 耗尽。full graph 捕获过多 batch sizes 导致 OOM 或推理挂起的警告实际在 [`platform.py` L308–326](https://github.com/vllm-project/vllm-ascend/blob/52d4acfa51fb868823d1070b81cbd2d97e9e4696/vllm_ascend/platform.py#L308-L326)，须单独归属。原 registry L555 本就区分了 platform 警告与 FAQ，不能合并成同一页证据。

**第一轮缺口仍有残留**：正文 L86 的总括“融合类优化改变内存布局”未说明何种布局及其对应证据；本轮只修了 EP 行号，没有处理第一轮已明确指出的该项。可保留已有融合反量化与通算融合例证，但不能由其名称推得尚未说明的布局变化。

**关闭所需**：将 150MiB、实际图内存与 KV 配置建议的阶段/条件分别写清，同步更正现行 registry 中被引用的简写；修正 FAQ URL，按上述位置分开 full graph、MLA 与 stream 证据；为布局变化补精确依据或收缩未获证的总括，将图机制限定为来源支持的执行与内存边界。继续要求日志/profiling 确认实际图模式及捕获/重放路径，保留未取证组合与数值影响 unknown。此处仍是内容修订要求，不要求运行硬件实验。

### C13 · CLOSED：两条许可范围 notes 已与 CC BY 4.0 一致

GPTQ 与 SmoothQuant 的 `license.notes`（registry L6762/L6776）均已改为 CC BY 4.0 在署名、许可链接与修改说明等条件下允许分享和改编，撤回“仅授予 arXiv 分发权”的旧说明。与 [CC BY 4.0 官方说明](https://creativecommons.org/licenses/by/4.0/)的允许用途和署名条件一致。

两条仍明确本库只作原创摘要与链接、未复制论文图表或长段正文，并保留仓库整体再分发许可状态。第一轮已核的 identifier、URL 与版本页归属本轮不重新展开；本次只核对剩余范围说明，关闭条件已满足。

## 新问题

**有，均属于 C09 修订引入的问题，归原项处理，不另增 C 编号或重复计数。**

| 对应项 | 本轮问题 | 优先级与影响 |
|---|---|---|
| C09，正文 L87 | 把图捕获后用于 KV 配置建议的 150MiB 经验缓冲，描述成启动期 CUDAGraph 内存预留 | P2；混淆阶段、内存预算与实际分配，不能据此判断图内存开销或优化命中 |
| C09，正文 L87 | FAQ URL 返回 404，且将 platform.py 的 full graph OOM/挂起警告归到 FAQ | P3；证据不可达且归属错误，须修复 URL 并拆开定位 |

L86 的布局变化总括是第一轮未修完的旧缺口，不计作本轮新增。其余与这四项有关的改动中未发现需要另立编号的新问题；其余九项 CLOSED 未重新检查。

## 整体结论

**本轮关闭 C01、C02、C13，C09 仍开放；T07-04 尚不能声明审阅通过。** C03、C04、C05、C06、C07、C08、C10、C11、C12 沿用第一轮 CLOSED。下一轮只需核对 C09 的上述残留及修订关联改动；本轮不改变正文的草稿/来源核对边界，不形成硬件验证结论。

`make check` 通过（111 content entries / 542 sources）；`make build` 在包含本报告与既有 `build/catalog.*` 的临时源码副本通过，构建输出仅写入临时副本。首次临时副本遗漏既有 catalog，因 `docs/first-fill-status.md` 的两个本地链接缺目标而失败，补入后重跑通过；这不是被检正文的新问题。文件指纹核对确认原有工作区文件与原有构建产物均未改变，本会话只新增本报告；核对期间另有并行会话新增 `batch-27-t07-06-codex-recheck-2.md`，不属于本轮编辑。`git diff --check` 通过。结构与构建检查不验证技术正确性或远程链接。

C01–C13：CLOSED 12、OPEN 1（本轮核对 4 项：CLOSED 3、OPEN 1；其余 9 项 CLOSED 沿用）
