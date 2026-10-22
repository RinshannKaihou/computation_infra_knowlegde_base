# 知识库独立质量评审与正确性抽检

日期：2026-10-22（Asia/Shanghai）。被评基线：`8a6f7ae7ff8d1c2e2a3645595c76c0dd3f13f8d4`；开始评审时工作区干净。

本次由主代理与三个 subagents 直接独立审读，不沿用仓库建设期间的模型、CLI、批次验收或例外接受规则。已有审阅记录只用于理解历史背景，不作为当前正文正确的证据。没有修改知识正文、执行集群操作或开展硬件实验；本文件只是新增的评审交付物。所有发现均保持待修订状态。

## 总体判断

**这是一个组织与证据意识较强、机制解释有实质内容的知识库；工程使用成熟度明显落后于内容覆盖广度。** 适合有基础的读者建立系统认识、查询版本条件、组织排障假设。对于“在指定环境执行哪些步骤、如何判读真实输出、何时确认恢复”的问题，还需要补具体实现与验证记录。

抽样没有显示大面积编造接口或把未实测写成已验证的问题。发现的主要错误更细：默认值混用、将例子写成穷尽定义、遗漏必要前提，以及把合理候选机制写进标准答案。这些错误会影响实际判断，不能因来源多或历史审阅轮数多而忽略。

| 维度 | 判断 | 主要依据 |
|---|---|---|
| 组织与查找 | 较强 | 九领域主归属、稳定 ID、平台/任务路径、结构化目录与关联引用完整；本轮检查通过 |
| 机制与概念 | 较强 | 抽查的精度、持久化、MPS、流式时延、RL 状态边界都有具体技术内容 |
| 来源可追溯性 | 较强 | 广泛使用固定 commit/版本化文档；抽样中能追回源码，并保留上游冲突 |
| 技术正确性 | 样本多数支持，存在局部缺陷 | 16 篇、36 组定向主张中，29 组支持，5 组错误或逻辑条件不足，2 组边界不完整；不能外推总体正确率 |
| 现场操作可用性 | 较弱 | 无真实环境档案引用、无本地复现；多数流程仍要求读者自行补采集实现和具体判据 |
| 教学与阅读体验 | 中等 | 内容深，但长段落、多平台例外与审计历史混排，妨碍快速提取结论 |
| 经验与评测证据 | 尚未建立本地闭环 | 本地 reproduced 为 0；公开题组没有运行分数，独立评测集尚缺 |

以上是定性评审，不是按篇数加权得到的评分。

## 全库盘点与检查

本轮从当前源文件重建清单，得到：

- 135 个条目：114 篇实质正文，21 篇导航；外部来源 577 项。
- 正文类型：concept 33、reference 29、procedure 36、case 9、experiment 7。
- 全部 135 条编辑状态为 draft。114 篇正文中，source_checked 99、not_verified 15、reproduced 0；状态命名本身不证明技术正确性。
- 所有条目的 `applicability.environment_refs` 均为空；这是缺少真实环境挂接，不等于缺少资料所述条件。
- AMD 标签覆盖 30 篇实质正文，但其中 case 0、experiment 0；NVIDIA 为 39 篇、case 3、experiment 2；Ascend 为 47 篇、case 5、experiment 5。平台标签可以重叠，不能相加当总篇数。
- 正文长度中位数约 10,945 字符；最长约 37,205 字符。仅 1 篇正文包含带 bash/shell/python/sh/console 语言标记的可执行代码块，且仓库没有 `scripts/` 目录。这是样例稀缺的辅助指标，不表示其他页面没有行内命令。
- 577 项来源中 572 项被 `source_refs` 使用。来源种类为 documentation 400、repository 132、paper 24、issue 21；这些是登记条目，不是独立实验数量。

| 检查 | 本轮结果 | 能证明什么 |
|---|---|---|
| `make check` | PASS：135 entries / 577 sources | 元数据、引用与工具覆盖的本地链接符合结构要求 |
| `make build` | PASS | 目录可生成 |
| 正文标题与元数据 title 比对 | 未发现不一致 | 标题一致 |
| knowledge/、paths/ 本地 Markdown 片段链接补查 | 9 处，未发现潜在缺失目标 | 使用近似 GitHub 标题 slug 规则的静态补查；未作浏览器渲染验证 |

没有把上述检查当作远程内容、源码语义或硬件兼容验证。工具代码未修改，本次没有运行其回归测试。

## 需要修订的发现

本报告 P2 表示会影响配置、诊断或实验判读的局部问题；P3 表示应补充以防误读的较小边界问题。没有在本次范围内发现 P0/P1，不代表全库不存在。

### IQ-01 · P2：NCCL 进程组超时预算混入了其他后端的默认值

位置：[NCCL 超时诊断指南](../../knowledge/03-communication/nccl-timeout-triage.md)，第 90 行；声明的框架来源基线在第 21、44 行。

正文将 `NCCL_IB_TIMEOUT` 与“PyTorch collective watchdog 的 30 分钟等待预算”区分。区分两层 timeout 的方向正确，但给出的无条件 30 分钟与本篇 PyTorch 2.8 基线不符。该版 `init_process_group(timeout)` 的默认值是 NCCL 10 分钟，其他后端 30 分钟；应用也可以显式覆盖。[PyTorch 2.8 官方定义](https://docs.pytorch.org/docs/2.8/distributed.html#torch.distributed.init_process_group)

影响：读者可能以错误默认值判断超时是否异常，或把旧案例中的 30 分钟推广到当前基线。

建议：改为“该参数独立于进程组 timeout；PyTorch 2.8 NCCL 默认 10 分钟，实际值读取初始化配置与日志”。如要保留 30 分钟，只能明确归属到具体历史案例。

### IQ-02 · P2：Pending 被写成只包含两个示例状态

位置：[Kubernetes 作业生命周期](../../knowledge/05-cluster-platform/kubernetes-job-lifecycle.md)，第 58 行。

正文写 `Pending`“原文仅含等待调度与下载镜像”。上游定义是 Pod 已被接受，但一个或多个容器尚未完成设置并准备运行；等待调度、下载镜像只是包含的示例，不能缩成全部范围。`Running` 的定义还包含所有容器已经创建这个条件。[Kubernetes v1.32 Pod phase](https://v1-32.docs.kubernetes.io/docs/concepts/workloads/pods/pod-lifecycle/#pod-phase)

影响：对已绑定节点、但仍卡在其他容器准备步骤的 Pending Pod，读者可能把调查错误地限制在调度和拉镜像。

建议：恢复上位定义，再列调度、镜像与其他容器准备过程；同时补回 Running 的容器创建条件。

### IQ-03 · P2：逻辑文件大小不能保证写到了所有 Lustre 条带目标

位置：[对象存储与并行文件系统](../../knowledge/04-data-storage/object-and-parallel-storage.md)，第 92 行。

“文件大小 ≥ stripe_size × stripe_count（保证每 OST 被写到）”缺少必要条件。稀疏文件可以满足逻辑长度而没有实际写满一个条带周期；PFL/composite layout 又可在不同 extent 使用不同布局。Lustre 手册 §1.3.1 说明未写数据不占用对应 OST 空间，§19.5 描述组合布局。[Lustre 官方手册](https://doc.lustre.org/lustre_manual.xhtml)

影响：验证可能通过 getstripe 和文件长度检查，却没有实际覆盖全部预期对象/OST，误报测试覆盖。

建议：限定普通 RAID0 布局，从偏移 0 实际连续写入至少一个完整条带周期，排除空洞并观测实际对象/OST 写入。PFL、DoM 与其他布局分别设计验证。getstripe 与读回哈希本身不证明每个目标实际收到写入。

取证说明：web 工具不支持该站 XHTML MIME；subagent 使用 curl 取回同一精确官方 URL 核对，未因抓取工具报错而判链接失效。

### IQ-04 · P2：checkpoint 间隔减半的示例不能推出“丢失不变”

位置：[可靠性统计、有效产出与恢复损失](../../knowledge/08-reliability/reliability-metrics-and-recovery-loss.md)，第 177 行。

正文说间隔减半、失败仍在共同保存点后 3 小时，丢失不变。它没有固定原间隔，也没有检查新增保存点是否已成功完成，因此结论不是所列前提的必然结果。

不计保存耗时、假设到期保存均成功的反例：

| 原间隔 → 新间隔 | 固定故障时刻 | 原最近保存点 → 新最近保存点 | 丢失工作 |
|---|---|---|---|
| 4h → 2h | 共同起点后 3h | 0h → 2h | 3h → 1h |
| 8h → 4h | 共同起点后 3h | 0h → 0h | 3h → 3h |

本轮用简单算术脚本重算了这两组时间点。这是合成反例，不是 checkpoint 实验。

正文“不能无条件断言每次重算都减半”的总方向正确。建议给出第二行那样明确的间隔和保存前提，或改为“实际损失取决于故障时刻与最近有效 checkpoint；期望减半还需要相位分布等假设”。

### IQ-05 · P2：未闭环案例的候选机制被写成了评测正解

位置：[诊断评测公开题组](../../knowledge/08-reliability/diagnostic-evaluation-fixtures.md)，PTF-02，第 57–59 行；与[对应来源案例](../../knowledge/03-communication/nccl-timeout-source-case.md)第 68、83 行对照。

输入只给出 rank 1–7 的同序号超时、rank 0 缺对应日志与利用率快照，并明确上游未确认根因；判据却将“单点缺席经同步屏障表现为全体超时”写成正确方向。要求保持 suspected 有帮助，但仍可能将与现有证据相容的其他答案判错。七条日志不能推出七个独立故障，也不能反过来证明只发生一个故障或确定缺席的原因。[PyTorch 原始 Issue #118369](https://github.com/pytorch/pytorch/issues/118369)

影响：公开题组会鼓励答题者套用预设故事；更严格地保留故障数量未知的答案反而可能失分。

建议：正解改为“不能按超时日志数计故障；优先检验共同阻塞、参与者未到达或操作次序分叉，补 rank 0 及其他 rank 的进展证据；故障数量与根因仍未知”。把单点缺席保留为高优先级候选，而非唯一正确机制。

### IQ-06 · P2：无 GPU 请求即暴露全部 GPU 的表述缺运行条件

位置：[加速器共享与租户隔离机制](../../knowledge/05-cluster-platform/accelerator-sharing-and-isolation.md)，第 79、124 行。

固定版本 device-plugin README 确实给出了“不请求 GPU 会看到全部设备”的警告，因此并非虚构引用。但正文把它写成插件的无条件行为。实际可见性还取决于运行时、镜像环境变量与设备注入路径；官方 Container Toolkit 文档区分 `NVIDIA_VISIBLE_DEVICES=all`、`none`、`void`/空/未设置，结果不同。[固定 README](https://github.com/NVIDIA/k8s-device-plugin/blob/487d7a93894b0f3ad08097169593972eb3ca8206/README.md)、[Container Toolkit GPU Enumeration](https://docs.nvidia.com/datacenter/cloud-native/container-toolkit/latest/docker-specialized.html#gpu-enumeration)

影响：读者可能误解分配与暴露的责任层，也无法据此正确预测非默认镜像或运行时下的行为。

建议：改成带条件的风险说明，例如“在所述 NVIDIA runtime/CUDA 镜像配置下，无资源请求也可能暴露全部 GPU”；核查 runtime、环境变量与实际设备注入，再判定暴露原因。

### IQ-07 · P3：idleReplicaCount 仅列大小关系，漏了只支持 0 的限制

位置：[容量、扩缩容与冷启动决策](../../knowledge/07-inference/capacity-and-autoscaling.md)，第 68 行。

正文只说 `idleReplicaCount` 可低于最小副本数。所链 KEDA v2.18 规格还明确该字段仅支持 0，非零值不能正常工作；需要保留 n 个常驻副本，应省略该字段、使用 `minReplicaCount=n`。[KEDA v2.18 idleReplicaCount](https://keda.sh/docs/2.18/reference/scaledobject-spec/#idlereplicacount)

例如 min=5、idle=2 虽满足正文写出的不等式，却不属于该版支持范围。考虑本段本就在讨论 scale-to-zero，保守定 P3。建议补明版本、仅支持 0 的条件，并统一字段名为 `minReplicaCount`。

补充 IQ-08 · P3：同文第 61 行把 `cooldownPeriod` 概括为冷却机制时，应明确它作用于缩至 0；普通 1↔N 副本变化由 HPA 控制。这是主要抽样集外的附加边界提醒，未重复计入 36 组主张。[KEDA v2.18 cooldownPeriod](https://keda.sh/docs/2.18/reference/scaledobject-spec/#cooldownperiod)

## 抽样中得到支持的内容

以下列出主张组及精确来源，避免报告只呈现问题而掩盖已核对的实质优点。同一行可以包含一组紧密关联的字段；不是逐句穷尽核验。

| 编号 | 本地正文与行号 | 核验内容 | 结果与一手证据 |
|---|---|---|---|
| E01 | dtype-layout-and-precision-semantics:94 | matmul 与 cuDNN 的 TF32 默认值、分别关闭 | 支持；[PyTorch 2.6 CUDA semantics](https://docs.pytorch.org/docs/2.6/notes/cuda.html#tensorfloat-32-tf32-on-ampere-and-later-devices) |
| E02 | 同文:96 | FP8 e4m3/e5m2 与 e8m0 scale 类型 | 支持；[CUDA 12.8 FP8](https://docs.nvidia.com/cuda/archive/12.8.0/cuda-math-api/cuda_math_api/group__CUDA__MATH__INTRINSIC__FP8.html) |
| E03 | 同文:121 | assert_close 公式、容差、默认检查与 NaN | 支持；[PyTorch 2.6 testing](https://docs.pytorch.org/docs/2.6/testing.html#torch.testing.assert_close) |
| E04 | communication-library-profiles:63 | 隐式 launch order 的版本、默认与 CUDA 条件 | 支持；[NCCL 2.27.5 环境变量](https://docs.nvidia.com/deeplearning/nccl/archives/nccl_2275/user-guide/docs/env.html#nccl-launch-order-implicit)及[并发 communicator](https://docs.nvidia.com/deeplearning/nccl/archives/nccl_2275/user-guide/docs/usage/communicators.html#using-multiple-nccl-communicators-concurrently) |
| E05 | 同文:64 | ncclResult_t 八值、Success/InProgress 非错误 | 支持；[NCCL 2.27.5 types](https://docs.nvidia.com/deeplearning/nccl/archives/nccl_2275/user-guide/docs/api/types.html#ncclresult-t) |
| E06 | nccl-timeout-triage:77 | RAS 的 MISMATCH/INCOMPLETE 判读 | 支持；[NCCL 2.27.5 RAS](https://docs.nvidia.com/deeplearning/nccl/archives/nccl_2275/user-guide/docs/troubleshooting/ras.html) |
| E07 | 同文:98 | dump-on-timeout 依赖非零 trace buffer | 支持；[PyTorch 2.8 NCCL 变量](https://docs.pytorch.org/docs/2.8/torch_nccl_environment_variables.html) |
| E08 | 同文:90 | watchdog 等待预算 | 问题，见 IQ-01 |
| E09 | health-evidence:349–351 | AMD reset 三种影响范围 | 支持；[AMD SMI docs-10.1.0](https://rocm.docs.amd.com/projects/amdsmi/en/docs-10.1.0/how-to/amdsmi-cli-tool.html#amd-smi-reset) |
| E10 | 同文:362–363 | N/A 分类与 CSV 缺列 | 支持；同一[固定 AMD 页面](https://rocm.docs.amd.com/projects/amdsmi/en/docs-10.1.0/how-to/amdsmi-cli-tool.html) |
| E11 | checkpoint-durability:63 | async_save 的暂存、线程保存与 Future | 支持；[PyTorch 2.6 DCP](https://docs.pytorch.org/docs/2.6/distributed.checkpoint.html) |
| E12 | 同文:67–77 | sync_files、元数据重命名与持久性边界 | 支持；[固定 filesystem.py](https://github.com/pytorch/pytorch/blob/1eba9b3aa3c43f86f4a2c807ac8e12c4a7767340/torch/distributed/checkpoint/filesystem.py)与[fsync 手册](https://man7.org/linux/man-pages/man2/fsync.2.html) |
| E13 | kubernetes-job-lifecycle:54 | Job terminal 条件延迟与 Pod 对象保留 | 支持；[v1.32 Job](https://v1-32.docs.kubernetes.io/docs/concepts/workloads/controllers/job/) |
| E14 | 同文:58 | Pending 定义 | 问题，见 IQ-02 |
| E15 | accelerator-sharing-and-isolation:57、101–104、134–135 | MPS 限额不是预留、错误影响范围与静态分区条件 | 支持；[NVIDIA MPS](https://docs.nvidia.com/deploy/mps/when-to-use-mps.html) |
| E16 | 同文:79、124 | 未请求 GPU 时暴露行为 | 边界不完整，见 IQ-06 |
| E17 | object-and-parallel-storage:54、84 | 不把 ETag 当端到端内容哈希 | 支持其保守判断；[Ceph Squid bucketops](https://docs.ceph.com/en/squid/radosgw/s3/bucketops/)与[objectops](https://docs.ceph.com/en/squid/radosgw/s3/objectops/) |
| E18 | 同文:92 | 文件大小保证条带写入覆盖 | 问题，见 IQ-03 |
| E19 | checkpoint-state-recovery-source-case:34、38、40 | 未初始化 optimizer state、strict false 报错、原脚本加载旧对象 | 支持；[PyTorch #164257](https://github.com/pytorch/pytorch/issues/164257) |
| E20 | 同文:68–70 | 固定修复的 FQN 检查与 strict 分支 | 支持；[固定修复 diff](https://github.com/pytorch/pytorch/commit/edd8d356b6d9a00cfa34fa323578e5cf1c7e0463) |
| E21 | latency-metrics:109、179 | TPOT 样本过滤、goodput 的逐请求 AND 判据 | 支持；[固定 serve.py L404–470](https://github.com/vllm-project/vllm/blob/b17039bccc17b94a2ea107272ad7bc93508708df/vllm/benchmarks/serve.py#L404-L470) |
| E22 | 同文:95–97、141–144 | completion/chat chunk、成功与 E2E 结束事件差异 | 支持；[固定 endpoint 实现](https://github.com/vllm-project/vllm/blob/b17039bccc17b94a2ea107272ad7bc93508708df/vllm/benchmarks/lib/endpoint_request_func.py#L179-L365) |
| E23 | capacity-and-autoscaling:61 | HPA 多指标失败方向、稳定窗与变化率 | 支持；[v1.32 HPA](https://v1-32.docs.kubernetes.io/docs/tasks/run-application/horizontal-pod-autoscale/) |
| E24 | 同文:66 | 弹性 EP 先排空再改 DP cores，与 K8s 副本分开 | 支持；[固定 async_llm.py L801–855](https://github.com/vllm-project/vllm/blob/b17039bccc17b94a2ea107272ad7bc93508708df/vllm/v1/engine/async_llm.py#L801-L855) |
| E25 | rl-rollout-consistency:151–153 | staleness 生产预算与 streaming 的参数边界 | 支持；[verl v0.9.1 fully_async](https://github.com/verl-project/verl/blob/v0.9.1/docs/advance/fully_async.md) |
| E26 | 同文:139、170 | delta 接收端限制、失败重启整个 job | 支持；[v0.9.1 delta_weight_transfer.py](https://github.com/verl-project/verl/blob/v0.9.1/verl/workers/rollout/vllm_rollout/delta_weight_transfer.py#L216-L240) |
| E27 | capacity-and-autoscaling:68 | idleReplicaCount 可配置范围 | 边界不完整，见 IQ-07 |
| E28 | reliability-metrics-and-recovery-loss:62 | HPP 的总运行时间/故障数估计 | 支持；[NIST apr451](https://www.itl.nist.gov/div898/handbook/apr/section4/apr451.htm) |
| E29 | 同文:71 | Llama 3 的快照中断数及归因语气 | 支持；[Llama 3 v3 §3.3.4](https://arxiv.org/html/2407.21783v3#S3.SS3.SSS4) |
| E30 | 同文:71 | 上游 Table 5 的计数/百分比冲突 | 支持；逐行复核该[固定表](https://arxiv.org/html/2407.21783v3#S3.T5)，没有替上游擅自消歧 |
| E31 | 同文:77–79 | MPG 的 SG/RG/PG 分层 | 支持；[MPG v1 §4.3](https://arxiv.org/html/2502.06982v1) |
| E32 | 同文:177 | checkpoint 间隔示例 | 条件不足，见 IQ-04 |
| E33 | diagnostic-evaluation-method:45 | Cloud-OpsBench 案例数与快照模拟机制 | 支持其论文转述；[固定 v1 论文](https://arxiv.org/html/2603.00468v1)；未运行该基准 |
| E34 | 同文:84 | ZTDR 定义及其不等同 abstention | 支持；同论文 §4.2 与本地逻辑区分 |
| E35 | diagnostic-evaluation-fixtures:57–59 | PTF-02 单点缺席判据 | 推理越界，见 IQ-05 |
| E36 | reference-architectures:107 | NVL72 域及 18 compute trays、9 switch trays、2 management TOR | 支持当前官方页；[DGX GB hardware](https://docs.nvidia.com/dgx/dgxgb200-user-guide/hardware.html)为动态页，未追认其历史页面身份 |

表中省略目录前缀的名称，均为 `knowledge/` 下唯一同名 Markdown 文件；精确定位按被评基线的本地行号。后续修改可能使行号移动。

其他取证限制：精度页第 95 行的一个 API URL 本轮两次未能通过 web 工具取得，未据此判定 404，也未用相邻页面代替证据；该项不计入上述 36 组。GitHub 抓取失败处，subagents 使用连接器或 curl 读取同一精确 ref；没有以搜索摘要代替原文。

## 系统性质量短板

1. **从判断框架到执行闭环还有距离。** 36 篇 procedure 并非空模板，通常有分支、证据要求与停止条件；但采集程序、输入样例、真实输出、可重跑制品和结果记录不足。新手仍须自行完成大量实现，Agent 也可能在“知道要看什么”之后临时补写未经验证的动作。优先补少量端到端示例，比继续增加题目覆盖更有价值。
2. **案例的证据强弱分布偏向未闭环公开 Issue。** 版本配套、HCCL、NCCL、精度迁移、设备可见性和 checkpoint 等案例都诚实保留了复验或根因缺口；这值得肯定，但意味着读者看到的更多是调查练习，较少是“原因—处置—真实复验”完整示范。不能将九篇 case 当作九个已验证修复方案。
3. **阅读负担偏高。** runtime 参考页超过 3.7 万字符；Kubernetes、RL、精度与部分 index 中，一个段落或表格单元同时承载结论、版本、例外、旧发现编号和维护历史。可将“当前结论与条件”“具体例子”“来源/历史细节”分层，正文首屏优先给读者答案与最短路径。
4. **三平台的经验覆盖不均。** AMD 有实际机制内容，不只是占位；但没有专门 case/experiment。跨平台比较说明不等于各平台都有可复用实践链。
5. **尚无独立的效果证据。** 模型审阅和来源对照不能回答使用知识库后是否更快定位、是否更少误判。公开题组本身也需要先修正 IQ-05，再区分检索回归与诊断效果评测。

已有记录中的累加精度契约、HCCL Test 配套交集等未知项，本次没有取得关闭证据；也没有因过去曾条件验收就视为已解决。反过来，明确公开 unknown 不是新的事实错误，不能重复充当本次新增缺陷。

## 建议的改进顺序

1. 先定向修正 IQ-01–IQ-08，并按原始证据或明确反例复核；无需等待硬件资源。
2. 选择 2–3 个高频问题补完整示例：固定环境、最小输入、采集动作、脱敏输出、分支判读、恢复确认。先完成一个 CPU 可做的 checkpoint 示例，再按可用资源补通信或推理示例。
3. 对新实验的前置条件做反例检查：稀疏文件、缺失 rank 日志、非默认 runtime、显式 timeout、非零 idle 值等。目标是检查“判据是否真能证明结论”，而非只检查字段齐不齐。
4. 压缩正文中的历史过程，将高密度参考与排障首屏分开；保留精确来源与当前未知项。
5. 再补独立案例评测，至少比较查找路径、引用正确性、候选区分、错误归因与恢复判据；不从本轮定向样本生成全库正确率。

本次发现仍待修订；本报告没有宣布全库评审通过，也没有改变正文的编辑或验证状态。
