---
id: software-stack.ascend-op-graph-failure-triage
title: 昇腾算子不支持与图编译失败诊断指南
type: procedure
domain: software-stack
status: draft
platforms: [ascend]
source_refs:
  - src.ascend.torch-npu-v7.2.0-pytorch2.6.0
  - src.pytorch.dispatcher-v2.6.0
  - src.huawei.cann-82rc1-aclerror
  - src.ascend.vllm-ascend-v0-14-0rc1
updated_at: "2026-10-08"
summary: 把“算子不支持”和“图编译失败”按层分开：框架 dispatch 与 CPU fallback、算子实现/编译层的 CANN 错误码、图模式层的捕获与显式 eager 对照；以 TorchNPU 固定快照为证据样板。
related_ids:
  - software-stack.layers-and-boundaries
  - software-stack.ascend-documented-profile
  - software-stack.ascend-version-mismatch-triage
  - software-stack.ascend-memory-oom-evidence
  - reliability.evidence-and-hypotheses
applicability:
  environment_refs: []
  notes: "流程以 TorchNPU v7.2.0-pytorch2.6.0 固定 commit 与 PyTorch v2.6.0 固定源码为证据样板；目标环境的 torch_npu/CANN/框架组合需另行固定，CANN 侧图编译排障的版本化文档未取得，标为缺口。"
verification:
  status: source_checked
  evidence_refs:
    - src.ascend.torch-npu-v7.2.0-pytorch2.6.0
    - src.pytorch.dispatcher-v2.6.0
    - src.ascend.vllm-ascend-v0-14-0rc1
  notes: "已核对 dispatcher 报错实现、VariableFallbackKernel.cpp 全文中的 PrivateUse1 CPU fallback、autograd/sparse 分支与构建收集，以及插件指南的显式 eager 配置；图组件结构与日志变量读取点仅覆盖所列范围，未在 NPU 环境执行任何算子或图编译。"
---

# 昇腾算子不支持与图编译失败诊断指南

## 目标与触发条件

触发信号：训练/推理启动或运行中报 “could not run … PrivateUse1”、“not implemented/not support”、GE/ACL 错误码，出现 NPU 算子回退 CPU 的告警/性能异常，或图模式（torch.compile/aclgraph/NPU Graph）启用后失败。目标是先确定失败发生在哪一层，再决定补什么证据。三层要分开：

1. **框架注册/dispatch 层**：区分后端实现缺失、CPU fallback 和该 dispatch 路径无法执行；
2. **算子实现/编译层**：算子有注册，但 CANN 侧编译或下发失败；
3. **图模式层**：图捕获/图编译失败，以及使用者显式切换 eager 的对照结果。

版本配套问题（库加载失败、ABI/符号错误）不在本文，见[昇腾版本配套诊断](ascend-version-mismatch-triage.md)；OOM 类失败见[昇腾 NPU 内存与 OOM 证据](ascend-memory-oom-evidence.md)。

## 适用范围与前置条件

证据样板：TorchNPU `v7.2.0-pytorch2.6.0`（commit `bc51ab84…`）与 PyTorch `v2.6.0`（commit `1eba9b3…`）。进入排查前固定：torch_npu/CANN/框架版本、模型与算子清单、执行模式（eager/图模式）、完整报错文本与日志级别配置。**已知缺口**：CANN 侧图编译/算子编译失败排障的版本化官方文档本轮未取得，涉及 GE 内部阶段的结论只能到错误码层面。

## 需要的证据

| 证据 | 采集范围或定位 | 用途 | 缺失时如何处理 |
|---|---|---|---|
| 完整报错文本与堆栈 | 报错首行、算子名、错误码、调用栈 | 分层判断 | 只有二手转述时不作层归属结论 |
| 版本与配置身份 | torch_npu/CANN/框架版本、图模式开关、环境变量 | 判断已知限制是否适用 | 版本未知时不执行版本特定处置 |
| 算子与执行路径 | 算子名、dispatch key、目标后端实现、CPU fallback 告警及同窗口 CPU/设备时间线 | 注册/回退支路 | 无告警不证明无回退；源码按算子名去重告警，实际执行路径仍需证据 |
| 日志级别 | torch_npu 读取 `ASCEND_GLOBAL_LOG_LEVEL`（[OptionsManager.cpp L229](https://github.com/Ascend/pytorch/blob/bc51ab84cc6f35c77aab1c59886e0ea43681a317/torch_npu/csrc/core/npu/register/OptionsManager.cpp#L229)）等环境变量 | 获得更完整日志 | 日志缺失时错误码是唯一线索 |

## 步骤与判断分支

| 步骤 | 检查或动作 | 运行影响 | 预期证据与解释 | 下一步 |
|---|---|---|---|---|
| 1 | 看报错形态分层。PyTorch dispatcher 的典型文本是“Could not run '\<op\>' with arguments from the 'PrivateUse1' backend…is only available for these backends: …”（固定 v2.6.0 的 [OperatorEntry.cpp L537–557](https://github.com/pytorch/pytorch/blob/1eba9b3aa3c43f86f4a2c807ac8e12c4a7767340/aten/src/ATen/core/dispatch/OperatorEntry.cpp#L537-L557)）；报错列出可用后端，说明该次 dispatch 未得到可执行处理，需继续核对 fallback，不能从缺少 NPU 专用 kernel 直接推出算子不可运行 | 只读 | dispatcher 报错或 CPU 回退告警 → 步骤 2；GE/ACL 错误码 → 步骤 3；图模式相关 → 步骤 4 | 按层分支 |
| 2 | 注册/回退支路：核对目标版本的算子实现与 dispatch key。固定 `VariableFallbackKernel.cpp` 为 `PrivateUse1` 注册全局 `npu_cpu_fallback`，调用 `at::native::cpu_fallback` 并提示 CPU 执行的性能影响；同文件 `AutogradPrivateUse1` 为独立 autograd fallback，`SparsePrivateUse1` 则直接报不支持（[L232–271](https://github.com/Ascend/pytorch/blob/bc51ab84cc6f35c77aab1c59886e0ea43681a317/torch_npu/csrc/aten/VariableFallbackKernel.cpp#L232-L271)，[CMake 收集该文件](https://github.com/Ascend/pytorch/blob/bc51ab84cc6f35c77aab1c59886e0ea43681a317/torch_npu/csrc/aten/CMakeLists.txt)）。具体算子回退能否成功仍取决于 CPU 实现和实际 dispatch 条件 | 只读 | CPU 回退告警提供执行路径线索，结合 CPU/设备时间线分析性能；仍报错时记录失败 backend、算子与调用栈；autograd fallback 不证明梯度实现正确 | 按实际路径选择 NPU 实现、替代算子或版本评估；不声称所有算子都能回退，也不从文件头推断无 CPU fallback |
| 3 | 实现/编译层支路：报错带 GE/ACL 错误码时，按固定快照 vendored 头文件与 CANN 错误码页核对语义（如 `ACL_ERROR_GE_DEVICE_MEMORY_ALLOCATION_FAILED`=245002、运行时内存 207001；头文件 [ge_error_codes.h L45](https://github.com/Ascend/pytorch/blob/bc51ab84cc6f35c77aab1c59886e0ea43681a317/third_party/acl/inc/ge/ge_error_codes.h#L45)、[rt_error_codes.h L43](https://github.com/Ascend/pytorch/blob/bc51ab84cc6f35c77aab1c59886e0ea43681a317/third_party/acl/inc/acl/error_codes/rt_error_codes.h#L43)；释义见 [CANN 错误码页](https://www.hiascend.com/document/detail/zh/CANNCommunityEdition/82RC1/API/appdevgapi/aclpythondevg_01_0911.html)）。错误码只给出失败类别；编译失败的内部阶段（shape 推导、tiling、编译）需要 CANN 侧日志，对应版本化排障文档本库未取得 | 读日志为主 | 错误码 + 算子名 + 触发 shape 构成最小证据 | 缺口处保持 `unknown`，不猜内部阶段 |
| 4 | 图模式支路：先确认启用了哪条图路径。固定快照含 vendored torchair 构建脚本（`third_party/torchair/install.sh`）、NPU 图捕获（`csrc/core/npu/NPUGraph.cpp`）与 torch.compile 相关 `_inductor/` 代码——**启用条件与配套关系本轮未核对**。推理侧插件指南说明 ACLGraph 默认启用；两种图模式均不能运行时，建议使用者显式设置 `enforce_eager=True` / `--enforce-eager` 做 eager 对照（[graph_mode.md L66–85](https://github.com/vllm-project/vllm-ascend/blob/52d4acfa51fb868823d1070b81cbd2d97e9e4696/docs/source/user_guide/feature_guide/graph_mode.md#L66-L85)），没有据此确认引擎会自动捕获失败并重试。graph capture 失败还可能是 stream 资源耗尽而非显存 OOM（FAQ 18） | 显式切换图/eager 属配置变更，按已有授权和窗口执行，记录配置并安排恢复 | 同版本/输入下显式 eager 正常 → 图路径为候选；eager 同样失败 → 回步骤 1–3；对照不单独证明图失败的内部原因 | 保留模式、捕获 size、触发输入与对照结果 |
| 5 | 汇总：层、算子、版本、报错文本、触发输入 | 无 | 结论回链到层与证据 | 满足完成判据后结束 |

## 停止条件与恢复安排

- 不在生产环境直接切换图模式或升级算子包试运气；版本与模式变更需授权与回滚计划。
- 提高日志级别会改变日志量与少量性能，验证后恢复。
- 报错涉及具体业务算子时，保存触发输入 shape/dtype 与最小复现脚本，而不是只保存报错截图。

## 完成判据

以下任一结果可以结束本轮诊断：

1. 失败被定位到具体一层（注册/实现编译/图模式），报错文本、算子名与版本证据一致；
2. 注册/回退结论有目标版本的 dispatch 注册、fallback 与实际报错/执行路径证据支持，CPU 性能与梯度正确性分别验证；
3. 实现/编译层结论到错误码与触发条件为止，CANN 内部阶段明确标为缺口；
4. 证据不足，但已记录缺失的版本、日志或文档证据，结论保持 `unknown`。

“换个版本能跑”不单独满足完成判据：需要说明换的是哪一层、为什么。

## 来源与验证记录

- [TorchNPU v7.2.0-pytorch2.6.0 固定快照](https://github.com/Ascend/pytorch/tree/bc51ab84cc6f35c77aab1c59886e0ea43681a317)：csrc/aten 结构、codegen 注册、VariableFallbackKernel 性质、torchair/NPUGraph/_inductor 存在性、OptionsManager 环境变量读取点。
- [PyTorch v2.6.0 OperatorEntry.cpp](https://github.com/pytorch/pytorch/blob/1eba9b3aa3c43f86f4a2c807ac8e12c4a7767340/aten/src/ATen/core/dispatch/OperatorEntry.cpp)：dispatcher 两种 NotImplemented 报错形态。
- [CANN 错误码页（URL 82RC1）](https://www.hiascend.com/document/detail/zh/CANNCommunityEdition/82RC1/API/appdevgapi/aclpythondevg_01_0911.html)与固定快照 vendored 错误码头文件。
- [vLLM Ascend v0.14.0rc1 graph_mode.md](https://github.com/vllm-project/vllm-ascend/blob/52d4acfa51fb868823d1070b81cbd2d97e9e4696/docs/source/user_guide/feature_guide/graph_mode.md#L66-L85)与既有 FAQ 18 记录：推理侧显式 eager 对照建议，不能外推训练图模式或引擎自动重试行为。
- 逐条主张与证据定位见[第十一批算子/图编译来源记录](../../docs/research/batch-11-op-graph-sources.md)。
- 当前验证范围：来源核对；未在 NPU 环境执行算子或图编译。
- 待确认：CANN 图编译/算子编译失败排障的版本化文档；torchair/NPUGraph/_inductor 的启用条件与配套；目标 torch_npu 版本的算子支持矩阵。
