# 第二十四批 T06-02 来源记录

任务：T06-02（训练框架组件、执行循环与平台职责对照；**new** reference `knowledge/06-training/framework-execution.md`，主题 06.3）。取证轮次：主会话作者角色首轮（2026-10-18；子代理 403，改主会话直接取证）。方式：curl 字节级取回（SHA-256 见下）＋ codeload 源码包；未运行任何训练代码。目标正文是"职责对照 reference"，与 02 章分工：02 讲算子分发/编译/后端适配机制，本页讲训练框架把 autograd/optimizer/分布式/编译/checkpoint 组装成执行循环的职责与三组档案。

## 三组独立资料档案（版本边界，不拼成同一套环境）

| 档案 | 固定版本 | 关键边界 |
|---|---|---|
| PyTorch 通用样板 | 文档 2.6 / 源码 tag v2.6.0 | 与既有 src.pytorch.*-2.6 系列同源；CUDA 语义按 cuda-semantics-2.6；ROCm 差异按 hip-notes-2.6/distributed-backend-2.6，不声称与 NPU 配套 |
| NVIDIA Megatron-Core | tag core_v0.19.2 | 复用既有冻结条目 src.nvidia.megatron-lm-core-v0.19.2；本轮新开 training.py/schedules.py/distrib_optimizer.py 三个文件锚点 |
| Ascend MindSpeed-LLM | tag v2.2.0（codeload） | **README 依赖表：PyTorch 2.7.1、torch_npu/驱动/固件/Toolkit/NNAL 均为"在研版本"；install_guide 固定 MindSpeed core `2.2.0_core_r0.12.1` 与 Megatron-LM `core_v0.12.1`**——即 MindSpeed-LLM v2.2.0 组合的是 core_v0.12.1，不是本页另一档案的 core_v0.19.2；两组 Megatron 样板分开陈述，不混用 |

## 本轮取回清单（2026-10-18）

| 对象 | 版本 | SHA-256（前 16 位） |
|---|---|---|
| megatron/training/training.py | core_v0.19.2 | d968ef8216f63d63 |
| megatron/core/pipeline_parallel/schedules.py | core_v0.19.2 | 9d3624f4b1bc8e9e |
| megatron/core/optimizer/distrib_optimizer.py | core_v0.19.2 | 40cae307ccb2a3f4 |
| docs.pytorch.org/docs/2.6/notes/autograd.html | 2.6 | 792703d16102b45c |
| docs.pytorch.org/docs/2.6/optim.html | 2.6 | 53351ea89339ffb9 |
| MindSpeed-LLM README.md | v2.2.0 | 7b4893c93e8884d1 |
| MindSpeed-LLM docs/pytorch/install_guide.md | v2.2.0 | 8dd60a6cc0983ffc |
| mindspeed_llm/training/training.py | v2.2.0 | 341c0792484b7113 |
| mindspeed_llm/training/arguments.py | v2.2.0 | fd64204269ad1749 |

## 主张—来源定位表

| 主张 | 登记 ID | 精确位置 | 支持范围 / 未覆盖 |
|---|---|---|---|
| Megatron 训练循环骨架 | NEW src.nvidia.megatron-training-loop-core-v0.19.2 | training.py：`train_step` L2336（docstring "Single training step"；含 rerun_state_machine、save_params/save_activations/save_tokens_per_expert 按间隔分支）；`setup_model_and_optimizer` L2017；`train()` L3342；从 megatron.core.pipeline_parallel 导入 `get_forward_backward_func` L98、在 train() 内取 schedule L3614 | 训练 step=forward_step_func+数据迭代+schedule+optimizer+opt_param_scheduler 的组合点；观测挂点（timers、per-iteration 保存分支）。未读 rerun_state_machine 细节（unknown） |
| Megatron 流水线调度实现 | NEW src.nvidia.megatron-training-loop-core-v0.19.2 | schedules.py：`get_forward_backward_func` L48（按 pp_size/vp_size 选择调度）；`forward_backward_pipelining_with_interleaving` L992；`forward_backward_pipelining_without_interleaving` L2120；`forward_step` L397；`backward_step` L532（非最后 stage 收 output_tensor_grad） | interleaved（VPP）与 1F1B 类调度的实现入口与选择逻辑；forward/backward 在 stage 间的执行边界。具体 warmup/steady 数值公式未逐行核（以函数结构为限） |
| Megatron 分布式优化器 | NEW src.nvidia.megatron-training-loop-core-v0.19.2 | distrib_optimizer.py：`class DistributedOptimizer` L113（docstring：**shard state across data-parallel ranks**、把 momentum/variance 等 optimizer state 分布到 DP 组、model_chunks/per_model_buffers/data_parallel_group 属性） | 分布式优化器的分片职责与 all-gather 组关系；与 06.1/06.2 的状态责任矩阵互链 |
| autograd 机制语义 | NEW src.pytorch.autograd-mechanics-2.6 | notes/autograd.html：L585–590（reverse automatic differentiation、DAG 记录历史、roots→leaves）；L659–663（局部禁用梯度：no-grad/inference mode 上下文管理器）；L905–910（同一计算图再次求导且需要其中间量时需 retain_graph=True——须在会释放中间量的先前 backward 中保留；已释放后无法追溯；线程安全边界） | 训练循环中 backward 的官方语义与 no_grad 边界；saved tensors/非可微函数细节在页内其他节，按需引用 |
| torch.optim 职责 | NEW src.pytorch.optim-docs-2.6 | optim.html：L585–595（构造 optimizer 持有当前 state、按计算出的梯度更新参数）；L589–601（参数可迭代/named_parameters）；L606–632（param groups 与逐组超参） | optimizer 在执行循环中的职责边界（持有 state、按梯度更新）；state_dict 语义已由既有 parallel-training-state-2.6 覆盖 |
| MindSpeed-LLM 训练入口与 Megatron 关系 | NEW src.ascend.mindspeed-llm-training-interface-v2.2.0 | mindspeed_llm/training/training.py：`pretrain()` L377（docstring 四步：**initialize Megatron→setup model/optimizer/lr schedule→数据集→train**）；`build_train_args` L291；`train()` L515；wrapper 族（get_model_wrapper L188、build_train_valid_test_data_loaders_wrapper L200） | MindSpeed-LLM 是包裹/扩展 Megatron 训练入口的职责链证据；per-task 注入点结构 |
| MindSpeed-LLM 参数校验与冲突检查 | NEW src.ascend.mindspeed-llm-training-interface-v2.2.0 | arguments.py：`extra_args_provider_decorator` L35；`_validate_cp_args` L242+（进入条件：该检查位于 ulysses/mamba/hybrid 各 CP 算法分支内、且要求 --use-mcore-models；num_attention_heads 须能被 ulysses_size×TP 整除且商 ≥1；GQA 分支（group_query_attention 开启且 num_query_groups ≥ 1 时进入）为串联除法：先 num_query_groups % TP == 0 且商 ≥1，再在未启用 kv_head_repeat_before_uly_alltoall 时要求该商 (num_query_groups/TP) % ulysses_size == 0 且商 ≥1——在正整数前提下等价于 num_query_groups 能被 TP×ulysses 整除，不是分别被 TP 和 ulysses 整除；开关绕过的是第二层检查，代价是通信与内存增加）；`_validate_instruction_finetune` L1015；`_validate_train_mode_conflict` L1023 | 平台侧组合约束校验的实例（CP×TP×GQA 头数），也供 T06-01 组合冲突表引用 |
| MindSpeed-LLM 依赖配套 | NEW src.ascend.mindspeed-llm-training-interface-v2.2.0 | README 依赖表 L57–95（PyTorch 2.7.1；驱动/固件/Toolkit/Kernel/NNAL/torch_npu/apex 在研版本；Python 3.10）；install_guide L56–76（MindSpeed `2.2.0_core_r0.12.1`、Megatron-LM `core_v0.12.1`、拷贝 megatron 目录进 MindSpeed-LLM） | "真正固定的 Mcore 依赖"=core_v0.12.1；在研组件保持 unknown，不与 PyTorch 2.6/CUDA 样板或 core_v0.19.2 拼配 |
| torch.compile/编译路径 | 复用 src.pytorch.torch-compiler-docs-2.6＋torch-compile-api/troubleshooting/faq/dynamic-shapes/cudagraph-trees-2.6＋compile-caching-tutorials | （Batch 17/16 已核对） | eager/compiled 的官方语义、常见陷阱与缓存行为；本轮未重开 |
| CUDA 执行语义（stream/event/分配器） | 复用 src.pytorch.cuda-semantics-2.6＋cuda-caching-allocator-v2.6.0 | （既有） | 异步执行、内存池与 stream 语义。本轮未重开 |
| TorchNPU 执行侧 | 复用 src.ascend.torch-npu-v7.2.0-pytorch2.6.0＋torchnpu-amp/stream-event/graphs-7.2.0 | （既有） | NPU 侧 autocast/stream/graph 差异。本轮未重开 |
| ROCm 执行差异 | 复用 src.pytorch.hip-notes-2.6＋distributed-backend-2.6＋amd.pytorch-compatibility-7.1.1 | （既有） | AMD 后端支持条件；不声称 Megatron/MindSpeed 可迁移 |
| dispatcher/算子注册 | 复用 src.pytorch.dispatcher-v2.6.0 | （既有） | 算子分发与设备后端注册的 02 章互链基础。本轮未重开 |

## 源码—职责定位表（写作骨架输入）

| 文件（tag） | 职责 | 观测挂点 |
|---|---|---|
| pytorch v2.6.0 torch/optim/optimizer.py（既有条目覆盖 state_dict 语义） | optimizer 基类、step/zero_grad、param groups | state_dict、梯度为 None 行为 |
| pytorch v2.6.0 torch/autograd（notes/autograd.html L585+） | 计算图记录与 backward | no_grad 块、retain_graph 错误 |
| Megatron core_v0.19.2 training.py L2336/L3342 | 单步与整循环组装 | timers、save_*_interval 分支、rerun_state_machine（细节 unknown） |
| Megatron core_v0.19.2 schedules.py L48/L992/L2120 | PP 调度选择与执行 | forward_step/backward_step 边界、tensor shape 通信 |
| Megatron core_v0.19.2 distrib_optimizer.py L113 | DP 组内 optimizer state 分片 | data_parallel_group、buffers |
| MindSpeed-LLM v2.2.0 training.py L291/L377/L515 | 包裹 Megatron 入口、构建参数 | build_train_args、e2e metrics（L586 get_e2e_base_metrics） |
| MindSpeed-LLM v2.2.0 arguments.py L35/L242/L1015 | 平台扩展参数与冲突校验 | ValueError/AssertionError 消息 |

## unknown 清单

1. Megatron `rerun_state_machine`、warmup/steady 调度数值公式、`full_iteration` CUDA graph 路径未逐行核对；正文以函数职责为限。
2. MindSpeed **core 仓**（`2.2.0_core_r0.12.1`）本体源码未取回（gitcode 外链；本轮只有 MindSpeed-LLM 侧的 checkout 指令证据）；其补丁注入点明细 unknown。
3. MindSpeed-LLM v2.2.0 README 的"实测预训练性能"表未采用（厂商口径，非本库结论）。
4. PyTorch 2.6 与 MindSpeed-LLM 所需 PyTorch 2.7.1 属不同样板；TorchNPU v7.2.0-pytorch2.6.0 条目覆盖的是 2.6 组合，与 MindSpeed-LLM 在研 torch_npu 不是同一配套。
5. `torch.compile` 全链路（dynamo/inductor 内部）已由 02 章/既有条目按需覆盖，本页只引用不重述；Megatron/MindSpeed 对 torch.compile 的支持状态未取证（unknown）。
6. 未运行任何代码；全部职责判断为源码结构转述。

## 建议登记条目（4 条新增）

```yaml
- id: src.nvidia.megatron-training-loop-core-v0.19.2
  title: NVIDIA Megatron-LM tag core_v0.19.2 训练循环/流水线调度/分布式优化器（冻结实现）
  url: https://github.com/NVIDIA/Megatron-LM/blob/core_v0.19.2/megatron/training/training.py
  kind: repository
  registered_at: '2026-10-18'
  revision: tag core_v0.19.2；curl raw 取回 2026-10-18（training.py SHA-256 d968ef8216f63d6373372190ac895fc905234c116bba3e804d2951876e6ad98c、schedules.py 9d3624f4b1bc8e9e4747f339587b3dab2560e0fc5faa9fecd736e4eed2d5f1b7、distrib_optimizer.py 40cae307ccb2a3f484ebd5d28ee8549eb572d1b0ba6e91dc5661c137bf560907）
  license:
    status: unknown
    scopes: []
    notes: Apache-2.0 为仓库主许可（未逐文件核对头声明）；仅链接并原创归纳。
  notes: Batch 24（T06-02）取证：training.py train_step/setup_model_and_optimizer/train 与 per-iteration 保存分支；schedules.py get_forward_backward_func（pp/vp 选择）、interleaved 与 without-interleaving 调度、forward_step/backward_step；distrib_optimizer.py DistributedOptimizer（DP 组内分片 optimizer state、model_chunks/buffers 属性）。rerun_state_machine 与调度数值公式未逐行核对。未运行代码。
- id: src.pytorch.autograd-mechanics-2.6
  title: PyTorch 2.6 Autograd mechanics 笔记
  url: https://docs.pytorch.org/docs/2.6/notes/autograd.html
  kind: documentation
  registered_at: '2026-10-18'
  revision: PyTorch 2.6 documentation；curl 字节级取回 2026-10-18，SHA-256 792703d16102b45ceaebd07ef3d070fd1398af5c32df147085bb4d12bc4f8283
  license:
    status: partial
    scopes:
    - scope: PyTorch v2.6.0 仓库随附文档
      identifier: BSD-3-Clause
      url: https://github.com/pytorch/pytorch/blob/v2.6.0/LICENSE
    notes: 沿用既有 PyTorch 条目许可口径；仅链接并原创归纳。
  notes: Batch 24（T06-02）取证：reverse AD 与 DAG 历史记录、no-grad/inference mode 局部禁用；retain_graph 语义限于同一计算图再次求导且需要其中间量：在会释放这些中间量的先前 backward 调用中保留；已释放后无法追溯恢复、只能重新 forward；常规新迭代的 forward 产生新图不受此要求；线程安全边界。未运行代码。
- id: src.pytorch.optim-docs-2.6
  title: PyTorch 2.6 torch.optim 文档
  url: https://docs.pytorch.org/docs/2.6/optim.html
  kind: documentation
  registered_at: '2026-10-18'
  revision: PyTorch 2.6 documentation；curl 字节级取回 2026-10-18，SHA-256 53351ea89339ffb9913c675bc5fe946fee1b04f12b042ba8544a12ae6d9a2db9
  license:
    status: partial
    scopes:
    - scope: PyTorch v2.6.0 仓库随附文档
      identifier: BSD-3-Clause
      url: https://github.com/pytorch/pytorch/blob/v2.6.0/LICENSE
    notes: 沿用既有 PyTorch 条目许可口径；仅链接并原创归纳。
  notes: Batch 24（T06-02）取证：optimizer 构造（参数可迭代/named_parameters、param groups 逐组超参）与"持有当前 state、按梯度更新参数"职责。state_dict 语义由既有 parallel-training-state-2.6 覆盖。未运行代码。
- id: src.ascend.mindspeed-llm-training-interface-v2.2.0
  title: MindSpeed-LLM v2.2.0 训练入口、参数校验与依赖配套（README/install_guide/training 源码）
  url: https://github.com/Ascend/MindSpeed-LLM/blob/v2.2.0/mindspeed_llm/training/training.py
  kind: repository
  registered_at: '2026-10-18'
  revision: tag v2.2.0；codeload 源码包取回 2026-10-18（training.py SHA-256 341c0792484b7113fb71716eda66c9f4715e106d370b34e80c6a5201f905b2b8、arguments.py fd64204269ad1749159d9b98f47c91f92cb17de5075cb92670f8ab1d5df42a38、README 7b4893c93e8884d18eb0ff5eee5291bd93eced52dd91572d6a2566c4a7b12f99、install_guide 8dd60a6cc0983ffcf1e1aaa84da2cba054d1362a7b53a6bffacd665c0bdad423）
  license:
    status: identified
    scopes:
    - scope: 固定 tag 的 README、install_guide 与 mindspeed_llm/training 源码；根 LICENSE 声明范围
      identifier: BSD-3-Clause
      url: https://github.com/Ascend/MindSpeed-LLM/blob/v2.2.0/LICENSE
    notes: 根 LICENSE 列出若干第三方文件其他许可；仅链接并原创归纳。
  notes: Batch 24（T06-02）取证：pretrain() 四步职责链（initialize Megatron→setup→数据→train）、build_train_args/train 与 wrapper 族；arguments.py extra_args_provider_decorator、_validate_cp_args（进入条件与 L37 同：位于 ulysses/mamba/hybrid 各 CP 分支、要求 --use-mcore-models；num_attention_heads 须能被 ulysses_size×TP 整除且商 ≥1；GQA 分支（开启且 G≥1 时进入）串联除法：G % TP == 0 且商 ≥1，未启用 kv-head-repeat 时该商还须能被 ulysses_size 整除且商 ≥1——即 G 能被 TP×ulysses 整除；开关绕过第二层，代价是通信与内存）、_validate_instruction_finetune/_validate_train_mode_conflict；README 依赖表（PyTorch 2.7.1、NPU 组件在研）与 install_guide 固定 MindSpeed 2.2.0_core_r0.12.1＋Megatron-LM core_v0.12.1。未运行任何代码；MindSpeed core 仓本体未取回。
```

## 修订轮补充取证与更正（2026-10-18，初审发现 B24-T062-C01–C09 处理）

- **C01 更正**：首轮"core tag 无 --tensor-model-parallel-size 等 CLI 定义"不成立。补开同 tag `megatron/training/argument_utils.py`（SHA-256 4abf3e5e5571c5aa025dd8f716f483c6984fa7dbcf89931574d79fed728dc130）：L96–107 把 dataclass 字段名转 `--kebab-case` 旗标、L214–229 `build_group` 遍历字段逐个 `add_argument`；TransformerConfig 继承 ModelParallelConfig（含 tp 字段）构成参数生成链（审阅者 U18/U19）。CLI 解析未运行。
- **C06 补证**：同 tag `tests/unit_tests/pipeline_parallel/test_schedules.py`（SHA-256 5854bac1a671281796bc1bf4329f1bcbf3331d327380132d9f66e4299bae660f）L47–76 `test_get_forward_backward_func` 三类调度选择断言；只读未运行。
- **C07 更正**：MindSpeed `_validate_cp_args` 整除方向已在本文与 registry 统一为"被整除"取模表述（见上表修订）。
- **C04**：AMD 执行差异落实为 HIP notes 的具体小节（Reuse the CUDA Interfaces/Checking for HIP/TF32/分布式后端限制）；ROCm 7.1.1 兼容页按独立版本线引用。
- 其余（C02/C03/C05/C08/C09）为正文表述与方法设计修订，无新增上游材料；正文哈希随修订变化，见 git 记录。

## 修订轮二补充（2026-10-18，复核轮发现处理）

- C05：恢复设计选定完整 optimizer step 截取边界（显式引用并行页两节）；恢复分支恢复截点 RNG 状态（非同 seed 重放）；观测项含跳步计数与参数组成员对照。
- C06：补 PyTorch 官方测试（新登记 src.pytorch.official-tests-v2.6.0：test_optim/test_autograd/test/dynamo/test_compile 三文件与具名测试，SHAs 见登记）；Megatron test_schedules 补环境前提（CUDA＋NCCL 真实初始化、只验证调度选择）。
- C07：GQA 约束改为串联除法表述（G/T 再除 U，商 ≥1；等价于 G 能被 T×U 整除），取证与 registry 同步。
- C08：retain_graph 时序改为"在会释放中间量的先前 backward 中保留；已释放无法追溯"；取证摘要同步。

## 修订轮三补充（2026-10-19）

- C06：PyTorch 测试补具名断言与适用条件（test_state_dict_deterministic L1403–1439、onlyCUDA 限定 L1646/L1697–1717、test_backward L2270–2280、test_backward_badcalls L1608–1611、test_compilation L25–32、test_dynamo_signatures L163–173）；正文覆盖状态同步为"部分映射完成"。
- C07：取证/registry 摘要补进入条件（use-mcore-models、CP 分支）、两次正商与开关层级。
- C08：取证 L34 与正文 L120 同步 retain_graph 完整定义。
- R01：编译样板明确选定"仅 compile(model)"，含 optimizer 的编译变体列为范围外；表格相应行更新。

## 修订轮四补充（2026-10-19，复核第三轮发现处理）

- C07：取证建议登记副本同步进入条件（CP 分支＋use-mcore-models）；S3-01/02/03：重编译判据改按 guard 原因、测试类归属更正为 InPlaceCompilationTests.test_compilation、optimizer 示例链接改 troubleshooting 两节。
