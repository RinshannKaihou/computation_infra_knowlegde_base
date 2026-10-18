# 第二十一批 T04-08 定向复核（第一轮）

复核日期：2026-10-18（实际取证日）。复核对象：提交 `3f11957ca2ef8af4a47078fdf21d318c4d7a09aa`（T04-08 初审修订）之后的当前工作区文件，即 [训练数据加载饥饿诊断指南](../../knowledge/04-data-storage/data-starvation-triage.md)、[Checkpoint 慢 I/O 诊断指南](../../knowledge/04-data-storage/checkpoint-slow-io-triage.md) 与作者来源记录 [batch-21-t04-08-sources.md](batch-21-t04-08-sources.md)。核验依据为 [初审报告](batch-21-t04-08-claude-review.md) 的 18 项发现（B21-C35–C52）及其关闭条件，以及作者 [修订记录](batch-21-review-fixes.md) 末节「T04-08 修订」。

**结论：T04-08 暂不通过。** 初审 18 项中 17 项 CLOSED，1 项 OPEN（B21-C50，P3）：来源记录定位表还有两行把正文未用的内容标为"直接"。修订另引入 5 项新发现（B21-C53–C57：P2 ×2、P3 ×3）：

- C54：checkpoint 计时例子写"序列化 CPU 在主线程"，与 v2.6.0 固定源码相反。
- C55：饥饿指南新增 RFC 8881 引用，但 `source_refs` 未列，与 C43 属同类缺陷。
- C53：自定义 stager 与前/反向重叠的条件写得不完整。这句措辞来自初审 C35 的关闭条件，见下文。
- C56：unknown 清单未收入修订新增的两类 unknown。
- C57：RGW 缓存格有一句无出处断言。

acceptance 1、3、4 通过。acceptance 2 部分满足：饥饿指南已满足，checkpoint 受 C54 影响。`make check` 通过（96 content entries / 446 sources），它只校验结构与本地链接，不说明技术正确性。

审阅者角色：与初审相同的独立审阅者，不是编写者。执行方式：本会话运行时系统提示标识的模型为 `claude-opus-5-5`（Claude Agent SDK 环境）。调用方没有提供 CLI modelUsage 一类的可核验记录，因此本报告无法独立证实模型身份；推理等级等运行元数据也没有可核验记录，不补造。这不是既有的 `gpt-6.1-sol / xhigh` 批量审阅约定，也不改写该约定。本轮只做只读核验：未改作者正文、来源记录、修订记录、登记、索引或计划，唯一新增文件是本报告；未执行任何训练、profiling、保存/恢复、负载工具或存储操作。模型审阅不构成平台、硬件或现场验证。

## 1. 输入（以 SHA-256 识别）

| 输入 | SHA-256 |
|---|---|
| [饥饿诊断指南](../../knowledge/04-data-storage/data-starvation-triage.md)（138 行；新增节 L93–106，完成判据 L127，来源条目 L137） | `1729513673762cecef77e5b25f525f63d125a0c15b72226c4f0b30f53a606855` |
| [Checkpoint 慢 I/O 诊断指南](../../knowledge/04-data-storage/checkpoint-slow-io-triage.md)（126 行；缺口声明 L59，新增节 L84–97，停止条件 L101，完成判据 L114，来源条目 L122，待确认 L126） | `dd99909422d81d9d7247e33937462bef8e834f80077c61565f232298e411c9b8` |
| [作者来源记录](batch-21-t04-08-sources.md)（43 行） | `ebc1be4fb29eac458e27a96bdb55c2a86ff2428489013700222a2598e50ce7fa` |
| [初审报告](batch-21-t04-08-claude-review.md) | `c99867734b1127eb60a6d369977fa616989d20b59049f4a3b69e4599da860e66` |
| [修订记录](batch-21-review-fixes.md)（「T04-08 修订」节 L446–467） | `7e00f95e7122e2cb5f1b959be186ba68d2d8669500df97a1cc9590469a4535a2` |

口径比对用的既有交付物、任务计划与来源登记，本轮哈希与初审逐一相同，初审的比对位置继续有效：T04-02 `7d70c719…c7cb`、T04-03 `e5ec20ce…e8b`、T04-06 `f92a5f80…481f`、T04-07 `aa9bb1d8…b40f`、T04-01 `f703eba9…cb81`、T04-04 `03fe46aa…481c`、计划 `7460b397…9d3`、登记 `88e48a04…74f`（全值见初审第 1 节）。

修订范围：`git show 3f11957 --unified=0` 的 hunk 只落在两篇的 `source_refs`、verification.notes、新增节（饥饿 L95、L99–102、L104；checkpoint L59、L86、L88–93、L95）、checkpoint 停止条件 L101、两篇完成判据补充句、T04-08 来源条目与 checkpoint 待确认 L126，以及来源记录 L8、L11–32、L38。原步骤 1–7、证据表与版本语义补充都没有改动。

## 2. 上游复取（审阅者独立获取）

全部用 `curl -sSL` 只读获取，默认 TLS 校验，HTTP 均为 200。原文放在临时目录 `/tmp/t0408r/`，未入库。

| 来源 | SHA-256 | 与初审 | 本轮核对点 |
|---|---|---|---|
| PyTorch v2.6.0 `state_dict_saver.py`（commit 1eba9b3，raw） | `a6fd9c92da2ab52dda5c433a041e6e0664aac974f659c16a1e4329ed69e8e68a` | 相同 | L227 `_stateful_to_state_dict`；L229 `stage`；L234 `executor.submit(save, …)`；L244–248 仅在 `should_synchronize_after_execute` 为真时调用 `synchronize_staging()`；`_save_state_dict` 内 L317 plan reduce_scatter、L323 `storage_writer.write_data`、L334 write all_reduce |
| 同 commit `staging.py` | `c1ec8939780a37a8d81858e8fe821a48b329c7fb6cc1cd36214be57d7b613ab2` | 相同 | L31–32 "dcp.save is called on the state_dict returned from stage in parallel. This call is responsible for serializing the state_dict and writing it to storage"；L34–39 该值为 True 时 synchronize_staging "will be called immediately after the serialization thread starts and before returning from dcp.async_save"，为 False 时由用户自定同步点，"(for example, by overlapping staging with the forward/backward pass)"；L44 协议默认 `_synchronize_after_execute = True`；L72/L81/L116 `BlockingAsyncStager` 阻塞拷贝、False、空操作 |
| 同 commit `filesystem.py`（本轮新取） | `5e4f5e5d707d0a94766ac3fe0b0329929b1f2345e8ffd0aa12b4e22bb8555b90` | — | L263 `_write_item` 内 `torch.save(data, stream)`（张量序列化）；L301–320 loader 与 BYTE_IO 经 `planner.resolve_data`；L507 `write_data` |
| 同 commit `default_planner.py`（本轮新取） | `1b66266c39a2476fda630ccd3c25ae1e547479b0fb01ac42a2102e9999ab08e1` | — | L136–138 `resolve_data`→`transform_object`；L146–148 BYTE_IO 时 `torch.save(object, bytes)`（非张量序列化） |
| nfs(5)（man7） | `2b9d9223f2faeadffdc7c50936a7d03ae0a194c25d9fc3d1662d40dd22e534fb` | 相同 | `lookupcache=mode`：all/none/pos(positive)；all 时正负目录项在父目录属性过期前视为有效，pos 时负项总是重验，none 时两类都重验；`actimeo` "sets all of acregmin, acregmax, acdirmin, and acdirmax to the same value" |
| exports(5)（man7） | `b71e95c6208c5480262437c9efd1b5bbcf3384fb60cecc6438f2a836fed5a5a2` | 相同 | 沿用初审核对（`async` 违反协议、异常重启可丢数据/损坏） |
| RFC 8881（rfc-editor 纯文本） | `3b7750c792f5e507cd69289cd1132034aed5ceadc03f5ddf24779426ea42474d` | 相同 | L8320 "During the grace period, the server must reject READ and WRITE …"；L14592 "pNFS is an OPTIONAL feature within NFSv4.1" |
| Lustre 2.x 手册 | `63b09d0650de3491eee9c976dff1246706dc6496bc996c139fdebdf7fc4a0d8c` | 相同 | §23.5.1 "the client will re-read or re-write the affected data up to five times … If it is still not possible, then an I/O error is returned"；ldiskfs "does NOT do any persistent checksumming"；§12.2 OST 侧 `obdfilter.*.job_stats` 示例给按作业的 read/write bytes（samples/min/max/sum）；brw_stats 为 OST I/O 请求直方图（§39.3.5） |
| 内核 v6.16 admin-guide/ext4 | `2849c200bf74329159de5009afa1ed9816096a868bcfee94a20126a02c3a1e84` | 相同 | `journal_path=path, journal_dev=devnum`（"When the external journal device's major/minor numbers have changed…"）；页内无"internal journal"或默认日志位置的表述 |
| 内核 v6.16 knfsd-stats | `ae000cd7d8da5232c0c801c83f020662f48ae0946245724275e2c0b0307d9d90` | 相同 | 沿用初审核对（只有 pool_stats 线程池计数） |
| fio-3.43 `io_u.c`（raw） | `a1b8dd596af63615722e2bce516ada1759cee77dbce378e2a9f7d6702933bca5` | 相同 | 沿用初审核对（L2097 clat、L2102 lat、L2427 slat） |

凡哈希相同的来源，初审第 1 节记录的原文核对点继续成立，本轮只补看上表列出的行。

## 3. 逐项判定

| ID | 优先级 | 关闭条件核验证据 | 判定 | 剩余差距 |
|---|---|---|---|---|
| B21-C35 | P2 | checkpoint L95 已改为默认 `BlockingAsyncStager` 下 staging 在主线程阻塞完成、先于后台 save，与后台 save 重叠的是后续训练步。链接 saver L229–248、staging.py L72–116，正文另引 L37。与 saver L229/L234/L248、staging.py L72/L81/L116 一致，"staging 与后台写重叠"已删除，内核 writeback 句保留 | **CLOSED** | 无。但新写的"自定义非阻塞 stager 可与前/反向重叠"缺少 `should_synchronize_after_execute=False` 这一条件，另立 C53（措辞源自初审关闭条件） |
| B21-C36 | P2 | 两篇 NFS 行（饥饿 L100、checkpoint L91）第 4 列改为"pNFS（RFC 8881 §12，OPTIONAL）在协议层分离 metadata server 与 storage devices，客户端 pNFS 范围 unknown（见本地与共享存储 §3）；非 pNFS 部署由同一服务器处理元数据与数据操作"。与 RFC L14592、T04-02 L91 一致；"协议层不分开"全文已无 | **CLOSED** | 无。饥饿指南因此新引了 RFC 8881，但 `source_refs` 未同步，另立 C55 |
| B21-C37 | P2 | 饥饿 L100 第 3 列带上 T04-02 L84 的 v3 限定与"Linux v4 客户端 CTO 行为未在已取源中单列（unknown）"。`actimeo` 与 `lookupcache=all\|none\|pos` 分开写，语义与 nfs(5) 原文一致。"不改变协议语义"全文已无 | **CLOSED** | 无 |
| B21-C38 | P2 | 饥饿 L104 ⑥、checkpoint L95 ④ 改为按实现写出各入口给出的量。knfsd-stats 只有线程池排队/唤醒计数（饱和信号，无请求字节/延迟）；Ceph health 是状态检查；Lustre Jobstats/brw_stats 给操作计数与 I/O 大小/时间分布；RGW（checkpoint 另含 NFS）后端逐操作字节/延迟记 unknown。饥饿 ⑥ 补"对照只在入口实际给出对应量时成立"。本轮看到 OST `job_stats` 示例含按作业 read/write 字节，饥饿 ⑥"可与应用侧请求对照"有出处 | **CLOSED** | 无。饥饿 ⑥ 没有像 checkpoint ④ 那样把"NFS 后端逐操作字节/延迟"单独记 unknown，但"knfsd-stats 无请求字节/延迟"与上述限定句已足以防止误用 |
| B21-C39 | P2 | 饥饿 L104 补 ②worker/CPU（锚证据表与数据路径阶段表）、③队列（下一顺位 batch 就绪与可交付队列为空时长，按序返回见 T04-01 L107）、④H2D 传输（NPU 计时 unknown）、⑤冷/热状态与工作集。checkpoint L95 ① 补状态收集/序列化 CPU 分开打点，⑤ 补读带宽、反序列化与 H2D 分开计时并标冷/热 | **CLOSED** | 覆盖层面已满足。① 把序列化写在主线程，与固定源码相反，另立 C54（P2）；acceptance 2 的判定受 C54 影响 |
| B21-C40 | P2 | 饥饿表：NFS 行补 T04-02 §5（L113）冷基线及其 unknown；RGW、Lustre 行记"冷/热基线入口 unknown"。checkpoint 表新增"争用观察点"列，四个实现逐行写明（RGW 记 unknown）；三类后端的读侧与缓存列都有冷/热入口或 unknown；Lustre 行补 §23.5.1 至多五次 re-read/re-write 与 Ch.35.3.8 初始建联超时 | **CLOSED** | 无。饥饿 RGW 格新增的"对象侧无客户端缓存层语义"无出处，另立 C57 |
| B21-C41 | P2 | checkpoint L91 补"违反 NFS 协议，异常重启可丢数据/损坏（exports(5)），Checkpoint 发布要求导出 `sync`（见本地与共享存储 §3/§4）"；停止条件 L101 补"不为提速……改用 NFS 导出 `async`"及理由。与 exports(5)、T04-02 L87/L100 一致 | **CLOSED** | 无 |
| B21-C42 | P2 | 饥饿 L101、checkpoint L92 均为"Complete 前后的可见性与列举一致性 unknown"，与 T04-03 L53 一致；"Complete 前"的收窄写法全文已无 | **CLOSED** | 无 |
| B21-C43 | P2 | 两篇 `source_refs` 已加 `src.kernel.admin-guide-ext4-v6.16`（饥饿 L20、checkpoint L22），两篇 T04-08 来源条目已列 admin-guide/ext4（L137、L122）。来源记录 L21 只留 admin-guide，`src.kernel.docs-ext4-v6.16` 已去掉 | **CLOSED** | 无。同类问题在 RFC 8881 上重现，另立 C55 |
| B21-C44 | P3 | 两篇 ext4 行第 4 列改为"默认内部日志时数据与日志同一设备；外部日志设备（`journal_dev`/`journal_path`）例外"，与关闭条件所给措辞一致；饥饿 L99 超时格与 T04-07 L60 对齐（"无超时挂载语义（块层命令超时不属本列范围，unknown）"） | **CLOSED** | 无。说明：admin-guide/ext4 页内只有外部日志设备选项，没有写日志的默认位置。"默认内部日志"这个限定词来自初审关闭条件的建议措辞，而本格的实际主张是"外部日志设备例外"，影响低，不另立发现 |
| B21-C45 | P3 | checkpoint L91 改为"grace 期服务器须以 NFS4ERR_GRACE 拒绝 READ/WRITE 与非 reclaim 锁请求，除非能保证安全"，锚点为 `#section-8.4.2.1`，与 RFC L8320 一致 | **CLOSED** | 无 |
| B21-C46 | P3 | 饥饿 L104 ⑦ 改为"slat（初始化到提交）/clat（提交到完成）、lat＝slat＋clat；io_u.c `issue_time`→clat L2097、`start_time`→lat L2102、slat L2427"，与 T04-06 L77 及 io_u.c 一致 | **CLOSED** | 无 |
| B21-C47 | P3 | 两篇节首（L95、L86）注明"Lustre 条目限 LTS 2.15.x 及以前引入的特性（见对象与并行存储 §1）"，T04-03 §1 L43 有稳定锚 LTS 2.15.x，范围句在 L34。checkpoint L93 带宽主张锚 §19.2，§19.3/§19.4 改标为命令节；`BAD WRITE CHECKSUM` 补"ldiskfs 无持久校验" | **CLOSED** | 无 |
| B21-C48 | P3 | checkpoint L92 改为"已登记来源内没有 RGW 逐操作计数器，暂按客户端计时＋网络/后端证据判定" | **CLOSED** | 无 |
| B21-C49 | P3 | L59 恢复"仍无已核对来源的支路只能按现场证据处理"，并补 NFS/RGW 传输选项层（rsize/wsize/proto、RGW HTTP 前端）。L59 与 L126 的 T04-08 五项相同，L126 另含既有的 DCP/MindIO/实测三项。来源记录 L38 扩为 12 项，初审逐条点名的缺项全部补入：RGW 读路径失败与超时、Complete 前后可见性、bucket 索引、ext4 inode/空间、NFS 服务器侧空间、Lustre 运行期超时与客户端缓存、v4 CTO | **CLOSED** | 无。修订新加的两类 unknown 没有进入清单，另立 C56 |
| B21-C50 | P3 | 定位表新增"引用方式"列（L13 有定义）。PG/OSD 排查、rados(8)、sysctl vm、MindIO、MLPerf 已改标"经链接沿用"；Lustre 行按实际引用收敛（§34.8/Ch.38 移出）；L8 的 rados bench 改记为"计时能力本轮未核对（`--show-time` 未评估）" | **OPEN** | 还有两行把正文未用的内容标为"直接"：L18 的"实现状态表、租约锁"（nfs41-server、client-identifier），两篇新增节都没有用到，pNFS 实现状态只经本地与共享存储 §3 间接出现；L24 的 PG_DAMAGED、OSD_TOO_MANY_REPAIRS、BLUESTORE_SLOW_OP_ALERT，两篇全文 0 次出现。这两行在 ea81e79 就已存在，初审 C50 的证据没有逐条点名，所以作者照点名清单修订时遗漏了它们。它们仍在"按正文实际直接引用收敛"的关闭条件之内。改法：把这两部分移到"经链接沿用"或删除 |
| B21-C51 | P3 | 两篇 notes（L41、L46）补"本轮未重取上游页面，新增条目以 T04-02/03/06/07 已核对口径与初审（B21-C35–C52）修订为准"；C35/C36/C37/C44 的派生主张已按初审核对的原文改写（见上行） | **CLOSED** | 无。修订中又出现了新的派生句（C54、C57），按新发现处理 |
| B21-C52 | P3 | 饥饿 L127 改为"判据 1–3 的完成记录（含硬失败修复后的同窗复核）还须同时包含"五项；完整性项按数据路径 §A 的字节校验和项核对（T04-01 L85 第 (2) 项），抽查范围由现场定；身份项引 §A 的 manifest（L85 第 (1) 项） | **CLOSED** | 无 |

计数：CLOSED 17（C35–C49、C51、C52），OPEN 1（C50）。

## 4. 新增发现（修订引入）

| ID | 优先级 | 受影响位置 | 摘要 |
|---|---|---|---|
| B21-C53 | P3 | checkpoint L95（"异步重叠不能简单相加"句） | 自定义 stager 与前/反向重叠的条件缺 `should_synchronize_after_execute=False` |
| B21-C54 | P2 | checkpoint L95 ① | "状态收集/序列化 CPU 与 staging 拷贝都在主线程"与 v2.6.0 固定源码相反 |
| B21-C55 | P2 | 饥饿 L8–20（source_refs）、L100、L137 | 正文新引 RFC 8881 §12，`source_refs` 与来源条目未列 `src.ietf.rfc-8881` |
| B21-C56 | P3 | 来源记录 L38；checkpoint L59；两表 NFS 行 | 修订新增的 unknown 未进入"完整清单" |
| B21-C57 | P3 | 饥饿 L101 第 3 列 | "对象侧无客户端缓存层语义"无出处 |

### B21-C53 — P3 / OPEN：自定义 stager 与前/反向重叠的条件写得不完整

位置：checkpoint-slow-io-triage.md L95，"只有自定义非阻塞 stager（`should_synchronize_after_execute`/`synchronize_staging`，…）才可能让 staging 与前/反向计算重叠"。

证据：

- staging.py L34–39：`should_synchronize_after_execute` 为 True 时，`synchronize_staging` "will be called immediately after the serialization thread starts and before returning from dcp.async_save"；只有设为 False，由用户在自定时点调用 `synchronize_staging`，才是"overlapping staging with the forward/backward pass"。
- staging.py L44：`AsyncStager` 协议默认 `_synchronize_after_execute = True`。saver L244–248 照此在 `async_save` 返回前调用 `synchronize_staging()`。
- 所以自定义非阻塞 stager 保留协议默认值时，`async_save` 仍要等 staging 完成才返回，staging 只与后台 save 的起始段重叠，不与前/反向重叠。正文只点出两个钩子名而没有给取值，持有这类 stager 的读者会把主线程等待 `synchronize_staging` 的时间误判为已被前/反向吸收。
- 来源说明：这句措辞照搬初审 C35 关闭条件（"仅自定义非阻塞 stager（`should_synchronize_after_execute`/`synchronize_staging`）可让 staging 与前/反向重叠"）。不精确源自初审，不是作者的偏离。默认路径的表述不受影响，所以定为 P3。

关闭条件：改为"仅当自定义 stager 的 `stage` 非阻塞、`should_synchronize_after_execute` 设为 False（协议默认 True，staging.py L44），且由用户在自定时点调用 `synchronize_staging` 时，staging 才可能与前/反向重叠（staging.py L34–39）；该值为 True 时 `async_save` 在返回前同步 staging（saver L244–248）"。链接范围覆盖 L34–L44。

### B21-C54 — P2 / OPEN：checkpoint 计时例子把序列化 CPU 写在主线程，与 v2.6.0 固定源码相反

位置：checkpoint-slow-io-triage.md L95 ①，"保存调用点停顿区间（状态收集/序列化 CPU 与 staging 拷贝都在主线程，分别打点…）"。

证据：

- staging.py L31–32：stage 返回后，"dcp.save is called on the state_dict returned from stage in parallel. This call is responsible for serializing the state_dict and writing it to storage"。
- 调用链：saver L234 把 `save` 提交给后台 executor；`_save_state_dict` 在 L334 的 write all_reduce 中经 L323 调用 `storage_writer.write_data`；filesystem.py L507 `write_data` → `_write_files_from_queue` → L263 `_write_item` 内 `torch.save(data, stream)` 序列化张量；非张量（BYTE_IO）经 `planner.resolve_data` 在 default_planner.py L148 `torch.save(object, bytes)` 序列化。两条序列化路径都在后台 save 线程里。
- `async_save` 在主线程执行的只有状态收集（saver L227 `_stateful_to_state_dict`）与 staging（L229）。同步 `save` 全部在调用线程执行，也没有 staging 步。① 的说法在两种模式下都不成立。
- 影响：按 ① 打点，会把后台的序列化 CPU 计入主线程停顿，或者在后台支路漏掉序列化。这与同文步骤 2（L77）"训练步正常但完成时间晚 → 后台/集合点支路"的分支相冲突，也与初审 C35 证据"后台 save（序列化、写入、两次集合点）"相反。这是 acceptance 2 点名的 staging/后台写入对齐层上的事实错误，与 C35 同级，定为 P2。

关闭条件：① 按 2.6 源码分写。`async_save` 的主线程为状态收集（saver L227）与 staging（L229）；序列化（filesystem.py L263、default_planner.py L148）与写入在后台 save 内，归入 ② 并与写入分开打点。同步 `save` 全部在调用线程、无 staging 步。如保留"状态收集"，限定为 `async_save` 调用前及 L227 的主线程部分。

### B21-C55 — P2 / OPEN：饥饿指南新引 RFC 8881 §12，`source_refs` 与来源条目未列

位置：data-starvation-triage.md L8–20（source_refs）、L100 第 4 列、L137。

证据：

- C36 修订后，饥饿 L100 内联链接 `https://datatracker.ietf.org/doc/html/rfc8881#section-12`。该 URL 在登记中对应 `src.ietf.rfc-8881`。ea81e79 版饥饿指南没有 RFC 8881 链接（`grep -c rfc8881` 为 0）。
- 饥饿 `source_refs`（L9–20，12 个 ID）没有 `src.ietf.rfc-8881`。L137 的 T04-08 来源条目列了 NFS 内核文档、nfs(5)、RGW、health-checks、Lustre、fio、admin-guide/ext4，没有 RFC 8881。
- checkpoint 两处都有，不受影响。本轮用脚本把两篇内联外链逐一映射到登记 ID 再对照 `source_refs`，T04-08 范围内只有这一处缺口。`make check` 不检查这类对应，所以没有报错。这与 C43 属同类缺陷，按同级定为 P2。

关闭条件：饥饿 `source_refs` 加 `src.ietf.rfc-8881`；L137 来源条目补"RFC 8881（§12）"。

### B21-C56 — P3 / OPEN：修订新增的 unknown 未进入"完整清单"

位置：来源记录 L38；checkpoint L59（"完整清单见来源记录"）；饥饿 L100、checkpoint L91 的 NFS 行。

证据：

- C36、C40 修订在两表 NFS 行新写入两类 unknown：一是客户端 pNFS 实现范围（两表第 4 列）；二是 NFS 冷/热基线中，drop_caches 后属性/目录项缓存与 v4 委托是否随之失效，以及服务器侧缓存（饥饿第 3 列、checkpoint 第 3 列，沿用 T04-02 L113）。
- 来源记录 L38 的 12 项都没有这两类，第 5 项只有 mountstats/nfsstat、服务器侧空间与 v4 CTO。checkpoint L59 仍称"完整清单见来源记录"。修订记录 L464 写"覆盖两表出现的全部 unknown"，与实际不符。

关闭条件：L38 补"客户端 pNFS 实现范围；NFS 冷/热基线中属性/目录项缓存与 v4 委托失效、服务器侧缓存"两项，或把 L59 的"完整清单"改为"主要清单"并列出差异。下一轮修订记录据实更正"全部"的表述。

### B21-C57 — P3 / OPEN：饥饿 RGW 缓存格"对象侧无客户端缓存层语义"无出处

位置：data-starvation-triage.md L101 第 3 列。

证据：

- 这句是 C40 修订新增的（ea81e79 版没有），没有内联来源，也没有标本库推论。T04-03 全文"缓存""cache"均为 0 次出现，来源记录 L22 的 RGW 行也没有对应主张。
- 已登记来源最多只能支持"Squid RGW S3 文档未定义客户端缓存语义"。训练读取对象存储时，SDK、挂载层或数据集库是否带缓存取决于现场实现。照原句读，读者可能跳过缓存冷/热状态的记录，这与同文计时例子 ⑤"标注冷/热状态"相冲突。

关闭条件：改为"已登记来源未定义 RGW 客户端缓存语义；SDK/挂载层/数据集库的缓存按现场实现记录，冷/热基线入口 unknown"，或标本库推论并写理由。

## 5. 逐条验收判定

| # | acceptance（计划 L5365–5368） | 判定 | 依据 |
|---|---|---|---|
| 1 | 保留相邻边界判断和已有 fixed DataLoader/DCP/MindIO 实现，不因后端类型新增统一调参命令 | **通过** | 修订 hunk 只落在 T04-08 新增节、notes、来源条目、缺口声明/待确认与停止条件（见第 1 节）；原步骤 1–7、证据表与固定锚点都没有改动。两篇新增节仍写"不给跨后端的统一调参命令"。停止条件 L101 新加"不改用导出 `async`"，边界只收紧不放宽。初审保留意见 C41、C49 已关闭 |
| 2 | 给出客户端/缓存、后端、CPU/队列、传输、staging/后台写入/read 的同窗计时对齐例子；明确异步重叠不能简单相加 | **部分** | 饥饿指南满足：①–⑦ 覆盖消费侧、worker CPU、队列、H2D 传输、冷/热、后端（按实现写出给出的量）与离线基线，关键路径判定明确。checkpoint 已覆盖 staging、后台、内核、后端、读侧/H2D/冷热，默认路径的重叠语义已与源码一致（C35 CLOSED），后端可用量已更正（C38 CLOSED）。但 ① 把序列化写在主线程（C54，P2），这正是本项点名的 staging/后台写入对齐层，所以本项只判部分；C53 为附带的精确度问题 |
| 3 | 为 NFS/RGW/Lustre 的争用、重试、元数据、cold/warm 和空间压力增加入口，链接独立基线与恢复流程 | **通过** | 两表三类后端的五类入口齐全，无来源处显式记 unknown。checkpoint 新增争用列，Lustre 补重试/超时。两篇都链接存储负载基线与存储恢复。初审列出的口径偏差（C36、C37、C42、C45、C47）已全部关闭。保留意见：C57（RGW 缓存格无出处句）、C56（unknown 清单）、C55（来源元数据） |
| 4 | 完成判据同时检查数据/制品身份、作业进展、完整性、时延/吞吐和资源代价；来源记录说明未运行工具 | **通过** | 饥饿 L127 已把五项扩到判据 1–3（含硬失败修复后），完整性锚 T04-01 §A 字节校验和（C52 CLOSED）。checkpoint L114 五项不变。来源记录 L38 第 12 项与两篇 notes、来源条目都写明本轮未运行任何工具 |

## 6. 总体结论

**暂不通过。** 初审 18 项中 CLOSED 17、OPEN 1（B21-C50）。新增 5 项（B21-C53–C57），其中 P2 两项：C54 是事实错误，C55 是来源元数据缺口。下一轮需关闭 C54、C55；C50、C53、C56、C57 都是 P3，改动小，建议同轮处理。之后对这 6 项做定向复核。acceptance 2 随 C54 关闭重新判定。

范围外观察（不编号，不计入本轮发现）：

- checkpoint L53 的既有阶段链"状态收集与序列化 → staging → 后台写入"（Batch 10 内容，不在 T04-08 diff 内）把序列化排在 staging 之前。对 `async_save` 而言，序列化在 staging 之后、后台 save 内进行。C54 可能由这句诱发。修 C54 时建议一并评估这句是否需要按同步/异步分写，以免同文自相矛盾。
- 初审 4.1 列出的三条范围外观察（nfs(5) v4 `cto/nocto`、T04-04 §2 L53 的同类收窄、RGW Metrics 页可作关闭路径）本轮未变，不重复。

## 7. 保留边界与无法核验事项

保留边界：

- 本复核只核对文本与上游文档/源码之间、以及本库各层记录之间的一致性，不构成平台兼容、硬件或现场验证。
- 没有执行 DataLoader、profiler、DCP 保存/恢复、MindIO、fio、rados bench，也没有做任何 NFS 挂载、RGW 请求或 Lustre 命令。文中所有"行为"都是文档或源码层证据。
- 本报告不改变任何正文的编辑状态或 `verification.status`，也不回填计划或批次状态。
- 初审自身不精确之处如实记录，不改写初审报告：C35 关闭条件的 stager 条件不完整（见 C53）；C44 关闭条件建议的"默认内部日志"在 admin-guide/ext4 页内没有原文；C50 的证据没有逐条点名 L18、L24 两行。

无法核验事项：

1. 执行模型身份：运行时系统提示标识为 `claude-opus-5-5`，但没有 CLI modelUsage 等可核验记录；推理等级未知。
2. 任何运行行为：未执行训练、profiling、保存/恢复或存储操作；未运行 `make build`（会写 `build/`，超出只读复核范围），只运行了 `make check`，运行前后 `git status` 均干净。
3. nfs(5)/exports(5) 的 nfs-utils release/commit 哈希沿用 unknown。本轮字节与初审相同，但无法证明与作者登记时的页面相同。
4. Ceph Squid 文档是分支文档，点版本 unknown；本轮未重取 RGW S3 与 health-checks 页，沿用初审取证。
5. Lustre：§12.2 Jobstats 与 §23.5.1 等所引章节是否都属 ≤ LTS 2.15.x 引入的特性，仍没有逐条核对 "Introduced in" 标记。初审第 5 节第 9 项（OST 侧 Jobstats 字段）本轮已核：OST 示例给按作业的 read/write bytes 计数（samples/min/max/sum），示例中没有时延字段。
6. RFC 8881 仍取 rfc-editor.org 纯文本，与登记的 datatracker HTML 未逐字比对。
7. filesystem.py 与 default_planner.py 本轮首次取哈希，初审没有对应记录可比；同一 commit（1eba9b3）下按 raw 内容核对行号。
8. T04-02/03/06/07/01 本身的正确性只就与 T04-08 相关的条目做了抽查，不构成对这些交付物的复审。
