---
id: data-storage.checkpoint-durability
title: Checkpoint 写入与持久化边界
type: concept
domain: data-storage
status: draft
platforms: [generic]
source_refs:
  - src.pytorch.dcp-2.6
  - src.linux-man-pages.fsync-6.19
  - src.ascend.mindio-acp-v26.1.1
updated_at: "2026-09-30"
summary: 区分状态截取、暂存、写入、提交和持久化证据，说明文件可见、保存接口返回与可恢复检查点之间的差别。
related_ids:
  - training.checkpoint-state-consistency
  - data-storage.training-data-path
  - hardware.resource-topology
verification:
  status: source_checked
  evidence_refs:
    - src.pytorch.dcp-2.6
    - src.linux-man-pages.fsync-6.19
    - src.ascend.mindio-acp-v26.1.1
  notes: 核对 PyTorch 2.6 DCP 文档和固定源码、Linux fsync 手册与固定 MindIO ACP README；未执行保存、故障注入或恢复实验。
---

# Checkpoint 写入与持久化边界

“checkpoint 保存成功”需要说明成功发生在哪一层。调用返回、训练状态已复制到主机内存、文件已生成、后台写入完成、数据达到持久化条件、训练能够从该点正确继续，是不同的判断。本页解释其中的存储边界；权重、优化器、随机状态与数据进度是否构成一致的训练恢复点，属于训练状态问题。

## 从状态截取到恢复候选

下面是本库用于组织证据的逻辑图，不是每个框架都有同名阶段，也不要求它们严格串行。

```mermaid
flowchart LR
    A[确定状态截取边界] --> B[生成不受后续训练修改的保存视图]
    B --> C[序列化与分片写入]
    C --> D[收集写入结果与元数据]
    D --> E[按实现协议提交或发布]
    E --> F[供恢复端选择的候选检查点]
    C -. 独立核对存储确认语义 .-> P[持久化条件与覆盖故障域]
    E -. 核对命名与提交记录的持久性 .-> P
    F --> V[读取、完整性与训练恢复验证]
```

不同实现可能先将数据暂存在内存，再向后端异步写入；也可能让写入调用等待后端确认。必须找到实际 API、配置和完成信号的定义，不能仅依据 `save`、`async`、`flush` 等名字判断。

| 观察点 | 可以支持什么 | 尚不能支持什么 |
|---|---|---|
| 状态已截取或暂存完成 | 保存视图已经建立；其是否独立于后续修改需由实现说明 | 全部 rank 的状态在同一个逻辑步；内容已到持久存储 |
| 某个写入调用返回 | 该接口约定范围内已接受或完成请求 | 所有分片完成；缓存已经持久化；整个检查点已发布 |
| 文件或对象能列出 | 名称当前可见 | 字节完整、分片齐全、属于同一次保存、断电后仍存在 |
| 后台任务成功完成 | 对应 Future、任务或存储请求所定义的工作完成 | 其覆盖之外的副本、目录记录、故障域或训练状态一致性 |
| 提交记录或 manifest 存在 | 实现协议认为检查点可被发现或读取 | 不能脱离协议认定所有引用对象都持久、安全或语义正确 |
| 读回与校验一致 | 在该时点、读路径和参考摘要下字节一致 | 保存的就是正确训练状态；其他客户端或故障后也可读 |
| 恢复后可继续训练 | 该环境与负载下完成一定范围的恢复验证 | 任意并行配置、框架版本和故障条件均可恢复 |

这是一张证据分类表，不要求所有存储都提供 manifest，也不把单个文件系统的语义强加给对象存储或分布式服务。

## PyTorch DCP：异步完成与写入者职责

PyTorch 2.6 的 DCP `async_save` 先暂存状态，再在独立线程执行保存，返回持有保存结果的 Future；暂存协议要求得到不受后续训练修改影响的视图。DCP 的存储接口把各 rank 的 `write_data` 与协调者的 `finish` 分开，后者写元数据并标记保存成功。因此，取得 Future、某个 rank 写完、整个保存任务完成应分别记录（[DCP 2.6：async_save、AsyncStager 与 StorageWriter](https://docs.pytorch.org/docs/2.6/distributed.checkpoint.html)）。这里没有把该接口自动认定为 TorchNPU/CANN 组合已支持。

固定 PyTorch v2.6.0 commit 的 `FileSystemWriter` 提供更具体的实现证据：

- `sync_files` 默认为 `True`，源码明确提醒关闭后不保证故障情况下检查点一致性（[参数与限制](https://github.com/pytorch/pytorch/blob/1eba9b3aa3c43f86f4a2c807ac8e12c4a7767340/torch/distributed/checkpoint/filesystem.py#L444-L466)）。
- 数据写入路径在该选项开启时请求 `fsync`（[写入实现](https://github.com/pytorch/pytorch/blob/1eba9b3aa3c43f86f4a2c807ac8e12c4a7767340/torch/distributed/checkpoint/filesystem.py#L326-L336)）。
- `finish` 写临时元数据、按选项请求同步，再将其改名为目标元数据文件（[提交实现](https://github.com/pytorch/pytorch/blob/1eba9b3aa3c43f86f4a2c807ac8e12c4a7767340/torch/distributed/checkpoint/filesystem.py#L574-L595)）。

这些事实说明需要核对具体 writer 和配置。它们没有给任意后端、存储控制器或故障场景提供端到端保证；也不能用“临时文件改名”几个字概括整个多文件检查点的事务语义。

## 文件同步与目录记录是两个层面

Linux `fsync(2)` 手册说明，它同步文件数据及相关元数据，并等待设备报告完成；但这不必然使包含该文件的目录项也到达磁盘，目录有自己的同步要求。同步也可能返回 I/O、空间或配额错误，不能把“发起了同步”记为“同步成功”（[Linux man-pages 6.19，fsync 的 DESCRIPTION 与 ERRORS](https://man7.org/linux/man-pages/man2/fsync.2.html)）。

据此，检查点方案需要分别说明文件内容、命名/目录或对象索引、提交标记以及副本状态的确认语义。上述手册描述 Linux 接口，不能据此推断某个网络文件系统、对象服务或自定义 writer 的全部持久性。后端服务的确认条件、挂载方式、缓存与故障模型仍需对应资料和验证。

## 昇腾相关实现例子：MindIO ACP

MindCluster v26.1.1 固定 commit 的 [MindIO ACP README](https://github.com/Ascend/mind-cluster/blob/44385c13d7b1d87def35f1604e8be4d16de6ca4e/component/mindio/acp/README.md)说明：检查点先写入训练服务器的内存系统，再异步写入后端可靠性存储。这直接支持将“内存暂存”和“后端持久化”拆成两项状态。

该 README 本身没有给出本页所需的全部确认接口、内存副本故障域、提交协议或用户任务配套。因此本页不推断暂存阶段能够抵抗整节点掉电、不填写内存副本数量，也不把模型保存调用返回当成后端持久化证据。MindIO ACP 的具体 API、版本配套和失败回退需要另行核对；它也不与已有 TorchNPU 历史档案自动构成已支持组合。

GPU/NPU 的设备到主机暂存方法可能不同。本文共用存储证据问题，设备内存拷贝、流同步、dtype/layout 和框架后端的实现分别查证。

## 应保留的检查点记录

| 记录组 | 建议字段 | 要避免的歧义 |
|---|---|---|
| 身份 | 作业、保存尝试 ID、逻辑步、框架/writer 版本、目标路径或对象前缀 | 重试和多次保存不能混用同一身份却未记录覆盖关系 |
| 内容清单 | 应有与实际分片、大小、格式、元数据版本、摘要算法与可信参考 | 文件数相同不证明内容相同；摘要一致也不证明状态语义正确 |
| 阶段时间 | 截取开始/结束、暂存完成、写入完成、提交/持久化确认 | 异步保存的主线程停顿与后台端到端完成延迟分开 |
| 配置 | 同步选项、后台并发、缓存、存储服务确认策略 | 不能只写“默认配置”，也不假设配置名跨版本含义一致 |
| 故障范围 | 进程退出、节点不可达、存储客户端/服务故障等目标条件 | 一次进程重启通过不能证明节点掉电或存储故障下安全 |
| 消费结果 | 恢复端选择了哪个保存 ID、读回/校验结果、缺失分片和拒绝原因 | 最近创建的目录不一定是最近完整的恢复点 |

建议每次保存使用能区分尝试的身份，并明确不完整产物如何被发现、拒绝和处理。这是本库的设计建议，不是所有框架现有的自动功能。保留已确认可用恢复点的策略应结合实际保留周期、空间与覆盖协议设计。

## 持久化与恢复成功需要分别验证

面向存储的验证应检查：预期分片及元数据是否齐全、错误能否传播到保存任务、读取端是否拒绝不完整产物、目标故障后是否仍能发现并读取已确认的点。实验必须先限定隔离环境与故障范围；本页没有执行这些实验。

之后还需要训练侧验证：保存时是否覆盖所需状态、各 rank 是否对应同一逻辑进度、恢复后的优化器/随机状态/数据游标是否符合应用约定，以及能否持续推进。仅从文件完整性不能完成这些判断。

待补证据：目标存储与 writer、实际配置和确认协议、MindIO ACP 完成信号与副本策略、GPU/NPU 暂存行为、故障后的读回证据。来源获取范围见[本批研究记录](../../docs/research/batch-03-f10-sources.md)。

训练侧的状态覆盖、重分片与恢复后对照见[Checkpoint 恢复一致性](../06-training/checkpoint-state-consistency.md)。
