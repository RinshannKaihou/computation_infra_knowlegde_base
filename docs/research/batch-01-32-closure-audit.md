# Batch 01–32 收尾分析与开放项

日期：2026-10-22（Asia/Shanghai）。输入基线：`3a0e155`，工作区起始无未提交修改。本次为仓库账面、交付身份和既有审阅证据的核对，不是一次新的全库技术审阅；历史实际模型、审阅角色和证据强弱以原报告为准。本次没有重新访问上游来源或执行现场实验。

**结论：32 个内容批次已完成约定交付，其中 Batch 17、19 按用户批准的例外条件验收；整个知识库尚未完全闭环。** 可以推送当前文档成果和审计记录，但不能宣称所有发现关闭、63 个主题无条件验收或硬件验证完成。

## 交付与审阅证据

- 首轮 Batch 01–07：`content-backlog.yaml` 的 41 项任务均 done，实际目标路径与稳定 ID 全部存在；见[首轮交付核对](../first-fill-status.md)。Batch 03–07 保留当时 astra 审阅记录，Batch 01/02 的补审与问题关闭见[四批补审汇总](batch-01-02-08-09-codex-review-summary.md)。没有将历史模型追改成当前约定模型。
- 第二轮 Batch 08–12：`round-02-backlog.yaml` 的 15 项任务均 done；Batch 08/09 见上述四批汇总，Batch 10–12 的 13 项发现经修订和定向复核关闭，见[三批汇总](batch-10-11-12-codex-review-summary.md)。
- 后续 Batch 13–32：20 个批次与 85 项任务均 done，99 个目标引用（含多任务复用同一文件）逐项核对文件、catalog 路径与稳定 ID，一致性错误为 0。`targets[].state` 保留历史 planned_new/existing/delivered 标签，本次交付判断依据实际文件与任务状态。

| Batch | 本轮任务数 | 已有终态记录及限定 |
|---|---:|---|
| 13 | 5 | [来源审计及补充复核入口](batch-13-source-audit.md) |
| 14 | 4 | [来源审计](batch-14-source-audit.md)，部分证据仍限编写者核对范围 |
| 15 | 4 | [来源审计](batch-15-source-audit.md)，部分证据仍限编写者核对范围 |
| 16 | 4 | [来源审计](batch-16-source-audit.md) |
| 17 | 4 | [第六次复核](batch-17-codex-sixth-recheck.md)＋[用户条件验收](batch-17-t02-10-exception.md)，C08 保持 OPEN |
| 18 | 4 | [来源审计](batch-18-source-audit.md) |
| 19 | 5 | [来源审计末段](batch-19-source-audit.md)＋[用户条件验收](batch-19-blocked-1-exception.md)，BLOCKED-1 保持 OPEN |
| 20 | 4 | [来源审计](batch-20-source-audit.md) |
| 21 | 4 | [来源审计](batch-21-source-audit.md)＋[T04-08 补交最终复核](batch-21-t04-08-claude-recheck-5.md) |
| 22 | 4 | [来源审计](batch-22-source-audit.md)＋[整批验收复核](batch-22-acceptance-codex-recheck.md) |
| 23 | 4 | [来源审计](batch-23-source-audit.md) |
| 24 | 4 | [来源审计](batch-24-source-audit.md)＋[交付后复查第五次复核](batch-24-post-close-codex-recheck-5.md)；早期 OPEN 以最终复核为准 |
| 25 | 4 | [来源审计](batch-25-source-audit.md) |
| 26 | 4 | [来源审计](batch-26-source-audit.md) |
| 27 | 4 | [来源审计](batch-27-source-audit.md) |
| 28 | 5 | [来源审计](batch-28-source-audit.md) |
| 29 | 4 | [来源审计及主题账面](batch-29-source-audit.md) |
| 30 | 5 | [来源审计及主题账面](batch-30-source-audit.md) |
| 31 | 5 | [来源审计](batch-31-source-audit.md)、[训练八主题核对](../../knowledge/06-training/index.md)、[推理八主题核对](../../knowledge/07-inference/index.md) |
| 32 | 4 | [来源审计及主题账面](batch-32-source-audit.md) |

本次读取逐批审计的终态、例外与相关最终复核；不将初审报告内历史 OPEN 直接计为当前 OPEN，也不把后续任务 done 用作关闭证据。未重新逐项运行全部历史审阅会话的模型元数据核验，原报告中未独立核验的证据继续保留其限定。

## 当前内容与覆盖

重建清单后共 **135 个条目、577 项来源**：knowledge/ 123 条、paths/ 12 条。实质正文 114 篇（concept 33、reference 29、procedure 36、case 9、experiment 7），导航 21 篇（index 9、path 12）。114 篇正文全部可在主题 evidence_refs 找到，未映射正文 0、无效 evidence ID 0。

63 个逐主题记录为 covered 54、covered_basic 8、partial 1，合并口径 **62/1/0**；唯一 partial 为 03.5。有限正文验收回填后 accepted 62、planned 1；02.6 的 accepted 受 B17-C08 例外约束，03.5 因 acceptance 5 未验收继续 planned。完整统计见[主题盘点](../topic-coverage-audit.md)及[机器清单](../../plans/topic-coverage.yaml)。

全部条目仍为 draft。正文 99 篇 source_checked、15 篇 not_verified（7 experiment＋8 procedure），本地 reproduced 为 0。登记来源、模型审阅、方法覆盖和结构检查不构成实测成功。

## 本次发现、修订及定向核对

| ID | 发现 | 修订与关闭依据 |
|---|---|---|
| CL-A01 | 盘点 YAML summary 停在 Batch 30 的 60/3/0，followup 为 20；批次字段分别残留 01–29/next 30 与剩余 8 批 | 从全部 63 个逐主题状态重算 62/1/0、followup 1；批次改 01–32、next null、剩余 0；保留原始输入快照 |
| CL-A02 | 盘点正文统计、小计表、catalog 数与实际状态不一致；README 缺当前收尾摘要 | 同步 135/577、114 正文＋21 导航、99/15/0 验证分布和九领域小计；README 明确当前与历史口径 |
| CL-A03 | 主计划仍有 30 个已完成有限正文核对的主题停在 planned，以及 21 条已在 Batch 29–31 审计关闭的内容缺口停在 open | 对照既有审计的主题账面、06/07/08 五方面入口及盘点行，逐条回填验收和关闭依据；03.5 与三个 both 轨道缺口不升状态。结果为主题 62 accepted / 1 planned；141 条原缺口中 137 closed / 4 open |
| CL-A04 | 12 个已覆盖主题的 followup_priority/recommended_action 仍要求新增或扩展正文；主计划 notice/execution_status_note 停留于早期执行状态 | 已覆盖主题改 maintain，notice 与执行说明指向当前结论；历史 input_snapshot/validation/documents 与原审阅报告保持原样 |
| CL-A05 | Batch 22/25/26 为 done，但缺 completion_record；路线图末段遗漏 B17-C08 | 补齐现存审计路径与对应完成日期；当前开放项统一列出 C08 和 BLOCKED-1；不重写历史审阅结论 |

以上五项属于本次账面核对发现。修订后通过下列全量交叉检查与定向核对关闭；这不是另一次独立模型技术审阅通过声明。

## 继续开放的事项及关闭条件

| 项目 | 当前状态与关闭所需证据 |
|---|---|
| B17-C08（P2） | 逐算子累加精度、TorchNPU cubeMathType 透传契约缺官方证据。按[例外清单](batch-17-t02-10-exception.md)保持 OPEN；只有官方文档或可登记的官方答复满足关闭条件，后续引用仍须 unknown |
| 03.5-G3 / BLOCKED-1 | HCCL Test 与目标 CANN/HDK/机型的自洽官方交集未建立；T03-06 acceptance 5 未验收，主题仍部分覆盖。按[例外清单](batch-19-blocked-1-exception.md)保留 OPEN；不同版本 API/Test 文档不能拼成部署条件 |
| 01.6-G3、08.7-G3 | 真实验收环境档案和实验结果仍缺；保持 both 轨道 open，由 V08 与相关 V 包按具体环境、输入、判据和外置证据验收 |
| 08.8-G3 / V12 | 独立诊断评测集本体尚未外置取得并隔离；公开教学题组只能证明方法交付，不关闭独立集缺口 |
| V00–V12 | 13 个验证工作包均 planned；七份既有方案执行 0/7。V00 已整理 19 个 skeleton_prepared/not_ready 实例，资源、授权、冻结件和证据位置等适用缺项未完成，不代表可执行或已完成 |

B17-C08 是独立审阅例外，没有额外增加一条原始 141 缺口；BLOCKED-1 对应 03.5-G3，因此不能重复计入原缺口总数。前三个 both 轨道缺口与方法层主题基础覆盖分开统计。来源工作包 A01–A20、S21–S27 的 planned/collecting 也不等于上述内容任务未交付：它们管理更广的采集范围，当前已使用的精确来源与主张以 registry、正文和逐批审计为准；本次不将这些工作包一并标完成。

## 验证与推送范围

- `make check`、`make build`：修订后均 PASS，135 entries / 577 sources；只验证结构和本地引用。
- 补充交叉核对：使用仓库拒绝重复键的 YAML loader，验证三轮任务目标的路径/ID、批次与任务集合、63 主题汇总和验收、141 缺口轨道、正文 evidence 映射、V 包与 19 实例状态，并对比历史快照和原审阅文件的 Git 身份。修订后全部 PASS：30 个主题验收、21 条内容缺口回填数量吻合，9 领域小计一致，原任务/依赖/策略与历史快照未变。
- `git diff --check`：本次修改 PASS；对全部待推送历史提交运行该检查时，报告 4 处既有空白格式提示（1 处行尾空格、3 处审阅报告末尾空行），未改写这些原始记录或重写历史。
- 本次只改当前状态文档与计划，不改 knowledge/、paths/、sources/registry.yaml 或 src/kb/；不需要新增测试或运行工具代码回归套件。
- 远程预检已执行 `git fetch origin`；当时 origin/main 是本地 main 的祖先，本地有 61 个尚未推送提交。推送将包含这些已有内容/审阅提交与本次收尾提交，使用普通 fast-forward push，不重写共享历史。最终远程提交身份由本次会话推送后核对，不在提交中预写成功结果。
