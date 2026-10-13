# 第二十一批 T04-07 第五次定向复核（作者第五轮修订后）

复核日期：2026-10-13（实际取证日）。正文 `updated_at: "2026-10-14"` 视为交付标签。

**结论：未通过。复核范围为 B21-C12、C13，共 2 项：CLOSED 1（C12），OPEN 1（P1：C13）。** 本轮不新增发现 ID。按原 ID 追记 1 处：

- C13：L87 Lustre 行的"预期"栏新增了"或 failed recovery 分支（Ch.38.1.6，后者只作停止分支）"，而同一行"失败判据"仍为"进入 failed recovery"。同一种结果因此既算预期，又算失败。第四次复核已判定关闭的矛盾（"failed recovery 只作停止分支，不作预期"）在本轮回退。

修订映射 T04-07 第五轮修订节（L73–76）与正文逐项核对后，C12 一致。C13 的"任一触发（四条件）"与正文不一致：正文停止条件列表在"任一触发即停"之前只列了三条，ext4 停止条件仍放在段末另起一句，没有并入列表。这一处属映射表述与文件不符。

`make check` 结果：通过（93 content entries / 417 sources，作者复核报告交付后运行）。它只校验结构和本地链接，不说明技术正确性。

审阅者角色独立于作者修订角色。审阅模型为 `claude-opus-5-5`，由用户明确要求使用；这不是既有的 `gpt-6.1-sol / xhigh` 批量审阅约定，也不改写该约定。推理等级等运行元数据没有可核验记录，不补造。本轮只读：只写本报告；未改作者正文、来源记录、修订映射、登记、索引或计划；未运行 `make build`；未执行任何故障注入、repair、remount、重连或演练。模型审阅不构成硬件或现场验证。

## 输入（以 SHA-256 识别）

| 输入 | SHA-256 前缀 | 核对 |
|---|---|---|
| [T04-07 正文](../../knowledge/04-data-storage/storage-client-backend-recovery.md)（97 行，procedure / draft） | `82d4e160639f2c21` | 与任务单一致 |
| [修订映射](batch-21-review-fixes.md)（T04-07 第五轮修订节 L73–76） | `f84f118cd0c540f9` | 与任务单一致 |
| [前次复核报告](batch-21-t04-07-claude-recheck-4.md)（剩余关闭条件的权威来源） | — | 按其 C12/C13"剩余关闭条件"逐条对照；其余已关闭项不重开 |
| [任务计划](../../plans/full-coverage-backlog.yaml)（T04-07 acceptance 4 条） | — | 沿用前次对照 |

行号说明：正文仍为 97 行，本轮涉及的 L73、L87、L89 与前次报告行号相同。

## 一次源重取（审阅者独立获取）

全部用 `curl -sSL` 只读获取，使用默认 TLS 校验，HTTP 均为 200。原文只放在临时目录 `/tmp/b21rc7e/`，未入库。

| 来源 | SHA-256 前缀 | 与前次比对 | 本轮核对点 |
|---|---|---|---|
| Squid PG 排查页 | `aa7e11cea56b65d8` | 同 | 内容未变；前次结论（`active+clean` 作为 PG 应达到的状态，未写成 repair 完成判据）沿用 → C12 |
| Lustre 手册 2.x | `63b09d0650de3491` | 同 | §38.1.6、§38.2、§38.1.2 原文，见下 → C13 |

Lustre 手册本轮核对的原文（摘录）：

```text
38.1.6. Failed Recovery In the case of failed recovery, a client is evicted by the server and must reconnect after having flushed its saved state related to that server, as described in Section 38.1.2, "Client Eviction" ...
38.2. Metadata Replay ... When a client detects an MDS failure, it connects to the new MDS and uses the metadata replay protocol to replay its requests.
```

取证限制：

- 只核对了上表列出的段落。Squid health-checks、ext4 admin-guide、nfs(5)、OSD 排查页、`osd-scrub-repair.sh` 本轮未重取，对应结论不在本轮范围内。
- 所有行为都是文档或源码层证据，未执行验证。

## 逐项复核

### B21-C12 — P1 / CLOSED

关闭证据：

- 剩余关闭条件 1：L73 存储侧完成条件已改为：

```text
Ceph PG_DAMAGED/OSD_SCRUB_ERRORS 消除且 PG 回到 `active+clean`（状态含义见 Squid PG 排查页；以此作完成判据为本库约定）
```

  这与 L89 的写法（"PG 状态含义见 Squid PG 排查页；以此作完成判据为本库约定"）一致。`active+clean` 不再归属 health-checks，同一判据在两处的来源归属已经统一。

非阻断：L73 这句不再给"PG_DAMAGED/OSD_SCRUB_ERRORS 消除"注明来源。前次条件允许"告警消除仍可引 health-checks"；health-checks 仍在 source_refs 中，且 L61、L62 已链接该页。补不补引用都不影响关闭。

### B21-C13 — P1 / OPEN（追记）

已满足：

- 条件 1 的计数部分：L73 的"三者任一触发即停"已改为"任一触发即停"，原来与 ext4 条件冲突的计数已经去掉。
- 条件 2 的引用部分：L87 预期栏已删去 Ch.38.1.2。现在的写法是"重连后进入 replay 流程（手册 Ch.38.2）"。本轮重取确认 §38.2 原文为"client detects an MDS failure … connects to the new MDS and uses the metadata replay protocol to replay its requests"，可以支持重连后进入 replay。

未满足：

- 条件 1 的合并部分：L73 的停止条件列表仍为"repair …；NFS grace …；Lustre 进入 failed recovery …；任一触发即停"，只有三条。ext4 停止条件（"回放报错或检查发现不一致即停"）仍放在完成条件和"任一未满足不进入训练侧"之后，单独成句。前次关闭条件写明要"并入列表"。修订映射写的"（四条件）"与正文列表不符。由于 ext4 那句自带"即停"，语义上的冲突已经消除，剩下的是位置问题；但它未达到关闭条件，映射的说法也与正文不一致。
- **L87 预期与失败判据矛盾（追记，回退）**：本轮 L87 原文为：

```text
| 客户端重连 | Lustre | eviction/replay 条件 | 重连后进入 replay 流程（手册 Ch.38.2）或 failed recovery 分支（Ch.38.1.6，后者只作停止分支） | 分支外状态/进入 failed recovery | 同上 |
```

  演练进入 failed recovery 时，结果落在预期栏的"或"分支内，同时又符合失败判据。括号里的"后者只作停止分支"说明了作者的意图，但"预期"一栏的含义是通过结果，把停止分支放进去会让判定变得模糊。第四次复核已关闭的矛盾因此回退。前次关闭条件 2 也写明"只保留 Ch.38.2 作为依据"，本轮另外加入了 Ch.38.1.6。§38.1.6 的原文（驱逐、清除保存状态后重连）本身没有引用错误，问题只在于它被放进了预期栏。

非阻断：

- L87 预期由"重连完成"改成了"进入 replay 流程"。进入流程不等于流程完成，作为演练的通过判据偏弱。建议写成"replay 完成、recovery 结束（Ch.38.2）"。
- L87 失败判据中的"分支外状态"目前可以理解为"replay 与 failed recovery 之外的状态"。按下面的条件 2 删掉预期栏中的 failed recovery 分支后，这几个字应同步删去，或改写成"replay 未完成"。
- L73 完成条件"Lustre recovery 完成并记录（手册 Ch.38.1.6；…）"把 Failed Recovery 小节当作"recovery 完成"的依据。该节只间接提到"VBR allows recovery to proceed for all of the connected clients"。改引 Ch.38.2 更贴切。这一处此前各轮都存在，不在本轮关闭条件内。

剩余关闭条件：

1. 把 L73 段末的 ext4 停止条件移到停止条件列表中，放在"任一触发即停"之前（使列表实际为四条，与修订映射一致）。
2. L87 预期栏删去"或 failed recovery 分支（Ch.38.1.6，后者只作停止分支）"。failed recovery 只留在失败判据栏（该栏已有"进入 failed recovery"）；如需引用，可在失败判据栏注 Ch.38.1.6。

## acceptance 对照

| acceptance | 判定 | 相关发现 |
|---|---|---|
| 1 四类实现的证据入口与故障责任边界 | 满足 | C14 CLOSED（前次） |
| 2 故障覆盖；恢复动作只引用选定实现条件 | 满足（ext4 路径/挂载/权限一格无来源，非阻断沿用） | C15 CLOSED（前次） |
| 3 先保留证据与恢复点；按官方条件选择重连/恢复服务/从可信副本恢复；repair/remount/回放的风险与停止条件独立 | 大体满足：计数冲突已消除；ext4 停止条件仍未并入列表 | C10 CLOSED（前次）；C13 OPEN |
| 4 正式上游测试案例；五类演练判据（未执行） | 大体满足：L73/L89 归属已统一；L87 Lustre 预期与失败判据重新矛盾 | C12 CLOSED；C13 OPEN |

C12 关闭后，`verification.status: source_checked` 的阻断项只剩 C13。C13 中的 L87 问题会影响"预期（来源依据）"一栏能否判定，建议在 C13 关闭后再把该状态视为成立。

## 结论

**T04-07 第五次定向复核不通过。复核范围 2 项（C12、C13）：CLOSED 1（C12），OPEN 1（P1：C13）。连同此前已关闭的 C10、C11、C14、C15、C16、C17、C18，B21-C10–C18 共 9 项：CLOSED 8，OPEN 1。** 本轮不新增发现 ID，按原 ID 追记 1 处：C13 中 L87 的 failed recovery 同时出现在预期栏和失败判据栏（回退）。

剩余工作是正文中的 2 处定点文字改动：

- C13：L73 把 ext4 停止条件移入"任一触发即停"之前的列表；L87 预期栏删去 failed recovery 分支。

修订后按上列"剩余关闭条件"再做定向复核。本复核只覆盖编辑与来源层面，所有存储行为都是文档或源码层证据，不得标为 reproduced。

`make check`：通过（93 content entries / 417 sources，作者复核报告交付后运行）。
