# 第二十批 T04-03 初审

审阅日期：2026-10-13（实际取证日）。正文 `updated_at` 与登记 `registered_at` 中的 `2026-10-14` 视为交付标签，不作为本轮取证日期；输入以下表 SHA-256 识别。

**结论：T04-03 需修订。新增 11 项发现（B20-C11–C21）：P1 ×3、P2 ×6、P3 ×2，全部 OPEN。** acceptance 1 有两项 P1 缺口（C11、C12），acceptance 4 有一项 P1 缺口（C13）；acceptance 2、3 各有 P2 缺口。`make check` 通过（90 content entries / 403 sources），但它只校验结构与本地链接，不说明技术正确性。正文 `verification.status: source_checked` 及 notes"已核对 … 锁章节"与下述来源原文有多处不一致，修订复核前不得据此视为已核对。

审阅者角色独立于作者。审阅模型为 `claude-opus-5-5`，由用户本次明确要求试用。这不是既有的 `gpt-6.1-sol / xhigh` 批量审阅约定，也不改写该约定；推理等级等运行元数据没有可核验记录，不补造。本轮只做审阅和只读取证：未改作者正文、来源记录、登记、索引或计划，未创建 bucket/对象，未挂载 Lustre，未执行任何读写或 benchmark。模型审阅不构成硬件或现场验证。

## 输入（以 SHA-256 识别）

| 输入 | SHA-256 |
|---|---|
| [T04-03 正文](../../knowledge/04-data-storage/object-and-parallel-storage.md)（83 行，reference / draft） | `9bf27e257fd25066f853b872bfc0a1f6774d3138889d24571ea1ab459ffbf19d` |
| [作者来源记录](batch-20-t04-03-sources.md)（15 行） | `d71e384a4da4fcc78dd5c576a44d06230e1e3c19902476c3d8923fd62f2bf33b` |
| [任务计划](../../plans/full-coverage-backlog.yaml)（T04-03 acceptance L5139–5143） | `f16309beadf5ae4f28d5fc7428a2348bea0cf08d155d57730a4d817cfcdd3e96` |
| [来源登记](../../sources/registry.yaml)（T04-03 新登记 L4995–5019；反例 L1055、L1069） | `6ed7f1d6ac7b70c259a11a471ccc02dda0ea23deaf43676a40d42e6cf27f2dec` |
| [04 索引](../../knowledge/04-data-storage/index.md)（工作区已改，旁证用，见 C20） | `b28f18f2286a8351b13f9829bf62ec763c19434bd59ccdc93edacb7e5e94dd2f` |

正文 `related_ids` 的三个 ID 与 `source_refs` 的四个 ID 都能解析。

## 一次源取证（审阅者独立获取）

全部用 `curl` 默认 TLS 校验只读获取，HTTP 均为 200。HTML 去标签后按文字核对，不只判可达性。原文只存在临时目录 `/tmp/t0403/`，未入库。

| 来源（登记 ID） | URL（最终） | SHA-256（原 HTML） | 核对点与结果 |
|---|---|---|---|
| Squid S3 索引（src.ceph.docs-rgw-s3-squid） | [s3/](https://docs.ceph.com/en/squid/radosgw/s3/) | `e48b4d877b49a9f80582c7a85d2e0f09e44e553cb4b67caada1b73e03cd4557f` | 首句写 RESTful API "compatible with the basic data access model of the Amazon S3 API"。Features Support 表中，Bucket Replication 为 "Partial / Permitted only across zones"，Create Bucket 与 ACL 为 "Different set of canned ACLs"，Multipart Uploads 与 Bucket Object Versions 为 Supported；另列 Unsupported Header Fields（`x-amz-id-2`）。页面无 latest 的 development 提示；页脚为 CC BY-SA 3.0。→ C16 |
| Squid serviceops（同上） | [serviceops/](https://docs.ceph.com/en/squid/radosgw/s3/serviceops/) | `a2fe21b0788d9a7c662a4cc4ee8c7aaa5e156ba7d2348a60887911a5c235417d` | List Buckets；**Get Usage Stats**（`GET /?usage`，返回 TotalBytes、TotalBytesRounded、TotalEntries 等）。→ C18 |
| Squid bucketops（同上） | [bucketops/](https://docs.ceph.com/en/squid/radosgw/s3/bucketops/) | `3f2a9d0db33f4910d7f85113723708e5ed4c59427d19efc3db451147fbf060ba` | GET Bucket 支持 prefix、delimiter、marker、max-keys（默认 1000）；`allow-unordered` 写明为 "Non-standard extension"。Contents 中 **ETag 写为 "An MD-5 hash of the object. (entity tag)"**，Type 为 Appendable 或 Normal。List Bucket Multipart Uploads（`GET /{bucket}?uploads`）列出 in-progress uploads。ENABLE/SUSPEND BUCKET VERSIONING 写明三态：Enabled 为每个对象分配唯一 version ID；Suspended 分配 version ID null；从未设置则 GET versioning 不返回状态。Object Lock 若建 bucket 时未启用，配置操作会失败。→ C13/C14/C15/C16 |
| Squid objectops（同上） | [objectops/](https://docs.ceph.com/en/squid/radosgw/s3/objectops/) | `14f5689f8f03a42761787b024a0558153519f30b585f9f1f0395e770f042e0ba` | Put Object 和 Initiate Multipart 有可选请求头 `content-md5`（"A base64 encoded MD-5 hash of the message"）。GET/HEAD 支持 range 与 if-match/if-none-match。Upload Part 不匹配时返回 404 NoSuchUpload。Complete 的说明为 "Assembles uploaded parts and creates a new object"，请求体含 PartNumber 与 part ETag，响应含新对象 ETag。Abort 只给出语法。**Append Object** 为 RGW 扩展：`x-rgw-next-append-position`，409 InvalidBucketstate，且不能用于已启用或暂停版本化的 bucket。versionId 只出现在 retention/legal-hold 的查询参数中，页面没有 versionId 响应头，也没有 ListObjectVersions 操作。→ C13/C14/C15/C16 |
| latest objectops（反例对照，未登记） | [latest objectops](https://docs.ceph.com/en/latest/radosgw/s3/objectops/) | `a394e1151900fedd55f5c080035ace0070bd4f57475f9cc85fe4f1c8b4baf1d3` | 页首有 "Notice: This document is for a development version of Ceph"。与 Squid 版逐词 diff，只多出 accounts 相关注释，并有 `Etag`/`ETag` 大小写差异。这说明 latest 与 Squid 文本确实可能分叉。→ C12 |
| Lustre 手册（src.lustre.ops-manual-2x） | 登记 `http://doc.lustre.org/lustre_manual.xhtml` → 重定向到 `https://doc.lustre.org/lustre_manual.xhtml` | `63b09d0650de3491eee9c976dff1246706dc6496bc996c139fdebdf7fc4a0d8c`（2,482,517 字节） | 标题 "Lustre* Software Release 2.x Operations Manual"，版权 Oracle 2010–2011 / Intel 2011–2017。手册中有 "Introduced in Lustre 2.5 … 2.17" 等逐特性标记，是滚动主线手册。章号核对：Ch.19 Managing File Layout (Striping)（19.3 setstripe、19.4 getstripe、19.5 PFL、19.9 Striping Internals），Ch.20 DoM 与 Ch.22 FLR 均标 "L 2.11"，Ch.12 Monitoring（Changelogs、Jobstats），Ch.39 Lustre Parameters。§1.1.1 写明 LDLM "ensures that files are coherent between all clients and servers"，MDT LDLM 管 inode 权限与路径名，每个 OST 有自己的 LDLM 管条带锁。§1.3.1 与 §19.3 写明默认 stripe_count 为 1、stripe_size 为 1MB。§34.10 写明 "By default … enforces POSIX coherency semantics"，多客户端同写一个文件会出现 lock ping-pong。§23.5.1 Lustre Checksums 写明客户端 in-memory 与 wire 两类 32-bit checksum，"ldiskfs backing file system does NOT do any persistent checksumming"，失配时记 `BAD WRITE CHECKSUM` 并最多重试五次。术语表 Extent lock 定义为 OSC 用来保护 OST 对象区段的 LDLM 锁。"glimpse" 在手册中只出现在 quota glimpse callback 场景。→ C12/C17/C18/C19 |

取证限制：

1. docs.ceph.com/en/squid/ 是 Squid **分支**文档，页面上没有点版本号（v19.2.x）标识，本轮也未取 releases 页。所以"Squid 文档对应哪一个补丁版本"在本轮仍是 unknown。
2. Lustre 手册是一个 2.4 MB 的单页 XHTML，本轮按章节标题和关键短语核对，没有通读全文。章节定位依赖 `<h2>/<h3>` 标题，可能漏掉嵌套较深的节。
3. 未取 Ceph 或 Lustre 源码、测试或 release notes（作者也未登记），所以 C11 只判断"缺失"，不判断实现行为本身。
4. HTML 转文本用正则去标签，未做版式级比对。
5. 未采集任何目标现场配置，也未做任何实测。

## 逐项发现

### B20-C11 — P1 / OPEN：两侧都缺"必要实现/测试和部署组成"

位置：正文 §1 表 L33–37、§4 L63；来源记录 L7–11；登记 L4995–5019。

证据：

- acceptance 1 要求 RGW 与 Lustre **分别**绑定"版本化官方文档、必要实现/测试和部署组成"。计划 `source_discovery`（L5152–5153）也要求查找"相关源码/测试"和"官方手册/源码"。
- 正文与来源记录只登记了两份文档。唯一的源码登记 `src.ceph.repo-caf3def` 是 main 主线（`src/ceph_release` 为 "21 umbrella dev"），只能用作反例，不能作为 Squid 的实现证据。
- 部署组成两侧都没有写出：RGW 侧缺 radosgw 守护进程、RADOS 池、bucket index；Lustre 侧缺 MGS/MGT、MDS/MDT、OSS/OST、客户端与 LNet。其实所取手册 §1.2（Management Server、File System Components、LNet、Lustre Cluster）已经直接覆盖 Lustre 部署组成，正文 §3 只写"手册 MDT/OST 章节"，没有给出锚点。
- 正文和来源记录都没有说明"为何不需要实现/测试"。

关闭条件：

- RGW：登记一个 Squid 点版本 tag 下的 ceph/ceph 固定 commit，用来定位 `src/rgw/` 中与本文主张相关的实现或测试（multipart 完成、ETag、版本化）。如果判断某项主张不需要实现证据，就在来源记录中逐条说明理由，并把对应主张标为"仅文档"。
- Lustre：登记所选稳定发布对应的源码或 release notes（例如某个 LTS tag），或者明确写"未取，unknown"及其影响范围。
- 两侧各补一行"部署组成"。Lustre 引手册 §1.2 的精确节名；RGW 引 Squid 版架构或部署页（新增登记）。未核实的组成写 unknown。
- 不能因为 scaffold 或部署条目存在，就写成"已覆盖实现"。

### B20-C12 — P1 / OPEN：版本绑定不成立——Ceph 只锚分支，Lustre 手册是滚动主线

位置：正文 §1 L35–36、frontmatter L14 summary、L29 范围注；登记 L5000、L5014；来源记录 L3（"releases 版本锚"）。

证据：

- Ceph：`/en/squid/` 是分支文档，页面上没有点版本号。来源记录 L3 声称取了"releases 版本锚"，但 registry 中没有对应登记，正文也没有链接。正文写"Squid（v19）"可以接受，但不能写成"已绑定稳定版行为"，至少要写明"分支文档，点版本 unknown"。
- Lustre：手册标题只写 "Release 2.x"，正文中带 "Introduced in Lustre 2.5 … 2.17" 等逐特性标记，说明它是随主线更新的滚动手册。用它证明"所选稳定版"的行为，和用 Ceph latest 证明 Squid 行为是同一类错误，只是本身没有 dev 提示。正文把"精确小版本 unknown"放在"不覆盖"列，等于没有选定稳定版，acceptance 1 的"所选稳定版"无法成立。
- 反例行用 scrubbing-latest 作对照，但它与 RGW S3 主题无关。本轮实取的 latest objectops 有 development 提示，且与 Squid 文本已出现分叉，比 scrubbing 页更能直接说明边界。

关闭条件：

- Ceph：在登记 revision 中写明"Squid 分支文档，取证日 2026-10-13（或作者实际日期），点版本 unknown"。如果要锚定点版本，就新增 releases 页或 tag 登记，并在正文写出该版本号。
- Lustre：选定一个稳定发布（例如某 LTS 版本），在正文与登记中写明"手册为 2.x 滚动版；本文主张只取所选版本及以前引入的特性"。DoM、FLR、PFL 等特性逐项标注手册中的引入版本（见 C17），超出所选版本的特性不纳入。
- 反例行可补 latest objectops 的 development 提示（需登记），或者删除与主题无关的 scrubbing 反例，只保留"latest 不证明 Squid"这一原则。

### B20-C13 — P1 / OPEN：ETag 规则的证据与所引页面原文相反；"ETag 仅作传输完整性参考"无来源

位置：正文 §2 L45（ETag 行）、§4 L67（"ETag 误作哈希"）、§5 L74；登记 L5000（"核对 … ETag"）。

证据：

- 正文 L45 写"multipart ETag 合成规则与单体不同"，证据位置是"同上（ETag 条目）"，即 Squid objectops。但 objectops 只说 Complete 响应返回 "The entity tag of the new object"，part ETag 是 "The part's entity tag"，**没有给出任何合成规则**。
- Squid bucketops 的 ListBucketResult 把 ETag 写成 **"An MD-5 hash of the object. (entity tag)"**。所引版本化文档本身就在诱导读者把 ETag 当成内容哈希，正文的"不得混用"恰好需要直接回应这一处原文，现在反而把它当成了支持证据。
- 正文 L74 写"ETag 仅作传输完整性参考"，Squid 三页中没有这个说法。文档中真正与传输完整性相关的机制是 Put Object 和 Initiate Multipart 的可选请求头 `content-md5`，正文没有提到。
- acceptance 4 的核心就是"身份/ETag/校验和不混用"，证据绑定错误属于阻断项。

关闭条件：

- ETag 行如实转述 Squid bucketops 的原文措辞，并标注"本库不把它作为内容哈希使用"及理由。multipart ETag 的合成规则要么引 Squid 点版本源码（随 C11 登记），要么写 unknown，不再引 Squid 页面作为依据。
- 删除或改写"ETag 仅作传输完整性参考"。如果保留传输层校验，改引 `content-md5` 请求头，并写明它只是可选项、只覆盖请求体，不等于读回后的内容哈希。
- 同步修正登记 L5000 的 notes，说明该页 ETag 条目的实际措辞。

### B20-C14 — P2 / OPEN：版本化三态已有文档却记为 unknown；versionId 返回与"旧版本"判断无来源

位置：正文 §2 L43（key/version 行）、L46（"读到旧版本属版本化语义"）、L83（待确认"版本化启用配置"）；来源记录 L15 第 6 项。

证据：

- Squid bucketops 的 ENABLE/SUSPEND BUCKET VERSIONING 写明了 Enabled、Suspended（version ID null）和从未设置三态，以及只有 bucket owner 能设置。正文 L43"版本化须显式启用（配置细节未细核，unknown）"和 L83 的 unknown 与此不符。
- L43"versionId 按版本化配置返回"的证据是 objectops，但 objectops 中 versionId 只是 retention/legal-hold 的查询参数。页面没有 `x-amz-version-id` 响应头，也没有 ListObjectVersions 操作；索引 Features 表只写 "Bucket Object Versions: Supported"。
- L46"读到旧版本属版本化语义，不等同损坏"在三页中都没有依据，而且把"读到旧版本"这个现象预设成正常行为，可能掩盖发布顺序问题。
- 另外：Append Object 不能用于已启用或暂停版本化的 bucket（409 InvalidBucketstate），这是 RGW 特有的版本化约束，正文没有写。

关闭条件：

- key/version 行改引 bucketops 版本化节，写清三态与 null version ID，删除对应的 unknown。
- versionId 的返回位置（响应头或列举）如果 Squid 文档未写，标 unknown 并说明"Features 表只声明 Supported"；不要引 objectops 作为依据。
- "读到旧版本"改为待判定的现象：需要用版本化状态和清单中的 versionId 才能区分"正常的旧版本"与"发布未完成或顺序错误"，不预设结论。

### B20-C15 — P2 / OPEN：multipart/commit/read/list 语义条目证据错位，可见性主张无来源

位置：正文 §2 L44（multipart 行）、L46（读/列举行）。

证据：

- L44 把 ListMultipartUploads 和其他操作一起记在"同上"（objectops）下，但它实际在 bucketops（List Bucket Multipart Uploads，列出 in-progress uploads）。objectops 中对应的是 List Multipart Upload Parts。
- L44"完成前对象不可见（语义以页为准）"在 Squid 页面中找不到对应文字。页面只说 Complete "Assembles uploaded parts and creates a new object"。"以页为准"这类兜底写法把核对工作推回给读者，不能算作取证。
- L46 写"bucketops Retention"，但 Put/Get Object Retention 在 objectops；bucketops 中是 Object Lock 配置，且有前提：必须在建 bucket 时启用，否则操作失败。
- 读与列举的已文档化要点没有写出：GET/HEAD 的 range、if-match 条件读；GET Bucket 的 prefix、delimiter、marker、max-keys（默认 1000）；`allow-unordered` 为非标准扩展；Upload Part 的 404 NoSuchUpload。列举与读之间的一致性（新对象多久能被列到）三页均未说明，应记 unknown，但正文没有记。

关闭条件：

- multipart 行拆为 Initiate、Upload Part（NoSuchUpload）、List Parts（objectops）、List Bucket Multipart Uploads（bucketops）、Complete、Abort，各自给出正确的页面。
- 可见性：引用能支持的原文；不能支持的写"Complete 前后可见性与列举一致性：Squid 文档未写明，unknown"。
- Retention 与 Object Lock 分开列，写明各自的页面与前提条件。
- 读与列举行补上 range/条件读、列举参数与默认值；`allow-unordered` 同时并入 C16 的扩展清单。

### B20-C16 — P2 / OPEN："RGW 实现 S3 子集"表述不准确，兼容边界没有用到已取的特性表

位置：正文 §2 L47、§1 L35"不覆盖"列、L29 范围注。

证据：

- Squid 索引原文是 "compatible with the basic data access model of the Amazon S3 API"，并附 Features Support 表：部分特性为 Partial（Bucket Replication 仅跨 zone），ACL 为 "Different set of canned ACLs"，另有 Unsupported Header Fields。
- RGW 同时有 AWS S3 没有的非标准扩展：GET Bucket 的 `allow-unordered`，Append Object（`x-rgw-next-append-position`），列举结果中的 `Type: Appendable/Normal`。
- 所以 RGW 既不是 AWS S3 的子集，也不是超集。正文写"子集"会让读者以为"RGW 能做的 AWS 都能做"。这在反方向移植时（从 RGW 迁到 AWS 或其他兼容服务）会出问题。acceptance 3 要求的"兼容范围不等同"需要具体到条目。

关闭条件：

- 把"S3 子集"改为"兼容 S3 基本数据访问模型；按 Squid Features 表逐项标注 Supported/Partial/差异；另有非标准扩展"，并引用索引 Features 表与具体扩展所在页面。
- 列出本文用到的操作（multipart、版本化、条件读、列举）在 Features 表中的状态，再写一句"跨服务移植须逐 API 核对"。

### B20-C17 — P2 / OPEN：Lustre 锁/一致性/DoM/FLR/默认条带写成"以手册为准"或 unknown，而手册有明文

位置：正文 §3 L53–57、§1 L36；L83 待确认"默认条带"；来源记录 L15 第 5 项。

证据：

- 一致性：§1.1.1 "Lustre Features" 写明 LDLM "ensures that files are coherent between all clients and servers"，MDT LDLM 管 inode 权限与路径名，每个 OST 自己的 LDLM 管其上的条带锁。§34.10 写明默认强制 POSIX coherency 语义，多客户端同写一个文件会出现 lock ping-pong。正文 L57"条带条件下的数据可见性以手册为准"没有转述这些可以直接引用的内容。
- 锁：术语表把 Extent lock 定义为 OSC 用于保护 OST 对象区段并发读写、文件大小获取与 truncate 的 LDLM 锁；§34.8 有 lockahead 与 noexpand。正文 L56 的 "glimpse" 在手册中只出现在 quota glimpse callback 场景，没有与客户端文件大小相关的描述，属于无来源的术语。
- DoM/FLR：手册目录中 Ch.20 DoM 与 Ch.22 FLR 均标 "L 2.11"；容量章节写明 DoM 在 2.11 及以后使用时，MDT 空间通常应不少于总空间的 5%。正文 L55"适用条件与版本支持以手册为准，不概括"回避了这些已有的明文。
- 默认条带：§1.3.1 与 §19.3 写明默认 stripe_count 为 1、stripe_size 为 1MB；stripe_count 设为 -1 表示条带跨所有可用 OST，start_ost 默认 -1（由 MDS 选择）。正文 L54 和 L83 把它记为"未核对 unknown"。
- 命名空间与 MDT/OST 行的证据位置写"手册 MDT/OST 章节"，没有节号（应为 §1.2.2）。

关闭条件：

- 一致性行改写为"LDLM 跨客户端/服务器保证一致性（§1.1.1）；默认 POSIX coherency，同文件多写者会锁争用（§34.10）"。目标现场的锁参数等未覆盖部分标 unknown。
- 锁行引术语表 Extent lock 和 §34.8。删除 glimpse，或者另找能支持它的来源。
- DoM/FLR 行写出引入版本 2.11，并与 C12 选定的稳定版对照；补 DoM 的 MDT 容量条件。
- 默认条带改写为手册默认值，并注明"文件系统或目录可覆盖，现场实际默认值 unknown"。
- 所有证据位置改为"章.节 + 节名"。

### B20-C18 — P2 / OPEN：观察点与典型异常记为 unknown，而已取的一次源已有覆盖

位置：正文 §4 L65–67；L83–84 待确认"RGW 管理统计端点""Lustre 性能计数器"；来源记录 L15 第 3、4 项。

证据：

- RGW：作者声称已核对的 Squid serviceops 中就有 Get Usage Stats（`GET /?usage`，按用户统计 TotalBytes、TotalEntries）。正文 L66"具体端点未登记，unknown"与此不符。可写入异常行的已文档化错误码有：NoSuchUpload（404）、InvalidBucketstate、PositionNotEqualToLength、ObjectNotAppendable（409）、BucketAlreadyExists。
- Lustre：Ch.12 Monitoring（Changelogs、Jobstats、LMT、CollectL），Ch.39 Lustre Parameters（例如 `lctl get_param osc.*.stats` 的 OST 统计，stats 文件中的 ldlm_enqueue）。§23.1 Handling Full OSTs 对应正文的"条带失衡"。§23.5.1 的 `BAD WRITE CHECKSUM` 日志是可以写进典型异常的具体信号。
- acceptance 3 要求观察点和异常按实现列出。这里不是缺少来源，而是没有使用已取的来源。

关闭条件：

- RGW 观察点补 `GET /?usage`（注明它是按用户的用量统计，不是性能计数器）。radosgw-admin 和日志如果仍未核实，单独保留 unknown。
- Lustre 观察点补 Jobstats、`*.stats` 参数与 Ch.12/39 的锚点。具体计数器的含义如果没有逐项核对，只列入口，不解释计数器含义。
- 典型异常行改为"信号＋出处"：RGW 错误码；Lustre 的 Full OST、checksum 失配日志、同文件多写者的锁争用（§34.10）。

### B20-C19 — P2 / OPEN：最小验证设计缺可判定的预期与门槛，校验层次没有分开

位置：正文 §5 L71–78。

证据：

- "身份"没有按实现定义：RGW 身份应是 bucket + key + versionId（版本化状态由 C14 决定），Lustre 身份是路径与布局（FID 是否纳入由作者决定）。L73 门槛"清单登记 key/version/长度"缺少内容哈希，而 L74 的内容哈希又没有说明算法、计算者和比对时点。
- Lustre 的 checksum 有明确边界：§23.5.1 说明客户端 checksum 是 32-bit 传输校验，ldiskfs 不做持久化校验。所以 L75/L76 的"内容哈希"必须是应用层端到端哈希，而且不能用 Lustre 的 wire checksum 代替。正文没有写这一层次划分，也没有引用 §23.5.1。
- L75"同一文件并发写后关闭 → 按锁协议可见"缺少可以判定的预期：应规定各客户端写入互不重叠的字节区间，关闭后由第三个客户端读回，逐区间比对哈希。重叠写入的结果顺序不确定，不能作为通过条件。这一设计还应引 §34.10 说明锁争用对性能的影响。
- L76 条带条件缺少覆盖条件：文件大小应不小于 stripe_size × stripe_count，才能保证每个 OST 都被写到；预期应同时检查 getstripe 布局与读回哈希。
- 对象发布缺少负向用例：Abort 后 List Bucket Multipart Uploads 不再列出该上传；Complete 后读回的 versionId 与清单一致；`content-md5` 只校验请求体，与读回哈希分开记录。

关闭条件：

- §5 先给出"三层"定义表：身份（按实现）、ETag（RGW 实体标签，不作内容哈希，见 C13）、校验和（传输层的 `content-md5` 或 Lustre wire checksum，与应用层端到端哈希分开）。
- 每个场景补可判定的预期与失败判据，包括上面列出的区间写、文件大小覆盖条件与负向用例。
- 继续保持"未执行，留空"，不标 reproduced。

### B20-C20 — P3 / OPEN：索引把 04.2 写成"交付完成"，正文把 verification 写成 source_checked，都早于审阅关闭

位置：[04 索引](../../knowledge/04-data-storage/index.md) L41；正文 frontmatter L19–24。

证据：

- 索引 L41 写"04.2 交付完成（T04-02/T04-03）"。但 T04-03 本轮未通过审阅，计划中 04.2 的 `content_acceptance_batch: 21`、`content_acceptance_status: planned`，gap 状态仍为 open。
- 正文 `verification.status: source_checked`，notes 写"已核对 … 锁章节"。C13–C18 表明多处核对结论与原文不符。

关闭条件：

- 索引改为"T04-03 已交付草稿，审阅中"之类的状态，主题验收留给 Batch 21。
- verification notes 只写实际核对过且与原文一致的条目；修订后再由定向复核确认。

### B20-C21 — P3 / OPEN：登记与来源记录的若干记载不准确

位置：登记 L5000、L5011、L5014；来源记录 L3、L7–15。

证据：

- L5000 写"核对 … versionId 条目"，但 objectops 中 versionId 只是查询参数（见 C14）；"ETag 条目"的实际措辞也没有记录（见 C13）。
- L5011 登记的 URL 是 `http://`，实际重定向到 `https://doc.lustre.org/lustre_manual.xhtml`。L5014 的 revision 没有记录"逐特性标记至 2.17，是滚动手册"这一点。
- 来源记录 L3 的"releases 版本锚"在登记中找不到对应项。来源记录没有保存取证日期或原文 SHA，后续复核无法比对页面是否已变化。

关闭条件：

- 按 C12–C14 的修订同步更新登记 notes 与 revision。Lustre URL 改为 https，revision 补"2.x 滚动手册，含 Introduced in 2.5–2.17 标记"。
- 来源记录补取证日期与页面 SHA-256（可参照本报告的一次源表）。releases 锚点要么登记，要么删除。

## 对照 acceptance 汇总

| acceptance | 判定 | 阻断发现 |
|---|---|---|
| 1 版本化官方文档＋实现/测试/部署；不以 latest dev 证明稳定版 | 未满足 | C11（P1）、C12（P1）；原则表述本身正确（latest 只作反例） |
| 2 对象语义与 Lustre 语义分开 | 部分满足：分栏正确，条目证据错位或回避明文 | C14、C15、C17（P2） |
| 3 接口/选型/瓶颈/观察点/异常按实现列；RGW ≠ AWS S3 | 部分满足：分列结构正确，观察点与兼容边界不准确 | C16、C18（P2） |
| 4 最小验证设计＋内容校验门槛；身份/ETag/校验和不混用 | 未满足 | C13（P1）、C19（P2） |

## 结论

**T04-03 未通过初审。新增 B20-C11–C21 共 11 项，全部 OPEN：P1 三项（C11、C12、C13），P2 六项（C14–C19），P3 两项（C20、C21）。** P1 与 P2 全部关闭前，不得声明审阅通过。修订后需要按发现 ID 做定向复核。

正文的骨架方向是对的：双样板分栏、latest 只作反例、"未执行不标 reproduced"、不把 RGW 等同 AWS S3 的原则。主要问题集中在三处：

1. 一次源已有明文的内容被记为 unknown 或"以手册/页为准"（C14、C17、C18）。
2. 证据位置与原文不符，其中 ETag 一处与原文正好相反（C13、C15）。
3. 缺少 acceptance 1 要求的实现/测试/部署组成和可成立的稳定版锚定（C11、C12）。

本报告只覆盖编辑与来源层面，不构成硬件、部署或现场验证。
