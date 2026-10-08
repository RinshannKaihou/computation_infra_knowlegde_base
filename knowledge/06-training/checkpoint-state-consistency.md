---
id: training.checkpoint-state-consistency
title: Checkpoint 恢复一致性
type: concept
domain: training
status: draft
platforms: [generic]
source_refs:
  - src.pytorch.dcp-2.6
  - src.pytorch.parallel-training-state-2.6
  - src.pytorch.numerical-verification-2.6
  - src.ascend.mindspeed-llm-ha-v2.2.0
  - src.ascend.mindspeed-llm-checkpoint-v2.2.0
  - src.ascend.mindio-acp-v26.1.1
updated_at: "2026-09-30"
summary: 区分 checkpoint API 完成、对象装载成功与训练正确续接，说明状态覆盖、重分片条件和恢复后验证。
related_ids:
  - data-storage.checkpoint-durability
  - training.parallelism-and-state
  - communication.collectives-and-rank-progress
verification:
  status: source_checked
  evidence_refs:
    - src.pytorch.dcp-2.6
    - src.pytorch.parallel-training-state-2.6
    - src.pytorch.numerical-verification-2.6
    - src.ascend.mindspeed-llm-ha-v2.2.0
    - src.ascend.mindspeed-llm-checkpoint-v2.2.0
    - src.ascend.mindio-acp-v26.1.1
  notes: 核对 PyTorch 2.6 DCP、并行与数值文档，以及固定 MindSpeed-LLM 和 MindIO 资料；未执行保存、恢复、故障注入或数值对照实验。
---

# Checkpoint 恢复一致性

checkpoint 可以被保存和加载，不等于训练已经从同一逻辑状态正确继续。恢复一致性至少包含三项：需要的状态都被覆盖，各状态来自可解释的同一截取边界，装载后数据、随机性和更新规则按预先定义的目标继续推进。

文件写入、后台完成、提交标记和持久化故障域由 [Checkpoint 写入与持久化边界](../04-data-storage/checkpoint-durability.md)说明；状态所有者和并行布局由[并行策略与训练状态](parallelism-and-state.md)说明。本页从一个可读的恢复候选开始，讨论训练语义。

## 先定义希望恢复到什么

恢复目标需要在保存前确定。常见目标包括：

- **完整 step 边界恢复**：回到最近完成的 optimizer step；没有未提交梯度或飞行 micro-batch，允许重放之后的输入。
- **精确数据进度恢复**：除状态外，还要求样本/token 序列无未声明的重复或遗漏。
- **step 中间恢复**：保留 gradient accumulation、micro-step、overflow 决议和 schedule 等暂态；实现要求显著高于普通 checkpoint。
- **改变并行布局后恢复**：保持模型和 optimizer 的逻辑状态，同时把支持的 tensor state 重新分片到目标布局；其他应用状态需另行定义转换语义。

这些目标不能混用验收标准。例如允许回退一个 checkpoint interval 的方案，可以接受已处理但未提交的数据被重放；要求 exactly-once 样本推进的方案则需应用级提交或去重协议。所选资料没有提供跨框架通用的 exactly-once 数据语义或 mid-step 恢复协议。

## 状态覆盖与截取一致性

下表是恢复 schema 的最小核对框架，不表示每项必须采用同一序列化文件。

| 状态组 | 需要核对的内容 | 常见错误 |
|---|---|---|
| 模型 | 参数、持久 buffer、canonical identity、shape/dtype/layout、模型结构版本 | 只核对 key 存在，忽略错误 shard、stage 或 buffer |
| optimizer | state、param groups、参数身份映射、分片表示 | 文件可读但 moment/variance 对到错误参数；结构变化后仍按 parameter ID 顺序装载 |
| scheduler | 独立 `state_dict`、与 optimizer 的装载顺序和逻辑位置 | 只恢复当前 LR 或用 global step 猜内部状态 |
| GradScaler/loss scale | scale、growth tracker、策略字段、截取是否在 `update()` 后 | 从未决 optimizer step 中间截取，overflow 决议与其他状态不一致 |
| RNG | Python、NumPy、CPU、各设备/并行 tracker 和必要 worker 状态 | 只恢复一个 seed；rank 或设备重排后沿用旧编号含义 |
| 数据进度 | 数据版本、样本/token 身份、epoch、sampler/loader 状态、预取与重放规则 | 把“已读入 worker”当“已完成训练”，或只保存 epoch |
| 逻辑进度 | optimizer/global step、micro-step、samples/tokens consumed、累计统计 | 一个 `step` 同时承担多种含义；world size 改变后计数换算不清 |
| 并行映射 | 旧与目标 DP/TP/PP/EP/CP 维度、group/mesh 顺序、stage/shard placement、格式版本 | 只记录 world size，恢复端从当前环境猜旧布局 |
| 运行身份 | checkpoint ID、模型/代码/数据修订、框架和必要依赖版本 | 把来自不同保存尝试或不同版本的分片组合起来 |

PyTorch 2.6 DCP 只保存调用者提供的 `state_dict`，不会自动发现 scheduler、GradScaler、RNG、数据游标或业务 step（[Distributed Checkpoint](https://docs.pytorch.org/docs/2.6/distributed.checkpoint.html)）。应用需要显式构建状态清单，并定义这些对象属于哪个逻辑截取点。

固定 v2.6.0 的默认 planner 为各 rank 的普通 tensor/非 tensor 建立写入项，再按相同 `MetadataIndex` 去重、选择写入者；默认按计划存储量选择，不能固定理解为协调 rank。上游局部 docstring 仍称非协调 rank 不保存普通 tensor/非 tensor，与同文件实际循环不一致；这里按固定实现说明（[`default_planner.py` 69–113](https://github.com/pytorch/pytorch/blob/1eba9b3aa3c43f86f4a2c807ac8e12c4a7767340/torch/distributed/checkpoint/default_planner.py#L69-L113)、[390–414](https://github.com/pytorch/pytorch/blob/1eba9b3aa3c43f86f4a2c807ac8e12c4a7767340/torch/distributed/checkpoint/default_planner.py#L390-L414)、[`_dedup_save_plans.py` 15–58](https://github.com/pytorch/pytorch/blob/1eba9b3aa3c43f86f4a2c807ac8e12c4a7767340/torch/distributed/checkpoint/_dedup_save_plans.py#L15-L58)）。

这还意味着“每 rank 都传入同名 RNG/游标 key”不保证保留每份状态：非 tensor index 只使用逻辑 FQN，去重时没有比较各 rank 内容是否一致（[`planner_helpers.py` 116–120](https://github.com/pytorch/pytorch/blob/1eba9b3aa3c43f86f4a2c807ac8e12c4a7767340/torch/distributed/checkpoint/planner_helpers.py#L116-L120)）。rank-local 状态需要不冲突的逻辑身份、明确的聚合表示或自定义保存方案，并验证恢复映射。以上是固定源码推理，尚未做多进程保存实验，不构成现成实现处方。

完整 step 边界通常更容易形成一致快照：optimizer 更新已完成，scheduler 和 scaler 已按既定顺序推进，数据提交计数已经确定，也没有待恢复的 gradient accumulation。若实际保存与训练并发，暂存视图还必须不受后续修改影响；异步写入和持久化完成条件继续由存储侧证据判断。

## API 完成是一组不同的观察点

| 观察点 | 能证明什么 | 不能证明什么 |
|---|---|---|
| `save()` 返回，或异步 Future/finalize 完成 | 对应 API 与 writer 定义范围内的保存工作完成 | 状态清单完整；所有对象来自同一逻辑 step；后端覆盖了目标故障域 |
| 文件和 metadata 可读 | reader 可以解析结构，目标对象可能可被分配和填充 | optimizer 对到正确参数；RNG、数据和 scheduler 已覆盖；改变布局受到支持 |
| `load()` 以普通 dict/非 `Stateful` 值返回 | DCP 已反序列化并替换或填充调用者映射 | 应用已调用 model/optimizer 的 `load_state_dict`；missing/unexpected 已按对象契约处置；训练轨迹正确 |
| `load()` 以 `Stateful` 值返回 | DCP 已先取该值的 `state_dict()`、完成读取，并在返回前调用其 `load_state_dict()` 且回调已返回 | 回调语义正确；所有对象处于同一逻辑时间；训练轨迹正确 |
| `set_state_dict`/对象 `load_state_dict` 完成 | 对象接受了相应状态，可以检查 key 和结构结果 | 不同对象属于同一逻辑时间；样本无重复/遗漏；下一次 update 与参考相符 |
| 首个 forward/backward/step 成功 | 基本结构和运行路径没有立即失败 | 学习率、overflow、样本序列和长期数值轨迹正确 |
| 预定义恢复窗口通过 | 在固定环境、输入、oracle 和门槛下满足本次验收目标 | 其他版本、拓扑、world size、模型或故障方式也得到支持 |

PyTorch 2.6 DCP `load` 要求目标 tensor 预先在目标设备分配，返回值为 `None`。固定实现对映射中的普通值完成反序列化后替换/填充映射；对 `Stateful` 值则在读取前调用 `state_dict()`，并在读取后、公共 `load` 返回前调用 `load_state_dict()`（[固定 v2.6.0 `state_dict_loader.py` 53–189](https://github.com/pytorch/pytorch/blob/1eba9b3aa3c43f86f4a2c807ac8e12c4a7767340/torch/distributed/checkpoint/state_dict_loader.py#L53-L189)）。所以普通 dict 路径仍要显式执行对象后处理；`Stateful` 路径返回表示回调完成，但两种路径都还要验证状态间一致性与继续训练。

MindSpeed-LLM v2.2.0 固定 [`save_checkpoint_wrapper`](https://github.com/Ascend/MindSpeed-LLM/blob/53f3639c3da9c000a187c44cc0c08d55026ddded/mindspeed_llm/training/checkpointing.py)也显示出类似边界：异步路径把 latest iteration tracker 更新注册为 finalize callback，而不是在调度后台保存时立即更新。该文件没有固定外部 `generate_state_dict` 和完整 load 语义，所以不能从一条“scheduled async save”日志推断恢复点已经可用。

## 相同布局恢复的应用责任

即使 world size 与并行配置不变，恢复端仍需完成以下关系核对：

1. 选择一个已经通过存储完整性和提交协议检查的 checkpoint ID，不把不同尝试的 shard 混合。
2. 用匹配的模型结构和并行配置创建目标对象，再装载模型与 optimizer state。
3. 显式处理 missing、unexpected、重命名和迁移字段；不能把宽松装载自动视为成功。
4. 按框架要求恢复 optimizer、scheduler、GradScaler 和其他 trainer state；记录装载顺序。
5. 恢复 RNG 与数据进度，并解释 worker 预取、已消费和已提交进度的差别。
6. 核对 global/optimizer step、micro-step、samples/tokens consumed 与 checkpoint 截取点一致。
7. 在允许继续写入新 checkpoint 前完成恢复后验证，避免错误状态覆盖最后一个已知可用点。

其中 2—6 是应用与训练框架责任，文件 writer 无法单独证明。Elastic launcher 也不替应用保存状态：PyTorch 2.6 elastic train script 明确说明 worker 失败后会重启所有 worker，训练脚本需要自己的 save/load checkpoint 逻辑，进度最多回到最近 checkpoint（[Elastic train script](https://docs.pytorch.org/docs/2.6/elastic/train_script.html)）。

## 改变 world size 与重分片

PyTorch 2.6 DCP 声明支持 load-time resharding，distributed state-dict API 也说明可在不同 trainer 数和/或不同并行方式之间转换模型与 optimizer state（[Distributed Checkpoint](https://docs.pytorch.org/docs/2.6/distributed.checkpoint.html)）。该能力需要同时满足以下条件：

1. 保存表示和目标 distributed object 属于 DCP planner 支持的类型；普通 rank-local 文件、任意第三方 shard 或应用自定义字节不会自动进入重分片。
2. 恢复端先按**目标** world size、模型结构和布局初始化对象，并在目标设备分配 tensor；DCP 依据目标 shard 读取所需范围。
3. 模型和 optimizer state 使用 canonical FQN 或实现规定的稳定参数身份；普通 optimizer parameter ID 与列表顺序不能承担跨布局身份。
4. shape、dtype、offset、mesh/placement、模型结构和 state-dict 格式受所用 API 支持；`set_state_dict` 的分片 tensor 要求 ShardedTensor 或 DTensor。
5. 显式选项必须满足分支条件：`StateDictOptions.broadcast_from_rank0=True` 要求 `full_state_dict=True`，PyTorch 2.6 页面还说明该路径支持 DTensor 而不支持 legacy ShardedTensor。
6. 保存与恢复版本兼容。DCP 文档明确不保证 saved state dict 跨 PyTorch 版本向后兼容，跨版本需要迁移或单独验证。
7. scheduler、GradScaler、RNG、数据进度、global step 和应用状态有明确的新布局语义；tensor 重分片不会自动转换这些状态。
8. PP stage 重新切分、参数增删/重命名、模型结构或 optimizer 变更有专用转换器，否则应明确拒绝。

因此，“DCP 支持重分片”是特定 state-dict 表示与目标对象之间的能力，不是“任意 world size 都可恢复”。改变 DP size 时还应先选择要保持的训练语义：相同 global batch、相同样本序列、相同 optimizer step，或只要求统计等价。这些目标会影响 per-rank batch、gradient accumulation、学习率规则、数据分区和允许重放量。

固定 MindSpeed-LLM v2.2.0 的[高可用性文档](https://github.com/Ascend/MindSpeed-LLM/blob/53f3639c3da9c000a187c44cc0c08d55026ddded/docs/pytorch/features/high_availability.md)给出的是另一组明确限制：只按 DP 粒度缩扩，对 DP size、MoE、长序列、配置和并行组合有条件，缩容后不能再次缩容，扩容只能回原规模。该能力不能用 PyTorch DCP 文档补齐；也不能把 MindSpeed 的限制反向推广给所有 DCP 环境。

## 恢复后验证

验证应先固定参考运行、输入和比较边界，再启动恢复运行。建议按层推进：

| 层次 | 核对内容 | 判定方式 |
|---|---|---|
| 身份与结构 | checkpoint、模型/数据/代码版本，key、shape、dtype、layout、param group、并行映射 | 离散字段和 key 集合精确比较；迁移字段逐项列出 |
| 逻辑进度 | optimizer/global step、micro-step、samples/tokens、epoch/sampler、scheduler、scaler growth tracker | 整数和枚举按应用契约精确比较；明确允许的回退、重放和跳过量 |
| 状态内容 | 参数、optimizer moment/variance、buffer、scheduler、scaler、RNG | 可精确序列化的字段精确比较；浮点 tensor 按预定义规则比较 |
| 同输入单步 | forward 输出、loss、梯度摘要、overflow 决议、LR 和一次参数更新 | 使用相同样本/token、顺序、mask/label、micro-batch 分组和随机控制 |
| 持续窗口 | 多个 step 的输入身份、loss/grad/update 差异、NaN/Inf、通信进展、样本计数 | 预先定义窗口长度和各量门槛；一次 step 成功不代替持续验证 |
| 终止与回退 | key/身份不符、无法解释的 step 跳变、样本不符、超容差或 rank 分叉 | 停止继续训练，保留失败 checkpoint 与对照证据，回退到已确认恢复点 |

“相同输入”至少包括样本或 token 身份、顺序、mask/label、micro-batch 分组和数据增强随机性；“相同数据集”不够。比较前还要固定 train/eval 模式、shape、dtype、layout、并行配置和随机控制。world size 或切分变化时，先说明哪些输入关系在数学上保持不变。

## 精确字段与浮点容差

离散身份、key 集合、shape、逻辑计数、样本/token 身份和并行映射通常应精确相等。对浮点输出、梯度和参数更新，是否要求 bitwise 取决于环境和验证目标。

PyTorch 2.6 的数值精度说明指出，浮点加法和乘法不满足结合律；即使数学等价且输入相同，不同 release、commit 或平台也不保证 bitwise identical（[Numerical accuracy](https://docs.pytorch.org/docs/2.6/notes/numerical_accuracy.html)）。因此跨布局、跨后端或运算顺序变化时，盲目把逐位相等作为唯一门槛会混淆数值行为与 checkpoint 错误。

若采用逐元素 close 规则，可明确写成 `|actual - expected| <= atol + rtol * |expected|`（[`torch.testing.assert_close`](https://docs.pytorch.org/docs/2.6/testing.html#torch.testing.assert_close)）。每个比较量仍需记录 `rtol`、`atol`、dtype、聚合方式、样本数和 NaN/Inf 规则；阈值应来自目标环境重复运行、模型数值分析或既有验收依据，不能直接把框架默认值当作业务门槛。本页没有为任何模型提供容差。

## 常见误解

- **“load 没报错就是恢复成功。”** 它只覆盖 API 的装载阶段；状态覆盖、对象身份、数据进度和继续训练需要另外验证。
- **“只要权重一致就能续训。”** optimizer、scheduler、scaler、RNG 和数据进度会改变下一次更新。
- **“重分片会自动转换所有 trainer state。”** DCP 的 tensor/state-dict 能力不自动定义 scheduler、数据或应用计数在新 DP size 下的语义。
- **“恢复对照必须 bitwise。”** 离散字段通常应精确，浮点量需要按环境和风险定义比较规则；两者不能用一个门槛处理。
- **“后台保存已经调度，就可以发布最新 checkpoint。”** 异步任务的调度、finalize、存储提交和训练语义验证是不同完成点。

## 适用边界与待确认问题

本文是来源核对后的概念框架，尚无本地 GPU/NPU、集群、存储或故障注入证据。MindIO ACP 固定 README 只支持“先在训练服务器内存暂存，再异步写后端可靠性存储”的 I/O 边界（[MindIO ACP v26.1.1](https://github.com/Ascend/mind-cluster/blob/44385c13d7b1d87def35f1604e8be4d16de6ca4e/component/mindio/acp/README.md)）；它不提供本页的训练状态 schema、数值一致性或与 MindSpeed-LLM v2.2.0 的配套证明。

待确认：目标框架完整 save/load schema 与顺序、模型和 optimizer 迁移规则、DataLoader 精确恢复能力、设备与模型并行 RNG、PP mid-step 协议、MindSpeed 外部 Megatron commit 与 load/resharding 语义、目标 NPU 软件栈配套，以及具体模型的容差、验证窗口和允许进度损失。完整来源登记 YAML、固定定位和许可证范围见[第四批研究记录](../../docs/research/batch-04-training-sources.md)。
