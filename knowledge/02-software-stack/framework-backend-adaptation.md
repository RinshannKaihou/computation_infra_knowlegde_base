---
id: software-stack.framework-backend-adaptation
title: 框架到设备后端的适配与能力核对
type: reference
domain: software-stack
status: draft
platforms: [generic, nvidia, amd, ascend, other]
source_refs:
  - src.pytorch.privateuseone-tutorial-2026-10-09
  - src.pytorch.dispatcher-v2.6.0
  - src.pytorch.extending-autograd-2.6
  - src.pytorch.library-custom-ops-2.6
  - src.pytorch.hip-notes-2.6
  - src.pytorch.backend-registration-v2.6.0
  - src.pytorch.gradcheck-source-v2.6.0
  - src.pytorch.torch-compiler-custom-backend-2.6
  - src.pytorch.distributed-backend-2.6
  - src.ascend.torch-npu-v7.2.0-pytorch2.6.0
  - src.ascend.torchnpu-device-registration-7.2.0
  - src.ascend.torchnpu-stream-event-7.2.0
  - src.ascend.torchnpu-amp-7.2.0
  - src.ascend.torchnpu-graphs-7.2.0
  - src.mindspore.pluggable-device-2.5.0
  - src.vllm.platform-interface-0.14
  - src.vllm.plugin-system-v0-14
updated_at: '2026-10-22'
summary: "以 PyTorch PrivateUse1 树外后端机制为责任清单主干，按设备选择、forward/backward、dtype/layout、算子覆盖与 fallback、编译、并行与引擎插件六项逐项核对 PyTorch CUDA/ROCm 内置路径与 TorchNPU 扩展后端（v7.2.0-pytorch2.6.0 固定快照），并以 MindSpore 可插拔设备（r2.5.0）与 vLLM 平台接口（v0.14.0）作第三方抽象责任对照；适配成功以任务级结果验证为准，不以 import 成功为准。"
related_ids:
  - software-stack.layers-and-boundaries
  - software-stack.operators-compilers-and-graphs
  - software-stack.runtime-execution-and-library-loading
  - software-stack.ascend-op-graph-failure-triage
  - software-stack.gpu-op-graph-failure-triage
applicability:
  environment_refs: []
  notes: "尚无环境档案：本文为文档级适配责任与能力核对表，未对准任何具体集群/版本组合。PyTorch 侧固定 v2.6 文档与 v2.6.0 源码（commit 1eba9b3）；TorchNPU 侧固定 v7.2.0-pytorch2.6.0（commit bc51ab84）；vLLM 侧固定 v0.14.0（commit b17039b）；MindSpore 侧为 r2.5.0 设计文档。目标环境的框架/后端组合需另行固定，不能据此认定适用。"
verification:
  status: source_checked
  evidence_refs:
    - src.pytorch.privateuseone-tutorial-2026-10-09
    - src.pytorch.dispatcher-v2.6.0
    - src.pytorch.hip-notes-2.6
    - src.pytorch.backend-registration-v2.6.0
    - src.pytorch.gradcheck-source-v2.6.0
    - src.ascend.torchnpu-device-registration-7.2.0
    - src.mindspore.pluggable-device-2.5.0
    - src.vllm.platform-interface-0.14
  notes: "对照第十七批取证记录（docs/research/batch-17-framework-backend-sources.md）所列固定版本来源核对，2026-10-09 按初审 B17-C09/C10 修订并经 raw 实测复核 backend_registration.py L295–340 与 gradcheck.py L1987–2004；TorchNPU test/npu 用例树未取得（504），正文不虚构其用例名；未在任何 GPU/NPU 环境安装或运行代码。"
---

# 框架到设备后端的适配与能力核对

## 范围与阅读方式

本文回答：一个加速器后端要被主流框架真正用起来，需要实现哪些责任面，以及如何逐项核对它是否真的可用。主干是 PyTorch 的 PrivateUse1 树外后端机制（[教程](https://docs.pytorch.org/tutorials/advanced/privateuseone.html)）；核对对象是三条固定路径——PyTorch CUDA/ROCm 内置路径（PyTorch 2.6 文档）、TorchNPU 扩展后端（固定快照 `bc51ab84`）；第三方对照是 MindSpore 可插拔设备（r2.5.0 设计文档）与 vLLM 平台接口（v0.14.0 源码）。

分工：组件职责分层见[软件栈分层](layers-and-boundaries.md)；编译栈内部机制见[算子分发、编译与计算图执行机制](operators-compilers-and-graphs.md)；初始化与同步语义见[驱动初始化、运行时执行同步与库装载](runtime-execution-and-library-loading.md)。本文只保留适配责任清单与核对方法，不重复上述机制正文。

硬边界：**适配成功 = 任务级结果验证通过**（forward/backward 数值对照、opcheck + gradcheck（仅支持梯度计算的自定义算子路径，见下节适用分支）、编译缓存身份、集合通信可跑通），`import torch_npu` 成功、`torch.cuda.is_available()` 为 True 都不算数。

## 适配责任清单（PrivateUse1 主干）

| 责任面 | 上游机制要求 | TorchNPU 快照实现证据 | 核对点 |
|---|---|---|---|
| 设备选择与注册 | `rename_privateuse1_backend` + `_register_device_module` + `generate_methods_for_privateuse1_backend`（[教程 How to Improve User Experience](https://docs.pytorch.org/tutorials/advanced/privateuseone.html)） | [`torch_npu/__init__.py @bc51ab84`](https://raw.githubusercontent.com/Ascend/pytorch/bc51ab84cc6f35c77aab1c59886e0ea43681a317/torch_npu/__init__.py)：`rename_privateuse1_backend("npu")`、`_register_device_module('npu', …)`、`generate_methods_for_privateuse1_backend`；`TORCH_DEVICE_BACKEND_AUTOLOAD` 开关与双加速器互斥报错 | `.npu()` 建张量并跑通 `mm`（厂商 README Quick Verification 最小例，需扩展为数值对照） |
| forward/backward | 经 `AutogradPrivateUse1` 注册 `torch::autograd::Function` 的 forward/backward（[教程 Register kernels](https://docs.pytorch.org/tutorials/advanced/privateuseone.html)）；自定义 autograd 写法见 [Extending torch.autograd](https://docs.pytorch.org/docs/2.6/notes/extending.html) | 快照内 autograd 桥接以教程机制为准，不另立实现断言 | `gradcheck` 只适用于支持梯度的自定义算子（见下节适用分支） |
| dtype/layout | 后端模块五接口含 AMP dtype 面（教程 Other Modules 前后文） | [`autocast_utils.py @bc51ab84`](https://raw.githubusercontent.com/Ascend/pytorch/bc51ab84cc6f35c77aab1c59886e0ea43681a317/torch_npu/npu/autocast_utils.py)：`get_amp_supported_dtype`（bf16 支持则 `[float16, bfloat16]` 否则 `[float16]`）；`__init__.py` 以 `for_storage=True` 传入 `unsupported_dtype = [quint8, quint4x2, quint2x4, qint32, qint8]`（[`__init__.py` L203–205](https://github.com/Ascend/pytorch/blob/bc51ab84cc6f35c77aab1c59886e0ea43681a317/torch_npu/__init__.py#L203-L205)） | 该列表按上游 [`backend_registration.py` L295–340](https://github.com/pytorch/pytorch/blob/1eba9b3aa3c43f86f4a2c807ac8e12c4a7767340/torch/utils/backend_registration.py#L295-L340)（L318–319）**仅在生成 Storage 方法时生效**，约束的是自动生成的 NPU Storage 转移方法，不覆盖 tensor/算子 dtype、AMP 与 layout/format——这些面各自需要证据，未取得的范围不判支持也不判不支持 |
| 算子覆盖与 fallback | `TORCH_LIBRARY_IMPL(aten, PrivateUse1)` 注册算子 + `TORCH_LIBRARY_IMPL(_, PrivateUse1)` 注册 CPU fallback（教程）；无实现时 dispatcher 给出两种 `NotImplementedError`（[OperatorEntry.cpp L537–557 @1eba9b3](https://github.com/pytorch/pytorch/blob/1eba9b3aa3c43f86f4a2c807ac8e12c4a7767340/aten/src/ATen/core/dispatch/OperatorEntry.cpp#L537-L557)） | 同教程机制；昇腾侧 fallback 判定见[昇腾算子不支持与图编译失败诊断](ascend-op-graph-failure-triage.md) | 报错文本 + 可用后端清单 + 输入形态 → 注册/覆盖缺口结论只到这一层 |
| 内存与 stream | 后端须提供 stream/event 同步原语 | [`streams.py @bc51ab84`](https://raw.githubusercontent.com/Ascend/pytorch/bc51ab84cc6f35c77aab1c59886e0ea43681a317/torch_npu/npu/streams.py)：`Stream/Event/SyncLaunchStream/ExternalEvent` 与 `wait_event/wait_stream/record_event/query/synchronize` | API 存在 ≠ 无 race；跨 stream 正确性需任务级验证 |
| 编译接口 | custom backend 契约 `(GraphModule, example_inputs) -> Callable`，经 `register_backend`/entry_points 注册；AOTAutograd 版只需支持 core Aten 子集（[Custom Backends](https://docs.pytorch.org/docs/2.6/torch.compiler_custom_backends.html)） | [`graphs.py @bc51ab84`](https://raw.githubusercontent.com/Ascend/pytorch/bc51ab84cc6f35c77aab1c59886e0ea43681a317/torch_npu/npu/graphs.py)：`NPUGraph`（capture/replay/pool/update，beta）、`make_graphed_callables` 前向+反向双图捕获 | TorchNPU 的 TorchAir 后端是否满足该契约以其文档为准，不据上游页推断 |
| 并行接口 | 第三方通信后端经 `Backend.register_backend(name, func, extended_api, devices)` 注册（[torch.distributed](https://docs.pytorch.org/docs/2.6/distributed.html)，experimental） | `torch_npu/__init__.py`：`Backend.register_backend("lccl"/"hccl", devices=["npu"])`（hccl 最后注册） | HCCL 语义与版本配套以 HCCL/CANN 文档为准 |
| 引擎插件 | 平台类须实现设备能力/内存/通信器/编译后端/配置校验等方法；OOT 平台用 `PlatformEnum.OOT`（[`interface.py @b17039b`](https://raw.githubusercontent.com/vllm-project/vllm/b17039bccc17b94a2ea107272ad7bc93508708df/vllm/platforms/interface.py) + [插件文档](https://docs.vllm.ai/en/latest/design/plugin_system.html)） | vLLM Ascend 快照配套（CANN 8.5.0/torch 2.9.0）与昇腾档案基线非同一组合，不可拼接 | 插件侧自保兼容（Compatibility Guarantee）不代替目标组合验证 |

## ROCm 内置路径的对照位置

PyTorch for HIP 有意复用 `torch.cuda` 接口（`device('cuda')` 写法、`is_available()` 同值），判别用 `torch.version.hip`（[HIP semantics](https://docs.pytorch.org/docs/2.6/notes/hip.html)）。但该页同时列出实质差异：ROCm 不支持 TF32；内存走 caching allocator 调试开关为 `PYTORCH_NO_HIP_MEMORY_CACHING`；hipBLAS workspace 经 `HIPBLAS_WORKSPACE_CONFIG`；分布式仅 nccl/gloo；版本检查宏须加 `USE_ROCM` 守卫；未列节回指 CUDA 文档。

**硬边界**：“复用接口 ≠ 语义等价”。`torch/cuda/graphs.py @v2.6.0` 全文无 ROCm/HIP 字样（见机制文）；任何 CUDA 页结论搬运到 ROCm 前须在 HIP 文档中找到对应陈述，否则记 unknown。

## 逐能力最小测试与判据（待执行设计）

下表每行给出最小输入/版本、方法或现有测试的精确链接、观察点、预期失败与通过/无法判断条件；TorchNPU 侧用例名未取得前一律写待执行设计，不虚构用例名或结果。适用分支：**训练路径**（需梯度）用 opcheck + gradcheck；**推理/无梯度路径**（forward-only、engine 插件）不用 gradcheck，以同输入数值对照 + 输出门禁为准；**标准算子**（aten 已有实现）以后端覆盖证据为准，opcheck/gradcheck 义务只落在**自定义算子**（官方 Warning 段范围）。

| 能力面 | 最小输入/版本 | 方法/测试链接 | 观察点 | 预期失败 | 通过 / 无法判断 |
|---|---|---|---|---|---|
| 设备选择 | 固定版本 + 单设备：`.npu()`/`device('cuda')` 建张量并跑通 `mm` | 厂商 README Quick Verification 最小例（存在性） | 设备可见、张量落点 | 无设备/映射错误（见设备资源链） | 可建张量且结果可读 = 存在性通过；性能与正确性另测 |
| forward/backward（训练·自定义有梯度算子） | 同输入、固定权重、double 精度输入、可微点、非重叠内存（gradcheck 默认按 double 设计，低精度输入很可能失败） | [`opcheck`](https://docs.pytorch.org/docs/2.6/library.html#testing-custom-ops)（schema/autograd 注册/fake/aot）+ [`gradcheck`](https://docs.pytorch.org/docs/2.6/notes/extending.html)（[源码前提 L1987–2004](https://github.com/pytorch/pytorch/blob/1eba9b3aa3c43f86f4a2c807ac8e12c4a7767340/torch/autograd/gradcheck.py#L1987-L2004)：double 默认、非可微点可失败、重叠内存很可能失败） | opcheck 四项 + 数值梯度 vs 解析梯度 | 非可微点/重叠内存导致的失败属方法局限，先换可微点与非重叠输入再判 | 两者都过 = 该算子训练路径通过；任一不过且排除方法局限 = 缺口 |
| forward/backward（训练·标准算子） | 同输入、固定权重、同 dtype；eager 基线 + 后端路径 | 同输入数值对照（forward 与 backward 输出分别比对，`assert_close`，容差按任务预设） | 前后向数值一致性 | 超差（不自动归因平台） | 双向在容差内 = 通过；任一超差 = 缺口 |
| 推理前向（无梯度） | 同输入、同权重、同 dtype/layout | 同输入数值对照（`assert_close`，容差按任务预设） | 输出一致性 | dtype 未对齐（`check_dtype` 门禁） | 在容差内 = 通过；超差 = 缺口（不自动归因平台） |
| dtype/layout/format | 逐组合：dtype × layout × memory_format × NPU 存储格式 | 上节 Storage 范围 + [`get_amp_supported_dtype`](https://raw.githubusercontent.com/Ascend/pytorch/bc51ab84cc6f35c77aab1c59886e0ea43681a317/torch_npu/npu/autocast_utils.py) 分支 + T02-10 检查方法 | 组合是否可建、可算 | Storage 转移方法对未覆盖 dtype 抛 `RuntimeError`（[backend_registration.py L281–289](https://github.com/pytorch/pytorch/blob/1eba9b3aa3c43f86f4a2c807ac8e12c4a7767340/torch/utils/backend_registration.py#L281-L289) 原文 "dtype is not supported by this backend"；**不是** dispatcher 未注册算子的 `NotImplementedError`，两者不合并） | 三标记分开：文档支持性（有/无）/ 方法适用性（适用/不适用）/ 实际结果（通过/失败/未测）；无覆盖证据 = unknown（不判支持/不支持） |
| 算子覆盖/fallback | 触发调用的算子 + 输入形态 | dispatcher 两种 `NotImplementedError` 形态（上表）+ 昇腾 fallback 判定（姐妹篇） | 报错文本 + 可用后端清单 | 无 fallback 的缺口报错 | 缺口定位到算子/参数组合；是否可换算子是后续工程判断 |
| 跨 stream 依赖 | 固定最小负载：生产 stream 写 → event 记录 → 消费 stream 等待 → 消费读取；固定版本与 stream/entity 身份 | `streams.py` 原语 + 同步点复测；参考结果为单 stream 串行执行的同输入输出 | 生产/消费先后、event 完成状态、消费结果与参考一致性 | 未同步读结果（见 T02-11 F1）；缺依赖对照（去掉 event 等待）下结果不一致 | 有依赖通过 + 缺依赖可复现不一致 = 依赖有效；任一条件无法执行 = 无法判断 |
| 编译/缓存身份 | 同输入 + 固定编译配置 + 缓存目录状态 | `test_cache_guard @1eba9b3`（L779–799）：图变化时 `miss==1, hit==0` 且结果不等 | 命中/未命中 + 结果 | guard 复合变化时的误复用 | 不误复用 = 通过；guard 独立入 key 无隔离证据，不主张 |
| 并行/集合通信 | 双设备、固定 collective（如 all-reduce）、固定 rank 次序与输入张量、固定后端版本 | `Backend.register_backend` 面 + HCCL/CANN 文档语义；预期输出为单设备参考结果的归约值 | 完成/错误语义 + 输出数值 | 后端未注册/版本不配套/错序 | 输出符合预期 + 语义符合文档 = 通过； rank 映射/次序未固定 = 无法判断 |
| 引擎插件 | 固定引擎/插件/模型组合 + 固定请求输入 | `verify_model_arch/verify_quantization` + 平台接口面；输出门禁（格式/长度/结束条件） | 配置校验 + 输出门禁 | 组合不配套 | 同上；插件自保兼容不代替组合验证 |
| 性能对照（待执行定义） | 与正确性对照**相同负载、相同输入、相同版本**；基线为 eager（训练）或单副本同步服务（推理） | warmup 后稳态计时；训练：step 时间与吞吐；推理：TTFT/TPOT/吞吐（口径归 07.7，不在此定义阈值） | 计时分布 + 成功/失败/取消分母 | 未同步计时（含异步未完成）、冷/热缓存混写 | 只报告分布与分母，不设通过阈值；计时方法学不合格 = 无法判断 |

`gradcheck` 不适用分支：推理前向、无梯度算子——改用同输入数值对照；非可微点——先换可微点重测，仍须梯度结论时用解析梯度对照并记剩余 unknown；重叠内存输入——先换非重叠输入，无法替换时记方法不适用。forward 数值接近**不能**作为梯度验证通过；gradcheck 缺席不记为缺口，gradcheck 通过不扩大为全路径结论。

## 第三方框架对照：MindSpore 可插拔设备

[Third-Party Hardware Interconnection（r2.5.0）](https://www.mindspore.cn/docs/en/r2.5.0/design/pluggable_device.html) 给出另一套职责划分，可与 PrivateUse1 互证抽象责任：上层统一运行时（GraphCompiler：控制流/异构切图/分阶段图优化 + 调用抽象层做算子选择编译/内存分配/stream 分配；GraphScheduler：Actor 化与线程池调度）vs 硬件抽象层（厂商实现面）；Kernel 模式（图切分/图优化/算子选择编译/DeviceAddress 内存 + Host/Device 拷贝 + 申请销毁/stream 创建销毁，附公共内存池与 SOMAS 复用算法）vs Graph 模式（整图 SuperKernel：图编译 ANF IR→第三方 IR→可执行；图执行：Tensor 格式理解/转换 + 调用执行 + 结果转回）；插件封动态库、运行时加载。

对照用途仅限“抽象责任有哪些”；不预设 MindSpore 支持本文任何目标版本，不引用其性能数字。

## 使用与解释注意事项

- 教程页（PrivateUse1、MindSpore 设计文档）是机制声明，不是能力承诺；`custom_cpu_fallback` 的存在不保证某算子在某后端真有 fallback。
- `unsupported_dtype` 五项仅约束自动生成的 NPU Storage 转移方法（上游 `backend_registration.py` L318–319 有 “[t]akes effect only when the storage method needs to be generated” 原文），`get_amp_supported_dtype` 分支、`register_backend` 的 experimental 标记都是快照/版本绑定的，换版本重核。
- `test_privateuseone_python_backend.py` 在 `1eba9b3` 是否存在未核实（main 存在，固定 commit 下 raw 404、blob 页 503），不作为固定版本证据引用；TorchNPU `test/npu` 目录树页取证轮 504，未取得前不得虚构其用例名。
- CANN 侧与 HCCL 配套、TorchNPU 算子覆盖逐项表沿用分层文跟踪缺口（U1/U2/U6），本文不从快照外推。

## 来源与更新范围

- PyTorch 2.6（固定文档 + v2.6.0 源码 commit `1eba9b3`）：[PrivateUse1 教程](https://docs.pytorch.org/tutorials/advanced/privateuseone.html)（浮动版本，不当 2.6 不可变文档）、[Extending torch.autograd](https://docs.pytorch.org/docs/2.6/notes/extending.html)、[torch.library](https://docs.pytorch.org/docs/2.6/library.html)（opcheck，义务范围仅自定义算子）、[HIP semantics](https://docs.pytorch.org/docs/2.6/notes/hip.html)、[Custom Backends](https://docs.pytorch.org/docs/2.6/torch.compiler_custom_backends.html)、[torch.distributed](https://docs.pytorch.org/docs/2.6/distributed.html)；源码 [OperatorEntry.cpp](https://github.com/pytorch/pytorch/blob/1eba9b3aa3c43f86f4a2c807ac8e12c4a7767340/aten/src/ATen/core/dispatch/OperatorEntry.cpp#L537-L557)、[test_codecache.py](https://github.com/pytorch/pytorch/blob/1eba9b3aa3c43f86f4a2c807ac8e12c4a7767340/test/inductor/test_codecache.py)、[backend_registration.py L295–340](https://github.com/pytorch/pytorch/blob/1eba9b3aa3c43f86f4a2c807ac8e12c4a7767340/torch/utils/backend_registration.py#L295-L340)（Storage 范围限定）、[gradcheck.py L1987–2004](https://github.com/pytorch/pytorch/blob/1eba9b3aa3c43f86f4a2c807ac8e12c4a7767340/torch/autograd/gradcheck.py#L1987-L2004)（double 默认/非可微点/重叠内存前提）。
- TorchNPU 固定快照（`bc51ab84`）：[`__init__.py` L203–205](https://github.com/Ascend/pytorch/blob/bc51ab84cc6f35c77aab1c59886e0ea43681a317/torch_npu/__init__.py#L203-L205)（`for_storage=True` + 五项 dtype）、[`streams.py`](https://raw.githubusercontent.com/Ascend/pytorch/bc51ab84cc6f35c77aab1c59886e0ea43681a317/torch_npu/npu/streams.py)、[`autocast_utils.py`](https://raw.githubusercontent.com/Ascend/pytorch/bc51ab84cc6f35c77aab1c59886e0ea43681a317/torch_npu/npu/autocast_utils.py)、[`graphs.py`](https://raw.githubusercontent.com/Ascend/pytorch/bc51ab84cc6f35c77aab1c59886e0ea43681a317/torch_npu/npu/graphs.py)。
- 第三方对照：[MindSpore pluggable device（r2.5.0）](https://www.mindspore.cn/docs/en/r2.5.0/design/pluggable_device.html)、[vLLM interface.py @b17039b](https://raw.githubusercontent.com/vllm-project/vllm/b17039bccc17b94a2ea107272ad7bc93508708df/vllm/platforms/interface.py)。
- 逐条主张与证据定位见[第十七批框架后端来源记录](../../docs/research/batch-17-framework-backend-sources.md)。
- 待确认：TorchNPU 固定 commit 的 `test/npu/*` 用例名（blocked，目录页 504）；CANN/HDK 精确交集与 HCCL 配套（unknown，沿用分层文缺口）；vLLM 树内 CUDA/ROCm 平台职责页（unknown）；ROCm 文档站文本许可（unknown）。
- 修订记录：2026-10-09 按初审 B17-C09/C10 修订（Storage 范围限定、逐能力测试表与适用分支；见 [batch-17-review-fixes.md](../../docs/research/batch-17-review-fixes.md)），相关发现已完成[定向复核](../../docs/research/batch-17-codex-sixth-recheck.md)，本条目已关闭项不再待复核；本地环境验证仍未执行。
