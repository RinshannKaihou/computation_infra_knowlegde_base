# 第七批来源与交付记录

集成日期：2026-09-30。T05 精度差异与 T06 恢复异常分别由 `gpt-5.6-sol / high` 子代理编写，T07 推理长尾由主任务编写；集成后交独立 `gpt-6-astra / xhigh` 审阅。全部保持 draft，P/C 为限定来源范围的 source_checked，X 为 not_verified。

## 本批正文

| 任务 | 正文 | 类型 |
|---|---|---|
| T05-P | [GPU 到 NPU 的精度差异诊断指南](../../knowledge/06-training/gpu-npu-precision-difference-triage.md) | procedure |
| T05-C | [GPU 到 NPU 的精度差异来源案例](../../knowledge/06-training/gpu-npu-precision-difference-source-case.md) | case |
| T05-X | [GPU 到 NPU 的精度差异验证实验设计](../../knowledge/06-training/gpu-npu-precision-difference-experiment.md) | experiment |
| T06-P | [Checkpoint 恢复状态异常诊断指南](../../knowledge/06-training/checkpoint-state-recovery-triage.md) | procedure |
| T06-C | [Checkpoint 恢复状态异常来源案例](../../knowledge/06-training/checkpoint-state-recovery-source-case.md) | case |
| T06-X | [Checkpoint 恢复状态异常验证实验设计](../../knowledge/06-training/checkpoint-state-recovery-experiment.md) | experiment |
| T07-P | [昇腾推理长尾诊断指南](../../knowledge/07-inference/ascend-inference-tail-latency-triage.md) | procedure |
| T07-C | [昇腾推理长尾来源案例](../../knowledge/07-inference/ascend-inference-tail-latency-source-case.md) | case |
| T07-X | [昇腾推理长尾验证实验设计](../../knowledge/07-inference/ascend-inference-tail-latency-experiment.md) | experiment |

来源记录：[T05](batch-07-training-sources.md)、[T06](batch-07-checkpoint-sources.md)、[T07](batch-07-inference-source-candidates.md)；早期发现另见[训练候选记录](batch-07-training-source-candidates.md)。T07 文件保留候选期名称，末尾已记录成文与来源再核查，不是额外正文。

本批新增 5 项正式来源（T07 在并行准备时已先登记），总计 63 项。首轮 41 篇正文均已形成，加 13 个导航/路径为 54 个条目；正文未重复放到 paths，模板不计入。

## 重点边界

- T05 固定 msprobe commit 与 PyTorch 数值说明，区分同平台重复、跨平台差异、非有限值与训练质量；seed、FP64 参考或工具标红阈值不变成跨 GPU/NPU 一致性保证。
- T05 案例 #17 补读 GitHub 连接器返回的单条评论；数据/模型/GPU 栈仍有缺口。DDP stride warning 不当作数值根因。
- T06 流程的 PyTorch2.6 默认 DCP planner 非 tensor 同 FQN 去重，与应用 rank-local 状态责任保留；实验覆盖文件/状态/继续训练的不同判据。
- T06 案例 #164257 是 PyTorch2.8/macOS CPU，已读四条 Issue 评论及 PR165228→固定 commit。示例创建新对象却使用旧对象的偏差、strict false 的特定改动、首个发行/现场复验未知均明确，不伪装 GPU/NPU 事故。
- T07 复用已审 vLLM0.14 指标和插件RC样板，两个快照未拼成验证组合；#17443 为独立 nightly 历史环境，连接器评论列表为空。客户端与引擎时间、输入/TTFT 与 kernel 吞吐、均值与尾部、成功请求与失败样本分别处理。
- 三项实验只有设计，无软件安装、保存/加载、训练、benchmark、profiling、设备/集群查询或故障注入结果。
- msprobe 文档 CC-BY-4.0 与产品 MulanPSL-2.0、分发包/EULA 分别登记；Issue/PR 讨论不自动继承代码许可。来源只读、原创归纳，未镜像全文或日志。

## 检查与轮末审阅

独立 `gpt-6-astra / xhigh` 初审发现两项 P2，均已修订并定向复核关闭；复核新增一项源码锚点 P3，也已关闭。详见[审阅报告](batch-07-astra-review.md)。

- 恢复实验改为同一提交父子版本的直接 missing-FQN 分支对照，独立记录 fresh-object 端到端占位状态；不再假定其必然触发修订分支。
- DCP 普通 dict 与 Stateful 的返回边界分别说明，并同步 F14 的直接传播段落。
- PyTorch 2.8 的三个源码锚点改用固定 commit 原文件行号，避免网页重排行号带来的误定位。
- 交付核对还修复了三篇案例摘要中未加引号的 ` #编号`，避免 YAML 注释截断 Agent 清单；章节页尾状态与写作指南同步更新。

最终 `make check` / `make build` 通过 54 entries / 63 sources；41 项任务身份、路径、元数据及摘要与生成清单一致。该结果仅覆盖结构与本地引用。首轮 41 项任务均标为 done；正文仍 draft，7 项实验仍 not_verified，没有软件安装、保存/加载、训练或现场验证结果。
