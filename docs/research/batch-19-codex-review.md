# 第十九批第一轮技术审阅记录

**最新进展（2026-10-12）：第三次定向复核完成，累计 9 CLOSED / 0 OPEN；T03-05/T04-01 在原定有限内容/来源范围通过，T03-06 对 T03-05 的审阅等待门已解除。** 通过范围与保留条件见[第三次复核](batch-19-codex-third-recheck.md)，[第一次](batch-19-codex-recheck.md)及[第二次](batch-19-codex-rerecheck.md)复核保留历史。其余 Batch 19 任务未在本轮审阅。下列发现与输入保留为初审历史，不作为最新状态表。

审阅日期：2026-10-10（Asia/Shanghai）。**结论：本轮 T03-05 / T04-01 暂不通过；B19-C01–C09 共 9 项 P2，全部 OPEN。** 本记录为初审交付，未修订知识正文，也未进行作者修订后的定向复核。T03-06/T03-07/T03-08 不在本次审阅范围内；按用户要求，T03-06 写作继续等待 T03-05 修订及复核通过。不能把本轮两项的审阅结果表述为整个 Batch 19 已验收。

约定模型 / effort 为 `gpt-6.1-sol / xhigh`。执行者为本会话 Codex 主助手，与既有取证和正文编写角色分开；未派发子代理。本会话没有提供可独立核验的实际模型与 effort 运行标识，故将该配置记录为用户约定，不写成已独立确认的执行元数据，沿用 [Batch 18 的记录方式](batch-18-codex-review.md)。模型审阅、来源核对与硬件验证分别记录。

依据：[T03-05 / T04-01 验收清单](../../plans/full-coverage-backlog.yaml)、[路线图来源门槛](../full-coverage-roadmap.md#批次执行与来源入口)、[依赖规则](../batch-dependencies.md)、[写作指南第 7 节](../authoring-guide.md#7-批次审阅约定)、[主归属目录](../../content-outline.md)及 [AGENTS](../../AGENTS.md)。T02-10 按 [C08 例外清单](batch-17-t02-10-exception.md)条件满足，C08 仍 OPEN；T02-11 草稿只作边界材料，不在本轮升为已验收输入。审阅不重开 Batch 17/18 的已关闭发现，也不改变前置任务的实际验收范围。

## 输入身份与范围

读取 T03-05 全文、T04-01 全文及相对 HEAD 的增量、两章索引、两份研究记录、来源审计、相关登记和 metadata schema。T04-01 的独立取证重点为 §A/§B/§C 与 NPU 新增段；既有 PyTorch 数据加载/CUDA 边界重读，MLPerf Storage v2.0 原有取证范围沿用，不宣称本轮重新核验其全文。

作者正文、研究记录和登记中的 `2026-10-14` 保留为输入标签；本次实际审阅日期为 2026-10-10，不由这些标签推导取证发生日期。

| 输入 | 初审 SHA-256 |
|---|---|
| [T03-05 正文](../../knowledge/03-communication/rccl-runtime-and-verification.md) | `7135560ff0bbc53e4e7f970e2521679ec006502053fd04ec6e3ab4aff81ed906` |
| [T04-01 正文](../../knowledge/04-data-storage/training-data-path.md) | `cbd7a3cbeb642a24cb6d4f4752b5a119226d8264d99e2d2135296a0c25ab41cc` |
| [03 索引](../../knowledge/03-communication/index.md) | `4cb6376d6a2298dd2cf76b935b78273b13c13e84584408bf90ba744d6caacf2d` |
| [04 索引](../../knowledge/04-data-storage/index.md) | `4565d9900300a232870b2040230461f020ce7c88464b013da3c530861f0a4cb5` |
| [RCCL 研究记录](batch-19-rccl-sources.md) | `2e65fbb8eafe833aa058a652084edd31b1df2edd24aacb0f9809a3e7e603435d` |
| [T04-01 研究记录](batch-19-t04-01-sources.md) | `5d3cf45a4895c503d3bbca3c764499e6cde19cb4b4485680413058f185883787` |
| [来源审计](batch-19-source-audit.md) | `45d5f4a668ebe4243375d508fe606a7a744eeb0c2350f74b87625f6f499f863e` |
| [来源登记](../../sources/registry.yaml)（386 项） | `e84c3b6eb61a83a46dbbfd371e5de4112def120131e0c374181e8e5acbf8f51f` |
| [任务清单](../../plans/full-coverage-backlog.yaml) | `121826a4d499273e7f6a00735e0a53931eef5c097bd66ab6b2425fdbc36ddfe0` |

以下正文位置均按上述输入的实际文件行号；上游源码行号按原文件计数。

## 独立取证范围

- RCCL `docs-10.1.0`：首页、library-specification、api-library、fault-tolerance、env-variables、troubleshooting、usage-tips 和 license 的精确 URL，默认 TLS 校验获取正文并核对站标 2.30.7。网页工具部分请求出现 cache miss/429，随后 curl 获取对应精确页成功；不以失败的网页片段代替来源，也未进行 latest/别名逐页差分。
- ROCm `docs-10.1.0` 兼容矩阵与 release-notes：读取设备/OS/驱动条件和组件表；MI300X acceptance 为本轮观察的 latest 页面。仍不建立整栈已测组合。
- `rocm-systems`：只读解析 `therock-10.1` annotated tag 到完整 commit `7da43026e4f2ef7600433c38c820732f7a205d22`；读取 rccl-tests 的 README、timer.cc、common.cu、all_reduce.cu、PERFORMANCE.md、util.cu 和许可，以及 RCCL group.cc、CHANGELOG、RegisterTests.cpp 与 CI 配置。关键测试、group 和案例文件再从完整 commit 获取，字节与 tag 获取结果一致。
- PR #9745：公共 GitHub API 返回 403、网页工具未取得正文后，通过 GitHub connector 取得 PR body、diff、合并身份和公开讨论；merge commit 为 `5bc651a82683b2ae21acf14ffc9af35f5c2722ae`，合并时间 2026-08-09 05:11:52 UTC。未访问其私有 CI 链接。原文 Test Plan 的 pipeline 复验项未勾选；本轮只确认测试跳过和 CI 配置修订存在，不证明挂起的运行路径已修复或目标流水线复验成功。正文提及的 PR #6843 本轮未独立取得，不提升为已核验旁证。
- PyTorch v2.6.0：读取固定 commit `1eba9b3aa3c43f86f4a2c807ac8e12c4a7767340` 的 sampler.py、distributed.py、dataloader.py、DCP stateful.py/state_dict_loader.py/metadata.py/filesystem.py 与 serialization.py；重读 2.6 data、CUDA、randomness、testing 精确文档。dataloader.py 为 77162 B，`state_dict`/`set_epoch` 均零命中；这是所查文件的否定证据。本轮未重做 DCP 全部 28 文件扫描，不将历史扫描扩大为所有后端没有校验。
- TorchData 0.11.0：精确 API 与 tutorial 页面重定向至 `meta-pytorch.org/data/0.11/`，站标仍为 0.11.0；解析 tag `v0.11.0` 到 commit `377e64c1be69a9be6649d14c9e3664070323e464`，读取 stateful_dataloader.py、sampler.py、README 与 LICENSE。README 的 torch 2.6.0 / torchdata 0.11.0 文档对应关系有依据；这不等于本库运行验证，更不证明 NPU 后端行为。
- TorchNPU：重读 `bc51ab84cc6f35c77aab1c59886e0ea43681a317` 的 CopyKernel.cpp、CachingHostAllocator.cpp、streams.py。CANN 8.2.RC1.alpha001：普通文档 URL 部分只返回站点壳，改取相同版本/文件的官方 `doc_center/source/zh/` 正文，核对 0101/0102/0105/0106/1807、0075/0076/1395/0020、0079/0083/0086/0091 与数据传输指南。保留既有记录对 0020/0086 版本绑定较弱的限定；0088/0089 超时细节未重新取证。

证据均使用[既有来源登记](../../sources/registry.yaml)的文档组或仓库范围：`src.amd.rccl-docs-10.1.0`、`src.rocm.rocm-systems-therock-10.1`、`src.rocm.rocm-systems-pr-9745`、PyTorch/DCP/TorchData 及 TorchNPU/CANN 对应 ID；本轮不新增来源 ID。临时原文、完整 PR 讨论和下载日志没有镜像进仓库；下表只记录关键获取身份，完整获取范围与定位以上述列表和各项发现为准。

| 关键证据 | 字节数 | SHA-256 |
|---|---:|---|
| RCCL fault-tolerance HTML | 71378 | `7370170fb32d61b008b47e98a11957bec6d9b688307333294b3f78febb0220e9` |
| rccl-tests common.cu | 107420 | `1339f9535d68b748677bd817e88d02002a71ff27b7f2b7ce41fcaccaa505f9d7` |
| rccl-tests util.cu | 26709 | `a27340e1b6119d145a454689a782a53383fec3dddfc9f0c6acaf65bba3415429` |
| rccl-tests PERFORMANCE.md | 5692 | `26ff0d9a73464548970a9a6fd08536b557058c7b1114756f673c156ef55ef650` |
| TorchData 0.11.0 API HTML | 56430 | `a3a82c20f349fd60228e7f38284b2ccdece1a502dd3e12664ebdff48c1aa0031` |
| TorchNPU CopyKernel.cpp | 15497 | `ffd690fc786007e40e9db49c38226a6d93a0b5f5fe66bfbed3a681618b77e5b2` |
| TorchNPU CachingHostAllocator.cpp | 12355 | `ed44e2afcd1d7084c3904e6fb95c21995b6577756f48abd3b955cd69cb21e2a9` |
| CANN 0106 官方静态正文 | 20762 | `dfcdaf0d9e0b3e4b45afee0005f604c9ccf89aafdf39acfaf4ac4a18015aa8bb` |

## 发现与关闭条件

### B19-C01 — P2：返回等于入队未区分 group/non-blocking，Abort 缺必要前提

位置：`rccl-runtime-and-verification.md:53、56–58`。

正文把 collective 返回和 `ncclGroupEnd` 统一解释为已入队，同时引入 non-blocking poll 和坏态 Abort，却没有区分 group 内调用尚未提交、non-blocking 返回 `ncclInProgress` 与成功入队。固定 group.cc 的非阻塞分支启动后台 group job 后立即返回 `ncclInProgress`；这时不能仅凭主机返回就把依赖操作或 event 当作已排在通信之后。初始化示例只列 InitRank/InitAll，没有给出 fault-tolerance 所要求的 `config.blocking=0` 创建条件；该页还要求 Abort 时没有线程位于 RCCL 调用中。省掉这两项，会把有前提的恢复方式写成所有 communicator 可直接采用的规则。

证据：[group.cc L919–958](https://github.com/ROCm/rocm-systems/blob/7da43026e4f2ef7600433c38c820732f7a205d22/projects/rccl/src/group.cc#L919-L958)、[library-specification 的 Group Semantics](https://rocm.docs.amd.com/projects/rccl/en/docs-10.1.0/api-reference/library-specification.html)、[fault-tolerance 的 Note / Asynchronous errors / Recovering from a failure](https://rocm.docs.amd.com/projects/rccl/en/docs-10.1.0/how-to/fault-tolerance.html)。

关闭条件：分列普通成功返回、group 内暂存、最外层 GroupEnd、non-blocking InProgress 和设备完成；写出 poll 到 `ncclSuccess` 后再建立依赖的条件与错误分支。补非阻塞 communicator 创建接口/config 和 Abort 的线程前提、调用方 deadline；保留对称路径无法靠 async error 报缺席的边界。无需运行故障注入。

### B19-C02 — P2：time 列写成毫秒，与固定实现相差 1000 倍

位置：`rccl-runtime-and-verification.md:73`。

正文直接采用 PERFORMANCE.md 的 ms 表述，但实际 common.cu 将秒乘 `1e6`，util.cu 表头明确 `(us)`。若按 ms 解释输出，延迟及由 time 复算的带宽会相差 1000 倍。这是文档与实现的冲突，应记录采信的实现，不能将源文笔误复制为测试口径。host steady_clock 主计时只覆盖本文默认路径；`-C`、`-I`、graph/device timing 是另外的口径，不能概括为所有模式均相同。

证据：[common.cu L1070–1087、L1259–1266](https://github.com/ROCm/rocm-systems/blob/7da43026e4f2ef7600433c38c820732f7a205d22/projects/rccl-tests/src/common.cu#L1259-L1266)、[util.cu L780–787](https://github.com/ROCm/rocm-systems/blob/7da43026e4f2ef7600433c38c820732f7a205d22/projects/rccl-tests/src/util.cu#L780-L787)、[PERFORMANCE.md](https://github.com/ROCm/rocm-systems/blob/7da43026e4f2ef7600433c38c820732f7a205d22/projects/rccl-tests/doc/PERFORMANCE.md)。

关闭条件：改为实际输出微秒，说明秒/微秒/GB/s 换算、默认每操作归一化及 MPI `-a` 聚合口径；将 PERFORMANCE.md 的 ms 记为来源冲突。只承诺所选默认模式，其他模式明确分开或排除，同步研究定位与测试设计。

### B19-C03 — P2：两次命令未形成校验分离，正确性判据缺覆盖配置

位置：`rccl-runtime-and-verification.md:73、88–89`。

第一条命令未设 `-c`，实际默认已经是 `-c 1`；再“另跑一遍 -c 1”并没有改变校验配置。源码的校验循环在计时后重初始化并另跑 collective，支持计时和校验阶段分离，不支持两条命令自动构成纯性能/正确性两种配置，也不证明每个计时迭代的输出都已校验。本文应区分这两个边界。

另外，`NCCL_TESTS_MIN_BW` 可从环境继承：页脚和退出码按扫描得到的平均 busbw 与 `0.9×设置值` 比较。正文只说“设阈值时出现 OK”，没有固定该环境项；这会使同一命令的非零退出含义随环境改变。`-c 0` 时输出 `#wrong=N/A`，不能当成零错误。

证据：[README L163–187](https://github.com/ROCm/rocm-systems/blob/7da43026e4f2ef7600433c38c820732f7a205d22/projects/rccl-tests/README.md#L163-L187)、[common.cu L138、L1192–1256](https://github.com/ROCm/rocm-systems/blob/7da43026e4f2ef7600433c38c820732f7a205d22/projects/rccl-tests/src/common.cu#L1192-L1256)、[common.cu L2757–2788](https://github.com/ROCm/rocm-systems/blob/7da43026e4f2ef7600433c38c820732f7a205d22/projects/rccl-tests/src/common.cu#L2757-L2788)、[util.cu L500–514、L799–806](https://github.com/ROCm/rocm-systems/blob/7da43026e4f2ef7600433c38c820732f7a205d22/projects/rccl-tests/src/util.cu#L799-L806)。

关闭条件：选择并明确一种设计——同次运行的计时/重跑校验分阶段，或显式不同 `-c` 的两种运行；后者的纯性能运行不独立提供正确性通过证据。固定 datatype/op、warmup/iters/check 次数、in-place/out-of-place、消息扫描覆盖和 `NCCL_TESTS_MIN_BW` 条件。要求完成全部计划行且实际校验开启，区分校验失败、带宽门限失败、程序错误和无法判断；不把重跑校验扩大为所有计时迭代的证明。

### B19-C04 — P2：单节点 304 GB/s 被带入跨节点参考，设计缺路径与挂起判据

位置：`rccl-runtime-and-verification.md:49、85–90`。

≥304 GB/s 出自单进程八 GPU、扫描至 8G 的 MI300X acceptance；本文计划是两节点十六进程、每进程一 GPU、扫描至 1G。路径从节点内互联变成包含节点间网络，消息范围和进程模型也不同，即使 OS 相同，也没有依据期待“同量级”。将低于此值记为无法判断虽然没有误判失败，但仍把不适用的数值当作性能参考。busbw 的归一化目标不使不同物理瓶颈等价。

`ibv_devinfo` / `rdma link` 正常不证明这次 RCCL 走了 RDMA，更不证明两个目标节点各八个 rank 的实际放置。命令也未给 MPI 实现/节点分配前提。F1 写 hang，却没有预声明等待期限及退出/保留证据条件；固定工具 `-T` 默认关闭，程序退出成功又只能证明所运行配置，不能单独验收预期网络路径。

证据：[MI300X acceptance 的 RCCL Allreduce](https://instinct.docs.amd.com/projects/system-acceptance/en/latest/gpus/mi300x.html)、[README 的多节点/1 process per GPU 与 timeout 参数](https://github.com/ROCm/rocm-systems/blob/7da43026e4f2ef7600433c38c820732f7a205d22/projects/rccl-tests/README.md)、[RCCL troubleshooting 的 Collecting system/RCCL information](https://rocm.docs.amd.com/projects/rccl/en/docs-10.1.0/how-to/troubleshooting-rccl.html)。这是有限实验设计的缺项，不要求本轮取得实机结果。

关闭条件：将 304 仅保留在原单节点条件下，不作为两节点同量级目标；跨节点性能与同配置基线比较，无基线则未判定。补 MPI/两节点分配前提、hostname/local rank/device 与实际 NET transport/HCA/端口的记录要求，路径无法确认时不能宣称 RDMA 分支通过。预声明有限等待/停止判据，并区分测试失败、原因未知和证据不足；工具 timeout 的覆盖范围不足时仍需总体等待约束。

### B19-C05 — P2：SUBSYS 不是 RCCL 的日志环境变量

位置：`rccl-runtime-and-verification.md:69、90`。

正文两处写 `NCCL_DEBUG=INFO SUBSYS=...`，RCCL 所读取的名称是 `NCCL_DEBUG_SUBSYS`。按当前字符串设置，COLL/TUNING 不会因此被启用；默认子系统仍为 INIT/BOOTSTRAP/ENV。B-hang 的采集与合并因此可能缺少 collective 记录，不能支持文中所说的时间线和 Replayer 输入。只设 COLL 又不足以同时保证采到初始化期 NIC count 日志，需要把采集目的与子系统对应。

证据：[env-variables 的 NCCL_DEBUG_SUBSYS](https://rocm.docs.amd.com/projects/rccl/en/docs-10.1.0/api-reference/env-variables.html)、[troubleshooting 的 Replayer 和 NIC counts 两节](https://rocm.docs.amd.com/projects/rccl/en/docs-10.1.0/how-to/troubleshooting-rccl.html)。

关闭条件：改用完整变量名，按初始化/调优/collective 的目的给出采集集合，说明何时开始采集及 `%h.%p` 文件与 rank 的关联；MPI 远端环境传递按所选 launcher 条件记录，不假设 shell 变量必然传播至所有节点。同步所有说明和研究记录。

### B19-C06 — P2：数据身份关系与四类对照仍为提纲，DCP 证据被泛化

位置：`training-data-path.md:81–83、161–166`；T04-01 acceptance 第一、第四项。

§A 只枚举五组字段并说关系由应用定义，没有定义 manifest 如何绑定样本 ID/物理对象/哈希，预处理结果如何关联原始输入和代码/配置/随机状态，缓存键如何区分缓存阶段及使失效可检查。可以没有统一框架契约，但仍须给出本文采用的概念关系或明确标为应用样板。三个独立验证目标也仅被命名，没有各自输入和通过条件。

其中 `storage_data` 仅含三个字段并非 DCP 通用协议：`Metadata.storage_data` 类型为 Any，三个字段来自 FileSystem 的 `_StorageInfo`。stateful.py 只声明两方法协议，不能证明 metadata 内容、28 文件扫描或 CRC 行为。CRC 注释明确谈 `set_crc32_options(False)` 产生的归档可加载，不能概括为任意文件字节损坏仍可加载。

§C 列出四种对照名、固定因素与 unknown，尚未说明每种对照实际改变什么、收集什么和如何比较。总样本数相同不能排除同数量的缺样/重样或次序错误；缓存“失效”未指定改变输入/变换身份后的可观测预期；恢复首批和持续窗口未定义未中断对照、已消费与已预取的边界及重放量。把这些全部转交另一个主文不完成本任务的数据路径对照设计。

证据：[T04-01 验收清单](../../plans/full-coverage-backlog.yaml)、[metadata.py L135–147](https://github.com/pytorch/pytorch/blob/1eba9b3aa3c43f86f4a2c807ac8e12c4a7767340/torch/distributed/checkpoint/metadata.py#L135-L147)、[filesystem.py L66–72](https://github.com/pytorch/pytorch/blob/1eba9b3aa3c43f86f4a2c807ac8e12c4a7767340/torch/distributed/checkpoint/filesystem.py#L66-L72)、[serialization.py L196–204](https://github.com/pytorch/pytorch/blob/1eba9b3aa3c43f86f4a2c807ac8e12c4a7767340/torch/serialization.py#L196-L204)、[PyTorch 2.6 randomness 的多 RNG/worker 种子控制](https://docs.pytorch.org/docs/2.6/notes/randomness.html)。

关闭条件：补一份原创、有限的数据身份/派生缓存关系与三类验证表；明确逻辑 ID、哈希对象/算法、变换与缓存阶段，未知的实际格式仍可保留 unknown。DCP/CRC 主张分别收窄到取得证据的实现和条件，历史扫描注明沿用而非本轮重新完成。四类对照逐项写输入/控制变量、观察记录、预期与无法判断；缺样/重样/乱序采用 ID 及顺序对照，恢复采用已消费位置和未中断基线，不承诺通用 exactly-once，也不要求实际执行。

### B19-C07 — P2：StatefulDataLoader 默认状态被缩成仅 batch 数，漏掉内建 sampler iterator

位置：`training-data-path.md:142`。

版本文档说状态包含已产 batch 数，没有说默认只存该数。固定实现未传入自定义 sampler 且 `shuffle=True` 时使用 TorchData 自带 RandomSampler，并用自己的 BatchSampler 包装；RandomSampler 的 iterator 已实现 Stateful，保存 generator state 和 yielded 数。DataLoader 会尝试序列化 index sampler、sampler iterator、dataset/fetcher 等对象，恢复时先检查 sampler 或 iterator 的 Stateful 能力，只有相应非 stateful 分支才退回 fast-forward。无需用户额外给 sampler 对象实现 state_dict，就存在自动取得 iterator 状态的内建路径。

“只存 batch 数；sampler/dataset 自带 state_dict 才调状态”因此既遗漏内建行为，也遗漏 iterator 的责任。它会误导使用者判断实际 checkpoint 包含哪些随机/进度状态。已产出的 batch 仍不自动等于训练完成消费的 batch，不跨 rank 的边界需要保留。

证据：[stateful_dataloader.py L334–346、L496–577](https://github.com/pytorch/data/blob/377e64c1be69a9be6649d14c9e3664070323e464/torchdata/stateful_dataloader/stateful_dataloader.py#L496-L577)、[sampler.py L18–31、L60–75、L108–109、L140–156](https://github.com/pytorch/data/blob/377e64c1be69a9be6649d14c9e3664070323e464/torchdata/stateful_dataloader/sampler.py#L60-L75)、[0.11.0 API](https://docs.pytorch.org/data/0.11/torchdata.stateful_dataloader.html)。

关闭条件：按 map-style 默认 shuffle、用户 sampler/iterator、iterable dataset/iterator、单/多 worker 分列状态来源和 fallback；区分文档概述与已核对的实现。保留 worker 聚合不跨 rank、num_workers/in_order 限制、训练已消费位置仍由应用对齐的边界；不把该源码核对升级为与目标 NPU 环境的运行保证。

### B19-C08 — P2：NPU 三路分支未真正分列，allocator 管理和错误语义被扩大

位置：`training-data-path.md:153、173`；T04-01 acceptance 第三项。

CopyKernel L88–115 只体现异步任务下发与 allocator 调用；真正的三路判定在 CachingHostAllocator L181–205：管理内存只登记 stream；非管理 D2H 且条件接口存在时直接返回，不登记该 buffer 的 event；其余非管理路径同步等待。正文将 `non_blocking=True` 统一说为异步下发加 event 登记，又将三路定位全指向 CopyKernel，漏掉 D2H 例外，读者无法判断主机阻塞与 buffer 生命周期。

allocator 对已释放块的复用管理也不能泛化为应用可随意修改仍存活的 host buffer。CANN 0106 说非 MallocHost 指针调用时不报错、执行相关业务可能出现不可预知错误；“静默错误”若指输出损坏/SDC，强于现有证据。stream/event 部分只有页码串和“三类同步分工”，尚未实际列出下发返回、查询状态、stream/event/device 等待、跨 stream 依赖与观察点；0020/0086 的较弱版本绑定也在正文消失了。

证据：[CopyKernel.cpp L85–122](https://github.com/Ascend/pytorch/blob/bc51ab84cc6f35c77aab1c59886e0ea43681a317/torch_npu/csrc/aten/common/CopyKernel.cpp#L85-L122)、[CachingHostAllocator.cpp L181–205、L214–235](https://github.com/Ascend/pytorch/blob/bc51ab84cc6f35c77aab1c59886e0ea43681a317/torch_npu/csrc/core/npu/CachingHostAllocator.cpp#L181-L205)、[CANN 0106 官方静态正文的功能/型号约束](https://www.hiascend.com/doc_center/source/zh/CANNCommunityEdition/82RC1alpha001/API/appdevgapi/aclcppdevg_03_0106.html)、[0076 stream 等待](https://www.hiascend.com/doc_center/source/zh/CANNCommunityEdition/82RC1alpha001/API/appdevgapi/aclcppdevg_03_0076.html)、[0086 event 查询](https://www.hiascend.com/doc_center/source/zh/CANNCommunityEdition/82RC1alpha001/API/appdevgapi/aclcppdevg_03_0086.html)、[0091 stream 等待 event](https://www.hiascend.com/doc_center/source/zh/CANNCommunityEdition/82RC1alpha001/API/appdevgapi/aclcppdevg_03_0091.html)。

关闭条件：在正文给出三路表，并限定所查 contiguous/同 dtype/base format 拷贝路径，列主机是否等待、allocator 是否登记和应用对 buffer 使用的完成前提；条件接口存在不等于已确认目标运行能力。把“不报错但业务行为不可预知”与 SDC 证据分开。给出选定 stream/queue、查询/同步/依赖和实际完成的观察表，保留弱版本绑定及 pin_memory/NPU 实验未知，不拼成已测 TorchNPU/CANN 组合。

### B19-C09 — P2：主张—来源定位表与取证报告引用不可复核

位置：`batch-19-rccl-sources.md:9–15`、`batch-19-t04-01-sources.md:9–15`；`rccl-runtime-and-verification.md:62、73、80–81、95`；`training-data-path.md:81、139–145、153、173`。

两份“主张—来源定位表”实际是短句串，未列精确 URL/commit/小节/行号和支持范围；末尾均写“详见取证报告 §4”，却没有报告路径，当前交付也没有相应 §4 可供打开。正文的测试计时、CHANGELOG 差异及 NPU 传输只给文件名、页码串或仓库树入口；DCP stateful.py 被放在不能支持的 metadata/CRC 主张之后；TorchData 只链首页。登记 source_refs 与 HTTP 200 检查不能填补这些定位缺口。PR #6843 如保留实测旁证，还需要独立登记和准确来源，不能借 PR #9745 的 source ID 取得支持。

证据：[写作指南 §5](../authoring-guide.md#5-来源证据与许可)要求逐条精确页面与近旁引用；[路线图来源入口](../full-coverage-roadmap.md#批次执行与来源入口)要求主张—来源定位表。上面 C01–C08 的上游具体定位表明同一树/协议文件不能代替实际支撑文件。

关闭条件：两份研究记录改为可逐项复核的映射，含主张、精确页面或固定源码、定位、支持/不支持范围及 unknown 条件；补实际取证报告链接或删除不存在的 §4 引用。技术主张附近补普通 Markdown 链接，源码行号按固定原文件核对；PR #6843 补登记取证或移除未核验旁证。收窄 verification notes 的“本轮核对”范围，保留历史作者记录，不将本审阅者的新取证冒充作者当时已完成。

## 已核对且无需另开问题的边界

- 样板交集与已测组合已明确分开；RCCL 2.30.7/ROCm 10.1.0 文档与 tag 的 CHANGELOG 版本标注冲突可以继续保留未知，未要求证明一个完整可部署栈。
- API deprecated 名称、rank/device/root 区别、P2P 匹配/group 并发条件、对称路径缺席无法靠 async error 报告、日志默认值及 NIC count mismatch 开关，在所选文档范围内有依据。C01 是遗漏前提，C05 是变量名错误，不否定这些已支持的局部机制。
- PR #9745 的 gfx908 挂起、gfx950 分项/bisect 反例、架构 allowlist skip 与 CI timeout 修改有来源；最早入版、底层挂起调用栈和 CI 修订后实际结果仍未证，不要求本库补做实测。
- PyTorch DataLoader 没有标准 state_dict/set_epoch 的所查文件否定证据、DistributedSampler 的 seed+epoch/补齐及 iterable 分片责任有依据。RandomSampler 无显式 generator 时从全局 PyTorch RNG 抽取种子；若全局 RNG 及消费历史固定，不能据无 generator 推导必然不可复现。现句仅说种子不固定时不可复现，本轮不把它误读为无 generator 必然失败。
- C08 精度前提按例外清单保留 unknown，T02-11 没有被表述为已验收输入；无需为本任务关闭 Batch 17 的 C08。
- 稳定 ID、主要归属、draft/generic 边界和章入口存在；`source_checked` 不代表 AMD/GPU/NPU 实机验证。

## 任务判定与修订顺序

| 任务 | 已有有限交付 | 待关闭范围 | 本轮判定 |
|---|---|---|---|
| T03-05 | 独立版本文档、初始化/原语概述、上游测试跳过案例、两节点方案框架 | C01–C05、C09：提交/恢复前提、计时/校验/路径判据、日志变量及来源定位 | 暂不通过 |
| T04-01 | 既有数据路径保留、sampler/loader 边界、TorchData 样板、精度例外联动 | C06–C09：身份/验证/对照设计、默认状态来源、NPU 分支与精确证据 | 暂不通过 |
| T03-06 / T03-07 / T03-08 | 本轮未交付审阅 | 依次按原前置及实际交付审阅 | 未审阅 |

建议先修 C01–C05 的事实和运行判据，以及 C07/C08 的状态/传输边界，再补 C06 的身份和有限对照设计，最后按 C09 将正文、研究记录、登记和 verification 定位对齐。无需为了通过本轮而执行 benchmark、变更设备配置、故障注入或验证现场集群。作者修订记录应逐项映射 B19-C01–C09；同一审阅者随后按文件身份定向复核并记录 CLOSED/OPEN，修订交付或 make 通过本身不关闭发现。

## 检查与限制

- `make check` / `make build`：PASS，87 篇内容 / 386 项来源；仅证明结构和本地文件链接，不能证明技术正确性、远端主张或实验通过。
- 本轮只新增本审阅报告并更新来源审计的当前状态/报告入口；作者正文、两份研究记录、两章索引、来源登记、任务清单及既有 Batch 17/18 记录保持输入，不代替作者修订，不更新主题覆盖或任务完成状态。
- 未改动 `src/kb/`，未新增内容实现镜像测试；按仓库规则无需 `make test`。
- 未运行上游代码、MPI/RCCL、真实存储、GPU/NPU、系统配置或故障注入；未建立环境档案，也未产生硬件复现结果。
