# 第十七批技术审阅记录

**最新进展（2026-10-09）：第六次定向复核完成，累计 12 项 CLOSED、1 项 OPEN（C08，P2），Batch 17 仍暂不通过。** 第五次要求的来源范围、Matmul 适用条件及 verification 同步均已满足，无新增修改项；累加精度与固定实现关联仍缺证，详见[第六次定向复核记录](batch-17-codex-sixth-recheck.md)。[第五次](batch-17-codex-fifth-recheck.md)、[第四次](batch-17-codex-fourth-recheck.md)、[第三次](batch-17-codex-third-recheck.md)、[第二次](batch-17-codex-rerecheck.md)、[第一次](batch-17-codex-recheck.md)及下列初审输入和当时判定保留为历史，已通过项不重开。

审阅日期：2026-10-09（Asia/Shanghai）。**结论：暂不通过；B17-C01–C13 共 13 项发现，11 项 P2、2 项 P3，全部 OPEN。** 本记录交付初审结果，尚未修订知识正文或执行修订后的定向复核。

约定模型 / effort 为 `gpt-6.1-sol / xhigh`。执行者为本会话 Codex 主助手，与本批 Kimi 主会话及取证、撰写角色分开；未派发子代理。本会话没有提供可独立核验的实际模型与 effort 运行标识，故将上述配置记为用户约定，不把它写成已独立确认的执行元数据。此前来源审计中的账户资金不足是作者当时派发失败的历史，不是本次审阅的执行结果。

依据：[完整覆盖路线图](../full-coverage-roadmap.md)、[T02-08–T02-11 验收清单](../../plans/full-coverage-backlog.yaml)、[写作指南第 7 节](../authoring-guide.md#7-批次审阅约定)及 [AGENTS](../../AGENTS.md)。来源核对、发现修订、定向复核和实机验证分别记录，不以报告交付关闭发现。

## 审阅范围与输入身份

完整读取三篇新正文、昇腾内存全文及其相对 HEAD 的增量、领域索引、四份研究记录、来源审计、相应来源登记和元数据 schema。检查了稳定 ID、主归属、导航、draft 与 verification 的边界。昇腾已有 allocator/workspace 段落在本批未改变；本次重点独立核对新增传输与同步段，不将旧段落全部升级为重新取证完成。

| 任务 | 正文 | 初审输入 SHA-256 |
|---|---|---|
| T02-08 | [framework-backend-adaptation.md](../../knowledge/02-software-stack/framework-backend-adaptation.md) | `1cdb9b18f46f47bcba66c96cbe80aef8ef69f7757f50eb60520edeac2b010c56` |
| T02-09 | [gpu-memory-oom-evidence.md](../../knowledge/02-software-stack/gpu-memory-oom-evidence.md) | `2b40cfff9c208530bf9bf169e97c14a179e11c31053bd112e54a875acca6cb35` |
| T02-10 | [dtype-layout-and-precision-semantics.md](../../knowledge/02-software-stack/dtype-layout-and-precision-semantics.md) | `952a5f8fd518aef7d66ad99be63b23a1642df9263c99457bb621d6ffb2620035` |
| T02-11 | [ascend-memory-oom-evidence.md](../../knowledge/02-software-stack/ascend-memory-oom-evidence.md) | `77f7f55f78ea2b3674c59d04c2bb286968a57467fcc199b2635d863120acdb49` |

领域索引初审 SHA-256：`7e0cb816f3d1575f24b246eeee6a345baffe65812ae8f5fb483c0efa1eac6be0`。来源登记初审 SHA-256：`a3d590d8727f157213cb77f9170f5b64be209291f1adf55c5bf37e1a0d6ac416`（326 项）。四份研究记录初审身份如下，修订时须同步而非只改正文：

| 研究记录 | SHA-256 |
|---|---|
| [框架后端](batch-17-framework-backend-sources.md) | `85df0b66c360f5ee0a010ebbfe587058f14ecf7a2f858501179eab08a5a3eed8` |
| [GPU 内存](batch-17-gpu-memory-sources.md) | `95039a4c0537326e3a5f933c295393e321a3bf3f8a43aa556ba092acd56048a5` |
| [精度语义](batch-17-dtype-precision-sources.md) | `4d576e73ea04b36cd5bec14bc92edf3d76ad733da18ed5f44495375a0ca9c3ca` |
| [Ascend 传输](batch-17-ascend-transfer-sources.md) | `26451cf51ce98f3a0e1589144768d9fae61235c488aab3f9ce6b7108b6d64fa0` |

Batch 15、16 的最新来源审计及第二轮复核已有发现闭环，但通过范围均有限，不能推成全部兼容矩阵、CANN/TorchAir 页面和真实环境已验收。本次保留这些前置边界。

## 独立取证范围

- PyTorch 2.6 官方页面：CUDA/HIP semantics、numerical accuracy、reproducibility、tensor attributes、torch.library、AMP/AMP examples、testing、CUDA memory usage。读取了 PrivateUse1 当前教程，确认其为浮动版本，不能当成 2.6 不可变文档。
- PyTorch 固定 commit `1eba9b3aa3c43f86f4a2c807ac8e12c4a7767340`：重新取得并核对 `memory.py`、`CUDACachingAllocator.cpp`、`CUDAAllocatorConfig.cpp/.h`、`CublasHandlePool.cpp`、`backend_registration.py`、`ScalarType.h`、`gradcheck.py`、`_comparison.py`、dispatcher、CUDA/HIP 文档源码和 custom backend 文档源码。下文源码行号均由 raw 原文件计数，不使用网页阅读器的行号。
- TorchNPU 固定 commit `bc51ab84cc6f35c77aab1c59886e0ea43681a317`：重新取得 `__init__.py`、`autocast_utils.py`、`graphs.py`、`streams.py`、`CopyKernel.cpp` 和 `CachingHostAllocator.cpp`，核对注册及拷贝调用链。未执行这些文件。
- CANN：从 0106 detail 页公开 HTML 中定位其 `doc_center/source/zh/CANNCommunityEdition/82RC1alpha001/...` 静态内容地址，再读取 0101/0102/0105/0106/1807、0075/0076/0079/0083/0086/0088/0089/0091/1395/0020、数据传输指南和 AOL 入口。静态正文取得不代表页头版本或发行包已核验；0020/0086 的版本绑定限制保留。
- CUDA 12.8 归档：Memory Management、Stream Ordered Memory Allocator、Graph Management 相关内存节点、cuBLAS 数值与复现章节、FP8 入口；cuDNN 8.9.0 仅核对有关精度枚举，不将两版本拼成运行环境。
- AMD docs-7.14.0：精确 HIP memory/stream-ordered 页面、ROCm/rocBLAS/MIOpen 精度页及 MI200 alternate implementation。网页工具部分返回 429 后，使用 curl 读取同一精确 URL；没有以 6.3.3 替代 7.14.0。本轮确认 allocator 页的 Linux/Windows 条件和相关 API 的 Beta 标记，以及 FP8 FNUZ/OCP 架构矩阵。
- MindSpore r2.5.0 可插拔设备设计页、vLLM 固定 `b17039bccc17b94a2ea107272ad7bc93508708df` 平台接口及 v0.14.0 插件文档。

新增五个文件级来源登记用于本次反证：`src.pytorch.cublas-handle-pool-v2.6.0`、`src.pytorch.cuda-allocator-config-v2.6.0`、`src.pytorch.backend-registration-v2.6.0`、`src.pytorch.scalar-type-v2.6.0`、`src.pytorch.gradcheck-source-v2.6.0`。只登记链接和核对范围，临时下载正文未镜像到仓库。

## 发现与关闭条件

### B17-C01 — P2：workspace、graph pool 与框架账户重叠，余量公式会重复计数

位置：`gpu-memory-oom-evidence.md:48、60、68–72、114–118`；GPU 内存研究记录 L37、L45。

正文把 cuBLAS workspace 与 graph 私有池列为张量分配器以外的独立账户，并在 `total − (allocated + ... + workspace + graph pool)` 中相加。固定实现中，cuBLAS workspace 经 caching allocator 分配；graph pool 的活跃分配和运行时 segment 也分别进入 aggregate allocated/reserved。因此这些分类可以解释用途，不能无条件作为互斥账户求和。公式还遗漏设备 free 和普通 allocator 缓存，把空闲容量也纳入了“不可归属显存”。

证据：[CublasHandlePool.cpp L166–167](https://github.com/pytorch/pytorch/blob/1eba9b3aa3c43f86f4a2c807ac8e12c4a7767340/aten/src/ATen/cuda/CublasHandlePool.cpp#L166-L167)；[allocator 活跃统计 L1443–1448](https://github.com/pytorch/pytorch/blob/1eba9b3aa3c43f86f4a2c807ac8e12c4a7767340/c10/cuda/CUDACachingAllocator.cpp#L1443-L1448)、[graph pool 与 reserved L2775–2784](https://github.com/pytorch/pytorch/blob/1eba9b3aa3c43f86f4a2c807ac8e12c4a7767340/c10/cuda/CUDACachingAllocator.cpp#L2775-L2784)。这里是固定源码路径结论，不是对任意外部库的占用推断。

关闭条件：区分用途分类、allocator 可见性与 runtime/SMI 统计；仅将已证明互斥且同设备同时间口径的量用于余量估算，明确 free、reserved 和 graph 子集，保留无法测量项；同步研究记录和相应登记，不把 Ascend 的独立 workspace allocator 迁移成 CUDA 事实。

### B17-C02 — P2：`non_blocking=True` 仍可能同步，遗漏了 host allocator 的被调用分支

位置：`ascend-memory-oom-evidence.md:139–145`；Ascend 研究记录 L16、L24；CopyKernel 来源登记 notes。

正文由 CopyKernel 的外层分支得出“不做流同步”。但它调用的 `CachingHostAllocator_recordEvent` 对不在其 blocks 中的 host 指针通常会同步；仅在条件接口存在且方向为 D2H 时有提前返回分支。登记记录已提到部分同步行为，正文仍作无条件断言。直接由 `aclrtMallocHost` 取得内存也不自动说明它属于 TorchNPU 这个 allocator 的 blocks。

证据：[CopyKernel.cpp L97–102](https://github.com/Ascend/pytorch/blob/bc51ab84cc6f35c77aab1c59886e0ea43681a317/torch_npu/csrc/aten/common/CopyKernel.cpp#L97-L102)；[CachingHostAllocator.cpp L181–207](https://github.com/Ascend/pytorch/blob/bc51ab84cc6f35c77aab1c59886e0ea43681a317/torch_npu/csrc/core/npu/CachingHostAllocator.cpp#L181-L207)。

关闭条件：按 allocator 管理的 host 内存／非管理内存、H2D／D2H、条件接口是否存在分列已证行为和 unknown；区分异步下发、调用是否阻塞、结果可读与 buffer 可复用。同步原生语义段、待执行验证、研究记录及登记。不得把条件接口存在解释成已验证运行能力。

### B17-C03 — P2：分配器“完整选项集”漏项，记录表给出未取得的 getter

位置：`gpu-memory-oom-evidence.md:64、113`；GPU 内存研究记录 L32。

源码解析还接受 `release_lock_on_cudamalloc`，并兼容 `release_lock_on_hipmalloc` 与 `pinned_use_hip_host_register` 拼写；本文列出的“完整选项集”遗漏前者及别名。记录表的 `_get_allocator_settings` 在所引固定 `memory.py` 中没有定义；该文件有 `_set_allocator_settings` 和 `get_allocator_backend`，两者不能写作假定 getter。环境快照记录的是请求配置，未必等于初始化后实际生效值。

证据：[CUDAAllocatorConfig.cpp L306–336](https://github.com/pytorch/pytorch/blob/1eba9b3aa3c43f86f4a2c807ac8e12c4a7767340/c10/cuda/CUDAAllocatorConfig.cpp#L306-L336)；[memory.py L921–934](https://github.com/pytorch/pytorch/blob/1eba9b3aa3c43f86f4a2c807ac8e12c4a7767340/torch/cuda/memory.py#L921-L934)。别名是选项名，不据此断言存在新的 HIP 环境变量。

关闭条件：改为准确的完整表或明确只列选项子集；移除无来源 getter，分别记录请求配置、已证实际 backend 与能取得的快照配置元数据，注明获取接口和限制；修正 `Config.h parse` 的模糊定位，同步研究记录和登记。

### B17-C04 — P2：CUDA/HIP 释放行为对照遗漏 CUDA 的隐式同步条件

位置：`gpu-memory-oom-evidence.md:80`。

HIP 文档确实写明 `hipFree/hipFreeHost` 会隐式调用 `hipDeviceSynchronize`。但紧接着说 CUDA `cudaFree`“无此表述”，遗漏了 CUDA 12.8 明确写出的隐式同步条件，容易被读成 CUDA 释放不会同步。相同函数名或不同措辞不能建立这种对照。

证据：[CUDA 12.8 cudaFree](https://docs.nvidia.com/cuda/archive/12.8.0/cuda-runtime-api/group__CUDART__MEMORY.html) 的 Description：对 async allocator 返回的指针不做隐式同步，调用者须确保访问结束；对其他指针可能隐式同步。[HIP 7.14.0 Memory management](https://rocm.docs.amd.com/projects/HIP/en/docs-7.14.0/reference/hip_runtime_api/modules/memory_management.html) 的 hipFree/hipFreeHost 各自给出其同步说明。

关闭条件：逐平台、逐分配来源说明释放与同步契约，保留 CUDA 的“可能”及 async 来源例外，不将文档措辞差异写成无同步保证。

### B17-C05 — P2：异步释放只写执行到 free 的边界，遗漏 API 返回后的使用限制

位置：`gpu-memory-oom-evidence.md:76`。

“free 到达后访问即 UB”只覆盖设备执行边界。CUDA 文档还明确限制：`cudaFreeAsync` 返回后，再下发访问该内存的 GPU 工作或查询指针属性会产生未定义行为。若只按 stream 尚未执行到 free 判断，还可能提交不合法的新工作。

证据：[CUDA 12.8 Stream Ordered Memory Allocator → cudaFreeAsync](https://docs.nvidia.com/cuda/archive/12.8.0/cuda-runtime-api/group__CUDART__MEMORY__POOLS.html)。已下发访问需按 stream/event 建立顺序，与返回后新提交访问是两件事。

关闭条件：明确主机 API 返回、已有工作流序依赖、设备实际释放三个时点，并写出上述新工作／属性查询限制；分配侧说明同流后续工作可依靠流序，跨流须建立依赖，避免误读为每次都要先做主机全局同步。

### B17-C06 — P2：两次结果不同不能直接判为正常，单次超差也不等于稳定差异

位置：`dtype-layout-and-precision-semantics.md:116–119`；精度研究记录 L34。

方法只列 `manual_seed + benchmark=False`，随后要求 bitwise 比较，并将启用 benchmark 或使用非确定算法时的不同结果直接归为“正常”。这些设置没有排除算法自身非确定、其他 RNG、未初始化输入或同步错误。即使存在已知非确定性，也不能据此认定具体差异满足任务阈值。下一步又把首个超差点直接定义为“第一稳定差异”，没有重复观察或稳定性判据。

证据：[PyTorch 2.6 Reproducibility](https://docs.pytorch.org/docs/2.6/notes/randomness.html) 的 CUDA convolution benchmarking、Avoiding nondeterministic algorithms、CUDA convolution determinism 和 Filling uninitialized memory 分别说明这些条件。

关闭条件：分别记录随机性、算法与同步控制以及无法排除的原因；两次不同先作为观察，再按预设任务规则判断；定位首差前确认输入／权重字节、重复比较及差异位置是否稳定，证据不足时保留 unknown。可复现差异仍需按任务容差验收，不能自动判正常。

### B17-C07 — P2：将病态或非有限输入的风险声明写成“须判错”

位置：`dtype-layout-and-precision-semantics.md:121`；精度研究记录 L34。

上游说病态矩阵可能使特定线性代数算法静默出错，非有限输入则没有行为保证。正文把它们合并为“须判错”，没有残差、参考解或任务判据。检测到高 condition number、NaN/inf 或换设备结果不同，本身不能证明已观察输出必然错误，更不能直接归因于计算平台缺陷。

证据：[PyTorch 2.6 Numerical accuracy → Linear algebra](https://docs.pytorch.org/docs/2.6/notes/numerical_accuracy.html#linear-algebra-torch-linalg) 的 Non-finite values / Extremal values in linalg。

关闭条件：改为适用性／数值风险分支；给出需拒绝输入、需进一步验证、已证错误的不同判据。若保留错误反例，定义可检查的参考或残差和阈值；没有执行就标为待执行设计，不编造错误结果。

### B17-C08 — P2：T02-10 的 Ascend 格式与精度必交范围未完成

位置：`dtype-layout-and-precision-semantics.md:35、43、84–86、130`；精度研究记录 L21、L42。

正文对 Ascend 只给 AOL 入口，且明确承认算子 dtype/format、计算／累加精度和 TorchNPU 格式转换实现均未取得。未知状态记录正确，但不满足任务要求的三平台基础语义；路线图明确禁止用 unknown 自动关闭必交子项。本轮可以取得 AOL 静态目录，目录仍不是某个算子的支持表。

证据：[T02-10 acceptance/source_discovery](../../plans/full-coverage-backlog.yaml) 与[路线图材料门槛](../full-coverage-roadmap.md)；[CANN AOL 入口](https://www.hiascend.com/document/detail/zh/CANNCommunityEdition/82RC1alpha001/API/aolapi/operatorlist_00001.html)。

关闭条件：补一个有限且明确的 Ascend dtype/内部格式/转换及计算精度样板，取得相应官方正文与固定实现；不能取得累加精度的字段仍记 unknown，但说明哪些必交子项尚未验收。只有用户明确调整范围才能撤销必交项，本次不自行缩减路线图。

### B17-C09 — P2：`unsupported_dtype` 是 Storage 方法生成参数，不能作整个后端的否定清单

位置：`framework-backend-adaptation.md:63、95`；框架研究记录 L31；设备注册来源 notes。

TorchNPU 确实传入该列表，但 PyTorch 固定接口明确说它仅在生成 Storage 方法时生效。正文把它放进整体 dtype/layout 能力表并称“否定清单”，扩大到了后端 tensor、算子和 AMP 能力；这些面需要各自证据。

证据：[backend_registration.py L295–340](https://github.com/pytorch/pytorch/blob/1eba9b3aa3c43f86f4a2c807ac8e12c4a7767340/torch/utils/backend_registration.py#L295-L340)，特别是 L318–319；[TorchNPU 调用 L203–205](https://github.com/Ascend/pytorch/blob/bc51ab84cc6f35c77aab1c59886e0ea43681a317/torch_npu/__init__.py#L203-L205)。

关闭条件：将列表限定为自动生成的 Storage 转移方法限制；把 AMP 支持声明、tensor/算子 dtype 覆盖、layout/format 分开，未取得的范围不据此判为支持或不支持；同步研究记录和登记。

### B17-C10 — P2：T02-08 没有逐能力测试与判据，且把梯度测试设成通用门槛

位置：`framework-backend-adaptation.md:55、59–68、78–84`；框架研究记录 L30、L44。

表格主要列实现存在性与“需验证”的提示，没有逐能力连接固定输入、观察点、预期失败、完整性／性能对照。dtype/layout、跨 stream 依赖、fallback 和并行／引擎尤其没有可判读的最小对照。又将 opcheck + gradcheck 写成适配成功必须项，而官方要求两者都用的范围是支持梯度计算的自定义算子；推理或无梯度路径不能照用该义务。gradcheck 默认精度等前提也未说明。

证据：[T02-08 acceptance](../../plans/full-coverage-backlog.yaml)；[torch.library → Testing custom ops / Warning](https://docs.pytorch.org/docs/2.6/library.html#testing-custom-ops)；[gradcheck.py L1987–2004](https://github.com/pytorch/pytorch/blob/1eba9b3aa3c43f86f4a2c807ac8e12c4a7767340/torch/autograd/gradcheck.py#L1987-L2004)。缓存上游例的存在不能补齐其他能力面。

关闭条件：逐能力提供最小输入／版本、测试或现有方法的精确链接、观察点、预期失败与通过／无法判断条件，显式区分训练、推理、自定义算子和标准算子。gradcheck 说明 dtype、可微点与重叠内存等前提及不适用分支；未取得 TorchNPU 用例时可提供待执行设计，不能虚构用例名或结果。

### B17-C11 — P2：F0–F2 的统计窗口和恢复状态不足以区分泄漏与分配失败

位置：`gpu-memory-oom-evidence.md:60、94、111、122`；GPU 内存研究记录 L45。

F0 重置 peak，但 F2 只写 OOM 后 empty_cache 和复跑，再比较 reserved.peak 与 num_ooms。peak 是历史最大值，OOM 次数只计事件；没有界定 F2 的统计重置、仍存活张量／失败现场引用、同步边界和干净进程对照，无法据此区分泄漏、缓存或容量失败。F1 切换 backend 时也未定义进程初始化边界。`inactive_split_bytes` 被称为“确诊键”，但 async backend 部分统计不适用，且固定实现对 expandable segment 不按普通 inactive_split 路径累计。

证据：[memory.py L246–268](https://github.com/pytorch/pytorch/blob/1eba9b3aa3c43f86f4a2c807ac8e12c4a7767340/torch/cuda/memory.py#L246-L268)；[CUDA semantics allocator 选项与统计限制](https://docs.pytorch.org/docs/2.6/notes/cuda.html#optimizing-memory-usage-with-pytorch-cuda-alloc-conf)；[allocator L1410–1423](https://github.com/pytorch/pytorch/blob/1eba9b3aa3c43f86f4a2c807ac8e12c4a7767340/c10/cuda/CUDACachingAllocator.cpp#L1410-L1423)。这是实验设计缺口，不是已证存在泄漏。

关闭条件：定义每个对照的初始化／恢复、存活对象、同步和统计窗口；跨 backend 使用独立已固定配置的进程，选择各 backend 有意义的指标；给出持续 retained allocation、可释放缓存、额度／容量失败及无法判断的判据。统计名称改为证据提示，不能由单键直接确诊；保持待执行，无实测结果。

### B17-C12 — P3：固定 CANN 枚举页是八项，不是九项

位置：`ascend-memory-oom-evidence.md:127`；Ascend 研究记录 L24；memcpy-kind 来源 notes。

重新取得的 1807 静态正文包含 H2H/H2D/D2H/D2D、DEFAULT、HOST_TO_BUF_TO_DEVICE、INNER_DEVICE_TO_DEVICE、INTER_DEVICE_TO_DEVICE，共八项。正文和登记写九项；登记括号内的成员数也只有八项。

证据：[CANN 82RC1alpha001 aclrtMemcpyKind 原文](https://www.hiascend.com/doc_center/source/zh/CANNCommunityEdition/82RC1alpha001/API/appdevgapi/aclcppdevg_03_1807.html)。

关闭条件：按固定页改为八项或移除不必要总数，同步研究记录和登记；页中 DEFAULT 的全角逗号另保留为来源笔误，不自行补出第九个成员。

### B17-C13 — P3：Tensor Attributes 页的“十二种”不是固定实现的完整 dtype 集合

位置：`dtype-layout-and-precision-semantics.md:52`；精度研究记录 L9、L30。

2.6 页面确实写十二种，因此不是误读该页；但固定 v2.6.0 `ScalarType.h` 还包含四种 Float8、ComplexHalf、量化和 UInt16/32/64 等类型。把旧页面摘要直接写成 tensor dtype“共 12 种”，会让读者误判格式存在性；类型存在、算子支持和 autocast 覆盖又是不同问题。

证据：[Tensor Attributes 2.6](https://docs.pytorch.org/docs/2.6/tensor_attributes.html#torch-dtype)；[ScalarType.h L60–91](https://github.com/pytorch/pytorch/blob/1eba9b3aa3c43f86f4a2c807ac8e12c4a7767340/c10/core/ScalarType.h#L60-L91)。

关闭条件：去掉完整数量断言，或明确该页只列十二种常见类型并说明与固定实现的差异；不把源码枚举存在扩大为全设备／全算子支持或 FP8 autocast 支持，同步研究记录和登记。

## 路线图验收判定

| 任务 | 本轮判定 | 剩余门槛 |
|---|---|---|
| T02-08 | 未通过 | C09/C10；职责清单已具备，逐能力验证表和适用分支不足 |
| T02-09 | 未通过 | C01/C03/C04/C05/C11；AMD 指定页面本轮取得不关闭这些技术／设计问题 |
| T02-10 | 未通过 | C06/C07/C08/C13；Ascend 必交来源缺口不得作为已完成 |
| T02-11 | 未通过 | C02/C12；已有待执行复制流程不是实机验证结果 |

T02-11 acceptance 第三项要求交付“待执行验证”设计，并不要求本批实际跑设备。原研究记录把实机未执行直接写成 acceptance 3 open，应在修订时分开：文档设计是否足够由本批审阅判断，实机结果仍在独立验证轨道。本轮取得 0088/0089 正文，不表示作者已补写或这些发现已关闭。

## 未覆盖与保留限制

- 没有安装 wheel、检查制品 ABI／METADATA、运行设备代码、复现 OOM／图捕获、测性能或数值结果。未运行集群、容器或生命周期操作。
- 未完成 TorchNPU `test/npu` 全树及其运行条件核验；`test_cache_guard` 使用 Batch 16 已关闭发现的固定证据，未在本轮重新下载该测试文件或执行它。
- TorchNPU Python 封装的底层 C++ synchronize/event 绑定未全部重新取得；条件 async memcpy 的运行时版本／硬件支持未建立。既有 Ascend allocator/workspace 来源不计为本轮全量重核。
- CANN 取得静态正文不等于统一确认页头、发行包与硬件交集；AOL 目录不替代单算子精度资料。0089 的 timeout 为 -1 永久等待、正数毫秒，Atlas 200/300/500 只支持永久等待；这是本轮取证补充，后续修订引用时保留产品限定。
- CUDA Graph Management 只核对本批有关内存节点的段落；未全量审阅图 API。ROCm fork 与上游 allocator diff、实际 wheel 默认 backend、MIOpen/rocBLAS 全部 workspace 机制未验收。
- `distributed` 全页、channels-last 浮动教程、PrivateUse1 历史修订与所有许可页未逐条独立复核。新增来源许可沿用已有同 commit 根许可记录，未把它扩大到网站资产／全部第三方文件。
- 尚无发现修订与定向复核报告。知识条目保持原有 `draft` 与限定 `source_checked`；本次初审反证说明后续需收紧或补充其核对范围，不能据结构检查提升为 `reviewed/reproduced`。

## 结构检查

初审修改前独立运行 `make check`：PASS，83 content entries / 326 sources。新增审阅证据登记后运行 `make check` 与 `make build`：均 PASS，83 content entries / 331 sources，生成 `build/catalog.json` 与 `build/catalog.md`。本轮未修改 `src/kb/`，未新增或执行设备实验。结构检查与构建不证明技术正确性、远程内容有效性或发现关闭；交付状态同步见[本批来源与交付记录](batch-17-source-audit.md)。
