---
id: data-storage.local-and-shared-storage
title: 本地与共享文件存储版本化参考
type: reference
domain: data-storage
status: draft
platforms: [generic]
source_refs:
  - src.kernel.docs-ext4-v6.16
  - src.kernel.admin-guide-ext4-v6.16
  - src.kernel.docs-nfs-v6.16
  - src.ietf.rfc-8881
  - src.nfs-utils.nfs-5-man7
  - src.nfs-utils.exports-5-man7
  - src.util-linux.mount-8-man7
  - src.kernel.docs-nvme-v6.16
  - src.kernel.docs-sysctl-vm-v6.16
  - src.linux-man-pages.fsync-6.19
  - src.linux-man-pages.rename-6.19
  - src.linux-man-pages.flock-6.19
  - src.linux-man-pages.fcntl-6.19
  - src.linux-man-pages.fcntl-locking-6.19
updated_at: "2026-10-14"
summary: 以 Linux v6.16 ext4 与 NFSv4.1（内核文档＋RFC 8881＋nfs-utils 手册页）为独立证据样板，解释本地与共享文件存储的接口、缓存、锁、一致性、持久性与负载选型；NVMe 取内核主机驱动文档为本地设备样板。
related_ids:
  - data-storage.training-data-path
  - data-storage.checkpoint-durability
  - data-storage.checkpoint-integrity-evidence
verification:
  status: source_checked
  evidence_refs:
    - src.kernel.docs-ext4-v6.16
    - src.kernel.admin-guide-ext4-v6.16
    - src.kernel.docs-nfs-v6.16
    - src.ietf.rfc-8881
    - src.nfs-utils.nfs-5-man7
    - src.nfs-utils.exports-5-man7
    - src.util-linux.mount-8-man7
    - src.kernel.docs-nvme-v6.16
    - src.kernel.docs-sysctl-vm-v6.16
    - src.linux-man-pages.fsync-6.19
    - src.linux-man-pages.rename-6.19
    - src.linux-man-pages.flock-6.19
    - src.linux-man-pages.fcntl-6.19
    - src.linux-man-pages.fcntl-locking-6.19
  notes: "最终核对范围（第五次复核通过）：内核 v6.16 ext4/admin-guide（含 data=/commit=/barrier/auto_da_alloc）/NFS（含 nfs41-server/knfsd-stats/client-identifier）/NVMe 文档、RFC 8881 §2/§8.4（含 §8.4.2.1 State Reclaim 精确锚点）/§9（含 §9.1.2）/§10/§12/§18（含 §18.26.4）锚点、nfs(5) CTO/锁/sync/soft、exports(5) async/sync、mount(8) 通用流程、rename/flock/fcntl/fcntl_locking(2)、sysctl vm 回写/drop_caches（非破坏性）；未取：nfs-utils release/commit 哈希、NVMe 联盟规范原文、客户端 mountstats、pNFS 客户端范围、目标现场配置；未做任何挂载/读写实测，未标 reproduced。"
---

# 本地与共享文件存储版本化参考

> 范围：Linux 本地文件存储（ext4 ＋ NVMe 主机驱动）与共享文件存储（NFSv4.1 内核客户端/服务器 ＋ nfs-utils 手册页）各自独立取证。`generic` 仅为导航聚合；ext4 保证不自动适用于 NFS，NFS 协议文本不等于内核实现行为，未固定的版本/配置不默认兼容。

## 1. 证据样板与版本边界

| 样板 | 版本 | 取证入口 | 不覆盖 |
|---|---|---|---|
| ext4 内核文档 | Linux v6.16 | [ext4 索引](https://www.kernel.org/doc/html/v6.16/filesystems/ext4/index.html)（overview/about/globals/dynamic）＋ [admin-guide/ext4](https://www.kernel.org/doc/html/v6.16/admin-guide/ext4.html)（`data=`/`commit=`/`barrier`/`auto_da_alloc`） | 其他内核版本行为；目标现场挂载选项与设备写缓存 |
| NFS 内核文档 | Linux v6.16 | [NFS 索引](https://www.kernel.org/doc/html/v6.16/filesystems/nfs/index.html)（含 [nfs41-server](https://www.kernel.org/doc/html/v6.16/filesystems/nfs/nfs41-server.html) 实现状态表、[knfsd-stats](https://www.kernel.org/doc/html/v6.16/filesystems/nfs/knfsd-stats.html) 服务器统计、[client-identifier](https://www.kernel.org/doc/html/v6.16/filesystems/nfs/client-identifier.html) 租约锁与客户端身份） | 协议与实现的差异部分（见 §3）；客户端 `/proc/self/mountstats` 未登记 unknown |
| NFSv4.1 协议 | RFC 8881 | [全文](https://datatracker.ietf.org/doc/html/rfc8881)（[§2 core infra](https://datatracker.ietf.org/doc/html/rfc8881#section-2)、[§8.4 crash recovery](https://datatracker.ietf.org/doc/html/rfc8881#section-8.4)、[§9 locking](https://datatracker.ietf.org/doc/html/rfc8881#section-9)、[§10.3.1 data caching](https://datatracker.ietf.org/doc/html/rfc8881#section-10.3.1)、[§10.4 delegation](https://datatracker.ietf.org/doc/html/rfc8881#section-10.4)、[§12 pNFS](https://datatracker.ietf.org/doc/html/rfc8881#section-12)、[§18.3 COMMIT](https://datatracker.ietf.org/doc/html/rfc8881#section-18.3)、[§18.32 WRITE](https://datatracker.ietf.org/doc/html/rfc8881#section-18.32)、[§18.51 RECLAIM_COMPLETE](https://datatracker.ietf.org/doc/html/rfc8881#section-18.51)） | 具体实现行为（以手册页与内核文档为准） |
| nfs(5)/exports(5) | nfs-utils（上游 Git 快照 2026-08-04，最新提交 2026-07-23；nfs.5 页日期 2012-10-09，exports.5 页日期 2009-12-31；release/commit 哈希 unknown） | [nfs(5)](https://man7.org/linux/man-pages/man5/nfs.5.html)、[exports(5)](https://man7.org/linux/man-pages/man5/exports.5.html) | 对侧语义（客户端页不证服务器，服务器页不证客户端） |
| mount(8)/rename/flock/fcntl | mount(8) util-linux 2.43.devel-1062（页日期 2026-08-03）；rename/flock/fcntl(2) man-pages 6.19（页日期 2026-02-08）；fcntl_locking(2) 同 release（页日期 2026-01-23）；fsync(2) 同 release（既有登记） | [mount(8)](https://man7.org/linux/man-pages/man8/mount.8.html)、[rename(2)](https://man7.org/linux/man-pages/man2/rename.2.html) | mount(8) 只给通用流程；文件系统特有语义见各手册页 |
| NVMe 主机驱动 | Linux v6.16 | [NVMe 索引](https://www.kernel.org/doc/html/v6.16/nvme/index.html)（[feature-and-quirk-policy](https://www.kernel.org/doc/html/v6.16/nvme/feature-and-quirk-policy.html)） | NVMe 联盟规范原文（未取，unknown）；具体设备 quirk 与易失写缓存行为 |

## 2. 本地文件存储：提交、锁、页缓存与故障域

| 条目 | 含义 | 条件或限制 | 证据位置 |
|---|---|---|---|
| `data=` 三模式 | `ordered`（默认：数据直接写主文件系统、元数据随后提交入日志）、`journal`（数据也入日志）、`writeback`（只日志元数据，崩溃后文件可能含陈旧数据） | 挂载选项；目标现场选项 unknown | [admin-guide/ext4](https://www.kernel.org/doc/html/v6.16/admin-guide/ext4.html) |
| `commit=` 间隔 | 日志提交周期，默认 5 s；至多丢失最近 5 s 元数据变更 | 同步缺省行为；`barrier` 见下行 | 同上 |
| `barrier` | 默认开启；需要 I/O 栈支持 barrier，jbd 遇 barrier 写错误带警告自动关闭；barrier 使易失磁盘写缓存可安全使用（性能代价）；仅电池保护等情形关闭才可能安全 | 文件系统层条件；设备侧写缓存行为 unknown | 同上 |
| `auto_da_alloc` | 默认 ordered 下的启发式：检测 replace-via-rename 与 replace-via-truncate 模式，journal 提交时先落新文件数据块，防零长度 | 启发式，不能替代文件与目录的 fsync | 同上 |
| rename 原子替换 | 已存在的 newpath 被原子替换；存在 oldpath/newpath 同指一文件的窗口；跨文件系统 EXDEV 失败（不限同目录） | rename(2) 语义；持久性仍需文件＋目录 fsync | [rename(2)](https://man7.org/linux/man-pages/man2/rename.2.html) |
| jbd2 commit/replay | commit block 为事务完整入日志的哨兵；revocation/replay 语义 | 机制描述；目标现场回放结果以实际日志为准 | [globals §3.6](https://www.kernel.org/doc/html/v6.16/filesystems/ext4/globals.html) |
| 本地锁 | 传统 POSIX 记录锁与 flock 均为 advisory；传统锁随进程（非 OFD）：进程终止释放，关闭任一指向该文件的 fd 即释放该进程全部锁；OFD 锁随打开文件描述：仅最后一次关闭该 OFD 时自动释放；flock 锁随打开文件描述：显式 LOCK_UN 或全部重复 fd 关闭时释放；主机崩溃后锁不跨重启保留（本库推论，手册页未逐字写出重启语义，标推论） | 单机语义；三类释放语义不可互换 | [fcntl_locking(2)](https://man7.org/linux/man-pages/man2/fcntl_locking.2.html)、[flock(2)](https://man7.org/linux/man-pages/man2/flock.2.html)；fcntl(2) 本页仅索引（见登记注） |
| 页缓存回写 | 脏页按 `dirty_expire_centisecs`/`dirty_writeback_centisecs` 回写；delalloc 推迟到 commit 超时/sync()/内存不足 | 机制解释，不给推荐值；目标现场参数 unknown | [sysctl vm](https://www.kernel.org/doc/html/v6.16/admin-guide/sysctl/vm.html)（已登记 src.kernel.docs-sysctl-vm-v6.16）、[ext4 overview](https://www.kernel.org/doc/html/v6.16/filesystems/ext4/overview.html) |
| ext4 特性位 | metadata_csum 可对既有 fs 用 tune2fs 追加（或需 e2fsck -D）；64bit 不可在既有 32 位 fs 开启（实验性 resize2fs 除外）；extents/flex_bg 事后开启未核对 unknown | 按特性逐一适用，不概括 | [ext4 overview §2.8](https://www.kernel.org/doc/html/v6.16/filesystems/ext4/overview.html) |
| 故障域 | 单机：设备、驱动、文件系统、页缓存；commit 窗口内元数据、未 fsync 数据在崩溃/断电下可丢失 | 跨主机不可读；NVMe 易失写缓存/flush 行为 unknown | admin-guide `commit=`/`barrier`；NVMe unknown 保留 |

## 3. 共享 NFS：缓存、锁、写入提交与恢复

| 条目 | 含义 | 条件或限制 | 证据位置 |
|---|---|---|---|
| 客户端挂载选项 | `sync`/`async`、`cto`/`nocto`、`ac`/`noac`、`actimeo`、`lookupcache` 等调谐客户端缓存行为 | 客户端侧旋钮；`sync` 挂载选项≠服务器 `sync` 导出选项（见下） | [nfs(5)](https://man7.org/linux/man-pages/man5/nfs.5.html) |
| close-to-open 一致性 | NFS 客户端模型：open 时校验、close 时回写；属性/目录项有缓存窗口（attribute/dentry caching），窗口内可读陈旧数据 | 此节仅以 v3 叙述；v4 缓存/委托语义见 RFC §10.3.1/§10.4，Linux v4 客户端 CTO 行为未在已取源中单列（unknown）；本地 ext4 为单机共享页缓存可见，不是 close-to-open | [nfs(5)](https://man7.org/linux/man-pages/man5/nfs.5.html)（DATA AND METADATA COHERENCE 节）；v4 委托见 [RFC §10.4](https://datatracker.ietf.org/doc/html/rfc8881#section-10.4)/[§10.3.1](https://datatracker.ietf.org/doc/html/rfc8881#section-10.3.1) |
| 锁 | v3 依赖 NLM/NSM 旁路协议（含重启恢复），v4 字节范围锁由服务器实现决定，可为 mandatory，share reservation 本身 mandatory；flock 在 NFS 客户端被模拟为整文件 fcntl 字节范围锁，两类锁互相作用；`nolock`/`local_lock` 有丢失语义风险 | 故障→锁：客户端故障后租约到期可释放（§8.4.1）；服务器重启后 grace 期 reclaim（§8.4.2.1）；网络分区超租约可撤销（§8.4.3）；Linux ≥3.12 客户端丢锁后 I/O 失败直至关闭重开（`nfs.recover_lost_locks` 可恢复旧行为）；Linux 服务器租约默认 90 s（grace 时长另参，未核 unknown） | [nfs(5)](https://man7.org/linux/man-pages/man5/nfs.5.html)（Using file locks with NFS）；内核租约锁见 [client-identifier](https://www.kernel.org/doc/html/v6.16/filesystems/nfs/client-identifier.html)；协议依据 [RFC §8.4.1](https://datatracker.ietf.org/doc/html/rfc8881#section-8.4.1)/[§8.4.2.1](https://datatracker.ietf.org/doc/html/rfc8881#section-8.4.2.1)/[§8.4.3](https://datatracker.ietf.org/doc/html/rfc8881#section-8.4.3)/[§9](https://datatracker.ietf.org/doc/html/rfc8881#section-9)（[§9.1.2](https://datatracker.ietf.org/doc/html/rfc8881#section-9.1.2) share reservation mandatory/字节锁可 mandatory）；flock NFS 模拟见 [flock(2) NFS details](https://man7.org/linux/man-pages/man2/flock.2.html)；丢锁 I/O 行为见 [fcntl_locking(2) Record locking and NFS](https://man7.org/linux/man-pages/man2/fcntl_locking.2.html) |
| 写入→提交→稳定存储 | 客户端回写触发于内存压力/sync/fsync/close/fcntl 加解锁（默认或 async 下"应用写入未必即时到服务器"）；WRITE 可带 UNSTABLE4，须 COMMIT＋write verifier 确认，服务器重启后未提交数据需重发 | write verifier 变化即重发信号 | [nfs(5)](https://man7.org/linux/man-pages/man5/nfs.5.html)；[RFC §18.32](https://datatracker.ietf.org/doc/html/rfc8881#section-18.32)/[§18.3](https://datatracker.ietf.org/doc/html/rfc8881#section-18.3) |
| 导出 sync/async | 服务器 `async` 允许落盘前应答，违反 NFS 协议，异常重启可丢数据/损坏；`sync` 自 nfs-utils 1.0.0 起默认 | 与客户端 `sync` 挂载选项同名不同义 | [exports(5)](https://man7.org/linux/man-pages/man5/exports.5.html) |
| hard vs soft | `soft`/`softerr` 超时可致静默数据损坏；Checkpoint 发布须 `hard` | 选型约束，见 §4 | [nfs(5)](https://man7.org/linux/man-pages/man5/nfs.5.html) |
| NFS rename | RENAME 对客户端原子（跨 fs 返 XDEV）；但重传下报错不代表未执行，调用方须复核结果 | 发布流程必须处理此条 | [RFC §18.26.4](https://datatracker.ietf.org/doc/html/rfc8881#section-18.26.4)；[rename(2) BUGS](https://man7.org/linux/man-pages/man2/rename.2.html) |
| 协议层恢复 | lease、grace period（期间服务器须拒绝某些 READ/WRITE）、reclaim、RECLAIM_COMPLETE | 协议机制；Linux grace 时长、客户端身份配置、reclaim 实际判据未核 unknown | [RFC §8.4](https://datatracker.ietf.org/doc/html/rfc8881#section-8.4)/[§9](https://datatracker.ietf.org/doc/html/rfc8881#section-9)/[§18.51](https://datatracker.ietf.org/doc/html/rfc8881#section-18.51) |
| pNFS | 协议 OPTIONAL（§12.1 原文）；服务器实现状态见内核 nfs41-server 状态表（含 pNFS 行） | 客户端实现范围 unknown | [RFC §12](https://datatracker.ietf.org/doc/html/rfc8881#section-12)、[nfs41-server](https://www.kernel.org/doc/html/v6.16/filesystems/nfs/nfs41-server.html) |
| 可见性≠持久性 | CTO/缓存窗口决定"看到什么"，COMMIT/稳定存储决定"丢什么"；两列分开判定 | 本节核心对照：POSIX 接口相似不等同持久性相同 | 上列各源 |

## 4. 负载选型表（数据/模型/Checkpoint）

| 负载 | 必要配置 | 客户端观察点 | 后端观察点 | 典型异常与来源边界 |
|---|---|---|---|---|
| 训练数据流读 | 只读挂载；`acregmin`/`actimeo` 调谐（代价：属性陈旧窗口）；NFS 侧 `hard` | iostat/读带宽（方法层通用手段，工具未登记）；重传计数（`/proc/self/mountstats` 未登记，unknown） | NFS 服务器统计（[/proc/fs/nfsd/pool_stats 等](https://www.kernel.org/doc/html/v6.16/filesystems/nfs/knfsd-stats.html)）；本地盘 smart/错误计数未登记 unknown | soft 超时 EIO/静默损坏、属性缓存陈旧读、grace 期 I/O 阻塞；饥饿定位见[饥饿诊断指南](data-starvation-triage.md) |
| Checkpoint 写（本地） | 暂存＋文件/目录 fsync 后 rename 提交 | 写带宽、fsync 延迟（方法层，工具未登记） | 后端空间与设备健康（未登记，unknown） | commit 窗口内掉电丢元数据、未 fsync 数据丢失；慢写定位见[慢写诊断指南](checkpoint-slow-io-triage.md) |
| Checkpoint 发布到 NFS | `hard` 挂载（本库约束：由 soft 静默损坏风险推出）＋导出 `sync`；发布前 fsync/close 并检查错误；rename 后复核结果（重传误报） | 同上＋verifier 变化即重发 | knfsd-stats 服务器侧 | 导出 `async` 致重启丢数据、UNSTABLE 未 COMMIT、旧版本/混合版本读（读回协议见计划中 T04-04，不在本页作结论） |
| 模型发布读回 | 内容身份校验（ETag/哈希/签名，责任划分见[完整性证据](checkpoint-integrity-evidence.md)） | 校验失败率、版本错配 | 对象后端观察点属 T04-03 范围，本页不作选型结论 | 缺片/错版/静默改动见完整性证据；对象发布流程见计划中 T04-04 |

NVMe 设备侧配置/观察点：易失写缓存与 flush 行为未取，unknown（不影响上表文件层结论）。

## 5. 可读/重启/校验与冷热基线方法（只设计不执行）

| 方法 | 前置条件 | 预期结果（来源依据） | 实际结果 | 执行授权 |
|---|---|---|---|---|
| 跨主机可读 | 写端 close/fsync 完成（CTO 前置）；读端 open | 读端读到新数据（nfs(5) CTO）；否则窗口内旧数据属预期 | 未执行，留空 | 按现场授权；不新增执行授权 |
| 本地重启可读 | 重挂载＋日志回放完成 | 回放完成后文件系统一致（jbd2 replay 机制）；commit 窗口内数据状态 unknown | 未执行，留空 | 同上 |
| NFS 重连恢复 | grace 结束＋reclaim 完成；verifier 未变 | 恢复后 I/O 正常；verifier 变化则重发未提交写（RFC §18.3）；实现层判据 unknown | 未执行，留空 | 同上 |
| 内容身份校验 | 清单＋哈希算法固定（见完整性证据） | 哈希一致即内容一致（算法碰撞边界见完整性证据） | 未执行，留空 | 同上 |
| 冷基线 | 本地：[drop_caches](https://www.kernel.org/doc/html/v6.16/admin-guide/sysctl/vm.html#drop-caches) 后首读（非破坏性，只清干净页缓存及可回收 dentry/inode；有 I/O/CPU 开销，不建议非测试调试环境用）；NFS 客户端冷＝本机 drop_caches 清本地干净页缓存，属性/目录项缓存与 v4 委托是否随之失效未在已取源中说明（unknown）；服务器侧 unknown | 首读带宽/延迟分布 | 未执行，留空 | 写 /proc/sys 需特权系本库推论（原文未写）；性能影响，仅授权窗口；本库不执行 |
| 热基线 | 重复读，缓存命中 | 稳态带宽/延迟分布 | 未执行，留空 | 同上 |

`drop_caches` 为非破坏性、有开销的操作（[sysctl vm](https://www.kernel.org/doc/html/v6.16/admin-guide/sysctl/vm.html)），"破坏性"旧措辞已纠正；需特权系本库推论（原文未写）。不填任何实测值，不标 reproduced。

## 来源与更新范围

- 上表各入口（内核 v6.16、RFC 8881、man7 快照、man-pages 6.19）。
- 待确认：nfs-utils release/commit 哈希；NVMe 联盟规范原文；客户端 mountstats/nfsstat 登记；pNFS 客户端实现范围；目标现场内核/挂载/导出配置；全部实测（未执行）。
