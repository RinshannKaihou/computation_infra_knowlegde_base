---
id: hardware.numa-memory-and-io-locality
title: NUMA、主机内存与 I/O 局部性的成对验证
type: procedure
domain: hardware
status: draft
platforms: [generic]
source_refs:
  - src.kernel.numa-memory-policy-v6.16
  - src.kernel.proc-cpuset-v6.16
  - src.kernel.docs-sysctl-kernel-v6.16
  - src.kernel.abi-sysfs-bus-pci-v6.16
  - src.kernel.docs-cgroup-v2-2026-10-08
  - src.numactl.man-pages-2026-08-04
  - src.openmpi.hwloc-doc-v2.15.0
  - src.openmpi.hwloc-doc-v2.11.2
  - src.amd.epyc9004-linux-network-tuning-58012-r1.5
  - src.acm.lameter-numa-overview-2013
  - src.acm.gaud-numa-challenges-2015
updated_at: "2026-10-09"
summary: 连接 NUMA 本地/远端访问、first-touch 页分配、进程/线程亲和与 PCIe/NIC/NVMe 局部性；给出 topology→进程→内存→I/O 证据链和同负载局部/远端成对测量方法，含线程迁移、NUMA 无感与数据饥饿反例。
related_ids:
  - hardware.resource-topology
  - data-storage.data-starvation-triage
  - data-storage.training-data-path
  - training.slow-rank-triage
applicability:
  environment_refs: []
  notes: "尚无环境档案；内核机制按 Linux v6.16 固定文档，工具按 numactl 上游 2026-08-04 快照与 hwloc v2.15.0/v2.11.2 文档；具体节点拓扑、内核与工具版本需先记录再套用。"
verification:
  status: source_checked
  evidence_refs:
    - src.kernel.numa-memory-policy-v6.16
    - src.kernel.proc-cpuset-v6.16
    - src.kernel.abi-sysfs-bus-pci-v6.16
    - src.numactl.man-pages-2026-08-04
    - src.amd.epyc9004-linux-network-tuning-58012-r1.5
    - src.acm.gaud-numa-challenges-2015
  notes: "核对 v6.16 内核文档行号、numactl/numastat man 页、hwloc 版本化文档、AMD 指南与两篇 CACM 文章；2026-10-09 补核 proc/cpuset 固定源码、任务策略线程范围及 proc.rst 的 numa_maps 字段，分开允许集、已安装策略、最近执行位置与页驻留。未执行任何 NUMA 测量或绑定操作。"
---

# NUMA、主机内存与 I/O 局部性的成对验证

## 目标与触发条件

回答的问题是：「进程使用的 CPU、内存和它访问的设备（加速器/NIC/NVMe）是否在同一个 NUMA 节点，跨节点访问是否解释了观察到的性能差异」。典型触发：训练 step 时间变长且伴随数据等待、H2D 传输时间异常、同机型不同节点性能不一致、网卡/盘吞吐低于预期。症状不直接等于 NUMA 根因——NUMA 只是候选之一，需要成对测量支持或反驳。

## 概念基础：放置先于绑定

NUMA 的关键是**物理放置**而非逻辑编号。Linux v6.16 文档对本地分配（local allocation）的表述是「从发生分配的 CPU 所在节点**开始**分配」（[numa_memory_policy.rst L205–L213](https://github.com/torvalds/linux/blob/038d61fd642278bab63ee8ef722c50d10ab01e8f/Documentation/admin-guide/mm/numa_memory_policy.rst#L205-L213)），即 **first-touch** 是一种分配起点倾向，不是落点保证：最终驻留还受允许节点集（cpuset/mempolicy 掩码）、该节点内存可用性、回退规则与显式策略（bind/interleave）影响。「开始尝试分配」不等于「最终驻留保证」，因此策略意图与实际页位置必须分别核对（见下文证据表）。推论：

- 内存策略只作用于策略安装后**新分配**的页，已 fault 的页保持原位（[L66–L69](https://github.com/torvalds/linux/blob/038d61fd642278bab63ee8ef722c50d10ab01e8f/Documentation/admin-guide/mm/numa_memory_policy.rst#L66-L69)）。先启动进程再绑策略，旧页不动。
- 系统默认策略运行时为 local allocation，启动期为 interleave（[L33–L44](https://github.com/torvalds/linux/blob/038d61fd642278bab63ee8ef722c50d10ab01e8f/Documentation/admin-guide/mm/numa_memory_policy.rst#L33-L44)）。
- 策略族：MPOL_DEFAULT 是回落语义而非真实策略；MPOL_BIND 限定节点集；MPOL_PREFERRED 单节点优先可回退；MPOL_INTERLEAVED 按页轮转；MPOL_PREFERRED_MANY 为掩码版；MPOL_WEIGHTED_INTERLEAVE 支持权重（[L175–L258](https://github.com/torvalds/linux/blob/038d61fd642278bab63ee8ef722c50d10ab01e8f/Documentation/admin-guide/mm/numa_memory_policy.rst#L175-L258)）。
- cpuset 限制优先于内存策略（[L502–L512](https://github.com/torvalds/linux/blob/038d61fd642278bab63ee8ef722c50d10ab01e8f/Documentation/admin-guide/mm/numa_memory_policy.rst#L502-L512)）。
- 任务内存策略有线程范围：新策略只作用于安装它的线程及该线程随后创建的线程，已存在的兄弟线程保留各自策略（[L60–L64](https://github.com/torvalds/linux/blob/038d61fd642278bab63ee8ef722c50d10ab01e8f/Documentation/admin-guide/mm/numa_memory_policy.rst#L60-L64)）。主线程或启动参数不能代替关键工作线程的策略证据；loader 等子进程也需单独定位。
- 内核自动NUMA balancing 会在 fault 时尝试把页迁往本地节点；官方明确「如果目标负载已经绑定到 NUMA 节点，应关闭该特性」（[sysctl/kernel.rst L701–L725](https://github.com/torvalds/linux/blob/038d61fd642278bab63ee8ef722c50d10ab01e8f/Documentation/admin-guide/sysctl/kernel.rst#L701-L725)）。注意 `/proc/sys/kernel/numa_balancing` 是**可按位组合的位掩码**而非互斥取值：0=DISABLED、1=NORMAL、2=MEMORY_TIERING，3=两者同时开启（同段说明各标志可 OR 组合）；看到 3 不是错误配置。测量时未记录该开关状态，结果不可比。

远端访问存在性能惩罚，但量级绑定具体机型：2013 年文献给「典型双路服务器」随机访问约 100ns、远端 +50%（[Lameter, CACM 56(9)](https://cacm.acm.org/practice/an-overview-of-non-uniform-memory-access/)）；2015 年在 4×Opteron 8385 / Linux v3.6 上测得远端约 +30% 延迟、单线程性能退化不超 20%，且拥塞时内存延迟可达约 1200 cycles（正常约 300）（[Gaud et al., CACM 2015](https://cacm.acm.org/practice/challenges-of-memory-management-on-modern-n-uma-systems/)）。这些是特定机型/年代的示例，不是通用阈值；本地 vs 远端的影响必须用本机成对测量确定。

## 适用范围与前置条件

- 内核机制按 Linux v6.16 固定文档（commit 038d61fd）；不同内核版本的策略集和默认值可能不同，先记录目标节点内核版本。
- 工具：numactl（man 页对应上游 git 2026-08-04 快照）、hwloc（v2.15.0/v2.11.2 文档）。命令字段以本机实际安装版本的 man 页为准。
- 平台拓扑作为输入而非结论：NVIDIA DGX H100（2×Intel Xeon 8480C）、Atlas 800T A2（4×鲲鹏 920）、AMD EPYC 节点（NPS 设置决定 NUMA 节点数）布局完全不同；本文只比较方法。**不假设设备 ordinal 与 NUMA 编号相同**：加速器/NIC 的设备编号来自驱动枚举顺序，NUMA 归属必须逐个核对（见步骤 1）。AMD 官方指南同样要求「Do not rely on past assumptions about settings such as APICID or CCX ordering」（[58012 Rev 1.5 §2.12](https://docs.amd.com/api/khub/documents/ScFqtjHuoA5CBw6e~hb01Q/content)）。
- 本文命令均为查询/绑定类，不改变系统配置；numa_balancing 等 sysctl 的修改需要现场授权，不在本文范围。

## 需要的证据（topology→进程→内存→I/O 链）

| 证据 | 采集（固定版本口径） | 单位/窗口 | 用途 | 缺失时 |
|---|---|---|---|---|
| NUMA 拓扑 | `numactl --hardware`（节点/CPU/内存清单）；`lstopo`（hwloc，含 I/O 设备挂载位置） | 一次性快照 | 确认节点数、CPU 归属、内存分布 | 不测量就停止，不假设对称 |
| 设备 NUMA 归属 | `/sys/bus/pci/devices/<BDF>/numa_node`（ABI：未知为 -1，初值来自 ACPI _PXM，[L355–L366](https://github.com/torvalds/linux/blob/038d61fd642278bab63ee8ef722c50d10ab01e8f/Documentation/ABI/testing/sysfs-bus-pci#L355-L366)）；NIC 经 `/sys/class/net/<if>/device/numa_node`（AMD 指南 §4.4.1 同款核对手法）；numactl 节点说明符支持 `pci:<BDF>`、`netdev:<if>` | 每设备一次 | 建立 加速器/NIC/NVMe→NUMA 节点 映射 | 读数 -1 表示固件未报告，记录 unknown，不猜 |
| 目标范围与允许集 | 列出训练进程、关键工作线程 TID 和 loader 等子进程 PID；逐 TID 读 `/proc/<pid>/task/<tid>/status` 的 `Cpus_allowed_list`/`Mems_allowed_list`，子进程另读自身路径 | 与负载窗口一致，记录 PID/TID、角色及容器 PID 命名空间 | 确认 CPU 可执行集和内存允许节点集；后者是 `task->mems_allowed`（[cpuset.c L4395–4402](https://github.com/torvalds/linux/blob/038d61fd642278bab63ee8ef722c50d10ab01e8f/kernel/cgroup/cpuset.c#L4395-L4402)），不是 MPOL_BIND/interleave 策略 | `/proc/<pid>/status` 是主线程状态，不能代表全部 TID/子进程；允许集不能证明策略安装 |
| 已安装的任务/VMA 内存策略 | 在实际目标线程内查询 `get_mempolicy`，记录 mode、节点掩码、flags 和地址范围（[L445–454](https://github.com/torvalds/linux/blob/038d61fd642278bab63ee8ef722c50d10ab01e8f/Documentation/admin-guide/mm/numa_memory_policy.rst#L445-L454)）；逐映射核对目标 `numa_maps` 的 policy 标签，和 N0=/N1= 页计数分开（[proc.rst L683–715](https://github.com/torvalds/linux/blob/038d61fd642278bab63ee8ef722c50d10ab01e8f/Documentation/filesystems/proc.rst#L683-L715)） | 与负载窗口一致，分别注明任务或地址策略范围 | 核对 bind/interleave 等是否实际安装；`numactl --show` 仅查询调用者自身，另起查询进程不能读出既有目标线程的策略 | 启动选项只是请求意图；映射策略快照也不证明所有线程策略一致。目标内查询不可取得时标 unknown，不以允许集替代 |
| 线程最近执行位置 | 对关键 TID 多次采样 `/proc/<pid>/task/<tid>/stat` 的 processor 字段（最近执行的 CPU） | 与负载窗口同窗口多次 | 样本跨 NUMA 节点可支持发生过迁移 | 最近执行 CPU 不是连续轨迹；样本未变化不能证明全程无迁移 |
| 进程页实际驻留分布 | `numastat -p <pid>`（按节点给出**该进程**的页分布，numastat(8) `-p` 选项；**注意带选项后显示单位改为 MB**，与默认输出的页不同）；或 `/proc/<pid>/numa_maps`（逐映射的 N0=/N1= 计数，单位为页） | MB（numastat -p）或页（numa_maps）；测量窗口前后取差分 | 验证「局部/远端放置」是否真实发生在被测进程上 | 放置分布 ≠ 访问路径；驻留快照差分不是访问次数；迁移窗口内的分布是动态的 |
| 系统级分配计数（仅背景） | `numastat`（默认系统级）：numa_hit/numa_miss/local_node/other_node（含义见 numastat(8)） | 单位为页；窗口前后差分 | 只作系统背景：这些是**全系统页分配事件计数**，包含其他进程，不能证明被测进程的放置，更不是远端访问计数 | 单独用它下结论 = 证据无效 |
| 内核开关 | `/proc/sys/kernel/numa_balancing`（位掩码：0/1/2 可组合，3 为 NORMAL+MEMORY_TIERING 同开） | 测量全程固定并记录 | 自动迁移会掩盖或转移放置差异 | 未记录则结果不可比 |
| 应用层指标 | step 时间、H2D 传输时间、I/O 等待（按工作负载自带计时） | 与绑定组同窗口 | 判断放置差异是否解释症状 | 只有微观带宽无应用指标时，结论限微观层 |

## 容器与 cpuset 限制（另列）

容器内进程的 NUMA 行为受 cgroup v2 cpuset 约束：`cpuset.cpus` 限定可用 CPU（空值继承最近非空祖先），`cpuset.mems` 限定内存节点（写入非空会把任务内存迁往指定节点，迁移有代价且可能不完全，官方建议先设置再放任务），`cpuset.cpus.partition` 控制独占分区（[docs.kernel.org cgroup-v2](https://docs.kernel.org/admin-guide/cgroup-v2.html)，动态页未标内核版本，2026-10-08 观察）。容器内 numactl/hwloc 看到的是受限视图；宿主机与容器内的拓扑证据要分别记录，不能互推。

## 步骤与判断分支

| 步骤 | 检查或动作 | 运行影响 | 预期证据与解释 | 下一步 |
|---|---|---|---|---|
| 1 | 记录节点拓扑、设备归属、目标 PID/关键 TID/子进程角色；固定 numa_balancing 状态并记录 | 只读 | 得到设备→NUMA 映射、目标范围与开关基线 | 映射缺失（-1）时记录 unknown 并继续，不假设；关键目标无法定位时不作完整进程结论 |
| 2 | 设计两组绑定：局部组 `--cpunodebind X --membind X`；远端组 `--cpunodebind X --membind Y`（Y≠X，numactl(8) 语义：membind 仅从指定节点分配、cpunodebind 限定 CPU 执行节点） | 仅作用于被测进程 | 两组仅内存放置不同，其余一致 | 负载需能从干净状态启动（first-touch 对旧页无效） |
| 3 | 同负载、同缓存/频率状态、同并发下分别运行两组，每组重复多次；按目标范围采集允许集、已安装任务/VMA 策略、关键 TID 最近 CPU 样本及各目标进程的页驻留（`numastat -p <pid>` 或 numa_maps） | 测试负载及目标内策略查询按授权范围 | 允许集容纳所需 CPU/节点、策略与请求一致，且局部组相关工作集主要驻留 X、远端组主要驻留 Y，才支持放置按意图发生；允许集相同不证明策略相同 | 策略未知、线程覆盖不足或驻留与请求矛盾时，不宣称绑定成立；查安装时机、VMA 策略、cpuset 与自动迁移后重测 |
| 4 | 比较两组应用层指标（step 时间/传输时间）的分布，记录重复次数与噪声范围 | — | 记录差异方向与幅度；**不预设局部必然更快**（分支 D）。差异超出噪声 → NUMA 放置是**受支持的候选解释**；未超出噪声 → 只能说**本次对照在该负载/窗口/分辨率下未支持该候选**，不能排除 NUMA（分支 F） | 结论只覆盖已测路径与条件 |
| 5 | 将结论与设备归属交叉：涉及加速器/NIC 时，确认数据传输是否跨 NUMA（如 CPU 在 X、设备在 Y）——注意 CPU—内存、CPU—设备、内存—设备是三条不同路径，分别核对 | — | AMD 指南明确：「Performance will be sub-par if the adapter uses cores and/or memory on the distant socket」（[58012 §4.2](https://docs.amd.com/api/khub/documents/ScFqtjHuoA5CBw6e~hb01Q/content)） | 跨节点时优先把进程/内存迁到设备所在节点再复测 |

判断分支（反例与陷阱）：

- **分支 A：线程迁移**。CPU 亲和约束允许执行集，不移动已有页；线程跨节点后，原先 first-touch 分配的页可能变成远端。逐关键 TID 核对允许集和已安装策略，再对齐最近 CPU 样本、目标进程页驻留及应用指标；主线程的 status 或一个 `numactl --show` 不能代替这些目标证据。各项观测均不能单独证明「迁移导致远端访问」；CPU 样本未变也不证明窗口内从未迁移。处置：CPU 亲和与内存策略成对设置，记录线程覆盖与采样局限。
- **分支 B：NUMA 无感/自动迁移掩盖**。numa_balancing 开启时内核会把热页迁往本地节点，测量窗口内放置是动态的；官方建议已绑定负载关闭该特性。记录开关（位掩码值）是结果可比的前提。
- **分支 C：数据饥饿伪装**。训练 step 变长若主要发生在数据等待，先按[数据饥饿诊断](../04-data-storage/data-starvation-triage.md)区分 loader/传输/消费段；NUMA 只解释其中「主机内存放置影响 H2D/供给」的一段，不能覆盖存储后端原因。
- **分支 D：局部率更高不必然更快**。Gaud 2015 的反例：PCA 负载交织后局部率从 33% 降到 25% 反而更快，因为集中访问单一节点的内存控制器造成拥塞（该研究同时测得拥塞时延迟可达约 1200 cycles）。结论：成对测量是「测量并记录差异」，不是「验证局部一定最优」；interleave 在某些负载下是合理选择。
- **分支 E：设备编号误导**。把「GPU 0 属于 NUMA 0」当默认是常见错误；设备 ordinal 来自驱动枚举，NUMA 归属只能来自 sysfs/hwloc/numactl 的核对结果。
- **分支 F：无差异不等于排除**。两组对照未观察到显著差异，只说明在该负载、窗口、消息/工作集规模、并发与测量分辨率下未支持 NUMA 假设；设备局部性、线程迁移、自动迁移、工作集未达远端惩罚区间、计时分辨率不足都可能掩盖效应。排除结论必须写明已覆盖的条件范围，并按 CPU—内存、CPU—设备、内存—设备三条路径分别限定。

## 停止条件与恢复安排

- 任一组绑定后进程无法启动或内存分配失败（membind 节点内存不足即失败，numactl(8) 语义），停止并记录，改用更大节点集或降低负载。
- 关键 TID/子进程证据缺失、已安装策略未知，或页驻留与请求矛盾且无法解释时，停止完整绑定结论；先排查目标范围、策略安装时机/VMA 范围、cpuset 与自动迁移。可记录已有观测及 unknown，不比较未经确认的局部/远端组。
- 所有绑定与查询均为进程级或只读操作，无系统状态需要恢复；若按现场授权修改过 numa_balancing，测量结束后恢复原值并记录。

## 完成判据

- 设备→NUMA 映射表完整（缺失项标 unknown）；numa_balancing 位掩码值已记录。
- 被测 PID、关键 TID 与子进程的覆盖范围明确；五类证据齐备：各任务允许集、已安装任务/VMA 策略、最近 CPU 样本、目标进程页驻留及应用指标。允许集没有被当作 bind/interleave 策略，主线程没有被当作全部线程；系统级 numastat 只作背景。
- 两组对照的驻留分布证明放置按意图发生，应用层指标差异（含重复次数与噪声范围）已记录方向与幅度；结论措辞为「本次对照支持/未支持 NUMA 候选」，并写明覆盖的负载、窗口与路径范围；不写成「排除 NUMA」。
- 结论写明机型、内核/工具版本、PID/TID 覆盖及窗口；不外推到其他机型。启动命令成功不等于目标策略、工作集放置或性能结论成立，须分别有策略查询、驻留分布和应用指标支持。

## 来源与验证记录

- [Linux v6.16 NUMA Memory Policy](https://github.com/torvalds/linux/blob/038d61fd642278bab63ee8ef722c50d10ab01e8f/Documentation/admin-guide/mm/numa_memory_policy.rst)（固定 commit，行号见正文）、[sysctl numa_balancing](https://github.com/torvalds/linux/blob/038d61fd642278bab63ee8ef722c50d10ab01e8f/Documentation/admin-guide/sysctl/kernel.rst#L701-L725)、[PCI sysfs ABI numa_node](https://github.com/torvalds/linux/blob/038d61fd642278bab63ee8ef722c50d10ab01e8f/Documentation/ABI/testing/sysfs-bus-pci#L355-L366)。
- 同 commit 的 [proc CPU 允许集](https://github.com/torvalds/linux/blob/038d61fd642278bab63ee8ef722c50d10ab01e8f/fs/proc/array.c#L406-L412)、[cpuset 内存允许集](https://github.com/torvalds/linux/blob/038d61fd642278bab63ee8ef722c50d10ab01e8f/kernel/cgroup/cpuset.c#L4395-L4402)、[proc.rst numa_maps](https://github.com/torvalds/linux/blob/038d61fd642278bab63ee8ef722c50d10ab01e8f/Documentation/filesystems/proc.rst#L683-L715)：允许集与策略、策略标签与驻留页数分开解释。
- [numactl(8)](https://man7.org/linux/man-pages/man8/numactl.8.html) 与 [numastat(8)](https://man7.org/linux/man-pages/man8/numastat.8.html)（man7 镜像，上游 2026-08-04 快照）；[hwloc v2.15.0](https://www.open-mpi.org/projects/hwloc/doc/v2.15.0/) 与 [v2.11.2 工具/I/O 章](https://www.open-mpi.org/projects/hwloc/doc/v2.11.2/a00345.php)；[cgroup v2](https://docs.kernel.org/admin-guide/cgroup-v2.html)（动态页）。
- [AMD EPYC 9004 Linux Network Tuning Guide 58012 Rev 1.5](https://docs.amd.com/api/khub/documents/ScFqtjHuoA5CBw6e~hb01Q/content)（NPS 与设备局部性）；[Lameter 2013](https://cacm.acm.org/practice/an-overview-of-non-uniform-memory-access/) 与 [Gaud 2015](https://cacm.acm.org/practice/challenges-of-memory-management-on-modern-n-uma-systems/)（量化示例与成对测量模板，特定机型）。
- 逐条主张与证据定位见[第十三批 NUMA 来源记录](../../docs/research/batch-13-numa-locality-sources.md)。
- 当前验证范围：仅来源核对，未在真实环境执行。
- 待确认：cgroup-v2 固定 commit 行号（docs.kernel.org 动态页）；NVMe numa_node 的专属 ABI 条目（当前为符号链接结构性推断）；Ascend/鲲鹏主机侧 NUMA 官方文档；远端访问带宽（GB/s 级）的可引用数字；各加速器机型的设备→NUMA 实测映射。
