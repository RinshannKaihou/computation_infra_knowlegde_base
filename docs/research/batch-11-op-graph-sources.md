# 第十一批来源记录：昇腾算子不支持与图编译失败（R2-10）

**2026-10-08 修订注记：** Codex `gpt-6.1-sol / xhigh` 按 B11-C01/C02 修正本记录并完成[定向复核](batch-10-11-12-codex-recheck.md)。下述原研究者、首次获取方式与当时任务状态为历史；修订补读和保留的未知条件见本记录及复核报告。

研究日期：2026-09-30（子代理首次尝试，因环境故障与两次超时未完成）至 2026-10-08（主任务直接定向取证）。目标正文：`knowledge/02-software-stack/ascend-op-graph-failure-triage.md`（procedure）。取证经 `gh api`（已认证）按固定 commit 原文件进行；未运行任何 NPU 代码。

## 主张—证据表

| 主张 | 证据位置 | 版本 | 类型 | 反证/未知 |
|---|---|---|---|---|
| PyTorch 核心 dispatcher 在该次 dispatch 无可执行处理时给出 Could not run / 可用后端列表；无 tensor 参数且缺 fallback 时为另一种报错文本 | pytorch v2.6.0（1eba9b3）aten/src/ATen/core/dispatch/OperatorEntry.cpp L537–557 | PyTorch 2.6 | 固定源码 | 缺少 NPU 专用 kernel 不等于不可运行；还需核对全局 fallback、实际失败 backend 与 CPU 实现，不代表算子或梯度正确性 |
| torch_npu 的算子注册由 codegen 生成：仓库含 codegen/ 目录与模板（codegen/templates/CustomRegisterSchema.cpp、CustomFunctions.cpp 等）；自定义算子经 custom_functions 路径 | Ascend/pytorch bc51ab84 文件树（codegen/、test/custom_ops/） | TorchNPU v7.2.0-pytorch2.6.0 | 固定源码（结构） | 具体生成流程未深入 |
| VariableFallbackKernel.cpp 同时注册三种 fallback：AutogradPrivateUse1 的 autograd 分支；PrivateUse1 的 npu_cpu_fallback 调 at::native::cpu_fallback，并按算子名去重提示性能影响；SparsePrivateUse1 分支直接报不支持。aten/CMakeLists.txt 的 cpp glob 包含该文件且排除清单没有它 | [固定文件 L232–271](https://github.com/Ascend/pytorch/blob/bc51ab84cc6f35c77aab1c59886e0ea43681a317/torch_npu/csrc/aten/VariableFallbackKernel.cpp#L232-L271)、[CMakeLists.txt](https://github.com/Ascend/pytorch/blob/bc51ab84cc6f35c77aab1c59886e0ea43681a317/torch_npu/csrc/aten/CMakeLists.txt) | 同上 | 固定源码全文 | 修正 B11-C01：文件头只讨论 autograd，不能代表整个文件；具体算子回退成功、性能和梯度正确性均需另证 |
| 图模式相关组件的存在性：third_party/torchair（vendored，install.sh 调 torchair/build_and_install.sh）；csrc/core/npu/NPUGraph.cpp/NPUGraphsUtils.cpp（NPU 图捕获）；torch_npu/_inductor/（fx_passes、npu_fusion_attention_graph 等 torch.compile 相关）；csrc/framework/aoe/AoeDumpGraphManager（AOE dump 图管理） | 文件树 + third_party/torchair/install.sh 前 30 行 | 同上 | 固定源码（存在性） | 各组件的启用条件、与 CANN 版本的配套未核对 |
| OptionsManager.cpp 的环境变量读取点：ASCEND_GLOBAL_LOG_LEVEL（L229）、TORCH_NPU_DISABLED_WARNING（L584）、HCCL_CONNECT/EXEC/EVENT_TIMEOUT、ACL_STREAM_TIMEOUT、ACL_DEVICE_SYNC_TIMEOUT、TASK_QUEUE_ENABLE、NPU_ASD_ENABLE、OOM_SNAPSHOT_* 等 | torch_npu/csrc/core/npu/register/OptionsManager.cpp 各 getenv 行 | 同上 | 固定源码 | 各变量的取值语义需对应版本文档，本轮未逐一展开 |
| GE/算子编译类错误码来自 CANN 侧：vendored third_party/acl/inc/ge/ge_error_codes.h（如 245002 = ACL_ERROR_GE_DEVICE_MEMORY_ALLOCATION_FAILED，L45）与 acl/error_codes/rt_error_codes.h（207001，L43）；CANN aclError 错误码页（82RC1，页头版本未核验）给释义 | 固定快照 vendored 头文件；已登记 src.huawei.cann-82rc1-aclerror | 同上 + 版本化文档 | 源码（头文件） | 错误码含义以 CANN 文档为准；CANN 侧"算子编译失败"的版本化排障章节本轮未取得，标缺口 |
| vLLM Ascend 图模式指南说明 ACLGraph 默认启用；两种图模式不能运行时建议使用者显式配置 enforce_eager=True / --enforce-eager；FAQ 18 记录 stream 耗尽捕获失败 | src.ascend.vllm-ascend-v0-14-0rc1（52d4acfa），[graph_mode.md L66–85](https://github.com/vllm-project/vllm-ascend/blob/52d4acfa51fb868823d1070b81cbd2d97e9e4696/docs/source/user_guide/feature_guide/graph_mode.md#L66-L85) | v0.14.0rc1 | 文档建议与显式配置示例 | 修正 B11-C02：不证明引擎自动捕获失败并重试 eager，训练侧图模式不共享该结论 |

## 未解决与抓取失败

- 首次研究子代理因 OAuth 故障中断，恢复后两次 2 小时超时；改由主任务直接取证（本记录）。
- CANN 版本化的图编译/算子编译排障文档未取到（hiascend SPA 抓取受限），缺口保留。
- torchair、NPUGraph、_inductor 的启用条件与报错形态未深入；算子支持的版本化矩阵文档未定位。
- 固定源码已确认 PrivateUse1 全局 CPU fallback；尚未确认目标算子的实际 dispatch、CPU 回退成功条件、性能和梯度正确性，也未核对其他版本或配置开关。
