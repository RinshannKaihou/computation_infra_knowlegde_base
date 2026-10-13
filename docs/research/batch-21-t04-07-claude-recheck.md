# 第二十一批 T04-07 定向复核（作者首轮修订后）

复核日期：2026-10-13（实际取证日）。正文 `updated_at: "2026-10-14"` 视为交付标签。

**结论：未通过。B21-C10–C18 共 9 项：CLOSED 1（C11），OPEN 8（C10、C12、C13 为 P1；C14、C15、C16、C17 为 P2；C18 为 P3）。** 本轮没有新增发现 ID。新发现的事实错误按原 ID 追记：正文 L68 把 Squid PG 页中 "relevant for Filestore, but not for BlueStore" 的限定反写成"与 BlueStore 相关"，追记到 C10；§1 Lustre 行多出一格，按 GFM 规则责任边界一列会被丢弃，追记到 C14；登记中测试脚本行数写错，追记到 C17。大部分修订已经落地，包括定位链、repair 单列、主案例改为 v19.2.7 回归测试、§5 判据表、故障×实现表和改名。剩余缺口集中在四处：来源标注、按实现拆分停止条件、表格结构、正文残留的计划 ID。`make check` 通过（93 content entries / 417 sources），它只校验结构与本地链接，不说明技术正确性。

审阅者角色独立于作者修订角色。审阅模型为 `claude-opus-5-5`，由用户明确要求使用；这不是既有的 `gpt-6.1-sol / xhigh` 批量审阅约定，也不改写该约定。推理等级等运行元数据没有可核验记录，不补造。本轮只读：未改作者正文、来源记录、修订映射、登记、索引或计划；未运行 `make build`；未执行任何故障注入、repair、remount、重连或演练。模型审阅不构成硬件或现场验证。

## 输入（以 SHA-256 识别）

| 输入 | SHA-256 前缀 | 核对 |
|---|---|---|
| [T04-07 正文](../../knowledge/04-data-storage/storage-client-backend-recovery.md)（97 行，procedure / draft） | `0662e0cca55dc11a` | 与任务单一致 |
| [作者来源记录](batch-21-t04-07-sources.md)（18 行） | `b055c87669540a1b` | 与任务单一致 |
| [修订映射](batch-21-review-fixes.md)（T04-07 修订节 L28–40） | `ddeb3157f54b4ebf` | 与任务单一致 |
| [前次初审报告](batch-21-t04-07-claude-review.md)（关闭条件权威来源） | `eb0eff4c79d7c3af` | 任务单未给前缀，此为本轮实测值 |
| [任务计划](../../plans/full-coverage-backlog.yaml)（T04-07 L5303–5323） | — | acceptance L5308–5311 已逐条对照 |
| [来源登记](../../sources/registry.yaml)（417 项；新增 L5165、L5176、L5190） | `36798c806595b5bf` | 与任务单一致 |

旁证（只读本库现行草稿）：[本地与共享存储](../../knowledge/04-data-storage/local-and-shared-storage.md)（§2 L73 jbd2 replay；§3 L85–90 grace/reclaim/verifier；§5 L110–111）；[恢复诊断指南](../../knowledge/06-training/checkpoint-state-recovery-triage.md)（"步骤与判断分支"节 L63）；`04-data-storage/index.md` L11、L45；`docs/full-coverage-roadmap.md` L191；`schemas/sources.schema.json` L18（kind 枚举）。

## 一次源重取（审阅者独立获取）

全部用 `curl -sSL` 或 `git ls-remote` 只读获取，默认 TLS 校验，HTTP 均为 200。原文只放在临时目录 `/tmp/b21rc7/`，未入库。8 份原文的 SHA-256 **与初审取得的字节完全相同**，因此初审取证表仍然有效。本轮只补核修订后正文新增的主张。

| 来源 | SHA-256 前缀（与初审同） | 本轮核对点 |
|---|---|---|
| Squid PG 排查页 | `aa7e11cea56b65d8` | 原文："The pg repair command is able to make repairs even when checksums are not available to it, as in the case of Filestore. Users working with replicated Filestore pools might prefer manual repair … `This material is relevant for Filestore, but not for BlueStore, which has its own internal checksums.`" 紧接 "The matched-record checksum … cannot prove … authoritative. If there is no checksum available, pg repair favors the data on the primary"。auto_repair："erasure-coded and BlueStore pools … `osd_scrub_auto_repair` (default false) is set to true and if no more than `osd_scrub_auto_repair_num_errors` (default 5)"。→ C10 |
| Squid OSD 排查页 | `d835a6d2ce61b5bc` | Warning 原文 "Reef does not support FileStore. Releases after Reef do not support FileStore. … pertinent only to the Quincy release of Ceph and to releases prior to Quincy"，与正文 L68、L78 一致。→ C11 |
| Squid health-checks | `a6a9ed5466bb87fe` | `BLUESTORE_SLOW_OP_ALERT` 条目存在（"storage drive may be failing"）。`OSD_TOO_MANY_REPAIRS` 写了阈值 `mon_osd_warn_num_repaired`（default 10）。`PG_DAMAGED` 含 inconsistent、snaptrim_error 与 repair 进行中三种状态。→ C13、C15 |
| nfs(5) | `2b9d9223f2faeadf` | `sec=flavors` 的有效值为 none/sys/krb5/krb5i/krb5p。"generates a "server not responding" message after retrans retries"。TCP 默认 retrans 2、UDP 3。→ C14、C15 |
| ext4 admin-guide v6.16 | `2849c200bf74329c` | 原文 "errors=remount-ro Remount the filesystem read-only on an error … (These mount options override the errors behavior specified in the superblock …)"。→ C14 |
| Lustre 手册 2.x | `63b09d0650de3491` | 以下节号与标题均属实：35.3.1–35.3.3；35.3.8 "Handling Timeouts on Initial Lustre File System Setup"；38.1.1–38.1.5；38.2.7 "Gaps in the Replay Sequence"；38.4 "Version-based Recovery"；23.1.2/23.1.3。`lfs check servers` 出现 2 次。"not healthy" 出现在 §35.3.2 "OSTs Become Read-Only" 中，原文为 `health_check` 显示 "not healthy"。→ C14、C16 |
| osd-scrub-repair.sh @ v19.2.7 | `3a696cb279d4274c` | `refs/tags/v19.2.7` → `c24c6707…`，`^{}` → `9ec952b9…`。L93 `TEST_corrupt_and_repair_replicated`；L106 注释 tracker #8914，紧挨 L107 的**主副本**调用；L225–245 `corrupt_and_repair_one`，L233 remove、L238 repair、L242 list-attrs、L243 `rados get`、L244 `diff`。文件共 **6258 行**（`wc -l`，末尾有换行）。→ C11、C12、C17 |
| 2015 博客 | `3b3e2c97d4f8fe08` | 与初审同字节；正文 L78 的四处细节与初审核对一致。→ C11 |

取证限制：

- tracker #8914、Squid release notes、RGW 健康/管理文档本轮仍未检索。
- `osd-scrub-repair.sh` 只核对了 L90–112 与 L222–248。
- 正文 §1 Lustre 行的渲染结果是按 GFM 表格规则推断的（本地 venv 无 markdown 渲染库，也没有运行 `make build`），没有看到实际渲染页面。
- 所有行为都是文档或源码层证据，未执行验证。

## 逐项复核

### B21-C10 — P1 / OPEN（追记事实错误）

已满足：

- L65 写入了 `ceph health detail` → `list-inconsistent-pg` → `list-inconsistent-obj --format=json-pretty`，要求保存 JSON，`read_error` 分支先查 `dmesg`/`smartctl`。
- L68 把 repair 单列，写明"权威性不可证"、replicated pool 只标 missing、auto_repair 的条件（与原文一致），"丢数据"已标为本库推论。
- 正文 L97 已不再把"repair 前清单"列为待确认。

未满足：

- **事实错误（追记）**：L68 写 `Filestore/BlueStore 限定：上段材料与 BlueStore 相关`。原文是 `relevant for Filestore, but not for BlueStore, which has its own internal checksums`（见上表）。正文把限定方向写反了，并且把这段讲"无 checksum / 手动修复"的材料套到 Squid 默认的 BlueStore 上。读者会因此认为"无 checksum 时偏向 primary"是 BlueStore 的常规行为。
- L67 仍写 `从可信副本恢复见下（repair 单列）`，所指的"下"就是第 4 步 repair，等于又把 repair 和"从可信副本恢复"挂在一起。
- 来源记录 unknown 第 6 条改成了 `repair 前清单外原文`，含义不清：读者无法判断还有哪份原文未取得。

剩余关闭条件：

1. 按原文改写 L68 的限定：checksum 不可用、手动修复的材料针对 Filestore，BlueStore 有内部 checksum。若保留"无 checksum 时偏向 primary"，需说明它属于 checksum 不可用的情形。
2. L67 删去"从可信副本恢复见下"的指向；如果本文没有 repair 以外的可信副本恢复流程，就写明"未取源，unknown"。
3. 来源记录 unknown 第 6 条写明具体缺什么，或者删除。

### B21-C11 — P1 / CLOSED

依据：

- L78 写明博客的 FileStore 前提，以及"Squid（Reef 及以后）不支持 FileStore"（引 OSD 页，已登记 L5176），并把博客降为历史参考。两份 shard 不符、"先试 repair"、集群级 noout 三处差异都已写入。
- L76 主案例改为 v19.2.7 `osd-scrub-repair.sh`。函数名、L93、L225–244、步骤和 diff 判据与源码逐行一致；tracker 记为未打开。
- L5165 已登记该测试，kind 为 `repository`。
- 博客 kind：schema 的 kind 枚举（`sources.schema.json` L18）没有博客类，本库 `src.nvidia.hopper-in-depth-blog-2022-03-22` 同样用 `documentation`，处理一致。

附记（不影响关闭）：

- L106 的 tracker 注释紧挨 L107 的主副本调用，并非对整个函数的注释。
- 该测试的"损坏"方式是删除对象（L233），没有覆盖 digest 不一致时如何选择权威副本；正文没有夸大这一点。
- 登记的行数误差记入 C17。

### B21-C12 — P1 / OPEN

已满足：L82–92 已改为逐项表格，覆盖客户端重连、可读、完整、提交一致性、负载恢复、故障域六行七项，全部未执行、实际一栏留空，并写明执行授权。

未满足：

- 关闭条件要求按 ext4/NFS/Ceph/Lustre 分行，无来源的项记 unknown。表中**完全没有 ext4**，也没有记 unknown。[本地与共享存储 §5](../../knowledge/04-data-storage/local-and-shared-storage.md) L110 已有"本地重启可读"判据可以直接引用。
- 多数"预期（来源依据）"一格没有来源：
  - L89 `active+clean`、告警消除：未链接 health-checks。
  - L90 `COMMIT/verifier`、`multipart Complete`：未链接 T04-02 §3 L86 或 T04-03 的对应节。
  - L91 只写了计划 ID `T04-06 基线`。
  - L92 "域外无影响"：既没有来源，也没有标为本库约定。
- 可读与完整两行的判据可能放反了。L88 把 `diff` 一致放在"可读"，L89 用 PG 健康状态表示"完整"。按测试原意，`rados get` 成功对应可读，`diff` 一致对应完整；PG `active+clean` 是健康状态，不能证明数据完整。

剩余关闭条件：补 ext4 行（或写明 unknown 及原因）；每格"预期"带链接来源或标"本库约定"；核对可读与完整两行的判据归属。

### B21-C13 — P1 / OPEN

已满足：

- L66 只把训练指南用作下游交接，并写明不复用其停止条件。
- L72 写明"任一未满足不进入训练侧"。
- 完成条件已按 Ceph/NFS/Lustre/ext4 分列。

未满足：

- L72 的"本文自己的存储侧停止条件"仍是那三条通用条件（正确性失败、超时、观测窗口失效），与初审指出的、原本来自训练指南的条件相同，只是改了标签。它们没有按实现分列，没有来源，也没有标为本库约定。关闭条件要求"按实现分列并引来源"。
- 完成条件各项都没有链接：
  - Ceph `PG_DAMAGED` 应引 health-checks。
  - NFS reclaim/grace 应引 T04-02 §3。注意 T04-02 L90 自己把"reclaim 实际判据、grace 时长"记为 unknown，本文照搬成完成条件时需要带上这条 unknown。
  - Lustre 应引 Ch.38.1.6。
  - "下一次 deep scrub 无新错误"应标为本库约定。

剩余关闭条件：停止条件按实现给出（例如 Ceph：repair 后 `list-inconsistent-obj` 仍非空或出现 `read_error`；NFS：grace 超时；Lustre：进入 failed recovery），每条带来源或标本库约定或 unknown；完成条件逐条链接来源，并保留上游的 unknown。

### B21-C14 — P2 / OPEN（追记结构缺陷）

已满足：

- Lustre 行删除了 §1.2.2，改引 `health_check`/"not healthy"、`lfs check servers`、`lfs df`、Ch.35.3、Ch.38.1，节号与原文一致。
- RGW 写明"健康/管理文档未检索（unknown）"。
- "knfsd 类比不适用"已删除。
- ext4 加了 `errors=`，NFS 加了 "server not responding"，均与原文一致。
- NFS 行的责任判据示例符合要求。

未满足：

- **结构缺陷（追记）**：表头 L45 只有 3 格，L50 Lustre 行却有 4 格，因为插入了 `| [手册](https://doc.lustre.org/lustre_manual.xhtml) |`。按 GFM 规则，多出的单元格会被丢弃，结果是"故障责任边界"一列显示为"手册"链接，`客户端 vs MDS/MDT vs OSS/OST vs LNet 分开判定` 不会显示。这是按规范推断的，未实际渲染。
- 关闭条件要求"责任边界各写一条判据示例"。Ceph 行（L49）和 Lustre 行（L50）只写了"分开判定"，没有判据示例。
- ext4 行写 `转只读事件指向 errors 配置`，与原文不符。admin-guide 原文为 "Remount the filesystem read-only on an error"：转只读说明文件系统检测到了错误，`errors=` 只决定检测到错误后如何反应，不是故障原因。

剩余关闭条件：

1. 把 Lustre 行的手册链接并入第 2 格，使该行恢复为 3 格。
2. Ceph、Lustre 各写一条判据示例。可用的例子：Ceph `read_error` 指向介质或设备侧，`data_digest_mismatch` 指向副本不一致（PG 页）；Lustre `health_check` 为 "not healthy" 且 ldiskfs 只读，指向 OSS/OST 块设备（§35.3.2）。
3. 把 ext4 行改为"转只读说明检测到文件系统错误，`errors=` 决定反应方式"。

### B21-C15 — P2 / OPEN

已满足：

- L56–61 已改为故障类别×实现的结构。
- 超时行引 nfs(5) 的 hard/soft/softerr、timeo、retrans 与静默损坏风险，与原文一致。
- Ceph 池满与 Lustre Full OST 已分开写，§23.1.2/23.1.3 属实。
- 慢盘一格的两项健康检查条目存在。
- Lustre 超时引 35.3.8，并说明它只覆盖初始建联，与原文标题一致。

未满足：

- "路径/挂载/权限/凭据"一行有三格既没有具体来源，也没有明确记 unknown，没有达到"每格引用具体选项、健康检查或手册节，否则记 unknown"：
  - Ceph 格写"见 RGW 文档"，没有链接；而 `src.ceph.docs-rgw-s3-squid` 已从 source_refs 删除。
  - Lustre 格写"同左按手册"，没有节号。
  - ext4 格写 `凭据不适用（unknown 不适用项注明）`，语义不清。
- ext4 超时格写"不适用（unknown）"，"不适用"与 unknown 相互矛盾。
- 附带：L61 说 `OSD_TOO_MANY_REPAIRS` 的阈值"未核 unknown"，但 health-checks 原文已给出 `mon_osd_warn_num_repaired`（default 10）。可直接写入，也可保留 unknown 但改为"未逐项核对"。

剩余关闭条件：把上述各格改为具体来源（加链接与节号）或明确的 unknown；"不适用"与 unknown 二选一并说明理由。

### B21-C16 — P2 / OPEN

已满足：

- L68–70 已把 repair、remount、回放分成三步。
- Lustre 回放（38.2、38.2.7、38.4、38.1.6）与 OSD 服务恢复（`add-noout`/`set-group noout`、degraded、`unset`）已补齐，节号与原文一致。
- remount 两处未取源的风险已明确记为 unknown。

未满足：

- 关闭条件要求每类动作按实现写风险、前置、停止条件。三步都只写了风险或机制，**没有各自的停止条件**，仍然共用 L72 的通用条件。初审指出的"停止条件共用一组"没有解决。
- 回放一步的风险只有"依赖日志完整（实现保证 unknown）"，而手册 §38.2.7 "Gaps in the Replay Sequence" 本身就是可引的回放风险，正文只列了节号，没有写它的含义。
- L68 的事实错误（C10）落在 repair 一步。

剩余关闭条件：repair、remount、回放各写一条停止条件（带来源，或标本库约定或 unknown）；回放一步写出 §38.2.7 所述风险的要点。

### B21-C17 — P2 / OPEN（追记登记误差）

已满足：

- 文件与 ID 已改为计划 target `storage-client-backend-recovery`。index L11/L45、plan L5303–5304、roadmap L191 一致，除初审报告引文外全库无旧名残留。
- source_refs 8 项全部可解析，新增三项已登记。
- verification.notes 只写实际核对范围。

未满足：

- **plan 列出但未使用的来源没有说明理由。** `src.ceph.docs-scrubbing-latest-2026-10-08`、`src.ceph.repo-caf3def`、`src.google.sre-data-integrity` 在正文、来源记录、修订映射中都检索不到；修订映射 L39 自述"plan 不用来源说明"，但没有对应文字。
- 来源记录 L14"客户端/后端证据"一行的 ID 一栏写 `T04-02/03 登记复用`，支持范围一栏写 `见各自主文`，没有逐主张写出登记 ID 与节、条目或行号。同一行列了 Ch.36，正文却没有使用 Ch.36。
- 正文 L48 链接了 exports(5)，但 source_refs 没有 `src.nfs-utils.exports-5-man7`（已登记于 L4907）。正文 L58 引了"RGW 文档"，却没有对应的登记 ID。
- **登记误差（追记）**：L5170 revision 写 `6259 行`，按 `wc -l` 实测为 6258 行（原文以换行结尾）。

剩余关闭条件：在来源记录（或正文"来源与更新范围"）写明三项 plan 来源未使用的理由；来源记录 L14 拆成逐主张的行（登记 ID 加节、条目或行号），删去未使用的 Ch.36 或补其用途；source_refs 补 exports(5)，RGW 一格补登记 ID 或改为 unknown；改正登记的行数。

### B21-C18 — P3 / OPEN

已满足：标题改为"先保留证据、保护恢复点"；博客改写为"Ceph 官方站点博客（2015，作者 shan）"；错误的"完整性证据 §8"链接已删除。

未满足：

- 读者可见文本仍有计划 ID：L47 `见 T04-02 §2`、L67 `见 T04-02`、L70 `见 T04-02 §3`、L86 `见 T04-02 §3/§5`、L91 `T04-06 基线`、L96 `T04-02/03 登记复用`。
- L52 写 `T04-02/03 引用均改为文档链接（本页不使用计划 ID）`，这句话本身用了计划 ID，与上述残留矛盾，而且属于修订说明，不应出现在正文。
- L80"博客 kind 说明"是登记元数据，不属于读者内容，宜移到来源记录或登记 notes。
- L66 指向恢复诊断指南的链接没有锚点，应链到"步骤与判断分支"节。

剩余关闭条件：上述计划 ID 全部改为带节名锚点的文档链接；删除 L52 与 L80 的修订说明，或移到来源记录；给训练指南链接加节锚点。

## acceptance 对照

| acceptance | 判定 | 相关发现 |
|---|---|---|
| 1 四类实现的证据入口与故障责任边界 | 部分满足：入口已补齐且与原文一致；Lustre 行格数错误会导致责任边界列被丢弃；Ceph/Lustre 无判据示例 | C14（P2） |
| 2 故障覆盖；恢复动作只引用选定实现条件 | 大体满足：超时、空间、降级三行已落到实现条件；凭据/权限一行仍有泛称 | C15（P2） |
| 3 先保留证据与恢复点；repair/remount/回放风险与停止条件独立 | 未满足：Filestore/BlueStore 限定写反；停止条件仍是通用的一组，未按动作和实现分开 | C10、C13（P1），C16（P2） |
| 4 正式上游测试案例；五类演练判据（未执行） | 前半句满足（C11 CLOSED）；判据表缺 ext4，多数"预期"没有来源 | C12（P1） |

横向问题：C17（plan 来源理由与记录定位，P2）、C18（计划 ID 残留，P3）。

## 结论

**T04-07 定向复核不通过。B21-C10–C18 共 9 项：CLOSED 1（C11），OPEN 8（P1 ×3：C10、C12、C13；P2 ×4：C14、C15、C16、C17；P3 ×1：C18）。** 本轮未新增发现 ID，按原 ID 追记 3 处：C10 的 Filestore/BlueStore 限定写反，C14 的 Lustre 行格数错误，C17 的登记行数误差。修订后应按上列"剩余关闭条件"再做定向复核。其中 C10 的事实错误应最先修正，因为它会直接误导 Squid/BlueStore 读者如何判断 repair 结果。C10 与 C17 关闭前，正文 `verification.status: source_checked` 不应视为成立。本复核只覆盖编辑与来源层面，所有存储行为都是文档或源码层证据，不得标为 reproduced。
