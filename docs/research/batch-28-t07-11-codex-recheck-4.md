# Batch 28 · T07-11 第四轮定向复核报告

**结论：C06＝CLOSED（原 P2）；本轮定向复核通过，新增独立发现 0。** 正文 L95 已满足[第三轮报告](batch-28-t07-11-codex-recheck-3.md)的唯一剩余条件：以查询结果记录实际 backend，单列请求配置，查询失败时记 unknown 并排除依赖其语义的统计比较。其余已关闭项沿用前轮结论，不重新审查或背书；累计 C01–C11 全部 CLOSED，N01 沿用第三轮 CLOSED。该结论仅关闭文档审阅问题，不代表目标平台或部署组合经硬件验证。

## 会话元数据与正文指纹

| 项目 | 记录 |
|---|---|
| 角色与范围 | 仅复核 C06 最后剩余的 CUDA 栏 backend 判据及本次修改引入的问题；本会话未编写或修订被审正文 |
| 实际执行模型 / 推理档位 | `gpt-6.1-sol / xhigh` |
| 模型核验 | 读取 `CODEX_THREAD_ID` 对应本地 JSONL 的 `session_meta` 与全部 `turn_context`；唯一模型/档位组合为 `model=gpt-6.1-sol`、`effort=xhigh`，与 `collaboration_mode.settings` 一致；assistant 文本未发现模型回退标记；未另启模型或子代理 |
| 本轮会话 ID | `01a15d8c-b177-7731-aa42-b7c66c042f9c` |
| 第三轮会话 ID | `01a15d85-fb23-7412-b59b-18072431a8c3`（沿用第三轮报告记录） |
| 执行方式 | 本地 Codex CLI；`originator=codex_exec`、`source=exec`、CLI 0.163.0；静态定向复核 |
| 日期 / 时区 | 2026-10-21 / Asia/Shanghai |
| 工作目录 | `/Users/ywang2397/work/AI_reliability_knowledge_base` |
| 修订后正文 | [gpu-inference-oom-triage.md](../../knowledge/07-inference/gpu-inference-oom-triage.md)，129 行 |
| 用户提供的正文 SHA-256 | `40c44cfd9a404c7066a5afac75d3453772649460188bc472e783da09f445ff89` |
| 独立计算的正文 SHA-256 | `40c44cfd9a404c7066a5afac75d3453772649460188bc472e783da09f445ff89`，**匹配** |
| 写入范围 | 仅新增本报告；检查与构建在含本报告的临时源码副本执行，不改正文、来源记录、registry、历史报告或工作区构建产物 |

仓库行号绑定上述正文指纹。关联文件指纹如下：

| 文件 | SHA-256 |
|---|---|
| [第三轮报告](batch-28-t07-11-codex-recheck-3.md) | `7823ead47db5a6922ddd2fb09ddf738dd64310bcaa77209ac3b4c6e155a9ad84` |
| [02 域 GPU 内存证据](../../knowledge/02-software-stack/gpu-memory-oom-evidence.md) | `d841a8e780f3c8e28b0faf2815903e970ba746bb27caa116da74dd9f1e4dfbdb` |

## C06 关闭判据与理由

| 第三轮唯一剩余条件 | 本轮核验 | 判定 |
|---|---|---|
| 实际 backend 用运行时查询结果取证 | 正文 L95 CUDA 栏明确记录 `get_allocator_backend()` 查询结果；与所引用 02 域 L116 的“已证实际 backend”一致。接口在此上下文为 `torch.cuda.memory.get_allocator_backend()`，没有新增不存在的 getter。 | 满足 |
| 实际 backend 与请求配置分列 | L95 明确 env/启动参数另列，且不能据请求配置推定已生效；不再以 allocator 配置代替实际 backend，也未把该查询扩写为全部选项生效值的查询。 | 满足 |
| 查询失败时保留未知并限制比较 | L95 明确实际 backend 记 unknown，并排除依赖其语义的统计比较；结合 L91、L101 仍记录查询失败状态，不将未知填为 0。 | 满足 |
| 保留 HIP 待核边界 | L95 的 HIP 文档支持列与目标构建待核列未变，实际 backend、选项集合与 fork 差异仍待核；L100 的 reset/backend 限制、L102 的版本分线保持原状。 | 满足 |

技术依据已重新读取：[PyTorch 2.6 memory 模块的 `get_allocator_backend` 定义](https://docs.pytorch.org/docs/2.6/_modules/torch/cuda/memory.html#get_allocator_backend)描述查询 active allocator backend，实现返回 `torch._C._cuda_getAllocatorBackend()`，并非直接返回当前 env 文本。[CUDA 2.6 Memory management](https://docs.pytorch.org/docs/2.6/notes/cuda.html#cuda-memory-management)说明部分统计仅对 native 有意义；同一 [memory 模块的 `memory_stats` 定义](https://docs.pytorch.org/docs/2.6/_modules/torch/cuda/memory.html#memory_stats)进一步注明 cudaMallocAsync 下部分统计无意义且恒报零。因此，先核对实际 backend、无法核对时排除依赖其语义的比较，是有依据的取证约束。unknown 与排除比较是仓库记录规则，不是声称上游 API 返回 unknown。

**C06＝CLOSED。** 该修订准确消除了第三轮保留的“请求配置替代实际 backend”问题；不需要取得目标 HIP 硬件读数或消除已有且明确保留的 unknown。

## 修改范围与新问题检查

在内存中仅将修订正文 L95 CUDA 单元格还原为第三轮旧文“`torch.cuda.memory_*`；backend 以 allocator 配置为准”，其余字节保持不变，计算所得 SHA-256 为 `a37ecd6fa344593f59a6745f134def4eec21b98435d77cd6bab7380c12a58ab7`，精确匹配第三轮正文指纹。由此确认相对第三轮被审版本，本次正文变化仅在该单元格；没有将工作区 Git 差异误当成本轮差异，也未写回还原文本。

重读 L91–102 与 02 域 L116、L126 后，未发现本次修改引入的新问题：表格仍为四列；实际 backend 与配置的证据等级清楚；失败时的 unknown 与失败状态可以同时记录；“排除依赖其语义的统计比较”未扩大为禁止所有独立设备读数；native 统计/reset 证据仍未外推为所有 backend 保证；CUDA 查询规则未移入 HIP 已核支持列。**新增独立发现 0，不新增 N 编号。** 前轮其余列组与已关闭问题不作全面复审。

本轮先读仓库规范、写作指南、内容归属与 schema，再核对第三轮报告和上述证据。固定 commit 的 PyTorch `memory.py` raw URL 及独立 `memory_stats` 生成页本轮读取失败，未记为远端重取成功；成功读取的 2.6 模块网页与 CUDA notes 用于版本化文档佐证，不宣称已与固定 commit 原文件逐字节相等。未重新核验 HIP/AMD SMI 或 vLLM 全部来源，也未因本轮范围扩大原有支持声明。

正文仍为 `draft / source_checked`。未启动推理引擎、运行 GPU/NPU 采集工具、构造负载、复现 OOM 或执行服务生命周期操作；未取得现场 backend 值，不宣称硬件、修复或恢复验证成功。

## 校验与写入范围

含本报告的临时源码副本中，`make check` 与 `make build` 均通过：**117 content entries / 553 sources**，生成 `build/catalog.md` 与 `build/catalog.json`。构建清单 `documents` 中本篇 SHA-256 与用户提供值一致，`procedure`、`draft / source_checked`、平台与引用元数据与修订正文一致。副本保留既有 `build/` 供本地链接检查，再由构建重建；使用仓库现有虚拟环境，未安装依赖、修改检查规则或 `src/kb/`，未新增测试。工作区构建产物未改写。

写报告前记录了 615 个既有文件的指纹（排除 `.git`、虚拟环境和解释器/测试缓存）。校验后的指纹核对确认正文与上表关联文件不变，无既有文件删除。本会话的工作区写入仅为新增本报告；同期观察到 `docs/topic-coverage-audit.md`、`plans/topic-coverage.yaml` 被修改，`docs/research/batch-28-t00-02-codex-recheck-3.md` 被新增，均非本会话写入，未覆盖或回滚这些并发变更。

结构检查与构建仅验证结构、本地引用和生成清单，不证明技术结论、远端链接或硬件适用性。
