# 第二十批 T04-04 初审

审阅日期：2026-10-13（实际取证日）。正文 `updated_at` 与登记 `registered_at` 中的 `2026-10-14` 视为交付标签，不作为本轮取证日期；输入以下表 SHA-256 识别。

**结论：T04-04 需修订。新增 10 项发现（B20-C22–C31）：P1 ×6、P2 ×3、P3 ×1，全部 OPEN。** acceptance 1、2、4 都有 P1 缺口，acceptance 3 有 P2 缺口。`make check` 通过（91 content entries / 409 sources），但它只校验结构与本地链接，不说明技术正确性。正文 `verification.status: source_checked` 与 notes"已核对 … hub 下载指南"所指的是 latest 页面而不是 v0.33.0 页面（C23）。修订复核前，不得据此视为已核对。

审阅者角色独立于作者。审阅模型为 `claude-opus-5-5`，由用户本次明确要求试用。这不是既有的 `gpt-6.1-sol / xhigh` 批量审阅约定，也不改写该约定；推理等级等运行元数据没有可核验记录，不补造。本轮只做审阅和只读取证：未改作者正文、来源记录、登记、索引或计划，未下载任何模型，未上传或发布对象，未执行读写、中断或计时试验。模型审阅不构成硬件或现场验证。

## 输入（以 SHA-256 识别）

| 输入 | SHA-256 |
|---|---|
| [T04-04 正文](../../knowledge/04-data-storage/artifact-transfer-and-publication.md)（78 行，procedure / draft） | `15ac48eae4c838593de0eac26c4b70f943356ee4c866330166ffc5bb4ae5af1b` |
| [作者来源记录](batch-20-t04-04-sources.md)（15 行） | `eba7cb415b9cacbe7193fa01dbd812242eec2db65a2629886e36c105e1fffc43` |
| [任务计划](../../plans/full-coverage-backlog.yaml)（T04-04 acceptance L5177–5181） | `f16309beadf5ae4f28d5fc7428a2348bea0cf08d155d57730a4d817cfcdd3e96` |
| [来源登记](../../sources/registry.yaml)（T04-04 新登记 L5070–5097） | `d83aac2cfb869f1b83d7715b8761101ed18515a305b9fd1573fedca931fb977a` |
| [04 索引](../../knowledge/04-data-storage/index.md)（工作区已改，旁证用） | `eaa61dc35280474bad0e37fd98e4b29b3bbc6cc07f64cd6c01e2e946333841fc` |

正文 `related_ids` 的五个 ID 和 `source_refs` 的七个 ID 都能解析到已有文件或登记项。

## 一次源取证（审阅者独立获取）

全部用 `curl` 只读获取，使用默认 TLS 校验；除注明外 HTTP 均为 200。HTML 去标签后按文字核对，不只判可达性。原文只存在临时目录 `/tmp/b20rev/`，未入库。

| 来源（登记 ID） | URL（最终） | SHA-256（原文） | 核对点与结果 |
|---|---|---|---|
| hub tag（src.hf.huggingface-hub-v0.33.0） | GitHub API `git/ref/tags/v0.33.0` → `git/tags/feaa503a…` | `13d85917…`（ref JSON） | v0.33.0 是 **annotated tag**，tag 对象为 `feaa503a4d6b0746918afa424e9050444aae4db8`，指向 commit `d5dff4efd9187cc5c56246f416d666ea1f808cb0`。与登记"所指 commit d5dff4ef"一致。 |
| hub LICENSE（同上） | [LICENSE@v0.33.0](https://github.com/huggingface/huggingface_hub/blob/v0.33.0/LICENSE) | `c71d239df91726fc519c6eb72d318ec65820627232b2f796219e87dcf35d0ab4` | Apache License 2.0 全文，与登记一致。 |
| hub 下载指南，**未版本化**（正文 L44 所引） | [en/guides/download](https://huggingface.co/docs/huggingface_hub/en/guides/download) | `cead89234c77da73972ca2be8dff2bc4def9df2ac3d85f82f7f4e2360af1ef79` | 文档版本菜单首项为 `main v2.2.0 …`。页面含 `dry_run=True`（返回 `DryRunFileInfo`），v0.33.0 页无此项。说明该 URL 是 latest，不是 v0.33.0。→ C23 |
| hub 下载指南 **v0.33.0** | [v0.33.0/en/guides/download](https://huggingface.co/docs/huggingface_hub/v0.33.0/en/guides/download) | `c94330fed5e22270043bd71d79c77f1adef19a785cb47e0db5b2628290ff111a` | 横幅为 "You are viewing v0.33.0 version. A newer version v2.2.0…"。`revision` 可取 branch、tag、`refs/pr/N` 或 commit hash，且 "it must be the full-length hash"。`snapshot_download()` "downloads an entire repository at a given revision"，内部调用 `hf_hub_download()`，并发下载。`local_dir` 下建 `.cache/huggingface/` 元数据。页内 resume、etag、incomplete、interrupt 均 0 次命中，与作者"指南页未写续传"一致；但实现有明文（下行）。→ C23/C24 |
| hub `file_download.py`@d5dff4ef | [file_download.py](https://github.com/huggingface/huggingface_hub/blob/d5dff4efd9187cc5c56246f416d666ea1f808cb0/src/huggingface_hub/file_download.py) | `a973d1986453bf5a8003f43053b08762eb05182304df6a31d7243a5fadbfe4ef` | L232–234：缓存基于 ETag，"its git-sha1 if stored in git, or its sha256 if stored in git-lfs"。L343–525 `http_get`：`resume_size>0` 时发 `Range` 头（L406–407）；遇 ConnectionError/ReadTimeout 时 "try to resume the download a few times"，最多 5 次（L500–517）；结束时只做**长度**比对，失败报 "Consistency check failed: file should be of size …"（L444–445、L485、L522）。L942–947：`resume_download` 已弃用，"Downloads always resume when possible"。L1122 blob 以 etag 命名；L1160–1163 在 `WeakFileLock` 下写 `blob_path + ".incomplete"`。L1655–1735 `_download_to_tmp_and_move`：force_download 或 hf_transfer 时删除 incomplete（L1684–1693），检查两侧磁盘空间（L1701–1704），下载完成后 `_chmod_and_move`。L1776 用 `shutil.move(..., copy_function=_copy_no_matter_what)`。全文无 `hashlib`，无 `fsync`。→ C24/C25/C28 |
| hub `_snapshot_download.py`@d5dff4ef | [_snapshot_download.py](https://github.com/huggingface/huggingface_hub/blob/d5dff4efd9187cc5c56246f416d666ea1f808cb0/src/huggingface_hub/_snapshot_download.py) | `e9747acff05654fe3ce29517ea1cd7f0982ca88aca30518306a4fdeea02b3d2e` | L165 `repo_info(revision=revision)`。L283 `commit_hash = repo_info.sha`。L305 各文件以 `revision=commit_hash` 下载。仓库文件数超过 50 000 时，L264–267 改用 `list_repo_tree(..., revision=revision)` 取文件列表：列表按原 revision 取，下载按 commit 取。→ C24 |
| hub `tests/test_file_download.py`@d5dff4ef | [test_file_download.py](https://github.com/huggingface/huggingface_hub/blob/d5dff4efd9187cc5c56246f416d666ea1f808cb0/tests/test_file_download.py) | `f19f048c88a5840b60adc883991d0220da1a5cbe46f0e51e72d8e497c34f68bc` | L514、L536 `test_file_consistency_check_fails_{regular,LFS}_file`：mock 错误长度，断言 `EnvironmentError`。L798–804 `test_resume_from_incomplete`：先在 `.incomplete` 写入伪数据 `"XXXX"`，再续传，期望结果为 `"XXXXent"`。注意 L804 是裸比较表达式，缺 `assert`。L806 `test_do_not_resume_on_force_download`。→ C24/C28 |
| safetensors tag（src.hf.safetensors-v0.7.0） | 登记 `huggingface/safetensors` 的 API 返回 **301**，重定向到 `safetensors/safetensors` | `e88f289c…`（301 JSON） | 跟随重定向后，v0.7.0 是 lightweight tag，直接指向 commit `fa27fa835a466cb50d07696ec20b94f46aed0e31`，与登记一致。仓库已迁到 `safetensors/safetensors` 组织。→ C31 |
| safetensors LICENSE | [LICENSE@v0.7.0](https://github.com/huggingface/safetensors/blob/v0.7.0/LICENSE) | `c71d239df91726fc519c6eb72d318ec65820627232b2f796219e87dcf35d0ab4` | Apache License 2.0 全文，与 hub 的 LICENSE 字节相同，与登记一致。 |
| safetensors README@v0.7.0 | [README.md](https://github.com/safetensors/safetensors/blob/v0.7.0/README.md) | `e430910cef3bfc36f06c236f25685dc6734ea9a50c5432d890f8b4fff05696e1` | §Format（L76–106）：8 字节 N（u64 LE），然后是 N 字节 JSON header（MUST 以 `{` 开头）。header 每项只有 `dtype`、`shape`、`data_offsets`，外加可选 `__metadata__`（只允许字符串到字符串）。**`data_offsets` "relative to the beginning of the byte buffer"**，指的是本文件内部的偏移。Notes 写明："Duplicate keys are disallowed. Not all parsers may respect this"；"Tensor values are not checked against, in particular NaN and +/-Inf could be in the file"；"The byte buffer needs to be entirely indexed, and cannot contain holes"。L172–174 header 上限为 100MB。全节没有校验和字段，也没有跨文件或分片索引。→ C22/C29/C31 |
| safetensors `safetensors/src/tensor.rs`@fa27fa83 | [tensor.rs](https://github.com/safetensors/safetensors/blob/fa27fa835a466cb50d07696ec20b94f46aed0e31/safetensors/src/tensor.rs) | `f94ad16fd2286b46d2608c764ce7afe31b7c29d25c71ded564bcd0fbd0580ea0` | L10 `MAX_HEADER_SIZE = 100_000_000`。错误枚举包括 `InvalidHeaderStart`、`InvalidHeaderDeserialization`、`HeaderTooLarge`、`InvalidOffset`、`MetadataIncompleteBuffer`（L20–45，消息见 L73–91）。L389 返回 `MetadataIncompleteBuffer`。这些是格式检查的精确失败点。→ C28/C29 |
| PyPI JSON | `pypi.org/pypi/{huggingface_hub,safetensors}/json` | — | 取证时 latest 分别为 huggingface_hub **2.2.0**、safetensors **0.8.0**。两个样板都不是最新版；来源记录"PyPI 最新版交叉核对"没有说明为何选这两个版本。→ C23 |

取证限制：只核对上述文件与行，未克隆仓库，未跑测试，也未找 safetensors 的读写测试文件。`hf_xet`/Xet 下载路径（`xet_get`）只看到调用点，没有核对实现。transformers 的 `model.safetensors.index.json` 约定本轮未取一次源。T04-02/03 的内容按本库现行草稿核对，未重新取其一次源。

## 发现

### B20-C22 — P1 / OPEN：分片关联写成 safetensors header 的 `data_offsets`，与原文不符

位置：正文 §1 L45；登记 L5097（"制品分片清单以 header 的 data_offsets 为准"）。

证据：README §Format 写明 `data_offsets` 指的是 "relative to the beginning of the byte buffer"，即**单文件内**张量的字节区间。格式里没有任何跨文件或分片的字段。多分片模型靠哪个文件把张量名映射到分片文件（常见做法是 transformers 的 `*.safetensors.index.json` / `weight_map`），正文没有写，也没有登记来源。acceptance 1 要求"必要分片/索引关联"，所以这一项实际缺失，而且现有表述会误导读者：读者会以为分片完整性可以从 header 推出。

另外，"来源与配置"只写了下载参数。制品集合里的 config、tokenizer 等非张量文件是否列入清单，以及按什么 SHA-256 列入，正文没有交代。

关闭条件：

- 把 `data_offsets` 改为"单文件内张量区间，用于格式检查"。
- 分片到文件的索引关联要么引用固定版本的一次源（例如 transformers 某 tag 的 index 文件写入/读取实现），要么明确记为本库设计约定，或记为 unknown。
- 清单补上"集合成员"字段，覆盖全部张量与非张量文件，并标明每个文件的长度和 SHA-256。
- 同步修订登记 L5097。

### B20-C23 — P1 / OPEN：hub 下载指南引用的是 latest（v2.2.0）页面，不是 v0.33.0

位置：正文 L44、L32 notes；来源记录 L3、L9；登记 L5075。

证据：正文所引 `…/en/guides/download` 的版本菜单首项为 `main v2.2.0`，页面还有 v0.33.0 没有的 `dry_run`。v0.33.0 有独立页面（`…/v0.33.0/en/guides/download`），横幅自述 v0.33.0。PyPI 取证时 latest 是 2.2.0，不是 0.33.0。正文以 v0.33.0 为样板，"已核对下载指南"却核对的是另一个大版本的文档。这是 T04-03 C11/C12 同类问题（latest 不能证明固定版本的行为）。

关闭条件：

- 正文、来源记录、登记三处统一改为 v0.33.0 版本化页面，并按该页重核 revision、snapshot_download 和缓存条目。
- 来源记录说明为何选 v0.33.0（以及 safetensors 0.7.0）而不是 latest，并写明不外推到 1.x/2.x。

### B20-C24 — P1 / OPEN：hub"续传 unknown""重试整个文件"与固定实现相反；没有把"下载成功≠内容一致"落到实现层

位置：正文 L55、L65、L78；来源记录 L9、L15 第 2 项；登记 L5083。

证据（file_download.py@d5dff4ef）：

- 续传有明文。默认总是续传（L942–947）：在 `.incomplete` 上追加写，用 `Range` 头续传（L406–407、L1695–1696）；网络错误最多续传 5 次（L500–517）。只有 force_download 或 hf_transfer 时才删除 incomplete，从头下载（L1684–1693）。正文"重试整个文件/分片"不是 v0.33.0 的默认行为。
- 下载完成的判据只有长度（L444–445、L485、L522），全文没有 `hashlib`。上游测试 L798–804 正好说明了后果：`.incomplete` 里的伪前缀 `"XXXX"` 被保留在最终文件中（期望 `"XXXXent"`）。所以 `hf_hub_download` 正常返回，并不说明内容与远端一致。这正是 acceptance 1"下载成功不等于版本一致"在实现层的反例，正文却记为 unknown。
- LFS 文件的 ETag 是 sha256（L232–234），blob 以 etag 命名（L1122），但本地不重算。hub 的 ETag 与 RGW 的 ETag 语义不同，正文 L57 只讨论了 RGW，不能互推。
- 版本：`snapshot_download` 先把 revision 解析为 `repo_info.sha`，再按该 commit 下载所有文件（L283、L305）。因此清单应记录**解析出的 40 位 commit**，不能只记 branch 或 tag。超过 50 000 个文件时，文件列表按原 revision 取（L264–267），存在"列表与内容来自不同 commit"的窗口，正文"读到旧/混合版本"一行没有覆盖这种情况。

关闭条件：

- §2"传输"行与 §3"传输中断"行按上述行号改写：续传机制、长度检查、无内容哈希。
- 清单"版本"字段改为"解析后的完整 commit hash（并记录请求的 revision）"。
- 读回验证明确要求：下载后在本地重算 SHA-256，与发布方清单比对，LFS ETag 只作为远端声称值。
- 补上 >50 000 文件时的混合版本窗口，或注明不适用的条件。
- unknown 清单删除"hub 续传"。

### B20-C25 — P1 / OPEN：本地与 NFS 合为一栏，NFS 提交条件缺失；fsync 与 rename 的次序写反；交叉引用错位

位置：正文 §2 L52–59。

证据：

- acceptance 2 要求"分别给出本地/NFS 文件暂存与 rename/fsync 条件 … 逐实现核对"。正文只有一栏"本地/NFS 文件暂存"。T04-02 已有 NFS 专属条件：UNSTABLE WRITE 须 COMMIT 并比对 write verifier（[local-and-shared-storage](../../knowledge/04-data-storage/local-and-shared-storage.md) L86）；可见性不等于持久性（[local-and-shared-storage](../../knowledge/04-data-storage/local-and-shared-storage.md) L92）；NFS 发布要求 `hard` 挂载、导出 `sync`、close/fsync 时检查错误、rename 后复核重传误报（[local-and-shared-storage](../../knowledge/04-data-storage/local-and-shared-storage.md) L100）。T04-04 一项都没有引入。
- L54 写"写临时名＋fsync 文件/目录后 rename"，即目录 fsync 发生在 rename 之前。要让 rename 产生的新目录项落盘，目录 fsync 必须在 rename **之后**（fsync(2) 写明目录项需要对目录显式 fsync；T04-02 L72 写的是"持久性仍需文件＋目录 fsync"）。这里的次序是审阅者依据 fsync(2) 语义推出的，正文应写出明确次序并引用来源。
- L59 写"T04-03 UNSTABLE/COMMIT"，但 UNSTABLE/COMMIT 在 T04-02 §3，T04-03 讲的是对象与 Lustre。
- hub 自己的提交步骤是 `shutil.move`，没有 fsync（L1735、L1776）。跨卷时会退化为复制（`_copy_no_matter_what`），不是原子 rename（docstring L1678 要求同卷）。所以 hub 缓存目录本身不能当作已持久发布的位置，正文也没有说明。

关闭条件：

- §2 拆为本地 ext4、NFSv4.1、RGW 三栏，NFS 栏按 T04-02 L86/L92/L100 写出条件，并给出可点击链接。
- 写明"写临时文件 → fsync(文件) → rename → fsync(目录)"的次序，引用 fsync(2)/rename(2) 登记。
- 修正 L59 的归属。
- 说明 hub 下载落地（move，无 fsync，跨卷时为复制）与本库发布提交之间的边界。

### B20-C26 — P1 / OPEN：多文件制品的提交点只按单文件或单对象定义，没有集合级原子发布条件

位置：正文 §2 L56，§3 L66–67。

证据：L56 写"rename 即提交点；提交后列清单"和"Complete 即提交点"。rename(2) 只保证单个 newpath 的原子替换，multipart Complete 只组装单个对象（T04-03 L53）。模型或 checkpoint 是多分片、多文件的集合，逐文件 rename 或逐对象 Complete 期间，读者可能看到新旧混合的集合。acceptance 2 点名"清单发布条件"，acceptance 3 点名"混合版本"，但正文没有给出集合级提交点：例如先写全部成员，最后发布清单或指针（文件侧用 rename 指针文件或目录，对象侧最后 PUT 清单对象），读者先读清单再按清单取成员。"提交后列清单"的次序也没有说明清单是提交点还是事后记录。

关闭条件：

- 两个分支各自写出集合级提交点、发布次序和读者协议（先清单后成员，成员哈希不符即失败）。
- 说明文件侧目录 rename 的条件（同文件系统、目标不存在或为空目录，以 rename(2) 为准），以及对象侧没有多对象原子性（以 Squid 文档为准，未写明则记 unknown）。
- 设计约定与上游保证分开标注。

### B20-C27 — P2 / OPEN：RGW versionId 用作版本字段和部分发布判据，但 T04-03 记为无法获取

位置：正文 L44、L66（"版本号未推进"）、L67（"版本化三态为准"）。

证据：T04-03 L84 写明 versionId 的获取位置 Squid 文档没有给出（Complete 响应只有 Location/Bucket/Key/ETag），未启用版本化或 Suspended 的 bucket 身份要加内容哈希。T04-04 把 versionId 当作现成的清单字段，并把"版本号未推进"作为部分发布的判据，既没有来源，也和 T04-03 的 unknown 矛盾。"版本化三态为准"没有说明三态各自怎样判定旧版本或混合版本。

关闭条件：

- 版本字段按 T04-03 L84 的身份分支改写（Enabled 且可获得 versionId / 其他情况用 key＋SHA-256）。
- 删除"版本号未推进"，或给出来源。
- 旧版本、混合版本的判定按三态分别写，并链接 T04-03 §5。

### B20-C28 — P1 / OPEN：acceptance 4 未满足——没有任何阶段计时和失败点，且声称上游实现与测试"未定位"

位置：正文 §4 L71–73；verification notes L32；来源记录 L15 第 1、3 项。

证据：§4 全文只写了"未定位（unknown），定位后按四阶段记录"。本轮已在固定 commit 上定位到可用的上游实现和测试（见一次源表）：

- 下载阶段：`_download_to_tmp_and_move` 依次为磁盘空间检查 → `.incomplete` 追加写 → `http_get` 续传与重试 → 长度一致性检查 → chmod 与 move（L1655–1735）。失败点有空间不足（L784–801）、超过重试次数（L505–507）、"Consistency check failed"（L444–445）。
- 测试：L514、L536（长度不符时报错）、L798–806（续传与 force_download 不续传）。
- 格式检查阶段：safetensors `tensor.rs` 的 `HeaderTooLarge`、`InvalidHeaderStart`、`InvalidOffset`、`MetadataIncompleteBuffer` 等（L20–45、L389）。

acceptance 要求"以精确上游实现/测试为例记录阶段计时与失败点"。上述位置可以给出阶段边界（在哪里打点）和失败点，不需要编造计时数据。

关闭条件：

- §4 按"解析 revision → 下载/续传 → 长度检查 → 落地 move → 本库 SHA-256 校验 → 格式检查 → 提交 → 读回"列出每个阶段的上游代码或测试锚点、可观测的计时起止点和失败信号。
- 计时值一律记为"未执行"。
- 注明上游测试 L804 缺 `assert`，因此它不能证明续传内容正确，只能作为行为样例。
- 没有找到 safetensors 读写测试的，保留 unknown 并写明检索范围。

### B20-C29 — P2 / OPEN：三类门槛中格式门过窄、正确性门没有门槛；重试与清理没有可执行条件

位置：正文 §2 L57、§3 L68–69。

证据：

- 格式检查只写了"header 可解析性"。README 和 tensor.rs 给出了可直接用作门槛的条件：首字符 `{`、header ≤100MB、offset 合法、字节区完整覆盖且无空洞（`MetadataIncompleteBuffer`）、键不重复（README 注明"Not all parsers may respect this"，因此依赖解析器）。README 还写明"Tensor values are not checked against … NaN and +/-Inf could be in the file"，所以格式检查通过不代表数值有效，这一点应当写入，作为格式门与正确性门的分界。
- acceptance 3 要求三者"分别有门槛"。正确性门写成"归引擎，不在本页"，没有给出任何通过条件，也没有指向负责的主文或任务。
- "幂等重试＋孤儿清理"没有对象：文件侧未写 `.incomplete` 残留与 force_download 删除（L1684–1693）、临时名与锁文件；对象侧未写按 List Bucket Multipart Uploads 找残留、再 Abort（T04-03 L53、L89）。

关闭条件：

- 格式门列出上述条件并给出锚点。
- 正确性门至少写出最低通过条件的形式（例如固定输入下与参考输出比对、容差由谁定），以及归属任务（T07-01）。缺失的部分声明为 unknown。
- 重试与清理按文件侧、对象侧分别列出残留物、发现方法和清理操作。

### B20-C30 — P2 / OPEN：durability/integrity 主文没有链接；推理加载链接归到错误任务

位置：正文 L48、L69、L73、L77。

证据：

- acceptance 4 要求"链接 checkpoint-durability/integrity 和推理加载主文"。正文只写"见完整性证据主文"，没有 Markdown 链接，全文也没有提到 checkpoint-durability。它们只出现在 frontmatter `related_ids`，AGENTS.md 要求用普通 Markdown 链接。T04-02/03 也只以任务号引用，没有链接。
- L73 写推理加载"链接待 T04-05 后补全"。T04-05 是"扩展数据、制品与后端完整性校验证据"（backlog L5204–5205，concept/revise），不是推理加载。推理加载对应的是 T07-01"权重加载、引擎 ready 与启动失败诊断"（backlog L6201，batch 26）和主题 07.1。

关闭条件：

- 正文加 [checkpoint-durability](../../knowledge/04-data-storage/checkpoint-durability.md)、[checkpoint-integrity-evidence](../../knowledge/04-data-storage/checkpoint-integrity-evidence.md)、[local-and-shared-storage](../../knowledge/04-data-storage/local-and-shared-storage.md)、[object-and-parallel-storage](../../knowledge/04-data-storage/object-and-parallel-storage.md) 的相对链接，并精确到节。
- 推理加载改为"T07-01（batch 26）未交付，暂链 [07 索引](../../knowledge/07-inference/index.md) 或声明缺失"。

### B20-C31 — P3 / OPEN：元数据、登记与来源记录的若干记载不准确

位置：正文 L8–16、L28–32、L48；登记 L5086、L5097；来源记录 L3、L7–15。

证据：

- `source_refs` 列出了 `src.pytorch.dcp-2.6`、`src.ascend.mindio-acp-v26.1.1`，正文却没有任何主张使用它们。fsync、rename、Ceph 三项也只间接通过 T04-02/03 使用，没有在本页就近引用。
- `verification.status: source_checked` 早于审阅关闭（与 T04-03 C20 同类问题），而且 notes 所称的"已核对下载指南"指向 latest 页面（C23）。
- safetensors 登记 URL `github.com/huggingface/safetensors` 已重定向到 `safetensors/safetensors`（API 返回 301）。
- 正文 L48"自带校验和未在 README 见到（unknown）"可以写得更确定：§Format 定义的 header 字段只有 dtype、shape、data_offsets 和 `__metadata__`，格式本身没有校验和字段。不过，库实现或外部工具是否另有校验，仍记 unknown。
- 来源记录没有取证日期、原文 SHA 和行号，后续复核无法比对。

关闭条件：

- 删除不用的 source_refs，或补上就近引用。
- verification 状态在定向复核通过后再升级。
- 登记 URL 更新为 `safetensors/safetensors`，或注明重定向。
- L48 按格式定义改写。
- 来源记录补取证日期、页面与文件的 SHA-256 及行号（可参照本报告的一次源表）。

## 对照 acceptance 汇总

| acceptance | 判定 | 阻断发现 |
|---|---|---|
| 1 清单字段齐全；下载成功≠版本一致/ready | 未满足：分片关联错误，版本记 branch 级，"下载成功≠一致"没有落到实现层 | C22（P1）、C23（P1）、C24（P1） |
| 2 本地/NFS rename/fsync 与 RGW multipart/清单条件逐实现核对 | 未满足：NFS 缺栏，fsync 次序错，没有集合级提交点 | C25（P1）、C26（P1）、C27（P2） |
| 3 中断/部分/旧/混合/重试/清理；三类门槛分开 | 部分满足：行目齐全，但续传、混合版本、清理与正确性门不成立或为空 | C24、C26（P1）、C29（P2） |
| 4 上游实现/测试阶段计时与失败点；链接 durability/integrity/推理加载 | 未满足：§4 为空，链接缺失或指向错误任务 | C28（P1）、C30（P2） |

## 结论

**T04-04 未通过初审。新增 B20-C22–C31 共 10 项，全部 OPEN：P1 六项（C22、C23、C24、C25、C26、C28），P2 三项（C27、C29、C30），P3 一项（C31）。** P1 与 P2 全部关闭前，不得声明审阅通过。修订后需要按发现 ID 做定向复核。

正文的方向是对的："下载成功≠ready"、ETag 不作内容哈希、未执行不标结果、后端承诺复用 T04-02/03 而不重复论证。主要问题有三处：

1. 固定版本的实现已有明文，正文却记为 unknown，或与实现相反（C24、C28）。
2. 关键证据落在错误的版本或语义层：指南用的是 latest 页面，`data_offsets` 被当作分片关联（C22、C23）。
3. 发布协议停在单文件、单对象层，NFS 与集合级提交条件缺失（C25、C26）。

本报告只覆盖编辑与来源层面，不构成硬件、部署或现场验证。
