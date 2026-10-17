# 第二十二批来源审计（T05-02/T05-03/T05-05 通过；T05-01 已于 2026-10-17 闭环通过；T05-04 于 2026-10-17 审阅闭环通过；主题范围复核已记录，批次置 done）

更新日期：2026-10-15；2026-10-17 更新：T05-01 经第 29–33 次复核闭环（C30–C34 全部 CLOSED，见 `batch-21-t05-01-codex-recheck-33.md`），T05-04 前置随之解除并完成交付；同日 T05-04 初审（`batch-22-t05-04-claude-review.md`）判定需修订（B22-C31–C38，P1×1/P2×4/P3×3），作者第 1 轮修订后经第 1 次定向复核（`batch-22-t05-04-claude-recheck.md`）：C31–C38 全部 CLOSED，新增 C39–C41（均 P3）；初审引证勘误成立并补充——初审引文真实出处为 prolog_epilog.html L622–625（页名误记为 gres.html），作者定位的 sbatch.html L2926–2928 全局编号定义属实，两页措辞差异并列引用。作者第 2 轮修订后经第 2 次定向复核（`batch-22-t05-04-claude-recheck-2.md`）：C39–C41 全部 CLOSED，新增 C42（P3，记录层同步）；C42 同步后经第 3 次定向复核（`batch-22-t05-04-claude-recheck-3.md`）：C42 CLOSED，新增 C43（P3，本文件 L3/L31 状态遗漏未随 L1/L13 同步）。C43 修复后经第 4 次定向复核（`batch-22-t05-04-claude-recheck-4.md`）：C43 CLOSED，新增 C44（P3，登记 notes L5247 残留"go-nvlib 枚举序"，与审计所记不符）。C44 按推荐方式修复（L5247 改为与正文/来源记录同口径写法，即登记原文"`VisitDevices` 回调序号与 NVML index、宿主 nvidia-smi 序号的关系（go-nvlib 未取）"；登记/正文/来源记录全文检索"枚举序"已为 0 命中）后经第 5 次定向复核（`batch-22-t05-04-claude-recheck-5.md`）：**C44 CLOSED，无新发现，B22-C31–C44 共 14 项全部 CLOSED，acceptance 4/4 满足，T05-04 通过审阅**。六轮审阅（初审＋五次定向复核）的模型元数据均经调用方按 CLI 输出核验：`modelUsage` 仅 `claude-opus-5-5` 单一模型、无 fallback 标记，均计入有效轮次。本文件初版（T05-02/T05-03 草稿交付时）由本会话（Muse Spark，作者角色）编写；审阅闭环由另一并行会话的独立审阅角色完成，本会话未参与复核判断，以下通过结论均转述对应复核报告。

## 本批任务状态

| 任务 | 状态 | 依据 |
|---|---|---|
| T05-02 Kubernetes 作业全生命周期与控制器责任 | 通过 | 初审＋五次定向复核，B22-C01–C11 合计 CLOSED 11 / OPEN 0（`batch-22-t05-02-claude-recheck-5.md`） |
| T05-03 Slurm 作业生命周期、设备资源与状态参考 | 通过 | 初审＋四次定向复核，B22-C12–C21 累计 CLOSED 10 / OPEN 0（`batch-22-t05-03-claude-recheck-4.md`） |
| T05-05 扩展 gang、配额和双平台调度策略 | 通过 | 初审＋五次定向复核，B22-C22–C30 共 9 项全部 CLOSED（`batch-22-t05-05-claude-recheck-5.md`）；`admission-and-placement.md` 修订在工作区 |
| T05-01（Batch 21 补交，T05-04 前置） | **通过（2026-10-17 闭环）** | 至 `batch-21-t05-01-codex-recheck-33.md`：C30–C34 累计 CLOSED 5 / OPEN 0，Acceptance 4/4 完整通过；gpt-6.1-sol / xhigh，无 fallback 标记 |
| T05-04 扩展 GPU 与 Slurm 设备资源账本 | **通过（2026-10-17 闭环）** | 初审＋五次定向复核，B22-C31–C44 共 14 项全部 CLOSED，acceptance 4/4 满足（`batch-22-t05-04-claude-recheck-5.md`）；`device-resource-chain.md` 修订在工作区。六轮（初审＋五次定向复核）模型元数据均经调用方核验：CLI 输出 `modelUsage` 仅 `claude-opus-5-5` 单一模型、无 fallback 标记，均计入有效轮次 |

## 本会话审阅尝试作废记录（2026-10-15）

- T05-02/T05-03 初审曾派发两路 `claude-opus-5-5#xhigh` 子代理，均因子虚调用失败（Insufficient account funds）错误终止，未产生报告文件。
- T05-02 改派一路 `opencode/gpt-6.1-sol#xhigh` 子代理，同样因子虚余额不足失败，未产生报告文件。
- 按 fallback 条款，以上三轮全部弃用：不留档、不引用、不计数。实际执行的初审与复核均为另一会话完成（claude 报告在库），与本会话无关。

## 验收复核作废记录（2026-10-17）

- 整批验收定向复核首次以 `codex exec resume --last` 派发：resume 未继承原模型（stderr 警告"recorded with model `gpt-6.1-sol` but is resuming with `gpt-6-astra`"，banner 显示 effort ultra），且传输反复断流（Reconnecting 5/5 后 stream disconnected），exit 1，未产生报告或有效输出。按 fallback 条款该轮弃用：不留档（无文件可留）、不引用、不计数。改以显式模型/档位参数重派同一会话。

## 取证与结构

- T05-02/T05-03 来源准备由本会话完成（两路只读取证＋作者抽查），登记新增 6 项（ job-lifecycle/测试路径/Slurm 文档/GRES/cgroup/testsuite），记录见 `batch-22-t05-02-sources.md`、`batch-22-t05-03-sources.md`。
- 本机 curl 对 `raw.githubusercontent.com` DNS 失败未做字节级取回，核对经 webfetch 只读完成（已在来源记录声明）。
- `make check` 通过（96 content entries / 444 sources）；只验证结构与本地链接。正文均为 `draft`，无真实环境验证。
- 工作区 T05-01 会话的未提交改动始终予以保留，本会话只做追加式写入，未修改其文件。

## 待办

1. ~~T05-01 C32/C33/C34 关闭~~（2026-10-17 已闭环：第 29–33 次复核后 C30–C34 全部 CLOSED，见 `batch-21-t05-01-codex-recheck-33.md`）。
2. ~~T05-04 解除阻塞后的交付修订~~（2026-10-17 已闭环：初审＋五次定向复核后 B22-C31–C44 共 14 项全部 CLOSED，acceptance 4/4 满足，见 `batch-22-t05-04-claude-recheck-5.md`）。
3. 范围外跟进候选（初审报告明确不对 T05-01 提发现）：镜像运行时基线 §2 M-ID② 把“分配 ID”与 deviceIDStrategy 绑定的措辞，与 T05-04 C33 修订后“账本侧 ID 与策略无关、运行时 ID 才由策略决定”的口径存在张力；如需修订 T05-01 已闭环正文，应单独立项走流程，不在 T05-04 内顺带改。
4. ~~Batch 22 整批验收（四任务审阅闭环＋主题范围复核）另行记录~~（2026-10-17 完成：四任务与 T05-01 审阅均闭环；主题范围复核记录于 `docs/topic-coverage-audit.md` 与 `plans/topic-coverage.yaml` 的 Batch 22 更新——05.1-G1/G2、05.2-G1/G2、05.4-G1/G3 共 6 缺口关闭，05.1/05.4/05.5 主题验收属 Batch 23、05.2/05.3/05.7 属 Batch 24，本批无主题升为已覆盖；backlog 批次 22 置 done）。
5. ~~整批收尾独立审阅~~（2026-10-17，codex `gpt-6.1-sol / xhigh`，`batch-22-acceptance-codex-review.md`）：内容交付与 6 缺口关闭成立；发现 B22X-C01（T05-04 实为初审＋五次复核共六轮，审计误写"五轮"且核验范围概括越界）、B22X-C02（章节导航三处仍将 T05-02/T05-03 标"待审阅"），均 P3，已修订（审计轮次计数与核验范围、盘点两文件同口径、导航三处"审阅已闭环、仍 draft、未实测"并保留 05.2 主题验收边界）。定向复核（`batch-22-acceptance-codex-recheck.md`）：**C01/C02 均 CLOSED，新增 0，整批收尾通过**。审阅者从本地 CLI 会话记录核验初审轮执行上下文为单一 `gpt-6.1-sol / xhigh`、无 fallback（其报告 §9）；复核轮 banner 为 gpt-6.1-sol / xhigh（其间一次 resume 模型漂移轮已作废，见上文作废记录）。
