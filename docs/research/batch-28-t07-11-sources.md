# 第二十八批 T07-11 来源记录

任务：T07-11（GPU 推理 OOM 与状态恢复诊断；**new** `knowledge/07-inference/gpu-inference-oom-triage.md`，主题 07.8）。取证轮次：主会话作者角色首轮（2026-10-21；前置 T07-01/T07-02 done）。以现有昇腾指南为同问题索引而非通用处方。未复现任何 OOM。

版本线：vLLM v0.14.0＝`b17039bc`；PyTorch 2.6 文档（既有登记）；ROCm 文档 7.14.0/10.1.0 线（既有登记）；nvidia-smi 文档 latest（2026-09-30 观察）。

## 本轮取回清单（vLLM 固定 commit；SHA-256 前 16 位）

| 文件 | SHA-256 前 16 位 | 与既有登记关系 |
|---|---|---|
| vllm/v1/worker/utils.py | c0758a66a105e72e | 复核 L253-273 request_memory 锚点（一致） |
| vllm/v1/worker/gpu_worker.py | eb33b5f2bd389ac3 | 复核 L331-339 profiling 断言锚点（一致） |
| vllm/v1/engine/core.py | a7a624e0ed151f00 | 复核 EngineCore 死亡两形态（L927-943） |
| vllm/v1/engine/core_client.py | 601d375067fa724e | 复核 EngineDeadError（L425-428） |
| vllm/v1/core/kv_cache_utils.py | —（在线核对 _check_enough_kv_cache_memory 仍在 L609 起） | L609-645 KV 容量 ValueError（既有锚点） |
| docs/usage/troubleshooting.md | dc679401e1078852 | L21-23 OOM 小节 |
| docs/configuration/conserving_memory.md | 895bc42beb0ff505 | 缓解项清单（TP 分片读取注记） |

## 主张—来源定位表

| 主张 | 登记 ID | 精确位置 | 支持范围 / 未覆盖 |
|---|---|---|---|
| 启动链：request_memory 启动检查（空闲显存<gmu 预算即 ValueError"Free memory on device…"）→权重加载→profile_run→KV 容量计算（不足 ValueError"No available memory for the cache blocks…"）→warmup/图捕获；profile 断言要求初始空闲>profile 后空闲，仅当终值≥初值（他进程净释放 R≥本进程净增长 G）时失败——R<G 通过；增加占用不被检出、通过不证明无干扰（复核 C04 更正） | 既有/扩展 src.vllm.inference-v0-14 | utils.py L253-273；gpu_worker.py L331-339；kv_cache_utils.py L609-645 | NVIDIA 路径原文；NPU 侧文案差异见昇腾指南 |
| CUDA OOM 与 vLLM 容量 ValueError 是不同错误：前者来自张量分配器（torch 层），后者来自引擎 KV 容量检查；EngineDeadError 只是"引擎不可恢复退出"传播信号，不单独证明 OOM 也不确定阶段 | 扩展 src.vllm.inference-v0-14；src.pytorch.cuda-semantics-2.6 等既有 | core.py L927-943；core_client.py L425-428；02 域内存证据链 | 语义区分 |
| 运行期 KV 不足=抢占重算（warning、长尾），不是 OOM；图捕获期 OOM 与运行期 OOM 处置不同（减 capture sizes/enforce_eager 隔离） | 既有 src.vllm.inference-v0-14 | optimization.md；troubleshooting.md L78-81（enforce_eager 隔离）；conserving_memory.md | 该版本语义 |
| 缓解项分层（**已被复核轮修订取代**，现行口径）：按首失败阶段从 conserving_memory 选取候选（TP I/O 注记/量化/max_model_len/max_num_seqs/图捕获——该页**无** gmu 条目）；gmu 的依据在 request_memory/KV 错误建议（utils L262-270、kv_cache_utils L615-642）与 optimization.md L19-24/L30-34；每个是单因素验证对象不是通用修复 | 扩展 src.vllm.inference-v0-14 | conserving_memory.md；troubleshooting.md L21-23；utils.py L262-270；optimization.md L19-24 | 官方原有项与本库验证方法分列（复核 C09 修订） |
| 物理显存 vs framework allocated/reserved vs 碎片 vs 其他进程：torch.cuda caching allocator 语义（reserved/allocated 统计、empty_cache 语义、allocator 配置）与 nvidia-smi 口径差异 | 既有 src.pytorch.torch-cuda-memory-usage-2.6、torch-cuda-memory-stats-2.6、cuda-allocator-config-v2.6.0、caching-device-allocator-stats-v2.6.0；src.nvidia.nvidia-smi-docs-latest-2026-09-30 | 02 域 gpu-memory-oom-evidence.md 已核锚点 | NVIDIA 分配器语义（T02-09 交付） |
| ROCm 异同：vLLM ROCm 安装/运行文档（gfx90a/942/950、ROCm 6.3+/torch 2.8+、无预编译 wheel）；PyTorch hip-notes（HIP 内存/设备语义差异）；amd-smi 显存字段；ROCm 无 nvidia-smi 对应文案，分配器为 PyTorch 同一 caching allocator 的 HIP 实现 | 既有 src.vllm.rocm-install-doc-v0-14、src.pytorch.hip-notes-2.6、src.amd.amd-smi-docs-10.1.0、src.amd.pytorch-rocm-fork | 各登记 notes | **ROCm 推理 OOM 的引擎级专属证据缺失**：vLLM troubleshooting 未单列 ROCm OOM 条目（如实记录）； allocator 行为差异未逐项核 |
| NCCL_CUMEM_ENABLE 历史（vLLM 0.4.3–0.10.1.1 曾置 0 规避 NCCL 显存问题，NCCL 2.22.3 修复后移除）——驱动/通信库侧显存占用的存在性证据 | 扩展 src.vllm.inference-v0-14 | troubleshooting.md L352 | 历史边界；当前版本无该覆盖 |
| 状态恢复（**已被复核轮修订取代**，现行口径）：仅已终止所有者的**本地**活动 KV/prefix/请求状态不自动被继承；外部/offload 缓存与远端 KV 的幸存、重新挂载、身份兼容，旧 frontend 请求、重试 attempt 与已提交输出的终态**分别核对**（无证据即 unknown，正文按所有者分列） | 本库归纳（依据上述＋T07-10 证据） | — | 归纳标注（复核 C07 修订） |

## unknown 清单

1. 未固定的部署组合：PyTorch 2.6 语义参考与 vLLM ROCm 要求的 torch 2.8+ 未拼成已核组合，目标实际构建待固定。
2. HIP 构建下 allocator 选项支持集合、默认 backend 与 fork 差异（目标版本复核）。
3. CUDA graph capture 期 workspace/私有池分配路径未逐行核；150MiB 冗余口径沿用第九批复核更正（compile_or_warm_up_model L453-510）。
4. 目标模型真实峰值内存。
5. 外部/offload 缓存与取消链在具体部署的生存与清理行为。
6. ROCm 引擎级 OOM 特有行为与公开案例形态（本轮未取得，不以 CUDA 案例外推）。
7. NVIDIA GPU 推理 OOM 公开 Issue 形态本轮未取（昇腾指南形态不跨平台外推）；正文不以合成案例替代。
8. MindIE/Ascend 侧不适用本文字段——链接昇腾指南与 MindIE 样板。
9. 未运行任何引擎/负载，未复现任何 OOM。

## 初审修订轮（2026-10-21，响应 batch-28-t07-11-codex-review.md 的 C01–C11）

- C01：请求级错误行拆三条原因链（输入验证=max_model_len 与输入/输出合计逐请求边界、非 max_num_batched_tokens；主动取消/断连；deadline/代理超时）；单请求错误既不单独证明 OOM 也不单独证明/排除副本故障。
- C02：启动链①④分列 gmu 方向（①降 gmu/减他进程；④升 gmu/降 max_model_len）；区分引擎批规模配置（影响 dummy/profile 规模 gpu_model_runner L4281-4308/L4693-4755）与在线到达并发；补显式 kv_cache_memory_bytes 分支（gpu_worker L295-313，KV 预算直接用指定值、步骤 6 公式仅自动路径）。
- C03：第④步拆"容量/配置检查（ValueError）→实际 KV 创建（core L254-270→executor initialize_from_config/compile_or_warm_up RPC abstract L110-116→worker L398-415）"；运行期步骤补阶段判别证据（请求 ID/输入与已计算 token/输出进度/调度形态/失败栈；混合 batch 拆不开保留 unknown）；profiling 可执行编译、编译错误不一定在⑤。
- C04：（**错误旧解释，已由复核轮取代——见下方"复核第一轮修订·补充"C04：失败对应 R≥G 而非 R<G**）profiling 断言照录实际比较（初始空闲>profile 后空闲、仅终值≥初值失败）；增加占用不被识别、通过不证明无干扰；独占性另行以同窗进程读数证明。
- C05：eager 定位为隔离具体操作（非专指容量）；"图捕获容量"结论须组合证据（首个 OOM 文本+请求字节+同窗分配记录+捕获规模对照）；capture 以 free 差值计图占用且 wrapper 保留 graph（L4838-4862）；保留量不必然异常、也不保证 reserved 必然回落；图类非 OOM 错误链接 02 域 GPU 算子/图失败指南。
- C06：ROCm 节改为字段级——HIP 复用 torch.cuda 接口名/`torch.version.hip` 判别/hipBLAS 已核边界/MIOpen-AITER unknown；amd-smi 固定 10.1.0 线、进程字段 vram_mem vs usedGpuMemory；PyTorch 2.6 语义参考与 vLLM ROCm torch 2.8+ 要求分线（非已核组合）；rocm.py 默认 worker 共用 gpu_worker 带配置前提；AMD 档案链接。
- C07：步骤 8 改所有者分立——仅已终止所有者本地活动状态不自动继承；外部/offload 与远端 KV 生存与身份兼容按实现核对（unknown 不在其上重建结论）；旧请求/重试 attempt/已提交输出各自核对终态。
- C08：步骤 8 改八步闭环（保存现场→隔离流量→确认终止对象与范围→核对退出与残留（对同条件基线，SMI/运行时/框架口径不互减）→仅清理已识别无其他消费者对象→采样对账→同身份重启+固定输入质量检查→预登记稳定窗）；完成判据拆"本轮诊断结束"与"恢复完成/允许接流"两组（后者须同时满足，不允许单 OR 跳过）。
- C09：缓解项标注"按首失败阶段从官方文档选取的候选项"；TP 注记归 I/O 时间；gmu 依据回链 request_memory/KV 错误建议与 optimization 抢占节（conserving_memory 无 gmu 条目）；多模态候选与 CPU 项边界注明。
- C10：来源记录 ID 更正（src.amd.pytorch-rocm-fork）；正文 AMD SMI 链接改固定 10.1.0 线与登记 ID 对齐；unknown 清单重列（部署组合/HIP 选项集合与默认 backend 与 fork 差异/capture workspace/目标模型真实峰值/外部缓存与取消链）。
- C11：正文补 execution-and-kv-cache、model-loading-and-readiness、amd-rocm-documented-profile、gpu-op-graph-failure-triage 链接；昇腾姊妹篇加 GPU 指南反向入口。

## 复核第一轮修订·补充（2026-10-21，响应 batch-28-t07-11-codex-recheck.md 的 C02/C04/C06/C07/C08/C09/C10/C11 剩余）

- C02 剩余：错误分类表删"改并发救不了 it"绝对禁令（改为批规模配置影响 dummy/profile 的口径）；④拆两个 KV 子分支（available_memory<=0 仅建议增 gmu；单请求 KV 超可用才增 gmu/降 max_model_len）；手工 kv_cache_memory_bytes 支路注明核对指定字节值与实际空闲量（增 gmu 不扩大指定值）。
- C04 剩余：比较式解释方向更正——失败对应 R≥G（他进程净释放抵消或超过本进程增长、终值≥初值），R<G 通过；来源记录同步；增加占用不被检出/通过不证明无干扰保留。
- C06 剩余：hipBLAS 已核边界写出（handle+stream 建立、持续持有、专门清理接口与配置项，hip-notes hipBLAS workspaces 节）；新增 CUDA/HIP/目标构建三列可填写字段映射表（采集 API、进程显存 vram_mem/usedGpuMemory 按版本核对、整卡口径；复用 02 域记录表列）。
- C07 剩余：来源记录状态恢复行改写为所有者分立现行口径并标注取代。
- C08 剩余：步骤③补发起终止＋等待退出时限＋到期未退/退出不完整→停止清理与重建、维持隔离；恢复门禁中"终态不明旧请求"须受控处置（隔离/禁用未验证复用/控制透明重试），仅记录 unknown 不满足接流门。
- C09 剩余：来源记录缓解项行同步（conserving_memory 无 gmu；gmu 依据 utils L262-270/kv_cache_utils L615-642/optimization L19-24）；registry notes 同步更正。
- C10 剩余：来源记录 unknown 清单扩为九项（覆盖正文六类：部署组合/HIP 选项集合/capture 路径/真实峰值/外部缓存与取消链/ROCm 行为与案例，并保留原有限制）。
- C11 剩余：正文补 ascend-memory-oom-evidence.md 直接链接（双向不迁移说明处）。

## 复核第二轮修订（2026-10-21，响应 batch-28-t07-11-codex-recheck-2.md 的 C04/C06 剩余与 N01）

- C04 剩余：来源记录"初审修订轮"C04 条目标注错误旧解释已被取代（R≥G 失败、R<G 通过为现行口径）。
- C06 剩余：字段映射表按列组扩行（allocated/reserved current/peak、memory_stats/snapshot 计数器、单位与来源工具、进程显存 NVML/vram_mem 口径、身份列、峰值重置/backend 语义、失败处置 × CUDA 已核/HIP 2.6 支持/目标待核）；HIP 2.6 文档明确列出的基础语义（allocated/max、reserved/max、memory_stats、memory_snapshot）填入支持列。
- N01：步骤③的"不进入⑤⑥"更正为"不进入⑤对象清理、⑥采样对账与⑦再启动"。

## 复核第三轮修订（2026-10-21，响应 batch-28-t07-11-codex-recheck-3.md 的 C06 剩余）

- C06 剩余：字段映射表 CUDA 栏 backend 判据改为 02 域 L116 口径——实际 backend 记 `get_allocator_backend()` 查询结果、请求配置另列、不能据请求配置推定已生效、查询失败记 unknown 并排除依赖其语义的统计比较。
