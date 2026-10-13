# 第十七批 T02-08 框架后端适配来源记录

任务：T02-08 框架到设备后端的适配与能力核对（`framework-backend-adaptation.md`，reference）。取证日期 2026-10-09。固定基线：PyTorch 2.6 文档 + v2.6.0 源码（commit `1eba9b3`）、TorchNPU v7.2.0-pytorch2.6.0（commit `bc51ab84`）、vLLM v0.14.0（commit `b17039b`）、MindSpore r2.5.0 设计文档。

## 候选来源（11 项新登记 + 1 复用）

| proposed-id | 精确 URL | 核对要点 |
|---|---|---|
| src.pytorch.extending-autograd-2.6 | docs/2.6/notes/extending.html | Function 子类、forward/setup_context/backward、gradcheck |
| src.pytorch.library-custom-ops-2.6 | docs/2.6/library.html | opcheck 四项、register_kernel/autograd/fake |
| src.pytorch.hip-notes-2.6 | docs/2.6/notes/hip.html | 复用 CUDA 接口、torch.version.hip、TF32 不支持、caching allocator、hipBLAS workspace、仅 nccl/gloo、USE_ROCM 宏、回指 CUDA 文档（集成者实开全文复核） |
| src.pytorch.torch-compiler-custom-backend-2.6 | docs/2.6/torch.compiler_custom_backends.html | backend 契约、register_backend/entry_points、AOT 后 core Aten 子集 |
| src.pytorch.distributed-backend-2.6 | docs/2.6/distributed.html | 后端矩阵、register_backend（experimental）、device_id 默认映射 |
| src.ascend.torchnpu-device-registration-7.2.0 | raw torch_npu/__init__.py @bc51ab84 | rename_privateuse1_backend("npu")、设备模块注册、unsupported_dtype、lccl/hccl 注册 |
| src.ascend.torchnpu-stream-event-7.2.0 | raw torch_npu/npu/streams.py @bc51ab84 | Stream/Event/SyncLaunchStream/ExternalEvent 与同步语义 |
| src.ascend.torchnpu-amp-7.2.0 | raw torch_npu/npu/autocast_utils.py @bc51ab84 | get_amp_supported_dtype 五接口实现 |
| src.ascend.torchnpu-graphs-7.2.0 | raw torch_npu/npu/graphs.py @bc51ab84 | NPUGraph、双图捕获、beta、autocast-cache 互斥 |
| src.mindspore.pluggable-device-2.5.0 | mindspore.cn r2.5.0 design/pluggable_device.html | GraphCompiler/GraphScheduler、Kernel/Graph 双模式、SOMAS、动态库插件（集成者实开全文复核） |
| src.vllm.platform-interface-0.14 | raw vllm/platforms/interface.py @b17039b | PlatformEnum、平台责任面、OOT（Apache-2.0） |
| （复用）src.pytorch.privateuseone-tutorial-2026-10-09 | tutorials/advanced/privateuseone.html | 与候选 C6 同页，去重复用既有登记 |

已验证但不单独立项：notes/cuda 与 torch.cuda（沿用 cuda-semantics-2.6）、TorchNPU README 配套表与 memory.py（沿用 torch-npu-v7.2.0 快照登记）、ROCm runtimes-and-compilers（C3 平台侧旁证）。

## 主张—来源定位表

| 主张 | 来源 | 定位 | 边界 |
|---|---|---|---|
| 树外后端经 PrivateUse1 集成 + CPU fallback | PrivateUse1 教程 | Register kernels 节代码块 | 机制声明；fallback 按算子逐项验证 |
| 反向经 AutogradPrivateUse1、AMP 经 AutocastPrivateUse1 | 同上 | 第 2–3 小节 | AMP 另需 BackendModule 五接口 |
| opcheck 测 API 用法、gradcheck 测数学正确 | torch.library | Testing custom ops 节 Warning 段 | 两者都跑，不互相代替 |
| 设备选择三件套 + 不支持 dtype 清单 | torch_npu/__init__.py | 尾部注册段；unsupported_dtype 行 | 快照实现；清单只适用于该快照 |
| 最小验证入口 .npu() + mm | torch-npu 快照 README | Quick Verification | 厂商最小例；须扩展为数值对照 |
| stream/event 四类与同步语义 | streams.py | 全文类与方法 | API 存在≠无 race |
| dispatcher 两种 NotImplementedError | dispatcher-v2.6.0 | OperatorEntry.cpp L537–557 | 复用 T02-05/06 入口 |
| ROCm 复用 CUDA 接口但 TF32 不支持等差异 | hip-notes-2.6 | 接口复用/TF32/内存/分布式节 | 复用接口≠语义等价 |
| ROCm 内存 caching allocator + 仅 nccl/gloo | hip-notes-2.6 | Memory management/distributed 节 | 与 T02-09 分工 |
| custom backend 契约与 AOT 子集 | custom-backend-2.6 | Overview/Registering/AOT 三节 | TorchAir 是否满足以其文档为准 |
| 第三方通信后端注册；TorchNPU 注册 lccl/hccl | distributed-2.6 + __init__.py | register_backend API 段；_register_distributed_backend_for_npu | experimental；HCCL 语义以 CANN 为准 |
| vLLM 平台责任面；OOT | interface.py + plugin-system | 全文；插件文档兼容保证 | Ascend 快照配套非同一组合，不拼接 |
| MindSpore 硬件抽象层与双模式 | pluggable-device-2.5.0 | 全文 + Kernel/Graph 两节 | 只取抽象责任对照 |

## 上游接口测试例

主推荐：`test/inductor/test_codecache.py::test_cache_guard @1eba9b3`（L779–799，沿用既有 src.pytorch.test-codecache-v2.6.0 登记；raw 200 本轮复核）。配套反例：`test_cudagraph_trees.py::test_error_on_dealloc_use`。文档级：opcheck + gradcheck。TorchNPU 侧 test/npu 树 504 未取到，不虚构用例名。

## unknown 清单

U-T1 TorchNPU test/npu 用例名（blocked，504）；U-T2 test_privateuseone_python_backend.py 在 1eba9b3 是否存在（unknown，404/503）；U-T3 ROCm 文档站文本许可（unknown）；U-T4 MindSpore r2.5.0 LICENSE（partial，master 核对 Apache-2.0）；U-T5 CANN/HCCL 配套逐项表（unknown，沿用 U1/U2/U6）；U-T6 vLLM 树内 CUDA/ROCm 职责页（unknown）。

## 修订记录（2026-10-09，按初审 B17-C09/C10）

- C09：unsupported_dtype 限定为 Storage 方法生成范围。复核上游 backend_registration.py L295–340（L318–319 原文 takes effect only when the storage method needs to be generated）与 TorchNPU __init__.py L203–205（for_storage=True）；正文能力表与注意事项同步限定，AMP/tensor/算子覆盖另需证据。
- C10：最小测试节改写为逐能力表（9 行：设备选择/训练梯度/推理前向/dtype/覆盖/stream/编译/并行/引擎），每行含最小输入、方法链接、观察点、预期失败与通过/无法判断；gradcheck 义务限定于支持梯度的自定义算子（torch.library Warning 范围），前提取自 gradcheck.py L1987–2004（double 默认、非可微点、重叠内存）；TorchNPU 用例缺失处一律待执行设计。定向复核待执行。

## 第二轮复核修订（2026-10-09，按 B17-C10 剩余条件）

- dtype 行失败类型更正：Storage 未覆盖组合抛 RuntimeError（backend_registration.py L281–289 原文），不是 dispatcher NotImplementedError；三标记分开（文档支持性/方法适用性/实际结果）。
- stream 行补生产/消费先后、参考结果、有/缺依赖对照；集合通信行补 collective、rank 次序、输入/预期输出与无法判断条件。
- 新增性能对照待执行定义（同负载/基线/稳态计时/分布与分母，不设阈值）与标准算子训练分支前后向数值对照；gradcheck 不适用分支细化（换可微点/解析对照/记 unknown），forward 接近不作梯度通过。
