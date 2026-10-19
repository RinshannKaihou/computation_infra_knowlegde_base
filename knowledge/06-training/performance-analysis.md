---
id: training.performance-analysis
title: 训练性能分解、profiling 与优化验证
type: procedure
domain: training
status: draft
platforms: [nvidia, amd, ascend]
source_refs:
- src.pytorch.profiler-2.6
- src.nvidia.nsight-systems-2025.3-archive
- src.verl.nsight-profiling-v0.9.1
- src.verl.torch-profiling-v0.9.1
- src.verl.ascend-profiling-v0.9.1
- src.ascend.torchnpu-profiler-source-7.2.0
- src.ascend.mindspeed-llm-training-interface-v2.2.0
- src.amd.rocprofiler-sdk-1.3.2-docs-7.14.0
- src.nvidia.megatron-training-log-core-v0.19.2
- src.nvidia.megatron-training-loop-core-v0.19.2
- src.pytorch.processgroupnccl-env-2.8
- src.nvidia.nccl-user-guide-2.27.5
updated_at: "2026-10-20"
summary: 在慢 rank 诊断之上建立训练性能的系统分解方法：固定有效产出与配置口径，按阶段与 rank 采集应用级与系统级证据，区分 PP bubble、EP 热点、长度偏斜、通信等待与主机同步，先找最早瓶颈再单因素优化，并以重复基线与吞吐、质量双判据验证收益。
related_ids:
- training.slow-rank-triage
- training.parallelism-and-state
- training.framework-execution
- communication.collectives-and-rank-progress
- data-storage.data-starvation-triage
applicability:
  environment_refs: []
  notes: "工具证据线分立：PyTorch 2.6 profiler 文档、Nsight Systems 2025.3 归档（子页未取得）、TorchNPU 7.2.0 profiler 源码、ROCprofiler-SDK 1.3.2（docs-7.14.0 线）、Megatron core_v0.19.2 与 MindSpeed-LLM v2.2.0 应用层口径、verl v0.9.1 采集指南；目标环境未建立档案。"
verification:
  status: source_checked
  evidence_refs:
  - src.pytorch.profiler-2.6
  - src.ascend.torchnpu-profiler-source-7.2.0
  - src.nvidia.megatron-training-log-core-v0.19.2
  - src.verl.ascend-profiling-v0.9.1
  notes: "已核对固定版本文档/源码（锚点见 docs/research/batch-25-t06-06-sources.md）；Nsight 工具细节子页与 CANN msprof 文档未取得（正文不转述其命令），全部工具未运行。"
---

# 训练性能分解、profiling 与优化验证

## 目标与触发条件

本流程回答：**一次训练的时间花在哪里**（阶段与 rank 分解）、**瓶颈最早出现在哪一层**（计算/通信/数据/主机/设备）、**一次优化是否真的有效**（吞吐与质量双判据）。触发条件：吞吐低于预期或随版本/配置变化回退、扩容后线性度差、慢 rank 已定位但需进一步分层（承接[慢 rank 诊断指南](slow-rank-triage.md)）、组合并行（TP×PP×EP×DP）调整前后需要证据。

本页不提供"调优参数清单"：优化项取决于瓶颈定位结果；未取得一手资料的工具细节不写命令（见工具对照表的取证边界）。

## 适用范围与前置条件

进入分解前必须固定的口径——不固定则任何数字不可比较：

| 口径项 | 要求 |
|---|---|
| 有效产出 | 有效 token/样本/step 的定义写明（pad、pack、被过滤样本、跳过 step 的处理）；吞吐一律换算到有效产出 |
| 模型与精度 | 架构、参数量、dtype/AMP 配置、loss scale 形态 |
| 并行与全局 batch | TP/PP/EP/DP/CP 布局、micro/global batch、序列长度分布 |
| 拓扑 | 节点数、卡数、互联、rank 映射（哪张卡在哪个节点哪条链路） |
| 缓存与状态 | 编译/图缓存状态、数据缓存、冷热启动区别声明 |
| 时间分解约定 | **重叠执行的时间区间不可直接相加**：内核、通信、复制在同一时间窗内并行时，按"墙钟区间＋各自占用"记录，不做算术和 |

应用层口径示例：Megatron core_v0.19.2 的 `training_log` 以 `elapsed_time_per_iteration`（区间耗时/迭代数）为基，TFLOPs＝`num_floating_point_operations/(elapsed_time_per_iteration×10^12×world_size)`，且 `log_throughput` 开关控制记录、advanced/skipped/nan iterations 分开计数（[training.py](https://github.com/NVIDIA/Megatron-LM/blob/core_v0.19.2/megatron/training/training.py)）——这是**应用自定义的均摊口径**，与硬件计数器或通信库口径不可直接相加比较。**同步语义**：Megatron Timer 的 start/stop 两端调用 `torch.cuda.synchronize()`，`barrier=True` 的区间计时还要求组内所有调用者参与（[timers.py](https://github.com/NVIDIA/Megatron-LM/blob/core_v0.19.2/megatron/core/timers.py)），`training_log` 的 interval-time 即用 `elapsed(barrier=True)`——读取已有日志是只读证据，但**新启用**更细计时会引入同步等待与扰动，其时长不能与异步 trace 直接等同，须记录 timing level 与 on/off 对照。verl 的 RL 训练另按角色（Actor/Ref/Rollout/Critic/Reward）分别计时，其口径见[RL rollout 协同](rl-rollout-consistency.md)。

## 工具对照与取证边界

| 工具 | 层次 | 已核对的证据 | 边界（未取得/未核对） |
|---|---|---|---|
| torch.profiler（2.6） | 应用级（CPU 算子/CUDA 活动、schedule、chrome trace） | [文档](https://docs.pytorch.org/docs/2.6/profiler.html)：activities/schedule(wait/warmup/active/repeat)/export_chrome_trace/key_averages | 页面无 NPU 说明；无多进程聚合视图（多 rank 需逐 rank 导出对齐）；采样扰动需自行对照评估 |
| NVIDIA Nsight Systems | 系统级（CUDA trace/NVTX） | 仅[2025.3 归档目录页](https://docs.nvidia.com/nsight-systems/2025.3/)（Release Notes/Installation/User Guide 结构存在性）；verl 使用面样板（[nsight 指南](https://github.com/volcengine/verl/blob/v0.9.1/docs/perf/nsight_profiling.md)：capture-range cudaProfilerApi、角色级 rank 控制、nsys-rep 落盘路径；其 Profiling Output 列 CUDA kernel/memory/CPU-GPU synchronization/NVTX）；verl 配套镜像实际安装 nsight-systems **2025.6.1**（[docker/Dockerfile.stable.sglang](https://github.com/volcengine/verl/blob/v0.9.1/docker/Dockerfile.stable.sglang)） | **2025.3 User Guide 子页取证 403，该版本工具能力细节未取得；"OS runtime trace"等能力未核对（不列已核对范围）；2025.6.1 与 2025.3 分属不同版本线不互推；本页不转述 nsys 命令**（指南自述参考的 `Dockerfile.vllm.sglang.megatron` 在 v0.9.1 不存在，为文档陈旧引用） |
| TorchNPU profiler（7.2.0） | 应用级（NPU 算子/活动） | [profiler.py 源码](https://raw.githubusercontent.com/Ascend/pytorch/bc51ab84cc6f35c77aab1c59886e0ea43681a317/torch_npu/profiler/profiler.py)：`profile(_KinetoProfile)`＋schedule＋tensorboard_trace_handler＋export_chrome_trace（与 torch.profiler 同构 API）；MindSpeed-LLM v2.2.0 集成（ProfilerLevel Level0/1/2、AiCMetrics、schedule）；verl 昇腾指南（level0 推荐/level1/level2、contents npu/cpu/memory/shapes/module/stack，module 记栈开销低于 stack） | CANN **msprof 系统工具官方文档未取得**（站点需 JS 渲染），msprof CLI/报告字段保持 unknown，不写命令 |
| ROCprofiler-SDK（1.3.2，docs-7.14.0 线） | 系统级（HIP API 回调＋内核计数器） | 既有[登记条目](https://rocm.docs.amd.com/projects/rocprofiler-sdk/en/docs-7.14.0/index.html)：运行时无关 tracing＋计数器基础设施 | 新旧 rocprof 工具边界未逐条核对（既有缺口保留）；与 ROCm 10.1.0 组件表 1.4.1 属不同版本线 |

跨工具时间对齐：应用级 trace（torch/TorchNPU profiler）与系统级工具（Nsight/ROCprofiler）各有时间源；对齐用共享事件（如同一 NVTX 区间或 step 边界），不用绝对时钟拼接。工具版本与运行环境一起记录；未取得的工具能力不在正文假设。

## 需要的证据

| 证据 | 采集范围或定位 | 用途 | 缺失时如何处理 |
|---|---|---|---|
| 应用层 step 计时 | 每 step/区间的墙钟、跳过 step 计数（应用日志，如 Megatron training_log） | 吞吐基线与异常 step 识别 | 无应用计时则先补（不依赖 profiler 跑全程） |
| 分 rank trace | 按指南选定的 rank 子集（慢 rank＋正常对照），应用级 profiler 的 schedule 窗口 | 阶段占比、等待区间 | 全 rank 采集代价高时至少一慢一快对照 |
| 通信证据 | NCCL/HCCL 观测（沿用[慢 rank 指南](slow-rank-triage.md)；语义与进度见[集合通信与 rank 进度](../03-communication/collectives-and-rank-progress.md)） | 区分通信本体慢与等待别人（后续沿[通信带宽退化指南](../03-communication/bandwidth-degradation-triage.md)） | 沿 03.7 取证路径 |
| 数据供给证据 | 数据阶段计时、队列/饥饿指标（[数据饥饿指南](../04-data-storage/data-starvation-triage.md)） | 数据等待分支 | 沿 04.5 路径 |
| 环境/供电 | 降频与温度证据（[供电散热证据](../01-hardware/power-thermal-evidence.md)） | 排除设备侧降频 | 沿 01.1 路径 |
| 系统级采样 | 按需：Nsight/ROCprofiler 窗口（工具细节未取得处只列占位） | 内核/拷贝/流并行的下层确认 | 不可得时以应用级证据推进，记录工具缺口 |

## 步骤与判断分支

| 步骤 | 检查或动作 | 运行影响 | 预期证据与解释 | 下一步 |
|---|---|---|---|---|
| 1 | 采集准备：固定上表口径，选定 rank 子集与采集窗口。**记录窗口身份**：外层训练/RL step 号、内部 mini/micro-batch 位置、schedule 推进点、continuous/discrete 模式、active 覆盖范围、导出 cycle 与文件的对应关系——profiler 的一次 `step()` 对应哪个单位必须声明；verl 样板中 `global_profiler.steps` 按 RL step 选择，而 torch profiler 的 schedule 在 update 的 mini-batch 上推进（continuous 模式跳到较晚 active 窗口会丢弃此前阶段；discrete 模式下其他阶段各自完整保存、update 只保留所选窗口；PyTorch 直接 `export_chrome_trace` 只保留最后一个 cycle，多窗口须逐 cycle 保存核对，[torch_profiling.md](https://github.com/volcengine/verl/blob/v0.9.1/docs/perf/torch_profiling.md)）；workload 热身与 profiler 自身 warmup 分开记录；分析前加门禁：**按窗口身份核对预期阶段/rank/工作量是否齐全**（缺失则该窗口不可用于阶段分解，如 CUDA 活动未被采到的"无 kernel trace"形态） | 采样本身有扰动，窗口宜短、位置宜固定；扰动量以"开采集 vs 不开"的 step 时间差记录 | 得到可比较的采集计划与完整性检查表 | 口径不全或窗口不完整→先补齐，不进入分解 |
| 2 | 重复基线：**从同一冻结起点（checkpoint：权重/optimizer/LR/scaler 状态/RNG/数据游标与输入身份）**恢复，同配置重复 ≥3 次窗口 | **主动实验**（恢复会重建训练状态、窗口推进参数/优化器/RNG/数据游标并可能写日志/checkpoint；在授权的隔离实验副本与独立输出目录执行，保护冻结 checkpoint 不被覆盖；读取已有日志才是只读） | 得到噪声带；后续优化收益必须超出噪声带才可主张 | 方差过大→先查间歇性因素（供电/争用/降频） |
| 3 | 阶段分解：forward/backward/optimizer/通信/数据在 step 内的区间（应用区间名＋trace） | 只读 | 阶段耗时排名只是**候选清单**，不是关键路径判定——可重叠工作的最长占用不等于限制 step 的等待 | 候选→步骤 4 逐分支取证 |
| 4 | 分支定位：按同一训练阶段、同一 micro-batch、rank/group 与依赖事件**回溯阻塞链**（谁在等谁、从哪条边开始），确认计算/通信重叠后仍暴露的等待。各分支的最低证据与区分规则：**PP bubble**——stage 空窗先区分计划内 fill/drain 或调度空泡与因数据/上游 stage 慢形成的同形等待，沿"生产者完成→发送/接收→消费者可执行"边回溯，见 stage 空窗不直接归因 PP 布局；**EP 热点**——专家 token 路由计数要与其服务时间和暴露等待相连，用配对输入/路由计数或受控对照区分"工作量多"与"单位工作慢/通信迟到"，只有相关性时保留候选；**长度偏斜**——长度分布与 rank 耗时差的对应需配对到同一 micro-batch，同样区分工作量与单位效率；**通信等待**——在集合点等待≠链路慢，沿[集合通信与 rank 进度](../03-communication/collectives-and-rank-progress.md)与[通信带宽退化指南](../03-communication/bandwidth-degradation-triage.md)区分；**CPU/设备同步**——需要能连接主机阻塞/同步事件与设备后续可执行工作的依赖证据，只知主机有准备工作不足以归因设备空档。无法闭合依赖链的空窗记**未解释空档**（可能是工作在其他进程、采集不完整或真实等待），不直接命名根因 | 只读＋可能的对照复跑 | 每分支有"最低证据→支持/否定→下一步/unknown"的可执行规则；**区分"受害慢 rank"（等别人的 rank）与"最早瓶颈"（让所有人等的源头）**——修受害 rank 无效 | 定位到最早阻塞边→步骤 5 |
| 5 | 单因素优化：一次只改一个变量（micro-batch 数/并行布局/通信算法/数据组织/算子路径） | 变更影响声明＋可回退配置 | 每次优化从冻结起点恢复，对照前后同窗口测量 | 有收益→步骤 6；无收益→记录反例，回到步骤 4 |
| 6 | 复测与判读：**A→B→A 恢复复测**（或等效交错/配对设计）——成功后恢复原配置复跑基线 A，确认 A 可复现且 B 的收益不依赖训练推进的漂移；测量吞吐**和**质量指标（loss/任务指标），对照噪声带与预注册非劣阈值 | **主动实验**（恢复＋复跑均推进训练状态；隔离副本执行、独立输出目录，不影响生产作业/恢复点） | 收益=吞吐提升超出噪声带、质量不劣化、A 基线可恢复；**无法保证等价状态（起点不可恢复/无配对设计）时只作探索结论，不宣布优化通过** | 通过→记录收尾；质量劣化或 A 不可恢复→优化作废或重新设计 |

**收益测量与质量观察协议（步骤 6 的执行细则）**：profiling 窗口只用于**定位**；最终 A、B、恢复 A 的吞吐在**关闭 profiler**、相同计时配置与相同热身/缓存策略下测量（细计时如须保留，声明其 synchronize/barrier 边界）——profiler 的 on/off 扰动检查不能替代这项独立复测（B 的差异可能只是事件采集成本差）。质量观察按**配对输入与等有效 token/更新预算**设计：预先写明指标、非劣阈值、采样位置与窗口长度；短窗口只能证明"该预算内未观察到劣化"，不外推完整收敛。

### 组合并行性能验证入口（承接 06.2-G3）

组合并行（TP×PP×EP×DP 等）的性能验证不是"改一个布局参数再测一次"：布局改变会联动派生维度。沿[并行策略与训练状态](parallelism-and-state.md)的组合身份样例（dense/expert 两套身份、组成员、stage 与 shard 映射——该页是合成推导，本页给它接性能验证），最小对照记录模板：

1. **固定项**：总资源预算（卡数/拓扑）、全局 batch、有效 token 数、数据身份与长度分布、精度配置。
2. **变更项与派生维度**：本次单变量（如 PP stage 数）＋随之联动的 micro-batch 数、TP 组规模、expert 分组——逐项记录，不只写变更项。
3. **采集选点**：按身份样例确定 rank→TP/PP/EP 组、stage/layer/expert 归属，选覆盖各组/各 stage 的 rank 子集（不只选慢的）。
4. **分解**：TP 组内计算/通信分开观察、PP bubble（stage 间等待边）、EP 路由分布（token/expert 计数）分别记录，不合并为"通信时间"。
5. **判据**：有效吞吐（有效 token 口径）＋质量不劣化＋A→B→A 恢复复测（同上）。
6. **候选对照最小样例（静态推导已填写，运行字段全部未执行；非启动验证）**：沿[身份样例页](parallelism-and-state.md)的同一合成语境（64 rank、32 层、num_experts=128、EP=4、合成 32k 序列）构造 A/B，仅变更 PP：

| 项 | A（基线） | B（仅改 PP） | 联动重算说明 |
|---|---|---|---|
| 布局 | tp=2, pp=2, cp=2（身份样例原配置） | tp=2, **pp=4**, cp=2 | 唯一独立变更 |
| dense DP | 64/(2×2×2)=**8** | 64/(2×4×2)=**4** | PP 翻倍必然减半 |
| stage/layer 归属 | 2 stage，各 16 层 | 4 stage，各 8 层 | stage 数变化，等待边数量随之变 |
| micro-batch 换算（保持全局 batch 32、micro_batch_size=2） | num_micro = 32/(8×2) = **2** | num_micro = 32/(4×2) = **4** | B 每 rank 串行 micro-batch 翻倍以维持全局 batch 与有效 token 不变 |
| 专家侧（PP 必须与 dense PP 一致） | ETP=2, EP=4, PP=2 → expert_dp = 64/(2×4×2) = **4** | ETP=2, EP=4, PP=4 → expert_dp = 64/(2×4×4) = **2** | 两套 grid 的 PP 一致约束使 expert_dp 随 PP 联动；EP 组的节点内放置随步长变化重算 |
| 约束检查（代入硬断言） | 64%(2×2×2)=0 ✓；128%4=0 ✓；32k%4=0 ✓ | 64%(2×4×2)=0 ✓；其余同 A ✓ | B 通过静态检查，可进入测量；未过即作废 |
| 代表 rank 37 的 B 侧身份（dense 步长 tp1/cp2/dp4/pp16） | — | 坐标 (pp=2, dp=1, cp=0, tp=1)；dense DP 组 {33, 37, 41, 45}、PP 组 {5, 21, 37, 53}（4 stage 链）、stage=2 → 第 16–23 层 | 与 A（身份样例）同 rank 的身份联动实例 |
| 代表 rank 37 的 B 侧专家身份（步长 etp1/ep2/edp8/pp16） | — | 坐标 (pp=2, edp=0, ep=2, etp=1)；EP 组 {33, 35, 37, 39}（仍在节点 4，与 A 相同）、expert DP 组 {37, 45}（较 A 的 4 副本缩为 2）、持有 expert 64–95 不变 | expert_dp 联动的具体成员变化 |
| 采集选点（具体 rank） | rank 37＋TP/PP/EP 组员（身份样例原选点）；2 个 stage 各 ≥1 | **PP 链 {5, 21, 37, 53}（覆盖全部 4 个 stage）＋dense DP 组 {33, 37, 41, 45} 取 37＋EP 组 {33, 35, 37, 39} 取 37** | B 的 stage 数变化使选点集合不同；上两行给出成员 |

A/B/恢复 A 结果表（结构交付，运行字段未执行）：

| 条件 | 有效吞吐 | 质量指标 | TP 组内计算/通信 | PP 等待边 | EP 路由分布 | A→B→A 恢复复测 |
|---|---|---|---|---|---|---|
| A | 未执行 | 未执行 | 未执行 | 未执行 | 未执行 | 未执行 |
| B | 未执行 | 未执行 | 未执行 | 未执行 | 未执行 | 未执行 |
| 恢复 A | 未执行 | 未执行 | — | — | — | 未执行（本行即该字段） |

静态字段（组身份/归属/换算/选点）为推导值，吞吐、质量、等待边与恢复复测全部标未执行/unknown；不虚构启动命令与实测数值，也不把任一维度的乘积当通用 world-size 公式。
7. 该模板未执行；不虚构启动命令与实测结果，也不把任一维度的乘积当通用 world-size 公式。

**反例与易错点**：

- **高设备利用率 ≠ 有效训练效率**：利用率只说明设备在跑，不说明算的是有效 token（padding、重算、空转内核都会抬高利用率）；有效产出口径才是分母。
- **阶段占比排名 ≠ 关键路径**：最长占用若可与其他工作重叠，并不限制 step；判断要看重叠后仍暴露的等待边。
- **无事件 ≠ 隐藏等待**：设备空窗且无通信证据时，可能是工作在其他进程/设备活动未被采到/真实等待三种情况——没有采集完整性与依赖证据时只记"未解释空档"。
- **等待不是通信慢**：rank 在集合通信的等待首先说明"它先到了"，先按[慢 rank 指南](slow-rank-triage.md)找谁后到，再沿[带宽退化指南](../03-communication/bandwidth-degradation-triage.md)查链路。
- **时间重叠相加**：同一窗口内并行执行的区间相加会得到超过墙钟的假占比；按区间记录，不按算术和。
- **连续训练的 A/B 窗口不可直接比较**：训练推进本身改变 loss 与数据位置；无冻结起点/恢复设计的对比只是探索。
- **启用计时≠零扰动**：带 synchronize/barrier 的计时（如 Megatron timers）会插入同步等待，其结果不能与异步 trace 直接等同。
- **优化无收益但"看起来忙了"**：增加并行度可能只搬移了等待位置（如 PP stage 数变化把 bubble 从一端挪到另一端）；无有效产出变化即无收益。
- 版本/配置回归是常见入口：一个带完整证据链的公开案例见[训练吞吐回归来源案例](performance-regression-source-case.md)。

## 停止条件与恢复安排

- 采样扰动不可接受（开采集后 step 时间变化过大）：缩短窗口/降低采集级别（NPU level0 优先）或退回已有日志读取为主（注意其 synchronize/barrier 边界）；不通过给部分 rank 加组 barrier 的方式"修"计时；记录工具限制，不硬采。
- 瓶颈定位到本页范围之外（链路退化→[带宽退化指南](../03-communication/bandwidth-degradation-triage.md)；后端异常→04.6；降频→[供电散热证据](../01-hardware/power-thermal-evidence.md)）：移交对应指南，本页保留口径与已有证据。
- 优化变更导致失败/质量劣化：按配置记录回退（回退配置不撤销已发生的参数/优化器更新，恢复实验状态须回到冻结起点 checkpoint）；已完成的测量结果保留（负结果也是证据）。
- 无法保证等价比较状态（起点不可恢复、A 复测失败）：结论降级为探索性，不宣布优化通过。
- 无法取证的层（如 msprof 细节、Nsight 子页能力）：保留 unknown，不用推测填空。

## 完成判据

1. 口径表全部固定并随结果一起归档（配置身份与冻结起点可复现）。
2. 有从冻结起点恢复的重复基线噪声带；所有收益结论对照噪声带与非劣阈值表述。
3. 瓶颈结论带最早阻塞边的回溯证据与受害 rank 的区分，不只给阶段排名；未解释空档如实标注。
4. 每次优化有单因素变更记录（含联动派生维度）＋A→B→A 恢复复测＋吞吐与质量双指标。
5. 组合并行验证按模板记录（固定项/变更与派生维度/采集选点/分解/判据）。
6. 未取得证据的工具/层以 unknown 列出；结论范围限于已测配置，不外推其他拓扑/版本。

## 来源与验证记录

- [torch.profiler 2.6 文档](https://docs.pytorch.org/docs/2.6/profiler.html)；[Nsight Systems 2025.3 归档目录页](https://docs.nvidia.com/nsight-systems/2025.3/)（子页 403，取证受限如实记录）。
- verl v0.9.1：[Nsight 使用指南](https://github.com/volcengine/verl/blob/v0.9.1/docs/perf/nsight_profiling.md)、[torch profiler 使用指南](https://github.com/volcengine/verl/blob/v0.9.1/docs/perf/torch_profiling.md)、[昇腾 Profiling 指导](https://github.com/volcengine/verl/blob/v0.9.1/docs/ascend_tutorial/zh/dev_guide/performance/ascend_profiling.rst)。
- [TorchNPU profiler 源码](https://raw.githubusercontent.com/Ascend/pytorch/bc51ab84cc6f35c77aab1c59886e0ea43681a317/torch_npu/profiler/profiler.py)（固定 commit）；MindSpeed-LLM v2.2.0 get_profiler（既有条目补充核对）；[Megatron training_log/timers](https://github.com/NVIDIA/Megatron-LM/blob/core_v0.19.2/megatron/training/training.py)；[ROCprofiler-SDK 文档](https://rocm.docs.amd.com/projects/rocprofiler-sdk/en/docs-7.14.0/index.html)（既有条目）。
- 当前验证范围：仅来源核对，未运行任何 profiling 或优化实验。
- 待确认：Nsight 工具细节正文、CANN msprof 官方文档、rocprof 新旧边界、各工具采样扰动的官方量化（见来源记录 unknown 清单）。
