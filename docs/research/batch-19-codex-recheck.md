# 第十九批第一次定向复核

**最新进展：第三次复核已完成，累计 9 CLOSED / 0 OPEN；T03-05/T04-01 的原定有限内容/来源范围通过，T03-06 对 T03-05 的等待已解除。** 当前判定见[第三次复核](batch-19-codex-third-recheck.md)，[第二次复核](batch-19-codex-rerecheck.md)保留历史。下列输入、发现和 3 CLOSED / 6 OPEN 为第一次复核历史。

复核日期：2026-10-12（Asia/Shanghai）。作者修订和研究记录的 `2026-10-14` 保留为输入标签，不据此推导实际执行日期。

**结论：C02、C04、C07 转 CLOSED；C01、C03、C05、C06、C08、C09 仍 OPEN，累计 3 CLOSED / 6 OPEN。T03-05 / T04-01 暂不通过，T03-06 写作继续等待。** 本轮没有新增发现 ID；保留 OPEN 的要求均属于[初审关闭条件](batch-19-codex-review.md)，并核对了修订带来的相关分支。不能把本次两项定向复核解释为整个 Batch 19 已验收。

约定模型 / effort 为 `gpt-6.1-sol / xhigh`，本会话 Codex 主助手执行，与作者修订角色分开；未派发子代理。实际运行标识没有可独立核验的元数据，沿用[初审的执行说明](batch-19-codex-review.md)。依据[写作指南](../authoring-guide.md#7-批次审阅约定)、[T03-05 / T04-01 验收清单](../../plans/full-coverage-backlog.yaml)、[路线图](../full-coverage-roadmap.md#批次执行与来源入口)和 [AGENTS](../../AGENTS.md)，不扩大为硬件验证，不重开 Batch 17/18 的已关闭发现。

## 输入身份与复核范围

读取两篇正文、[首轮修订映射](batch-19-review-fixes.md)、两份研究定位表、来源审计、初审报告与相关登记。正文行号均指以下输入。来源登记和任务清单与初审身份相同；作者对两篇正文和两份研究记录的修订以当前文件身份为准。

| 输入 | SHA-256 |
|---|---|
| [T03-05 正文](../../knowledge/03-communication/rccl-runtime-and-verification.md) | `e3dc21c7d025503276e38c68aca3b33a6525764fece2ec547d21cacaba43a143` |
| [T04-01 正文](../../knowledge/04-data-storage/training-data-path.md) | `90ef263ae3dc2847b18237a32bf85cab1f757d6c221ee955e8267696a108ebbe` |
| [RCCL 来源记录](batch-19-rccl-sources.md) | `1da252617170b524fa02d81519753bfb7a783bfc0a5377d27ec5475bb43cb148` |
| [T04-01 来源记录](batch-19-t04-01-sources.md) | `cca911fe25b878405bd358938f33d0036cb4dc6a10d6f9ae20665f97c47ec61b` |
| [修订映射](batch-19-review-fixes.md) | `582d9b52a1b0996a5f73789e26f2e3b0e4cf66a3c04c250ea5f5c87c493a010f` |
| [来源审计](batch-19-source-audit.md) | `3f342d2ff899646bed5bf5090685c1d94ee5b2a77a16fe85777d283b38ab43ca` |
| [初审报告](batch-19-codex-review.md) | `d03ad2607ccc903b5432dd74acf16d59dc475454ff368b1a7646fea07b2c6e24` |
| [来源登记](../../sources/registry.yaml)（386 项） | `e84c3b6eb61a83a46dbbfd371e5de4112def120131e0c374181e8e5acbf8f51f` |
| [任务清单](../../plans/full-coverage-backlog.yaml) | `121826a4d499273e7f6a00735e0a53931eef5c097bd66ab6b2425fdbc36ddfe0` |

## 一次源复验

以默认 TLS 校验的 curl 只读重抓 30 份精确页面/固定源码，全部 HTTP 200，未编译或执行上游代码。网页工具取得 RCCL troubleshooting，api-library 与 CANN 静态页未能取得时改用 curl；两条获取路径的局限不当作作者结论成立的证据。

- `rocm-systems` 固定 commit `7da43026e4f2ef7600433c38c820732f7a205d22`：group.cc；rccl-tests common.cu/util.cu/timer.cc/README/PERFORMANCE.md；CHANGELOG 和 RegisterTests.cpp。
- RCCL `docs-10.1.0`：api-library、library-specification、fault-tolerance、env-variables、troubleshooting。重点复核 config 创建、GroupEnd 分支、日志过滤和初始化采集条件。
- TorchData 固定 commit `377e64c1be69a9be6649d14c9e3664070323e464`：stateful_dataloader.py、sampler.py；0.11.0 API 精确页重定向至 `meta-pytorch.org/data/0.11/`，版本标识保留。
- PyTorch 固定 commit `1eba9b3aa3c43f86f4a2c807ac8e12c4a7767340`：metadata.py、filesystem.py、serialization.py、state_dict_loader.py。未重做历史 28 文件关键词扫描。
- TorchNPU 固定 commit `bc51ab84cc6f35c77aab1c59886e0ea43681a317`：CopyKernel.cpp、CachingHostAllocator.cpp、streams.py。CANN 同版本官方静态正文：0106、0076、0086、0091、0020、0079、0083；没有把 0088/0089 超时细节或未知运行能力补成已证条件。

下列关键来源按原文件计数行号；八项与初审证据表共有的 SHA 均相同，未把发现解释为上游改版。未重新取证的兼容矩阵、MI300X acceptance、PR 合并讨论与许可范围沿用初审记录，不宣称本轮重新核对全部来源。临时原文和获取日志未镜像入库；既有 source ID 覆盖这些文档组/源码范围，本轮无新增登记。

| 关键证据 | 字节数 | SHA-256 |
|---|---:|---|
| RCCL group.cc | 38321 | `6bf37f4fd458eadb18ed18eea9af67bf4ad75b0097b78ba5a8528b19287ce5b5` |
| RCCL api-library HTML | 438446 | `a208670b5ca6c5b7adedce178a4e2dcad51459fe29a21fefcb34b6232c084cd5` |
| rccl-tests common.cu | 107420 | `1339f9535d68b748677bd817e88d02002a71ff27b7f2b7ce41fcaccaa505f9d7` |
| rccl-tests util.cu | 26709 | `a27340e1b6119d145a454689a782a53383fec3dddfc9f0c6acaf65bba3415429` |
| TorchData stateful_dataloader.py | 84336 | `426c3ef475481165f9a7d44238040f81de213a4e8ee58ad8fe734e52a2717830` |
| TorchData sampler.py | 7843 | `6dd9a2574f687ba80b4b4a562cca2a17d96676f5a92c096c1ff0770639536029` |
| TorchNPU CopyKernel.cpp | 15497 | `ffd690fc786007e40e9db49c38226a6d93a0b5f5fe66bfbed3a681618b77e5b2` |
| TorchNPU CachingHostAllocator.cpp | 12355 | `ed44e2afcd1d7084c3904e6fb95c21995b6577756f48abd3b955cd69cb21e2a9` |
| CANN 0091 静态正文 | 11333 | `760def2eb4dd7a58b3ceb77e0ed6ae9d62e638491016552109265783f85ea947` |

## 逐项状态

| ID | 状态 | 已接受修订与剩余范围 |
|---|---|---|
| C01 | OPEN | 五态、成功后依赖、Abort 线程前提和 deadline 已补；非阻塞创建 API/config 的连接仍缺，InProgress 分支条件应精确化。 |
| C02 | CLOSED | 实现微秒、文档 ms 冲突、每操作归一化、MPI `-a` 和其他模式边界已修正。 |
| C03 | OPEN | 单次重跑校验及环境门限已说明；最终命令的 datatype/placement 与计划行完整性门禁仍未固定。 |
| C04 | CLOSED | 304 限原单节点；跨节点同配置基线、实际路径记录/未确认分支与总体等待约束已加入。 |
| C05 | OPEN | 变量全名、目的集、pid/rank 与 MPI 传递边界已补；B-hang 仍只设 COLL 却要求检查初始化 NIC 日志。 |
| C06 | OPEN | 身份关系、三验证、DCP/CRC 收窄及四对照已展开；缓存失效预期仍跨阶段泛化，数据顺序判据须限定应用契约。 |
| C07 | CLOSED | 内建/用户 sampler iterator、dataset/fetcher 与非 Stateful fallback 责任已修正；worker/rank/消费边界保留。 |
| C08 | OPEN | 三路和路径限定已补；resume 告警被放入错误分支，0091 等待方向写反，完成观察仍需限定事件和返回状态。 |
| C09 | OPEN | 定位表、悬空 §4 和 PR #6843 已修订；正文核心主张附近的精确链接及部分映射仍未补全。 |

### C01 — OPEN：创建接口和条件分支仍需补齐

T03-05 L56–59 的 group 暂存、成功入队与设备完成区分、poll 成功再建依赖、Abort 线程和带外 deadline 已接受。剩余是初审明确要求的“创建接口/config”：L53 仍只给普通 `ncclCommInitRank`/InitAll，L56/L58 仅说 `config.blocking=0`，未说明通过哪个接口把 config 传入创建过程。api-library 明确给出 `ncclCommInitRankConfig(..., ncclConfig_t *config)` 与 `NCCL_CONFIG_INITIALIZER`；普通 InitRank 没有 config 参数。[RCCL API library 的 Communicator Configuration 和 InitRankConfig](https://rocm.docs.amd.com/projects/rccl/en/docs-10.1.0/api-reference/api-library.html)。

L56(d) 还应写成“进入后台 group job 分支、返回 InProgress 时”。源码 L921 同时要求 non-blocking 和 preconnect/async job 条件，并非仅 `config.blocking=0` 就一律走该分支；其他分支可正常返回成功。返回值判断不能被一种模式标签替代。[group.cc L919–958](https://github.com/ROCm/rocm-systems/blob/7da43026e4f2ef7600433c38c820732f7a205d22/projects/rccl/src/group.cc#L919-L958)。

下一次关闭条件：补初始化 config、传入 InitRankConfig 的有限调用关系，成功/InProgress/错误分别处理；只对实际返回 InProgress 的分支 poll 到成功再建立依赖。保留现有 Abort/deadline/设备完成边界，无需运行程序。

### C02 — CLOSED：默认计时口径已对齐实现

T03-05 L75 已改微秒，并明确 PERFORMANCE.md 的 ms 与实现冲突；默认每操作归一化、`-m`、MPI `-a` 0/1/2/3 和默认 Avg 有说明，`-C/-I/-G/device` 不再概括为同一种默认计时。重抓实现确认秒乘 `1e6` 与 `(us)` 表头，README 支持所列参数。[common.cu L1070–1087](https://github.com/ROCm/rocm-systems/blob/7da43026e4f2ef7600433c38c820732f7a205d22/projects/rccl-tests/src/common.cu#L1070-L1087)、[L1259–1266](https://github.com/ROCm/rocm-systems/blob/7da43026e4f2ef7600433c38c820732f7a205d22/projects/rccl-tests/src/common.cu#L1259-L1266)、[util.cu L780–787](https://github.com/ROCm/rocm-systems/blob/7da43026e4f2ef7600433c38c820732f7a205d22/projects/rccl-tests/src/util.cu#L780-L787)、[README L163–183](https://github.com/ROCm/rocm-systems/blob/7da43026e4f2ef7600433c38c820732f7a205d22/projects/rccl-tests/README.md#L163-L183)。正文近旁链接的剩余问题归 C09，不重开计时事实。

### C03 — OPEN：参数与最终命令、计划覆盖门禁未一致

T03-05 L77/L79 的单次 `-c 1`、重跑不证明所有计时迭代、`N/A` 不当零错误、MIN_BW 要求 unset 及四分说明已接受。源码确认重初始化后另跑校验，环境门限按 `0.9×设置值` 影响退出码。[common.cu L1192–1256](https://github.com/ROCm/rocm-systems/blob/7da43026e4f2ef7600433c38c820732f7a205d22/projects/rccl-tests/src/common.cu#L1192-L1256)、[L2757–2788](https://github.com/ROCm/rocm-systems/blob/7da43026e4f2ef7600433c38c820732f7a205d22/projects/rccl-tests/src/common.cu#L2757-L2788)。

L77 的 datatype 仍是“如 `-d half -o sum`，按目标声明”，placement 是“`-O` 明确”并补默认 both；L95 最终命令未带这些设置，仅称“上节固定参数”。实际该命令默认 Float/Sum/both，与 half 示例并非同一输入。参数化设计可以成立，但必须要求执行前选定并记入完整命令，或明确全文采用默认 Float/Sum/both，不把示例和实际调用混为已固定配置。[README L156–190](https://github.com/ROCm/rocm-systems/blob/7da43026e4f2ef7600433c38c820732f7a205d22/projects/rccl-tests/README.md#L156-L190)。

L96 的 P1 仍只列 exit 0/零 wrong/无越界，没有初审要求的“全部计划行完成且校验实际开启”条件。初审关闭门禁未随修订补入，不能仅因已写扫描参数便将覆盖记录省掉。

下一次关闭条件：让参数声明与最终命令一致；列出预期扫描行/placement 和实际输出核对要求。缺行、N/A、提前停止或未完成计划一律不判 P1；正确性通过与性能无基线时未判定继续分开。无需增加测试次数或平台范围。

### C04 — CLOSED：按有限设计接受路径与等待约束

T03-05 L92/L96–98 已将 304 仅留在单节点单进程八 GPU/8G 条件；两节点性能按同配置基线比较，无基线未判定。MPI/节点分配、hostname/local rank/device、transport/HCA/端口成为记录要求；RDMA 设备存在与实际 transport 已分开，未确认路径保留未确认分支。总体 wall-clock 期限要求执行前声明，`-T` 不被当作全程保证，超时保留证据并区别测试失败和原因未知。[固定 README 的多节点示例与 timeout 参数](https://github.com/ROCm/rocm-systems/blob/7da43026e4f2ef7600433c38c820732f7a205d22/projects/rccl-tests/README.md)、[RCCL troubleshooting 的系统与 RCCL 信息采集](https://rocm.docs.amd.com/projects/rccl/en/docs-10.1.0/how-to/troubleshooting-rccl.html)。

这是执行前固定输入/期限的文档设计通过，不代表已经取得 MPI 放置或 RDMA 运行证据；完整输入/校验覆盖的剩余要求归 C03，日志分支归 C05。L98“期限内未结束即停采”应随下轮同步写成“期限届满仍未结束”，以与 L97 的超时停止规则一致；本轮按前后文已有的期限门理解，不另开 ID 或要求实测。

### C05 — OPEN：B-hang 仍无法从 COLL-only 采集取得 INIT 证据

T03-05 L67–71 已接受全变量名、不同采集目的、`%h.%p` 到 rank 的启动映射，以及 MPI 环境传递条件。L68 也明确只设 COLL 采不到初始化 NIC 日志；但 L98 的 B-hang 仍指定 `NCCL_DEBUG_SUBSYS=COLL` 后“先查 Local Net device counts min/max”，没有指明同时保留并读取此前初始化日志，或从启动前用联合目的集采集。

env 页面区分 INIT 与 COLL；troubleshooting 明确 NIC count 检查发生在 communicator initialization，Replayer 的 COLL 输入不能替代这份启动证据。[环境变量的 NCCL_DEBUG_SUBSYS](https://rocm.docs.amd.com/projects/rccl/en/docs-10.1.0/api-reference/env-variables.html)、[troubleshooting 的 NIC counts / Replayer](https://rocm.docs.amd.com/projects/rccl/en/docs-10.1.0/how-to/troubleshooting-rccl.html)。

下一次关闭条件：B-hang 与采集目的表使用同一方案：从初始化前保留需要的联合子系统日志，或明确读取另存的启动日志再分析 COLL 时间线。缺启动证据时该检查无法判断，不能把没有相关日志当作 NIC count 一致。无需强行重放未知现场。

### C06 — OPEN：缓存阶段和数据顺序的预期仍需限定

T04-01 L81/L83/L85 已补概念关系、三个独立验证输入及条件，DCP `Any`、FileSystem `_StorageInfo`、CRC 配置条件和历史扫描范围已正确收窄；L178–183 已加入 ID/序列及未中断恢复基线，原有提纲缺项多数已补。[metadata.py L135–147](https://github.com/pytorch/pytorch/blob/1eba9b3aa3c43f86f4a2c807ac8e12c4a7767340/torch/distributed/checkpoint/metadata.py#L135-L147)、[filesystem.py L66–72](https://github.com/pytorch/pytorch/blob/1eba9b3aa3c43f86f4a2c807ac8e12c4a7767340/torch/distributed/checkpoint/filesystem.py#L66-L72)、[serialization.py L196–204](https://github.com/pytorch/pytorch/blob/1eba9b3aa3c43f86f4a2c807ac8e12c4a7767340/torch/serialization.py#L196-L204)。

剩余集中在对照的预期。L181 把输入或变换身份变化统一设为“失效后应见后端字节回升”，与 L81 已区分的读缓存/预处理结果缓存/组 batch 缓存不一致。一个用于判读的概念反例是：仅变换配置变化，派生结果缓存应失效，但未变的原始字节仍命中读缓存；此时需要重新计算结果，并不必增加持久化后端读取。这是本文缓存阶段边界的推导，不是本库事故或实测。后端字节变化应只在所选缓存层/控制条件要求重新读取时作预期，派生缓存另观测重算/新结果身份。

L85“消费序列与清单一致”还需说明此处训练语义的有限范围与预期序列的生成契约；manifest 的对象身份不能一概代替 sampler/shuffle/drop_last/补齐后的访问序列。L182 在固定对照条件下发现 ID/顺序不一致，若已违反已声明契约，应记该项校验失败、原因待查；未确定契约或证据不足才是无法判断。不要把已知的不一致仅以原因 unknown 消除其验证结果。

下一次关闭条件：按选定缓存阶段分列改变因素、失效证据与预期，删除统一的后端字节门。将清单身份、样本/访问顺序契约和变换结果重复性各自的覆盖范围说清，预期序列由固定 sampler/分片/补齐规则或未中断对照得出；保留允许的重复/丢尾，不引入通用 exactly-once 承诺。

### C07 — CLOSED：状态来源与回退条件已修正

T04-01 L146–147 已包括内建 RandomSampler iterator 的 generator/yielded 状态、用户 sampler/iterator 的 Stateful 分支，以及 iterable dataset/fetcher/iterator；不再把默认状态缩成仅 batch 数。单进程实现先尝试相应对象状态，再走非 Stateful fallback；worker 聚合不跨 rank、num_workers/in_order 限制、已产出不等于已消费的责任边界仍在。[stateful_dataloader.py L334–346](https://github.com/pytorch/data/blob/377e64c1be69a9be6649d14c9e3664070323e464/torchdata/stateful_dataloader/stateful_dataloader.py#L334-L346)、[L496–577](https://github.com/pytorch/data/blob/377e64c1be69a9be6649d14c9e3664070323e464/torchdata/stateful_dataloader/stateful_dataloader.py#L496-L577)、[sampler.py L60–75](https://github.com/pytorch/data/blob/377e64c1be69a9be6649d14c9e3664070323e464/torchdata/stateful_dataloader/sampler.py#L60-L75)、[0.11.0 API](https://docs.pytorch.org/data/0.11/torchdata.stateful_dataloader.html)。未验证目标 NPU 配套的边界不因 CLOSED 消失，正文链接剩余问题归 C09。

### C08 — OPEN：错误分支和等待方向仍与一次源不符

T04-01 L158–164 的路径限定和三路已接受其主要结构：管理指针登记 stream；非管理 D2H 且条件接口存在时不登记直接返回；其余非管理同步等待。条件接口不作为目标能力证明，0106 不报错与 SDC 分开，0020/0086 弱绑定与 pin_memory 未验证也已保留。

L164 的“失败抛错；checkpoint-resume 模式只告警”不适用于这行的 allocator recordEvent 分支：CachingHostAllocator L191–196 在同步错误时检查并 `AT_ERROR`，没有 resume 分支。告警逻辑在 CopyKernel L103–121 的 **non_blocking=False** 分支；不能搬到 non_blocking=True 调用的非管理指针等待路径。另不能用受该告警例外影响的成功返回替代完成证据。[CachingHostAllocator.cpp L181–205](https://github.com/Ascend/pytorch/blob/bc51ab84cc6f35c77aab1c59886e0ea43681a317/torch_npu/csrc/core/npu/CachingHostAllocator.cpp#L181-L205)、[CopyKernel.cpp L97–121](https://github.com/Ascend/pytorch/blob/bc51ab84cc6f35c77aab1c59886e0ea43681a317/torch_npu/csrc/aten/common/CopyKernel.cpp#L97-L121)。

L168 及研究记录 L22 把 0091 写成“event 等待 stream”，方向反了：`aclrtStreamWaitEvent(stream, event)` 是指定 stream 的后续任务等待 event 捕获的任务完成，主机调用异步返回；它不是主机等待完成，也不是 event 等待 stream。跨 stream 的有限关系应为源 stream 记录 event，目标 stream 等待该 event，再安排依赖工作。[CANN 0091 的功能与 stream 参数](https://www.hiascend.com/doc_center/source/zh/CANNCommunityEdition/82RC1alpha001/API/appdevgapi/aclcppdevg_03_0091.html)、[0083 RecordEvent](https://www.hiascend.com/doc_center/source/zh/CANNCommunityEdition/82RC1alpha001/API/appdevgapi/aclcppdevg_03_0083.html)。

“实际完成以查询/同步返回为准”也应保留返回状态区别：`aclrtQueryEventStatus` 返回 0 表示查询成功，任务完成由出参 COMPLETE/NOT_READY 判断，并应保证 record/query 覆盖的是对应任务且先后顺序明确；跨线程乱序有来源警告。[0086 查询状态与约束](https://www.hiascend.com/doc_center/source/zh/CANNCommunityEdition/82RC1alpha001/API/appdevgapi/aclcppdevg_03_0086.html)。

下一次关闭条件：删去 allocator 行上的 resume 例外，若解释 CopyKernel 的同步分支则单列其位置/先同步再拷贝/错误条件；将正文和映射中 0091 统一改为 stream 等待 event，区分设备依赖、主机等待、查询成功和任务完成，给出 event 的记录/覆盖前提。无需补 0088/0089 超时细节或实机结果。

### C09 — OPEN：定位表改善，正文近旁链接与部分映射未闭环

两份研究记录已改为映射表，固定 commit/核心行号、支持范围和 unknown 已加入；悬空 §4 与未登记 PR #6843 旁证已删除，verification 已分开作者/审阅者范围，这些关闭动作接受。

初审还要求技术主张附近的普通 Markdown 精确链接，目前 T03-05 L56/L63/L75–81、T04-01 L146/L158–168 仍主要写文件名/行号/页码，核心实现链接只在研究记录中。DCP 段 L83 的近旁链接已补，但不能代表上述其他段也已完成；C02/C07 的技术事实可关闭，C09 的阅读取证链仍 OPEN。

研究记录还有可具体修正的定位：RCCL L19 的 CHANGELOG 只给章节名没有文件 URL，PR 案例 L25 的 RegisterTests.cpp 同样只有文件名/行号；T04-01 L19 的 DataLoader 否定证据没有原文件 URL，Stateful 回调段缺 state_dict_loader 精确链接；L22 的 0091 方向错误须与 C08 同步。不要求每个重复提及都复制一组来源，但承担结论的正文/映射位置应可直接打开支持证据。[写作指南 §5](../authoring-guide.md#5-来源证据与许可)。

下一次关闭条件：补上述核心位置的近旁实现/精确页面链接，并同步余下映射；记录正确的一次源支撑范围，不将当前审阅者的新抓取冒充作者历史取证。已有来源组可复用，无需为相同文件另造登记 ID。

## 后续范围与检查

- CLOSED：C02、C04、C07；OPEN：C01、C03、C05、C06、C08、C09。下一轮仅复核六项剩余要求及受影响同步，已关闭技术事实不重复扩大检查。
- T03-05 仍受 C01/C03/C05/C09 阻断，T03-06 不能解锁；T04-01 仍受 C06/C08/C09 阻断。T03-07/T03-08 未在本轮审阅。
- T02-10/C08 的[例外清单](batch-17-t02-10-exception.md)保留；T02-11 草稿仍只作边界材料，不转为已验收引用。本轮不改变 Batch 17/18 的状态、正文或证据记录。
- 本轮只新增复核报告，并更新初审报告/来源审计的最新状态和入口；作者正文、研究记录、修订映射、索引、来源登记、任务/主题计划保持本轮输入。历史初审内容保留，不改写为当前结论。
- `make check` / `make build`：均 PASS（87 篇内容 / 386 项来源）。未改 `src/kb/`，不新增内容实现镜像测试，未执行 `make test`；结构检查不证明技术正确性或远端条件。
- 无真实 GPU/NPU/存储、MPI/RCCL 运行、设备配置变更或故障注入；正文保持 draft/source_checked，不产生硬件复现结论。
