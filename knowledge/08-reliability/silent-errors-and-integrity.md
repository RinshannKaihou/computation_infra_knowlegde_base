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
  - src.arxiv.llama3-infrastructure
  - src.ocp.sdc-in-ai-2025
  - src.usenix.superbench-atc24
  - src.pytorch.numerical-verification-2.6
  - src.ascend.msprobe-26.2.0.b110
  - src.huawei.hdk-26.1x-a2-npu-smi-2026-10-08
  - src.huawei.hdk-26.1x-a2-dcmi-ecc
  - src.ascend.faultdiag-v26.1.1
  - src.pytorch.parallel-training-state-2.6
  - src.arxiv.sdc-llm-training-2502-v1
  - src.nvidia.dcgm-v3.3.9
  - src.rocm.rocm-systems-therock-10.1
updated_at: "2026-10-21"
summary: 定义静默错误（SDC，相对硬件原生检测的静默）与相邻概念，分层说明日志盲区、应用间接症状与主动结果校验的边界；给出 Fleetscanner/Ripple 检测量化（等价检出与部署覆盖分列）、真实不健康节点上的训练传播三层级证据（activation/梯度/optimizer 状态/参数/checkpoint 传播链）与 ABFT 检测失败反例，比较字节/元数据/算子校验、冗余重算、差分/不变量与任务质量检测；NVIDIA/AMD/Ascend 按版本记录观测与校验能力，NPU SDC 发生率保持 unknown。
related_ids:
  - reliability.dimensions-and-failure-domains
  - reliability.evidence-and-hypotheses
  - reliability.fault-models-and-propagation
  - reliability.test-design-and-coverage
  - hardware.health-evidence
  - hardware.node-acceptance-triage
  - training.gpu-npu-precision-difference-triage
  - training.checkpoint-state-consistency
  - data-storage.checkpoint-integrity-evidence
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
  notes: "本批（Batch 30）补读并节级核对：arXiv:2203.08989v1 全文（§3–§6 与表 1）、LLM 训练 SDC 研究两个版本（ACL 2025 正式版＝登记主修订；arXiv:2502.12340v1 全文用于附录定位，两版附录编号不同、正文引用按版本分列）、OCP 白皮书 §5.2–§6 至文末（文件 30 页）、msprobe 固定 tag 比对文档（docs 许可 CC BY 4.0 已核）、npu-smi/DCMI ECC 官方页、PyTorch 2.6 Adam 源码（optimizer 状态依赖）。未做任何硬件测试或故障注入；论文数字均限其声明的平台、缺陷族与实验设置。"
---

# 静默错误与计算完整性判定

## 定义与要解决的问题

**静默错误（silent data corruption, SDC）**：故障使系统产出错误结果，且**未触发硬件内置检测机制**——这是“静默”的精确含义（OCP 白皮书对故障位结局的分类：benign、fault corrected、DUE、SDC 四类中的最后一类，图 1 p.8；能被硬件报告或纠正的错误不属于 SDC，归健康证据范畴）。Meta 的定义性案例是“2x3 得 5”；其后续研究给出应用侧后果的量化例子——`(1.1)^53` 算成 0（正确值 156.24），导致数据库缺行与应用数据丢失，且系统事件与内核日志全程干净（[arXiv:2102.11245v1 §1](https://arxiv.org/abs/2102.11245v1)、[arXiv:2203.08989 §1](https://arxiv.org/abs/2203.08989)）。它要回答的问题是：当硬件检测没有报警的时候，凭什么相信计算结果是对的。

三个相邻但不同的概念先分开：

| 概念 | 域 | 表现 | 主要证据来源 |
|---|---|---|---|
| 静默错误（SDC） | 结果正确性 | 硬件检测未报、输出错误 | Meta CPU SDC 系列论文、OCP AI 白皮书、AWS/Harvard LLM 训练研究 |
| 灰色退化（gray failure / fail-slow） | 性能稳定性 | 渐进变慢、冗余掩盖局部退化 | SuperBench（Azure GPU 集群，[ATC 2024](https://www.usenix.org/conference/atc24/presentation/xiong)） |
| 软件/算法层的静默错误结果 | 数值语义 | 病态输入下 linalg 静默返回错误结果等 | PyTorch 数值文档 |

## “静默”分三层：不能一概而论

把“静默”无条件扩大成“什么都检不出”会同时高估和低估问题。分三层记录：

1. **硬件原生检测未触发是定义性的**：SDC 的分类位置就是“未被硬件错误检测机制报告”（OCP §3.1 p.8）。Meta 排查案例中肇事机器的系统事件与内核日志全部干净（[§5–§6](https://arxiv.org/abs/2102.11245v1)）；论文指出 ECC 主要保护 SRAM，CPU 内并非所有数据通路都有同等保护（§1–§2）。OCP 另指出 AI 系统固有的 fault-masking 会推迟或阻止发现（执行摘要 p.3）。
2. **应用间接症状仍然可用**：被动健康计数没有告警≠没有任何分析证据。OCP §5.1（p.16）记录基于应用异常统计与 kernel 例外行为分布反推嫌疑硬件的分析法（其 fleet 观察中比测试法多检出 41%，§5.1 p.15–16）——这类证据形成**候选**，不构成硬件报告。
3. **主动结果校验可以有限检出**：向被测对象施加已知输入并校验输出的测试（Meta 的 reproducer 与 fleet 筛查、OCP 记录的 canary/共置测试、DCGM diagnostic 里的显存写入-回读比对等）属于主动校验，可检出部分 SDC——但覆盖取决于输入、执行路径与触发条件，**一次 PASS 不等于无 SDC**。

推理纪律与第 2/3 层对应：**“没有报警”不能推出“没有问题”；反过来，主动测试未触发也不能反推缺陷不存在**（间歇触发条件可能未被覆盖）。

## 为什么一次测试不够：四个机制性原因

Meta 后续论文给出 SDC 难以一次测全的四个原因（[arXiv:2203.08989 §4](https://arxiv.org/abs/2203.08989)，约 3 年 fleet 观察归纳）：

1. **数据随机化**：损坏 CPU 上多数计算正确，特定位模式子集必错（3×5=15 但 3×4=10），测试状态空间大；
2. **电气变化**：频率/电压/电流组合变化会加速错误出现，一个工作点正确不保证所有工作点正确；
3. **环境变化**：机房热点与季节温差影响电压/频率余量（数据中心 A 正确、数据中心 B 算错是可能的）；
4. **生命周期变化**：硅随时间退化，可能早于传统浴盆曲线；论文记录一台设备同一计算序列每日重复、6 个月后才失败。

由此得出的可操作结论：对 SDC 的保护只能来自**反复测试与持续改进的检测**，而不是一次验收。OCP 记录的同一检查六个月后才失败的磨损案例（§5.0 p.15）与第 4 条同型。

## 检测策略的量化对比：Fleetscanner 与 Ripple

Meta 在数百万台规模 fleet 上比较了两类策略（[arXiv:2203.08989 §5–§6 与表 1](https://arxiv.org/abs/2203.08989)；研究范围限“某 CPU 缺陷族的一个较大子集、测试覆盖 fleet 的显著比例”。**共同比较基准**＝该研究在此缺陷族上观察到的失败集合（两方法合并检出的并集，非对未知全部缺陷的召回率）；下表各比例均以此为分母）：

| 维度 | Fleetscanner（生产外） | Ripple（生产中共置） |
|---|---|---|
| 运行时机 | 搭固件升级/内核升级/重装/维修等维护窗口的排空（drain）阶段，机器空闲时执行 | 与生产负载共置，毫秒级间隔持续执行（always-on） |
| 单次测试时长 | 分钟级 | 数百毫秒以内 |
| 规模 | 生命周期约 6800 万次测试、约 40 亿 fleet 秒 | 每月约 25 亿次测试、约 1 亿 fleet 秒 |
| 占该失败集合的比例 | 93%（其中 23% 为 Ripple 达不到的独有部分） | 77%（共同 70%＋独有 7%） |
| 达到**同一终点**（共同 70% 子集）的时间 | 约 5–6 个月 | 约 15 天 |
| 代价 | 占用维护窗口与算力（论文称“昂贵但重要”） | 按负载类型测量 footprint tax 并压到阈值下；上线前经 shadow A/B 测试保护 |

两项**不进入上表比较**的时间量（统计终点不同，单列）：Fleetscanner 按其节奏完成一次全 fleet 扫描约 5–6 个月（部署/扫描范围）；Ripple 把新发现的 signature 扩大部署到全 fleet 约 2 周（发布速度，非同等检出覆盖）。
两条结论直接可用：**单一手段覆盖不足**（23%/7% 互有独有；OCP 对周期筛查与共置测试也记录约 70% 检出集合重叠，§5.1 p.15–16）；**检出手段会改变被测系统**——Ripple 需要按负载调缩放、测 footprint tax，本身就说明检测有成本与副作用。覆盖比例随缺陷类型变化（论文 §6.3），93%/77% 不可当通用保证。

## 训练中的传播：真实不健康节点上的三层级证据

AWS/Harvard 的研究首次用**真实** SDC 节点（被云平台 fleet 管理压力测试筛出的 15 台“不健康”节点，其中部分确认是训练使用中由健康转不健康）量化 SDC 对 LLM 训练的影响。方法要点：XLA 编译器保证指令序确定，先验证任意两台健康节点结果完全一致，再配对健康/不健康节点，用计算同步（lock-step 并行）与参数同步在三个层级隔离影响——该同步机制假设通信本身不产生 SDC（依据：节点通过集合通信压力测试、同步原语不经计算单元、网络有奇偶/ECC 保护），这是论文声明的假设而非本文可独立的结论。版本定位：主体实验见 ACL 2025 正式版（[ACL 2025，pp. 20372–20394](https://aclanthology.org/2025.acl-long.996/)）；附录实验细节/结果/解释的节号引用 arXiv v1（[arXiv:2502.12340v1](https://arxiv.org/abs/2502.12340v1) 附录 D.1–D.4）——**两版附录编号不同**（ACL 版附录仅 D.1 解释与 D.2 低精度两节，实验在正文），引用按各自版本定位。

| 层级 | 度量 | 观察结果（限其实验设置：单节点张量并行、16/32 层 decoder） |
|---|---|---|
| 子模块计算（前向/反向的 attention、FFN） | mismatch frequency（不一致元素比例）、mismatch severity（非零元素相对误差均值，跨层取最大） | 节点间差异大：最差节点 fwd/attn 平均频率 2.89e-2，另一些节点该设置为 0；severity 可达三位数至 1e12 量级（Node 9 bwd/ffn 9.63e+12）；发生不均匀、呈尖峰（训练最初几步出现高峰——论文以“可能因初始化期间整体利用率更高”**解释**，属作者推测而非独立控制的因果结论） |
| 单个 optimizer step 的梯度 | 梯度差 L2 范数与真值梯度范数之比（WCNTS，取最差） | 最大 5.1%（Node 11）：单步内 SDC 噪声相对梯度本身通常较小 |
| 训练周期（预训练＋微调） | loss 曲线、参数差（L2）、微调精度与分歧率（DP） | **loss 几乎重合但参数持续漂移到不同极小值**；漂移速率各节点相近，作者归因于损失面尖锐、SDC 充当触发器；微调方面，**多数非灾难性运行的 DP 不大于换随机种子的数据重排对照**（且仅限所测六项任务），但存在明确反例——Node 6 在 CosmosQA 上末期 loss 尖峰使测试精度为 0、DP=100%（同一表中换 seed 的健康节点 DP 为 6.70%），不能把“不大于换种子”读成 SDC 影响的统计上界 |

### 传播链：错误进入 optimizer 状态与 checkpoint 之后

正文实验只测到参数层，但传播不止于此。按训练状态的依赖关系（方法推导，依据 PyTorch 2.6 固定源码的 Adam 实现里梯度→一/二阶矩→参数更新的状态链，[torch/optim/adam.py](https://github.com/pytorch/pytorch/blob/1eba9b3aa3c43f86f4a2c807ac8e12c4a7767340/torch/optim/adam.py)，非本库实测）：

```text
单步错值（activation，暂态，可被后续计算覆盖或放大）
  → 本步梯度（错梯度参与本次 update）
    → optimizer 持久状态（Adam 动量/二阶矩按梯度累积：错梯度污染的是跨 step 存续的状态，
       即使随后把参数恢复，被污染的动量仍会影响后续多步）
      → 参数 update（权重漂移；ACL 实验显示 loss 可全程不露痕迹）
        → checkpoint（漂移参数被保存；OCP §6.3.2 讨论延迟发现导致必须回滚到更早状态）
```

对判定与恢复的三条含义：

1. **“loss 正常”不能排除 SDC**：Node 10 的子模块与梯度持续受扰，但预训练与微调 loss 与健康节点完全一致——SDC 可能在尖峰出现前已影响训练一段未知时间（论文 §7.1）。
2. **可信恢复点早于“最新 checkpoint”**：恢复必须回到**确认未被污染**的保存点；若错误已写入 optimizer 状态或 checkpoint，重启或加载最新 checkpoint 都不够（恢复边界与状态清单见[Checkpoint 状态一致性](../06-training/checkpoint-state-consistency.md)；文件字节完整性是另一层，见[Checkpoint 完整性证据](../04-data-storage/checkpoint-integrity-evidence.md)——字节保存正确不等于数值语义正确）。判定“数据错误”候选时，先区分**输入/参考数据自身错误**与**计算产生错值**：先核对数据身份与参考值（golden 值本身）的来源正确性。
3. **观测可能改变发生率**：同步/监控降低加速器利用率，论文**提示**其可能降低 SDC 发生频率（未独立控制利用率的因果结论）——Node 14 在计算同步下**超过 4000 个 optimizer step 的观察窗口内**仅偶发、在参数同步下每步都有梯度差（§9）。“加探针后没再复现”不能反推缺陷消失。

## 检测方法分层：覆盖、成本与假阴性/误报

综合 OCP §5.2–§5.3 分类法（本批已读全文）、上述论文实测证据与平台工具文档，按验收要求的类别比较。未取得量化成本或覆盖率的格子保持 unknown，不给阈值。

| 方法 | 机制与来源 | 覆盖与成本 | 已知假阴性/误报与盲区 |
|---|---|---|---|
| 目标化 reproducer | 缩减失败案例为最小可复现输入（Meta 43 万行 JIT 汇编缩到 60 行测试） | 强证据（同核同输入必现）；依赖已有嫌疑样本 | elusive 触发条件可能无法系统复现 |
| fleet 周期筛查 / 共置迷你测试 | 见上节 Fleetscanner/Ripple 与 OCP §5.1（45–60 天窗口 vs 数天全 fleet） | 互有独有覆盖，需组合 | 覆盖随缺陷族变化；与负载/维护争资源 |
| 确定性重放＋对照 | 相同输入重跑比对；Gemini 规模配合空闲机扫描与热备上的 SDC 扫描器（OCP §5.1.4.1 p.19）；ACL 2025 §7.2 的影子数据并行副本同思路——每 step 选定数据并行 rank 重算并在梯度 all-reduce 时比对，作者认为这是当前可靠检出的最好方案 | 强，但要求可重放性与额外容量 | 非确定性训练需先固定执行（如 XLA 指令序），且有性能代价；只覆盖被选中的 rank/对象 |
| 字节/端到端完整性校验（信息冗余） | 在流水线多阶段存取并校验 checksum/哈希（OCP §5.2.1）；存储侧的文件校验见[Checkpoint 完整性证据](../04-data-storage/checkpoint-integrity-evidence.md) | 低成本，适合多节点通信与存储层 | 只证明**字节未变**，不证明数值语义正确；需后续纠正/回滚机制配套 |
| 元数据/结构校验 | **结构属性检查**（dtype、shape、张量计数——msprobe 与 `assert_close` 均把属性检查与数值比较分开，[固定 tag 文档](https://github.com/Ascend/msprobe/blob/tag_MindStudio_26.2.0.B110_001/docs/zh/user_guide/accuracy_compare/pytorch_accuracy_compare_instruct.md)、[testing.html](https://docs.pytorch.org/docs/2.6/testing.html#torch.testing.assert_close)） | 自动化开销很低（属性比对本身）；具体开销未量化（unknown） | 不检查值：合法范围内的数值错误不触发（对本类成立，见下行的指纹类） |
| 内容指纹校验 | CRC-32 等内容指纹比对（msprobe 将 CRC-32 不一致单列为 error 条件，与 dtype/shape 分列） | 计算与参考保存的成本未量化（unknown） | 在**参考可信且未发生哈希碰撞**前提下可发现内容变化（含保持 dtype/shape 的变化）；但不证明计算语义正确、不能容纳合法浮点差异；参考本身污染时假阴性 |
| 差分/不变量与 golden 对照 | 已知答案输入的周期校验（canary）、与预计算 golden 值比对（ACL 研究的 fleet 管理即用小训练＋golden 值比对筛节点，§3.1）、不变量断言 | 依赖校验点设计；dump/参考运行等成本未量化（unknown） | oracle 错误或未覆盖路径→假阴性；不变量过强→误报 |
| 任务质量检测 | loss/梯度范数监控（随负载持续）与下游精度/输出质量评估，两类并列不统一排序 | 覆盖：**对 SDC 低敏感**（ACL 实证 loss 几乎重合而参数已漂移）；成本：直接复用训练已计算的 loss 则增量近零，另行计算梯度范数需额外归约/同步、下游评估需额外运行——后两者未量化（unknown） | **误报边界**：正常随机性、数据分布变化与合法数值差异也可触发质量指标异常（OCP §5.4 非确定性混淆）；质量 oracle 缺失时静默劣化（[故障模型](fault-models-and-propagation.md) F7 行口径） |
| 复制与一致性校验（空间冗余） | 多副本/影子模型比对输出；对关键层冗余执行（OCP §5.2.2） | 检出有效，但开销在规模上可能不可行 | 副本间共享依赖时对共同原因失效（见[相关故障案例](correlated-failure-source-case.md)） |
| 整数剩余校验 | 模小素数（mod 3/7）并行计算验证算术结果（OCP §5.2.3） | 计算便宜 | 面向整数/量化数据与算术密集流水线；浮点张量语义下不直接适用 |
| ABFT / 校验和矩阵乘 | 把校验和编入算法（矩阵乘、attention 层）实现前向检错（OCP §5.3.2） | 有望低开销 | **实测反例**：ACL 研究在 float32、全部线性层上加 checksummed matmul，15 台已知不健康节点中仅 Node 14 被频繁标出（arXiv v1 附录 D.2；ACL 正文 Results for Experiment II 与 Fig.5）；三条解释（arXiv v1 附录 D.3；ACL 附录 D.1）——扰动落在浮点误差界内使阈值不触发、ABFT 开销降低利用率从而降低 SDC 发生率、SDC 可能发生在矩阵乘之外。且误差界按 IEEE-754 fp32+ 单位舍入推导，**bf16 直接套用会在健康节点上假阳性**（arXiv v1 附录 D.4；ACL 附录 D.2）。结论：ABFT 不是“装了就能检出”，精度/召回与数据类型、算子覆盖强相关 |
| checkpoint/重启（时间冗余） | 检出后回滚到此前**正确**状态（OCP §5.3.1） | 恢复手段而非检测手段 | 提频增存储/IO 与编排开销、压低运行 goodput；epoch 末才存不够；可信恢复点的确定见上一节 |

选择原则与[统一测试方法](test-design-and-coverage.md)共用：先声明要覆盖的故障模型与对象，再按覆盖×成本×假阴性/误报组合；任何一行都不单打独斗。

## 判定之前先扣除数值噪声背景

把“结果不一致”判为硬件 SDC 之前，必须先排除软件与数值语义的合法差异。PyTorch 2.6 文档支持的边界：

- 浮点加法/乘法不满足结合律，PyTorch 不保证数学等价的计算逐位相同，也不保证跨 release/commit/平台一致；**CPU 与 GPU 即使输入逐位相同、控制随机源后结果仍可能不同**（[numerical accuracy 开篇](https://docs.pytorch.org/docs/2.6/notes/numerical_accuracy.html)）。
- **整批执行与逐 batch 样本分别执行同一运算、整张量与切片执行**不保证逐位一致；linalg 对病态输入可能静默返回错误结果（软件层静默错误，与硬件 SDC 区分）。
- TF32、FP16/BF16 降精度累加等开关会改变数值结果——跨平台/跨配置比对前必须固定。
- 完全可复现不保证跨 release/commit/平台，即使同 seed（[randomness 开篇](https://docs.pytorch.org/docs/2.6/notes/randomness.html)，同登记条目的可复现性页）。
- `assert_close` 判据是 `|actual−expected| ≤ atol + rtol·|expected|`，默认容差按 dtype（float32 rtol 1.3e-6/atol 1e-5；bfloat16 1.6e-2/1e-5），是经验值不是硬件正确性保证（[testing.html](https://docs.pytorch.org/docs/2.6/testing.html#torch.testing.assert_close)，同登记条目的 testing 页）。

因此合规的判定流程：固定 dtype/开关/输入 → 用任务约定容差比对而非判等 → 排除已知数值语义后的完整性异常进入 SDC **候选**。稳定复现、确定性重放、迁移到其他设备、冗余对比用于**增强或削弱**假设，不是入口门槛——间歇故障只在特定条件下触发，早期可能没有稳定复现（OCP §3.2.1 p.9）；反过来，超出容差也不自动等于硬件故障，软件/数据/算法解释保留到定位证据闭合。与[GPU→NPU 精度差异诊断](../06-training/gpu-npu-precision-difference-triage.md)共用同一套容差纪律。

## 平台证据清单：NVIDIA / AMD / Ascend 按版本记录

| 平台 | 已核版本与观测/校验能力 | 边界与 unknown |
|---|---|---|
| NVIDIA | 被动观测字段（固定 v3.3.9，commit b0ec3c6，[dcgm_fields.h L751–793](https://github.com/NVIDIA/DCGM/blob/b0ec3c624ea21e688b0d93cf9b214ae0eeb6fe52/dcgmlib/dcgm_fields.h#L751-L793)）：`DCGM_FI_DEV_ECC_CURRENT`/`_PENDING`（300/301）、`DCGM_FI_DEV_ECC_SBE_VOL_TOTAL`/`_DBE_VOL_TOTAL`（310/311，volatile 累计）、`DCGM_FI_DEV_ECC_SBE_AGG_TOTAL`/`_DBE_AGG_TOTAL`（312/313，aggregate/persistent 累计）及 L1/L2 等逐位缓存细分（字段全集见[设备健康证据](../01-hardware/health-evidence.md)）；NVML/`nvidia-smi` 观察边界同该篇（未单独冻结版本）。主动诊断：DCGM diagnostic 显存插件以写入-回读校验并报告 mismatch（`DCGM_FR_MEMORY_MISMATCH` 为独立判据）；显存类测试的前提含按 GPU 配置判定允许性（无对应配置默认不允许）与所配置的最小内存分配条件（current user-guide 口径，2026-10-08 观察）；其余插件前提未逐项核（unknown）；Xid 动作表与 field diagnostic 的 RMA 地位见[节点验收](../01-hardware/node-acceptance-triage.md)（user-guide 形态页与 v3.3.9 源码快照**分别登记**） | ECC/mismatch 均为被报告或被测出的错误观测面；对 SDC 的 fleet 级检出覆盖率无公开量化来源（unknown），不以 Meta CPU 数字外推 |
| AMD | rccl-tests 固定 tag（therock-10.1）README（[README L175](https://github.com/ROCm/rocm-systems/blob/therock-10.1/projects/rccl-tests/README.md)）：`-c` 对每个算子的结果做正确性检查、命中报 `#wrong`，并声明校验在大 GPU 规模下的开销——校验对象为算子输出、可开关；关闭（`-c 0`）时 `#wrong=N/A` 表示**未校验**而非零错误（RCCL 正文固定 tag 口径）；ROCm 侧硬件观测能力（ECC/错误计数字段）**本批未核**（unknown），SDC 发生率同样 unknown；详见[RCCL 运行时与验证](../03-communication/rccl-runtime-and-verification.md) | 同左 |
| Ascend | 见下表（HDK 26.1.x A2 树，npu-smi/DCMI 官方页＋msprobe 固定 tag＋FaultDiag 固定 commit） | NPU 的 SDC 发生率、fleet 级检测实践与保障能力：检索范围内无公开一手材料，**保持 unknown**（不以 CPU/GPU 研究代填） |

**Ascend 逐项记录**：

| 证据 | 精确内容（固定版本锚点） | 边界 |
|---|---|---|
| ECC 计数（[npu-smi ECC 支持页](https://www.hiascend.com/doc_center/source/zh/HDK/2610/A2/A2npu/npusmi_0034.html)；命令参考入口登记为 [npusmi_0007](https://www.hiascend.com/doc_center/source/zh/HDK/2610/A2/A2npu/npusmi_0007.html)，HDK 26.1.x A2 树） | `npu-smi info -t ecc -i id` 输出 `HBM Single/Double Bit Error Count`（当前）、`Aggregate Total Err Cnt`（生命周期累计）、`Isolated Pages Count` 与 `Next-Isolated Pages Count`（单比特两项为预留恒 0；多比特待隔离取值 0–64，经复位/重启/上下电刷新为已隔离数）；计数上限 4294967295；支持矩阵含 Atlas 900 A2 PoD/800T A2 等，物理机 root | **被 ECC 检出并计数的是 signaled 错误**（corrected/DUE 类），不构成 SDC 检出或发生率证据 |
| DCMI 接口（[dcmi_047](https://www.hiascend.com/doc_center/source/zh/HDK/2610/A2/A2DCMI/dcmi_047.html)） | `dcmi_get_device_ecc_info(card_id, device_id, input_type, ...)`，`input_type` **仅支持 `DCMI_DEVICE_TYPE_HBM`**；返回 `enable_flag` 与单/多比特当前计数（**系统重启清零**）、生命周期累计、隔离页数；文档注明“查询到多比特错误，需要进行相关问题定位和处理” | 同上；SRAM/DDR 等组件类型该接口不支持 |
| 算子/张量级精度比对（[msprobe 固定 tag 比对文档](https://github.com/Ascend/msprobe/blob/tag_MindStudio_26.2.0.B110_001/docs/zh/user_guide/accuracy_compare/pytorch_accuracy_compare_instruct.md)，tag `MindStudio_26.2.0.B110_001`；docs 目录许可 CC BY 4.0） | dump（config.json）→ 精度比对 → 分级可视化；指标含 Cosine、EucDist、MaxAbsErr、MaxRelativeErr、千分之一/千分之五误差比例、统计量相对误差、CRC-32、`Requires_grad Consistent`；官方口径 Cosine“实际可接受阈值为大于 0.99”、MaxAbsErr“小于 0.001”、千分位比例“仅作为精度下降趋势的参考，并不参与计算精度是否通过的判定”；error 标记规则如 input 千分之一比例 >0.9 且 output <0.6、norm 相对误差 input <0.1 且 output >0.5、dtype/shape 不一致；`_reduce_scatter_base` 等占位输入 API 与 `empty`/`to` 等冗余 API 有豁免规则 | **离线比对工具的判定规则**：阈值是官方经验口径，且“趋势参考不参与判定”与“error 标记规则使用该比例”并存（上游自身口径的两层区分，本库照录不替其消解）；文档明示 NPU 与 CPU/GPU 差异随模型执行不断累积，同一 API 可能因输入差异大到无法比对——比对通过不等于无 SDC，比对异常也需先走容差纪律 |
| 日志规则诊断（[FaultDiag v26.1.1 固定 commit](https://github.com/Ascend/mind-cluster/blob/44385c13d7b1d87def35f1604e8be4d16de6ca4e/docs/zh/faultdiag/ascend-faultdiag/05_usage/04_fault_diagnosis.md)） | 日志清洗后 `ascend-fd diag` 输出根因节点分析（按 HCCL 报错定位根因/首错节点与根因节点链）与故障事件分析（按故障知识图谱给故障分类/名称/建议方案/关键日志/传播链）；`-p` 可诊断性能劣化（计算降频、CPU 抢占、网络拥塞）；终端最多 16 条、完整结果在 diag_report.json | 规则匹配产出**候选假设与建议**，不构成根因证明；其示例报告为文档示例非真实事故；本库不将其输出当作 SDC 证据 |

**NPU SDC 资料可得性边界（本批检索范围与结论）**：本批检索范围覆盖 hiascend HDK 版本化文档树（npu-smi/DCMI/健康管理）、CANN 文档入口、msprobe 仓库固定 tag、mind-cluster 固定 commit 的 FaultDiag 组件文档。结果：公开材料能支撑 ECC 计数（有信号错误）、离线精度比对与日志规则诊断；**未找到**昇腾/NPU 的 SDC 发生率统计、fleet 级 SDC 扫描实践或算力校验保障的公开一手文档。因此 NPU 的 SDC 发生率、检测覆盖与保障能力在本库保持 **unknown**，不以 CPU（Meta：约千分之一硅设备，[2203.08989 §2](https://arxiv.org/abs/2203.08989)）或 GPU（Llama 3 快照：意外中断的 1.4% 归因 SDC，[arXiv:2407.21783 Table 5](https://arxiv.org/abs/2407.21783v3)，归因口径含 suspected）研究代填；后两者也各自限其平台、规模与统计口径。

**故障注入的地位**：注入（如位翻转、算子输出扰动）只能**评估检测方法的覆盖与响应**（见[统一测试方法](test-design-and-coverage.md)），合成注入的检出不构成真实硬件 SDC 发生证据；ACL 研究同样把“注入研究可能与生产 SDC 不同”列为既有工作局限（§2.1）。

## 适用边界

- Meta 两篇论文均为数据中心 **CPU** 证据（第二篇明确限某 CPU 缺陷族的较大子集）；“适用于加速器”是 OCP 白皮书的多厂商共识性讨论，不是等量实测。GPU 数字（Llama 3 Table 5）限其 54 天快照与"confirmed or suspected"归因口径。
- ACL 研究限其声明范围：15 台临时持有的不健康节点、单节点张量并行、同步机制降低 SDC 发生率的影响未消除、loss 尖峰只在微调中观察到。数字不可外推为“训练遇到 SDC 必然如何”。
- SuperBench 的灰色退化是性能域概念，其 Azure 数字（77.8%、22.61× MTBI 等）限特定集群与仿真。
- OCP 白皮书本次已读至文末（文件 30 页）；其引用的 goodput 论文见[可靠性指标](reliability-metrics-and-recovery-loss.md)。
- 本文没有任何本地硬件测试、注入或生产观测；所有数字是来源方在其环境的一手观察，本文对 optimizer 状态传播的说明是方法推导（依据固定源码），不是本库实验结论。

## 常见误解

- **“健康检查全绿 = 计算正确”**：硬件检测未触发是 SDC 的定义域，被动日志与健康摘要不覆盖；但应用间接症状可形成候选、主动结果校验可有限检出——三层分开说，不能互相替代。
- **“ECC 存在 = 数据通路全覆盖 / ECC 计数非零才有问题”**：ECC 主要保护存储结构且覆盖不完整（Meta §1–§2）；Ascend 侧 ECC 计数是 signaled 错误的证据，ECC 未报不能推出计算正确。
- **“ABFT/校验和装上就能检出 SDC”**：见上表实测反例——真实不健康节点上 float32 ABFT 大多不触发，bf16 直接套用还会假阳性。
- **“loss 正常 = 训练未受 SDC 影响”**：真实节点证据显示参数可以在 loss 几乎重合的情况下持续漂移到不同极小值。
- **“微调结果最多和换随机种子一样差”**：反例存在（Node 6 末期尖峰致精度 0）；“不大于换种子”只描述多数非灾难性运行在所测任务上的观察。
- **“跨平台结果不同 = 硬件有 SDC”**：浮点非结合性与合法实现差异是背景噪声，先走容差纪律。
- **“一次 canary/筛查通过 = 该设备无 SDC”**：数据随机化、电气/环境/生命周期变化使检测必须反复进行；OCP 记录同一检查六个月后才失败的磨损案例。
- **“性能退化和计算错误是一回事”**：灰色退化与 SDC 分属性能与正确性两维，见[可靠性维度与故障域](dimensions-and-failure-domains.md)。

## 例子与相关知识

一个合规的怀疑链：训练 loss 出现不可解释偏差 → 按[精度差异诊断](../06-training/gpu-npu-precision-difference-triage.md)扣除配置与数值噪声 → 先核对输入/参考数据身份（排除 oracle 污染）→ 差异绑定特定节点/核且同输入必现 → 构造最小 reproducer → 用确定性重放或影子副本比对增强/削弱 → fleet 内同型硬件筛查；若确认 SDC，恢复点回退到未污染 checkpoint 并核对 optimizer 状态。相关入口：[证据与假设](evidence-and-hypotheses.md)、[故障模型与传播](fault-models-and-propagation.md)、[统一测试方法](test-design-and-coverage.md)（注入评估检测覆盖）、[可靠性指标](reliability-metrics-and-recovery-loss.md)（SDC 造成的有效产出损失口径）。

## 来源核对范围

- [Silent Data Corruptions at Scale, arXiv:2102.11245v1](https://arxiv.org/abs/2102.11245v1)：定义、干净日志盲区、fleet 检测机制（§1/§5/§7/§8；第九批已核）。
- [Detecting silent data corruptions in the wild, arXiv:2203.08989v1](https://arxiv.org/abs/2203.08989)（CC BY-NC-ND 4.0）：本批全文核读——硅测试漏斗（§3）、四类触发因素与 6 个月退化实验（§4）、Fleetscanner/Ripple 机制（§5）、表 1 与量化（§6，等价检出终点 70%/15 天/5–6 个月与 signature 部署 2 周分列）。仅归纳。
- [Understanding Silent Data Corruption in LLM Training, ACL 2025](https://aclanthology.org/2025.acl-long.996/)（登记主修订；pp. 20372–20394）与 [arXiv:2502.12340v1](https://arxiv.org/abs/2502.12340v1)（全文用于附录定位）：fleet 管理筛选手法（§3.1）、三层级实验与表值（§4–§6）、静默性论证（§7.1）、ABFT 实测（正文 Results for Experiment II/Fig.5 ＋ arXiv v1 附录 D.1–D.4）、局限（§9）。两版附录编号不同，引用按版本定位。
- [The Llama 3 Herd of Models, arXiv:2407.21783](https://arxiv.org/abs/2407.21783v3)：本文仅引 Table 5 的 SDC 归因行（1.4%，confirmed-or-suspected 口径）；完整核对见[可靠性指标](reliability-metrics-and-recovery-loss.md)。
- [OCP 白皮书 Silent Data Corruption in AI（2025-08-27，CC BY-SA 4.0）](https://www.opencompute.org/documents/sdc-in-ai-ocp-whitepaper-final-pdf)：第九批读 p.1–19；本批补读 §5.2.1–§5.2.3、§5.3、§5.4、§6 至文末（文件 30 页）。
- [PyTorch 2.6 数值精度/可复现性/assert_close](https://docs.pytorch.org/docs/2.6/notes/numerical_accuracy.html)（第九批已核，登记条目含 randomness 与 testing 页）与 [PyTorch 2.6 Adam 源码](https://github.com/pytorch/pytorch/blob/1eba9b3aa3c43f86f4a2c807ac8e12c4a7767340/torch/optim/adam.py)（本批核 optimizer 状态依赖，固定 commit 1eba9b3）。
- Ascend：[npu-smi ECC 页](https://www.hiascend.com/doc_center/source/zh/HDK/2610/A2/A2npu/npusmi_0034.html)与 [DCMI dcmi_047](https://www.hiascend.com/doc_center/source/zh/HDK/2610/A2/A2DCMI/dcmi_047.html)（HDK 26.1.x A2 树，本批逐字段核读）；[msprobe 固定 tag 比对文档](https://github.com/Ascend/msprobe/blob/tag_MindStudio_26.2.0.B110_001/docs/zh/user_guide/accuracy_compare/pytorch_accuracy_compare_instruct.md)（指标、阈值、标记与豁免规则逐条核读；docs 许可 CC BY 4.0 经 [docs/LICENSE](https://github.com/Ascend/msprobe/blob/tag_MindStudio_26.2.0.B110_001/docs/LICENSE) 核对）；[FaultDiag v26.1.1 固定 commit 文档](https://github.com/Ascend/mind-cluster/blob/44385c13d7b1d87def35f1604e8be4d16de6ca4e/docs/zh/faultdiag/ascend-faultdiag/05_usage/04_fault_diagnosis.md)（概述/诊断/日志清洗/附录）。
- 逐条主张与读取范围见[第三十批 T08-04 来源记录](../../docs/research/batch-30-t08-04-sources.md)。
- 待确认：NPU 侧 SDC 发生率与 fleet 级检测实践的一手材料（当前 unknown）；2203.08989 后续版本（abs 页当前仅 v1）；ACL 研究不健康节点维修归队后的复测结果（论文未含）。
