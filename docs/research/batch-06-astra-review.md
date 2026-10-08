# 第六批独立审阅记录

审阅日期：2026-09-30。审阅者：独立 `gpt-6-astra / xhigh`。初审结论：**2 项 P2、2 项 P3，待修订与定向复核；未发现 P1。** 以下行号以本轮初审读取的源文件为准。

## 范围与方法

逐篇阅读 T01–T04 的 12 篇 procedure/case/experiment，阅读三份 batch-06 研究/交付记录，核对本批 7 项新增来源登记、对应章节入口、平台/任务路径和 backlog/填充计划。T05–T07 不纳入本轮技术结论；并行写作造成的临时总数或来源差异未作为本批缺陷。

遵循 AGENTS.md、README.md、docs/authoring-guide.md 与 content-outline.md；仅新增本报告。只读核对官方文档、固定源码、GitHub Issue/评论/PR 与公开 API，未安装、构建或运行上游软件，未访问容器、集群、GPU/NPU，未执行硬件诊断、通信测试或故障注入。没有运行 `make check`、`make build` 或测试；主任务报告的 48 条目/59 来源 PASS 是其结构检查结果，本审阅不重新声明为独立实测。

## 发现

### B06-P2-01：HCCL 案例遗漏报告者后续分析和 AI_CPU 对照

- 本地定位：[hccl-timeout-source-case.md](../../knowledge/03-communication/hccl-timeout-source-case.md) 第 55、65、73、82–89、104–106 行；[通信来源记录](batch-06-communication-sources.md) 第 96–108 行及相应待办/来源摘要；[registry.yaml](../../sources/registry.yaml) 第 737–749 行。
- 问题：案例仅根据 Issue 正文整理单/双开关 workaround，写成没有可见评论、关闭理由/日期未知。GitHub HTML 抽取确实未呈现活动正文，但公开 comments API 返回了三条此前已有评论，遗漏改变了“已掌握哪些处置证据”的判断。
- 精确原始证据：报告者 MarinaMiao 在 [2026-08-15 03:19:11 UTC 的评论](https://github.com/vllm-project/vllm-ascend/issues/14296#issuecomment-5300280446)中给出 MoE/AllGather 抢核初判、带完整日期的 2026-08-15 plog 摘要，援引 HCCL_OP_EXPANSION_MODE 文档，并报告切换为 `AI_CPU` 后症状消失，同时提醒性能可能受影响；这是一项不同于关闭两个框架开关的对照。 [2026-08-17 07:40:21 UTC 的跟进](https://github.com/vllm-project/vllm-ascend/issues/14296#issuecomment-5313215244)作者关联为 CONTRIBUTOR，正文明确标注 Automated Response，不能升级为维护者独立验证。[2026-09-22 03:17:18 UTC 的评论](https://github.com/vllm-project/vllm-ascend/issues/14296#issuecomment-5770710734)只转述一个可能解决问题的 PR 编号；[Issue API](https://api.github.com/repos/vllm-project/vllm-ascend/issues/14296)同时给出该时刻关闭、`state_reason=completed`。
- 影响：读者会漏掉已经公开的环境变量对照及更具体日志，错误地把尚未完整读取的活动区当成“没有后续证据”。这不是因为缺少本地复现而提出的缺陷。
- 建议：补三条评论的作者、时间、证据级别与结果边界；明确初始正文日志与后续另一时间窗口日志不能拼成一次运行。保留原始单/双开关表述差异，并单独记录 AI_CPU 对照。将状态改为“completed 关闭，仍无可核实修复链/本库复现”；最后评论中的 `pr#14296` 不能直接当成修复 PR，因为同仓库 #14296 已是当前 Issue。评论所引官方页为 `latest`，本轮 web 工具未能取得该页正文，因此“多通信域并行限制”目前只能写为报告者援引，不能自动视作已核对的 CANN 9.0.1 支持声明。

### B06-P2-02：独立 Docker 路径无法满足设备流程的必经步骤与完成条件

- 本地定位：[ascend-device-visibility-triage.md](../../knowledge/05-cluster-platform/ascend-device-visibility-triage.md) 第 19、38–40、62–65、96 行。
- 问题：适用范围明确包含独立 Docker client/runtime，并要求区分两条路径；但步骤 2 的正常出口只能进入 Kubernetes，步骤 3–4 强制检查 Device Plugin、资源账本与 Allocate，完成条件又要求串齐这些证据。合法的独立 Docker 环境没有这些对象。
- 精确原始证据：MindCluster 固定 commit `44385c13d7b1d87def35f1604e8be4d16de6ca4e` 的 [Device Plugin 文档第 5–7 行](https://github.com/Ascend/mind-cluster/blob/44385c13d7b1d87def35f1604e8be4d16de6ca4e/docs/en/scheduling/developer_guide/installation_deployment/manual_installation/04_ascend_device_plugin.md#L5-L7)明确区分需要调度插件的场景和只需容器化/监控、不需插件的场景；同快照的 [Docker client 文档](https://github.com/Ascend/mind-cluster/blob/44385c13d7b1d87def35f1604e8be4d16de6ca4e/docs/en/scheduling/usage/containerization/02_usage_on_the_docker_client.md)给出的入口是容器创建规格、runtime 变量及挂载结果。
- 影响：Human/Agent 按表执行时，会把独立 Docker 下正常不存在的插件/Pod/Allocate 证据当作最早断点，或无法完成一个被声明适用的流程。
- 建议：在起始身份和主机检查后显式分流。Kubernetes 路径进入插件/资源/分配步骤；独立 Docker 路径以容器创建参数、设备/挂载白名单和 runtime 配置作为预期，直接核对实际注入与进程枚举。证据表与完成判据也条件化；独立 Docker 的 Pod/Allocate 等字段记“不适用”，不能记“缺失/异常”。

### B06-P3-01：PR 审阅评论链接没有指向支持该结论的真实评论

- 本地定位：[环境与设备来源记录](batch-06-environment-device-sources.md) 第 122 行。
- 问题：该行把“审阅者称 hack、作者答复将改进”链接到 `discussion_r2320917327`。实际 PR 评论接口中对应的审阅意见为 [`discussion_r2319156564`](https://github.com/vllm-project/vllm-ascend/pull/2541#discussion_r2319156564)，作者回复为 [`discussion_r2319163741`](https://github.com/vllm-project/vllm-ascend/pull/2541#discussion_r2319163741)，分别发表于 2025-09-03 14:24:14 和 14:26:41 UTC。
- 影响与建议：论断本身得到真实评论支持，但精确定位失效；更换为两条正确评论链接即可，不需要改变补丁范围或现场复验未知的结论。

### B06-P3-02：研究记录仍把无资源请求直接等同于容器无设备

- 本地定位：[环境与设备来源记录](batch-06-environment-device-sources.md) 第 140 行 C0；正式 [ascend-device-visibility-experiment.md](../../knowledge/05-cluster-platform/ascend-device-visibility-experiment.md) 第 56、60、68、76、103 行已加入限制。
- 问题：研究表仍只写“同节点/镜像，不请求 NPU”，就预期没有容器设备；正式实验已正确要求排除 privileged、hostPath、人工设备挂载及 runtime 默认注入，因此两份交付记录不一致。
- 原始证据：固定 [MindCluster Docker client 文档](https://github.com/Ascend/mind-cluster/blob/44385c13d7b1d87def35f1604e8be4d16de6ca4e/docs/en/scheduling/usage/containerization/02_usage_on_the_docker_client.md)明确存在 runtime 环境变量和人工设备挂载路径；[Kubernetes v1.32 Device Plugin 接口](https://v1-32.docs.kubernetes.io/docs/concepts/extend-kubernetes/compute-storage-net/device-plugins/#device-plugin-implementation)只规定插件分配机制，并没有给出“不申请扩展资源便不可能访问任何设备”的保证。
- 影响与建议：正式实验当前没有该漏洞；同步研究 C0 的隔离/runtime 前提，并保留前提不成立时无法判断，避免后续编写重新引入旧假设。

## 已核对且未形成缺陷的重点

| 范围 | 本轮实际核对 | 结论边界 |
|---|---|---|
| T01 | 固定 TorchNPU README 的安装、Quick Verification、Python 表和 CANN/Extension 矩阵；#1188 正文、两条真实评论及 completed 关闭状态 | 同行声明没有被写成运行兼容；安装顺序建议没有被写成报告者复验；2.5.1 历史案例没有外推到 2.6/8.3 |
| T02 | Kubernetes v1.32 接口；固定 MindCluster Docker/插件文档；#2557 正文与三条评论；#2541 PR diff、审阅评论、合入 API 和固定 envs/connector 代码 | merge commit `07d44ade194b018ae2cc172482d55cb746c5fd0e` 与 DP/TP 物理 ID 切片吻合；新增单测只覆盖有限 mock 路径；PHYSICAL_DEVICES 限于当时 Mooncake 实现，现场复测未知 |
| T03 | HCCL 8.1.RC1.alpha001 官方 PDF §9.1.2；#14296 正文、全部三条评论及 Issue API | EI0002、rank 缺席/错序、设备/链路与 timeout 预算没有混成单一根因；8.1 指南与 CANN 9.0.1 案例分开；上述评论遗漏需修订 |
| T04 | NCCL 2.27.5 env/troubleshooting/RAS；PyTorch 2.8 环境变量页；#118369 正文与全部八条评论、关闭 API | RAS 自 2.24 起、trace-buffer 依赖、IB timeout 与 watchdog 分层准确；SeqNum 限同 group；rank 0 缺行/利用率保留为假设；stale/not_planned 不作修复；现代观测变量未倒推 2.1.2 |
| 状态与许可 | 12 篇 frontmatter、7 项新增登记、固定 PR Apache-2.0 与 PyTorch v2.8.0 LICENSE、PDF 版权页 | 全部 draft；P/C source_checked 与 X not_verified 分开，无伪造运行结果；Issue/审阅文本、仓库自有代码/文档、厂商 PDF 和软件包许可未合并 |

导航与 backlog 保留稳定 ID 和主归属，T01–T04 各三篇处于 reviewing，路径引用正文；没有把未来网站/API/执行器宣称为实现。未发现需要用内容测试替代本次技术修订的理由。

## 未核实限制与复核入口

- 本轮官方 PDF 取得文本，截图接口返回 cache miss，未完成视觉检查；§9.1.2 可通过章号定位，PDF 抽取索引为 P88–P89（从零计数），印刷页号为 83–84。后续可把正文“第 88–89 页”明确为索引或改为印刷页号，避免页码歧义。
- CANN 8.3 安装页及 #14296 评论引用的 `latest` HCCL 环境变量页本轮 web 打开失败；不把失败当作内容错误，也不声称已独立核实这两页正文。未扩大核验到所有未采用候选 Issue、所有引用的基础条目源码或后续发行版。
- 没有任何本地运行/兼容性/恢复验证。未知硬件、HDK、镜像、目标版本和实验阈值是合理的设计缺口，本轮未强行视为缺陷。
- 修订后定向复核 B06-P2-01 的评论/状态/版本边界及其研究/registry 同步、B06-P2-02 的双路径步骤与完成条件，再核对两项 P3。由主任务负责结构检查与本批最终状态更新。

## 修订后定向复核（2026-09-30）

**结论：四项初审发现均已修订并通过定向复核，本批无未关闭的 P1/P2/P3 发现。** 上文保留初审记录，不表示问题仍存在。此次仅重读受影响正文、研究记录与来源登记，并对照初审已取得的原始评论、API 元数据和固定文档；没有重复执行外部软件或硬件操作。

| 发现 | 修订与复核定位 | 结果 |
|---|---|---|
| B06-P2-01 | `hccl-timeout-source-case.md` 第 24、55、65–68、76、92–96、111–113 行，通信研究记录第 96–108 行和“审阅后的评论补读”，registry 中 `src.vllm-ascend.issue-14296` | 三条评论与 UTC 时间已纳入；AI_CPU 是报告者缓解反馈；自动回复没有升级为独立根因验证；同号 PR 提及未伪造修复链；completed 关闭与修复未证实分开。正文日志和评论没有强行拼成同一次运行，`latest` 手册限制仍归属报告者援引。通过。 |
| B06-P2-02 | `ascend-device-visibility-triage.md` 第 32、38–40、49–55、63–68、80、96、100–105 行 | 初始身份、版本、证据表、步骤 2 分流、Kubernetes 专属步骤 3–4、独立 Docker 的创建规格/runtime 预期、恢复及完成条件已条件化。独立 Docker 不再需要补造 Pod/插件/Allocate 证据。通过。 |
| B06-P3-01 | 环境与设备研究记录第 122 行 | 两个 PR 审阅锚点分别指向 `2319156564` 和 `2319163741`，与本轮已取得的真实审阅/回复相符。通过。 |
| B06-P3-02 | 环境与设备研究记录第 141 行 C0 | 无 NPU request 之外，明确排除 privileged、设备 hostPath、人工挂载/显式旁路，并确认 runtime 不会默认注入设备；前提不成立时不推断不可见，与正式实验一致。通过。 |

HCCL 指南主文、研究记录和 registry 已澄清印刷页号 83–84 与零基索引 88–89。复核时 procedure 的 verification.notes 和 experiment 的末尾链接标签仍保留旧“第 88–89 页”表述，已告知主任务作为非阻断的一致性清理；不影响 §9.1.2 的技术依据或上述四项关闭。

本次未运行 `make check/build/test`，也未改变任何正文或共享文件。主任务说明本次全库结构检查受到下一批 T05/T06 并行新增内容尚未完成登记的影响，待后续集成重跑；本报告不把上一轮 48/59 PASS 写成修订后的全库构建已通过，也不将下一批的临时状态算作第六批技术缺陷。

技术审阅通过只针对这些来源归纳和流程设计；12 篇仍应保留 `draft`，P/C 的 `source_checked` 不等于本地复现，X 仍为 `not_verified`。初审列出的页面获取限制与现场验证缺口继续有效。
