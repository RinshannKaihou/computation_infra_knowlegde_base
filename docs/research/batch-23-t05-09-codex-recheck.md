# Batch 23 · T05-09 定向复核

## 审阅元数据

| 项 | 记录 |
|---|---|
| 对象 | T05-09「平台组件升级、发布、回退与回服」；作者修订后第 1 轮定向复核 |
| 角色 | 本会话 Codex，以初审报告的同一独立审阅者角色继续复核；不担任正文作者，不代改正文 |
| 前轮报告 | [batch-23-t05-09-codex-review.md](batch-23-t05-09-codex-review.md)；沿用 B23-T09-C01 至 C09，不以作者修订说明代替核验 |
| 实际模型 | **unknown**；当前接口未暴露精确底层模型 ID，不能把仓库约定或前轮角色名称当作模型身份凭证 |
| 实际 effort | **unknown**；接口未暴露实际推理档位，不冒记为 xhigh |
| 模型审计 | 未另启 CLI 模型、子代理或外部审阅者；无法证明实际路由为单一指定模型、无 fallback，模型身份验收仍未完成 |
| 日期与时区 | 2026-10-18，Asia/Shanghai（UTC+08:00）；本轮显式时钟记录为 16:50:22、16:53:06；落盘后检查与输入哈希复核完成于 16:56:10 |
| 方法 | 重读修订正文与初审关闭条件；重新打开固定版本官方网页；GitHub 连接器读取固定 commit 原文件，对长文件另读相关行段；核对相邻回收流程与只读结构检查 |
| 写入权限 | **只创建本报告**；不改正文、来源、登记表、计划或其他报告，不写 build/，不操作集群或制品 |

主审正文为 [platform-change-and-rollback.md](../../knowledge/05-cluster-platform/platform-change-and-rollback.md)，本次读取共 **177 行**。下文“正文行号”均对应该输入，不是初审的 172 行版本。另读取 [来源记录](batch-23-t05-09-sources.md)、[T05-08 节点摘除与资源回收](../../knowledge/05-cluster-platform/node-drain-resource-reclamation.md)、[README](../../README.md)、[编写指南](../authoring-guide.md)、[归属边界](../../content-outline.md)及 [来源登记表](../../sources/registry.yaml)相关条目。

16:50:22 输入 SHA-256：

| 文件 | SHA-256 |
|---|---|
| `knowledge/05-cluster-platform/platform-change-and-rollback.md` | `4342d9cb8d460d9054d1392c7a37678a30fb3393d3be0e0cdc0044c648637d1d` |
| `docs/research/batch-23-t05-09-codex-review.md` | `78430116fc4c043b73f9f7def8dad8650e70ce6d17be91b4372500d55db92e15` |
| `docs/research/batch-23-t05-09-sources.md` | `307103073b53db235a8b307933841cfc39e2760a4f464b69fba3393eeb4eaec8` |
| `sources/registry.yaml` | `c2f1fad836ddfa72105f54f028d6a094d0bc9107c9a36bc7bbbfefdd61bf4b25` |

工作树原有 Batch 23 正文、来源记录和其他报告等未跟踪文件，以及领域入口、登记表修改；这些不是本轮产生的改动，不覆盖、不回退。收尾时另观察到 `docs/research/batch-23-t05-07-codex-recheck.md` 出现，本轮没有写入该文件，不把此外部变化归为本次交付。

## 逐项复核表

判定按**初审完整关闭条件与当前正文整体语义**执行，不只检查修订关键词是否出现。E01–E11 为本轮重新取得的上游证据，精确入口与章节列于“证据边界”。OPEN 项中的已修正部分予以保留，不把部分修正说成毫无进展。

| 原发现 | 级别 | 判定 | 正文证据位置 | 核验结果与上游依据 |
|---|---|---|---|---|
| B23-T09-C01 | P2 | **CLOSED** | 第 113、116、126、153、157 行 | 已写清失败进入 `upgrade-failed`，排障后人工置回 `upgrade-required`；任一阶段失败即停发，不要求 validation 连败。事件、失败现场与授权分别由观测、停发和前置条件覆盖。符合 E03 的 Troubleshooting；“停发下一波次”是本文流程门禁，不冒充控制器自动冻结整个集群的保证。 |
| B23-T09-C02 | P2 | **OPEN** | 第 98、113、116、126 行 | 容器化/宿主预装边界、空等待选择器、300 秒、`force=false`、drain 默认关闭和非 controller 路径已补对。但初审要求的 emptyDir 策略仍未入档，也未解释删除超时的破坏性后果，不能据 `force=false` 推定会安全等待任务结束。E03；剩余条件见下。 |
| B23-T09-C03 | P2 | **OPEN** | 第 118、127 行 | Container Manager 的脚本路径与禁用 install、Device Plugin 的 Runtime/mounts 条件、TaskD 镜像内处理及回退不一概卸新装旧均已修正。但镜像/全量两条路径只列名称，关键使用限制仍缺；“其余组件才按卸旧装新”仍过宽。E08/E09；剩余条件见下。 |
| B23-T09-C04 | P2 | **OPEN** | 第 61、72–77、87、118、127、157、161 行 | 已要求 history、目标 revision 可用制品，禁止首次纳管/无历史时承诺 Helm 回退，保留先 CRD 后应用与回退后复验。但未明确分别核对两个 Release 的目标 revision 与升级前版本/配置/状态的对应关系；通用变更档案不等于这项映射已经成为门禁。E07；剩余条件见下。 |
| B23-T09-C05 | P2 | **OPEN** | 第 96、101、103、111 行 | “所有可达 apiserver 允许交集”和 1.31/1.32 混版示例已正确加入；仍只明确 kube-proxy 对同节点 kubelet 的偏差，未完整列其对 apiserver 的独立上下界，且 policy 顺序与 kubeadm 操作单元仍未分开。E01/E02；剩余条件见下。 |
| B23-T09-C06 | P2 | **CLOSED** | 第 77、96、124、161 行 | 预检与档案已区分 local/stacked 和 external etcd；本地备份恢复限定到前者，外置需另有匹配备份，无匹配备份即停，空目录不算恢复点；通用资产还要求恢复演练记录。与 E02 的 Recovering from a failure state 相符，未将该目录升级为通用旧 minor 降级保证。 |
| B23-T09-C07 | P2 | **CLOSED** | 第 97、105、135、140、142、164 行 | 已把升级前作业结束、旧 stepd 混合残留清零纳入完成门槛，不再以新 daemon 启动当完成。结合受控新任务从请求到释放、作业/stepd 清单与 T05-08 旧执行退出证据移交，覆盖旧执行退出与新执行验证。E06 的 Upgrade Procedure 支持该门槛。 |
| B23-T09-C08 | P3 | **OPEN** | 第 65、105、125 行 | 已补同一 major 维护补丁按 Minor Upgrades 逐 release 判断，不再完全遗漏例外；但同一恢复表仍绝对写“启动新 daemon 后无原地降级”，前文粗体也未限定大版本/格式迁移。例外与绝对禁语并存，尚未消除原发现。E06；剩余条件见下。 |
| B23-T09-C09 | P2 | **CLOSED** | 第 34、86、131–144、163–166 行；T05-08 第 162–180 行 | 已有重注册、请求→分配→容器稳定身份→使用→释放账本核对；逐层三态、未知不得回服、受控探针先于全面生产准入；正文增加 T05-08 链接与旧执行/释放证据移交。E11 支持注册、Allocate 和分配身份的区别；阈值仍明确由现场基线/SLO 给出，没有冒称官方统一门槛。 |

### OPEN 项的剩余关闭条件

#### B23-T09-C02：数值已补齐，删除保护语义仍不完整

正文第 116 行没有 `deleteEmptyDir` 的记录要求，也没有解释 300 秒耗尽时会发生什么。E03 的 Configuration Options 将 `force` 用于是否处理无控制器管理的 Pod，并另述超时后的强制删除；它不是“永不强删”的总开关。因此，本次用户列举的默认数值检查已满足，但**初审 C02 的完整关闭条件尚未满足**。

可关闭条件：把实际生效的等待选择器、超时及其后果、force、emptyDir/drain 策略和作业恢复点一并列为波次前门禁；补齐 `gpuPodDeletion.deleteEmptyDir=false` 的默认与改变它的数据影响，并说明 `force=false` 不能替代作业保护。按是否启用 drain 分支记录其有效配置，不必复制全部 YAML 或提供执行命令。此项是 C02 残留，不另编号 R01。

#### B23-T09-C03：路径拆分后，还需落下停任务与适用限制

正文第 118 行对 Container Manager、Device Plugin 和 TaskD 的修正与固定 commit 原文一致，不能再报这些点“未修”。剩余问题是：

- E08/E09 区分**全量升级需要停止训练/推理任务**与同版本内的镜像更新；正文未把停任务条件写入 MindCluster 的选择分支。
- E09 的镜像方式不改权限/启动参数，且不适用于 TaskD；正文仅说“两条路径不同”，未保留这些限制。
- E09“升级其他组件”还给出运行断点续训任务时 ClusterD 的特殊处理；正文继续用“其余组件才按卸载旧、安装新”概括，仍可能掩盖条件分支。

可关闭条件：明写全量/镜像路径的停任务、同版本及配置限制，说明 TaskD 不走该镜像更新方式；把“其余组件”限定为相应组件章节与条件成立时的常规路径，保留 ClusterD 特例，或明确本文排除该场景并要求另立方案。无需扩写为完整安装手册，也不能反过来承诺任何同版本更新都无中断。

#### B23-T09-C04：有历史，不等于目标就是升级前的可恢复组合

E07“版本回退”分别查看 `mindcluster`、`mindcluster-crds` 的 history，选择 revision 后先回 CRD 再回应用，并检查组件状态。正文第 127 行已补“有历史且有制品”，第 157 行也有复验；本轮不否认这些修正。缺少的是把**两个独立历史中的目标 revision，分别与实际升级前状态核对并形成配套组合**的明确要求。第 72–77 行通用的制品、配置差异和备份字段没有规定该对应关系，不能把任意可用旧 revision 当作这次变更的恢复点。

可关闭条件：在 Helm 恢复分支逐一记录两个 Release 的身份、history、目标 revision、对应版本/配置/可用制品，以及它们与升级前状态的匹配证据；明确两个 revision 号不能仅凭数字相同就认定配套。继续保留无历史不承诺回退、CRD 数据不自动回迁及恢复后复验的边界。

#### B23-T09-C05：交集规则需要完整的 kube-proxy 约束作输入

E01“kube-proxy”同时规定其对 apiserver 的“不新于、最多旧三个 minor”与对同节点 kubelet 的正负三个 minor 限制；HA 1.31/1.32 示例给出的 proxy 允许集合为 **1.29、1.30、1.31**。正文第 101 行只列后一个关系，第 103 行只举不得升 1.32 的上界例子，未补 apiserver 下界。

用于定向验证的**规则反例，不是现场记录**：apiserver 为 1.31/1.32、同节点 kubelet 为 1.31 时，proxy 1.28 满足正文明确列出的“与 kubelet 差不超过三版”，却不满足 E01。交集口号本身不能补出缺失的集合。

可关闭条件：列齐 kube-proxy 的两类独立约束，再对整个通信集合取交集；同时明确第 101 行是 policy 的组件依赖顺序，第 111 行是 kubeadm 节点级工作流，不能合成为任意拆分的执行清单。E01 提醒部署工具可能更严格，E02 的 How it works 说明 kubeadm 会协调控制面组件及 addon，不能省略工具层核对。

#### B23-T09-C08：维护补丁例外不能与绝对禁语并列

E06 同时包含 Reverting an Upgrade 的状态/数据库风险与 Minor Upgrades 对维护补丁混版、原地降级较宽容的说明，并仍要求备份。正文新增的补丁判断句方向正确，但第 125 行右栏仍为无条件的“启动新 daemon 后无原地降级”，第 65、105 行主句也继续把迁移说成普遍必然事件。

可关闭条件：统一修改这些主句和恢复表，将强限制绑定到大版本或确有状态/schema 迁移的场景；同一 major 的维护补丁逐 release 核验，不承诺任意补丁可降级。也可明确本文采用“不依赖原地降级”的更严格本地策略，但不能把该策略标成覆盖所有补丁的官方结论。仅保留段尾补充句不足以消除表内矛盾。

## 新增发现

**本轮新增独立发现 0 项；不分配 B23-T09-R01。** 上述五项是原 C02/C03/C04/C05/C08 的未闭合部分，沿用原编号和级别，避免重复计数。

对修订所增加的人工重试、宿主驱动分流、HA 交集、etcd 部署形态、旧 stepd 完成门槛、设备三态及证据移交，未发现另有充分证据可认定为本次修订新引入的独立问题。这不等于对整篇或所有现场组合给出无缺陷保证。

## 结论

**本轮不通过，需针对 OPEN 项修订后再次定向复核。**

- **CLOSED 4 项**：C01、C06、C07、C09，均为 P2。
- **OPEN 5 项**：C02、C03、C04、C05（4 项 P2）及 C08（1 项 P3）；P1 为 0。
- **新增发现 0 项**。不能因请求中列举的大多数修订词句已出现，就将未满足的完整关闭条件计为通过。
- 本结论只评价上述输入的文档技术边界与门禁，不证明任何真实升级、回退或回服成功。正文应继续保持 `draft / not_verified`；实际模型与 effort 的身份核验仍为 unknown。

## 证据边界

### 本轮重新打开的上游材料

以下均在 **2026-10-18** 重新读取，不以初审报告或作者来源笔记代替原文。网页中的版本树不等于不可变内容，也不等于本轮证明其仍处支持期；本轮没有把“当前最新版本”作为验收目标。

| 编号 | 精确材料与读取结果 | 本轮核对位置 |
|---|---|---|
| E01 | [Kubernetes v1.32 Version Skew Policy](https://v1-32.docs.kubernetes.io/releases/version-skew-policy/)，网页正文读取成功 | Supported version skew，尤其 kube-proxy、HA 示例；Supported component upgrade order；部署工具附加限制。页面自述为停止维护的静态快照 |
| E02 | [Kubernetes v1.32 Upgrading kubeadm clusters](https://v1-32.docs.kubernetes.io/docs/tasks/administer-cluster/kubeadm/kubeadm-upgrade/)，网页正文读取成功 | 节点级 workflow、控制面/addon 升级说明、Recovering from a failure state、How it works；local etcd member 备份及 external etcd 空目录区别 |
| E03 | [GPU Operator 25.3 GPU Driver Upgrades](https://docs.nvidia.com/datacenter/cloud-native/gpu-operator/25.3/gpu-driver-upgrades.html)，网页正文读取成功 | About、Configuration Options、Upgrade State Machine、暂停/跳过、Troubleshooting、非 controller 路径；C01/C02 的直接依据 |
| E04 | [GPU Operator 25.3 Upgrade](https://docs.nvidia.com/datacenter/cloud-native/gpu-operator/25.3/upgrade.html)，网页正文读取成功 | 手动 CRD 与 pre-upgrade hook 两路径；驱动另走专门升级流程。未把算子升级等同于宿主驱动升级 |
| E05 | [GPU Operator 25.3 Platform Support](https://docs.nvidia.com/datacenter/cloud-native/gpu-operator/25.3/platform-support.html)，网页正文读取成功 | Versioning、Life Cycle 与同 major/下一 major 约束；不据此拼接未核验的现场矩阵 |
| E06 | [Slurm 24.11.7 归档 Upgrade Guide](https://slurm.schedmd.com/archive/slurm-24.11.7/upgrades.html) 精确 URL 重开返回工具 `Internal Error`，**未读到归档网页正文**；改用官方仓库 [固定 release 源文件](https://github.com/SchedMD/slurm/blob/defaf214db2e55326f45ab08f1bde5b2036d9f5d/doc/html/upgrades.shtml)，GitHub 连接器读取成功 | `#revert`、`#minor_upgrades`、`#procedure`；原文件第 154–204 行另行读取，覆盖回退边界、维护补丁例外和旧 stepd 作业完成要求 |
| E07 | MindCluster 固定 commit [Helm 升级](https://github.com/Ascend/mind-cluster/blob/44385c13d7b1d87def35f1604e8be4d16de6ca4e/docs/zh/scheduling/03_installation_guide/04_upgrade/02_helm_upgrade.md)，GitHub 连接器读取成功 | 使用约束、kubectl 纳管与升级分支、版本回退；第 283–327 行及后续回退步骤另读，确认两套 history 与先 CRD 后应用 |
| E08 | 同 commit [手动升级摘要](https://github.com/Ascend/mind-cluster/blob/44385c13d7b1d87def35f1604e8be4d16de6ca4e/docs/zh/scheduling/03_installation_guide/04_upgrade/01_manual_upgrade.md)，GitHub 连接器读取成功 | 全量/镜像两方式、是否跨版本、配置限制和是否停任务 |
| E09 | 同 commit [开发者指南手动升级](https://github.com/Ascend/mind-cluster/blob/44385c13d7b1d87def35f1604e8be4d16de6ca4e/docs/zh/scheduling/05_developer_guide/00_installation_deployment/01_upgrade.md)，GitHub 连接器读取成功 | 升级说明、TaskD、Container Manager、Device Plugin、其他组件、升级镜像；第 145–285、305–444、395–433 行针对性补读，未用被截断的整文件回包代替这些中段 |
| E10 | 同 commit [release_notes.md](https://github.com/Ascend/mind-cluster/blob/44385c13d7b1d87def35f1604e8be4d16de6ca4e/docs/zh/release_notes.md)，GitHub 连接器读取第 1–90 行成功 | 产品字段仍为 26.1.0、配套表和组件勿跨版本混用；不把仓库 tag 名自动当作表内产品版本 |
| E11 | [Kubernetes v1.32 Device Plugins](https://v1-32.docs.kubernetes.io/docs/concepts/extend-kubernetes/compute-storage-net/device-plugins/)，网页正文读取成功 | Allocate/runtime 配置、Handling kubelet restarts、Monitoring device plugin resources/PodResources；用于核对 C09，不证明厂商插件具体组合已验证 |

Slurm release 身份另经本轮官方仓库 [tag ref](https://api.github.com/repos/SchedMD/slurm/git/ref/tags/slurm-24-11-7-1) 和 [annotated tag 对象](https://api.github.com/repos/SchedMD/slurm/git/tags/9d1ef1877186d8101769352831c8f0fe303df31c) 重新核对：tag `slurm-24-11-7-1` → tag 对象 `9d1ef1877186d8101769352831c8f0fe303df31c` → commit `defaf214db2e55326f45ab08f1bde5b2036d9f5d`。该官方 release 源码可支持 C07/C08 的内容判断，**不能证明未获取的归档部署网页与它逐字相同**；也不将工具 Internal Error 写成确定的 HTTP 状态或站点全面不可用。

固定文件身份：Slurm E06 返回 blob SHA `701fcb673f6c795925e0e11d2efc6abd2607ce9c`；MindCluster E07/E08/E09/E10 分别返回 `9a5596344abdbce273f17d7fecafc54bc301c307`、`0b32cedb4db16ed5b36a226abd75103664a58de5`、`7c641ea5f8ecc7648b234c6685530bd10bf16931`、`22c1bef4faa78a7d35efcac5eac7ff8e96f513de`。这些是上游 Git 对象标识，与本地输入 SHA-256 分开记录。

### 校验、限制与未执行项

- 已在报告落盘前后各执行一次 `PYTHONDONTWRITEBYTECODE=1 make check`：均为 **PASS，100 content entries / 469 sources**；只说明结构和本地链接检查通过，不验证技术主张、远程网页或本报告全部关闭条件。
- 落盘后另核对九项发现的唯一性与 4 CLOSED / 5 OPEN 统计、本报告本地链接和行尾空白，均通过；16:56:10 收尾核对上表四项输入哈希均未变化。本轮工具写入仅本报告，不能将其他并行工作树变化当成本轮修改。
- **未执行 `make build`**：默认会写 `build/`，与本轮只允许创建指定报告的权限冲突；没有为了通用构建约定扩大写入范围。未改 `src/kb/`，不新增代码测试。
- 没有执行 Kubernetes、Slurm、GPU Operator、MindCluster 升级/回退命令，没有启动硬件测试或设备探针，没有取得现场备份恢复、目标 revision 配套或应用 SLO 的实测证据。
- 初审报告提供旧正文哈希和定位，但本轮没有取得其完整旧正文副本；故不声称完成逐字 diff 或穷尽全部修订回归。复核以旧发现及关闭条件、当前正文和重新读取的上游材料为依据；未确认的新问题不强行编号。
- NVIDIA 的 25.3 是版本文档树，不是固定 commit；Kubernetes 快照也不等同于不可变字节。本轮结论仅绑定访问日期和已读取章节，不把许可、支持周期或所有平台兼容性扩展为已核验。
