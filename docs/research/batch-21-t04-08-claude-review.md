# 第二十一批 T04-08 初审（独立审阅）

审阅日期：2026-10-18（实际取证日）。审阅对象：提交 `ea81e79ef940eeff4e13ef7862748c7cdb9f8ad9`（Batch 21 补交 T04-08），即 [训练数据加载饥饿诊断指南](../../knowledge/04-data-storage/data-starvation-triage.md) 与 [Checkpoint 慢写与恢复 I/O 诊断指南](../../knowledge/04-data-storage/checkpoint-slow-io-triage.md) 的加法修订，以及作者来源记录 [batch-21-t04-08-sources.md](batch-21-t04-08-sources.md)。输入以下表 SHA-256 识别。

**结论：T04-08 暂不通过。新增 18 项发现（B21-C35–C52）：P1 ×0、P2 ×9、P3 ×9，全部 OPEN。** acceptance 1、4 通过；acceptance 2、3 部分满足。三处新增主张与固定上游原文相反：checkpoint 计时例子写 `async_save` 的 staging 与后台写重叠，而 v2.6.0 默认 `BlockingAsyncStager` 先阻塞完成拷贝、再提交后台 save；两篇 NFSv4.1 行写元数据/数据"协议层不分开"，而 RFC 8881 §12.2 的 pNFS 正是在协议层分离二者；饥饿指南把 `lookupcache` 写成"只改变窗口长度"，nfs(5) 中它决定的是哪类目录项被信任或重验。另有几处与 T04-02/03 原文口径不一致：v3 CTO 限定丢失、导出 `async` 的数据丢失代价未带、RGW "Complete 前后"可见性被收窄为"前"。两篇 frontmatter 都漏列了正文已引用的 ext4 来源。没有发现跨后端统一调参命令或阈值推荐，正文没有虚构实测。`make check` 通过（96 content entries / 446 sources），它只校验结构与本地链接，不说明技术正确性。

审阅者角色：独立审阅者，不是编写者。执行方式：本会话运行时系统提示标识的模型为 `claude-opus-5-5`（Claude Agent SDK 环境）。调用方没有提供 CLI modelUsage 一类的可核验记录，因此本报告无法独立证实模型身份；推理等级等运行元数据也没有可核验记录，不补造。这不是既有的 `gpt-6.1-sol / xhigh` 批量审阅约定，也不改写该约定。本轮只做审阅和只读取证：未改作者正文、来源记录、登记、索引或计划，唯一新增文件是本报告；未执行任何训练、profiling、保存/恢复、负载工具或存储操作。模型审阅不构成平台、硬件或现场验证。

## 1. 输入（以 SHA-256 识别）

| 输入 | SHA-256 |
|---|---|
| [饥饿诊断指南](../../knowledge/04-data-storage/data-starvation-triage.md)（137 行，procedure / draft；新增节 L92–105，完成判据增补 L126） | `aeb53ec49274e9c792001ca06af321eab8f3eef069eae844b86e3b7f931e7f63` |
| [Checkpoint 慢 I/O 诊断指南](../../knowledge/04-data-storage/checkpoint-slow-io-triage.md)（125 行，procedure / draft；缺口声明 L58，新增节 L83–96，完成判据增补 L113，待确认 L125） | `ddefa66303f65008231711b583beb6097ea91cec8b8f1bad22abcc8c4bae7134` |
| [作者来源记录](batch-21-t04-08-sources.md)（42 行） | `5c4a782caef42cb86ba408176b1981b1ee5db320d7f200edc3056129b2a50591` |
| [任务计划](../../plans/full-coverage-backlog.yaml)（T04-08 L5343 起，acceptance L5364–5368） | `7460b397a50ca1391ae1dc73dd2227adcffc9b2842f760e74866811efb0e29d3` |
| [来源登记](../../sources/registry.yaml)（本轮核对的 15 个 ID，见下） | `88e48a04f1194bd1740b7f6a850395fddbb875e9035d76b2193f14f82892674f` |

口径比对用的既有交付物（按本库现行草稿逐行核对）：

| 文件 | SHA-256 | 比对位置 |
|---|---|---|
| [T04-02 本地与共享存储](../../knowledge/04-data-storage/local-and-shared-storage.md) | `7d70c7198696c0338fafa91a71cc06312d31b96ffb0481f9f142fc884845c7cb` | §3 L84（CTO v3 限定）、L87（导出 async）、L90（grace 须拒绝）、L91（pNFS）；§4 L100；§5 L113 |
| [T04-03 对象与并行存储](../../knowledge/04-data-storage/object-and-parallel-storage.md) | `e5ec20ce4ecb2254f6bf1631a749a194b9eda3daf13517fc120dd391b3ca1e8b` | L34（≤ LTS 2.15.x）、§2 L53/L56（Complete 前后、列举 unknown）、§4 L79–80 |
| [T04-06 存储负载基线](../../knowledge/04-data-storage/storage-workload-baselines.md) | `f92a5f8075ca5c5947e2f0b234cc44341c9a5ae3c172c692d28a1e521f06481f` | §2 L63（rados 重试 unknown）、§4 L77（slat/clat/lat 与取样行） |
| [T04-07 存储恢复](../../knowledge/04-data-storage/storage-client-backend-recovery.md) | `aa9bb1d89e72db96a41509b372b9133f0a1abcd5b679e487607aa163d438b40f` | §1 L49、§2 L60（超时/重试）、§5 L90 |
| [T04-01 训练数据路径](../../knowledge/04-data-storage/training-data-path.md) | `f703eba9a49f545e7e62ec3864c3e0b176b313f9fcdcbdfffc565200c2cbcb81` | 流水线节 L50–73、§A L79–85、阶段表 L101–102 |
| [T04-04 传输发布](../../knowledge/04-data-storage/artifact-transfer-and-publication.md) | `03fe46aad2e9df6e5ba41fd2018909d2e51ddf27c997ee78d106ca791e74481c` | §2 L53（见 4.1 范围外观察） |

元数据核对：两篇新增的 `source_refs`（饥饿指南 6 个、checkpoint 7 个）全部在登记中存在，revision 描述与正文用法一致；`related_ids` 新增的 6 个 content_id 都能解析到已有文件；`updated_at: "2026-10-18"` 与提交日期一致。新增 Markdown 链接的相对路径（同目录互链、`../../docs/research/` 前缀、来源记录中的 `../../knowledge/04-data-storage/`）均正确，`make check` 未报断链。

## 一次源取证（审阅者独立获取）

全部用 `curl -sSL` 只读获取，默认 TLS 校验，HTTP 均为 200。HTML 去标签后按文字核对，不只判可达性。原文只放在临时目录 `/tmp/t0408/`，未入库。

| 来源（登记 ID） | URL | SHA-256（原文） | 核对点与结果 |
|---|---|---|---|
| PyTorch v2.6.0 `state_dict_saver.py` / `staging.py`（src.pytorch.dcp-2.6） | [saver](https://github.com/pytorch/pytorch/blob/1eba9b3aa3c43f86f4a2c807ac8e12c4a7767340/torch/distributed/checkpoint/state_dict_saver.py)、[staging](https://github.com/pytorch/pytorch/blob/1eba9b3aa3c43f86f4a2c807ac8e12c4a7767340/torch/distributed/checkpoint/staging.py) | saver `a6fd9c92da2ab52dda5c433a041e6e0664aac974f659c16a1e4329ed69e8e68a`；staging `c1ec8939780a37a8d81858e8fe821a48b329c7fb6cc1cd36214be57d7b613ab2` | saver L229 `staged_state_dict = storage_writer.stage(state_dict)` 先在主线程执行，L234 才 `executor.submit(save, …)`，L248 仅在 `should_synchronize_after_execute` 为真时 `synchronize_staging()`，L250 返回 Future。staging L72 `BlockingAsyncStager` "stages the state_dict on CPU RAM and blocks until the copy is complete"，L81 `_synchronize_after_execute = False`，L116 `synchronize_staging` 为 "No-op function, since staging is blocking"。协议 docstring L37 给出的重叠例子是自定义 stager "overlapping staging with the forward/backward pass"。→ C35 |
| PyTorch v2.6.0 `dataloader.py`（src.pytorch.dataloader-source-v2.6.0） | [dataloader.py](https://github.com/pytorch/pytorch/blob/1eba9b3aa3c43f86f4a2c807ac8e12c4a7767340/torch/utils/data/dataloader.py) | `f08b241c088e66361a4c7a526a55ee4e9eafd3b08beeedbfc90896ec06fcb3d3` | L680 `_profile_name = f"enumerate(DataLoader)#{self.__class__.__name__}.__next__"`；L703–704 `__next__` 包在 `record_function(self._profile_name)` 里。属实。 |
| fio-3.43 HOWTO.rst / io_u.c（src.fio.repo-3.43） | [HOWTO](https://github.com/axboe/fio/blob/fio-3.43/HOWTO.rst)、[io_u.c](https://github.com/axboe/fio/blob/fio-3.43/io_u.c) | HOWTO `f1b129ac62423ef1fb6e9a981846b766929703600b1dfc0cfb733810770e1285`（与 T04-06 审阅取得字节相同）；io_u.c `a1b8dd596af63615722e2bce516ada1759cee77dbce378e2a9f7d6702933bca5` | HOWTO L5060–5082：slat "from when fio initialized the I/O to submission"，clat "from submission to completion"；L5099–5102 lat 为二者之和。io_u.c L2097 以 `issue_time` 计 clat（L2124 `add_clat_sample`），L2102 以 `start_time` 计 lat（L2103 `add_lat_sample`）；slat 在 L2427 `add_slat_sample`。→ C46 |
| nfs(5)（src.nfs-utils.nfs-5-man7） | [nfs.5](https://man7.org/linux/man-pages/man5/nfs.5.html) | `2b9d9223f2faeadffdc7c50936a7d03ae0a194c25d9fc3d1662d40dd22e534fb`（与 T04-07 审阅取得字节相同） | `soft / softerr / hard`：hard 无限重试，soft/softerr 在 retrans 次后返回 EIO/ETIMEDOUT，"soft timeout can cause silent data corruption"。`timeo`：TCP 默认 600（60 s），线性退避至 600 s。`retrans`：TCP 2 次、UDP 3 次。`actimeo` "sets all of acregmin, acregmax, acdirmin, and acdirmax to the same value"。`lookupcache=mode`：mode 为 all/none/pos(positive)，决定正/负目录项在父目录属性过期前是否视为有效，none 为使用前总是重验。DATA AND METADATA COHERENCE → Close-to-open 节以 "When an application opens a file stored on an NFS version 3 server…" 叙述。"Options for NFS version 4 only" 下另有 `cto / nocto`（仅目录，"File data caching behavior is not affected by this option"）。→ C37、4.1 |
| exports(5)（src.nfs-utils.exports-5-man7） | [exports.5](https://man7.org/linux/man-pages/man5/exports.5.html) | `b71e95c6208c5480262437c9efd1b5bbcf3384fb60cecc6438f2a836fed5a5a2` | `async`："allows the NFS server to violate the NFS protocol and reply to requests before any changes … have been committed to stable storage"；"Using this option usually improves performance, but at the cost that an unclean server restart (i.e. a crash) can cause data to be lost or corrupted"；nfs-utils 1.0.0 之后 `sync` 为默认。→ C41 |
| RFC 8881（src.ietf.rfc-8881） | [rfc8881.txt](https://www.rfc-editor.org/rfc/rfc8881.txt)（登记 URL 为 datatracker HTML，同一 RFC） | `3b7750c792f5e507cd69289cd1132034aed5ceadc03f5ddf24779426ea42474d` | §8.4.2.1 State Reclaim："During the grace period, the server must reject READ and WRITE operations and non-reclaim locking requests … with an error of NFS4ERR_GRACE, unless it can guarantee that these may be done safely"。§12.2 pNFS Definitions："The first instantiation of pNFS, as part of NFSv4.1, separates the file system protocol processing into two parts: metadata processing and data processing"；§12.2.2 定义 metadata server，数据经 storage devices 访问。§18.3 COMMIT、§18.32 WRITE 节号属实。→ C36、C45 |
| 内核 v6.16 knfsd-stats（src.kernel.docs-nfs-v6.16） | [knfsd-stats](https://www.kernel.org/doc/html/v6.16/filesystems/nfs/knfsd-stats.html) | `ae000cd7d8da5232c0c801c83f020662f48ae0946245724275e2c0b0307d9d90` | 页内只描述 `/proc/fs/nfsd/pool_stats`，字段为 packets-arrived、sockets-enqueued、threads-woken、threads-timedout（线程池排队与唤醒计数），无请求字节或延迟；其余格式交由 nfsstat(8)（未登记）。→ C38 |
| 内核 v6.16 admin-guide/ext4（src.kernel.admin-guide-ext4-v6.16） | [admin-guide/ext4](https://www.kernel.org/doc/html/v6.16/admin-guide/ext4.html) | `2849c200bf74329159de5009afa1ed9816096a868bcfee94a20126a02c3a1e84`（与 T04-07 审阅取得字节相同） | `commit=nrsec` 默认 5 s，"you will lose as much as the latest 5 seconds of metadata changes"；`errors=remount-ro`；`journal_path=path, journal_dev=devnum`（外部日志设备）。→ C43、C44 |
| Ceph Squid health-checks（src.ceph.docs-health-checks-squid） | [health-checks](https://docs.ceph.com/en/squid/rados/operations/health-checks/) | `a6a9ed5466bb87fee93908d505ba59c96272961f2e72c1dec05a7955f0823907`（与 T04-07 审阅取得字节相同） | OSD_FULL、OSD_NEARFULL、OSD_BACKFILLFULL、POOL_FULL、POOL_NEAR_FULL、BLUESTORE_SLOW_OP_ALERT、PG_DAMAGED、OSD_TOO_MANY_REPAIRS 条目存在。均为状态检查，不提供请求字节或延迟。→ C38 |
| Ceph Squid RGW S3 objectops / bucketops / serviceops（src.ceph.docs-rgw-s3-squid） | [objectops](https://docs.ceph.com/en/squid/radosgw/s3/objectops/)、[bucketops](https://docs.ceph.com/en/squid/radosgw/s3/bucketops/)、[serviceops](https://docs.ceph.com/en/squid/radosgw/s3/serviceops/) | objectops `14f5689f8f03a42761787b024a0558153519f30b585f9f1f0395e770f042e0ba`；bucketops `3f2a9d0db33f4910d7f85113723708e5ed4c59427d19efc3db451147fbf060ba`（serviceops 未存哈希） | Upload Part 状态码 404 NoSuchUpload "Specified upload-id does not match any initiated upload on this object"；List Bucket Multipart Uploads 返回 in-progress uploads；`GET /?usage` 为按用户的用量统计（TotalBytes 等）。与正文一致。 |
| Ceph Squid RGW Metrics（未登记；本轮旁证） | [radosgw/metrics](https://docs.ceph.com/en/squid/radosgw/metrics/) | `e414b2af83802959cf3b19a43b40d89283bd98d8663144d5e96802f85858cd62` | "The Ceph Object Gateway uses Perf counters to track metrics"；Op Metrics 含 `put_obj_ops`/`put_obj_bytes`/`put_obj_lat`、`get_obj_ops`/`get_obj_bytes`/`get_obj_lat` 等，可经 counter dump 与 Prometheus 输出。→ C48、4.1 |
| Lustre Operations Manual 2.x（src.lustre.ops-manual-2x） | [lustre_manual.xhtml](https://doc.lustre.org/lustre_manual.xhtml) | `63b09d0650de3491eee9c976dff1246706dc6496bc996c139fdebdf7fc4a0d8c`（与 B20、T04-06、T04-07 审阅取得字节相同） | 目录与正文核对：§1.1.1 Lustre Features 含 "The Lustre distributed lock manager (LDLM) ensures that files are coherent between all clients and servers"；§1.2.2 Components；§12.2 Jobstats（§12.2.3 示例为按作业的 MDT 操作 samples/reqs）；§19.2 Striping Considerations（"Providing high-bandwidth access…"）；§19.3 `lfs setstripe`、§19.4 `getstripe`（命令节）；§23.1 Handling Full OSTs（23.1.2 禁建、23.1.3 迁移）；§23.5.1 Lustre Checksums（"a 32-bit checksum … corrupted in transit over the network. The ldiskfs backing file system does NOT do any persistent checksumming"；不匹配时 "re-read or re-write … up to five times"）；§34.10 Small Files（"lock ping-pong between client nodes if they are all writing to the same file"）；§35.3.8 Handling Timeouts on Initial Lustre File System Setup；§39.3.5 Monitoring the OST Block I/O Stream（brw_stats，含 I/O time 直方图）。→ C40、C47 |
| MindIO ACP flush 接口（src.ascend.mindio-acp-v26.1.1） | [flush接口.md](https://github.com/Ascend/mind-cluster/blob/44385c13d7b1d87def35f1604e8be4d16de6ca4e/component/mindio/acp/doc/Interface_description/flush%E6%8E%A5%E5%8F%A3.md) | 未存哈希（抽查） | "等待后台异步刷盘任务全部执行成功"；返回 0 成功 / 1 失败；无超时参数。与 checkpoint 步骤 6 及计时例子 ② 一致。 |

取证限制：

- 未重取 T04-08 未修改的既有内容所依据的来源（PyTorch 2.6 profiler/data/DCP HTML 文档、MLPerf Storage v2.0 指南、sysctl vm.rst、fsync(2)、MindIO save 接口）。
- Lustre 手册只核对了上表所列章节，没有逐条核对各节的 "Introduced in" 标记（见 C47、第 5 节）。
- 未执行任何命令行为验证；上表所有"行为"都是文档或源码层证据。

## 2. 发现

### 2.1 汇总表

| ID | 优先级 | 受影响位置 | 摘要 |
|---|---|---|---|
| B21-C35 | P2 | checkpoint L94 | "`async_save` 的 staging 与后台写重叠"与 v2.6.0 固定源码不符 |
| B21-C36 | P2 | 饥饿 L99、checkpoint L90（元数据 vs 数据列） | NFSv4.1"协议层不分开"与 RFC 8881 §12.2 pNFS 及 T04-02 §3 相反 |
| B21-C37 | P2 | 饥饿 L99（缓存列） | 丢掉 T04-02 的 v3 CTO 限定；`lookupcache` 语义写错；"不改变协议语义"无出处 |
| B21-C38 | P2 | 饥饿 L103 ③、checkpoint L94 ④ | knfsd-stats、Ceph health 被当作可与应用侧字节/延迟对照的后端统计 |
| B21-C39 | P2 | 饥饿 L103、checkpoint L94；acceptance 2 | 计时对齐例子缺 CPU/队列与传输层，饥饿指南还缺缓存状态 |
| B21-C40 | P2 | 饥饿 L96–101、checkpoint L87–92；acceptance 3 | NFS/RGW/Lustre 无 cold/warm 入口；checkpoint 无争用列，Lustre 缺重试入口 |
| B21-C41 | P2 | checkpoint L90、L100 | 导出 `async` 未带"违反协议、可丢数据"代价 |
| B21-C42 | P2 | 饥饿 L100、checkpoint L91 | RGW "Complete 前后可见性 unknown"被收窄为"Complete 前" |
| B21-C43 | P2 | 两篇 frontmatter `source_refs`、来源条目 | 正文内联 admin-guide/ext4，未列 `src.kernel.admin-guide-ext4-v6.16` |
| B21-C44 | P3 | 饥饿 L98、checkpoint L89 | ext4"同一介质不分层"与外部日志设备选项不符；超时措辞与 T04-07 不一 |
| B21-C45 | P3 | checkpoint L90 | grace 期"可拒绝"弱化 RFC 的 must，锚点偏粗 |
| B21-C46 | P3 | 饥饿 L103 ④ | fio slat/clat 缩写与取样行对应关系偏离 T04-06 |
| B21-C47 | P3 | 饥饿 L101、checkpoint L92 | Lustre 校验和限定与 ≤ LTS 2.15.x 范围未带出，条带带宽锚点偏移 |
| B21-C48 | P3 | checkpoint L91（另 L58、L125） | "慢只能按客户端计时"超出"无已核对来源"的证据范围 |
| B21-C49 | P3 | checkpoint L58、L125；两表；来源记录 L35–37 | unknown 清单在四处之间不同步，删去"只能按现场证据处理" |
| B21-C50 | P3 | 来源记录 L8、L11–31 | 定位表与正文实际引用不一致；rados bench 沿用归属在 T04-06 找不到 |
| B21-C51 | P3 | 饥饿 L40、checkpoint L45 | verification.notes 未披露"未重取上游页面"，新增派生主张未经任何核对 |
| B21-C52 | P3 | 饥饿 L126 | 完整性项为条件式，五项同查对硬失败修复分支的适用不明确 |

### 2.2 逐条

### B21-C35 — P2 / OPEN：checkpoint 计时例子"`async_save` 的 staging 与后台写重叠"与 v2.6.0 固定源码不符

位置：checkpoint-slow-io-triage.md「后端支路入口与同窗计时对齐」L94，"异步重叠不能简单相加"句。

证据：

- state_dict_saver.py@1eba9b3 L229 在主线程调用 `storage_writer.stage(state_dict)`，返回后 L234 才 `executor.submit(save, staged_state_dict, …)`。
- staging.py L72：`BlockingAsyncStager` "blocks until the copy is complete"；L81 `_synchronize_after_execute = False`；L116 `synchronize_staging` 是空操作。正文步骤 1（L75）自己写明 `FileSystemWriter` 继承 `BlockingAsyncStager`。
- AsyncStager 协议 docstring L37 给出的重叠例子是自定义 stager "overlapping staging with the forward/backward pass"，即与训练前/反向重叠，不是与后台写重叠。
- 所以默认路径下，同一次保存的 staging 与后台写是先后串行的；与后台 save（序列化、写入、两次集合点）重叠的是后续训练步。本句与同文步骤 2（L76）"staging 在主线程内执行"自相矛盾。按本句做关键路径判定，会把 staging 时间当成可被后台写吸收的部分。

关闭条件：改写为"默认 `BlockingAsyncStager` 下 staging 阻塞主线程并先于后台 save；后台 save 与后续训练步重叠；仅自定义非阻塞 stager（`should_synchronize_after_execute`/`synchronize_staging`）可让 staging 与前/反向重叠"，引 saver L229/L234/L248 与 staging.py L37/L72/L116。"内核 writeback 与应用写重叠"一句可保留。

### B21-C36 — P2 / OPEN：两篇 NFSv4.1 行写元数据/数据"协议层不分开"，与 RFC 8881 §12.2 及 T04-02 §3 的 pNFS 行相反

位置：data-starvation-triage.md L99 第 4 列；checkpoint-slow-io-triage.md L90 第 4 列。

证据：

- RFC 8881 §12.2："The first instantiation of pNFS, as part of NFSv4.1, separates the file system protocol processing into two parts: metadata processing and data processing"；§12.2.2 定义 metadata server，数据经 storage devices 与 storage protocol 访问。
- T04-02 §3 L91 已登记：pNFS 为协议 OPTIONAL，服务器实现状态见 nfs41-server，客户端实现范围 unknown。T04-08 的写法与前序交付物冲突。

关闭条件：删去"协议层不分开"。改写为"pNFS（RFC 8881 §12，OPTIONAL）在协议层分离 metadata server 与 storage devices，客户端 pNFS 范围 unknown（见本地与共享存储 §3）；非 pNFS 部署由同一服务器处理元数据与数据操作"。如保留"非 pNFS 时按操作类别区分瓶颈"一类判断，标为本库推论。

### B21-C37 — P2 / OPEN：饥饿指南 NFSv4.1 缓存格丢掉 T04-02 的 v3 限定，`lookupcache` 语义写错

位置：data-starvation-triage.md L99 第 3 列；来源记录 L16。

证据：

- nfs(5) 的 Close-to-open 节以 "When an application opens a file stored on an NFS version 3 server…" 叙述。T04-02 §3 L84 据此限定"此节仅以 v3 叙述；…Linux v4 客户端 CTO 行为未在已取源中单列（unknown）"。本格行头是 NFSv4.1，直接写"CTO/属性缓存窗口内可读陈旧数据"，没有带这一限定。来源记录 L16 写了"v3 语境叙述；v4 CTO 单列 unknown"，正文未同步。
- nfs(5) `lookupcache=mode`：mode 取 all/none/pos，决定正/负目录项在父目录属性过期前是否视为有效，none 表示使用前总是重验。它选的是哪类条目被信任，不是"窗口长度"。改变窗口长度的是 `actimeo`（把 acregmin/acregmax/acdirmin/acdirmax 设为同一值）。
- "不改变协议语义"在 nfs(5) 中找不到对应原文，也没有标为本库推论。

关闭条件：本格带上 T04-02 §3 的 v3 限定与 v4 unknown；`lookupcache` 按 nfs(5) 原意写（正/负目录项的信任与重验），与 `actimeo` 分开；"不改变协议语义"删除，或标本库推论并写理由。

### B21-C38 — P2 / OPEN：计时例子把 knfsd-stats 与 Ceph health 当作可与应用侧"请求字节/延迟对照"的后端统计

位置：data-starvation-triage.md L103 ③；checkpoint-slow-io-triage.md L94 ④。

证据：

- knfsd-stats（v6.16）只描述 `/proc/fs/nfsd/pool_stats`：packets-arrived、sockets-enqueued、threads-woken、threads-timedout。这是线程池排队与唤醒计数，可作服务器饱和信号，但没有请求字节或延迟。
- Ceph health-checks 是状态检查（OSD_FULL 等），也不给请求字节或延迟。
- Lustre 的 Jobstats（§12.2.3 示例为按作业的操作 samples）与 brw_stats（§39.3.5 含 I/O 大小与 I/O time 直方图）能部分支撑对照。
- RGW 侧逐操作字节/延迟在已登记来源内没有入口（见 C48）。
- 饥饿指南写"与应用侧请求字节/延迟对照"，对 NFS 与 Ceph 而言，按已登记来源做不到。

关闭条件：③/④ 按实现分写各入口实际给出的量：knfsd-stats 为服务器线程池饱和信号，Ceph health 为状态，Lustre Jobstats/brw_stats 为操作计数与 I/O 时间分布。NFS/RGW 的后端请求字节/延迟记 unknown（或先登记新来源再写），不写成可直接对照。

### B21-C39 — P2 / OPEN：同窗计时例子未覆盖 acceptance 2 列出的 CPU/队列与传输层

位置：data-starvation-triage.md L103；checkpoint-slow-io-triage.md L94；acceptance 2（计划 L5366）。

证据：

- acceptance 2 要求覆盖"客户端/缓存、后端、CPU/队列、传输、staging/后台写入/read"。
- 饥饿指南的例子由四项组成：①消费侧 record_function 区间；②训练循环取 batch 打点，与 ① 量的是同一边界；③后端；④fio 离线基线。没有 worker CPU/解码耗时，没有可交付队列或"下一顺位 batch 就绪"时刻，没有 H2D 传输起止（T04-01 阶段表 L101–102 已有对应观测项与单位），也没有客户端缓存冷/热状态。
- checkpoint 的例子覆盖了 staging、后台写、内核、后端、读侧与缓存冷/热。序列化 CPU 和恢复侧 H2D 没有进入对齐例子，而步骤 5（L79）自己要求"恢复慢时先区分读、反序列化与 H2D"。

关闭条件：饥饿指南的例子补上 worker CPU/队列就绪与 H2D 传输两层（锚到本文证据表与 T04-01 阶段表，保留 PyTorch/CUDA 语境限定与 NPU unknown），并加客户端缓存冷/热状态；checkpoint 的例子补序列化 CPU 与恢复侧 H2D，或写明为何不适用。

### B21-C40 — P2 / OPEN：NFS/RGW/Lustre 的 cold/warm 入口缺失；checkpoint 表无争用列，Lustre 缺重试/超时入口

位置：data-starvation-triage.md L96–101；checkpoint-slow-io-triage.md L87–92；acceptance 3（计划 L5367）。

证据：

- 饥饿指南只有 ext4 行写了冷/热与 drop_caches（L98）。NFS 行的缓存格写的是 CTO 一致性窗口，不是冷/热基线。T04-02 §5 L113 已有 NFS 客户端冷基线条目（本机 drop_caches；属性/目录项缓存与 v4 委托是否失效 unknown；服务器侧 unknown），没有被链接。RGW、Lustre 两行没有 cold/warm 条目，也没有记 unknown。
- checkpoint 表的"读侧与缓存"列中，NFS 行只链 CTO（§3），RGW 行只链读/条件请求（§2），Lustre 行写"缓存语义以手册为准"，都不是冷/热入口。
- checkpoint 表没有"争用"列。NFS（knfsd-stats）与 RGW 的争用入口缺失，Lustre 锁争用只出现在写路径列。
- checkpoint 的 Lustre 行没有重试/超时入口。已登记手册 §23.5.1 写明校验和不匹配时客户端 "re-read or re-write … up to five times"（登记 L5025 也记"五次重试后 EIO"）；§35.3.8 初始建联超时饥饿指南已用。

关闭条件：两表为 NFS/RGW/Lustre 各补 cold/warm 入口（NFS 链 T04-02 §5 并带其 unknown；RGW/Lustre 没有来源就显式记 unknown）；checkpoint 表补争用入口（新增列，或并入现有列但逐实现写明）；Lustre 行补重试/超时入口。

### B21-C41 — P2 / OPEN：checkpoint NFS 行列出导出 `async`，未带 exports(5)/T04-02 的数据丢失代价

位置：checkpoint-slow-io-triage.md L90 第 2 列；停止条件 L100。

证据：

- exports(5) `async`："allows the NFS server to violate the NFS protocol…"；"Using this option usually improves performance, but at the cost that an unclean server restart (i.e. a crash) can cause data to be lost or corrupted"。
- T04-02 §3 L87 保留了"违反 NFS 协议，异常重启可丢数据/损坏"；§4 L100 把导出 `sync` 列为 Checkpoint 发布到 NFS 的必要配置。
- 本行出现在"写路径慢/失败的特征入口"列，只写"允许落盘前应答"，读者容易把它读成提速选项。本文停止条件 L100 只禁止关闭 `sync_files` 与调大 dirty 参数，没有覆盖导出选项。这是 T04-02 已有边界判断在本文的缺失，但未达到"统一调参命令"红线（见第 3 节 acceptance 1）。

关闭条件：本格补"违反协议、异常重启可丢数据/损坏；Checkpoint 发布要求导出 `sync`（见本地与共享存储 §3/§4）"；停止条件补"不为提速改用导出 `async`"或等价表述。

### B21-C42 — P2 / OPEN：两篇 RGW 行把 T04-03 的"Complete 前后可见性 unknown"收窄为"Complete 前"

位置：data-starvation-triage.md L100 第 3 列；checkpoint-slow-io-triage.md L91 第 2 列。

证据：

- T04-03 §2 L53："Complete 前后可见性与列举一致性 Squid 文档未写明（unknown）"；L56："新对象多久可被列到：三页均未说明（unknown）"。
- 两篇都以"见对象与并行存储 §2"为据，却只写"Complete 前"。T04-07 §5 L90 也只把"multipart Complete 可见"作为设计预期，§2 的 unknown 保留。
- 收窄后，读者可能认为 Complete 之后的可见性是已知的，这直接影响恢复读回与跨客户端读取的判定。

关闭条件：两处改为"Complete 前后的可见性与列举一致性 unknown"，与 T04-03 §2 逐字一致。

### B21-C43 — P2 / OPEN：两篇正文内联引用 admin-guide/ext4，frontmatter 未列 `src.kernel.admin-guide-ext4-v6.16`

位置：data-starvation-triage.md L8–19（source_refs）、L98、L136；checkpoint-slow-io-triage.md L8–21、L89、L121；来源记录 L20。

证据：

- 两篇新增节都链接 `https://www.kernel.org/doc/html/v6.16/admin-guide/ext4.html`（饥饿 L98、checkpoint L89）。该 URL 在登记中对应 `src.kernel.admin-guide-ext4-v6.16`（registry L4951–4961）。
- 两篇 `source_refs` 都没有这个 ID，两篇"来源与验证记录"中的 T04-08 条目也没有列 ext4。来源记录 L20 却把它列为本轮所引。
- `make check` 不检查内联 URL 与 `source_refs` 的对应关系，所以没有报错。

关闭条件：两篇 `source_refs` 加 `src.kernel.admin-guide-ext4-v6.16`，两篇的 T04-08 来源条目补 ext4 admin-guide。来源记录 L20 若只用了 admin-guide，去掉 `src.kernel.docs-ext4-v6.16`，或写明它的用途。

### B21-C44 — P3 / OPEN：ext4 行"同一介质，元数据/数据不分层"与外部日志设备选项不符；超时措辞与 T04-07 不一致

位置：data-starvation-triage.md L98 第 2、4 列；checkpoint-slow-io-triage.md L89 第 4 列。

证据：

- admin-guide/ext4 列有 `journal_path=path, journal_dev=devnum`（"When the external journal device's major/minor numbers have changed…"），即日志可以放在独立设备上。"同一介质"不是普遍成立，也没有给出处。
- T04-07 §2 L60 写"ext4 无超时挂载语义（不适用；块层命令超时不属本格范围，unknown）"。本行改成"无客户端超时语义"，并丢了块层超时 unknown。

关闭条件：元数据列改为"默认内部日志时数据与日志同一设备；外部日志设备（`journal_dev`/`journal_path`）例外"，或标本库推论；超时格与 T04-07 §2 对齐，保留块层超时 unknown。

### B21-C45 — P3 / OPEN：checkpoint NFS 行"grace 期服务器可拒绝某些 READ/WRITE"弱化 RFC 的 must

位置：checkpoint-slow-io-triage.md L90 第 2 列。

证据：RFC 8881 §8.4.2.1："During the grace period, the server must reject READ and WRITE operations and non-reclaim locking requests … with an error of NFS4ERR_GRACE, unless it can guarantee that these may be done safely"。T04-02 §3 L90 写"须拒绝某些 READ/WRITE"。本行写"可拒绝"，链接锚到 §8.4，而 T04-02 notes（L46）已把 §8.4.2.1 记为精确锚点。

关闭条件：改为"须以 NFS4ERR_GRACE 拒绝 READ/WRITE 与非 reclaim 锁请求，除非能保证安全"，链接锚到 §8.4.2.1。

### B21-C46 — P3 / OPEN：饥饿指南 fio 计时口径缩写与取样行对应关系偏离 T04-06

位置：data-starvation-triage.md L103 ④。

证据：

- HOWTO@fio-3.43：slat 为"from when fio initialized the I/O to submission"，clat 为"from submission to completion"（L5060–5082），lat 为二者之和（L5099–5102）。
- io_u.c L2097 以 `issue_time` 计 clat，L2102 以 `start_time` 计 lat；slat 在 L2427 采样。
- T04-06 §4 L77 写的是"slat（初始化到提交）、clat（提交到完成），lat＝slat＋clat；`issue_time`→clat L2097、`start_time`→lat L2102"。本句写成"slat（提交）/clat（完成）拆分（…io_u.c 取样行 L2097/L2102）"，读者会把 L2102 当成 slat 或 clat 的取样行。checkpoint L94 直接链 T04-06 §4，没有这个问题。

关闭条件：按 T04-06 §4 的口径逐字改写，或只链 T04-06 §4 不复述。

### B21-C47 — P3 / OPEN：Lustre 条目的校验和限定与版本范围未带出，条带带宽锚点偏移

位置：data-starvation-triage.md L101；checkpoint-slow-io-triage.md L92。

证据：

- 手册 §23.5.1："a 32-bit checksum … to ensure that the data has not been corrupted in transit over the network. The ldiskfs backing file system does NOT do any persistent checksumming"。T04-03 §4 L80 保留了"ldiskfs 无持久校验"；checkpoint 行只写"32-bit 传输校验"。本文完成判据要求"完整性（读回校验结论）"，缺了这一限定，读者可能把 wire checksum 当成落盘完整性。
- "写带宽受条带布局影响"的依据在 §19.2 Striping Considerations（"Providing high-bandwidth access…"）。本行锚 §19.3/§19.4，这两节是 `lfs setstripe`/`getstripe` 的命令节。
- 两表行头写"Lustre 2.x"。T04-03 L34 与登记 L5025 的主张范围是"只用 LTS 2.15.x 及以前引入的特性"，正文未带出。

关闭条件：checkpoint 行补"ldiskfs 无持久校验"；带宽主张锚 §19.2；两表的 Lustre 行头或节首注明"主张限 ≤ LTS 2.15.x 引入特性（见对象与并行存储 §1）"。

### B21-C48 — P3 / OPEN：checkpoint RGW 行"慢只能按客户端计时"超出"无已核对来源"的证据范围

位置：checkpoint-slow-io-triage.md L91 第 2 列；相关 L58、L125。

证据：Ceph Squid 文档有 [RGW Metrics](https://docs.ceph.com/en/squid/radosgw/metrics/) 页："The Ceph Object Gateway uses Perf counters to track metrics"，Op Metrics 含 `put_obj_ops`/`put_obj_bytes`/`put_obj_lat`、`get_obj_ops`/`get_obj_bytes`/`get_obj_lat` 等。该页未登记，所以本库记"无已核对来源"本身不错。但"只能按客户端计时"是从"未检索"推到了"不存在"。

关闭条件：改为"已登记来源内没有 RGW 逐操作计数器，暂按客户端计时＋网络/后端证据判定"。如要关闭这个 unknown，按登记流程登记该页（含版本与许可）后再写入口。

### B21-C49 — P3 / OPEN：unknown 清单在缺口声明、待确认、表格与来源记录之间不同步

位置：checkpoint-slow-io-triage.md L58、L125；两篇新增表格；来源记录 L35–37。

证据：

- checkpoint L58 写"完整清单见来源记录"，但来源记录 L37 的 9 项不含表格中出现的这些 unknown：RGW 读路径失败语义与超时语义、Complete 前后可见性、bucket 索引细节、ext4 inode/空间耗尽、NFS 服务器侧空间、Lustre 运行期超时细分与客户端缓存细分、NFS v4 CTO。
- checkpoint L58 列"RGW 性能计数器/官方负载基准与日志端点"，L125 待确认只列"RGW 性能计数器/日志端点"，少了"官方负载基准"。
- ea81e79 之前的缺口声明是"网络文件系统、RDMA、对象存储的传输行为暂无已核对来源，相关支路只能按现场证据处理"。收窄后，"只能按现场证据处理"这条边界对仍为 unknown 的支路（RDMA 等）不再出现。另外，NFS/RGW 的传输行为（如 nfs(5) 中 rsize/wsize/proto 一类的传输选项、RGW HTTP 前端）不在 T04-02/03 已核对条目内，也没有列入剩余 unknown。

关闭条件：来源记录的 unknown 清单补齐表格中的 unknown（或把"完整清单"改为"主要清单"并列出差异）；L58 与 L125 列同一组项；恢复"仍 unknown 的支路只能按现场证据处理"；NFS/RGW 传输行为列为 unknown，或写明已由何处覆盖。

### B21-C50 — P3 / OPEN：来源记录定位表与正文实际引用不一致；rados bench 沿用归属在 T04-06 中找不到

位置：来源记录 L8、L11–31。

证据：

- L13 表头称"本轮新增内容所引"。但 L24（Ceph PG/OSD 排查）与 L26（rados(8)）在两篇新增节中没有直接引用，只经 T04-07/T04-06 的链接间接出现；L22 的 Lustre 行列了 §34.8 与 Ch.38，新增节没有用到。
- L8 写"rados bench 无分阶段计时（T04-06 记 unknown，沿用）"。T04-06 正文、来源记录与审阅记录中只有"rados bench 重试语义未核对（unknown）"（storage-workload-baselines.md L63），没有"无分阶段计时"的记录。T04-06 审阅 L30 记录了 rados(8) 的 `--show-time` 选项，本轮未判断它是否构成阶段计时。
- 反方向：L20 列了 ext4 来源，正文 frontmatter 却没有列（见 C43）。

关闭条件：定位表按正文实际直接引用收敛，经链接沿用的另列一栏；L8 的 rados bench 归属改为准确出处，或改记为本轮新判断并写依据。

### B21-C51 — P3 / OPEN：verification.notes 未披露"未重取上游页面"，而新增节含前序交付物中没有的派生主张

位置：data-starvation-triage.md L40；checkpoint-slow-io-triage.md L45；来源记录 L7。

证据：

- 来源记录 L7 写明"未重新抓取页面——页面内容以各来源登记时的取证记录为准"。两篇 notes 只写"复用登记版本化后端来源……本轮未运行任何工具"，没有说明未重取页面。
- C35、C36、C37（lookupcache 与"不改变协议语义"）、C44（同一介质）涉及的句子，在 T04-02/03/06/07 中都没有，所以没有经过任何一轮页面核对。对这些新增句子，`verification.status: source_checked` 不成立。

关闭条件：两篇 notes 写明"本轮未重取上游页面；新增条目以 T04-02/03/06/07 已核对口径为准"。新增的派生主张逐条处理：改回前序口径，或重新核对原文，或标本库推论。

### B21-C52 — P3 / OPEN：饥饿指南完成判据的完整性项为条件式，五项同查对硬失败修复分支的适用不明确

位置：data-starvation-triage.md L126。

证据：

- acceptance 4 要求完成判据"同时检查"身份、进展、完整性、时延/吞吐与资源代价。本文写"完整性（如发生读回，记录校验结论）"。数据加载本身就是读，"如发生读回"的触发条件不清楚。T04-01 §A L85 已有"字节校验和"独立验证项，可以直接引用。
- 五项同查限定在"定位到后端支路或做过受控对照时"。完成判据 2（硬失败修复后）是否适用，没有写明。

关闭条件：完整性项改为引 T04-01 §A 的字节校验和（抽查范围由现场定）；写明完成判据 2 的修复也需要五项记录，或写明不适用的理由。

## 3. 逐条验收判定

| # | acceptance（计划 L5365–5368） | 判定 | 依据 |
|---|---|---|---|
| 1 | 保留相邻边界判断和已有 fixed DataLoader/DCP/MindIO 实现，不因后端类型新增统一调参命令 | **通过** | diff 显示原步骤 1–7、证据表、停止条件、版本语义补充与 DataLoader/DCP/MindIO 固定锚点均未改动，删改只涉及 checkpoint 缺口声明 L58 与待确认 L125。相邻边界判断保留：饥饿 L67"应用等待但无后端请求证据时不能定为存储"、checkpoint L68"应用慢但后端空闲时不能定为存储"、L78"不能据此排除存储后端"等。两篇新增节各自写明"不给跨后端的统一调参命令"；表中只出现各实现的默认值（`timeo` 60 s/600 s、`commit` 5 s）与只读观察命令（`lfs df`、`getstripe`）；`lfs setstripe` 作为 Lustre 专属布局入口出现，未给参数值。保留意见：C41（导出 `async` 未带代价）与 C49（删去"只能按现场证据处理"）不构成违反红线，但需修订。 |
| 2 | 给出客户端/缓存、后端、CPU/队列、传输、staging/后台写入/read 的同窗计时对齐例子；明确异步重叠不能简单相加 | **部分** | 两篇都写了"异步重叠不能简单相加"，并改用关键路径判定；staging/后台写/读侧、内核层、后端都有例子，且锚到固定实现。缺 CPU/队列与传输层，饥饿指南缺缓存状态（C39）。checkpoint 的重叠举例与固定源码不符（C35）。后端对照项的可用量写过头（C38）。 |
| 3 | 为 NFS/RGW/Lustre 的争用、重试、元数据、cold/warm 和空间压力增加入口，链接独立基线与恢复流程 | **部分** | 三类后端的重试、元数据、空间压力都有入口；争用在饥饿指南有，checkpoint 缺；cold/warm 三类后端都缺（C40）。两篇都链接了 storage-workload-baselines 与 storage-client-backend-recovery。部分入口内容与上游或前序口径不符（C36、C37、C42、C45、C47）。 |
| 4 | 完成判据同时检查数据/制品身份、作业进展、完整性、时延/吞吐和资源代价；来源记录说明未运行工具 | **通过** | 两篇完成判据都新增了五项（饥饿 L126、checkpoint L113），checkpoint 的身份项链接完整性证据与传输发布。来源记录 L3 与 L37 第 9 项、两篇 notes 及来源条目都写明本轮未运行任何工具。保留意见：C52。 |

## 4. 总体结论与保留边界

**总体结论：暂不通过。** 需关闭 C35–C43（9 项 P2）后做定向复核；C44–C52（9 项 P3）建议同轮处理。acceptance 2、3 的"部分"分别随 C35/C38/C39 与 C40 的关闭重新判定。

保留边界：

- 本审阅只核对文本与上游文档/源码之间的一致性，以及本库各层记录之间的一致性。它不构成平台兼容、硬件或现场验证。
- 没有执行 DataLoader、profiler、DCP 保存/恢复、MindIO、fio、rados bench，也没有做任何 NFS 挂载、RGW 请求或 Lustre 命令。文中所有"行为"都是文档或源码层证据。
- 本报告不改变任何正文的编辑状态或 `verification.status`。`source_checked` 是否适用于新增句子，由作者按 C51 处理。
- 计划中 T04-08 的 `status: planned` 未随交付提交更新。按本库惯例，状态在审阅闭环后回填，因此不作为发现。

### 4.1 范围外观察（不编号，不计入本轮发现）

- nfs(5) 快照的 "Options for NFS version 4 only" 下另有 `cto / nocto`："…for NFS directories on this mount point… File data caching behavior is not affected by this option"。这与 T04-02 §3 L84"Linux v4 客户端 CTO 行为未在已取源中单列（unknown）"有关，建议 T04-02 的维护者评估。它不改变 C37 的关闭条件，T04-08 只需与 T04-02 现行口径同步。
- T04-04 artifact-transfer-and-publication.md §2 L53 也写"完成前可见性/列举一致性 unknown"，与 C42 属同类收窄，位于已闭环任务。
- Squid RGW Metrics 页（见 C48）同样可以作为 T04-03 §4、T04-06 §5、T04-07 待确认中"RGW 性能计数器/管理统计"unknown 的关闭路径。

## 5. 本轮无法核验的事项

1. 执行模型身份：运行时系统提示标识为 `claude-opus-5-5`，但没有 CLI modelUsage 等可核验记录；推理等级未知。
2. 任何运行行为：未执行训练、profiling、DCP 保存/恢复、MindIO、fio、rados bench、NFS 挂载、RGW 请求或 Lustre 命令；未运行 `make build`（会写 `build/`，超出只读审阅范围）。
3. nfs(5)/exports(5) 的 nfs-utils release/commit 哈希（man7 快照，unknown 沿用）。本轮取得的 nfs.5.html 字节与 T04-07 审阅（2026-10-13）记录的哈希相同，但无法证明与作者登记时（HTML rendering 2026-09-09）的页面相同。
4. Ceph Squid 文档是分支文档，点版本 unknown；RGW Metrics 页对目标点版本是否适用未核对。
5. Lustre 2.x 滚动手册：所引 §12.2、§19.2–19.4、§23.1、§23.5.1、§34.10、§35.3.8、§39.3.5 是否都属于 ≤ LTS 2.15.x 引入的特性，没有逐条核对 "Introduced in" 标记。
6. RFC 8881 本轮取 rfc-editor.org 纯文本，登记 URL 为 datatracker HTML。节号与正文一致，两种渲染未逐字比对。
7. T04-08 未修改的既有内容所依据的来源（PyTorch 2.6 profiler/data/DCP HTML 文档、MLPerf v2.0 指南、sysctl vm.rst、fsync(2)、MindIO save 接口等）未重取；只抽查了 MindIO flush 接口。
8. knfsd-stats 页之外的 NFS 服务器统计（如 nfsstat(8) 读取的其他文件）未登记，未核对。
9. Lustre Jobstats 的 OST 侧字段本轮只看到 §12.2.3 的 MDT 示例，OST 示例未逐字核对。
10. T04-02/03/06/07 本身的正确性只就与 T04-08 相关的条目做了抽查，不构成对这些交付物的复审。
11. 链接只做了本地相对路径核对（`make check` 通过）；外部 URL 只对本轮取证的页面判了可达。
