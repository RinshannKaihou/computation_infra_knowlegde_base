# 第二十批 T04-02 初审

审阅日期：2026-10-13（实际取证日）。正文 `updated_at`、登记 `registered_at` 中的 `2026-10-14` 视为交付标签，不作为本轮取证日期。

**结论：T04-02 需修订。新增 10 项发现（B20-C01–C10）：P1 ×2、P2 ×6、P3 ×2，全部 OPEN。** acceptance 1、2 有 P1 级缺口；acceptance 3、4 有 P2 级缺口。`make check` 通过（89 content entries / 396 sources），但它只校验结构与本地链接，不说明技术正确性。正文 `verification.status: source_checked` 与下述若干来源矛盾不一致，修订复核前不得据此视为已核对。

审阅者角色独立于作者。审阅模型为 `claude-opus-5-5`，用户本次明确要求试用。这不是既有的 `gpt-6.1-sol / xhigh` 批量审阅约定，也不改写该约定；推理等级等运行元数据未取得可核验记录，不补造。本轮只审阅、取证，未改作者正文、来源记录、登记或计划，未执行任何挂载、读写、`drop_caches` 或 benchmark。模型审阅不构成硬件或现场验证。

## 输入（以 SHA-256 识别）

| 输入 | SHA-256 |
|---|---|
| [T04-02 正文](../../knowledge/04-data-storage/local-and-shared-storage.md)（92 行，reference / draft） | `9edf0be64824d8ffaa19c43b10ad8ad09ba2b74167827ec41f363a8deb01156b` |
| [作者来源记录](batch-20-t04-02-sources.md)（19 行） | `ff1318513dbbcdd64df60a6cc30b4b8fe085559c1984f440a0b13bff5e180c24` |
| [任务计划](../../plans/full-coverage-backlog.yaml)（T04-02 acceptance L5095–5099） | `f16309beadf5ae4f28d5fc7428a2348bea0cf08d155d57730a4d817cfcdd3e96` |
| [来源登记](../../sources/registry.yaml)（末尾 7 项为 T04-02 新登记） | `a89ee2a790922ace4c8afe6539dc2649406da673242e2e85d3727c3e913a625b` |
| [04 索引](../../knowledge/04-data-storage/index.md)（工作区已改：新增条目、04.2 状态） | `fc78daa2881e1a00fc6dbabfc9cace0dc8136ddb691ab70c3d0c144eaa41d900` |

正文 `related_ids` 的三个 ID 均可解析到现存文件。索引改动只有三处：related_ids 追加、导航条目、04.2 状态行，未见越界改写。

## 一次源取证（审阅者独立获取）

全部用 `curl` 默认 TLS 校验只读获取，均 HTTP 200。HTML 去标签后按文字核对，不只判可达性。原文仅存临时目录，未入库。

| 来源（登记 ID） | URL | SHA-256（原 HTML） | 核对点与结果 |
|---|---|---|---|
| ext4 索引（src.kernel.docs-ext4-v6.16） | [index](https://www.kernel.org/doc/html/v6.16/filesystems/ext4/index.html) | `72f452e9beb53f8c9fc3c504df824342c298a300cdfe5cee44d5dbf961204fb4` | 页头 6.16.0；目录含 §2.8 Checksums、§2.13 Atomic Block Writes、§3.6 Journal (jbd2) 含 Commit Block/Fast Commit Replay |
| ext4 overview（同上） | [overview](https://www.kernel.org/doc/html/v6.16/filesystems/ext4/overview.html) | `be0e963a89eef482b9facc9ac0c3dce98e8eeba3588503dc8c66bfef3d45f043` | delayed allocation 推迟到 "commit timeout is hit, or sync() is called, or the kernel runs out of memory"；§2.8 "Existing filesystems can have checksumming added by running tune2fs -O metadata_csum"，64bit 不能在既有 32 位 fs 上开启（实验性 resize2fs 除外）→ 见 C06 |
| ext4 globals（同上） | [globals](https://www.kernel.org/doc/html/v6.16/filesystems/ext4/globals.html) | `d21499dc02120587d9a01ce7620ce4926971632db8ff5be9d6f715df27f5052d` | §3.6.8 commit block 为事务完整写入日志的哨兵；replay/revocation 描述 → 见 C01 |
| ext4 admin guide（**未登记**；与 ext4 索引同属 v6.16 文档，但路径在 `admin-guide/` 下） | [admin-guide/ext4](https://www.kernel.org/doc/html/v6.16/admin-guide/ext4.html) | `2849c200bf74329159de5009afa1ed9816096a868bcfee94a20126a02c3a1e84` | `data=journal/ordered(*)/writeback`、`commit=nrsec` 默认 5 s、`barrier`、`auto_da_alloc` 的 replace-via-rename 处理 → 见 C01 |
| ext4 about / dynamic（同上） | about / dynamic | `94197d8c…a1e84`（about 全值 `94197d8ccc831d225cda0da7aa80c83789f4921e0b58392075768150074360de`）；dynamic `508dffdef905ef7858f2bd10a5656bd7a31edc437875a401b236f781a0110223` | 可达；§4.2.3 Extent Tree 存在 |
| ext4 journal 子页 | journal.html | `03bf5ba461d0209e1a7b58a55040fb9a6c5753cc56989c2c1c43d77e0ddf9143` | 可达，未逐段比对 |
| RFC 8881（src.ietf.rfc-8881） | [rfc8881](https://datatracker.ietf.org/doc/html/rfc8881) | `f123da2a13fcab41b89833163229d2dd13934bbaeb48cf9c0762d84101742867` | 约 2.6 MB。锚点 `section-2` "Core Infrastructure"、`section-12` "Parallel NFS (pNFS)"、`section-18` "NFSv4.1 Operations" 均存在且标题吻合；§12.1 原文 "pNFS is an OPTIONAL feature within NFSv4.1" 与正文一致。另核 §8.4 Crash Recovery（grace period）、§9 File Locking、§10.3.1 Data Caching and OPENs、§18.3 COMMIT（UNSTABLE4、write verifier）、§18.32 WRITE、§18.51 RECLAIM_COMPLETE → 见 C02/C04 |
| nfs(5)（src.nfs-utils.nfs-5-man7） | [nfs.5](https://man7.org/linux/man-pages/man5/nfs.5.html) | `2b9d9223f2faeadffdc7c50936a7d03ae0a194c25d9fc3d1662d40dd22e534fb` | 页脚 "9 October 2012 NFS(5)" 与正文一致；COLOPHON 为 nfs-utils，取自上游 Git 2026-08-04，最新提交 2026-07-23；rendering 2026-09-09。"DATA AND METADATA COHERENCE" 节存在，含 Close-to-open、Weak cache consistency、Attribute caching、Directory entry caching、The sync mount option、Using file locks with NFS；`soft/softerr/hard` 有 "silent data corruption" 警示 → 见 C02/C03/C04/C09 |
| exports(5)（src.nfs-utils.exports-5-man7） | [exports.5](https://man7.org/linux/man-pages/man5/exports.5.html) | `b71e95c6208c5480262437c9efd1b5bbcf3384fb60cecc6438f2a836fed5a5a2` | 页脚 "31 December 2009"；同一 nfs-utils Git 快照；`async` "allows the NFS server to violate the NFS protocol … an unclean server restart … can cause data to be lost or corrupted"，`sync` 自 1.0.0 后为默认；`nohide`/`crossmnt`/`fsid` 语义与正文一致 |
| mount(8)（src.util-linux.mount-8-man7） | [mount.8](https://man7.org/linux/man-pages/man8/mount.8.html) | `0fd3413f4fb073c6d083925a7ad04ac24af5235be2c28ee73da2f66a54bb16f9` | 版本行 "util-linux 2.43.devel-1062-f... 2026-08-03 MOUNT(8)" 与正文/登记一致（正文略去截断的提交后缀，可接受） |
| fsync(2)（src.linux-man-pages.fsync-6.19） | [fsync.2](https://man7.org/linux/man-pages/man2/fsync.2.html) | `f0a986d21500222ecb69580fc7a910f346c6b1ff1005ca515501fb05bb5d91f5` | "Linux man-pages 6.19 2026-02-08"，与既有登记一致 |
| rename(2)（**未登记**） | [rename.2](https://man7.org/linux/man-pages/man2/rename.2.html) | `8772946a809a0db54f4854f200908f10bee758ea452e8df5efd955bc3b8e6e57` | man-pages 6.19；"If newpath already exists, it will be atomically replaced …"，"there will probably be a window in which both oldpath and newpath refer to the file"；BUGS："On NFS filesystems, you can not assume that if the operation failed, the file was not renamed" → 见 C01/C04 |
| NFS 内核索引（src.kernel.docs-nfs-v6.16） | [nfs index](https://www.kernel.org/doc/html/v6.16/filesystems/nfs/index.html) | `d5327b4777501622ebab338fc8d654dfcaef97e6dc2d9a9302d69309b06139de` | 子页：client-identifier、exporting、knfsd-stats、localio、nfs41-server、pnfs、reexport、rpc-cache、rpc-server-gss |
| NFS 子页（同上） | nfs41-server / knfsd-stats / client-identifier / pnfs | `abbabbf74da3982467dbea13acbbddb60a727fadfdfc22ed6c35d11abc9890b0` / `ae000cd7d8da5232c0c801c83f020662f48ae0946245724275e2c0b0307d9d90` / `ad693fc98d3387d7e60f054bfff808040a6b70052a766065419ad6896e77bac5` / `5f0c78f97085988104303f60222c27ce2db60a4b63b88ed19d419d7939d4c789` | nfs41-server 有服务器端 NFSv4.1 操作实现状态表（含 pNFS REQ/OPT 行）；knfsd-stats 描述 `/proc/fs/nfsd/pool_stats` 等服务器统计；client-identifier 说明 "lease-based file locking" 与客户端身份对状态恢复的作用 → 见 C02/C07/C09 |
| NVMe 索引 / quirk 策略（src.kernel.docs-nvme-v6.16） | [index](https://www.kernel.org/doc/html/v6.16/nvme/index.html) / [policy](https://www.kernel.org/doc/html/v6.16/nvme/feature-and-quirk-policy.html) | `2ddcd5c4780ad3d2540deb8762758f2136d5e25d256f802bd04ea8b062ed1196` / `7318e823d8e91b68a53db348e2dd83aa56ad3f95f385e4ad28ed0de8b55806c7` | 页头 6.16.0；policy 说明 `drivers/nvme/host/` 支持 NVMe 规范族，规范见 nvmexpress.org；索引仅含 policy 与 pci-endpoint-target 两页，与正文"驱动策略"范围一致 |
| sysctl/vm（src.kernel.docs-sysctl-vm-v6.16，既有登记，计划 existing_source_ids） | [vm](https://www.kernel.org/doc/html/v6.16/admin-guide/sysctl/vm.html) | `c63ae6ff9e96ac3b541236342db8691bc46816c17397451c0080f010cfce21f8` | `drop_caches`："This is a non-destructive operation and will not free any dirty objects"，并称"use outside of a testing or debugging environment is not recommended"；`dirty_expire_centisecs`/`dirty_writeback_centisecs` 存在 → 见 C05 |

取证限制：

1. kernel.org 的 v6.16 HTML 是渲染产物。`src.kernel.docs-sysctl-vm-v6.16` 登记的是固定 commit 的 GitHub `.rst`，本轮未逐字节比对 HTML 与该 rst，只按段落文字核对。
2. man7.org 是第三方渲染快照，不是 nfs-utils/util-linux 发行包。未下载 man-pages-6.19 源码包，作者"源码包不含 nfs.5"的说法本轮未独立复核；nfs(5)/exports(5) 的 COLOPHON 已确认页面归属 nfs-utils。
3. NVMe 联盟规范原文未取，同作者。
4. HTML→文本用正则去标签，未做版式级比对。
5. 未采集任何目标现场配置。

## 逐项发现

### B20-C01 — P1 / OPEN：提交/日志/rename 保证被记为 unknown，而所选 v6.16 文档与 man-pages 6.19 已直接覆盖

位置：正文 L58（rename 行）、L60（故障域行"ext4 文档 journal 描述"无链接）、L92（待确认）；来源记录 L19 第 3、6 项。

证据：

- acceptance 1 明确要求"读写/同步/提交/rename 的保证"。正文 rename 行写"POSIX/手册页常识，ext4 文档未单列，记 unknown"。但同版本 [admin-guide/ext4](https://www.kernel.org/doc/html/v6.16/admin-guide/ext4.html) 写明了三处：`data=ordered`（默认，数据先于元数据提交入日志落盘）、`data=journal`/`data=writeback` 的差异，以及 `commit=` 默认 5 s（"you will lose as much as the latest 5 seconds of metadata changes"）。它还写了 `auto_da_alloc`：在默认 data=ordered 下检测 replace-via-rename，使新文件数据块在 rename 提交前落盘，以避免 "zero-length" 问题。
- [rename(2)](https://man7.org/linux/man-pages/man2/rename.2.html) 写明了 newpath 原子替换，并说明存在 oldpath/newpath 同指一文件的窗口。正文"同目录 rename 为原子替换"把条件写窄、写偏了：原子替换不以同目录为条件，跨文件系统则以 EXDEV 失败。
- globals §3.6 写了 jbd2 的 commit block 与 replay，正文却只写"journal 描述（未细核）"，没有页面锚点。

关闭条件：

- 补一组本地提交语义行：data= 三模式、commit 间隔、barrier、auto_da_alloc 的适用条件，各附精确页面与节名。
- 把 auto_da_alloc 定性为默认 ordered 模式下的启发式，不能替代 fsync 文件与目录。
- rename 行改引 rename(2)，去掉"常识"作为证据，修正"同目录"条件。
- 登记 rename(2) 与 admin-guide/ext4：新增 ID，或把后者明确并入 ext4 登记的 revision/notes。admin-guide 路径不在登记 URL 之下，不能默认被覆盖。
- journal 回放如仍有未核细节，只把真正未覆盖的部分留作 unknown，例如目标现场挂载选项和设备写缓存行为。

### B20-C02 — P1 / OPEN：锁缺失；NFS 恢复只引 §18 并整体记 unknown

位置：正文 §3 L64–71（无锁行）、L70（服务器重启/重连）；§2 无本地锁行。

证据：acceptance 2 要求本地与 NFS 分别说明"客户端缓存、锁、可见性和恢复条件"，但正文两侧都没有锁条目。已取一次源中可直接支持的材料如下：

- [nfs(5)](https://man7.org/linux/man-pages/man5/nfs.5.html) "Using file locks with NFS"：v3 依赖 NLM/NSM 旁路协议支持重启后锁恢复，v4 锁在主协议内；NLM 仅 advisory；flock(2) 被转换为 advisory 锁；还有 `nolock`、`local_lock` 选项。
- RFC 8881 [§9](https://datatracker.ietf.org/doc/html/rfc8881#section-9) 锁与共享保留；[§8.4](https://datatracker.ietf.org/doc/html/rfc8881#section-8.4) Crash Recovery 的 grace period，期间服务器须拒绝某些 READ/WRITE；[§18.51](https://datatracker.ietf.org/doc/html/rfc8881#section-18.51) RECLAIM_COMPLETE。
- 内核 [client-identifier](https://www.kernel.org/doc/html/v6.16/filesystems/nfs/client-identifier.html)："lease-based file locking"，客户端身份影响重启后的状态维持与恢复。

L70 只链 §18 总目录，正文把协议已规定的恢复机制与"实现行为未核"混成一项 unknown。

关闭条件：

- §3 增加锁行（v3 NLM/NSM 与 v4 内置、advisory、flock 转换、nolock/local_lock 风险）。
- 恢复行拆为两项：协议层（lease、grace、reclaim，引 §8.4/§18.51）和 Linux 实现/现场（grace 时长、客户端身份配置，未核则 unknown）。
- 本地侧补锁语义行。若不登记 fcntl(2)/flock(2)，须明确记 unknown，不得留空。
- 两侧都写清楚"锁在何种故障后保持或丢失"。

### B20-C03 — P2 / OPEN：把 close-to-open 归给本地文件系统，一致性对照写反

位置：正文 L71（"本地 close-to-open 与 NFS 一致性模型不同"）、L68（"接近-开放一致性"）。

证据：nfs(5) "Close-to-open cache consistency" 明确 CTO 是 NFS 客户端的一致性模型：打开时校验、关闭时回写。"Weak cache consistency"、"Attribute caching"、"Directory entry caching" 进一步说明属性/目录项缓存窗口内可能读到陈旧数据。本地 ext4 单机多进程经同一页缓存可见，并非 close-to-open。L71 恰是 acceptance 2"不把 POSIX 相似等同持久性相同"的核心行，归属写反会误导读者。L68 "接近-开放"是对 close-to-open 的误译。

关闭条件：

- 改写 L68/L71：本地＝单机共享页缓存可见，持久性另由 fsync/日志决定；NFS＝CTO＋属性/目录项缓存窗口（`cto/nocto`、`ac/noac`、`actimeo`、`lookupcache`）。
- 注明 nfs(5) 的 CTO 叙述以 v3 为例，v4 "similar"。如引用 v4 委托（delegation），用 RFC 8881 §10.4/§10.3.1 锚点。
- 可见性与持久性分列，不在同一格合并。

### B20-C04 — P2 / OPEN：NFS 写入—提交—持久链路缺失，Checkpoint 发布到共享存储无条件

位置：正文 L66（sync/async 只写为"缓存与一致性调谐"）、L67（导出 async 无后果说明）、L78（Checkpoint 行"fsync 后再发布到共享"）。

证据：

- nfs(5) "The sync mount option"：默认（或 async）时，客户端写入要等到内存压力、sync/fsync、close 或 fcntl 加解锁才发往服务器；"data written by an application may not immediately appear on the server"。
- RFC 8881 [§18.32](https://datatracker.ietf.org/doc/html/rfc8881#section-18.32) WRITE 的 UNSTABLE4 与 [§18.3](https://datatracker.ietf.org/doc/html/rfc8881#section-18.3) COMMIT：用 write verifier 发现服务器重启后未提交数据需重发。
- [exports(5)](https://man7.org/linux/man-pages/man5/exports.5.html) `async`：服务器在落稳定存储前应答，"violate the NFS protocol"，服务器异常重启可丢失或损坏数据。
- nfs(5) `soft/softerr`：可致 "silent data corruption"。
- [rename(2)](https://man7.org/linux/man-pages/man2/rename.2.html) BUGS：NFS 上 rename 报错不代表未执行（重传）。

以上都是 Checkpoint 发布到 NFS 的直接持久性条件，正文没有写。另外，客户端 `sync` 挂载选项与服务器 `sync` 导出选项同名、语义不同，正文 L66 未区分。

关闭条件：

- §3 增加"写入→提交→稳定存储"行：客户端回写触发点、UNSTABLE/COMMIT/verifier、导出 sync/async、hard 与 soft/softerr。
- Checkpoint 行补必要配置：`hard` 挂载、导出 `sync`、发布前 fsync/close 的错误检查、rename 结果在 NFS 上的复核，并标明来源边界。
- 明确区分客户端 `sync` 挂载选项与服务器 `sync` 导出选项。

### B20-C05 — P2 / OPEN：`drop_caches` 被称为"破坏性"，与内核文档相反；页缓存回写未引既有登记源

位置：正文 L86；§2 页缓存相关行 L57/L60；计划 `existing_source_ids` 含 `src.kernel.docs-sysctl-vm-v6.16`，但正文 source_refs 未引。

证据：

- [sysctl/vm](https://www.kernel.org/doc/html/v6.16/admin-guide/sysctl/vm.html) `drop_caches`："This is a non-destructive operation and will not free any dirty objects"。文档同时说明它会造成显著 I/O/CPU 开销，"use outside of a testing or debugging environment is not recommended"。
- 正文"特权破坏性操作"与原文相反。"需授权窗口执行"的结论成立，但理由应是写 `/proc/sys` 需特权、影响性能、不建议在生产使用。
- acceptance 1 要求解释页缓存，正文没有引用同一既有源中的 `dirty_expire_centisecs`/`dirty_writeback_centisecs` 回写边界。
- 冷基线如用于 NFS：客户端 drop_caches 不冷却服务器端缓存，正文未写这一层次。

关闭条件：

- 改正 L86 措辞并引既有登记，按该登记的固定 commit/行号或 v6.16 页面锚点。
- §2 补页缓存回写行（脏页过期/回写周期，仅解释机制，不给推荐值）。
- §5 冷/热基线写明本地页缓存、NFS 客户端缓存、NFS 服务器缓存各自的"冷"条件，服务器侧无法控制时记 unknown。

### B20-C06 — P2 / OPEN：ext4 特性位与 delalloc 行和 overview 原文不符或超出原文

位置：正文 L56、L57。

证据：

- L56 称 extents/flex_bg/metadata_csum/64bit"需要文件系统创建时启用的特性位"。[overview §2.8](https://www.kernel.org/doc/html/v6.16/filesystems/ext4/overview.html) 原文："Existing filesystems can have checksumming added by running tune2fs -O metadata_csum"（可能要求 e2fsck -D）。只有 64bit 明示不能在既有 32 位 fs 上开启（实验性 resize2fs 除外）。extents/flex_bg 能否事后开启，本轮与作者均未核对。
- L57 的"崩溃/断电时未落盘数据丢失"以"同上"（overview）为证据，但 overview 只写放置决策推迟到 commit 超时、sync() 或内存不足，没有写丢失后果。丢失后果在 admin-guide 的 `commit=` 与 `auto_da_alloc` "zero-length problem" 中才有原文。

关闭条件：

- L56 按特性逐一写明原文条件（metadata_csum 可 tune2fs 追加，64bit 不可），未核的特性记 unknown。
- L57 的丢失后果改引 admin-guide/fsync(2) 的精确位置（与 C01 的登记一并处理）。
- 可选：overview §2.13 Atomic Block Writes（仅 Direct I/O、需设备硬件原子写、v6.13 起单块）与"torn write"故障域相关。若不纳入，不必补，但不得暗示 ext4 普通缓冲写无撕裂风险。

### B20-C07 — P2 / OPEN：负载选型表缺后端观察点、关键配置与典型异常，且越出来源范围

位置：正文 §4 L75–79。

证据：acceptance 3 要求"必要配置和客户端/后端观察点、典型异常与来源边界"。逐项看：

- **观察点**只有客户端侧（iostat、读带宽、"重传计数 unknown"），无服务器/后端侧。同一 v6.16 NFS 索引中的 [knfsd-stats](https://www.kernel.org/doc/html/v6.16/filesystems/nfs/knfsd-stats.html) 给出 `/proc/fs/nfsd/pool_stats` 等服务器统计，可作为后端观察点来源；客户端 `/proc/self/mountstats`/`nfsstat` 不在已取源中，应记 unknown 或另行登记，不得空写。
- **必要配置**缺 Checkpoint 写到 NFS 的 `hard`/导出 `sync`（见 C04）；训练读行只写 acregmin 调谐，未说明其可见性代价（C03）。
- **典型异常**过稀：缺 soft 超时 EIO/静默损坏、属性缓存陈旧读、服务器重启 grace 期间 I/O 阻塞、NFS rename 重传误报、本地掉电后 commit 窗口内元数据丢失。
- **NVMe**在表中没有任何设备侧配置/观察点。规范未取可以理解，但应显式记 unknown，例如易失写缓存/flush 行为。
- **"模型发布读回"行**的"对象"后端不在本条目登记源内（对象存储属 T04-03），来源边界列未声明这一点。

关闭条件：

- 每行补齐"必要配置 / 客户端观察点 / 后端观察点 / 典型异常 / 来源边界"，每格有来源或显式 unknown。
- 对象存储内容改为指向后续条目的边界说明，不在本页作选型结论。

### B20-C08 — P2 / OPEN：方法节缺"预期结果"与前置条件，预期/实际分离只是声明

位置：正文 §5 L83–87。

证据：acceptance 4 要求"所有预期结果与实际结果分开"。正文只有一句原则性声明（L87），各方法都没有给出预期结果，也没有记录字段。

- 跨主机可读方法缺 CTO 前置条件：写端须 close/fsync 后读端再 open，否则属性缓存窗口内读到旧数据属预期行为。
- 重启/重连只写"检查日志回放完成/状态恢复"，没有可观察判据，例如 grace 期内 I/O 行为、reclaim 完成、写 verifier 变化后的重发。实现层若无来源，判据应记 unknown。

关闭条件：

- 每个方法给出"前置条件 / 预期结果（来源依据）/ 实际结果（未执行，留空）/ 执行授权"四栏或等价结构。
- 预期结果只引已登记来源。
- 不填任何实测值，不标 reproduced。

### B20-C09 — P3 / OPEN：若干 unknown 在已选文档集内可收敛；nfs-utils 快照锚点未记

位置：正文 L47–48、L69、L92；来源记录 L19；登记 `src.nfs-utils.*` revision。

证据：

- "pNFS 内核实现支持范围 unknown"：同一 v6.16 NFS 索引下的 [nfs41-server](https://www.kernel.org/doc/html/v6.16/filesystems/nfs/nfs41-server.html) 有服务器端 NFSv4.1 操作实现状态表（含 pNFS 行）。客户端侧仍可保留 unknown。
- "NFS 性能计数器 unknown"至少服务器侧可由 knfsd-stats 收敛。
- nfs(5)/exports(5) 的 COLOPHON 给出可复核快照锚点："obtained from the project's upstream Git repository … on 2026-08-04 … most recent commit … 2026-07-23"。正文与登记只写"release 未绑定"，未记此快照，也没有记 exports(5) 页面日期 "31 December 2009"。正文 L48 "同快照"表述不足。

关闭条件：

- 按实际取证收敛上述 unknown，或说明为何不采用。
- 登记 revision 补 nfs-utils Git 快照日期与 exports(5) 页面日期，release/commit 哈希仍可记 unknown。

### B20-C10 — P3 / OPEN：交叉引用无链接，来源记录颗粒度只到索引页

位置：正文 L77（"饥饿诊断指南"）、L78（"持久化边界主文""T04-04"）、L79/L85（"完整性证据主文"）；来源记录 L9–15。

证据：

- AGENTS.md 要求使用普通 Markdown 链接。上述对应文件（[data-starvation-triage.md](../../knowledge/04-data-storage/data-starvation-triage.md)、[checkpoint-durability.md](../../knowledge/04-data-storage/checkpoint-durability.md)、[checkpoint-integrity-evidence.md](../../knowledge/04-data-storage/checkpoint-integrity-evidence.md)）均已存在，但正文只给名称。
- T04-04 是计划任务、尚无页面，应写明"计划中"。
- 来源记录的 NFS/NVMe/ext4 行只给索引 URL，未按主张给节名或锚点，例如 nfs(5) 节名、exports(5) 选项名、RFC 节号。登记写"实开 exporting/pnfs/localio/reexport"，但正文未使用这些子页的任何内容。

关闭条件：补链接，计划任务标注状态；来源记录按主张细化到节/锚点；只保留正文实际使用的子页说明。

## 逐条 acceptance 判定

| acceptance | 判定 | 主要发现 |
|---|---|---|
| 1 版本固定与路径/挂载/页缓存/读写/同步/提交/rename 保证与故障域 | 版本选定通过（ext4/NVMe/NFS 均 v6.16，RFC 8881，man7 快照版本行与原文一致）；保证说明**未通过** | C01（P1）、C05、C06 |
| 2 本地 vs NFS 的缓存/锁/可见性/恢复，不把 POSIX 相似等同持久性 | **未通过**：锁缺失，恢复混为 unknown，对照行归属写反 | C02（P1）、C03、C04 |
| 3 负载选型表、必要配置、观察点、典型异常与来源边界 | **未通过**：后端观察点与关键配置缺失 | C07、C04 |
| 4 可读/重启/校验/冷热基线方法，预期与实际分开 | "只设计不执行"通过（未声称执行，未标 reproduced）；"预期与实际分开"**未通过** | C08、C05 |

## 结论

**需修订。** 10 项发现全部 OPEN：P1 两项（C01、C02）、P2 六项（C03–C08）、P3 两项（C09、C10）。作者修订后须逐项给出改动位置与来源锚点，再做针对性复核；P1/P2 全部关闭前不得声明审阅通过。正文继续保持 `draft`；修订后 `verification.notes` 应按实际核对范围重写。本审阅不构成硬件、挂载或现场验证。
