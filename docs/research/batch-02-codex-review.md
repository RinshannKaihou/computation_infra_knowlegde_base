# 第二批审阅记录（用户授权由 Codex 替代 astra）

审阅日期：2026-09-30。审阅者：本会话 Codex 主助手；用户明确授权本助手替代 astra 补审。没有派发 gpt-6-astra/xhigh 或子代理。授权、版本清单和去重统计见[四批汇总](batch-01-02-08-09-codex-review-summary.md)。

**最新结论：修订后定向复核通过，发现全部关闭。** 本批 B02-C01 已关闭；batch 08 的同一依赖发现同步关闭。 关闭依据与最终文件身份见[定向复核记录](batch-02-08-09-codex-recheck.md)。

## 初审记录（历史）

以下结论、发现位置和开放状态保留为初审快照；最终状态以文末定向复核为准。

**结论：审阅完成，暂不通过；1 项 P2 开放。** 问题同时影响 batch 08 的数据饥饿流程，按同一个发现 ID 跟踪。未修改知识正文，没有设备或集群执行。

## 审阅对象与实际来源核对

| 对象 | 本次核对 |
|---|---|
| [计算节点资源与拓扑参考](../../knowledge/01-hardware/resource-topology.md)（F03） | 重新读取 [Atlas 800T A2 产品页](https://e.huawei.com/cn/products/computing/ascend/atlas-800t-a2)与 [DGX H100/H200 Introduction](https://docs.nvidia.com/dgx/dgxh100-user-guide/introduction-to-dgxh100.html)；产品组件不能替代目标节点 BOM、枚举或设备互联证据 |
| [训练数据供给路径与等待](../../knowledge/04-data-storage/training-data-path.md)（F09） | PyTorch 2.6 [DataLoader 文档](https://docs.pytorch.org/docs/2.6/data.html)、[CUDA 语义](https://docs.pytorch.org/docs/2.6/notes/cuda.html)，以及 v2.6.0 固定 DataLoader 源码；[MLPerf Storage v2.0 Submission_guidelines.md](https://github.com/mlcommons/storage/blob/7e71ca162d8f9e7ae4b5b698d7d79b0883817f25/Submission_guidelines.md) 的模拟消费与内存边界 |
| [从物理设备到容器资源的状态链](../../knowledge/05-cluster-platform/device-resource-chain.md)（F11） | [Kubernetes v1.32 Device Plugins](https://v1-32.docs.kubernetes.io/docs/concepts/extend-kubernetes/compute-storage-net/device-plugins/)；MindCluster 固定 commit `44385c13d7b1d87def35f1604e8be4d16de6ca4e` 的[组件说明](https://github.com/Ascend/mind-cluster/blob/44385c13d7b1d87def35f1604e8be4d16de6ca4e/docs/en/scheduling/introduction/01_component_description.md)与 [plugin.go](https://github.com/Ascend/mind-cluster/blob/44385c13d7b1d87def35f1604e8be4d16de6ca4e/component/ascend-device-plugin/pkg/server/plugin.go) |
| [昇腾档案](../../knowledge/02-software-stack/ascend-documented-profile.md)（E01 的 CANN 补充） | 用浏览器加载[快速安装](https://www.hiascend.com/document/detail/zh/CANNCommunityEdition/83RC1/softwareinst/instg/instg_quick.html?Mode=PmIns&InstallType=netconda&OS=openEuler&Software=cannToolKit)与[安装 NPU 驱动和固件](https://www.hiascend.com/document/detail/zh/CANNCommunityEdition/83RC1/softwareinst/instg/instg_0005.html?Mode=PmIns&InstallType=netconda&OS=openEuler&Software=cannToolKit)的目标正文，确认驱动/固件前提、物理机职责与 `8.3.RCX` 页头；没有执行页面命令 |

另读取[本批来源审计](batch-02-source-audit.md)、三份专题记录、来源登记和导航。已有明示的 Atlas 拓扑、NPU 传输语义与目标集群未知项保留，不因资料缺失而要求作者补造内容。

## B02-C01 · P2 · 队列深度的方向判断缺少“可按序消费”的限定

状态：**开放**。

位置：[training-data-path.md](../../knowledge/04-data-storage/training-data-path.md) 第 73 行、105 行；同样表述传播到 [data-starvation-triage.md](../../knowledge/04-data-storage/data-starvation-triage.md) 第 59、70 行（batch 08）。

正文用“消费时队列为空”判断上游瓶颈，并用“队列长期满”判断消费者或更下游更慢，却没有区分任务索引队列、worker 结果队列、pin-memory 阶段、乱序缓存与实际可返回给训练的 batch。要求填写采集点有帮助，但尚不足以支持这里不带条件的方向结论。

PyTorch 2.6 默认按序返回。固定源码 [`dataloader.py` L1449–1480](https://github.com/pytorch/pytorch/blob/1eba9b3aa3c43f86f4a2c807ac8e12c4a7767340/torch/utils/data/dataloader.py#L1449-L1480) 先查 `_rcvd_idx` 对应 batch；后续完成的结果可以留在 `_task_info`，等待前面的结果。因此“已产出很多 batch”和“下一 batch 可消费”可以分叉。若把预取或缓冲的占用读作消费队列已满，会把慢 worker/顺序等待误归给消费者；若只看 IPC 队列为空，又会漏掉已移入中间缓存的数据。

**建议修订：** 将方向推理限定到已定义、可立即按当前顺序消费的 batch 队列；其他队列深度仅作线索。增加“按序返回的队首等待”支路，用 batch/task ID、worker 开始/完成时间、结果接收与交付时间区分供给不足、乱序等待、pinning 与消费背压。不要把关闭 `in_order` 写成通用修复。

**关闭条件：** 基础条目和 batch 08 流程同步修订；能正确解释“早期 batch 未完成、多个后续 batch 已完成，训练仍等待”的源码级反例，并保留真实队列语义未知时的 `unknown`。该反例来自代码分析，本次没有运行 DataLoader 性能实验。

## 已核对而未形成发现的部分

- 主机与设备内存、控制关系与物理互联的区分合理；两份产品资料均没有被当作目标环境实测。
- MLPerf Storage 使用模拟消费节奏，不能代表完整解码、预处理或 GPU/NPU 执行；正文保留了这个边界。
- Device Plugin 健康上报、分配记录、容器访问和框架初始化没有被合并成同一种成功。Kubernetes 的不健康设备、既有分配与 allocatable 口径符合所引文档。
- CANN 补充只证明当前安装职责；精确历史 HDK 和整栈支持仍未知。

## 初审结束状态（历史）

本批新增 1 项 P2、0 项 P3，尚未关闭；结构与导航检查结果见[汇总](batch-01-02-08-09-codex-review-summary.md)。本次完成审阅，不把来源检查或生成目录视作问题关闭。

## 定向复核最终状态（2026-09-30）

本批 B02-C01 已关闭；batch 08 的同一依赖发现同步关闭。 原关闭条件经实际正文和固定来源核对均已满足；少量表述补正与复核后 SHA-256 见[定向复核记录](batch-02-08-09-codex-recheck.md)。本批在原审阅范围内通过，没有待复核项；正文仍为 `draft / source_checked`，未做环境执行。
