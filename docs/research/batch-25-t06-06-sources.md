# 第二十五批 T06-06 来源记录

任务：T06-06（训练性能分解、profiling 与优化验证；**new** procedure `knowledge/06-training/performance-analysis.md`，主题 06.2/06.6）。取证轮次：主会话作者角色首轮（2026-10-20）。工具文档按"能取得什么就固定什么"取证：Nsight Systems 归档目录页（子页 403）、verl profiling 使用指南（nsys/torch/NPU 三份）、TorchNPU profiler 源码、Megatron training_log/timers 源码、MindSpeed-LLM profiler 集成（补充核对既有条目）。未运行任何 profiling。

版本选择口径：PyTorch profiler 复用既有 src.pytorch.profiler-2.6；ROCm 侧复用 src.amd.rocprofiler-sdk-1.3.2-docs-7.14.0（SDK 1.3.2，与 ROCm 10.1.0 组件表的 1.4.1 为不同版本线，不混）；Nsight 固定归档 2025.3；verl 固定 v0.9.1（与 T06-04 同包）。

## 本轮取回清单（2026-10-20）

| 对象 | 版本 | SHA-256（前 16 位） |
|---|---|---|
| Nsight Systems 归档目录页 | 2025.3 | f8e799c12bfe87e9 |
| verl docs/perf/nsight_profiling.md | v0.9.1 | c89e235c02ae949e |
| verl docs/perf/torch_profiling.md | v0.9.1 | 38ff9641d832c4e7 |
| verl docs/ascend_tutorial/zh/dev_guide/performance/ascend_profiling.rst | v0.9.1 | 80278b812bda6b12 |
| torch_npu/profiler/profiler.py | TorchNPU bc51ab84 | a63f21d6214bb59c |
| Megatron megatron/training/training.py | core_v0.19.2 | d968ef8216f63d63 |
| Megatron megatron/core/timers.py | core_v0.19.2 | 14e76e6578adf7e6 |

取证限制：Nsight user-guide/quickstart 子页经 curl（含浏览器 UA）与 WebFetch 双路径均 AccessDenied/403，未取得工具细节正文——正文不转述未取得的 nsys 命令与选项。hiascend msprof 页面 HTTP 200 但需 JS 渲染，正文同样不取其命令细节；Ascend 侧以 TorchNPU profiler 源码＋verl/MindSpeed 集成使用证据替代，msprof 系统工具文档未取得如实记录。

## 主张—来源定位表

| 主张 | 登记 ID | 精确位置 | 支持范围 / 未覆盖 |
|---|---|---|---|
| Nsight Systems 版本化文档存在性 | NEW src.nvidia.nsight-systems-2025.3-archive | 目录页（Release Notes/Installation Guide/User Guide/Archives、last updated 2026-04-26） | 仅目录级证据；工具细节正文未取得（403），不转述 |
| RL 训练 nsys 采集样板 | NEW src.verl.nsight-profiling-v0.9.1 | nsight_profiling.md（capture-range cudaProfilerApi 固定、controller/worker 选项直传、角色配置、nsys-rep 落盘路径 /tmp/ray/session_latest/logs/nsight/） | 系统级工具如何嵌入多角色训练的官方使用面；nsys 版本以 docker 文件为锚 |
| torch profiler 采集样板 | NEW src.verl.torch-profiling-v0.9.1 | torch_profiling.md（global steps 列表＋角色 ranks 控制） | 与 nsys 同构的两层控制结构（应用级工具对照） |
| NPU 采集样板与级别 | NEW src.verl.ascend-profiling-v0.9.1 | ascend_profiling.rst（tool=npu、level_none/level0 推荐/level1/level2、contents npu/cpu/memory/shapes/module/stack、module 比 stack 开销低） | FSDP/MindSpeed 后端 GRPO/DAPO 训练的 NPU profiling 官方口径 |
| NPU profiler 接口面 | NEW src.ascend.torchnpu-profiler-source-7.2.0 | profiler.py：class profile(_KinetoProfile)、schedule/on_trace_ready、tensorboard_trace_handler、export_chrome_trace | TorchNPU 以 Kineto 接口暴露 NPU 采集；与 torch.profiler API 同构的差异点（ProfiperActivity.NPU、AiCMetrics）另见 MindSpeed 集成 |
| MindSpeed profiler 集成 | 补充核对 src.ascend.mindspeed-llm-training-interface-v2.2.0 | training.py：get_profiler/is_profile_enabled L214–275（torch_npu.profiler ProfilerLevel.Level0/1/2、ExportType Text/Db、AiCMetrics.PipeUtilization、schedule(wait/warmup/active/repeat/skip_first)、tensorboard_trace_handler） | Ascend 应用层 profiling 的 Megatron 系实现（training.py SHA 复核与登记一致） |
| 应用层吞吐口径 | NEW src.nvidia.megatron-training-log-core-v0.19.2 | training.py training_log L2568+：elapsed_time_per_iteration=L2825、TFLOPs＝num_floating_point_operations/(elapsed×10^12×world_size) L2832、log_throughput 开关 L2854、能耗/功率 L2863、advanced/skipped/nan iterations 计数、timers(barrier) 区间聚合 | 应用定义的吞吐/TFLOPs/跳步计数口径（与硬件计数器不可直接相加）；timers.py 为区间计时实现 |
| PyTorch profiler 能力 | 复用 src.pytorch.profiler-2.6 | （既有） | activities/schedule/export_chrome_trace/key_averages；页面无 NPU 说明、无多进程聚合视图 |
| NCCL/通信观测 | 复用 src.pytorch.processgroupnccl-env-2.8、src.nvidia.nccl-user-guide-2.27.5 | （既有） | 通信等待的观测入口（与慢 rank 指南互链） |
| AMD 侧工具边界 | 复用 src.amd.rocprofiler-sdk-1.3.2-docs-7.14.0 | （既有） | ROCprofiler-SDK 1.3.2（docs-7.14.0 线）：tracing＋计数器基础设施；新旧 rocprof 边界未逐条核对（既有缺口保留） |
| PP/EP 负载观测背景 | 复用 src.nvidia.megatron-training-loop-core-v0.19.2 | （既有，Batch 24） | 训练循环中 timers 的使用位置；本轮补 training_log 指标细节 |

## unknown 清单

1. Nsight Systems 工具细节正文未取得（子页 403）；nsys 命令、报告字段不在本库正文复述，仅经 verl 使用面引用。
2. CANN msprof 官方文档未取得（hiascend JS 渲染）；msprof CLI/图形工具细节保持 unknown，Ascend 侧正文以 torch_npu.profiler 接口面为界。
3. Nsight Compute（kernel 级）未取证；正文只在工具对照表中列出，不写能力细节。
4. rocprof/rocprofiler 新旧工具边界沿用既有条目的未核对缺口；ROCm 侧 torch profiler 的 HIP 活动映射未逐项核对。
5. verl profiling 指南的采集扰动数字无官方量化；正文只写"采样扰动须以基线对照评估"的方法要求。
6. Megatron TFLOPs 公式的 num_floating_point_operations 来源（config 字段）只取证到调用层，未逐模型核对。
7. 全部工具未运行；性能分解的判据由正文给设计，非实测阈值。

## 修订轮补充取证（2026-10-20，初审 B25-T06-C01–C07 后）

- **nsys 版本锚更正（C05）**：nsight_profiling.md 自述参考 `docker/Dockerfile.vllm.sglang.megatron`，该文件在 v0.9.1 不存在（文档陈旧引用，审阅轮核出）；实际核对 `docker/Dockerfile.stable.sglang`（SHA-256 99386acc562092ca81b167f681fd563b716c62fe87eff15b4348ac21d9dc2dd7）：ARG NSIGHT_VERSION=2025.6.1（L9）、安装 nsight-systems 2025.6.1（L52–59）。registry `src.verl.nsight-profiling-v0.9.1` notes 已同步更正；2025.6.1（verl 使用面）与 2025.3 归档目录页分立，正文表格已把"OS runtime"降为未核对。
- **Megatron timers 同步语义（C06）**：timers.py Timer.start/stop 两端 `torch.cuda.synchronize()`、可选 barrier；training_log interval-time 用 `elapsed(barrier=True)`。正文口径段已补"读取已有日志 vs 新启用计时"的区别。
- **verl torch_profiling.md 补充细读（C03）**：global_profiler.steps 按 RL step 选择、torch schedule 推进 update mini-batch；continuous 模式跳到较晚 active 窗口丢弃此前阶段；"Traces with no GPU kernels"为采集失败反例。正文采集计划已加计步单位与完整性门禁。
- 正文新增"组合并行性能验证入口"小节（C04，承接 06.2-G3）；优化验证补冻结起点与 A→B→A 恢复复测（C01）；阶段排名降为候选、阻塞链回溯与"未解释空档"（C02）；通信分支改直链并补 bandwidth-degradation-triage 回链（C07）。

## 第三轮修订（2026-10-20，复核轮二 C01–C04/R01 后）

- **C01**：新增"收益测量与质量观察协议"——profiling 窗口只用于定位，最终 A/B/恢复 A 吞吐在关闭 profiler、相同计时配置与热身/缓存策略下测量；质量按配对输入与等有效 token/更新预算观察；短窗口结论不外推完整收敛。
- **C02**：步骤 4 各分支落成"最低证据→支持/否定→下一步/unknown"可执行规则（PP 区分计划内 fill/drain vs 上游慢同形等待并按生产者→通信→消费者边回溯；EP/长度用配对路由计数区分工作量与单位效率；CPU/设备需连接主机阻塞与设备后续可执行的依赖证据）。
- **C03**：采集计划补窗口身份（外层 step/mini-batch 位置/schedule 推进点/continuous-discrete 模式/active 范围/导出 cycle 与文件对应；discrete 边界；多 cycle 逐个保存核对）。
- **C04**：组合并行小节补候选对照最小样例（TP4×PP2×DP8→TP4×PP4×DP4，联动重算项/约束检查/采集选点/结果表）；parallelism-and-state.md 组合并行节补性能验证入口回链。
- **R01**：步骤 2/6 的"只读"标签改为"主动实验"（恢复/复跑推进训练状态，隔离副本执行、保护冻结 checkpoint）。

## 第四轮修订（2026-10-20，复核轮三 C04 后）

- **C04**：候选对照样例真正填写——沿 parallelism-and-state 身份样例同一语境（64 rank/32 层/num_experts=128/EP=4）构造 A（tp2×pp2×cp2，dense dp=8）与 B（仅改 pp=4，dense dp=4）；联动重算项逐格填写（stage/layer 归属 16 层→8 层、micro-batch 换算 2→4 保持全局 batch、专家 grid 的 PP 一致约束使 expert_dp 4→2、EP 组放置随步长变化、采集选点按 stage 数变化）；约束检查代入硬断言逐项核对；A/B/恢复 A 结果表结构交付、运行字段全部标未执行。

## 第五轮修订（2026-10-20，复核轮四 C04 组成员填写后）

- **C04 最终填写**：B 侧代表 rank 37 的具体组成员补齐——dense 步长 tp1/cp2/dp4/pp16 下坐标 (pp=2,dp=1,cp=0,tp=1)，dense DP 组 {33,37,41,45}、PP 链 {5,21,37,53}（4 stage）、stage 2→第 16–23 层；专家步长 etp1/ep2/edp8/pp16 下 EP 组 {33,35,37,39}（仍在节点 4）、expert DP 组 {37,45}（4 副本缩为 2）、持有 expert 64–95 不变；B 采集选点写为具体 rank 集合（PP 链＋DP 组 37＋EP 组 37）。算术经本地复算。
