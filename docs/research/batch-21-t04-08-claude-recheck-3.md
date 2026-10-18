# 第二十一批 T04-08 定向复核（第三轮）

复核日期：2026-10-18（实际取证日）。复核对象：提交 `270f0d0bc6dabe75c9a6bc5f67ff237b06a05912`（T04-08 第三轮修订）之后的当前工作区文件，即 [训练数据加载饥饿诊断指南](../../knowledge/04-data-storage/data-starvation-triage.md)、[Checkpoint 慢 I/O 诊断指南](../../knowledge/04-data-storage/checkpoint-slow-io-triage.md) 与作者来源记录 [batch-21-t04-08-sources.md](batch-21-t04-08-sources.md)。核验依据：[第二次定向复核](batch-21-t04-08-claude-recheck-2.md)仍 OPEN 的 B21-C50、C54、C56 与新增 C58、C59 的关闭条件（C56 另沿用[第一次定向复核](batch-21-t04-08-claude-recheck.md) L133 的原始关闭条件），以及[修订记录](batch-21-review-fixes.md)末节「T04-08 第三轮修订」（L478–484）。

**结论：T04-08 暂不通过。** 本轮核验 5 项，CLOSED 3（C50、C54、C59），OPEN 2（C56、C58）。另有 1 项新发现 B21-C60（P3）。现存 3 项 OPEN 全部为 P3，正文需改的只有 checkpoint 两句，另需在来源记录补锚点、在修订记录追加一条更正。

- C58：L53 不再把序列化排在 staging 之前，`async_save` 的次序已与 ① 一致。但关闭条件给的两种改法（按模式改写，或注明次序以 ① 为准）都没有采用。"staging → 后台写入（含序列化）"对同步 `save` 仍不成立，第二次复核所说"两种模式下都不成立"只解决了一半。
- C56：清单第 5 项已补"冷/热基线的服务器侧"，正文侧完整。关闭条件后半"修订记录据实更正 L464 的'全部'与 L475 的'完整清单由此重新成立'"已连续两轮没有执行。
- C60（新）：① 新增的"同步 `save` 全程在调用线程执行"在 `thread_count>1` 时不成立：`FileSystemWriter.write_data` 另起 `thread_count−1` 个写线程，在返回前 join（filesystem.py L535–563）。这句与同篇步骤 3 的"`thread_count>1` 时分桶并发写"冲突，也没有固定源码锚点。这一措辞来自第二次复核 C54 的关闭条件（"都在调用线程"），属审阅侧错误，作者照用（见第 7 节）。

acceptance 1–4 两篇均判通过，其中 2 带保留意见（C58、C60）。`make check` 通过（96 content entries / 446 sources），它只校验结构与本地链接，不说明技术正确性。

审阅者角色：与初审、前两次复核相同的独立审阅者，不是编写者。执行方式：本会话运行时系统提示标识的模型为 `claude-opus-5-5`（Claude Agent SDK 环境），本轮由该会话直接完成，未委派子代理。调用方没有提供 CLI modelUsage 一类的可核验记录，本报告无法独立证实模型身份；推理等级等运行元数据也没有可核验记录，不补造。这不是既有的 `gpt-6.1-sol / xhigh` 批量审阅约定，也不改写该约定。本轮只做只读核验：未改作者正文、来源记录、修订记录、登记、索引或计划，唯一新增文件是本报告；未执行任何训练、profiling、保存/恢复、负载工具或存储操作。模型审阅不构成平台、硬件或现场验证。

## 1. 输入（以 SHA-256 识别）

| 输入 | SHA-256 |
|---|---|
| [饥饿诊断指南](../../knowledge/04-data-storage/data-starvation-triage.md)（139 行；source_refs L8–21，notes L42，NFS 行 L101，计时例子 L105，来源条目 L138） | `300139c131fab3b2a161db658dac06e0ebc3756cf468aa39caf12586b9dc1675` |
| [Checkpoint 慢 I/O 诊断指南](../../knowledge/04-data-storage/checkpoint-slow-io-triage.md)（126 行；notes L46，阶段链 L53，缺口声明 L59，步骤 1/3 L76/L78，NFS 行 L91，计时例子 L95） | `4e79329a9fbaf509352341340fd2703eb290c81c1bb7e5ff1b0bc640b8531f6b` |
| [作者来源记录](batch-21-t04-08-sources.md)（43 行；fio 行 L25，DCP 行 L27，unknown 清单 L38） | `7dcb6a43854e32bddabf526017596cc01f210c8122116045e3ed20a1111a06a9` |
| [第二次定向复核](batch-21-t04-08-claude-recheck-2.md) | `e7486d054e730607ca56a104f6ac87970e8f6f18a07cac24382f493a664c1d5b` |
| [第一次定向复核](batch-21-t04-08-claude-recheck.md)（与第二次复核所记相同） | `4b0b179d8f32ca1760dcb31454a85e5129394588e00c4089b725ba75a99d23ab` |
| [初审报告](batch-21-t04-08-claude-review.md)（与前两次复核所记相同） | `c99867734b1127eb60a6d369977fa616989d20b59049f4a3b69e4599da860e66` |
| [修订记录](batch-21-review-fixes.md)（484 行；「T04-08 第三轮修订」L478–484） | `6c9e369c3b9a5d4a1d32d37e935d7273715dbb7393ecfa498798258576d701a1` |

修订范围：在三份复核对象上，`git diff a6f841f 270f0d0` 的 hunk 只有饥饿 L42（notes）；checkpoint L46（notes）、L53（阶段链）与 L95（① 括注）；来源记录 L25、L27、L38。同一提交还新增了第二次复核报告和修订记录 L477–484，二者不是本轮复核对象。两篇的步骤表、证据表、后端表、停止条件与完成判据都没有改动。工作区在复核开始时干净，HEAD 即 270f0d0。

## 2. 上游复取（审阅者独立获取）

用 `curl -sSL` 从 `raw.githubusercontent.com` 只读获取 PyTorch commit `1eba9b3aa3c43f86f4a2c807ac8e12c4a7767340` 下 `torch/distributed/checkpoint/` 的四个文件，默认 TLS 校验，HTTP 均为 200。原文放在临时目录 `/tmp/t0408r3/`，未入库。

| 来源 | SHA-256 | 与前次 | 本轮核对点 |
|---|---|---|---|
| `state_dict_saver.py` | `a6fd9c92da2ab52dda5c433a041e6e0664aac974f659c16a1e4329ed69e8e68a` | 同第一、二次复核 | 同步 `save` 从 L59 开始；L147–158 在 `_profile()` 内直接 `return _save_state_dict(state_dict=_stateful_to_state_dict(…))`，没有 executor，也没有 stager 调用；`_save_state_dict` 从 L263 开始，L317 `reduce_scatter`，L320–323 `storage_writer.write_data`，L334 `all_reduce`。`async_save` L227 `_stateful_to_state_dict`、L229 `stage`、L233–234 提交后台、L244–248 条件同步，与前次一致 |
| `filesystem.py` | `5e4f5e5d707d0a94766ac3fe0b0329929b1f2345e8ffd0aa12b4e22bb8555b90` | 同 | `_SerialCpuLoader.values()` 在 L115 `tensor.cpu()`，D2H 拷贝在写路径内；`_OverlappingCpuLoader`（L124–146）用设备流，不另起线程。`_write_files_from_queue` 从 L273 开始，含 L320 BYTE_IO `resolve_data` 与 L263 张量 `torch.save`。`_FileSystemWriter.write_data`（L507–572）：L536–550 另起 `thread_count−1` 个 `threading.Thread` 执行 `_write_files_from_queue`，L552–560 调用线程自身也执行，L562–563 join 后才返回。`thread_count` 默认 1（`_FileSystemWriter` L449、`FileSystemWriter` L729） |
| `staging.py` | `c1ec8939780a37a8d81858e8fe821a48b329c7fb6cc1cd36214be57d7b613ab2` | 同 | 本轮无新主张，只确认字节未变 |
| `default_planner.py` | `1b66266c39a2476fda630ccd3c25ae1e547479b0fb01ac42a2102e9999ab08e1` | 同 | L136–138 `resolve_data`→`transform_object`；L146–148 BYTE_IO 时 `torch.save(object, bytes)` |

第三轮修订没有涉及 nfs(5)、exports(5)、RFC 8881、内核 NFS 文档、Ceph、Lustre、ext4、fio 的主张，所以没有重取这些来源，沿用前三轮的核对。C56 新补项的出处是库内 [本地与共享存储](../../knowledge/04-data-storage/local-and-shared-storage.md) L113（冷基线行"服务器侧 unknown"），本轮确认该行仍在，文件最后修改提交仍是 0ad0f81。

## 3. 逐项判定

| ID | 优先级 | 关闭条件核验证据 | 判定 | 剩余差距 |
|---|---|---|---|---|
| B21-C50 | P3 | L25 主张列删去了"与负载矩阵参数"，"支持范围 / 未覆盖"列注明"负载矩阵参数经 storage-workload-baselines.md 链接沿用，两篇正文未直接引用"。关闭条件二选一（删去，或移到"经链接沿用"），这里删去并在同行加注，效果相同。"直接（饥饿指南）"与正文一致：饥饿 L105 ⑦ 直接链接 fio 3.43 并给出 io_u.c 取样行；checkpoint L95 只提 slat/clat，链接的是库内基线页 §4，source_refs 也没有 `src.fio.repo-3.43`。定位表其余行除 L27（见 C59）外未改，第二次复核 3.1 的逐行结论仍成立 | **CLOSED** | 无 |
| B21-C54 | P3（上轮降级） | L95 ① 现为"①主线程与后台的分界（`async_save` 语境；同步 `save` 全程在调用线程执行，无 staging 与后台段之分，保存调用点停顿即全部）：状态收集与 staging 拷贝在主线程…；序列化在后台 save 内执行…"。关闭条件的两项都已写入：① 已限定 `async_save`；同步 `save` 句已补。"无 staging 与后台段之分"按"二者不分段"理解，与源码一致：同步路径没有 stager 调用，D2H 拷贝发生在写路径内（filesystem.py L115，或 `_OverlappingCpuLoader` 的设备流）。"保存调用点停顿即全部"与 saver L147–158、filesystem.py L562–563（返回前 join）一致 | **CLOSED** | 无。说明：同步句的"全程在调用线程执行"在 `thread_count>1` 时不成立，也没有带关闭条件改法里的 saver L152–153 锚点。这是新写入句子的精度问题，措辞源自审阅侧，另立 C60，不在 C54 内重复计 |
| B21-C56 | P3 | L38 第 5 项末尾补了"冷/热基线的服务器侧"，对应两表 NFS 缓存格的"服务器侧 unknown"（饥饿 L101 第 3 列、checkpoint L91 第 3 列；出处 T04-02 L113）。本轮把两篇中 unknown/未核对/无已核对/无已登记的全部出现处（饥饿 L91、L100–L107、L126；checkpoint L59、L79、L90–L97、L112）逐一对照 12 项清单：L79、L112、L126 是结论状态，不需要登记；其余都有对应项。checkpoint L59 的"完整清单"现在成立 | **OPEN**（P3） | 正文侧已无差距，剩下的是记录侧。第一次复核 L133 的关闭条件要求"下一轮修订记录据实更正'全部'的表述"，第二次复核又补列了 L475。第三轮修订记录（L478–484）仍没有执行：L482 只写了补项，没有说明 L464"覆盖两表出现的全部 unknown"和 L475"'完整清单'由此重新成立"在写入时不成立。改法：下一轮修订记录追加一句据实更正，不改写 L464、L475 原文；正文不需要再改 |
| B21-C58 | P3 | L53 现为"状态收集 → staging（设备到主机/主机内存拷贝，默认实现下在主线程）→ 后台写入（含序列化）→ 内核页缓存与 fsync → 存储后端 →（恢复侧）读与反序列化"。序列化已从 staging 之前移入后台写入，`async_save` 的次序（saver L227 → L229 → L234 → filesystem.py L263 / default_planner.py L148）与 ① 一致，第二次复核指出的"同文前后两种说法"在 `async_save` 语境下已消除 | **OPEN**（P3） | 关闭条件的两种改法（"L53 按模式改写阶段链"，或"在 L53 注明次序以 ① 的分界为准"）都没有采用。L53 没有限定模式，"staging → 后台写入"对同步 `save` 不成立：同步路径没有 stager 调用，也没有后台线程，D2H 拷贝在写路径内（filesystem.py L115），整个过程在保存调用返回前完成（saver L147–158）。第二次复核证据第 2 点写的是"两种模式下都不成立"，现在只解决了 `async_save` 一半。① 已经写明同步语义，L53 与 ① 在同步模式下仍不一致。改法：链后加"（`async_save` 的次序；同步 `save` 无独立 staging 与后台段，见计时例子 ①）"。第二次复核示例中的"同步 save 在调用线程"同样不精确（见 C60），不要照用 |
| B21-C59 | P3 | (a) L27 已补 filesystem.py L263 与 default_planner.py L148。本轮把 checkpoint 正文全部 PyTorch 固定 blob 锚点（L77 saver L228–242/L273–334；L78 filesystem L290–302/L331–334；L80 filesystem L617–674；L95 saver L234、L229–248，filesystem L263，default_planner L148，staging L37–116）逐一对照 L27，都已覆盖（L234 落在 L229–248 内）；第三轮正文没有新增锚点。(b) checkpoint notes 改为"初审及定向复核（B21-C35–C59）"，覆盖了关闭条件要求的 C35–C57，并延伸到第二次复核；C58、C59 的修订依据是该轮复取的同一份源码（哈希未变），这一表述成立。(c) 饥饿 notes 的枚举补了 RFC 8881，与 source_refs L16、来源条目 L138 一致 | **CLOSED** | 无。说明：关闭条件括注的"（§12）"没有写进 notes；§12 已在来源条目 L138，notes 中其他来源也只列到登记粒度，不构成差距 |

计数：CLOSED 3（C50、C54、C59），OPEN 2（C56、C58）。

## 4. 新增发现（修订引入）

| ID | 优先级 | 受影响位置 | 摘要 |
|---|---|---|---|
| B21-C60 | P3 | checkpoint L95 ① 括注；关联步骤 3 L78、来源记录 L27 | 同步 `save`"全程在调用线程执行"在 `thread_count>1` 时与固定源码不符，且没有锚点 |

### B21-C60 — P3 / OPEN：① 的同步 `save` 句在 `thread_count>1` 时与固定源码不符，且无锚点

位置：checkpoint-slow-io-triage.md L95 ① 括注"同步 `save` 全程在调用线程执行，无 staging 与后台段之分，保存调用点停顿即全部"。

证据：

- 同步 `save` 的调用链是 saver L152 `_save_state_dict` → L320–323 `storage_writer.write_data`。`FileSystemWriter`（继承 `_FileSystemWriter`）的 `write_data`（filesystem.py L507–572）在 L536–550 另起 `thread_count−1` 个 `threading.Thread`，目标都是 `_write_files_from_queue`；该函数包含 L263 的张量 `torch.save`，以及 L320 的 BYTE_IO `resolve_data`（→ default_planner.py L148 `torch.save`）。调用线程在 L552–560 也执行同一函数，在 L562–563 join 后才返回。因此 `thread_count>1` 时，一部分序列化与写入是在另起的写线程中完成的。在默认 `thread_count=1`（L449/L729）下原句成立。
- "保存调用点停顿即全部"在两种取值下都成立（返回前已 join），所以计时指导本身没有错，错在线程归属。读者如果用采样 profiler 只看调用线程，会把 join 等待当成序列化或写入耗时，误判阶段。
- 同篇步骤 3（L78）写"`thread_count>1` 时分桶并发写"，没有区分模式。同步 `save` 且 `thread_count>1` 时，它与 ① 的"全程在调用线程"直接冲突。
- 该句没有锚点。① 的 `async_save` 部分每句都带固定锚点，同步句是新增的实质主张。按本库"在实质主张附近引用精确页面或 revision"的要求，应带 saver L152–153。
- 来源：第二次复核 C54 的关闭条件写的是"状态收集、规划、序列化与写入都在调用线程（saver L152–153）"，C58 示例写的是"同步 save 在调用线程"，作者照此写入。措辞错误出在审阅侧，本报告第 7 节如实记录，不归咎作者。但正文现在的表述与固定源码不符，仍按修订引入编号。

关闭条件：把 ① 的同步句改成不涉及线程归属的表述并加锚点，例如"同步 `save` 无独立 staging 与后台段：状态收集、规划、D2H 拷贝、序列化与写入都在保存调用返回前完成（[state_dict_saver.py L152–153](https://github.com/pytorch/pytorch/blob/1eba9b3aa3c43f86f4a2c807ac8e12c4a7767340/torch/distributed/checkpoint/state_dict_saver.py#L152-L153)；`thread_count>1` 时写入由调用线程与另起的写线程分担，返回前 join，[filesystem.py L535–563](https://github.com/pytorch/pytorch/blob/1eba9b3aa3c43f86f4a2c807ac8e12c4a7767340/torch/distributed/checkpoint/filesystem.py#L535-L563)），保存调用点停顿即全部"。来源记录 L27 同步补 saver L152–153 与 filesystem.py L535–563。可与 C58 同改。

## 5. 逐条验收判定

历次判定：初审为 通过/部分/部分/通过；第二次复核为 通过/通过（保留）/通过（保留）/通过。

| # | acceptance（计划 L5365–5368） | 饥饿指南 | Checkpoint 指南 | 依据 |
|---|---|---|---|---|
| 1 | 保留相邻边界判断和已有 fixed DataLoader/DCP/MindIO 实现，不因后端类型新增统一调参命令 | **通过** | **通过** | 第三轮 hunk 只落在第 1 节所列位置。L53 改写是让 Batch 10 的既有阶段链对齐固定 DCP 实现，既有锚点与步骤一处未删。两篇新增节仍写"不给跨后端的统一调参命令"（饥饿 L96、checkpoint L86）。C58、C60 的建议改法也只是限定既有表述，不削弱本项 |
| 2 | 给出客户端/缓存、后端、CPU/队列、传输、staging/后台写入/read 的同窗计时对齐例子；明确异步重叠不能简单相加 | **通过** | **通过**（保留：C58、C60） | 饥饿 ①–⑦ 与重叠说明本轮未改，仍满足。checkpoint ① 的 `async_save` 分界与源码一致，并已限定模式（C54 CLOSED）；重叠条件完整（C53 第二次复核已关）；后端可用量与读侧分段沿用已关闭的结论。剩下的是同步句的线程归属（C60）与 L53 概述没有限定模式（C58），二者都不影响例子在 staging、后台写入与读侧的对齐内容 |
| 3 | 为 NFS/RGW/Lustre 的争用、重试、元数据、cold/warm 和空间压力增加入口，链接独立基线与恢复流程 | **通过** | **通过** | 两表五类入口本轮未改，无来源处都显式记 unknown，两篇都链接存储负载基线与存储恢复。C56 的正文侧已完整，剩余只在修订记录，不影响本项 |
| 4 | 完成判据同时检查数据/制品身份、作业进展、完整性、时延/吞吐和资源代价；来源记录说明未运行工具 | **通过** | **通过** | 两篇完成判据本轮未改（饥饿 L128、checkpoint L114）；来源记录 L38 第 12 项、两篇 notes 与来源条目都写明本轮未运行任何工具 |

## 6. 总体结论

**暂不通过。** 本轮核验 5 项：CLOSED 3、OPEN 2；新增 1 项。T04-08 累计 26 项（B21-C35–C60）：CLOSED 23，OPEN 3（C56、C58、C60），全部为 P3。acceptance 1–4 的实质内容已满足，但按本库审阅约定，OPEN 项须经修订和定向复核后才能宣告通过。

3 项改动都很小，建议同轮完成：

- checkpoint L95 ①：同步句改为"在保存调用返回前完成"一类不涉线程归属的表述，并加 saver L152–153、filesystem.py L535–563 两个锚点（C60）。
- checkpoint L53：链后注明这是 `async_save` 的次序，同步 `save` 见 ①（C58）。
- 来源记录 L27：补 saver L152–153 与 filesystem.py L535–563（C60）。
- 修订记录：追加一句据实更正，说明 L464 的"全部"与 L475 的"完整清单由此重新成立"在写入时不成立（C56）。

下一轮定向复核只需核对这 3 项及其修订 hunk。

范围外观察（不编号，不计入本轮发现）：

- 修订记录 L481 写"C58（L39 阶段链与 ① 矛盾）"，实际位置是 checkpoint L53（L39 是 frontmatter 的 `verification:` 行）；L481 引的"staging（主线程）"也与正文实际的"staging（设备到主机/主机内存拷贝，默认实现下在主线程）"不同。修订记录不在本轮三份复核对象内，所以不编号，建议随 C56 的追加更正一并订正行号。
- checkpoint summary（L24）的阶段列举"状态收集、staging 拷贝、后台写入…"同样没有区分模式（Batch 10 内容，T04-08 未改）。若按 C58 给 L53 加模式说明，作者可一并评估 summary 是否需要同样处理。
- 第二次复核列出的范围外观察（完成判据 L109 的"序列化"与"写线程"在张量路径上不可分；MindIO 链接的登记粒度）本轮未变，不重复。

## 7. 保留边界与无法核验事项

保留边界：

- 本复核只核对文本与上游源码之间、以及本库各层记录之间的一致性，不构成平台兼容、硬件或现场验证。
- 没有执行 DataLoader、profiler、DCP 保存/恢复、MindIO、fio、rados bench，也没有做 NFS 挂载、RGW 请求或 Lustre 命令。文中所有"行为"都是文档或源码层面的证据。
- 本报告不改变任何正文的编辑状态或 `verification.status`，也不回填计划或批次状态。
- 审阅侧错误如实记录，不改写前几份报告：第二次复核 C54 关闭条件的"状态收集、规划、序列化与写入都在调用线程"与 C58 示例的"同步 save 在调用线程"，在 `thread_count>1` 时不成立，作者照用后形成 C60。第二次复核核验同步路径时只对照了 saver L152–153，没有继续查到 `FileSystemWriter.write_data` 的线程模型；本轮补查后才发现。

无法核验事项：

1. 执行模型身份：运行时系统提示标识为 `claude-opus-5-5`，没有 CLI modelUsage 等可核验记录；推理等级未知。
2. 任何运行行为：只运行了 `make check`，运行前后 `git status` 都是干净的；没有运行 `make build`（会写 `build/`，超出只读复核范围）。
3. 本轮只重取了四个 DCP 源码文件。nfs(5)、exports(5)、RFC 8881、内核 NFS 文档、Ceph、Lustre 手册、admin-guide/ext4、fio 没有重取（第三轮修订不涉及其主张），沿用前三轮的取证。nfs-utils 的 release/commit 哈希仍为 unknown；Ceph Squid 点版本仍为 unknown。
4. Lustre 所引章节是否都是 LTS 2.15.x 及以前引入的特性，仍没有逐条核对 "Introduced in" 标记。
5. RFC 8881 取的是 rfc-editor.org 纯文本，与登记的 datatracker HTML 未逐字比对。
6. `thread_count>1` 时调用线程与写线程之间的实际负载分配，以及 join 等待在 profiler 中如何呈现，只是从源码读出，没有经过运行验证。同步路径中 D2H 拷贝位于写路径内，也只是源码层结论。
