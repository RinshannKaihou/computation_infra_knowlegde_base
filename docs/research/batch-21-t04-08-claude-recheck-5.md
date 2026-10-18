# 第二十一批 T04-08 定向复核（第五轮）

复核日期：2026-10-18（实际取证日）。复核对象：提交 `3483beecf04e6c274f5b1c38cec31a718f1e787e`（T04-08 第五轮修订）之后的当前工作区文件，即 [训练数据加载饥饿诊断指南](../../knowledge/04-data-storage/data-starvation-triage.md)、[Checkpoint 慢 I/O 诊断指南](../../knowledge/04-data-storage/checkpoint-slow-io-triage.md) 与作者来源记录 [batch-21-t04-08-sources.md](batch-21-t04-08-sources.md)。核验依据：[第四次定向复核](batch-21-t04-08-claude-recheck-4.md)仍 OPEN 的 B21-C60 与新增 C61 的关闭条件（C60 的条件最早见[第三次定向复核](batch-21-t04-08-claude-recheck-3.md)），以及[修订记录](batch-21-review-fixes.md)末节「T04-08 第五轮修订」（L492–496）。

**结论：通过。** 本轮核验 2 项，CLOSED 2（C60、C61），OPEN 0；修订没有引入新错误，不新增发现 ID。T04-08 累计 27 项（B21-C35–C61），CLOSED 27，OPEN 0。

- C60：① 里"同步 `save` 无 staging 与后台段之分"一句后补了 [state_dict_saver.py L152–153](https://github.com/pytorch/pytorch/blob/1eba9b3aa3c43f86f4a2c807ac8e12c4a7767340/torch/distributed/checkpoint/state_dict_saver.py#L152-L153) 锚点，并说明理由"同步 `save` 函数体无 stager 调用与 executor 提交"。来源记录 L27 也补了同一行号。本轮复取的固定源码中，L152–153 正是 `return _save_state_dict(` 与 `state_dict=_stateful_to_state_dict(state_dict),` 两行；在同步 `save` 函数体 L59–158 内检索 stage/stager/staging、executor、Thread、submit，一处都没有；同一检索在 `async_save` 内能命中 L229、L233–234（见第 2 节）。关闭。
- C61：两篇 notes 的修订依据都改成了"初审及定向复核（B21-C35 起，逐项见 docs/research/batch-21-review-fixes.md）"，这是第四次复核建议的开放写法。修订记录 T04-08 各节（L446 起）逐项记有 C35–C61 的全部 27 个 ID，"逐项见"成立。关闭。

acceptance 1–4 两篇均判通过，第四次复核为 checkpoint 第 2 条保留的 C60 已经解除。`make check` 通过（96 content entries / 446 sources），它只校验结构与本地链接，不说明技术正确性。

审阅者角色：与初审及前四次复核相同的独立审阅者，不是编写者。执行方式：本会话运行时系统提示标识的模型为 `claude-opus-5-5`（Claude Agent SDK 环境），本轮由该会话直接完成，未委派子代理。调用方没有提供 CLI modelUsage 一类的可核验记录，本报告无法独立证实模型身份；推理等级等运行元数据也没有可核验记录，不补造。这不是既有的 `gpt-6.1-sol / xhigh` 批量审阅约定，也不改写该约定；本报告的"通过"是否满足该约定，由维护者决定。本轮只做只读核验：未改作者正文、来源记录、修订记录、登记、索引或计划，唯一新增文件是本报告；未执行任何训练、profiling、保存/恢复、负载工具或存储操作。模型审阅不构成平台、硬件或现场验证。

## 1. 输入（以 SHA-256 识别）

| 输入 | SHA-256 |
|---|---|
| [饥饿诊断指南](../../knowledge/04-data-storage/data-starvation-triage.md)（139 行；notes L42，节首 L96，计时例子 L105，接续 L107，完成判据 L128） | `69ebaeb185b5f66963d14fda76262dee4f30f8dfe9a1d9d7f0e4cd962801d5a8` |
| [Checkpoint 慢 I/O 诊断指南](../../knowledge/04-data-storage/checkpoint-slow-io-triage.md)（126 行；notes L46，阶段链 L53，缺口声明 L59，步骤 2/3 L77/L78，节首 L86，计时例子 L95，接续 L97，完成判据 L114） | `78be16f761f16f89eba300538a28f43be11a10fc0947d8f99d2f83a6b76098f5` |
| [作者来源记录](batch-21-t04-08-sources.md)（43 行；DCP 行 L27，unknown 清单 L38） | `9365a6e12e0027ef0cab1d98adf18e85f8a7aa7ac5e7aacd446bc8bfd003b770` |
| [第四次定向复核](batch-21-t04-08-claude-recheck-4.md) | `66312b09503f481de9f2d56d1729c78756bc47a9b70f0e7830d89261dceaba62` |
| [第三次定向复核](batch-21-t04-08-claude-recheck-3.md)（与第四次复核所记相同） | `5020109b82d4af49dd168caa24d9bde74bb4c48062e8255c28aeaf8d07d592c7` |
| [第二次定向复核](batch-21-t04-08-claude-recheck-2.md)（同上） | `e7486d054e730607ca56a104f6ac87970e8f6f18a07cac24382f493a664c1d5b` |
| [第一次定向复核](batch-21-t04-08-claude-recheck.md)（同上） | `4b0b179d8f32ca1760dcb31454a85e5129394588e00c4089b725ba75a99d23ab` |
| [初审报告](batch-21-t04-08-claude-review.md)（同上） | `c99867734b1127eb60a6d369977fa616989d20b59049f4a3b69e4599da860e66` |
| [修订记录](batch-21-review-fixes.md)（496 行；T04-08 各节起于 L446，「T04-08 第五轮修订」L492–496） | `9ac758bc4d482b8933ce8128de0ea4810179417179946b6d89c90d1018223ad0` |

修订范围：在三份复核对象上，`git diff 6f18cf6 3483bee` 共四处 hunk：checkpoint L46（notes）、checkpoint L95（① 括注补锚点）、饥饿 L42（notes）、来源记录 L27（state_dict_saver.py 列表加 L152–153）。同一提交还新增了第四次复核报告和修订记录 L491–496。修订记录不是本轮复核对象；C61 的"逐项见"指向它，所以本轮核对了 T04-08 各节的 ID 覆盖和第五轮一节的内容。两篇的步骤表、证据表、后端表、停止条件和完成判据都没有改动。复核开始时工作区干净，HEAD 即 3483bee。

## 2. 上游复取（审阅者独立获取）

用 `curl -sSL` 从 `raw.githubusercontent.com` 只读获取 PyTorch commit `1eba9b3aa3c43f86f4a2c807ac8e12c4a7767340` 下 `torch/distributed/checkpoint/` 的四个文件，默认 TLS 校验，HTTP 均为 200。原文放在临时目录 `/tmp/t0408r5/`，未入库。

| 来源 | SHA-256 | 与前次 | 本轮核对点 |
|---|---|---|---|
| `state_dict_saver.py` | `a6fd9c92da2ab52dda5c433a041e6e0664aac974f659c16a1e4329ed69e8e68a` | 同前四次复核 | 同步 `save` 自 L59 起，下一个顶层定义是 L161–162 的 `async_save`，函数体到 L158 为止。L147–158 是 `_profile()` 块；L152 `return _save_state_dict(`，L153 `state_dict=_stateful_to_state_dict(state_dict),`。在 L59–158 内按模式 `stag|[Ee]xecutor|Thread|submit|offload|Future` 检索（`stag` 同时覆盖 stage/stager/staging/synchronize_staging），零命中。被调的 `_save_state_dict`（L263–334）内同样零命中。阳性对照：同一模式在 `async_save` 内命中 L229 `storage_writer.stage`、L231 `_offload_state_dict_to_cpu`、L233 `ThreadPoolExecutor`、L234 `executor.submit`，说明检索有效。另外，L323 调 `storage_writer.write_data`，L325 `all_writes.wait()`，L334 `all_reduce` |
| `filesystem.py` | `5e4f5e5d707d0a94766ac3fe0b0329929b1f2345e8ffd0aa12b4e22bb8555b90` | 同 | L535–550 另起 `thread_count−1` 个 `threading.Thread`；L552–560 调用线程自己也执行 `_write_files_from_queue`；L562–563 join；L570–572 返回已 `set_result` 的 Future。与第四次复核所记一致 |
| `staging.py` | `c1ec8939780a37a8d81858e8fe821a48b329c7fb6cc1cd36214be57d7b613ab2` | 同 | 本轮无新主张，只确认字节未变 |
| `default_planner.py` | `1b66266c39a2476fda630ccd3c25ae1e547479b0fb01ac42a2102e9999ab08e1` | 同 | 本轮无新主张；L148 锚点未变 |

第五轮修订不涉及 nfs(5)、exports(5)、RFC 8881、内核 NFS 文档、Ceph、Lustre、ext4、fio 的主张，所以没有重取这些来源，沿用前几轮的核对。

## 3. 逐项判定

| ID | 优先级 | 关闭条件核验证据 | 判定 | 剩余差距 |
|---|---|---|---|---|
| B21-C60 | P3 | 关闭条件（第三次复核 L72，第四次复核 L50 收窄为剩余差距）：(a) ① 的同步句不涉及线程归属；(b) 加 saver L152–153（或 L147–158）与 filesystem.py L535–563 两个锚点；(c) 来源记录 L27 同步补这两个行号。第四次复核判 (a) 已满足，(b)(c) 只补了 filesystem.py 一半，剩余差距是"同步 `save` 无 staging 与后台段之分"没有固定锚点。本轮核对：(b) checkpoint L95 ① 现为"同步 `save` 无 staging 与后台段之分——同步 `save` 函数体无 stager 调用与 executor 提交，见 [state_dict_saver.py L152–153](https://github.com/pytorch/pytorch/blob/1eba9b3aa3c43f86f4a2c807ac8e12c4a7767340/torch/distributed/checkpoint/state_dict_saver.py#L152-L153)——调用方等到保存完成才返回，`thread_count>1` 时写入分到额外线程并在返回前 join，见 filesystem.py L535–563"。链接的 commit 与 `#L152-L153` 片段正确，两行内容见第 2 节。"函数体无 stager 调用与 executor 提交"经 L59–158 全函数体检索成立（检索模式与阳性对照见第 2 节）；`async_save` 的对应调用（L229 `stage`、L233–234 executor `submit`）都在 L161 之后。锚点没有放在第四次复核建议的"调用方等到保存完成才返回"之后，而是紧跟"无 staging 与后台段之分"。剩余差距针对的正是这个主张，所以这个位置更贴切。(c) 来源记录 L27 的 state_dict_saver.py 列表现为"L152–153/L228–242/L229–248/L273–334"，filesystem.py 列表保留 L535–563。(a) 未退化：句中仍没有线程归属表述，"写入分到额外线程并在返回前 join"与 L536–563 一致 | **CLOSED** | 无 |
| B21-C61 | P3 | 关闭条件（第四次复核 L71）：把 checkpoint L46 的区间改到至少覆盖 C60（若按 C61 修订则到 C61），或者改成不需要逐轮更新的写法，例如"初审及历次定向复核（B21-C35 起，逐项见修订记录）"；饥饿 L42 可改可不改。本轮核对：checkpoint L46 与饥饿 L42 现在都是"初审及定向复核（B21-C35 起，逐项见 docs/research/batch-21-review-fixes.md）修订为准"，采用开放写法，两篇统一。逐点核对：(1) 两份文件与来源记录中都已不含"C35–C5x"一类的闭区间。(2) 路径 `docs/research/batch-21-review-fixes.md` 存在；它写在 YAML 字符串里，不是 Markdown 链接，`make check` 不校验它，这符合 notes 字段的用法。(3) "逐项见"成立：修订记录 T04-08 各节（L446、L469、L478、L486、L492 五节）逐一记有 C35–C61 全部 27 个 ID，每个 ID 至少出现一次。(4) 两篇 notes 的其余文字（"本轮未重取上游页面""未运行任何工具"）未改，与 C59(b) 关闭时的口径一致 | **CLOSED** | 无 |

计数：CLOSED 2（C60、C61），OPEN 0。

## 4. 新增发现（修订引入）

无。本轮核对了第五轮全部四处 hunk，以及修订记录 L492–496 对它们的描述：

- checkpoint L95 ①：新插入的锚点子句没有改动 ① 中任何既有主张。括注里的两组破折号让句子变长，但层次可读（主张 → 锚点理由 → 调用方语义 → join 锚点）。这属于行文问题，不是错误，不编号。
- checkpoint L46 与饥饿 L42：只替换了修订依据的写法，其余字节未变。
- 来源记录 L27：只在 state_dict_saver.py 列表加了 L152–153，按行号升序插入。checkpoint 正文现有 12 处 DCP 固定锚点（L77 两处、L78 两处、L80 一处、L95 七处），全部落在 L27 列表内。
- 修订记录 L492–496：标题中的"第四次定向复核 2/3 CLOSED"与第四次复核计数一致；C60、C61 两条与实际 hunk 一致。"记录更正"一条说第三、四轮记录（L481、L489）误把阶段链位置写成 L39、实际为 L53、L39 是 verification 行。本轮在 a6f841f、270f0d0、6f18cf6、3483bee 四个版本上逐一核对，L39 都是 `verification:`，L53 都是阶段链所在的"触发："段，L481、L489 的原文也都写着"L39"，更正属实，原文未改写。

## 5. 逐条验收判定

历次判定：初审为 通过/部分/部分/通过；第二、三、四次复核均为 1–4 全部通过，其中 checkpoint 第 2 条带保留（第四次复核的保留为 C60）。

| # | acceptance（计划 L5365–5368） | 饥饿指南 | Checkpoint 指南 | 依据 |
|---|---|---|---|---|
| 1 | 保留相邻边界判断和已有 fixed DataLoader/DCP/MindIO 实现，不因后端类型新增统一调参命令 | **通过** | **通过** | 第五轮 hunk 只有 notes 改写、一个锚点及其理由、来源记录一个行号，没有删改任何既有实现主张。checkpoint 的 DCP 固定锚点从 11 处增至 12 处，都在来源记录 L27 内；步骤 6 的 MindIO 两处固定锚点未动。饥饿指南的 DataLoader 固定锚点未动。两篇的"不给跨后端的统一调参命令"仍在（饥饿 L96、checkpoint L86），本轮没有新增调参命令 |
| 2 | 给出客户端/缓存、后端、CPU/队列、传输、staging/后台写入/read 的同窗计时对齐例子；明确异步重叠不能简单相加 | **通过** | **通过**（保留解除） | 饥饿 L105 未改，仍满足。checkpoint：C60 关闭后，① 中同步 `save` 与 `async_save` 的分界都有固定锚点（同步侧 L152–153、L535–563；异步侧 L234、L229–248、staging.py L37–116），L53 阶段链括注引用的 ① 不再缺出处。重叠条件、后端可用量和读侧分段沿用已关闭的结论 |
| 3 | 为 NFS/RGW/Lustre 的争用、重试、元数据、cold/warm 和空间压力增加入口，链接独立基线与恢复流程 | **通过** | **通过** | 两表本轮未改；来源记录 L38 的 unknown 清单未改，C56 关闭时逐处对照的结论仍成立。两篇仍链接存储负载基线与存储恢复（饥饿 L107、checkpoint L97） |
| 4 | 完成判据同时检查数据/制品身份、作业进展、完整性、时延/吞吐和资源代价；来源记录说明未运行工具 | **通过** | **通过** | 完成判据未改（饥饿 L128、checkpoint L114）。来源记录 L38 第 12 项、两篇 notes（"未运行任何工具"）和两篇来源条目（饥饿 L138、checkpoint L122）仍写明未运行任何工具；C61 改写的只是 notes 中的修订依据，没有动这部分说明 |

## 6. 总体结论

**通过。** 本轮核验 2 项：CLOSED 2、OPEN 0；无新增发现。T04-08 累计 27 项（B21-C35–C61）：CLOSED 27，OPEN 0。acceptance 1–4 两篇均判通过，不再带保留。按本库审阅约定，每个发现都经过修订和定向复核后关闭，审阅链到此结束。

这一结论的范围：

- 它是编辑与来源一致性审阅的结论，不改变两篇的 `status: draft` 或 `verification.status: source_checked`，也不回填计划或批次状态；是否据此推进状态由维护者决定。
- 执行模型是 `claude-opus-5-5`，不是 `gpt-6.1-sol / xhigh` 批量审阅约定所指的模型。该约定是否需要另行补审，本报告不作判断。

范围外观察（不编号，不计入本轮发现）：

- 修订记录 L490 说第三轮原句"与 thread_count>1 线程模型相反"，比第三次复核的判断（`thread_count=1` 时成立、`>1` 时不成立）更重。第四次复核已记下这一点，本轮没有变化。它只是历史记录的措辞，不影响正文，不需要跟进。
- ① 用两行锚点 L152–153 支持一个关于整个函数体的否定主张（"无 stager 调用与 executor 提交"）。读者点开锚点，只能看到 `save` 直接进入 `_save_state_dict` 的那两行，否定部分要读完 L59–158 才能确认；本轮已经完整读过。第四次复核把 L152–153 与 L147–158 都列为可接受的写法，所以这里不构成差距。如果以后要改，可以把锚点扩到 L147–158，让读者在一屏之内看到完整的 `_profile()` 块。

## 7. 保留边界与无法核验事项

保留边界：

- 本复核只核对文本与上游源码之间、以及本库各层记录之间的一致性，不构成平台兼容、硬件或现场验证。
- 没有执行 DataLoader、profiler、DCP 保存/恢复、MindIO、fio、rados bench，也没有做 NFS 挂载、RGW 请求或 Lustre 命令。文中所有"行为"都是文档或源码层面的证据。
- 本报告不改变任何正文的编辑状态或 `verification.status`，也不回填计划或批次状态。
- 审阅侧自查：第四次复核给出的 C60 锚点（saver L152–153，或 L147–158）和 C61 的开放写法示例，经本轮复取的源码与修订记录核对都成立。本轮没有发现前几份报告中新的审阅侧错误。

无法核验事项：

1. 执行模型身份：运行时系统提示标识为 `claude-opus-5-5`，没有 CLI modelUsage 等可核验记录；推理等级未知。
2. 任何运行行为：只运行了 `make check`，运行前 `git status` 干净；没有运行 `make build`，因为它会写 `build/`，超出只读复核范围。
3. 本轮只重取了四个 DCP 源码文件。nfs(5)、exports(5)、RFC 8881、内核 NFS 文档、Ceph、Lustre 手册、admin-guide/ext4 和 fio 都没有重取（第五轮修订不涉及它们的主张），沿用前几轮的取证。nfs-utils 的 release/commit 哈希仍为 unknown，Ceph Squid 点版本也仍为 unknown。
4. Lustre 所引章节是否都是 LTS 2.15.x 及以前引入的特性，仍没有逐条核对 "Introduced in" 标记。
5. RFC 8881 取的是 rfc-editor.org 纯文本，与登记的 datatracker HTML 未逐字比对。
6. `thread_count>1` 时调用线程与写线程之间的实际负载分配，以及 join 等待在 profiler 中如何呈现，都只是从源码读出，没有经过运行验证。
