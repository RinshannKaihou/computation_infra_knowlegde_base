# 第十一批审阅记录（gpt-6.1-sol / xhigh）

**修订后最终状态（2026-10-08）：** 1 项 P1、3 项 P2、1 项 P3 已逐项修订并定向复核关闭，本批在初审范围内通过，见[定向复核](batch-10-11-12-codex-recheck.md)。下文初审发现、原输入位置与当时结论保留为历史。

审阅日期：2026-10-08。审阅者：本会话 Codex 主助手，运行上下文确认模型为 `gpt-6.1-sol / xhigh`；正文编写者为 Opus。重新核对正文与固定源码，未派发子代理。此前[替代复查](batch-11-substitute-review.md)保留为历史。

**初审结论（历史）：审阅完成，暂不通过；1 项 P1、3 项 P2、1 项 P3 开放。** 对象 SHA-256、统计与执行边界见[汇总](batch-10-11-12-codex-review-summary.md)。

## 范围与实际证据核对

完整读取[算子/图编译诊断](../../knowledge/02-software-stack/ascend-op-graph-failure-triage.md)、[弹性训练](../../knowledge/06-training/elastic-training-and-membership.md)、[量化质量](../../knowledge/07-inference/quantization-and-quality.md)，对应三份研究记录、来源审计、registry 与任务/导航。

| 主题 | 本次重新取得的固定文件 | 覆盖与限制 |
|---|---|---|
| 算子/图模式 | TorchNPU `bc51ab84…` 的 VariableFallbackKernel.cpp 全文与 aten/CMakeLists.txt；PyTorch `1eba9b3…` 的 OperatorEntry.cpp L537–560；插件 `52d4acfa…` 的 graph_mode.md 全文 | autograd fallback 与 CPU fallback 必须区分；CMake glob 包含该文件且未排除。图/eager 的指南是显式操作建议；CANN 内部编译阶段仍为缺口 |
| 弹性训练 | PyTorch `1eba9b3…` 的 torch/distributed/run.py、elastic/agent/server/api.py；MindSpeed-LLM `53f3639…` 的 high_availability.md 与 high_availability.py | 核对 torchrun 与 WorkerSpec 默认值的区别，以及 HA/弹性依赖和冲突断言；PyTorch 2.6 run.html 本次网页读取失败，以固定 run.py 的文档和实现对照 |
| 量化 | vLLM `b17039bc…` 的 quantization/README.md、int8.md、目录 API 与 model.py L867–945；插件 `52d4acfa…` 的 supported_features.md 与 quantization.md 前 60 行 | 14 个方法页加 README；支持表与方法页存在 SM 7.5 冲突；插件工具链与 W8A8 声明可核对。每个 kernel 的硬件路径及质量效果未执行 |

既有来源：`src.ascend.torch-npu-v7.2.0-pytorch2.6.0`、`src.pytorch.dispatcher-v2.6.0`、`src.pytorch.elastic-2.6`、`src.ascend.mindspeed-llm-ha-v2.2.0`、`src.vllm.inference-v0-14`、`src.ascend.vllm-ascend-v0-14-0rc1`。新增读取的 run.py/API 文件沿用 elastic 登记中固定的 PyTorch commit；本次直接读取其根 LICENSE，不扩展到生成站点或第三方制品许可。

## 初审发现（历史，已关闭）

### B11-C01 / P1：同一 TorchNPU 文件实际注册 CPU fallback，正文却断言不存在

- 位置：[算子诊断](../../knowledge/02-software-stack/ascend-op-graph-failure-triage.md)第 62 行；[来源记录](batch-11-op-graph-sources.md)的 fallback 行与末节；[来源审计](batch-11-source-audit.md)的重点边界。
- 问题：只引用文件头的 autograd 说明，得出整个文件只是 autograd fallthrough、未注册算子不会回退 CPU。固定文件后半部分定义 `npu_cpu_fallback`，调用 `at::native::cpu_fallback`，并为 `PrivateUse1` 注册全局 fallback，直接反证核心诊断分支。
- 证据：[VariableFallbackKernel.cpp L247–271](https://github.com/Ascend/pytorch/blob/bc51ab84cc6f35c77aab1c59886e0ea43681a317/torch_npu/csrc/aten/VariableFallbackKernel.cpp#L247-L271)；[aten/CMakeLists.txt](https://github.com/Ascend/pytorch/blob/bc51ab84cc6f35c77aab1c59886e0ea43681a317/torch_npu/csrc/aten/CMakeLists.txt)的 cpp 收集和排除清单。前部的 `AutogradPrivateUse1` 与后部的 `PrivateUse1` 是不同注册；`SparsePrivateUse1` 另有直接报错的 fallback。
- 影响：文档会漏掉自动 CPU 执行及其性能代价，错误解释“不支持 NPU 算子”的运行结果，也使读者把注册缺失直接当成不可运行。
- 关闭条件：重写注册层支路，区分后端实现、全局 CPU fallback、autograd 与 sparse fallback；记录 CPU 回退警告和性能线索。只声明固定源码确有该机制，具体算子能否成功仍需 CPU 实现及实际 dispatch 条件；同步研究记录/source-audit，避免反向声称所有算子都能回退。

### B11-C02 / P2：图模式指南的显式切换被写成引擎回退行为

- 位置：[算子诊断](../../knowledge/02-software-stack/ascend-op-graph-failure-triage.md)第 64 行与[来源记录](batch-11-op-graph-sources.md)末条。
- 问题：正文在“已知行为”中写两种图模式都失败时回退 eager，缺少实际动作和配置主体，容易被读成引擎会处理失败。固定指南要求使用者切换，并给出 `enforce_eager=True` / `--enforce-eager` 示例，没有证明自动捕获失败后重试 eager。
- 证据：[graph_mode.md L66–85](https://github.com/vllm-project/vllm-ascend/blob/52d4acfa51fb868823d1070b81cbd2d97e9e4696/docs/source/user_guide/feature_guide/graph_mode.md#L66-L85)。
- 关闭条件：明确“指南建议使用者显式启用 eager 进行对照”，保留授权/配置影响；若要声称自动回退，另给固定实现和触发条件；同步研究记录。

### B11-C03 / P2：WorkerSpec 的默认 3 被当成 torchrun 重启默认值

- 位置：[弹性训练](../../knowledge/06-training/elastic-training-and-membership.md)第 47 行及[来源记录](batch-11-elastic-sources.md)失败模式行。
- 问题：同一段同时讨论 torchrun，却用 WorkerSpec 签名说明默认重启 3 次。固定 v2.6.0 的 torchrun 参数默认是 0；WorkerSpec API 默认 3 是另一入口。正文会让读者误以为未配置的 torchrun 能自动容忍三次失败。
- 证据：[run.py L490–497](https://github.com/pytorch/pytorch/blob/1eba9b3aa3c43f86f4a2c807ac8e12c4a7767340/torch/distributed/run.py#L490-L497)与[api.py L78–86](https://github.com/pytorch/pytorch/blob/1eba9b3aa3c43f86f4a2c807ac8e12c4a7767340/torch/distributed/elastic/agent/server/api.py#L78-L86)。
- 关闭条件：分列 torchrun CLI 默认 0 与 WorkerSpec API 默认 3，要求记录实际传入/环境覆盖值；不把示例里的 `--max-restarts=3` 当默认值，研究记录与 registry 覆盖范围同步。

### B11-C04 / P2：INT8 支持结论未标出同快照的 SM 7.5 冲突

- 位置：[量化质量](../../knowledge/07-inference/quantization-and-quality.md)第 37、41 行及[来源记录](batch-11-quantization-sources.md)支持表/INT8 两行。
- 问题：正文并列给出“支持 Turing”与“compute capability >7.5”，没有说明同一个 Turing（SM 7.5）会得到相反结果。上游方法页自身也在严格不等式后列 Turing，不能将该矛盾整理成一致的硬件可用条件。
- 证据：[README.md L46–63](https://github.com/vllm-project/vllm/blob/b17039bccc17b94a2ea107272ad7bc93508708df/docs/features/quantization/README.md#L46-L63)和[int8.md L8–13](https://github.com/vllm-project/vllm/blob/b17039bccc17b94a2ea107272ad7bc93508708df/docs/features/quantization/int8.md#L8-L13)。
- 关闭条件：将 SM 7.5 边界明确记为文档冲突，按具体量化实现核对 runtime/kernel 条件后再判断；没有进一步证据时保持未知。Blackwell 说明限定为此方法页和版本，不升级为所有 INT8 实现的通用限制。

### B11-C05 / P3：registry 仍登记 15 个方法页，旧复查却已声称同步关闭

- 位置：[registry](../../sources/registry.yaml)第 518 行 `src.vllm.inference-v0-14` 的 notes。
- 问题：正文和研究记录已改为 14 个方法页，登记仍写 15；这与此前替代复查的“已同步 registry”不符。
- 证据：[固定目录](https://github.com/vllm-project/vllm/tree/b17039bccc17b94a2ea107272ad7bc93508708df/docs/features/quantization)本次 API 列表共 15 个文件，其中 README 一个、方法页 14 个。
- 关闭条件：更正登记计数，逐项确认正文、研究记录、registry 一致；将新发现的关闭依据记在本次复核，不覆盖旧报告历史。

## 初审结束状态（历史）

B11-C01–C05 全部开放。P1 为核心流程与固定实现直接矛盾，应优先修订；其余发现分别影响配置行为、硬件支持判断和证据一致性。三篇继续 `draft / source_checked`，没有 NPU、弹性训练或量化评估的执行结果。

## 修订后最终状态

B11-C01–C05 全部 CLOSED。具体改动、与上游证据的定向对照及修订后文件身份见[复核记录](batch-10-11-12-codex-recheck.md)。本批在原审阅范围内通过；三篇仍为 `draft / source_checked`，没有真实环境执行结果。
