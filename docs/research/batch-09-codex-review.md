# 第九批审阅记录（用户授权由 Codex 替代 astra）

审阅日期：2026-09-30。审阅者：本会话 Codex 主助手；用户明确授权本助手替代 astra 补审。没有派发 gpt-6-astra/xhigh 或子代理。此报告与原[同环境子代理替代复查](batch-09-substitute-review.md)分别记录。

**最新结论：修订后定向复核通过，发现全部关闭。** 本批 B09-C01 至 B09-C05 及关联的 B08-C01 均已关闭。 关闭依据与最终文件身份见[定向复核记录](batch-02-08-09-codex-recheck.md)。

## 初审记录（历史）

以下结论、发现位置和开放状态保留为初审快照；最终状态以文末定向复核为准。

**结论：审阅完成，暂不通过。** 本批新增 3 项 P2、2 项 P3，另受 batch 08 的 1 项 P2 影响。全部开放；去重统计、正文版本与检查结果见[四批汇总](batch-01-02-08-09-codex-review-summary.md)。

## 审阅范围与实际证据

| 正文 | 本次重新核对的来源 |
|---|---|
| [昇腾推理 OOM 诊断指南](../../knowledge/07-inference/ascend-inference-oom-triage.md) | vLLM commit `b17039bccc17b94a2ea107272ad7bc93508708df` 的 EngineCore 与 client 错误传播；vLLM Ascend commit `52d4acfa51fb868823d1070b81cbd2d97e9e4696` 的 NPU worker 内存预算；关联 TorchNPU 分配器；Issue #15920、#12692 的正文与实际返回评论 |
| [通信带宽退化诊断指南](../../knowledge/03-communication/bandwidth-degradation-triage.md) | nccl-tests commit `b4d5beebca8a76cf01335f724d154b9b9d394d96` 的 common.cu、util.cu；NCCL 2.27.5 RAS；浏览器渲染的 CANN 9.1.X HCCL Test 参数/结果/规格正文 |
| [静默错误与计算完整性判定](../../knowledge/08-reliability/silent-errors-and-integrity.md) | arXiv:2102.11245v1 的 HTML §5–§8；OCP 白皮书文本提取中 §3.2.1 等相关段落；SuperBench §2.2 的数字与分母；PyTorch 2.6 numerical_accuracy/testing 文档；关联健康证据正文 |

同时读取本批来源审计、三份来源记录、原替代复查、元数据、来源登记和导航。PDF 核查使用文本提取，未完成图表像素或整篇论文的独立复核；只用可读文字确认下列发现。没有构建通信工具、启动服务、施加负载或注入故障。

## B09-C01 · P2 · EngineDeadError 不能用于确定启动阶段

状态：**开放**。位置：[ascend-inference-oom-triage.md](../../knowledge/07-inference/ascend-inference-oom-triage.md) 第 64 行；[推理 OOM 来源记录](batch-09-inference-oom-sources.md)的同类解释也需同步。

步骤 1 把客户端 `EngineDeadError` 解释为 EngineCore 进程内启动失败，再选择启动或运行分支。固定 [`core.py` L927–943](https://github.com/vllm-project/vllm/blob/b17039bccc17b94a2ea107272ad7bc93508708df/vllm/v1/engine/core.py#L927-L943) 在构造 EngineCore 后进入 `run_busy_loop()`；捕获异常时，`engine_core is None` 才打印 failed to start，已有对象则打印 fatal error 并发出 ENGINE_CORE_DEAD。客户端 [`core_client.py` L425–428](https://github.com/vllm-project/vllm/blob/b17039bccc17b94a2ea107272ad7bc93508708df/vllm/v1/engine/core_client.py#L425-L428) 收到该标记会抛 `EngineDeadError`。因此运行期间死亡同样可出现该异常，它也没有单独证明根因是 OOM。

**建议及关闭条件：** 将它解释为引擎不可恢复退出的传播信号；阶段依据启动完成、最后成功请求、EngineCore 原始日志/栈和时间线判断，依据更早的分配或容量错误确认 OOM。修订后“服务已运行一段时间再死亡”的情形必须能进入运行分支；无法确定阶段时保留 `unknown`。

## B09-C02 · P2 · 把主动校验整体排除在 SDC 检测之外

状态：**开放**。位置：[silent-errors-and-integrity.md](../../knowledge/08-reliability/silent-errors-and-integrity.md) 第 48、88 行，标题、摘要和同段解释应同步。

正文断言摘要、计数器与主动测试都覆盖不到无报错误算，并以 SDC 的“静默”定义推出健康证据不覆盖。被动日志缺少告警不等于主动结果校验也无法检出。原论文 [§7 Detection Mechanisms](https://arxiv.org/html/2102.11245v1#S7) 明确用特定计算和已知参考值比较来发现 SDC；这也与正文自己的 reproducer/fleet/canary 方法表相冲突。

**建议及关闭条件：** 分开“被动事件未检出”“特定主动测试未触发”与“结果校验检出不一致”。主动测试的覆盖取决于输入、执行路径和触发条件；一次 PASS 不能排除全部 SDC。不能保证当前某个 DCGM/MindX 测试一定检出，但也不能按定义宣布主动测试一概无效。健康证据关联段、常见误解、摘要与检测表需一致。

## B09-C03 · P2 · 把稳定复现与硬件绑定误设为 SDC 嫌疑的入口条件

状态：**开放**。位置：[silent-errors-and-integrity.md](../../knowledge/08-reliability/silent-errors-and-integrity.md) 第 76 行。

“可复现、随输入数据相关、绑定特定硬件时，才进入 SDC 嫌疑”把定位之后得到的证据提前设为入口门槛。来源并未把一个 CPU 案例的特征定义为所有 SDC 的必要条件。[OCP §3.2.1，印刷 p.9](https://www.opencompute.org/documents/sdc-in-ai-ocp-whitepaper-final-pdf#page=9)说明故障可能只在特定运行条件下间歇触发；早期尚无稳定复现或硬件定位，不能据此排除怀疑。

**建议及关闭条件：** 区分完整性异常、SDC 候选与已定位硬件原因。排除已知数值语义后，异常可进入候选调查；复现、重放、迁移、冗余和设备关联用于增强或削弱假设，不能要求先满足全部条件。浮点判据使用任务约定的容差；精确整数、不变量或校验和按各自契约比较。修订后要允许“偶发异常、设备尚未定位”的候选状态，同时保留软件/数据/算法等替代解释，不能将超容差自动判成硬件故障。

## B09-C04 · P3 · RAS MISMATCH 缺少正常瞬态和重复查询限定

状态：**开放**。位置：[bandwidth-degradation-triage.md](../../knowledge/03-communication/bandwidth-degradation-triage.md) 第 68 行；[带宽来源记录](batch-09-bandwidth-sources.md)的 RAS 行。

正文称 MISMATCH 可识别慢 rank/进度分叉，却略去官方解释中的正常情形。[NCCL 2.27.5 RAS：Sample Output](https://docs.nvidia.com/deeplearning/nccl/archives/nccl_2275/user-guide/docs/troubleshooting/ras.html)指出活跃通信期间的计数差异可能正常；多次查询仍推进时不必担忧，持续不变才值得调查。初始化/销毁过渡也可能暂时出现 MISMATCH。

**建议及关闭条件：** 补上同一 communicator、相同阶段的连续查询与正常基线；把单次 MISMATCH 作为快照线索。持续停滞也不直接证明链路退化。正文与研究记录同步保留该限定。

## B09-C05 · P3 · SuperBench 链路比例的分母被扩张

状态：**开放**。位置：[silent-errors-and-integrity.md](../../knowledge/08-reliability/silent-errors-and-integrity.md) 第 44 行。

“ToR 上行链路半数失效才显著掉带宽”遗漏了冗余子集限定。[SuperBench §2.2，印刷 p.838](https://www.usenix.org/system/files/atc24-xiong.pdf#page=5) 描述的是特定测试床、ToR 有 25% 冗余上行、部分交换机超过一半的**冗余链路**失效时发生回归，并非全部上行链路的一半，也不是通用触发阈值。

**建议及关闭条件：** 恢复“部分 ToR 的冗余链路”分母、特定并发测试条件，并删除泛化的“才”字；数值示例只用于说明掩盖，不转化为链路运维阈值。

## 跨批次影响与已排除的疑点

- [B08-C01](batch-08-codex-review.md)：推理流程依赖的 TorchNPU OOM 机制遗漏进程额度来源；修订分配器条目时也要同步推理流程的检查分支。按同一个发现 ID 去重。
- 插件 KV 预算中的框架峰值与非框架增量在固定 NPU worker 实现中有依据；不能将 GPU 的额外预算常量直接套给 NPU。
- nccl-tests 固定源码支持主要 host 计时循环、校验循环分离及失败页脚；未把带宽数字推成链路故障。HCCL Test `NULL` 不能表示正确性通过，与当前渲染结果说明一致；具体内部计时归约仍未知。
- 再读 [#15920 报告者更正](https://github.com/vllm-project/vllm-ascend/issues/15920#issuecomment-5677674442)确认原 V1/强制 chunked prefill 归因被撤回；[#12692](https://github.com/vllm-project/vllm-ascend/issues/12692)仍只有报告者的碎片推断，本次返回 1 条评论而元数据为 2。正文保留了两者的未闭环边界，未认定修复。
- 旧替代复查关闭的 2 项 P2、7 项 P3 是历史结果，不覆盖本次新增发现。OCP 早期来源表仍有三类结局的历史写法，与已改成四类的正文不一致；后续修订应同步事实记录，不能把旧表当作最终分类证据。

## 初审结束状态（历史）

新增 3 项 P2、2 项 P3 均开放，关联 B08-C01 也开放。未修改正文，未关闭发现，未增加技术复现状态。所有修订均需按各项关闭条件定向复核；结构检查和构建只验证结构与本地引用。

## 定向复核最终状态（2026-09-30）

本批 B09-C01 至 B09-C05 及关联的 B08-C01 均已关闭。 原关闭条件经实际正文和固定来源核对均已满足；少量表述补正与复核后 SHA-256 见[定向复核记录](batch-02-08-09-codex-recheck.md)。本批在原审阅范围内通过，没有待复核项；正文仍为 `draft / source_checked`，未做环境执行。
