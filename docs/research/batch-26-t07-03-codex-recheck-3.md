# Batch 26 T07-03 第三轮定向复核

## 复核头部

- 角色与范围：知识库批次审阅者；仅核对[第二轮定向复核](batch-26-t07-03-codex-recheck-2.md)中 C03、C07 的来源表同步残留、R02 的正文出处修订，以及这三处修订是否引入新问题。C01、C02、C04、C05、C06、C08、R01 沿用 **CLOSED**，不重做整篇初审。
- 日期：2026-10-21（Asia/Shanghai）。
- 实际模型／推理档位：`gpt-6.1-sol / xhigh`。已读取当前本地 Codex CLI 会话 `01a15a8c-b2d1-7fe1-a008-6a94ad38df68` 的执行元数据：`originator: codex_exec`、`source: exec`、CLI `0.163.0`；已检查的全部 `turn_context` 只有该模型与档位，已输出的 assistant 文本未见回退标记。当前会话直接执行，未另启模型或子代理。
- 已读约定：根 `AGENTS.md`、`README.md`、[写作指南](../authoring-guide.md)、`content-outline.md`；参照 T07-03 acceptance，不增加现场验证要求。
- 仓内核对位置：[来源记录](batch-26-t07-03-sources.md) L29／L31、[正文](../../knowledge/07-inference/mindie-execution-profile.md) L129；仅对照正文 L72／L101、registry 的相关摘要确认同步一致。仓内行号为本轮工作区的 1-based 行号。
- 上游取证：通过 GitHub 文件连接器重新取得 `Ascend/MindIE-LLM@69e5a5dd4b533eaffc7e198320435350825a36f7` 的配置页、混部部署页、Qwen README、模型支持列表四个原文件，保留空行核对下述行锚点；SHA-256 前 16 位依次为 `59f1dd120399191f`、`75bd1da15eb171f2`、`09941aede58df7cc`、`cebe1df8005841c3`，均与来源记录一致。另重开 latest 支持列表，仅核 Qwen 表头及相关模型行，不建立整站与快照映射。
- 执行边界：未安装或运行引擎、启动服务、发送模型请求或执行硬件测试；仓内只新增本报告。

## C03（P2）— CLOSED：来源表已补齐 D 侧身份卡数约束

- 来源记录 L29 的 worldSize 摘要现已补入“PD 分离 D 侧须与下发身份设置的卡数一致（ModelConfig 表 L128）”，直接满足第二轮剩余关闭条件；单机 NPU 数与多机 ranktable 分支仍保留。
- 固定[配置表 worldSize 行 L128](https://github.com/Ascend/MindIE-LLM/blob/69e5a5dd4b533eaffc7e198320435350825a36f7/docs/zh/user_guide/user_manual/service_parameter_configuration.md#L128)明确区分多机由 ranktable 计算与 D 分离场景的身份卡数约束。新增摘要与该行、正文 L72 及 registry 对应表述一致；没有扩写为 PD 分离部署已取证或可运行。

## C07（P2）— CLOSED：来源表两个入口的工作目录条件已同步

- 来源记录 L31 现明确 run 包工作目录为 `{MindIE安装目录}/latest/mindie-service`，相对路径后台命令绑定在该目录执行，并保留“不能在 bin 目录启动”；与固定[混部页 L255–270](https://github.com/Ascend/MindIE-LLM/blob/69e5a5dd4b533eaffc7e198320435350825a36f7/docs/zh/user_guide/user_manual/prefill_decode_mixed_deployment.md#L255-L270)及 [L293–295](https://github.com/Ascend/MindIE-LLM/blob/69e5a5dd4b533eaffc7e198320435350825a36f7/docs/zh/user_guide/user_manual/prefill_decode_mixed_deployment.md#L293-L295)一致，原来的目录歧义已消除。
- 同行 whl 分支已补“从安装目录开始，启动目录须可写”，分别对应原页[起始步骤 L12–17](https://github.com/Ascend/MindIE-LLM/blob/69e5a5dd4b533eaffc7e198320435350825a36f7/docs/zh/user_guide/user_manual/prefill_decode_mixed_deployment.md#L12-L17)与[入口及可写要求 L117–136](https://github.com/Ascend/MindIE-LLM/blob/69e5a5dd4b533eaffc7e198320435350825a36f7/docs/zh/user_guide/user_manual/prefill_decode_mixed_deployment.md#L117-L136)。未混用 run 包的相对路径命令；与正文 L101、registry 摘要一致，满足第二轮两个分支的同步条件。

## R02（P3）— CLOSED：卡数推荐与 TP 的证据已分开说明

- 正文 L129 已删去“两表卡数列均为 Tensor Parallel 口径”，改为“TP 依据 Qwen README 的 A2 Tensor Parallelism 列；支持列表该列为‘硬件规格’卡数、未明示并行语义”。同一候选仍将 worldSize=2 的推荐卡数归于支持列表，没有变更已选配置。
- 固定 [Qwen README L9–11](https://github.com/Ascend/MindIE-LLM/blob/69e5a5dd4b533eaffc7e198320435350825a36f7/examples/atb_models/examples/models/qwen/README.md#L9-L11)的 A2 列明确为 Tensor Parallelism，Qwen2-7B-Instruct 行包含 world size 2；固定[支持列表 L36–39](https://github.com/Ascend/MindIE-LLM/blob/69e5a5dd4b533eaffc7e198320435350825a36f7/docs/zh/user_guide/model_support_list.md#L36-L39)的对应列为“硬件规格”，A2 行推荐 2 卡。[latest Qwen 节](https://mindie-llm-doc.readthedocs.io/zh-cn/latest/user_guide/model_support_list/#qwen-系列)（本轮取回：2026-10-21）同样未把该列明示为 TP。
- 修订满足第二轮列出的分别归因关闭条件，不再替支持列表定义其未明示的并行语义；两表卡数差异及候选未达可执行条件的限定仍保留，不重开 C05／C06。

## 新发现

无。本轮三处修订范围内未发现新增的证据扩大、模式边界混淆或来源表同步缺口。

## 整体结论

**本轮通过。C03、C07、R02 全部 CLOSED**；其余 7 项沿用 CLOSED，T07-03 的 C01–C08、R01–R02 共 **10 项 CLOSED，开放项为 0**。该结论限于既定审阅范围及本轮三处修订，不扩大此前 CLOSED 项的证据范围。

正文继续保持 `draft / source_checked`。产品包／源码版本映射、权重与依赖身份、connector 等既有 unknown 不因此关闭；模型审阅不建立实际组合可运行性，也不代替真实环境验证。

### 结构检查与写入边界

- 原工作区执行 `PYTHONDONTWRITEBYTECODE=1 make check` 通过：**110 content entries／538 sources**。
- 在 `/private/tmp/t07-03-recheck-3-7ggg4kwt/validation-copy` 的文件副本执行 `make check`、`make build` 均通过；构建仅写入临时副本，仓内 `build/` 未写入。结构校验不代替上述证据核对。
- 对照开始时记录的 **557 个已跟踪／未忽略文件**摘要，原有文件变化为 **0**、删除为 **0**，唯一新增为本报告；未修改正文、来源记录、registry 或历史审阅报告。未修改 `src/kb/`，不新增测试。
