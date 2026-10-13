# 第十七批第二次定向复核记录

**最新进展（2026-10-09）：[第六次定向复核](batch-17-codex-sixth-recheck.md)已完成，第五次三项修订均通过，无新增修改项；累加精度与固定实现关联仍缺证，累计 12 项 CLOSED、1 项 P2 OPEN（C08）。** 以下保留第二次复核输入、证据及当时判定；最新条件以第六次报告为准，已通过项不重开，Batch 17 仍暂不通过。

复核日期：2026-10-09（Asia/Shanghai）。**结论：暂不通过。本轮关闭 B17-C01、C03、C10；B17-C08、C11 仍 OPEN（均为 P2）。累计 13 项发现中 11 项 CLOSED、2 项 OPEN。** 第一次复核已关闭的八项不重新打开，不将新取得的转换证据扩成算子精度验收。

依据：[初审](batch-17-codex-review.md)、[第一次定向复核及剩余关闭条件](batch-17-codex-recheck.md)、[第二轮修订记录](batch-17-review-fixes.md)、[完整覆盖路线图](../full-coverage-roadmap.md)、[T02-08–T02-11 清单](../../plans/full-coverage-backlog.yaml)及[批次审阅约定](../authoring-guide.md#7-批次审阅约定)。

执行者为初审及第一次复核的同一 Codex 主助手，与正文编写者分开；未派发子代理。本轮未改知识正文和四份作者研究记录。用户约定模型/effort 为 `gpt-6.1-sol / xhigh`；沿用此前披露：本会话没有可独立核验的实际运行标识，不能把约定当作已经确认的执行元数据。

## 范围、输入与取证

读取三篇第二轮修订正文、四份研究记录及修订附录、修订/来源审计、相关登记和验收条件。Ascend 内存正文与领域索引相对第一次复核输入没有变化，不重新验收旧 allocator/workspace 全文。只判定 C01/C03/C08/C10/C11 剩余关闭条件及本轮新增主张。

| 输入 | 本轮复核 SHA-256 |
|---|---|
| [框架正文](../../knowledge/02-software-stack/framework-backend-adaptation.md) | `a09ceee65f9eaa667964bf56a649eb0f80dc236766bf58150f867f0c19c425b2` |
| [GPU 内存正文](../../knowledge/02-software-stack/gpu-memory-oom-evidence.md) | `d980da441b4359b22273cf5f2cdb0ab5016e549c1911289a06ad55e450ad8dce` |
| [精度正文](../../knowledge/02-software-stack/dtype-layout-and-precision-semantics.md) | `9a6b4a32fcaabcfad06cb8ecf03baddb9f247ad27f6a8027d86ed1b26480eaa5` |
| [Ascend 内存正文](../../knowledge/02-software-stack/ascend-memory-oom-evidence.md) | `b1c3e6cfceb9625d109a93629ce13d2ffa8205d58f17e5f2efae58155b6c2869` |
| [框架研究记录](batch-17-framework-backend-sources.md) | `378f49a01d13db8a5a898a281001eab33f0cbe7631687024d0bb3c3233e02b50` |
| [GPU 研究记录](batch-17-gpu-memory-sources.md) | `8cb427efb380ec940b33b8d62361cdfb650fd7ba8f7a0481a209b8ff55551ff6` |
| [精度研究记录](batch-17-dtype-precision-sources.md) | `a0eaefab0e977b6a3d2edbdb70fe9bb1dc5097cf4164d60054452afb29b65100` |
| [Ascend 研究记录](batch-17-ascend-transfer-sources.md) | `113773bb6234d1447af990870002be5cdfa4367d1cee24e585bdb3a01356d608` |
| [修订记录](batch-17-review-fixes.md)（追加本次结果前） | `42a8de94b3c2aa8a71c098a31501df07f9917827bca20e0528bfc93af39d0eef` |
| [来源登记](../../sources/registry.yaml)（补登本次反证前，334 项） | `c1f327cd8b4487542632be31b89ea809ced5729e8f8913c1543ee62ab82499d8` |

- 重读初审同日取得的固定 PyTorch raw 相关段落：CublasHandlePool、CUDACachingAllocator、memory.py、backend_registration.py、gradcheck.py；不把相关段落复核写成这些文件全部重新下载/运行。
- 通过用户引用的精确 raw 地址独立取得并完整读取 TorchNPU `bc51ab84cc6f35c77aab1c59886e0ea43681a317` 的 FormatCastHelper.h（29 行）和 FormatCastKernelNpu.cpp（287 行）；读取同 commit FormatHelper.cpp L96–126 的 base 判定。格式 info/dtype 映射表和 Helper 具体实现未逐项验收。
- 对 reset 语义补充取得 PyTorch `1eba9b3aa3c43f86f4a2c807ac8e12c4a7767340` 的 CUDACachingAllocator.h 与 CachingDeviceAllocator.h，沿 native 统计调用链核对 `Stat::reset_peak`。新登记 `src.pytorch.caching-device-allocator-stats-v2.6.0`，334→335 sources；原登记未改写。
- 网页工具未能取得本轮三个 TorchNPU raw 文件，改用 curl 访问同一固定 URL；临时文件不镜像到仓库。AOL 简介沿用同日已取得静态正文，未重新取得逐算子支持/精度表。
- 重建并检查 `build/catalog.json` 的 GPU summary 已是新用途/可见性口径。Markdown catalog 只列标题等导航字段，但 **JSON catalog 仍包含 summary**；不能把“catalog 仅列标题”作为不用同步 summary 的理由。本轮实际 summary 已改正确，不构成开放项。

## 五项关闭判定

行号为本轮输入源文件坐标。

| 发现 | 状态 | 本轮判定与定位 |
|---|---|---|
| B17-C01 — P2 | CLOSED | GPU L27 摘要改用途/可见性；L117–118 分 graph 活跃量与保留高水位，声明同口径/窗口、保留可含非活跃块；L121 继续并列不相加。修订附录同步，重建 JSON summary 确认无旧“独立账户”断言 |
| B17-C03 — P2 | CLOSED | GPU L115 与 `src.pytorch.torch-cuda-memory-source-v2.6.0` notes 均区分 active backend 与 env 请求快照，明确不代表全部选项生效值；符合 [memory.py L925–934](https://github.com/pytorch/pytorch/blob/1eba9b3aa3c43f86f4a2c807ac8e12c4a7767340/torch/cuda/memory.py#L925-L934) |
| B17-C08 — P2 | OPEN，继续补证 | 精度 L39、L47–51 已同步简介/有限核对范围，L97 补转换文件；L94、L100 的算子计算/累加精度等强制子项仍未验收，且门控错误条件还需收紧，见下文 |
| B17-C10 — P2 | CLOSED，限待执行设计 | 框架 L87–98 修正 Storage RuntimeError、三种状态分离、标准算子前后向、生产/消费/event 参考、collective/rank/归约预期、性能基线/稳态/分母及方法不适用分支。符合原剩余设计条件，不代表已跑通 |
| B17-C11 — P2 | OPEN，窗口设计已修复 | GPU L125 已规定清理/保留、同步、起点、终点在再 reset 前保存与同阶段基线；但末尾将历史计数与峰值一并称为归零，与 native 固定实现冲突，见下文 |

C01 依据为 [cuBLAS workspace L166–167](https://github.com/pytorch/pytorch/blob/1eba9b3aa3c43f86f4a2c807ac8e12c4a7767340/aten/src/ATen/cuda/CublasHandlePool.cpp#L166-L167)、[活跃统计 L1443–1448](https://github.com/pytorch/pytorch/blob/1eba9b3aa3c43f86f4a2c807ac8e12c4a7767340/c10/cuda/CUDACachingAllocator.cpp#L1443-L1448) 与 [graph 保留统计 L2775–2784](https://github.com/pytorch/pytorch/blob/1eba9b3aa3c43f86f4a2c807ac8e12c4a7767340/c10/cuda/CUDACachingAllocator.cpp#L2775-L2784)。这里只核对统计类型和归属关系，未取得私有池高水位的实际测量值。

C10 的失败类型与 [Storage 转移 L281–289](https://github.com/pytorch/pytorch/blob/1eba9b3aa3c43f86f4a2c807ac8e12c4a7767340/torch/utils/backend_registration.py#L281-L289) 一致；梯度方法前提对照 [gradcheck L1987–2004](https://github.com/pytorch/pytorch/blob/1eba9b3aa3c43f86f4a2c807ac8e12c4a7767340/torch/autograd/gradcheck.py#L1987-L2004)。执行时仍须固定实际版本、输入、collective/rank 和计时参数。缺依赖对照能否复现差异属于实验结果；未出现差异不能反推缺依赖安全。关闭的是方法设计缺口，不是后端、算子或性能验收。

## 剩余开放条件

### B17-C08 — P2，OPEN：转换样板取得，算子精度强制子项仍未完成

已验收补充：

- [FormatCastHelper.h L11–23](https://github.com/Ascend/pytorch/blob/bc51ab84cc6f35c77aab1c59886e0ea43681a317/torch_npu/csrc/aten/common/FormatCastHelper.h#L11-L23) 是接口声明，不作为已跑通转换的证据。
- [FormatCastKernelNpu.cpp](https://github.com/Ascend/pytorch/blob/bc51ab84cc6f35c77aab1c59886e0ea43681a317/torch_npu/csrc/aten/common/FormatCastKernelNpu.cpp) 有候选 aclnn 路径、非 aclnn 路径和物理排布/view 元数据注释。L35–37 的 dtype 转换调用存在，具体映射未验收。
- [FormatHelper.cpp L96–126](https://github.com/Ascend/pytorch/blob/bc51ab84cc6f35c77aab1c59886e0ea43681a317/torch_npu/csrc/framework/FormatHelper.cpp#L96-L126) 支持按 info 查 base、未知格式报错和 base 等于自身的判定。
- AOL 登记与 verification notes 已同步“简介取得、支持表未取得”，前次元数据矛盾已消除。

剩余位置：精度 L94、L97、L100；转换登记 `src.ascend.torchnpu-format-cast-7.2.0` notes。

1. 仍没有有限算子的 compute/累加精度与官方支持条件样板。转换格式不等于计算精度；作者正确写 unknown，也正确保留必交子项 OPEN。因此本轮不能关闭 C08 或 T02-10。
2. L97 将门控“不满足”简写成 NOT_SUPPORT，范围过宽。固定代码 L39–83 中：aclnn-only 且缺少接口会报错；非 aclnn-only、jit-disable 分支在接口缺失且无 customize_dtype 时返回 false；计算尺寸失败且无 customize_dtype 时也可返回 false；jit 未禁用且无 customize_dtype 同样返回 false，而非一律报 NOT_SUPPORT。带 customize_dtype 的若干分支另有报错条件。该函数的定义存在还不证明已验收公开入口到它的完整调用链。

关闭条件：补一个版本明确、有精确官方算子正文及固定实现依据的计算精度样板，写清 dtype/format/硬件条件；缺失累加精度继续单列未知及未验收子项，不由转换代码代替。把转换门控写成分支条件，区分返回 false 的候选非 aclnn 路径与明确 NOT_SUPPORT 条件；同步正文、登记和附录，保留完整调用链未核验范围。未取得强制证据时继续 OPEN，未经用户调整不缩减范围。

### B17-C11 — P2，OPEN：峰值 reset 不归零

本轮有序窗口和存活对象处理已经满足第一次复核的设计要求；不再要求重写该顺序。剩余位置仅为 GPU L125 末尾 reset 解释及相应记录中的同类概括。

[allocator L1637–1679](https://github.com/pytorch/pytorch/blob/1eba9b3aa3c43f86f4a2c807ac8e12c4a7767340/c10/cuda/CUDACachingAllocator.cpp#L1637-L1679) 将事件计数归零，但峰值走 `Stat::reset_peak()`；[CachingDeviceAllocator.h L25–32](https://github.com/pytorch/pytorch/blob/1eba9b3aa3c43f86f4a2c807ac8e12c4a7767340/c10/core/CachingDeviceAllocator.h#L25-L32) 的累计 reset 将 allocated/freed 归零，峰值 reset 则是 `peak = current`。因此若开始窗口仍保留模型/缓存，峰值起点可以非零；这并非 reset 失败，也不是本窗口新增分配量。这里是固定 native 统计实现，不推为所有 backend 的保证。

关闭条件：将解释改为“累计量/事件计数按所列键归零，峰值重置到当前值”，明确起点快照允许非零，窗口 peak 是绝对高水位，不能直接作为新增分配或泄漏量；同步修订附录/记录。本轮不因未做设备实验阻止关闭，所需只是纠正这个可直接核对的源码事实。

## 累计状态与任务边界

| 状态 | 发现 |
|---|---|
| CLOSED（11 项） | C01、C02、C03、C04、C05、C06、C07、C09、C10、C12、C13 |
| OPEN（2 项 P2） | C08、C11 |

- T02-08：原 C09/C10 设计发现关闭，未将未知配套、TorchNPU 现有用例树或实际执行能力补作通过。
- T02-09：C01/C03 关闭，C11 仍需纠正峰值解释，暂不通过。
- T02-10：C08 尚未完成强制精度证据，暂不通过，不解锁依赖其完成的任务。
- T02-11：C02/C12 沿用第一次复核关闭；0088/0089、旧 allocator/workspace 与接口支持边界保留，非本轮全量验收。待执行验证设计与实机结果仍分别统计。

不更新 backlog 为 done，不关闭主题覆盖缺口，条目保持 `draft` 与限定 `source_checked`。两个开放项沿用原 ID/P2，未另增发现 ID。

## 检查结果与限制

补登前独立 `make check` / `make build`：均 PASS，83 content entries / 334 sources；补登 native 统计反证后均 PASS，83 content entries / 335 sources。生成 catalog，不证明技术正确性、远程内容有效或发现关闭。

未修改 `src/kb/`，未新增代码测试；未执行设备/集群代码，未安装 wheel、跑 OOM、数值、梯度、通信或性能实验。新增源码仅在临时目录读取，未镜像全文入库。许可沿用同 commit 根许可登记，未全量审查网站或第三方文件许可。后续只需对 C08/C11 的实际修订定向复核；历史关闭项不重复列为待办。
