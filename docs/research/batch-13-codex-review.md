# 第十三批审阅记录（gpt-6.1-sol / xhigh）

**修订后最终状态（2026-10-08）：** 初审 15 项发现（2 P1、11 P2、2 P3）经修订与两轮定向复核全部关闭；复核新增 3 项（B13-C16/C17/C18）同样关闭。累计 18 项全部 CLOSED，本批在原审阅范围内通过，见[定向复核记录](batch-13-codex-recheck.md)。下文初审发现与当时结论保留为历史。

审阅日期：2026-10-08。审阅者：Codex 会话，模型 gpt-6.1-sol，reasoning effort xhigh（用户当前约定）；正文编写者：Kimi（主会话），取证：探索子代理。首轮执行 60 分钟超时被外层终止，经 resume 续跑完成报告；审阅者声明基于超时前已完成的核对，未重启全部抽查。

**初审结论（历史）：暂不通过；2 项 P1、11 项 P2、2 项 P3，合计 15 项开放。**

## 审阅者声明的已完成范围

- 读取五篇正文、五份研究记录、两个领域入口、对应 backlog acceptance 与本批来源登记；检查元数据、source_refs、related_ids、内部链接与导航；make check 通过（73 项内容、116 项来源）。
- 重新取得并核对：NVIDIA SuperPOD electrical/planning 页、DGX H100/H200 与 GB200 用户指南、HPE QuickSpecs 电源部分、Redfish schema（部分字段与 Thermal 废弃标记）、HDK 26.1 A2 的温度/功耗/电压/频率/健康/降P 页、Linux v6.16 NUMA 文档、numactl/numastat、Hopper 博客与 H100 白皮书镜像部分规格、CDNA2 白皮书与 MI200 ISA 部分内容、HIP 6.3.3 异步拷贝限制。

## 审阅者声明的未覆盖项（复核时必须补取）

- hma2_01.html 附件 xlsx 中 0x80E20207、0x80E21007 原始事件定义（未取得附件）。
- CANN 8.2 架构页 0008–0012 与 API 页 0105/0106（只取得网站外壳）。
- Atlas 800T A2 用户指南 26 的 64GB、1600GB/s、HCCS 392GB/s 原始段落（B13-C12 仅依据内部矛盾，不冒充上游独立确认）。
- Supermicro 数据表数字的完整视觉核对；H100 产品页 3.35 TB/s 精确型号追溯；MI200 ISA LDS 64kB/CU 精确段落复核。
- 未执行 make build（只读环境）；无任何设备/BMC/设施/负载实验。

## 初审发现（全文照录，15 项）

### B13-C01 — P2：设备三种视图被错误写成一一对应实体
- 位置：terms-and-system-boundaries.md:54。问题："OS 设备节点、PCIe 端点、调度资源是同一实体的三种视图"过于绝对；拆分、聚合或虚拟化映射可打破一一对应。证据：NVIDIA MIG Device Names 页（同一物理 GPU 下多个 MIG Device/UUID）。关闭条件：改为显式身份映射关系，补 MIG/虚拟设备反例，与设备资源链一致；不得以 ordinal/设备节点数量推断物理端点或故障域数量。

### B13-C02 — P2：T00-01 的主归属链接与路径验收未完整交付
- 位置：terms-and-system-boundaries.md:47、57、126。问题：超节点仅注明未来 Batch 14，未提供当前主归属链接；未明确完成阅读路径可达性验收。证据：backlog T00-01 acceptance（术语逐项链接主归属、路径可达性验收）。关闭条件：为超节点建立当前可用、边界明确的定义主归属或取得验收范围调整；补充路径可达性检查记录。

### B13-C03 — P1：参数化配电公式缺少电压定义，50% 约束方向混淆
- 位置：rack-power-cooling-and-failure-domains.md:53、55。问题：`相数×U×I` 未限定 U 是相电压还是线电压，240V 示例成立于该指南特定 Wye 接法；把"每路容量能支持总峰值的 50%"写成"任一路径 ≤50% 峰值"，混淆容量下限与负载分配上限。证据：SuperPOD electrical Table 7（区分 Distribution/Line Voltage）。关闭条件：分开定义单相、三相线电压和相电压公式及接法；明确容量、正常负载、失效后负载三者；用 Table 7 至少一组 Wye、一组 Delta 数据重新核算。

### B13-C04 — P2：OEM 功率口径的内部矛盾被当成一致预算模型
- 位置：rack-power-cooling-and-failure-domains.md:47、56、63、95。问题：TDP 132kW 与 1.5×TDP≈192kW 算术不一致（直接计算 198kW），矛盾存在于 HPE 上游；"8×33kW 合计132kW"未区分装机总额定与冗余后容量（直接乘积 264kW）；"8 个只支持 N+1"缺已核对段落支持。关闭条件：保留 OEM 声明并记录矛盾未解决；分列装机/正常/冗余后/设计峰值；取得 Supermicro 精确证据及 HPE 冗余配置证据后再写保证性结论。

### B13-C05 — P2：单路供电失效被泛化为必然降性能
- 位置：rack-power-cooling-and-failure-domains.md:80、101；power-thermal-evidence.md:145。问题：单 rPDU 失效（剩 4 PSU）与三 PSU 失效（降性能条款）混用；冗余余量减少不等于已限制性能。关闭条件：区分冗余降级、容量不足、功率限制和性能下降；按明确失效数量、接线及机型描述条件。

### B13-C06 — P2：频率字段增加了未获支持的"标称"语义
- 位置：power-thermal-evidence.md:113、120、146。问题：上游将 Aicore Freq 描述为"Aicore频率"，未定义为标称/判定阈值；curFreq 低于该字段不能单独证明节流；页面示例本身同时出现利用率 0、Freq1850、curFreq800。证据：npusmi_0016。关闭条件：删除"标称"标签；频率差异写成观察项；区分空闲、负载变化、策略限制与故障事件，补同窗口负载和功率/温度证据要求。

### B13-C07 — P2：负面能力结论超出了扫描证据
- 位置：power-thermal-evidence.md:120；batch-13-training-npu-power-sources.md:28、48。问题："没有 throttle reason 等价物"需限定已核对文档范围；help 类型清单实际含 pwm-mode、pwm-duty-ratio、cpu-freq-up（类型出现不证明训练机型支持，也不证明存在 reason 位图）。证据：npusmi_0008。关闭条件：改为"在列明页面中未找到与 NVIDIA reason 位图相同的公开接口"；列出检查页面和未检查范围；修正扫描记录；另查 PWM 类型支持矩阵。

### B13-C08 — P2：降P 查询遗漏 PCIe 机型的 iBMC 限制
- 位置：power-thermal-evidence.md:120、133；batch-13-training-npu-power-sources.md:27。问题：HCCS 支持设备日志与 iBMC 两种方式，PCIe 只支持设备侧方式，iBMC 查询无效。证据：npusmi_0177。关闭条件：分列 HCCS/PCIe/卡产品及方法支持；同步修改关联表与研究记录；不把"不支持该查询"解释成"没有降P"。

### B13-C09 — P1：NUMA 成对验证使用了错误对象和错误证据
- 位置：numa-memory-and-io-locality.md:71、72、86、92、107。问题：numastat 默认是系统级页分配计数，不是目标进程驻留分布，也不是远端访问计数；other_node 差分不能证明目标进程放置成功或远端访问；numactl --show 作用于当前进程。证据：docs.kernel.org numastat 页、numastat(8) -p 选项、numactl.8 --show 语义。关闭条件：重新设计证据链：指定目标 PID/TID，分别验证允许 CPU 集、实际执行位置、进程页驻留分布和应用指标；明确每种观测不能证明什么；系统计数只作辅助背景；重写步骤 3、线程迁移分支和完成判据。

### B13-C10 — P2：first-touch 被写成无条件落点保证
- 位置：numa-memory-and-io-locality.md:48。问题：默认本地分配是"从该 CPU 节点开始分配"的倾向，允许节点、内存可用性、回退及显式策略均影响结果；"开始尝试分配"≠"最终驻留保证"。关闭条件：限定策略/允许节点/回退条件；策略意图与实际页位置核对分开。

### B13-C11 — P2：无显著差异被过度解释为排除 NUMA
- 位置：numa-memory-and-io-locality.md:87、107。问题：两组无差异只说明该负载/窗口/条件下未观察到效应，不能排除所有 NUMA 因素。关闭条件：改为限定性"本次对照未支持该候选解释"；列出重复次数、噪声/阈值、实际放置与负载稳定性要求；分别处理 CPU—内存、CPU—设备、内存—设备路径。

### B13-C12 — P2：HCCS 汇总带宽出现七倍放大
- 位置：accelerator-execution-and-data-movement.md:78、107。问题：前文"七条 HCCS 链路最大合计 392GB/s"与后表"7×392GB/s 理论"矛盾，后者再次乘七；审阅者未取得原始段落，仅确认内部矛盾。关闭条件：重新取得精确指南段落，明确每链路/每处理器合计、单向/双向口径；统一正文两处、研究记录和 registry。

### B13-C13 — P2：主机传输与设备内部搬运/同步混在同一层
- 位置：accelerator-execution-and-data-movement.md:98、105、108。问题：H2D/D2H 行纳入 cuda::memcpy_async/TMA（设备 global↔shared 搬运）；同步混入 kernel 内 PipeBarrier，未区分 host stream 完成、kernel 线程同步和内部流水依赖。关闭条件：按 host↔device、device↔device、device global↔片上存储分别列路径与 API；另列 host/stream/kernel/内部流水同步层；复核 CANN 8.2 正文后验收。

### B13-C14 — P3：精确来源定位与登记不完整
- 位置：rack-power-cooling-and-failure-domains.md:46；accelerator-execution-and-data-movement.md:59、109。问题：EAP=EPP 脚注在 planning 页而非 electrical 页；3.35 TB/s 产品口径缺近旁精确来源与登记；rocm_bandwidth_test 已进入正文但研究记录以许可未核为由不登记（许可未知应记录为未知而非省略）。关闭条件：修正 EAP 来源页；补齐 3.35 TB/s 对应型号/版本及近旁引用；登记 ROCm 仓库并明确 revision 或观察日期；同步研究记录和 registry。

### B13-C15 — P3：numa_balancing 被误写成三个互斥取值
- 位置：numa-memory-and-io-locality.md:73。问题：该字段是可按位组合的控制值（0/1/2 及组合 3），仅列互斥取值会把 3 误判为错误。证据：v6.16 sysctl/kernel.rst L701–L725（各标志可 OR 组合）。关闭条件：改为位掩码语义并解释 0/1/2/3；同步研究记录与 registry。

## 无发现项（审阅者声明）

元数据结构、ID 唯一性、内部链接及 related_ids 存在性；32 项新增来源与 2 项更新的登记数量；draft 与硬件验证边界（未把文档声明写成实测）；Thermal 废弃及 schema≠设备实现的边界声明（已核对部分）。

## 关闭要求（审阅者）

先修订 P1 及 P2 发现，同步正文、研究记录和 registry；再针对修改点复核，并补取未覆盖的精确上游证据（xlsx 事件、CANN 8.2 页、Atlas 指南 26 HCCS 段、Supermicro/HPE 精确口径、3.35 TB/s 型号）。
