# 第二十批 T04-03 第二次定向复核（作者第二轮修订后）

复核日期：2026-10-13（实际取证日）。正文 `updated_at` 与登记 `registered_at` 中的 `2026-10-14` 视为交付标签。

**结论：T04-03 未通过第二次定向复核。** 本轮复核 7 项，CLOSED 3 项（C11、C13、C15），OPEN 4 项（C12、C16、C19、C21）。连同前次已关闭的 C14、C17、C18、C20，B20-C11–C21 累计 CLOSED 7、OPEN 4。P1 中仍有 C12 未关闭。

本轮登记同步已真实落盘：rgw-s3 revision、lustre revision 及 LTS 锚、repo commit `9ec952b9`、ETag 措辞、wiki LTS 登记均可在工作区 `sources/registry.yaml` 中逐字看到，前次"未落盘"的问题已解决。剩余问题分为四类：

1. 正文没有改引已登记的 LTS 来源（C12）。
2. Features 表中没有的"列举"被写成 Supported（C16）。
3. versionId 的取得途径写成了 Squid 文档并未记载的位置（C19）。
4. Lustre 登记 URL 仍为 `http://`（C21）。

审阅者角色独立于作者。审阅模型为 `claude-opus-5-5`，由用户本次明确要求使用。这不是既有的 `gpt-6.1-sol / xhigh` 批量审阅约定，也不改写该约定；推理等级等运行元数据没有可核验记录，不补造。本轮只做只读取证，只写本报告：未改作者正文、来源记录、修订映射、登记、索引或计划，未创建 bucket 或对象，未挂载 Lustre，未执行任何读写或 benchmark。作者自述已独立复核全部取证点，本报告不采信该自述，以下各项均为审阅者重新取证的结果。模型审阅不构成硬件或现场验证。

## 输入（以 SHA-256 识别）

| 输入 | SHA-256 |
|---|---|
| [T04-03 正文](../../knowledge/04-data-storage/object-and-parallel-storage.md)（96 行） | `731de4b598c396d34f372a8e1947b74ba880c70524ca189b75245166896deb40` |
| [作者来源记录](batch-20-t04-03-sources.md)（16 行） | `0a08b1b0e8653ed01c7ff5f562d253f98b5b119f411dc5050c8f76afb74b1516` |
| [修订映射](batch-20-review-fixes.md)（T04-03 第二轮节 L67–76） | `19300e48b5accf31a032780c9c0cc98e1984bc9f1151a6730c9ab07ba64011c4` |
| [前次复核报告](batch-20-t04-03-claude-recheck.md) | `6855594d125b69813fa19c8592313bd96e87a39895f5b9fe962bb9d3709fd271` |
| [任务计划](../../plans/full-coverage-backlog.yaml)（T04-03 acceptance 4 条，L5139–5143） | `f16309beadf5ae4f28d5fc7428a2348bea0cf08d155d57730a4d817cfcdd3e96`（与前两轮相同） |
| [来源登记](../../sources/registry.yaml)（407 项；T04-03 相关 L4995–5069） | `9d965f8539f9c69ec693e067154b39846052e287dfa8a43b82746bd28c9ab0d9` |

`make check`：PASS（90 content entries / 407 sources）。它只校验结构与本地链接，不说明技术正确性。

## 一次源重取证（审阅者独立获取）

全部用 `curl -L` 默认 TLS 校验只读获取，HTTP 均为 200。原文只存放在临时目录 `/tmp/t0403r2/`，未入库。

| 来源 | SHA-256 / 结果 | 核对点 |
|---|---|---|
| Squid S3 索引 | `e48b4d877b49a9f80582c7a85d2e0f09e44e553cb4b67caada1b73e03cd4557f`（与前两轮一致） | Features 表全行：List/Delete/Create Bucket、Bucket Lifecycle、Bucket Replication **Partial**（"Permitted only across zones"）、Policy、Bucket Website、Bucket ACLs、Bucket Location、Bucket Notification、Bucket Object Versions、Get Bucket Info (HEAD)、Bucket Request Payment、Put/Delete/Get Object、Object ACLs、Get Object Info (HEAD)、POST Object、Copy Object、Multipart Uploads、Object Tagging、Bucket Tagging、Storage Class。**表中没有 List Objects / GET Bucket 行，也没有条件读行**（→ C16）。兼容措辞为 "compatible with the basic data access model of the Amazon S3 API" |
| Squid bucketops | `3f2a9d0db33f4910d7f85113723708e5ed4c59427d19efc3db451147fbf060ba`（一致） | GET 子资源只有 `max-keys`/`location`/`acl`/`uploads`/`object-lock`/`notification` 等，**没有 `?versions` 列举**（→ C19） |
| Squid objectops | `14f5689f8f03a42761787b024a0558153519f30b585f9f1f0395e770f042e0ba`（一致） | Complete Multipart 响应实体只有 `Location`/`Bucket`/`Key`/`ETag`，**没有 versionId**（→ C19）；`versionId` 只出现在 retention/legal-hold 的查询参数中；404 NoSuchUpload 原文为 "Specified upload-id does not match any initiated upload on this object"；Abort 只有语法 `DELETE /{bucket}/{object}?uploadId=` |
| Squid RGW 索引 | `695cd90d5fc04a76c9de3b9ba15a3ef205562acc084d11b7fdecf5afe848cbea`（一致） | "compatible with a large subset of the Amazon S3 RESTful API" |
| ceph/ceph tag v19.2.7 | `git ls-remote`：`refs/tags/v19.2.7` → `c24c670729945982079397f922db1a750ddc16f4`；`refs/tags/v19.2.7^{}` → `9ec952b9f9668e9fa97e29a4c2b51e951674df2a` | 与正文 L38、登记 L5025 一致 |
| Lustre 手册 | `63b09d0650de3491eee9c976dff1246706dc6496bc996c139fdebdf7fc4a0d8c`（一致） | 本轮只确认字节未变，未重读节文本（节号核对见前两轮） |
| [wiki Lustre_Release_Information](https://wiki.lustre.org/Lustre_Release_Information) | 两次获取 SHA 不同（`fc8bf385…`、`cfa400f7…`），**页面是动态生成的**，作者记录的 `42d1b0e6` 无法复现 | "Current LTS Release Lustre 2.15.8 Released December 2, 2025"；"Current Major Release Lustre 2.17.0 Released December 29, 2025"；`http://` 重定向到 `https://` |
| [lustre.org/download](https://www.lustre.org/download/) | `cc89cd99…`（未登记） | 仅用于确认正文 L41 所引页面；前次已核对该页无"LTS"字样 |

取证限制：

1. HTML 用正则去标签，没有做版式级比对。
2. RGW 源码本轮未重读，只重核 tag 解引用。
3. Lustre 手册只核对字节一致。
4. 没有采集任何目标现场配置，也没有做任何实测。

## 逐项复核

### B20-C11 — P1 / **CLOSED**

证据：

- 正文 L38 写"实现锚 v19.2.7 tag（所指 commit 9ec952b9；tag 对象 c24c6707 非 commit）"。
- 登记 L5025 写"tag 对象 c24c6707，所指 commit 9ec952b9，经 ls-remote 两行核对"。
- 两处都与审阅者 `ls-remote` 的两行输出一致。

非阻断（前次遗留，未采纳，不阻断）：

- L40 仍把守护进程归入"未逐页核对 unknown"。RGW 索引原文已写明 radosgw 守护进程和"不使用 Ceph MDS"，可以直接写出。

### B20-C12 — P1 / **OPEN**

已满足：

- 登记 L5000 的 rgw-s3 revision 已写"分支文档（取证日 2026-10-13），点版本 unknown"。
- 登记 L5014 的 lustre revision 已写"2.x 滚动手册，含 2.5–2.17 标记；稳定锚 LTS 2.15.x（见 src.lustre.release-info-wiki）"。
- L5008 notes 已删除"latest/dev 文档（已登记 scrubbing-latest）"。
- 新登记 `src.lustre.release-info-wiki`（L5059），它写明的 "Current LTS Release 2.15.8" 与审阅者取证一致。

剩余问题：

- **正文没有改引**：正文 L41 仍写"稳定锚 LTS 2.15.x（下载页列 2.15.8）"，没有链接 wiki 页。`source_refs`（L8–13）中也没有 `src.lustre.release-info-wiki`。结果是：正文的 LTS 主张仍指向一个不写 LTS 的页面，而写明 LTS 的来源只出现在登记里，正文不可追溯。修订映射 C12 写"LTS 2.15.8 登记 mapping"，只做了登记一侧。

关闭条件（即前次关闭条件第 2 条的后半句）：

- 正文 L41 改为引用 wiki 页（链接，并注明取证日）。
- 把 `src.lustre.release-info-wiki` 加入 `source_refs`。
- "下载页列 2.15.8"要么删除，要么改写为与 LTS 判定无关的旁注。

非阻断：

- wiki 页是动态页面，SHA 每次获取都不同（见一次源表）。建议登记 revision 注明"动态页面，以取证日所见文字为准，SHA 不可复现"。

### B20-C13 — P1 / **CLOSED**

证据：

- 登记 L5008 notes 已写明 bucketops 把 List 结果 ETag 写为 "An MD-5 hash of the object"，并说明本库不把它当作内容哈希使用。这满足初审 C13 关闭条件的第 3 条（同步登记 notes，说明 ETag 条目的实际措辞）。
- 正文 L52、L53 的状态与前次复核相同，仍然满足。

非阻断：

- 登记 L5000 revision 仍写"核对 … versionId … 条目"，可以补一句"versionId 仅作为 retention/legal-hold 的查询参数出现"。这句话出现在前次报告的剩余问题叙述中，但不在初审关闭条件内，不阻断。

### B20-C15 — P2 / **CLOSED**

证据：

- 正文 L51 已改为"upload-id 不匹配返 404 NoSuchUpload"，与 objectops 原文 "Specified upload-id does not match any initiated upload on this object" 一致。
- L78 典型异常中的 NoSuchUpload（404）没有附带错误的触发条件。

### B20-C16 — P2 / **OPEN**

已满足：

- L58 已逐项列出 Features 表状态，包括 Replication Partial（仅跨 zone）、canned ACL 差异和 Unsupported Header Fields 表。经核对，这些与原文一致。
- L58 已经回应 RGW 索引页的 "large subset" 措辞。

剩余问题：

1. **新事实错误（按原 ID 追记）**：L58 写"列举（Supported）状态以 Features 表为准"。Features 表**没有** List Objects / GET Bucket 行，只有 List Buckets（列出 bucket，不是列出对象）。前次关闭条件明确要求对列举对象写"Features 表未单列"。
2. **把推导写成了表中状态**：L58 写"条件读（Get Object Supported）"。这是用 Get Object 行推出条件读，表中并没有条件读行。应写"Features 表未单列（Get Object 为 Supported；条件读参数见 objectops）"，或者明确标为推论。
3. **"以 Features 表为准"的兜底写法仍在**：前次关闭条件第 1 条就是要求去掉这种写法，逐项写明。
4. **"非子集"仍未标为推论**：L58 把 "large subset" 解释为"覆盖广度"，把"非子集"解释为"集合关系"。这是作者的解读，原文只写了 "large subset"。另外，"既非子集也非超集"现在只出现在反驳语句中，正文其他位置不再有这一主张。前次关闭条件要求注明"非子集"是本库依据非标准扩展（`allow-unordered`、Append）得出的推论。
5. **措辞**：L58 写"Features 表实测状态"。该表是官方的支持声明，不是实测结果。建议改为"声明状态"。

关闭条件：

- 列举改为"Features 表未单列（仅有 List Buckets）"，条件读改为"Features 表未单列"并附 objectops 位置。
- 删除"以 Features 表为准"。
- 加一句明确的推论标注，例如："RGW 文档自述为 'large subset'；本库据 RGW 独有扩展推论其接口集合不是 AWS S3 的严格子集（推论，非原文）"。
- "实测状态"改为"声明状态"。

### B20-C19 — P2 / **OPEN**

已满足：

- Lustre 身份已选定为"路径＋getstripe 布局，不含 FID"，并写明这是本库设计决定及其理由（L82）。
- 端到端哈希已写明算法（SHA-256）、计算者（发布方发布前写入清单，读回方重算）和比对方式（L82）。
- Abort 已移到"预期"栏，前次指出的"预期写进失败判据栏"的错误已消除。

剩余问题：

1. **新事实错误（按原 ID 追记）**：L82 写"versionId 取自 Complete 响应/版本化列举"。审阅者核对 Squid 文档：
   - Complete Multipart 的响应实体只有 `Location`/`Bucket`/`Key`/`ETag`，没有 versionId；
   - bucketops 没有 `?versions` 列举。

   这一句与正文自己的 L50（"无 `x-amz-version-id` 响应头记载，无 ListObjectVersions 操作"）互相矛盾。后面的"Squid 文档未给出响应头位置则记 unknown"也不能补救，因为前半句已经把两处 Squid 文档没有记载的位置写成了来源。
2. **未版本化 bucket 的判定仍缺**：L82 的身份定义固定包含 versionId；L86 的失败判据"versionId 不一致即失败"也没有区分 bucket 是否启用了版本化。前次关闭条件要求写明：未版本化（或 Suspended，version ID 为 null）的 bucket 以 bucket＋key＋哈希判定。
3. **Abort 没有失败判据，也没有单独的前置条件**：L86 的失败判据栏只写"versionId 不一致即失败"，没有写 Abort 的失败判据（Abort 后 List Bucket Multipart Uploads 仍列出该 uploadId）。前置栏只写"multipart Complete"，没有写 Abort 用例需要的"发起 multipart 后 Abort"。前次关闭条件要求单独成行，修订映射写的"Abort 负向用例改预期栏"只完成了一半。

关闭条件：

- versionId 的取得方式二选一：
  - 引已登记的 `src.ceph.repo-v19.2.7` 中 `rgw_rest_s3.cc` 输出的 `x-amz-version-id` 响应头，并标"实现侧，Squid 文档未记载"；
  - 或者直接写 unknown。

  删除"Complete 响应/版本化列举"的表述。
- 补写未版本化或 Suspended bucket 的身份定义（bucket＋key＋SHA-256），并把 L86 的失败判据改成按版本化状态区分。
- Abort 单独成行：前置为"发起 multipart 后 Abort"，预期为"List Bucket Multipart Uploads 不再列出该 uploadId"，失败判据为"仍列出"。

### B20-C21 — P3 / **OPEN**

已满足：

- 来源记录 L3 已补取证日期（2026-10-13）和各页 SHA-256 前缀，前缀与本报告一次源表中的全长 SHA 一致（wiki 除外，见下）。
- releases 页已注明"仅浏览版本映射，未登记"，满足前次关闭条件第 3 条中的"注明"选项。
- 登记 L5000、L5008、L5014 已同步（见 C12、C13）。

剩余问题：

- **登记 L5011 的 Lustre 手册 URL 仍是 `http://doc.lustre.org/lustre_manual.xhtml`**。前次关闭条件第 1 条把它列为四处之一（初审 C21 也要求改为 https），修订映射 C21 首轮也自称"Lustre https"，但实际仍未修改。正文 L41 用的是 https，与登记不一致。
- 新登记 `src.lustre.release-info-wiki`（L5061）同样用 `http://`。该地址会重定向到 https，建议一并统一。

关闭条件：

- 登记 L5011 改为 `https://doc.lustre.org/lustre_manual.xhtml`（建议 L5061 也改为 https）。

非阻断：

- 来源记录说"全文见复核报告一次源表"，但 wiki 的 `42d1b0e6` 不在任何一份复核报告里，审阅者也无法复现（动态页面）。建议在记录中注明这一点。其余各页的全长 SHA 见本报告一次源表。
- unknown 清单第 4、6 项（"RGW 管理统计端点"、"版本化启用细节"）前次已作为非阻断提出，仍可细化。

## 对照 acceptance 汇总

| acceptance | 判定 | 未关闭发现 |
|---|---|---|
| 1 版本化官方文档＋实现/测试/部署；不以 latest dev 证明稳定版 | 基本满足：登记已落盘，实现锚正确；正文 LTS 锚仍指向不写 LTS 的页面 | C12（正文改引）、C21（URL https） |
| 2 对象语义与 Lustre 语义分开 | 满足 | — |
| 3 接口/选型/瓶颈/观察点/异常按实现列出；RGW ≠ AWS S3 | 部分满足 | C16（列举/条件读被写成表中状态；推论未标注） |
| 4 最小验证设计＋内容校验门槛；身份/ETag/校验和不混用 | 部分满足：ETag/校验和已分开；versionId 来源写错，未版本化身份和 Abort 判据仍缺 | C19 |

## 结论

**T04-03 未通过第二次定向复核：本轮 7 项中 CLOSED 3（C11、C13、C15），OPEN 4（C12、C16、C19、C21）。累计 B20-C11–C21：CLOSED 7、OPEN 4，P1 中 C12 仍为 OPEN。** 本轮没有新增发现 ID，新事实错误按原 ID 追记：

- "列举（Supported）"在 Features 表中并不存在，追记在 C16；
- "versionId 取自 Complete 响应/版本化列举"在 Squid 文档中没有依据，并与正文 L50 矛盾，追记在 C19。

剩余修订都是局部改动：

- C12：正文 L41 改引 wiki，`source_refs` 补 ID；
- C16：L58 改三处措辞，加一句推论标注；
- C19：改写 L82 的 versionId 句，补未版本化身份，Abort 拆成单独一行；
- C21：登记 L5011 URL 改为 https。

修订后需要按 C12、C16、C19、C21 再做定向复核。作者自查时应同时 `grep` 正文和登记，确认两侧都已改动；本轮 C12 和 C21 都是一侧改了、另一侧没改。本报告只覆盖编辑与来源层面，不构成硬件、部署或现场验证。
