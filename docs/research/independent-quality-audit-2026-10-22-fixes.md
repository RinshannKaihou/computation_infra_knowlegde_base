# 独立质量审计 IQ-01–IQ-08 修订与定向核对记录

日期：2026-10-22（Asia/Shanghai）。依据：[独立质量审计](independent-quality-audit-2026-10-22.md)，被评提交 `8a6f7ae7ff8d1c2e2a3645595c76c0dd3f13f8d4`。

本轮已修订全部 8 项具体发现，涉及 7 篇正文，并由修订者重新读取原始证据、检查反例。本文是作者侧修订与核对记录，未重新召集原审阅团队，不替代原审阅者的定向复核或宣布全库评审通过。原审计及既有批次报告保留交付时态。

## 逐项修订与核对

| 发现 | 修订位置 | 当前表述与核对依据 |
|---|---|---|
| IQ-01 · P2 | [NCCL 超时指南](../../knowledge/03-communication/nccl-timeout-triage.md)，“NCCL 2.27.5 的观测边界” | 区分 IB local-ack 与进程组 timeout；按 [PyTorch 2.8 API](https://docs.pytorch.org/docs/2.8/distributed.html#torch.distributed.init_process_group) 补 NCCL 默认 10 分钟、其他后端 30 分钟、显式覆盖与现场日志核查。历史案例的 30 分钟不改写成当前默认值 |
| IQ-02 · P2 | [Kubernetes 作业生命周期](../../knowledge/05-cluster-platform/kubernetes-job-lifecycle.md)，“Pod 生命周期” | 恢复 Pending 的上位定义，将调度和下载镜像作为示例；补回 Running 要求所有容器已创建。按 [v1.32 Pod phase](https://v1-32.docs.kubernetes.io/docs/concepts/workloads/pods/pod-lifecycle/#pod-phase) 整理五状态表，Unknown 不再等同已确认节点失联 |
| IQ-03 · P2 | [对象与并行存储](../../knowledge/04-data-storage/object-and-parallel-storage.md)，第 5 节 | 限普通 RAID0、偏移 0 起连续实际写入完整条带周期、排除空洞与布局变化；同时要求布局、读回完整性、可归属的逐目标写入证据，证据缺失为 unknown。按 [§1.3.1](https://doc.lustre.org/lustre_manual.xhtml#lustre_striping) 的未写入空间语义与 [§19.5](https://doc.lustre.org/lustre_manual.xhtml#pfl) 的组合布局核对；PFL/DoM/FLR 分别设计，采集接口尚未固定 |
| IQ-04 · P2 | [可靠性统计与恢复损失](../../knowledge/08-reliability/reliability-metrics-and-recovery-loss.md)，第六节 | 给定故障 3h、0h 已有有效保存点、忽略保存耗时且到期保存均成功：4h→2h 的损失 3h→1h，8h→4h 的损失 3h→3h。已用有理数算术重算；均匀相位下 `T/2` 的期望另列，未把它当成单次保证 |
| IQ-05 · P2 | [公开题组](../../knowledge/08-reliability/diagnostic-evaluation-fixtures.md)，PTF-02 | 输入改问能否确定故障数量，区分“缺 rank 日志”与“rank 缺席”；判据明确数量与根因未知，保留参与者未到达、错序、共同阻塞、日志缺失与 transport 分支。对照 [Issue 原文](https://github.com/pytorch/pytorch/issues/118369)、[候选两分支评论](https://github.com/pytorch/pytorch/issues/118369#issuecomment-1973742710)及[来源案例](../../knowledge/03-communication/nccl-timeout-source-case.md)，不再要求单点缺席故事作为正解 |
| IQ-06 · P2 | [共享与隔离机制](../../knowledge/05-cluster-platform/accelerator-sharing-and-isolation.md)，“整卡独占”及有限样板表 | 两处无条件表述均改为按运行条件判断的风险。读取 [固定 README](https://github.com/NVIDIA/k8s-device-plugin/blob/487d7a93894b0f3ad08097169593972eb3ca8206/README.md#running-gpu-jobs)与 [Toolkit 1.20.0 GPU Enumeration](https://docs.nvidia.com/datacenter/cloud-native/container-toolkit/1.20.0/docker-specialized.html#gpu-enumeration)，列明 all/none/void/空/未设置的差异，要求核对 runtime、有效环境变量与实际注入路径；不以环境变量替代显式 CDI 调查 |
| IQ-07 · P3 | [容量与扩缩容](../../knowledge/07-inference/capacity-and-autoscaling.md)，“KEDA 的空闲副本限制” | 按 [KEDA v2.18 idleReplicaCount](https://keda.sh/docs/2.18/reference/scaledobject-spec/#idlereplicacount) 补仅支持 0、须小于 minReplicaCount；常驻 n 个副本时省略 idleReplicaCount、设置 minReplicaCount=n。加入 min=5、idle=2 的不支持反例；没有把 v2.18 视为集成样板的已知实际版本 |
| IQ-08 · P3 | 同上，“振荡控制”段 | 按 [KEDA v2.18 cooldownPeriod](https://keda.sh/docs/2.18/reference/scaledobject-spec/#cooldownperiod) 限定为缩至零的冷却期，普通 1↔N 由 HPA 控制；未宣称该字段为所有副本变化的冷却机制 |

## 来源、状态与验证

- 来源登记新增 `src.keda.scaledobject-spec-2.18`，复用并补充 PyTorch 2.8、Pod v1.32、Lustre、Toolkit 1.20.0 条目的核对范围；同步更正 KServe 登记中的字段名和遗漏限制。条目总数仍为 135，来源由 577 增至 578。
- web 工具不能读取 Lustre 的 XHTML MIME，固定 README 页面抓取也失败；改用 curl 读取相同官方 URL/同 commit 原文件，均成功。Lustre 的 `lustre_striping`、`pfl` 锚已在原 XHTML 核实。GitHub 评论由连接器读取，不以页面缺失评论判定证据不存在。
- 本次取回内容的 SHA-256：Lustre XHTML 为 `aee8fc69ea4dff34525714137865356e7f7a3dd24b2fdea8236a7b351f198a3e`；固定 README 为 `275441486e964dfc59d23ae766cc93b9a1cd2f06033ae1e92590cf436823374a`。原文件仅用于临时核对，未镜像进仓库；Lustre 仍是滚动手册，哈希不能保证日后同 URL 内容不变。
- 七篇正文保留稳定 ID、`draft` 与原 `source_checked` 状态，补充本次核对范围；没有新增环境档案或 `reproduced` 声明。算术重算不计 checkpoint 实验，也未执行 GPU/NPU、Lustre、容器或扩缩容操作。

## 系统性建议的后续边界

原审计的工程成熟度短板仍成立。完整示例先沿 [V06 CPU checkpoint 路径](../../plans/validation-backlog.yaml)准备固定构建、输入与预先判据；通信验证沿 V03/V04、推理长尾验证沿 V07 等实例推进，独立效果证据沿 V12 获取。当前 [V00 实例](../../plans/v00-preparation-instances.yaml)仍为 not_ready，未因本文升级任何工作包状态。

本轮把 Pod 定义改为表格，拆开缩零配置、空闲下限、重新激活与睡眠模式，减轻这两处阅读负担。全库长文整理、AMD 专门案例/实验以及真实“原因—处置—复验”示范仍需后续实质工作；不能用这 8 项文字修订声称这些短板已解决。

## 仓库检查

| 检查 | 实际结果与范围 |
|---|---|
| `make check` | PASS：135 content entries / 578 sources；结构与本地文件链接检查 |
| `make build` | PASS：生成 `build/catalog.json` 与 `build/catalog.md`；产物未直接编辑 |
| `git diff --check` | PASS；未发现空白错误 |
| 元数据与来源解析补查 | 7 篇的稳定 ID 均保留，日期为 2026-10-22，编辑/验证状态未升级；PyTorch 与 Pod 来源 notes 改为折叠块，解析后保留 `#` 锚点后的核对内容，KEDA 新登记解析完整 |
| IQ-04 算术 | 固定故障时刻与有效保存点的两组合成对照重算一致；无 checkpoint 实测结果 |

以上不验证远程页面将来的内容、目标环境兼容性或硬件行为。未修改 `src/kb/`，本轮未运行工具回归测试，也没有产生诊断效果分数。
