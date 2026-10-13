# 第二十批 T04-05 定向复核（作者首轮修订后）

复核日期：2026-10-13（实际取证日）。审阅模型 `claude-opus-5-5`，由用户本次明确要求。这不是既有的 `gpt-6.1-sol / xhigh` 批量审阅约定，也不改写该约定；推理等级等运行元数据没有可核验记录，不补造。审阅者角色独立于作者修订角色。

**结论：T04-05 定向复核未通过。B20-C32–C40 共 9 项：CLOSED 5（C32、C34、C36、C37、C38），OPEN 4（C33、C35、C39、C40）。** 仍未关闭的 P1 有 1 项（C33），原因是本轮新取证发现 NFS 行"TCP 下无传输校验"是事实错误。C35 与 C39 的缺口是同一件事：修订映射和正文都声称 `src.lustre.ops-manual-2x` 的登记已补 §23.5.1，但登记文件里没有。C40 剩下定义句与新增节矛盾，以及一处计划 ID 没有链接。本轮不新增发现 ID；TCP 事实错误属于 C33"NFS 行没有字节校验分析"的范围，按原 ID 追记。

本轮只做只读核对：未改作者正文、来源记录、修订映射、登记、索引或计划；未执行保存、损坏注入、scrub、repair 或任何读写试验。模型审阅不构成硬件或现场验证。

## 输入（以 SHA-256 识别）

| 输入 | SHA-256 |
|---|---|
| T04-05 正文 `knowledge/04-data-storage/checkpoint-integrity-evidence.md`（153 行，concept / draft） | `20a68bd12fb304b3ab83ea8fe98887c7941dd9e10de697f8c9735fc8e1ae5dac` |
| 作者来源记录 `docs/research/batch-20-t04-05-sources.md`（19 行） | `588f4f91c62cfc85486c5464b7076c4b62079928939409ba041cd9af77287076` |
| 修订映射 `docs/research/batch-20-review-fixes.md`（T04-05 第二轮节 L147–157） | `ec59eab7a99288c6b4d4ef18aaf1ddbf5562198ca4934dc8b964be878ae6e089` |
| 初审报告 `docs/research/batch-20-t04-05-claude-review.md`（关闭条件权威来源） | `afb099d9396b53ecf4f412f140cff9bdc8f6f934a044756e4adbddcdf0287e68` |
| 任务计划 `plans/full-coverage-backlog.yaml`（T04-05 L5204–5244，acceptance L5220–5224） | `f16309beadf5ae4f28d5fc7428a2348bea0cf08d155d57730a4d817cfcdd3e96` |
| 来源登记 `sources/registry.yaml`（410 项；新增 `src.ceph.docs-bluestore-squid` L5098–5111） | `227aa464f94c2c60b0ea58dfb221acdc5977f4ef714fd1118522554683fa17a6` |

`make check`：`PASS: 91 content entries; 410 sources.` 它只校验结构与本地链接，不说明技术正确性。正文 `source_refs` 13 个 ID、`related_ids` 8 个 ID 都能解析。`git diff` 核对：§1–§4 正文与初审时相同，只改了定义句前半、适用边界、来源节与 frontmatter，均在 C40 许可的最小同步范围内。

## 一次源重取（审阅者独立获取）

用 `curl -sSL` 只读获取，默认 TLS 校验，HTTP 均为 200。原文只存在 `/tmp/b20rc5/`，未入库。HTML 去标签后按文字核对。

| 来源 | SHA-256（原文） | 本轮核对点 |
|---|---|---|
| [nfs(5)](https://man7.org/linux/man-pages/man5/nfs.5.html) | `2b9d9223f2faeadffdc7c50936a7d03ae0a194c25d9fc3d1662d40dd22e534fb`（与初审字节相同） | UDP 节："the UDP checksum is 16 bit only, so there is a chance of 1 in 65536 that it will match even if the packet payload is corrupt"。`krb5i` "provides a cryptographically strong guarantee that the data in each RPC request has not been tampered with"。`soft` 节："Using NFS over TCP or increasing the value of the retrans option may mitigate some of the risks"。**全页没有"TCP 无传输校验"之类的表述。** → C33 |
| [RFC 9293](https://www.rfc-editor.org/rfc/rfc9293.txt)（未登记；本轮仅作审阅者核对用） | `6d9ac8be4b0286f8c3d337addf442b2eb6a9b14e1366594ea7fbc273f93dc2d9` | §3.1 Header Format L405–408："Checksum: 16 bits … the 16-bit ones' complement of the ones' complement sum of all 16-bit words in the header and text"。TCP 有自身的 16-bit 校验，覆盖头部和数据。→ C33 |
| [SRE Data Integrity](https://sre.google/sre-book/data-integrity/) | `b92a15e5121f9e4a8788e46edccae31ea0eb7d6d377d9493335cd878824172b2` | 正文 §8 引的四句都核对到原文："data recovery plans should not rely upon replication"；"the only test that should let you sleep at night is a full end-to-end test"；Gmail validators "has detected actual data integrity problems in production"；Google Music 案例 "It had been over a month since the buggy data deletion pipeline first ran"。另有一句 "Datastores that automatically sync multiple replicas guarantee that a corrupt database row or errant delete are pushed to all of your copies"，可以支持正文"同义"的说法。→ C38 |
| [Lustre Manual 2.x](https://doc.lustre.org/lustre_manual.xhtml) | `63b09d0650de3491eee9c976dff1246706dc6496bc996c139fdebdf7fc4a0d8c`（与初审字节相同） | §23.5.1 "re-read or re-write the affected data up to five times … If it is still not possible, then an I/O error is returned to the application"；in-memory 与 wire 两类由 `checksum_pages` 一并开关。正文 Lustre 行转述与原文一致。→ C35 |
| [Squid BlueStore 配置](https://docs.ceph.com/en/squid/rados/configuration/bluestore-config-ref/) | `3a00d9c724fa7adb941b6562bdcf0d5bfc781a3ad50ee1725009da35409392ee` | "BlueStore checksums all metadata and all data written to disk"；数据默认 crc32c；"about one in four billion given a 32-bit (4 byte) checksum"。→ C34/C36 |
| [Squid health-checks](https://docs.ceph.com/en/squid/rados/operations/health-checks/) | `a6a9ed5466bb87fee93908d505ba59c96272961f2e72c1dec05a7955f0823907` | OSD_TOO_MANY_REPAIRS："any read error that occurs when another replica is available is repaired immediately"。→ C34 |
| hub `tests/test_file_download.py`@d5dff4ef | `f19f048c88a5840b60adc883991d0220da1a5cbe46f0e51e72d8e497c34f68bc`（与初审相同） | L798 `def test_resume_from_incomplete`，L802 写入 `"XXXX"`，L804 是裸比较表达式 `self.file_path.read_text() == "XXXXent"`，没有 `assert`。→ C38 |
| safetensors README@v0.7.0（raw） | `e430910cef3bfc36f06c236f25685dc6734ea9a50c5432d890f8b4fff05696e1` | `### Format` 在 L76，字段清单是 8 字节 header 长度、JSON header（dtype/shape/data_offsets、可选 `__metadata__`）和字节缓冲区。全文不区分大小写检索 "sign"，没有命中。所以"所选格式内无签名字段"成立。→ C36 |

取证限制：RFC 8881 没有重取，NFS 行的 COMMIT/write verifier 依据经 T04-02 §3 转引（该节链接 RFC §18.32/§18.3，T04-02 recheck-5 已通过）。PyTorch DCP、MindIO、zipfile 与 §1–§4 一样没有重取（逐字未改）。对抗性碰撞与签名机制没有取一次源，正文也记为 unknown。

## 逐项判定

### B20-C32 — P1 → CLOSED

- 训练状态恢复已链接到 `../06-training/checkpoint-state-recovery-triage.md`，链接文字点名了"适用范围与前置条件""停止条件与恢复安排""完成判据"三节（正文 L153），这三节在目标文件中都存在（L36、L97、L103）。
- 存储侧 repair/隔离写明"归 T04-07（batch 21，未交付），缺失部分 unknown，不以 concept 页代替"（L153）。
- 步骤顺序标为"**本库设计约定**"，SRE 原则另列于 L152。
- "Ceph repair 前的不一致对象清单无官方原文，unknown"（L153）。

非阻断备注：三个链接都指向同一文件，没有带片段。本库内部链接没有片段的先例，`make check` 也不检查片段，所以不影响关闭；读者需要自己按节名找到对应节。

### B20-C33 — P1 → OPEN（追记新取证事实错误）

已满足：

- `krb5i`、UDP 16-bit、`soft` 静默损坏三条已写入，与 nfs(5) 原文一致（L133）。
- "不能发现"一栏补全了初审要求的三项（L133）。
- 持久化一栏补了"UNSTABLE WRITE 须 COMMIT＋write verifier"（L133），与 T04-02 §3 一致。
- CTO 不再写成 v4.1 既定行为：证据栏写"CTO 仅 v3 有原文，v4 unknown"，适用边界 L91 同步。
- `source_refs` 已补 `src.nfs-utils.nfs-5-man7` 与 `src.ietf.rfc-8881`（L19–20）。

剩余问题：

1. **追记事实错误（本轮新取证）。** L133 写"TCP 下无传输校验（依赖端到端哈希）"。nfs(5) 没有这样的表述，反而说用 TCP "may mitigate" `soft` 的风险。RFC 9293 §3.1 定义了 TCP 头部的 16-bit checksum，覆盖头部和数据。准确的说法是：TCP 有 16-bit 校验，强度与 UDP 同一量级，nfs(5) 没有给出它的漏检率；它不能替代端到端哈希。
2. **自相矛盾。** 同一格先断言"NFS 协议本身无端到端内容校验"，括号里又写"RFC 未见对应机制，unknown；不作断言"。按初审关闭条件，没有 RFC 8881 依据时应只记 unknown，不应同时写出断言。
3. 初审关闭条件中的第三个分列项"服务器后端文件系统的校验（实现相关，unknown）"没有单独写出。持久化一栏的"实现细节 unknown"只涵盖持久化实现，不涵盖后端文件系统校验。

剩余关闭条件：

- 删去"TCP 下无传输校验"，改为"TCP 自带 16-bit checksum（RFC 9293 §3.1；漏检率 nfs(5) 未给，unknown），不替代端到端哈希"。若引 RFC 9293，需先登记，或改用已登记来源，或只写 unknown。
- "NFS 协议本身无端到端内容校验"改为只记 unknown，例如"NFS 协议层是否有端到端内容校验未核（unknown）"。
- 读路径一栏补"服务器后端文件系统校验：实现相关，unknown"。

### B20-C34 — P2 → CLOSED

- 读路径已按 RADOS 层（BlueStore checksum＋有副本时读修复）和 RGW 层（GET 无端到端内容校验、ETag 不作内容哈希）分列（L134），两条 Squid 原文都已核对。
- "到达 OSD 前已错的字节会被正确算 checksum 并多副本保存"已标"本库推论"（L134）。
- BlueStore 页已登记（`src.ceph.docs-bluestore-squid`，registry L5098），并进入 `source_refs`/`evidence_refs`。
- §3 的 latest 引用加了"Squid 版同句已核对"（L111），适用边界 L90 同步。

非阻断备注：

- BlueStore 原文是"checksums all … data written to disk"，说的是写入时计算；页内没有"每次读取都校验"的逐字句（初审已记）。正文把它放在"读路径（RADOS 层）"下，可以读成读路径校验。建议改成"落盘 checksum（读取时比对的逐字说明未见）"。
- 登记 revision 中的"forty 亿分之一"是中英混写笔误，建议改为"约四十亿分之一"。

### B20-C35 — P2 → OPEN

已满足：

- Lustre 行按 §23.5.1 补全了两类 checksum、读写两向、默认开启、adler32 可改、五次重试后返回 I/O error（L135），本轮逐句核对一致。
- `BAD WRITE CHECKSUM` 已注明为写方向日志。
- "不能发现"限定为 ldiskfs OST；ZFS OST 记为 unknown。
- 持久化/修复一栏改为 e2fsck/ZFS scrub/LFSCK，并注明 LFSCK 不是内容校验。
- 证据栏给出手册链接与节号。

剩余问题：登记没有补。`sources/registry.yaml` L5009–5019 的 `src.lustre.ops-manual-2x` revision 仍只写"核对 striping/DoM/FLR/llite/ldlm 章节"，notes 也没有 §23.5.1；全文件检索 "23.5.1" 没有命中。但正文 L135 证据栏写"登记 src.lustre.ops-manual-2x 已补 §23.5.1"，修订映射 L149、L153 也这样声称。这是读者可见的不实陈述。

剩余关闭条件：在该登记的 revision 或 notes 中实际补上 §23.5.1 Lustre Checksums（含 §23.5.1.1 算法）；或者删去正文 L135 的"已补"字样，改为引用对象存储正文 §4/§5 已列的 §23.5.1。修订映射对应行要按实际情况改。

### B20-C36 — P2 → CLOSED

- 碰撞分为随机漏检（引 BlueStore Squid 原句，已核对）和对抗碰撞（"不在本库来源覆盖内，unknown"）（L127）。
- 循环引用已解除：L121 的"见下文"现在指向 L127 的实际内容，L127 不再回指。
- 签名：所选 safetensors 格式内无签名字段（README §Format，本轮核对属实）；hub/RGW 签名机制记 unknown（L124、L127）。
- 可信清单写出了信任锚条件：同信道哈希只证明"与该信道声称值一致"，清单独立获取与保护方式 unknown，本库约定另注（L127）。

非阻断备注：L124 证据栏"safetensors README §Format（见制品传输登记注）"没有直接链接。`src.hf.safetensors-v0.7.0` 已在 `source_refs`，所以可以追溯。L127 的"见 T04-03 §5"见 C40。

### B20-C37 — P2 → CLOSED

- "缺样"改为"缺片/缺成员"（L141）。
- 补了 DCP 实例化段（L146）：`.metadata` 中 `storage_data` 对应清单；完整读回要覆盖每个 `(relative_path, offset, length)`；结构检查只是形状断言；MindIO 文件个数检查只覆盖部分缺片。这些事实与 §2 一致。
- 第 4 步分了两种情况：训练 checkpoint 指向恢复一致性"恢复后验证"（L144 有链接）；推理制品写"归 T07-01，未交付，unknown"（L139）。
- 错误×步骤对照用一段文字写出（L146）。
- 交叉引用的落点已核对：错版"见对象存储 §5"对应 `object-and-parallel-storage.md` §5 的身份三层定义（L82–84）；缺片与静默改动"见制品传输 §3"对应该页 §3 的部分发布与端到端校验两行。

### B20-C38 — P2 → CLOSED

- hub 条改为"测试期望值为 `"XXXXent"` 但 L804 缺 `assert`（测试未强制）"，并限定"反例含义以此为限"（L150）。本轮核对行号属实。"实现以长度为完成判据（见制品传输 §4）"与 `artifact-transfer-and-publication.md` §4 的长度检查行一致。
- Ceph/Lustre 两条已移为"检测信号（非反例）"（L151）。
- SRE 引了两条原则、validator 与两个案例，并注明"不外推到 AI checkpoint"（L152），四句都已核对原文。正文说"should not rely upon replication"与"写入前已错的字节会被多副本忠实保存"同义。原文同章另有 "Datastores that automatically sync multiple replicas guarantee that a corrupt database row or errant delete are pushed to all of your copies"，可以支持这一说法；如改引这句会更直接，但不要求。
- "Google Music 2012 误删数周后发现"与原文"over a month"相容。

### B20-C39 — P2 → OPEN

已满足：

- 来源记录新增"主张—来源定位表"，§5–§8 各主张都对应到登记 ID 与页/节/行（来源记录 L7–15）。
- NFS 依据改为 nfs(5) 与 RFC 8881，`source_refs` 已同步。
- SRE 在正文 L152 有落点。
- `verification.notes` 改为写明两轮取证范围与 unknown（L47）。来源记录 L3 也说明第二轮有远程取证，前后不再矛盾。

剩余问题：初审关闭条件"Lustre §23.5.1 补入登记"没有落实（见 C35）。`verification.notes` 列出了"Lustre §23.5.1 全文"，但登记没有对应记录。另外，来源记录 NFS 行没有列出 COMMIT/write verifier 的依据。该主张经 T04-02 §3 转引 RFC §18.32/§18.3，建议在定位表中写明这个转引路径（非阻断）。

剩余关闭条件：与 C35 同一处修订（登记补 §23.5.1，或改写正文和映射中的"已补"）。

### B20-C40 — P3 → OPEN

已满足：

- 来源节已合并成一个（L107–114），新增节来源并入其中（L113）。全页只剩一个来源节，满足"或合并两个来源节"。
- 适用边界补了 NFS/RGW/Lustre/hub/safetensors 的版本锚（L91）。
- "待确认"去掉了已回答的"其他存储系统 scrub 等价物"，补入签名、Xet、实测等项（L114）。
- `related_ids` 补了四个 ID（L27–29、L31）。
- 04 索引 L28 的摘要已更新。
- T07-01、T04-07 都加注了"未交付"。

剩余问题：

1. 定义节 L54 前半句已扩展为"字节损坏、版本错误、真实性缺失、训练状态错误分开判定"，但句末仍保留"本文只管'字节/文件是否损坏'这一层证据"，与同一段前文以及 §5–§8 矛盾。
2. L127 的"见 T04-03 §5"没有链接，也不是未交付任务。读者看到的是计划 ID，应改为指向 `object-and-parallel-storage.md` 的链接，L121 已有这样的写法。

非阻断备注：四个新增节标题带"（T04-05 新增）"。库内 03 等域也有标题带任务 ID 的先例，本轮不据此判 OPEN。04 索引 L43 的覆盖说明仍只写"四层校验边界"，可顺手同步。

剩余关闭条件：L54 末句改为与扩展后的范围一致，例如删去"只管…这一层"，或改为"字节、版本、真实性分层判定；训练状态正确性以 06 为主"。L127 的"T04-03 §5"改为文档链接。

## acceptance 对照

| acceptance | 判定 | 相关发现 |
|---|---|---|
| 1 原语对照与碰撞/真实性/可信清单/语义边界 | 满足 | C36 CLOSED |
| 2 选定后端读路径/持久化/scrub-checksum；不把 RADOS scrub 当 RGW 端到端 | 未满足：NFS 行有 TCP 事实错误和自相矛盾的断言；Lustre 行内容正确，但证据指针仍指向不存在的登记内容。RGW 行与"RADOS scrub ≠ RGW 端到端"满足 | C33 OPEN（P1）、C35 OPEN；C34 CLOSED |
| 3 验证链与四类错误区分 | 满足 | C37 CLOSED |
| 4 官方反例；证据保留/隔离/恢复点/恢复后校验链接到专门流程 | 满足 | C32、C38 CLOSED |

横向问题：C39 OPEN（与 C35 同一登记缺口）、C40 OPEN（定义句与一处计划 ID）。

## 结论

**T04-05 定向复核未通过：CLOSED 5（C32、C34、C36、C37、C38）/ OPEN 4（C33、C35、C39、C40）。** 按严重度看，OPEN 中有 P1 ×1（C33）、P2 ×2（C35、C39）、P3 ×1（C40）。剩余工作量小，集中在四处：

1. NFS 行删去"TCP 下无传输校验"，把"NFS 协议无端到端内容校验"改为只记 unknown，并补后端文件系统校验 unknown（C33）。
2. `src.lustre.ops-manual-2x` 登记实际补上 §23.5.1；或者删去正文 L135 与修订映射中的"已补"（C35、C39）。
3. L54 定义句末句与新范围对齐（C40）。
4. L127 的"T04-03 §5"改为链接（C40）。

修订后需要按上述 ID 再做定向复核。`verification.status: source_checked` 在 C33/C35/C39 关闭前不应视为对新增节成立。本报告只覆盖编辑与来源层面，未执行任何实测；所有后端行为仍是文档或实现层证据，不得标为 reproduced。
