# 第十五批审阅记录（gpt-6.1-sol / xhigh）

审阅日期：2026-10-09。审阅者：Codex 会话，模型 gpt-6.1-sol，reasoning effort xhigh（用户当前约定）；正文编写者：Kimi（主会话），取证与撰写：探索/撰写子代理。审阅输出全文照录如下。

---
# Batch 15 独立技术审阅报告

**结论：暂不通过。** 本次发现 **6 项 P2、1 项 P3** 问题，涉及资源计数、错误归因、运行时销毁语义、工具适用范围和证据状态一致性。另有部分上游正文未能取得，不能将这些部分记为独立核验通过。

## 审阅记录

- **审阅日期：**2026-10-09，Asia/Shanghai。
- **模型 / effort：**用户约定为 `gpt-6.1-sol / xhigh`。本会话未暴露可核验的实际模型及 effort 运行元数据，因此这里如实记录约定配置，不声称已独立确认实际执行配置。
- **角色：**独立审阅者；未参与 Kimi 主会话及其子代理的正文编写。
- **操作边界：**只读审阅，未修改仓库，未执行设备初始化、诊断、压测、安装或固件操作；按要求跳过 `make build`。
- **结构检查：**运行 `PYTHONDONTWRITEBYTECODE=1 make check`，结果为 **PASS：77 个内容条目、210 条来源**。这证明结构与引用检查通过，不证明技术正确性或硬件兼容性。

## 已完成核对范围

已阅读八个交付文件、四份 Batch 15 取证记录，并对照 `README.md`、作者指南、内容边界、元数据 schema，以及 `plans/full-coverage-backlog.yaml:4193` 起的四项任务要求。取证记录仅用于定位主张与来源，没有替代独立上游核查。

| 范围 | 已完成的独立核对 |
|---|---|
| T01-09 节点验收 | 环境身份、证据接入、复测和回服方法；OCP 环境与历史字段；SuperBench 方法与适用边界；DCGM 文档中的退出码、测试级别及部分前提；GPU Node Triage 的基线与 RMA 边界；ascend-dmi 静态正文的参数、耗时、业务影响及 PRBS 冲突；NVSM §3.8.4 文本及示例图像 |
| T02-01 主机资源 | Linux v6.16 的 cgroup、PSI、proc、OOM/sysctl、cpuset 文档及相关固定 commit；man-pages 6.19 的限额和错误语义；OCI v1.3.0 的设备与 seccomp 字段；udev 规则；NVIDIA 580.105.08 FAQ、libnvidia-container 固定源码中的设备路径常量、CDI 文档；ROCm 7.2.4 prerequisites/docker 页面 |
| T02-02 运行时与库装载 | CUDA 12.8 PG、Runtime/Driver API 的初始化、同步及错误边界；HIP docs-6.3.3、ROCR；可取得的 cuBLAS、NCCL、cuDNN、rocBLAS、RCCL 职责页；`ld.so`、`ldd`、`proc_pid_maps`；固定 commit 的 CUDA vectorAdd、HIP saxpy/streams 示例；CANN `aclFinalize` 正文 |
| T02-03 配套交集 | TorchNPU 固定 README 配套表；PyPI 2.6.0.post3 六个 wheel 的文件名、平台标签、上传日期和索引 SHA-256；NGC PyTorch 25.01 release notes、Support Matrix 的可取得内容；CUDA forward/minor compatibility；ModelZoo 旁证及正文的 unknown/blocked 保留情况 |
| 元数据与导航 | frontmatter、ID 唯一性、`source_refs`、`related_ids`、内部引用和索引入口；检查发现的证据状态矛盾另列 B15-C07 |

## 声明的未覆盖项

以下项目**不计为独立核验通过**，也不因未取得正文直接判定作者主张错误：

- **CANN 8.2.RC1.alpha001 API 页组：**除实际取得正文的部分外，多数重开请求仅返回门户壳或超时。初始化次数、Device/Context 引用关系、Stream/Event 数量上限、查询枚举、错误接口及示例流程未完成逐条独立核验；页面标题和 URL 中的版本字符串不能代替正文。
- **昇腾配套及容器资料：**MindCluster 六类产品挂载表、历史 FAQ、Gitee hook 实现，以及 CANN 8.3.RCX、TorchNPU 7.2.0 安装/兼容性动态页，未完成全部正文及字段的独立复核。因此不确认精确 HDK 交集或 Python 微版本上限已经闭合。
- **其他取得限制：**MIOpen 对应职责页返回 HTTP 429；NERSC-10 v6.0 完整 PDF 返回 HTTP 403，只取得官方索引中的部分 Appendix A 内容；NGC catalog 的历史 build 身份未独立确认。Support Matrix 的复杂跨列归属、DCGM 全部 SKU 配置和插件实现、SuperBench Table 2 未逐项完成。
- **制品及现场验证：**未下载 wheel 比对实际字节摘要或 `METADATA`，未取得容器 manifest digest，未验证任何具体硬件/软件组合。T01-09 的真实环境缺口仍由授权验证轨道关闭。

---

## 发现列表

### B15-C01 — P2：前后差分不能替代非层级计数完成容器归因

**位置：**  
`knowledge/02-software-stack/host-resource-pressure-and-device-access.md:83`  
`knowledge/02-software-stack/host-resource-pressure-and-device-access.md:174`  
`knowledge/02-software-stack/host-resource-pressure-and-device-access.md:185`  
`knowledge/02-software-stack/host-resource-pressure-and-device-access.md:196`

**问题：**正文多次把“`.local` 或同路径前后差分”写成等价归因方法。差分只消除时间窗前的累计量，**不会消除后代 cgroup 的贡献**。父目录的 `memory.events` 即使取差分，仍可能仅反映另一个子 cgroup 的事件。

此外，`oom_kill` 统计的是该范围内被任意 OOM killer 杀死的进程，不能仅凭它增长判断发生了 `memory.max` 限额 OOM。

**证据与精确定位：**Linux v6.16，`Documentation/admin-guide/cgroup-v2.rst`，固定 commit `038d61fd642278bab63ee8ef722c50d10ab01e8f`，`memory.events` / `memory.events.local` 段，源码约 1441–1495 行。官方文档明确说明前者为层级计数，后者才是本级事件；`oom_kill` 包含任意类型 OOM killer。citeturn174333view0

**关闭条件：**
- 将“时间窗差分”和“空间范围归因”分开说明。
- 使用目标身份对应范围的 `.local` 差分，或明确叶子 cgroup／后代范围并结合被杀 PID、cgroup 和 OOM 日志。
- 删除“同路径差分即可排除后代贡献”的表述；补充“父级两个子组、仅非目标子组被杀”的反例进行定向复核。

### B15-C02 — P2：把 `FDSize` 当作已打开 FD 用量

**位置：**`knowledge/02-software-stack/host-resource-pressure-and-device-access.md:189`

**问题：**步骤 6 要求读取 status 的 `FDSize/Threads`“对照使用率”。其中 `FDSize` 是已分配的描述符表槽位数，不是当前打开的 FD 数。用它判断 `RLIMIT_NOFILE` 使用率，会将表容量误当实际占用。

**证据与精确定位：**Linux v6.16 `Documentation/filesystems/proc.rst`，Table 1-2 的 `FDSize` 行；官方定义为当前已分配的 file descriptor slots。相同文档将 `/proc/<pid>/fd` 定义为包含进程文件描述符的目录。citeturn772184view0

**关闭条件：**
- 将 `FDSize` 明确标为描述符表容量信息，不用作打开 FD 数或限额利用率。
- 用 `/proc/<pid>/fd` 等实际描述符证据核对占用，并记录权限及采样竞争限制。
- 对 `RLIMIT_NOFILE` 保留“可分配 FD 编号上界”的准确语义，不把容量比值直接作为触限判据。

### B15-C03 — P2：将系统级 `file-max` 放入 `EMFILE` 归因分支

**位置：**`knowledge/02-software-stack/host-resource-pressure-and-device-access.md:189`

**问题：**“EMFILE 分清 RLIMIT_NOFILE / nr_open / file-max 三层”混合了不同调用阶段和错误码。打开文件时的进程描述符限额对应 `EMFILE`，系统级打开文件表耗尽对应 `ENFILE`；`nr_open` 则限制提高 `RLIMIT_NOFILE` 硬限的上界，相关设置失败可返回 `EPERM`。

这不是措辞偏好，而是会改变错误码对应的诊断路径。

**证据与精确定位：**man-pages 6.19，`open(2)` 的 ERRORS：`EMFILE` 与 `ENFILE` 分列；`getrlimit(2)` 的 ERRORS：硬 `RLIMIT_NOFILE` 超过 `/proc/sys/fs/nr_open` 时返回 `EPERM`。citeturn513416view0turn271554view0

**关闭条件：**
- 将 `EMFILE`、`ENFILE` 和调整限额时的 `EPERM` 分开。
- 保留 `file-nr/file-max` 与 printk 的系统级辅助证据用途，但不把它们写成 `EMFILE` 的直接含义。
- 在分支中记录失败的具体系统调用，而不只记录 errno 名称。

### B15-C04 — P2：设备打开 errno 被写成唯一根因

**位置：**`knowledge/02-software-stack/host-resource-pressure-and-device-access.md:188`

**问题：**正文写“EPERM 指向 cgroup 设备控制器，EACCES 指向节点权限/udev”，随后又写“节点在但 EPERM → cgroup 许可层”。设备控制器拒绝可以产生 `EPERM`，但逆向推断不成立：seccomp 也可在系统调用尚未执行时返回该 errno。`EACCES` 也不能单独证明问题由 udev 规则造成。

同一行还把“cpu-manager 重置 device cgroup”的历史案例放进“节点不在 → 挂载/可见性”括号，混淆了**节点存在但访问被拒绝**与节点缺失。

**证据与精确定位：**OCI runtime-spec v1.3.0，`config-linux.md` 的 Seccomp / `defaultErrnoRet`：`SCMP_ACT_ERRNO` 可指定 errno，默认是 `EPERM`；`seccomp(2)` 的 `SECCOMP_RET_ERRNO` 明确说明可不执行系统调用而返回 errno。citeturn697817view0turn772184view2

**关闭条件：**
- 改为候选层提示，不以 errno 单独宣布 cgroup 或 udev 根因。
- 联合检查设备身份、DAC/组权限、设备控制策略、seccomp，以及可取得的安全审计证据。
- 将 cpu-manager 案例归入访问许可分支；明确其历史版本限制。

### B15-C05 — P2：将 HIP 队列销毁扩写成命令随队列删除

**位置：**  
`knowledge/02-software-stack/runtime-execution-and-library-loading.md:214`  
`knowledge/02-software-stack/runtime-execution-and-library-loading.md:227`

**问题：**原文引用后总结为“允许 in-flight 命令随队列删除”。上游允许的是**队列在仍有 in-flight 命令时被销毁，或等待全部命令后销毁**，没有在该段保证 in-flight 命令被取消、删除或不再执行。正文把队列生命周期扩写成任务取消语义，可能误导资源释放和故障处理。

**证据与精确定位：**HIP docs-6.3.3、页头版本 6.3.42134，Stream management → `hipStreamDestroy`，约 192–200 行；关键限定为队列可在命令仍 in-flight 时销毁，也可能等待命令完成。citeturn269795view0

**关闭条件：**
- 删除“命令随队列删除”的推断，准确保留上游两种队列销毁可能。
- 明确该段不建立任务取消保证，也不能据此认为缓冲区可安全释放。
- 更新平台差异表及取证记录中的同义概括，并定向复核销毁、同步、资源释放三个概念。

### B15-C06 — P2：NVSM 示例图中的适用限制与参数说明遗漏

**位置：**  
`knowledge/01-hardware/node-acceptance-triage.md:105`  
`knowledge/01-hardware/node-acceptance-triage.md:150`  
`knowledge/01-hardware/node-acceptance-triage.md:155`

**问题：**正文依据 §3.8.4 抽取文本概括包含网卡测试，并将 `--no-prompt` 语义记为未明示。但同节示例是图像，补核发现：

- NIC 压测附有 **DGX-1、DGX-2、Luna** 的机型限制。
- 交互提示已说明可以使用 `--no-prompt` 跳过该提示。

示例中的历史限制不宜直接当作当前全部机型的最终支持矩阵，但也不能完全遗漏后，用宽泛组件清单描述覆盖。相邻 DGX H100/H200 quickstart 不能补足 NIC 支持证明。

**证据与精确定位：**NVSM User Guide Release 25.03，§3.8.4，**印刷页 70、PDF 第 76 页**示例截图；NIC 测试说明和交互提示行。该信息不在普通正文抽取结果中。citeturn1view0

**关闭条件：**
- 分列 §3.8.4 正文的泛述与示例中的机型限定；未取得当前具体机型 NIC 支持证据前保持 unknown。
- 将 `--no-prompt` 对该交互提示的作用标为已取得说明，不推导其完整行为或 `--force` 的含义。
- **继续保留 `DURATION` 单位 unknown**；本次图像核查仍未建立其单位。
- 更新取证记录，明确包含图像核验，而非仅 pdftotext。

### B15-C07 — P3：已取得的 wheel 索引身份仍被列为完全缺失

**位置：**`knowledge/02-software-stack/compatibility-evidence.md:203`

**问题：**末尾称“本轮没有固定 wheel 文件名、构建标记、摘要……”。但本页第 113 行已经记录六个 wheel 的索引身份，`ascend-documented-profile.md:73` 起列出完整文件名及 SHA-256。这会把**索引声明已取得**与**实际字节／构建来源未核验**混为一类缺口。

**证据与精确定位：**PyPI `torch-npu` 2.6.0.post3 的 Release files / 各 wheel Details，共六个发行文件及 SHA-256，与正文表一致；这仅确认索引声明，不确认下载字节或构建 commit。citeturn459903view0

**关闭条件：**
- 将待确认项改为实际未取得的层次，例如下载字节摘要、wheel `METADATA`、构建 commit/ABI 身份、精确驱动固件交集及本地验证。
- 保留“文件名与索引 SHA-256 已取得、内容未下载核验”的明确状态。

## 无发现项

以下仅表示**在已完成核对范围内没有发现问题**：

- **结构检查通过：**未发现本批 ID 重复、无效 `source_refs/related_ids` 或失效内部文件引用；软件栈索引包含新增两篇入口。
- **真实环境边界保留：**`node-acceptance-triage.md:111` 与 `node-acceptance-triage.md:154` 没有伪造现场档案，也没有用方法交付关闭 01.6-G3 或冒充 V08 验证。
- **NVIDIA 冲突没有被抹平：**R545 前后冲突、Python 3.12 与源码路径 `python3.10` 的矛盾仍被明确保留；上游 25.01 release notes 确有这些冲突。citeturn702112view0
- **Ascend 精确交集仍阻塞：**没有将 HDK 系列通配或 ModelZoo 的 8.3.RC2 旁证改写成 8.3.RC1 精确驱动/固件支持证明；ModelZoo 表不能填补这一交集。citeturn678507view3
- **Batch 14 重点边界：**DCGM 226/205 未被改写成启动失败或直接硬件根因；ascend-dmi 的 `-st`、`--sc` 范围和 PRBS 原文矛盾在已核对处保留。citeturn863874view1turn230290view0turn753484view0
- **iBMC 标注：**本批 node-acceptance 正文未直接重述具体 iBMC 告警码；其关联 BMC 条目保留“编写者核对记录、未独立核验”限定。此次未据此建立新的处置规则。
- **验证强度未升级：**文档核对、索引身份、官方样例与本地硬件复现仍分开记录，没有将 `source_checked` 写成整栈验证通过。

## 最终结论与复核要求

**暂不通过。** 结构检查已通过，但 B15-C01 至 B15-C06 会影响诊断正确性或证据适用边界，需要修订后定向复核；B15-C07 需要同步修正证据状态。

关闭上述发现后，还应对声明未覆盖的关键动态上游补充可独立读取、带版本身份的正文或合法导出资料。**来源登记齐全和作者取证记录存在，不能替代这些独立核对。** 后续结论仍应限定为文档技术审阅，不得据此关闭硬件验证、真实环境档案或精确配套交集的既有阻塞。
