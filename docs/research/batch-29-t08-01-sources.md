# 第二十九批 T08-01 来源记录

任务：T08-01（故障模型、跨层传播与共享失效分析；**new** `knowledge/08-reliability/fault-models-and-propagation.md`，主题 08.2/08.5）。取证轮次：主会话作者角色首轮（2026-10-21；无前置依赖，批内为首任务）。

## 新增来源与主张定位

| 主张 | 登记 ID | 精确位置 | 支持范围 |
|---|---|---|---|
| fault/error/failure 定义链、dormant/active、vulnerability；失效模式四视角（content/timing、halt/silent/erratic、signaled/unsignaled、consistent/Byzantine）；八维初等故障类与组合类；solid(hard)/elusive(soft) 与 intermittent；跨层传播（组件失效成为所在系统故障、服务接口外部传播） | src.paper.avizienis-dependability-2004（**本轮新增**） | [作者 Landwehr 托管全文 PDF](https://www.landwehr.org/2004-aviz-laprie-randell.pdf)（IEEE TDSC 1(1):11–33, 2004；DOI 10.1109/TDSC.2004.2；2026-10-21 curl 取回 2.6MB PDF，pdftotext 逐段核对 §2.2/§3.2.1/§3.3/§4） | 仅定义与分类学；论文不含 GPU/NPU 系统与任何发生率 |

## 复用来源与主张定位

| 主张 | 登记 ID | 精确位置 | 支持范围 |
|---|---|---|---|
| 级联失效＝正反馈放大；重试必须随机指数退避＋预算；队列保持小；deadline 传播 | src.google.sre-cascading-failures | [Addressing Cascading Failures](https://sre.google/sre-book/addressing-cascading-failures/)（Batch 28 已核，2026-10-21 观察） | 图 B 上行放大段与传播要点；对策细节归 08.5 处置正文 |
| 按关键度丢弃、容量以资源度量 | src.google.sre-handling-overload | [Handling Overload](https://sre.google/sre-book/handling-overload/)（Batch 28 已核） | 图 B 依赖行的对策存在性 |
| CPU SDC、干净日志盲区 | src.arxiv.sdc-at-scale-v1 | [arXiv:2102.11245v1](https://arxiv.org/abs/2102.11245v1)（§5/§7，第九批已核） | F2 行 CPU 证据；不外推 GPU/NPU |
| AI 加速器生态静默损坏检测讨论 | src.ocp.sdc-in-ai-2025 | OCP 峰会材料（既有登记） | F2 行 GPU 侧范围限定；未取得 NPU 发生率 |
| 冗余掩盖灰色退化、缺陷 IB 链路与热节流观察 | src.usenix.superbench-atc24 | [USENIX ATC 2024](https://www.usenix.org/conference/atc24/presentation/xiong)（第九/十批已核页码） | F3 行；限 Azure GPU 场景 |
| 隐式错误（HTTP 200 但内容错） | src.google.sre-monitoring-distributed-systems | [Monitoring Distributed Systems](https://sre.google/sre-book/monitoring-distributed-systems/)（2026-09-29 已核） | 静默失效行（经由 08.6 正文间接引用，正文未直接展开） |
| 机柜供电/散热共享域、N+1 与三回路负载 ≤50% | 01 域已核登记（DGX H100/H200 planning 等，见 rack-power-cooling-and-failure-domains） | 见 [rack-power 正文](../../knowledge/01-hardware/rack-power-cooling-and-failure-domains.md) | F8 行与共同依赖行（本文不重复数值） |
| 一个慢 rank 经同步屏障表现为全体超时 | 03 域已核登记 | [collectives-and-rank-progress](../../knowledge/03-communication/collectives-and-rank-progress.md) | "传播≠多起故障"纪律 |
| 设备健康观测/诊断隔离语义 | 01/05 域已核登记（DCGM docs、nvidia-smi docs） | [health-evidence](../../knowledge/01-hardware/health-evidence.md) | F1 行可观测点；平台差异段 |

## 本文原创部分

fault→error→failure 表的 GPU/NPU 例子列、三维度分类表、两张传播图（图 A 训练/图 B 推理）、FMEA 表九行（发生条件列全部为条件描述、无概率）、传播/同因区分五步法、冗余独立性检查问题清单。

## unknown 清单

1. 所有 FMEA 行均无发生概率来源，正文按"示例，非概率"标注。
2. NPU 侧静默损坏/故障统计无公开充分材料，F2 行对 NPU 保持 unknown。
3. Avizienis 八维故障类的 31 组合类全文枚举未复制进正文（仅引用维度存在性）；需要完整枚举时回原论文 Fig.5。
4. 传播图各边为典型路径归纳（本库原创），无单一来源可整体支撑；逐边证据须回各域正文与现场时间线。
