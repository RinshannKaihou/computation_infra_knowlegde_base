# 第十六批审阅记录（gpt-6.1-sol / xhigh）

审阅日期：2026-10-09。审阅者：Codex 会话，模型 gpt-6.1-sol，reasoning effort xhigh（用户当前约定）；正文编写者：Kimi（主会话），取证与撰写：探索/撰写子代理。审阅输出全文照录如下。

---
# Batch 16 独立技术审阅报告

- **审阅日期**：2026-10-09（Asia/Shanghai）。
- **模型 / effort**：用户约定为 `gpt-6.1-sol / xhigh`。本会话未提供可核验的实际运行模型与 effort 元数据，因此如实记录约定，**不将其冒充实际执行配置的证明**。
- **审阅角色**：独立审阅者；未参与 Kimi 主会话及其子代理的取证、正文编写。
- **总体结论**：**暂不通过**。确认 **5 项发现：P1 × 1、P2 × 4**；另有明确列出的上游核对未覆盖项。
- **执行边界**：未修改文件，未安装软件或运行设备代码；按只读环境要求跳过 `make build`。

## 一、已完成核对范围

### 1. 仓库与验收要求

已阅读仓库说明、作者指南、内容归属、元数据 schema，以及 T02-04、T02-05、T02-06、T02-07 的 `acceptance` 与 `evidence_blockers`。核对了本批正文、领域索引、四份取证记录及对应来源登记。

执行：

`PYTHONDONTWRITEBYTECODE=1 make check`

结果：**通过，80 个内容条目、277 条来源**。这仅证明检查器覆盖的结构与引用规则通过，不证明技术正确性或远端页面内容。

### 2. 独立上游核对

重新打开并核对了可读取的相关段落，包括：

- ROCm 10.1.0 发布说明的组件版本、TheRock 过渡与合并包、部分组件文档、许可页、安装及 Instinct 验收资料、PyTorch 分发渠道资料。
- CUDA 12.8 发布说明、安装指南元包表、Runtime API 捕获模式及错误枚举；Compute Sanitizer 与 NVIDIA capture-failures 页面。
- PyTorch 2.6 CUDA Graphs 约束，以及固定源码中的编译配置、缓存实现和官方测试；部分无法读取的 HTML 页面改用同一版本文档源码核对。
- caching 教程固定源码 `pytorch/tutorials@8a5c6f1ca69c57b65811ddd843859809cf8c541a`，并与 PyTorch v2.6.0 实现交叉检查。
- HIP docs-7.14.0 环境变量、调试、错误处理、错误码，ROCgdb，以及 docs-7.1.1 PyTorch 兼容说明。
- `pytorch#188355`、`#193735`、`#137414`，PR `#188641`、落地 commit `0ab462c`，以及 `rccl#2022` 的相关讨论。
- 部分 AscendCL、PrivateUse1 与 TorchAir 页面；CANN/TorchAir 整组未完成全量核对，限制见下一节。

下文所称 **PyTorch 固定源码**，统一指 commit：

`1eba9b3aa3c43f86f4a2c807ac8e12c4a7767340`

## 二、声明的未覆盖项

以下限制不作为“正文必然错误”的证据，但也不能计为审阅通过：

1. **ROCm 10.1.0 兼容矩阵**：精确页面读取失败，未独立完成 MI300X 选择器条件块、14 个驱动版本、固件及虚拟化字段逐项核对；发布说明不能替代这些条件块。
2. **HIP graphs docs-10.1.0、ROCprofiler-SDK docs-7.14.0**：指定页面读取失败，相关接口、捕获限制与工具职责未完成完整复核。
3. **CANN/TorchAir 页面组**：部分指定 URL 返回导航壳或与路径版本不符的页面，未完成 `instg_0003` 三渠道包名、HCCL 简介、aclnn 流程、aclmdlRI 页组、缓存环境变量和全部 TorchAir 720 指南的逐项独立核对。
4. **PyTorch 文档与修复版本归属**：部分 2.6 HTML 页面以固定源码补核，但未完成全部章节逐句对照；未独立完成 `0ab462c` 对正文所列全部 release tag 的祖先关系比较。
5. **来源历史增量**：确认当前登记总数为 277，但未独立重构“210→275，再补 2 条”的历史变更链。
6. **实验与构建**：未做硬件验证、故障复现、性能测量、wheel 安装或包内容检查；未运行 `make build`。

## 三、发现列表

### B16-C01 — P1：CUDA Graphs 约束后果分档错误，并扩大禁止范围

**位置**

- `knowledge/02-software-stack/operators-compilers-and-graphs.md:137`
- `knowledge/02-software-stack/gpu-op-graph-failure-triage.md:90`

**问题**

机制文把“同进程同时只能一个 capture”“capture 期间不得有其他 CUDA 工作”放进“违反多半直接 runtime error”一档。PyTorch 2.6 原文将这两项放在**可能导致静默数值错误或未定义行为**的一档。

此外，原文禁止的是捕获期间的 **non-captured CUDA work**，正文“其他 CUDA 工作”遗漏了这个限定。

诊断文虽然分档正确，又将第二档写成“不会被报错暴露”“违反无报错，只能靠清单排除”，把上游的概率性风险描述改成了绝对断言。两篇不仅互相矛盾，还会误导读者对错误可观测性的判断。

**证据**

PyTorch 2.6 `notes/cuda.html` → CUDA Graphs → Constraints：单进程并发 capture 和任何线程上的非捕获 CUDA 工作，均位于静默数值错误／未定义行为一组；原文使用的是“likely”，不是必然有错或必然无报错。citeturn328624view3

**关闭条件**

- 将两项移入正确分档，恢复“非捕获 CUDA 工作”的限定。
- 将诊断文的绝对表述改为“可能不报错，不能依赖异常检测排除”。
- 定向复核两篇及取证表中的全部约束、后果与限定词，确保一致。

### B16-C02 — P2：将 901 的通用错误语义缩成外部线程原因，并外推到 HIP

**位置**

- `knowledge/02-software-stack/gpu-op-graph-failure-triage.md:99`
- `docs/research/batch-16-gpu-op-graph-triage-sources.md:28`

**问题**

共享错误码表把 901 的“典型含义”写为“外部工作/线程打断捕获”。这确实沿用了 NVIDIA 实践指南简表的措辞，但 **901 的 Runtime API 定义不是外部线程归因**，而是先前错误已经使当前捕获序列失效；HIP 官方定义也明确如此。

当前表将实践指南的场景化概括用作 CUDA/HIP 共用释义，容易把同线程中的先前非法调用、900→901 级联等情况误判为线程干扰。正文自己的主案例恰好已经记录了这种级联。

**证据**

- CUDA Runtime API 12.8，`group__CUDART__TYPES.html` → `cudaErrorStreamCaptureInvalidated = 901`：当前捕获序列因先前错误失效。citeturn152250view0
- HIP docs-7.14.0，`reference/error_codes.html` → `hipErrorStreamCaptureInvalidated`：先前捕获错误导致失效后，继续进行捕获操作。citeturn328624view2
- NVIDIA capture-failures 的简表确实给出外部工作／线程概括；应保留其来源与场景边界，而不是替代错误定义。citeturn152250view1

**关闭条件**

将共用释义改为“先前错误已使捕获序列失效”，要求追溯首个捕获失败；把外部线程干扰保留为 NVIDIA 页中的具体场景。同步修订取证记录，说明实践指南简表与 Runtime API 定义的粒度差异。

### B16-C03 — P2：将不在 PyTorch 2.6 中的 Mega-Cache API 混入固定样板

**位置**

- `knowledge/02-software-stack/operators-compilers-and-graphs.md:121`
- `docs/research/batch-16-operators-compilers-sources.md:24`
- `docs/research/batch-16-gpu-op-graph-triage-sources.md:17`

**问题**

正文明确将 GPU 主样板固定为 PyTorch 2.6，却在缓存组成中直接列入：

`torch.compiler.save_cache_artifacts()` / `load_cache_artifacts()`

这些接口出现在所引用的较新教程中，但**不存在于本文固定的 v2.6.0 `torch/compiler/__init__.py` 中**。教程笼统的“PyTorch 2.4 or later”前提，不能证明其中每个新增接口都在 2.6 可用。

“latest 教程、环境变量默认值按 2.6 复核”的注记没有解决 API 可用版本问题。

**证据**

固定 PyTorch 源码对两个接口均无定义；固定教程 `8a5c6f1` 的 Mega-Cache 小节则明确列出它们，构成需要显式隔离的版本差异。citeturn505829view0turn534123view0turn534123view1

**关闭条件**

- 从“2.6 主样板能力”中移除这两个接口，或单独标为“较新教程能力，非 2.6 能力”。
- 若保留可用性说明，补充准确的最低版本或固定实现证据。
- 检查同一较新教程引入的其他缓存组件描述是否也被无条件归入 2.6。
- 同步更新两份取证记录，不能仅复述教程总前提。

### B16-C04 — P2：缓存测试同时改变了 FX 图，不能证明 guard 值独立决定缓存身份

**位置**

- `knowledge/02-software-stack/operators-compilers-and-graphs.md:122`
- `knowledge/02-software-stack/operators-compilers-and-graphs.md:227`
- `knowledge/02-software-stack/operators-compilers-and-graphs.md:251`
- `knowledge/02-software-stack/gpu-op-graph-failure-triage.md:126`
- `docs/research/batch-16-operators-compilers-sources.md:37`

**问题**

正文将 `test_cache_guard` 解释为“guard 值参与缓存身份，不同取值的编译产物不互相命中”。

该测试将 `val=6` 改为 `val=4` 时，执行分支也从 **sin 改为 cos**，因此 FX 图本身发生变化。它不能隔离证明：

- guard 值本身独立进入缓存 key；
- 所有不同 guard 取值都不能命中；
- 这是“同图、同形状、同配置”之外的独立变量反例。

实现中的“先按 key 查候选，再检查 guard 表达式是否成立”，也不能简化为“不同值即不同 key”。

**证据**

固定源码 `test/inductor/test_codecache.py:779` 的测试确实同时改变分支与算子；`torch/_inductor/codecache.py` 的 `FxGraphCache._lookup_graph` 则对同一 key 的候选执行 guard 表达式检查。citeturn268072view1turn505829view1

**关闭条件**

将该测试结论收窄为“分支变化形成不同图时，不错误复用此前产物”。若要说明 guard 对命中的作用，引用候选 guard 检查实现；若要声称 guard 值独立进入 key，补充能够控制其他变量的精确证据。同步修订标题、总括段落和诊断文回链说明。

### B16-C05 — P2：将 Inductor 缓存禁用开关等同于全栈冷启动

**位置**

- `knowledge/02-software-stack/operators-compilers-and-graphs.md:123`
- `knowledge/02-software-stack/operators-compilers-and-graphs.md:227`
- `knowledge/02-software-stack/gpu-op-graph-failure-triage.md:185`
- `knowledge/02-software-stack/gpu-op-graph-failure-triage.md:186`
- `docs/research/batch-16-operators-compilers-sources.md:25`

**问题**

正文把 `TORCHINDUCTOR_FORCE_DISABLE_CACHES=1` 写成“全禁”“强制冷启动计时”。固定源码限定的是 **Inductor 层缓存**，不能据此保证整个编译栈处于冷状态。

同时，已显式设置的 `TRITON_CACHE_DIR` 不随更换 `TORCHINDUCTOR_CACHE_DIR` 自动更换；Triton 编译器仍有自己的命中路径。若不明确进程状态与实际缓存目录，文中的冷／热对照可能仍复用缓存。

此外，“禁用缓存”与“缓存机制正常开启、但缓存为空”的冷启动不是同一实验条件。

**证据**

- 固定 `_inductor/config.py:90` 将开关范围限定为 Inductor 层。citeturn268072view0
- 固定 `runtime/cache_dir_utils.py` 的 `triton_cache_dir` 优先返回显式 `TRITON_CACHE_DIR`。citeturn534123view3
- PyTorch 固定源码所钉住的 Triton commit `35c6c7c6284582b3f41c71c150e11b517acf074a`，`python/triton/compiler/compiler.py:248` 附近具有独立缓存命中与返回编译产物的路径。citeturn268072view2

**关闭条件**

明确区分“禁用 Inductor 缓存”与“测量冷缓存启动”；后者需说明新进程或进程内状态重置、实际 Inductor/Triton 缓存目录、远程缓存状态及清理范围，并保留命中／未命中观测。不要把单一开关当作全栈冷启动证明。

## 四、无发现项

在已核对范围内，以下方面未发现需要另立编号的问题；这不是对未覆盖来源的背书：

- **元数据与引用结构**：`make check` 通过，未发现目标条目的 ID 唯一性、来源引用或内部链接检查错误。
- **T02-07 回填**：`operators-compilers-and-graphs.md:37` 已加入姐妹篇 `related_ids`，`operators-compilers-and-graphs.md:257` 已补正文链接；领域索引包含新增入口。
- **文档样板不冒充实测**：AMD 档案保留 `not_run`；GPU 指南保留 `not_verified`、空环境与实验证据引用，没有把结构检查或官方测试源码阅读写成本库复现。
- **平台边界**：未将 MI300X 样板写成 MI325X／MI355X、Radeon／Ryzen或 GIM 虚拟化的通用可运行配套；相关未取证边界仍保留。
- **冲突与缺口**：HIP、LLVM 站标冲突及 FAQ／config 默认值差异仍有记录；CANN 编译器职责缺口、HCCL 的 8.2.RC1alpha001 树绑定、HDK 交集 `blocked` 未被消解。
- **案例证据分层**：`@skipIfRocm` 未被当作 HIP 测试通过；`#193735` 的“无法复现后关闭”未被写成修复；公开案例未被写成本地事故或本库实验结果。

## 五、验收结论与复核要求

**结论：暂不通过。**

T02-06 的固定版本能力、缓存证据与对照方法，以及 T02-07 的错误语义和诊断判据，仍有影响技术正确性或证据边界的问题。T02-04、T02-05 暂未确认同等级正文错误，但上游核对尚不完整，不能据此宣布全面通过。

关闭顺序：

1. 修订 B16-C01 至 B16-C05，并同步修订取证记录中的重复结论。
2. 对约束分档、901 定义、2.6 API 可用性、guard 证据和冷缓存方法做**定向复核**。
3. 补齐本报告声明的关键上游未覆盖项，或明确保留为尚未验收的子项。
4. 修订者在可写环境运行 `make check`、`make build`，提供结果供结构／构建复核。

**发现修订完成不等于审阅通过；审阅通过也不等于硬件验证通过。**
