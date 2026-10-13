# 第二十批 T04-02 定向复核（作者首轮修订后）

复核日期：2026-10-13（实际取证日）。正文 `updated_at`、登记 `registered_at` 中的 `2026-10-14` 视为交付标签，不作为本轮取证日期。

**结论：T04-02 尚未通过。B20-C01–C10 中 CLOSED 5 项（C04、C06、C07、C08、C09），OPEN 5 项（C01、C02、C03、C05、C10）。** 两项 P1（C01、C02）仍为 OPEN，所以 P1/P2 未全部关闭，不得声明审阅通过。修订面已大幅收敛，剩余问题范围很窄，主要是：

- C02：新引入一处事实错误（"v4 锁均为 advisory"）。
- C02：锁在各类故障后保持还是丢失，仍未落到具体条件。
- C03：沿用了初审关闭条件中的一处不实前提（"v4 similar"）。这是初审方的错误，本轮一并更正。

`make check` 通过（89 content entries / 400 sources），但它只校验结构与本地链接，不说明技术正确性。

审阅者角色独立于作者修订角色。审阅模型为 `claude-opus-5-5`，由用户本次明确要求。这不是既有的 `gpt-6.1-sol / xhigh` 批量审阅约定，也不改写该约定；推理等级等运行元数据未取得可核验记录，不补造。本轮只读核对，只写本报告，未改作者正文、来源记录、修订映射、登记或计划，未执行任何挂载、读写、`drop_caches` 或 benchmark。模型复核不构成硬件或现场验证。

## 输入（以 SHA-256 识别）

| 输入 | SHA-256 |
|---|---|
| [T04-02 正文](../../knowledge/04-data-storage/local-and-shared-storage.md)（113 行，reference / draft） | `91edbce3faf487042e82cabae23a96a40fa8a97ffc81673283cd511d2c367d3b` |
| [作者来源记录](batch-20-t04-02-sources.md)（21 行） | `566f0a0e68ccccf13ef16c39dccbc4167faee5c99800ed4a2665a3859dea824b` |
| [修订映射](batch-20-review-fixes.md)（T04-02 节，14 行） | `26e15349f3e0de01716be8773c7b89055520517a87fcdca045e51b7f5076cdfd` |
| [初审报告](batch-20-t04-02-claude-review.md)（关闭条件权威来源） | `c4a7f714d2dece30a0718a99f3a2d1939158350559e36931420e0f44b4a18fe6` |
| [任务计划](../../plans/full-coverage-backlog.yaml)（T04-02 acceptance 4 条，与初审同一文件） | `f16309beadf5ae4f28d5fc7428a2348bea0cf08d155d57730a4d817cfcdd3e96` |
| [来源登记](../../sources/registry.yaml)（400 项） | `2d2042fe717ecdf25ddf5689e7f742baf5c5e1fb6690b83f6d1f8a1738da670e` |

修订映射只给出每项的处理摘要，没有正文行号与来源锚点，不满足初审"逐项给出改动位置与来源锚点"的要求。本轮按正文现行内容逐项定位，不以映射文字作为关闭依据。

## 一次源取证（审阅者独立获取）

全部用 `curl` 默认 TLS 校验只读获取，均 HTTP 200。HTML 去标签后按文字核对。原文仅存临时目录，未入库。

| 来源 | SHA-256（原 HTML） | 与初审一致性 | 本轮核对点 |
|---|---|---|---|
| [admin-guide/ext4](https://www.kernel.org/doc/html/v6.16/admin-guide/ext4.html) | `2849c200…a1e84` | 同初审 | `data=ordered`："All data are forced directly out to the main file system prior to its metadata being committed to the journal"；`commit=nrsec` "lose as much as the latest 5 seconds of metadata changes"；`barrier=<0\|1(*)>` 全文；`auto_da_alloc` 同时覆盖 replace-via-rename 与 replace-via-truncate |
| [ext4 overview](https://www.kernel.org/doc/html/v6.16/filesystems/ext4/overview.html) / [globals](https://www.kernel.org/doc/html/v6.16/filesystems/ext4/globals.html) | `be0e963a…` / `d21499dc…` | 同初审 | §2.8 tune2fs 追加 metadata_csum，必要时 e2fsck -D |
| [nfs(5)](https://man7.org/linux/man-pages/man5/nfs.5.html) / [exports(5)](https://man7.org/linux/man-pages/man5/exports.5.html) | `2b9d9223…` / `b71e95c6…` | 同初审 | Close-to-open 节仅以 NFS version 3 叙述，**无 "similar" 字样**（见 C03）；Using file locks with NFS；The sync mount option 四个触发点含 fcntl 加解锁；COLOPHON 两页均为 Git 快照 2026-08-04 |
| [rename(2)](https://man7.org/linux/man-pages/man2/rename.2.html) | `8772946a…` | 同初审 | 原子替换、EXDEV、NFS BUGS；页日期 2026-02-08 |
| [flock(2)](https://man7.org/linux/man-pages/man2/flock.2.html) | `f46b6eb4cb7c9da8cbe5d7a425943323140da0d4b2b766b6e54d6bc436e6ba09` | 本轮新取 | man-pages 6.19，2026-02-08；锁随所有重复 fd 关闭释放；"NFS details"：自 2.6.12 起 NFS 客户端把 flock 模拟为整文件 fcntl 字节范围锁 |
| [fcntl(2)](https://man7.org/linux/man-pages/man2/fcntl.2.html) | `33c2f86787d125e4156645967ee17dbb0df69a0b352d45457d56218641152b5a` | 本轮新取 | man-pages 6.19，2026-02-08。**该页在 6.19 中只是命令索引**："Advisory record locking" 下仅列 F_SETLK(2const) 等链接，锁语义正文在 fcntl_locking(2)（见 C02/C10） |
| [fcntl_locking(2)](https://man7.org/linux/man-pages/man2/fcntl_locking.2.html)（**未登记**） | `ea550a7908ec74412fafdd602c6a7271dac4fb83b452b484246fed81b6fb7fc9` | 本轮新取 | man-pages 6.19，页日期 2026-01-23。记录锁在进程终止时自动释放，关闭指向该文件的任一 fd 即释放该进程在此文件上的全部锁；强制锁自 Linux 5.15 起不再支持；"Record locking and NFS"：自 Linux 3.12 起 NFSv4 客户端失联丢锁后，自认持锁进程的 I/O 失败，直至关闭并重开；`nfs.recover_lost_locks` 可恢复旧行为；Linux 服务器 `/proc/fs/nfsd/nfsv4leasetime` 默认 90 s |
| [RFC 8881](https://datatracker.ietf.org/doc/html/rfc8881) | `8315801b62a59f50ea8b357881282d16e03b44a371d5c303f2a2166f624a3186` | **与初审 `f123da2a…` 不同**（datatracker 动态渲染，按文字核对） | §9.1.x："Byte-range locks may be implemented by the server as either mandatory or advisory"，share reservation "by their nature are mandatory"；§8.4.1 客户端故障时租约到期后可释放锁；§8.4.2.1 grace 期间 "must reject READ and WRITE operations and non-reclaim locking requests … with NFS4ERR_GRACE, unless …"；§8.4.3 分区时长超过租约时服务器可释放或按冲突撤销锁；§18.26.4 "The RENAME operation must be atomic to the client"，跨 fs 返回 NFS4ERR_XDEV |
| NFS 内核子页 [nfs41-server](https://www.kernel.org/doc/html/v6.16/filesystems/nfs/nfs41-server.html) / [knfsd-stats](https://www.kernel.org/doc/html/v6.16/filesystems/nfs/knfsd-stats.html) / [client-identifier](https://www.kernel.org/doc/html/v6.16/filesystems/nfs/client-identifier.html) | `abbabbf7…` / `ae000cd7…` / `ad693fc9…` | 同初审 | 状态表含 pNFS (REQ)/(OPT) 及 LAYOUTGET 等行；`/proc/fs/nfsd/pool_stats`；"lease-based file locking" |
| [sysctl/vm](https://www.kernel.org/doc/html/v6.16/admin-guide/sysctl/vm.html) | `c63ae6ff…` | 同初审 | drop_caches："drop clean caches, as well as reclaimable slab objects like dentries and inodes"；"non-destructive … will not free any dirty objects"；"use outside of a testing or debugging environment is not recommended"。**原文未写"需特权"**（见 C05） |

取证限制：

1. 同初审限制 1–5：HTML 是渲染产物，man7.org 是第三方快照，未取 NVMe 联盟规范，使用正则去标签，未采集现场配置。
2. RFC 8881 页面哈希与初审不同。datatracker 页面会动态渲染，本轮按章节文字核对，所用段落与初审结论无冲突。
3. fcntl_locking(2) 与 F_SETLK(2const) 未登记。本轮只用它们核对"作者登记的 fcntl(2) 能否支撑正文主张"，不替作者登记。

## 逐项复核

### B20-C01 — P1 / **OPEN**（剩余范围窄）

已满足：

- 正文 L61–65 新增 `data=`、`commit=`、`auto_da_alloc`、rename、jbd2 五行，均有精确页面链接。
- `auto_da_alloc` 已定性为"启发式，不能替代文件与目录的 fsync"（L63）。
- rename 改引 rename(2)，去掉"常识"，修正"同目录"条件（L64）。
- admin-guide/ext4 与 rename(2) 均已新增登记（registry L4940、L4951）。
- unknown 已收窄到"目标现场选项""NVMe 易失写缓存"（L50、L69）。

未满足：

1. **barrier 适用条件缺失。** 初审关闭条件明列"barrier … 的适用条件"，正文只在 L62 条件列写"`barrier` 影响落盘次序保证"，没有写出原文条件。原文条件包括：默认开启；需要 I/O 栈支持；jbd 遇 barrier 写错误时会带警告自动关闭；barrier 让易失磁盘写缓存可安全使用；只有电池保护等情形下关闭才可能安全。最后一点还与 L69 的"易失写缓存 unknown"直接相关：文件系统层条件已由 admin-guide 覆盖，unknown 只应保留设备侧行为。
2. **`data=ordered` 措辞有歧义**（L61，登记 L4940 notes 同）。"数据先于元数据入日志"可被读成数据也进入日志。原文是数据先直接写入主文件系统，元数据随后提交到日志；ordered 模式不把数据写入日志，数据入日志的是 `journal` 模式。

剩余关闭条件：

- 增加 barrier 行或在条件列写全上述条件，引 admin-guide `barrier=` 项。
- `data=ordered` 改为与原文一致的表述，登记 notes 同步更正。
- 非阻断：`auto_da_alloc` 可补 replace-via-truncate。

### B20-C02 — P1 / **OPEN**（含一处新事实错误）

已满足：

- §3 新增锁行（L77），覆盖 v3 NLM/NSM、v4 内置、flock 转换和 `nolock`/`local_lock`。
- §2 新增本地锁行（L66），并登记 flock(2)/fcntl(2)。
- 恢复拆为协议层（L82，引 §8.4/§9/§18.51）与实现层 unknown。
- grace 期间拒绝 READ/WRITE 的表述与 §8.4.2.1 原文一致。

未满足：

1. **新事实错误：L77"均为 advisory"。** nfs(5) 只说 "NLM supports advisory file locks only"，说的是 v3。RFC 8881 §9 明确允许服务器把字节范围锁实现为 mandatory，share reservation 本身就是 mandatory。所以 v4 不能概括为 advisory。另外，flock(2) "NFS details" 写明 NFS 客户端把 flock 模拟为整文件 fcntl 锁，两类锁在 NFS 上会互相作用。这一点比"flock 转 advisory"更具体，建议并写。
2. **"锁在何种故障后保持或丢失"未写出。** L77 条件列写的是"按上列逐项判定"，这是推迟判断，不是陈述；本地锁行 L66 完全没有故障语义。可用的一次源在同一 man-pages 6.19 与 RFC 内：
   - 本地：fcntl_locking(2) 记录锁在进程终止时释放，关闭任一指向该文件的 fd 即释放该进程在此文件上的全部锁；flock(2) 锁随所有重复 fd 关闭释放；主机崩溃后锁不跨重启保留。最后一点手册页未逐字写出，如不引源，应标为本库推论。
   - NFS：RFC §8.4.1 客户端故障后，锁在租约到期后可被释放；§8.4.2.1 服务器重启后在 grace 期内 reclaim；§8.4.3 分区时长超过租约时锁可被撤销。fcntl_locking(2) "Record locking and NFS"：Linux ≥3.12 客户端丢锁后 I/O 失败，直至关闭并重开，`nfs.recover_lost_locks` 可恢复旧行为。
3. **证据颗粒度：fcntl(2) 在 man-pages 6.19 中只是索引页。** 本地锁行 L66 与登记 `src.linux-man-pages.fcntl-6.19`（registry L4973，notes "记录锁接口"）指向的页面不含锁语义正文，不能支撑"advisory 锁语义"。

剩余关闭条件：

- 删去或改正"均为 advisory"：v3 NLM 为 advisory；v4 字节范围锁由服务器实现决定，可为 mandatory；share reservation 为 mandatory。
- 两侧各写一句"故障→锁保持/丢失"：本地写进程退出、fd 关闭、主机崩溃；NFS 写客户端故障、服务器重启、网络分区超过租约，以及 Linux 客户端丢锁后的 I/O 行为。各附 §8.4.1/§8.4.2.1/§8.4.3 与 fcntl_locking(2) 锚点。
- 登记 fcntl_locking(2)，记 man-pages 6.19 与页日期 2026-01-23；或把 fcntl-6.19 的 URL/notes 改为实际含语义的页面，并在正文改链。
- 可选：fcntl_locking(2) 记载 Linux 服务器 `nfsv4leasetime` 默认 90 s。它可收敛"Linux 租约时长"一项；grace 时长仍是另一参数，未核时保留 unknown。

### B20-C03 — P2 / **OPEN**（剩余项源自初审错误）

已满足：

- CTO 已正确归属 NFS 客户端（L76），本地写为"单机共享页缓存可见，不是 close-to-open"。
- "接近-开放"误译已去除。
- 列出 `cto/nocto`、`ac/noac`、`actimeo`、`lookupcache`（L75）。
- 可见性与持久性已分列（L84）。
- v4 委托改引 RFC §10.4/§10.3.1。

未满足：

- L76"以 v3 叙述为例，**v4 类似**"缺少来源。本轮复核 nfs(5) Close-to-open 节全文，原文只以 "NFS version 3 server" 叙述，全页 "similar" 三处均与 CTO 无关。
- **这一不实前提出自初审 C03 关闭条件**（"注明 nfs(5) 的 CTO 叙述以 v3 为例，v4 'similar'"），作者照此写入。现由审阅方更正，不归责作者修订。

剩余关闭条件：

- 把"v4 类似"改为"nfs(5) 此节仅以 v3 叙述；v4 的缓存/委托语义见 RFC §10.3.1/§10.4，Linux v4 客户端 CTO 行为未在已取源中单列（unknown）"，或补引能直接支持 v4 CTO 的一次源。

### B20-C04 — P2 / **CLOSED**

证据：

- L78 写入→提交→稳定存储行与 nfs(5) "The sync mount option" 一致：内存压力、sync/msync/fsync、close、fcntl 加解锁四个触发点均已核对。
- L78 的 UNSTABLE4/COMMIT/verifier 引 RFC §18.32/§18.3。
- L79 导出 `async` 与 exports(5) 原文一致（"violate the NFS protocol"，`sync` 自 1.0.0 后为默认）。
- L80 hard/soft 引 "silent data corruption"。
- L75、L79 已区分客户端 `sync` 挂载选项与服务器 `sync` 导出选项。
- L92 Checkpoint 发布行补齐 `hard`＋导出 `sync`、fsync/close 错误检查和 rename 复核。

非阻断追记（不影响关闭，建议同轮修正）：

- L81"服务端语义同原子替换"引的是 rename(2) BUGS，但该节只说 NFS 上报错不代表未执行，不支持"原子"。应补引 RFC 8881 [§18.26.4](https://datatracker.ietf.org/doc/html/rfc8881#section-18.26.4)（"The RENAME operation must be atomic to the client"，跨 fs 返回 NFS4ERR_XDEV）。
- L80"Checkpoint 发布须 `hard`"是本库从 soft 风险推出的约束，nfs(5) 未直接这样要求，宜标"本库约束"。

### B20-C05 — P2 / **OPEN**（剩余范围窄）

已满足：

- "破坏性"已纠正为非破坏性、只清干净对象、有 I/O/CPU 开销、不建议生产使用（L105、L108），引 sysctl vm。
- §2 新增页缓存回写行，引 `dirty_expire_centisecs`/`dirty_writeback_centisecs`，不给推荐值（L67）。
- 服务器侧冷条件已记 unknown。

未满足：

- **NFS 客户端缓存的"冷"条件未写出。** 初审关闭条件要求本地页缓存、NFS 客户端缓存、NFS 服务器缓存三层各写"冷"条件，正文 L105 只写"NFS：客户端冷＋服务器侧 unknown"。可按已登记源写成：客户端 `drop_caches` 清本机干净页缓存及可回收 dentry/inode（sysctl vm 原文）；NFS 属性缓存、目录项缓存或 v4 委托是否随之失效，未在已取源中说明，记 unknown。

非阻断追记：

- L105"需写特权文件"不在 sysctl vm 原文中。可删去，或标为本库推论。
- 正文链接 kernel.org v6.16 HTML，登记 URL 为固定 commit 的 GitHub rst。初审允许"v6.16 页面锚点"，但正文未带 `#drop-caches` 锚点，建议补上。

剩余关闭条件：补 NFS 客户端"冷"条件（含 unknown 边界）。

### B20-C06 — P2 / **CLOSED**

证据：

- L68 逐项写明特性位条件：metadata_csum 可用 tune2fs 追加，或需 e2fsck -D，与 overview §2.8 原文一致；64bit 不可在既有 32 位 fs 上开启；extents/flex_bg 记 unknown。
- delalloc 时机仍引 overview（L67），与原文一致。
- 丢失后果改由故障域行 L69 引 admin-guide `commit=`/`barrier`，不再以 overview 为证。
- 未纳入 Atomic Block Writes，正文也没有暗示普通缓冲写无撕裂风险。

### B20-C07 — P2 / **CLOSED**

证据：

- §4 L88–93 改为五列：必要配置、客户端观察点、后端观察点、典型异常与来源边界。
- 后端观察点引 knfsd-stats `/proc/fs/nfsd/pool_stats`，已核对；客户端 mountstats 显式 unknown。
- Checkpoint 发布行有 `hard`/导出 `sync`。
- 异常列补齐 soft EIO/静默损坏、属性陈旧读、grace 阻塞、UNSTABLE 未 COMMIT 和 rename 误报。
- 对象后端改为 T04-03 边界说明；NVMe 设备侧单列 unknown（L95）。

非阻断追记：L90 的 `iostat` 和 L91 的"写带宽、fsync 延迟"没有登记来源，也未标 unknown。它们是通用观察手段，不构成事实主张，建议标"方法层，工具未登记"。

### B20-C08 — P2 / **CLOSED**

证据：

- §5 L99–106 已改为"前置条件 / 预期结果（来源依据）/ 实际结果 / 执行授权"四栏。
- 跨主机可读写入了 CTO 前置条件。
- NFS 重连写入了 grace/reclaim/verifier 判据，实现层判据记 unknown。
- 实际结果全部"未执行，留空"，未填实测值，未标 reproduced。
- 预期结果所依据的来源均已登记。

### B20-C09 — P3 / **CLOSED**

证据：

- pNFS 服务器侧已收敛到 nfs41-server 状态表（L83），本轮已核到 pNFS (REQ)/(OPT) 与 LAYOUT* 行；客户端侧保留 unknown。
- 服务器性能计数器已由 knfsd-stats 收敛。
- 正文 L53 与登记 nfs-5/exports-5 revision 已补 Git 快照 2026-08-04、最新提交 2026-07-23，以及两页页日期，与两页 COLOPHON 一致；release/commit 哈希仍为 unknown。

（fcntl_locking(2) 的租约时长可进一步收敛一项 unknown，已并入 C02 可选项，不影响本项关闭。）

### B20-C10 — P3 / **OPEN**（剩余范围窄）

已满足：

- 交叉引用改为 Markdown 链接，对应文件均存在：[data-starvation-triage.md](../../knowledge/04-data-storage/data-starvation-triage.md)、[checkpoint-slow-io-triage.md](../../knowledge/04-data-storage/checkpoint-slow-io-triage.md)、[checkpoint-integrity-evidence.md](../../knowledge/04-data-storage/checkpoint-integrity-evidence.md)。
- T04-04 已标"计划中"。
- 来源记录 L9–15 已按主张细化到节、选项和锚点。

未满足：

1. **登记仍未"只保留正文实际使用的子页说明"。** `src.kernel.docs-nfs-v6.16` 的 revision（registry L4879）仍写"实开 index/exporting/pnfs/localio/reexport"，没有写正文实际使用的 nfs41-server、knfsd-stats、client-identifier。来源记录 L17 写"索引登记范围保留"，与初审关闭条件不一致：登记应如实写明支撑正文的子页。
2. **fcntl(2) 登记颗粒度只到索引页**，见 C02 第 3 点，属同类问题。

非阻断追记：

- `verification.evidence_refs` 未列 sysctl-vm、fsync、rename、flock、fcntl，但 `notes` 声称已核对这些来源，宜补齐。
- 在 C01/C02 关闭前，`verification.status: source_checked` 与 OPEN 项不一致。正文保持 `draft`，复核通过后再按实际核对范围重写 notes。

剩余关闭条件：

- 更新 `src.kernel.docs-nfs-v6.16` 的 revision/notes，写明正文实际使用的三个子页。exporting/pnfs/localio/reexport 如未用于任何主张，标为"仅可达性核对"。
- fcntl 登记颗粒度按 C02 处理。

## 逐条 acceptance 判定

| acceptance | 判定 | 剩余项 |
|---|---|---|
| 1 版本固定与路径/挂载/页缓存/读写/同步/提交/rename 保证与故障域 | 大部分已满足；**未通过** | C01（barrier 条件、ordered 措辞） |
| 2 本地 vs NFS 的缓存/锁/可见性/恢复，不把 POSIX 相似等同持久性 | **未通过** | C02（"均为 advisory"错误、故障→锁结果、fcntl 颗粒度）；C03（"v4 类似"无源） |
| 3 负载选型表、必要配置、观察点、典型异常与来源边界 | **通过**（含非阻断追记） | — |
| 4 可读/重启/校验/冷热基线方法，预期与实际分开 | 结构通过；**未通过** | C05（NFS 客户端冷条件） |

## 结论

**T04-02 未通过定向复核：CLOSED 5（C04、C06、C07、C08、C09），OPEN 5（C01、C02、C03、C05、C10）。** OPEN 项中 P1 两项（C01、C02）、P2 两项（C03、C05）、P3 一项（C10）。本轮未新增发现 ID。新发现的事实错误（"v4 锁均为 advisory"）按 C02 追记；初审自身的不实前提（"v4 similar"）按 C03 更正，并注明来源于初审。

作者修订后须逐项给出正文行号与来源锚点，并做第二轮定向复核。P1/P2 全部关闭前不得声明审阅通过。正文继续保持 `draft`。本复核不构成硬件、挂载或现场验证。
