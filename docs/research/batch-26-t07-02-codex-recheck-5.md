# Batch 26 T07-02 第五轮定向复核（微型范围）

## 复核头部

- 角色与范围：知识库批次审阅者；仅核对[第四轮复核](batch-26-t07-02-codex-recheck-4.md)留下的 C01／C04 两处记录修订及其是否引入新问题。C02／C03／C05／C06／C07／R01／R02／R03／R04 沿用 CLOSED，不重新展开审阅。
- 模型／推理档位：`gpt-6.1-sol / xhigh`。已读取当前本地 Codex CLI 会话 `01a15855-11b3-7f60-866d-a2878be458f8` 的执行元数据：`originator: codex_exec`、`source: exec`、CLI `0.163.0`；本轮 `turn_context` 仅有上述单一模型与档位，审阅输出未见模型回退标记，未调用其他模型或子代理。
- 日期：2026-10-20（Asia/Shanghai）。
- 本地对象：[正文](../../knowledge/07-inference/engine-backend-boundaries.md) L118、[作者来源记录](batch-26-t07-02-sources.md) L37／L44；仅为核对一致性读取正文 L68、来源记录 L51／L53、[registry](../../sources/registry.yaml) L6691／L6719，以及[加载页身份表](../../knowledge/07-inference/model-loading-and-readiness.md) L117–127。行号以本轮读取位置为准。
- 上游取证：GitHub 网页与 raw 读取均返回 Cache miss 后，通过 GitHub 文件 API 按固定 ref 独立重取指定原文件行段：vLLM `b17039bccc17b94a2ea107272ad7bc93508708df` 的 `scheduler.py` L351–401／L800–819；MindIE-LLM `69e5a5dd4b533eaffc7e198320435350825a36f7` 的 `fcfs_policy.cpp` L468–510 及仓内模型表 L36–39。保留原文件坐标，未以作者缓存代替取回。
- 执行边界：仅新增本报告；未修改正文、来源、索引、计划或原工作区构建产物；未运行推理引擎或进行硬件验证。
- 结构与变更范围核对：在包含本报告及既有 `build/` 链接目标的临时工作区副本执行 `make check`、`make build`，均通过（109 content entries／537 sources）；仅验证结构和本地引用。摘要比对确认本轮记录的 551 个非忽略既有文件及原工作区两份 `build/` 文件未变，仅新增本报告。

## C01（P2）— CLOSED

正文 Ascend 表 L118 的 MindIE 单元格现已明确：**样板权重与 tokenizer 的 revision 均未固定，状态为 unknown，待现场按加载页身份表固定**。两项身份均有当前状态，补齐第四轮唯一剩余字段；所链身份表要求不可变 revision／内容摘要，与此待固定状态一致。

新增“HF／ModelScope 链接列只给仓库入口，不构成已固定身份”的限定也成立：[固定仓内模型表 L36–39](https://github.com/Ascend/MindIE-LLM/blob/69e5a5dd4b533eaffc7e198320435350825a36f7/docs/zh/user_guide/model_support_list.md#L36-L39)的 Qwen2-7B-Instruct 行仅给模型仓库 URL，没有固定权重或 tokenizer revision。本次只据此核对入口性质，不建立该固定仓内表与 latest 站点的同版关系。

**满足第四轮剩余关闭条件，C01 关闭。** 其余 C01 条件沿用第四轮已满足结论；不要求取得实际 revision 或补做实验。

## C04（P2）— CLOSED

- **来源表 L37 已同步 vLLM 局部抢占链。** 主张列新增分配失败后的抢占选择、释放 KV／encoder cache、PREEMPTED、清零计算进度及放回 waiting；精确位置加入 [scheduler.py L351–401](https://github.com/vllm-project/vllm/blob/b17039bccc17b94a2ea107272ad7bc93508708df/vllm/v1/core/sched/scheduler.py#L351-L401) 与 [_preempt_request L800–819](https://github.com/vllm-project/vllm/blob/b17039bccc17b94a2ea107272ad7bc93508708df/vllm/v1/core/sched/scheduler.py#L800-L819)，并注明“复核轮三补核”。原文件支持这些有限主张；未覆盖范围已收窄为完整调度算法中的 token 预算实现细节、完整触发路径及 async 模式语义，不再把已核局部抢占链整体排除。
- **来源表 L44 已同步 MindIE 模式选择／RECOMPUTE 片段。** 主张与精确位置均加入 [fcfs_policy.cpp L468–510](https://github.com/Ascend/MindIE-LLM/blob/69e5a5dd4b533eaffc7e198320435350825a36f7/src/scheduler/policy/fcfs_policy.cpp#L468-L510)，注明“复核轮三补核”；原文件包含 SWAP／RECOMPUTE 选择，以及 RECOMPUTE 下置 WAITING、FreeSeq、状态重置。该片段无队列插入操作；来源表明确保留完整触发条件、再入队链与完整算法未核，没有推成 MindIE 不存在再入队。

两条主张行现与正文 L68、unknown 清单 L51／L53 及 registry 已接受的有限证据边界一致。**满足第四轮剩余来源表同步条件，C04 关闭。** 无须补核完整调度器或再入队实现。

## 新发现

**无。** 两处记录修订未引入新的身份已固定暗示、调度机制误述或取证范围冲突；其余已 CLOSED 项保持原结论。

## 整体结论

**通过第五轮定向复核：C01、C04 均为 CLOSED。** C02／C03／C05／C06／C07／R01／R02／R03／R04 沿用 CLOSED，T07-02 在既定审阅范围内闭环，无剩余开放发现。

正文继续保持 `draft / source_checked`；MindIE latest 与固定源码／产品包的同版关系、实际部署组合及硬件功能交集均未因此获得验证。
