---
id: reliability.diagnostic-evaluation-fixtures
type: reference
domain: reliability
status: draft
title: 诊断评测公开题组
platforms: [generic]
source_refs:
  - src.pytorch.dcp-issue-164257
  - src.pytorch.dcp-fix-edd8d35
  - src.pytorch.issue-118369
  - src.vllm-ascend.issue-2557
  - src.meta.oct4-2021-postmortem
  - src.cloudflare.oct-2021-facebook-outage
  - src.arxiv.sdc-detection-wild-2203
  - src.acl.sdc-llm-training-2502
  - src.arxiv.llama3-infrastructure
  - src.ascend.faultdiag-v26.1.1
updated_at: "2026-10-21"
summary: 九条公开教学/检索回归题组：固定输入（来自已登记公开证据）、证据 oracle（精确来源锚点）、允许 unknown 的判据与七维 rubric；覆盖训练/推理/硬件/通信/存储/平台与无法判定样例；一条合成夹具显式标注。本题组只作公开教学与检索回归，不是独立 holdout（独立集由 V12 外置管理）。
related_ids:
  - reliability.diagnostic-evaluation-method
  - reliability.evidence-and-hypotheses
  - reliability.postmortem-and-knowledge-update
verification:
  status: source_checked
  evidence_refs:
    - src.pytorch.dcp-issue-164257
    - src.pytorch.issue-118369
    - src.vllm-ascend.issue-2557
    - src.meta.oct4-2021-postmortem
    - src.arxiv.sdc-detection-wild-2203
    - src.acl.sdc-llm-training-2502
    - src.arxiv.llama3-infrastructure
  notes: "每条题目的输入与 oracle 均取自本库已登记来源的固定观察（Issue 正文/复盘/论文固定节/固定 tag 文档），逐条在正文内给出锚点；未运行任何评测，无分数。"
---

# 诊断评测公开题组

本题组配合[诊断评测方法规范](diagnostic-evaluation-method.md)使用。**角色声明：这些条目进入知识库后属于 train/dev 侧的公开教学与检索回归材料，不是独立 holdout**；独立评测集由 [V12 工作包](../../plans/validation-backlog.yaml)外置获取与管理。

每条题目统一格式：**输入**（固定证据片段与问题）→ **证据 oracle**（精确来源锚点，判分依据）→ **判据**（什么算答对；允许 unknown 的写明何时应弃答）→ **rubric 侧重**（七维中该题重点考察的维度）。七维定义见方法规范第四节。

## 题组

### PTF-01 训练·checkpoint 恢复状态语义（证据强度 A）

- **输入**：PyTorch 2.8.0 单进程 DCP 场景：未初始化 bias 的 optimizer state，`strict=False` 加载仍抛 KeyError；报告者另给出“创建新对象却加载旧对象”的复现 quirk。问：故障在哪一层（DCP 机制/调用方/版本组合），下一项最有区分力的检查是什么？
- **证据 oracle**：[Issue #164257](https://github.com/pytorch/pytorch/issues/164257) 正文与环境（macOS 26/M3 CPU、Python 3.13.1）；修复对照[固定 commit edd8d35](https://github.com/pytorch/pytorch/commit/edd8d356b6d9a00cfa34fa323578e5cf1c7e0463)（缺失 optimizer FQN 的存在性检查，strict 两分支）。
- **判据**：正确路径＝识别为“缺失 FQN 的存在性检查”类机制问题而非数据损坏；给出“用固定版本 state_dict 路径对照”类检查。**边界**：首个含修复的发行版本未知（登记口径），据此答“已随某版本修复”不得分。
- **rubric 侧重**：假设区分力、事实/平台边界。

### PTF-02 通信·rank 缺席与 watchdog 超时（证据强度 C→A 部分）

- **输入**：8 rank 训练，rank 1–7 在 SeqNum 880 的 Broadcast 上 watchdog 超时；rank 0 无同类日志且利用率快照为 0%。维护者未确认根因，Issue 以 stale 关闭。问：这是 7 起独立故障还是 1 起故障的表现？候选假设排序与下一项检查？
- **证据 oracle**：[Issue #118369](https://github.com/pytorch/pytorch/issues/118369)（opened 2024-01-26；2026-05-05 stale 关闭、无修复链接）；[集合通信与 rank 进度](../03-communication/collectives-and-rank-progress.md)的缺席参与者机制。
- **判据**：正确方向＝“单点缺席经同步屏障表现为全体超时”（传播≠多起）；下一项检查应指向 rank 0 侧证据（主机状态/进程存活）。**边界**：根因未确认（stale≠修复），答案保持 suspected；断言“rank 0 宕机为 confirmed”不得分。
- **rubric 侧重**：假设区分力、abstention（部分）。

### PTF-03 推理·平台 容器内设备可见性（证据强度 A）

- **输入**：vLLM Ascend on K8s：容器内 `npu-smi` 显示物理 ID 0/3/4/7，torch_npu 按逻辑范围 0–3 初始化报错。问：断链在四层链（物理存在→驱动可见→平台可分配→容器可用）的哪一层？
- **证据 oracle**：[vllm-ascend Issue #2557](https://github.com/vllm-project/vllm-ascend/issues/2557) 正文、关键评论与 2025-12-18 completed close；[从物理设备到容器资源的状态链](../05-cluster-platform/device-resource-chain.md)。
- **判据**：正确＝区分“物理 ID vs 逻辑 ID”映射层；给出映射核对检查。**边界**：登记口径明确“没有同现场合入后复验”——据此宣称“该场景已全面修复”不得分，且不得把该 Mooncake 场景外推到所有框架。
- **rubric 侧重**：事实/平台边界、引用精度。

### PTF-04 平台·网络 共同原因与冗余独立性（证据强度 B）

- **输入**：2021-10-04：多服务同时不可用；外部观测者看到全球多地对该平台域名解析失败、BGP 撤路由；运营方复盘称一条维护期配置命令在骨干路由器全量下发且撤销未生效。问：为什么“多服务同时故障”应优先怀疑共同原因而非多起并发独立故障？该事件中哪些冗余没有起到预期作用？
- **证据 oracle**：[Meta 复盘](https://engineering.fb.com/2021/10/05/networking-traffic/outage-details/)（运营方一手）＋[Cloudflare 观测](https://blog.cloudflare.com/october-2021-facebook-outage/)（外部观测），整理见[相关故障来源案例](correlated-failure-source-case.md)。
- **判据**：正确＝用“共享配置下发平面/控制通道”解释同时性；指出 DNS 服务器离线导致日常维护通道同时不可用的耦合。时间线须区分**事件发生时刻**（命令下发）与**外部发现时刻**（全球解析失败可观测）。
- **rubric 侧重**：假设区分力、事实/平台边界（时间线）。

### PTF-05 硬件·正确性 应用侧 SDC 症状识别（证据强度 A）

- **输入**：Spark 作业：`(1.1)^53` 的聚合结果为 0（正确 156.24），下游数据库缺行；涉事机器系统事件与内核日志全部干净。问：候选原因集（软件 bug/数据问题/硬件 SDC）如何排序？为什么日志干净不是“无硬件问题”的证据？
- **证据 oracle**：[arXiv:2203.08989 §1](https://arxiv.org/abs/2203.08989)（含对前作的引用与量化例子）；[静默错误与计算完整性判定](silent-errors-and-integrity.md)的判定流程。
- **判据**：正确＝SDC 进入候选、日志干净不排除硬件、提出最小 reproducer/换机对照类检查；**先走容差与数值噪声扣除**再谈硬件。
- **rubric 侧重**：假设区分力、下一项检查。

### PTF-06 硬件·检测方法 ABFT 假阴性判读（证据强度 A）

- **输入**：15 台经 fleet 管理压力测试筛出的不健康节点上训练模型，float32 的校验和矩阵乘（ABFT）几乎不触发（仅 1 台被频繁标出），而逐元素比对显示持续存在不一致。问：ABFT 没报＝没有 SDC 吗？给出三条可能解释。
- **证据 oracle**：[arXiv:2502.12340 附录 D](https://arxiv.org/abs/2502.12340)（D.2 结果、D.3 三条解释：扰动落在浮点误差界内/开销降低利用率从而降低发生率/SDC 可能在矩阵乘之外；D.4 bf16 假阳性）。
- **判据**：正确＝“检测方法未触发≠缺陷不存在”；三条解释至少给出两条。
- **rubric 侧重**：事实/平台边界（检测覆盖）、假设区分力。

### PTF-07 硬件·统计判读 中断归因口径（证据强度 A）

- **输入**：某 405B 预训练 54 天快照：466 次中断中 419 次意外；论文称约 78% 归因“已确认或疑似的硬件问题”，GPU 类合计 58.7%，SDC 单独 1.4%。问：从这些数字能推出“任意 16K 卡集群 SDC 导致中断的概率≈1.4%”吗？“confirmed or suspected”这个口径对数字的含义是什么？
- **证据 oracle**：[arXiv:2407.21783 §2.2 与 Table 5](https://arxiv.org/abs/2407.21783)。
- **判据**：正确＝不能外推（平台/规模/归因口径特定；“suspected”含未证实归因）；正确使用该数字的方式是作为同型集群的参照区间而非阈值。
- **rubric 侧重**：事实/平台边界、引用精度。

### PTF-08 无法判定样例（证据强度 U）

- **输入**：同上快照 Table 5 中“NCCL Watchdog Timeouts”归为 **Unknown** 类（1.7%）。一次本地集群复现“NCCL watchdog 超时导致作业重启”，手头只有超时日志与重启记录，无逐 rank 进度证据。问：根因最可能是什么？
- **证据 oracle**：Table 5 的 Unknown 归类本身；[证据与假设](evidence-and-hypotheses.md)的假设三分。
- **判据**：**正确答案是弃答**——列出能把候选（慢 rank/链路降级/软件缺陷/其他）区分开的下一项证据（逐 rank 时间线、链路计数器、复现窗口），并说明每项证据分别支持/反驳哪个候选。任何给出单一确定根因的回答不得分。
- **rubric 侧重**：abstention、下一项检查。

### PTF-09 合成夹具·诊断输出到候选假设（合成，显式标注）

> **本条为合成教学夹具**：输入取自工具文档的固定示例输出，不是任何真实事故；只验证“规则输出→候选假设”的转换规则，不证明任何故障发生率或工具命中率。

- **输入**：Ascend FaultDiag 诊断报告（固定 tag v26.1.1 文档示例）：根因节点 worker-0 device-2、首错节点 worker-1 device-2、现象“RoCE 重传超次（ERROR CQE）”、传播链“Link Down → RDMA 通信重传超次 → notify wait 超时”。问：这份报告能支持哪些结论、不能支持哪些？
- **证据 oracle**：[FaultDiag 04_fault_diagnosis.md 固定 commit](https://github.com/Ascend/mind-cluster/blob/44385c13d7b1d87def35f1604e8be4d16de6ca4e/docs/zh/faultdiag/ascend-faultdiag/05_usage/04_fault_diagnosis.md)（报告字段语义）。
- **判据**：能支持＝“存在规则命中的候选链，建议沿传播链采集交换机日志/物理层证据”；不能支持＝“根因已确认是光模块故障”（规则匹配≠根因，见[事故复盘](postmortem-and-knowledge-update.md)与[静默错误](silent-errors-and-integrity.md)平台证据表）。
- **rubric 侧重**：假设区分力、事实/平台边界。

## 使用与维护规则

1. **判分**：按方法规范第四节 rubric 逐维打分；每题的“判据”栏是该题主判据，边界句（“据此宣称 X 不得分”）是负面清单。
2. **检索回归**：本题组另用于验证知识库导航——从每题的问题出发应能在三跳内定位到“证据 oracle”栏指向的正文/来源；正文重构后跑一遍即回归。
3. **更新**：上游来源变化（Issue 补充评论、论文出新版）按[事故复盘、来源更新与知识维护](postmortem-and-knowledge-update.md)第三节的触发规则复核本题；题目修改视为换卷。
4. **不声称**：本题组不产生“诊断准确率”类总体分数；任何总体结论只能来自 V12 外置评测。

## 来源核对范围

各条目的证据 oracle 均为本库已登记来源，逐条锚点见正文；三份 Issue 的登记口径（含 stale 关闭、completed close、无同现场复验等边界）见 sources/registry.yaml 对应条目；Meta/Cloudflare 复盘为 Batch 29 全文核读；论文类为 Batch 30 全文核读（见[静默错误](silent-errors-and-integrity.md)与[可靠性统计](reliability-metrics-and-recovery-loss.md)的来源核对节）。逐条主张与读取范围见[第三十批 T08-08 来源记录](../../docs/research/batch-30-t08-08-sources.md)。待确认：V12 外置集交付后本题组条目是否需要去重替换。
