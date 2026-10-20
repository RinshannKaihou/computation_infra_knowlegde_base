# 第二十六批 T06-08 来源记录

任务：T06-08（核验恢复状态与弹性训练的 v1 边界；**revise** concept，目标 `knowledge/06-training/checkpoint-state-consistency.md` 与 `knowledge/06-training/elastic-training-and-membership.md`，主题 06.1/06.7/06.8）。取证轮次：主会话作者角色首轮（2026-10-20，Batch 25 尚未收尾期间的并行来源准备轮）。

执行边界：仅来源准备（固定 tag/commit 的 codeload 源码包、官方文档页取回），未运行任何恢复/弹性/保存命令；**未修改 `sources/registry.yaml`、正文、领域索引与主计划**（Batch 25 占用串行集成资源，NEW 登记号待集成轮统一处理）。本记录不构成 T06-08 交付完成。（集成轮于同日完成登记，见文末。）

版本选择口径：MindSpeed-LLM 复用既有登记线 **v2.2.0（commit `53f3639c`）**；其外部 Megatron 依赖由 `docs/pytorch/install_guide.md` 明确为 **Megatron-LM `core_v0.12.1` tag**（另需 MindSpeed 仓 `2.2.0_core_r0.12.1` 分支，本轮未取证该仓本体）。MindIO TTP 约束页属 **MindX DL 6.0.0** 文档线；taskd 下载页属 **MindCluster 71RC1** 线；两者为 HA 文档外链锚定的外部组件文档，与 MindSpeed-LLM v2.2.0 的配套关系不互推。PyTorch 侧复用 **2.6 文档/源码线（commit `1eba9b3a`）**，wheel 边界取自 pytorch.org 官方历史版本页（ROCm 6.1 / 6.2.4）。注意整包哈希口径（审阅修订，T06-08-C05）：本轮 MindSpeed-LLM 整包 `c6db8136f3163c59` 与 Batch 25 记录的 `693f619a8b608726` 不同，原因是两次取回使用了**同一 commit 的不同归档命名**（tag 名归档顶层目录为 `MindSpeed-LLM-2.2.0/`，commit 名归档为 `MindSpeed-LLM-53f3639c…/`；去除顶层目录后 1903 个成员的路径、内容哈希与成员元数据完全一致，PAX 全局注释指向同一 commit）——不是"跨次下载 gzip 不稳定"；文件级哈希（如 `mindspeed_llm/training/training.py` 本轮 `341c0792484b7113`，与 Batch 24 登记 `341c0792…` 一致）是跨轮次的稳定内容锚。Megatron 整包同此口径（tag 名归档）。

## 本轮取回清单（2026-10-20）

| 对象 | 版本/ref | SHA-256（前 16 位） |
|---|---|---|
| MindSpeed-LLM codeload 源码包 | v2.2.0（53f3639c） | c6db8136f3163c59（整包；与 Batch 25 记录不同的原因是 tag 名/commit 名两种归档命名，非下载不稳定，见版本口径） |
| docs/pytorch/features/high_availability.md | 同上 | 83b6b6d8e3590f0e |
| docs/pytorch/install_guide.md | 同上 | 8dd60a6cc0983ffc |
| README.md（依赖配套表） | 同上 | 7b4893c93e8884d1 |
| mindspeed_llm/training/checkpointing.py | 同上 | beaa6057ac72f74f |
| mindspeed_llm/features_manager/high_availability/initialize_patch.py | 同上 | 5051c2494f1022c7 |
| mindspeed_llm/features_manager/high_availability/high_availability.py | 同上 | a9be983cd7e61a00 |
| pretrain_gpt.py | 同上 | b3ca649a9f11868d |
| mindspeed_llm/training/training.py（锚定复核） | 同上 | 341c0792484b7113 |
| Megatron-LM codeload 源码包 | core_v0.12.1 tag | 3e83d4a79014d77c（整包，同上口径） |
| megatron/training/checkpointing.py | 同上 | 713fc0fcb172b710 |
| megatron/core/dist_checkpointing/serialization.py | 同上 | b535efb72229fbf3 |
| PyTorch 2.6 DCP 文档页 | docs/2.6 线 | c22d13339435adad |
| MindIO TTP 约束限制页（MindX DL 6.0.0） | 渲染取回 2026-10-20 | 无字节快照（hiascend JS 页，见 unknown #2） |
| mindio_ttp whl 下载页（MindIO ACP 009） | — | 取回失败（两次服务端 500，见 unknown #1） |

## 主张—来源定位表

| 主张 | 登记 ID | 精确位置 | 支持范围 / 未覆盖 |
|---|---|---|---|
| HA 开关与环境变量语义：`--enable-high-availability`（TTP 临终遗言，要求全局≥1 份完整优化器数据）、`--enable-hbmfault-repair`（要求≥1 副本卡）、`--enable-worker-reboot`（空中加油，重启故障节点）、`--distributed-optimizer-no-replica`（改用 CKPT 文件修复）、`--enable-elastic-training`（剔除故障卡所在 DP 域节点）；`HIGH_AVAILABILITY=dump/retry/recover/elastic-training` 环境变量优先于 args | 复用 src.ascend.mindspeed-llm-ha-v2.2.0（本轮取回同文件复核） | high_availability.md 使用说明节（L48–71） | 开关语义；副本优化器内存公式表（fp16/bf16 param, fp32 grads 等）在文档前部，本轮未逐行重摘（撰写时复核） |
| 使用约束：DP size>1；MoE 需稠密层与稀疏层 DP 均>1；长序列需 dp_cp_size>1。弹性四条专属约束：仅支持 enable-high-availability＋use-distributed-optimizer；不支持 use-custom-fsdp、reuse-fp32-param；仅支持 DP/TP/PP；缩容后不可再次缩容，扩容仅支持直接扩回原有规模 | 复用 src.ascend.mindspeed-llm-ha-v2.2.0 | high_availability.md 使用约束节（L73–87） | 文档口径约束；未实测验证 |
| mindio_ttp/taskd 制品依赖与渠道：弹性训练依赖两个 whl（mindio_ttp、taskd），下载页分别在 MindX DL 6.0.0 文档与 MindCluster 71RC1 文档 | 复用 src.ascend.mindspeed-llm-ha-v2.2.0 | high_availability.md L41–45（外链） | 渠道声明；whl 本体未取得（unknown #1） |
| MindIO TTP（TFT）外部约束：仅 A+K 组合硬件；Atlas 800（9000）不支持 MindIO UCE/ARF；仅支持 ZeRO-1 且总体要求 DP Size 为偶数，副本数为 2 时要求 DP Size>1、其他副本数要求 DP Size 能被副本数整除；开启 MoE 前稠密层 DP>1、开启后稠密层与稀疏层 DP 均>1；副本优化器以算代传实现；增加片上内存总量（GB）＝模型参数量 N（B＝十亿）×12×副本数（全局总量，OOM 按官方口径扩容）；Controller 主备（1 活跃+2 备份）、切换与临终保存需健康卡数>world_size/2；副本不完整或分片校验（长时修改、分片间 iteration 不一致）失败则临终 checkpoint 不生成；TTP 不使用 ACP 异步保存、直接写持久化存储、临终保存后结束训练进程；不支持级联故障（保存中再故障即失败）；ARF 需≥2 节点、不支持 Controller 所在节点故障与级联故障，ARF 失败由 MindCluster 接管 | NEW src.ascend.mindio-ttp-constraints-mindxdl-600 | hiascend MindX DL 6.0.0「MindIO TFT 约束限制」页（全文，2026-10-20 两次渲染取回一致） | 外部组件恢复约束的官方文档口径；**渲染取回无字节快照**；与既有 src.ascend.mindio-acp-v26.1.1（ACP 线）的边界：TTP 明确不走 ACP 异步保存 |
| MindSpeed→Megatron 状态委托链：`save_checkpoint_wrapper` 内经 `generate_state_dict` 组装状态（import 自 `megatron.training.checkpointing`），`dist_checkpointing.save`＋`get_default_save_sharded_strategy`/`fully_parallel` 策略落盘；tracker finalize 位置沿用 | NEW src.ascend.mindspeed-llm-checkpointing-v2.2.0（或并入既有 checkpoint-v2.2.0 条目，集成角色定） | mindspeed_llm/training/checkpointing.py（import L21–33；save_checkpoint_wrapper L145–285，generate_state_dict 调用 L210、dist_checkpointing.save L236） | wrapper 调用链；异步格式限制与 optimizer sharding 选项已在既有 checkpoint-v2.2.0 notes |
| Megatron core_v0.12.1 状态生成：`generate_state_dict`（args、checkpoint_version 3.0、iteration；`ckpt_format=="torch_dist"`→`sharded_state_dict()` 否则 `state_dict_for_save_checkpoint()`；optimizer 分支同规则；opt_param_scheduler、rerun_state_machine、rng_state） | NEW src.nvidia.megatron-checkpointing-core-v0.12.1 | megatron/training/checkpointing.py L649–703 | 状态组装责任面；`use_dist_ckpt` 参数已声明 deprecated |
| Megatron core_v0.12.1 加载边界：`_load_base_checkpoint` 按序判定——显式 `ckpt_step` 先行提供 iteration；其次存在非持久 checkpoint 且其 iteration 不小于当前有效 iteration 时直接采用（否则告警）；均未命中且无 tracker 文件才进入缺 checkpoint 分支（告警＋随机初始化，或 `--exit-on-missing-checkpoint` 退出）；`find_checkpoint_rank_0`/`read_metadata` 辅助 | NEW src.nvidia.megatron-checkpointing-core-v0.12.1 | megatron/training/checkpointing.py L162/L227/L878–935（显式 step L906–907、非持久分支 L909–918、缺 checkpoint 分支 L924 起）；数据计数恢复 L1357–1370 | 加载入口与决策边界；完整 load_checkpoint（load_state_dict 时机、验证分支）本轮仅入口级（unknown #4） |
| ckpt_format 三值 torch/torch_dist/torch_dcp 与 serialization 职责 | NEW src.nvidia.megatron-checkpointing-core-v0.12.1 | generate_state_dict 分支注释；megatron/core/dist_checkpointing/serialization.py（本轮哈希钉扎，正文撰写再读） | 分派存在性；torch_dcp 写出目录与 PyTorch DCP 原生布局兼容性未核（unknown #6） |
| mindio_ttp/taskd 仓库内接口面：`from mindio_ttp.adaptor import tft_init_controller_processor, ttp_initialize_replica_dp_group / tft_is_arf_reboot_node`；`from taskd.python.adaptor.elastic_training import common`；后训练 base_trainer 缺包即 `sys.exit("The mindio_ttp package is not installed. Exiting.")` | NEW src.ascend.mindspeed-llm-ha-code-v2.2.0（文件切面：initialize_patch.py L26/L48、pretrain_gpt.py L200、base_trainer.py L204–206） | — | 调用面与缺包行为；adaptor 实现在外部 whl（unknown #1） |
| DCP 设备无关口径：async_save 先将 state_dict 去暂存（默认 CPU 内存）再后台线程保存，标注 experimental；DCP 文档无任何 ROCm/CUDA 专属支持声明（导航中 HIP semantics 为独立页） | 复用/补强 src.pytorch.dcp-2.6 | docs.pytorch.org/docs/2.6/distributed.checkpoint.html（async_save 说明与 Warning） | 文档口径；不构成 ROCm 实测声明 |
| PyTorch 2.6.0 wheel 边界：ROCm 6.1 与 ROCm 6.2.4（均仅 Linux），索引 `https://download.pytorch.org/whl/rocm6.1`、`…/rocm6.2.4`；另有 CUDA 11.8/12.4/12.6 与 CPU 构建 | NEW src.pytorch.wheel-matrix-2.6.0 | pytorch.org get-started/previous-versions（2.6.0 节，渲染取回） | 发行面版本边界；不证明 DCP 在 ROCm 的行为（unknown #5） |
| torchrun/elastic 恢复契约（checkpoint 为恢复前提、max-restarts、rendezvous） | 复用 src.pytorch.elastic-2.6 | （既有） | 本轮未重开 |

## unknown 清单

1. mindio_ttp/taskd whl 制品本体未获取：下载页（mindioacp009）两次服务端 500；whl 的版本矩阵、adaptor 接口实现、与 CANN/驱动的配套 unknown。仓库内仅调用面。
2. MindIO TTP 约束页为渲染取回（hiascend JS 页面），无字节快照与 SHA；2026-10-20 审阅修订轮已第二次渲染取回并逐条复核对齐（两次一致）。MindX DL 6.0.0 文档线与 MindSpeed-LLM v2.2.0 的正式配套矩阵未从产品文档证实，仅 HA 文档外链锚定。审阅者另打开同产品线《故障恢复加速》PDF 作为补充证据（量纲与 HTML 一致）；作者按其 URL 直下仅得 2 页文档、与审阅分页不符，未登记，不作为来源。
3. MindSpeed 仓（`2.2.0_core_r0.12.1` 分支）本体未取证；install_guide 声明的安装链未逐项核对（在研版本驱动/固件/Toolkit/NNAL、PyTorch 2.7.1、transformers 4.43.2＋模型例外 4.51.0/4.54.0）。
4. Megatron `load_checkpoint` 完整流（state_dict 装载时机、iteration 校验、非连续步骤行为）与 serialization.py 的 load 路径仅入口级；正文撰写轮需再读。
5. DCP×ROCm：官方无 DCP×平台支持矩阵；wheel 存在性（ROCm 6.1/6.2.4）不构成 DCP 行为声明；ROCm 构建下进程组后端映射（NCCL/RCCL/Gloo）未取证。技术保证仅到"DCP 默认路径基于进程组＋文件系统后端、async_save 暂存 CPU"层面。
6. Megatron `torch_dcp` 格式的落盘布局与 PyTorch DCP 原生 `torch.distributed.checkpoint` 目录的互相可读性未逐文件核对。
7. `high_availability.py` validate_args 断言（mindio_ttp/taskd 导入检查、use_dist_ckpt/swap_optimizer/EP/CP 断言）复用 Batch 17 登记记录，本轮仅哈希复核未重读全文；正文撰写时复核。
8. 未运行任何命令；全部为文档/源码口径，无本库实测结果。

## 集成轮结果（2026-10-20 已执行）

- 新登记 3 项：src.ascend.mindio-ttp-constraints-mindxdl-600（hiascend 文档，许可 unknown 按 hiascend 先例）、src.nvidia.megatron-checkpointing-core-v0.12.1（LICENSE 直核为 NVIDIA BSD-3-Clause）、src.pytorch.wheel-matrix-2.6.0（站点许可未确立，仅链接与归纳）。
- 并入既有条目 2 项：mindspeed-llm-checkpointing 切面并入 src.ascend.mindspeed-llm-checkpoint-v2.2.0 的 notes（同一文件 checkpointing.py，补 import 链与 install_guide 的 Megatron core_v0.12.1 钉扎）；initialize_patch.py/pretrain_gpt.py 代码切面并入 src.ascend.mindspeed-llm-ha-v2.2.0 的 notes。
- T06-08 修订轮启动；两篇目标正文保持稳定 ID。
