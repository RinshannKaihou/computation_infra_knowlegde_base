---
id: software-stack.host-resource-pressure-and-device-access
title: OS/进程资源压力与设备访问诊断
type: procedure
domain: software-stack
status: draft
platforms: [generic, nvidia, ascend, amd]
source_refs:
  - src.kernel.docs-cgroup-v2-v6.16
  - src.kernel.docs-cgroup-v2-2026-10-08
  - src.kernel.docs-psi-v6.16
  - src.kernel.docs-proc-v6.16
  - src.kernel.docs-sysctl-vm-v6.16
  - src.kernel.docs-sysctl-kernel-v6.16
  - src.kernel.docs-sysctl-fs-v6.16
  - src.kernel.docs-cgroup-v1-devices-v6.16
  - src.kernel.docs-cgroup-v1-cpusets-v6.16
  - src.kernel.proc-cpuset-v6.16
  - src.linux-man-pages.sched-setaffinity-6.19
  - src.linux-man-pages.getrlimit-6.19
  - src.linux-man-pages.open-2-6.19
  - src.linux-man-pages.seccomp-2-6.19
  - src.linux-man-pages.namespaces-6.19
  - src.linux-man-pages.proc-pid-limits-6.19
  - src.systemd.udev-7-2026-08-04
  - src.oci.runtime-spec-v1.3.0
  - src.nvidia.driver-readme-580.105.08
  - src.nvidia.libnvidia-container-v1.20.1
  - src.nvidia.container-toolkit-docs-2026-10-09
  - src.hiascend.mindcluster-docker-runtime-mounts-7.1rc1
  - src.hiascend.mind-cluster-source-v7.0rc1
  - src.hiascend.atlas200ia2-container-install-25.2.0
  - src.hiascend.mindcluster-faq-cpuset-device-cgroup-7.2rc1
  - src.amd.rocm-install-linux-prerequisites-7.2.4
  - src.amd.rocm-docker-7.2.4
  - src.pytorch.dataloader-source-v2.6.0
  - src.kubernetes.device-plugins-v1-32
  - src.vllm-ascend.issue-15920
updated_at: "2026-10-09"
summary: 对主机资源压力与设备访问问题做分层取证：先分开物理内存不足、cgroup 限额与设备侧 OOM，再把设备可见性、访问许可与框架执行能力分列核对，并以单变量隔离对照收尾。
related_ids:
  - software-stack.layers-and-boundaries
  - hardware.numa-memory-and-io-locality
  - cluster-platform.device-resource-chain
  - data-storage.data-starvation-triage
applicability:
  environment_refs: []
  notes: "尚无环境档案；内核机制按 Linux v6.16 固定 commit（038d61fd）文档，man 页按 man-pages 6.19，容器场景按 OCI runtime-spec v1.3.0 与 cgroup v2 前提。目标节点的内核、cgroup 版本、容器运行时与各平台驱动/运行时版本需先记录再套用。"
verification:
  status: not_verified
  evidence_refs: []
  notes: "方法流程未在真实环境执行；本文仅完成来源核对，所有步骤为待验证的诊断框架，不构成执行处方。"
---

# OS/进程资源压力与设备访问诊断

## 目标与触发条件

回答的问题是：「进程慢、被杀、fork/open 失败或看不到/用不了设备，是主机资源压力、限额配置还是设备访问链哪一段造成的」。典型触发：训练或推理进程被 OOM killer 终止、报 `Too many open files`/`Resource temporarily unavailable`、容器内设备节点缺失或打开被拒、绑核后设备工具失效、同节点不同容器表现不一致。

症状不直接等于根因。本文的第一条纪律是**分开三类「内存耗尽」**：物理内存不足（全系统 OOM）、cgroup limit 触达（cgroup 内 OOM）、设备侧 OOM（加速器内存分配失败）——三者的证据位置和处置完全不同，合并判断是常见误诊来源。第二条纪律是**把设备访问拆成三层分列**：节点可见性（mount namespace 里有没有这个节点）、访问许可（cgroup 设备控制器与节点权限）、框架执行能力（驱动用户态库与设备后端能否初始化），任何一层单独成立都不蕴含另外两层（分层归属方法见[主机到模型执行的软件栈分层](layers-and-boundaries.md)）。

## 适用范围与前置条件

- 内核机制固定引用 Linux v6.16 文档（torvalds/linux commit `038d61fd642278bab63ee8ef722c50d10ab01e8f`，经 git.kernel.org 核对 v6.16 tag 指向该 commit）；docs.kernel.org 动态页不作固定引用。man 页按 man-pages 6.19（man7.org 镜像，2026-10-09 观察）为口径。目标节点内核版本不同，字段与默认值可能不同，先记录再套用。
- 容器场景的前提：OCI runtime-spec v1.3.0（2025-11-02 release commit `92249139`）与 cgroup v2。v1/v2 混合挂载的系统上，设备控制器与接口文件的形态不同，诊断前必须先确认挂载的是哪个版本。
- 平台部分（NVIDIA / Ascend / AMD）各按对应版本厂商文档取证，**不提供跨平台万能挂载命令**：三家的设备节点模型、隔离粒度与运行时注入机制不同（见第五节），照抄一个平台的挂载清单到另一个平台是配置错误来源。
- 本文命令以 /proc、cgroupfs 原始路径为基准，不依赖 psutil/bpftool 等工具（bpftool 链未取证，见已知缺口）。写 cgroup 文件、改 sysctl、调亲和属变更操作，需现场授权；文档不授予执行权限。
- 与本文衔接的前置阅读：[NUMA、主机内存与 I/O 局部性的成对验证](../01-hardware/numa-memory-and-io-locality.md)（亲和与 cpuset 交互、允许集与策略的分辨）；[设备资源链](../05-cluster-platform/device-resource-chain.md)（K8s 设备插件到容器运行的链路）；[数据饥饿诊断](../04-data-storage/data-starvation-triage.md)（FD/共享内存耗尽表现为数据等待时的分界）。

## 机制边界：每个旋钮能判断什么、不能判断什么

以下各机制给「能判断什么 / 不能判断什么」。所有行号指向 v6.16 固定 commit。

### cgroup v2 骨架与控制器下发

cgroup v2 由 core 与控制器组成：本节点可用的控制器列在 `cgroup.controllers`，向 `cgroup.subtree_control` 写 `+cpu +memory -io` 逐层下发；受 top-down 约束（子节点不能超出父节点启用的控制器）与 no-internal-process 约束（非根 domain 节点启用控制器后不能留有进程）（[cgroup-v2.rst L443–L454、L487–L520](https://github.com/torvalds/linux/blob/038d61fd642278bab63ee8ef722c50d10ab01e8f/Documentation/admin-guide/cgroup-v2.rst)）。**能判断**：目标层级上某控制器是否已下发（未下发时对应接口文件不存在，这不是故障）。**不能判断**：控制器文件存在不等于限制生效——`memory.max` 默认值就是 `max`（不限）。

每个非根 cgroup 有 `cgroup.events`（`populated`/`frozen`），`cgroup.procs` 列出全部 PID（zombie 不出现）；线程粒度由 `cgroup.threads`/`cgroup.type`（domain/threaded）管理（[L945–L955、L266–L281、L342–L392](https://github.com/torvalds/linux/blob/038d61fd642278bab63ee8ef722c50d10ab01e8f/Documentation/admin-guide/cgroup-v2.rst)）。**不能判断**：`cgroup.procs` 的进程列表不代表资源归属完整——线程可能属于 threaded 子树。

### 内存：memory.max、memory.high、memory.events、memory.oom.group

- `memory.max` 是硬限：「If a cgroup's memory usage reaches this limit and can't be reduced, the OOM killer is invoked in the cgroup」（[L1351–L1359](https://github.com/torvalds/linux/blob/038d61fd642278bab63ee8ef722c50d10ab01e8f/Documentation/admin-guide/cgroup-v2.rst)）。
- `memory.high` 是节流限：「Going over the high limit never invokes the OOM killer」（[L1325–L1337](https://github.com/torvalds/linux/blob/038d61fd642278bab63ee8ef722c50d10ab01e8f/Documentation/admin-guide/cgroup-v2.rst)）。两者可用 O_NONBLOCK 打开以跳过同步回收（[L1339–L1349、L1368–L1378](https://github.com/torvalds/linux/blob/038d61fd642278bab63ee8ef722c50d10ab01e8f/Documentation/admin-guide/cgroup-v2.rst)）。**能判断**：进程被杀（max 路径）与进程变慢但活着（high 节流路径）是两种判据，不能合并。**不能判断**：high 触发的节流不会留下 OOM 记录；且「某些分配不触发 OOM killer」（[L1364–L1366](https://github.com/torvalds/linux/blob/038d61fd642278bab63ee8ef722c50d10ab01e8f/Documentation/admin-guide/cgroup-v2.rst)，可返回 -ENOMEM）——没有 oom_kill 计数不等于内存从未触限。
- `memory.events`（**层级累计**）：`low`（低于 low 边界仍被回收，提示 low 超配）、`high`（被路由进 direct reclaim）、`max`（用量触及 max）、`oom`（达到限额且分配将失败）、`oom_kill`（原文「killed by **any kind of** OOM killer」——任一种 OOM killer 都计入，不限于 memory.max 路径）、`oom_group_kill`；`memory.events.local` 的字段「local to the cgroup i.e. not hierarchical」仅计本级（[L1443–L1491](https://github.com/torvalds/linux/blob/038d61fd642278bab63ee8ef722c50d10ab01e8f/Documentation/admin-guide/cgroup-v2.rst)）。**能判断**：该 cgroup 子树历史上是否发生过触限与击杀。**不能判断**：单读一次绝对值不能定位「这次事故是谁的」。**归因必须把时间窗差分与空间范围分开**：前后差分只消除窗口开始前的累计量，**不消除后代 cgroup 的贡献**——文档明言 file modified 事件可由「an event down the hierarchy」产生（除非挂载时用了 legacy 的 `memory_localevents` 选项，默认含子树计数，[L196–L203](https://github.com/torvalds/linux/blob/038d61fd642278bab63ee8ef722c50d10ab01e8f/Documentation/admin-guide/cgroup-v2.rst)）。父级路径的差分只证明「这个子树里发生过」：反例——父 cgroup 下 A、B 两个子组，窗口内仅 B（非目标）被杀，父级 `oom_kill` 差分照样增长，与目标容器 A 无关。落到单个容器要用**目标身份对应范围**的 `memory.events.local` 差分，或确认目标在叶子/明确后代范围内并结合被杀 PID、cgroup 身份与 OOM 日志交叉核对；`oom_kill` 增长本身也不单独证明 `memory.max` 限额 OOM（任意 OOM killer 都计入），OOM 上下文判定要回到 dmesg 报告与 `max`/`oom` 字段。
- `memory.oom.group=1` 时该 cgroup（含后代）作为不可分割负载整体被杀或都不杀；`oom_score_adj=-1000` 的任务例外永不杀；「If the OOM killer is invoked in a cgroup, it's not going to kill any tasks outside of this cgroup」（[L1425–L1441](https://github.com/torvalds/linux/blob/038d61fd642278bab63ee8ef722c50d10ab01e8f/Documentation/admin-guide/cgroup-v2.rst)）。**这是「cgroup limit OOM 与全局 OOM 分开判断」的直接依据**：cgroup OOM 不越界，反之全局 OOM 也不读 memory.max。

### OOM 的四种「允许内存」上下文与全局开关

OOM killer 的 badness 打分（0 不杀 – 1000 必杀）按「允许内存」占比估算，而「The amount of 'allowed' memory depends on the context in which the oom killer was called」——四种上下文：**cpuset 耗尽 / mempolicy 节点耗尽 / memory（或 swap）limit 触达 / 全系统耗尽**（[proc.rst §3.1 L1736–L1782](https://github.com/torvalds/linux/blob/038d61fd642278bab63ee8ef722c50d10ab01e8f/Documentation/filesystems/proc.rst)）。`/proc/<pid>/oom_score_adj`（-1000 禁用该任务的 OOM 杀）与旧接口 `oom_adj`（-17 等价）；`/proc/<pid>/oom_score` 含 adj 后有效范围 [0,2000]（[§3.2 L1785–L1793](https://github.com/torvalds/linux/blob/038d61fd642278bab63ee8ef722c50d10ab01e8f/Documentation/filesystems/proc.rst)）。**能判断**：同一进程在不同上下文中的被杀顺位不同——这是「物理内存不足 vs cgroup limit」必须分开判断的机制原因。**不能判断**：同一 RSS 在不同上下文中分母不同，`oom_score` 跨上下文不可比，不能用裸分推断「它最容易被杀」。

全局行为由 sysctl 控制（[sysctl/vm.rst](https://github.com/torvalds/linux/blob/038d61fd642278bab63ee8ef722c50d10ab01e8f/Documentation/admin-guide/sysctl/vm.rst)）：`panic_on_oom`=0 杀进程；=1 panic，但 mempolicy/cpuset 限定的节点耗尽只杀进程不 panic；**=2 连 memory cgroup 内 OOM 也整机 panic**；`oom_kill_allocating_task` 非 0 时直接杀触发者、跳过全表扫描；`oom_dump_tasks`=1 时 OOM 输出 pid/rss/oom_score_adj 任务清单；`overcommit_memory`=0/1/2。**诊断含义**：节点 panic 重启而现场没有 OOM 记录时，先查 `panic_on_oom`——=2 会把容器级 OOM 放大成整机事件，症状形态完全不同。

### 进程数与线程数限额

- cgroup pids 控制器：`pids.max` 硬限（默认 `max`）、`pids.current`/`pids.peak`；超限后 fork()/clone() 返回 **-EAGAIN**；`pids.events` 的 `max` 字段计数触限次数；计数对象是 TID（[cgroup-v2.rst L2324–L2381、L243–L249](https://github.com/torvalds/linux/blob/038d61fd642278bab63ee8ef722c50d10ab01e8f/Documentation/admin-guide/cgroup-v2.rst)）。**不能误判**：组织性操作不受限——写入 `cgroup.procs` 可造成 `pids.current > pids.max`（[L2375–L2378](https://github.com/torvalds/linux/blob/038d61fd642278bab63ee8ef722c50d10ab01e8f/Documentation/admin-guide/cgroup-v2.rst)），current 超 max 不等于异常。
- `RLIMIT_NPROC`：按 **real UID** 计数（含线程），超限 fork 返回 EAGAIN，对 CAP_SYS_ADMIN/CAP_SYS_RESOURCE 持有者与 UID 0 不强制；rlimit 是 per-process 属性、线程组共享，fork 继承、execve 保留（[getrlimit(2)](https://man7.org/linux/man-pages/man2/getrlimit.2.html)）。**这是与 cgroup pids 平行的第二条防线**：一个按 UID 合计、一个按 cgroup 合计，排查 EAGAIN 时两条都要查。
- 系统级：`threads-max` 控制 fork 可创建的最大线程数（初始值使线程结构约占可用 RAM 的 1/8，可写上限 FUTEX_TID_MASK=0x3fffffff）；`pid_max` 为 PID 回绕值（[sysctl/kernel.rst L1542–L1555、L1044–L1049](https://github.com/torvalds/linux/blob/038d61fd642278bab63ee8ef722c50d10ab01e8f/Documentation/admin-guide/sysctl/kernel.rst)）。容器内 PID 另受 pid namespace 约束。

### 文件描述符限额（三层分开判）

打开文件失败的 errno 分属不同层（[open(2)](https://man7.org/linux/man-pages/man2/open.2.html) ERRORS 分列）：

- `RLIMIT_NOFILE`（进程层）：超限时 open/pipe/dup 返回 **EMFILE**（「The per-process limit on the number of open file descriptors has been reached」）；软限是内核强制值、硬限是软限上限，非特权进程只能**降低**硬限且不可逆（[getrlimit(2)](https://man7.org/linux/man-pages/man2/getrlimit.2.html)）。
- `/proc/sys/fs/nr_open`（调整限额时的封顶）：把硬 `RLIMIT_NOFILE` 提到 nr_open 之上时 setrlimit 返回 **EPERM**（「tried to increase the hard RLIMIT_NOFILE limit above the maximum defined by /proc/sys/fs/nr_open」）——这是**调限额失败**的 errno，不是打开文件的 errno；nr_open 默认 1048576，「Actual limit depends on RLIMIT_NOFILE」（[sysctl/fs.rst](https://github.com/torvalds/linux/blob/038d61fd642278bab63ee8ef722c50d10ab01e8f/Documentation/admin-guide/sysctl/fs.rst)）。
- 系统级打开文件表（file table）：耗尽时 open 返回 **ENFILE**（「The system-wide limit on the total number of open files has been reached」）；`/proc/sys/fs/file-max` 是内核可分配文件句柄的系统级上限，触限时 printk `VFS: file-max limit <number> reached`；`file-nr` 三值（已分配/未用/上限）是这一层的辅助证据，2.6 起第二值恒 0。

**能判断**：EMFILE 归进程 rlimit 层、ENFILE 归系统级打开文件表——两个打开失败的 errno 各对应明确层；记录时写明**失败的具体系统调用**（open/pipe/dup/setrlimit…），不只记 errno 名。**setrlimit/prlimit 报 EPERM 不能反推唯一原因**：getrlimit(2) ERRORS 分列三种 EPERM——① 非特权进程提高硬限而缺 `CAP_SYS_RESOURCE`；② 把硬 `RLIMIT_NOFILE` 提到 `/proc/sys/fs/nr_open` 之上；③ `prlimit()` 调用者无权设置目标 PID 的限额。反例：请求的新硬限远低于 nr_open，无 `CAP_SYS_RESOURCE` 的进程提高现有硬限同样报 EPERM——判别须结合 resource 种类、原软/硬限、请求值、nr_open 当前值、调用者能力与目标 PID 权限，证据不足保持 unknown。**不能判断**：`file-nr` 第二值恒 0 不是错误（文档明言）；`/proc/<pid>/limits` 里的数值是启动时继承链的结果，改了 shell ulimit 不影响已在跑的进程。**FD 占用的核对方法**：`RLIMIT_NOFILE` 是可分配 FD 编号的上界；当前实际打开的描述符以 `/proc/<pid>/fd` 目录条目为准（[proc.rst §3.13](https://github.com/torvalds/linux/blob/038d61fd642278bab63ee8ef722c50d10ab01e8f/Documentation/filesystems/proc.rst)「List of symlinks to open files」，L2267 起）；`status` 的 `FDSize` 是「number of file descriptor slots currently allocated」——**已分配描述符表槽位，是容量信息，不是当前打开 FD 数**（Table 1-2，L265），不能用 FDSize 对限额求「使用率」。读 `/proc/<pid>/fd` 受权限约束（无权限时目录不可列），且进程并发开关 FD 时读数是采样值（采样竞争），只作时点证据。框架侧症状样例：PyTorch DataLoader 捕获 "Too many open files" 后给出 raise 与 NOTE（提示检查 ulimit、`--shm-size` 等，[dataloader.py L1280–L1320，v2.6.0 固定源码](https://github.com/pytorch/pytorch/blob/v2.6.0/torch/utils/data/dataloader.py)）——报错文本是症状侧证据，限额归因仍回到 `/proc/<pid>/limits` 与 cgroup 层。

### namespace

8 类 namespace（cgroup/ipc/network/mount/pid/time/user/uts）各隔离不同资源；经 clone(2)/unshare(2) 的 CLONE_NEW* 创建，除 user namespace（3.8 起无特权可建）外一般需 CAP_SYS_ADMIN；`/proc/<pid>/ns/*` 符号链接的 st_dev+st_ino 相同即同一 namespace；`/proc/sys/user/max_*_namespaces` 是每用户 namespace 数上限，触限时 clone/unshare 返回 **ENOSPC**（[namespaces(7)](https://man7.org/linux/man-pages/man7/namespaces.7.html)）。**能判断**：容器「建不起来」报 ENOSPC 时，max_*_namespaces 是候选而非磁盘问题。**对设备诊断的关键边界**：mount namespace 隔离挂载表——容器内「设备节点存在与否」由本 mount ns 决定，与是否持有打开权限（cgroup 设备控制器）是两层，必须分列。

### CPU 调度、cpuset 与亲和

- cgroup cpu 控制器：`cpu.stat` 恒报 usage/user/system_usec，控制器启用后另报 nr_periods、nr_throttled、throttled_usec、nr_bursts、burst_usec；`cpu.max` 为 `$MAX $PERIOD` 带宽硬限（默认 `max 100000`，**只作用 fair-class**）；`cpu.weight` 默认 100、范围 [1,10000]；`cpu.pressure` 输出 PSI（[cgroup-v2.rst L1115–L1193](https://github.com/torvalds/linux/blob/038d61fd642278bab63ee8ef722c50d10ab01e8f/Documentation/admin-guide/cgroup-v2.rst)）。**不能判断**：cpu.max 不约束 RT 任务；throttled 计数只覆盖 fair-class 进程——throttled 为零不排除其他调度类被限。
- cpuset 控制器：层级约束（子集不得超过父）；`cpuset.cpus` 空值继承最近非空祖先、**不受热插拔影响**；`cpuset.cpus.effective` 只读、**受热插拔影响**；`cpuset.cpus.partition` 支持 member/root/isolated（isolcpus 的 CPU 需放入 isolated partition）（[L2384–L2453、L2643–L2654](https://github.com/torvalds/linux/blob/038d61fd642278bab63ee8ef722c50d10ab01e8f/Documentation/admin-guide/cgroup-v2.rst)）。**能判断**：请求的 cpus 与实际生效的 effective 可以不同，诊断必须读 effective，不能只核对编排层写下去的值。
- 亲和的「软」边界：`sched_setaffinity(2)` 设的是 per-thread 掩码，实际运行集是「掩码 ∩ 系统实际存在 CPU」的交集，且「The system may further restrict…if the 'cpuset' mechanism…is being used. These restrictions…are silently imposed by the kernel」；fork 继承、execve 保留（[sched_setaffinity(2)](https://man7.org/linux/man-pages/man2/sched_setaffinity.2.html)）。v1 cpusets 文档更明确：「If a task is moved from one cpuset to another…the task will be allowed to run on any CPU allowed in its new cpuset, **negating the effect of the prior sched_setaffinity() call**」；内存放置在下一次分配时更新、CPU 放置立即更新（[cpusets.rst §1.1/§1.3/§1.9](https://github.com/torvalds/linux/blob/038d61fd642278bab63ee8ef722c50d10ab01e8f/Documentation/admin-guide/cgroup-v1/cpusets.rst)）。**这是「改了亲和仍被挪走」类症状的机制解释**：cpuset 变更可静默抵消此前设的亲和。`/proc/<pid>/status` 的 `Cpus_allowed_list` 是亲和与 cpuset 交集后的**结果值**（与 [cpuset.c 源码证据](../01-hardware/numa-memory-and-io-locality.md)互证），读到它不等于知道是谁设置的。更完整的成对验证方法见 [NUMA 局部性一文](../01-hardware/numa-memory-and-io-locality.md)。

### PSI 压力停滞信息

`/proc/pressure/{cpu,memory,io}` 各输出 `some avg10/avg60/avg300/total` 与 `full ...` 两行：some = 至少部分任务停滞的时间占比，full = 所有非 idle 任务**同时**停滞（该状态视为 thrashing）；「CPU full is undefined at the system level…set to zero for backward compatibility」（5.13 起）（[psi.rst Pressure interface 节](https://github.com/torvalds/linux/blob/038d61fd642278bab63ee8ef722c50d10ab01e8f/Documentation/accounting/psi.rst)）。**能判断**：压力存在与否与程度的时间序列（total 为微秒累计，可对自定义窗口求差）。**不能判断**：系统级 cpu full 恒为 0，**不能用 full 判 CPU 压力**；PSI 说「有停滞」不说「谁停滞」。

PSI 触发器：向 /proc/pressure/* 写 `<some|full> <stall us> <window us>` 后用 poll/epoll 等待；窗口 500ms–10s；非特权用户可建触发器但窗口必须是 2s 的整数倍。cgroup2 挂载后每个 cgroup 目录有 `cpu.pressure`/`memory.pressure`/`io.pressure`，语义相同（[psi.rst Monitoring 与 Cgroup2 interface 节](https://github.com/torvalds/linux/blob/038d61fd642278bab63ee8ef722c50d10ab01e8f/Documentation/accounting/psi.rst)）。**关键陷阱**：容器内若挂载的是宿主机 /proc，读到的是系统级而非容器级压力——per-cgroup 压力必须读 cgroupfs 里的 *.pressure，两处不能混用。

## 设备访问机制：可见性、访问许可、执行能力三层

### cgroup 设备控制器：v1 白名单 vs v2 BPF

- **v1**：devices 白名单每条含 type（a/c/b）、major、minor（可 `*`）、access（r/w/m 组合）；`devices.allow` 加、`devices.deny` 删；`echo a > devices.deny` 清空默认全允许；子 cgroup 永不能获得父未授予的访问；拒绝在 open/mknod 时生效（[cgroup-v1/devices.rst §1–§4](https://github.com/torvalds/linux/blob/038d61fd642278bab63ee8ef722c50d10ab01e8f/Documentation/admin-guide/cgroup-v1/devices.rst)）。
- **v2**：「Cgroup v2 device controller has no interface files and is implemented on top of cgroup BPF」——用 BPF_PROG_TYPE_CGROUP_DEVICE 程序挂到 cgroup，访问发生时执行，返回 0 则失败并返回 **-EPERM**；同时管 mknod 与既有节点访问（[cgroup-v2.rst Device controller 节 L2657–L2678](https://github.com/torvalds/linux/blob/038d61fd642278bab63ee8ef722c50d10ab01e8f/Documentation/admin-guide/cgroup-v2.rst)）。

**诊断缺口（如实呈现）**：v2 下**没有可读的文件能枚举设备规则**，只能借助 bpftool 等查已挂 BPF 程序；该工具链本批未取证，v2 上无法从内核侧直接列出允许清单（可回退到编排/运行时层的期望配置做对比，见下）。**EPERM 只是候选层提示，不是根因**：设备控制器拒绝会产生 -EPERM，但 seccomp 同样可以——`SCMP_ACT_ERRNO` 的默认 errno 就是 EPERM（OCI runtime-spec `defaultErrnoRet`「The default is `EPERM`」，[config-linux.md Seccomp 节 L874 起](https://github.com/opencontainers/runtime-spec/blob/92249139eea7161e13745abd4cb6d0ea02a3227a/config-linux.md)），且 seccomp 过滤器可在**系统调用尚未执行时**直接返回 errno（[seccomp(2)](https://man7.org/linux/man-pages/man2/seccomp.2.html)）。v1/v2 并存期诊断必须先确认挂载版本。

### OCI runtime-spec 的三层分离

OCI runtime-spec v1.3.0（[config-linux.md](https://github.com/opencontainers/runtime-spec/blob/92249139eea7161e13745abd4cb6d0ea02a3227a/config-linux.md)）把设备相关配置拆成三层，正好对应本文的三层分列：

1. **`linux.devices`**（[L127–L192](https://github.com/opencontainers/runtime-spec/blob/92249139eea7161e13745abd4cb6d0ea02a3227a/config-linux.md)）：列出容器内必须**可见**的设备（type/path/major/minor/fileMode/uid/gid），运行时可以 mknod 或 bind mount 等方式提供；「Containers MAY NOT access any device node that is not either explicitly referenced in the devices array or listed as being part of the default devices」，默认设备含 /dev/null、/dev/zero、/dev/full、/dev/random、/dev/urandom、/dev/tty、/dev/ptmx（及 terminal 时 /dev/console）。这一层管**节点可见性**。
2. **`linux.resources.devices`**（[L404–L442](https://github.com/opencontainers/runtime-spec/blob/92249139eea7161e13745abd4cb6d0ea02a3227a/config-linux.md)）：配置 allowed device list（按 cgroup v1 语义描述），「The runtime MUST apply entries in the listed order」，字段 allow/type/major/minor/access（rwm 组合）。这一层管 **cgroup 访问许可**。注意：spec 以 v1 语义描述，v2 系统上由运行时转换为 BPF——转换是实现行为，spec 不保证逐条可观测（这正是上节 v2 枚举缺口的来源）。`linux.unified` 允许对 cgroup v2 写任意 key=value（[L713–L734](https://github.com/opencontainers/runtime-spec/blob/92249139eea7161e13745abd4cb6d0ea02a3227a/config-linux.md)）。
3. **`linux.namespaces`**（[L22–L80](https://github.com/opencontainers/runtime-spec/blob/92249139eea7161e13745abd4cb6d0ea02a3227a/config-linux.md)）：type 枚举 pid/network/mount/ipc/uts/user/cgroup/time；指定 path 则加入既有 namespace、否则新建；未列出的类型继承运行时所在 namespace。mount namespace 决定 /dev 视图；user namespace 的 uid/gid 映射影响设备节点属主在容器内的呈现。

第三层「框架执行能力」不在 OCI spec 范围：节点可见且许可放行后，用户态驱动库能否初始化、框架设备后端能否创建上下文，属[软件栈分层](layers-and-boundaries.md)中「OS/驱动 ↔ 平台运行时 ↔ 框架后端」边界的问题，需要平台层证据（日志、初始化返回值）单独判断。

### udev 与节点权限

udev 接收内核 uevent、按规则匹配后用 OWNER/GROUP/MODE 赋值键覆盖编译默认权限；规则目录优先级 `/etc/udev/rules.d` > `/run/udev/rules.d` > `/usr(/local)/lib/udev/rules.d`，同名文件后者被前者替换；设备节点名本身不能被 udev 改名（只能加 SYMLINK）（[udev(7)](https://man7.org/linux/man-pages/man7/udev.7.html)，man7 镜像自 systemd 2026-08-04 快照）。**能判断**：宿主机上节点属主/权限为什么是当前值（查生效规则链）。**不能判断**：节点权限由 udev 规则与驱动默认共同决定，不能凭单一主机经验外推；非 systemd-udevd 环境（如部分容器镜像内）没有 udev，容器内节点权限来自运行时注入时的设置。

## 三平台设备节点与运行时配置（各按文档，无万能命令）

### NVIDIA

- **节点与权限**：用户态驱动组件要求内核模块已加载且设备文件存在——「/dev/nvidiactl 和 /dev/nvidia[0-9]+ 必须存在，且对应用用户有读写权限」；设备文件由用户态组件（或 setuid 的 nvidia-modprobe 兜底）创建，默认 UID=0 GID=0 Mode=**0666**；可用 `NVreg_DeviceFileUID/GID/Mode` 模块参数修改，`NVreg_ModifyDeviceFiles=0` 关闭动态管理（[驱动 README 580.105.08 Ch17B L4329–L4341、Ch7 FAQ L1125–L1173](https://download.nvidia.com/XFree86/Linux-x86_64/580.105.08/README/README.txt)，README 标 "Last Updated: 2025-10-29"）。**诊断含义**：默认 0666 意味着节点权限通常不构成分组隔离，隔离主要落在挂载与 cgroup 两层；发行版机制可能改默认，文档建议优先用发行版机制。
- **节点全集（libnvidia-container v1.20.1 源码口径）**：NV_DEVICE_MAJOR=195；/dev/nvidia%d（per-GPU，minor 来自驱动）、/dev/nvidiactl（minor 255）、/dev/nvidia-modeset（minor 254）、/dev/nvidia-uvm、/dev/nvidia-uvm-tools、/dev/nvidia-caps/nvidia-cap%d、/dev/nvidia-caps-imex-channels/channel%d；lookup_devices 中 nvidiactl 必加，uvm/uvm-tools 与 modeset 分别受 OPT_NO_UVM/OPT_NO_MODESET 控制（[nvc_internal.h 与 nvc_info.c，commit 3e428194，tag v1.20.1](https://github.com/NVIDIA/libnvidia-container/tree/3e428194f8616a81e16834d27365e4a663668533/src)，BSD-3-Clause）。**注意**：源码枚举是注入「全集」，实际注入集合随 driver capabilities（compute/utility/graphics…）与环境变量裁剪；本仓库未运行该工具，不能从清单反推某容器「应该有」哪些节点。
- **Container Toolkit 与 CDI**：组件含 nvidia-container-runtime、nvidia-ctk、nvidia-cdi-hook、runtime hook、nvidia-container-cli、libnvidia-container1；CDI 规格由 nvidia-cdi-refresh systemd 服务生成到 `/var/run/cdi/nvidia.yaml`（v1.18.0 起自动）；**已知限制**：不处理驱动移除与 MIG 重配置（须手动触发刷新）；JIT-CDI 模式在 NVML/WSL2 系统上按容器请求即时生成；MIG 管理需注入 /dev/nvidia-caps/ 节点且容器须持 CAP_SYS_ADMIN（[Container Toolkit index 与 cdi-support，latest 可变页，2026-10-09 观察](https://docs.nvidia.com/datacenter/cloud-native/container-toolkit/latest/cdi-support.html)）。**诊断含义**：hook 注入失败或 MIG 重配置后 CDI 过期，是「节点可见性」失效的厂商承认来源——表现为节点缺失而非权限拒绝。

### Ascend

- **设备集（按产品分表，不可泛化）**：MindCluster 7.1.RC1「Ascend Docker Runtime 默认挂载内容」给出按产品分开的六张表。通用表为 /dev/davinci_X（NPU 设备，X 为 ID）、/dev/davinci_manager、/dev/hisi_hdc、/dev/devmm_svm，加 /usr/local/Ascend/driver/{lib64,include}、/usr/local/dcmi、/usr/local/bin/npu-smi、/var/queue_schedule（需 MindCluster≥6.0.0 且 HDK≥24.1.RC2）；Atlas 200I A2 / 500 A2 表另含 /dev/svm0、/dev/ts_aisle、/dev/upgrade、/dev/sys、/dev/vdec、/dev/vpc、/dev/pngd、/dev/venc、/dev/dvpp_cmdlist、/dev/log_drv 等；以只读方式默认挂载（[表1–表6](https://www.hiascend.com/document/detail/zh/mindcluster/71RC1/clustersched/dlug/mxdlug_appendices_002.html)，经 doc_center 静态镜像读取，双路径说明见已知缺口）。**引用必须带产品限定**，不存在官方「通用最小集」。
- **运行时机制（开源实证）**：Ascend Docker Runtime 是基于 OCI 的 prestart hook，按 `ASCEND_VISIBLE_DEVICES` 挂 NPU 设备、在 host 上配置容器 device cgroup（保证只用指定 NPU）、挂 CANN 运行时库。源码 `runtime/process/process.go` L86–L93 定义 davinci/vdavinci/davinci_manager(/_docker)/devmm_svm/hisi_hdc 设备集；`addDeviceToSpec` **同时**向 `spec.Linux.Devices` 追加节点、向 `spec.Linux.Resources.Devices` 追加 `{Allow:true, Access:"rwm"}`（[gitee ascend/mind-cluster v7.0.RC1，process.go L60–L110/L380–L560](https://gitee.com/ascend/mind-cluster/tree/v7.0.RC1/component/ascend-docker-runtime)，Apache-2.0；该仓库已公告迁往 Gitcode）。这是「可见性与 cgroup 许可由运行时同时写入」的源码实证——两层都由 hook 负责，任何一层写入失败都表现为不同症状。310B 走 16 个管理设备清单 + davinci_manager_docker 回退；`ASCEND_VISIBLE_DEVICES` 为空或 `void` 时不挂设备。**vNPU 注意**：vdavinciN 在容器内重命名为 davinciN（process.go L411–L421），容器内所见编号与宿主机 /dev 名不同属预期，不要按宿主机编号核对。
- **裸机安装的容器挂载口径**：Atlas 200I A2 25.2.0 安装文档列 --device 挂 /dev/davinci_X、/dev/davinci_manager、/dev/devmm_svm、/dev/hisi_hdc；-v 挂 /usr/local/dcmi、npu-smi、driver/lib64、/etc/ascend_install.info、version.info；容器内创建与宿主机驱动运行用户同 gid 的用户；验证命令 `ls /dev | grep davinci*`（[宿主机目录挂载到容器](https://www.hiascend.com/document/detail/zh/Atlas%20200I%20A2/2520/ep/installationguide/Install_54.html)）。**版本陷阱**：该页建议多容器配 `--kernel-memory`，这是依赖 kmem accounting 的 **cgroup v1 时代 knob**，cgroup v2 已废弃该特性（[cgroup-v2.rst「Deprecated v1 Core Features」节 L3117 起](https://github.com/torvalds/linux/blob/038d61fd642278bab63ee8ef722c50d10ab01e8f/Documentation/admin-guide/cgroup-v2.rst)）——按宿主 cgroup 版本分写，不可直接搬用到 v2 系统。
- **历史冲突案例（cpu-manager 重置 device cgroup）**：MindCluster 7.2.RC1 FAQ 记录：K8s `cpu-manager-policy=static` 下 `npu-smi info` 报错——CPU manager reconcile 时 runc update 按容器 cgroup config 重设 device 规则，把 Ascend Docker Runtime 挂载时添加的 cgroup 设备访问权限冲掉；官方措施是改用 Ascend Device Plugin 挂载（`-useAscendDocker=false`）覆盖（[FAQ](https://www.hiascend.com/document/detail/zh/mindcluster/72rc1/clustersched/dlug/dlug_installation_faq_021.html)）。**这是「CPU 绑核与设备权限相互影响、可见性与访问许可分列」的直接案例**——节点还在、权限没了。**时效警示**：案例环境为 Atlas 800 推理服务器 3000 / CentOS 7.6 / K8s 1.12，机制（runc update 重置 device cgroup）在新版 kubelet/runc 上是否仍存在未核证，只能作为「这类交互曾发生、需按现网验证」的历史案例引用。

### AMD

- **节点与权限组**：ROCm GPU 访问默认经 **video** 与 **render** 两个系统组（video 传统管视频设备、render 管 DRM render node）；或用 udev 规则 `KERNEL=="kfd"`（及 `SUBSYSTEM=="drm" KERNEL=="renderD*`）设 MODE=0666 或自定义组 0660；官方提供 amdgpu-insecure-instinct-udev-rules 包（页内引用 30.30.4 驱动仓）（[ROCm install-on-linux prerequisites，docs-7.2.4，页标 2026-02-24](https://rocm.docs.amd.com/projects/install-on-linux/en/docs-7.2.4/install/prerequisites.html)）。**注意**：ROCm 不支持 IGP，IGP 可枚举时用 HIP_VISIBLE_DEVICES 排除也可能崩溃——「看到了不该看的设备」本身可以是故障源。
- **容器透传与隔离粒度**：`--device /dev/kfd`（「The main compute interface, **shared by all GPUs**」）+ `--device /dev/dri`（整目录 = 全部 GPU）；按卡限制用单个 /dev/dri/renderD128 等 render node 与 /dev/kfd 并列传入；MI300X/MI350X 分区模式（DPX/QPX/CPX）下每个分区是一个 render node（CPX 例：renderD128–D136 属第一颗物理 GPU）；容器内用 rocminfo / `amd-smi list` 验证（只枚举透传进来的 GPU）（[ROCm docker 页，docs-7.2.4，页标 2026-06-05](https://rocm.docs.amd.com/projects/install-on-linux/en/docs-7.2.4/how-to/docker.html)）。**诊断含义**：kfd 是全 GPU 共享的单节点——节点可见性层面**无法**按卡隔离 kfd，按卡隔离落在 render node 与运行时层；renderD 编号到物理 GPU 的映射随分区模式变化，不能按固定编号推卡。与 NVIDIA（per-GPU 节点 + caps）和 Ascend（per-chip davinciN + vdavinci 重命名）模型不同，三平台不可共用一张「设备节点—隔离」对应表。

## 需要的证据（分层采集表）

采集纪律：**同一进程 / 容器 / 节点三层，压力、限额、等待与失败时间对齐**——所有快照记录采集时刻，事件类证据（dmesg、events 计数）记录与症状时间窗的先后关系；容器内 /proc 若直挂宿主机 procfs，进程级字段是主机视角，需先经 `/proc/<pid>/cgroup` 与挂载表确认视角（mountinfo 解析文档本批未逐字段核对，见已知缺口）。

| 证据 | 采集位置（固定版本口径） | 用途 | 缺失时如何处理 |
|---|---|---|---|
| 进程内存与描述符 | `/proc/<pid>/status`：VmPeak/VmSize/VmHWM/VmRSS（=RssAnon+RssFile+RssShmem）/VmSwap、FDSize、Threads、SigQ、Cpus_allowed(_list)、Mems_allowed(_list)、voluntary/nonvoluntary_ctxt_switches、Cap*、Seccomp（[proc.rst Table 1-2 L249–L320](https://github.com/torvalds/linux/blob/038d61fd642278bab63ee8ef722c50d10ab01e8f/Documentation/filesystems/proc.rst)）；精确快照用 `/proc/<pid>/smaps`；**当前打开的描述符另读 `/proc/<pid>/fd`**（§3.13「List of symlinks to open files」，L2267 起） | 进程级用量与允许集结果值；FD 占用以 `/proc/<pid>/fd` 为准 | **RSS 类计数为异步维护、可能不精确**（[L244–L247](https://github.com/torvalds/linux/blob/038d61fd642278bab63ee8ef722c50d10ab01e8f/Documentation/filesystems/proc.rst)）——不要用单点 VmRSS 做严格判据；**FDSize 是已分配描述符表槽位（容量信息），不是打开 FD 数**（L265），不作 RLIMIT_NOFILE 使用率判据；`/proc/<pid>/fd` 受权限约束、进程并发开关 FD 时为采样值 |
| 进程限额 | `/proc/<pid>/limits`（逐资源软/硬限与单位，2.6.24 起；[proc_pid_limits(5)](https://man7.org/linux/man-pages/man5/proc_pid_limits.5.html)） | RLIMIT_NOFILE/NPROC 的一手证据位；ulimit 只是 shell 内建对该接口的包装 | 进程已退出时无法回溯，只能查启动方配置；记录 unknown |
| OOM 顺位 | `/proc/<pid>/oom_score`、`oom_score_adj` | 解释「为什么杀它」（结合上下文，见机制节） | 跨上下文不可比，不作横向排序依据 |
| 容器压力与限额 | cgroupfs 目标路径：`memory.current/max/high`、`memory.events.local`（归因用**目标范围**的 `.local` 差分；同路径 `memory.events` 差分只消除窗口前累计、仍含后代贡献，见机制节）、`memory.pressure`、`cpu.stat/max/pressure`、`pids.current/max/events`、`cpuset.cpus.effective`、`cgroup.events`、`io.*` | 容器级触限、节流、击杀计数与压力 | cgroup 路径需先解析；v1/v2 混合挂载分别记录 |
| 节点压力与余量 | `/proc/pressure/{cpu,memory,io}`（系统级；cpu full 恒 0 不可用）、`/proc/sys/fs/{file-nr,file-max,nr_open}`、`/proc/sys/kernel/{threads-max,pid_max}`、`/proc/sys/vm/panic_on_oom` 等 | 全系统资源池状态与全局 OOM 行为基线 | 与容器级分列，不互相替代 |
| 失败事件文本 | dmesg / 内核日志：OOM 报告（`oom_dump_tasks`=1 时含 pid/rss/oom_score_adj 清单）、file-max 触限 printk（`VFS: file-max limit <number> reached`） | 失败时间点与上下文（哪种 OOM、哪个 cgroup） | 日志滚动丢失时记录窗口缺口，不补写推测 |
| 设备三层 | 可见性：容器内 `ls /dev` 对照平台清单（第五节）；许可：打开失败的**准确 errno 与失败的具体系统调用**、设备身份（major/minor、属主/组/mode）、DAC/组权限、设备控制策略（运行时期望配置）、seccomp 配置（OCI `linux.seccomp`；status 的 `Seccomp` 字段为当前模式）与可取得的安全审计证据；执行能力：平台工具（nvidia-smi / npu-smi / rocminfo / amd-smi）在容器内的枚举结果 | 把「看不到」「打不开」「用不了」分开；errno 只作候选层提示（EPERM：设备控制器或 seccomp；EACCES：DAC/组权限方向），单独不作根因 | 三层任一未取证时，结论限定在已覆盖层 |
| 时间对齐 | 症状日志时间戳、events/printk 时间、采集快照时刻、负载窗口 | 把「压力出现→限额触达→等待累积→失败发生」排成一条时间线 | 时钟源不一致（容器内外）先记录偏移再对齐 |

## 步骤与判断分支

| 步骤 | 检查或动作 | 运行影响 | 预期证据与解释 | 下一步 |
|---|---|---|---|---|
| 1 | 固定现场：记录内核版本、cgroup 挂载版本（v1/v2/混合）、目标进程 PID 与其 `/proc/<pid>/cgroup` 路径、容器身份、症状时间窗 | 只读 | 得到后续所有证据的坐标系；版本不明时一切字段解释暂停 | 进 2 |
| 2 | 区分三类内存耗尽：**(a) 物理内存不足**——节点级 `/proc/pressure/memory`、dmesg 全局 OOM 报告（allowed memory 上下文为全系统）；**(b) cgroup limit**——目标路径 `memory.events.local` 差分的 max/oom/oom_kill（`.local` 才是本级计数；同路径 `memory.events` 差分只除窗口前累计、仍含后代贡献，反例见机制节）、dmesg 中 cgroup 上下文 OOM（被杀 PID 与 cgroup 身份须对上目标）、`memory.max` 当前值；`oom_kill` 增长不单独证明 `memory.max` 限额 OOM（任一种 OOM killer 都计入）；**(c) 设备侧 OOM**——框架/驱动分配失败错误（如 NPU 侧已登记的分配失败案例 [vllm-ascend issue 15920](https://github.com/vllm-project/vllm-ascend/issues/15920)：~98K prompt prefill 分配 18.00 GiB 失败与 81K 时静默卡住两种形态，报告者单方归因、维护者未确认）对照 dmesg 与驱动日志 | 只读 | 三类各有独立证据位，落哪类定哪条处置线；注意 `panic_on_oom=2` 会把 (b) 放大成整机 panic（症状形态完全不同）；设备侧 OOM 的内核文档本批未取得（见已知缺口），当前只能以框架/驱动错误 + 主机侧无 OOM 记录做排除法 | 落 (a)→3，落 (b)→4，落 (c)→5，都无法确认→保留 unknown 并进 6 的隔离对照 |
| 3 | 物理内存路径：节点 PSI memory some/full、空闲与回收迹象、全系统 OOM 上下文中的候选清单；交叉核对是否有 cgroup `memory.high` 节流放大（high 只节流不杀，见机制节） | 只读 | 全系统耗尽 + 无限额触达 → 物理容量/超卖问题；`overcommit_memory` 与 `oom_kill_allocating_task` 取值一并记录 | 结论与扩容/限流建议；或回 2 重分 |
| 4 | cgroup 限额路径：`memory.max` 是否收紧、`memory.events` 时序、`memory.oom.group` 是否置 1（整组被杀的解释）、被杀进程 oom_score_adj；**不要**把 high 节流误当 max 击杀，也不要用层级累计值直接归因单容器 | 只读 | 容器内 OOM 不越出该 cgroup（机制节），宿主机其他服务同时段异常应另查全局路径 | 改限额须按变更流程（见步骤 7/8） |
| 5 | 设备路径三层分列：**可见性**——容器内节点是否存在（对照第五节平台清单，注意 Ascend vNPU 重命名、AMD kfd 共享模型、NVIDIA CDI 过期已知限制）；**访问许可**——errno 只作候选层提示：EPERM 可来自 cgroup 设备控制器（v2 BPF 返回 -EPERM）**或 seccomp**（`SCMP_ACT_ERRNO` 默认 EPERM，可在系统调用未执行时返回），EACCES 指向 DAC/组权限方向但**不能单独证明是 udev 规则问题**——联合核对设备身份（major/minor）、节点属主/组/mode、设备控制策略、seccomp 配置与可取得的安全审计证据；v2 下设备规则不可枚举（缺口），对照运行时期望配置（OCI `resources.devices`/`linux.seccomp` 或平台 hook 源码口径）；**执行能力**——平台工具枚举结果、框架后端初始化日志（对照[软件栈分层](layers-and-boundaries.md)的边界表，K8s 侧资源已分配≠容器内可用，见[设备资源链](../05-cluster-platform/device-resource-chain.md)） | 只读 | 三层各过各的证据：节点在但打开被拒（EPERM/EACCES）→ 访问许可分支，再按上列候选逐项收敛（**Ascend cpu-manager 历史案例属此分支**：绑核 reconcile 经 runc update 重置 device cgroup——节点在、权限被冲掉；机制限于 K8s 1.12/CentOS 7.6 历史环境，新版未核）；节点不在 → 挂载/可见性层；两层都通但框架失败 → 执行能力层 | 逐层收敛；需要修复时按平台文档，不套万能命令 |
| 6 | FD/进程/线程限额分支（症状为 EMFILE/ENFILE/EAGAIN/ENOSPC 或 setrlimit 失败时）：读 `/proc/<pid>/limits`；FD 实际占用用 `/proc/<pid>/fd` 条目数核对（受权限约束、采样值），status 的 `FDSize` 只是已分配描述符表槽位（容量信息），不作使用率判据；EAGAIN 分清 RLIMIT_NPROC（按 real UID 合计）与 pids.max（按 cgroup 合计）两条防线；**errno 按层分**——EMFILE=进程 `RLIMIT_NOFILE`、ENFILE=系统级打开文件表（`file-nr`/`file-max` 与 dmesg printk 为该层辅助证据，不是 EMFILE 的含义）、setrlimit/prlimit 报 EPERM 为**三种候选之一**（非特权进程缺 `CAP_SYS_RESOURCE` 提高硬限／硬 `RLIMIT_NOFILE` 超 `nr_open`／`prlimit()` 无权设置目标 PID 限额），按 resource 种类、原软/硬限、请求值、nr_open、调用者能力与目标 PID 权限判别，证据不足保持 unknown；记录失败的具体系统调用（open/pipe/dup/setrlimit…），不只记 errno 名；ENOSPC 在建容器/建 ns 场景查 `max_*_namespaces` | 只读 | 哪层满归哪层；rlimit 硬限非特权只能降不能升（不可逆），修改前记录原值 | 进 7 |
| 7 | **隔离对照设计**：一次只改一项——或改一个限额（如放宽目标 cgroup `memory.max`）、或改一处亲和（cpuset/affinity）、或换最小负载（同进程骨架、最小工作集），其余条件保持；记录改动前值、改动方式、回退步骤。对照口径：同一观察窗内症状是否消失/复现，而不是「跑起来了没有」 | 变更操作，需现场授权；最小负载先验证不给系统加压 | 单变量变化后症状消失且回退后复现 → 该变量为受支持的候选；症状不变 → 排除该单变量（不证明其他变量无辜） | 任何一步触发新的失败（如 OOM、进程无法启动）→ 立即停止并回退 |
| 8 | 收尾：把压力、限额、等待与失败时间在进程/容器/节点三层对齐成一条时间线；结论写明覆盖范围与未排除项 | 只读 | 时间线自洽、三层证据各自落位、unknown 项列出 | 满足完成判据结束 |

判断分支（陷阱）：

- **分支 A：RSS 单点误判**。VmRSS 是异步维护的近似值，文档明言可能不精确；接近限额的走势判断要用多次采样或 smaps 快照，不能用一次读数宣布「没超」。
- **分支 B：层级累计归因错误**。`memory.events` 含后代累计，**同路径前后差分不能排除后代贡献**——反例：父 cgroup 下 A、B 两个子组，窗口内只有 B（非目标）被杀，父级差分的 `oom_kill` 照样增长，与 A 无关。归因用目标范围的 `memory.events.local` 差分，或确认目标为叶子/明确后代范围并结合被杀 PID、cgroup 身份与 OOM 日志；`oom_kill` 增长也不单独证明 `memory.max` 限额 OOM（任一种 OOM killer 都计入，见机制节）。
- **分支 C：容器内 /proc 视角错误**。容器直挂宿主机 procfs 时，status/limits/pressure 全是主机视角；先解析 cgroup 路径与挂载来源再下结论。
- **分支 D：high 与 max 混淆**。`memory.high` 触顶的表现是变慢（direct reclaim 节流），永远不会产生 oom_kill；把它当「OOM」会误诊，把它当「没问题」会漏掉慢性压力。
- **分支 E：亲和被 cpuset 静默抵消**。改了 sched_setaffinity 仍被挪走是机制内行为（cpusets.rst 明言 negating）；读 `cpuset.cpus.effective` 与 status 的 `Cpus_allowed_list` 结果值，不以「我设置了什么」为证据。与 [NUMA 局部性一文](../01-hardware/numa-memory-and-io-locality.md)的允许集/策略分辨互为上下文。
- **分支 F：三层混判**。节点存在（可见性）+ 打开 EPERM（许可）+ 框架初始化失败（执行能力）是三个独立故障位；Ascend 历史案例显示 CPU 绑核能经 runc update 冲掉许可层——「绑核后设备坏了」先查许可层而不是设备层。
- **分支 G：v2 设备规则不可枚举**。cgroup v2 没有 devices.allow/deny 文件可读；「让我看看规则」在 v2 上没有直接答案，只能对照运行时期望配置或等 bpftool 链取证（见已知缺口），不要伪造一个文件路径去读。

## 停止条件与恢复安排

- **变更即记录**：任何限额/亲和修改前记录原值（rlimit 硬限非特权降低不可逆；cgroup 写值即时生效），写明回退命令与责任人；改动触发新失败（进程无法启动、membind 类分配失败、新 OOM）立即停止并回退到记录值。
- **主动测试边界**：写 cgroup 文件、改 sysctl、重启服务、插拔式设备操作均需现场授权与维护窗口，本文不授予执行权限；测试负载从最小集起步，出现节点级 PSI 恶化或目标外进程受影响即停止。
- **证据不足不硬判**：三层证据任何一层无法取得（进程已退出、日志已滚动、v2 规则不可枚举且无运行时配置可查），结论保留 unknown 并列出缺口，不用最上层的报错文本代替根因。
- **panic 现场**：整机 panic（含 panic_on_oom=2 放大场景）后先保全内核日志与转储，再恢复服务；恢复后按 sysctl 基线重新核对全局 OOM 行为配置。

## 完成判据

- 三类内存耗尽（物理 / cgroup limit / 设备侧）各有明确证据落位，或明确记录为 unknown；`panic_on_oom`、`oom_dump_tasks` 等全局行为基线已记录。
- 设备问题按可见性 / 访问许可 / 执行能力三层分列，每层有各自证据；引用的平台节点清单带产品限定与版本。
- 压力、限额、等待与失败时间在进程/容器/节点三层对齐成一条时间线；容器/主机视角已分辨。
- 若做了隔离对照：单变量、前后值与回退步骤齐全，结论措辞为「支持/未支持该候选」，写明覆盖的负载与窗口。
- 所有未排除假设与证据缺口写入记录；不使用「跑起来了」代替根因结论。

## 已知缺口与冲突

- **bpftool / BPF 设备程序枚举链未取证**：cgroup v2 设备规则无文件可读，枚举工具链待后续批次；当前 v2 上许可层判断只能对照运行时期望配置。
- **设备侧 OOM 内核文档缺口**：验收要求「设备 OOM 与物理内存/cgroup limit 分开判断」，但设备侧（如 KFD/amdgpu 显存压力）无对应内核文档条目；现有证据为已登记 NPU 分配失败案例与 ROCm/驱动文档，系统级判据建议另批取证。
- **Ascend FAQ 案例时效**：cpu-manager static 触发 runc update 重置 device cgroup 的案例基于 K8s 1.12 / CentOS 7.6；新版 kubelet/runc 上机制是否仍存在未核证，仅作历史案例。
- **hiascend 双路径取得说明**：document/detail 动态页 2026-10-09 观察返回 cookie 墙，两条 MindCluster 文档（7.1.RC1 挂载表、7.2.RC1 FAQ）经同内容 doc_center 静态镜像读取；未比对两者是否逐字节一致，引用保留动态路径。
- **docs.kernel.org 与固定 commit 口径差**：既有登记 src.kernel.docs-cgroup-v2-2026-10-08 为动态页观察记录；本文一律以 v6.16 固定 commit 为准（两版在本文覆盖字段上内容一致）。
- **man7.org 为滚动镜像**：man 页以 colophon 的 man-pages 6.19 为固定口径；如需不可变引用应改取 kernel.org 的 man-pages-6.19 tarball（未取得）。
- **NVIDIA Container Toolkit 文档无版本化快照**：latest 可变页；不可变对应物取 libnvidia-container 固定 tag（v1.20.1）。
- **/proc/\<pid\>/mountinfo 与 /proc/\<pid\>/cgroup 解析文档未逐字段核对**：容器视角的 cgroup 路径拼接依赖这两个文件，proc.rst §3.5 有 mountinfo 节但本批未核，步骤中的解析动作需补证。
- **AMD 文档版本映射**：ROCm prerequisites 页引用的驱动仓版本（30.30.4）随页面版本变化，引用须带页面版本（docs-7.2.4）。

## 来源与验证记录

- 内核机制（v6.16 固定 commit `038d61fd`）：[cgroup-v2.rst](https://github.com/torvalds/linux/blob/038d61fd642278bab63ee8ef722c50d10ab01e8f/Documentation/admin-guide/cgroup-v2.rst)（controllers/events/cpu/memory/pids/cpuset/device，行号见正文）、[psi.rst](https://github.com/torvalds/linux/blob/038d61fd642278bab63ee8ef722c50d10ab01e8f/Documentation/accounting/psi.rst)、[proc.rst](https://github.com/torvalds/linux/blob/038d61fd642278bab63ee8ef722c50d10ab01e8f/Documentation/filesystems/proc.rst)（OOM 上下文与 status 字段表）、[sysctl/vm.rst](https://github.com/torvalds/linux/blob/038d61fd642278bab63ee8ef722c50d10ab01e8f/Documentation/admin-guide/sysctl/vm.rst)、[sysctl/kernel.rst](https://github.com/torvalds/linux/blob/038d61fd642278bab63ee8ef722c50d10ab01e8f/Documentation/admin-guide/sysctl/kernel.rst)、[sysctl/fs.rst](https://github.com/torvalds/linux/blob/038d61fd642278bab63ee8ef722c50d10ab01e8f/Documentation/admin-guide/sysctl/fs.rst)、[cgroup-v1/devices.rst](https://github.com/torvalds/linux/blob/038d61fd642278bab63ee8ef722c50d10ab01e8f/Documentation/admin-guide/cgroup-v1/devices.rst)、[cgroup-v1/cpusets.rst](https://github.com/torvalds/linux/blob/038d61fd642278bab63ee8ef722c50d10ab01e8f/Documentation/admin-guide/cgroup-v1/cpusets.rst)。
- man 页（man-pages 6.19 口径）：[sched_setaffinity(2)](https://man7.org/linux/man-pages/man2/sched_setaffinity.2.html)、[getrlimit(2)](https://man7.org/linux/man-pages/man2/getrlimit.2.html)、[open(2)](https://man7.org/linux/man-pages/man2/open.2.html)（EMFILE/ENFILE 分列）、[seccomp(2)](https://man7.org/linux/man-pages/man2/seccomp.2.html)（SECCOMP_RET_ERRNO 不执行系统调用即返回 errno）、[namespaces(7)](https://man7.org/linux/man-pages/man7/namespaces.7.html)、[proc_pid_limits(5)](https://man7.org/linux/man-pages/man5/proc_pid_limits.5.html)、[udev(7)](https://man7.org/linux/man-pages/man7/udev.7.html)（systemd 2026-08-04 快照）。
- 容器规范：[OCI runtime-spec v1.3.0 config-linux.md](https://github.com/opencontainers/runtime-spec/blob/92249139eea7161e13745abd4cb6d0ea02a3227a/config-linux.md)（devices / resources.devices / unified / namespaces 四节，行号见正文）。
- 平台：NVIDIA [驱动 README 580.105.08](https://download.nvidia.com/XFree86/Linux-x86_64/580.105.08/README/README.txt)、[libnvidia-container v1.20.1](https://github.com/NVIDIA/libnvidia-container/tree/3e428194f8616a81e16834d27365e4a663668533)、[Container Toolkit cdi-support](https://docs.nvidia.com/datacenter/cloud-native/container-toolkit/latest/cdi-support.html)；Ascend [MindCluster 7.1.RC1 默认挂载内容](https://www.hiascend.com/document/detail/zh/mindcluster/71RC1/clustersched/dlug/mxdlug_appendices_002.html)、[mind-cluster v7.0.RC1 ascend-docker-runtime 源码](https://gitee.com/ascend/mind-cluster/tree/v7.0.RC1/component/ascend-docker-runtime)、[Atlas 200I A2 25.2.0 容器挂载](https://www.hiascend.com/document/detail/zh/Atlas%20200I%20A2/2520/ep/installationguide/Install_54.html)、[MindCluster 7.2.RC1 cpu-manager FAQ](https://www.hiascend.com/document/detail/zh/mindcluster/72rc1/clustersched/dlug/dlug_installation_faq_021.html)；AMD [ROCm prerequisites docs-7.2.4](https://rocm.docs.amd.com/projects/install-on-linux/en/docs-7.2.4/install/prerequisites.html)、[ROCm docker docs-7.2.4](https://rocm.docs.amd.com/projects/install-on-linux/en/docs-7.2.4/how-to/docker.html)。
- 框架与集群侧复用：[PyTorch dataloader v2.6.0 源码](https://github.com/pytorch/pytorch/blob/v2.6.0/torch/utils/data/dataloader.py)（FD 耗尽报错样例）；[Kubernetes v1.32 Device Plugins](https://v1-32.docs.kubernetes.io/docs/concepts/extend-kubernetes/compute-storage-net/device-plugins/)（设备分配链，与[设备资源链](../05-cluster-platform/device-resource-chain.md)衔接）；[vllm-ascend issue 15920](https://github.com/vllm-project/vllm-ascend/issues/15920)（NPU 分配失败案例，报告者单方归因未确认）。
- 逐条主张与证据定位见[第十五批来源记录](../../docs/research/batch-15-host-resource-sources.md)。
- 当前验证范围：仅来源核对；方法流程未在真实环境执行，verification 状态为 not_verified。
- 待确认：bpftool 枚举链、设备侧 OOM 内核文档、Ascend FAQ 机制在新版 runc 的状态、mountinfo/cgroup 解析逐字段、man-pages tarball 固定引用、各平台运行时新版行为。
