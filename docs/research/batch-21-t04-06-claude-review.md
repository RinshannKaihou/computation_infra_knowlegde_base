# 第二十一批 T04-06 初审

审阅日期：2026-10-13（实际取证日）。正文 `updated_at: "2026-10-14"` 视为交付标签，不作为本轮取证日期；输入以下表 SHA-256 识别。

**结论：T04-06 需修订。新增 9 项发现（B21-C01–C09）：P1 ×2、P2 ×6、P3 ×1，全部 OPEN。** acceptance 1 与 4 各有一项 P1 缺口；acceptance 2、3 有 P2 缺口。正文没有万能阈值，也没有虚构的测量数据，这一点满足 acceptance 4 后半句。fio tag/commit/许可、rados(8) bench 段落、Lustre 手册章号（Ch.12/19/39）都经本轮一次源核对属实。`make check` 通过（92 content entries / 412 sources），但它只校验结构与本地链接，不说明技术正确性。

审阅者角色独立于作者。审阅模型为 `claude-opus-5-5`，由用户本次明确要求试用。这不是既有的 `gpt-6.1-sol / xhigh` 批量审阅约定，也不改写该约定；推理等级等运行元数据没有可核验记录，不补造。本轮只做审阅和只读取证：未改作者正文、来源记录、登记、索引或计划，未执行 fio、rados bench、MLPerf Storage 或任何负载/容量实测。模型审阅不构成硬件或现场验证。

## 输入（以 SHA-256 识别）

| 输入 | SHA-256 |
|---|---|
| [T04-06 正文](../../knowledge/04-data-storage/storage-workload-baselines.md)（67 行，reference / draft） | `0be36fdd9afdb2daa4b7b3e1ce694e85017b2b932256e1c6a6e33203435d346a` |
| [作者来源记录](batch-21-t04-06-sources.md)（16 行） | `2247f634b1201b1bebeba9c559d87cf7f857d6be2f54d6b3ea442ddb3b3cc263` |
| [任务计划](../../plans/full-coverage-backlog.yaml)（T04-06 L5248–5288，acceptance L5265–5269） | `f16309beadf5ae4f28d5fc7428a2348bea0cf08d155d57730a4d817cfcdd3e96` |
| [来源登记](../../sources/registry.yaml)（新登记 src.fio.repo-3.43 L5112、src.ceph.docs-rados-man-squid L5126） | `82e54c7ef9dfe90e2b2f01ca605adbbc4f25e08e6194c070907158fd07ab7961` |

旁证（按本库现行草稿核对，未重新取其一次源）：`local-and-shared-storage.md`（T04-02，§5 冷基线与 drop_caches、§4 knfsd-stats 用法）、`04-data-storage/index.md` 工作区 diff（新增 related_id 与 04.5 条目）、`docs/full-coverage-roadmap.md` L190。正文 `related_ids` 四个 ID 都能解析到已有文件。

## 一次源取证（审阅者独立获取）

全部用 `curl -sSL` 或 `git ls-remote` 只读获取，默认 TLS 校验；HTTP 均为 200。HTML 去标签后按文字核对，不只判可达性。原文只存在临时目录 `/tmp/b21rev6/`，未入库。

| 来源（登记 ID） | URL | SHA-256（原文） | 核对点与结果 |
|---|---|---|---|
| fio tag（src.fio.repo-3.43） | `git ls-remote https://github.com/axboe/fio.git` | — | `refs/tags/fio-3.43` → tag 对象 `bef04e7b…`，`^{}` → commit `d2dcd7e053d1…`。与登记"所指 commit d2dcd7e0"一致。未发现 fio-3.44 及以上 tag。 |
| fio COPYING@fio-3.43 | [raw](https://raw.githubusercontent.com/axboe/fio/fio-3.43/COPYING) | `8177f975…b880643` | 首行 "GNU GENERAL PUBLIC LICENSE Version 2, June 1991"，与登记一致。 |
| fio HOWTO.rst@fio-3.43 | [raw](https://raw.githubusercontent.com/axboe/fio/fio-3.43/HOWTO.rst) | `f1b129ac62423ef1fb6e9a981846b766929703600b1dfc0cfb733810770e1285` | 矩阵条目均存在：`numjobs` L677、`time_based` L699、`ramp_time` L711（"before logging any performance numbers"）、`direct` L1200、`fsync` L1472、`end_fsync` L1519、`invalidate` L1974、`iodepth` L3541、`verify` L4129、`steadystate` L4403、`clat_percentiles`/`lat_percentiles`/`percentile_list` L4745–4754。**正文未用但与验收直接相关的条目**：`http` ioengine L2283–2290（"GET/PUT requests over HTTP(S) with libcurl to a WebDAV or S3 endpoint"，"only supports direct IO of iodepth=1; you need to scale this via numjobs"，"blocksize defines the size of the objects"），`http_mode` L3230（webdav/swift/s3）；`rados` ioengine L2273；元数据 ioengine `filecreate`/`filestat`/`filedelete`/`dircreate`/`dirstat` L2422–2450（"measure file lookup and meta data access"）；`rate`/`rate_iops`/`rate_process=poisson` L3689–3729；`latency_target` L3747（"find the max performance point … while maintaining a latency below this target"）及 `latency_window`/`latency_percentile`/`latency_run` L3754–3771；`--status-interval` L205–213（累计值，非逐段；与 json 合用会产生拼接的多段 JSON）；slat/clat 定义 L5060–5080；Terse v3 字段 L5334（含 `cpu_user`、`iodepth_*`、`disk_util`）；Client/Server L5671 起，L5764 "Terse output in client/server mode will differ slightly"。→ C01/C03/C04/C05 |
| fio 源码 io_u.c / ioengines.c@fio-3.43 | [io_u.c](https://raw.githubusercontent.com/axboe/fio/fio-3.43/io_u.c) / [ioengines.c](https://raw.githubusercontent.com/axboe/fio/fio-3.43/ioengines.c) | `a1b8dd59…6bca5` / `eec135b6…65fbef` | `account_io_completion` io_u.c L2083：L2097 `ntime_since(&io_u->issue_time, …)` 记 clat，L2102–2103 `ntime_since(&io_u->start_time, …)` 记 lat；`issue_time` 在 ioengines.c L374–375 取时。即 fio 的 lat = slat + clat 起止点可在源码定位。正文未引用。→ C03 |
| rados(8)（src.ceph.docs-rados-man-squid） | [squid man](https://docs.ceph.com/en/squid/man/8/rados/) | `712a32480451d516a0006d57a4a26936b1ef5d5bc09a429d0c3338f9b2b229f8` | `bench seconds mode [ -b objsize ] [ -t threads ]`；mode 为 write/seq/rand，seq/rand 为读基准，读前须先以 `--no-cleanup` 跑 write；默认对象 4 MB、16 个模拟线程；"The --run-name <label> option is useful for benchmarking a workload test from multiple clients"；"-b objsize option is valid only in write mode"；"write and seq must be run on the same host"。Bench options 节：`-t/--concurrent-ios`、`--show-time`、`--no-verify`、`--write-object`/`--write-omap`/`--write-xattr`。页面 HTML 无点版本号，只有 URL 中的 `squid`。→ C03/C09 |
| MLPerf Storage v2.0（src.mlcommons.storage-rules-v2.0） | [raw@7e71ca16](https://raw.githubusercontent.com/mlcommons/storage/7e71ca162d8f9e7ae4b5b698d7d79b0883817f25/Submission_guidelines.md) | `d107aa39521ef53e508fb83e333c6dbd1ba7ef11969632f156bef1f08a1e10cf` | L79 以 `sleep()` 代替加速器计算；L94 "data transfers from storage in this test terminate with the data in host DRAM; transfering data into the accelerator memory is not included"；L234–237 checkpoint "duration is the maximum time across all processes"、"throughput is the minimum across all processes"；L311 结果为连续 5 次运行均值；L333–342 训练指标为 samples/s 且受最小 AU 约束，AU 计算排除首个 step 的 I/O；L353 checkpoint 指标为读/写带宽，外加"写完到另一 host 可读"的时间；L407–408 须先跑 warm-up，数据集至少为全部节点内存之和的 5 倍；L570 提交 JSON `mlperf_storage_report.json`（`benchmark.sh reportgen` 在 rank0 生成）；L585 起结果目录结构。正文对以上内容一条都没有写。→ C02/C03/C05 |
| Lustre Operations Manual 2.x（src.lustre.ops-manual-2x） | [lustre_manual.xhtml](https://doc.lustre.org/lustre_manual.xhtml) | `63b09d0650de3491eee9c976dff1246706dc6496bc996c139fdebdf7fc4a0d8c`（与 B20 审阅取得的字节相同） | 目录：Ch.12 "Monitoring a Lustre File System"（§12.2 Lustre Jobstats）；Ch.19 "Managing File Layout (Striping) and Free Space"；Ch.39 "Lustre Parameters"（§39.3.3–39.3.5 客户端 offset/extent 统计与 "Monitoring the OST Block I/O Stream"）。正文三处章号属实。手册中存在 `osc.<name>.stats` 与 `osc.*.rpc_stats` 示例。**正文未用**：Ch.32 "LNet Self-Test"，Ch.33 "Benchmarking Lustre File System Performance (Lustre I/O Kit)"，含 sgpdd-survey、obdfilter-survey、ost-survey、mds-survey（§33.5 "Testing MDS Performance"）。→ C06 |

取证限制：

- 未检索 Ceph 官方是否另有 RGW 负载基准文档；C01 只依据已登记的 fio 中已有的 S3 ioengine，不断言 Ceph 侧没有。
- fio 源码只定位了 lat/clat 取样点，未逐行审计 slat 取样、百分位桶算法、client/server 汇总实现。
- MLPerf 的 DLIO 实现与 `mlperf_storage_report.json` 字段未取；只核对了提交指南原文。
- PyTorch profiler/DataLoader、nfs(5)、内核 NFS 文档本轮未重取，它们在正文中没有新的具体主张（见 C08）。
- 未执行任何工具；fio http/rados 引擎能否对 Squid RGW/RADOS 正常工作未验证。

## 发现

### B21-C01 — P1 / OPEN：对象接口终点缺失；"fio 不覆盖对象语义"与 fio HOWTO 相反

位置：正文 §1 L40–41；L17 summary；"来源与更新范围" L67；acceptance 1。

证据：

- acceptance 1 要求分别限定 fio、**对象客户端**、MLPerf Storage 的版本与终点，并把文件系统、**对象接口**、加速器端到端三类结果分开。正文对象一侧只有 rados bench。按 rados(8) 原文，它走 librados，终点是 RADOS 对象层，不是对象接口（RGW S3）。正文把 RGW S3 记为 unknown，所以对象接口这一终点实际上空缺。
- 正文 L40 写 fio "不覆盖：对象语义"。但已登记、已核对的 fio 3.43 HOWTO L2283–2290 有 `http` ioengine，可对 S3 端点发 GET/PUT；`http_mode` L3230 可取 webdav/swift/s3。L2273 还有 librados 的 `rados` ioengine。正文结论与所引一次源相反。
- HOWTO 给出了这个对象客户端的关键限制："only supports direct IO of iodepth=1; you need to scale this via numjobs"，"blocksize defines the size of the objects"，"TRIM is translated to object deletion"。这些限制决定了对象接口结果不能与块/文件层的 iodepth 结果直接对比，正文都没写。
- L17 summary 称"文件/对象/加速器端到端三层终点分开"，当前正文只分出了文件层、RADOS 层和消费侧，三层并未成立。

关闭条件：

- §1 增加对象接口行：fio 3.43 `http` ioengine（`http_mode=s3`），写明终点为"S3 请求完成（客户端侧）"，并写明 iodepth=1、靠 numjobs 扩展、bs 即对象大小、TRIM 即删除，引 HOWTO 对应条目。
- 删除或改正 fio 行"不覆盖：对象语义"。
- rados bench（以及 fio `rados` 引擎）明确标为 RADOS 层，不作为对象接口结果。
- 若不采用 fio http 引擎，写明理由；"RGW 侧官方负载基准未找到"改为"Ceph 侧未检索到；fio 引擎对 Squid RGW 的兼容性未验证（unknown）"。

### B21-C02 — P2 / OPEN：MLPerf Storage 的测量终点写成了"提交规则与结果格式"，未写 host DRAM 与模拟加速器

位置：正文 §1 L42–43。

证据：

- "测量终点"一栏写的是"存储基准提交规则与结果格式"，这不是终点。指南 L94 写明终点："data transfers from storage in this test terminate with the data in host DRAM; transfering data into the accelerator memory is not included"。L79 说明加速器计算由 `sleep()` 代替。
- 训练负载指标是"samples/s，受最小 AU 约束"（L333–342），checkpoint 负载是读/写带宽加跨 host 可读时间（L353）。正文没有区分这两类负载的终点。
- acceptance 1 要求把加速器端到端与存储基准分开。MLPerf 是"模拟加速器、止于 host DRAM"，PyTorch profiler 是"真实加速器的消费侧"。两者的区别正是这里要讲清的边界，正文只写了"不覆盖加速器端到端训练供给结论"。

关闭条件：MLPerf 行的终点改为"host DRAM（加速器计算以 sleep 模拟，不含 H2D 传输）"，分列训练（samples/s＋最小 AU）与 checkpoint（读/写带宽＋跨 host 可读时间），逐条引指南行或节号；与 profiler 行的"真实加速器消费侧"并列说明不可互比。

### B21-C03 — P1 / OPEN：分阶段与跨客户端观测只有一句话，没有用固定工具的计时实现和官方结果格式举例

位置：正文 §4 L62；acceptance 4 前半句；plan `source_discovery` L5280（"fio 官方文档与源码计时/校验范围"）。

证据：

- acceptance 4 要求"以固定工具计时实现和官方结果格式为例说明分阶段/跨客户端观测"。§4 只列了"fio 输出格式/terse/json"和"MLPerf Storage 提交格式"这几个名词，没有说明任何一个计时起止点或聚合规则。
- **fio 计时**：HOWTO L5060–5080 定义 slat（初始化到提交）、clat（提交到完成），`lat_percentiles` L4749 说明 total latency = slat + clat。源码 io_u.c L2097/L2102 分别从 `issue_time`、`start_time` 计到完成。`ramp_time` L711 内的 I/O 不计入结果。`--status-interval` L205–213 输出的是**累计值**，不是逐段值，与 json 合用时输出需要拆分。逐段时间序列应使用 `write_lat_log`/`log_avg_msec`（L4537/L4575）。这些都是"分阶段观测"的直接依据，正文都没有写。
- **fio 跨客户端**：HOWTO L5671 起的 Client/Server 模式是 fio 自带的多机加压与汇总方式，L5764 写明该模式下 terse 输出"will differ slightly"。正文未提。
- **rados bench 跨客户端**：rados(8) 原文写明 `--run-name` "useful for benchmarking a workload test from multiple clients"，且 "write and seq must be run on the same host"。正文未提。
- **MLPerf 官方聚合规则**：checkpoint 的 duration 取所有进程的**最大值**，throughput 取所有进程的**最小值**（L234–237）；AU 排除首个 step 的 I/O（L340）；结果为连续 5 次运行的均值（L311）；提交 `mlperf_storage_report.json`（L570）。这正是"跨客户端如何汇总"的官方样例，正文一条都没写。
- 正文把 knfsd-stats 列为"跨客户端观测入口"。T04-02 §4 对它的用法是 NFS **服务器侧**统计（`/proc/fs/nfsd/pool_stats`），不是跨客户端观测。

关闭条件：

- §4 至少用一个固定工具写清计时起止点（建议 fio：slat/clat/lat，引 HOWTO 条目与 io_u.c 行号），并说明 ramp_time 不计入、status-interval 为累计值、逐段序列需用 lat log。
- 写清跨客户端汇总方式：fio client/server、rados bench `--run-name` 与同 host 约束、MLPerf 的 max/min 聚合与 5 次均值、`mlperf_storage_report.json`。
- knfsd-stats 改标为"服务器侧"，NFS 客户端侧统计记 unknown（或引已登记来源）。
- 不同工具的计时口径不同，结果不得直接互比，在 §4 写明。

### B21-C04 — P2 / OPEN：饱和曲线与可用容量方法无来源；完成指标与对照没有落到工具输出

位置：正文 §3 L58；acceptance 3。

证据：

- "峰值点之后须继续加压画出饱和段，可用容量按延迟/失败门限读取"没有来源，也没有标为本库约定。fio 有直接对应的官方机制，正文未用：`latency_target` L3747 "find the max performance point … while maintaining a latency below this target"，配合 `latency_window`/`latency_percentile`/`latency_run`（L3754–3771），按延迟门限读取可用点。
- 正文没有区分**发起负载**与**完成吞吐**。fio 用 iodepth 加压时是闭环：完成越慢，发起越少，饱和段会被压平。要画出饱和曲线需要定速发起，即 `rate`/`rate_iops` 与 `rate_process=poisson`（L3689–3729）。acceptance 3 写"完成吞吐"，正是要求这一区分。
- 指标只列了名称，没有落到工具输出：元数据可用 fio `filestat`/`filecreate`/`filedelete`/`dircreate`/`dirstat`（L2422–2450），Lustre 有 mds-survey（Ch.33.5）；CPU 与队列在 fio terse v3 中有 `cpu_user`/`cpu_sys`、`iodepth_*`、`disk_util` 字段（L5334）；后端容量、网络占用没有任何来源或工具，也没记 unknown。
- 隔离、争用、冷热三组对照各只有一个词。没有写每组须记录什么：独占窗口如何证明（共存负载清单）、争用负载如何描述、冷态的证据（引 T04-02 §5 已有的冷基线方法）。

关闭条件：

- 饱和/可用容量方法引 fio `latency_target` 系列与 `rate`/`rate_process` 条目，或明确标为本库约定。
- 写明发起负载与完成吞吐的区别，以及闭环加压的局限。
- 每项指标给出工具输出字段或来源；没有来源的项（后端容量、网络）记 unknown。
- 三组对照各写出须记录的条件与证据。

### B21-C05 — P2 / OPEN：工作负载矩阵只有维度名，没有映射到工具参数；失败重试无来源；读者可见文本含计划 ID

位置：正文 §2 L48–54；acceptance 2。

证据：

- 维度齐全：数据规模、读写、随机/顺序、块/对象大小、并发、客户端数、条带、缓存、durability、失败重试、后端空间、运行窗口，十二项都在表内。
- 但"来源"一栏只链接 fio tree 根目录，没有对应到具体参数。可对应的有：fio `rw`/`bs`/`size`/`nrfiles`/`iodepth`/`numjobs`/`direct`/`invalidate`/`fsync`/`end_fsync`/`ramp_time`/`time_based`；rados bench `seconds`/`mode`/`-b`/`-O`/`-t`/`--max-objects`；MLPerf "数据集 ≥ 全部节点内存之和的 5 倍"（L408、L431）和 warm-up（L407）。
- 缓存一行只引 T04-02 的 drop_caches，没有提 fio 自身的 `direct`（L1200）、`invalidate`（L1974）。另外，rados(8) 要求读基准前先跑 write（`--no-cleanup`），刚写入的数据可能留在缓存中，这是一个对象层冷热条件（是否留缓存是本库推论，需注明）。
- "失败重试"一行没有任何来源，fio 与 rados bench 的重试和错误处理语义都没说明，也没记 unknown。
- "后端空间"没有定义（例如已用比例或剩余空间）。Lustre Ch.19 标题即含 "Free Space"，可作入口。
- 读者可见文本写"见 T04-02 §5""T04-02/03"，这是计划 ID，不是链接（B20-C40 已指出同类问题）。

关闭条件：每个维度给出至少一个工具的参数名并引条目；失败重试给出来源或记 unknown；定义后端空间；计划 ID 改为文档链接。

### B21-C06 — P2 / OPEN：Lustre 官方性能工具缺失；计数器含义有手册可查却记为 unknown

位置：正文 §1 L44；§4 L62；"来源与更新范围" L67；plan `source_discovery` L5280（"Lustre 官方性能工具/计数器说明"）。

证据：

- 手册 Ch.33 "Benchmarking Lustre File System Performance (Lustre I/O Kit)" 是官方基准工具章，含 sgpdd-survey（裸设备）、obdfilter-survey（OST）、ost-survey（客户端到 OST）、mds-survey（MDS 元数据）；Ch.32 是 LNet Self-Test（网络）。plan 的 source_discovery 明确要求固定 Lustre 官方性能工具，正文只列了观测入口。
- 正文称计数器"含义未逐项核对，unknown"。手册 §12.2 有 Jobstats 的工作方式与示例输出，§39.3.3–39.3.5 有客户端 offset/extent 统计与 brw_stats 的说明。来源已登记并可读，不应直接记 unknown。
- CollectL 是否为 Lustre 自带工具，正文未说明。

关闭条件：§1 增加 Lustre I/O Kit 与 LNet Self-Test 行，写明各自的测量终点（裸设备 / OST / 客户端到 OST / MDS / 网络），并与文件层 fio 结果分开；至少核对 Jobstats 与 brw_stats 的字段含义，其余保留 unknown；注明 CollectL 的性质。

### B21-C07 — P2 / OPEN：任务目标中的四类代表实现与训练关联没有落点

位置：全文；plan objective L5264。

证据：

- objective 是"建立本地/NFS/RGW/Lustre 四类代表实现独立 I/O 基线、缓存/并发/容量、长尾/争用与训练关联口径"。正文按工具组织，没有按实现组织。本地与 Lustre 可由 fio 覆盖；NFS 只出现了 knfsd-stats；RGW 见 C01。读者无法查到"在 NFS 上做基线时，哪个工具测什么终点、看哪些统计"。
- "训练关联"只有一句"加速器端到端结果单独记录（profiler/DataLoader 侧）"。正文没有链接已有的[训练数据路径](../../knowledge/04-data-storage/training-data-path.md)或[饥饿诊断指南](../../knowledge/04-data-storage/data-starvation-triage.md)，虽然二者已在 `related_ids` 中。
- 长尾一词只出现在标题中，§3 的"延迟分布（含百分位）"没有说明长尾观测（例如百分位列表 `percentile_list` L4754、按时间的 lat log）。

关闭条件：增加一张"实现 × 工具/终点 × 统计入口"小表（四行），空缺记 unknown；训练关联链接到上述两页的具体节；长尾段落说明百分位与时间序列的取法。

### B21-C08 — P2 / OPEN：交付路径/ID 与计划不一致；source_refs 与实际依据不符；来源记录缺精确定位

位置：正文 frontmatter L2、L8–29；plan L5260–5262；roadmap L190；作者来源记录 L7–12。

证据：

- plan 的 target 是 `knowledge/04-data-storage/storage-workload-baselines.md` / `data-storage.storage-workload-baselines`（`state: planned_new`），roadmap L190 也是这一路径。交付文件为 `storage-load-capacity-baseline.md` / `data-storage.storage-load-capacity-baseline`。两边没有说明，后续主题验收按计划路径查找会落空。
- `source_refs` 列了 `src.nfs-utils.nfs-5-man7`，但正文没有任何主张依据 nfs(5)。knfsd-stats 的依据是 `src.kernel.docs-nfs-v6.16`，却没有列入。`src.pytorch.profiler-2.6`、`src.pytorch.dataloader-source-v2.6.0` 已列入，但正文没有链接，也没有具体主张。
- `verification.notes` 称"已核对 … MLPerf Storage v2.0 提交指南"，正文却没有使用该指南的任何具体内容（见 C02/C03）。notes 称核对了"矩阵参数/verify/延迟/输出"，但正文没有一个 HOWTO 条目名或锚点。
- AGENTS.md 要求"cite exact supporting pages or revisions near substantive claims"。来源记录"fio 负载"一行只链接 tree 根目录，MLPerf 一行写"既有登记"，均未写节号、条目名或行号。
- 登记 src.fio.repo-3.43 的 revision 写"所指 commit d2dcd7e0"，经核对正确。建议同时记录 tag 对象 `bef04e7b`，以免 B20 中 Ceph 登记那样把 tag 对象与 commit 混淆。

关闭条件：路径/ID 与计划对齐（改文件名/ID，或在 plan 与 roadmap 中记录变更）；`source_refs` 与实际依据一致；notes 只写正文实际用到的核对范围；来源记录逐主张列出条目名、节号或行号。

### B21-C09 — P3 / OPEN：工具行描述不精确

位置：正文 §1 L40–41。

证据：

- fio 行把"verify 校验"列为测量终点。verify 是完整性检查（HOWTO L4129：写后按 header/pattern 校验），不是性能终点。启用后会多出读校验阶段，影响吞吐结果。
- rados bench 行写"block/object 大小、seq/rand、omap"。原文 `-b objsize` "valid only in write mode"；seq/rand 依赖先前 write 加 `--no-cleanup` 留下的对象；omap 对应 Bench options 中的 `--write-omap`。默认 4 MB / 16 线程也未写。

关闭条件：verify 移出性能终点，或单列为"完整性附加阶段，会影响吞吐"；rados bench 行补充上述约束与默认值。

## acceptance 对照

| acceptance | 判定 | 相关发现 |
|---|---|---|
| 1 工具版本与终点；文件/对象/加速器端到端分开 | 未满足：fio、rados、MLPerf 版本已固定；对象接口终点缺失，且与 fio HOWTO 相反；MLPerf 终点未写 | C01（P1）、C02（P2） |
| 2 工作负载矩阵 | 部分满足：十二个维度都在；没有映射到工具参数，失败重试无来源 | C05（P2） |
| 3 完成指标、对照、饱和/可用容量 | 部分满足："不由峰值推出"的原则已写；方法无来源，未区分发起负载与完成吞吐，指标未落到工具 | C04（P2） |
| 4 计时实现/官方结果格式；无万能阈值或虚构数据 | 未满足：分阶段与跨客户端观测只有一句话。后半句满足：全文无阈值、无测量数据 | C03（P1） |

横向问题：C06（Lustre 官方工具，P2）、C07（四类实现与训练关联，P2）、C08（路径与来源记录，P2）、C09（工具描述，P3）。

## 结论

**T04-06 初审不通过，需修订。B21-C01–C09 共 9 项：P1 ×2（C01、C03），P2 ×6（C02、C04–C08），P3 ×1（C09），全部 OPEN。** 修订后须按各项关闭条件做定向复核。正文 `verification.status: source_checked` 在 C08 关闭前不应视为成立。本审阅只覆盖编辑与来源层面，未执行任何实测；文中所有工具行为都是文档或源码层证据，不得标为 reproduced。
