# V00 准备实例独立审阅报告

审阅日期：2026-10-22。审阅角色：独立审阅，与交付物写作分开。本轮只新增本报告，不修订被审文件。

**审阅范围结论：修订后通过。** 本轮发现 **6 项 P2 应修、1 项 P3 建议，0 项 P1**。P2 均为 OPEN，当前尚不能声明审阅通过；须由写作方修订，再由独立审阅者定向复核。这里评价的是准备实例骨架的交付质量，不是 V00 实例验收、资源就绪或真实环境验证通过。

## 审阅对象、基准与方法

- 主体：[v00-preparation-instances.yaml](../../plans/v00-preparation-instances.yaml)，以及同步修改的 [validation-backlog.yaml](../../plans/validation-backlog.yaml)、[交付与审计记录](v00-preparation-record.md)。用户会话称 Batch 33；本报告沿用“独立验证轨道首轮交付”，不计入内容批次。
- 逐份读取 V01–V07 的七份 experiment 正文（V06 覆盖两个实例），对照假设、组名、条件分支、停止/恢复要求、版本身份与边界；对 V08–V12 的 22 个不同方法文件核对存在性、章节定位，并抽查其概括所指段落。
- 完整解析 [来源登记表](../../sources/registry.yaml)，逐一核对实例列出的全部来源 ID；以 `git diff HEAD -- plans/validation-backlog.yaml` 和结构化字段比较核对改动范围。
- 阅读仓库 README、authoring-guide、content-outline、内容 schema 与根 AGENTS.md。使用仓库拒绝重复键的 YAML loader 解析实例、backlog 和 registry，另外检查映射、字段、状态与数量。
- Git 比较基线：`e26f6b5be374dafa4c196d8c9fb99133be51bf50`。开始审阅时已有三项交付改动：backlog 已修改，实例文件与交付记录未跟踪；它们不是本轮审阅产生的改动。

本轮核对的是仓库内转写与交付账面；未重新获取远程上游资料，未执行安装、训练、通信、存储、集群或硬件验证。方案自身的技术正确性、远程页面当前内容及现场兼容性不在本轮结论内。

## 发现

### V00R-C01 — 四个来源 ID 被改写，五处引用无法在 registry 解析

- **优先级：P2 应修；状态：OPEN。**
- **分类：事实错误（来源登记事实），并造成结构/账面不一致。**
- **受影响位置：** `plans/v00-preparation-instances.yaml` 的 V04、V05、V06-CPU、V06-DCP-MULTIRANK / `source_anchors`；`docs/research/v00-preparation-record.md` 第 27 行。
- **问题：** 版本号中的点被转写为短横线。实例共有 22 次来源引用、19 个不同字符串，其中 5 次引用涉及 4 个未登记 ID；其余 17 次引用均存在。登记表本身没有新增来源，但“全部 source_anchors 复用既有登记”的账面主张不成立。

| 实例与行号 | 实例中的未登记值 | registry 中既有的正确值与行号 |
|---|---|---|
| V04，180 | `src.pytorch.processgroupnccl-env-2-8` | `src.pytorch.processgroupnccl-env-2.8`，772 |
| V05，221 | `src.pytorch.numerical-verification-2-6` | `src.pytorch.numerical-verification-2.6`，475 |
| V05，222 | `src.pytorch.parallel-training-state-2-6` | `src.pytorch.parallel-training-state-2.6`，460 |
| V06-CPU，260；V06-DCP-MULTIRANK，300 | `src.pytorch.dcp-2-6` | `src.pytorch.dcp-2.6`，308 |

- **证据：** 对应方案 frontmatter 保留正确 ID：`nccl-timeout-experiment.md:11`、`gpu-npu-precision-difference-experiment.md:10–11`、`checkpoint-state-recovery-experiment.md:9`。交付记录第 27 行称“全部 source_anchors 复用既有登记”。
- **关闭条件：** 五处引用恢复为既有稳定 ID，不为错拼值新增 registry 别名；遍历全部来源引用，确认未解析项为零，再核对交付记录的来源复用主张。

### V00R-C02 — 六个实例漏列约定字段，字段齐备的自检账面不实

- **优先级：P2 应修；状态：OPEN。**
- **分类：结构/账面不一致。**
- **受影响位置：** `plans/v00-preparation-instances.yaml` 的 V10-NFS-V41、V10-RGW-S3、V10-LUSTRE、V11-NODE-CHANGE、V11-CONTROL-PLANE、V11-SERVICE-RECOVERY / `source_anchors`；交付记录第 30 行。
- **问题：** 这六个实例省略了 `source_anchors`，并非显式空列表。它们与同文件的 `instance_schema` 及其他同类实例结构不一致，严格按字段读取的消费者会遇到缺键；交付记录声称“必填字段齐备”，没有披露此差异。
- **证据：** 实例文件第 28–37 行声明实例字段，第 34 行列出 `source_anchors`。六处 `method_content_refs` 后直接进入 `known_fields`，分别在第 477–482、510–515、543–548、607–610、638–640、667–671 行。同类的 V10-LOCAL-EXT4-NVME 第 448 行、V11-SHARING-ISOLATION 第 578 行均显式填写 `source_anchors: []`。交付记录第 30 行称自检包含“必填字段齐备”。
- **关闭条件：** 六个实例补齐该字段；没有直接来源锚点时可用 `[]`，无需为凑字段新增来源。按约定字段检查全部 19 个实例，更新并重核自检账面。当前 `instance_schema` 是说明性映射，不应把 YAML 能解析等同于字段完整性已验证。

### V00R-C03 — 新增说明把独立实例门槛改成了全体等待

- **优先级：P2 应修；状态：OPEN。**
- **分类：转写走样（依赖与状态推进语义）。**
- **受影响位置：** `plans/validation-backlog.yaml` / V00 / `preparation_note`，第 42 行新增末句。
- **问题：** “全部实例通过各自验收前 V00 与各 V 包保持 planned”要求所有包等到全部实例通过才可推进。原规则允许某个实例通过后，仅对应子组独立就绪；其他环境未知或其他组仍 planned 不应阻塞它。当前所有状态仍 planned 是正确的，但追加句为后续推进设立了错误总门槛。
- **证据：** 新句明确写“全部实例……前……各 V 包保持 planned”。同文件第 39 行原验收句则是“该实例通过只使相应验证子组就绪，不代表所有验证资源准备完成”；第 505–506 行规定“仅该实例通过才允许对应运行；不要求先取得所有环境”。V10 第 390 行、V11 第 457 行也要求其他子组可以继续 planned。实例文件第 723–727 行保留了正确的局部门槛表述。
- **关闭条件：** 追加说明只陈述本次骨架交付后当前状态不变，并明确后续按各实例独立验收与推进；总包完成仍遵守各自完整验收条件。用“V06 CPU 实例已验收、其他资源仍未知”和“V10 一个后端已验收、其余后端仍 planned”两个纸面场景复核，不要求实际运行或改变当前状态。

### V00R-C04 — V06 第二实例的环境缺项与通过条件没有覆盖 DCP 端到端组的版本

- **优先级：P2 应修；状态：OPEN。**
- **分类：转写走样（已固定版本分工遗漏）。**
- **受影响位置：** `plans/v00-preparation-instances.yaml` / V06-DCP-MULTIRANK / `unknown_fields.environment_identity`、`instance_pass_requirements`，第 310–325 行。
- **问题：** 实例第 305 行纳入 H0、EP/EF、BP/BF/BS、D0 以及多 rank 的 L0/L1/L2，但环境缺项只列“独立 PyTorch 2.6.0 环境”，通过条件也只要求建立“独立 PyTorch 2.6 多进程环境”。原方案仅对多 rank 部分固定 2.6.0；H0 使用 2.8.0，P/F 端到端组分别使用固定 parent/commit。只按当前最小清单准备 2.6 环境，无法覆盖本实例自己声明的 B 组。
- **证据：** `checkpoint-state-recovery-experiment.md:63–66` 固定 P/F/H 的三种身份；第 75 行仅在“多 rank 部分”固定 2.6.0；第 101–105 行分别列 H0 的 2.8.0、EP/EF 与 BP/BF 的 parent/fixed 路径以及 D0；第 144–146 行将端到端组与独立 2.6 多 rank 组分开执行。backlog 第 253–254 行要求第二阶段准备“对应 PyTorch/DCP 构建和启动方式”。实例第 306 行的“多 rank 部分固定 PyTorch 2.6.0”本身正确，问题是后面的准备清单没有保留这一限定。
- **关闭条件：** 分列端到端 B 组与多 rank C 组的环境、构建与启动要求；B 组可明确引用 V06-CPU 的不可变 P/F 制品身份，H0 另列 H 身份，不能以 2.6 环境替代。补齐各组脚本、输入、状态契约与证据准备的引用；未覆盖的组明确保留未就绪。这里要求修正骨架清单，不要求本轮真实构建制品。

### V00R-C05 — V02 的通过判据丢失 N1 的条件性

- **优先级：P2 应修；状态：OPEN。**
- **分类：转写走样（判据条件遗漏）。**
- **受影响位置：** `plans/v00-preparation-instances.yaml` / V02 / `known_fields.preregistered_criteria`，第 101 行。
- **问题：** 该字段把“N1 差异稳定首现于逻辑 ID 选择并随恢复消失”列为无条件的通过要求。原方案允许无法安全构造 N1 时仅保留 B0/C0/R0，并把 H3 记为未验证；不能因未运行获准省略的 N1 而否决其余设计范围。实例第 99 行正确保留了条件性，但第 101 行与之冲突。
- **证据：** `ascend-device-visibility-experiment.md:62` 写“若无法构造单变量 N1，只保留 B0/C0/R0 并把 H3 记为未验证”；第 104 行判据以“若执行 N1”开头。实例第 101 行则以“通过须……”直接串联 N1 的要求。
- **关闭条件：** 判据恢复“若执行 N1”的限定，并明确不执行时的覆盖范围与 H3 未验证状态；以“环境证据不足以安全区分物理/逻辑 ID”的纸面分支定向复核。不得通过猜编号来满足判据。

### V00R-C06 — 实例最小通过清单未统一兜住 V00 的全部验收面

- **优先级：P2 应修；状态：OPEN。**
- **分类：结构/账面不一致（验收条件覆盖不足）。**
- **受影响位置：** `plans/v00-preparation-instances.yaml` / `instance_schema.instance_pass_requirements`、各实例的通过清单和 `common_unknowns_note`；重点例为 V05、V07、V11-SHARING-ISOLATION、V12。
- **问题：** 文件将 `instance_pass_requirements` 定义为“还须补齐的最小集合”，但各实例列出的条件没有共同的完整验收兜底。部分清单不要求把仍为 null 的授权、清理恢复负责人及条件落实为可审阅记录；部分也未明确脚本/输入冻结与重复策略。共同说明解释四个 null 的现状及真实取得后才能填写，却没有明确“这些面与适用缺项未审定时，任何局部清单完成都不能令实例通过”。这不是要求现在填实缺项，而是需要防止以后只按局部列表验收。
- **证据：**
  - backlog 第 35–39 行要求资源窗口/隔离/清理/停止恢复、脚本/输入/预先判据/重复策略、外置证据，以及完整验收句。
  - 实例第 37 行把通过清单定义为“最小集合”。V05 第 240–243 行和 V07 第 359–362 行仍有四个共同 null，但各自第 244–247、363–366 行的清单没有列明授权与清理恢复条件的审定。
  - V11-SHARING-ISOLATION 第 589–590 行脚本/输入和重复/阈值仍 null；第 595–598 行只要求环境身份、baseline/干扰清单以及授权/负责人/证据位置，没有要求这些冻结面完成。
  - V12 第 719–722 行没有清理恢复条件与可复核执行脚本/评测输入冻结的明确门槛；仅“记录负责人”不能代替清理恢复条件。第 723–727 行的共同现状说明也未列出完整共同验收规则。
- **关闭条件：** 明确所有实例均须满足的共同通过门槛，并由各局部清单引用：真实环境与来源身份、脚本/输入冻结、预先判据和适用重复策略、已有授权及隔离/资源预算、停止/清理/恢复条件与负责人、外置脱敏证据位置均可审阅。适用项仍缺失时保持 `not_ready`；确实不适用的项给出范围和理由，不静默省略。可以指向方案原有条件，不要求复制全文，也不要求在本轮取得资源或授权。修订后逐实例核对覆盖，特别重查上述四例。

### V00R-C07 — 建议为 V11 节点变更的 B0/N/R 表述补上方法出处

- **优先级：P3 建议；状态：OPEN，不单独阻断。**
- **分类：建议（方法定位）。**
- **受影响位置：** `plans/v00-preparation-instances.yaml` / V11-NODE-CHANGE / `known_fields.acceptance_boundary`，第 613 行。
- **问题：** 这里写“回退边界按 B0/N/R 对照与不可逆操作清单执行”，但该实例两个 `method_content_refs` 没有定义 B0/N/R。两个正文已有充分的变更档案、停止、回退与回服要求，缺的是这套名称的定位，容易让读者把另一条目的软件栈方法当成本子组已定义的完整流程。
- **证据：** 第 607–609 行仅引用 `node-drain-resource-reclamation.md` 与 `platform-change-and-rollback.md`。B0/N/R 的明确定义实际见 `environment-installation-and-upgrade.md:176–186`，不可逆边界见其第 188–210 行；平台变更正文第 157、161–165 行则用自身的预检、回服与逐层三态判据表述。
- **关闭条件：** 可补充精确方法引用并注明仅作跨域参照，或改用当前两份正文已定义的流程名称；不因此扩大平台支持范围或运行权限。

## A–E 逐维核对结果

### A. 忠实性

| 实例 | 核对结果 |
|---|---|
| V01 | 已核对、未见问题：候选核心版本/Python 范围、B0/N1/N2/N3/R0、最小矩阵乘、六类观测、七步记录与停止条件一致；未把候选核心当成可运行基线。 |
| V02 | H1–H3、四组设计、C0 的旁路隔离条件、七层记录、八步方法、MindCluster 与案例不构成官方配套的边界一致；N1 判据条件丢失见 C05。 |
| V03 | 已核对、未见问题：H1–H5、A–D 证据分层、结果检查准入、先证据后清理与配套 Test 缺口一致；未把固定 master 快照当配套发行物。 |
| V04 | N1–N5、A–E、RAS 2.24+ 与文档 2.27.5/PyTorch 2.8 的版本限定、工具与框架基线边界一致；来源 ID 错拼见 C01。 |
| V05 | E1–E6、A–F、序列化字节身份、CPU/float64 条件参考、预登记容差及 dump 治理一致；来源 ID 见 C01，通过清单见 C06。第 229 行“企业资源释放”措辞不影响其指向的设备/存储释放要求。 |
| V06-CPU | 已核对其设计概括、未见额外问题：P/F 与 H 身份分工、P0/F0/S0/PC/FC、真正 missing-FQN 前提、Linear(4,2,bias=True)、fresh target 与禁止生产 checkpoint 的边界一致；来源 ID 见 C01。 |
| V06-DCP-MULTIRANK | B/C 组名称、四观测点、夹具非生产建议、oracle 与 L2 条件性均保留；环境准备版本分工见 C04，来源 ID 见 C01。 |
| V07 | 已核对、未见转写问题：B0/V1/R0/O1、冷热分层、到达速率与并发限制、时钟/窗口和四类判读一致；通过清单见 C06。 |
| V08 | 已核对、未见问题：四层验收、真实节点档案、未支持/失败/跳过分列及不能以模板关闭实测 gap 的边界有正文依据。 |
| V09 | 已核对、未见问题：verbs/网络层与 collective 层边界、同窗计数器和单变量恢复要求有方法出处；扩展不是基础组的硬前置。 |
| V10-LOCAL-EXT4-NVME | 已核对、未见概括问题：本地文件语义、§2/§5、冷热/提交/校验与不外推其他后端一致。 |
| V10-NFS-V41 | 已核对、未见概括问题：NFS §3/§5、缓存/锁/deleg 与按后端记录的边界一致；约定字段缺失见 C02。 |
| V10-RGW-S3 | 已核对、未见概括问题：Squid 文档身份、对象语义、§2/§5 与不等同 AWS S3 的边界一致；约定字段缺失见 C02。 |
| V10-LUSTRE | 已核对、未见概括问题：滚动手册的 2.x 表述、§3/§5、MDT/OST/stripe 及独立后端结论一致；约定字段缺失见 C02。 |
| V11-SHARING-ISOLATION | 已核对、未见概括问题：共享路线、租户边界、两租户对照与 NPU 故障隔离/QoS 未证实的边界一致；通过清单见 C06。 |
| V11-NODE-CHANGE | drain、账本回收、回服及失败保留隔离的方向一致；约定字段缺失见 C02，B0/N/R 定位建议见 C07。 |
| V11-CONTROL-PLANE | 已核对、未见概括问题：K8s/Slurm 分支、恢复点与账本/应用进展边界一致；约定字段缺失见 C02。 |
| V11-SERVICE-RECOVERY | 已核对、未见概括问题：路由/重试、冷启动、发布/回退及 ready 不代替请求/质量恢复一致；约定字段缺失见 C02。 |
| V12 | 已核对、未见概括问题：PTF-01–10 是公开教学材料，案例家族/版本/时间划分、输入/答案外置、未知标签与泄漏检查有依据；通过清单见 C06。 |

除已列发现外，未见将方案预期写成实测、编造通用阈值或新增硬件兼容性结论。现场值（制品摘要、脚本输入、具体容差、资源与授权）仍作为未知保留；不将这种合法缺项本身计为错误。

### B. 完整性与结构

- **数量与归属已核对、未见问题：** 19 个唯一实例、12 个 package；`package_index` 展开与实例 ID 的多重集合完全一致，每个实例的 `package` 与索引一致。19 = 9 个单实例包 + V06 的 2 个 + V10 的 4 个 + V11 的 4 个。
- **映射已核对、未见问题：** V01–V12 的 fragment 均为 package id，可经 `package_index` 解析到该包全部实例；V06 两个实例对应前两道 phase gate，V10/V11 子组名称与 backlog 的四个 subrun 逐项一致，scheme_refs 也与 backlog 一致且内容 ID 均存在。
- **扩展处理已核对、未见问题：** backlog 第 255–256 行只在选择存储/设备扩展时要求其实际前置，第 354 行只在选择特定 collective/AMD/HCCL、路由/rail 扩展时补前置。当前不造占位实例符合条件性语义；“选定后另建实例”是对按实际子组准备原则的具体编排，不表示 backlog 原文已存在这几个字。
- **解析已核对、未见问题：** 实例、backlog、registry 均通过拒绝重复键的 YAML 解析。字段齐备与来源解析分别存在 C02、C01，不能因 YAML 可解析而忽略。

V08–V12 引用的 22 个不同方法文件均存在，下列所指章节真实存在；没有发现虚构文件或章节。表中行号为审阅时仓库源文件坐标。

| 方法文件（位于 knowledge/） | 已核对的章节定位 |
|---|---|
| `01-hardware/node-acceptance-triage.md` | 55 验收环境档案；84 步骤与判断分支；109 证据接入；133 完成判据 |
| `01-hardware/health-evidence.md` | 201 NVIDIA；269 Ascend；313 AMD；378 跨平台对照 |
| `01-hardware/resource-topology.md` | 107 拓扑字段；150 板卡到超节点；257 三方核对 |
| `03-communication/ethernet-ib-roce-rdma.md` | 48 机制；77 verbs 四分；98 分阶段错误；109 完成/持久/可见边界 |
| `03-communication/rdma-baseline-and-congestion-triage.md` | 49 前提；79 计数器；122 步骤；148 停止与恢复 |
| `03-communication/bandwidth-baselines.md` | 128 单机/多机/拓扑；144 跨节点矩阵与 rail；197 最小记录 |
| `04-data-storage/local-and-shared-storage.md` | 64 §2 本地；79 §3 NFS；105 §5 可读/重启/校验与冷热 |
| `04-data-storage/object-and-parallel-storage.md` | 47 §2 对象；62 §3 并行存储；82 §5 最小验证三层定义 |
| `04-data-storage/storage-workload-baselines.md` | 52 负载矩阵；67 完成/容量；75 计时；81 实现×工具 |
| `04-data-storage/storage-client-backend-recovery.md` | 55 故障覆盖；64 恢复步骤；81 演练判据 |
| `04-data-storage/checkpoint-integrity-evidence.md` | 56 四层校验；129 后端读路径；137 验证链 |
| `05-cluster-platform/accelerator-sharing-and-isolation.md` | 60 边界分层；75 NVIDIA 路线；150 Ascend；202 最小验证 |
| `05-cluster-platform/contention-capacity-validation.md` | 100 步骤；129 公平性；164 停止/恢复；177 完成判据 |
| `05-cluster-platform/node-drain-resource-reclamation.md` | 84 步骤；158 停止/恢复；178 验证准入；210 完成判据 |
| `05-cluster-platform/platform-change-and-rollback.md` | 67 变更档案；90 步骤；146 停止/恢复；159 完成判据 |
| `05-cluster-platform/control-plane-recovery.md` | 86 故障分支；128 备份/恢复/重建门槛；147 账本与进展 |
| `07-inference/routing-and-flow-control.md` | 45 四层职责；75 预算/背压；93 重试边界；100 有限对照 |
| `07-inference/capacity-and-autoscaling.md` | 50 触发器；63 冷启动；82 有限对照与判据 |
| `07-inference/release-and-recovery.md` | 48 发布流程；64 故障分支；74 语义边界；81 验证设计 |
| `08-reliability/diagnostic-evaluation-method.md` | 31 划分与隔离；47 角色；57 证据分级；70 评测维度 |
| `08-reliability/diagnostic-evaluation-fixtures.md` | 46 题组（PTF-01–10 均存在）；124 使用与维护规则 |
| `08-reliability/test-design-and-coverage.md` | 44 选择矩阵；67 统计纪律；85 注入/压力字段；111 七方案准备矩阵 |

### C. 缺项保留与状态纪律

- **当前值已核对、未见问题：** 19/19 为 `readiness: not_ready`、`instance_status: skeleton_prepared`。四个共同字段 `resources_available`、`authorization_scope`、`evidence_location_external`、`cleanup_recovery_owner` 在 19 个实例中全部显式为 null（共 76 个 null），未伪填资源、授权、证据库或负责人。
- **backlog 改动范围已核对、未见越界：** 移除 top-level `preparation_delivery`、恢复 V00 原 `preparation_note`、将 V01–V12 的实例引用恢复 null 后，解析对象与 HEAD 完全相等；文本 diff 也只落在这三类改动。新增说明本身的语义问题见 C03。
- **包状态与 0/7 已核对、未见问题：** V01–V12 全部 planned、`executed_at` 全 null、`evidence_refs` 全空；V00 同样 planned/null/空证据。七份 experiment 均为 `verification.status: not_verified`、证据为空，正文仍明确未执行。19 个骨架不计为任何一份方案的真实运行。

### D. 账面核对

| 交付记录的主张 | 文件实际与结论 |
|---|---|
| registry 577、无新增 | **已核对、未见问题。** registry 为 577 个唯一来源 ID，文件字节与 HEAD 相同；但“全部 source_anchors 均为既有 ID”有 C01。 |
| 内容条目 135、无变化 | **已核对、未见问题。** knowledge/ 123 个、paths/ 12 个，合计 135；两目录相对 HEAD 无差异，也没有新增未跟踪内容文件。 |
| 内容覆盖 62/1/0 不受影响 | **已核对、未见本交付引入的问题。** topic 逐项重算为 covered 54 + covered_basic 8、partial 1、missing 0；topic-coverage 文件本交付未改。该文件 summary 仍是较早快照，不能代替逐项重算，本报告不扩大审阅为历史汇总维护。 |
| 19 实例、12 包 | **已核对、未见问题。** ID 唯一，拆分与索引数量一致。 |
| V00 自身 ref 保持 null | **已核对、未见问题。** backlog 第 47 行为 null，没有为 V00 自建实例。 |
| V03 与 03.5-BLOCKED-1 同源 | **已核对、未见问题。** 实例第 143/150/163 行保留配套 Test 缺口；[BLOCKED-1 例外清单](batch-19-blocked-1-exception.md)第 7、17、23 行说明目标 CANN/HDK/机型官方交集未建立，下游不得当成已确立条件；未声称例外已关闭。 |
| 01.6 实测、08.7 真实执行、V12 独立集仍缺证据 | **已核对、未见问题。** 节点验收正文第 45/111 行保留真实档案缺口，测试方法正文第 113 行保留 0/7，评测方法正文第 43/88 行保留 V12 外置独立集边界；内容覆盖升级不等于验证缺口关闭。 |
| 必填字段齐备 | **不成立，见 C02。** YAML 可解析与 19 个 ID 一致不能证明字段齐备。 |
| make check / make build 通过 | 本轮可复跑通过，见下文；不据此补证写作轮历史命令日志，也不认为这两项检查已校验 plans/ 的实例字段和来源 ID。 |

### E. 授权边界与通过条件

**不构成执行授权、不声明资源就绪：已核对、未见问题。** 实例 notice 第 7–12 行、common_unknowns_note 第 723–727 行、backlog notice 与交付记录的“只整理，不执行”互相一致。资源/授权 null 与所有 not_ready 状态未被其他实测或就绪声明推翻。

**通过条件与 V00 验收句对齐：存在 C06，须修订。** 目前骨架的字段分面总体覆盖已知方法与现场缺项，但“最小通过集合”需明确共同门槛，不能把完整 V00 验收要求缩成某实例的三条局部清单。C03 还需恢复局部验收不等全体资源的语义。即使文档修订并通过本次编辑审阅，各实例仍维持 not_ready，直到相应现场准备真实完成且可审阅；该验收也不产生新的执行授权。

## 检查记录与定向复核要求

- `make check`：PASS，135 content entries / 577 sources。
- `make build`：在 `/private/tmp` 下的临时仓库副本执行，PASS，生成 135 条内容 / 577 来源的 catalog。副本最初未携带已有 build/catalog，预检因 first-fill-status 的两条生成物链接不存在而失败；复制本仓库已有的两份 catalog 后，以相同源文件重跑通过。使用副本是为遵守“只新增报告、不修改其他文件”；没有重写本仓库 build/。
- 自定义只读核对：拒绝重复键解析、实例/索引双向一致、scheme refs 存在且等于对应 backlog、V10/V11 subrun 同序同名、所有共同 null、planned/null/空证据与授权字段范围比较均完成；发现的来源错拼和缺键如 C01/C02，如实保留失败项。
- 本轮结束前按开始审阅时的文件摘要核对原有工作树文件，未改动交付物或其他已有文件；唯一新增仓库文件为本报告。未修改 src/kb/，不需要运行其测试套件。

常规 check/build 不检查 plans/ 内这些准备实例的字段契约或 `source_anchors` 的登记解析；它们通过不能关闭本报告的发现。复核时至少重跑 C01/C02 的全量交叉核对、C03/C05 的条件分支纸面检查、C04 的 B/C 环境对照，以及 C06 的逐实例验收覆盖核对。修订前不将任一 P2 标 CLOSED。

**最终范围结论：修订后通过；本轮尚未通过，等待上述 P2 修订与定向复核。**

## 会话元数据与核验定位

- `CODEX_SESSION_ID`：`01a1619a-8581-7290-911e-0b5afb7910bd`。
- `CODEX_THREAD_ID`：`01a1619a-8581-7290-911e-0b5afb7910bd`。
- 本轮 rollout JSONL：`/Users/ywang2397/.codex/sessions/2026/10/22/rollout-2026-10-22T11-14-39-01a1619a-8581-7290-911e-0b5afb7910bd.jsonl`。
- 已读取该文件的 `session_meta` 与 `turn_context`；审阅时第 8 行 `turn_context.payload` 为 `model: gpt-6.1-sol`、`effort: xhigh`、`cwd: /Users/ywang2397/work/AI_reliability_knowledge_base`。`session_meta` 的 originator 为 `codex_exec`、CLI 版本 `0.163.0`。本轮未派发其他审阅模型，未发生模型回退。
- 调用方可在 `~/.codex/sessions` 下按上述会话 ID 查找 rollout；若路径因归档变化，以 JSONL 内 `type == "turn_context"` 的 payload 核对 model/effort/cwd，以 `session_meta.payload.id` 交叉核对会话身份。不要用提示词中的模型名称代替实际执行元数据。
