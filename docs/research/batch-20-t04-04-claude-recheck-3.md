# 第二十批 T04-04 第三次定向复核（作者第三轮修订后）

复核日期：2026-10-13（实际取证日）。审阅模型 `claude-opus-5-5`，由用户本次明确要求。这不是既有的 `gpt-6.1-sol / xhigh` 批量审阅约定，也不改写该约定；推理等级等运行元数据没有可核验记录，不补造。审阅者角色独立于作者修订角色。

**结论：T04-04 第三次定向复核未通过。本轮范围 6 项（C24、C25、C26、C29、C30、C31）：CLOSED 4（C25、C26、C29、C31），OPEN 2（C24、C30）。连同前两轮已关闭、本轮不重开的 C22、C23、C27、C28，B20-C22–C31 合计 CLOSED 8 / OPEN 2。** C24 剩两处：L56 来源栏的链接文字仍写着 L618；RGW"传输"栏新写入的"RGW 上传无续传语义"是没有来源支持的否定断言（按原 ID 追记）。C30 剩一处：L53 RGW 栏的"见 T04-03 §2"仍是纯文本。三处都只需改一两个词或一个链接。不新增发现 ID。

本轮只做只读核对：未改作者正文、来源记录、修订映射、登记或计划；未下载模型，未上传或发布对象，未执行读写、中断或计时试验。模型审阅不构成硬件或现场验证。

## 输入（以 SHA-256 识别）

| 输入 | SHA-256 | 与任务给定前缀 |
|---|---|---|
| [T04-04 正文](../../knowledge/04-data-storage/artifact-transfer-and-publication.md)（97 行，procedure / draft） | `28041ec977fdb538…` | 一致 |
| [修订映射](batch-20-review-fixes.md)（T04-04 第三轮节 L123–129） | `c534b375ee77af96…` | 一致 |
| [前次复核报告](batch-20-t04-04-claude-recheck-2.md)（剩余关闭条件权威来源） | `00187ead9ee8d5fe…` | 任务未给前缀 |
| [任务计划](../../plans/full-coverage-backlog.yaml)（T04-04 acceptance 4 条） | `f16309beadf5ae4f28d5fc7428a2348bea0cf08d155d57730a4d817cfcdd3e96` | 与前两轮相同，未变 |

`make check`：`PASS: 91 content entries; 409 sources.` 只校验结构与本地链接，不校验技术正确性和远端链接。

## 源重取（审阅者独立获取）

用 `curl` 默认 TLS 只读获取，原文只存放在 `/tmp/b20rc3/`，未入库。

| 来源 | SHA-256 | 核对结果 |
|---|---|---|
| hub `file_download.py`@d5dff4ef | `a973d198…bfe4ef` | 与前两轮一致。L530 `def xet_get`；L600–603 `PyXetDownloadInfo(..., hash=xet_file_data.file_hash, ...)`；L618 `name="huggingface_hub.xet_get"`（进度条参数）；L627–633 `download_files(...)`；L1708–1710 Xet 分支条件与 `xet_get` 调用。 |
| safetensors README@v0.7.0 | `e430910c…5e1696e1` | 与前两轮一致。L89 "Duplicate keys are disallowed. Not all parsers may respect this."；L94 "Tensor values are not checked against, in particular NaN and +/-Inf could…"。 |
| Ceph Squid objectops 页 | `14f5689f…f042e0ba` | 去标签后有 "Multipart Upload Part"（upload-id 不匹配返回 404 NoSuchUpload）、"List Multipart Upload Parts"（`GET /{bucket}/{object}?uploadId=`）和 "Complete Multipart Upload"（"Assembles uploaded parts and creates a new object, thereby completing a multipart upload."）。全页没有 "resume" 一词，也没有写明中断后能否在同一 upload-id 下续传。 |

取证限制：

- hf_xet（外部 Rust 包）的实现未核对，仍为 unknown。
- 未克隆仓库，未跑测试，未经 GitHub API 重做 tag→commit 解析。
- Ceph 页为动态站点，字节可能随时间变化，按文字核对。fsync(2)、rename(2)、T04-02 原始来源本轮未重取。T04-02 和 T04-03 只核对了正文中被引的行。

## 逐项复核

### B20-C24 — P1 / **OPEN**（L35 已限定；L618 残留在链接文字中；RGW 新断言无据）

- 已满足：
  - L35 改为"hub 下载完成判据只有长度（plain HTTP 路径；无内容哈希），见 §2"。限定写在断言内，§2 的 L56 是 Xet 例外行，并标了 unknown。满足"一类限定"。
  - RGW 栏"传输"（L55）删除了"同左"，改为上传方向，并链接[对象与并行存储 §2](../../knowledge/04-data-storage/object-and-parallel-storage.md)。
  - L56 本地栏正文写"哈希交外部包 L600–603，下载 L627–633"，与重取原文逐行一致。
- 未满足：
  1. **L56 第三栏（来源栏）的链接文字仍是"file_download.py L530/618/1708-1710"**。正文锚点已改，来源栏没有同步。L618 是进度条参数，不支持该行任何主张。前次条件写的是"L56 锚点 L618 改为 L600–603/L627–633"，只做了一半。
  2. **追记（新事实问题，按原 ID）**：L55 RGW 栏写"RGW 上传无续传语义"。这是新写入的否定断言，没有来源支持。T04-03 §2 multipart 行（object-and-parallel-storage.md L53）和 Squid objectops 页都列出了 Upload Part（按 upload-id 和 partNumber 上传）和 List Multipart Upload Parts。也就是说，接口上可以列出已上传的分片，再在同一 upload-id 下补传其余分片。文档没有用"续传"一词，但也没有否定这种用法。括号里的"续传仅 hub 下载实现行为，不外推上传"是正确的，问题只在前半句把"不外推"写成了"无"。
  3. 不阻断（沿用前次第 4 条）：L80"超过 5 次重试"仍没有注明只适用于 HTTP 分支。L80 的计时起止写了 `http_get`，已隐含分支。
- 剩余关闭条件：
  - L56 来源栏链接文字改为"file_download.py L530/L600–603/L627–633/L1708–1710"（删除 618）。
  - L55 RGW 栏把"RGW 上传无续传语义"改为不作否定断言的写法，例如"hub 续传语义不外推到上传；multipart 中断后能否在同一 upload-id 下补传分片，Squid 文档未写明（unknown；接口有 List Parts）"。也可以照前次建议写"中断后按 List uploads 找残留再 Abort"。

### B20-C25 — P1 / **CLOSED**

- L54 改引"[本地与共享存储 §3](../../knowledge/04-data-storage/local-and-shared-storage.md) 提交链/锁行与 [§4 选型表发布行]"。T04-02 §3 有"写入→提交→稳定存储"行（L86，UNSTABLE4/COMMIT/write verifier，RFC §18.32）和"可见性≠持久性"行（L92）；§4 发布行（L100）覆盖 `hard`、`sync`、fsync/close 查错和 rename 后复核。L54 的各项主张都能在这两节找到出处。
- L57 的"rename(2)"已就近链接 man7 页。
- 不阻断：
  - 两个链接都只到文件，节号写在链接文字里，与 C27 的处理方式相同，可以接受。
  - "提交链/锁行"中的"锁行"与 L54 的主张关系不大，可以删除。
  - L57 写成了"以 rename(2)（[rename(2)](https://man7.org/linux/man-pages/man2/rename.2.html)）为准"，词重复了，可以只保留链接。

### B20-C26 — P1 / **CLOSED**

- L57 RGW 栏改为"Complete 即单对象提交点（见[对象与并行存储 §2](../../knowledge/04-data-storage/object-and-parallel-storage.md) multipart 行）"。T04-03 L53 multipart 行写明 Complete"组装分片建新对象"，并链接 Squid objectops。本轮重取的 objectops 原文是 "Assembles uploaded parts and creates a new object, thereby completing a multipart upload."，支持"Complete 即单对象建立点"。集合级提交点仍标为"本库设计"，单文件 rename 一侧已有 rename(2) 链接。上游语义和本库设计已分开标注，且各附来源。
- 不阻断：Squid 文档没有写 Complete 前后的可见性，T04-03 L53 已记为 unknown。L53 本栏写"完成前可见性/列举一致性 unknown"，与之一致。

### B20-C29 — P2 / **CLOSED**

- L70 的现象列标注了"（方法设计，未执行）"。
- 锁文件补充了"删除仍被并发下载持有的锁文件的安全条件未核对，unknown"。
- L72 补了 [README L89] 和 [README L94] 两个链接（目标为 v0.7.0 README），本轮重取，两行原文与正文主张一致。
- 不阻断：链接只到文件，没有到 `#L89` 和 `#L94` 的行锚点。行号已写在链接文字里，可以接受。L70 句末仍写"按清单比对清理"，读者可能理解成锁文件也照此清理。由于前面的括号已标 unknown，不构成照做指令。

### B20-C30 — P2 / **OPEN**（L68、L85 已链接；L53 仍为纯文本）

- 已满足：L68"见 [T04-03 §2/§5]"、L85"[T04-03 §5]"已改为指向 `object-and-parallel-storage.md` 的链接，链接文字带节号。
- 未满足：**L53 RGW 栏仍为纯文本"（见 T04-03 §2）"**。前次剩余条件点名了"L53、L68、L85"三处，修订映射写的是"T04-03 引用改链接"，但 L53 没有改。
- 剩余关闭条件：L53 的"见 T04-03 §2"改为 `[T04-03 §2](object-and-parallel-storage.md)` 一类的链接。

### B20-C31 — P3 / **CLOSED**

- 前次剩余条件是"按 C26 剩余条件，在 L57 为 Complete 语义补 Ceph 文档就近引用，或从 `source_refs` 删除该 ID"。前次 C26 写明，链接到 T04-03 §2 multipart 行"同时满足 C31 第 3 条"。本轮 L57 已加该链接，T04-03 L53 再链接 Squid objectops 与 bucketops。`src.ceph.docs-rgw-s3-squid` 留在 `source_refs` 中，经一跳链接可追溯到原页。
- 如实说明：正文本身仍然没有 docs.ceph.com 直链，修订映射所说的"Ceph 登记正文引用落盘"是通过 T04-03 间接实现的。按前次条件，这样可以接受。
- 前次 C31 条目中"L56 锚点 L618 的修正见 C24"只是交叉引用，残留的问题记在 C24 下，不在此重复计数。

## 不阻断追记（不新增 ID，不改变计数）

- C28（已 CLOSED，不重开）：前次关于 L82"L784–786 _check_disk_space 只 log warning"的锚点建议（实际是 L799 `warnings.warn`，检查在下载前 L1705–1706）本轮未处理。仍建议修正。
- 修订映射：第二轮节现在只出现一次（L110），重复已消除。第三轮节标题写"处理 C24/C25/C26/C29/C30"，但正文条目包含 C31，建议标题补上 C31。
- 范围外：登记 `src.linux-man-pages.rename-6.19` 的条目 notes（L4961）现在是 rename 内容（newpath 原子替换、EXDEV、NFS 重传），前次怀疑的错位已不存在。license 下另有一条 notes（L4960）属于许可说明，不算重复。正文 `updated_at` 和登记 `registered_at` 仍是 2026-10-14，晚于取证日 2026-10-13，留给作者核查。

## 对照 acceptance

| acceptance | 判定 | 未关闭 |
|---|---|---|
| 1 清单字段；下载成功≠版本一致/ready | 满足；L35 已限定 plain HTTP | — |
| 2 本地/NFS/RGW 提交条件逐实现核对 | 提交条件与引用已满足；RGW 传输栏有一处无据否定断言，Xet 来源栏有 L618 残留 | C24（P1，局部） |
| 3 中断/部分/旧/混合/重试/清理；三类门槛 | 满足 | — |
| 4 阶段计时与失败点；链接 durability/integrity/推理加载 | 基本满足；L53 一处 T04-03 引用未链接 | C30（P2） |

## 结论

**第三次定向复核未通过：本轮 6 项 CLOSED 4 / OPEN 2；C22–C31 合计 CLOSED 8 / OPEN 2。** 剩余工作：

1. **C24（P1）**：L56 来源栏链接文字删除 618，改为 L600–603/L627–633。L55 RGW 栏"RGW 上传无续传语义"改为不作否定断言的写法（Squid 文档未写明，unknown；接口有 List Parts）。
2. **C30（P2）**：L53 RGW 栏"见 T04-03 §2"改为链接。

P1、P2 全部关闭前不得声明审阅通过。修订后按 ID（C24、C30）再做定向复核。本报告只覆盖编辑与来源层面，不构成硬件、部署或现场验证。
