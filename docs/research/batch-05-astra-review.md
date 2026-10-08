# 第五批独立验证审阅

审阅日期：2026-09-30。审阅者：独立 `gpt-6-astra / xhigh`。范围为 F01、F02、F04、F12、E02 五篇正文，四份第五批正式研究记录，新增 11 项来源登记，以及相应章节、平台、任务导航和计划。以下行号为初审时定位，修订后以章节及所引语句为准。

**初审结论：需要修订后定向复核。发现 0 项 P1、2 项 P2、1 项 P3。** 两项 P2 均位于 F04：MindX 不同测试的适用条件被合并，以及 exporter 的窗口计数与累计计数缺少指标族区分。未发现把源码样板拼成已验证 GPU/NPU 配套、把 catalog layer SHA 当作 manifest digest、虚构实验或将草稿标成实测结果的情况。

本次只新增本报告，没有修改正文、registry、导航或计划，没有运行 `make`、上游代码、安装、镜像、设备查询或主动测试。公开网页和固定源码通过只读工具获取；`curl` 只显示文件内容，`git ls-remote` 只核对公开 tag，未克隆仓库。主任务报告的 33 entries / 51 sources 结构检查通过属于独立结构证据，不是本审阅执行的检查，也不替代技术正确性核对。

## R1 — P2：MindX 前置条件需要保留其对应测试项

**定位：** [F04 的 MindX 主动诊断边界](../../knowledge/01-hardware/health-evidence.md)，初审第 126–128 行；[健康与配套研究记录](batch-05-health-profile-sources.md)，初审第 85–87 行。

正文写“页面记录约 20–40 GB 主机内存条件”，随后把“PRBS 有 6.0.RC2.1 起的版本条件，Atlas A2 场景另有 HDK 23.0+ 条件”放在同一句。CANN、root、IP、特权容器/虚拟机又被归为“部分项目”。这样无法判断每个条件约束哪个测试，尤其会让 PRBS 邻近的 HDK 条件被错误继承。

**精确依据：** [MindX DL 6.0.RC2 故障诊断页](https://www.hiascend.com/doc_center/source/zh/mindx-dl/60rc2/toolbox/ascenddmi/toolboxug_0020.html)的“约束与限制”“前提条件”和表 3 分别规定：

- 20–40 GB HOST 内存对应 **AICore 压测**；HDK 23.0.0+ 的 MCU/驱动/固件，以及 CANN 7.0.0+ toolkit 与配套 kernels，对应 **AICore 诊断/压测**。
- **PRBS** 的工具版本下限是 6.0.RC2.1；表 3 另列三种产品、root、物理机/特权容器等条件，并未把上述 AICore 的 HDK/CANN 条款赋给 PRBS。
- **network** 的 Host root 与 RoCE IP/检测对象 IP 条件是另一个测试的前提。页面还把普通 HBM 诊断与 HBM 压测的业务影响分开。

**影响与建议：** 这是适用条件限定不足，不是目标硬件已被证明不支持。将三条压缩摘要改成按 AICore、PRBS、network、HBM 诊断/压测分开的短表或句子；只给实际对应的项目附内存、软件、权限和业务影响条件。保留同页 PRBS 结果表的内部冲突，不自行定义 PASS/FAIL，也不由本次修订产生运行授权。同步研究记录中的同样表述。

## R2 — P2：exporter 窗口样本数、累计记录数和状态转换数需要分开

**定位：** [F04 的 exporter 计数段](../../knowledge/01-hardware/health-evidence.md)，初审第 89–91 行；[健康与配套研究记录](batch-05-health-profile-sources.md)，初审第 57 行。

“XID 和 clock-event 等指标按配置窗口统计样本记录”没有限定指标名，覆盖范围过宽。后半句虽然说明累计量会重置，却没有纠正累计 clock event 的统计对象不同，读者仍可能把事件记录、采样点和状态转换作为同一数量。

**精确依据：** [DCGM Exporter Metrics](https://docs.nvidia.com/datacenter/dcgm/latest/reference/dcgm-exporter-metrics.html)的 “Windowed sample counts” 与 “Cumulative totals” 明确分开四个指标：

| 指标 | 当前页面描述的统计对象 |
|---|---|
| `DCGM_EXP_XID_ERRORS_COUNT` | 配置窗口内的 XID 样本记录，按 `xid` 分类 |
| `DCGM_EXP_CLOCK_EVENTS_COUNT` | 配置窗口内某个 clock-event bit 为 active 的样本记录 |
| `DCGM_EXP_XID_ERRORS_TOTAL` | collector 启动后观察到的非零 XID 记录 |
| `DCGM_EXP_CLOCK_EVENTS_TOTAL` | 每个 clock event 从 inactive 到 active 的转换；初始已 active 的状态不会计为新转换 |

同页还说明：窗口族没有有效 source sample 时可产生无 `xid`/`clock_event` 标签的零值序列；累计族在首次观察前可能没有序列。累计值在 exporter 启动或 hot reload 重建 collector 后重置。

**影响与建议：** 这是现有概括超出来源支持范围的问题，不是实际采集结果未知本身造成的缺陷。至少点名 `*_COUNT` 才适用“窗口样本数、受采样节奏影响”，再单独解释两个 `*_TOTAL` 的差别及重置范围；补一句“零值、序列缺失与没有事件不能互换”，与本页的采集失败/未覆盖原则对应。原始 `DCGM_FI_DEV_XID_ERRORS` 仍是具体 XID 值，不应被当成上述派生计数。所有这些说明继续限定为本次读取的 `latest` 页面，不能外推到 DCGM v3.3.9 或未部署的 exporter 版本。

## R3 — P3：详细填充计划的首段仍显示第三批时期的当前状态

**定位：** [详细填充计划](../population-plan.md)，初审第 3 行。

首段仍称“当前共 11 篇正文……33 项来源”，并称第三批刚进入审阅；同文件第 169 行、[第五批交付记录](batch-05-source-audit.md)和 [backlog](../../plans/content-backlog.yaml)已记录前四批交付、第五批待审及 20 篇正文/51 项来源。该首段没有标为历史快照，作为计划入口会误导后续进度判断。

**建议：** 更新首段为实际集成状态，或显式标为原计划基线并另列当前状态。总览研究记录中“F12 尚未完成”可以保留作为准备阶段历史，但宜明确其时点；该记录末尾已说明 F12 集成完成，不能继续把早期准备条件当作当前缺口。无需将第五批任务提前标为 done，也无需改变正文 `draft`。

## 实际核对范围与未列为缺陷的事项

| 范围 | 本次实际核对 | 结论和限制 |
|---|---|---|
| F01 训练总览 | 全文、导航关系；Kubernetes v1.32 AllocateResponse、PyTorch 2.6 DataLoader/DCP 与 2.8 group rank 文档 | 职责依赖与非严格串行、可选 checkpoint、平台 API 不等价均有明确限定；未把保存返回当正确续训。未重新完整审查第四批并行/恢复实现 |
| F02 推理总览 | 全文、F16 和第四批审阅报告中的 R2 闭合记录 | HTTP 预处理、默认 engine arrival、frontend 接收后的 iteration 终点、三类时钟与显式 override 已同步；本次没有重复整个第四批源码调用链。图亦明确 chunk/update 不等于 token，服务入口依部署而异 |
| DCGM 固定字段 | `v3.3.9` tag 解引用为 `b0ec3c624ea21e688b0d93cf9b214ae0eeb6fe52`；实际逐行读取 fields 604–607、640–643、758–778、915–930、982–985 | 引用行号对应 replay、XID、volatile/aggregate ECC、retired/pending、NVLink FLIT total。头文件只固定字段描述；精确重置/清除和型号覆盖仍需其他证据，不能由字段存在推断支持 |
| DCGM 当前概念 | Health Monitoring、Diagnostics、Exporter Metrics 精确页面 | 被动 health、主动负载、采集状态及不以单项诊断决定 RMA 的边界得到支持；`latest` 与固定源码分开是正确的。exporter 统计对象需按 R2 修订 |
| NPU DCMI | 固定 header 的 ECC/故障事件/健康/错误/网络/订阅定义；Go 1504–1524、1567–1582、1780–1813、1955–2023、2266–2290 | 调用返回与设备值分开、网络超时、封装层 DeviceNotReady 映射均有依据。单错误码 helper 只返回首码；本页未声称它返回完整列表。未证明型号支持、码义或本地有效采样 |
| MindX 6.0.RC2 页面 | 业务影响、内存/版本/权限条件、表 3 及表 4 | PRBS 的 FAIL/PASS 与中文解释确实相反，保留冲突正确；读取失败与硬件损坏分开正确。测试条件应按 R1 拆开 |
| NVIDIA 25.01 档案 | release Contents、Driver Requirements、Announcements；NGC layer 页前 10 项可见元数据；current CUDA minor compatibility 与 Frameworks User Guide | R545 两段、Python 3.12 与 3.10 路径差异均实际存在；build id/ref、Python 构建字段符合页面。宿主/容器、上游 PyTorch tag/厂商构建、DCGM 研究参考/镜像依赖均已分开；digest、签名和制品内容仍未知 |
| Kueue | `v0.19.0` tag 解引用为 `911a822a49bcfd99c9c62203a009efa4130ad604`；固定 admission/workload/TAS 文档与 Workload API 74–83、628–642 | QuotaReserved、Admitted、PodsReady 区别，按 PodSet count 核算，Ready/可调度节点容量，required/preferred 与 Provisioning 下延迟 topology assignment 均有依据。`.status.active` 与 API `.spec.active` 的冲突记录准确 |
| Volcano / MindCluster | Volcano 1.15.0 PodGroup/Gang 两页；固定 MindCluster 芯片亲和性、节点亲和性与调度流程 | 最低成员/资源不等于全部业务进程同步；旧 Atlas、Box16、A2 例外与 A3 HiAM 分开；`self-maintain-available-card` 两路径有依据。未外推与 Kueue 或上游 Volcano 的部署配套 |
| 许可和来源登记 | 新增 11 项字段；DCGM README 182–184 与 LICENSE；Kueue LICENSE；复用 MindCluster 的已登记范围 | DCGM 源码 Apache-2.0 与二进制 SLA 分开；Kueue 仓库来源未扩张为所有站点资产许可；网页未知许可保持未知。正文为原创摘要和短字段，没有搬入厂商图或完整文档 |
| 元数据与导航 | 五篇 frontmatter、四个相关章节入口、两平台/两任务路径、backlog/source-acquisition 与 source audit | 单一主归属、稳定 ID、draft/source_checked、未验证说明一致；未把未来网站/API 或实验写成完成。进度入口首段需按 R3 同步 |

上表是限定范围的来源审阅，不是完整产品兼容审查。没有核对实际 GPU/NPU、驱动/固件、容器文件系统、调度配置、监控序列或性能结果；没有由来源冲突推导实际运行必然成功/失败。

## 定向复核入口

主任务修订后，复核 R1 的每项条件是否准确绑定测试对象，R2 是否分开 `COUNT` / 两种 `TOTAL` 及缺样本/缺序列语义，R3 是否消除当前进度冲突，并检查正文与研究记录同步。结构检查和构建由主任务执行；本报告保留初审事实，复核结论另行追加。

## 修订后定向复核（2026-09-30）

**复核结论：R1–R3 全部闭合；本次修订范围内未发现新增 P1/P2/P3 问题。第五批来源审阅通过。** 此结论覆盖初审发现和对应同步改动，不表示实际 GPU/NPU、监控、调度或软件配套已得到验证。

| 发现 | 复核结果与闭合依据 |
|---|---|
| R1 — P2 | 已闭合。F04 第 133–144 行按测试项拆表，20–40 GB 只归 AICore 压测，HDK/CANN 条款归 AICore 诊断/压测；PRBS 单列工具版本、三个产品、root 和物理机/特权容器范围，没有继承虚拟机或 AICore 软件条件。network 的 IP 前提与 HBM 诊断/压测业务影响分别记录。AICore 和 network 未展开的产品/环境范围明确指向原页表 3，没有泛化为全型号支持；研究记录第 85–88 行同步。与初审已实际读取的 MindX 同页“约束与限制”“前提条件”、表 1–3 相符。PRBS 结果表冲突及未执行授权的边界继续保留。 |
| R2 — P2 | 已闭合。F04 第 89–100 行点名四个指标族，窗口样本、非零 XID 记录和 inactive→active 转换已分开，并说明初始 active 不计新转换、缺有效样本的无分类标签零序列、首次观察前可能无累计序列，以及 exporter 启动/hot reload 重建 collector 的重置。原始 XID 码与派生计数、设备/缓存/exporter 三类生命周期保持区分；研究记录第 57 行同步。与初审已读取的 Exporter Metrics 两个对应章节相符，并保留 latest 语义不能倒推固定 v3.3.9 或未知 exporter 版本的限制。 |
| R3 — P3 | 已闭合。填充计划第 3 行更新为前四批交付、第五批处理审阅及 20 正文/13 导航的集成基线，场景草稿明确待后续分批集成，精确任务状态和生成清单另有入口；没有把并行写作文件数直接充当已集成交付数。总览研究记录保留准备阶段原文及末尾的集成后同步说明，当前 F12 状态以该说明与 backlog 为准，不再由计划首段沿用第三批状态。 |

本次回读 F04 的修订段及前后限制、健康与配套研究记录、填充计划首段、相关来源 notes、总览研究记录和 backlog 状态；以初审已逐条打开的精确外部证据定向比较，没有重复全量来源审查。仅追加本报告，未修改其他文件，未运行 `make check`、`make build` 或任何上游代码/设备测试。并行进行的 T01–T04/T07 场景及其尚待登记的来源不在本次范围。正文继续保持 `draft` / `source_checked`。
