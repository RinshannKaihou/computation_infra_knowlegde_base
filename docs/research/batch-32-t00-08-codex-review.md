# Batch 32 · T00-08 独立初审报告

## 会话元数据与结论

| 项目 | 记录 |
|---|---|
| 审阅角色 / 轮次 | 独立批次审阅者；第一轮初审；本会话不承担正文编写或问题修订 |
| 指定及实际模型 / 档位 | `gpt-6.1-sol / xhigh`；实际与指定一致 |
| 会话归属核验 | 当前 rollout 的 L10 为本任务用户消息，包含“审阅对象：Batch 32 任务 T00-08”、commit `90c38f7` 和指定报告路径；L1 的 `session_meta.id` 与环境 `CODEX_SESSION_ID`、`CODEX_THREAD_ID` 三者均为 `01a16146-4c66-7691-95cd-0191f407121a` |
| rollout 坐标 | `/Users/ywang2397/.codex/sessions/2026/10/22/rollout-2026-10-22T09-42-39-01a16146-4c66-7691-95cd-0191f407121a.jsonl` |
| 最新 turn_context | 同文件 **L8**，时间戳 `2026-10-22T01:42:49.857Z`；`model=gpt-6.1-sol`、`effort=xhigh`、`cwd=/Users/ywang2397/work/AI_reliability_knowledge_base` |
| collaboration_mode 互核 | `mode=default`；`settings.model=gpt-6.1-sol`、`reasoning_effort=xhigh`、`developer_instructions=null`；与 `turn_context.model/effort` 一致 |
| turn ID | `01a16146-4d01-7993-8896-6b9bd55b0f4b`，用户消息所带 turn ID 与上下文一致 |
| 执行方式 / 日期 | 当前本地 Codex CLI 直接审阅；`originator=codex_exec`、CLI `0.163.0`；2026-10-22 / Asia/Shanghai；未另启模型或子代理 |
| 身份结论 | 写入前重新读取，最新且唯一的 `turn_context` 仍为上述记录；符合指定模型和档位。工具输出引用历史文档中的回退标记，不是本轮模型回退事件；不以配置默认值或正文自述代替核验 |
| Git 基准 | HEAD 为 `90c38f7592137eeb2b1862983822fe415cf471c5`；六份主审输入的当前字节均与该 commit 一致。四页修订另与 `90c38f7^` 对照 |
| 写入范围 | **仅新增本报告** `docs/research/batch-32-t00-08-codex-review.md`；不修改五个导航页、作者取证、registry、计划、其他入口、历史报告或构建产物 |

开始审阅时先执行 `wc -l` 和 `shasum -a 256`。下列六份主审输入在写入报告前重新计算，行数、摘要均未变化：

| 输入文件 | 行数 | SHA-256 |
|---|---:|---|
| [AMD 平台页](../../paths/platforms/amd.md) | 125 | `842715335cbd95ab56926a52d2e8af968157065b693211c07bfc13ab66e214a1` |
| [NVIDIA 平台页](../../paths/platforms/nvidia.md) | 208 | `fe49690a0ffe68e8ad5eef7c8e1e361e4adfe10b7870b0fdc2c5bddf2e9c05c6` |
| [昇腾平台页](../../paths/platforms/ascend.md) | 228 | `79a8e5e9a325dd8d9b655cebbcde3694357d510fc913090ae59ec9a48c887fea` |
| [训练排障页](../../paths/tasks/training-triage.md) | 169 | `ec072b7b433c88e5d9d24a95e3ac15383b164a761a8aab8088c37589f838b1f4` |
| [推理排障页](../../paths/tasks/inference-triage.md) | 143 | `569e212bf7d4348651d3e1247ff4b706a963806b362b4303162cc1162a2e86e7` |
| [T00-08 取证记录](batch-32-t00-08-sources.md) | 29 | `f0e33b60ced60a08d77a9b6e3e592381e73490544c645024030296df68c1a825` |

**初审结论：需修订并定向复核，暂不通过。共 3 项发现：P1 0 项、P2 2 项（C01–C02）、P3 1 项（C03），全部为 OPEN。** AMD 的主要文档样板、健康及 RCCL 验证链成立；新增排障分支与结构校验成立。剩余问题是个别 AMD 入口没有对应平台取证边界、五页尚缺阅读完成检查，以及入口回链不齐。不能据本次链接检查宣布 00.6 最终关闭。

优先级口径：P1＝足以严重误导处置的关键错误；P2＝影响任务交付、导航功能或验收证据的必修事项；P3＝局部入口、记录或可追溯性问题。下文各导航页行号以上表输入为准；“完成检查”指阅读路径的知识与证据产出，不要求本轮执行硬件验证。

## 范围与方法

先读 `README.md`、`AGENTS.md`、[编写指南](../authoring-guide.md) §3/§5/§6/§7、`schemas/content.schema.json` 和 `content-outline.md`。报告格式参照 [T06-09 初审](batch-31-t06-09-codex-review.md)及 [T00-05 初审](batch-31-t00-05-codex-review.md)。完整读取五页和取证记录，以 [backlog](../../plans/full-coverage-backlog.yaml) T00-08 L7603–7737（objective、三条 acceptance 和来源限制在 L7629–7644）及主题 00.6 L291–340 为依据；特别核对 L332 的“具有先修和目标/完成检查”。

本轮进行了以下只读核对：

1. 解析五页全部内联本地链接，核对目标文件、稳定 ID、类型、平台字段、`related_ids`、来源 ID 和日期；对四页修订与父 commit 比较，区分新增和保留内容。
2. 逐个检查 NVIDIA/昇腾新增正文入口的平台字段，抽查其实际正文段落；对 AMD 的硬件、软件栈、框架分发、RCCL、健康、推理交集及 unknown 清单作定向正文核对。通用方法与具体平台实现分别判断，未把 `generic` 自动当作 AMD 兼容证据。
3. 检查两个排障表的全部行和新增分支，比较旧行原文；检查三平台/两排障页之间的直接链接，以及 README、00 首页、角色页和其他知识/路径页的入链。
4. 将 AMD 页尾四项 URL 与 registry 对应 ID 逐字比较；对照取证记录的数量口径及取证限制。未重新抓取外部网页，未重审兄弟篇全部上游技术主张；本报告的技术抽查结论限于导航是否准确承接已有正文及其证据边界。
5. 执行 `PYTHONDONTWRITEBYTECODE=1 make check`。遵守本轮只新增报告的范围，未执行 `make build`、测试或任何正文中的安装、诊断、恢复、采样、编译和故障注入命令。

### 共用链接、稳定 ID 与表格验收

| 页面 | 本地链接处数 / 不同目标 | related ID 数 / 本次新增数 | 稳定 ID 与日期 |
|---|---:|---:|---|
| AMD | 55 / 46 | 42 / 42 | `path.platform.amd` 在父 commit 中不存在；新 ID 全库唯一；2026-10-22 |
| NVIDIA | 82 / 82 | 73 / 31 | `path.platform.nvidia` 与父 commit 相同；2026-10-22 |
| 昇腾 | 98 / 91 | 85 / 28 | `path.platform.ascend` 与父 commit 相同；2026-10-22 |
| 训练排障 | 97 / 71 | 61 / 12 | `path.task.training-triage` 与父 commit 相同；2026-10-22 |
| 推理排障 | 82 / 59 | 46 / 9 | `path.task.inference-triage` 与父 commit 相同；2026-10-22 |

五页合计 **414 处本地链接、118 个不同目标**，全部目标存在；全部 related/source ID 存在。五页均为 `type: path / domain: overview / status: draft`。两个排障页保持 `platforms: [generic]`，三平台页分别标自己的平台；四个旧 ID 没有被重新分配。

训练表 L96–118 含表头/分隔行共 23 行，新增 9 个内容行；推理表 L80–96 共 17 行，新增 8 个内容行。**每行均为 4 个管道符、3 列**。与父 commit 对照，训练表原有 14 行、推理表原有 9 行（均含表头/分隔行）逐行原文保留；没有旧行截断或错列。推理原有 OOM 行仍指昇腾专篇，新增 L89 明确提供 NVIDIA/AMD 分支，二者可区分。

## 已核实的主链与边界

### AMD 的样板、观测与验证链

| 导航位置 | 实际正文承担与核对结论 |
|---|---|
| AMD L63、L67、L71：硬件与栈样板 | [执行与数据移动](../../knowledge/01-hardware/accelerator-execution-and-data-movement.md) L49–51 的确使用 H100 / **MI200（CDNA2）** / Atlas A2 三种代际样板；[资源拓扑](../../knowledge/01-hardware/resource-topology.md) L52、L157–158 另有 Supermicro/MI300X 节点样板。两种 AMD 代际各有所指，导航没有将 MI200 写成 MI300X 的同一硬件组织 |
| AMD L67：ROCm 与框架 | [AMD ROCm 档案](../../knowledge/02-software-stack/amd-rocm-documented-profile.md) L140–149 分别记录框架声明、AMD 索引与上游 wheel 渠道，L216–227 分列 documented/conflict/unknown，均为 not_run。入口没有把上游 PyTorch wheel 与 AMD 分发渠道合并，也没有把不同文章的版本拼成整栈实测组合 |
| AMD L67、L90：RCCL | [三库档案](../../knowledge/03-communication/communication-library-profiles.md) L43–52 独立记录 RCCL 2.30.7；[RCCL 运行档案](../../knowledge/03-communication/rccl-runtime-and-verification.md) L40、L46–50 保留五元仅为文档交集的限制。L74–82 实有 rccl-tests 计时/重跑校验、N/A 和门限口径，L91–99 实有两节点待执行设计；没有把单节点 ≥304 GB/s 样例当作两节点通过线 |
| AMD L91：健康、AFID 与 N/A | [健康正文](../../knowledge/01-hardware/health-evidence.md) L313–343 有 AMD SMI 27.1.0 / docs-10.1.0、CPER/AFID 与 AFID 最小集合，L357–365 分字段级/节级解释 N/A、查询失败和原因未知。入口称“数据不可用判定”，未将所有 N/A 一概改为采集失败或零错误 |
| AMD L91：BMC OEM | [BMC 正文](../../knowledge/01-hardware/bmc-firmware-and-events.md) L117–127 确为 Supermicro/MI300X 机型 OEM 支路，并明确 OEM 行为不代表 AMD 官方行为；L205 保留 MI300X 逐项 FirmwareInventory 与 OAM 固件暴露 unknown。入口没有虚构 AMD 自有 BMC 管理接口 |
| AMD L87–89、L93–96：执行、OOM、质量及性能 | [GPU 算子诊断](../../knowledge/02-software-stack/gpu-op-graph-failure-triage.md) L53、L57、L70 有四分支和 AMD 独立文档线；[GPU 内存正文](../../knowledge/02-software-stack/gpu-memory-oom-evidence.md) L53、L81–90 实有 HIP 7.14.60850 独立证据。混合精度、性能和输出质量目标均含 amd；[性能正文](../../knowledge/06-training/performance-analysis.md) L72 仍区分 ROCprofiler 旧版样板与 ROCm 10.1.0；慢 rank 伴随入口的不足见 C01 |
| AMD L94：推理交集与量化 | [引擎档案](../../knowledge/07-inference/engine-backend-boundaries.md) L90–103 有 AMD/ROCm 交集，PD、KV 与制品身份仍有未证实项；[量化正文](../../knowledge/07-inference/quantization-and-quality.md) L40、L106 起独列 AMD/ROCm。导航没有把 NVIDIA 功能表复制成 AMD 支持矩阵 |
| AMD L100–104：unknown | ROCm 档案 L218–227 保留 HIP/LLVM 站标冲突、虚拟化、Windows/WSL2、AGFHC/CVS 等未知；RCCL 档案 L105 保留整栈已测组合、latest/别名 diff、最早入版和 hang 机理等未知。导航用链接委托清单，没有转写成已支持/已不支持。这里列明的是抽查对象，不替原正文增加结论 |
| AMD L75、L103：架构边界 | [参考架构](../../knowledge/00-overview/reference-architectures.md) L113–115 的确将 AMD 放在 OEM 节点＋平台档案经通用接口接入集群的位置；AMD 官方同构超节点仍未知。该节的**集群参考样板实际是 NVIDIA DGX SuperPOD H100**，L146 也保留 AMD 集群级官方同构样板未取得；入口没有把它改称 AMD 官方集群方案 |

AMD 直接链接 **36 个不同知识目标**：21 个明确含 `amd`、9 个 generic 领域 index、6 个其他 generic 正文。后六篇是配套证据、设备资源链、节点验收、带宽退化、慢 rank 和静默错误判定；其中带宽退化正文 L78–79/L127 有 RCCL 取证入口，静默错误正文 L164–169 有 AMD 平台清单。节点验收在 AMD L92 已限定为通用方法并另指 RCCL。其余通用模型不能因此自动升格为 AMD 实现证据，重点不足见 C01。

取证记录 L14 的“30 篇 platform 含 amd”可复算为 AMD 页 **related_ids 中的 30 个含 amd 条目**，并非正文内联链接数量：其中 9 篇（runtime、operators、framework-backend、host-resource、distributed-inference、capacity、routing、PD、release）目前仅在 related_ids 中。此处记录两种口径，不将其误判为 30 个链接失效，也不以元数据中的 ID 替代读者可见的逐链解释。

### NVIDIA、昇腾与新增排障行

| 核对组 | 正文落点与结果 |
|---|---|
| 两平台新增条目的平台字段 | NVIDIA 新增的 31 个知识入口、昇腾新增的 28 个知识入口逐条核对：均含对应具体平台或为通用模型/方法；不存在具体平台排斥项。昇腾未列 routing-and-flow-control、RCCL 档案及两篇 GPU OOM 正文；NVIDIA 未列 RCCL 档案、MindIE 专属档案。generic 调度器/框架正文的样板仍按各自正文区分 |
| 硬件与软件描述 | NVIDIA L157–172、昇腾 L147–160 的 H100/Atlas A2、OEM/iBMC、NUMA 和互联描述与目标相符。[安装正文](../../knowledge/02-software-stack/environment-installation-and-upgrade.md) L55、L77、L111 分别承载 CUDA 12.8 / CANN 8.3.RCX / ROCm 10.1.0 及七层梯子，并明确运行时篇旧版方法须重核；导航保留不同样板版本，没有据“七层”承诺目标环境安装成功 |
| 框架、训练与隔离 | [框架适配](../../knowledge/02-software-stack/framework-backend-adaptation.md) L55、L74–78 区分 CUDA/ROCm 内置路径及 TorchNPU；两平台的 framework/workflow/performance 入口描述成立。[共享隔离](../../knowledge/05-cluster-platform/accelerator-sharing-and-isolation.md) L116、L128–130 保留 time slicing 与 vNPU/vCANN-RT 条件；两平台页没有抹去故障隔离 unknown |
| 训练新增 9 行，L110–118 | GPU 算子/内存分别进入 GPU 专篇并另链昇腾；主机资源正文 L81–85/L164–167 有 cgroup 与 AMD 访问支路；[控制面](../../knowledge/05-cluster-platform/control-plane-recovery.md) L52–58 实有恢复点和账本；[drain](../../knowledge/05-cluster-platform/node-drain-resource-reclamation.md) L43–47 区分退出服务与实际回收；[多租户验证](../../knowledge/05-cluster-platform/contention-capacity-validation.md) L98/L106–109 有单租户基线与两租户对照。存储/BMC 行准确对应其证据入口 |
| 推理新增 8 行，L89–96 | [GPU OOM](../../knowledge/07-inference/gpu-inference-oom-triage.md) L45 明确 NVIDIA/AMD 与首失败阶段；[模型装载](../../knowledge/07-inference/model-loading-and-readiness.md) L44 分三条引擎证据线；引擎交集、[输出质量](../../knowledge/07-inference/output-quality-evaluation.md) L42 的输入身份/四层指标、[容量](../../knowledge/07-inference/capacity-and-autoscaling.md) L50 起触发器、[路由](../../knowledge/07-inference/routing-and-flow-control.md) L45 起四层职责均有实际正文。没有把 generic 推理导航声明为昇腾已具备 routing 专篇的平台取证 |
| 存储与恢复验证 | [存储恢复](../../knowledge/04-data-storage/storage-client-backend-recovery.md) L43/L64 以保留证据、保护恢复点为前提；[服务恢复](../../knowledge/07-inference/release-and-recovery.md) L44/L48 区分 liveness/readiness/质量并给出预热→递增→gate→drain；训练 L130 所述正确性与持续进展双判据由[故障恢复路径](../../paths/tasks/fault-recovery.md) L33 承担。导航没有把读回、进程重启或探针成功单独当作恢复通过 |
| 编辑与执行边界 | 三平台及两任务页仍为 draft，均声明未实测。NVIDIA L194、昇腾 L181 和 AMD L63/L104 保留文档样板、独立版本及未知项，不形成统一兼容矩阵。九领域通过现有 index 可达，无正文复制或未来文件假链接 |

### AMD 四项外部入口逐字核对

| AMD 行号 | source ID / registry 起始行 | URL 比较及采信边界 |
|---|---|---|
| L116 | `src.amd.rocm-install-docs-10.1.0` / L2660 | `https://rocm.docs.amd.com/en/docs-10.1.0/install/rocm.html`，逐字一致 |
| L117 | `src.amd.rocm-release-notes-10.1.0` / L2632 | `https://rocm.docs.amd.com/en/docs-10.1.0/about/release-notes.html`，逐字一致 |
| L118 | `src.amd.rccl-docs-6.3.3` / L2441 | `https://rocm.docs.amd.com/projects/rccl/en/docs-6.3.3/index.html`，逐字一致；登记站标为 RCCL **2.21.5**，只是历史文档入口，不拿它证明正文的 2.30.7 样板 |
| L119 | `src.amd.amd-smi-docs-10.1.0` / L1842 | `https://rocm.docs.amd.com/projects/amdsmi/en/docs-10.1.0/index.html`，逐字一致；登记标题/修订对应 AMD SMI 27.1.0 |

四项均为既有官方登记，未新增来源或用未登记主页充当兼容依据；RCCL 2.30.7 的细节通过所链 RCCL 正文的 docs-10.1.0 证据承接。这个 URL 检查不代表本轮再次认证远程页面内容。

## 逐项发现

### C01 · P2 · OPEN · AMD 入口未区分通用伴读与尚无 AMD 取证的具体诊断实现

- **位置**：AMD L80、L95；关联 L63、L108 和取证记录 L14–15。
- **问题**：AMD 平台页把“设备暴露核对”直接交给 generic 设备资源链，并把慢 rank 指南与有 AMD 取证的性能分析并列为首要入口，但没有说明前者尚无 AMD 插件/运行时接入取证、后者具体诊断证据仅为 PyTorch/NCCL/DCGM。按本轮要求，不能只凭 `generic` 把这些实现路径视为已核对的 AMD 分支。页首的统一“非兼容矩阵”声明不足以定位到这两个入口的实际证据缺口。
- **证据**：
  1. [慢 rank 指南](../../knowledge/06-training/slow-rank-triage.md) `platforms: [generic]`（L7），来源 L9–14 为 PyTorch/NCCL/DCGM；L26、L46 固定 PyTorch 2.8 / NCCL 2.27.5；L54–58、L65 起实际使用 NCCL RAS、desync、flight recorder 和 DCGM。全篇没有 AMD/ROCm/RCCL/HIP 取证段落。不能由接口或库名相似推定这些检查在目标 RCCL/ROCm 构建成立。
  2. [设备资源链](../../knowledge/05-cluster-platform/device-resource-chain.md) L43–58 给出 Kubernetes 通用责任模型，其实现例子是 MindCluster、NVIDIA Device Plugin 与 Slurm；全篇没有 AMD 实现取证。对 AMD 设备节点和容器访问，已有的 [OS/进程资源正文](../../knowledge/02-software-stack/host-resource-pressure-and-device-access.md) L164–167 反而明确核对 `/dev/kfd`、render node、权限及 ROCm 容器文档，但在 AMD 页仅登记了 related ID，没有正文链接。
  3. 对照有效通用入口：[带宽退化正文](../../knowledge/03-communication/bandwidth-degradation-triage.md) L78–79/L127 实有 RCCL 对照；静默错误正文有 AMD 证据清单；节点验收的链接文字已经写明“通用方法，AMD 侧通信基线样板用 RCCL 档案”。C01 不否定通用责任模型或阶段分析方法，只指出当前两处入口没有同等清楚地隔开方法与实现取证。
- **建议修订**：让 AMD 的实际访问/慢 rank 诊断优先进入已有 AMD 取证正文（如主机设备访问、性能分析和 RCCL 档案）；需要保留的通用伴读，逐项说明仅借用责任链或阶段分析，AMD 具体插件、RAS/desync/flight recorder 等能力仍待核对。同步取证记录的覆盖表述；不必为修导航而补写兄弟篇或开展硬件试验。
- **关闭条件**：读者能在入口处区分“含 AMD 取证的诊断目标”“通用方法伴读”“AMD 实现能力尚未核对”；所列具体 AMD 检查可追到相应正文条件，不能由 generic、NCCL 相似接口或另一平台插件推导兼容。

### C02 · P2 · OPEN · 五页没有承载 00.6 所要求的阅读完成检查

- **位置**：AMD L65–112；NVIDIA L96–118、L155–198；昇腾 L108–185；训练排障 L84–134；推理排障 L68–112；[主题定义](../../plans/full-coverage-backlog.yaml) L295、L332。
- **问题**：五页均有用途说明、材料/问题入口和不同程度的环境或证据输入要求，但没有面向读者的路径完成检查。因而虽可证明“有入口”，尚无法按 00.6 判断“走完路径后应能交付什么、哪些条件未知时尚不能完成”。这属于主题关闭所要求的导航内容缺口，不是要求将路径变成实测操作手册。
- **证据**：
  1. 00.6 `delivery_scope`（L295）要求每条路径带先修、目标与完成检查；`closure_criteria` 第一条（L332）再次明确“具有先修和目标/完成检查”。T00-08 的五个目标都在该主题中。
  2. 三平台页的“先明确环境”分别要求记录机型、版本、拓扑，后面列领域和正文；没有检查读者是否已区分样板与实际环境、能否找到对应取证/unknown、能否说明下一项验证缺什么。AMD L125 的 `make check` 是作者的文件/ID 检查，不能代替读者的完成检查。
  3. 两排障页“先整理问题描述”提供输入，“形成案例时保留什么”提供案例记录要求；二者之间只有入口表和相关链接，未明确一次**知识定位**何时完成（例如症状、首要领域、候选原因、缺失证据、下一项检查及停止条件能否对应起来）。正文里的恢复完成判据也不能自动充当导航路径本身的完成检查。
- **建议修订**：在五页各补一组简短、可核对的阅读产出，并明确必要先修/进入条件及目标；可以引用所链正文的现有判据，不复制机制或命令。平台路径可检查版本/制品身份与未知组合、平台术语和验证入口；排障路径可检查现象→证据→假设→下一项检查/停止条件的定位结果。
- **关闭条件**：五页均有能定位的先修/进入条件、知识目标及完成检查，读者可据此判断已完成、仍需补证据或超出路径范围；实际执行与硬件验证仍保持独立状态。本轮不代改主题状态。

### C03 · P3 · OPEN · 平台回链和任务入口未完成一致收口

- **位置**：AMD L108、L112、L125；NVIDIA L118、L196–198；昇腾 L183–185；关联[角色页](../../paths/roles/reading-by-role.md) L89。
- **问题**：AMD 页能直接进入另外两平台及两个排障页，两个排障页也都能进入三平台；但 NVIDIA/昇腾“任务路径入口”只列六条阶段路径和角色页，遗漏两个既有排障首要入口。昇腾页还没有另外两平台的比较/切换链接。角色路径的平台枚举继续只列昇腾/NVIDIA。现有 README/00 首页仍能绕行到 AMD，因此这是局部入口不齐，不是全库不可达。
- **证据**：在五个目标内部解析全部直接链接，邻接关系如下：

  | 起点 | 直接链接的本组目标 |
  |---|---|
  | AMD | NVIDIA、昇腾、训练排障、推理排障 |
  | NVIDIA | 昇腾、AMD |
  | 昇腾 | 无 |
  | 训练排障 | 昇腾、NVIDIA、AMD |
  | 推理排障 | 昇腾、NVIDIA、AMD |

  [README](../../README.md) L31 的平台行确有 AMD；[00 首页](../../knowledge/00-overview/index.md) L39 的 00.6 行、L50 也有三平台。角色页 L89 在 commit 基准和当前工作区均只枚举两平台；其当前并发修订未改变该处。AMD 有 README/00 首页、NVIDIA、两个排障页等入链，不能声称“AMD 无入口”。
- **建议修订**：在 NVIDIA/昇腾现有任务入口中接入训练/推理排障；为昇腾补与另两平台一致的比较/切换入口。角色页的旧枚举作为关联导航同步项交给相应作者处理。无需将五页改成全互链图，也无需重复正文。
- **关闭条件**：从任一平台页能直接找到两个排障首要入口，三平台间的切换方式一致；角色导航的平台枚举与三平台现状相符或明确只是选定示例；本地链接和 ID 继续有效。

## acceptance 逐条判断

| 条款 | 初审判断 | 依据与限制 |
|---|---|---|
| 1 · AMD 串联硬件/ROCm/RCCL/框架/观测与验证方法，明确样板及未取证组合 | **主要链成立，C01 必修** | 样板、框架分发、健康、RCCL 计时与两节点设计及 unknown 委托准确；慢 rank/设备访问入口的 AMD 实现取证边界仍需就地分清 |
| 2 · NVIDIA/Ascend 链接完整 v1 领域内容，保留术语、档案及已知未知，不改写统一兼容矩阵 | **内容入口与平台边界满足本轮抽查；收口仍有 C03** | 九领域入口和新增 31/28 个知识入口存在，平台字段无错误排斥项，描述及独立版本抽查成立；不据此宣称所有兄弟篇技术主张或真实组合已经重新验证 |
| 3 · 两排障入口纳入新诊断分支与恢复验证，五目标共用链接/稳定 ID 验收 | **新增分支、恢复验证、表格与 ID 子项满足；回链需 C03 修正** | 新增 9/8 行，旧行全部保留；414 处链接和 ID 校验通过；双判据/服务质量验证有正文承担 |
| 00.6 关联关闭条件 · 已核对正文、先修、目标/完成检查，无复制或未来文件假链接 | **尚未满足，C01–C02 必修** | 没有失效文件或重复正文；但 generic 实现不能充作 AMD 取证，五页缺少阅读完成检查。主题其他角色/任务的独立审阅、修订与复核也不能由本报告代为关闭 |

取证记录的“复核轮修订记录（初审后）”仍为待追记，符合本轮初审阶段，不能预先当作已完成修订/复核；任务与主题账本仍为 planned，本报告不据此自动报错或代改状态。

## 校验、输入快照与结论

实际执行 `PYTHONDONTWRITEBYTECODE=1 make check`，退出码 **0**：**PASS：135 content entries / 577 sources**。其检查范围为结构和本地文件链接，不验证远程页面、锚点、描述语义、平台能力或兼容性。表格列数、父 commit 旧行保留、平台字段、直接回链及版本边界另由上述只读核对承担。

开始时还对以下方法/定义/入链文件执行了 `wc -l` 与 `shasum -a 256`，基准如下：

| 文件 | 行数 | SHA-256 |
|---|---:|---|
| README.md | 158 | `4c2e54298f2693173dae66377124c90c4481fc4d5d01fe7efde09621c9a71874` |
| AGENTS.md | 22 | `69262a5db32adfac46f6ab28d48d9670f2e1700cb2b946155ad3f3ccfe6f6454` |
| docs/authoring-guide.md | 132 | `75ee28d1aca7a4ac1d56ae493856037770a14fcdac27fa9b662451cee169a801` |
| schemas/content.schema.json | 52 | `b60b8d9ccb8728f034607901124c4206f5dc705ca824e31ce0ab5615523d0147` |
| content-outline.md | 191 | `ed9033d2f53fa504fc05e55b221697dd7a1d14c5adaf58f8cc0a6613f8fe7046` |
| plans/full-coverage-backlog.yaml | 7774 | `abffb0eaff9a825ac37ff1921acfa7a2d1fb73289d85f9d8d88a24febec71530` |
| sources/registry.yaml | 7249 | `78ee35bbb0bd602d200deb5a1370af894d4765f723aeaa1970543f4be90adeed` |
| knowledge/00-overview/index.md | 69 | `365231c7cc00790fc3bde9064f0ddf7513c22429f87ed5337e272dde829a8a3f` |
| docs/research/batch-31-t06-09-codex-review.md | 140 | `ab68d30cf6560b580f622ed6225251ed3b8e1e8fd1efb60db8a0c96d6edb1dff` |
| docs/research/batch-31-t00-05-codex-review.md | 139 | `0da82777995cdbc96e1da584763e86607097dbe107705496888919ce471ee5fc` |

本工作区开始时已有其他 Batch 32 文件的修改与三份未跟踪审阅报告。对 710 个 Git 跟踪及非忽略的未跟踪文件做只读 SHA-256 快照，审阅开始至本报告写入前观察到 5 个范围外文件变化：`batch-32-t00-07-sources.md`、角色页、故障恢复页、迁移升级页和性能优化页；无新增/删除。这些并发变化不由本会话工具产生。六份主审输入始终与头表及目标 commit 一致；没有把工作区其他修改归成本报告的修订。

报告落盘后再次对照写入前快照：710 个既存文件无变化、无删除，唯一新增文件为本报告（共 711 个）；报告内联本地链接检查无缺失。本会话唯一文件写入为本报告；未执行 `make build`，未改 `src/kb/`，未新增测试或运行 `make test`，未操作真实集群。**C01–C03 全部保持 OPEN，T00-08 需作者修订后由同一审阅者定向复核。** 模型审阅、入口完整和结构通过均不建立硬件验证结果，不授权关闭真实验证轨道或宣布 00.6 最终覆盖通过。
