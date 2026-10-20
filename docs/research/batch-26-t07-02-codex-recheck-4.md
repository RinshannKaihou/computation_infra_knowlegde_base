# Batch 26 T07-02 第四轮定向复核

## 复核头部

- 角色：知识库批次审阅者；仅核对[第三轮复核](batch-26-t07-02-codex-recheck-3.md)留下的 **C01、C04** 关闭条件及第四轮修订引入的问题。C02／C03／C05／C06／C07／R01／R02／R03／R04 沿用 CLOSED，不重新展开审阅。
- 模型／推理档位：`gpt-6.1-sol / xhigh`。已读取当前本地 Codex CLI 会话 `01a1583c-f7a7-70a2-87c0-addae0454d31` 的执行元数据：`originator: codex_exec`、`source: exec`、CLI `0.163.0`，`turn_context` 为上述单一模型与档位；有效审阅未采用其他模型、子代理或模型回退结果。
- 日期：2026-10-20（Asia/Shanghai）。
- 本地对象：[正文](../../knowledge/07-inference/engine-backend-boundaries.md) L68、L86、L88、L103、L109、L118 及必要邻接语境；[作者来源记录](batch-26-t07-02-sources.md) L37／L44／L51／L53；[registry](../../sources/registry.yaml) L6691／L6719。行号以本轮读取位置为准；作者所述改动逐项以实际文件核验。
- 上游取证：GitHub 网页／raw 读取失败后，通过 GitHub 文件 API 独立重取固定 ref 原文件，保留空行核对原文件坐标。vLLM `b17039bccc17b94a2ea107272ad7bc93508708df`：connector `factory.py`、`nixl_connector_usage.md`、`disagg_prefill.md`、`scheduler.py`；vllm-ascend `52d4acfa51fb868823d1070b81cbd2d97e9e4696`：根 `README.md`、`DeepSeek-R1.md`、`DeepSeek-V3.1.md`；MindIE-LLM `69e5a5dd4b533eaffc7e198320435350825a36f7`：`fcfs_policy.cpp`、仓内模型支持表。未以作者缓存代替独立取回，也未将固定仓内表与 latest 站点建立同版关系。
- 执行边界：仅新增本报告；未修改正文、来源、索引、计划或原工作区构建产物，未安装、构建或运行推理引擎，未进行硬件验证。
- 结构校验：在包含本报告与既有 `build/` 链接目标的临时工作区副本执行 `make check`、`make build`，均通过（109 content entries／537 sources）。检查仅验证结构与本地引用，不证明技术正确性或远程内容。摘要核对确认本轮开始时的 550 个非忽略既有文件及原工作区两份 `build/` 文件未变，仅新增本报告。

## C01（P2）— 未关闭：主要修订成立，MindIE tokenizer 身份状态仍缺项

**本轮已满足的条件：**

- NVIDIA L88 已明确驱动版本 unknown，并承接该档案已有的权重／tokenizer 待现场固定、wheel 变体未选状态。AMD L103 已分别记录权重／tokenizer 待固定、驱动与容器／制品身份 unknown。两处不再缺少第三轮指出的身份维度，不要求选出实际部署组合。
- Ascend L118 两线均明确 HDK／驱动版本 unknown，并记录未选镜像／制品；vllm-ascend 侧另明确 DeepSeek 权重／tokenizer 待现场固定。[固定 README L55](https://github.com/vllm-project/vllm-ascend/blob/52d4acfa51fb868823d1070b81cbd2d97e9e4696/README.md#L55)确实单列 HDK 参考入口，正文没有再把 CANN 8.5.0 当成 HDK 身份已知。MindIE 侧“HF／ModelScope 链接列未固定 revision”已明确权重版本尚未固定，不能视为不可变权重身份已知。
- DeepSeek L109 的样板归属已落定：[R1 教程 L6–18](https://github.com/vllm-project/vllm-ascend/blob/52d4acfa51fb868823d1070b81cbd2d97e9e4696/docs/source/tutorials/DeepSeek-R1.md#L6-L18)以 R1-W8A8 为例并列出 A2／A3 节点条件；[V3.1 教程 L25–30](https://github.com/vllm-project/vllm-ascend/blob/52d4acfa51fb868823d1070b81cbd2d97e9e4696/docs/source/tutorials/DeepSeek-V3.1.md#L25-L30)列出 BF16 与量化变体。正文将这些限定为文档条件，所选样板的图／EP／PD 组合明确 unknown，下方全局行不替代样板级结论，满足第三轮该项要求。
- NVIDIA PD 行 L86 的三处证据已各归其位：[factory.py L146–204](https://github.com/vllm-project/vllm/blob/b17039bccc17b94a2ea107272ad7bc93508708df/vllm/distributed/kv_transfer/kv_connector/factory.py#L146-L204)是实际 connector 注册段；[NIXL 指南 L5–28](https://github.com/vllm-project/vllm/blob/b17039bccc17b94a2ea107272ad7bc93508708df/docs/features/nixl_connector_usage.md#L5-L28)包含安装依赖、所需版本的定位入口与通信依赖；[disagg_prefill.md L1–16](https://github.com/vllm-project/vllm/blob/b17039bccc17b94a2ea107272ad7bc93508708df/docs/features/disagg_prefill.md#L1-L16)支持 experimental 与不提升吞吐的文档声明。未把该声明当成本库实测结论。

**唯一剩余缺项：正文 L118 的 MindIE 单元格仍只记录“样板权重身份”，未说明 tokenizer 的身份／revision 当前是已知、待现场固定还是 unknown。** [固定仓内 Qwen2-7B-Instruct 行 L36–39](https://github.com/Ascend/MindIE-LLM/blob/69e5a5dd4b533eaffc7e198320435350825a36f7/docs/zh/user_guide/model_support_list.md#L36-L39)给出模型仓库入口，不能代填本档案的 tokenizer 选择与固定状态。该缺项已经包含在第三轮“Ascend 两线各自权重／tokenizer revision”的关闭条件内，不是新增验收要求。正文 L124 的未来重建清单也仍不能替代当前档案状态。

**剩余关闭条件：** 在 MindIE 依赖身份单元格明确权重与 tokenizer 的 revision 均未固定／unknown、待现场按身份表固定，或分别给出已有证据支持的状态即可。不要求下载权重、取得实际 revision、验证 tokenizer 或补做硬件实验。其余本轮 C01 修订不再阻碍关闭；**保留 C01／P2，仅剩上述字段记录。**

## C04（P2）— 未关闭：正文、unknown 与 registry 已同步，来源表两条主张行仍未完成

**正文边界修订满足条件。** L68 已区分已核局部条件与未全面核对的完整触发路径，并将差异限定为取证覆盖深度，没有再据此判断两引擎实际链条完整性：

- [vLLM Scheduler L351–401](https://github.com/vllm-project/vllm/blob/b17039bccc17b94a2ea107272ad7bc93508708df/vllm/v1/core/sched/scheduler.py#L351-L401)中，`allocate_slots` 返回 None 后，PRIORITY 分支按 `(priority, arrival_time)` 选取，另一分支取 running 尾部；[_preempt_request L800–819](https://github.com/vllm-project/vllm/blob/b17039bccc17b94a2ea107272ad7bc93508708df/vllm/v1/core/sched/scheduler.py#L800-L819)释放 KV／encoder cache、置 PREEMPTED、清零计算进度并放回 waiting。正文的有限描述与源码相符。
- [MindIE FcfsPolicy L468–510](https://github.com/Ascend/MindIE-LLM/blob/69e5a5dd4b533eaffc7e198320435350825a36f7/src/scheduler/policy/fcfs_policy.cpp#L468-L510)包含 SWAP／RECOMPUTE 模式选择，以及 RECOMPUTE 下的 WAITING、FreeSeq、状态重置；该片段确无队列插入操作。正文保留完整再入队链未核，没有推成引擎不存在再入队。
- 来源记录 unknown #1／#3（L51／L53）已列出上述有限已核路径；registry L6691／L6719 也已加入相应片段并保留未核完整路径的边界。这些修订可接受。

**仍未满足的是第三轮明确要求的主张—来源定位表同步。** 本轮实际文件与作者所述“两行已同步”不一致：

| 位置 | 实际残留 | 尚需完成的同步 |
|---|---|---|
| 来源表 L37，vLLM 调度组件行 | 精确位置未列 L351–401／L800–819；支持范围仍写“完整调度算法（token 预算实现、抢占路径）不在本切面” | 将已核局部抢占选择与释放／置位／放回 waiting 的位置纳入该行，并把未覆盖范围限定为其外的完整算法／触发路径等 |
| 来源表 L44，MindIE 调度策略族行 | 精确位置仍仅列 `fcfs_policy.cpp L37–111` 等原范围，未加入 L468–510；主张与支持范围未登记新增模式选择／RECOMPUTE 片段及其边界 | 加入 L468–510，说明已核模式选择、WAITING／FreeSeq／状态重置；该片段无队列插入，完整触发与再入队链未核 |

unknown 清单与 registry 已更新，不能代替这两条主张行自身的精确位置和已核／未核范围；也不需要为同步重复补核整个调度器。**保留 C04／P2，仅剩来源表 L37／L44 的同步。** 不要求补齐 MindIE 完整再入队实现或开展运行测试。

## 新发现

**无独立新发现。** MindIE tokenizer 状态遗漏属于原 C01 剩余身份字段；来源表两行未同步属于原 C04 剩余取证记录条件，均不另立编号或重复累计。其余本轮修订未发现新的机制误述；已 CLOSED 项保持原结论。

## 整体结论

**未通过第四轮定向复核。C01、C04 仍未关闭，保留原 P2。** C02／C03／C05／C06／C07／R01／R02／R03／R04 沿用 CLOSED。

剩余工作仅为：补明 MindIE 样板 tokenizer 的当前未知／待固定状态；同步来源表 vLLM 与 MindIE 两条主张行的已核片段、精确位置及未核范围。完成这两处记录修订后再作定向复核，无须扩审其他平台特性或补做硬件实验。

正文继续保持 `draft / source_checked`。本报告不建立 MindIE latest 与固定源码／产品包的同版关系，也不证明任何 NVIDIA／AMD／Ascend 部署组合或功能交集已获硬件验证。
