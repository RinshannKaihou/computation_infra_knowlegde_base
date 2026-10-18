# Batch 24 · T06-01 Codex 定向复核报告

- 复核日期：2026-10-18。
- 结论：**暂不通过**。
- 初审发现 B24-T061-C01–C09：**CLOSED 4 项、OPEN 5 项**；剩余 OPEN 为 C01、C02、C05、C06、C07，沿用初审 P2 优先级。
- 新发现：**B24-T061-R01，P2 / OPEN，1 项**。合计当前 OPEN 6 项，其中 P1 0 项、P2 6 项、P3 0 项；不把同一初审问题的残留重复登记为新发现。
- 执行者：本会话 Codex，技术审阅角色；未派发子代理，未修改正文、导航、registry 或计划。唯一新增的仓库文件为本报告。
- 模型记录：当前会话没有可供本报告独立核验的实际模型标识、推理档位及路由元数据，记为 `unknown`；不据导航文字宣称实际运行了 `gpt-6.1-sol / xhigh`，也不虚构额外 CLI 审阅轮次。

## 1. 输入、定位与证据边界

已读取仓库 `README.md`、`docs/authoring-guide.md`、`content-outline.md`、`schemas/content.schema.json`，以及以下复核输入：

| 输入 | 本轮读取范围 / 快照 |
|---|---|
| [初审报告](batch-24-t06-01-codex-review.md) | 全文；逐项重读第 2 节 C01–C09 的原位置、证据和建议关闭条件 |
| [修订后正文](../../knowledge/06-training/parallelism-and-state.md) | L1–239；SHA-256 `7b1fe727823501d25d8e84b00a2bcc9f147320f756b45b9f67379611dfcfde29` |
| [作者取证记录](batch-24-t06-01-sources.md) | L1–106；SHA-256 `ba934c39907fa244072279e8d8621366181fe060a9afff4e2de49a4c3c1d2607` |
| [来源登记](../../sources/registry.yaml) | 正文全部 11 个 `source_refs` 对应条目，以及相关 `revision`、`notes`；SHA-256 `cfb95b9746f8405bf2c9f8d0101090fb9086a5a663c31d1d261693d3d700e59a` |
| [任务清单](../../plans/full-coverage-backlog.yaml) | L5832–5879：T06-01 的目标、五条验收、来源准备要求、关联主题与单篇修改范围 |
| 相邻章节与导航 | 训练入口、Checkpoint 恢复一致性章节，以及原有通信/存储分工与链接 |

以下“正文 L…”均指上述 **239 行修订快照**，不是初审的 212 行快照。初审报告 SHA-256 为 `51e1085eb1bb3bf3421216d2dd4bd5cd45f2c23bfe9c7eed3bb7fa52948f1193`。Git HEAD 为 `bce9d978f58d71e180e46ca81069a152fb646ea0`；开始时已有未提交改动，不归为审阅者修改。

**补充材料实况：**本轮实际取得的取证文件止于 L106 的 YAML 代码围栏。CLI 更正位于 L42、L54；未见 L106 之后另附的“静态代入说明”。因此静态代入以正文 L122、L222 的实际文字独立复算，不把用户提及但文件中未出现的附录当作已读证据。此项只记录输入边界，不单独计技术发现。

独立取证采用固定 tag/commit raw 文件及 PyTorch 2.6 版本化页面，索引为附录 E01–E18。源码坐标均来自 curl 实际取回文件的 LF 原始行号，未将网页阅读工具转换后的行号用于 GitHub 源码锚点。初次 Python HTTPS 请求遇到本机 CA 校验错误，随后改用 curl，**未关闭 TLS 校验**；18 个精确 URL 最终均返回 HTTP 200。网页工具读取 MindSpeed arguments 时的内部错误，也已由同 URL 的 curl 200 与字节核对补足，不误报为上游不可达。

固定 raw 文件可与初审/作者哈希比较者均一致；版本化 HTML 的字节哈希有差异，按本轮实际内容复核，不仅凭哈希差异推断技术内容改变。没有安装、导入或运行上游训练代码；没有启动进程组、训练、checkpoint 保存/加载或硬件实验。

## 2. 初审发现逐项判定表

| 编号 / 原优先级 | 原位置与关闭条件重核 | 修订后定位、上游依据与判定理由 | 状态 |
|---|---|---|---|
| B24-T061-C01 / P2 | 初审正文 L101–115；要求合成固定拓扑、模型/精度、完整候选并行度及 micro-batch/累积数，限定全分片策略，撤回无依据性能泛化 | 正文 **L126–138** 已增加 8×8 不对称拓扑、固定模型尺寸与 `FULL_SHARD` 限定，撤去通用 8 卡上限、固定通信次数和高通信占比断言；E10、E11 支持其机制边界。但除纯 DP/FSDP 外，TP/PP/VPP/CP/EP 行仍未补齐共同占满 64 ranks 的其余维度、各行 micro-batch/累积数与放置；精度亦未固定。全局 batch 的唯一示例还算错，见 R01。不能据此完成固定条件下的候选比较。 | **OPEN** |
| B24-T061-C02 / P2 | 初审正文 L82–88；要求至少一个进程具备可核算的全部身份，包括 expert-TP、expert-DP、EP/CP 关系、专家集合与 shard 归属 | 正文 **L86–102** 新增 rank 37 的 dense mesh 及 TP/CP/PP/dense-DP 成员，静态复算一致；E03 支持这种 mesh 表达。但 **L99 仍只有“某 32 个连续编号专家”占位，L102 将 expert-DP/expert-TP、EP 嵌套顺序列为 unknown**，没有 EP 组及组内 rank。E02 L479–491、L859–907 明确 dense/expert 两套 rank generator，不能用 dense 维度乘积与 `128 % 4` 替代专家身份核对。L100 的 `layers.3` 也未说明与 stage 16–31 的局部/全局编号对应。诚实标 unknown 合理，但并未满足样例验收。 | **OPEN** |
| B24-T061-C03 / P2 | 初审正文 L86、L188；要求区分原样恢复与受支持布局转换，不将物理布局完全相等作为通用必要条件 | 正文 **L86–102** 已去掉“不一致就会错位”的无条件判断；**L165–176、L215** 区分稳定逻辑身份和物理 rank，明确有证据的转换不要求 placement 相同，检查旧→新逻辑覆盖、唯一性与加载结果；第三方转换保持 unknown。E08 的 DCP 概述、`get_state_dict`/`set_state_dict` 支持这一限定；与既有恢复一致性章节的重分片边界一致。 | **CLOSED** |
| B24-T061-C04 / P2 | 初审正文 L88、L96、L204；要求分清硬断言、功能不支持和性能 warning，核对实际条件分支 | 正文 **L104–120、L231** 已分列硬断言、assert 排除、性能提醒和文档前提，明确 Hopper 及以前的 overlap 分支不因此拒绝启动。E01 **L1413–1435** 在硬件条件下调用 `warn_rank_0` 并允许按优先侧选 1/32；与紧随其后的另一 `else` 分支 assert 未混淆。初审的 warning 升级为硬失败问题已纠正。 | **CLOSED** |
| B24-T061-C05 / P2 | 初审正文 L97、L204 等；要求统一整除方向、补齐 GQA KV-repeat 分支，并做正反静态代入 | **正文 L113–114、L122、L231 的技术修订接受**：专家数取模方向正确，GQA 补上 TP 与未 repeat 时的 Ulysses 条件；E01 L1600–1603、E04 L247–263 可核对，48/52 的静态代入也正确。但**作者取证记录 L40 仍写“num_experts 须整除 EP size”**，与同一源码及正文方向相反，且无后续更正说明。该项未在本次交付材料中完整闭环；不是否定已经改对的正文公式。 | **OPEN** |
| B24-T061-C06 / P2 | 初审正文 L155–172；要求区分不序列化与不更新，说明累积未提交、overflow、不跳步成功更新三类边界及 scaler/scheduler/数据计数 | 正文 **L197** 已补两层含义，并按 E05 L2474、L2503、L2518–2531、L3941–3942 正确说明成功/失败时 scheduler、skipped iteration 与 consumed samples 分叉；应用 data commit 保留显式契约/unknown。**仍缺 scaler 在 overflow 跳过参数更新时如何变化，以及未完成累积时哪些更新不得提前发生。**L194 只谈序列化与截取，L197 回指的状态矩阵也只谈保存字段。E06 L355–365、L463–480、L599–614 明确“不执行参数更新”不等于“不执行 scaler 更新”。原关闭条件要求的三类执行边界尚未完整写出。 | **OPEN** |
| B24-T061-C07 / P2 | 初审正文 L195；要求反例隔离目标约束，不错误归因首次拒绝点，绕过后现象未取证则为 unknown | 正文 **L222** 已改为 CP4、heads 48→52；world-size、序列长和 head 取模均复算正确，绕过后的行为已改 unknown，接受这两部分。**但“单独违反…其余前置约束均满足”仍未被给定输入证明。**E04 L273–282 在 head 检查前先要求 `use_mcore_models`；该参数在 L116–117 为 `store_true`，正文未设定。E04 L1456–1479 还先调用配套 Megatron 校验；不能以另一版本 E01 的两个余数穷尽该前置链。它现在能证明目标 head 检查式不满足，尚不能证明所称单一启动拒绝。 | **OPEN** |
| B24-T061-C08 / P3 | 初审正文 L115 与 registry；要求替换失效后端页，重开登记一致且不越界的精确页面 | 正文 **L140、L237** 现链接到 PyTorch 2.6 `distributed.html`，与 registry **L3575–3588** 相符。E09 本轮 HTTP 200；核对 `Backends` 与第三方后端扩展说明。正文没有新增具体 ROCm/RCCL 版本兼容承诺，仍禁止将 NVIDIA 结论平移。关闭限于 URL 和边界修复，不把该通用页当作任意 AMD 环境兼容证明。 | **CLOSED** |
| B24-T061-C09 / P3 | 初审正文 L64；要求 router 形成路由/概率，dispatcher 消费映射，不把专家选择归给 dispatcher | 正文 **L64** 已明确 router 在先，dispatcher 消费 `routing_map`/`probs` 做重排和通信，算法由上层决定。E07 **L618–640、L698–716** 接收既有映射并执行 A2A，与 registry **L4697–4707** 已有“路由值由调用方决定”的边界一致；没有新增未经核对的 router 算法结论。 | **CLOSED** |

### 2.1 剩余关闭动作

以下是针对残留问题的建议，不是本轮已实施修改：

- **C01：**每行给出完整、可核算的 64-rank 候选，固定精度、micro-batch、累积数与组放置；逐行保持相同 global batch。拓扑可以是清楚定义的合成模型，不要求伪造带宽测量。未测效率继续写分析预期或 unknown。
- **C02：**明确选择自定义合成布局或指定框架布局。补出 rank 37 的有序 EP/expert-TP/expert-DP 组、组内编号、确切专家 ID、参数全局 FQN、tensor shape/shard 轴与 offset；将 stage 的局部层号转换写清。检查专家逻辑覆盖、合法副本和 shard 唯一归属，不能只验 dense 维度乘积。
- **C05：**同步更正取证记录 L40 的反向表述，例如统一为 `num_experts % EP == 0`；保留已正确的正文和 repeat 分支。该残留沿原编号记录，不另外生成 R 编号。
- **C06：**补一张三情形执行表：累积未提交、overflow/no-update、成功更新，分别说明参数/成功更新计数、scheduler、scaler 和数据进度。若用 PyTorch GradScaler 说明 scaler，就明确这是独立样板，不声称 Megatron 一定调用该类；若说明 Megatron 自有 loss scaler，另核对其固定实现。应用 data commit 不从 consumed samples 推导。
- **C07：**若只演示 `_check_attention_head` 的静态分支，显式以前置校验已满足为条件，并撤掉“其余均满足”的实证口吻；若仍声称整条启动路径只在该点失败，则补齐必要模型模式、GQA/KV、hidden/head 等输入和**实际配套版本**的前置校验依据，不跨用 core_v0.19.2 当作 MindSpeed v2.2.0 的配套 Mcore。

## 3. 新发现

### B24-T061-R01 — P2 / OPEN：固定 global batch 的合成示例算错

- **位置：**正文 **L126**，影响 **L128–138** 的固定 batch 候选比较及 L217 的固定 batch 吞吐判据。
- **问题：**正文将 global batch 512 的一组例子写成 micro-batch 1、梯度累积 8、dense DP 8。在普通不含额外 GTP 数据轴的合成设定中，这三个数给出的是 **`1 × 8 × 8 = 64`，不是 512**。TP、PP、CP 的 rank 不应再次作为独立数据副本乘进去；L86 已将 dense DP 明确算为 8。
- **上游依据：**E18 的固定 micro-batch calculator **L367、L381–394** 使用 `num_micro_batches = global_batch_size // (micro_batch_size * data_parallel_size)`；E05 **L2522–2526** 的 scheduler 样本增量也区分 DP 与额外、显式存在时的 GTP 轴。本例未声明额外 GTP 数据轴，不能事后补乘物理卡数弥补错误。
- **影响：**读者按该示例会得到不同有效 batch 和 micro-batch 数，进而改变 PP bubble 填充及 scheduler/样本计数语义；不能用于声明固定 global batch 的公平比较。此为修订中新出现的确定性数值错误，区别于 C01 原有的配置不完整。
- **建议关闭条件：**保持 micro-batch 1、DP8、global batch 512 时，应把累积/micro-batch 数改为 **64**，或提供其他乘积确为 512 的完整组合；并将整张表各候选逐行复算。若选择其他 batch 口径或额外数据轴，必须先明确其实现定义和固定值。静态算术不标成训练或性能实验。

除 R01 外，没有另行登记新的 OPEN P1/P2。rank 37 的 expert 身份和层号问题沿 C02，反例前置条件沿 C07，不重复计数。

## 4. 独立静态核算记录

本节为本轮审阅者执行的**整数与集合枚举**，没有导入上游代码，不是 CLI 解析、启动校验、collective 或训练测试。

| 核算对象 | 实际核算结果 | 支持范围 |
|---|---|---|
| Dense mesh | 枚举 `(pp,dp,cp,tp) ∈ 2×8×2×2`，映射 `32pp+4dp+2cp+tp`，得到 0–63 共 64 个唯一 rank | dense 坐标映射为双射，不证明 expert grid |
| rank 37 | 坐标 `(1,1,0,1)`；TP `[36,37]`/组内 1，CP `[37,39]`/组内 0，PP `[5,37]`/组内 1，dense DP `[33,37,41,45,49,53,57,61]`/组内 1 | 正文 L88–98 的这些具体值成立 |
| 专家数方向 | `128 % 4 = 0` | 支持正文修正；不支持取证记录 L40 的反向表述 |
| Ulysses head 正反例 | `divmod(48,4×2)=(6,0)`；`divmod(52,4×2)=(6,4)` | 前者满足、后者不满足 E04 L247–249 的 head 检查式 |
| GQA 补充分支 | TP2/Ulysses4，query groups 8：`8%2=0` 且 `(8/2)%4=0`；query groups 4：`4%2=0` 但 `(4/2)%4=2` | 后一组在 KV-repeat 关闭时违反补充分支；不是训练结果 |
| 新反例的两项前置 | `64 % (2×2×4)=0`；`32768 % (2×4)=0` | 只证明这两项整数约束，不证明完整 MindSpeed 前置链 |
| Global batch | `1×8×8=64`；要求 512 时，`512/(1×8)=64` 个 micro-batch | R01 的确定性反证 |

CLI 补证另核对：E12 **L95–107、L214–229** 确实从 dataclass 字段生成参数名并调用 `add_argument`；E13 中存在 TP/PP/CP/EP 配置字段，E01 引入相应参数工厂。作者取证 L42、L54 撤回“未找到字面量 CLI 定义就认为不存在”的更正成立。这里仍没有执行 CLI 解析，也不把“存在生成入口”升级成某一合成配置可成功启动。

## 5. T06-01 验收重核

| 验收条目 | 修订后核对 | 结果 |
|---|---|---|
| 1. EP dispatch/combine、负载与通信；CP/SP 与 TP 的实现化区分 | 正文 L60–80；C09 的职责归属已修正，E07 支持；CP/SP 与平台边界未扩大为跨平台可用性证明。正文 GQA 分支修正接受，但相应取证方向残留见 C05。 | **核心正文满足；取证闭环仍有残留** |
| 2. 固定模型/序列/global batch/拓扑，比较状态内存、通信、bubble、偏斜和效率；不承诺无条件最优 | 正文 L124–140；增加合成拓扑、`FULL_SHARD` 与 unknown，方向正确；各行完整候选/精度/累积/放置仍不足，global batch 例子错误。 | **未满足：C01、R01** |
| 3. global/group rank、mesh、stage、expert/shard 样例与冲突检查 | 正文 L82–122；dense 样例可核算，硬/软限制已分开；expert 身份仍是占位，不能完成全组合映射检查。 | **部分满足：C02、C05** |
| 4. forward/backward/accumulation/optimizer/scaler/data commit 所有权、边界与合法跳步 | 正文 L178–199；Megatron 更新与样本计数分叉已补，应用提交边界未越界；累积未提交与 overflow 的 scaler 行为仍未完成。 | **部分满足：C06** |
| 5. 映射、梯度/更新、吞吐扩展、负载、恢复判据；有来源实现例与明确合成反例 | 正文 L211–222；C03 的合法重分片边界已修正，E15 支持官方脚本的 TP1/PP4/EP16 配置；合成标签和绕过后 unknown 已补，但“仅一条启动约束失败”的前置链仍未证。 | **部分满足：C07；吞吐固定条件另受 R01 影响** |

任务 `source_discovery` 的边界继续保留：固定 NVIDIA、MindSpeed、PyTorch 版本相互不组成同一已验证软件栈；未执行上游测试；MindSpeed 核心仓外链、目标 NPU 配套及 PyTorch experimental CP 在 TorchNPU 的实际可用性不在本轮已证明范围。E14、E16 中厂商 CP/VPP 示例仅按其固定文档口径接受，不用作本库性能测量。

### 5.1 既有内容、元数据与跨章边界

- `training.parallelism-and-state` 的稳定 ID、`type: concept`、`domain: training`、`status: draft`、`platforms: [generic]` 保留，未产生第二个正文主归属。`updated_at: "2026-10-18"` 与本轮日期相符。
- 与 HEAD 比较，**状态责任矩阵、状态身份章节完整不变；原截取边界与 MindSpeed 样板文本仍完整保留**。C03 的修正与 `checkpoint-state-consistency.md` 的同布局恢复、改变 world size 及应用状态契约一致。
- 本轮没有把硬件/通信实现细节改归本页，也没有将 Checkpoint 文件持久性当成训练恢复正确性；原有通信、存储和恢复一致性链接仍承担各自职责。
- `verification.status: source_checked` 没有升级为硬件复现；来源 ID 和本地导航可解析不代表本报告中的 OPEN 项已解决。
- 导航中的模型文字不用于推定本次实际模型。任务计划仍为 `planned / needs_source_preparation / source_revision: null`，本轮不改计划状态。

## 6. 结构校验与写入范围

| 检查 | 本轮结果 | 边界 |
|---|---|---|
| `PYTHONDONTWRITEBYTECODE=1 make check` | 报告写入前后均退出 0：103 content entries / 491 sources | 仅结构、ID、引用和本地文件目标，不证明远程页面或技术结论 |
| `make build` | 在 `/private/tmp/b24-t061-recheck.jEhUgE/snapshot` 隔离副本执行，使用项目现有解释器，退出 0：103 entries / 491 sources | 复制原有 `build/catalog.*` 一并还原链接预检输入；未在原仓库改写 `build/`；构建不作为训练验证 |
| 写入范围核对 | 工作树状态相对开始时仅多本报告；正文、初审、取证记录与 registry 的四个 SHA-256 均未变化；报告无行尾空格 | 正文、取证记录、registry、导航与计划均未修改；未提交或建分支 |

未修改 `src/kb/`，不需要新增测试；未运行 `make test`。下载的上游文件和临时构建副本放在 `/private/tmp`，不把上游源码、日志或可变运行状态批量加入仓库。

## 7. 结论

**本轮暂不通过。** 初审 9 项中 CLOSED 4 项、OPEN 5 项；另有新发现 R01（P2 / OPEN）。尚不满足“全部初审发现 CLOSED 且无新 OPEN P1/P2”的通过条件。

后续应修订 C01、C02、C05、C06、C07 及 R01，再按实际修改位置做定向复核。已关闭的 C03、C04、C08、C09 不因其他条目开放而重新计为 OPEN；反过来，已完成的局部修正也不自动关闭剩余缺口。即使下一轮全部关闭，也只表示本任务的来源与技术文字审阅通过，不证明 GPU/NPU 兼容、吞吐收益或恢复正确性。

## 附录：本轮精确上游证据索引

以下 URL 均为本轮 curl 实际取回的原始目标，**HTTP 200**。SHA-256 为取回字节摘要，不是运行结果。源码行号按这些 raw 字节计数；HTML 使用页内章节/符号定位。

| 索引 | 精确上游证据 | 核对位置 / 用途 | SHA-256 |
|---|---|---|---|
| E01 | [Megatron arguments.py · core_v0.19.2](https://raw.githubusercontent.com/NVIDIA/Megatron-LM/core_v0.19.2/megatron/training/arguments.py) | L422–431 world size；L1291–1298 hidden/head 与 CP；L1413–1435 warning；L1600–1603 experts | `f7fad20bc0e0cd9ba4b9ba7e70fa1a1b77030dfd020a7edb50b1d3b3aa41ebf6` |
| E02 | [Megatron parallel_state.py · core_v0.19.2](https://raw.githubusercontent.com/NVIDIA/Megatron-LM/core_v0.19.2/megatron/core/parallel_state.py) | L479–491、L859–907：dense/expert grids 与 expert-DP | `1f6e23a01022c06be3b67f930095898e5032f6ff93695f8da5aae3b5a546dcf0` |
| E03 | [PyTorch device_mesh.py · v2.6.0](https://raw.githubusercontent.com/pytorch/pytorch/v2.6.0/torch/distributed/device_mesh.py) | L381–408：mesh 值、SPMD 与组成员例子 | `d16e1975093c53fd6e5415adf6c3f98093b7a03cc8123b905f5c8dfa13246012` |
| E04 | [MindSpeed-LLM arguments.py · v2.2.0](https://raw.githubusercontent.com/Ascend/MindSpeed-LLM/v2.2.0/mindspeed_llm/training/arguments.py) | L116–117、L242–286、L1456–1479：head/GQA 分支及先行校验 | `fd64204269ad1749159d9b98f47c91f92cb17de5075cb92670f8ab1d5df42a38` |
| E05 | [Megatron training.py · core_v0.19.2](https://raw.githubusercontent.com/NVIDIA/Megatron-LM/core_v0.19.2/megatron/training/training.py) | L2474、L2503、L2518–2531、L3941–3942：更新、scheduler 与样本计数 | `d968ef8216f63d6373372190ac895fc905234c116bba3e804d2951876e6ad98c` |
| E06 | [PyTorch grad_scaler.py · commit 1eba9b3…](https://raw.githubusercontent.com/pytorch/pytorch/1eba9b3aa3c43f86f4a2c807ac8e12c4a7767340/torch/amp/grad_scaler.py) | L355–365、L463–480、L599–614：overflow 跳过参数更新、scaler 更新/保存 | `eb4bc91fda9815ba40206e2dbb68f9845b85622fee3a92611f227b5845b20780` |
| E07 | [Megatron token_dispatcher.py · core_v0.19.2](https://raw.githubusercontent.com/NVIDIA/Megatron-LM/core_v0.19.2/megatron/core/transformer/moe/token_dispatcher.py) | L618–640、L698–716：接收路由与 A2A dispatch | `7af2746153268f5c5f7f03d7a340092541b633fbc8faa10f666d6ddbdf98be0a` |
| E08 | [PyTorch 2.6 DCP](https://docs.pytorch.org/docs/2.6/distributed.checkpoint.html) | 概述、`get_state_dict`、`set_state_dict`：受支持重分片及 canonical FQN | `ad4f2bc2dc743c92f59d1d24dd8b70dffae025b328973d9c982f7d5728be45ef` |
| E09 | [PyTorch 2.6 distributed](https://docs.pytorch.org/docs/2.6/distributed.html) | `Backends`、第三方后端扩展；正文与 registry URL 一致性 | `d1ff3826c6001ebcfb0b60b32896bce143e46c2424a97ce1cba968ce9939baef` |
| E10 | [PyTorch 2.6 DDP](https://docs.pytorch.org/docs/2.6/generated/torch.nn.parallel.DistributedDataParallel.html) | 梯度归约、应用输入切分责任；不提供无条件通信时延规律 | `521efaebb667e7679dd966f6e7e2d62f1f54f76086f7716547e8ad6c6b70b84a` |
| E11 | [PyTorch 2.6 FSDP](https://docs.pytorch.org/docs/2.6/fsdp.html) | `ShardingStrategy.FULL_SHARD`：参数/梯度/optimizer state 全分片 | `9721517343079f7bc5c78d00908108caf59ca943ec9c1c5e74adf1d32125ab1c` |
| E12 | [Megatron argument_utils.py · core_v0.19.2](https://raw.githubusercontent.com/NVIDIA/Megatron-LM/core_v0.19.2/megatron/training/argument_utils.py) | L95–107、L214–229：dataclass→CLI 参数工厂 | `4abf3e5e5571c5aa025dd8f716f483c6984fa7dbcf89931574d79fed728dc130` |
| E13 | [Megatron model_parallel_config.py · core_v0.19.2](https://raw.githubusercontent.com/NVIDIA/Megatron-LM/core_v0.19.2/megatron/core/model_parallel_config.py) | TP/PP/CP/EP dataclass 配置字段；CLI 更正补证 | `edd808ad5a1e613343d87f8a4fae87c2157125acbcf5ac1cbf9dc355d518859f` |
| E14 | [MindSpeed-LLM CP 微调文档 · v2.2.0](https://raw.githubusercontent.com/Ascend/MindSpeed-LLM/v2.2.0/docs/pytorch/features/fine-tuning-with-context-parallel.md) | L22–51：前提、算法和固定环境的 TP2/PP1/CP4 对照 | `f899c7292961f6c5cd69eb9e46ccb9e2099c9c86e9fb5ca7fbcd77cb810bdc51` |
| E15 | [MindSpeed-LLM GLM4.5-MoE A3 脚本 · v2.2.0](https://raw.githubusercontent.com/Ascend/MindSpeed-LLM/v2.2.0/examples/mcore/glm45-moe/pretrain_glm45_moe_106b_4k_A3_ptd.sh) | L16–18、L28–45、L48–72：官方组合实例，仅静态核对 | `5f065dbb1adb044c1224c4826653a56c8c1d0f581bd009c12d51d47403d3a028` |
| E16 | [MindSpeed-LLM VPP 文档 · v2.2.0](https://raw.githubusercontent.com/Ascend/MindSpeed-LLM/v2.2.0/docs/pytorch/features/virtual_pipeline_parallel.md) | L13、L19–26：通信/bubble 取舍和 16 层示例 | `126e2895b8f4499d72185d7dc47acc4e2aadf20f6cc4f92a02118b5cecb740c3` |
| E17 | [MindSpeed-LLM Ring Attention 文档 · v2.2.0](https://raw.githubusercontent.com/Ascend/MindSpeed-LLM/v2.2.0/docs/pytorch/features/ring-attention-context-parallel.md) | CP 算法与官方长序列适用边界；不外推 NPU 实际兼容性 | `c15aa4faecb39cdb9c28bf9bd00f6c2e980180671d62a40f3ab106db5b7304bf` |
| E18 | [Megatron num_microbatches_calculator.py · core_v0.19.2](https://raw.githubusercontent.com/NVIDIA/Megatron-LM/core_v0.19.2/megatron/core/num_microbatches_calculator.py) | L367、L381–394：global batch、micro-batch 与 DP 的整数关系 | `a540540481321f233a23355bd5857854e3bfc86d36e69f611d1c7b66dd8d494f` |

外部文件仅列精确链接、摘要与原创审阅判断，不搬入上游长段、图表或源码包，不改变仓库尚未选择统一再分发许可的状态。
