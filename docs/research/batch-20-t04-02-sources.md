# 第二十批 T04-02 来源记录

任务：T04-02（新建 `local-and-shared-storage.md`）。作者取证轮次：首轮（内核 v6.16 ext4/NFS/NVMe 文档、RFC 8881 全文、man7 快照、man-pages-6.19 源码包核对 nfs.5 归属）＋第二轮（admin-guide/ext4、rename/flock/fcntl(2)、nfs41-server/knfsd-stats/client-identifier、COLOPHON 快照、exports 页日期；独立复核初审取证点）。

## 主张—来源定位表（ID—精确页面/节—字段/支持范围）

| 主张 | 已登记 ID | 精确页面/节 | 支持范围 / 未覆盖 |
|---|---|---|---|
| ext4 提交语义 | src.kernel.admin-guide-ext4-v6.16 | [admin-guide/ext4](https://www.kernel.org/doc/html/v6.16/admin-guide/ext4.html)（`data=` 三模式、`commit=` 默认 5 s、`barrier`、`auto_da_alloc`） | 挂载语义；目标现场选项 unknown |
| ext4 参考 | src.kernel.docs-ext4-v6.16 | [overview](https://www.kernel.org/doc/html/v6.16/filesystems/ext4/overview.html)（§2.8 metadata_csum/64bit 条件、delalloc 时机）、[globals §3.6](https://www.kernel.org/doc/html/v6.16/filesystems/ext4/globals.html)（commit block/replay） | 机制描述；特性位按项适用 |
| rename/锁 | src.linux-man-pages.rename-6.19 / src.linux-man-pages.flock-6.19 / src.linux-man-pages.fcntl-6.19 / src.linux-man-pages.fcntl-locking-6.19 / src.linux-man-pages.fsync-6.19 | [fcntl_locking(2)](https://man7.org/linux/man-pages/man2/fcntl_locking.2.html)（释放语义/强制锁 5.15 停支/NFS 丢锁/nfsv4leasetime 90 s；fcntl(2) 本页仅索引）； [rename(2)](https://man7.org/linux/man-pages/man2/rename.2.html)（原子替换/EXDEV/NFS BUGS）、flock/fcntl advisory、fsync(2) | man-pages 6.19；NFS 语义以 nfs(5)/RFC 为准 |
| NFS 参考 | src.kernel.docs-nfs-v6.16 | [nfs41-server](https://www.kernel.org/doc/html/v6.16/filesystems/nfs/nfs41-server.html)（实现状态表）、[knfsd-stats](https://www.kernel.org/doc/html/v6.16/filesystems/nfs/knfsd-stats.html)（pool_stats）、[client-identifier](https://www.kernel.org/doc/html/v6.16/filesystems/nfs/client-identifier.html)（租约锁） | 服务器侧；客户端 mountstats unknown |
| NFSv4.1 协议 | src.ietf.rfc-8881 | [RFC 8881](https://datatracker.ietf.org/doc/html/rfc8881)（§2/§8.4/§9/§10.3.1/§10.4/§12/§18.3/§18.32/§18.51 锚点实测） | 协议文本；实现行为 unknown |
| 挂载/导出选项 | src.nfs-utils.nfs-5-man7 / src.nfs-utils.exports-5-man7 | [nfs(5)](https://man7.org/linux/man-pages/man5/nfs.5.html)（CTO/锁/sync/soft）、[exports(5)](https://man7.org/linux/man-pages/man5/exports.5.html)（async/sync/nohide/crossmnt/fsid） | Git 快照 2026-08-04（提交 2026-07-23）；release/commit 哈希 unknown |
| 通用挂载/NVMe/页缓存 | src.util-linux.mount-8-man7 / src.kernel.docs-nvme-v6.16 / src.kernel.docs-sysctl-vm-v6.16 | [mount(8)](https://man7.org/linux/man-pages/man8/mount.8.html)（util-linux 2.43.devel）、[quirk policy](https://www.kernel.org/doc/html/v6.16/nvme/feature-and-quirk-policy.html)、[sysctl vm](https://www.kernel.org/doc/html/v6.16/admin-guide/sysctl/vm.html)（drop_caches 非破坏性、dirty 回写） | 联盟规范原文 unknown；目标现场 unknown |

正文实际使用的子页：ext4 overview/globals、admin-guide/ext4、nfs41-server/knfsd-stats/client-identifier、NVMe policy；index 页仅作入口。未使用 exporting/pnfs/localio/reexport 具体内容（索引登记范围保留）。

## unknown 清单

1. nfs-utils release/commit 哈希；2. NVMe 联盟规范原文与设备写缓存；3. 客户端 mountstats/nfsstat；4. pNFS 客户端实现范围；5. extents/flex_bg 事后开启；6. 目标现场配置；7. 全部实测（未执行）。
