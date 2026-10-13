# 第二十一批 T04-06 定向复核（作者首轮修订后）

复核日期：2026-10-13（实际取证日）。正文 `updated_at: "2026-10-14"` 视为交付标签，不作为取证日期。

**结论：T04-06 定向复核不通过。B21-C01–C09 共 9 项：CLOSED ×5（C01、C03、C06、C08、C09），OPEN ×4（C02、C04、C05、C07，均为 P2）。两项 P1（C01、C03）已关闭。** 剩余四项都是小范围的引用、措辞或链接问题，按下文剩余关闭条件修订后，再做一次定向复核即可。本轮没有新增发现 ID。修订中新出现的一处事实偏差按原 ID 追记在 C04 下（`rate` 是上限，不是定速发起）。这处偏差部分来自初审 C04 证据本身的表述，详见 C04。`make check` 通过（92 content entries / 412 sources），但它只校验结构与本地链接，不说明技术正确性。

审阅者角色独立于作者修订角色。审阅模型为 `claude-opus-5-5`，由用户本次明确要求。这不是既有的 `gpt-6.1-sol / xhigh` 批量审阅约定，也不改写该约定；推理等级等运行元数据没有可核验记录，不补造。本轮只做只读取证：未改作者正文、来源记录、修订映射、登记、索引或计划，未执行 fio、rados bench、MLPerf Storage 或任何负载/容量实测。模型审阅不构成硬件或现场验证。

## 输入（SHA-256，本轮实算）

| 输入 | SHA-256 前缀 | 与任务给定值 |
|---|---|---|
| 正文 `knowledge/04-data-storage/storage-workload-baselines.md`（95 行，reference / draft） | `83d1e8aae5c73068` | 一致 |
| 作者来源记录 `docs/research/batch-21-t04-06-sources.md`（16 行） | `7f0df520f2eb6c37` | 一致 |
| 修订映射 `docs/research/batch-21-review-fixes.md`（T04-06 节 L2–13） | `553ef02d0651ea74` | 一致 |
| 初审报告 `docs/research/batch-21-t04-06-claude-review.md` | `b4aba67c0cfca2f0` | 任务未给值；按说明，作者只机械对齐了旧文件名链接 |
| 任务计划 `plans/full-coverage-backlog.yaml`（T04-06 L5248–5288） | `f16309beadf5ae4f` | 与初审记录一致，未改 |
| 来源登记 `sources/registry.yaml`（412 项；fio L5112、rados L5126） | `550dc68e29d2d0e6` | 一致 |

旁证（按本库现行草稿核对，未重新取其一次源）：`local-and-shared-storage.md`（T04-02 §4 L94–100 knfsd-stats 为服务器侧、§5 L105 冷热基线）、`object-and-parallel-storage.md` L79（`GET /?usage` 为用量统计）、`training-data-path.md` 与 `data-starvation-triage.md` 的节标题、`04-data-storage/index.md` 工作区 diff（related_id 与 04.5 链接已指向新名）、`docs/full-coverage-roadmap.md` L190。

## 一次源取证（审阅者独立重取）

全部用 `curl -sSL` 或 `git ls-remote` 只读获取，默认 TLS 校验，HTTP 均为 200。原文只存放在临时目录 `/tmp/b21re6/`，未入库。**五份原文的 SHA-256 与初审取得的字节完全相同**，因此行号可以直接沿用初审取证。本轮仍逐行重读了正文引用的每个行号。

| 来源 | SHA-256（原文） | 本轮核对 |
|---|---|---|
| fio tag | — | `refs/tags/fio-3.43` → tag 对象 `bef04e7badc1…`，`^{}` → commit `d2dcd7e053d1…`；未见 fio-3.44 及以上 tag。正文 L41 与登记 L5117 的 tag 对象/commit 记法正确。 |
| fio HOWTO.rst@fio-3.43 | `f1b129ac…70e1285` | 正文引用的行号均与所述条目对应：L205 `--status-interval`（"cumulative … does *not* provide per-period measurements"，与 json 合用需拆分）、L699 `time_based`、L711 `ramp_time`、L1200 `direct`、L1472 `fsync`、L1519 `end_fsync`、L1974 `invalidate`、L2273 `rados`（via librados）、L2283–2290 `http`（"only supports direct IO of iodepth=1 … scale this via numjobs"，"blocksize defines the size of the objects"，"TRIM is translated to object deletion"）、L2422–2450 元数据引擎、L3230 `http_mode`、L3541 `iodepth`、L3689 `rate`、L3747 `latency_target`、L4403 `steadystate`、L4537 `write_lat_log`、L4575 `log_avg_msec`、L4749–4752 `lat_percentiles`（"sum of submission latency and completion latency"）、L4754 `percentile_list`、L5060–5080 slat/clat、L5334 terse v3、L5671 Client/Server、L5764 terse 差异。另核对正文未用但与 C04/C05 相关的条目：`rate` L3691 "Cap the bandwidth"、`rate_iops` L3709 "Cap the bandwidth to this number of IOPS"、`rate_process` L3721–3729（linear 的延迟"gets adjusted based on I/O completion rates"）、`latency_run` L3767–3771（按调整 queue depth 寻找满足目标的点）、`continue_on_error` L4779（"Normally fio will exit the job on the first observed failure"；启用后追加 total error count 与 first error）。 |
| fio io_u.c@fio-3.43 | `a1b8dd59…6bca5` | `account_io_completion` L2083：L2097 `llnsec = ntime_since(&io_u->issue_time, …)`，经 L2124 `add_clat_sample` 记为 clat；L2102 `tnsec = ntime_since(&io_u->start_time, …)`，经 L2103 `add_lat_sample` 记为 lat。正文 L77 所述成立。另见 L2115：`latency_target` 判定用的是 tnsec（总延迟）。 |
| rados(8) Squid | `712a3248…b229f8` | `bench seconds mode [ -b objsize ] [ -t threads ]`；读基准前须先以 `--no-cleanup` 跑 write；默认 4 MB / 16 线程；`--run-name` "useful for benchmarking a workload test from multiple clients"；"-b objsize option is valid only in write mode"；"write and seq must be run on the same host otherwise the objects created by write will have names that will fail seq"；`-O/--object-size` "Set the object size for put/get ops and for write benchmarking"；`--max-objects`。正文 L44/L58/L59 所述成立。 |
| MLPerf Storage v2.0 Submission_guidelines.md@7e71ca16 | `d107aa39…a1e10cf` | L79 `sleep()`；L94 host DRAM 终点、不含 accelerator memory 传输；L234–237 duration 取进程最大值、throughput 取进程最小值；L311 连续 5 次均值；L333 训练指标 "samples per second, subject to a minimum accelerator utilization (AU)"；L340 首个 step I/O 排除；L353 checkpoint 读/写带宽＋写完到可读的时间；L407 warm-up；L408 "For Training benchmarks, the dataset size must be at least 5x"；L431 HOST_MEMORY_MULTIPLIER = 5；L570 `mlperf_storage_report.json`（rank0 上用 `benchmark.sh reportgen` 生成）。正文 L45/L56/L79 内容均成立，但 L45 未给行号（见 C02）。 |
| Lustre Operations Manual | `63b09d06…a0d8c` | Ch.12 "Monitoring a Lustre File System"（§12.2 Jobstats；§12.4 CollectL："another tool that can be used to monitor a Lustre file system"，外部站点 collectl.sourceforge.net）；Ch.19 "Managing File Layout (Striping) and Free Space"，`lfs setstripe [--size] [--stripe-count] … [--index]`；Ch.32 "Testing Lustre Network Performance (LNet Self-Test)"；Ch.33 I/O Kit：sgpdd-survey "bare metal performance of devices while bypassing the kernel block device layers"，obdfilter-survey 在 OSS 上直接测 OST，或经网络测；ost-survey 用 `lfs setstripe` 对每个 OST 写文件并比较读写速度；§33.5 mds-survey。brw_stats 为 "Histogram data characterizing I/O requests to the OSTs"（§39.3.5）。正文 L47/L48/L60 所述成立。 |

取证限制：

- 未检索 Ceph 官方是否另有 RGW 负载基准文档，也未验证 fio `http`/`rados` 引擎对 Squid RGW/RADOS 的兼容性。
- 未审计 fio slat 取样、百分位桶算法与 client/server 汇总的源码实现，只核对了 HOWTO 文字和 lat/clat 两个取样点。
- MLPerf DLIO 实现与 `mlperf_storage_report.json` 字段未取。
- PyTorch profiler/DataLoader 与内核 NFS 文档本轮未重取。正文对它们没有新的具体主张，只链接本库已有页面。
- 未执行任何工具或实测。

## 逐项判定

### B21-C01 — P1 / CLOSED：对象接口终点

证据：

- 正文 L42 新增"fio（对象接口）"行：`http` ioengine、`http_mode=s3`，终点为"S3 请求完成（客户端侧）"。限制写明了 direct IO、iodepth=1、靠 numjobs 扩展、`blocksize` 即对象大小、TRIM 即对象删除，与 HOWTO L2283–2290 一致。同一行写明"与块/文件层 iodepth 结果不可直接对比"，以及"对 Squid RGW 的兼容性未验证（unknown）"。
- 原"不覆盖：对象语义"现在只留在"fio（块/文件）"行（L41）。按行拆分后，这个限定只针对块/文件引擎，成立。
- L43 中 fio `rados` 引擎、L44 中 rados bench 都标为 RADOS 层，并注明"不是对象接口（RGW S3）结果"。
- L17 summary 改为"文件/对象接口/RADOS/加速器端到端终点分开"，与表格一致。
- 来源记录 L9 给出 http L2283–2290、http_mode L3230、rados L2273。

非阻断提示：L44 与登记 L5139 notes 仍写"RGW 侧官方负载基准未找到"。初审关闭条件中的改述要求以"不采用 fio http 引擎"为前提；作者已采用该引擎，因此不作为剩余条件。若要更准确，可改为"Ceph 侧未检索到"，因为"未找到"暗示已做过检索。

### B21-C02 — P2 / OPEN：MLPerf 终点内容已改正，但指标与终点未逐条引行号

已满足：正文 L45 终点为 host DRAM，注明加速器计算以 `sleep()` 模拟、不含 H2D 传输。训练（samples/s＋最小 AU）与 checkpoint（读/写带宽＋跨 host 可读时间）已分列，并注明与 profiler"真实加速器消费侧"不可互比。内容与指南 L79/L94/L333/L353 一致。

未满足：初审关闭条件要求"逐条引指南行或节号"。正文 L45 只写"v2.0 提交指南"，没有行号。来源记录 L11 列了 sleep L79 和 DRAM L94，但训练指标（L333，§4.1）与 checkpoint 指标（L353，§4.2）在正文和来源记录中都没有定位。

剩余关闭条件：在正文 L45 或来源记录 L11 补上训练指标 L333–340（§4.1）与 checkpoint 指标 L353（§4.2）的定位。建议正文 L45 同时给出 L79/L94。

### B21-C03 — P1 / CLOSED：分阶段计时与跨客户端汇总

证据：

- 正文 L77 写清了 fio 计时：slat、clat 与 lat = slat + clat（HOWTO L5060–5080、L4749–4752），取样点 io_u.c L2097/L2102（已逐行重读确认），`ramp_time` 不计入，`--status-interval` 输出累计值且与 json 合用须拆分，逐段序列使用 `write_lat_log`/`log_avg_msec`。
- L79 写了跨客户端汇总：fio client/server（terse 输出略有差异，L5764）；rados `--run-name` 与同 host 约束；MLPerf 的 duration 取最大值、throughput 取最小值、5 次均值和 `mlperf_storage_report.json`（来源记录 L11 给出 L234–237/L311/L570）。knfsd-stats 改标为服务器侧，与 T04-02 §4 L98/L100 一致；NFS 客户端统计记为 unknown。"不同工具计时口径不同，结果不得直接互比"已写明。
- 四条关闭条件全部满足。L79 中"见 T04-02 §4"是计划 ID 而非链接，归入 C05 处理。

### B21-C04 — P2 / OPEN：方法已引 fio 条目，但"定速发起"与来源不符，推论未标注

已满足：

- `latency_target`/`latency_window`/`latency_percentile`/`latency_run` 与 `rate`/`rate_iops`/`rate_process=poisson` 已引用（正文 L73，来源记录 L9 给出 L3689/L3747）。
- 发起负载与完成吞吐的区分已写。
- 指标已落到 terse v3 字段（L69，L5334 字段核对属实）；后端容量与网络占用记为 unknown。
- 三组对照的记录要求已写（L71）。

**追记（新事实偏差，归入原 ID）：**

- 正文 L73 写"以 `rate`/`rate_iops`＋`rate_process=poisson` 定速发起"。HOWTO L3691、L3709 对这两个选项的原文都是 "Cap"，即**上限**。`rate_process` 的默认值 linear 会"根据 I/O 完成速率调整"间隔（L3723–3725）；poisson 只改变提交间隔的分布（L3725–3729）。原文没有承诺按设定速率开环发起。在未完成 I/O 达到 iodepth/numjobs 上限时，实际发起仍会受限。所以"定速发起"超出了来源支持的范围。这一偏差部分源自初审 C04 证据中"要画出饱和曲线需要定速发起，即 `rate`/`rate_iops` 与 `rate_process=poisson`"的表述；初审把它写成了来源事实，本轮予以更正。
- 同段标题写"引 fio 官方机制，非本库自创"，但段内"fio iodepth 为闭环，饱和段会被压平"与"可用容量按延迟/失败门限读取"在 HOWTO 中没有对应原文。前者是推论（同样出自初审证据），后者中的"失败门限"是本库约定；只有"延迟门限"有 `latency_target` 支持。

剩余关闭条件：

1. 把"定速发起"改为"以 `rate`/`rate_iops` 设定发起**上限**（HOWTO L3689/L3707 "Cap"），`rate_process=poisson` 改变提交间隔分布（L3721）"。补充说明实际发起速率仍受 iodepth/numjobs 约束，须另行记录实际达到的发起量。
2. 把"iodepth 为闭环、饱和段被压平"标为本库推论。"可用容量按失败门限读取"标为本库约定，延迟门限部分保留对 `latency_target` 的引用。删除或限定"非本库自创"。

### B21-C05 — P2 / OPEN：参数映射已完成，计划 ID 仍在读者文本中；失败语义 unknown 与已取源不符

已满足：十个矩阵行都给出了工具参数（L56–65），所引 HOWTO 行号核对属实。缓存行补充了 `direct`/`invalidate`，rados 读后缓存已标为本库推论（L61）。后端空间定义为本库约定（L64）。

未满足：

- 初审关闭条件"计划 ID 改为文档链接"没有落实，但修订映射 `batch-21-review-fixes.md` L9 写的是"计划 ID 改链接"。正文读者可见文本仍有计划 ID：L61 来源列"HOWTO；T04-02"、L62"NFS/RGW 语义见 T04-02/03"、L71"冷态证据引 T04-02 §5"、L79"见 T04-02 §4"。只有 L61 正文中的"本地与共享存储 §5"一处是链接。
- **追记：** 失败重试行 L63 写"fio 与 rados bench 的重试/错误语义未在已取源中核对（unknown）"。但作者已取的 HOWTO L4779 `continue_on_error` 说明了 fio 的错误语义：默认在首个失败处退出；启用后对 EIO/EILSEQ 继续运行，并追加错误计数与首个错误。这一行也直接影响 §3"失败"指标能否采集。fio 一侧不应记为 unknown；rados bench 一侧仍为 unknown。

剩余关闭条件：

1. 上述四处计划 ID 改为相对链接：`local-and-shared-storage.md` 对应 T04-02，`object-and-parallel-storage.md` 对应 T04-03，节号可写在链接文字中。
2. 失败重试行引 HOWTO `continue_on_error`（L4779），写明默认首错退出；rados bench 的重试语义保留 unknown。

### B21-C06 — P2 / CLOSED：Lustre 官方性能工具与计数器

证据：正文 L47 新增 I/O Kit（sgpdd-survey 裸设备、obdfilter-survey OST、ost-survey 客户端到 OST、mds-survey §33.5）与 LNet Self-Test（Ch.32）行，并写明与文件层 fio 不可互比。L48 改为"含义已核对 Jobstats 与 brw_stats，其余 unknown"，并说明 CollectL 是外部工具（与手册 §12.4 一致）。L88 的 Lustre 行与之一致。章节号与工具描述均已对照手册核实。

非阻断提示：L48 只写了"已核对"，没有给出含义本身或节号。建议补一句"brw_stats 为发往 OST 的 I/O 请求直方图（§39.3.5）；Jobstats 工作方式见 §12.2"，并把来源记录 L12 从章号细化到节号。

### B21-C07 — P2 / OPEN：实现对照表与长尾已补；训练关联只链接到页面，未到节

已满足：

- L83–88 是四行"实现 × 工具/终点 × 统计入口 × 空缺"表，空缺记为 unknown。
- L90 补了长尾说明（`percentile_list`＋按时间的 lat log）。
- 训练关联链接到两页。

未满足：初审关闭条件是"训练关联链接到上述两页的**具体节**"。L46 与 L90 只链接到页面。L46"计时口径"在 `training-data-path.md` 中没有同名节。

剩余关闭条件：L90 和 L46 指明具体节，用节名或锚点均可，例如 `training-data-path.md` 的"每个阶段观察什么"（L89）、"为什么低设备利用率不能证明存储慢"（L109），以及 `data-starvation-triage.md` 的"步骤与判断分支"（L62）。

非阻断提示：L87 的 `GET /?usage`（用量非性能）在本页没有来源或链接。它的依据在 T04-03 `object-and-parallel-storage.md` L79，建议加链接。

### B21-C08 — P2 / CLOSED：路径/ID、source_refs 与来源记录

证据：

- 文件名与 ID 已改为计划 target `storage-workload-baselines.md` / `data-storage.storage-workload-baselines`，与 plan L5261–5262、roadmap L190 一致。全库（不含 build/）已没有旧名残留；index 的 related_id 与 04.5 链接都已指向新名。
- `source_refs` 删除了 nfs(5)，加入 `src.kernel.docs-nfs-v6.16`（knfsd-stats）。两个 PyTorch 来源对应 L46 工具行及其链接页，可以接受。
- `verification.notes` 改为本页实际使用的核对范围。登记 src.fio.repo-3.43 已补 tag 对象 `bef04e7b` 与 io_u.c 行。来源记录 L9–12 已按条目/行号列出（C02 的缺口另计）。

非阻断提示：

- 来源记录没有 knfsd-stats（`src.kernel.docs-nfs-v6.16`）与 PyTorch 的行。正文对它们只是转引本库页面，不阻断，但建议补一行"经 T04-02/训练数据路径转引"。
- 登记 src.ceph.docs-rados-man-squid 的 revision（L5131）仍写"核对 bench 写基准选项（block/object 大小、seq/rand、omap）"，与本页现用的核对点（4 MB/16 线程/`--no-cleanup`/`--run-name`/同 host）不完全一致，可以顺手更新。

### B21-C09 — P3 / CLOSED：工具行描述

证据：L50 已把 verify 单列为"完整性附加阶段……不列为性能终点"。L44 rados bench 行补了默认 4 MB/16 线程、`-b` 只在 write 模式有效、seq/rand 依赖 `--no-cleanup`，并已删除与 omap 相关的不精确表述。以上均与 rados(8) 原文一致。

## acceptance 对照（修订后）

| acceptance | 判定 | 相关项 |
|---|---|---|
| 1 工具版本与终点；文件/对象/加速器端到端分开 | 满足：三层终点与 RADOS 层分开；MLPerf 内容正确，只缺行号 | C01 CLOSED；C02 OPEN（引用） |
| 2 工作负载矩阵 | 基本满足：十个矩阵行都已映射参数；计划 ID 残留，fio 失败语义误记为 unknown | C05 OPEN |
| 3 完成指标、对照、饱和/可用容量 | 基本满足：方法与指标已落到工具；"定速发起"超出来源，推论未标 | C04 OPEN |
| 4 计时实现/官方结果格式；无万能阈值或虚构数据 | 满足：全文无阈值、无测量数据 | C03 CLOSED |

## 结论

**T04-06 定向复核不通过。CLOSED 5 项（C01、C03、C06、C08、C09），OPEN 4 项（C02、C04、C05、C07，均为 P2），没有 P1 遗留。** 作者按 C02/C04/C05/C07 的剩余关闭条件修订后，须再做一次定向复核。C04 下的追记更正了初审证据中关于 `rate` 的表述，修订时应以 HOWTO 原文（"Cap"）为准。正文 `verification.status: source_checked` 在剩余项关闭前仍不应视为成立。本复核只覆盖编辑与来源层面；文中所有工具行为都是文档或源码层证据，未经实测，不得标为 reproduced。
