# 第二十批 T04-05 初审

审阅日期：2026-10-13（实际取证日）。正文 `updated_at: "2026-10-14"` 视为交付标签，不作为本轮取证日期；输入以下表 SHA-256 识别。

**结论：T04-05 需修订。新增 9 项发现（B20-C32–C40）：P1 ×2、P2 ×6、P3 ×1，全部 OPEN。** acceptance 2 与 4 各有一项 P1 缺口；acceptance 1、3 有 P2 缺口。acceptance 2 中"不把 Ceph RADOS scrub 自动当 RGW 端到端校验"一句已明确写出，这一点满足。`make check` 通过（91 content entries / 409 sources），但它只校验结构与本地链接，不说明技术正确性。既有 §1–§4、适用边界、常见误解节经 `git diff` 核对确为逐字保留（diff 只动 frontmatter 与文末追加）。

审阅者角色独立于作者。审阅模型为 `claude-opus-5-5`，由用户本次明确要求试用。这不是既有的 `gpt-6.1-sol / xhigh` 批量审阅约定，也不改写该约定；推理等级等运行元数据没有可核验记录，不补造。本轮只做审阅和只读取证：未改作者正文、来源记录、登记、索引或计划，未执行保存、损坏注入、scrub、repair 或任何读写试验。模型审阅不构成硬件或现场验证。

## 输入（以 SHA-256 识别）

| 输入 | SHA-256 |
|---|---|
| [T04-05 正文](../../knowledge/04-data-storage/checkpoint-integrity-evidence.md)（145 行，concept / draft） | `4e138c0b11e178e3c0e84115d3277b4590a43b6e482c1a26c857d59c477e8e76` |
| [作者来源记录](batch-20-t04-05-sources.md)（15 行） | `cb48a354ac96e810bde2e4be8981c21cc1723b80ffbfde6a64e55379ecd8f305` |
| [任务计划](../../plans/full-coverage-backlog.yaml)（T04-05 L5204–5244，acceptance L5220–5224） | `f16309beadf5ae4f28d5fc7428a2348bea0cf08d155d57730a4d817cfcdd3e96` |
| [来源登记](../../sources/registry.yaml)（T04-05 无新增 ID） | `96309fd1d8a9c9abf81add42e413c4def8e44d1f414190bdfe4bc106ca07f930` |

旁证（按本库现行草稿核对，未重新取其一次源）：`artifact-transfer-and-publication.md`（T04-04，recheck-5 通过）、`object-and-parallel-storage.md`（T04-03，recheck-5 通过）、`local-and-shared-storage.md`（T04-02，recheck-5 通过）、`06-training/checkpoint-state-consistency.md`、`06-training/checkpoint-state-recovery-triage.md`。正文 `related_ids` 四个 ID 与 `source_refs` 十个 ID 都能解析到已有文件或登记项。

## 一次源取证（审阅者独立获取）

全部用 `curl -sSL` 只读获取，默认 TLS 校验；除注明外 HTTP 均为 200。HTML 去标签后按文字核对，不只判可达性。原文只存在临时目录 `/tmp/b20rev5/`，未入库。

| 来源（登记 ID） | URL | SHA-256（原文） | 核对点与结果 |
|---|---|---|---|
| Google SRE Data Integrity（src.google.sre-data-integrity） | [sre-book/data-integrity](https://sre.google/sre-book/data-integrity/) | `b92a15e5121f9e4a8788e46edccae31ea0eb7d6d377d9493335cd878824172b2` | 有 defense in depth 三层：soft deletion、backups and their related recovery methods、regular data validation，并写明 "data recovery plans should not rely upon replication"。"Out-of-band data validation" 节以 Gmail 每日 validator 为例，原文说这些 validator "has detected actual data integrity problems in production"。"Knowing That Data Recovery Will Work" 节要求 "Continuously test the recovery process"，并称 "the only test that should let you sleep at night is a full end-to-end test"。另有案例节 "Gmail—February, 2011: Restore from GTape" 与 "Google Music—March 2012: Runaway Deletion Detection"。正文 §5–§8 对这些内容一条都没有引用。→ C38/C39 |
| Lustre Operations Manual 2.x（src.lustre.ops-manual-2x） | [lustre_manual.xhtml](https://doc.lustre.org/lustre_manual.xhtml) | `63b09d0650de3491eee9c976dff1246706dc6496bc996c139fdebdf7fc4a0d8c` | §23.5.1 "Lustre Checksums" 的要点：客户端有两类 checksum，in-memory 和 wire；"a 32-bit checksum of the data **read or written** on both the client and server is computed"；"The **ldiskfs** backing file system does NOT do any persistent checksumming"；默认在客户端开启；失配时 syslog 记 `BAD WRITE CHECKSUM`，客户端 "re-read or re-write the affected data up to five times"，仍失败则向应用返回 I/O error。§23.5.1.1 写明默认算法为 adler32，可改。§1 另说 ZFS 作后端时 "leverage the … data integrity features of ZFS"，并区分恢复工具 "e2fsck for ldiskfs OSTs, scrub for ZFS OSTs"。LFSCK 的定位是 "restore consistency between storage components"。→ C35 |
| nfs(5)（src.nfs-utils.nfs-5-man7） | [nfs.5](https://man7.org/linux/man-pages/man5/nfs.5.html) | `2b9d9223f2faeadffdc7c50936a7d03ae0a194c25d9fc3d1662d40dd22e534fb` | 原文 "Using NFS over UDP on high-speed links such as Gigabit can cause silent data corruption"，并说明 UDP checksum 只有 16 bit，"silent data corruption will occur"。`sec=krb5i` "provides a cryptographically strong guarantee that the data in each RPC request has not been tampered with"。soft 超时可致静默损坏一条已在 T04-02 §3 引用。→ C33 |
| Ceph Squid BlueStore 配置（未登记；Squid 文档许可同 src.ceph.docs-rgw-s3-squid） | [squid bluestore-config-ref](https://docs.ceph.com/en/squid/rados/configuration/bluestore-config-ref/) | `3a00d9c724fa7adb941b6562bdcf0d5bfc781a3ad50ee1725009da35409392ee` | Checksums 节原文 "BlueStore checksums all metadata and all data written to disk"；数据默认 crc32c，也可选 xxhash32/xxhash64；通常每 4 KB 存约 4 字节 checksum。截短 checksum 会提高漏检概率，原文给出 "about one in four billion given a 32-bit (4 byte) checksum"。这是官方给出的"随机错误漏检率"表述，可用于碰撞/漏检边界。页内未见"每次读取都校验"的逐字句，读路径修复依据见下行。→ C34/C36 |
| Ceph Squid osd-config-ref（对照正文 §3 所引 latest 版） | [squid](https://docs.ceph.com/en/squid/rados/configuration/osd-config-ref/) / [latest](https://docs.ceph.com/en/latest/rados/configuration/osd-config-ref/) | `831c2d06…85af3c7c`（squid）/ `e90266b3…d548c557`（latest） | 两版都含 "Light scrubbing checks the object size and attributes … Deep scrubbing reads the data and uses checksums" 原句。Squid 中 `osd_deep_scrub_interval` 默认 7 天，`osd_scrub_auto_repair` 默认 `false`。正文 §3 对 Squid 的结论成立，但引用的是 latest 版。→ C34 |
| Ceph Squid health-checks | [squid health-checks](https://docs.ceph.com/en/squid/rados/operations/health-checks/) | `a6a9ed5466bb87fee93908d505ba59c96272961f2e72c1dec05a7955f0823907` | 与正文 §3 一致：PG_DAMAGED 是 "Data scrubbing has discovered problems with data consistency"，OSD_SCRUB_ERRORS "generally paired with PG_DAMAGED"。OSD_TOO_MANY_REPAIRS 节写明 "scrub handles errors only for data at rest"，并且 "any read error that occurs when another replica is available is repaired immediately"，这是 RADOS 读路径修复的依据。→ C34 |
| hub `tests/test_file_download.py`@d5dff4ef（src.hf.huggingface-hub-v0.33.0） | [raw](https://raw.githubusercontent.com/huggingface/huggingface_hub/d5dff4efd9187cc5c56246f416d666ea1f808cb0/tests/test_file_download.py) | `f19f048c88a5840b60adc883991d0220da1a5cbe46f0e51e72d8e497c34f68bc`（与 T04-04 审阅取得的字节相同） | L798 `test_resume_from_incomplete`，L802 写入伪数据 `"XXXX"`，L804 `self.file_path.read_text() == "XXXXent"` 是裸表达式，缺 `assert`，L806 起为 force_download 用例。行号与正文 L136 一致。→ C38 |

取证限制：

- PyTorch DCP、MindIO、zipfile 三类来源在本轮未重取，原因是 §1–§4 逐字未改，且这些来源已在第十二批核对过。
- safetensors 与 hub 实现行由 T04-04 审阅取证并已通过复核，本轮只重取了上表的 hub 测试文件。
- Squid `pg-repair` 页按 `/rados/operations/pg-repair/` 路径返回 404（`1e2e3c11…`），未再寻找替代路径，因此 repair 前的证据保留步骤没有官方原文可比对。
- MD5/SHA-256 的碰撞强度没有取一次源（例如 RFC 6151、NIST 文档），C36 只要求作者补源或改写为本库约定。
- 未检索 hub、RGW、safetensors 的签名机制。

## 发现

### B20-C32 — P1 / OPEN：修复前证据保留、隔离、恢复点和恢复后校验没有链接到专门流程

位置：正文 §8 L139；acceptance 4 后半句。

证据：L139 把"恢复流程"链接到两篇 **concept**：[恢复一致性](../../knowledge/06-training/checkpoint-state-consistency.md)和[持久化边界](../../knowledge/04-data-storage/checkpoint-durability.md)。库内其实已有专门的 **procedure**，即 [Checkpoint 恢复状态异常诊断指南](../../knowledge/06-training/checkpoint-state-recovery-triage.md)（`training.checkpoint-state-recovery-triage`）。它的"适用范围与前置条件"写明"在最后一个已知可恢复点完成验证前，不允许新运行覆盖它"，"停止条件与恢复安排"节写了停止与授权条件，正对 acceptance 所说的"隔离/恢复点选择与恢复后校验"，但正文没有链接它。存储侧的 repair/恢复流程归 T04-07（plan L5290 起，`content_type: procedure`，batch 21，planned），正文也没有标为"未交付/缺失部分 unknown"。

另外，L139 自拟了"保留文件＋清单＋日志快照 → 隔离 → 选恢复点 → 复验"的顺序，却没给来源，也没说明 Ceph `pg repair` 前需要保留什么（例如修复前的不一致对象清单）。修复会改写副本，所以修复前保留证据是本节的关键边界。

关闭条件：

- 训练状态恢复链接到 `checkpoint-state-recovery-triage.md` 的对应节（前置条件、停止条件与恢复安排、完成判据）。
- 存储侧 repair/隔离流程明确写"归 T04-07（batch 21，未交付）"，缺失部分记 unknown，不以 concept 页代替。
- L139 的步骤顺序要么标为本库设计约定，要么引用来源（例如 SRE 章 "should not rely upon replication" 与 "full end-to-end test"）。
- Ceph repair 前的证据项若无官方原文，记 unknown。

### B20-C33 — P1 / OPEN：NFS 行没有字节校验分析，并与 T04-02 的 v4 CTO 边界冲突

位置：正文 §6 L121。

证据：

- acceptance 2 要求核对"读路径、持久化、scrub/checksum 能发现与不能发现的错误"。NFS 行的"读路径校验"一栏只写了 CTO、属性缓存和锁协议。这些是可见性和一致性机制，不是校验。该行没有回答 NFS 读写数据由什么校验，因此"不能发现"一栏也就无从谈起。nfs(5) 本身给出了必要事实：UDP 在高速链路上可致 silent data corruption（UDP checksum 只有 16 bit）；`sec=krb5i` 提供每个 RPC 的完整性保证；`soft`/`softerr` 超时可致静默损坏（T04-02 §3 已引）。正文三条都没写。
- "持久化/修复"一栏只写了 grace/reclaim，漏了 T04-02 §3 已核对的 UNSTABLE WRITE → COMMIT → write verifier 这条真正的持久化判据。
- 行首标"NFS（v4.1）CTO"。但 T04-02 §3 原文写的是"此节仅以 v3 叙述；… Linux v4 客户端 CTO 行为未在已取源中单列（unknown）"。本行把 unknown 写成了 v4.1 的既定行为。

关闭条件：

- 读路径一栏分列：协议/传输层校验（TCP 与 UDP 的差别、`krb5i` 可选）、NFS 协议没有端到端内容校验（若作此断言，须有 RFC 8881 依据，否则记 unknown）、服务器后端文件系统的校验（实现相关，unknown）。
- "不能发现"一栏补入：未启用 `krb5i` 时的传输损坏、`soft` 超时导致的静默损坏、写入前已错的字节。
- 持久化一栏补 COMMIT 和 write verifier。
- CTO 措辞与 T04-02 §3 的 v3/v4 边界保持一致。
- `source_refs` 补 `src.nfs-utils.nfs-5-man7`、`src.ietf.rfc-8881`（见 C39）。

### B20-C34 — P2 / OPEN：RGW 行的"读路径校验"一栏没有读路径校验，并遗漏 BlueStore checksum 与读修复

位置：正文 §6 L122；frontmatter `source_refs`。

证据：

- RGW 行"读路径校验"一栏写的是"multipart/版本化按文档；`content-md5` 只覆盖请求体"。multipart 和版本化是发布语义；`content-md5` 是写入请求头。三者都不在读路径上。
- RGW 的数据落在 RADOS 上。Squid BlueStore 文档写明 "checksums all metadata and all data written to disk"，默认算法 crc32c。Squid health-checks 写明读错误在有其他副本时 "repaired immediately"。这两条恰好是 RADOS 层读路径与持久层的校验和修复，本行都没写。
- "不能发现"一栏的理由只写了"RGW 语义层（版本/可见性/部分发布）不在其范围内"。更直接的边界没写：BlueStore checksum 和 scrub 都在 OSD 收到数据之后才起作用。客户端到 RGW、或 RGW 处理过程中已经出错的字节，会被正确地算出 checksum 并多副本保存（正文 §3 L70 已有同类表述，可直接引用）。这一推论应标为本库推论。
- 前文 §3 引用的是 latest 文档，而 §6 声明后端为 Squid。本轮核对 Squid 版 scrub 原句与 `osd_scrub_auto_repair=false` 默认值，确认两版一致，结论不受影响。但 RGW 行引"前文 §3"时，版本锚不一致。

关闭条件：

- 读路径一栏改写为 RADOS 层（BlueStore checksum＋有副本时读修复，引 Squid 原页）与 RGW 层（GET 无端到端内容校验；ETag 不作内容哈希）分列。
- "不能发现"一栏补"到达 OSD 前已错的字节"，标为本库推论。
- Squid BlueStore 页登记或并入既有 Ceph 登记的 revision 说明。
- §3 的 latest 引用对 Squid 后端的适用性加一句说明，例如"Squid 版同句已核对"。

### B20-C35 — P2 / OPEN：Lustre 行对手册 §23.5.1 的转述不完整、未限定 ldiskfs，证据指针失效

位置：正文 §6 L123；`sources/registry.yaml` src.lustre.ops-manual-2x 条目。

证据：

- 手册 §23.5.1 原文：checksum 有 in-memory 与 wire 两类，覆盖 "data read or written"；默认开启；失配时重读或重写最多五次，仍失败返回 I/O error；默认算法 adler32。正文只写了"客户端 32-bit 传输校验（wire）"，漏了 in-memory 一类、读写两向、重试后返回 EIO 的行为。还把 `BAD WRITE CHECKSUM`（写方向日志）放进"读路径校验"栏。
- "不能发现：持久化内容损坏"没有限定范围。手册原文只说 **ldiskfs** 不做持久校验；对 ZFS OST，手册另写 "data integrity features of ZFS"，并以 "scrub for ZFS OSTs" 作恢复工具。正文行内虽有"ldiskfs 无持久校验"字样，结论栏却泛化到了整个 Lustre。
- "持久化/修复"一栏写"锁协议一致性"。锁不是持久化或修复机制。按手册，相关工具是 e2fsck（ldiskfs）、ZFS scrub 与 LFSCK（组件间一致性，不是数据内容校验）。
- 证据栏写"手册 §23.5.1（见对象存储登记注）"，没有链接。登记 src.lustre.ops-manual-2x 的 revision/notes 只列了 striping/DoM/FLR/llite/ldlm，**没有 §23.5.1**，所以这个指针指向的是不存在的内容。

关闭条件：

- 按 §23.5.1 原文补全两类 checksum、读写两向、五次重试后返回 EIO、默认 adler32 可改。
- "不能发现"一栏限定为 ldiskfs OST；ZFS OST 记"手册称有 ZFS 完整性特性，具体行为未核（unknown）"。
- 持久化/修复一栏改为 e2fsck/ZFS scrub/LFSCK 的范围说明，或记 unknown。
- 证据栏给出手册链接与节名；登记 revision 补 §23.5.1（或改为引用对象存储正文 §4，那里已列 §23.5.1）。

### B20-C36 — P2 / OPEN：碰撞、真实性、可信清单三条边界只有一句话，且无来源、引用互相指向

位置：正文 §5 L109、L112、L115。

证据：

- L109 内容哈希行写"碰撞边界见下"，L115 边界句写"碰撞（CRC32/MD5 弱于 SHA-256，选型见上）"，两处互相指向，都没有给出来源。
- 正文没有区分两类风险：一类是**随机错误漏检**（CRC/checksum 的设计目标，BlueStore 页给出官方量级，32-bit 约四十亿分之一），另一类是**对抗性碰撞**（针对 MD5 的构造攻击，与随机漏检不同）。acceptance 1 要求说清"碰撞"边界，这一区分是核心。
- 签名行只写了"真实性 / unknown"，没有说明所选样板是否带签名字段。T04-04 审阅已核对 safetensors README，header 中没有签名或校验和字段，可以写成"所选格式内无签名字段"。
- "可信清单"只有"须可信来源＋版本固定"一句，没回答关键问题：清单和数据经同一信道获取时（例如 hub 的 LFS ETag sha256 由同一服务端声称），哈希比对只能证明"与该信道声称值一致"，不能证明真实性。T04-03 §5 的约定是"发布方写入清单，读回方重算"，但正文没交代清单本身如何受保护、读回方从哪里独立获得清单。

关闭条件：

- 碰撞边界分随机漏检（引 BlueStore Squid 原句或其他固定来源）与对抗碰撞（引固定来源，或标为本库约定/unknown）。
- 删除"见下/见上"的循环引用。
- 签名行写明所选样板格式内无签名字段（引 safetensors README），hub/RGW 的签名机制记 unknown。
- 可信清单补"清单信任锚"条件：同信道哈希不证明真实性，并说明本库约定的清单来源与保护方式，或记 unknown。

### B20-C37 — P2 / OPEN：验证链没有落到 checkpoint 本身，"缺样"与验收"缺片"不一致，正确性门指向未交付的计划 ID

位置：正文 §7 L127–132。

证据：

- acceptance 3 要求区分"缺片"。正文写的是"缺样"，在本库语境下容易读成缺数据样本。它的定义"清单有、读回无"其实是缺成员或缺分片。
- 本页主题是 checkpoint，但验证链只用制品与对象的术语（commit/versionId）。没有说明它在 DCP 上如何实例化：清单对应 `.metadata` 中 `storage_data` 列出的 `.distcp` 文件集合；完整读回需要覆盖每个 `(relative_path, offset, length)`；MindIO 的文件个数检查只覆盖"缺片"的一部分。前文 §2 已有这些事实，链条却没有用上。
- 第 4 步"同输入结果（正确性门，见 T07-01）"给的是计划 ID，不是链接，而且 T07-01 属推理侧、batch 26，尚未交付。对训练 checkpoint，已有的落点是 [恢复一致性"恢复后验证"表的"同输入单步/持续窗口"两行](../../knowledge/06-training/checkpoint-state-consistency.md)。
- 四类错误分别在链条的哪一步被发现、哪一步发现不了，没有写成对照。比如错版在第 1 步按清单判定；静默改动只有第 2 步做全文件哈希时才能发现，DCP 按 offset 读取不等于完整读回。

关闭条件：

- "缺样"改为"缺片/缺成员"。
- 补一段 DCP（可附 MindIO）实例化：清单、完整读回、结构、同输入各对应什么。
- 第 4 步对训练 checkpoint 链接到 06 恢复后验证，对推理制品写"归 T07-01（未交付），unknown"。
- 给出"错误类别 × 步骤"的发现/不能发现对照，可用一行或一张小表。

### B20-C38 — P2 / OPEN：官方反例只有 hub 测试一条，Ceph/Lustre 条目只是告警信号；已登记的 SRE 案例未用

位置：正文 §8 L136–138。

证据：

- acceptance 4 要求"官方测试/案例支持的反例"。L136 的 hub 测试符合要求（行号经本轮核对）。但"伪前缀 `XXXX` 残留进最终文件"写成了事实。由于 L804 缺 `assert`，测试本身并不强制这一结果；它只能说明测试作者的期望值，以及实现在续传时不校验已有前缀，后一点由 T04-04 已核对的长度判据支持。
- L137（Ceph 告警）与 L138（Lustre 日志）是文档描述的检测信号，不是"看似成功、实际错误"的反例，也不是测试或案例。
- 已登记的 SRE 章有现成的官方案例与原则，正文没有用：Gmail 2011 从磁带恢复、Google Music 2012 删除流水线误删且数周后才发现、Gmail 的 out-of-band validator 在生产中发现过真实问题、"should not rely upon replication"、"only … full end-to-end test"。其中"不应依赖副本"与本页"写入前已错的字节会被多副本忠实保存"（§3 L70）直接相关；out-of-band validator 是 §4 "应用自检无可引用实现"的一个可引用案例，尽管它不是 AI checkpoint 场景，登记 notes 已作此限定。

关闭条件：

- hub 条改写为"测试期望值为 `XXXXent`（L804 缺 assert，测试未强制）；实现以长度为完成判据（T04-04 §2）"。
- Ceph/Lustre 两条移到"检测信号"，或补上对应的官方测试或案例。
- 至少引用 SRE 章的一处案例或原则，作为"成功不等于正确 / 恢复须端到端验证"的官方支持，并注明不外推到 AI checkpoint。
- 若不用，从 `evidence_refs` 移除 SRE（见 C39）。

### B20-C39 — P2 / OPEN：来源记录缺精确定位，登记 ID 与实际依据不符，verification notes 夸大核对范围

位置：作者来源记录 L7–11；正文 frontmatter L8–37；登记 src.lustre.ops-manual-2x。

证据：

- AGENTS.md 要求"cite exact supporting pages or revisions near substantive claims"。来源记录三行只写"复用既有＋T04-03/04""正文 §5"，没有逐主张给出页、节或行。
- 来源记录称 NFS 行依据 `src.kernel.docs-nfs-v6.16`，但 NFS 行的实际依据（CTO、grace/reclaim）来自 nfs(5)（`src.nfs-utils.nfs-5-man7`）与 RFC 8881（`src.ietf.rfc-8881`）。这两个 ID 都不在正文 `source_refs` 中。
- SRE 被加入 `source_refs` 与 `evidence_refs`，notes 也称核对了"恢复目标/演练原则"，但正文 §5–§8 没有任何一句由它支持（见 C38）。
- notes 写"Lustre 手册（wire checksum/锁）"已核对，但登记 revision 没有记录 §23.5.1（见 C35）。来源记录自述"无新增远程取证，仅复用已核对来源"，这与 notes 的"新增 … 核对"措辞不一致。

关闭条件：

- 来源记录逐行列出 §5–§8 每条主张所依据的登记 ID 与页、节、行。
- NFS 依据改为 nfs(5) 与 RFC 8881，并同步更新 `source_refs`。
- SRE 要么在正文中有落点，要么移出 `evidence_refs`。
- notes 改为如实描述："复用 T04-02/03/04 已核对来源，本任务未新增远程取证"；Lustre §23.5.1 补入登记。

### B20-C40 — P3 / OPEN：新增节放在旧的"来源与待确认问题"之后，定义、边界与导航未同步

位置：正文 L44、L76–81、L96–102、L104 起；`related_ids`；`knowledge/04-data-storage/index.md` L28。

证据：

- 新增 §5–§8 追加在旧"来源与待确认问题"之后，全页因此有两个来源节。
- L44 定义仍写"本文只管'字节/文件是否损坏'这一层证据"，但新增节已经覆盖版本、真实性和训练状态错误。
- 适用边界节没有给 NFS/RGW/Lustre/hub 的版本锚。
- L102 的"待确认：其他存储系统的 scrub 等价物"已部分被新增节回答，却未更新。
- `related_ids` 没有加入正文已链接的 artifact-transfer、object-and-parallel-storage、local-and-shared-storage，以及 C32 要求链接的 recovery-triage。
- 读者可见文本中出现计划 ID（"T04-03 §5""T07-01"）。
- 04 索引中本页的摘要仍只写"四层校验"。

任务目标是"保留 DCP/MindIO/Ceph 校验层次的**准确边界**"，没有要求逐字不动。对定义、边界、待确认三处做最小同步修改，不违背任务目标。

关闭条件：新增节移到旧来源节之前，或合并两个来源节；定义句、适用边界、待确认三处做最小同步修改；补 `related_ids`；计划 ID 改为文档链接或加注"未交付"；更新索引摘要。

## acceptance 对照

| acceptance | 判定 | 相关发现 |
|---|---|---|
| 1 原语对照与碰撞/真实性/可信清单/语义边界 | 部分满足：六类原语齐全，语义边界清楚；碰撞、真实性、可信清单三条边界没有来源，也不够具体 | C36（P2） |
| 2 选定后端读路径/持久化/scrub-checksum；不把 RADOS scrub 当 RGW 端到端 | 未满足：NFS 行缺校验分析，且有版本边界冲突；RGW、Lustre 两行转述不完整。"不把 RADOS scrub 当 RGW 端到端"已明确写出 | C33（P1）、C34、C35（P2） |
| 3 验证链与四类错误区分 | 部分满足：链条和四类错误都已给出；未落到 checkpoint，"缺片"措辞不符，正确性门指向未交付任务 | C37（P2） |
| 4 官方反例；证据保留/隔离/恢复点/恢复后校验链接到专门流程 | 未满足：没有链接专门流程；官方反例只有一条，且措辞过强 | C32（P1）、C38（P2） |

横向问题：C39（来源与核对记录，P2）、C40（结构与导航，P3）。

## 结论

**T04-05 初审不通过，需修订。B20-C32–C40 共 9 项：P1 ×2（C32、C33），P2 ×6（C34–C39），P3 ×1（C40），全部 OPEN。** 修订后须按各项关闭条件做定向复核。正文 `verification.status: source_checked` 在 C39 关闭前不应视为对新增节成立。本审阅只覆盖编辑与来源层面，未执行任何实测；所有后端行为仍为文档或实现层证据，不得标为 reproduced。
