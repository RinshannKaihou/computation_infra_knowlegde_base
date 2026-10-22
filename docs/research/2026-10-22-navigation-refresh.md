# README 归档与过期入口清理

日期：2026-10-22。基线：`c59da25`。范围：README、九个领域首页、knowledge/ 与 paths/ 中的交付/审阅状态措辞，以及维护指南、旧计划和交接文档。依据为仓库现有文件和最终审阅记录；未重新抓取上游文档，不声称重新验证所选版本的现时兼容性。

## 修改与依据

| 项目 | 清理结果 | 依据 |
|---|---|---|
| README 开头交付状态与逐批历史 | 原文移入[交付历史归档](../archive/readme-delivery-history.md)，修正相对链接；首页保留标题、简介后直接进入“从这里开始” | 原提交的 README；归档保留文字和历史模型身份 |
| README 内容与贡献入口 | 早期正文列表改为跨领域选读；添加内容不再引导启动已经完成的批次；网站/索引“均已生成”的表述收窄为当前静态 catalog 能力 | 已有正文、Makefile 与当前校验/构建实现 |
| 00/01/02/03/04/05 首页 | 去掉“其余二级主题待补充”的过期泛称；硬件首页接入已交付的 NPU 传输/同步和验收档案方法，通信首页接入三库/RCCL 档案与拥塞热点分支 | 各页面已有正文、[Batch 17](batch-17-source-audit.md)、[Batch 19](batch-19-source-audit.md)及[主题盘点](../topic-coverage-audit.md) |
| 存储首页 | 清除 T04-03/04/05/06/07“审阅中”及“主题验收留待 Batch 21”；补齐制品发布、负载基线和恢复正文入口 | [Batch 20 审计](batch-20-source-audit.md)、[Batch 21 审计](batch-21-source-audit.md)、[T04-08 最终复核](batch-21-t04-08-claude-recheck-5.md) |
| 推理/可靠性首页 | T07-12“导航核对阶段”、T08-09“审阅待做”改为已完成原范围核对；九首页“首轮成果”标题统一为内容维护表述 | [Batch 31](batch-31-source-audit.md)、[Batch 32](batch-32-source-audit.md) |
| 节点生命周期与存储正文 | 删除节点 drain、T07-01 推理加载、T04-07 存储恢复“未交付”的过期指代，直接链接对应流程；就绪与输出质量分列 | [节点摘除流程](../../knowledge/05-cluster-platform/node-drain-resource-reclamation.md)、[推理加载](../../knowledge/07-inference/model-loading-and-readiness.md)、[输出质量评估](../../knowledge/07-inference/output-quality-evaluation.md)、[存储恢复](../../knowledge/04-data-storage/storage-client-backend-recovery.md) |
| 四篇 Batch 17 正文及两篇存储正文 | “定向复核待执行/待复核”改为实际终态并给最终报告定位；精度正文明确 C08 继续 OPEN | [B17 第六次复核](batch-17-codex-sixth-recheck.md)、[条件验收](batch-17-t02-10-exception.md)、[T04-03 第五次复核](batch-20-t04-03-claude-recheck-5.md)、[T04-05 第三次复核](batch-20-t04-05-claude-recheck-3.md) |
| 维护文档 | Git 指南说明已配置 origin；写作指南改为内容维护与证据补齐阶段；首轮交付、填充计划、Opus 交接、批次依赖和完整覆盖路线图加历史范围提示，原路径与历史正文保留 | Git 配置、[收尾分析](batch-01-32-closure-audit.md)、现行[写作指南](../authoring-guide.md) |

## 保留的信息

- 两项例外 B17-C08、BLOCKED-1 和三个真实证据缺口不因本次清理关闭；七份实验方案仍未执行，V00 的 19 个实例仍 not_ready。
- `draft`、`source_checked`、`not_verified` 与 `reproduced` 的状态均未上调；精确来源、技术论断、命令、参数、阈值和平台版本边界未重新改写。
- 缺少现场结果、未取得上游证据、尚无独立案例/实验的具体待办继续保留；公开案例中的“审阅中”若描述当时的上游讨论，不当作本库当前待审状态清除。
- docs/research/ 的原审阅报告及历史模型记录保持原样；旧计划中的输入快照、任务图和当时统计不替换成当前数值。

## 定向检查

- `make check`、`make build` 与 `git diff --check` 全部通过：135 个条目 / 577 项来源。
- 对照 Git 基线核验通过：17 个修改的内容文件保持稳定 ID、类型、平台、来源和编辑/验证状态；代码块与外部 URL 序列不变。仅两篇存储正文的 verification.notes 更新审阅完成定位；原审阅报告、全部计划 YAML 和 paths/ 无改动。
- 归档文字与原 README 的迁移块逐字对照通过（仅转换相对链接）；全部本地链接通过结构检查。README 首节为“从这里开始”，不再含批次状态流水账；九领域首页不再含本次识别的过期状态。远程 README 未添加指向忽略目录 build/ 的文件链接。
