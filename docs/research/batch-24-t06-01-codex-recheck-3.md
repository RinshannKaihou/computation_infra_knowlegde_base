# Batch 24 · T06-01 Codex 定向复核第三轮

## 1. 结论与范围

- 日期：2026-10-19（Asia/Shanghai）。仅复核[第二轮报告](batch-24-t06-01-codex-recheck-2.md)仍 OPEN 的 **B24-T061-C01、C02、C06**；既有 CLOSED 项只作关联回归抽查，不重开整篇初审。
- 上轮 3 个 OPEN 项中，**C02、C06 CLOSED；C01 仍 OPEN / P2**。此前 CLOSED 的 C03、C04、C05、C07、C08、C09、R01 维持原判定。
- 新增 **B24-B24-T061-S3-01 / P3 / OPEN**：新增 overflow 行对 growth tracker 的表述需明确为重置，而非笼统“推进”。沿用用户要求的双 `B24` 新问题编号前缀。
- 原 C01–C09 加 R01 累计 **CLOSED 9 / OPEN 1**；计入本轮新项后 **CLOSED 9 / OPEN 2**，开放优先级为 **P1 0、P2 1、P3 1**。
- **结论：暂不通过。** 虽无新 OPEN P1/P2，但 C01 尚未关闭，不满足“全部上一轮 OPEN 项 CLOSED 且无新 OPEN P1/P2”。
- 执行者：本会话 Codex，技术审阅角色；未派发子代理或另起模型调用。当前上下文没有可独立核验的实际模型、推理档位及路由元数据，记录为 **unknown**，不将约定模型冒记为实际执行模型。
- 本轮只新增本报告，不修改正文、作者取证、来源登记、导航、计划或原工作区构建产物。未安装或运行训练框架，未启动进程组、训练、checkpoint 保存/加载或 GPU/NPU 实验。

## 2. 输入与取证方法

按仓库约定先读 `README.md`、[编写指南](../authoring-guide.md)、[内容归属](../../content-outline.md)及 `schemas/content.schema.json`，再对照第二轮的三个剩余关闭条件。下文 P/A/T 为当前源文件行号，不沿用第二轮旧正文坐标。

| 简称 | 输入及本轮位置 | SHA-256 |
|---|---|---|
| P | [修订正文](../../knowledge/06-training/parallelism-and-state.md)，重点 L86–104、L126–140、L186–209；关联回归 L64–68、L108–124、L165–178、L225–247 | `f374643f46171a6aa9f310d5b1b2cd0e033a6416a8506cf7b784e9290fa56fd6` |
| A | [作者取证](batch-24-t06-01-sources.md)，重读末尾 L116–120“修订轮三补充”，并对照原取证 | `b015a0510f14a424129a3a7afc54d7b7b17bf8173ec0e51cb1817a83d54ff979` |
| R2 | [第二轮复核](batch-24-t06-01-codex-recheck-2.md)，第 3.1–3.3 节的关闭条件与第 6 节验收 | `fded215d930ae3b59e8326fd7c9628c5cf6cdb668a72d319cda6f3da45e12e84` |
| T | [完整覆盖任务表](../../plans/full-coverage-backlog.yaml)，T06-01 L5832–5879 | `53bfc8fe47d56ab322e546c853858cbaa90cf5a5d0305b33a80bab0f39275d54` |
| R | [来源登记](../../sources/registry.yaml)，相关 PyTorch、Megatron、MindSpeed 来源包及冻结范围 | `3ea07202e7e0573c8ff8089bc5fcdd142b5a51269dc1f646a9d4a08d065215a2` |

Git HEAD：`bce9d978f58d71e180e46ca81069a152fb646ea0`。工作区原有正文、registry、导航和其他审阅材料的未提交改动，不归为本轮产出。

必要上游证据采用只读重开：第 7 节 E01–E04 的固定 raw 文件均经 curl 在保持 TLS 校验的情况下成功取回，SHA-256 与第二轮记录一致；另取回 PyTorch 2.6 AMP 梯度累积页和同一固定提交下的 CUDA AMP scale-update 内核。网页工具对部分 raw 文件的展示行号与 curl 文件不一致，对内核页读取失败；本报告的**源码行号和字节判定一律以成功取回且核对哈希的原文件为准**，不将网页工具问题推定为上游变更或不可达。

独立核算仅使用审阅者编写的 Python 整数/集合枚举，未导入、执行上游模块。合成布局的自洽性不等于 Megatron 默认 order、配置可启动性或硬件验证。

## 3. 上轮 OPEN 项逐项判定

| 编号 / 优先级 | 修订与补证 | 判定及依据 |
|---|---|---|
| **B24-T061-C01 / P2** | P L128 新增 `node = rank // 8`；L132–138 标注每行通信组放置；A L118 | **OPEN**。公共物理放置已补，batch 与卡数仍正确。但“各候选按上文合成步长构造”未将不同维度大小下的有序组定义自洽：CP2 的步长、CP4 的跨节点判断及 EP 行的 EP 步长与引用的布局不一致。既不能原样复用旧数值步长，也不能仅按原轴顺序重算后得到表中结果。详见 3.1。 |
| **B24-T061-C02 / P2** | P L104 新增连续专家分配规则、专家参数完整身份与副本说明；A L119 | **CLOSED**。rank 37 的 experts 0–31、`expert_0.gate_proj` 的全局/本地 shape、bf16、轴 0 和 offset 5504 均可由明确的合成约定核算；ETP 覆盖与 EDP 副本关系无冲突，满足 R2 第 3.2 节关闭条件。详见 3.2。 |
| **B24-T061-C06 / P2** | P L199–207 新增累积窗口三情形表；A L120 | **CLOSED**。非最后 micro-step 明确不更新参数、不调用 `update()`、不变 scale、不推进 scheduler/成功计数；有效 batch 末再分成功/overflow，已补齐 R2 第 3.3 节要求的窗口执行契约。新增 growth tracker 措辞精度单列为 S3-01 / P3，不重复开放原 P2。详见 3.3 和第 4 节。 |

### 3.1 C01：公共节点编号已补，候选组构造仍不自洽

接受 P L128 新增的连续 8 rank 一节点；在此前身份样例中，TP `[36,37]` 同属节点 4、PP `[5,37]` 跨节点 0/4、dense DP `[33,37,41,45,49,53,57,61]` 跨 4 个节点，均算对。问题不是要求实测拓扑，而是这个 **TP2/PP2/CP2/DP8 身份样例的数值步长不能原封不动用于选型表的其他候选**。

采用对正文较宽松的解释：保留 dense 轴从慢到快的顺序 `[pp,dp,cp,tp]`，但随每行大小重算步长，则

`rank = ((pp_idx × DP + dp_idx) × CP + cp_idx) × TP + tp_idx`。

同理，保留已声明的 expert 轴顺序 `[pp,ep,edp,etp]` 时，步长也必须随 EDP 大小变化。这是对作者合成布局的推导，不冒充框架实际 order；[E01 的有序维度/步长构组语义](https://raw.githubusercontent.com/NVIDIA/Megatron-LM/core_v0.19.2/megatron/core/parallel_state.py)亦要求大小和顺序共同确定成员。

| 候选 | 依上述轴顺序重算的完整组例 | `node = rank // 8` 下的结果 | 与修订文字的差异 |
|---|---|---|---|
| CP2、TP=PP=1、DP32 | `rank = 2×dp_idx + cp_idx`；CP 组 `[0,1]`、`[2,3]`，依此类推 | 32 个 CP 组全部节点内，跨节点 0/32 | P L137 写 `[r,r+2]`；该步长来自旧 TP2 样例，不是此候选的 CP 轴步长 |
| CP4、TP=PP=1、DP16 | `rank = 4×dp_idx + cp_idx`；CP 组 `[0,1,2,3]`、`[4,5,6,7]`，依此类推 | 16 个 CP 组全部节点内，跨节点 0/16 | P L137 的“CP 组开始跨节点”不能由所引用的轴顺序与公共节点约定推出 |
| EP4、ETP2、PP=1、EDP8 | `rank = 16×ep_idx + 2×edp_idx + etp_idx`；rank 37 的 EP 组为 `[5,21,37,53]` | EP 跨节点；ETP `[36,37]` 节点内 | P L138 所称 EP 组 `[r,r+8]` 沿用的是旧 EDP4 样例步长，应重新定义；EP 的节点内外定性虽然仍为跨节点，具体成员不对 |

若把“按上文合成步长”解为原样保留数值，问题更直接：

- 将旧 dense 步长 `[32,4,2,1]` 用于 CP2/DP32，会生成 64 个互异的**偶数 rank 0–126**，缺少 0–63 中的 32 个奇数，另有 32 个 rank 越界。
- 将旧 expert 步长 `[32,8,2,1]` 用于 EP4/EDP8/ETP2，64 个坐标只得到 **40 个唯一 rank（0–39）**。例如 `(ep=1,edp=0,etp=0)` 与 `(ep=0,edp=4,etp=0)` 都映射到 rank 8；无法满足全 64 rank 的覆盖与唯一性。

这不是说 CP4 不可能跨节点，或 EP 只能有某一种放置。**作者可以另选合成 order 或显式 rank 表实现跨节点 CP；但必须把该候选的全部有序组及其互斥覆盖写清，不能让读者自行补一套新布局来解释表格。**

**剩余关闭条件：**保留公共节点/本地设备约定，为各行明确完整的维度顺序与按大小重算的步长，或给出等价的可枚举构组规则；修正 CP2/CP4/EP 的组例与节点内外结论。至少检查每套 grid 恰覆盖 0–63、无坐标冲突、组内序号与成员一致。允许使用完全合成的放置，不要求补训练、带宽或性能实验。此处是 C01 原“固定放置”关闭条件尚未满足，不另计新 P2。

### 3.2 C02：专家到参数 shard 的身份链已闭环

P L104 已明确这是一套本库合成分配，而非声称核对了 Megatron 实际专家顺序；两套 generator 及 PP 组一致性的来源范围与 [E01](https://raw.githubusercontent.com/NVIDIA/Megatron-LM/core_v0.19.2/megatron/core/parallel_state.py) L479–491、L859–907 相符。

独立枚举结果：

- dense：`rank = 32×pp + 4×dp + 2×cp + tp`；rank 37 为 `(1,1,0,1)`。
- expert：`rank = 32×pp + 8×ep + 2×edp + etp`；rank 37 为 `(1,0,2,1)`；未启用的 GTP/EGTP 因子按 1 处理。
- 两个 grid 分别恰覆盖 0–63，全部 32 个 PP 组一致。rank 37 的有序 ETP/EP/EDP 组分别为 `[36,37]`、`[37,45,53,61]`、`[33,35,37,39]`，组内序号分别为 1、0、2。
- EP 组内序号 `k` 对应 `[32k,32k+32)`，四段恰覆盖 128 个专家；因此 rank 37 的专家区间确定为 **0–31**，不再仅靠旧表 L99 的占位信息推断。
- `layers.20.mlp.experts.expert_0.gate_proj`：第 20 层在 pp=1 的全局层区间 16–31 内；全局 shape `[11008,4096]`、dtype bf16，沿第 0 维分两片。ETP 序号 0/1 分别覆盖 `[0,5504)` / `[5504,11008)`，本地 shape 均为 `[5504,4096]`；rank 37 的 offset **5504** 正确。
- 对 expert 0，stage 1 内的四组 ETP 副本为 `[32,33]`、`[34,35]`、`[36,37]`、`[38,39]`；`[33,35,37,39]` 持有同一后半行片的四个 EDP 逻辑副本，不是四块不同 shard。对 128 个专家、每个专家的 4 个 EDP 副本分别枚举，两片均无交叠、无遗漏。

因此接受原 C02 关闭。此结论只覆盖所定义的合成参数，不证明实际 FQN、checkpoint schema、真实专家分配或任何框架转换器已验证，也不替 C01 的不同候选补定义。

### 3.3 C06：有效 batch 窗口内的执行边界已补齐

[PyTorch 2.6 AMP examples 的 Gradient accumulation 节](https://docs.pytorch.org/docs/2.6/notes/amp_examples.html#gradient-accumulation)明确以有效 batch 为 inf/NaN 检查、跳步及 scale 更新粒度，累积期间梯度保持 scaled、scale 固定；有多个 optimizer 时，`update()` 应在相关 `scaler.step()` 全部结束后调用，亦见 [E03](https://raw.githubusercontent.com/pytorch/pytorch/1eba9b3aa3c43f86f4a2c807ac8e12c4a7767340/torch/amp/grad_scaler.py) L478–480。

P L203 现在明确非最后 micro-step 不调用 `update()`、不改变 scale，不更新参数、不推进 scheduler/成功更新计数，只积累梯度和相应读取/micro-step 进度；L204–205 将成功与 overflow 分开。原来的“每个迭代末尾”已有同表有效 batch 的限定，不再据这句话单独认定窗口不清。

P L199 的 Megatron 成功/失败分支也与 [E04](https://raw.githubusercontent.com/NVIDIA/Megatron-LM/core_v0.19.2/megatron/training/training.py) L2474、L2503、L2518–2531、L3941–3942 相符：scheduler 只在成功时推进，consumed samples 在两分支都推进。这里对 scaler 的说明限于启用相应 PyTorch GradScaler 的语义，不推定 Megatron 使用该类，也不把这一说明与选型表的 bf16 场景拼成实测配置。

P L207 继续把应用 data commit 留给显式契约，不从 consumed samples 推定已提交；mid-step 恢复仍须覆盖未提交梯度和累积计数，通用恢复能力保持 unknown。上述满足原 C06 的剩余关闭条件；增长计数器的新措辞问题见下一节。

## 4. 新发现

### B24-B24-T061-S3-01 · P3 · OPEN：overflow 行应写明 growth tracker 重置

- **位置：**P L205，新三情形表的 overflow/scaler 单元格：“按 backoff 缩小 scale、推进 growth tracker”。
- **依据：**这里已经正确要求调用 `update()`，但“推进 growth tracker”没有区分 scaler 状态变化与连续成功次数增加。[同一 PyTorch 固定提交的 AMP CUDA 内核](https://raw.githubusercontent.com/pytorch/pytorch/1eba9b3aa3c43f86f4a2c807ac8e12c4a7767340/aten/src/ATen/native/cuda/AmpKernels.cu) L188–190 在 found-inf 分支缩小 scale 并将 tracker **置 0**；L191–204 的非 overflow 分支才先增加连续成功计数，达到增长间隔后也重置。E03 L599–614 同时将该计数器定义为连续未跳步次数，并纳入 scaler state dict。
- **影响与分级：**可能让恢复状态表的读者误把 overflow 作为又一次连续成功计数。它不推翻已明确的“不在 micro-step 中途更新 scaler”契约，也没有证据表明实际代码如此执行，故列为 **P3 精确性问题**，不升级为 P2 或重新开放 C06。
- **关闭条件：**把 overflow 行明确改成“`update()` 执行，scale 按 backoff 缩小，growth tracker 重置为 0”；如果描述成功分支的 tracker，也应说明增长间隔触发后的重置，而非无条件递增。修订后针对这两行与固定源码复核，无需训练实验。

## 5. 已 CLOSED 项的关联回归抽查

| 项目 | 抽查范围与判定 |
|---|---|
| C03 | P L104 新增逻辑副本/shard 身份，与 L165–178、L225 的“稳定逻辑身份不等于物理 rank；受支持布局转换可改变 placement”边界无冲突，维持 CLOSED。 |
| R01 | P L128、L132–138 的八个候选逐行复算：dense 维度乘积均为 64，`micro 1 × 累积 × dense DP` 均为 512。EP 的 EDP8 未被额外乘进独立样本 batch，VPP 的 vp2 未被计入物理 rank，维持 CLOSED。构组残留仍归 C01，不混为 batch 算错。 |
| C04、C05、C07 | 仅检查邻近文字未因新增放置/shard/table 改动回退：硬断言/功能不支持/warning 仍分开；`128 % 4 == 0` 方向不变；合成反例的 mcore 与前置校验假设、绕过后 unknown 均保留。维持第二轮 CLOSED，不冒称本轮重新完成全部上游校验链。 |
| C08、C09 | 本轮三处修订不改后端链接或 router/dispatcher 责任；文本仍保留 PyTorch 2.6 distributed 链接及 AMD 不平移限定、router 产生映射且 dispatcher 消费映射。维持既有 CLOSED，不重复开展无关联网审阅。 |

R01 的复算依据仍为 [E02 微批计算器](https://raw.githubusercontent.com/NVIDIA/Megatron-LM/core_v0.19.2/megatron/core/num_microbatches_calculator.py) L367、L381–394。卡数与 batch 算术通过不能替代 C01 所要求的组成员/物理拓扑闭环。

## 6. T06-01 验收重新核对

| 任务验收 | 本轮复核结果 | 状态 |
|---|---|---|
| 1. EP dispatch/combine、专家负载/通信；CP/SP 与 TP 的精确来源区别 | P L60–80 的既有来源范围、平台/版本限定与职责修正未因三处新增文字回退；不扩大初审范围。 | **维持满足** |
| 2. 固定模型/序列/batch/拓扑的内存、通信、bubble、偏斜与扩展比较，无无条件最佳 | 公共节点映射已补，模型、bf16、batch、并行度与累积数仍完整；但 CP/EP 的组构造与放置结论不自洽。无测量收益仍保留为分析预期/unknown。 | **部分满足：C01 / P2** |
| 3. global/group rank、mesh、stage、expert、shard 身份及冲突检查 | P L104 的具体专家、参数 shape/dtype/轴/offset 与 EDP 副本已经补齐，身份样例静态覆盖检查通过。 | **满足：C02 CLOSED** |
| 4. forward/backward/accumulation/update/scaler/data commit 的所有权及合法跳步 | P L186–207 补齐累积中途与窗口末成功/overflow 的执行契约，data commit 与 mid-step 能力边界明确；growth tracker 的精确措辞仍有新 P3。 | **原 P2 关闭；保留 S3-01 / P3** |
| 5. 映射、梯度/更新、吞吐扩展、负载和恢复判据；来源实现例与合成反例 | P L223–232 保留判据、官方配置例及明确的条件式静态反例；未把脚本存在或取模代入写成本地运行成功。 | **维持满足本轮来源与文字范围** |

主归属仍为 `knowledge/06-training`，稳定 ID `training.parallelism-and-state`、`draft / source_checked` 未升级。PyTorch 2.6、Megatron core_v0.19.2 与 MindSpeed-LLM v2.2.0 仍按独立样板处理，MindSpeed 配套 Mcore core_v0.12.1 / PyTorch 2.7.1 不与另外两套拼成已支持环境。没有将来源复核、配置算术或结构检查视为硬件验证。

## 7. 本轮精确上游证据

均为一手资料，只链接、短摘要及原创审阅，不复制长段文档、源码包或性能表。E05 是既有 PyTorch 2.6 来源包下的补充文档页；E06 为同一固定 PyTorch 提交下用于核对本轮新增 tracker 措辞的补充实现位置。本轮按“只新增报告”约束不修改 registry，不将补充核查冒记为正文已完成新增来源登记。

| 编号 | 精确来源及位置 | 本轮取回 SHA-256 |
|---|---|---|
| E01 | [Megatron parallel_state.py · core_v0.19.2](https://raw.githubusercontent.com/NVIDIA/Megatron-LM/core_v0.19.2/megatron/core/parallel_state.py)，L289–375 的维度/步长构组、L479–491、L859–907 的两套 generator 与 PP 一致性 | `1f6e23a01022c06be3b67f930095898e5032f6ff93695f8da5aae3b5a546dcf0` |
| E02 | [Megatron num_microbatches_calculator.py · core_v0.19.2](https://raw.githubusercontent.com/NVIDIA/Megatron-LM/core_v0.19.2/megatron/core/num_microbatches_calculator.py)，L367、L381–394 的有效 batch 与微批数关系 | `a540540481321f233a23355bd5857854e3bfc86d36e69f611d1c7b66dd8d494f` |
| E03 | [PyTorch grad_scaler.py · commit 1eba9b3…](https://raw.githubusercontent.com/pytorch/pytorch/1eba9b3aa3c43f86f4a2c807ac8e12c4a7767340/torch/amp/grad_scaler.py)，L355–365、L463–480、L521–531、L599–614 的 step/update/保存语义 | `eb4bc91fda9815ba40206e2dbb68f9845b85622fee3a92611f227b5845b20780` |
| E04 | [Megatron training.py · core_v0.19.2](https://raw.githubusercontent.com/NVIDIA/Megatron-LM/core_v0.19.2/megatron/training/training.py)，L2474、L2503、L2518–2531、L3941–3942 的成功/跳步与计数分支 | `d968ef8216f63d6373372190ac895fc905234c116bba3e804d2951876e6ad98c` |
| E05 | [PyTorch 2.6 AMP examples — Gradient accumulation](https://docs.pytorch.org/docs/2.6/notes/amp_examples.html#gradient-accumulation)，有效 batch 粒度、累积期间 scale 不变及窗口末 `step/update` 示例 | HTML `685b630c3e44dabfcc7f990805b811727a7369ab5b13bd800d7a4c1e420384bb`；按章节核对，不用 HTML 行号冒充源码坐标 |
| E06 | [PyTorch AmpKernels.cu · 同一 commit](https://raw.githubusercontent.com/pytorch/pytorch/1eba9b3aa3c43f86f4a2c807ac8e12c4a7767340/aten/src/ATen/native/cuda/AmpKernels.cu)，L181–215 的 scale/连续成功计数更新 | `c61b085b99c6422e5ba734e0f35b1b08e3acda3391f19796a40f79dbaa6d3e0e` |

## 8. 检查与交付边界

- 在包含当前未提交修订、本报告与原有构建文件的临时隔离副本中执行 `make check`：**PASS，103 content entries / 493 sources**。
- 在同一隔离副本执行 `make build`：**PASS**，仅在该副本生成 `build/catalog.json` 与 `build/catalog.md`。两项检查只验证结构和本地链接，不验证远程证据、技术结论、配置可启动性或训练恢复正确性。
- 原工作区 `build/` 不重建，不修改 `src/kb/`，不新增单元测试，不执行训练或硬件验证。

后续只需针对 C01 的候选组定义/放置和 S3-01 的计数器措辞修订后定向复核；无需以新增实测来补救一个尚未自洽的合成布局。通过条件仍按用户给定规则执行，不能以作者补充已写、报告已交付或结构构建成功直接宣布通过。
