# 第六批来源与交付记录

集成日期：2026-09-30。T01–T04 共 12 篇正文由两个 `gpt-5.6-sol / high` 子代理分别编写。主任务集成来源、目录和阅读路径，交独立 `gpt-6-astra / xhigh` 审阅。全部保持 `draft`；流程/案例为限定来源范围的 `source_checked`，实验为 `not_verified`。

## 本批正文

| 任务 | 正文 | 类型 |
|---|---|---|
| T01-P | [昇腾版本配套失败诊断指南](../../knowledge/02-software-stack/ascend-version-mismatch-triage.md) | procedure |
| T01-C | [昇腾版本配套失败来源案例](../../knowledge/02-software-stack/ascend-version-mismatch-source-case.md) | case |
| T01-X | [昇腾版本配套失败验证实验设计](../../knowledge/02-software-stack/ascend-version-mismatch-experiment.md) | experiment |
| T02-P | [容器内 NPU 不可见诊断指南](../../knowledge/05-cluster-platform/ascend-device-visibility-triage.md) | procedure |
| T02-C | [容器内 NPU 不可见来源案例](../../knowledge/05-cluster-platform/ascend-device-visibility-source-case.md) | case |
| T02-X | [容器内 NPU 不可见验证实验设计](../../knowledge/05-cluster-platform/ascend-device-visibility-experiment.md) | experiment |
| T03-P | [HCCL 超时诊断指南](../../knowledge/03-communication/hccl-timeout-triage.md) | procedure |
| T03-C | [HCCL 超时来源案例](../../knowledge/03-communication/hccl-timeout-source-case.md) | case |
| T03-X | [HCCL 超时验证实验设计](../../knowledge/03-communication/hccl-timeout-experiment.md) | experiment |
| T04-P | [NCCL 超时诊断指南](../../knowledge/03-communication/nccl-timeout-triage.md) | procedure |
| T04-C | [NCCL 超时来源案例](../../knowledge/03-communication/nccl-timeout-source-case.md) | case |
| T04-X | [NCCL 超时验证实验设计](../../knowledge/03-communication/nccl-timeout-experiment.md) | experiment |

研究记录：[版本与设备](batch-06-environment-device-sources.md)、[HCCL 与 NCCL](batch-06-communication-sources.md)。

本批新增 7 项正式来源；备选 Gitee IBS5FF 只留在研究发现中，未被正文采用，因此没有并入正式来源表。此前第五批 51 项来源，加本批 7 项和并行第七批 T07 的 1 项，为当前 59 项。当前 48 个内容条目包括 35 篇正文与 13 个导航/路径，其中 T07 的 3 篇属于下一批；不能把它们计作本批 12 篇。

## 核查重点与边界

- T01 固定发行包矩阵与实际制品身份分开；版本不符不自动证明当前报错的根因，安装顺序建议不等于报告者复验。
- T02 沿主机、插件、账本、分配、容器、目标进程取证，保留物理/逻辑设备编号；Mooncake 专用补丁不当作所有 NPU 容器的配置处方。
- T03 保留不同 CANN/HCCL 文档版本与历史案例环境；EI0002/notify timeout 不直接归因为网卡。案例补读三条评论，保留报告者 AI_CPU 缓解、单/双开关差异、自动回复和含糊修复提及；completed 关闭不证明修复。
- T04 区分 PyTorch watchdog、NCCL RAS、IB verbs timeout 及观测工具版本；缺失 rank 日志、利用率和 stale 关闭不证明根因或修复。
- 公开案例保留环境缺口、评论定位、Issue/PR 状态和现场复验边界；Issue/评论许可不套用源码许可证。
- 实验只设计隔离、控制变量、证据、停止与恢复标准；没有执行软件安装、容器、集群查询、设备测试或故障注入。

## 检查与轮末审阅

集成后 `make check` 与 `make build` 通过：48 content entries / 59 sources。仅验证结构、ID、来源引用和本地链接，不是技术验证或远程链接巡检。[独立 astra/xhigh 审阅](batch-06-astra-review.md)发现 2 P2 与 2 P3：HCCL 评论遗漏、独立 Docker 分流、PR 精确锚点和研究负控制前提。主任务修订正文/研究/registry，定向复核全部关闭。PDF 页码另统一为印刷83–84与零基索引88–89。

修订后与第七批一起 `make check` / `make build` 通过：54 entries / 63 sources；第七批尚待独立技术审阅，数量不扩大第六批审阅范围。
