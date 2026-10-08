---
id: cluster-platform.ascend-device-visibility-source-case
title: 容器内 NPU 不可见来源案例
type: case
domain: cluster-platform
status: draft
platforms: [ascend]
source_refs:
  - src.vllm-ascend.issue-2557
  - src.vllm-ascend.pr-2541
updated_at: "2026-09-30"
summary: "复盘 vLLM Ascend #2557 中容器物理设备编号与 torch_npu 逻辑编号混用，以及 PR #2541 的有限修补范围。"
related_ids:
  - cluster-platform.ascend-device-visibility-triage
  - cluster-platform.device-resource-chain
  - reliability.evidence-and-hypotheses
applicability:
  environment_refs: []
  notes: 案例仅覆盖 2025 年 vLLM Ascend Mooncake connector 的物理/逻辑 ID 问题；不构成所有容器或框架的配置处方。
verification:
  status: source_checked
  evidence_refs:
    - src.vllm-ascend.issue-2557
    - src.vllm-ascend.pr-2541
  notes: 已核对 Issue、关键评论、PR 状态和固定 merge commit 代码；未复现原集群，且页面无报告者同环境复测日志。
---

# 容器内 NPU 不可见来源案例

## 案例来源与问题

本案例来自 [vLLM Ascend Issue #2557](https://github.com/vllm-project/vllm-ascend/issues/2557) 与 [PR #2541](https://github.com/vllm-project/vllm-ascend/pull/2541)。Kubernetes Pod 已请求四个 NPU，容器内 `npu-smi` 能列出物理编号 0、3、4、7，但报告者从 `/dev/davinci*` 取得这些编号并写入 `ASCEND_RT_VISIBLE_DEVICES` 后，torch_npu 进程只接受逻辑范围 `[0,4)`，选择 4 或 7 失败。

因此，这不是“容器内完全没有设备节点”的案例。它展示的是容器物理编号和框架逻辑编号发生分叉，最终表现为设备计数或选择失败。

## 当时环境与近期变化

报告者列出的环境为 Ubuntu 22.04 aarch64、torch 2.5.1、torch_npu 2.5.1.post1、vLLM 0.9.1、vLLM Ascend dev commit `f6a0e1629`、CANN 8.2.RC1。Pod 请求四个 `huawei.com/Ascend910`。

页面未给出 Kubernetes、kubelet、Device Plugin、Ascend Docker Runtime、驱动/固件、镜像 digest 或完整 Pod 最终配置。设备节点如何从 Allocate 结果进入容器也没有完整时间线。

## 事件与证据时间线

| 时间与时区 | 事件或观测 | 实体与范围 | 证据定位 |
|---|---|---|---|
| 2025-08-26，GitHub UTC | Issue 报告 Pod 请求 4 个设备；容器内管理工具列出 0、3、4、7 且健康 | 单个报告者的 Kubernetes Pod | [Issue 正文](https://github.com/vllm-project/vllm-ascend/issues/2557) |
| 2025-08-26，GitHub UTC | 报告者把物理设备编号写入可见设备变量；torch_npu 报输入须在 `[0,4)`，随后设备数/选择失败 | 同一容器进程；逻辑映射配置 | [Issue 错误与配置](https://github.com/vllm-project/vllm-ascend/issues/2557) |
| 2025-09-01，GitHub UTC | 另一用户称多节点场景有同类症状 | 不同环境；信息不完整 | [跟随评论](https://github.com/vllm-project/vllm-ascend/issues/2557#issuecomment-3241077552) |
| 2025-09-03，GitHub UTC | 贡献者称 cherry-pick PR #2541 可处理，但不是最佳方案，未来可能在 TE 侧改进 | 对 Mooncake connector 的处置建议 | [关键评论](https://github.com/vllm-project/vllm-ascend/issues/2557#issuecomment-3247467513) |
| 2025-09-03，GitHub UTC | PR #2541 合入 main，merge commit `07d44ade194b018ae2cc172482d55cb746c5fd0e`；页面记录检查和批准 | 项目代码和单元测试状态 | [PR #2541](https://github.com/vllm-project/vllm-ascend/pull/2541) |
| 2025-12-18，GitHub UTC | Issue 作者关闭 Issue 为 completed | Issue 项目状态 | [Issue 状态](https://github.com/vllm-project/vllm-ascend/issues/2557) |

## 假设与调查

| 候选解释 | 支持证据 | 反对或缺失证据 | 检查与结论 |
|---|---|---|---|
| 容器没有任何 NPU 设备 | 用户称设备不可用 | `npu-smi` 列出 0、3、4、7 且健康；存在 `/dev/davinci*` | 被该案例的容器观察反驳 |
| 物理 ID 被错误用作框架逻辑 ID | 物理编号稀疏，torch_npu 明确要求 `[0,4)` | 完整 runtime 注入配置未给出 | 最符合已知错误边界 |
| Mooncake/TE 仍需要物理 ID | PR 新增单独的物理设备变量，并按 DP/TP 切片 | 只覆盖固定 connector 代码 | 对该实现得到代码证据支持 |
| PR 已在原集群修复事件 | 贡献者建议 cherry-pick；Issue 后来关闭 | 无报告者同集群复测、镜像或发行 tag | 保持未知 |

## 处理与结果

PR #2541 在固定 merge commit 的 [`envs.py`](https://github.com/vllm-project/vllm-ascend/blob/07d44ade194b018ae2cc172482d55cb746c5fd0e/vllm_ascend/envs.py#L138-L141)增加 `PHYSICAL_DEVICES`，在 [`mooncake_connector.py`](https://github.com/vllm-project/vllm-ascend/blob/07d44ade194b018ae2cc172482d55cb746c5fd0e/vllm_ascend/distributed/mooncake_connector.py#L759-L778)读取物理 ID、按 DP/TP 范围切片并校验数量。新增单元测试覆盖 `PHYSICAL_DEVICES="10,11"` 时默认 rank 选择 10 的路径。

PR 合入且自动检查通过，证明项目代码发生了这项变更。贡献者同时把它描述为非最佳方案，审阅中也讨论了未来更稳健的处理。因此结果应写成“固定 Mooncake connector 补丁已合入”，不能写成所有容器的通用修复，也不能写成原集群已复测恢复。

## 可复用经验与边界

- 设备节点存在、管理工具可列举、框架可枚举与框架可选择每个逻辑 ID需要分别记录。
- 必须同时保存主机物理 ID、分配 ID、容器设备节点和进程逻辑 ID；编号相同不能靠猜测，编号不同也不必然表示漏挂载。
- 框架可见变量和需要物理拓扑的组件可以承担不同语义。该 PR 的 `PHYSICAL_DEVICES` 只属于当时实现，不是所有框架必须设置的变量。
- Issue 关闭和 PR 合入不能替代同一集群、同一镜像、同一输入的复测。
- 若容器枚举和单设备选择已通过，后续 HCCL 失败应移交通信路径。具体检查顺序见[容器内 NPU 不可见诊断指南](ascend-device-visibility-triage.md)。

## 来源与未解问题

- [vLLM Ascend Issue #2557](https://github.com/vllm-project/vllm-ascend/issues/2557)
- [Issue 中的处置建议](https://github.com/vllm-project/vllm-ascend/issues/2557#issuecomment-3247467513)
- [vLLM Ascend PR #2541](https://github.com/vllm-project/vllm-ascend/pull/2541)
- [固定 merge commit 的 connector 代码](https://github.com/vllm-project/vllm-ascend/blob/07d44ade194b018ae2cc172482d55cb746c5fd0e/vllm_ascend/distributed/mooncake_connector.py#L759-L778)
- 本地复现状态：未开展。
- 待确认：原集群的插件/runtime/驱动配置、补丁后镜像、同环境复测，以及后续发行是否采用其他实现。
