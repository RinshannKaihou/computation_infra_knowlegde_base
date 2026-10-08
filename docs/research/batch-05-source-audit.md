# 第五批来源与交付记录

集成日期：2026-09-30。F01/F02/F04/E02 由 `gpt-5.6-sol / high` 编写，F12 由主任务编写；整批集成后交 `gpt-6-astra / xhigh` 独立审阅。所有条目保持草稿，来源核对和现场验证分开。

## 本批正文

| 任务 | 正文 | 来源记录 |
|---|---|---|
| F01 | [一次训练任务的端到端路径](../../knowledge/00-overview/training-lifecycle.md) | [全流程来源](batch-05-overview-sources.md) |
| F02 | [一次推理请求的端到端路径](../../knowledge/00-overview/inference-lifecycle.md) | [全流程来源](batch-05-overview-sources.md) |
| F04 | [设备健康证据与检测边界](../../knowledge/01-hardware/health-evidence.md) | [健康与配套来源](batch-05-health-profile-sources.md) |
| F12 | [作业准入、调度与拓扑放置](../../knowledge/05-cluster-platform/admission-and-placement.md) | [准入与放置来源](batch-05-f12-sources.md) |
| E02 | [NVIDIA 软件栈的文档配套档案](../../knowledge/02-software-stack/nvidia-documented-profile.md) | [健康与配套来源](batch-05-health-profile-sources.md) |

本批新增 11 项来源，累计 51 项；累计 20 篇正文、13 个导航/路径条目。正文已接入主目录、平台与任务路径。来源登记不表示全项目已读完，导航覆盖也不表示目录中全部主题已完成。

## 重点核查边界

- 两篇全流程文只串联主要职责和观察点；图不代表所有框架的严格时序。推理计时需与第四批指标审阅结论同步。
- 健康证据分开状态摘要、事件、计数器、采样失败与未覆盖；DCGM、DCMI、MindX 各自版本和产品条件独立。
- 主动测试只记录资源影响及适用条件，没有执行测试。MindX PRBS 结果表的内部冲突保持未解。
- NVIDIA 容器档案固定 tag 与可见构建元数据，没有拉取镜像或核验 manifest digest。驱动 R545 条款及 Python 版本/路径冲突保留。
- Kueue 逻辑配额、准入条件、TAS 放置与设备分配分开；Volcano 最小组约束不等于应用同步。MindCluster 型号亲和规则不能外推全部 NPU。
- Kueue admission 文档的 `.status.active` 与固定 API 的 `.spec.active` 有差异；本库不据前者给出修改命令。
- 来源只链接并作原创归纳；代码、文档、软件包和第三方许可范围分别保留。

## 轮末审阅

[独立 astra/xhigh 报告](batch-05-astra-review.md)初审发现 0 P1、2 P2、1 P3：MindX 测试条件归属、exporter 计数语义和填充计划首段过期。主任务修订 F04 与来源记录、同步计划；同一独立审阅者定向复核 R1–R3 全部闭合，修订范围无新增问题。

集成时 `make check` / `make build` 已通过 33 entries / 51 sources；修订后连同并行场景草稿再检查通过 48 entries / 59 sources。后一个数量包含第六批和第七批部分内容，不扩大第五批技术审阅范围。内容均继续 `draft`，没有现场实验。

## 下一轮

进入 T01–T04 环境配套、NPU 设备可见性、HCCL 与 NCCL 超时场景，收集流程依据、真实公开案例和实验设计资料。案例证据不足时保留待办，不用虚构事故补齐数量；实验设计不填写未发生的测量结果。
