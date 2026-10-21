# Batch 31 · T00-04 初审报告

## 会话元数据与结论

| 项目 | 记录 |
|---|---|
| 审阅角色 / 轮次 | 独立批次审阅者；第一轮初审；与正文编写者角色分离，本会话只审阅、只写本报告 |
| 实际执行模型 / 档位 | `gpt-6.1-sol / xhigh` |
| 模型核验方法 | 以环境变量 `CODEX_SESSION_ID` / `CODEX_THREAD_ID` 定位当前 rollout JSONL，读取最新 `turn_context`，交叉核对 `session_meta.id`；不以配置默认值、其他会话或引用文本中的模型标记代替 |
| 模型核验结果 | `turn_context.model=gpt-6.1-sol`、`effort=xhigh`、`cwd=/Users/ywang2397/work/AI_reliability_knowledge_base`；`collaboration_mode.mode=default`，`collaboration_mode.settings={model: gpt-6.1-sol, reasoning_effort: xhigh, developer_instructions: null}`，两层设置一致 |
| 模型核验坐标 | `/Users/ywang2397/.codex/sessions/2026/10/22/rollout-2026-10-22T01-13-11-01a15f73-dd74-7880-b830-bb528c222620.jsonl` L8，时间戳 `2026-10-21T17:13:16.488Z`；`session_meta` 在 L1 |
| 会话 ID / turn ID | `01a15f73-dd74-7880-b830-bb528c222620` / `01a15f73-de7b-7851-af90-47c2f0527e01` |
| 身份结论 | 符合本轮指定模型与档位；当前本地 Codex CLI 会话直接执行，未另启审阅子代理或其他模型。工具输出引用内容中的 `[frontier_llm]` 不作为回退依据，本轮以当前 `turn_context` 为准 |
| 日期 / 时区 | 2026-10-22 / Asia/Shanghai；正文与取证记录的修订日期为 2026-10-21 |
| 执行方式 | 只读本地文件、Git 基线比较、schema/引用检查与定向上游取证；仅新增本报告 |
| 写入范围 | `docs/research/batch-31-t00-04-codex-review.md`；不修改正文、取证记录、来源表、导航、计划、历史审阅或构建产物 |

| 正文基准（审阅开始时先执行 `wc -l` 与 `shasum -a 256`） | 行数 | SHA-256 |
|---|---:|---|
| `knowledge/00-overview/training-lifecycle.md` | 151 | `07681ebe62e5eb1d055bc271f2615a24975d3575b16cbd9fc7b03e8a82f4a1ea` |
| `knowledge/00-overview/inference-lifecycle.md` | 153 | `8ca211d0aec866ede7047664d3ce6f74627cd6eacea32cdb55f48c2fb1b79938` |

**初审结论：需局部修订并定向复核，暂不通过。共 2 项开放发现：P1 0 项、P2 1 项（C01）、P3 1 项（C02）。** 原有主链、表格、计时口径与来源引用均保留；问题集中在新增推理入口的 drain 请求边界和平台证据身份表述，不要求重写正文或扩充领域内容。训练侧在本次有限终态核对范围内满足要求。

优先级：P1＝足以严重误导处置的关键错误；P2＝影响技术准确性、边界或验收判据的必修事项；P3＝局部措辞、定位与可追溯性问题。下文“训练文”“推理文”分别指上表两文，行号以上述摘要为准。

## 范围与方法

已读取 `README.md`、`AGENTS.md`、`docs/authoring-guide.md`、`schemas/content.schema.json` 与 `content-outline.md` 的 00 域归属。完整重读[训练文](../../knowledge/00-overview/training-lifecycle.md)、[推理文](../../knowledge/00-overview/inference-lifecycle.md)和[本任务取证记录](batch-31-t00-04-sources.md)，以 [T00-04](../../plans/full-coverage-backlog.yaml) L7270–7327，特别是 objective（L7288）及三条 acceptance（L7290–7292）为准。报告结构参照 [Batch 30 · T08-05 初审](batch-30-t08-05-codex-review.md)。

本任务是既有基础已覆盖主题的有限最终 v1 链路核对。06/07 首页、02 域新文的独立交付及 backlog 状态同步不在本轮判定范围；读取这些领域正文仅用于核对本任务新增入口实际承载的内容，不重新裁定其整篇审阅状态。

原口径比较采用当前 `HEAD=ef2a6052273529b6ab7fa0899a603f79a7a8f58d` 中的两文与工作区修订版：训练文原 blob 为 `4861e3a1bc12ee26243310b50a21fedabf9224b6`（121 行），推理文原 blob 为 `7a6b0ca152d6c7acf59067b40bd345fbe3dcaebe`（128 行）。逐节、逐表和 Mermaid 块作文本比较，另核对完整 diff；不因新增标题导致行号移动而判作原文变化。

对新增入口逐一核对目标存在性，定向读取其分支差异、状态责任、恢复分层、请求语义与平台限定；检查两文 frontmatter 的 Draft 2020-12 schema、日期、来源与 related IDs。上游只选读新增摘要涉及的边界，不重审原有全部源码、动态网站或兄弟篇的完整来源链。

本轮独立打开的上游证据如下，均未执行其中命令：

| 证据 | 核对范围与结果 |
|---|---|
| [Kubernetes v1.32 Pod Lifecycle](https://v1-32.docs.kubernetes.io/docs/concepts/workloads/pods/pod-lifecycle/#pod-termination) | `Termination of Pods`：本地关闭与端点状态更新并行；terminating 端点不接常规新流量，既有连接完成/排空另有责任。该机制不证明在途生成可迁移，支持 C01 的边界判断 |
| [PyTorch v2.6.0 固定 run.py](https://github.com/pytorch/pytorch/blob/1eba9b3aa3c43f86f4a2c807ac8e12c4a7767340/torch/distributed/run.py#L286-L374) | `Failure Modes`、`Membership Changes`、`Important Notices`：成员变化重建 WorkerGroup、rank 不稳定，应用自行保存/加载 checkpoint。生成站点 `elastic/run.html` 本轮读取失败，改读同一版本固定源码 docstring，未称站点已重新核实 |
| [vLLM 固定 ROCm 安装文档](https://github.com/vllm-project/vllm/blob/b17039bccc17b94a2ea107272ad7bc93508708df/docs/getting_started/installation/gpu.rocm.inc.md#L1-L26) | 核实 Docker 推荐与无预编译 ROCm wheel 两项，均限该固定版本；与交集档案及 registry `src.vllm.rocm-install-doc-v0-14` 一致，不外推后续版本 |
| [vLLM 固定 async_llm.py](https://github.com/vllm-project/vllm/blob/b17039bccc17b94a2ea107272ad7bc93508708df/vllm/v1/engine/async_llm.py#L433-L459) | 断连/生成器取消进入 abort；EngineDeadError 分支不逐请求 abort。该局部片段不证明完整 HTTP shutdown、资源即时归还或在途流自动排空 |
| [vLLM Ascend 固定 conf.py](https://github.com/vllm-project/vllm-ascend/blob/52d4acfa51fb868823d1070b81cbd2d97e9e4696/docs/source/conf.py#L62-L81) | `vllm_version/pip_vllm_version/ci_vllm_version` 为 0.14.1 线，Ascend 标注 0.14.0rc1，印证原文保留的独立快照边界，不能归并为上游 b17039bc |
| [MindIE 固定 release_notes.md](https://github.com/Ascend/MindIE-LLM/blob/69e5a5dd4b533eaffc7e198320435350825a36f7/docs/zh/release_notes.md#L1-L57) | 核实仓内文档自述 3.1.0 与其配套表；不据此建立开源源码、产品包及 latest 站点的全局同版映射 |

## 已核实的主链与边界

### 原口径与元数据

| 检查对象 | 核对结论 |
|---|---|
| 训练主链 | 训练文 L49–84、L110–145 对应原有六节文本逐节完全一致：导航图、阶段→知识表、四条线、step、checkpoint 可选分支及指标绑定均未改动。3 张原表和 1 个 Mermaid 块原样保留 |
| 推理主链 | 推理文 L44–76、L97–147 对应原有六节文本逐节完全一致：导航图、问题入口、请求阶段表、三类状态、客户端/服务端计时和引擎/后端边界均保留。2 张原表、导航图和计时序列图原样保留 |
| 分母与时钟 | 训练文 L119、L135–145 仍区分运行代次、micro/optimizer step、观察点和保存恢复阶段；推理文 L101–106、L135–141 仍区分 attempted/completed/failed/cancelled、客户端/服务端起止、wall-clock/monotonic、成功样本过滤及聚合分位数。未新增统一阈值或把不同观察点相减当网络时间 |
| 来源保留 | 两文各 5 个 `source_refs` 及各自 `verification.evidence_refs` 均与 HEAD 完全一致，所引 ID 均存在。训练文 8 处、推理文 13 处外链的 URL 序列与 HEAD 完全一致；本修订没有新增外链或把旧快照替换为新版本。保留引用不等于本轮重新核实全部历史来源 |
| Schema 与关系引用 | 两文 frontmatter（含日期格式）通过 schema；`updated_at: "2026-10-21"` 与修订记录一致。训练文 related IDs 15 项、推理文 12 项，各新增 6 项，均能解析到现存条目；26＋23 处本地相对链接目标均存在 |
| 验证与编辑状态 | 两文保持 `draft / source_checked`、`platforms: [generic]`；verification notes 明确终态核对仅补入口，保留未运行训练/推理/硬件实验说明。取证记录 L7、L18–26 对修改类别和 unknown 的描述总体相符，不能凭这些 notes 给技术或硬件验收升级 |
| 所有权与修订规模 | 仅新增导航摘要与入口，机制仍归 02/06/07 各正文。训练文末尾继续明确专家并行、精确 worker 游标和 mid-step 不由总览证明；推理文末尾保留未固定控制面实现及未实测条件 |

### 新增入口的正文承载核对

| 总览入口 | 实际承载位置与边界 | 本轮判断 |
|---|---|---|
| pretrain / SFT / LoRA（训练文 L90–93） | [预训练与微调](../../knowledge/06-training/pretraining-and-finetuning.md) L45–52 区分目标与参数适配两轴及选样；L95–126 有状态契约、adapter 身份、resume 与新阶段的继承/重置及合并边界；L137–164 有计损 token 口径和阶段验证 | 入口承载成立；“同上”可追到同表上一行，不要求复制其矩阵 |
| RL rollout（L94） | [RL 协同](../../knowledge/06-training/rl-rollout-consistency.md) L56、L62–90 区分 legacy V0 样板、离线 DPO 与在线 PPO/GRPO；权重发布回边明确。L179–204 有版本/吞吐/有效样本率与有限验证；L208–215 保持三平台版本线分立 | 不把离线 DPO 等同在线 rollout；不把 07 域 vLLM 0.14.0 与 verl 要求的版本拼成环境 |
| 状态责任与初始化（L96） | [并行状态](../../knowledge/06-training/parallelism-and-state.md) L172–191 有参数、梯度、optimizer、scheduler、scaler、RNG、数据进度及提交点矩阵；[框架执行](../../knowledge/06-training/framework-execution.md) L50–79、L114–127 有组件责任与初始化/首步/更新分界 | 承载成立；总览中的箭头按职责导航理解，不当作固定串行实现 |
| 恢复分层（L100） | [Checkpoint 一致性](../../knowledge/06-training/checkpoint-state-consistency.md) L47–56、L82–96、L150–171 区分截点、API 完成、身份/字段、同输入单步、持续窗口和终止回退；精确字段与浮点容差分开 | 承载成立；未承诺通用 mid-step 或 exactly-once 数据恢复 |
| 弹性与持续进展（L101–102） | [弹性训练](../../knowledge/06-training/elastic-training-and-membership.md) L35–69、L83–99 分开 PyTorch 应用 checkpoint 与 MindSpeed 副本机制；[性能分析](../../knowledge/06-training/performance-analysis.md) L50–63、L87–98、L146–161 固定有效产出/时钟，回溯最早阻塞边，保留停止与恢复 A 对照 | 承载成立；应用状态责任不能替代 MindSpeed 的副本、DP 粒度及外部组件条件 |
| 扩缩容与冷启动（推理文 L84） | [容量与扩缩容](../../knowledge/07-inference/capacity-and-autoscaling.md) L44–48、L63–71、L82–97 有负载/SLO 容量、cold start、ready gate、drain、PD 双池、有限预算和停止恢复 | 入口成立，但总览把新流量与在途流压为“请求被重路由”，见 C01 |
| 版本发布、副本/引擎故障（L85、L87、L90） | [发布与恢复](../../knowledge/07-inference/release-and-recovery.md) L42–62 三层健康及五步发布；L64–79 包含 worker/core、Pod、PD 单侧、重试风暴、残留状态；L81–92 给出逻辑请求×attempt 对账、稳定窗、质量、资源和停止闭环 | 承载成立；“恢复后核对延迟、失败/取消与质量”与原成功样本过滤口径相容，ready 不代替恢复 |
| 请求失败与重试（L86） | [路由与流控](../../knowledge/07-inference/routing-and-flow-control.md) L93–98 分开关联 ID、幂等证据、未送达/送达未见响应/已提交响应，以及取消与延迟资源回收；L100–116 有固定负载与版本边界 | 承载成立，未证明透明续传或 exactly-once；C01 的缩容摘要必须同样保留该边界 |
| NVIDIA/AMD 与 Ascend OOM（L88） | [GPU OOM](../../knowledge/07-inference/gpu-inference-oom-triage.md) L43–58、L71–81 覆盖启动预算、加载、profile、KV、图及运行期 prefill/decode/混批；[Ascend OOM](../../knowledge/07-inference/ascend-inference-oom-triage.md) L62–70、L93–108 保留 NPU 文案、账户和固定插件线 | 承载成立；NVIDIA/AMD 入口实际有 ROCm 身份与取证差异，未把 CUDA/NPU 分配器字段互换 |
| 三平台环境前置（训练文 L103；推理文 L90） | [安装/升级/回退方法](../../knowledge/02-software-stack/environment-installation-and-upgrade.md) L65–92、L157–210 有依赖门禁、分层验证、变化矩阵、B0/N/R 与恢复门槛；L215–221 指向平台与上层执行档案，并明确引擎安装另归上层正文 | 作为环境前置方法入口成立，不能据此称已有完整引擎安装处方或可执行组合；未重审 T02-12 的独立闭环 |
| 训练平台分支（L107–108） | NVIDIA/Ascend 专题确有主目录正文链接，并非空页；更直接的[框架执行](../../knowledge/06-training/framework-execution.md) L95–112 给出三组独立资料档案和 ROCm 差异。[AMD 档案](../../knowledge/02-software-stack/amd-rocm-documented-profile.md) L65–93、L110–123、L210–229 有真实平台内容与 documented/conflict/unknown × not_run；[混合精度](../../knowledge/06-training/mixed-precision-and-convergence.md) L53–63、L88–102 保留 ROCm 独立版本条件 | 平台链接成立；“无 AMD Megatron/MindSpeed 对应档案”限该三组执行档案，不解读成 AMD 不支持训练或不存在其他上游实现 |
| 推理平台交集与 MindIE（L94–95） | [引擎交集](../../knowledge/07-inference/engine-backend-boundaries.md) L24、L46、L72–118 分开 NVIDIA、AMD、Ascend 及源码/latest 声明；[MindIE 执行](../../knowledge/07-inference/mindie-execution-profile.md) L36–54、L124–144 有 3.1.0 文档线、同快照差异、PD 配置与 unknown | 有实质平台正文；未列组合仍 unknown，未写已实测。总览版本归属的限定需按 C02 修正 |

## 编号发现

### C01 · P2 · 缩容 drain 摘要未区分新请求改路由与在途流排空

- **位置**：推理文 L84；关联 L86、L90、L105。
- **问题**：“缩容 drain 期间请求被重路由”省略了请求所处状态，把入口侧新流量选路与已接纳流式请求的处理压成同一动作。读者可能由此认为 drain 会将正在生成的请求转移到其他副本并继续完成；这弱化了承载正文明确保留的排空、终态未知与重试限制，也影响 completed/failed/cancelled 的对账。
- **证据**：[容量篇](../../knowledge/07-inference/capacity-and-autoscaling.md) L67 写的是先摘除路由/端点、排空在途流再退出；[发布恢复篇](../../knowledge/07-inference/release-and-recovery.md) L57 要求停止新准入、观察实际路由收敛，单独核对已接纳流的完成/取消，超期终止者记录终态不确定，且完整自动排空行为仍 unknown；L76–77 不承诺已输出流透明续传或新副本自动继承本地 KV。[路由篇](../../knowledge/07-inference/routing-and-flow-control.md) L96–98 同样限制已送达与已提交响应的重试。[Kubernetes v1.32 终止语义](https://v1-32.docs.kubernetes.io/docs/concepts/workloads/pods/pod-lifecycle/#pod-termination)也只区分常规流量摘除与既有连接的完成/排空，不提供应用生成状态迁移保证。
- **建议修订**：只需在该表格单元区分“新请求经实际路由收敛转向其他可服务副本”和“在途流按 drain 契约完成/取消；超期或终态不明按重试边界处理”。沿用现有链接，无需新增迁移方案或改画原图。
- **关闭条件**：从该行能明确判断新请求与在途流的不同去向；不存在自动迁移/续传暗示，不以端点摘除当作实际排空完成；失败、取消与未知终态仍按目标正文对账。定向复核该行与 L86/L90 的一致性即可，不要求演练或硬件测试。

### C02 · P3 · 平台摘要的版本限定未准确对应承载档案的证据身份

- **位置**：推理文 L94，关联 L95、L147。
- **问题**：同一句并列上游、Ascend 与 MindIE 后，用“本文所有 vLLM 细节均限 b17039bc 固定快照”作总括，范围过宽；本篇 L147 实际另引 Ascend `52d4acf`，并保留其文档指向 vLLM 0.14.1 的差异。同时，“MindIE LLM 3.1.0”的组件/交集入口没有保留它只是仓内文档线自述的限定。承载交集篇采用开源仓 `master@69e5a5dd` 与另记的 latest 声明，未建立 3.1.0 产品包到全部源码/支持表的映射。本项是版本归属措辞与可追溯性问题，不据此判定 3.1.0 数字错误或平台不支持。
- **证据**：[交集篇](../../knowledge/07-inference/engine-backend-boundaries.md) L24、L46、L74 明确三线分立、开源/产品包区分以及 latest 支持表未核同版；[MindIE 执行篇](../../knowledge/07-inference/mindie-execution-profile.md) L38–41 仅采信 release notes 作为 3.1.0 文档线，源码/产品包映射仍 unknown。独立读取 [Ascend conf.py](https://github.com/vllm-project/vllm-ascend/blob/52d4acfa51fb868823d1070b81cbd2d97e9e4696/docs/source/conf.py#L62-L81)确认其 vLLM 配套标注为 0.14.1；[MindIE release notes](https://github.com/Ascend/MindIE-LLM/blob/69e5a5dd4b533eaffc7e198320435350825a36f7/docs/zh/release_notes.md#L1-L57)确有 3.1.0 自述，但不能单独消除上述身份缺口。
- **建议修订**：将 b17039bc 限定明确写成“本页上游 vLLM 执行/计时细节”；Ascend 继续按其固定快照另列。MindIE 入口保留 `69e5a5dd` 开源快照身份，若保留 3.1.0，注明是文档自述线并指向现有执行档案，不泛化到产品包或 latest 支持表。
- **关闭条件**：总览的每个版本标签均能对应其实际承载档案，b17039bc 不覆盖 Ascend 独立证据；3.1.0 不被读成已核同版的产品/源码/站点全集。不需改旧 source_refs、补建兼容档案或重审兄弟篇。

## 三条 acceptance 的逐条判断

| 条款 | 覆盖与边界 | 初审判断 |
|---|---|---|
| 1 · 训练准入、加载、初始化、step、保存、异常恢复、持续进展；pretrain/SFT/RL 及状态责任 | 原主链与阶段表保留；L86–108 补足工作流、状态责任、初始化分诊、成员变更、恢复分层和进展验证。模型/状态装载与续训由框架及 checkpoint 正文承接，未把加载返回当恢复通过 | **满足本轮有限导航验收**；不是训练或恢复实测通过 |
| 2 · 推理入口/路由/排队/加载/prefill/decode/流式输出/取消释放；副本变化、失败重试、恢复 | 原图、请求表、状态和计时保留；L78–95 五类变化均有实质正文入口，恢复验证包含延迟、失败/取消、质量；加载与 ready 由副本生命周期和新增承载正文展开 | **部分满足，C01 必修**；入口齐全，但 drain 摘要的请求状态边界需与承载正文一致 |
| 3 · 阶段、观察点、分母/时钟、停止判据、来源一致；三平台实质链接、unknown 和未实测边界 | 原表/图/来源完全保留；停止及恢复门槛由 checkpoint、性能、容量与发布正文承接，未提供虚构阈值。三平台均有实际正文，未入档案组合仍 unknown，draft/source_checked 未升级 | **部分满足**：C01 涉及完成/排空观察点；C02 需准确限定平台快照归属。维护核对不等于硬件验证这一边界满足 |

## 校验、写入与结论

仅执行只读 Git/文本比较、schema（含日期格式）、ID 与本地链接检查；这些检查不证明技术正确性、远程全部资料可达或环境兼容。未运行训练、推理、安装、升级、回退、压测、故障注入或任何 GPU/NPU 实验。未运行 `make check`、`make build`、`make test`；本轮仅新增非目录正文的审阅报告，按用户只写指定文件的范围不重建 `build/`。

审阅开始时两文及其他批次材料已有工作区变更，本会话不接管或修改这些变更。写入前记录的仓库源文件清单（Git tracked＋非忽略 untracked，排除本报告）为 687 个文件，按路径及文件 SHA-256 汇总的清单 SHA-256 为 `8f72a4496205b275d7149dc546cdd04f976f63a76fd6e1149c0ff5ad635a75c3`；交付时重新计算仍为同一数量与同一摘要，确认报告之外文件未变。两文仍为 151 / 153 行及上表 SHA-256；报告全部本地相对链接目标存在，无行尾空白。交付时再读最新 turn_context，仍为 L8 的同一模型、档位、cwd 与 collaboration_mode.settings。

**T00-04 第一轮初审暂不通过，需编写者按 C01–C02 作局部修订，再由同一审阅者定向复核。** 不要求扩写正文、复制领域机制或补做实测以关闭这两项；本报告不承担正文修订，也不宣告整批其他任务完成。模型身份核验、编辑验收、问题关闭与硬件验证分别记账，任何导航和维护记录均不构成 NVIDIA / Ascend / AMD 组合支持或恢复成功的证明。
