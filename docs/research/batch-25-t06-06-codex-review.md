# Batch 25 T06-06 初审报告（gpt-6.1-sol / xhigh）

- 日期：2026-10-20（Asia/Shanghai）。
- 审阅对象：[训练性能分解、profiling 与优化验证](../../knowledge/06-training/performance-analysis.md)，连同[来源记录](batch-25-t06-06-sources.md)、[来源登记](../../sources/registry.yaml)、[06 章导航](../../knowledge/06-training/index.md)及相关指南。
- 审阅方式：当前本地 Codex CLI 会话独立初审，未委托其他审阅者；标题按任务指定的模型/档位记录。本轮未取得可独立核验的 CLI 启动模型元数据，不补写“已核验实际模型”的结论。
- 对象快照：正文 SHA-256 `de51c44e48e8bade96331336601866917fd8ce4a916bea2de1c69586f33c9c3e`；来源记录 SHA-256 `f9e084ebd9db83482db5fd979873cc7a8806bc30ba874496a326405ab6951a4d`。下列正文行号针对该快照。
- 写入范围：仅新增本报告，不修改正文、来源记录、registry、导航或其他批次文件。未执行 profiling、训练、优化复跑或硬件实验。

## 核对范围与取证限制

已重新阅读 `README.md`、`docs/authoring-guide.md`、`content-outline.md`、元数据 schema、T06-06 五条验收条款及 `06.2-G3` 的分工；检查正文全文、12 个 `source_refs` 的登记、六个指定新增来源、导航入口及 slow-rank、collectives、data-starvation、power-thermal 的链接关系。

本轮通过 GitHub 连接器取回指定 ref 的文件正文/相关函数，而非只读作者的来源摘要。`volcengine/verl` 的 API 返回迁移信息，仓库元数据确认为同一 repository ID `881221486`、现名 `verl-project/verl`；后续沿该仓库读取。固定 tag 的解析结果：verl `v0.9.1` → `1876b06d0a3e4e71e06230be10af14492ca8a75b`，Megatron `core_v0.19.2` → `4b4acac9a1d28ea6829c8d4f566d75698a21249d`。

| 独立重读的上游证据 | 本轮定位与边界 |
|---|---|
| [verl Nsight 指南](https://github.com/verl-project/verl/blob/1876b06d0a3e4e71e06230be10af14492ca8a75b/docs/perf/nsight_profiling.md) | Prerequisites、Global profiling control、Worker process profiling、输出位置和 Profiling Output；Git blob `f8665b42a01d52b39fdf4f923b35dd376c6172a1`。其 Dockerfile 版本锚另行读取返回 404，见 C05。 |
| [verl torch 指南](https://github.com/verl-project/verl/blob/1876b06d0a3e4e71e06230be10af14492ca8a75b/docs/perf/torch_profiling.md) | 两级控制、mini-batch schedule、训练/rollout 进程范围、缺失阶段与缺失 GPU 活动；Git blob `04d0903ba3b97f8bba285ac962b53b027d5489c9`。 |
| [verl 昇腾指南](https://github.com/verl-project/verl/blob/1876b06d0a3e4e71e06230be10af14492ca8a75b/docs/ascend_tutorial/zh/dev_guide/performance/ascend_profiling.rst) | 两级控制、level/contents、训练与推理分离及精细采集边界；Git blob `09fb587808af53f60b413b6794c320393c25d548`。 |
| [TorchNPU profiler.py](https://github.com/Ascend/pytorch/blob/bc51ab84cc6f35c77aab1c59886e0ea43681a317/torch_npu/profiler/profiler.py) | 本地 `_KinetoProfile` 定义、`export_chrome_trace`、`tensorboard_trace_handler`、`profile` 的 schedule/on_trace_ready/start/stop/step；Git blob `39f02b57d39539e78247c4b605f12236dbfb5c3c`。 |
| [Megatron training.py](https://github.com/NVIDIA/Megatron-LM/blob/4b4acac9a1d28ea6829c8d4f566d75698a21249d/megatron/training/training.py) / [timers.py](https://github.com/NVIDIA/Megatron-LM/blob/4b4acac9a1d28ea6829c8d4f566d75698a21249d/megatron/core/timers.py) | `training_log` 的计数、batch、区间计时、吞吐和日志分支；`Timer` 的同步、barrier、elapsed 语义。Git blob 分别为 `57b8efe9390eca9ca8596ed5bb073ed62d9d014d`、`78204ad243f068e0944d1f54f113780363003a78`。 |
| [MindSpeed-LLM training.py](https://github.com/Ascend/MindSpeed-LLM/blob/v2.2.0/mindspeed_llm/training/training.py#L214-L275) | `is_profile_enabled/get_profiler` 的 rank、Level、AiCMetrics、schedule 与 handler；只证明固定 ref 的集成。 |
| [PyTorch 2.6 profiler](https://docs.pytorch.org/docs/2.6/profiler.html) / [ROCprofiler-SDK docs-7.14.0 文档首页](https://rocm.docs.amd.com/projects/rocprofiler-sdk/en/docs-7.14.0/) | 前者核对 activities、schedule、导出、worker_name 和 shape/stack 开销；后者核对 SDK 1.3.2 的 tracing/异步活动/计数器基础设施。没有据此补写 ROCm CLI 或支持组合。 |

访问限制单独保留：Shell 对 codeload 域名解析失败；网页工具未成功取回 [Nsight 2025.3 目录页](https://docs.nvidia.com/nsight-systems/2025.3/)及其归档落点，User Guide 的重取也失败。因此，目录结构、更新时间和原取回 SHA-256 本轮仍只是**作者记录，未独立复核**；本轮失败不能改写成独立确认了作者所述的 HTTP 403。未改用其他版本 User Guide 代替 2025.3。CANN msprof 官方文档未取得，CLI、报告字段、配套与扰动细节继续 unknown。

## 重点主张核对结果

- **Megatron 公式的算术结构正确**：`training_log` 的分子是 `num_floating_point_operations(args, batch_size, ...)` 的返回值，分母为 `elapsed_time_per_iteration × 10**12 × args.world_size`；上游日志明确单位为 **TFLOP/s/GPU**，不是累计 TFLOP，也不是有效 token/s。`total_iterations = advanced + skipped`，nan 为另记的计数，不能再把三者相加。正文没有把 nan 明说成第三个互斥桶，故不据此报错；建议补全单位与区间分母解释。
- **verl NPU 级别没有读反**：上游 level0 为推荐默认；level1 在其上增加 AscendCL 与 AI Core 指标，level2 再增加 Runtime 与 AI CPU 指标。`module` 比 `stack` 的性能膨胀更低也是该指南的表述，不是本库量化实测。来源记录与 registry 的增量描述一致；正文仅简列级别，未反向转述。
- **TorchNPU 接口存在**：固定 commit 确有上述 API。`_KinetoProfile` 在该文件内自行定义，接口相似不能进一步证明它复用了 PyTorch Kineto 后端或跨版本兼容；正文“同构 API”只能按接口形态理解。
- **没有发现未经核对的完整工具命令**：正文未给出 `nsys`、`msprof`、`rocprof` 的可执行命令。`capture-range cudaProfilerApi`、角色 rank 控制与默认报告位置有 verl 固定版本指南支持，不应误判为偷偷转述不可访问的 Nsight User Guide；但工具能力和版本边界仍有 C05。
- **元数据与已有入口基本合规**：`draft / source_checked`、空环境档案及未运行声明没有冒充硬件验证；12 个 source_refs、5 个 related_ids 均可解析。06 章第 27、51 行已接入本页，正文现有本地链接目标均存在。

## 发现列表

### B25-T06-C01 — P2：优化验证缺少训练状态恢复和回归基线闭环

- **受影响位置**：正文第 52–60、91–96、106–118 行。
- **问题描述**：同配置重复三次窗口、前后测吞吐和 loss，尚不能保证优化对照有效。正文没有固定起始 checkpoint、optimizer/LR/动态精度状态、RNG、数据游标与输入身份，也没有成功优化后恢复原配置复跑 A 基线的步骤；“回退配置”仅在失败时出现。连续训练中的 A/B 窗口可能处于不同训练阶段或处理不同长度数据，loss 改善/吞吐变化可来自训练推进，而非优化。只回退配置也不能撤销已经发生的参数和优化器更新。
- **证据（上游定位）**：[Megatron training_log 的 batch 与迭代计数](https://github.com/NVIDIA/Megatron-LM/blob/4b4acac9a1d28ea6829c8d4f566d75698a21249d/megatron/training/training.py#L2658-L2672)说明计量依赖当前运行状态，并不提供状态等价保证；[并行策略与训练状态](../../knowledge/06-training/parallelism-and-state.md)第 56 行已明确权重相同不能推出 sampler/RNG/计数一致。T06-06 验收第 4 条要求“重复基线/恢复”，不是只有重复窗口。
- **建议关闭条件**：补齐可恢复的实验起点和数据身份；给出 A→B→A 恢复复测或等效的配对/交错设计及原基线未恢复时的否决条件。把无 profiler 的吞吐复测与 profiling 定位窗口分开；预先约定等有效 token/更新预算下的 loss/任务指标、非劣阈值和有限窗口结论边界。不能保证等价状态时明确只做探索，不宣布优化通过。

### B25-T06-C02 — P2：阶段占比与无事件现象被直接用作瓶颈判据

- **受影响位置**：正文第 74、80–85、93–94、117 行。
- **问题描述**：“占比最大阶段→对应分支”仍是耗时排名，不是关键路径判断；即使禁止重叠时间相加，也不能推出占用最长的可重叠工作限制了 step。另将“隐藏等待”写成“trace 中设备空闲但无通信”的等式，缺少采集完整性、主机阻塞/同步、跨进程阶段及生产者—消费者依赖证据。某个 worker 没有设备活动既可能是真等待，也可能是工作在别的进程或设备活动未被采到。现有 PP/EP/长度分支只列候选证据名，未给出如何支持/否定候选、如何追到最早阻塞边的判断规则。
- **证据（上游定位）**：[verl torch 指南 What one RL step looks like on disk](https://github.com/verl-project/verl/blob/1876b06d0a3e4e71e06230be10af14492ca8a75b/docs/perf/torch_profiling.md#L255-L268)明确 rollout 在独立进程、actor 可空闲，需结合 trainer 计时和对应进程 trace；[Traces with no GPU kernels](https://github.com/verl-project/verl/blob/1876b06d0a3e4e71e06230be10af14492ca8a75b/docs/perf/torch_profiling.md#L327-L335)给出 CUDA 活动丢失的采集失败反例。前者和后者都不能被“无事件=隐藏等待”排除。本库[慢 rank 指南](../../knowledge/06-training/slow-rank-triage.md)第 65–71 行也要求按 collective 序号和阶段证据逐层定位。
- **建议关闭条件**：将阶段排名降为候选；补一条按同一训练阶段、micro-batch、rank/group 和依赖事件回溯阻塞链的方法，标出计算/通信重叠后仍暴露的等待。为 PP bubble、EP 热点、长度偏斜、通信本体与主机同步分别列最低证据、反证/区分检查和 unknown 出口；没有完整活动或生产者证据时只记“未解释空档”，不得直接命名根因。

### B25-T06-C03 — P2：通用 warmup/active 采集步骤未说明 verl 的计步单位与丢阶段风险

- **受影响位置**：正文第 63、69、81、91、93 行；来源记录第 27 行。
- **问题描述**：正文同时引入普通训练 profiler 和 verl RL 样板，却统一要求选 schedule 窗口、“warmup 后 active”，未说明 profiler 的一次 `step()` 对应训练 iteration、mini-batch 还是 micro-batch。在本次指定 verl 版本中，`global_profiler.steps` 选择 RL step，而 torch schedule 仅推进 update mini-batch；continuous 模式中跳到较晚 active 窗口还会丢掉此前阶段。读者若据该通用步骤采完整 RL step，再按阶段占比分解，会把没有保存的阶段误判为无耗时。采集前 workload 热身与 profiler 自身 warmup 也未区分。
- **证据（上游定位）**：[verl Scheduling the update loop's mini-batches](https://github.com/verl-project/verl/blob/1876b06d0a3e4e71e06230be10af14492ca8a75b/docs/perf/torch_profiling.md#L152-L204)直接说明上述单位、continuous/discrete 差异及更早阶段被丢弃的条件；[PyTorch 2.6 profile.step/schedule/export_chrome_trace](https://docs.pytorch.org/docs/2.6/profiler.html)只定义调用者推进的 profiler step，且直接导出在 Kineto 下只保存最后一个 cycle，不能自动保证完整训练窗口。
- **建议关闭条件**：采集计划必须记录外层 step、内部 mini/micro-batch、schedule 推进点、active 覆盖范围及导出 cycle 身份；对 verl continuous/discrete 给出固定版本的限制说明，不把普通训练的热身策略机械套用。分析前增加“预期阶段/rank/窗口是否齐全”的门禁；无需补写任何未取得的 CLI。

### B25-T06-C04 — P2：组合并行只有触发词，尚无可执行的 TP×PP×EP 性能验证入口

- **受影响位置**：正文第 46、58–61、81、93–96 行；`plans/full-coverage-backlog.yaml` 第 2289–2297 行的 `06.2-G3` 分工。
- **问题描述**：第 46 行提到 TP×PP×EP×DP，口径表要求记录布局，但后续没有把 rank→TP/PP/EP 组、stage/layer/expert 归属接到采集选点和结果表。步骤 4 也没有 TP 组内计算/通信的独立观察入口。通用“改一个并行布局”不足以指导组合变更：需要明确哪些资源/全局 batch/数据条件固定、哪些派生维度联动、怎样区分 bubble、expert 路由与组内通信的代价变化。不能据此关闭由 T06-01 与本页共同承担的 G3。
- **证据（上游定位）**：[并行策略正文的组合身份样例](../../knowledge/06-training/parallelism-and-state.md#组合并行身份样例与冲突检查)第 84–123 行已有 dense 与 expert 两套身份、组成员、stage 与 shard 映射，但它明确是合成推导，不是性能验证；[执行清单](../../plans/full-coverage-backlog.yaml)的 `06.2-G3` 当前仍 open，要求“组合并行的映射/性能验证”。[Megatron training_log](https://github.com/NVIDIA/Megatron-LM/blob/4b4acac9a1d28ea6829c8d4f566d75698a21249d/megatron/training/training.py#L2621-L2656)列出的 compute、send/recv、梯度同步等计时只能作为取证锚，不能代替组合验证设计。
- **建议关闭条件**：增加具名“组合并行性能验证”小节并从身份样例互相导航；给出未执行的最小对照记录模板，含资源预算、配置及派生维度、组/stage/expert 对应的采集 rank、TP/PP/EP 分解、有效吞吐/质量与恢复复测。至少说明一组合法候选如何沿该入口比较；不要求虚构启动命令或实测结果，不把任意维度乘积当通用 world-size 公式。

### B25-T06-C05 — P2：Nsight 的目录级证据边界未贯穿能力和版本说明

- **受影响位置**：正文第 31、39、70、74 行；来源记录第 25–26、39 行；registry 的 `src.nvidia.nsight-systems-2025.3-archive`、`src.verl.nsight-profiling-v0.9.1`。
- **问题描述**：正文虽没有转述未知命令，但表中仍把“OS runtime”列为 Nsight Systems 2025.3 的已知范围。作者登记的目录页不能支持该版本的具体采集能力；本次读取的 verl Profiling Output 列 CUDA kernel、memory、CPU-GPU synchronization、NVTX，没有 OS-runtime 能力/版本证明。另登记称 nsys 版本以 `docker/Dockerfile.vllm.sglang.megatron` 固定为锚，本轮固定 ref 下该文件返回 404；不能把上游指南的旧路径提示当成已核实的版本配套，更不能据此连接到 2025.3。
- **证据（上游定位）**：[verl Nsight Prerequisites 与 Profiling Output](https://github.com/verl-project/verl/blob/1876b06d0a3e4e71e06230be10af14492ca8a75b/docs/perf/nsight_profiling.md)只建议参考该 Dockerfile 并列出使用面；[该固定 commit 的 docker 目录](https://github.com/verl-project/verl/tree/1876b06d0a3e4e71e06230be10af14492ca8a75b/docker)和该文件的独立读取未得到所称版本锚。本轮也未成功重取 [2025.3 归档目录页](https://docs.nvidia.com/nsight-systems/2025.3/)，不以最新版文档替证。
- **建议关闭条件**：把目录存在性、verl 使用样板与目标工具支持版本分开；OS runtime 降为未核对，或补取得并登记的固定版本一手证据。版本锚须核到真实存在的固定文件及字段；取不到则明确 nsys 实际版本与 verl×2025.3 配套 unknown。保留当前不写未知命令、msprof unknown 的纪律；本项不是要求绕过 403 或补造命令。

### B25-T06-C06 — P3：Megatron 应用计时的同步语义没有随指标一并交代

- **受影响位置**：正文第 63、80、93、108 行；来源记录第 31 行及 registry 的 Megatron training-log 条目。
- **问题描述**：目前只说明均摊公式和 timer 区间聚合，却没有说明这些计时的同步边界；后文还把扰动不可接受时“改用应用计时为主”作为退路。读取已有日志当然可以是只读，但启用更细 timer 或照搬其计时代码不等于无扰动：不能把人为同步形成的等待当作原始执行图，也不能把这类时长与异步 trace 直接等同。
- **证据（上游定位）**：[Timer.start/stop](https://github.com/NVIDIA/Megatron-LM/blob/4b4acac9a1d28ea6829c8d4f566d75698a21249d/megatron/core/timers.py#L109-L168)在两端调用 `torch.cuda.synchronize()`，可选 barrier 还要求组内所有调用者参与；[training_log 的 interval-time](https://github.com/NVIDIA/Megatron-LM/blob/4b4acac9a1d28ea6829c8d4f566d75698a21249d/megatron/training/training.py#L2824-L2833)明确使用 `elapsed(barrier=True, ...)`。这是本任务指定源码中已经取得的语义，不属于需要继续保持 unknown 的工具细节。
- **建议关闭条件**：补充已有日志读取与新增/启用计时的区别，记录 timing level、同步/barrier 范围和 on/off 对照；应用计时只能作为注明同步边界的替代证据。不要建议在只选部分 rank 的插桩中随意加入组 barrier。

### B25-T06-C07 — P3：通信专题仅有 metadata 关联和章节号，正文缺少可点击的交接链接

- **受影响位置**：正文第 27、82、94、101、109 行；相关指南的互链。
- **问题描述**：数据、供电、slow-rank 均有实际 Markdown 链接，而通信分支只写“03.7”“沿 03 章口径”或链接 slow-rank；`communication.collectives-and-rank-progress` 仅在 related_ids 中。本页没有直接连到 collectives 或 bandwidth-degradation。四篇指定关联页目前也均没有返回本页的链接；metadata 可解析不能替代正文中的操作交接。
- **证据（本地定位，无外部工具命题）**：[collectives-and-rank-progress](../../knowledge/03-communication/collectives-and-rank-progress.md)与[带宽退化指南](../../knowledge/03-communication/bandwidth-degradation-triage.md)均已存在；本页链接清单未包含它们。T06-06 验收第 5 条要求链接通信专题，写作指南第 6 节要求普通相对 Markdown 链接。
- **建议关闭条件**：在通信等待分支直接链接到语义/进度页和对应性能诊断页；在至少一个合适的上游入口补上“进一步性能分解”的返回链接，或明确其他入口负责反向导航。数据/供电现有链接保留，不要求为每页机械添加双向链接。

## 总体判断与验收逐条对照

**初审需修订，不声明 T06-06 通过。共 7 项发现：P1 0 项、P2 5 项、P3 2 项。** 这些是内容/方法与取证边界缺口，不是本轮实测出的训练故障；修订后需按同一发现 ID 定向复核。

| 验收条款 | 本轮判断 | 已具备与剩余缺口 |
|---|---|---|
| 1. 固定有效产出、模型/精度/并行/batch/拓扑/缓存，禁止重叠相加 | 基本满足 | 第 54–61 行列全主要口径；公式算术正确。实验状态/输入等价仍需 C01，计时边界需 C06，不能因此把阶段排名当关键路径。 |
| 2. 工具范围、扰动、版本与时间关联；未知细节不写命令 | 部分满足 | 四条平台证据线分开，未知 CLI 未写，msprof unknown 合理。C03 的采集粒度与完整性、C05 的 Nsight 能力/版本证据、C06 的同步扰动需补齐；不得将目录页视作支持矩阵。 |
| 3. PP/EP/长度/通信/同步/隐藏等待，区分受害与最早瓶颈 | 部分满足 | 候选分支与受害 rank 原则齐全，但 C02 的关键路径/区分判据、C03 的缺阶段门禁尚缺；目前不足以完成自述的最早瓶颈定位。 |
| 4. 单因素、重复基线/恢复、吞吐与质量共同判据 | 部分满足 | 有三次窗口、噪声带、双指标及利用率反例；C01 的等价状态、恢复复测和质量预算未闭环。 |
| 5. 准备、分支、终止/恢复、负例及数据/通信/供电链接 | 部分满足 | 有流程、终止与无收益反例，数据/供电链接可达；分支深度见 C02，恢复见 C01，通信交接见 C07。 |
| 06.2-G3：组合并行性能验证承接 | 未满足关闭条件，保持 open | 有组合名与配置口径，没有 C04 所需的具名性能验证入口；T06-01 的映射样例不构成此处性能验证的替代。 |

## 结构校验与交付边界

- 已执行 `make check`、`make build`：两者通过，输出均为 `107 content entries; 523 sources`，构建生成 catalog。
- 结构/本地链接检查不检查远程证据、技术因果、版本兼容或硬件正确性；通过它们不能关闭上述发现。
- 本报告不修改任务状态、主题缺口、正文 verification 或已有文件。Nsight 归档独立重取、msprof 细节及全部真实环境验证仍有明确边界，不能补称已完成。
