# 第三批独立验证审阅

审阅日期：2026-09-29。审阅者：`gpt-6-astra / xhigh`。这是正文修改前的独立审阅记录，不是正式知识条目，也不是 GPU/NPU 实验报告。

结论：**本轮暂不应整体标为完成。发现 4 项 P2 技术问题，涉及 F07、F08、F18；另有 3 项 P3 定位或一致性问题。未发现 P1。** F10、F17 在此次抽查范围内未发现实质问题。明确保留的未知条件、没有硬件或没有执行实验均不构成缺陷。

## 审阅范围与方法

先读取 `AGENTS.md`、`README.md`、`docs/authoring-guide.md` 和 `content-outline.md`，再阅读五篇正文、第三批来源记录与总审计、来源登记、章节和平台/任务入口，以及计划状态。

实际打开并抽查了 NCCL 2.27.5 的 collective、stream、communicator 和 group-call 页面；PyTorch 2.8 distributed 页面及其 `WorkNCCL` 实现；固定 nccl-tests README、性能说明、`common.cu`、AllReduce/AllGather/AlltoAll 实现与许可；固定 cann-hccl README 与根许可；HCCL 正式 PDF；DCP 2.6 文档与固定 `filesystem.py`；Linux `fsync(2)`；固定 MindIO ACP README；Google SRE 四章、SuperBench PDF 和 SDC v1 PDF。

GitHub/Gitee 的原始文件只通过 HTTPS 读取，未执行其内容。PyTorch `v2.8.0` 经只读 `git ls-remote` 解析为 `ba56102387ef21a3b04b357e5b183d48f0afefc7`，随后用完整 SHA 再次读取 `ProcessGroupNCCL.cpp`。未安装、构建或运行上游项目，没有访问硬件、集群或存储实验。未运行 `make`，避免与主任务并发构建；主任务此前报告的结构检查通过不作为技术正确性的证据。本审阅仅新增此文件。

以下正文行号以本次审阅开始时的版本为准；修订后可用段落标题和引用中的原文定位。

## P2-01：NCCL 调用返回不总是已经入队

- 位置：`knowledge/03-communication/collectives-and-rank-progress.md:76`，以及第 125、127 行的概括。
- 问题：该段无条件表述 NCCL collective 在成功入队到给定 stream 后返回。对放在 `ncclGroupStart/End` 内的调用，这个判断不成立；读者按它把逐次调用返回记为“已提交设备”，会错误重建进度。
- 证据：同一个 [NCCL 2.27.5 Group Calls 页面](https://docs.nvidia.com/deeplearning/nccl/archives/nccl_2275/user-guide/docs/usage/groups.html)的 “Management Of Multiple GPUs From One Thread” 明确说明组内 stream 操作可以在尚未入队时返回；“Nonblocking Group Operation” 又区分 `ncclGroupEnd()` 返回 `ncclSuccess` 与 `ncclInProgress`，后者仍可能在后台提交。
- 修正建议：将普通调用的成功返回限定到其实际调用模式，补充组内调用与非阻塞 communicator 的提交完成边界；明确 API 聚合组与 process group/communicator 不是同一个对象。不要把 `ncclGroupEnd()` 的任意返回都写成已入队。把本次新增核对的 group-call 页面加入 F07 研究记录及原来源条目的核对范围。
- 完成判据：第 76 段和平台表不再把组内调用返回当作普遍的入队标志。

## P2-02：Work 等待和完成状态被概览简写过度概括

- 位置：`knowledge/03-communication/collectives-and-rank-progress.md:76`。
- 问题：`Work.wait()` 被概括为不阻塞 CPU；`is_completed()` 被描述为成功入队且输出可安全使用。前者遗漏实际例外，后者把概览页面的简化描述直接当作 NCCL Work 的成功条件。本文的主题正是区分完成层次，这两项会导致错误解读日志和完成标志。
- 证据：同一 [PyTorch 2.8 Work.wait API](https://docs.pytorch.org/docs/2.8/distributed.html#torch.distributed.Work.wait)明确说明显式 timeout 会等待 CPU 线程；该页 `init_process_group` 还说明 `TORCH_NCCL_BLOCKING_WAIT`。固定实现的 [775–839 行](https://github.com/pytorch/pytorch/blob/ba56102387ef21a3b04b357e5b183d48f0afefc7/torch/csrc/distributed/c10d/ProcessGroupNCCL.cpp#L775-L839)首先建立当前 CUDA stream 对结束事件的依赖；`blockingWait_` 或显式 timeout 分支在 CPU 上等待，barrier 还有专门的 CPU 同步分支。默认 `blockingWait_` 的读取位于第 960 行。
- 额外证据：[580–585 行](https://github.com/pytorch/pytorch/blob/ba56102387ef21a3b04b357e5b183d48f0afefc7/torch/csrc/distributed/c10d/ProcessGroupNCCL.cpp#L580-L585)的 `isCompleted()` 返回异常存在或 GPU 执行完成；[649–661 行](https://github.com/pytorch/pytorch/blob/ba56102387ef21a3b04b357e5b183d48f0afefc7/torch/csrc/distributed/c10d/ProcessGroupNCCL.cpp#L649-L661)检查结束事件。因此 `True` 不能单独作成功或输出安全证据，也不能简单等同“刚入队”。概览页和此具体 backend 实现的措辞差异应如实保留。
- 修正建议：限定正常、非 barrier、未显式设置 timeout、未启用 blocking-wait 的 NCCL Work 等待路径；分别说明 stream 依赖、CPU 等待、异常和 GPU 结束事件。删除 `is_completed()` 的无条件成功推论，或明确概览只提供通用说明，具体 WorkNCCL 以固定实现及错误状态为准。更新 F07 研究记录和来源条目的固定源码定位。
- 完成判据：可以从正文判断默认返回为何不是 CPU 观测到的设备完成，也能知道什么条件会阻塞 CPU；完成标志和成功状态不再混用。

## P2-03：nccl-tests 的显示 time 不总是带宽公式的分母

- 位置：`knowledge/03-communication/bandwidth-baselines.md:60`、第 100–109 行计时说明；相应 F08 研究记录。
- 问题：公式前将 `t` 定义为工具“最终用于报告的平均操作时间”，但固定实现允许 `-C 1` 用 CPU 时间替换显示列，同时带宽仍按另一个完成时间计算。读者据显示 time 重算 `algbw` 会得到不一致结果，并可能把 CPU 提交时间误作实际操作耗时。
- 证据：固定 `b4d5beebca8a76cf01335f724d154b9b9d394d96` 的 [`common.cu:795–811`](https://github.com/NVIDIA/nccl-tests/blob/b4d5beebca8a76cf01335f724d154b9b9d394d96/src/common.cu#L795-L811)分别计算 `cputimeSec` 和 `deltaSec`，后者在完成等待后归一化，graph 模式还除以 launch 次数，随后按 `-a` 聚合；[823–824 行](https://github.com/NVIDIA/nccl-tests/blob/b4d5beebca8a76cf01335f724d154b9b9d394d96/src/common.cu#L823-L824)始终把 `deltaSec` 传给 `getBw`；[886–887 行](https://github.com/NVIDIA/nccl-tests/blob/b4d5beebca8a76cf01335f724d154b9b9d394d96/src/common.cu#L886-L887)才用 `report_cputime` 选择显示时间。
- 修正建议：公式的 `t` 定义为 `getBw` 实际使用的 `deltaSec`。明确默认 `-C 0` 的显示 time 与此分母一致，而 `-C 1` 的 CPU time 不能用来回算报告带宽。区分 `-I` 的逐次 CUDA-event 摘要与主表分母；`-K` 仅处理该摘要，不改变主表带宽。若展开逐次聚合，固定实现第 889–914 行使用逐次跨 GPU/线程/进程最大值，再计算摘要，不要把它混同主表 `-a`。
- 完成判据：默认、CPU time、graph、逐次 event 四种路径的分母和显示字段能明确区分，且不需执行基准即可对照固定源码验证。

## P2-04：合成 GPU 例在缺乏排序依据时宣称某 rank 最晚

- 位置：`knowledge/08-reliability/evidence-and-hypotheses.md:122–126`。
- 问题：例子同时声称 `rank 7` 的 batch-ready “最晚”及跨主机墙钟偏移未量化，却没有另外给出共同观测点、校准时钟或因果顺序。相同 step/collective ID 只能对齐身份，不能建立跨 rank 时间顺序。第 124 行承认事件实现边界未核对，却直接把其偏移标为支持输入/传输先变慢；这违反了本页第 59–77 行对时钟、字段语义和未知的约定。
- 证据：这是正文内部的可推导矛盾；Google SRE [Test and Treat](https://sre.google/sre-book/effective-troubleshooting/#test-and-treat)所要求的测试前提与混杂控制也不能补足该例未给出的观测条件。主任务另提出同一疑点，独立核对后确认成立。
- 修正建议：可以把观测改为同一 rank 的单调时钟测得某一明确阶段耗时，相对该 rank 的可比历史窗口延长，保留跨 rank 绝对先后未知；若保留“最晚”，应补齐足够精度的共同时间基准或可证明该顺序的因果 trace。事件边界仍未知时，H1 只保留候选，不标支持。下一项检查可先确认字段边界再分段关联。
- 完成判据：示例每一项“支持”均由已明确对象、时间和语义的观测支撑，不靠 step ID 替代时钟校准。

## P3-01：多个固定源码行号和 HCCL PDF 页锚点没有落在支持位置

这些错误不会使对应全部技术主张失真，但使“精确来源已核对”的交付难以复核，建议同轮修正。

F08 的 fixed SHA 本身正确；以下为本次直接读取 raw 文件得到的行号：

| 正文位置与主张 | 当前链接的问题 | 固定 SHA 的实际位置 |
|---|---|---|
| 第 46 行，大小解析 | 224–258 从 communicator 初始化开始，未覆盖 K 与最终返回 | `common.cu:240–274` |
| 第 71 行，AllReduce 公式 | 52–58 是初始化尾部 | `all_reduce.cu:59–65` |
| 第 71 行，AllGather 公式 | 33–39 只到 base bandwidth，缺系数 | `all_gather.cu:38–44` |
| 第 71 行，AlltoAll 公式 | 43–49 未覆盖系数 | `alltoall.cu:48–54` |
| 第 91 行，两个 buffer 模式 | 871–886 属于检查和显示时间 | `common.cu:952–960` |
| 第 106 行，warm-up 与 barrier | 669–715 属于 event timing 辅助函数 | `common.cu:720–733` |
| 第 107 行，时间归一化和 rank 聚合 | 738–765 属于 graph capture/性能循环前半 | `common.cu:795–811` |
| 第 108 行，逐次 event 取时/摘要 | 617–658 属于发起 collective 和完成等待 | 事件取时 `666–683`；摘要 `889–914` |
| 第 131 行，检查迭代与错误汇总 | 767–821 属于性能计时/graph 清理 | `common.cu:828–883` |

F07 中 HCCL PDF 的 `#page=` 使用从 1 起的物理页数；本次网页工具的 `P0` 才表示首页。应避免将零基页索引写入链接：

- 第 39 行的 rank/group 相关概念在物理第 9–10 页，rank ID 定义在第 10 页；当前 `#page=8` 在执行流程。
- 第 78 行的 Notify/SDMA 和执行文字在物理第 8 页；当前 `#page=7` 只到简介及流程引入。
- 第 101 行的单卡/链路导致大量超时在物理第 9 页；当前 `#page=8` 在前页。
- 第 63 行 AllReduce 一致性约束在物理第 47 页，Broadcast 一致性约束在第 48 页；当前 `#page=45` 还在配置/通信域名称接口。建议拆成两个精确页链接，并保留章节 3.3.1/3.3.2。

同步检查 F07/F08 研究记录中的页码说明，注明物理页码或文档印刷页码，避免继续混用。

## P3-02：HCCL 模型中的 n 缺少独立定义

- 位置：`knowledge/03-communication/bandwidth-baselines.md:147`。
- 问题：引用 `D = α + nβ + nγ` 时没有定义这里的 `n`；本页前文的 `n` 是 rank 数。固定 [cann-hccl README 算法介绍](https://gitee.com/ascend/cann-hccl/blob/2d685b084a60366b47ad8e50a563ee5c4dbef7fe/README.md#alg_desc)第 38 行明确这里的 `n` 是通信数据的 byte 数，节点个数另用 `p`。
- 修正建议：明确重新定义 `n` 的单位为 byte，或为本页改用 `m`/`S_h` 并注明符号替换，使 `α`、`mβ`、`mγ` 都是时间；不要让读者把 rank 数乘进每 byte 时间。

## P3-03：数据存储主题地图仍把已有主题整体标待建设

- 位置：`knowledge/04-data-storage/index.md:32–33`，主题 04.3/04.4。
- 问题：同页已有 F10 草稿入口，但主题地图仍将 checkpoint 读写持久化及完整性整体标为待建设，与通信/可靠性章节“已有基础正文草稿，细节待补”的状态表达不一致。
- 修正建议：04.3 链接 F10 并标明已有基础草稿；04.4 可注明已有部分边界说明、完整专题待补。无需把整章或未写的操作流程标成完成。

## 抽查通过的边界与未发现问题的部分

- NCCL 2.27.5 的同 count/datatype 契约、root 为 communicator rank、PyTorch 多 process group 的创建/执行顺序和显式多线程同步要求，与精确官方页一致。NCCL 2.26 起隐式 launch ordering 的条件没有被写成取消顺序要求。
- NCCL-tests 表内六种 bus factor、ReduceScatter 总输入与 AllGather 总输出的 `S`、十进制 GB/s 与二进制参数后缀、AlltoAll 不支持 in-place 正确性报告、检查迭代不覆盖全部 timed iterations，均有相应固定文档/源码支持；未伪装成物理链路计数器或本地性能结果。
- HCCL 旧 CANN RC/alpha API PDF 与 `cann-hccl` master 固定快照被分别使用；正文没有把它们拼成配套。Test 字段、未知精确公式、未知默认统计和未知 NPU 峰值的处理恰当。
- F10 对 DCP Future、writer 的分工以及固定 `filesystem.py` 的 `sync_files`、数据同步、临时元数据和改名描述与源码相符。源码还包含已有 `.metadata` 删除后再 rename 的分支；正文并未据此许诺覆盖更新原子性。文件、目录记录和后端故障模型被分开，也未声称跨文件事务或任意故障持久性。MindIO ACP README 的内存暂存/异步后端写入被正确限缩使用。
- F17 的四维框架和故障域明确是原创整理；SRE 的 SLI、隐式错误、恢复系统原则与 SuperBench 的 Azure GPU 灰色退化研究没有被写成跨平台阈值或已验证标准。
- F18 使用的 SDC v1 确实以数据中心 CPU 为研究范围，正文明确拒绝将其发生率、个案或日志覆盖外推到 GPU/NPU；NPU 例子保持合成且没有把无日志当成支持 SDC 的证据。
- 来源登记区分了源码、网页、论文和软件制品。此次抽查的 nccl-tests README/根 BSD 许可、cann-hccl 限定用途许可和 HCCL PDF 权利声明未与登记冲突。未知文档许可未被自动套上代码许可证，没有看到复制外部图表或长段正文。
- 五篇均保留 `draft`，`source_checked` 限定到来源核对；计划为 `reviewing`，README 与总审计没有提前宣布第三批审阅通过。平台/任务入口链接同一正文，没有重复主归属。

## 交接与阻断范围

P2-01/P2-02 阻断 F07；P2-03 阻断 F08；P2-04 阻断 F18，因此第三批不能整体结束。F10、F17 无此次审阅发现的技术阻断。P3 项建议一并修正，尤其固定来源定位可在本次源码核对基础上直接完成。

主任务修订后应核对相关段落和来源记录，再执行仓库要求的 `make check` 与 `make build`。关闭本次问题表示草稿范围内的技术/编辑问题已处理，不意味着文章需要改成 `reviewed`，也不提升为 `reproduced`。

## 修订后定向复核：本轮问题全部关闭

复核完成日期：2026-09-30（Asia/Shanghai）。复核者：`gpt-6-astra / xhigh`。**最新结论：原审阅中的 4 项 P2 和 3 项 P3 均已关闭，在本次修订范围内未发现剩余实质问题；第三批可结束草稿交付阶段。** 上文保留首次审阅时的发现和阻断状态作为历史记录，本节是修订后的结论。

本次重新读取 F07、F08、F18 的相关段落，F07/F08 来源提取记录、registry 对应条目及数据存储索引，并与首次审阅已经实际读取的固定源码和官方页面逐项对照。未扩展为新一轮广泛审阅，未修改正文，未运行上游程序或硬件实验。

| 原问题 | 修订后的定位与确认结果 | 状态 |
|---|---|---|
| P2-01 NCCL 返回/入队边界 | F07 第 76 行与第 129–131 行的平台表已区分组内调用、nonblocking group 的 `ncclInProgress`/`ncclSuccess` 和设备完成；API 聚合组与 communicator 已明确分开 | 关闭 |
| P2-02 Work 等待与完成状态 | F07 第 78–80 行已限定普通非 barrier/default wait 路径，写明 timeout、blocking-wait、barrier 的 CPU 等待条件；`is_completed()` 与异常/结束事件的关系及不能单独证明成功已说明。固定 `ba561023…` 源码定位进入正文、提取记录和 registry | 关闭 |
| P2-03 显示 time 与带宽分母 | F08 第 60 行将 `t` 定义为实际 `deltaSec`；第 108–109 行区分 `-C` 显示、graph 归一化、主表 `-a` 和逐次 event 摘要，说明 `-I/-K` 不替换带宽分母；提取记录一致 | 关闭 |
| P2-04 合成例的时间排序与假设支持 | F18 第 122–126 行改用同 rank 单调时钟及已确认的主机取批边界，与本 rank 历史窗口比较；跨 rank 先后保持未知。H1 只得到阶段变慢现象的支持，没有再宣布其为慢 step 起因 | 关闭 |
| P3-01 固定来源定位 | F08 的解析、公式、warm-up、计时、逐次摘要、正确性和 buffer 模式锚点均已改到前述固定文件位置；F07 的 HCCL 正文链接已使用物理第 8、9、10、47、48 页，研究记录其余位置改用明确章节 | 关闭 |
| P3-02 HCCL 数据量符号 | F08 第 148 行使用 `m` 表示 byte 数并解释原文符号替换，节点数 `p` 与 rank 数 `n` 不再混淆；提取记录一致 | 关闭 |
| P3-03 数据存储主题地图 | 索引第 32–33 行已链接 F10，分别标明已有基础草稿/部分完整性说明，以及仍待补充的内容 | 关闭 |

主任务报告修订后 `make check` 与 `make build` 通过，覆盖 24 个条目和 33 项来源；复核者未重复运行。这一结构检查与以上定向技术复核分别记录。原来的 F10/F17 抽查结论不变；未知硬件条件、平台配套、性能阈值和现场验证状态继续保留。关闭本轮问题不将任何条目自动提升为 `reviewed` 或 `reproduced`。
