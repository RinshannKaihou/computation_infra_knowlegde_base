---
id: software-stack.runtime-execution-and-library-loading
title: 驱动初始化、运行时执行同步与库装载
type: reference
domain: software-stack
status: draft
platforms: [generic, nvidia, ascend, amd]
source_refs:
  - src.nvidia.cuda-toolkit-12-8
  - src.nvidia.cuda-12-8-runtime-api-pdf
  - src.nvidia.cuda-12-8-driver-api-init
  - src.nvidia.cublas-12-8
  - src.nvidia.cudnn-docs-latest-2026-10-09
  - src.nvidia.nccl-user-guide-2.32.3-2026-10-09
  - src.nvidia.cuda-samples-v12.8
  - src.huawei.cann-82rc1alpha001-acl-runtime-memory
  - src.huawei.cann-82rc1alpha001-acl-init-context-sync-2026-10-09
  - src.huawei.cann-82rc1alpha001-acl-appdev-flow-2026-10-09
  - src.huawei.cann-82rc1alpha001-acl-resnet50-sample-page
  - src.amd.hip-docs-6.3.3
  - src.amd.rocr-runtime-docs-6.3.3
  - src.amd.rocblas-docs-6.3.3
  - src.amd.miopen-docs-6.3.3
  - src.amd.rccl-docs-6.3.3
  - src.amd.rocm-examples-58fd61ac
  - src.linux-manpages-ldso-6.19
  - src.linux-manpages-ldd-6.19
  - src.linux-manpages-proc-pid-maps-6.19
  - src.pytorch.cuda-semantics-2.6
  - src.ascend.torch-npu-v7.2.0-pytorch2.6.0
updated_at: "2026-10-09"
summary: 固定版本对照 CUDA 12.8、CANN 8.2.RC1.alpha001 与 HIP 6.3.42134 的驱动/运行时初始化、stream/event 同步与错误发现时机、基础库职责和进程实载库身份的记录方法，并给出初始化→运算→同步→结果检查的最小验证方法定义。
related_ids:
  - software-stack.layers-and-boundaries
  - hardware.accelerator-execution-and-data-movement
  - software-stack.compatibility-evidence
verification:
  status: source_checked
  evidence_refs:
    - src.nvidia.cuda-toolkit-12-8
    - src.nvidia.cuda-12-8-runtime-api-pdf
    - src.nvidia.cuda-12-8-driver-api-init
    - src.huawei.cann-82rc1alpha001-acl-init-context-sync-2026-10-09
    - src.huawei.cann-82rc1alpha001-acl-appdev-flow-2026-10-09
    - src.amd.hip-docs-6.3.3
    - src.amd.rocr-runtime-docs-6.3.3
    - src.linux-manpages-ldso-6.19
    - src.linux-manpages-ldd-6.19
    - src.linux-manpages-proc-pid-maps-6.19
    - src.nvidia.cuda-samples-v12.8
    - src.amd.rocm-examples-58fd61ac
  notes: 仅对照第十五批取证记录（docs/research/batch-15-runtime-library-sources.md）所列固定版本文档页与源码快照核对接口语义、错误时机与装载规则；未在任何真实 GPU/NPU 设备上执行初始化、运算或同步，最小验证方法为方法层定义。
---

# 驱动初始化、运行时执行同步与库装载

## 范围与阅读方式

本文是运行时层的参考页，回答三件事：

1. 进程如何从「加载驱动」走到「运行时可用」——初始化路径、上下文建立与失败边界；
2. 任务下发后「主机返回」「设备完成」「异步错误被发现」三个时机如何区分，stream/event 同步接口各自的语义；
3. 运行时之上的数学/算子/通信基础库各管什么，以及如何记录一个进程**实际装载**的库身份。

固定版本声明：CUDA 侧以 [12.8 归档文档](https://docs.nvidia.com/cuda/archive/12.8.0/)为准（含同归档 Runtime API PDF 与 Driver API HTML）；CANN 侧以社区版 8.2.RC1.alpha001 文档树为准（URL 路径段 `/82RC1alpha001/`，页面 ID 为该版本树内编号，随版本变化，引用必须带版本限定）；AMD 侧以 HIP 6.3.42134（docs-6.3.3）与 ROCR 1.14.0（docs-6.3.3）为准；Linux 装载规则以 man-pages 6.19 为准。所有观察日期为 2026-10-09。

三条重要边界：

- **不宣称 API 一一等价。** 三栈都有「初始化、上下文、流、事件、同步、错误码」这些概念槽位，但接口名、返回形态和语义细节各不相同（例如 CANN 查询 Event 状态的接口是 `aclrtQueryEventStatus`，不存在 `aclrtQueryEvent`；HIP 的 `hipDeviceScheduleBlockingSync` 在 ROCm 平台是 Yield 的同义词）。本文逐栈引用原文，差异集中列在[各栈平台差异](#各栈平台差异不宣称等价的实例)。
- **框架层不在本文范围。** PyTorch 等框架在自己的设备后端里封装同步（如 PyTorch 2.6 CUDA semantics 的 asynchronous execution 一节描述框架级异步执行与同步接口，[文档](https://docs.pytorch.org/docs/2.6/notes/cuda.html)）；TorchNPU 是昇腾的 PyTorch 适配插件（[固定快照](https://github.com/Ascend/pytorch/tree/bc51ab84cc6f35c77aab1c59886e0ea43681a317)），框架语义不能替代运行时语义，反之亦然。层间归属见[主机到模型执行的软件栈分层](layers-and-boundaries.md)。
- **硬件数据移动另文。** 主机↔设备、设备内、设备间拷贝路径与硬件同步点见[加速器执行单元、内存层次与数据移动机制](../01-hardware/accelerator-execution-and-data-movement.md)；本文只展开其中「host↔stream 同步」这一层的运行时 API 语义。

本文未在任何真实设备上执行初始化或运算；所有接口语义为文档核对结论，第七节的验证流程是方法定义，不是已执行记录。

## CUDA 12.8：初始化与执行同步

### 驱动 API 初始化

`cuInit(Flags)` 初始化 Driver API，必须在当前进程任何其他 Driver API 函数之前调用，Flags 当前必须为 0；未调用时任何 Driver API 函数返回 `CUDA_ERROR_NOT_INITIALIZED`。函数页同时注记它「may also return error codes from previous, asynchronous launches」——初始化调用本身就可能成为此前异步错误的报告点（[CUDA Driver API 12.8 Initialization](https://docs.nvidia.com/cuda/archive/12.8.0/cuda-driver-api/group__CUDA__INITIALIZE.html)）。

### 运行时初始化：显式与隐式

按 [CUDA C++ Programming Guide 12.8 §3.2.1](https://docs.nvidia.com/cuda/archive/12.8.0/cuda-c-programming-guide/index.html)：

- 自 **CUDA 12.0** 起，`cudaInitDevice()` / `cudaSetDevice()` 会显式初始化运行时和指定设备的 primary context；因此检查 `cudaSetDevice()` 返回值中的初始化错误「变得非常重要」。
- 缺省这些调用时，运行时隐式使用 device 0 并按需自初始化。12.0 之前 `cudaSetDevice()` 不触发初始化，旧代码惯用空操作 `cudaFree(0)` 隔离初始化计时与错误——这只是历史背景，新版语义已变。
- error handling 与 version management 两组函数不触发运行时初始化。

**Primary context**：运行时为每个设备创建一个 primary context，在「第一个需要该设备活动上下文的运行时函数」处初始化，进程内所有 host 线程共享；创建过程含必要的 JIT 编译与设备代码装载。`cudaDeviceReset()` 销毁当前设备的 primary context，之后任意线程的下一个需要活动上下文的运行时调用会重建它（PG §3.2.1；[Runtime API 12.8 PDF](https://docs.nvidia.com/cuda/archive/12.8.0/pdf/CUDA_Runtime_API.pdf) §6.34）。§6.34 还说明：进程内 CUDA Runtime 的设备与 Driver API 的 CUcontext 是一一对应关系；`cudaInitDevice()` 初始化但不使上下文成为 current，`cudaSetDevice()` 经 `cuCtxSetCurrent()` 使其 current；primary context 保持活动直到 `cudaDeviceReset()`，且建议只在退出前或「从未指定 launch failure 恢复」时 reset。

Driver API 侧对同一 primary context 提供引用计数管理：`cuDevicePrimaryCtxRetain` / `Release` / `Reset` / `GetState` / `SetFlags`，context 在最后一次 release 时自动 reset（不同于 CUDA 4.0 及更早 runtime retain 后永久激活的行为）；`CU_CTX_SCHED_SPIN` / `YIELD` / `BLOCKING_SYNC` / `AUTO` 调度标志控制 host 线程等待 GPU 的方式（[Primary Context Management](https://docs.nvidia.com/cuda/archive/12.8.0/cuda-driver-api/group__CUDA__PRIMARY__CTX.html)）。

Runtime 与 Driver API 的关系（PDF §6.1/§6.34）：runtime 提供隐式初始化、上下文与模块管理，driver API 提供显式控制；`CUstream` 与 `cudaStream_t`、`CUevent` 与 `cudaEvent_t` 类型相同可互换；进程内同设备建多个 CUcontext 会显著降低性能，强烈不建议。

### 模块惰性装载

PG §20 Lazy Loading：cubin/fatbin/PTX 中 kernel 与数据的装载被延迟到首次使用。运行时部分随 CUDA 11.8 发布（11.7 起 `cuModuleLoad` 不再立即装载 kernel），需 R515+ 用户态库。环境变量 `CUDA_MODULE_LOADING` / `CUDA_MODULE_DATA_LOADING` 取值为 DEFAULT/LAZY/EAGER，**12.8 文档标注 default is LAZY**；`cuModuleGetLoadingMode()` 可查询（调用前须 `cuInit`）。§20.5 列出的风险直接影响初始化与首启延迟的故障判断：kernel 装载可能需要 context 同步，与并发自旋 kernel 反模式叠加可致死锁；启动时占满显存的分配器会导致 kernel 装载内存不足；自动调优场景需预热（[CUDA C++ Programming Guide 12.8](https://docs.nvidia.com/cuda/archive/12.8.0/cuda-c-programming-guide/index.html) §20 与附录环境变量表）。

### 主机返回、设备完成与异步错误发现时机

PG §3.2.12 Error Checking 给出的错误模型是本文「三个时机」区分的依据：

- **主机返回 ≠ 设备完成**：异步函数在设备完成任务前返回，其返回码**不可能包含设备侧异步错误**，只报告主机侧执行前错误（典型为参数校验）。
- **异步错误的发现时机**：异步错误「将由其后某个不相关的运行时函数调用报告」。要在某次异步调用后即时检查，唯一办法是调用 `cudaDeviceSynchronize()`（或其他同步机制）并检查其返回码。
- **kernel launch 无返回码**：须在 launch 后立即用 `cudaPeekAtLastError()` / `cudaGetLastError()` 取 pre-launch 错误。
- **每线程错误变量**：运行时为每个 host 线程维护一个初始为 `cudaSuccess` 的错误变量，每次出错被覆盖；`cudaPeekAtLastError()` 只读，`cudaGetLastError()` 读后复位为 `cudaSuccess`；`cudaErrorNotReady`（`cudaStreamQuery` / `cudaEventQuery` 可能返回）不算错误、不进该变量。API 参考另注记 `cudaGetLastError` 返回的是「同一 CUDA Runtime 库实例」的错误——静态链接时进程内可能存在多个 runtime 实例（PG §3.2.12；[Runtime API 12.8 PDF](https://docs.nvidia.com/cuda/archive/12.8.0/pdf/CUDA_Runtime_API.pdf) §6.4）。

注意：「sticky error」这一术语在 CUDA 12.8 的 PG、Runtime API（HTML 与 PDF）与 Driver API Error Handling 页均检索不到；12.8 文档的错误模型就是上面这套表述。涉及不可恢复错误的描述需另找固定版本来源，不得倒填进 12.8（见[已知证据缺口](#已知证据缺口)）。

### Stream 与 Event 同步接口

[Stream Management](https://docs.nvidia.com/cuda/archive/12.8.0/cuda-runtime-api/group__CUDART__STREAM.html)（12.8 归档）要点：

| 接口 | 语义 | 备注 |
|---|---|---|
| `cudaStreamCreate()` | 在调用线程当前上下文上创建异步 stream | 若无线程当前上下文，则选定设备 primary context、置为当前并初始化后再建 stream（同见于 `cudaStreamCreateWithFlags/WithPriority`） |
| `cudaStreamNonBlocking` 标志 | 不与 NULL stream 隐式同步 | 创建标志 |
| `cudaStreamSynchronize()` | 阻塞至该 stream 全部操作完成 | — |
| `cudaStreamQuery()` | 完成返回 `cudaSuccess`，未完返回 `cudaErrorNotReady` | 后者不算错误 |
| `cudaStreamDestroy()` | 立即返回；资源在设备完成该 stream 全部工作后自动释放 | 延迟回收语义，与 HIP 不同（见平台差异） |

每个函数页均带两条注记：可能返回之前异步启动的错误码；若该调用触发内部 CUDA 运行时初始化，还可能返回 `cudaErrorInitializationError` / `cudaErrorInsufficientDriver` / `cudaErrorNoDevice`——这三者是「驱动未就绪」类初始化失败在运行时的直接信号。

[Event Management](https://docs.nvidia.com/cuda/archive/12.8.0/cuda-runtime-api/group__CUDART__EVENT.html)（12.8 归档）要点：`cudaEventRecord()` 把调用时刻 stream 的内容捕获进 event（event 与 stream 须同上下文），**未 record 过的 event 查询返回 `cudaSuccess`**；`cudaEventQuery()` 全部捕获工作完成返回 `cudaSuccess`、否则 `cudaErrorNotReady`；`cudaEventSynchronize()` 等待捕获工作完成，`cudaEventBlockingSync` 标志决定 host 线程阻塞等待还是忙等；`cudaEventDestroy()` 可在未完成时调用、不阻塞，资源在完成时异步释放（之后再使用句柄是未定义行为）。`cudaEventElapsedTime` 计时分辨率约 0.5µs，且受同 stream 中间任务影响。

`cudaDeviceSynchronize()` 的语义以 [PG §3.2.8.5.3 Explicit Synchronization](https://docs.nvidia.com/cuda/archive/12.8.0/cuda-c-programming-guide/index.html) 为准：「waits until all preceding commands in all streams of all host threads have completed」。该函数在 12.8 归档中的函数级参考页缺失，见下面的取证缺口。

### 同步/异步 memcpy 的主机行为细则

[API Synchronization Behavior](https://docs.nvidia.com/cuda/archive/12.8.0/cuda-runtime-api/api-sync-behavior.html)（12.8 归档）：

- 同步版 H2D（pageable 主机内存）：先做 stream 同步，数据复制到 DMA staging 缓冲区后函数即返回，**DMA 本身未必完成**；
- pinned H2D 与 D2H（pageable/pinned）：对 host 同步；
- D2D：不做 host 同步；
- kernel launch 对 host 异步；
- 总原则原文：「Any CUDA API call may block or synchronize…undocumented behavior should not be relied upon」——除文档明写的同步行为外，不要依赖任何未记录的阻塞/同步副作用。Driver 侧的 `CU_CTX_SYNC_MEMOPS` 标志可强制同步内存操作真正同步（见 Primary Context Management 页）。

### CUDA 12.8 归档的取证缺口（如实记录）

`group__CUDART__DEVICE.html`（Device Management，含 `cudaDeviceSynchronize` / `cudaSetDevice` / `cudaGetDeviceCount` 的函数级参考页）在 12.8 HTML 归档返回 404，而 modules 页仍链接该地址；同归档 Runtime API PDF 的目录只有「6.2 Device Management [DEPRECATED]」而正文缺该章节。本文对这些函数的定位以 PG §3.2.8.5.3（`cudaDeviceSynchronize` 语义）与 PDF §6.34（初始化/复位语义）替代；live（非归档）docs 页存在但未核对版本，不作固定引用。

## CANN 8.2.RC1.alpha001（AscendCL）：初始化与执行同步

以下页面均取自 `https://www.hiascend.com/document/detail/zh/CANNCommunityEdition/82RC1alpha001/...`。页面 ID（如 `aclcppdevg_03_0022`）是该版本文档树的内部编号，随版本变化，**引用必须带 8.2.RC1.alpha001 限定**。版本绑定依据 URL 路径段、页内 doc_center/source 静态内容地址与同版本树交叉链接三重一致；其中 `aclcppdevg_03_0022`（aclInit）的 detail 页服务端 `<title>` 错渲染为另一版本页面标题，属站点缺陷，不影响正文内容归属（详见取证记录）。

### aclInit 与 aclFinalize

[aclInit（aclcppdevg_03_0022）](https://www.hiascend.com/document/detail/zh/CANNCommunityEdition/82RC1alpha001/API/appdevgapi/aclcppdevg_03_0022.html)：`aclInit(const char *configPath)` 是 AscendCL 初始化函数，configPath 指向 json 配置文件（可传 NULL）。约束：使用 AscendCL 接口开发应用必须先调用 `aclInit`；**一个进程内只能调用一次**；与 `aclFinalize` 配对使用。可配置项含 Dump、Profiling、错误信息上报模式（默认线程级别）、默认 Device（若同时调用 `aclrtSetDevice` 则后者优先）。

[aclFinalize（aclcppdevg_03_0023）](https://www.hiascend.com/document/detail/zh/CANNCommunityEdition/82RC1alpha001/API/appdevgapi/aclcppdevg_03_0023.html)：去初始化、释放进程内 AscendCL 资源；接口内默认增加 **2000ms 延时**用于 Device 业务日志回传（可用环境变量 `ASCEND_LOG_DEVICE_FLUSH_TIMEOUT=0` 去除）；进程退出前应确保已去初始化；不建议在析构函数中调用（单例析构顺序未知可致进程异常退出）。

### Device、隐式默认 Context/Stream 与引用计数

官方资源申请流程（[应用开发指南：运行管理资源申请与释放（aclcppdevg_000009）](https://www.hiascend.com/document/detail/zh/CANNCommunityEdition/82RC1alpha001/appdevg/aclcppdevg/aclcppdevg_000009.html)、[AscendCL初始化与去初始化（aclcppdevg_000007）](https://www.hiascend.com/document/detail/zh/CANNCommunityEdition/82RC1alpha001/appdevg/aclcppdevg/aclcppdevg_000007.html)）：必须 `aclInit` 初始化；按顺序申请 Device、Stream——`aclrtSetDevice` 指定 Device 的同时**隐式创建默认 Context 与默认 Stream**；一个 Device 对应一个默认 Context、一个默认 Stream，均无需显式释放，随 `aclrtResetDevice` 一并释放；释放顺序相反：`aclrtDestroyStream`（仅显式创建的）→ `aclrtResetDevice`。指南示例代码标注「不可以直接拷贝编译运行，仅供参考」。

[aclrtSetDevice（aclcppdevg_03_0039）](https://www.hiascend.com/document/detail/zh/CANNCommunityEdition/82RC1alpha001/API/appdevgapi/aclcppdevg_03_0039.html) 约束说明：

- 隐式创建的默认 Context 所含 Stream 数按型号不同：Atlas 推理系列 / 200 / 300 / 500 含 2 个 Stream（1 默认 + 1 内部同步）；Atlas A2 训练系列 / 800I A2 / A200I A2 Box / 200I / 500 A2 / Atlas 训练系列含 1 个默认 Stream。
- 同一进程多线程对同一 Device 调用 `aclrtSetDevice` 时，隐式默认 Context 是同一个。
- 与 `aclrtResetDevice` 是**引用计数**配对：每 setDevice +1、resetDevice −1，归零才真正释放；不配对不调用时进程退出也会释放（功能上无问题）；不同进程/线程可指定同一 Device。

[aclrtResetDevice（aclcppdevg_03_0040）](https://www.hiascend.com/document/detail/zh/CANNCommunityEdition/82RC1alpha001/API/appdevgapi/aclcppdevg_03_0040.html)：复位 Device 并释放资源（含默认 Context、默认 Stream 及其下创建的所有 Stream）；默认 Context/Stream 下任务未完成时系统等待完成后再释放。复位前建议顺序：`aclrtDestroyEvent` → `aclrtDestroyStream`（显式）→ `aclrtDestroyContext`（显式）→ `aclrtResetDevice`，否则可能业务异常。另有 `aclrtResetDeviceForce`（0041，可不配对使用）。

### 显式 Context 与推荐场景

[aclrtCreateContext（aclcppdevg_03_0059）](https://www.hiascend.com/document/detail/zh/CANNCommunityEdition/82RC1alpha001/API/appdevgapi/aclcppdevg_03_0059.html)、[aclrtSetCurrentContext（aclcppdevg_03_0061）](https://www.hiascend.com/document/detail/zh/CANNCommunityEdition/82RC1alpha001/API/appdevgapi/aclcppdevg_03_0061.html)：不显式创建则使用 `aclrtSetDevice` 隐式创建的默认 Context。隐式适合简单应用——多线程下执行结果取决于线程调度顺序；**显式 Context 推荐用于复杂应用**。`aclrtSetCurrentContext` 设置线程 Context，多次调用以最后一次为准；Device 已复位的 Context 不能再设置。若从未 `aclrtSetDevice`，首次 `aclrtCreateContext` 会为该 Device 绑定一个默认 Stream。注意 CANN 这套「隐式默认 Context + 可选显式 Context」机制与 CUDA primary context 不同构，不宣称等价。

### 同步与异步语义：三个时机在 CANN 的表达

[同步&异步API说明（aclcppdevg_03_0020）](https://www.hiascend.com/document/detail/zh/CANNCommunityEdition/82RC1alpha001/API/appdevgapi/aclcppdevg_03_0020.html) 给出关键界定（厂商原文）：「对于异步接口，主机线程调用异步接口后仅代表下发任务，在任务未完成前，异步接口已向主机线程返回成功。用户需要调用显式同步接口阻塞主机线程，等待任务完成，否则可能会导致训练或推理等业务异常、**Device断链掉卡**等未知情况。」该页同时建议尽量少用 Device 级同步以免拖延主机。

| 接口 | 语义 | 页面 |
|---|---|---|
| `aclrtSynchronizeStream(stream)` | 阻塞应用直到指定 Stream 中所有任务完成 | [0076](https://www.hiascend.com/document/detail/zh/CANNCommunityEdition/82RC1alpha001/API/appdevgapi/aclcppdevg_03_0076.html) |
| `aclrtSynchronizeDevice(void)` | 阻塞直到正在运算的 Device 完成运算（多 Device 时等待当前 Context 对应 Device） | [0056](https://www.hiascend.com/document/detail/zh/CANNCommunityEdition/82RC1alpha001/API/appdevgapi/aclcppdevg_03_0056.html) |
| `aclrtSynchronizeEvent(event)` | 阻塞直到指定 Event 完成（更细粒度） | 0020 页说明 |
| `aclrtStreamQuery(stream, *status)` | 查询 Stream 任务状态；status 为出参枚举 `aclrtStreamStatus`：`ACL_STREAM_STATUS_COMPLETE=0` / `NOT_READY=1` / `RESERVED=0xFFFF`；**函数返回值是 aclError（0 成功），状态经出参表达** | [0075](https://www.hiascend.com/document/detail/zh/CANNCommunityEdition/82RC1alpha001/API/appdevgapi/aclcppdevg_03_0075.html)、[1395](https://www.hiascend.com/document/detail/zh/CANNCommunityEdition/82RC1alpha001/API/appdevgapi/aclcppdevg_03_1395.html) |

Stream 创建（[aclrtCreateStream，0066](https://www.hiascend.com/document/detail/zh/CANNCommunityEdition/82RC1alpha001/API/appdevgapi/aclcppdevg_03_0066.html)）：每个 Context 对应一个默认 Stream（隐式创建），官方「推荐显式」创建；Stream 数量有上限且按型号不同——Atlas A2 训练 / 800I A2 / A200I A2 Box：1984；Atlas 训练系列：2048（多进程接近上限可能创建失败，建议分批）；Atlas 200I / 500 A2：512；推理系列与 200/300/500：1024。同一 Stream 中异步任务按下发顺序执行。

### Event 生命周期与状态查询

接口顺序：`aclrtCreateEvent` → `aclrtRecordEvent` → `aclrtStreamWaitEvent` → `aclrtResetEvent`。

- [aclrtCreateEvent（0079）](https://www.hiascend.com/document/detail/zh/CANNCommunityEdition/82RC1alpha001/API/appdevgapi/aclcppdevg_03_0079.html)：可用于两 Event 间耗时统计与多 Stream 同步等待；**资源在首次 `aclrtRecordEvent` 时才申请**，受单 Device Event 上限约束：A2 / 800I A2 / 200I / 500 A2 为 65536，训练系列 65535，推理系列 / 200 / 300 / 500 为 1023。
- [aclrtRecordEvent（0083）](https://www.hiascend.com/document/detail/zh/CANNCommunityEdition/82RC1alpha001/API/appdevgapi/aclcppdevg_03_0083.html)：异步接口（成功仅代表下发成功），捕获当前 Stream 已下发任务。
- [aclrtQueryEventStatus（0086）](https://www.hiascend.com/document/detail/zh/CANNCommunityEdition/82RC1alpha001/API/appdevgapi/aclcppdevg_03_0086.html)：`aclrtQueryEventStatus(event, *status)` 查询捕获任务状态，出参枚举 `ACL_EVENT_RECORDED_STATUS_COMPLETE` / `NOT_READY`；未 record 过的 Event 查询返回 COMPLETE。**注意接口名是 `aclrtQueryEventStatus`——CANN 没有 `aclrtQueryEvent`。** 多线程分别调用 Record 与 Query 时，官方提示时序可能乱序。
- [aclrtStreamWaitEvent（0091）](https://www.hiascend.com/document/detail/zh/CANNCommunityEdition/82RC1alpha001/API/appdevgapi/aclcppdevg_03_0091.html)：异步接口，使指定 Stream 后续任务等待 Event 捕获任务完成。

### 错误接口

- [aclGetRecentErrMsg（aclcppdevg_03_0028）](https://www.hiascend.com/document/detail/zh/CANNCommunityEdition/82RC1alpha001/API/appdevgapi/aclcppdevg_03_0028.html)：获取并**清空**同进程/线程内其他 AscendCL 接口调用失败的错误描述信息（进程级或线程级由 `aclInit` 的 err_msg_mode 控制，默认线程级）；建议每次接口调用失败都调用，否则错误信息可能堆积丢失；多次调用只有最后一次返回的字符串指针有效；获取失败返回 nullptr。
- [aclrtGetLastError（0144）](https://www.hiascend.com/document/detail/zh/CANNCommunityEdition/82RC1alpha001/API/appdevgapi/aclcppdevg_03_0144.html) / [aclrtPeekAtLastError（0143）](https://www.hiascend.com/document/detail/zh/CANNCommunityEdition/82RC1alpha001/API/appdevgapi/aclcppdevg_03_0143.html)：前者获取当前线程 Runtime 错误码并清空（无新错误前再取得 `ACL_SUCCESS`），后者仅获取不清空；level 当前仅支持线程级别。所有上述接口返回值统一「返回 0 表示成功，返回其他值表示失败，参见 aclError」（[aclError 枚举，1345](https://www.hiascend.com/document/detail/zh/CANNCommunityEdition/82RC1alpha001/API/appdevgapi/aclcppdevg_03_1345.html)）。注：另有已登记来源 src.huawei.cann-82rc1-aclerror 是 Python 树 82RC1 路径的错误码页，版本未核验，引用以本树 1345 页为准。

## ROCm/HIP 6.3.42134（docs-6.3.3）：初始化与执行同步

### hipInit 与隐式初始化（含 HSA runtime 角色）

[HIP 6.3.3 Initialization and version](https://rocm.docs.amd.com/projects/HIP/en/docs-6.3.3/reference/hip_runtime_api/modules/initialization_and_version.html)：`hipInit(unsigned int flags)` 显式初始化 HIP 运行时，flags 应为 0；「Most HIP APIs implicitly initialize the HIP runtime」，`hipInit` 用于控制初始化时机。`hipRuntimeGetVersion` 有平台警告：AMD 平台返回 HIP 版本，NVIDIA 平台返回 CUDA runtime 版本，两者无映射关系。

[HIP 6.3.3 how-to Initialization](https://rocm.docs.amd.com/projects/HIP/en/docs-6.3.3/how-to/hip_runtime_api/initialization.html)：「The HIP runtime is initialized automatically when the first HIP API call is made」；初始化内容包括读环境变量、设置活动/可见设备、装载必要库、建立内存拷贝与 cooperative launch 的内部缓冲、**初始化编译器以及 HSA runtime**、检查资源或设备缺失错误。`hipDeviceReset()` 删除当前进程创建的 stream/内存/kernel/event，之后任何新 HIP API 调用会重新初始化运行时。`hipSetDevice()` 绑定当前线程到指定 GPU 的上下文；其参考页称它「does no synchronization with the previous or new device, and has very little runtime overhead」。

HSA runtime 的角色（[ROCR documentation，docs-6.3.3](https://rocm.docs.amd.com/projects/ROCR-Runtime/en/docs-6.3.3/index.html)，页面标题 ROCR 1.14.0）：「The ROCm runtime (ROCR) is AMD's implementation of HSA runtime, which is a thin, user-mode API that exposes the necessary interfaces to access and interact with graphics hardware driven by the AMDGPU driver set and the ROCK kernel driver」。即 HIP 初始化向下经过 ROCR 到 AMDGPU/ROCK 驱动；HIP↔ROCR 的具体版本对应关系本轮未取证（见[已知证据缺口](#已知证据缺口)）。

### 同步与错误语义

[Device management](https://rocm.docs.amd.com/projects/HIP/en/docs-6.3.3/reference/hip_runtime_api/modules/device_management.html)：

- `hipSetDevice(int)`：设置后续 HIP 调用的默认设备，存于线程本地存储；多线程可用同一设备；返回 `hipSuccess` / `hipErrorInvalidDevice` / `hipErrorNoDevice`。
- `hipDeviceSynchronize(void)`：阻塞 host 线程直到当前设备所有活动 stream 的命令完成；文档原文 **"HIP does not support multiple blocking modes (yet!)"**——阻塞等待方式不可配。
- `hipDeviceReset()`：丢弃当前设备状态（删除全部 stream/内存/kernel/event），调用前须确保无其他线程在用。
- 调度标志 `hipDeviceScheduleBlockingSync` 在 ROCm 平台是 Yield 的同义词（hipSetDeviceFlags 页），与 CUDA 的阻塞同步语义不同。

[Stream management](https://rocm.docs.amd.com/projects/HIP/en/docs-6.3.3/reference/hip_runtime_api/modules/stream_management.html)：`hipStreamCreate` / `WithFlags` / `WithPriority` 创建异步 stream（堆分配，须 `hipStreamDestroy` 释放）；`hipStreamSynchronize()` 是 "host-synchronous: the host will block until the specified stream is empty"，遵循 null-stream 语义、受 `hipDeviceLaunchBlocking` 标志控制等待方式；`hipStreamQuery()` 全部完成返回 `hipSuccess`、否则 `hipErrorNotReady`（状态快照，典型用于调试）；`hipStreamDestroy()` 的语义原文是「If commands are still executing on the specified stream, some may complete execution before the queue is deleted. The queue may be destroyed while some commands are still inflight, or may wait for all commands queued to the stream before destroying it.」——上游给出的是**两种都可能**的销毁时机：队列可在仍有 in-flight 命令时被销毁，也可能等全部排队命令完成后才销毁；「some may complete」只说部分命令可能在队列删除前完成。**该段不建立任务取消保证**：不能据此认为 in-flight 命令被取消、删除或不再执行，也不能据此认为命令使用过的缓冲区已可安全释放。这与 CUDA `cudaStreamDestroy`「立即返回、资源待设备完成后自动释放」的延迟回收措辞不同；**销毁（队列生命周期结束）、同步（host 阻塞等待完成）与资源释放（内存/句柄回收）是三个概念**，各栈文档只承诺其明确声明的那一部分。

[Event management](https://rocm.docs.amd.com/projects/HIP/en/docs-6.3.3/reference/hip_runtime_api/modules/event_management.html)：`hipEventRecord()` 在指定 stream 记录；event 从 "recording" 到 "recorded" 的迁移发生在到达 stream 头部、此前命令全部完成后；未 record 就 query/synchronize 返回 `hipSuccess`（无挂起 event）；重复 record 覆盖旧状态，对正在 recording 的 event 再 record 结果未定义；`hipEventQuery()` 完成返回 `hipSuccess`、未完 `hipErrorNotReady`；`hipEventSynchronize()` 阻塞至 event 就绪；`hipEventBlockingSync` 标志使 `hipEventSynchronize` 阻塞等待（更低功耗、更高延迟），默认 flag 为主动同步。`hipEventElapsedTime` 分辨率约 1µs（CUDA 文档为约 0.5µs）。

[Error handling](https://rocm.docs.amd.com/projects/HIP/en/docs-6.3.3/reference/hip_runtime_api/modules/error_handling.html)：`hipGetLastError()` 返回同一 host 线程内任何 HIP 运行时调用产生的最后错误并复位为 `hipSuccess`；`hipPeekAtLastError()` 只读不复位；`hipGetErrorName` / `hipGetErrorString` 转字符串。**HIP 文档没有与 CUDA PG §3.2.12 等价的「异步错误由后续无关调用报告」整段表述**，该行为结论只按 CUDA/CANN 原文成立，HIP 侧不外推。

### 各栈平台差异（不宣称等价的实例）

| 槽位 | CUDA 12.8 | CANN 8.2.RC1.alpha001 | HIP 6.3.42134 |
|---|---|---|---|
| Event 状态查询 | `cudaEventQuery` 直接返回 `cudaSuccess` / `cudaErrorNotReady`（返回码表达） | **`aclrtQueryEventStatus`**（无 `aclrtQueryEvent`）：函数返回 aclError，状态经出参枚举 `ACL_EVENT_RECORDED_STATUS_COMPLETE/NOT_READY`；未 record 的 Event 查询返回 COMPLETE | `hipEventQuery` 返回 `hipSuccess` / `hipErrorNotReady`；未 record 查询返回 `hipSuccess` |
| Stream 状态查询 | `cudaStreamQuery` 以返回码 `cudaErrorNotReady` 表达 | `aclrtStreamQuery` 返回 aclError，状态经出参 `aclrtStreamStatus`（COMPLETE=0 / NOT_READY=1 / RESERVED=0xFFFF） | `hipStreamQuery` 返回 `hipSuccess` / `hipErrorNotReady` |
| 阻塞等待模式 | `cudaEventBlockingSync` 标志、`CU_CTX_SCHED_*` 调度标志可选阻塞/忙等 | 0020 页建议少用 Device 级同步；未见等价调度标志取证 | `hipDeviceSynchronize`「尚不支持多阻塞模式」；`hipDeviceScheduleBlockingSync` 在 ROCm 平台是 Yield 同义词 |
| Stream 销毁 | `cudaStreamDestroy` 立即返回、资源待设备完成后自动释放 | 释放随 `aclrtResetDevice` 或显式 `aclrtDestroyStream`；复位前建议先销毁显式资源 | `hipStreamDestroy`：队列可在仍有 in-flight 命令时被销毁、或等全部命令完成后再销毁（上游给出两种可能）；无任务取消保证，不能据此推断 in-flight 命令不再执行或缓冲区可释放 |
| Event Record 措辞 | `cudaEventRecord` 按「捕获 stream 内容」描述 | `aclrtRecordEvent` 自称异步接口，成功仅表示下发成功 | `hipEventRecord` 按 recording→recorded 状态迁移描述 |
| Event 计时分辨率 | `cudaEventElapsedTime` 约 0.5µs | 两 Event 间耗时统计（分辨率未取证） | `hipEventElapsedTime` 约 1µs |

## 基础库职责与装载身份

### 运行时之上的数学/算子/通信库职责

| 平台 | 库 | 职责（厂商表述归纳） | 来源与版本 |
|---|---|---|---|
| NVIDIA | cuBLAS | 「an implementation of BLAS on top of the NVIDIA CUDA runtime」；四组 API：cuBLAS、cublasXt、cublasLt（轻量、专用于 GEMM、可选算法与启发式）、cuBLASDx（不随 CUDA Toolkit 分发）；新 API 经 `cublas_v2.h`、句柄显式传递以支持多线程多 GPU 与可重入；legacy API 已 deprecated | [cuBLAS 12.8 §1](https://docs.nvidia.com/cuda/archive/12.8.0/cublas/index.html)（12.8 归档） |
| NVIDIA | cuDNN | 「a GPU-accelerated library of primitives for deep neural networks」 | [cuDNN 文档首页](https://docs.nvidia.com/deeplearning/cudnn/latest/)（**滚动 latest**，2026-10-09 观察时内容含 SM100/9.x 条目；归档站仅到 cudnn-897 即 8.9.7，本页不可作不可变快照） |
| NVIDIA | NCCL | 拓扑感知的 GPU 间通信原语库：集合通信（AllReduce/Broadcast/Reduce/AllGather/ReduceScatter/AlltoAll/Gather/Scatter）与点对点 send/receive；每个 collective 用单个 kernel 同时处理通信与计算；支持 PCIe/NVLink/InfiniBand Verbs/IP sockets；collective 带 stream 参数直接嵌入 CUDA 编程模型 | [NCCL User Guide Overview](https://docs.nvidia.com/deeplearning/nccl/user-guide/docs/overview.html)（**滚动 latest**，观察时页面标题 NCCL 2.32.3，2026-10-09；归档在 nccl/archives 与 nccl-archived） |
| AMD | rocBLAS | 「the ROCm BLAS library…implemented in the HIP programming language and optimized for AMD GPUs」 | [rocBLAS docs-6.3.3](https://rocm.docs.amd.com/projects/rocBLAS/en/docs-6.3.3/index.html) |
| AMD | MIOpen | AMD 开源深度学习原语库；用 fusion 优化内存带宽与 kernel 启动开销，提供自动调优基础设施；实现多种卷积优化算法 | [What is MIOpen? docs-6.3.3](https://rocm.docs.amd.com/projects/MIOpen/en/docs-6.3.3/what-is-miopen.html)（页面标题 MIOpen 3.3.0） |
| AMD | RCCL | 独立的多 GPU、多节点集合通信原语库，面向 AMD GPU 优化；使用 PCIe 与 xGMI 高速互联 | [RCCL docs-6.3.3](https://rocm.docs.amd.com/projects/rccl/en/docs-6.3.3/index.html)（页面标题 RCCL 2.21.5） |
| Ascend | aclnn | 单算子 API 执行方式：直接调用算子接口、无需 IR 定义；接口为「两段式」（`aclnnXxxGetWorkspaceSize` 计算 workspace + `aclnnXxx` 执行，stream 入参）；NN 算子与融合算子前缀 `aclnnXxx`，DVPP 算子前缀 `acldvppXxx`；调用时直接使用算子二进制包（Ascend-cann-kernels）中已编译好的算子、无需再编译 | [单算子调用流程（aclcppdevg_000017）](https://www.hiascend.com/document/detail/zh/CANNCommunityEdition/82RC1alpha001/appdevg/aclcppdevg/aclcppdevg_000017.html)（8.2.RC1.alpha001） |

两条边界说明：

- docs-6.3.3 是 AMD 文档站点的版本标签，其下各组件页标题版本并不一致（MIOpen 3.3.0、RCCL 2.21.5、ROCR 1.14.0、HIP 6.3.42134）——引用时分别记录，不要把 docs 标签当成组件版本。
- CANN 侧与 cuBLAS/cuDNN/NCCL 的对应归属（如 HCCL 通信库）超出本任务范围、未取证，本文不补齐（见[已知证据缺口](#已知证据缺口)）。

### 装载身份：四层区分

「库装上了吗」是四个不同的问题，证据各不相同：

| 层 | 问题 | 记录方法 | 来源 |
|---|---|---|---|
| 1. 搜索路径 | 动态链接器按什么顺序找库 | ld.so 搜索规则（见下） | [ld.so(8)，man-pages 6.19](https://man7.org/linux/man-pages/man8/ld.so.8.html) |
| 2. 包安装 | 磁盘上由发行包/安装器放置了哪些库文件及版本 | 属发行版/安装器管理范畴；本批来源未覆盖具体包管理工具，且「磁盘存在」不等于会被选中和装载 | （本批未取证，见缺口） |
| 3. 进程映射 | 运行中的进程实际把哪些文件映射进地址空间 | `/proc/<pid>/maps` | [proc_pid_maps(5)，man-pages 6.19](https://man7.org/linux/man-pages/man5/proc_pid_maps.5.html) |
| 4. 调用成功 | 库中函数是否真正被成功调用 | 函数级检查：初始化/算子调用返回码、错误接口（见各栈错误语义节） | 各栈 API 参考 |

**第 1 层：ld.so 搜索顺序**（[ld.so(8)](https://man7.org/linux/man-pages/man8/ld.so.8.html) DESCRIPTION，man-pages 6.19，页脚日期 2026-08-03，man7.org 取自 2026-09-09 tarball）。依赖字符串含斜杠时按路径名直接装载；否则依次：

1. `DT_RPATH`（`DT_RUNPATH` 不存在时）；
2. `LD_LIBRARY_PATH`（安全执行模式下忽略）；
3. `DT_RUNPATH`——只用于**直接** `DT_NEEDED` 依赖、不及子依赖，与 `DT_RPATH` 作用于整棵依赖树不同；
4. `/etc/ld.so.cache`（`-z nodefaultlib` 时跳过默认路径条目）；
5. 默认 `/lib`、`/usr/lib`（部分 64 位架构为 `/lib64`、`/usr/lib64`）。

该页还含 `$ORIGIN` / `$LIB` / `$PLATFORM` 动态串令牌与 glibc-hwcaps 目录（glibc 2.33+）等细节。

**第 2 层与第 3 层的间隙**：`ldd` 通常以 `LD_TRACE_LOADED_OBJECTS=1` 调用动态链接器，列出依赖解析到的对象路径与装载地址——这是「解析时」视图（[ldd(1)](https://man7.org/linux/man-pages/man1/ldd.1.html)，man-pages 6.19）。两条注意：其一，安全警告——某些情形 `ldd` 可能直接执行程序，**不可信二进制不要用 `ldd`**，可用 `objdump -p … | grep NEEDED` 替代，但 objdump 只显示直接依赖、`ldd` 显示整棵依赖树；其二，进程运行中经 `dlopen` 装载的库不在 `ldd` 输出之列。

**第 3 层：`/proc/<pid>/maps`**（[proc_pid_maps(5)](https://man7.org/linux/man-pages/man5/proc_pid_maps.5.html)，man-pages 6.19）：每行含地址区间、权限（r/w/x/s/p）、offset、dev、inode、pathname（映射的实际文件路径），可据此核对进程**实载**库身份；已删除文件标注 " (deleted)"；匿名映射无路径名。这是「进程映射」层的记录方法；要确认「调用成功」仍需函数级检查（第 4 层），例如 CUDA/CANN/HIP 各自的 last-error 接口。

## 失败候选分支

下表是形成候选假设的入口，不是根因判定；每条分支需同环境证据确认。

### 初始化失败

| 候选分支 | 观测 | 版本限定 |
|---|---|---|
| 驱动未加载/不可用（CUDA） | Driver API 任何函数返回 `CUDA_ERROR_NOT_INITIALIZED`（未 `cuInit` 或驱动不可用）；运行时首调触发初始化时返回 `cudaErrorInitializationError` / `cudaErrorInsufficientDriver` / `cudaErrorNoDevice` | [cuInit 页](https://docs.nvidia.com/cuda/archive/12.8.0/cuda-driver-api/group__CUDA__INITIALIZE.html)、[Stream Management 各函数页注记](https://docs.nvidia.com/cuda/archive/12.8.0/cuda-runtime-api/group__CUDART__STREAM.html)（12.8） |
| 设备不存在/无效（HIP） | `hipSetDevice` 返回 `hipErrorInvalidDevice` / `hipErrorNoDevice` | [Device management](https://rocm.docs.amd.com/projects/HIP/en/docs-6.3.3/reference/hip_runtime_api/modules/device_management.html)（6.3.3） |
| 初始化顺序/次数违反（CANN） | 未先 `aclInit` 即调用其他 AscendCL 接口；`aclInit` 一进程内重复调用（约束：只能一次，与 `aclFinalize` 配对） | [aclInit 0022](https://www.hiascend.com/document/detail/zh/CANNCommunityEdition/82RC1alpha001/API/appdevgapi/aclcppdevg_03_0022.html)（8.2.RC1.alpha001） |
| 上下文/流资源超限（CANN） | 显式 `aclrtCreateStream` 失败：Stream 上限按型号 1984/2048/512/1024，多进程接近上限可能创建失败（官方建议分批） | [aclrtCreateStream 0066](https://www.hiascend.com/document/detail/zh/CANNCommunityEdition/82RC1alpha001/API/appdevgapi/aclcppdevg_03_0066.html) |
| 惰性装载风险（CUDA） | 首启延迟拉长或死锁：kernel 装载需 context 同步，与并发自旋 kernel 反模式叠加可死锁；启动时占满显存的分配器导致 kernel 装载内存不足；自动调优需预热 | PG 12.8 §20.5（12.8 起默认 LAZY） |
| OS 层权限/设备节点访问 | 三栈文档均未覆盖设备节点权限机制；列为候选分支，需 OS 层证据（本批未取证） | 见[已知证据缺口](#已知证据缺口) |

### 动态链接失败

| 候选分支 | 观测 | 来源 |
|---|---|---|
| 搜索路径序导致选错库 | 同名库被 `DT_RPATH`/`LD_LIBRARY_PATH`/`DT_RUNPATH` 中更靠前的路径抢先装载；注意 `DT_RUNPATH` 不及传递依赖，`DT_RPATH` 作用于整棵依赖树 | [ld.so(8)](https://man7.org/linux/man-pages/man8/ld.so.8.html) |
| 安全执行模式下环境变量失效 | setuid/特权进程中 `LD_LIBRARY_PATH` 被忽略，与交互 shell 行为不一致 | 同上 |
| 「解析到」与「实载」不一致 | 用 `ldd`（解析时视图）与 `/proc/<pid>/maps`（运行时实载）双向核对；`dlopen` 装载的库只出现在后者 | [ldd(1)](https://man7.org/linux/man-pages/man1/ldd.1.html)、[proc_pid_maps(5)](https://man7.org/linux/man-pages/man5/proc_pid_maps.5.html) |
| 版本符号/ABI 不匹配 | 解析阶段失败的候选分支；具体符号版本机制本批来源未覆盖，版本配套证据分级见[如何判断版本配套是否有依据](compatibility-evidence.md) | 待取证项见缺口 |

### 异步执行失败（错误延迟发现的时机）

| 候选分支 | 观测 | 来源 |
|---|---|---|
| 异步错误由后续无关调用报告（CUDA） | 失败 kernel 的返回点在之后某个不相关的运行时调用；即时确认唯一办法是 `cudaDeviceSynchronize()`（或其他同步机制）并查其返回码 | PG 12.8 §3.2.12 |
| launch 前错误被忽略（CUDA） | kernel launch 无返回码；未紧跟 `cudaGetLastError()` 时 pre-launch 错误（配置非法等）混入后续错误变量 | 同上 |
| 错误变量串实例（CUDA） | 静态链接导致进程内多个 CUDA Runtime 实例时，`cudaGetLastError` 只报告同一实例的错误 | Runtime API 12.8 PDF §6.4 |
| 「下发成功」误当「执行成功」（CANN） | 异步接口返回成功仅代表下发；不显式同步可能导致「业务异常、Device断链掉卡」（厂商原文） | [同步&异步API说明 0020](https://www.hiascend.com/document/detail/zh/CANNCommunityEdition/82RC1alpha001/API/appdevgapi/aclcppdevg_03_0020.html) |
| 错误信息堆积丢失（CANN） | 接口失败后未调用 `aclGetRecentErrMsg()`，错误信息可能堆积丢失；该接口取并清，默认线程级 | [aclGetRecentErrMsg 0028](https://www.hiascend.com/document/detail/zh/CANNCommunityEdition/82RC1alpha001/API/appdevgapi/aclcppdevg_03_0028.html) |
| HIP 错误延迟行为未取证 | HIP 文档只有线程级 `hipGetLastError`/`hipPeekAtLastError` 语义，没有「异步错误由后续无关调用报告」的等价表述；不从 CUDA 外推 | [HIP Error handling](https://rocm.docs.amd.com/projects/HIP/en/docs-6.3.3/reference/hip_runtime_api/modules/error_handling.html) |

## 最小验证方法：初始化→运算→同步→结果检查

**方法层定义（本库未在真实设备执行）**。四步缺一不可，每步的记录项即该步的失败边界：

1. **初始化**：选定设备并建立运行时可用状态——CUDA 用 `cudaSetDevice()`（12.0 起显式初始化，查返回码）；CANN 用 `aclInit`（进程内一次）+ `aclrtSetDevice`（隐式默认 Context/Stream）；HIP 首次 API 调用隐式初始化（或 `hipInit(0)` 控制时机）。记录首个失败接口与返回码。
2. **运算**：分配设备内存、H2D 拷入、启动一个确定性最小算子/kernel（三栈官方示例见下）。
3. **同步**：显式同步点并读取其结果——`cudaDeviceSynchronize()` / `aclrtSynchronizeStream()` / `hipDeviceSynchronize()` 或等价的 host 同步拷贝；CUDA 与 HIP 在 kernel launch 后立即查 `GetLastError`（pre-launch 错误），CANN 在接口失败后调 `aclGetRecentErrMsg`。
4. **结果检查**：D2H 拷回后做数值或逻辑比对。**三栈官方示例中只有 CUDA vectorAdd 含数值校验**，其余须自行补比对环节（见下）。

### 官方最小示例（逐栈）

**CUDA：vectorAdd（[cuda-samples @ tag v12.8](https://github.com/NVIDIA/cuda-samples/tree/v12.8/Samples/0_Introduction/vectorAdd)，固定 commit `db3eea23946bca2e90a75eca2b5b3e07158a9e11`，BSD 三条款）**。流程：`cudaMalloc` ×3 → `cudaMemcpy` H2D ×2（同步版）→ `vectorAdd<<<…>>>` 启动 → 立即 `cudaGetLastError()` 检查 pre-launch 错误 → `cudaMemcpy(h_C, d_C, …, cudaMemcpyDeviceToHost)`（对 host 同步的拷贝，兼作同步点）→ 逐元素 `fabs(h_A[i]+h_B[i]-h_C[i]) > 1e-5` 校验，失败即 `EXIT_FAILURE` → `cudaFree`；每步错误以 `cudaGetErrorString` 打印。这是三栈中**唯一含官方数值结果校验**的最小示例。注意：第十三批曾以 master 分支观察 bandwidthTest 并记「README 提 Toolkit 12.4」，两批固定基准不同，引用时勿混。

**CANN：单算子调用流程（[应用开发指南 aclcppdevg_000017](https://www.hiascend.com/document/detail/zh/CANNCommunityEdition/82RC1alpha001/appdevg/aclcppdevg/aclcppdevg_000017.html)，8.2.RC1.alpha001）**。官方最小流程：`aclInit` → 申请运行管理资源（`aclrtSetDevice`、`aclrtCreateStream`）→ `aclrtMalloc` + `aclrtMemcpy` 传输 → `aclnnXxxGetWorkspaceSize` 计算 workspace、`aclrtMalloc` 申请、`aclnnXxx` 执行 → **`aclrtSynchronizeStream` 阻塞直到指定 Stream 所有任务完成** → `aclrtMemcpy` 拷回 → 释放（aclDestroyTensor 等、`aclrtDestroyStream`、`aclrtResetDevice`）→ `aclFinalize`。指南示例代码标注「不可以直接拷贝编译运行，仅供参考」；完整可编译样例指向 [ResNet-50 样例页（aclcppdevg_04_0024）](https://www.hiascend.com/document/detail/zh/CANNCommunityEdition/82RC1alpha001/appdevg/aclcppdevg/aclcppdevg_04_0024.html)。边界记录：该页 2026-10-09 仍链接 gitee.com/ascend/samples，而**该仓库已停止维护、迁移至 gitcode.com/cann**（gitee API 确认仓库描述，gitcode 新仓未核对）——引用样例工程时须注明旧链状态。校验逻辑（ResNet-50 top5 后处理）在样例工程中，非数值断言。

**HIP：rocm-examples（[固定 commit `58fd61ac9ed7313b84542f90ea3fc2ca9bd60813`](https://github.com/ROCm/rocm-examples/tree/58fd61ac9ed7313b84542f90ea3fc2ca9bd60813)，MIT）**。`HIP-Basic/saxpy/main.hip`：`hipMalloc` → `hipMemcpy` H2D → 默认流启动 `saxpy_kernel` → `HIP_CHECK(hipGetLastError())` → `hipMemcpy` D2H（注释明示 "This call blocks the host's execution until the copy is finished"）→ `hipFree`，**仅打印前 10 个元素、无数值校验**。`HIP-Basic/streams/main.hip`：2×`hipStreamCreate` → `hipMemcpyAsync`（pinned host）→ 两流各 launch → `hipMemcpyAsync` D2H → `hipDeviceSynchronize()` 等待两流完成 → `hipStreamDestroy`；同 stream 内 async 拷贝与 kernel 隐式同步（注释：非 pinned 时 `hipMemcpyAsync` 退化为同步）。**该仓库默认分支为 amd-staging（可变），引用必须带上述固定 commit。** 「结果检查」环节 HIP 侧以 API 语义（`hipGetLastError` + 同步 + 自行比对）补齐，不宣称示例含校验。

### 不可用/冲突的版本关系（保留 conflict，不强行闭合）

- **docs-6.3.3 组件版本不一**：MIOpen 3.3.0、RCCL 2.21.5、ROCR 1.14.0、HIP 6.3.42134 同挂一个 docs 标签，组件版本须分别记录，不能互相代表。
- **HIP↔ROCR 版本对应未取证**：HIP 初始化内部使用 HSA runtime，但 HIP 6.3.42134 与 ROCR 1.14.0 的配套关系本轮未核对官方发布说明，保留为未解决项。
- **滚动 URL**：cuDNN（latest）与 NCCL（观察时 2.32.3）文档首页是滚动页，职责表述稳定但不可作不可变快照；本文引用带观察日期 2026-10-09。固定归档存在（cuDNN 至 8.9.7；NCCL nccl/archives、nccl-archived），需要固定版本时应另选归档页。
- **CANN 页面 ID 版本绑定**：`aclcppdevg_*` 编号是 8.2.RC1.alpha001 树内编号，换版本即失效；跨版本引用须重新定位。
- **CUDA 12.8 归档缺陷**：Device Management 函数级参考页 404、PDF 缺章（见 CUDA 节末）；live 页未核对版本，不作替代固定引用。

## 已知证据缺口

- **HCCL 职责页未取证**：CANN 侧通信库与 NCCL/RCCL 的职责对照缺失，本文只在 aclnn 一行覆盖算子库。
- **CANN 驱动（HDK）边界资料未取证**：驱动↔运行时的接口边界（对应 CUDA cuInit/Driver API 一层）在 CANN 侧无来源，T02-02 source_discovery 中该项保持 blocked。
- **OS 层权限与设备节点机制未取证**：初始化失败的「权限」分支只列为候选，无本批来源支持具体机制。
- **cuDNN/NCCL 固定归档页未固定**：当前引用为滚动页 + 观察日期。
- **CUDA 12.8 归档 Device Management 章节 404/PDF 缺章**；live 页未核对。
- **「sticky error」术语在 12.8 文档检索不到**：不可恢复错误的术语化描述需另找固定版本来源。
- **HIP 异步错误报告行为未取证**：HIP 文档无等价段落，不外推。
- **包安装层记录方法未取证**：发行版包管理器（rpm/dpkg 等）与 CANN/ROCm/CUDA 安装器的包身份记录不在本批来源内。

## 来源核对范围

逐条主张与证据定位见[第十五批来源记录](../../docs/research/batch-15-runtime-library-sources.md)。主要来源：

- NVIDIA：[CUDA C++ Programming Guide 12.8](https://docs.nvidia.com/cuda/archive/12.8.0/cuda-c-programming-guide/index.html)（§3.2.1 初始化、§3.2.8.5.3 显式同步、§3.2.12 错误检查、§20 惰性装载）、[Runtime API 12.8 Stream](https://docs.nvidia.com/cuda/archive/12.8.0/cuda-runtime-api/group__CUDART__STREAM.html)/[Event](https://docs.nvidia.com/cuda/archive/12.8.0/cuda-runtime-api/group__CUDART__EVENT.html)/[API Synchronization Behavior](https://docs.nvidia.com/cuda/archive/12.8.0/cuda-runtime-api/api-sync-behavior.html)、[Runtime API 12.8 PDF](https://docs.nvidia.com/cuda/archive/12.8.0/pdf/CUDA_Runtime_API.pdf)（§6.1/§6.4/§6.34）、[Driver API 12.8 Initialization](https://docs.nvidia.com/cuda/archive/12.8.0/cuda-driver-api/group__CUDA__INITIALIZE.html) 与 [Primary Context Management](https://docs.nvidia.com/cuda/archive/12.8.0/cuda-driver-api/group__CUDA__PRIMARY__CTX.html)、[cuBLAS 12.8](https://docs.nvidia.com/cuda/archive/12.8.0/cublas/index.html)、[NCCL User Guide](https://docs.nvidia.com/deeplearning/nccl/user-guide/docs/overview.html)（滚动，2026-10-09）、[cuDNN](https://docs.nvidia.com/deeplearning/cudnn/latest/)（滚动，2026-10-09）、[cuda-samples v12.8 vectorAdd](https://github.com/NVIDIA/cuda-samples/tree/v12.8/Samples/0_Introduction/vectorAdd)。
- Ascend（均为 CANN 社区版 8.2.RC1.alpha001 树）：[aclInit 0022](https://www.hiascend.com/document/detail/zh/CANNCommunityEdition/82RC1alpha001/API/appdevgapi/aclcppdevg_03_0022.html)、[aclFinalize 0023](https://www.hiascend.com/document/detail/zh/CANNCommunityEdition/82RC1alpha001/API/appdevgapi/aclcppdevg_03_0023.html)、[同步&异步API说明 0020](https://www.hiascend.com/document/detail/zh/CANNCommunityEdition/82RC1alpha001/API/appdevgapi/aclcppdevg_03_0020.html)、[aclrtSetDevice 0039](https://www.hiascend.com/document/detail/zh/CANNCommunityEdition/82RC1alpha001/API/appdevgapi/aclcppdevg_03_0039.html)、[aclrtResetDevice 0040](https://www.hiascend.com/document/detail/zh/CANNCommunityEdition/82RC1alpha001/API/appdevgapi/aclcppdevg_03_0040.html)、[aclrtCreateContext 0059](https://www.hiascend.com/document/detail/zh/CANNCommunityEdition/82RC1alpha001/API/appdevgapi/aclcppdevg_03_0059.html)/[aclrtSetCurrentContext 0061](https://www.hiascend.com/document/detail/zh/CANNCommunityEdition/82RC1alpha001/API/appdevgapi/aclcppdevg_03_0061.html)、[aclrtCreateStream 0066](https://www.hiascend.com/document/detail/zh/CANNCommunityEdition/82RC1alpha001/API/appdevgapi/aclcppdevg_03_0066.html)、[aclrtStreamQuery 0075](https://www.hiascend.com/document/detail/zh/CANNCommunityEdition/82RC1alpha001/API/appdevgapi/aclcppdevg_03_0075.html)/[aclrtStreamStatus 1395](https://www.hiascend.com/document/detail/zh/CANNCommunityEdition/82RC1alpha001/API/appdevgapi/aclcppdevg_03_1395.html)、[aclrtSynchronizeStream 0076](https://www.hiascend.com/document/detail/zh/CANNCommunityEdition/82RC1alpha001/API/appdevgapi/aclcppdevg_03_0076.html)/[aclrtSynchronizeDevice 0056](https://www.hiascend.com/document/detail/zh/CANNCommunityEdition/82RC1alpha001/API/appdevgapi/aclcppdevg_03_0056.html)、[aclrtCreateEvent 0079](https://www.hiascend.com/document/detail/zh/CANNCommunityEdition/82RC1alpha001/API/appdevgapi/aclcppdevg_03_0079.html)/[aclrtRecordEvent 0083](https://www.hiascend.com/document/detail/zh/CANNCommunityEdition/82RC1alpha001/API/appdevgapi/aclcppdevg_03_0083.html)/[aclrtQueryEventStatus 0086](https://www.hiascend.com/document/detail/zh/CANNCommunityEdition/82RC1alpha001/API/appdevgapi/aclcppdevg_03_0086.html)/[aclrtStreamWaitEvent 0091](https://www.hiascend.com/document/detail/zh/CANNCommunityEdition/82RC1alpha001/API/appdevgapi/aclcppdevg_03_0091.html)、[aclGetRecentErrMsg 0028](https://www.hiascend.com/document/detail/zh/CANNCommunityEdition/82RC1alpha001/API/appdevgapi/aclcppdevg_03_0028.html)、[aclrtGetLastError 0144](https://www.hiascend.com/document/detail/zh/CANNCommunityEdition/82RC1alpha001/API/appdevgapi/aclcppdevg_03_0144.html)/[aclrtPeekAtLastError 0143](https://www.hiascend.com/document/detail/zh/CANNCommunityEdition/82RC1alpha001/API/appdevgapi/aclcppdevg_03_0143.html)/[aclError 1345](https://www.hiascend.com/document/detail/zh/CANNCommunityEdition/82RC1alpha001/API/appdevgapi/aclcppdevg_03_1345.html)、指南 [000007](https://www.hiascend.com/document/detail/zh/CANNCommunityEdition/82RC1alpha001/appdevg/aclcppdevg/aclcppdevg_000007.html)/[000009](https://www.hiascend.com/document/detail/zh/CANNCommunityEdition/82RC1alpha001/appdevg/aclcppdevg/aclcppdevg_000009.html)/[000017](https://www.hiascend.com/document/detail/zh/CANNCommunityEdition/82RC1alpha001/appdevg/aclcppdevg/aclcppdevg_000017.html)、[ResNet-50 样例页 04_0024](https://www.hiascend.com/document/detail/zh/CANNCommunityEdition/82RC1alpha001/appdevg/aclcppdevg/aclcppdevg_04_0024.html)。
- AMD：[HIP 6.3.3 Initialization and version](https://rocm.docs.amd.com/projects/HIP/en/docs-6.3.3/reference/hip_runtime_api/modules/initialization_and_version.html)、[how-to Initialization](https://rocm.docs.amd.com/projects/HIP/en/docs-6.3.3/how-to/hip_runtime_api/initialization.html)、[Device management](https://rocm.docs.amd.com/projects/HIP/en/docs-6.3.3/reference/hip_runtime_api/modules/device_management.html)、[Stream management](https://rocm.docs.amd.com/projects/HIP/en/docs-6.3.3/reference/hip_runtime_api/modules/stream_management.html)、[Event management](https://rocm.docs.amd.com/projects/HIP/en/docs-6.3.3/reference/hip_runtime_api/modules/event_management.html)、[Error handling](https://rocm.docs.amd.com/projects/HIP/en/docs-6.3.3/reference/hip_runtime_api/modules/error_handling.html)、[ROCR docs-6.3.3](https://rocm.docs.amd.com/projects/ROCR-Runtime/en/docs-6.3.3/index.html)、[rocBLAS docs-6.3.3](https://rocm.docs.amd.com/projects/rocBLAS/en/docs-6.3.3/index.html)、[MIOpen docs-6.3.3](https://rocm.docs.amd.com/projects/MIOpen/en/docs-6.3.3/what-is-miopen.html)、[RCCL docs-6.3.3](https://rocm.docs.amd.com/projects/rccl/en/docs-6.3.3/index.html)、[rocm-examples @58fd61ac](https://github.com/ROCm/rocm-examples/tree/58fd61ac9ed7313b84542f90ea3fc2ca9bd60813)。
- Linux 装载：[ld.so(8)](https://man7.org/linux/man-pages/man8/ld.so.8.html)、[ldd(1)](https://man7.org/linux/man-pages/man1/ldd.1.html)、[proc_pid_maps(5)](https://man7.org/linux/man-pages/man5/proc_pid_maps.5.html)（均 man-pages 6.19）。
- 框架层参照：[PyTorch 2.6 CUDA semantics](https://docs.pytorch.org/docs/2.6/notes/cuda.html)、[TorchNPU 固定快照](https://github.com/Ascend/pytorch/tree/bc51ab84cc6f35c77aab1c59886e0ea43681a317)（仅用于说明框架层边界，不作为运行时语义证据）。
