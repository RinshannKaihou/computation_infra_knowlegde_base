# AI 算力基础设施与计算可靠性知识库

面向 Human 与 Agent，共同覆盖 GPU/NPU、训练/后训练/推理。内容按系统领域组织，可靠性贯穿各章，平台和任务入口串联同一份正文。

**首轮状态（2026-09-30 首轮交付时口径）：首轮 41 篇正文草稿已交付。** 第三至第七批已完成独立 astra/xhigh 审阅及问题修订复核，首轮任务清单全部完成。九个领域已有基础正文，并提供 7 组诊断指南、公开来源案例和实验设计。首轮来源登记共 63 项，正文均保持草稿；尚未开展真实 GPU/NPU 环境验证。

交付范围、审阅记录与证据缺口见[首轮内容交付核对](docs/first-fill-status.md)。首轮结束后已暂停，后续由 Opus 接手，见[交接提示词](docs/handoff-to-opus.md)。第二轮首批（batch 08）新增 3 篇：昇腾 NPU 内存与 OOM 证据、训练数据加载饥饿诊断、空闲设备但作业等待诊断；第二批（batch 09）再增 3 篇：昇腾推理 OOM 诊断、通信带宽退化诊断、静默错误与计算完整性判定；第三批（batch 10）再增 3 篇：慢 rank 诊断、供电散热与性能退化证据、Checkpoint 慢写与恢复 I/O 诊断；第四批（batch 11）再增 3 篇：昇腾算子不支持与图编译失败诊断、弹性训练与成员变更、推理量化与输出质量验证；第五批（batch 12）再增 3 篇：Prefill/Decode 分离与流量分配、新节点与返修节点验收、Checkpoint 完整性与校验证据。任务清单见[第二轮任务表](plans/round-02-backlog.yaml)，来源与审阅记录见各批来源审计（[batch-08](docs/research/batch-08-source-audit.md)、[batch-09](docs/research/batch-09-source-audit.md)、[batch-10](docs/research/batch-10-source-audit.md)、[batch-11](docs/research/batch-11-source-audit.md)、[batch-12](docs/research/batch-12-source-audit.md)）；batch 01/02/08/09 已经 Codex 代审并复核闭环，见[四批汇总](docs/research/batch-01-02-08-09-codex-review-summary.md)。

2026-09-30，用户授权由本会话 Codex 替代 astra 补审 batch 01、02、08、09。[四批审阅汇总](docs/research/batch-01-02-08-09-codex-review-summary.md)：batch 01 无修改项，其他三批的 9 项唯一发现（5 P2、4 P3）经修订和[定向复核](docs/research/batch-02-08-09-codex-recheck.md)全部关闭，四批在原审阅范围内通过。截至 2026-10-08（batch 12 交付后），目录为 69 content entries / 84 sources；知识正文仍保持草稿。本次没有实际派发 astra/xhigh，也没有开展硬件验证。

2026-10-08 用户将当前及后续批次的审阅模型更新为 **`gpt-6.1-sol / xhigh`**。batch 10、11、12 的 9 篇正文已由该模型完成审阅，初审发现 13 项（1 P1、9 P2、3 P3），现经修订与[定向复核](docs/research/batch-10-11-12-codex-recheck.md)全部关闭，三批在原审阅范围内通过；见[三批审阅汇总](docs/research/batch-10-11-12-codex-review-summary.md)。正文仍为 `draft / source_checked`，本次未执行真实环境验证。历史报告保留实际模型记录，当前约定见[写作指南](docs/authoring-guide.md#7-批次审阅约定)。

2026-10-08 已完成[原设计 63 个二级主题的覆盖盘点](docs/topic-coverage-audit.md)：12 个已覆盖基础范围、44 个部分覆盖、7 个尚无主干正文。逐主题依据、缺口与补齐建议见[机器可读清单](plans/topic-coverage.yaml)。两轮草稿交付完成与全部主题覆盖完成分别统计。后续已形成[完整覆盖规划](docs/full-coverage-roadmap.md)和[执行清单](plans/full-coverage-backlog.yaml)：85 项内容任务、Batch 13–32 共 20 个后续批次；规划交付时任务均为 planned；实际运行状态由对应交付与审阅记录更新。51 个待补主题与 12 个基础已覆盖主题均有本轮验收范围，141 条原盘点缺口逐项映射。运行前查看[批次依赖与并行规则](docs/batch-dependencies.md)，按具体前置验收解锁任务。

2026-10-09，Batch 13 的四篇新正文与一篇修订完成补充审阅、修订及两轮 `gpt-6.1-sol / xhigh` 定向复核，R01–R06 全部关闭，在该审阅范围内通过；见[来源审计](docs/research/batch-13-source-audit.md)与[复核汇总](docs/research/batch-13-codex-rerecheck.md)。当前目录为 73 content entries / 123 sources；正文仍为 `draft / source_checked`，尚无真实硬件验证。

## 从这里开始

| 目录 | 内容范围 |
|---|---|
| [00 导读与系统全景](knowledge/00-overview/index.md) | 端到端路径、架构和学习入口 |
| [01 物理设施与计算节点](knowledge/01-hardware/index.md) | 供电散热、CPU、GPU/NPU、设备内存与硬件健康 |
| [02 系统软件与加速器执行栈](knowledge/02-software-stack/index.md) | 驱动、CANN/CUDA/ROCm、算子、编译和框架适配 |
| [03 互联网络与分布式通信](knowledge/03-communication/index.md) | 拓扑、RDMA、集合通信和通信异常 |
| [04 数据路径与存储系统](knowledge/04-data-storage/index.md) | 加载、缓存、存储、持久化与完整性 |
| [05 集群平台与资源管理](knowledge/05-cluster-platform/index.md) | 容器、设备分配、调度、隔离与生命周期 |
| [06 训练与后训练系统](knowledge/06-training/index.md) | 并行、训练状态、精度、性能与恢复 |
| [07 推理与服务系统](knowledge/07-inference/index.md) | 引擎、KV cache、路由、服务质量与恢复 |
| [08 可靠性与计算正确性方法](knowledge/08-reliability/index.md) | 故障模型、证据、归因、验证与度量 |

平台入口：[昇腾](paths/platforms/ascend.md) · [NVIDIA](paths/platforms/nvidia.md) · [AMD](paths/platforms/amd.md)

任务入口：[训练问题定位](paths/tasks/training-triage.md) · [推理问题定位](paths/tasks/inference-triage.md)。这些入口是阅读路径，尚不是经过现场验证的操作流程。另有按任务阶段的六条路径——[选型与容量](paths/tasks/selection-and-capacity.md)、[节点验收](paths/tasks/node-acceptance.md)、[环境安装](paths/tasks/environment-installation.md)、[性能优化](paths/tasks/performance-optimization.md)、[迁移与升级](paths/tasks/migration-and-upgrade.md)、[故障恢复](paths/tasks/fault-recovery.md)——与[按角色阅读路径](paths/roles/reading-by-role.md)。

## 已有正文

| 内容 | 可以帮助回答的问题 |
|---|---|
| [一次训练任务的端到端路径](knowledge/00-overview/training-lifecycle.md) | 资源、数据、训练状态与进展在哪些层交汇？ |
| [一次推理请求的端到端路径](knowledge/00-overview/inference-lifecycle.md) | 请求、调度、KV 与服务指标如何对应？ |
| [设备健康证据与检测边界](knowledge/01-hardware/health-evidence.md) | 健康摘要、事件、计数器、检测失败与未覆盖如何分开？ |
| [NVIDIA 软件栈的文档配套档案](knowledge/02-software-stack/nvidia-documented-profile.md) | 一个容器标签固定了什么，驱动和运行层的哪些条件仍未知？ |
| [作业准入、调度与拓扑放置](knowledge/05-cluster-platform/admission-and-placement.md) | 空闲设备、配额、准入、放置与应用进展为什么不能互相替代？ |
| [主机到模型执行的软件栈分层](knowledge/02-software-stack/layers-and-boundaries.md) | 驱动、平台软件、框架后端、推理引擎和集群设备插件各负责什么？ |
| [如何判断版本配套是否有依据](knowledge/02-software-stack/compatibility-evidence.md) | 发行包、源码分支、官方声明和本地验证怎样分别判断？ |
| [昇腾软件栈的文档配套档案](knowledge/02-software-stack/ascend-documented-profile.md) | 固定 TorchNPU 发布快照说明了哪些配套关系，哪些环境条件仍未知？ |
| [计算节点资源与拓扑参考](knowledge/01-hardware/resource-topology.md) | CPU、主机/设备内存、PCIe、网络和共享故障域怎样记录？ |
| [训练数据供给路径与等待](knowledge/04-data-storage/training-data-path.md) | 等待发生在存储、CPU、队列、传输还是训练消费阶段？ |
| [从物理设备到容器资源的状态链](knowledge/05-cluster-platform/device-resource-chain.md) | 设备存在、驱动可见、平台可分配、容器可访问和框架可用如何区分？ |
| [集合通信与 rank 进度](knowledge/03-communication/collectives-and-rank-progress.md) | 怎样匹配参与者、次序和参数，为什么超时不能直接归因于网络？ |
| [通信带宽与性能基线口径](knowledge/03-communication/bandwidth-baselines.md) | algbw、busbw、物理链路流量怎样区分，GPU/NPU 结果何时可比？ |
| [Checkpoint 写入与持久化边界](knowledge/04-data-storage/checkpoint-durability.md) | 保存返回、后台完成、持久化与可恢复之间分别需要什么证据？ |
| [可靠性维度与故障域](knowledge/08-reliability/dimensions-and-failure-domains.md) | 如何分别定义可用性、正确性、性能和恢复目标？ |
| [诊断中的证据、假设与结论](knowledge/08-reliability/evidence-and-hypotheses.md) | 怎样对齐证据、比较候选原因并选择下一项检查？ |
| [并行策略与训练状态](knowledge/06-training/parallelism-and-state.md) | 并行布局怎样改变参数、优化器、随机状态和数据进度的责任？ |
| [Checkpoint 恢复一致性](knowledge/06-training/checkpoint-state-consistency.md) | 保存、加载、重分片和正确续训分别需要哪些验证？ |
| [推理执行与 KV cache](knowledge/07-inference/execution-and-kv-cache.md) | prefill/decode、batch、前缀复用、抢占和 KV 容量如何关联？ |
| [推理延迟与吞吐指标字典](knowledge/07-inference/latency-metrics.md) | TTFT、TPOT、ITL、E2E、吞吐与 goodput 的统计口径怎样区分？ |
| [昇腾 NPU 内存与 OOM 证据](knowledge/02-software-stack/ascend-memory-oom-evidence.md) | 物理设备内存、框架分配/保留、workspace 和碎片怎样区分？OOM 报错在哪一层抛出？ |
| [训练数据加载饥饿诊断指南](knowledge/04-data-storage/data-starvation-triage.md) | 取 batch 等待怎样定位到存储、CPU 处理、队列、传输或消费的首个边界？ |
| [空闲设备但作业等待诊断指南](knowledge/05-cluster-platform/idle-resource-job-waiting-triage.md) | 有空闲设备但作业不运行时，等待在配额、准入、拓扑、放置还是设备分配？ |
| [昇腾推理 OOM 诊断指南](knowledge/07-inference/ascend-inference-oom-triage.md) | OOM 在启动检查、profiling、图编译、prefill、decode 还是并发运行期？哪一层抛出？ |
| [通信带宽退化诊断指南](knowledge/03-communication/bandwidth-degradation-triage.md) | “带宽变低”是测量口径、配置/映射还是真实链路退化？ |
| [静默错误与计算完整性判定](knowledge/08-reliability/silent-errors-and-integrity.md) | 健康检查全绿时凭什么相信计算结果？SDC 与正常数值噪声如何区分？ |
| [慢 rank 诊断指南](knowledge/06-training/slow-rank-triage.md) | 分布式训练变慢时，谁先慢、慢在数据/计算/通信/设备哪个阶段？ |
| [供电、散热与性能退化证据](knowledge/01-hardware/power-thermal-evidence.md) | 供电/散热异常如何表现为降频降速？健康摘要为什么不能排除它们？ |
| [Checkpoint 慢写与恢复 I/O 诊断指南](knowledge/04-data-storage/checkpoint-slow-io-triage.md) | 保存/恢复慢在 staging、后台写入、内核 writeback、后端还是读路径？ |
| [昇腾算子不支持与图编译失败诊断指南](knowledge/02-software-stack/ascend-op-graph-failure-triage.md) | 报错在框架注册层、算子编译层还是图模式层？ |
| [弹性训练与成员变更](knowledge/06-training/elastic-training-and-membership.md) | 成员变更如何达成一致？训练状态谁来恢复？ |
| [推理量化与输出质量验证](knowledge/07-inference/quantization-and-quality.md) | 量化支持矩阵怎么读？输出质量用什么证据验证？ |
| [Prefill/Decode 分离（PD 分离）与流量分配](knowledge/07-inference/pd-disaggregation.md) | PD 分离能优化什么、不能优化什么？connector 与流量分配各自归谁负责？ |
| [新节点与返修节点验收](knowledge/01-hardware/node-acceptance-triage.md) | 新节点/返修节点投产前，规格核对、被动证据、主动诊断与基准验收各提供什么强度的证据？ |
| [Checkpoint 完整性与校验证据](knowledge/04-data-storage/checkpoint-integrity-evidence.md) | 容器格式、框架元数据、存储 scrub、应用自检各能发现哪类损坏？ |

这些条目的 `source_checked` 只覆盖正文所列来源核对范围，不代表硬件验证。选定版本是研究样板，不是部署版本推荐；核查过程和缺口见[第一批来源记录](docs/research/batch-01-source-audit.md)、[第二批来源记录](docs/research/batch-02-source-audit.md)、[第三批来源记录](docs/research/batch-03-source-audit.md)、[第四批来源记录](docs/research/batch-04-source-audit.md)、[第五批来源记录](docs/research/batch-05-source-audit.md)、[第六批来源记录](docs/research/batch-06-source-audit.md)和[第七批来源记录](docs/research/batch-07-source-audit.md)。

## 场景专题

每组分别提供诊断流程、真实来源案例和待执行实验设计。

| 主题 | 指南 | 案例 | 实验 |
|---|---|---|---|
| 昇腾版本配套 | [诊断指南](knowledge/02-software-stack/ascend-version-mismatch-triage.md) | [来源案例](knowledge/02-software-stack/ascend-version-mismatch-source-case.md) | [实验设计](knowledge/02-software-stack/ascend-version-mismatch-experiment.md) |
| 容器内 NPU 可见性 | [诊断指南](knowledge/05-cluster-platform/ascend-device-visibility-triage.md) | [来源案例](knowledge/05-cluster-platform/ascend-device-visibility-source-case.md) | [实验设计](knowledge/05-cluster-platform/ascend-device-visibility-experiment.md) |
| HCCL 超时 | [诊断指南](knowledge/03-communication/hccl-timeout-triage.md) | [来源案例](knowledge/03-communication/hccl-timeout-source-case.md) | [实验设计](knowledge/03-communication/hccl-timeout-experiment.md) |
| NCCL 超时 | [诊断指南](knowledge/03-communication/nccl-timeout-triage.md) | [来源案例](knowledge/03-communication/nccl-timeout-source-case.md) | [实验设计](knowledge/03-communication/nccl-timeout-experiment.md) |
| 昇腾推理长尾 | [诊断指南](knowledge/07-inference/ascend-inference-tail-latency-triage.md) | [来源案例](knowledge/07-inference/ascend-inference-tail-latency-source-case.md) | [实验设计](knowledge/07-inference/ascend-inference-tail-latency-experiment.md) |
| GPU→NPU 精度差异 | [诊断指南](knowledge/06-training/gpu-npu-precision-difference-triage.md) | [来源案例](knowledge/06-training/gpu-npu-precision-difference-source-case.md) | [实验设计](knowledge/06-training/gpu-npu-precision-difference-experiment.md) |
| Checkpoint 恢复状态 | [诊断指南](knowledge/06-training/checkpoint-state-recovery-triage.md) | [来源案例](knowledge/06-training/checkpoint-state-recovery-source-case.md) | [实验设计](knowledge/06-training/checkpoint-state-recovery-experiment.md) |

## 初始载体

**Markdown 正文 + 少量 YAML 元数据**是本项目的内容源格式。Markdown 适合解释、图表、代码、案例和普通链接；文件可直接阅读、评审和纳入 Git。元数据使 Agent 能识别主领域、平台、来源和审核状态。

复杂的兼容矩阵、来源和实验配置可用独立 YAML/JSON，通过 ID 关联。大型日志、实时监控数据和证据附件单独存放。网站、搜索索引和 Agent 内容清单均由源文件生成。

目前没有部署网站、向量数据库、知识 API 或现场工具执行服务。可以先通过编辑器或仓库浏览器阅读 Markdown，后续发布网站时保留现有内容。

## 添加内容

首两轮记录见[详细填充计划](docs/population-plan.md)与[首轮内容任务清单](plans/content-backlog.yaml)。Batch 13 起按[完整覆盖路线图](docs/full-coverage-roadmap.md)与[执行清单](plans/full-coverage-backlog.yaml)推进，材料由[原来源工作包](plans/source-acquisition.yaml)和[补充工作包](plans/followup-source-acquisition.yaml)管理；真实证据单列[验证任务](plans/validation-backlog.yaml)，验证轨道的 V00 已知字段整理与准备实例骨架见 [V00 准备实例](plans/v00-preparation-instances.yaml)（全部 not_ready，未执行）。任务状态随交付更新，只有已创建的正文才计入内容产量。

先读[写作指南](docs/authoring-guide.md)，再选择模板：

- [概念](templates/concept.md)
- [参考](templates/reference.md)
- [操作或诊断流程](templates/procedure.md)
- [事故案例](templates/case.md)
- [验证实验](templates/experiment.md)

复制模板到对应领域，填写元数据和正文，再在章节首页添加链接。外部来源先登记到[来源表](sources/registry.yaml)，技术论断附近仍需指向具体资料位置。平台/任务页引用主目录内容。

首次准备校验环境（需要 Python 3.10+；依赖下载需要网络）：

```bash
make setup
```

内容检查与清单生成：

```bash
make check
make build
```

命令优先使用项目 `.venv`，没有该环境时使用当前 `python3`。构建生成 `build/catalog.md` 和 `build/catalog.json`：前者供人浏览，后者供 Agent 获取 ID、路径、元数据、来源及文件摘要。`build/` 可重建，不是内容源文件。

校验覆盖 YAML/JSON Schema、必填字段、ID 唯一性、主领域归属、来源与关系引用、内联 Markdown 本地文件链接。模板不作为正式内容校验。引用式链接、远程链接可达性、页内锚点、技术结论、证据语义及实际环境兼容性，仍需单独核验。

开发校验工具时安装开发依赖并运行回归测试：

```bash
make setup-dev
make test
```

## 文件分工

```text
knowledge/       00–08 系统领域正文与章节入口
paths/           平台、任务阅读路径
templates/       五类内容模板
sources/         外部来源、许可范围与版本状态
docs/            写作约定
config/          主目录登记
schemas/         元数据与来源的结构约束
src/kb/          结构校验及内容清单生成
tests/           校验工具的回归测试
build/           自动生成的导航与 Agent 清单
```

Agent 编辑内容前参阅[AGENTS.md](AGENTS.md)。

Git 日常操作、提交检查与远程备份说明见[版本管理指南](docs/git-workflow.md)。正文、来源、计划和审阅记录纳入版本管理，`build/`、本地环境与缓存通过忽略规则排除。

设计依据：[内容总目录](content-outline.md) · [架构建议](architecture-proposal.md) · [调研备忘录](research-memo-2026-09-29.md)。这些文档记录设计和调研，不属于已经完成的技术知识条目。

仓库自身的对外发布许可尚未决定；第三方内容保留各自许可与署名要求。初始来源登记以链接和许可范围说明为主，未镜像外部全文。
