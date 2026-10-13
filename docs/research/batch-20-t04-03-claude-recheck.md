# 第二十批 T04-03 定向复核（作者首轮修订后）

复核日期：2026-10-13（实际取证日）。正文 `updated_at` 与登记 `registered_at` 中的 `2026-10-14` 视为交付标签。

**结论：T04-03 未通过定向复核。B20-C11–C21 共 11 项：CLOSED 4（C14、C17、C18、C20），OPEN 7（C11、C12、C13、C15、C16、C19、C21）。三项 P1（C11、C12、C13）都还没关闭。** 正文修订方向正确，大部分实质缺口已补上。剩下的问题主要有三类：

1. 修订映射和派单说明称 rgw-s3、lustre 两项登记的 revision"已更新"，但工作区 `sources/registry.yaml` 中这两项与初审时逐字相同（见 C12、C13、C21）。
2. 新登记的 v19.2.7 实现锚把 tag 对象 SHA 写成了 commit（C11）。
3. 新增的 LTS 锚点没有登记来源，所引下载页上也没有"LTS"字样（C12）。

审阅者角色独立于作者。审阅模型为 `claude-opus-5-5`，由用户本次明确要求使用。这不是既有的 `gpt-6.1-sol / xhigh` 批量审阅约定，也不改写该约定；推理等级等运行元数据没有可核验记录，不补造。本轮只做只读取证，只写本报告：未改作者正文、来源记录、修订映射、登记、索引或计划，未创建 bucket 或对象，未挂载 Lustre，未执行任何读写或 benchmark。作者自述已独立复核初审的全部取证点，本报告不采信该自述，以下各项均为审阅者重新取证的结果。模型审阅不构成硬件或现场验证。

## 输入（以 SHA-256 识别）

| 输入 | SHA-256 |
|---|---|
| [T04-03 正文](../../knowledge/04-data-storage/object-and-parallel-storage.md)（96 行） | `1a92dd9f2d2122edc306045a56450aab28c3492e3a699a3becec9d8d182b89b9` |
| [作者来源记录](batch-20-t04-03-sources.md)（16 行） | `f3c8475ac028d59a576f4a8ec1a03e4483b83bca2fd69d680032b90f7a8ffc1e` |
| [修订映射](batch-20-review-fixes.md)（T04-03 节 L53–65） | `30512b9f5644b84afc48f5aac0f7600667b29baebeb1f60ba2784fd98c5bb5bc` |
| [初审报告](batch-20-t04-03-claude-review.md) | `5b869706aae097dc79d0ca922f53a4da755e2e57b603f7f4809f9e7e617d90cd` |
| [任务计划](../../plans/full-coverage-backlog.yaml)（T04-03 acceptance 4 条） | `f16309beadf5ae4f28d5fc7428a2348bea0cf08d155d57730a4d817cfcdd3e96`（与初审相同） |
| [来源登记](../../sources/registry.yaml)（406 项；T04-03 相关 L4995–5058） | `d32d9ff1e794e331a13bf6789a3927e2ad7bef12953b70c4659e167f70c4fbba` |

`make check`：PASS（90 content entries / 406 sources）。它只校验结构与本地链接，不说明技术正确性。

## 一次源重取证（审阅者独立获取）

全部用 `curl` 默认 TLS 校验只读获取，HTTP 均为 200。原文只存放在临时目录 `/tmp/t0403r/`，未入库。

| 来源 | SHA-256 / 结果 | 核对点 |
|---|---|---|
| Squid s3 索引、serviceops、bucketops、objectops | 四页 SHA 与初审**逐字节一致**（`e48b4d87…`、`a2fe21b0…`、`3f2a9d0d…`、`14f5689f…`） | 版本化三态及"must be the bucket owner"；Features 表；409 PositionNotEqualToLength / ObjectNotAppendable / InvalidBucketstate；409 BucketAlreadyExists；Upload Part 404 NoSuchUpload 原文为 "Specified **upload-id** does not match any initiated upload on this object"；GET 的 range 头 |
| latest objectops | `a394e115…`，与初审一致 | development 提示 |
| Squid RGW 索引 [radosgw/](https://docs.ceph.com/en/squid/radosgw/)（新登记 rgw-index-squid） | `695cd90d5fc04a76c9de3b9ba15a3ef205562acc084d11b7fdecf5afe848cbea` | "object storage interface built on top of librados"；"Ceph Object Gateway daemon (radosgw)"；"does NOT use the Ceph Metadata Server"；目录含 HTTP Frontends、Multisite、Zone、Pool Placement、Configuring Pools、Dynamic bucket index resharding。**S3 接口措辞为 "compatible with a large subset of the Amazon S3 RESTful API"**（→ C16） |
| ceph/ceph tag v19.2.7（新登记 repo-v19.2.7） | `git ls-remote`：`refs/tags/v19.2.7` → `c24c670729945982079397f922db1a750ddc16f4`；`refs/tags/v19.2.7^{}` → **`9ec952b9f9668e9fa97e29a4c2b51e951674df2a`** | 带注释的 tag：`c24c6707…` 是 tag 对象，`9ec952b9…` 才是 commit（→ C11）。该 tag 下 `src/ceph_release` 为 "19 / squid / stable"。`rgw_op.cc` 含 `RGWCompleteMultipart`（8 处）、`MultipartUpload`（13 处），`check_previously_completed` 中 L6569–6574 用各 part ETag 计算 MD5 后拼接 "-<part 数>"。`rgw_rest_s3.cc` 含 `versionId`，并在 L469、L2756、L2762、L3495、L4111 输出 `x-amz-version-id` 响应头 |
| Lustre 手册 | `63b09d06…`，与初审一致；`http://` 重定向到 `https://` | 节号与节名：§1.1.1 Lustre Features、§1.2.2 Lustre File System Components、§1.3.1、Ch.12（§12.2 Lustre Jobstats）、§19.3/§19.4、§19.5 PFL "L 2.10"、Ch.20 DoM 与 Ch.22 FLR "Introduced in Lustre 2.11"、§23.1、§23.5.1、§34.8 Server-Side Advice and Hinting（L 2.9；lockahead/noexpand）、§34.10、Ch.39；术语表 Extent lock；DoM 2.11+ 时 "MDT space should typically be 5 percent or more"；checksum 失配时 "re-read or re-write … up to five times"。手册中有 "Introduced in Lustre 2.16" 等标记 |
| [lustre.org/download](https://www.lustre.org/download/)（**未登记**） | — | Latest News 列 "Lustre 2.17.0 released"、"Lustre 2.15.8 released"，**页面无"LTS"字样**（→ C12） |
| [wiki.lustre.org/Lustre_Release_Information](https://wiki.lustre.org/Lustre_Release_Information)（未登记，旁证） | — | "Current LTS Release: Lustre 2.15.8, Released December 2, 2025" |

取证限制：

1. 只按函数名和关键字定位 RGW 源码，没有逐行审计，也没有定位测试文件。
2. Lustre 手册仍然只按标题和关键短语核对，没有通读全文。
3. HTML 用正则去标签，没有做版式级比对。
4. 没有采集任何目标现场配置，也没有做任何实测。

## 逐项复核

### B20-C11 — P1 / **OPEN**

已满足：

- RGW 侧登记了 v19.2.7 tag（`src/ceph_release` 确为 squid stable），`src/rgw` 中的定位与上表一致。
- Lustre 侧写明"源码/release notes 未取（unknown；影响：实现细节以手册文本为准）"（正文 L42）。
- 两侧都补了部署组成行（L40、L42、L64）。§1.2.2 节名正确。RGW 索引原文支持 librados、HTTP 前端、池、resharding、multisite/zone 这几项。

剩余问题：

- **事实错误**：登记 L5025 和正文 L38 写"commit c24c6707…"。实际 `c24c6707…` 是 annotated tag 对象，peeled commit 是 `9ec952b9f9668e9fa97e29a4c2b51e951674df2a`。登记还写着"经 ls-remote 核对"，说明取到了未解引用的那一行。

关闭条件：

- 登记 revision 与正文改为"tag v19.2.7（tag 对象 c24c6707…，commit 9ec952b9…）"，或者只写 commit。

非阻断：

- RGW 索引原文直接写了 radosgw 守护进程，也写了"不使用 Ceph MDS"。L40 可以写出这两点，不必把它们归入"未逐页核对 unknown"。
- 来源记录可以补一句：本文的 RGW 行为主张均为"仅文档"，实现锚只用于定位。

### B20-C12 — P1 / **OPEN**

已满足：

- 正文 L38 写明"Squid 分支文档（取证日 2026-10-13），点版本 unknown"。
- 正文 L32、L41 写明 Lustre "2.x 滚动手册（含 2.5–2.17 标记）"，主张只用 2.15 及以前引入的特性。DoM、FLR 为 2.11，PFL 为 2.10，§34.8 为 2.9，都不晚于 2.15，与手册标记一致。
- 反例改用 latest objectops（新登记），并移除了 dev scrub 的引用。

剩余问题：

1. **登记未同步**（关闭条件 1、2 的"登记中写明"部分）：
   - 登记 L5000 的 rgw-s3-squid revision 仍是"Ceph Squid（v19）版本化文档 …"，没有"分支文档／取证日／点版本 unknown"。
   - 登记 L5014 的 Lustre revision 仍是"精确小版本绑定 unknown"，没有"滚动手册"和所选 LTS 锚。
   - 登记 L5008 的 notes 仍写"latest/dev 文档（已登记 scrubbing-latest）"，与"dev scrub 引用已移除"的说法不一致。
   - 这两项与初审时逐字相同。修订映射 C12/C21 和派单说明称已更新，与工作区不符。T04-02 第三轮曾出现"脚本缺 write 未落盘"，本次疑似同类问题，作者应自查。
2. **LTS 锚无登记来源**：正文 L32、L41 的"稳定锚 LTS 2.15.x（下载页列 2.15.8）"没有对应的登记项。所引 lustre.org 下载页只列 "2.15.8 released"，不写 LTS。审阅者旁证 wiki "Lustre_Release_Information" 写有 "Current LTS Release: Lustre 2.15.8"，但它也未登记。

关闭条件：

- 按上述三处同步登记 revision 与 notes。
- 登记一个能写明 2.15 为 LTS 的页面（例如上述 wiki 页，记取证日），并在正文 L41 改引该页。

### B20-C13 — P1 / **OPEN**

已满足：

- 正文 L52 如实转述了 bucketops 的 "An MD-5 hash of the object. (entity tag)"，写明本库不把 ETag 当作内容哈希及其理由，并把合成规则记为 unknown（未引源码）。
- L53 写明 `content-md5` 是可选项，只覆盖请求体，不等于读回哈希。
- "ETag 仅作传输完整性参考"一句已删除。

剩余问题：

- **关闭条件 3 未满足**：登记 L5000 仍写"核对 multipart/ETag/versionId/Retention 条目"，没有记录 ETag 条目的实际措辞，也没有记录 versionId 只是查询参数。

关闭条件：

- 按初审 C13 的条件同步登记 L5000 的 notes 或 revision。

非阻断：

- 已登记的 v19.2.7 中，`rgw_op.cc` L6569–6574 在 `check_previously_completed` 里用各 part ETag 计算 MD5，并拼接 "-<part 数>"。这是一处与 multipart ETag 相关的计算，但它出现在"重复完成检查"路径中，不能直接当作对外合成规则的证据。正文保留 unknown 是可以接受的。若要关闭这个 unknown，需要进一步定位 Complete 主路径。

### B20-C14 — P2 / **CLOSED**

证据：

- 正文 L49 的三态和"仅 bucket owner 可设置"与 bucketops 原文一致（"must be the bucket owner"、"version ID null"、"does not return a versioning state value"）。
- L50 把 versionId 返回位置限定为"在 Squid 文档中"未记载，并写明 Features 表只声明 Supported。
- L57 把"读到旧版本"改为待判定现象。
- L56 写了 Append 的 409 约束。

非阻断：

- L96 待确认项和来源记录 unknown 第 6 项"版本化启用（配置）细节"与 L49 已文档化的三态容易混淆，建议写明具体指什么（例如 MFA delete 等），或者删除。
- 已登记的 v19.2.7 中，`rgw_rest_s3.cc` 多处输出 `x-amz-version-id` 响应头。正文"文档未记载"的表述本身成立；实现侧证据可以作为 §5 获取 versionId 的路径（见 C19）。

### B20-C15 — P2 / **OPEN**

已满足：

- multipart 已按页拆分：List Parts 在 objectops，List Bucket Multipart Uploads 在 bucketops。
- 可见性与列举一致性记为 unknown。
- Retention 与 Object Lock 分开列，并写了前提条件。
- range、if-match/if-none-match、列举参数、max-keys 默认 1000、`allow-unordered` 都已补上。

剩余问题：

- **事实不精确**：正文 L51 写"Upload Part（part 不匹配返 404 NoSuchUpload）"。objectops 原文是 "Specified **upload-id** does not match any initiated upload on this object"，触发条件是 upload-id 不匹配，不是 part 不匹配。初审对这一点的措辞（"不匹配时返回"）本身也有歧义，这一处不全归责于作者。

关闭条件：

- 改为"upload-id 不匹配任何已发起的上传时返 404 NoSuchUpload"。

### B20-C16 — P2 / **OPEN**

已满足：

- "子集"已改为兼容模型，原文引用正确。
- Features 表中的 Partial（Replication 仅跨 zone）、canned ACL 差异、Unsupported Header Fields 都已写入。
- 扩展清单（Append、`allow-unordered`、Appendable）已列出。
- 写明"跨服务移植须逐 API 核对"。

剩余问题：

1. **关闭条件 2 未满足**：L58 写"本文用到的 multipart/版本化/条件读/列举状态以 Features 表为准"，又回到了"以表为准"的兜底写法。按原文核对，Features 表中：
   - Multipart Uploads 为 Supported；
   - Bucket Object Versions 为 Supported；
   - Get Object 和 Get Object Info (HEAD) 为 Supported；
   - 表中**没有**单列"条件读"或"列举对象（List Objects）"，只有 List Buckets。
2. **新登记来源带来的表述冲突**：新引用的 RGW 索引原文写 "compatible with a large subset of the Amazon S3 RESTful API"。正文的"既非子集也非超集"没有回应这一措辞。这与初审 C13 是同一类问题：所引来源的措辞与正文主张表面上相反。

关闭条件：

- L58 逐项写出上述状态，并对条件读和列举对象写"Features 表未单列"。
- 注明 RGW 索引写的是 "large subset"、S3 索引写的是 "basic data access model"。"非子集"是本库依据非标准扩展得出的推论，需要标为推论。

### B20-C17 — P2 / **CLOSED**

证据：

- 正文 L64–68 的节号与节名都与手册一致：§1.1.1、§34.10 原文"enforces POSIX coherency semantics … lock ping-pong"、术语表 Extent lock、§34.8（L 2.9）lockahead/noexpand、默认 stripe_count 1 与 stripe_size 1MB（§1.3.1 原文）、§19.3/§19.4。
- DoM 与 FLR 为 2.11、PFL 为 2.10，DoM 的 MDT 空间条件为 "5 percent or more"。
- glimpse 已删除。

### B20-C18 — P2 / **CLOSED**

证据：

- 正文 L77 写了 `GET /?usage`，并注明它不是性能计数器；radosgw-admin 单独记为 unknown。
- Lustre 写了 Jobstats（§12.2）、Ch.12 和 Ch.39 的入口，并注明只列入口。
- L78 的异常信号都给了出处：NoSuchUpload、409；Full OST §23.1、`BAD WRITE CHECKSUM` §23.5.1、§34.10。

非阻断：

- L78 写"最多重试语义以手册为准"，而手册原文明确是 "up to five times"，之后返回 I/O error。建议直接写出。
- L96 的待确认项"RGW 管理统计端点"建议改成"radosgw-admin / Admin Ops 统计"，以免和已写入的 `GET /?usage` 混淆。

### B20-C19 — P2 / **OPEN**

已满足：

- 三层定义已经先给出（L82）。
- Lustre wire checksum 引了 §23.5.1，并与应用层哈希分开。
- 已有区间写、第三个客户端读回、重叠写不作通过条件；文件大小覆盖条件（≥ stripe_size × stripe_count）＋getstripe＋读回哈希；`content-md5` 与读回哈希分开记录。
- 保持"未执行，留空"，没有标 reproduced。

剩余问题：

1. **负向用例写错了栏**：L86 失败判据栏写"Abort 后 List uploads 不再列出"。这是 Abort 用例的**预期**，不是失败判据。照字面读，"不再列出"反而会被判为失败。Abort 用例也没有自己的前置条件。
2. **Lustre 身份没有确定**：L82 写"FID 纳入与否由作者定，此处不定"。初审说的"由作者决定"指的是要作者在正文中作出选择，而本文作者就是做这个决定的人，"此处不定"等于身份定义仍然缺失。
3. **端到端哈希没有说明算法、计算者和比对时点**（初审 C19 的证据第 1 点）：L87–L89 只写"哈希一致"。
4. **versionId 的获取路径没有交代**：L86 预期"versionId 与清单一致"，但 §2 L50 写明 Squid 文档没有记载返回位置。同时，未启用版本化的 bucket 中，身份不含 versionId 时应当如何判定，也没有写。

关闭条件：

- 把 Abort 拆成单独一行：前置为发起 multipart 后 Abort；预期为 List Bucket Multipart Uploads 不再列出该 uploadId；失败判据为仍然列出。
- 选定 Lustre 身份，例如"路径＋布局（getstripe 输出）"，FID 纳入或不纳入二选一。
- 写明端到端哈希的算法、由谁计算（写入方生成清单、读回方重算）和比对时点。
- 写明 versionId 的取得方式。可以引已登记实现中的 `x-amz-version-id`，并标"实现侧，文档未记载"，或者写 unknown。未版本化的 bucket 以 bucket＋key＋哈希判定。

### B20-C20 — P3 / **CLOSED**

证据：

- 04 索引 L41 已改为"T04-03 已交付草稿，审阅中；主题验收留待 Batch 21"。
- 正文 verification notes 改为"最终核对范围（初审修订后待复核）"，所列章节与审阅者核对的范围一致。

非阻断：

- notes 中"v19.2.7 src/rgw 定位"随 C11 一并修正 commit 标注即可。
- 在 C11–C13 关闭前，`source_checked` 只代表"已有核对记录"，不代表复核已通过。

### B20-C21 — P3 / **OPEN**

已满足：

- 来源记录补了逐主张的定位表、unknown 清单和第二轮取证范围。
- 三项新登记（repo-v19.2.7、rgw-index-squid、latest-boundary）的 URL、revision、许可字段齐全。

剩余问题（与派单说明"rgw-s3/lustre 两项 revision 已更新"不符）：

- 登记 L5011 的 Lustre URL 仍是 `http://`，L5014 的 revision 没有补"2.x 滚动手册，含 2.5–2.17 标记"。
- 登记 L5000、L5008 未同步（同 C12、C13）。
- 来源记录**没有取证日期，也没有页面 SHA-256**。初审关闭条件明确要求补这两项。
- 来源记录 L3 仍写首轮取了"releases 页"，但登记中没有这一项。修订映射只写"releases 锚澄清（版本映射见实现锚）"，来源记录本身没有删除或说明。

关闭条件：

- 同步登记上述四处。
- 来源记录补取证日期与各页 SHA-256（可以直接用本报告和初审的一次源表）。
- releases 页要么登记，要么在来源记录中删除，或注明"未采用，由 v19.2.7 tag 取代"。

## 对照 acceptance 汇总

| acceptance | 判定 | 未关闭发现 |
|---|---|---|
| 1 版本化官方文档＋实现/测试/部署；不以 latest dev 证明稳定版 | 未满足：内容已补齐，但锚点标注和登记有误 | C11（commit SHA）、C12（登记未同步；LTS 锚无登记来源） |
| 2 对象语义与 Lustre 语义分开 | 基本满足 | C15（一处触发条件不精确） |
| 3 接口/选型/瓶颈/观察点/异常按实现列出；RGW ≠ AWS S3 | 部分满足 | C16（Features 状态未逐项写出；"large subset"措辞未回应） |
| 4 最小验证设计＋内容校验门槛；身份/ETag/校验和不混用 | 部分满足：正文 ETag 已纠正，但登记未同步；验证设计还有栏位和定义缺口 | C13（登记）、C19 |

## 结论

**T04-03 未通过定向复核：CLOSED 4（C14、C17、C18、C20），OPEN 7（C11、C12、C13、C15、C16、C19、C21）。三项 P1 均为 OPEN。** 本轮没有新增发现 ID。修订中出现的新事实错误都按原 ID 追记：

- tag 对象 SHA 被写成 commit，追记在 C11；
- LTS 锚没有登记来源，追记在 C12；
- NoSuchUpload 的触发条件写错，追记在 C15；
- RGW 索引写有 "large subset"，追记在 C16。

剩余工作量不大，大多是登记同步和措辞修正：

- C12、C13、C21 的主体是让登记文件真正落盘。作者应在下次提交前，用 `grep` 核对 L5000、L5008、L5011、L5014 的实际内容。
- C11、C15 各改一处。
- C16 补 Features 状态，并回应 "large subset"。
- C19 拆出 Abort 行，补齐身份、哈希和 versionId 的定义。

修订后需要按上述 ID 再做定向复核。本报告只覆盖编辑与来源层面，不构成硬件、部署或现场验证。
