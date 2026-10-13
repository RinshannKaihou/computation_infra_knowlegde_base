# 第十七批审阅发现修订记录

修订日期：2026-10-09。针对[初审报告](batch-17-codex-review.md)（结论暂不通过；B17-C01–C13 共 13 项，11 P2 + 2 P3）逐项修订正文、研究记录与来源登记。本轮只做修订，未执行定向复核；知识条目保持 `draft`，不声明通过。

修订人取证方式：逐项重新取得固定 commit raw 原文件并计数行号（不用网页阅读器行号），CANN 静态正文经 `doc_center/source/.../82RC1alpha001/...` 实开复核，CUDA 12.8 归档页全文抓取复核。行号均为本次实测值。

## C01（P2）：workspace/graph 账户重复计数 — 已修订

- 反证复核：`CublasHandlePool.cpp L166–167`（`getNewWorkspace` 经 `CUDACachingAllocator::get()->allocate`）、allocator `L1443–1448`（活跃块插入增 `allocated_bytes/active`）、`L2775–2784`（graph 私有池块照常增 `total_allocated_memory/reserved_bytes`）。
- 修订：`gpu-memory-oom-evidence.md` 定义节加用途≠互斥账户声明；“独立账户”节改写为“用途分类与分配器可见性”；余量公式改写为归因清单（并列不相加，仅互斥同口径量可估算）；`inactive_split` 改证据提示并注 async/expandable 统计限制；记录表 workspace/graph 两行改为子集说明；Ascend 独立 workspace 不迁移。研究记录 append 修订附录；`cuda-caching-allocator` 登记 notes 追加三处行号证据。

## C02（P2）：non_blocking 条件同步 — 已修订

- 反证复核：`CopyKernel.cpp` 定义 L88、分支区 L88–115；`CachingHostAllocator.cpp L181–207`（非 blocks 指针仅条件接口存在且 D2H 时提前返回，否则 `AclrtSynchronizeStreamWithTimeout`）。
- 修订：`ascend-memory-oom-evidence.md` §C 改写为三分支分列（管理内存/非管理 D2H+条件接口/非管理 H2D 或无条件接口），明确异步下发/调用阻塞/结果可读/buffer 复用四分；条件接口存在不作运行能力断言。研究记录、CopyKernel 登记 notes 同步。

## C03（P2）：选项集漏项与虚构 getter — 已修订

- 反证复核：`CUDAAllocatorConfig.cpp L306–336`（含 `release_lock_on_cudamalloc` 及 `release_lock_on_hipmalloc`/`pinned_use_hip_host_register` 拼写别名）；`memory.py` 全文 grep（无 `_get_allocator_settings`，仅 `_set_allocator_settings` + `get_allocator_backend`）。
- 修订：选项表补全 10 项 + 别名说明（非新环境变量）；“Config.h parse”改为 `CUDAAllocatorConfig.cpp` 定位；记录表改用 `get_allocator_backend()` + env 快照并注请求≠生效。研究记录、`cuda-caching-allocator`、`torch-cuda-memory-source` 登记同步。

## C04（P2）：cudaFree 隐式同步遗漏 — 已修订

- 反证复核：12.8 MEMORY 页 `cudaFree` Description 全文（async 来源不做隐式同步，其他 `may perform implicit synchronization`）。
- 修订：AMD 节改写为按平台按分配来源的释放/同步契约，保留 CUDA“可能”及 async 例外；不作跨平台对照。

## C05（P2）：FreeAsync 返回后限制遗漏 — 已修订

- 反证复核：12.8 POOLS 页 `cudaFreeAsync`（返回后新下发访问/属性查询即 UB）。
- 修订：流序节补三时点与跨流依赖说明，纠正全局同步误读。

## C06（P2）：重复性判据不足 — 已修订

- 反证复核：2.6 Reproducibility 全文（benchmarking/非确定算法/determinism/未初始化内存四节）。
- 修订：重复控制扩展为清单；两次不同先记观察；第一稳定差异须字节一致、重复比较、可重复超差；可复现差异仍过任务容差门。

## C07（P2）：“须判错”过强 — 已修订

- 反证复核：Numerical accuracy → Linear algebra（非有限无保证、病态可静默错）。
- 修订：改三档处理（拒绝输入/进一步验证/已证错误），阈值与参考按任务预设；待执行设计，不编造结果。

## C08（P2）：Ascend 必交范围 — 有限样板已补，剩余子项保持 open

- 新增取证：`_format.py @bc51ab84` raw 全文 38 行（Format 枚举 15 成员）；AOL 简介静态正文（未审明支持不推荐/不保证效果）；新增登记 `src.ascend.torchnpu-npu-format-7.2.0`。
- 修订：Ascend 节改写为有限样板（存储格式枚举 + dtype 分支 + 官方边界），转换 API 与逐算子计算/累加精度逐项列为 unknown。按路线图强制门：unknown 不关闭必交子项，剩余缺口在主题验收时保持 open。

## C09（P2）：unsupported_dtype 范围扩大 — 已修订

- 反证复核：`backend_registration.py L295–340`（L318–319 Storage 范围原文）、TorchNPU `__init__.py L203–205`（`for_storage=True`）。
- 修订：能力表、注意事项、来源节同步限定为 Storage 转移方法范围；AMP/tensor/算子覆盖另需证据。

## C10（P2）：逐能力测试缺失 — 已修订

- 反证复核：`gradcheck.py L1987–2004`（double 默认、非可微点、重叠内存）、torch.library Warning（义务范围自定义算子）。
- 修订：最小测试节改写为 9 行逐能力表（含输入/方法/观察点/预期失败/通过-无法判断），训练/推理/自定义/标准算子四分支，gradcheck 不适用分支单列；TorchNPU 用例缺失处待执行设计。新增 `source_refs`/`evidence_refs` 两项审阅登记来源。

## C11（P2）：F0–F2 统计窗口不足 — 已修订

- 反证复核：`memory.py` 统计语义、CUDA semantics 选项与统计限制、allocator `L1410–1423`。
- 修订：F0–F2 补初始化/恢复/存活对象/同步/统计窗口、跨 backend 独立进程与分指标、四判据；`inactive_split` 改证据提示。保持待执行，无实测结果。

## C12（P3）：枚举计数 9→8 — 已修订

- 反证复核：1807 静态原文逐项计数 8 项。
- 修订：正文、研究记录、登记 notes 同步为八项全称；全角逗号保留为来源笔误。

## C13（P3）：12 种完整性断言 — 已修订

- 反证复核：`ScalarType.h L60–91`（Float8/ComplexHalf/亚字节量化/UInt16-64 等）。
- 修订：改为页列常见类型摘要 + 实现枚举差异；存在/支持/覆盖三分。`source_refs` 追加审阅登记的 scalar-type 来源。

## 第二轮复核修订（2026-10-09，针对第一次定向复核 5 项 OPEN）

- C01：摘要改用途/可见性口径；记录表 graph 行拆分为活跃量（同窗口 allocated 子集）与保留高水位（reserved 高水位子集）。
- C03：登记纠正 get_allocator_backend 查询 active backend（memory.py L925–934），env 单列请求配置；两者都不代表全部选项生效值。
- C08：补格式转换有限样板（FormatCastHelper/Kernel、FormatHelper base 判定，均 raw 实测；新增登记 2 项）；AOL 登记记录简介已取得；verification notes 说明有限核对范围；逐算子计算/累加精度等仍 unknown 并保持 open。
- C10：dtype 行失败类型更正为 RuntimeError 并三标记分开；stream/集合通信行补全对照要素；新增性能对照待执行定义与标准算子前后向对照；gradcheck 不适用分支细化。
- C11：F0–F2 改写为有序窗口 + 口径二选一；依据 memory.py L334–370 与 allocator L1637–1679（本次复核）。

## 第三轮修订（2026-10-09，针对第二次定向复核 2 项 OPEN）

- C08：转换门控改写为分支条件（NOT_SUPPORT vs 返回 false 三类）；补算子级 autocast 归属样板（AutoCastOps.cpp 全文实测，明确非计算精度证据）；新增登记 1 项；逐算子计算/累加精度仍 unknown 并保持 open。
- C11：峰值语义更正为 peak = current（CachingDeviceAllocator.h L25–32 本次实测）；正文 source_refs 追加复核补登来源。

## 第四轮修订（2026-10-09，针对第三次定向复核 C08 剩余两处限定）

- 候选门控与入口关系纠正（分支坐标、返回值契约、入口体未调用、核验范围限重载分支）。
- autocast 样板补第五种策略（fp32_append_dtype，不同宏，norm 三重载 L128–142）；计算/累加精度仍 unknown 并保持 open。

## 状态

第四轮修订完成，研究记录一份已 append 修订附录，登记 notes 修订 2 条（无新增登记）。`make check`/`make build` 待运行。第四次定向复核完成：两处限定均通过，无新增修改项；C08 继续 OPEN（逐算子计算/累加精度强制证据），累计 12 关闭/1 开放，不更新 backlog 任务状态。

## 第一次定向复核结果（2026-10-09）

上述“待运行/待复核”保留为修订提交时状态。审阅者现已完成[定向复核](batch-17-codex-recheck.md)：8 项 CLOSED，C01/C03/C08/C10/C11 共 5 项 P2 仍 OPEN，需按报告中的剩余关闭条件继续修订。本轮独立 `make check` / `make build` 均通过（83 content entries / 332 sources）；Batch 17 仍暂不通过，知识条目保持 draft，backlog 状态未动，未执行硬件验证。

## 第二次定向复核结果（2026-10-09）

第二轮修订后的[第二次定向复核](batch-17-codex-rerecheck.md)完成：本轮 C01/C03/C10 关闭，累计 11 项 CLOSED，C08/C11 共 2 项 P2 仍 OPEN。C08 的转换样板与元数据补证已核实，算子精度强制子项及门控范围仍需补齐/收紧；C11 的窗口顺序已修复，但峰值 reset 是 peak=current，不是归零，需要纠正原概括。本轮新增一个 native 统计实现反证登记，334→335 sources；补登后独立 `make check` / `make build` 均通过（83 content entries / 335 sources）。以上“待运行/待复核”及第一次结果保留为各阶段历史；最新关闭条件以第二次报告为准，Batch 17 仍暂不通过，条目保持 draft，backlog 状态未动，未执行硬件验证。

## 第三次定向复核结果（2026-10-09）

第三轮修订后的[第三次定向复核](batch-17-codex-third-recheck.md)完成：C11 关闭，累计 12 项 CLOSED，C08 仍 OPEN（P2）。C11 的 native 峰值重置语义与修订附录、来源引用一致；C08 的转换分支分类与普通 autocast 注册样板已核对，强制计算/累加精度证据仍缺，且候选门控/当前入口关系、原文件坐标与全文注册策略概括需按报告限定。独立 `make check` / `make build` 均通过（83 content entries / 336 sources），本次不增加登记。上述待复核状态与前两次结果保留为历史，最新关闭条件以第三次报告为准；Batch 17 仍暂不通过，条目保持 draft，backlog 未动，未执行硬件验证。

## 第四次定向复核结果（2026-10-09）

第四轮修订后的[第四次定向复核](batch-17-codex-fourth-recheck.md)完成：候选门控/入口关系、原文件坐标及 autocast 注册范围两处限定均已满足，本轮无新增修改项，不再把它们列为待办。C08 仅剩原有的逐算子计算/累加精度强制证据缺口，继续 OPEN（P2）；累计仍为 12 项 CLOSED、1 项 OPEN，Batch 17 暂不通过。独立 `make check` / `make build` 均通过（83 content entries / 336 sources），无新增登记。上述待复核状态及前三次判定保留为历史，最新剩余条件以第四次报告为准；条目保持 draft，backlog 未动，未执行硬件验证。

## 第五轮修订（2026-10-09，C08 计算精度样板）

针对第四次复核保留的逐算子计算/累加精度强制缺口，经 doc_center 静态 markdown 通道实开全文核对：aclDataType 全量枚举表、互推导关系规则、aclnnAdd 逐参数 dtype 表（含 A2 BFLOAT16 差异与 ACLNN_ERR_PARAM_INVALID 条件）、aclnnMatmul 逐项 dtype 表与 cubeMathType 四选项计算逻辑（KEEP_DTYPE；ALLOW_FP32_DOWN_PRECISION 即训练/推理 F32→F16、A2 F32→HF32；USE_FP16；USE_HF32 限 A2；A2 BFLOAT16 互推导排除项）。新增登记 4 项（336→340 sources）。正文补计算精度样板并同步 source_refs/evidence_refs、verification 范围说明、待确认清单。TorchNPU 侧 cubeMathType 透传实现未在快照内定位；累加精度官方未陈述，继续单列 unknown 并保持 open。`make check`/`make build` 通过（83 content entries / 340 sources）。第五次定向复核待执行；复核前不关闭 C08，不更新 backlog 任务状态。

## 第五次定向复核结果（2026-10-09）

上述第五轮提交描述保留为修订时记录。审阅者独立取得四个精确登记正文并完成[第五次定向复核](batch-17-codex-fifth-recheck.md)：互推导与 Add 支持样板核实，Matmul 官方计算逻辑契约取得；当前数据类型页为 19 项简写表而非所称全量/torch 对应列，Matmul 摘要还需补 KEEP_DTYPE、USE_FP16、推导/输出及一维例外条件，verification notes 的取得范围需同步。累加精度和固定实现关联仍缺证，C08 继续 OPEN（P2）；累计 12 项 CLOSED、1 项 OPEN，Batch 17 暂不通过。第四次通过的两处限定不重开，不新增发现 ID。独立 `make check` / `make build` 均通过（83 content entries / 340 sources），本次未改正文、研究记录或登记；条目保持 draft，backlog 未动，未执行硬件验证。

## 第六轮修订（2026-10-09，第五次复核三项要求）

- 数据类型页 19 行简写表更正（含 STRING、无 torch 列）与登记同步；Matmul 条件补全（KEEP/USE_FP16 产品限制、推导后类型规则、一维排除）与 SDK/实现分别记录；verification notes 同步两算子范围。累加精度与实现关联继续 unknown / OPEN。

## 第六次定向复核结果（2026-10-09）

[第六次定向复核](batch-17-codex-sixth-recheck.md)完成：第五次三项修订要求均已满足，正文、登记与研究附录一致，无新增修改项，不再列为待办。官方计算逻辑契约及其支持条件已核实；累加精度与固定实现关联继续缺证，C08 仍 OPEN（P2），累计 12 项 CLOSED、1 项 OPEN，Batch 17 暂不通过。独立 `make check` / `make build` 均通过（83 content entries / 340 sources），无新增登记。本轮未改正文、作者研究记录或登记；条目保持 draft，backlog 未动，未执行硬件验证。前五次输入与判定保留为历史，最新剩余条件以第六次报告为准。

## 第六次定向复核结果（2026-10-09）

第六轮修订后的[第六次定向复核](batch-17-codex-sixth-recheck.md)完成：三项修订（简写表、Matmul 条件、verification 范围）均通过，无新增修改项。C08 仅剩累加精度与固定实现关联证据缺口，继续 OPEN（P2）；累计 12 项 CLOSED、1 项 OPEN，Batch 17 暂不通过。条目保持 draft，backlog 未动，未执行硬件验证。

## 本地包取证（2026-10-09，C08 累加精度）

用户提供 CANN 8.2.RC1.alpha001 安装包已解包核对（见 batch-17-local-package-sources.md）：aclnn_matmul.h 确认两段式接口 + cubeMathType 参数（无累加陈述）；opp JSON 系 cost-model 非契约；fixpipe 注释系单实现细节未采用；包内无 doc/PDF。累加精度官方陈述在包内不存在，C08 该子项继续 OPEN。本地文件不合 registry URL 模式，未新增登记。
