---
id: training.checkpoint-state-recovery-source-case
title: Checkpoint 恢复状态异常来源案例
type: case
domain: training
status: draft
platforms: [generic]
source_refs:
  - src.pytorch.dcp-issue-164257
  - src.pytorch.dcp-fix-edd8d35
updated_at: "2026-09-30"
summary: "复盘 PyTorch #164257 中未参与 loss 的 bias 没有 optimizer state、strict false 仍触发 KeyError，以及后续固定修订的边界。"
related_ids:
  - training.checkpoint-state-recovery-triage
  - training.checkpoint-state-consistency
  - data-storage.checkpoint-durability
applicability:
  environment_refs: []
  notes: 案例限定为 PyTorch 2.8.0、macOS 26、Apple M3 CPU 的单进程 DCP 报告及后续 main 修订；不能外推到 GPU/NPU 或其他发行。
verification:
  status: source_checked
  evidence_refs:
    - src.pytorch.dcp-issue-164257
    - src.pytorch.dcp-fix-edd8d35
  notes: 已核对 Issue 正文与四条公开评论、PR 审阅/合入时间线和固定提交 diff；未运行示例，原环境是否按修订复测未知。
---

# Checkpoint 恢复状态异常来源案例

## 案例来源与问题

本案例来自 [PyTorch Issue #164257](https://github.com/pytorch/pytorch/issues/164257)、[PR #165228](https://github.com/pytorch/pytorch/pull/165228)和固定 [commit `edd8d356…`](https://github.com/pytorch/pytorch/commit/edd8d356b6d9a00cfa34fa323578e5cf1c7e0463)。

报告者使用带 bias 的线性层和 AdamW，但 loss 只读取 `model.weight`。报告解释 bias 未参与 loss，因此 optimizer 没有为它创建内部 state。保存后恢复在拆分 optimizer state 时无条件索引 bias 的 FQN，触发 `KeyError: 'bias'`；报告称即使 `StateDictOptions(strict=False)` 和 `DefaultLoadPlanner(allow_partial_load=True)` 也会失败。

## 当时环境与代码边界

Issue 列出的环境为 PyTorch 2.8.0、Python 3.13.1、macOS 26.0 arm64 和 Apple M3 CPU；CUDA build/runtime 均为 `None/No CUDA`。日志显示 `torch.distributed` 未初始化，DCP 按单进程意图运行。

示例还有一个不能省略的对象关系：它创建了 `model2/optimizer2`，注释称重建后加载，但实际 `dcp.load` 仍传入 `AppState(model, optimizer)`，即保存时使用的旧对象。公开脚本因此没有证明“加载到新对象也失败”。本库没有修正脚本并执行，不能替原作者声称完成 fresh-object 复现。

## 事件与证据时间线

| 时间与时区 | 事件或观测 | 实体与范围 | 证据定位 |
|---|---|---|---|
| 2025-09-30，GitHub UTC | Issue 打开；报告 PyTorch 2.8.0 单进程 DCP 在缺少 bias optimizer state 时触发 KeyError | macOS 26、Apple M3 CPU、Python 3.13.1；无 CUDA | [Issue 正文与环境](https://github.com/pytorch/pytorch/issues/164257) |
| Issue 打开后，评论时间未由 connector 返回 | 维护者/贡献者建议直接调用 `set_state_dict(model, optim, options=...)`；报告者执行后得到缺少必需 state-dict 参数的 TypeError | 建议调用本身不完整，不能验证原 KeyError 是否修复 | [建议](https://github.com/pytorch/pytorch/issues/164257#issuecomment-3354013216)与[报告者回复](https://github.com/pytorch/pytorch/issues/164257#issuecomment-3366282525) |
| Issue 打开后，评论时间未由 connector 返回 | 另一用户称 strict false 对 optimizer state load 无效；后续贡献者称检查 key 存在似乎可修复 | 前者缺完整环境；后者是调查观察，尚不是合入代码 | [同类报告](https://github.com/pytorch/pytorch/issues/164257#issuecomment-3365280795)与[修订方向](https://github.com/pytorch/pytorch/issues/164257#issuecomment-3375212603) |
| 2025-10-11，GitHub UTC | PR #165228 打开并关联 #164257，目标是处理未保存 optimizer state 的参数 | PyTorch main 的 proposed code change | [PR #165228](https://github.com/pytorch/pytorch/pull/165228) |
| 2025-10-27，GitHub UTC | PR 页面记录 reviewer approval；时间线随后有 merge workflow 失败与重试 | PR 审阅和 CI/merge 流程 | [PR 时间线](https://github.com/pytorch/pytorch/pull/165228) |
| 2025-11-05，GitHub UTC | mergebot 添加 Merged 标签，并记录由 `edd8d35` 关闭 PR | PyTorch main 固定提交 | [PR 时间线](https://github.com/pytorch/pytorch/pull/165228)与[固定提交](https://github.com/pytorch/pytorch/commit/edd8d356b6d9a00cfa34fa323578e5cf1c7e0463) |

Issue 评论补强了问题链：另一用户也报告 strict false 无效，贡献者随后提出 key 存在性检查。但建议的直接 `set_state_dict` 调用缺少必需参数，报告者得到 TypeError，不能被写成 workaround 或复验成功。PR 评论时间线记录了 approval、rebase 和多次 merge workflow 尝试；作者称若干失败“似乎无关”只是评论，不足以判定 CI 根因。最终合入仍以 Merged 记录和固定 commit 为准。

## 假设与调查

| 候选解释 | 支持证据 | 反对或缺失证据 | 检查与结论 |
|---|---|---|---|
| checkpoint 缺少整个 bias 参数 | 报错 key 为 bias | 示例模型 state 与 optimizer state 是不同对象；报告只说明 optimizer state 未初始化 | 不获支持；不能把 optimizer state 缺失写成权重缺失 |
| bias 未参与 update，AdamW 未为它创建 state | loss 只使用 weight；报告者明确给出该解释 | 本轮未运行并检查保存内容 | 与脚本和固定修订目标一致，仍是来源报告而非本地测量 |
| `strict=False` 没有传到 optimizer state 拆分分支 | PyTorch 2.8.0 仍无条件索引并 KeyError；后续提交新增 `info.strict` 分支 | 没有对 2.8.0 源码做本地执行 | 固定 diff 支持代码路径修订 |
| 直接调用 `set_state_dict(model, optim, options=...)` 可绕过问题 | 一条评论提出该尝试 | 调用缺少两个必需 state-dict 参数，报告者得到 TypeError | 该建议未形成可用 workaround |
| 新对象恢复也一定失败 | 注释声称重建对象 | 实际 load 传旧 model/optimizer | 原脚本不能检验，保持未知 |
| 固定提交在原环境修复并正确续训 | PR 已合入 main | 无 Issue 作者同环境复测、无继续训练对照 | 保持未知 |

## 处理与结果

固定提交修改 `torch/distributed/checkpoint/state_dict.py` 的 `_split_optim_state_dict`：对 `requires_grad` 参数先检查 FQN 是否存在；存在则装入，缺失且 strict 为真则抛出解释性 `RuntimeError`，缺失且 strict 为假则跳过。精确分支见 [commit `edd8d356…` 的单文件 diff](https://github.com/pytorch/pytorch/commit/edd8d356b6d9a00cfa34fa323578e5cf1c7e0463)。

可确认结果是修订于 2025-11-05 合入 PyTorch main。首个包含该提交的正式发行版、backport 和原 Issue 环境复测未核实。strict false 跳过缺失 state 后，bias 没有恢复 optimizer 历史仍是事实；应用必须判断这种缺失是否符合保存边界，而不能把“不抛异常”直接写成训练恢复正确。

## 可复用经验与边界

- 模型参数存在、`requires_grad=True` 和 optimizer 已为参数创建 state 是三个不同状态；惰性 state 必须按实际 update 观察。
- `allow_partial_load`、对象 `strict` 和应用对缺失字段的接受策略可能作用在不同层，名称相似不能互相替代。
- Issue 示例代码的注释、对象实例和实际调用要逐一核对；修正示例后的行为属于新实验，不是原报告事实。
- PR Closed 顶部状态不能单独判断是否合入；本案例用时间线的 Merged 标签和固定 commit 交叉确认。
- main 合入不等于已有发行版或 backport，更不等于 GPU/NPU 环境验证。
- 一条装载异常的具体分流见[Checkpoint 恢复状态异常诊断指南](checkpoint-state-recovery-triage.md)。

## 来源与未解问题

- [PyTorch Issue #164257](https://github.com/pytorch/pytorch/issues/164257)
- [PyTorch PR #165228](https://github.com/pytorch/pytorch/pull/165228)
- [固定 commit `edd8d356…`](https://github.com/pytorch/pytorch/commit/edd8d356b6d9a00cfa34fa323578e5cf1c7e0463)
- 本地复现状态：未开展。
- 待确认：fresh-object 版本的结果、Issue 原环境复测、首个包含修订的发行版/backport，以及跳过 state 后的继续训练语义。
