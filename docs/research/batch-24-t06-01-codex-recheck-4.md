# Batch 24 · T06-01 Codex 定向复核第四轮

## 1. 结论与审阅范围

- 日期：2026-10-19（Asia/Shanghai）。仅复核第三轮仍 OPEN 的 **B24-T061-C01 / P2** 与 **B24-B24-T061-S3-01 / P3**；第三轮以前已 CLOSED 的项目不重查、不重开。验收表中未受本轮修订影响的结论明确承接第三轮，不冒称重新完成其上游取证。
- 两个上轮 OPEN 项均 **CLOSED**。新增 **B24-T061-S4-01 / P2 / OPEN**：选型表 EP 行把 expert-DP 的 stride 2 通信组标为“节点内”，但按该行 EDP=8 和公共节点公式，每组实际跨两个节点。
- **结论：暂不通过。** “全部上一轮 OPEN 项 CLOSED”已满足；“无新 OPEN P1/P2”未满足。本轮新增开放项为 P1 0、P2 1、P3 0；不将新发现重复计入已关闭的旧编号。
- 执行者：本会话 Codex，技术审阅角色；未派发子代理、未另起模型调用。当前上下文无可独立核验的实际模型、推理档位及路由元数据，均记为 **unknown**，不把仓库约定模型冒记为实际执行模型。
- 本轮只新增本报告。未修改正文、作者取证、来源登记、导航、计划或原工作区构建产物；未安装或运行训练框架、分布式进程组、checkpoint 保存/加载或 GPU/NPU 实验。

## 2. 输入、证据与方法

按仓库要求先读 `README.md`、[编写指南](../authoring-guide.md)、[内容归属](../../content-outline.md)与 `schemas/content.schema.json`。用户提示的 `docs/research/batch-24/t06-01-codex-recheck-3.md` 在当前仓库不存在；实际读取下表 R3，未创建替代路径。

| 简称 | 输入及本轮定位 | SHA-256 |
|---|---|---|
| P | [修订正文](../../knowledge/06-training/parallelism-and-state.md)，定向位置 L126–140、L201–207；验收覆盖位置见第 5 节 | `240d0d928983c8e50a20a4b5d40464a14dde8a59cf118c509eed771a298d1d94` |
| A | [作者取证](batch-24-t06-01-sources.md)，末尾 L122–124“修订轮四补充” | `a7b97d1f7d262deec9cb0a75a8178a112a4c3512a85a3d4afb384affadc29e32` |
| R3 | [第三轮报告](batch-24-t06-01-codex-recheck-3.md)，第 3.1 节 C01 剩余关闭条件、第 4 节 S3-01 与第 6 节验收 | `ea83206cff61b261b1c48d6374c191ace2d6cc527b09f28411626ee395fe8f7b` |
| T | [完整覆盖任务表](../../plans/full-coverage-backlog.yaml)，T06-01 L5832–5879 的目标与五条 acceptance | `53bfc8fe47d56ab322e546c853858cbaa90cf5a5d0305b33a80bab0f39275d54` |

Git HEAD：`bce9d978f58d71e180e46ca81069a152fb646ea0`。开始审阅时正文、registry、导航及若干其他审阅材料已有未提交改动，均不归为本轮产出。

作者补充仅说明“统一轴序与逐候选步长重算、修正放置标注；overflow 行 tracker 改为重置”，本轮不以补充的自述直接判定通过。采用两种核对：

1. 只读重开第 6 节三份精确上游文件，保留 TLS 校验，以原始字节的 SHA-256 和原文件行号核对；三份哈希均与第三轮对应记录一致。网页工具未能展示 CUDA 内核文件，但 curl 成功取得该精确文件；不把展示失败认定为上游不可达。
2. 审阅者用 Python 标准库整数/集合枚举正文声明的合成 grid，不导入、执行上游代码。按慢→快轴序生成所有坐标，核查 rank 覆盖、坐标唯一性、逐轴组分区和有序组内序号，再按 `node = rank // 8` 计算跨节点情况。不复算已 CLOSED 的 batch 问题，不重查既有 expert/参数 shard 身份项。

## 3. 第三轮 OPEN 项逐项判定

| 编号 / 优先级 | 判定 | 修订与依据 |
|---|---|---|
| **B24-T061-C01 / P2** | **CLOSED** | P L128 明确 dense 轴序 `[pp,dp,cp,tp]`、expert 轴序 `[pp,ep,edp,etp]`，均按候选大小重算步长，不再搬用旧样例的数值步长。L137 的 CP2/CP4 组例和节点内结论、L138 的 EP stride 16 与 ETP 节点内结论，均与公式相符。完整 grid 及有序组检查见 3.1。R3 指出的旧步长复用、CP4 错判跨节点和 EP stride 8 三处缺陷已消除。该行 expert-DP 的错误放置另按本轮新发现 S4-01 记录，不以关闭旧项豁免新问题。 |
| **B24-B24-T061-S3-01 / P3** | **CLOSED** | P L205 已改为 `update()` 执行、按 backoff 缩小 scale、重置 growth tracker，并明确“连续未跳步计数归零”。与固定 PyTorch CUDA 实现 E02 L188–190 一致。L204 仅写成功分支按增长策略调整 scale，未声称 tracker 无条件递增；E02 L194–204 的增长间隔触发重置与之不冲突。E03 L608 也把 tracker 定义为连续未跳步次数。仅关闭本项精确措辞问题，不重开已 CLOSED 的 C06。 |

### 3.1 C01：统一构组规则与原错误的关闭证据

P L128 的 dense 公式为：

`rank = ((pp_idx × DP + dp_idx) × CP + cp_idx) × TP + tp_idx`。

expert 轴同理得到：

`rank = ((pp_idx × EP + ep_idx) × EDP + edp_idx) × ETP + etp_idx`。

这是**作者声明的合成顺序**，不是 Megatron 默认 order 的验证。上游 E01 L322–375 体现了组成员由有序维度大小及其乘积步长共同确定的机制；不能只看 stride 数字就判断是否节点内。以下结果来自本轮独立枚举。

| 候选 / grid | 轴大小，均按慢→快排列 | 重算步长 | 相关组的跨节点结果 |
|---|---|---|---|
| 纯 DP、FSDP `FULL_SHARD` | dense `(1,64,1,1)` | `(64,1,1,1)` | DP 1 组，每组覆盖 8 节点 |
| TP2 配 SP | dense `(1,32,1,2)` | `(64,2,2,1)` | TP 32 组全部节点内；DP 2 组均跨 8 节点 |
| PP2、VPP（物理 PP2，vp2 不另作 rank 轴） | dense `(2,32,1,1)` | `(32,1,1,1)` | PP 32 组均跨 2 节点；DP 2 组均跨 4 节点 |
| CP2 | dense `(1,32,2,1)` | `(64,2,1,1)` | CP 32 组全部节点内；DP 2 组均跨 8 节点 |
| CP4 | dense `(1,16,4,1)` | `(64,4,1,1)` | CP 16 组全部节点内，每节点两个组；DP 4 组均跨 8 节点 |
| EP4 行的 dense grid | dense `(1,32,1,2)` | `(64,2,2,1)` | TP 32 组全部节点内；dense DP 2 组均跨 8 节点 |
| EP4 行的 expert grid | expert `(1,4,8,2)` | `(64,16,2,1)` | EP 16 组均跨 4 节点；ETP 32 组全部节点内；**expert-DP 8 组均跨 2 节点，见 S4-01** |

分别枚举纯 DP、FSDP、TP、PP、VPP、CP2、CP4、EP dense 与 EP expert，共九个 grid 实例。每个实例均恰覆盖 `0..63`，无重复坐标映射、无缺失或越界；对每个轴，固定其余坐标生成的组覆盖全体 rank 且互不重叠，每组大小正确、成员顺序对应轴坐标，组内序号检查通过。

原三处错误的具体替换结果：

- CP2：`rank = 2×dp + cp`，首组 `[0,1]`，而非旧 `[r,r+2]`；32 个组均不跨节点。
- CP4：`rank = 4×dp + cp`，组为 `[4k,4k+1,4k+2,4k+3]`（`k=0..15`）；16 个组均不跨节点。
- EP4/EDP8/ETP2：`rank = 16×ep + 2×edp + etp`。rank 37 的 EP 组 `[5,21,37,53]`，分别位于节点 `[0,2,4,6]`；ETP 组 `[36,37]` 同在节点 4。正文现在的 EP stride 16、ETP 相邻对标注正确。

因此关闭 C01 所记载的旧缺陷；**不据此宣布整行放置标注全部正确**，新发现按下一节独立处理。

## 4. 新发现

### B24-T061-S4-01 · P2 · OPEN：expert-DP 的八成员 stride 2 组并非节点内

- **位置：**P L138，EP 候选中的“expert-DP 组 stride 2 节点内”；公共物理放置与公式在 P L128。
- **可复算依据：**该候选 EDP=8、ETP=2、EP=4、PP=1。固定 expert 轴的 `ep=e`、`etp=t`，扫描 `edp=d`，得到完整 expert-DP 组：`G_EDP(e,t) = [16e + 2d + t | d=0..7]`，其中 `e=0..3`、`t=0..1`。首组 `[0,2,4,6,8,10,12,14]` 的节点为 `[0,0,0,0,1,1,1,1]`；不是单一节点。全体 8 个 expert-DP 组均跨两个节点，每个节点各有 4 个成员。
- **指定 rank 反例：**rank 37 对应 expert 坐标 `(pp=0,ep=2,edp=2,etp=1)`，其 expert-DP 组为 `[33,35,37,39,41,43,45,47]`，覆盖节点 4、5；rank 37 的组内序号为 2。ETP `[36,37]` 节点内与这个结论并不冲突，不能把 ETP 的相邻对放置转用于 expert-DP。
- **与 C01 的关系：**原报告指出的 CP2/CP4/EP 步长与组例已经修正、完整构组规则也已自洽；本项单列本轮确认的 expert-DP 放置错误，避免在同一缺陷上同时开放新旧两个编号。构组正确与文字把该组误标成节点内是两个层次，前者通过不使后者成立。
- **影响与分级：**固定选型场景明确假设节点间带宽低于节点内。错误地将 expert-DP 通信域归入节点内，会误导读者对专家副本同步通信成本及并行放置取舍的分析，直接影响任务验收第 2 条，因此为 **P2**，而非仅格式或术语 P3。这里只确认合成组的节点覆盖，不推断实际框架采用该顺序或断言任何测量性能。
- **关闭条件：**在保留当前合成公式与 EDP=8 时，将该短语明确修正为“expert-DP 组 stride 2，每组 8 rank，跨 2 节点”，并给出一个与公共节点公式一致的组例。若作者选择改放置而保留“节点内”，须同时重新声明可枚举的 expert order/组成员，保证全 64 rank 覆盖、ETP/EP/EDP 分区与相应节点结论一致；不能只改其中一句来掩盖布局冲突。只需对这处修订做定向复算，无需补训练或带宽实验。

## 5. T06-01 验收条目重新核对

验收来自 T 的五条 acceptance；未受本轮修订影响的已验收部分只检查覆盖位置并承接 R3，不重新审阅第三轮已 CLOSED 项。

| 任务验收 | 位置及本轮判定 | 状态 |
|---|---|---|
| 1. EP dispatch/combine、专家负载与通信；CP/SP 与 TP 的精确实现区别 | P L60–80 保留机制、来源与版本边界；未受本轮两处修订影响，不重开已关闭职责/兼容性问题的上游证据。 | **维持第三轮满足结论** |
| 2. 固定模型/序列/batch/拓扑，比较内存、通信、bubble、偏斜与扩展，无无条件最佳配置 | P L126–140 的统一公式已消除 C01 原错误；但 L138 的 expert-DP 节点内标注与同一公式矛盾。合成假设、无测量和无最佳配置声明不能豁免该静态错误。 | **部分满足：S4-01 / P2 / OPEN** |
| 3. global/group rank、mesh、stage、expert、shard 身份及冲突检查 | P L82–104 的身份样例承接第三轮已满足结论，不重查 C02 等既有 CLOSED 项；本轮选型 grid 的覆盖、唯一性及组内序号核对通过，物理放置标注错误单列于验收第 2 条。 | **维持第三轮满足结论** |
| 4. forward/backward/accumulation/update/scaler/data commit 的边界、所有权与合法跳步 | P L186–207 保留阶段责任与累积窗口三情形表；本轮只核实 L205 tracker 重置及相邻成功分支没有相反表述。S3-01 已关闭，不重新审阅 C06。 | **满足本轮定向范围；S3-01 CLOSED** |
| 5. 映射、梯度/更新、吞吐扩展、负载与恢复判据；有来源实现例与明确合成反例 | P L221–232 仍保留判据、固定版本官方配置例及明确的条件式静态反例；不重新打开已 CLOSED 的配置约束或反例问题。 | **维持第三轮来源与文字范围的满足结论** |

主归属和稳定 ID 仍为 `knowledge/06-training` / `training.parallelism-and-state`；正文仍保持 `draft / source_checked`。本轮不升级编辑或实验验证状态，不把合成枚举当成框架可启动性、实际 order、后端兼容性或 GPU/NPU 硬件验证。

## 6. 本轮重开的精确上游证据

只保留精确链接、定位与原创摘要，不在仓库保存上游源码快照或大日志。源码行号以 curl 取得的原文件为准，不采用网页转换后的行号。三份均属于既有版本/提交的核查，不修改来源登记或作者取证。

| 编号 | 一手来源与本轮使用范围 | SHA-256 |
|---|---|---|
| E01 | [Megatron parallel_state.py · core_v0.19.2](https://raw.githubusercontent.com/NVIDIA/Megatron-LM/core_v0.19.2/megatron/core/parallel_state.py)，L289–375，重点 L322–375 的乘积步长、坐标分解与有序构组；不据此宣称正文合成轴序就是默认 order | `1f6e23a01022c06be3b67f930095898e5032f6ff93695f8da5aae3b5a546dcf0` |
| E02 | [PyTorch AmpKernels.cu · commit 1eba9b3aa3c43f86f4a2c807ac8e12c4a7767340](https://raw.githubusercontent.com/pytorch/pytorch/1eba9b3aa3c43f86f4a2c807ac8e12c4a7767340/aten/src/ATen/native/cuda/AmpKernels.cu)，L188–204 的 overflow 归零、成功计数及增长间隔重置；仅作该 PyTorch CUDA 实现证据，不推广为 NPU 内核验证 | `c61b085b99c6422e5ba734e0f35b1b08e3acda3391f19796a40f79dbaa6d3e0e` |
| E03 | [PyTorch grad_scaler.py · 同一 commit](https://raw.githubusercontent.com/pytorch/pytorch/1eba9b3aa3c43f86f4a2c807ac8e12c4a7767340/torch/amp/grad_scaler.py)，L599–614，tracker 连续未跳步次数定义与 `update()` 后保存说明 | `eb4bc91fda9815ba40206e2dbb68f9845b85622fee3a92611f227b5845b20780` |

## 7. 检查与交付边界

- 独立合成枚举：九个 grid 实例的覆盖、唯一性、逐轴组分区及有序组内序号检查通过；expert-DP 的节点覆盖得到 S4-01，不能把枚举程序断言通过写成正文全部标注通过。
- 在包含本报告与当前未提交文件的隔离副本中执行 `make check`：**PASS，103 content entries / 493 sources**；执行 `make build`：**PASS**，仅在该副本生成 `build/catalog.json` 与 `build/catalog.md`。使用原工作区既有虚拟环境的 Python 作为解释器，未安装依赖；原工作区 `build/` 不重建。
- 对审阅开始时记录的 499 个现有文件逐一比较 SHA-256，并核对新增/删除清单：现有文件变更 0、删除 0，唯一新增文件为本报告；比较范围包含原工作区既有 `build/` 文件。
- 未修改 `src/kb/`，不新增单元测试，不执行训练、恢复或硬件验证。结构检查不证明远程内容、技术结论或模型路由正确。

后续只需修订 S4-01 的 expert-DP 放置标注，并对该项定向复核。当前不得以“原 OPEN 已全部关闭”单独宣布通过，仍须同时满足没有新 OPEN P1/P2 的验收条件。
