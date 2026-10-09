# 第十三批来源记录：统一术语、先修关系与系统责任边界（T00-01）

研究日期：2026-10-08。研究者：探索子代理（非 gpt-6.1-sol）。目标正文：`knowledge/00-overview/terms-and-system-boundaries.md`（reference，planned，验收标准见 plans/full-coverage-backlog.yaml T00-01）。范围：两本开源知识书的固定版本与章节定位、SRE 排障章归属核对、三组同名异义的可引用实例。未执行任何集群/设备操作；除本文件外未改动仓库其他文件。

## 固定版本与章节定位

| 来源 | 固定版本（2026-10-08 获取） | 许可核查 | 本次选用章节 |
|---|---|---|---|
| [stas00/ml-engineering](https://github.com/stas00/ml-engineering) | master `fb75494c0d9e536f048e27be2869a77fe65ad9f4` | GitHub license API 确认 CC-BY-SA-4.0，文件名为 `LICENSE-CC-BY-SA`（无裸 LICENSE） | `compute/accelerator/README.md`（加速器总览）、`network/README.md` 与 `network/comms.md`（p2p/RMA/collective 图解）、`orchestration/README.md`（Slurm/Kubernetes/Slinky）、`debug/README.md`（排障索引）、`training/fault-tolerance/` 与 `training/checkpoints/` |
| [Infrasys-AI/AIInfra](https://github.com/Infrasys-AI/AIInfra) | main `b97c0385ba07a62a717d82a0e7aed2927f12fc35`（最后提交 2025-12-22） | 根 `LICENSE` 为 Apache-2.0（ZOMI 版权，正文）；`LICENSE-CODE` 为 MIT（Microsoft 版权，疑站点模板遗留，范围待逐文件核对）→ registry 可由 unknown 更新为 partial | `00Summary/`、`01AICluster/02L0L1Base`（服务器/机柜/供电）、`01AICluster/03SuperPod`、`03DockCloud/03DiveintoK8s/05K8sRuntime.md`、`04Train/`、`05Infer/`；注意多节自标 `:o:` 未完成，`07Application/07Safe` 是应用安全而非基础设施可靠性 |
| [Google SRE — Effective Troubleshooting](https://sre.google/sre-book/effective-troubleshooting/) | SRE Book（2016）第 12 章；2026-10-08 复核可访问 | 已登记，status unknown 维持 | 假设—演绎定义句："given a set of observations … we iteratively hypothesize potential causes for the failure and try to test those hypotheses."归属修正：属 SRE Book 而非 workbook（workbook 目录无此章，已核对） |

## 同名异义主张—证据表（URL 均已 2026-10-08 打开核对）

| 主张 | 来源与定位 | 版本/日期 | 证据性质 | 反例/未知 |
|---|---|---|---|---|
| worker 在 Kubernetes 指运行负载的节点机器："a set of worker machines, called nodes … worker node(s) host the Pods" | [Kubernetes Cluster Architecture](https://kubernetes.io/docs/concepts/architecture/) | 可变网页，2026-10-08 观察 | 官方文档原文 | PyTorch DataLoader 的 worker 是子进程；torchrun/elastic 语境的 worker 又指训练进程 |
| worker 在 PyTorch DataLoader 指加载子进程（`num_workers` "multi-process data loading … worker processes"） | [PyTorch 2.6 torch.utils.data](https://docs.pytorch.org/docs/2.6/data.html)（已登记 src.pytorch.data-loader-2.6） | 2.6 | 官方文档原文 | 与 K8s worker node 无语义交集 |
| CUDA 栈内 runtime 构建于 driver API 之上（Introduction 及 §17/§20.3 两 API 并列） | [CUDA C++ Programming Guide 12.8](https://docs.nvidia.com/cuda/archive/12.8.0/cuda-c-programming-guide/index.html)（已登记 src.nvidia.cuda-toolkit-12-8） | 12.8 归档 | 官方文档原文 | Kubernetes container runtime 是 kubelet 经 CRI 驱动的节点组件，另一层概念 |
| container runtime 是 CRI 之后的节点组件 | [Kubernetes CRI](https://kubernetes.io/docs/concepts/architecture/cri/) | 可变网页，2026-10-08 观察 | 官方文档原文 | 候选新登记 src.kubernetes.cri-2026-10-08 |
| 「checkpoint/状态」在训练框架指可恢复训练状态（"you will lose progress up to the most recent checkpoint"） | [PyTorch 2.6 elastic train_script](https://docs.pytorch.org/docs/2.6/elastic/train_script.html)（已登记 src.pytorch.elastic-2.6） | 2.6 | 官方文档原文 | 集群平台的状态是调度相位；与下一行激活重算机制分开 |
| gradient/activation checkpointing 在前向少保存部分中间张量，反向重算，以计算换内存；该机制本身不提供训练状态持久化 | [PyTorch 2.6 torch.utils.checkpoint.checkpoint](https://docs.pytorch.org/docs/2.6/checkpoint.html#torch.utils.checkpoint.checkpoint)（src.pytorch.activation-checkpoint-2.6） | 2.6，2026-10-09 重取 | 官方机制说明；持久化区别为本库据此作出的术语归纳 | 2026-10-09 B13-R05 修订：AIInfra 固定 b97c0385 的 04Train/03TrainAcceler/08Checkpoint.md 只有未完成提示和占位，撤下其技术主张引用，仍可作章节组织入口；未运行 PyTorch |
| 集群平台作业/容器组状态是调度相位（`status.phase`: pending/running/unknown/inqueue） | [Volcano v1.15.0 PodGroup](https://volcano.sh/docs/v1.15.0/concepts/podgroup/) | v1.15.0 文档 | 官方文档 status 定义 | 候选新登记 src.volcano.podgroup-v1.15.0 |

## 候选登记/更新

- 更新 `src.stas.ml-engineering`：回填 revision 为上述 commit；notes 补充许可证文件名 `LICENSE-CC-BY-SA`。
- 更新 `src.infrasys.aiinfra`：回填 revision；license 由 unknown 改为 partial（正文 Apache-2.0 / LICENSE-CODE MIT 两 scope，后者主体为 Microsoft、范围待核）；notes 补充多节自标未完成、内容含 PPT/视频引用。
- 新增 `src.kubernetes.cluster-architecture-2026-10-08`（worker node 定义）、`src.kubernetes.cri-2026-10-08`（CRI/container runtime 定义）、`src.volcano.podgroup-v1.15.0`（调度相位例）。均为可变或版本化官方网页，只链接+原创归纳。

## 缺口与边界

- 两本书用于术语的通用组织与中文对照入口，具体命令/支持能力一律回查厂商版本化资料（本书不作兼容性证据）。
- AIInfra 的 LICENSE-CODE 归属异常（Microsoft）已记录，不据此复制任何代码片段。
- 术语表只覆盖原目录九领域用到的概念，不建立无限词典；未列入的术语不代表不存在同名异义。
