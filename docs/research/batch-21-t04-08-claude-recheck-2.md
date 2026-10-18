# 第二十一批 T04-08 定向复核（第二轮）

复核日期：2026-10-18（实际取证日）。复核对象：提交 `a6f841f518d9fee399e944dc353284aed3919a00`（T04-08 第二轮修订）之后的当前工作区文件，即 [训练数据加载饥饿诊断指南](../../knowledge/04-data-storage/data-starvation-triage.md)、[Checkpoint 慢 I/O 诊断指南](../../knowledge/04-data-storage/checkpoint-slow-io-triage.md) 与作者来源记录 [batch-21-t04-08-sources.md](batch-21-t04-08-sources.md)。核验依据：[第一次定向复核](batch-21-t04-08-claude-recheck.md)仍 OPEN 的 B21-C50 与新增 B21-C53–C57 的关闭条件，以及[修订记录](batch-21-review-fixes.md)末节「T04-08 第二轮修订」（L469–476）。

**结论：T04-08 暂不通过。** 本轮核验 6 项，CLOSED 3（C53、C55、C57），OPEN 3（C50、C54、C56）。另有 2 项新发现（B21-C58、B21-C59），均为 P3。现存 5 项 OPEN 全部为 P3。C54 原定 P2，现在 `async_save` 主线程与后台的分界已与固定源码一致，技术主体接受。剩下的是同步模式的限定，按本库先例（[Batch 18 第四次复核](batch-18-codex-fourth-recheck.md) C12）降为 P3，沿用原 ID。

- C54：① 没有限定 `async_save`；关闭条件要求的"同步 `save` 全部在调用线程、无 staging 步"没有写入。
- C58：C54 修订后，checkpoint L53 的阶段链"状态收集与序列化 → staging"与 L95 ①"序列化在后台 save 内执行"在同一篇里直接矛盾。
- C56：unknown 清单仍缺两表 NFS 冷/热基线格中的"服务器侧 unknown"。
- C50：定位表 fio 行的"与负载矩阵参数"仍标"直接"。
- C59：C54 新增的源码锚点没有进入来源记录；两篇 verification.notes 的取证口径没有随修订同步。

acceptance 1–4 均判通过，其中 2、3 带保留意见（见第 5 节）。`make check` 通过（96 content entries / 446 sources），它只校验结构与本地链接，不说明技术正确性。

审阅者角色：与初审、第一次复核相同的独立审阅者，不是编写者。执行方式：本会话运行时系统提示标识的模型为 `claude-opus-5-5`（Claude Agent SDK 环境）。调用方没有提供 CLI modelUsage 一类的可核验记录，本报告无法独立证实模型身份；推理等级等运行元数据也没有可核验记录，不补造。这不是既有的 `gpt-6.1-sol / xhigh` 批量审阅约定，也不改写该约定。本轮只做只读核验：未改作者正文、来源记录、修订记录、登记、索引或计划，唯一新增文件是本报告；未执行任何训练、profiling、保存/恢复、负载工具或存储操作。模型审阅不构成平台、硬件或现场验证。

## 1. 输入（以 SHA-256 识别）

| 输入 | SHA-256 |
|---|---|
| [饥饿诊断指南](../../knowledge/04-data-storage/data-starvation-triage.md)（139 行；source_refs L8–21，notes L42，后端表 L98–103，计时例子 L105，完成判据 L128，来源条目 L138） | `f58ea2faa0eff1966ce23b1ac1130342bc5f15dc5caf9633b59b1f93eb5a8a6b` |
| [Checkpoint 慢 I/O 诊断指南](../../knowledge/04-data-storage/checkpoint-slow-io-triage.md)（126 行；notes L46，阶段链 L53，缺口声明 L59，后端表 L88–93，计时例子 L95，来源条目 L122，待确认 L126） | `c92ec2e3f0500bd562edf1799f424ee1b14d7c77f50ec5356252ccc562fccace` |
| [作者来源记录](batch-21-t04-08-sources.md)（43 行；定位表 L15–32，unknown 清单 L38） | `9567180a41cd941bd4665d88db3eff90921f048e020ce180ce2a16a6ab023dec` |
| [第一次定向复核](batch-21-t04-08-claude-recheck.md) | `4b0b179d8f32ca1760dcb31454a85e5129394588e00c4089b725ba75a99d23ab` |
| [初审报告](batch-21-t04-08-claude-review.md)（与第一次复核所记相同） | `c99867734b1127eb60a6d369977fa616989d20b59049f4a3b69e4599da860e66` |
| [修订记录](batch-21-review-fixes.md)（476 行；「T04-08 第二轮修订」L469–476） | `52400deab721332ad60a66061786f871b86ff9fb5c001abb8fc82fc0e4bdb54e` |

修订范围：`git show a6f841f --unified=0` 在三份复核对象上的 hunk 只有饥饿 L16（source_refs 加 `src.ietf.rfc-8881`）、L102（RGW 缓存格）、L138（来源条目），checkpoint L95（① 与重叠条件句），来源记录 L18、L24、L38。原步骤 1–7、证据表、后端表其余格、停止条件与完成判据都没有改动。同一提交还新增了第一次复核报告与修订记录末节，二者不是本轮复核对象。

## 2. 上游复取（审阅者独立获取）

全部用 `curl -sSL` 只读获取，默认 TLS 校验，HTTP 均为 200。原文放在临时目录 `/tmp/t0408r2/`，未入库。

| 来源 | SHA-256 | 与前次 | 本轮核对点 |
|---|---|---|---|
| PyTorch v2.6.0 `state_dict_saver.py`（commit 1eba9b3，raw） | `a6fd9c92da2ab52dda5c433a041e6e0664aac974f659c16a1e4329ed69e8e68a` | 同第一次复核 | 同步 `save` 自 L59 起，L152–153 在调用线程直接 `_save_state_dict(state_dict=_stateful_to_state_dict(…))`，无 executor、无 staging；`async_save` L227 `_stateful_to_state_dict`、L229 `stage`、L233–234 `ThreadPoolExecutor(max_workers=1)`/`executor.submit(save, …)`、L244–248 仅当 `should_synchronize_after_execute` 为真时 `synchronize_staging()` |
| 同 commit `staging.py` | `c1ec8939780a37a8d81858e8fe821a48b329c7fb6cc1cd36214be57d7b613ab2` | 同 | L31–32 后台 save 负责序列化与写入；L34–39 True/False 两种同步语义（False 时由用户自定同步点，例子为与前/反向重叠）；L44 协议默认 True；L72/L81/L116 `BlockingAsyncStager` 阻塞拷贝、False、空操作 |
| 同 commit `filesystem.py` | `5e4f5e5d707d0a94766ac3fe0b0329929b1f2345e8ffd0aa12b4e22bb8555b90` | 同 | L263 `torch.save(data, cast(IO[bytes], stream))`，张量直接序列化进文件流；L318–329 BYTE_IO 经 L320 `planner.resolve_data` 后整块写入，张量经 loader 后 L328 `_write_item` |
| 同 commit `default_planner.py` | `1b66266c39a2476fda630ccd3c25ae1e547479b0fb01ac42a2102e9999ab08e1` | 同 | L136–138 `resolve_data`→`transform_object`；L146–148 BYTE_IO 时 `torch.save(object, bytes)` |
| RFC 8881（rfc-editor 纯文本） | `3b7750c792f5e507cd69289cd1132034aed5ceadc03f5ddf24779426ea42474d` | 同 | 本轮无新主张，只确认字节未变 |
| 内核 v6.16 knfsd-stats | `ae000cd7d8da5232c0c801c83f020662f48ae0946245724275e2c0b0307d9d90` | 同 | C50 收窄后的 L18 只剩此页 |
| Ceph Squid health-checks | `a6a9ed5466bb87fee93908d505ba59c96272961f2e72c1dec05a7955f0823907` | 同初审（第一次复核未重取） | C50 收窄后的 L24 只剩 OSD_FULL/NEARFULL/POOL_FULL |

本轮修订不涉及 nfs(5)、exports(5)、Lustre 手册、admin-guide/ext4、fio，没有重取，沿用初审与第一次复核的核对。

## 3. 逐项判定

| ID | 原优先级 | 关闭条件核验证据 | 判定 | 剩余差距 |
|---|---|---|---|---|
| B21-C50 | P3 | L18 收窄为 knfsd-stats 一页（饥饿 L101、checkpoint L91 都直接链接该页）；L24 收窄为 OSD_FULL/NEARFULL/POOL_FULL（饥饿 L102、checkpoint L92 都直接引用），其余条目注明"本轮未直接引用"。两行都已满足。本轮把定位表 L17–L32 逐行对照两篇新增节（见 3.1） | **OPEN**（P3） | L25 fio 行写"fio 计时口径（…）与负载矩阵参数"，标"直接（饥饿指南）"。饥饿新增节直接引用的 fio 内容只有 ⑦ 的 slat/clat/lat（L105）。负载矩阵是 T04-06 §2「工作负载矩阵（维度→工具参数）」，只经 L107 的存储负载基线链接到达；来源记录自己的 L9 也写"fio 负载矩阵…复用 T04-06 交付物"，与 L25 自相矛盾。这半句自 ea81e79 就存在，初审与第一次复核都没有点名，是审阅侧遗漏，仍在"按正文实际直接引用收敛"的关闭条件之内。改法：删去"与负载矩阵参数"，或移到"经链接沿用"行 |
| B21-C53 | P3 | checkpoint L95 现为"只有自定义 stager 把 staging 做成非阻塞、且 `should_synchronize_after_execute=False`（协议默认 True；为 True 时 saver 在返回 Future 前调用 `synchronize_staging()`）时，staging 才可能与前/反向计算重叠"，链接 `staging.py#L37-L116`。对照源码：非阻塞与 False 两个必要条件齐全；"协议默认 True"即 L44，在链接范围内；True 分支由同句 saver L229–248 链接支撑（L244–248）；docstring 重叠例子 L37–39 在链接范围内 | **CLOSED** | 无。说明：关闭条件里"由用户在自定时点调用 `synchronize_staging`"没有写入正文，但它是 False 取值的语义（staging.py L35–39），不是另一个重叠条件，原文在链接范围内；链接从 L37 而非 L34 起，L34–36 的 True 分支内容已由 saver 链接覆盖。两点都不构成剩余差距 |
| B21-C54 | P2 | L95 ① 现为"主线程与后台的分界：状态收集与 staging 拷贝在主线程…；序列化在后台 save 内执行（自 saver L234 提交；写线程侧 filesystem.py L263、planner 侧 default_planner.py L148）；保存调用点停顿区间与后台完成分别打点"。对照源码：L227、L229 在调用线程，L234 提交后台，L263 与 L148 两条序列化路径都在后台 save 的写路径内。`async_save` 部分与源码一致，"序列化在主线程"的错误已消除，技术主体接受。关闭条件中"归入 ② 并与写入分开打点"不计为差距：张量的 `torch.save` 直接写入文件流（L263），在 Python 层序列化与写入是同一次调用，这项要求是复核者写得过细（见第 7 节） | **OPEN**（剩余降为 P3） | 关闭条件要求的"同步 `save` 全部在调用线程、无 staging 步"没有写入：L95 全行 `async_save` 与"同步"都是 0 次出现，① 没有限定模式。按字面读，"序列化在后台 save 内执行"对同步 `save` 不成立：同步路径（saver L59、L152–153）没有后台线程，也没有 staging。修订记录 L471 没有提到同步模式。改法：① 句首限定"`async_save` 时"，补一句"同步 `save` 无 staging 步，状态收集、规划、序列化与写入都在调用线程（saver L152–153），停顿即保存调用全程"。可与 C58 同改 |
| B21-C55 | P2 | 饥饿 source_refs L16 已列 `src.ietf.rfc-8881`；L138 来源条目已列"RFC 8881（§12）"，NFS 内核文档括注收窄为 knfsd-stats。本轮用脚本把两篇全部内联外链映射到登记 ID 并对照 source_refs：T04-08 范围内的外链都能落到 source_refs 中的 ID。knfsd-stats 是 `src.kernel.docs-nfs-v6.16` 的子页，PyTorch 固定 blob 链接分属 `src.pytorch.dcp-2.6`、`src.pytorch.dataloader-source-v2.6.0`（登记 revision 含 commit 1eba9b3） | **CLOSED** | 无。饥饿 notes L42 的来源枚举仍没有 RFC 8881，这超出 C55 的关闭条件，并入 C59 |
| B21-C56 | P3 | 来源记录 L38 第 5 项已补"客户端 pNFS 实现范围"与"冷/热基线中属性/目录项缓存与 v4 委托是否随本机 drop_caches 失效"。本轮把两表与两段计时例子中的全部 unknown 逐一对照 12 项清单，除下一格所列外都有对应 | **OPEN**（P3） | 第一次复核关闭条件列的第二项是"NFS 冷/热基线中属性/目录项缓存与 v4 委托失效、服务器侧缓存"，"服务器侧"没有补入。两表 NFS 缓存格（饥饿 L101 第 3 列、checkpoint L91 第 3 列）都写"服务器侧 unknown"，出处 T04-02 L113 冷基线行"服务器侧 unknown"。第 5 项的"服务器侧空间证据"对应的是空间列，不是这一项。checkpoint L59 仍称"完整清单见来源记录"。修订记录 L475 写"'完整清单'由此重新成立"，与实际不符，也没有按关闭条件据实更正 L464 的"全部"。改法：第 5 项补"冷基线的服务器侧缓存状态"；下一轮修订记录更正 L464 与 L475 的完整性表述 |
| B21-C57 | P3 | 饥饿 L102 第 3 列现为"冷/热基线入口 unknown（对象侧缓存语义无已核对来源）"；"无客户端缓存层"全文 0 次出现 | **CLOSED** | 无。关闭条件建议措辞中的"SDK/挂载层/数据集库的缓存按现场实现记录"没有采用。C57 担心的是读者因无出处断言而跳过冷/热记录；现在断言已删，同文 ⑤（L105）仍要求"标注冷/热状态与工作集"，这一风险已不存在 |

计数：CLOSED 3（C53、C55、C57），OPEN 3（C50、C54、C56）。

### 3.1 C50：定位表逐行核对（L17–L32）

"直接"按来源记录 L13 的定义判定：两篇新增节直接引用的才算。表述内容在新增节写出、细节链到 KB 页（如 RGW 条目）的，也算直接。新增节引用的同篇既有步骤锚点，不视为"经链接沿用"。

| 行 | 来源 | 标注 | 核对 |
|---|---|---|---|
| L17 | nfs(5) | 直接 | 符合：hard/soft/softerr/timeo、soft 风险、actimeo/lookupcache、CTO v3 语境都在饥饿 L101；checkpoint L91 引 hard/soft |
| L18 | knfsd-stats | 直接 | 符合（本轮已收窄） |
| L19 | RFC 8881 §18.3/§18.32/§8.4.2.1/§12 | 直接 | 符合：四节在 checkpoint L91 都有，§12 也在饥饿 L101 |
| L20 | exports(5) | 直接 | 符合：checkpoint L91、L101 |
| L21 | admin-guide/ext4 | 直接 | 符合：data=/commit=/barrier（checkpoint L90）、errors=（饥饿 L100）、journal_dev/journal_path（两篇） |
| L22 | RGW S3 | 直接 | 符合：multipart/upload-id/NoSuchUpload（checkpoint L92）、版本化三态（饥饿 L102）、`GET /?usage`（两篇） |
| L23 | Lustre 手册 | 直接 | 符合：所列各章节在两篇新增节都能找到 |
| L24 | health-checks | 直接 | 符合（本轮已收窄） |
| L25 | fio 3.43 | 直接（饥饿指南） | **不符**：slat/clat/lat 符合；"与负载矩阵参数"只经链接到达（见上表 C50 行） |
| L26 | profiler/dataloader 源码/data.html | 直接 | 符合：record_function 区间（饥饿 ①），"按序返回"在 ③ 写出 |
| L27 | DCP 2.6 | 直接 | 已列锚点符合（含新增节引用的同篇步骤 2/5）；C54 新增的 filesystem.py L263、default_planner.py L148 未列，属修订引入，见 C59 |
| L28–L32 | PG/OSD 排查、rados(8)、sysctl vm、MindIO、MLPerf | 经链接沿用 | 符合 |

## 4. 新增发现（修订引入）

| ID | 优先级 | 受影响位置 | 摘要 |
|---|---|---|---|
| B21-C58 | P3 | checkpoint L53 与 L95 ① | C54 修订后，同一篇对序列化位置的两处表述相互矛盾 |
| B21-C59 | P3 | 来源记录 L27；checkpoint notes L46；饥饿 notes L42 | 修订后来源说明文字没有同步：新增锚点未入定位表，notes 取证口径与来源枚举滞后 |

### B21-C58 — P3 / OPEN：C54 修订后 checkpoint 阶段链与计时例子对序列化位置的表述矛盾

位置：checkpoint-slow-io-triage.md L53「目标与触发条件」中的阶段链"**状态收集与序列化 → staging（设备到主机/主机内存拷贝）→ 后台写入 → …**"；L95 ①。

证据：

- L95 ① 修订后写"序列化在后台 save 内执行"，即在 staging 之后（saver L229 stage → L234 提交 → filesystem.py L263 / default_planner.py L148）。L53 仍把序列化排在 staging 之前，同一篇前后两种说法。
- 对照固定源码，L53 的次序在两种模式下都不成立：`async_save` 先 staging，序列化在后台写路径内；同步 `save` 没有 staging 步，序列化发生在写入过程中（saver L152–153 → filesystem.py L263）。
- L53 是仓库初始化时就有的 Batch 10 文字（`git log -L53,53` 只有 01e6aea），不在 T04-08 的 diff 内。第一次复核第 6 节把它列为范围外观察，并建议"修 C54 时一并评估……以免同文自相矛盾"。第二轮修订记录没有提到 L53。修订前 ① 与 L53 的说法一致（虽然都错），C54 修订后两处才形成同文矛盾，所以本轮按修订引入编号。读者按 L53 的阶段顺序打点，会和 ① 的分界冲突；但计时例子本身正确，所以定为 P3。

关闭条件：L53 按模式改写阶段链，例如"状态收集 →（仅 `async_save`）staging → 序列化与写入（`async_save` 时在后台 save 内；同步 `save` 在调用线程）→ 内核页缓存与 fsync → 存储后端 →（恢复侧）读与反序列化"；或在 L53 注明次序以 ① 的分界为准。这只是让既有表述与固定 DCP 实现一致，不违反 acceptance 1 的"保留已有 fixed DCP 实现"。可与 C54 剩余项同改。

### B21-C59 — P3 / OPEN：修订后来源说明文字没有同步

位置：来源记录 L27（DCP 行"精确页面/节"列）；checkpoint verification.notes（L46）；饥饿 verification.notes（L42）。

证据：

- (a) C54 修订在 checkpoint L95 新引了 filesystem.py L263 与 default_planner.py L148 两个固定源码锚点。来源记录 L27 的锚点列只有 state_dict_saver.py L228–242/L229–248/L273–334、staging.py L37/L72/L116、filesystem.py L290–302/L331–334/L617–674，`grep -c` 查 `L263` 与 `default_planner` 都是 0。saver L234 落在已列的 L229–248 之内，不算缺。登记 `src.pytorch.dcp-2.6` 的 revision 含源码 commit 1eba9b3，所以不需要新登记，只是定位表没有同步。
- (b) checkpoint notes 仍写"新增条目以 T04-02/03/06/07 已核对口径与初审（B21-C35–C52）修订为准"。C53/C54 的修订依据是第一次复核取得并核对的原文：filesystem.py 与 default_planner.py 在第一次复核第 2 节首次取哈希，staging.py L34–44 的同步语义也在那一轮核对。notes 的取证口径应延伸到第一次复核。这与 C51 是同类披露问题。
- (c) 饥饿 notes 枚举复用来源（"内核 v6.16 NFS、nfs(5)、Squid RGW S3 与健康检查、Lustre 2.x 手册、fio 3.43 计时锚点、admin-guide/ext4"），没有 RFC 8881。C55 修订后，同篇 source_refs（L16）与来源条目（L138）都已列入，三处不一致。

关闭条件：L27 补"filesystem.py L263、default_planner.py L148"；checkpoint notes 改为以"初审与第一次定向复核（B21-C35–C57）"的修订为准；饥饿 notes 枚举补 RFC 8881（§12）。

## 5. 逐条验收判定

| # | acceptance（计划 L5365–5368） | 判定 | 依据 |
|---|---|---|---|
| 1 | 保留相邻边界判断和已有 fixed DataLoader/DCP/MindIO 实现，不因后端类型新增统一调参命令 | **通过** | 第二轮 hunk 只落在第 1 节所列 7 处，原步骤、证据表与固定锚点都没有删改；两篇新增节仍写"不给跨后端的统一调参命令"。C58 建议的 L53 改写是把既有表述对齐固定实现，不削弱本项 |
| 2 | 给出客户端/缓存、后端、CPU/队列、传输、staging/后台写入/read 的同窗计时对齐例子；明确异步重叠不能简单相加 | **通过**（保留：C54 剩余、C58） | 饥饿指南与上轮相同，满足。checkpoint ① 的主线程/后台分界已与固定源码一致（C54 技术主体接受），重叠条件已完整（C53 CLOSED），后端可用量与读侧分段沿用上轮已关闭的结论。上轮判"部分"的原因（序列化写在主线程）已消除。剩余的是同步模式限定与 L53 概述的次序矛盾，不影响例子对 staging/后台写入层的对齐内容 |
| 3 | 为 NFS/RGW/Lustre 的争用、重试、元数据、cold/warm 和空间压力增加入口，链接独立基线与恢复流程 | **通过**（保留：C56） | 两表五类入口齐全，无来源处显式记 unknown；C57 无出处句已删；C55 来源元数据已补。剩余 C56 只涉及来源记录清单是否完整，正文入口不受影响 |
| 4 | 完成判据同时检查数据/制品身份、作业进展、完整性、时延/吞吐和资源代价；来源记录说明未运行工具 | **通过** | 两篇完成判据本轮未改（饥饿 L128、checkpoint L114）；来源记录 L38 第 12 项、两篇 notes 与来源条目都写明本轮未运行任何工具 |

## 6. 总体结论

**暂不通过。** 本轮 6 项中 CLOSED 3、OPEN 3；新增 2 项。T04-08 累计 25 项（B21-C35–C59）：CLOSED 20，OPEN 5（C50、C54、C56、C58、C59），全部为 P3。acceptance 1–4 的实质内容已满足；按本库审阅约定，OPEN 项须经修订并定向复核后才能宣告通过。

5 项改动都很小，建议同轮完成：

- checkpoint：L95 ① 限定 `async_save` 并补同步 `save` 句（C54），L53 阶段链按模式改写（C58），notes 取证口径延伸到第一次复核（C59b）。
- 饥饿：notes 来源枚举补 RFC 8881（C59c）。
- 来源记录：L25 删去或移出"与负载矩阵参数"（C50），L27 补两处锚点（C59a），L38 第 5 项补"冷基线的服务器侧缓存状态"（C56）。
- 修订记录：据实更正 L464"全部"与 L475"完整清单由此重新成立"的表述（C56）。

本轮已对定位表逐行核对（3.1），也对两表全部 unknown 逐项对照了清单。除上列各项外，没有发现其他不一致。下一轮定向复核只需核对这 5 项及其修订 hunk。

范围外观察（不编号，不计入本轮发现）：

- checkpoint 完成判据 L109 把"序列化"与"写线程"列为两个可定位阶段（Batch 10 内容）。对张量数据，两者在 filesystem.py L263 是同一次 `torch.save(data, stream)` 调用，不加专门埋点就无法分开计时。是否需要说明，由作者另行评估。
- checkpoint 步骤 6 与来源条目 L120 的 MindIO 接口页链接，按 URL 前缀落在 `src.ascend.mind-cluster*` 登记下；source_refs 列的是 `src.ascend.mindio-acp-v26.1.1`（登记 URL 为 ACP README）。这属于 Batch 10 内容与登记粒度问题，本轮未判断。
- 初审 4.1 与第一次复核第 6 节列出的其余范围外观察本轮未变，不重复。

## 7. 保留边界与无法核验事项

保留边界：

- 本复核只核对文本与上游文档/源码之间、以及本库各层记录之间的一致性，不构成平台兼容、硬件或现场验证。
- 没有执行 DataLoader、profiler、DCP 保存/恢复、MindIO、fio、rados bench，也没有做 NFS 挂载、RGW 请求或 Lustre 命令。文中所有"行为"都是文档或源码层证据。
- 本报告不改变任何正文的编辑状态或 `verification.status`，也不回填计划或批次状态。
- 审阅侧不精确之处如实记录，不改写前两份报告：第一次复核 C54 关闭条件"与写入分开打点"写得过细（张量路径序列化与写入同一次调用）；C53 关闭条件"链接范围覆盖 L34–L44"多要了 L34–36（True 分支已由 saver 链接覆盖）；C50 的 L25 残留初审与第一次复核都没有点名。

无法核验事项：

1. 执行模型身份：运行时系统提示标识为 `claude-opus-5-5`，没有 CLI modelUsage 等可核验记录；推理等级未知。
2. 任何运行行为：未执行训练、profiling、保存/恢复或存储操作。只运行了 `make check`，运行前后 `git status` 均干净；未运行 `make build`（会写 `build/`，超出只读复核范围）。
3. nfs(5)、exports(5)、Lustre 手册、admin-guide/ext4、fio、Ceph RGW S3 本轮没有重取（第二轮修订不涉及其主张），沿用前两轮取证。nfs-utils release/commit 哈希仍为 unknown；Ceph Squid 点版本仍为 unknown。
4. Lustre 所引章节是否都属 ≤ LTS 2.15.x 引入的特性，仍没有逐条核对 "Introduced in" 标记。
5. RFC 8881 取 rfc-editor.org 纯文本，与登记的 datatracker HTML 未逐字比对。
6. T04-02 L113（冷基线"服务器侧 unknown"）按现文引用，未复审 T04-02 本身。
7. 序列化与写入在张量路径上不可分，这是从固定源码读出的结论，没有经过运行时计时验证。
