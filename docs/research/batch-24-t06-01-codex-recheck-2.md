# Batch 24 · T06-01 Codex 定向复核第二轮

## 1. 结论与范围

- 日期：2026-10-18（Asia/Shanghai）。仅评价 T06-01 本轮修订，不评价 Batch 24 其他任务或整个训练主题的完成情况。
- 第一轮留下的 **6 个 OPEN 项：本轮 CLOSED 3、仍 OPEN 3**。关闭 **B24-T061-C05、C07、R01**；保留 **B24-T061-C01、C02、C06**，均沿用 P2。
- 第一轮已经 CLOSED 的 C03、C04、C08、C09 经关联回归抽查，维持 CLOSED。累计 C01–C09 加 R01 为 **CLOSED 7 / OPEN 3**；开放优先级分布为 **P1 0、P2 3、P3 0**。
- **本轮独立新发现 0 项**，不新增 B24-T061-S2-xx 编号；原问题的残留继续沿原编号，不重复计数。
- **结论：暂不通过。** 尚未达到“全部上一轮 OPEN 项 CLOSED 且无新 OPEN P1/P2”的通过条件。
- 执行者：本会话 Codex，技术审阅角色；未派发子代理或另起外部模型审阅。上下文没有可独立核验的实际模型、推理档位及路由元数据，记录为 **unknown**，不以约定模型代替实际执行记录。
- 本轮只新增本报告，不修改正文、作者取证、来源登记、导航、任务状态或原工作区构建产物。没有启动训练、进程组、checkpoint 保存/加载或 GPU/NPU 实验；静态核算和结构检查均不构成硬件验证。

## 2. 输入、快照与证据方法

先读取 `README.md`、[编写指南](../authoring-guide.md)、[内容归属](../../content-outline.md)及元数据 schema，再对照[初审报告](batch-24-t06-01-codex-review.md)、[第一轮复核](batch-24-t06-01-codex-recheck.md)的原关闭条件。本轮定位使用当前源文件行号，不沿用旧报告的正文坐标。

| 简称 | 输入与本轮重点位置 |
|---|---|
| P | [修订正文](../../knowledge/06-training/parallelism-and-state.md)，全文 L1–241；重点 L86–104、L112–140、L186–201、L224 |
| A | [作者取证](batch-24-t06-01-sources.md)，全文 L1–114；逐项核对 L108–114“修订轮二补充”，另核对 L40 的实际更正 |
| T | [完整覆盖任务表](../../plans/full-coverage-backlog.yaml)，T06-01 L5832–5879 的目标、五条 acceptance、来源准备与单篇归属 |
| R | [来源登记](../../sources/registry.yaml)，正文相关既有来源包；重点 PyTorch 固定 commit、Megatron 两条冻结实现记录及 MindSpeed-LLM v2.2.0 配套边界 |

输入 SHA-256：

| 文件 | SHA-256 |
|---|---|
| P | `9ea9b72f33503e94fcf69a11a9386bd4390eb6f26c4179fcb54fceab9db12b00` |
| A | `b69631ccf6ad1fbe7390ebefde6b09c25a963de5b3803195e3921ea2de571eb3` |
| 第一轮复核 | `d4c6c2a2650323a27b4c578743d13f9c4cdd44bde2cbdc2a1d891ebb64f5fe35` |
| 初审报告 | `51e1085eb1bb3bf3421216d2dd4bd5cd45f2c23bfe9c7eed3bb7fa52948f1193` |
| R | `656c2f814bb2b0a28bd60de2c3a113f133550ae0ddd12eb1c6e4305646354d15` |

Git HEAD 为 `bce9d978f58d71e180e46ca81069a152fb646ea0`。开始时已有未提交的正文、导航、registry 改动和其他审阅材料，均不归为本轮修改。

独立重开了第 7 节 E01–E09 的精确上游位置。六个固定 raw 文件均由 curl 在保持 TLS 校验的情况下成功取回，字节哈希与已有取证相符；源码行号采用这些原文件的 LF 坐标。网页工具读取 MindSpeed arguments 出现内部错误，但同一精确 raw URL 经 curl 成功取回，不把工具错误当作上游不可达。版本化 HTML 另按实际正文核对，不以网页转换行号生成源码锚点。没有安装、导入或执行上游训练代码。

## 3. 上轮 OPEN 项逐项判定

| 编号 / 优先级 | 本轮正文及作者补证 | 判定与依据 |
|---|---|---|
| **B24-T061-C01 / P2** | P L128–140；A L110 | **OPEN**。bf16、micro=1、各行 DP/累积及 64-rank 数量分解已补齐到可复算的程度，旧 batch 算错单独按 R01 关闭；`FULL_SHARD`、无测量的收益边界也保留。但“不对称拓扑”仍未落实为各候选的 rank→节点/设备及组放置。TP 行只有“宜落在低时延域”的建议，PP/CP/EP 等也未声明其通信组究竟落节点内还是跨节点。第一轮要求的固定放置条件仍缺，详见 3.1。 |
| **B24-T061-C02 / P2** | P L86–104；A L111 | **OPEN**。两套 RankGenerator、ETP/expert-DP 公式及 rank 37 的新组成员均核对正确；合成 order 不等于默认框架 order 的边界已写明，不要求作者伪称实测框架布局。第 20 层也已修正到 stage 16–31 内。但专家编号仍是占位/unknown，参数 shard 仍缺确定 shape、轴和可核算 offset，无法完成 expert→参数→shard 的身份闭环，详见 3.2。 |
| **B24-T061-C05 / P2** | P L68、L115–116、L124、L233；A L40、L112 | **CLOSED**。A L40 已实际改为 `num_experts % EP == 0`，不再只是追加说明而保留反向取证。与 E05 L1600–1603 一致；P 保留 GQA 的 TP 与未 repeat 时的额外 Ulysses 分支，符合 E04 L247–263。48/52 的正反例与 GQA 静态代入见第 4 节。关闭限于公式、条件和取证方向，不代表配置已启动。 |
| **B24-T061-C06 / P2** | P L190–201，尤其 L199；A L113 | **OPEN**。新增 overflow 时跳过参数更新、仍更新 scaler 的说明与 E03 L355–365、L463–480 一致；成功/失败的 scheduler 与 consumed samples 分叉也正确。新增累积未完不得更新参数、mid-step 须保存梯度和计数的内容接受。但原关闭条件还要求说明累积未提交时 scaler/scheduler 等是否推进；正文仍只禁止提前更新参数，未明确 scale 在整个有效 batch 累积期间须保持不变及 `update()` 不能逐 micro-step 调用，详见 3.3。 |
| **B24-T061-C07 / P2** | P L224；A L114 | **CLOSED**。已显式设置 `--use-mcore-models`，并把前置 Megatron 校验通过列为“假定”，不是声称已有实际启动证据。E04 L276–282 的先行模式检查、序列检查与 head 检查顺序支持这一条件式推导；L1456–1479 的外部前置校验没有被省略。48→52 的取模正确，绕过后的行为仍为 unknown。仅关闭“在所声明前提成立时演示目标检查式”的反例，不认可为完整配置或首次失败的运行证明；句中“其余前置约束均满足”按其前面的假设限定理解。 |
| **B24-T061-R01 / P2** | P L128、L132–138；A L110 | **CLOSED**。已改为 `micro 1 × 累积 × dense DP = 512`，逐行复算全为 512，且各物理维度乘积为 64，详见第 4 节。EP 行未把 expert-DP=8 当成独立样本 DP，也未重复乘 TP/PP/CP；公式与 E02 L367、L381–394 一致。该项算术闭环与 C01 放置条件未闭环分开评价。 |

### 3.1 C01 残留：卡数分解完整，不等于放置固定

P L128 确定了 8 节点×8 卡和节点内/间带宽不对称，却没有指定各候选怎样把通信组嵌入该拓扑。不能用身份样例 L86 的 dense mesh 直接补全表格：该样例为 TP2/PP2/CP2/DP8，表中多数候选不是这个分解；身份样例本身也未给出 rank→节点/本地设备的映射。

这是尚未完成的合成条件，不是要求补做性能实验。例如，若另行约定连续 8 ranks 为一个节点，则同为 PP2/DP32 的候选可以取 PP 组 `[0,1]`，也可以取 `[0,32]`；前者在节点内，后者跨节点。两种分解都占满 64 ranks，但 P L135 的主要点对点通信经过不同链路。在拓扑非对称的比较中，这个条件不能留给读者任选。

**剩余关闭条件：**给出公共 rank→节点/设备约定，并为每个候选声明有序 group/mesh 的构造或足以推出放置的维度顺序。可以完全采用明确的合成放置，不需真实带宽或训练测量；未测扩展效率继续保留分析预期/unknown。FSDP/VPP 等行省写的单位维度可用统一默认值说明，不能仅因没有重复写 `=1` 就否定其已经算对的 batch。

### 3.2 C02 残留：专家组正确，专家与 shard 身份仍未落地

E01 L479–491、L859–907 支持 dense/expert 两套布局及 PP 组一致性要求；本轮对作者合成布局的独立枚举结果如下：

- dense：`rank = 32×pp + 4×dp + 2×cp + tp`，rank 37 坐标为 `(1,1,0,1)`。
- expert：`rank = 32×pp + 8×ep + 2×edp + etp`，rank 37 坐标为 `(1,0,2,1)`；本例没有额外 GTP/EGTP 轴，即相应因子取 1。
- 有序 expert-TP 组 `[36,37]` / 组内 1；EP 组 `[37,45,53,61]` / 组内 0；expert-DP 组 `[33,35,37,39]` / 组内 2。两个合成 grid 的全部 32 个 PP 组相同，不只是 rank 37 的 `[5,37]` 恰好相同。
- `expert_dp=64/(2×4×2)=4`，dense DP 为 8；两者不应在同一坐标公式中当成可独立相乘的轴。上述合成集合正确，不声称等于上游默认 order 的生成结果。

**尚缺的原验收内容：**P L99 仍写“某 32 个连续编号专家”，L104 也明确把具体专家编号区间留为 unknown；P L100 只有 `layers.20.self_attention.qkv`、row-shard 与符号式 `hidden/2`，没有选定 tensor 的全局 shape、shard 轴、本地 shape 和确定 offset，也没有将具体专家参数接到这个映射里。因而现有覆盖检查只证明物理 rank 网格及组成员自洽，不证明逻辑专家/参数 shard 的无漏、无冲突及合法副本归属。

**剩余关闭条件：**在同一合成样例中明示专家分配规则，给出 rank 37 的确切 expert IDs；选一个明确的专家参数或另一个有完整定义的参数，列出全局 FQN、shape、dtype、shard 轴及 offset，并检查各 shard 的逻辑覆盖与 expert-DP 副本关系。可以自行规定合成 tensor 和分配顺序，不要求读取真实 checkpoint；不能把本报告可替作者推导出的约定当作正文已经写出。层号问题及缺少 EP/ETP/EDP 组的问题已经修好，不再列作残留。

### 3.3 C06 残留：累积窗口内 scaler 边界仍不完整

P L199 的 overflow 新增文字本身正确：E03 的普通 enabled GradScaler 路径会在 inf/NaN 时不做参数更新，但在有效迭代末调整 scaler；成功时 scale 也不一定每次变大。正文明确用 PyTorch GradScaler 说明 scaler，不能据此推断 Megatron 一定实例化了这个类。Megatron 的 scheduler/样本分支按 E06 独立核对，两套样板不拼成一个已验证软件组合。

未闭环之处是：P L199 写 `update()`“每个迭代末尾调用”，同段随后只说明完整累积窗口结束前不得更新参数，没有界定这里的“迭代”是有效 batch 而非每个 micro-step，也没说累积中途不得改变 scale。E03 L478–480 要求所有相关 optimizer 的 `scaler.step()` 之后才更新；E07 的 **Gradient accumulation** 节进一步明确 scale 在整个有效 batch 累积期间不变，inf/NaN 检查、跳步和 scale 更新按有效 batch 粒度发生。中途仅保证“不更新参数”并不足以保证梯度可解释。

这仍是第一轮 C06 的“累积未提交时哪些更新不得提前发生”，不是新增发现。没有逐 micro-step 调用 scaler 的运行记录，因此本报告不声称作者代码已实际犯错，也不据缺少一张表本身拒绝关闭；需要的是文字中的执行契约完整。

**剩余关闭条件：**显式说明非最后 micro-step 只累积梯度/推进对应 micro-step 与已读取进度，不提前执行 optimizer/scaler 更新、不提前推进成功更新计数或按成功更新驱动的 scheduler；启用缩放时，整个窗口的 scaled gradients 使用同一 scale。窗口结束后再分成功/overflow 两支。应用 data commit、数据重放和未声明的跨框架行为继续按显式契约或 unknown 处理，不从 consumed samples 推定已提交。也可用简洁三情形表表达，不要求特定排版或新增硬件实验。

## 4. 独立静态核算

仅使用审阅者编写的整数和集合枚举，未导入上游模块。以下 `tp/pp/cp` 的单位维度采用单策略候选的通常省写解释；其算术成立不替代 C01 所要求的放置声明。

| 合成候选 | `(TP, PP, CP, dense DP)` | micro | 累积 | rank 数乘积 | global batch |
|---|---|---|---|---|---|
| 纯 DP | `(1,1,1,64)` | 1 | 8 | 64 | 512 |
| FSDP FULL_SHARD | `(1,1,1,64)` | 1 | 8 | 64 | 512 |
| TP+SP | `(2,1,1,32)` | 1 | 16 | 64 | 512 |
| PP | `(1,2,1,32)` | 1 | 16 | 64 | 512 |
| VPP，vp=2 | `(1,2,1,32)` | 1 | 16 | 64 | 512 |
| CP2 | `(1,1,2,32)` | 1 | 16 | 64 | 512 |
| CP4 | `(1,1,4,16)` | 1 | 32 | 64 | 512 |
| EP4，ETP=2 | `(2,1,1,32)` | 1 | 16 | 64 | 512 |

VPP 的 virtual chunks 不额外乘物理 rank；EP 行另有 `2×4×8×1=64` 的 expert grid 分解，不能把 expert-DP 再乘进同一 batch。身份样例若另外固定 global batch=512，则其 dense DP8 需要累积 64；正文现在没有把该身份样例重新写成 micro1/累积8/global512，不再重现 R01。

其他核算：

| 对象 | 本轮结果 | 证据边界 |
|---|---|---|
| dense / expert 网格 | 分别枚举 64 个唯一 rank，均恰为 0–63；全部 PP 组相同 | 仅证明作者声明的两个合成映射，不证明实际启动或专家编号分配 |
| 专家整除方向 | `128 % 4 = 0` | 支持 P 与 A L40 的修正 |
| Ulysses head 正反例 | `divmod(48,8)=(6,0)`；`divmod(52,8)=(6,4)` | 对应 E04 L247–249 的目标分支 |
| GQA，无 KV-repeat | TP2/Ulysses4：query groups 8 通过；4 虽可被 TP2 整除，但 `(4/2)%4=2` 不通过 | 对应 E04 L250–263；repeat 打开仅绕过该额外 Ulysses 分支，不绕过 TP 分支 |
| 反例两项整数前置 | `64%(2×2×4)=0`；`32768%(2×4)=0` | 不把两项余数冒充完整 MindSpeed/Megatron 前置校验的实测证明 |

## 5. 已 CLOSED 项的关联回归抽查

| 编号 | 当前关联位置与抽查结果 | 状态 |
|---|---|---|
| C03 | P L169–178、L217 仍区分稳定逻辑身份、同布局恢复与有支持证据的重分片；L104 新增 expert grid 没有恢复“物理 rank/placement 必须不变”的通用判据。E09 的 DCP 支持范围没有被扩展到任意第三方状态。C02 的样例缺口不重复算作 C03 回归。 | **维持 CLOSED** |
| C04 | P L106–122、L233 仍分硬断言、功能不支持和性能提醒。E05 L1413–1435 的 MoE overlap 分支为 warning，未被重新写成 assert；与后续其他条件的 assert 分支区分。 | **维持 CLOSED** |
| C08 | P L142 的链接及 R 的 backend 条目仍为同一 PyTorch 2.6 `distributed.html`；本轮 E08 可重开，未恢复失效 `distributed.backend.html`，未新增 AMD/ROCm 版本配套承诺。 | **维持 CLOSED** |
| C09 | P L64、L66 的 router 形成路由、dispatcher 消费映射的职责划分未变；本轮改动集中于组身份、batch、scaler 和反例，没有将具体路由算法重新归给 dispatcher。按第一轮已核对的冻结 dispatcher 证据维持结论，本轮未扩大为 router 全实现审查。 | **维持 CLOSED** |

没有发现需另以 B24-T061-S2-xx 登记的独立新问题。修订新增文字中的关联缺口，已分别归到 C01、C02、C06。

## 6. T06-01 验收条目重核

| 验收条目 | 本轮核对 | 结果 |
|---|---|---|
| 1. EP dispatch/combine、专家负载与通信；CP/SP 与 TP 的实现化区分 | P L60–80；保留实现/版本边界，C09 维持关闭；整除与 GQA 分支及取证方向本轮闭环。 | **满足本轮来源与文字范围** |
| 2. 固定模型/序列/global batch/拓扑，比较状态内存、通信、bubble、偏斜和扩展效率，不给无条件最优 | 精度和候选 batch 数量已补齐且算对；收益仍按机制/unknown 表达。但候选组在不对称设备拓扑中的放置未固定。 | **未满足：C01；R01 已关闭** |
| 3. global/group rank、mesh、stage、expert、shard 样例和冲突检查 | dense/expert 组与 PP 一致性现可核算；层号及整除方向修正接受。但专家 IDs 和完整参数 shard 归属仍缺。 | **未满足：C02** |
| 4. forward/backward/accumulation/optimizer/scaler/data commit 的边界、所有权与合法跳步 | overflow/no-update 与成功更新的计数分叉、data commit unknown 均保留；未完成累积时 scaler 等的执行边界仍不完整。 | **部分满足：C06** |
| 5. 映射、梯度/更新、吞吐扩展、负载与恢复判据；来源实现例和合成反例 | P L215–224 的判据类别、官方脚本例和明确合成反例保留；C03 维持关闭，C07 按条件式静态反例关闭。官方脚本没有被写成本地运行成功。 | **满足本轮来源与文字范围；不代表实验验证** |

来源准备继续按三套独立档案处理：PyTorch 2.6、Megatron core_v0.19.2 与 MindSpeed-LLM v2.2.0；P L239 的配套 Mcore core_v0.12.1 / PyTorch 2.7.1 不与其他样板拼成可用组合。实际硬件、NPU 组件配套、mid-step 通用恢复、目标加载/重分片能力仍为原声明的 unknown。稳定 ID `training.parallelism-and-state`、单篇主归属及 `draft / source_checked` 未因本轮审阅升级。

## 7. 本轮精确上游证据

下列均为一手来源。外部材料仅作链接、短摘要与原创审阅判断，不复制长段、源码包或性能表，不改变仓库或第三方材料的许可状态。E07 为既有 PyTorch 2.6 来源包下的补充文档页；按“只新增本报告”的范围，不修改来源登记。

| 编号 | 精确位置与本轮用途 | SHA-256 / 获取状态 |
|---|---|---|
| E01 | [Megatron parallel_state.py · core_v0.19.2](https://raw.githubusercontent.com/NVIDIA/Megatron-LM/core_v0.19.2/megatron/core/parallel_state.py)，L479–491、L859–907；两套 rank generator、expert-DP 与 PP 组一致性 | HTTP 200；`1f6e23a01022c06be3b67f930095898e5032f6ff93695f8da5aae3b5a546dcf0` |
| E02 | [Megatron num_microbatches_calculator.py · core_v0.19.2](https://raw.githubusercontent.com/NVIDIA/Megatron-LM/core_v0.19.2/megatron/core/num_microbatches_calculator.py)，L367、L381–394；batch 与 micro-batch/DP 的关系 | HTTP 200；`a540540481321f233a23355bd5857854e3bfc86d36e69f611d1c7b66dd8d494f` |
| E03 | [PyTorch grad_scaler.py · commit 1eba9b3…](https://raw.githubusercontent.com/pytorch/pytorch/1eba9b3aa3c43f86f4a2c807ac8e12c4a7767340/torch/amp/grad_scaler.py)，L355–365、L463–480、L599–614；skip/update/保存边界 | HTTP 200；`eb4bc91fda9815ba40206e2dbb68f9845b85622fee3a92611f227b5845b20780` |
| E04 | [MindSpeed-LLM arguments.py · v2.2.0](https://raw.githubusercontent.com/Ascend/MindSpeed-LLM/v2.2.0/mindspeed_llm/training/arguments.py)，L242–282、L1456–1479；GQA、mcore 前提与前置校验调用 | curl HTTP 200；`fd64204269ad1749159d9b98f47c91f92cb17de5075cb92670f8ab1d5df42a38` |
| E05 | [Megatron arguments.py · core_v0.19.2](https://raw.githubusercontent.com/NVIDIA/Megatron-LM/core_v0.19.2/megatron/training/arguments.py)，L1413–1435、L1600–1603；warning 与专家整除方向 | HTTP 200；`f7fad20bc0e0cd9ba4b9ba7e70fa1a1b77030dfd020a7edb50b1d3b3aa41ebf6` |
| E06 | [Megatron training.py · core_v0.19.2](https://raw.githubusercontent.com/NVIDIA/Megatron-LM/core_v0.19.2/megatron/training/training.py)，L2474、L2503、L2518–2531、L3941–3942；scheduler/skip/消费计数 | HTTP 200；`d968ef8216f63d6373372190ac895fc905234c116bba3e804d2951876e6ad98c` |
| E07 | [PyTorch 2.6 AMP examples — Gradient accumulation](https://docs.pytorch.org/docs/2.6/notes/amp_examples.html#gradient-accumulation)；有效 batch 粒度及累积窗口内固定 scale | 精确章节可读；curl HTTP 200；HTML `153f2c9a131320204d04d96fafbf84bd189093ca6ddecaf66aecdb43565e0273` |
| E08 | [PyTorch 2.6 distributed](https://docs.pytorch.org/docs/2.6/distributed.html)；backend 链接回归与范围 | 本轮网页工具成功重开；不据此推定任意 AMD/NPU 配套 |
| E09 | [PyTorch 2.6 DCP](https://docs.pytorch.org/docs/2.6/distributed.checkpoint.html)，`get_state_dict` / `set_state_dict` 与支持范围；恢复映射边界抽查 | 本轮网页工具成功重开；不推定任意第三方状态可转换 |

## 8. 结构检查与交付边界

在包含当前未提交修订文件与本报告的临时隔离副本中执行：

- `make check`：**PASS，103 content entries / 493 sources**。
- `make build`：**PASS**，仅在隔离副本内生成 `build/catalog.json` 与 `build/catalog.md`。
- 首次临时副本未携带已有 `build/`，导致 `docs/first-fill-status.md` 指向上述两个产物的本地链接检查失败；补带原有产物后重新执行两条命令均通过。这是临时副本准备问题，不计为正文或仓库的新发现。
- 原工作区的两个构建文件保留不动。没有修改 `src/kb/`，不需新增单元测试，也没有运行训练或硬件测试。

这些检查只验证结构和本地链接，不验证技术结论、远程证据、配置可启动性或恢复正确性，不能代替第 3 节的技术关闭条件。

最终通过条件仍为：完成 C01、C02、C06 的剩余修订，并针对这些具体位置重新核对；不以作者“已处理”的补充、报告存在或结构构建成功直接宣称通过。
