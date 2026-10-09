---
id: software-stack.gpu-op-graph-failure-triage
title: GPU 算子、编译和图执行失败的定向诊断
type: procedure
domain: software-stack
status: draft
platforms: [generic, nvidia, amd]
source_refs:
  - src.pytorch.torch-compile-troubleshooting-2.6
  - src.pytorch.tutorials-compile-caching-8a5c6f1
  - src.pytorch.inductor-profiling-2.6
  - src.pytorch.cuda-semantics-2.6
  - src.pytorch.dispatcher-v2.6.0
  - src.nvidia.compute-sanitizer-2026.3-2026-10-09
  - src.nvidia.cuda-runtime-api-stream-12.8
  - src.nvidia.cuda-runtime-api-error-enum-12.8
  - src.nvidia.dl-cuda-graph-capture-failures-2026-10-09
  - src.triton.compiler-3-2-0-35c6c7c6
  - src.amd.rocm-env-vars-7.14.0
  - src.amd.hip-debugging-7.14.0
  - src.amd.hip-logging-7.14.0
  - src.amd.hip-error-handling-7.14.0
  - src.amd.hip-error-codes-7.14.0
  - src.amd.rocgdb-16.3-docs-7.14.0
  - src.amd.rocprofiler-sdk-1.3.2-docs-7.14.0
  - src.amd.pytorch-compatibility-7.1.1
  - src.pytorch.issue-188355
  - src.pytorch.pr-188641-linalg-eigh-cudagraph-unsafe
  - src.pytorch.issue-193735
  - src.rocm.rccl-issue-2022
updated_at: "2026-10-09"
summary: "把 GPU 路径（NVIDIA CUDA / AMD ROCm·HIP）的算子、编译与图执行失败按后端注册/算子覆盖、动态编译、graph capture、运行与异步报错四个分支分层取证，每分支固定收集首失败接口、输入/shape/dtype 与构建缓存身份；两平台的诊断工具、编译路径观测与支持限制分别引用固定版官方资料，并以「CUDA 路径不能直接宣称 HIP 适用」为硬边界；以 pytorch#188355（max-autotune 把 cuSOLVER 支撑的 linalg.eigh 放进 CUDA graph 捕获分区）的观察—归因—修复三层证据作案例样板。"
related_ids:
  - software-stack.operators-compilers-and-graphs
  - software-stack.ascend-op-graph-failure-triage
  - software-stack.runtime-execution-and-library-loading
  - software-stack.layers-and-boundaries
applicability:
  environment_refs: []
  notes: "尚无环境档案（environment_refs 为空）：流程未对准任何具体集群/版本组合，不能据此认定适用。证据样板为 PyTorch 2.6 固定文档与 v2.6.0 源码（commit 1eba9b3）、Inductor caching 教程源码（pytorch/tutorials commit 8a5c6f1）、CUDA 12.8.0 归档 Runtime API 页、Compute Sanitizer 手册（无版本化页，以 Release Notes 2026.3 + 观察日期 2026-10-09 锚定）、NVIDIA CUDA Graph 最佳实践 capture-failures 页（无版本化 URL，页面声明 0.16.1，2026-10-09 观察）、ROCm docs-7.14.0（HIP/ROCgdb 16.3/ROCprofiler-SDK 1.3.2）与 docs-7.1.1 PyTorch 兼容页（7.14.0 同路径 404）。目标环境的 torch/CUDA 或 ROCm·HIP/Triton 组合需另行固定。"
verification:
  status: not_verified
  evidence_refs: []
  notes: "方法流程未在真实环境执行：未运行任何编译、图捕获、诊断工具或复现脚本。正文技术结论对照第十六批取证记录（docs/research/batch-16-gpu-op-graph-triage-sources.md）所列固定版本来源核对；主案例与对照案例均为来源整理（上游 issue/PR/commit 与官方回归测试），不是本地复现。901 共用释义、约束分档表述与缓存开关边界按第十六批独立审阅 B16-C01/C02/C04/C05 于 2026-10-09 修订（见 docs/research/batch-16-review-fixes.md）。"
---

# GPU 算子、编译和图执行失败的定向诊断

## 目标与触发条件

触发信号：GPU 路径上出现以下任一类失败——(a) 算子报 `NotImplementedError` / backend 不支持；(b) `torch.compile` 编译期错误、graph break、反复重编译或超限静默回退 eager；(c) CUDA Graphs / HIP graphs 捕获失败（`cudaErrorStreamCapture*` / `hipErrorStreamCapture*`，错误码 900 起）；(d) 运行期异步报错，栈不指向发起代码的位置。

目标：先把失败定性到一个**分支**，再决定补什么证据。四个分支——后端注册/算子覆盖、动态编译、graph capture、运行与异步报错——每个分支固定收集三类证据：**首失败接口**（首个报错/首个 guard 失败/首个捕获错误的算子或函数）、**输入/shape/dtype**（触发调用的 tensor 形态）、**构建与缓存身份**（PyTorch/Triton 版本、GPU、图与形状、编译配置、缓存目录状态）。

症状≠根因：`cudaErrorStreamCaptureUnsupported` 只说明捕获期间发生了禁止操作，不说明是哪个调用发起的（可能是用户代码，也可能是 DataLoader 的 pin_memory 线程）；`NotImplementedError` 只说明该次 dispatch 未得到可执行实现，不说明算子整体不可用；异步报错的栈顶往往离真实发起点很远。分支之间还会叠加：捕获失败后，后续操作常连锁报 Invalidated——定性必须锚定**首**失败接口。

与姐妹篇的分工：本文只覆盖 NVIDIA（CUDA）与 AMD（ROCm/HIP）。dispatcher 两种 `NotImplementedError` 报错形态的源码原文与昇腾 PrivateUse1/CPU fallback 判定在[昇腾算子不支持与图编译失败诊断指南](ascend-op-graph-failure-triage.md)展开，本文只借其报错形态作分支入口；昇腾侧的日志开关（如 `ASCEND_GLOBAL_LOG_LEVEL`）与回退命令不适用于本文两平台，不在此重复。四种「图」（框架 graph / 编译中间表示 / 设备 graph capture / 算子库）的机制解释、guard 与缓存身份的机制层证据、TorchAir/aclgraph 路径见[算子分发、编译与计算图执行机制](operators-compilers-and-graphs.md)。运行时初始化与进程实载库身份的取证见[驱动初始化、运行时执行同步与库装载](runtime-execution-and-library-loading.md)。

**硬边界**：本文所有 CUDA 路径的工具、错误码语义与修复结论只到 CUDA 为止；HIP 侧只能引用 ROCm/HIP 官方资料。「API 名称对应」「错误码数值相同」都不构成「行为一致」的证据（详见「CUDA 路径 ≠ HIP 适用」节）。

## 适用范围与前置条件

| 证据线 | 固定方式 | 说明 |
|---|---|---|
| PyTorch 框架层 | [PyTorch 2.6 固定文档](https://docs.pytorch.org/docs/2.6/torch.compiler_troubleshooting.html) + v2.6.0 源码 commit `1eba9b3aa3c43f86f4a2c807ac8e12c4a7767340` | TORCH_LOGS 选项集、CUDA 语义约束、dispatcher 报错形态均绑定 2.6；不能外推到其他版本 |
| Inductor 编译缓存 | [caching 教程](https://pytorch.org/tutorials/recipes/torch_compile_caching_tutorial.html)为 latest 可变页，以[源码 commit 8a5c6f1](https://github.com/pytorch/tutorials/blob/8a5c6f1ca69c57b65811ddd843859809cf8c541a/recipes_source/torch_compile_caching_tutorial.rst)（2025-06-24）固定 | 页标 Last Verified 2024-11-05；缓存身份口径引用时注明此固定方式 |
| CUDA Runtime API | [12.8.0 归档 Stream 页](https://docs.nvidia.com/cuda/archive/12.8.0/cuda-runtime-api/group__CUDART__STREAM.html) | 版本化归档 URL |
| Compute Sanitizer | [手册](https://docs.nvidia.com/compute-sanitizer/ComputeSanitizer/index.html)无版本化 HTML（各版本路径 404），以 [Release Notes](https://docs.nvidia.com/compute-sanitizer/ReleaseNotes/index.html) 最新条目 2026.3 + 观察日期 2026-10-09 锚定 | 滚动文档，引用须带此锚定说明 |
| NVIDIA CUDA Graph 最佳实践 | [capture-failures 页](https://docs.nvidia.com/dl-cuda-graph/troubleshooting/capture-failures.html)无版本化 URL（versions.json 仅 latest），页面 JS 声明版本 0.16.1，2026-10-09 观察 | 滚动文档；页内 NCCL watchdog 演变叙述只引到页内口径 |
| AMD ROCm/HIP | [docs-7.14.0](https://rocm.docs.amd.com/en/docs-7.14.0/reference/environment-variables/index.html) 固定（发布 2026-07-15），含 [ROCgdb 16.3](https://rocm.docs.amd.com/projects/ROCgdb/en/docs-7.14.0/index.html) 与 [ROCprofiler-SDK 1.3.2](https://rocm.docs.amd.com/projects/rocprofiler-sdk/en/docs-7.14.0/index.html) | en/latest 已是 ROCm 10.1.0，个别环境变量语义不同，跨版本引用必须带 docs-7.14.0 前缀 |
| AMD PyTorch 兼容 | [docs-7.1.1 兼容页](https://rocm.docs.amd.com/en/docs-7.1.1/compatibility/ml-compatibility/pytorch-compatibility.html)（页内日期 2025-12-10） | 该页在 docs-7.14.0 路径下 404（文档结构迁移），只能作 7.1.1 版本线证据 |

前置条件：进入排查前固定并记录——PyTorch 与 Triton（或 pytorch-triton-rocm）版本、GPU 型号与驱动/CUDA 或 ROCm·HIP 版本、编译配置（backend/mode/dynamic、`TORCHINDUCTOR_*`、诊断变量当前取值）、缓存目录位置（含 `TRITON_CACHE_DIR` 是否显式设置及实际生效目录）与冷/热状态。本文引用的命令与变量不授予执行权限；诊断变量（`CUDA_LAUNCH_BLOCKING`、`HIP_LAUNCH_BLOCKING`、`AMD_SERIALIZE_*`、`TORCH_LOGS`、sanitizer）都会改变时序或日志量，须在授权窗口使用并在取证后复位。

## 需要的证据

| 证据 | 采集范围或定位 | 用途 | 缺失时如何处理 |
|---|---|---|---|
| 首失败接口 | 首个报错的算子/函数名、完整报错文本、堆栈首帧；编译问题取首个 guard 失败或首个 graph break 位置；捕获问题取第一条 stream capture 错误码 | 分支定性与归因锚点 | 只有二手转述或截图时不作分支归属结论 |
| 输入/shape/dtype | 触发调用的 tensor 的 shape/dtype/device/layout（guard 检查的正是这些维度） | 判断算子覆盖缺口与重编译/guard 假设 | 缺失时不做版本特定或 dtype 特定结论 |
| 构建与缓存身份 | PyTorch 与 Triton 版本、GPU 型号、图与输入形状、编译配置；`TORCHINDUCTOR_CACHE_DIR` 位置与冷/热状态 | 区分「缓存身份变化导致的重新编译」与「真实施差异」；跨机器/跨版本结果可比性 | 未固定身份时不比较跨机结果，不作「换机器就好了」结论 |
| 版本与环境快照 | torch/CUDA 或 ROCm·HIP/驱动版本 + 全部诊断变量取值 | 判断已知限制与工具适用性（如 ROCm 7.0 前后 `hipGetLastError` 语义不同） | 版本未知时不执行版本特定处置 |
| 分支专属证据 | dispatcher 报错文本、`TORCH_LOGS`/tlparse 输出、错误码（`cudaError*`/`hipError*`）、sanitizer/ROCgdb/ROCprofiler 输出 | 各分支内判定 | 见步骤表各行 |

## 步骤与判断分支

| 步骤 | 检查或动作 | 运行影响 | 预期证据与解释 | 下一步 |
|---|---|---|---|---|
| 1 | 分支定性（只读）：按首失败报错形态分流。报错文本为 "Could not run '\<op\>' with arguments from the '\<backend\>' backend…is only available for these backends: …" 或 "There were no tensor arguments to this function…no fallback function is registered"（v2.6.0 固定源码两种 `NotImplementedError` 形态，[OperatorEntry.cpp L537–557 @1eba9b3](https://github.com/pytorch/pytorch/blob/1eba9b3aa3c43f86f4a2c807ac8e12c4a7767340/aten/src/ATen/core/dispatch/OperatorEntry.cpp#L537-L557)）→ 步骤 2；`torch.compile` 编译期错误/graph break/重编译告警 → 步骤 3；`cudaErrorStreamCapture*`/`hipErrorStreamCapture*` → 步骤 4；GPU 错误但栈不指向发起代码 → 先按步骤 5 序列化复核再回读定性 | 只读 | 首失败接口 + 三类固定证据构成最小证据集；异步错误可能伪装成其他分支，必要时先做步骤 5 再定性 | 按分支进入对应步骤 |
| 2 | 后端注册/算子覆盖分支：记录报错列出的可用后端清单，区分「该 aten 算子在目标后端无实现」与「该输入参数组合（dtype/layout 触发的 dispatch key）路由到无实现路径」；同时记录输入/shape/dtype 与构建身份。AMD 侧已知覆盖缺口的官方例证：无符号整型（除 uint8）eager 支持有限、"primarily exist to assist usage with torch.compile"（[PyTorch compatibility — docs-7.1.1](https://rocm.docs.amd.com/en/docs-7.1.1/compatibility/ml-compatibility/pytorch-compatibility.html)） | 只读为主；补做覆盖核对时按既有授权 | 报错文本 + 后端清单 + 输入形态 → 「注册/覆盖缺口」结论只到这一层；是否可换算子/换 dtype 是后续工程判断 | 缺口明确 → 换实现或评估版本；报错发生在编译产物内 → 回步骤 3/4 复核 |
| 3 | 动态编译分支（`torch.compile`）：用 `TORCH_LOGS` 分项定位——`graph_breaks`（用户代码位置+原因）、`guards`、`recompiles`（含触发的 guard 失败）、`dynamic`；确认是否超过 `torch._dynamo.config.cache_size_limit`（示例值 8，另有 `accumulated_cache_size_limit`）——超限后不再编译、回退 eager 运行并告警，属**静默性能退化**形态，须主动查告警（[torch.compile Troubleshooting — PyTorch 2.6](https://docs.pytorch.org/docs/2.6/torch.compiler_troubleshooting.html)）。崩溃处置项仅记录不作默认：`suppress_errors=True` 崩溃时跳过追踪（官方称非最佳实践）、`@torch.compiler.disable` 局部禁用 | 只读日志；`TORCH_LOGS` 增大日志量与少量开销，取证后关闭 | graph break 位置 + guard 失败原因 + 重编译次数/上限 → 区分「代码不可追踪」「输入假设变化」「超限回退」三种形态；机制解释见[机制文](operators-compilers-and-graphs.md) | 需要组件级定界 → 「诊断工具」节消融链；纯覆盖问题 → 回步骤 2 |
| 4 | graph capture 分支：先按错误码对照（下表）与隐蔽触发清单核对。两档约束不可合并：违反**多半报运行时错误**（capture 须在非默认流、禁止 `.item()` 等 CPU↔GPU 同步、多 generator 须 `CUDAGraph.register_generator_state` 注册并使用 graphsafe API）；违反**多半静默数值错误/未定义行为**（同进程同时只能一个捕获、捕获期间进程内任意线程不得有非捕获 CUDA 工作（non-captured CUDA work）、CPU 工作不捕获、每次 replay 读写相同虚拟地址、禁止动态控制流与动态 shape、多流捕获允许但另有限制）——原文两档均为 "likely"：第二档违反**可能不报错**，不能依赖异常检测排除，须靠核对清单（[CUDA semantics — PyTorch 2.6](https://docs.pytorch.org/docs/2.6/notes/cuda.html)）。捕获期同步探测：`torch.cuda.set_sync_debug_mode(1)` 告警 / `(2)` 报错（[NVIDIA capture-failures 页](https://docs.nvidia.com/dl-cuda-graph/troubleshooting/capture-failures.html)） | 只读核对；探测模式为进程内配置，用后复位 | 错误码 + 触发线程/调用点 → 把「哪条约束被谁违反」定位到调用点；第二档约束违反可能不报错，不能靠异常检测排除，须靠清单核对 | 违规点在用户代码 → 修复/规避；违规点在编译产物 → 回步骤 3 消融 + 见来源案例 |
| 5 | 运行与异步报错分支：CUDA 侧 `CUDA_LAUNCH_BLOCKING=1` 强制同步——异步执行下 GPU 错误在实际执行后才上报，栈不指向请求位置（[CUDA semantics 2.6 Asynchronous execution](https://docs.pytorch.org/docs/2.6/notes/cuda.html)）；HIP 侧 `HIP_LAUNCH_BLOCKING=1`（等同 `AMD_SERIALIZE_KERNEL`），官方调试指引明示 fault 由异步 GPU 命令产生、回溯显示的是 runtime 路径，设 `AMD_SERIALIZE_KERNEL=3 AMD_SERIALIZE_COPY=3`（入队前+入队后均等待）才能在回溯中看到发起内核的代码（[Debugging with HIP — docs-7.14.0](https://rocm.docs.amd.com/projects/HIP/en/docs-7.14.0/how-to/debugging.html)）。正确性深查用 [Compute Sanitizer](https://docs.nvidia.com/compute-sanitizer/ComputeSanitizer/index.html) 四工具（见诊断工具节） | 高：序列化与 sanitizer 显著改变时序与吞吐，只在授权窗口与可重跑负载上用，取证后复位 | 序列化后栈指向发起内核的代码 → 首失败接口回填步骤 1 定性；序列化后问题消失 → 时序/竞态类候选，不能判「无问题」 | 回步骤 1–4 用修正后的首失败接口重定性 |
| 6 | 汇总：分支、首失败接口、输入/shape/dtype、构建与缓存身份、错误码/日志片段、已排除假设 | 无 | 结论回链到分支与证据 | 满足完成判据后结束 |

**CUDA/HIP 捕获错误码对照**（CUDA 侧取自 [NVIDIA capture-failures 页](https://docs.nvidia.com/dl-cuda-graph/troubleshooting/capture-failures.html)，本轮取证覆盖 900/901/904/905/906；**901 的通用释义以 [CUDA Runtime API 12.8 错误枚举](https://docs.nvidia.com/cuda/archive/12.8.0/cuda-runtime-api/group__CUDART__TYPES.html)与 [HIP error codes — docs-7.14.0](https://rocm.docs.amd.com/projects/HIP/en/docs-7.14.0/reference/error_codes.html) 的定义为准**，NVIDIA 简表的场景化概括另行注明粒度差异；HIP 侧取自 HIP error codes 页 Stream Capture Errors 900–908——数值与 CUDA 对应码一致，但场景描述为 HIP 官方表述，引用时各自带平台前缀）：

| 码 | CUDA 名称（NVIDIA 页） | HIP 名称（HIP 页） | 典型含义 |
|---|---|---|---|
| 900 | cudaErrorStreamCaptureUnsupported | Unsupported | 捕获期间发生禁止操作 |
| 901 | cudaErrorStreamCaptureInvalidated | Invalidated | **先前错误已使当前捕获序列失效**（CUDA 12.8："invalidated due to a previous error"；HIP："failed due to a previous error during capture"）——定性须追溯**首个**捕获失败；NVIDIA capture-failures 简表把典型场景概括为「外部工作/线程打断捕获」，粒度粗于 Runtime API 定义，不能反推 901 必由外部线程引起（同线程先前非法调用、900→901 级联同样落在定义内） |
| 904 | cudaErrorStreamCaptureUnjoined | Unjoined | 参与捕获的流未汇合 |
| 905 | cudaErrorStreamCaptureIsolation | Isolation | 依赖了未捕获的工作 |
| 906 | cudaErrorStreamCaptureImplicit | Implicit | 对默认流形成禁止依赖 |
| 902/903/907/908 | 本轮未从 NVIDIA 页取证 | Merge / Unmatched / CapturedEvent / WrongThread | 仅 HIP 页列出，不作 CUDA 侧断言 |

**捕获失败的隐蔽触发清单**（[NVIDIA capture-failures 页](https://docs.nvidia.com/dl-cuda-graph/troubleshooting/capture-failures.html)；Runtime API 层的捕获会话规则另见 [CUDA 12.8 Stream 页](https://docs.nvidia.com/cuda/archive/12.8.0/cuda-runtime-api/group__CUDART__STREAM.html)）：

- 用户代码同步：`.item()` / `.cpu()` / `print(tensor)` / `torch.cuda.synchronize()`；
- **任意线程**（含 DataLoader 的 pin_memory 线程、NCCL watchdog 线程）发起 stream/event query——报错栈可能完全不在用户代码；
- global 捕获模式下 pinned 内存的分配/释放（`cudaHostAlloc`/`cudaFreeHost`）；
- AccumulateGrad/DDP 在默认流上的初始化 → 906；
- 未注册的 generator：PyTorch 侧抛 `RuntimeError: Attempt to increase offset for a CUDA generator not in capture mode`（主动抛错以防静默错误）；
- `torch.compile` 函数须先 warmup 再进捕获（首次编译会访问 RNG state）；
- Runtime API 层：`cudaStreamBeginCapture` 不能在 legacy stream 上发起、须在同一流结束、非 Relaxed 模式下须同线程结束；被捕获 kernel 不得使用 texture/surface 引用；`cudaThreadExchangeStreamCaptureMode` 三模式（Global/ThreadLocal/Relaxed）决定对「潜在不安全 API 调用」的禁止范围，Relaxed 仍禁止与捕获必然冲突的调用（如查询捕获内记录的 event）；`cudaMalloc` 不入队、不被捕获观察，依赖其 replay 的图将无效。

## 诊断工具与编译路径观测

### PyTorch / NVIDIA 侧

| 观测目标 | 工具与用法 | 边界 |
|---|---|---|
| 编译过程分项日志 | `TORCH_LOGS`：`graph_breaks`（用户代码位置+原因）、`guards`、`recompiles`（含触发的 guard 失败）、`dynamic`；深调另有 `trace_bytecode`/`trace_source`/`graph_code`/`bytecode`/`aot_graphs`/`output_code`/`kernel_code` 与 `+all/+dynamo/+aot/+inductor`；可编程接口 `torch._logging.set_logs`（[Troubleshooting 2.6 Logging Tools](https://docs.pytorch.org/docs/2.6/torch.compiler_troubleshooting.html)） | 选项集随版本变化，2.6 清单不外推 |
| 跨 rank 编译汇总 | `TORCH_TRACE="/tmp/tracedir"` 收集 + `pip install tlparse && tlparse /tmp/tracedir` 出 HTML 报告；分布式作业每 rank 一份；官方建议先 tlparse 后 TORCH_LOGS（同页 tlparse 节） | **trace 含全部模型代码**（敏感模型不应外发），不含权重；tlparse 为独立 PyPI 包，版本未在页内固定 |
| 组件消融定界 | 后端链 `backend="eager"`（仅 Dynamo 图捕获）→ `"aot_eager"`（+AOTAutograd）→ `"aot_eager_decomp_partition"`（+分解/切分）→ `"inductor"`；Inductor 内再分 mode=default/reduce-overhead/max-autotune；`dynamic=True/False/None` 单独对照（同页 Ablation 节） | 仅定位到组件层，不证明组件内根因 |
| 最小复现 | `TORCHDYNAMO_REPRO_AFTER="dynamo"` 或 `"aot"` 生成 repro.py；精度问题 `TORCHDYNAMO_REPRO_LEVEL=4`（同页 Minifier 节） | 官方自述局限：「most of the time nowadays, the minifier doesn't work as expected」——不可作为必得步骤 |
| Inductor 内核级观测 | `TORCHINDUCTOR_UNIQUE_KERNEL_NAMES=1` 生成含算子类别的内核名；`TORCHINDUCTOR_BENCHMARK_KERNEL=1` 单核计时；`TORCHINDUCTOR_MAX_AUTOTUNE` 扩 autotune（[TorchInductor GPU Profiling — 2.6](https://pytorch.org/docs/2.6/torch.compiler_inductor_profiling.html)） | `UNIQUE_KERNEL_NAMES` 默认关闭以提高缓存命中，开启会降低命中率，取证后须恢复 |
| 编译缓存观测 | 缓存身份官方口径：「same PyTorch and Triton version, as well as, same GPU when device is set to be cuda」；本机缓存 `TORCHINDUCTOR_CACHE_DIR`（默认 `/tmp/torchinductor_<user>`）；组件含 FXGraphCache/AOTAutogradCache/PGO-cache/AutotuneCache（教程称 AutotuningCache；经 v2.6.0 固定源码核对在 2.6 中存在）与 FXGraph+Triton 产物打包（TritonBundler，教程称 InductorCache——组合概念，2.6 已有实现映射）；教程另列的 Mega-Cache API（`save_cache_artifacts()`/`load_cache_artifacts()`）不在 2.6 中、属较新教程能力（[caching 教程 @8a5c6f1](https://github.com/pytorch/tutorials/blob/8a5c6f1ca69c57b65811ddd843859809cf8c541a/recipes_source/torch_compile_caching_tutorial.rst)） | 缓存身份粒度的固定源码测试证据（图与 guard 同时变化不误复用；配置变化独立入 key；guard 值独立入 key 未证明）与 Triton 三层缓存的区分（TritonCodeCache 的 Python 模块缓存 / Triton 编译器自身产物缓存 / TritonBundler 打包）见[机制文](operators-compilers-and-graphs.md) |
| 运行正确性 | [Compute Sanitizer](https://docs.nvidia.com/compute-sanitizer/ComputeSanitizer/index.html) 四工具：memcheck（默认，越界/未对齐访问与硬件异常）、racecheck（共享内存冒险）、initcheck（未初始化全局内存读）、synccheck（同步原语误用）；调用 `compute-sanitizer [options] app [args]` | 注入改变时序，竞态类可能不复现；PTX 编译期 patching 要求编译器与 sanitizer 属同一 CUDA toolkit 版本；无版本化 HTML，以 Release Notes 2026.3 + 观察日期 2026-10-09 锚定 |
| 上游 issue 复现要素 | autograd、动态形状、自定义算子、config（`torch._dynamo.config`/`torch._inductor.config` 与 backend/mode 参数）、上下文管理器、tensor subclass（同页 Creating a reproducer 节） | 页内自述 non-exhaustive |

### AMD ROCm/HIP 侧（docs-7.14.0 固定）

| 观测目标 | 工具与用法 | 边界 |
|---|---|---|
| HIP API/内核日志 | `AMD_LOG_LEVEL` 0–5（LOG_NONE..LOG_EXTRA_DEBUG）、`AMD_LOG_LEVEL_FILE` 重定向、`AMD_LOG_MASK` 位掩码过滤（0x1 API 调用、0x80 内核创建与参数、0x40000 含图内内存的内存池、0x100000 comgr 路径等）（[ROCm env vars — docs-7.14.0](https://rocm.docs.amd.com/en/docs-7.14.0/reference/environment-variables/index.html)；[Logging HIP activity](https://rocm.docs.amd.com/projects/HIP/en/docs-7.14.0/how-to/logging.html)） | release 与 debug 版 HIP 均可用；en/latest（ROCm 10.1.0）个别变量语义不同，引用带版本前缀 |
| 编译路径观测 | `HIPCC_VERBOSE`（1/2/4/5/6/7 组合）打印 hipcc 生成的 clang++ 子命令（示例含 `--offload-arch=gfx90a --driver-mode=g++`）；`GPU_DUMP_CODE_OBJECT=1` dump code object；comgr 侧 `AMD_COMGR_SAVE_TEMPS`/`AMD_COMGR_EMIT_VERBOSE_LOGS`/`AMD_COMGR_REDIRECT_LOGS`；`HIPRTC_COMPILE_OPTIONS_APPEND` 附加 hiprtc 选项（同上两页） | hipcc 在 NVIDIA 平台走 nvcc（`HIP_PLATFORM` 自动探测），诊断输出形态随平台不同 |
| 编译产物不匹配的错误码入口 | `hipErrorInvalidDeviceFunction`(98) 明示「`--offload-arch` 编译的代码在不兼容 GPU 上执行」；`hipErrorNoBinaryForGpu`(209，含「JIT compilation failure during runtime」场景)、`hipErrorInvalidKernelFile`(218)、`hipErrorInvalidImage`(200)、`hipErrorSharedObjectInitFailed`(303)、`hipErrorSharedObjectSymbolNotFound`(302)（[HIP error codes — docs-7.14.0](https://rocm.docs.amd.com/projects/HIP/en/docs-7.14.0/reference/error_codes.html)） | hipModule/镜像类错误码自成体系，无 CUDA 同号对应断言 |
| 源码级调试 | [ROCgdb 16.3](https://rocm.docs.amd.com/projects/ROCgdb/en/docs-7.14.0/index.html)：Linux 源码级调试器（基于 GDB，角色对应 CUDA-GDB），经 ROCdbgapi 做 host+GPU 异构调试，支持 HIP 内核断点/单步/变量检视，随 ROCm 装于 /opt/rocm/bin | Linux 工具，不能写成跨平台等价物 |
| tracing 与计数器 | [ROCprofiler-SDK 1.3.2](https://rocm.docs.amd.com/projects/rocprofiler-sdk/en/docs-7.14.0/index.html)：运行时无关的 tracing（API 回调+异步活动记录）与内核计数器采集基础设施，配套 AQLprofile | 旧 rocprofiler（非 SDK）项目页在 docs-7.14.0 下 404；rocprof 称呼仍出现在 HIP 错误码页；新旧工具对应关系未核（缺口） |
| PyTorch on ROCm 结构 | ROCm 支持已上游化进 pytorch/pytorch，AMD 另维护 ROCm/pytorch 分叉；PyTorch 经 HIPIFY 由 CUDA 后端生成 HIP 源码；C++ 扩展验证编译器为 amdclang++（[compatibility — docs-7.1.1](https://rocm.docs.amd.com/en/docs-7.1.1/compatibility/ml-compatibility/pytorch-compatibility.html)） | 该页在 docs-7.14.0 路径 404，只能作 7.1.1 版本线证据；已知问题（如 `torch.backends.cuda.matmul.allow_fp16_reduced_precision_reduction` 不支持）随版本线变化 |

### 「CUDA 路径 ≠ HIP 适用」硬边界

不能以 CUDA 路径直接宣称 HIP 适用。本文记录的具体差异（各自引用本平台来源）：

1. **错误码数值对齐 ≠ 行为对齐**：HIP Stream Capture Errors 900–908 数值与 CUDA 对应码一致，但页面为 HIP 官方表述；[ROCm/rccl #2022](https://github.com/ROCm/rccl/issues/2022) 中 AMD 工程师称 ROCm 7.0 起捕获期行为对齐 CUDA，属 issue 内工程师陈述，不是版本化文档承诺。
2. **错误查询语义有版本分界**：kernel launch 不直接返回错误，CUDA 用 `cudaGetLastError`；HIP 用 `hipGetLastError()`（返回并复位）/`hipPeekAtLastError()`（不复位），其行为自 ROCm 7.0 起对齐 `cudaGetLastError`——7.0 之前可能返回非错误的 `hipSuccess`/`hipErrorNotReady`（[HIP Error handling — docs-7.14.0](https://rocm.docs.amd.com/projects/HIP/en/docs-7.14.0/how-to/hip_runtime_api/error_handling.html)）。取证须先定 ROCm 版本。
3. **异步序列化变量各自独立**：`CUDA_LAUNCH_BLOCKING` 与 `HIP_LAUNCH_BLOCKING`/`AMD_SERIALIZE_KERNEL`/`AMD_SERIALIZE_COPY` 语义对应但变量与实现独立，不能互称。
4. **`torch.cuda.CUDAGraph` 对 ROCm 的适用性无直接官方声明**：v2.6.0 `torch/cuda/graphs.py` 全文无 ROCm/HIP 字样（见[机制文](operators-compilers-and-graphs.md)）；HIP 侧捕获约束只能依据 HIP graphs 文档（捕获中默认流同步调用 `hipMalloc`/`hipMemcpy`/`hipFree` 不被允许，须改 `*Async` 形态）。
5. **PyTorch 无 HIP 调试专页**：docs/2.6/notes/hip.html 为 404；AMD 侧调试口径全部来自 ROCm/HIP 文档与 ROCm 兼容页，不得写成「PyTorch 官方 HIP 调试说明」。

## 来源案例：观察—归因—修复三层证据

主案例选取 [pytorch#188355](https://github.com/pytorch/pytorch/issues/188355) + 修复 [PR #188641](https://github.com/pytorch/pytorch/pull/188641)（合并 commit [`0ab462c`](https://github.com/pytorch/pytorch/commit/0ab462c59c2a26ae36624635db822125e4cb710c)）：算子覆盖（cuSOLVER 支撑的 linalg）、编译（Inductor lowering/分区）与图捕获三个分支交叉，三层证据齐全，且报告自带 eager/compile 对照。**本案例为来源整理，本库未复现。**

### 观察层（报错与现象）

- 环境：torch `2.14.0.dev20260624+cu130`、CUDA 13.0。含 `torch.linalg.eigh` 的函数在 `torch.compile(mode="max-autotune")` 下**第二次迭代**失败：`torch.AcceleratorError: CUDA error: operation not permitted when stream is capturing`（900 cudaErrorStreamCaptureUnsupported），随后 `operation failed due to a previous error during capture`（901 cudaErrorStreamCaptureInvalidated）；栈顶在 `torch/_inductor/cudagraph_trees.py` 的 `_record`。
- 报告自带三组对照：**eager 正常、max-autotune-no-cudagraphs 正常、max-autotune 失败**；复现脚本 30 行内自包含。
- 按本文步骤读法：首失败接口为 `torch.linalg.eigh`（实际执行体 `aten._linalg_eigh.default`）；触发形态是录制阶段（第二次迭代）而非首跑；错误码 900→901 级联，定性只锚定 900。

### 归因层（上游确认的根因）

[PR #188641](https://github.com/pytorch/pytorch/pull/188641) 正文：`torch.linalg.eigh` 经 Inductor lowering 为 fallback 算子 `aten._linalg_eigh.default`，CUDA 上由 cuSOLVER 支撑，在图捕获期间执行不安全；Inductor 的 cudagraph 分区未把该算子归类为 unsafe，故 max-autotune 可能把它放进捕获分区并在录制时失败。修复选择既有 cudagraph-unsafe 归类机制而非特判 max-autotune，理由原文照录：「the unsupported behavior belongs to the operator's CUDA implementation regardless of the compile mode that tries to capture it」。

归因强度注记：PR 自述「Generated by my agent」，issue 本身无维护者评论；归因可信度锚定在**合并的代码变更 + 回归测试 + 批准人**，不锚定讨论串共识。

### 修复层（合并与回归测试）

- 合并 commit [`0ab462c`](https://github.com/pytorch/pytorch/commit/0ab462c59c2a26ae36624635db822125e4cb710c)（2026-07-11 上 main）：`torch/_inductor/utils.py` +2 行（向 cudagraph-unsafe 算子表加 `aten._linalg_eigh.default`，注释「cuSOLVER-backed linalg.eigh is not CUDA graph capturable」）；`test/inductor/test_cudagraph_trees.py` +34 行回归测试 `CudaGraphTreeTests.test_graph_partition_max_autotune_skips_linalg_eigh`（断言 unsafe 归类、按 issue 报告的 matmul→eigh 模式跑 3 次迭代、FileCheck 断言日志「Created 2 graph partitions: 1 cudagraphable, 1 non-cudagraphable」）。
- 版本归属（GitHub compare 逐 tag 验证）：v2.10.0–v2.13.0 均不含该 commit；**v2.14.0（2026-09-02 发布）与 v2.14.1 含该修复**。
- 关键边界：回归测试带 `@skipIfRocm`——上游回归只覆盖 CUDA；unsafe 归类表在框架层、后端无关，但 HIP 侧 cuSOLVER 对应物（hipsolver）的捕获安全性**没有上游测试背书**，不能把该修复写成「ROCm 同样验证通过」。
- PR Test Plan 含修复前后各跑一次 issue 复现的对照与 B200 计时（eager 0.3085 ms / no-cudagraphs 0.3155 ms / 修复后 max-autotune 0.3554 ms），属提交者自述结果，本库未复现。

### 对照案例与旁证

- [pytorch#193735](https://github.com/pytorch/pytorch/issues/193735)（「关闭≠修复」实例）：ROCm 7.2.4 + torch 2.10.0+rocm7.2.4（AMD 构建）、MI350X VF（gfx950）上 `mode="max-autotune"` 多 shape 负载崩 `hipErrorStreamCaptureInvalidated`；报告内对照：单 shape 正常、default/reduce-overhead 正常、max-autotune-no-cudagraphs 正常。AMD 维护者在更新版 nightly 上未能复现，以「unable to reproduce」关闭——**无归因、无修复链**，只作 ROCm 侧症状词汇与对照写法示例，不可引用为已解决缺陷。AMD docs-7.1.1 兼容页另称 PyTorch 2.9+ROCm 7.1.1 已修「Inductor 在 HIP 下使用 CUDA graph trees 的 device error」——AMD 单方发布说明、未对应具体上游 PR，不与本案混写。
- [ROCm/rccl #2022](https://github.com/ROCm/rccl/issues/2022)（通信域旁证）：捕获集合通信报 `hipErrorStreamCaptureUnsupported`；AMD 工程师定位为 RCCL 惰性初始化在捕获期调用 `hipFree()`，并称与 CUDA 行为一致（报告者在 B200 上复验 NCCL 同样不可捕获）；无代码修复链接，已迁移至 [ROCm/rocm-systems#2785](https://github.com/ROCm/rocm-systems/issues/2785)。仅作 HIP 捕获错误语义与 CUDA 对齐讨论的旁证，不进主案例。

## eager/compile/cache 显式对照与恢复确认

方法层定义（本库未执行；主案例的三组对照是该矩阵的最小子集）：

1. **基线一致**：同一输入、同一权重与 dtype 下分别运行 eager 与编译路径；结果比对按容差（下游编译器数值可与 eager 有细微差异，见[机制文](operators-compilers-and-graphs.md)FAQ 引用），不要求逐位相等。
2. **对照矩阵**：eager / 消融后端链（eager → aot_eager → aot_eager_decomp_partition → inductor）/ mode 变体（default、reduce-overhead、max-autotune-no-cudagraphs、max-autotune）/ `dynamic=True/False/None`。逐项记录结果、性能与是否触发本分支症状。
3. **分别验证三件事**：**结果**（数值比对）、**性能**（warmup 后稳态计时，冷/热缓存分开——`TORCHINDUCTOR_CACHE_DIR` 固定位置；`TORCHINDUCTOR_FORCE_DISABLE_CACHES=1` 只禁 Inductor 层缓存、不是全栈冷启动。冷缓存测量须**同时**满足两个独立维度：进程内状态已处理（新进程或进程内重置，说明方式），**并**使测量范围内相关持久化缓存（Inductor/Triton/远程）处于已说明的冷状态——记录实际 Inductor/Triton 目录、远程缓存处理方式与清理范围，保留命中/未命中证据；只重启进程而保留磁盘缓存应记为「新进程启动」，不能称「冷缓存启动」）、**回退后的行为**（超 `cache_size_limit` 回落 eager 后的正确性与性能都要复核，不能默认回退无害）。
4. **恢复确认**：修复或规避后用**同输入**复跑原失败负载确认；缓存清理边界——缓存身份任一要素（PyTorch/Triton 版本、GPU、图/形状、配置）变化时旧缓存自然不命中，验证「冷启动下的行为」须显式清理或更换 `TORCHINDUCTOR_CACHE_DIR`，同时记录 `TRITON_CACHE_DIR` 是否显式设置与实际生效目录（显式设置时不随 `TORCHINDUCTOR_CACHE_DIR` 更换而变，Triton 编译器有独立命中路径——即使换新进程，保留的持久化缓存仍可能命中）、远程缓存处理方式、进程内状态处理方式（新进程或进程内重置）；`TORCHINDUCTOR_FORCE_DISABLE_CACHES=1` 是禁用 Inductor 层缓存，与「缓存机制正常开启但目录为空」的冷启动不是同一实验条件，不得混写；只清部分缓存时结论注明清理范围；诊断变量（`TORCH_LOGS`、序列化变量、`TORCHINDUCTOR_UNIQUE_KERNEL_NAMES`、sanitizer）全部复位后再复跑——**诊断环境下的恢复不能当作生产恢复**。

## 停止条件与恢复安排

- 三类固定证据（首失败接口、输入/shape/dtype、构建与缓存身份）齐备、分支定性明确且各结论能回链到固定版来源时，按完成判据停止；不为「跑完全部分支」继续加压。
- 序列化变量与 sanitizer 改变时序：在诊断环境下不复现的问题不能判「无问题」，须回普通模式复核后才允许收尾。
- tlparse trace 含全部模型代码：敏感模型的 trace 不外发，保留在受控位置。
- `TORCHINDUCTOR_UNIQUE_KERNEL_NAMES` 降低缓存命中率、`TORCH_LOGS` 增大日志量：取证后复位。
- 升级 PyTorch/CUDA/ROCm 版本「试运气」不是诊断步骤；版本变更需授权与回滚计划，且变更后按对照矩阵重新建立基线。
- 缓存清理/换目录低风险但改变后续命中行为：记录清理范围与时间，避免冷/热证据混写。

## 完成判据

以下任一结果可以结束本轮诊断：

1. 失败被定性到一个分支，三类固定证据齐备且相互一致，工具观测结论（错误码表、`TORCH_LOGS`/tlparse、消融链）能回链到具体固定版本文档页；
2. 采用了对照实验的，基线一致性与三件事（结果/性能/回退后行为）分别有记录，恢复确认含同输入复跑与缓存清理边界说明；
3. NVIDIA 与 AMD 的结论各自有本平台来源支撑，未发生 CUDA→HIP 互推；
4. 证据不足时结论保持 `unknown`，缺失项（见已知缺口）写入待补清单。

「换个版本能跑」「上游 issue 已关闭」都不单独满足完成判据：前者要说明换的是哪一层、为什么；后者见对照案例 #193735。

## 已知缺口

- **compute-sanitizer 无版本化 HTML**：各版本路径均 404，只能以无版本 URL + Release Notes 2026.3 + 观察日期 2026-10-09 锚定。
- **dl-cuda-graph 指南无版本化 URL**：versions.json 仅 latest，页面 JS 声明 0.16.1（2026-10-09 观察），属滚动文档。
- **CUDA 编程指南「Prohibited and Unhandled Operations」整表未抓取**：捕获禁止操作由 Runtime API 12.8 归档页 + PyTorch 2.6 cuda.html + NVIDIA 最佳实践错误码页三处拼合覆盖；需逐 API 权威清单时须补抓固定版本 programming guide 对应节。
- **PyTorch 无 HIP 调试专页**（docs/2.6/notes/hip.html 404）。
- **ROCm docs-7.14.0 无 pytorch-compatibility 页**（结构迁移；本文用 docs-7.1.1，2025-12-10 版本线）。
- **AMD 侧无版本化逐阶段排障手册**（类似 CANN 错误码页之于昇腾）：HIP 侧证据止于错误码表、日志变量与调试器/分析工具入口。
- **旧 rocprofiler 与新 ROCprofiler-SDK 对应关系未核**；rocprofiler（非 SDK）项目页在 docs-7.14.0 下 404。
- **主案例的 ROCm 外推边界**：unsafe 归类表在框架层，但回归测试 `@skipIfRocm`，hipsolver 路径捕获安全性无上游测试证据。
- **en/latest 已是 ROCm 10.1.0**：与 docs-7.14.0 个别环境变量语义不同，跨版本引用必须带版本前缀。

## 来源与验证记录

- PyTorch 2.6（固定文档）：[torch.compile Troubleshooting](https://docs.pytorch.org/docs/2.6/torch.compiler_troubleshooting.html)（TORCH_LOGS/tlparse/消融/Minifier/cache_size_limit/reproducer 清单）、[TorchInductor GPU Profiling](https://pytorch.org/docs/2.6/torch.compiler_inductor_profiling.html)（内核级环境变量）、[CUDA semantics](https://docs.pytorch.org/docs/2.6/notes/cuda.html)（异步执行、graph capture 两档约束）；v2.6.0 源码 [OperatorEntry.cpp @1eba9b3](https://github.com/pytorch/pytorch/blob/1eba9b3aa3c43f86f4a2c807ac8e12c4a7767340/aten/src/ATen/core/dispatch/OperatorEntry.cpp#L537-L557)。
- Inductor 缓存：[caching 教程（渲染页）](https://pytorch.org/tutorials/recipes/torch_compile_caching_tutorial.html)与[源码 commit 8a5c6f1](https://github.com/pytorch/tutorials/blob/8a5c6f1ca69c57b65811ddd843859809cf8c541a/recipes_source/torch_compile_caching_tutorial.rst)。
- NVIDIA：[Compute Sanitizer 手册](https://docs.nvidia.com/compute-sanitizer/ComputeSanitizer/index.html)（无版本化；[Release Notes](https://docs.nvidia.com/compute-sanitizer/ReleaseNotes/index.html) 2026.3 锚定，2026-10-09 观察）、[CUDA Runtime API 12.8 Stream 页](https://docs.nvidia.com/cuda/archive/12.8.0/cuda-runtime-api/group__CUDART__STREAM.html)、[CUDA Runtime API 12.8 错误枚举页](https://docs.nvidia.com/cuda/archive/12.8.0/cuda-runtime-api/group__CUDART__TYPES.html)（901 通用释义：cudaErrorStreamCaptureInvalidated "invalidated due to a previous error"）、[CUDA Graph Best Practice — Capture Failures](https://docs.nvidia.com/dl-cuda-graph/troubleshooting/capture-failures.html)（无版本化 URL，页面声明 0.16.1，2026-10-09 观察）；Triton 3.2.0 线 [compiler.py @35c6c7c6](https://github.com/openai/triton/blob/35c6c7c6284582b3f41c71c150e11b517acf074a/python/triton/compiler/compiler.py) L250 附近独立缓存命中路径（Inductor 层缓存禁用≠Triton 缓存禁用的证据）。
- AMD（docs-7.14.0）：[ROCm environment variables](https://rocm.docs.amd.com/en/docs-7.14.0/reference/environment-variables/index.html)、[Debugging with HIP](https://rocm.docs.amd.com/projects/HIP/en/docs-7.14.0/how-to/debugging.html)、[Logging HIP activity](https://rocm.docs.amd.com/projects/HIP/en/docs-7.14.0/how-to/logging.html)、[HIP Error handling](https://rocm.docs.amd.com/projects/HIP/en/docs-7.14.0/how-to/hip_runtime_api/error_handling.html)、[HIP error codes](https://rocm.docs.amd.com/projects/HIP/en/docs-7.14.0/reference/error_codes.html)、[ROCgdb 16.3](https://rocm.docs.amd.com/projects/ROCgdb/en/docs-7.14.0/index.html)、[ROCprofiler-SDK 1.3.2](https://rocm.docs.amd.com/projects/rocprofiler-sdk/en/docs-7.14.0/index.html)；[PyTorch compatibility — docs-7.1.1](https://rocm.docs.amd.com/en/docs-7.1.1/compatibility/ml-compatibility/pytorch-compatibility.html)（2025-12-10）。
- 案例：[pytorch#188355](https://github.com/pytorch/pytorch/issues/188355)、[PR #188641](https://github.com/pytorch/pytorch/pull/188641)、[commit 0ab462c](https://github.com/pytorch/pytorch/commit/0ab462c59c2a26ae36624635db822125e4cb710c)、[pytorch#193735](https://github.com/pytorch/pytorch/issues/193735)、[ROCm/rccl #2022](https://github.com/ROCm/rccl/issues/2022)（含 [rocm-systems#2785](https://github.com/ROCm/rocm-systems/issues/2785) 迁移）。
- 逐条主张与证据定位见[第十六批 GPU 算子/图排障来源记录](../../docs/research/batch-16-gpu-op-graph-triage-sources.md)。
- 当前验证范围：来源核对；未执行任何 GPU 程序、编译、图捕获、诊断工具或复现脚本；案例均为来源整理非本地复现。
- 待确认：见「已知缺口」；另含 tlparse 独立包版本未固定、compute-sanitizer「same toolkit」要求的具体组合矩阵未取证。
