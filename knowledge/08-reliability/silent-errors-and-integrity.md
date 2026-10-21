---
id: reliability.silent-errors-and-integrity
title: 静默错误与计算完整性判定
type: concept
domain: reliability
status: draft
platforms: [generic]
source_refs:
  - src.arxiv.sdc-at-scale-v1
  - src.arxiv.sdc-detection-wild-2203
  - src.acl.sdc-llm-training-2502
  - src.ocp.sdc-in-ai-2025
  - src.usenix.superbench-atc24
  - src.pytorch.numerical-verification-2.6
  - src.ascend.msprobe-26.2.0.b110
  - src.huawei.hdk-26.1x-a2-npu-smi-2026-10-08
  - src.huawei.hdk-26.1x-a2-dcmi-ecc
  - src.ascend.faultdiag-v26.1.1
updated_at: "2026-10-21"
summary: 定义静默错误（SDC）与相邻概念，给出被动监控盲区、Fleetscanner/Ripple 的检测量化对比、真实不健康节点上 LLM 训练三层级影响与 ABFT 检测失败证据、字节/校验和/冗余/重算各检测方法的覆盖与边界，以及 NVIDIA/AMD/Ascend 逐平台校验与证据清单；NPU SDC 发生率保持 unknown。
related_ids:
  - reliability.dimensions-and-failure-domains
  - reliability.evidence-and-hypotheses
  - reliability.fault-models-and-propagation
  - reliability.test-design-and-coverage
  - hardware.health-evidence
  - training.gpu-npu-precision-difference-triage
verification:
  status: source_checked
  evidence_refs:
    - src.arxiv.sdc-at-scale-v1
    - src.arxiv.sdc-detection-wild-2203
    - src.acl.sdc-llm-training-2502
    - src.ocp.sdc-in-ai-2025
    - src.usenix.superbench-atc24
    - src.pytorch.numerical-verification-2.6
    - src.ascend.msprobe-26.2.0.b110
    - src.huawei.hdk-26.1x-a2-npu-smi-2026-10-08
    - src.huawei.hdk-26.1x-a2-dcmi-ecc
  notes: "本批（Batch 30）补读并节级核对：arXiv:2203.08989v1 全文（检测量化 §3–§6 与表 1）、arXiv:2502.12340v1（ACL 2025 正式版）全文含附录 D（三层级实验与 ABFT 失败证据）、OCP 白皮书 §5.2–§6 与 §5.4（此前仅读至 §5.1；文件重核为 30 页）、msprobe 固定 tag 比对文档、npu-smi/DCMI ECC 官方页。未做任何硬件测试或故障注入；论文数字均限于其声明的平台与缺陷族范围。"
---

# 静默错误与计算完整性判定

## 定义与要解决的问题

**静默错误（silent data corruption, SDC）**：计算结果错误，但没有任何系统事件或错误日志指示这次误算。Meta 的定义性案例是“2x3 得 5”；其后续研究给出应用侧后果的量化例子——`(1.1)^53` 算成 0（正确值 156.24），导致数据库缺行与应用数据丢失，且日志全程干净（[arXiv:2102.11245v1 §1](https://arxiv.org/abs/2102.11245v1)、[arXiv:2203.08989 §1](https://arxiv.org/abs/2203.08989)）。它要回答的问题是：当所有监控都“绿”的时候，凭什么相信计算结果是对的。

三个相邻但不同的概念先分开：

| 概念 | 域 | 表现 | 主要证据来源 |
|---|---|---|---|
| 静默错误（SDC） | 结果正确性 | 输出错误、无报错 | Meta CPU SDC 系列论文、OCP AI 白皮书、AWS/Harvard LLM 训练研究 |
| 灰色退化（gray failure / fail-slow） | 性能稳定性 | 渐进变慢、冗余掩盖局部退化 | SuperBench（Azure GPU 集群） |
| 软件/算法层的静默错误结果 | 数值语义 | 病态输入下 linalg 静默返回错误结果等 | PyTorch 数值文档 |

OCP 白皮书把单个故障位的结局分为四类：benign（无影响）、fault corrected（被 ECC 类机制纠正）、DUE（检出但不可纠正，fail-stop）与 SDC（未触发硬件检测且产出错误结果）；只有最后一类需要本文的判定方法，能被报告或纠正的错误属于健康证据范畴（图 1，p.8）。

## 为什么被动监控检不出、一次测试也不够

被动证据不覆盖 SDC 是定义性的：Meta 排查案例中肇事机器的系统事件与内核日志全部干净（[§5–§6](https://arxiv.org/abs/2102.11245v1)）；OCP 白皮书指出 AI 系统固有的 fault-masking 会进一步推迟或阻止发现（执行摘要 p.3）。反向边界同样成立：**主动结果校验可以检出部分 SDC，但一次 PASS 不等于无 SDC**——覆盖取决于输入、执行路径与触发条件。

Meta 后续论文给出 SDC 难以一次测全的四个机制性原因（[§4](https://arxiv.org/abs/2203.08989)，约 3 年 fleet 观察归纳）：

1. **数据随机化**：损坏 CPU 上多数计算正确，特定位模式子集必错（3×5=15 但 3×4=10），测试状态空间大；
2. **电气变化**：频率/电压/电流组合变化会加速错误出现，一个工作点正确不保证所有工作点正确；
3. **环境变化**：机房热点与季节温差影响电压/频率余量（数据中心 A 正确、数据中心 B 算错是可能的）；
4. **生命周期变化**：硅随时间退化，可能早于传统浴盆曲线；论文记录一台设备同一计算序列每日重复、6 个月后才失败。

由此得出的可操作结论：对 SDC 的保护只能来自**反复测试与持续改进的检测**，而不是一次验收；这为下面的量化对比提供了前提。

## 检测策略的量化对比：Fleetscanner 与 Ripple

Meta 在数百万台规模 fleet 上比较了两类策略（[arXiv:2203.08989 §5–§6 与表 1](https://arxiv.org/abs/2203.08989)；数字限“某 CPU 缺陷族的大部分缺陷、覆盖 fleet 的很大比例”这一研究范围）：

| 维度 | Fleetscanner（生产外） | Ripple（生产中共置） |
|---|---|---|
| 运行时机 | 搭固件升级/内核升级/重装/维修等维护窗口的排空（drain）阶段，机器空闲时执行 | 与生产负载共置，毫秒级间隔持续执行（always-on） |
| 单次测试时长 | 分钟级 | 数百毫秒以内 |
| 规模 | 生命周期约 6800 万次测试、约 40 亿 fleet 秒 | 每月约 25 亿次测试、约 1 亿 fleet 秒 |
| 对该缺陷族的覆盖 | 检出 SDC 的 93%，其中 23% 为 Ripple 达不到的独有覆盖 | 共同覆盖部分 15 天达到 70%；另有 7% 独有覆盖（Ripple 总覆盖 77%） |
| 达到同等覆盖时间 | 约 5–6 个月覆盖全 fleet | 新特征（signature）约两周内可扩到全 fleet |
| 代价 | 占用维护窗口与算力（“昂贵但重要”） | 按负载类型测量 footprint tax 并压到阈值下；上线前经 shadow A/B 测试保护 |

两条结论直接可用：**单一手段覆盖不足**（OCP 白皮书对周期筛查与共置测试也记录约 70% 检出集合重叠，§5.1 p.15–16）；**检出手段会改变被测系统**——Ripple 的共置测试需要按负载调缩放、测 footprint tax，本身就说明检测有成本与副作用。覆盖比例随缺陷类型变化，不可把 93%/77% 当作通用保证。

## 训练中的传播：真实不健康节点上的三层级证据

AWS/Harvard 的研究（ACL 2025；[arXiv:2502.12340](https://arxiv.org/abs/2502.12340)）首次用**真实** SDC 节点（被云平台 fleet 管理压力测试筛出的 15 台“不健康”节点，其中部分确认是训练使用中由健康转不健康）量化 SDC 对 LLM 训练的影响。方法要点：XLA 编译器保证指令序确定，先验证任意两台健康节点结果完全一致，再配对健康/不健康节点，用计算同步（lock-step 并行）与参数同步在三个层级隔离影响——该同步机制假设通信本身不产生 SDC（依据：节点通过集合通信压力测试、同步原语不经计算单元、网络有奇偶/ECC 保护），这是论文声明的假设而非本文可独立的结论。

| 层级 | 度量 | 观察结果（限其实验设置：单节点张量并行、16/32 层 decoder） |
|---|---|---|
| 子模块计算（前向/反向的 attention、FFN） | mismatch frequency（不一致元素比例）、mismatch severity（非零元素相对误差均值，跨层取最大） | 节点间差异大：最差节点 fwd/attn 平均频率 2.89e-2，另一些节点该设置为 0；severity 可达三位数甚至 1e12 量级（如 Node 9 bwd/ffn 9.63e+12）；发生不均匀，呈尖峰（训练最初几步系统整体利用率高时更高） |
| 单个 optimizer step 的梯度 | 梯度差 L2 范数与真值梯度范数之比（WCNTS，取最差） | 最大 5.1%（Node 11）：单步内 SDC 噪声相对梯度本身通常较小 |
| 训练周期（预训练＋微调） | loss 曲线、参数差（L2）、微调精度与分歧率 | **loss 几乎重合但参数持续漂移到不同极小值**；漂移速率各节点相近，作者归因于损失面尖锐、SDC 充当触发器；微调分歧率不大于换随机种子的数据重排；个别节点出现 loss 尖峰，其中 Node 6 末期尖峰致 CosmosQA 测试精度为 0；是否出现尖峰与任务损失面相关 |

对判定实践的三条含义：

1. **“loss 正常”不能排除 SDC**：Node 10 的子模块与梯度持续受扰，但预训练与微调 loss 与健康节点完全一致——SDC 可能在尖峰出现前已影响训练一段未知时间（论文 §7.1）。
2. **观测会改变发生率**：同步/监控本身降低加速器利用率，从而降低 SDC 发生频率（同一节点在计算同步下每 4000 步才偶发、在参数同步下每步都有梯度差）。“加探针后没再复现”不能反推缺陷消失。
3. **错误传播有条件**：早期参数上的错误可能被后续更新覆盖，关键层晚期错误可能发散（OCP §5.4 对迭代式训练的同型讨论）；影响程度依赖模型结构与训练阶段，不存在统一阈值。

## 检测方法分层：覆盖、成本与假阴性/误报

综合 OCP §5.2–§5.3 的分类法（本批已读全文）与上述论文的实测证据：

| 方法 | 机制与来源 | 覆盖与成本 | 已知假阴性/误报与盲区 |
|---|---|---|---|
| 目标化 reproducer | 缩减失败案例为最小可复现输入（Meta 43 万行 JIT 汇编缩到 60 行测试） | 强证据（同核同输入必现）；依赖已有嫌疑样本 | elusive 触发条件可能无法系统复现 |
| fleet 周期筛查 / 共置迷你测试 | 见上一节 Fleetscanner/Ripple 与 OCP §5.1（45–60 天窗口 vs 数天全 fleet） | 互有独有覆盖，需组合 | 覆盖随缺陷族变化；与负载/维护争资源 |
| 确定性重放＋对照 | 相同输入重跑比对；Gemini 规模配合空闲机扫描与热备上的 SDC 扫描器 | 强，但要求可重放性与额外容量 | 非确定性训练需先固定执行（如 XLA 指令序），且这有性能代价 |
| 端到端完整性校验（信息冗余） | 在流水线多阶段存取并校验 checksum/哈希（OCP §5.2.1） | 低成本，适合多节点通信与存储层 | 只检出被校验对象的变化；需要后续纠正/回滚机制配套 |
| 复制与一致性校验（空间冗余） | 多副本/影子模型比对输出；对关键层冗余执行（OCP §5.2.2） | 检出有效，但开销在规模上可能不可行 | 副本间共享依赖时对共同原因失效（见[相关故障案例](correlated-failure-source-case.md)） |
| 整数剩余校验 | 模小素数（mod 3/7）并行计算验证算术结果（OCP §5.2.3） | 计算便宜，适合整数/量化数据与算术密集流水线 | 面向整数运算；浮点张量语义下不直接适用 |
| ABFT / 校验和矩阵乘 | 把校验和编入算法（矩阵乘、attention 层）实现前向检错（OCP §5.3.2） | 有望低开销 | **实测反例**：ACL 2025 研究在 float32、全部线性层上加 checksummed matmul，15 台已知不健康节点中仅 Node 14 被频繁标出；作者给出三条解释——扰动落在浮点误差界内使校验阈值不触发、ABFT 开销降低利用率从而降低 SDC 发生率、SDC 可能发生在矩阵乘之外（附录 D.3）。且其误差界按 IEEE-754 fp32+ 单位舍入推导，**bf16 下直接套用会在健康节点上假阳性**（附录 D.4）。结论：ABFT 不是“装了就能检出”，精度/召回与数据类型、算子覆盖强相关 |
| 冗余重算 / 影子数据并行副本 | 每 step 用影子副本对选定数据并行 rank 重算并在梯度 all-reduce 时比对（ACL 2025 §7.2 建议；与 Gemini 热备扫描器同思路） | 论文认为这是当前“可靠检出的最好方案” | 等于为被覆盖对象付一份计算；只覆盖被选中的 rank/对象 |
| checkpoint/重启（时间冗余） | 检出后回滚到已保存状态（OCP §5.3.1） | 恢复手段而非检测手段 | 提频增存储/IO 与编排开销、压低运行 goodput；epoch 末才存不够 |

选择原则与[统一测试方法](test-design-and-coverage.md)共用：先声明要覆盖的故障模型与对象，再按覆盖×成本×假阴性/误报组合，不默认任一方法单打独斗。

## 判定之前先扣除数值噪声背景

把“结果不一致”判为硬件 SDC 之前，必须先排除软件与数值语义的合法差异。PyTorch 2.6 文档支持的边界：

- 浮点加法/乘法不满足结合律，PyTorch 不保证数学等价的计算逐位相同，也不保证跨 release/commit/平台一致；**CPU 与 GPU 即使输入逐位相同、控制随机源后结果仍可能不同**（[numerical accuracy 开篇](https://docs.pytorch.org/docs/2.6/notes/numerical_accuracy.html)）。
- batched 与逐元素、整张量与切片不保证逐位一致；linalg 对病态输入可能静默返回错误结果（软件层静默错误，与硬件 SDC 区分）。
- TF32、FP16/BF16 降精度累加等开关会改变数值结果——跨平台/跨配置比对前必须固定。
- 完全可复现不保证跨 release/commit/平台，即使同 seed（[randomness 开篇](https://docs.pytorch.org/docs/2.6/notes/randomness.html)）。
- `assert_close` 判据是 `|actual−expected| ≤ atol + rtol·|expected|`，默认容差按 dtype（float32 rtol 1.3e-6/atol 1e-5；bfloat16 1.6e-2/1e-5），是经验值不是硬件正确性保证（[testing.html](https://docs.pytorch.org/docs/2.6/testing.html#torch.testing.assert_close)）。

因此合规的判定流程：固定 dtype/开关/输入 → 用任务约定容差比对而非判等 → 排除已知数值语义后的完整性异常进入 SDC **候选**。稳定复现、确定性重放、迁移到其他设备、冗余对比用于**增强或削弱**假设，不是入口门槛——间歇故障只在特定条件下触发，早期可能没有稳定复现（OCP §3.2.1 p.9）；反过来，超出容差也不自动等于硬件故障，软件/数据/算法解释保留到定位证据闭合。与[GPU→NPU 精度差异诊断](../06-training/gpu-npu-precision-difference-triage.md)共用同一套容差纪律。

## 平台证据清单：NVIDIA / AMD / Ascend 按版本记录

**NVIDIA**：被动侧 DCGM 字段与主动诊断（diagnostic 四级 run level、各插件前提与判据）见[设备健康证据](../01-hardware/health-evidence.md)与[节点验收](../01-hardware/node-acceptance-triage.md)；Xid 动作表与 field diagnostic 的 RMA 地位见 GPU Node Triage（已登记来源）。这些是**有信号错误**的检测；对其 SDC 检出覆盖率，本库无公开量化来源，不外推 Meta CPU 数字。

**AMD**：ROCm/RCCL 侧观测与验证口径见[RCCL 运行时与验证](../03-communication/rccl-runtime-and-verification.md)；SDC 发生率同样无公开充分材料，保持 unknown。

**Ascend（按固定版本记录）**：

| 证据 | 精确内容 | 边界 |
|---|---|---|
| ECC 计数（npu-smi，HDK 26.1.x A2 树） | `npu-smi info -t ecc -i id` 输出 `HBM Single/Double Bit Error Count`（当前）、`Aggregate Total Err Cnt`（生命周期累计）、`Isolated Pages Count` 与 `Next-Isolated Pages Count`（单比特两项为预留恒 0；多比特待隔离取值 0–64，经复位/重启/上下电刷新为已隔离数）；计数上限 4294967295；支持矩阵含 Atlas 900 A2 PoD/800T A2 等，物理机 root | **被 ECC 检出并计数的是 signaled 错误**（OCP 分类里的 corrected/DUE 类），不构成 SDC 检出或发生率证据 |
| DCMI 接口（HDK 26.1.x A2 树） | `dcmi_get_device_ecc_info(card_id, device_id, input_type, ...)`，`input_type` **仅支持 `DCMI_DEVICE_TYPE_HBM`**；返回 `enable_flag` 与单/多比特当前计数（**系统重启清零**）、生命周期累计、隔离页数；文档注明“查询到多比特错误，需要进行相关问题定位和处理” | 同上；SRAM/DDR 等组件类型该接口不支持 |
| 算子/张量级精度比对（msprobe，MindStudio Probe tag `MindStudio_26.2.0.B110_001`） | dump（config.json）→ 精度比对 → 分级可视化三步；指标含 Cosine、EucDist、MaxAbsErr、MaxRelativeErr、千分之一/千分之五误差比例、统计量（max/min/mean/L2）相对误差、CRC-32、`Requires_grad Consistent`；官方口径 Cosine“实际可接受阈值为大于 0.99”、MaxAbsErr“小于 0.001”，千分位比例“仅作为精度下降趋势的参考，并不参与计算精度是否通过的判定”；error 标记规则如 input 千分之一比例 >0.9 且 output <0.6、norm 相对误差 input <0.1 且 output >0.5、梯度不一致、dtype/shape 不一致；`_reduce_scatter_base` 等占位输入 API 与 `empty`/`to` 等冗余 API 有豁免规则 | **离线比对工具的判定规则**，阈值是官方经验口径；文档明示 NPU 与 CPU/GPU 差异随模型执行不断累积，同一 API 可能因输入差异大到无法比对——比对通过不等于无 SDC，比对异常也需先走容差纪律 |
| 日志规则诊断（Ascend FaultDiag，mind-cluster v26.1.1 固定 commit） | 日志清洗后 `ascend-fd diag` 输出根因节点分析（按 HCCL 报错定位根因服务器/首错节点/根因节点链）与故障事件分析（按故障知识图谱给故障分类/名称/建议方案/关键日志/传播链）；`-p` 可诊断性能劣化（计算降频、CPU 抢占、网络拥塞） | 规则匹配产出的是**候选假设与建议**，不构成根因证明；本库不将其输出当作 SDC 证据 |

**NPU SDC 资料可得性边界（本批检索范围与结论）**：本批检索范围覆盖 hiascend HDK 版本化文档树（npu-smi/DCMI/健康管理）、CANN 文档入口、msprobe 仓库固定 tag、mind-cluster 固定 commit 的 FaultDiag 组件文档。结果：公开材料能支撑 ECC 计数（有信号错误）、离线精度比对与日志规则诊断；**未找到**昇腾/NPU 的 SDC 发生率统计、fleet 级 SDC 扫描实践或算力校验保障的公开一手文档。因此 NPU 的 SDC 发生率、检测覆盖与保障能力在本库保持 **unknown**，不以 CPU（Meta：约千分之一硅设备）或 GPU（Llama 3 快照：意外中断的 1.4% 归因 SDC）研究代填；后两者也各自限其平台与统计口径。

**故障注入的地位**：注入（如位翻转、算子输出扰动）只能**评估检测方法的覆盖与响应**（见[统一测试方法](test-design-and-coverage.md)），合成注入的检出不构成真实硬件 SDC 发生证据；ACL 2025 论文同样把“注入研究可能与生产 SDC 不同”列为既有工作局限（§2.1）。

## 适用边界

- Meta 两篇论文均为数据中心 **CPU** 证据（第二篇明确限某 CPU 缺陷族）；“适用于加速器”是 OCP 白皮书的多厂商共识性讨论，不是等量实测。GPU 数字（Llama 3 Table 5）限其 54 天快照与归因口径（“confirmed or suspected”）。
- ACL 2025 研究限其声明范围：15 台临时持有的不健康节点、单节点张量并行、同步机制降低 SDC 发生率的影响未消除、loss 尖峰只在微调中观察到。数字不可外推为“训练遇到 SDC 必然如何”。
- SuperBench 的灰色退化是性能域概念，其 Azure 数字（77.8%、22.61× MTBI 等）限特定集群与仿真。
- OCP 白皮书本次已读至文末（文件 30 页；此前登记按 29 页记，已更正）；§5.2/§5.3 的分类法正文已读，但其引用的 goodput 论文见[可靠性指标](reliability-metrics-and-recovery-loss.md)。
- 本文没有任何本地硬件测试、注入或生产观测；所有数字是来源方在其环境的一手观察。

## 常见误解

- **“健康检查全绿 = 计算正确”**：被动日志不覆盖 SDC；主动校验也只能覆盖其输入与路径覆盖到的部分。
- **“ECC 存在 = 数据通路全覆盖 / ECC 计数非零才有问题”**：ECC 主要保护 SRAM/HBM 等存储结构且覆盖不完整（Meta §1–§2）；Ascend 侧 ECC 计数是 signaled 错误的证据，ECC 未报不能推出计算正确。
- **“ABFT/校验和装上就能检出 SDC”**：见上表实测反例——真实不健康节点上 float32 ABFT 大多不触发，bf16 直接套用还会假阳性。
- **“loss 正常 = 训练未受 SDC 影响”**：真实节点证据显示参数可以在 loss 几乎重合的情况下持续漂移到不同极小值。
- **“跨平台结果不同 = 硬件有 SDC”**：浮点非结合性与合法实现差异是背景噪声，先走容差纪律。
- **“一次 canary/筛查通过 = 该设备无 SDC”**：数据随机化、电气/环境/生命周期变化使检测必须反复进行（Meta §4）；OCP 记录同一检查六个月后才失败的磨损案例（§5.0 p.15）。
- **“性能退化和计算错误是一回事”**：灰色退化与 SDC 分属性能与正确性两维，见[可靠性维度与故障域](dimensions-and-failure-domains.md)。

## 例子与相关知识

一个合规的怀疑链：训练 loss 出现不可解释偏差 → 按[精度差异诊断](../06-training/gpu-npu-precision-difference-triage.md)扣除配置与数值噪声 → 差异绑定特定节点/核且同输入必现 → 构造最小 reproducer → 用确定性重放或影子副本比对增强/削弱 → fleet 内同型硬件筛查。相关入口：[证据与假设](evidence-and-hypotheses.md)、[故障模型与传播](fault-models-and-propagation.md)、[统一测试方法](test-design-and-coverage.md)（注入评估检测覆盖）、[可靠性指标](reliability-metrics-and-recovery-loss.md)（SDC 造成的有效产出损失口径）。

## 来源核对范围

- [Silent Data Corruptions at Scale, arXiv:2102.11245v1](https://arxiv.org/abs/2102.11245v1)：定义、干净日志盲区、fleet 检测机制（§1/§5/§7/§8；第九批已核）。
- [Detecting silent data corruptions in the wild, arXiv:2203.08989v1](https://arxiv.org/abs/2203.08989)（CC BY-NC-ND 4.0）：本批全文核读——硅测试漏斗（§3）、四类触发因素与 6 个月退化实验（§4）、Fleetscanner/Ripple 机制（§5）、表 1 与 93%/23%/7%/15 天/5–6 个月等量化（§6）。仅归纳，不改编再分发。
- [Understanding Silent Data Corruption in LLM Training, ACL 2025（arXiv:2502.12340v1）](https://aclanthology.org/2025.acl-long.996/)：本批全文核读含附录 D——fleet 管理筛选手法（§3.1）、三层级实验与全部表值（§4–§6）、静默性论证（§7.1）、ABFT 实测失败与三条解释、bf16 假阳性（§7.2、附录 D.1–D.4）、局限（§9）。
- [OCP 白皮书 Silent Data Corruption in AI（2025-08-27，CC BY-SA 4.0）](https://www.opencompute.org/documents/sdc-in-ai-ocp-whitepaper-final-pdf)：第九批读 p.1–19；本批补读 §5.2.1–§5.2.3、§5.3.1–§5.3.2、§5.4、§6 至文末（文件 30 页）。
- [PyTorch 2.6 数值精度/可复现性/assert_close](https://docs.pytorch.org/docs/2.6/notes/numerical_accuracy.html)（第九批已核）。
- Ascend：npu-smi ECC 页与 DCMI `dcmi_get_device_ecc_info`（HDK 26.1.x A2 树，本批逐字段核读）；msprobe 固定 tag 的 PyTorch 精度比对文档（指标、阈值、error/warning 标记与豁免规则逐条核读）；FaultDiag v26.1.1 固定 commit 的概述/故障诊断/日志清洗文档。
- 逐条主张与读取范围见[第三十批 T08-04 来源记录](../../docs/research/batch-30-t08-04-sources.md)。
- 待确认：NPU 侧 SDC 发生率与 fleet 级检测实践的一手材料（当前 unknown）；Meta 2203.08989 后续是否公开更新版本（abs 页 v1 为最新）；ACL 2025 研究的不健康节点在维修归队后的复测结果（论文未含）。
