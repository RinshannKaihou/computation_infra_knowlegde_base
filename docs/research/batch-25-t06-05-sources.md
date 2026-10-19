# 第二十五批 T06-05 来源记录

任务：T06-05（混合精度、算子适配与收敛验证；**new** procedure `knowledge/06-training/mixed-precision-and-convergence.md`，主题 06.5）。取证轮次：主会话作者角色首轮（2026-10-20）。PyTorch 侧固定 v2.6.0（commit 1eba9b3，沿用既有登记线）；Megatron 固定 core_v0.19.2（codeload 包与 Batch 24 登记同 SHA）；案例链经 gh API 观察。未运行任何精度实验。

版本选择口径：三组档案分立——PyTorch 2.6 AMP（文档 src.pytorch.amp-2.6/amp-examples-2.6 既有＋本轮 GradScaler 源码/测试）、Megatron core_v0.19.2 loss scale 实现、TorchNPU 7.2.0 autocast（既有 src.ascend.torchnpu-amp-7.2.0/autocast-ops-7.2.0）；MindSpeed-LLM v2.2.0 示例的 --initial-loss-scale 65536 复用既有 src.ascend.mindspeed-llm-workflows-v2.2.0。AMD 侧复用 src.amd.pytorch-compatibility-7.1.1（AMP/已知问题）。

## 本轮取回清单（2026-10-20）

| 对象 | 版本 | SHA-256（前 16 位） |
|---|---|---|
| torch/amp/grad_scaler.py | v2.6.0 | eb4bc91fda9815ba |
| torch/cuda/amp/grad_scaler.py（shim） | v2.6.0 | 5931b704656fa388 |
| torch/distributed/fsdp/sharded_grad_scaler.py | v2.6.0 | a54ce5b209840eea |
| test/test_autocast.py | v2.6.0 | df95ba0c7746d4b2 |
| test/distributed/_composable/fsdp/test_fully_shard_grad_scaler.py | v2.6.0 | f5e034a50e4c5e57 |
| Megatron codeload 包（core/optimizer） | core_v0.19.2 | 4c16ccc2a0d4c1b6（与登记一致） |
| megatron/core/optimizer/grad_scaler.py | core_v0.19.2 | 81402e800476fce9 |
| megatron/core/optimizer/optimizer.py | core_v0.19.2 | 24609822f7c165c9 |
| issue #200537 / PR #200697 / commit cbffccce | gh API 观察 | —（API 元数据） |

注：v2.6.0 无 test/test_cuda_amp.py（git tree 全量枚举确认，GradScaler 专项测试并入分布式套件）；torch/cuda/amp/grad_scaler.py 为 deprecated 转发 shim（38 行）。

## 主张—来源定位表

| 主张 | 登记 ID | 精确位置 | 支持范围 / 未覆盖 |
|---|---|---|---|
| GradScaler 语义与默认参数 | NEW src.pytorch.amp-grad-scaler-source-v2.6.0 | amp/grad_scaler.py L49+、L107–144：init_scale 2^16/growth 2.0/backoff 0.5/growth_interval 2000、断言 growth>1/backoff<1；L93–97（inf/NaN 时乘 backoff_factor 跳过 step、growth_interval 连续无 inf 乘 growth_factor） | 动态 loss scale 的完整实现语义；unscale_ 与 clip 顺序、多损失独立 scaler 见既有 src.pytorch.amp-examples-2.6 |
| torch.cuda.amp 命名弃用 | NEW src.pytorch.amp-grad-scaler-source-v2.6.0 | cuda shim 全文：deprecated FutureWarning、转发 torch.amp.GradScaler("cuda") | 与 src.pytorch.amp-2.6 的 torch.autocast(device_type=…) 弃用口径一致 |
| 分布式 loss scale（FSDP） | NEW src.pytorch.amp-grad-scaler-source-v2.6.0 | sharded_grad_scaler.py L42+：ShardedGradScaler(GradScaler)、_GeneralMultiDeviceReplicator、_refresh_per_optimizer_state | 分片梯度下 scaler 状态按 optimizer 分立；found_inf 跨 rank 的归约语义未逐行核（unknown，正文不写 collective 细节） |
| found_inf 可观测性（测试锚） | NEW src.pytorch.amp-tests-v2.6.0 | test_fully_shard_grad_scaler.py L77–80：断言 _per_optimizer_states[id(opt)]["found_inf_per_device"] 与注入 has_inf 一致 | 官方测试把 found_inf 当公开可断言状态；测试通过标准属其套件非本库阈值 |
| autocast 行为测试锚 | NEW src.pytorch.amp-tests-v2.6.0 | test_autocast.py：TestAutocastCPU/GPU/MPS/TorchAutocast 类 | autocast 算子归属有官方测试；逐算子清单以 src.pytorch.amp-2.6 的三类 op 表为准 |
| Megatron loss scale 双模式 | NEW src.nvidia.megatron-grad-scaler-core-v0.19.2 | grad_scaler.py：MegatronGradScaler L11（ABC）、ConstantGradScaler L43、DynamicGradScaler L61+（min_scale/growth_factor/backoff_factor/growth_interval/hysteresis 参数 L87–103） | 常数/动态两种策略独立于 PyTorch GradScaler 实现；DynamicGradScaler 含 hysteresis（连续 N 次 NaN 才回退）与 min_scale 下界，与 PyTorch 参数面不同 |
| fp16 优化器与 master 权重 | NEW src.nvidia.megatron-grad-scaler-core-v0.19.2 | optimizer.py：MixedPrecisionOptimizer L654、get_loss_scale L704、Float16OptimizerWithFloat16Params L964、FP32Optimizer.get_loss_scale 恒 1（L1259） | fp16 参数＋fp32 主权重的框架级实现；与 06.1 状态责任矩阵互链 |
| MindSpeed 初始 loss scale 65536 | 复用 src.ascend.mindspeed-llm-workflows-v2.2.0 | pretrain_llama2_7b_ptd.sh L65（--initial-loss-scale 65536） | Ascend 侧 Megatron 系脚本沿用 2^16 初始 scale 的实例 |
| TorchNPU autocast 边界 | 复用 src.ascend.torchnpu-amp-7.2.0＋src.ascend.torchnpu-autocast-ops-7.2.0 | （既有） | bf16 支持条件、逐算子 autocast 归属四族宏 |
| 精度诊断工具 | 复用 src.ascend.msprobe-training-guide-2026-09-30、src.pytorch.numerical-verification-2.6 | （既有） | 首差异定位与数值边界 |
| AMD 侧 AMP 条件 | 复用 src.amd.pytorch-compatibility-7.1.1 | Known issues：allow_fp16_reduced_precision_reduction 等不支持 | ROCm 侧 reduced precision 开关边界；混合精度总体支持以上游 PyTorch AMP 为准 |
| 算子适配案例（静默 dtype） | NEW src.pytorch.issue-200537 | issue 正文（复现脚本/三组对照/根因定位 AutocastRNN.cpp 硬编码 at::kHalf）；修复 commit cbffccce（get_autocast_dtype(at::kCUDA)）＋test/test_cuda.py；main 已核对 | autocast 算子包装器的 dtype 适配错误如何在训练中静默出现、如何用 dtype 对照与直接调用区分；ROCm miopen_rnn 对应修复未核对（unknown）；本库未复现 |

## unknown 清单

1. GradScaler 的 found_inf 在 DDP/NCCL 下的跨 rank 归约实现未逐行核对（正文只写"分布式训练各 rank 的 inf 判断须一致"的检查要求，不写实现细节）。
2. Megatron DynamicGradScaler 的 hysteresis 精确行为（连续次数语义）只取证到参数与 docstring，未运行验证。
3. 案例 #200537 的 ROCm 侧（miopen_rnn 硬编码 kHalf）修复状态未核对；修复进入哪个 release tag 未逐 tag 确认。
4. MindSpeed-LLM/TorchNPU 侧混合精度收敛窗口的官方对照数据无一手来源（验证方法正文给设计，不引数字）。
5. msprobe 的 dump/比对接口仅到既有登记范围；算子级精度比对流程未实测。
6. 全部源码已读未运行；容差/样本量等判据由正文给出设计而非实测阈值。

## 修订轮补充（2026-10-20，初审 B25-T05-C01–C09 后）

- **C01/C04（Megatron hysteresis 与 min_scale）**：registry `src.nvidia.megatron-grad-scaler-core-v0.19.2` notes 已更正——固定实现状态机为"非有限梯度递减计数、计数耗尽回退且退避不重置计数"；min_scale 只截断 scale、跳步按 found_inf_flag 决定（optimizer.py L755–774/L815–822，审阅轮定位）。正文机制速览与停止条件已改。
- **C02（GradScaler 时序）**：registry `src.pytorch.amp-grad-scaler-source-v2.6.0` notes 已更正为 scale→backward→unscale_→scaler.step（普通/融合路径区别）→update 的职责分立；"跳过更新"按实际参数/状态变化观测。
- **C03（found_inf 私有状态）**：registry `src.pytorch.amp-tests-v2.6.0` notes 已收窄（内部状态非公开 API、采集时点 unscale 后 update 前、测试限 CUDA/FSDP2/≥4GPU/skipIfRocm）。
- **C05（ROCm 版本限定）**：正文已把已知不支持项限定到其原页"PyTorch 2.7/2.8＋ROCm 7.0/7.1"节内两个完整字段（`torch.backends.cuda.matmul.allow_fp16_reduced_precision_reduction`、`allow_bf16_reduced_precision_reduction`），并与 PyTorch 2.6 机制样板分立；其余组合 unknown。
- **C06（案例分层）**：正文案例锚已改为三分层（报告者自述 nightly 2.16.0.dev20261010+cu130/RTX 3090/cuDNN 9.26；修复与测试设计限 BF16 硬件/cuDNN≥9.13/跳过 ROCm；本库未复现），删除"必在收敛曲线现形"外推；步骤 2 改"定位配置/实现/支持条件"。
- **C07/C08（判据闭环）**：每配置独立重复 R 次与计步口径（尝试步 vs 实际成功更新）分列；固定验证集质量检查为所有通过结论必经；任务质量阈值与统计分辨阈分列，不确定性不支持判定时补采或 unknown。
- **C09（回链）**：gpu-npu-precision-difference-triage.md（完成判据节＋related_ids）与 dtype-layout-and-precision-semantics.md（边界段）已补 training.mixed-precision-and-convergence 回链。

## 第三轮修订（2026-10-20，复核轮二 C01/C07/R01 后）

- **C01**：Megatron DynamicGradScaler 补完整状态机（初始值、非有限分支、finite 未满窗口不复位、唯一复位分支＝完整 growth_interval 窗口）＋三类静态序列示例（真,假,真/真,真,真/真,真,假,假,假,真，源码推演非运行结果）；registry notes 同步补全。
- **C07**：完成判据"重复与样本量"扩为可执行判读契约——窗口对齐轴三选一预注册（effective-batch 尝试/样本 token/成功更新）、跳步时 scheduler 与数据游标推进策略预注册并记录实际推进量、R 次结果的汇总量与不确定性表示及通过/失败/unknown 规则预注册。
- **R01**：跳步判据更正——不能按参数数值变化判定（合法零增量反例：v2.6.0 SGD 全零梯度分支）；改为按 optimizer 分层计数（尝试/因非有限抑制/进入未抑制更新分支），参数增量独立记录、零增量保留多解释；registry GradScaler 条目 notes 同步更正。

## 第四轮修订（2026-10-20，复核轮三 R01 后）

- **R01 剩余**：停止条件中的跳步率补统计契约——按 optimizer 分列；分子＝确认因非有限值被抑制次数、分母＝有效 batch 边界的 step 尝试数（排除 micro-step/成功更新数/可分类子集作分母）；未确认事件记账保留并报告上下界或保守 unknown（示例 1/10 确认＋1 未确认 → [1/10, 2/10]），不静默丢弃、不填作成功或跳步；分母为零的窗口不产出比率。
