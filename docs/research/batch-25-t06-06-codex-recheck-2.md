# Batch 25 T06-06 第三轮定向复核报告

- 日期：2026-10-20（Asia/Shanghai）。本轮为第三轮修订后的定向复核，不是训练或硬件验证。
- 对象：[性能分解正文](../../knowledge/06-training/performance-analysis.md)、[第三轮修订记录](batch-25-t06-06-sources.md)、[组合身份页](../../knowledge/06-training/parallelism-and-state.md)，并对照[初审](batch-25-t06-06-codex-review.md)、[第二轮复核](batch-25-t06-06-codex-recheck.md)、[来源登记](../../sources/registry.yaml)与[任务验收条款](../../plans/full-coverage-backlog.yaml)。下列正文行号均针对本轮快照。
- 执行方式：当前本地 Codex CLI 会话独立复核，未委托其他审阅者。沿用任务约定 `gpt-6.1-sol / xhigh`；本轮没有可独立核验的 CLI 启动模型元数据，不把约定冒充已核验的实际模型。
- 写入边界：仅新增本报告；不修改正文、来源记录、registry、导航、任务状态或 `06.2-G3` 状态。未执行训练、profiling、checkpoint 恢复、优化复跑或设备操作。

## 一、结论摘要

**C01、C02、C03、R01 CLOSED；C04 仍为 OPEN（原 P2）。C05、C06、C07 保持 CLOSED，未发现回归。本轮无须新增 B25-T06-R2-xx 发现。** 累计 8 项发现中，7 项 CLOSED、1 项 OPEN；C04 的剩余缺口继续沿原 ID 跟踪，不重复计为新发现。

**整体判定：仍需修订，不声明 T06-06 通过既定审阅范围。** 五条通用验收要求本轮已满足其内容方法要求，但既定范围内的组合并行性能验证承接 C04 尚未闭环，`06.2-G3` 不建议关闭。这里不要求补造实测数值或开展硬件实验。

### 复核快照

| 文件 | SHA-256 |
|---|---|
| `knowledge/06-training/performance-analysis.md` | `b10fbb6453ef467c5a6d65fcee4c84eb54f33c6617216e40e2b029c0029dd1c2` |
| `docs/research/batch-25-t06-06-sources.md` | `6e335d8704f815cd7b45eb219f8cab59060be4e1c99c02f6a716e16032fa7f3d` |
| `knowledge/06-training/parallelism-and-state.md` | `d46cfcf6dc785de96fba9fcfb538e1d3453db2e4aa359d637c03d5f1307f9338` |
| `sources/registry.yaml` | `99b81d2047b01fc2ed7885143d062e6e0d7b44a0415db22dd63d1d9dd474857b` |

## 二、本轮待复核项

| 发现 ID | 优先级 | 判定 | 修订证据与判定依据 |
|---|---|---|---|
| B25-T06-C01 | P2 | **CLOSED** | 正文第 98 行明确分开 profiling 定位与最终收益测量：A/B/恢复 A 均关闭 profiler，保持计时配置及热身/缓存策略一致，细计时保留时声明同步边界；质量按配对输入、等有效 token/更新预算，预先规定指标、非劣阈值、采样位置和窗口长度，短窗口不外推完整收敛。第 92、95–96、128–129、134–137 行保留冻结训练状态、每条件恢复、重复基线、A→B→A 与无法等价比较时的否决条件。满足第二轮剩余关闭条件，不表示这些实验已经执行。 |
| B25-T06-C02 | P2 | **CLOSED** | 正文第 93–94 行不再以排名定根因，并已把区分方向写入各分支：PP 按生产者完成→发送/接收→消费者可执行的依赖边区分计划空泡与上游迟到；EP 把路由量、服务时间和暴露等待配对，以配对计数/受控对照区分工作量与单位效率，仅相关时保留候选；长度分支要求同 micro-batch 配对并作同类区分；通信分支直接移交已有判据；CPU/设备分支要求主机阻塞与设备可执行之间的依赖证据，只有准备工作不支持归因。缺少完整依赖链时统一进入“未解释空档”，结合第 91、116、136 行的完整性和最早阻塞边门禁，达到本轮最低定性规则要求，而非宣称已有通用量化阈值。 |
| B25-T06-C03 | P2 | **CLOSED** | 正文第 91 行补齐外层 step、mini/micro-batch 位置、schedule 推进点、continuous/discrete、active 范围及 cycle—文件身份，按预期阶段/rank/工作量核对完整性；说明 discrete 下其他阶段独立保存、update 只保存所选窗口，多 cycle 逐个保存核对。其 RL step/update mini-batch 区别及两种模式边界，与本轮重读的固定 verl 指南一致；PyTorch 的 Kineto 导出末 cycle 限制也已承接。 |
| B25-T06-C04 | P2 | **OPEN** | 正文第 109 行新增 A＝TP4×PP2×DP8、B＝TP4×PP4×DP4，身份页第 86 行也已补返回链接；这些进展认可。但第 109 行仍主要要求执行者“必须重算”“先过约束检查”“结果表逐条件记录”，没有把这些要求实际填写到该对照例。两套 grid、batch 换算、stage/layer 与采集 rank 的派生值，以及 A/B/恢复 A 结果记录结构仍未落地。不能仅凭 dense 乘积为 64 就确认完整候选合法并已演示如何比较。详见下一节。 |
| B25-T06-R01 | P3 | **CLOSED** | 正文第 92、96 行明确改为“主动实验”，说明恢复/复跑会改变训练状态，在授权的隔离实验副本及独立输出目录执行，保护冻结 checkpoint，不影响生产作业/恢复点；已有日志读取与实验复跑已区分。满足第二轮运行影响及授权边界的关闭条件，本报告不据此执行实验。 |

### C04 剩余缺口与最小关闭条件

**受影响位置：正文第 102–110、138 行；来源记录第 59 行。** 身份页回链这一子项已完成，不再作为开放理由；“说明性、非启动验证”的边界也正确。剩余问题是尚无一份真正填好的候选对照记录，而不是缺少实测吞吐。

1. **完整候选身份未定。** 新例没有明确 CP、ETP、EP、expert-DP 与其他因子的取值或继承规则。身份页第 90、112–114 行的原样例是 TP2/CP2/PP2、ETP2/EP4，并非新例的 TP4；原步长和专家组不能原样搬入。A/B 的 dense 三因子乘积均为 64 只支持有限的算术自洽，不能代替两套 grid 的覆盖、整除和 PP 组一致性检查。此处不判定 A/B 必然非法，而是不能据现有文字认定已给出一组完整、经静态核对的候选。
2. **联动关系仍是待填写清单。** 没有填写固定 global/micro batch 后每个条件的 micro-batch/累积数，也没有具体的 stage/layer 归属及 A/B 采集 rank。举例说明缺口：若明确采用身份页第 151–155 行的 global batch 512、micro-batch 1，并令 CP 与其他未启用因子为 1，则 A/B 的累积数应分别为 `512/(1×8)=64`、`512/(1×4)=128`。这是审阅者额外声明假设后的纯算术核对，不是正文已经交付的填写记录，更不是启动或性能验证。
3. **结果表只被提及，尚未交付。** 第 109 行列出需记录的指标，但没有 A、B、恢复 A 的条件行，读者不能沿该例核对各条件的配置/采集身份、分解项和收益判读；来源记录第 59 行概括为已补“结果表”，比实际正文更充分。该差异是同一 C04 的交付证据不足，不另报新 ID。

**最小关闭条件**：保留现有模板与回链，在其下真正填写一组 A/B 对照：明确模型/拓扑与未启用维度；写出 dense/expert DP、micro-batch/累积数、stage/layer/expert 归属和代表 rank/组成员的联动结果；将适用的固定实现约束代入并记录静态核对结论；提供 A/B/恢复 A 的结果表。静态字段应有推导值，吞吐、质量、实际等待边和恢复复测等未执行字段可以全部标“未执行/unknown”，不要求实测数值或命令。来源记录同步如实说明，随后仅对 C04 定向复核。

上述要求延续初审及第二轮的“一组合法候选如何沿入口比较”，不是新增验收范围。Megatron 固定源码的[两套 grid 与 PP 组检查](https://github.com/NVIDIA/Megatron-LM/blob/4b4acac9a1d28ea6829c8d4f566d75698a21249d/megatron/core/parallel_state.py#L871-L907)及[固定 batch 的 micro-batch 计算](https://github.com/NVIDIA/Megatron-LM/blob/4b4acac9a1d28ea6829c8d4f566d75698a21249d/megatron/core/num_microbatches_calculator.py#L367-L395)支持为何需要填写这些派生项；本报告没有替作者选定或启动一个新配置。

## 三、已关闭项的回归检查

| 发现 ID | 判定 | 本轮核对 |
|---|---|---|
| B25-T06-C05（P2） | **保持 CLOSED** | 正文第 70 行、来源记录第 49 行与 registry 均保留 2025.3 目录证据和 verl 镜像 2025.6.1 使用面分立，不再将 OS runtime 列为已核对能力。本轮重新读取固定 Dockerfile，确认版本声明及安装路径指向 2025.6.1；只证明该文件的构建指令，不证明镜像构建成功或现场兼容。未重开既有能力/版本边界问题。 |
| B25-T06-C06（P3） | **保持 CLOSED** | 正文第 63、98、120、126 行保留 start/stop 的 CUDA synchronize、interval-time 的 barrier、计时开关对照和部分 rank 不得随意加组 barrier。本轮重读 `Timer` 与 `training_log` 固定源码吻合；读取已有日志和新增细计时仍被明确区分，未回归为零扰动替代。 |
| B25-T06-C07（P3） | **保持 CLOSED** | 正文第 82、94、117、127 行可直接进入 collectives/带宽退化指南，带宽退化指南第 41 行保留返回本页链接；数据饥饿、供电散热链接与 06 章第 51 行入口存在。身份页新回链未破坏既有导航，不要求每篇机械双向链接。 |

## 四、本轮独立来源核对与限制

本轮重新读取相关上游内容，不将作者修订摘要直接作为关闭依据。通过 GitHub tag API 确认 verl `v0.9.1` 仍解析到 `1876b06d0a3e4e71e06230be10af14492ca8a75b`；Megatron 沿用既定冻结 commit `4b4acac9a1d28ea6829c8d4f566d75698a21249d`。表内 SHA 为 GitHub 返回的文件 blob 身份，不与本地快照 SHA-256 混称。

| 精确来源 | 本轮核对位置与支持范围 |
|---|---|
| [PyTorch 2.6 profiler](https://docs.pytorch.org/docs/2.6/profiler.html) | `profile`、`schedule`、`step`、`export_chrome_trace`：调用者推进计步，Kineto 导出只含末 cycle；shape/stack 采集有额外开销。支持 C01 的独立收益复测理由及 C03 导出边界，不提供本库实验的质量阈值。 |
| [verl torch 指南](https://github.com/verl-project/verl/blob/1876b06d0a3e4e71e06230be10af14492ca8a75b/docs/perf/torch_profiling.md#L152-L204) | “Scheduling the update loop's mini-batches”及第 250–335 行的跨进程阶段、缺阶段/缺设备活动说明；与 C02 的未解释空档和 C03 的窗口身份相符。blob `04d0903ba3b97f8bba285ac962b53b027d5489c9`。 |
| [verl Nsight 指南](https://github.com/verl-project/verl/blob/1876b06d0a3e4e71e06230be10af14492ca8a75b/docs/perf/nsight_profiling.md#L11-L40) | Prerequisites 仍引用旧 Dockerfile 名；两级控制、rank/discrete 和落盘说明未改变其使用面边界。blob `f8665b42a01d52b39fdf4f923b35dd376c6172a1`。 |
| [Dockerfile.stable.sglang](https://github.com/verl-project/verl/blob/1876b06d0a3e4e71e06230be10af14492ca8a75b/docker/Dockerfile.stable.sglang#L9) | 第 9、52–60 行声明、安装并链接 Nsight 2025.6.1；不据此推定 Nsight 2025.3 工具能力。blob `76fb2ffb4afc9a37b1c0b8b03ef26e00b7b7ab11`。 |
| [Megatron timers](https://github.com/NVIDIA/Megatron-LM/blob/4b4acac9a1d28ea6829c8d4f566d75698a21249d/megatron/core/timers.py#L109-L168)及[training_log](https://github.com/NVIDIA/Megatron-LM/blob/4b4acac9a1d28ea6829c8d4f566d75698a21249d/megatron/training/training.py#L2824-L2833) | 同步、可选 barrier、默认全局 communicator 以及 `elapsed(barrier=True)` 与正文一致。blob 分别为 `78204ad243f068e0944d1f54f113780363003a78`、`57b8efe9390eca9ca8596ed5bb073ed62d9d014d`。 |
| [Megatron parallel_state](https://github.com/NVIDIA/Megatron-LM/blob/4b4acac9a1d28ea6829c8d4f566d75698a21249d/megatron/core/parallel_state.py#L871-L907)及[num_microbatches_calculator](https://github.com/NVIDIA/Megatron-LM/blob/4b4acac9a1d28ea6829c8d4f566d75698a21249d/megatron/core/num_microbatches_calculator.py#L367-L395) | ETP 默认值、expert-DP 整除、两套 PP 组相同，以及固定 global/micro/DP 下的累积数。blob 分别为 `2a3c75811221aacaa0130f8feb081859788f3c5d`、`033820f174a6ed8d66853ae89b09220554f27341`。仅用于静态关系核对，不声称初始化进程组。 |

部分 GitHub 精确 URL 经网页工具读取出现 cache miss，随后通过 GitHub 连接器按同一固定 ref 读取成功；不把首次失败解释为文件不存在。本轮未重新取得 Nsight 2025.3 目录/子页、CANN msprof、AMD 指定版本页面或全部 NPU profiler 源码，不追加独立确认其取回状态，也不拿其他版本补证。既有工具能力、版本配套、CLI、新旧 rocprof 边界和运行扰动的 unknown 继续保留；这些边界不妨碍关闭本轮方法项，但不是硬件验证。

## 五、验收条款 1–5 与整体判定

| 验收条款 | 本轮判定 | 依据与范围 |
|---|---|---|
| 1. 固定有效产出、模型/精度/并行/global batch/拓扑/缓存，禁止重叠相加 | **通用要求满足** | 正文第 52–63、92、98 行保留口径、重叠约定与等价状态；不把字段清单等同于 C04 的候选记录已经填好。 |
| 2. 工具范围、扰动、版本与时间关联，未知细节不写命令 | **既定取证范围内满足** | C03 已关闭，C05/C06 无回归；第 67–74、91、98、126 行保留平台/版本边界、窗口完整性及扰动说明。msprof、Nsight 子页、新旧 rocprof 等未取得内容继续 unknown，不表示工具或版本组合支持已经验证。 |
| 3. PP/EP/长度/通信/CPU-设备同步/隐藏等待，区分受害与最早瓶颈 | **方法要求满足** | C02/C03 已关闭；阶段排名仅为候选，依赖边回溯、分支区分与未解释空档出口明确。现场仍须取得足以支持具体根因的证据。 |
| 4. 单因素、重复基线/恢复、吞吐与质量共同判据，不以高利用率替代效率 | **方法要求满足** | C01/R01 已关闭；冻结起点、重复窗口、A→B→A、关闭 profiler 的收益复测、配对预算与有限结论齐全，高利用率反例仍在。 |
| 5. 准备、分支、终止/恢复、无效反例及数据/通信/供电链接 | **通用要求满足** | 第 76–98、112–139 行有证据、流程、分支、停止/恢复与反例；C07 及主动实验影响边界无回归。 |
| 既定承接项：06.2-G3 组合映射/性能验证 | **保持 OPEN** | C04 只完成候选数值对和回链，未完成合法候选沿模板比较的具体填写例；这是本轮唯一剩余开放项。 |

**最终整体判定：需继续修订 C04，暂不通过既定审阅范围。** 后续只需补齐该项并定向复核；已关闭项不因 C04 重复打开。正文继续保持 `draft / source_checked`、空 `environment_refs` 与未实测声明，本报告不更改任务/主题状态。

## 六、结构校验与交付边界

- 已执行 `make check`、`make build`，两者均通过：`107 content entries; 525 sources`；生成 `build/catalog.json` 与 `build/catalog.md`。本报告的本地 Markdown 链接另行核对目标文件存在。
- 校验后复算正文、来源记录、身份页、registry 与第二轮报告的 SHA-256，均未改变；与写入前工作区状态相比，仅新增本报告这一源文件。
- `make check`/`make build` 只验证结构与本地引用，不证明技术因果、远程资料可达性、版本兼容或硬件正确性。
- 本轮不修改 `src/kb/`，无需新增测试；未开展训练或硬件测试。保留工作区原有其他变更，构建产物仅按仓库要求生成。
