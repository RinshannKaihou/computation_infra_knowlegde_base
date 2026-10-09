# 第十六批定向复核记录（gpt-6.1-sol / xhigh）

复核日期：2026-10-09。复核者：Codex 会话（resume），模型 gpt-6.1-sol / xhigh。复核对象为[初审记录](batch-16-codex-review.md)的 5 项发现及[修订记录](batch-16-review-fixes.md)。复核输出全文照录如下。

---
# Batch 16 初审发现定向复核报告

- **复核日期**：2026-10-09（Asia/Shanghai）。
- **模型 / effort**：用户约定为 `gpt-6.1-sol / xhigh`；本会话没有可核验的实际运行模型及 effort 元数据，因此记录约定，**不将其作为实际执行配置的证明**。
- **角色与边界**：独立审阅者；未修改正文、研究记录或来源登记，未运行设备代码或性能实验。
- **结论**：**暂不通过**。原发现 **3 项 CLOSED、2 项 OPEN**；修订引入 **B16-C06（P2）、B16-C07（P3）**。

## 一、已完成范围

已对照两篇修订正文、两份研究记录、`docs/research/batch-16-review-fixes.md`、三条新增来源登记及受影响的既有登记。

独立重开核对的主要材料：

- PyTorch v2.6.0 固定 commit `1eba9b3aa3c43f86f4a2c807ac8e12c4a7767340`：CUDA Graphs Constraints、compiler API、Inductor/Dynamo 配置、FXGraph/AOTAutograd/PGO/Autotune 缓存、Triton bundling、缓存目录逻辑及 `test_cache_guard`。
- tutorials 固定 commit `8a5c6f1ca69c57b65811ddd843859809cf8c541a` 的缓存教程。
- Triton commit `35c6c7c6284582b3f41c71c150e11b517acf074a` 的编译缓存命中分支、版本标识，以及 PyTorch 的对应 CI commit pin。
- CUDA Runtime API 12.8 错误枚举、HIP docs-7.14.0 错误码、NVIDIA capture-failures 简表。

独立执行 `PYTHONDONTWRITEBYTECODE=1 make check`：**PASS，80 个内容条目、280 条来源**。三条新增 ID 与引用通过结构检查；该结果不证明技术正确性或远端内容。本轮未运行 `make build`，保持审阅操作不改写生成产物。

以下 PyTorch 上游定位均指上述固定 commit，而非 `main`。

## 二、逐项判定

| 发现 | 判定 | 复核结果 |
|---|---|---|
| **B16-C01 — P1** | **CLOSED** | `operators-compilers-and-graphs.md:139`、`gpu-op-graph-failure-triage.md:92` 已恢复正确两档，将单进程单 capture、任意线程上的 **non-captured CUDA work** 放入静默数值错误／未定义行为组；保留两档的 `likely`，不再断言必然报错或必然无报错。两份取证表同步一致。上游定位：`docs/source/notes/cuda.rst` → Constraints。citeturn269353view1 |
| **B16-C02 — P2** | **CLOSED** | `gpu-op-graph-failure-triage.md:101` 已将 901 定义改为先前错误导致捕获序列失效，要求追溯首个失败；NVIDIA 简表的外部工作／线程描述仅作为场景化概括，不再成为 CUDA/HIP 共用归因。研究记录及新增错误枚举登记一致。citeturn570567view1turn342544view0turn570567view3 |
| **B16-C03 — P2** | **OPEN** | Mega-Cache 两个 API 已正确隔离为非 2.6 能力；固定 `torch/compiler/__init__.py` 确实没有这两个接口。但“同教程其他组件逐项甄别”的关闭条件尚未满足：修订错误地把 `InductorCache` 所描述的打包机制一并判为非 2.6，详见 **B16-C06**。citeturn269353view0turn269857view0turn941647view0 |
| **B16-C04 — P2** | **CLOSED** | `operators-compilers-and-graphs.md:255` 已指出 `val=6→4` 同时使分支 `sin→cos`、FX 图变化，不再用该测试证明 guard 值独立进入 key；`FxGraphCache._lookup_graph` 的“按 key 取候选，再检查候选 guard 表达式”也已正确保留。身份汇总、诊断文及研究记录没有继续扩大该测试结论。citeturn705329view0turn606788view0 |
| **B16-C05 — P2** | **OPEN** | Inductor 层限定、显式 `TRITON_CACHE_DIR` 的独立性、Triton 独立命中路径均已修正。但冷启动操作仍允许“清空缓存目录 **或新进程**”，且既有来源登记还保留“全禁（冷启动计时）”。详见下一节。citeturn608817view1turn414715view1turn487906view0 |

### B16-C03 剩余关闭条件

Mega-Cache API 部分无需重做；最低可用版本暂未取得的限制可以保留。剩余要求是关闭 **B16-C06**，同步正文、两份研究记录、来源登记和修订摘要中的组件判定。C03 的 OPEN 与 C06 是同一未完成关闭条件的关联记录，**不按两个独立根因计数**。

### B16-C05 剩余差距与关闭条件

**位置**

- `knowledge/02-software-stack/operators-compilers-and-graphs.md:231`
- `knowledge/02-software-stack/gpu-op-graph-failure-triage.md:187`
- `docs/research/batch-16-review-fixes.md:82`
- `docs/research/batch-16-review-fixes.md:83`
- `sources/registry.yaml:3109`

**剩余问题**

1. **新进程不能替代持久化缓存的冷状态。** 两篇操作段落仍写“清空的缓存目录或新进程”。FXGraphCache 会从磁盘／远程缓存按 key 读取候选，Triton 编译器也会读取其缓存元数据并直接返回已缓存产物。因此，即使换新进程，保留的持久化缓存仍可能命中；只记录目录和清理范围，不能把未清理的状态变成冷缓存状态。citeturn606788view0turn487906view0
2. **既有登记未同步。** `sources/registry.yaml:3109` 仍保留 `TORCHINDUCTOR_FORCE_DISABLE_CACHES=1 全禁（冷启动计时）`，与修订正文及新增固定源码登记相冲突。

**精确上游定位**

- `torch/_inductor/codecache.py:1000`，`FxGraphCache._lookup_graph`：读取本地／远程候选并检查 guards。
- `torch/_inductor/runtime/cache_dir_utils.py`，`triton_cache_dir`：显式 `TRITON_CACHE_DIR` 优先，不随 Inductor 目录替换。
- Triton `python/triton/compiler/compiler.py:250` 附近：元数据存在且未启用 `always_compile` 时直接命中。
- `torch/_inductor/config.py:90`：禁用开关的声明范围是 Inductor 层。citeturn606788view0turn414715view1turn487906view0turn608817view1

**关闭条件**

- 将“目录清空 **或** 新进程”改为两个独立维度：处理进程内状态，**并**使测量范围内的相关持久化缓存处于已说明的冷状态。
- 明确实际 Inductor/Triton 目录、远程缓存处理方式及命中／未命中证据；若只重启进程而保留磁盘缓存，应称“新进程启动”，不能称“冷缓存启动”。
- 同步上述操作段落、修订摘要及 `sources/registry.yaml:3109`；保留“禁用缓存”与“缓存开启但为空”不是同一实验条件的区分。

## 三、新发现

### B16-C06 — P2：以不存在同名类为由，错误否定 2.6 已有的 FXGraph/Triton 打包机制

**位置**

- `knowledge/02-software-stack/operators-compilers-and-graphs.md:125`
- `knowledge/02-software-stack/gpu-op-graph-failure-triage.md:128`
- `docs/research/batch-16-operators-compilers-sources.md:24`
- `docs/research/batch-16-operators-compilers-sources.md:121`
- `docs/research/batch-16-gpu-op-graph-triage-sources.md:17`
- `docs/research/batch-16-review-fixes.md:52`
- `sources/registry.yaml:3165`

**问题**

修订将两类证据混为一谈：

- `torch.compiler.save_cache_artifacts()/load_cache_artifacts()`：固定 2.6 中没有这些 API。
- 教程中的 `InductorCache`：定义为 FXGraphCache 与 Triton cache 的组合，**不是对同名 Python 类存在性的声明**。

因此，“无 `InductorCache` 类／字符串”不能推出“FXGraphCache+Triton 打包是非 2.6 能力”。固定 2.6 已有实际收集、保存和恢复路径。citeturn269353view0turn269857view0turn941647view0turn606788view0

同一段把 Triton 编译产物缓存主要对应到 `TritonCodeCache`，也没有准确区分层次：该类通过 `PyCodeCache.load(source_code)` 加载生成的 Python kernel 模块，并非教程所说 cubin 等编译产物缓存的完整实现定位。应分别指出 Triton 编译器的产物缓存与 PyTorch 的 bundling 路径。citeturn644564view2turn487906view0

**精确上游证据**

- tutorials@`8a5c6f1`，`recipes_source/torch_compile_caching_tutorial.rst` → Modular caching：`InductorCache` 是 FXGraphCache 与 Triton cache 的组合。citeturn269857view0
- PyTorch `torch/_inductor/triton_bundler.py:63`，`TritonBundler`：记录 kernel、收集产物，并在缓存读取时恢复产物。citeturn887367view0
- `torch/_inductor/compile_fx.py:679`，cache-miss 分支：调用 `TritonBundler.collect()`、`set_triton_bundle()`，随后保存 FXGraph 缓存。citeturn941647view0
- `torch/_inductor/codecache.py:1076`：读取 `graph._triton_bundle` 并调用 `TritonBundler.read_and_emit()`。citeturn606788view0
- `torch/_inductor/config.py:23`：bundling 配置在 OSS、环境变量未覆盖时的默认值为 **True**；实际路径仍受缓存启用、禁用开关等条件控制，不能误读 `TritonBundler.is_enabled()` 后面的 OSS fallback 为默认关闭。citeturn608817view1turn880417view0turn887367view0
- `torch/_inductor/codecache.py:2820`，`TritonCodeCache.load`：调用的是 `PyCodeCache.load`，应与 Triton 编译产物缓存区分。citeturn644564view2

**关闭条件**

- 将“Mega-Cache API 不在 2.6”与“教程组件概念在 2.6 中的实现映射”分开。
- 删除“InductorCache 打包机制非 2.6”的断言，补入 `TritonBundler`、FXGraph 保存／恢复路径及实际开关条件。
- 区分 `TritonCodeCache` 的 Python 模块缓存、Triton 编译产物缓存和产物打包。
- 同步所有上述正文、研究记录、来源登记和修订摘要，不能仅删除同名类判断而留下“非 2.6”结论。

### B16-C07 — P3：Triton 固定来源关联被错误写成“只钉版本号、不钉完整 commit”

**位置**

- `docs/research/batch-16-review-fixes.md:92`
- 关联登记：`sources/registry.yaml:3171`

**问题与证据**

修订摘要称“v2.6.0 钉的是版本号非完整 commit”。但在相同 PyTorch 固定 commit 下：

` .ci/docker/ci_commit_pins/triton.txt:1 `

内容正是 `35c6c7c6284582b3f41c71c150e11b517acf074a`。这不是仅凭版本字符串推断的关联，而是已有可直接引用的 **CI 固定源码关联**。当前摘要错误描述了取证链。citeturn647886view0

**关闭条件**

- 改正“非完整 commit”的断言，补记该 CI pin 的精确路径和固定 PyTorch revision，并同步来源登记。
- 保持范围准确：这证明对应 CI 源码 pin，**不自动证明所有 PyTorch/ROCm wheel 或本地安装均使用同一 Triton commit**。

## 四、无新增异议的核对项

- C01 的分档、`likely` 和 `non-captured` 限定已一致恢复。
- C02 的 CUDA/HIP 901 定义与 NVIDIA 简表场景边界已正确分离。
- C04 不再将 `sin→cos` 的复合变化当作 guard 独立入 key 的证据。
- FORCE_DISABLE 的层次限定、显式 Triton 目录独立性与 Triton 独立命中路径本身没有剩余异议；C05 的 OPEN 来自操作口径和登记同步，而不是这些修订。
- 本轮结构检查未发现新增 ID、引用或本地链接错误。

## 五、仍未覆盖的材料与验证

**本轮关键定向材料已取得；不再以这些材料不可读作为 C01–C05 的限制。** 但初审以下未覆盖项仍未关闭，本轮没有扩展为全批重新取证：

| 初审未覆盖项 | 本轮状态 |
|---|---|
| ROCm 10.1.0 兼容矩阵的 MI300X 条件块、14 个驱动版本、固件与虚拟化字段 | **仍未完成独立核对** |
| HIP graphs docs-10.1.0、ROCprofiler-SDK docs-7.14.0 指定页 | **仍未完成完整核对** |
| CANN/TorchAir 页组：三渠道包名、HCCL、aclnn、aclmdlRI、缓存环境变量及全部 720 指南 | **仍未完成逐项核对** |
| 全部 PyTorch 2.6 HTML 章节逐句对照；`0ab462c` 对正文所列全部 release tag 的祖先比较 | **仍未完成**；本轮只补核定向固定源码 |
| “210→275，再补 2 条”的来源历史变更链 | **仍未重构**；本轮确认当前总数 280 及三条新增 ID |
| 硬件验证、故障复现、性能测量、wheel 安装及包内容检查、`make build` | **本轮均未执行**；`make check` 已独立通过 |

## 六、最终结论

**暂不通过。**

C01、C02、C04 关闭；C03、C05 仍 OPEN。必须完成缓存组件映射纠正、冷缓存实验条件修订和来源记录同步，并关闭新增 C06、C07 后，再进行定向复核。

这不是对修订方向的否定，也不要求重做已关闭项；但当前缓存部分仍存在影响技术正确性与可追溯性的具体差距。即使这些发现全部关闭，也不能把初审未覆盖项或硬件验证自动计为通过。
