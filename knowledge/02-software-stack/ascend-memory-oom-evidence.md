---
id: software-stack.ascend-memory-oom-evidence
title: 昇腾 NPU 内存与 OOM 证据
type: concept
domain: software-stack
status: draft
platforms: [ascend]
source_refs:
  - src.ascend.torch-npu-v7.2.0-pytorch2.6.0
  - src.huawei.cann-82rc1alpha001-acl-runtime-memory
  - src.huawei.cann-82rc1-aclerror
  - src.pytorch.cuda-semantics-2.6
updated_at: "2026-09-30"
summary: 区分昇腾 NPU 的物理设备内存、框架分配/保留、算子 workspace 与碎片证据；固定 TorchNPU/CANN 来源版本，说明 OOM 报错的抛出层与异步执行的归因边界。
related_ids:
  - software-stack.layers-and-boundaries
  - software-stack.ascend-documented-profile
  - software-stack.ascend-version-mismatch-triage
  - hardware.resource-topology
  - reliability.evidence-and-hypotheses
verification:
  status: source_checked
  evidence_refs:
    - src.ascend.torch-npu-v7.2.0-pytorch2.6.0
    - src.huawei.cann-82rc1alpha001-acl-runtime-memory
    - src.huawei.cann-82rc1-aclerror
  notes: 核对 TorchNPU v7.2.0-pytorch2.6.0 固定 commit 的内存 API、分配器与 workspace 实现、选项解析和 OOM 文案，CANN 8.2.RC1.alpha001 内存管理页与 82RC1 错误码页，以及 PyTorch 2.6 CUDA 语义页的对照小节；未在 NPU 环境安装或运行任何代码。
---

# 昇腾 NPU 内存与 OOM 证据

## 定义与要解决的问题

“NPU out of memory”是一条框架或运行时错误文本，不直接等于“设备物理内存被张量用完”。判断一次 OOM 的证据位置，至少要分开四层：

1. **物理设备内存**：HBM 等片上内存的总量与空闲量，以及驱动、固件和运行时的自身占用；
2. **框架分配器**：torch_npu 的 caching allocator 从运行时批量取得（reserved）再切分给张量（allocated）的部分，以及切分产生的不可释放碎片；
3. **算子 workspace**：算子下发使用的独立工作区，与张量分配器不是同一账户，报错文案也不同；
4. **异步执行的时间错位**：设备侧错误可能在触发它的主机调用之后才浮现，报错栈位置不一定是根因位置。

本文固定 TorchNPU `v7.2.0-pytorch2.6.0`（commit `bc51ab84cc6f35c77aab1c59886e0ea43681a317`）与 CANN 8.2.RC1.alpha001 版本化页面作为证据基线。选项集和文案随版本变化——同一仓库 master 分支的分配器配置项已经不同——引用前必须固定版本。本文不是任何生产环境的内存配置建议，也不构成该快照与任一 CANN/HDK/硬件组合的配套声明。

## 机制与关键关系

### 物理设备内存与运行时固定占用

[CANN 8.2.RC1.alpha001 的内存管理总体说明](https://www.hiascend.com/document/detail/zh/CANNCommunityEdition/82RC1alpha001/API/appdevgapi/aclcppdevg_03_0094.html)支持以下官方声明：系统为防大页不足会提前预留大页内存；应用可用 `aclrtGetMemInfo` 查询空闲大页（`ACL_HBM_MEM_HUGE`）与普通内存（`ACL_HBM_MEM_NORMAL`）；在 Ascend EP 形态下，首次训练/推理会把 AI CPU 算子从 Host 搬到 Device 缓存，占用约 100M–200M Device 内存，仅 Device 重启才释放。这意味着“设备总量 − 框架看到的占用”存在不为零的固定差值，差值本身不是泄漏证据。

`aclrtMalloc` 的官方语义：在 Device 上分配线性内存、首地址 64B 对齐、申请 size 向上对齐 32B 后再加 32B（1G 大页申请除外）、不初始化内容、接口内部不做隐式 Device/流同步、成败立即返回；文档同时建议避免频繁申请释放，改为预分配或二次管理（[aclrtMalloc](https://www.hiascend.com/document/detail/zh/CANNCommunityEdition/82RC1alpha001/API/appdevgapi/aclcppdevg_03_0095.html)）。torch_npu 的 caching allocator 正是建立在这一层之上的“二次管理”。

框架内查询物理视角的入口是 `torch_npu.npu.mem_get_info`，返回底层 `_npu_getDeviceMemories` 的 (free, total)（[`__init__.py` L469–477](https://github.com/Ascend/pytorch/blob/bc51ab84cc6f35c77aab1c59886e0ea43681a317/torch_npu/npu/__init__.py#L469-L477)）。npu-smi 等系统工具的显存口径本轮未核对，不能与上述 API 数字直接对齐。

### 框架分配器：allocated、reserved 与碎片

TorchNPU 固定快照的内存 API 集中在 [`torch_npu/npu/memory.py`](https://github.com/Ascend/pytorch/blob/bc51ab84cc6f35c77aab1c59886e0ea43681a317/torch_npu/npu/memory.py#L18-L44)，包括 `memory_allocated`、`max_memory_allocated`、`memory_reserved`、`max_memory_reserved`、`memory_stats`、`memory_summary`、`empty_cache`、`empty_virt_addr_cache`（NPU 特有，仅解映射虚拟地址、保留物理 handle）、`set_per_process_memory_fraction`、`memory_snapshot` 等。两个口径必须分开：

- `memory_allocated` 返回 `allocated_bytes.all.current`：当前张量实际占用（[`memory.py` L343–358](https://github.com/Ascend/pytorch/blob/bc51ab84cc6f35c77aab1c59886e0ea43681a317/torch_npu/npu/memory.py#L343-L358)）；
- `memory_reserved` 返回 `reserved_bytes.all.current`：分配器从运行时取得并管理的总量（[`memory.py` L383–396](https://github.com/Ascend/pytorch/blob/bc51ab84cc6f35c77aab1c59886e0ea43681a317/torch_npu/npu/memory.py#L383-L396)）。

reserved 与 allocated 的差包含空闲缓存块和不可释放碎片；`memory_stats` 的 `inactive_split_bytes` 键即后者（[`memory.py` L170–241](https://github.com/Ascend/pytorch/blob/bc51ab84cc6f35c77aab1c59886e0ea43681a317/torch_npu/npu/memory.py#L170-L241)）。`memory_stats` 还带 `num_ooms`、`num_alloc_retries` 计数器，`memory_summary` 头部会打印 NPU OOMs / npuMalloc retries。

张量分配失败时，固定快照在错误码为 `ACL_ERROR_RT_MEMORY_ALLOCATION` 时进入 OOM 分支：先查 `aclrtGetMemInfo(ACL_HBM_MEM,…)`、累加 `num_ooms`、记录 trace、回调 OOM observer，然后抛出（[`NPUCachingAllocator.cpp` L1385–1439](https://github.com/Ascend/pytorch/blob/bc51ab84cc6f35c77aab1c59886e0ea43681a317/torch_npu/csrc/core/npu/NPUCachingAllocator.cpp#L1385-L1439)）：

```text
NPU out of memory. Tried to allocate … (NPU X; … total capacity; … already allocated;
… current active; … free; [… allowed; ]… reserved in total by PyTorch) If reserved memory is >>
allocated memory try setting max_split_size_mb to avoid fragmentation.
```

**同一个错误码有两个来源，必须先分开。** 除运行时分配调用返回该码外，分配器自身在进程额度检查时也设置它：`set_fraction` 为真且 `total_allocated_memory + size` 超过 `allowed_memory_maximum` 时直接失败返回，**此时还没有向运行时申请这次内存**（[`alloc_block` L2692–2694](https://github.com/Ascend/pytorch/blob/bc51ab84cc6f35c77aab1c59886e0ea43681a317/torch_npu/csrc/core/npu/NPUCachingAllocator.cpp#L2692-L2694)）。额度由 `setMemoryFraction` 按 `fraction × device_total` 设定（[`L1717–1724`](https://github.com/Ascend/pytorch/blob/bc51ab84cc6f35c77aab1c59886e0ea43681a317/torch_npu/csrc/core/npu/NPUCachingAllocator.cpp#L1717-L1724)），对应 `set_per_process_memory_fraction` 的效果；设了额度时，OOM 文案在 “free” 之后多一项 “allowed”（上文方括号处），且 observer 收到的容量参数是额度而非物理总量（[`L1391–1409`](https://github.com/Ascend/pytorch/blob/bc51ab84cc6f35c77aab1c59886e0ea43681a317/torch_npu/csrc/core/npu/NPUCachingAllocator.cpp#L1391-L1409)、[`L1429–1436`](https://github.com/Ascend/pytorch/blob/bc51ab84cc6f35c77aab1c59886e0ea43681a317/torch_npu/csrc/core/npu/NPUCachingAllocator.cpp#L1429-L1436)）。所以“设备仍有空闲却报 OOM”可以是进程额度到顶——调查时先查额度与实际生效配置，再对照物理空闲、reserved、active 与本次请求大小；不能从这个错误码直接认定运行时分配失败或碎片，也不能把 observer 的容量参数默认解释为物理总量。

两点边界：其一，这个 OOM 在分配路径上由框架分配器**同步**抛出，分配类 OOM 的报错位置是可信的；但耗尽发生的时刻仍可能早于报错，文案中的 max_split_size_mb 只是内置的碎片提示，不是已确诊的根因。其二，同一文件还有两处防御性分支：≥1EB 的请求直接报 “NPU out of memory. Tried to allocate more than 1EB memory.”（[`NPUCachingAllocator.cpp` L3515–3519](https://github.com/Ascend/pytorch/blob/bc51ab84cc6f35c77aab1c59886e0ea43681a317/torch_npu/csrc/core/npu/NPUCachingAllocator.cpp#L3515-L3519) 与 L3543–3547），与真实设备耗尽无关——同一条错误前缀不保证同一种根因。

### 算子 workspace 是另一本账

固定快照中 workspace 由独立的 `NPUWorkspaceAllocator` 管理，OOM 文案也不同：“NPU out of memory. NPUWorkspaceAllocator tried to allocate … take a try to set the environment variable TASK_QUEUE_ENABLE=1.”（[`NPUWorkspaceAllocator.cpp` L426–437](https://github.com/Ascend/pytorch/blob/bc51ab84cc6f35c77aab1c59886e0ea43681a317/torch_npu/csrc/core/npu/NPUWorkspaceAllocator.cpp#L426-L437)）。调查 OOM 时先按文案区分是张量分配器还是 workspace 分配器抛出，再决定看什么指标；两者相互挤压的关系在该快照代码中没有量化说明，不能假设它们共享一个可观测账户。

执行下发路径还有一层重试：`NpuUtils::IsOomError` 遇到 `ACL_ERROR_GE_DEVICE_MEMORY_ALLOCATION_FAILED` 时，首次先 `FreeDeviceCachedMemory` 再重试一次，仍失败才抛 “NPU out of memory. device id: …”（[`NpuUtils.cpp` L249–263](https://github.com/Ascend/pytorch/blob/bc51ab84cc6f35c77aab1c59886e0ea43681a317/torch_npu/csrc/framework/utils/NpuUtils.cpp#L249-L263)，[`OpParamMaker.cpp` L267/L289](https://github.com/Ascend/pytorch/blob/bc51ab84cc6f35c77aab1c59886e0ea43681a317/torch_npu/csrc/framework/OpParamMaker.cpp#L267)，`NPU_MAX_OP_EXEC_TRY_NUM=2`）。即下发路径的 OOM 报错之前可能已经发生过一次“清缓存重试”，这一动作本身会改变当时的内存状态。

内存相关错误码：`ACL_ERROR_RT_MEMORY_ALLOCATION = 207001`（“内存申请失败”）、`ACL_ERROR_GE_DEVICE_MEMORY_ALLOCATION_FAILED = 245002`（固定快照 vendored 头文件 [`rt_error_codes.h` L43](https://github.com/Ascend/pytorch/blob/bc51ab84cc6f35c77aab1c59886e0ea43681a317/third_party/acl/inc/acl/error_codes/rt_error_codes.h#L43)、[`ge_error_codes.h` L45](https://github.com/Ascend/pytorch/blob/bc51ab84cc6f35c77aab1c59886e0ea43681a317/third_party/acl/inc/ge/ge_error_codes.h#L45)）；错误码释义另见 [CANN 错误码页](https://www.hiascend.com/document/detail/zh/CANNCommunityEdition/82RC1/API/appdevgapi/aclpythondevg_01_0911.html)（URL 路径 82RC1，页头版本未经核验）。

### PYTORCH_NPU_ALLOC_CONF：固定版本的五个选项

固定快照在分配器单例初始化时读取 `PYTORCH_NPU_ALLOC_CONF`（[`NPUCachingAllocator.cpp` L886](https://github.com/Ascend/pytorch/blob/bc51ab84cc6f35c77aab1c59886e0ea43681a317/torch_npu/csrc/core/npu/NPUCachingAllocator.cpp#L886)），解析入口与选项分派在 [L1034–1080](https://github.com/Ascend/pytorch/blob/bc51ab84cc6f35c77aab1c59886e0ea43681a317/torch_npu/csrc/core/npu/NPUCachingAllocator.cpp#L1034-L1080)。该版本支持五个选项：

| 选项 | 该快照行为 | 解析位置 |
|---|---|---|
| `max_split_size_mb` | 超过该大小的空闲块可被切分上限；默认 size_t 最大值 | L946–961 |
| `garbage_collection_threshold` | 取值 (0,1) 开区间，默认 0；仅当同时设置了 `set_per_process_memory_fraction`（`set_fraction` 为真）且阈值大于零时，才在缓存搜索失败、申请新块**之前**触发主动回收；回收门槛 = 阈值 × 进程额度（`allowed_memory_maximum`）。只配该选项而不设 fraction 不启用这条路径；它不代表其他释放缓存的重试路径 | 解析 L963–975；生效条件 [L1353–1369](https://github.com/Ascend/pytorch/blob/bc51ab84cc6f35c77aab1c59886e0ea43681a317/torch_npu/csrc/core/npu/NPUCachingAllocator.cpp#L1353-L1369)；门槛 [L2624–2629](https://github.com/Ascend/pytorch/blob/bc51ab84cc6f35c77aab1c59886e0ea43681a317/torch_npu/csrc/core/npu/NPUCachingAllocator.cpp#L2624-L2629) |
| `expandable_segments` | 默认 false；True 时先用 `AclrtReserveMemAddress` 探测，失败告警并回退 false | L977–999 |
| `base_addr_aligned_kb` | 基地址对齐 | L1001–1019 |
| `page_size` | 仅允许 `1g` | L1021–1032 |

未识别的选项报 “Unrecognized CachingAllocator option”；`expandable_segments` 与 `max_split_size_mb`、`garbage_collection_threshold` 互斥（[L1068–1079](https://github.com/Ascend/pytorch/blob/bc51ab84cc6f35c77aab1c59886e0ea43681a317/torch_npu/csrc/core/npu/NPUCachingAllocator.cpp#L1068-L1079)）。`expandable_segments` 的实现用 `AclrtReserveMemAddress` 预留虚拟地址（代码注释说明预留量约为总内存的 1⅛，[L380–383](https://github.com/Ascend/pytorch/blob/bc51ab84cc6f35c77aab1c59886e0ea43681a317/torch_npu/csrc/core/npu/NPUCachingAllocator.cpp#L380-L383)）再分离映射物理页，小池页 2MiB、大池页 20MiB，且不支持 NPU tensor IPC（注释块 [L288–362](https://github.com/Ascend/pytorch/blob/bc51ab84cc6f35c77aab1c59886e0ea43681a317/torch_npu/csrc/core/npu/NPUCachingAllocator.cpp#L288-L362)；对应测试 `test/npu/test_expandable_segments.py`）。

**不要**把这组选项当成跨版本常量：2026-09-30 观察的 master 分支已改为另一配置类与另一组白名单选项。同样不要把 CUDA 的 `PYTORCH_CUDA_ALLOC_CONF` 选项集平移过来——两者名称相似但支持集、默认值和互斥关系分别由各自代码定义。

### 观测与证据落盘

- `memory_stats` / `memory_summary` 给出 allocated/reserved/inactive_split/num_ooms 等键值，是框架账户的第一手证据。
- 公开 API `memory_snapshot()`（在 `__all__` 中）返回分配器快照；私有 `_record_memory_history`/`_snapshot`/`_dump_snapshot` 虽在代码中存在（[memory.py L726–889](https://github.com/Ascend/pytorch/blob/bc51ab84cc6f35c77aab1c59886e0ea43681a317/torch_npu/npu/memory.py#L726-L889)），但固定快照的 API 对照文档把这三个的 NPU 兼容列留空（[`torch_npu_apis.md` L22513 附近](https://github.com/Ascend/pytorch/blob/bc51ab84cc6f35c77aab1c59886e0ea43681a317/docs/api/torch_npu_apis.md)）——代码存在不等于文档承诺兼容。
- `OOM_SNAPSHOT_ENABLE`（0 关；2 记录 state 级历史；其他非 0 值记录全部）挂接 OOM observer，OOM 时生成 `oom_snapshot_<pid>_<时间戳>.pickle`，目录由 `OOM_SNAPSHOT_PATH` 控制（[`OptionsManager.cpp` L567–578、L594–640](https://github.com/Ascend/pytorch/blob/bc51ab84cc6f35c77aab1c59886e0ea43681a317/torch_npu/csrc/core/npu/register/OptionsManager.cpp#L567-L640)）；该机制被 `#ifndef BUILD_LIBTORCH` 包裹，libtorch 构建下为空操作。
- `PYTORCH_NO_NPU_MEMORY_CACHING` 可绕过 caching allocator 直调运行时分配（OptionsManager.cpp L557–562），`TASK_QUEUE_ENABLE` 取值 0/1/2、默认 1（L537–551）——后者是异步下发默认开启的间接证据。

### 异步执行与归因边界

CUDA 对照（仅限 CUDA，不作 NPU 证据）：PyTorch 2.6 的 [CUDA 语义页](https://docs.pytorch.org/docs/2.6/notes/cuda.html#asynchronous-execution)明确 GPU 默认异步执行，设备错误到操作实际执行时才上报，stack trace 不显示发起请求的位置，可用 `CUDA_LAUNCH_BLOCKING=1` 强制同步定位；同页 [#memory-management](https://docs.pytorch.org/docs/2.6/notes/cuda.html#memory-management) 和 [#cublas-workspaces](https://docs.pytorch.org/docs/2.6/notes/cuda.html#cublas-workspaces) 分别说明 caching allocator 行为与 cuBLAS workspace 缓存。

NPU 侧在固定快照中只有间接证据：`TASK_QUEUE_ENABLE` 默认 1 表明算子经任务队列异步下发；下发路径的 OOM 有“清缓存重试”；统一错误文本在检查点抛出。**“OOM 或设备错误报在与根因无关的位置”这一具体错位陈述在该快照代码中没有直接表述**——本文把它作为机制推断保留：分配类 OOM 的抛出点可信（host 侧同步），但设备执行期错误的上报位置与真实耗尽时刻仍需目标版本的 CANN 日志机制文档或现场证据确认。

## 适用边界

- 全部 API 行号、选项集、文案和错误码仅对 TorchNPU `v7.2.0-pytorch2.6.0`（commit `bc51ab84`）负责；master 与历史版本均可能不同。
- CANN 内存页为 8.2.RC1.alpha001 版本化页面；`aclrtGetMemInfo` 的 HBM huge/normal 语义、AI CPU 缓存 100M–200M 占用按该页陈述；83RC1 同路径页面版本标识不一致且部分抓取失败，未采用。
- vendored CANN 头文件随 TorchNPU 快照固定，其与任一 CANN 发行版的对应关系未核验。
- 本文没有覆盖 npu-smi 等系统工具口径、CANN 算子 workspace 的版本化文档章节、以及任何实测数值。

## 常见误解

- **“memory_allocated 很低，所以设备空闲”**：reserved 中的空闲缓存、inactive_split 碎片、AI CPU 算子缓存（约 100M–200M，仅重启释放）和驱动/运行时占用都不在 allocated 里。
- **“报错建议 max_split_size_mb，根因就是碎片”**：那只是 OOM 文案的内置提示；确认碎片需要 `inactive_split_bytes` 等键值与分配历史证据。
- **“empty_cache() 释放设备内存给别的进程”**：它只释放分配器持有的未使用缓存；已分配张量不受影响；`empty_virt_addr_cache` 更进一步只解映射虚拟地址。另外注意：该快照 memory.py 的 docstring 多处沿用 CUDA 措辞（如提到 `nvidia-smi`、`cudaMalloc`），docstring 不是 NPU 行为证据。
- **“文档对照表里没有空缺即全部兼容”**：固定快照的 `docs/api/torch_npu_apis.md` 对部分内存 API（如 `memory_snapshot`、`get_allocator_backend`）的 NPU 列留空，对 `_record_memory_history` 等私有 API 的兼容列也留空；留空应读作未承诺，而不是已支持。
- **“同一条 ‘NPU out of memory’ 前缀是同一种根因”**：张量分配器、workspace 分配器、下发重试路径和 1EB 防御分支共用前缀，抛出层和语义各不相同。
- **“CUDA 的分配器环境变量和语义可以照搬到 NPU”**：`PYTORCH_NPU_ALLOC_CONF` 的选项集由 TorchNPU 代码定义且随版本变化；`PYTORCH_CUDA_ALLOC_CONF` 的 backend、roundup_power2_divisions、pinned_* 等选项在该快照中不存在。

## 例子与相关知识

一个典型的误归因链条：训练在中途某算子处报 “NPU out of memory”，按本文分层应先读文案前缀区分抛出层（张量分配器 / NPUWorkspaceAllocator / 下发重试路径），再取 `memory_stats` 的 allocated/reserved/inactive_split/num_ooms，并对照物理视角的 `mem_get_info`；若启用了 `OOM_SNAPSHOT_ENABLE`，分析对应 pickle；最后才评估是否与异步下发的错位有关。各层证据的采集与解释需要匹配目标版本，本文未提供可执行命令。

相关条目：[软件栈分层](layers-and-boundaries.md)（组件职责）、[昇腾文档配套档案](ascend-documented-profile.md)（版本条件）、[昇腾版本配套诊断](ascend-version-mismatch-triage.md)、[节点资源与拓扑](../01-hardware/resource-topology.md)（设备内存的物理背景）、[证据与假设](../08-reliability/evidence-and-hypotheses.md)（结论分级）。

## 来源与待确认问题

- [TorchNPU 固定快照](https://github.com/Ascend/pytorch/tree/bc51ab84cc6f35c77aab1c59886e0ea43681a317)：内存 API、分配器/workspace/下发路径实现、选项解析、OOM 文案、快照落盘机制、API 对照表空缺。
- [CANN 8.2.RC1.alpha001 内存管理总体说明](https://www.hiascend.com/document/detail/zh/CANNCommunityEdition/82RC1alpha001/API/appdevgapi/aclcppdevg_03_0094.html)与 [aclrtMalloc](https://www.hiascend.com/document/detail/zh/CANNCommunityEdition/82RC1alpha001/API/appdevgapi/aclcppdevg_03_0095.html)；[CANN 错误码页（URL 82RC1）](https://www.hiascend.com/document/detail/zh/CANNCommunityEdition/82RC1/API/appdevgapi/aclpythondevg_01_0911.html)。
- [PyTorch 2.6 CUDA 语义页](https://docs.pytorch.org/docs/2.6/notes/cuda.html)：仅作 CUDA 对照。
- 逐文件读取范围与失败记录见[第八批内存来源记录](../../docs/research/batch-08-memory-sources.md)。
- 待确认：npu-smi 口径；workspace 与张量池相互挤压的量化关系；expandable_segments 的生产效果；CANN 算子 workspace 的版本化文档章节；异步错位的直接官方证据；其他 TorchNPU/CANN 版本的选项集与文案。
