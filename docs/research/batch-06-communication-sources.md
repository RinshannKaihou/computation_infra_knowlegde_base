# 第六批 T03 / T04 通信超时来源准备

> 调研记录，不是知识库正式正文，也不是生产环境操作手册。

- 调研范围：T03-P/C/X（Ascend HCCL 超时）与 T04-P/C/X（NVIDIA NCCL 超时）。
- 核对日期：2026-09-30。
- 执行边界：只读取公开文档、固定版本源码索引和公开 Issue；未安装或运行上游软件，未拉取容器或大型制品，未访问集群，未执行通信测试、故障注入或硬件诊断。
- 证据边界：Issue 中的环境、日志、复现率和归因首先是报告者陈述；状态为 `Closed`、`DONE` 或 `Closed as not planned` 均不自动表示问题已修复。

## 可写判定

当前证据足以写六篇边界明确的草稿，且无需为“覆盖所有超时根因”继续无限搜集：

- T03-P 可按“先对齐所有 rank 的进度和最早异常，再分计算/次序、设备、网络、超时配置支路”来写。CANN 8.1.RC1.alpha001 HCCL 用户指南明确支持这些分支，但不能把某个 `EI0002` 或 `507034/507048` 单独写成已定位根因。
- T03-C 可选择 vLLM Ascend #14296。它有完整软件栈、16 卡单节点、阶段、约 300 秒时间线和 HCCL AIV group 证据，后续补读三条评论取得报告者 AI_CPU 缓解反馈，但仍无独立根因确认或可核验修复链。报告中“只关闭 `enable_dsa_cp`”与“同时关闭 `enable_dsa_cp`、`enable_flashcomm1`”存在冲突，案例必须保留这一点。
- T03-X 可写成隔离环境中的验证设计：先验证相同 rank 映射和操作序列，再做单变量 AIV group/配置对照；不能把生产服务、整节点或网络故障注入当成默认步骤。
- T04-P 可结合 NCCL 2.27.5 文档、NCCL RAS（2.24 起）和 PyTorch 2.8 ProcessGroupNCCL 观测字段。正文必须先声明目标 NCCL/PyTorch 版本，不能把 2.27.5 或 PyTorch 2.8 的变量倒推为旧版可用。
- T04-C 可选择 PyTorch #118369。报告展示 rank 1–7 在同一 `SeqNum=880` 的 `BROADCAST` 超时而 rank 0 没有相同超时行；维护者把“rank 0 未进入同一 collective”作为调查假设，报告者随后提供 rank 0 利用率为 0% 的快照。Issue 最终因 stale 自动关闭，没有修复 PR 或已证实根因。
- T04-X 可写成被动 flight-recorder/RAS 观察加受控 `nccl-tests` 基线的设计。缺 rank 或错序注入只允许在一次性、无业务的隔离作业内设计，不在正文给出可直接复制到生产的注入命令。

## 共用证据模型

F07、F08、F18 已经提供正文应复用的分析边界：

1. **症状**：框架或通信层报告哪一个 rank、communicator、collective、sequence/op index、数据量和 timeout。
2. **进度**：同一 communicator 内各 rank 最后完成、正在等待、下一项计划执行的 collective 是否一致。不同 communicator 的序号不能直接比较。
3. **更早异常**：先于大面积 timeout 的进程退出、设备错误、CUDA/NPU kernel 错误、OOM、数据分支、checkpoint、编译/图捕获或网络事件。
4. **传输与设备**：链路、接口选择、CQE/link-down/packet-loss、GPU/NPU 健康、拓扑和容器可见性只能作为独立证据，不因 timeout 自动成立。
5. **状态**：报告时的 `open/closed/DONE`、可见评论、关联 PR、版本发布和验证结果分开记录。

正式 procedure 的完成条件不应是“提高 timeout 后不再立刻报错”，而应至少达到以下一种：

- 找到第一个偏离共同 collective 次序或没有进入目标 collective 的 rank，并能解释其他 rank 的等待；
- 找到早于通信超时、与 rank/设备/链路对应的独立故障证据；
- 在固定软件、rank 映射和工作负载后，受控对照能重复改变同一观测量；
- 证据不足时明确收敛为“根因未定”，保存所缺的 rank 日志、拓扑、版本或时间同步信息。

## T03：Ascend HCCL 超时

### 官方证据与版本边界

#### CANN 8.1.RC1.alpha001 HCCL 用户指南

[《CANN 社区版 8.1.RC1.alpha001 集合通信用户指南 01》](https://www.hiascend.com/doc_center/source/zh/CANNCommunityEdition/81RC1alpha001/devguide/hccl/hcclug/CANN%E7%A4%BE%E5%8C%BA%E7%89%88%208.1.RC1.alpha001%20%E9%9B%86%E5%90%88%E9%80%9A%E4%BF%A1%E7%94%A8%E6%88%B7%E6%8C%87%E5%8D%97%2001.pdf)的文档日期为 2025-03-19。PDF 印刷第 83–84 页（零基页面索引 88–89）的 9.1.2 节“执行通信操作超时（EI0002）”可支撑 T03-P 的主干：

- `Notify` 等待超时可能伴随 remote rank、heartbeat lost、进程退出或网络断开信息。
- 任一 rank/链路失败都可能使其他 rank 等待；另一组候选包括某 rank 长时间执行阻塞任务、部分 rank 没有到达同一 notify、任务序列不一致、跨机链路不稳，以及训练场景中执行/连接 timeout 配置关系。
- 如果只在部分 rank 报 timeout，应优先检查其他 rank 是否更早退出、报错或卡在别处；如果所有 rank 都 timeout，应比较首末报错时间，并寻找最后进入通信或被 checkpoint 等工作阻塞的 rank。
- 设备日志中的 `error cqe`、网络拥塞和 link-down 是需要额外证据验证的支路，不是 `EI0002` 的同义词。

本指南与现有 `src.huawei.hccl-api-cann-8.0-rc1-alpha003` 不是同一版本。前者支撑 8.1.RC1.alpha001 的排查分支；后者只支撑 8.0.RC1.alpha003 API 语义，不能拼成一个经验证的配套栈。

指南还给出 `HCCL_CONNECT_TIMEOUT`、`HCCL_RDMA_TIMEOUT`、`HCCL_RDMA_RETRY_CNT`、`HCCL_EXEC_TIMEOUT` 等变量的版本内说明。正式 procedure 不应抄一个统一 timeout 数值：指南里的 `export HCCL_EXEC_TIMEOUT=3600` 是示例，不能代替基于工作负载阶段、正常耗时和版本的判断；延长 timeout 也不能修复错序、进程退出、设备错误或断链。

#### 固定实现与既有机制页

- 复用 `src.ascend.cann-hccl-2d685b08`，只把固定 commit `2d685b084a60366b47ad8e50a563ee5c4dbef7fe` 当作 HCCL Test/实现接口快照。它不能替代 CANN 产品支持矩阵，也不能证明某个生产故障的根因。
- 复用 F07 的 rank-progress 记录法和 F18 的 hypothesis table；HCCL 的 op/tag、stream/task、rank 和时间戳按原字段保存，不把它们强行映射为 NCCL 的 `SeqNum`。
- 复用 F08 的基线边界：带宽下降只能推动“路径/负载/拓扑变化”假设，不能单独证明超时来自网络。

### T03-P procedure 的证据顺序

#### 1. 先固定环境和身份

至少记录：CANN、HCCL/torch_npu/框架版本，容器或宿主边界，NPU 型号与数量，单机/多机，rank 到设备/节点/网卡的映射，communicator/group 名称，以及报错是否发生在初始化、训练/推理、checkpoint、profile/图捕获或退出阶段。字段未知时写 `unknown`，不从错误码推断硬件或网络。

#### 2. 建立跨 rank 时间线

以同一 group/tag/collective 为单位，提取每个 rank 的：最后成功项、等待项、stream/task/op index、最早错误时间、timeout 时间、进程退出时间。先校正主机时钟或记录无法校正；否则“最早/最后”只能是各节点本地时间。

HCCL 指南允许正文写出两个关键分叉：

- **部分 rank 先超时**：去其他 rank 查更早的设备/运行时/进程错误或没有进入该 collective 的证据。
- **所有 rank 都超时**：比较错误时间和最后进展，查长任务、checkpoint、数据不均、不同 collective 顺序和网络/设备支路。

#### 3. 保持互斥但可并行验证的候选支路

| 候选支路 | 支持证据 | 反证或仍缺证据 |
| --- | --- | --- |
| rank 没到达/次序不一致 | 同 group 内最后完成项不同；某 rank 在计算、数据或另一 collective；错误前已有进程退出 | 只有统一 `EI0002`，没有其他 rank 的前序日志 |
| 长计算或阶段性阻塞 | 同一 rank 在 checkpoint、图捕获、编译或长 kernel；等待时间与该阶段相符 | 只通过提高 timeout 暂时消失，未解释为何超出正常基线 |
| 设备/运行时错误 | timeout 之前有 NPU/AICore/AIV、ECC、掉卡或 runtime 错误，并能对应设备/rank | timeout 后的级联 `ERR99999` 或同步失败，不足以证明首因 |
| 网络/链路 | 同期 `error cqe`、link-down、packet loss、接口/路由或跨节点路径异常 | 单节点作业或仅有“remote rank unknown”，仍不能排除次序/设备问题 |
| timeout 配置 | 正常操作本来就超过当前、版本内合法的 timeout，且各 rank 仍在一致进展 | 错序、退出、断链时延长 timeout 只延后失败 |

#### 4. 停止条件与完成条件

- 一旦日志出现设备不可恢复错误、链路持续异常、进程退出或数据一致性风险，停止任何主动复现，把现场转交设备/网络/框架对应负责人。
- 不在生产作业中用反复拉长 timeout 作为“定位”。
- procedure 到“已定位”必须有可复核的 rank/时间/事件链；无法取得其他 rank 或前序日志时结论保持 `unknown`。

### T03-C 真实案例筛选

#### 采用：vLLM Ascend #14296

来源：[vllm-project/vllm-ascend #14296](https://github.com/vllm-project/vllm-ascend/issues/14296)，2026-08-14 打开；2026-09-22 03:17:18 UTC 以 completed 关闭，2026-09-30 观察仍为 Closed。

**环境。** 报告列出 PyTorch 2.10.0、torch_npu 2.10.0.post2、Python 3.11、vllm-ascend `releases/v0.26.0rc` commit `baaf1809`、vllm commit `d02df748bf`、openEuler 24.03 容器、CANN 9.0.1、单节点 Ascend 910B3 ×16。部署为单节点 PD-mixed、TP=16、DCP=16、MoE expert parallel，并使用 AIV expansion mode。

**时间线与状态。** 报告称权重加载后进入 `profile_run` / cudagraph capture，尚未接收真实请求；16 卡的 `aiv_all_gather_bfloat16_t` 等待约 300 秒后出现 vector core timeout。日志示例给出 task 时间约 03:43:22，随后 `EI0002`、`507034` 和 engine initialization failure。plog 中显示两个 AIV group（`group_name_103` 与 `group_name_3`）以及 rank 15、op index 181 的同步状态。

**可支持的有限结论。** 这是“启动期、同节点、特定图捕获/DCP/MoE/AIV 组合下，多 group 进展异常并级联为 HCCL timeout”的报告。报告者声称在两个物理节点上均能 100% 复现；这提高了复现陈述的具体性，但不是维护者独立验证，也不能排除共同的软件/配置条件。

**不能写成已证实的结论。**

- “DCP 与 MoE AIV group 并发导致死锁”仍是报告者归因；后续评论补充抢核初判与 AI_CPU 缓解反馈，自动回复不作为独立确认，未定位到可核验修复链。
- Issue 开头写关闭 `enable_dsa_cp` 后可启动；“规避旁路”和 Additional Context 又写必须同时关闭 `enable_dsa_cp` 与 `enable_flashcomm1`。这两个说法不能合并成已验证单变量 workaround。
- API 记录 completed 关闭；同刻作者含糊提及一个可能解决问题的 PR，编号却与 Issue 相同。具体关闭依据、真实修复提交/发行版本与质量性能复验仍未知。
- 这是 CANN 9.0.1/Ascend 910B3/vLLM 特定组合，不能据此给 CANN 8.1 或任意 HCCL 作一般性兼容结论。

#### 次选：Ascend PyTorch #IBS5FF

[Gitee Ascend/pytorch #IBS5FF](https://gitee.com/ascend/pytorch/issues/IBS5FF)提供另一种 `EI0002`/`507048` 形态：单机 8×910B2 64 GB、PyTorch 2.4.0、torch_npu 2.4.0.post2、CANN 8.0.RC3、Python 3.10.16；多个 rank 在 2025-03-10 04:19:37 附近报告同一 AllReduce tag 的 notify timeout，约 04:20:20 elastic launcher 终止进程。

它只适合作为“同一错误仍需回看其他 rank 和更早异常”的辅助材料：页面状态为 `DONE`，但没有可见维护者分析、关联 PR/branch 或明确修复；外链大日志未纳入本库，报告者加入的 synchronize/barrier 改动也没有得到维护者确认。若正式案例采用 #14296，则无需把 #IBS5FF 注册为主来源。

#### 不采用为 T03-C 主案例

- vLLM Ascend #1955：环境只到单机 910B2C×16 和 0.9.2rc1 镜像，状态为 wait-feedback 后关闭，缺少关键评论、关闭原因和修复；正文中的清理/重启命令也不应复用。
- vLLM Ascend #9490：主要是非 root、TP>1 初始化和派生镜像差异，不是证据完整的 HCCL 执行 timeout 案例，且环境变量/镜像改动相互混杂。

### T03-X 实验设计

实验目标是区分“rank/collective 进展分叉”“特定 group/配置并发”和“设备/网络独立故障”，不是证明整个 HCCL 栈健康。

| 项目 | 设计要求 |
| --- | --- |
| 隔离 | 使用无业务、可回收的测试节点/容器和专用 rank group；不与训练/推理服务共享 NPU、网卡、端口或日志目录 |
| 固定条件 | 固定 CANN/HCCL/torch_npu/框架 commit、模型/输入、rank 映射、group 创建次序、图模式与超时配置；记录每次唯一 run id |
| 被动基线 | 先在不注入故障的条件下收集各 rank 的最后成功项、group/tag、stream/task/op index、阶段时间和设备/链路状态 |
| 单变量对照 | 只改变一个已记录的 group/框架开关或 communicator 结构；#14296 中两个同时关闭的开关不能当成单变量证据 |
| 故障注入 | 仅在一次性隔离作业设计“某 rank 不进入/次序改变/进程退出”等注入；不提供生产可复制命令，不做交换机、共享网卡或整机破坏性注入 |
| 资源范围 | 明确占用的 NPU、HBM、CPU、主机内存、端口、HCCS/RoCE 带宽、日志空间和最长运行时间；HCCL Test 的适用设备/版本另核 |
| 停止判据 | 首个不可恢复 NPU/runtime 错误、链路持续异常、超出时间/温度/功耗/日志预算、影响隔离边界或无法保持 rank 身份时立即停止 |
| 恢复判据 | 测试进程和 communicator 已清理；调度隔离解除前完成设备/链路被动健康检查；端口、临时配置和日志归档恢复；未通过则不回生产 |
| 成功判据 | 对照重复改变预先定义的进度差异或 timeout 结果，并能以 rank 时间线解释；只出现一次 `PASS`、只延长 timeout 或只看到“未复现”均不够 |

本批不执行该实验，也不登记实验结果。

## T04：NVIDIA NCCL 超时

### 官方证据与版本边界

#### NCCL 2.27.5

复用 `src.nvidia.nccl-user-guide-2.27.5`，正文引用精确子页：

- [Environment Variables](https://docs.nvidia.com/deeplearning/nccl/archives/nccl_2275/user-guide/docs/env.html)：`NCCL_DEBUG`、`NCCL_DEBUG_FILE`、`NCCL_DEBUG_SUBSYS` 用于日志范围；`NCCL_SOCKET_IFNAME` 会绕过自动接口选择；`NCCL_SOCKET_RETRY_CNT`/`NCCL_SOCKET_RETRY_SLEEP_MSEC` 自 2.24 起；`NCCL_IB_TIMEOUT` 是 InfiniBand verbs timeout，不能当成 PyTorch collective watchdog timeout。文档还警告调试变量若长期保留，可能导致次优行为、故障或 hang。
- [Troubleshooting](https://docs.nvidia.com/deeplearning/nccl/archives/nccl_2275/user-guide/docs/troubleshooting.html)：先保留 NCCL 返回码和 `NCCL_DEBUG=WARN` 证据；容器/虚拟机中的 `/sys`、共享内存、接口和拓扑是环境支路。它们不是看到 watchdog timeout 后的默认根因。
- [RAS](https://docs.nvidia.com/deeplearning/nccl/archives/nccl_2275/user-guide/docs/troubleshooting/ras.html)：RAS 自 NCCL 2.24 起，可以在运行中查询 job/process/communicator。`MISMATCH` 表示 collective op count 不一致；如果重复查询时差异继续变化，可能只是暂时负载不均，只有长期不变才推动“stuck”假设。`INCOMPLETE`/missing process 也需要结合进程和 communicator 身份解释。

RAS 页给出的精确查询程序是 `ncclras`，并列出 `-h`、`-p`、`-v`、`-t` 选项和默认本地端口 28028。正式 procedure 只有在目标 NCCL ≥2.24、组件实际包含该程序、端口/权限经过授权时才能引用；不把它写成对 NCCL 2.23 或未知版本通用的命令。

#### PyTorch 2.8 ProcessGroupNCCL

[PyTorch 2.8 ProcessGroupNCCL Environment Variables](https://docs.pytorch.org/docs/2.8/torch_nccl_environment_variables.html)可支撑框架层观察：

- `TORCH_NCCL_DUMP_ON_TIMEOUT` 需要 `TORCH_NCCL_TRACE_BUFFER_SIZE > 0`；
- `TORCH_NCCL_DESYNC_DEBUG` 用于帮助识别 collective desync 的 culprit rank；
- `TORCH_NCCL_ENABLE_TIMING`、`TORCH_NCCL_TRACE_CPP_STACK` 和 dump 文件配置控制补充证据；
- `TORCH_NCCL_ENABLE_MONITORING` 与 heartbeat timeout 用于在 watchdog 无进展时终止进程，属于作业存活/清理行为，不是根因诊断结论；
- `TORCH_NCCL_ASYNC_ERROR_HANDLING` 不同值的清理行为不同，不能在未核对默认值和目标版本时擅改。

该页是 PyTorch 2.8，页面标注创建/更新于 2025-06-10。它不适用于 #118369 的 PyTorch 2.1.2，也不能直接套入 E02 的 PyTorch 2.6.0a0/NCCL 2.25.1 文档基线。正式 procedure 应把“当前环境能否使用某变量”列为版本核对项。

### T04-P procedure 的证据顺序

#### 1. 固定环境与 communicator 身份

记录 PyTorch、NCCL、CUDA runtime、driver、GPU/NIC、单机/多机、容器、网络 transport/interface、rank 到 GPU/节点映射和 process group/communicator。`SeqNum` 只在同一 process group 语境比较；不同 group 的相同数字没有可比性。

#### 2. 先读 watchdog 行，再回看更早证据

从每个 rank 提取 `SeqNum`、`OpType`、输入/输出元素数、configured timeout、实际等待时间，以及 last enqueued/completed work（若版本输出）。随后回看：

- 哪个 rank 没有同一 sequence/op；
- 哪个 rank 已进入不同 collective 或不同数据/控制分支；
- timeout 前是否已有 CUDA kernel、OOM、process exit、device Xid、transport、socket/IB、link 或 topology 错误；
- watchdog/monitor 终止是首因还是故障后的清理动作。

#### 3. 候选支路

| 候选支路 | 支持证据 | 不足以支持 |
| --- | --- | --- |
| 缺 rank/错序 | 同 group 的 sequence/op 不一致，或某 rank 没有进入目标 collective；RAS mismatch 长期不变 | 只看到多数 rank 的相同 timeout，缺失 rank 日志尚未取得 |
| 上游计算/数据分支 | 某 rank 停在数据加载、checkpoint、CPU/GPU kernel、异常分支或已退出 | rank 利用率低本身；仍需栈或事件时间线 |
| NCCL/网络 transport | timeout 前有明确 NCCL WARN、socket/IB 错误、link 事件；受控基线随路径改变 | 只有 `NCCL_IB_TIMEOUT` 或接口配置，没有故障事件 |
| GPU/driver | timeout 前有 Xid、CUDA error、设备丢失并对应 rank/GPU | watchdog 为保护数据一致性终止进程，这是后果而非设备故障证明 |
| 正常操作超时 | 所有 rank 序列一致并持续进展，正常耗时可重复超过框架 timeout | 仅把 timeout 调大后没有立即报错 |

#### 4. 调试设置护栏

- 调试输出要按 host/PID/rank 使用唯一文件，避免 `NCCL_DEBUG_FILE` 覆盖。
- 明确日志磁盘预算、保留期和敏感内容；TRACE/大 ring buffer 只在短期、隔离或容量受控时使用。
- `NCCL_SOCKET_IFNAME`、socket retry、IB timeout 等会改变运行行为。没有证据时不以“调试”为名同时改多项网络变量。
- 一旦进程状态、设备错误或数据一致性不再可信，停止复现并保留现场。

### T04-C 真实案例：PyTorch #118369

来源：[pytorch/pytorch #118369](https://github.com/pytorch/pytorch/issues/118369)，2024-01-26 打开；2026-05-05 由 stale 流程关闭为 `not planned`。

**环境。** 报告者在 AWS P4 实例上用 DeepSpeed 对 Llama2-7B 做 supervised fine tuning；给出 Linux 5.15 AWS x86_64、Python 3.10.12、PyTorch 2.1.2+cu121、Transformers 4.35.2、Accelerate 0.26.1。后续 `nvidia-smi` 快照显示 8×NVIDIA A100-SXM4-40GB、driver 535.104.12 和页面显示的 CUDA 12.2。该快照是报告者运行时观察，不应反推完整 AWS 实例、NIC 或 NCCL 版本。

**时间线与 rank 进度。** 2024-01-25 17:50 左右，rank 1–7 均报告 `WorkNCCL(SeqNum=880, OpType=BROADCAST, NumelIn=131137536, NumelOut=131137536, Timeout(ms)=1800000)`，实际约 1800.6–1800.9 秒；随后 ProcessGroupNCCL 为避免异步 CUDA 数据不一致而终止进程，17:51 左右 launcher 依次 kill 8 个子进程。原始 excerpt 没有 rank 0 的相同 timeout 行。

**关键评论。** 维护者/贡献者在[首条分析评论](https://github.com/pytorch/pytorch/issues/118369#issuecomment-1915684994)中说明 broadcast 需要所有 rank 参与，并把“rank 0 没有打印 timeout、可能没有加入该 broadcast”作为调查方向，而不是确认结论。报告者随后给出[GPU 利用率快照](https://github.com/pytorch/pytorch/issues/118369#issuecomment-1915819487)：GPU 0 为 0%，GPU 1–7 为 100%。这与 rank 0 分叉假设相容，但利用率不是进程控制流证据。

2024-03-01 的[进一步评论](https://github.com/pytorch/pytorch/issues/118369#issuecomment-1973742710)把候选分成两类：所有 rank 正确调用而 network/NCCL 层没有完成，或一个/多个 rank 没有在正确时间调用正确 collective；评论认为后者更可能，需要对 DeepSpeed 的 collective 顺序做 instrumentation。它还提到当时 Flight Recorder 尚未普遍可用，不能把这段 2024 评论当成今天的版本说明。

**状态与结论。** 页面没有关联修复 PR 或根因验证。2026-05-05 的[关闭评论](https://github.com/pytorch/pytorch/issues/118369#issuecomment-4383979717)明确写为 stale 自动关闭、如仍活跃可 reopen。因此案例结论只能是“rank 0 未进入同一 broadcast 是有日志和利用率支持的首选假设，根因未解决”；不能写成 NCCL 网络故障、DeepSpeed bug 或 PyTorch 修复。

### T04-X 实验设计

| 项目 | 设计要求 |
| --- | --- |
| 隔离 | 专用 GPU/NIC/节点或调度器独占分区；不与生产 communicator、端口和日志目录共享；先取得主动测试授权 |
| 版本固定 | 记录 driver/CUDA/NCCL/PyTorch、容器 digest、GPU/NIC/交换路径、接口选择和 nccl-tests commit；只启用目标版本存在的观测功能 |
| 被动阶段 | 先用框架已有 watchdog 日志；适用时再开启唯一 debug file、受限 trace buffer、desync debug 或 NCCL RAS，观察 sequence/op/rank，而不改变 transport |
| 基线阶段 | 复用 `src.nvidia.nccl-tests-b4d5beeb` 的固定 commit 作为测试程序源码身份；固定 collective、消息大小、rank 映射、warmup/iteration、校验和接口，建立正常完成时间与带宽分布 |
| 对照阶段 | 一次只改变 communicator/collective 次序、rank 行为或 transport 路径中的一个变量；不同 process group 单独编号 |
| 故障注入 | 缺 rank、错序或进程终止仅在一次性隔离作业内设计，确保 launcher 能回收全部进程；不向生产交换机、共享 IB/RoCE fabric 或设备注入故障 |
| 资源预算 | 明确 GPU/HBM、CPU/内存、PCIe/NVLink、NIC/fabric 带宽、端口、日志容量和运行时间；高 debug 级别可能显著增加日志与时延 |
| 停止判据 | 首个 Xid/CUDA fatal、持续 link/transport 错误、数据校验失败、影响共享网络、超出时长/温度/功耗/日志预算或 rank 回收失败即停止 |
| 恢复判据 | 全部进程/communicator/RAS listener 已退出，调试变量和接口覆盖已撤销，设备/链路被动健康及一次无注入基线恢复，之后才解除隔离 |
| 成功判据 | 预期的 rank/sequence 分叉与 timeout 能在对照中稳定出现/消失，且无注入基线恢复；单次吞吐、单次无超时或提高 timeout 不构成验证 |

本批不执行 `nccl-tests`、RAS 查询或任何故障注入，也不登记实验结果。

## 命令与变量收录边界

- HCCL 用户指南的日志搜索和 `HCCL_EXEC_TIMEOUT` 示例只作为来源证据描述，不在 T03-P 提供一键命令。实际日志根路径、引号/工具、产品版本和权限必须由目标环境确认。
- 可在 T04-P 精确列出 NCCL 2.27.5 文档中的变量名和 RAS 程序/选项，但必须带版本、行为改变和授权边界；不提供组合式“万能调试环境变量”。
- PyTorch 2.8 的 `TORCH_NCCL_*` 变量只对版本确认后的目标环境收录。#118369 的 PyTorch 2.1.2 案例不得补写当时不存在或未启用的变量。
- Issue 中的启动、清理、服务和模型命令不进入正式 procedure。它们包含环境特定路径、资源配置和可能的副作用，不是厂商通用处方。

## 未知与待办

- 取得 #14296 报告者的 AI_CPU 缓解反馈和自动跟进；未独立核实 CANN 9.0.1 的相应手册条件、根因与真实修复提交/版本。
- HCCL 8.1.RC1.alpha001 PDF 与 #14296 的 CANN 9.0.1 不是同版；procedure 只能使用通用证据顺序，不能用 8.1 的参数范围替代 9.0.1 核验。
- #IBS5FF 的外链大日志、`DONE` 关闭理由及修复信息未取得；不把外链日志纳入来源或复述为已验证事实。
- #118369 未报告 NCCL 精确版本、NIC/fabric、网络拓扑、DeepSpeed 版本或 rank 0 的进程栈；根因保持未知。
- NCCL 2.27.5 RAS 输出和 PyTorch 2.8 flight recorder 字段没有在本地运行验证；只能按文档版本描述。
- 两个实验均未执行。正式 X 条目继续保持 `draft`、`verification.status: not-verified`，不写伪造结果。

## 六篇正文的来源映射

| 条目 | 主来源 | 补充来源 | 不得越界 |
| --- | --- | --- | --- |
| T03-P | CANN 8.1.RC1.alpha001 HCCL User Guide §9.1.2 | F07/F08/F18；固定 HCCL commit | 不给统一 timeout，不把错误码等同根因 |
| T03-C | vLLM Ascend #14296 | #IBS5FF 仅作对比 | Closed 不等于修复；workaround 冲突保留 |
| T03-X | 固定 HCCL commit；官方 timeout 分支 | F07/F08/F18 | 只写隔离设计，不声称执行 |
| T04-P | NCCL 2.27.5 env/troubleshooting/RAS | PyTorch 2.8 ProcessGroupNCCL；F07/F08/F18 | 每个命令/变量带版本，不将 IB timeout 当 watchdog timeout |
| T04-C | PyTorch #118369 及三个关键评论 | 固定 NCCL 概念页 | rank 0 为候选首因，不是已证实根因；stale 关闭不等于修复 |
| T04-X | NCCL 2.27.5 RAS；固定 nccl-tests commit | PyTorch 2.8 观测字段；F08 | 主动测试/注入隔离，恢复后才解封，不写结果 |

## 可复用的现有登记

- `src.huawei.hccl-api-cann-8.0-rc1-alpha003`
- `src.ascend.cann-hccl-2d685b08`
- `src.nvidia.nccl-user-guide-2.27.5`
- `src.nvidia.nccl-tests-b4d5beeb`
- `src.pytorch.distributed-2.8`

其中 `src.pytorch.distributed-2.8` 的登记 URL 是 distributed 总页；为了让 `TORCH_NCCL_*` 变量有精确支持页，下面另提 ProcessGroupNCCL 2.8 子页来源，而不是把总页当作已核对每个变量。

## 待合并来源 YAML

下面是符合 `schemas/sources.schema.json` 的完整独立 YAML。正式合并前应检查 ID 是否已由其他批次登记；本文件不修改 `sources/registry.yaml`。

```yaml
schema_version: 1
sources:
  - id: src.huawei.hccl-user-guide-cann-8.1-rc1-alpha001
    title: CANN 社区版 8.1.RC1.alpha001 集合通信用户指南 01
    url: https://www.hiascend.com/doc_center/source/zh/CANNCommunityEdition/81RC1alpha001/devguide/hccl/hcclug/CANN%E7%A4%BE%E5%8C%BA%E7%89%88%208.1.RC1.alpha001%20%E9%9B%86%E5%90%88%E9%80%9A%E4%BF%A1%E7%94%A8%E6%88%B7%E6%8C%87%E5%8D%97%2001.pdf
    kind: documentation
    registered_at: '2026-09-30'
    revision: CANN Community 8.1.RC1.alpha001; document 01; 2025-03-19
    license:
      status: unknown
      scopes: []
      notes: 厂商 PDF 的版权与再分发范围未核验；公开可读不等于允许全文再分发，本库只链接并作原创归纳，CANN/HCCL 软件包许可另计。
    notes: T03-P/X 的版本化官方来源；重点使用印刷第 83–84 页（零基索引 88–89）9.1.2 的 EI0002、rank 进度、早期错误、设备和网络分支。未执行文档命令，不与 CANN 8.0 API 或 9.0.1 案例拼成支持矩阵。
  - id: src.vllm-ascend.issue-14296
    title: "vLLM Ascend #14296：DCP/MoE AIV 启动期 HCCL timeout 报告"
    url: https://github.com/vllm-project/vllm-ascend/issues/14296
    kind: issue
    registered_at: '2026-09-30'
    revision: opened 2026-08-14; completed close 2026-09-22; three comments read 2026-09-30; no verified fix chain
    license:
      status: unknown
      scopes: []
      notes: Issue 页面、评论、附件和日志的再分发范围未核验；仓库源码许可证不自动覆盖用户提交内容。本库只链接并作有限事实归纳。
    notes: T03-C 来源；正文与三条评论记录 AIV group 证据、报告者抢核初判及 AI_CPU 缓解反馈、自动跟进和含糊 PR 提及；completed 关闭不证明修复。两个框架开关表述冲突仍保留，CANN 对应官方限制与质量/性能结果未独立验证。
  - id: src.ascend-pytorch.issue-ibs5ff
    title: "Ascend PyTorch #IBS5FF：单机八卡 AllReduce notify timeout 报告"
    url: https://gitee.com/ascend/pytorch/issues/IBS5FF
    kind: issue
    registered_at: '2026-09-30'
    revision: opened 2025-03-10; observed status DONE 2026-09-30; no linked pull request or branch visible
    license:
      status: unknown
      scopes: []
      notes: Gitee Issue、附件和外链日志的许可及持久性未核验；仓库源码许可证不自动覆盖用户提交内容。本库不复制外链大日志。
    notes: T03-C 次选/对照；提供 CANN 8.0.RC3、torch_npu 2.4.0.post2、8x910B2 和多 rank 时间线，但 DONE 原因、维护者分析和修复未知，不作为已解决案例。
  - id: src.pytorch.processgroupnccl-env-2.8
    title: PyTorch 2.8 ProcessGroupNCCL Environment Variables
    url: https://docs.pytorch.org/docs/2.8/torch_nccl_environment_variables.html
    kind: documentation
    registered_at: '2026-09-30'
    revision: PyTorch 2.8 documentation; page created/updated 2025-06-10
    license:
      status: partial
      scopes:
        - scope: PyTorch v2.8.0 仓库自有文档源码；网站部署、商标和第三方内容另计
          identifier: BSD-3-Clause
          url: https://github.com/pytorch/pytorch/blob/v2.8.0/LICENSE
      notes: PyTorch 仓库许可证可覆盖其自有文档源码；不据此扩张到 NCCL、CUDA、网站基础设施或第三方内容。
    notes: T04-P/X 的框架层观测来源；用于 dump-on-timeout、trace buffer、desync debug、timing 和 monitoring 的版本化语义。不能倒推到 PyTorch 2.1.2 案例或未经核对的其他版本。
  - id: src.pytorch.issue-118369
    title: "PyTorch #118369：Rank 0 缺席的 NCCL Broadcast watchdog timeout"
    url: https://github.com/pytorch/pytorch/issues/118369
    kind: issue
    registered_at: '2026-09-30'
    revision: opened 2024-01-26; automatically closed as stale/not planned 2026-05-05; no fix linked
    license:
      status: unknown
      scopes: []
      notes: Issue、评论和日志的再分发范围未核验；PyTorch 仓库 BSD-3-Clause 不自动覆盖用户提交内容。本库只链接并作有限事实归纳。
    notes: T04-C 主案例；rank 1-7 在 SeqNum 880 Broadcast 超时、rank 0 缺少同类行且利用率快照为 0%，支持进度分叉假设。维护者未确认根因；stale 关闭不是修复。
```

## 审阅后的评论补读

静态页面漏载评论；GitHub 连接器补得 3 条。报告者 MarinaMiao 的 [5300280446](https://github.com/vllm-project/vllm-ascend/issues/14296#issuecomment-5300280446)（2026-08-15 03:19:11 UTC）补充 MoE/AllGather 抢核初判、AI_CPU 缓解及可能性能代价；其援引的 latest HCCL 手册尚未独立读取，不当作 9.0.1 保证。[5313215244](https://github.com/vllm-project/vllm-ascend/issues/14296#issuecomment-5313215244)（8 月 17 日）自标 Automated Response，不是独立验证。[5770710734](https://github.com/vllm-project/vllm-ascend/issues/14296#issuecomment-5770710734)与 completed 关闭均为 9 月 22 日 03:17:18 UTC；含糊 PR 编号未定位真实补丁。正文/registry 已同步，保留两个框架开关对照冲突。
