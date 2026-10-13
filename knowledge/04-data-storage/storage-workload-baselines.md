---
id: data-storage.storage-workload-baselines
title: 存储负载、容量与长尾基线口径
type: reference
domain: data-storage
status: draft
platforms: [generic]
source_refs:
  - src.fio.repo-3.43
  - src.ceph.docs-rados-man-squid
  - src.mlcommons.storage-rules-v2.0
  - src.pytorch.profiler-2.6
  - src.pytorch.dataloader-source-v2.6.0
  - src.lustre.ops-manual-2x
  - src.kernel.docs-nfs-v6.16
updated_at: "2026-10-14"
summary: 以 fio 3.43（含 http/rados 引擎）、Ceph Squid rados bench、MLPerf Storage v2.0 为负载工具样板，规定工作负载矩阵、完成指标、容量与长尾观测口径；文件/对象接口/RADOS/加速器端到端终点分开，不给万能阈值。
related_ids:
  - data-storage.training-data-path
  - data-storage.data-starvation-triage
  - data-storage.local-and-shared-storage
  - data-storage.object-and-parallel-storage
verification:
  status: source_checked
  evidence_refs:
    - src.fio.repo-3.43
    - src.ceph.docs-rados-man-squid
    - src.mlcommons.storage-rules-v2.0
    - src.lustre.ops-manual-2x
  notes: "已核对 fio 3.43 HOWTO 条目（http/rados 引擎、slat/clat、rate/latency_target、terse、client/server、元数据引擎）与 io_u.c 取样行、rados(8) bench 选项、MLPerf 提交指南行号、Lustre Ch.12/19/32/33/39；RGW 侧官方负载基准、部分计数器含义未取（unknown）；未执行任何负载实测。"
---

# 存储负载、容量与长尾基线口径

> 范围：负载怎么描述、测什么终点、容量与长尾怎么看。本页只定口径与方法，不给阈值、不编造测量数据。`generic` 仅为导航聚合；工具跑通不构成训练端到端供给证据。

## 1. 工具样板与测量终点（分开）

| 工具 | 版本 | 测量终点 | 不覆盖 |
|---|---|---|---|
| fio（块/文件） | 3.43（tag fio-3.43，所指 commit d2dcd7e0，tag 对象 bef04e7b；GPL-2.0） | 块/文件层：吞吐、延迟分布 | 训练语义；对象语义 |
| fio（对象接口） | 同上（`http` ioengine 对 S3 端点发 GET/PUT，`http_mode=s3`；`blocksize` 即对象大小） | S3 请求完成（客户端侧）；限制：仅 direct IO、iodepth=1，靠 numjobs 扩展；TRIM 即对象删除 | 与块/文件层 iodepth 结果不可直接对比；对 Squid RGW 的兼容性未验证（unknown） |
| fio（RADOS/元数据） | 同上（`rados` 引擎走 librados；`filecreate`/`filestat`/`filedelete`/`dircreate`/`dirstat` 测文件查找与元数据访问） | RADOS 层 / 元数据操作 | 不是对象接口（RGW S3）结果 |
| rados bench | Squid 版 [rados(8)](https://docs.ceph.com/en/squid/man/8/rados/)（`bench seconds mode [-b objsize] [-t threads]`；mode 含 write/seq/rand；默认对象 4 MB、16 模拟线程；`-b` 仅 write 模式有效；seq/rand 依赖先前 write 加 `--no-cleanup` 留下的对象） | RADOS 对象层基准 | RGW S3 语义；Ceph 侧未检索到官方负载基准（unknown），第三方 S3 压测工具不引用 |
| MLPerf Storage | v2.0 提交指南 | 终点 L94：止于 host DRAM；加速器计算以 `sleep()` 代替 L79；训练指标 samples/s＋最小 AU §4.1 L333–342；checkpoint 读/写带宽＋跨 host 可读时间 §4.2 L353 | 加速器端到端训练供给结论（与 profiler"真实加速器消费侧"不可互比） |
| PyTorch profiler/DataLoader | 2.6（消费侧分解，见[训练数据路径"每个阶段观察什么"](training-data-path.md)） | 真实加速器消费侧等待 | 存储后端归因（见[饥饿诊断指南"步骤与判断分支"](data-starvation-triage.md)） |
| Lustre 官方基准 | 2.x 手册 Ch.33 I/O Kit（sgpdd-survey 裸设备、obdfilter-survey 测 OST、ost-survey 客户端到 OST、mds-survey 测 MDS 元数据 §33.5）与 Ch.32 LNet Self-Test（网络） | 各自终点如括号所示 | 文件层 fio 结果不可直接互比 |
| Lustre 观测 | 2.x 手册 Ch.12（Jobstats 工作方式与示例输出）/Ch.39（客户端 offset/extent 统计、brw_stats、OST 块 I/O 流） | 统计入口（含义已核对 Jobstats 与 brw_stats，其余 unknown） | CollectL 为外部采集框架对接，非 Lustre 自带工具（性质说明） |

verify 为完整性附加阶段（HOWTO `verify` 写后按 header/pattern 校验），启用后多出读校验阶段、影响吞吐，不列为性能终点。

## 2. 工作负载矩阵（维度→工具参数）

| 维度 | 工具参数与条件 | 来源 |
|---|---|---|
| 数据规模 | fio `size`/`nrfiles`；MLPerf 数据集 ≥ 全部节点内存之和 5 倍＋warm-up | HOWTO；指南 L407–408/L431 |
| 读写/随机顺序 | fio `rw`；rados `mode`（write/seq/rand） | HOWTO；rados(8) |
| 块/对象大小 | fio `bs`（对象引擎下即对象大小）；rados `-b`/`-O`（`-b` 仅 write 有效） | HOWTO L2283–2290；rados(8) |
| 并发/客户端数 | fio `iodepth`/`numjobs`/client-server 模式；rados `-t`/`--run-name`（多客户端；write 与 seq 须同 host） | HOWTO L3541/L5671；rados(8) |
| 条带 | Lustre `lfs setstripe`（count/size/offset） | [Lustre 手册 §19](https://doc.lustre.org/lustre_manual.xhtml) |
| 缓存 | fio `direct`（L1200）、`invalidate`（L1974）；[T04-02](local-and-shared-storage.md) drop_caches 冷基线（见[本地与共享存储 §5](local-and-shared-storage.md)）；rados 读基准依赖先前 write 留下的对象（可能仍在缓存，是否留缓存是本库推论，须注明） | HOWTO；[T04-02](local-and-shared-storage.md) |
| durability | fio `fsync`/`end_fsync`；NFS/RGW 语义见 [T04-02](local-and-shared-storage.md)/[T04-03](object-and-parallel-storage.md) | HOWTO L1472/L1519 |
| 失败重试 | fio 默认首次失败即退出，`continue_on_error` 可继续非致命错误并统计错误数（HOWTO L4779）；rados bench 重试语义未核对（unknown） | HOWTO；rados unknown |
| 后端空间 | 已用比例/剩余空间；Lustre Ch.19 含 Free Space | 定义为本库约定；手册入口 |
| 运行窗口 | `ramp_time`（预热不计入）、`time_based`、`steadystate` | HOWTO L699/L711/L4403 |

## 3. 完成指标、对照与饱和/可用容量

指标落到工具输出：吞吐/延迟/失败（fio terse v3 含 `cpu_user`/`cpu_sys`、`iodepth_*`、`disk_util` L5334）；元数据（fio 元数据引擎；Lustre mds-survey）；CPU/队列（terse 字段）；后端容量、网络占用无来源（unknown）。

对照三组各须记录：隔离（独占窗口＋共存负载清单证明）、争用（共享负载描述）、冷热（冷态证据引 [T04-02 §5](local-and-shared-storage.md) 冷基线方法）。

饱和与可用容量：以 `latency_target` 按延迟门限读取可用点（配 `latency_window`/`latency_percentile`/`latency_run`，HOWTO L3747–3771）；`rate`/`rate_iops` 为**上限封顶**而非定速开环（HOWTO L3689），`rate_process=poisson` 调整到达过程；上限值不等于实际发出负载，实际发出速率须单独记录，否则不得以 cap 为横轴画饱和曲线；fio iodepth 为闭环、饱和段可能被压平**为本库推论**；区分**发起负载**与**完成吞吐**（acceptance 3 要求）；可用容量按延迟门限读取（官方机制），按失败门限读取**为本库约定**，门限由现场定。

## 4. 分阶段计时与跨客户端汇总（固定实现举例）

fio 计时（HOWTO＋源码）：slat（初始化到提交）、clat（提交到完成），lat＝slat＋clat；取样点 io_u.c（`issue_time`→clat L2097、`start_time`→lat L2102）；`ramp_time` 内 I/O 不计入；`--status-interval` 输出累计值（非逐段），与 json 合用须拆分；逐段序列用 `write_lat_log`/`log_avg_msec`。

跨客户端汇总：fio client/server 模式（terse 输出略有差异）；rados bench `--run-name` 多客户端＋同 host 约束；MLPerf 官方规则：checkpoint duration 取进程最大、throughput 取进程最小，结果为连续 5 次运行均值，提交 `mlperf_storage_report.json`；knfsd-stats 为 NFS 服务器侧统计（见 [T04-02 §4](local-and-shared-storage.md)选型表），NFS 客户端侧统计 unknown。**不同工具计时口径不同，结果不得直接互比。**

## 5. 实现×工具对照与训练关联

| 实现 | 工具/终点 | 统计入口 | 空缺 |
|---|---|---|---|
| 本地 ext4/NVMe | fio 块/文件层 | terse/CPU/队列字段 | 后端容量 unknown |
| NFS | fio 文件层＋knfsd-stats（服务器侧） | 服务器统计；客户端统计 unknown | 跨客户端汇总 unknown |
| RGW/RADOS | rados bench（RADOS 层）；fio http 引擎（S3 客户端侧，未验证对 Squid 兼容） | `GET /?usage`（用量非性能）；rados bench 输出 | RGW 官方基准 unknown |
| Lustre | I/O Kit（裸设备/OST/客户端到 OST/MDS）＋LNet Self-Test；fio 文件层 | Jobstats/stats/brw_stats | 计数器其余含义 unknown |

训练关联：加速器端到端结果单独记录，消费侧分解见[训练数据路径"每个阶段观察什么"](training-data-path.md)，饥饿归因见[饥饿诊断指南"步骤与判断分支"](data-starvation-triage.md)。长尾观测：延迟百分位（`percentile_list`）＋按时间 lat log，两者结合看分布与漂移。

## 来源与更新范围

- 上表各入口（fio 3.43 tag、Squid man 页、MLPerf v2.0 提交指南行号、Lustre 手册章号）。
- 待确认：RGW 侧官方负载基准；部分计数器含义；对象请求计时；NFS 客户端统计；全部实测（未执行）。
