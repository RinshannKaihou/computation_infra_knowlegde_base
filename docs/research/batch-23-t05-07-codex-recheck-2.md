# Batch 23 · T05-07 第二轮定向复核（Codex）

## 1. 审阅元数据

| 项 | 记录 |
|---|---|
| 任务 / 轮次 | T05-07「多租户争用、公平性与容量验证」；承接上一轮独立审阅角色，对 C04、C05、C06、R01 做第二轮定向复核，并检查相关修订是否引入新问题 |
| 复核基准 | [上一轮复核报告](batch-23-t05-07-codex-recheck.md)第 2.1–2.3 节和 R01 的关闭条件；作者修订说明不是关闭依据 |
| 实际模型 / effort | **`unknown / unknown`**。当前接口未暴露可核验的实际模型及推理档位；不能以仓库约定、历史报告或“同一审阅者”的角色连续性推定模型配置 |
| 执行方式 | 当前 Codex CLI 会话直接审阅；未派发子代理，未另行启动其他模型，未修改历史模型记录 |
| 日期 / 时区 | 2026-10-18，Asia/Shanghai（UTC+08:00） |
| 写入范围 | 仅新增本报告；不修改正文、作者来源记录、来源登记、计划、代码或仓库 `build/` |
| 取证方式 | 重读当前正文与上一轮关闭条件；通过 GitHub 连接器重新读取固定 commit 的 Kueue 文档/API、Slurm 同版本文档源码及优先级实现、Ascend 两份特性文档；另重新打开 NVIDIA MPS 官方文档 |
| 验证范围 | 文档和方法的定向复核；未连接集群、提交任务、变更策略、预置历史、重配设备或终止客户端，不构成硬件验证 |

主审材料：[正文](../../knowledge/05-cluster-platform/contention-capacity-validation.md)，下文简称 **P**。P 为本轮实际读取的 199 行版本，行号均指原始 Markdown，不是网页转换行号。另核对 [README](../../README.md)、[编写指南](../authoring-guide.md)、[领域边界](../../content-outline.md)、[T05-07 计划](../../plans/full-coverage-backlog.yaml)、[作者来源记录](batch-23-t05-07-sources.md)和[来源登记](../../sources/registry.yaml)。上游证据编号 E01–E09 均为**本轮重新取得**，不沿用上一轮编号含义。

2026-10-18 17:06（UTC+08:00）记录的输入 SHA-256：

| 文件 | SHA-256 |
|---|---|
| P | `8b8d98b22c25bac186f32a839dff3655c72c56a897d2d28a13ee28695dd3501e` |
| 上一轮复核报告 | `b3fd1de82f7458f64f2cd42d7994bd0cae90b51e1386e6651fb909efd2a6b673` |
| 作者来源记录 | `26644ab94c0bc3ffdb9469f248a88535427a5a2af0443bb5cd3c25ffecf48d9c` |
| 来源登记 | `a336ce6edc17521e79c164d254c2fb272dde9cb60aea8b978ac5018262cce62c` |

## 2. 逐项复核表

**CLOSED 仅表示该发现的文档关闭条件已满足；不代表实验已执行或平台组合已验证。OPEN 保留原 ID，不把旧问题的剩余部分另编为新发现。**

| 发现 / 级别 | 判定 | 当前证据位置与核验结果 | 剩余要求 / 关闭边界 |
|---|---|---|---|
| **B23-T07-C04 / P2** | **OPEN（部分关闭）** | P L105（步骤 2）、L125、L182：已要求说明初态如何建立，列出匹配预置历史、交换顺序的配对轮次、按各轮历史预测准入顺序三类可审查路线，并设“不满足则不据等待差异判公平策略”的门槛；不再只是记录后宣称控制完成。P L105、L127、L182 也补齐真实 association、QOS、`TRESBillingWeights` 与计费口径；未配置计费权重时 Raw Usage 为 CPU-seconds，与 E04 相符。**但 Slurm 有效优先级权重及实际贡献仍未成为检查门槛**：没有要求核验 `PriorityWeightFairshare` 和其他有效优先级因子的贡献；L127 的“FairShare 只是多因子之一”和 L199 的“站点权重待确认”仍只是说明/未知项。E05 的加权公式及 E06 的实际乘权求和实现支持这一差别 | 将 Slurm 有效优先级权重及 A/B 作业的因子贡献接入步骤 2 和完成判据；无法确认或公平因子没有有效贡献时，不按等待先后裁决该公平策略。初态方法和 CPU-seconds 修订无需重做；详见 2.1 |
| **B23-T07-C05 / P2** | **CLOSED** | P L110（步骤 7）与 L183（完成判据）均明确要求“参数/对象 → 生效时机/条件 → 实际生效证据 → 不满足时停止/降级”；步骤同时禁止无可用观测时作该层隔离的因果结论，完成判据也禁止没有生效证据时归因。L110 保留单变量、实际并发/设备身份/资源形状、模式/profile 改变重建基线及并发下降的策略权衡。E03 的准入过程与 E08/E09 的共享限额机制不能互相替代，修订没有再把配置存在当成执行生效 | 满足上一轮要求的可审查记录结构及缺证据分支；不要求在未执行的设计中伪造各控制的现场有效值，也不要求新增通用部署命令。实际选用的控制仍须在执行前填实证据 |
| **B23-T07-C06 / P2** | **CLOSED** | P L109（步骤 6）与 L184（完成判据）均要求预登记共同分析窗口、采样间隔、时间戳误差、各层相对基线变化判据，并在无法分辨先后时保留并列候选/证据不足。L109 明确区分“充分观测下未检出显著退化”和“采集缺失或分辨率不足”；L185 给出候选边界、给定负载/窗口下未观察到显著退化、证据不足无法排序三类结论。两处不再把后两类合并为 unknown，也没有把候选直接当根因 | 两处一致；L184 的“共同窗口”与 L109 的“共同分析窗口”无实质差异。检测阈值/持续条件须落实在预登记变化判据中；不声称上游规定了通用采样值或统计阈值 |
| **B23-T07-R01 / P3** | **CLOSED** | P L19–20 已加入两个既有 Ascend source ID；L162 的静态/动态 vNPU、vCANN-RT 论断分别就近链接固定 commit 的 HDK 与 vCANN-RT 特性说明；作者来源记录 L24–25 已新增两行映射。来源登记 L5796–5815 的 ID、URL、revision 与正文链接一致。重新读取 E07：HDK 的原理/使用说明/约束支持切分与分配概括；vCANN-RT 特性页支持时分复用。P L162 仍明确跨 vNPU 故障隔离/QoS 未证实、实际未执行 | 已形成“论断 → 精确页面 → source ID → registry → 作者来源记录”的可追溯链。正文末尾没有再次重复列出这两个链接，不妨碍就近引用闭合；未把厂商机制说明升级为 Kueue/Slurm 与 Ascend 组合验证 |

### 2.1 C04：初态方法已补，但不能用计费权重替代优先级权重

**本轮认可的修订：** P L105 和 L182 不再停留在“初态已控制”的结论句，而是要求在三类路线中给出初态建立/预测方法，缺项则限制结论。结合 L125 的基线前后、并发前历史状态、采样窗口及禁止清零生产账本，已经满足上一轮所要求的**方法框架**。这里不因没有现场轮次、历史数值或实际实验数据维持 OPEN；真实 association 与计费口径的检查要求也已有实质补充。

**仍未满足的是上一轮 2.1 明确提出的有效优先级权重检查：**

- P L105 和 L182 的 Slurm 清单包含 `PriorityType`/Fair Tree、association、QOS、`TRESBillingWeights`，却没有要求读取 `PriorityWeightFairshare`、其他启用因子的有效权重及它们对本轮 A/B 作业的实际贡献。L182 的“权重”出现在 Kueue 分支，不能据此视为 Slurm 已覆盖。P L127、L199 对多因子和待确认站点权重的描述也没有补上这个门槛。
- E04/E05 区分两件事：`TRESBillingWeights` 决定资源使用怎样计入账本；`PriorityWeightFairshare` 决定公平因子怎样参与作业优先级。E06 的 `_get_priority_internal` 先把 fair-share 因子乘 `weight_fs`，再与其他加权因子求和，不能由计费权重已核验推出公平优先级确实影响排序。
- **反例是方法推演，不是现场事件：** 即使 multifactor/Fair Tree、association、QOS 和计费历史均已确认，若 `PriorityWeightFairshare=0`，fair-share 因子对该加权优先级就没有贡献；即使非零，其他有效因子仍可能主导结果。现有清单不能排除此分支。E05 还说明整体调度评估顺序并非只有作业优先级，不能把实际启动次序机械等同于公平因子排序。

**最小关闭要求：** 在步骤 2 与完成判据中明确要求核验 Slurm 生效的优先级权重（至少包含 `PriorityWeightFairshare`）及 A/B 作业的有效因子贡献，并据其实际历史、shares 层级、association、QOS、计费/衰减口径解释预期；不能确认这些贡献、或该公平因子无有效作用时，不根据等待差异判定其公平策略。可保留为待执行时必填的审查记录，无需现在虚构现场值或额外执行命令。

### 2.2 C05/C06：记录要求不是现场结果，但已构成关闭门槛

C05 现在要求的是具体所选控制的四段记录，并明示缺证据禁止归因；不是只列控制层名称。以重新打开的 E09 为例，uniform active-thread 限额的生效与客户端启动关联，且有有效设备属性观测入口；这说明为何“配置已保存”不能替代“当前对象确已生效”。P L110/L183 的要求能容纳并强制审查这一区别；不应在本轮另加“必须部署所有控制路线”的关闭条件。

C06 的两处文本现在使用相同的证据质量分流：观测充分且未检出变化，结论受给定负载/窗口限制；缺采集或分辨能力不足，结论是无法排序；有候选时还需干预/恢复证据才能推进因果解释。P L84、L109、L184–185 相互兼容。本项属于实验设计内部一致性核验，不是拿厂商文档代替统计设计或现场检测能力验证。

## 3. 新增发现

**本轮未确认需要从 B23-T07-R02 起单独编号的新增发现。**

- C04 的优先级权重残留已在上一轮 2.1 中提出，继续使用 **B23-T07-C04 / P2 / OPEN**，不重复登记为 R02。
- C05、C06 没有发现修订引入新的控制生效或结果分类矛盾；R01 的来源补齐也没有引入已执行、跨实例 QoS 或平台组合兼容性保证。
- 此结论仅覆盖本轮定向范围及其相邻约束，不表示重新完成全篇、其他任务或所有外链的全面审阅。

## 4. 结论

- **本轮 4 项：3 项 CLOSED（C05、C06、R01），1 项 OPEN（C04，P2）。** C04 中初态控制方法、真实 association 和计费口径已有实质进展，但原要求的有效优先级权重/因子贡献门槛仍未补齐。
- **不能声明 T05-07 已全部复核通过。** 建议仅对 C04 的上述残留修订后再做定向复核；不需要重开本轮已关闭项，也不把待现场执行本身当作新的文档缺陷。
- 上一轮已关闭的 C01、C02、C03、C07 不在本轮重新裁决范围内。本轮未发现相关新增文本要求撤销它们的原判定，但不声称对它们重做完整上游复核。
- P 保持 `draft / not_verified`、空环境/证据引用和“未执行”说明符合现有证据；模型审阅通过与实验验证必须分开记录。

## 5. 证据边界

### 5.1 本轮重新取得的关键上游材料

以下 GitHub 材料均经连接器请求指定 ref，返回原文和 blob SHA；不是仅依据作者来源笔记或上一轮摘要。以文件名、节名和函数名定位；原文件范围仅对本轮按该范围读取的源码使用。

| 编号 | 版本 / 精确材料 / 本轮位置 | 支持范围与限制 |
|---|---|---|
| E01 | Kueue `911a822a49bcfd99c9c62203a009efa4130ad604`：[Admission Fair Sharing](https://github.com/kubernetes-sigs/kueue/blob/911a822a49bcfd99c9c62203a009efa4130ad604/site/content/en/docs/concepts/admission_fair_sharing.md)，How it works、Entry Penalty、Configuration、Observability；blob `8ca78993495b26cca7a48efff6d63992dc524693` | 同 CQ 多 LQ 历史准入排序、衰减/采样/资源权重、CQ 显式启用、LQ weight 和历史状态。没有把示例参数当成默认值、匹配历史或现场已生效证据 |
| E02 | 同 Kueue commit：[localqueue_types.go](https://github.com/kubernetes-sigs/kueue/blob/911a822a49bcfd99c9c62203a009efa4130ad604/apis/kueue/v1beta2/localqueue_types.go)，本轮读取原文件 L120–290 请求范围，包含 `LocalQueueFairSharingStatus`、`LocalQueueAdmissionFairSharingStatus`；blob `8de00fbd6bd55b3dcf8351fbdd56538ddd4a325e` | 区分嵌套历史用量/更新时间与 `weightedShare`；字段定义存在不证明现场值已正确填充 |
| E03 | 同 Kueue commit：[Admission](https://github.com/kubernetes-sigs/kueue/blob/911a822a49bcfd99c9c62203a009efa4130ad604/site/content/en/docs/concepts/admission.md)，两阶段准入说明；blob `c2f4d205902d0f24a37838f3b0921156ca2e4b98` | 配额预留与 AdmissionChecks 的准入对象，不提供运行期 GPU/主机/网络/存储隔离证明 |
| E04 | Slurm [release tag 对象](https://api.github.com/repos/SchedMD/slurm/git/tags/9d1ef1877186d8101769352831c8f0fe303df31c)重新确认 `slurm-24-11-7-1` 指向 `defaf214db2e55326f45ab08f1bde5b2036d9f5d`；该 commit 的 [sshare.1](https://github.com/SchedMD/slurm/blob/defaf214db2e55326f45ab08f1bde5b2036d9f5d/doc/man/man1/sshare.1)，DESCRIPTION、SSHARE OUTPUT FIELDS、FAIR_TREE MODIFICATIONS；blob `5f44c4d87dc31aadaf21cf89adfce0a52e9f28b3` | 核验版本、multifactor 依赖、Raw Usage 未配置 `TRESBillingWeights` 时的 CPU-seconds 回退及 Fair Tree 字段；没有执行 `sshare` |
| E05 | 同 Slurm commit：[priority_multifactor.shtml](https://github.com/SchedMD/slurm/blob/defaf214db2e55326f45ab08f1bde5b2036d9f5d/doc/html/priority_multifactor.shtml)，Job Priority Factors In General（另定向重读原文件 L88–148）、Fair-share Factor（L235–300）、Configuration；blob `3f4d5ce47f7d4e1ca55efa756a1b64a14fc8e8ef` | 独立的优先级乘权与账本计费、整体调度评估次序。版本一致的文档源文件不等于已取得归档 HTML，也不证明站点有效配置 |
| E06 | 同 Slurm commit：[priority_multifactor.c](https://github.com/SchedMD/slurm/blob/defaf214db2e55326f45ab08f1bde5b2036d9f5d/src/plugins/priority/multifactor/priority_multifactor.c)，本轮读取 L1–215、L550–730、L1820–2010；重点 `_get_priority_internal` 中 fair-share 乘 `weight_fs` 后与其他因子求和；blob `1ad1c680c64f5f42d32975a19d987a11bede1961` | 用同版本实际实现交叉核验 C04 的有效贡献问题；只审查这些片段，不声称完成整个调度器、配置加载或完整 Fair Tree 算法审计 |
| E07 | Ascend `44385c13d7b1d87def35f1604e8be4d16de6ca4e`：[HDK 特性说明](https://github.com/Ascend/mind-cluster/blob/44385c13d7b1d87def35f1604e8be4d16de6ca4e/docs/zh/scheduling/04_usage/02_virtual_instance/00_virtual_instance_with_hdk/01_description.md)，原理介绍、产品支持说明、使用说明、使用约束，blob `09228039a611477372ffcaa432a8a921e5233edf`；[vCANN-RT 特性说明](https://github.com/Ascend/mind-cluster/blob/44385c13d7b1d87def35f1604e8be4d16de6ca4e/docs/zh/scheduling/04_usage/02_virtual_instance/01_virtual_instance_with_vcann_rt/00_description.md)，特性、原理、使用说明/约束，blob `0e467cec4a97ee9d09f321a416d2942d02f0a309` | 支持 P L162 的机制概括和 R01 链接核验；vCANN-RT 页还限定仅推理、requests 的百分比含义。未由“资源隔离性好”推出跨 vNPU 故障隔离/QoS 保证，未沿其可变外链认证完整运行时组合 |
| E08 | NVIDIA device plugin `487d7a93894b0f3ad08097169593972eb3ca8206`：[README](https://github.com/NVIDIA/k8s-device-plugin/blob/487d7a93894b0f3ad08097169593972eb3ca8206/README.md)，原文件 L350–380 的 Shared Access to GPUs；blob `44594d4343967a313ff268223c8f638de005062c` | 共享模式与控制层边界；本轮只重读该范围，不重新认证全部部署参数、插件版本与驱动组合 |
| E09 | NVIDIA [When to Use MPS](https://docs.nvidia.com/deploy/mps/when-to-use-mps.html)，2026-10-18 重新打开，重点 Dynamic Execution Resource Provisioning、Application Considerations | uniform active-thread 限额与启动时机/有效属性、限额不等于专用资源预留、未同步终止风险；可变官方页面，不当作固定插件版本的组合验证或操作授权 |

### 5.2 访问限制与方法边界

- 固定版本材料以 GitHub 连接器返回的指定 commit 原文与 blob 为主要依据，并补充打开对应 GitHub 网页；没有以搜索摘要或最新分支替代固定版本。NVIDIA 为另行打开的可变官方页面，不能套用这些固定版本身份。
- 本轮重新请求 Slurm 24.11.7 的 `sshare.html`、`priority_multifactor.html` 归档页，网页接口返回 Internal Error，**未取得归档 HTML**；不能据此声称 HTTP 404。采用 E04 已确认 release 对应 commit 的文档源码与 E06 实现，不声称与归档 HTML 逐字一致，也不独立确认作者记载的 man2html 页脚时间。
- 取得上游机制与源码只能核验方法应检查什么，不能证明现场初态匹配、控制实际生效、计费/优先级配置正确、时间分辨率足够或任何性能改善。不存在本轮实测历史账本、有效权重、两租户采样数据或隔离干预结果。
- 本轮未重新审计全部来源、许可证、MLCommons Storage、Ascend 模板/动态调度全文、最低固件/CANN 矩阵、全部 MPS/MIG 路线或其他 T05 任务；R01 关闭不依赖这些范围已获验证。C06 的判断是实验设计评审，不虚构统一采样精度或显著性数值。
- 工作区开始时已有多份未提交/未跟踪材料；不提交、不回滚、不整理它们。输入哈希标识实际读取版本，不声称工作区是原子快照。

### 5.3 本地检查与写入范围复验

- 本报告落盘后执行 `PYTHONDONTWRITEBYTECODE=1 make check`：**PASS，100 content entries / 469 sources**。在仓库外临时镜像执行 `make build`（使用本仓库既有 Python 环境并禁止写 bytecode）：**PASS，100 / 469**。生成物仅写临时镜像，不修改仓库 `build/`；这些检查不验证远程内容或技术结论。
- 写报告前对 463 份工作区文件记录 SHA-256（排除 Git、虚拟环境、工具目录与 Python 缓存），17:16 复验确认第 1 节四份主审材料哈希均未变化，未发现原文件被删除。
- **并行变更边界：** 同次复验发现 `knowledge/05-cluster-platform/node-drain-resource-reclamation.md` 内容变化，以及另外出现 T05-08、T05-09 的第二轮复核报告。本审阅未写入或回滚这些文件，也不采用其复核结论；本轮仓库写操作仅针对本报告。检查/隔离构建只代表执行或复制时所见工作区，不构成原子快照保证。
- 未修改 `src/kb/`，未新增测试、运行硬件测试或采集实时集群状态。
