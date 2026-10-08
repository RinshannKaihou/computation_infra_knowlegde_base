# 第五批 F12 准入、调度与拓扑放置来源

2026-09-30，主任务来源准备。F12 正式正文已创建并接入导航，待轮末审阅；本记录不是调度器运行验证。用户要求下一轮完成后由 astra/xhigh 审阅。

## Kueue v0.19.0

只读 `git ls-remote` 解析 tag：tag 对象 `7b3cad14a540cd256dc9c658be5a23fff809ff68`，剥离后 commit `911a822a49bcfd99c9c62203a009efa4130ad604`。读取 GitHub 该 commit 的递归目录（未截断），再读取以下固定 raw 文件；没有执行源码。

| 固定来源 | 核对范围 |
|---|---|
| [admission.md](https://github.com/kubernetes-sigs/kueue/blob/911a822a49bcfd99c9c62203a009efa4130ad604/site/content/en/docs/concepts/admission.md) | 配额预留、TAS 与 admission checks 的不同职责；不将其中 ProvisioningRequest 失败处理推广为所有插件行为 |
| [workload.md](https://github.com/kubernetes-sigs/kueue/blob/911a822a49bcfd99c9c62203a009efa4130ad604/site/content/en/docs/concepts/workload.md) | Workload 是准入对象，podSets 表达一组 Pod 的资源需求；requests 和数量用于配额核算 |
| [workload_types.go](https://github.com/kubernetes-sigs/kueue/blob/911a822a49bcfd99c9c62203a009efa4130ad604/apis/kueue/v1beta1/workload_types.go) | WorkloadSpec.Active 的 JSON 字段为 active；条件 QuotaReserved、Admitted、PodsReady 分开；PodsReady 也可包含已经成功结束的 Pod，不等同当前全部 Pod 正在提供业务 |
| [topology_aware_scheduling.md](https://github.com/kubernetes-sigs/kueue/blob/911a822a49bcfd99c9c62203a009efa4130ad604/site/content/en/docs/concepts/topology_aware_scheduling.md) | 分层节点标签、可调度节点容量、拓扑资源关联、required 与 preferred 区别；启用 Provisioning AdmissionCheck 时存在延迟拓扑分配路径，不能把所有准入写成统一固定顺序 |
| [LICENSE](https://github.com/kubernetes-sigs/kueue/blob/911a822a49bcfd99c9c62203a009efa4130ad604/LICENSE) | 根 Apache-2.0；本次仅引用仓库自有文档/API，第三方与站点资产另计 |

来源内部差异：admission.md 写 `.status.active`，同 commit WorkloadSpec 与 Workload 示例则是 `.spec.active`。后者由 API 结构支持；正式概念正文无需给修改指令，不能照抄前者为现场命令。网页 [v0.19 Admission](https://kueue.sigs.k8s.io/v0.19/docs/concepts/admission/) 保留同一差异。

这些资料支持逻辑配额、准入条件与放置约束的区别，不证明 Kueue 已为任意 NPU 型号配置拓扑或设备插件，也不证明准入后应用通信组已完成初始化。

## Volcano v1.15.0 文档

实际通过版本导航打开 [PodGroup](https://volcano.sh/docs/v1.15.0/concepts/podgroup/) 和 [Gang 插件](https://volcano.sh/docs/v1.15.0/scheduler/plugins/gang/)，页面显示 v1.15.0。只采用最小成员/资源约束、PodGroup phase/conditions 与 gang 的概念边界。不把最低成员数当全部副本数，也不把调度器内部 Ready 与 Kubernetes Pod Ready 或应用 rendezvous 等同。

未固定 Volcano 实现 commit，未核查控制器映射或镜像；文档网页许可未知。因此该来源只作为版本化概念说明，不支持任何默认配置、与 MindCluster 的版本配套或运行保证。

## MindCluster v26.1.1

复用 `src.ascend.mind-cluster-v26.1.1`，commit `44385c13d7b1d87def35f1604e8be4d16de6ca4e`。实际读取：

- [芯片亲和性](https://github.com/Ascend/mind-cluster/blob/44385c13d7b1d87def35f1604e8be4d16de6ca4e/docs/zh/scheduling/04_usage/03_basic_scheduling/01_affinity_scheduling/03_ascend_ai_processor_based_affinity.md)：按产品分节。旧 Atlas 训练系列双 HCCS 环的约束有自己的条件；同页明确 Atlas 800T A2/Atlas 900 A2 PoD 不采用该芯片亲和性调度。A3 的 HiAM 配对、Box16 的环结构另有规则，不能把“卡数足够”当型号无关的放置证明。正式概念文可只保留这一差异，不复制全部型号表。
- [节点亲和性](https://github.com/Ascend/mind-cluster/blob/44385c13d7b1d87def35f1604e8be4d16de6ca4e/docs/zh/scheduling/04_usage/03_basic_scheduling/01_affinity_scheduling/04_node_based_affinity.md)：交换机亲和策略另有任务和配置条件；不能与节点内芯片亲和混为一层。
- [调度流程](https://github.com/Ascend/mind-cluster/blob/44385c13d7b1d87def35f1604e8be4d16de6ca4e/docs/zh/scheduling/04_usage/03_basic_scheduling/02_scheduling_process_of_the_ascend_ai_processor.md)：描述的是华为适配修改的 Volcano；`self-maintain-available-card` 的 true/false 路径不同。调度注解、Pod 绑定、Allocate 与最终设备映射是不同证据点，链接 F11 解释后半段，不重复复制流程。
- [组件 README](https://github.com/Ascend/mind-cluster/blob/44385c13d7b1d87def35f1604e8be4d16de6ca4e/component/ascend-for-volcano/README.md)：仅用于确认插件定位；具体亲和性正文优先使用上述按型号划分的 docs 文件。component README 不自动套用 docs/LICENSE。

这里没有确认 MindCluster 与上游 Volcano v1.15.0 或 Kueue v0.19.0 可以组合部署。前三项 docs 许可沿用同 commit 已登记范围，本次没有复制图片或上游配置文件。

## 可合并的新来源

```yaml
- id: src.kueue.admission-v0.19.0
  title: Kueue v0.19.0 准入、拓扑与 Workload 固定资料
  url: https://github.com/kubernetes-sigs/kueue/tree/911a822a49bcfd99c9c62203a009efa4130ad604
  kind: repository
  registered_at: "2026-09-30"
  revision: v0.19.0; commit 911a822a49bcfd99c9c62203a009efa4130ad604
  license:
    status: partial
    scopes:
      - scope: 固定仓库自有 API 代码与所引文档源码；第三方文件及独立站点资产另计
        identifier: Apache-2.0
        url: https://github.com/kubernetes-sigs/kueue/blob/911a822a49bcfd99c9c62203a009efa4130ad604/LICENSE
    notes: 已读取根许可，仅链接和原创归纳；没有复制图、示例配置或代码，也未核查制品及第三方 notices。
  notes: 实际读取 admission、workload、topology_aware_scheduling 文档与 v1beta1 Workload API；记录 admission 文档的 status.active 与 API spec.active 差异。未部署或运行，不构成与 NPU、MindCluster 或 Volcano 的配套声明。
- id: src.volcano.podgroup-gang-v1.15.0
  title: Volcano v1.15.0 PodGroup 与 Gang 文档
  url: https://volcano.sh/docs/v1.15.0/concepts/podgroup/
  kind: documentation
  registered_at: "2026-09-30"
  revision: v1.15.0 documentation observed 2026-09-30
  license:
    status: unknown
    scopes: []
    notes: 网页版本已核对，未取得足以覆盖该网页的再分发许可；仅链接和原创摘要，不用代码许可证代替。
  notes: 实际打开同版本 PodGroup 与 scheduler/plugins/gang 页面，只用最小组约束和状态概念；未固定二进制或实现，不推断与 MindCluster 的配套。
```

## F12 已采用的内容结构

原创阶段图区分对象接受、排队/配额、准入、节点放置、设备分配、进程启动与应用就绪；各平台对应不同状态，不强制共用同一枚举。用小型资源碎片例解释数量与可放置性的区别，再分开节点间网络层级、节点内设备互联、故障域分散这三类目标。最后给读取状态所需的对象身份、配置、资源账本、约束、事件和应用进度字段。

保留未知：目标机型、驱动、设备插件、调度器扩展、版本、拓扑标签可信度、配置与并发资源变化。没有集群实测不妨碍概念交付，但不能把图中的每个箭头写成已经验证的现场能力。
