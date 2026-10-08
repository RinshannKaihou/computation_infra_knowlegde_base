# 第十二批来源与交付记录

**最新审阅状态（2026-10-08）：** 用户约定的 `gpt-6.1-sol / xhigh` 审阅、修订与定向复核已完成；4 项 P2、2 项 P3 全部关闭，本批在原审阅范围内通过，见[本批报告](batch-12-codex-review.md)、[定向复核](batch-10-11-12-codex-recheck.md)和[三批汇总](batch-10-11-12-codex-review-summary.md)。旧替代复查与集成计数保留为历史，此前 astra 审阅义务已由用户新约定替代。

集成日期：2026-10-08。第二轮第五批（round-02 backlog 的 R2-13/14/15）由 Opus 编写。三个研究方向（PD 分离、节点验收、checkpoint 完整性）均由探索子代理按时完成取证，主任务核对关键行号后整合。全部保持 draft；一篇 procedure 与两篇 concept 均为限定来源范围的 source_checked。

## 本批正文

| 任务 | 正文 | 类型 |
|---|---|---|
| R2-13 | [Prefill/Decode 分离（PD 分离）与流量分配](../../knowledge/07-inference/pd-disaggregation.md) | concept |
| R2-14 | [新节点与返修节点验收](../../knowledge/01-hardware/node-acceptance-triage.md) | procedure |
| R2-15 | [Checkpoint 完整性与校验证据](../../knowledge/04-data-storage/checkpoint-integrity-evidence.md) | concept |

来源记录：[PD 分离](batch-12-pd-disaggregation-sources.md)、[节点验收](batch-12-node-acceptance-sources.md)、[checkpoint 完整性](batch-12-checkpoint-integrity-sources.md)。任务清单：[plans/round-02-backlog.yaml](../../plans/round-02-backlog.yaml)。

## 来源变化

新增 6 项登记（总计 84 项）：`src.nvidia.dcgm-diag-user-guide-latest-2026-10-08`、`src.nvidia.gpu-node-triage-2026-10-08`、`src.huawei.mindx-dl-60rc2-ascend-dmi-display-2026-10-08`、`src.ceph.docs-scrubbing-latest-2026-10-08`、`src.ceph.repo-caf3def`、`src.python.zipfile-docs-2026-10-08`。扩充 9 项既有登记 notes：vllm.inference-v0-14、vllm-ascend-v0-14-0rc1、dcgm-v3.3.9、dcgm-diagnostics-latest-2026-09-30、usenix.superbench-atc24、mindx-dl-60rc2-ascend-dmi-2026-09-29、dgx-h100-h200-user-guide-2026-01-26、pytorch.dcp-2.6、ascend.mindio-acp-v26.1.1。Ceph 侧 main 分支已解析并固定为 commit caf3def8088a17706021a8fd68ee40f62beda519（2026-10-07），man page 与许可行在该 commit 复核通过。来源工作包 A06（Ceph）由 planned 转为 collecting。

## 修订后的重点边界（2026-10-08）

- PD 分离：vLLM v0.14.0 官方明示"DOES NOT improve throughput"且标 experimental；connector 清单以固定 commit 的 factory.py 注册表（10 个）为准，全树无 SharedStorageConnector；流量分配是引擎之外的外部代理职责（toy 代理为轮询示例）；昇腾侧只按插件矩阵（Functional, xPyD）与限制条款（异构 P/D 不支持、非对称 TP 整除约束），教程内部版本引用落后于快照，只作步骤形态证据。
- 节点验收：四层证据不能互相替代，DCGM 两形态页清单差异继续保留；非零退出码含调用失败与诊断结果失败，需同时解析结果。AICore 软件前提、HOST 20–40GB 预算、单项耗时、诊断后重启/压测后分析再重启已补；测试完成不自动回服，失败/必需检查未覆盖/unknown 维持隔离，处置与收尾/复测/验收达标后才恢复。NPU 与 DCGM 级别/覆盖等价性仍未知，一次通过不证明完全无故障。
- checkpoint 完整性：DCP FileSystem 默认单桶与多线程分桶、False 时逐 item 文件布局已按参数/实现核对；.metadata 为 pickle，offset/length 定位文件内记录。所查路径未见独立内容摘要，关键词扫描不证明所有后端均无校验，形状断言不验证内容。CRC32 的结论限于 2.6 docstring；MindIO checker 是文件个数门控；Ceph 默认不自动修复，健康检查为 PG_DAMAGED 与 inconsistent 状态标志。完整性研究任务标签已修为 R2-15。
- 三篇正文均未执行真实环境验证；procedure 的 `environment_refs` 为空并注明缺失条件。

## 集成时检查与替代复查（历史）

`make check` / `make build` 通过：69 content entries / 84 sources（新增 3 篇正文、6 项来源），catalog 中三篇新条目标题与摘要已核对。

**独立审阅限制同前：当前环境没有 gpt-6-astra/xhigh 派发能力，本轮未能完成约定模型的独立审阅。** 替代措施：同环境只读子代理定向复查（[复查记录](batch-12-substitute-review.md)）；发现与修订以该记录为准。该复查不构成 astra/xhigh 独立审阅；本批的约定模型审阅义务保留。三篇正文保持 draft、限定范围 source_checked，无 reproduced，无任何环境执行结果。
