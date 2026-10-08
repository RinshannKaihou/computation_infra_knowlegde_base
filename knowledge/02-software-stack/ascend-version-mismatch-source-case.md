---
id: software-stack.ascend-version-mismatch-source-case
title: 昇腾版本配套失败来源案例
type: case
domain: software-stack
status: draft
platforms: [ascend]
source_refs:
  - src.vllm-ascend.issue-1188
updated_at: "2026-09-30"
summary: "复盘 vLLM Ascend #1188 中上游依赖与 TorchNPU 可用版本的冲突，并保留报告者未复测这一证据缺口。"
related_ids:
  - software-stack.ascend-version-mismatch-triage
  - software-stack.ascend-documented-profile
  - software-stack.compatibility-evidence
applicability:
  environment_refs: []
  notes: 仅适用于理解 2025 年 vLLM Ascend 0.9.0 安装依赖冲突的调查方法；不能外推到其他发行、硬件或 CANN 组合。
verification:
  status: source_checked
  evidence_refs:
    - src.vllm-ascend.issue-1188
  notes: 已核对公开 Issue 正文、关键评论和关闭状态；未本地复现，且原报告者未提供修复后日志。
---

# 昇腾版本配套失败来源案例

## 案例来源与问题

本案例整理自 [vLLM Ascend Issue #1188](https://github.com/vllm-project/vllm-ascend/issues/1188)。报告者的问题是：vLLM 0.9.0 的安装会取得 PyTorch 2.7.0，但当时可用的 TorchNPU 组合使用 PyTorch 2.5.1，应怎样安装。

这是依赖约束与安装顺序案例，不是本库现场事故。公开页面没有完整错误全文、硬件与驱动信息，也没有报告者按建议重装后的启动或计算结果。

## 当时环境与近期变化

Issue 正文给出的环境为：vLLM 0.9.0、vLLM Ascend 0.9.0、CANN 8.1.RC1，以及报告者所称已安装的 torch 2.5.1 与 torch_npu 2.5.1。硬件、驱动/固件、OS、CPU 架构、Python、容器镜像、wheel 来源与摘要均未知。

可确认的变化是安装 vLLM 0.9.0 后出现 PyTorch 2.7.0 依赖，而维护者随后解释 vLLM Ascend 的安装会因 TorchNPU 依赖把 torch 调整回 2.5.1。该解释针对当时版本化安装流程，不构成任意版本的通用安装规则。

## 事件与证据时间线

| 时间与时区 | 事件或观测 | 实体与范围 | 证据定位 |
|---|---|---|---|
| 2025-06-12，GitHub UTC | 报告者列出 vLLM/vLLM Ascend 0.9.0、CANN 8.1.RC1 和 torch/TorchNPU 2.5.1，并询问 torch 2.7.0 冲突 | 报告者的安装环境；制品来源未知 | [Issue 正文](https://github.com/vllm-project/vllm-ascend/issues/1188) |
| 2025-06-15 02:40，GitHub UTC | 项目成员说明当时使用 torch 2.5.1，指向版本化 `v0.9.0rc2` 安装页，并解释先装 vLLM、再装 vLLM Ascend 时会调整 torch 版本 | 维护者对当时发布流程的说明 | [关键评论](https://github.com/vllm-project/vllm-ascend/issues/1188#issuecomment-2973444343) |
| 2025-06-15 03:00，GitHub UTC | 同一成员询问是否还有问题；Issue 随后标记 completed | Issue 项目状态 | [后续评论](https://github.com/vllm-project/vllm-ascend/issues/1188#issuecomment-2973451049) |

关键评论中另有一句把 `python 2.5.1` 写入上下文。结合相邻关于 torch 的说明，这里不能被引用为 Python 版本要求；案例不修正原文，也不据此补写 Python 配套。

## 假设与调查

| 候选解释 | 支持证据 | 反对或缺失证据 | 检查与结论 |
|---|---|---|---|
| 上游 vLLM 与 TorchNPU 的 torch 约束在安装中冲突 | 报告者观察到 2.7.0；维护者明确说明当时后端使用 2.5.1 | 没有依赖解析日志或 lockfile | 得到维护者说明支持；精确解析链仍不完整 |
| 依照版本化安装顺序可得到目标组合 | 维护者给出版本化页面并解释后续安装会调整 torch | 没有报告者重装后的包清单 | 属于建议，实际成功未知 |
| CANN、驱动或硬件不兼容导致问题 | 正文只给 CANN 8.1.RC1 | 没有运行时错误、驱动和硬件证据 | 未获得支持，保持未知 |
| 建议后服务与计算恢复 | Issue 关闭为 completed | 没有启动、最小算子、模型或数值结果 | 不能确认 |

## 处理与结果

公开可确认的处理只有维护者指向版本化安装说明并解释依赖调整顺序。Issue 被标记为 completed，但页面没有报告者的复验。因此，本案例的结果是“维护者给出与当时发行相符的处置说明并关闭 Issue”，不是“原环境已证明修复”。

也没有关联 PR 表明项目代码因该 Issue 改动。关闭状态不能替代安装清单、启动结果或计算正确性证据。

## 可复用经验与边界

- 先记录解析前后的完整包身份，再判断是依赖求解问题还是运行时问题。
- 上游引擎、后端插件和 TorchNPU 可能分别约束 torch；应读取同一发行的版本化说明，不能拼接当前主干文档。
- 安装顺序可以改变最终解析结果，因此“曾安装某版本”不等于进程最终加载该版本。
- 维护者建议、Issue 关闭、导入成功、服务启动和计算正确是不同状态。
- 本案例不支持 TorchNPU 2.6、CANN 8.3.RC1 或其他 vLLM Ascend 发行。实际调查应使用[版本配套失败诊断指南](ascend-version-mismatch-triage.md)。

## 来源与未解问题

- [vLLM Ascend Issue #1188](https://github.com/vllm-project/vllm-ascend/issues/1188)
- [维护者的安装顺序说明](https://github.com/vllm-project/vllm-ascend/issues/1188#issuecomment-2973444343)
- 本地复现状态：未开展。
- 待确认：原环境的 Python、硬件、HDK、OS、包来源与摘要，以及重装后的包清单、启动和最小功能结果。
