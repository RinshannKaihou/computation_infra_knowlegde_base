# 第七批 T06 Checkpoint 恢复异常来源准备

交付日期：2026-09-30。本记录只覆盖 T06 的流程、来源案例和实验设计。公开 PyTorch 页面、PyTorch 2.6 DCP 文档与固定源码于 2026-09-30 只读核对；没有安装 PyTorch、运行 Issue 脚本、保存或加载 checkpoint，也没有使用 GPU/NPU、集群或训练环境。

## backlog 身份与范围

| 任务 | 标题 | 稳定 ID | 目标路径 |
|---|---|---|---|
| T06-P | Checkpoint 恢复状态异常诊断指南 | `training.checkpoint-state-recovery-triage` | `knowledge/06-training/checkpoint-state-recovery-triage.md` |
| T06-C | Checkpoint 恢复状态异常来源案例 | `training.checkpoint-state-recovery-source-case` | `knowledge/06-training/checkpoint-state-recovery-source-case.md` |
| T06-X | Checkpoint 恢复状态异常验证实验设计 | `training.checkpoint-state-recovery-experiment` | `knowledge/06-training/checkpoint-state-recovery-experiment.md` |

三篇均选定 PyTorch Distributed Checkpoint（DCP）作为具体框架样板。通用诊断结构可以迁移，API、strict 语义、状态格式和重分片保证不能外推到其他框架。案例限定为 PyTorch 2.8.0/macOS/Apple M3 CPU 单进程，不写成 GPU/NPU 事故或本地复现。

## 复用的已审机制

复用 `src.pytorch.dcp-2.6` 与[Checkpoint 恢复一致性](../../knowledge/06-training/checkpoint-state-consistency.md)，主要边界如下：

1. DCP 保存调用者提供的 state dict；scheduler、GradScaler、RNG、数据游标和业务 step 不会因使用 DCP 自动进入 checkpoint。
2. PyTorch 2.6 公共 `load` 对映射中的 `Stateful` 值会先调用 `state_dict()`，完成读取后在返回前调用 `load_state_dict()`；对普通 dict/非 `Stateful` 值则反序列化并替换或填充映射（[固定 `state_dict_loader.py` 53–189](https://github.com/pytorch/pytorch/blob/1eba9b3aa3c43f86f4a2c807ac8e12c4a7767340/torch/distributed/checkpoint/state_dict_loader.py#L53-L189)）。两条路径都返回 `None`，但对象回调边界不同；返回仍不能证明回调语义、状态间一致性或继续训练正确。
3. 目标 tensor 必须在加载前按目标设备和布局建立。load-time resharding 依赖受支持的 DCP 表示、目标对象、canonical FQN、shape/dtype/layout 和框架版本条件，不是任意 world size 转换。
4. 固定 v2.6.0 默认 planner 为各 rank 的普通 tensor/非 tensor 建写入项，再按相同 `MetadataIndex` 去重并选择写入者。普通非 tensor 的 index 只使用逻辑 FQN；去重时不比较各 rank 内容是否相同（[`planner_helpers.py` 116–120](https://github.com/pytorch/pytorch/blob/1eba9b3aa3c43f86f4a2c807ac8e12c4a7767340/torch/distributed/checkpoint/planner_helpers.py#L116-L120)、[`_dedup_save_plans.py` 15–58](https://github.com/pytorch/pytorch/blob/1eba9b3aa3c43f86f4a2c807ac8e12c4a7767340/torch/distributed/checkpoint/_dedup_save_plans.py#L15-L58)）。因此每 rank 同名但内容不同的 RNG/游标不能假定全部保留；应用要给出不冲突身份、聚合表示或自定义方案，并验证恢复映射。
5. 文档明确不保证 saved state dict 跨 PyTorch 版本向后兼容。2.6 机制只能作为流程样板，不能补写 2.8 Issue 或后续 main commit 的发行支持。

写作时还链接[Checkpoint 写入与持久化边界](../../knowledge/04-data-storage/checkpoint-durability.md)：恢复状态异常的第一步是选择已通过存储完整性/提交条件的 checkpoint。文件不完整与训练状态不一致是两类问题，不能用同一个“load 失败”标签合并。

## T06-P：证据链和分支

### 观察对象

| 层次 | 观察对象 | 可区分的问题 |
|---|---|---|
| checkpoint 身份与存储 | run/save attempt、checkpoint ID、manifest/metadata、分片、提交状态、writer/reader 版本 | 选错点、混入不同尝试、缺分片、版本不兼容 |
| 目标结构 | 模型结构版本、canonical FQN、shape/dtype/layout、并行映射、目标 tensor 分配 | missing/unexpected key、参数重命名、错误 shard/stage、目标未初始化 |
| optimizer | param groups、参数身份、实际已有 state FQN、未初始化 state 的参数、装载选项 | “参数存在”与“optimizer 已为它创建 state”混淆，strict 分支不清 |
| trainer/application state | scheduler、scaler、RNG、数据/采样进度、global/optimizer/micro step、累计统计 | 文件可读但续训逻辑点不一致；rank-local 内容被同名去重 |
| 恢复后执行 | 同输入的 forward/loss/gradient/update、LR/overflow、样本身份、持续窗口 | 第一步能跑但轨迹、数据或更新已偏离 |

### 建议分支

| 最早异常 | 优先假设 | 不应跳到的结论 |
|---|---|---|
| checkpoint 不可发现、分片/metadata 不齐或 reader 报 I/O | 保存/提交/存储完整性或选择错误 | optimizer 或训练逻辑是根因 |
| DCP 规划/读取阶段 missing key、shape/layout 不符 | 保存 schema、目标结构、版本或重分片前提不符 | 文件损坏已被证明 |
| DCP 读取完成，显式对象装载或 `Stateful.load_state_dict` 回调失败 | root object 后处理、strict/missing/unexpected、optimizer 参数映射；回调失败时公共 `load` 不会正常返回 | DCP 读取失败；或对象装载完成即恢复正确 |
| optimizer 某参数无 state | 参数可能未参与 loss/update，或 optimizer 算法尚未为它惰性创建 state | 该参数本身缺失或 checkpoint 必然损坏 |
| 对象装载成功，step/LR/scaler/RNG/数据不符 | 应用状态未保存、截取边界不一致、装载顺序或 rank-local 映射错误 | 权重一致足以续训 |
| 同输入第一步成功但持续窗口偏离 | 浮点顺序、输入/RNG、optimizer 或进度状态差异 | 只凭非 bitwise 差异认定 checkpoint 错误 |

流程停止条件应包括：checkpoint 身份或版本未知；正在覆盖最后一个已知可用点；需要修改生产 checkpoint 或继续训练但没有隔离/回退；对象和时间无法对齐；宽松加载丢弃了未审计字段；world size/布局改变但转换前提未知。完成判据要求分别报告“可读”“对象装载”“状态对齐”“同输入一步”“持续窗口”，未覆盖层不得并入成功。

## T06-C：PyTorch #164257 → PR #165228 → 固定提交

### Issue 可确认事实

[PyTorch Issue #164257](https://github.com/pytorch/pytorch/issues/164257)于 2025-09-30 打开。报告环境明确为：

- PyTorch 2.8.0，Python 3.13.1；
- macOS 26.0 arm64，Apple M3 CPU；
- CUDA build/runtime 均为 `None/No CUDA`；
- `torch.distributed` 未初始化，DCP 警告按单进程意图处理。

示例用 `Linear(4, 2, bias=True)` 和 AdamW，只对 `model.weight` 求均值、反向并 step。bias 未参与 loss，因此报告解释 optimizer 没有为 bias 建内部 state。保存后加载触发 `KeyError: 'bias'`，即使 `StateDictOptions(strict=False)` 和 `DefaultLoadPlanner(allow_partial_load=True)` 都被使用。

必须保留示例的一个 quirk：代码新建了 `model2/optimizer2`，但 `dcp.load` 仍传入 `AppState(model, optimizer)`，即旧对象。公开脚本因此不能证明“加载到新建对象也同样失败”；本批没有修正脚本并运行，不能声称替原作者完成了该复现。

通过 GitHub connector 读取到四条 Issue 评论：

- [评论 3354013216](https://github.com/pytorch/pytorch/issues/164257#issuecomment-3354013216)把问题初步定位为 DCP load，并建议直接调用 `set_state_dict(model, optim, options=...)`；这个调用没有提供该 API 必需的 model/optimizer state dict。
- [评论 3365280795](https://github.com/pytorch/pytorch/issues/164257#issuecomment-3365280795)由另一用户称遇到同样问题，`StateDictOptions(strict=False)` 对 optimizer state dict 加载没有作用；该评论没有完整环境或复现附件。
- 报告者在[评论 3366282525](https://github.com/pytorch/pytorch/issues/164257#issuecomment-3366282525)按前述建议调用后得到缺少两个 keyword-only state-dict 参数的 `TypeError`，并称结果符合预期。这不是对原 KeyError 的修复验证。
- 后续贡献者在[评论 3375212603](https://github.com/pytorch/pytorch/issues/164257#issuecomment-3375212603)称正在调查，检查 key 是否存在似乎可修复；之后出现 PR #165228。评论中的“seem to fix”属于贡献者观察，固定 diff 和合入记录提供更强的代码证据。

### 修订链

[PR #165228](https://github.com/pytorch/pytorch/pull/165228)标题为修复“parameter with unsaved optimizer state”的 KeyError，正文关联 #164257。GitHub connector 返回 2025-10-27 的 APPROVED review，以及多次 rebase/merge workflow 尝试；公开时间线在 2025-11-05 显示 `Merged` 标签并由 bot 记录落入 `edd8d35`。此前一次 ROCm job 失败和一次 mandatory checks/merge-rule 失败只能说明当时合入未完成，不能据作者“似乎无关”的评论判定失败与修订无关；最终状态用固定 commit 交叉确认。

固定 [commit `edd8d356b6d9a00cfa34fa323578e5cf1c7e0463`](https://github.com/pytorch/pytorch/commit/edd8d356b6d9a00cfa34fa323578e5cf1c7e0463)只改 `torch/distributed/checkpoint/state_dict.py`：

- 对 `requires_grad` 参数，先检查 optimizer state 的 FQN 是否存在，存在才装入；
- 缺失且 `info.strict` 为真时抛出解释性 `RuntimeError`，并指向 `StateDictOptions(strict=False)`；
- 缺失且 strict 为假时不再无条件索引该 FQN，而是跳过缺失 state。

这证明固定 main commit 的代码分支与合入记录，不能证明首个包含修订的发行版本、任何 backport、Issue 原环境复测、GPU/NPU 行为或完整训练续接正确。PR 对话属于用户生成内容；PyTorch 根 BSD-3-Clause 只用于固定 commit 的仓库自有代码，不能覆盖 Issue/PR 评论许可。

### fresh target 与 partial-load 的遮蔽风险

进一步核对 v2.8.0 固定源码后，原先的 fresh-object 实验设计不能保证触发上述 diff：

- [`_init_optim_state` 605–644](https://github.com/pytorch/pytorch/blob/ba56102387ef21a3b04b357e5b183d48f0afefc7/torch/distributed/checkpoint/state_dict.py#L605-L644)在 optimizer state 为空、参数没有现存 gradient 时，为所有 `requires_grad` 参数设置零 gradient、以零 LR 调用一次 `step()`，再清除 gradient。
- [`_get_optim_state_dict` 774–835](https://github.com/pytorch/pytorch/blob/ba56102387ef21a3b04b357e5b183d48f0afefc7/torch/distributed/checkpoint/state_dict.py#L774-L835)会先调用 `_init_optim_state`；[`_load_optim_state_dict` 932–952](https://github.com/pytorch/pytorch/blob/ba56102387ef21a3b04b357e5b183d48f0afefc7/torch/distributed/checkpoint/state_dict.py#L932-L952)也会调用它。fresh AdamW 经目标 `AppState.state_dict → get_state_dict` 后，可能已同时具有 weight/bias 的占位 state。
- v2.8.0 `DefaultLoadPlanner` 将 `allow_partial_load=True` 传为非 strict 计划（[`default_planner.py` 315–352](https://github.com/pytorch/pytorch/blob/ba56102387ef21a3b04b357e5b183d48f0afefc7/torch/distributed/checkpoint/default_planner.py#L315-L352)）；checkpoint metadata 缺少目标 FQN 时，本地计划直接 `continue`，不会删除目标映射的既有值（[453–492](https://github.com/pytorch/pytorch/blob/ba56102387ef21a3b04b357e5b183d48f0afefc7/torch/distributed/checkpoint/default_planner.py#L453-L492)）。

直接 parent 同样在 [`_get_optim_state_dict` 888–956](https://github.com/pytorch/pytorch/blob/658c5f879c37142b1df51c7eb6c5a5bb06318597/torch/distributed/checkpoint/state_dict.py#L888-L956)和[`_load_optim_state_dict` 1053–1074](https://github.com/pytorch/pytorch/blob/658c5f879c37142b1df51c7eb6c5a5bb06318597/torch/distributed/checkpoint/state_dict.py#L1053-L1074)调用 [`_init_optim_state` 615–656](https://github.com/pytorch/pytorch/blob/658c5f879c37142b1df51c7eb6c5a5bb06318597/torch/distributed/checkpoint/state_dict.py#L615-L656)。固定提交只修改 missing-FQN 条件分支，P/F 都需处理同一占位风险。

因此 fresh target 加 partial load 可能把 bias 占位 state 原样带到 `Stateful.load_state_dict` 的 incoming mapping，使 `_split_optim_state_dict` 看到 bias 已存在。该组即使成功，也没有覆盖 missing-FQN 修订。Issue 原脚本之所以仍报告 KeyError，一个关键差异是它虽然创建了 model2/optimizer2，实际 `dcp.load` 仍传旧 model/optimizer；旧 optimizer 已有 weight state，`_init_optim_state` 会因 state 非空早退，bias 仍缺失。这是源码路径解释，尚未执行复验。

固定提交的 API 记录给出直接 parent `658c5f879c37142b1df51c7eb6c5a5bb06318597`。补丁因果实验应使用该 parent 与 `edd8d356…` 的同构建配方，只允许这一个提交差异；PyTorch 2.8.0 只作历史症状对照，不能把它与后续 main 的全部差异归因于单个补丁。

## T06-X：实验设计范围

实验分三部分，均尚未执行。

### A. missing-FQN 最小分支对照

先生成源 state：只让 weight 参与 loss/update；在调用源 `get_state_dict` 前证明 optimizer 已有 weight state、没有 bias state。因为 state 已非空，`_init_optim_state` 预计早退；源 `get_state_dict` 后还要再次核对 optimizer state FQN 缺 bias、param group 仍列 bias。只要 bias 已出现，实验前提失败。

把这份已确认缺 bias 的 model/optimizer state 直接交给 fresh target 的 `set_state_dict`，不经过 DCP 文件读取，也不先调用目标 `get_state_dict`。`set_state_dict` 内部装载仍会初始化 target optimizer，因此需记录 target-native 调用前后状态，异常 target 随后销毁。

| 组 | 固定源码/输入 | 目的 |
|---|---|---|
| P0 | 直接 parent `658c5f8…`；缺 bias；`strict=False` | 单补丁前无条件索引基线 |
| F0 | `edd8d356…`；与 P0 同 schema/输入；`strict=False` | 验证缺失 FQN 被跳过 |
| S0 | `edd8d356…`；同一缺失输入；`strict=True` | 验证解释性 RuntimeError |
| PC/FC | parent/fixed；weight 与 bias state 完整 | 两侧正控制 |

P/F 使用相同 OS、Python、toolchain、依赖和构建选项；身份或额外差异不清时，不作补丁因果判断。F0 不抛错不等于 bias optimizer 历史已恢复；还要记录返回后的 bias state 是缺失、占位还是在后续 update 新建。

### B. 独立 DCP 端到端对照

端到端组记录四个点：目标原生 state；`Stateful.state_dict/get_state_dict` 输出；DCP 读取后的普通 dict 或 `Stateful.load_state_dict` 回调入口 keys；传入 `set_state_dict` 及其返回/异常后的目标 state。

| 组 | 路径 | 边界 |
|---|---|---|
| H0 | PyTorch 2.8.0，忠实 Issue 的“创建新对象但 load 旧对象”路径 | 历史症状对照，不是 fresh 恢复，也不作补丁因果 |
| EP/EF | parent/fixed，fresh `Stateful`；planner `allow_partial_load=True`，回调 `strict=False`；不裁剪 target skeleton | 观察 bias 是否由 target get 初始化并被 partial skip 保留；callback 输入含 bias 时明确判为“未覆盖补丁分支” |
| BP/BF | parent/fixed，instrumented `Stateful`；planner `allow_partial_load=True`，回调 `strict=False`；记录 target get 后只移除已确认缺失的 bias optimizer-state FQN，保留 model/param-group | 受控触达 missing-FQN；只有 callback 输入仍缺 bias 时可与最小分支交叉确认 |
| BS | 与 BF 相同，只把回调改为 `strict=True` | 验证回调中的 strict 错误；异常表示公共 `dcp.load` 未正常返回 |
| D0 | 普通 dict 目标以 `allow_partial_load=True` 完成 DCP 读取后，再显式调用 `set_state_dict(strict=False)` | 把读入映射与对象装载分开；记录 partial load 是否保留占位 bias |

BP/BF/BS 的裁剪只是测试夹具，不是生产处方；误删 model、param group 或其他 state 即使组无效。任一组在回调/set 入口已经含 bias state，都不能宣称进入固定 diff 的 missing-FQN 分支。

### C. 多 rank 应用状态身份

| 组 | state dict 设计 | 目的 |
|---|---|---|
| L0 | 各 rank 在相同非 tensor FQN 下放不同游标/RNG 摘要，使用固定 PyTorch 2.6 默认 planner | 观察同 FQN 去重的实际保留结果，不预设写入 rank |
| L1 | 为每份 rank-local 状态赋不冲突逻辑身份，或采用执行前定义的聚合表示 | 正确性对照；验证恢复映射覆盖每个 rank |

L0/L1 是固定源码推理的实验化验证，不属于 #164257 的单进程案例，也不能用 commit `edd8d356…` 的 optimizer 修复解释。执行前需确定进程数、backend、输入、rank 重排政策和内容 oracle；不执行 GPU/NPU 或 world-size 变化可先在受支持的 CPU 多进程隔离环境设计，但本轮没有创建环境。

停止条件：版本/commit 身份不明、组间改变多个因素、测试写入共享 checkpoint、旧点可能被覆盖、目标对象关系未记录，或多 rank 中任一进程状态缺失。完成标准要预先定义错误类型、离散字段精确相等、浮点 close 规则、数据身份和持续窗口；不能盲目以 bitwise 作为跨版本/布局唯一门槛。

## 来源登记 YAML proposals

以下条目按 `schemas/sources.schema.json` 编写。本子任务不修改共享 registry。

```yaml
schema_version: 1
sources:
  - id: src.pytorch.dcp-issue-164257
    title: "PyTorch Issue #164257：unused parameter 的 optimizer state 恢复错误"
    url: https://github.com/pytorch/pytorch/issues/164257
    kind: issue
    registered_at: "2026-09-30"
    revision: "issue opened 2025-09-30; closed status and body observed 2026-09-30"
    license:
      status: unknown
      scopes: []
      notes: GitHub Issue 正文、日志和可能的评论属于用户生成内容；PyTorch 仓库 BSD-3-Clause 不自动覆盖讨论文本。本库只保留链接、必要短事实和原创分析，不复制完整脚本或日志。
    notes: 核对 PyTorch 2.8.0、macOS 26/Apple M3 CPU、Python 3.13.1、单进程 DCP、未初始化 bias optimizer state、strict false 仍 KeyError、示例创建新对象却加载旧对象的 quirk，以及四条公开 Issue 评论；评论中的建议调用缺必需 state-dict 参数，贡献者称 key 存在性检查似乎可修复。本轮未运行脚本。
  - id: src.pytorch.dcp-fix-edd8d35
    title: "PyTorch PR #165228 与固定 optimizer state 恢复修订"
    url: https://github.com/pytorch/pytorch/commit/edd8d356b6d9a00cfa34fa323578e5cf1c7e0463
    kind: repository
    registered_at: "2026-09-30"
    revision: edd8d356b6d9a00cfa34fa323578e5cf1c7e0463
    license:
      status: partial
      scopes:
        - scope: 固定 commit 的 PyTorch 仓库自有代码；Issue/PR 讨论及第三方文件另计
          identifier: BSD-3-Clause
          url: https://github.com/pytorch/pytorch/blob/edd8d356b6d9a00cfa34fa323578e5cf1c7e0463/LICENSE
      notes: 根 LICENSE 支持固定 commit 的仓库自有代码范围；PR 评论和审阅文本许可未知。本库只作短事实摘要并链接精确 diff。
    notes: 核对 PR 165228 在 2025-11-05 的 Merged 记录、固定提交及其直接 parent 658c5f879c37142b1df51c7eb6c5a5bb06318597、缺失 optimizer FQN 的存在性检查和 strict true/false 分支；首个包含该提交的发行版本、backport、Issue 原环境复测和 GPU/NPU 行为未知。
```

## 未知项和执行记录

- 首个包含 `edd8d356…` 的 PyTorch 正式发行版及 backport 未核实，不从 main 合入推导发行支持。
- Issue 作者没有在已取得页面中提供对固定提交的同环境复测；本轮也没有执行原脚本或修订脚本。
- 已通过 GitHub connector 取得四条 Issue 评论和 PR 的公开 issue/review 评论时间线；connector 返回不保证覆盖已删除、不可公开或服务端未返回的内容，不据缺失内容补写结论。
- 没有 GPU/NPU、分布式集群、world-size 变化或 rank-local 多进程实测；generic 只表示概念与导航范围，不表示平台兼容。
- 没有运行 `make`、上游测试、安装、保存/加载、训练或硬件操作；没有修改 registry、计划、导航、索引或 build。
