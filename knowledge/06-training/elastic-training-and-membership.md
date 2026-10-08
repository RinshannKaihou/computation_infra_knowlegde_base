---
id: training.elastic-training-and-membership
title: 弹性训练与成员变更
type: concept
domain: training
status: draft
platforms: [generic]
source_refs:
  - src.pytorch.elastic-2.6
  - src.ascend.mindspeed-llm-ha-v2.2.0
updated_at: "2026-10-08"
summary: 解释弹性训练的机制底座（rendezvous、成员变更、失败语义）与两个固定样板的边界：PyTorch 2.6 elastic 只重建进程组、状态恢复是应用责任；MindSpeed-LLM 用副本机制支持缩容续训与 UCE 在线修复。
related_ids:
  - training.parallelism-and-state
  - training.checkpoint-state-consistency
  - communication.collectives-and-rank-progress
  - reliability.dimensions-and-failure-domains
  - data-storage.checkpoint-durability
verification:
  status: source_checked
  evidence_refs:
    - src.pytorch.elastic-2.6
    - src.ascend.mindspeed-llm-ha-v2.2.0
  notes: "已核对 PyTorch 2.6 elastic 系列文档与 MindSpeed-LLM v2.2.0 固定 commit 的 HA 文档及实现入口；两者版本体系不同，仅作机制对照；未运行弹性训练或故障注入。"
---

# 弹性训练与成员变更

## 定义与要解决的问题

弹性训练指训练作业的成员（节点/进程数）可以在运行中变化：节点故障后缩容继续、资源空闲后扩容恢复、或按调度要求伸缩。要理解的机制问题是：成员变化如何被发现与达成一致、进程组如何重建、训练状态谁来恢复。本文用两个固定样板对照：**PyTorch 2.6 elastic（torchelastic/torchrun）** 与 **MindSpeed-LLM v2.2.0 的高可用/弹性功能**。`generic` 指机制问题通用；两者版本体系不同（MindSpeed-LLM 该 tag 的 README 指向 PyTorch 2.7.1），不能拼成一套已验证组合。

## PyTorch 2.6 elastic：rendezvous 与成员变更

**rendezvous** 是分布式同步原语加对等发现，官方文档列出五项功能（[elastic/rendezvous.html](https://docs.pytorch.org/docs/2.6/elastic/rendezvous.html)）：

- **Barrier**：至少 min 节点加入才放行，达到 max 立即完成；min 未达有整体超时且视为不可重试；
- **Exclusivity**：同一 job 任意时刻只允许一个节点组存在，迟到节点只能等待；
- **Consistency**：完成后成员就 membership 与 rank 达成一致——注意 **rank 不稳定**，不能硬编码 RANK/LOCAL_RANK 对应关系；
- **Fault-tolerance**：rendezvous 过程中节点失败时自动以剩余健康节点重新 rendezvous；
- **共享 KV store**：返回实现 `Store` API 的存储，仅本次 rendezvous 成员共享。

后端有 c10d（推荐，基于 TCPStore）、etcd-v2 与 etcd legacy；`RendezvousTimeout` 默认 join 600s、last_call 30s、close 30s。

**成员变更与失败语义**（[elastic/run.html](https://docs.pytorch.org/docs/2.6/elastic/run.html) 的 failure modes 与 important notices）：

- 每节点一个 agent 进程管理本地 worker；worker 失败 → 停掉所有 worker，按实际 `max_restarts` 预算重启；节点离开/到达 → agent 停掉全部 worker，组建新 WorkerGroup，以新 RANK/WORLD_SIZE 重启。
- **默认值按入口区分**：torchrun CLI 的 `--max-restarts` 默认 **0**（[固定 run.py L490–497](https://github.com/pytorch/pytorch/blob/1eba9b3aa3c43f86f4a2c807ac8e12c4a7767340/torch/distributed/run.py#L490-L497)）；直接构造 `WorkerSpec` 的 API 默认 **3**（[api.py L78–86](https://github.com/pytorch/pytorch/blob/1eba9b3aa3c43f86f4a2c807ac8e12c4a7767340/torch/distributed/elastic/agent/server/api.py#L78-L86)）。示例中的 `--max-restarts=3` 是显式配置。调查时记录实际入口、命令行/环境覆盖和最终生效值，不能假设未配置的 torchrun 容忍三次失败。
- **失败或成员变更时，幸存 worker 全部被立即杀死**；训练进度恢复**完全依赖应用自己的 checkpoint**，频率取决于作业对丢失工作的容忍度。torchelastic 只重建进程组（重新分配 RANK/WORLD_SIZE、注入 MASTER_ADDR/PORT），不保存或恢复模型/优化器状态——这是多处文档的合成结论。
- 弹性（min≠max）时禁止硬编码 WORLD_SIZE；仅支持同质 LOCAL_WORLD_SIZE。

**错误分类**（[elastic/errors.html](https://docs.pytorch.org/docs/2.6/elastic/errors.html)）：User Error（输入非法 / worker 子进程失败）、Platform Error（agent 自身）、Infra Error（域之外，如宿主机）。`@record` 把未捕获异常写入 `TORCHELASTIC_ERROR_FILE`，agent 聚合所有子进程错误文件并上报时间戳最小者（“Root Cause” 是启发式）。2.6 的失败记录类名是 `ProcessFailure`——文档页面没有旧名 `WorkerFailure`。`LocalElasticAgent` 的 `exit_barrier_timeout`（默认 300s）防止把先正常退出的 worker 误判为缩容事件。

## MindSpeed-LLM v2.2.0：副本机制上的 HA 与弹性

固定 commit 的[高可用文档](https://github.com/Ascend/MindSpeed-LLM/blob/53f3639c3da9c000a187c44cc0c08d55026ddded/docs/pytorch/features/high_availability.md)描述了与 PyTorch elastic 不同的底座：**把 DP 组切成两个副本 DP 组，使优化器状态均有备份**（内存代价：bf16 grads 时每卡约 4+32/d，对比分布式优化器 4+16/d；推荐千卡及以上集群）。在此之上：

| 功能 | 文档语义 | 边界 |
|---|---|---|
| TTP（临终遗言） | 故障后校验优化器中间状态完整性/一致性，生成一次临终 checkpoint，恢复可回到故障前一刻 | “故障前一刻”的精确 step 语义未定义 |
| UCE Step 级重计算 | NPU 卡内存 UCE 故障实时检测，检测到后基于副本在线修复故障卡并继续训练（`--enable-hbmfault-repair`，要求全局至少存在一个故障卡的副本卡） | “实时检测”的实现层级（芯片/驱动/框架）未指明 |
| 弹性训练 | 故障且无空闲资源时基于副本缩掉部分节点继续训练；有空闲资源后再扩容回原规模（`--enable-elastic-training`，剔除故障卡所在 DP 域对应节点；要求未故障节点中至少一份完整优化器数据；需配合 MindCluster 组件） | **仅支持 DP 粒度缩扩**；缩扩由谁驱动、通信组如何重建，文档未述 |

弹性训练的文档约束（逐条，L75–84）：① 须同时开 `--enable-high-availability` 与 `--use-distributed-optimizer`；② 不支持 `use-custom-fsdp`、`reuse-fp32-param`；③ 仅支持 DP/TP/PP 并行；④ **缩容后不可再次缩容，扩容仅支持直接回到原有规模**。通用约束另有：ptd 切分下 DP size>1；MoE 时稠密与稀疏层 DP size 均>1；长序列并行时 dp_cp_size>1。依赖 `mindio_ttp` 与 `taskd` 两个 whl 包；`HIGH_AVAILABILITY` 环境变量优先级高于命令行参数。

实现入口已确认存在：`mindspeed_llm/features_manager/high_availability/high_availability.py` 注册五个开关，`validate_args` 在代码层强制 mindio_ttp/taskd 导入、HA 先于弹性、拒绝 use_custom_fsdp/reuse_fp32_param/EP>1/CP>1，另有**文档未列**的两条断言（HA 与 `use_dist_ckpt`、`swap_optimizer` 冲突）。注意两边并非包含关系：开关组合与冲突约束以代码为更严，而缩容次数约束（④）仅见文档、代码中无对应断言。

## 机制对照与边界

| 问题 | PyTorch 2.6 elastic | MindSpeed-LLM v2.2.0 |
|---|---|---|
| 成员变更如何达成 | rendezvous（c10d/etcd），min/max、排他、一致性 | 文档未述内部协议；需 MindCluster 组件配合 |
| 失败后的状态从哪来 | 应用自己的 checkpoint（torchelastic 不恢复状态） | 副本 DP 组的优化器状态备份（在线），TTP 临终 checkpoint（离线） |
| 缩扩粒度 | 节点/worker 组重建，应用负责状态 | 仅 DP 粒度；缩容一次、扩容回原规模 |
| rank 稳定性 | rank 不稳定，禁止硬编码 | 未述 |

共同教训：**弹性机制解决“进程组还能不能继续”，训练状态正确性是另一件事**——前者由框架/平台提供，后者依赖 checkpoint 频率、副本覆盖与恢复验证（见[Checkpoint 恢复一致性](checkpoint-state-consistency.md)与[写入持久化边界](../04-data-storage/checkpoint-durability.md)）。

## 常见误解

- **“开了弹性就不丢进度”**：PyTorch elastic 下丢失的是最近 checkpoint 之后的全部进度；MindSpeed-LLM 的副本覆盖优化器状态，但 TTP/UCE/弹性各自有前提（副本卡存在、DP 粒度、开关组合）。
- **“成员变更后原 rank 含义不变”**：rendezvous 语义明确 rank 不稳定。
- **“worker 失败只影响该 worker”**：两者都按整组处理——PyTorch 是杀光重启，MindSpeed-LLM 是剔除故障卡所在 DP 域对应节点。
- **“文档约束是全集”**：MindSpeed-LLM 代码里还有文档未列的冲突断言（use_dist_ckpt、swap_optimizer）。

## 例子与相关知识

- 慢成员导致的集合点等待不是成员变更，先用[慢 rank 诊断](slow-rank-triage.md)区分“慢”与“死”。
- 成员变更触发的集合通信重建与超时，关联[集合通信与 rank 进度](../03-communication/collectives-and-rank-progress.md)。
- 副本/冗余与掩盖的关系见[可靠性维度与故障域](../08-reliability/dimensions-and-failure-domains.md)。

## 来源与待确认问题

- [PyTorch 2.6 elastic 文档](https://docs.pytorch.org/docs/2.6/elastic/run.html)（run/rendezvous/errors/agent/train_script 子页）。
- [MindSpeed-LLM v2.2.0 高可用文档与实现入口](https://github.com/Ascend/MindSpeed-LLM/tree/53f3639c3da9c000a187c44cc0c08d55026ddded)。
- 逐条主张与证据定位见[第十一批弹性训练来源记录](../../docs/research/batch-11-elastic-sources.md)。
- 待确认：MindSpeed-LLM 弹性缩扩的内部驱动与通信组重建细节；MindIO TTP 约束限制外链页；UCE 检测的实现层级；TTP “故障前一刻”的时间语义；PyTorch 2.8 elastic 页未核对。
