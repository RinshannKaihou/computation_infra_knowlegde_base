# 第十二批来源记录：Checkpoint 完整性与校验证据（R2-15）

**2026-10-08 修订注记：** Codex `gpt-6.1-sol / xhigh` 按 B12-C03/C06 修正本记录并完成[定向复核](batch-10-11-12-codex-recheck.md)。下述原研究者、首次获取方式与当时任务状态为历史；修订补读和保留的未知条件见本记录及复核报告。

研究日期：2026-10-08。研究者：探索子代理（非 astra）。
目标正文：`knowledge/04-data-storage/` 下「Checkpoint 完整性与校验证据」（concept）。
范围：A) PyTorch DCP 2.6（tag v2.6.0，registry id `src.pytorch.dcp-2.6`）应用层校验；B) MindIO ACP（MindCluster commit `44385c13d7b1d87def35f1604e8be4d16de6ca4e`，registry id `src.ascend.mindio-acp-v26.1.1`）register_checker；C) Ceph scrub/deep-scrub/repair（候选新来源，未登记）；D) Python zipfile CRC 行为。时间盒约 30 分钟，未覆盖项见末节。

## 主张—证据表（A：PyTorch DCP 2.6）

| 主张 | 来源与定位 | 版本/环境 | 证据性质 | 反例/未知 |
|---|---|---|---|---|
| FileSystemWriter 默认 single_file_per_rank=True、thread_count=1，一个本地计划的多个 write item 合为同一桶 .distcp；多线程按大小/类型分桶，single_file_per_rank=False 才按 item 建文件，另有 pickle .metadata | [固定 filesystem.py](https://github.com/pytorch/pytorch/blob/1eba9b3aa3c43f86f4a2c807ac8e12c4a7767340/torch/distributed/checkpoint/filesystem.py)：L225–246、L447–463、L507–534、L574–595 | PyTorch v2.6.0 固定 commit | 源码参数与实现 | B12-C03：L439–440 的简略 docstring 不能代表默认文件布局；文件数量以配置/保存计划/metadata 为准 |
| **`.metadata` 是 pickle 序列化的 `Metadata` 对象，不是 JSON**；写时先写 `.metadata.tmp` 再 rename（tmp→正式）实现原子替换 | filesystem.py L582-584（`pickle.dump(metadata, metadata_file)`）、L595（rename）；读取侧 L677-686 `pickle.load`，无任何验证 | 同上 | 源码原文 | 任务预设"JSON？"被源码否定 |
| `Metadata` 字段仅 `state_dict_metadata / planner_data / storage_data / storage_meta`；`storage_data` 为 `MetadataIndex → _StorageInfo(relative_path, offset, length)`；`StorageMeta` 仅 `checkpoint_id/save_id/load_id`；所查 FileSystem 的这些声明字段未见独立内容摘要，不能据此概括 planner_data 扩展或其他后端 | `torch/distributed/checkpoint/metadata.py` L136-147（Metadata）、L129-133（StorageMeta）；filesystem.py L66-72（_StorageInfo）、L574-578（storage_md 组装） | 同上 | 源码原文 | — |
| 数据写入路径：tensor 项经 `torch.save(data, stream)` 嵌入 .distcp；字节项（BYTE_IO）`stream.write(data.getbuffer())` 裸写；写完按 `sync_files` 做 fsync；`WriteResult` 只记 offset/length | filesystem.py L249-270（_write_item，L259 裸写、L263 torch.save）、L266-269（WriteResult）、L331-335（fsync） | 同上 | 源码原文 | — |
| 读取路径按 metadata 的 offset/length 定位记录；tensor 项经 torch.load 与 narrow_tensor_by_index 后检查形状；read_metadata 直接 pickle.load | filesystem.py L624–625、L647、L655–659、L666–668、L677–686 | 同上 | 源码原文 | 形状断言不证明内容完整；解析可检出某些损坏，保持可解析性与形状的损坏可能逃过，不能断言所有同长度损坏均无感 |
| 此前对 filesystem.py 与 DCP 28 个 .py 文件的校验和关键词扫描未命中；所查 FileSystemWriter/Reader 的 storage_data 与读写实现未见独立内容摘要 | 原研究 gh api 扫描记录（见读取清单）；固定 filesystem.py 与 metadata.py | 同上 | 关键词扫描与所查实现证据 | 扫描不是所有后端/扩展路径无校验的证明；本次修订限定到实际读取范围，未重新执行全包扫描 |
| 对照：torch.save 的 zip 容器**写时默认对每条 record 计算并写入 CRC32**（`_compute_crc32: bool = True`），可经 `set_crc32_options(False)` 关闭；官方注释：关闭后"unzipping of the torch.save output [may] fail or warn due to corrupted CRC32. **However torch.load will be able to load the file.**" | `torch/serialization.py` L184（全局默认）、L187-193（get_crc32_options docstring）、L196-209（set_crc32_options docstring 原文）、L778/781/797（PyTorchFileWriter 传入该标志） | 同上 | 源码+docstring 原文 | 表明 torch 自研 reader 不依赖 CRC32；C++ PyTorchFileReader 是否在任何路径验证 CRC32 未逐行核对（见未解决项） |

## 主张—证据表（B：MindIO ACP，MindCluster 固定 commit）

| 主张 | 来源与定位 | 版本/环境 | 证据性质 | 反例/未知 |
|---|---|---|---|---|
| `register_checker(callback, check_dict, user_context, timeout_sec)` 注册**异步回调**；callback 第一参数 result 为"数据完整性校验的结果，0 为成功，其他为失败" | mind-cluster@44385c1 `component/mindio/acp/doc/Interface_description/register_checker接口.md` L5、L10、L30 | v26.1.1 固定 commit | 文档原文 | — |
| **check_dict 语义 = 文件个数完备性**："数据完整性校验条件，类型为dict，用来校验指定path下的文件个数是否符合要求"，key=path、value=该路径下文件个数；示例 `{'/mnt/dpc01/checkpoint-last': 4}` | 同上 L39-41、L77-78 | 同上 | 文档原文 | **ACP 的"完整性"是文件个数，不是字节级校验和**；目录内无 checksum/CRC 段落（API接口参考.md 仅列链接，save/load 接口文档无校验字段） |
| checker 在流程中的位置：异步保存完成后由 `async_write_tracker_file` 注册（`register_checker(_save_post_process, {real_iteration_dir: total_file_count}, iteration, 300)`）；回调成功（result==0）才写 tracker 文件（写入 iteration 号），失败记日志 "watching checkpoint failed" 且不写 tracker | `component/mindio/acp/python_whl/mindio_acp/mindio_acp/acc_checkpoint/framework_acp.py` L96-104（签名与 docstring）、L111-124（_save_post_process）、L136（注册）；register_checker接口.md L57-62（timeout [1,3600]，指向 async_write_tracker_file） | 同上 | 源码+文档互证 | tracker 加载侧读取逻辑（CheckpointRapidLoaderMixin）未逐行核 |
| MindIO ACP 总体定位：checkpoint 先写训练服务器内存、再异步写后端可靠性存储 | `component/mindio/acp/README.md` L5 | 同上 | 文档原文 | — |
| load 接口安全须知：内部用 pickle，仅可加载可信数据 | `load接口.md` L69-70 | 同上 | 文档原文 | — |

## 主张—证据表（C：Ceph 存储层完整性；候选新来源，未登记）

| 主张 | 来源与定位 | 版本/环境 | 证据性质 | 反例/未知 |
|---|---|---|---|---|
| scrub 语义："One way that Ceph ensures data integrity is by scrubbing placement groups… analogous to fsck on the object storage layer… compares each primary object to its replicas, ensuring that no objects are missing or mismatched. **Light scrubbing checks the object size and attributes**, and is usually done daily. **Deep scrubbing reads the data and uses checksums to ensure data integrity**, and is usually done weekly." | https://docs.ceph.com/en/latest/rados/configuration/osd-config-ref/ Scrubbing 节（访问 2026-10-08） | latest = Ceph 21 Umbrella 开发主线（ceph/ceph main `src/ceph_release` = "21 umbrella dev"） | 文档原文 | 版本化 URL（/en/tentacle/ 等）内容未核对 |
| 频率与自动修复配置：`osd_scrub_min_interval` 默认 1 day；`osd_scrub_max_interval` 默认 7 days；`osd_deep_scrub_interval` "Deep scrub each PG (i.e., verify data checksums) at least this often" 默认 7 days；`osd_scrub_auto_repair` **默认 false**（开启后 scrub 发现错误自动修，但损坏对象数超 `osd_scrub_auto_repair_num_errors` 默认 5 则不修） | 同上 Scrubbing 节各配置项 | 同上 | 文档原文 | — |
| 健康检查语义：PG_DAMAGED = "Data scrubbing has discovered problems with data consistency"（PG 带 `inconsistent` 或 `snaptrim_error` 标志，或 repair 进行中）；OSD_SCRUB_ERRORS = "Recent OSD scrubs have discovered inconsistencies"，通常与 PG_DAMAGED 成对 | https://docs.ceph.com/en/latest/rados/operations/health-checks/ PG_DAMAGED、OSD_SCRUB_ERRORS 节（访问 2026-10-08） | 同上 | 文档原文 | **latest 文档无名为 PG_INCONSISTENT 的健康检查**（全页检索零命中）；"inconsistent" 是 PG 状态标志，健康检查名是 PG_DAMAGED |
| scrub 覆盖边界：scrub 只处理 at-rest 数据；读路径错误在有可用副本时立即修复（OSD_TOO_MANY_REPAIRS 节，阈值 mon_osd_warn_num_repaired 默认 10） | 同上 OSD_TOO_MANY_REPAIRS 节 | 同上 | 文档原文 | — |
| 手动入口：仅 flagged clean 的 PG 会被 scrub；`ceph pg scrub <pgid>`（PG_NOT_SCRUBBED 节）、`ceph pg deep-scrub <pgid>`（PG_NOT_DEEP_SCRUBBED 节）、`ceph pg repair <pgid>`（man page "Subcommand repair starts repair on <pgid>"） | health-checks 页 PG_NOT_SCRUBBED/PG_NOT_DEEP_SCRUBBED 节；ceph/ceph@main `doc/man/8/ceph.rst` L48、L1633-1637 | 同上 | 文档+man 原文 | — |
| Ceph 文档许可：CC BY-SA 3.0 | ceph/ceph@main `doc/conf.py` L59-60 "Licensed under Creative Commons Attribution Share Alike 3.0" | 同上 | 构建配置原文 | 页脚未被网页提取器捕获，以仓库 conf.py 为准 |

## 主张—证据表（D：Python zipfile，可选项已完成）

| 主张 | 来源与定位 | 版本/环境 | 证据性质 | 反例/未知 |
|---|---|---|---|---|
| zip 每个成员自带 CRC-32（`ZipInfo.CRC` = "CRC-32 of the uncompressed file"）；`ZipFile.testzip()` "Read all the files in the archive and check their CRC's and file headers. Return the name of the first bad file, or else return None."；解压可因 "incorrect password / CRC checksum / ZIP format" 失败 | https://docs.python.org/3/library/zipfile.html（访问 2026-10-08） | Python 3 文档（页面含 3.14 特性标注） | 文档原文 | torch.load 不走 Python zipfile，走自研 C++ reader，二者行为不可互推 |

## 关键摘录

- DCP 写路径（filesystem.py L263、L331-335、L584）：`torch.save(data, cast(IO[bytes], stream))`；`os.fsync(stream.fileno())`；`pickle.dump(metadata, metadata_file)`。
- DCP tensor 读路径（filesystem.py L666–668）的显式形状断言不证明内容正确；不能据此排除 torch.load 等解析步骤可能发现的损坏。
- serialization.py L201-203 注释原文："Setting this to False may make unzipping of the torch.save output fail or warn due to corrupted CRC32. However torch.load will be able to load the file."
- MindIO register_checker 文档 L39 原文："数据完整性校验条件，类型为dict，用来校验指定path下的文件个数是否符合要求。"
- MindIO framework_acp.py L136：`mindio_acp.register_checker(_save_post_process, {real_iteration_dir: total_file_count}, iteration, 300)`。
- Ceph osd-config-ref Scrubbing 节原文："Light scrubbing checks the object size and attributes… Deep scrubbing reads the data and uses checksums to ensure data integrity…"

## 冲突与未解决项

- 任务预设路径 `component/mindio/doc/Interface_description/` 不存在；实际为 `component/mindio/acp/doc/Interface_description/`（已按实际定位，正文引用须用实际路径）。
- 任务预设的 `.metadata`"JSON？"被源码否定：实为 pickle。
- 任务预设的 PG_INCONSISTENT 健康检查名在 latest 文档不存在；实际为 PG_DAMAGED + PG 状态标志 `inconsistent`。旧版（reef/squid/tentacle）文档页未逐一核对。
- torch.load 的 C++ reader（PyTorchFileReader/miniz）是否在任何模式验证 CRC32 未核对 C++ 源码；现有证据是 Python 层 docstring 暗示不验证。正文建议表述为"torch.load 不依赖 CRC32（2.6 文档字符串明示 CRC32 缺失/损坏时仍可加载）"。
- DCP 未覆盖项：`_fsspec_filesystem.py` 等后端变体、`format_utils.py` 内容未逐行读（仅关键词扫描）；DCP 文档页（docs.pytorch.org/docs/2.6/distributed.checkpoint.html）未重读。
- MindIO 未覆盖项：`multi_save`、`preload`、`convert` 等其余接口文档未读；wheel 内 memfs 实现（C++）是否有传输级校验未查。
- Ceph health-checks 页 footer/版本标识未被提取器捕获，版本以 ceph main `src/ceph_release`（21 umbrella dev）佐证。

## 实际读取清单

- pytorch/pytorch @ v2.6.0（gh api，tag 固定）：`torch/distributed/checkpoint/filesystem.py`（769 行全文）、`torch/distributed/checkpoint/metadata.py`（关键节全文）、`torch/serialization.py`（L180-215 + 全文 crc 关键词 grep）、`torch/distributed/checkpoint/` 目录 28 个 .py 文件（逐一下载做 checksum/crc32/hashlib/digest 扫描，零命中）。
- Ascend/mind-cluster @ 44385c13d7b1d87def35f1604e8be4d16de6ca4e（gh api，commit 固定）：`component/mindio/acp/doc/Interface_description/register_checker接口.md`（84 行全文）、`load接口.md`（70 行全文）、`save接口.md`（71 行全文）、`API接口参考.md`（checker 条目定位）、`component/mindio/acp/python_whl/mindio_acp/mindio_acp/acc_checkpoint/framework_acp.py`（239 行全文）、`component/mindio/acp/README.md`（grep）。
- docs.ceph.com/en/latest/rados/operations/health-checks/（FetchURL 全文，访问 2026-10-08；PG_DAMAGED/OSD_SCRUB_ERRORS/OSD_TOO_MANY_REPAIRS/PG_NOT_SCRUBBED/PG_NOT_DEEP_SCRUBBED 节逐段读）。
- docs.ceph.com/en/latest/rados/configuration/osd-config-ref/（FetchURL，访问 2026-10-08；Scrubbing 节全节读）。
- docs.ceph.com/en/latest/rados/operations/monitoring-osd-pg/（FetchURL 全文，访问 2026-10-08；用于核对 PG 状态语义）。
- ceph/ceph @ main（gh api）：`doc/man/8/ceph.rst`（pg scrub/deep-scrub/repair 子命令节）、`doc/conf.py`（许可行）、`src/ceph_release`（"21 umbrella dev"）。
- docs.python.org/3/library/zipfile.html（FetchURL，访问 2026-10-08；ZipInfo.CRC、testzip、Decompression pitfalls 节）。

## 给正文的建议（完整性证据分层）

1. **容器格式层**：torch.save 默认写 zip CRC32，外部 zip 工具可校验；2.6 docstring 说明关闭 CRC32 仍可由 torch.load 加载，不能把 zip 有 CRC 当作 torch.load 内容校验保证，也不据此概括所有 C++ reader 路径。DCP tensor 项内嵌 torch.save，BYTE_IO 裸写，不带该容器 CRC。
2. **框架元数据层**：所查 FileSystem 的 .metadata（pickle）用 relative_path/offset/length 定位记录，默认文件按配置分桶，形状断言不验证内容。解析可能发现部分损坏，保持可解析性和形状的损坏可能逃过；本次证据不排除所有后端/扩展路径的校验。MindIO register_checker 门控文件个数与 tracker 更新，不是字节校验。
3. **存储层 scrub**：Ceph light scrub（对象大小/属性，通常每日）与 deep scrub（读数据+checksum，通常每周，`osd_deep_scrub_interval` 默认 7 天）；发现后以 PG_DAMAGED/OSD_SCRUB_ERRORS 报警，**默认不自动修复**（`osd_scrub_auto_repair=false`），手动 `ceph pg repair` → 能发现 at-rest 副本不一致/介质位衰减，不能发现"写入前已损坏"的应用层错误（垃圾进、垃圾被忠实地多副本保存）。
4. **应用自检层**：训练侧自算摘要/加载后数值合理性检查（loss、grad norm 等）。前三层均不覆盖语义级正确性；本批来源中无现成应用层实现可引，正文此层只能给出建议性表述并标注为实践建议而非来源事实。
