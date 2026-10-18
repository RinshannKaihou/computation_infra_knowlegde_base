# 第二十三批来源审计（T05-06/T05-07/T05-08/T05-09）

更新日期：2026-10-18。状态：**Batch 23 已交付并通过审阅**；四篇正文均为 `draft`，未做真实环境验证。

## 本批任务状态

| 任务 | 操作 / 类型 | 目标文件 | 最终状态 |
|---|---|---|---|
| T05-06 加速器共享与租户隔离机制 | 新增 / concept | `knowledge/05-cluster-platform/accelerator-sharing-and-isolation.md` | **通过审阅**：初审 4 P1/2 P2/1 P3 + 复核新增 R01–R06，初审 + 7 轮定向复核后全部 CLOSED；Ascend 共享分支已用官方 vNPU/vCANN 文档补齐；跨 vNPU 故障隔离/QoS 保留 unknown |
| T05-07 多租户争用、公平性与容量验证 | 新增 / procedure | `knowledge/05-cluster-platform/contention-capacity-validation.md` | **通过审阅**：初审 7 P2 + R01，初审 + 3 轮定向复核后全部 CLOSED；未执行 |
| T05-08 节点摘除、drain 与资源回收流程 | 新增 / procedure | `knowledge/05-cluster-platform/node-drain-resource-reclamation.md` | **通过审阅**：初审 2 P1/6 P2/1 P3 + R01，初审 + 4 轮定向复核后全部 CLOSED；未执行 drain/驱逐 |
| T05-09 平台组件升级、发布、回退与回服 | 新增 / procedure | `knowledge/05-cluster-platform/platform-change-and-rollback.md` | **通过审阅**：初审 8 P2/1 P3，初审 + 3 轮定向复核后全部 CLOSED；未执行升级/回退 |

## 来源准备

- 新增登记 **24** 项，`sources/registry.yaml` 由 446 增至 **470**（无重复 ID）；`make check` / `make build` 通过（100 content entries / 470 sources）。
- 单任务来源记录：
  - `docs/research/batch-23-t05-06-sources.md`（作者侧直接取证＋审阅补充；MIG Guide supported-gpus/concepts/deployment-considerations、MPS index/when-to-use、k8s-device-plugin v0.20.1 README 共享节、A100 显存错误恢复、Ascend 组件 README 与 HDK/vCANN-RT 虚拟化文档）
  - `docs/research/batch-23-t05-07-sources.md`（作者侧直接取证；Kueue v0.19.0 fair sharing 两页、Slurm 24.11.7 sshare）
  - `docs/research/batch-23-t05-08-sources.md`（只读取证子代理；Kubernetes v1.32 静态快照 12 页次、Slurm 24.11.7 slurmd/power_save/scontrol 重开）
  - `docs/research/batch-23-t05-09-sources.md`（只读取证子代理；K8s version skew/kubeadm、Slurm upgrades/quickstart、GPU Operator 25.3、MindCluster v26.1.1）
- 取证方式：全部为 FetchURL 只读或固定 commit/归档页实开；未做 curl 字节级取回与哈希校验；未部署、未提交任务、未执行 drain/升级。
- 取证限制：审阅轮中 codex 对 `slurm.schedmd.com` 归档页多次访问失败（DNS/网页工具），改用 SchedMD 官方仓库 `slurm-24-11-7-1` tag 指向的同版本源码补证；这不等于归档 HTML 字节已由审阅者复核。作者侧此前 FetchURL 实开成功，两轮证据强度分别记录。
- 子代理配额说明：4 路取证中 T05-08/T05-09 完成；T05-06/T05-07 因子代理账户周配额（403）失败，改由主会话作者角色直接取证并记录同一口径。

## 新增登记条目

T05-06：`src.nvidia.mig-user-guide-2026-10-18`、`src.nvidia.mps-docs-2026-10-18`、`src.nvidia.k8s-device-plugin-sharing-v0.20.1`、`src.ascend.ascend-device-plugin-44385c13`；审阅补充 `src.nvidia.mig-deployment-considerations-2026-10-18`、`src.nvidia.a100-mem-error-recovery-2026-10-18`、`src.nvidia.k8s-device-plugin-mps-v0.20.1`、`src.ascend.virtual-instance-hdk-44385c13`、`src.ascend.virtual-instance-vcann-44385c13`。

T05-07：`src.kueue.fair-sharing-v0.19.0`、`src.slurm.sshare-24.11.7`。

T05-08：`src.kubernetes.node-drain-v1-32`、`src.kubernetes.eviction-pdb-v1-32`、`src.kubernetes.node-shutdown-v1-32`、`src.kubernetes.node-lifecycle-v1-32`、`src.kubernetes.daemonset-static-pod-v1-32`、`src.kubernetes.storage-reclaim-v1-32`、`src.slurm.node-power-lifecycle-24.11.7`。

T05-09：`src.kubernetes.version-skew-v1-32`、`src.kubernetes.kubeadm-upgrade-v1-32`、`src.slurm.upgrades-24.11.7`、`src.nvidia.gpu-operator-upgrade-25.3`、`src.nvidia.gpu-operator-platform-support-25.3`、`src.ascend.mind-cluster-upgrade-v26.1.1`。

## 证据边界

- T05-06：NVIDIA 文档为 2026-10-18 观察的可变页。Ascend 侧已取得官方 HDK 虚拟化实例（静态/动态 vNPU、产品支持表、模板、分配/回收约束）与 vCANN-RT 软切分文档；**跨 vNPU 的故障隔离与性能 QoS 保证、固件/CANN 最低版本矩阵仍保留 unknown**，不以 GPU 机制类推。
- T05-07：Kueue 默认参数、Slurm 站点权重与 decay、两租户实测数据均未取得；官方共享限制仅作语义案例，不含性能数字；MIG 的隔离承诺已限定到独立 GI。
- T05-08：Kubernetes 为 v1.32 静态快照、Slurm 为 24.11.7 归档（审阅轮以同版本源码补证）；站点 PDB/超时/`ReturnToService` 参数、CSI detach 驱动行为与 Ascend 节点摘除行为未取得。
- T05-09：GPU Operator 仅支持同 major 或下一 major；算子回退/驱动降级无官方步骤；K8s 无官方 downgrade；Slurm 大版本状态/数据库迁移后不可原地降级（维护补丁按 Minor Upgrades 逐 release 判断）；MindCluster 无官方灰度/波次说明。

## 结构检查

- `make check`：PASS（100 content entries / **470** sources）。
- `make build`：PASS，生成 `build/catalog.json`、`build/catalog.md`。
- 以上只证明结构与本地链接，不证明技术正确或远程内容。

## 审阅与复核

- 审阅约定：`claude-opus-5-5` 优先；若出现 fallback（模型不一致、`[frontier_llm]` 标记、认证/路由失败），该轮弃用并切换 `gpt-6.1-sol / xhigh`。
- **2026-10-18 弃用记录**：首轮以 `claude-opus-5-5` 派发四路；其中一路报告自述会话中途模型标识由 `claude-opus-5-5` 变为 `claude-opus-5`，属实际执行模型与指定不一致。按 2026-10-13 约定，该批 claude 轮次全部弃用：报告已删除、不引用、不计入轮次；改用 `codex` 的 `gpt-6.1-sol / xhigh` 重新初审。
- **初审与定向复核结果（全部 CLOSED）**：
  - T05-06：初审 4 P1/2 P2/1 P3（C01–C07）+ 复核新增 R01–R06；初审 + 7 轮定向复核后全部 CLOSED。关键收敛：Ascend HDK/vCANN 共享模型与配套样板、MIG 独立 GI/CI 边界、MPS/time-slicing 有限样板（A100 + CUDA 11 + R525 + 插件 v0.20.1，Legacy v2、动态限额）、runtime 选路（默认 NVIDIA runtime 或 RuntimeClass）、组件职责分层。
  - T05-07：初审 7 P2（C01–C07）+ R01；初审 + 3 轮定向复核后全部 CLOSED。关键收敛：MIG 承诺限定、基线稳定性门槛、B 基线/可比性、初态控制方法、Slurm 有效权重与因子贡献、控制生效证据、时间分辨与三分类结果、MPS 安全退出、Ascend 来源追溯。
  - T05-08：初审 2 P1/6 P2/1 P3（C01–C09）+ R01；初审 + 4 轮定向复核后全部 CLOSED。关键收敛：恢复三层门槛、关机两路径、PDB 三分支、cordon/DS 边界、取消/重排分离、COMPLETING/身份账本、数据前置、状态例子与受控验证、429 归因。
  - T05-09：初审 8 P2/1 P3（C01–C09）；初审 + 3 轮定向复核后全部 CLOSED。关键收敛：人工重试语义、驱动波次默认值、MindCluster 路径条件、Helm 两 Release 对应、HA skew 交集与 kube-proxy 双约束、local etcd、旧 stepd 完成门槛、维护补丁例外、三态回服门禁。
- **模型核验（调用方）**：初审与全部定向复核均以 `codex exec -m gpt-6.1-sol --config model_reasoning_effort="xhigh"` 启动。调用方读取 `~/.codex/sessions/2026/10/18/` 下对应 rollout（初审 16:25 四份；复核 17:04–17:52 各份）的 `turn_context`，均为单一 `model=gpt-6.1-sol`、`effort=xhigh`，未见 fallback 标记或模型切换。部分审阅报告内写 unknown 是审阅者侧的保守记录，已由调用方补核；不改变报告结论。
- **证据访问限制**：审阅轮中 codex 对 `slurm.schedmd.com` 归档页多次访问失败（DNS/网页工具），改用 SchedMD 官方仓库 `slurm-24-11-7-1` tag 指向的同版本源码补证；作者侧此前 FetchURL 实开成功。两轮证据强度分别记录，未声称归档 HTML 字节已由审阅者复核。
- **最终结论**：四任务均通过既定审阅与定向复核范围；模型审阅不替代真实硬件、升级、回退或回服演练，正文保持 `draft`。

## 待办

1. ~~汇总四份初审发现并修订正文/来源记录~~（已完成）。
2. ~~定向复核至发现全部关闭；如复核新增问题，继续修订与再复核~~（已完成；四任务全部 CLOSED）。
3. ~~主题范围复核：05.1-G3、05.4-G2、05.5-G1/G2/G3、05.6-G1/G2/G3；更新 `plans/topic-coverage.yaml`、`docs/topic-coverage-audit.md`、backlog 任务/批次状态与路线图“续作入口”~~（已完成；8 缺口关闭，05.1/05.4/05.5/05.6 升为已覆盖基础）。
4. 保留 Batch 17–21 主题范围复核的既有待办（不在本批内顺带处理）。
5. 真实环境验证仍属独立轨道：T05-06 的共享隔离实测、T05-07 的两租户对照、T05-08 的 drain/回收演练、T05-09 的升级/回退/回服演练均未执行，相关验证包（V11 等）继续跟踪。
