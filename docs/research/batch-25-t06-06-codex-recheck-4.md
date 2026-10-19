# Batch 25 T06-06 第五轮定向复核报告

- 日期：2026-10-20（Asia/Shanghai）。复核作者第五轮修订，不是训练、启动、profiling 或硬件验证。
- 对象：[性能分解正文](../../knowledge/06-training/performance-analysis.md)第 100–132 行、[来源记录](batch-25-t06-06-sources.md)第 66–68 行；结合[组合身份页](../../knowledge/06-training/parallelism-and-state.md)第 84–125 行，按[第四轮复核](batch-25-t06-06-codex-recheck-3.md)的剩余关闭条件核对 C04。其余七项对照[初审](batch-25-t06-06-codex-review.md)、[第二轮复核](batch-25-t06-06-codex-recheck.md)及[第三轮复核](batch-25-t06-06-codex-recheck-2.md)做回归检查。正文行号均针对下列快照。
- 执行与模型核验：当前本地 Codex CLI 会话独立复核，未委托其他审阅者。按 `CODEX_SESSION_ID` 定位本会话唯一 JSONL，仅提取 `turn_context` 的模型与推理字段，得到单一 `model=gpt-6.1-sol`、`effort=xhigh`；本轮报告无模型回退标记，历史实际模型记录不改写。
- 写入边界：仅新增本报告；不修改正文、来源记录、[来源登记](../../sources/registry.yaml)、导航、[任务清单](../../plans/full-coverage-backlog.yaml)或主题状态，不执行任何训练与设备操作。

## 一、结论摘要

**B25-T06-C04：CLOSED（原 P2）。** 正文第 119–121 行已实际填入 B 的 dense/expert 坐标、具体组成员、stage/layer/expert 归属与采集 rank，不再只有“重算”“各取一个”等待填要求；来源记录第 68 行与交付相符。下述独立复算全部通过，满足第四轮剩余静态填写条件。

**C01、C02、C03、R01、C05、C06、C07 均保持 CLOSED，未发现回归；本轮没有新增开放问题。累计 8 项发现全部 CLOSED，OPEN 为 0。**

**最终整体判定：T06-06 通过既定审阅范围。** 这里通过的是内容、来源边界、组合映射/对照设计及静态候选记录的审阅，不是性能收益或硬件正确性验证。`06.2-G3` 在本页承接的内容审阅阻塞已消除；本报告不代为更改其登记状态，也不将“性能验证方法已交付”改写成“性能实验已完成”。

### 复核快照

| 文件 | SHA-256 |
|---|---|
| `knowledge/06-training/performance-analysis.md` | `81249354f5bac3e9e303d0333ad5e9611e83fb00bccc7b36ff9db8bd79f91f0d` |
| `docs/research/batch-25-t06-06-sources.md` | `97e6364698ccce6b9e41946d6a5509f488349d181960e55998aee528dce38184` |
| `knowledge/06-training/parallelism-and-state.md` | `d46cfcf6dc785de96fba9fcfb538e1d3453db2e4aa359d637c03d5f1307f9338` |
| `sources/registry.yaml` | `6be465aebd3aa52ac672b532eb1d0af8ed4bdc3296c8c4a37dc3282ad55484fe` |
| `docs/research/batch-25-t06-06-codex-recheck-3.md` | `804f46074b0ba4ea127dfe0f1552c13d8d8d9a7994e58590c4486e1897a21d13` |

## 二、C04：B 的步长、坐标与组成员

### 适用假设及源码规则

沿正文与身份页的同一合成条件：world size=64，8 节点×8 卡，连续 8 个 rank 为一节点；32 层、128 专家，TP=ETP=2、CP=2、EP=4，仅 PP 从 A 的 2 改为 B 的 4；默认轴序，未启用的 GTP/EGTP 因子为 1。stage、层号、节点号均按样例从 0 起，层连续均分；不把该分配推广为任意模型或流水线调度。

固定 Megatron commit 的 [RankGenerator](https://github.com/NVIDIA/Megatron-LM/blob/4b4acac9a1d28ea6829c8d4f566d75698a21249d/megatron/core/parallel_state.py#L479-L556)与[默认初始化参数](https://github.com/NVIDIA/Megatron-LM/blob/4b4acac9a1d28ea6829c8d4f566d75698a21249d/megatron/core/parallel_state.py#L601-L620)规定默认 `tp-cp-ep-dp-pp` 轴序；[分组算法](https://github.com/NVIDIA/Megatron-LM/blob/4b4acac9a1d28ea6829c8d4f566d75698a21249d/megatron/core/parallel_state.py#L289-L373)按前缀乘积形成步长，前面的轴变化更快。[初始化两套 generator](https://github.com/NVIDIA/Megatron-LM/blob/4b4acac9a1d28ea6829c8d4f566d75698a21249d/megatron/core/parallel_state.py#L858-L907)中，dense 的 EP=1，expert 的 CP=1，expert DP 按 `64/(ETP×EP×PP×EGTP)` 推导，并断言两套 PP 组成员相等。因此不能把 dense DP 当作 expert DP，也不能在 expert grid 的乘积中再次乘 CP。

### 独立复算结果

| 核对项 | A：PP=2 | B：PP=4 | 判定 |
|---|---|---|---|
| dense DP 及快→慢步长 | DP=8；`tp/cp/dp/pp = 1/2/4/32` | DP=4；`tp/cp/dp/pp = 1/2/4/16` | 正确 |
| expert DP 及快→慢步长 | EDP=4；`etp/ep/edp/pp = 1/2/8/32` | EDP=2；`etp/ep/edp/pp = 1/2/8/16` | 正确 |
| rank 37 dense 坐标 | `(pp=1,dp=1,cp=0,tp=1)` | `(pp=2,dp=1,cp=0,tp=1)` | 正确；B：`37=2×16+1×4+0×2+1` |
| rank 37 expert 坐标 | `(pp=1,edp=0,ep=2,etp=1)` | `(pp=2,edp=0,ep=2,etp=1)` | 正确；B：`37=2×16+0×8+2×2+1` |
| dense DP 组 | `{33,37,41,45,49,53,57,61}` | `{33,37,41,45}` | 固定其他坐标，扫描 DP，步长 4 |
| expert DP 组 | `{37,45,53,61}` | `{37,45}` | 固定其他坐标，扫描 EDP，步长 8；副本数 4→2 |
| 两套 grid 的 PP 链 | `{5,37}` | `{5,21,37,53}` | 两套一致；PP 步长 32→16 |
| TP / ETP 组 | 均为 `{36,37}` | 均为 `{36,37}` | 不变；组内序号均为 1 |
| EP 组及节点放置 | `{33,35,37,39}`，节点 4 | `{33,35,37,39}`，仍在节点 4 | 不变；各成员整除 8 的商均为 4 |
| stage / layer | stage 1，层 16–31 | stage 2，层 16–23 | B 每 stage 8 层，`2×8=16` |
| 本地专家编号 | expert 64–95 | expert 64–95 | EP 组内序号仍为 2，`128/4=32`，起点 `2×32=64` |

专家编号依据为[本地专家索引规则](https://github.com/NVIDIA/Megatron-LM/blob/4b4acac9a1d28ea6829c8d4f566d75698a21249d/megatron/core/transformer/moe/moe_layer.py#L181-L194)。编号不变不意味着跨 PP stage 是同一参数副本；仍须结合层身份解释。正文第 117 行的“随步长变化重算”应理解为复算要求，第 120 行现已明确交付“EP 组及节点放置不变”的结果，不再据此推断 EP 放置实际改变。

**PP 一致性不是只比 stage 数。** B 的 dense 低位维度乘积 `2×2×4=16`，expert 低位维度乘积 `2×4×2=16`；两套全部 PP 链均为 `{residue,residue+16,residue+32,residue+48}`（`residue=0..15`）。rank 37 的 residue=5，恰得 `{5,21,37,53}`。本轮枚举核对的是全部 PP 组相等，而非只核对这一条代表链。

### 采集选点与既有对照字段

正文第 121 行填写的 B 选点是 PP 链 `{5,21,37,53}`，再从所列 dense DP、EP 组各取 rank 37；**去重后仍为 `{5,21,37,53}`，不是额外六个采集进程**。逐项对应如下，两套 grid 的 stage 身份一致：

| 采集 rank | PP stage | 连续均分层区间 |
|---|---|---|
| 5 | 0 | 0–7 |
| 21 | 1 | 8–15 |
| 37 | 2 | 16–23 |
| 53 | 3 | 24–31 |

这已把原先“4 个 stage 各取一个”的数量要求落成具体选点，并把 rank 37 接到实际 DP/EP 组。**它是代表 PP 链的静态采集方案，不是所有 TP/DP/EP 组或全部组员的完整观测证据。** 真正判断 TP 组内计算/通信、EP 路由偏斜时，仍需关联相应 TP `{36,37}`、EP `{33,35,37,39}` 的组员事件和工作量证据；不得用 rank 37 单点替代全组结论。该限制受正文第 91 行完整性门禁、第 94 行依赖证据要求及第 107 行分解要求约束；当前没有声称这些未执行的观测已经完成，不据此新增全量采集或硬件实验的关闭条件。

已完成字段也未回归：正文第 114–118 行给出 dense DP 8→4、expert DP 4→2、层数 16→8，固定 global batch=32、micro-batch size=2 时，`num_micro=32/(8×2)=2`→`32/(4×2)=4`，反算两边均为 32，且不重复计入 CP/EP。按[固定 batch 换算规则](https://github.com/NVIDIA/Megatron-LM/blob/4b4acac9a1d28ea6829c8d4f566d75698a21249d/megatron/core/num_microbatches_calculator.py#L367-L395)，两者均整除且至少为 1；所列 world-size、专家数、序列长度整除检查均通过，不等于通过全部启动约束。第 123–131 行保留 A/B/恢复 A 结果表，吞吐、质量、等待边和恢复复测仍为未执行/unknown，没有虚构收益。

**本地算术检查：PASS。** 使用独立 Python 枚举 A/B 的 dense/expert 四套 64-rank grid，检查 16 个单轴分组分区的无重无漏覆盖、全部 rank 的 stage 一致性、两套全部 PP 组相等、A/B 全部 EP 分组不变、上述 rank 37 身份/组员/专家编号、选点覆盖及 batch/整除关系。未导入上游训练代码，未初始化进程组；该检查仅证明合成映射自洽。C04 因此关闭，不把审阅者推导代替作者缺失字段——本轮所需字段已存在于正文。

## 三、其余七项的回归检查

| 发现 ID | 判定 | 当前正文与关联证据 |
|---|---|---|
| B25-T06-C01（P2） | **保持 CLOSED** | 第 92、95–98、150–159 行保留冻结权重/optimizer/LR/scaler/RNG/数据游标与输入身份、至少三次基线、A→B→A、关闭 profiler 的独立吞吐复测、配对输入与等预算质量观察及短窗口结论边界；新增组员表未越过这些门禁。 |
| B25-T06-C02（P2） | **保持 CLOSED** | 第 93–94、136–139、158 行仍将阶段排名作为候选；PP 沿生产者→通信→消费者回溯，EP/长度区分工作量与单位效率，通信/CPU 分支需依赖证据，无法解释的空窗记未解释空档；没有把布局算术当瓶颈原因。 |
| B25-T06-C03（P2） | **保持 CLOSED** | 第 91 行保留 RL step 与 update mini-batch 计步差异、continuous/discrete 边界、active/cycle—文件身份、多 cycle 保存及阶段/rank/工作量完整性门禁；本轮重读固定 verl 指南与 PyTorch 2.6 的末 cycle 导出规则，未见回归。 |
| B25-T06-R01（P3） | **保持 CLOSED** | 第 92、96 行明确恢复/复跑属于主动实验，须授权隔离副本、独立输出目录、保护冻结 checkpoint；第 150–151 行区分配置回退与状态恢复，等价状态不成立则降级为探索。静态候选表没有新增执行授权。 |
| B25-T06-C05（P2） | **保持 CLOSED** | 第 70 行、来源记录第 49 行与 registry 保持 Nsight 2025.3 目录证据、verl 实际镜像 2025.6.1 两条版本线分立；OS runtime 仍未核对。本轮重读固定 nsight 指南及实际 Dockerfile，未用后者证明 2025.3 能力或现场配套。 |
| B25-T06-C06（P3） | **保持 CLOSED** | 第 63、98、142、148 行保留 Timer 两端 synchronize、可选 barrier、interval-time 的 `elapsed(barrier=True)`、读已有日志/新增计时区别和禁止部分 rank 随意加组 barrier；与重读固定源码相符。 |
| B25-T06-C07（P3） | **保持 CLOSED** | 第 82–84、94、139、149 行的数据/通信/供电交接链接仍存在；带宽退化指南第 41 行、训练入口第 51 行及身份页第 86 行保留性能正文入口，未见导航回归。 |

## 四、独立来源复核与新问题检查

除第二节组映射与专家编号所列精确锚点，本轮重新取得以下既有来源的指定位置；未新增外部来源登记。Git blob SHA 为连接器返回值，不与本地 SHA-256 混用。

| 来源与固定位置 | 核对内容 | Git blob SHA |
|---|---|---|
| 第二节所列 Megatron `parallel_state.py`；`moe_layer.py` | 默认顺序、步长分组、两个 grid 的 PP 组一致性、EP 组内序号到专家编号 | 分别为 `2a3c75811221aacaa0130f8feb081859788f3c5d`、`48e78775a849575a9d46f95d900490ded4a5946d` |
| 第二节所列 `num_microbatches_calculator.py`；[arguments.py 第 422–431 行](https://github.com/NVIDIA/Megatron-LM/blob/4b4acac9a1d28ea6829c8d4f566d75698a21249d/megatron/training/arguments.py#L422-L431)、[第 1295–1298 行](https://github.com/NVIDIA/Megatron-LM/blob/4b4acac9a1d28ea6829c8d4f566d75698a21249d/megatron/training/arguments.py#L1295-L1298)、[第 1600–1603 行](https://github.com/NVIDIA/Megatron-LM/blob/4b4acac9a1d28ea6829c8d4f566d75698a21249d/megatron/training/arguments.py#L1600-L1603) | 固定 batch 换算与已列 world-size/序列长度/专家数整除要求 | 分别为 `033820f174a6ed8d66853ae89b09220554f27341`、`fd30984b38ae64e1207a948c71ef04dbaf5925da` |
| [verl torch_profiling.md 第 152–204 行](https://github.com/verl-project/verl/blob/1876b06d0a3e4e71e06230be10af14492ca8a75b/docs/perf/torch_profiling.md#L152-L204)、[第 250–335 行](https://github.com/verl-project/verl/blob/1876b06d0a3e4e71e06230be10af14492ca8a75b/docs/perf/torch_profiling.md#L250-L335) | mini-batch schedule、两种采集模式、跨进程阶段与缺失活动边界 | `04d0903ba3b97f8bba285ac962b53b027d5489c9` |
| [verl nsight_profiling.md 第 11–32 行](https://github.com/verl-project/verl/blob/1876b06d0a3e4e71e06230be10af14492ca8a75b/docs/perf/nsight_profiling.md#L11-L32)、[Dockerfile.stable.sglang 第 9–60 行](https://github.com/verl-project/verl/blob/1876b06d0a3e4e71e06230be10af14492ca8a75b/docker/Dockerfile.stable.sglang#L9-L60) | 指南旧文件名与实际 Dockerfile 的 2025.6.1 声明、安装、链接 | 分别为 `f8665b42a01d52b39fdf4f923b35dd376c6172a1`、`76fb2ffb4afc9a37b1c0b8b03ef26e00b7b7ab11` |
| [Megatron timers.py 第 109–168 行](https://github.com/NVIDIA/Megatron-LM/blob/4b4acac9a1d28ea6829c8d4f566d75698a21249d/megatron/core/timers.py#L109-L168)、[training.py 第 2824–2833 行](https://github.com/NVIDIA/Megatron-LM/blob/4b4acac9a1d28ea6829c8d4f566d75698a21249d/megatron/training/training.py#L2824-L2833) | Timer 同步/barrier 与区间均摊吞吐公式 | 分别为 `78204ad243f068e0944d1f54f113780363003a78`、`57b8efe9390eca9ca8596ed5bb073ed62d9d014d` |
| [PyTorch 2.6 profiler](https://docs.pytorch.org/docs/2.6/profiler.html#torch.profiler._KinetoProfile.export_chrome_trace) | Kineto 直接导出仅末 cycle、shape/stack 采集开销 | 版本化文档页，无 Git blob 记录 |

两个 GitHub 网页锚点初次读取返回缓存读取失败，随后在相同冻结 ref 下经 GitHub 连接器取得相应原文件行；`parallel_state.py` 的固定 raw URL 也成功读取。未将读取失败解释为内容不存在，报告 GitHub 行号以原文件坐标为准。本轮没有重新取回 Nsight 2025.3 工具细节子页、CANN msprof、AMD 指定版本细节或全部 TorchNPU/MindSpeed profiler 源码；这些既有 unknown 与未实测边界继续保留，不补称本轮确认可达或兼容。

**新问题检查：未发现需另立发现编号的问题。** 重点检查了 dense/expert DP 混用、PP 数相等但组员不同、EP 放置被误称改变、专家编号/层身份混淆、采集 rank 重复计数以及单点观测被外推为全组证据。新填静态字段无算术冲突，也没有实测或优化收益声明；历史修订段不替代最新正文和第五轮实际交付。

## 五、最终验收与交付边界

- [T06-06 的五条验收要求](../../plans/full-coverage-backlog.yaml)在既定内容审阅范围内均通过：有效产出/重叠口径、工具证据与 unknown、各分支依赖判据、单因素/重复/恢复/双指标，以及专题交接与停止条件均未回归；组合身份到候选对照/具体采集选点/结果表的 C04 链路现已补齐。
- 正文保持 `draft / source_checked`、空 `environment_refs` 与未实测声明。审阅通过不等于编辑状态自动提升，也不构成 NVIDIA/AMD/Ascend 任意版本与拓扑的支持结论。
- 已执行 `make check`、`make build`，均通过：`107 content entries; 525 sources`；构建产物为 `build/catalog.json`、`build/catalog.md`。结构与本地链接检查不证明技术因果、远程可达性、环境兼容或硬件正确性。
- 本报告 10 处本地 Markdown 链接（9 个不同目标）另行检查，目标均存在。排除 Git 内部文件、生成产物与缓存后，纳入快照的 536 个既有文件经 SHA-256 回查均未修改或删除；同期另出现 `docs/research/batch-25-t06-07-codex-recheck-3.md`，并非本轮工具写入，已与本报告分离核对，保留且不读取、不修改、不计入本轮交付。因此不将并发新增文件归为本轮修改，也不以全工作区新增数量为一作失实断言。
- 交付仅新增本报告；未修改 `src/kb/`，未新增测试或执行 `make test`。本轮 Python 仅做静态算术，不是训练、通信或性能测试；未运行任何 profiling、checkpoint 恢复或硬件实验。
