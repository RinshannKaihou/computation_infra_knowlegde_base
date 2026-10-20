# Batch 26 T07-03 独立审阅报告

## 审阅头部

- 角色：与正文作者独立的知识库批次审阅者；本轮只记录发现，不修订正文、索引、来源登记或计划。
- 模型／推理档位：`gpt-6.1-sol / xhigh`。已读取本轮本地 CLI 会话 `01a158b9-8b74-7c23-8602-4b666e5b0d70` 的执行元数据：`originator: codex_exec`、`source: exec`、CLI `0.163.0`；已检查的全部 `turn_context` 只有上述单一模型和档位，未见模型回退标记，未派发其他模型或子代理。
- 日期：2026-10-20（Asia/Shanghai）。
- 验收基准：`plans/full-coverage-backlog.yaml:6330` 的 T07-03 五条 acceptance；来源与原文件坐标按 [authoring-guide 第 5 节](../authoring-guide.md#5-来源证据与许可)核对。
- 对象：
  1. `knowledge/07-inference/mindie-execution-profile.md` 全文及 frontmatter。
  2. `knowledge/07-inference/index.md` 本轮新增的 MindIE 条目（第 43 行）及 related ID（第 24 行）。其他批次新增内容仅作为交叉引用背景读取。
  3. `sources/registry.yaml` 新增 `src.ascend.mindie-llm-docs-69e5a5dd`，以及 `src.ascend.mindie-llm-src-69e5a5dd` notes 中本轮 Qwen 扩展。
  4. `docs/research/batch-26-t07-03-sources.md` 作者来源记录。

### 取证方式与限制

1. 通过 GitHub 文件读取连接器，独立重开 `69e5a5dd4b533eaffc7e198320435350825a36f7` 的七个指定文件：`architecture_overview.md`、`service_parameter_configuration.md`、`prefill_decode_mixed_deployment.md`、`release_notes.md`、`log_overview.md`、`offline_inference.md`、Qwen `README.md`。另重开根 README、`.readthedocs.yaml`、`mkdocs.yml` 和仓内 `model_support_list.md`；直接核对两个 example 目录的 Contents API 清单。
2. 网页工具读取 GitHub/raw 地址初次返回 Cache miss，shell 直连也未成功；随后使用 GitHub 连接器取得原文件，未将前述失败算作已取回。Kimi WebBridge 健康探测返回未运行，没有经其取得网页，也没有启动或安装服务。
3. 曾重新读取已有 codeload 压缩包辅助定位：完整 SHA-256 为 `1b67d0215ffc8dd0b0335cd7650b1a9cd53d863b59446b70680c3866d9b6f4f7`，其 PAX `comment` 为上述完整 commit。该包没有重新下载；最终七个指定文件及仓内模型表均与本轮 GitHub 独立重取字节一致，不以作者缓存代替上游取证。
4. 七个指定文件重新计算的 SHA-256 前 16 位依次为：架构 `069f3c6ad68d8c22`、配置 `59f1dd120399191f`、混部部署 `75bd1da15eb171f2`、版本说明 `f4dddd5a096b4f68`、日志 `578c37d87d0c84ae`、离线推理 `c8c3b80637ac4b7b`、Qwen README `09941aede58df7cc`，全部吻合作者记录。仓内模型表为 `cebe1df8005841c3`。
5. 通过网页工具重新打开 [latest 模型支持列表](https://mindie-llm-doc.readthedocs.io/zh-cn/latest/user_guide/model_support_list/)和 [latest 发布说明](https://mindie-llm-doc.readthedocs.io/zh-cn/latest/release_notes/)。核对的是本次工具返回的渲染内容，不是站点部署日志；没有取得站点构建 commit 或构建 ID，不能据此认定全站与固定源码同版。
6. 为核对新增比较与冲突，另从 GitHub 重开同 MindIE commit 的 `policy_factory.cpp`、`fcfs_policy.cpp`、`config_manager_impl.cpp`；重开 vLLM `b17039bccc17b94a2ea107272ad7bc93508708df` 的 `health.py`、`async_llm.py`、`request_queue.py` 及 `scheduler.py` 的 `_preempt_request` 片段。这里只核查报告列明的有限语义，不重做 T07-01／02 全部审阅。
7. 以下 GitHub `#L` 坐标来自保留空行的原始文件，均为 1-based；没有使用网页工具显示行号拼接源码锚点。服务配置页的 Markdown 表每一行可能很长，按原始行核对类型、范围、默认值、单位及模式条件。
8. 未安装、构建或运行 MindIE/vLLM，未加载权重，未发模型请求，未执行量化、硬件测试、配置修改或资源清理。仓库结构检查与清单构建不属于上述运行验证。

## 发现列表

共 **8 项开放发现：P1 0 项、P2 7 项、P3 1 项**。以下关闭条件须由作者修订后接受独立定向复核，本轮不标记任何发现已关闭。

### T07-03-C01 — P2：构建配置及单行一致性不足以关闭 latest 与固定快照的对应 gate

- 位置：`knowledge/07-inference/mindie-execution-profile.md:38`–`:40`；`sources/registry.yaml:6725`、`:6733`；`docs/research/batch-26-t07-03-sources.md:5`、`:33`、`:53`。
- 发现：仓内确有 Read the Docs/MkDocs 构建配置，Qwen2-7B-Instruct 的仓内模型表行也与本次 latest 渲染行一致；这些证据支持“具有该文档树的构建配置”“抽查行一致”，不足以推出“2026-10-20 取回内容对应 69e5a5dd 快照”这一全局版本映射。配置中没有锁定已经部署到 latest 的 commit。README 表与 release_notes 的数值差异已被正确发现，但“README 表滞后”仍是作者解释，来源未声明谁应被判为过期。采信固定 release_notes 作为本页文档线可以成立，不能进一步认定整个开源实现或产品包已核为该发行版。
- 证据：[`.readthedocs.yaml L17–19`](https://github.com/Ascend/MindIE-LLM/blob/69e5a5dd4b533eaffc7e198320435350825a36f7/.readthedocs.yaml#L17-L19)只指定构建使用 `mkdocs.yml`；[MkDocs L1–7](https://github.com/Ascend/MindIE-LLM/blob/69e5a5dd4b533eaffc7e198320435350825a36f7/mkdocs.yml#L1-L7)指定站点 URL、`docs_dir: docs/zh` 与 GitCode 仓库入口，没有站点部署修订。固定 [README L57–61](https://github.com/Ascend/MindIE-LLM/blob/69e5a5dd4b533eaffc7e198320435350825a36f7/README.md#L57-L61)为 2.3.0↔8.5.0；固定 [release_notes L13–38](https://github.com/Ascend/MindIE-LLM/blob/69e5a5dd4b533eaffc7e198320435350825a36f7/docs/zh/release_notes.md#L13-L38)自述 3.1.0 及另一组配套。两者都存在，不构成官方的冲突裁定。
- 关闭条件：保留“本页采用固定快照内自述 3.1.0 的文档”的有限选择；将 README 滞后明确标为推断、保留源码／产品包版本映射 unknown。latest 对应关系继续按页、取回日期和抽查范围记录；如需声明站点对应 commit，补可核验的构建身份或覆盖所引用页面的版本对应证据。同步修正文、登记新条目和来源记录，不能凭本轮推断回填 T07-01／02 的既有 gate。

### T07-03-C02 — P2：文档的抢占开关描述被扩大为固定源码全部抢占行为的结论

- 位置：`knowledge/07-inference/mindie-execution-profile.md:85`、`:117`、`:132`；`sources/registry.yaml:6733`；`docs/research/batch-26-t07-03-sources.md:29`。
- 发现：配置页确实把 `maxPreemptCount>0` 描述为开启抢占，并要求 `cpuMemSize≠0`；正文转述该表本身有依据。但第 132 行将其作为与 vLLM 比较的引擎级“显式开关（默认关）”，没有保留同快照实现中的区别。已核 FCFS 局部路径中，该计数限制的是选择 SWAP 的条件；不足该条件时默认走 RECOMPUTE，而不是跳过抢占。`maxFirstTokenWaitTime` 也不是该运行队列所有抢占的必要条件。因而不能用参数为 0 排除重计算抢占，也不能将所有调度抢占都归入首 token 等待门控。
- 证据：[配置表 L129、L154、L156](https://github.com/Ascend/MindIE-LLM/blob/69e5a5dd4b533eaffc7e198320435350825a36f7/docs/zh/user_guide/user_manual/service_parameter_configuration.md#L129-L156)给出文档口径；[配置校验 L325–328](https://github.com/Ascend/MindIE-LLM/blob/69e5a5dd4b533eaffc7e198320435350825a36f7/src/config_manager/config_manager_impl.cpp#L325-L328)确有 CPU 内存交叉条件。[FCFS L376–395](https://github.com/Ascend/MindIE-LLM/blob/69e5a5dd4b533eaffc7e198320435350825a36f7/src/scheduler/policy/fcfs_policy.cpp#L376-L395)在块追加／分配失败或 `newRequestFirst_` 时调用 `Preempt`，该片段没有 `maxPreemptCount>0` 的总开关；[L468–508](https://github.com/Ascend/MindIE-LLM/blob/69e5a5dd4b533eaffc7e198320435350825a36f7/src/scheduler/policy/fcfs_policy.cpp#L468-L508)先置 RECOMPUTE，仅在 `swapNum<maxPreemptCount && CanSwapOut` 时改为 SWAP，重计算分支会置 WAITING、释放序列并重置计算状态。
- 关闭条件：分开标明“配置文档声明”和“固定源码已核局部模式选择”，记录二者不能直接合并的边界；撤回 0 关闭全部抢占及两个参数门控全部抢占的表述。与 vLLM 的比较只覆盖各自已核路径。可把源码已有的 `requestId`、`seqId`、`preempt mode`、`maxPreemptCount config`、`swapNum` 日志字段作为定向验证观察项，但不得写成已观察到的运行结果；产品包是否采用该路径仍保留 unknown。

### T07-03-C03 — P2：配置摘要遗漏 PD 分离及多机模式的失效条件

- 位置：`knowledge/07-inference/mindie-execution-profile.md:72`、`:79`、`:83`；`sources/registry.yaml:6733`；`docs/research/batch-26-t07-03-sources.md:28`–`:29`。
- 发现：ScheduleConfig 表没有说明 `templateType`、`prefillTimeMsPerReq`、`decodeTimeMsPerReq` 在 PD 分离无效，容易让读者把 Standard/Mix 选择及 P/D 时间估算用于独立 P、D 实例。`worldSize` 被无条件写成须等于使用的 NPU 数，漏掉多机由 ranktable 决定且该字段失效的分支。新来源 notes 的 `maxQueueDelayMicroseconds/maxFirstTokenWaitTime（PD 分离不生效）` 还将失效限定连在两个字段之后；原表只对后者给出此声明。
- 证据：[配置 L128](https://github.com/Ascend/MindIE-LLM/blob/69e5a5dd4b533eaffc7e198320435350825a36f7/docs/zh/user_guide/user_manual/service_parameter_configuration.md#L128)区分多机及 D 分离身份卡数；[L143–156](https://github.com/Ascend/MindIE-LLM/blob/69e5a5dd4b533eaffc7e198320435350825a36f7/docs/zh/user_guide/user_manual/service_parameter_configuration.md#L143-L156)逐项写出上述 PD 失效条件，并未在 `maxQueueDelayMicroseconds` 行写相同限定。[混部部署 L339–346](https://github.com/Ascend/MindIE-LLM/blob/69e5a5dd4b533eaffc7e198320435350825a36f7/docs/zh/user_guide/user_manual/prefill_decode_mixed_deployment.md#L339-L346)进一步明确多机时 `npuDeviceIds/worldSize` 失效，由 ranktable 确定实际卡号和总 Rank 数。
- 关闭条件：在相关参数旁直接补齐模式范围，明确区分单机配置值、多机 ranktable 和 PD 身份；将新来源 notes 中两个等待参数拆开。维持已正确写出的 `tokenTimeout/e2eTimeout` 在 PD 分离无效、`kv_trans_timeout/kv_link_timeout` 仅 PD 分离生效的边界，不把原表没有声明的失效范围自行补出。

### T07-03-C04 — P2：部署支持摘要漏掉已取回的硬件／规模及特性叠加限制

- 位置：`knowledge/07-inference/mindie-execution-profile.md:94`–`:100`；`docs/research/batch-26-t07-03-sources.md:31`、`:33`；对应 acceptance 第 3 条。
- 发现：多机混部只被概括成“单机显存放不下时使用多节点＋TLS/KMC”，遗漏原页明确的硬件、规模和节点采样配置限制；本轮采用的 3.1.0 release_notes 还新增了与本页 SplitFuse、prefix cache 直接相关的叠加约束，正文未记录。作者来源表写“混部+分离模式均有专页”，但列出的精确位置只有混部页；参数存在与源码策略存在不能代替未列明的分离部署依赖取证。
- 证据：[混部部署 L322–326](https://github.com/Ascend/MindIE-LLM/blob/69e5a5dd4b533eaffc7e198320435350825a36f7/docs/zh/user_guide/user_manual/prefill_decode_mixed_deployment.md#L322-L326)在多机节自述仅 Atlas 800I A2、最多 4 机 32 卡、不支持 Atlas 300I Duo，且各节点默认采样参数不一致可能卡死；[release_notes L97–99](https://github.com/Ascend/MindIE-LLM/blob/69e5a5dd4b533eaffc7e198320435350825a36f7/docs/zh/release_notes.md#L97-L99)规定 PD 混部不能同时开启 Prefix Cache、SplitFuse 与 DP>1，PD 分离不受这一限制。[配置 L133](https://github.com/Ascend/MindIE-LLM/blob/69e5a5dd4b533eaffc7e198320435350825a36f7/docs/zh/user_guide/user_manual/service_parameter_configuration.md#L133)把具体分离部署示例指向外部 MindIE Motor 开发指南，并要求关注 HCCL 重传相关变量；本轮记录没有该精确页的独立核对。
- 关闭条件：注明这些是固定文档相应部署段的声明，补齐硬件／规模／一致性限制与 3.1.0 叠加约束，不能扩写为所有模式的一般上限。分开记录 dmi 参数级证据、策略构造级证据及部署依赖未知范围；删除“分离专页已核”的无定位说法，或补精确来源、版本和依赖取证。无需为此假造 connector 实现或实际 PD 运行支持。

### T07-03-C05 — P2：Qwen 样板与模型支持表的卡数差异被写成互证

- 位置：`knowledge/07-inference/mindie-execution-profile.md:125`；`sources/registry.yaml:6719` 的本轮扩展；`docs/research/batch-26-t07-03-sources.md:35`。
- 发现：Qwen README 的 Qwen2-7B-Instruct 行摘录准确，但同型号／同硬件的卡数与仓内模型支持表并不相同。笼统写“读表行互证”，以及“两表维度不同”不足以处理发生在重叠字段上的差异。模型支持表也没有 prefix_cache 或 MindIE Service 两列，不能用它互证这些特性。
- 证据：[固定 Qwen README L9–11](https://github.com/Ascend/MindIE-LLM/blob/69e5a5dd4b533eaffc7e198320435350825a36f7/examples/atb_models/examples/models/qwen/README.md#L9-L11)为 A2 TP 1/2/4/8、300I Duo TP 2/4/8，W8A8／prefix_cache／MindIE Service 均勾选；[固定模型表 L34–39](https://github.com/Ascend/MindIE-LLM/blob/69e5a5dd4b533eaffc7e198320435350825a36f7/docs/zh/user_guide/model_support_list.md#L34-L39)为 A2 1/2/4、300I Duo 1/2，另列 A3 1/2。本轮 [latest 渲染行](https://mindie-llm-doc.readthedocs.io/zh-cn/latest/user_guide/model_support_list/#qwen-系列)与后者相同。README [L31](https://github.com/Ascend/MindIE-LLM/blob/69e5a5dd4b533eaffc7e198320435350825a36f7/examples/atb_models/examples/models/qwen/README.md#L31)还限定其 world size 为对话测试可跑通配置，需考虑输入长度内存占用。
- 关闭条件：逐项注明共同证据（例如 W8A8）、仅 README 声明的列，以及硬件卡数未解决差异；不把差异值并集当已支持范围，也不推定某表过期。候选验证样板使用哪个值、采用什么来源范围须明确；正文、来源扩展及作者记录同步撤回笼统互证。

### T07-03-C06 — P2：尚未把所选模型、执行配置与依赖收束成一个有限样板

- 位置：`knowledge/07-inference/mindie-execution-profile.md:16`、`:54`、`:97`、`:119`、`:121`–`:126`；对应 acceptance 第 1、4 条。
- 发现：已有不可变源码 ref、文档自述发行版、配套表、Qwen 模型名和多种执行选项，但最小验证仍使用未选择的“小模型”，没有把 Qwen2-7B-Instruct 与具体硬件、dtype、backend、单／多机、PD 模式、安装形态结合为同一候选样板。ATB、PyTorch 等实际执行依赖只写已安装，没有版本或逐项 unknown；Qwen 文件中已有的模型专属依赖和 dtype 条件也未进入样板。这样尚不能判断该验证设计到底针对哪条执行路径。此项不要求真实部署，也不要求把未知配套编成已支持组合。
- 证据：T07-03 acceptance 第 1 条要求固定模型、实际适用依赖与运行模式；[离线推理 L5–16](https://github.com/Ascend/MindIE-LLM/blob/69e5a5dd4b533eaffc7e198320435350825a36f7/docs/zh/user_guide/user_manual/offline_inference.md#L5-L16)要求 CANN、PyTorch、Torch-NPU、ATB Models；[Qwen README L71–89](https://github.com/Ascend/MindIE-LLM/blob/69e5a5dd4b533eaffc7e198320435350825a36f7/examples/atb_models/examples/models/qwen/README.md#L71-L89)列出 Qwen2 的 transformers≥4.40.1、Qwen2-7B 建议 BF16、300I Duo 仅 FP16 等条件。兼容矩阵的产品配套本身不能填补这些模型级、运行形态级字段。
- 关闭条件：选定一个文档候选样板，将模型／权重修订身份、硬件与卡数、dtype／量化、backend、PD／并行模式、安装入口和依赖放在同一记录中；已知值给精确来源，未取得的 ATB/PyTorch/制品映射等逐项写 unknown，明确仍未达到可执行条件。把现有启动→确定请求→质量→健康→状态回收→同环境重试设计绑定该样板，保留实际阈值、资源基线或权重身份尚缺的条件，不宣称执行通过。

### T07-03-C07 — P2：将 run 包入口泛化为服务入口，且删掉了后台启动所需部分

- 位置：`knowledge/07-inference/mindie-execution-profile.md:41`、`:54`、`:99`；`sources/registry.yaml:6733`；`docs/research/batch-26-t07-03-sources.md:31`。
- 发现：第 99 行把 `nohup ./bin/mindieservice_daemon` 称为后台启动，但该转述删掉了原命令的重定向及 `&`，`nohup` 本身不会把进程放到后台；同时没有保留它属于 run 包操作分支、需在安装目录相应工作目录执行的条件。原页还给出 whl 的 `mindie_llm_server` 入口。正文把服务化形态直接括注为 daemon，容易把两种包形态及路径混成一个未经限定的命令。来源记录将 daemon 的产品包归属标为推断／待核，正文也应保持这个证据强度。
- 证据：[混部页 whl 分支 L117–131](https://github.com/Ascend/MindIE-LLM/blob/69e5a5dd4b533eaffc7e198320435350825a36f7/docs/zh/user_guide/user_manual/prefill_decode_mixed_deployment.md#L117-L131)使用 `mindie_llm_server`；[run 分支 L256–287](https://github.com/Ascend/MindIE-LLM/blob/69e5a5dd4b533eaffc7e198320435350825a36f7/docs/zh/user_guide/user_manual/prefill_decode_mixed_deployment.md#L256-L287)限定工作目录，后台命令包含 `> output.log 2>&1 &`，也另给前台命令。该页提供启动说明，不证明任意现场已安装相同布局。
- 关闭条件：分别说明 whl/run 入口和工作目录；若保留可复制的后台命令，保持原命令关键 shell 语义及条件完整，或仅描述入口并链接精确步骤。daemon 的制品归属继续标为未确认，不把仓库内未找到实现提升为闭源产品归属的已证事实；无需为审阅执行这些命令。

### T07-03-C08 — P3：把父目录条目数写成 Qwen 同目录的模型目录数

- 位置：`knowledge/07-inference/mindie-execution-profile.md:123`；`sources/registry.yaml:6719` 的本轮扩展；`docs/research/batch-26-t07-03-sources.md:35`。
- 发现：链接定位 `.../models/qwen/`，但括号写“同目录含 36 个模型目录”。Qwen 目录本身有 10 个文件、没有子目录；其父 `models/` 的 36 个条目也只有 34 个目录，另两个为 Python 文件。量化脚本与三个校准 prompt 的存在性核对正确，问题在层级和计数。
- 证据：本轮对固定 commit 的 [models 目录](https://github.com/Ascend/MindIE-LLM/tree/69e5a5dd4b533eaffc7e198320435350825a36f7/examples/atb_models/examples/models)与 [qwen 目录](https://github.com/Ascend/MindIE-LLM/tree/69e5a5dd4b533eaffc7e198320435350825a36f7/examples/atb_models/examples/models/qwen)分别用 Contents API 重取并按 `type` 计数；父目录的两个普通文件是 `clip_score_base_runner.py`、`coco_base_runner.py`。
- 关闭条件：改为准确的父目录／子目录定位与数量，或删除无助于样板追溯的总数；正文、来源 notes 与作者定位表同步修正，保留已核的脚本名和 README 摘要。

## 五条 acceptance 对照

| 验收条款 | 审阅结果 |
|---|---|
| 1. 固定源码 ref／产品发行版、模型、适用依赖和模式，区分 server／LLM／backend | 部分满足。ref 固定、架构分层及文档自述 3.1.0 有证据；站点／源码／发行包对应推断见 C01，有限样板身份与依赖见 C06，服务入口形态见 C07。不能把固定文档自述等同于实现／制品已同版。 |
| 2. 初始化、调度、P/D、block／KV 生命周期及观测字段；vLLM 仅比较已证语义 | 部分满足。架构、配置、日志及健康三态有来源；通过已有加载页／组件页链接复用有限 KV 分配、重置和释放语义，符合一个主归属原则。抢占总开关比较仍需 C02 修订，模式作用范围见 C03。未要求把已有文章全文复制到本页。 |
| 3. 并行／PD／connector／服务依赖的真实支持和限制 | 部分满足。dmi、两个 KV 超时、策略构造存在有依据，connector 未核明确保留；参数失效分支及多机／特性叠加限制缺漏见 C03、C04，Qwen 卡数冲突见 C05。不应将这些缺口统称为完整支持已确认。 |
| 4. 配置、内存、调度／执行异常首证据及最小启动／执行／回收设计 | 部分满足。文件大小／权限、内存超限、离线初始化失败、请求超时的首证据有据；设计覆盖请求、质量、健康、清理和重试，但样板未收束见 C06。C02 所列实现／观测字段可用于定向验证，仍不得冒充本库运行记录。 |
| 5. 至少一个精确配置／源码／测试样板可追溯；不整篇复制、不假造包或现场结果 | 固定 Qwen README、脚本及校准 prompt 能追溯，且未执行脚本；未见全文搬运或伪造运行。重叠支持字段的冲突与目录定位须按 C05、C08 修正；引用存在性不等于已验证该配置可运行。 |

## 审阅维度逐项记录

| 维度 | 核对结论 |
|---|---|
| frontmatter、稳定 ID、标题、类型、领域与草稿状态 | 已核对，未见问题。`inference.mindie-execution-profile`、`reference / inference / draft`，标题一致；平台仅 ascend，没有借 generic 推导适用性。 |
| source_refs、evidence_refs、related_ids 与本地链接 | 已核对，未见问题。引用 ID 均存在，相关正文与来源类型未混用；验证状态为 source_checked，未标 reproduced。 |
| 章节索引的本轮 related ID 与新增链接 | 已核对，未见问题。索引第 24、43 行指向本篇，无重复正文或新的跨领域主归属；技术摘要须随正文发现收敛，不据导航存在宣称通过。 |
| 四层架构与 Server／LLM Manager／Text Generator／Modeling 责任 | 已核对，未见问题。与原架构 L11–31 一致；ACLGraph／ATBGraph 是图后端声明，未冒充硬件验证。服务制品及入口的范围限定另见 C07。 |
| release_notes 产品表及 CANN／MindCluster／CCAE 矩阵数值 | 已核对，未见问题。产品自述 3.1.0、正式版／三个月、推荐配套及 3.1.0 三组矩阵行摘录吻合；跨文档／实现的身份推断另见 C01，遗漏的叠加限制见 C04。 |
| ServerConfig 抽查 | 已核对，未见问题。大小门槛、1026／1027、Prometheus、maxLinkNum=1000／建议300、并发＋两倍排队／第3倍+1拒绝、HTTPS 默认及 openAiSupport 热更新均有原表依据；tokenTimeout/e2eTimeout 默认600秒及 PD 分离无效转述正确。 |
| ModelConfig 内存／超时／权限抽查 | npuMemSize 的 GB 单位、-1／正整数模式、0.8 比例及扣减项、超限启动失败／卡死、多模态与 PD-atb 限制，已核对，未见问题。两个 KV 超时的10／1080秒及建立通信域重试语义有据；worldSize 适用范围见 C03。modelWeightPath 的属组／非软链接／≤750来自混部部署表。 |
| ScheduleConfig 默认值、范围与语义抽查 | 128且其他值为16倍数、50／8192及先达到者组batch、FCFS只能0、150／50毫秒、decode batch默认200／Duo上限2000、5000微秒、2500毫秒、512／128均与原表吻合。抢占文档与实现的边界见 C02；模式失效条件见 C03。 |
| 健康检查三态 | 已核对，未见问题。0关闭、1–100开启并作阈值、同步周期虚拟单Token推理＋利用率、正常／失败且高利用率／失败且低利用率的三态判定准确；未虚构检测周期。本轮另确认原表默认阈值10%，live／ready有状态码映射，但不据此填造一次实际探测。 |
| 日志／指标字段 | 已核对，未见问题。组件枚举、审计／调试分类、Critical及部分Error错误码来源准确；指标清单保留unknown。原日志格式还允许子模块前缀，且仅时间／级别／消息为必选，其他字段受MINDIE_LOG_VERBOSE配置；正文简式未被当作缺字段即故障的判据。 |
| 离线推理的失败清理口径 | 已核对，未见问题。用户自定义修改导致初始化失败需手动结束进程，原页有此限定；没有把它扩写成所有失败的强制处置。 |
| 与 vLLM 的有限对照 | 健康错误标志与Priority队列存在性，已核对，未见问题；`async_llm.py L727–730`、`request_queue.py L131–146`与已有加载页引用吻合。抢占释放／回waiting片段有据，但MindIE总开关对照需C02修订，不能由同名概念建立整体等价。 |
| PD／并行支持与模式范围 | 有发现，见 C03–C05；connector实现未核的unknown本身正确。混部段、分离参数、源码构造路径及外部Motor部署说明属于不同强度证据。 |
| 来源许可、引用强度与复制范围 | 已核对，未见问题。新docs条目采用partial并保留README“本文档”的范围解释及第三方例外；没有把仓库代码许可作为全站无条件再分发许可。交付以链接和归纳为主，未见整篇原文／图像快照搬入。 |
| unknown、适用性与运行真实性 | 未安装／未运行、环境引用为空、指标清单／connector／产品包映射等缺口保留，未见伪造运行结果。版本冲突解释、实际样板依赖及服务入口的证据强度须按C01、C06、C07收窄。 |
| 样板存在性、精确定位及跨表冲突 | 有发现，见 C05、C08。README行及脚本文件确实存在；卡数差异不能用笼统互证掩盖，条目数不能写成子目录数。 |

## 结构检查与写入边界

- 已执行 `PYTHONDONTWRITEBYTECODE=1 make check`，报告落盘后再次执行也通过：110 content entries／538 sources。该结果仅检查结构及本地文件链接。
- 在 `/private/tmp/t07-03-review-evidence/validation-copy` 的工作区文件副本执行 `make check`、`make build`，均通过，仍为110条正文／538项来源；已核对构建清单中的本篇标题、摘要、类型及draft状态。临时副本首次检查因未复制既有 `build/catalog.*`、无法解析历史文档链接而失败；补入这两份既有产物后重新检查及构建通过，未为此修改仓内任何源文件。构建产物只写临时目录。
- 对比本轮审阅写入前的554个已跟踪／未忽略文件摘要，原有文件变化为0；唯一新增为本报告。仓内 `build/` 没有写入。
- 不修改 `src/kb/`，不新增实现测试，不执行推理环境验证；原有工作区改动属于本轮开始前的状态。

## 整体结论

**本轮不通过，需修订后定向复核。** 固定原文重取与摘要核验完成，架构、核心表值、内存公式及健康三态的大部分转述有据；仍有7项P2和1项P3开放。须收窄版本对应推断，分开文档与源码抢占语义，补齐模式／支持限制，处理Qwen跨表差异，并完善候选样板及启动入口。关闭这些发现前，不将T07-03标为审阅通过；任何来源核对或结构检查均不构成真实硬件／产品包兼容性验证。
