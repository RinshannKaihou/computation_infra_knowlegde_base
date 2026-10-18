# Batch 23 · T05-08 第二轮定向复核报告

## 审阅元数据

| 项目 | 记录 |
|---|---|
| 任务与轮次 | T05-08「节点摘除、drain 与资源回收流程」；第二轮定向复核，仅重新判定上一轮仍 OPEN 的 C01、C03、C06、C08，并检查修订引入的问题 |
| 角色 | 延续同一独立审阅角色，不是正文作者；依据上一轮报告逐项复核，未委派子代理 |
| 实际模型 | **unknown**。当前接口未暴露可核验的精确模型标识；不能用仓库约定模型代填，也不能证明各轮底层模型相同 |
| 实际 effort | **unknown**。接口未暴露实际 reasoning effort，不能将约定的 `xhigh` 写成实际值 |
| 日期与时区 | 2026-10-18，Asia/Shanghai（UTC+08:00）；本轮本地读取、上游重读与检查均在该日进行 |
| 直接依据 | [第一次定向复核报告](batch-23-t05-08-codex-recheck.md)，并重读[初审发现及关闭条件](batch-23-t05-08-codex-review.md)；不以作者说明替代正文或上游证据 |
| 唯一写入 | 新建本报告；不改正文、既有报告、来源记录、登记表、计划、代码或 `build/` |
| 执行边界 | 只读文档/源码及本地结构检查；未连接集群，未执行 drain、Eviction、状态恢复、取消、重排、重启、断电、设备/卷清理或提交验证负载 |

本轮审阅快照如下；取证后、写报告前再次校验，四份文件的指纹一致。

| 文件 | 行数 / SHA-256 |
|---|---|
| [正文](../../knowledge/05-cluster-platform/node-drain-resource-reclamation.md) | 230 行；`0dbee808f362b95bdc985ccb680e6319570614c7e02355c7de1a5a9e06d304ff` |
| [任务来源记录](batch-23-t05-08-sources.md) | 144 行；`ea9e73731beeda279c989dd814ccb2f7dc9ed52b404524c1a466c19a8ab760ef` |
| [第一次定向复核报告](batch-23-t05-08-codex-recheck.md) | 132 行；`a66b795e4114eb09a8cca3f3789e800154518a969f05941601ed07469b0739ef` |
| [来源登记表](../../sources/registry.yaml) | `a336ce6edc17521e79c164d254c2fb272dde9cb60aea8b978ac5018262cce62c` |

**行号口径：** 下文「正文 L…」「来源记录 L…」「登记表 L…」均为上述本地源文件行号。用户沿用的旧正文 **L114 / L134，在当前快照对应 L120 / L140**；当前 L114 是表格分隔行，L134 是批处理责任行。上游源码坐标另行注明，不使用网页提取行号拼接源码锚点。`CLOSED` 仅关闭相应文档缺陷，不等于现场验证、指定模型合规认证或整篇通过。

## 逐项复核表

| 发现 ID | 原级别 | 判定 | 本轮证据与理由 |
|---|---|---|---|
| B23-T08-C01 | P1 | **OPEN** | 正文 L120、L140 已删除“注册成功即生产放行”的含义；L184–188 已要求独立生产屏障、执行前批准、核实入口及失败撤销例外。但总恢复段 L170 要求保持 `DRAIN`，L173 才启动新验证负载，L174 又绝对限定验证通过后才执行 `RESUME` / `UNDRAIN`；与 L120、L140 中验证前的 `RESUME` 顺序仍不一致。固定版本 [scontrol 的 DRAIN/RESUME/UNDRAIN](https://github.com/SchedMD/slurm/blob/defaf214db2e55326f45ab08f1bde5b2036d9f5d/doc/man/man1/scontrol.1) 不支持在保持 DRAIN 时启动新 job。三个失败输入的禁止生产放行已补齐，但正向验证启动路径尚未统一，详见下节。 |
| B23-T08-C03 | P2 | **CLOSED** | 正文 L92、L101–107 已区分健康目标、默认 IfHealthyBudget 的不健康 Running 目标、AlwaysAllow 的不健康 Running 目标；L104 有健康数满足/下降的未执行反例与 `desiredHealthy > 0` 分支限制。来源记录 L14/L76、登记表 L5559 均已撤销无条件“永不完成”的归纳，限定健康 Pod 并保留 AlwaysAllow 例外。与 [v1.32 PDB 的健康判定及策略节](https://v1-32.docs.kubernetes.io/docs/tasks/run-application/configure-pdb/#unhealthy-pod-eviction-policy)、[v1.32.0 eviction.go L235–258](https://github.com/kubernetes/kubernetes/blob/v1.32.0/pkg/registry/core/pod/storage/eviction.go#L235) 一致。 |
| B23-T08-C06 | P2 | **CLOSED** | 正文 L190–201 的最小账本连接节点、执行身份、分配记录、实际设备/映射依据、观察时间及重启边界；L201 明确 PodResources 不能直接提供 UID/容器 ID/ATTEMPT，须同期 API/CRI 对齐，连接不唯一则 unknown，重启后重采。L119/L153/L155/L215 保留进程、Epilog、job/step 与平台账本的独立核对。与 [v1.32 Device Plugins 的 List 与重启说明](https://v1-32.docs.kubernetes.io/docs/concepts/extend-kubernetes/compute-storage-net/device-plugins/#monitoring-device-plugin-resources) 相符；Slurm 编号限制另以同版本源码核对。已形成可填写、可执行前审定的方法，不要求伪造现场数据。 |
| B23-T08-C08 | P2 | **CLOSED** | 正文 L203–208 已有批准/发起/证据确认人、新执行 attempt、镜像与数据/Checkpoint 版本、覆盖范围、不适用说明、观察窗口及判断基线；缺基线不通过，验证结束再对账，失败或缺证回隔离。L173、L188、L201、L217 将其接到验证准入、身份账本及最终生产门槛；L136–142 的例子仍明确未执行，Kubernetes 例子可对照 [v1.32 disruptions 的 PDB example](https://v1-32.docs.kubernetes.io/docs/concepts/workloads/pods/disruptions/#poddisruptionbudget-example)。验证记录本身的闭环缺口关闭；其准入前置仍受 C01 和新增 R01 阻塞，不重复计入 C08。 |

### C01：失败门控已补，正向状态恢复仍有两种互斥读法

修订的有效部分应保留：L120 不再把注册等同生产准入，L140 不再把 IDLE 等同可排生产，L188 明确没有核实入口就停止，并要求验证失败撤销例外。这些不是单纯换词，确实增加了生产放行约束。

不过，总恢复段标注“顺序不可颠倒”：**L170 保持 DRAIN → L173 发起新验证负载 → L174 仅验证通过后 RESUME/UNDRAIN**。主路径 L120、状态例子 L140 却是先 RESUME/注册，再受控验证。L184 的“保持生产隔离前提下状态恢复”是正确原则，但未明确修正总恢复段对具体状态动作的绝对限制；L186 又将 RESUME/UNDRAIN 重列为验证后动作。

同版本 scontrol 源文档 NODES—UPDATE 明确区分：DRAIN 拒绝新 job；RESUME 改变状态并要求注册；UNDRAIN 清 drain，但不替代有效注册。另重读的[同版本 reservation 指南](https://github.com/SchedMD/slurm/blob/defaf214db2e55326f45ab08f1bde5b2036d9f5d/doc/html/reservations.shtml)支持为特定用户/账户保留资源，以及用于节点调查的维护 reservation；**这不使 reservation 成为在 DRAIN 上启动新 job 的旁路**。因此矛盾是流程可执行性缺口，不是要求增加一条未经授权的命令。

**未执行的定向输入：** 以下仅逐段代入文档条件，不是集群结果。

| 输入 | 当前应走的分支与证据位置 | 生产放行判定 |
|---|---|---|
| 必须卸载的 CSI 卷仍未卸载，或缺少卸载证据 | L163 停止，L171–172 冲突/必需证据未闭合，L188 明文禁止；这里不把已批准的保留 PV 数据决定混同“卸载已成功” | **不得放行**；缺证亦不得进入下一步 |
| 设备仍有过期分配 | L166、L171、L201、L216 要求消除冲突并独立证明旧分配释放，L188 明文禁止 | **不得放行** |
| 验证失败或结果证据缺失 | L173 回隔离，L188 撤销验证例外，L208 保存证据并返回隔离 | **不得放行** |
| 站点无可用且可核实的验证入口 | L120、L188 停止并记 unknown | **不得靠 RESUME 先放开生产再验证** |
| 节点仍 DRAIN，但已具备有效、排除普通生产的维护 reservation，需要启动新验证 job | 按 L170/L174 不能先 RESUME；按 L116 的状态语义，新 job 又不能启动；L120/L140 则预先使用 RESUME | **正向路径仍不自洽，C01 保持 OPEN** |

**剩余关闭条件：** 将总恢复段改为持续保持“普通生产隔离”，而不是无条件保持某个具体状态；明确在旧执行/资源冲突及基础设施门槛通过、独立生产屏障已经生效并核实后，哪一步可执行必要的 RESUME/注册以准入验证。验证通过且清理对账完成后才撤销其余生产屏障；不要求已恢复的节点重复 RESUME。同步衔接 L120、L140、L170–188，明确屏障在改变调度条件**之前**生效；再次检查上述三个失败输入。此项沿用 C01，不另编新号。

### C03：正文、摘要及反例的一致性

来源记录 L14 的概述、L76 的登记建议，以及登记表 L5559 的实际条目现已一致：健康 Pod 的预算阻塞不能外推为所有 Pod 都不可驱逐，AlwaysAllow 的不健康目标例外仍在；默认策略没有被概括成“仅 disruptionsAllowed 决定”。L76 与 L5559 的 notes 文本一致。

以 PDB 状态已同步、无其他拒绝原因为前提，正文反例与本轮重读的 eviction 实现可作以下来源推演：

| 目标与输入 | PDB 分支判读 |
|---|---|
| 健康目标，`disruptionsAllowed=0`，任一策略 | 健康目标不享受 AlwaysAllow 的不健康例外 |
| Running/Ready=False，IfHealthyBudget，`currentHealthy=desiredHealthy=2`，剩余预算 0 | 符合不健康目标的直接放行分支，不因零剩余预算扣减/拒绝 |
| 同上，但 `currentHealthy=1`、`desiredHealthy=2`、剩余预算 0 | 不满足该直接放行分支，不能套用前例 |
| Running/Ready=False，AlwaysAllow，即使健康预算不足 | 不因该健康预算条件拒绝；不保证整次 drain 成功 |

`desiredHealthy > 0` 是本轮核对的 v1.32.0 源码直接放行分支条件，不能反推 `desiredHealthy=0` 时所有删除都被拒绝；该分支未命中后仍有后续预算检查。正文没有作这种反推。以上均未向 API 发送请求，也未修改 PDB。

### C06：最小方法已能落到关联记录

结合 L119、L190–201、L215，读者现在可以按以下顺序审定记录，而不是仅列出互不连接的字段：

1. 固定节点身份与观察窗口，按旧执行和新验证 attempt 分开填行，并记录重启边界。
2. Kubernetes 用同期 API/CRI 将 Pod/container 名称连到 Pod UID、容器 ID/ATTEMPT，再连接 PodResources 的资源名/设备 ID；发生同名替换或无法唯一对齐时记 unknown，不以名称或数量相同放行。
3. Slurm 将 NodeName、job/step 和重启计数连到 GRES 分配记录、实际设备及 cgroup/设备节点；映射依据须按平台核实。TRES 数量或一个 GPU 编号本身都不能替代这条映射。
4. 分别核对旧进程退出、旧平台分配释放、新验证 attempt 获得正确分配；daemon/插件重启后重新采集，历史快照只能保留作历史证据，不能继续充当当前放行依据。

PodResources 的身份局限已与上游 List 结构逐字段核对。同版本 Slurm [sbatch.1 的环境变量说明](https://github.com/SchedMD/slurm/blob/defaf214db2e55326f45ab08f1bde5b2036d9f5d/doc/man/man1/sbatch.1)也明确 `SLURM_JOB_GPUS` 是分配的全局 GPU ID、不是设备 cgroup 内的相对编号；[GRES 文档](https://github.com/SchedMD/slurm/blob/defaf214db2e55326f45ab08f1bde5b2036d9f5d/doc/html/gres.shtml)要求在启动后检查设备编号与设备文件映射。这支持正文要求记录映射与重采，不能据此保证 NPU 或具体插件行为。本轮关闭的是最低对账方法缺口，不是声称已经采到一份合格账本。

### C08：记录模板可审定，但不得越过准入前置

L205–208 已把身份/版本、责任人、设备与通信路径、应用进展/数据结果、观察窗口/基线及结束清理组织到同一执行前记录；L201 规定旧退出、旧释放、新验证分配分别核对，L188 规定验证入口的批准与生产屏障，L217 把两者接入完成条件。因此本项不再只是四类负载的目标清单。

实际节点、镜像、Checkpoint、窗口、阈值和证据确认记录仍需现场填入；缺项按正文 unknown/失败处理，不能宣告验证通过。C01 的状态顺序矛盾及下述 R01 是此前置入口的缺陷，不因 C08 的记录模板合格而消失。

## 新增发现

### B23-T08-R01 · 专用 namespace 不能独立构成验证准入机制

- **级别 / 状态：P2 / OPEN。** 新增位置：正文 **L185**，相关防护 L188；这是新增三层表中的 Kubernetes 机制表述问题，与 C01 的 Slurm/总恢复顺序矛盾不同。
- **问题：** L185 将“容忍、`nodeName` 或专用 namespace”并列为保持 cordon/污点时的验证入口。namespace 可以用作归属或已配置策略的选择条件，但 namespace 本身既不豁免 cordon/污点，也不保证只有验证负载能设置容忍或直接绑定。L188 的执行前核实、unknown 停止要求降低了误用风险，却不能使这个并列选项成为 Kubernetes 原生能力。
- **上游依据：** [v1.32 Namespaces](https://v1-32.docs.kubernetes.io/docs/concepts/overview/working-with-objects/namespaces/)描述命名/资源作用域，Node 不是 namespaced 对象；[v1.32 safely-drain-node 的两个例外](https://v1-32.docs.kubernetes.io/docs/tasks/administer-cluster/safely-drain-node/#use-kubectl-drain-to-remove-a-node-from-service)分别是 unschedulable 容忍与直接 `nodeName`。进一步读取 [v1.32.0 NodeUnschedulable.Filter](https://github.com/kubernetes/kubernetes/blob/v1.32.0/pkg/scheduler/framework/plugins/nodeunschedulable/node_unschedulable.go#L130)，其 cordon 判定读取节点 unschedulable 和 Pod 的匹配容忍，不以 namespace 提供例外。[v1.32 taints 文档](https://v1-32.docs.kubernetes.io/docs/concepts/scheduling-eviction/taint-and-toleration/#concepts)还区分 `nodeName` 绕过调度器与 NoExecute 的继续约束。
- **未执行反例 / 影响：** 默认调度器下，节点 cordon，验证 Pod 仅换到专用 namespace、没有相应容忍或直接绑定，仍不能靠 namespace 进入节点；若用 `nodeName` 但节点存在未容忍的 NoExecute，也不能据此保证验证持续运行。前者是基于 Filter 的推演，后者来自文档机制，均不是现场结果。误把归属范围当有效入口，会使恢复验证再次卡住，或诱使操作者为继续而解除隔离；本文不授权这种处置。
- **关闭条件：** 将 namespace 明确为归属/策略选择字段，不再与真实准入机制作为无条件替代项并列。若站点确有基于 namespace 的 admission/调度策略，须说明并核实它如何提供所需容忍/绑定约束、谁可使用，以及什么控制继续阻断普通生产；仍不得自行发明通用旁路。对采用容忍/`nodeName` 的分支明确核对适用污点/effect，不能用 `nodeName` 暗示绕过 NoExecute。再次代入“只有 namespace”和“直接绑定但未容忍 NoExecute”两个输入，未知或不满足时应停止，而不是认定验证入口已具备。

## 结论

- 本轮四项：**C03、C06、C08 CLOSED；C01 OPEN（P1）**。
- 新增：**B23-T08-R01 OPEN（P2）**。不将 C01 尚存的原根因重新编号。
- 三个指定失败输入在新增门槛下均不得放行生产；但这不等于正向验证准入顺序已经自洽。仍需修订 C01 与 R01，再作定向复核，**不能宣布 T05-08 或 Batch 23 审阅通过**。
- 上一轮已关闭的 C02、C04、C05、C07、C09 不在本轮重审范围；不追改历史判定，也不据本轮声称已重新完整核验。
- 正文保持 `draft / not_verified`；本轮不修改其元数据，不提供硬件、CSI、平台兼容性或恢复能力的实测背书。

## 证据边界

### 本轮重新打开的关键上游

| 材料 | 本轮成功读取的位置与用途 |
|---|---|
| [Kubernetes v1.32 configure-pdb](https://v1-32.docs.kubernetes.io/docs/tasks/run-application/configure-pdb/) | 零自愿驱逐概述、Healthiness、Unhealthy Pod Eviction Policy；使用 v1.32 静态快照，不用当前版替换 |
| [Kubernetes v1.32 Device Plugins](https://v1-32.docs.kubernetes.io/docs/concepts/extend-kubernetes/compute-storage-net/device-plugins/) | Handling kubelet restarts、Monitoring 的 List protobuf；核对名称/资源/设备字段及身份缺项 |
| [Kubernetes v1.32 safely-drain-node](https://v1-32.docs.kubernetes.io/docs/tasks/administer-cluster/safely-drain-node/)、[taints](https://v1-32.docs.kubernetes.io/docs/concepts/scheduling-eviction/taint-and-toleration/)、[namespaces](https://v1-32.docs.kubernetes.io/docs/concepts/overview/working-with-objects/namespaces/) | 分别核对 cordon 例外、NoSchedule/NoExecute 与直接绑定的区别、namespace 作用域；支撑 R01 |
| [Kubernetes v1.32 disruptions](https://v1-32.docs.kubernetes.io/docs/concepts/workloads/pods/disruptions/) | PodDisruptionBudget example 的替代副本尚未可用、drain 阻塞和容量不足；不将 Pending 泛化为必须加节点 |
| [Kubernetes v1.32.0 eviction.go](https://github.com/kubernetes/kubernetes/blob/v1.32.0/pkg/registry/core/pod/storage/eviction.go) | 原文件 L220–290；不健康目标直接放行分支及后续预算检查；仅补充该发布源码，不代表所有 v1.32 补丁 |
| [Kubernetes v1.32.0 node_unschedulable.go](https://github.com/kubernetes/kubernetes/blob/v1.32.0/pkg/scheduler/framework/plugins/nodeunschedulable/node_unschedulable.go) | 原文件 L95–163，关键 Filter 在 L130 之后；R01 的默认调度器反例依据 |
| [Slurm 发布 tag 对象](https://api.github.com/repos/SchedMD/slurm/git/tags/9d1ef1877186d8101769352831c8f0fe303df31c) | 本轮独立读取，`slurm-24-11-7-1`、消息为 24.11.7 release，指向 `defaf214db2e55326f45ab08f1bde5b2036d9f5d`；对象报告 unsigned，不声称签名验证 |
| [Slurm scontrol.1](https://github.com/SchedMD/slurm/blob/defaf214db2e55326f45ab08f1bde5b2036d9f5d/doc/man/man1/scontrol.1) | 固定上述 commit，读取原文件 L1700–1920；核心为 NODES—UPDATE 的 DRAIN、RESUME、UNDRAIN 与 ResumeAfter |
| [Slurm reservations.shtml](https://github.com/SchedMD/slurm/blob/defaf214db2e55326f45ab08f1bde5b2036d9f5d/doc/html/reservations.shtml) | 同 commit，L1–170；保留资源、用户/账户及维护调查例子；不证明任何实际站点已正确配置 |
| [Slurm sbatch.1](https://github.com/SchedMD/slurm/blob/defaf214db2e55326f45ab08f1bde5b2036d9f5d/doc/man/man1/sbatch.1)、[gres.shtml](https://github.com/SchedMD/slurm/blob/defaf214db2e55326f45ab08f1bde5b2036d9f5d/doc/html/gres.shtml) | 同 commit；sbatch 读取 L3240–3355、L3400–3510，核对 GPU ID 和重启计数；gres 成功读取 L1–190、L280–365，核对分配记录及启动后设备映射边界 |

**访问限制：** 本轮重开 Slurm 24.11.7 归档 `scontrol.html` 和 `reservations.html`，网页工具均返回 `Internal Error`，未取得可读归档正文；这不是 HTTP 404 的证据。随后通过 GitHub 只读连接器成功取得上表同版本官方源文件及 tag。一次额外读取 gres L235–296 遇到连接器传输错误，未用该次失败响应作为证据；表中仅列成功读取范围。源码可以支持对应版本语义，不能据此声称已核对归档 HTML 的字节内容或生成时间。

### 本地检查、写入与未验证事项

- 已阅读 `README.md`、`docs/authoring-guide.md`、`content-outline.md` 及用户提供的根目录规则；未发现适用的更深层 AGENTS.md。
- 已运行 `PYTHONDONTWRITEBYTECODE=1 make check`：**PASS，100 content entries / 469 sources**。只验证结构与本地链接，不验证远程页面、本文技术结论或任何恢复结果；禁止生成 Python 字节码以避免额外写入。
- **未运行 `make build`**：它会写 `build/catalog.json`、`build/catalog.md`，与用户本轮只允许创建本报告的约束冲突。未改 `src/kb/`，未运行集群/硬件测试。
- 工作区开始即有用户/其他工作的未提交修改及未跟踪文件，未作撤销、覆盖或归因。17:06:39 建立内存文件指纹基线，覆盖 468 个普通文件，排除 `.git`、`.venv`、`.agents`、`.codex`、`__pycache__`；17:12:18 对照时，基线中的既有文件指纹全部未变，新增本报告及 `batch-23-t05-07-codex-recheck-2.md`、`batch-23-t05-09-codex-recheck-2.md`。后两份属于本轮工具写入以外观察到的并发新增，未读取其内容、未修改、未作作者归因。本轮写入调用只涉及本报告；不能宣称整个工作区仅新增一份文件，也不将非原子检查夸大为全程文件系统审计。
- 只保留链接和原创审阅归纳，没有新建上游镜像、下载缓存、现场日志或实验附件。实际 reservation/分区/允许清单、Kubernetes admission/容忍约束、镜像/Checkpoint、CSI 卸卷、设备映射与重采、验证窗口/阈值仍无现场证据；unknown 不因文档 CLOSED 而转为已验证。
