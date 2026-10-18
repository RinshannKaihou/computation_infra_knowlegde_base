# Batch 23 · T05-07 定向复核（Codex）

## 1. 审阅元数据

| 项 | 记录 |
|---|---|
| 任务 / 轮次 | T05-07「多租户争用、公平性与容量验证」；承接上一轮独立审阅角色，对 C01–C07 定向复核并检查修订的新增问题 |
| 初审依据 | [初审报告](batch-23-t05-07-codex-review.md)；按其逐项关闭条件核验，而非只按作者的修订说明核验 |
| 实际模型 / effort | **`unknown / unknown`**。本轮接口未提供可核验的实际模型及推理档位元数据；不以仓库约定或上轮的 `gpt-6.1-sol / xhigh` 记录推定本轮配置，不更改历史记录 |
| 执行方式 | 当前 Codex CLI 会话直接复核；未派发子代理，未另行启动或路由其他模型 |
| 日期 / 时区 | 2026-10-18，Asia/Shanghai（UTC+08:00） |
| 写入权限 | 只创建本报告；正文、来源登记、计划和仓库 `build/` 均不修改 |
| 取证方式 | 重读正文、初审报告、作者来源记录及相关登记；重新取得 Kueue 固定 commit、Slurm 24.11.7 release 对应仓库文档源文件、NVIDIA 官方文档；另核对扩展的 Ascend 论断 |
| 实验边界 | 未连接集群、提交任务、修改准入/配额、重配设备或终止客户端；文档复核不是硬件、兼容性或安全验证 |

主审文件：[正文](../../knowledge/05-cluster-platform/contention-capacity-validation.md)，下文简称 **P**；位置均为本轮读取的原文件行号，P 共 195 行。另读 [README](../../README.md)、[编写指南](../authoring-guide.md)、[领域边界](../../content-outline.md)、[schema](../../schemas/content.schema.json)、[T05-07 计划](../../plans/full-coverage-backlog.yaml)、[作者来源记录](batch-23-t05-07-sources.md)和[来源登记](../../sources/registry.yaml)。邻文[共享与隔离机制](../../knowledge/05-cluster-platform/accelerator-sharing-and-isolation.md)只用于追溯入口，不替代上游材料。

输入快照 SHA-256：

| 文件 | SHA-256 |
|---|---|
| P | `0e42033283ee0e9a2db1de740046b8deed2508ce30a1a67e011ce199e0719f9c` |
| 初审报告 | `033341e4e985d5c79c10b35123b635df76c9e4dc54d6a86d78e82d2aa4fa281e` |
| 作者来源记录 | `a613060cf3466938a51472c2b8a37b8cd4371ea5d034859e91e5739feed9a047` |
| 来源登记 | `c2f1fad836ddfa72105f54f028d6a094d0bc9107c9a36bc7bbbfefdd61bf4b25` |
| T05-07 所在计划 | `581c9079b9c864f3877e615290fe8116a3fe60667c7256336e244c8c14f62de9` |

初审正文的历史哈希是 `13bb10da07528b8d2305baf7aec40a0c7d27bc75eef56cd0d6900ae39158b451`，与本轮不同；本轮实际重读了修订正文。没有取得旧正文的完整可重放快照，故不声称完成了逐字版本差异审计。

## 2. 逐项复核表

**CLOSED 表示原发现的文档关闭条件已满足，不表示设计已在现场执行。OPEN 保留原 ID 和 P2，不把未完成部分换号为新增发现。** E01–E10 的实际重开位置与版本见第 5 节。

| 初审 ID / 级别 | 判定 | 本轮正文证据位置及核验结果 | 尚缺内容 / 关闭要求 |
|---|---|---|---|
| **B23-T07-C01 / P2** | **CLOSED** | P L151、L155–160，尤其 L159：预计表已限于**不同 GI**，写明同 GI 的 CI 共享显存/引擎，以及主机、PCIe、网络、存储和整卡/驱动故障仍可能共同影响。正文 L151 只是引述 GPU 内机制对照表，不再由此推出端到端零干扰；L181 也不作全场景保证。与 E09 的 GI/CI 和 Table 3 边界相符 | 原「分区内互不影响」已删除；原问题关闭。实际 GI/profile 及跨层干扰仍待环境验证 |
| **B23-T07-C02 / P2** | **CLOSED** | P L104–105 要求基线自身差异落在预登记噪声带内才推进；超出则固定条件、补重复或停止。L178 同样要求基线稳定，并把并发变化和基线噪声分开。步骤和完成判据方向一致 | 不要求作者编造噪声数值或实际重复结果；原推进条件错误已关闭 |
| **B23-T07-C03 / P2** | **CLOSED** | P L106 新增 B-alone；可比设计须登记相同有效工作单位、目标份额和资源请求，异构设计改用各自基线归一化退化/SLO，禁止异构 step/请求直接求份额。L107 确认应用负载实际重叠；L178–179 要求异构 B 基线可重复，并把可比性设为份额比较条件 | 按初审允许的“可比设计或异构归一化设计”二选一关闭，不把括注“异构负载必需”误读为异构 B 可跳过。此判定不认可任意两种请求天然可比 |
| **B23-T07-C04 / P2** | **OPEN** | P L121 已正确补充目标 CQ 的 admissionMode、同 CQ 多 LQ 的 AFS、跨 CQ 的 cohort/借用/抢占区分及历史字段完整路径，并明确 `weightedShare` 不是历史量；E01–E03 支持。L123、L180 已要求历史状态与映射；L125 已列 Slurm PriorityType/Fair Tree、association、QOS、计费和 decay | 仍缺**可审查的初态/轮次控制方法**，以及 Slurm 有效优先级权重、真实 A/B association 归属与计费口径的检查分支。仅记录历史状态或在完成清单声称“已控制”不等于控制顺序效应；详见 2.1 |
| **B23-T07-C05 / P2** | **OPEN** | P L108 已按控制层分类，要求每轮单变量、实际并发/设备身份/资源形状，切换模式/profile 重建基线；L108、L182 正确把总并发下降的改善标为策略权衡 | 仍未给出所选控制的**生效证据与失效分支**。控制层名称列表不能替代“改变什么、何时作用于哪些对象、怎么核实确已生效”；E04、E07–E09 支持区分；详见 2.2 |
| **B23-T07-C06 / P2** | **OPEN** | P L82 新增统一时钟、提交/开始/就绪/稳态/结束、run/attempt 及实际映射；L107 要求真实负载重叠。L181 已容纳候选边界、未观察到显著退化、证据不足三类结论，且否认候选直接等于根因 | 仍未预登记采样分辨率/时钟误差和各层变化判据；且 L107 把“无可检出退化”与“证据不足排序”合并记 unknown，与 L181 的区分不一致；详见 2.3 |
| **B23-T07-C07 / P2** | **CLOSED** | P L109 去掉无条件可逆，改按已登记安全退出路径释放 B，列出 server/client 状态证据，禁止未同步终止；不能安全退出即停止。L171–173 补充同步退出、FAULT/疑似受影响时禁止直接终止、按文档安全路径恢复，不得为释放 B 破坏 A，故障轮与正常释放轮分开。与 E08 的提前终止及错误遏制约束相符 | 原缺失的安全护栏已补齐。不是给任意版本的强杀/复位授权，也不是认证所有 MPS 恢复路线均可逆 |

### 2.1 C04：已解释机制，但试验门槛仍未闭合

- **已完成部分不再争议：** L121 的 AFS 范围、CQ 显式启用和字段解释正确；L123 不允许清零生产账本也正确。这里不是因为没有现场配置或默认值而维持 OPEN。
- **初态控制仍是陈述，不是方法：** L123 要求记录，L180 声称初态已控制，但没有说明各轮如何建立可比较历史，或如何把先 A 后 B 的用量/衰减差异纳入预期。至少选择一种可审查方案，例如在获授权的隔离测试对象上设置匹配的预置历史、采用交换顺序的配对轮次并记录每轮初态，或明确按各轮历史预测准入顺序、不能等初态比较时不判策略公平性。记录不等于必须把所有历史清零。
- **Slurm 还需有效策略检查：** E05 限定 `sshare` 依赖 `priority/multifactor`；E06 的公平因子有独立 `PriorityWeightFairshare`，还受到其他有效因子影响。P L125 只列 PriorityType/Fair Tree 和 QOS，没有要求核验这些权重及其实际贡献；启用 multifactor 不足以证明 fair-share 对排序有作用。应列 A/B 作业的真实 cluster/account/user/partition association、shares 层级和 QOS，核实实际 `TRESBillingWeights`，未配置时明确是 CPU-seconds 而非 GPU 物理服务量，并保留历史/decay 的解释。
- **关闭条件：** 把上述有效配置、映射及初态控制落实为并发前的门槛；缺项时限制为资源/SLO 观察，不据等待差异判该公平策略。无需现在填入虚构的现场值。

### 2.2 C05：单变量约束已补，强制控制的观测仍缺失

- **已完成部分不再争议：** 不再把准入配额直接等同于运行期隔离，也已明确模式/profile 变化要重建基线及减少并发的权衡。
- **剩余缺口：** L79 记录共享模式，L108 记录并发/身份和形状，但没有要求提供所选限制实际执行的证据。保存参数、上报 replica 数或发现两个任务变成串行，不能证明运行中的客户端受到预期资源上限约束。E04 的准入账本和 E07 的访问名额，与 E08 的运行期资源限额作用不同；E08 还说明 uniform active-thread 限额在客户端启动时确定，并非修改配置就改变现存客户端。
- **关闭条件：** 对本轮选中的控制路线写清“参数/对象 → 生效时机与支持条件 → 实际生效证据 → 不满足时停止或降级”。可分别用准入条件与实际重叠量、MPS 对应版本的有效客户端限额、MIG 实际 GI/profile 归属、主机/网络/存储所选控制的有效状态作证；无可用观测则不得作该层隔离因果结论。保留现有单变量、重新基线及并发下降不等于隔离的约束，不要求补出通用部署命令。

### 2.3 C06：时间线已补，排序的分辨能力与结果分类仍需一致

- **已完成部分不再争议：** 统一时间线、身份和实际重叠已出现；完成判据也不再强制找出某个根因。
- **剩余缺口：** 统一时钟不自动解决指标采样间隔、聚合窗口及时间戳误差；P 未要求登记这些信息，也未把各层的相对基线异常阈值/持续时间纳入判定。两个变化落在同一可分辨窗口时仍不能排序。此要求是对试验设计的内部核验，不是假称上游规定了统一统计阈值。
- **分类矛盾：** L107 的“无可检出退化或证据不足以排序时记 unknown”混合了不同证据质量。充分观测下未发现显著退化，与采集缺失/分辨率不足不能排序，应按 L181 分开；前者仍须限定负载、窗口和检测能力，不能等价于零干扰。
- **关闭条件：** 预登记共同分析窗口、采样与时间误差、各层相对基线变化判据；超出时序分辨能力时记并列候选或证据不足。同步修改步骤 L107 与完成判据 L181，使三类结果一致，并继续要求干预/恢复支持因果解释。

## 3. 新增发现

### B23-T07-R01 · P3 / OPEN：扩展的 Ascend 机制论断没有接入本篇来源链

- **位置：** P L8–21、L160、L188–195；[来源登记](../../sources/registry.yaml)中的 `src.ascend.virtual-instance-hdk-44385c13` 和 `src.ascend.virtual-instance-vcann-44385c13`。
- **现象：** 当前预计表具体区分静态/动态 vNPU 与 vCANN-RT 时分复用，但该行及本篇来源记录没有指向支持这些区分的精确文档；两个已登记的专项来源也未进入 P 的 `source_refs`。原有组件 README 的设备上报/健康说明不能替代这些机制依据，邻文已经引用它们也不等于本篇完成引用。
- **独立核验：** 本轮重新打开同 commit 的 HDK、vCANN-RT 特性说明（E10），确认这些概括有一手支持；因此这是**可追溯性缺口，不是把论断判成错误，也不是新发现了 NPU 故障隔离保证**。本轮新增发现编号不表示已取得精确引入提交；旧正文完整快照缺失的限制见第 1 节。
- **影响：** 本篇读者及按来源依赖追踪的工具无法从这条新增/扩展的预计直接回溯相应固定版本依据；也不易区分“切分与分配条件已有资料”与“跨实例故障隔离/QoS 未证实”。
- **可关闭条件：** 在 L160 附近链接同 commit 的精确 HDK/vCANN-RT 说明并加入这两个既有 source ID，或删除本篇未接入证据的具体扩展论断、保持未知。继续保留“未执行”和故障隔离/QoS 未证实；不必重复登记已存在的来源，不得把机制资料提升成 Kueue/Slurm 与 Ascend 组合已验证。

除 R01 外，本轮未确认其他需要单独编号的新增问题。C04–C06 是初审关闭条件仍有剩余，不重复计为 R02–R04。

## 4. 结论

**定向复核未通过：原 7 项中 4 项 CLOSED、3 项 OPEN；新增 1 项 P3 OPEN。**

- CLOSED：**C01、C02、C03、C07**。
- OPEN：**C04、C05、C06**，均保留 **P2**；新增 **B23-T07-R01 / P3**。
- 修订已解决 MIG 无条件零干扰、基线推进方向、B 参照/异构比较和 MPS 安全退出护栏；尚不能把本篇标为审阅通过。
- 下一轮应按第 2 节剩余关闭条件及 R01 核验，不要求为关闭文档发现而编造基准结果。P 的 `draft / not_verified`、空环境与验证证据引用应继续保持；模型审阅不替代实验验证。

## 5. 证据边界

### 5.1 本轮实际重开的关键上游

GitHub 材料由连接器重新返回固定 ref 的原文及 blob SHA，不是转抄作者说明。位置以文件/节/结构名表示；不把网页工具转换后的行号拼成 GitHub 原文件行号。

| 编号 | 固定版本 / 实开位置 | 本轮支持的结论与边界 |
|---|---|---|
| E01 | Kueue `911a822a49bcfd99c9c62203a009efa4130ad604` 的 [Admission Fair Sharing](https://github.com/kubernetes-sigs/kueue/blob/911a822a49bcfd99c9c62203a009efa4130ad604/site/content/en/docs/concepts/admission_fair_sharing.md)，How it works、Entry Penalty、Configuration、Observability；blob `8ca78993495b26cca7a48efff6d63992dc524693` | 同 CQ 的 LQ 历史准入排序、显式 admissionMode、衰减与权重、示例输出；未把 `168h`/`5m` 示例视为现场值或默认值 |
| E02 | 同 commit 的 [localqueue_types.go](https://github.com/kubernetes-sigs/kueue/blob/911a822a49bcfd99c9c62203a009efa4130ad604/apis/kueue/v1beta2/localqueue_types.go)，`LocalQueueSpec`、`LocalQueueFairSharingStatus`、`LocalQueueAdmissionFairSharingStatus`；blob `8de00fbd6bd55b3dcf8351fbdd56538ddd4a325e` | CQ 归属、嵌套历史字段与 `weightedShare` 注释。只确认 API 文本，不把存在字段当作现场采样正常或已填充证明 |
| E03 | 同 commit 的 [Fair Sharing](https://github.com/kubernetes-sigs/kueue/blob/911a822a49bcfd99c9c62203a009efa4130ad604/site/content/en/docs/concepts/fair_sharing.md)，两类机制及 Limitations；blob `271692c069b94bac09071213f1cb7330be5069ef` | AFS 与基于抢占的公平不是同一机制；未用该页指向另一 commit 的实现链接替代当前版本证据 |
| E04 | 同 commit 的 [Admission](https://github.com/kubernetes-sigs/kueue/blob/911a822a49bcfd99c9c62203a009efa4130ad604/site/content/en/docs/concepts/admission.md)，blob `c2f4d205902d0f24a37838f3b0921156ca2e4b98`；[ClusterQueue](https://github.com/kubernetes-sigs/kueue/blob/911a822a49bcfd99c9c62203a009efa4130ad604/site/content/en/docs/concepts/cluster_queue.md)，原文件 L330–455，blob `cf9eba2047b0e62280a92d01c2d0b5da04385f7d` | 配额预留、准入检查、借用/借出与抢占；它们不是 GPU、网络或存储运行期带宽隔离证明 |
| E05 | Slurm [release tag 对象](https://api.github.com/repos/SchedMD/slurm/git/tags/9d1ef1877186d8101769352831c8f0fe303df31c)确认 `slurm-24-11-7-1` 指向 `defaf214db2e55326f45ab08f1bde5b2036d9f5d`；该 commit 的 [sshare.1](https://github.com/SchedMD/slurm/blob/defaf214db2e55326f45ab08f1bde5b2036d9f5d/doc/man/man1/sshare.1)，原文件 L1–240；blob `5f44c4d87dc31aadaf21cf89adfce0a52e9f28b3` | multifactor 依赖、Raw Usage 计费回退、Fair Tree/Level FS、RPC 调用风险。没有执行 `sshare`，也不提供轮询脚本 |
| E06 | 同 Slurm commit 的 [priority_multifactor.shtml](https://github.com/SchedMD/slurm/blob/defaf214db2e55326f45ab08f1bde5b2036d9f5d/doc/html/priority_multifactor.shtml)，原文件 L1–195、L230–410，重点 General、Fair-share Factor、Configuration；blob `3f4d5ce47f7d4e1ca55efa756a1b64a14fc8e8ef` | 多因子权重、Fair Tree、计费与历史衰减；用于核验 24.11.7 的文档语义，不是完整调度器实现审计或站点有效配置证据 |
| E07 | NVIDIA 插件固定 commit `487d7a93894b0f3ad08097169593972eb3ca8206` 的 [README](https://github.com/NVIDIA/k8s-device-plugin/blob/487d7a93894b0f3ad08097169593972eb3ca8206/README.md)，原文件 L350–385、L470–590；blob `44594d4343967a313ff268223c8f638de005062c` | 访问名额、time-slicing/MPS 互斥和节点级范围、插件 MPS experimental/MIG 限制及资源上限；未据此认证固定插件与当前 MPS 文档的组合 |
| E08 | NVIDIA [When to Use MPS](https://docs.nvidia.com/deploy/mps/when-to-use-mps.html)，System/Application Considerations、Memory Protection and Error Containment、Dynamic Execution Resource Provisioning、Client Early Termination；2026-10-18 重开 | 未同步终止的危害、FAULT 后恢复条件、启动时确定的限额，以及区分 Legacy v2/v3 的安全客户端终止路径。是可变官方文档，不是绑定现场 CUDA/驱动的操作授权 |
| E09 | NVIDIA [MIG Concepts](https://docs.nvidia.com/datacenter/tesla/mig-user-guide/concepts.html)，GI/CI、Profile Placement、Table 3；2026-10-18 重开，页面显示更新于 2026-10-13 | GI/CI 共享边界与 GPU 内机制比较，足以否定原无条件互不影响；不证明主机、网络、存储隔离或现场支持组合 |
| E10 | Ascend `44385c13d7b1d87def35f1604e8be4d16de6ca4e` 的 [HDK 特性说明](https://github.com/Ascend/mind-cluster/blob/44385c13d7b1d87def35f1604e8be4d16de6ca4e/docs/zh/scheduling/04_usage/02_virtual_instance/00_virtual_instance_with_hdk/01_description.md)（原理、使用说明/约束），blob `09228039a611477372ffcaa432a8a921e5233edf`；[vCANN-RT 特性说明](https://github.com/Ascend/mind-cluster/blob/44385c13d7b1d87def35f1604e8be4d16de6ca4e/docs/zh/scheduling/04_usage/02_virtual_instance/01_virtual_instance_with_vcann_rt/00_description.md)（时分复用、原理、使用约束），blob `0e467cec4a97ee9d09f321a416d2942d02f0a309` | 支持 P L160 的机制概括并支撑 R01 的来源补齐建议；未确认跨 vNPU 故障隔离/QoS，也未认证 Kueue/Slurm 的 NPU 接入 |

### 5.2 访问缺口与未验证范围

- **Slurm 精确归档仍未取得正文：** 本轮重新请求 `https://slurm.schedmd.com/archive/slurm-24.11.7/sshare.html` 和 `https://slurm.schedmd.com/archive/slurm-24.11.7/priority_multifactor.html`，网页接口均返回不可访问；不是已确认的 HTTP 404。E05–E06 是核过 release tag 的同版本仓库文档源文件，不能声称与缺失的归档 HTML 逐字相同，也未独立核实归档 man2html 页脚日期。
- Kueue 三个 raw URL 首次通过网页接口读取返回 Cache miss，随后通过 GitHub 连接器取得精确 commit 原文及 blob；没有用搜索片段、最新文档或作者笔记替代固定版本材料。
- 未核对全部默认化实现、控制器算法或完整平台支持矩阵；本轮未重新审计 MLCommons Storage、其他 Ascend 组件、驱动/固件兼容性与许可证。固定提交和 blob 只识别读取的材料，不等于网页快照已归档。
- 无现场配置、历史账本、测量时间线、重复分布、SLO 数字或干预/恢复结果；本报告的 CLOSED 只覆盖文档修订。正文保留 `draft / not_verified` 与未执行结果是恰当的。

### 5.3 本地检查与写入范围

- 本报告落盘后执行 `PYTHONDONTWRITEBYTECODE=1 make check`：**PASS，100 content entries / 469 sources**。在包含原有本地链接目标的临时镜像执行 `make build`（使用仓库既有 Python 环境、禁止写入 bytecode）：**PASS，100 / 469**；生成物只写临时镜像，未改写仓库 `build/`。这些检查只验证结构与本地链接，不验证远程材料或技术正确性。
- 16:56 的输入复验确认第 1 节五份材料哈希均未变化；当时对报告落盘前的全部已登记工作区文件逐项 SHA-256 复验也全部一致。本审阅工具的仓库写操作只针对本报告。
- **并行变更说明：** 16:57 末次校验期间检测到 `knowledge/05-cluster-platform/platform-change-and-rollback.md` 哈希变化，工作区另出现 T05-06、T05-09 的复核报告；本轮未写入、回滚或借用其结论。第 1 节五份主审材料此时仍与输入哈希一致。工作区不是原子快照，隔离构建结果只代表所复制的输入。
- 未修改 `src/kb/`，不新增测试或运行硬件测试。工作区开始时已有其他未提交/未跟踪材料；不回滚或整理它们。
