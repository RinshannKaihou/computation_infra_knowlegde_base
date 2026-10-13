# 第十七批第四次定向复核记录

**最新进展（2026-10-09）：[第六次定向复核](batch-17-codex-sixth-recheck.md)已完成。** 第五次三项修订均通过，无新增修改项；累加精度与固定实现关联缺证，C08 继续 OPEN（P2），累计 12 项关闭/1 项开放。以下保留第四次输入与当时判定，已通过的两处限定不重开。

复核日期：2026-10-09（Asia/Shanghai）。**本轮两处表述限定均通过定向复核，无新增修改项。B17-C08 仍 OPEN（P2），剩余原因仅为原有的逐算子计算/累加精度强制证据未取得；累计 12 项 CLOSED、1 项 OPEN，Batch 17 暂不通过。** 已通过的限定不再列为待办，前轮关闭项不重新打开。

依据：[第三次定向复核及关闭条件](batch-17-codex-third-recheck.md)、[第四轮修订记录](batch-17-review-fixes.md)、[完整覆盖路线图](../full-coverage-roadmap.md)、[T02-10 验收清单](../../plans/full-coverage-backlog.yaml)与[批次审阅约定](../authoring-guide.md#7-批次审阅约定)。执行者为初审及前三次复核的同一 Codex 主助手，与正文编写者分开；未派发子代理。用户约定为 `gpt-6.1-sol / xhigh`；沿用此前披露，本会话没有可独立核验的实际运行标识，不把约定写成已确认的执行元数据。

## 输入与核对范围

| 输入 | 第四次复核 SHA-256 |
|---|---|
| [精度正文](../../knowledge/02-software-stack/dtype-layout-and-precision-semantics.md) | `91328eb1ad98b77540c728c39f0aa71d0984c22b6f18ef206a17de7042168ffd` |
| [精度研究记录](batch-17-dtype-precision-sources.md) | `56267b1b76e290c2f9b5110dbb5905ba132fdfe3ebb2e24ff9d00b7aa4ae838e` |
| [修订记录](batch-17-review-fixes.md)（追加本次结果前） | `f1250c301da20da9a08a3594152f36ad3a5cabdff82b5f716f8e6c7432f12dd6` |
| [来源登记](../../sources/registry.yaml)（336 项，本轮不改） | `18858b2de1d7177749ff3c783b0eced6c4abfee6a7ea89bbae4e6b8724d6804a` |

重读正文 L53、L96–103、两项登记 notes 和第四轮研究附录。复用本会话同日独立取得的 TorchNPU 固定 raw（commit `bc51ab84cc6f35c77aab1c59886e0ea43681a317`），重新核对 FormatCastKernelNpu.cpp 的候选函数、相关入口体以及 AutoCastOps.cpp 的注册宏。没有重新下载文件，没有新增来源，也没有将作者的“实测”记为设备代码执行。

GPU、框架、Ascend 内存正文、领域索引、另外三份研究记录及 backlog 的摘要与第三次复核输入一致。本轮不重做这些已关闭项的技术验收。

## C08 两处限定判定

| 第三次复核的待修订限定 | 本轮判定 | 当前定位与依据 |
|---|---|---|
| 候选门控/入口关系及分支坐标 | 已满足 | 精度 L99、L53；第四轮研究附录及 `src.ascend.torchnpu-format-cast-7.2.0` notes 均区分候选函数返回契约与已查入口体。NOT_SUPPORT 为 L50–52，尺寸失败 false 为 L54–62，缺接口 false 为 L70–75；范围限所查重载，不外推全仓库或全部绑定链 |
| autocast 注册策略范围 | 已满足 | 精度 L101、L53；第四轮研究附录及 `src.ascend.torchnpu-autocast-ops-7.2.0` notes 均补不同宏的 `fp32_append_dtype`，将“四族”限定为普通宏，不当作全文全部策略 |

第一项对照 [FormatCastKernelNpu.cpp L20–85](https://github.com/Ascend/pytorch/blob/bc51ab84cc6f35c77aab1c59886e0ea43681a317/torch_npu/csrc/aten/common/FormatCastKernelNpu.cpp#L20-L85) 与 [L155–284 的入口体](https://github.com/Ascend/pytorch/blob/bc51ab84cc6f35c77aab1c59886e0ea43681a317/torch_npu/csrc/aten/common/FormatCastKernelNpu.cpp#L155-L284)。所核对入口体未调用该候选函数，文件注释为未来功能保留；正文已撤去当前入口按候选布尔值切换路径的暗示。不同入口重载的短路/base/通用分支只在本次所查范围内采信。

第二项对照 [AutoCastOps.cpp L128–142](https://github.com/Ascend/pytorch/blob/bc51ab84cc6f35c77aab1c59886e0ea43681a317/torch_npu/csrc/aten/AutoCastOps.cpp#L128-L142)：norm 三个重载通过 `KERNEL_DIFFERENT_REDISPATCH_SIGNATURE_PRIVATEUSEONE` 注册 `fp32_append_dtype`，与四类普通 `KERNEL_PRIVATEUSEONE` 注册分别说明。正文继续明确这是 autocast 注册策略，不是逐算子内核计算/累加精度证据。

研究记录前段保留各轮历史，第四轮附录已纠正第三轮旧概括；不将历史文字另计新发现。两处限定作为 C08 内的修订要求判为已满足，不增加发现 ID，也不将整个 C08 误记 CLOSED。

## 唯一剩余开放条件

**B17-C08 — P2，OPEN。** 位置为精度正文 L53、L96、L103 的未覆盖范围与 unknown 清单。逐算子计算/累加精度及支持条件仍缺证；本轮的门控关系、格式转换、autocast 策略和 AOL 简介均不替代该强制子项。作者保持 unknown / OPEN 的处理符合路线图，不静默缩减范围。

关闭条件沿用第三次报告：取得版本明确、带精确官方算子正文及固定实现依据的计算精度样板，记录输入/输出 dtype、格式、硬件/接口条件及计算精度。累加精度缺证时继续单列未知及未验收子项；必交证据未齐时 C08 继续 OPEN。后续只定向复核实际补入的强制证据及其正文/登记/研究记录同步，不重复要求修改本轮已通过的两处限定。

累计 CLOSED：C01、C02、C03、C04、C05、C06、C07、C09、C10、C11、C12、C13（12 项）；OPEN：C08（1 项 P2）。T02-10 继续暂不通过，不解锁依赖其完成的任务；其他任务沿用原复核边界。条目保持 `draft / source_checked`，backlog 与主题覆盖状态不调整。

独立 `make check` / `make build` 均 PASS：83 content entries / 336 sources。本轮仅新增第四次复核报告、更新审阅状态并追加修订结果，未改知识正文、四份作者研究记录、来源登记或 `src/kb/`；未新增代码测试、未运行设备/集群或数值实验、未全量重审许可。结构检查不证明技术正确性或硬件验证。
