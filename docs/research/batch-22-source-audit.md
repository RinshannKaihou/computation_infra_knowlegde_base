# 第二十二批来源审计（T05-02/T05-03/T05-05 通过；T05-01 已于 2026-10-17 闭环通过；T05-04 初审后第 1 轮修订完成、待定向复核）

更新日期：2026-10-15；2026-10-17 更新：T05-01 经第 29–33 次复核闭环（C30–C34 全部 CLOSED，见 `batch-21-t05-01-codex-recheck-33.md`），T05-04 前置随之解除并完成交付；同日 T05-04 初审（`batch-22-t05-04-claude-review.md`）判定需修订（B22-C31–C38，P1×1/P2×4/P3×3），作者第 1 轮修订已按关闭条件落实（含初审引证勘误一处：SLURM_JOB_GPUS 实际在 sbatch.html L2926–2928 而非 gres.html），待定向复核。本文件初版（T05-02/T05-03 草稿交付时）由本会话（Muse Spark，作者角色）编写；审阅闭环由另一并行会话的独立审阅角色完成，本会话未参与复核判断，以下通过结论均转述对应复核报告。

## 本批任务状态

| 任务 | 状态 | 依据 |
|---|---|---|
| T05-02 Kubernetes 作业全生命周期与控制器责任 | 通过 | 初审＋五次定向复核，B22-C01–C11 合计 CLOSED 11 / OPEN 0（`batch-22-t05-02-claude-recheck-5.md`） |
| T05-03 Slurm 作业生命周期、设备资源与状态参考 | 通过 | 初审＋四次定向复核，B22-C12–C21 累计 CLOSED 10 / OPEN 0（`batch-22-t05-03-claude-recheck-4.md`） |
| T05-05 扩展 gang、配额和双平台调度策略 | 通过 | 初审＋五次定向复核，B22-C22–C30 共 9 项全部 CLOSED（`batch-22-t05-05-claude-recheck-5.md`）；`admission-and-placement.md` 修订在工作区 |
| T05-01（Batch 21 补交，T05-04 前置） | **通过（2026-10-17 闭环）** | 至 `batch-21-t05-01-codex-recheck-33.md`：C30–C34 累计 CLOSED 5 / OPEN 0，Acceptance 4/4 完整通过；gpt-6.1-sol / xhigh，无 fallback 标记 |
| T05-04 扩展 GPU 与 Slurm 设备资源账本 | 初审需修订→第 1 轮修订完成，待定向复核（2026-10-17） | 初审 `batch-22-t05-04-claude-review.md`：B22-C31–C38（P1×1 C31 重启/重建/发现失败可取证却记 unknown；P2×4 C32–C35；P3×3 C36–C38）。修订：GPU 节增重启/重建表与发现失败分支、账本/运行时 ID 分列、健康标记粒度限制、回收验证改正；Slurm 节补相对编号/SLURM_JOB_GPUS/刷新四路径/就近引用；对照表与入口同步；`make check`/`make build` 通过（96/446）。模型元数据经调用方核验：CLI 输出 `modelUsage` 仅 `claude-opus-5-5` 单一模型，无 fallback 标记，本轮计入有效轮次 |

## 本会话审阅尝试作废记录（2026-10-15）

- T05-02/T05-03 初审曾派发两路 `claude-opus-5-5#xhigh` 子代理，均因子虚调用失败（Insufficient account funds）错误终止，未产生报告文件。
- T05-02 改派一路 `opencode/gpt-6.1-sol#xhigh` 子代理，同样因子虚余额不足失败，未产生报告文件。
- 按 fallback 条款，以上三轮全部弃用：不留档、不引用、不计数。实际执行的初审与复核均为另一会话完成（claude 报告在库），与本会话无关。

## 取证与结构

- T05-02/T05-03 来源准备由本会话完成（两路只读取证＋作者抽查），登记新增 6 项（ job-lifecycle/测试路径/Slurm 文档/GRES/cgroup/testsuite），记录见 `batch-22-t05-02-sources.md`、`batch-22-t05-03-sources.md`。
- 本机 curl 对 `raw.githubusercontent.com` DNS 失败未做字节级取回，核对经 webfetch 只读完成（已在来源记录声明）。
- `make check` 通过（96 content entries / 444 sources）；只验证结构与本地链接。正文均为 `draft`，无真实环境验证。
- 工作区 T05-01 会话的未提交改动始终予以保留，本会话只做追加式写入，未修改其文件。

## 待办

1. ~~T05-01 C32/C33/C34 关闭~~（2026-10-17 已闭环：第 29–33 次复核后 C30–C34 全部 CLOSED，见 `batch-21-t05-01-codex-recheck-33.md`）。
2. ~~T05-04 解除阻塞后的交付修订~~（2026-10-17 已交付并完成初审＋第 1 轮修订；待定向复核关闭 B22-C31–C38）。
3. 范围外跟进候选（初审报告明确不对 T05-01 提发现）：镜像运行时基线 §2 M-ID② 把“分配 ID”与 deviceIDStrategy 绑定的措辞，与 T05-04 C33 修订后“账本侧 ID 与策略无关、运行时 ID 才由策略决定”的口径存在张力；如需修订 T05-01 已闭环正文，应单独立项走流程，不在 T05-04 内顺带改。
4. Batch 22 整批验收（四任务审阅闭环＋主题范围复核）另行记录；T05-04 审阅闭环前不得宣布本批完成。
