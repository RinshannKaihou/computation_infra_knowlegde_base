# Batch 25 T06-06 第二轮定向复核报告

- 日期：2026-10-20（Asia/Shanghai）。本轮为初审后的修订复核，不是训练或硬件验证。
- 对象：[修订正文](../../knowledge/06-training/performance-analysis.md)、[初审报告](batch-25-t06-06-codex-review.md)、[来源记录](batch-25-t06-06-sources.md)、[registry](../../sources/registry.yaml)，以及组合身份样例、通信回链和任务验收条款。
- 执行方式：当前本地 Codex CLI 会话独立复核，未委托其他审阅者。任务约定模型/档位为 `gpt-6.1-sol / xhigh`；本轮没有可独立核验的 CLI 启动模型元数据，不将约定写成已核验的实际模型。
- 正文快照 SHA-256：`618be90f870f4c7aa77a9a56fd6a94e7a300dd49fb18035ac7cc0718e62a8a69`；来源记录：`733b78d1b0333255eef271d4e0b7a27d46b1a330969598823015fdc20d645be1`。下列正文行号针对该快照。
- 写入边界：仅新增本报告；不修改正文、registry、来源记录、导航、任务状态或 `06.2-G3` 状态。未执行训练、profiling、checkpoint 恢复、优化复跑或硬件实验。

## 一、逐项判定表

**原 7 项发现：3 项 CLOSED（C05、C06、C07），4 项 OPEN（C01–C04，均为原 P2）。** OPEN 项认可本轮已完成的修订，但尚未满足初审中明确给出的全部实质关闭条件；不另编 R 编号重复计算这些遗留问题。

| 发现 ID | 原优先级 | 判定 | 本轮依据与理由 |
|---|---|---|---|
| B25-T06-C01 | P2 | **OPEN** | 正文第 92、95–96、125–126、131–134 行已补冻结起点、权重/optimizer/LR/scaler/RNG/数据身份、A→B→A 和原基线不能恢复时否决，训练推进混杂的主要缺口已修。但步骤 6 仍未规定用于最终收益判定的 A/B 吞吐必须关闭 profiler，未把定位窗口与收益测量明确分开；通用质量判据也尚未绑定等有效 token/更新的观察预算及有限窗口结论。组合模板第 102 行固定 token 数是进展，不能替代通用验证协议。见下文剩余关闭条件。 |
| B25-T06-C02 | P2 | **OPEN** | 第 93–94、112–113、133 行已正确将排名降为候选，要求依赖回溯，并将无事件降为“未解释空档”，不再直接命名根因。但步骤 4 仍主要列证据名称；“每分支给出最低证据、区分检查与 unknown 出口”是对执行者的要求，尚未实际给出各分支支持/否定候选的规则。PP 的 stage 等待、EP token 计数、长度与耗时相关，都仍可能是上游阻塞的结果。通信分支已有具体交接，不能替代其他分支的区分判据。 |
| B25-T06-C03 | P2 | **OPEN** | 第 91 行已准确区分 RL step 与 update mini-batch，区分 workload 热身和 profiler warmup，并增加完整性门禁；continuous 跳窗丢早期阶段的说明与上游一致。但计划未要求保存 `discrete` 模式、active 覆盖的 mini-batch 范围、导出 cycle/文件身份；也未说明 discrete 模式下其他阶段各自完整保存、update 仅保留所选窗口的边界。只核对阶段名存在，不能确认同名 update 阶段覆盖的是哪一段工作。PyTorch 直接导出只保留最后 cycle 的限制仍未承接。 |
| B25-T06-C04 | P2 | **OPEN** | 第 98–107 行已新增具名入口，包含固定资源、派生维度、按 TP/PP/EP 身份选 rank、分开记录 TP/PP/EP、双指标与恢复，模板本身是有效补充。但仍没有初审要求的“一组合法候选如何沿该入口比较”的最小填写样例，无法检查变更 PP 后 dense/expert DP、micro-batch 与 stage 归属如何联动并保持全局 batch。正文单向链接身份页，身份页尚无返回此性能验证入口的链接。故只能认可模板交付，尚不能据此关闭组合映射/性能验证的承接缺口。 |
| B25-T06-C05 | P2 | **CLOSED** | 第 70 行与 registry 对应 notes 已删除 OS runtime 的已核对能力表述，明确 2025.3 目录页与 2025.6.1 使用面分立；本轮独立取回固定 commit 的真实 Dockerfile，确认第 9 行 `NSIGHT_VERSION=2025.6.1`，第 52–60 行下载、安装该版本 deb 并建立 2025.6.1 路径的链接，SHA-256 与作者记录完全一致。旧文件独立读取为 404。关闭的是能力/版本取证越界，不代表已确认目标环境兼容或镜像构建成功。 |
| B25-T06-C06 | P3 | **CLOSED** | 第 63、117、123 行已同时说明 Timer start/stop 的 CUDA synchronize、可选 barrier、interval-time 的 `elapsed(barrier=True)`，区分读取已有日志与新增细计时，并要求 timing level/on-off 对照；明确不向部分 rank 添加组 barrier。与本轮重读的 Megatron 固定源码一致。现场仍需记录具体 barrier group（源码默认 None 为全局 communicator），这不再被正文隐去为零扰动计时。 |
| B25-T06-C07 | P3 | **CLOSED** | 第 82、94、114、124 行已直接链接 collectives/带宽退化指南；[带宽退化指南第 41 行](../../knowledge/03-communication/bandwidth-degradation-triage.md)已补返回本页的实际 Markdown 链接。数据与供电链接保留，06 章入口存在。符合初审“不要求每页机械双向链接、至少一处合适返回入口”的关闭条件。 |

### 仍为 OPEN 的具体关闭条件

#### C01：补齐收益测量与质量观察协议

保留本轮冻结起点和 A→B→A 设计，补一句可执行的分工：profiling 窗口只用于定位；最终 A、B、恢复 A 的吞吐在关闭 profiler、相同计时配置与相同热身/缓存策略下测量，细计时如保留须声明同步边界。每个条件按配对输入和等有效 token/更新预算观察质量，预先写明指标、非劣阈值、采样位置及窗口长度；短窗口只能证明该预算内未观察到劣化，不外推完整收敛。

步骤 1 的 profiler on/off 扰动检查不能替代这项最终复测：即使 A 可以恢复，B 也可能仅减少 profiler 的事件采集成本，而非提高关闭采集后的训练效率。[PyTorch 2.6 profiler 文档](https://docs.pytorch.org/docs/2.6/profiler.html)明确 shape/stack 采集会增加开销；这是保留独立收益测量的依据，不是本轮实测结果。

#### C02：把“需给判据”落成实际分支判据

无需新造阈值或工具命令，但至少给出各分支的“最低证据 → 支持/否定 → 下一步/unknown”规则。例如：

- PP：区分计划内 fill/drain 或调度空泡，与因数据、上游 stage 慢而形成的同形等待；沿生产者完成、发送/接收及消费者可执行边回溯，不能见 stage 空窗即归因 PP 布局。
- EP/长度：路由 token 数或长度分布要与对应 micro-batch、rank/expert 的服务时间和暴露等待相连，并用配对输入/路由计数或受控对照区分“工作量多”与“单位工作执行慢/通信迟到”；只有相关性时保留候选。
- CPU/设备同步：需要能连接主机阻塞/同步事件与设备后续可执行工作的依赖证据；只知道主机有准备工作仍不足以把设备空档归因给它。

这些是补齐本页方法的建议，并非声称上游已给出通用因果阈值。[verl 的跨进程阶段与无 GPU kernel 说明](https://github.com/verl-project/verl/blob/1876b06d0a3e4e71e06230be10af14492ca8a75b/docs/perf/torch_profiling.md#L250-L335)仍支持本轮保留“未解释空档”的正确修订。

#### C03：补齐窗口身份，而不仅是阶段存在性

在采集计划和结果记录中明确外层 RL/训练 step、内部 mini/micro-batch、schedule 推进位置、continuous/discrete 模式、active 范围及导出 cycle/文件对应关系。补上 discrete 的边界说明；多 cycle 时保存/核对每个所需窗口，不能把一次 `export_chrome_trace` 当作全部 cycle 的合集。

依据为固定 verl 指南的 [Scheduling the update loop's mini-batches](https://github.com/verl-project/verl/blob/1876b06d0a3e4e71e06230be10af14492ca8a75b/docs/perf/torch_profiling.md#L152-L204)及 [PyTorch 2.6 `export_chrome_trace`](https://docs.pytorch.org/docs/2.6/profiler.html#torch.profiler._KinetoProfile.export_chrome_trace)。完整性门禁应按这些身份核对预期工作量；不要求为了凑完整而全 rank 长时间采集。

#### C04：补一个不冒充启动验证的候选对照样例

可沿现有 64-rank 合成身份样例填写 A/B 记录，明确本次独立变更、必须重算的 dense/expert 组身份、stage/layer/expert 归属、全局 batch 约束、各条件采集选点与结果表；候选须先通过对应固定实现的约束检查，不能只列一串 TP×PP×EP 数字。示例仅需说明如何比较，不要求命令或实测数值；并从[身份样例所在页](../../knowledge/06-training/parallelism-and-state.md#组合并行身份样例与冲突检查)补到此入口的普通链接。现有样例是映射推导，不能替代性能对照设计。

### 独立重读的上游及边界

本轮重新读取文件内容/相关函数，而非只采信来源记录。verl `v0.9.1` 本轮经 tag API 再次解析为 `1876b06d0a3e4e71e06230be10af14492ca8a75b`；Megatron 沿初审固定的 `4b4acac9a1d28ea6829c8d4f566d75698a21249d` 读取。以下 blob SHA 是 GitHub 返回的文件身份，不与 SHA-256 混称。

| 上游 | 本轮实际核对位置与结论 |
|---|---|
| [verl Nsight 指南](https://github.com/verl-project/verl/blob/1876b06d0a3e4e71e06230be10af14492ca8a75b/docs/perf/nsight_profiling.md) | 重读 Prerequisites、global/worker 控制、落盘与 Profiling Output。确有旧 Dockerfile 引用；能力列表为 CUDA kernel、memory、CPU-GPU synchronization、NVTX。blob `f8665b42a01d52b39fdf4f923b35dd376c6172a1`。 |
| [Dockerfile.stable.sglang](https://github.com/verl-project/verl/blob/1876b06d0a3e4e71e06230be10af14492ca8a75b/docker/Dockerfile.stable.sglang#L9) | 取回全文 5255 字节。第 9 行为 ARG；[第 52–60 行](https://github.com/verl-project/verl/blob/1876b06d0a3e4e71e06230be10af14492ca8a75b/docker/Dockerfile.stable.sglang#L52)在 RUN 中另设版本为 `2025.6.1_2025.6.1.190-1_<arch>`、下载/apt 安装并链接到 2025.6.1，不能只凭 ARG 推断安装。对取回文本复算 Git blob SHA-1 为 `76fb2ffb4afc9a37b1c0b8b03ef26e00b7b7ab11`，与 API 一致；SHA-256 为 `99386acc562092ca81b167f681fd563b716c62fe87eff15b4348ac21d9dc2dd7`，与作者记录一致。 |
| [旧 Dockerfile 路径](https://github.com/verl-project/verl/blob/1876b06d0a3e4e71e06230be10af14492ca8a75b/docker/Dockerfile.vllm.sglang.megatron) | 固定 commit 独立读取返回 GitHub 404；同时读取 docker 目录可见 stable.sglang。旧路径不能继续充当版本证据。 |
| [verl torch 指南](https://github.com/verl-project/verl/blob/1876b06d0a3e4e71e06230be10af14492ca8a75b/docs/perf/torch_profiling.md) | 重读两级控制、schedule 的 mini-batch 单位与 active 启用条件、continuous/discrete 差异、跨进程完整 step、缺失阶段及无 GPU kernel 反例。blob `04d0903ba3b97f8bba285ac962b53b027d5489c9`。 |
| [verl 昇腾指南](https://github.com/verl-project/verl/blob/1876b06d0a3e4e71e06230be10af14492ca8a75b/docs/ascend_tutorial/zh/dev_guide/performance/ascend_profiling.rst) | 重读两级配置、level_none/0/1/2、contents、训练/推理分离和 rollout 窗口。level0 为指南推荐默认，level1 增加 AscendCL/AI Core，level2 再增加 Runtime/AI CPU；module 相对 stack 开销更低是指南表述，不是本库测量。blob `09fb587808af53f60b413b6794c320393c25d548`。 |
| [TorchNPU profiler.py](https://github.com/Ascend/pytorch/blob/bc51ab84cc6f35c77aab1c59886e0ea43681a317/torch_npu/profiler/profiler.py) | 重读本地定义的 `_KinetoProfile`、export、handler、`profile` 构造和 start/stop/step。接口及 schedule 推进存在；不据接口命名认定底层复用 PyTorch Kineto 或跨版本兼容。blob `39f02b57d39539e78247c4b605f12236dbfb5c3c`。 |
| [Megatron training.py](https://github.com/NVIDIA/Megatron-LM/blob/4b4acac9a1d28ea6829c8d4f566d75698a21249d/megatron/training/training.py#L2621) / [timers.py](https://github.com/NVIDIA/Megatron-LM/blob/4b4acac9a1d28ea6829c8d4f566d75698a21249d/megatron/core/timers.py#L109) | 重读 timing level 对应区间、batch/advanced+skipped 分母，以及 interval-time/TFLOP/s/GPU；Timer 两端同步、barrier group、elapsed 停止/恢复语义与正文修订一致。blob 分别为 `57b8efe9390eca9ca8596ed5bb073ed62d9d014d`、`78204ad243f068e0944d1f54f113780363003a78`。公式是每 GPU 的应用均摊速率，不是有效 token/s。 |
| [MindSpeed-LLM training.py](https://github.com/Ascend/MindSpeed-LLM/blob/v2.2.0/mindspeed_llm/training/training.py#L214) | 重读 rank 选择、ProfilerLevel/ExportType/AiCMetrics、checkpoint iteration 关联的 schedule 和 handler。blob `114200e463737cbdebba0b222b1d1c2d5df67d8b`；只证明该 ref 的集成，不证明与本页其他来源组成可运行栈。 |
| [PyTorch 2.6 profiler](https://docs.pytorch.org/docs/2.6/profiler.html) | 本轮网页取回成功，核对 schedule/step、on_trace_ready、直接导出的最后 cycle 限制、worker_name 与 shape/stack 额外开销。 |

Dockerfile 只证明该固定文件的安装配方，**不证明镜像实际构建、当前作业工具版本、verl v0.9.1 的通用支持矩阵或与 Megatron core_v0.19.2 的兼容组合**；文件自身还列有 `MCORE_VERSION=core_v0.18.0`、`VERL_VERSION=v0.7.1`，不可把本页各独立证据线拼成一套验证环境。

本轮未成功重取 Nsight 2025.3 的 docs/归档目录，也未成功重取 ROCprofiler-SDK docs-7.14.0 指定首页；这些重取失败不等于独立确认作者记录的 HTTP 403。Nsight 目录内容/作者原取回摘要和 AMD 页面细节本轮不追加独立确认，沿用既有边界，不拿其他版本页面替证。CANN msprof 细节继续 unknown。上述限制不妨碍核实 Dockerfile 和关闭 C05，但不能写成工具支持已验证。

## 二、新发现

### B25-T06-R01 — P3：新增状态恢复/复跑动作仍被标为“只读”

- **状态：OPEN。受影响位置：正文第 92、96 行的“运行影响”列。**
- **问题**：步骤 2 现在要求恢复 checkpoint 并重新执行训练窗口，却仍标“只读基线”；步骤 6 新增恢复原配置复跑 A，却标“只读（A 复测）”。读取已有日志才是只读；实际恢复会替换进程内训练状态，训练窗口会推进参数/optimizer/RNG/数据游标，并可能写日志或 checkpoint、占用设备。括号注明恢复有成本，没有消除“只读”对动作性质的误标。
- **依据**：[写作指南第 6 节](../authoring-guide.md#6-链接正文和操作边界)要求说明主动测试、配置修改与生命周期操作的目标范围和运行影响；正文第 125 行也已正确承认回退配置不能撤销参数/optimizer 更新。本项是本轮扩展恢复/复跑动作后与影响标签形成的冲突，不重复计算 C01 的实验等价性问题。
- **关闭条件**：把已有证据读取与实验复跑分列；后者明确为会恢复/推进训练状态的主动实验，在已有授权的隔离实验副本与独立输出目录执行，保护冻结 checkpoint，不覆盖生产作业/恢复点。文档本身不授予执行权。不要求本轮真的恢复或训练。

除此之外，本轮未发现需要新编号的修订回归。C01–C04 的未完成项继续沿原 ID 跟踪；C05–C07 不因其他缺口重复打开。

## 三、总体判定

**本轮结论：需继续修订，不声明 T06-06 整体通过。** 原发现剩余 4 项 P2 OPEN；新增 1 项 P3 OPEN。确认关闭原 1 项 P2、2 项 P3。不存在本轮实测出的硬件或训练故障结论。

| 验收条款 | 整体判定 | 依据及未完成项 |
|---|---|---|
| 1. 固定有效产出、模型/精度/并行/global batch/拓扑/缓存；重叠时间不可相加 | **条款自身满足** | 第 54–63 行保留完整口径与重叠约定，第 92 行补状态身份。收益试验的独立测量/预算仍按第 4 条及 C01 跟踪；不把条款 1 满足扩展为所有试验已可比。 |
| 2. 工具范围、扰动、版本与时间关联；未知细节不写命令 | **部分满足** | C05、C06 已关闭，2025.3/2025.6.1 版本线与同步扰动交代正确；msprof、rocprof 等边界保留，未补造命令。C03 的模式/窗口/cycle 身份尚未落地，仍影响采集证据解释。 |
| 3. PP/EP/长度/通信/CPU-设备同步/隐藏等待；区分受害与最早瓶颈 | **部分满足** | 候选与关键路径、未解释空档、阻塞链回溯和通信交接已改善；各分支如何支持/否定候选仍见 C02，完整性身份仍见 C03。 |
| 4. 单因素、重复基线/恢复、吞吐与质量共同判据；不以高利用率代替效率 | **部分满足** | 冻结起点、≥3 次窗口、A→B→A、噪声带、预注册非劣阈值、利用率反例均已有；关闭 profiler 的收益复测、统一质量预算和有限窗口边界仍见 C01。主动复跑的影响标签还需 R01。 |
| 5. 准备、分支、终止/恢复、无效反例，以及数据/通信/供电链接 | **部分满足** | C07 链接闭环已满足，停止/回退和反例内容有效；方法深度仍受 C02/C03 影响，恢复影响标签受 R01 影响。不能因导航补齐而整体放行。 |
| 06.2-G3 承接 | **保持 OPEN，不建议本轮关闭** | 具名模板已经建立，但合法候选的完整对照记录与身份页返回入口未补；见 C04。该缺口是内容方法验收，不以虚构硬件结果为关闭条件。 |

### 结构校验与交付边界

- 本轮 `make check`、`make build` 均通过，输出为 `107 content entries; 525 sources`；生成 `build/catalog.json` 和 `build/catalog.md`。正文与来源记录的 SHA-256 在校验后复算未变。本轮源文件写入仅为此新增报告，保留工作区原有其他变更。
- 校验通过只能证明结构与本地引用，不证明上述方法缺口已关闭、远程内容可达或硬件正确性；本轮无需增加内容测试，也未修改 `src/kb/`。
- 正文仍为 `draft / source_checked`，`environment_refs` 为空；本报告不改变编辑状态、实验验证状态或任务/主题验收状态。后续应先修订 C01–C04 和 R01，再按原 ID 定向复核。
