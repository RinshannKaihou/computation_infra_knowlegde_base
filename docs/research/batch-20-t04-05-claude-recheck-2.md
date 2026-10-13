# 第二十批 T04-05 第二次定向复核（作者第三轮修订后）

复核日期：2026-10-13（实际取证日）。审阅模型 `claude-opus-5-5`，由用户本次明确要求。这不是既有的 `gpt-6.1-sol / xhigh` 批量审阅约定，也不改写该约定；推理等级等运行元数据没有可核验记录，不补造。审阅者角色独立于作者修订角色。

**结论：T04-05 第二次定向复核未通过。本轮范围 4 项（C33、C35、C39、C40）：CLOSED 3（C35、C39、C40），OPEN 1（C33，P1）。B20-C32–C40 合计 9 项：CLOSED 8，OPEN 1。** C33 剩下的只有一处：NFS 行新写入的"TCP 16-bit checksum（弱）"没有任何已登记来源支撑，也没有采用前次复核给出的三种处理方式之一。事实本身正确，问题在于证据。本轮没有发现新的事实错误，不新增发现 ID。

本轮只做只读核对：未改作者正文、来源记录、修订映射、登记、索引或计划；未执行保存、损坏注入、scrub、repair 或任何读写试验。模型审阅不构成硬件或现场验证。

## 输入（以 SHA-256 识别）

| 输入 | SHA-256 |
|---|---|
| T04-05 正文 `knowledge/04-data-storage/checkpoint-integrity-evidence.md`（153 行，concept / draft） | `3c5257326d9f1051c349e76cb406a7ebc07d2a37f4583a147d5513152aea536f` |
| 修订映射 `docs/research/batch-20-review-fixes.md`（T04-05 第三轮节 L160–164） | `94ef49a6af8a67fb4706cef0bd510ed93f41b5c5c05758999b3e97b9ecfe998c` |
| 前次复核 `docs/research/batch-20-t04-05-claude-recheck.md`（关闭条件权威来源） | `af08cbf14726384231382c45b3fcf00e8c2d3e4acc2f10af11f076bb2b683ac8` |
| 任务计划 `plans/full-coverage-backlog.yaml`（T04-05 acceptance L5220–5224） | `f16309beadf5ae4f28d5fc7428a2348bea0cf08d155d57730a4d817cfcdd3e96` |
| 来源登记 `sources/registry.yaml`（410 项；`src.lustre.ops-manual-2x` L5009–5019） | `fb27b7e4bd0e21373a2a6ca91e2e7b1699caa95a51531ccea84c90f71e4ddcca` |
| 链接落点 `knowledge/04-data-storage/object-and-parallel-storage.md`（§5 L82–84） | `e5ec20ce4ecb2254f6bf1631a749a194b9eda3daf13517fc120dd391b3ca1e8b` |

前五项 SHA-256 前缀与任务说明一致（`3c5257326d9f1051`、`94ef49a6af8a67fb`、`fb27b7e4bd0e2137`）。`make check` 结果见文末。

## 一次源重取（审阅者独立获取）

用 `curl -sS` 只读获取，默认 TLS 校验，HTTP 均为 200。原文只存放在 `/tmp/b20rc6/`，未入库。HTML 去标签后按文字核对。

| 来源 | SHA-256（原文） | 本轮核对点 |
|---|---|---|
| [nfs(5)](https://man7.org/linux/man-pages/man5/nfs.5.html) | `2b9d9223f2faeadffdc7c50936a7d03ae0a194c25d9fc3d1662d40dd22e534fb`（与前两轮字节相同） | "Using NFS over UDP on high-speed links such as Gigabit can cause silent data corruption"；"the UDP checksum is 16 bit only, so there is a chance of 1 in 65536 that it will match even if the packet payload is completely random"；`soft` 节 "Using NFS over TCP … may mitigate some of the risks"。**全页 "checksum" 只出现在 UDP 段落，没有任何关于 TCP 校验和或其强度的表述。** → C33 |
| [Lustre Manual 2.x](https://doc.lustre.org/lustre_manual.xhtml) | `63b09d0650de3491eee9c976dff1246706dc6496bc996c139fdebdf7fc4a0d8c`（与前两轮字节相同） | §23.5.1："two types of data checksums: in-memory … and wire"；"a 32-bit checksum of the data read or written on both the client and server"；"The ldiskfs backing file system does NOT do any persistent checksumming"；"enabled, by default"；"re-read or re-write the affected data up to five times … an I/O error is returned"。§23.5.1.1："By default, the Lustre software uses the adler32 checksum algorithm"，wire 算法可经 `checksum_type` 改；in-memory 固定优先 adler32。→ C35/C39 |

取证限制：RFC 9293 本轮没有重取。前次复核已取得 §3.1 原文（SHA-256 `6d9ac8be…`），确认 TCP 头部有覆盖头部和数据的 16-bit checksum；它仍未登记，所以只用来判断正文事实是否正确，不能当作正文的证据。RFC 8881 与 T04-02 §3 的转引路径同前次复核，没有重取。

## 逐项判定

### B20-C33 — P1 → OPEN（剩 1 处来源缺口）

前次剩余关闭条件逐条对照（正文 L133）：

1. **删去"TCP 下无传输校验" — 已满足。** 原错误表述已删去，事实方向现在正确：TCP 有 16-bit checksum。UDP 一段（高速链路静默损坏、约 65536 分之一误匹配）与 nfs(5) 原文一致；65536 的概率挂在 UDP 后面，没有错挂到 TCP。
2. **"NFS 协议本身无端到端内容校验"改为只记 unknown — 已满足。** 现在写的是"NFS 协议层端到端内容校验未见对应机制（unknown，不作'没有'断言）"，前后自相矛盾的问题已消除。
3. **补"服务器后端文件系统校验：实现相关，unknown" — 实质满足。** 已写入，但放在"持久化/修复"栏，不在前次条件所说的读路径栏。读者能看到这条 unknown，所以不据此判 OPEN；作为非阻断备注记录。

未满足的剩余问题：

- **TCP 校验的来源。** 前次关闭条件写明："若引 RFC 9293，需先登记，或改用已登记来源，或只写 unknown。"作者三种都没做。正文直接断言"TCP 16-bit checksum（弱）"，同一行的证据栏只有 nfs(5) 和 `local-and-shared-storage.md` §3。nfs(5) 不含 TCP checksum 的任何表述（见上表），登记中也没有 RFC 9293 或其他 TCP 规范（全文件检索 "9293" 没有命中）。括号里的"（弱）"是强度判断，同样没有来源；前次建议的说法是"漏检率 nfs(5) 未给，unknown"。
- 修订映射 L162 写"TCP 16-bit 弱校验＋原文 65536 误匹配概率"，容易被读成 65536 来自 TCP 的原文。正文实际挂在 UDP 后，没有问题；映射措辞建议顺手改清楚（非阻断）。

剩余关闭条件（选其一）：

- 在 `sources/registry.yaml` 登记 RFC 9293，revision 写明 §3.1 Header Format 的 Checksum 字段；在 L133 证据栏加入该来源，并加入 `source_refs`/`evidence_refs`。"弱"改为可溯源的描述（例如"16-bit，与 UDP 同位宽"），或者删掉；或者
- 不引 RFC：把 TCP 一句改为"TCP 传输层校验及其漏检率在已登记来源中未给出（unknown）"，删去"（弱）"。

两种做法都需要同步修订映射。

### B20-C35 — P2 → CLOSED

- 登记已补：`src.lustre.ops-manual-2x` 的 revision（L5014）现在写着"§23.5.1 Lustre Checksums（in-memory/wire 两类、读写两向、五次重试后 EIO、默认 adler32；ldiskfs 范围）"。逐项对照本轮重取的手册原文，都一致；"默认 adler32"对应 §23.5.1.1，满足前次"含 §23.5.1.1 算法"的要求。
- 正文 L135 证据栏"登记 src.lustre.ops-manual-2x 已补 §23.5.1"现在属实，读者可见的不实陈述已消除。
- 正文 Lustre 行其余内容与前次相同，前次已逐句核对一致。

非阻断备注：登记里"ldiskfs 范围"措辞偏简略。原文的意思是"ldiskfs 后端不做持久化 checksum"，不是"checksum 只适用于 ldiskfs"。可改为"ldiskfs 后端无持久 checksum"，免得读反。

### B20-C39 — P2 → CLOSED

前次剩余关闭条件与 C35 是同一处登记缺口，登记已经补上（见 C35）。`verification.notes`（L47）列出的"Lustre §23.5.1 全文（两类 checksum/重试/EIO/adler32）"现在有登记记录对应，修订映射 L163 与实际一致。

非阻断（前次已提，仍未处理）：来源记录 NFS 行没有写 COMMIT/write verifier 经 T04-02 §3 转引 RFC 8881 §18.32/§18.3 的路径。

### B20-C40 — P3 → CLOSED

- **定义句末句（L54）。** "本文只管'字节/文件是否损坏'这一层证据"已删，换成"字节/版本/真实性/状态四类证据的划分见下文新增节"，与同段前文及 §5–§8 不再矛盾。
- **L121/L127 链接。** 两处"T04-03 §5"现在都是指向 `object-and-parallel-storage.md` 的 Markdown 链接，`make check` 能解析。落点核对：该页 §5（L82–84）写有"端到端哈希本库设计约定：SHA-256，由发布方在发布前计算并写入清单，读回方重算比对"，与 L127 括注"本库约定为发布方写入、读回方重算"一致。前次复核把 L121 的写法当作范例，本轮按同一标准判定关闭。

非阻断备注：

- 两处链接文字仍是计划 ID"T04-03 §5"，同表 L122/L123 用的是"对象存储 §2/§3"。改成"对象存储 §5"会更统一，读者也不用知道计划 ID。
- L54 说"四类证据"指字节/版本/真实性/状态；验证链节（L139–144）的"四类错误"是缺片/错版/静默改动/训练状态错误，真实性另在原语对照节。两组"四类"不是同一套划分，可考虑把 L54 的"见下文新增节"写具体（例如"见校验原语对照与验证链两节"）。
- 04 索引 L43 的覆盖说明（前次已提）本轮不在范围内，未核对。

## acceptance 对照

| acceptance | 判定 | 相关发现 |
|---|---|---|
| 1 原语对照与碰撞/真实性/可信清单/语义边界 | 满足 | C36 CLOSED（前次）；C40 链接已修 |
| 2 选定后端读路径/持久化/scrub-checksum；不把 RADOS scrub 当 RGW 端到端 | 未满足（仅剩证据层缺口）：NFS 行事实方向已正确，但 TCP 校验的断言没有已登记来源。Lustre 行登记已补；RGW 行满足 | C33 OPEN（P1）；C34、C35 CLOSED |
| 3 验证链与四类错误区分 | 满足 | C37 CLOSED（前次） |
| 4 官方反例；证据保留/隔离/恢复点/恢复后校验链接到专门流程 | 满足 | C32、C38 CLOSED（前次） |

横向：C39、C40 CLOSED。

## 结论

**T04-05 第二次定向复核未通过。本轮 4 项：CLOSED 3（C35、C39、C40）/ OPEN 1（C33，P1）。B20-C32–C40 累计：CLOSED 8 / OPEN 1。**

剩下的工作只有一处：L133 的"TCP 16-bit checksum（弱）"要么登记 RFC 9293 §3.1 并在证据栏引用（同时去掉或溯源"弱"），要么改写为 unknown；修订映射同步。改完后只需对 C33 做定向复核。`verification.status: source_checked` 在 C33 关闭前不应视为对 NFS 行成立。本报告只覆盖编辑与来源层面，未执行任何实测；所有后端行为仍是文档或实现层证据，不得标为 reproduced。

`make check`：PASS（91 content entries / 410 sources，作者复核报告交付后运行；只校验结构与本地链接）。
