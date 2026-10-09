# 第十六批审阅发现修订记录（B16-C01–C05）

修订日期：2026-10-09。修订者：撰写子代理（非 gpt-6.1-sol）。依据：`docs/research/batch-16-codex-review.md`（审阅约定 gpt-6.1-sol / xhigh；5 项发现：P1×1、P2×4）。修订前按报告给出的精确上游定位**重新打开核对**了全部关键来源（逐条见下），核对结论记入对应来源登记与研究记录；未执行任何编译、图捕获或设备代码；两篇正文维持 `draft` 与 `source_checked` / `not_verified` 语义，只收窄或重述结论，未扩大。

修改文件一览：

- `knowledge/02-software-stack/operators-compilers-and-graphs.md`（C01、C03、C04、C05）
- `knowledge/02-software-stack/gpu-op-graph-failure-triage.md`（C01、C02、C04、C05）
- `docs/research/batch-16-operators-compilers-sources.md`（C01、C03、C04、C05 同步）
- `docs/research/batch-16-gpu-op-graph-triage-sources.md`（C01、C02、C03 同步）
- `sources/registry.yaml`（新增 3 条来源，见文末）

## B16-C01（P1）CUDA Graphs 约束后果分档错误并扩大禁止范围

**修改位置**

- 机制文「设备图捕获（一）：CUDA Graphs 手动路径」Constraints 清单：「同进程同时只能一个 capture」「capture 期间进程内任何线程不得运行**非捕获 CUDA 工作**（non-captured CUDA work）」从「多半 runtime error」档移入「多半静默数值错误或未定义行为」档；同档补齐「CPU 工作不被捕获（replay 时被省略）」「多流捕获允许但另有限制」；第一档补多 generator 注册项（register_generator_state + graphsafe API）；补注两档原文均为 "likely"（多半），既非必然报错也非必然无报错。
- 诊断文步骤 4：第二档改为「违反**可能不报错**，不能依赖异常检测排除，须靠核对清单」；表格「预期证据与解释」列的「第二档约束违反无报错，只能靠清单排除」同步改为「可能不报错，不能靠异常检测排除，须靠清单核对」；第二档补 non-captured 限定与多流条目。
- 取证表同步：`batch-16-operators-compilers-sources.md` CUDA Graphs 行（限定词 + 多流 + 两档 likely 措辞）、`batch-16-gpu-op-graph-triage-sources.md` PyTorch 捕获约束行（删除「不会被报错暴露」绝对表述，补 non-captured 限定）。

**依据（重开核对）**

- `docs/source/notes/cuda.rst` @v2.6.0 commit `1eba9b3`（Constraints 节）：第一档 "Violating any of these will likely cause a runtime error" 仅含非默认流、CPU↔GPU 同步禁止、CUDA RNG 多 generator 注册三项；第二档 "Violating any of these will likely cause silent numerical errors or undefined behavior" 含原文条目 "Within a process, only one capture may be underway at a time" 与 "No non-captured CUDA work may run in this process (on any thread) while capture is underway"，同档还有 CPU work elided、same (virtual) memory addresses、动态控制流/动态形状、multistream restrictions。两档均为 likely 措辞——与审阅报告一致，正文原分档确属错误。

## B16-C02（P2）将 901 的通用错误语义缩成外部线程原因并外推到 HIP

**修改位置**

- 诊断文「CUDA/HIP 捕获错误码对照」：表导语注明 901 通用释义以 CUDA Runtime API 12.8 错误枚举与 HIP error codes 页定义为准；901 行改为「**先前错误已使当前捕获序列失效**……定性须追溯**首个**捕获失败；NVIDIA capture-failures 简表把典型场景概括为『外部工作/线程打断捕获』，粒度粗于 Runtime API 定义，不能反推 901 必由外部线程引起（同线程先前非法调用、900→901 级联同样落在定义内）」。
- `batch-16-gpu-op-graph-triage-sources.md` 错误码表行：同步改为 Runtime API/HIP 定义 + 简表粒度差异说明，并补两处定义链接。
- 正文「症状≠根因」段既有「连锁报 Invalidated 须锚定首失败」与新释义一致，未改；主案例观察层的「900→901 级联，定性只锚定 900」亦与新释义一致。

**依据（重开核对）**

- CUDA Runtime API 12.8.0 归档 `group__CUDART__TYPES.html`：`cudaErrorStreamCaptureInvalidated = 901` — "The current capture sequence on the stream has been invalidated due to a previous error."
- HIP docs-7.14.0 `reference/error_codes.html`：`hipErrorStreamCaptureInvalidated` — "Operation failed due to a previous error during capture. This error occurs when a stream capture has been invalidated by a prior error but capture operations are still being attempted…"
- NVIDIA capture-failures 页（页面声明 0.16.1）：简表 901 行确为 "Capture was interrupted by external work or thread"，但**同页**报错文本亦写 "operation failed due to a previous error during capture"——简表是场景化概括，粒度差异成立。
- 新增来源登记 `src.nvidia.cuda-runtime-api-error-enum-12.8`（归档页，同 Stream 页 EULA 口径）。

## B16-C03（P2）将不在 PyTorch 2.6 中的 Mega-Cache API 混入固定样板

**修改位置**

- 机制文「编译缓存：组成、身份与落盘」组成项：整条改写为「组成（v2.6.0 固定源码逐项核对）」，Mega-Cache 两个 API 与 `InductorCache` 组件单独标为「较新教程能力（非 2.6）」，注明 `torch/compiler/__init__.py` 无这两个接口、codecache.py 无 `InductorCache`，最低可用版本未取得，且教程 "PyTorch 2.4 or later" 总前提不证明逐接口在 2.6 可用。
- 诊断文「编译缓存观测」行：组件列表改为经 2.6 核对的名称（Triton 产物缓存 / AutotuneCache），注明教程另列的 Mega-Cache API 与 InductorCache 不在 2.6。
- 两份研究记录对应行同步（batch-16-operators-compilers-sources.md 组成行 + 缺口与冲突新增「教程缓存组件与 2.6 的版本差异」条目；batch-16-gpu-op-graph-triage-sources.md 编译缓存身份行）。

> 注（第二轮，B16-C06）：本节及下方甄别表中把 `InductorCache` 判为「非 2.6」、把 TritonCache 主要对应到 `TritonCodeCache` 的两处结论已被定向复核撤销/修正——教程 `InductorCache` 是「FXGraphCache 与 Triton cache 的组合」概念而非同名类存在性声明，2.6 有 TritonBundler 实现映射；`TritonCodeCache` 加载的是 Python kernel 模块而非 cubin 产物缓存。Mega-Cache API「非 2.6」的判定复核确认正确、保留。详见文末「第二轮（定向复核后）」。

**同一教程其他组件的甄别（关闭条件第 3 项，逐项重开核对 v2.6.0 @1eba9b3）**

- FXGraphCache：在 2.6——`class FxGraphCache`（torch/_inductor/codecache.py L937），`fx_graph_cache` 配置 L45–47（OSS 默认开）。保留为 2.6 组件。
- TritonCache：2.6 无同名类；机制上对应 `TritonCodeCache`（codecache.py L2820）、`bundle_triton_into_fx_graph_cache` 配置（L23–25/56–58）与缓存目录 `triton/<device>` 子目录。正文改写为「Triton 产物缓存」并注明命名差异。
- InductorCache（教程称 FXGraphCache+Triton 打包）：v2.6.0 无该类、无该字符串（全仓库树检索无 `inductor_cache` 命名）。**非 2.6，单独标注。**
- AOTAutogradCache：在 2.6——`class AOTAutogradCache`（torch/_functorch/_aot_autograd/autograd_cache.py L611，非 _inductor/codecache.py）。保留为 2.6 组件（正文补准确路径）。
- PGO-cache：在 2.6——`torch/_dynamo/pgo.py` 存在，开关 `TORCH_DYNAMO_AUTOMATIC_DYNAMIC_LOCAL_PGO` 默认 0（_dynamo/config.py L532–535）。保留为 2.6 组件（正文补准确路径与默认值）。
- AutotuningCache：在 2.6——`class AutotuneCache`（torch/_inductor/runtime/autotune_cache.py L64；教程外链钉的 commit 795a6a0 非 2.6，属教程自身引用）。正文注「教程称 AutotuningCache」。
- Mega-Cache（save/load_cache_artifacts）：`torch/compiler/__init__.py`（404 行）与 `__all__` 均无定义。**非 2.6，单独标注；最低可用版本未取得（保留限制）。**

**依据来源**：pytorch/tutorials @`8a5c6f1`（recipes_source/torch_compile_caching_tutorial.rst，Mega-Cache 小节与组件清单）；v2.6.0 源码 commit `1eba9b3`（上述各文件）。新增来源登记 `src.pytorch.inductor-cache-sources-v2.6.0`。

## B16-C04（P2）缓存测试同时改变了 FX 图，不能证明 guard 值独立决定缓存身份

**修改位置**

- 机制文「编译缓存」身份项：改为「图与 guard 同时变化时的 cache miss；编译配置进入 key；guard 值独立进入 key 未证明」。
- 机制文「对照方法：编译缓存身份」段：test_cache_guard 收窄为「图变化（伴随 guard 值变化）时 cache miss 且不误复用」，明确「该测试不能隔离证明 guard 值独立进入缓存 key，此独立证据未取得」；配置变化入 key 仍由 test_hash_config_changes 单独支撑。
- 机制文反例二小节：标题改为「图与 guard 同时变化的 cache miss（test_cache_guard）」；正文明确 val=6→4 同时把分支 sin 改为 cos、FX 图本身变化；补 `FxGraphCache._lookup_graph`（codecache.py L1000 起）先按 key 取候选、再对候选求值 guard 表达式的实现依据，说明不能简化为「guard 值不同即不同 key」；「guard 值独立进入缓存 key」标注未取得。
- 机制文「常见误解·缓存命中=结果一致」：改为「test_cache_guard 观察到图与 guard 同时变化时不互相命中、不误复用」。
- 诊断文「编译缓存观测」行边界列：改为「图与 guard 同时变化不误复用；配置变化独立入 key；guard 值独立入 key 未证明」。
- 研究记录同步：`batch-16-operators-compilers-sources.md` 反例 B 行整行收窄（含 _lookup_graph 证据）、「对照方法与缓存身份」汇总行收窄、缺口新增「guard 值独立入 key 的隔离证据未取得」条目。

**依据（重开核对）**

- `test/inductor/test_codecache.py` L779–799 @1eba9b3：`test_cache_guard` 的 `f(x, val)` 中 `val>5` 走 `x.sin()`、否则 `x.cos()`；两次调用 val=6 / val=4，分支与算子同时变化，FX 图必然不同；断言为第二次仍 miss=1、hit=0 且 `assertNotEqual(a, b)`。
- `torch/_inductor/codecache.py` L1000 起：`FxGraphCache._lookup_graph` 按 key 定位候选目录（local 子目录 + remote），再 "evaluate their guards to determine whether there's a hit"——命中判定含候选 guard 表达式求值，不能化简为「guard 值不同即不同 key」。
- 结论：审阅指出的混杂变量成立；原表述「guard 值参与缓存身份、不同取值不互相命中」超出该测试证明力，已全部收窄。

## B16-C05（P2）将 Inductor 缓存禁用开关等同于全栈冷启动

**修改位置**

- 机制文「编译缓存」落盘与开关项：删除「全禁（冷启动计时用）」；改为「只禁 Inductor 层缓存」（引 config.py L90–91 注释原文 "Force disabled all inductor level caching"），并写明显式 `TRITON_CACHE_DIR` 不随 `TORCHINDUCTOR_CACHE_DIR` 更换而变（cache_dir_utils.py 的 `triton_cache_dir` 优先返回显式值，未设时才用 `triton/<device>` 子目录）、Triton 有独立命中路径（compiler.py L250 附近）；补「禁用 Inductor 缓存 ≠ 缓存开启但为空的冷启动，也不是全栈冷启动证明」，冷缓存测量须说明新进程或进程内状态重置、实际生效的 Inductor/Triton 缓存目录、远程缓存状态与清理范围，并保留命中/未命中观测。
- 机制文「对照方法：编译缓存身份」操作含义：冷启动计时改为「清空的缓存目录或新进程 + 记录 TRITON_CACHE_DIR 实际取值与清理范围」，不再写「FORCE_DISABLE_CACHES 强制冷启动计时」。（注：本条与下条的「**或**新进程」口径于第二轮被 B16-C05 复核改为两个独立维度——新进程不能替代持久化缓存的冷状态，见文末「第二轮」。）
- 诊断文「对照矩阵」第 3 条：性能对照改为「FORCE_DISABLE_CACHES 只禁 Inductor 层缓存、不是全栈冷启动，冷启动计时须用清空的缓存目录或新进程并保留命中/未命中观测」；第 4 条恢复确认：补记 `TRITON_CACHE_DIR` 显式设置与实际生效目录、远程缓存状态、新进程/进程内重置方式，并明确「禁用 Inductor 层缓存」与「缓存机制正常开启但目录为空」不是同一实验条件、不得混写。
- 诊断文「适用范围与前置条件」：缓存目录记录项补「含 TRITON_CACHE_DIR 是否显式设置及实际生效目录」。
- 研究记录同步：`batch-16-operators-compilers-sources.md` 落盘与开关行整行改写（含三处源码证据）+ 缺口新增「禁用 Inductor 缓存≠冷缓存启动」条目。

**依据（重开核对）**

- v2.6.0 `torch/_inductor/config.py` L90–91：`force_disable_caches = os.environ.get("TORCHINDUCTOR_FORCE_DISABLE_CACHES") == "1"`，其上一行注释 "Force disabled all inductor level caching -- This will override any other caching flag"——范围限 Inductor 层。
- v2.6.0 `torch/_inductor/runtime/cache_dir_utils.py`：`triton_cache_dir()` 优先返回显式 `TRITON_CACHE_DIR`；`cache_dir()` 读 `TORCHINDUCTOR_CACHE_DIR` 否则 `tempdir/torchinductor_<user>`；未设 TRITON_CACHE_DIR 时 Triton 缓存落在 `cache_dir()/triton/<device>`。
- Triton commit `35c6c7c6`（`python/triton/__init__.py` 报 `__version__='3.2.0'`，为 tag v3.2.0 祖先；PyTorch v2.6.0 `.ci/docker/triton_version.txt` 钉 3.2.0）`python/triton/compiler/compiler.py`：`compile()`（L217 起）自行计算 hash 查缓存，L250 附近 `if not always_compile and metadata_path is not None:` 分支注释 "cache hit!" 并直接返回已缓存编译产物——独立命中路径成立。
- 新增来源登记 `src.triton.compiler-3-2-0-35c6c7c6`（核对了 commit 与 v2.6.0 钉定版本 3.2.0 的对应关系：v2.6.0 钉的是版本号非完整 commit，该 commit 属 3.2.0 线，已在登记 revision 中如实记录）。（注：括号内「钉的是版本号非完整 commit」的取证链描述于第二轮被 B16-C07 更正——v2.6.0 `.ci/docker/ci_commit_pins/triton.txt:1` 直接钉定该完整 commit，见文末「第二轮」。）

## 新增来源登记（sources/registry.yaml，277→280）

- `src.pytorch.inductor-cache-sources-v2.6.0`：v2.6.0 缓存相关源码（codecache.py、cache_dir_utils.py、autotune_cache.py、autograd_cache.py、pgo.py、torch/compiler/__init__.py），notes 记录 C03/C04/C05 逐项核对结果。
- `src.triton.compiler-3-2-0-35c6c7c6`：Triton 3.2.0 线 compiler.py 独立缓存命中路径（C05）。
- `src.nvidia.cuda-runtime-api-error-enum-12.8`：CUDA Runtime API 12.8 错误枚举页（C02，901 定义）。

## 验证

- `PYTHONDONTWRITEBYTECODE=1 make check`：**PASS，80 个内容条目、280 条来源**（结构、引用与本地链接检查；不证明技术正确性或远端内容）。
- `make build`：**PASS**，重建 `build/catalog.json` 与 `build/catalog.md`。

## 保留限制（未取得/未裁决）

- Mega-Cache API 的最低可用 PyTorch 版本未取得（教程总前提 "2.4 or later" 不作数；`InductorCache` 项已于第二轮改判为 2.6 有实现映射的概念名，不再列入此项）；如需补齐须另查固定实现 commit。
- 「guard 值独立进入缓存 key」的隔离证据未取得；如需证明须控制 FX 图与其他变量的专门测试或实现级证据。
- 本修订只处理 B16-C01–C05 及其同步；审阅报告「声明的未覆盖项」（ROCm 10.1.0 兼容矩阵、HIP graphs docs-10.1.0/ROCprofiler-SDK 页、CANN/TorchAir 页组、0ab462c 全 tag 祖先比较、来源历史增量）不在本轮范围，仍按报告保留为未验收子项。
- 发现修订完成不等于审阅通过；审阅通过也不等于硬件验证通过。

---

# 第二轮（定向复核后）

修订日期：2026-10-09。修订者：撰写子代理（非 gpt-6.1-sol）。依据：`docs/research/batch-16-codex-recheck.md`（复核结论：C01/C02/C04 CLOSED；C03、C05 OPEN；新增 B16-C06（P2）、B16-C07（P3））。本轮只处理 C06（含 C03 关联）、C05 剩余差距、C07；CLOSED 三项未动。修订前按报告精确上游定位重开核对全部新证据（逐条见下）；未执行任何编译、图捕获或设备代码；draft 与 verification 语义不变。

## B16-C06 + B16-C03 剩余（P2）缓存组件映射纠正

**修改位置**

- `knowledge/02-software-stack/operators-compilers-and-graphs.md` 组成项（原 125 行）整条重写：撤销第一轮「`InductorCache` 非 2.6」判定——教程 `InductorCache` 定义即「FXGraphCache 与 Triton cache 的组合」，是概念名而非同名 Python 类存在性声明；补入 2.6 实现映射（TritonBundler 生命周期、compile_fx cache-miss 保存路径、codecache 命中恢复路径、开关与默认值）；新增 Triton 三层缓存区分（`TritonCodeCache` / Triton 编译器自身产物缓存 / TritonBundler 打包）；Mega-Cache API 保留「非 2.6」标注（该判定复核确认正确）。
- `knowledge/02-software-stack/gpu-op-graph-failure-triage.md` 编译缓存观测行（原 128 行）：组件列表改为「……与 FXGraph+Triton 产物打包（TritonBundler，教程称 InductorCache——组合概念，2.6 已有实现映射）」；边界列补三层 Triton 缓存区分指向机制文。
- `docs/research/batch-16-operators-compilers-sources.md` 组成行（24 行）与「缺口与冲突」条目（121 行）：同步改写并如实记录「第一轮曾以无同名类判非 2.6，属误判，已撤销」。
- `docs/research/batch-16-gpu-op-graph-triage-sources.md` 编译缓存身份行（17 行）：同步改写。
- `sources/registry.yaml` `src.pytorch.inductor-cache-sources-v2.6.0` 条目：路径清单补 triton_bundler.py 与 compile_fx.py；notes 补 TritonBundler/保存恢复路径/开关默认值/TritonCodeCache 层次区分，并记录撤销理由；`src.pytorch.compile-caching-tutorials-2026-10-09` 条目组件清单同步。
- 本文第一轮 C03 节加注撤销说明（见上）。

**依据（重开核对，v2.6.0 @1eba9b3）**

- `torch/_inductor/triton_bundler.py` L63 `class TritonBundler`：docstring 自述「notes each time we compile a triton kernel. When collect is called, converts all the previously noted kernels and their artifacts into a structured bytes blob…read_and_emit is called when a cache entry is read」——记录 kernel、收集产物、读取时恢复，属实。
- `torch/_inductor/compile_fx.py` L679 起 cache-miss 分支（注释 "CACHE MISS: Compile the graph and save to cache"）：L683 `TritonBundler.begin_compile()` → L695 `TritonBundler.collect()` → L696 `set_triton_bundle(triton_bundle)`，随后保存 FXGraph 缓存。
- `torch/_inductor/codecache.py` L1076：命中读取时 `if bundle := graph._triton_bundle:` → `TritonBundler.read_and_emit(bundle)`。
- `torch/_inductor/config.py` L23–27：`bundle_triton_into_fx_graph_cache_default()` 经 `get_tristate_env("TORCHINDUCTOR_BUNDLE_TRITON_INTO_FX_GRAPH_CACHE", True if not is_fbcode() else None)`——OSS 环境变量未覆盖时默认 **True**；`triton_bundler.py` L86 `is_enabled()` 首查 `force_disable_caches`——实际路径受缓存启用/禁用开关控制，其内部 OSS fallback 分支（config 为 None 时 return False）在 OSS 默认 True 下不会触发，不得误读为默认关闭。
- `torch/_inductor/codecache.py` L2820 `TritonCodeCache.load(kernel_name, source_code)` → `_module_to_triton_kernel(PyCodeCache.load(source_code), ...)`——加载生成 的 Python kernel 模块，**不是** cubin 编译产物缓存；Triton 编译产物缓存属 Triton 仓库 compiler.py 自身路径，PyTorch 侧打包属 TritonBundler。
- 教程 @8a5c6f1 Modular caching 节：`InductorCache: A bundle of FXGraphCache and Triton cache`——组合定义，非类存在性声明。

## B16-C05 剩余（P2）冷缓存两维度

**修改位置**

- `knowledge/02-software-stack/operators-compilers-and-graphs.md`「落盘与开关」（127 行）与「对照方法·编译缓存身份」操作含义（231 行）：「清空的缓存目录**或**新进程」改为两个独立维度——其一处理进程内状态（新进程或进程内重置，说明方式），其二使测量范围内相关持久化缓存（Inductor/Triton/远程）处于**已说明的冷状态**（记录实际 Inductor/Triton 目录、远程缓存处理方式与清理范围，保留命中/未命中证据）；明确「只重启进程而保留磁盘缓存＝『新进程启动』，不能称『冷缓存启动』」（FXGraphCache 按 key 从磁盘/远程读候选、Triton 编译器读自身缓存元数据直接返回产物）。
- `knowledge/02-software-stack/gpu-op-graph-failure-triage.md` 对照矩阵第 3 条（187 行）与恢复确认第 4 条（188 行）：同步两维度口径；第 4 条补「即使换新进程，保留的持久化缓存仍可能命中」。
- `sources/registry.yaml` L3109（`src.pytorch.compile-caching-tutorials-2026-10-09` notes）：删除「`TORCHINDUCTOR_FORCE_DISABLE_CACHES=1` 全禁（冷启动计时）」口径，改为「教程按全禁口径用于冷启动计时；v2.6.0 config.py L90–91 实为 Inductor 层缓存限定——非全栈冷启动，也≠缓存开启但为空的冷启动条件，冷缓存测量须进程内状态与持久化缓存两个维度分别处理」。
- `docs/research/batch-16-operators-compilers-sources.md` 缺口条目（123 行）：补两维度口径与「换新进程不消除持久化缓存命中」依据。
- 本文第一轮 C05 节（82–83 行）加注「或→两维度」的更正说明。

**依据（重开核对）**

- `torch/_inductor/codecache.py` L1000 起 `_lookup_graph`：local 子目录 + remote 按 key 读取候选——持久化缓存跨进程可命中。
- `torch/_inductor/runtime/cache_dir_utils.py` `triton_cache_dir`：显式 `TRITON_CACHE_DIR` 优先，不随 Inductor 目录替换。
- Triton `python/triton/compiler/compiler.py` L250 附近：元数据存在且未启用 always_compile 时直接命中返回。
- `torch/_inductor/config.py` L90：开关声明范围是 Inductor 层。

## B16-C07（P3）Triton CI pin 取证链

**修改位置**

- `sources/registry.yaml` `src.triton.compiler-3-2-0-35c6c7c6` 条目：revision 与 notes 更正取证链——PyTorch v2.6.0（commit 1eba9b3）`.ci/docker/ci_commit_pins/triton.txt` 第 1 行内容即 `35c6c7c6284582b3f41c71c150e11b517acf074a`，是 CI commit pin 的**直接记录**，非仅凭版本字符串推断；第一轮「v2.6.0 钉的是版本号非完整 commit」表述有误，已更正（`.ci/docker/triton_version.txt` 钉 3.2.0 亦属实，两者并存）。范围限定保留：证明 CI 源码 pin 关联，不自动证明所有 PyTorch/ROCm wheel 或本地安装使用同一 Triton commit。
- 本文第一轮 C05 依据节（92 行）加注更正说明。

**依据（重开核对）**

- `https://raw.githubusercontent.com/pytorch/pytorch/1eba9b3aa3c43f86f4a2c807ac8e12c4a7767340/.ci/docker/ci_commit_pins/triton.txt`（2026-10-09 取回）：第 1 行恰为 `35c6c7c6284582b3f41c71c150e11b517acf074a`。

## 第二轮验证

- `PYTHONDONTWRITEBYTECODE=1 make check`：**PASS，80 个内容条目、280 条来源**。
- `make build`：**PASS**，重建 `build/catalog.json` 与 `build/catalog.md`。

## 第二轮保留限制

- Mega-Cache API 最低可用 PyTorch 版本仍未取得（唯一保留的非 2.6 组件项）。
- CI pin 证明范围限 CI 源码关联；wheel/本地安装的 Triton commit 一致性未取证。
- 复核报告「仍未覆盖的材料与验证」各表项不在本轮范围；发现修订完成不等于审阅通过，审阅通过也不等于硬件验证通过。
