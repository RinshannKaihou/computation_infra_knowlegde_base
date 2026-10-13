# 第二十批 T04-03 第三次定向复核（作者第三轮修订后）

复核日期：2026-10-13（实际取证日）。正文 `updated_at` 与登记 `registered_at` 中的 `2026-10-14` 视为交付标签。

**结论：T04-03 未通过第三次定向复核。** 本轮复核 4 项：CLOSED 1 项（C21），OPEN 3 项（C12、C16、C19）。加上此前已关闭的 C11、C13、C14、C15、C17、C18、C20，B20-C11–C21 累计 CLOSED 8 项、OPEN 3 项。P1 中的 C12 仍为 OPEN，但只差在正文补一个取证日。

本轮在实质上有进展：

- 正文已链接 wiki 页，并把它加入 `source_refs` 和 `evidence_refs`。
- 正文已删除"以 Features 表为准"和"versionId 取自 Complete 响应/版本化列举"。
- Abort 已单独成行。
- 登记中的 Lustre 手册 URL 已改为 https。

剩余问题都是小范围的措辞或判据修改，其中一处是新的推理错误：正文把"对象列举"说成从 List Buckets 行推出。这一处按原 ID 追记在 C16。

审阅者独立于作者。审阅模型为 `claude-opus-5-5`，由用户本次明确指定。这不是既有的 `gpt-6.1-sol / xhigh` 批量审阅约定，也不改写该约定。推理等级等运行元数据没有可核验的记录，本报告不补造。

本轮只做只读取证，只写本报告。审阅者未改动作者正文、来源记录、修订映射、登记、索引或计划；未创建 bucket 或对象；未挂载 Lustre；未执行任何读写或 benchmark。修订映射中的作者自述不作为证据，以下判定均来自审阅者重新取证。模型审阅不构成硬件验证或现场验证。

## 输入（以 SHA-256 识别，均与任务给出的前缀一致）

| 输入 | SHA-256 |
|---|---|
| [T04-03 正文](../../knowledge/04-data-storage/object-and-parallel-storage.md)（99 行） | `2b2a6bd4d2b8a95e07b55318a704976a0530fed0ced5c53cae89468979295f4a` |
| [作者来源记录](batch-20-t04-03-sources.md)（16 行） | `b30c2bebd30d5f4ba8ad64a8b2b5d189d104f30f77e8abe296dc7d28cff35376` |
| [修订映射](batch-20-review-fixes.md)（T04-03 第三轮节 L78–83） | `cbcc544add2cbe1b9ec8627f60b3d91c6a5c9b01e818a27a1c56eff6a7274397` |
| [前次复核报告](batch-20-t04-03-claude-recheck-2.md)（剩余关闭条件的权威来源） | `1875dde556c3ac8d609794d8392608d3b48a9dbf52da54cb0772fc8c6a9f2deb` |
| [任务计划](../../plans/full-coverage-backlog.yaml)（T04-03 acceptance 4 条） | `f16309beadf5ae4f28d5fc7428a2348bea0cf08d155d57730a4d817cfcdd3e96`（与前三轮相同） |
| [来源登记](../../sources/registry.yaml)（407 项；T04-03 相关 L4995–5069） | `26cd1d3a7643a0b74a79782e29fcec6ceb7d5bbd6478eb3238ab6abee5919f29` |

`make check`：PASS（90 content entries / 407 sources）。该检查只校验结构和本地链接，不说明技术正确性。

## 一次源重取证（审阅者独立获取）

全部来源都用 `curl -sSL` 并保留默认 TLS 校验，只读获取，HTTP 状态均为 200。原文只放在临时目录 `/tmp/t0403r3/`，未入库。

| 来源 | SHA-256 / 结果 | 核对点 |
|---|---|---|
| Squid S3 索引 | `e48b4d877b49a9f80582c7a85d2e0f09e44e553cb4b67caada1b73e03cd4557f`（与前三轮一致） | 按 `<tr>` 解析 Features 表，共 24 行，具体见下文 C16。表中没有 List Objects / GET Bucket 行，也没有条件读行 |
| Squid bucketops | `3f2a9d0db33f4910d7f85113723708e5ed4c59427d19efc3db451147fbf060ba`（一致） | 不含 `?versions`、`ListObjectVersions`、`x-amz-version-id` 三个字串 |
| Squid objectops | `14f5689f8f03a42761787b024a0558153519f30b585f9f1f0395e770f042e0ba`（一致） | 不含 `x-amz-version-id`；GET Object 请求头有 `range`、`if-match`（"Gets only if object ETag matches ETag"）、`if-none-match` |
| Lustre 手册 | `63b09d0650de3491eee9c976dff1246706dc6496bc996c139fdebdf7fc4a0d8c`（一致） | 只核对字节一致 |
| [wiki Lustre_Release_Information](https://wiki.lustre.org/Lustre_Release_Information) | 两次获取：https 直连得到 `616b7abb…`，http 经重定向得到 `8e32fd1c…`。两次 SHA 不同，与前次所得也不同 | "Current LTS Release Lustre 2.15.8 Released December 2, 2025"，与正文 L43、登记 L5064 一致；再次确认页面为动态生成，SHA 不可复现 |

取证限制：

1. HTML 用正则去标签解析，没有做版式级比对。
2. 本轮未重读 RGW 源码，也未重新 `ls-remote` 核对 tag；C11 已关闭，不在本轮范围内。
3. Lustre 手册只核对字节一致。
4. 没有采集任何目标现场配置，也没有做任何实测。

## 逐项复核

### B20-C12 — P1 / **OPEN**（仅差取证日）

已满足：

- 正文 L43 已改为链接 [Release Information](http://wiki.lustre.org/Lustre_Release_Information)，并写明"记 Current LTS Release 2.15.8"，与审阅者取证一致。
- 下载页改写为旁注："下载页仅列版本号，无 LTS 字样"。它不再承担 LTS 判定，满足前次关闭条件第 3 条。
- `source_refs`（L14）和 `evidence_refs`（L28）都已加入 `src.lustre.release-info-wiki`，满足前次关闭条件第 2 条。
- 登记 L5014 的 revision 指向 `src.lustre.release-info-wiki`，正文和登记两侧已一致。

剩余问题：

- 前次关闭条件第 1 条要求引用 wiki 页时"链接，并注明取证日"。正文 L43 只给了链接，没有取证日。L40 的"取证日 2026-10-13"只修饰 Ceph 行。wiki 页是动态页面，"Current LTS Release"会随时间变化，所以必须写明取证日，读者才能判断"2.15.8"在什么时间成立。

关闭条件：

- 在正文 L43 的 wiki 引用处补"（取证日 2026-10-13）"或等价写法。

非阻断：

- L43 的链接与登记 L5061 都仍是 `http://`，实际会重定向到 https，建议一并改为 https（见 C21）。

### B20-C16 — P2 / **OPEN**

审阅者解析得到的 Features 表全部 24 行（"Feature | Status | Remarks"）：

- List Buckets | Supported
- Delete Bucket | Supported
- Create Bucket | Supported | Different set of canned ACLs
- Bucket Lifecycle | Supported
- Bucket Replication | Partial | Permitted only across zones
- Policy (Buckets, Objects) | Supported
- Bucket Website | Supported
- Bucket ACLs (Get, Put) | Supported | Different set of canned ACLs
- Bucket Location | Supported
- Bucket Notification | Supported
- Bucket Object Versions | Supported
- Get Bucket Info (HEAD) | Supported
- Bucket Request Payment | Supported
- Put Object | Supported
- Delete Object | Supported
- Get Object | Supported
- Object ACLs (Get, Put) | Supported
- Get Object Info (HEAD) | Supported
- POST Object | Supported
- Copy Object | Supported
- Multipart Uploads | Supported
- Object Tagging | Supported
- Bucket Tagging | Supported
- Storage Class | Supported

已满足：

- 正文 L60 列出的各行状态都与上表一致，包括 Replication 为 Partial（仅跨 zone）和 canned ACL 差异。正文没有虚构表中不存在的行，也没有写错状态。
- "以 Features 表为准"已删除（全文 grep 无命中）。
- "既非子集也非超集"已标为"本库推论"并给出理由（RGW 独有扩展），满足前次的推论标注条件。
- 正文写明"表中无 List Objects/条件读单列"，满足"Features 表未单列"这一要求。

剩余问题：

1. **新推理错误（按原 ID 追记）**：L60 写"条件读/对象列举为本库从 Get Object/List Buckets 行的推论"。按并列顺序，"对象列举"对应的是"List Buckets 行"。List Buckets 是列出 bucket 的服务级操作，不能推出对象级列举是否受支持；前次报告已明确指出这一点（"列出 bucket，不是列出对象"）。对象列举在 Squid 文档中的实际依据是 bucketops 的 GET Bucket 节，正文 L56 也已引用该节（prefix/delimiter/marker/max-keys）。所以这里不应写成从 Features 表推出的推论，而应写成"Features 表未单列；操作见 bucketops GET Bucket"。
2. **"实测"仍未改**：L60 仍写"Features 表实测行"。前次关闭条件第 4 条要求把"实测状态"改为"声明状态"。修订映射只把"精确行"标为已处理，没有处理这处措辞。Features 表是官方支持声明，写作"实测"会让读者误以为本库做过测试。
3. **条件读没有附 objectops 位置**：L60 只说条件读是从 Get Object 行推出的推论，没有指向 objectops。审阅者核实 objectops 的 GET Object 请求头确有 `if-match` 和 `if-none-match`，所以条件读有直接的文档依据，不必当作推论。L56 的证据栏写"同上两页"，但上一行 L55 只列了 objectops 一页，指代不清。

关闭条件：

- 把 L60 的推论句改为："Features 表未单列对象列举与条件读（仅有 List Buckets，指列出 bucket）；对象列举见 bucketops GET Bucket，条件读见 objectops GET Object 请求头 `if-match`/`if-none-match`"。改后，"从 List Buckets 行推论"这一表述应不再出现。
- 把"Features 表实测行"改为"Features 表声明状态"或等价写法。

非阻断：

- "'large subset' 指覆盖广度"仍是作者的解读，可加"（本库解读）"。
- 建议把 L56 证据栏的"同上两页"改为明确页名。

### B20-C19 — P2 / **OPEN**

已满足：

- **versionId 的来源**：L84 改为"versionId 获取位置 Squid 文档未给出——Complete 响应仅 Location/Bucket/Key/ETag，bucketops 无版本列举，记 unknown"。这与审阅者取证一致：两页都没有 `x-amz-version-id` 或 `?versions`。"Complete 响应/版本化列举"的错误表述已删除，与 L52 也不再矛盾。满足前次关闭条件第 1 条的"直接写 unknown"选项。
- **Abort 单独成行**：L89 的前置是"该 upload-id 在 List uploads 可见"，预期是"Abort 后 List uploads 不再列出该上传"，失败判据是"仍列出即失败"。三栏齐全，满足前次关闭条件第 3 条。

剩余问题：

1. **未版本化身份没有按关闭条件写全**：L84 写"未启用版本化的 bucket 身份为 bucket＋key（以版本化三态为准）"，有两处不足。
   - 前次关闭条件要求写 bucket＋key＋SHA-256。仅用 bucket＋key 无法区分同一 key 被覆盖前后的内容。
   - Suspended 状态（新对象 version ID 为 null，见 L51）属于"未启用版本化"还是"Enabled"，没有写明。"以版本化三态为准"只是把判断推回给读者。
2. **对象发布行没有按版本化状态区分**：L88 的预期是"versionId（若可获得）与清单一致"，失败判据是"versionId 不一致即失败"。前次关闭条件第 2 条要求按版本化状态区分这一栏，但本轮没有修改。再加上 L84 已把 versionId 的获取方式记为 unknown，这一行在任何版本化状态下都可能缺少可判定的失败判据。本节标题要求"可判定预期"，这一行目前不满足。

关闭条件：

- L84 把身份写成分支：
  - Enabled：bucket＋key＋versionId（获取方式 unknown）；
  - Suspended 或从未设置：bucket＋key＋清单 SHA-256。
- L88 的预期和失败判据按同一分支写：
  - Enabled 且能获得 versionId：versionId 与清单不一致即失败；
  - 其他情况：读回 SHA-256 与清单不一致即失败。

### B20-C21 — P3 / **CLOSED**

证据：

- 登记 L5011 已改为 `url: https://doc.lustre.org/lustre_manual.xhtml`，与正文 L43–44 的手册链接一致，满足前次唯一的关闭条件。
- 来源记录 L3 已写明"wiki 为动态页，作者快照前缀仅作当时记录，不可复现"，采纳了前次的非阻断建议。本轮取证再次证实该页 SHA 每次都不同。
- 来源记录 L3 保留了"releases 页仅浏览版本映射，未登记"。

非阻断：

- 登记 L5061（`src.lustre.release-info-wiki`）和正文 L43 的 wiki 链接仍是 `http://`，可以统一改为 https。
- 登记 L5064 的 revision 写"wiki 快照实开"，但没有注明"动态页面，以取证日所见文字为准"，可以补上。
- unknown 清单第 4、6 项仍可细化（前次已提出）。

## 对照 acceptance 汇总

| acceptance | 判定 | 未关闭发现 |
|---|---|---|
| 1 版本化官方文档＋实现/测试/部署；不以 latest dev 证明稳定版 | 基本满足：LTS 锚已改引 wiki，两侧已一致；只差取证日 | C12 |
| 2 对象语义与 Lustre 语义分开 | 满足 | — |
| 3 接口/选型/瓶颈/观察点/异常按实现列出；RGW ≠ AWS S3 | 基本满足：Features 表各行准确，推论已标注；仍有"从 List Buckets 推论对象列举"和"实测"两处措辞问题 | C16 |
| 4 最小验证设计＋内容校验门槛；身份/ETag/校验和不混用 | 部分满足：versionId 已记 unknown，Abort 已单独成行；未版本化身份缺 SHA-256 且未写 Suspended，对象发布行没有可判定的分支判据 | C19 |

## 结论

**T04-03 未通过第三次定向复核：本轮 4 项中 CLOSED 1 项（C21），OPEN 3 项（C12、C16、C19）。B20-C11–C21 累计 CLOSED 8 项、OPEN 3 项，P1 中 C12 仍为 OPEN。** 本轮没有新增发现 ID。新推理错误"对象列举为本库从 List Buckets 行的推论"按原 ID 追记在 C16。

剩余修订只涉及正文三处：

- C12：L43 的 wiki 引用补取证日。
- C16：L60 改写推论句，指向 bucketops GET Bucket 和 objectops `if-match`；"实测行"改为"声明状态"。
- C19：L84 的身份按版本化状态分支，并补 SHA-256；L88 的预期和失败判据按同一分支改写。

修订后需要按 C12、C16、C19 再做定向复核。作者自查时请 `grep` 正文中的"实测行""List Buckets 行""若可获得"，确认这些表述都已处理。本报告只覆盖编辑与来源层面，不构成硬件、部署或现场验证。
