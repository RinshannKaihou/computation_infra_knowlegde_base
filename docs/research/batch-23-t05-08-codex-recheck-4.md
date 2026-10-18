# Batch 23 · T05-08 第四轮定向复核报告

## 审阅元数据

| 项目 | 记录 |
|---|---|
| 任务与轮次 | T05-08「节点摘除、drain 与资源回收流程」；第四轮定向复核 C01、R01，并检查此次修订是否引入新问题 |
| 角色与执行 | 延续同一独立审阅角色，不是正文作者；本会话直接核对正文、历史关闭条件和精确版本上游材料，未委派子代理 |
| 实际模型 | **unknown**；接口未暴露可核验的精确模型标识，不以仓库约定模型代填，也不能证明跨轮底层模型完全相同 |
| 实际 effort | **unknown**；接口未暴露实际 reasoning effort，不把约定的 `xhigh` 当作实际值 |
| 日期与时区 | 2026-10-18，Asia/Shanghai（UTC+08:00） |
| 直接依据 | [第三轮定向复核报告](batch-23-t05-08-codex-recheck-3.md)，重点为其 L46–50 的 C01 最终交接条件、L64–75 的 R01 剩余条件；另核对[初审 C01](batch-23-t05-08-codex-review.md#b23-t08-c01--失败恢复不能先解除隔离)的原始失败门控范围 |
| 唯一写入 | 只创建本报告；不修改正文、历史报告、来源记录、登记表、计划、代码或构建产物 |
| 执行边界 | 只读文档及上游版本材料，运行不生成文件的结构检查；未连接集群，未执行节点、调度、设备、卷或验证负载操作 |

本轮取证并于写报告前确认未变化的文件快照：

| 文件 | 行数 / SHA-256 |
|---|---|
| [正文](../../knowledge/05-cluster-platform/node-drain-resource-reclamation.md) | 230 行；`ca8234a2a4015f80a3614622fc9ecce1fa4837f18c8e8a4be4cbe43ffbfd043a` |
| [第三轮报告](batch-23-t05-08-codex-recheck-3.md) | 111 行；`b4bd590a1545aff5bbdca59ae560567b42f7e65348b5e2d2ae9c07e660a2f415` |
| [任务来源记录](batch-23-t05-08-sources.md) | `ea9e73731beeda279c989dd814ccb2f7dc9ed52b404524c1a466c19a8ab760ef` |
| [来源登记表](../../sources/registry.yaml) | `a336ce6edc17521e79c164d254c2fb272dde9cb60aea8b978ac5018262cce62c` |

下文「正文 L…」均指上述正文快照的原文件行号。`CLOSED` 针对完整发现 ID，而非仅认可作者本轮修改的一句话；场景代入均为文档逻辑核对，不是现场测试。

## 逐项判定

| 发现 ID | 原级别 | 本轮判定 | 证据与理由 |
|---|---|---|---|
| B23-T08-C01 | P1 | **CLOSED** | L174 已明确最终撤销验证例外与独立生产排除控制，并按当前状态区分「已恢复：仅解除剩余控制，不重复 RESUME/UNDRAIN」与「仍隔离：才执行所需状态动作」；L186、L217 同步。与 L120、L140、L172、L184 的控制先行、再注册/恢复路径一致；L208、L217 仍要求验证负载退出后再次对账，失败门控未退化。详见下节及 S01、S02。 |
| B23-T08-R01 | P2 | **CLOSED** | L185 已指定污点 effect、要求验证 Pod 容忍相应污点，并明确 `nodeName` 只绕过调度器、不豁免未容忍的 `NoExecute`；namespace 只作组织边界，且禁止用它或单独 `nodeName` 替代节点级准入控制。全文其他相关表述未形成相反承诺；原发现的 namespace 与 NoExecute 两个子条件均已覆盖。详见下节及 K01–K03。 |

### C01：最终交接与验证前注册路径闭合

本轮将恢复安排、三层表、主路径和完成判据作为同一流程核对，而非把「验证通过」单独解释成可立即解除一切屏障：

| 门槛 | 正文证据 | 定向判断 |
|---|---|---|
| 验证前注册/状态恢复 | L120、L140、L172、L184：先启用并核实生产排除控制，再执行必要的注册/状态动作；L120 要求成功注册后清 NoResp | 节点状态恢复不是生产放行；没有可核实的持续生产屏障就停止，不能先恢复调度再补控制 |
| 验证与退出后清理 | L173、L188：只允许生产仍被阻断时受控验证，失败返回隔离；L208、L217：验证负载退出后设备、卷、端点与账本再次收敛，才最终放行 | L174 的成功分支受这些明确条件约束，不能在验证负载仍占用资源时提前解除生产排除控制 |
| 最终解除与状态分支 | L174：撤销验证例外及独立生产排除控制；已恢复节点只解除剩余控制，不重复 RESUME/UNDRAIN；仍 DRAIN/cordon 才执行相应动作，并记录当前状态、解除项及核实证据 | 上轮缺失的独立屏障交接与避免重复 RESUME 均已补齐；不再把节点状态命令当作 reservation 等控制已经解除的证据 |
| 同步与失败门控 | L186、L217 同步当前状态分支；L163、L166、L188、L207、L208 保留卸卷、过期分配、验证失败或缺证即停止的条件 | 未因最终交接修订而放宽失败输入；三层表和完成判据没有回到无条件恢复状态的旧路径 |

按当前正文作以下未执行的分支代入：

| 输入 | 应有的最终交接 | 结论 |
|---|---|---|
| Slurm 在已核实的生产排除控制下完成 RESUME、有效注册与受控验证，验证 job/step 已退出、资源再次对账完成 | 撤销验证特殊准入，解除剩余独立生产排除控制并留证；节点已经恢复，不再 RESUME/UNDRAIN | **闭合**。S01 将状态动作与有效注册分开说明；S02 将 reservation 的修改/删除另列，且运行作业未退出时不能删除 reservation。正文不再以重复节点状态动作代替最终控制交接 |
| Kubernetes 为基础设施恢复已在独立生产屏障下 uncordon，随后验证与退出后对账完成 | 解除剩余生产排除控制，不再要求重复状态变更 | **闭合**。L174 的分支标题、L186 的禁止项与 L217 的完成条件共同限定「按当前状态」，不是无条件再 uncordon |
| 节点当前仍处于 DRAIN/cordon | 只有既有验证、退出和对账门槛均满足，才进入 L174 的仍隔离分支并执行所需状态动作 | **有条件闭合**，不是新旁路授权。特别是 Slurm：若新验证 job 因仍 DRAIN 而无法启动，不能用 reservation/分区名义假定它可越过 DRAIN，应回到控制先行的注册路径，或按 L188 停止并记 unknown |
| 必须卸载的 CSI 卷仍未卸载或缺证；设备仍有过期分配；验证失败或缺少基线/结果 | 维持或恢复生产隔离，不进入最终解除屏障分支 | **三类均不得普通生产放行**，分别由 L163/L188、L166/L188、L173/L188/L207–208 阻断 |

L120 的步骤 6 与 L140 的状态例子仍是压缩说明；它们没有另加验证后重复 RESUME 的要求，也没有授权跳过独立生产控制的解除。其「验证后开放普通生产」现在由 L174、L186、L208、L217 给出了完整展开，故与主恢复路径不矛盾。L140 的 `IDLE + NoResp` 也须连同 L120 的有效注册、清 NoResp 理解，不将尚未注册成功当作具备验证条件。

S01 明确 DRAIN 不允许新 job，RESUME/UNDRAIN 各有状态与注册前提；本报告不把正文 L120、L185 的「可覆盖 DRAIN」解释成普通 reservation 能让新 job 在 DRAIN 节点上直接运行。这里核验的是生产排除控制能够先于状态恢复建立、贯穿验证、最后显式解除的文档闭环，不是对任何站点配置能力的证明。

### R01：effect、NoExecute 与直接绑定边界已补齐

L185 的修订不再把「容忍或 nodeName」当成不区分 effect 的替代选项，而是先指定实际污点 effect，再要求相应容忍，并为直接绑定明确保留 NoExecute 限制。K01 的 Concepts 支持这一边界：容忍需与实际污点匹配；`nodeName` 绕过调度器，并不免除未容忍的 NoExecute。匹配容忍也不是验证必然成功或可无限运行的保证，仍须满足 L188、L203–208 的入口、窗口和结果要求。

| 未执行的输入 | 本轮正文覆盖与判定 |
|---|---|
| 验证 Pod 只有专用 namespace，没有可核实的节点级入口 | L185 明确 namespace 只是组织边界、不能单独阻断生产 Pod，禁止用它替代节点级控制；L188 无入口则停止、记 unknown。**不能认定获准验证** |
| 验证 Pod 使用 nodeName，但不容忍节点实际存在的 NoExecute；或只具备 NoSchedule 容忍 | L185 明文不豁免未容忍的 NoExecute；不能因直接绑定就认定具备可持续运行的验证入口，须在生产隔离下停止并核对对应容忍。**原指定反例已覆盖** |
| nodeName 可以绕过 cordon/NoSchedule 的调度限制 | L91、L99 是调度绕过风险说明；L185 仍禁止以单独 nodeName 代替节点级准入控制，L188 要求授权与持续生产阻断。**不等于生产准入或 NoExecute 豁免** |

全文检索并逐处复读的相关位置为：L91、L99 的直接绑定/调度限制，L97 的 out-of-service 容忍例外，L151 的一般污点/容忍排查，L185 的验证准入，以及 L201 的 namespace 身份字段。**未发现把 nodeName 或 namespace 自身当作节点级准入豁免的剩余表述**；L201 的 namespace 只用于身份对账，不是准入承诺。K02 支持 cordon 存在直接绑定等例外，K03 只提供命名空间作用域，不能据此推导节点级放行能力。

## 新增发现

**未发现此次修订引入的独立新问题；本轮不启用 B23-T08-R02 及后续编号。** 已检查解除独立屏障是否提前、是否再次要求已恢复节点 RESUME、是否以最终仍 DRAIN 的分支暗示验证 job 可直接旁路，以及 effect 修订是否重新引入 namespace/nodeName 豁免。上述结论均依赖正文的完整门槛；没有把一般站点未知条件或已经覆盖的原项再编号。

## 结论

- **B23-T08-C01（P1）：CLOSED。** 最终屏障解除、已恢复节点不重复 RESUME/UNDRAIN、仍隔离节点按需状态变更，与验证前注册路径及失败门控一致。
- **B23-T08-R01（P2）：CLOSED。** effect/相应容忍、未容忍 NoExecute 与 nodeName 的边界已经明确；namespace 不再被视为节点级准入机制。
- **本次第四轮定向复核通过，无新增发现。** 这只关闭本轮指定的两个发现，不是重新宣布全文、其他任务或 Batch 23 全部审阅通过；其他历史已关闭项不在本轮重新判定范围内。
- 正文仍为 `draft / not_verified`。本轮不修改编辑或验证状态，不将文档逻辑核对、结构检查或模型审阅当作真实环境验证。

## 证据与执行边界

### 本轮重新取得的上游材料

以下沿用既有报告及来源链中的版本定位，不新增正式来源 ID，也不修改登记表。Kubernetes 只按 v1.32 静态快照核对，Slurm 只按固定 24.11.7 发布对象核对；不以当前主版本或默认分支替代。

| 标识 | 精确来源与定位 | 本轮用途及限制 |
|---|---|---|
| K01 | [Kubernetes v1.32 Taints and Tolerations — Concepts](https://v1-32.docs.kubernetes.io/docs/concepts/scheduling-eviction/taint-and-toleration/#concepts) | 重读 nodeName、污点匹配与 NoExecute 段落；只支撑准入边界，不证明具体 Pod 已匹配或可持续运行 |
| K02 | [Kubernetes v1.32 Safely Drain a Node — Drain the node](https://v1-32.docs.kubernetes.io/docs/tasks/administer-cluster/safely-drain-node/#drain-the-node) | 重读 unschedulable 容忍、直接绑定例外和维护后 uncordon；不把 cordon 视为绝对生产屏障 |
| K03 | [Kubernetes v1.32 Namespaces — Not all objects are in a namespace](https://v1-32.docs.kubernetes.io/docs/concepts/overview/working-with-objects/namespaces/#not-all-objects-are-in-a-namespace) | 重读资源作用域和 Node 非 namespaced 的说明；不把 namespace 自身当节点级准入控制 |
| S00 | [Slurm 发布 tag 对象](https://api.github.com/repos/SchedMD/slurm/git/tags/9d1ef1877186d8101769352831c8f0fe303df31c) | 重新取得 `slurm-24-11-7-1`、24.11.7 release 消息及 commit `defaf214db2e55326f45ab08f1bde5b2036d9f5d`；对象报告 unsigned，不声称签名验证 |
| S01 | [Slurm 24.11.7 scontrol.1](https://github.com/SchedMD/slurm/blob/defaf214db2e55326f45ab08f1bde5b2036d9f5d/doc/man/man1/scontrol.1) | GitHub 只读连接器重新取得原文件 L1700–1920，核对 NODES UPDATE 的 DRAIN、RESUME、UNDRAIN 及注册条件；只核对手册语义，未检查节点管理实现或运行返回码 |
| S02 | [Slurm 24.11.7 reservations.shtml — Modification/Deletion](https://github.com/SchedMD/slurm/blob/defaf214db2e55326f45ab08f1bde5b2036d9f5d/doc/html/reservations.shtml#L248) | 同 commit 重新取得 L240–315，核对 reservation 修改、到期/删除及运行中作业的删除限制；不能据此证明现场控制已配置、已生效或已解除 |

Slurm 24.11.7 归档 `scontrol.html`、`reservations.html` 本轮均尝试打开，网页工具返回 `Internal Error`，未取得正文；不将其说成 HTTP 404。随后通过官方 GitHub 仓库连接器成功取得 S00、S01、S02，以固定发布材料补核，不声称核对了归档 HTML 字节内容。另一次 reservation 原文件 L1–110 读取遇到连接中断，未作为结论依据。

### 本地检查与写入限制

- 已从 `README.md`、`docs/authoring-guide.md` 和 `content-outline.md` 的规则与边界入手；在 docs/knowledge/sources 子树未发现更深层 AGENTS.md。
- 运行 `PYTHONDONTWRITEBYTECODE=1 make check`：**PASS，100 content entries / 469 sources**。仅检查结构与本地文件链接，不证明本报告判断、技术正确性、远程引用或现场行为。
- **未运行 `make build`**：已核对其会写入 `build/catalog.json`、`build/catalog.md`，与本轮只允许创建本报告的限制冲突。未修改 `src/kb/`，未运行测试或生成其他证据附件。
- 17:23:43（UTC+08:00）建立内存 SHA-256 基线，覆盖 475 个普通文件，排除 `.git`、`.venv`、`.agents`、`.codex`、`__pycache__`；17:25:52 写报告前复核，未观察到新增、删除或内容变化。该观察有明确时间边界，不宣称工作区以后不会出现并发修改。
- 17:28:19 再次检查时，除本报告外，观察到新增 `docs/research/batch-23-t05-06-codex-recheck-3.md`，以及 `knowledge/05-cluster-platform/accelerator-sharing-and-isolation.md` 内容指纹变化。本轮未写入这两个路径、未读取其变更内容或作作者归因；不宣称整个工作区只有本报告发生变化。T05-08 正文、第三轮报告、任务来源记录和来源登记表的指纹均未变化，本报告的取证快照仍成立。
- 只写入本报告，不追改历史模型记录，不新增缓存/镜像或修改来源登记。现场 reservation/分区/允许清单、容忍与直接绑定限制、CSI 卸卷、设备映射、验证窗口/基线及结果均仍缺少实测证据；本轮关闭的是文档发现，不是这些现场未知条件。
