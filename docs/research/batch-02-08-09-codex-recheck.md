# batch 02、08、09 修订的 Codex 定向复核

复核日期：2026-09-30。复核者：原代审的本会话 Codex 主助手。依据用户授权和[修订响应](batch-02-08-09-review-fixes.md)，按原报告的关闭条件检查实际文件；没有派发 astra/xhigh 或子代理。

**最终结论：9 项唯一发现全部关闭（5 P2、4 P3），没有待复核项。** batch 02、08、09 在原审阅范围内通过；batch 01 初审无修改项的结论保持。跨批次依赖 B02-C01、B08-C01 已同步关闭。完整覆盖见[四批汇总](batch-01-02-08-09-codex-review-summary.md)。

## 文件身份与复核方法

- 在本次补正前，独立计算修订响应中 7 篇正文的 SHA-256，全部与提交值一致；原始提交摘要保留在修订响应中。
- 重读修订正文、5 份研究记录和关联 registry notes。再次检查初审已取得的固定 commit 源码原文；重新读取 Meta 论文 §7、OCP §3.2.1、NCCL 2.27.5 RAS 和 SuperBench §2.2 的相关段落。
- 逐项验证原先的源码反例或证据边界能否被当前流程正确解释，再检查跨文档一致性。以下正文行号对应本文件末尾的最终 SHA-256。
- 源码反例是静态分析，PDF 核对使用可读文本。本次没有运行 DataLoader 实验、推理服务、通信测试、设备调参或故障注入；没有扩大整篇论文、完整上游工程或平台兼容性验证范围。

## 逐项关闭依据

| ID | 级别 | 实际复核位置与关闭依据 | 最终状态 |
|---|---|---|---|
| B02-C01 | P2 | [数据路径](../../knowledge/04-data-storage/training-data-path.md) L75、82、109 和[数据饥饿流程](../../knowledge/04-data-storage/data-starvation-triage.md) L59、70：区分中间缓冲与可按序交付 batch。后续任务完成但 `_rcvd_idx` 未就绪时仍等待，符合固定 `_next_data` 的 `_task_info` 分支；队列语义未知保留 `unknown`，未把关闭 `in_order` 作为通用修复。 | 已关闭 |
| B08-C01 | P2 | [内存证据](../../knowledge/02-software-stack/ascend-memory-oom-evidence.md) L62–70 和[推理 OOM 流程](../../knowledge/07-inference/ascend-inference-oom-triage.md) L56、68：额度检查可在运行时申请前设置同一错误码，`allowed` 日志与 observer 容量含义已写清；运行分支先核实际额度配置。设备仍有空闲、进程额度已满的反例不再误判为碎片或底层申请失败。 | 已关闭 |
| B08-C02 | P3 | 内存证据 L89：包含 `set_fraction` 与 threshold > 0 的前提、缓存未命中后申请新块前的时机、threshold × `allowed_memory_maximum` 的门槛，并区分其他缓存释放重试路径。研究记录一致。 | 已关闭 |
| B08-C03 | P3 | [空闲设备等待流程](../../knowledge/05-cluster-platform/idle-resource-job-waiting-triage.md) L49、59、62：先核策略、对象时间、控制器接管，再结合队列位置和队首状态；空 conditions 单独只能保留未知，不能反推 StrictFIFO 或直接处置队首。研究记录没有反向推断。 | 已关闭 |
| B09-C01 | P2 | 推理 OOM 流程 L64：运行期 fatal 经 `ENGINE_CORE_DEAD` 传播异常，启动/运行阶段由就绪记录、最后成功请求与原始日志判断；运行一段时间后死亡进入运行分支，缺证据保留 `unknown`，异常不单独证明 OOM。来源记录删除了“构造失败也必然抛同一异常”的无依据扩大。 | 已关闭 |
| B09-C02 | P2 | [静默错误判定](../../knowledge/08-reliability/silent-errors-and-integrity.md) summary、L48–56、检测方法表和 L94：区分被动报告缺口、主动参考结果校验可检出、一次 PASS 不能排除全部；与 Meta §7 和方法表一致，没有保证某个具体诊断套件必然覆盖。 | 已关闭 |
| B09-C03 | P2 | 静默错误判定 L82：已知数值语义扣除后的完整性异常可进入候选，重放/迁移/复现/设备关联是证据增强方式，偶发且未定位设备的情形不会被排除；浮点容差与精确契约分开，软件/数据/算法解释保留，未直接归因硬件。符合 OCP 间歇触发的机制边界。 | 已关闭 |
| B09-C04 | P3 | [带宽退化流程](../../knowledge/03-communication/bandwidth-degradation-triage.md) L68 和 RAS 研究记录：包含活跃通信和初始化/销毁的正常瞬态，同一 communicator、同一阶段的连续查询与负载正常基线；持续停滞只支持调查，不直接证明链路退化。 | 已关闭 |
| B09-C05 | P3 | 静默错误判定 L44 和 SuperBench 研究记录：分母为部分 ToR 的冗余链路，测试床有 25% 冗余上行，多组双节点对同时通信；不再指全部上行的一半，不作为通用触发阈值。与 §2.2 文字一致。 | 已关闭 |

## 关键来源定位

- B02-C01：PyTorch commit `1eba9b3aa3c43f86f4a2c807ac8e12c4a7767340`，[函数入口 L1424](https://github.com/pytorch/pytorch/blob/1eba9b3aa3c43f86f4a2c807ac8e12c4a7767340/torch/utils/data/dataloader.py#L1424)、[按序/乱序分支 L1449–1480](https://github.com/pytorch/pytorch/blob/1eba9b3aa3c43f86f4a2c807ac8e12c4a7767340/torch/utils/data/dataloader.py#L1449-L1480)。
- B08-C01/C02：TorchNPU commit `bc51ab84cc6f35c77aab1c59886e0ea43681a317`，[额度拒绝 L2692–2694](https://github.com/Ascend/pytorch/blob/bc51ab84cc6f35c77aab1c59886e0ea43681a317/torch_npu/csrc/core/npu/NPUCachingAllocator.cpp#L2692-L2694)、[额度设置 L1717–1724](https://github.com/Ascend/pytorch/blob/bc51ab84cc6f35c77aab1c59886e0ea43681a317/torch_npu/csrc/core/npu/NPUCachingAllocator.cpp#L1717-L1724)、[observer L1391–1409](https://github.com/Ascend/pytorch/blob/bc51ab84cc6f35c77aab1c59886e0ea43681a317/torch_npu/csrc/core/npu/NPUCachingAllocator.cpp#L1391-L1409)、[GC 前提 L1353–1369](https://github.com/Ascend/pytorch/blob/bc51ab84cc6f35c77aab1c59886e0ea43681a317/torch_npu/csrc/core/npu/NPUCachingAllocator.cpp#L1353-L1369)、[GC 门槛 L2624–2629](https://github.com/Ascend/pytorch/blob/bc51ab84cc6f35c77aab1c59886e0ea43681a317/torch_npu/csrc/core/npu/NPUCachingAllocator.cpp#L2624-L2629)。
- B08-C03：Kueue commit `911a822a49bcfd99c9c62203a009efa4130ad604`，[Unattempted Workload L243–248](https://github.com/kubernetes-sigs/kueue/blob/911a822a49bcfd99c9c62203a009efa4130ad604/site/content/en/docs/tasks/troubleshooting/troubleshooting_jobs.md#L243-L248) 只给出条件性的“可能”。
- B09-C01：vLLM commit `b17039bccc17b94a2ea107272ad7bc93508708df`，[构造与 fatal 分支 L927–943](https://github.com/vllm-project/vllm/blob/b17039bccc17b94a2ea107272ad7bc93508708df/vllm/v1/engine/core.py#L927-L943)、[客户端接收死亡标记 L425–428](https://github.com/vllm-project/vllm/blob/b17039bccc17b94a2ea107272ad7bc93508708df/vllm/v1/engine/core_client.py#L425-L428)。这些行不足以推断构造失败时客户端一定抛同一异常。
- B09-C02/C03：[Meta v1 §7 Detection Mechanisms](https://arxiv.org/html/2102.11245v1#S7) 与 [OCP §3.2.1，印刷 p.9](https://www.opencompute.org/documents/sdc-in-ai-ocp-whitepaper-final-pdf#page=9)。
- B09-C04：[NCCL 2.27.5 RAS Sample Output](https://docs.nvidia.com/deeplearning/nccl/archives/nccl_2275/user-guide/docs/troubleshooting/ras.html#sample-output)。
- B09-C05：[SuperBench §2.2，印刷 p.838 / 文件第 5 页](https://www.usenix.org/system/files/atc24-xiong.pdf#page=5)。

## 复核时一并完成的补正

这些补正属于原发现的关闭范围，完成后重新核对，未留下新的待办项：

1. B02-C01：正文和 registry 的函数名从 `_process_next_result` 改为固定源码实际的 `_next_data`。
2. B08-C03：显式补上队列位置和队首状态，与原关闭条件、流程步骤 5 对齐。
3. B09-C01：正文使用“客户端收到该标记会抛”，来源记录与修订响应不再宣称两种失败路径必然抛同一异常。
4. B09-C04：正文和研究记录补同一 communicator、相同阶段与正常基线，正文添加具体 RAS 页面链接。
5. B09-C05：正文和研究记录补多组双节点对并发条件，研究记录也恢复正确分母与范围。

## 最终正文身份（SHA-256）

修订响应的旧摘要保留为复核前提交身份；以下为本次补正并重新检查后的最终身份。另 5 篇正文的摘要与初审汇总一致。

| 正文 | SHA-256 |
|---|---|
| [training-data-path](../../knowledge/04-data-storage/training-data-path.md) | `302e4ae06636a15a8857db7f8952074fbd51bcea3a5baaa7a55265afedf54a37` |
| [ascend-memory-oom-evidence](../../knowledge/02-software-stack/ascend-memory-oom-evidence.md) | `3494d91dbda5eb8dfabe451cd26875e8592339dc8bdafde7669ea9d8655e00e7` |
| [data-starvation-triage](../../knowledge/04-data-storage/data-starvation-triage.md) | `4a165fe1643f0b89d1709b1a35d8a4d493c581ccc23b480b9b032f3aac71a990` |
| [idle-resource-job-waiting-triage](../../knowledge/05-cluster-platform/idle-resource-job-waiting-triage.md) | `6eb2770ba3251a23ef7f6c0403dfbcfa16ac264e875b0076007b860b9c4090d3` |
| [ascend-inference-oom-triage](../../knowledge/07-inference/ascend-inference-oom-triage.md) | `37b4d31df84c1631a146b183ec998f6d8525ffde9caa22644450b447d79e497d` |
| [bandwidth-degradation-triage](../../knowledge/03-communication/bandwidth-degradation-triage.md) | `06098c0d06db09ec4813eeaa5de49198906f75624a8d8845c084bb08a83f8630` |
| [silent-errors-and-integrity](../../knowledge/08-reliability/silent-errors-and-integrity.md) | `d65abb5fd8e862e8edf07012580e8f6af6283eb5b5faecb574b12f79db22b964` |

## 本地检查与状态边界

`make check` 与 `make build` 均通过：**60 content entries / 71 sources**。12 篇正文的最终 SHA-256 和全部元数据与生成 catalog 一致；汇总、修订响应和本复核记录的 9 个发现 ID 与关闭状态一致，7 篇最终摘要已登记。没有改动 `src/kb/`，不需要新增测试或运行 `make test`。

全部正文仍为 `draft / source_checked`，没有新增 `reviewed` 或 `reproduced`，没有环境实验。关闭的是这 9 项文档缺陷；实际硬件支持、运行结果及原文明确的来源缺口仍按各正文记录。结构检查与构建不证明技术正确性或远程链接有效。
