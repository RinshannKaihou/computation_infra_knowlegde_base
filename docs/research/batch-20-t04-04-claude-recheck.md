# 第二十批 T04-04 定向复核（作者首轮修订后）

复核日期：2026-10-13（实际取证日）。审阅模型 `claude-opus-5-5`，由用户本次明确要求。这不是既有的 `gpt-6.1-sol / xhigh` 批量审阅约定，也不改写该约定；推理等级等运行元数据没有可核验记录，不补造。审阅者角色独立于作者修订角色。

**结论：T04-04 定向复核未通过。B20-C22–C31 共 10 项：CLOSED 1（C28），OPEN 9（C22、C23、C24、C25、C26、C27、C29、C30、C31）。** 9 项中实质性缺口 3 项：C24 有新取证的事实错误，C22 的登记仍与正文矛盾，C27 缺三态判定。其余 6 项只剩文档层面的残缺（就近引用、标注、节号、记录字段）。不新增发现 ID。C24 下追记的 Xet 分支问题属于原发现"hub 传输行与固定实现不符"的范围，按原 ID 记录。

本轮只做只读核对：未改作者正文、来源记录、修订映射、登记或计划；未下载模型，未上传或发布对象，未执行读写、中断或计时试验。模型审阅不构成硬件或现场验证。

## 输入（以 SHA-256 识别）

| 输入 | SHA-256 |
|---|---|
| [T04-04 正文](../../knowledge/04-data-storage/artifact-transfer-and-publication.md)（96 行，procedure / draft） | `c706de484bdf45608ca37f916e4296511e8ef1c708282c487caa60e799436be5` |
| [作者来源记录](batch-20-t04-04-sources.md)（17 行） | `925a33209fad694ca43424a57985055de4652164d49e09724dd0aa944a2f0247` |
| [修订映射](batch-20-review-fixes.md)（T04-04 节 L96–108） | `d3da44115f8447846c90430fe04c443a2c67a51681050745b933531437333d8b` |
| [初审报告](batch-20-t04-04-claude-review.md)（关闭条件权威来源） | `67f6ac99034bc75d17e49e8aba3fa9d7c08771582e4e4c8897b6fcafe8309cac` |
| [任务计划](../../plans/full-coverage-backlog.yaml)（T04-04 acceptance 4 条） | `f16309beadf5ae4f28d5fc7428a2348bea0cf08d155d57730a4d817cfcdd3e96` |
| [来源登记](../../sources/registry.yaml)（409 项；T04-04 两项 L5070–5097） | `287237cf80720e065f95b8dac45b3571ddc072825e3fc937aee00be49f55a2c1` |

`make check`：`PASS: 91 content entries; 409 sources.` 只校验结构与本地链接。正文四个主文链接与 07 索引链接的目标文件都存在。

## 一次源重取（审阅者独立获取）

用 `curl` 默认 TLS 只读获取（raw.githubusercontent.com 按 commit/tag 取原文），原文只存在 `/tmp/b20rc/`，未入库。

| 来源 | SHA-256 | 与初审比对 / 本轮核对点 |
|---|---|---|
| hub `file_download.py`@d5dff4ef（1803 行） | `a973d198…bfe4ef` | 与初审逐字节一致。正文 §2/§4 与登记引用的行号逐一核对无误：L232–234、L406–407、L444–445、L485、L500–517、L522、L942–947、L1122、L1160–1163、L1678、L1684–1693、L1735、L1776。全文 `hashlib`、`fsync` 均 0 次命中。**新增核对**：L1708–1732 的分支条件是 `xet_file_data is not None and is_xet_available()` 走 `xet_get`，否则才走 `http_get`；`xet_get` 的调用不传 `resume_size`，也不进入 L500–517 的重试；L600–603 把 `hash=xet_file_data.file_hash` 交给外部 `hf_xet.download_files`。→ C24 |
| hub `setup.py`@d5dff4ef | （本轮新取） | L17 的 `install_requires` 含 `hf-xet>=1.1.2,<2.0.0`，条件为 platform_machine 是 x86_64、amd64、arm64 或 aarch64。也就是说，在主流平台上 hf_xet 随默认安装进入环境。→ C24 |
| hub `_snapshot_download.py`@d5dff4ef | `e9747acf…b3d2e` | 与初审一致。L165、L264–267、L283、L305 核对无误。 |
| hub `tests/test_file_download.py`@d5dff4ef | `f19f048c…f68bc` | 与初审一致。L514、L536、L798–804 核对无误。**追记**：L806 起的 `test_do_not_resume_on_force_download`，其 L812 `self.file_path.read_text() == "content"` 同样是裸比较，缺 `assert`。→ C28（不阻断） |
| safetensors `tensor.rs`@fa27fa83 | `f94ad16f…80ea0` | 与初审一致。L10 `MAX_HEADER_SIZE`、L18–46 错误枚举、L387–389 `MetadataIncompleteBuffer` 核对无误。 |
| safetensors README@v0.7.0 | `e430910c…5e1696e1` | 与初审一致。L83 `data_offsets` "relative to the beginning of the byte buffer"；L85 `__metadata__`；L89 重复键；L94 NaN/±Inf；L101 不得有空洞；L174 100MB。 |
| hub 下载指南 v0.33.0 版页 | `f956ec22…d1ec5`（HTML 动态渲染，与初审字节不同，按文字核对） | 去标签后："You are viewing" 1 次，"full-length hash" 1 次，"entire repository at a given revision" 1 次，`dry_run` 0 次，resume 0 次。与正文 L45、登记 L5075 一致。 |
| safetensors 新组织地址 `github.com/safetensors/safetensors/tree/v0.7.0` | — | HTTP 200（登记 L5086 新 URL 可达）。 |

取证限制：

- GitHub REST API 本轮返回 403（未认证限流），所以 tag→commit 的解析没有经 API 重做。本轮按 commit SHA 直接取原文，取到的字节与初审一致，可间接确认。
- hf_xet（外部 Rust 包）的续传、重试与哈希校验实现未核对。
- 未克隆仓库，未跑测试。
- fsync(2)、rename(2)、Ceph 页面本轮未重取，只核对了其登记 ID 存在（L322、L4951、L4995）。

**初审自我更正**：初审 C28 把 `_check_disk_space`（L784–801）列为"空间不足"失败点。实际上 L799 是 `warnings.warn`，只发警告，不是失败点。作者在正文 L81 和登记 L5083 的纠正正确。初审对 Xet 路径"只看到调用点"，没有指出它是默认安装下的主路径，本轮补核（见 C24）。

## 逐项复核

### B20-C22 — P1 / **OPEN**（正文已改，登记未同步）

- 已满足：正文 L44 把 `data_offsets` 改为"单文件内张量区间，只用于格式检查"，引文与 README L83 一致。跨文件的分片索引记为 unknown，或改由本库设计约定另行声明。L41 新增"集合成员"字段，覆盖张量与非张量文件，每个文件记长度和 SHA-256，并标为"本库清单要求"。
- 未满足："同步修订登记 L5097"。登记 `src.hf.safetensors-v0.7.0` 的 `notes`（L5097）原样保留"制品分片清单以 header 的 data_offsets 为准"和"格式自带校验和未在 README 见到（unknown）"，与同条目 `revision`（L5089，"无校验和字段"）和正文 L44/L47 直接矛盾。修订映射 L99 与 C31 行没有提到 L5097。
- 剩余关闭条件：改写登记 L5097 notes，删除 data_offsets 作为分片清单依据的表述，校验和表述与 L5089 统一。

### B20-C23 — P1 / **OPEN**（实质已改，只差记录位置）

- 已满足：正文 L45 改用 v0.33.0 版页，本轮核对横幅、full-length hash 和 snapshot_download 原文无误；登记 L5075 已同步；正文 L47 写明不追 latest（2.2.0/0.8.0），也不外推到 1.x/2.x。
- 未满足：关闭条件要求在**来源记录**中说明为何选 v0.33.0 与 safetensors 0.7.0。来源记录（L3–17）没有这项说明。正文 L47 只写了"选 … 为固定样板"，这是结论，不是理由。
- 剩余关闭条件：在来源记录补一句选版依据，例如目标环境锁定的版本，或"作者选样，与目标环境的对应关系 unknown"，并与正文 L47 一致。

### B20-C24 — P1 / **OPEN**（原关闭条件基本满足；新取证发现事实错误，按原 ID 追记）

- 已满足：§2"传输"行和 §4 按行号写明续传（Range、默认续传、5 次重试）、只按长度判定、无 hashlib；版本字段记"解析出的 40 位 commit＋请求的 revision"（L43）；读回要求本地重算 SHA-256，LFS ETag 只作远端声称值（L70）；超过 50 000 文件的跨 commit 窗口已写入 L43 和 L68；unknown 清单已删除"hub 续传"。本轮逐行核对了以上行号，全部无误。
- **追记的新事实错误**：正文 L35"hub 下载完成判据只有长度（无内容哈希）"、L55"默认总是续传 … 网络错误最多续传 5 次；完成判据只有长度"、L79"超过 5 次重试"都写成无条件成立，但它们只适用于 `http_get` 分支。在 d5dff4ef 上：
  - `setup.py` L17 让 x86_64/amd64/arm64/aarch64 平台默认安装 hf-xet；
  - `file_download.py` L1708 规定，只要仓库文件带 Xet 元数据并且 hf_xet 可用，就走 `xet_get`。该调用不传 `resume_size`，不经过 L500–517 的重试，也不经过 L483–485/L522 的长度检查；
  - L600–603 把 `file_hash` 交给 hf_xet，hf_xet 是否据此校验内容未核对，为 unknown。

  因此在默认安装、Xet 存储的仓库上，正文对续传、重试和"无内容哈希"的断言没有依据。来源记录 L9、L17 已把 Xet 列为 unknown，但正文全文没有提到 Xet，读者无从得知这个限定。
- 附带：§2"传输"行 RGW 栏写"同左＋RGW multipart"。向 RGW 发布是上传（multipart），hub 下载的续传语义不适用于上传方向，"同左"会造成误读。
- 剩余关闭条件：
  1. L35、L55、L60、L79–80 限定为"HTTP 分支（无 Xet 元数据，或 hf_xet 不可用）"，锚点 L1708–1732。
  2. 写明默认安装下 Xet 分支的存在条件（setup.py L17、file_download.py L1708）。该分支的续传、重试和内容校验记为 unknown，"下载后本地重算 SHA-256"仍作为两个分支共同的读回要求。
  3. RGW 栏"传输"改为上传方向的表述。

### B20-C25 — P1 / **OPEN**（实质已改，缺就近引用）

- 已满足：§2 拆成本地、NFS、RGW 三栏（L51）；NFS 栏引入 UNSTABLE/COMMIT 与 verifier、可见性≠持久性、`hard`、导出 `sync`、close/fsync 查错、rename 后复核，链接到 [local-and-shared-storage](../../knowledge/04-data-storage/local-and-shared-storage.md)，与 T04-02 L86/L88/L92/L100 的原文一致；L53 写明"写临时名 → fsync(文件) → rename → fsync(目录)"；原"T04-03 UNSTABLE/COMMIT"的错误归属已删除；L57 写明 hub 落地边界（move、无 fsync、跨卷时为复制），与 L1678/L1735/L1776 一致。
- 未满足：关闭条件要求次序"引用 fsync(2)/rename(2) 登记"。L53 的次序和 L56 的"以 rename(2) 为准"都没有就近链接，fsync-6.19 与 rename-6.19 只出现在 frontmatter `source_refs`。次要问题：NFS 栏写"见本地与共享存储 §3"，但 `hard`＋导出 `sync`＋rename 后复核出自 T04-02 §4（L100，§4 起于 L94）。
- 剩余关闭条件：在 L53、L56 就近链接 fsync(2)、rename(2) 的登记页；NFS 栏改为"§3、§4"。

### B20-C26 — P1 / **OPEN**（实质已改，缺"设计约定 / 上游保证"标注）

- 已满足：L56 两个分支都写出集合级提交点（先写全部成员，最后发布清单或指针；对象侧最后 PUT 清单对象）和读者协议（先读清单，哈希不符即失败）；目录 rename 条件写明同文件系统、目标不存在或为空目录；对象侧没有多对象原子性，记为 unknown。
- 未满足："设计约定与上游保证分开标注"。L56 没有把"集合级提交点＋读者协议"标为本库设计约定，读者无法区分它和 rename(2)/Complete 的上游保证。修订映射 L103 自称"设计/上游分开标"，与正文不符。
- 剩余关闭条件：在 L56 把集合级提交点与读者协议明确标为"本库设计约定"，单文件 rename、单对象 Complete 标为上游语义（附来源）。

### B20-C27 — P2 / **OPEN**

- 已满足：版本字段按 T04-03 L84 的身份分支改写（L43、L60：Enabled 且可获得 versionId / 其他情况用 key＋SHA-256），与 T04-03 L84 原文一致；"版本号未推进"已删除。
- 未满足："旧版本、混合版本的判定按三态分别写，并链接 T04-03 §5"。L68 只写"用 revision 解析 commit/versionId＋清单判定；判定方法见 T04-03 §5"，既没有分 Enabled / Suspended / 从未设置三态（T04-03 L51），"T04-03 §5"也是纯文本，没有链接。
- 剩余关闭条件：L68 按三态分别写旧版本和混合版本的判定（Enabled 时按 versionId＋清单；Suspended 与从未设置时按 key＋SHA-256＋清单，versionId 不可用），并链接 [对象与并行存储](../../knowledge/04-data-storage/object-and-parallel-storage.md) §5。

### B20-C28 — P1 / **CLOSED**

- §4（L74–86）按"解析 revision → 下载/续传 → 长度检查 → 落地 move → 本库 SHA-256 → 格式检查 → 提交/读回"列出上游锚点、计时起止和失败信号；计时值一律未执行（L86）；注明 L804 缺 `assert`，只作行为样例；safetensors 读写测试记为 unknown，并写明检索范围；磁盘空间不足改为"警告，不是失败点"（本轮核对 L799 为 `warnings.warn`，纠正正确，初审有误）。锚点逐行核对无误。
- 不阻断追记：L812（force_download 用例）同样缺 `assert`，建议 L86 一并注明。"force 不续传"这一主张另有实现 L1684–1693 支持，结论不受影响。下载/续传行只适用于 HTTP 分支，由 C24 的剩余关闭条件一并处理，不在此重复计为 OPEN。

### B20-C29 — P2 / **OPEN**（格式门与正确性门已满足；清理残留未列全）

- 已满足：格式门（L71）列出首字符 `{`、≤100MB、offset 合法、无空洞、键不重复（依赖解析器），并写明通过不代表数值有效（NaN/±Inf），锚点与 tensor.rs、README 一致；正确性门（L72）给出最低形式（固定输入与参考输出比对、容差由负责任务定），归属 T07-01，缺失部分记为 unknown；对象侧写明按 List uploads 找残留再 Abort（L67）。
- 未满足：初审证据点名的文件侧"临时名与锁文件"没有列出。L66 只列了 hub 的 `.incomplete`，本库自身 §2 协议中断后留下的临时名文件，以及 hub `WeakFileLock`（L1160）的锁文件，都没有写发现方法和清理操作。L71 的"键不重复""NaN"出自 README L89/L94，该行只链接了 tensor.rs。
- 剩余关闭条件：L66 补上本库临时名文件和 hub 锁文件两类残留的发现方法与清理操作（未执行就写"方法设计"；锁文件清理条件不明的记 unknown）；L71 补 README 锚点。

### B20-C30 — P2 / **OPEN**（链接已加，未精确到节）

- 已满足：L90 加入四个主文的相对链接，目标均存在；推理加载改为"T07-01（batch 26，未交付）"，暂链 07 索引（L91）。
- 未满足："精确到节"。L90 的 durability/integrity 链接只到文件，括号里写的是主题，没有节号；正文 L53、L67、L68 的"T04-03 §2/§5"仍是纯文本，没有链接。
- 剩余关闭条件：durability/integrity 链接标注所指的节；L53、L67、L68 的 T04-03 引用改为带节号的 Markdown 链接。

### B20-C31 — P3 / **OPEN**

- 已满足：`source_refs` 删除 dcp 与 mindio；safetensors 登记 URL 迁到 `safetensors/safetensors`（L5086，本轮核对 200），并注明 301；正文 L47 按格式定义改写为"格式本身没有校验和字段"；来源记录补了取证日期（L3）和行号（L9–10）。
- 未满足：
  1. `verification.status` 仍为 `source_checked`（L26），关闭条件要求定向复核通过后再升级。
  2. 来源记录没有页面和文件的 SHA-256。L13 只写"见复核报告一次源表"，"一核对一致处以复核记录为准"语义不清，也没有给出作者自己的哈希或比对结论。
  3. fsync、rename、Ceph 三项留在 `source_refs`，但正文没有就近引用（与 C25 重叠）。
  4. 登记 L5097 的旧校验和表述与 L47 改写矛盾（与 C22 重叠）。
- 剩余关闭条件：status 回退到复核通过前的状态，或在通过后再升级；来源记录写出作者实开的 SHA-256（至少 file_download、_snapshot、test、README、tensor.rs、v0.33.0 指南页），或明确写"作者未自算，采用复核报告表"并说明比对方式；三项登记补就近引用，或从 `source_refs` 删除；修订 L5097。

## 对照 acceptance

| acceptance | 判定 | 未关闭 |
|---|---|---|
| 1 清单字段；下载成功≠版本一致/ready | 未满足：正文字段已齐；但 hub 断言没有限定在 HTTP 分支，登记 L5097 仍与正文矛盾 | C24（P1）、C22（P1）、C23（P1，记录层） |
| 2 本地/NFS/RGW 提交条件逐实现核对 | 基本满足，只剩引用和标注层残缺 | C25、C26（P1，残留）、C27（P2） |
| 3 中断/部分/旧/混合/重试/清理；三类门槛 | 门槛已分开；清理残留和三态判定未齐 | C29、C27（P2） |
| 4 阶段计时与失败点；链接 durability/integrity/推理加载 | 阶段表满足；链接未精确到节 | C30（P2） |

## 结论

**定向复核未通过：CLOSED 1 / OPEN 9。** 主要剩余工作：

1. **C24（实质）**：hub 续传、重试和长度判据限定在 HTTP 分支，并补上默认安装下 Xet 分支的条件和 unknown。
2. **C22、C31（登记）**：修订登记 L5097。
3. **C27（实质）**：按三态写出旧版本和混合版本的判定，并加链接。
4. **C23、C25、C26、C29、C30、C31（文档残缺）**：补选版理由、就近引用、"设计约定 / 上游保证"标注、本库临时名和锁文件残留、节号链接，补来源记录 SHA-256，回退 verification 状态。

P1、P2 全部关闭前不得声明审阅通过。修订后需要按 ID 再做定向复核。本报告只覆盖编辑与来源层面，不构成硬件、部署或现场验证。
