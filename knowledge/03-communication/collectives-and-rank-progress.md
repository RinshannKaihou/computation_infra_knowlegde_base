---
id: communication.collectives-and-rank-progress
title: 集合通信与 rank 进度
type: concept
domain: communication
status: draft
platforms: [generic]
source_refs:
  - src.nvidia.nccl-user-guide-2.27.5
  - src.pytorch.distributed-2.8
  - src.huawei.hccl-api-cann-8.0-rc1-alpha003
updated_at: "2026-09-29"
summary: 从通信域、调用契约和多 rank 时间线理解集合通信进度，区分主机返回、设备完成、对端进度与超时症状。
related_ids:
  - communication.bandwidth-baselines
  - reliability.evidence-and-hypotheses
  - hardware.resource-topology
  - software-stack.layers-and-boundaries
verification:
  status: source_checked
  evidence_refs:
    - src.nvidia.nccl-user-guide-2.27.5
    - src.pytorch.distributed-2.8
    - src.huawei.hccl-api-cann-8.0-rc1-alpha003
  notes: 已核对 NCCL 2.27.5、PyTorch 2.8 和 CANN 8.0.RC1.alpha003 HCCL 接口参考中的指定页面；未在 GPU、NPU 或集群上执行通信、故障注入或超时复现。
---

# 集合通信与 rank 进度

集合通信不是“每个进程各自调用一次同名函数”这么简单。一次集合操作由一个确定的参与者集合共同形成：各 rank 必须在同一个通信域里，以彼此兼容的次序和参数进入对应操作。任一 rank 尚未到达、进入了另一项操作、提交了不兼容的参数，或在更早的计算与设备任务中失败，其余 rank 都可能停在看起来正常的通信调用上。

本文回答三个问题：哪些条件使各 rank 的调用能够互相匹配；“调用返回”“设备完成”和“对端继续前进”为何不是同一个时刻；为什么通信超时只描述观察到的等待结果，不能单独证明网络故障。

## 三个基本对象

| 对象 | 含义 | 容易混淆的边界 |
|---|---|---|
| communicator / process group / 通信域 | 一组参与者、组内 rank 编号以及后端通信状态的上下文。PyTorch `ProcessGroup` 是框架抽象；NCCL communicator 和 HCCL 通信域是具体后端对象 | 名称相同、成员数量相同，不足以证明两个进程持有的是同一实例或同一成员顺序 |
| rank | 进程或设备在**某个组内**的逻辑编号。编号只在对应通信域中解释 | global/world rank、group rank、local rank 和物理 GPU/NPU 编号不是同一标识。PyTorch 2.8 将 rank 定义为进程组内连续编号；HCCL 文档还区分 world、group 与 local rank（[PyTorch rank](https://docs.pytorch.org/docs/2.8/distributed.html#torch.distributed.get_rank)，[HCCL 相关概念](https://www.hiascend.com/doc_center/source/zh/CANNCommunityEdition/80RC1alpha003/apiref/hcclapiref/CANN%208.0.RC1.alpha003%20%E9%9B%86%E5%90%88%E9%80%9A%E4%BF%A1%E6%8E%A5%E5%8F%A3%E5%8F%82%E8%80%83%2001.pdf#page=10)） |
| collective instance | 通信域中某一逻辑位置上的一次集体操作，例如第 37 次 all-reduce | “第 37 次”是帮助对齐证据的概念，不保证每个后端日志都暴露相同的 sequence number，也不能跨通信域直接比较 |

通信域决定“谁应当参加”和“rank 编号怎样解释”；集合操作决定这些参与者在本次交换中扮演什么角色。NCCL 2.27.5 要求 communicator 中的每个 CUDA 设备获得唯一的 `0..n-1` rank，并把 communicator 对象固定关联到 rank 与设备（[Creating a Communicator](https://docs.nvidia.com/deeplearning/nccl/archives/nccl_2275/user-guide/docs/usage/communicators.html)）。HCCL 8.0.RC1.alpha003 则把默认 world group 与其子集自定义 group 分开，并说明自定义组中的 rank 会从 0 重新编号。两者都说明：排障记录必须同时保存组身份、组内 rank 与设备映射，不能只写“rank 3”。

## 一次集合操作的匹配契约

可以把一次集合操作的逻辑身份写成：

```text
(通信域实例, 该域内的相对次序, 操作类型, 操作参数契约)
```

它不是任何库承诺的线协议字段，而是一种核对模型。四部分中任一项在参与者间不一致，都可能让不同 rank 以为自己正在参加不同的操作。

| 契约维度 | 需要一致或相容的内容 | 说明 |
|---|---|---|
| 参与者 | 通信域成员、成员顺序、rank 到进程/设备的映射 | 默认 world group 与子组不能混用；root 是组内 rank 时也不能当作物理设备号。NCCL 文档特别说明 broadcast/reduce 的 root 是 rank，不是 device number（[Collective Operations](https://docs.nvidia.com/deeplearning/nccl/archives/nccl_2275/user-guide/docs/usage/collectives.html)） |
| 次序 | 同一通信域内各参与者进入可匹配的 collective；多通信域并发还要满足后端的全局次序约束 | PyTorch 2.8 要求进程组按相同次序创建；对多个 NCCL process group，还要求各 rank 的 collective 执行次序全局一致，并要求多线程调用显式同步（[Groups](https://docs.pytorch.org/docs/2.8/distributed.html#groups)） |
| 操作语义 | collective 类型、root、reduction op、split/count 向量等 API 特有参数 | rank 0 调 all-reduce、rank 1 调 broadcast，即使 buffer 字节数相同也不是一次匹配操作 |
| buffer 契约 | count、dtype、shape/size、输入输出布局和设备位置，按具体 API 检查 | 不能把“所有 collective 的 shape 必须相同”当成统一规则；有的 API 明确允许不等长输入，另一些要求同 count 或同 size |

原生 NCCL 2.27.5 明确要求每个 rank 用相同 count 和 datatype 调用 collective，否则行为未定义，可能挂起、崩溃或数据损坏（[Collective Operations](https://docs.nvidia.com/deeplearning/nccl/archives/nccl_2275/user-guide/docs/usage/collectives.html)）。这里的契约是元素数与数据类型，不是 Python 张量 shape。框架会再叠加自己的约束：PyTorch 2.8 的 `broadcast` 要求参与进程的 tensor 元素数相同，`all_gather_into_tensor` 要求各 rank 输入 tensor 大小相同（[Collective functions](https://docs.pytorch.org/docs/2.8/distributed.html#collective-functions)）。

HCCL 8.0.RC1.alpha003 也按具体原语定义一致性：`HcclAllReduce` 要求所有 rank 的 `count`、`dataType`、`op` 相同；`HcclBroadcast` 还要求 `root` 相同且全局只有一个 root（[HcclAllReduce，3.3.1](https://www.hiascend.com/doc_center/source/zh/CANNCommunityEdition/80RC1alpha003/apiref/hcclapiref/CANN%208.0.RC1.alpha003%20%E9%9B%86%E5%90%88%E9%80%9A%E4%BF%A1%E6%8E%A5%E5%8F%A3%E5%8F%82%E8%80%83%2001.pdf#page=47)、[HcclBroadcast，3.3.2](https://www.hiascend.com/doc_center/source/zh/CANNCommunityEdition/80RC1alpha003/apiref/hcclapiref/CANN%208.0.RC1.alpha003%20%E9%9B%86%E5%90%88%E9%80%9A%E4%BF%A1%E6%8E%A5%E5%8F%A3%E5%8F%82%E8%80%83%2001.pdf#page=48)）。因此应记录应用看到的 shape、后端接收的 count/dtype 和变长操作的分段参数；只比较一个字段不足以证明调用匹配。

## 四种“进度”不能互相代替

同一句“这个 rank 已完成通信”常把不同层次混在一起。至少要区分以下观察：

| 进度层次 | 能说明什么 | 不能说明什么 |
|---|---|---|
| 主机进入调用 | 进程执行到了框架或通信库入口 | 参数已通过检查、任务已提交到设备、其他 rank 已到达 |
| 主机提交/返回 | 本地主机调用满足了该 API 的返回条件 | 设备数据传输已经完成、输出可被任意 stream/线程使用、对端主机也已返回 |
| 本地设备完成 | 本 rank 的相关设备依赖和数据操作达到完成条件 | 对端应用已经执行到下一步；其他通信域没有未完成工作 |
| 对端/全组进度 | 其他参与者到达了匹配位置或完成了其本地工作 | 所有 rank 的主机、设备和后续应用状态处于同一行代码 |

NCCL 2.27.5 的普通 stream 调用说明区分成功入队与设备异步完成（[CUDA Stream Semantics](https://docs.nvidia.com/deeplearning/nccl/archives/nccl_2275/user-guide/docs/usage/streams.html)），但必须同时识别调用模式：`ncclGroupStart/End` 内的单次 collective 可以在尚未入队时返回；若 communicator 采用 nonblocking 模式，`ncclGroupEnd()` 返回 `ncclInProgress` 时还可能在后台提交，要等相应状态成为 `ncclSuccess` 才能认定该提交阶段成功。即便成功提交，仍需按 CUDA stream/event 语义判断设备完成。这里的 API 聚合组不是 process group 或 communicator（[Group Calls 的 Caution 与 Nonblocking Group Operation](https://docs.nvidia.com/deeplearning/nccl/archives/nccl_2275/user-guide/docs/usage/groups.html)）。

对 PyTorch 2.8 的 NCCL 后端，普通非 barrier Work 在未启用 `TORCH_NCCL_BLOCKING_WAIT`、未传入有效的显式 timeout 时，`wait()` 主要建立当前 CUDA stream 对 NCCL 完成事件的依赖，并不等待 CPU 观测到设备完成。启用 blocking-wait 或设置显式 timeout 会进入 CPU 等待路径；barrier 也有专门的 CPU 同步分支。等待过程中仍可能发现异常，不能把返回和成功混为一谈（[Work.wait API](https://docs.pytorch.org/docs/2.8/distributed.html#torch.distributed.Work.wait)，[v2.8.0 固定实现的 synchronizeStream/wait](https://github.com/pytorch/pytorch/blob/ba56102387ef21a3b04b357e5b183d48f0afefc7/torch/csrc/distributed/c10d/ProcessGroupNCCL.cpp#L775-L839)）。

`is_completed()` 也不能单独充当成功标志。通用文档概览用入队/stream 可用性描述 CUDA 异步操作，但这个固定 `WorkNCCL::isCompleted()` 实现返回“存在异常，或 GPU 结束事件已完成”；因此 `True` 既不能简单等同刚入队，也不能排除错误。记录时应保留具体 backend、版本、错误状态及后续使用所在 stream 的依赖（[固定 isCompleted 实现](https://github.com/pytorch/pytorch/blob/ba56102387ef21a3b04b357e5b183d48f0afefc7/torch/csrc/distributed/c10d/ProcessGroupNCCL.cpp#L580-L585)，[结束事件查询](https://github.com/pytorch/pytorch/blob/ba56102387ef21a3b04b357e5b183d48f0afefc7/torch/csrc/distributed/c10d/ProcessGroupNCCL.cpp#L649-L661)）。上述实现边界不能移植到 HCCL/NPU。

选定的 HCCL 文档给出了另一套机制边界：HCCL 在执行阶段编排 Notify、SDMA 等任务，由 runtime 下发到昇腾设备任务调度器；Notify wait 会阻塞设备任务流，直到对端的 Notify record 到达（[HCCL 执行流程](https://www.hiascend.com/doc_center/source/zh/CANNCommunityEdition/80RC1alpha003/apiref/hcclapiref/CANN%208.0.RC1.alpha003%20%E9%9B%86%E5%90%88%E9%80%9A%E4%BF%A1%E6%8E%A5%E5%8F%A3%E5%8F%82%E8%80%83%2001.pdf#page=8)）。该文档中的 C++ collective 接口接收 `aclrtStream`，示例在通信调用后另行同步 stream；但它没有为本文所覆盖的每个 collective 精确定义“主机函数返回”与“任务已入队/设备已完成”的统一边界。因此这项边界在本页记为 `unknown`，不能用 NCCL 的 CUDA stream 结论补齐，也不能据此推荐 CUDA/NCCL 环境变量。

## 多 rank 时间线：超时常发生在异常之后

下面是一个概念时间线。它不模拟任何具体后端线程或网络协议，只展示“最先出错的 rank”与“最先报告通信超时的 rank”可能不同。

```mermaid
sequenceDiagram
    participant R0 as rank 0
    participant R1 as rank 1
    participant R2 as rank 2
    Note over R0,R2: 同一通信域，预期 collective C17
    R0->>R0: C17 主机调用返回或进入等待
    R1->>R1: 更早的计算/设备任务异常
    Note right of R1: 没有进入 C17
    R2->>R2: C17 主机调用返回或进入等待
    Note over R0,R2: 设备或进度线程等待缺失参与者
    R0-->>R0: 超时被观测并上报
    R2-->>R2: 稍后上报超时
```

这里 R0 最先打印 timeout，不表示 R0 是故障源；R1 的更早异常才解释了它为什么没有参加 C17。另一类常见分叉是调用次序不一致：部分 rank 在某通信域的第 *k* 个位置调用 all-reduce，另一些 rank 在同一位置调用 broadcast，双方都可能等待“尚未到达”的对端。还有一种情况是所有主机都已提交，某个设备任务因设备错误、stream 依赖或链路问题无法推进，其他 rank 随后一起超时。

HCCL 8.0.RC1.alpha003 文档明确指出，单卡问题和通信链路问题都可能让集群出现大量超时，因此需要收集全组日志来锁定问题位置（[HCCL 异常流程](https://www.hiascend.com/doc_center/source/zh/CANNCommunityEdition/80RC1alpha003/apiref/hcclapiref/CANN%208.0.RC1.alpha003%20%E9%9B%86%E5%90%88%E9%80%9A%E4%BF%A1%E6%8E%A5%E5%8F%A3%E5%8F%82%E8%80%83%2001.pdf#page=9)）。NCCL 2.27.5 的错误说明也分别列出外部 CUDA 调用错误、系统调用错误、无效参数/用法和异步通信错误；其中网络错误只是异步错误的一类（[Error handling](https://docs.nvidia.com/deeplearning/nccl/archives/nccl_2275/user-guide/docs/usage/communicators.html#error-handling-and-communicator-abort)）。

所以 timeout 的可靠含义只是：某个观察者等待的条件在给定时限内没有满足。它提供时间和受影响通信域，却不自动给出根因层。候选解释至少包括：参与者缺失、分支或次序分叉、参数契约不匹配、进程退出、较早的计算/设备异常、设备任务停滞、主机调度长停顿，以及节点内或节点间通信路径故障。

## 用一条可对齐的时间线描述进展

要判断“谁先停下”，来自每个 rank 的记录需要能对齐到同一对象，而不仅是收集更多日志文本。适合长期保存的最小字段包括：

| 字段组 | 建议保留的内容 | 用途 |
|---|---|---|
| 运行身份 | job/run、重启代次、进程 PID、节点、设备稳定标识 | 防止把重启前后或不同作业的同名 rank 混在一起 |
| rank 身份 | world/global rank、group 标识、group rank、local rank、group 成员有序列表 | 判断参与者与编号映射是否一致 |
| 操作身份 | 每通信域 sequence/trace 标识（若实现提供）、collective 类型、root/op、shape、count、dtype、split 信息 | 判断各 rank 是否在谈同一次操作；没有公共 sequence 时只能用邻近事件谨慎重建 |
| 进度事件 | 主机入口、主机返回、设备提交、设备完成、wait/同步入口与返回、超时/错误 | 区分卡在主机、设备依赖还是对端进度 |
| 时间基础 | 原始时间戳、时钟来源、采集端与已知偏差 | 跨节点墙钟未校准时，不能仅按字符串时间决定全局先后 |
| 前序异常 | 同一进程和设备在目标 collective 之前的首个异常、退出或资源事件 | 避免从最后一批连锁 timeout 倒推根因 |

“最早异常”也必须限定证据范围：它是当前已收集记录中最早的异常事件，不自动等于物理根因。若某节点日志缺失、时钟偏移未知或设备异步错误晚于实际故障上报，时间线只能给出下一项待核对关系。

## 平台与版本边界

| 主题 | NCCL 2.27.5 / PyTorch 2.8 样板 | HCCL 8.0.RC1.alpha003 样板 |
|---|---|---|
| 通信上下文 | PyTorch ProcessGroup 映射到 NCCL communicator；多 process group 的并发次序有明确警告 | world/custom group 与 HCCL 通信域；group rank 可相对 world rank 重排 |
| 设备执行 | NCCL 与 CUDA stream 关联；组内调用可能尚未入队，nonblocking group 还需确认提交成功；设备执行和提交分开观察 | 文档描述 runtime 下发 Notify/SDMA 等设备任务，Notify wait/record 协调设备流 |
| 参数契约例子 | NCCL collective 同 count、同 datatype；PyTorch 再定义 tensor size/stream 可见性 | 各 HCCL 原语分别定义 count、datatype、op、root 等一致性 |
| 主机返回边界 | 按 NCCL 普通/聚合组/nonblocking 模式及 PyTorch Work 的 timeout、blocking-wait、barrier 分支分别解释；完成标志还需检查错误 | 所选 HCCL 文档没有给出覆盖所有 collective 的统一精确定义，记为 `unknown` |
| 超时解释 | CUDA、系统、API 使用、进程/节点/网络等都可能妨碍进展 | 正式文档明确列出单卡与链路问题都可能造成集群大量超时 |

这三份版本化资料是用于理解边界的样板，不构成 PyTorch 2.8 与 NCCL 2.27.5 的配套声明，也不构成任何 TorchNPU、CANN、HCCL、固件和 NPU 型号组合的支持声明。NCCL 2.26 起的多 communicator 隐式 launch ordering 还需要特定配置且仍要求各设备上的主机发起次序匹配；不能把该特性概括成“多通信域无需排序”（[NCCL multiple communicators](https://docs.nvidia.com/deeplearning/nccl/archives/nccl_2275/user-guide/docs/usage/communicators.html#using-multiple-nccl-communicators-concurrently)）。

## 来源与待确认问题

- [NCCL 2.27.5 User Guide](https://docs.nvidia.com/deeplearning/nccl/archives/nccl_2275/user-guide/docs/)：通信域、collective 参数、CUDA stream 与多 communicator 次序。
- [PyTorch 2.8 `torch.distributed`](https://docs.pytorch.org/docs/2.8/distributed.html)：process group/rank、组创建顺序、collective 参数与同步/异步语义。
- [CANN 8.0.RC1.alpha003《集合通信接口参考》文档版本 01](https://www.hiascend.com/doc_center/source/zh/CANNCommunityEdition/80RC1alpha003/apiref/hcclapiref/CANN%208.0.RC1.alpha003%20%E9%9B%86%E5%90%88%E9%80%9A%E4%BF%A1%E6%8E%A5%E5%8F%A3%E5%8F%82%E8%80%83%2001.pdf)：HCCL 概念、执行流程、参数约束与异常说明。来源核对范围见[研究记录](../../docs/research/batch-03-f07-sources.md)。
- 待确认：目标环境真实的 group 创建与销毁次序、框架到后端的 sequence 映射、时钟误差、设备与 rank 映射、NPU collective 的主机返回边界，以及平台版本支持关系。


性能测量口径见[通信带宽与性能基线口径](bandwidth-baselines.md)，证据组织方法见[诊断中的证据、假设与结论](../08-reliability/evidence-and-hypotheses.md)。
