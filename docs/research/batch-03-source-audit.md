# 第三批来源与交付记录

日期：2026-09-29。范围：F07、F08、F17、F18，以及并行补充的 F10。写作子代理使用 `gpt-5.6-sol / high`，F10 由主任务补充。按用户要求，集成后使用 `gpt-6-astra / xhigh` 独立验证审阅，处理发现后才将本轮任务标为完成并进入下一轮。

## 正文与来源定位

| 任务 | 正文 | 提取记录 | 核查范围 |
|---|---|---|---|
| F07 | [集合通信与 rank 进度](../../knowledge/03-communication/collectives-and-rank-progress.md) | [F07 来源](batch-03-f07-sources.md) | NCCL 2.27.5、PyTorch 2.8、CANN 8.0.RC1.alpha003 HCCL 正式接口中的参与者、次序、参数与进度 |
| F08 | [通信性能口径](../../knowledge/03-communication/bandwidth-baselines.md) | [F08 来源](batch-03-f08-sources.md) | nccl-tests 固定实现中的 size/计时/algbw/busbw/正确性；cann-hccl 固定 README 的 HCCL Test 字段 |
| F10 | [Checkpoint 持久化边界](../../knowledge/04-data-storage/checkpoint-durability.md) | [F10 来源](batch-03-f10-sources.md) | DCP 2.6、固定 FileSystemWriter、Linux fsync、固定 MindIO ACP README |
| F17 | [可靠性维度与故障域](../../knowledge/08-reliability/dimensions-and-failure-domains.md) | [可靠性来源](batch-03-reliability-sources.md) | SLI/监控/恢复方法，SuperBench 的 GPU 研究范围 |
| F18 | [证据、假设与结论](../../knowledge/08-reliability/evidence-and-hypotheses.md) | [可靠性来源](batch-03-reliability-sources.md) | 假设检验、观测边界、CPU SDC 研究与跨平台外推限制 |

本批新增十四项正式来源登记，累计三十三项。正文累计十一篇，导航/路径十三项。固定软件版本分别用于说明概念和实现，不构成它们彼此的支持矩阵；不同文章引用不同 PyTorch/CANN 版本时按各页条件解释。

## 集成时处理的问题

- 补齐所有新来源 ID，修正候选来源 YAML 中带冒号标题的引号。
- 为 F07/F08 增加互链，将新内容接入通信、数据存储和可靠性章节，以及平台/任务阅读路径。
- 将写作状态与来源核对、硬件验证分开；所有新正文仍为 `draft`。
- 明确 F10 的临时元数据与同步实现不能证明任意存储后端的端到端持久化。
- 不把 HCCL Test 字段名与 NCCL-tests 统计公式直接等同，不把 CPU SDC 发生情况写成 GPU/NPU 结论。

## 轮末审阅

状态：已完成 `gpt-6-astra / xhigh` 独立审阅及修订后的定向复核。完整过程见[独立审阅记录](batch-03-astra-review.md)，保留初审发现，不以最终通过覆盖历史。

初审发现 4 项 P2 和 3 项 P3，全部处理并经同一审阅者复核关闭：

| 发现 | 修订与核验 |
|---|---|
| NCCL 组内调用返回不保证入队 | 补 API 聚合组与 nonblocking group 的成功提交条件，更新平台表与来源范围 |
| Work 等待/完成概括过度 | 对照 v2.8.0 固定 WorkNCCL 源码区分默认 stream 依赖、CPU 等待、barrier 与异常；不把 is_completed 当成功 |
| 显示 time 与带宽分母混淆 | 以 getBw 实际使用的 deltaSec 定义分母，区分 -C、graph、-I/-K 与主表聚合 |
| 合成例跨 rank 先后无证据 | 改为同 rank、明确埋点边界下的单调时钟耗时，对跨 rank 先后保留未知 |
| 固定源码/PDF 定位偏移 | 修正 common.cu 与算子函数行号、HCCL 物理页锚点；研究记录同步 |
| HCCL 模型符号混淆 | 用 m 表示通信 byte 数，避免与 rank 数 n 混用 |
| 存储主题地图未更新 | 04.3/04.4 链接已有草稿并保留未完成部分 |

`make check` 与 `make build` 在修订后通过：24 个内容条目、33 项来源。此次未修改校验器，无需新增或运行代码回归测试。所有正文仍为 `draft/source_checked`；结构检查、模型审阅与实测分别记录。

## 未执行与后续

没有安装或运行上游软件，没有 GPU/NPU、集群、存储实验，也没有本地事故数据。示意时间线和假设示例是原创概念内容，不是生产复盘。来源许可按具体文档、代码与制品范围登记，没有引入整库统一再分发许可。

下一轮推进 F13/F14 训练状态与恢复、F15/F16 推理执行与指标；F04、F12、端到端总览和各平台问题专题继续按依赖推进。来源不足的案例保持待办，不以合成材料代替。
