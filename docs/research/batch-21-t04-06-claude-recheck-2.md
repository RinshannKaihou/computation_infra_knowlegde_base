# 第二十一批 T04-06 第二次定向复核（作者第二轮修订后）

复核日期：2026-10-13（实际取证日）。正文 `updated_at: "2026-10-14"` 视为交付标签，不作为取证日期。

**结论：第二次定向复核不通过。本轮范围 4 项：CLOSED ×1（C02），OPEN ×3（C04、C05、C07，均为 P2）。合计 B21-C01–C09：CLOSED ×6，OPEN ×3，没有 P1 遗留。** 三项 OPEN 各只差一处：C04 缺少"实际发起量须另行记录"的说明，C05 在 L61 和 L79 仍有未链接的计划 ID，C07 的 L46 仍未指到节。本轮没有发现新的事实错误，也没有新增 ID。`make check` 结果：PASS（92 content entries / 412 sources，作者复核报告交付后运行；只校验结构与本地链接）。

审阅者角色独立于作者修订角色。审阅模型为 `claude-opus-5-5`，由用户本次明确要求。这不是既有的 `gpt-6.1-sol / xhigh` 批量审阅约定，也不改写该约定；推理等级等运行元数据没有可核验记录，不补造。本轮只做只读取证：未改作者正文、来源记录、修订映射、登记、索引或计划，未执行 fio、rados bench、MLPerf Storage 或任何负载实测。模型审阅不构成硬件或现场验证。C01/C03/C06/C08/C09 已在前次复核中 CLOSED，本轮不重开。

## 输入（SHA-256，本轮实算）

| 输入 | SHA-256 前缀 | 与任务给定值 |
|---|---|---|
| 正文 `knowledge/04-data-storage/storage-workload-baselines.md`（96 行） | `7f2d48b63e0fb878` | 一致 |
| 修订映射 `docs/research/batch-21-review-fixes.md`（第二轮节 L15–20） | `f3c1a905bb552260` | 一致 |
| 前次复核 `docs/research/batch-21-t04-06-claude-recheck.md` | `21d5063ce78f52f5` | 任务未给值；作为剩余关闭条件的依据 |
| 任务计划 `plans/full-coverage-backlog.yaml`（T04-06 acceptance） | `f16309beadf5ae4f` | 与前两轮一致，未改 |

旁证：`training-data-path.md` 与 `data-starvation-triage.md` 的节标题，以及 `local-and-shared-storage.md` 的节标题（§4 L94、§5 L105），均按本库现行草稿核对。

## 一次源取证（审阅者独立重取）

用 `curl -sSL` 只读获取，默认 TLS 校验，HTTP 均为 200。原文只存放在临时目录 `/tmp/b21re7/`，未入库。

| 来源 | SHA-256（原文） | 与前两轮 |
|---|---|---|
| fio HOWTO.rst@fio-3.43（raw.githubusercontent.com） | `f1b129ac…70e1285` | 字节相同，行号可直接比对 |
| MLPerf Storage Submission_guidelines.md@7e71ca16 | `d107aa39…a1e10cf` | 字节相同 |

本轮逐行重读了以下位置：

- MLPerf：§2.1 Training（L73–96）中的 L79 `sleep()` 与 L94 host DRAM 终点；§4.1 "Training Workloads"（标题 L331），训练指标 L333 到 AU=100% 说明 L342；§4.2 "Checkpoint Workloads"（标题 L351），checkpoint 指标 L353。
- fio：`rate` L3689（L3691 "Cap the bandwidth"）；`rate_iops` L3707（L3709 "Cap the bandwidth to this number of IOPS"）；`rate_process` L3721–3729（linear 的延迟"gets adjusted based on I/O completion rates"，poisson 按泊松过程提交）；`latency_target` L3747 至 `latency_run` L3767–3771；`continue_on_error` L4779–4785（默认首错退出；启用后对 EIO/EILSEQ 继续，并追加错误总数与首个错误）以及 L4787–4792 关于 buffered 写错误可能漏检的说明。

取证限制：rados bench 的重试语义本轮未取（正文已记为 unknown）。fio `rate` 在 iodepth 用满时实际能达到的发起速率，本轮没有核对源码，只依据 HOWTO 文字。未执行任何工具。

## 逐项判定

### B21-C02 — P2 / CLOSED：MLPerf 终点节号/行号

证据：正文 L45 写为

```text
终点 L94：止于 host DRAM；加速器计算以 `sleep()` 代替 L79；训练指标 samples/s＋最小 AU §4.1 L333–342；checkpoint 读/写带宽＋跨 host 可读时间 §4.2 L353
```

节号与行号都和指南原文对上：L333 是训练指标，L342 是 AU 段末行，L353 是 checkpoint 指标，§4.1 与 §4.2 的标题分别在 L331 和 L351。前次复核的剩余条件（补 L333–340 §4.1 与 L353 §4.2，并建议正文给出 L79/L94）全部满足。

非阻断提示：L79/L94 属于 §2.1，可在正文补上节号，与 §4.1/§4.2 写法一致。

### B21-C04 — P2 / OPEN：rate 上限已纠正，推论和约定已标注；缺少"实际发起量须记录"

已满足：

- 正文 L73 已删掉"定速发起"，改为

  ```text
  `rate`/`rate_iops` 为**上限封顶**而非定速开环（HOWTO L3689），`rate_process=poisson` 调整到达过程
  ```

  与 HOWTO L3691/L3709 的 "Cap" 一致。全文也已没有"定速"。
- "fio iodepth 为闭环、饱和段可能被压平"已标为**本库推论**；"按失败门限读取"已标为**本库约定**；延迟门限仍引 `latency_target`（L3747–3771，范围覆盖 `latency_run`）；"非本库自创"已删除（全文 grep 无匹配）。剩余条件 2 满足。
- 失败重试（L63，修订映射把它归在 C04 下，前次复核记在 C05 条件 2）：

  ```text
  fio 默认首次失败即退出，`continue_on_error` 可继续非致命错误并统计错误数（HOWTO L4779）；rados bench 重试语义未核对（unknown）
  ```

  与 HOWTO L4779–4785 一致，rados 一侧保留 unknown。满足。

未满足：剩余条件 1 的后半句"补充说明实际发起速率仍受 iodepth/numjobs 约束，须另行记录实际达到的发起量"没有落到正文。L73 只写了"区分**发起负载**与**完成吞吐**"，没有告诉读者：`rate` 只是上限，设了并不等于真的按这个速率发起了。读者如果把设定值当作横轴的发起负载来画饱和曲线，就会犯前次复核纠正的同一个错误，只是换了个位置。

剩余关闭条件：在 L73 补一句，说明 `rate`/`rate_iops` 设定值不能当作实际发起负载，须另行记录实际达到的发起量（取 fio 输出中实际的 IOPS/带宽）。"受 iodepth/numjobs 约束"如果写进去，须标为本库推论，因为 HOWTO 没有对应原文。

非阻断提示：

- L73 只引了 `rate` 的 L3689，可补 `rate_iops` L3707 与 `rate_process` L3721。
- "`rate_process=poisson` 调整到达过程"可以写得更精确："按泊松过程提交；默认 linear 按完成速率调整间隔"（L3723–3729）。
- L63 的"失败"指标可补 HOWTO L4787–4792：buffered 写的设备错误可能被 fio 漏检，除非使用 `sync`/`direct` 或 `fsync`/`fdatasync`。这关系到 §3"失败"计数是否完整。

### B21-C05 — P2 / OPEN：计划 ID 只改了两处，L61 与 L79 仍是纯文本

已满足：

- L62 durability 行的 NFS/RGW 语义已改为相对链接，分别指向 `local-and-shared-storage.md` 与 `object-and-parallel-storage.md`，链接文字为 T04-02/T04-03。
- L71 冷态证据已改为指向 `local-and-shared-storage.md` 的链接，链接文字为"T04-02 §5"，与该页 §5（L105）对应。

链接文字仍用计划 ID，这一点前次条件允许（"节号可写在链接文字中"），不再追究。

未满足：全文 grep `T0[0-9]-[0-9]{2}` 后，仍有三处没有链接的计划 ID：

- L61 正文："T04-02 drop_caches 冷基线（见[本地与共享存储 §5]…）"。后面的链接已指向正确页面，但前面的"T04-02"仍是纯文本。
- L61 来源列："HOWTO；T04-02"。
- L79："knfsd-stats 为 NFS **服务器侧**统计（见 T04-02 §4）"。前次复核点名的四处之一，本轮没有改。

修订映射 L19 写的是"计划 ID 改链接（durability/对照行）"，范围小于前次关闭条件列出的四处。

剩余关闭条件：L79 的"见 T04-02 §4"改为指向 `local-and-shared-storage.md` 的相对链接（§4 为该页 L94）。L61 正文中的"T04-02"删掉，或并入后面的链接；L61 来源列改为链接或页面名。

### B21-C07 — P2 / OPEN：L90 已指到节，L46 未改

已满足：L90 的链接文字已带节名，分别是"训练数据路径'每个阶段观察什么'"和"饥饿诊断指南'步骤与判断分支'"。两个节名与目标页标题完全一致（`training-data-path.md` L89、`data-starvation-triage.md` L62）。

未满足：前次条件要求 L90 **和 L46** 都指明具体节。L46 仍为

```text
2.6（消费侧分解，见[训练数据路径](training-data-path.md)计时口径）
```

`training-data-path.md` 没有叫"计时口径"的节（全页标题见旁证），所以读者找不到它指的是哪一节。修订映射 L20 写的是"训练关联精确到节"，没有说明 L46 未改。

剩余关闭条件：L46 把"计时口径"改成实际节名（例如"每个阶段观察什么"或"用相邻边界建立瓶颈证据"，L125），或在链接上加锚点。L46 不覆盖列中的"饥饿诊断指南"链接也宜同样指到节，但这一处不作为关闭条件。

非阻断提示（沿用前次）：L87 的 `GET /?usage` 仍没有指向 `object-and-parallel-storage.md` 的链接。

## acceptance 对照（第二轮修订后）

| acceptance | 判定 | 相关项 |
|---|---|---|
| 1 工具版本与终点；文件/对象/加速器端到端分开 | 满足 | C01、C02 CLOSED |
| 2 工作负载矩阵 | 基本满足：十个维度都有参数；失败重试已引 `continue_on_error`；计划 ID 链接仍有残留（编辑问题，不涉及内容） | C05 OPEN |
| 3 完成指标、对照、饱和/可用容量 | 基本满足："定速"偏差已纠正，推论和约定已标注；缺少实际发起量的记录要求 | C04 OPEN |
| 4 计时实现/官方结果格式；无万能阈值或虚构数据 | 满足（本轮未改动相关段落） | C03 CLOSED |

## 结论

**第二次定向复核不通过。本轮 C02 CLOSED；C04、C05、C07 OPEN（均为 P2）。累计 CLOSED 6 项（C01、C02、C03、C06、C08、C09），OPEN 3 项（C04、C05、C07）。** 三项剩余条件都只涉及正文一两行（L73、L61/L79、L46），不需要重新取源。修订后须再做一次定向复核，只核对这三处。正文 `verification.status: source_checked` 在剩余项关闭前仍不应视为成立。本复核只覆盖编辑与来源层面；文中工具行为都是文档层证据，未经实测，不得标为 reproduced。
