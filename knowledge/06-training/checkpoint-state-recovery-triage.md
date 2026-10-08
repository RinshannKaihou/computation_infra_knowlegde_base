---
id: training.checkpoint-state-recovery-triage
title: Checkpoint 恢复状态异常诊断指南
type: procedure
domain: training
status: draft
platforms: [generic]
source_refs:
  - src.pytorch.dcp-2.6
  - src.pytorch.dcp-fix-edd8d35
updated_at: "2026-09-30"
summary: 以 PyTorch DCP 为样板，从恢复点身份、目标结构、对象装载、应用状态到继续训练逐层定位 checkpoint 恢复异常。
related_ids:
  - training.checkpoint-state-consistency
  - data-storage.checkpoint-durability
  - reliability.evidence-and-hypotheses
applicability:
  environment_refs: []
  notes: 适用于 PyTorch DCP 状态恢复的证据分层；目标 PyTorch 版本、硬件、并行布局、writer/reader 和训练应用尚未指定。
verification:
  status: source_checked
  evidence_refs:
    - src.pytorch.dcp-2.6
    - src.pytorch.dcp-fix-edd8d35
  notes: 已核对 PyTorch 2.6 DCP 文档和固定源码，以及后续 optimizer missing-state 修订；未执行保存、加载、训练或 GPU/NPU 验证。
---

# Checkpoint 恢复状态异常诊断指南

## 目标与触发条件

当 checkpoint 找不到或读不全、DCP 规划/读取报错、模型或 optimizer 应用状态失败、恢复后 step/LR/数据进度异常，或任务可以运行但轨迹偏离时，本流程定位最早出现分叉的边界。

流程只选择 PyTorch Distributed Checkpoint（DCP）作为具体样板。其他框架的 strict 选项、状态格式和重分片保证必须另查。训练恢复应先定义目标：回到完整 optimizer step、允许多少重放、是否保持精确样本序列，以及 world size/布局是否变化；详细语义见[Checkpoint 恢复一致性](checkpoint-state-consistency.md)。

## 适用范围与前置条件

- 固定 run/attempt、checkpoint ID、保存 attempt、框架和 reader/writer 版本、模型/代码/数据修订、world size 与并行布局。
- 先按[写入与持久化边界](../04-data-storage/checkpoint-durability.md)确认所选恢复点已经发布且分片/metadata 属于同一次保存。存储不完整与训练状态不一致须分开。
- 建立应有状态清单：模型、optimizer、scheduler、GradScaler、RNG、数据/采样进度、global/optimizer/micro step、累计统计和并行映射。
- 保存原始错误、strict/partial-load 选项、目标对象构造和装载顺序。宽松装载不是无条件成功策略。
- 在最后一个已知可恢复点完成验证前，不允许新运行覆盖它。生产恢复、checkpoint 修改和继续训练需要独立授权与回退。

## 需要的证据

| 证据组 | 同一对象/时点应记录 | 用途 | 缺失时如何处理 |
|---|---|---|---|
| 恢复点身份 | run/save attempt、checkpoint ID、分片/metadata、提交状态、摘要、reader/writer 版本 | 排除选错点、混合保存和存储缺失 | 停在存储边界，不能进入状态根因结论 |
| 保存 schema | 应有 key/FQN、shape/dtype/layout、param groups、应用状态清单 | 判断保存覆盖 | schema 未定义时把缺失字段记 `unknown` |
| 目标结构 | 模型结构、canonical FQN、目标 tensor 分配、并行 mesh/stage/shard | 判断读取和重分片前提 | 目标未固定则不做 load 成功判断 |
| optimizer 实况 | 参数 identity、param groups、实际存在的 state FQN、未参与更新参数 | 区分参数存在与 optimizer state 已初始化 | 不从 `requires_grad` 推断一定已有 state |
| 装载结果 | DCP 读取、对象 `set_state_dict/load_state_dict`、missing/unexpected、strict 分支 | 定位 DCP 与对象后处理边界 | 保留首个错误，不用连锁异常替代 |
| 继续训练 | step/LR/scaler/RNG/数据身份、同输入一步和持续窗口 | 判断训练是否从目标逻辑点续接 | 未运行时只报告“已装载”，不能写恢复正确 |

## PyTorch DCP 的责任边界

PyTorch 2.6 DCP 保存调用者提供的 state dict，不会自动发现 scheduler、GradScaler、RNG、数据游标或业务 step（[Distributed Checkpoint](https://docs.pytorch.org/docs/2.6/distributed.checkpoint.html)）。`load` 要求目标 tensor 已在目标设备和布局分配，返回值为 `None`，但返回前发生什么取决于传入映射的值：对普通 dict/非 `Stateful` 值，DCP 完成反序列化并替换或填充目标映射，应用仍需按对象契约调用 model/optimizer 的装载 API；对 `Stateful` 值，DCP 先调用其 `state_dict()` 取得读取目标，读取完成后会在公共 `load` 返回前调用该对象的 `load_state_dict()`（[固定 v2.6.0 `state_dict_loader.py` 53–189](https://github.com/pytorch/pytorch/blob/1eba9b3aa3c43f86f4a2c807ac8e12c4a7767340/torch/distributed/checkpoint/state_dict_loader.py#L53-L189)）。因此 `Stateful` 调用的 `load` 返回能够证明回调已返回，却仍不能证明 missing/unexpected 处置、跨对象逻辑时间或继续训练正确。

固定 v2.6.0 默认 planner 会为各 rank 的普通 tensor/非 tensor 建立写入项，再按相同 `MetadataIndex` 去重并选择写入者（[`default_planner.py` 69–113](https://github.com/pytorch/pytorch/blob/1eba9b3aa3c43f86f4a2c807ac8e12c4a7767340/torch/distributed/checkpoint/default_planner.py#L69-L113)、[`_dedup_save_plans.py` 15–58](https://github.com/pytorch/pytorch/blob/1eba9b3aa3c43f86f4a2c807ac8e12c4a7767340/torch/distributed/checkpoint/_dedup_save_plans.py#L15-L58)）。普通非 tensor 的 index 只使用逻辑 FQN，去重没有比较各 rank 内容是否相同（[`planner_helpers.py` 116–120](https://github.com/pytorch/pytorch/blob/1eba9b3aa3c43f86f4a2c807ac8e12c4a7767340/torch/distributed/checkpoint/planner_helpers.py#L116-L120)）。

所以，每 rank 都传同名 `rng` 或 `cursor` 不保证保留每份 rank-local 内容。应用必须给它们不冲突的逻辑身份、明确的聚合表示或自定义方案，并验证恢复到新 rank 的映射。不能把 planner 的去重选择者固定理解为协调 rank。

## 步骤与判断分支

| 步骤 | 检查或动作 | 运行影响 | 预期证据与解释 | 下一步 |
|---|---|---|---|---|
| 1 | 冻结失败 attempt 与 checkpoint 身份，选择已提交的只读副本 | 只读；复制会消耗存储 | 身份/分片/metadata 齐全才进入训练状态；否则属于存储或选择边界 | 完整进 2；不完整移交存储调查 |
| 2 | 比较保存 schema 与目标模型/optimizer/应用 schema | 只读结构检查 | missing/unexpected、重命名、shape/layout 和版本差异应显式列出 | 可映射进 3；未知或不支持则停止 |
| 3 | 按目标 world size/布局建立对象和 tensor，记录装载选项 | 分配内存/显存；不启动训练 | 对象构造正确是 DCP 读取前提，不证明保存内容正确 | 进入 4 |
| 4 | 按普通 dict 或 `Stateful` 路径记录读取与对象应用边界；`Stateful` 用回调内日志区分 | 读取 I/O；可能分配临时内存 | planner/reader 失败与 `Stateful.load_state_dict` 回调失败分别定位；公共 `load` 返回表示所选路径已完成，不表示训练正确 | 依据最早失败分流 |
| 5 | 审计模型、optimizer 和 trainer/application state | 只读比较 | 离散身份精确核对；缺失字段按契约拒绝或记录宽松处置 | 符合进 6；不符停止 |
| 6 | 用固定输入运行一次 forward/backward/update，再观察预定窗口 | 消耗计算和数据；须隔离授权 | 一步验证更新边界；持续窗口验证进度、样本和数值轨迹 | 满足完成判据后发布恢复点 |

### 最早异常怎样分流

| 最早异常 | 优先检查 | 不能推出 |
|---|---|---|
| checkpoint 不可发现、分片或 metadata 缺失、I/O 错误 | 保存 attempt、提交协议、reader/writer 与存储 | optimizer 或训练逻辑是根因 |
| DCP 规划/读取时报 missing key、shape 或 layout 不符 | 保存 schema、目标结构、canonical FQN、版本和重分片条件 | 字节损坏已被证明 |
| 读取完成，显式对象装载或 `Stateful.load_state_dict` 回调失败 | strict/missing/unexpected、optimizer 参数映射、root object 后处理；回调失败时公共 `load` 不会正常返回 | DCP 读取失败；或对象装载完成就应能训练 |
| 参数存在但 optimizer state 的 FQN 缺失 | 参数是否实际参与 loss/update，算法是否惰性创建 state，strict 契约 | checkpoint 必然损坏或参数权重缺失 |
| 对象装载完成，scheduler/scaler/RNG/游标/step 不符 | 状态是否保存、截取边界、装载顺序、rank-local 映射 | 权重一致足以续训 |
| 同输入一步成功，持续窗口偏离 | 输入身份、随机性、数据进度、optimizer state、浮点顺序 | 首步成功已证明长期正确 |

## optimizer state 缺失的 strict 分支

后续 PyTorch main 的固定 [commit `edd8d356…`](https://github.com/pytorch/pytorch/commit/edd8d356b6d9a00cfa34fa323578e5cf1c7e0463)修改 `_split_optim_state_dict`：`requires_grad` 参数的 FQN 存在于已保存 optimizer state 时才加载；缺失且 strict 为真时抛出解释性 `RuntimeError`，strict 为假时跳过该缺失 state。该提交修的是特定分支，不等于宽松装载后训练语义自动正确。

诊断时必须记录：目标参数是否有权重、是否要求梯度、保存前是否参与实际 update、optimizer 是否应有 state、缺失是否被契约允许。若 strict false 跳过一个预期应存在的 moment/variance，API 不报错仍属于待处置异常。固定提交在 2025-11-05 合入 main；首个包含它的发行版本和 backport 本页未核实，不能按版本号猜测。

## world size 或布局变化

PyTorch 2.6 文档声明 DCP 支持 load-time resharding，但前提是保存表示和目标 distributed object 受支持、目标对象先按新布局初始化、模型/optimizer 使用稳定 canonical FQN，且 shape/dtype/layout/格式满足 API 条件。文档也明确不保证 saved state dict 跨 PyTorch 版本向后兼容。

重分片只处理相应 tensor/state-dict 表示，不会自动转换 scheduler、scaler、RNG、数据进度、global step 或每 rank 应用状态。world size 改变时要先定义保持 global batch、样本顺序、optimizer step 还是只要求统计等价；定义不清即停止。

## 停止条件与恢复安排

以下情况停止继续 load 或训练：恢复点身份/版本未知；目标结构或转换规则不明确；宽松装载丢弃字段但没有逐项批准；rank-local 状态映射无法解释；world size/布局变化超出固定资料；验证将覆盖最后可用 checkpoint；需要生产写入、共享资源或不可回退变更。

所有验证使用恢复点的只读副本和新输出路径。失败时保留原 checkpoint、目标结构清单、首个错误和对照结果，销毁临时对象，回退到最后已确认点。不要让失败恢复运行发布“最新”标记。

## 完成判据

完成诊断需分别给出：

1. checkpoint 身份、分片/metadata 和存储选择状态；
2. 保存/目标 schema 及全部 missing、unexpected、迁移和宽松处置；
3. 模型、optimizer、scheduler、scaler、RNG、数据进度和逻辑 step 的状态；
4. rank-local 状态及并行映射的责任和恢复关系；
5. 同输入一次更新与预定义持续窗口的结果；
6. 可恢复、失败或无法判断结论，以及未覆盖的平台、版本和布局。

离散 key、shape、计数、样本身份与映射通常应精确相等。浮点量的 bitwise/close 规则须按版本、布局和目标风险预先定义；不同运算顺序时不能盲目以 bitwise 作为唯一门槛。

## 来源与验证记录

- [PyTorch 2.6 Distributed Checkpoint](https://docs.pytorch.org/docs/2.6/distributed.checkpoint.html)
- [固定 v2.6.0 默认 planner 去重实现](https://github.com/pytorch/pytorch/blob/1eba9b3aa3c43f86f4a2c807ac8e12c4a7767340/torch/distributed/checkpoint/_dedup_save_plans.py#L15-L58)
- [固定 optimizer missing-state 修订](https://github.com/pytorch/pytorch/commit/edd8d356b6d9a00cfa34fa323578e5cf1c7e0463)
- 当前验证范围：公开来源核对；未运行保存、加载或继续训练。
- 待确认：目标版本、完整状态 schema、writer/reader、并行布局、数据精确恢复能力及数值门槛。
