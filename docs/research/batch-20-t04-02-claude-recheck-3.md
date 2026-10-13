# 第二十批 T04-02 第三次定向复核（作者第三轮修订后）

复核日期：2026-10-13（实际取证日）。正文 `updated_at` 与登记 `registered_at` 中的 `2026-10-14` 仍按交付标签处理，不作为取证日期。

**结论：T04-02 尚未通过。本轮复核 3 项（C01、C02、C10）：CLOSED 1 项（C10），OPEN 2 项（C01、C02）。B20-C01–C10 合计 CLOSED 8 项，OPEN 2 项（均为 P1）。** P1 未全部关闭，不得声明审阅通过。

本轮正文修订到位：本地锁三类释放语义已分列，逐句核对原文无误。剩余问题全部是"修订映射称已处理、实际未落盘或只做了一半"：

- C01：admin-guide 登记 notes 的 ordered 措辞已纠正，但 `auto_da_alloc` 仍只写 replace-via-rename。前次关闭条件点名要求补 replace-via-truncate。
- C02：
  - L85 证据列新加的 §8.4.1、§8.4.2.1 链接分别指向父节 `#section-8.4` 和 `#section-8.4.2`；
  - 前次点名的 §9.1.2、flock(2) "NFS details"、fcntl_locking(2) "Record locking and NFS" 仍未进入 L85 证据列；
  - flock 登记注未改；
  - fcntl-locking 登记注出现与上轮正文 L74 相同的过度概括（按 C02 追记）。

`make check` 通过（`PASS: 89 content entries; 401 sources.`）。它只校验结构与本地链接，不说明技术正确性。

审阅者角色独立于作者修订角色。审阅模型为 `claude-opus-5-5`，由用户本次明确要求。这不是既有的 `gpt-6.1-sol / xhigh` 批量审阅约定，也不改写该约定；推理等级等运行元数据未取得可核验记录，不补造。本轮只读核对，只写本报告，未改作者正文、来源记录、修订映射、登记或计划，未执行任何挂载、读写、`drop_caches` 或 benchmark。模型复核不构成硬件或现场验证。

## 输入（以 SHA-256 识别）

| 输入 | SHA-256 | 与前次比较 |
|---|---|---|
| [T04-02 正文](../../knowledge/04-data-storage/local-and-shared-storage.md)（121 行，reference / draft） | `353d2326e95220d478ba30965c3abdf1bf54c29f8e5d22786a441fc81c5b9442` | 已改 |
| [作者来源记录](batch-20-t04-02-sources.md)（21 行） | `8d58ae110bfb0299f1b7e6d48220c2ec6e5f82c9f631e8489d753daf3e1bc8e8` | **未改**（与前两轮同哈希） |
| [修订映射](batch-20-review-fixes.md)（42 行，含第三轮修订节与改动位置索引） | `bc67e25a30132d7a3da4b56738517ae141ec0c7e8d8ec1e1c7a72ebd96b00993` | 已改 |
| [前次复核报告](batch-20-t04-02-claude-recheck-2.md)（剩余关闭条件权威来源） | `40e73a0b0a0625da9640075c9c8a58b3feb7a84327376ad035a84bd98e977672` | — |
| [任务计划](../../plans/full-coverage-backlog.yaml)（T04-02 acceptance 4 条） | `f16309beadf5ae4f28d5fc7428a2348bea0cf08d155d57730a4d817cfcdd3e96` | 同前三轮 |
| [来源登记](../../sources/registry.yaml)（401 项） | `f4d3ab7b230067d428729277d24f47e6a5f7313263171306e17422c6172f6bdd` | 已改 |

修订映射核对：

- 第二轮节重复已去除，现存一份（L16–23）。
- 新增的"改动位置索引"（L25–36）**行号与当前正文不符**。例如：
  - 本地锁标为 L66，实际在 L74；
  - NFS 锁、提交与恢复标为 L77–84，实际在 L83–92；
  - C01 标为 L61–64，实际在 L68–73。

  本轮仍按正文现行内容逐项定位，不以映射行号作为关闭依据。
- 第三轮节称登记"三处文字同步真实落盘"。核对结果：nfs 子页、fcntl-6.19 索引备注、ordered 措辞三处确已落盘；但前次关闭条件中另有 admin-guide `auto_da_alloc` truncate、flock-6.19 notes 两处，第三轮节未提及，登记中也未处理。

## 一次源取证（审阅者独立获取）

全部用 `curl` 默认 TLS 校验只读获取，均返回 HTTP 200。HTML 用正则去标签后按文字核对。原文只保存在临时目录，未入库。

| 来源 | SHA-256（原 HTML） | 与前次一致性 | 本轮核对点 |
|---|---|---|---|
| [fcntl_locking(2)](https://man7.org/linux/man-pages/man2/fcntl_locking.2.html) | `ea550a79…b6fb7fc9` | 同前次 | "record locks described above are associated with the process (unlike the open file description locks …)"；"If a process closes any file descriptor referring to a file, then all of the process's locks on that file are released"；"Record locks are automatically released when the process terminates"；OFD 锁 "available since Linux 3.15"、"associated with the open file description … much like locks acquired with flock(2)"、"only automatically released on the last close of the open file description, instead of being released on any close of the file"；"Open file description locks are advisory byte-range locks" |
| [flock(2)](https://man7.org/linux/man-pages/man2/flock.2.html) | `f46b6eb4…6ba09` | 同前次 | "the lock is released either by an explicit LOCK_UN operation on any of these duplicate file descriptors, or when all such file descriptors have been closed"；"Since Linux 2.6.12, NFS clients support flock() locks by emulating them as fcntl(2) byte-range locks on the entire file" |
| [fcntl(2)](https://man7.org/linux/man-pages/man2/fcntl.2.html) | `33c2f867…52b5a` | 同前次 | 仍只是命令索引页 |
| [admin-guide/ext4](https://www.kernel.org/doc/html/v6.16/admin-guide/ext4.html) | `2849c200…a1e84` | 同前次 | `auto_da_alloc`："ext4 will detect the replace-via-rename **and replace-via-truncate** patterns" |
| [RFC 8881](https://datatracker.ietf.org/doc/html/rfc8881) | `6e7002c0…69189` | **与前三轮均不同**（datatracker 动态渲染） | 页内锚点实测：`id="section-8.4.1"`、`id="section-8.4.2.1"`、`id="section-8.4.3"`、`id="section-9"`、`id="section-9.1.2"` 均存在 |

取证限制：

1. 前几轮的取证限制继续适用：HTML 是渲染产物；man7.org 是第三方快照；去标签使用正则；未采集现场配置。
2. RFC 8881 页面哈希又一次变化。本轮只核对锚点是否存在，不重读 §8.4/§9 正文；前次已按文字核对过这些段落。
3. 本轮未重取 nfs(5)、client-identifier、sysctl vm、nfs41-server、knfsd-stats。它们支撑的是已 CLOSED 项，或本轮正文未改动的主张。

## 逐项复核

### B20-C01 — P1 / **OPEN**（只剩一处登记短语）

已满足：

- **ordered 措辞**：`src.kernel.admin-guide-ext4-v6.16` 的 notes（registry L4950）现为"data=ordered 默认（数据直接写主文件系统、元数据随后提交入日志；数据入日志的是 journal 模式）"，与原文 "All data are forced directly out to the main file system prior to its metadata being committed to the journal" 一致，与正文 L68 一致。前次的歧义原句已消除。
- 正文 L68–71 无回退。

未满足：

- **同一 notes 仍写"auto_da_alloc 为默认 ordered 下 replace-via-rename 启发式"**（registry L4950），没有 replace-via-truncate。原文是 "detect the replace-via-rename and replace-via-truncate patterns"，正文 L71 也已写两种模式。前次关闭条件明文要求"同时补上 replace-via-truncate"。第三轮修订节只提到 ordered 措辞，未处理此项。

剩余关闭条件：

- registry L4950 notes 中 `auto_da_alloc` 一句改为"replace-via-rename 与 replace-via-truncate 启发式"。

### B20-C02 — P1 / **OPEN**

已满足：

- **本地锁三类分列**（正文 L74），逐句核对 fcntl_locking(2) 与 flock(2) 原文：
  - 传统锁"随进程（非 OFD）：进程终止释放，关闭任一指向该文件的 fd 即释放该进程全部锁"，与原文一致，限定正确；
  - OFD 锁"仅最后一次关闭该 OFD 时自动释放"，与原文 "only automatically released on the last close of the open file description" 一致；
  - flock 锁"显式 LOCK_UN 或全部重复 fd 关闭时释放"，与 flock(2) 原文一致；
  - 已不再把 flock 称作"记录锁"；条件列写"三类释放语义不可互换"。

  前次追记的过度概括在正文中已消除。另有一处非阻断：本行"均为 advisory"只列传统锁与 flock，未提 OFD 锁。原文写 OFD 锁同样是 advisory，所以这里只是省略，没有写错。
- **fcntl(2) 登记注**（registry L4983）已写明"man-pages 6.19 中 fcntl(2) 仅为命令索引……锁语义正文见 fcntl_locking(2)……不作语义证据"，与取证一致。正文 L74"fcntl(2) 本页仅索引（见登记注）"的引用现已落地。
- **L85 证据列**已加入 RFC §8.4.1、§8.4.2.1、§8.4.3、§9 链接文字。

未满足：

1. **L85 新增 RFC 链接中，两处的锚点与文字不符。** 链接文字 "§8.4.1" 指向 `#section-8.4`，"§8.4.2.1" 指向 `#section-8.4.2`。本轮实测页内 `id="section-8.4.1"` 与 `id="section-8.4.2.1"` 均存在，前次关闭条件也已给出精确 URL。修订映射 L28 称"RFC §8.4.1/§8.4.2.1/§8.4.3/§9/§18 锚点"，与正文现状不符。
2. **前次点名的其余支撑页仍不在 L85 证据列。** L85 含义列与条件列中的下列主张，本行仍无出处：
   - "v4 字节范围锁……可为 mandatory，share reservation 本身 mandatory"——依据是 RFC §9.1.2，本行只链到 §9 总节；
   - "flock 在 NFS 客户端被模拟为整文件 fcntl 字节范围锁"——依据是 flock(2) "NFS details"，本行未链 flock(2)；
   - "Linux ≥3.12 客户端丢锁后 I/O 失败直至关闭重开（`nfs.recover_lost_locks`）""Linux 服务器租约默认 90 s"——依据是 fcntl_locking(2) "Record locking and NFS"，本行未链 fcntl_locking(2)。前次关闭条件点名要求这一锚点。
3. **flock-6.19 登记注未改**（registry L4972）。仍写"NFS 上转换为 advisory 锁（以 nfs(5) 为准）"，与 flock(2) 原文及正文 L85 的"模拟为整文件 fcntl 字节范围锁"不一致。前次关闭条件明文要求更新，第三轮修订节未提及。
4. **新事实问题（按 C02 追记）：fcntl-locking-6.19 登记注有与上轮正文 L74 相同的过度概括。** registry L4994 写"进程终止释放记录锁；关闭任一指向该文件的 fd 即释放该进程全部锁"，没有"传统（进程关联）记录锁"的限定。fcntl_locking(2) 原文把这一释放语义限定在传统记录锁，并说明 OFD 锁不同；而该页本身就定义了 OFD 锁。正文已改正，登记注仍是旧说法，二者不一致。

剩余关闭条件：

- L85 证据列：
  - "§8.4.1" 改链 `https://datatracker.ietf.org/doc/html/rfc8881#section-8.4.1`；"§8.4.2.1" 改链 `…#section-8.4.2.1`；
  - 补 [RFC §9.1.2](https://datatracker.ietf.org/doc/html/rfc8881#section-9.1.2)、[flock(2)](https://man7.org/linux/man-pages/man2/flock.2.html)（NFS details）、[fcntl_locking(2)](https://man7.org/linux/man-pages/man2/fcntl_locking.2.html)（Record locking and NFS）。
- registry L4972 flock-6.19 notes 改为"NFS 客户端（Linux ≥2.6.12）把 flock 模拟为整文件 fcntl 字节范围锁，两类锁在 NFS 上互相作用"。
- registry L4994 fcntl-locking-6.19 notes 中，释放语义限定为"传统（进程关联）记录锁"，并补"OFD 锁在最后一次关闭 open file description 时释放"。

### B20-C10 — P3 / **CLOSED**

证据：

- **nfs 登记实际子页**：`src.kernel.docs-nfs-v6.16` 的 revision（registry L4879）现为"正文实际使用 nfs41-server（实现状态表）、knfsd-stats（pool_stats）、client-identifier（租约锁）；exporting/pnfs/localio/reexport 仅可达性核对，未用于主张"。这与前次关闭条件逐项一致，也与正文 L58、L91、L98 的实际引用一致。
- **作者来源记录 L17**：文件未改（哈希同前），但现有文字已与新登记一致。L17 列出了正文实际使用的三个子页，并写明"未使用 exporting/pnfs/localio/reexport 具体内容"。前次要求改写，是因为它与旧登记 revision 冲突（旧 revision 写"实开 index/exporting/pnfs/localio/reexport"）。登记改正后冲突已消失，因此不再构成关闭障碍。
- **fcntl(2) 登记注**：已写明索引定位（见 C02"已满足"）。
- **evidence_refs**：正文 L31–45 共 14 项，与 `source_refs` L9–22 逐项一致，且均为已登记 ID（`make check` 通过）。

非阻断残留：

- registry L4884 的 notes 仍是"内核 NFS 文档入口"。revision 已足以说明实际范围，notes 可顺手同步。
- 作者来源记录 L17 的"（索引登记范围保留）"与登记"仅可达性核对，未用于主张"的措辞可以统一。

## 非阻断追记（不影响本轮计数）

- **正文 L113 执行授权列有重复粘贴。**"写 /proc/sys 需特权系本库推论（原文未写）；性能影响，"连续出现两次。C05 已 CLOSED，不重开，建议同轮删除重复。
- **前次 C05 残留已处理**：正文 L116 现为"需特权系本库推论（原文未写）"，与 L113 一致。
- **前次 C02 非阻断项未处理**：§1 表 L61 版本列仍只写"页日期 2026-02-08"，未补 fcntl_locking(2) 的页日期 2026-01-23；该行"取证入口"也未列 fcntl_locking(2)。
- **修订映射**：改动位置索引的行号需按当前正文重写（见"输入"节）。第三轮节应如实列出本轮未处理的关闭条件，不应只列已处理的。
- `verification.status: source_checked` 仍与 OPEN 项并存。正文继续保持 `draft`，复核通过后再按实际核对范围重写 notes。

## 逐条 acceptance 判定

| acceptance | 判定 | 剩余项 |
|---|---|---|
| 1 版本固定与路径/挂载/页缓存/读写/同步/提交/rename 保证与故障域 | 正文满足；**未通过** | C01（admin-guide 登记 notes 缺 replace-via-truncate） |
| 2 本地 vs NFS 的缓存/锁/可见性/恢复，不把 POSIX 相似等同持久性 | **未通过** | C02（L85 两处锚点错位、三类支撑页未链；flock、fcntl-locking 登记注） |
| 3 负载选型表、必要配置、观察点、典型异常与来源边界 | **通过**（本轮正文无回退） | — |
| 4 可读/重启/校验/冷热基线方法，预期与实际分开 | **通过** | L113 重复粘贴为非阻断 |

## 结论

**T04-02 未通过第三次定向复核。本轮 3 项中 CLOSED 1 项（C10），OPEN 2 项（C01、C02）。B20-C01–C10 合计 CLOSED 8 项，OPEN 2 项（均为 P1）。** 本轮未新增发现 ID。fcntl-locking 登记注的过度概括按 C02 追记。

剩余工作都是文字级修改，共五处：

- 登记 notes 三处：admin-guide 一个短语，flock、fcntl-locking 各一句；
- 正文 L85 证据列：两个锚点改链，另补三个支撑页链接。

作者修订后，须按当前正文与登记的实际行号逐项给出位置，并确认改动已落盘（建议附修改后文件的 SHA-256），然后再做定向复核。P1 全部关闭前不得声明审阅通过。正文继续保持 `draft`。本复核不构成硬件、挂载或现场验证。
