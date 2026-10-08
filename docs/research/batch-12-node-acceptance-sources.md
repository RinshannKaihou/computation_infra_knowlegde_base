# 第十二批来源记录：新节点与返修节点验收（R2-14）

**2026-10-08 修订注记：** Codex `gpt-6.1-sol / xhigh` 按 B12-C01/C02 修正本记录并完成[定向复核](batch-10-11-12-codex-recheck.md)。下述原研究者、首次获取方式与当时任务状态为历史；修订补读和保留的未知条件见本记录及复核报告。

研究日期：2026-10-08。研究者：探索子代理（非 astra）。目标正文：`knowledge/01-hardware/node-acceptance-triage.md`（procedure，planned，验收标准见 plans/round-02-backlog.yaml R2-14）。范围：DCGM 主动诊断级别与前提、SuperBench 主动验证方法与判据、昇腾 ascend-dmi 能力、DGX 规格核对点、NVIDIA GPU Node Triage 候选来源结构。未执行任何设备命令、诊断或基准测试；除本文件外未改动仓库其他文件（registry/plans/knowledge 均未动）。

## 主张—证据表（DCGM 主动诊断）

| 主张 | 来源与定位 | 版本/环境 | 证据性质 | 反例/未知 |
|---|---|---|---|---|
| dcgmi diag 四个预置级别覆盖递增（高级别含低级别全部测试）：r1=software；r2 加 pcie、memory、memory_bandwidth；r3 加 diagnostic、targeted_stress、targeted_power、nvbandwidth、nccl_tests；r4 加 memtest、pulse（表中名称） | https://docs.nvidia.com/datacenter/dcgm/latest/user-guide/dcgm-diagnostics.html "Run Levels and Tests" 表（2026-10-08 观察；该 user-guide 形态页未单独登记，与已登记 learn 形态页同属 DCGM latest 文档） | latest（可变）；表头注明 "measured on Hopper GPU systems" | 官方文档原文表 | learn 形态页的测试选择指南未列 nccl_tests、sm_stress，而含 context_create；两页清单不一致（见冲突节） |
| 典型耗时量级（官方表头）：r1 <2.5 秒；r2 4 卡 <2.5 分钟 / 8 卡 <10.5 分钟；r3 4 卡 <10 分钟 / 8 卡 <35 分钟；r4 4 卡 <45 分钟 / 8 卡 <2.25 小时 | 同上表头 | Hopper GPU 系统实测口径 | 官方文档原文 | 其他 GPU 数/型号耗时未给；triage 页称 long(r3) "approximately 30 minutes"，与 8 卡 <35 分钟口径一致 |
| 级别语义定位：Level 1 作 readiness metric；Level 2 作失败后的 epilogue；Level 3/4 由管理员作 post-mortem。learn 页对应表述：收工前快速就绪检查、失败作业后中等级别、隔离疑似故障时选单项、返修回服前管理员级长测 | user-guide 页 "DCGM Diagnostic Goals" 第 3 条；learn 页 "When diagnostics are useful"（2026-10-08） | latest | 官方文档原文 | — |
| targeted 测试目的：targeted_power=持续功率负载（默认目标 TDP-1 W，达到 target_power 的 75% 才判过）；targeted_stress=受控 GEMM 维持目标 GFLOPS（默认达成 95% 判过），监控温度/PCIe replay/SBE；pulse_test=快速电流/功率脉冲击穿供电不稳（默认按 SKU 遍历 pattern，Hopper 0–22）；memory=显存分配/读写/数据完整性/ECC/L1 cache（默认分配 75% 显存，5 种 pattern）；diagnostic=持续矩阵乘+显存遍历，监控 XID/温度/uncorrectable 错误（默认 test_duration 180s）；memtest=11 个 memtest86 风格用例，默认 test7+test10 交替 10 分钟；nvbandwidth=单主机 copy 带宽（限定产品清单）；nccl_tests=单节点 NCCL 正确性（不支持多节点） | user-guide 页各 Plugin 小节（Targeted Power/Targeted Stress/Pulse Test/GPU Memory/Diagnostic/Memtest/NVBandwidth/NCCL Tests，2026-10-08） | latest | 官方文档原文 | pulse 在级别表中名称为 `pulse`、learn 页示例用 `pulse_test`，命名不一致；sm_stress 出现在 H100 配置示例与 --check-interval 帮助中但不在级别表 |
| 前提/影响：诊断消耗 GPU 算力、显存、PCIe、NVLink、CPU、供电与散热；长套件可重置状态或与运行中进程冲突；侵入性测试只能在可移出服务的资源上运行，需显式选 entity、与调度器协调、先 drain 应用；software/deployment 插件在目标 GPU 有其他图形进程时判失败；nvbandwidth 在 MCUTIL>10%（GPU 忙）时判失败 | learn 页 Warning 块与 "Preparing a Run"；user-guide 页 Deployment Plugin "Failure"、NVBandwidth "Failure Conditions"（2026-10-08） | latest | 官方文档原文 | "独占" 为归纳：文档逐条给出冲突条件而非一条 exclusive 声明 |
| 权限/环境前提：诊断默认降权到非特权 service account 执行；pulse_test 曾因 service account 对工作目录无写权限失败（官方给了停服务/改 systemd WorkingDirectory 两种规避）；存在 DCGM_ST_REQUIRES_ROOT 退出码（227）；nccl_tests 需预设 DCGM_NCCL_TESTS_BIN_PATH（未设则优雅跳过），root 运行时对测试二进制有 owner/权限安全检查；software 检查含设备节点访问/cgroup 限制、驱动冲突、环境变量、page-retirement/row-remap/InfoROM/Fabric Manager 状态；deployment 插件要求 nouveau 未加载、CUDA 库可达 | user-guide 页 Pulse Test 注意事项、Exit Codes 表、NCCL Tests Plugin Prerequisites、Deployment Plugin Preconditions；learn 页 software 行（2026-10-08） | latest（pulse 权限问题注明 DCGM 2.4/3.0，"will be fixed in a future release"，当前状态未核实） | 官方文档原文 | 权限问题是否已修复未知 |
| 结果语义：按测试汇总、每 entity 与 Warning 组织，错误带 ID/Severity/Category；ISOLATE/RESET 按官方建议及时处理，其余作站点分析。非零码既可能是调用失败，也可能是诊断执行后的结果失败：226/DCGM_ST_NVVS_ERROR 与 205/DCGM_ST_NVVS_ISOLATE_ERROR；需同时解析 test status、warning、skipped、per-entity error，JSON 无稳定 schema | [user-guide Exit Codes](https://docs.nvidia.com/datacenter/dcgm/latest/user-guide/dcgm-diagnostics.html#exit-codes)、Automating Responses、Logging；learn Results and Logging/Exit status（2026-10-08） | latest | 官方文档 | B12-C01：不能把非零码仅当启动/连接失败，也不能由此单独判硬件根因；必需检查跳过无替代证据时不回服 |
| 边界（官方原文）："DCGM Diagnostics do not repair faults, replace NVIDIA offline field diagnostics, or determine RMA eligibility"；失败可源于 host、权限、库、拓扑、冷却、供电或负载干扰，不必然在目标处理器；被动健康无事件但主动诊断可失败，反之亦然 | learn 页 "Beyond Scope"/"When diagnostics are useful"；user-guide 页 "Beyond the Scope"（2026-10-08） | latest | 官方文档原文 | — |
| 配置分层：diag-skus.yaml 提供按产品（PCI ID）的默认 is_allowed/阈值；--configfile 覆盖、--parameters 最终优先；配置不能让缺失插件或不支持测试变为可用；v3.3.9 固定源码 nvvs/diag-skus.yaml.in 实际含 targeted_power/targeted_stress/sm_stress/memory_bandwidth/pulse_test 等按 SKU 配置块 | learn 页 "Configuration File"；NVIDIA/DCGM@b0ec3c624ea21e688b0d93cf9b214ae0eeb6fe52 nvvs/diag-skus.yaml.in L24–36 起（gh api 读取）；nvvs/plugin_src 目录仅 contextcreate/diagnostic/memory/memtest/pcie/software/targetedpower/targetedstress | DCGM v3.3.9 固定 commit + latest 文档 | 固定源码 + 官方文档 | sm_stress 在配置中出现但 plugin_src 无同名目录，实现归属未追；pulse/nvbandwidth/nccl_tests 不在该开源目录 |

## 主张—证据表（SuperBench 主动验证）

| 主张 | 来源与定位 | 版本/环境 | 证据性质 | 反例/未知 |
|---|---|---|---|---|
| 动机：硬件冗余导致灰色退化（gray failure）；厂商出厂 qualification 测不出只在真实负载出现的退化（A100 计算+通信并发触发 L2 cache 干扰的案例，单独 GEMM 或 NCCL 测试均不暴露）；被动排障慢（38.1% incident 超过 1 天）且不恢复冗余 | arXiv HTML https://arxiv.org/html/2402.06194v2 §1、§2.1–2.2（2026-10-08 读取；对应已登记 src.usenix.superbench-atc24，USENIX ATC 2024 pp.835–850） | 论文 v2；Azure A100 生产观察 | 同行评审论文 | Azure 特定数据不外推；35× 为缺陷链路数量倍数（前批已核） |
| benchmark 三层分类：端到端 benchmark（代表性模型 CNN/BERT/GPT，参数取生产最常见配置）；component-wise micro-benchmark（CPU、内存、GPU 计算单元、GPU 显存、NIC/HCA、磁盘、PCIe/xGMI/NVLink、网络链路，采用厂商认可的第三方工具）；pattern-wise micro-benchmark（常用形状的 cuBLAS/cuDNN kernel、常用消息大小的 all-reduce/all-to-all 原语）。Table 2 为完整清单 | 同上 §3.2、§4 | 论文 | 论文 | arXiv HTML 抽取未渲染 Table 2 表格内容，具体 benchmark 名称清单本轮未取得 |
| 通过判据不是厂商规格比对：论文明确端到端性能无法直接映射硬件规格（GPU FLOPS/显存带宽/NVLink 速度）且无 ground truth；判据为离线无监督学习——在 CDF 分布空间算样本相似度，迭代剔除缺陷样本后取中位样本作 criteria，相似度阈值 α=0.95；吞吐类指标用单向距离只判"更差"；首次（集群 build-out）跑全集学判据，后续选择性验证与判据比对 | 同上 §2.3、§3.4、Algorithm 2、§5.3 | 论文 | 论文 | α 为经验值；判据需随数据周期更新 |
| 执行分层：先 single-node 阶段后 multiple-node 阶段；每阶段先 micro 后端到端；每阶段结束剔除缺陷节点以免污染后续测试；网络验证用逐对 RDMA 扫描，full scan O(n)（round-robin 配对）、quick scan O(1)（按 hop 数拓扑感知） | 同上 §4 "Networking Validation" | 论文 | 论文 | — |
| 生产检出规模：部署 Azure 两年+，作为集群交付前的 quality gate；build-out 期 24k+ A100 GPU（3k+ VM）、90 天数据，10.36% 节点被判为缺陷（不去重口径：每缺陷节点可被多个 benchmark 命中）；有效 benchmark 复测一致性 >97.5%、多数 >99.0% | 同上 §5.4 | 论文 | 论文（生产统计） | 缺陷定义即"任何失败或退化"，无独立 ground truth |
| 局限（论文自述或可推导）：MTBI 提升 22.61× 来自仿真而非生产实测，且仿真假设"全集 benchmark 能发现所有 incident"；测量方差不可消除（引 MLPerf ±2.5%/±5%）；不可能覆盖全部负载×规模×节点序组合；罕见负载需先漏检一次再补为新端到端 benchmark；固件/驱动更新后需重调参数 | 同上 §1、§2.3、§3.2、§5.1–5.2、§3.4 "Repeatability" | 论文 | 论文 | — |

## 主张—证据表（昇腾 ascend-dmi 与整机侧）

| 主张 | 来源与定位 | 版本/环境 | 证据性质 | 反例/未知 |
|---|---|---|---|---|
| ascend-dmi 提供整卡故障诊断（-dg），检查项分软件类（cann=CANN 与驱动兼容性、driver=驱动健康）与硬件类（device、network、bandwidth、aiflops、hbm、aicore、signalQuality、prbs）；bandwidth 覆盖 H2D/D2H/D2D/P2P 四方向 | registry 条目 URL toolboxug_0020.html（2026-10-08 复读） | MindX DL 6.0.RC2 | 官方文档参数表 | 各检查项内部方法（判据/阈值）页面未给 |
| 多项检查有产品/权限限制：network、hbm 仅训练系列/A2 训练（hbm 另含 800I A2）；aicore 限 A2 训练/800I A2 且 root，容器/VM 需特权，不能与其他项同测；prbs 限 root + 指定机型（800T A2/200T A2 Box16/800I A2），默认 prbs31 不可改码型，仅物理机/特权容器，不与其他项同测，RoCE 端口时长 3–10s 且仅 6.0.RC2.1+；signalQuality 覆盖 PCIe/HCCS/RoCE | 同上 | MindX DL 6.0.RC2 | 官方文档原文 | 首次提取未得页首/表4，修订时已补读；PRBS PASS/FAIL 描述内部冲突与 SKIP/读取失败边界继续保留 |
| 压力测试能力：-s 触发 HBM/AICore；--sc 为 AICore 次数（1–100，默认1）；-st 为 HBM 时长 60–604800 秒；-qs 与 -st/--sc 互斥；部分测试默认确认提示。补读页首表1/2：AICore 单轮诊断 7–20 分钟、压测 15–40 分钟；上线/巡检建议 3 轮诊断全部通过，任一 EMERGENCY_WARN 转故障处置 | [0020 页表1/2与参数表](https://www.hiascend.com/doc_center/source/zh/mindx-dl/60rc2/toolbox/ascenddmi/toolboxug_0020.html)，2026-10-08 修订时补读 | MindX DL 6.0.RC2 | 官方文档表与前提 | 文档耗时不是目标机型/本站保证；有单项耗时表，仍无已核对的 DCGM 式级别化套件 |
| AICore 前提与收尾：页列 Atlas A2 配套 HDK 23.0.0+ MCU/驱动/固件、CANN 7.0.0+ toolkit 与 kernels、环境配置；压测 HOST 需约 20–40GB 内存且不可在上次未完成时重复；诊断完成重启设备，压测后先分析定位再重启 | 同上“约束与限制”“前提条件” | 同上 | 官方前提及动作要求 | B12-C02：软件版本下限不构成已验证配套；实际重启须授权与窗口。恢复服务需处置、必要收尾/复测和验收条件满足，测试完成不自动回服；此回服门槛为本库流程判断 |
| 查询能力（同工具显示界面）：芯片型号、NPU 数量、实时功耗、AI Core/Cube/Vector 信息、AI CPU、内存容量与带宽使用率、温度、电压、health、PCIe 链路 LnkCap/LnkSta 速率宽度、错误计数、ECC 单/双 bit 计数（Atlas A2 训练系列不支持该 ECC 显示项） | toolboxug_0019.html 表2（2026-10-08；同文档树相邻页，未单独登记） | MindX DL 6.0.RC2 | 官方文档原文 | 0019 页未登记入 registry，正文若引用需补登记 |
| NPU 侧有 ascend-dmi -dg 与压测，覆盖软件兼容性/驱动/设备/网络/带宽/算力/HBM/AICore/信号质量/误码，并给单项诊断/压测耗时 | 同页表1/2、参数与状态表 | MindX DL 6.0.RC2 | 官方文档归纳 | 缺口：尚无已核对的 r1–r4 式级别化套件或对应 DCGM 的严重度/分类处置枚举；覆盖差异（供电脉冲、长期 memtest 等）未证实，不声明等价 |
| DGX H100/H200 验收可核对的规格基线：8×H100(640GB)/H200(1.128TB)；4×NVSwitch 900GB/s；4×OSFP 带 8×CX-7 IB 400G + 2×双口 CX-7；2TB DIMM；6×3.3kW PSU 4+2，≥3 PSU 才开机、仅 3 PSU 供电时降性能运行；环境 5–30°C、20–80%RH、1105 CFM@80%PWM、38,557 BTU/hr；网络端口↔PCI bus↔GPU 映射表可用于拓扑核对；DGX OS 预装 NVSM（主动健康监控）与 DCGM | https://docs.nvidia.com/dgx/dgxh100-user-guide/introduction-to-dgxh100.html（2026-10-08 复读；已登记 src.nvidia.dgx-h100-h200-user-guide-2026-01-26） | 页面 last updated 2026-01-26 | 官方文档原文 | 该页无验收/burn-in 流程章节；规格只作核对基线，H100/H200 数值分列勿混 |

## 主张—证据表（候选新来源：NVIDIA GPU Node Triage）

| 主张 | 来源与定位 | 版本/环境 | 证据性质 | 反例/未知 |
|---|---|---|---|---|
| 官方故障节点排查结构：通知来源→三张流程图（通用/用户报告/调试应用）；上报厂商的数据清单（OS/驱动信息、关键日志、已做步骤、nvidia-bug-report.sh 全量输出、HGX 的 fabric manager 日志、DCGM Diagnostics 日志）；常见 Xid 表（13/31/45/48/61/62/63/64/74/79/92/94/95/123）含动作（drain/cordon、reset、field diag、报 bug）；按架构/FM 状态/虚拟化分列的 GPU reset 能力限制表 | https://docs.nvidia.com/deploy/gpu-debug-guidelines/gpu-node-triage.html（2026-10-08 观察） | latest（可变） | 官方文档原文 | **未登记**；许可状态 unknown（deploy 文档树未见再分发许可声明）；页面无版本号/更新日期可见 |
| 与验收直接相关的官方建议：dcgmi diag 的 1/2/3 套件（该页只提三级，未提 level 4），long 约 30 分钟，可作 prolog/收工前检查；"Field diagnostic is the authoritative and comprehensive NVIDIA tool… usually required before an RMA"，运行时机须咨询系统厂商；网络验收用 nccl-tests all_reduce_perf 逐对测、投产前记录性能作基线；多 rail 拓扑可按 rail 隔离 | 同上 "Running DCGM Diagnostics"/"Running Field Diagnostics"/"Network Testing" | latest | 官方文档原文 | 与 DCGM 文档 r4 存在口径差（该页只列三级）；建议正文引用时注明该页为 deploy 树动态页 |

## DCGM 级别/测试清单摘录（user-guide 页原表，latest，2026-10-08 观察）

| Plugin | 测试名 | r1 Short <2.5s | r2 Medium（4 卡 <2.5min，8 卡 <10.5min） | r3 Long（4 卡 <10min，8 卡 <35min） | r4 Extra Long（4 卡 <45min，8 卡 <2.25h） |
|---|---|---|---|---|---|
| Software | software | ✓ | ✓ | ✓ | ✓ |
| PCIe+NVLink | pcie | | ✓ | ✓ | ✓ |
| GPU Memory | memory | | ✓ | ✓ | ✓ |
| Memory Bandwidth | memory_bandwidth | | ✓ | ✓ | ✓ |
| Diagnostics | diagnostic | | | ✓ | ✓ |
| Targeted Stress | targeted_stress | | | ✓ | ✓ |
| Targeted Power | targeted_power | | | ✓ | ✓ |
| NVBandwidth | nvbandwidth | | | ✓ | ✓ |
| NCCL Tests | nccl_tests | | | ✓ | ✓ |
| Memory Stress | memtest | | | | ✓ |
| Input EDPp | pulse | | | | ✓ |

表头注明 "measured on Hopper GPU systems"。`-r` 帮助文本：1=Quick (System Validation)、2=Medium (Extended System Validation)、3=Long (System HW Diagnostics)、4=Extended (Longer-running System HW Diagnostics)；可用测试名逗号组合（如 `-r "pcie,diagnostic"`），指定单项会附带执行内置 software 检查（learn 页）。非数据中心 GPU（GeForce/Quadro）只支持 level 1，更高级别按产品文档（learn 页 Note）。

## SuperBench 分类与判据摘录（arXiv:2402.06194v2）

- 分类（§3.2）：端到端 benchmark 代表客户负载（CNN/BERT/GPT，参数取生产分布最 prevalent 值；新主导负载可扩展加入）；component-wise micro-benchmark 覆盖 CPU/内存/GPU 计算单元/GPU 显存/NIC/HCA/磁盘/PCIe/xGMI/NVLink/网络链路，"leverage third-party tools accredited by hardware vendors"；pattern-wise micro-benchmark 为常用 cuBLAS/cuDNN 形状与 all-reduce/all-to-all 常用消息大小。
- 判据（§3.4）：原文 "there is no ground truth to differentiate the performance of defective components…end-to-end performance cannot be directly mapped to hardware specifications"；在经验 CDF 分布空间定义样本距离/相似度（Eq.2–3），Algorithm 2 迭代剔除相似度 ≤α 的样本后取中位样本为 criteria，α=0.95（§5.3）；在线过滤用单向距离（Eq.4）只判性能更差方向。
- 执行（§4）：single-node 阶段→multiple-node 阶段；每阶段 micro 先行、端到端随后；阶段间剔除缺陷节点。网络验证 full scan O(n) round-robin、quick scan O(1) 按 hop。
- 生产（§5.4）："acts as a quality gate…before delivering GPU clusters"；24k+ A100/90 天 build-out 数据，10.36% 节点缺陷；MTBI 22.61× 为仿真（§5.2 假设全集可发现全部 incident）。

## 冲突与未解决项

1. DCGM 两个 latest 页面测试清单不一致：learn 页选择指南含 context_create、不含 nccl_tests/sm_stress；user-guide 级别表含 nccl_tests（r3）、不含 context_create；pulse vs pulse_test 命名不一致。正文引用测试名时注明所依据页面。
2. sm_stress：出现在 user-guide 的 H100 配置示例、--check-interval 帮助及 v3.3.9 diag-skus.yaml.in，但不在级别表，plugin_src 无同名目录——实现归属与默认级别未解决，正文不宜断言其属于某级别。
3. GPU Node Triage 页只提 diag 套件 1–3，未提 level 4；与 DCGM 文档并存，引用时注明口径来源。
4. SuperBench arXiv HTML 的 Table 2（完整 benchmark 清单）未被提取器渲染，本轮未取得逐项名单；如需逐项引用需读 PDF。
5. 初次研究仅提取 0020 页参数表；2026-10-08 修订补读已取得页首表1/2、前提/限制与表4，AICore 资源与收尾缺口已补。PRBS PASS/FAIL 内部冲突仍存在，不据此给通过判定。0019 显示界面及 user-guide/triage 页已在集成阶段登记，初次研究的“未登记”备注仅是当时快照。
6. DGX 指南无验收/burn-in 专章；只可作规格核对基线。
7. DCGM pulse_test 权限问题标注 DCGM 2.4/3.0 且 "will be fixed"，当前 latest 是否已修未核实。
8. 未核实项：dcgmi mndiag（多节点诊断）细节、DCGM 各 SKU diag-skus.yaml 的具体阈值数值（正文不应写死阈值）。

## 实际读取清单

1. https://docs.nvidia.com/datacenter/dcgm/latest/learn/modules/dcgm-diagnostics.html —— FetchURL 全文（2026-10-08）
2. https://docs.nvidia.com/datacenter/dcgm/latest/user-guide/dcgm-diagnostics.html —— FetchURL 全文 72K 字符含插件参考（2026-10-08；该形态页未单独登记）
3. https://docs.nvidia.com/deploy/gpu-debug-guidelines/gpu-node-triage.html —— FetchURL 全文（2026-10-08；候选未登记）
4. https://arxiv.org/html/2402.06194v2 —— FetchURL 全文（2026-10-08；§1–§7，表 1/3–6 文本部分渲染、Table 2 未渲染）
5. https://www.hiascend.com/doc_center/source/zh/mindx-dl/60rc2/toolbox/ascenddmi/toolboxug_0020.html —— FetchURL（2026-10-08；仅参数表，两次抓取一致）
6. https://www.hiascend.com/doc_center/source/zh/mindx-dl/60rc2/toolbox/ascenddmi/toolboxug_0019.html —— FetchURL（2026-10-08；显示界面参数表2，未登记）
7. https://docs.nvidia.com/dgx/dgxh100-user-guide/introduction-to-dgxh100.html —— FetchURL 全文（2026-10-08）
8. NVIDIA/DCGM@b0ec3c624ea21e688b0d93cf9b214ae0eeb6fe52 —— gh api：仓库根、nvvs/、nvvs/plugin_src/ 目录列表；nvvs/diag-skus.yaml.in 测试名 grep（L22–215）
9. sources/registry.yaml、plans/round-02-backlog.yaml、docs/research/batch-10-power-thermal-sources.md —— 本地复读

## 给正文的建议（验收分层与证据强度）

1. **被动证据层**（最弱但零侵入）：健康监控/Xid/ECC 计数/规格核对（DGX 组件表、端口映射、电源冗余行为）。边界：Healthy/无事件只覆盖已启用规则与保留样本（health-monitoring 页前批已核），不能证明硬件完好。
2. **主动诊断层**（中强证据，需 drain）：DCGM r1 就绪检查（秒级）→ r2 失败后检查（分钟级）→ r3/r4 管理员级（十分钟到小时级，Hopper 口径）；昇腾用 ascend-dmi -dg + -s 压测，注意产品/root/特权容器限制与防呆提示。边界：一次通过 ≠ 硬件无故障；失败可源于 host/权限/拓扑/供电/负载干扰；DCGM 明确不判定 RMA 资格，RMA 前以 field diagnostics 为准（triage 页）。
3. **基准验收层**（性能退化证据，需基线）：nccl-tests 逐对+投产前记录基线（triage 页官方建议）；SuperBench 方法为"与集群群体判据比"而非"与厂商规格比"，单机验收没有群体判据时只能依赖本地基线/规格下限（如 targeted_power 的 TDP-1×75%）——正文应区分这两种判据来源。
4. **仍只能标 unknown 的项**：NPU 侧与 DCGM 对应的级别化套件/处置枚举及覆盖对比；其他机型/配置的资源影响和耗时；SuperBench Table 2 逐项清单；未在该页给出的内部判据；pulse_test 权限问题修复状态。0020 页已有单项耗时表与 AICore HOST 内存预算，本次补读后不再将两项概括为缺失。
5. 返修节点额外引用：SuperBench 的 OFR/hot buffer 流转模式与"修复后全量重验"做法（§3.1 workflow 第 7 步）可作流程参考，但标注为单一厂商生产实践。
