---
id: software-stack.ascend-version-mismatch-experiment
title: 昇腾版本配套失败验证实验设计
type: experiment
domain: software-stack
status: draft
platforms: [ascend]
source_refs:
  - src.ascend.torch-npu-v7.2.0-pytorch2.6.0
  - src.huawei.cann-83rcx-install-2026-09-29
updated_at: "2026-09-30"
summary: 通过已知基线、单变量错配和恢复对照，区分依赖解析、导入链接、运行时与最小算子阶段的版本影响。
related_ids:
  - software-stack.ascend-version-mismatch-triage
  - software-stack.ascend-documented-profile
  - software-stack.compatibility-evidence
applicability:
  environment_refs: []
  notes: 仅为实验设计；完整硬件、HDK、OS、CANN 子包、wheel 来源和隔离节点尚未确定，不能直接执行。
verification:
  status: not_verified
  evidence_refs: []
  notes: 尚未执行任何安装、NPU 运算或版本故障注入；所有结果均为预期分支而非测量值。
---

# 昇腾版本配套失败验证实验设计

## 问题与假设

研究问题是：在硬件、HDK、OS、镜像和输入固定时，改变 PyTorch、TorchNPU 或 CANN 用户态中的一个版本，能否在依赖解析、导入/动态链接、设备运行时或最小算子边界产生可重复差异，并在恢复基线后消失？

假设 H1：若差异由单一版本变量引起，则错配组与基线的制品身份只有该变量不同，首个失败层可重复，恢复组回到基线行为。若基线失败、多个变量联动改变，或设备健康/加载路径漂移，则 H1 无法判断。

实验不验证上层引擎、分布式通信、模型加载、性能或数值训练正确性。

## 环境与输入

固定 TorchNPU README 给出一个**候选核心**：CANN 8.3.RC1、PyTorch 2.6.0、TorchNPU 2.6.0.post3，Python 3.9/3.10/3.11。对应的[配套表](https://github.com/Ascend/pytorch/blob/bc51ab84cc6f35c77aab1c59886e0ea43681a317/README.md#ascend-auxiliary-software)和 [Python 表](https://github.com/Ascend/pytorch/blob/bc51ab84cc6f35c77aab1c59886e0ea43681a317/README.md#pytorch-and-python-version-matching-table)只覆盖 README 中的声明。

执行前必须另行补齐并冻结：

- 专用 NPU 节点、硬件型号与拓扑、驱动/固件精确身份；
- OS/内核与 CPU 架构、容器运行时和镜像 digest；
- CANN 全部必需子包、安装介质来源与摘要；
- Python 精确补丁版本，PyTorch/TorchNPU wheel 文件名、索引来源与摘要；
- 动态库搜索路径和实际加载文件；
- 固定随机输入、dtype、shape、设备、预期输出计算方法和容差。

这些条件当前未具备，因此候选核心不能被称为可执行基线。

## 实验设计

| 组 | 保持不变 | 唯一变更 | 目的与预期观察 |
|---|---|---|---|
| B0 | 全部已核实基线 | 无 | 建立依赖解析、import、设备枚举和最小算子参照 |
| N1 | B0 除 PyTorch 外全部 | 改为不在同一固定矩阵行的 PyTorch 制品 | 观察解析、import 或符号边界；不预设必然失败方式 |
| N2 | B0 除 TorchNPU 外全部 | 改为另一固定发行制品 | 观察 extension 与 PyTorch/CANN 交界 |
| N3 | B0 除 CANN 用户态外全部 | 只改一组明确的 CANN 用户态子包 | 区分 import 与运行时/算子阶段；不得隐式改 HDK |
| R0 | 恢复 B0 全部身份 | 撤销 N1/N2/N3 | 验证环境可回到基线，排除持续漂移 |

N1、N2、N3 应分开运行，每次从相同基线重建。每组至少按执行前确定的次数重复；重复数和判定阈值不能在看见结果后调整。B0 与 R0 使用完全相同的输入、dtype、shape 和输出比较方法。

最小功能采用固定 README [Quick Verification](https://github.com/Ascend/pytorch/blob/bc51ab84cc6f35c77aab1c59886e0ea43681a317/README.md#quick-verification)所代表的两个 NPU tensor 矩阵乘法路径，但实际脚本、随机种子、输入值和容差必须在执行前保存。README 示例本身没有规定统计重复或数值容差。

## 前置条件与运行影响

- 只在可销毁、可重建的隔离环境和专用节点执行；不得修改共享生产 CANN、驱动或固件。
- 每次安装会改变包、缓存和动态链接状态；使用独立镜像或环境，并保存镜像与 wheel 摘要。
- 最小算子占用单个 NPU、少量显存和计算时间；具体上限由执行计划预先填写。
- 不运行上层模型或 HCCL；若验证扩展到这些范围，应建立新的实验和资源评估。
- 任一组影响其他租户、需要重启共享服务、无法恢复基线，或实际加载文件与清单不一致时立即停止。

## 执行与记录方法

1. 审核 B0 的完整官方依据、硬件/HDK 条件和介质摘要；任一项缺失则不开始。
2. 创建隔离环境，记录安装前后 lockfile、包清单、解析输出、镜像 digest 和时间窗。
3. 对 B0 依次记录 import、实际加载库、设备枚举、最小算子退出状态和输出。
4. 每次只创建一个 N 组；复核除了目标变量外的摘要均与 B0 相同，再运行同一检查。
5. 保存首个失败及其前置成功状态；后续连锁错误另列，不覆盖首个边界。
6. 销毁 N 组或恢复 B0，建立 R0，并用同一输入重复检查。
7. 比较重复间稳定性，记录偏差、缺失和任何未计划变化。

## 观测字段

| 类别 | 必记字段 |
|---|---|
| 身份 | 节点/容器、镜像、Python、包文件与摘要、CANN 子包、HDK、OS/架构 |
| 解析 | 请求约束、解析后的版本、安装顺序、退出状态、告警 |
| 加载 | import 状态、实际动态库路径、首个缺失符号或 ABI 错误 |
| 设备 | 设备数、所选逻辑设备、运行时初始化状态 |
| 计算 | 输入摘要、dtype/shape、输出摘要、参照与容差、退出状态 |
| 恢复 | R0 身份与 B0 差异、同输入结果、设备健康变化 |

## 通过、失败与无法判断的判据

支持 H1 需要同时满足：B0 与 R0 的身份相同并通过预定义最小功能；某个 N 组只有目标版本不同；该组的首个差异在重复中稳定；恢复后差异消失。此处“通过”只覆盖最小功能。

若 N 组与 B0 没有差异，只能说明该最小路径未暴露问题，不能宣称组合全面兼容。若 B0/R0 失败、包解析连带改变其他组件、动态库来源不同、硬件健康变化、容差事后修改或重复结果不稳定，结论为无法判断。

任何组出现错误都不自动证明官方 `unsupported`；官方支持状态仍由固定发行资料决定。

## 实际结果与证据

尚未执行。当前没有环境清单、安装日志、NPU 输出或恢复证据，不填写测量结果。

完成复现后才可将 `verification.status` 设为 `reproduced`，并填写可定位、可审阅的 `evidence_refs`。

## 局限、来源与后续问题

- [TorchNPU 固定配套表](https://github.com/Ascend/pytorch/blob/bc51ab84cc6f35c77aab1c59886e0ea43681a317/README.md#ascend-auxiliary-software)
- [TorchNPU 固定 Quick Verification](https://github.com/Ascend/pytorch/blob/bc51ab84cc6f35c77aab1c59886e0ea43681a317/README.md#quick-verification)
- [CANN 8.3.RCX 安装前提](https://www.hiascend.com/document/detail/zh/canncommercial/83RC1/softwareinst/instg/instg_0002.html)
- 局限：固定来源未补齐可执行的硬件/HDK/OS/介质组合，也不覆盖 vLLM、MindSpeed、HCCL 或目标模型。
- 待确认：完整基线、隔离资源、重复次数、数值参照与容差。
