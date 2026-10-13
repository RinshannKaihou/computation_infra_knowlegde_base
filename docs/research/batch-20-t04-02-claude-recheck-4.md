# 第二十批 T04-02 第四次定向复核（作者第四轮修订后）

复核日期：2026-10-13（实际取证日）。正文 `updated_at` 与登记 `registered_at` 中的 `2026-10-14` 仍按交付标签处理，不作为取证日期。

**结论：T04-02 尚未通过。本轮复核 2 项（C01、C02）：CLOSED 1 项（C01），OPEN 1 项（C02）。B20-C01–C10 合计 CLOSED 9 项，OPEN 1 项（P1）。** P1 未全部关闭，不得声明审阅通过。

第四轮修订基本落盘：

- 三处登记注均已改，逐句对照原文无误；
- L85 证据列已补 §9.1.2、flock(2) NFS details、fcntl_locking(2) Record locking and NFS；
- "§8.4.1" 已改链到精确锚点；
- L113 重复粘贴已删。

剩余一处：L85 链接文字 "§8.4.2.1" 仍指向 `#section-8.4.2`。修订映射第四轮节称"§8.4.1/§8.4.2.1 锚点纠正"，与正文现状不符。

`make check` 通过（`PASS: 89 content entries; 401 sources.`）。它只校验结构与本地链接，不说明技术正确性或远程锚点。

审阅者角色独立于作者修订角色。审阅模型为 `claude-opus-5-5`，由用户本次明确要求。这不是既有的 `gpt-6.1-sol / xhigh` 批量审阅约定，也不改写该约定；推理等级等运行元数据未取得可核验记录，不补造。本轮只读核对，只写本报告，未改作者正文、来源记录、修订映射、登记或计划，未执行任何挂载、读写、`drop_caches` 或 benchmark。模型复核不构成硬件或现场验证。

## 输入（以 SHA-256 识别）

任务给出的 16 位哈希前缀与本地 `shasum -a 256` 结果逐一相符。

| 输入 | SHA-256（前 16 位，已核对） | 与前次比较 |
|---|---|---|
| [T04-02 正文](../../knowledge/04-data-storage/local-and-shared-storage.md)（121 行，reference / draft） | `e59c866921fef4d4` | 已改（前次 `353d2326…`） |
| [作者来源记录](batch-20-t04-02-sources.md) | `8d58ae110bfb0299` | 未改（与前三轮同哈希） |
| [修订映射](batch-20-review-fixes.md)（47 行，含第四轮修订节 L44–47） | `4e900101a4692d9b` | 已改（前次 `bc67e25a…`） |
| [前次复核报告](batch-20-t04-02-claude-recheck-3.md)（剩余关闭条件权威来源） | `a81657b0bc592835` | — |
| [任务计划](../../plans/full-coverage-backlog.yaml) | `f16309beadf5ae4f` | 同前四轮 |
| [来源登记](../../sources/registry.yaml)（401 项，按顶层 `- id:` 计数） | `84f2871bb76251a6` | 已改（前次 `f4d3ab7b…`） |

修订映射核对：

- 第四轮节（L44–47）列出的 C01、C02 各项，除 §8.4.2.1 锚点外均已落盘（见下）。
- 前次报告要求作者"按当前正文与登记的实际行号逐项给出位置，并建议附修改后文件的 SHA-256"。第四轮节没有行号；修改后哈希由任务输入提供。
- "改动位置索引"（L25–36）仍是旧行号，例如 C02 标为 L66、L77–84，实际在 L74、L85。该索引标题已声明"不冻结；以节名为准"，本轮按正文现行内容定位，不作为关闭依据。

## 一次源取证（审阅者独立获取）

全部用 `curl` 默认 TLS 校验只读获取，均返回 HTTP 200。HTML 去标签后按文字核对。原文只保存在系统临时目录，未入库。

| 来源 | SHA-256（原 HTML） | 与前次一致性 | 本轮核对点 |
|---|---|---|---|
| [admin-guide/ext4](https://www.kernel.org/doc/html/v6.16/admin-guide/ext4.html) | `2849c200…a1e84` | 同前次 | `auto_da_alloc`："ext4 will detect the replace-via-rename and replace-via-truncate patterns and force that any delayed allocation blocks are allocated such that at the next journal commit, in the default data=ordered mode, the data blocks of the new file are forced to disk before the rename() operation is committed"；"avoids the 'zero-length' problem" |
| [flock(2)](https://man7.org/linux/man-pages/man2/flock.2.html) | `f46b6eb4…6ba09` | 同前次 | NFS details："Since Linux 2.6.12, NFS clients support flock() locks by emulating them as fcntl(2) byte-range locks on the entire file. This means that fcntl(2) and flock() locks do interact with one another over NFS"；local_lock 见 nfs(5) |
| [fcntl_locking(2)](https://man7.org/linux/man-pages/man2/fcntl_locking.2.html) | `ea550a79…b6fb7fc9` | 同前次 | 传统锁 "associated with the process (unlike the open file description locks …)"；"If a process closes any file descriptor referring to a file, then all of the process's locks on that file are released"；"record locks are automatically released when the process terminates"；OFD 锁 "only automatically released on the last close of the open file description"；强制锁 "no longer supported at all in Linux 5.15 and above"；Record locking and NFS："Since Linux 3.12, if an NFSv4 client loses contact with the server, any I/O to the file by a process which 'thinks' it holds a lock will fail until that process closes and reopens the file"、"nfs.recover_lost_locks, can be set to 1 to obtain the pre-3.12 behavior"、nfsv4leasetime "The default value for this file is 90" |
| [RFC 8881](https://datatracker.ietf.org/doc/html/rfc8881) | `359026ae…61eda9` | **与前四轮均不同**（datatracker 动态渲染） | 锚点实测：`section-8.4.1`、`section-8.4.2`、`section-8.4.2.1`、`section-8.4.3`、`section-9`、`section-9.1.2` 均存在。§8.4.2 标题 "Server Failure and Recovery"，§8.4.2.1 标题 "State Reclaim"。§9.1.2："Share reservations are established by OPEN operations and by their nature are mandatory"；"Byte-range locks may be implemented by the server as either mandatory or advisory" |

取证限制：

1. 前几轮的取证限制继续适用：HTML 是渲染产物；man7.org 是第三方快照；去标签采用正则；未采集现场配置。
2. RFC 8881 页面哈希再次变化。本轮核对了锚点存在性，并按文字核对了 §9.1.2 和 §8.4.2/§8.4.2.1 的开头段落；未重读 §8.4.1、§8.4.3 正文，前几轮已按文字核对。
3. 本轮未重取 nfs(5)、client-identifier、sysctl vm 等页。它们支撑的是已 CLOSED 项，或本轮正文未改动的主张。
4. 锚点核对只证明页内存在该 `id`，不证明浏览器跳转行为；`make check` 不检查远程锚点。

## 逐项复核

### B20-C01 — P1 / **CLOSED**

证据：

- `src.kernel.admin-guide-ext4-v6.16` 的 notes（registry L4950）现为"auto_da_alloc 为默认 ordered 下 replace-via-rename 与 replace-via-truncate 启发式（防 zero-length），不能替代文件与目录 fsync"。这与原文 "detect the replace-via-rename and replace-via-truncate patterns" 一致，满足前次唯一的剩余关闭条件。
- 同一 notes 中的 ordered 措辞（前轮已改）无回退。
- 正文 L68–71（`data=`/`commit=`/`barrier`/`auto_da_alloc`）无回退。L71 写两种模式，与登记一致。

### B20-C02 — P1 / **OPEN**（只剩一个锚点）

已满足（对照前次剩余关闭条件逐条）：

1. **"§8.4.1" 改链**：L85 现为 `[RFC §8.4.1](…rfc8881#section-8.4.1)`，锚点实测存在。✔
2. **补 RFC §9.1.2**：L85 现有 `[§9.1.2](…#section-9.1.2)`，并注"share reservation mandatory/字节锁可 mandatory"。这与 §9.1.2 原文一致，支撑 L85 含义列"可为 mandatory，share reservation 本身 mandatory"。✔
3. **补 flock(2) NFS details**：L85 现有 `[flock(2) NFS details](…/flock.2.html)`，支撑"flock 在 NFS 客户端被模拟为整文件 fcntl 字节范围锁，两类锁互相作用"，与原文一致。✔
4. **补 fcntl_locking(2) Record locking and NFS**：L85 现有 `[fcntl_locking(2) Record locking and NFS](…/fcntl_locking.2.html)`。它支撑条件列"Linux ≥3.12 客户端丢锁后 I/O 失败直至关闭重开（`nfs.recover_lost_locks` 可恢复旧行为）""Linux 服务器租约默认 90 s"，与原文一致。✔
5. **flock-6.19 登记注**（registry L4972）现为"NFS 客户端自 2.6.12 起把 flock 模拟为整文件 fcntl 字节范围锁，两类锁在 NFS 上互相作用（以 nfs(5)/fcntl_locking 为准）"。原错误说法"NFS 上转换为 advisory 锁"已删除，与原文及正文 L85 一致。✔
6. **fcntl-locking-6.19 登记注**（registry L4994）现为"传统记录锁随进程，进程终止释放，关闭任一指向该文件的 fd 即释放该进程全部锁（OFD 锁仅最后关闭释放，不适用此条）"。释放语义已限定为传统锁，并补了 OFD 锁的释放条件，与原文及正文 L74 一致。前次追记的过度概括已消除。✔

未满足：

- **L85 链接文字 "§8.4.2.1" 仍指向 `https://datatracker.ietf.org/doc/html/rfc8881#section-8.4.2`**（父节 "Server Failure and Recovery"），而不是 `#section-8.4.2.1`（"State Reclaim"）。本轮实测 `id="section-8.4.2.1"` 存在。条件列"服务器重启后 grace 期 reclaim（§8.4.2.1）"引用的正是子节。修订映射 L47 称"§8.4.1/§8.4.2.1 锚点纠正"，只有前一半属实。这一点在前次报告中已列为未满足第 1 项，本轮仍未改。

剩余关闭条件：

- 正文 L85 证据列中，`[§8.4.2.1](https://datatracker.ietf.org/doc/html/rfc8881#section-8.4.2)` 改为 `[§8.4.2.1](https://datatracker.ietf.org/doc/html/rfc8881#section-8.4.2.1)`。只改这一处 URL 片段。

## 非阻断追记（不影响本轮计数）

- **前次非阻断项 L113 重复粘贴已处理。** 执行授权列现为"写 /proc/sys 需特权系本库推论（原文未写）；性能影响，仅授权窗口；本库不执行"，已无重复。
- **fcntl-locking 登记注省略版本限定。** registry L4994"NFS 丢锁后 I/O 失败直至关闭重开"未写原文的"Since Linux 3.12"和"NFSv4 client"。同句"nfs.recover_lost_locks 可恢复旧行为"已暗示存在旧行为，正文 L85 也写了"Linux ≥3.12"，所以这里只是省略，没有写错。建议顺手补"（Linux ≥3.12，NFSv4 客户端）"。
- **前次 C02 非阻断项仍未处理**：§1 表 L61 版本列仍只写"页日期 2026-02-08"，未补 fcntl_locking(2) 的页日期 2026-01-23（登记 L4989 已有）；该行"取证入口"也未列 fcntl_locking(2)、flock(2)。
- **前次 C10 非阻断项仍未处理**：registry L4884 nfs 登记 notes 仍是"内核 NFS 文档入口"，未与 revision 同步。
- **修订映射**：改动位置索引仍是旧行号；第四轮节未给实际行号，并把未完成的 §8.4.2.1 写成已纠正。下轮修订节应只列实际落盘的改动。
- `verification.status: source_checked`（正文 L30）仍与 OPEN 项并存。正文继续保持 `draft`（L6），复核通过后再按实际核对范围重写 notes。

## 逐条 acceptance 判定

| acceptance | 判定 | 剩余项 |
|---|---|---|
| 1 版本固定与路径/挂载/页缓存/读写/同步/提交/rename 保证与故障域 | **通过**（C01 本轮关闭） | — |
| 2 本地 vs NFS 的缓存/锁/可见性/恢复，不把 POSIX 相似等同持久性 | **未通过** | C02（L85 §8.4.2.1 锚点） |
| 3 负载选型表、必要配置、观察点、典型异常与来源边界 | **通过**（本轮正文无回退） | — |
| 4 可读/重启/校验/冷热基线方法，预期与实际分开 | **通过**（L113 重复已删） | — |

## 结论

**T04-02 未通过第四次定向复核。本轮 2 项中 CLOSED 1 项（C01），OPEN 1 项（C02）。B20-C01–C10 合计 CLOSED 9 项，OPEN 1 项（P1）。** 本轮未新增发现 ID，也无须按原 ID 追记新的事实错误。

剩余工作只有一处 URL 片段：正文 L85 中 "§8.4.2.1" 的链接由 `#section-8.4.2` 改为 `#section-8.4.2.1`。作者修订后须在修订映射中如实写明该处位置，并附修改后正文的 SHA-256，然后再做定向复核。P1 全部关闭前不得声明审阅通过。正文继续保持 `draft`。本复核不构成硬件、挂载或现场验证。
