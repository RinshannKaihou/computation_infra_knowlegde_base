---
id: inference.ascend-inference-tail-latency-source-case
title: 昇腾推理长尾来源案例
type: case
domain: inference
status: draft
platforms: [ascend]
source_refs:
  - src.vllm-ascend.issue-17443
updated_at: "2026-09-30"
summary: 从一个仍未闭环的 A3 长上下文报告分析版本、长度、客户端口径和失败样本如何影响回归归因。
related_ids:
  - inference.latency-metrics
  - reliability.evidence-and-hypotheses
applicability:
  environment_refs: []
  notes: 外部报告的 A3、GLM-5.3-Flash W8A8、P/D 分离和 2026 年 nightly 环境；不是本库 v0.14.0rc1 样板。具体制品、驱动配套和负载未在本地核验。
verification:
  status: source_checked
  evidence_refs:
    - src.vllm-ascend.issue-17443
  notes: 核对 Issue 正文与页面状态，并通过 GitHub 连接器取得空评论列表；未验证报告数字、根因或修复，未开展本地复现。
---

# 昇腾推理长尾来源案例

## 来源和已知事实

本页整理 [vLLM Ascend #17443](https://github.com/vllm-project/vllm-ascend/issues/17443)。报告于 2026-09-24 提交，2026-09-30 读取时为 Open；GitHub 连接器在该次读取返回空评论列表，未取得修复链。下表均为报告者陈述，不是本库测量。

| 项目 | 报告中的必要条件 |
|---|---|
| 部署 | 两节点 A3，各 16 个 NPU；GLM-5.3-Flash W8A8，1P1D，含 KV 连接器和代理 |
| 软件标识 | 测试树 `18d161d76`；当前 HEAD 含测试之后的补丁，pip 元数据也被报告为滞后；不能只靠版本字符串重建现场 |
| 对照时间线 | 9 月 22 日在旧树 `d6481c7ae` 测较短输入，随后切树；9 月 23 日测更长输入与混合负载；原文未注明这些本地时间的时区 |
| 观测 | ais_bench 3.1.0 流式 chat；混合负载报告 128 次请求中 125 次成功、3 次失败，TTFT p99 为 172.47 秒 |
| 原作者判断 | 怀疑版本回归，同时承认跨版本输入长度不同，需要同长度 A/B；没有报告已完成该对照 |

完整环境、启动条件和原始表格见 [Issue 的 environment、benchmark 与 changes 三节](https://github.com/vllm-project/vllm-ascend/issues/17443)。报告没有提供可复核的制品摘要、完整启动脚本或逐请求证据；公开陈述不能替代这些材料。

## 本库如何评估证据

以下是本库的方法分析，**不是维护者给出的根因**。

| 假设或推论 | 现有证据的作用 | 下一步所需证据 |
|---|---|---|
| 更换代码造成性能回归 | 时间相关性提出候选，但输入长度也变化 | 相同请求、到达过程、缓存状态与资源下的两版本对照；完整代码与制品身份 |
| 首输出变慢来自纯 prefill 计算 | 客户端首输出前包含多个阶段，尚未隔离 | prefill 调度、执行、KV 转移、decode 接纳、返回路径的对应事件 |
| 最短 TTFT 代表无排队下限 | 最快样本仍可能等待，无法据此排除排队 | 对应请求的真实入队/调度时间和其他角色等待 |
| 平均 TPOT 稳定证明 decode 健康 | 均值不说明尾部与失败请求 | 请求级 TPOT/ITL、长停顿与失败分类；保留输出长度分层 |
| 总吞吐下降证明某一角色容量下降 | 不同负载、失败过滤和窗口可能改变比值 | 固定负载、成功/失败规则与窗口，关联角色级队列和持续进展 |

尤其不能把 `input_tokens / client_TTFT` 改名为 kernel prefill 吞吐。客户端和服务端有各自起止事件；当前 ais_bench 的具体聚合实现尚未核查，也不能直接套用本库 [vLLM 指标样板](latency-metrics.md)的过滤规则。

## 处理状态、可复用经验与缺口

本页没有可确认的修复结果。原文提出的升级范围、补丁或调度方向只是候选，不能写成执行处方。相关 Issue 的链接也不构成相同根因证明。

可复用的是调查顺序：保留实际测试树；固定输入与负载再比较版本；为每个“慢”标明观察者与窗口；把失败率和尾部分布一起交付。下一步是补齐可复核的同负载 A/B、逐请求时序、失败原因以及后续维护者结论。取得这些证据前，根因、影响范围和首个修复版本均未知。
