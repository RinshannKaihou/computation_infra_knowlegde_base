# 第二十一批 T04-08 来源记录（补交）

任务：T04-08（Batch 21 补交，修订既有 `data-starvation-triage.md` 与 `checkpoint-slow-io-triage.md`）。取证/修订日期：2026-10-18。性质：**全部复用已登记来源，本轮无新增外部来源登记**；按 T04-08 source_discovery「复用 T04-02/03/06/07 的版本化后端来源；回查 profiler/trace/record_function 和工具阶段计时实现」执行。

## 来源固定方式

1. 后端语义（NFS/ext4/RGW/Lustre、恢复与健康检查）：复用 T04-02/T04-03/T04-07 交付时已固定并登记的来源，本轮逐条核对 registry 条目的 revision 与许可字段（见下表），未重新抓取页面——页面内容以各来源登记时的取证记录为准（T04-02/03/07 各有独立来源记录）。
2. 计时实现回查：profiler record_function 区间名与 DataLoader 源码锚点沿用既有登记（src.pytorch.profiler-2.6、src.pytorch.dataloader-source-v2.6.0，v2.6.0 commit 1eba9b3）；DCP `dcp_logger` 方法级计时沿用 src.pytorch.dcp-2.6（同 commit）；fio slat/clat 取样点沿用 src.fio.repo-3.43（tag fio-3.43，commit d2dcd7e0，HOWTO 与 io_u.c 取样行，T04-06 已核）；rados bench 是否有阶段计时能力本轮未核对（T04-06 仅登记其重试语义 unknown；rados(8) 的 `--show-time` 选项未评估），两篇正文不写其计时能力。
3. 基线/对照口径：fio 负载矩阵、隔离/争用/冷热三组对照、latency_target 饱和读法，复用 T04-06 交付物 `storage-workload-baselines.md` 及其登记来源；不新增阈值或实测值。

## 主张—来源定位表

「直接」＝两篇正文新增节直接引用；「经链接沿用」＝正文经 KB 内页面链接间接使用，新增节未直接引用。

| 主张 | 已登记 ID | 精确页面/节 | 引用方式 | 支持范围 / 未覆盖 |
|---|---|---|---|---|
| NFS 客户端重试/超时（hard 无限重试、soft/softerr retrans 后 EIO/ETIMEDOUT、timeo 线性退避、soft 静默损坏风险）；actimeo 窗口长度与 lookupcache 正/负目录项信任语义；CTO 节 v3 语境 | src.nfs-utils.nfs-5-man7 | [nfs(5)](https://man7.org/linux/man-pages/man5/nfs.5.html) | 直接 | nfs-utils Git 快照 2026-08-04；release/commit 哈希 unknown；客户端页不证服务器；v4 CTO 单列 unknown |
| NFS 服务器统计入口（knfsd-stats/pool_stats 线程池排队/唤醒计数，饱和信号） | src.kernel.docs-nfs-v6.16 | [knfsd-stats](https://www.kernel.org/doc/html/v6.16/filesystems/nfs/knfsd-stats.html) | 直接 | 服务器侧；无请求字节/延迟；客户端 mountstats unknown |
| NFS COMMIT/write verifier、grace 期 NFS4ERR_GRACE、pNFS 协议层分离 | src.ietf.rfc-8881 | [§18.3](https://datatracker.ietf.org/doc/html/rfc8881#section-18.3)、[§18.32](https://datatracker.ietf.org/doc/html/rfc8881#section-18.32)、[§8.4.2.1](https://datatracker.ietf.org/doc/html/rfc8881#section-8.4.2.1)、[§12](https://datatracker.ietf.org/doc/html/rfc8881#section-12) | 直接 | 协议文本；实现行为以手册页/内核文档为准；客户端 pNFS 范围 unknown |
| NFS 导出 sync/async（async 违反协议、异常重启可丢数据/损坏） | src.nfs-utils.exports-5-man7 | [exports(5)](https://man7.org/linux/man-pages/man5/exports.5.html) | 直接 | 与客户端 sync 挂载选项同名不同义 |
| ext4 挂载语义（data=/commit=/barrier、errors= 反应方式、journal_dev/journal_path 外部日志设备） | src.kernel.admin-guide-ext4-v6.16 | [admin-guide/ext4](https://www.kernel.org/doc/html/v6.16/admin-guide/ext4.html) | 直接 | 内核 v6.16；目标现场选项 unknown |
| RGW S3 读/列举/multipart/版本化条目；`GET /?usage` 为用量非性能 | src.ceph.docs-rgw-s3-squid | [S3 索引](https://docs.ceph.com/en/squid/radosgw/s3/)、[bucketops](https://docs.ceph.com/en/squid/radosgw/s3/bucketops)、[objectops](https://docs.ceph.com/en/squid/radosgw/s3/objectops) | 直接 | Squid 分支文档（取证日 2026-10-13），点版本 unknown；RGW 官方性能基准/日志端点 unknown |
| Lustre MDT/OST 瓶颈分离、Jobstats、条带（§19.2 带宽主张）、Full OST、锁争用、校验和（含 ldiskfs 无持久校验与至多五次重试）、初始建联超时 | src.lustre.ops-manual-2x | [手册](https://doc.lustre.org/lustre_manual.xhtml) §1.1.1/§1.2.2/Ch.12/§19.2/§19.3–19.4/§23.1/§23.5.1/§34.10/§35.3.8/Ch.39 | 直接 | 2.x 滚动手册；主张限 ≤ LTS 2.15.x 引入特性；计数器其余含义 unknown |
| Ceph 空间压力检查（OSD_FULL/NEARFULL/POOL_FULL） | src.ceph.docs-health-checks-squid | [health-checks](https://docs.ceph.com/en/squid/rados/operations/health-checks/) | 直接 | Squid 分支；状态检查无请求字节/延迟；PG_DAMAGED/OSD_TOO_MANY_REPAIRS/BLUESTORE_SLOW_OP_ALERT 等其余条目本轮未直接引用 |
| fio 计时口径（slat 初始化到提交/clat 提交到完成/lat＝slat＋clat；io_u.c `issue_time`→clat L2097、`start_time`→lat L2102、slat L2427）与负载矩阵参数 | src.fio.repo-3.43 | [fio-3.43 树](https://github.com/axboe/fio/tree/fio-3.43)（HOWTO；io_u.c） | 直接（饥饿指南） | 独立基线工具计时，不是训练/保存路径内计时；GPL-2.0 已核 |
| 训练消费侧计时（record_function 区间、profiler 语义） | src.pytorch.profiler-2.6 / src.pytorch.dataloader-source-v2.6.0 / src.pytorch.data-loader-2.6 | [profiler](https://docs.pytorch.org/docs/2.6/profiler.html)、[dataloader.py L680/L703–704](https://github.com/pytorch/pytorch/blob/1eba9b3aa3c43f86f4a2c807ac8e12c4a7767340/torch/utils/data/dataloader.py#L680-L704) | 直接 | PyTorch 2.6；NPU 侧 profiler 未核对 |
| DCP async_save/staging/集合同步点/dcp_logger 方法级计时 | src.pytorch.dcp-2.6 | [DCP 2.6 文档](https://docs.pytorch.org/docs/2.6/distributed.checkpoint.html)＋固定源码（state_dict_saver.py L228–242/L229–248/L273–334、staging.py L37/L72/L116、filesystem.py L290–302/L331–334/L617–674） | 直接 | 文档＋v2.6.0 源码；dcp_logger 无分阶段计时 |
| Ceph 恢复定位链与 repair 边界 | src.ceph.docs-troubleshooting-pg-squid / src.ceph.docs-troubleshooting-osd-squid | [PG 排查](https://docs.ceph.com/en/squid/rados/troubleshooting/troubleshooting-pg/)、[OSD 排查](https://docs.ceph.com/en/squid/rados/troubleshooting/troubleshooting-osd/) | 经链接沿用（正文链接 storage-client-backend-recovery.md） | 见 storage-client-backend-recovery.md §3 |
| rados bench 选项；重试语义 unknown；`--show-time` 计时能力未评估（T04-06 仅登记重试语义 unknown，本轮沿用；正文不写其计时能力） | src.ceph.docs-rados-man-squid | [rados(8)](https://docs.ceph.com/en/squid/man/8/rados/) | 经链接沿用（正文链接 storage-workload-baselines.md） | bench 为 RADOS 层 |
| 内核 dirty/writeback 语义 | src.kernel.docs-sysctl-vm-v6.16 | [vm.rst L165–242（v6.16 commit 038d61fd）](https://github.com/torvalds/linux/blob/038d61fd642278bab63ee8ef722c50d10ab01e8f/Documentation/admin-guide/sysctl/vm.rst#L165-L242) | 经链接沿用（checkpoint 步骤 4 既有内容） | 机制解释；目标现场参数 unknown |
| MindIO ACP save/flush 完成语义 | src.ascend.mindio-acp-v26.1.1 | [ACP README/接口文档](https://github.com/Ascend/mind-cluster/blob/44385c13d7b1d87def35f1604e8be4d16de6ca4e/component/mindio/acp/README.md)（MindCluster v26.1.1 commit 44385c13） | 经链接沿用（checkpoint 步骤 6 既有内容） | memfs 实现与性能数据未公开核对 |
| MLPerf Storage 测量边界（host DRAM 终点、drop_caches 条件、强制 fsync） | src.mlcommons.storage-rules-v2.0 | [Submission_guidelines v2.0（commit 7e71ca16）](https://github.com/mlcommons/storage/blob/7e71ca162d8f9e7ae4b5b698d7d79b0883817f25/Submission_guidelines.md) | 经链接沿用（既有内容） | 不能替代训练端到端供给判断 |

许可口径：上表各 ID 的许可状态沿用 registry 登记（identified/partial/unknown 逐条）；本库只做原创归纳与链接，不复制原文。

## unknown 清单（本轮保留，不补写）

1. RDMA 传输行为（S22 包未执行，无已核对来源）；2. NFS/RGW 传输选项层行为（rsize/wsize/proto、RGW HTTP 前端）；3. RGW 官方性能计数器/负载基准/日志端点，读路径失败与超时语义；4. RGW Complete 前后的可见性与列举一致性、bucket 索引细节、冷/热基线入口；5. NFS 客户端 mountstats/nfsstat 登记、服务器侧空间证据、v4 客户端 CTO 单列行为、客户端 pNFS 实现范围、冷/热基线中属性/目录项缓存与 v4 委托是否随本机 drop_caches 失效；6. ext4 inode/空间耗尽与块层命令超时；7. Lustre 计数器其余含义、精确小版本、运行期超时细分、客户端缓存细分与冷/热基线入口；8. nfs-utils release/commit 哈希；9. rados bench 重试语义与 `--show-time` 计时能力（未评估）；10. NPU 侧 profiler/阶段计时实现；11. 目标现场后端版本/配置与实测基线；12. 全部实测与工具运行（本轮未执行任何工具，符合验收「来源记录说明未运行工具」）。

## 与其他记录的关系

- 后端语义细节以各交付物为准：NFS/ext4 见 [T04-02 本地与共享存储](../../knowledge/04-data-storage/local-and-shared-storage.md)、RGW/Lustre 见 [T04-03 对象与并行存储](../../knowledge/04-data-storage/object-and-parallel-storage.md)、基线口径见 [T04-06 存储负载基线](../../knowledge/04-data-storage/storage-workload-baselines.md)、恢复流程见 [T04-07 存储恢复](../../knowledge/04-data-storage/storage-client-backend-recovery.md)；本篇是两篇诊断指南的修订取证记录。
- T04-08 不触碰 B17-C08 例外约束范围（GPU 精度证据，与存储无关）；BLOCKED-1（HCCL 交集）与本任务无关。
