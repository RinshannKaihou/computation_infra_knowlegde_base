# 第二十一批 T04-07 来源记录

任务：T04-07（新建 `storage-client-backend-recovery.md`，与计划 target 对齐；T04-02/03/05/T04-06 依赖已通过）。作者取证轮次：首轮（Squid PG/OSD 排查页、健康检查页、2015 博客；复用 T04-02/03 登记）＋第二轮（v19.2.7 scrub-repair 测试函数行号、Lustre Ch.35/38 节号、nfs(5) 超时行、ext4 errors= 行；独立复核初审取证点）。

## 主张—来源定位表（ID—精确页面/节/行—字段/支持范围）

| 主张 | 登记 ID | 精确页面/节/行 | 支持范围 / 未覆盖 |
|---|---|---|---|
| PG 定位修复链 | src.ceph.docs-troubleshooting-pg-squid | [troubleshooting-pg](https://docs.ceph.com/en/squid/rados/troubleshooting/troubleshooting-pg/)（list-inconsistent-pg/obj、read_error 前置、repair 语义/auto_repair、Filestore 限定） | Squid 版；修复前清单即本链输出 |
| OSD 维护/FileStore 边界 | src.ceph.docs-troubleshooting-osd-squid | [troubleshooting-osd](https://docs.ceph.com/en/squid/rados/troubleshooting/troubleshooting-osd/)（FileStore 声明、add-noout、degraded） | Squid release notes 原文未见 unknown |
| 健康检查 | src.ceph.docs-health-checks-squid | [health-checks](https://docs.ceph.com/en/squid/rados/operations/health-checks/)（OSD_FULL/PG_DAMAGED/TOO_MANY_REPAIRS，阈值 default 10 已用） | 入口；其余阈值细节 unknown |
| 回归测试主案例 | src.ceph.test-scrub-repair-v19.2.7 | [osd-scrub-repair.sh@v19.2.7](https://github.com/ceph/ceph/blob/v19.2.7/qa/standalone/scrub/osd-scrub-repair.sh)（L93/L106/L225-244；其余未审计） | 正式测试；tracker #8914 未打开 unknown |
| 历史参考 | src.ceph.blog-manual-repair-object-2015 | [博客](https://ceph.com/en/news/blog/2015/ceph-manually-repair-object/)（FileStore 全链条） | 历史流程；不适用 Squid |
| NFS 客户端证据 | src.nfs-utils.nfs-5-man7 | [nfs(5)](https://man7.org/linux/man-pages/man5/nfs.5.html)（超时/soft/krb5i/server not responding） | 超时行；重传统计 unknown（内核 NFS 文档本任务未引用，已从 notes 去除） |
| ext4 证据 | src.kernel.admin-guide-ext4-v6.16 | [admin-guide/ext4](https://www.kernel.org/doc/html/v6.16/admin-guide/ext4.html)（errors= 三值） | 可用性行 |
| Lustre 证据 | src.lustre.ops-manual-2x | [手册](https://doc.lustre.org/lustre_manual.xhtml)（Ch.35.3/38.1/health_check/lfs） | Ch.36 未使用（与本任务无关） |
| RGW 证据 | src.ceph.docs-rgw-s3-squid | [S3 索引](https://docs.ceph.com/en/squid/radosgw/s3/)（版本化/multipart；健康/管理文档未检索 unknown） | 部署行 |
| 博客 kind | src.ceph.blog-manual-repair-object-2015 | schema 无博客类，沿用 documentation（与本库其他博客引用一致），walkthrough 性质 | — |

plan 列出但未使用来源的理由：src.ceph.docs-scrubbing-latest-2026-10-08（latest 版，本文统一用 Squid 版，已被替代）；src.ceph.repo-caf3def（main 主线 commit，本文实现锚用 v19.2.7 tag）；src.google.sre-data-integrity（恢复原则类来源，本文恢复原则以实现文档为准，SRE 未引用）。

## unknown 清单

1. tracker #8914；2. Squid release notes FileStore 原文；3. NFS 重传统计登记；4. RGW 日志端点；5. Lustre 计数器含义；6. repair 前清单指本链输出（`list-inconsistent-obj` JSON），无其他官方原文（unknown 已关闭项）。7. 目标现场配置；8. 全部实测与演练（未执行）。
