# 第二十批 T04-03 第四次定向复核（作者第四轮修订后）

复核日期：2026-10-13（实际取证日）。正文 `updated_at` 与登记 `registered_at` 中的 `2026-10-14` 视为交付标签。

**结论：T04-03 未通过第四次定向复核。** 本轮复核 3 项：CLOSED 1 项（C12），OPEN 2 项（C16、C19）。加上此前已关闭的 C11、C13、C14、C15、C17、C18、C20、C21，B20-C11–C21 累计 CLOSED 9 项、OPEN 2 项。P1 已全部关闭，剩余两项均为 P2。

本轮有一处作者说明与一次源不符，按原 ID 追记在 C16：作者称 objectops 中 `if-match`/`if-none-match` 只出现在 Copy Object 的 `x-amz-copy-if-match` 上下文，GET Object 节只有 range/if-modified-since/if-unmodified-since。审阅者取证结果相反：GET Object 节和 Get Object Info（HEAD）节都列出全部五个请求头。作者来源记录登记的 objectops 前缀 `14f5689f` 与本轮所取字节完全一致，所以作者本地副本中同样有这两项。

审阅者独立于作者。审阅模型为 `claude-opus-5-5`，由用户本次明确指定。这不是既有的 `gpt-6.1-sol / xhigh` 批量审阅约定，也不改写该约定。推理等级等运行元数据没有可核验的记录，本报告不补造。

本轮只做只读取证，只写本报告。审阅者未改动作者正文、来源记录、修订映射、登记、索引或计划；未创建 bucket 或对象；未挂载 Lustre；未执行任何读写或 benchmark。修订映射中的作者自述不作为证据，以下判定均来自审阅者重新取证。模型审阅不构成硬件验证或现场验证。

## 输入（以 SHA-256 识别，均与任务给出的前缀一致）

| 输入 | SHA-256 |
|---|---|
| [T04-03 正文](../../knowledge/04-data-storage/object-and-parallel-storage.md)（99 行） | `9369b860ae496030ffc6424a4d6fab62117a8176f044c486cfd2109ada303721` |
| [修订映射](batch-20-review-fixes.md)（T04-03 第四轮节 L85–89） | `601bca5ed968f74912bb1a277124abea7899ce564ff2d310347b6bd306d0d299` |
| [前次复核报告](batch-20-t04-03-claude-recheck-3.md)（C12/C16/C19 剩余关闭条件的权威来源） | `75ab662043a1daf4baad0237677c9873155eef4279a65f25f15bc3194777b540` |
| [任务计划](../../plans/full-coverage-backlog.yaml)（T04-03 acceptance 4 条） | `f16309beadf5ae4f28d5fc7428a2348bea0cf08d155d57730a4d817cfcdd3e96`（与前几轮相同） |

`make check`：PASS（90 content entries / 407 sources）。该检查只校验结构和本地链接，不说明技术正确性。

## 一次源重取证（审阅者独立获取）

全部来源都用 `curl -sSL` 并保留默认 TLS 校验，只读获取，HTTP 状态均为 200。原文只放在临时目录 `/tmp/t0403r4/`，未入库。

| 来源 | SHA-256 / 结果 | 核对点 |
|---|---|---|
| Squid objectops | `14f5689f8f03a42761787b024a0558153519f30b585f9f1f0395e770f042e0ba`（与前几轮及作者来源记录 L3 一致） | GET Object 节请求头共五项：`range`、`if-modified-since`（"Gets only if modified since the timestamp."）、`if-unmodified-since`、`if-match`（"Gets only if object ETag matches ETag."）、`if-none-match`（"Gets only if object ETag doesn't match."）。Get Object Info（HEAD）节列出同样五项。Copy Object 节另有 `x-amz-copy-if-*` 四项，与 GET 节是两组不同的请求头 |
| Squid bucketops | `3f2a9d0db33f4910d7f85113723708e5ed4c59427d19efc3db451147fbf060ba`（一致） | GET Bucket 节："Returns a list of bucket objects."，参数 prefix/delimiter/marker/max-keys，`allow-unordered` 为 "Non-standard extension"；结果为 ListBucketResult/Contents |
| Squid S3 索引 | `e48b4d877b49a9f80582c7a85d2e0f09e44e553cb4b67caada1b73e03cd4557f`（一致） | Features 表与前次报告所列 24 行相同，没有 List Objects 行，也没有条件读行 |
| [wiki Lustre_Release_Information](https://wiki.lustre.org/Lustre_Release_Information) | `39049fbc…`（动态页，与前几轮都不同，符合预期） | "Current LTS Release Lustre 2.15.8 Released December 2, 2025"，与正文 L43 一致 |

取证限制：

1. HTML 用正则去标签解析，没有做版式级比对。
2. 本轮未重取 Lustre 手册、RGW 索引和 v19.2.7 tag；相关项已关闭，不在本轮范围内。
3. 审阅者无法读取作者的本地副本，只能比较作者登记的前缀。前缀 `14f5689f` 与本轮所取字节一致；本轮所取字节中 GET Object 节含 `if-match`/`if-none-match`。
4. 没有采集任何目标现场配置，也没有做任何实测。

## 逐项复核

### B20-C12 — P1 / **CLOSED**

证据：

- 正文 L43 现为"[Release Information](http://wiki.lustre.org/Lustre_Release_Information) 记 Current LTS Release 2.15.8，取证日 2026-10-13，该页动态变化"。取证日直接附在 wiki 引文上，满足前次唯一的关闭条件。
- 本轮重取 wiki，文字仍为 "Current LTS Release Lustre 2.15.8"，与正文一致。
- 前几轮已满足的条件（下载页旁注、`source_refs` L14 和 `evidence_refs` L28 含 `src.lustre.release-info-wiki`、登记 L5014 revision 指向该来源）本轮未退化。

非阻断：

- 正文 L43 和登记 L5061 的 wiki 链接仍是 `http://`，实际会重定向到 https，建议统一改为 https。

### B20-C16 — P2 / **OPEN**（仅剩条件读一处）

已满足：

- "Features 表实测行"已改为"Features 表声明状态"（L60），正文 grep "实测行"无命中。
- 对象列举改为"以 bucketops GET Bucket 节（返回对象列表，prefix/delimiter/marker/max-keys）为据，不从 List Buckets 推出"（L60），与审阅者取证一致。正文 grep "List Buckets 行"无命中。
- Features 表各行状态仍与一次源一致，"既非子集也非超集"仍标为本库推论并给出理由。

剩余问题：

1. **作者说明与一次源不符（按原 ID 追记）**：修订映射 L88 和本轮任务说明都称 GET Object 节只有 range/if-modified-since/if-unmodified-since，`if-match`/`if-none-match` 只出现在 Copy Object 上下文。一次源证据见上表：GET Object 节和 HEAD 节都列出五项，Copy Object 中的是另一组 `x-amz-copy-if-match`/`x-amz-copy-if-none-match`。作者登记的 objectops 前缀与本轮取证一致，所以差异不来自页面版本。正文 L60 列出的三项本身都存在于原文，不是错误事实；问题在于作者据此判断另两项不存在，这个判断是错的。
2. **条件读仍标为推论**：L60 写"条件读以 objectops GET Object 的 range/if-modified-since/if-unmodified-since 为据（表无单列，Get Object 行推论，标推论）"。同一句里先以 objectops 原文为据，又标为从 Features 表 Get Object 行推出。条件读在 objectops 中有原文请求头，不是推论。前次关闭条件要求"条件读见 objectops GET Object 请求头"，不再按推论处理。这一处没有满足。
3. **L56 与 L60 请求头集合不一致**：L56 写"GET/HEAD 支持 range 与 if-match/if-none-match 条件读"，L60 写 range/if-modified-since/if-unmodified-since。两处都只列了原文五项中的一部分，并且各列各的。读者会以为两处依据不同。

关闭条件：

- 删除 L60 的"（表无单列，Get Object 行推论，标推论）"，改为"Features 表未单列；见 objectops GET Object/HEAD 请求头原文"或等价写法。
- L56 与 L60 使用同一组请求头。可以写全五项（range、if-modified-since、if-unmodified-since、if-match、if-none-match），也可以在一处写全、另一处引用该处。

非阻断：

- 前次的两条非阻断建议（"large subset 指覆盖广度"加"本库解读"；L56 证据栏"同上两页"改为明确页名）仍未处理，可一并修改。

### B20-C19 — P2 / **OPEN**（仅剩 L88 判据）

已满足：

- **身份按版本化状态分支（L84）**：
  - Enabled：bucket＋key＋versionId，versionId 获取位置记 unknown。
  - 从未设置：bucket＋key＋内容哈希。
  - Suspended：新增对象 versionId 为 null，按无有效版本对待，身份同样加内容哈希。

  同段写明端到端哈希按本库约定为 SHA-256，由发布方写入清单。"内容哈希"因此等价于前次要求的"清单 SHA-256"。Suspended 的归类已写明，不再推给读者判断。这部分满足前次关闭条件第 1 条。
- "若可获得"一语已从正文删除（grep 无命中）。

剩余问题：

- **L88 的分支没有补 SHA-256 判据**：L88 的预期是"versionId 仅在版本化启用且可获得时与清单比对（……多数情形下该比对记 unknown 留空）"，失败判据是"可获得时不一致即失败；不可获得时该判据留空，不判失败"。前次关闭条件第 2 条要求"其他情况：读回 SHA-256 与清单不一致即失败"，本轮改成了留空。这样有两个后果：
  - 作者自己写明"多数情形"下 versionId 拿不到，所以本行在多数情形下没有失败判据。另一项预期"对象可见"也没有写不可见时判失败。
  - L84 已把 Suspended 和从未设置状态的身份定义为 bucket＋key＋SHA-256，L88 却不用这个身份做判定。§5 的三层定义与场景表脱节。

  下一行"跨客户端读回"有哈希判据，但它的前置是"发布完成"，判断的是另一件事，不能代替发布行本身的判据。本节标题要求"可判定预期"，这一行目前仍不满足。

关闭条件：

- L88 的预期和失败判据按 L84 的同一分支改写：
  - Enabled 且能获得 versionId：versionId 与清单不一致即失败；
  - 其他情况（Suspended、从未设置，或 versionId 不可获得）：读回 SHA-256 与清单不一致即失败。
- 补"对象不可见即失败"，或把"对象可见"并入上述判据。

## 对照 acceptance 汇总

| acceptance | 判定 | 未关闭发现 |
|---|---|---|
| 1 版本化官方文档＋实现/测试/部署；不以 latest dev 证明稳定版 | 满足：LTS 锚引 wiki 并附取证日 | — |
| 2 对象语义与 Lustre 语义分开 | 满足 | — |
| 3 接口/选型/瓶颈/观察点/异常按实现列出；RGW ≠ AWS S3 | 基本满足：对象列举依据已改正，"实测"已改；条件读仍标推论，L56/L60 请求头集合不一致 | C16 |
| 4 最小验证设计＋内容校验门槛；身份/ETag/校验和不混用 | 基本满足：身份已按三态分支并含 SHA-256；对象发布行在 versionId 不可获得时没有失败判据 | C19 |

## 结论

**T04-03 未通过第四次定向复核：本轮 3 项中 CLOSED 1 项（C12），OPEN 2 项（C16、C19）。B20-C11–C21 累计 CLOSED 9 项、OPEN 2 项，P1 已全部关闭。** 本轮没有新增发现 ID。作者关于 GET Object 请求头的说明与一次源不符，按原 ID 追记在 C16。

剩余修订只涉及正文三处：

- C16：L60 删除"Get Object 行推论，标推论"，改指 objectops GET Object/HEAD 请求头原文；L56 与 L60 的请求头集合统一。
- C19：L88 在 versionId 不可获得时以读回 SHA-256 判定，并补"不可见即失败"。

修订后需要按 C16、C19 再做定向复核。作者自查时请 `grep` 正文中的"标推论""判据留空"，并在 objectops GET Object 节核对 `if-match` 一行。本报告只覆盖编辑与来源层面，不构成硬件、部署或现场验证。
