---
id: training.framework-execution
title: 训练框架组件、执行循环与平台职责对照
type: reference
domain: training
status: draft
platforms: [generic]
source_refs:
- src.pytorch.parallel-training-state-2.6
- src.pytorch.autograd-mechanics-2.6
- src.pytorch.optim-docs-2.6
- src.pytorch.torch-compiler-docs-2.6
- src.pytorch.torch-compile-api-2.6
- src.pytorch.torch-compile-troubleshooting-2.6
- src.pytorch.cuda-semantics-2.6
- src.pytorch.dispatcher-v2.6.0
- src.pytorch.distributed-backend-2.6
- src.pytorch.official-tests-v2.6.0
- src.pytorch.hip-notes-2.6
- src.nvidia.megatron-training-loop-core-v0.19.2
- src.nvidia.megatron-lm-core-v0.19.2
- src.ascend.mindspeed-llm-training-interface-v2.2.0
- src.ascend.mindspeed-llm-ha-v2.2.0
- src.ascend.torch-npu-v7.2.0-pytorch2.6.0
- src.nvidia.megatron-examples-core-v0.12.1
updated_at: "2026-10-18"
summary: 建立训练驱动、autograd、分布式封装、optimizer、编译、算子后端与 checkpoint 接口的职责图，比较 PyTorch 2.6、Megatron-Core core_v0.19.2 与 MindSpeed-LLM v2.2.0 三组独立资料档案，并给出各阶段故障分界与小规模执行路径验证方法。
related_ids:
- training.parallelism-and-state
- training.checkpoint-state-consistency
- software-stack.operators-compilers-and-graphs
verification:
  status: source_checked
  evidence_refs:
  - src.pytorch.autograd-mechanics-2.6
  - src.pytorch.optim-docs-2.6
  - src.nvidia.megatron-training-loop-core-v0.19.2
  - src.ascend.mindspeed-llm-training-interface-v2.2.0
  notes: 仅核对固定 tag 源码与版本化文档语义（锚点见 docs/research/batch-24-t06-02-sources.md）；未运行任何训练代码、未编译任何模型、未安装 Megatron/MindSpeed/TorchNPU。eager/compiled 行为差异以官方文档为限，未实测。
---

# 训练框架组件、执行循环与平台职责对照

本页回答"训练框架把哪些组件组装成执行循环、各组件对什么负责、出问题时在哪一层分界"。算子分发、编译器与图执行的机制细节归 02 章（见[算子分发、编译与计算图执行机制](../02-software-stack/operators-compilers-and-graphs.md)）；并行策略的状态责任归[并行策略与训练状态](parallelism-and-state.md)；checkpoint 文件语义归 04 章。

## 范围与阅读方式

对照对象是三组**互相独立**的资料档案（版本边界见下节），不是一个可拼装的统一栈：PyTorch 2.6（文档＋v2.6.0 源码）、NVIDIA Megatron-LM tag `core_v0.19.2`、Ascend MindSpeed-LLM tag `v2.2.0`。同名概念（如 optimizer、schedule）在三者中职责相似但接口不同，不默认等价。

## 训练执行循环的职责图

一个典型训练 step 的组件链与其责任：

```
训练驱动（train loop）
 ├─ 数据迭代器        → 产出 batch；随机性与游标状态（06.1 状态矩阵）
 ├─ forward_step_func → 调用模型得到 loss；观测挂点：timers、loss 标量
 ├─ 分布式封装        → DDP/FSDP/TP/PP/CP/EP 组合；通信发生在域边界（并行页）
 │    └─ PP schedule  → forward/backward 在 stage 间的次序与 activation 传递
 ├─ autograd          → 记录并反向遍历计算图；no_grad/inference mode 边界
 ├─ optimizer         → 持有当前 state、按梯度更新参数；param groups
 ├─（可选）编译        → torch.compile/图模式：执行路径变化，数值语义另行验证
 ├─ 算子后端          → dispatcher 选设备实现（02 章）
 └─ checkpoint 接口   → 把上述状态按截取边界落盘（04 章＋06.1）
```

PyTorch 侧官方语义：autograd 是 reverse 自动微分系统，按执行顺序记录 DAG，从输出向输入反向求导（[Autograd mechanics](https://docs.pytorch.org/docs/2.6/notes/autograd.html) L585–590）；局部禁用梯度用 no-grad/inference mode 上下文（L659–663）；计算图按迭代重建。`retain_graph` 的时序语义：**只有计划对同一张图再次求导、且反向依赖其中间量时，才需要在会释放这些中间量的那次 backward 调用中传 `retain_graph=True`**（图释放发生在该次反向中；之后再补传无法追溯恢复，只能重新 forward 重建图——[Autograd mechanics](https://docs.pytorch.org/docs/2.6/notes/autograd.html) L901–910 及 saved-variable 语义）。常规下一迭代经新的 forward 产生新图，不由此推出每步都要保图。optimizer 构造时接收参数可迭代对象（或 named_parameters），持有当前 state 并按计算出的梯度更新参数，param groups 支持逐组超参（[torch.optim](https://docs.pytorch.org/docs/2.6/optim.html) L585–632）。

Megatron 侧（core_v0.19.2）：`train_step` 组合 forward_step_func、数据迭代器、模型、optimizer、opt_param_scheduler 与 schedule（[training.py](https://github.com/NVIDIA/Megatron-LM/blob/core_v0.19.2/megatron/training/training.py) L2336）；schedule 由 `get_forward_backward_func` 按 pp/vp 规模选择，interleaved（VPP）与 without-interleaving 两族实现在 [schedules.py](https://github.com/NVIDIA/Megatron-LM/blob/core_v0.19.2/megatron/core/pipeline_parallel/schedules.py) L48、L992、L2120；`backward_step` 在非最后 stage 接收 output_tensor_grad（L532）。分布式优化器把 optimizer state 分片到 DP 组（[distrib_optimizer.py](https://github.com/NVIDIA/Megatron-LM/blob/core_v0.19.2/megatron/core/optimizer/distrib_optimizer.py) L113–124）。

MindSpeed-LLM 侧（v2.2.0）：`mindspeed_llm.training.pretrain` 的 docstring 给出四步职责链——initialize Megatron→setup model/optimizer/lr schedule→取数据集→train（[training.py](https://github.com/Ascend/MindSpeed-LLM/blob/v2.2.0/mindspeed_llm/training/training.py) L377 起）；即 MindSpeed-LLM 以包裹/扩展 Megatron 入口的方式提供平台能力，`build_train_args`（L291）与 wrapper 族（get_model_wrapper L188 等）是注入点。其 install_guide 固定 MindSpeed core `2.2.0_core_r0.12.1` 与 Megatron-LM `core_v0.12.1`。

## eager 与 compiled 的 step 路径

以 PyTorch 2.6 样板说明同一步在两种路径下的数据/控制流差异。**本表的编译样板明确选定为"仅 `compile(model)`"**（只包装模型/前向调用；外层训练驱动、optimizer、scaler、scheduler 与分布式 hook 保持 eager）——这是下表的对照前提；官方文档也允许把 optimizer 等训练可调用对象纳入编译范围（此时 optimizer frame 的 guard 失配会触发重编译，观测语义随之变化；示例见 [troubleshooting：Where to apply torch.compile](https://docs.pytorch.org/docs/2.6/torch.compiler_troubleshooting.html#where-to-apply-torch-compile) 与 [Wrapping constants with tensors](https://docs.pytorch.org/docs/2.6/torch.compiler_troubleshooting.html#wrapping-constants-with-tensors)——后者含 optimizer/scheduler 与学习率 guard 失配示例），该变体不在本表范围内、需另行对照：

| step 组成部分 | eager 路径 | compiled 路径（对被包装对象） | 观测挂点 |
|---|---|---|---|
| 数据装载/预处理 | 每次迭代正常执行 | 通常在编译区外（除非单独包装） | DataLoader 指标、sampler 游标 |
| forward | 逐算子执行，autograd 边推边记图 | Dynamo 捕获 Python/图，AOT Autograd 捕获反向，默认 Inductor 生成优化执行体（[torch.compiler](https://docs.pytorch.org/docs/2.6/torch.compiler.html) L589–600） | 编译日志与图 break 计数（[troubleshooting 的 Logging tools/Backend ablation](https://docs.pytorch.org/docs/2.6/torch.compiler_troubleshooting.html) L670 起） |
| backward | autograd 遍历本迭代记录的图 | 反向随 AOT 捕获进入编译体；graph break 处**分段**执行（break 后回退分段语义） | 同上；分段位置是 compiled 特有观测点 |
| 梯度同步/累积 | DDP/FSDP hook 按其语义执行 | **编译区外（本表样板）**——逻辑上的更新/跳步契约（并行页三情形表）不受编译影响；若改用含 optimizer 的编译范围，则 guard 失配与重编译成为该行的额外观测项 | hook 时间线（eager hook 无对应编译 frame）；模型编译区的重编译**先核对 guard 原因**（形状/dtype/设备特化与动态形状发现属正常行为），仅稳定输入与预热基线下的异常频度才作检查项（该基线属验证设计、未建立） |
| optimizer update / scaler / scheduler | 正常执行，跳步分支见[并行页单步边界](parallelism-and-state.md) | **编译区外（本表样板）**；其推进契约是逻辑层的，与是否编译解耦 | update_successful/skipped 计数 |

判读边界：**编译成功只说明改写后的可执行体生成并可运行，不构成数值正确性保证，也没有"框架自检通过数值"这回事**——重写引入的算子替换、精度与随机性行为差异要用同输入对照验证（06.5/08.6 的方法），可用编译侧的精度对照工具辅助（troubleshooting 页 Accuracy 相关小节）。缓存使"第二次运行与第一次不同"成为预期。Megatron/MindSpeed 对 torch.compile 的支持状态未取证（unknown）；两者的执行路径按 eager＋自有融合算子描述。

## 三组资料档案与版本边界

| 档案 | 模型/程序范围 | 框架与依赖 | 硬件边界 | 未知项 |
|---|---|---|---|---|
| PyTorch 通用样板 | 通用张量程序与官方文档示例（未绑定具体模型）；文档 2.6＋源码 tag v2.6.0 | CUDA 构建语义按 [cuda-semantics](https://docs.pytorch.org/docs/2.6/notes/cuda.html)（stream/异步/缓存分配器）；ROCm 构建差异按 [HIP notes](https://docs.pytorch.org/docs/2.6/notes/hip.html)；与具体加速卡/驱动/NCCL 版本的配套未核 | CUDA 与 ROCm 构建分别适用；NPU 不在本档案内 | 与任何具体 NPU 栈的配套；官方测试面广阔未逐项映射（见测试定位表） |
| NVIDIA Megatron-Core | 本页引用其训练循环/调度/分布式优化器实现（training.py、schedules.py、distrib_optimizer.py；面向 GPT 类大模型训练，未绑定具体模型配置）；tag core_v0.19.2 | 通信语义引用 03 章 NCCL 档案（未核版本配套）；并行度参数由 `ModelParallelConfig`/`TransformerConfig` 字段经参数工厂生成 CLI（[arguments.py](https://github.com/NVIDIA/Megatron-LM/blob/core_v0.19.2/megatron/training/arguments.py) L2290 起＋[argument_utils.py](https://github.com/NVIDIA/Megatron-LM/blob/core_v0.19.2/megatron/training/argument_utils.py) L96–107、L214–229 把 dataclass 字段转成 `--kebab-case` 旗标；CLI 实际解析未运行） | NVIDIA GPU（代际未逐一限定；MoE 通信重叠的 Hopper 分界见[并行页](parallelism-and-state.md)） | 具体硬件支持矩阵；rerun_state_machine、调度数值公式、CUDA graph full-iteration 路径未逐行核对；对 torch.compile 的支持 |
| Ascend MindSpeed-LLM | 本页引用 `mindspeed_llm/training` 入口与参数校验（未绑定具体模型配置）；tag v2.2.0 | README 依赖表：PyTorch 2.7.1、Python 3.10；NPU 驱动/固件/Toolkit/NNAL/torch_npu/apex 均为"在研版本"；install_guide 固定 MindSpeed core `2.2.0_core_r0.12.1`＋Megatron-LM `core_v0.12.1` | 昇腾 NPU（型号未核） | 在研组件的实际配套不可核；MindSpeed core 仓本体源码未取回；torch.compile 支持 |

三组档案两两不组成同一软件环境：MindSpeed-LLM v2.2.0 组合的是 core_v0.12.1，不是 core_v0.19.2；PyTorch 2.6 与 MindSpeed-LLM 所需 2.7.1 是不同样板；TorchNPU v7.2.0-pytorch2.6.0 条目覆盖的是 2.6 组合，与 MindSpeed-LLM 的在研 torch_npu 不是同一配套。引用任何一组的结论时版本随行。

**AMD/ROCm 边界（本页采用的执行差异，均为 2.6 版本化文档原文）**：HIP 复用 CUDA 命名接口（同一 API 名在 HIP 构建下映射到 ROCm 实现，[HIP notes](https://docs.pytorch.org/docs/2.6/notes/hip.html) "Reuse the CUDA Interfaces"）；HIP 构建判别方法见同页 "Checking for HIP"；该版本文档还记录了 TF32 与 `torch.distributed` 后端在 ROCm 侧的限制（同页相应小节），分布式支持条件以 [PyTorch 2.6 distributed](https://docs.pytorch.org/docs/2.6/distributed.html) 为准，NCCL 结论不得平移。另注：AMD 官方 [ROCm 7.1.1 PyTorch 兼容页](https://rocm.docs.amd.com/en/docs-7.1.1/compatibility/ml-compatibility/pytorch-compatibility.html)（`src.amd.pytorch-compatibility-7.1.1`）属**独立版本线**（覆盖 PyTorch 2.9＋ROCm 7.1.1、2.7/2.8＋ROCm 7.0 分节），不拼入本页 PyTorch 2.6 组合。**不声称 NVIDIA Megatron 或 MindSpeed-LLM 可直接迁移到 AMD**：两者的设备相关路径在 ROCm 上的等价物未取证（unknown）。

## 各阶段故障分界与小规模验证方法

| 阶段 | 典型症状 | 分界证据 | 归属层 |
|---|---|---|---|
| 初始化 | 进程组/设备初始化失败、mesh 不一致 | init_process_group/parallel_state 报错位置；组成员表打印 | 分布式封装/环境（02.7、03.6） |
| first step | 首步即错（形状/连接错误） | 形状断言、TP/PP 连接处的 shape 通信日志 | 模型并行映射（并行页冲突检查表） |
| backward/update | loss 正常但梯度/更新异常 | grad 范数、overflow 决议、optimizer state 分片重建日志 | autograd/optimizer/精度（06.5） |
| 保存/加载 | checkpoint 后无法续训 | 截取边界断言、恢复后首步 loss 对比 | checkpoint 接口（04 章＋06.1/06.7） |
| 编译路径 | 仅 compiled 下异常 | eager 与 compiled 同输入对照；缓存清理后复现 | 编译/算子后端（02 章） |

**小规模执行路径验证方法（设计，未执行；连通性检查与恢复一致性分开）**：

- **连通性检查**：单机小规模（如单卡或 2 卡）小模型跑通"初始化→first step→backward/update→保存"的执行路径，逐步引入一个并行维度或一个平台组件，每次只变更一项；观测项为首步 loss 数值、梯度范数是否产生、`update_successful`/跳步计数是否按预期分叉。这证明执行路径连通，不证明数值正确或生产规模可用。
- **恢复一致性检查（另一类判断，判据须先约定）**：**本设计选定"完整 optimizer step 边界"为截取点**（截取条件与状态清单沿用[并行页](parallelism-and-state.md)"截取边界"与"单步内的所有权与合法跳步"两节：无飞行 micro-batch、无待提交梯度、scaler 已 `update()`、scheduler/数据提交计数推进到同一逻辑点）。设未中断参考分支与恢复分支：两者从**同一截取点保存的状态**出发（保存内容含模型、optimizer、scheduler、scaler、**各 RNG 的截点状态**——恢复分支加载的是保存的 generator 状态本身，不是"同 seed 重放"）、消费**同一后继输入**（固定数据切片，游标随截点恢复）；观测项为恢复分支首个成功更新的 loss/梯度范数与参考分支同位步的差异、`update_successful`/跳步计数、可训练参数与 optimizer 参数组的成员对照；比较规则（哪些量、多大容差、比较几步）**事先写定**，不确定即停止并按 08 章假设检验展开。参数更新是否生效与合法跳步（overflow 不更新但 scaler/样本计数推进，见[并行页](parallelism-and-state.md)）是独立观测项，不用 loss 单值混判。
- 官方参照示例的边界：Megatron 的 [run_simple_mcore_train_loop.py](https://github.com/NVIDIA/Megatron-LM/blob/core_v0.12.1/examples/run_simple_mcore_train_loop.py) 是**合成数据示例**（MockGPTDataset；硬编码 TP=2、PP=1），其保存/加载函数只处理模型 state，且循环在加载前结束——不含 optimizer/RNG/数据游标的完整恢复与"加载后再走一步"的对照（[脚本](https://github.com/NVIDIA/Megatron-LM/blob/core_v0.12.1/examples/run_simple_mcore_train_loop.py) L107–115、L118–157）。完整状态闭环属待补验证设计，不在本页伪造。

## 源码—职责定位表（实现 + 测试/断言）

| 文件（固定 tag） | 职责 | 观测挂点 | 对应测试/断言（未运行） |
|---|---|---|---|
| PyTorch v2.6.0 `torch/optim/optimizer.py` L235 起/L644/L841/L940/L1012 起 | optimizer 基类、param groups、state_dict、zero_grad | state_dict、梯度为 None 行为 | 官方测试（已读未运行；SHA-256 76cf0c7a…）：[test_optim.py](https://github.com/pytorch/pytorch/blob/v2.6.0/test/test_optim.py) `test_state_dict_deterministic` L1352（L1403–1439：克隆参数、加载 optimizer state 后**继续更新并对照参数值、状态与参数组**——state_dict 装载后更新等价性，非完整应用 checkpoint/RNG 恢复证明）；`test_state_dict_with_cuda_params` L1648（**onlyCUDA 参数化限定**；L1697–1717 检查加载不改写输入 state、step 后状态设备与后续更新）；state_dict pre/post hook L1735/L1748 |
| PyTorch v2.6.0 `torch/autograd`（[notes/autograd](https://docs.pytorch.org/docs/2.6/notes/autograd.html)） | 计算图记录与 backward（图按迭代重建） | no_grad 块；retain_graph 的条件与时序见上文"PyTorch 侧官方语义"完整定义（同图再次求导且需其中间量时，在会释放它们的先前 backward 中保留） | 官方测试（已读未运行；SHA-256 a8daf1cb…）：[test_autograd.py](https://github.com/pytorch/pytorch/blob/v2.6.0/test/test_autograd.py) `test_grad` L902（`grad()` 对指定输入求导并对照）；`test_backward` L2263（L2270–2280 对照解析梯度）；`test_backward_badcalls` L1608（L1608–1611：对 requires_grad=False 输入调用 backward 报错——错误边界） |
| PyTorch v2.6.0 `torch.compiler` 公共 API | 编译入口与回退边界 | 编译日志、重编译计数 | 官方测试（已读未运行；SHA-256 36745171…）：[test/dynamo/test_compile.py](https://github.com/pytorch/pytorch/blob/v2.6.0/test/dynamo/test_compile.py) `InPlaceCompilationTests.test_compilation` L25–32（`ToyModel`＋`model.compile(backend=CompileCounter)`，单次调用后断言 frame 数为 1）、`test_dynamo_signatures` L163–173（公共/内部 API 签名一致性——**不验证完整训练 step、编译数值或 optimizer/scheduler 路径**） |
| Megatron core_v0.19.2 `megatron/training/training.py` L2336/L2017/L3342 | train_step、setup_model_and_optimizer、train 主循环 | timers、save_params/save_activations/save_tokens_per_expert 按间隔分支 | 本轮未定位 train_step 专项单测（缺口） |
| Megatron core_v0.19.2 `megatron/core/pipeline_parallel/schedules.py` L48/L992/L2120 | 调度选择与 forward/backward 执行 | forward_step/backward_step 边界、tensor shape 通信 | [test_schedules.py](https://github.com/NVIDIA/Megatron-LM/blob/core_v0.19.2/tests/unit_tests/pipeline_parallel/test_schedules.py) L47–76 `test_get_forward_backward_func`：断言配置为 TP=2 下 PP=1→no_pipelining、PP=4 无 VP→without_interleaving、PP=4/VP=2 与 PP=2/VP=4→with_interleaving（SHA-256 5854bac1…；已读未运行）。**环境前提**：该测试经 `Utils.initialize_model_parallel` 进入真实分布式初始化（CUDA 设备＋NCCL 进程组），需要 GPU/多进程环境，不是纯函数单测；它只验证调度函数选择，不验证数值、通信完成或完整 step |
| Megatron core_v0.19.2 `megatron/core/optimizer/distrib_optimizer.py` L113 | DP 组内 optimizer state 分片 | data_parallel_group、per_model_buffers | 本轮未定位 distributed optimizer 专项单测（缺口） |
| MindSpeed-LLM v2.2.0 `mindspeed_llm/training/training.py` L291/L377/L515 | 包裹 Megatron 入口、构建训练参数 | build_train_args、e2e metrics（L586） | MindSpeed 侧测试（tests/ut、tests/st）未逐项核对（缺口） |
| MindSpeed-LLM v2.2.0 `mindspeed_llm/training/arguments.py` L35/L242/L1015 | 平台扩展参数与冲突校验 | ValueError/AssertionError 消息 | 同上 |

测试覆盖现状：NVIDIA 档案有调度选择测试、PyTorch 档案已完成 optimizer/autograd/compile 三组代表性测试的具名映射（断言与适用条件见上表）；MindSpeed 侧测试（tests/ut、tests/st）与 PyTorch 更大测试面（如完整训练循环、分布式端到端）的映射仍未完成——缺口如实记录，不以已映射部分外推全覆盖，也不以 NVIDIA 测试套用到其他平台。

第三方组件（如 MindSpeed-LLM 调用的 Megatron `generate_state_dict`、MindSpeed core 补丁）的源码调用只能说明**接口接触点**；未读取的内部协议保持 `unknown`，不从接口形状推定行为。

## 使用与解释注意事项

- 同名不同义：Megatron `train_step` 与 PyTorch 训练循环的"step"在不同粒度（含 schedule 与 micro-batch 循环）；不同实现的 optimizer state_dict 布局**不能默认互换**（跨 PyTorch/Megatron/MindSpeed 的兼容性未验证；仅已读的具体格式可作有条件比较），也不要反过来断言存在互转能力。
- "训练在跑"不是任何一层的健康证据；按上表分界取证。
- 编译缓存使重复运行行为不同；排查时区分首次与缓存后路径。
- 三组档案的结论不得跨版本/跨平台拼接引用。

## 来源与更新范围

取证记录与逐条锚点见 [batch-24-t06-02-sources](../../docs/research/batch-24-t06-02-sources.md)。本页为 draft；未运行任何所引代码，未建立环境档案。
