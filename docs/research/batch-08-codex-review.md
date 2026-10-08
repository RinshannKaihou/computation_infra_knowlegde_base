# 第八批审阅记录（用户授权由 Codex 替代 astra）

审阅日期：2026-09-30。审阅者：本会话 Codex 主助手；用户明确授权本助手替代 astra 补审。没有派发 gpt-6-astra/xhigh 或子代理。此报告与原[同环境子代理替代复查](batch-08-substitute-review.md)是两次不同的审阅。

**最新结论：修订后定向复核通过，发现全部关闭。** 本批 B08-C01、B08-C02、B08-C03 及继承的 B02-C01 均已关闭；B08-C01 对 batch 09 的影响同步关闭。 关闭依据与最终文件身份见[定向复核记录](batch-02-08-09-codex-recheck.md)。

## 初审记录（历史）

以下结论、发现位置和开放状态保留为初审快照；最终状态以文末定向复核为准。

**结论：审阅完成，暂不通过。** 本批新增 1 项 P2、2 项 P3；还受到 batch 02 的 1 项 P2 影响。全部开放，去重统计与版本清单见[四批汇总](batch-01-02-08-09-codex-review-summary.md)。未修改知识正文或执行硬件实验。

## 审阅对象与证据

- [昇腾 NPU 内存与 OOM 证据](../../knowledge/02-software-stack/ascend-memory-oom-evidence.md)：逐段对照 TorchNPU 固定 commit `bc51ab84cc6f35c77aab1c59886e0ea43681a317` 的 caching allocator、workspace allocator、NpuUtils 和相关内存接口；读取 CANN 8.2.RC1.alpha001 [内存管理](https://www.hiascend.com/document/detail/zh/CANNCommunityEdition/82RC1alpha001/API/appdevgapi/aclcppdevg_03_0094.html)及 [aclrtMalloc](https://www.hiascend.com/document/detail/zh/CANNCommunityEdition/82RC1alpha001/API/appdevgapi/aclcppdevg_03_0095.html)页面。
- [训练数据加载饥饿诊断指南](../../knowledge/04-data-storage/data-starvation-triage.md)：对照 PyTorch 2.6 DataLoader 文档和固定 `dataloader.py` 的预取、超时、worker 失败、取数与按序返回路径。
- [空闲设备但作业等待诊断指南](../../knowledge/05-cluster-platform/idle-resource-job-waiting-triage.md)：核对 Kueue 固定 commit `911a822a49bcfd99c9c62203a009efa4130ad604` 的 troubleshooting_jobs、topology_aware_scheduling、Workload API 和 scheduler；Kubernetes、MindCluster 设备链作为已核对的关联边界。

同时读取[来源审计](batch-08-source-audit.md)、三份专题研究记录、旧替代复查、元数据、来源登记和导航。没有重审全部 Kueue 控制器或全部 TorchNPU 文件；没有把源码存在视为设备版本支持。

## B08-C01 · P2 · 同一 OOM 错误码还可由进程内存额度检查产生

状态：**开放**。

位置：[ascend-memory-oom-evidence.md](../../knowledge/02-software-stack/ascend-memory-oom-evidence.md) 第 62–69 行。关联影响：batch 09 [推理 OOM 流程](../../knowledge/07-inference/ascend-inference-oom-triage.md)对本条目的依赖。

正文把 `ACL_ERROR_RT_MEMORY_ALLOCATION` 称为“底层错误”，并摘录省掉 `allowed` 的 OOM 文案，遗漏了重要的进程额度分支。固定源码 [`alloc_block` L2692–2694](https://github.com/Ascend/pytorch/blob/bc51ab84cc6f35c77aab1c59886e0ea43681a317/torch_npu/csrc/core/npu/NPUCachingAllocator.cpp#L2692-L2694) 在 `total_allocated_memory + size` 超过 `allowed_memory_maximum` 时，自己设置该码并返回失败，此时还没有调用运行时申请这次内存。

额度来自 [`setMemoryFraction` L1717–1724](https://github.com/Ascend/pytorch/blob/bc51ab84cc6f35c77aab1c59886e0ea43681a317/torch_npu/csrc/core/npu/NPUCachingAllocator.cpp#L1717-L1724)；OOM 分支在 [L1391–1409](https://github.com/Ascend/pytorch/blob/bc51ab84cc6f35c77aab1c59886e0ea43681a317/torch_npu/csrc/core/npu/NPUCachingAllocator.cpp#L1391-L1409) 生成 `allowed` 并改变 observer 的容量参数，[L1429–1436](https://github.com/Ascend/pytorch/blob/bc51ab84cc6f35c77aab1c59886e0ea43681a317/torch_npu/csrc/core/npu/NPUCachingAllocator.cpp#L1429-L1436) 将它加入报错。设备仍有空闲量也可能触发这种 OOM；不能从该码认定是运行时分配失败或碎片。

**建议修订：** 区分“分配器中的错误状态”与实际 ACL 调用返回；补上 `set_per_process_memory_fraction`/`allowed` 分支和可选日志字段。推理流程遇到这类张量 OOM 时先查额度和实际生效配置，再与物理空闲、reserved、active 及请求大小对照；不自动解除额度。

**关闭条件：** 基础机制、报错摘录和推理流程一致；能从源码解释“设备仍有空闲但进程额度已到上限”的情形，observer 容量字段也不再默认解释为物理总量。没有真实故障复现时只关闭文档缺陷，不新增 `reproduced`。

## B08-C02 · P3 · GC 阈值的生效条件和触发时机缺失

状态：**开放**。位置：[ascend-memory-oom-evidence.md](../../knowledge/02-software-stack/ascend-memory-oom-evidence.md) 第 87 行。

“分配重试时的回收阈值”没有覆盖固定快照的实际条件：缓存搜索失败后，只有 `set_fraction` 为真且 threshold 大于零才调用 GC，而且发生在申请新块之前（[`NPUCachingAllocator.cpp` L1353–1369](https://github.com/Ascend/pytorch/blob/bc51ab84cc6f35c77aab1c59886e0ea43681a317/torch_npu/csrc/core/npu/NPUCachingAllocator.cpp#L1353-L1369)）。回收门槛是 threshold 乘 `allowed_memory_maximum`（[L2624–2629](https://github.com/Ascend/pytorch/blob/bc51ab84cc6f35c77aab1c59886e0ea43681a317/torch_npu/csrc/core/npu/NPUCachingAllocator.cpp#L2624-L2629)）。只配置该选项而没有设置 fraction，并不启用这条主动 GC 路径。

**建议及关闭条件：** 表格区分解析范围与运行条件，补上 fraction、额度分母及“缓存未命中、申请新块前”的时机；不能将其他释放缓存重试路径都归到这个阈值。无需为文档修订执行设备调参。

## B08-C03 · P3 · conditions 为空不能直接反推 StrictFIFO 队首阻塞

状态：**开放**。位置：[idle-resource-job-waiting-triage.md](../../knowledge/05-cluster-platform/idle-resource-job-waiting-triage.md) 第 59 行；第 49 行的证据解释应保持一致。

来源说的是“使用 StrictFIFO、尚未尝试准入的 Workload，status **可能**没有 condition”（[`troubleshooting_jobs.md` L243–248](https://github.com/kubernetes-sigs/kueue/blob/911a822a49bcfd99c9c62203a009efa4130ad604/site/content/en/docs/tasks/troubleshooting/troubleshooting_jobs.md#L243-L248)）。正文将其反向写成空 conditions 直接指向 StrictFIFO/队首，并认为等待层已经定位；来源不支持这种充分条件。空列表本身也没有证明控制器已经处理这个对象。

**建议及关闭条件：** 先核对实际 `queueingStrategy`、对象创建与控制器处理时间、队列和队首状态；满足这些证据时将“尚未尝试”列为候选解释。只有空列表时保持等待原因 `unknown`，并检查控制器接管/状态尚未更新；不能因空列表直接改走队首处置。

## 从基础批次继承的发现

[B02-C01](batch-02-codex-review.md)：数据饥饿流程第 59、70 行也未区分中间队列占用与可按序消费 batch。按同一问题跟踪，不重复计算新增发现；基础条目与流程均修订后才能关闭。

## 已核对的正确边界与限制

- allocated/reserved、workspace 独立账户、清缓存重试与 1EB 防御分支均有固定代码支持；内置碎片提示没有被当作根因证明。
- NPU 异步报错栈的精确错位结论被明确标为机制推断，保留 CANN 证据缺口，未冒充已有实测。
- Kueue 配额、准入检查、TAS 与 kube-scheduler 的职责区分合理；细分 reason 的默认关闭特性门已有明确限制。
- 原同环境复查关闭的 4 项 P3 是历史记录；本次新增发现不因那次“已关闭”而自动关闭。结构检查和构建见[汇总](batch-01-02-08-09-codex-review-summary.md)。

## 定向复核最终状态（2026-09-30）

本批 B08-C01、B08-C02、B08-C03 及继承的 B02-C01 均已关闭；B08-C01 对 batch 09 的影响同步关闭。 原关闭条件经实际正文和固定来源核对均已满足；少量表述补正与复核后 SHA-256 见[定向复核记录](batch-02-08-09-codex-recheck.md)。本批在原审阅范围内通过，没有待复核项；正文仍为 `draft / source_checked`，未做环境执行。
