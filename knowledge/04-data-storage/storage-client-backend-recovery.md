---
id: data-storage.storage-client-backend-recovery
title: 存储客户端、后端异常与恢复验证
type: procedure
domain: data-storage
status: draft
platforms: [generic]
source_refs:
  - src.ceph.docs-troubleshooting-pg-squid
  - src.ceph.docs-troubleshooting-osd-squid
  - src.ceph.docs-health-checks-squid
  - src.ceph.test-scrub-repair-v19.2.7
  - src.ceph.blog-manual-repair-object-2015
  - src.nfs-utils.nfs-5-man7
  - src.nfs-utils.exports-5-man7
  - src.ceph.docs-rgw-s3-squid
  - src.lustre.ops-manual-2x
  - src.kernel.admin-guide-ext4-v6.16
updated_at: "2026-10-14"
summary: ext4/NFS 客户端可用性、Ceph RGW/RADOS 健康、Lustre 客户端/元数据/数据服务的证据入口与故障责任边界；覆盖挂载/权限/超时/空间耗尽/后端降级；恢复先保留证据、保护恢复点；主案例为 v19.2.7 官方回归测试，2015 博客降为历史参考；演练判据逐项设计。
related_ids:
  - data-storage.local-and-shared-storage
  - data-storage.object-and-parallel-storage
  - data-storage.checkpoint-integrity-evidence
  - data-storage.checkpoint-durability
  - data-storage.storage-workload-baselines
  - training.checkpoint-state-recovery-triage
applicability:
  environment_refs: []
  notes: "流程以 Ceph Squid 排查/健康文档、v19.2.7 回归测试、ext4 管理指南、nfs-utils 手册页、Lustre 2.x 手册为证据样板；目标环境的版本、拓扑、凭据与授权需另行固定。故障注入或修复仅写方法及现场前提，不操作共享存储。"
verification:
  status: source_checked
  evidence_refs:
    - src.ceph.docs-troubleshooting-pg-squid
    - src.ceph.docs-troubleshooting-osd-squid
    - src.ceph.test-scrub-repair-v19.2.7
    - src.ceph.blog-manual-repair-object-2015
  notes: "已核对 Squid PG/OSD 排查页、健康检查页、v19.2.7 测试函数行号、博客链条、复用本地与共享存储/对象存储登记；未执行任何故障注入、修复、重连或演练。"
---

# 存储客户端、后端异常与恢复验证

> 范围：先证据入口与责任边界，再故障覆盖（故障类别 × 实现），再恢复步骤（先保留证据、保护恢复点；repair/remount/回放分节），最后主案例（官方回归测试）与历史参考、演练判据设计。`generic` 仅为导航聚合；恢复动作只能引用选定实现条件；未执行不标 reproduced。

## 1. 证据入口与故障责任边界（按实现分列）

| 实现 | 可用性证据入口 | 故障责任边界（含判据示例） |
|---|---|---|
| ext4 本地 | 挂载状态、dmesg；`errors=remount-ro\|continue\|panic`（转只读说明检测到文件系统错误，`errors=` 只决定检错后的反应方式，[admin-guide/ext4](https://www.kernel.org/doc/html/v6.16/admin-guide/ext4.html)）；日志回放完成（见[本地与共享存储 §2](local-and-shared-storage.md)） | 单机：设备/驱动/文件系统检出错误；`errors=` 只是反应方式 |
| NFS 客户端 | 挂载选项（[nfs(5)](https://man7.org/linux/man-pages/man5/nfs.5.html)）；retrans 次后 "server not responding" 消息；服务器导出（[exports(5)](https://man7.org/linux/man-pages/man5/exports.5.html)）；重传统计（mountstats 未登记，unknown） | "server not responding"指向服务器或网络；`soft` 返回 EIO 属客户端选项后果；缓存/锁属客户端，导出/负载属服务器 |
| Ceph RGW/RADOS | `ceph health detail`；scrub 报警 PG_DAMAGED/OSD_SCRUB_ERRORS；满类检查 OSD_FULL/NEARFULL/POOL_FULL（`ceph df`、`full_ratio`）；RGW 健康/管理文档未检索（unknown） | RADOS 层 vs RGW 语义层分开判定：`read_error` 指向介质或设备侧，`data_digest_mismatch` 指向副本不一致（见 PG 排查页） |
| Lustre 客户端/元数据/数据 | `health_check` 的 "not healthy" 判读（§35.3.2 OST 只读语境）、`lfs check servers`、`lfs df`、Ch.35.3/38.1（见[手册](https://doc.lustre.org/lustre_manual.xhtml)） | 客户端 vs MDS/MDT vs OSS/OST vs LNet 分开判定：`health_check` "not healthy" 且 ldiskfs 只读指向 OSS/OST 块设备（§35.3.2） |


## 2. 故障覆盖（故障类别 × 实现）

| 类别 | ext4 | NFS | Ceph | Lustre |
|---|---|---|---|---|
| 路径/挂载/权限/凭据 | 路径/挂载/权限按实现检查；凭据：ext4 无凭据概念（不适用，理由为单机本地文件系统） | 同左；`sec=krb5*` 凭据语义见 [nfs(5)](https://man7.org/linux/man-pages/man5/nfs.5.html)，超出部分 unknown | 池/对象命名与权限见 RGW 文档（细节 unknown；RGW 文档登记见 [S3 索引](https://docs.ceph.com/en/squid/radosgw/s3/)，未逐项核对） | 凭据见手册 §30.6 Kerberos；超出 unknown |
| 超时/重试 | ext4 无超时挂载语义（不适用；块层命令超时不属本格范围，unknown） | hard 无限重试；soft/softerr retrans 次后 EIO/ETIMEDOUT；timeo TCP 默认 60 s 线性退避至 600 s，retrans TCP 2/UDP 3；soft 静默损坏风险（[nfs(5)](https://man7.org/linux/man-pages/man5/nfs.5.html)） | RGW 超时未检索（unknown） | Ch.35.3.8 只覆盖初始建联超时；运行期超时与恢复见 Ch.38（unknown 细分） |
| 空间/元数据耗尽 | inode/空间耗尽无来源（unknown） | 同左 unknown | 池满：`ceph df`、`full_ratio`、短期 `set-full-ratio`、加 OSD 或删数据；残留 rados bench 对象须谨慎删除（见 [health-checks](https://docs.ceph.com/en/squid/rados/operations/health-checks/) OSD_FULL 节） | Full OST：禁建（§23.1.2）、数据迁移（§23.1.3）（见手册 §23.1） |
| 后端降级/损坏 | 慢盘无来源（unknown） | 同左 unknown | OSD 慢盘/坏盘：OSD_TOO_MANY_REPAIRS（阈值 `mon_osd_warn_num_repaired` 默认 10，见 health-checks）、BLUESTORE_SLOW_OP_ALERT（条目存在，阈值未核 unknown）；副本不一致见 §3–§4 | OST 缺失/损坏/只读见 Ch.35.3 |

## 3. 恢复步骤（先保留证据、保护恢复点）

1. 保留证据：Ceph 官方定位链 `ceph health detail` → `rados list-inconsistent-pg <pool>` → `rados list-inconsistent-obj <pgid> --format=json-pretty`（逐 OSD size/digest、逐 shard 错误）；保存其 JSON 输出；shard 错误含 `read_error` 时先查 `dmesg` 与 `smartctl`（物理错误前置条件，见 [Squid PG 排查页](https://docs.ceph.com/en/squid/rados/troubleshooting/troubleshooting-pg/)）。
2. 保护恢复点：在最后一个已知可恢复点验证前不覆盖；存储恢复完成前不进入训练侧结论（训练侧按[恢复诊断指南"适用范围与前置条件"](../06-training/checkpoint-state-recovery-triage.md)首条开始；该指南的停止条件针对训练侧，不复用为存储侧条件，见下）。
3. 按官方条件选择：重连（NFS grace/reclaim，见[本地与共享存储 §3](local-and-shared-storage.md)）；恢复服务（OSD 维护前 `add-noout`/`set-group noout`，集群级 noout 只是 thought exercise；停止后 PG 变 degraded，维护后 `unset`；见 [Squid OSD 排查页](https://docs.ceph.com/en/squid/rados/troubleshooting/troubleshooting-osd/)）；Lustre MDS/OST failover（Ch.38.1.3/38.1.4）。repair 以外的"从可信副本恢复"流程未取源（unknown）。
4. repair（停止条件：repair 后 `list-inconsistent-obj` 仍非空或出现 `read_error` 即停，改用人工流程；本库约定）：`ceph pg repair` 按 Ceph 选定的权威副本修复，**权威性不可证**（checksum 不能证明任一副本权威；无 checksum 时偏向 primary，可能并非未损坏副本，需人工判断）；replicated pool 下仅把不一致副本标 missing，恢复不在 repair 范围内；EC/BlueStore pool 在 `osd_scrub_auto_repair` 开且错误数 ≤ 默认 5 时自动修复；"选错权威即丢数据"为本库推论。适用限定：上段"无 checksum/手动修复"材料针对 Filestore（BlueStore 有内部 checksum，不适用）；"权威性不可证、偏向 primary、需人工判断"同样限 Filestore 或 checksum 不可用情形；PG 页未描述 BlueStore 下如何选择权威副本（unknown）。通用部分保留原文的"repair 不能解决所有问题"与 Ceph 不自动修复；FileStore 相关材料只适用于 Quincy 及以前（见 OSD 排查页）。
5. remount（停止条件：remount 后挂载选项未生效或状态异常即停，本库约定）：ext4 `errors=remount-ro` 为系统自动转只读（见 admin-guide）；手动 remount 丢失未同步状态的风险未取源（unknown）；NFS remount 与 hard/soft 关系未取源（unknown）。
6. 回放（停止条件：回放序列出现不可解释的 gap、§38.4.1 VBR 消息（`Version mismatch during replay`）或客户端驱逐即停，本库约定）：ext4 日志回放；Lustre Metadata Replay（Ch.38.2）：gap 的两种来源为 lost replies 与缺席恢复的客户端，未全部重连时缺席客户端的请求不再回放，gap 之后能否回放由 VBR 按版本判定，版本不匹配时客户端被驱逐（§38.4）；Failed Recovery 分支只作停止或升级分支（§38.1.6：客户端被驱逐并须清除保存状态），不作完成条件；NFS reclaim 状态回放（见[本地与共享存储 §3](local-and-shared-storage.md)）。回放依赖日志完整（机制描述；实现保证 unknown）。

本文自己的存储侧停止条件：repair 后 `list-inconsistent-obj` 仍非空或出现 `read_error` 即停（Ceph，见 PG 排查页；本库约定）；NFS grace 结束时 reclaim 仍未完成即停（见[本地与共享存储 §3](local-and-shared-storage.md)；grace 时长 unknown 沿用；本库约定）；Lustre 进入 failed recovery 即停并记录（手册 Ch.38.1.6）；ext4 回放报错或检查发现不一致即停（本库约定；专用停止语义未取源）；任一触发即停。存储侧完成条件：Ceph PG_DAMAGED/OSD_SCRUB_ERRORS 消除且 PG 回到 `active+clean`（状态含义见 [Squid PG 排查页](https://docs.ceph.com/en/squid/rados/troubleshooting/troubleshooting-pg/)；以此作完成判据为本库约定）；NFS reclaim 完成与 grace 结束（见[本地与共享存储 §3](local-and-shared-storage.md)，reclaim 实际判据与 grace 时长 unknown 沿用）；Lustre recovery 完成并记录（手册 Ch.38.2；failed recovery 只作停止分支，不作完成）；ext4 回放/检查完成（见[本地与共享存储 §2/§5](local-and-shared-storage.md)，超出部分 unknown）。任一未满足不进入训练侧。

## 4. 主案例：v19.2.7 官方回归测试（正式上游测试）

`qa/standalone/scrub/osd-scrub-repair.sh`（tag v19.2.7，所指 commit 9ec952b9）：`TEST_corrupt_and_repair_replicated`（L93；注释关联 tracker #8914，未打开）对非主与主副本分别调 `corrupt_and_repair_one`（L225–244）：`objectstore_tool … remove` → `repair $pg` → `list-attrs` → `rados get` 读回 → 与原件 `diff`。读回 diff 即"可读/完整"判据样板（见 §5）。同文件另有 `TEST_auto_repair_bluestore_*`、`TEST_repair_stats`（未审计，unknown）。该测试用 objectstore 工具，不依赖 FileStore 布局。

历史参考（降级，非主案例）：Ceph 官方站点博客（2015，作者 shan）手动修复流程——HEALTH_ERR 定位 PG → OSD 日志 digest 不一致 → `find` 定位对象文件 → 比对副本 → 停 OSD → flush journal → 移走坏对象 → `ceph pg repair`。**FileStore 前提**：对象文件路径与 journal flush 只适用于 FileStore；Squid（Reef 及以后）不支持 FileStore，故整条流程不适用于 Squid/BlueStore，仅作历史流程参考。另记两处风险细节：日志显示**两份** shard 与已知 digest 不符（权威选择本身不清）；博客开头建议"先试 repair"、两副本 trick 用集群级 noout，均与本文流程/Squid 建议不同。

## 5. 演练判据设计（只设计不执行；前置/预期/失败判据/实际留空/执行授权）

| 类别 | 实现 | 前置 | 预期（来源依据） | 失败判据 | 实际/授权 |
|---|---|---|---|---|---|
| 客户端重连 | ext4 | 重挂载条件具备 | 重挂载后日志回放完成即进入完成判定（回放后文件系统一致为完成判据，见[本地与共享存储 §5](local-and-shared-storage.md)；commit 窗口内数据状态 unknown 沿用；无 ext4 专用重连协议，记 unknown） | 回放未完成 | 未执行留空；按现场授权 |
| 客户端重连 | NFS | grace/reclaim 条件具备 | reclaim 完成；verifier 变化即重发（见[本地与共享存储 §3](local-and-shared-storage.md)/§5） | grace 超时未完成/哈希不符 | 未执行留空；按现场授权 |
| 客户端重连 | Lustre | eviction/replay 条件 | 重连后 replay 完成、recovery 结束（手册 Ch.38.2） | replay 未完成/进入 failed recovery 分支（Ch.38.1.6，只作停止分支） | 同上 |
| 可读 | Ceph | repair 完成 | `rados get` 成功（测试 L243 样板） | 读失败 | 同上 |
| 完整 | Ceph | repair 完成 | 读回与原件 diff 一致（测试 L244 样板）＋PG 回到 `active+clean`、告警消除（PG 状态含义见 [Squid PG 排查页](https://docs.ceph.com/en/squid/rados/troubleshooting/troubleshooting-pg/)；以此作完成判据为本库约定） | diff 不符/仍 inconsistent/告警在 | 同上 |
| 提交一致性 | NFS/RGW | 前置同各自提交条件 | COMMIT/verifier 通过（见[本地与共享存储 §3](local-and-shared-storage.md)）；multipart Complete 可见（设计预期，见[对象与并行存储 §5](object-and-parallel-storage.md)；§2 可见性 unknown 保留） | verifier 不符/不可见 | 同上 |
| 负载恢复 | 通用 | 有[负载基线](storage-workload-baselines.md)（无基线记 unknown） | 恢复到基线分布内（本库约定） | 低于基线 | 同上 |
| 故障域演练 | Ceph/Lustre | 维护域示例（`set-group noout`；手册 38.1.3/38.1.4） | 故障域内影响，域外无影响（本库约定） | 越界影响 | 同上；故障注入仅方法＋现场前提，不操作共享存储 |

## 来源与更新范围

- 上表各入口（Squid 排查/健康页、v19.2.7 测试、博客案例、[本地与共享存储](local-and-shared-storage.md)/[对象与并行存储](object-and-parallel-storage.md)登记复用）。
- 待确认：NFS 重传统计登记；RGW 日志端点；Lustre 计数器含义；tracker #8914；目标现场配置；全部实测与演练（未执行）。
