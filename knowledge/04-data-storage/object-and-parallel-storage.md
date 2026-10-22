---
id: data-storage.object-and-parallel-storage
title: 对象与并行存储版本化参考
type: reference
domain: data-storage
status: draft
platforms: [generic]
source_refs:
  - src.ceph.docs-rgw-s3-squid
  - src.ceph.docs-rgw-index-squid
  - src.ceph.repo-v19.2.7
  - src.ceph.docs-rgw-s3-latest-boundary
  - src.lustre.ops-manual-2x
  - src.lustre.release-info-wiki
updated_at: '2026-10-22'
summary: 以 Ceph Squid（v19 分支文档＋v19.2.7 实现锚）RGW S3 接口与 Lustre 2.x 手册（稳定锚 LTS 2.15.x）为双样板，解释对象 key/version、multipart、读回与 Lustre 命名空间/分条/锁/一致性，及部署组成、选型、瓶颈、观察点与最小验证设计。
related_ids:
  - data-storage.local-and-shared-storage
  - data-storage.checkpoint-integrity-evidence
  - data-storage.training-data-path
verification:
  status: source_checked
  evidence_refs:
    - src.ceph.docs-rgw-s3-squid
    - src.ceph.docs-rgw-index-squid
    - src.ceph.repo-v19.2.7
    - src.lustre.ops-manual-2x
    - src.lustre.release-info-wiki
  notes: "最终核对范围（修订与第五次定向复核已完成；记录见 docs/research/batch-20-t04-03-claude-recheck-5.md）：Squid S3 三页条目、RGW 索引部署入口、v19.2.7 src/rgw 定位、Lustre 手册 §1/§12/§19/§20/§22/§23/§34/§39 与术语表；latest 页仅边界；未做任何创建/读写实测。 2026-10-22 IQ-03 重核 Lustre §1.3.1/§19.5 的未写入空间与组合布局边界；条带覆盖判据仅为验证设计，未执行。"
---

# 对象与并行存储版本化参考

> 范围：Ceph Squid（v19）RGW S3 与 Lustre 2.x 各自独立取证。稳定锚：Ceph 取 Squid 分支文档＋v19.2.7 tag 实现定位；Lustre 取 2.x 滚动手册但主张只用 LTS 2.15.x 及以前引入的特性（DoM/FLR 均为 2.11 引入，PFL 为 2.10 引入）。`generic` 仅为导航聚合；RGW 兼容范围见 §2 末行，不等同 AWS S3；3FS 为未来扩展，不在本期。

## 1. 证据样板、版本与部署组成

| 样板 | 版本 | 取证入口 | 不覆盖 |
|---|---|---|---|
| Ceph RGW S3 | Squid（v19）分支文档（取证日 2026-10-13），点版本 unknown；实现锚 v19.2.7 tag（所指 commit 9ec952b9；tag 对象 c24c6707 非 commit） | [S3 索引](https://docs.ceph.com/en/squid/radosgw/s3/)（[serviceops](https://docs.ceph.com/en/squid/radosgw/s3/serviceops)、[bucketops](https://docs.ceph.com/en/squid/radosgw/s3/bucketops)、[objectops](https://docs.ceph.com/en/squid/radosgw/s3/objectops)） | 点版本行为差异；AWS S3 全集 |
| Ceph RGW 实现 | ceph/ceph v19.2.7（src/rgw 定位，未逐行审计；测试文件未定位 unknown） | [src/rgw 树](https://github.com/ceph/ceph/tree/v19.2.7/src/rgw)（rgw_op.cc 含 RGWCompleteMultipart/MultipartUpload/etag；rgw_rest_s3.cc 含 versionId） | 逐行语义审计；测试覆盖 |
| Ceph RGW 部署组成 | Squid 索引入口 | [RGW 索引](https://docs.ceph.com/en/squid/radosgw/)：librados 之上的 REST 网关；HTTP 前端；池配置；bucket 索引 resharding；multisite/zone 条目 | 守护进程/池/索引细节未逐页核对处 unknown |
| Lustre | 2.x 滚动手册（含 2.5–2.17 逐特性标记）；稳定锚 LTS 2.15.x（[Release Information](https://wiki.lustre.org/Lustre_Release_Information) 记 Current LTS Release 2.15.8，取证日 2026-10-13，该页动态变化；下载页仅列版本号，无 LTS 字样） | [手册全文](https://doc.lustre.org/lustre_manual.xhtml) | 精确小版本行为；目标现场配置 |
| Lustre 部署组成 | 手册 §1.2.2 | MGS/MGT、MDS/MDT、OSS/OST、客户端、LNet（[§1.2.2](https://doc.lustre.org/lustre_manual.xhtml) Lustre File System Components，节号为手册目录号） | 源码/release notes 未取（unknown；影响：实现细节以手册文本为准） |
| 反例边界 | latest 开发版（仅边界） | [latest objectops](https://docs.ceph.com/en/latest/radosgw/s3/objectops/)（页首 development 提示；与 Squid 文本已分叉） | 不作任何行为证据；dev scrub 页与 RGW 主题无关，已移除引用 |

## 2. 对象语义（Ceph RGW S3，以 Squid 文档为准）

| 条目 | 含义 | 条件或限制 | 证据位置 |
|---|---|---|---|
| key/version | 对象 key 命名空间；版本化三态：Enabled（每对象唯一 version ID）、Suspended（新增对象 version ID null）、从未设置（GET versioning 无状态返回）；仅 bucket owner 可设置 | Squid bucketops 版本化节原文；超出三态的语义 unknown | [bucketops](https://docs.ceph.com/en/squid/radosgw/s3/bucketops)（ENABLE/SUSPEND BUCKET VERSIONING） |
| versionId 返回位置 | versionId 在 Squid 文档中仅出现在 retention/legal-hold 查询参数；无 `x-amz-version-id` 响应头记载，无 ListObjectVersions 操作 | Features 表"Bucket Object Versions: Supported"仅为支持声明，不给出返回位置 | 同上＋[S3 索引 Features 表](https://docs.ceph.com/en/squid/radosgw/s3/) |
| multipart | Initiate、Upload Part（upload-id 不匹配返 404 NoSuchUpload）、List Parts（objectops）、List Bucket Multipart Uploads（bucketops，列 in-progress）、Complete（组装分片建新对象，请求体含 PartNumber 与 part ETag，响应含新对象 ETag）、Abort（仅语法页） | 按页拆分引用；Complete 前后可见性与列举一致性 Squid 文档未写明（unknown） | [objectops](https://docs.ceph.com/en/squid/radosgw/s3/objectops)、[bucketops](https://docs.ceph.com/en/squid/radosgw/s3/bucketops) |
| ETag | Squid bucketops 把 List 结果 ETag 写为 "An MD-5 hash of the object. (entity tag)"；objectops 只说 Complete 响应返回新对象 ETag、请求体含 part ETag，**无合成规则** | 本库不把 ETag 作内容哈希使用（理由：multipart 合成规则文档未给，且 bucketops 措辞本身诱导误读）；合成规则 unknown（未引源码） | 同上两页 |
| content-md5 | Put Object 与 Initiate Multipart 的可选请求头（base64 MD5）；只覆盖请求体 | 可选项；不等同读回后的内容哈希 | [objectops](https://docs.ceph.com/en/squid/radosgw/s3/objectops) |
| 读/列举 | GET/HEAD 支持全部五项请求头：range、if-modified-since、if-unmodified-since、if-match、if-none-match；GET Bucket 支持 prefix/delimiter/marker/max-keys（默认 1000）；`allow-unordered` 为非标准扩展 | 新对象多久可被列到：三页均未说明（unknown） | 同上两页 |
| Retention/Object Lock | Put/Get Object Retention 在 objectops；Object Lock 配置在 bucketops，前提为建 bucket 时启用 | 两处分开引用，不合并 | 同上两页 |
| Append Object（RGW 扩展） | `x-rgw-next-append-position`；409 状态（InvalidBucketstate 等）；不可用于已启用/暂停版本化的 bucket；列举 Type 含 Appendable/Normal | RGW 特有约束；移植到 AWS/其他服务前逐 API 核对 | [objectops](https://docs.ceph.com/en/squid/radosgw/s3/objectops) |
| 读到旧版本 | 待判定现象：须用 bucket 版本化状态＋清单 versionId 区分"正常的旧版本"与"发布未完成/顺序错误"，不预设正常 | 判定方法见 §5 | 版本化节＋§5 |
| 兼容模型 | "compatible with the basic data access model of the Amazon S3 API"；Features 表声明状态：List Buckets/Delete Bucket/Create Bucket、Lifecycle、Policy、Website、ACL、Location、Notification、Object Versions、HEAD、Put/Delete/Get Object 均为 Supported，Replication 为 Partial（仅跨 zone），canned ACL 为差异集合，另有 Unsupported Header Fields 表；非标准扩展：`allow-unordered`、Append Object（含 Appendable/Normal 列举类型） | "large subset"指覆盖广度；"既非子集也非超集"为本库推论（理由：含 RGW 独有扩展，反向移植须逐 API 核对）；条件读以 objectops GET/HEAD 五项请求头原文为据；对象列举以 bucketops GET Bucket 节（返回对象列表，prefix/delimiter/marker/max-keys）为据；**跨服务移植须逐 API 核对** | [S3 索引](https://docs.ceph.com/en/squid/radosgw/s3/) |

## 3. 并行存储语义（Lustre 2.x，以手册为准；引用为"章.节＋节名"，章号取手册目录）

| 条目 | 含义 | 条件或限制 | 证据位置 |
|---|---|---|---|
| 部署与命名空间 | MGS/MGT、MDS/MDT、OSS/OST、客户端、LNet；文件命名空间由 MDT 服务，数据分布在 OST | 元数据路径与数据路径分离；MDT 操作瓶颈与 OST 带宽瓶颈分开观测 | 手册 §1.2.2 |
| 一致性 | LDLM 跨客户端/服务器保证一致（§1.1.1：MDT LDLM 管 inode 权限与路径名，各 OST LDLM 管其条带锁）；默认强制 POSIX coherency；多客户端同写一文件出现 lock ping-pong（性能影响） | 目标现场锁参数 unknown | 手册 §1.1.1、§34.10 |
| 锁 | Extent lock：OSC 用来保护 OST 对象区段并发读写/大小获取/truncate 的 LDLM 锁；§34.8 lockahead/noexpand 建议 | 与 NFS 锁模型不互推 | 手册术语表、§34.8 |
| 分条 | stripe_count 默认 1、stripe_size 默认 1MB（文件系统可配，目录/文件可覆盖，现场实际 unknown）；stripe_count -1 表跨全部可用 OST，start_ost -1 由 MDS 选择；`lfs setstripe` 设布局，`getstripe` 查布局 | 小文件分条放大另行评估 | 手册 §1.3.1、§19.3/§19.4 |
| DoM/FLR/PFL | DoM（2.11 引入；MDT 空间通常应 ≥ 总空间 5%）、FLR（2.11 引入）、PFL（2.10 引入）；均 ≤ LTS 2.15.x，可纳入 | 超出 2.15.x 的特性不纳入 | 手册 Ch.20/Ch.22/§19.5 |

## 4. 接口、选型、瓶颈、观察点与异常（按实现分列）

| 维度 | Ceph RGW S3 | Lustre 2.x |
|---|---|---|
| 接口 | S3 REST（SDK/CLI）；管理面 radosgw-admin 未核对 unknown | POSIX 挂载＋`lfs` 布局管理 |
| 选型 | 大对象/版本化发布、跨客户端读回；multipart 发布条件见 §5 | 大文件高并发读写、分条调谐；小文件走 DoM 评估 |
| 容量/元数据瓶颈 | bucket/对象数与索引实现未核对 unknown | MDT 操作瓶颈 vs OST 带宽瓶颈，分开观测 |
| 观察点 | `GET /?usage`（按用户用量统计 TotalBytes/TotalEntries，非性能计数器）；radosgw-admin/日志未核对 unknown | Jobstats、Ch.12 Monitoring（Changelogs/Jobstats）、Ch.39 参数（如 OST stats；只列入口，不解释计数器含义） |
| 典型异常 | NoSuchUpload（404）、InvalidBucketstate/409、未完成 multipart 残留、版本错配 | Full OST（§23.1）、`BAD WRITE CHECKSUM` 日志（§23.5.1，客户端 32-bit 传输校验，ldiskfs 无持久校验，最多重试语义以手册为准）、同文件多写锁争用（§34.10） |

## 5. 最小验证设计（只设计不执行；三层先行定义）

三层定义：身份（RGW：bucket＋key＋versionId；versionId 获取位置 Squid 文档未给出——Complete 响应仅 Location/Bucket/Key/ETag，bucketops 无版本列举，记 unknown，待实现锚或读回试验；未启用版本化的 bucket 身份为 bucket＋key＋内容哈希（无 versionId 可用）；Suspended bucket 新增对象 versionId 为 null，按无有效版本对待，身份同样加内容哈希；Lustre：路径＋getstripe 布局，不含 FID——本库设计决定，理由为 FID 跨重建/迁移语义未核对）；ETag（RGW 实体标签，不作内容哈希）/ 校验和（传输层 `content-md5`（可选，只覆盖请求体）/Lustre wire checksum（32-bit，只覆盖传输）与应用层端到端哈希分开；端到端哈希本库设计约定：SHA-256，由发布方在发布前计算并写入清单，读回方重算比对）。

| 场景 | 前置＋可判定预期 | 失败判据 | 实际 |
|---|---|---|---|
| 对象发布 | multipart Complete；预期按身份分支：Enabled 且可获得 versionId 时 versionId 与清单一致，其他情况读回 SHA-256 与清单一致，且对象可见 | versionId/哈希任一不一致即失败；对象不可见即失败 | 未执行，留空 |
| 对象发布负向 | Abort 未完成上传；前置：该 upload-id 在 List uploads 可见；预期：Abort 后 List uploads 不再列出该上传 | 仍列出即失败 | 未执行，留空 |
| 跨客户端读回 | 发布完成；预期：读回字节与清单一致；`content-md5` 只覆盖请求体，与读回哈希分开记录 | 哈希不一致即失败 | 未执行，留空 |
| Lustre 多客户端 | 各客户端写互不重叠区间并关闭，第三客户端读回逐区间比对；预期：区间哈希全对（重叠写顺序不定，不作通过条件；锁争用影响性能见 §34.10） | 任一区间哈希错即失败 | 未执行，留空 |
| 条带写入覆盖（普通 RAID0 布局） | 固定单一普通 RAID0 布局与目标对象/OST 映射；从偏移 0 实际连续写入至少 `stripe_size × stripe_count` 字节，无空洞、无布局变更，写入成功并完成关闭；预期：getstripe 布局符合设定、读回哈希正确，且与该文件/测试窗口可关联的对象或 OST 写入观测覆盖全部预期目标 | 布局/哈希不符或观测显示目标未收到写入即失败；缺少可归属的写入证据时，覆盖结论为 unknown，不能判通过 | 未执行，留空 |

**覆盖判据的依据与反例**：[手册 §1.3.1 Lustre File System and Striping](https://doc.lustre.org/lustre_manual.xhtml#lustre_striping) 说明普通 RAID0 按条带轮转，未写入的数据不在 OST 上预留空间。因此逻辑文件大小达到一个条带周期（例如仅扩展长度的稀疏文件）不能证明每个目标实际收到写入；`getstripe` 证明布局，读回哈希证明所读内容，二者本身都不能替代逐目标写入证据。上表的连续实际写入与观测要求是本库验证设计，不是已执行结果。

[§19.5 PFL](https://doc.lustre.org/lustre_manual.xhtml#pfl) 的 composite layout 为不同 extent 配置不同子布局，不能套用单一 `stripe_size × stripe_count` 覆盖整文件。PFL、DoM、FLR 等其他布局须分别按组件范围、目标位置或镜像设计验证；目标版本的采集接口、计数器含义与证据归属方法尚未固定，仍需另行取证。

不填实测值，不标 reproduced。

## 来源与更新范围

- 上表各入口（Squid 版文档、v19.2.7 tag、Lustre 2.x 手册）。
- 待确认：Ceph 点版本行为差异；Lustre 精确小版本；RGW 管理统计端点；Lustre 计数器含义；版本化启用配置细节；默认条带现场值；FID 纳入；全部实测（未执行）。
