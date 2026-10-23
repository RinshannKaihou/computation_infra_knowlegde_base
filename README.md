# AI 算力基础设施与计算可靠性知识库

主要服务昇腾用户，面向 Human 与 Agent，提供系统学习、资料查询和工程判断参考。内容覆盖 GPU/NPU、训练/后训练/推理，按系统领域组织；其他平台内容用于比较和按需查阅。

**当前处于使用与按需维护阶段，批量内容建设已结束。** 暂无实测或故障注入环境；来源核对与未验证说明随正文保留，不妨碍学习和查询。旧路线图、批次、交接和模型/CLI 约定已退出当前执行流程。

[当前状态与使用方式](docs/current-status.md) · [昇腾入口](paths/platforms/ascend.md) · [历史归档](docs/archive/README.md)

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

## 内容选读

下面是各类问题的代表入口，完整内容见各领域首页。本地执行 `make build` 后，还可使用 `build/catalog.md` 和 `build/catalog.json` 浏览完整清单。

| 内容 | 可以帮助回答的问题 |
|---|---|
| [统一术语、先修关系与系统责任边界](knowledge/00-overview/terms-and-system-boundaries.md) | 如何区分设备、节点、rank、后端与控制面责任？ |
| [单机、集群与超节点的参考架构及选择](knowledge/00-overview/reference-architectures.md) | 系统如何组织，共享依赖和规模约束在哪里？ |
| [计算节点资源与拓扑参考](knowledge/01-hardware/resource-topology.md) | CPU、内存、设备和互联的资源关系怎样记录？ |
| [新节点与返修节点验收](knowledge/01-hardware/node-acceptance-triage.md) | 如何分层验收并保留环境与证据？ |
| [三平台安装基线、迁移升级与回退验证](knowledge/02-software-stack/environment-installation-and-upgrade.md) | 如何检查安装条件、版本变化和恢复路径？ |
| [三套通信库能力与版本条件档案](knowledge/03-communication/communication-library-profiles.md) | NCCL、RCCL、HCCL 的能力、运行条件和未知项如何分别判断？ |
| [本地与共享文件存储](knowledge/04-data-storage/local-and-shared-storage.md) · [对象与并行存储](knowledge/04-data-storage/object-and-parallel-storage.md) | 缓存、一致性、持久性和恢复语义怎样分开？ |
| [Kubernetes 作业生命周期](knowledge/05-cluster-platform/kubernetes-job-lifecycle.md) · [Slurm 作业与设备资源](knowledge/05-cluster-platform/slurm-jobs-and-device-resources.md) | 准入、调度、设备分配和应用进展各由谁负责？ |
| [RL rollout、权重同步与训练推理协同](knowledge/06-training/rl-rollout-consistency.md) | 策略版本、样本身份与失败重放怎样关联？ |
| [权重加载、引擎 ready 与启动失败诊断](knowledge/07-inference/model-loading-and-readiness.md) | 权重加载、探针成功与真正就绪如何区分？ |
| [隔离、重试预算、降级与恢复选择](knowledge/08-reliability/mitigation-and-recovery-principles.md) | 如何选择处置动作并验证恢复？ |
| [可靠性统计、有效产出与恢复损失](knowledge/08-reliability/reliability-metrics-and-recovery-loss.md) | 如何统一统计窗口、分母和恢复代价？ |

`source_checked` 只覆盖各正文声明的来源核对范围；文档样板、模型审阅和实验设计均不表示本库已完成现场验证。

## 场景专题

高频排障快速分流：[NCCL 超时](knowledge/03-communication/nccl-timeout-triage.md#快速分流先找下一项检查) · [GPU 推理 OOM（NVIDIA/AMD）](knowledge/07-inference/gpu-inference-oom-triage.md#快速分流先找下一项检查) · [Checkpoint 恢复](knowledge/06-training/checkpoint-state-recovery-triage.md#快速分流先找下一项检查)。三篇首屏按“现象→证据→判断分支→下一项检查”组织，详细机制与来源保留在下层；这些是文档入口，未经过现场验证。

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

## 内容格式与使用边界

**Markdown 正文 + 少量 YAML 元数据**是本项目的内容源格式。Markdown 适合解释、图表、代码、案例和普通链接；文件可直接阅读、评审和纳入 Git。元数据使 Agent 能识别主领域、平台、来源和审核状态。

复杂的兼容矩阵、来源和实验配置可用独立 YAML/JSON，通过 ID 关联。大型日志、实时监控数据和证据附件单独存放。当前构建从源文件生成导航目录与 Agent 静态内容清单。

目前没有部署网站、向量数据库、知识 API 或现场工具执行服务。可以先通过编辑器或仓库浏览器阅读 Markdown，后续发布网站时保留现有内容。

## 按需维护

围绕实际问题、发现的错误和来源变化维护正文，不按旧批次继续填充。按主题的主要归属维护内容，外部资料登记在[来源表](sources/registry.yaml)。需要编辑时阅读[写作指南](docs/authoring-guide.md)；日常查询从上方阅读入口进入即可。

真实验证和独立评测仍无执行证据。[原验证计划](plans/validation-backlog.yaml)与[准备实例](plans/v00-preparation-instances.yaml)作为未来可选方案保留；待有具体需求与相应条件时再选择适用部分，不是当前排期或知识库使用门槛。

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
docs/            写作约定、维护记录与历史归档
config/          主目录登记
schemas/         元数据与来源的结构约束
src/kb/          结构校验及内容清单生成
tests/           校验工具的回归测试
build/           自动生成的导航与 Agent 清单
```

Agent 编辑内容前参阅[AGENTS.md](AGENTS.md)。

Git 日常操作、提交检查与远程备份说明见[版本管理指南](docs/git-workflow.md)。正文、来源、计划和审阅记录纳入版本管理，`build/`、本地环境与缓存通过忽略规则排除。

[内容地图与归属边界](content-outline.md)继续用于维护主目录。[早期架构建议](architecture-proposal.md)与[调研备忘录](research-memo-2026-09-29.md)已归档，记录当时的设计设想，不作为当前开发待办或能力声明。

## 许可证

除另有声明外，本项目原创代码、文档、配置和模板均采用 [Apache License 2.0](LICENSE)。许可证全文来自 [Apache 官方](https://www.apache.org/licenses/LICENSE-2.0.txt)。

第三方内容、依赖及外部引用材料保留各自的版权、许可与署名要求，不因本项目采用 Apache-2.0 而改变。具体来源与许可范围见[来源登记表](sources/registry.yaml)；本库以链接和原创归纳为主，未镜像外部全文。

## 当前状态与历史记录

[当前状态与待确认项](docs/current-status.md) · [历史归档索引](docs/archive/README.md)。详细覆盖基线和旧计划按需从归档索引查阅；来源审计与原评审报告保留原路径供追溯。

[2026-10-22 独立质量审计](docs/research/independent-quality-audit-2026-10-22.md) · [IQ-01–IQ-08 修订与定向核对](docs/research/independent-quality-audit-2026-10-22-fixes.md)
