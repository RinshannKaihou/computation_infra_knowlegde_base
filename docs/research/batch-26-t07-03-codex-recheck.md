# Batch 26 T07-03 修订后定向复核

## 复核头部

- 角色：知识库批次审阅者；对照[初审 C01–C08](batch-26-t07-03-codex-review.md)的关闭条件复核，并检查修订引入的问题。本轮只新增本报告，不修订正文、索引、来源登记、计划或历史报告。
- 日期：2026-10-21（Asia/Shanghai）。
- 实际模型／推理档位：`gpt-6.1-sol / xhigh`。已读取当前本地 CLI 会话 `01a15a83-af18-7521-9968-b129102389ca` 的执行元数据：`originator: codex_exec`、`source: exec`、CLI `0.163.0`；已检查的全部 `turn_context` 只有这一模型与档位，已输出的 assistant 消息未见回退标记；未派发其他模型或子代理。当前会话本身即为本地 Codex CLI 审阅，没有另启一轮审阅。
- 已读约定：根 `AGENTS.md`、`README.md`、[authoring-guide](../authoring-guide.md)、`content-outline.md`；验收基准仍为 `plans/full-coverage-backlog.yaml` 的 T07-03 五条 acceptance。本轮不改变原验收范围。
- 复核对象：[正文](../../knowledge/07-inference/mindie-execution-profile.md)全文及元数据；[来源记录](batch-26-t07-03-sources.md)；[registry](../../sources/registry.yaml) 的 MindIE 相关条目，重点为新 docs 条目和 src 条目的 Qwen 扩展；[章节索引](../../knowledge/07-inference/index.md)的本篇链接。下文仓内行号均为本轮工作区的 1-based 坐标。

### 上游重开与证据范围

通过 GitHub 文件读取连接器，独立重新取得 `Ascend/MindIE-LLM@69e5a5dd4b533eaffc7e198320435350825a36f7` 的原文件，保留空行核对 GitHub 行锚点；另通过该 commit 的 Contents API 分别重取 `examples/atb_models/examples/models/` 与 `qwen/`，按 `type` 计数。未以作者缓存或初审摘要代替本轮上游取证。

| 重开对象 | 本轮主要核对位置 | SHA-256 前 16 位 |
|---|---|---|
| `service_parameter_configuration.md` | L55–67、L128–134、L143–157；逐行核对模式、默认值及抢占文档声明 | `59f1dd120399191f` |
| `prefill_decode_mixed_deployment.md` | L12–17、L117–143、L255–295、L305–346；两种包入口、工作目录与多机限制 | `75bd1da15eb171f2` |
| `release_notes.md` | L13–38、L97–99；文档线及特性叠加约束 | `f4dddd5a096b4f68` |
| `src/scheduler/policy/fcfs_policy.cpp` | L376–395、L468–508；调用、模式选择、日志与 RECOMPUTE 分支 | `41db63a789f6371c` |
| `src/config_manager/config_manager_impl.cpp` | L325–328；CPU 内存交叉校验 | `9bd2feda00c52c8c` |
| Qwen `README.md` | L9–11、L31–38、L71–89；特性、TP 卡数、依赖与 dtype | `09941aede58df7cc` |
| `model_support_list.md` | L3–8、L34–39；支持分级及 Qwen2-7B-Instruct 行 | `cebe1df8005841c3` |
| 根 `README.md`／`.readthedocs.yaml`／`mkdocs.yml` | README L57–61、构建配置 L17–19、MkDocs L1–7 | `1f030a9e43ad6a89`／`50f0d586e4cae46c`／`9d1a133dc432d0ad` |
| `offline_inference.md` | L5–16；执行依赖与失败限定 | `c8c3b80637ac4b7b` |

以上 11 个返回文件均重新计算 Git blob SHA-1，与连接器返回的文件身份一致；作者记录中已有的上述文档 SHA-256 也全部相符。父 `models/` 实得 36 条目（34 个目录、2 个 Python 文件）；`qwen/` 实得 10 个文件、0 个子目录。

另于 2026-10-21 用网页工具重新打开 [latest 模型支持列表的 Qwen 节](https://mindie-llm-doc.readthedocs.io/zh-cn/latest/user_guide/model_support_list/#qwen-系列)，本次返回的 Qwen2-7B-Instruct 行与固定仓内 L39 的卡数及 W8A8 声明相符。该核对仍只覆盖这条记录；没有取得站点构建 ID／部署 commit，不建立整站、源码或产品包的版本映射。

未安装、构建或运行 MindIE/vLLM，未加载权重、发送模型请求、执行量化或硬件验证。vLLM 部分只检查此次比较是否随 MindIE 结论收窄，不重做 T07-01／02 全部源码审阅。

## C01–C08 逐项结论表

“部分修订、未关闭”表示已有改进，但原关闭条件仍有明确缺口；沿用原发现 ID 和优先级，不另计为新发现。

| 初审项 | 本轮结论 | 已核对的修订与证据 | 剩余关闭条件 |
|---|---|---|---|
| **C01（P2）版本 gate 与冲突裁定** | **部分修订、未关闭** | 正文 L39–40、来源记录 L5 与 registry L6733 已收窄为抽查一致、未锁部署 commit、源码／产品包映射 unknown；采信 release_notes 作为文档线也有明确限定。[构建配置](https://github.com/Ascend/MindIE-LLM/blob/69e5a5dd4b533eaffc7e198320435350825a36f7/.readthedocs.yaml#L17-L19)与 [MkDocs](https://github.com/Ascend/MindIE-LLM/blob/69e5a5dd4b533eaffc7e198320435350825a36f7/mkdocs.yml#L1-L7)不提供部署身份；[README L61](https://github.com/Ascend/MindIE-LLM/blob/69e5a5dd4b533eaffc7e198320435350825a36f7/README.md#L57-L61)与 [release_notes L13–38](https://github.com/Ascend/MindIE-LLM/blob/69e5a5dd4b533eaffc7e198320435350825a36f7/docs/zh/release_notes.md#L13-L38)仍仅构成数值差异。 | 同步尚未完成：registry **L6725 的 revision 仍断言 README 为“滞后项”**；来源记录 **L33 仍称“滞后冲突”并归入“官方声明口径”**；**L53 仍称“站点＝仓内 docs 构建、取回对应 69e5a5dd”，且称已同步两条文档条目**。改为有界差异／未裁定表述，撤回全局对应结论；若 L53 保留为历史记录，应就地注明该判断已撤回，不能继续作为有效结论。既有 latest／repo 条目的历史 gate 本身无需被强行关闭。 |
| **C02（P2）抢占文档与源码分立** | **关闭（已核局部路径范围）** | 正文 L86、L119、L137，registry L6733 与来源记录 L29 已撤回“0 关闭全部抢占”，并区分文档声明与 SWAP 计数门控。[FCFS L376–395](https://github.com/Ascend/MindIE-LLM/blob/69e5a5dd4b533eaffc7e198320435350825a36f7/src/scheduler/policy/fcfs_policy.cpp#L376-L395)的相关 Preempt 调用没有所述总开关；[L468–508](https://github.com/Ascend/MindIE-LLM/blob/69e5a5dd4b533eaffc7e198320435350825a36f7/src/scheduler/policy/fcfs_policy.cpp#L468-L508)确认默认 RECOMPUTE、满足计数及可换出条件才选 SWAP，以及已列日志字段。[配置校验 L325–328](https://github.com/Ascend/MindIE-LLM/blob/69e5a5dd4b533eaffc7e198320435350825a36f7/src/config_manager/config_manager_impl.cpp#L325-L328)确认 CPU 内存交叉条件。观察项没有被写成运行结果；vLLM 对照已限定局部链。 | 无原发现剩余修订项。这里的关闭不证明全部抢占触发条件、其他策略或实际产品包均采用该路径。 |
| **C03（P2）PD／多机参数范围** | **部分修订、未关闭** | 正文 L72、L80、L84、L88 和两份来源摘要，已补单／多机分支及 templateType、P/D 时间估算在分离无效，并撤回 maxQueueDelayMicroseconds 的分离失效声明；tokenTimeout/e2eTimeout、两个 KV 超时的既有范围保持正确。对应[配置 L128–134](https://github.com/Ascend/MindIE-LLM/blob/69e5a5dd4b533eaffc7e198320435350825a36f7/docs/zh/user_guide/user_manual/service_parameter_configuration.md#L128-L134)、[L143–156](https://github.com/Ascend/MindIE-LLM/blob/69e5a5dd4b533eaffc7e198320435350825a36f7/docs/zh/user_guide/user_manual/service_parameter_configuration.md#L143-L156)及[多机说明 L339–346](https://github.com/Ascend/MindIE-LLM/blob/69e5a5dd4b533eaffc7e198320435350825a36f7/docs/zh/user_guide/user_manual/prefill_decode_mixed_deployment.md#L339-L346)。 | 原关闭条件还要求区分 **PD 身份**。固定配置 **L128 明确 D 分离推理时须与下发身份设置的卡数一致**，正文 L72、registry L6733 和来源记录 L29 都仍只写单机卡数／多机 ranktable，遗漏该条件。将这条已取得的 D 身份约束补在 worldSize 旁，并在两份来源摘要同步；不能用“Motor 指南未核”代替已经取得的参数行条件。 |
| **C04（P2）部署与叠加限制** | **关闭（文档声明范围）** | 正文 L97、L99–100，registry L6733 与来源记录 L31 已补混部多机的硬件／规模／采样一致性限制；与[混部页 L322–326](https://github.com/Ascend/MindIE-LLM/blob/69e5a5dd4b533eaffc7e198320435350825a36f7/docs/zh/user_guide/user_manual/prefill_decode_mixed_deployment.md#L322-L326)一致。[release_notes L97–99](https://github.com/Ascend/MindIE-LLM/blob/69e5a5dd4b533eaffc7e198320435350825a36f7/docs/zh/release_notes.md#L97-L99)的三特性不能同时开启约束及分离例外已准确记录；没有扩写成任意两项均互斥。[配置 L133](https://github.com/Ascend/MindIE-LLM/blob/69e5a5dd4b533eaffc7e198320435350825a36f7/docs/zh/user_guide/user_manual/service_parameter_configuration.md#L133)的外部 Motor 指南明确未取证，来源表也已撤回分离专页已核的说法。 | 无原发现剩余修订项。分离部署依赖、connector 实现与实际支持仍为 unknown，不因本项关闭而补证。 |
| **C05（P2）Qwen 跨表差异** | **关闭（差异保留）** | 正文 L128–129、registry L6719 与来源记录 L35 已按字段区分：W8A8 支持有共同证据；prefix_cache／MindIE Service 仅 README 有相应列；卡数不取并集、不判过期。重开的 [README L9–11](https://github.com/Ascend/MindIE-LLM/blob/69e5a5dd4b533eaffc7e198320435350825a36f7/examples/atb_models/examples/models/qwen/README.md#L9-L11)、[测试配置限定 L31](https://github.com/Ascend/MindIE-LLM/blob/69e5a5dd4b533eaffc7e198320435350825a36f7/examples/atb_models/examples/models/qwen/README.md#L31)与[固定支持列表 L34–39](https://github.com/Ascend/MindIE-LLM/blob/69e5a5dd4b533eaffc7e198320435350825a36f7/docs/zh/user_guide/model_support_list.md#L34-L39)支持这些转述。transformers≥4.40.1 与 BF16 建议已从 [L71–89](https://github.com/Ascend/MindIE-LLM/blob/69e5a5dd4b533eaffc7e198320435350825a36f7/examples/atb_models/examples/models/qwen/README.md#L71-L89)纳入。 | 无原发现剩余修订项。“口径不同”只是差异背景，未被用于消解冲突；本项关闭不裁定哪套卡数可在现场运行。 |
| **C06（P2）有限候选样板与验证绑定** | **部分修订、未关闭** | 正文 L121、L129 已把验证计划绑定到 Qwen2-7B-Instruct／A2／BF16／atb／standard／单机／whl；权重与 tokenizer 身份、依赖版本、资源／质量阈值缺口及未达可执行条件均有保留。选 BF16 符合 [README L38](https://github.com/Ascend/MindIE-LLM/blob/69e5a5dd4b533eaffc7e198320435350825a36f7/examples/atb_models/examples/models/qwen/README.md#L38)与 [L88–89](https://github.com/Ascend/MindIE-LLM/blob/69e5a5dd4b533eaffc7e198320435350825a36f7/examples/atb_models/examples/models/qwen/README.md#L88-L89)，没有虚构依赖兼容结果。 | L129 的卡数仍为 **1／2／4 备选范围**，没有选定验证样板的 worldSize，也未明确 **TP／DP 等并行选择及是否量化**。BF16 是 dtype，不能代替量化选择；standard 只固定混部身份，不能固定并行配置。原关闭条件要求把这些字段收束为同一候选记录：从所采信范围中选定一组卡数／并行／量化配置，或明确列为分别编号的候选，并让最小设计指向其中一条。可用支持列表的推荐 2 卡作为文档选择，仍不得声明已验证。依赖版本和权重 revision 继续 unknown 完全允许，不要求真实部署后才关闭。 |
| **C07（P2）两入口与启动工作目录** | **部分修订、未关闭** | 正文 L54、L101，registry L6733 与来源记录 L31 已分开 whl／run，后台命令的重定向及 `&` 也完整；daemon 制品归属继续未确认。whl 的 `mindie_llm_server` 及 `Daemon start success!` 同见[混部页 L117–131](https://github.com/Ascend/MindIE-LLM/blob/69e5a5dd4b533eaffc7e198320435350825a36f7/docs/zh/user_guide/user_manual/prefill_decode_mixed_deployment.md#L117-L131)，因此验证计划使用该成功日志没有新证据冲突。 | **工作目录仍未说清**：正文仅写“安装目录对应工作目录”，来源摘要写“安装目录工作目录”，却保留相对命令 `./bin/...`。原页 [L255–270](https://github.com/Ascend/MindIE-LLM/blob/69e5a5dd4b533eaffc7e198320435350825a36f7/docs/zh/user_guide/user_manual/prefill_decode_mixed_deployment.md#L255-L270)明确为 **`{MindIE安装目录}/latest/mindie-service`**；[L293–295](https://github.com/Ascend/MindIE-LLM/blob/69e5a5dd4b533eaffc7e198320435350825a36f7/docs/zh/user_guide/user_manual/prefill_decode_mixed_deployment.md#L293-L295)说明不能在 bin 目录启动。应写出 run 分支准确工作目录，并说明 whl 分支从安装目录开始、启动目录需可写；或删去可复制命令，仅保留分别指向精确步骤的入口链接。同步正文／registry／来源记录即可，无需执行命令。 |
| **C08（P3）目录定位与计数** | **部分修订、未关闭** | 正文 L125、registry L6719 以及来源记录 L35 第一列，已改为父目录 36 条目＝34 目录＋2 文件，与本轮 Contents API 一致。两个普通文件确为 `clip_score_base_runner.py`、`coco_base_runner.py`；Qwen 的脚本和三个 prompt 文件均存在。 | 同一来源记录 **L35 的“精确位置”列仍写“models/ 共 36 个模型目录”**，与该行第一列冲突。将该处同步为 36 条目／34 目录＋2 文件，或删去总数，即可达到原关闭条件。固定[父目录](https://github.com/Ascend/MindIE-LLM/tree/69e5a5dd4b533eaffc7e198320435350825a36f7/examples/atb_models/examples/models)与 [qwen 目录](https://github.com/Ascend/MindIE-LLM/tree/69e5a5dd4b533eaffc7e198320435350825a36f7/examples/atb_models/examples/models/qwen)已经分别重取，不缺上游证据。 |

## 新发现

### T07-03-R01 — P3：新增样板与最小验证设计的相对章节指向写反

- 位置：`knowledge/07-inference/mindie-execution-profile.md:121`、`:131`。
- 发现：L121 写“绑定上节……候选样板”，但候选记录实际在其后的 L129；新增的 L131 又写“下节最小验证设计”，而下一节是“与 vLLM 的有证据对照”，最小验证设计实际在前面的 L121。两个方向均指错，削弱此次新增的样板与计划绑定关系。这是修订引入的定位问题，与 C06 尚未选定具体配置分别计数；未见因此伪造运行结果。
- 证据：本轮重读的[正文](../../knowledge/07-inference/mindie-execution-profile.md)章节顺序为“首失败边界与最小验证设计”→“可追溯样板：Qwen”→“与 vLLM 的有证据对照”。
- 关闭条件：将 L121 改为指向后文候选记录、L131 改为指向前文最小设计，或使用稳定章节链接；同时保留“尚未达到可执行条件、当前仅为计划”的限定。

## 整体结论

**本轮未通过，需继续修订并定向复核。** C02、C04、C05 共 **3 项关闭**；C01、C03、C06、C07、C08 共 **5 项未关闭（4 P2＋1 P3）**。另新增 **R01（P3）**，合计开放 **6 项（4 P2＋2 P3）**，无 P1。原问题的残留未重复编为 R 编号。

主要技术收窄已有依据：抢占不再被写成总开关，多机及三特性叠加限制已补，Qwen 跨表差异也未被合并为支持结论。剩余工作是清除相互矛盾的版本／计数记录，补 D 身份条件、明确候选配置和启动目录，并修正内部定位。文档中允许保留的依赖／权重／产品包／connector unknown 不构成本轮额外补跑硬件的要求。

### 结构检查与写入边界

- 在原工作区执行 `PYTHONDONTWRITEBYTECODE=1 make check`，通过：**110 content entries／538 sources**；报告落盘后再次检查通过。
- 在 `/private/tmp/t07-03-recheck-__ytv28f/validation-copy` 的工作区文件副本执行 `make check`、`make build`，均通过；报告同步到副本后再次检查及构建通过。历史链接所需的既有 `build/catalog.json`／`catalog.md` 一并复制，构建只写临时副本。已核对生成清单中本篇的 ID、标题、摘要及 `reference / inference / draft / source_checked`，未把结构通过当成技术复核通过。
- 对比开始时记录的 **555 个已跟踪／未忽略文件**摘要，原有文件变化为 **0**；唯一新增为本报告。仓内 `build/` 未写入；不修改 `src/kb/`，不新增测试，不执行推理环境验证。
- 模型审阅及来源核对均不代表真实环境验证；正文继续保持草稿，不据本报告建立部署组合或产品包兼容性结论。
