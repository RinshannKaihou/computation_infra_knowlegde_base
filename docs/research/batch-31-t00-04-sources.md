# 第三十一批 T00-04 来源记录

任务：T00-04（训练与推理端到端路径的终态范围验收；**revise** `knowledge/00-overview/training-lifecycle.md`＋`knowledge/00-overview/inference-lifecycle.md`，主题 00.2/00.3）。取证轮次：主会话作者角色首轮（2026-10-21；两主题原基础已覆盖，本任务为有限终态链路核对与必要修订）。

## 新增来源与主张定位

无。修订为导航级链接整合，全部链接指向已交付正文（其来源与审阅记录见各自正文与 docs/research/batch-24/25/26/27/28/31 各记录）；两文原有来源快照不变，verification notes 已注明 2026-10-21 终态核对范围。

## 复用来源与主张定位

| 主张 | 登记 ID | 精确位置 | 支持范围 |
|---|---|---|---|
| 原有两文全部既有主张 | 两文 frontmatter source_refs（不变） | 原登记快照 | Batch 05 已核，本次未改动原口径 |
| 新增分支/入口承载正文 | pretraining-and-finetuning / rl-rollout-consistency / framework-execution / checkpoint-state-consistency / elastic-training-and-membership / performance-analysis / environment-installation-and-upgrade / capacity-and-autoscaling / release-and-recovery / routing-and-flow-control / gpu·ascend-inference-oom-triage / engine-backend-boundaries / mindie-execution-profile / amd-rocm-documented-profile | 各正文 | 各自固定版本与审阅边界 |

## 本文原创部分

- training-lifecycle：新增「工作流分支与状态责任」表（pretrain/SFT/RL rollout 三分支差异点与入口）、「异常恢复与持续进展的验证入口」「平台分支」小节；平台边界段更新（专家并行/mid-step/RL 边界改为指向 06 域正文而非"不由总览证明"的旧表述）。
- inference-lifecycle：新增「副本变更、失败/重试与恢复验证入口」表（五类变化×关系×入口）、「平台分支」小节；适用边界段更新（控制面环节改为指向 07 域方法档案并保留未实测边界）。
- 两文 frontmatter：updated_at/summary/related_ids 扩充；verification notes 补终态核对说明。

## unknown 清单

1. 两文仍为 draft、导航性整理；未运行任何实验。
2. AMD 训练侧 Megatron/MindSpeed 无对应档案（保持 unknown，不画成已支持）；推理侧未入交集档案的组合保持 unknown。
3. 平台安装/升级/回退入口指向 02 域文档样板（T02-12），未实测。

## 复核轮修订记录（初审后）

- C01（P2）：副本扩缩容行拆分"新请求经实际路由收敛转向其他可服务副本"与"在途流按 drain 契约完成/取消（超期或终态不明按重试边界处理）"，并注明不承诺透明续传/KV 自动迁移。
- C02（P3）：平台分支改三线分立——上游 vLLM 限 b17039bc；vLLM Ascend 限 52d4acf（含文档指向 v0.14.1 的差异说明）；MindIE 标注为"仓内文档线自述的 3.1.0"（69e5a5dd 快照，产品包/latest 支持表映射 unknown）。
