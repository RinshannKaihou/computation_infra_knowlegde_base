# Batch 27 · T07-07 第三轮定向复核

## 会话元数据

- 审阅角色：AI 可靠性知识库批次审阅者；仅核对[第二轮复核](batch-27-t07-07-codex-recheck-2.md)仍开放的 C08、C10、N01 是否关闭及本轮修订是否引入新问题。C01、C02、C03、C04、C05、C06、C07、C09 共 8 项 CLOSED 沿用，不重做初审。
- 实际执行模型：`gpt-6.1-sol`；实际推理档位：`xhigh`。
- 核验依据：`CODEX_THREAD_ID=01a15b39-6d18-7613-b7c9-36abd17ba8aa` 对应本地 CLI rollout；`session_meta` 为 `originator=codex_exec`、`source=exec`、`cli_version=0.163.0`，本轮已查 `turn_context` 只有 `model=gpt-6.1-sol / effort=xhigh`，cwd 与下列目录一致。按实际运行元数据记录，未用用户期望或全局配置代填；未调用其他审阅模型，所查记录未见模型切换，助手消息文本未见回退标记。
- 工作目录：`/Users/ywang2397/work/AI_reliability_knowledge_base`；日期：2026-10-21（Asia/Shanghai）。
- 被检对象：工作区当前的 [PD 正文](../../knowledge/07-inference/pd-disaggregation.md)、[T07-07 来源记录](batch-27-t07-07-sources.md)、[registry](../../sources/registry.yaml)。以下行号均为本轮原文件坐标。
- 写入范围：只新增本报告；不代改被检对象、导航、计划或审核状态。按仓库规范重建忽略目录 `build/`。

| 被检文件 | 行数 | SHA-256 |
|---|---|---|
| knowledge/07-inference/pd-disaggregation.md | 160 | `fb62631bc0b58df1019de7cd18142db1d05477797a3dac8eba95107d47e9e371` |
| docs/research/batch-27-t07-07-sources.md | 67 | `91ab71ea428af7302faca3a6708f0616ac17cceffc04e86e95b6b121482529f2` |
| sources/registry.yaml | 6788 | `9b74921fee9f385d28df2f5e6c001cb039b90704a883fd80aba8b799d697082a` |

已读取仓库 `AGENTS.md`、[README](../../README.md)、[写作指南](../authoring-guide.md)、[内容总目录](../../content-outline.md)与[元数据 schema](../../schemas/content.schema.json)。本轮实际重读 `/tmp/b27-fetch/va-disagg_prefill.md` 以及 `/tmp/MindIE-LLM-master/` 内两份 Python 文件、`src/engine/transfer_output_handler.cpp` 的相关原文件区段；重新计算的四份文件完整 SHA-256 **4/4 与[初审记录](batch-27-t07-07-codex-review.md)一致**。证据版本分别为 vLLM Ascend `52d4acfa51fb868823d1070b81cbd2d97e9e4696`、MindIE-LLM `69e5a5dd4b533eaffc7e198320435350825a36f7`。另核对同一 MindIE 快照的 `LICENSE.md` 及三份源码头部许可声明；LICENSE 摘要前 16 位 `1b783a52f139dfb8` 与 registry 一致。

网络工具重新打开固定 commit 的 Ascend PD 指南、MindIE `separate_deployment_engine.py` 与 `LICENSE.md` 均返回 cache miss；本轮不宣称远程 URL 可达性已验证。下列技术判定来自上述本地原文件及其已核摘要，GitHub 行号锚点使用原文件坐标。作者修订清单仅作定位线索，不代替关闭证据。未安装依赖、启动服务或执行 GPU/NPU、故障注入、性能及输出质量实验。

## C08 / C10 / N01 逐项判定

### C08 · P3 · 满足，CLOSED

**位置**：正文 L93、L131；来源记录 L36、L65。

正文 D 预分配行与 Ascend 拉式流程均已使用精确标识符 `RequestStatus.WAITING_FOR_REMOTE_KVS`；第二处反引号内不再含字面星号。对照固定指南 [L45](https://github.com/vllm-project/vllm-ascend/blob/52d4acfa51fb868823d1070b81cbd2d97e9e4696/docs/source/developer_guide/feature_guide/disaggregated_prefill.md#L45)与 [L51](https://github.com/vllm-project/vllm-ascend/blob/52d4acfa51fb868823d1070b81cbd2d97e9e4696/docs/source/developer_guide/feature_guide/disaggregated_prefill.md#L51)，词尾均带 S，与当前正文一致。

来源记录 L65 同步改为 `WAITING_FOR_REMOTE_KVS`，明确 L45/L51 与“词尾带 S——修订轮更正”；原先把缺 S 形态归为指南原文的错误说明已替换，主表 L36 也保持正确形态。对当前正文与来源记录扫描，未见缺 S 的状态名或反引号内加粗标记残留。第二轮剩余关闭条件满足；其余已满足部分沿用。

### C10 · P2 · 满足，CLOSED

**位置**：来源记录 L38、L46、L67；正文 L123、L133、L153。

主张—来源定位表 L38 的支持范围单元格已直接改为“connector 底层协议/完整路径未核”，并在该单元格明确撤回初稿“不在开源仓”、说明开源仓已见封装，指向正文与 unknown 4。L46 继续记录底层传输协议及完整路径未核，并撤回初稿旧断言；主表与 unknown 清单现已一致，不再需要读者依靠末尾修订清单消解冲突。

局部证据与保守边界仍成立：Python [L432–452](https://github.com/Ascend/MindIE-LLM/blob/69e5a5dd4b533eaffc7e198320435350825a36f7/mindie_llm/text_generator/utils/separate_deployment_engine.py#L432-L452)包含 `cache_manager.pull_blocks` 调用及 CANN 异常处理，[L575–603](https://github.com/Ascend/MindIE-LLM/blob/69e5a5dd4b533eaffc7e198320435350825a36f7/mindie_llm/text_generator/utils/separate_deployment_engine.py#L575-L603)包含远端 instance 已链接与目标 block ID 范围检查；C++ [L24–58](https://github.com/Ascend/MindIE-LLM/blob/69e5a5dd4b533eaffc7e198320435350825a36f7/src/engine/transfer_output_handler.cpp#L24-L58)处理请求 ID、取消后结果与失败回调。`KvTransferAgent` 的[占位类 L10–17](https://github.com/Ascend/MindIE-LLM/blob/69e5a5dd4b533eaffc7e198320435350825a36f7/mindie_llm/distributed/kv_transfer/kv_transfer_agent.py#L10-L17)仍不被用作全仓缺位证据，外部 `llm_datadist` 的底层协议、完整路径与指标保持 unknown。第二轮剩余关闭条件满足，无需扩查该依赖。

### N01 · P3 · 满足，CLOSED（沿用第一轮新增项）

**位置**：正文 frontmatter L8–13、L24–32；registry L6630–6643、L6708–6721；来源记录 L52–53、L67。

`source_refs` 与 `verification.evidence_refs` 现均包含 `src.ascend.mindie-llm-repo-69e5a5dd` 和 `src.ascend.mindie-llm-src-69e5a5dd`。Python 路径的验证证据已关联到仓库级来源，C++ `src/` 路径继续关联源码切面；不再只靠 docs 或 `src/` 条目承载 Python 的核对声明。

registry 的本轮新增说明实际位于 mindie-repo 的 **`license.notes`（L6642）**：明确列出 `separate_deployment_engine.py`、`kv_transfer_agent.py` 及局部取证范围，以本条仓库身份关联登记，许可按根 `LICENSE.md` 口径，并交叉指向 mindie-src 顶层 notes 的同轮说明。其仓库源码 scope 与根 LICENSE 链接分别在 L6639、L6641；两份 Python 文件头部也声明 Mulan PSL v2。该关联虽写在 `license.notes`，已清楚表达证据归属与许可依据，满足第二轮要求，不必为字段位置另立问题。L6643 的“仅锚定仓库身份与 README 口径”属于明确标记的 Batch 26 取证说明，当前 Batch 27 关联由 L6642 另行写明。

mindie-src 的 URL、许可 scope 仍限定 `src/`（L6710、L6717）；L6721 保留 C++ 取证、Python 局部事实与底层依赖 unknown。跨来源说明未将其 scope 自动扩成全仓。文档许可继续由独立 docs 条目承载，未把文档与源码许可合并；本轮未扩展到第三方依赖许可或仓库整体再分发结论。

来源记录“集成轮结果”L52 已按路径区分 Python→mindie-repo、C++→mindie-src，L53 列出原三项文档/实现 notes 扩展，L67 保留本轮局部事实定位。原先“全部文件落在既有三个 scope”的现行汇总已被替换；当前汇总与正文五项来源/证据关联、registry 实际登记相符。第二轮三项剩余关闭条件均满足，无需新增来源 ID。

## 新问题

**未发现本轮修订引入、需要另立 ID 的新问题。** C08 的标识符及原文归因、C10 的主表旧断言、N01 的 Python/C++ 证据与来源 scope 已分别闭环。根 LICENSE 的关联没有覆盖第三方依赖，局部源码核对也未被扩大为完整传输路径、平台配套或运行成功保证。其余 8 项 CLOSED 沿用原审阅范围，不据本轮未重审扩大其结论。

## 整体结论

**本轮定向复核通过。** C08、C10、N01 全部关闭；连同沿用的 8 项 CLOSED，累计 11 个既有问题全部关闭，当前开放项为 0。本结论仅覆盖 T07-07 既有发现的修订闭环及本轮修订引入的问题。

已执行 `make check`、`make build`，均通过：**112 content entries / 542 sources**。这些检查只验证结构与本地文件链接，不证明技术正确性、远程链接可达性或真实平台行为。正文仍为 `draft / source_checked`，没有建立硬件兼容、资源回收完成、恢复成功、性能改善或输出质量等价的实测结论；未修改 `src/kb/`，未新增测试。

交付前逐文件 SHA-256 比对确认，入场取样的 580 个既有源文件均未变化。本轮只写入本报告并重建忽略目录 `build/`；期间另有 `batch-27-t07-05-codex-recheck-3.md` 出现在工作区，本轮未写入或修改该文件。

统计：本轮定向复核 3 项（CLOSED=3，OPEN=0）；沿用 CLOSED=8；累计既有问题 11 项（CLOSED=11，OPEN=0；开放 P1=0、P2=0、P3=0）；本轮新问题=0；make check=PASS；make build=PASS；硬件验证=未执行；整体=本轮定向复核通过。
