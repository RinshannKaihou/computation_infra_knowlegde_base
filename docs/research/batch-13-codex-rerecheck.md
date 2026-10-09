# Batch 13 补充审阅定向复核汇总

日期：2026-10-09（Asia/Shanghai；执行的 UTC 日期为 2026-10-08）。原审阅会话 `01a11c1a-4fb4-7f73-a0a3-d97e5f379dff`，配置 `gpt-6.1-sol / xhigh`；完整复核运行使用显式 `read-only`。

当前状态：**补充审阅及定向修订范围内通过。R01–R06 六个跟踪条目均 CLOSED，无剩余 OPEN/BLOCKED。** R03 与 R06 跟踪的是同一处剩余时间窗缺口，不重复计数。

第一轮报告见[原审阅者报告](batch-13-codex-rerecheck-round-1.md)。本轮正常退出、返回码 0，11/11 输入 SHA-256 匹配；`make check` 返回 PASS。初始五项发现保留在[补充审阅报告](batch-13-codex-rereview.md)，修改过程见[修订记录](batch-13-rereview-revisions.md)。

第一轮实际取得 DCMI、Linux 固定源码/文档、DCGM、Redfish 及 PyTorch 关键原文。健康定义 XLSX 未独立取得、npu-smi 全量负面扫描为编写者记录、现场版本和环境缺口仍保留；复核关闭不意味着硬件验证，正文仍为 `draft / source_checked`。

## 两轮关闭记录

| 条目 | 最终状态 | 独立关闭依据 |
|---|---|---|
| R01（P2） | CLOSED | 第一轮重取 DCMI，确认能力范围、原因位与支持矩阵 |
| R02（P2） | CLOSED | 第一轮重取 Linux 与 numactl 固定来源，确认允许集/策略/线程/驻留证据分开 |
| R03（P2） | CLOSED | 第一轮确认不可读分支和实体范围；第二轮确认剩余取样边界补修 |
| R04（P3） | CLOSED | 第一轮重取精确 PSU schema，确认数组及废弃字段 |
| R05（P3） | CLOSED | 第一轮重取 PyTorch 2.6 实际机制段，替换占位引用 |
| R06（P3，修订引入） | CLOSED | 第二轮重新取得固定 MonitorThermal/MonitorPower，确认 endTime 与最新样本边界 |

第二轮报告见[原审阅者报告](batch-13-codex-rerecheck-round-2.md)：正常退出、返回码 0，3/3 新输入指纹匹配；实际重新取得 DCGM 两个函数原文，同一 blob SHA `1ff23bb905f1276a0f846551a44cd803a0c1034c`。R01/R02/R04/R05 沿用第一轮关闭，未声称第二轮重新技术审阅；本轮没有新增 R07。

原报告保留各自实际日期、配置、读取范围、指纹和来源取得限制。第一次 resume 未继承只读沙箱的运行由主执行者主动中断，仅执行读取、无最终结论；完整两轮显式配置 read-only，并由 turn_context 核对配置。CLI 对已有 codegraph 配置键及模型元数据缺失给出警告；记录的是实际请求/会话配置，不将其作为底层模型身份认证，也没有改用其他模型。

## 集成后的记录调整

两轮报告保存后，仅更新关闭状态、汇总/交付记录和 README 导航；知识正文及研究记录的技术内容未再改动。来源登记仅将 DCGM notes 的“待第二轮”改为已关闭；第二轮报告中的 registry SHA 保留为审阅输入，以下另记状态更新后的指纹，避免混用。

最终 `sources/registry.yaml` SHA-256：`6dae2d9d4af6c36e8b7ba2ffa1b514e97993175718c8a34627a9c5325ec9f5aa`。

最终集成后，主执行者实际运行 `make check`、`make build`，两项退出码均为 0，PASS: 73 content entries / 123 sources；构建生成 build/catalog.json 与 build/catalog.md。正文及研究记录技术输入指纹保留，未执行硬件验证。
