---
id: communication.nccl-timeout-source-case
title: "NCCL Broadcast 超时来源案例：PyTorch #118369"
type: case
domain: communication
status: draft
platforms: [nvidia]
source_refs:
  - src.pytorch.issue-118369
updated_at: "2026-09-30"
summary: 整理一个 rank 1–7 在同一 Broadcast sequence 超时、rank 0 缺少对应行的外部案例，并保留维护者假设与 stale 关闭未修复边界。
related_ids:
  - communication.nccl-timeout-triage
  - communication.nccl-timeout-experiment
  - communication.collectives-and-rank-progress
  - reliability.evidence-and-hypotheses
applicability:
  environment_refs: []
  notes: "外部案例限定于报告者所述 AWS P4、8xA100-SXM4-40GB、PyTorch 2.1.2+cu121 和 DeepSpeed SFT 环境；NCCL/DeepSpeed 精确版本、NIC/fabric 和完整拓扑未知。"
verification:
  status: source_checked
  evidence_refs:
    - src.pytorch.issue-118369
  notes: "已核对 Issue 正文和公开评论中的环境、rank/sequence 时间线、GPU 利用率、维护者候选分支及 2026-05-05 stale 关闭说明；未本地复现，也没有修复 PR 或已证实根因。"
---

# NCCL Broadcast 超时来源案例：PyTorch #118369

## 案例来源与问题

本案例整理公开的 [pytorch/pytorch #118369](https://github.com/pytorch/pytorch/issues/118369)。报告者在 AWS P4 实例上用 DeepSpeed 对 Llama2-7B 做 supervised fine tuning，约 30 分钟等待后，rank 1–7 均在同一 `SeqNum=880`、`OpType=BROADCAST` 上报 ProcessGroupNCCL watchdog timeout，随后 launcher 终止全部子进程。

原始错误片段没有 rank 0 的同类 timeout 行。案例的核心问题因此是：rank 0 是否没有在正确时间进入这次 broadcast，以及它停在了哪一段上游控制流。网络/NCCL transport 故障仍是候选，但公开材料没有独立网络事件。

这是外部 Issue 来源整理。本库没有接触 AWS 实例、训练代码、数据、日志文件或进程栈，也没有运行复现。

## 当时环境与近期变化

| 层次 | 报告值 | 证据边界 |
| --- | --- | --- |
| 云/节点 | AWS P4 instance | 报告者没有给出完整实例型号、节点数、NIC/EFA、fabric 或拓扑；不能仅凭 P4 名称补齐 |
| GPU | 后续快照显示 8×NVIDIA A100-SXM4-40GB | 来自报告者评论中的单次 `nvidia-smi` 输出；没有 GPU UUID、NVLink/NVSwitch 或健康历史 |
| driver/CUDA 展示 | driver 535.104.12；`nvidia-smi` 显示 CUDA 12.2 | “CUDA Version”是 driver 展示能力字段，不等于容器/环境中的 CUDA runtime 精确身份 |
| OS/Python | Linux 5.15.0-1050-aws x86_64，glibc 2.31；Python 3.10.12 | 宿主/容器边界和镜像 digest 未给出 |
| PyTorch | 2.1.2+cu121，GPU available true | NCCL 精确版本、编译选项与动态加载库未知 |
| 应用栈 | Transformers 4.35.2；Accelerate 0.26.1；DeepSpeed 命令；Llama2-7B SFT | DeepSpeed 版本、训练 commit、配置内容、数据与近期变更未给出 |

报告者说创建新 virtualenv 后仍得到同类错误。这只能降低“原 virtualenv 独有状态”的可信度，不能证明系统软件、网络或应用控制流未变，也不是环境独立复现。

## 事件与证据时间线

| 时间与时区 | 事件或观测 | 实体与范围 | 证据定位 |
| --- | --- | --- | --- |
| 2024-01-25 17:50 左右，日志时区未说明 | rank 1–7 依次报告 `SeqNum=880`、`BROADCAST`、输入/输出元素数 131137536，configured timeout 1800000 ms，实际约 1800.6–1800.9 s | 7 个已显示 rank；原始 excerpt 没有 rank 0 对应行 | [Issue 错误片段](https://github.com/pytorch/pytorch/issues/118369) |
| 同期 | ProcessGroupNCCL 提示异步 CUDA 后续计算可能使用损坏/不完整数据，并终止进程以避免数据不一致 | 多个已超时进程 | 同上；这是 watchdog 之后的保护动作 |
| 2024-01-25 17:50:38–17:51:10 | launcher 依次 kill 8 个 subprocess；rank 7 对应进程退出码 -6 | 本地进程 0–7 | 同上 |
| 2024-01-29 22:27 UTC | 贡献者指出 broadcast 需要所有 rank，rank 0 没有打印 timeout，建议调查它是否未加入 | rank 0 为候选 culprit | [issuecomment-1915684994](https://github.com/pytorch/pytorch/issues/118369#issuecomment-1915684994) |
| 2024-01-30 00:23 UTC | 报告者提供快照：GPU 0 利用率 0%，GPU 1–7 为 100%；各 GPU 有 Python 进程和约 2.4–3.0 GiB 显存 | 8 个 GPU | [issuecomment-1915819487](https://github.com/pytorch/pytorch/issues/118369#issuecomment-1915819487) |
| 2024-03-01 18:48 UTC | 贡献者将原因分为 transport 未完成或一个/多个 rank 未按时调用正确 collective，并认为后者更可能；建议 instrumentation | 框架/DeepSpeed 控制流 | [issuecomment-1973742710](https://github.com/pytorch/pytorch/issues/118369#issuecomment-1973742710) |
| 2026-05-05 23:38 UTC | 维护者评论 `Category: Stale`，自动关闭并提示若仍活跃可 reopen | Issue 状态 | [issuecomment-4383979717](https://github.com/pytorch/pytorch/issues/118369#issuecomment-4383979717) |

rank 1–7 的 timeout 时间接近，说明它们对同一次 broadcast 等待到了相同预算；它不能证明这 7 个 rank 的更早进度完全相同。rank 0 没有对应错误行也可能来自日志缺失，因此必须与其进程栈/trace 交叉验证。

## 假设与调查

| 候选解释 | 支持证据 | 反对或缺失证据 | 检查与结论 |
| --- | --- | --- | --- |
| rank 0 没有进入 SeqNum 880 Broadcast | rank 1–7 同一 sequence/op 超时；rank 0 无同类行；贡献者明确提出该方向；GPU 0 利用率 0% | 没有 rank 0 的 Python/C++ 栈、last enqueued/completed、flight recorder 或业务阶段；日志 excerpt 可能不完整 | **首选调查假设，未确认** |
| rank 0 在不同应用控制流/collective | DeepSpeed 并行栈可能在某 rank 走不同分支；维护者建议 instrument collective 次序 | 没有训练代码、配置和逐 rank trace | **合理但未定位** |
| NCCL/网络 transport 未完成 | 维护者保留“所有 rank 正确调用但 network/NCCL 层失败”的分支 | 没有 NCCL WARN、socket/IB/link、NIC/fabric 或路径事件；rank 0 缺席更推动控制流分支 | **未排除，证据弱** |
| GPU 0 硬件/driver 故障 | GPU 0 利用率低 | 仍有 Python 进程和显存；没有 Xid/CUDA fatal/device loss；利用率为 0 也可能是等待 CPU/数据/控制流 | **不能由利用率证明** |
| timeout 预算过短 | configured timeout 为 30 分钟 | broadcast 在 30 分钟内无共同完成，且 rank 0 可能没参与；没有正常耗时基线 | **不能建议仅提高 timeout** |

维护者在 2024-03 评论中提到当时正在开发 ProcessGroupNCCL Flight Recorder，尚未普遍可用。该历史评论不能倒推本案例已有 trace，也不能替代今天针对目标 PyTorch 版本的文档核对。

## 处理与结果

公开记录中的实际动作包括：报告者更换 virtualenv，再次遇到错误；贡献者建议从 rank 0 调用次序和进程位置调查；报告者提供 GPU 利用率快照；后续评论没有给出 root stack、源码定位、配置修复或成功重跑。

因此结果是：

- **运行状态**：当次训练被 watchdog/launcher 终止；没有恢复成功记录。
- **根因状态**：rank 0 未进入同一 broadcast 是证据较强的调查假设，仍未由栈、trace 或最小复现确认。
- **修复状态**：没有关联修复 PR、commit 或 release，也没有验证 workaround。
- **Issue 状态**：2026-05-05 因 stale 自动关闭为 `not planned`；这是生命周期处理，不是技术修复。

## 可复用经验与边界

- 首先在同一 process group 中比较 rank、`SeqNum`、`OpType` 和数据量。多数 rank 同步超时常常是在等待一个缺席 rank。
- “没打印 timeout”的 rank 是调查入口，不是自动 culprit；可能存在日志缺失、提前退出或不同 group。
- GPU 利用率和显存能说明设备当时的表面活动，不能说明进程正在执行哪段控制流。需要栈、trace 或应用 instrumentation。
- watchdog 为保护数据一致性终止进程是超时后的行为，不能反推 GPU、NCCL 或网络是首因。
- 网络与控制流两类假设都应保留，直到有 NCCL/transport 事件或 rank 调用轨迹把它们分开。
- stale/`not planned` 关闭不等于问题不再存在，也不等于维护者拒绝了某个根因；它只说明公开线程未继续推进。

这些方法可以迁移到其他 NCCL timeout；本案例的 AWS、A100、PyTorch 2.1.2 或 DeepSpeed 条件不能外推为其他版本的已知缺陷。

## 来源与未解问题

- [PyTorch #118369](https://github.com/pytorch/pytorch/issues/118369)：核对 Issue 环境、错误片段、评论和当前状态。
- [rank 0 调查方向](https://github.com/pytorch/pytorch/issues/118369#issuecomment-1915684994)、[GPU 利用率快照](https://github.com/pytorch/pytorch/issues/118369#issuecomment-1915819487)、[两类候选分支](https://github.com/pytorch/pytorch/issues/118369#issuecomment-1973742710)、[stale 关闭](https://github.com/pytorch/pytorch/issues/118369#issuecomment-4383979717)。
- 本地复现状态：未开展；未运行 PyTorch、DeepSpeed、NCCL 或任何 GPU/网络测试。
- 待确认：NCCL/DeepSpeed 版本、rank 0 的完整日志和栈、process group 身份、训练代码/配置、NIC/fabric/拓扑、设备/driver 事件、最小复现、根因和修复版本。
