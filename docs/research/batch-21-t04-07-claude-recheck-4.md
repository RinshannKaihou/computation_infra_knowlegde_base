# 第二十一批 T04-07 第四次定向复核（作者第四轮修订后）

复核日期：2026-10-13（实际取证日）。正文 `updated_at: "2026-10-14"` 视为交付标签。

**结论：未通过。复核范围为 B21-C10、C12、C13、C17，共 4 项：CLOSED 2（C10、C17），OPEN 2（P1 ×2：C12、C13）。** 本轮不新增发现 ID。按原 ID 追记 1 处：

- C13：§5 判据表 Lustre 行（L87）的预期"重连完成"引用了手册 Ch.38.1.2。本轮重取确认该节标题为 `Client Eviction`，内容是驱逐原因与驱逐后果，不能支持"重连完成"这一预期。

修订映射 T04-07 第四轮修订节（L65–71）所列改动与文件逐项核对后一致，没有发现"声称已改而文件未改"的情况。剩余两项 OPEN 的问题都是修订映射没有声称处理过的位置（L73 的 `active+clean` 归属、L73 的"三者"计数），因此不是映射失实，是修订遗漏。

`make check` 通过（93 content entries / 417 sources）。它只校验结构和本地链接，不说明技术正确性。

审阅者角色独立于作者修订角色。审阅模型为 `claude-opus-5-5`，由用户明确要求使用；这不是既有的 `gpt-6.1-sol / xhigh` 批量审阅约定，也不改写该约定。推理等级等运行元数据没有可核验记录，不补造。本轮只读：只写本报告；未改作者正文、来源记录、修订映射、登记、索引或计划；未运行 `make build`；未执行任何故障注入、repair、remount、重连或演练。模型审阅不构成硬件或现场验证。

## 输入（以 SHA-256 识别）

| 输入 | SHA-256 前缀 | 核对 |
|---|---|---|
| [T04-07 正文](../../knowledge/04-data-storage/storage-client-backend-recovery.md)（97 行，procedure / draft） | `2fa3d9613cc75661` | 与任务单一致 |
| [作者来源记录](batch-21-t04-07-sources.md)（24 行） | `2ddbde25a9ce8075` | 与任务单一致 |
| [修订映射](batch-21-review-fixes.md)（T04-07 第四轮修订节 L65–71） | `9e94a09a0f89b1f6` | 与任务单一致 |
| [前次复核报告](batch-21-t04-07-claude-recheck-3.md)（剩余关闭条件的权威来源） | `e5a281312bdf4312` | 按其"剩余关闭条件"逐条对照 |
| [任务计划](../../plans/full-coverage-backlog.yaml)（T04-07 acceptance 4 条） | — | 沿用前次对照 |
| [来源登记](../../sources/registry.yaml)（417 项） | — | 计数 417；`src.kernel.docs-nfs-v6.16`（L4874）、`src.ceph.docs-rgw-s3-squid`（L4995）可解析 |

行号说明：正文比上一轮多 1 行（L52–53 为两个空行），§3 之后的行号整体比前次报告大 1。前次报告中的 L72、L84、L86、L88 分别对应本轮的 L73、L85、L87、L89。

## 一次源重取（审阅者独立获取）

全部用 `curl -sSL` 只读获取，使用默认 TLS 校验，HTTP 均为 200。原文只放在临时目录 `/tmp/b21rc7d/`，未入库。

| 来源 | SHA-256 前缀 | 与前次比对 | 本轮核对点 |
|---|---|---|---|
| Squid PG 排查页 | `aa7e11cea56b65d8` | 同 | `active+clean` 出现 3 次：目录项 `Erasure Coded PGs are not active+clean`、同名小节标题，以及 `Placement Groups Never Get Clean` 节中的 `never achieve an active+clean status might indicate a problem`。该页把它作为 PG 应达到的状态，但没有把它写成 repair 的完成判据 → C12 |
| Squid health-checks | `a6a9ed5466bb87fe` | 同 | `active+clean` 全页仍只出现 1 次（monitor 数据库增长语境：`placement groups that have not reached an active+clean state in a long time`） → C12 |
| Lustre 手册 2.x | `63b09d0650de3491` | 同 | 节标题：`38.1.1. Client Failure`、`38.1.2. Client Eviction`、`38.1.6. Failed Recovery`、`38.2.7. Gaps in the Replay Sequence`、`38.4.1. VBR Messages`。§38.1.2 原文开头为 `If a client is not behaving properly from the server's point of view, it will be evicted`，随后列出驱逐原因 → C13 |

取证限制：

- 只核对了上表列出的段落。ext4 admin-guide、nfs(5)、OSD 排查页、`osd-scrub-repair.sh` 本轮未重取；它们对应的结论不在本轮范围内。
- 所有行为都是文档或源码层证据，未执行验证。

## 逐项复核

### B21-C10 — P1 / CLOSED

关闭证据：

- 条件 1、2 未回退：L69 仍有"适用限定"，写明"权威性不可证、偏向 primary、需人工判断"只限 Filestore 或 checksum 不可用的情形，并记录"PG 页未描述 BlueStore 下如何选择权威副本（unknown）"；L68 末句仍为"repair 以外的'从可信副本恢复'流程未取源（unknown）"。
- 条件 3：[来源记录](batch-21-t04-07-sources.md) L24 第 6 条已改写为：

```text
6. repair 前清单指本链输出（`list-inconsistent-obj` JSON），无其他官方原文（unknown 已关闭项）。
```

  这与前次建议的改法一致。来源记录 L9 的"修复前清单即本链输出"、正文 L67 的"保存其 JSON 输出"也与之一致。

非阻断（沿用）：L69 主句仍先加粗写出 `**权威性不可证**`，限定写在同一条目的末尾。另外，第 6 条既已关闭，留在"unknown 清单"中容易误读，可以考虑移出清单。

### B21-C12 — P1 / OPEN

已满足：

- 条件 1 的 L89 部分（前次 L88）：完成判据改为"PG 回到 `active+clean`、告警消除（PG 状态含义见 Squid PG 排查页；以此作完成判据为本库约定）"。本轮重取确认 PG 排查页把 `active+clean` 作为 PG 应达到的状态，"作完成判据"已标为本库约定，可以接受。
- 条件 2（次要，L85，前次 L84）：预期改为"重挂载后日志回放完成即进入完成判定（回放后文件系统一致为完成判据，见本地与共享存储 §5 …）"，完成判据的主语已经是"回放后文件系统一致"，与旁证 §5 一致。按满足处理。

未满足：

- 条件 1 的 L73 部分（前次 L72）：存储侧完成条件仍为下面这句，没有改动：

```text
Ceph PG_DAMAGED/OSD_SCRUB_ERRORS 消除且 PG 回到 `active+clean`（见 health-checks，下一次 deep scrub 无新错误为本库约定）
```

  括号里的"本库约定"只覆盖 deep scrub，`active+clean` 的归属仍指向 health-checks。本轮重取确认 health-checks 只在 monitor 数据库增长的语境中提到该状态。这样，同一个判据在 L73 归属 health-checks，在 L89 归属 PG 排查页＋本库约定，两处不一致。修订映射 L68 只声称改了 L88，对 L72 没有声称，属遗漏而非映射失实。

非阻断：L85 的失败判据仍只写"回放未完成"。回放完成但文件系统不一致的情形，在该行既不满足预期，也不落入失败判据。建议补上"回放后不一致"。

剩余关闭条件：

1. L73 的 `active+clean` 归属改为与 L89 相同的写法（状态含义见 PG 排查页；作完成判据为本库约定）。告警消除仍可引 health-checks。

### B21-C13 — P1 / OPEN（追记）

已满足：

- 条件 1：L87 Lustre 行的预期改为"重连完成（…；failed recovery 只作停止分支，不作预期）"，失败判据改为"分支外状态/进入 failed recovery"。演练中进入 failed recovery 现在判为失败，与 L71、L73 的"failed recovery 只停不完成"一致，前次指出的矛盾已消除。
- 条件 2 的实质部分：L73 末尾新增"ext4 停止条件：回放报错或检查发现不一致即停（本库约定；专用停止语义未取源）"，已标为本库约定，并记录未取源。

未满足：

- 条件 2 的计数部分：同一段前半的存储侧停止条件仍为"……Lustre 进入 failed recovery 即停并记录（手册 Ch.38.1.6）；三者任一触发即停"。ext4 停止条件放在"任一未满足不进入训练侧"之后另起一句，没有并入停止条件列表，"三者"也未按前次关闭条件改为"四者"或"任一"。读者按"三者任一触发即停"理解时，ext4 不在列表内。这一处只是措辞和位置问题，但前次关闭条件写明了要改。
- **来源归属（追记）**：L87 预期栏"重连完成（手册 Ch.38.1.2/38.2；…）"。本轮重取确认 §38.1.2 是 `Client Eviction`，内容是驱逐的原因与后果，不支持"重连完成"。§38.2（Metadata Replay）可以作为恢复与回放的依据。这处引用此前各轮都存在，前次报告没有指出，属审阅侧遗漏，不归咎于作者。

非阻断：L87 失败判据中的"分支外状态"，在预期已不含分支之后失去了所指，建议删去或写明指什么。

剩余关闭条件：

1. 把 ext4 停止条件并入 L73 的存储侧停止条件列表，并把"三者任一触发即停"改为"四者任一触发即停"或"任一触发即停"。
2. L87 预期栏删去 Ch.38.1.2，或把它移到前置一栏（eviction 条件），只保留 Ch.38.2 作为"重连完成"的依据。

### B21-C17 — P2 / CLOSED

关闭证据：

- 条件 1：正文 source_refs L16 已有 `src.ceph.docs-rgw-s3-squid`，与正文 L59 的 RGW S3 索引链接以及来源记录 L17 一致；登记 L4995 可解析。
- 条件 2：`src.kernel.docs-nfs-v6.16` 已从三处统一去掉：正文 source_refs（L8–18）不含该项；applicability.notes（L30）改为"ext4 管理指南、nfs-utils 手册页"，不再写"内核 v6.16 NFS"；来源记录 L14 的 ID 栏为 `src.nfs-utils.nfs-5-man7`，并注明"内核 NFS 文档本任务未引用，已从 notes 去除"。在正文与来源记录中检索 `docs-nfs-v6.16`，均无命中。该登记项（L4874）仍保留在 registry 中，供其他条目使用，不受影响。

非阻断（沿用）：来源记录 L16 的 Lustre 定位仍只写"Ch.35.3/38.1/health_check/lfs"，没有包含正文引用的 §23.1、§30.6、§38.2、§38.4、§38.4.1。

## acceptance 对照

| acceptance | 判定 | 相关发现 |
|---|---|---|
| 1 四类实现的证据入口与故障责任边界 | 满足 | C14 CLOSED（前次） |
| 2 故障覆盖；恢复动作只引用选定实现条件 | 满足（ext4 路径/挂载/权限一格无来源，非阻断沿用） | C15 CLOSED（前次） |
| 3 先保留证据与恢复点；按官方条件选择重连/恢复服务/从可信副本恢复；repair/remount/回放的风险与停止条件独立 | 大体满足：C10 已关闭；ext4 停止条件已写，但未并入"三者"列表 | C10 CLOSED；C13 OPEN |
| 4 正式上游测试案例；五类演练判据（未执行） | 大体满足：failed recovery 矛盾已消除，L89 归属已改；L73 的 `active+clean` 归属未同步，L87 的 Ch.38.1.2 引用不支持预期 | C12、C13 OPEN |

C17 已关闭。按前次报告的说法，`verification.status: source_checked` 的阻断项中，C10 与 C17 已经解除。C12、C13 中残留的归属问题仍会影响"预期（来源依据）"一栏的准确性，建议在这两项关闭后再把该状态视为成立。

## 结论

**T04-07 第四次定向复核不通过。复核范围 4 项（C10、C12、C13、C17）：CLOSED 2（C10、C17），OPEN 2（P1 ×2：C12、C13）。连同此前已关闭的 C11、C14、C15、C16、C18，B21-C10–C18 共 9 项：CLOSED 7，OPEN 2。** 本轮不新增发现 ID，按原 ID 追记 1 处：C13 中 L87 引用的 Ch.38.1.2 不支持"重连完成"。

剩余工作都是正文中的定点文字改动，共 3 处：

- C12：L73 的 `active+clean` 归属，改为与 L89 一致。
- C13：L73 把 ext4 停止条件并入列表并修正"三者"；L87 预期栏的 Ch.38.1.2。

修订后按上列"剩余关闭条件"再做定向复核。本复核只覆盖编辑与来源层面，所有存储行为都是文档或源码层证据，不得标为 reproduced。
