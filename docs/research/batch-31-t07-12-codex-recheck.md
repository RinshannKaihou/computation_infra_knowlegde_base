# Batch 31 · T07-12 定向复核报告

## 会话元数据与结论

| 项目 | 记录 |
|---|---|
| 审阅角色 / 轮次 | 原独立审阅者；初审后第一轮定向复核；只核对 C01–C04 的关闭条件及修订引入的回归，不承担正文修订 |
| 指定及实际模型 / 档位 | 指定 `gpt-6.1-sol / xhigh`；实际 `gpt-6.1-sol / xhigh`，符合正式复核要求 |
| 核验方法 | 开始即由环境 `CODEX_SESSION_ID` / `CODEX_THREAD_ID` 定位本会话 rollout JSONL，读取最新 `turn_context`，核对 model、effort、cwd 及 collaboration_mode.settings；交付前再次确认 |
| 核验结果 | `model=gpt-6.1-sol`、`effort=xhigh`、`cwd=/Users/ywang2397/work/AI_reliability_knowledge_base`；`collaboration_mode.mode=default`，`settings.model=gpt-6.1-sol`、`settings.reasoning_effort=xhigh`、`settings.developer_instructions=null`；一致，无模型/档位回退，未另启模型或子代理 |
| 核验坐标 | `/Users/ywang2397/.codex/sessions/2026/10/22/rollout-2026-10-22T00-06-15-01a15f36-97db-7b00-9e92-6860f27347ae.jsonl` **L260**（本轮最新 turn_context，`2026-10-21T16:18:57.509Z`）；同文件 L1 为 session_meta |
| 标记事件判定 | 本轮读取 authoring-guide §7 L128 时出现的 `[frontier_llm]` 为引用文字，rollout L277 类型为 `response_item / custom_tool_call_output`；不构成模型回退。正式判定依据仍为本轮 turn_context |
| 会话 ID / 执行方式 | `01a15f36-97db-7b00-9e92-6860f27347ae`；同一独立审阅者的本地 Codex CLI 会话直接执行 |
| 日期 / 时区 | 2026-10-22 / Asia/Shanghai（UTC+08:00；本轮 turn_context 为本地 00:18:57） |
| 修订正文 / 行数 | `knowledge/07-inference/index.md`，**131 行**（先执行 wc -l） |
| 修订正文 SHA-256 | `d3c5613a7e393a7b275078821304b38f7d398ac75aac56e7122627c7be353eca`（shasum -a 256） |
| 取证记录 / 行数 / SHA-256 | `docs/research/batch-31-t07-12-sources.md`，40 行；`66fa9916dd8498d652999fc97fe8d5fabe7190a9a7589698920122591e1d35ef` |
| 原初审报告 SHA-256 | `f25c12d16ccb5f69b36c0cb7bf3494f7ae66dd69e5721f64a76eeb54c6f6f7f9`；历史报告不修改 |
| 本轮写入范围 | 仅新增 `docs/research/batch-31-t07-12-codex-recheck.md`；不修改正文、来源记录、registry、计划、历史报告及原工作区 build |

**结论：C01、C02、C03、C04 全部 CLOSED；本轮定向复核通过。** 原初审 4 项发现已全部关闭，OPEN＝0；定向范围内未发现需编号 R01 或后续编号的新问题。T07-12 在初审及本轮定向复核覆盖的内容审阅范围内通过；这不构成硬件、平台兼容性、缓存行为或真实负载验证通过。

## 范围与方法

以[初审报告](batch-31-t07-12-codex-review.md)的四项关闭条件为准，独立读取[修订正文](../../knowledge/07-inference/index.md) L42、L66、L72、L74、L77、L95–96 及必要邻接语境，并核对[修订记录](batch-31-t07-12-sources.md) L13、L33–36。没有重做 40 格全量语义审阅、11 组历史任务审阅或 18 项缺口关闭依据审查；这些部分沿用初审范围内结论。

对照初审时保留的源码副本 `/private/tmp/b31-t0712-review-t7fbrqxq/validation-copy`（其 index 为初审所记 `f3c690d7…`），确认本次 index 仅改上述 **7 行**，frontmatter 未变；取证记录仅改 L13 的来源身份摘要，并把初审后修订占位替换为四项记录。重新打开被修订入口调用的正文段落，检查其能否承担新标签，以及未执行、平台/版本 unknown 和适用条件是否保留。没有新增上游技术主张，本轮未重新抓取远程页面或重审引擎实现；初审的上游取证只按原范围沿用。

## C01（P2）— CLOSED

- **修订位置**：正文 L72；取证记录 L33。
- **独立核对**：07.3 验证格现直接链接[昇腾长尾实验设计](../../knowledge/07-inference/ascend-inference-tail-latency-experiment.md)。该文 L42–53 确有 B0/V1/R0、恢复相同缓存准备、冷热分层和 prefix 身份限制；L57–62 要求保存配置差异、实际发起序列、逐请求结果、等待/KV/抢占/阶段关联并检查恢复；L66–77 给出判读、无法判断及停止条件。新标签与目标内容相符，验证入口已能承担缓存/调度对照方法。
- **边界核对**：本页同时保留“未执行”和“容量实测基线待补”；原 Ascend 固定范围链接保留为限制说明，不再是该格唯一依据。实验 frontmatter 仍为 `not_verified / evidence_refs: []`，L19 的单实例前提、P/D 需补条件及 L81 的未执行/不外推边界未变。“可复用”在此是方法复用，没有承诺任一平台或部署已可执行。
- **判定**：满足原关闭条件。未把支持声明当成实验结果，也未为填格升级验证状态。

## C02（P2）— CLOSED

- **修订位置**：正文 L66、L95–96；取证记录 L13/L34。
- **独立核对**：三处总括现明确区分固定 commit、固定仓内文档线、版本化文档与按页＋读取日期记录的动态页面；MindIE 3.1.0 仅归属固定仓内文档线，latest 支持/快速入门与源码/产品包的同版关系没有被确认为成立。L95 新增的[组件档案](../../knowledge/07-inference/engine-backend-boundaries.md)链接有效，该文 L74/L117 仍将 latest 与固定源码/产品包分开；[MindIE 档案](../../knowledge/07-inference/mindie-execution-profile.md) L38–41 保留仓内版本声明、README 差异、页级抽查及产品包 unknown。[加载页](../../knowledge/07-inference/model-loading-and-readiness.md) L23/L179 仍按 2026-10-20 latest 记录。
- **动态及版本来源核对**：正文 L96 显式列举 MindIE latest、Prometheus/Envoy 动态页面；与[指标篇](../../knowledge/07-inference/latency-metrics.md) L247 及[路由篇](../../knowledge/07-inference/routing-and-flow-control.md) L112 的既有限制一致。docs-10.1.0 的既有具体归属仍可在[GPU 指南](../../knowledge/07-inference/gpu-inference-oom-triage.md) L126 和 registry 的 `src.amd.amd-smi-docs-10.1.0` 定位；本页未由这个文档版本推出整套 ROCm 的配套或运行保证。
- **同步及回归核对**：取证记录 L13 同步分列来源身份，明确不把动态页并入定版线；L34 保留同版关系 unknown。registry 与初审副本字节一致，`src.ascend.mindie-llm-doc-latest.revision` 仍为 latest 未定版；没有通过更改登记消除版本 gate。跨平台不互推和 generic 不构成兼容承诺的表述保留。
- **判定**：满足原关闭条件。动态页面未被定版，源码/文档/产品包未被合并为已知同版或已验证组合。

## C03（P3）— CLOSED

- **修订位置**：正文 L74、L77；取证记录 L35。
- **07.5 核对**：新标签明确“单副本失败的最小证据/验证设计与三项最小验证”，与[布局篇](../../knowledge/07-inference/distributed-inference-layouts.md) L137–139 的证据链、correctness/throughput/latency 方法一致，且注明未执行。PD 的“评估建议”由[PD 篇](../../knowledge/07-inference/pd-disaggregation.md) L47 承担，平台对照仍对应 L129–135；L142 继续保留实测效果待验证。布局限制/跨页冲突现明写为支持边界，没有再冒充验证方法。
- **07.8 核对**：[GPU 指南](../../knowledge/07-inference/gpu-inference-oom-triage.md) L81–82/L117 确有单因素、退出/清理/再启动和独立接流恢复门；[昇腾指南](../../knowledge/07-inference/ascend-inference-oom-triage.md) L83–98 仅按其现状承担停止、回滚安排及诊断结束判据。新标签分别链接两篇，不再把 GPU 的完整恢复流程归给两篇共同所有。服务层[发布恢复设计](../../knowledge/07-inference/release-and-recovery.md) L81–92 仍有基线、受控事件、请求对账、恢复/回退及停止闭环，L99 明确未执行。
- **判定**：满足原关闭条件。标签与方法归属一致，方法、支持边界和运行结果没有混用；不需要为关闭本项新增节锚点或扩写相邻正文。

## C04（P3）— CLOSED

- **修订位置**：正文 L42；取证记录 L36。
- **独立核对**：导语已去掉“其余主题继续建设；新正文正在轮末审阅”，改为既有正文在各自批次完成编辑审阅、本页当前处于 T07-12 导航核对阶段，并保留 draft 和未经本地实测。与 L97 的历史闭环定位、L81/L85–87 的来源案例/实验及 OOM 待补状态、L131 的内容交付与后续实测缺口相容。
- **判定**：满足原关闭条件。历史内容审阅、当前导航审阅和真实验证三个状态已区分，未提前宣称本轮复核通过或真实验证完成。

## 修订回归与新增发现

**新增独立发现：0；无 R01 或后续编号。** 本结论限于七行导航修订、取证记录同步及必要邻接语境，不扩展为对全章或依赖篇的新一轮背书。

- **链接与元数据**：正文 126 处本地链接、47 个唯一相对目标均存在，新增方法入口和组件档案入口有效；frontmatter 通过 schema/日期格式校验且与初审一致，稳定 ID 仍为 `inference.index`、`draft / generic`。未新增页内锚点，不以目标文件存在替代上述正文语义核对。
- **边界未升级**：与初审副本摘要逐项比较，12 篇直接涉及关闭条件的关联正文均未变，包含执行/KV、指标、长尾实验、加载、组件、MindIE、路由、布局、PD、两篇 OOM 及发布恢复篇。由此只确认导航对既有方法与限制的准确指引，未新增结果、参数或平台能力声明。
- **验证账本未升级**：validation-backlog 与初审副本一致；V01–V07 仍为 planned、executed_at=null、evidence_refs=[]、preparation_instance_ref=null，0/7 仍成立。来源、full-coverage-backlog 亦与初审副本一致；没有为关闭 C01–C04 修改 18 项账本同步或任务验收状态。
- **状态分离**：source_checked 不代表真实负载验证；容量/SLO 实测基线、实际缓存命中/清理、部署组合及独立 OOM 案例/实验的原有缺口继续保留。

## 检查与写入范围

`git diff --check` 通过。报告落盘后，在 `/private/tmp/b31-t0712-recheck-8wrki6rv/validation-copy` 的源码副本（含本报告及既有 build 链接目标）执行 `make check`、`make build`，均退出 0：**PASS: 126 content entries / 575 sources**，成功生成两个 catalog 文件。使用现有虚拟环境并设置 `PYTHONDONTWRITEBYTECODE=1`，构建仅写临时副本；原工作区 build 未变。检查只验证结构、本地文件引用和生成过程，不证明技术正确性、远端可达性或硬件行为。未修改 `src/kb/`，不新增测试，不执行 `make test`。

本轮入场工作区已有训练/推理入口及 full-coverage-backlog 修改，以及 T06-09 审阅/来源文件、T07-12 初审报告和来源记录。本会话不修改这些文件；报告写入前记录 680 个既有文件的 SHA-256（排除 `.git`、虚拟环境和解释器/测试缓存，包含原 build）。交付前比对既有文件变化 0、删除 0，唯一新增为本报告；两份受审输入仍为头表所列行数及 SHA-256，历史初审报告未变。

**本轮四项：CLOSED＝4、OPEN＝0；新增问题＝0；开放 P1＝0、P2＝0、P3＝0。T07-12 在原审阅及本轮关闭条件范围内通过。** 未执行任何引擎、请求、负载、资源清理、发布或故障实验；模型审阅不替代真实环境验证。
