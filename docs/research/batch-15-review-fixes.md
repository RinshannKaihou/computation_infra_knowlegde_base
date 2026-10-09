# 第十五批审阅修订记录（B15-C01–C07）

修订日期：2026-10-09。依据：docs/research/batch-15-codex-review.md（gpt-6.1-sol / xhigh 独立审阅，7 项发现：6 P2、1 P3）。修订人：Kimi 子代理。所有修订均重开对应上游核对后落笔（内核 v6.16 固定 commit `038d61fd`、man-pages 6.19、OCI runtime-spec v1.3.0 commit `92249139`、HIP docs-6.3.3、NVSM 25.03 PDF 第 76 页图像、PyPI JSON API 记录）；未执行任何设备操作。

修订后运行 `PYTHONDONTWRITEBYTECODE=1 make check`（PASS：79 个内容条目、277 条来源；两项计数含并行进行的 Batch 16 新增内容，本轮修订自身新增 2 条登记来源、0 个内容条目）与 `make build`（重建 build/catalog）。verification 语义未变化：host-resource 为 not_verified，runtime/compatibility 为 source_checked，node-acceptance 为 not_verified；结论范围未扩大。

## B15-C01（P2）：memory.events 差分与归因分开

**修改位置：**
- knowledge/02-software-stack/host-resource-pressure-and-device-access.md「内存：memory.max、memory.high、memory.events、memory.oom.group」节的 memory.events 条目（原 L83）：分列「时间窗差分」（只消除窗口前累计）与「空间范围归因」（须用目标范围 `memory.events.local` 差分或明确叶子/后代范围 + 被杀 PID/cgroup 身份/OOM 日志）；删除「`.local` 或同路径前后差分」等价表述；补充父级两子组、仅非目标子组被杀的反例；`oom_kill` 引原文「killed by **any kind of** OOM killer」并明确其增长不单独证明 memory.max 限额 OOM。
- 同文「需要的证据」表容器压力行（原 L174）：改为「归因用**目标范围**的 `.local` 差分；同路径 `memory.events` 差分只消除窗口前累计、仍含后代贡献」。
- 同文步骤 2 (b)（原 L185）：改用 `memory.events.local` 差分 + 被杀 PID 与 cgroup 身份对上目标；加 oom_kill 语义限定。
- 同文「判断分支（陷阱）」分支 B（原 L196）：删除「归因用 `.local` 或同路径前后差分」，写入两子组反例。
- docs/research/batch-15-host-resource-sources.md 内核机制表 memory.events 行：同步修正断言，补 L196–L203（memory_localevents legacy 挂载选项，默认含子树计数）。
- sources/registry.yaml src.kernel.docs-cgroup-v2-v6.16 notes：补核记录。

**依据：**Linux v6.16 cgroup-v2.rst @038d61fd L1443–L1491（「all fields in this file are hierarchical and the file modified event can be generated due to an event down the hierarchy」；oom_kill「killed by any kind of OOM killer」；memory.events.local「local to the cgroup i.e. not hierarchical」）、L196–L203（memory_localevents），2026-10-09 重开核对。

## B15-C02（P2）：FDSize 是描述符表槽位容量

**修改位置：**
- host-resource-pressure-and-device-access.md「文件描述符限额」节：新增「FD 占用的核对方法」段——`RLIMIT_NOFILE` 是可分配 FD 编号上界；当前打开描述符以 `/proc/<pid>/fd` 目录条目为准（§3.13「List of symlinks to open files」）；`FDSize` 是「number of file descriptor slots currently allocated」（已分配槽位/容量信息，不是打开 FD 数），不作 RLIMIT_NOFILE 使用率判据；读 `/proc/<pid>/fd` 受权限约束、并发开关 FD 时为采样值。
- 同文「需要的证据」表进程内存与描述符行（原 L171）：FDSize 标注移到「缺失时如何处理」列，加 `/proc/<pid>/fd` 采集位置与限制。
- 同文步骤 6（原 L189）：FD 占用核对改用 `/proc/<pid>/fd` 条目数；FDSize 标为容量信息。
- docs/research/batch-15-host-resource-sources.md 观测接口表 /proc status 行：同步修正。
- sources/registry.yaml src.kernel.docs-proc-v6.16 notes：补核 L265 与 §3.13 L2267 起。

**依据：**Linux v6.16 proc.rst @038d61fd Table 1-2 L265（FDSize 定义）与 §3.13 L2267 起（/proc/<pid>/fd），2026-10-09 重开核对。

## B15-C03（P2）：EMFILE/ENFILE/setrlimit-EPERM 三层分列

**修改位置：**
- host-resource-pressure-and-device-access.md「文件描述符限额」节：改为分层各自 errno——EMFILE=进程 `RLIMIT_NOFILE`（open(2) 原文）；ENFILE=系统级打开文件表（open(2) 原文；file-nr/file-max 与 printk 为该层辅助证据，不是 EMFILE 的含义）；setrlimit/prlimit 报 EPERM=限额调整失败（非打开文件 errno；三种候选原因见第二轮 B15-C08 修正）。加「记录失败的具体系统调用（open/pipe/dup/setrlimit…），不只记 errno 名」。
- 同文步骤 6（原 L189）：「EMFILE 分清三层」改为按 errno 分层表述，症状集加 ENFILE 与 setrlimit 失败。
- docs/research/batch-15-host-resource-sources.md：getrlimit 行补核、新增 open(2) 行、fs.rst 行 errno 映射同步。
- sources/registry.yaml：新登记 src.linux-man-pages.open-2-6.19；src.linux-man-pages.getrlimit-6.19 notes 补核。

**依据：**man-pages 6.19 open(2) ERRORS（EMFILE/ENFILE 分列）、getrlimit(2) ERRORS（「tried to increase the hard RLIMIT_NOFILE limit above the maximum defined by /proc/sys/fs/nr_open」→EPERM），2026-10-09 重开核对。

## B15-C04（P2）：设备打开 errno 改为候选层提示

**修改位置：**
- host-resource-pressure-and-device-access.md「cgroup v2 设备控制器」节诊断缺口段（原 L129 附近）：删除「打开返回 EPERM → 疑似被设备控制器拒绝」的定向判断；改为 EPERM 是候选层提示——设备控制器与 seccomp 均可产生（OCI `defaultErrnoRet`「The default is `EPERM`」；seccomp(2) 可在系统调用未执行时返回 errno）。
- 同文「需要的证据」表设备三流行（原 L177）：许可层证据改为准确 errno 与失败调用、设备身份、DAC/组权限、设备控制策略、seccomp 配置（OCI `linux.seccomp`、status 的 Seccomp 字段）与安全审计证据的联合清单。
- 同文步骤 5（原 L188）：「EPERM 指向 cgroup 设备控制器，EACCES 指向节点权限/udev」改为候选层提示（EACCES 指向 DAC/组权限方向但不能单独证明 udev 问题）；**cpu-manager 历史案例从「节点不在 → 挂载/可见性」括号移到「节点在但打开被拒 → 访问许可」分支**，保留「限于 K8s 1.12/CentOS 7.6 历史环境、新版未核」限定。
- docs/research/batch-15-host-resource-sources.md 设备访问机制表：v2 设备控制器行加逆向不成立说明；新增 seccomp errno 语义行。
- sources/registry.yaml：新登记 src.linux-man-pages.seccomp-2-6.19；src.oci.runtime-spec-v1.3.0 notes 补核 Seccomp 节。
- 正文 frontmatter source_refs 增补 open(2)/seccomp(2) 两条。

**依据：**OCI runtime-spec v1.3.0 config-linux.md @92249139 Seccomp 节 L874 起（defaultErrnoRet 与 syscalls[].errnoRet 默认 EPERM）、seccomp(2) SECCOMP_RET_ERRNO（「without executing the system call」），2026-10-09 重开核对。

## B15-C05（P2）：hipStreamDestroy 不扩写为命令随队列删除

**修改位置：**
- knowledge/02-software-stack/runtime-execution-and-library-loading.md「同步与错误语义」节 stream 段（原 L214）：删除「允许 in-flight 命令随队列删除」推断；按上游原文记录两种销毁时机（队列可在仍有 in-flight 命令时被销毁，或等全部命令完成后销毁）；明确该段不建立任务取消保证、不能据此认为缓冲区可安全释放；加「销毁/同步/资源释放是三个概念」的定向复核说明。
- 同文「各栈平台差异」表 Stream 销毁行（原 L227）：HIP 格改为「两种可能 + 无任务取消保证」。
- docs/research/batch-15-runtime-library-sources.md HIP Stream 行与「API 不等价点」第 (4) 条：同步修正，并记录销毁/同步/资源释放三概念的定向复核结果（CUDA/HIP/CANN 各自承诺面）。

**依据：**HIP docs-6.3.3（页头 6.3.42134）Stream management → hipStreamDestroy 原文，2026-10-09 重开核对（原文与既有引文逐字一致；修正的是引文后的概括）。

## B15-C06（P2）：NVSM 示例图补核

**修改位置：**
- knowledge/01-hardware/node-acceptance-triage.md「验收测试工具前提汇总」NVSM 行（原 L105）：分列「§3.8.4 正文泛述」（组件清单）与「示例中的机型限定」（印刷页 70 / PDF 第 76 页示例截图：NIC 压测「only available on DGX-1, DGX-2, and Luna Systems」、非支持平台「results for this component will be blank」、示例表 NIC 为 SKIPPED）；当前具体机型 NIC 压测支持保持 unknown，DGX H100/H200 quickstart 不能补足；`--no-prompt` 对确认提示的作用标为已取得说明（示例原文「(Pass --no-prompt option in command next time to suppress this prompt)」），不推导完整行为与 `--force` 含义；DURATION 单位继续 unknown。
- 同文「适用范围」缺口声明（原 L53）、「来源与验证记录」NVSM 条（原 L150）、「待确认」（原 L155）与 frontmatter verification notes（原 L36）：同步更新。
- docs/research/batch-15-node-acceptance-sources.md NVSM 行、缺口节、实际读取清单第 8 条：更新为「含图像核验」，附取得方式（600 DPI 渲染 + OCR）。

**依据：**NVSM User Guide Release 25.03 PDF（623,444 字节，署期 2026-07-13）第 76 页（印刷页 70）示例截图，2026-10-09 下载后 600 DPI 渲染并 OCR 核验（与审阅者提供的图像结论一致：NIC 机型限定、--no-prompt 提示跳过说明、NIC=SKIPPED）；DURATION 单位在正文与图像中均未出现。

## B15-C07（P3）：wheel 索引身份分层表述

**修改位置：**
- knowledge/02-software-stack/compatibility-evidence.md「来源与更新范围」末条（原 L203）：「本轮没有固定 wheel 文件名、构建标记、摘要……」改为分层——**已取得（索引声明层面）**：六个 wheel 的完整文件名、平台标签与索引 sha256（PyPI JSON API，2026-10-09）；**未取得**：下载字节摘要比对、wheel `METADATA`、构建 commit/ABI 身份（abi1 变体无独立清单）、CANN 8.3.RC1 精确驱动/固件配套页、本地整栈实测。与 ascend-documented-profile.md 的清单状态一致。
- 同文「决策表」首行附加条件列：由「实际 wheel 文件、架构、ABI 和摘要为 unknown」改为同样的分层表述（索引层身份已取得；未选择部署 wheel、下载字节与构建身份 unknown）。
- docs/research/batch-15-profile-intersection-sources.md 无需修正（其制品身份表与缺口第 8 条本就区分「索引声明 sha256 已取得、未下载比对」，本次仅使 compatibility-evidence.md 与之对齐）。

**依据：**PyPI torch-npu 2.6.0.post3 JSON API（六个 wheel 及索引 sha256，2026-10-09 取得，见 batch-15-profile-intersection-sources.md 制品身份表）；ascend-documented-profile.md「发行包声明」节既有清单。

## 新登记来源与验证

- sources/registry.yaml 新增：src.linux-man-pages.open-2-6.19（open(2) EMFILE/ENFILE）、src.linux-man-pages.seccomp-2-6.19（SECCOMP_RET_ERRNO）；扩展 src.kernel.docs-cgroup-v2-v6.16、src.kernel.docs-proc-v6.16、src.linux-man-pages.getrlimit-6.19、src.oci.runtime-spec-v1.3.0 的核对 notes。
- 审阅报告中「关闭发现后还应补充可独立读取的动态上游正文」属后续批次工作，不在本轮 7 项修订范围内。
- 验证：`PYTHONDONTWRITEBYTECODE=1 make check` PASS（79 个内容条目、277 条来源；含并行 Batch 16 的新增，本轮新增 2 条登记来源）；`make build` 重建 build/catalog.json 与 catalog.md 正常。

## 第二轮（定向复核后，2026-10-09）

依据：docs/research/batch-15-codex-recheck.md（gpt-6.1-sol / xhigh 定向复核：初审 7 项中 6 项 CLOSED、B15-C06 因独立图像取证未完成 OPEN，另引入 B15-C08/P2）。复核会话独立运行 `make check` PASS（80 个内容条目、277 条来源，为当时工作树整体计数）。

### B15-C08（P2）：setrlimit/prlimit 的 EPERM 不反推唯一原因

**问题（复核报告）：**第一轮把「EPERM（setrlimit/prlimit）」写成「=硬限被 nr_open 封顶」的反向等号，把一个可能原因当成唯一诊断结果；getrlimit(2) ERRORS 实分列三种 EPERM。

**修改位置：**
- knowledge/02-software-stack/host-resource-pressure-and-device-access.md「文件描述符限额」节能判断段（约 L108）：改为候选原因分列——① 非特权进程提高硬限而缺 `CAP_SYS_RESOURCE`；② 把硬 `RLIMIT_NOFILE` 提到 `/proc/sys/fs/nr_open` 之上；③ `prlimit()` 调用者无权设置目标 PID 的限额。补「低于 nr_open 但无权提高硬限」反例；判别须结合 resource 种类、原软/硬限、请求值、nr_open 当前值、调用者能力与目标 PID 权限，证据不足保持 unknown。
- 同文步骤 6（约 L193）：「setrlimit/prlimit 报 EPERM=硬限被 `nr_open` 封顶」改为「三种候选之一」并列出判别输入与 unknown 保持。
- 本文档第一轮 B15-C03 节（原 L33 附近）：同步删除「=硬限被 nr_open 封顶」表述，指向本节。
- docs/research/batch-15-host-resource-sources.md getrlimit 行与修订记录、sources/registry.yaml src.linux-man-pages.getrlimit-6.19 notes：同步为三种 EPERM 分列（原 notes 只记了前两种，与正文不一致的问题一并修正）。

**依据：**man-pages 6.19 getrlimit(2) ERRORS 三条 EPERM 原文（「An unprivileged process tried to raise the hard limit; the CAP_SYS_RESOURCE capability is required」／「tried to increase the hard RLIMIT_NOFILE limit above the maximum defined by /proc/sys/fs/nr_open」／「(prlimit()) The calling process did not have permission to set limits for the process specified by pid」），2026-10-09 重开核对。

### B15-C06（P2，证据链边界）：第 76 页图像内容标注为编写者核对记录

**问题（复核报告）：**复核会话图像调用失败，未能判读 NVSM 25.03 PDF 第 76 页（印刷页 70）示例截图，无法独立核验来自该图像的引文与结果表；该项 OPEN 属取证阻塞，非正文技术错误。

**修改位置：**
- knowledge/01-hardware/node-acceptance-triage.md「验收测试工具前提汇总」NVSM 行（约 L105）：来自该图像的三项内容（NIC 压测 DGX-1/DGX-2/Luna 机型限定与非支持平台结果说明、`--no-prompt` 提示作用、示例结果表 NIC=SKIPPED）统一标注为「编写者对官方 PDF 图像页的核对记录（600 DPI 渲染 OCR），独立审阅者会话图像调用失败、未能判读该页图像，未独立核验」；PDF URL 与页码（第 76 页/印刷页 70）保留以便后续独立复核。
- 同文缺口声明（约 L53）、来源与验证记录 NVSM 条（约 L150）、待确认（约 L155）、frontmatter verification notes（约 L36）：同步标注证据链边界。
- docs/research/batch-15-node-acceptance-sources.md NVSM 行、缺口节、实际读取清单第 8 条、修订记录：同步，并如实记录「初审报告曾引该图像并给出同向结论，二轮复核未能重演」。
- sources/registry.yaml src.nvidia.nvsm-user-guide-25.03 notes：补记 §3.8.4 正文核对与图像证据链边界。

**依据：**docs/research/batch-15-codex-recheck.md（复核会话「第 76 页截图调用未返回本会话可判读的图像」）；Batch 13/14 对无法独立核验附件的既定标注先例（如 bmc-firmware-and-events.md 的「编写者核对记录、未独立核验」限定）。DURATION 单位与 `--force` 语义继续 unknown；当前具体机型 NIC 压测支持继续 unknown；不据此建立处置规则。

### 第二轮验证

`PYTHONDONTWRITEBYTECODE=1 make check` PASS（80 个内容条目、277 条来源，当前工作树整体计数）。verification 语义未变化，无结论扩大。
