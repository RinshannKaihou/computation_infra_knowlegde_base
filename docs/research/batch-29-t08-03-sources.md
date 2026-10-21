# 第二十九批 T08-03 来源记录

任务：T08-03（隔离、重试预算、降级与恢复选择；**new** `knowledge/08-reliability/mitigation-and-recovery-principles.md`，主题 08.5/08.1）。取证轮次：主会话作者角色首轮（2026-10-21；批内前置 T08-01/T08-02 已交付）。

## 新增来源与主张定位

| 主张 | 登记 ID | 精确位置 | 支持范围 |
|---|---|---|---|
| 纯指数退避仍同步聚簇（"there are still clusters of calls"、竞争未实质下降）；Full Jitter（0 到 min(cap, base·2^attempt) 均匀随机）/Equal Jitter/Decorrelated Jitter 定义；实验结论（无 jitter 最差、100 竞争客户端调用减半以上、full 与 decorrelated 取舍）；jittered backoff 应为远程客户端标准做法 | src.aws.backoff-jitter-2015（**本轮新增**） | [Exponential Backoff and Jitter](https://aws.amazon.com/blogs/architecture/exponential-backoff-and-jitter/)（Marc Brooker，2015-03-04；2026-10-21 WebFetch 两轮核对，含 2023 更新注） | 退避/jitter 小节；未取最大重试次数等数值建议（原文未给） |

## 复用来源与主张定位

| 主张 | 登记 ID | 精确位置 | 支持范围 |
|---|---|---|---|
| 随机指数退避、每请求重试上限、服务级重试预算示例、可重试/不可重试区分、deadline 传播与取消传播 | src.google.sre-cascading-failures | [Addressing Cascading Failures](https://sre.google/sre-book/addressing-cascading-failures/)（Batch 28 已核） | 重试五条边界之 1/2/4 |
| 每请求最多 3 次尝试、客户端 10% 重试比例预算、仅在紧邻上一层重试 | src.google.sre-handling-overload | [Handling Overload](https://sre.google/sre-book/handling-overload/)（Batch 28 已核） | 重试预算三件套的示例数值（标为 SRE 示例非推荐） |
| 错误预算与 SLO 驱动发布冻结决策 | src.google.sre-implementing-slos | [Implementing SLOs](https://sre.google/workbook/implementing-slos/)（2026-09-29 已核） | 故障预算小节 |
| 五类簇级断路器与 max_retries 并发上限；推荐 retry budgets 替代静态重试上限 | src.envoy.circuit-breaking-arch-latest-2026-10-21 | [Envoy Circuit Breaking](https://www.envoyproxy.io/docs/envoy/latest/intro/arch_overview/upstream/circuit_breaking)（Batch 28 已核，latest 可变页） | 预算三件套的服务级示例 |
| Job backoffLimit 默认 6＋指数退避 | src.kubernetes.job-lifecycle-v1-32 | [Job 概念页](https://kubernetes.io/docs/concepts/workloads/controllers/job/)（v1.32 快照，Batch 22 已核） | 训练重启预算段 |
| 容器重启退避 10s 起封顶 300s、运行 10 分钟重置 | src.kubernetes.pod-lifecycle-v1-32 | [Pod 生命周期页](https://kubernetes.io/docs/concepts/workloads/pods/pod-lifecycle/)（v1.32 快照，Batch 28 已核） | 同上 |
| torchrun CLI max-restarts 默认 0 与 WorkerSpec API 默认 3 须区分；elastic 只重建进程组、状态恢复是应用责任；checkpoint 是恢复前提 | src.pytorch.elastic-2.6 | [PyTorch 2.6 elastic/run](https://docs.pytorch.org/docs/2.6/elastic/run.html)（2026-10-08 核对，B11-C03 修订后口径） | 恢复选择表训练行 |
| 副本机制支持缩容续训与 UCE 在线修复；外部组件约束 | src.ascend.mindspeed-llm-ha-v2.2.0 | [high_availability.md](https://github.com/Ascend/MindSpeed-LLM/blob/53f3639c3da9c000a187c44cc0c08d55026ddded/docs/pytorch/features/high_availability.md)（v2.2.0 tag；2026-10-08 补核） | 恢复选择表训练行（Ascend 样板） |
| 流式输出重试边界、KV 重算、副本切换与回滚验证 | 07 域既有正文 | [pd-disaggregation](../../knowledge/07-inference/pd-disaggregation.md)/[release-and-recovery](../../knowledge/07-inference/release-and-recovery.md)/[execution-and-kv-cache](../../knowledge/07-inference/execution-and-kv-cache.md)/[routing-and-flow-control](../../knowledge/07-inference/routing-and-flow-control.md) | 恢复选择与隔离小节的机制引用 |

## 本文原创部分

六字段前置表、按四维目标的选择表、重试五条边界的组织、降级三层表、恢复选择五行表、有限故障对照设计五步、授权边界段。所有阈值留白，未设任何推荐数值。

## unknown 清单

1. 本文全部"推荐配置"留空：重试次数/比例/退避基数/预算比例均须按目标环境设定，来源只提供机制与示例值（已标"示例非推荐"）。
2. 训练侧"含恢复损失的可用产出折算"具体算法未定义（T08-06 可靠性统计范围）；本文只用符号 a'。
3. 故障对照设计的统计方法（样本量、显著性）属 08.7/30 批，本文只给设计骨架。
4. vLLM 侧重试/预取策略未在本轮重新取证（07 域既有登记未覆盖引擎内部 retry 参数），正文引用限于 KV 重算/副本切换机制层。
