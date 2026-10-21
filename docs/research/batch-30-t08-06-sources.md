# 第三十批 T08-06 来源记录

任务：T08-06（可靠性统计、有效产出与恢复损失；**new** `knowledge/08-reliability/reliability-metrics-and-recovery-loss.md`，主题 08.1/08.8）。取证轮次：主会话作者角色首轮（2026-10-21；依赖 T08-03 已于 Batch 29 交付）。

## 新增来源与主张定位

| 主张 | 登记 ID | 精确位置 | 支持范围 |
|---|---|---|---|
| 有效训练时间定义（useful training over elapsed time）与 >90%；54 天 466/47/419 中断；约 78% confirmed-or-suspected 硬件、GPU 58.7%、SDC 1.4%、NCCL watchdog 归 Unknown 1.7%；仅 3 次人工介入、日均≥1 次中断；checkpoint 每卡 1 MB–4 GB、Tectonic 240 PB/2 TB/s（峰 7 TB/s）；NCCL flight recorder | src.arxiv.llama3-infrastructure（**本轮新增**） | [arXiv:2407.21783v3](https://arxiv.org/abs/2407.21783) §2 基础设施段与 Table 5（2026-10-21 HTML 核读；百分比经 GPU 类六行求和=58.7% 自洽核对；Faulty GPU 行绝对计数 148 与 30.1% 不自洽，只引用百分比） | 16K H100、405B 预训练、54 天快照与其归因口径；不外推 |
| MPG＝SG×RG×PG 定义（SG 全体所需芯片同时可用/fleet 容量；RG 已存 checkpoint 有效 chip-time/allocated、最后 checkpoint 到失败间不计；PG 理想/实际执行时间）；occupancy 不区分产出的批评；分量定位优化（Table 2） | src.arxiv.mpg-tpu-goodput-2025（**本轮新增**） | [arXiv:2502.06982v1](https://arxiv.org/abs/2502.06982) §4.1/§4.3/§5（2026-10-21 全文核读） | Google 内部 TPU fleet；示例数值未引用 |
| OCP §5.3.1：频繁 checkpoint 压低 runtime goodput、epoch 末 checkpoint 不足、exascale checkpoint 时间逼近 MTTF 的风险 | src.ocp.sdc-in-ai-2025（既有登记，Batch 30 补读） | §5.3.1/§5.4（p.21–22） | 机制性讨论 |

## 复用来源与主张定位

| 主张 | 登记 ID | 精确位置 | 支持范围 |
|---|---|---|---|
| SLI/错误预算口径（推理侧记账的联动样板） | src.google.sre-implementing-slos | 章节（2026-09-29 已核） | SRE 工程口径 |
| 症状/观测区分（事件起止按可观测证据定义的底座） | src.google.sre-monitoring-distributed-systems | 章节（2026-09-29 已核） | 同上 |
| MTBI 22.61× 为仿真、非常生产 A/B | src.usenix.superbench-atc24 | 局限节（第十二批已核） | Azure GPU |
| vLLM finish reason 语义、goodput 绑定 SLO、幸存者偏差 | src.vllm.inference-v0-14 | 经 [latency-metrics](../../knowledge/07-inference/latency-metrics.md) 转引（固定源码锚点） | vLLM v0.14.0 |
| elastic 重启语义 | src.pytorch.elastic-2.6 | 文档＋实现分支口径（Batch 11/29 已核） | PyTorch 2.6 |

## 本文原创部分

统计框架要素表（对象/窗口/分母/事件起止/删失/缺失/重叠/聚合）、MTBF/MTTR 使用边界三条、六类量记账表（有效产出/已提交/重算/丢失/恢复三段/健康窗口）、事件表与窗口聚合 YAML schema、合成计算例（168h 窗口、量纲闭合：161.0/168.0≈95.8% vs 165.5/168.0≈98.5%；32 卡→512 卡的分母 factor 演示）、"同一症状四维结论不同"对照表。

## unknown 清单

1. 本地辖内环境无长期事件数据；真实统计需按 schema 现场采集（采集系统部署不在本文范围）。
2. MTBF/MTTR 的分布检验方法（更新过程检验等）未登记原始统计来源，正文只给使用边界。
3. MPG 论文示例 fleet 数值未读未引。
4. Llama 3 Table 5 绝对计数的渲染不自洽问题（148 vs 30.1%）——后续版本 PDF 若自洽可更新口径。
