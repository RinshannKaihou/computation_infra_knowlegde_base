# 第二十批 T04-03 第五次定向复核（作者第五轮修订后）

复核日期：2026-10-13（实际取证日）。正文 `updated_at` 与登记 `registered_at` 中的 `2026-10-14` 视为交付标签。

**结论：T04-03 通过第五次定向复核。** 本轮复核 2 项（C16、C19），均为 CLOSED。加上此前已关闭的 C11、C12、C13、C14、C15、C17、C18、C20、C21，B20-C11–C21 累计 CLOSED 11 项、OPEN 0 项。本轮没有新增发现 ID，也没有需要按原 ID 追记的新事实错误。下文列出几条非阻断建议，不影响通过判定。

审阅者独立于作者。审阅模型为 `claude-opus-5-5`，由用户本次明确指定。这不是既有的 `gpt-6.1-sol / xhigh` 批量审阅约定，也不改写该约定。推理等级等运行元数据没有可核验的记录，本报告不补造。

本轮只做只读取证，只写本报告。审阅者未改动作者正文、来源记录、修订映射、登记、索引或计划；未创建 bucket 或对象；未挂载 Lustre；未执行任何读写或 benchmark。修订映射中的作者自述不作为证据，以下判定均来自审阅者重新取证。"通过"只表示编辑与来源层面的复核通过，不构成硬件验证、部署验证或现场验证，正文 `status: draft` 与 `verification.status: source_checked` 不因本报告改变。

## 输入（以 SHA-256 识别，均与任务给出的前缀一致）

| 输入 | SHA-256 前缀 |
|---|---|
| [T04-03 正文](../../knowledge/04-data-storage/object-and-parallel-storage.md)（100 行） | `78f8542a23b66e35` |
| [修订映射](batch-20-review-fixes.md)（T04-03 第五轮节 L91–94） | `5184fe0c30bc24a8` |
| [前次复核报告](batch-20-t04-03-claude-recheck-4.md)（C16/C19 剩余关闭条件的权威来源） | `5b97dfde3d6845b6` |
| [任务计划](../../plans/full-coverage-backlog.yaml)（T04-03 acceptance 4 条） | `f16309beadf5ae4f`（与前几轮相同） |

`make check`：PASS（90 content entries / 407 sources）。该检查只校验结构和本地链接，不说明技术正确性。

## 一次源重取证（审阅者独立获取）

全部来源都用 `curl -sSL` 并保留默认 TLS 校验，只读获取，HTTP 状态均为 200。原文只放在临时目录 `/tmp/t0403r5/`，未入库。

| 来源 | SHA-256 前缀 / 结果 | 核对点 |
|---|---|---|
| Squid objectops（`/objectops` 经 1 次重定向到 `/objectops/`） | `14f5689f8f03a427`（与前几轮及作者来源记录一致） | Get Object 节 Request Headers：`range`、`if-modified-since`（"Gets only if modified since the timestamp."）、`if-unmodified-since`（"Gets only if not modified since the timestamp."）、`if-match`（"Gets only if object ETag matches ETag."）、`if-none-match`（"Gets only if object ETag doesn't match."）。Get Object Info（`HEAD /{bucket}/{object}`）节列出同样五项。Copy Object 节的是另一组 `x-amz-copy-if-*` |
| [wiki Lustre_Release_Information](https://wiki.lustre.org/Lustre_Release_Information)（https 直取，0 次重定向） | `27732cfb518c42fe`（动态页，与前几轮不同，符合预期） | "Current LTS Release Lustre 2.15.8 Released December 2, 2025"，与正文 L43 一致。页内另有一处历史段落写 "Current LTS Release 2.2"，属旧版本存档文字，不影响判定 |
| `http://wiki.lustre.org/Lustre_Release_Information`（仅 HEAD） | 301 → `https://wiki.lustre.org/Lustre_Release_Information` | 用于判断登记 L5061 的 http 链接是否可达 |

取证限制：

1. HTML 用正则去标签解析，没有做版式级比对。
2. 本轮未重取 bucketops、S3 索引、Lustre 手册、RGW 索引和 v19.2.7 tag；这些只支撑已关闭项或本轮未改动的文字，不在本轮范围内。
3. 没有采集任何目标现场配置，也没有做任何实测。

## 逐项复核

### B20-C16 — P2 / **CLOSED**

前次关闭条件逐条核对：

1. **删除"Get Object 行推论，标推论"，改指 objectops 原文**：满足。L60 条件栏现为"条件读以 objectops GET/HEAD 五项请求头原文为据"。正文 grep "标推论""Get Object 行推论"均无命中。L60 中剩下的"为本库推论"只修饰"既非子集也非超集"，这是前几轮已认可的推论标注，与条件读无关。
2. **L56 与 L60 使用同一组请求头**：满足。L56 写全五项"range、if-modified-since、if-unmodified-since、if-match、if-none-match"，L60 以"五项请求头"引用同一集合，两处不再各列各的。五项与本轮取证的 Get Object 节、Get Object Info 节逐字一致。
3. **wiki https**（任务列入本项范围，原为 C12 的非阻断建议）：正文 L43 已改为 `https://wiki.lustre.org/Lustre_Release_Information`，直取 200。登记 L5061 仍是 `http://`，见下方非阻断第 2 条。

前次追记的作者说明错误（称 `if-match`/`if-none-match` 只见于 Copy Object）已在修订映射 L93 和正文 L56 中承认并纠正。

非阻断：

1. **正文 L56 混入修订过程说明**："（作者此前误称后两项仅见于 Copy Object，特此纠正）"是修订记录，不是面向读者的技术内容。读者不知道"作者此前"指什么。这一更正已记在修订映射 L93，建议从正文删除这个括号。
2. **登记 L5061 仍为 `http://`**：现在会 301 跳到 https，链接可用。正文已经改成 https，建议登记同步，免得同一来源出现两个 URL。
3. **L56 证据栏"同上两页"指代不清**：上一行 L55 只引用 objectops 一页，所以"同上两页"无法从相邻行推出。按内容应为 objectops（GET/HEAD）和 bucketops（GET Bucket），建议写明页名。这条前几轮已经提过。
4. **L60 证据栏只链 S3 索引**：条件栏引用了 objectops 和 bucketops 原文，证据栏却只有 S3 索引链接。建议补上这两页链接。
5. "large subset 指覆盖广度"仍未注明是本库解读（前几轮已提）。

### B20-C19 — P2 / **CLOSED**

前次关闭条件逐条核对：

1. **L88 按 L84 的同一分支改写**：满足。L88 预期为"Enabled 且可获得 versionId 时 versionId 与清单一致，其他情况读回 SHA-256 与清单一致"。"其他情况"是"Enabled 且可获得 versionId"的补集，覆盖了 Suspended、从未设置，以及 Enabled 但 versionId 不可获得三种情况，与前次关闭条件的分支一一对应。L84 的身份定义（Enabled：bucket＋key＋versionId；从未设置和 Suspended：bucket＋key＋内容哈希；端到端哈希约定为 SHA-256 并写入清单）与 L88 的判定因此一致，§5 的三层定义与场景表不再脱节。
2. **对象不可见即失败**：满足。L88 失败判据为"versionId/哈希任一不一致即失败；对象不可见即失败"。
3. 前次的问题是：多数情形下 versionId 拿不到，这一行就没有失败判据。现在这种情形落入 SHA-256 分支，每条分支都有失败判据。正文 grep "判据留空""若可获得"均无命中。

非阻断：

1. "versionId/哈希任一不一致"中的"任一"可能被理解为 Enabled 分支也要比对哈希，而预期栏在该分支只列 versionId。两种读法都不会让判定失效。若要更清楚，可写成"所在分支的比对项不一致即失败"，或明确 Enabled 分支是否同时比对 SHA-256。
2. "对象可见"没有说明用哪种操作判定（例如 HEAD 或 GET 返回成功）。最小验证设计可以接受，执行前补上即可。

## 对照 acceptance 汇总

| acceptance | 判定 | 未关闭发现 |
|---|---|---|
| 1 版本化官方文档＋实现/测试/部署；不以 latest dev 证明稳定版 | 满足：LTS 锚引 wiki（https）并附取证日 | — |
| 2 对象语义与 Lustre 语义分开 | 满足 | — |
| 3 接口/选型/瓶颈/观察点/异常按实现列出；RGW ≠ AWS S3 | 满足：条件读直接引 objectops GET/HEAD 五项原文，L56/L60 集合一致 | — |
| 4 最小验证设计＋内容校验门槛；身份/ETag/校验和不混用 | 满足：对象发布行按身份分支判定，各分支都有失败判据，并含不可见即失败 | — |

## 结论

**T04-03 通过第五次定向复核：本轮 2 项均 CLOSED（C16、C19）。B20-C11–C21 累计 CLOSED 11 项、OPEN 0 项。** 本轮没有新增发现 ID，也没有按原 ID 追记的新事实错误。

建议作者顺手处理上文非阻断项，优先删除正文 L56 中的修订过程括号，其次同步登记 L5061 的 https。这些项不需要再做定向复核。本报告只覆盖编辑与来源层面，不构成硬件、部署或现场验证。
