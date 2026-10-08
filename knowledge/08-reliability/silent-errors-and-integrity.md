---
id: reliability.silent-errors-and-integrity
title: 静默错误与计算完整性判定
type: concept
domain: reliability
status: draft
platforms: [generic]
source_refs:
  - src.arxiv.sdc-at-scale-v1
  - src.usenix.superbench-atc24
  - src.ocp.sdc-in-ai-2025
  - src.pytorch.numerical-verification-2.6
updated_at: "2026-09-30"
summary: 定义静默错误（结果错误但无报错）与相邻概念，解释被动监控的盲区与主动校验的覆盖边界，给出冗余、不变量、canary、fleet 筛查与数值容差比对的证据强度和边界。
related_ids:
  - reliability.dimensions-and-failure-domains
  - reliability.evidence-and-hypotheses
  - hardware.health-evidence
  - training.gpu-npu-precision-difference-triage
verification:
  status: source_checked
  evidence_refs:
    - src.arxiv.sdc-at-scale-v1
    - src.usenix.superbench-atc24
    - src.ocp.sdc-in-ai-2025
    - src.pytorch.numerical-verification-2.6
  notes: "已核对 SDC 论文 v1 节级内容、SuperBench 印刷页 835–844、OCP 白皮书 p.1–19/29 与 PyTorch 2.6 数值/随机性/testing 文档；未做任何硬件测试或故障注入。"
---

# 静默错误与计算完整性判定

## 定义与要解决的问题

**静默错误（silent data corruption, SDC）**：计算结果错误，但没有任何系统事件或错误日志指示这次误算。Meta 的定义性案例是“2x3 得 5”——在特定微架构条件下静默发生，系统事件与错误日志中没有任何指示（[arXiv:2102.11245v1 §1](https://arxiv.org/abs/2102.11245v1)）。它要回答的问题是：当所有监控都“绿”的时候，凭什么相信计算结果是对的。

三个相邻但不同的概念必须先分开：

| 概念 | 域 | 表现 | 主要证据来源 |
|---|---|---|---|
| 静默错误（SDC） | 结果正确性 | 输出错误、无报错 | Meta CPU SDC 论文、OCP AI 白皮书 |
| 灰色退化（gray failure / fail-slow） | 性能稳定性 | 渐进变慢、冗余掩盖局部退化 | SuperBench（Azure GPU 集群） |
| 软件/算法层的静默错误结果 | 数值语义 | 病态输入下 linalg 静默返回错误结果等 | PyTorch 数值文档 |

冗余在两者中都扮演掩盖角色：SuperBench 实证了冗余链路/行重映射掩盖性能退化——在其特定测试床中，ToR 交换机配置了 25% 冗余上行链路，部分交换机超过一半的**冗余**链路失效时，多组双节点对同时通信的 all-reduce 带宽显著下降（这是掩盖机制的示例，不是通用触发阈值）；HBM 行重映射 >10 次的 GPU 端到端回归概率高 77.8%（[§2.2，印刷页 837–838](https://www.usenix.org/conference/atc24/presentation/xiong)）；OCP 白皮书则指出 AI 系统固有的 fault-masking 行为会掩盖 SDC、推迟或阻止其被发现（[执行摘要 p.3 与 §3.3 p.10](https://www.opencompute.org/documents/sdc-in-ai-ocp-whitepaper-final-pdf)）。两类掩盖都使“没有报警”不能推出“没有问题”。

## 被动监控的盲区与主动校验的覆盖边界

Meta 论文的排查案例显示：肇事机器的系统事件日志、内核日志全部干净，“从系统健康监控角度看没有任何失败症状”（[§5–§6](https://arxiv.org/abs/2102.11245v1)）。原因层面，论文指出 ECC 主要保护 SRAM，CPU 内并非所有数据通路和功能块都有同等保护，因此 SDC 率高于软错误模型的预测（§1–§2）。

由此得出的边界要分三层，不能一概而论：

- **被动证据不覆盖**：日志、事件和健康摘要依赖错误被报告，SDC 的定义就是没有这样的报告通道；[设备健康证据与检测边界](../01-hardware/health-evidence.md)中的被动字段确实覆盖不到这一类。
- **主动结果校验可以检出**：同一篇论文的检测机制正是用特定计算与已知参考值比较来发现 SDC（[§7 Detection Mechanisms](https://arxiv.org/html/2102.11245v1)）——下面的检测方法表中的 reproducer、fleet 筛查和 canary 都属于这一类。被动日志缺告警不等于主动校验也无法检出。
- **一次 PASS 不等于无 SDC**：主动测试的覆盖取决于输入、执行路径和触发条件；某个具体测试套件（如任一 DCGM/MindX 测试）能否检出当前故障事先不能保证，未触发不等于不存在。

同理，OCP 白皮书把故障结局分为 benign、fault corrected、DUE（detected unrecoverable error）与 SDC 四种（图 1，p.8）——只有落到 SDC 这一类的才需要本节的判定方法；能被硬件报告或纠正的错误属于健康证据范畴。

## 判定与检测方法：证据强度分层

| 方法 | 机制 | 证据强度与代价 | 来源 |
|---|---|---|---|
| 目标化 reproducer | 把失败案例逐步缩减为最小可复现输入（Meta 案例从 43 万行 JIT 汇编缩到 60 行测试） | 强证据（同核同输入必现），但依赖已有嫌疑样本 | Meta 论文 §5、§5.3 |
| fleet 周期筛查 | 维护窗口或周期调度的独立测试（OCP：45–60 天覆盖、分钟级测试） | 覆盖慢、与负载争窗口 | OCP §5.1（p.15–16） |
| 与负载共置的迷你测试 | 毫秒–秒级测试随生产负载运行，数天覆盖全 fleet | 覆盖快、单点开销小 | OCP §5.1 |
| 分析法 | 按核心统计应用异常分布反推嫌疑硬件 | OCP 记录比测试法多检出 41%（特定 fleet 观察） | OCP §5.1 |
| 确定性重放 | 相同输入重跑比对，Google Gemini 规模下配合空闲机扫描与热备定位 SDC | 强，但要求可重放性与额外容量 | OCP §5.1.4.1（p.19） |
| 冗余与一致性校验 | 空间/时间/信息冗余、端到端完整性校验、整数剩余校验、ABFT | 分类法存在；代价随冗余度增长（Meta §8.1 承认成本问题） | OCP §5.2 目录（正文未读）、Meta §8 |
| 不变量与 canary 校验 | 对已知答案的输入周期校验；训练侧观察 NaN 传播与梯度方差污染两种发散模式 | 中等，依赖校验点设计 | OCP §5.1.1（p.16–17） |

OCP 记录的覆盖率事实：周期筛查与共置测试的检出集合约 70% 重叠——单一手段不足以覆盖（§5.1，p.15–16）。Gemini 的规模事实：该规模下 SDC 每 1–2 周影响一次训练（§5.1.4.1，p.19）——这是特定规模的一手观察，不是通用发生率。

## 判定之前先扣除数值噪声背景

把“结果不一致”判为硬件 SDC 之前，必须先排除软件与数值语义的合法差异。PyTorch 2.6 文档支持的边界：

- 浮点加法/乘法不满足结合律，PyTorch 不保证数学等价的计算逐位相同，也不保证跨 release/commit/平台一致；**CPU 与 GPU 即使输入逐位相同、控制随机源后结果仍可能不同**（[numerical accuracy 开篇](https://docs.pytorch.org/docs/2.6/notes/numerical_accuracy.html)）。
- batched 与逐元素、整张量与切片的计算不保证逐位一致；linalg 对病态输入可能静默返回错误结果（软件层静默错误，与硬件 SDC 区分开）。
- TF32、FP16/BF16 降精度累加等开关会改变数值结果——跨平台/跨配置比对前必须固定。
- 完全可复现不保证跨 release/commit/平台，即使同 seed（[randomness 开篇](https://docs.pytorch.org/docs/2.6/notes/randomness.html)）。
- `assert_close` 的判据是 `|actual−expected| ≤ atol + rtol·|expected|`，省略时按 dtype 取默认容差（如 float32 为 rtol 1.3e-6/atol 1e-5，bfloat16 为 1.6e-2/1e-5）；这些默认值是经验值，不是硬件正确性保证（[testing.html #torch.testing.assert_close](https://docs.pytorch.org/docs/2.6/testing.html#torch.testing.assert_close)）。

因此合规的判定流程是：固定 dtype/开关/输入 → 用任务约定的容差比对而非判等（精确整数、不变量或校验和按各自契约比较）→ 排除已知数值语义后的完整性异常即可进入 SDC **候选**。稳定复现、确定性重放、迁移到其他设备、冗余对比和设备关联用于**增强或削弱**假设，而不是入口门槛——间歇性故障只在特定运行条件下触发，早期可能尚无稳定复现（OCP §3.2.1，p.9），不能据此排除怀疑。反过来，超出容差也不自动等于硬件故障：软件、数据、算法的替代解释保留到定位证据闭合为止。这与[GPU→NPU 精度差异诊断](../06-training/gpu-npu-precision-difference-triage.md)共用同一套容差纪律。

## 适用边界

- Meta 论文明确以数据中心 CPU 为主；“适用于加速器”是作者的外推陈述，不是实测。GPU/NPU 的 SDC 发生率不能从该论文推出。
- SuperBench 的灰色退化是性能域概念，其 Azure 数字（77.8%、22.61× MTBI 等）来自特定集群与仿真，不外推为通用阈值；22.61× 明确是仿真而非生产 A/B。
- OCP 白皮书已读范围为 p.1–19/29；检测分类法（§5.2/§5.3）与开放问题（§6）的细节未读，本文只引用目录级分类名。
- “SDC 随温度/电压/频率间歇激活”在 OCP §3.2.1（p.9）是机制性陈述（非新实测）；Meta v1 论文只把它列为待研究方向，不能引用 v1 支持该结论。
- 本文没有 NPU 侧的 SDC 公开一手证据；昇腾或其他 NPU 平台的判定路径需各自来源。

## 常见误解

- **“健康检查全绿 = 计算正确”**：被动日志与健康摘要不覆盖 SDC（没有报错通道）；主动结果校验可以检出部分 SDC，但其覆盖取决于输入、执行路径与触发条件，一次 PASS 同样不排除全部 SDC。
- **“ECC 存在 = 数据通路全覆盖”**：ECC 主要保护 SRAM，覆盖不完整是 SDC 率高于软错误模型的原因之一。
- **“跨平台结果不同 = 硬件有 SDC”**：浮点非结合性与合法实现差异是背景噪声，须先用容差纪律扣除。
- **“性能退化和计算错误是一回事”**：灰色退化（变慢）与 SDC（算错）分属性能与正确性两个维度，见[可靠性维度与故障域](dimensions-and-failure-domains.md)。
- **“一次 canary 通过 = 硬件无 SDC”**：Meta 记录同一检查运行六个月后才失败的磨损案例（OCP §5.0，p.15）；单次通过只是当次证据。

## 例子与相关知识

一个合规的怀疑链：训练 loss 出现不可解释的偏差 → 先按[精度差异诊断](../06-training/gpu-npu-precision-difference-triage.md)扣除配置与数值噪声 → 差异绑定特定节点/核且同输入必现 → 构造最小 reproducer → fleet 内同型硬件筛查。相关方法入口：[证据与假设](evidence-and-hypotheses.md)、[设备健康证据](../01-hardware/health-evidence.md)。

## 来源与待确认问题

- [Silent Data Corruptions at Scale, arXiv:2102.11245v1](https://arxiv.org/abs/2102.11245v1)（仅 v1，无后续版本；ar5iv 全文节号定位）。
- [SuperBench, USENIX ATC 2024](https://www.usenix.org/conference/atc24/presentation/xiong)（已读印刷页 835–844；845–850 未读）。
- [OCP 白皮书 Silent Data Corruption in AI（2025-08-27，CC BY-SA 4.0）](https://www.opencompute.org/documents/sdc-in-ai-ocp-whitepaper-final-pdf)（已读 p.1–19/29）。
- [PyTorch 2.6 数值精度](https://docs.pytorch.org/docs/2.6/notes/numerical_accuracy.html)、[可复现性](https://docs.pytorch.org/docs/2.6/notes/randomness.html)、[testing.html 的 assert_close](https://docs.pytorch.org/docs/2.6/testing.html#torch.testing.assert_close)。
- 逐条主张与读取范围见[第九批静默错误来源记录](../../docs/research/batch-09-silent-error-sources.md)。
- 待确认：检测策略的量化原始论文 arXiv:2203.08989（未读）；LLM 训练侧 SDC 一手研究（arXiv:2502.12340，未读）；OCP §5.2 之后的检测细节；NPU 侧一手证据。
