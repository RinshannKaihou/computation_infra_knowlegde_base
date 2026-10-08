---
id: training.checkpoint-state-recovery-experiment
title: Checkpoint 恢复状态异常验证实验设计
type: experiment
domain: training
status: draft
platforms: [generic]
source_refs:
  - src.pytorch.dcp-2.6
  - src.pytorch.dcp-issue-164257
  - src.pytorch.dcp-fix-edd8d35
updated_at: "2026-09-30"
summary: 用同源码基线的 missing-FQN 最小分支对照、独立 DCP 端到端对照和多 rank 状态身份组验证恢复边界。
related_ids:
  - training.checkpoint-state-recovery-triage
  - training.checkpoint-state-recovery-source-case
  - training.checkpoint-state-consistency
applicability:
  environment_refs: []
  notes: 仅为 PyTorch DCP 实验设计；PyTorch 2.8.0 历史症状环境、固定提交及其直接 parent 的同构建隔离环境、CPU 多进程资源和训练 oracle 尚未准备。
verification:
  status: not_verified
  evidence_refs: []
  notes: 尚未安装或运行 PyTorch、保存/加载 checkpoint、创建多进程组或执行训练；本文没有测量结果。
---

# Checkpoint 恢复状态异常验证实验设计

> 本页只定义实验，不授权安装、构建、保存、加载或训练。当前没有实际结果。

## 问题与假设

实验回答三个彼此分开的命题：

1. 当 checkpoint 的 optimizer state 缺少一个仍 `requires_grad` 的参数 FQN 时，固定修订 `edd8d356…` 是否只改变 `_split_optim_state_dict` 的 strict false/true 分支？
2. 通过 DCP `Stateful` 包装器恢复 fresh optimizer 时，目标端 `get_state_dict` 初始化和 partial-load 跳过是否会把 bias 占位 state 留在回调输入，从而根本没有触发 missing-FQN 分支？
3. 多 rank 以相同非 tensor FQN 保存不同 rank-local 内容时，默认 planner 实际保留什么；使用不冲突身份后能否按预定义映射恢复？

补丁因果对照只比较固定 commit `edd8d356b6d9a00cfa34fa323578e5cf1c7e0463` 与它的直接 parent `658c5f879c37142b1df51c7eb6c5a5bb06318597`，使用相同构建配方和依赖。PyTorch 2.8.0 只用于复核 Issue 的历史症状，不能与后续 main commit 的全部差异归因于这一个补丁。

预注册假设如下：

- H1：在输入给 `_split_optim_state_dict` 的 optimizer state 确实缺少 bias FQN 时，parent 的 strict false 路径触发无条件索引错误；固定 commit 的 strict false 跳过该 FQN，strict true 抛出补丁定义的解释性 `RuntimeError`。
- H2：fresh AdamW 的 `get_state_dict` 会通过 `_init_optim_state` 为所有 `requires_grad` 参数初始化 state；若 partial planner 对 checkpoint 中缺失的 bias key 不发出读请求，该目标占位值可能保留到 `Stateful.load_state_dict` 回调，导致 H1 分支不再是 missing-FQN 输入。
- H3：同名 rank-local 非 tensor 不能假定逐 rank 保存；不冲突身份或明确定义的聚合表示才可按 oracle 验证覆盖。

H1–H3 都需要执行证据。本设计不预先把源码推理写成实测，也不验证 GPU/NPU、world-size 变化或其他框架。

## 精确源码前提

PyTorch v2.8.0 的 [`_init_optim_state`](https://github.com/pytorch/pytorch/blob/ba56102387ef21a3b04b357e5b183d48f0afefc7/torch/distributed/checkpoint/state_dict.py#L605-L644)在 optimizer state 为空且参数没有现存 gradient 时，为所有 `requires_grad` 参数设置零 gradient、以零 LR 调一次 `step()`，再清除 gradient。[`_get_optim_state_dict`](https://github.com/pytorch/pytorch/blob/ba56102387ef21a3b04b357e5b183d48f0afefc7/torch/distributed/checkpoint/state_dict.py#L774-L835)和[`_load_optim_state_dict`](https://github.com/pytorch/pytorch/blob/ba56102387ef21a3b04b357e5b183d48f0afefc7/torch/distributed/checkpoint/state_dict.py#L932-L952)都会调用该初始化函数。因此“fresh optimizer”在目标端调用 `get_state_dict` 后不再等价于“optimizer state 仍为空”。

补丁对照的直接 parent 也保留同一关键路径：[`_init_optim_state` 615–656](https://github.com/pytorch/pytorch/blob/658c5f879c37142b1df51c7eb6c5a5bb06318597/torch/distributed/checkpoint/state_dict.py#L615-L656)、[`_get_optim_state_dict` 888–956](https://github.com/pytorch/pytorch/blob/658c5f879c37142b1df51c7eb6c5a5bb06318597/torch/distributed/checkpoint/state_dict.py#L888-L956)及[`_load_optim_state_dict` 1053–1074](https://github.com/pytorch/pytorch/blob/658c5f879c37142b1df51c7eb6c5a5bb06318597/torch/distributed/checkpoint/state_dict.py#L1053-L1074)。固定提交只改后面的 missing-FQN 分支，所以 P/F 端到端组都必须检查初始化造成的占位 state。

同版本 `DefaultLoadPlanner` 把 `allow_partial_load=True` 转为非 strict 的本地计划（[`default_planner.py` 315–352](https://github.com/pytorch/pytorch/blob/ba56102387ef21a3b04b357e5b183d48f0afefc7/torch/distributed/checkpoint/default_planner.py#L315-L352)）；本地计划遇到 checkpoint metadata 中不存在的目标 FQN 时直接跳过该读请求（[`default_planner.py` 453–492](https://github.com/pytorch/pytorch/blob/ba56102387ef21a3b04b357e5b183d48f0afefc7/torch/distributed/checkpoint/default_planner.py#L453-L492)）。它没有在这条分支中删除目标映射的既有值。

固定[提交 diff](https://github.com/pytorch/pytorch/commit/edd8d356b6d9a00cfa34fa323578e5cf1c7e0463)只把 `_split_optim_state_dict` 对缺失 optimizer FQN 的无条件索引改为“存在则装入；缺失且 strict true 报解释性错误；缺失且 strict false 跳过”。实验必须先证明传入该函数的 state 中确实没有目标 FQN，才能声称覆盖这条修订。

## 环境与输入

### missing-FQN 部分

- P 环境：固定 parent `658c5f879c37142b1df51c7eb6c5a5bb06318597`。
- F 环境：固定 commit `edd8d356b6d9a00cfa34fa323578e5cf1c7e0463`。
- P/F 使用相同 OS、Python、编译器、构建选项、依赖锁定、CPU 和实验脚本；记录源码 SHA、制品摘要和完整依赖差异。无法证明只差该提交时，不作补丁因果判断。
- H 环境：PyTorch 2.8.0 正式制品，只用于 Issue 历史路径；记录制品来源、摘要、macOS/CPU 差异，结果不并入 P/F 因果对照。
- 固定 `Linear(4, 2, bias=True)`、AdamW 超参数、初始化权重、输入/loss、随机性、保存目录和脚本 revision。

源对象只让 weight 参与 loss并执行一次 optimizer step。调用源对象 `get_state_dict` 前，必须用 optimizer 自身状态记录证明 weight state 已存在而 bias state 不存在；由于 optimizer state 已非空，预计 `_init_optim_state` 早退。随后记录 `get_state_dict` 输出中 optimizer `state` 的 FQN 集合和 param-group 参数集合。若 bias state 已出现，missing-FQN 组无效，不得继续解释补丁分支。

完整 state 正控制让 weight 与 bias 都参与 loss/update。所有组还要固定 model state、param groups 和输入字节，避免把 schema 或训练差异混入分支测试。

### 多 rank 部分

- 固定 PyTorch 2.6.0、CPU 多进程 backend、world size、rank 顺序、默认 planner、writer、共享存储和脚本 revision。
- 每 rank 生成可精确区分的非 tensor `cursor` 和 RNG 摘要；只使用测试标识。
- L0 使用相同逻辑 FQN；L1 使用不冲突 rank-local 身份或执行前定义的聚合表示。映射 oracle 在保存前冻结。

## 实验设计 A：直接覆盖补丁分支

这一部分不经过 DCP 文件读取。它把源对象生成且已确认缺少 bias FQN 的 `model_state_dict`/`optim_state_dict` 直接传给目标对象的 `set_state_dict`，用于隔离 `_split_optim_state_dict` 修订。

在调用 `set_state_dict` 前，目标 model/optimizer 必须 fresh；只读取 optimizer 原生 `state_dict()` 或内部 state 的离散 key，不调用目标 `get_state_dict`。`set_state_dict` 的装载路径自身仍会调用 `_init_optim_state`，所以还要记录调用前后目标 optimizer state；异常组的目标对象可能已被部分初始化，必须销毁，不能继续作为训练恢复对象。

| 组 | 源码与输入 | 选项 | 判定目的 |
| --- | --- | --- | --- |
| P0 | parent；源 optimizer state 缺 bias | `strict=False` | 单补丁前基线；只有输入缺 bias 已证明时，KeyError 才覆盖旧的无条件索引分支 |
| F0 | 固定 commit；与 P0 同 schema/内容 | `strict=False` | 检验固定 diff 是否跳过缺失 bias FQN |
| S0 | 固定 commit；与 P0 同 schema/内容 | `strict=True` | 检验补丁定义的解释性 `RuntimeError` |
| PC | parent；weight/bias state 完整 | 与 P0 相同 | parent 正控制 |
| FC | 固定 commit；与 F0 相同但 state 完整 | 与 F0 相同 | fixed 正控制 |

P0/F0/S0 必须记录传给 `set_state_dict` 的完整 model/optimizer key/FQN 集合，而不是只记录异常文本。F0 不抛错只证明该分支允许缺失；还需确认装载后的 target optimizer 中 bias state 是缺失、占位、重新初始化还是在下一次 update 创建，并按应用契约判断是否允许。

## 实验设计 B：独立 DCP 端到端路径

这一部分验证 wrapper、planner、读取和回调的组合行为，不用其结果替代 A 的单补丁分支对照。PyTorch 2.6 固定实现表明，对映射中的 `Stateful` 值，公共 `load` 会先调用 `state_dict()`，读取后在返回前调用 `load_state_dict()`（[`state_dict_loader.py` 53–189](https://github.com/pytorch/pytorch/blob/1eba9b3aa3c43f86f4a2c807ac8e12c4a7767340/torch/distributed/checkpoint/state_dict_loader.py#L53-L189)）。实验 wrapper 要在两个回调中记录 keys，不能只看 `load` 是否返回。

| 组 | 路径 | 目的与有效性 |
| --- | --- | --- |
| H0 | PyTorch 2.8.0，忠实 Issue：创建 model2/optimizer2，但仍把已训练的旧 model/optimizer 放入 `AppState` | 历史症状对照；不得称为 fresh-object 恢复，也不用于单补丁因果 |
| EP/EF | parent/fixed，fresh target `Stateful`；planner `allow_partial_load=True`，回调 `set_state_dict(strict=False)`；不裁剪目标 skeleton | 观察目标 `get_state_dict` 是否补出 bias，以及 partial load 后 callback 输入是否仍含 bias；若含 bias，该组没有覆盖 missing-FQN 分支 |
| BP/BF | parent/fixed，受控 instrumented `Stateful`；planner `allow_partial_load=True`，回调 `strict=False`；在记录目标 `get_state_dict` 后，只从读取 skeleton 删除已知缺失的 bias optimizer-state FQN，保留 model 与 param-group 身份 | 使 callback 输入的 missing-FQN 前提可观察；只有 callback 输入仍缺 bias 时，才把 parent/fixed 差异与 A 交叉确认 |
| BS | 与 BF 相同，只把回调选项改为 `strict=True` | 检验端到端回调是否得到补丁定义的 strict 错误；错误时公共 `load` 不应正常返回 |
| D0 | 普通 dict/非 `Stateful` 目标；planner `allow_partial_load=True`，先按 EP 的完整 fresh skeleton 读取，再显式调用 `set_state_dict(strict=False)` | 分开观察 DCP 读取返回与应用对象装载；若 partial load 保留 bias，占位会在显式 set 前被识别 |

BP/BF/BS 的 skeleton 裁剪是测试夹具，不是生产恢复建议。删除对象必须由源 checkpoint 缺失集合和目标 canonical FQN 共同确定；若裁剪了 model 权重、param group 或其他 state，该组无效。

### 四个观测点

每组至少记录以下离散快照，并给出取样发生在调用前还是回调内：

1. **target-native**：任何目标 `get_state_dict` 前，model keys、optimizer 原生 state key/param groups；
2. **target-get**：`Stateful.state_dict`/显式 `get_state_dict` 返回的 model keys、optimizer state FQN 和 param-group FQN；同时记录调用是否改变 target-native optimizer state；
3. **load-input/output**：普通 dict 在 `dcp.load` 返回后的 keys；`Stateful` 则在 `load_state_dict` 回调入口记录 DCP 读取后的 incoming keys；
4. **set-before/after**：传给 `set_state_dict` 的 keys、strict 值、首个异常，以及返回后 target-native model/optimizer state。

只要某组在第 3 点已经含 bias optimizer state，就不得声称该组触发固定 diff 的 missing-FQN 分支。只要回调抛错，公共 `dcp.load` 就没有正常返回；读取完成与公共 API 完成要分别记录。

## 实验设计 C：rank-local 非 tensor

| 组 | 保存输入 | 恢复目标 | 目的 |
| --- | --- | --- | --- |
| L0 | 各 rank 同一 FQN、内容不同 | 原 world size/原 rank 顺序 | 观察默认去重后实际可恢复内容；不预设写入者 |
| L1 | 各 rank 不冲突 FQN 或明确定义的聚合表示 | 原 world size/原 rank 顺序 | 验证每份 rank-local 内容覆盖和映射 |
| L2 | 与 L1 相同 | 允许的 rank 重排方案 | 仅在应用已定义旧身份到新 rank 的映射时检验；否则不执行 |

固定 v2.6.0 默认 planner 的去重路径见 [`default_planner.py`](https://github.com/pytorch/pytorch/blob/1eba9b3aa3c43f86f4a2c807ac8e12c4a7767340/torch/distributed/checkpoint/default_planner.py#L390-L414)和 [`_dedup_save_plans.py`](https://github.com/pytorch/pytorch/blob/1eba9b3aa3c43f86f4a2c807ac8e12c4a7767340/torch/distributed/checkpoint/_dedup_save_plans.py#L15-L58)；非 tensor index 只用 FQN 的位置见 [`planner_helpers.py`](https://github.com/pytorch/pytorch/blob/1eba9b3aa3c43f86f4a2c807ac8e12c4a7767340/torch/distributed/checkpoint/planner_helpers.py#L116-L120)。L0 用于验证固定源码推理，不构成推荐保存方案。

## 前置条件与运行影响

- 只用可销毁环境、临时 checkpoint 目录和独立输出路径；禁止指向生产 checkpoint 或“latest”标记。
- 不安装到共享训练环境，不修改生产模型、writer、数据游标或保留策略。
- 构建 P/F 制品前固定 toolchain、依赖和构建参数；任一非源码差异无法解释时停止补丁因果比较。
- 单进程部分消耗 CPU/内存/I/O；多 rank 部分消耗固定进程、共享存储和同步资源。具体配额在执行计划中填写。
- 多 rank 中任一进程退出、身份重排、内容 oracle 丢失或 writer 配置变化时停止该轮。
- 发现测试输出可能覆盖已知恢复点、需要 GPU/NPU/集群或影响其他负载时立即停止并重新评估授权。

## 执行与记录方法

1. 固定 H/P/F 环境身份、构建信息、脚本、初始化、loss、optimizer 超参数、对象关系和预期缺失 FQN。
2. 生成 missing 与完整源 state；先验证 source-native 和 source-get keys，不满足缺失前提就停止对应组。
3. 运行 PC/FC 正控制，再运行 P0/F0/S0；每组用新的 target 对象并记录四个观测点中适用的点。
4. 在独立目录运行 H0、EP/EF、BP/BF/BS、D0；逐点记录 keys，明确哪组实际进入 callback 和哪组实际缺 FQN。
5. 只对已返回且状态契约允许的组，用同一输入执行一次 forward/backward/update，再运行预定短窗口；失败对象不复用。
6. 在独立 PyTorch 2.6 环境运行 L0/L1；保存每 rank 原内容、rank 身份、planner metadata、实际恢复内容和写入者。只有映射契约明确时才运行 L2。
7. 清理临时对象、进程和目录，确认没有改动基线制品与生产恢复点。

## 观测与比较规则

| 类别 | 必记字段 | 比较方式 |
| --- | --- | --- |
| 身份 | 源码 parent/commit、制品摘要、toolchain/依赖、脚本、checkpoint ID、对象实例 | 精确相等；P/F 只允许预注册的源码提交差异 |
| 分支输入 | source/target/get/load/callback/set 各点的 key/FQN、param groups、strict/partial-load | 精确集合；缺失 FQN 必须在进入 split 前可见 |
| optimizer | 每参数 state、step/moment/variance、初始化与创建时点 | 离散存在性精确；浮点按预定规则 |
| API 边界 | DCP 读取、`Stateful` 回调进入/退出、`set_state_dict`、异常类型和栈顶 | 分阶段记录，不把回调失败写成 `load` 返回 |
| 训练进度 | optimizer/global step、输入身份、样本顺序 | 精确相等或预定义允许重放 |
| rank-local | 保存 rank 身份、FQN、原内容、恢复目标与内容 | 按映射 oracle 精确比较 |

同源码基线的离散分支结果按精确值比较。浮点是否 bitwise 由执行环境与实验目标决定；跨版本或运算顺序变化时，门槛须来自重复基线或既有验收依据。

## 通过、失败与无法判断的判据

支持 H1 至少要求：P/F 制品除目标提交外可比；P0/F0/S0 进入 split 前的 optimizer state 都缺同一 bias FQN；PC/FC 正控制通过；P0 出现旧无条件索引错误，F0 跳过，S0 给固定 diff 的 strict 错误。任何组在进入 set 前已含 bias，均不能计入 H1。

支持 H2 要求：EP/EF 的 target-native、target-get 和 callback-input 快照显示 fresh target 初始化与 partial skip 的实际变化。若 callback 输入含 bias，只能得出该端到端组没有覆盖补丁分支；不能据其“成功”或“两个版本相同”否定修订。BP/BF/BS 只有在裁剪范围和 callback 缺失集合均符合预注册时，才能与 A 交叉确认。

支持 H3 要求：L0 的实际保留结果与 planner metadata 可定位；L1 每份 rank-local 内容按 oracle 恢复；若执行 L2，旧身份到新 rank 的映射完整。L0 恰好恢复某 rank 内容不能证明其他 rank 状态被保存。

以下情况为无法判断：源码/制品身份不明、P/F 存在额外差异、目标 `get_state_dict` 未被记录、missing FQN 在 callback 前被占位填充、测试夹具误删其他 key、正控制失败、组间改变多个变量、保存点被覆盖、重复不稳定、rank 身份混淆或阈值事后调整。

## 实际结果与证据

尚未执行。当前没有构建制品、安装记录、checkpoint、key 快照、错误输出、继续训练对照或多 rank planner metadata。

完成复现后才可将 `verification.status` 改为 `reproduced`，并填写非空、可定位的 `evidence_refs`。源码预期、Issue 输出和实验计划不能替代本实验结果。

## 局限、来源与后续问题

- [PyTorch 2.6 Distributed Checkpoint](https://docs.pytorch.org/docs/2.6/distributed.checkpoint.html)与[固定 `load` 实现](https://github.com/pytorch/pytorch/blob/1eba9b3aa3c43f86f4a2c807ac8e12c4a7767340/torch/distributed/checkpoint/state_dict_loader.py#L53-L189)
- [PyTorch Issue #164257](https://github.com/pytorch/pytorch/issues/164257)
- [固定修订 `edd8d356…`](https://github.com/pytorch/pytorch/commit/edd8d356b6d9a00cfa34fa323578e5cf1c7e0463)及其[直接 parent `658c5f8…`](https://github.com/pytorch/pytorch/commit/658c5f879c37142b1df51c7eb6c5a5bb06318597)
- 局限：minimal set 分支、DCP 端到端与多 rank planner 是三个独立实验；都不证明 GPU/NPU、world-size 改变、其他 optimizer 或完整生产训练正确。
- 待确认：可复核的 P/F 同构建制品、隔离资源、重复次数、应用对缺失 optimizer state 的契约，以及数值和数据进度门槛。
