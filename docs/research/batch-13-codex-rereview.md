# Batch 13 当前修订稿独立只读技术审阅报告

后续状态（2026-10-09）：原 `gpt-6.1-sol / xhigh` 会话完成修订后的两轮只读定向复核，R01–R05 及修订新增 R06 均 CLOSED，在补充审阅及定向修订范围内通过，见[复核汇总](batch-13-codex-rerecheck.md)与[修订记录](batch-13-rereview-revisions.md)。下文保持 2026-10-08 初始审阅原貌，包括当时 OPEN 状态、位置、指纹和执行声明；历史措辞不代表后续稿状态。

## 1. 审阅声明与结论

- **日期：**2026-10-08。
- **角色：**本次独立技术审阅者，不是正文编写者。
- **模型与 reasoning effort：**按用户提供的当前会话配置记录为 `gpt-6.1-sol / xhigh`。本次未切换模型、未另派模型、未生成子代理；工具未返回可另行验证的底层模型身份，因此此项属于会话配置记录，而非运行时身份认证。
- **授权与执行边界：**用户明确授权本次审阅。只读取仓库材料、查询远程来源并运行 `make check`；未修改仓库文件、未提交、未读取凭据、未执行硬件、集群、供电、绑定或负载实验；未运行 `make build`。
- **独立性：**先完成正文、研究记录与上游证据核查，形成本次发现，再读取两份历史审阅报告。历史通过状态不作为本次通过依据。

**本次结论：暂不通过，部分来源证据受限。**

本次有 **5 项开放发现：P1 0 项、P2 3 项、P3 2 项**。其中三项 P2 分别涉及训练 NPU 实时降频观测能力、NUMA 策略与线程证据语义、DCGM 被动健康规则的解释范围。均须修订并完成定向复核后才能关闭，本次没有自行宣称任何新发现已解决。

无法独立取得的来源没有被直接判为技术错误；已明确记录且未用于保证性结论的未知，也没有被泛化为新增阻塞项。

## 2. 精确输入范围

审阅对象是工作区中的当前文件，不是仅依据某个已提交版本。仓库存在预先已有的修改及未跟踪文件；本次没有整理、覆盖或提交这些文件。

### 完整读取的正文与研究记录

| 任务 | 正文及读取范围 | 完整读取的研究记录 |
|---|---|---|
| T00-01 | `knowledge/00-overview/terms-and-system-boundaries.md`，第 1–163 行 | `docs/research/batch-13-terms-sources.md` |
| T01-01 | `knowledge/01-hardware/rack-power-cooling-and-failure-domains.md`，第 1–130 行 | `docs/research/batch-13-rack-power-sources.md` |
| T01-02 | `knowledge/01-hardware/power-thermal-evidence.md`，第 1–159 行，包括本批 NPU 修订及既有技术主张 | `docs/research/batch-13-training-npu-power-sources.md` |
| T01-03 | `knowledge/01-hardware/numa-memory-and-io-locality.md`，第 1–121 行 | `docs/research/batch-13-numa-locality-sources.md` |
| T01-04 | `knowledge/01-hardware/accelerator-execution-and-data-movement.md`，第 1–152 行 | `docs/research/batch-13-accelerator-execution-sources.md` |

另读取：

- `AGENTS.md`、`README.md`、`docs/authoring-guide.md`、`content-outline.md`。
- `docs/research/batch-13-source-audit.md`。
- `plans/full-coverage-backlog.yaml` 中上述五项任务的 acceptance。
- `sources/registry.yaml`、`schemas/content.schema.json`。
- `knowledge/00-overview/index.md`、`knowledge/01-hardware/index.md`及相关导航、主归属与内部引用。
- 为追溯既有功热内容，读取相关 batch 10 来源记录。
- 独立核查完成后读取 `docs/research/batch-13-codex-review.md`、`docs/research/batch-13-codex-recheck.md`。

### 审阅结束时的正文指纹

以下为 SHA-256，用于主执行者确认报告对应的输入；不表示仓库处于干净状态。

| 正文 | SHA-256 |
|---|---|
| `terms-and-system-boundaries.md` | `c2351009ea34f56384ffa1e7042c66a48ad4487d38ab6a42c0c40ce57898b067` |
| `rack-power-cooling-and-failure-domains.md` | `f122792e4f7f25d859c842e241a49d5a103e1064727a0130eb2401de1b53c372` |
| `power-thermal-evidence.md` | `ed5f689e6bfa0c1c148c108b761482e52881f875709194398b35df6a6a61605d` |
| `numa-memory-and-io-locality.md` | `ee7fc3c7aaab637b27dc561ca61599666273d68be16f837b39556dd1a8260754` |
| `accelerator-execution-and-data-movement.md` | `242bdbaf8d0d3d9eaa929b45ea7ef0f309a5ac08a61420307f1584902a80bf14` |

## 3. 本次可行动发现

### B13-R01 — P2：NPU 负面能力结论仍有范围泄漏，遗漏同版本官方 DCMI 降频原因位图

**状态：OPEN。**

**位置：**

- `knowledge/01-hardware/power-thermal-evidence.md:120`：限定 npu-smi 页面范围后，又概括实时侧没有单一判定字段。
- `knowledge/01-hardware/power-thermal-evidence.md:148`：训练线 NPU 的能力总结未交代 DCMI 路径。
- 关联记录：`docs/research/batch-13-training-npu-power-sources.md:28`、`docs/research/batch-13-training-npu-power-sources.md:48`，仍出现“只能”间接观测及未限定的“无 throttle reason 等价物”。

**触发主张与核查结果：**

没有发现 npu-smi reason 位图接口，不能推出同一训练产品线不存在公开的实时原因接口。本次独立取得 **HDK 26.1.x、A2 DCMI** 官方页面，确认存在：

- `dcmi_get_device_info` 的 `DCMI_MAIN_CMD_LP`；
- 子命令 `DCMI_LP_SUB_CMD_AICORE_FREQREDUC_CAUSE`；
- 8 字节、64 位降频原因位图；
- 每 100 ms 更新，不能查询历史原因；
- 表 2 区分 `IDLE`、`THERMAL`、`SW_EDP`、`HW_EDP`、`POWER_BREAK`、`SVFD`、`POWERCAPPING`；
- 表 3 明列 Atlas 800T A2、Atlas 900 A2 PoD 的部署场景支持情况。

**精确证据：**

[HDK 26.1.x A2 DCMI：DCMI_MAIN_CMD_LP，约束说明、表 1–3](https://www.hiascend.com/doc_center/source/zh/HDK/2610/A2/A2DCMI/dcmi_077.html)。

其原文语义是：存在可读取**当前 AI Core 降频原因**的公开接口，同时限定更新周期、历史查询能力及部署场景。它不是 NVIDIA 字段的逐位等价替代，也不是健康事件历史。

**影响：**

读者可能错误地认为训练 NPU 只能通过频率差、健康事件和日志间接观测，遗漏直接原因采集路径；也会使后续设施—设备—应用关联设计建立在不完整的能力清单上。

**建议：**

保留“在列明 npu-smi 页面中未找到”的限定结论，另列 DCMI 接口、支持矩阵与限制。明确空闲原因不等于故障节流，不能把任意置位直接解释成供电或散热故障。同步修订研究记录中的“只能”“无等价物”，补充来源登记与近旁引用；不推断本地已安装版本必然支持。

**关闭条件：**

正文、研究记录与 registry 一致区分 npu-smi、DCMI、健康事件及 exporter 四条证据路径；定向复核上述官方表格、版本和部署限制。无需执行设备查询。

**与旧发现关系：**

这是 **B13-C07 范围限定修订的残留缺口，并有本次新增上游证据**。不撤销 B13-C06 已删除“标称”误释的修订；旧编号及历史 CLOSED 状态保留，本次问题以 B13-R01 跟踪。

---

### B13-R02 — P2：NUMA 允许集仍被用于确认内存策略意图，主线程证据不能代表全部工作线程

**状态：OPEN。**

**位置：**

- `knowledge/01-hardware/numa-memory-and-io-locality.md:71`。
- `knowledge/01-hardware/numa-memory-and-io-locality.md:88`。
- `knowledge/01-hardware/numa-memory-and-io-locality.md:110`。

**触发主张：**

正文把 `/proc/<pid>/status` 的 `Cpus_allowed_list`、`Mems_allowed_list`归入“进程允许集与绑定意图”，用于“确认策略意图”；测量步骤主要围绕目标 PID 采集允许集。

**精确证据与原文语义：**

1. [Linux v6.16 NUMA memory policy，固定 commit，Memory policies 与 Task/Process Policy](https://github.com/torvalds/linux/blob/038d61fd642278bab63ee8ef722c50d10ab01e8f/Documentation/admin-guide/mm/numa_memory_policy.rst#L15-L69)：cpuset 是行政允许范围，不能与内存策略混同；多线程进程的 task policy 只作用于安装策略的线程及其之后创建的线程，已存在的兄弟线程保留原策略。
2. [同 revision 的 `/proc/status` 实现](https://github.com/torvalds/linux/blob/038d61fd642278bab63ee8ef722c50d10ab01e8f/fs/proc/array.c)：状态输出针对传入的 task，调用 task CPU 允许集及 cpuset 状态输出。
3. [同 revision 的 cpuset 文档](https://github.com/torvalds/linux/blob/038d61fd642278bab63ee8ef722c50d10ab01e8f/Documentation/admin-guide/cgroup-v1/cpusets.rst)：cpuset 限制与进程内存绑定策略相互作用，但不是同一个策略对象。

`Mems_allowed_list`不能证明已经安装了 `MPOL_BIND`、interleave 或某个 VMA 策略。读取主线程的 CPU 允许集，也不能证明所有训练线程、通信线程和独立 loader 进程具有同样的 affinity。

**影响：**

可能把“允许从 X、Y 分配”误认为“已经绑定到 Y”，或把主线程绑定当成全部工作线程绑定。即使后续有页驻留快照，仍不能据此确认策略安装对象及线程覆盖范围。

**建议：**

分别记录：

- cpuset/任务允许范围；
- 关键 TID 的 CPU affinity；
- 已安装的 task/VMA 内存策略及其作用域；
- 实际页驻留；
- 应用指标。

说明 `numa_maps` 的策略标签与节点页数提供不同证据；目标进程语境内的策略查询与外部主线程状态查询不能混用。关键子进程应单独列 PID，不由父进程状态代替。将 task stat 的处理器字段称为最近执行处理器采样，而非连续实时位置证明。

**关闭条件：**

表格、步骤和完成判据不再把允许集当作已安装内存策略的证明；明确 PID/TID/子进程覆盖范围，并通过固定上游语义定向复核。无需绑定或负载实验。

**与旧发现关系：**

属于 **B13-C09 证据链重写后的进一步缺口**。系统级 numastat 与目标进程驻留已分开，B13-C16 的 MB/页单位修订也成立；这些历史修订不因本条而被抹去。

---

### B13-R03 — P2：DCGM 被动 watch 被过度概括为“只看 violation 增量”

**状态：OPEN。**

**位置：**

- `knowledge/01-hardware/power-thermal-evidence.md:87`。
- `knowledge/01-hardware/power-thermal-evidence.md:144`。

**触发主张：**

正文称电源 watch 与热 watch 同理，并总结“被动 watch 只看 violation 增量”。

**精确证据：**

[DCGM v3.3.9 固定源码 `DcgmHealthWatch.cpp`，`MonitorThermal`、`MonitorPower`、CPU thermal 路径](https://github.com/NVIDIA/DCGM/blob/b0ec3c624ea21e688b0d93cf9b214ae0eeb6fe52/modules/health/DcgmHealthWatch.cpp)。

本次独立读取固定实现，确认：

- GPU thermal 路径检查 thermal violation 差值；
- GPU power 路径除 power violation 差值外，还检查 `DCGM_FI_DEV_POWER_USAGE` 的不可读状态，并可产生 `DCGM_FR_POWER_UNREADABLE`；
- 同文件还有 CPU 温度阈值相关的被动监测路径。

因此，“被动”指不启动专用测试负载，不等于所有规则都只读取 violation 计数器。

**影响：**

可能把电源 watch 的 WARN 一律解释为发生过功率节流，忽略功率遥测不可读；也可能把 GPU thermal 分支的实现外推至整个健康监测模块。

**建议：**

把结论限定为“该版本 GPU thermal violation 分支”；分别说明 GPU power 的 violation 与遥测不可读分支。健康结果解释必须读取具体 incident/error code，不能只凭 WARN 或 watch 名称归因。保留“Healthy 不证明供电散热无问题”的边界。

**关闭条件：**

第 87、144 行及对应来源记录与固定实现一致；定向复核 `MonitorPower` 的不可读分支和规则作用对象。无需运行 DCGM 或诊断负载。

**与旧发现关系：**

无直接对应的 B13-C01–C18 条目。这是本次对既有功热内容的新增发现。

---

### B13-R04 — P3：Redfish PSU 风扇字段清单遗漏当前数组字段及废弃边界

**状态：OPEN。**

**位置：**

`knowledge/01-hardware/rack-power-cooling-and-failure-domains.md:81`。

**触发主张：**

`PowerSupplyMetrics v1.3.0` 的观察字段只列 `FanSpeedPercent`，未交代 `FanSpeedsPercent`。

**精确证据：**

[DMTF `PowerSupplyMetrics.v1_3_0.json`，`FanSpeedPercent`与`FanSpeedsPercent`定义](https://redfish.dmtf.org/schemas/v1/PowerSupplyMetrics.v1_3_0.json)。

该精确 schema 明确：

- 单数字段 `FanSpeedPercent` 自 v1.1.0 废弃；
- 采用 `FanSpeedsPercent` 数组支持 PSU 内多个风扇。

**影响：**

按该清单设计采集时，可能只查旧字段而遗漏多风扇数组。旧字段仍出现在 schema 中，并不意味着它是该版本推荐的唯一读取入口。

**建议：**

列出 `FanSpeedsPercent`，将 `FanSpeedPercent`标为兼容旧字段；继续保持“schema 有字段不证明设备实现”的声明，并区分缺失、null 与有效读数。

**关闭条件：**

字段表与固定 schema 一致，研究记录同步标明废弃版本及数组结构；不得假定任何设备一定实现新字段。

**与旧发现关系：**

无直接对应旧条目。既有 Thermal 废弃提示不能代替这个独立字段的生命周期核查。

---

### B13-R05 — P3：梯度检查点主张引用的固定章节实际为空白占位页

**状态：OPEN。**

**位置：**

`knowledge/00-overview/terms-and-system-boundaries.md:149`。

关联记录为 `docs/research/batch-13-terms-sources.md` 的 checkpoint 同名异义证据行。

**触发主张：**

正文以 AIInfra 固定 commit 的 `04Train/03TrainAcceler/08Checkpoint.md`，支持“gradient checkpointing 是重算省显存技术，不写盘”。

**精确证据与原文语义：**

1. [AIInfra 固定 commit 的 `08Checkpoint.md`](https://github.com/Infrasys-AI/AIInfra/blob/b97c0385ba07a62a717d82a0e7aed2927f12fc35/04Train/03TrainAcceler/08Checkpoint.md)：本次独立取得的文件只有标题、未完成提示和占位内容，没有支持该技术解释的正文。
2. [PyTorch 2.6 `torch.utils.checkpoint`](https://docs.pytorch.org/docs/2.6/checkpoint.html)：直接说明 activation checkpointing 通过反向传播期间重算中间激活，以计算换取内存。

**影响：**

技术区分本身有官方依据，但当前引用不能支撑它；仅核对章节名称或仓库目录，会把未完成内容误当成已核验技术来源。

**建议：**

用 PyTorch 2.6 的实际机制文档替换该技术引用，写成“activation checkpointing 本身不是持久化训练检查点”。AIInfra 可继续作为内容组织参考，但不能承担这条实质主张的证明责任。

**关闭条件：**

正文近旁引用、研究记录和来源登记指向实际支持该主张的页面；定向复核不再以空白章节标题代替正文证据。

**与旧发现关系：**

无直接对应旧条目；不是对历史 B13-C14 所列其他引用修订的重复发现。

## 4. 逐篇来源核查范围

“独立取得”只表示本次取得并读取了所列页面、表格或源码片段，不代表整套手册逐页审计，也不代表设备验证。

### 4.1 术语与系统边界

**已独立重新取得并检查：**

- [PyTorch 2.6 DataLoader](https://docs.pytorch.org/docs/2.6/data.html) 的 worker process 语义。
- [Kubernetes CRI](https://kubernetes.io/docs/concepts/architecture/cri/) 页面及其官方重定向。
- [NVIDIA MIG Device Names](https://docs.nvidia.com/datacenter/tesla/mig-user-guide/mig-device-names.html) 的逻辑设备身份反例。
- CUDA 12.8 官方 PDF 的运行时及执行模型相关内容。
- AIInfra 指定 checkpoint 文件的固定 revision；stas00 指定 revision 的 accelerator README 部分内容。
- PyTorch 2.6 activation checkpointing 机制，见 B13-R05。

**仅编写者记录支持、未在本次完成完整原文复核：**

两本资料的全部章节归属、逐文件许可范围，以及术语表中其余平台状态、elastic 恢复与排障方法的全部近旁证据。

**未取得或未完成：**

未取得可用于本次完整复核的 Volcano v1.15.0 PodGroup 正文及 PyTorch elastic 相关目标页；未把这些页面的引用存在性当作语义确认。

### 4.2 机柜供电、散热与共享依赖

**已独立重新取得并检查：**

- [SuperPOD planning](https://docs.nvidia.com/dgx-superpod/design-guides/dgx-superpod-data-center-design-h100/latest/planning.html)：EAP/EPP、组件功耗、密度与气流相关内容。
- [SuperPOD electrical](https://docs.nvidia.com/dgx-superpod/design-guides/dgx-superpod-data-center-design-h100/latest/electrical.html)：Table 7、50% 两种约束及存活 PSU 条件。
- [DGX H100/H200 指南](https://docs.nvidia.com/dgx/dgxh100-user-guide/introduction-to-dgxh100.html) 的 PSU、工作温度、气流与降性能条款。
- NVIDIA GB200 官方指南硬件部分；[HPE QuickSpecs V6](https://www.hpe.com/us/en/collaterals/collateral.a50009224enw.html) 的 Power Delivery 内容。
- [Supermicro 原始 PDF](https://www.supermicro.com/datasheet/datasheet_SuperCluster_GB200_NVL72.pdf)：取得两页 PDF，相关数字表所在第 2 页完成文本及截图核对。
- Redfish 的 PowerSubsystem、PowerSupplyMetrics、EnvironmentMetrics、CoolingUnit、CoolantConnector、LeakDetector 精确版本 schema，以及 Thermal 废弃相关内容。

**仅编写者摘录支持：**

Atlas 800T A2 产品页所列整机供电、风扇与环境规格，本次未取得相应规格段落；不能以取得产品网页外壳代替核验。

**未取得或未解决：**

- Delta 208 V、60 A 行的 32.8 kW 与正文线电流公式的口径关系，仍未从上游页面推出。
- HPE 的 132 kW、1.5 倍与 approximately 192 kW，以及 Supermicro 的 8×33 kW、total 132 kW，原文歧义确实存在；本次没有替 OEM 解释或给出容量保证。
- 未验证任何现场冗余接线、冷却能力或 Redfish 实现。

### 4.3 供电、散热与性能证据

**已独立重新取得并检查：**

- DCGM v3.3.9 固定字段及健康实现相关片段。
- DCGM 当前官方 exporter 指标、health monitoring 页面；COUNT 样本计数、TOTAL 跳变及重启重置语义。
- nvidia-smi 官方手册相关内容、DGX H100/H200 规格。
- [SuperBench 原论文 §2.1，印刷页 837](https://www.usenix.org/system/files/atc24-xiong.pdf#page=4)：环境差异及缺陷 IB 链路观察，不外推为通用阈值。
- MindCluster v26.1.1 固定 `collector_for_npu.go` 的温度、功耗、电压、当前频率及健康指标定义。
- HDK 26.1.x A2 npu-smi 的 `0012、0016、0023、0025、0027、0029、0030、0039、0008、0177` 所述相关字段、支持矩阵或约束。
- 本次新增取得的 A2 DCMI `dcmi_077`，见 B13-R01。

**仅编写者摘录支持：**

- 健康故障定义 XLSX 的 0x80E20207、0x80E21007、关联事件及“最近 8 次”说明。
- 未重新取得的 memory、降P设置/复位及 A3 相关目标页的细节。
- exporter 全采集组默认配置及全仓库负面能力扫描，不由本次局部源码阅读重新确认。

**未取得：**

健康故障定义 XLSX 原始附件。本次没有重扫 `npusmi_0002–0181` 全部存在页，因此不继承编写者全页扫描的覆盖声明。

### 4.4 NUMA、内存与 I/O 局部性

**已独立重新取得并检查：**

- Linux v6.16 固定 NUMA memory policy 文档、sysctl NUMA balancing 文档、PCI NUMA ABI，以及相关 proc/cpuset 实现和文档片段。
- numactl 官方仓库的 `numactl.8`、`numastat.8`。这不能替代对研究记录所称 man7 特定快照身份的确认。
- hwloc 官方文档中的工具与 I/O 拓扑说明。
- [AMD 58012 Rev.1.5](https://docs.amd.com/api/khub/documents/ScFqtjHuoA5CBw6e~hb01Q/content) 的 NUMA topology、网卡本地资源与调优相关段落。

**仅编写者摘录支持：**

Lameter、Gaud 文章中的具体示例数值，以及 Atlas 用户指南的 CPU 配置。

**未取得或未完成：**

两篇 CACM 原文未取得可复核正文；Atlas 指南未取得。没有执行拓扑查询、策略查询、绑定或成对性能测量。

### 4.5 加速器执行与数据移动

**已独立重新取得并检查：**

- [CUDA 12.8 官方 PDF](https://docs.nvidia.com/cuda/archive/12.8.0/pdf/CUDA_C_Programming_Guide.pdf) 的执行模型、page-locked、传输重叠、stream 与同步相关内容；Hopper 官方博客及 H100 产品相关规格。
- [AMD CDNA2 白皮书](https://www.amd.com/content/dam/amd/en/documents/instinct-business-docs/white-papers/amd-cdna2-white-paper.pdf) 的 GCD、L2、HBM 与互联相关内容。
- [MI200 ISA](https://www.amd.com/content/dam/amd/en/documents/instinct-tech-docs/instruction-set-architectures/instinct-mi200-cdna2-instruction-set-architecture.pdf) 的 wavefront、SALU/VALU、EXEC、LDS 64 kB/32 bank 精确段落。
- [HIP 6.3.3 memory API](https://rocm.docs.amd.com/projects/HIP/en/docs-6.3.3/doxygen/html/group___memory.html) 的非 pinned 同步退化、HCC 注记及 peer access/host staging 条件。
- ROCm bandwidth test 固定 revision README 的 RBT-NG 实现说明。
- CANN 8.2 的独立队列/同步及 SPMD 相关页面；ACL `0105` 的同步复制、kind 与 peer 条件；ascend-dmi bandwidth 官方页面。

**仅编写者摘录支持：**

CANN `0010` 存储单元表、`0106` 异步复制细节，以及 Atlas 指南 HCCS、64 GB、1600 GB/s 规格段落。

**未取得或未完成：**

HC34 deck 的目标数字页、上述 Ascend 原文；未逐项复核 CUDA sample 源码、全部工具许可或 RBT 弃用声明文件。第三方 H100 白皮书镜像没有被当作独立官方原件。

## 5. 指定受限来源的补取结果

| 指定来源 | 本次结果 | 可使用的证据强度 |
|---|---|---|
| `hma2_01.xlsx`：0x80E20207、0x80E21007 | 未取得附件字节、工作表或原始行；官方入口及替代获取失败后停止 | 仅编写者解析记录支持，不能写成本次独立核验 |
| CANN 架构 `0010` | 只取得导航/外壳，未取得目标表正文 | 六类 buffer 描述仍为编写者摘录支持 |
| ACL `0105` | 已取得官方正文及相关支持/约束内容 | 本次独立取得 |
| ACL `0106` | 未取得目标正文 | 64 B 对齐、Host 分配及 EP/RC 细节仍为编写者摘录支持 |
| Atlas 用户指南 HCCS | 未取得目标规格段落 | 392 GB/s 合计口径只确认了正文内部一致性，没有冒充原文核验 |
| Supermicro PDF | 已取得；第 2 页相关规格表完成文本及视觉核对 | 原始表列数字已独立复核；容量歧义仍未解决 |

同一受限来源在连续两种方式失败后，没有继续反复尝试。没有用猜测的附件直链、网站标题、搜索片段或编写者重复声明代替原始证据。

## 6. 验收、元数据与导航判断

| 验收项 | 本次判断 |
|---|---|
| T00-01 | 主归属、当前超节点定义落点、同名异义及领域图结构已交付；R05 引用缺口待修订 |
| T01-01 | 参数化预算、OEM 口径差异、冷却与失效域边界已交付；R04 待修订；未解决容量口径不能由本报告升级为设计保证 |
| T01-02 | 主要训练 npu-smi 字段及逐命令限制有重新取得的证据；R01、R03 待修订；XLSX 事件机制仍非本次独立确认 |
| T01-03 | 系统计数/目标驻留、MB/页、首次分配及不预设局部更快等修订保留；R02 的策略与线程对象语义待修订 |
| T01-04 | 主机传输、设备内部搬运及同步层次已分开；CUDA/HIP 与部分 CANN 证据已取得；关键 Ascend 表格和规格仍证据受限，不能宣称本次全部独立核验通过 |

未发现本批元数据结构、稳定 ID、内部链接存在性或两个知识域入口的新增结构问题。五篇仍为 `draft / source_checked`，没有 `reproduced`；procedure 的环境缺失及未执行实验边界仍需保留。

这里的 `source_checked`只能按记录的核对主体和来源范围解释，不能转换为“本次审阅者已独立取得所有来源”，更不能转换为硬件兼容性或实验验证通过。

## 7. 历史编号与本次关系

两份历史报告记载 **B13-C01–B13-C18 全部 CLOSED**。本报告保留这些历史编号和状态，不重新编号、不替代原报告，也不以其 CLOSED 状态作为本次通过依据。

| 历史编号 | 历史最终状态 | 本次处理 |
|---|---|---|
| B13-C01、C02 | CLOSED | 设备映射反例及当前定义主归属修订保留 |
| B13-C03、C04、C05 | CLOSED | 接法、两个 50% 条件、OEM 歧义及失效情景区分保留；未解决口径不扩大保证 |
| B13-C06 | CLOSED | 删除“标称”及空闲干扰说明保留 |
| B13-C07 | CLOSED | 本次发现范围限定仍有残留，并取得新 DCMI 证据，以 R01 跟踪 |
| B13-C08 | CLOSED | HCCS/PCIe 查询边界的已取得部分保留；未取得页不冒充复核 |
| B13-C09、C16 | CLOSED | 系统/进程对象与单位修订保留；策略及线程覆盖缺口以 R02 跟踪 |
| B13-C10、C11 | CLOSED | first-touch 非保证及“未支持而非排除”修订保留 |
| B13-C12 | CLOSED | 七倍放大已从当前正文消除；原始 HCCS 规格本次仍未取得 |
| B13-C13 | CLOSED | 路径/同步分层及 Host 分配前提已写入；0106 原文仍受限 |
| B13-C14、C15 | CLOSED | 引用定位、登记及 balancing 位掩码修订保留 |
| B13-C17、C18 | CLOSED | 时钟偏差与已完成重写的措辞修订保留；不由作者记录替代全部上游复核 |

本次新增问题使用 **B13-R01–B13-R05**，均为 OPEN；不新增 B13-C19。

## 8. 实际执行检查

执行命令：

```text
PYTHONDONTWRITEBYTECODE=1 make check
```

实际结果：

```text
PASS: 73 content entries; 119 sources.
Checked structure and local file links; not technical correctness or remote links.
```

`make check` 实际通过。macOS 的 make/xcrun 临时缓存写入被只读环境拒绝，产生警告；未影响检查器返回的 PASS，不作为技术验证结果。

**未执行：**

- `make build`、`make test`、lint 或格式化。
- GPU/NPU、BMC、设施、集群查询与诊断。
- 电源失效、散热、绑定、NUMA 成对负载或数据移动实验。
- 仓库写入、提交、报告文件保存。

## 9. 关闭与后续复核要求

主执行者应先修订 **R01–R03** 的能力及证据语义，再同步 **R04–R05** 的字段和引用；同步更新相关正文、研究记录及需要调整的来源登记。

定向复核必须检查修改后的实际文本与本报告列出的精确来源，不能仅接受“已按建议修改”的声明。无法取得的 XLSX、CANN 或 Atlas 原文，可以继续作为明确的证据限制保留，但不能改写成本次已独立确认。

**最终状态：暂不通过，部分来源证据受限；5 项新发现仍开放。历史 18 项 CLOSED 记录保留，本报告不替代历史报告。**

## 10. 本会话报告交付与来源登记

主执行者于 2026-10-08 保存此报告；审阅者的只读执行与本节的报告集成分别记录。实际 CLI 审阅配置为 `gpt-6.1-sol`、`model_reasoning_effort=xhigh`、`sandbox=read-only`；会话 ID 为 `01a11c1a-4fb4-7f73-a0a3-d97e5f379dff`。审阅进程正常结束，返回码 0。

主执行者逐条核对了五项发现的对应正文位置与支持来源，并确认上列五份正文 SHA-256 与审阅启动、报告交付时一致。补充的原始源码定位：

- R02：[cpuset.c L4395–L4402](https://github.com/torvalds/linux/blob/038d61fd642278bab63ee8ef722c50d10ab01e8f/kernel/cgroup/cpuset.c#L4395-L4402) 输出 task 的 mems_allowed；不是 task/VMA 内存策略查询。
- R03：[DcgmHealthWatch.cpp L1629–L1639](https://github.com/NVIDIA/DCGM/blob/b0ec3c624ea21e688b0d93cf9b214ae0eeb6fe52/modules/health/DcgmHealthWatch.cpp#L1629-L1639) 是 GPU 功耗不可读 WARN 的分支。行号按固定 commit 原始文件核对。

新增来源登记见 [registry](../../sources/registry.yaml)：

| 本次证据 | 来源 ID | 用途 |
|---|---|---|
| HDK 26.1.x A2 DCMI LP | `src.huawei.hdk-26.1x-a2-dcmi-low-power-2026-10-08` | R01 当前降频原因位图及支持限制 |
| Linux v6.16 proc/cpuset | `src.kernel.proc-cpuset-v6.16` | R02 允许集与策略、线程对象的区分 |
| PyTorch 2.6 activation checkpointing | `src.pytorch.activation-checkpoint-2.6` | R05 的实际机制支持页 |

R03 复用 `src.nvidia.dcgm-v3.3.9`；R04 复用 `src.dmtf.redfish-schemas-v1-2026.2`；AIInfra 空白章节使用已登记的固定 revision。登记新证据不关闭发现，也不修改五篇正文的审核或验证状态。

本会话交付的修改限于本报告、来源登记和 [交付记录](batch-13-source-audit.md) 的当前审阅状态；正文、五份编写者研究记录及 B13-C01–C18 历史报告保留。

保存报告和补登来源后，主执行者实际运行：

```text
make check
PASS: 73 content entries; 122 sources.
make build
PASS: 73 content entries; 122 sources.
Built build/catalog.json and build/catalog.md.
```

两项命令返回码均为 0；`git diff --check` 通过。只确认结构、本地链接及清单生成；B13-R01–R05 仍全部 OPEN，本次未执行真实环境验证。
