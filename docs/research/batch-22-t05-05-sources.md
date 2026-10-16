# 第二十二批 T05-05 来源记录

任务：T05-05（修订 `knowledge/05-cluster-platform/admission-and-placement.md`，concept）。作者取证方法：webfetch 只读读取固定 ref 原文件全文（行区间见下表；curl 字节级取回未执行，未部署运行）。Volcano v1.15.0 gang 插件全文（validJobFn L58–93/preempt L97–137/ready-pipelined L191–219/OnSessionClose L229–297）＋调度动作（enqueue L95–99 入队门；allocate L152–169 跳过/L313–336 提交/L832–844 丢弃；gangpreempt L32–52/L248 bundle 默认开；gangreclaim 同模型）＋控制器（running L35–46/L107–110 重启回落；restarting L35–49 重试上限；util applyPolicies 默认 Sync）＋Kueue ClusterQueue 全文 561 行（flavor/borrow/preemption/fungibility/stopPolicy L60–74/L201–242/L309–472/L506–515）＋复用 T05-02（Kueue 准入/门控）/T05-03（Slurm 分区/QOS/优先级/预留）/MindCluster 登记。

## 主张—来源定位表（ID—精确页面/节—字段/支持范围）

| 主张 | 登记 ID | 精确页面/节 | 支持范围 / 未覆盖 |
|---|---|---|---|
| Gang 成组决策/失败上报 | src.volcano.gang-plugin-v1.15.0 | [gang.go@8fc394c1](https://github.com/volcano-sh/volcano/blob/8fc394c11e8db0d0ada5c17816b58bced9d7213d/pkg/scheduler/plugins/gang/gang.go)（validJobFn L58–93/reclaim-preempt L97–137/ready-pipelined L191–219/OnSessionClose L229–297） | 插件层；应用 rendezvous 不在此层 |
| 调度动作（入队/分配/抢占） | src.volcano.scheduler-actions-v1.15.0（含 api/job_info.go L877–886/L1202–1208 Ready/Pipelined 计数；gangreclaim.go L32–52/L247 bundle 默认开） | [enqueue.go L95–99](https://github.com/volcano-sh/volcano/blob/8fc394c11e8db0d0ada5c17816b58bced9d7213d/pkg/scheduler/actions/enqueue/enqueue.go)（入队门）；[allocate.go L152–169/L313–336/L832–844](https://github.com/volcano-sh/volcano/blob/8fc394c11e8db0d0ada5c17816b58bced9d7213d/pkg/scheduler/actions/allocate/allocate.go)（跳过/提交/丢弃）；[gangpreempt.go L32–52/L248](https://github.com/volcano-sh/volcano/blob/8fc394c11e8db0d0ada5c17816b58bced9d7213d/pkg/scheduler/actions/gangpreempt/gangpreempt.go)＋gangreclaim 同模型（bundle 默认开） | 动作层；proportion/capacity/overcommit 公式未审计（unknown） |
| 控制器重启/重试/策略 | src.volcano.job-controller-v1.15.0 | [running.go L35–46/L107–110](https://github.com/volcano-sh/volcano/blob/8fc394c11e8db0d0ada5c17816b58bced9d7213d/pkg/controllers/job/state/running.go)（重启回落）；[restarting.go L35–49](https://github.com/volcano-sh/volcano/blob/8fc394c11e8db0d0ada5c17816b58bced9d7213d/pkg/controllers/job/state/restarting.go)（重试上限）；[job_controller_util.go L182–196/L286–288 applyPolicies](https://github.com/volcano-sh/volcano/blob/8fc394c11e8db0d0ada5c17816b58bced9d7213d/pkg/controllers/job/job_controller_util.go)（默认 Sync）/[job_controller_actions.go L813–816/L877–880](https://github.com/volcano-sh/volcano/blob/8fc394c11e8db0d0ada5c17816b58bced9d7213d/pkg/controllers/job/job_controller_actions.go)（minAvailable 同步） | 控制器层；handler 事件路径未覆盖（unknown） |
| Kueue 配额/借用/抢占样板 | src.kueue.cluster-queue-v0.19.0 | [cluster_queue.md@911a822a](https://github.com/kubernetes-sigs/kueue/blob/911a822a49bcfd99c9c62203a009efa4130ad604/site/content/en/docs/concepts/cluster_queue.md)（flavor/borrow/lending/preemption/fungibility/stopPolicy） | 样板层；未部署验证 |
| Slurm 样板 | src.slurm.docs-24.11.7（复用：reservations/priority_multifactor/qos/job_reason_codes/squeue 页） | T05-03 登记范围（公平性评估顺序、fair-share、预留独占/不改 priority、QOS 三作用、reason 释义） | 复用 T05-03 取证，不重复取证；站点值 unknown |
| MindCluster 边界 | src.ascend.mind-cluster-v26.1.1（复用） | 既有 NPU 节 | 复用，不推导 |

## 来源差异记录

- Gang 文档把 Pipelined 列入 Ready（文档页），实现 `ReadyTaskNum` 不计 Pipelined（job_info.go L877–886）：以实现为准，见正文。

## unknown 清单

1. Volcano handler 事件路径、配额类插件判定公式、站点启用的 action/plugin；2. Kueue×Volcano/MindCluster 共部署；3. 全部实测（未执行）。
