# 第五批准入与放置资料候选

2026-09-29，主任务预查。尚非正式来源登记或 F12 正文。

## 已打开的项目原始页面

- [Kueue v0.19 Admission](https://kueue.sigs.k8s.io/v0.19/docs/concepts/admission/)：页面版本导航为 v0.19，内容分开 quota reservation、启用 TAS 时的物理放置检查及 admission checks。正式正文可用来区分配额与准入；其失败处理段包含特定 ProvisioningRequest 语义，不应直接外推到全部 admission check 实现。页面显示 `.status.active`，正式写作前应与固定 API/源码交叉核验，不照抄为变更命令。
- [Volcano v1.15.0 PodGroup](https://volcano.sh/docs/v1.15.0/concepts/podgroup/)：通过当前页版本导航进入，页面显示 v1.15.0；`minMember`、`minResources`、`phase` 和 `conditions` 可用于解释组级约束及状态证据。满足最小成员约束不能证明全部进程已完成 rendezvous 或训练开始。
- [Volcano 当前 Gang 插件说明](https://volcano.sh/docs/scheduler/plugins/gang/)：已读取正文，但尚未固定源码。页面中的内部 Ready 术语不应自动等同 Kubernetes Pod Ready condition。涉及 `minAvailable` 与 PodGroup `minMember` 的映射，正式写作应另取固定控制器/调度插件实现。

## 正式写作边界

1. 共用概念链为：对象被接受 → 排队/配额 → 准入 → 节点放置 → 设备分配 → 容器/进程启动 → 应用组就绪。各系统可能合并或省略阶段，不套一个统一状态枚举。
2. 不因两节点各有四个设备，就推断一个请求八设备的单 Pod 可放置；同时记录设备资源类型、CPU/主机内存、节点条件和拓扑约束。
3. NPU 的拓扑与资源名从固定 MindCluster/MindSpeed 或厂商说明取得。Kueue/Volcano 的概念和 GPU 示例不证明任一 Ascend 插件组合已支持。
4. 继续读取许可、精确发行来源以及与现有 F11 的边界；不得仅凭当前网页宣布支持版本或默认配置。
