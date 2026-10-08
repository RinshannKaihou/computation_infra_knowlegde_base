# 第十二批审阅记录（gpt-6.1-sol / xhigh）

**修订后最终状态（2026-10-08）：** 4 项 P2、2 项 P3 已逐项修订并定向复核关闭，本批在初审范围内通过，见[定向复核](batch-10-11-12-codex-recheck.md)。下文初审发现、原输入位置与当时结论保留为历史。

审阅日期：2026-10-08。审阅者：本会话 Codex 主助手，运行上下文确认模型为 `gpt-6.1-sol / xhigh`；正文编写者为 Opus。重新核对上游证据，未派发子代理。此前[替代复查](batch-12-substitute-review.md)保留为历史。

**初审结论（历史）：审阅完成，暂不通过；4 项 P2、2 项 P3 开放，无 P1。** 对象身份、统计与结构检查见[汇总](batch-10-11-12-codex-review-summary.md)。

## 范围与实际证据核对

完整读取[PD 分离](../../knowledge/07-inference/pd-disaggregation.md)、[节点验收](../../knowledge/01-hardware/node-acceptance-triage.md)、[Checkpoint 完整性](../../knowledge/04-data-storage/checkpoint-integrity-evidence.md)，三份研究记录、来源审计及 registry/任务/导航。

| 主题 | 本次重新取得并核对的证据 | 覆盖与限制 |
|---|---|---|
| PD 分离 | vLLM `b17039bc…` 的 disagg_prefill.md、factory.py、offloading_connector.py 前 80 行；插件 `52d4acfa…` 的 PD 特性指南和支持矩阵 | 动机、experimental、10 个注册项及异构/TP 限制有证据；跨 connector 的替代关系没有由注册表证明。本次未全树重扫 SharedStorageConnector、未复验失败策略或部署性能 |
| 节点验收 | [DCGM user-guide](https://docs.nvidia.com/datacenter/dcgm/latest/user-guide/dcgm-diagnostics.html)、[learn diagnostics](https://docs.nvidia.com/datacenter/dcgm/latest/learn/modules/dcgm-diagnostics.html)、[DGX 规格](https://docs.nvidia.com/dgx/dgxh100-user-guide/introduction-to-dgxh100.html)、[ascend-dmi 6.0.RC2](https://www.hiascend.com/doc_center/source/zh/mindx-dl/60rc2/toolbox/ascenddmi/toolboxug_0020.html)、[SuperBench v2](https://arxiv.org/html/2402.06194v2) | 核对 r1–r4 表、退出码、诊断边界、AICore 前提与收尾、群体判据及仿真/生产统计的区别；没有主动诊断或验收实测 |
| Checkpoint 完整性 | PyTorch `1eba9b3…` 的 filesystem.py、serialization.py；MindCluster `44385c13…` 的 register_checker 接口、framework_acp.py；[Ceph 配置](https://docs.ceph.com/en/latest/rados/configuration/osd-config-ref/)与[health checks](https://docs.ceph.com/en/latest/rados/operations/health-checks/) | 确认 pickle metadata、默认 CRC 选项、文件个数门控、scrub 和默认自动修复关闭；未重做 DCP 全包扫描、C++ CRC 路径或损坏注入 |

既有登记为 `src.vllm.inference-v0-14`、`src.ascend.vllm-ascend-v0-14-0rc1`、DCGM user-guide/learn 两项、`src.nvidia.dgx-h100-h200-user-guide-2026-01-26`、`src.huawei.mindx-dl-60rc2-ascend-dmi-2026-09-29`、`src.usenix.superbench-atc24`、`src.pytorch.dcp-2.6`、`src.ascend.mindio-acp-v26.1.1`、`src.ceph.docs-scrubbing-latest-2026-10-08`。本次文档抓取的 latest 内容与历史固定代码快照分别理解。

## 初审发现（历史，已关闭）

### B12-C01 / P2：DCGM 非零退出码也能表达诊断已运行且失败

- 位置：[节点验收](../../knowledge/01-hardware/node-acceptance-triage.md)步骤 6，第 69 行。
- 问题：“非零只代表请求/启动/连接错误”漏掉诊断失败，可能导致自动化把真实检出当基础设施调用失败。
- 证据：[user-guide 的 Exit Codes](https://docs.nvidia.com/datacenter/dcgm/latest/user-guide/dcgm-diagnostics.html#exit-codes)列出 226 / `DCGM_ST_NVVS_ERROR`（诊断成功执行但报错）和 205 / `DCGM_ST_NVVS_ISOLATE_ERROR`（需要隔离）；[learn 的 Exit status](https://docs.nvidia.com/datacenter/dcgm/latest/learn/modules/dcgm-diagnostics.html#exit-status)也包括 diagnostic error。
- 关闭条件：分清调用/启动/连接失败与诊断结果失败，保留解析每测试/每 entity 状态、warning 和 skipped 的要求；退出码不足以判定硬件根因，但也不能忽略其诊断失败含义。

### B12-C02 / P2：测试完成直接恢复节点，遗漏 AICore 前提与收尾

- 位置：[节点验收](../../knowledge/01-hardware/node-acceptance-triage.md)步骤 4、第 73–77 行停止/恢复安排与适用前提。
- 问题：正文要求主动测试“完成后”按 drain 记录恢复，没有明确失败/跳过/未判定时维持隔离的门槛；AICore 支路也遗漏同一官方页的具体资源与收尾要求，并将影响量级笼统写为未量化。
- 证据：[ascend-dmi 页的使用说明与前提条件](https://www.hiascend.com/doc_center/source/zh/mindx-dl/60rc2/toolbox/ascenddmi/toolboxug_0020.html)明确 AICore 压测占 HOST 约 20–40GB 内存，诊断完成需重启设备，压测完成需先分析定位再重启，并列 HDK 23.0.0+、CANN 7.0.0+及算子包前提；[DCGM learn](https://docs.nvidia.com/datacenter/dcgm/latest/learn/modules/dcgm-diagnostics.html#when-diagnostics-are-useful)将回服前长测和故障处置放在管理员工作流。
- 关闭条件：按检查项补前提、HOST 内存预算和完成后的动作条件；恢复服务以问题处置、必要重启/复测和验收判据满足为门槛，失败/证据不足维持隔离并记录下一步。重启等真实动作仍依用户授权与现场窗口，不由本文授予权限。同步来源研究记录与 registry 的核对范围。

### B12-C03 / P2：FileSystemWriter 文件布局被错误地固定为每个 request 一个文件

- 位置：[Checkpoint 完整性](../../knowledge/04-data-storage/checkpoint-integrity-evidence.md)第 47 行；[研究记录](batch-12-checkpoint-integrity-sources.md)A 表首行。
- 问题：默认 `single_file_per_rank=True`、`thread_count=1` 时，多个 write item 放入同一分桶数据文件；多线程时按桶组织，关闭 single_file_per_rank 才按 item 建文件。“每个 write request 一个 .distcp”不能作为默认布局或完整性检查的文件数预期。
- 证据：[filesystem.py L447–463](https://github.com/pytorch/pytorch/blob/1eba9b3aa3c43f86f4a2c807ac8e12c4a7767340/torch/distributed/checkpoint/filesystem.py#L447-L463)和[write_data L507–534](https://github.com/pytorch/pytorch/blob/1eba9b3aa3c43f86f4a2c807ac8e12c4a7767340/torch/distributed/checkpoint/filesystem.py#L507-L534)。metadata 的 offset/length 正用于定位文件中的多个记录。
- 关闭条件：按参数/分桶描述布局，实际文件集以写入计划与 metadata 为准；同步研究记录，不从 tensor/request 数直接推出数据文件数量。

### B12-C04 / P2：“不承诺提升吞吐”被扩展成不评估总吞吐

- 位置：[PD 分离](../../knowledge/07-inference/pd-disaggregation.md)第 36 行，官方声明之后的评估建议。
- 问题：上游声明该版本 PD 分离不提高吞吐，正文进一步建议只看 TTFT/ITL、排除总吞吐。这个建议不由来源推出；只报告时延可能掩盖吞吐、失败率或资源投入的变化，无法判断同等成本/负载下的服务能力。
- 证据：[固定 disagg_prefill.md L10–16](https://github.com/vllm-project/vllm/blob/b17039bccc17b94a2ea107272ad7bc93508708df/docs/features/disagg_prefill.md#L10-L16)只有动机与吞吐声明。补充评估建议属于本库方法判断，需与上游原文分开。
- 关闭条件：保留版本限定的官方声明，同时在固定负载和资源预算下联合观察 TTFT/ITL、吞吐/goodput、失败率及 KV 传输成本；不以改善时延单独宣称部署获益，不把吞吐变化冒充本库已有实测。

### B12-C05 / P3：不存在某 connector 不证明其他 connector 是其替代物

- 位置：[PD 分离](../../knowledge/07-inference/pd-disaggregation.md)第 41 行与[研究记录](batch-12-pd-disaggregation-sources.md)冲突项 2。
- 问题：从 SharedStorageConnector 未出现，推出旧“共享存储 connector”的对应物为 Offloading/LMCache 系。注册表只能证明名称注册；本次取得的 OffloadingConnector 入口接入 KV offload 架构，并未证明共享存储跨实例 P/D 传输或旧接口兼容关系。
- 证据：[factory.py L146–203](https://github.com/vllm-project/vllm/blob/b17039bccc17b94a2ea107272ad7bc93508708df/vllm/distributed/kv_transfer/kv_connector/factory.py#L146-L203)与[offloading_connector.py L24–65](https://github.com/vllm-project/vllm/blob/b17039bccc17b94a2ea107272ad7bc93508708df/vllm/distributed/kv_transfer/kv_connector/v1/offloading_connector.py#L24-L65)。
- 关闭条件：保留实际注册清单，删除未经证明的对应/替代关系；若保留，补具体后端、跨实例传输和版本迁移依据，区分缓存卸载与 PD 传输。

### B12-C06 / P3：完整性研究记录标错任务编号

- 位置：[完整性研究记录](batch-12-checkpoint-integrity-sources.md)第 1 行。
- 问题：标题标 R2-12；[backlog](../../plans/round-02-backlog.yaml)中 R2-12 是量化质量，本篇为 R2-15。研究记录会被错误关联到另一批/另一主题。
- 关闭条件：更正研究记录任务标签为 R2-15，核对 source-audit、backlog、稳定 content ID 的映射；正文稳定 ID 保持不变。

## 初审结束状态（历史）

B12-C01–C06 均开放。三篇继续 `draft / source_checked`。pickle metadata、CRC 选项和文件个数门控有固定证据，但仅关键词扫描不能证明所有 DCP 后端/路径均无校验；对 payload 的形状检查也不等于对所有同长度损坏都没有任何解析错误。这些范围在后续修订时应继续限定。没有任何服务部署、设备诊断、损坏注入或修复实测。

## 修订后最终状态

B12-C01–C06 全部 CLOSED。具体改动、与上游证据的定向对照及修订后文件身份见[复核记录](batch-10-11-12-codex-recheck.md)。本批在原审阅范围内通过；三篇仍为 `draft / source_checked`，没有真实环境执行结果。
