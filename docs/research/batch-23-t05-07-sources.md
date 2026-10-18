# 第二十三批 T05-07 来源记录

任务：T05-07（多租户争用、公平性与容量验证，procedure 类新文章的知识材料）。取证轮次：作者侧首轮（2026-10-18）。原计划的只读取证子代理因账户周配额（403）未执行，本记录由主会话作者角色直接取证。取证方式全部为 FetchURL 只读；未部署 Kueue/Slurm、未提交任务、未运行任何负载。

版本声明：

- Kueue：固定 commit `911a822a49bcfd99c9c62203a009efa4130ad604`（v0.19.0）。本轮实开 `site/content/en/docs/concepts/fair_sharing.md` 与 `site/content/en/docs/concepts/admission_fair_sharing.md`。
- Slurm：固定 24.11.7 归档（`https://slurm.schedmd.com/archive/slurm-24.11.7/`），本轮实开 `sshare.html`（man2html 生成时间 2025-11-11 GMT）；`priority_multifactor.html` 与 `slurm.conf.html` 复用既有登记范围。
- NVIDIA：MIG User Guide 与 MPS 文档为可变页（2026-10-18 观察），device-plugin 为固定 commit `487d7a93...`（v0.20.1）。

## 主张—来源定位表（ID—精确页面/节—字段/支持范围）

| 主张 | 登记 ID | 精确页面/节 | 支持范围 / 未覆盖 |
|---|---|---|---|
| Kueue 的准入公平共享机制 | NEW src.kueue.fair-sharing-v0.19.0 | [admission_fair_sharing.md@911a822a](https://github.com/kubernetes-sigs/kueue/blob/911a822a49bcfd99c9c62203a009efa4130ad604/site/content/en/docs/concepts/admission_fair_sharing.md) 全页 | AdmissionFairSharing 为 beta、默认启用（v0.15+）；按 LocalQueue 历史用量排序，低用量优先；用量按 `usageHalfLifeTime` 衰减、按 `usageSamplingInterval` 采样；`resourceWeights` 表示资源类型相对权重；入口罚分（Entry Penalty，v0.13.0+）在准入时立即计入用量，防止瞬时大量提交绕过统计；ClusterQueue 以 `admissionScope.admissionMode: UsageBasedAdmissionFairSharing` 启用；LocalQueue `fairSharing.weight` 默认 1；观测入口 `status.fairSharing`（consumedResources/lastUpdate/weightedShare）。未覆盖：默认参数数值、站点实测 |
| Kueue 抢占式公平共享的边界 | NEW src.kueue.fair-sharing-v0.19.0 | [fair_sharing.md@911a822a](https://github.com/kubernetes-sigs/kueue/blob/911a822a49bcfd99c9c62203a009efa4130ad604/site/content/en/docs/concepts/fair_sharing.md) 全页 | 以 Dominant Resource Share（DRS）论证不同 ClusterQueue 的两个工作负载不会互相循环抢占；分层（Hierarchical）情形仍缺证明（页面自述 Limitations）；该页链接的 strategy.go 指向另一 commit，引用时不得当作本 commit 的实现证据 |
| Slurm 公平份额的字段与观测口径 | NEW src.slurm.sshare-24.11.7 | [sshare.html](https://slurm.schedmd.com/archive/slurm-24.11.7/sshare.html)（DESCRIPTION/SSHARE OUTPUT FIELDS/FAIR_TREE MODIFICATIONS/PERFORMANCE 节） | 仅在 priority/multifactor 插件下可用；数据经 slurmdbd 由 slurmctld 读取；字段含 Raw Shares/Norm Shares/Raw Usage/Norm Usage/Effectv Usage/FairShare/GrpTRESMins/GrpTRESRaw/TRESRunMins；FAIR_TREE 默认下 Level FS = Norm Shares / Effectv Usage（<1 过服务、>1 欠服务、无用量为 infinity）；sshare 对 slurmctld 发 RPC，禁止循环高频调用。未覆盖：站点权重与 decay 配置 |
| Slurm 多因子优先级中的公平份额位置 | 复用 src.slurm.docs-24.11.7 | 既有登记：priority_multifactor.html（评估序与九因子）、slurm.conf.html（PriorityDecayHalfLife/PriorityFlags 等） | 支撑「FairShare 只是多因子之一，等待时间/QOS/TRES 等因素共同决定优先级」；本轮未重开 |
| 队列配额、借用与抢占的账本字段 | 复用 src.kueue.cluster-queue-v0.19.0＋src.kueue.admission-v0.19.0＋src.kueue.job-lifecycle-v0.19.0 | 既有登记：ClusterQueue flavor/borrow/lending/preemption/fungibility、两阶段准入、clusterqueue flavorsReservation/flavorsUsage、metrics 与 evicted reason | 支撑「容量由配额+借用+抢占+flavor 共同决定，总卡数/利用率不能单独表示可用容量」；本轮未重开 |
| 设备共享不提供完整隔离（官方限制案例） | 复用 src.nvidia.k8s-device-plugin-v0.20.1（README 共享节）＋src.nvidia.mps-docs-2026-10-18 | device-plugin README：time-slicing 无显存/故障隔离、replicas 不保证比例算力；MPS when-to-use：单用户活动 server、错误遏制有限、提前终止未定义 | 构成验收要求的「官方共享/隔离限制」案例，只陈述语义限制，不编造性能数字；性能影响须由两租户对照实测回答 |
| MIG 的容量碎片与实例上限 | 复用 src.nvidia.mig-user-guide-2026-10-18 | concepts.html（profile placement 与 fragmentation、最大实例数 7/4/2） | 支撑「剩余卡数不等于可满足形状；容量记录须含拓扑/碎片与实例规格」 |
| 存储负载口径 | 复用 src.mlcommons.storage-rules-v2.0 | 既有登记：负载定义、缓存条件、吞吐/时延指标 | 支撑「存储争用须绑定负载、缓存状态与并发条件」；本轮未重开 |
| Ascend 设备账本与健康 | 复用 src.ascend.mind-cluster-v26.1.1＋src.ascend.ascend-device-plugin-44385c13 | 既有登记：Register/ListAndWatch/Allocate；组件 README 的虚拟设备上报与健康由物理设备决定 | 支撑「NPU 侧可观测到设备与虚拟设备分配，但无共享隔离保证」 |
| Ascend 静态/动态 vNPU 的资源与分配边界 | 复用 src.ascend.virtual-instance-hdk-44385c13 | [HDK 特性说明@44385c13](https://github.com/Ascend/mind-cluster/blob/44385c13d7b1d87def35f1604e8be4d16de6ca4e/docs/zh/scheduling/04_usage/02_virtual_instance/00_virtual_instance_with_hdk/01_description.md)（产品支持/资源组成/约束）；[动态 vNPU 调度](https://github.com/Ascend/mind-cluster/blob/44385c13d7b1d87def35f1604e8be4d16de6ca4e/docs/zh/scheduling/04_usage/02_virtual_instance/00_virtual_instance_with_hdk/05_dynamic_vnpu_scheduling/01_dynamic_vnpu_scheduling_inference.md) | 支撑「静态/动态 vNPU 有模板化资源组成与分配约束」；不支持故障隔离/QoS 保证；具体争用与公平性未测 |
| Ascend vCANN-RT 软切分 | 复用 src.ascend.virtual-instance-vcann-44385c13 | [vCANN-RT 特性说明@44385c13](https://github.com/Ascend/mind-cluster/blob/44385c13d7b1d87def35f1604e8be4d16de6ca4e/docs/zh/scheduling/04_usage/02_virtual_instance/01_virtual_instance_with_vcann_rt/00_description.md) | 支撑「vCANN-RT 为时分复用、仅推理、requests 为 AICore 百分比」；跨容器隔离/开销未证实 |

## unknown 清单

1. Kueue AdmissionFairSharing 的默认 `usageHalfLifeTime`/`usageSamplingInterval` 数值：页面未列，须读安装默认配置。
2. Kueue 公平性指标在 v0.19.0 的完整清单：`observability/metrics` 页本轮 404（路径未定位），仅由 admission_fair_sharing 的 `status.fairSharing` 与既有 clusterqueue metrics 证据支撑。
3. Slurm 公平份额的站点实际权重、`PriorityDecayHalfLife`、QOS 系数：unknown，须读现场配置。
4. NVIDIA 共享模式的真实性能/争用数据：官方文档只给语义限制，无公开基准数字；不得以「预计」冒充案例结果。
5. Ascend NPU 共享/虚拟化下的争用与公平性证据：已有 HDK 静态/动态 vNPU 与 vCANN-RT 的资源切分、模板与分配约束文档，但无跨 vNPU 故障隔离/QoS 保证，也无争用/公平性实测；不得从 GPU 机制类推。
6. 两租户对照的全部实测：未部署、未运行、未采集；正文只能给方法与预计结果/实际结果分栏。

## 建议登记条目

```yaml
- id: src.kueue.fair-sharing-v0.19.0
  title: Kueue v0.19.0 公平共享文档（Fair Sharing 与 Admission Fair Sharing）
  url: https://github.com/kubernetes-sigs/kueue/blob/911a822a49bcfd99c9c62203a009efa4130ad604/site/content/en/docs/concepts/admission_fair_sharing.md
  kind: repository
  registered_at: '2026-10-18'
  revision: commit 911a822a49bcfd99c9c62203a009efa4130ad604（v0.19.0）；2026-10-18 经 FetchURL 实开同 commit 的 fair_sharing.md 与 admission_fair_sharing.md
  license:
    status: partial
    scopes:
    - scope: 固定仓库自有文档源码；第三方文件及独立站点资产另计
      identifier: Apache-2.0
      url: https://github.com/kubernetes-sigs/kueue/blob/911a822a49bcfd99c9c62203a009efa4130ad604/LICENSE
    notes: 沿用 src.kueue.admission-v0.19.0 已核对的根许可口径；只链接并原创归纳，未复制示例配置或代码。
  notes: Batch 23（T05-07）取证：admission_fair_sharing（beta/默认开、历史用量排序与衰减、Entry Penalty、resourceWeights、ClusterQueue admissionScope、LocalQueue weight、status.FairSharing 观测）；fair_sharing（DRS 防循环抢占论证与分层情形 Limitations；页内链接指向另一 commit，不作为本 commit 实现证据）。未覆盖：默认参数数值、完整指标清单。
- id: src.slurm.sshare-24.11.7
  title: Slurm 24.11.7 sshare 命令参考（归档）
  url: https://slurm.schedmd.com/archive/slurm-24.11.7/sshare.html
  kind: documentation
  registered_at: '2026-10-18'
  revision: 24.11.7 archive（man2html 生成时间 2025-11-11 GMT）；2026-10-18 经 FetchURL 只读
  license:
    status: unknown
    scopes: []
    notes: SchedMD 站点许可未核对；只链接并原创归纳，未复制手册长段。
  notes: Batch 23（T05-07）取证：仅 priority/multifactor 下可用；数据经 slurmdbd；输出字段（Raw/Norm Shares、Raw/Norm Usage、Effectv Usage、FairShare、GrpTRESMins、GrpTRESRaw、TRESRunMins）；FAIR_TREE 默认语义（Norm Shares 按层、Effectv Usage 相对父级、Level FS=Norm/Effectv、无用量为 infinity）；PERFORMANCE 节的 RPC/循环调用告警。未执行 sshare。
```
