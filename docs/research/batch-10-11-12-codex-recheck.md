# Batch 10、11、12 修订与定向复核（gpt-6.1-sol / xhigh）

日期：2026-10-08。用户在初审后要求“直接进行修正”。修订与复核由同一会话 Codex 主助手 `gpt-6.1-sol / xhigh` 分阶段完成，原正文编写者为 Opus；本次未另派审阅代理。

**技术定向复核结论：13 项唯一发现（1 P1、9 P2、3 P3）全部关闭，三批在初审范围内通过。** 这是正文与来源证据的修订闭环，不是设备/作业/部署验证。初审问题、输入 SHA-256 和当时的未通过结论分别保留于[batch 10](batch-10-codex-review.md)、[batch 11](batch-11-codex-review.md)、[batch 12](batch-12-codex-review.md)及[汇总](batch-10-11-12-codex-review-summary.md)。

## 逐项关闭依据

逐项重读修订后的正文和研究记录，与初审关闭条件及固定来源对照；登记中的相同主张同步核对。以下 CLOSED 只表示对应发现的文档问题已解决。

| 发现 | 修订与定向核对 | 关闭状态 |
|---|---|---|
| B10-C01 / P2 | [慢 rank 步骤 1](../../knowledge/06-training/slow-rank-triage.md)改为 RAS 计数/状态/响应完整性线索；无差异或未展开仍未定，结合各 rank 阶段时间线才分全体/个别。研究记录与 NCCL 登记同步限定推论，默认/verbose 展开条件与归档 RAS 页一致 | CLOSED |
| B10-C02 / P2 | [I/O 步骤 4](../../knowledge/04-data-storage/checkpoint-slow-io-triage.md)去掉“才刷出”与“不是存储”；补周期/老化脏页写回，节流为等待层，同窗口后端吞吐/延迟/错误仍需对照。研究记录与 Linux 登记同步，符合固定 vm.rst L165–242 | CLOSED |
| B11-C01 / P1 | [算子诊断步骤 1–2](../../knowledge/02-software-stack/ascend-op-graph-failure-triage.md)按 PrivateUse1 CPU fallback、AutogradPrivateUse1 与 SparsePrivateUse1 分开；核对固定文件 L232–271 与 CMake 收集，补告警/性能线索，具体算子成功及梯度正确性未保证。研究记录、审计和 TorchNPU/dispatcher 登记已去掉错误的“无 CPU fallback”结论 | CLOSED |
| B11-C02 / P2 | 同篇步骤 4 将图/eager 写为使用者显式配置 `enforce_eager=True` / `--enforce-eager` 的对照，记录授权/窗口/恢复与输入，图路径仅作候选。研究记录区分指南建议与自动重试，核对 graph_mode.md L66–85 | CLOSED |
| B11-C03 / P2 | [弹性训练默认值](../../knowledge/06-training/elastic-training-and-membership.md)分列 torchrun CLI 0 与 WorkerSpec API 3，要求记录实际入口/覆盖值，不把示例当默认。研究记录、审计、elastic 登记与固定 run.py L490–497 / api.py L78–86 一致，登记许可范围说明所列自有代码及生成站点边界 | CLOSED |
| B11-C04 / P2 | [量化支持边界](../../knowledge/07-inference/quantization-and-quality.md)明确同快照 Turing/SM 7.5 与 >7.5 的冲突，kernel/runtime 可用性保留 unknown；Blackwell 限制归属该方法页/快照。研究记录、审计、vLLM 登记一致，未用推断填补硬件支持 | CLOSED |
| B11-C05 / P3 | [vLLM 登记](../../sources/registry.yaml)改为 14 个方法页加 README，共 15 个文件；正文、研究记录与固定目录清单一致。旧替代复查的关闭声明保留为历史，本次实际补齐的遗漏按此项关闭 | CLOSED |
| B12-C01 / P2 | [节点验收步骤 6](../../knowledge/01-hardware/node-acceptance-triage.md)区分调用失败与诊断执行后的检出失败，列 226/NVVS_ERROR 与 205/NVVS_ISOLATE_ERROR，并继续解析 per-test/per-entity、Warning、skipped；研究记录和 DCGM 两形态页登记同步，退出码不单独判根因 | CLOSED |
| B12-C02 / P2 | 同篇前提、步骤 4/6、停止条件与完成判据形成回服门槛：未处置故障、必需检查 skipped 无替代证据、unknown 或收尾未完成维持隔离。按 ascend-dmi 页补 HDK/CANN/算子包、HOST 20–40GB、诊断后重启/压测后分析再重启、单项耗时与三轮诊断建议；研究记录/审计/登记同步，动作仍需授权与窗口 | CLOSED |
| B12-C03 / P2 | [完整性布局](../../knowledge/04-data-storage/checkpoint-integrity-evidence.md)按 single_file_per_rank/thread_count 区分默认单桶、多线程分桶和 False 时逐 item 文件，实际文件集由计划/metadata 确认；研究记录/审计/DCP 登记同步，与 filesystem.py L225–246、L447–463、L507–534 一致 | CLOSED |
| B12-C04 / P2 | [PD 评估](../../knowledge/07-inference/pd-disaggregation.md)保留 v0.14.0 官方不提升吞吐的声明，另标本库建议：固定负载/资源下联合比较时延、吞吐/goodput、失败率与 KV 传输成本。研究记录/登记同步，未声称已有实测收益 | CLOSED |
| B12-C05 / P3 | 同篇 connector 清单删除 Offloading/LMCache 与旧共享存储接口的对应/替代推断；注册名称证据、缓存卸载与跨实例 PD 传输分别理解。研究记录冲突项与登记同步，offloading_connector.py L24–65 只用于说明入口接入 kv_offload，未推断兼容关系 | CLOSED |
| B12-C06 / P3 | [完整性研究标题](batch-12-checkpoint-integrity-sources.md)改为 R2-15，并与 backlog、source-audit 和 `data-storage.checkpoint-integrity-evidence` 对照；R2-12 仍归属量化质量，稳定 content ID 未改变 | CLOSED |

## 对照证据与额外限定

固定源码沿用初审取得的原文件内容与相同 commit，未切换到 master/latest：

- [TorchNPU VariableFallbackKernel.cpp L232–271](https://github.com/Ascend/pytorch/blob/bc51ab84cc6f35c77aab1c59886e0ea43681a317/torch_npu/csrc/aten/VariableFallbackKernel.cpp#L232-L271)与同目录 CMakeLists.txt；[插件 graph_mode.md L66–85](https://github.com/vllm-project/vllm-ascend/blob/52d4acfa51fb868823d1070b81cbd2d97e9e4696/docs/source/user_guide/feature_guide/graph_mode.md#L66-L85)。
- [PyTorch run.py L490–497](https://github.com/pytorch/pytorch/blob/1eba9b3aa3c43f86f4a2c807ac8e12c4a7767340/torch/distributed/run.py#L490-L497)、同 commit 的 elastic/agent/server/api.py 与 [filesystem.py](https://github.com/pytorch/pytorch/blob/1eba9b3aa3c43f86f4a2c807ac8e12c4a7767340/torch/distributed/checkpoint/filesystem.py)。
- [vLLM 固定量化目录](https://github.com/vllm-project/vllm/tree/b17039bccc17b94a2ea107272ad7bc93508708df/docs/features/quantization)的 README/int8.md；同 commit 的 disagg_prefill.md、connector factory 和 offloading_connector.py。
- [Linux 固定 vm.rst L165–242](https://github.com/torvalds/linux/blob/038d61fd642278bab63ee8ef722c50d10ab01e8f/Documentation/admin-guide/sysctl/vm.rst#L165-L242)。

本轮重新取得 [NCCL 2.27.5 RAS](https://docs.nvidia.com/deeplearning/nccl/archives/nccl_2275/user-guide/docs/troubleshooting/ras.html#sample-output)、[DCGM user-guide Exit Codes](https://docs.nvidia.com/datacenter/dcgm/latest/user-guide/dcgm-diagnostics.html#exit-codes)和 [ascend-dmi 6.0.RC2 故障诊断页](https://www.hiascend.com/doc_center/source/zh/mindx-dl/60rc2/toolbox/ascenddmi/toolboxug_0020.html)。0020 页本次完整取得页首表1/2、前提/限制与表4，原研究仅提取参数表的限制已更新；有单项耗时表不等于取得 DCGM 式级别化套件，表4 的 PRBS 状态冲突继续保留。latest DCGM 证据仍只覆盖本次取得内容。

复核同时修正完整性篇与研究建议中的范围表述：关键词扫描未命中不能证明所有 DCP 后端/扩展无校验；形状断言不能验证内容，也不能证明所有同长度损坏均不会被解析发现。相关摘要与 DCP 登记同步限定，未重做全包关键词扫描或 C++ CRC 路径审计。

## 修订后身份与结构检查

本次实际修订 8 篇正文；供电散热篇无初审发现，正文保持不变。8 份研究记录、10 项既有来源的 notes/许可范围、三批来源审计与当前状态入口同步更新；未新增来源 ID 或改变已有 revision。

九篇稳定 ID、标题、路径、类型、领域、平台、source_refs、related_ids 与初审输入一致，均保持 `draft / source_checked`。正文作者/修订者分阶段记录，不把复核通过提升为环境复现。

初审输入 SHA-256 保留在汇总；以下为定向复核通过时的正文身份：

| 批次 | 正文 / 稳定 ID | 修订后 SHA-256 |
|---|---|---|
| 10 | [慢 rank 诊断指南](../../knowledge/06-training/slow-rank-triage.md) / `training.slow-rank-triage`  | `e885553d5a4d084ed28910e383a720035ec1b31c6a00235dd7ee8d5c7a1f30f8` |
| 10 | [供电、散热与性能退化证据](../../knowledge/01-hardware/power-thermal-evidence.md) / `hardware.power-thermal-evidence` （未改） | `27136987c5a74e1a7c54eb79c11130bdf87296d06cf0396afcb26971032ea1ee` |
| 10 | [Checkpoint 慢写与恢复 I/O 诊断指南](../../knowledge/04-data-storage/checkpoint-slow-io-triage.md) / `data-storage.checkpoint-slow-io-triage`  | `e9479e45830dd815356e3d1af8e8f6b3874f74528e225aee3f6b0274db778393` |
| 11 | [昇腾算子不支持与图编译失败诊断指南](../../knowledge/02-software-stack/ascend-op-graph-failure-triage.md) / `software-stack.ascend-op-graph-failure-triage`  | `2e33ec990b819576d189f43a6bf3e28e418b20167986ea39ff508985ce5651b7` |
| 11 | [弹性训练与成员变更](../../knowledge/06-training/elastic-training-and-membership.md) / `training.elastic-training-and-membership`  | `c6dd1d75d445cc6e968a8ed27d79e45eefba50607a428f5b6cb0c8bc6bcca1f1` |
| 11 | [推理量化与输出质量验证](../../knowledge/07-inference/quantization-and-quality.md) / `inference.quantization-and-quality`  | `b64a20dc28e56d13a5cc29d8595ea1563ab192b52070ac4844b0a3afc6a7db6a` |
| 12 | [Prefill/Decode 分离（PD 分离）与流量分配](../../knowledge/07-inference/pd-disaggregation.md) / `inference.pd-disaggregation`  | `806a15650b79837f0e3ae0c11f8f5f08643a9e711b1dc0d592df53e13588c343` |
| 12 | [新节点与返修节点验收](../../knowledge/01-hardware/node-acceptance-triage.md) / `hardware.node-acceptance-triage`  | `209f6ad477d262a2ad5d76f750d777331d2aec057413e2be3bcbc8ac8f9d506c` |
| 12 | [Checkpoint 完整性与校验证据](../../knowledge/04-data-storage/checkpoint-integrity-evidence.md) / `data-storage.checkpoint-integrity-evidence`  | `73b8e425167c2a2b84075d370bb24787bb27095ff30a2ebacccc4afc99b98f8d` |

2026-10-08 修订收尾：`make check` 与 `make build` 均通过，69 content entries / 84 sources，已重建 `build/catalog.md` 和 `build/catalog.json`。逐项核对九篇当前 frontmatter 的全部字段、路径与 SHA-256 均和 catalog 一致，8 篇正文已修订、供电散热篇未改；13 个发现 ID 与优先级/关闭计数在报告、汇总与本复核中一致。84 项来源 ID/URL/revision 保持不变，改动仅涉及所述 notes 与一项许可范围说明。

未修改 `src/kb/`，没有新增或运行开发回归测试。结构/本地链接检查不替代技术对照，不证明任何现场命令已运行。

## 最终状态

B10-C01–C02、B11-C01–C05、B12-C01–C06 均 CLOSED，无剩余本轮开放发现。保留的未知条件（SM 7.5 runtime、NPU 图模式配套、工具覆盖对比、DCP 扩展/C++ 路径等）已在对应正文如实说明；这些缺口没有被写成已验证支持。没有设备诊断、重启、压测、服务部署、存储修复或损坏注入实测。
