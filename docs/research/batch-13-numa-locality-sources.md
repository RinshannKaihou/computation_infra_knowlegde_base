# 第十三批来源记录：NUMA、主机内存与 I/O 局部性及成对验证（T01-03）

研究日期：2026-10-08。研究者：探索子代理（非 gpt-6.1-sol）。目标正文：`knowledge/01-hardware/numa-memory-and-io-locality.md`（procedure，planned，验收标准见 plans/full-coverage-backlog.yaml T01-03）。范围：Linux NUMA 内存策略（固定 v6.16）、numactl/numastat、hwloc、PCIe 设备 NUMA 归属 ABI、cgroup v2 cpuset、AMD EPYC NPS 官方指南、NUMA 局部/远端量化学术来源。未执行任何测量；除本文件外未改动仓库其他文件。

修订日期：2026-10-09，主执行者按 B13-R02 同步正文、本记录及登记表；补核同 commit 的 proc/cpuset、proc.rst 与任务策略范围。首次取证者与“仅改本文件”的声明保留为历史。未查询目标进程、设置绑定或运行负载。

## 主张—证据表（内核机制，固定 torvalds/linux `038d61fd642278bab63ee8ef722c50d10ab01e8f` = tag v6.16）

| 主张 | 来源与定位 | 版本 | 证据性质 | 反例/未知 |
|---|---|---|---|---|
| 系统默认策略运行时为 local allocation；启动期为 interleave 以防压垮启动节点 | [numa_memory_policy.rst L33–L44](https://github.com/torvalds/linux/blob/038d61fd642278bab63ee8ef722c50d10ab01e8f/Documentation/admin-guide/mm/numa_memory_policy.rst#L33-L44) | v6.16 | 官方文档 | — |
| first-touch 官方表述：local allocation "starts at the node containing the cpu where the allocation takes place"（缺页发生在哪颗 CPU，就从该 CPU 所在节点分配） | [L205–L213](https://github.com/torvalds/linux/blob/038d61fd642278bab63ee8ef722c50d10ab01e8f/Documentation/admin-guide/mm/numa_memory_policy.rst#L205-L213) | v6.16 | 官方文档 | 任务策略仅作用于安装后新分配的页，已 fault 页保持原位（[L66–L69](https://github.com/torvalds/linux/blob/038d61fd642278bab63ee8ef722c50d10ab01e8f/Documentation/admin-guide/mm/numa_memory_policy.rst#L66-L69)） |
| MPOL_DEFAULT 是回落语义而非真实策略；MPOL_BIND 限节点集；MPOL_PREFERRED 单节点优先可回退；MPOL_INTERLEAVED 按页轮转（匿名/共享按 faulting 地址页偏移取模，page cache 按每任务计数器）；MPOL_PREFERRED_MANY 掩码版；MPOL_WEIGHTED_INTERLEAVE 权重接口在 /sys/kernel/mm/mempolicy/weighted_interleave/ | [L175–L258](https://github.com/torvalds/linux/blob/038d61fd642278bab63ee8ef722c50d10ab01e8f/Documentation/admin-guide/mm/numa_memory_policy.rst#L175-L258) | v6.16 | 官方文档 | weighted interleave 权重接口未取独立文档 |
| 系统调用：set_mempolicy / get_mempolicy / mbind / set_mempolicy_home_node；cpuset 限制优先于 policy | [L429–L481](https://github.com/torvalds/linux/blob/038d61fd642278bab63ee8ef722c50d10ab01e8f/Documentation/admin-guide/mm/numa_memory_policy.rst#L429-L481)、[L502–L512](https://github.com/torvalds/linux/blob/038d61fd642278bab63ee8ef722c50d10ab01e8f/Documentation/admin-guide/mm/numa_memory_policy.rst#L502-L512) | v6.16 | 官方文档 | — |
| 任务策略仅作用于安装线程及它随后创建的线程，既有兄弟线程保留原策略；get_mempolicy 查询调用任务，flags 可选择地址策略/位置 | [L60–L64](https://github.com/torvalds/linux/blob/038d61fd642278bab63ee8ef722c50d10ab01e8f/Documentation/admin-guide/mm/numa_memory_policy.rst#L60-L64)、[L445–L454](https://github.com/torvalds/linux/blob/038d61fd642278bab63ee8ef722c50d10ab01e8f/Documentation/admin-guide/mm/numa_memory_policy.rst#L445-L454) | v6.16 | 固定文档 | 需覆盖实际关键 TID 与子进程；另起 helper 或读主线程不能代表全部目标策略 |
| Cpus_allowed_list 来自 task CPU 掩码；Mems_allowed_list 来自 task->mems_allowed，是允许集而非任务/VMA mempolicy | [array.c L406–L412](https://github.com/torvalds/linux/blob/038d61fd642278bab63ee8ef722c50d10ab01e8f/fs/proc/array.c#L406-L412)、[cpuset.c L4395–L4402](https://github.com/torvalds/linux/blob/038d61fd642278bab63ee8ef722c50d10ab01e8f/kernel/cgroup/cpuset.c#L4395-L4402) | v6.16 | 固定源码 | /proc/<pid>/status 为主线程；需逐关键 TID 读 task/<tid>/status，loader 等子进程单列 |
| numa_maps 的 policy 标签描述映射策略，N0=/N1= 为各节点驻留页数，二者是不同证据 | [proc.rst L683–L715](https://github.com/torvalds/linux/blob/038d61fd642278bab63ee8ef722c50d10ab01e8f/Documentation/filesystems/proc.rst#L683-L715) | v6.16 | 固定文档 | 映射快照不能证明所有线程任务策略一致；驻留分布不是访问次数 |
| numa_balancing：/proc/sys/kernel/numa_balancing 为**可按位组合的位掩码**（0=DISABLED、1=NORMAL、2=MEMORY_TIERING，3=两者同开，各标志可 OR 组合）；"there is a performance penalty if remote memory is accessed by a CPU"；机制是周期性 unmap 并在 fault 时判断迁移；"If the target workload is already bound to NUMA nodes then this feature should be disabled" | [sysctl/kernel.rst L701–L725](https://github.com/torvalds/linux/blob/038d61fd642278bab63ee8ef722c50d10ab01e8f/Documentation/admin-guide/sysctl/kernel.rst#L701-L725) | v6.16 | 官方文档 | balancing 收益无保证（同段自述）；成对测量时须固定并记录该开关（B13-C15 修订：此前误写为三个互斥取值） |
| PCI 设备 NUMA 归属：/sys/bus/pci/devices/.../numa_node = 设备连接的 NUMA 节点，未知为 -1；初值来自 ACPI _PXM 或同类固件源；可写覆盖但 taint（TAINT_FIRMWARE_WORKAROUND） | [ABI sysfs-bus-pci L355–L366](https://github.com/torvalds/linux/blob/038d61fd642278bab63ee8ef722c50d10ab01e8f/Documentation/ABI/testing/sysfs-bus-pci#L355-L366) | v6.16 | 官方 ABI | NIC/NVMe 经 /sys/class/.../device 符号链接复用同一属性（结构性推断，无 NVMe 专属 ABI 条目） |

## 主张—证据表（工具与容器）

| 主张 | 来源与定位 | 版本 | 证据性质 | 反例/未知 |
|---|---|---|---|---|
| numactl：--membind 仅从指定节点分配（不足即失败）、--cpunodebind 限定 CPU 执行节点、--interleave 轮转可回退、--localalloc/--preferred、--show/--hardware；节点说明符支持 netdev:DEV、pci:[seg:]bus:dev[:func]、block:PATH、file:PATH（工具内置设备→节点解析，反证「设备 ordinal=NUMA 编号」不成立） | [numactl(8) man7 镜像](https://man7.org/linux/man-pages/man8/numactl.8.html) | 上游 numactl git 2026-08-04 快照（页脚） | 官方 man 页 | 非版本化发行快照；COPYRIGHT 段自述 GPLv2 |
| numastat：默认输出是**全系统页分配事件计数**（按节点、单位页，可换 MB）：numa_hit=按意图在本节点分配成功；numa_miss=本想到别的节点却分到本节点（对应他节点 numa_foreign）；local_node=进程运行于本节点时在本节点分配；other_node=进程运行于其他节点时在本节点分配；数据源 /sys/devices/system/node/node*/numastat。`-p <pid>` 按节点给出目标进程分布，带选项后单位为 MB（B13-C09/C16）；numactl `--show` 仅作用于调用者，既有目标的允许集、安装策略及驻留应按上表分别取证 | [numastat(8) man7 镜像](https://man7.org/linux/man-pages/man8/numastat.8.html)、[numactl(8)](https://man7.org/linux/man-pages/man8/numactl.8.html) | 同上 | 官方 man 页 | 系统计数不能证明目标放置；允许集不证明 mempolicy，驻留快照差分不是访问次数；stat 的 processor 是最近执行 CPU，采样未变不证明全程无迁移 |
| hwloc：节点内层次图含 NUMA memory nodes、caches、packages、die、cores、PU 与 I/O 设备；I/O 对象（eth0/sda/mlx5_0/nvml0）挂到匹配物理位置的普通对象（通常 NUMA node）下，局部性沿 parent 上溯；hwloc-bind 支持 pci=0000:02:03.0 与 os=eth0 表示靠近该设备的 CPU | [hwloc v2.15.0 首页](https://www.open-mpi.org/projects/hwloc/doc/v2.15.0/)、[v2.11.2 工具章](https://www.open-mpi.org/projects/hwloc/doc/v2.11.2/a00345.php)、[I/O 章](https://www.open-mpi.org/projects/hwloc/doc/v2.11.2/a00348.php) | v2.15.0 / v2.11.2 | 官方文档 | doxygen 锚点跨版本不稳定，引用必须带版本号；hwloc 自述 OS 报告信息可能不完整 |
| cgroup v2 cpuset：cpuset.cpus（空值继承最近非空祖先；值保持到下次写入）；cpuset.cpus.effective 只读；cpuset.mems（写入非空会把任务内存迁往指定节点，迁移有代价且可能不完全，建议先设再放任务）；cpuset.cpus.partition（member/root/isolated） | [docs.kernel.org/admin-guide/cgroup-v2.html](https://docs.kernel.org/admin-guide/cgroup-v2.html) | 动态页（未标内核版本），2026-10-08 观察 | 官方（未固定版本） | 固定 commit 的 cgroup-v2.rst 行号因 raw 限流（429）未取，登记时注明 |

## 主张—证据表（厂商指南与量化）

| 主张 | 来源与定位 | 版本 | 证据性质 | 反例/未知 |
|---|---|---|---|---|
| AMD EPYC 9004：NPS=4 把每 socket 分 4 象限（各 3 CCD/3 UMC/1 I/O Hub），最近距离在象限内；NPS=2/1/0 分别为 2 域/单节点/跨双 socket 单域；LLC as NUMA 时单 socket 至多 12 个 NUMA 节点；"Do not rely on past assumptions about settings such as APICID or CCX ordering"；测网卡性能前先确定其在哪个 socket/NUMA 节点，"Performance will be sub-par if the adapter uses cores and/or memory on the distant socket"；§4.4.1 用 cat /sys/class/net/(if)/device/numa_node 与 local_cpulist 核对 | [AMD Linux Network Tuning Guide for AMD EPYC 9004, Pub 58012 Rev 1.5](https://docs.amd.com/api/khub/documents/ScFqtjHuoA5CBw6e~hb01Q/content) §2.12/§4.2/§4.3.1/§4.4.1 | Rev 1.5，2024-02 | 厂商官方 | 无带宽数字；AMD 明示不授许可，仅链接+原创归纳 |
| 远端访问量化示例（特定语境）：随机访问约 100ns、远端 +50%（2013 年「典型双路商务服务器」语境）；SLIT 距离本地 10/远端 20 为相对值 | [Lameter, An Overview of Non-Uniform Memory Access, CACM 56(9)](https://cacm.acm.org/practice/an-overview-of-non-uniform-memory-access/) | 2013-09 | 学术 | 非通用阈值 |
| 成对测量学术模板：4×Opteron 8385、4 NUMA 节点、Linux v3.6；单线程「全本地 vs 全远端」（标准 Linux 工具强制线程与内存同/异节点）性能退化从不超 20%；现代机远端约 +30% 延迟（旧机可至 7×）；拥塞时内存延迟可达 ~1200 cycles（正常 ~300）；反例：局部率更好不必然更快（PCA 交织后局部率 33%→25% 反而更快，拥塞效应） | [Gaud et al., Challenges of Memory Management on Modern NUMA Systems, CACM](https://cacm.acm.org/practice/challenges-of-memory-management-on-modern-n-uma-systems/) | 2015-12 | 学术（指明机型） | 特定机型/年代；证明「测量并记录差异」而非假设局部必然更优 |

## 候选新来源登记

`src.kernel.numa-memory-policy-v6.16`、`src.kernel.docs-sysctl-kernel-v6.16`、`src.kernel.abi-sysfs-bus-pci-v6.16`、`src.kernel.docs-cgroup-v2-2026-10-08`、`src.numactl.man-pages-2026-08-04`（numactl(8)+numastat(8) 合一）、`src.openmpi.hwloc-doc-v2.15.0`、`src.openmpi.hwloc-doc-v2.11.2`、`src.amd.epyc9004-linux-network-tuning-58012-r1.5`、`src.acm.lameter-numa-overview-2013`、`src.acm.gaud-numa-challenges-2015`。

2026-10-08 补登 `src.kernel.proc-cpuset-v6.16`；2026-10-09 将同 commit 的 `Documentation/filesystems/proc.rst` 核对范围补入该来源 notes，许可范围仍按已核对文件记录。

## 缺口与冲突

- 带宽差异（GB/s 级）无官方/学术可引用数字：AMD 指南仅给通道数与定性表述；现有量化均为时延/相对值且特定机型，正文不得写成通用阈值。
- docs.kernel.org cgroup-v2 未标内核版本；固定引用待补（raw 429）。
- Intel SNC 分支未取证（任务允许二选一，已选 AMD NPS）；Ascend 主机侧 NUMA 官方文档未取证；Intel/鲲鹏主机拓扑输入保留 unknown。
- NVMe numa_node 路径为符号链接结构性推断，未逐字核对。
