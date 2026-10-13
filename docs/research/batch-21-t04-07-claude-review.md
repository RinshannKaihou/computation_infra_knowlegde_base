# 第二十一批 T04-07 初审

审阅日期：2026-10-13（实际取证日）。正文 `updated_at: "2026-10-14"` 视为交付标签，不作为本轮取证日期；输入以下表 SHA-256 识别。

**结论：T04-07 需修订。新增 9 项发现（B21-C10–C18）：P1 ×4、P2 ×4、P3 ×1，全部 OPEN。** 四条 acceptance 都有缺口。acceptance 3 和 4 各有 P1。正文把官方给出的 repair 前不一致对象清单记成 unknown，把 `ceph pg repair` 写成"从可信副本恢复"，与 Squid 原文不符。所选上游案例是 FileStore 流程，而 Squid 文档写明 Reef 及以后不支持 FileStore。演练判据只有一段话，没有逐项设计。存储侧的停止条件和前置条件直接引用训练恢复指南，与计划缺口 04.6-G3"不得由训练恢复指南代替存储恢复"相抵触。正文未虚构实测结果，也没有把任何项目标为已执行，这一点满足。`make check` 通过（93 content entries / 414 sources），但它只校验结构与本地链接，不说明技术正确性。

审阅者角色独立于作者。审阅模型为 `claude-opus-5-5`，由用户本次明确要求试用。这不是既有的 `gpt-6.1-sol / xhigh` 批量审阅约定，也不改写该约定；推理等级等运行元数据没有可核验记录，不补造。本轮只做审阅和只读取证：未改作者正文、来源记录、登记、索引或计划；未执行任何故障注入、repair、remount、重连或演练。模型审阅不构成硬件或现场验证。

## 输入（以 SHA-256 识别）

| 输入 | SHA-256 |
|---|---|
| [T04-07 正文](../../knowledge/04-data-storage/storage-client-backend-recovery.md)（76 行，procedure / draft） | `0b10fdeb2fa56286b5a1b76fbaf0ca1af49560c8ff5063173941fea20bab9131` |
| [作者来源记录](batch-21-t04-07-sources.md)（15 行） | `f69ed5293babd3606d1ce94fd4b812fe8585ca0659748898a854dea8da7a55de` |
| [任务计划](../../plans/full-coverage-backlog.yaml)（T04-07 L5290–5333，acceptance L5308–5311） | `f16309beadf5ae4f28d5fc7428a2348bea0cf08d155d57730a4d817cfcdd3e96` |
| [来源登记](../../sources/registry.yaml)（新登记 src.ceph.docs-troubleshooting-pg-squid L5140、src.ceph.blog-manual-repair-object-2015 L5154） | `4ac30b8823600222233693471ce2af8408e5ea84524ae21d6d3a09386643b3f7` |

旁证（按本库现行草稿核对，未重新取其一次源）：[本地与共享存储](../../knowledge/04-data-storage/local-and-shared-storage.md)（T04-02 §2/§3/§5）、[对象与并行存储](../../knowledge/04-data-storage/object-and-parallel-storage.md)（T04-03 §4/§5）、[完整性证据](../../knowledge/04-data-storage/checkpoint-integrity-evidence.md)（"官方反例与证据保留"节）、[恢复诊断指南](../../knowledge/06-training/checkpoint-state-recovery-triage.md)、`04-data-storage/index.md` 工作区 diff（新增 related_id 与 04.6 条目）、`docs/full-coverage-roadmap.md` L117/L191。正文 `related_ids` 五个 ID 都能解析到已有文件。

## 一次源取证（审阅者独立获取）

全部用 `curl -sSL` 或 `git ls-remote` 只读获取，默认 TLS 校验，HTTP 均为 200。HTML 去标签后按文字核对，不只判可达性。原文只放在临时目录 `/tmp/b21rev7/`，未入库。

| 来源（登记 ID） | URL | SHA-256（原文） | 核对点与结果 |
|---|---|---|---|
| Squid PG 排查页（src.ceph.docs-troubleshooting-pg-squid） | [troubleshooting-pg](https://docs.ceph.com/en/squid/rados/troubleshooting/troubleshooting-pg/) | `aa7e11cea56b65d8bae5bbaed376a5875f3c2bd81051def60491cf749f0b91a1` | "PGs Inconsistent" 节的定位链为：`ceph health detail`（示例 `HEALTH_ERR 1 pgs inconsistent; 2 scrub errors`）→ `rados list-inconsistent-pg <pool>` → `rados list-inconsistent-obj <pgid> --format=json-pretty`。后者输出 `errors`、`union_shard_errors`、`selected_object_info` 和逐 OSD 的 `shards`（size/data_digest/omap_digest），并逐项解释 `data_digest_mismatch`、`size_mismatch` 等含义。**Warning 框**的内容是：shard 的 errors 含 `read_error` 时"likely due to physical storage errors"，应在 repair 前检查 `dmesg` 与 `smartctl`。它不是覆盖写警告。"More Information on PG Repair" 节写道：repair "attempts to overwrite the digest of the inconsistent copy with the digest of the authoritative copy"；对 replicated pool，它"marks the inconsistent copy as missing"，且"recovery is beyond the scope of pg repair"；`osd_scrub_auto_repair` 默认 false，仅 EC 与 BlueStore pool 在错误数不超过 `osd_scrub_auto_repair_num_errors`（默认 5）时自动修复；"The matched-record checksum and the calculated checksum cannot prove that any specific copy is in fact authoritative. If there is no checksum available, pg repair favors the data on the primary, but this might not be the uncorrupted replica … human intervention is necessary"；同段注明"This material is relevant for Filestore, but not for BlueStore"。"PG Repair Walkthrough" 链到 `ceph.io/geen-categorie/ceph-manually-repair-object/`。→ C10/C11/C16 |
| 2015 博客（src.ceph.blog-manual-repair-object-2015） | [登记 URL](https://ceph.com/en/news/blog/2015/ceph-manually-repair-object/)；Squid 页所链 [ceph.io 旧址](https://ceph.io/geen-categorie/ceph-manually-repair-object/) | `3b3e2c97d4f8fe089b5816b711cdbd716b0b2db7f2630f526d32dab699bffaf3`（两址字节相同） | 署名 "Apr 27, 2015 shan"。链条与登记一致：health detail 定位 PG 17.1c1（acting [21,25,30]）→ `grep 'ERR'` OSD 日志 → `find` 进入 `/var/lib/ceph/osd/ceph-21/current/17.1c1_head/DIR_…` → 比对各副本 size/MD5 → 停 OSD → `--flush-journal` → 移走坏对象 → 启动 → `ceph pg repair`。正文没有写到的细节：①日志中 **shard 21 与 shard 25 两份**都报 `digest 0 != known digest 3062795895`，即三副本中有两份与已知 digest 不符；②博客开头建议"You can always try to run ceph pg repair … and check"，即先 repair 后调查；③两副本场景的"trick"是设置集群级 `noout`、停 OSD 等待同步；④`current/<pg>_head/DIR_*` 目录与 journal flush 都属于 FileStore 布局。→ C11/C16 |
| Squid OSD 排查页（未登记；本轮旁证） | [troubleshooting-osd](https://docs.ceph.com/en/squid/rados/troubleshooting/troubleshooting-osd/) | `d835a6d2ce61b5bc6cf3f512e0ac42afb86b719ffa603ef459f498e57ae7e7fc` | Warning："Reef does not support FileStore. Releases after Reef do not support FileStore. Any information that mentions FileStore is pertinent only to the Quincy release of Ceph and to releases prior to Quincy." "Stopping without Rebalancing" 节说集群级 `ceph osd set noout` 只是 "thought exercise"，Luminous 及以后宜用 `ceph osd add-noout osd.N` / `set-group noout <bucket>` 只标记受影响对象，并注明 OSD 停止后其 PG 标为 degraded。→ C11/C16 |
| Squid health-checks（未在本文 source_refs；T04-05 已用） | [health-checks](https://docs.ceph.com/en/squid/rados/operations/health-checks/) | `a6a9ed5466bb87fee93908d505ba59c96272961f2e72c1dec05a7955f0823907` | `OSD_FULL`：`ceph df`、`ceph osd dump \| grep full_ratio`；短期可 `ceph osd set-full-ratio <ratio>` 恢复写入；长期在合适的 CRUSH 故障域加 OSD 或删数据；并提示可能有残留的 rados bench 对象，"very, very carefully deleted"。另有 `OSD_NEARFULL`/`OSD_BACKFILLFULL`/`POOL_FULL`。`PG_DAMAGED` 包含 repair 进行中的状态；`OSD_TOO_MANY_REPAIRS` 说明读修复计数可揭示 scrub 未报的坏盘。→ C14/C15 |
| ceph/ceph v19.2.7 回归测试（src.ceph.repo-v19.2.7 同 tag，测试文件未登记） | `git ls-remote https://github.com/ceph/ceph.git`；[osd-scrub-repair.sh@v19.2.7](https://raw.githubusercontent.com/ceph/ceph/v19.2.7/qa/standalone/scrub/osd-scrub-repair.sh) | 脚本 `3a696cb279d4274c7d7a338f0872ae35e16202d259226dc428b24355337f52f3`（6258 行） | `refs/tags/v19.2.7` → tag 对象 `c24c6707…`，`^{}` → commit `9ec952b9…`，与登记一致。`TEST_corrupt_and_repair_replicated`（L93）对非主与主副本分别调用 `corrupt_and_repair_one`；后者为 L225 起，依次 `objectstore_tool … remove` → `repair $pg` → `list-attrs` → `rados get` → `diff ORIGINAL COPY`。L106 注释 "Reproduces http://tracker.ceph.com/issues/8914"（tracker 内容本轮未打开）。同文件有 `TEST_auto_repair_bluestore_*`、`TEST_repair_stats` 等。这是固定 tag 上的正式上游修复测试，且读回 diff 本身就是"可读/完整"判据的样板。→ C11/C12 |
| nfs(5)（src.nfs-utils.nfs-5-man7） | [nfs.5](https://man7.org/linux/man-pages/man5/nfs.5.html) | `2b9d9223f2faeadffdc7c50936a7d03ae0a194c25d9fc3d1662d40dd22e534fb` | `soft / softerr / hard`："Determines the recovery behavior of the NFS client after an NFS request times out"；hard 无限重试；soft/softerr 在 retrans 次后返回 EIO/ETIMEDOUT；"soft timeout can cause silent data corruption"。`timeo`：TCP 默认 600（60 s），线性退避至 600 s；UDP 用自适应算法。`retrans`：未指定时 UDP 3 次、TCP 2 次；"generates a 'server not responding' message after retrans retries"。→ C14/C15 |
| ext4 admin-guide v6.16（T04-02 已用，归 src.kernel.docs-ext4-v6.16 族） | [admin-guide/ext4](https://www.kernel.org/doc/html/v6.16/admin-guide/ext4.html) | `2849c200bf74329159de5009afa1ed9816096a868bcfee94a20126a02c3a1e84` | `errors=remount-ro` / `continue` / `panic`，挂载选项覆盖超级块中的 errors 行为。这是"remount-ro"的官方触发条件，正文没有使用。→ C14/C16 |
| Lustre Operations Manual 2.x（src.lustre.ops-manual-2x） | [lustre_manual.xhtml](https://doc.lustre.org/lustre_manual.xhtml) | `63b09d0650de3491eee9c976dff1246706dc6496bc996c139fdebdf7fc4a0d8c`（与 B20、B21-T04-06 审阅取得的字节相同） | 目录核对：**§1.2.2 是 "Lustre File System Components"**（架构说明，不是状态入口）；§23.1 "Handling Full OSTs"（23.1.2 Disabling creates on a Full OST、23.1.3 Migrating Data within a File System）属实；§12.2 Jobstats、Ch.39 Lustre Parameters 属实。**正文未用**：Ch.38 "Lustre File System Recovery"（38.1.1 Client Failure、38.1.2 Client Eviction、38.1.3 MDS Failure、38.1.4 OST Failure、38.1.5 Network Partition、38.1.6 Failed Recovery、38.2 Metadata Replay、38.4 Version-based Recovery、38.6 Imperative Recovery）；Ch.35 "Lustre File System Troubleshooting"（35.3.1 OST Object is Missing or Damaged、35.3.2 OSTs Become Read-Only、35.3.3 Identifying a Missing OST）；Ch.36 Troubleshooting Recovery（36.1 backing ldiskfs 错误/损坏、36.4 LFSCK）；`health_check` 的 "not healthy" 判读；`lfs check servers`、`lfs df`。→ C14/C16 |

取证限制：

- 未检索 Ceph RGW 的健康、日志或管理面（radosgw-admin）文档。C14 只指出正文 RGW 一侧没有入口，不断言官方没有相关文档。
- `osd-scrub-repair.sh` 只读了 L93–112 与 L225–246 两段及函数列表，没有审计其余测试；tracker #8914 未打开。
- 未核对 Squid 是否仍能运行 FileStore OSD。上表 Warning 原文写的是 "Reef does not support FileStore"，Squid 晚于 Reef，本审阅据此判断，但未见到 Squid release notes 原文。
- 内核 NFS 文档、exports(5)、RGW S3 文档本轮未重取。它们在本文正文中没有新的具体主张（见 C17）。
- 未执行任何命令行为验证；上述所有行为都是文档或源码层证据。

## 发现

### B21-C10 — P1 / OPEN：官方 repair 前不一致清单被记为 unknown；`pg repair` 被写成"从可信副本恢复"，与 Squid 原文相反

位置：正文 §3 L60、L62、L63；§2 L56；"来源与更新范围" L76；来源记录 L9、L15；acceptance 3。

证据：

- 正文 L60 写"Ceph repair 前的不一致对象清单无官方原文时记 unknown"，L76 与来源记录 unknown 清单第 3 条也写"repair 前清单原文"未定。Squid PG 页的 `rados list-inconsistent-pg <pool>` 与 `rados list-inconsistent-obj <pgid> --format=json-pretty` 正是官方的 repair 前不一致对象清单：它给出逐 OSD 的 size/data_digest/omap_digest 和逐 shard 错误。登记 L5145 的 revision 也写了"核对 list-inconsistent-pg/obj"。正文、来源记录和登记三处互相矛盾。
- 同页 Warning 要求：shard 错误含 `read_error` 时，repair 前先查 `dmesg` 与 `smartctl`。这一条是官方给出的"先保留证据、再修复"前置条件，正文没有写。
- 正文 L62 把 `ceph pg repair` 归入"从可信副本恢复"。原文写 checksum "cannot prove that any specific copy is in fact authoritative"；没有 checksum 时 repair "favors the data on the primary, but this might not be the uncorrupted replica"，因此 "human intervention is necessary"。对 replicated pool，repair 只把不一致副本标为 missing，"recovery is beyond the scope of pg repair"。repair 本身不保证副本可信。
- 正文 L56、L62 说"覆盖写警告见下/见案例"。原文 Warning 框讲的是物理存储错误，不是覆盖写。覆盖写的描述在 "More Information on PG Repair" 节，且同节限定"relevant for Filestore, but not for BlueStore"。正文没有写这一限定，也没有写 auto_repair 的条件（EC/BlueStore pool、错误数 ≤ `osd_scrub_auto_repair_num_errors` 默认 5）。
- 正文 L63"选错权威即丢数据"没有原文依据。原文只写到 primary"might not be the uncorrupted replica"。"丢数据"是本库推论，需要标注。

关闭条件：

- §3 第 1 步写入 Ceph 官方定位链（`ceph health detail` → `list-inconsistent-pg` → `list-inconsistent-obj --format=json-pretty`），说明应保存它的 JSON 输出；`read_error` 分支先查 `dmesg`/`smartctl`。删除正文、来源记录中"repair 前清单无官方原文"的 unknown。
- 把 `pg repair` 从"从可信副本恢复"中移出，单列为"按 Ceph 选定的权威副本修复，权威性不可证，需人工判断"，并引原文；replicated pool 的"标 missing、恢复不在 repair 范围内"一并写入。
- 写明 Filestore/BlueStore 限定与 auto_repair 条件；"丢数据"标为本库推论。

### B21-C11 — P1 / OPEN：上游案例是 FileStore 流程，不适用于 Squid；未说明适用边界；未选用固定 tag 上的正式回归测试

位置：正文 §4 L65–67；frontmatter L27、L33；来源记录 L10；登记 L5154–5164；acceptance 4 前半句；plan `source_discovery` L5323（"一项可追踪案例/回归测试"）。

证据：

- 博客流程依赖 FileStore：对象是 `current/17.1c1_head/DIR_*` 下的普通文件，可以 `find`、算 MD5、`mv`，还要 `--flush-journal`。Squid OSD 排查页写明 "Reef does not support FileStore. Releases after Reef do not support FileStore"。本文其余 Ceph 主张都以 Squid 为准，在 Squid（BlueStore）上，这个案例的"定位对象文件→移走"步骤没有对应操作。正文只写"旧版本命令只作流程参考"，没有说明整条流程的存储后端前提已不成立。
- 案例中有正文漏掉的风险证据。日志显示 shard 21 与 shard 25 **两份**都与已知 digest 不符，三副本里多数与 object info 不一致，博客随后却说"stop the OSD that has the wrong object"（单数）。"哪一份可信"在案例中本身就不清楚，这恰好能支持 C10 的"权威性不可证"，正文没有用上。
- 博客的操作顺序与本文 §3 的"先保证据"相反：开头即建议"You can always try to run ceph pg repair … and check"。两副本"trick"使用集群级 `noout`，Squid OSD 页已把集群级 noout 降为 "thought exercise"，建议改用 `add-noout`/`set-group noout`。正文对这两点都没有写。
- acceptance 4 要求"正式上游存储故障/修复**测试**案例"，plan source_discovery 写"可追踪案例/回归测试"。博客是操作演示，不是测试。登记的固定 tag v19.2.7（commit `9ec952b9`）中有 `qa/standalone/scrub/osd-scrub-repair.sh`：`TEST_corrupt_and_repair_replicated` 分别破坏非主与主副本，经 `ceph-objectstore-tool` 删除对象、`repair`、`rados get` 读回后与原件 `diff`，注释关联 tracker #8914。它使用 objectstore 工具而不是文件路径，不依赖 FileStore 布局，读回 diff 也可直接作为 §5 的"可读/完整"判据样板。
- 登记 kind 写 `documentation`。博客不是产品文档，建议改为与本库其他博客或案例类来源一致的 kind（若 schema 有对应值）。

关闭条件：

- §4 写明博客的 FileStore 前提，以及"Squid 不支持 FileStore"（引 Squid OSD 排查页，并登记该页）；把博客降为"历史流程参考，不适用于 Squid/BlueStore"。
- 写入"两份 shard 与已知 digest 不符"的细节，并说明它对权威副本选择的含义；写明博客"先试 repair"与集群级 noout 和本文流程或 Squid 建议的差异。
- 另选一个与 Squid 对应的正式上游测试作为主案例。建议用 v19.2.7 的 `osd-scrub-repair.sh`，写清测试函数名、行号、步骤和判据。若改选其他测试，同样固定 tag/commit 与行号；tracker 若引用，须实际打开核对。
- 核对登记 kind。

### B21-C12 — P1 / OPEN：演练判据没有设计，只有一句模板说明

位置：正文 §5 L69–71；acceptance 4 后半句；plan objective L5306。

证据：

- acceptance 4 要求设计五类判据：客户端重连、可读/完整/提交一致性、负载恢复、故障域演练（其中可读、完整、提交一致性分别算）。§5 只有一句话："以 §3 步骤为模板，每项列前置、预期、失败判据"，没有列出任何一项。
- 本库已有先例：T04-02 §5 与 T04-03 §5 都用"前置/预期（来源依据）/失败判据/实际（未执行，留空）/执行授权"表逐项列出。本文缺少同等结构。
- 可直接引用的已登记来源足以写出大部分判据：NFS 重连（grace/reclaim、verifier 变化即重发，见 T04-02 §3/§5）；Ceph 修复后的可读/完整（`rados get` + 与原件 diff，见 C11 的回归测试；修复后 PG 回到 `active+clean`、`PG_DAMAGED` 消除）；Lustre 客户端重连（Ch.38.1.2 eviction、38.1.6 failed recovery、38.2 replay）；故障域（Squid OSD 页 `set-group noout <CRUSH bucket>` 维护域示例、Lustre 38.1.3/38.1.4 failover）。负载恢复缺少基线时，可引 [T04-06 基线口径](../../knowledge/04-data-storage/storage-workload-baselines.md)，或记 unknown。
- "故障注入仅写方法及现场前提"这句满足 plan 的执行授权要求，但"方法"本身也没有写。

关闭条件：§5 改为逐项表格，至少覆盖五类判据，并按实现（ext4/NFS/Ceph/Lustre）分行；每项写前置、预期（带来源）、失败判据、实际（未执行，留空）、执行授权；无来源的项记 unknown 并说明原因。

### B21-C13 — P1 / OPEN：存储侧的前置与停止条件引用训练恢复指南，未给出存储恢复完成条件

位置：正文 §3 L61、L63；plan objective L5306；topic 04.6 gap `04.6-G3`（plan L1807–1815，"不得由训练恢复指南代替存储恢复"）。

证据：

- L61"保护恢复点"引用恢复诊断指南的前置条件；L63 repair/remount/回放的停止条件引用该指南"停止条件"。该指南的停止条件针对的是 DCP 装载与继续训练（"停止继续 load 或训练"），并不涉及 repair、remount 或日志回放。
- 该指南第 1 步写"不完整移交存储调查"，完整性证据页"官方反例与证据保留"节写"存储侧 repair/隔离流程归 T04-07"。也就是说，两页都把存储侧交给本文，本文又引回训练指南，形成循环，存储侧条件仍然没有落点。
- plan objective 要求"明确存储恢复与训练状态恢复各自完成条件"。正文没有存储恢复完成条件。可写入的已核对条件包括：Ceph `PG_DAMAGED`/`OSD_SCRUB_ERRORS` 消除且 PG 回到 `active+clean`（下一次 deep scrub 无新错误）；NFS reclaim 完成与 grace 结束（T04-02 §3/§5）；Lustre recovery 完成或 failed recovery 分支（Ch.38.1.6）；ext4 回放/检查完成。正文也没有写存储恢复完成后何时交给训练侧（恢复诊断指南第 1 步）。

关闭条件：

- §3 写本文自己的存储侧停止条件与完成条件，按实现分列并引来源；训练指南只作为"存储完成后的下游交接"引用。
- 增加一句交接说明：存储完成条件满足 → 训练侧按恢复诊断指南第 1 步开始；任何存储侧条件未满足时，不进入训练侧结论。

### B21-C14 — P2 / OPEN：证据入口不足或错位（acceptance 1）

位置：正文 §1 L42–47。

证据：

- **Lustre**：表中"MDT/OST 状态（手册 §1.2.2）"有误。§1.2.2 是 "Lustre File System Components"，即架构说明，不是状态入口。手册中可作入口的内容有：`health_check` 的 "not healthy" 判读、`lfs check servers`、`lfs df`、Ch.35.3（OST 对象缺失或损坏、OST 变只读、识别缺失 OST）、Ch.38.1（client/MDS/OST 故障与网络分区）。正文都没有用。
- **RGW**：只写"RGW 用量/日志（未登记，unknown）"。acceptance 1 要求"Ceph RGW/RADOS 健康"，RGW 一侧没有任何入口，unknown 也没有写明检索范围。T04-03 §4 已登记 `GET /?usage`，但那是用量统计，不是健康状态，正文也没有说明这一点。
- **Ceph 行**夹有一句"knfsd 类比不适用"，与该行内容无关。
- **ext4**：只写"日志回放完成"。ext4 admin-guide v6.16 的 `errors=remount-ro|continue|panic` 是"文件系统转只读"的官方条件，也是客户端可用性的直接证据，正文没有使用。
- **NFS**：重传统计记 unknown 可以接受（T04-02 已记 mountstats 未登记）。但 nfs(5) 写明 retrans 次重试后客户端产生 "server not responding" 消息，这是已登记来源中的客户端侧证据入口，正文没有写。
- 责任边界一栏四行都写了"分开判定"，但没有说明依据哪条证据判定属于哪一侧（例如 NFS："server not responding"指向服务器或网络，`soft` 返回 EIO 属于客户端选项后果）。

关闭条件：Lustre 行改引 Ch.35.3/38.1 与 `health_check`/`lfs check servers`，删除 §1.2.2；RGW 行写出健康入口或写明"未检索 RGW 健康/管理文档，unknown"；删除"knfsd 类比不适用"；ext4 行加 `errors=`；NFS 行加 "server not responding"；责任边界各写一条判据示例。

### B21-C15 — P2 / OPEN：故障覆盖已列出类别，但恢复动作没有落到选定实现条件（acceptance 2）

位置：正文 §2 L51–56。

证据：

- 四类故障都已列出，类别覆盖满足。但 acceptance 2 要求"恢复动作只能引用选定实现条件"，§2"恢复动作引用"一栏多为泛称："按实现重挂载/续凭据""超时参数与重试策略见各实现文档""清理/扩容"。
- **超时/重试**：nfs(5) 已给出 hard/soft/softerr 的恢复行为、timeo（TCP 默认 60 s、线性退避至 600 s）、retrans（TCP 2、UDP 3）和 soft 静默损坏风险。正文没有使用。RGW 超时、Lustre 超时（如 Ch.35.3.8）没有入口，也没有标 unknown。
- **空间耗尽**："池满"与"Full OST §23.1"放在同一格，混合了两个实现。Ceph 有 `OSD_FULL` 处理（`ceph df`、`full_ratio`、短期 `set-full-ratio`、加 OSD 或删数据、残留 rados bench 对象"very, very carefully"删除）；Lustre §23.1 有禁止在满 OST 上创建与数据迁移。正文对两者都只写了一个名称。ext4 inode 耗尽没有来源。
- **凭据**："续凭据"在 ext4/NFS/RGW/Lustre 中都没有引来源（NFS `sec=krb5*`、RGW S3 认证都已在本库其他页提及），应逐项引用或记 unknown。
- **后端降级**："OSD 慢盘"没有来源。Squid `OSD_TOO_MANY_REPAIRS` 与 `BLUESTORE_SLOW_OP_ALERT` 是可引的健康检查，本轮仅确认条目存在。

关闭条件：§2 改为"故障类别 × 实现"的结构，每格引用具体选项、健康检查或手册节，没有来源的格记 unknown；Ceph 池满与 Lustre Full OST 分开写。

### B21-C16 — P2 / OPEN：repair/remount/回放的风险与停止条件没有分实现、没有来源；Lustre 回放与 Ceph 服务恢复缺失

位置：正文 §3 L62–63；acceptance 3 后半句。

证据：

- acceptance 3 要求三类动作的风险与停止条件"独立说明"。L63 把三者写在一句话里，停止条件共用一组（"正确性失败、超时或观测窗口失效"），且来自训练指南（见 C13）。
- **remount**："remount 丢失未同步状态"没有来源。ext4 `errors=remount-ro` 是系统自动转只读的情形，与手动 remount 的风险不是一回事；NFS remount 与 hard/soft 的关系也没有写。
- **回放**：只写了 ext4 日志回放。Lustre 有专门的恢复与回放机制（Ch.38.2 Metadata Replay、38.2.7 Gaps in the Replay Sequence、38.4 Version-based Recovery、38.1.6 Failed Recovery）；NFS 的 reclaim 也属于状态回放（T04-02 §3）。正文都没有写，"回放依赖日志完整"也没有来源。
- **恢复服务**："OSD 重启/切出"没有来源。Squid OSD 排查页"Stopping without Rebalancing"给出维护前的 `add-noout`/`set-group noout`、停止后 PG 变 degraded、维护后 `unset`，并提示集群级 noout 只是 "thought exercise"。这是选定实现的官方条件，正文没有写。Lustre 的 MDS/OST failover（Ch.38.1.3/38.1.4）也没有写。

关闭条件：§3 第 4 步拆成 repair、remount、回放三个小节（或三行表），按实现写风险、前置、停止条件，并逐条引来源（Squid PG 页与 OSD 页、ext4 admin-guide、nfs(5)/T04-02 §3、Lustre Ch.38/36）；无来源的写成本库约定或 unknown。

### B21-C17 — P2 / OPEN：交付路径/ID 与计划不一致；source_refs 与正文依据不符；来源记录缺精确定位

位置：正文 frontmatter L2、L8–17、L28–33；plan L5302–5305、L5318–5321；roadmap L191；作者来源记录 L11、L15。

证据：

- plan target 为 `knowledge/04-data-storage/storage-client-backend-recovery.md` / `data-storage.storage-client-backend-recovery`（`state: planned_new`），roadmap L191 也是这一路径。交付的文件为 `storage-anomaly-and-recovery.md` / `data-storage.storage-anomaly-and-recovery`。两边都没有说明变更。T04-06 中同类问题（B21-C08）后来是按计划路径改名关闭的，可参照处理。
- `source_refs` 列了 `src.kernel.docs-nfs-v6.16`、`src.kernel.docs-ext4-v6.16`、`src.ceph.docs-rgw-s3-squid`，但正文没有链接这三者，也没有依据它们的具体主张。plan `existing_source_ids` 中的 `src.ceph.docs-scrubbing-latest-2026-10-08`、`src.ceph.repo-caf3def`、`src.google.sre-data-integrity` 未使用，也没有说明原因（其中 SRE 章 "data recovery plans should not rely upon replication" 与 C10/C11 的结论直接相关）。
- `verification.notes` 称"已核对 Squid PG 排查页定位链与修复警告"。但正文没有写定位链中的 `list-inconsistent-*`，"修复警告"的内容也与原文 Warning 框不符（见 C10）。
- 来源记录"客户端/后端证据"一行只写"见各自主文"，没有节号或条目名。AGENTS.md 要求"cite exact supporting pages or revisions near substantive claims"。

关闭条件：路径/ID 与计划对齐（改文件名与 ID 并同步 index，或在 plan 与 roadmap 中记录变更）；`source_refs` 与正文实际依据一致，新增依据（Squid OSD 排查页、health-checks、回归测试）先登记；plan 列出但不用的来源写明理由；notes 只写实际核对范围；来源记录逐主张写节号、条目或行号。

### B21-C18 — P3 / OPEN：读者可见文本中的计划 ID、模糊节号与措辞

位置：正文 L38、L44、L58、L60、L67、L75。

证据：

- 读者可见文本写"见 T04-02 §2""T04-02/03 登记复用"，这些是计划 ID，不是链接（B20-C40、B21-C05 已指出同类问题）。
- "[完整性证据 §8]"：目标页的标题没有编号。按 `##` 标题计数，第 8 个是"选定后端的读路径与校验责任"，而证据保留在第 10 个"官方反例与证据保留"。节号与链接都指不到正确位置。指向恢复诊断指南的两处链接也没有锚点。
- 标题"先保证据护恢复点"压缩过度，读者难以断句（应为"先保留证据、保护恢复点"）。
- §4 标题"2015 官方博客"：博客署名作者为 shan，发布在 Ceph 官方站点。建议写"Ceph 官方站点博客（2015，作者 shan）"，以免与官方文档混淆。

关闭条件：计划 ID 改为文档链接；节号改为节名并加锚点链接；修正标题措辞与博客描述。

## acceptance 对照

| acceptance | 判定 | 相关发现 |
|---|---|---|
| 1 四类实现的证据入口与故障责任边界 | 部分满足：四行都有；Lustre 节号错位，RGW 无入口，ext4/NFS 漏用已登记来源中的官方入口；责任边界没有判据 | C14（P2） |
| 2 故障覆盖；恢复动作只引用选定实现条件 | 部分满足：类别齐全；恢复动作多为泛称，没有落到实现条件 | C15（P2） |
| 3 先保证据与恢复点，再按官方条件选择；repair/remount/回放风险与停止条件独立 | 未满足：官方 repair 前清单被记 unknown；repair 被误称"可信副本恢复"；停止条件来自训练指南且没有分开；Lustre 回放与 Ceph 服务恢复缺失 | C10（P1）、C13（P1）、C16（P2） |
| 4 正式上游故障/修复测试案例；五类演练判据（未执行） | 未满足：案例不适用于 Squid，且不是测试；判据没有设计。"未执行"表述满足 | C11（P1）、C12（P1） |

横向问题：C17（路径与来源一致性，P2）、C18（措辞与链接，P3）。

## 结论

**T04-07 初审不通过，需修订。B21-C10–C18 共 9 项：P1 ×4（C10、C11、C12、C13），P2 ×4（C14、C15、C16、C17），P3 ×1（C18），全部 OPEN。** 修订后须按各项关闭条件做定向复核。正文 `verification.status: source_checked` 在 C10 与 C17 关闭前不应视为成立。本审阅只覆盖编辑与来源层面，未执行任何故障注入、repair、remount、重连或演练；文中所有存储行为都是文档或源码层证据，不得标为 reproduced。
