---
id: path.task.performance-optimization
title: 性能优化任务路径
type: path
domain: overview
status: draft
platforms:
- generic
source_refs:
- src.stas.ml-engineering
updated_at: '2026-10-22'
summary: 运行阶段性能退化的分层阅读路径：先定义负载与基线，再按硬件、主机、数据、通信、训练/推理、平台争用逐层定位。
related_ids:
- training.performance-analysis
- training.slow-rank-triage
- training.performance-regression-source-case
- hardware.power-thermal-evidence
- hardware.numa-memory-and-io-locality
- software-stack.host-resource-pressure-and-device-access
- data-storage.data-starvation-triage
- data-storage.checkpoint-slow-io-triage
- data-storage.storage-workload-baselines
- communication.bandwidth-baselines
- communication.bandwidth-degradation-triage
- communication.rdma-baseline-and-congestion-triage
- inference.latency-metrics
- inference.execution-and-kv-cache
- inference.capacity-and-autoscaling
- inference.routing-and-flow-control
- cluster-platform.accelerator-sharing-and-isolation
- cluster-platform.contention-capacity-validation
- path.task.migration-and-upgrade
- path.task.fault-recovery
---

# 性能优化任务路径

本页把"训练或推理变慢 / 不达预期"的阅读串成一条路径。它是导航草稿，不是优化处方：路径坚持先定义负载与基线、再分层定位最早瓶颈，不提供任何环境无关的调参结论；所链正文中的工具与样板各有版本与取证边界。本路径只组织阅读，不执行任何操作。`generic` 表示导航意图，不表示所有平台适用。

## 前置材料（先于优化讨论）

1. **负载定义**：训练（模型/并行配置/global step 口径）还是推理（模型/请求分布/并发与 SLO）；负载未定义前，"慢"没有对象。
2. **基线**：历史基线（同负载同口径）或厂商/工具样板口径；基线与现状必须同分母同口径才可比较。
3. **变化清单**：性能变化前的软硬件变更记录（版本、配置、拓扑、租户）。
4. **观测权限**：profiling、遥测与诊断工具能否开启；权限不足时先登记缺口（见停止条件）。

## 阅读顺序（先口径，后分层）

1. **先固定口径**：训练侧[训练性能分解、profiling 与优化验证](../../knowledge/06-training/performance-analysis.md)（有效产出与配置口径、受害方与最早瓶颈的区分）；推理侧[推理延迟与吞吐指标字典](../../knowledge/07-inference/latency-metrics.md)（TTFT/TPOT/ITL/E2E/吞吐/goodput 的起止点与聚合窗口）；存储侧[存储负载、容量与长尾基线口径](../../knowledge/04-data-storage/storage-workload-baselines.md)。
2. **硬件层**：[供电、散热与性能退化证据](../../knowledge/01-hardware/power-thermal-evidence.md)（降频位图、violation 计数与健康摘要的边界；注意 NPU 侧观测缺口）与[NUMA、主机内存与 I/O 局部性的成对验证](../../knowledge/01-hardware/numa-memory-and-io-locality.md)（局部/远端成对测量）。
3. **主机/OS 层**：[OS/进程资源压力与设备访问诊断](../../knowledge/02-software-stack/host-resource-pressure-and-device-access.md)（物理内存、cgroup 限额与设备侧 OOM 分列）。
4. **数据路径**：[训练数据供给路径与等待](../../knowledge/04-data-storage/training-data-path.md) → [训练数据加载饥饿诊断](../../knowledge/04-data-storage/data-starvation-triage.md)；checkpoint 侧 [Checkpoint 慢写与恢复 I/O 诊断](../../knowledge/04-data-storage/checkpoint-slow-io-triage.md)。
5. **通信层**：先[通信带宽与性能基线口径](../../knowledge/03-communication/bandwidth-baselines.md)，再[通信带宽退化诊断](../../knowledge/03-communication/bandwidth-degradation-triage.md)（测量口径 / 配置映射 / 真实链路三分），跨节点路径与拥塞另见 [RDMA 网络基线、路由与拥塞诊断](../../knowledge/03-communication/rdma-baseline-and-congestion-triage.md)。
6. **训练/推理执行层**：训练[慢 rank 诊断](../../knowledge/06-training/slow-rank-triage.md)（谁先慢、慢在哪个阶段）与[训练吞吐回归来源案例](../../knowledge/06-training/performance-regression-source-case.md)（框架层回归的公开反例）；推理[推理执行与 KV cache](../../knowledge/07-inference/execution-and-kv-cache.md)（容量压力、抢占重算、驱逐与批组成）、[容量、扩缩容与冷启动决策](../../knowledge/07-inference/capacity-and-autoscaling.md)与[请求路由、准入与流控](../../knowledge/07-inference/routing-and-flow-control.md)。
7. **平台争用层**：[加速器共享与租户隔离机制](../../knowledge/05-cluster-platform/accelerator-sharing-and-isolation.md)与[多租户争用、公平性与容量验证](../../knowledge/05-cluster-platform/contention-capacity-validation.md)——共享环境里"变慢"的第一候选之一。

## 目标产出

- 口径固定的基线对照表：指标、分母、窗口、测量工具与版本。
- 首个瓶颈边界的判定记录：哪一层、哪个证据、哪个时间点最早偏离；受害方与最早瓶颈分开表述。
- 单因素优化方案与双判据验证设计：吞吐/延迟改善与质量不回退（训练收敛判据、推理输出质量判据）同时成立才算完成。

## 下一步判断

- 证据指向环境或版本问题（升级/迁移引入）：转[迁移与升级任务路径](migration-and-upgrade.md)。
- 证据指向设备故障或降级（降频、ECC、链路劣化）：转[故障恢复任务路径](fault-recovery.md)与对应平台路径（[NVIDIA](../platforms/nvidia.md)/[昇腾](../platforms/ascend.md)/[AMD](../platforms/amd.md)）。
- 结论仍不确定：按[证据与假设方法](../../knowledge/08-reliability/evidence-and-hypotheses.md)列候选与区分检查，再回分层继续。

## 完成/停止条件

- **完成**：瓶颈边界有证据支撑，优化经单因素验证且双判据（性能 + 质量）通过，基线对照表更新入档。
- **停止并升级**：无基线且无法建立（无历史数据、无同口径样板）→ 先补基线，不开始调参；profiling/采集权限不足 → 登记缺口并升级，不用推测代替证据；多个变量同时变化 → 先固定单因素再比较；证据不足以区分受害方与最早瓶颈 → 按[性能分解正文](../../knowledge/06-training/performance-analysis.md)的停止条件处理，不宣布结论。

## 原始资料入口

- [ML Engineering](https://github.com/stas00/ml-engineering)：训练/推理性能与工程诊断的实践资料入口（既有登记）。

以上为外部入口，引用前需核对各自版本与许可。

## 逐链检查（T00-07 交付记录，2026-10-22）

本页全部内链经 `make check` 通过，引用的目标正文均为已交付条目；未引用未交付正文。页尾外部入口为既有登记来源（`source_refs`），不承载本页导航主张。
