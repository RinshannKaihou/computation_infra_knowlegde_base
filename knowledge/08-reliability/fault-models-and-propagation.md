---
id: reliability.fault-models-and-propagation
title: 故障模型、跨层传播与共享失效分析
type: concept
domain: reliability
status: draft
platforms: [generic]
source_refs:
  - src.paper.avizienis-dependability-2004
  - src.google.sre-cascading-failures
  - src.google.sre-handling-overload
  - src.arxiv.sdc-at-scale-v1
  - src.ocp.sdc-in-ai-2025
  - src.usenix.superbench-atc24
updated_at: "2026-10-21"
summary: 用 fault→error→failure 三链定义故障、差错与失效，按持续性/显隐性/相关性给出面向 GPU/NPU 系统的故障分类，给出训练与推理两张跨层传播图、有限 FMEA 表与区分传播/同因、检验隔离与冗余独立性的方法；不给出任何发生率。
related_ids:
  - reliability.dimensions-and-failure-domains
  - reliability.evidence-and-hypotheses
  - reliability.silent-errors-and-integrity
  - reliability.correlated-failure-source-case
  - reliability.mitigation-and-recovery-principles
  - hardware.rack-power-cooling-and-failure-domains
  - hardware.health-evidence
  - communication.collectives-and-rank-progress
  - cluster-platform.device-resource-chain
  - data-storage.training-data-path
verification:
  status: source_checked
  evidence_refs:
    - src.paper.avizienis-dependability-2004
    - src.google.sre-cascading-failures
    - src.arxiv.sdc-at-scale-v1
    - src.ocp.sdc-in-ai-2025
    - src.usenix.superbench-atc24
  notes: 已对照 Avizienis 2004（作者托管全文 PDF）、Google SRE 级联失效章、SDC at scale 论文、OCP SDC in AI 2025 与 SuperBench 论文核对本文引用的定义与结论；两张传播图与 FMEA 表为本库原创整理，未在真实 GPU/NPU 集群验证，不包含也不暗示任何故障发生概率。
---

# 故障模型、跨层传播与共享失效分析

## 要回答的问题

排障时最先混乱的三个词是"故障""报错"和"失效"：一张 GPU 报 ECC 错是不是故障？多个 rank 同时超时是各自失效还是一次故障的传播？本文回答：怎样把异常组织成**故障（fault）→ 差错（error）→ 失效（failure）**链条，怎样按持续性、显隐性和相关性分类，怎样画出一次故障在训练或推理栈中的跨层传播路径，以及怎样用有限的分析表检验隔离与冗余假设。故障域与四维可靠性目标的定义见[可靠性维度与故障域](dimensions-and-failure-domains.md)；本文把那篇的"域"细化到可记录的故障条目。

`generic` 表示分类方法跨平台通用；各平台的错误码、检测工具与冗余机制不同（见平台差异），环境未知时不假设分类成立。

## fault / error / failure：先固定三个词

Avizienis 等人的依赖性分类学给出标准链条（[IEEE TDSC 2004，§2.2](https://www.landwehr.org/2004-aviz-laprie-randell.pdf)）：

| 概念 | 定义（按原文归纳） | GPU/NPU 系统的例子 |
|---|---|---|
| **失效 failure** | 交付服务偏离正确服务的**事件**；从正确服务到不正确服务是一次转换 | 请求超时或返回错值；训练 step 停滞；作业退出码非 0；checkpoint 读回失败 |
| **差错 error** | 系统总状态中**可能导致后续服务失效的那部分偏离**；多数差错不会到达外部接口 | 损坏的激活值仍在计算；计数器越界前的错误状态；只影响部分副本的旧配置 |
| **故障 fault** | 差错的**被判定或被假设的成因**；可以是内部的或外部的 | 坏内存单元、驱动缺陷、错误配置、掉电、输入数据污染 |

三个性质直接可用：

- **休眠与激活**：故障在产生差错前处于休眠态；激活模式（输入组合、环境条件）可复现的称为 **solid/hard**，不可系统复现的称为 **elusive/soft**，后者与暂态物理故障的表现接近（同文 §4）。这解释了"重跑就好了"为什么不是根因证据。
- **跨层因果**：组件失效会变成所在系统的故障，并通过服务接口向接收方外部传播（A 的失效是 B 的故障）。因此"上游报错"与"本地故障"是同一条链的两段，不是两个独立事件。
- **漏洞 vulnerability**：外部故障要造成差错，通常先有使能它的内部故障（如同样的错误配置之所以生效，是因为缺少校验这道防线）。

失效模式按四个视角细分（同文 §3.3），每个视角都有 GPU/NPU 对应物：

| 视角 | 分类 | GPU/NPU 对应 |
|---|---|---|
| 领域 | content（内容错）/ timing（过早或过晚）；两者兼有 | 错误输出 token；慢 rank 拖垮 step 时间；"结果对但 TTFT 超限" |
| 可检测性 | signaled（有告警）/ unsignaled（无告警）；检测机制自身会 false alarm | ECC 不可纠正错误带信号 vs 静默数据损坏（SDC）无信号；健康检查误报隔离了好节点 |
| 一致性 | consistent（所有用户看到同一错误）/ inconsistent（各用户不同，即 Byzantine） | 同一副本对所有请求错；分布式训练中部分 rank 数值发散（各 rank 看到的"正确值"不同） |
| 后果 | severity 分级（按应用定义） | 由业务约定，本文不预设 |

## 故障分类：持续性、显隐性、相关性

| 维度 | 取值 | 判定对象 | 与处置的关系 |
|---|---|---|---|
| 持续性 | 暂态 / 间歇 / 永久 | **故障本身**（或其激活模式）：一次即逝、反复出现但不定时、持续存在 | 暂态倾向重试与观察；永久要求隔离替换；间歇最难，需要捕获窗口而非单次复现 |
| 显隐性 | 显性（有信号）/ 静默（无信号） | **失效模式**（信号是否到达观测点） | 静默失效需要独立的正确性检测（见[静默错误与计算完整性判定](silent-errors-and-integrity.md)），不能靠告警缺席判健康 |
| 相关性 | 独立 / 相关 / 共同原因 | **多个对象之间的故障关系** | 只有跨越相关故障域的冗余才有效；定义见[可靠性维度与故障域](dimensions-and-failure-domains.md)的共同原因一节 |

间歇故障在分类学中是"表现相似于暂态物理故障的难复现开发故障与暂态物理故障的合称"；它们的共同特征是差错出现与消失看似随机（同文 §4，Fig.13）。这与 GPU/NPU 系统中"偶发 collective 超时、重启后消失"的现象同型，但**本文不引用任何发生率**。

三条纪律：

1. **不要把统计外推当分类**。"某研究称数据中心 CPU 的 SDC 常见"不能推出 NPU 也有相同比例：[SDC at scale](https://arxiv.org/abs/2102.11245v1) 覆盖的是数据中心 CPU 与跨栈应用表现；[OCP SDC in AI 2025](https://www.opencompute.org/) 讨论的是 AI 加速器生态的检测实践；两者都不建立 NPU 发生率，本库保持 unknown。
2. **不要把冗余当成独立**。多卡、多副本、多路径只有在供电、网络、存储、控制面、镜像与配置批次上不共享时才独立（见传播图的共同依赖行）。
3. **不要把传播当多起故障**。一个慢 rank 经同步集合通信表现为全体超时是传播，不是每个 rank 各自坏了（见[集合通信与 rank 进度](../03-communication/collectives-and-rank-progress.md)）。

## 两张跨层传播图

以下为本库**原创示意图**：箭头是差错传播的典型路径，不是必然路径；每条边是否成立要靠当时证据（对齐方法见[诊断中的证据、假设与结论](evidence-and-hypotheses.md)）。

**图 A：训练栈（数据 → rank → collective → 作业 → 有效进展）**

```text
数据/存储层        主机与设备层          集合通信层           作业/调度层            目标
┌─────────┐   ┌─────────────┐   ┌──────────────┐   ┌───────────────┐   ┌──────────┐
│样本损坏/ │──▶│ rank 计算错值 │──▶│ 一步 collective│──▶│ step 停滞/超时  │──▶│有效进展损失│
│读路径变慢│   │ 慢 rank(OOM/降频)│   │ 全体等最慢者    │   │ 作业失败/重启   │   │(重算+恢复) │
└─────────┘   └─────────────┘   └──────┬───────┘   └───────┬───────┘   └──────────┘
     ▲            ▲      ▲              │待机/重传            │backoff/重新排队
     │            │      └── 静默错值可绕过告警直达 loss/权重               │
     │            └─ 设备不可纠正错误/掉卡: 单点故障                       │
 共同依赖（跨层横切）: 机柜供电与散热域 │ ToR/spine 网络 │ 存储路径 │ 控制面(调度/状态) │ 镜像与配置批次
```

要点：差错可以在任何一层被截断（校验、重试、隔离），也可能换一种形式继续传播——数值差错以 loss 发散或权重损坏的形式存入 checkpoint，把一次暂态故障固化为永久状态（恢复边界的讨论见[Checkpoint 状态一致性](../06-training/checkpoint-state-consistency.md)）。

**图 B：推理服务（依赖 → 副本 → 路由 → 请求 → SLO）**

```text
依赖层            引擎/副本层          路由/准入层           客户端               目标
┌─────────┐   ┌─────────────┐   ┌──────────────┐   ┌───────────────┐   ┌──────────┐
│模型库/存储│──▶│ 副本加载失败/ │──▶│ 端点摘除/队列堆积│──▶│ 超时重试(放大)  │──▶│可用性/延迟 │
│配置/服务发现│  │ KV 膨胀 OOM   │   │ 准入拒绝(过载)  │   │ 退避风暴       │   │goodput 下降│
│下游依赖   │   └─────────────┘   └──────────────┘   └───────────────┘   └──────────┘
└─────────┘        ▲ 副本间共享: 同镜像/同配置/同存储读路径/同交换机上联
 共同依赖（跨层横切）: 供电/散热 │ 网络(ToR/spine、LB) │ 存储与模型库 │ 控制面与服务发现 │ 发布批次
```

要点：服务层故障经常**上行放大**——副本减少使剩余副本过载，过载提高超时率，客户端重试再放大流量；Google SRE 把这类正反馈称为级联失效，并给出队列保持小、重试预算、负载丢弃等对策（[Addressing Cascading Failures](https://sre.google/sre-book/addressing-cascading-failures/)、[Handling Overload](https://sre.google/sre-book/handling-overload/)，对策正文见[隔离、重试预算、降级与恢复选择](mitigation-and-recovery-principles.md)）。

**共同依赖行的证据来源**（各域已有正文，此处只汇总）：机柜供电/散热与 N+1 口径见[机柜供电散热与故障域](../01-hardware/rack-power-cooling-and-failure-domains.md)；网络拓扑（rail、leaf-spine）见[互联路径与拓扑](../03-communication/interconnect-paths.md)；存储读路径见[训练数据路径](../04-data-storage/training-data-path.md)；控制面与资源账本边界见[从物理设备到容器资源的状态链](../05-cluster-platform/device-resource-chain.md)；作业重启行为见[Kubernetes 作业全生命周期](../05-cluster-platform/kubernetes-job-lifecycle.md)。

## 有限 FMEA 表

下表是**框架示例**：发生条件列只写"何时可能"不写概率；可观测点与检测盲区按各域已登记来源写；每行的隔离/冗余假设在使用前必须按现场核实。空行由使用时补全。

| # | 故障（层） | 发生条件（示例，非概率） | 直接影响与传播 | 可观测点 | 检测盲区 | 隔离/冗余假设 |
|---|---|---|---|---|---|---|
| F1 | 设备不可纠正错误/掉卡 | 硬件物理故障；供电瞬变等外部故障 | 单 rank 停止 → 集合通信全体阻塞 → 作业重启；推理侧单副本不可用 → 端点摘除 | 驱动/带外事件、DCGM 类健康工具、集群设备事件 | 事件未上报或延迟；应用层只见超时不见根因 | 单卡故障只影响本节点作业；跨节点作业依赖调度器重建（K8s 重建语义见 05 域） |
| F2 | 静默数据损坏（SDC） | 位翻转且不经 ECC 或校验暴露 | 错值进入激活/梯度/权重 → 数值发散或污染 checkpoint 固化 | 无直接告警；间接靠 loss 异常、对照校验、事后审计 | 恰好落在容差内的错值；检测本身有假阴性/误报 | 冗余计算、校验和、副本比对可截断，但仅覆盖被校验的对象（见 08.6 判定方法） |
| F3 | 互联链路降级/缺陷 | 线缆/端口缺陷、温度、拥塞配置 | 集合通信变慢 → step 时间上涨（灰色退化）；重传增加 | 链路计数器、带宽基线对照（SuperBench 报告此类退化可能被冗余掩盖，[ATC 2024](https://www.usenix.org/conference/atc24/presentation/xiong)） | 平均值掩盖长尾；未跑基线时无对照 | 多 rail 分摊；但共享 ToR/ spine 时冗余不独立 |
| F4 | 主机资源耗尽 | 内存泄漏、磁盘写满、PID/句柄限制 | 进程 OOM 被杀 → 等同 F1 的 rank 缺席；推理侧请求失败 | 主机指标、cgroup 事件、OOM 日志 | 容器内视角缺主机上下文；缓慢泄漏在重启后重置难定位 | 节点级隔离（驱逐）有效；同节点多租户共享内核与 I/O 不是独立域 |
| F5 | 控制面不可用/降级 | 状态存储慢或分区、控制器缺陷 | 新作业不能创建、已有作业继续（数据面/control plane 分离时）；恢复积压 | 控制面指标、apiserver 延迟 | 数据面"看似正常"掩盖控制面故障；带外通道是否独立未核 | 控制面多副本仍可能共享底层存储/配置批次（见 05 域控制面恢复正文） |
| F6 | 共享存储路径变慢/不可用 | 后端容量、元数据服务、网络拥塞 | 数据加载停顿 → 训练 step 停滞；checkpoint 写失败 → 恢复点损失 | 存储客户端指标、IO 基线对照 | 客户端缓存掩盖早期退化；多作业共享时难归因 | 多路径/多后端冗余；同交换机上联时仍相关 |
| F7 | 配置/镜像/模型发布批次缺陷 | 一次发布作用于多个副本或节点 | 同批副本同时行为异常（共同原因）；推理输出质量劣化 | 版本标签对照、灰度监控、输出质量评估 | 无质量 oracle 时静默劣化；回滚是否完整未验证 | 灰度/金丝雀把批次拆小；批次内对象不独立 |
| F8 | 机柜供电/散热域事件 | 同一供电组/冷却回路的物理事件 | 整机柜多节点同时离线（图 A/B 各层同时缺席） | 带外传感器、机柜级电流/温度 | 应用层只见"多节点失联"看不到域归属 | N+1 供电、双回路按负载 ≤50% 等设计假设须按机型文档核实 |
| F9 | 客户端重试风暴（放大） | 服务降速 + 无预算的同步重试 | 请求量放大挤占容量 → 进一步超时（正反馈） | 服务端队列/并发指标、重试率 | 服务端只见"流量高"看不到客户端策略 | 重试预算与 jitter 退避（对策见 08.5 处置正文） |

**平台差异**（同一行故障在不同平台的分类工具不同，只登记工具边界不判优劣）：NVIDIA 侧以 DCGM 字段/健康判定与 NVML/`nvidia-smi` 观测、NCCL 超时在应用层表现（见[硬件健康证据](../01-hardware/health-evidence.md)、[NCCL 超时诊断](../03-communication/nccl-timeout-triage.md)）；Ascend 侧为 CANN/HCCL 错误语义与 `npu-smi`、MindSpeed-LLM 高可用文档把副本/断点续训/弹性作为处置机制登记（见[HCCL 超时诊断](../03-communication/hccl-timeout-triage.md)、v2.2.0 HA 文档登记）；AMD 侧为 ROCm/RCCL 观测与验证口径（见[RCCL 运行时与验证](../03-communication/rccl-runtime-and-verification.md)）。CPU/GPU 研究统计（F2 行的公开研究）不外推 NPU。

## 区分传播与同因、检验隔离与冗余独立性

一次异常涉及多个对象时，按顺序回答：

1. **时间线对齐**：把每个对象的观测对齐到统一时钟与实体身份（方法见[诊断中的证据、假设与结论](evidence-and-hypotheses.md)）；谁先异常？"多 rank 同时超时"里常有一个最先越界的 rank。
2. **首个异常者所在层**：首个异常出现在依赖层（存储/网络/供电）更接近共同原因；出现在多个不相邻层的同一时刻，优先怀疑共享的配置/发布或控制面。
3. **共享依赖清单核对**：对每个受影响对象填写供电组、上联交换机、存储路径、控制面实例、镜像与配置版本（模板见[计算节点资源与拓扑参考](../01-hardware/resource-topology.md)）；全部命中同一格即相关故障证据，"位于不同节点"不构成独立。
4. **反向对照**：找一个未受影响的相似对象，列出它与受影响对象的依赖差异；差异项就是候选的共享故障源。
5. **有限验证**：按[隔离、重试预算、降级与恢复选择](mitigation-and-recovery-principles.md)的故障对照设计，在可牺牲环境注入同类故障，检验"隔离域/冗余确实跨域"的假设；一个完整公开案例的推理过程见[相关故障与冗余失效的公开案例](correlated-failure-source-case.md)。

冗余独立性检查问题（建系统时问，不是出事后问）：两个副本是否同一镜像/同一发布批次？是否同一 ToR/同一 spine？是否同一供电组/冷却回路？是否同一存储读路径？是否依赖同一服务发现/DNS/认证？是否同一控制面实例？任一"是"即冗余部分失效，须按相关故障计算共同失效范围。

## 适用边界与待确认

- 本文的分类、传播图与 FMEA 表是**框架与示例**，不含任何故障率、MTBF 或概率数字；把任何一行用于具体环境前，必须先核实该行的隔离/冗余假设与观测点是否存在。
- NPU 侧公开的静默损坏/故障统计不充分，F2 行对 NPU 保持 unknown，不以 CPU/GPU 研究填补。
- 传播图的每条边是"典型路径"而非必然；实际链路以时间线证据为准。
- 故障**处置**（隔离/重试/降级/恢复的选择与预算）不在本文展开，见[隔离、重试预算、降级与恢复选择](mitigation-and-recovery-principles.md)；验收与注入测试的统一方法属 08.7，另批交付。

## 来源核对范围

- [Avizienis 等，IEEE TDSC 2004](https://www.landwehr.org/2004-aviz-laprie-randell.pdf)：核对 §2.2 的 failure/error/fault 定义、dormant/active、vulnerability；§3.3 失效模式四视角；§3.2.1 八维初等故障类；§4 的 solid/elusive、间歇故障与跨层传播。不复制其图表，不外推发生率。
- [Google SRE Book：Addressing Cascading Failures](https://sre.google/sre-book/addressing-cascading-failures/) 与 [Handling Overload](https://sre.google/sre-book/handling-overload/)：核对级联失效的正反馈描述与重试/丢弃对策的存在性；对策细节由 08.5 处置正文引用。
- [SDC at scale，arXiv:2102.11245](https://arxiv.org/abs/2102.11245v1)：核对 CPU SDC 与"干净日志"盲区；仅用于 F2 行的 CPU 证据，不外推 GPU/NPU。
- [OCP SDC in AI 2025](https://www.opencompute.org/)：核对 AI 加速器生态对静默损坏检测的公开讨论范围；未取得 NPU 发生率数据。
- [SuperBench，USENIX ATC 2024](https://www.usenix.org/conference/atc24/presentation/xiong)：核对冗余掩盖灰色退化与链路缺陷观察（限其论文 Azure GPU 场景）；不外推为其他集群基线。
