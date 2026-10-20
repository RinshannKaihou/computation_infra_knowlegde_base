# Batch 26 T07-03 第二轮定向复核

## 复核头部

- 角色与范围：知识库批次审阅者；仅复核[第一轮定向复核](batch-26-t07-03-codex-recheck.md)中 C01、C03、C06、C07、C08、R01 的剩余关闭条件及本次修订引入的问题。C02、C04、C05 沿用 **CLOSED**，不扩大其既定证据范围，也不重做整篇初审。
- 日期：2026-10-21（Asia/Shanghai）。
- 实际模型／推理档位：`gpt-6.1-sol / xhigh`。已读取当前本地 Codex CLI 会话 `01a15a88-dea2-7d30-a040-6dc6e0b22927` 的执行元数据：`originator: codex_exec`、`source: exec`、CLI `0.163.0`；已检查的全部 `turn_context` 只有该模型与档位，已输出的 assistant 文本未见回退标记。当前会话直接执行复核，未另启模型或子代理。
- 已读约定：根 `AGENTS.md`、`README.md`、[写作指南](../authoring-guide.md)、`content-outline.md`；参照 `plans/full-coverage-backlog.yaml` 的 T07-03 acceptance，未增加真实部署或硬件验证要求。
- 仓内对象：[正文](../../knowledge/07-inference/mindie-execution-profile.md)、[来源记录](batch-26-t07-03-sources.md)、[registry](../../sources/registry.yaml) 的 MindIE docs 条目及 Qwen 扩展；以当前文件实际内容判断，不以修订摘要代替核对。下文仓内位置均为本轮工作区的 1-based 行号。
- 上游取证：通过 GitHub 文件连接器重新取得 `Ascend/MindIE-LLM@69e5a5dd4b533eaffc7e198320435350825a36f7` 的服务配置页、混部部署页、模型支持列表、Qwen README、根 README、release_notes 六个原文件，保留空行核对行锚点。六文件的 Git blob SHA-1 均与返回身份相符，SHA-256 前 16 位均与第一轮记录一致；另重取该 commit 的父 `models/` Contents API 清单。重新打开 latest 模型支持列表的 Qwen 节，只核该页相关表头及模型行，不建立整站或产品包版本映射。
- 执行边界：未安装、构建或运行 MindIE/vLLM，未执行启动命令、模型请求、量化或硬件测试。本轮仅新增本报告。

## C01（P2）— CLOSED：版本差异与历史对应判断已同步收窄

- 核对位置：registry L6725、L6733；来源记录 L5、L33、L53；正文 L39–40。
- registry `revision` 已把 README 表述改为与 release_notes「数值不同（未裁定，采信 release_notes 作文档线）」。来源表 L33 同样保留差异，并在支持范围列明确「采信 release_notes 为本文档线」，不再以“滞后冲突”作为官方裁定。
- 来源记录 L53 已就地注明首轮「站点＝仓内 docs 构建、取回对应 69e5a5dd」判断被撤回，现限于抽查页级一致；正文、registry notes、来源记录 L5 的有限对应口径一致，源码／产品包映射继续 unknown。
- 重开的[根 README L57–61](https://github.com/Ascend/MindIE-LLM/blob/69e5a5dd4b533eaffc7e198320435350825a36f7/README.md#L57-L61)与 [release_notes L13–38](https://github.com/Ascend/MindIE-LLM/blob/69e5a5dd4b533eaffc7e198320435350825a36f7/docs/zh/release_notes.md#L13-L38)仍分别给出两组版本数值，未提供哪方过期的裁定。现有修订满足第一轮列出的三处同步条件；既有 latest／repo 历史 gate 无须因此被回填为关闭。

## C03（P2）— 部分修订，仍未关闭：来源表遗漏 D 身份约束

- 核对位置：正文 L72；registry L6733；来源记录 L28–29。
- 正文与 registry 已补「PD 分离 D 侧须与下发身份设置的卡数一致」，与固定[配置表 worldSize 行 L128](https://github.com/Ascend/MindIE-LLM/blob/69e5a5dd4b533eaffc7e198320435350825a36f7/docs/zh/user_guide/user_manual/service_parameter_configuration.md#L128)相符；单机卡数、多机 ranktable 分支仍保留。
- **来源记录尚未同步**：L28 只列出 worldSize 字段，L29 仍仅写「worldSize 单机须等于 NPU 数、多机由 ranktable 决定且 npuDeviceIds/worldSize 失效」，没有 D 侧身份卡数条件。因此，修订摘要所称三处同步在当前工作区尚未全部落实。
- 剩余关闭条件：在来源记录的 worldSize 摘要旁补齐该 D 身份约束，并定位到 ModelConfig 表 L128。其余已核模式边界沿用第一轮结论，不要求另取 Motor 指南或执行 PD 验证。本项为原 C03 残留，不另编新发现。

## C06（P2）— CLOSED：候选样板已选定一组配置

- 核对位置：正文 L121、L129、L131。
- 同一候选记录现已收束为 **Qwen2-7B-Instruct／Atlas 800I A2／worldSize=2／TP／BF16 原生、不做量化／backendType=atb／inferMode=standard／单机／whl**；W8A8 被列为后续变体，没有混入本次样板。最小验证设计明确绑定这条记录。
- 选 2 卡符合固定[支持列表 L39](https://github.com/Ascend/MindIE-LLM/blob/69e5a5dd4b533eaffc7e198320435350825a36f7/docs/zh/user_guide/model_support_list.md#L39)的 A2 推荐卡数；TP 的直接依据为 [Qwen README L9–11](https://github.com/Ascend/MindIE-LLM/blob/69e5a5dd4b533eaffc7e198320435350825a36f7/examples/atb_models/examples/models/qwen/README.md#L9-L11)，BF16 依据见 [L38](https://github.com/Ascend/MindIE-LLM/blob/69e5a5dd4b533eaffc7e198320435350825a36f7/examples/atb_models/examples/models/qwen/README.md#L38)及 [L86–89](https://github.com/Ascend/MindIE-LLM/blob/69e5a5dd4b533eaffc7e198320435350825a36f7/examples/atb_models/examples/models/qwen/README.md#L86-L89)。不做量化是本候选的选择，不能由表中 W8A8 支持勾选反推为必须量化。
- 权重／tokenizer revision、依赖版本映射、阈值与资源基线仍明确待定，未达可执行条件、验证保持计划的限定均在。因此第一轮 C06 所要求的配置收束与验证绑定已满足；新增的“两表均为 TP 口径”出处表述另记 **R02（P3）**，不否定所选 TP 配置已有 README 依据。

## C07（P2）— 部分修订，仍未关闭：来源表仍保留含糊工作目录

- 核对位置：正文 L101；registry L6733；来源记录 L31。
- 正文与 registry 已明确 run 分支在 **`{MindIE安装目录}/latest/mindie-service`** 执行完整后台命令，且不能在 bin 目录启动；whl 分支从安装目录开始、启动目录须可写。分别符合[混部页 L12–17](https://github.com/Ascend/MindIE-LLM/blob/69e5a5dd4b533eaffc7e198320435350825a36f7/docs/zh/user_guide/user_manual/prefill_decode_mixed_deployment.md#L12-L17)、[L117–136](https://github.com/Ascend/MindIE-LLM/blob/69e5a5dd4b533eaffc7e198320435350825a36f7/docs/zh/user_guide/user_manual/prefill_decode_mixed_deployment.md#L117-L136)、[L255–270](https://github.com/Ascend/MindIE-LLM/blob/69e5a5dd4b533eaffc7e198320435350825a36f7/docs/zh/user_guide/user_manual/prefill_decode_mixed_deployment.md#L255-L270)与 [L293–295](https://github.com/Ascend/MindIE-LLM/blob/69e5a5dd4b533eaffc7e198320435350825a36f7/docs/zh/user_guide/user_manual/prefill_decode_mixed_deployment.md#L293-L295)。
- **来源记录 L31 未同步**：仍是「run 包在安装目录工作目录 `nohup ./bin/mindieservice_daemon > output.log 2>&1 &`」，没有准确子目录、不能在 bin 启动的条件；whl 仍仅列入口名，缺少起始目录与可写要求。该行继续保留相对路径命令，单列原页行号不能消除摘要本身的工作目录歧义。
- 剩余关闭条件：同步修正来源记录 L31 的两个分支；或删去该行可复制命令，改为分别指向准确步骤的入口链接。正文、registry 本次改动无需返工，无需执行启动命令。本项为原 C07 残留，不另编新发现。

## C08（P3）— CLOSED：精确位置列的计数已一致

- 核对位置：来源记录 L35 的主张列与精确位置列；正文 L125；registry L6719。
- 来源表原残留的「36 个模型目录」已改为「36 个条目（34 目录＋2 个 Python 文件）」，与同一行主张列及其他两处一致。
- 本轮重取固定[父目录清单](https://api.github.com/repos/Ascend/MindIE-LLM/contents/examples/atb_models/examples/models?ref=69e5a5dd4b533eaffc7e198320435350825a36f7)，按 `type` 计数确为 36 条目、34 个目录、2 个普通文件；两文件为 `clip_score_base_runner.py`、`coco_base_runner.py`。满足第一轮剩余关闭条件。

## R01（P3）— CLOSED：样板与验证设计的章节方向已修正

- 核对位置：正文 L121、L123、L129、L131、L133。
- L121 现指「后文‘可追溯样板：Qwen’节」，候选记录位于其后的 Qwen 节；L131 现指「上述最小验证设计（见前节）」，实际对应前面的“首失败边界与最小验证设计”节，没有再误指后面的 vLLM 对照节。
- 两处均保留样板未达可执行条件前设计保持计划的限定。章节定位与绑定关系符合关闭条件。

## 新发现

### T07-03-R02 — P3：新增“两表均为 TP 口径”缺少支持列表的直接依据

- 位置：`knowledge/07-inference/mindie-execution-profile.md:129`，本次新增括注「两表卡数列均为 Tensor Parallel 口径」。
- 发现：Qwen README 的 A2／300I Duo 列明确命名为 Tensor Parallelism；模型支持列表的对应列是“硬件规格”，列出设备与卡数，未明示这些卡数均为 TP，也未声明 DP 等并行组合。本次将两表共同归为 TP 口径，扩大了支持列表本身所提供的证据。该问题属于新增出处表述，不重开已关闭的 C05 卡数差异项，也不把 TP=2 候选误判为无依据。
- 证据：固定 [Qwen README L9–11](https://github.com/Ascend/MindIE-LLM/blob/69e5a5dd4b533eaffc7e198320435350825a36f7/examples/atb_models/examples/models/qwen/README.md#L9-L11)明确给出 Tensor Parallelism 表头；固定[模型支持列表 L36–39](https://github.com/Ascend/MindIE-LLM/blob/69e5a5dd4b533eaffc7e198320435350825a36f7/docs/zh/user_guide/model_support_list.md#L36-L39)只给“硬件规格”与卡数。重开的 [latest Qwen 节](https://mindie-llm-doc.readthedocs.io/zh-cn/latest/user_guide/model_support_list/#qwen-系列)同样没有把该列明示为 TP；网页导航中的“张量并行”入口不构成该列定义。
- 关闭条件：删除“两表……均为”括注，或改为分别说明「2 卡采信支持列表推荐值；TP 依据 Qwen README 的 A2 Tensor Parallelism 列」。如保留两表共同口径结论，须补能定义支持列表该列并行语义的精确证据。无需改变已选配置或补跑硬件。

## 整体结论

**本轮未通过，仍需修订并定向复核。** 本轮六项中，**C01、C06、C08、R01 共 4 项 CLOSED**；**C03、C07 共 2 项仍未关闭（均 P2）**，原因均为来源表未同步到正文与 registry 的修订。C02、C04、C05 共 3 项沿用 CLOSED。另新增 **R02（P3）**，当前合计开放 **3 项（2 P2＋1 P3）**，无 P1。

下一轮只需核对来源记录 L29／L31 的残留与正文 L129 的新增出处表述。允许保留的依赖、权重、产品包及 connector unknown 不因此变成现场验证要求；本报告不建立任何组合的实际可运行性。正文继续为 `draft / source_checked`，模型审阅与结构校验均不代表硬件验证。

### 结构检查与写入边界

- 原工作区执行 `PYTHONDONTWRITEBYTECODE=1 make check` 通过：**110 content entries／538 sources**。
- 在 `/private/tmp/t07-03-recheck-2-0olw4kvo/validation-copy` 的文件副本执行 `make check`、`make build` 均通过；保留历史本地链接需要的既有 catalog 文件，构建产物仅写临时副本。已核对生成清单中本篇的 ID、标题、摘要及 `reference / inference / draft / source_checked`，未把结构通过当作技术通过。
- 对照开始时记录的 **556 个已跟踪／未忽略文件**摘要，原有文件变化为 **0**，唯一新增文件为本报告；仓内 `build/` 未写入。未修改 `src/kb/`，不新增测试。
