# 第十七批 T02-11 Ascend 传输同步来源记录

任务：T02-11 Ascend 主机传输、stream 与同步证据补齐（修订 `ascend-memory-oom-evidence.md`，只做加法）。取证日期 2026-10-09。实开方式：hiascend `document/detail/...` 页为 JS 渲染（webfetch 仅返回门户壳），正文证据取自 `doc_center/source/.../82RC1alpha001/...` 静态内容地址（200 且内容与页名相符）；页头版本未能直接核验者如实标注。

## 候选来源（10 项新登记）

| proposed-id | 精确 URL | 核对要点 |
|---|---|---|
| src.huawei.cann-82rc1alpha001-acl-host-mem | …/aclcppdevg_03_0101.html（FreeHost 同目录 0102） | 锁页、对齐、无隐式同步、配对释放；RC 形态申请 Device 内存 |
| src.huawei.cann-82rc1alpha001-acl-memcpy-sync | …/aclcppdevg_03_0105.html | 立刻复制；kind 预留自判；Device 间 peer 前提 |
| src.huawei.cann-82rc1alpha001-acl-memcpy-async | …/aclcppdevg_03_0106.html | 下发成功≠执行成功；64B 对齐；非 MallocHost 内含静默不可预知；EP/RC 形态差异 |
| src.huawei.cann-82rc1alpha001-acl-memcpy-kind | …/aclcppdevg_03_1807.html | 9 枚举；HOST_TO_BUF_TO_DEVICE 例外；DEFAULT 自判（全角逗号笔误照录） |
| src.huawei.cann-82rc1alpha001-acl-stream-sync | …/aclcppdevg_03_0076.html（同目录 0075/1395/0020） | SynchronizeStream/Query 出参枚举；三类同步；异步成功≠执行成功（0020 版本绑定弱） |
| src.huawei.cann-82rc1alpha001-acl-event-sync | …/aclcppdevg_03_0079.html（同目录 0083/0086/0091/0088） | 首次 Record 占资源；异步 Record/Wait；顺序与乱序警示；无 aclrtQueryEvent；0088/0089 未细读 |
| src.huawei.cann-82rc1alpha001-acl-data-transfer-guide | …/aclcppdevg_000010.html（974 行） | 样例固定顺序；释放顺序证据；示例不可直接编译运行；SynchronizeDevice 0056 |
| src.ascend.torch-npu-v7.2.0-copy-nonblocking | CopyKernel.cpp @bc51ab84（copy_between_host_and_device 定义 L88，分支区 L88–115；h2d/d2h 调用点约 L131–230，2026-10-09 raw 实测复核） | non_blocking 双分支原生语义；不与 CUDA 互证 |
| src.ascend.torch-npu-v7.2.0-pinned-host-alloc | CachingHostAllocator.cpp @bc51ab84（398 行） | event 驱动重用；free≠可重用；is_pinned 仅 CPU；pin_memory 留空 |
| src.ascend.torch-npu-v7.2.0-stream-event | streams.py @bc51ab84 + utils/NPUStream/Stream.cpp | synchronize 全 stream；直通绑定；SyncLaunchStream 反例；Event.reset 前提 |

CUDA 对照沿用既有 cuda-semantics-2.6，不新增、不作 NPU 证据。

## 主张—来源定位表（12 行）

MallocHost 语义与释放前提（0101/0102）；非 MallocHost 异步 H2D/D2H 静默不可预知（0106）；同步/异步分野与 kind 预留（0105/0106/0020）；样例顺序与不可编译声明（000010）；kind 九枚举与例外（1807）；三类同步分工与出参形态（0076/0075/1395/0020/0086/0088）；Event 资源与顺序/乱序（0079/0083/0086）；NPU non_blocking 双分支（CopyKernel 定义 L88、分支区 L88–115，2026-10-09 raw 实测复核）；CachingHostAllocator event 重用（L110–260）；synchronize 直通与反例（utils/streams/NPUStream/Stream.cpp）；memory_stats 事后读取与 num_ooms 先累加（memory.py + 既有 OOM 分支）；CUDA 三段表述仅限 CUDA + apis 表留空读法（cuda-semantics + apis.md）。

## 修订加法草案（已执行）

现有「异步执行与归因边界」节之后新增 §A（主机内存与 H2D/D2H）、§B（stream/event 三类同步）、§C（non_blocking 与 host buffer 生命周期）+ 待执行四步验证（复制→算子→同步→比对）与 F1/F2/F3 失败分支；适用边界与待确认清单追加限定。既有 allocator/workspace 行号引用一律未动。

## unknown/blocked 清单

接口支持版本化记录部分解除（已定位子项），整项关闭待执行轮复核行号 + 补 0088/0089 正文；SynchronizeEvent 超时语义未解除；non_blocking 切割条件为执行轮独立成段；HOST_TO_BUF_TO_DEVICE 使用情况与条件函数含义未解除（blocked）；0020/0086 版本绑定弱（引用保留限定）；CANN 页许可 unknown（非 blocker）；实机执行未解除（acceptance 3 待执行验证保持 open）。

## 修订记录（2026-10-09，按初审 B17-C02/C12）

- C02：non_blocking 条件同步分列。复核 CopyKernel.cpp L88–115（定义 L88、分支区）与 CachingHostAllocator.cpp L181–207（非 blocks 指针仅条件接口存在且 D2H 时提前返回，否则同步等待）；正文区分异步下发/调用阻塞/结果可读/buffer 复用四件事；条件接口存在不作运行能力断言。登记 notes 同步。
- C12：1807 静态原文逐项计数为 8 项（修订轮实测复核），正文与登记“九项”更正为八项全称；全角逗号保留为来源笔误。定向复核待执行。

## 第二轮复核说明（2026-10-09）

- C02/C12 第一轮复核已关闭；本轮未新增修订。T02-11 整任务仍不作完成声明（0088/0089 正文未细读、旧 allocator/workspace 非全量重核）。
