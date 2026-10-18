# 第二十一批 T04-08 定向复核（第四轮）

复核日期：2026-10-18（实际取证日）。复核对象：提交 `6f18cf69877dcdec5581c888faecf9baa02966cd`（T04-08 第四轮修订）之后的当前工作区文件，即 [训练数据加载饥饿诊断指南](../../knowledge/04-data-storage/data-starvation-triage.md)、[Checkpoint 慢 I/O 诊断指南](../../knowledge/04-data-storage/checkpoint-slow-io-triage.md) 与作者来源记录 [batch-21-t04-08-sources.md](batch-21-t04-08-sources.md)。核验依据：[第三次定向复核](batch-21-t04-08-claude-recheck-3.md)仍 OPEN 的 B21-C56、C58 与新增 C60 的关闭条件（C56 另沿用[第一次定向复核](batch-21-t04-08-claude-recheck.md) L133 与[第二次定向复核](batch-21-t04-08-claude-recheck-2.md)补列的条件），以及[修订记录](batch-21-review-fixes.md)末节「T04-08 第四轮修订」（L486–490）。

**结论：T04-08 暂不通过。** 本轮核验 3 项，CLOSED 2（C56、C58），OPEN 1（C60）。另有 1 项新发现 B21-C61（P3）。现存 2 项 OPEN 都是 P3，需要改的是 checkpoint 一篇的一个锚点和 notes 中的一个区间，加上来源记录里一个行号。

- C56：修订记录 L488 追加了据实更正，指明 L464 的"全部"与 L475 的"完整清单由此重新成立"在写入时不成立，L464、L475 原文未改写。关闭。
- C58：L53 链后注明"阶段次序按 `async_save` 实现叙述；同步 `save` 无 staging/后台分段，见…①"，与固定源码一致。关闭。
- C60：线程归属的错误已改掉，filesystem.py L535–563 锚点已加到正文和来源记录 L27。关闭条件要求的另一个锚点 saver L152–153 没有加，正文和来源记录都没有。"同步 `save` 无 staging 与后台段之分"这一主张仍没有固定锚点：正文现有的 saver 锚点都不在同步 `save` 的函数体内，filesystem.py L535–563 只能说明 `write_data` 返回前 join。
- C61（新）：checkpoint `verification.notes` 的修订依据区间仍写"B21-C35–C59"。第四轮按 C60 改写了 ① 并新增锚点，notes 没有同步，与 C59(b) 属同类问题。

acceptance 1–4 两篇均判通过，其中 checkpoint 第 2 条保留 C60。`make check` 通过（96 content entries / 446 sources），它只校验结构与本地链接，不说明技术正确性。

审阅者角色：与初审、前三次复核相同的独立审阅者，不是编写者。执行方式：本会话运行时系统提示标识的模型为 `claude-opus-5-5`（Claude Agent SDK 环境），本轮由该会话直接完成，未委派子代理。调用方没有提供 CLI modelUsage 一类的可核验记录，本报告无法独立证实模型身份；推理等级等运行元数据也没有可核验记录，不补造。这不是既有的 `gpt-6.1-sol / xhigh` 批量审阅约定，也不改写该约定。本轮只做只读核验：未改作者正文、来源记录、修订记录、登记、索引或计划，唯一新增文件是本报告；未执行任何训练、profiling、保存/恢复、负载工具或存储操作。模型审阅不构成平台、硬件或现场验证。

## 1. 输入（以 SHA-256 识别）

| 输入 | SHA-256 |
|---|---|
| [饥饿诊断指南](../../knowledge/04-data-storage/data-starvation-triage.md)（139 行；notes L42，节首 L96，计时例子 L105，接续 L107，完成判据 L128） | `300139c131fab3b2a161db658dac06e0ebc3756cf468aa39caf12586b9dc1675`（与第三次复核所记相同） |
| [Checkpoint 慢 I/O 诊断指南](../../knowledge/04-data-storage/checkpoint-slow-io-triage.md)（126 行；notes L46，阶段链 L53，缺口声明 L59，步骤 2/3 L77/L78，节首 L86，计时例子 L95，接续 L97，完成判据 L114） | `280922db6dd6a813aef4e101ed482cc00f8f2d3344a953d69a4b404600f5c993` |
| [作者来源记录](batch-21-t04-08-sources.md)（43 行；DCP 行 L27，unknown 清单 L38） | `b8b57e01a23a7cae785eb5ddc9bb488161fa8c9b339efd94033125ebf2c0d6d5` |
| [第三次定向复核](batch-21-t04-08-claude-recheck-3.md) | `5020109b82d4af49dd168caa24d9bde74bb4c48062e8255c28aeaf8d07d592c7` |
| [第二次定向复核](batch-21-t04-08-claude-recheck-2.md)（与第三次复核所记相同） | `e7486d054e730607ca56a104f6ac87970e8f6f18a07cac24382f493a664c1d5b` |
| [第一次定向复核](batch-21-t04-08-claude-recheck.md)（同上） | `4b0b179d8f32ca1760dcb31454a85e5129394588e00c4089b725ba75a99d23ab` |
| [初审报告](batch-21-t04-08-claude-review.md)（同上） | `c99867734b1127eb60a6d369977fa616989d20b59049f4a3b69e4599da860e66` |
| [修订记录](batch-21-review-fixes.md)（490 行；第一轮 L464，第二轮 L475，第三轮 L481，「T04-08 第四轮修订」L486–490） | `e3b8cb5adcac8f2195b6d818aaecc56559e365bbd6ea7cb4b19577146bd64bf9` |

修订范围：在三份复核对象上，`git diff 270f0d0 6f18cf6` 只有三处 hunk：checkpoint L53（链后括注）、checkpoint L95（① 括注）、来源记录 L27（filesystem.py 列表加 L535–563）。饥饿指南的 diff 为空。同一提交还新增了第三次复核报告和修订记录 L485–490。修订记录不是本轮复核对象，但 C56 的关闭条件落在修订记录上，所以本轮核对了它的这一节。两篇的步骤表、证据表、后端表、停止条件、完成判据与 notes 都没有改动。工作区在复核开始时干净，HEAD 即 6f18cf6。

## 2. 上游复取（审阅者独立获取）

用 `curl -sSL` 从 `raw.githubusercontent.com` 只读获取 PyTorch commit `1eba9b3aa3c43f86f4a2c807ac8e12c4a7767340` 下 `torch/distributed/checkpoint/` 的四个文件，默认 TLS 校验，HTTP 均为 200。原文放在临时目录 `/tmp/t0408r4/`，未入库。

| 来源 | SHA-256 | 与前次 | 本轮核对点 |
|---|---|---|---|
| `state_dict_saver.py` | `a6fd9c92da2ab52dda5c433a041e6e0664aac974f659c16a1e4329ed69e8e68a` | 同前三次复核 | 同步 `save` 从 L59 开始。L147–158 是 `_profile()` 块：`_storage_setup` 之后直接 `return _save_state_dict(state_dict=_stateful_to_state_dict(state_dict), …)`（L152–153），没有 executor，也没有 `stage()` 调用。`_save_state_dict` 中 L323 调 `storage_writer.write_data`，L325 `all_writes.wait()`，L334 `all_reduce`。`async_save`：L227 `_stateful_to_state_dict`；L228–231 调 `stage`，非 AsyncStager 时调 `_offload_state_dict_to_cpu`；L233–241 用单 worker `ThreadPoolExecutor` 提交 `save`；L244–248 按条件调 `synchronize_staging()`；L250 返回 Future |
| `filesystem.py` | `5e4f5e5d707d0a94766ac3fe0b0329929b1f2345e8ffd0aa12b4e22bb8555b90` | 同 | `_FileSystemWriter.write_data`（L507–572）：L535 `threads = []`；L536–550 另起 `thread_count−1` 个 `threading.Thread`，目标是 `_write_files_from_queue`；L552–560 调用线程自己也执行该函数；L562–563 join；L570–572 返回已 `set_result` 的 Future。`thread_count` 默认 1（L449、L729） |
| `staging.py` | `c1ec8939780a37a8d81858e8fe821a48b329c7fb6cc1cd36214be57d7b613ab2` | 同 | 本轮无新主张，只确认字节未变 |
| `default_planner.py` | `1b66266c39a2476fda630ccd3c25ae1e547479b0fb01ac42a2102e9999ab08e1` | 同 | 本轮无新主张；L148 锚点未变 |

第四轮修订不涉及 nfs(5)、exports(5)、RFC 8881、内核 NFS 文档、Ceph、Lustre、ext4、fio 的主张，所以没有重取这些来源，沿用前几轮的核对。

## 3. 逐项判定

| ID | 优先级 | 关闭条件核验证据 | 判定 | 剩余差距 |
|---|---|---|---|---|
| B21-C56 | P3 | 关闭条件：第一次复核 L133 要求修订记录据实更正"全部"；第二次复核补列 L475；第三次复核给出改法"下一轮修订记录追加一句据实更正，不改写 L464、L475 原文；正文不需要再改"。修订记录 L488 现为"特此更正——第一轮记录 L464「覆盖两表出现的全部 unknown」与第二轮记录 L475「完整清单由此重新成立」两处说法当时不成立（缺 NFS 冷/热基线服务器侧等项，经第三轮修订才补齐）；以本行更正为准"。逐点核对：(1) 两处引文与原文一致。L464 原文"覆盖两表出现的全部 unknown"逐字相同；L475 原文是"checkpoint 缺口声明"完整清单"由此重新成立"，更正只去掉了内层引号，意思不变。(2) 更正理由属实。L464 写入时清单还缺三项：第二轮补的"客户端 pNFS 实现范围"、"属性/目录项缓存与 v4 委托是否随本机 drop_caches 失效"，以及第三轮补的"冷/热基线的服务器侧"，都在"等项"之内。L475 写入时只缺最后一项。(3) `git diff 270f0d0 6f18cf6` 在修订记录上只有新增行，L464、L475 原文未改写。(4) 正文侧：来源记录 L38 与两表的 unknown 本轮未改，第三次复核逐处对照的结论仍成立，checkpoint L59 的"完整清单"成立 | **CLOSED** | 无 |
| B21-C58 | P3 | 关闭条件（第三次复核 L49）：在链后加"（`async_save` 的次序；同步 `save` 无独立 staging 与后台段，见计时例子 ①）"，或者采用第二次复核给的另一种改法。L53 链后现为"（阶段次序按 `async_save` 实现叙述；同步 `save` 无 staging/后台分段，见「后端支路入口与同窗计时对齐」节①）"，与建议改法同义。对照源码：`async_save` 的次序是 saver L227 → L228–231 → L233–241 → 写路径（filesystem.py L263 / default_planner.py L148），与链一致；同步 `save` 的 L147–158 没有 stager 也没有 executor，"无 staging/后台分段"成立。括注引用的节名与 L84 标题一致，① 在 L95。第二次复核说的"两种模式下都不成立"，两半现在都已解决 | **CLOSED** | 无。说明：括注中的同步主张以 ① 为出处，而 ① 中该主张缺锚点，这一问题计入 C60，不在这里重复计 |
| B21-C60 | P3 | 关闭条件（第三次复核 L72，第 6 节 L91、L93）分三项。(a) 把 ① 的同步句改成不涉及线程归属的表述；(b) 加 saver L152–153 与 filesystem.py L535–563 两个锚点；(c) 来源记录 L27 同步补这两个行号。核对结果如下。(a) 满足。"全程在调用线程执行"已删除，现为"调用方等到保存完成才返回——`thread_count>1` 时写入分到额外线程并在返回前 join"。"等到保存完成才返回"与 saver L152–153 → L323/L325（`wait()`）→ L334 一致，也与 filesystem.py L562–572（join 后返回已完成的 Future）一致。同步路径与步骤 3 L78"`thread_count>1` 时分桶并发写"也不再冲突。(b) 只满足一半。filesystem.py L535–563 已加，范围覆盖 L536–550 另起线程、L552–560 调用线程参与和 L562–563 join，行号与固定源码一致；saver L152–153 没有加。(c) 同样只补了 L535–563 | **OPEN**（P3） | 剩余差距是"同步 `save` 无 staging 与后台段之分"仍没有固定锚点。全文的 saver 锚点只有 L77 的 L228–242、L273–334 和 L95 的 L234、L229–248，都不在同步 `save` 的函数体（L59–158）内。filesystem.py L535–563 只说明 `write_data` 在返回前 join，不能说明同步路径没有 stager 和后台 executor。第三次复核 C60 证据第 4 点针对的正是这个缺口。修订记录 L490 如实写了"来源记录 DCP 行补该锚点"（单数），但没有说明为什么不补 saver 锚点。改法：在 ① 的"调用方等到保存完成才返回"之后加 [state_dict_saver.py L152–153](https://github.com/pytorch/pytorch/blob/1eba9b3aa3c43f86f4a2c807ac8e12c4a7767340/torch/distributed/checkpoint/state_dict_saver.py#L152-L153)（也可以用 L147–158），来源记录 L27 的 state_dict_saver.py 列表补同一行号。可选：把"写入分到额外线程"改为"写入由调用线程与另起的 `thread_count−1` 个线程分担"（L536–560）。现句没有提到调用线程也参与写入，但也没有说写入只在额外线程中进行，不算错误，不计入差距 |

计数：CLOSED 2（C56、C58），OPEN 1（C60）。

## 4. 新增发现（修订引入）

| ID | 优先级 | 受影响位置 | 摘要 |
|---|---|---|---|
| B21-C61 | P3 | checkpoint L46 `verification.notes` | 修订依据区间"B21-C35–C59"没有纳入第四轮的修订依据 C60 |

### B21-C61 — P3 / OPEN：checkpoint notes 的修订依据区间未纳入 C60

位置：checkpoint-slow-io-triage.md L46 `verification.notes`："新增条目以 T04-02/03/06/07 已核对口径与初审及定向复核（B21-C35–C59）修订为准"。

证据：

- 第四轮按 C60 改写了 L95 ① 的同步句，并新增 filesystem.py L535–563 锚点。这次改写的依据是第三次复核的 C60 及其复取的源码，不在"C35–C59"之内。notes 本轮未改：`git diff 270f0d0 6f18cf6` 在 L46 没有 hunk。
- 同类问题有先例。C59(b) 要求 notes 的修订依据覆盖复核引入的锚点，作者在第三轮把区间写成"C35–C59"。显式的 ID 区间每轮修订都要跟着改，这一轮漏改了。
- 饥饿指南 L42 也写"C35–C59"。但饥饿指南第四轮未改，C60 也不涉及它，所以那一处仍然成立，不计入本项。
- 影响限于验证元数据的可追溯性，不影响技术内容，也不影响 acceptance 判定。

关闭条件：把 checkpoint L46 的区间改为覆盖实际依据（至少到 C60；若下一轮按 C61 修订，则到 C61）。也可以改成不需要逐轮更新的写法，例如"初审及历次定向复核（B21-C35 起，逐项见修订记录）"，这样以后不会再出现同类问题。饥饿 L42 可以不动；如果想让两篇写法统一，也可以一起改。

## 5. 逐条验收判定

历次判定：初审为 通过/部分/部分/通过；第二、三次复核均为 1–4 全部通过，其中 checkpoint 第 2 条带保留。

| # | acceptance（计划 L5365–5368） | 饥饿指南 | Checkpoint 指南 | 依据 |
|---|---|---|---|---|
| 1 | 保留相邻边界判断和已有 fixed DataLoader/DCP/MindIO 实现，不因后端类型新增统一调参命令 | **通过** | **通过** | 第四轮 hunk 只在 checkpoint L53、L95 与来源记录 L27，内容都是加限定或补锚点。checkpoint 全文的 11 处 DCP 固定锚点（L77 两处、L78 两处、L80、L95 六处）都还在，且都在来源记录 L27 的列表内（L234 落在 L229–248 内）；步骤 6 的 MindIO 锚点未动。两篇的"不给跨后端的统一调参命令"仍在（饥饿 L96、checkpoint L86），本轮没有新增调参命令 |
| 2 | 给出客户端/缓存、后端、CPU/队列、传输、staging/后台写入/read 的同窗计时对齐例子；明确异步重叠不能简单相加 | **通过** | **通过**（保留：C60） | 饥饿指南文件未变（哈希与第三次复核相同），仍满足。checkpoint：C58 关闭后，L53 的概述与 ① 在两种模式下都一致；① 的同步句不再有线程归属错误，join 语义带了锚点；`async_save` 的分界、重叠条件、后端可用量与读侧分段沿用已关闭的结论。剩下的只是同步主张缺 saver 锚点（C60），不影响例子在 staging、后台写入和读侧的对齐内容 |
| 3 | 为 NFS/RGW/Lustre 的争用、重试、元数据、cold/warm 和空间压力增加入口，链接独立基线与恢复流程 | **通过** | **通过** | 两表本轮未改。C56 关闭后，正文中的 unknown 与来源记录清单一致，修订记录里过时的说法也已更正。两篇仍链接存储负载基线与存储恢复（饥饿 L107、checkpoint L97） |
| 4 | 完成判据同时检查数据/制品身份、作业进展、完整性、时延/吞吐和资源代价；来源记录说明未运行工具 | **通过** | **通过** | 完成判据未改（饥饿 L128、checkpoint L114）。来源记录 L38 第 12 项、两篇 notes 与来源条目仍写明未运行任何工具。C61 只涉及 notes 中的修订依据区间，与"未运行工具"的说明无关 |

## 6. 总体结论

**暂不通过。** 本轮核验 3 项：CLOSED 2、OPEN 1；新增 1 项。T04-08 累计 27 项（B21-C35–C61）：CLOSED 25，OPEN 2（C60、C61），全部为 P3。acceptance 1–4 的实质内容已满足，但按本库审阅约定，OPEN 项须经修订和定向复核后才能宣告通过。

剩余改动只涉及 checkpoint 一篇和来源记录的一行，可以同轮完成：

- checkpoint L95 ①：在"调用方等到保存完成才返回"之后加 saver L152–153（或 L147–158）锚点（C60）。
- 来源记录 L27：在 state_dict_saver.py 的列表中补同一行号（C60）。
- checkpoint L46 notes：把修订依据区间改到覆盖 C60/C61，或者改成不需要逐轮更新的写法（C61）。

下一轮定向复核只需核对这 2 项及其修订 hunk。

第二次复核的关闭条件措辞曾经引出 C60。为避免再出现这种情况，本报告建议的锚点都已对照本轮复取的固定源码逐行核过：L152–153 是 `return _save_state_dict(` 与 `state_dict=_stateful_to_state_dict(state_dict),` 两行，L147–158 是整个 `_profile()` 块，两者都没有 stager 或 executor 调用。

范围外观察（不编号，不计入本轮发现）：

- 修订记录 L481 和 L489 两次把阶段链的位置写成"L39"。逐版本核对 ea81e79 到 6f18cf6，阶段链在初次提交时位于 L52，此后一直在 L53；L39 是 frontmatter 的 `verification:` 行。第二、三次复核写的都是 L53，所以这个行号错误出在修订记录一侧。第三次复核已经建议订正，第四轮没有订正，L489 又用了一次。修订记录不是本轮复核对象，因此不编号；建议下一轮按 C56 的做法追加一句更正。
- 修订记录 L490 说原句"与 thread_count>1 线程模型相反"。第三次复核的判断是 `thread_count=1` 时成立、`>1` 时不成立，L490 的说法比这更重。这不影响正文，记在这里。
- checkpoint summary（L24）用"或"列举候选阶段，不是在陈述次序，不需要跟着 L53 补模式说明。第三次复核提出的这条观察到此结束。
- 第二次复核列出的其他范围外观察（完成判据 L109 的"序列化"与"写线程"在张量路径上不可分；MindIO 链接的登记粒度）本轮没有变化，不再重复。

## 7. 保留边界与无法核验事项

保留边界：

- 本复核只核对文本与上游源码之间、以及本库各层记录之间的一致性，不构成平台兼容、硬件或现场验证。
- 没有执行 DataLoader、profiler、DCP 保存/恢复、MindIO、fio、rados bench，也没有做 NFS 挂载、RGW 请求或 Lustre 命令。文中所有"行为"都是文档或源码层面的证据。
- 本报告不改变任何正文的编辑状态或 `verification.status`，也不回填计划或批次状态。
- 审阅侧核对：第三次复核 C60 给出的示例措辞（"由调用线程与另起的写线程分担，返回前 join"）及其锚点（saver L152–153、filesystem.py L535–563），经本轮复取的源码核对都成立。本轮没有发现前几份报告中新的审阅侧错误。

无法核验事项：

1. 执行模型身份：运行时系统提示标识为 `claude-opus-5-5`，没有 CLI modelUsage 等可核验记录；推理等级未知。
2. 任何运行行为：只运行了 `make check`，运行前后 `git status` 都是干净的；没有运行 `make build`，因为它会写 `build/`，超出只读复核范围。
3. 本轮只重取了四个 DCP 源码文件。nfs(5)、exports(5)、RFC 8881、内核 NFS 文档、Ceph、Lustre 手册、admin-guide/ext4 和 fio 都没有重取（第四轮修订不涉及它们的主张），沿用前几轮的取证。nfs-utils 的 release/commit 哈希仍为 unknown，Ceph Squid 点版本也仍为 unknown。
4. Lustre 所引章节是否都是 LTS 2.15.x 及以前引入的特性，仍没有逐条核对 "Introduced in" 标记。
5. RFC 8881 取的是 rfc-editor.org 纯文本，与登记的 datatracker HTML 未逐字比对。
6. `thread_count>1` 时调用线程与写线程之间的实际负载分配，以及 join 等待在 profiler 中如何呈现，都只是从源码读出，没有经过运行验证。
