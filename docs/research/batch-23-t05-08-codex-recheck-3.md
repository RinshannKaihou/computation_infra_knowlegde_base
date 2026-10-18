# Batch 23 · T05-08 第三轮定向复核报告

## 审阅元数据

| 项目 | 记录 |
|---|---|
| 任务与轮次 | T05-08「节点摘除、drain 与资源回收流程」；第三轮定向复核 C01、R01，并检查这次修订是否引入新问题 |
| 角色 | 延续同一独立审阅角色，不是正文作者；直接重读正文、上一轮完整关闭条件与上游材料，未委派子代理 |
| 实际模型 | **unknown**；接口未暴露可核验的精确模型标识，不用仓库约定模型代填，也不能证明跨轮底层模型完全相同 |
| 实际 effort | **unknown**；接口未暴露实际 reasoning effort，不把约定的 `xhigh` 写成实际值 |
| 日期与时区 | 2026-10-18，Asia/Shanghai（UTC+08:00） |
| 直接依据 | [第二轮定向复核报告](batch-23-t05-08-codex-recheck-2.md)，重点为其 L54 的 C01 剩余关闭条件与 L90–96 的 R01；另核对[初审 C01](batch-23-t05-08-codex-review.md#b23-t08-c01--失败恢复不能先解除隔离)的原始风险范围 |
| 唯一写入 | 只新建本报告；不修改正文、既有报告、来源记录、登记表、计划、代码或构建产物 |
| 执行边界 | 只读文档/源码与本地结构检查；未连接集群，未执行节点、调度、设备、卷或验证负载操作 |

本轮取证并在写报告前复核的文件快照：

| 文件 | 行数 / SHA-256 |
|---|---|
| [正文](../../knowledge/05-cluster-platform/node-drain-resource-reclamation.md) | 230 行；`464f36602f4509164c6e9d6d0d4fffe3cbad2b48ad4079ab6de04f5afdaf700a` |
| [第二轮报告](batch-23-t05-08-codex-recheck-2.md) | 131 行；`8f9a1125cece42b00443826ccda016ed3a2c1ef83123bd91896d4188fc372d1e` |
| [任务来源记录](batch-23-t05-08-sources.md) | 144 行；`ea9e73731beeda279c989dd814ccb2f7dc9ed52b404524c1a466c19a8ab760ef` |
| [来源登记表](../../sources/registry.yaml) | `a336ce6edc17521e79c164d254c2fb272dde9cb60aea8b978ac5018262cce62c` |

下文「正文 L…」均指上述正文快照的原文件坐标；上游引用按版本、文件与节定位，不把网页提取行号当成源码行号。`CLOSED`/`OPEN` 针对完整发现 ID，而不是只核对作者此次列举的修改句。

## 逐项复核表

| 发现 ID | 原级别 | 判定 | 本轮证据与理由 |
|---|---|---|---|
| B23-T08-C01 | P1 | **OPEN** | 验证前的危险顺序已实质修正：L120、L140、L168–176、L184 均允许在生产排除控制先启用并核实后注册/恢复，L188、L208、L217 仍禁止失败输入放行。但 L174、L186 仍统一写成验证后「再执行 `uncordon` / `RESUME` / `UNDRAIN`」，没有区分已在前面完成恢复的分支，也未明确如何解除仍在生效的独立生产排除控制。尚未满足上一轮 L54 明确要求的「撤销其余生产屏障；不要求已恢复节点重复 RESUME」。这不是断言原先的验证前生产泄漏仍存在；残余是最终回服交接没有闭合。见下节及 S01、S02。 |
| B23-T08-R01 | P2 | **OPEN** | **namespace 子问题已解决**：L185 已明确它只是组织边界，不能单独阻断生产 Pod，并禁止以其替代节点级控制；全文另一次 namespace 出现在 L201 的身份字段说明，不是准入承诺。但 L185 仍把「cordon/污点 + 容忍或 `nodeName`」作为概括入口，未限定污点 effect，也未补上上一轮 L96 明确要求的 `nodeName` 不绕过未容忍 `NoExecute` 的检查。L188 的通用停止条件不能代替这个已经指定的分支。见下节及 K01–K04。 |

### C01：验证前顺序一致，最终生产切换仍需分支

对作者要求核对的三个位置逐一重读，不能再沿用第二轮的旧结论说它们仍要求「保持 DRAIN 时启动新 job」：

| 位置 | 本轮正文实际内容 | 定向判断 |
|---|---|---|
| 总恢复安排，L168–176 | L170 先保持隔离；L171 排除旧占用/分配冲突；L172 要求先启用并核实生产排除控制，再执行必要的状态动作；L173 才受控验证 | 验证前顺序已与主路径一致；L170 是初始步骤，不再绝对限制后续一直保持 DRAIN |
| 三层门槛，L184–188 | L184 将生产排除控制放在注册/恢复之前，无控制不得 `RESUME`/`UNDRAIN`/`uncordon`；L188 无可核实入口则停止 | 基础设施恢复与生产准入已经拆开；并未声明 reservation 可以绕过 DRAIN 启动 job |
| Slurm 步骤 6 与状态例子，L120、L140 | 先启用并核实生产排除控制，再 RESUME/注册，之后受控验证、撤销例外、开放生产；L120 明确成功注册后清 NoResp，普通生产仍被阻断 | 与前两处的验证前门槛一致；L140 的压缩例子须连同 L120 理解，不能在 NoResp 未清时认定可验证 |

上述修改符合 S01 的 DRAIN/RESUME/UNDRAIN 语义：DRAIN 本身不允许新 job；验证前状态恢复与持续生产隔离可以分别处理。S02 支持用受限 reservation 或维护分区组织节点调查，但不证明任何站点屏障已经配置正确。

**剩余缺口在 L174、L186 的最后一步，不在前置顺序。** 现有句子仍将三种状态动作统一列为最终开放生产的动作。若前面已经 RESUME、注册成功，并使用持续生效的维护 reservation 阻断生产，验证结束后节点并不需要再靠 RESUME 恢复状态；真正尚需交接的是这项生产排除控制。S01 的 RESUME/UNDRAIN 是节点状态动作，不能据此推断它会删除 reservation；S02 的 Reservation Modification/Deletion 则把 reservation 的修改、到期及删除另行说明。

**未执行的正向输入：** 采用 S02 所支持的无限期节点维护 reservation，先核实其阻断普通生产，再 RESUME、完成注册与验证，验证 job 退出、资源对账完成。此时如果「撤销验证例外」仅指撤销验证负载的特殊授权，而 reservation 本身仍在，随后执行节点状态动作不能证明普通生产已开放；若作者意指「撤销验证例外」也包含解除这项 reservation，应把这一含义与先后门槛写明。这里指出的是文本存在两种实施读法，**不声称已经观察到重复 RESUME 的具体返回码或站点调度结果**。

**剩余关闭条件：** 在 L174、L186 明确验证通过、验证负载退出且再次对账完成后，先撤销验证负载的特殊准入，再按执行前审定的方案解除/切回独立生产排除控制；只有节点确实仍需要状态恢复时才执行相应状态动作，不要求已恢复节点重复 RESUME。同步 L120、L140 的最终交接语义，并保留 L188 的失败隔离门槛。无需编造通用 reservation/分区修改命令。本条件沿用第二轮 L54，不另编号。

### C01：三个指定失败输入均不得普通生产放行

以下为文档条件代入，不是现场测试：

| 输入 | 正文证据位置与应走分支 | 判定 |
|---|---|---|
| 必须卸载的 CSI 卷仍未卸载，或缺少卸载证据 | L163 停止；L171 的资源冲突未闭合；L188 明文禁止；L208、L217 要求验证结束后再次收敛 | **不得开放普通生产**。L171 的「明确保留」不等于必需卸卷成功；不应把保留 PVC/PV 数据对象的决定当作仍挂载卷的安全证明。K05 也不支持仅靠节点状态判断旧写入者已安全退出 |
| 设备仍有过期分配 | L166 停止；L171 不允许过期/重复分配；L188 明文禁止；L201 要分别证明旧执行退出、旧平台分配释放、新验证 attempt 正确分配；L216 要账实一致 | **不得开放普通生产**；不能用新验证成功掩盖旧分配未释放 |
| 验证失败，或缺少结果/基线证据 | L173 返回隔离；L188 撤销验证例外并恢复生产隔离；L207 缺基线不通过；L208 失败或缺证返回隔离 | **不得开放普通生产**；也不得进入 L174 的成功分支 |

因此，三个负向门控均已具备，并不因 C01 的最终交接仍 OPEN 而失效；反之，负向门控成立也不能替代正向流程的完整关闭。

### R01：不再把 namespace 当准入控制，但 NoExecute 子条件仍缺

全文检索并逐处核对 namespace、容忍、`nodeName` 与污点表述后，**没有发现修订后的正文仍把专用 namespace 单独当作准入控制**。L185 的组织边界/禁止替代表述与 K03 一致；L201 只是 PodResources 的名称字段说明。这里不把已经纠正的 namespace 误写继续计为未修正。

但第二轮 R01 的关闭条件还包括对「只有 namespace」和「直接绑定但未容忍 NoExecute」两个输入分别判断。修订后的 L185、L188 没有新增 `NoExecute`/effect 的限制；L91、L99 只是说明直接绑定绕过调度，L151 的一般污点排查、L97 的 out-of-service 处置也不能补足验证入口的这一条件。K02 的 Concepts 明确：`nodeName` 绕过调度器及 NoSchedule 检查，不意味着可以忽略未容忍的 NoExecute；后者还影响 Pod 继续运行。K04 则只支持 unschedulable 与对应容忍的判断，不提供 namespace 旁路。

| 未执行的输入 | 根据上游应如何判断 | 当前正文覆盖 |
|---|---|---|
| 节点 cordon，验证 Pod 只有专用 namespace，没有匹配容忍或直接绑定 | namespace 本身不构成入口；无法核实可用入口则停止 | L185、L188 已覆盖该方向，namespace 子问题可以关闭 |
| 验证 Pod 使用 `nodeName`，节点仍存在它没有容忍的 NoExecute 污点 | 不能认定具备可持续运行的验证入口；应停止并核对该污点及相应容忍，而不是为继续验证解除生产隔离 | L185 的「容忍或 nodeName」仍未说明这项必要限制；L188 只有一般停止条件，上一轮指定的反例尚未写回正文 |

**剩余关闭条件：** 对 L185 的分支明确核对实际污点 key/value/effect 与所需容忍；直接绑定只绕过调度器，不豁免未容忍的 NoExecute。仅确认 `nodeName` 或 namespace 不足时，应在保持生产隔离下停止、记 unknown，而不是认定入口已经具备。继续保留只有验证 Pod 获准使用相应容忍/绑定能力的前提。本条件沿用第二轮 L96，不另编号，也不要求本轮真实提交 Pod。

## 新增发现

**无独立新增发现；本轮未启用 B23-T08-R02 及后续编号。** C01 的最终生产屏障交接和避免重复 RESUME，以及 R01 的 NoExecute 分支，均已在第二轮明确列为关闭条件，不把原项残余重新包装成新发现。也未把全文重检 namespace 时已经纠正的表述重复计数。

## 结论

- **B23-T08-C01：OPEN。** 验证前「控制先行、再注册/恢复、再验证」三处已一致，三个指定失败输入均不得放行；但最终开放生产仍需明确独立屏障的解除与已恢复状态分支。
- **B23-T08-R01：OPEN。** namespace 误作准入机制的子问题已解决；上一轮明确要求的污点 effect/NoExecute 分支尚未完成，不能据局部修正关闭整个 ID。
- 本轮没有新的独立发现；仍需针对上述原项残余修订并复核，**不宣布 T05-08 或 Batch 23 审阅通过**。不扩大结论为原有「验证前直接放生产」风险仍然存在。
- 其他已 CLOSED 项本轮不重新判定；正文仍为 `draft / not_verified`，不把文档核对、结构检查或模型审阅当作硬件与恢复验证。

## 证据边界

### 本轮实际重新打开的上游材料

| 编号 | 材料与精确定位 | 本轮用途与限制 |
|---|---|---|
| K01 | [Kubernetes v1.32 Safely Drain a Node — Use kubectl drain to remove a node from service](https://v1-32.docs.kubernetes.io/docs/tasks/administer-cluster/safely-drain-node/#use-kubectl-drain-to-remove-a-node-from-service) | 重读 unschedulable 容忍、直接 nodeName 的例外与维护后 uncordon；只支持这些机制，不证明 cordon 是绝对屏障 |
| K02 | [Kubernetes v1.32 Taints and Tolerations — Concepts](https://v1-32.docs.kubernetes.io/docs/concepts/scheduling-eviction/taint-and-toleration/#concepts) | 重读 nodeName 与 NoSchedule/NoExecute 的区别、匹配 effect 及 NoExecute 的持续运行约束；支撑 R01 尚存子条件 |
| K03 | [Kubernetes v1.32 Namespaces](https://v1-32.docs.kubernetes.io/docs/concepts/overview/working-with-objects/namespaces/) | 重读资源作用域与 Not all objects are in a namespace；Node 非 namespaced 资源，不能把 namespace 自身当节点级准入机制 |
| K04 | [Kubernetes v1.32.0 node_unschedulable.go](https://github.com/kubernetes/kubernetes/blob/v1.32.0/pkg/scheduler/framework/plugins/nodeunschedulable/node_unschedulable.go#L130) | GitHub 只读连接器重新取得原文件 L95–163；Filter 检查 node.spec.unschedulable 与相应 NoSchedule 容忍，不按 namespace 豁免。补充证据仅限定该发布源码，不代表所有 v1.32 补丁或所有调度器 |
| K05 | [Kubernetes v1.32 Node Shutdowns — Non-graceful handling / Forced storage detach on timeout](https://v1-32.docs.kubernetes.io/docs/concepts/cluster-administration/node-shutdown/#non-graceful-node-shutdown-handling) | 重读真实关机前提、人工移除 out-of-service、仍有写入者时 force detach 的风险；不据此证明任何 CSI 驱动已经卸卷 |
| S00 | [Slurm 发布 tag 对象](https://api.github.com/repos/SchedMD/slurm/git/tags/9d1ef1877186d8101769352831c8f0fe303df31c) | 重新取得 `slurm-24-11-7-1`、24.11.7 release 消息及其 commit `defaf214db2e55326f45ab08f1bde5b2036d9f5d`；对象报告 unsigned，不声称签名验证 |
| S01 | [Slurm 24.11.7 scontrol.1](https://github.com/SchedMD/slurm/blob/defaf214db2e55326f45ab08f1bde5b2036d9f5d/doc/man/man1/scontrol.1) | 固定 S00 的 commit，重新读取原文件 L1700–1920，重点 NODES—UPDATE 的 DRAIN/RESUME/UNDRAIN 与 ResumeAfter；节点状态动作不等于已证明生产排除控制解除 |
| S02 | [Slurm 24.11.7 reservations.shtml](https://github.com/SchedMD/slurm/blob/defaf214db2e55326f45ab08f1bde5b2036d9f5d/doc/html/reservations.shtml) | 同 commit，重新读取原文件 L1–170、L240–315，核对受限资源、无限期维护调查 reservation、Modification/Deletion；不能据此假定现场已配置或已撤销屏障 |

Kubernetes 页面均使用 v1.32 静态快照，不用当前主版本页面替代。Slurm 24.11.7 归档 `scontrol.html`、`reservations.html` 本轮均尝试重开，但网页工具返回 `Internal Error`，未取得可读正文；该结果不是 HTTP 404 证据。随后成功通过官方 GitHub 仓库连接器核对同版本 tag 及 S01/S02，结论仅依据成功取得的内容，不声称核对了归档 HTML 字节内容或生成时间。另一次默认分支代码搜索仅用于探索，及一次固定 commit 的 raw URL 读取失败，均未作为版本语义依据；本轮未据此声称检查了 Slurm 节点管理实现。

### 本地检查、写入与未验证事项

- 已阅读 `README.md`、`docs/authoring-guide.md`、`content-outline.md` 及用户提供的根规则；在本轮涉及的 docs/knowledge/sources 子树未发现更深层 AGENTS.md。
- 运行 `PYTHONDONTWRITEBYTECODE=1 make check`：**PASS，100 content entries / 469 sources**。检查范围只是结构与本地文件链接，不检查远程页面、技术正确性、报告判定或现场执行结果。
- **未运行 `make build`**：它会写 `build/catalog.json`、`build/catalog.md`，与本轮只允许创建本报告的限制冲突。未修改 `src/kb/`，不运行测试、硬件验证或集群操作。
- 17:16:08（UTC+08:00）建立内存文件指纹基线，覆盖 471 个普通文件，排除 `.git`、`.venv`、`.agents`、`.codex`、`__pycache__`；17:18:16 写报告前检查时，发现 T05-07/T05-09 第二轮报告及另两篇非目标正文已变化，并新增 T05-06 第二轮报告。这些变化发生在本轮写入前，未读取其变更内容、未修改、未作作者归因。正文、第二轮 T05-08 报告、任务来源记录与登记表的上述指纹均保持一致；不宣称整个工作区无并发变化。
- 本轮写入只涉及本报告，不新建上游镜像、缓存文件、配置或证据附件。不改来源登记表，也不追改历史模型记录。现场 reservation/分区/允许清单、容忍/绑定限制、CSI 卸卷、设备映射、验证窗口/基线及结果均仍无实测证据；本文的反例是来源支持的推演，不是实验记录。
