# 第二十批 T04-04 第二次定向复核（作者第二轮修订后）

复核日期：2026-10-13（实际取证日）。审阅模型 `claude-opus-5-5`，由用户本次明确要求。这不是既有的 `gpt-6.1-sol / xhigh` 批量审阅约定，也不改写该约定；推理等级等运行元数据没有可核验记录，不补造。审阅者角色独立于作者修订角色。

**结论：T04-04 第二次定向复核未通过。本轮范围 9 项（C22–C27、C29–C31）：CLOSED 3（C22、C23、C27），OPEN 6（C24、C25、C26、C29、C30、C31）。连同前次已关闭、本轮不重开的 C28，B20-C22–C31 合计 CLOSED 4 / OPEN 6。** 唯一的实质缺口在 C24：L35 的 hub 断言仍是无条件表述，RGW"传输"栏仍写"同左"，新增的 Xet 锚点 L618 指错了行。其余 5 项只剩引用、标注和清理条目层面的残缺，每项都是一两处局部改动。不新增发现 ID。

本轮只做只读核对：未改作者正文、来源记录、修订映射、登记或计划；未下载模型，未上传或发布对象，未执行读写、中断或计时试验。模型审阅不构成硬件或现场验证。

## 输入（以 SHA-256 识别）

| 输入 | SHA-256 | 与任务给定前缀 |
|---|---|---|
| [T04-04 正文](../../knowledge/04-data-storage/artifact-transfer-and-publication.md)（97 行，procedure / draft） | `4fe1708603ac1621…` | 一致 |
| [作者来源记录](batch-20-t04-04-sources.md)（17 行） | `90bd15d2ca38d882…` | 一致 |
| [修订映射](batch-20-review-fixes.md)（T04-04 第二轮节 L110–121、L123–133） | `0e36ac65d8202964…` | 一致 |
| [前次复核报告](batch-20-t04-04-claude-recheck.md)（剩余关闭条件权威来源） | `9fc6157b1f2cbbee633371343cb8109cb819d05e5df39eaf3f839d781150bdc7` | — |
| [任务计划](../../plans/full-coverage-backlog.yaml)（T04-04 acceptance 4 条） | `f16309beadf5ae4f28d5fc7428a2348bea0cf08d155d57730a4d817cfcdd3e96` | 与前次复核相同，未变 |
| [来源登记](../../sources/registry.yaml)（409 项；T04-04 两项 L5070–5097） | `6ee7da221df2e067…` | 一致 |

`make check`：`PASS: 91 content entries; 409 sources.` 只校验结构与本地链接，不校验技术正确性和远端链接。

## 一次源重取（审阅者独立获取）

用 `curl` 默认 TLS 只读获取，原文只存放在 `/tmp/b20rc2/`，未入库。

| 来源 | SHA-256 | 核对结果 |
|---|---|---|
| hub `file_download.py`@d5dff4ef（1803 行） | `a973d198…bfe4ef` | 与前次和作者记录一致。L530 是 `def xet_get`；L600–603 的 `PyXetDownloadInfo(..., hash=xet_file_data.file_hash, ...)` 是传哈希的位置；L627–633 是 `download_files(...)` 调用；L1708–1710 是 Xet 分支条件与 `xet_get` 调用；L1725–1732 是 `http_get` 分支（传 `resume_size`）。**L618 是进度条参数 `name="huggingface_hub.xet_get"`，与"向外部包传文件哈希"无关。** → C24 |
| hub `setup.py`@d5dff4ef（161 行） | `27aa7974…181722` | 与作者记录前缀一致。L17 为 `hf-xet>=1.1.2,<2.0.0`，平台条件 x86_64/amd64/arm64/aarch64，正文 L56 表述正确。 |
| hub `_snapshot_download.py`@d5dff4ef | `e9747acf…b3d2e` | 一致。L264–267（>50 000 文件按原 revision 列表）、L283（`commit_hash = repo_info.sha`）、L305（按 commit 下载）无误。作者记录前缀写成 7 位 `e9747ac`，记录自述为"前缀 8 位"，属笔误。 |
| hub `tests/test_file_download.py`@d5dff4ef | `f19f048c…f68bc` | 一致。 |
| safetensors `tensor.rs`@fa27fa83 | `f94ad16f…80ea0` | 一致。正文 L72 锚点 L10（`MAX_HEADER_SIZE`）、L20–45（错误枚举 InvalidHeaderStart…MetadataIncompleteBuffer）、L73–91（Display 文案）、L389（`MetadataIncompleteBuffer` 返回）逐行无误。 |
| safetensors README@v0.7.0 | `e430910c…5e1696e1` | 一致。L83 data_offsets 原文、L89"Duplicate keys are disallowed. Not all parsers may respect this."、L94 NaN/±Inf 未检查、L101 无空洞、L174 100MB。 |
| hub 下载指南 v0.33.0 版页 | `910396c8…`（动态渲染，与作者 `fcb88d5f`、前次 `f956ec22` 均不同，按文字核对） | 去标签后："You are viewing" 1 次、"full-length hash" 1 次、"entire repository at a given revision" 1 次、`dry_run` 0 次，与正文 L45、登记 L5075 一致。 |
| `github.com/safetensors/safetensors/blob/v0.7.0/README.md` | — | HTTP 200（正文 L44 链接可达）。 |

取证限制：

- hf_xet（外部 Rust 包）的续传、重试和哈希校验实现未核对，仍为 unknown。
- 未克隆仓库，未跑测试，未经 GitHub API 重做 tag→commit 解析；本轮按 commit SHA 取原文，字节与前两轮一致。
- fsync(2)、rename(2)、Ceph 页面本轮未重取，只核对登记 ID 存在（L322、L4951、L4995），以及正文 L53 的 man7 链接与登记 URL 一致。

## 逐项复核

### B20-C22 — P1 / **CLOSED**

- 登记 `src.hf.safetensors-v0.7.0` 的 notes（L5097）已改写为"data_offsets 为单文件内张量区间（README 原文），跨文件分片索引关联未取源（unknown）；……格式本身无校验和字段"，与同条目 revision（L5089）、正文 L44/L47 一致。前次剩余条件已满足。
- 正文 L41（集合成员＋每文件长度与 SHA-256，标为"本库清单要求"）、L44（单文件区间，引文对 README L83）保持正确。

### B20-C23 — P1 / **CLOSED**

- 来源记录 L13 已补选版理由："v0.33.0/0.7.0 为取证时已发布一段时间的固定版本（非最新……），结论不外推到 1.x/2.x"，与正文 L47 一致。目标环境与样板的对应关系由正文 frontmatter `applicability.notes`（L24，"目标环境的……版本……需另行固定"）承接。
- 不阻断：理由只说明"非最新"，没有说明"为何是这两个版本"（例如与某个目标环境锁定的版本对应）。现有表述没有声称这种对应，不构成事实错误。

### B20-C24 — P1 / **OPEN**（Xet 例外行已加；限定仍不完整，新锚点有误）

- 已满足：
  - L55"传输"行限定为"plain HTTP 路径；Xet 例外见下行"。
  - 新增 L56"Xet 路径例外"行写明 setup.py L17 的默认安装条件、L1708 的分支条件（有 Xet 元数据且可用时走 `xet_get`），以及该路径不传 `resume_size`、跳过 5 次重试和长度检查。NFS 栏写明 Xet 行为 unknown。上述内容逐行核对无误。
  - 登记 hub notes（L5083）已加"plain HTTP 路径"限定。
  - L71"下载后本地重算 SHA-256"不分分支，满足"两个分支共同读回要求"。
- 未满足：
  1. **L35 仍是无条件断言**："hub 下载完成判据只有长度（无内容哈希），见 §2"。前次条件 1 点名了 L35。在默认安装、Xet 存储的仓库上，这句话没有依据：L1708 分支不经过长度检查，hf_xet 是否按 `file_hash` 校验内容仍为 unknown。
  2. **RGW 栏"传输"（L55）仍写"同左＋RGW multipart/版本化条件"**。前次条件 3 要求改为上传方向的表述。向 RGW 发布是上传，"同左"把 hub 下载的续传、重试和长度判据带进了上传方向。
  3. **新锚点 L618 有误**：L56 写"file_download.py L530/618/1708-1710"，用来支持"向外部包传文件哈希"。L618 实为进度条参数 `name="huggingface_hub.xet_get"`。传哈希在 L600–603（`PyXetDownloadInfo(... hash=xet_file_data.file_hash ...)`），交给外部包在 L627–633（`download_files(...)`）。
  4. L80（§4"下载/续传"行）计时起止写了 `http_get`，隐含了分支限定，但失败信号"超过 5 次重试"没有注明只适用于 HTTP 分支。建议与第 1 条一并加注；单独不阻断。
- 剩余关闭条件：L35 加"plain HTTP 路径；Xet 路径见 §2 例外行（unknown）"一类限定；RGW 栏"传输"改为上传方向表述，例如"multipart 上传；中断后按 List uploads 找残留再 Abort（见 T04-03 §2）"，并删除"同左"；L56 锚点 L618 改为 L600–603/L627–633。

### B20-C25 — P1 / **OPEN**（就近引用已加一处；NFS 节号仍不完整）

- 已满足：L53 本地栏的次序"写临时名 → fsync(文件) → rename → fsync(目录)"已就近链接 fsync(2) 和 rename(2) 的 man7 页，URL 与登记 L322/L4951 一致。hub 落地边界（L58）保持正确。
- 未满足：
  1. NFS 栏（L54）只引"本地与共享存储 §4 选型表发布行"。前次条件是"§3、§4"。§4 发布行（T04-02 L100）覆盖了 `hard`、导出 `sync`、fsync/close 查错、rename 后复核、UNSTABLE 未 COMMIT 和 verifier，但"可见性≠持久性"只在 §3（T04-02 L91）。write verifier 的协议出处（RFC §18.32）也在 §3（L86）。只引 §4，L54 的部分主张就失去了出处。
  2. L57"以 rename(2) 为准"没有就近链接。同表 L53 已有链接，因此这一条的影响较小，但前次条件点名了此处。
- 剩余关闭条件：L54 改为"见本地与共享存储 §3、§4"（或分别标注各条主张对应的节）；L57 的"rename(2)"加链接。

### B20-C26 — P1 / **OPEN**（设计约定已标注；上游语义缺来源）

- 已满足：L57 两处集合级提交点分别标为"本库设计，非上游保证"和"本库设计"，与单文件 rename、单对象 Complete 区分开。读者协议、目录 rename 条件和对象侧无多对象原子性（unknown）保持不变。修订映射所述现在与正文相符。
- 未满足：前次条件要求"单文件 rename、单对象 Complete 标为上游语义（附来源）"。rename 一侧可由 L53 的链接承接（同 C25 第 2 条）。"Complete 即单对象提交点"没有任何就近来源：RGW 栏全文没有 Ceph 文档链接，也没有链接 T04-03 中对应的行。
- 剩余关闭条件：L57 的 RGW 栏"Complete 即单对象提交点"附上来源，可以是登记 `src.ceph.docs-rgw-s3-squid` 的 objectops 页，或链接 [对象与并行存储 §2](../../knowledge/04-data-storage/object-and-parallel-storage.md) 的 multipart 行。这一处同时满足 C31 第 3 条。

### B20-C27 — P2 / **CLOSED**

- L69 已按三态写出旧版本和混合版本的判定：Enabled 时用 versionId（可获得时）＋清单；Suspended 或从未设置时以内容哈希为准；revision 制品用解析出的 commit（>50k 窗口除外）。判定方法链接到 [T04-03 §5](../../knowledge/04-data-storage/object-and-parallel-storage.md)。与 T04-03 L51（三态定义）、L84（身份分支）、L88（对象发布判据）一致。
- 不阻断：L69 没有写明"Enabled 但无法获得 versionId"的情况。L61 已写"Enabled 且可获得 versionId / 其他用 key＋SHA-256"，两处合读没有缺口。T04-03 L84 的身份是"bucket＋key＋内容哈希"，L69 只写"内容哈希"，建议补上 key。链接只到文件，§5 写在链接文字里，可以接受。

### B20-C29 — P2 / **OPEN**（残留类别已列出；方法状态、锁文件 unknown 和 README 锚点缺失）

- 已满足：L70"重试与清理"列出了文件侧残留 `.incomplete`、临时名和锁文件，发现方法为"缓存/暂存目录扫描后按清单比对清理"；对象侧残留为 in-progress multipart（List 后 Abort）。格式门（L72）和正确性门（L73）保持正确，tensor.rs 锚点逐行无误。
- 未满足：
  1. L70 的扫描和清理方法没有标注"方法设计，未执行"。L67 对 `.incomplete` 有此标注，L70 新增的临时名和锁文件没有。
  2. 前次条件要求"锁文件清理条件不明的记 unknown"。L70 把锁文件与其他残留一样写成"按清单比对清理"。hub 用 `WeakFileLock`（file_download.py L1160 一带）保护并发下载；删除仍被其他进程持有的锁文件，安全条件没有取源。目前正文写成了可以照做的操作，没有标 unknown。
  3. L72 的"键不重复（解析器未必遵守）"和"NaN/±Inf 可存在于文件"出自 README L89/L94，但该行只链接 tensor.rs，README 锚点没有补。
- 剩余关闭条件：L70 标注"方法设计，未执行"；锁文件清理的安全条件（持有者是否存活、是否有并发下载）记为 unknown，或写明"仅在无并发下载时清理"并标为本库约定；L72 补 [README §Format](https://github.com/safetensors/safetensors/blob/v0.7.0/README.md) 链接（L89/L94）。

### B20-C30 — P2 / **OPEN**（§5 链接已精确到节名；正文三处 T04-03 引用仍为纯文本）

- 已满足：L91 的 durability 和 integrity 链接已注明节名（"文件同步与目录记录是两个层面"、"四层校验机制与各自边界"），两节标题与目标文件 L73、L36 原文一致。T04-02 §4 和 T04-03 §2/§5 链接带节号。L69 的 T04-03 §5 已改为链接。
- 未满足：前次条件点名的正文引用中，L53 RGW 栏"见 T04-03 §2"、L68"见 T04-03 §2/§5"仍是纯文本。§4 的 L85"T04-03 §5"也是纯文本。
- 剩余关闭条件：L53、L68、L85 的 T04-03 引用改为 Markdown 链接（目标为 `object-and-parallel-storage.md`，链接文字带节号）。

### B20-C31 — P3 / **OPEN**（只剩 Ceph 就近引用与锚点笔误）

- **审阅者自我更正（前次第 1 条）**：前次要求把 `verification.status` 从 `source_checked` 回退，或等复核通过后再升级。这个要求过严。schema（`schemas/content.schema.json` L35）中该字段只取 `not_verified / source_checked / reproduced`，记录的是来源核对状态，不是编辑审阅状态。AGENTS.md 也写明"Editorial review and experimental verification are separate"，审阅是否通过由 `status: draft` 与复核记录承载。同目录已通过审阅的 T04-02、T04-03 也都是 `source_checked`。作者已实际核对来源，保留 `source_checked` 是正确的。此条视为满足。
- 已满足：
  - 第 2 条：来源记录 L13 已写出作者实开的 SHA-256 前缀（file_download、_snapshot、测试、setup、README、tensor.rs、v0.33.0 指南）。本轮核对，除动态渲染的指南页外，前缀全部与审阅者所取一致。不阻断：_snapshot 前缀只有 7 位，与"前缀 8 位"的自述不符；"一致处以复核记录为准"仍然含糊，建议改为"指南页为动态渲染，字节不可复现，按文字核对"。
  - 第 4 条：登记 L5097 已修订（见 C22）。
  - 第 3 条中的 fsync 和 rename：L53 已就近链接。
- 未满足：第 3 条中的 Ceph。`src.ceph.docs-rgw-s3-squid` 仍在 `source_refs`（L11），但正文没有任何 docs.ceph.com 链接，也没有就近指向该登记。
- 剩余关闭条件：按 C26 剩余条件，在 L57 RGW 栏为 Complete 语义补 Ceph 文档就近引用，或从 `source_refs` 删除该 ID。L56 锚点 L618 的修正见 C24。

## 不阻断追记（不新增 ID，不改变计数）

- C28（已 CLOSED，不重开）：正文 L82 写"L784–786 _check_disk_space 只 log warning"。L784–786 是函数签名和 docstring，实际的 `warnings.warn` 在 L799，走的是 Python warnings 机制，不是 logger。另外，该检查在下载前执行（L1705–1706），不在 move 阶段。登记 L5083 也写成"L784-786"。建议锚点改为 L784–801/L799，并把它移到"下载/续传"阶段。结论"空间不足不是失败点"本身正确。
- 修订映射 `batch-20-review-fixes.md` 中"T04-04 第二轮修订"出现了两次（L110 与 L123），内容大体重复，建议合并。
- 范围外观察，不计入本轮：登记 `src.linux-man-pages.rename-6.19`（L4951–4961）的 license 下有两行相同的 `notes`，条目 notes 写的是记录锁与 NFS 租约内容，与 rename(2) 不符，疑似错位。另外，正文 `updated_at` 和两项登记的 `registered_at` 都是 2026-10-14，晚于本轮取证日 2026-10-13。这些不属于 C22–C31 的关闭条件，留给作者或后续批次核查。

## 对照 acceptance

| acceptance | 判定 | 未关闭 |
|---|---|---|
| 1 清单字段；下载成功≠版本一致/ready | 基本满足；L35 hub 断言未限定 HTTP 分支 | C24（P1） |
| 2 本地/NFS/RGW 提交条件逐实现核对 | 基本满足；只剩引用层残缺（NFS 节号、Complete 来源、rename 链接），RGW 传输方向表述有误 | C24、C25、C26（P1，局部） |
| 3 中断/部分/旧/混合/重试/清理；三类门槛 | 三态判定已满足；清理条目缺方法状态和锁文件 unknown | C29（P2） |
| 4 阶段计时与失败点；链接 durability/integrity/推理加载 | 阶段表满足；正文三处 T04-03 引用未链接 | C30（P2） |

## 结论

**第二次定向复核未通过：本轮 9 项 CLOSED 3 / OPEN 6；C22–C31 合计 CLOSED 4 / OPEN 6。** 剩余工作都是局部修改：

1. **C24（P1，实质）**：L35 加分支限定；RGW 栏"传输"改为上传方向表述；L56 锚点 L618 → L600–603/L627–633。
2. **C25、C26、C31（P1/P3，引用）**：NFS 栏改引 §3、§4；L57 的 rename(2) 加链接，Complete 补 Ceph 或 T04-03 §2 来源（同时关闭 C31）。
3. **C29（P2）**：L70 标"方法设计，未执行"，锁文件清理条件记 unknown；L72 补 README 锚点。
4. **C30（P2）**：L53、L68、L85 的 T04-03 引用改为链接。

P1、P2 全部关闭前不得声明审阅通过。修订后按 ID 再做定向复核。本报告只覆盖编辑与来源层面，不构成硬件、部署或现场验证。
