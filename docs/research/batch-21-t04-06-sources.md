# 第二十一批 T04-06 来源记录

任务：T04-06（新建 `storage-workload-baselines.md`，与计划 target 对齐；原暂用名已改）。作者取证轮次：首轮（fio tag/HOWTO/GPL-2.0、rados man、Lustre 观测章）＋第二轮（HOWTO 全条目行号、io_u.c 取样行、MLPerf 指南行号、Lustre Ch.32/33、rados bench 约束；独立复核初审取证点）。

## 主张—来源定位表（ID—条目/行—字段/支持范围）

| 主张 | 登记 ID | 条目/行 | 支持范围 / 未覆盖 |
|---|---|---|---|
| fio 负载/计时 | src.fio.repo-3.43 | HOWTO（http L2283-2290/http_mode L3230/rados L2273/slat-clat L5060-5080/rate L3689/latency_target L3747/status-interval L205/terse L5334/元数据 L2422/client-server L5671）＋io_u.c L2097/L2102 | 块/文件/S3/RADOS 层；RGW 兼容 unknown |
| RADOS 基准 | src.ceph.docs-rados-man-squid | man 页 bench 选项（4MB/16 线程/--no-cleanup/--run-name/同 host） | RADOS 层；RGW 侧 unknown |
| 提交规则 | src.mlcommons.storage-rules-v2.0 | 指南（sleep L79/DRAM L94/max-min L234-237/5 次 L311/5 倍 L407-408/report L570） | 规则与格式；端到端 unknown |
| Lustre 工具/观测 | src.lustre.ops-manual-2x | Ch.32/33（I/O Kit/LNet Self-Test）、Ch.12/39（Jobstats/stats） | 入口；部分含义 unknown |

## unknown 清单

1. RGW 官方负载基准；2. 部分计数器含义；3. NFS 客户端统计；4. 对象请求计时；5. 全部实测（未执行）。
