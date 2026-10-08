# 第四批 F13/F14 训练状态与恢复来源准备

交付日期：2026-09-30。来源页面读取、tag 解析和固定文件核对完成于 2026-09-29；本文记录 F13/F14 的来源核查、可支持结论、写作边界和候选来源登记，不代表任何 GPU/NPU、存储或恢复实验已经完成。

## 任务边界

以 `plans/content-backlog.yaml` 为准：

| 任务 | 标题 | 稳定 ID | 目标路径 | 本轮准备范围 |
|---|---|---|---|---|
| F13 | 并行策略与训练状态 | `training.parallelism-and-state` | `knowledge/06-training/parallelism-and-state.md` | 解释 DP、参数/梯度/优化器分片、TP、PP 如何改变状态布局、rank 责任、通信和 checkpoint 表示 |
| F14 | Checkpoint 恢复一致性 | `training.checkpoint-state-consistency` | `knowledge/06-training/checkpoint-state-consistency.md` | 区分 API 保存/加载完成与训练语义恢复，整理状态覆盖、重分片条件、恢复后对照和容差 |

F13/F14 的主归属是训练。文件写入、后台任务、提交标记和持久化故障域由 [F10](../../knowledge/04-data-storage/checkpoint-durability.md) 负责；通信域、rank、collective 次序和设备完成边界由 [F07](../../knowledge/03-communication/collectives-and-rank-progress.md) 负责。本批不在训练文章中重复讲存储协议或把通信超时直接归因于网络。

## 选定资料与固定版本

### PyTorch 2.6

PyTorch 文档统一固定到 `2.6` URL；需要源码定位时使用 PyTorch `v2.6.0` commit `1eba9b3aa3c43f86f4a2c807ac8e12c4a7767340`。本次实际打开并读取了以下精确页面：

| 页面 | 实际核对内容 | 不支持的外推 |
|---|---|---|
| [DistributedDataParallel](https://docs.pytorch.org/docs/2.6/generated/torch.nn.parallel.DistributedDataParallel.html) | DDP 同步各模型副本的梯度；不替用户切分输入；参数不在迭代中广播，优化器应在各进程以相同方式更新参数；buffer 默认从 rank 0 广播 | DDP 自动保存数据游标；所有 rank 的任意应用状态天然一致；NPU 后端具有相同实现细节 |
| [FSDP](https://docs.pytorch.org/docs/2.6/fsdp.html) | `FULL_SHARD` 分片参数、梯度和优化器状态；参数在计算前 all-gather，梯度在反向后 reduce-scatter；full/sharded optimizer state 的转换与不同 world size 示例 | 任意本地 shard 文件都能独立恢复；任意并行策略或框架版本都可自动重分片 |
| [Tensor Parallelism](https://docs.pytorch.org/docs/2.6/distributed.tensor.parallel.html) | TP 基于 DTensor；用户按模块 FQN 和 1-D `DeviceMesh` 指定 row/column/sequence 等布局；输入输出可能需要布局变换 | TP 计划可从 tensor 内容自动推断；任意 N-D mesh、PP 或第三方实现具有同一格式；实验性 API 是稳定兼容承诺 |
| [Pipeline Parallelism](https://docs.pytorch.org/docs/2.6/distributed.pipelining.html) | PP 同时切分模型权重与执行，运行时处理 micro-batch 切分、调度、通信和梯度传播；该包处于 alpha | 普通 step checkpoint 会保存飞行中的 micro-batch、activation 或 schedule 状态；其他 PP 实现格式等价 |
| [Distributed Checkpoint](https://docs.pytorch.org/docs/2.6/distributed.checkpoint.html) | DCP 保存调用者提供的 `state_dict`；对 ShardedTensor/DTensor 按本地 shard 读写；加载前目标张量必须在目标设备分配；`get_state_dict` 用 canonical FQN 统一多种并行表示并声明可按不同 trainer 数/并行方式重分片 | DCP 自动发现 scheduler、GradScaler、RNG、数据游标或业务 step；保存/加载返回即训练正确；跨 PyTorch 版本向后兼容 |
| [Optimizer `state_dict`](https://docs.pytorch.org/docs/2.6/generated/torch.optim.Optimizer.state_dict.html) | optimizer state 按 parameter ID 保存，`param_groups` 还带超参数；普通加载按列表对应关系匹配且没有额外验证 | 仅文件可读就证明 optimizer state 对到了正确参数；修改模型/参数组后可无条件加载 |
| [`LRScheduler`](https://docs.pytorch.org/docs/2.6/generated/torch.optim.lr_scheduler.LRScheduler.html) | scheduler 有独立 `state_dict`；包含 `self.__dict__` 中除 optimizer 外的状态 | optimizer state 自动包含完整 scheduler 进度；只恢复 global step 就等价恢复 scheduler |
| [`GradScaler` 固定源码](https://github.com/pytorch/pytorch/blob/1eba9b3aa3c43f86f4a2c807ac8e12c4a7767340/torch/amp/grad_scaler.py) | `state_dict()` 包含 scale、growth/backoff factor、growth interval 和 growth tracker；建议在 `update()` 后截取 | 任意混合精度实现使用相同字段；恢复 scale 就足以证明数值轨迹一致 |
| [`torch.random`](https://docs.pytorch.org/docs/2.6/random.html) 与 [Reproducibility](https://docs.pytorch.org/docs/2.6/notes/randomness.html) | CPU 默认 generator 有可取回/设置的状态；Python、NumPy 与库内 generator 可能是不同随机源；同 seed 不保证跨 release/platform 完全复现 | 一个全局 seed 覆盖所有 rank、DataLoader worker、第三方库和设备 generator；CPU/GPU/NPU 随机状态格式等价 |
| [`DistributedSampler`](https://docs.pytorch.org/docs/2.6/data.html#torch.utils.data.distributed.DistributedSampler) | sampler 按 replica/rank 选择数据子集；每个 epoch 需在创建迭代器前调用 `set_epoch()` 以改变跨 epoch 排序 | `DataLoader` 自动提供任意时刻的可恢复游标；epoch 数可以唯一确定样本位置 |
| [Elastic train script](https://docs.pytorch.org/docs/2.6/elastic/train_script.html) | worker 失败时会重启所有 worker，应用需要自己的 save/load checkpoint 逻辑；进度最多退回最近 checkpoint | elastic launcher 自动保存训练状态；重启成功代表数值连续或没有重复/遗漏样本 |
| [Numerical accuracy](https://docs.pytorch.org/docs/2.6/notes/numerical_accuracy.html) | 浮点加法/乘法非结合；数学等价计算、不同 release/commit/platform 即使输入相同也不保证 bitwise identical | 恢复对照必须逐字节相同；任意差异都可判为 checkpoint 错误 |
| [`torch.testing.assert_close`](https://docs.pytorch.org/docs/2.6/testing.html#torch.testing.assert_close) | close 的数值条件为 `|actual-expected| <= atol + rtol*|expected|`；dtype/device/layout 等结构检查另行控制 | 文档默认容差天然适合任意模型、loss、梯度或长时间训练；容差无需按比较目标和风险定义 |

上述 PyTorch 页面用于同一 `2.6` 文档快照内的机制解释。它们不构成 PyTorch 2.6 与任何 NCCL、TorchNPU、CANN、MindSpeed 或硬件版本的配套声明。

### MindSpeed-LLM v2.2.0：固定 NPU 实现样板

官方 tag `v2.2.0` 在 2026-09-29 通过远端 tag 查询解析为 commit `53f3639c3da9c000a187c44cc0c08d55026ddded`。本次只读取固定文件，没有安装、导入或运行仓库代码。

| 固定对象 | 核对结果 | 使用边界 |
|---|---|---|
| [README](https://github.com/Ascend/MindSpeed-LLM/blob/53f3639c3da9c000a187c44cc0c08d55026ddded/README.md) | tag 对应 2.2.0；该快照表中 PyTorch 为 2.7.1，TorchNPU/CANN 等写作“在研版本” | 不能与本批 PyTorch 2.6 文档拼成支持组合，也不能据此填写明确 CANN/torch_npu 制品版本 |
| [高可用性文档](https://github.com/Ascend/MindSpeed-LLM/blob/53f3639c3da9c000a187c44cc0c08d55026ddded/docs/pytorch/features/high_availability.md) | 分布式优化器状态在 DP 组分布；副本优化器把 DP 组再分成副本组；弹性训练只按 DP 粒度缩扩，并列出 DP size、MoE、长序列和配置约束 | 这是该固定快照的功能说明，不是所有 MindSpeed/MindIO 版本的保证；外链 wheel、TaskD、MindCluster 与硬件没有在本任务验证 |
| [checkpointing.py](https://github.com/Ascend/MindSpeed-LLM/blob/53f3639c3da9c000a187c44cc0c08d55026ddded/mindspeed_llm/training/checkpointing.py) 中 `save_checkpoint_wrapper` | 调用外部 Megatron 的 `get_rng_state` 与 `generate_state_dict`，把 model、optimizer、scheduler、RNG、iteration 交给生成逻辑，并另加累计 FLOP；legacy 分布式 optimizer 和 distributed checkpoint 走不同分支；异步保存只允许 distributed `torch_dist` 格式 | 关键 `generate_state_dict`、完整 load 逻辑和 Megatron distributed-checkpoint 语义来自外部依赖，不在该文件内；不能仅凭 wrapper 宣布字段格式、加载顺序、重分片或恢复正确性 |
| 同一 `save_checkpoint_wrapper` 的完成分支 | 同步路径在 barrier 后更新 latest iteration tracker；异步路径把 tracker 更新注册为 finalize callback，随后调度后台保存 | “scheduled async save” 日志不等于 finalize 已完成；tracker 语义仍需结合外部 Megatron save request 与实际存储验证，存储边界引用 F10 |
| [确定性计算文档](https://github.com/Ascend/MindSpeed-LLM/blob/53f3639c3da9c000a187c44cc0c08d55026ddded/docs/pytorch/features/deterministic_computation.md) | 文档要求显式参数和环境变量，并提示特定 SuperPod/RoCE 拓扑变化时通信算法行为不同 | 不能把“同参数”省略为只比较权重/seed；不能把此文档扩展为跨拓扑、跨版本或 PyTorch 2.6 的 bitwise 保证 |

高可用文档对弹性恢复给出的固定约束必须近旁保留：

- 为保留完整 optimizer 状态，Data Parallel Size 要大于 1；MoE 和长序列还分别增加稠密/稀疏 DP 与 `dp_cp_size` 条件。
- 弹性训练当前只允许特定高可用与 distributed optimizer 组合，不支持 `use-custom-fsdp` 和 `reuse-fp32-param` 场景。
- 文档只列出 DP、TP、PP 组合；缩容后不能再次缩容，扩容只能回原规模。
- 因此不能把它概括为“任意 world size、任意并行映射可恢复”。

`checkpointing.py` 自身有 Apache-2.0 文件头；高可用 Markdown 没有单独文件头，根 `LICENSE` 明确说“除非另有说明适用于所有文件”，其主条款为 BSD 3-Clause，并继续列出若干第三方文件的其他许可。候选来源登记因此把代码与文档拆开，不用一个许可证覆盖两者。

### 复用第三批来源

- `src.pytorch.dcp-2.6`：继续用于 DCP save/load、canonical FQN、重分片、异步完成和 writer 责任。F13/F14 不再创建重复 DCP 来源。
- `src.ascend.mindio-acp-v26.1.1`：只支持“训练服务器内存暂存后异步写后端存储”的 I/O 边界。它不支持训练状态字段、恢复后的数值一致性或与上述 MindSpeed-LLM v2.2.0 的版本配套。

## F13 可写结论：并行改变的是布局和责任

下表把上游直接支持的事实与本库用于组织内容的工程含义分开。后者是待编辑评审的归纳，不表述为某个框架的统一标准。

| 策略 | 状态与布局 | 主要通信/执行关系 | checkpoint 与恢复要求 |
|---|---|---|---|
| DDP 式数据并行 | 每个 rank 有完整模型副本；梯度被同步；普通 optimizer state 通常跟随每个副本本地持有；各 rank 消费不同数据子集 | backward 触发梯度归约；参数由各 rank optimizer 以相同方式更新；buffer 可按 DDP 配置同步 | 模型/optimizer 可能有重复副本，但数据进度、RNG 和应用计数未因此自动相同；保存者去重不能丢掉 rank-local 必要状态 |
| FSDP/ZeRO 式状态分片 | 以 PyTorch 2.6 `FULL_SHARD` 为例，参数、梯度、optimizer state 均分片；计算窗口内临时聚合参数 | forward/backward 前 all-gather 参数，backward 后 reduce-scatter 梯度；optimizer 更新本地 shard | 恢复端需知道目标模型与 shard 布局；不能把某个 rank 的 local shard 当完整模型。full、sharded、local state dict 的语义和内存/通信成本不同 |
| Tensor Parallel | 单层参数及中间 tensor 按 row/column/sequence 等规则分片，布局依赖 module FQN、mesh 与 plan | 层内 collective 或布局 redistribution 把分片计算连接起来 | parallel plan、mesh 维度、参数 canonical identity 与 shard placement 属于恢复 schema；仅保存 tensor 字节不足以解释分片 |
| Pipeline Parallel | 各 stage 持有不同模块，执行又按 micro-batch 调度；stage/rank 映射决定谁拥有哪些权重 | stage 间 point-to-point activation/gradient 传输，并由 schedule 控制飞行中的 micro-batch | 最稳妥的普通 checkpoint 边界应避开未完成的 optimizer step 和飞行 micro-batch；若要 mid-step 精确恢复，还需额外保存梯度累积、schedule 和在途状态，所选资料没有给出通用实现 |
| 组合并行 | 一个 rank 可能同时处于 DP、TP、PP、context/expert 等多个通信域；同名 rank 需绑定每个域解释 | 多个 group 的 collective 与 point-to-point 次序叠加 | 必须记录每个并行维度、group 成员顺序、rank 到设备/stage/shard 的映射和状态格式；单一 `world_size` 不能完整描述布局 |

### 训练状态责任矩阵

| 状态 | 典型所有者 | 并行影响 | F13/F14 应明确的 checkpoint 责任 |
|---|---|---|---|
| 模型参数与持久 buffer | `nn.Module` / 并行 wrapper | DDP 复制，FSDP/TP/PP 分片或按 stage 划分；buffer 同步规则可能不同 | 记录 canonical 参数身份、shape/dtype、布局和模型结构版本；使用对应并行 API 生成可加载表示 |
| 梯度与累积槽 | autograd、参数 `.grad`、通信 bucket 或框架累积器 | 可能被 all-reduce/reduce-scatter，可能只在本 rank 存在；micro-step 内是暂态 | 若只在 optimizer step 完成后保存，可把“无待提交梯度”作为边界条件；要恢复 step 中间点则需显式纳入梯度与累积计数，不能默认框架已保存 |
| optimizer state 与 param group | optimizer；分片实现可改变实际 holder | DDP 可复制，FSDP/ZeRO/分布式 optimizer 可按 DP 或模型空间分片 | 保存 state、param groups、参数身份映射和分片格式；普通 optimizer parameter ID 没有额外匹配校验，优先使用 canonical FQN 转换或等价的实现协议 |
| LR/参数 scheduler | scheduler / trainer | 通常是逻辑全局状态，但实例可能在各 rank 复制 | 单独保存和恢复其 `state_dict`，记录 load 顺序；不能只用 optimizer 当前 LR 或 global step 猜回完整 scheduler 内部状态 |
| GradScaler / loss-scale 状态 | AMP scaler 或训练框架 | 通常各训练副本需逻辑一致；某些实现会分布归约 overflow 信号 | 保存当前 scale、growth tracker 和相关策略；PyTorch 2.6 建议在 `update()` 后截取，不能在 optimizer step 尚未决议时任意保存 |
| RNG | Python、NumPy、PyTorch CPU、每设备 generator、模型并行 RNG tracker、DataLoader worker 等 | rank、设备、并行组和调用次序会改变随机数消费 | 明确需要恢复哪些 generator 及其与 rank/设备的映射；单一 seed 不等于恢复到同一随机序列位置 |
| 数据进度 | dataset/sampler/DataLoader/trainer | DP rank 数和 sampler epoch 改变样本划分；worker 预取会让“已读”和“已训练”不同 | 记录数据集版本、epoch、已提交样本/批次、sampler/loader 可恢复状态和重放策略；只存 iterator 对象或 global step 通常不足 |
| global step / micro-step / samples consumed | trainer | gradient accumulation、DP size 和 batch 语义会改变 step 与样本数的关系 | 分开记录 optimizer step、micro-step、samples/tokens consumed 和最近完整提交边界；world size 改变时不能只沿用一个整数 |
| 并行映射与配置 | launcher、framework parallel state、模型切分 plan | 决定参数、optimizer shard、stage、RNG 与数据分区落在哪些 rank | 保存足以重建目标布局的 TP/PP/DP/EP/CP 维度、mesh/group 顺序、stage/layer 分配和格式版本；不要用当前环境盲猜旧布局 |
| 数据/模型/代码身份 | 应用与作业编排 | 与并行无关但决定状态是否可解释 | 记录模型结构、tokenizer/数据修订、配置和必要代码版本；同名参数或相同步数不证明语义相同 |

这里的“保存”是训练状态覆盖要求；字节何时落到持久存储仍由 F10 的 writer、提交和故障域证据判断。

## F14 可写结论：API 成功与训练恢复正确是两层判断

### 需要区分的完成点

| 完成点 | 能证明什么 | 仍不能证明什么 |
|---|---|---|
| `save()` 返回或异步 Future/finalize 完成 | 对应 API 与 writer 定义的保存工作完成；具体边界引用 F10 | 应用包含了所有训练状态；各状态来自同一逻辑 step；恢复后轨迹正确 |
| checkpoint 文件/metadata 可读 | 结构可被 reader 解析，目标对象可能可分配和装载 | optimizer 对到正确参数；data/RNG/scheduler 已覆盖；world-size 变化被支持 |
| `load()` 返回 | DCP 已把请求的对象读入调用者提供的目标结构；PyTorch 2.6 的 `load` 返回 `None` | root module 后处理已完成；missing/unexpected key 已按策略处置；训练可继续 |
| `set_state_dict` / 各对象 `load_state_dict` 完成 | 模型/optimizer/scheduler/scaler 等对象接受了相应状态；可检查 missing/unexpected keys | 状态间逻辑时间一致；数据无重复/遗漏；下一步 loss/update 与参考相符 |
| 首个 forward/backward/step 成功 | 基本结构和运行路径没有立即失败 | 长期数值轨迹、学习率、样本序列、吞吐和故障恢复目标达标 |
| 预定义恢复窗口通过 | 在固定环境、输入与 oracle 下满足已定义结构/数值/进展门槛 | 其他版本、拓扑、数据、world size 和故障模式都可恢复 |

### world size 变化与重分片的必要条件

PyTorch 2.6 DCP 文档明确声称支持 load-time resharding，`get_state_dict` 也声明可在不同 trainer 数和/或不同并行方式之间重分片。该能力有具体前提，正文不能简写成“world size 可任意变化”：

1. 保存表示必须是 DCP 和目标 distributed object 支持的表示；普通 rank-local 文件、任意第三方 shard 或应用自定义字节不自动进入 DCP planner。
2. 恢复前先按**目标** world size、模型结构和并行布局初始化对象并分配目标 tensor；DCP 在这些目标 shard 上按需读取。
3. 模型/optimizer identity 需要 canonical FQN 或实现规定的稳定映射；普通 optimizer parameter ID 与列表顺序不能当成跨布局稳定键。
4. shard 的 shape、dtype、offset、mesh/placement、模型结构和 state-dict 格式要受所用 API 支持；`set_state_dict` 对 sharded tensor 要求 ShardedTensor 或 DTensor。
5. `StateDictOptions.broadcast_from_rank0=True` 还要求 `full_state_dict=True`，且 PyTorch 2.6 页面明确只支持 DTensor、不支持 legacy ShardedTensor。默认值不能省略成统一行为。
6. DCP 页面明确不保证 saved state dict 的跨 PyTorch 版本向后兼容。跨版本恢复需要单独迁移或验证证据。
7. scheduler、GradScaler、RNG、data progress、global step 和应用自定义状态并不会因为模型/optimizer tensor 被重分片而自动变换；应用需定义它们在新 DP size、batch 或 accumulation 规则下的语义。
8. PP stage 重新切分、模型结构变化、参数增删/重命名和 optimizer 变更超出“同一状态换 shard 布局”的简单情形，需对应转换器或明确不支持。
9. MindSpeed-LLM v2.2.0 的高可用文档只支持按 DP 粒度的有限缩扩，且有配置和次数限制；不能拿 PyTorch DCP 的声明补齐 MindSpeed/MindIO 的未知能力，也不能反向用该 NPU 限制缩窄所有 DCP 环境。

### 恢复后验证设计

恢复验证应先定义参照和边界，再选择比较方法。建议为未来 F14 或验证实验保留以下层次：

| 层次 | 建议检查 | 比较规则 |
|---|---|---|
| 身份与结构 | checkpoint ID、模型/数据/代码版本、参数 key、shape、dtype、layout、optimizer param group、并行映射 | 离散字段和 key 集合通常要求精确相等；缺失、额外或迁移字段显式列出 |
| 逻辑进度 | optimizer/global step、micro-step、samples/tokens consumed、epoch/sampler progress、scheduler position、scaler growth tracker | 整数与枚举按应用契约精确比较；说明故障后允许重放或跳过多少工作 |
| 状态内容 | 参数、optimizer moment/variance、buffer、scheduler、scaler、RNG | 可精确比较的序列化字段精确比较；浮点 tensor 是否精确或容差比较由环境和目标决定 |
| 同输入单步对照 | 从未中断参考运行和恢复运行取得相同 batch/token IDs，比较 forward 输出、loss、梯度摘要、overflow 决策、LR 与一次参数更新 | 固定模型模式、输入身份/顺序、shape、dtype、layout、并行配置和随机控制；容差在运行前定义 |
| 持续窗口 | 连续若干 step 的输入身份、loss/grad/update 差异、NaN/Inf、collective 进展、吞吐与样本计数 | 窗口长度与允许偏差基于故障目标和模型特性；一次 step 成功不是长期正确性 |
| 终止与回退 | 超出容差、样本身份不一致、状态 key 不匹配、无法解释的 step 跳变或 rank 分叉 | 停止继续训练，保留失败 checkpoint 和对照证据，回退到已确认恢复点 |

“相同输入”至少包括样本或 token 身份、顺序、mask/label、micro-batch 分组及数据增强随机性；仅写“相同数据集”不够。若 world size 或并行切分变化，需要先定义数学上想保持的是相同 global batch、相同样本序列、相同 optimizer step 还是只要求统计等价，这几种目标并不相同。

浮点对照不应无条件要求 bitwise：PyTorch 2.6 明确说明运算顺序、release、commit 与平台会影响结果，即使输入相同也不保证逐位一致。建议写出每个量的 `rtol`、`atol`、dtype、聚合方式、样本数和 NaN/Inf 规则；可采用 `|actual-expected| <= atol + rtol*|expected|` 作为逐元素规则，但阈值必须来自同环境重复运行、模型数值分析或既有验收依据，不能直接把框架默认值当业务门槛。离散状态、样本身份、key/shape 和逻辑计数仍应精确核对。

## 未知与后续写作必须保留的限制

- 没有在本仓库运行 PyTorch DCP、DDP、FSDP、TP、PP、MindSpeed、MindIO、TorchNPU 或 Megatron，也没有 GPU/NPU/集群/存储验证。
- 没有验证 MindSpeed-LLM v2.2.0 的 wheel、外部 Megatron commit、MindIO TTP/TaskD 制品、CANN/torch_npu/驱动/固件组合；README 反而把多个 NPU 组件标为“在研版本”。
- 没有从 `checkpointing.py` 推断外部 `generate_state_dict` 的完整字段、load 顺序、格式兼容或 resharding 保证。正式正文引用该文件时按 `save_checkpoint_wrapper` 和分支条件定位，不估算源码行号。
- 没有来源支持“保存梯度是所有训练 checkpoint 的必选项”。是否需要梯度取决于保存边界；若定义在完整 optimizer step 之后，可以把无飞行 micro-step 作为前提。
- 没有通用资料保证 DataLoader iterator 能在任意 worker 预取状态下精确恢复。数据游标、重放与去重仍是应用设计问题。
- 没有给任何模型填写数值容差、恢复窗口、允许进度损失或性能门槛；这些必须来自目标环境基线与业务恢复目标。
- 没有把 MindSpeed 的“确定性计算”说明外推成跨拓扑 bitwise 保证；固定文档自身提示拓扑变化可能改变通信行为。

## 建议写作结构

### F13：并行策略与训练状态

1. 先定义训练恢复状态，不把 checkpoint 等同于模型权重。
2. 用“复制、分片、按 stage 所有、暂态”四种布局描述 DP/FSDP/TP/PP。
3. 给出状态责任矩阵，重点覆盖参数、梯度、optimizer、scheduler、scaler、RNG、数据进度、global/micro step 和并行映射。
4. 解释 rank 属于多个通信域，状态身份要绑定 group/mesh/stage，而不是只记 global rank。
5. 用 PyTorch 2.6 作为框架样板，用 MindSpeed-LLM v2.2.0 作为独立 NPU 实现样板；明确两者不是支持组合。
6. 结尾列出 checkpoint 需要传给 F14 的 schema 与 unknown。

### F14：Checkpoint 恢复一致性

1. 引用 F10 区分保存/持久化，再定义训练语义一致性。
2. 列状态覆盖与截取边界：同一完整 optimizer step、无未决异步更新/gradient accumulation，或显式保存中间状态。
3. 区分 `save`/`load`/`set_state_dict` 返回、对象装载成功和训练继续正确。
4. 单列 same-world-size 与 changed-world-size；后者写清 DCP、目标对象预分配、canonical FQN、支持的 shard 类型和应用状态转换条件。
5. 给恢复后验证表：结构、逻辑进度、同输入单步、持续窗口、退出/回退。
6. 数值比较说明 bitwise、精确字段和容差字段的边界；不提供无证据阈值。

## 建议新增到 `sources/registry.yaml` 的完整条目

以下四项是**新增候选**，按 `schemas/sources.schema.json` 编写。本子任务不修改共享 registry；主任务合入前需检查 ID 冲突与 YAML 缩进。

```yaml
  - id: src.pytorch.parallel-training-state-2.6
    title: PyTorch 2.6 并行训练与状态文档
    url: https://docs.pytorch.org/docs/2.6/distributed.html
    kind: documentation
    registered_at: "2026-09-30"
    revision: "PyTorch 2.6 documentation; source commit 1eba9b3aa3c43f86f4a2c807ac8e12c4a7767340"
    license:
      status: partial
      scopes:
        - scope: PyTorch v2.6.0 仓库自有代码与随附文档；独立网站资产和第三方材料另计
          identifier: BSD-3-Clause
          url: https://github.com/pytorch/pytorch/blob/1eba9b3aa3c43f86f4a2c807ac8e12c4a7767340/LICENSE
      notes: 版本化页面由 PyTorch 仓库文档生成；本库仅作原创归纳并链接精确页面，不复制示例、图或网站资产。
    notes: 实际核对 DDP、FSDP、tensor parallel、pipeline parallel、optimizer、scheduler、GradScaler、RNG、DataLoader/DistributedSampler 与 elastic train script 页面及固定 GradScaler 源码；用于训练状态布局与责任，不构成与 NCCL、TorchNPU、CANN、MindSpeed 或硬件的配套声明，未运行任何上游代码。
  - id: src.pytorch.numerical-verification-2.6
    title: PyTorch 2.6 数值精度、可复现性与 assert_close 文档
    url: https://docs.pytorch.org/docs/2.6/notes/numerical_accuracy.html
    kind: documentation
    registered_at: "2026-09-30"
    revision: "PyTorch 2.6 documentation; source commit 1eba9b3aa3c43f86f4a2c807ac8e12c4a7767340"
    license:
      status: partial
      scopes:
        - scope: PyTorch v2.6.0 仓库自有代码与随附文档；独立网站资产和第三方材料另计
          identifier: BSD-3-Clause
          url: https://github.com/pytorch/pytorch/blob/1eba9b3aa3c43f86f4a2c807ac8e12c4a7767340/LICENSE
      notes: 本库只链接版本化页面并原创归纳 bitwise、随机性和容差边界，未复制示例或网站资产。
    notes: 实际核对 numerical accuracy、reproducibility 与 torch.testing.assert_close 页面；支持浮点结果不盲目要求 bitwise 和显式记录 rtol/atol 规则，不提供任何模型的验收阈值，也不构成跨平台确定性保证。
  - id: src.ascend.mindspeed-llm-ha-v2.2.0
    title: MindSpeed-LLM v2.2.0 固定高可用性文档
    url: https://github.com/Ascend/MindSpeed-LLM/blob/53f3639c3da9c000a187c44cc0c08d55026ddded/docs/pytorch/features/high_availability.md
    kind: documentation
    registered_at: "2026-09-30"
    revision: "v2.2.0 tag; commit 53f3639c3da9c000a187c44cc0c08d55026ddded"
    license:
      status: identified
      scopes:
        - scope: 固定 commit 的 high_availability.md 文档源码；文件无单独许可头，根 LICENSE 声明除另有说明外适用于所有文件
          identifier: BSD-3-Clause
          url: https://github.com/Ascend/MindSpeed-LLM/blob/53f3639c3da9c000a187c44cc0c08d55026ddded/LICENSE
      notes: 根 LICENSE 还列出若干第三方文件的其他许可；本条仅登记该 Markdown 文本，不覆盖文档引用的图片、外链 MindIO/TaskD 制品或其他第三方材料。本库不复制原图和长段正文。
    notes: 核对 distributed/replica optimizer 的 DP 状态布局、TTP/UCE/弹性功能描述，以及 DP size、MoE、长序列、并行方式和缩扩次数限制；没有安装相关 wheel、运行恢复或核验外链组件配套。该 tag README 指向 PyTorch 2.7.1 且多项 NPU 组件为在研，不能与 PyTorch 2.6 来源拼成支持组合。
  - id: src.ascend.mindspeed-llm-checkpoint-v2.2.0
    title: MindSpeed-LLM v2.2.0 固定 checkpoint wrapper 实现
    url: https://github.com/Ascend/MindSpeed-LLM/blob/53f3639c3da9c000a187c44cc0c08d55026ddded/mindspeed_llm/training/checkpointing.py
    kind: repository
    registered_at: "2026-09-30"
    revision: "v2.2.0 tag; commit 53f3639c3da9c000a187c44cc0c08d55026ddded"
    license:
      status: identified
      scopes:
        - scope: 固定 checkpointing.py 文件；文件头明确声明
          identifier: Apache-2.0
          url: https://github.com/Ascend/MindSpeed-LLM/blob/53f3639c3da9c000a187c44cc0c08d55026ddded/mindspeed_llm/training/checkpointing.py
      notes: 只适用于该文件明确标示的代码；外部 Megatron、ModelOpt、MindIO、TorchNPU、制品与仓库其他文件另行核查。本库仅作原创解释和链接。
    notes: 核对 save_checkpoint_wrapper 对 model/optimizer/scheduler/RNG/iteration/累计 FLOP 的传递、legacy 与 distributed checkpoint 分支、optimizer sharding 选项、异步格式限制及 tracker finalize 位置；generate_state_dict、完整 load 与 dist-checkpoint 语义属于未随本文件固定的外部依赖，未运行代码或硬件。
```

## 复用来源的完整 schema 快照

以下两项已经存在于 `sources/registry.yaml`，**不要重复插入**；这里保留完整条目供 F13/F14 写作审计。

```yaml
  - id: src.pytorch.dcp-2.6
    title: PyTorch 2.6 Distributed Checkpoint 文档与固定 FileSystemWriter 实现
    url: https://docs.pytorch.org/docs/2.6/distributed.checkpoint.html
    kind: documentation
    registered_at: "2026-09-29"
    revision: "2.6 documentation; source commit 1eba9b3aa3c43f86f4a2c807ac8e12c4a7767340"
    license:
      status: partial
      scopes:
        - scope: PyTorch 固定 commit 根代码 LICENSE；生成站点及第三方材料另计
          identifier: BSD-3-Clause
          url: https://github.com/pytorch/pytorch/blob/1eba9b3aa3c43f86f4a2c807ac8e12c4a7767340/LICENSE
      notes: 根许可沿用本库对 PyTorch v2.6.0 的已核对记录；不概括所有文档与发行包。仅原创归纳和链接。
    notes: 核对 async_save、AsyncStager、StorageWriter 和 filesystem.py 的 sync_files、写入、元数据提交；不是目标后端持久性或 TorchNPU 支持声明。
  - id: src.ascend.mindio-acp-v26.1.1
    title: MindIO ACP v26.1.1 固定 README
    url: https://github.com/Ascend/mind-cluster/blob/44385c13d7b1d87def35f1604e8be4d16de6ca4e/component/mindio/acp/README.md
    kind: repository
    registered_at: "2026-09-29"
    revision: 44385c13d7b1d87def35f1604e8be4d16de6ca4e
    license:
      status: partial
      scopes:
        - scope: 固定 MindCluster commit 的根代码许可；组件文档与第三方材料仍需分别核查
          identifier: Apache-2.0
          url: https://github.com/Ascend/mind-cluster/blob/44385c13d7b1d87def35f1604e8be4d16de6ca4e/LICENSE
      notes: 沿用同 commit 已核对的根代码许可；没有把 docs/LICENSE 的范围自动延伸到 component 下 README，也未核验 wheel 和第三方内容。仅原创归纳与链接。
    notes: 只核对 README 的先内存暂存、再异步后端写入关系；未核对接口/副本/回退细节，未安装或运行，不构成与现有 TorchNPU 档案的整栈配套。
```

## 获取与执行记录

- 通过官方远端只读解析 MindSpeed-LLM `v2.2.0` tag，并在 `/private/tmp` 做 shallow checkout；没有修改上游仓库。
- 对固定 MindSpeed 文档、代码和 LICENSE 的 official raw URL 实际取回正文，并与 shallow checkout 文件逐字节比较一致。SHA-256 分别为：高可用文档 `83b6b6d8e3590f0ea158b0d6f40f22606c466dfbf19db6c344246cd55b68ca9f`，`checkpointing.py` `beaa6057ac72f74fbc0fe1e2a82a9f6acc5c34e3591d6f526b6fcce5f4535069`，根 LICENSE `41e59bea3bfd8fd8f236fbda2f86266e9041d6eaa6ef3d7522bd2460f951e093`。
- 实际读取了上述 PyTorch 2.6 版本化页面；为核对生成页面无法完整显示的 GradScaler 状态字段，另取固定 commit 的 `torch/amp/grad_scaler.py`，SHA-256 为 `eb4bc91fda9815ba40206e2dbb68f9845b85622fee3a92611f227b5845b20780`。
- 没有执行上游测试、训练、保存、加载、故障注入或硬件操作；没有安装依赖；没有运行 `make check` 或 `make build`，也没有改动 registry、plan、index、README 与路径页。本记录交付阶段仅新增 backlog 指定的 F13/F14 正文。

## 第四批审阅修订：默认 planner 去重

PyTorch 2.6 DCP 只保存调用者提供的 `state_dict`，不会自动发现 scheduler、GradScaler、RNG、数据游标或业务 step（[Distributed Checkpoint](https://docs.pytorch.org/docs/2.6/distributed.checkpoint.html)）。应用需要显式构建状态清单，并定义这些对象属于哪个逻辑截取点。

固定 v2.6.0 的默认 planner 为各 rank 的普通 tensor/非 tensor 建立写入项，再按相同 `MetadataIndex` 去重、选择写入者；默认按计划存储量选择，不能固定理解为协调 rank。上游局部 docstring 仍称非协调 rank 不保存普通 tensor/非 tensor，与同文件实际循环不一致；这里按固定实现说明（[`default_planner.py` 69–113](https://github.com/pytorch/pytorch/blob/1eba9b3aa3c43f86f4a2c807ac8e12c4a7767340/torch/distributed/checkpoint/default_planner.py#L69-L113)、[390–414](https://github.com/pytorch/pytorch/blob/1eba9b3aa3c43f86f4a2c807ac8e12c4a7767340/torch/distributed/checkpoint/default_planner.py#L390-L414)、[`_dedup_save_plans.py` 15–58](https://github.com/pytorch/pytorch/blob/1eba9b3aa3c43f86f4a2c807ac8e12c4a7767340/torch/distributed/checkpoint/_dedup_save_plans.py#L15-L58)）。

这还意味着“每 rank 都传入同名 RNG/游标 key”不保证保留每份状态：非 tensor index 只使用逻辑 FQN，去重时没有比较各 rank 内容是否一致（[`planner_helpers.py` 116–120](https://github.com/pytorch/pytorch/blob/1eba9b3aa3c43f86f4a2c807ac8e12c4a7767340/torch/distributed/checkpoint/planner_helpers.py#L116-L120)）。rank-local 状态需要不冲突的逻辑身份、明确的聚合表示或自定义保存方案，并验证恢复映射。以上是固定源码推理，尚未做多进程保存实验，不构成现成实现处方。
