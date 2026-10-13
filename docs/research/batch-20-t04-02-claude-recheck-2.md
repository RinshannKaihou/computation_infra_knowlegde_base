# 第二十批 T04-02 第二次定向复核（作者第二轮修订后）

复核日期：2026-10-13（实际取证日）。正文 `updated_at` 与登记 `registered_at` 中的 `2026-10-14` 仍按交付标签处理，不作为取证日期。

**结论：T04-02 尚未通过。本轮复核范围为 5 项（C01、C02、C03、C05、C10），其中 CLOSED 2 项（C03、C05），OPEN 3 项（C01、C02、C10）。合计 B20-C01–C10：CLOSED 7 项，OPEN 3 项。** P1 的 C01、C02 仍为 OPEN，因此不得声明审阅通过。

正文修订已基本到位。剩余问题集中在以下三处：

- 登记 notes/revision 未同步。修订映射声称已处理，但 `sources/registry.yaml` 中的对应条目未改，涉及 C01、C02、C10。
- 本地锁行有新的过度概括：把传统记录锁的释放语义套用到 OFD 锁和 flock 上（按 C02 追记）。
- NFS 锁行新增的故障→锁主张，证据列没有链接到实际支撑页（C02）。

`make check` 通过（`PASS: 89 content entries; 401 sources.`）。它只校验结构与本地链接，不说明技术正确性。

审阅者角色独立于作者修订角色。审阅模型为 `claude-opus-5-5`，由用户本次明确要求。这不是既有的 `gpt-6.1-sol / xhigh` 批量审阅约定，也不改写该约定；推理等级等运行元数据未取得可核验记录，不补造。本轮只读核对，只写本报告，未改作者正文、来源记录、修订映射、登记或计划，未执行任何挂载、读写、`drop_caches` 或 benchmark。模型复核不构成硬件或现场验证。

## 输入（以 SHA-256 识别）

| 输入 | SHA-256 |
|---|---|
| [T04-02 正文](../../knowledge/04-data-storage/local-and-shared-storage.md)（122 行，reference / draft） | `e9bac45f905688b046943cdb4f615b110001f9e3f762d022f2cd39cfd256e3d3` |
| [作者来源记录](batch-20-t04-02-sources.md)（21 行） | `8d58ae110bfb0299f1b7e6d48220c2ec6e5f82c9f631e8489d753daf3e1bc8e8` |
| [修订映射](batch-20-review-fixes.md)（T04-02 第二轮修订节） | `fa6d6dd8781159f1a78d00c008bcc7472f5ec9e6d6a5a459bae1d117f86be675` |
| [前次复核报告](batch-20-t04-02-claude-recheck.md)（剩余关闭条件权威来源） | `750b50b454cd30dd98ee495e7b8cd8dba0b314127d5035a32845cb16b281aac3` |
| [任务计划](../../plans/full-coverage-backlog.yaml)（T04-02 acceptance 4 条；与前两轮同一文件） | `f16309beadf5ae4f28d5fc7428a2348bea0cf08d155d57730a4d817cfcdd3e96` |
| [来源登记](../../sources/registry.yaml)（401 项） | `5c527af4404235dd4e9cea1fad041969ba84db1ca7ad3483ee87073e98e01ed3` |

修订映射问题：

- 第二轮修订节在 L16–23 与 L25–32 **整段重复**。
- 修订映射仍未给出正文行号与来源锚点。
- 修订映射中有三处与登记现状不符，见 C01、C02、C10。

本轮按正文和登记的现行内容逐项定位，不以映射文字作为关闭依据。

## 一次源取证（审阅者独立获取）

全部用 `curl` 默认 TLS 校验只读获取，均返回 HTTP 200。HTML 用正则去标签后按文字核对。原文只保存在临时目录，未入库。

| 来源 | SHA-256（原 HTML） | 与前次一致性 | 本轮核对点 |
|---|---|---|---|
| [admin-guide/ext4](https://www.kernel.org/doc/html/v6.16/admin-guide/ext4.html) | `2849c200…a1e84` | 同前次 | `data=ordered`："All data are forced directly out to the main file system prior to its metadata being committed to the journal"；`barrier=<0\|1(*)>` 全文（"requires an IO stack which can support barriers"、"if jbd gets an error on a barrier write, it will disable again with a warning"、"making volatile disk write caches safe to use, at some performance penalty"、"battery-backed … disabling barriers may safely improve performance"）；`auto_da_alloc` 覆盖 replace-via-rename 与 replace-via-truncate |
| [fcntl_locking(2)](https://man7.org/linux/man-pages/man2/fcntl_locking.2.html) | `ea550a79…b6fb7fc9` | 同前次 | 传统记录锁 "associated with the process (unlike the open file description locks …)"；"If a process closes any file descriptor referring to a file, then all of the process's locks on that file are released"；OFD 锁 "only automatically released on the last close of the open file description"；"By default, both traditional … and open file description record locks are advisory"；强制锁 "no longer supported at all in Linux 5.15 and above"；"Lost locks"节：EIO "until the lock is removed or the file descriptor is closed. Since Linux 3.12 … at least for NFSv4"；"Record locking and NFS"节：自 3.12 起 I/O 失败 "until that process closes and reopens the file"，`nfs.recover_lost_locks`，`/proc/fs/nfsd/nfsv4leasetime` 默认 90 |
| [flock(2)](https://man7.org/linux/man-pages/man2/flock.2.html) | `f46b6eb4…52b5a` | 同前次 | "NFS details"：自 2.6.12 起 "emulating them as fcntl(2) byte-range locks on the entire file … fcntl(2) and flock() locks do interact with one another over NFS" |
| [fcntl(2)](https://man7.org/linux/man-pages/man2/fcntl.2.html) | `33c2f867…2b5a` | 同前次 | 仍只是命令索引页 |
| [sysctl/vm](https://www.kernel.org/doc/html/v6.16/admin-guide/sysctl/vm.html) | `c63ae6ff…` | 同前次 | 页内存在 `id="drop-caches"` 锚点；"drop clean caches, as well as reclaimable slab objects like dentries and inodes"；原文未写需要何种特权 |
| [nfs(5)](https://man7.org/linux/man-pages/man5/nfs.5.html) | `2b9d9223…` | 同前次 | "NLM supports advisory file locks only"；`lock`/`nolock`、`local_lock` |
| [client-identifier](https://www.kernel.org/doc/html/v6.16/filesystems/nfs/client-identifier.html) | `ad693fc9…` | 同前次 | 租约锁与客户端身份 |
| [RFC 8881](https://datatracker.ietf.org/doc/html/rfc8881) | `a0f633b1…a8a2` | **与前两轮均不同**（datatracker 动态渲染，按文字核对） | **§9.1.2**："Share reservations … by their nature are mandatory"；"Byte-range locks may be implemented by the server as either mandatory or advisory"。§8.4.1 Client Failure and Recovery；§8.4.2.1 State Reclaim（"must reject READ and WRITE … unless …"）；§8.4.3：分区超过租约时 "the server may free all locks … or … MUST be revoked as necessary"；§18.26.4 "The RENAME operation must be atomic to the client" |

取证限制：

1. 前两轮的取证限制继续适用：HTML 是渲染产物；man7.org 是第三方快照；未取 NVMe 联盟规范；去标签使用正则；未采集现场配置。
2. RFC 8881 页面哈希与前两轮都不同。本轮按章节文字核对，所用段落与前两轮的结论无冲突。
3. 本轮未重取 ext4 overview/globals、exports(5)、rename(2)、nfs41-server、knfsd-stats。它们支撑的是已 CLOSED 项，或本轮正文未改动的行。

## 逐项复核

### B20-C01 — P1 / **OPEN**（只剩登记同步）

已满足：

- **barrier**：正文 L70 新增独立行，覆盖四个条件：默认开启；需要 I/O 栈支持，jbd 遇 barrier 写错误时带警告自动关闭；barrier 使易失写缓存可安全使用，但有性能代价；只有电池保护等情形下关闭才可能安全。条件列写明"文件系统层条件；设备侧写缓存行为 unknown"，与前次要求的 unknown 边界一致。以上已逐句对照 admin-guide 原文。
- **ordered 措辞**：正文 L68 现为"数据直接写主文件系统、元数据随后提交入日志"，与原文一致。同一行补出 `journal`（数据也入日志）和 `writeback`（崩溃后文件可能含陈旧数据）。
- **`auto_da_alloc` 非阻断项**：正文 L71 已补 replace-via-truncate。

未满足：

- **登记未同步。** `src.kernel.admin-guide-ext4-v6.16` 的 notes（registry L4950）仍是"data=ordered 默认（**数据先于元数据入日志**）"，也就是前次指出的歧义原句。同一 notes 仍把 `auto_da_alloc` 写成只针对 "replace-via-rename 启发式"。修订映射 L18 称"登记同步"，与登记现状不符。

剩余关闭条件：

- 把该条登记 notes 中的 ordered 表述改为与原文一致，例如"数据先直接写入主文件系统，元数据随后提交到日志；ordered 不把数据写入日志"。同时补上 replace-via-truncate。

### B20-C02 — P1 / **OPEN**（含一处新的过度概括）

已满足：

- **"均为 advisory"已删除**（正文 L85）。现写为：v3 NLM/NSM；v4 字节范围锁由服务器实现决定，可为 mandatory；share reservation 本身 mandatory。与 nfs(5) "NLM supports advisory file locks only"及 RFC §9.1.2 原文一致。
- **flock 模拟细节**已写入 L85，与 flock(2) "NFS details"一致。
- **NFS 侧故障→锁**已写入 L85 条件列：
  - 客户端故障后，租约到期即可释放（§8.4.1）；
  - 服务器重启后，在 grace 期内 reclaim（§8.4.2.1）；
  - 网络分区超过租约时，锁可被撤销（§8.4.3）；
  - Linux ≥3.12 客户端丢锁后 I/O 失败，直至关闭并重开；`nfs.recover_lost_locks` 可恢复旧行为；
  - Linux 服务器租约默认 90 s，grace 时长仍为 unknown。

  以上主张均已核对原文，内容正确。
- **本地侧故障→锁**已写入 L74：进程终止、关闭 fd、主机崩溃三种情形。主机崩溃一条已标为本库推论。
- **登记**：已新增 `src.linux-man-pages.fcntl-locking-6.19`（registry L4984），revision 记 man-pages 6.19、页日期 2026-01-23，与页面 COLOPHON 一致。正文 frontmatter 的 `source_refs` 与 `evidence_refs` 均已列入。

未满足：

1. **新事实问题（按 C02 追记）：本地锁行把传统记录锁的释放语义套用到全部本地锁上。** L74 写"flock/fcntl 均为 advisory **记录锁**；进程终止释放记录锁，关闭任一指向该文件的 fd 即释放该进程在此文件上的全部锁"。fcntl_locking(2) 原文把这一释放语义限定在**传统（进程关联）记录锁**，并专门说明它与 OFD 锁不同。原文对 OFD 锁（`F_OFD_SETLK*`，Linux 3.15 起）的说法是 "only automatically released on the last close of the open file description, instead of being released on any close of the file"。flock 锁也不属于记录锁：flock(2) 是整文件锁，与 open file description 关联，正文后半句已正确描述它的释放方式。"均为 advisory"在本地侧本身成立：原文写明两类记录锁默认 advisory，强制锁自 Linux 5.15 起不再支持，而本库样板是 v6.16。问题只在"记录锁"的归类，以及"关闭任一 fd 释放全部锁"被扩大到 OFD 锁。
2. **L85 证据列没有链接到新增主张的支撑页。** 前次关闭条件要求"各附 §8.4.1/§8.4.2.1/§8.4.3 与 fcntl_locking(2) 锚点"。条件列虽以文字写出了 RFC 章节号，但 L85 证据列只链接了 nfs(5) 和 client-identifier，下列支撑页都不在本行：
   - RFC §9.1.2（mandatory/advisory、share reservation）；
   - RFC §8.4.1/§8.4.2.1/§8.4.3；
   - flock(2) "NFS details"（模拟为整文件 fcntl 锁）；
   - fcntl_locking(2) "Record locking and NFS"（Linux ≥3.12 丢锁行为、`nfs.recover_lost_locks`、`nfsv4leasetime` 90 s）。

   其中 fcntl_locking(2) 是关闭条件中点名要求的锚点。目前它在全文只被 L74 本地锁行引用，L85 的 Linux 丢锁与 90 s 主张在本行无出处。
3. **fcntl(2) 登记注未改。** `src.linux-man-pages.fcntl-6.19` 的 notes（registry L4983）仍是"记录锁接口；NFS 语义以 nfs(5)/RFC 为准"，没有写明本页在 6.19 中只是索引。正文 L74 写"fcntl(2) 本页仅索引（见登记注）"，但登记注里没有这句话，引用落空。修订映射 L19 称"fcntl-6.19 备注索引定位"，与登记现状不符。
4. **flock(2) 登记注过时**（与第 3 点同类）。registry L4972 notes 仍写"NFS 上转换为 advisory 锁（以 nfs(5) 为准）"，与正文 L85 及 flock(2) 原文的"模拟为整文件 fcntl 字节范围锁"不一致。

剩余关闭条件：

- 改写 L74：把"关闭任一 fd 即释放该进程全部锁"限定为传统（进程关联）记录锁；补一句 OFD 锁在最后一个 open file description 关闭时释放（fcntl_locking(2) "Open file description locks"）；flock 不称作"记录锁"。
- L85 证据列补齐 RFC [§9.1.2](https://datatracker.ietf.org/doc/html/rfc8881#section-9.1.2)、[§8.4.1](https://datatracker.ietf.org/doc/html/rfc8881#section-8.4.1)、[§8.4.2.1](https://datatracker.ietf.org/doc/html/rfc8881#section-8.4.2.1)、[§8.4.3](https://datatracker.ietf.org/doc/html/rfc8881#section-8.4.3)、flock(2) "NFS details"、fcntl_locking(2) "Record locking and NFS"。
- 更新 `fcntl-6.19` notes，写明本页在 6.19 中只是命令索引，锁语义见 `fcntl-locking-6.19`。更新 `flock-6.19` notes，写明 NFS 客户端把 flock 模拟为整文件 fcntl 字节范围锁。
- 非阻断：§1 表 L61 的版本列只写"页日期 2026-02-08"，可补 fcntl_locking(2) 的页日期 2026-01-23。

### B20-C03 — P2 / **CLOSED**

证据：

- 正文 L84 条件列现为"此节仅以 v3 叙述；v4 缓存/委托语义见 RFC §10.3.1/§10.4，Linux v4 客户端 CTO 行为未在已取源中单列（unknown）"。这与前次给出的替代表述一致，"v4 类似"已去除。
- 证据列链接到 nfs(5) DATA AND METADATA COHERENCE 节，以及 RFC §10.4、§10.3.1。
- 前次已满足的部分没有回退：CTO 归属、本地"单机共享页缓存可见，不是 close-to-open"、可见性与持久性分列（L92）。

### B20-C05 — P2 / **CLOSED**（含非阻断残留）

证据：

- **NFS 客户端冷条件**已写入 L113："NFS 客户端冷＝本机 drop_caches 清本地干净页缓存，属性/目录项缓存与 v4 委托是否随之失效未在已取源中说明（unknown）；服务器侧 unknown"。这与前次关闭条件一致。sysctl vm 原文只写 "drop clean caches, as well as reclaimable slab objects like dentries and inodes"，正文没有越过原文推断 NFS 属性缓存或委托的失效行为。
- **drop-caches 锚点**：L113 链接到 `…/sysctl/vm.html#drop-caches`，本轮已确认页内存在 `id="drop-caches"`。
- **特权推论**：L113 执行授权列写为"写 /proc/sys 需特权系本库推论（原文未写）"。

非阻断残留：

- 正文 L116 仍写"`drop_caches` 为非破坏性但**需特权**、有开销的操作（sysctl vm）"。这把特权写成了 sysctl vm 的原文主张，与 L113 的推论标注矛盾。此项在前次报告中属于非阻断，因此不影响关闭，但修订映射 L21 称"特权标推论"只完成了一半。建议与 C01/C02 同轮处理：删去 L116 的"需特权"，或同样标为本库推论。

### B20-C10 — P3 / **OPEN**

已满足：

- `verification.evidence_refs`（正文 L31–45）已补齐 sysctl-vm、fsync、rename、flock、fcntl、fcntl-locking，与 `source_refs` 一致，并与 notes 声称的核对范围对应。
- fcntl 颗粒度：已登记 `fcntl-locking-6.19`。正文 L74 已改链 fcntl_locking(2)。

未满足：

1. **`src.kernel.docs-nfs-v6.16` 的 revision 未改**（registry L4879）。仍写"实开 index/exporting/pnfs/localio/reexport（curl 200）"，没有写明正文实际使用的 nfs41-server、knfsd-stats、client-identifier。notes（L4884）也只写"内核 NFS 文档入口"。修订映射 L22 称"nfs 登记写明实际三子页"，与登记现状不符。作者来源记录 L17 也仍写"未使用 exporting/pnfs/localio/reexport 具体内容（索引登记范围保留）"。
2. fcntl(2) 登记注没有写明索引定位，与 C02 第 3 点为同一问题，在此不重复计数。

剩余关闭条件：

- 更新 `src.kernel.docs-nfs-v6.16` 的 revision/notes，写明正文实际使用 nfs41-server（实现状态表、pNFS 行）、knfsd-stats（`pool_stats`）、client-identifier（租约锁与客户端身份）三个子页。exporting/pnfs/localio/reexport 标为"仅可达性核对，未用于主张"。
- 作者来源记录 L17 同步改写。
- fcntl(2) 登记注按 C02 处理。

## 非阻断追记（不影响本轮计数）

- 修订映射第二轮修订节整段重复（L16–23 ≡ L25–32），并且有三处"已处理"与登记现状不符（C01 登记同步、C02 fcntl 登记注、C10 nfs 子页）。修订映射应以登记实际内容为准，并逐项写出正文行号与登记行号。
- `verification.status: source_checked` 仍与 OPEN 项并存。正文继续保持 `draft`，复核通过后再按实际核对范围重写 notes。
- 前次 C04/C07 的非阻断项已在正文落实：L89 引用 RFC §18.26.4；L100 把 `hard` 标为本库约束；L98–99 标注"方法层，工具未登记"。这两项原已 CLOSED，本轮不重开，仅作记录。

## 逐条 acceptance 判定

| acceptance | 判定 | 剩余项 |
|---|---|---|
| 1 版本固定与路径/挂载/页缓存/读写/同步/提交/rename 保证与故障域 | 正文满足；**未通过** | C01（admin-guide 登记 notes 未同步） |
| 2 本地 vs NFS 的缓存/锁/可见性/恢复，不把 POSIX 相似等同持久性 | **未通过** | C02（本地锁释放语义过度概括；L85 证据列缺锚点；fcntl/flock 登记注）；C03 已关闭 |
| 3 负载选型表、必要配置、观察点、典型异常与来源边界 | **通过**（前次已判定，本轮正文无回退） | — |
| 4 可读/重启/校验/冷热基线方法，预期与实际分开 | **通过** | C05 已关闭；L116 措辞为非阻断残留 |

## 结论

**T04-02 未通过第二次定向复核。本轮 5 项中 CLOSED 2 项（C03、C05），OPEN 3 项（C01、C02、C10）。B20-C01–C10 合计 CLOSED 7 项，OPEN 3 项（P1 两项 C01、C02；P3 一项 C10）。** 本轮未新增发现 ID。本地锁释放语义的过度概括按 C02 追记。

剩余工作量很小，基本是登记 notes/revision 同步、L74 一句限定、L85 证据列补链。作者修订后须逐项给出正文行号与登记行号，再做定向复核。P1/P2 全部关闭前不得声明审阅通过。正文继续保持 `draft`。本复核不构成硬件、挂载或现场验证。
