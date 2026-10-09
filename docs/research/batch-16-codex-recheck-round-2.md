# 第十六批定向复核记录·第二轮（gpt-6.1-sol / xhigh）

复核日期：2026-10-09。复核者：Codex 会话（resume），模型 gpt-6.1-sol / xhigh。复核对象：B16-C03/C05/C06/C07 的第二轮修订。**最终结论：通过——B16-C01–C07 全部关闭，无新增发现，保留证据边界。** 复核输出全文照录如下。

---
# Batch 16 第二轮定向复核报告

- **复核日期**：2026-10-09（Asia/Shanghai）。
- **模型 / effort**：用户约定为 `gpt-6.1-sol / xhigh`。本会话没有可核验的实际运行模型及 effort 元数据，因此如实记录约定，不将其作为实际执行配置的证明。
- **最终结论**：**通过——限 Batch 16 已审阅范围及发现修订闭环。** C01–C07 全部 CLOSED；本轮未发现需要新增为 B16-C08 的问题。初审未覆盖子项仍不计为已独立验收。

## 一、逐项判定

| 发现 | 判定 | 关闭依据 |
|---|---|---|
| **B16-C03 — P2** | **CLOSED** | Mega-Cache 两个 API 继续明确标为“不在 v2.6.0 固定源码中”；同教程其他缓存组件的甄别已由 C06 修订补齐，不再因缺少同名类而否定对应机制。 |
| **B16-C05 — P2** | **CLOSED** | 两篇正文已将进程内状态与持久化缓存冷状态设为必须同时处理的两个维度，明确“新进程启动≠冷缓存启动”；既有 registry 记录已补入 Inductor 层限定，不再将禁用开关直接作为全栈冷缓存证明。 |
| **B16-C06 — P2** | **CLOSED** | “InductorCache 非 2.6”断言已撤销；补齐 bundling 保存／恢复路径、OSS 默认 True 与 `is_enabled()` 条件；三个 Triton 相关缓存层次已分清，并同步到研究记录、registry 和修订摘要。 |
| **B16-C07 — P3** | **CLOSED** | 已补记 `.ci/docker/ci_commit_pins/triton.txt:1` 的完整 commit 直接记录，改正“只钉版本号”的取证链描述，并保留 CI pin 不代表所有 wheel／本地安装的范围限定。 |

**C01、C02、C04 保持此前 CLOSED，本轮不重新打开这些发现。**

## 二、关键核对结果

本轮重新读取的 PyTorch 固定源码均为：

`1eba9b3aa3c43f86f4a2c807ac8e12c4a7767340`

### C03／C06：组件映射与版本隔离正确

`knowledge/02-software-stack/operators-compilers-and-graphs.md:125` 已正确区分教程概念名与具体类名，并补齐：

- `torch/_inductor/triton_bundler.py:63`：记录 kernel、收集产物及读取恢复的生命周期。
- `torch/_inductor/compile_fx.py:679`：cache-miss 分支执行 `begin_compile()`、`collect()`、`set_triton_bundle()`，随后保存 FXGraph 缓存。
- `torch/_inductor/codecache.py:1076`：读取 `graph._triton_bundle`，调用 `read_and_emit()` 恢复产物。

这些实现支持“2.6 已有 FXGraph/Triton 产物打包机制”的修订结论；教程的 `InductorCache` 本身是组合概念，不能用同名类是否存在来判断能力。citeturn447527view0turn526302view0turn245309view0turn447527view1

默认值与条件也已对齐：`config.py:23` 给 OSS、环境变量未覆盖时的 bundling 默认值 **True**；`is_enabled()` 先处理强制禁用，再返回非 None 的配置值。其后的 OSS fallback 不能读成默认关闭，正文也没有把默认值扩大为每次运行必然执行打包。citeturn526302view0turn526302view1

三层缓存现在分别描述为：

- `TritonCodeCache`：通过 `PyCodeCache.load` 加载生成的 Python kernel 模块；
- Triton 编译器自身缓存：按编译身份读取元数据和编译产物，具有独立命中分支；
- `TritonBundler`：PyTorch 侧收集、打包及恢复这些产物。

没有继续把 Python 模块缓存当作 cubin 等编译产物缓存的完整实现。citeturn245309view1turn542835view1turn526302view0

Mega-Cache API 的版本隔离仍然保留：固定 `torch/compiler/__init__.py` 没有 `save_cache_artifacts()`／`load_cache_artifacts()`；较新教程的总前提不能证明这两个 API 在 2.6 可用。最低可用版本未取得的限制可以继续保留。citeturn799234view1turn447527view0

同步位置已核对，包括：

- `knowledge/02-software-stack/gpu-op-graph-failure-triage.md:128`
- `docs/research/batch-16-operators-compilers-sources.md:24`
- `docs/research/batch-16-operators-compilers-sources.md:121`
- `docs/research/batch-16-gpu-op-graph-triage-sources.md:17`
- `sources/registry.yaml:3165`
- `docs/research/batch-16-review-fixes.md:120`

### C05：冷缓存条件已落实为两个维度

`operators-compilers-and-graphs.md:127`、`operators-compilers-and-graphs.md:231`、`gpu-op-graph-failure-triage.md:187`、`gpu-op-graph-failure-triage.md:188` 均已要求：

**处理进程内状态，并使测量范围内相关持久化缓存处于已说明的冷状态。**

这与实现一致：FXGraphCache 可以读取磁盘／远程候选，Triton 可以直接命中已缓存产物；只换新进程不会自动消除这些命中。citeturn447527view1turn542835view1turn799234view0

`sources/registry.yaml:3109` 已撤销原“全禁（冷启动计时）”作为操作结论的口径，明确开关限于 Inductor 缓存，且禁用缓存不等于“缓存机制开启但为空”的实验条件。研究记录及第二轮摘要同步一致。上游教程本身也明确说的是 **all Inductor caching**，不能外推为全栈缓存禁用。citeturn526302view1turn799234view0

### C07：CI pin 取证链已补齐

独立重取 `.ci/docker/ci_commit_pins/triton.txt:1`，内容确为：

`35c6c7c6284582b3f41c71c150e11b517acf074a`

`sources/registry.yaml:3171`、`sources/registry.yaml:3179` 与 `docs/research/batch-16-review-fixes.md:157` 已把关联依据改为该直接 CI pin，并保留“不能自动证明所有 PyTorch/ROCm wheel 或本地安装使用同一 commit”的限定。citeturn542835view0

修订记录第一轮的旧表述仍作为历史保留，但已附明确撤销／更正说明，并指向第二轮现行结论；不再将这些已注明失效的历史表述重复报为未修复问题。

## 三、结构检查

独立执行：

`PYTHONDONTWRITEBYTECODE=1 make check`

结果：**PASS，80 个内容条目、280 条来源**。

两篇正文仍为 `draft`；机制文保持 `source_checked`，诊断文保持 `not_verified`，没有将源码阅读、审阅或结构检查改写成设备实测。本轮未修改文件、未运行 `make build`；编写者记录的 build PASS 不作为本轮独立执行结果。

## 四、保留的证据边界与未核对项

**本轮关闭的是技术发现，不是补齐所有平台与实验取证。** 以下边界继续保留：

- Mega-Cache API 最低可用版本、guard 值独立进入缓存 key 的隔离证据仍未取得。
- CI pin 只证明固定源码关联；wheel／本地安装的实际 Triton commit 未核对。
- 文档样板不是实测；CUDA 文档及接口不能直接外推 HIP/ROCm 适用性。
- AMD 未取证设备／产品线／虚拟化组合不得外推；CANN 固定文档树、编译器职责缺口及 HDK 交集 blocked 等原有限制不因本轮通过而解除。

初审声明的以下未覆盖项，本轮仍未完成独立核对：

| 未覆盖项 | 保留状态 |
|---|---|
| ROCm 10.1.0 兼容矩阵的 MI300X 条件块、14 个驱动版本、固件及虚拟化字段 | 未完成逐项核对 |
| HIP graphs docs-10.1.0、ROCprofiler-SDK docs-7.14.0 指定页 | 未完成完整核对 |
| CANN/TorchAir 页组的包清单、HCCL、aclnn、aclmdlRI、缓存环境变量及全部 720 指南 | 未完成全量核对 |
| 全部 PyTorch 2.6 HTML 章节逐句对照；`0ab462c` 对全部所列 release tag 的祖先比较 | 未完成 |
| “210→275，再补 2 条”的来源历史变更链 | 未重构；当前 280 条已确认 |
| 硬件复现、性能测量、wheel 安装、包内容检查及本轮独立 build | 未执行 |

## 最终结论

**通过。Batch 16 已记录的 B16-C01–C07 全部关闭，本轮无新增发现。**

此结论代表**已审阅范围内的文档技术审阅及修订闭环通过**，不代表全部 backlog 验收子项、全部上游页面或硬件验证已经完成；上述未核对子项必须继续保留为未验收状态。
