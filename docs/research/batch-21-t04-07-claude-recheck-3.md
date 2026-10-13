# 第二十一批 T04-07 第三次定向复核（作者第三轮修订后）

复核日期：2026-10-13（实际取证日）。正文 `updated_at: "2026-10-14"` 视为交付标签。

**结论：未通过。复核范围为 B21-C10、C12–C18，共 8 项（C11 已 CLOSED，不重开）：CLOSED 4（C14、C15、C16、C18），OPEN 4（P1 ×3：C10、C12、C13；P2 ×1：C17）。** 本轮不新增发现 ID。新查出的逻辑问题按原 ID 追记 1 处：

- C13：§5 判据表 Lustre 重连行（L86）仍把"进入 failed recovery 分支"列为预期，与 L70、L72 的"failed recovery 只停不完成"矛盾。

修订映射 T04-07 第三轮修订节（L53–63）有三处所称修订在文件中没有落实：

- C10"记录第 6 条澄清"：来源记录 L24 第 6 条未改动。这是第二次声称已修订。
- C12"L88 active+clean 归属"：L88 与 L72 仍写 `active+clean`（见 health-checks）。
- C17：映射本轮只写了"记录 L3/L11 订正"，没有声称处理关闭条件 1、2；文件中这两项也确实没有处理。

`make check` 通过（93 content entries / 417 sources）。它只校验结构和本地链接，不说明技术正确性。

审阅者角色独立于作者修订角色。审阅模型为 `claude-opus-5-5`，由用户明确要求使用；这不是既有的 `gpt-6.1-sol / xhigh` 批量审阅约定，也不改写该约定。推理等级等运行元数据没有可核验记录，不补造。本轮只读：只写本报告；未改作者正文、来源记录、修订映射、登记、索引或计划；未运行 `make build`；未执行任何故障注入、repair、remount、重连或演练。模型审阅不构成硬件或现场验证。

## 输入（以 SHA-256 识别）

| 输入 | SHA-256 前缀 | 核对 |
|---|---|---|
| [T04-07 正文](../../knowledge/04-data-storage/storage-client-backend-recovery.md)（96 行，procedure / draft） | `5a253dbb88a47f44` | 与任务单一致 |
| [作者来源记录](batch-21-t04-07-sources.md)（24 行） | `ab2f5548083da3fd` | 与任务单一致 |
| [修订映射](batch-21-review-fixes.md)（T04-07 第三轮修订节 L53–63） | `80778d9961dde89a` | 与任务单一致 |
| [前次复核报告](batch-21-t04-07-claude-recheck-2.md)（剩余关闭条件的权威来源） | — | 按其"剩余关闭条件"逐条对照 |
| [任务计划](../../plans/full-coverage-backlog.yaml)（T04-07 acceptance 4 条） | — | 沿用前次对照 |
| [来源登记](../../sources/registry.yaml)（417 项） | `0e0a15fffd713af2` | 与任务单一致；`src.kernel.docs-nfs-v6.16`（L4874）、`src.ceph.docs-rgw-s3-squid`（L4995）可解析 |

旁证（只读本库现行草稿）：

- [本地与共享存储](../../knowledge/04-data-storage/local-and-shared-storage.md)：§2 L73（jbd2 commit/replay）、§5 L110（本地重启可读）。
- [对象与并行存储](../../knowledge/04-data-storage/object-and-parallel-storage.md)：§2 L53（Complete 可见性 unknown）、§5 L88（对象可见为设计预期）。

## 一次源重取（审阅者独立获取）

全部用 `curl -sSL` 只读获取，使用默认 TLS 校验，HTTP 均为 200。原文只放在临时目录 `/tmp/b21rc7c/`，未入库。

| 来源 | SHA-256 前缀 | 与前次比对 | 本轮核对点 |
|---|---|---|---|
| Squid PG 排查页 | `aa7e11cea56b65d8` | 同 | `In the case of erasure-coded and BlueStore pools, Ceph will automatically perform repairs if osd_scrub_auto_repair (default false) … (default 5)`；`The pg repair command will not solve every problem. Ceph does not automatically repair PGs …`；`This material is relevant for Filestore, but not for BlueStore …` 段落内容同前次 → C10 |
| Squid health-checks | `a6a9ed5466bb87fe` | 同 | `active+clean` 全页仍只出现 1 次（PG 长时间未达该状态的语境），不是完成判据 → C12 |
| Lustre 手册 2.x | `63b09d0650de3491` | 同 | §30.6 标题为 `Configuring Kerberos (KRB) Security`（含 30.6.1 What Is Kerberos?、30.6.2 Security Flavor、30.6.3 Kerberos Setup）。§38.4 原文：`If the versions do not match, then the client is evicted`。§38.4.1 列出 `Version mismatch during replay` 与 `version recovery fails, reconnecting` 两条消息 → C15、C16 |
| ext4 admin-guide v6.16 | `2849c200bf743291` | 同 | 未改动部分，不复核 → C14 |

取证限制：

- tracker #8914、Squid release notes、RGW 健康/管理文档本轮仍未检索。
- Lustre 手册只核对了 §30.6 标题和 §38.1.6、§38.2.7、§38.4 相关段落。
- 未重取 `osd-scrub-repair.sh`；正文 §4 本轮未改动，C11 不重开。
- 所有行为都是文档或源码层证据，未执行验证。

## 逐项复核

### B21-C10 — P1 / OPEN

已满足：

- 条件 1：L68 新增"适用限定"，写明"权威性不可证、偏向 primary、需人工判断"同样只限 Filestore 或 checksum 不可用的情形，并记录"PG 页未描述 BlueStore 下如何选择权威副本（unknown）"。通用部分保留了 `will not solve every problem` 与"Ceph 不自动修复"，与原文一致。auto_repair 的条件（EC/BlueStore、默认 false、默认 5）也与原文一致。
- 条件 2：L67 末句为"repair 以外的'从可信副本恢复'流程未取源（unknown）"。

未满足：

- 条件 3：[来源记录](batch-21-t04-07-sources.md) L24 第 6 条仍是 `repair 前清单外原文`，与上一轮相同，没有改写也没有删除。修订映射 L44（第二轮）和 L55（第三轮）两次称"记录第 6 条澄清"，都与文件不符。

非阻断建议：L68 主句仍先加粗写出 `**权威性不可证**`，限定写在同一条目的末尾。字面上已满足条件 1，但读者先读到的是没有限定的结论。建议把限定移到加粗处旁边，或去掉加粗。

剩余关闭条件：改写或删除来源记录 L24 第 6 条，例如改为"repair 前清单即定位链输出，无清单外原文"，或直接删去。

### B21-C12 — P1 / OPEN

已满足：

- 条件 1：L89 改引对象与并行存储 §5 的设计预期（旁证 L88 原文为"且对象可见"），并保留 §2 的可见性 unknown（旁证 L53）。
- 条件 2：L90 的预期标为"本库约定"，链接文字已改为"负载基线"。

未满足（条件 3，前次列为次要）：

- L88 仍写"PG 回到 `active+clean`、告警消除（见 health-checks）"，L72 存储侧完成条件也仍写"PG 回到 `active+clean`（见 health-checks …）"。本轮重取确认 health-checks 页只在"长时间未达 `active+clean`"的语境中提到该状态，没有把它作为完成判据。修订映射 L56 称"L88 active+clean 归属"已修订，与文件不符。
- L84 的 ext4 预期仍以"重挂载后日志回放完成"为主体，§5 的预期"回放后文件系统一致"只放在括号里。旁证 §5 L110 把"重挂载＋日志回放完成"列为前置，把"回放后文件系统一致"列为预期。现写法已把两者都写出，本项按部分满足处理，但主语仍然错位。

剩余关闭条件：

1. L88 与 L72 的 `active+clean` 改为"本库约定"，或改引 PG 排查页中对应的段落；告警消除仍可引 health-checks。
2. L84 的预期主语改为"回放后文件系统一致"，"日志回放完成"移入前置一栏（次要）。

### B21-C13 — P1 / OPEN（追记）

已满足：

- 条件 1（L70、L72 部分）：Lustre 完成条件已删去"或进入 failed recovery 分支"。L70、L72 都写明 failed recovery 只作停止或升级分支，引 §38.1.6 的驱逐与状态清除。
- 条件 2：NFS 停止条件改为"grace 结束时 reclaim 仍未完成即停"，可以与完成条件"reclaim 完成与 grace 结束"区分；已标本库约定，并沿用 grace 时长 unknown。
- 条件 3：Ceph 停止条件在 L68 标"本库约定"，在 L72 标"见 PG 排查页；本库约定"。两处都是本库约定，PG 页只作理由，可以接受。
- 条件 4 的完成条件部分：ext4 完成条件"回放/检查完成"引本地与共享存储 §2/§5，超出部分记 unknown。§2 L73 和 §5 L110 支持"回放"；"检查"（如 fsck）由"超出部分 unknown"兜底，可以接受。

未满足：

- **逻辑矛盾（追记）**：L86 的 §5 判据表 Lustre 重连行，预期仍为"重连完成或进入 failed recovery 分支"，失败判据为"分支外状态"。按此设计，演练中进入 failed recovery 仍判为通过，与 L70、L72 新写的"failed recovery 只作停止分支，不作完成"直接矛盾。手册 §38.1.6 写明，failed recovery 时客户端被驱逐，并须清除保存状态。前次报告只点了 L72，没有点到 L86 的同类写法，这是审阅侧的遗漏，不归咎于作者。
- 条件 4 的停止条件部分：L72 的存储侧停止条件只有 Ceph、NFS、Lustre 三项（"三者任一触发即停"）。ext4 没有停止条件，也没有记为 unknown。L69 的 remount 停止条件和 L70 的回放停止条件（gap、VBR 消息、驱逐）都不是 ext4 回放失败的判据。

剩余关闭条件：

1. L86 的预期改为"重连完成（recovery 完成）"；把"进入 failed recovery"移入失败判据或停止分支，引 §38.1.6。
2. L72 补 ext4 停止条件（例如"回放失败或挂载后转只读即停"，标为本库约定，可引 admin-guide `errors=`），或明确记为 unknown；"三者"相应改为"四者"或"任一"。

### B21-C14 — P2 / CLOSED

关闭证据：L48 第 3 格改为"单机：设备/驱动/文件系统检出错误；`errors=` 只是反应方式"，与同行第 2 格以及 admin-guide `errors=` 原文一致。原句 `转只读事件指向 errors 配置` 已删除。表格分隔符未变（每行 4 个未转义 `|`，`\|` 已转义）。前次已满足的条件 1、2 未回退。

### B21-C15 — P2 / CLOSED

关闭证据：

- 条件 1：L58 Lustre 凭据格改为"凭据见手册 §30.6 Kerberos；超出 unknown"，"同左"已删除。本轮重取确认 §30.6 标题为 `Configuring Kerberos (KRB) Security`，节号与主题一致。
- 条件 2：L59 ext4 超时格改为"ext4 无超时挂载语义（不适用；块层命令超时不属本格范围，unknown）"，"单机同步 I/O 模型"的理由已删除。

非阻断：L58 ext4 的"路径/挂载/权限按实现检查"仍然既无来源也没有记 unknown。前次已列为次要问题，不属关闭条件。

### B21-C16 — P2 / CLOSED

关闭证据：

- 条件 1：L70 改写为"gap 的两种来源为 lost replies 与缺席恢复的客户端，未全部重连时缺席客户端的请求不再回放，gap 之后能否回放由 VBR 按版本判定，版本不匹配时客户端被驱逐（§38.4）"。这与手册 §38.2.7 原文（`the failed clients had requests that will no longer be replayed`）和 §38.4 原文（`If the versions do not match, then the client is evicted`）一致。
- 条件 2：停止信号改为"§38.4.1 VBR 消息（`Version mismatch during replay`）或客户端驱逐"，消息原文已核对存在。"版本号回退"已删除。

非阻断：停止信号首项"不可解释的 gap"没有写观测方法。另外两项信号可以在现场判定，因此按本库约定接受。

### B21-C17 — P2 / OPEN

已满足：

- 条件 3（次要）：来源记录 L3 改为"Lustre Ch.35/38 节号"，与 L16 的"Ch.36 未使用"一致。L11 改为"阈值 default 10 已用 … 其余阈值细节 unknown"，与正文 L61 一致。

未满足：

- 条件 1：正文 L58 链接了 RGW S3 索引，来源记录 L17 也列了 `src.ceph.docs-rgw-s3-squid`（登记 L4995 可解析），但正文 source_refs（L8–17）仍没有这一项。
- 条件 2：来源记录 L14 仍列 `src.kernel.docs-nfs-v6.16`，applicability.notes（L29）仍写"内核 v6.16 NFS/ext4 文档"，但正文没有引用内核 NFS 文档，source_refs 中也没有。三处仍不一致。
- 附带（非阻断）：本轮正文新引用了手册 §30.6、§38.2、§38.4、§38.4.1、§23.1，来源记录 L16 的定位只写了"Ch.35.3/38.1/health_check/lfs"，建议一并补全。

剩余关闭条件：

1. source_refs 补 `src.ceph.docs-rgw-s3-squid`。
2. 处理 `src.kernel.docs-nfs-v6.16` 的去留，使正文、notes、来源记录三处一致。

在 C10 与 C17 关闭前，正文的 `verification.status: source_checked` 仍不应视为成立。

### B21-C18 — P3 / CLOSED

关闭证据：

- 条件 1：L90 的链接文字改为"负载基线"。在正文中检索计划 ID 模式 `T0x-xx`，无命中。
- 条件 2：L78 末尾的博客 kind 元数据说明已删除；该内容仍保留在来源记录 L18。
- 条件 3：L66 改为"'适用范围与前置条件'首条"。

## acceptance 对照

| acceptance | 判定 | 相关发现 |
|---|---|---|
| 1 四类实现的证据入口与故障责任边界 | 满足 | C14 CLOSED |
| 2 故障覆盖；恢复动作只引用选定实现条件 | 满足（ext4 路径/挂载/权限一格无来源，属非阻断） | C15 CLOSED |
| 3 先保留证据与恢复点；按官方条件选择重连/恢复服务/从可信副本恢复；repair/remount/回放的风险与停止条件独立 | 大体满足：repair 的 Filestore 限定、可信副本恢复 unknown、§38.2.7 要点已到位；ext4 仍缺存储侧停止条件；来源记录第 6 条未改 | C10、C13（P1）；C16 CLOSED |
| 4 正式上游测试案例；五类演练判据（未执行） | 前半句满足（C11 CLOSED）；判据表 Lustre 行把 failed recovery 列为预期，`active+clean` 归属未改 | C12、C13（P1） |

横向问题：C17（source_refs 与记录一致性，P2）。

## 结论

**T04-07 第三次定向复核不通过。复核范围 8 项（C10、C12–C18）：CLOSED 4（C14、C15、C16、C18），OPEN 4（P1 ×3：C10、C12、C13；P2 ×1：C17）。连同前次已关闭的 C11，B21-C10–C18 共 9 项：CLOSED 5，OPEN 4。** 本轮不新增发现 ID，按原 ID 追记 1 处：C13 中 L86 判据表把 failed recovery 列为预期。

剩余工作都是文字或元数据层面的定点改动，共 7 处：

- C10：来源记录 L24 第 6 条。
- C12：L72、L88 的 `active+clean` 归属；L84 的预期主语（次要）。
- C13：L86 的 failed recovery；L72 的 ext4 停止条件。
- C17：source_refs 补 RGW；`src.kernel.docs-nfs-v6.16` 的去留。

建议作者在修订映射中只记录实际落到文件的改动：本轮有两处所称修订（C10 第 6 条、C12 的 L88）与文件不符。修订后按上列"剩余关闭条件"再做定向复核。本复核只覆盖编辑与来源层面，所有存储行为都是文档或源码层证据，不得标为 reproduced。
