# 第二十一批 T04-06 第三次定向复核（作者第三轮修订后）

复核日期：2026-10-13（实际取证日）。正文 `updated_at: "2026-10-14"` 视为交付标签，不作为取证日期。

**结论：第三次定向复核通过。本轮范围 3 项（C04、C05、C07）：CLOSED ×3，OPEN ×0。合计 B21-C01–C09：CLOSED ×9，OPEN ×0，没有 P1/P2 遗留。** 本轮没有发现新的事实错误，也没有新增 ID。下文附非阻断提示，不作为关闭条件。

审阅者角色独立于作者修订角色。审阅模型为 `claude-opus-5-5`，由用户本次明确要求。这不是既有的 `gpt-6.1-sol / xhigh` 批量审阅约定，也不改写该约定；推理等级等运行元数据没有可核验记录，不补造。本轮只做只读取证：未改作者正文、来源记录、修订映射、登记、索引或计划，未执行 fio、rados bench、MLPerf Storage 或任何负载实测。模型审阅不构成硬件或现场验证。C01/C02/C03/C06/C08/C09 已在前次复核中 CLOSED，本轮不重开。

## 输入（SHA-256，本轮实算）

| 输入 | SHA-256 前缀 | 与任务给定值 |
|---|---|---|
| 正文 `knowledge/04-data-storage/storage-workload-baselines.md`（95 行） | `58aff9d32e90db01` | 一致 |
| 修订映射 `docs/research/batch-21-review-fixes.md`（第三轮节 L22–26） | `98607376fbd5df57` | 任务未给值，以现行文件为准 |
| 前次复核 `docs/research/batch-21-t04-06-claude-recheck-2.md` | `812a7aa5e921a622` | 任务未给值；剩余关闭条件的依据 |
| 任务计划 `plans/full-coverage-backlog.yaml`（T04-06 acceptance） | `f16309beadf5ae4f` | 与前三轮一致，未改 |

旁证（本库现行草稿）：`training-data-path.md` 节标题"每个阶段观察什么"在 L89；`local-and-shared-storage.md` §4"负载选型表（数据/模型/Checkpoint）"在 L94，其 L98/L100 行提到 knfsd-stats 服务器统计；§5"可读/重启/校验与冷热基线方法"在 L105，L113 为 drop_caches 冷基线。

一次源：沿用前次复核留在临时目录的 fio HOWTO.rst@fio-3.43，本轮重算 SHA-256 为 `f1b129ac…70e1285`，与前两轮字节相同，行号可直接比对。本轮只重读 L3691/L3709（"Cap"）与 L5172–5177（`IO complete`、`IO issued rwt`）。未重取 MLPerf 指南（本轮范围不涉及）。

## 逐项判定

### B21-C04 — P2 / CLOSED：上限值不等于实际发出负载

剩余关闭条件（前次复核 L72）：在 L73 补一句，说明 `rate`/`rate_iops` 设定值不能当作实际发起负载，须另行记录实际达到的发起量；如写"受 iodepth/numjobs 约束"须标为本库推论。

证据：正文 L73 现为

```text
`rate`/`rate_iops` 为**上限封顶**而非定速开环（HOWTO L3689），`rate_process=poisson` 调整到达过程；上限值不等于实际发出负载，实际发出速率须单独记录，否则不得以 cap 为横轴画饱和曲线；fio iodepth 为闭环、饱和段可能被压平**为本库推论**
```

- "上限值不等于实际发出负载"与 HOWTO L3691/L3709 的 "Cap" 一致。
- "实际发出速率须单独记录"满足记录要求；"否则不得以 cap 为横轴画饱和曲线"直接堵住了前次指出的误用。
- 正文没有写"受 iodepth/numjobs 约束"，因此不需要推论标注；既有的闭环推论仍保留**本库推论**标注。

剩余条件满足，CLOSED。

非阻断提示：

- 正文没有说实际发出速率从哪里取。HOWTO L5175–5177 的 `IO issued rwt` 记录已发出的读/写/trim 请求数及 short/dropped 数，可除以运行时间得到发出速率；L5172 `IO complete` 是完成计数。**审阅者自纠：** 前次复核 L72 括注"取 fio 输出中实际的 IOPS/带宽"把完成吞吐当作发起量，不准确。fio 汇总的 IOPS/带宽属于完成侧，应以 `IO issued rwt` 为发起侧依据。此项不影响关闭，因为正文本身没有采用那条括注。
- 前次的其余非阻断提示（补 `rate_iops` L3707、`rate_process` L3721–3729 的精确表述、L63 补 HOWTO L4787–4792 buffered 写错误漏检）本轮未处理，仍然有效。

### B21-C05 — P2 / CLOSED：计划 ID 全部链接化

剩余关闭条件（前次复核 L97）：L79"见 T04-02 §4"改为指向 `local-and-shared-storage.md` 的相对链接；L61 正文的"T04-02"删去或并入链接；L61 来源列改为链接或页面名。

证据：全文 grep `T0[0-9]-[0-9]{2}` 共命中 4 行（L61、L62、L71、L79），每处计划 ID 都在链接文字内：

```text
L61 正文：[T04-02](local-and-shared-storage.md) drop_caches 冷基线（见[本地与共享存储 §5](local-and-shared-storage.md)）
L61 来源：HOWTO；[T04-02](local-and-shared-storage.md)
L79：knfsd-stats 为 NFS 服务器侧统计（见 [T04-02 §4](local-and-shared-storage.md)选型表）
```

L62、L71 在前次已链接，本轮未变。L79 的链接目标 §4 是"负载选型表"，该表 L98/L100 写有 knfsd-stats 服务器侧统计，与正文说法对应。没有纯文本计划 ID 残留，CLOSED。

非阻断提示：L61 正文有两个链接都指向同一页（"T04-02"与"本地与共享存储 §5"），可合并为一个带节号的链接。

### B21-C07 — P2 / CLOSED：L46 指向精确节名

剩余关闭条件（前次复核 L111）：L46 把"计时口径"改为实际节名，或在链接上加锚点。

证据：正文 L46 现为

```text
2.6（消费侧分解，见[训练数据路径"每个阶段观察什么"](training-data-path.md)） | 真实加速器消费侧等待 | 存储后端归因（见[饥饿诊断指南"步骤与判断分支"](data-starvation-triage.md)）
```

"每个阶段观察什么"与 `training-data-path.md` L89 的标题完全一致；"计时口径"已删去。前次只作提示的"不覆盖"列链接也已指到节，与 `data-starvation-triage.md` L62 标题一致。L90 未变，仍指到两个节。CLOSED。

非阻断提示（沿用前次）：L87 的 `GET /?usage` 仍没有链接到 `object-and-parallel-storage.md`。

## 范围外观察（不重开，不新增 ID）

- §1 表 L45（MLPerf Storage 行）只有 3 个单元格，表头是 4 列：版本列括注里写了终点，"加速器端到端训练供给结论（…）"落在"测量终点"列，"不覆盖"列为空。这是表格结构问题，不是事实错误。另外，L45 自己写明终点"止于 host DRAM"、计算用 `sleep()` 代替，"测量终点"列却写"加速器端到端"，读者可能误读。建议作者下次修订时把这一行整理成 4 列，例如在"不覆盖"列写真实加速器计算。C02 已 CLOSED，本条不影响本轮结论。

## acceptance 对照（第三轮修订后）

| acceptance | 判定 | 相关项 |
|---|---|---|
| 1 工具版本与终点；文件/对象/加速器端到端分开 | 满足（L45 表格结构见范围外观察） | C01、C02 CLOSED |
| 2 工作负载矩阵 | 满足：十个维度都有参数；计划 ID 已全部链接 | C05 CLOSED |
| 3 完成指标、对照、饱和/可用容量 | 满足：上限与实际发出负载已区分，并要求单独记录 | C04 CLOSED |
| 4 计时实现/官方结果格式；无万能阈值或虚构数据 | 满足（本轮未改动相关段落） | C03 CLOSED |

## 结论

**第三次定向复核通过。本轮 C04、C05、C07 CLOSED（3/3）。B21-C01–C09 累计 CLOSED ×9，OPEN ×0。** 编辑与来源层面的审阅到此结束，T04-06 正文 `verification.status: source_checked` 在本复核范围内可以成立。文中工具行为都是文档层证据，未经实测，不得标为 reproduced；status 仍为 draft，是否升级由作者和用户决定。非阻断提示可在后续修订中处理，不需要再复核。

`make check`：PASS（92 content entries / 412 sources，作者复核报告交付后运行；只校验结构与本地链接）。
