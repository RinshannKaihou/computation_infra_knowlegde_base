# Batch 31 来源与交付审计

收尾日期：2026-10-21。五任务：T06-09（训练主题五方面入口与交付核对，**navigation/revise** `knowledge/06-training/index.md`，主题 06.1–06.8）、T07-12（推理主题入口及缓存/SLO 最终边界核对，**navigation/revise** `knowledge/07-inference/index.md`，主题 07.1–07.8）、T02-12（三平台安装基线、迁移升级与回退验证，**new** `knowledge/02-software-stack/environment-installation-and-upgrade.md`，主题 02.7）、T00-04（训练与推理端到端路径终态范围验收，**revise** `knowledge/00-overview/training-lifecycle.md`＋`inference-lifecycle.md`，主题 00.2/00.3）、T00-05（学习者、架构设计与运维角色阅读路径，**new/navigation** `paths/roles/reading-by-role.md`，主题 00.6）。批内顺序按依赖：T06-09、T07-12 → T02-12、T00-04 → T00-05。

## 来源账面

- registry 575→578 后于复核轮合并重复身份定格 **577**：新增 `src.nvidia.driver-installation-guide-latest-2026-10-21`（latest 可变页，Ubuntu/version-locking 两节＋第三轮补读 Post-installation Verify the Driver Version）、`src.huawei.cann-83rcx-upgrade-uninstall-2026-10-21`（instg_0027–0033 升级/卸载＋instg_0094 安装后配置，doc_center/source 静态镜像核读）；CUDA 12.8 安装指南的 T02-12 核读并入既有 `src.nvidia.cuda-12-8-installation-guide-linux`（首建的平行 ID 按复核 C13 并删除）；ROCm 安装页为既有 `src.amd.rocm-install-docs-10.1.0` 补读（Batch 31 段经原始 HTML 更正"无卸载章节"误记——两轮网页转换漏读 Uninstalling 节，unknown 收窄为完整回退/依赖恢复）。
- 既有条目核正：`src.amd.rocm-bandwidth-test-d7f5efe` URL 钉固定 commit 树；`src.nvidia.cuda-samples-v12.8` 扩展核读同 tag bandwidthTest（README 原文照录 CUDA Toolkit 12.5，不外推）；CANN/驱动条目 notes 按复核更正（固件卸载完整路径、脚本按包分列、Kernels 前提、local/network 仓库分列）。
- 取证方法备注：hiascend 沿用 doc_center/source 静态镜像；ROCm 安装页为选择器驱动单页，WebFetch 转换两次漏读 Uninstalling 节，最终以 curl 原始 HTML 定位复核（教训：大页面转换截断需原始 HTML 兜底）。

## 审阅账面（全部 gpt-6.1-sol / xhigh，每轮经 turn_context 核验）

| 任务 | 初审 | 复核轮次 | 终态 |
|---|---|---|---|
| T06-09 | 2 项（P2×1、P3×1）＋R01 | 2 轮（首启 resume 档位 high 按约定整轮作废不计；显式 xhigh 重跑后 C01/C02/R01 全 CLOSED） | 3/3 CLOSED |
| T07-12 | 4 项（P2×2、P3×2） | 1 轮 | 4/4 CLOSED |
| T02-12 | 13 项（P2×10、P3×3） | 5 轮（R01–R07→R08–R12→R13/R14→R15） | 13＋15＝28/28 CLOSED |
| T00-04 | 2 项（P2×1、P3×1） | 1 轮 | 2/2 CLOSED |
| T00-05 | 4 项（P2×2、P3×2）＋R01 | 2 轮 | 5/5 CLOSED |

合计 42 项编号发现全部 CLOSED，无 P1、无例外项；T06-09 一次档位失配轮按 authoring-guide §7 作废（报告删除、不计轮次，事实留痕于其取证记录）。复核主要修订方向：**导航任务的账面纪律**（backlog 缺口状态滞后同步 06 域 9 项＋07 域 18 项，只改状态字段并逐组对证；02 index 不得提前写"审阅已闭环"）；**来源身份**（MindIE latest 与 3.1.0 文档线分立、ROCm Uninstalling 误记更正、CUDA 双模板冲突照录、平行来源身份合并、固定 tag/commit 钉扎）；**判据分层**（安装身份/已加载身份/固件信息分项、样例自带校验 vs 计算正确性契约、B0/N/R 三状态对照、制品保全与全量卸载分列、通配 purge 命中并列旧版标注语义推断）；**演练可复核性**（纸面演练逐跳记录＋显式题设假设＋先修核对）。未运行任何安装/升级/查询/样例；正文均为 draft（T02-12 为 procedure、verification source_checked）。

## 主题账面

02.7 升为已覆盖（基础）（T02-12 补齐安装验证梯子/变化矩阵/回退边界，文档样板未实测）；00.2/00.3 维护验收（T00-04 终态核对，不改变 covered 判断）；00.6 保持部分覆盖（三角色路径已交付，任务/平台路径收口属 Batch 32）。统计重算 **61/2/0**（部分覆盖余 00.6 与 03.5-BLOCKED-1）。本文件收尾同步追记了此前两批未同步到盘点审计文档的 Batch 29/30 逐主题行（账面原以两批 source-audit 与盘点 YAML 为准）。批次与五任务置 done（completion_record：本文件）。机器可读记录见 plans/topic-coverage.yaml 与 plans/full-coverage-backlog.yaml。

## 写作轮次自记

- 导航修订保留稳定 ID（training.index/inference.index/overview.training-lifecycle/overview.inference-lifecycle）；06/07 两个 index 新增八主题五方面入口表与交付核对小节；00 导读首页接入角色路径。
- T02-12 全部命令与回显来自官方文档原文（CUDA 12.8 归档、NVIDIA 驱动指南 latest、CANN 8.3.RCX 静态镜像、ROCm docs-10.1.0 原始 HTML）；"变更前准入门禁"三类缺项停止规则为本文方法原创。
- T00-05 纸面演练为三问三答逐跳记录，纸面导航检查不产生运行结果。
- 各轮修订记录见五份 sources 记录的修订小节；07.3/07.7 边界复核、07 域 18 项账面同步、06 域 9 项账面同步均有逐组对证表（见各审阅/复核报告）。
- 下一批 Batch 32（末批）：T00-06 选型/验收/安装任务路径、T08-09 可靠性主题五方面核对、T00-07 性能/迁移/恢复任务路径、T00-08 三平台入口与排障路径收口。
