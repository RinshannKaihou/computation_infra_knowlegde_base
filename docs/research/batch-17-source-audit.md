# 第十七批来源与交付记录

**最新复核状态（2026-10-09）：第六次定向复核完成，累计 12 项 CLOSED、1 项 OPEN（B17-C08，P2），暂不通过。** 第五次要求的简写表来源范围、Matmul 支持条件及 verification 同步均已满足，无新增修改项；当前阻止关闭的证据范围为累加精度与固定实现关联，详见[第六次定向复核记录](batch-17-codex-sixth-recheck.md)。独立 `make check` / `make build` 均通过（83 content entries / 340 sources），本轮不增加登记。知识条目保持 `draft`，backlog 与主题覆盖状态未调整，未做实机验证。已通过项不重开；研究记录前段保留各阶段历史。

**第四轮修订状态（2026-10-09）：C08 两处限定已修订并通过第四次定向复核**（候选门控分支坐标与返回值契约、入口体未调用声明、核验范围限重载分支；autocast 第五种策略 fp32_append_dtype；见[修订记录](batch-17-review-fixes.md)），计算/累加精度仍 unknown 并保持 open。独立 `make check` / `make build` 通过（83 / 336），不因表述修订通过关闭整个 C08。

**第五轮修订与第五次复核状态（历史，2026-10-09）：C08 新增四项来源，336→340 sources，第五次定向复核已执行。** 互推导与 Add 支持样板核实，Matmul 计算逻辑契约取得；当时数据类型页范围与 Matmul 支持条件仍需修订。详见[第五次报告](batch-17-codex-fifth-recheck.md)，该三项现经第六次复核通过；保留当轮输入及 83 / 340 的独立结构检查结果。

**第六轮修订与复核状态（2026-10-09）：第五次三项要求已修订并通过第六次定向复核**（19 行简写表更正、Matmul 条件补全与 SDK/实现分别记录、verification 两算子范围同步；见[修订记录](batch-17-review-fixes.md)）。累加精度与实现关联继续 unknown / OPEN，不因三项表述修订通过关闭整个 C08。

**第四次复核状态（历史，2026-10-09）：当时 12 项 CLOSED、1 项 OPEN（C08，P2）。** 候选门控/入口关系及 autocast 第五策略限定均通过，无新增修改项；当时仅剩强制精度证据，详见[第四次定向复核](batch-17-codex-fourth-recheck.md)。当轮独立检查为 83 content entries / 336 sources。

**第三次复核状态（历史，2026-10-09）：当时 12 项 CLOSED、1 项 OPEN（B17-C08，P2），暂不通过。** C11 峰值 reset 解释修复并关闭，C08 强制精度证据及新增样板范围限定仍待补齐，详见[第三次定向复核记录](batch-17-codex-third-recheck.md)。当轮独立 `make check` / `make build` 通过（83 content entries / 336 sources）。

**第二次复核状态（历史，2026-10-09）：当时 11 项 CLOSED、2 项 OPEN（B17-C08/C11，均为 P2），暂不通过。** 本轮 C01/C03/C10 关闭；C08 的转换/元数据补证已核实，计算/累加精度及门控范围仍未验收；C11 的有序窗口已修复，峰值 reset 的归零表述仍需纠正。详见[第二次定向复核记录](batch-17-codex-rerecheck.md)。当轮新增 `CachingDeviceAllocator.h` 文件级反证登记，334→335 sources；补登前后独立 `make check` / `make build` 均通过，补登后为 83 content entries / 335 sources。

**第一次复核状态（历史，2026-10-09）：当时 8 项 CLOSED、5 项 OPEN（B17-C01/C03/C08/C10/C11，均为 P2），暂不通过。** 详见[第一次定向复核记录](batch-17-codex-recheck.md)，保留当轮输入、残留条件与 83 content entries / 332 sources 的结构结果；结构检查不关闭技术发现。

**初审状态（历史，2026-10-09）：初审报告交付时暂不通过；B17-C01–C13 共 13 项发现（11 P2、2 P3），当时全部 OPEN，尚未修订及定向复核。** 详见[技术审阅记录](batch-17-codex-review.md)，含固定输入身份、精确上游证据、逐项关闭条件与路线图验收判定。用户约定配置为 `gpt-6.1-sol / xhigh`；执行者为 Codex 主助手，实际模型/effort 未有可独立核验的运行标识，按报告披露，不把约定当成已确认执行元数据。知识正文与四份原取证记录初审当轮未改写，原有错误表述由发现跟踪，不据此继续宣称相关主张已通过技术审核。

初审补登五项文件级证据（326→331 sources）；初审前独立 `make check` 通过（83 content entries / 326 sources）。补登后 `make check` 与 `make build` 均通过（83 content entries / 331 sources），生成 `build/catalog.json` 与 `build/catalog.md`。这些检查仅验证结构与本地引用，不证明技术正确性、远程内容有效性或发现关闭。本批仍不更新 backlog 为 done、不关闭主题缺口，真实环境验证仍未执行。

**修订状态（2026-10-09）：第一轮 B17-C01–C13 修订后第一次定向复核 8 项关闭、5 项 P2 开放（C01/C03/C08/C10/C11）；第二轮修订已完成**（摘要与记录表口径、登记 active backend、转换样板与元数据同步、测试表对照要素、有序统计窗口；新增登记 2 项至 334 sources；见[修订记录](batch-17-review-fixes.md)）。第二次定向复核后 11 项关闭、C08/C11 开放；第三轮修订新增 autocast 注册来源至 336 sources，第三次定向复核后 C11 关闭、C08 继续 OPEN。知识条目保持 `draft`，不由提交修订自动关闭发现。

**草稿交付时状态（历史，2026-10-09）：待审阅——正文草稿与来源登记已交付，`make check`/`make build` 通过（83 content entries / 326 sources），当时尚未执行约定审阅。** 本批为 full-coverage 路线图 Batch 17（full-coverage-backlog 的 T02-08/T02-09/T02-10/T02-11），前置 T02-02（Batch 15）、T02-04/T02-05/T02-06（Batch 16）已有其已审阅范围内的发现闭环；前置报告中未覆盖的矩阵及接口证据仍保留，不能写成全部独立验收。全部保持 draft；三篇新正文与一处修订均为限定来源范围的文档级取证，无 reproduced。

## 本批正文

| 任务 | 正文 | 类型 | 备注 |
|---|---|---|---|
| T02-08 | [框架到设备后端的适配与能力核对](../../knowledge/02-software-stack/framework-backend-adaptation.md) | reference | 新增（PrivateUse1 责任清单 + 三路径核对 + MindSpore/vLLM 对照） |
| T02-09 | [GPU 分配器、保留内存与 OOM 证据](../../knowledge/02-software-stack/gpu-memory-oom-evidence.md) | concept | 新增（allocated/reserved、碎片键、记录表与三对照；AMD 独立证据） |
| T02-10 | [dtype、layout、格式转换与有限精度语义](../../knowledge/02-software-stack/dtype-layout-and-precision-semantics.md) | concept | 新增（五层语义、三平台开关条件句、最小检查四步；收敛/量化归 06.5/07.4） |
| T02-11 | [昇腾 NPU 内存与 OOM 证据](../../knowledge/02-software-stack/ascend-memory-oom-evidence.md) | concept | 修订（加法：主机传输/stream-event/non_blocking 三节 + 待执行验证；既有行号引用未动） |

来源记录：[框架后端](batch-17-framework-backend-sources.md)、[GPU 内存](batch-17-gpu-memory-sources.md)、[精度语义](batch-17-dtype-precision-sources.md)、[Ascend 传输同步](batch-17-ascend-transfer-sources.md)。任务清单：[plans/full-coverage-backlog.yaml](../../plans/full-coverage-backlog.yaml)。

## 来源变化

新增 46 项登记（280→326）：T02-08 计 11 项（PrivateUse1 相关 5 页 + TorchNPU 文件快照 4 项 + MindSpore r2.5.0 + vLLM interface.py；PrivateUse1 教程页去重复用既有登记），T02-09 计 12 项（torch.cuda 内存 API/stats/usage 3 页 + memory.py/CUDACachingAllocator 双源码 + CUDAGraph + CUDA 12.8 MEMORY/POOLS/GRAPH 3 页 + HIP 内存/流序 2 页 + ROCm/pytorch fork），T02-10 计 13 项（tensor-attributes/amp/amp-examples/set_float32_matmul_precision/testing/channels-last 6 页 + cuBLAS/FP8/cuDNN 3 页 + CANN AOL 入口 + ROCm/rocBLAS/MIOpen 精度 3 页），T02-11 计 10 项（CANN host/memcpy/stream/event/传输指南 7 页组 + TorchNPU CopyKernel/CachingHostAllocator/streams 3 快照）。

复用既有登记（不计数）：dispatcher-v2.6.0、torch-npu-v7.2.0-pytorch2.6.0、vllm.plugin-system-v0-14、privateuseone-tutorial-2026-10-09、cuda-semantics-2.6、profiler-2.6、numerical-verification-2.6、msprobe-training-guide-2026-09-30、cann-82rc1alpha001-acl-memcpy-2026-10-08、test-codecache-v2.6.0。

## 集成者核对

- 候选文档 URL 29 个全部 HTTP 200（curl 复核）；源码 raw 10 个全部 200；CANN 5 页 200（JS 壳，内容经静态地址取证）；GitHub blob 页偶发 503，引用一律用 raw 固定 commit。
- 集成者实开全文复核 4 项：HIP semantics（TF32 不支持等差异逐项确认）、MindSpore pluggable device（双模式与职责划分确认）、CUDA 12.8 Stream Ordered Allocator（流序语义与 pool 属性确认）、HIP 7.14.0 流序分配器页存在性；其余条目内容按取证轮实开记录采信，登记 notes 如实区分两种核对深度。
- 结构检查：`make check` / `make build` PASS（83 content entries / 326 sources）。结构检查只证明结构与本地引用，不代表技术正确性或远程内容有效性。

## 草稿交付时待审阅与已知边界（历史）

- 作者当时尝试约定审阅（gpt-6.1-sol / xhigh）未执行成功：2026-10-09 调用 `opencode/gpt-6.1-sol#xhigh` 独立审阅子代理失败（Upstream request failed: Insufficient account funds），当时记录为 blocked。该失败保留为历史；本次 Codex 初审的角色、模型标识边界和结果见文件顶部与新报告，修订及定向复核仍待完成。本批不更新 backlog 任务状态、不关闭任何主题缺口、不声明通过。
- 撰写者自查（非独立审阅，不替代约定审阅）：2026-10-09 对 TorchNPU 快照行号做 raw 实测复核——CopyKernel.cpp `copy_between_host_and_device` 定义 L88、分支区 L88–115 与正文描述一致（已据此收紧行号引用）；CachingHostAllocator.cpp 398 行、malloc/processEvents/aclrtMallocHost/recordEvent 行段与登记一致；streams.py `__all__` 与 SyncLaunchStream taskqueue 表述一致；autocast_utils 5 函数与 bf16 分支一致。
- T02-11 的 evidence_blocker 部分解除（已定位子项），整项关闭待执行轮行号复核 + 0088/0089 正文细读；acceptance 3 待执行验证保持 open。
- CANN 逐算子精度表（T02-10）、ROCm 默认 backend 与 fork diff（T02-09）、TorchNPU test/npu 用例名（T02-08）保持 unknown/blocked，正文均如实保留。
