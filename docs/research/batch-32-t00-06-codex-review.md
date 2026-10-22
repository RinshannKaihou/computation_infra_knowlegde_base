# Batch 32 · T00-06 初审报告

## 会话元数据与结论

| 项目 | 记录 |
|---|---|
| 审阅角色 / 轮次 | 独立批次审阅者；第一轮初审；本会话不承担正文编写或问题修订 |
| 指定及实际模型 / 档位 | gpt-6.1-sol / xhigh；实际与指定一致，本轮有效 |
| 核验方法 | 定位本地当前会话 rollout JSONL，以本任务用户消息核对归属，再与环境 CODEX_SESSION_ID、CODEX_THREAD_ID 互核；读取最新 turn_context 的 model、effort、cwd，不采用配置默认值或正文自述 |
| rollout | /Users/ywang2397/.codex/sessions/2026/10/22/rollout-2026-10-22T09-09-25-01a16127-e0da-73e0-b65c-6179c6ce9cc4.jsonl |
| 会话归属证据 | L1 session_meta 的 id、session_id 均为 01a16127-e0da-73e0-b65c-6179c6ce9cc4，cwd 为本仓库；两个环境会话 ID 均为该值；L10 用户消息明确包含“独立批次审阅者”“Batch 32”“T00-06”、90c38f7 和本报告文件名 |
| 用户消息坐标 | L10，2026-10-22T01:09:42.482Z；该条用户消息文本 SHA-256：f9aa006ee5aa6ed047d606901362ef9e997b7c8ce8bd0ef9ece3a6349ca12b28 |
| 最新 turn_context | L8，2026-10-22T01:09:42.474Z；model=gpt-6.1-sol；effort=xhigh；cwd=/Users/ywang2397/work/AI_reliability_knowledge_base |
| collaboration_mode | mode=default；settings.model=gpt-6.1-sol；settings.reasoning_effort=xhigh；settings.developer_instructions=null |
| turn ID | 01a16127-e209-74b1-a808-bcfd273d72e8 |
| 写入前复核 | 再读当前 rollout，最新 turn_context 仍为上述 L8；未另启模型、子代理或委托审阅 |
| 执行方式 / 日期 | 当前本地 Codex CLI 会话直接审阅；2026-10-22 / Asia/Shanghai |
| 仓库基准 | HEAD=90c38f7592137eeb2b1862983822fe415cf471c5；审阅开始时 git status --short 为空 |
| 任务定义 | [执行清单](../../plans/full-coverage-backlog.yaml) T00-06 L7441–7488；objective/acceptance L7461–7465；主题 00.6 L291–340；文件 SHA-256：abffb0eaff9a825ac37ff1921acfa7a2d1fb73289d85f9d8d88a24febec71530 |
| 写入范围声明 | 仅新增 docs/research/batch-32-t00-06-codex-review.md；不修改三页、取证记录、registry、角色页、其他导航、计划、代码或 build/；所有发现保留 OPEN |

开始审阅正文前，已实际执行 wc -l 与 shasum -a 256，基准如下：

| 文件 | 行数 | SHA-256 |
|---|---:|---|
| [选型与容量路径](../../paths/tasks/selection-and-capacity.md) | 68 | ca3ce3e2726b7cab7f486b49a49f155a687cf5e4fd9d6611723c87e67df299e6 |
| [节点验收路径](../../paths/tasks/node-acceptance.md) | 78 | 6867b91907c436d07682d1fe39b804208010ab2a4bc75b15606b227b3693bf17 |
| [环境安装路径](../../paths/tasks/environment-installation.md) | 77 | 0eb2082de15e837c29c4d8488bd20fd53691dcd9afe2642ea7362bb37cdf0663 |
| [本批取证记录](batch-32-t00-06-sources.md) | 32 | 9c67a35c44da4b83e2d96acc0bd503959d7e69b79e7fea58c8f5987d2a1bfb1e |

| 结论项 | 初审判断 |
|---|---|
| 模型与档位 | 核验通过 |
| 三页五要素与正文归属 | 五要素均有明确位置，未复制领域机制；安装页门禁与分流条件存在语义差异 |
| 本地链接 / 元数据 | 42 处内链、36 个不同目标全部存在，内容 ID、类型、领域、编辑状态已逐个核对；三页 frontmatter 合规 |
| 外部入口 | 5/5 URL 与登记逐字一致；2/5 链接文本与登记 title 逐字一致，其余 3 项为省略限定信息的标题 |
| 入链 | 三页分别为 8、9、10 处，无零入链页；角色页到三条新任务路径的直接接入仍缺 |
| 结构校验 | PYTHONDONTWRITEBYTECODE=1 make check：退出码 0，135 content entries / 577 sources |
| 初审总评 | **需修订并定向复核，暂不通过：5 项发现，P1 0 项、P2 2 项、P3 3 项，全部 OPEN** |

优先级口径：P1＝足以严重误导处置的关键错误；P2＝影响任务交付、导航功能或验收证据的必修事项；P3＝局部入口、记录或可追溯性问题。以下 S、N、I 分别表示选型、节点验收、环境安装三页，坐标均使用上述指纹对应的源文件行号。

## 范围与方法

已先读 README.md、AGENTS.md、[写作指南](../authoring-guide.md)、[内容 schema](../../schemas/content.schema.json)和[内容总目录](../../content-outline.md)的总体原则及 00 域；完整读取三页与取证记录，核对 T00-06 objective、三条 acceptance、existing_source_ids、source_discovery，及主题 00.6 的闭合条件。主题 01.6、02.7 的 delivery_scope 分别保留真实验收档案独立验证、三平台文档样板与实跑结果分离的边界。报告格式参照 [T00-05 初审](batch-31-t00-05-codex-review.md)。

检查分为结构与语义两部分：解析三页全部内联本地链接并逐个读取目标元数据；抽查各步用途、指定节名、判定口径与目标正文承载关系；对安装骨架的门禁、七层梯子、结果契约、三平台样板和回退边界作重点对照。文件存在或 make check PASS 均不代替描述匹配。

写入报告前，扫描根目录以及 knowledge/、paths/、docs/、sources/、plans/、templates/、config/ 下全部 **678 份正式源 Markdown**：根目录 5、knowledge 123、paths 12、docs 532、sources 1、templates 5，plans/config 无 Markdown。解析内联相对链接，剔除围栏代码和行内代码，按来源文件实际目录解析目标；报告自身不计入该快照。原始字符串路径、related_ids、规划 YAML 中的 targets 不计作可点击入链。

另以只读网页工具打开五个精确外部 URL：NVIDIA 两项、MindX 与 ROCm 返回页面文本；CANN instg_0098 返回“该工具不可访问”。这不等于该 URL 为 404 或来源不存在；本轮没有补写 HTTP 状态、也没有重审五份厂商文档的全部章节、安装命令或许可。外部入口与登记的一致性以本地逐字比较为证据，链接见下表。没有额外采集大批材料。

## 已核实的主链与边界

### 五要素及导航用途

| 路径 | 前置材料 | 阅读顺序 | 目标产出 | 下一步判断 | 完成 / 停止条件 | 判断 |
|---|---|---|---|---|---|---|
| S 选型与容量 | L32–37：负载画像、五类目标、硬约束、候选资料 | L39–47，七步 | L49–53：候选对照、容量预算、待验证清单 | L55–59：到货验收、安装准备、缺证登记 | L61–64：完成条件及缺规格/供电散热/成本时登记 blocked 并交决策者 | 五要素齐全；只提供比较与阅读方法，无采购或容量结论 |
| N 节点验收 | L34–40：订单/台账、平台、权限工具、被动证据、三种结论 | L42–50，四层证据骨架加七步阅读 | L52–56：逐层记录、无法判断项、档案 | L58–62：通过后接安装；失败/缺证分流；证据冲突降级 | L64–67：记录完成与工具前提/规格/明确故障停止分支 | 五要素齐全；“记录完成”允许失败/unknown，不等于通过或回服，N60 另设全部通过条件 |
| I 环境安装 | L32–38：身份、回退、结果判据 | L40–48，七步 | L50–54：逐层判定、结果契约、环境档案 | L56–60：运行、故障分层、迁移与缺证登记 | L62–65：完成与停止条件 | 五要素在形式上齐全；门禁摘要、继续/停止条件须修订，见 C01–C02 |

三页均为 type=path、domain=overview、status=draft、platforms=[generic]，各自 id 唯一，title 与本页 H1 一致，updated_at 为带引号的日期字符串 2026-10-22。source_refs 数量分别为 0、2、3；related_ids 分别为 13、13、10，共 36 次引用，全部存在。领域正文 ID 前缀与目标 domain 对应；path.* 是路径稳定 ID，目标 type=path、domain=overview，不误判为领域前缀错误。schema 不要求 path 具备 procedure 的 applicability/verification 字段。

### 描述与目标正文的语义抽查

| 导航表述 / 入口 | 实际承载位置 | 核对结果 |
|---|---|---|
| S41 五类目标、有效产出、能耗边界、三窗口表 | [设计目标正文](../../knowledge/00-overview/design-targets-and-tradeoffs.md) L45–80、L133–143 | 五类目标、训练净进展/推理 goodput、四层能耗边界和正常/故障/恢复窗口均真实存在；并无现场成本或能耗结论 |
| S42 两个超节点样板及集群约束比较 | [参考架构](../../knowledge/00-overview/reference-architectures.md) L103–128 | GB200 NVL72、Atlas 900 A3 SuperPoD 与集群样板分列；比较仍需实际证据，不提供胜负结论 |
| S43“选型四步法” | [节点生命周期](../../knowledge/01-hardware/node-selection-and-lifecycle.md) L64–89 | 实际有“第一步：需求转译”“第二步：有效能力测量”“第三步：成本侧预算（供电/散热锚点）”“第四步：有效成本与部署核对”；导航是简写，四步结构真实，未虚构同名独立章节 |
| S44–45 资源记录、互联样板、文档带宽与作业带宽 | [资源拓扑](../../knowledge/01-hardware/resource-topology.md) L48–52、L93 起字段表；[互联路径](../../knowledge/03-communication/interconnect-paths.md) L54、L75–118、L131 起 | 资源/端口/设备/交换结构及共享故障域有承载；两个互联样板独立，文档标称值不当作作业可用值 |
| S46 存储接口、一致性、选型双样板 | [本地/共享存储](../../knowledge/04-data-storage/local-and-shared-storage.md) §1–4；[对象/并行存储](../../knowledge/04-data-storage/object-and-parallel-storage.md) §1–4 | 前者为本地文件系统/NFS，后者为 Ceph RGW S3/Lustre；接口和选型条件按实现分列，不是四种通用部署承诺 |
| N44、N49 四层证据与测试工具前提表 | [节点验收正文](../../knowledge/01-hardware/node-acceptance-triage.md) L73–107、L118–139 | 规格→被动→主动→基准结构真实；DCGM、ascend-dmi 与 NVSM 的权限/机型/跳过条件分列，不承诺工具等价 |
| N45–48 身份、健康、资源及供电散热 | BMC 正文“固件身份清单与更新边界”“事件记录方法”；健康正文“五类证据”“五种含义的区分：跨平台对照”；资源字段及供电散热正文 | 所链正文承载相应用途；健康摘要、事件、累计计数、采集失败与未覆盖可区分，NPU 观测缺口没有被补成已有能力 |
| N49 AMD 通信验证样板 | [RCCL 档案](../../knowledge/03-communication/rccl-runtime-and-verification.md) L91–105 | 两节点验证明确为待执行设计；性能无同配置基线时保持未判定，不由校验通过代证 |
| N50“验收与投产前证据锚点”“隔离与返修证据锚点” | [节点生命周期](../../knowledge/01-hardware/node-selection-and-lifecycle.md) L107、L113 两个三级标题 | 两个节名逐字存在；动作锚点仍受 NVIDIA/Ascend/OEM 各自来源限制 |
| I34“变更前准入门禁”、I42“七层安装验证梯子” | [T02-12 正文](../../knowledge/02-software-stack/environment-installation-and-upgrade.md) L65–89 | 门禁与 L1–L7 真实存在，实际标题为“安装验证梯子（七层，逐层判定）”；问题是摘要改变门禁内容，不是节名虚构，见 C01–C02 |
| I44–45 最小验证方法与框架内置/扩展路径 | [运行时正文](../../knowledge/02-software-stack/runtime-execution-and-library-loading.md) L310–334；[后端适配](../../knowledge/02-software-stack/framework-backend-adaptation.md) L53–82 | 初始化→运算→同步→结果检查方法真实；CUDA/ROCm 内置与 TorchNPU 扩展的分支真实。运行时篇的 CANN/HIP 文档线较旧，T02-12 L111 已明确禁止直接拼成目标版本组合 |
| I46–48 容器、设备状态链及首个故障分层 | 容器基线 §1、§4；设备资源状态链各层职责；主机资源/设备访问诊断的取证表和步骤分支 | 所述用途有承载；设备可见、可分配、可访问与后端可用没有被等同 |

安装路径连接三平台档案采用两跳：I42 → T02-12 正文 → 该文 L215 的 NVIDIA、Ascend、AMD ROCm 三个实际链接；N50 则直接链接三份档案。不能仅因 I 页没有直接列三个档案链接就判其不可达。最小运行基线由 I42 到 T02-12 L93–111 的结果契约与方法入口承载；此处的契约尚待针对实例冻结，样例通过不等于整项验收通过。

### 全部本地链接的逐个元数据核对

下表覆盖三页 **42 处链接、36 个不同目标**；“位置”列保留重复链接。S 为 13 处/13 目标，N 为 15 处/14 目标，I 为 14 处/12 目标。N61 的生命周期重复、I34/I42 与 I54/I59 的重复均已计入。

| 位置 | 目标文件 | 内容 ID | 类型 / 主领域 / 编辑状态 |
|---|---|---|---|
| S41 | [design-targets-and-tradeoffs.md](../../knowledge/00-overview/design-targets-and-tradeoffs.md) | `overview.design-targets-and-tradeoffs` | `reference` / `overview` / `draft` |
| S42 | [reference-architectures.md](../../knowledge/00-overview/reference-architectures.md) | `overview.reference-architectures` | `concept` / `overview` / `draft` |
| N45 | [bmc-firmware-and-events.md](../../knowledge/01-hardware/bmc-firmware-and-events.md) | `hardware.bmc-firmware-and-events` | `reference` / `hardware` / `draft` |
| N46 | [health-evidence.md](../../knowledge/01-hardware/health-evidence.md) | `hardware.health-evidence` | `reference` / `hardware` / `draft` |
| N44 | [node-acceptance-triage.md](../../knowledge/01-hardware/node-acceptance-triage.md) | `hardware.node-acceptance-triage` | `procedure` / `hardware` / `draft` |
| S43, N50, N61 | [node-selection-and-lifecycle.md](../../knowledge/01-hardware/node-selection-and-lifecycle.md) | `hardware.node-selection-and-lifecycle` | `procedure` / `hardware` / `draft` |
| N48 | [power-thermal-evidence.md](../../knowledge/01-hardware/power-thermal-evidence.md) | `hardware.power-thermal-evidence` | `reference` / `hardware` / `draft` |
| S44 | [rack-power-cooling-and-failure-domains.md](../../knowledge/01-hardware/rack-power-cooling-and-failure-domains.md) | `hardware.rack-power-cooling-and-failure-domains` | `concept` / `hardware` / `draft` |
| S44, N47 | [resource-topology.md](../../knowledge/01-hardware/resource-topology.md) | `hardware.resource-topology` | `reference` / `hardware` / `draft` |
| N50 | [amd-rocm-documented-profile.md](../../knowledge/02-software-stack/amd-rocm-documented-profile.md) | `software-stack.amd-rocm-documented-profile` | `reference` / `software-stack` / `draft` |
| N50 | [ascend-documented-profile.md](../../knowledge/02-software-stack/ascend-documented-profile.md) | `software-stack.ascend-documented-profile` | `reference` / `software-stack` / `draft` |
| I36 | [compatibility-evidence.md](../../knowledge/02-software-stack/compatibility-evidence.md) | `software-stack.compatibility-evidence` | `reference` / `software-stack` / `draft` |
| I34, I42 | [environment-installation-and-upgrade.md](../../knowledge/02-software-stack/environment-installation-and-upgrade.md) | `software-stack.environment-installation-and-upgrade` | `procedure` / `software-stack` / `draft` |
| I45 | [framework-backend-adaptation.md](../../knowledge/02-software-stack/framework-backend-adaptation.md) | `software-stack.framework-backend-adaptation` | `reference` / `software-stack` / `draft` |
| I48 | [host-resource-pressure-and-device-access.md](../../knowledge/02-software-stack/host-resource-pressure-and-device-access.md) | `software-stack.host-resource-pressure-and-device-access` | `procedure` / `software-stack` / `draft` |
| I43 | [layers-and-boundaries.md](../../knowledge/02-software-stack/layers-and-boundaries.md) | `software-stack.layers-and-boundaries` | `concept` / `software-stack` / `draft` |
| N50 | [nvidia-documented-profile.md](../../knowledge/02-software-stack/nvidia-documented-profile.md) | `software-stack.nvidia-documented-profile` | `reference` / `software-stack` / `draft` |
| I44 | [runtime-execution-and-library-loading.md](../../knowledge/02-software-stack/runtime-execution-and-library-loading.md) | `software-stack.runtime-execution-and-library-loading` | `reference` / `software-stack` / `draft` |
| N49 | [bandwidth-baselines.md](../../knowledge/03-communication/bandwidth-baselines.md) | `communication.bandwidth-baselines` | `reference` / `communication` / `draft` |
| S45 | [interconnect-paths.md](../../knowledge/03-communication/interconnect-paths.md) | `communication.interconnect-paths` | `reference` / `communication` / `draft` |
| N49 | [rccl-runtime-and-verification.md](../../knowledge/03-communication/rccl-runtime-and-verification.md) | `communication.rccl-runtime-and-verification` | `reference` / `communication` / `draft` |
| S46 | [local-and-shared-storage.md](../../knowledge/04-data-storage/local-and-shared-storage.md) | `data-storage.local-and-shared-storage` | `reference` / `data-storage` / `draft` |
| S46 | [object-and-parallel-storage.md](../../knowledge/04-data-storage/object-and-parallel-storage.md) | `data-storage.object-and-parallel-storage` | `reference` / `data-storage` / `draft` |
| I46 | [container-image-runtime-baseline.md](../../knowledge/05-cluster-platform/container-image-runtime-baseline.md) | `cluster-platform.container-image-runtime-baseline` | `reference` / `cluster-platform` / `draft` |
| I47 | [device-resource-chain.md](../../knowledge/05-cluster-platform/device-resource-chain.md) | `cluster-platform.device-resource-chain` | `concept` / `cluster-platform` / `draft` |
| S47 | [parallelism-and-state.md](../../knowledge/06-training/parallelism-and-state.md) | `training.parallelism-and-state` | `concept` / `training` / `draft` |
| S47 | [capacity-and-autoscaling.md](../../knowledge/07-inference/capacity-and-autoscaling.md) | `inference.capacity-and-autoscaling` | `procedure` / `inference` / `draft` |
| S47 | [distributed-inference-layouts.md](../../knowledge/07-inference/distributed-inference-layouts.md) | `inference.distributed-inference-layouts` | `concept` / `inference` / `draft` |
| N74 | [amd.md](../../paths/platforms/amd.md) | `path.platform.amd` | `path` / `overview` / `draft` |
| S58, N60 | [environment-installation.md](../../paths/tasks/environment-installation.md) | `path.task.environment-installation` | `path` / `overview` / `draft` |
| N61 | [fault-recovery.md](../../paths/tasks/fault-recovery.md) | `path.task.fault-recovery` | `path` / `overview` / `draft` |
| I58 | [inference-triage.md](../../paths/tasks/inference-triage.md) | `path.task.inference-triage` | `path` / `overview` / `draft` |
| I54, I59 | [migration-and-upgrade.md](../../paths/tasks/migration-and-upgrade.md) | `path.task.migration-and-upgrade` | `path` / `overview` / `draft` |
| S57 | [node-acceptance.md](../../paths/tasks/node-acceptance.md) | `path.task.node-acceptance` | `path` / `overview` / `draft` |
| I58 | [performance-optimization.md](../../paths/tasks/performance-optimization.md) | `path.task.performance-optimization` | `path` / `overview` / `draft` |
| I58 | [training-triage.md](../../paths/tasks/training-triage.md) | `path.task.training-triage` | `path` / `overview` / `draft` |

36 个目标按类型为 reference 17、concept 6、procedure 5、path 8；按主领域为 overview 10、hardware 7、software-stack 9、communication 3、data-storage 2、cluster-platform 2、training 1、inference 2。目标均为 draft，无未来文件假链接。验证字段为 source_checked 25、not_verified 3、未设置 8（均为路径条目）；没有 reproduced 目标。编辑状态与验证状态分别统计，没有把 draft 或 source_checked 当作现场验证。

### 平台、验证与操作边界

S30 明确样板、规格与成本示例未实测，不构成部署环境；N32 明确工具前提、版本与机型限制及不授予操作权限；I30 明确未执行安装、实际执行依据既有授权与现场条件。三页 generic 均用于导航意图，未发现将某条厂商命令无条件推广到三平台的断言。

[节点验收正文](../../knowledge/01-hardware/node-acceptance-triage.md) 的 verification.status=not_verified、environment_refs=[]，L154 明示真实验收档案缺口留给 V08；[节点生命周期](../../knowledge/01-hardware/node-selection-and-lifecycle.md) 同为 not_verified。T02-12 为 draft/source_checked、environment_refs=[]，L219–221 明示未执行安装、升级或卸载；不能把该文来源核对读成安装成功。[验证账本](../../plans/validation-backlog.yaml) V00 L14–38、V08 L278–310 均为 planned、executed_at=null、evidence_refs=[]，与这些限制一致。

三份平台档案分别保留 NVIDIA 宿主/容器配套冲突、Ascend 精确驱动/固件交集缺证与 AMD 版本/矩阵条件，不是可部署整栈清单。安装路径所用运行时篇的 CANN 8.2.RC1.alpha001、HIP 6.3.42134 方法样板与安装骨架的 CANN 8.3.RCX、ROCm 10.1.0 文档线不同，T02-12 L111 已明确另核目标线接口、样例与适用条件，未核保持未完成；本轮没有据交叉链接推定版本兼容。

节点验收 N66 的“完成”是本轮记录结束，不能替代 N60 的全部通过或验收正文 L135–139 的回服门槛。验收后若安装或变更驱动/固件/拓扑，原证据仍受验收正文 L131 的版本面与复验要求约束；本轮没有把三页排列解释为未经条件核对即可顺序执行的命令流程。

### 页尾外部入口与登记的逐字比对

| 位置 / 来源 ID | URL 比对 | 链接文本与登记 title |
|---|---|---|
| N71；src.nvidia.gpu-node-triage-2026-10-08 | [本页及登记入口](https://docs.nvidia.com/deploy/gpu-debug-guidelines/gpu-node-triage.html)逐字一致；registry L1046–1048 | 本页“NVIDIA GPU Node Triage and Systematic Debug Guidelines”；登记“NVIDIA GPU Node Triage and Systematic Debug Guidelines（latest，2026-10-08 观察）”；不逐字一致 |
| N72；src.huawei.mindx-dl-60rc2-ascend-dmi-2026-09-29 | [本页及登记入口](https://www.hiascend.com/doc_center/source/zh/mindx-dl/60rc2/toolbox/ascenddmi/toolboxug_0020.html)逐字一致；registry L644–646 | 均为“MindX DL 6.0.RC2 ascend-dmi 故障诊断”；逐字一致 |
| I69；src.nvidia.driver-installation-guide-latest-2026-10-21 | [本页及登记入口](https://docs.nvidia.com/datacenter/tesla/driver-installation-guide/latest/index.html)逐字一致；registry L7239–7241 | 本页“NVIDIA Driver Installation Guide（latest）”；登记“NVIDIA Driver Installation Guide（latest 可变页，2026-10-21 观察）”；不逐字一致 |
| I70；src.huawei.cann-83rcx-upgrade-uninstall-2026-10-21 | [本页及登记入口](https://www.hiascend.com/doc_center/source/zh/CANNCommunityEdition/83RC1/softwareinst/instg/instg_0098.html)逐字一致；registry L7228–7230 | 本页“CANN community 8.3.RCX 安装指南升级与卸载”；登记“CANN community 8.3.RCX 安装指南升级与卸载（instg_0027–0033，doc_center/source 静态镜像核读）”；不逐字一致 |
| I71；src.amd.rocm-install-docs-10.1.0 | [本页及登记入口](https://rocm.docs.amd.com/en/docs-10.1.0/install/rocm.html)逐字一致；registry L2660–2662 | 均为“Install AMD ROCm 10.1.0”；逐字一致 |

五项 source_refs 与所列 URL 一一对应，没有借用另一个来源 ID。I69/I70 的相邻说明保留了部分被标题省略的观察口径/核读范围，因此 C04 限定为标题与登记可追溯性问题，不记作 URL 错误或来源失效。S 无外部入口、source_refs=[]，符合指南。

### 入链快照

| 来源文件 | 到 S 的行号 | 到 N 的行号 | 到 I 的行号 |
|---|---:|---:|---:|
| [README](../../README.md) | 33 | 33 | 33 |
| [00 首页](../../knowledge/00-overview/index.md) | 26 | 26 | 26 |
| [AMD 平台页](../../paths/platforms/amd.md) | 112 | 112 | 112 |
| [昇腾平台页](../../paths/platforms/ascend.md) | 185 | 185 | 185 |
| [NVIDIA 平台页](../../paths/platforms/nvidia.md) | 198 | 198 | 198 |
| [训练排障页](../../paths/tasks/training-triage.md) | 130 | 130 | 130 |
| [推理排障页](../../paths/tasks/inference-triage.md) | 108 | 108 | 108 |
| [故障恢复页](../../paths/tasks/fault-recovery.md) | 61 | — | — |
| [迁移升级页](../../paths/tasks/migration-and-upgrade.md) | — | 57 | 39 |
| [选型页](../../paths/tasks/selection-and-capacity.md) | — | 57 | 58 |
| [验收页](../../paths/tasks/node-acceptance.md) | — | — | 60 |
| 合计：链接次数 / 不同来源文件 | 8 / 8 | 9 / 9 | 10 / 10 |

合计 27 处入链、11 个不同来源文件，无零入链页。角色页直接到三页均为 0，见 C05；不据此宣称三页整体不可发现。README → 00 首页 → 三页可直接到达，00 首页 L39 也已更新 00.6 的交付范围，没有沿用“全部待建设”的旧口径。

### 取证记录的一致性

取证记录 L3 的三份交付物与实际文件、type=path 和主题 00.6 一致；L7/L13–18 的复用正文与五项既有来源对得上，S 无外部来源段。L14 所述 T02-12 已有独立审阅闭环，可对应[第五轮复核](batch-31-t02-12-codex-recheck-5.md) L19 的原审阅范围通过结论；该结论仍不等于真实安装成功。

L20–22 的原创范围确为导航结构、停止条件归纳与检查记录，没有搬入新命令或运行数据；但其中“准入门禁三类缺一即停”沿用了不准确的门禁概括，须随 C01 修订。L26 的未执行、L27 的样板外缺证处理、L28 的 latest 漂移提示在三页有对应限制；这些 unknown 不能代替对门禁本身的精确复述。

L30–32“复核轮修订记录（初审后）/（待审阅后追记）”如实处于未追记状态。本轮没有作者修订或定向复核，保留该占位合理，不作为发现，也不代作者补写关闭记录。

## 逐项发现

### C01 · P2 · 安装路径的“三类准入材料”替换了骨架正文的有效基线门禁

- **状态**：OPEN。
- **位置**：I34–38、I65；取证记录 L22。
- **问题**：路径宣称“按”骨架的变更前准入门禁、三类缺一即停，却将三类概括为环境身份、回退准备、结果判据。骨架实际是完整依赖交集、有效 baseline、恢复路径；“将来用什么判定结果”不能代替“变更前已有何种状态/基线证据”。首次安装也有明确例外要求，不能直接省略这一门禁。
- **证据**：[T02-12 正文](../../knowledge/02-software-stack/environment-installation-and-upgrade.md) L65–75，尤其 L72：首次安装须记录安装前状态与清理目标，已有环境升级没有 baseline 即停止；L186 再说明首次安装以安装前状态记录与安装目标清单替代 B0。I34–38 未保留任一安排，I65 又以该三类作为停止条件。I36 的身份摘要也没有完整保留骨架 L71“硬件×OS×驱动×运行时×框架/引擎”依赖交集的范围。
- **建议修订**：按原文保留依赖交集、基线/首次安装例外、恢复路径三个门禁入口；结果契约继续作为安装判定要求，不替换基线。导航只需概括并准确链接原节，不复制安装手册；取证记录的归纳同步校正。
- **关闭条件**：能从路径明确判断“已有环境无可复跑基线不得变更”“首次安装须记录安装前状态及清理/恢复目标”，并按目标场景核对完整依赖链；三类摘要和取证记录与骨架逐项对应。不得补造任何 B0 结果。

### C02 · P2 · 安装页的运行分流与停止规则没有沿用同一套验收门槛

- **状态**：OPEN。
- **位置**：I58–65，重点 I58、I65；对照 I53、I64。
- **问题**：I58 仅以“梯子全部通过”分流到运行阶段，未带入 I64 已要求的最小运行基线结果契约和档案登记；骨架允许记录“样例自带校验通过”，同时明确该状态仍不足以作最终验收。停止条件又把“某层失败”的硬停止缩窄成“某层失败且触发不可逆/高危边界”。I59 有先定位责任层的正确方向，但没有完整保留任一层失败即不得继续向上安装的规则。这使“下一步”“完成”“停止”三处条件不一致。
- **证据**：[骨架](../../knowledge/02-software-stack/environment-installation-and-upgrade.md) L79 要求任一层失败先在该层定位、不要继续向上安装；L109 明确契约字段未冻结时最终安装/升级验收不能记通过。I53/I64 已提结果契约，故问题是分流漏条件及失败停止被收窄，并非整页完全遗漏正确性边界。
- **建议修订**：运行分流显式以本页完成条件成立为前提；一般层失败先停止向上安装并定位，高危/不可逆边界另外要求停核恢复路径。无法判断项继续保留未完成，不因样例通过或局部层通过提前放行。
- **关闭条件**：纸面对照两例均不产生提前继续：① L3 安装失败但尚未涉及高危动作，仍不得进入更高层安装；② 官方样例均按自带规则通过、结果契约未冻结，仍不得转为运行就绪/验收通过。修订后的分流、完成与停止条件互相一致且与骨架相符，无需实际执行安装。

### C03 · P3 · 兼容性方法被简写成“分级”，四类依据也与目标正文不一致

- **状态**：OPEN。
- **位置**：I36。
- **问题**：该行将“发行包声明 / 源码分支 / 官方声明 / 本地验证”归为目标正文的方法“分级”；目标并非这个四类列表，第三类实际为单个项目的测试声明或 CI 结果。“官方声明”与第一类重叠，遗漏测试覆盖这一不同证据对象；“分级”也未保留原文要求的声明轴和本地验证轴。
- **证据**：[兼容性证据正文](../../knowledge/02-software-stack/compatibility-evidence.md) L34–41 明确不能压缩为从弱到强的证据等级，须分别记录官方声明与本地验证；L43–50 的四类为发行包官方兼容矩阵/发行说明、源码分支/构建配置、项目测试声明/CI、本地运行验证。本轮未发现 I 页已据此给出某个错误兼容结论，因此按局部方法描述问题记 P3。
- **建议修订**：用“区分依据类型并分别记录声明/验证状态”等准确表述；如保留四项枚举，应包含测试/CI，而不将笼统“官方声明”替换该项。
- **关闭条件**：从 I36 到目标正文，读者能一一对应所列依据，并知道本地 passed 不自动等于官方 supported；无需新增兼容矩阵或实验结果。

### C04 · P3 · 三个外部入口的链接文本没有完整沿用登记标题

- **状态**：OPEN。
- **位置**：N71、I69、I70；对应 registry L1047、L7240、L7229。
- **问题**：五个 URL 全部一致，但这三项链接文本分别省略了 latest/观察日期、可变页观察范围、静态镜像及核读节范围，未满足本轮要求核对的 title 一致口径。I69/I70 的后续说明保留了相关信息，故不判为错源或错误 URL；N71 本身也未展示登记中的观察口径。
- **证据**：前述逐字比对表列出了本页文本和登记 title 全文；只有 MindX、ROCm 两项逐字一致。N78/I77 的来源复用、URL 一致声明可成立，不能扩展成“所有链接文本也与登记逐字一致”。
- **建议修订**：沿用登记完整标题；若作者确需短标题，应保留清晰的登记 ID/完整标题对应及观察/核读范围，明确它是简称。不要为标题修订改换已对齐的 URL 或伪造新版核读记录。
- **关闭条件**：三项入口的标题/简称与登记关系可直接核对，latest 日期和静态镜像范围不丢失；五项 URL 仍保持准确。取证记录继续仅声明实际完成的比对范围。

### C05 · P3 · 新任务路径已接入主导航，角色页仍未接入准备阶段任务入口

- **状态**：OPEN。
- **位置**：[角色页](../../paths/roles/reading-by-role.md) L63–71、L84–91；本批三页的入链接入。
- **问题**：README、00 首页、三平台页和两条排障页都已接入，但角色阅读路径仍仅直达原有领域正文或既有排障路径，没有到选型、节点验收、环境安装三页的直接任务入口。从角色出发开展准备阶段任务时，无法在该页直接选取本批新组织的顺序与完成/停止检查。
- **证据**：对上述 678 份 Markdown 的入链扫描中，角色页到 S/N/I 均为 0；S/N/I 总入链分别为 8/9/10，故这不是三页孤立或全库不可发现。架构角色 L65–71 直接列架构、目标、硬件与安装正文，未链接本批任务页；本轮用户指定入链检查明确包含角色页接入。
- **建议修订**：在合适角色段落补充准备阶段任务入口，复用三页的顺序与检查，不复制技术正文；无需让每个角色无差别重复所有入口。
- **关闭条件**：从角色页按适用角色可直接找到并打开本批三类任务路径；README、00 首页及现有入链继续有效。无需重复增加无用途链接，也不据入口补齐宣告整个主题 00.6 或 Batch 32 已验收完成。

## 三条 acceptance 的逐条判断

| T00-06 acceptance | 已核实覆盖 | 初审判断 |
|---|---|---|
| 1. 每条路径含前置材料、顺序、目标产出、下一步判断及完成/停止条件；主目录只存一份技术正文 | 三页五要素均有位置，三页只给用途、产出与分流，没有另写安装/诊断机制或命令流程 | **部分满足，须修订**：C01–C02 使安装页条件与所链骨架不一致；五要素存在不等于其语义已验收 |
| 2. 选型连接容量/成本与硬件组成；验收连接被动证据/主动诊断/样板验证；安装连接三平台档案与最小运行基线 | S41–47、N44–50 主链匹配；安装经 I42 → 骨架 L215 到三平台档案，经 L93–111 到最小运行契约；36 个目标全部已存在 | **主链覆盖满足，交付仍需修订**：C03 的方法描述、C04 的入口可追溯性、C05 的角色接入；安装放行条件另见 C01–C02 |
| 3. 链接实际环境验证状态，不把示例机型/来源核对写成可直接部署的环境 | 三页全局边界、目标元数据、平台档案和 V00/V08 账本一致，未发现伪造运行数据；not_verified 与 source_checked 均未提升为 reproduced | **满足该条状态表达要求**；不因此豁免 C01–C02 的导航条件修订，也不宣告任何真实验收或安装成功 |

## 校验与结论

实际运行 **PYTHONDONTWRITEBYTECODE=1 make check**，退出码 **0**，输出 **PASS: 135 content entries; 577 sources.** 检查范围是结构、引用 ID 与本地文件链接，不验证技术正确性、页内锚点、远程可达性、描述承载关系、门禁充分性或真实环境兼容性。[校验器](../../src/kb/cli.py) L204–222 仅在 build 子命令下写构建产物。

遵照本轮“只新增报告、不要运行 make build”的明确限制，未执行 make build，未写 build/；未改 src/kb/，未运行 make test；未执行正文中的安装、诊断、压测、基准、重启或集群操作。审阅期间先记录了 707 个 Git 已登记及未忽略现存文件的 SHA-256，交付复查用于核实既存文件未变、唯一新增为本报告；四份输入的行数和指纹维持头表。

**T00-06 本轮初审暂不通过。C01–C05 全部 OPEN，须由编写者修订后进行定向复核；本会话仅交付发现。** 通过范围将限于三条导航路径的链接、描述、条件、来源登记与验证边界，不等于 GPU/NPU 实测、采购结论、可部署组合或安装/回退验收。取证记录的待追记占位保持原状，本报告不代写问题关闭或主题闭合记录。

