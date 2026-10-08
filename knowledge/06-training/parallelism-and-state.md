---
id: training.parallelism-and-state
title: 并行策略与训练状态
type: concept
domain: training
status: draft
platforms: [generic]
source_refs:
  - src.pytorch.parallel-training-state-2.6
  - src.pytorch.dcp-2.6
  - src.ascend.mindspeed-llm-ha-v2.2.0
  - src.ascend.mindspeed-llm-checkpoint-v2.2.0
updated_at: "2026-09-30"
summary: 说明数据、状态分片、张量和流水线并行如何改变训练状态的所有者、布局、通信与恢复责任。
related_ids:
  - communication.collectives-and-rank-progress
  - data-storage.checkpoint-durability
  - training.checkpoint-state-consistency
verification:
  status: source_checked
  evidence_refs:
    - src.pytorch.parallel-training-state-2.6
    - src.pytorch.dcp-2.6
    - src.ascend.mindspeed-llm-ha-v2.2.0
    - src.ascend.mindspeed-llm-checkpoint-v2.2.0
  notes: 核对 PyTorch 2.6 版本化文档、MindSpeed-LLM v2.2.0 固定文档与 checkpoint wrapper；未运行训练、保存、加载或 GPU/NPU 实验。
---

# 并行策略与训练状态

训练状态不只是模型权重。一个可解释的训练恢复点还可能包含 optimizer、scheduler、loss scaler、随机数生成器、数据进度、逻辑步和并行映射。并行策略会改变这些状态是复制、分片、按 stage 所有，还是只在一个计算窗口内短暂存在；因此 `world_size` 和一组 tensor 字节不足以描述训练状态。

本页讨论状态的所有者、布局和 checkpoint 表示。collective 匹配与 rank 进展见[集合通信语义、rank 进展与超时](../03-communication/collectives-and-rank-progress.md)，文件写入、提交和持久化见 [Checkpoint 写入与持久化边界](../04-data-storage/checkpoint-durability.md)，装载后是否能正确继续训练见 [Checkpoint 恢复一致性](checkpoint-state-consistency.md)。

## 并行改变了什么

下表以 PyTorch 2.6 的 DDP、FSDP、Tensor Parallel 和 Pipeline Parallel 为版本化样板。它用于解释关系，不表示其他框架采用相同格式或提供相同恢复能力。

| 策略 | 状态布局与所有者 | 主要通信或执行关系 | 对 checkpoint 的影响 |
|---|---|---|---|
| DDP 式数据并行 | 每个 rank 有完整模型副本；普通 optimizer state 通常也随副本本地持有；每个 rank 消费不同数据子集 | backward 同步梯度；参数由各进程的 optimizer 以相同方式更新；buffer 可按配置广播 | 权重和 optimizer 可能可去重，数据进度与 RNG 却可能是 rank-local；不能因模型有副本就只保留一个 rank 的全部应用状态 |
| FSDP/ZeRO 式状态分片 | 以 FSDP `FULL_SHARD` 为例，参数、梯度和 optimizer state 均被分片；完整参数只在计算窗口内聚合 | forward/backward 前 all-gather 参数，backward 后 reduce-scatter 梯度 | 单个 local shard 不是完整模型；需要声明 full、sharded 或 local 表示，以及目标布局如何重建 |
| Tensor Parallel | 单层参数和中间 tensor 按 row、column、sequence 等规则分片；布局依赖 module FQN、mesh 和 plan | 层内 collective 或 layout redistribution 连接各分片计算 | 参数身份必须与 mesh、placement 和 parallel plan 关联；只记录 global rank 不能解释 shard |
| Pipeline Parallel | 各 stage 拥有不同模块，micro-batch 由 schedule 在 stage 间推进 | stage 间传输 activation 和 gradient；schedule 决定飞行中的 micro-batch | 普通 step 边界可避免保存飞行状态；若要 mid-step 恢复，还要覆盖梯度累积、schedule 与在途状态 |
| 组合并行 | 同一进程可同时属于 DP、TP、PP、expert/context 等多个通信域 | 多个 group 的 collective 与点对点操作按各自次序叠加 | 需要记录每个并行维度、成员顺序、stage/shard 分配和状态格式；单一 `world_size` 不能描述布局 |

PyTorch 2.6 的 DDP 文档明确把输入切分留给应用，并说明参数不会在每次迭代中广播；DDP 依靠梯度同步后各 optimizer 以相同方式更新副本（[DistributedDataParallel](https://docs.pytorch.org/docs/2.6/generated/torch.nn.parallel.DistributedDataParallel.html)）。因此“权重副本相同”不能推出 sampler 位置、RNG 或任意应用计数也相同。

FSDP `FULL_SHARD` 的参数、梯度和 optimizer state 分片及其 all-gather/reduce-scatter 关系由 [PyTorch 2.6 FSDP 文档](https://docs.pytorch.org/docs/2.6/fsdp.html)定义。Tensor Parallel 则用 DTensor 和 1-D `DeviceMesh` 表达 row/column/sequence 等布局，并按 module FQN 应用 plan（[Tensor Parallelism](https://docs.pytorch.org/docs/2.6/distributed.tensor.parallel.html)）。Pipeline Parallel 同时切分权重和执行，以 micro-batch、stage 通信和 schedule 组织计算；PyTorch 2.6 将该包标为 alpha（[Pipeline Parallelism](https://docs.pytorch.org/docs/2.6/distributed.pipelining.html)）。这些资料没有提供跨框架通用的 shard 或 stage checkpoint 格式。

## 状态责任矩阵

训练系统应为每类状态指定逻辑所有者、物理持有者、保存表示和恢复规则。“逻辑全局”不表示只有一个物理副本；“每 rank 持有”也不表示每份都能互换。

| 状态 | 并行下的典型变化 | checkpoint 责任 |
|---|---|---|
| 模型参数与持久 buffer | DDP 复制，FSDP/TP 分片，PP 按 stage 分配；buffer 的同步规则可不同 | 保存稳定参数身份、shape、dtype、布局和模型结构版本；用对应并行 API 生成可加载表示 |
| 梯度与累积槽 | 可能经 all-reduce/reduce-scatter，也可能只存在于本 rank；micro-step 内仍可能是暂态 | 在完整 optimizer step 后保存时，可把“无待提交梯度”列为前提；若支持 mid-step 恢复，需显式保存梯度、累积计数与未决更新 |
| optimizer state 与 param groups | DDP 可复制；FSDP、ZeRO 或 distributed optimizer 可分片 | 保存 state、param groups、参数身份映射和分片格式；不要把普通 parameter ID 当作跨布局稳定键 |
| scheduler | 通常是逻辑全局进度，但实例可能在各 rank 复制 | 单独保存其 `state_dict` 和装载顺序；当前 LR 或 global step 未必能重建全部内部状态 |
| GradScaler/loss scale | 副本通常需要逻辑一致，overflow 决议可能涉及归约 | 保存 scale、growth tracker 和策略字段；PyTorch 2.6 的实现建议在 `update()` 后截取状态 |
| RNG | Python、NumPy、PyTorch CPU、设备 generator、模型并行 tracker 和 worker 可能彼此独立 | 明确保存哪些 generator，并记录其与 rank、设备和并行域的映射；单一 seed 不等于同一随机序列位置 |
| 数据进度 | DP rank 数和 sampler epoch 会改变样本分区；worker 预取使“已读取”与“已训练”不同 | 记录数据修订、epoch、已提交样本/批次、sampler/loader 可恢复状态，以及允许重放或去重的规则 |
| global step、micro-step、样本/token 数 | gradient accumulation、DP size 和 batch 语义会改变这些计数的对应关系 | 分开记录 optimizer step、micro-step、samples/tokens consumed 和最近完整提交点；不能只保存一个 `step` 整数 |
| 并行映射 | 决定参数、optimizer shard、stage、RNG 和数据分区由谁持有 | 保存 TP/PP/DP/EP/CP 维度、mesh/group 成员顺序、stage/layer 分配和格式版本 |
| 模型、代码与数据身份 | 不因并行而消失，却决定序列化字段如何解释 | 记录模型结构、配置、tokenizer/数据修订和必要代码版本；同名 key 或相同步数不证明语义一致 |

PyTorch optimizer 的普通 `state_dict` 以 parameter ID 保存 state，并在 `param_groups` 中保存参数列表和超参数；加载时按列表关系匹配，没有额外的参数身份验证（[Optimizer.state_dict](https://docs.pytorch.org/docs/2.6/generated/torch.optim.Optimizer.state_dict.html)）。`LRScheduler` 有自己的 `state_dict`（[LRScheduler](https://docs.pytorch.org/docs/2.6/generated/torch.optim.lr_scheduler.LRScheduler.html)）。固定 PyTorch v2.6.0 的 [`GradScaler.state_dict` 与 `update`](https://github.com/pytorch/pytorch/blob/1eba9b3aa3c43f86f4a2c807ac8e12c4a7767340/torch/amp/grad_scaler.py)还说明 loss scale 的当前值和 growth tracker 是独立状态。把这三类状态折叠为“optimizer 已保存”会遗漏恢复语义。

随机性也不是一个字段。PyTorch 提供 CPU 默认 generator 的取回和设置接口，而可复现性说明同时列出 Python、NumPy 和库内独立 generator 等来源（[`torch.random`](https://docs.pytorch.org/docs/2.6/random.html)、[Reproducibility](https://docs.pytorch.org/docs/2.6/notes/randomness.html)）。`DistributedSampler` 还要求每个 epoch 在创建迭代器前调用 `set_epoch()` 以改变排序（[数据加载文档](https://docs.pytorch.org/docs/2.6/data.html#torch.utils.data.distributed.DistributedSampler)）。这些资料不保证任意 DataLoader worker 预取位置可由 seed 和 epoch 精确恢复。

## 状态身份需要超过 global rank

rank 是某个通信域中的编号，不是长期稳定的状态身份。组合并行中，一个进程同时拥有 global rank、各 group 内 rank、设备映射、mesh coordinate 和 pipeline stage。重启或改变 world size 后，这些编号可能重新分配，而逻辑参数、stage 或数据分区仍需找到对应状态。

可供恢复协议使用的身份至少包括：

- canonical parameter FQN、模型结构版本和 tensor 的 shape/dtype；
- 旧、目标 DP/TP/PP/EP/CP 维度与有序 group/mesh 描述；
- shard offset/placement，或框架支持的等价布局描述；
- pipeline stage 与 layer/module 的映射；
- RNG、optimizer shard 和数据分区所绑定的逻辑域；
- checkpoint 格式、框架版本和必要转换器版本。

PyTorch 2.6 的 distributed state-dict API 用 canonical FQN 统一若干并行表示，并声明模型和 optimizer state 可面向不同 trainer 数或并行方式重分片（[DCP `get_state_dict`](https://docs.pytorch.org/docs/2.6/distributed.checkpoint.html)）。这个接口范围不能推广为任意应用状态或第三方 shard 自动可转换；目标对象初始化、支持的 tensor 类型和格式条件仍需在恢复侧满足。

## 截取边界决定暂态是否属于 checkpoint

恢复点若定义在完整 optimizer step 之后，可以把无飞行 micro-batch、无待提交梯度累积、scaler 已完成 `update()`、scheduler 和数据提交计数已推进到同一逻辑点作为截取条件。这样不必声称“所有 checkpoint 都必须保存梯度”。

若要求从 step 中间精确恢复，则需要另行覆盖梯度、micro-step、未完成的 overflow 决议、pipeline schedule、在途 activation/gradient、数据预取和异步状态更新。所选资料没有给出跨 DDP/FSDP/TP/PP 的通用 mid-step checkpoint 协议，因此这项能力应在具体实现资料和实验出现前保持 `unknown`。

## MindSpeed-LLM v2.2.0 样板

固定 MindSpeed-LLM v2.2.0 的[高可用性文档](https://github.com/Ascend/MindSpeed-LLM/blob/53f3639c3da9c000a187c44cc0c08d55026ddded/docs/pytorch/features/high_availability.md)说明 distributed optimizer state 分布在 DP 组内，replica optimizer 还会把 DP 组划成副本组。其弹性训练只按 DP 粒度缩扩，并列出 DP size、MoE、长序列、并行组合、配置和缩扩次数限制。这是一个“并行布局直接限制恢复能力”的具体例子，不是任意 world size 恢复的承诺。

同一 commit 的 [`save_checkpoint_wrapper`](https://github.com/Ascend/MindSpeed-LLM/blob/53f3639c3da9c000a187c44cc0c08d55026ddded/mindspeed_llm/training/checkpointing.py)把 model、optimizer、scheduler、RNG 和 iteration 交给外部 Megatron 的 `generate_state_dict`，并补充累计 FLOP；legacy distributed optimizer 与 distributed checkpoint 走不同分支，异步保存只允许 distributed `torch_dist` 格式。同步分支在 barrier 后更新 latest iteration tracker，异步分支把更新注册为 finalize callback。

这段 wrapper 只能支持“调用者传递了哪些对象”和“哪些分支在何时更新 tracker”。`generate_state_dict` 的完整字段、加载顺序、格式兼容和重分片语义属于没有在该文件中固定的外部依赖，保持 `unknown`。该 tag 的 README 指向 PyTorch 2.7.1，并把多个 NPU 组件标为“在研版本”，所以不能与本页 PyTorch 2.6 样板拼成已支持软件组合。

## 常见误解

- **“所有 rank 的权重相同，所以只保存一个 rank 的状态即可。”** DDP 权重副本不覆盖 rank-local RNG、数据进度或应用状态；分片并行下单 rank 权重本身也不完整。
- **“保存了 global step 就保存了训练进度。”** step 与 micro-step、样本数、token 数、scheduler、scaler 和 sampler 位置不是同一状态。
- **“分片只是存储优化，不改变恢复协议。”** shard placement、参数身份和目标布局决定字节由谁读入以及如何组合。
- **“world size 描述了整个并行布局。”** 相同 world size 可以对应不同 DP/TP/PP/EP/CP 分解、group 顺序和 stage 分配。
- **“同 seed 就能续接随机轨迹。”** 多类 generator、rank 映射和随机调用顺序都可能变化。

## 适用边界与待确认问题

本文的共用模型是“内容、身份、布局、逻辑时间”四部分，`generic` 不表示任何 GPU/NPU 组合已经兼容。PyTorch 结论固定在 2.6 文档和 v2.6.0 源码；MindSpeed 结论固定在 v2.2.0 commit。未安装或运行 PyTorch、MindSpeed、MindIO、TorchNPU、Megatron，也未核验 CANN、驱动、固件和硬件配套。

待确认：目标训练框架实际生成的状态 schema，optimizer 与参数稳定身份的映射，设备与模型并行 RNG tracker，DataLoader 的可恢复边界，PP mid-step 状态，目标 NPU 组合的完整加载和重分片能力，以及各状态在失败时允许的重放范围。来源核查和许可证范围见[第四批研究记录](../../docs/research/batch-04-training-sources.md)。
