# 第十九批第二次定向复核

**最新进展：第三次复核完成，C03/C09 CLOSED，累计 9 CLOSED / 0 OPEN；T03-05/T04-01 在原定有限范围通过。** 当前判定与 T03-06 等待门见[第三次复核](batch-19-codex-third-recheck.md)。下列 7 CLOSED / 2 OPEN 和对应发现为第二次复核历史。

复核日期：2026-10-12（Asia/Shanghai）。作者文件中的 `2026-10-14` 保留为输入标签，不作为本轮实际执行日期。

**结论：C01、C05、C06、C08 转 CLOSED；此前 C02、C04、C07 保持 CLOSED，累计 7 CLOSED / 2 OPEN。C03、C09 仅在 T03-05 范围仍 OPEN；T04-01 在本轮原定内容与来源审阅范围内通过，T03-05 暂不通过，T03-06 继续等待。** 本轮没有新增发现 ID，两个剩余项均为修订影响下的原关闭要求。T03-06/T03-07/T03-08 未在本轮审阅，不声明整个 Batch 19 通过。

约定模型 / effort 为 `gpt-6.1-sol / xhigh`，本会话 Codex 主助手执行，与作者修订角色分开；未派发子代理。实际模型与 effort 运行标识无可独立核验元数据，沿用[初审说明](batch-19-codex-review.md)。依据[第一次复核的剩余条件](batch-19-codex-recheck.md)、[写作指南](../authoring-guide.md#7-批次审阅约定)、[任务验收表](../../plans/full-coverage-backlog.yaml)、[主归属目录](../../content-outline.md)和 [AGENTS](../../AGENTS.md)，不扩大为实机验证或前置任务验收。

## 输入身份

读取两篇正文、两份来源映射、第二轮修订记录及现行报告/来源审计。源码行号按固定原文件计数，以下正文行号均属本轮输入。

| 输入 | SHA-256 |
|---|---|
| [T03-05 正文](../../knowledge/03-communication/rccl-runtime-and-verification.md) | `e9093ffb1a536c57cb14bee39e6bd72e8183985d7bc01875cf89f480531bd855` |
| [T04-01 正文](../../knowledge/04-data-storage/training-data-path.md) | `f703eba9a49f545e7e62ec3864c3e0b176b313f9fcdcbdfffc565200c2cbcb81` |
| [RCCL 来源记录](batch-19-rccl-sources.md) | `891c737e94dcfc4d1c40e5a7ed9cf6f96847ba56fdecb46482a8c3394b8b50c2` |
| [T04-01 来源记录](batch-19-t04-01-sources.md) | `4e1e78607281286f4ec39b6b77298f4c0af7282a8ade9f65f826bca6ed5bb0f3` |
| [修订映射](batch-19-review-fixes.md) | `f0771b468e9f0e98f4b40856a1bad20be618b13407bc6e446e76c450b04a9e64` |
| [第一次复核](batch-19-codex-recheck.md) | `c4e7a10909bb153d8b4b728a53159ff8b5429ee8403df94264f2c1d6b8d616a0` |
| [初审报告](batch-19-codex-review.md) | `ebc802a44e708db5ab872c9d6f578115d8a3d6a71a42a9569369c6872b4f2aa2` |
| [来源审计](batch-19-source-audit.md) | `b47dcbd96f66b1d65825fea671e2e3348c2c4a85fd744c10c8b8907f6e019076` |
| [来源登记](../../sources/registry.yaml)（386 项） | `e84c3b6eb61a83a46dbbfd371e5de4112def120131e0c374181e8e5acbf8f51f` |

来源登记仍与初审同一身份；03/04 索引与 Batch 17/18 研究文件对照第一次复核输入未变。本轮写入保护覆盖正文、研究记录、修订映射、全部计划与既有其他报告，不将作者已存在的未提交改动归作本轮修改。

## 一次源复验与链接检查

以默认 TLS 校验 curl 只读重抓 12 份相关一次源，全部 HTTP 200，字节 SHA 与第一次复核相同：固定 `7da43026e4f2ef7600433c38c820732f7a205d22` 的 rccl-tests common.cu/README/src/timer.cc 和 RCCL group.cc；RCCL docs-10.1.0 的 api-library/env-variables/troubleshooting；固定 `bc51ab84cc6f35c77aab1c59886e0ea43681a317` 的 CopyKernel.cpp/CachingHostAllocator.cpp；CANN 8.2.RC1.alpha001 官方静态 0086/0091/0083。网页工具请求部分源码与 API 未取得时用 curl，不把 cache miss 当作 HTTP 404。

另对正文新加的 timer 链接进行两次精确路径检查：GitHub blob 和同路径 raw 均 HTTP 404，见 C09。未重新抓取其余全部远端引用；DCP/TorchData/其他 CANN 的固定证据范围沿用[第一次复核](batch-19-codex-recheck.md#一次源复验)，本轮主要核对受影响正文及映射一致性。未编译或执行上游代码，临时原文/日志没有镜像入库，无新增来源登记。

| 关键重抓证据 | 字节数 | SHA-256 |
|---|---:|---|
| rccl-tests common.cu | 107420 | `1339f9535d68b748677bd817e88d02002a71ff27b7f2b7ce41fcaccaa505f9d7` |
| rccl-tests README | 14309 | `7b2dbdab28a619a47c8ac685704fc6a1432fc7d42ce4c87c71ab82a7b905e2cc` |
| rccl-tests src/timer.cc | 615 | `c1e4e76679cc56c62b84633035a07ae563e7c6d47d769324c978b12c229d436f` |
| RCCL api-library HTML | 438446 | `a208670b5ca6c5b7adedce178a4e2dcad51459fe29a21fefcb34b6232c084cd5` |
| TorchNPU CopyKernel.cpp | 15497 | `ffd690fc786007e40e9db49c38226a6d93a0b5f5fe66bfbed3a681618b77e5b2` |
| TorchNPU CachingHostAllocator.cpp | 12355 | `ed44e2afcd1d7084c3904e6fb95c21995b6577756f48abd3b955cd69cb21e2a9` |
| CANN 0086 静态正文 | 9080 | `b8420f5c9cc3080c61acbb333cc390e6eeb7f60231e5f999f232a703bac4d85e` |
| CANN 0091 静态正文 | 11333 | `760def2eb4dd7a58b3ceb77e0ed6ae9d62e638491016552109265783f85ea947` |

## 状态与关闭依据

| ID | 当前状态 | 本轮判定 |
|---|---|---|
| C01 | CLOSED | 创建 API/config 和 InProgress 条件分支已补齐。 |
| C02 | CLOSED | 保持第一次复核的微秒/默认计时有限通过范围。 |
| C03 | OPEN | 覆盖门禁已补，但 `-O both` 不是该版本的双 placement 参数。 |
| C04 | CLOSED | 保持有限跨节点设计通过，期限措辞已同步。 |
| C05 | CLOSED | 初始化日志与 COLL 时间线分开保留，缺启动证据不推断 NIC count 一致。 |
| C06 | CLOSED | 缓存阶段及访问序列契约已分列，失败/原因未知/证据不足已区分。 |
| C07 | CLOSED | 保持状态来源和回退条件通过，近旁来源链已补。 |
| C08 | CLOSED | allocator 与 CopyKernel 同步分支分开；0091 方向、0086 状态及记录前提已修正。 |
| C09 | OPEN | T04-01 来源修订已满足；T03-05 新 timer 链接错误，需改精确路径。 |

### C01 — CLOSED

T03-05 L53 已给出 `ncclCommInitRankConfig`、`ncclConfig_t` 与 `NCCL_CONFIG_INITIALIZER`，与 L58 的 blocking=0 创建条件连通。L56 将 InProgress 限定到 non-blocking 且 preconnect/async job 的后台分支，其他成功返回不被模式标签替代；成功后建立依赖、设备完成、Abort 线程与 deadline 的边界保留。[api-library 的 InitRankConfig / Communicator Configuration](https://rocm.docs.amd.com/projects/rccl/en/docs-10.1.0/api-reference/api-library.html)、[group.cc L919–958](https://github.com/ROCm/rocm-systems/blob/7da43026e4f2ef7600433c38c820732f7a205d22/projects/rccl/src/group.cc#L919-L958)。

非阻断文字维护：L56“错误分支按 (e) 处理”指向设备完成，宜改指紧邻的“错误”条 L57。实际错误条和恢复前提已存在，本轮不将这一编号错指重新解释为全部错误处理未交付，也不新增 ID。

### C03 — OPEN：`-O both` 实际只选择 in-place

T03-05 L77/L95 已统一 Float/Sum 与迭代/校验参数，L77/L96 加入计划覆盖完整、校验开启、缺行/N/A/提前停止不判 P1 的门禁。这些修订接受。剩余是两个命令中的 `-O both`：固定 README 只定义 `-O 0`（in-place only）和 `-O 1`（out-of-place only），两种 placement 是**不传 `-O` 时的默认值**。[README L187–190](https://github.com/ROCm/rocm-systems/blob/7da43026e4f2ef7600433c38c820732f7a205d22/projects/rccl-tests/README.md#L187-L190)。

源码默认两个 enable 标记均为 1；解析 `-O` 时直接调用 `strtol`，再把另一个标记反置。`both` 没有数值前缀，按该解析路径得到 0，因此 out-of-place 关闭、in-place 开启。这里是源码判读，未实际运行 benchmark。[common.cu L174–179](https://github.com/ROCm/rocm-systems/blob/7da43026e4f2ef7600433c38c820732f7a205d22/projects/rccl-tests/src/common.cu#L174-L179)、[L2092–2095](https://github.com/ROCm/rocm-systems/blob/7da43026e4f2ef7600433c38c820732f7a205d22/projects/rccl-tests/src/common.cu#L2092-L2095)。

当前覆盖门禁会阻止缺 out-of-place 时判 P1，但计划命令本身仍不实现声明的双 placement 覆盖。下一次关闭条件仅需修正这处选项及同步描述：全文省略 `-O`，声明使用其默认双 placement；或分别设计 `-O 0` / `-O 1` 两种运行。沿用当前单次默认模式设计时，可采用如下修订命令（文档建议，未执行）：

```bash
mpirun -np 16 -N 8 --bind-to numa ./build/all_reduce_perf -d float -o sum -n 20 -w 1 -m 1 -b 8 -e 1G -f 2 -g 1 -c 1
```

输出核对按各尺寸行里的 out-of-place / in-place 两组列进行；默认输出表头实际是两组列，不要求为同一尺寸额外拼成两行。该形态见[util.cu L760–787](https://github.com/ROCm/rocm-systems/blob/7da43026e4f2ef7600433c38c820732f7a205d22/projects/rccl-tests/src/util.cu#L760-L787)，本轮沿用已核对快照。其他 MIN_BW、完整行、正确性与性能未判定条件保持，不要求增加实机验证或新平台范围。

### C05 — CLOSED

T03-05 L98 不再从 COLL-only 日志推断 NIC count。启动前保留 INIT/BOOTSTRAP/NET 证据，另读 COLL 时间线，或明确读另存的启动日志；缺启动证据时 NIC 检查无法判断。与 L67/L68 的目的、pid/rank 映射和 MPI 传播边界相符，期限措辞在 L97 已同步。[env-variables 的子系统定义](https://rocm.docs.amd.com/projects/rccl/en/docs-10.1.0/api-reference/env-variables.html)、[troubleshooting 的 Replayer 与初始化 NIC counts](https://rocm.docs.amd.com/projects/rccl/en/docs-10.1.0/how-to/troubleshooting-rccl.html)。这是证据读取/判读设计，不宣称已实际取得启动或挂起日志。

### C06 — CLOSED

T04-01 L85 的预期访问序列已由固定 sampler/shuffle/drop_last/补齐规则或未中断对照生成，manifest 对象身份不再代替顺序契约。L181 将读/派生结果/组 batch 缓存分开；仅变换配置变化以派生层重算/新结果身份为证据，不要求持久化后端字节回升；目标策略未知仍只记现象。L182 明确违反已声明契约则该项校验失败、原因待查，未确定契约或证据不足才是无法判断。三类验证、DCP/CRC 已接受范围保留，未新增统一格式、通用阈值或 exactly-once 保证。判读关系是作者方法设计，不冒充上游实现或现场结果。

### C08 — CLOSED

T04-01 L164 已删除 allocator 的 resume 例外；L166 将先同步后拷贝及 resume 告警放回 non_blocking=False 的 CopyKernel 分支，不推广到其他路径。L168 及研究记录已一致为源 stream RecordEvent 在先、目标 stream 等待 event 的后续任务依赖；主机异步返回不等于完成，随后用同步确认。0086 查询返回 0、出参 COMPLETE/NOT_READY 与 record/query 顺序/跨线程乱序已分开。[CachingHostAllocator.cpp L181–205](https://github.com/Ascend/pytorch/blob/bc51ab84cc6f35c77aab1c59886e0ea43681a317/torch_npu/csrc/core/npu/CachingHostAllocator.cpp#L181-L205)、[CopyKernel.cpp L97–121](https://github.com/Ascend/pytorch/blob/bc51ab84cc6f35c77aab1c59886e0ea43681a317/torch_npu/csrc/aten/common/CopyKernel.cpp#L97-L121)、[0091](https://www.hiascend.com/doc_center/source/zh/CANNCommunityEdition/82RC1alpha001/API/appdevgapi/aclcppdevg_03_0091.html)、[0086](https://www.hiascend.com/doc_center/source/zh/CANNCommunityEdition/82RC1alpha001/API/appdevgapi/aclcppdevg_03_0086.html)。

条件接口不作为目标运行能力证明，0020/0086 弱版本绑定、pin_memory/NPU 配套未知、0088/0089 超时细节未知保持；同步分支的错误/告警不得当作计算成功证据。未新增 NPU 实验或部署组合声明。

### C09 — OPEN：仅余 T03-05 的 timer 精确路径

正文 group/对照/计时/PR、T04-01 Stateful/游标/NPU 的近旁链接已补，研究记录 CHANGELOG/RegisterTests/dataloader/state_dict_loader/0091 同步，悬空 §4 和未登记 PR #6843 保持删除；作者与审阅者取证范围分开。T04-01 对应的 C09 要求已满足，不以另一个文件的 timer 链接阻断其本轮有限内容范围。

T03-05 L75 新加的 timer 链接漏了 `src/`，本轮下列两个精确地址均 HTTP 404：

- [正文使用的错误 blob 路径](https://github.com/ROCm/rocm-systems/blob/therock-10.1/projects/rccl-tests/timer.cc)。
- [同 ref / 路径的 raw 检查](https://raw.githubusercontent.com/ROCm/rocm-systems/therock-10.1/projects/rccl-tests/timer.cc)。

正确文件是 [固定 commit 的 projects/rccl-tests/src/timer.cc](https://github.com/ROCm/rocm-systems/blob/7da43026e4f2ef7600433c38c820732f7a205d22/projects/rccl-tests/src/timer.cc)，本轮 raw 获取为 HTTP 200、615 B，记录 SHA 见证据表。下一次关闭条件：将 L75 href 改为这一精确路径并定向复验；不需新增 source ID，不重做已接受的全部定位表。

## 通过范围与后续门槛

| 范围 | 判定 | 保留条件 |
|---|---|---|
| T03-05 | 暂不通过 | C03 的 placement 参数、C09 的 timer URL 待关闭；T03-06 继续等待。 |
| T04-01 | 本轮原定内容/来源范围通过 | 数据身份/游标、缓存/对照与选定 NPU 源码语义为有限文档范围；正文保持 draft/source_checked。 |
| T03-06/T03-07/T03-08 | 本轮未审阅 | 不由两篇正文的结果推导整批完成或解锁全部后续。 |

T04-01 的通过不将 T02-11 草稿升级为已验收前置，不关闭任务计划中的依赖或扩展硬件配套；T02-10 仍按 [C08 例外清单](batch-17-t02-10-exception.md)条件满足，累加精度/cubeMathType 未证部分继续 unknown。整栈组合、latest/别名 diff、PR 最早入版/底层挂起机理和无实机证据等既有边界均保留。

本轮只新增复核报告并同步初审/第一次复核/来源审计的最新状态入口。作者正文、研究记录、修订映射、索引、登记、任务计划和 Batch 17/18 其他记录保持本轮输入；不代替作者修改命令或链接。历史报告保留当轮判定，不改写为当前结果。

`make check` / `make build` 均 PASS（87 篇内容 / 386 项来源）。报告本地链接、状态集合和受保护输入身份另行核对；结构通过不证明远端 URL、技术正确性或硬件验证。未改 `src/kb/`，未添加内容镜像测试或运行 `make test`；没有 MPI/RCCL、GPU/NPU、真实存储执行、设备配置或故障注入。
