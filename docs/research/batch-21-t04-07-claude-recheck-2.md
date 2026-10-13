# 第二十一批 T04-07 第二次定向复核（作者第二轮修订后）

复核日期：2026-10-13（实际取证日）。正文 `updated_at: "2026-10-14"` 视为交付标签。

**结论：未通过。复核范围为 B21-C10、C12–C18，共 8 项（C11 已 CLOSED，不重开）：CLOSED 0，OPEN 8（P1 ×3：C10、C12、C13；P2 ×4：C14、C15、C16、C17；P3 ×1：C18）。** 本轮不新增发现 ID。新查出的事实或逻辑问题按原 ID 追记，共 5 处：

- C10：PG 页原文的 HTML 段落结构表明，"权威性不可证"属于 Filestore 限定段，正文却加粗写成适用于所有情形的结论。
- C12："multipart Complete 可见"引用的上游节本身把该项记为 unknown。
- C13：Lustre 的 failed recovery 同时出现在停止条件和完成条件中。
- C13：NFS 的"grace 超时"停止条件与"grace 结束"完成条件相互冲突。
- C16：正文对 §38.2.7 的概括与手册原文不符。

第二轮修订已落实的部分：Filestore/BlueStore 限定方向已改正；三个表的格数一致；可读/完整判据已对调；三类动作各有停止条件；plan 未用来源已写明理由；登记行数已改正；L52 的修订说明已删除。仍未关闭的缺口有六处：

1. 存储侧停止条件与完成条件互相矛盾，且来源标注不一致。
2. 一个判据单元格的引用与其来源的 unknown 冲突。
3. ext4 责任边界一格仍保留被指出的原句。
4. Lustre 凭据格仍没有节号。
5. source_refs 与正文链接不一致。
6. 正文仍残留计划 ID 和元数据说明。

`make check` 通过（93 content entries / 417 sources），它只校验结构和本地链接，不说明技术正确性。

审阅者角色独立于作者修订角色。审阅模型为 `claude-opus-5-5`，由用户明确要求使用；这不是既有的 `gpt-6.1-sol / xhigh` 批量审阅约定，也不改写该约定。推理等级等运行元数据没有可核验记录，不补造。本轮只读：只写本报告；未改作者正文、来源记录、修订映射、登记、索引或计划；未运行 `make build`；未执行任何故障注入、repair、remount、重连或演练。模型审阅不构成硬件或现场验证。

## 输入（以 SHA-256 识别）

| 输入 | SHA-256 前缀 | 核对 |
|---|---|---|
| [T04-07 正文](../../knowledge/04-data-storage/storage-client-backend-recovery.md)（96 行，procedure / draft） | `5e45ff09101094fa` | 与任务单一致 |
| [作者来源记录](batch-21-t04-07-sources.md)（24 行） | `b790ba0e08f8b488` | 任务单未给前缀，为本轮实测值 |
| [修订映射](batch-21-review-fixes.md)（T04-07 第二轮修订节 L42–51） | `cda575fc7d88b799` | 同上 |
| [前次复核报告](batch-21-t04-07-claude-recheck.md)（剩余关闭条件的权威来源） | `b5a95b4de0c5c881` | 同上 |
| [任务计划](../../plans/full-coverage-backlog.yaml)（T04-07 L5303–5323） | — | acceptance L5308–5311 已逐条对照 |
| [来源登记](../../sources/registry.yaml)（417 项） | — | 项数与任务单一致；L4874、L4907、L4995、L5165–5170 已核 |

旁证（只读本库现行草稿）：

- [本地与共享存储](../../knowledge/04-data-storage/local-and-shared-storage.md)：§2 L64–77、§3 L79–92、§5 L105–116。
- [对象与并行存储](../../knowledge/04-data-storage/object-and-parallel-storage.md)：§2 L53、§5 L88。
- [负载基线](../../knowledge/04-data-storage/storage-workload-baselines.md)：节标题与全文中"恢复/分布"的检索结果。
- [恢复诊断指南](../../knowledge/06-training/checkpoint-state-recovery-triage.md)：L36–42、L63。
- `src/kb/cli.py` L78：注释说明不检查链接片段。

## 一次源重取（审阅者独立获取）

全部用 `curl -sSL` 只读获取，默认 TLS 校验，HTTP 均为 200。原文只放在临时目录 `/tmp/b21rc7b/`，未入库。

| 来源 | SHA-256 前缀 | 与前次比对 | 本轮核对点 |
|---|---|---|---|
| Squid PG 排查页 | `aa7e11cea56b65d8` | 同 | HTML 段落边界：`This material is relevant for Filestore, but not for BlueStore …` 是一个新 `<p>` 的首句，同一段接着写 `cannot prove that any specific copy is in fact authoritative`、`favors the data on the primary`、`human intervention is necessary`。前一段以 `might prefer manual repair to ceph pg repair.` 结束。另有通用表述 `The pg repair command will not solve every problem.` → C10、C13 |
| Squid health-checks | `a6a9ed5466bb87fe` | 同 | `PG_DAMAGED`、`OSD_SCRUB_ERRORS`、`OSD_TOO_MANY_REPAIRS`（`mon_osd_warn_num_repaired`，default 10）、`BLUESTORE_SLOW_OP_ALERT` 均存在。`active+clean` 在全页只出现一次，位于 MON_DISK_BIG 的说明里，不是完成判据 → C12、C13 |
| Squid OSD 排查页 | `d835a6d2ce61b5bc` | 同 | 未改动部分，不复核 |
| Lustre 手册 2.x | `63b09d0650de3491` | 同 | §38.1.6 原文："a client is evicted by the server and must reconnect after having flushed its saved state"。§38.2.7 原文：gap 的两种来源是 lost replies 和 "clients missing from recovery"。所有客户端都已重连时，"the only possibility is … the reply was lost"，这些请求在恢复后处理。客户端未全部重连时，"the failed clients had requests that will no longer be replayed"，由 VBR 判断 gap 之后的请求能否安全回放。§38.4：版本不匹配时 "the client is evicted"。§38.4.1 列出 VBR 消息 → C13、C16 |
| Ceph RGW S3 索引 | `e48b4d877b49a9f8` | 前次未取 | 页面列有 ACL 与 bucket policy 的支持条目；没有 pool 命名、cephx 凭据或健康检查内容 → C15、C17 |
| ext4 admin-guide v6.16 | `2849c200bf743291` | 前 15 位与前次记录相同，第 16 位不同（前次记为 `c`，本轮为 `1`） | 前 60 位相同而内容不同几乎不可能，判断为前次报告的转录笔误，但无法证实。本轮已按本次取得的字节重新核对 `errors=` 原文 → C14 |
| nfs(5) | `2b9d9223f2faeadf` | 同 | 未改动部分，不复核 |
| osd-scrub-repair.sh @ v19.2.7（raw） | `3a696cb279d4274c` | 同 | `wc -l` 为 6258。L93、L106–107、L225、L233、L238、L242–244 与正文 L76 一致。`TEST_auto_repair_bluestore_*`（L382 起，共 5 个）与 `TEST_repair_stats`（L653）均存在 → C17 |

取证限制：

- tracker #8914、Squid release notes、RGW 健康/管理文档本轮仍未检索。
- `osd-scrub-repair.sh` 只核对了上列行。
- Lustre 手册只核对 §35.3、§38.1–38.4 相关段落。
- 表格渲染按 GFM 规则推断：本轮已逐行数过三个表的未转义分隔符，表头与各行一致，但没有看到实际渲染页面。
- 所有行为都是文档或源码层证据，未执行验证。

## 逐项复核

### B21-C10 — P1 / OPEN（追记）

已满足：

- 条件 1 按字面已满足。L68 改为"无 checksum/手动修复材料针对 Filestore（BlueStore 有内部 checksum，不适用）"，方向与原文一致。"偏向 primary"前带有"无 checksum 时"。
- 条件 2 的前半部分：L67 已删除"从可信副本恢复见下"，改为"repair 单列见下（…不称'可信副本恢复'）"。
- repair 语义（标 missing、恢复不在 repair 范围内、auto_repair 条件与默认值 5）与原文逐句一致。

未满足：

- **事实问题（追记）**：本轮看了 HTML 段落边界。`This material is relevant for Filestore, but not for BlueStore` 开启的这一段，内容正是"checksum 不能证明任一副本权威 → 无 checksum 偏向 primary → 需人工介入"。因此"权威性不可证、需人工判断"在原文中**至少同样**属于 Filestore 限定的范围，不能在没有限定的情况下推广到 BlueStore。正文 L68 却把 `**权威性不可证**` 加粗写成 repair 的一般性质，L67 也重复了一次。Squid 默认的 BlueStore 读者会因此认为权威选择总是无法证明。这与初审 C10 指出的误导属于同一类（方向相反）。说明：前次报告的关闭条件 1 只依据纯文本把限定理解为指向前一段，本轮依据段落结构予以修正。这一偏差源于审阅侧，不归咎于作者。
- 条件 2 的后半部分：正文没有 repair 以外的"从可信副本恢复"流程（2015 博客的手动流程限于 FileStore，已降级），但没有写明"未取源，unknown"。acceptance 3 明确列出了"从可信副本恢复"。
- 条件 3：修订映射 L44 称"记录 unknown 第 6 条澄清"，但[来源记录](batch-21-t04-07-sources.md) L24 的第 6 条仍是 `repair 前清单外原文`，没有改动。只有 L9 的支持范围一栏加了"修复前清单即本链输出"。

剩余关闭条件：

1. L67–68 把"权威性不可证、偏向 primary、需人工判断"限定在 Filestore 或 checksum 不可用的情形。另写明 PG 页没有描述 BlueStore 下如何选择权威副本（unknown）。通用部分可保留原文的 `will not solve every problem` 与"Ceph 不自动修复"。
2. 写明 repair 以外的"从可信副本恢复"流程未取源（unknown）。
3. 改写或删除来源记录 L24 的第 6 条。

### B21-C12 — P1 / OPEN（追记）

已满足：

- 补了 ext4 行（L84），引用本地与共享存储 §5，并记录"无 ext4 专用重连协议"为 unknown。
- 可读/完整已对调：L87 用 `rados get` 成功（测试 L243），L88 用 `diff` 一致（L244）加 PG 健康状态，与前次条件一致。
- NFS、Lustre、故障域三行带有来源或"本库约定"。

未满足：

- **引用冲突（追记）**：L89 的"multipart Complete 可见（见对象与并行存储 §2）"与来源矛盾。对象与并行存储 §2 L53 原文为 `Complete 前后可见性与列举一致性 Squid 文档未写明（unknown）`，"对象可见"只是该文 §5 L88 的设计预期。正文把上游的 unknown 当成了有来源的预期。
- L90 负载恢复的"预期"为"恢复到基线分布内"，既没有来源，也没有标"本库约定"。负载基线一文没有定义恢复判据；它的链接放在"前置"一栏，不能为"预期"提供依据。修订映射 L45 称"预期全带链接/约定"，与实际不符。
- 次要问题：
  - L84 ext4 的"预期"把 §5 的前置条件"日志回放完成"当成了预期，却漏了 §5 的预期"回放后文件系统一致"，以及"commit 窗口内数据状态 unknown"。
  - L88 的"PG 回到 `active+clean`（见 health-checks）"：health-checks 页没有把 `active+clean` 作为判据（见取证表），应改引 PG 排查页，或标为本库约定。

剩余关闭条件：

1. L89 改引对象与并行存储 §5 的设计预期，并保留 §2 的可见性 unknown。
2. L90 的"预期"标"本库约定"，或给出来源。
3. 订正 L84 的预期和 L88 的 `active+clean` 归属（次要，可与上两条一起处理）。

### B21-C13 — P1 / OPEN（追记）

已满足：

- L72 已按 Ceph/NFS/Lustre 分列停止条件。
- 完成条件中，Ceph 链接了 health-checks，deep scrub 一项标为本库约定。
- NFS 完成条件带链接，并沿用了上游的 reclaim/grace unknown。

未满足：

- **逻辑矛盾（追记）**：Lustre 的停止条件是"进入 failed recovery 即停"，完成条件却是"recovery 完成**或进入 failed recovery 分支**并记录"，而 L72 末句规定"任一未满足不进入训练侧"。按这些写法，failed recovery 既触发停止，又满足完成条件，因而可以进入训练侧。手册 §38.1.6 写明 failed recovery 时客户端被驱逐，并须清掉与该服务器相关的保存状态。把它算作"完成"会让未回放的状态被当作已恢复。
- **逻辑矛盾（追记）**：NFS 的停止条件"grace 超时即停"与完成条件"grace 结束"指的是同一事件，无法区分。按本意，前者应当是"grace 结束时 reclaim 仍未完成"。本地与共享存储 §3 L90 没有任何停止判据，而且把 Linux grace 时长记为 unknown，所以"见 §3"不能作为这条停止条件的来源。
- Ceph 停止条件的来源标注前后不一致：L68 标"本库约定"，L72 同一条件写"见 PG 排查页"。PG 页没有给出 repair 后的停止判据（只有 `will not solve every problem` 与"需人工介入"），应统一标为本库约定，可附 PG 页作理由。
- ext4 没有停止条件。ext4 的完成条件"回放/检查完成"既没有链接，也没有标约定或 unknown，不满足"完成条件逐条链接来源"。

剩余关闭条件：

1. Lustre 完成条件删去"或进入 failed recovery 分支"。failed recovery 只作停止或升级分支，并引 §38.1.6 的驱逐与状态清除。
2. NFS 停止条件改为可与完成条件区分的表述，标为本库约定，并带上 grace 时长的 unknown。
3. Ceph 停止条件在 L68 与 L72 统一标注。
4. 给出 ext4 的停止条件与完成条件来源（可引本地与共享存储 §2 jbd2 与 §5），或记为 unknown。

### B21-C14 — P2 / OPEN

已满足：

- 条件 1：三个表都没有格数错位。§1 每行 4 个未转义分隔符，即 3 格；L48 的 `\|` 已转义。
- 条件 2：Ceph（L50）的 `read_error` 与 `data_digest_mismatch` 示例与 PG 页一致。Lustre（L51）的 `health_check` "not healthy" 加 ldiskfs 只读示例与 §35.3.2 一致。
- 条件 3 的一半：L48 第 2 格已改为"转只读说明检测到文件系统错误，`errors=` 只决定检错后的反应方式"。

未满足：同一行第 3 格"故障责任边界"仍保留原句 `转只读事件指向 errors 配置`，与本行第 2 格以及 admin-guide 原文矛盾。

剩余关闭条件：把 L48 第 3 格改为与第 2 格一致的判据（例如"转只读指向设备/驱动/文件系统检出错误；`errors=` 只是反应方式"）。完成后 C14 即可关闭。

### B21-C15 — P2 / OPEN（追记）

已满足：

- NFS 凭据一格引 `sec=krb5*`/nfs(5)，超出部分记 unknown。
- Ceph 一格链接了 S3 索引并记"细节 unknown"。索引页有 ACL/bucket policy 条目，可以作为入口。
- ext4 凭据一格选了"不适用"并写了理由。
- `OSD_TOO_MANY_REPAIRS` 的阈值已直接写入，与原文一致。

未满足：

- L58 Lustre 凭据格仍为 `同左按手册；超出 unknown`，没有节号。"同左"指向 NFS 的 `sec=krb5*`，不适用于 Lustre。前次条件已点名此格。
- **事实问题（追记）**：L59 ext4 超时格写的理由是"单机同步 I/O 模型"，与本库自身来源矛盾。本地与共享存储 §2 L75 记载，ext4 有脏页回写与 delalloc（异步回写）。"ext4 无超时挂载语义"可以成立，但不能用"同步 I/O"作理由。块层命令超时等是否属于本格范围，没有来源（unknown）。
- 次要问题：L58 ext4 的"路径/挂载/权限按实现检查"既没有来源，也没有记 unknown。Ceph 格的"池"命名与 cephx 凭据不在 S3 索引的范围内，目前由"细节 unknown"兜底，可以接受。

剩余关闭条件：

1. Lustre 凭据格给出手册节号，或改为明确的 unknown（并删去"同左"）。
2. 删除或改正 ext4 超时格的"同步 I/O"理由。

### B21-C16 — P2 / OPEN（追记）

已满足：

- repair（L68）、remount（L69）、回放（L70）各有独立的停止条件，均标为本库约定。
- remount 两处 unknown 保留。

未满足：

- **概括不符（追记）**：L70 写 `§38.2.7 Gaps 指回放序列中的空洞，须逐项解释来源`。手册原文已经给出了 gap 的两种来源与处理方式（见取证表）。"须逐项解释来源"不是手册内容；正文也没有写出 §38.2.7 真正的风险要点：客户端未全部重连时，缺席客户端的请求**不再回放**，gap 之后的请求是否回放由 VBR 按版本判定，版本不匹配时客户端被驱逐（§38.4）。前次关闭条件是"写出 §38.2.7 所述风险的要点"，本轮仍未达到。
- L70 的停止信号"版本号回退"在手册中没有对应的可观察输出。手册可观察的信号是 §38.4.1 的 VBR 消息（`Version mismatch during replay`、`version recovery fails`）和客户端驱逐。作为本库约定，这个信号无法在现场判定。

剩余关闭条件：

1. 按原文改写 §38.2.7 要点（两种来源、缺席客户端请求丢失、VBR 判定与驱逐）。
2. 把回放停止信号改为手册中可观察的信号（§38.4.1 消息、驱逐、§38.1.6），或在约定中说明如何观测。

### B21-C17 — P2 / OPEN

已满足：

- 来源记录 L20 写明了三项 plan 来源未使用的理由。这三项与 plan L5319–5321 一致，理由可以接受。
- 来源记录已按主张拆成逐行，Ch.36 标为"未使用"（L16）。
- source_refs 已补 `src.nfs-utils.exports-5-man7`（L4907 可解析）。
- 登记 L5170 的行数已改为 6258，与本轮 `wc -l` 一致。

未满足：

- 正文 L58 链接了 RGW S3 索引，来源记录 L17 也列了 `src.ceph.docs-rgw-s3-squid`，但正文 source_refs（L8–17）没有这一项。初审的核心条件"source_refs 与依据一致"因此仍未满足。
- 来源记录 L14 列了 `src.kernel.docs-nfs-v6.16`，applicability.notes（L29）也声称以"内核 v6.16 NFS…文档"为证据样板，但正文没有引用内核 NFS 文档，source_refs 中也没有。应二选一：补引用和 source_refs，或从记录和 notes 中删去。
- 次要问题：来源记录 L11 仍写"阈值细节 unknown"，与正文 L61 已写入的默认值 10 不一致。L3 仍写"Ch.35/36/38 节号"，与 L16 的"Ch.36 未使用"不一致。

剩余关闭条件：

1. source_refs 补 `src.ceph.docs-rgw-s3-squid`。
2. 处理 `src.kernel.docs-nfs-v6.16` 的去留，使正文、notes、记录三处一致。
3. 订正来源记录 L3 和 L11（次要）。

### B21-C18 — P3 / OPEN

已满足：

- L52 的修订说明已删除。
- 训练指南的链接改为带节名的链接（"适用范围与前置条件"，L36 存在）。
- 其余计划 ID 已改为带节号或节名的文档链接。本库检查器不校验链接片段（`src/kb/cli.py` L78），同批文档对中文节标题的惯例也是在链接文字中写节名，因此本轮按此接受，不强求 `#` 片段。

未满足：

- L90 的链接文字仍为 `T04-06 基线`，读者可见。
- L78 末尾仍有元数据说明 `（博客 kind 说明移至来源记录：schema 无博客类，沿用 documentation。）`。内容已移到来源记录 L18，但正文的这句没有删除。修订映射 L51 称"L80 移记录"，与实际不符。
- 次要问题：L66 写"…'适用范围与前置条件'第 1 步"，但该节（L36–42）是要点列表，不是步骤，应改为"首条"，或指向实际要点"先按写入与持久化边界确认…"。

剩余关闭条件：

1. L90 链接文字改为文档名或节名（例如"负载基线"）。
2. 删除 L78 末尾的说明句。
3. 订正"第 1 步"的措辞（次要）。

## acceptance 对照

| acceptance | 判定 | 相关发现 |
|---|---|---|
| 1 四类实现的证据入口与故障责任边界 | 大体满足：入口、表结构、Ceph/Lustre 判据示例均已到位；ext4 责任边界一格仍保留错误归因 | C14（P2） |
| 2 故障覆盖；恢复动作只引用选定实现条件 | 大体满足：Lustre 凭据格没有节号；ext4 超时理由与本库来源矛盾 | C15（P2） |
| 3 先保留证据与恢复点；按官方条件选择重连/恢复服务/从可信副本恢复；repair/remount/回放的风险与停止条件独立 | 未满足：repair 权威性结论越出 Filestore 限定；可信副本恢复没有记 unknown；存储侧停止与完成条件有两处矛盾；§38.2.7 要点不符 | C10、C13（P1），C16（P2） |
| 4 正式上游测试案例；五类演练判据（未执行） | 前半句满足（C11 CLOSED，本轮复核源码行号仍一致）；判据表中一格引用与上游 unknown 冲突，一格预期没有来源 | C12（P1） |

横向问题：C17（source_refs 与记录一致性，P2）、C18（计划 ID 与元数据残留，P3）。

## 结论

**T04-07 第二次定向复核不通过。复核范围 8 项（C10、C12–C18）：CLOSED 0，OPEN 8（P1 ×3：C10、C12、C13；P2 ×4：C14、C15、C16、C17；P3 ×1：C18）。连同前次已关闭的 C11，B21-C10–C18 共 9 项：CLOSED 1，OPEN 8。** 本轮不新增发现 ID，按原 ID 追记 5 处：C10 的 BlueStore 推广、C12 的 unknown 冲突、C13 的两处停止/完成矛盾、C16 的 §38.2.7 概括。

建议修订顺序：先改 C10 与 C13。前者影响 Squid/BlueStore 读者对 repair 的判断；后者让 failed recovery 可以进入训练侧。C14、C18 都只剩一两处文字改动。C10 与 C17 关闭前，正文的 `verification.status: source_checked` 不应视为成立。修订后应按上列"剩余关闭条件"再做定向复核。本复核只覆盖编辑与来源层面，所有存储行为都是文档或源码层证据，不得标为 reproduced。
