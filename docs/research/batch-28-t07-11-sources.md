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
| 启动链：request_memory 启动检查（空闲显存<gmu 预算即 ValueError"Free memory on device…"）→权重加载→profile_run→KV 容量计算（不足 ValueError"No available memory for the cache blocks…"）→warmup/图捕获；profile 假设同设备其他进程显存不变（共享容器会触发断言错误） | 既有/扩展 src.vllm.inference-v0-14 | utils.py L253-273；gpu_worker.py L331-339；kv_cache_utils.py L609-645 | NVIDIA 路径原文；NPU 侧文案差异见昇腾指南 |
| CUDA OOM 与 vLLM 容量 ValueError 是不同错误：前者来自张量分配器（torch 层），后者来自引擎 KV 容量检查；EngineDeadError 只是"引擎不可恢复退出"传播信号，不单独证明 OOM 也不确定阶段 | 扩展 src.vllm.inference-v0-14；src.pytorch.cuda-semantics-2.6 等既有 | core.py L927-943；core_client.py L425-428；02 域内存证据链 | 语义区分 |
| 运行期 KV 不足=抢占重算（warning、长尾），不是 OOM；图捕获期 OOM 与运行期 OOM 处置不同（减 capture sizes/enforce_eager 隔离） | 既有 src.vllm.inference-v0-14 | optimization.md；troubleshooting.md L78-81（enforce_eager 隔离）；conserving_memory.md | 该版本语义 |
| 缓解项分层（官方）：TP 分摊（注意每进程读全量权重、建议分片 checkpoint）；量化；降 max_model_len/max_num_seqs；gpu_memory_utilization 调整——每个都是单因素验证对象，不是通用修复 | 扩展 src.vllm.inference-v0-14 | conserving_memory.md；troubleshooting.md L21-23 | 官方缓解清单 |
| 物理显存 vs framework allocated/reserved vs 碎片 vs 其他进程：torch.cuda caching allocator 语义（reserved/allocated 统计、empty_cache 语义、allocator 配置）与 nvidia-smi 口径差异 | 既有 src.pytorch.torch-cuda-memory-usage-2.6、torch-cuda-memory-stats-2.6、cuda-allocator-config-v2.6.0、caching-device-allocator-stats-v2.6.0；src.nvidia.nvidia-smi-docs-latest-2026-09-30 | 02 域 gpu-memory-oom-evidence.md 已核锚点 | NVIDIA 分配器语义（T02-09 交付） |
| ROCm 异同：vLLM ROCm 安装/运行文档（gfx90a/942/950、ROCm 6.3+/torch 2.8+、无预编译 wheel）；PyTorch hip-notes（HIP 内存/设备语义差异）；amd-smi 显存字段；ROCm 无 nvidia-smi 对应文案，分配器为 PyTorch 同一 caching allocator 的 HIP 实现 | 既有 src.vllm.rocm-install-doc-v0-14、src.pytorch.hip-notes-2.6、src.amd.amd-smi-docs-10.1.0、src.pytorch.pytorch-rocm-fork | 各登记 notes | **ROCm 推理 OOM 的引擎级专属证据缺失**：vLLM troubleshooting 未单列 ROCm OOM 条目（如实记录）； allocator 行为差异未逐项核 |
| NCCL_CUMEM_ENABLE 历史（vLLM 0.4.3–0.10.1.1 曾置 0 规避 NCCL 显存问题，NCCL 2.22.3 修复后移除）——驱动/通信库侧显存占用的存在性证据 | 扩展 src.vllm.inference-v0-14 | troubleshooting.md L352 | 历史边界；当前版本无该覆盖 |
| 状态恢复：进程死亡后 KV/请求/缓存身份随进程消失；重启=重新走启动链；与 release-and-recovery 的排空/摘除边界衔接 | 本库归纳（依据上述＋T07-10 证据） | — | 归纳标注 |

## unknown 清单

1. ROCm 推理 OOM 公开案例与引擎级专属诊断条目未取得——ROCm 支路按"安装/运行边界＋PyTorch 分配器通用语义＋amd-smi 口径"写，引擎侧特有行为标 unknown。
2. 未逐行核 vLLM CUDA graph 捕获内存的分配路径（capture 期 workspace 归属）；150MiB 冗余口径沿用第九批复核更正（compile_or_warm_up_model L453-510）。
3. NVIDIA GPU 推理 OOM 的公开 Issue 形态记录：本轮未取（昇腾指南的两条未闭环形态不跨平台外推）；正文不以合成案例替代。
4. MindIE/Ascend 侧不适用本文字段——链接昇腾指南与 MindIE 样板。
5. 未运行任何引擎/负载，未复现任何 OOM。
