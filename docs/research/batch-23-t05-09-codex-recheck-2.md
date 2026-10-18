# Batch 23 · T05-09 第二轮定向复核

## 审阅元数据

| 项 | 记录 |
|---|---|
| 对象 | T05-09「平台组件升级、发布、回退与回服」；针对上一轮 OPEN 的 C02、C03、C04、C05、C08 逐项复核 |
| 角色 | 本会话 Codex，延续同一独立审阅者角色；不担任正文作者，不代改正文 |
| 前轮报告 | [第一轮定向复核](batch-23-t05-09-codex-recheck.md)；并对照[初审发现与关闭条件](batch-23-t05-09-codex-review.md) |
| 实际模型 | **unknown**；当前接口未暴露精确底层模型 ID，不以仓库约定、角色名称或历史报告替代实际身份 |
| 实际 effort | **unknown**；接口未暴露实际推理档位，不冒记为 xhigh |
| 模型审计 | 本轮未另启 CLI 模型、子代理或外部审阅者；无法据此证明实际路由为指定单一模型、无 fallback，模型身份验收仍未完成 |
| 日期与时区 | 2026-10-18，Asia/Shanghai（UTC+08:00）；本轮显式时钟记录为 17:05:24、17:07:44、17:08:08；落盘后检查与输入哈希复核完成于 17:16:00 |
| 方法 | 重读当前正文、前轮完整关闭条件与相关来源登记；重新打开 Kubernetes v1.32、GPU Operator 25.3 页面；通过 GitHub 连接器重读 MindCluster 固定 commit 和 Slurm 同 release 源文件，不以作者说明代替上游证据 |
| 写入权限 | **只创建本报告**；不修改正文、来源登记、其他报告或计划，不写 build/，不执行集群变更 |

主审正文：[platform-change-and-rollback.md](../../knowledge/05-cluster-platform/platform-change-and-rollback.md)，本轮输入为 **177 行**。下文“正文行号”均对应这份输入。已读取 [README](../../README.md)、[编写指南](../authoring-guide.md)、[归属边界](../../content-outline.md)、[来源记录](batch-23-t05-09-sources.md)及[登记表](../../sources/registry.yaml)相关条目。E 编号沿用前轮所指材料，但以下结论建立在本轮重新读取结果上。

输入 SHA-256（17:08:08 重核，与首次采集一致）：

| 文件 | SHA-256 |
|---|---|
| `knowledge/05-cluster-platform/platform-change-and-rollback.md` | `8cc632bc95a1ebbc8695ee149b160e333826b4f197b19d10721005338f104c80` |
| `docs/research/batch-23-t05-09-codex-recheck.md` | `ad6e49bf71342e9f8a4b12d0a90e7b264a54e48d08650853048545f9d074acf4` |
| `docs/research/batch-23-t05-09-codex-review.md` | `78430116fc4c043b73f9f7def8dad8650e70ce6d17be91b4372500d55db92e15` |
| `docs/research/batch-23-t05-09-sources.md` | `307103073b53db235a8b307933841cfc39e2760a4f464b69fba3393eeb4eaec8` |
| `sources/registry.yaml` | `a336ce6edc17521e79c164d254c2fb272dde9cb60aea8b978ac5018262cce62c` |

## 逐项复核表

| 发现 | 级别 | 判定 | 正文证据位置 | 上游核对与理由 |
|---|---|---|---|---|
| B23-T09-C02 | P2 | **CLOSED** | 第 98、113、116、126 行，核心为第 116 行 | 已将等待选择器/超时、GPU Pod 删除的 300 秒超时及超时强删后果、force、emptyDir、drain 有效配置、作业恢复点列为波次前门禁；明确空等待选择器不等待任何 Pod、`deleteEmptyDir=false` 及改 true 的数据影响，并否定把 `force=false` 当作“永不强删”总开关。与 E03 的 Configuration Options 对应；容器化/宿主预装、controller/非 controller 的边界仍保留。原删除保护语义缺口满足关闭条件。 |
| B23-T09-C03 | P2 | **CLOSED** | 第 118、127 行，核心为第 118 行 | 已区分全量跨版本升级停训练/推理任务与受限同版本镜像升级：后者不改权限/启动参数，TaskD 不适用。“其余组件”不再是一律卸旧装新的结论；已限定组件章节与条件成立的常规路径，并明确排除正在运行断点续训任务时的 ClusterD 特例、要求另立方案。E08 的两方式摘要与 E09 的升级说明、升级其他组件、升级镜像支持这些边界；Container Manager、TaskD、Device Plugin 分支亦未被本次修订抹去。 |
| B23-T09-C04 | P2 | **CLOSED** | 第 127 行；第 157、161 行为恢复后复验与档案门槛 | 失败恢复表已要求两个 Release 分别核对 history、目标 revision、版本/配置/可用制品及与升级前状态的匹配证据，并明确 revision 数字相同不足以认定配套。E07 的版本回退节分别检查 `mindcluster` 与 `mindcluster-crds` 历史，再先回 CRD、后回应用。正文保留首次纳管/无历史不承诺 Helm 回退、CRD 数据不自动回迁及回退后复验。组合匹配是本库的显式证据门禁，不是假称上游已验证某组现场 revision。 |
| B23-T09-C05 | P2 | **CLOSED** | 第 101、103、111 行 | 已同时列出 kube-proxy 对 apiserver 的“不新于、最多旧 3 minor”及对同节点 kubelet 的正负 3 minor 约束；HA 情况取全部可达 apiserver 的交集。1.31/1.32 apiserver、1.31 kubelet 的反例和 1.29/1.30/1.31 集合均符合 E01；1.28 被新版 apiserver 的下界排除。第 101 行明确 policy 依赖顺序不同于第 111 行的 kubeadm 节点执行单元，并保留部署工具可更严格的限制；E02 的 workflow 与 How it works 支持该区分。 |
| B23-T09-C08 | P3 | **OPEN** | 第 65、105、125 行；剩余问题在第 65 行 | 第 105 行“通常会迁移／具体以 release 为准”及第 125 行“大版本或已发生状态/schema 迁移后”的修改有效，**原失败表中的无条件禁语已消除，表内与维护补丁例外已一致**。但第 65 行仍把 daemon 首启后的不支持降级及“只能靠备份/快照恢复”无条件归为 Slurm 官方结论；虽有段末补丁提示，却未直接限定这条主句。E06 同时存在 Reverting an Upgrade 警告与 Minor Upgrades 的维护补丁例外，前轮要求统一主句和恢复表的关闭条件尚未全部满足。 |

### C08 的有效修订、残留及关闭条件

此次并非没有修复：第 105 行已避免把迁移说成每次必然发生，第 125 行也不再与同一行的维护补丁分支互相冲突。残留仅在第 65 行的概括句：

> Slurm 文档明确写出：daemon 首次启动后回退（降级）不受支持，只能靠备份/快照恢复

该句未绑定大版本或确有状态/schema 迁移的场景。段末“维护补丁级升级另按……判断”是必要的例外提示，但这一写法在前轮即已存在；本轮不能把它当成已消除前面绝对断言的新证据，也不能只复查表格而遗漏同一发现指向的摘要位置。这里是 **C08 原有残留，不另编号为 R01**，级别仍为 P3，不据此推导任何特定维护补丁可安全降级。

**剩余关闭条件：**将第 65 行这条主句也明确限定到大版本升级／已经发生状态或数据库 schema 迁移的边界，并把同 major 维护补丁的逐 release 核验写成该结论的例外；或者明确声明本文采用“不依赖原地降级”的更严格本地策略，而不是声称官方对所有维护补丁一律禁止降级。保留现有备份要求即可，无需增加未经核验的降级组合或执行命令。

## 新增发现

**本轮新增独立发现 0 项；不分配 B23-T09-R01。**

针对此次新增的删除策略记录、MindCluster 条件分支、Helm 两 Release 对应关系及 kube-proxy 反例，未发现具有充分证据的新引入独立问题。C08 是前轮发现的未闭合部分，继续沿用原编号，避免重复计数。此结论不等于对全部正文、所有版本组合或真实现场作无缺陷保证。

## 结论

**第二轮定向复核未全部通过：4 CLOSED / 1 OPEN。**

- **CLOSED：**C02、C03、C04、C05，均为 P2；上述四项的本轮关闭条件已满足。
- **OPEN：**C08，P3；失败表矛盾已修复，但第 65 行摘要主句仍需同步限定。
- **新增发现：**0 项。前轮已关闭的 C01、C06、C07、C09 不在本轮重新逐项验收范围，未因本轮结果自动重开，也不冒记为全部重新验证。
- 完成 C08 的上述最小修订后，定向复核第 65、105、125 行的一致性即可；本轮不代改正文。
- 本报告只评价指定范围的文档技术边界与门禁，不证明升级、回退或回服成功；正文继续保持 `draft / not_verified`。实际模型/effort 的身份核验与技术项判定分开记录。

## 证据边界

### 本轮重新打开的关键上游材料

以下材料均于 **2026-10-18** 本轮重新读取。网页章节为网页位置，GitHub 行段为固定 commit 原文件的请求行段，不把网页工具转换后的显示行号当成 GitHub 原文件行号。

| 编号 | 精确材料与读取结果 | 本轮定位与用途 |
|---|---|---|
| E01 | [Kubernetes v1.32 Version Skew Policy](https://v1-32.docs.kubernetes.io/releases/version-skew-policy/)，网页正文读取成功；对应 `src.kubernetes.version-skew-v1-32` | Supported version skew → kube-proxy 及其 HA 示例；Supported component upgrade order；文首关于部署工具附加限制的说明。用于 C05 的两类约束、交集、顺序层级。 |
| E02 | [Kubernetes v1.32 Upgrading kubeadm clusters](https://v1-32.docs.kubernetes.io/docs/tasks/administer-cluster/kubeadm/kubeadm-upgrade/)，网页正文读取成功；对应 `src.kubernetes.kubeadm-upgrade-v1-32` | Upgrade workflow 的三类节点顺序及 How it works：`apply` 协调控制面组件和 CoreDNS/kube-proxy，`node` 在其他控制面/工作节点的职责不同。用于 C05，不生成部署命令清单。 |
| E03 | [GPU Operator 25.3 GPU Driver Upgrades](https://docs.nvidia.com/datacenter/cloud-native/gpu-operator/25.3/gpu-driver-upgrades.html)，网页正文读取成功；属于 `src.nvidia.gpu-operator-upgrade-25.3` 已登记材料 | Configuration Options 的 `waitForCompletion`、`gpuPodDeletion`、`drain`，并对照 About 与 Upgrade State Machine。用于 C02；超时强删与 unmanaged Pod 的 force 控制不是同一语义，drain 是启用且前一阶段未删净时的条件分支。 |
| E06 | [Slurm 24.11.7 归档 Upgrade Guide](https://slurm.schedmd.com/archive/slurm-24.11.7/upgrades.html) 重开返回工具 `Internal Error`，**本轮未读到该网页正文**。改用官方仓库[同 release 固定 commit 的 `doc/html/upgrades.shtml`](https://github.com/SchedMD/slurm/blob/defaf214db2e55326f45ab08f1bde5b2036d9f5d/doc/html/upgrades.shtml)，GitHub 连接器读取成功；对应 `src.slurm.upgrades-24.11.7` 的同版本源码证据 | 原文件第 150–210 行，重点为 `id="revert"` 与 `id="minor_upgrades"` 两节：启动后状态/数据库风险、恢复备份的损失边界，以及维护补丁对混版和原地降级更宽容、仍须当前备份。用于 C08；不以可变最新版替代。 |
| E07 | MindCluster commit `44385c13d7b1d87def35f1604e8be4d16de6ca4e` [Helm 升级](https://github.com/Ascend/mind-cluster/blob/44385c13d7b1d87def35f1604e8be4d16de6ca4e/docs/zh/scheduling/03_installation_guide/04_upgrade/02_helm_upgrade.md)，GitHub 连接器读取成功；属于 `src.ascend.mind-cluster-upgrade-v26.1.1` 已登记材料 | 原文件第 1–68 行的使用约束、管理方式，以及第 283 行起至末尾的版本回退：两套 history、目标 revision、先 CRD 后应用、组件状态确认。用于 C04。 |
| E08 | 同 commit [手动升级摘要](https://github.com/Ascend/mind-cluster/blob/44385c13d7b1d87def35f1604e8be4d16de6ca4e/docs/zh/scheduling/03_installation_guide/04_upgrade/01_manual_upgrade.md)，GitHub 连接器读取完整短文件成功；同一登记项 | 全量升级与升级镜像两方式的停任务、同版本及权限/启动参数限制。用于 C03。 |
| E09 | 同 commit [开发者指南手动升级](https://github.com/Ascend/mind-cluster/blob/44385c13d7b1d87def35f1604e8be4d16de6ca4e/docs/zh/scheduling/05_developer_guide/00_installation_deployment/01_upgrade.md)，GitHub 连接器分段读取成功；同一登记项 | 第 1–90 行升级说明/方式表与环境检查、第 145–267 行 TaskD 与 Container Manager、第 305–365 行 Device Plugin 条件、第 395–444 行其他组件/ClusterD 特例/升级镜像与 TaskD 排除。用于 C03，不用摘要代替这些限制。 |

Slurm release 身份也在本轮重新核对：[tag ref](https://api.github.com/repos/SchedMD/slurm/git/ref/tags/slurm-24-11-7-1) 的 `slurm-24-11-7-1` 指向 tag 对象 `9d1ef1877186d8101769352831c8f0fe303df31c`；[tag 对象](https://api.github.com/repos/SchedMD/slurm/git/tags/9d1ef1877186d8101769352831c8f0fe303df31c) 标为 24.11.7 release，目标 commit 为 `defaf214db2e55326f45ab08f1bde5b2036d9f5d`。因此使用的是同 release 官方源文件，不是把归档读取失败写成已成功访问；也不声称源码与本轮未获取的部署网页逐字一致。

连接器返回的上游 Git blob SHA：Slurm E06 为 `701fcb673f6c795925e0e11d2efc6abd2607ce9c`；MindCluster E07/E08/E09 分别为 `9a5596344abdbce273f17d7fecafc54bc301c307`、`0b32cedb4db16ed5b36a226abd75103664a58de5`、`7c641ea5f8ecc7648b234c6685530bd10bf16931`。它们是上游对象标识，不与本地输入 SHA-256 混用。

### 校验与未执行项

- 报告写入前后各执行一次 `PYTHONDONTWRITEBYTECODE=1 make check`：均为 **PASS，100 content entries / 469 sources**。它只验证结构与本地链接，不验证技术正确性、远程内容、实际模型身份或升级回退结果。
- 落盘后另以只读脚本核对五个规定章节、五项唯一发现与 4 CLOSED / 1 OPEN 统计、本报告本地链接及行尾空白，均通过；17:16:00 重核上述五个输入哈希均未变化。
- **未执行 `make build`**：该命令会写 `build/`，与本轮只允许创建指定报告冲突；不为通用构建约定扩大写入范围。未改 `src/kb/`，不新增代码测试，不运行可能写覆盖率文件的测试命令。
- 本轮工具唯一写入为本报告。工作树在开始时已有其他修改及未跟踪文件，未清理、覆盖、归因于本轮或据此声称其他工作已验收。
- 没有执行 Kubernetes、Slurm、GPU Operator、MindCluster 的升级/回退/drain 命令，没有起集群、设备探针或硬件实验；未取得实际作业恢复点、Release 配套组合或应用 SLO 的现场证据。
- 本轮重新核查的是这五项关闭条件及修订邻近的语义，不是整批重新初审；未取得完整旧正文副本，不声称完成逐字 diff 或穷尽所有回归。未将来源记录中的宽泛归纳代替固定上游原文。
- Kubernetes v1.32 页面自述为停止维护的静态快照；NVIDIA 25.3 是版本文档树而非不可变 commit。本轮不判断它们仍处支持期，不核验最新版或扩展到其他硬件/软件组合，也未重新开展第三方许可审计。
