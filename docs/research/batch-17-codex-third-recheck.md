# 第十七批第三次定向复核记录

**最新进展（2026-10-09）：[第六次定向复核](batch-17-codex-sixth-recheck.md)已完成，第五次三项修订均通过，无新增修改项；累加精度与固定实现关联仍缺证。** 本报告所列两处限定已在[第四次复核](batch-17-codex-fourth-recheck.md)通过，不重开；累计仍为 12 项 CLOSED、1 项 P2 OPEN（C08），以下保留第三次输入与当时判定。

复核日期：2026-10-09（Asia/Shanghai）。**结论：暂不通过。本轮 B17-C11 CLOSED，B17-C08 仍 OPEN（P2）；累计 13 项发现中 12 项 CLOSED、1 项 OPEN。** 前两次复核关闭的十一项不重新打开，不以 autocast 注册策略代替算子计算/累加精度证据。

依据：[第二次定向复核及关闭条件](batch-17-codex-rerecheck.md)、[第三轮修订记录](batch-17-review-fixes.md)、[完整覆盖路线图](../full-coverage-roadmap.md)、[T02-08–T02-11 验收清单](../../plans/full-coverage-backlog.yaml)及[批次审阅约定](../authoring-guide.md#7-批次审阅约定)。

执行者为初审及前两次复核的同一 Codex 主助手，与正文编写者分开；未派发子代理。本轮未改知识正文、四份作者研究记录、来源登记或 backlog。用户约定模型/effort 为 `gpt-6.1-sol / xhigh`；沿用此前披露：本会话没有可独立核验的实际运行标识，不把约定当作已经确认的执行元数据。

## 输入与取证范围

| 输入 | 第三次复核 SHA-256 |
|---|---|
| [GPU 内存正文](../../knowledge/02-software-stack/gpu-memory-oom-evidence.md) | `d841a8e780f3c8e28b0faf2815903e970ba746bb27caa116da74dd9f1e4dfbdb` |
| [精度正文](../../knowledge/02-software-stack/dtype-layout-and-precision-semantics.md) | `e462f69ed618577d4b8fae445754213084f5f1c6836e79997d2370fc1331a2f4` |
| [GPU 研究记录](batch-17-gpu-memory-sources.md) | `e7f5f0555223ba6ff06b7821ba7f8cb01e64a99fc4cddb6efa85ec6bd382f915` |
| [精度研究记录](batch-17-dtype-precision-sources.md) | `26d8636076b5ad7f36eeb40ed7d8f2cf9570e46a065637993fe5ddc885511275` |
| [修订记录](batch-17-review-fixes.md)（追加本次结果前） | `01d1dba061ca35a6fff4d899b4818d9aa98c3b906ce8048f1ea92a6b0a267756` |
| [来源登记](../../sources/registry.yaml)（336 项，本轮不改） | `589df7a07fbdc8ecd2535c4cecc34ab3a9e45456ae925795df8bcf70ba587105` |

重新读取 C08/C11 对应正文、两份研究修订附录、登记 notes、前次关闭条件与任务边界。框架正文、Ascend 内存正文、领域索引及另两份研究记录的输入摘要与第二次复核一致，不重做已关闭项验收。

- 重读同日独立取得的 PyTorch 固定 raw：`1eba9b3aa3c43f86f4a2c807ac8e12c4a7767340` 的 CachingDeviceAllocator.h L25–32、CUDACachingAllocator.cpp L1637–1679；沿 native 统计链核对 reset。
- 重读同日独立取得的 TorchNPU 固定 raw：`bc51ab84cc6f35c77aab1c59886e0ea43681a317` 的 FormatCastKernelNpu.cpp（287 行），本轮检查候选门控与 NPUNativeFunctions 入口体到实现的调用关系。没有验收 Python 绑定、生成 wrapper 的完整注册链或运行时分发。
- 独立取得并完整读取同 commit AutoCastOps.cpp（159 行）。网页工具返回 cache miss，普通 curl 受 DNS 限制，随后经工具授权的网络读取取得同一固定 URL；未运行下载的源码，未镜像全文入库。使用作者新增的 `src.ascend.torchnpu-autocast-ops-7.2.0` 登记，不另增来源。
- 本轮没有取得新的 CANN 逐算子计算精度/支持表，没有逐项验收 dtype-format 映射表或存储格式适用条件。AOL 简介及前轮格式样板沿用已核对范围。

## 两项关闭判定

行号为本轮输入源文件坐标。

| 发现 | 状态 | 本轮判定与定位 |
|---|---|---|
| B17-C11 — P2 | CLOSED | GPU L17 追加统计实现来源；L126 正确区分累计/事件计数归零与峰值重置到 current，允许非零起点，声明绝对高水位不能直接作为新增分配/泄漏量，并限定 native 实现。GPU 研究附录 L65–67 与登记一致，满足第二次关闭条件 |
| B17-C08 — P2 | OPEN | 精度 L99 已区分门控报错与返回 false，L101 新增有边界的 autocast 注册样板，L53/L96/L103 明确保留精度未知；但强制计算/累加精度证据仍缺。新增全文概括及候选路径的表述还需按实际注册宏/调用关系限定，见下文 |

C11 依据为 [Stat L25–32](https://github.com/pytorch/pytorch/blob/1eba9b3aa3c43f86f4a2c807ac8e12c4a7767340/c10/core/CachingDeviceAllocator.h#L25-L32) 与 [native allocator L1637–1679](https://github.com/pytorch/pytorch/blob/1eba9b3aa3c43f86f4a2c807ac8e12c4a7767340/c10/cuda/CUDACachingAllocator.cpp#L1637-L1679)：历史累计 allocated/freed 及所列事件计数归零，峰值设为当前值。已修复的窗口顺序不重复列为修改项；本次关闭源码事实和方法设计发现，不代表设备实验完成。

## B17-C08 — P2，OPEN：剩余证据与新样板边界

已核实的进展：

- [候选门控 L39–85](https://github.com/Ascend/pytorch/blob/bc51ab84cc6f35c77aab1c59886e0ea43681a317/torch_npu/csrc/aten/common/FormatCastKernelNpu.cpp#L39-L85) 确实区分 aclnn-only 缺接口报 NOT_SUPPORT、无 customize_dtype 时的三个 false 分支，以及有 customize_dtype 时的错误条件。本轮不再把这些分支概括为一律报错。
- 本轮核对的 [NPUNativeFunctions 入口体及实现 L155–284](https://github.com/Ascend/pytorch/blob/bc51ab84cc6f35c77aab1c59886e0ea43681a317/torch_npu/csrc/aten/common/FormatCastKernelNpu.cpp#L155-L284) 有同格式短路、目标格式重载中的双边 base 快径和通用转换调用；这支持有限的 C++ 实现路径说明。不同重载分支不同，不扩大为全部公开绑定/运行时链已经验收。
- [AutoCastOps.cpp](https://github.com/Ascend/pytorch/blob/bc51ab84cc6f35c77aab1c59886e0ea43681a317/torch_npu/csrc/aten/AutoCastOps.cpp) 支持四类普通 `KERNEL_PRIVATEUSEONE` 注册，以及 binary_cross_entropy 的 autocast 禁用。正文正确声明这是注册策略、不是逐算子内核计算或累加精度证据。

剩余位置：[精度正文 L99–103](../../knowledge/02-software-stack/dtype-layout-and-precision-semantics.md)、[精度研究附录 L58–59](batch-17-dtype-precision-sources.md)、转换与 autocast 两项登记 notes。

1. **强制证据仍缺。** L96/L103 的 compute dtype、累加精度和支持条件仍 unknown；autocast 归属、格式转换和 AOL 简介均不代替这些证据。作者保留 OPEN 的处理正确，不能据新增一项登记关闭 C08 或 T02-10。
2. **候选门控与当前入口不能连成已证 fallback 链。** 本次核对文件中 `MaybeUseAclnnNpuFormatCast` 和 `format_cast_impl_out_npu_aclnn` 只出现定义，L20/L113 注释说明为未来功能保留；上述入口链未调用它们。L99、研究附录及登记的“返回 false 走候选非 aclnn 路径”应明确只是在说明候选函数返回值，不能据此声称当前入口按这个布尔值切换路径。不推断整个仓库不存在其他调用。另须纠正 L99 的原文件坐标：接口缺失且无 customize_dtype 的 false 在 L70–75；L54–62 是 jit-disable、接口存在但尺寸 API 失败的分支。aclnn-only 缺接口错误完整为 L50–52。
3. **四个普通注册族不等于全文所有策略。** AutoCastOps.cpp [L128–142](https://github.com/Ascend/pytorch/blob/bc51ab84cc6f35c77aab1c59886e0ea43681a317/torch_npu/csrc/aten/AutoCastOps.cpp#L128-L142) 还通过 `KERNEL_DIFFERENT_REDISPATCH_SIGNATURE_PRIVATEUSEONE` 为 norm 三个重载注册 `fp32_append_dtype`。L101 和登记按 `KERNEL_PRIVATEUSEONE` 限定的四族说法可以成立，但研究附录“全文 159 行（四族 + 禁用）”不能当作完整策略清单。应补列第五种策略及不同宏，或明确这是普通注册宏的有限摘录，未列项不视为不存在。

关闭条件：沿用前次强制证据要求，取得至少一个版本明确、带精确官方算子正文及固定实现依据的计算精度样板，记录输入/输出 dtype、格式、硬件/接口条件和计算精度；累加精度缺证时继续单列未知及未验收子项，不能用 autocast 代替或静默缩减范围。同步修正上述候选门控/当前入口关系、原文件坐标和注册策略概括的范围，保持正文、登记与研究附录一致。未取得强制证据时 C08 继续 OPEN；本轮不要求重写已核实的格式枚举、base 定义或 C11 窗口设计。

## 累计状态与检查

| 状态 | 发现 |
|---|---|
| CLOSED（12 项） | C01、C02、C03、C04、C05、C06、C07、C09、C10、C11、C12、C13 |
| OPEN（1 项 P2） | C08 |

T02-09 对应的既有发现现已闭环，仍保留原文列明的未知项与待执行实验；不等于整个主题或所有 backend 已验证。T02-10 因 C08 继续暂不通过，不解锁依赖其完成的任务。T02-08/T02-11 沿用前两次复核范围；backlog 与主题覆盖状态不调整，条目保持 `draft / source_checked`。

独立 `make check` / `make build` 均 PASS：83 content entries / 336 sources。本轮只新增第三次复核报告、更新审阅状态及追加修订记录结果；未改 `src/kb/`，未新增代码测试。结构检查不证明技术正确性、远程内容有效或硬件验证。未安装软件包，未执行设备/集群、OOM、数值、梯度、通信或性能实验；未重新全量审查许可。
