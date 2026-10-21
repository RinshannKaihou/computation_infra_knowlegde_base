# Batch 31 · T07-12 第一轮初审报告

## 会话元数据与结论

| 项目 | 记录 |
|---|---|
| 审阅角色 / 轮次 | 独立批次审阅者；第一轮初审；本会话不承担正文编写或问题修订 |
| 指定及实际执行模型 / 档位 | 指定 `gpt-6.1-sol / xhigh`；实际 `gpt-6.1-sol / xhigh` |
| 模型核验方法 | 从环境 `CODEX_SESSION_ID` / `CODEX_THREAD_ID` 取得当前会话 ID，在当日 sessions 目录按 ID 定位 rollout JSONL（亦为目录内最新文件），读取最新 `turn_context` 的 `model`、`effort`、`cwd` 和 `collaboration_mode.settings`；不以默认配置或历史会话代替 |
| 模型核验结果 | `model=gpt-6.1-sol`、`effort=xhigh`、`cwd=/Users/ywang2397/work/AI_reliability_knowledge_base`；`collaboration_mode.mode=default`，其 `settings.model=gpt-6.1-sol`、`settings.reasoning_effort=xhigh`、`settings.developer_instructions=null`，一致；本轮未另启模型或子代理，无模型/档位回退 |
| 核验坐标 | `/Users/ywang2397/.codex/sessions/2026/10/22/rollout-2026-10-22T00-06-15-01a15f36-97db-7b00-9e92-6860f27347ae.jsonl` L8（`turn_context`，时间戳 `2026-10-21T16:06:23.464Z`）；会话身份另见同文件 L1 `session_meta` |
| 标记事件判定 | 工具输出出现的 `[frontier_llm]` 来自读取 authoring-guide §7 L128 的原文，rollout L38 的事件为 `response_item / custom_tool_call_output`；不是执行模型元数据。用户提示中也有该字样。按本轮明确要求以 `turn_context` 判断，未将引用文字误判为回退 |
| 会话 ID | `01a15f36-97db-7b00-9e92-6860f27347ae` |
| 执行方式 | 当前本地 Codex CLI 会话直接审阅；本地只读核对、GitHub 文件连接器和登记网页只读取证；仅报告落盘 |
| 日期 / 时区 | 2026-10-22 / Asia/Shanghai（UTC+08:00；上述 UTC 时间折算为本地 2026-10-22 00:06:23） |
| 审阅正文 / 行号基准 | `knowledge/07-inference/index.md`，先执行 `wc -l`，结果 **131 行** |
| 正文 SHA-256 | `f3c690d73486a015b37378dc97f6053c1e8480621a3527e2457e3c8848cd23cc`（`shasum -a 256`） |
| 写入范围 | 仅新增 `docs/research/batch-31-t07-12-codex-review.md`；不修改正文、取证记录、registry、计划、历史审阅报告或原工作区构建产物 |

**初审结论：需修订并定向复核，暂不通过。共 4 项开放发现：P1 0 项、P2 2 项（C01–C02）、P3 2 项（C03–C04）。** 缓存身份、batch 生命周期、统计分母和 SLO 核心边界基本保留；主要必修项为 07.3 的验证入口未承担所标方面，以及“均为固定快照”的总括覆盖了仍未定版的来源。七份旧方案实际执行 **0/7** 正确；18 项推理内容缺口的状态同步有对应交付及复核证据。

优先级：P1＝足以严重误导处置的关键错误；P2＝影响技术准确性、证据边界或验收判据的必修事项；P3＝局部措辞、定位与可追溯性问题。下述“正文 L…”均以上表哈希为基准；其他文件分别给出坐标。本报告不替代真实环境验证。

## 范围与方法

先读 `README.md`、`AGENTS.md`、[写作指南](../authoring-guide.md)（含元数据约定及 §7）、[content schema](../../schemas/content.schema.json)及[内容总目录](../../content-outline.md)的 07 域归属。重读[正文](../../knowledge/07-inference/index.md)和[本批取证记录](batch-31-t07-12-sources.md)。验收依据是 [T07-12](../../plans/full-coverage-backlog.yaml) L7160–7214 的 objective 与 L7183–7186 四条 acceptance，不以作者自述“已核对”替代验收。

逐格核对正文 L70–77 的 **8×5＝40 格**，独立打开全部 **17 篇**去重后的所链正文，核对其内容能否承担对应方面；区分概念/支持条件、可观察证据、诊断处置、验证方法、来源案例和实际结果。以下矩阵提供每格落点，不仅检查文件存在。相邻正文只核对被本页调用的部分和边界，不重做其全部技术初审。

读取 L97 的 11 对来源/最终复核文件，核对任务头、目标正文、最终结论及必要边界，并检查是否还有更高序号的复核文件。以 YAML 解析后语义比较及 `git diff -- plans/full-coverage-backlog.yaml` 双重核对相对 HEAD 的变更；逐项比对 topic-coverage、任务状态和缺口归属。读取七份旧实验方案的 frontmatter 与 validation-backlog 的 V01–V07；V07 另重读全文，其余六份本轮不重审实验方法。

本轮定向重新取得的上游证据均已登记于 registry；没有新增来源，也未运行其中任何服务、负载或处置命令：

| 登记来源 / 精确对象 | 本轮核对范围与限制 |
|---|---|
| `src.vllm.inference-v0-14`：[prefix_caching.md](https://github.com/vllm-project/vllm/blob/b17039bccc17b94a2ea107272ad7bc93508708df/docs/design/prefix_caching.md#L1-L36) | GitHub 文件连接器按固定 commit 读取原文件 L1–36，核对 hash 组成、隔离信息及完整 block 限制；不据此证明目标服务命中或隔离已生效 |
| 同上：[serve.py](https://github.com/vllm-project/vllm/blob/b17039bccc17b94a2ea107272ad7bc93508708df/vllm/benchmarks/serve.py#L404-L470) | 原文件 L404–470；核对成功过滤、TPOT 的 0/1 token 分支、ITL 扁平聚合及 goodput 对已给 SLO 的同时满足规则；不重新审查全部 endpoint 路径 |
| `src.ascend.vllm-ascend-v0-14-0rc1`：[conf.py](https://github.com/vllm-project/vllm-ascend/blob/52d4acfa51fb868823d1070b81cbd2d97e9e4696/docs/source/conf.py#L62-L80) | 原文件 L62–80；vLLM substitution 为 v0.14.1，插件为 v0.14.0rc1，不与上游 v0.14.0 拼成已验证配套 |
| `src.ascend.mindie-llm-docs-69e5a5dd`：[release_notes.md](https://github.com/Ascend/MindIE-LLM/blob/69e5a5dd4b533eaffc7e198320435350825a36f7/docs/zh/release_notes.md#L1-L65) | 原文件 L1–65；核对仓内文档自述 3.1.0 及配套表。该文档版本声明不证明全部源码、latest 网站和产品包同版 |
| `src.vllm.rocm-install-doc-v0-14` 对应固定仓内 [gpu.rocm.inc.md](https://github.com/vllm-project/vllm/blob/b17039bccc17b94a2ea107272ad7bc93508708df/docs/getting_started/installation/gpu.rocm.inc.md#L1-L28) | 原文件 L1–28；核对 ROCm/torch 与硬件条件、docker 推荐及无预编译 ROCm wheel 的版本内声明；不是安装成功记录 |
| `src.ascend.mindie-llm-doc-latest`：[模型支持列表](https://mindie-llm-doc.readthedocs.io/zh-cn/latest/user_guide/model_support_list/) | 本日打开精确登记页并定向查看表头、Qwen2-7B-Instruct 行；页面仍走 latest 入口。本轮未建立其部署 commit 与 69e5a5dd 的映射，不把个别行一致推广为整站同版 |
| `src.prometheus.histograms-2026-09-29`：[Histograms and summaries](https://prometheus.io/docs/practices/histograms/) | 本日重开动态页 Quantiles 段，核对 classic histogram 先 rate、合并 bucket 后计算 quantile；不建立特定目标后端的版本兼容结论 |

## 已核实的主链与边界

### 四项重点边界

| 边界 | 独立正文证据 | 本页判断 |
|---|---|---|
| 缓存身份 | execution-and-kv-cache L84–108 区分活动 KV、无活动引用的可复用 block、驱逐与抢占；hash 包含父 hash、精确 token 和额外隔离信息，仅复用完整 block。latency-metrics L213–215 另区分权重加载、本地 prefix 命中、外部 KV load、miss/recompute | L72/L93 未将它们合并为同一缓存对象，未把相似文本当作命中证明；容量和清理的现场验证仍未知 |
| batch 生命周期 | execution-and-kv-cache L43–70、L86–108：每轮活动集合/token 预算变化；结束/取消、释放引用、空闲可复用、驱逐与重算分开。engine-backend-boundaries L65–70 保留 MindIE 与上游的有限比较及未核完整链 | L72/L93 未把 batch 写成固定同行请求，也未把参数同名当跨引擎等价 |
| 统计分母 | latency-metrics L35–46、L101–133、L159–197：request/token/interval 不混计，TPOT eligible 与 0/1 token 规则分开，throughput 分子及窗口固定，失败/取消单列。固定 serve.py 本轮重取支持成功过滤及 interval 聚合 | L76/L94 没有改写分母；“分开报告”是记录要求，不冒称各后端已完整采集到取消 |
| SLO 边界 | latency-metrics L177–189、L217–247：goodput 只计成功且同时满足已声明 SLO 的请求，不等于普通 throughput；实例 p99 不可平均成整体 p99，bucket/window/population 须匹配。长尾实验 L30–32/L66–81 另有预先判据及未决规则 | L76/L94 未引入通用阈值或实测保证；来源案例仍为外部报告。C01 是入口缺失，不是要求补实测 |

### 40 格逐格核对

下表缩写仅用于审阅坐标：E＝[execution-and-kv-cache](../../knowledge/07-inference/execution-and-kv-cache.md)，L＝[model-loading-and-readiness](../../knowledge/07-inference/model-loading-and-readiness.md)，B＝[engine-backend-boundaries](../../knowledge/07-inference/engine-backend-boundaries.md)，M＝[mindie-execution-profile](../../knowledge/07-inference/mindie-execution-profile.md)，Q＝[quantization-and-quality](../../knowledge/07-inference/quantization-and-quality.md)，O＝[output-quality-evaluation](../../knowledge/07-inference/output-quality-evaluation.md)，D＝[distributed-inference-layouts](../../knowledge/07-inference/distributed-inference-layouts.md)，P＝[pd-disaggregation](../../knowledge/07-inference/pd-disaggregation.md)，R＝[routing-and-flow-control](../../knowledge/07-inference/routing-and-flow-control.md)，A＝[capacity-and-autoscaling](../../knowledge/07-inference/capacity-and-autoscaling.md)，S＝[release-and-recovery](../../knowledge/07-inference/release-and-recovery.md)，G＝[gpu-inference-oom-triage](../../knowledge/07-inference/gpu-inference-oom-triage.md)，N＝[ascend-inference-oom-triage](../../knowledge/07-inference/ascend-inference-oom-triage.md)，T＝[latency-metrics](../../knowledge/07-inference/latency-metrics.md)，H＝[长尾诊断](../../knowledge/07-inference/ascend-inference-tail-latency-triage.md)，C＝[长尾来源案例](../../knowledge/07-inference/ascend-inference-tail-latency-source-case.md)，V＝[长尾实验](../../knowledge/07-inference/ascend-inference-tail-latency-experiment.md)。数字为各文件行号。

| 主题 / 本页位置 | 原理与边界 | 设计与使用 | 观测与判断 | 故障与处置 | 验证与案例 |
|---|---|---|---|---|---|
| 07.1 / L70 | E32–70；L59–93，有阶段和状态解释 | L95–115，有 loader/格式/分片边界 | E137–151；L117–129，有执行记录与身份字段 | L131–141，有第一失败分类 | L143–173，有身份、启动、ready、质量、清理及重复设计，未执行 |
| 07.2 / L71 | B48–59，有三线组件职责 | M43–102；B72–118，有配置与有限交集 | M104–109；B65–70，有日志/主动探测及局部语义，指标清单未核继续 unknown | M111–119；B120–129，有分类与升级重核清单 | M121–138，有候选样板绑定和最小设计；不是运行结果，产品包/依赖身份仍缺 |
| 07.3 / L72 | E72–84，KV payload/容量与不同存活状态 | E86–108，抢占/驱逐/复用身份及生命周期 | E43–52、110–151，有迭代调度、指标组合及事件字段 | G71–84；N60–70，有 GPU/NPU 分线容量诊断 | **未满足，C01**：所标 E126–135 是 Ascend 支持/版本限制；E159 只列待验证项，没有所需对照设计或案例入口 |
| 07.4 / L73 | Q42–65，有机制和摘要证据边界 | Q67–78、90–138，有三层事实、累加 unknown、平台矩阵及冲突 | Q80–88，有配置与命中、容量与延迟的区分 | Q149–157，有三层归因与条件回退 | Q140–147；O44–121，有评估、预注册、对照 schema 及来源例，未冒称本库结果 |
| 07.5 / L74 | D47–77；P43–47，有所有权、同步及 PD 动机边界 | D79–99；P55–81，有选型及 connector 分线条件 | D126–135；P83–110，有可观察证据/阶段与指标粒度 | P112–123；S64–72，有已核失败分支、取消、清理 unknown | **内容存在但标签需修，C03**：D137–139 有最小验证，P142 指向长尾方法/质量对照；本格文字却指向 D101–124/P129–135 的支持限制与平台对照 |
| 07.6 / L75 | R45–56，路由/引擎/P-D/健康职责与请求状态分开 | R58–73；A50–80；S48–62，有算法、控制环、发布及回退条件 | R75–91、104–106；A44–59，有预算、信号、窗口及容量判据 | S64–79；A66–70，有故障和 drain/双池分支 | R100–108；S81–92，有有限对照、停止/恢复及请求对账，未执行 |
| 07.7 / L76 | T33–46，有样本对象/单位/定义/分母 | T177–215，有 SLO 集合、失败过滤及 warm/cache 记录要求 | T48–99、217–247，有观察者/时钟及聚合边界 | H50–90，有证据分支、受控对照及停止/完成判据 | T249–262；C27–59；V28–81，有模板、外部未闭环案例和未执行实验，三者不等同实测 |
| 07.8 / L77 | S42–46，有三层健康与制品身份 | S74–79；R93–98，有重试、请求与缓存身份边界 | G86–104；N72–81，有两平台取证差异及未闭环报告形态 | G71–84、106–119；N60–98，有阶段/抛出层、单变量和诊断完成判据 | G81–82、106–119；S81–92 可承担恢复验证；但本格称“两篇 OOM 指南”的定位/归属过宽，见 C03 |

40 格均有链接，文件级可达不等于方面验收通过。07.3 缺少有效的验证方法/案例入口；07.5、07.8 已有可用方法正文，属于入口描述与落点需要校准，不判成正文方法完全缺失。保留的“场景指南”L85–87 仍将独立 OOM 案例/实验列待补，与指南内的方法设计可以并存；本轮不要求为导航验收新增独立 OOM 案例或实施实验。

### 平台、状态与所有权

- **vLLM / Ascend**：E30/L44/B24 以及各篇来源指向上游 `b17039bc…` 与插件 `52d4acf…` 两线；E128–135/T264–270 保留功能矩阵不等于模型/硬件组合支持、310P 限制及 v0.14.1 文档变量冲突。导航没有宣称二者安装配套通过。
- **MindIE**：M36–41 将 `69e5a5dd…` 中自述 3.1.0 的文档线、README 的另一数值线、latest 页抽查及产品包 unknown 分开。L23/L179、B74/B109–118 仍明确部分支持声明来自 2026-10-20 读取的 latest，不能由 M 的固定文档档案反向定版，见 C02。
- **AMD / ROCm**：B90–103、D110–112、P53/P135、G89–103 分别限定安装条件、实现门控、RIXL 分支、HIP 同名接口与目标构建未知；没有由 ROCm 行向 Ascend 迁移 CUDA 字段，也没有把 PyTorch 2.6 语义参考与要求 torch 2.8+ 的 vLLM ROCm 样板拼成已核部署组合。本页的 generic 没有新增兼容承诺。
- **状态**：本章 17 篇正文全部为 `draft`；其中 16 篇 `source_checked`，长尾实验为 `not_verified`，无 `reproduced`。首页自身 `type: index / draft / generic`，schema 不强制其填写 procedure/experiment 的附加字段。来源核对和真实执行分离正确，但“来源核对一概等于固定快照”的措辞需按 C02 修正。
- **跨域归属**：正文 L99/L103–105 保留 02 算子/数值语义、03 通信、04 制品/读取、05 资源/平台、08 证据/质量方法的边界；linked 正文通过普通相对链接调用，未复制或移动主归属。T02-08、T02-09、T02-10、T04-04 的任务及目标条目均存在、任务为 done；本轮不重新为这些依赖的全部技术结论背书。

### 七份旧方案状态

| V 包 | scheme 所指既有实验 | 原方案 / 账本核对 |
|---|---|---|
| V01 | [昇腾版本配套](../../knowledge/02-software-stack/ascend-version-mismatch-experiment.md) | draft / not_verified；planned；executed_at=null |
| V02 | [设备可见性](../../knowledge/05-cluster-platform/ascend-device-visibility-experiment.md) | 同上 |
| V03 | [HCCL 超时](../../knowledge/03-communication/hccl-timeout-experiment.md) | 同上 |
| V04 | [NCCL 超时](../../knowledge/03-communication/nccl-timeout-experiment.md) | 同上 |
| V05 | [GPU→NPU 精度](../../knowledge/06-training/gpu-npu-precision-difference-experiment.md) | 同上 |
| V06 | [Checkpoint 恢复状态](../../knowledge/06-training/checkpoint-state-recovery-experiment.md) | 同上；CPU 路径可准备不等于已执行 |
| V07 | [昇腾推理长尾](../../knowledge/07-inference/ascend-inference-tail-latency-experiment.md) | 同上；全文 L81 明确无测量结果 |

七篇 `applicability.environment_refs`、`verification.evidence_refs` 均空；V01–V07 的 `evidence_refs` 均空、`preparation_instance_ref` 均 null。故 L96 的 **0/7** 与[验证清单](../../plans/validation-backlog.yaml)一致，且不暗示七份准备实例已就绪。导航没有改变这些字段，也没有用编辑审阅关闭真实验证轨道。

### 11 组闭环与 18 项账面同步

正文 L97 的 **22 个文件全部存在且任务对应正确**；逐组最终报告均声明既定范围内闭环，没有用报告存在性代替其结论。所链文件亦为当前命名序列的最终复核；历史报告原有模型记录不改写。

| 任务 / 来源记录 | 所链最终复核及本轮定位 |
|---|---|
| T07-01 / [来源](batch-26-t07-01-sources.md) L3 | [recheck-2](batch-26-t07-01-codex-recheck-2.md) L35，C01–C11 全部关闭；保留 latest gate |
| T07-02 / [来源](batch-26-t07-02-sources.md) L3 | [recheck-5](batch-26-t07-02-codex-recheck-5.md) L34–36，无开放发现，latest/源码/产品包同版仍未证 |
| T07-03 / [来源](batch-26-t07-03-sources.md) L3 | [recheck-3](batch-26-t07-03-codex-recheck-3.md) L35，10 项关闭；不扩大产品包或运行范围 |
| T07-04 / [来源](batch-27-t07-04-sources.md) L3 | [recheck-3](batch-27-t07-04-codex-recheck-3.md) L68/L72，13 项关闭；量化×图等组合仍未验证 |
| T07-05 / [来源](batch-27-t07-05-sources.md) L3 | [recheck-3](batch-27-t07-05-codex-recheck-3.md) L50，7 项关闭；未执行评估 |
| T07-06 / [来源](batch-27-t07-06-sources.md) L3 | [recheck-4](batch-27-t07-06-codex-recheck-4.md) L55，原 11 项及 N01/N02 均关闭；真实硬件验证 0 |
| T07-07 / [来源](batch-27-t07-07-sources.md) L3 | [recheck-3](batch-27-t07-07-codex-recheck-3.md) L64，11 项关闭；不证明恢复/清理/性能/质量等价 |
| T07-08 / [来源](batch-28-t07-08-sources.md) L3 | [recheck-3](batch-28-t07-08-codex-recheck-3.md) L20，剩余条件关闭，既有关闭项沿用，无新增发现 |
| T07-09 / [来源](batch-28-t07-09-sources.md) L3 | [recheck-3](batch-28-t07-09-codex-recheck-3.md) L19–21，既有发现全部关闭；不等于部署/压测 |
| T07-10 / [来源](batch-28-t07-10-sources.md) L3 | [recheck-2](batch-28-t07-10-codex-recheck-2.md) L21，剩余五项关闭，原审阅范围通过 |
| T07-11 / [来源](batch-28-t07-11-sources.md) L3 | [recheck-4](batch-28-t07-11-codex-recheck-4.md) L3，C01–C11 全关、N01 沿用关闭；未验证部署 |

18 项逐组核对结果如下；`closure_lane` 全为 `content`，各 gap 的 `validation_refs` 仍空，不能把内容缺口 closed 解读为相关技术 unknown 已消解。

| 缺口组 | G1 / G2 / G3 对应任务 | 相对 HEAD 变更与关闭证据 |
|---|---|---|
| 07.1-G1…G3 | T07-01 / T07-01 / T07-01 | 三项 status 均 open→closed；L59–173 的加载、身份、诊断和验证计划及最终复核支持内容交付 |
| 07.2-G1…G3 | T07-02 / T07-03 / T07-02＋T07-03 | 三项同上；组件/有限语义、MindIE 实质档案及带 unknown 的交集档案已交付 |
| 07.4-G1…G3 | T07-04 / T07-05 / T07-04 | 三项同上；机制/评估及组合冲突均有正文。关闭的是缺少核对内容，未解决的组合冲突继续 unknown |
| 07.5-G1…G3 | T07-06 / T07-07 / T07-03＋T07-07 | 三项同上；布局/connector/其他引擎 PD 的已核部分和缺证边界已交付；不要求未知底层协议被补成已知 |
| 07.6-G1…G3 | T07-08 / T07-09 / T07-10 | 三项同上；路由、扩缩容、发布恢复方法及固定实现样板已交付，尚未执行 |
| 07.8-G1…G3 | T07-08＋T07-10 / T07-10＋T07-11 / T07-11 | 三项同上；故障/重试、恢复核对及 GPU 专题有正文及复核，独立 OOM 案例/实验仍待补 |

解析相对 HEAD 的整个 YAML 后，共 **27 处语义变更**：上述 **18 处**属于 07 域；另 **9 处**为 06.2-G3、06.4-G2/G3、06.5-G1/G2/G3、06.6-G1/G2/G3 的状态同步，与同工作区训练入口工作并存，**不计为 T07-12 的 18 项，也不据此判为推理任务误伤**。全部变更都只涉及对应 gap 的 `status: open→closed`，没有其他字段改动；07.3/07.7、验证账本和其他主题未被这 18 项修改。`plans/topic-coverage.yaml` 中相应六主题均为 covered_basic、gaps=[]；T07-01–T07-11 为 done，闭环文件如上，足以支持“内容交付状态同步”。

T07-12 本身仍 planned，八主题的 `content_acceptance_status` 仍 planned；本轮初审不替作者更新它们，也不因历史内容缺口 closed 宣告本轮导航验收通过。

## 逐项发现

### C01 · P2 · 07.3 的“验证与案例”格用支持范围声明替代验证入口

- **位置**：正文 L72 第五方面；关联 L66/L91 的五方面核对声明；取证记录 L14/L20–21。
- **问题**：该格唯一链接的文字是“Ascend 样板只能证明自身固定范围”，指向执行/KV 篇的版本/支持边界，后面再写容量实测基线待补。这一组合正确保留未实测事实，却没有把读者送到缓存/调度对照方法或案例，不能完成“完整链接五方面”的要求。来源核对也不能充当真实负载验证方法。
- **证据**：[执行/KV 篇](../../knowledge/07-inference/execution-and-kv-cache.md) L126–135 是功能矩阵、硬件、版本变量及不可外推范围；L137–151 是取证字段；L159 列待验证项，没有 baseline/变体/恢复及判据。反之，任务 07.3 的 `retained_evidence_ids` 已包含[长尾实验](../../knowledge/07-inference/ascend-inference-tail-latency-experiment.md)，该文 L42–53/L55–77 确有 B0/V1/R0、冷热缓存准备、事件关联、停止/恢复和判据，且 V07 仍未执行。本批可以复用该方法入口，不需创造结果。
- **关闭条件**：07.3 验证格直接链接真正承担缓存/调度验证方法或来源案例的既有正文，标签与内容一致；读者能定位对照条件、缓存身份/准备方式、观测和判读边界。容量实测基线、实际清理/命中验证及 V07 未执行状态继续保留；不得为填格而升级 verification。

### C02 · P2 · 固定快照的总括抹去了 MindIE latest 等动态来源的既有限制

- **位置**：正文 L66、L95、L96；取证记录 L13。
- **问题**：本页将 MindIE/ROCm 等档案统一概括为各自“固定快照”，又将来源核对统一解释为对照固定文档/源码。被汇总的证据并非全部已定版：MindIE 的固定仓内 3.1.0 文档线与仍未定版的 latest 支持/快速入门材料是两种身份。将二者一并定版会弱化此前为通过审阅而明确保留的版本 gate；同样，指标及服务控制篇还引用动态 Prometheus/Envoy 页面。
- **证据**：[加载页](../../knowledge/07-inference/model-loading-and-readiness.md) L23/L179 仍按 2026-10-20 latest 记录；[组件档案](../../knowledge/07-inference/engine-backend-boundaries.md) L74/L109–118 明确 latest 支持表未与 `69e5a5dd` 源码或产品包核同版；[MindIE 档案](../../knowledge/07-inference/mindie-execution-profile.md) L38–41 只采信固定仓内 release_notes 作为 3.1.0 文档线、只做页级抽查、不建立整站映射。registry `src.ascend.mindie-llm-doc-latest.revision` 明记 latest 未定版及版本 gate。[T07-02 最终复核](batch-26-t07-02-codex-recheck-5.md) L36 亦明确保留该边界。本轮重开[登记的 latest 页](https://mindie-llm-doc.readthedocs.io/zh-cn/latest/user_guide/model_support_list/)没有取得整站部署 commit 证据；固定 [release_notes](https://github.com/Ascend/MindIE-LLM/blob/69e5a5dd4b533eaffc7e198320435350825a36f7/docs/zh/release_notes.md#L1-L65)只能证明其自身自述。另 T247 明记 Prometheus 动态文档未钉网站 commit，R112 明记 Envoy latest 可变。
- **关闭条件**：导航及本批取证记录准确区分固定 commit/版本文档与按页＋读取日期记录的动态来源；MindIE 3.1.0 仅归属已固定的仓内文档线，latest 与源码/产品包同版及部署组合仍 unknown。保留现有来源，不以改 registry 为“固定”或把 latest 声明整体并入 3.1.0 来消除差异；无需为导航任务新增全站取证。

### C03 · P3 · 07.5/07.8 验证格的标签与实际方法落点不完全对应

- **位置**：正文 L74、L77 的“验证与案例”格。
- **问题**：07.5 把“布局限制与跨页冲突”“昇腾侧与 MindIE 对照”放在验证格，标签引向平台条件，没有指出同文件真正的验证设计。07.8 说“两篇 OOM 指南的单因素验证与状态恢复核对”，实际该链接只指向 GPU 指南，且该完整恢复子流程并非两篇各自都具备。由于链接是整篇，两格均可在目标正文或同格的发布恢复链接找到实质方法，本项判为定位/归属问题，不认定方法正文缺失。
- **证据**：[分布式布局](../../knowledge/07-inference/distributed-inference-layouts.md) L101–124 是所写限制，L137–139 才是单副本影响证据链和 correctness/throughput/latency 最小验证；[PD 篇](../../knowledge/07-inference/pd-disaggregation.md) L129–135 是平台比较，L47/L142 才指明评估纪律和方法入口。[GPU 指南](../../knowledge/07-inference/gpu-inference-oom-triage.md) L81–82/L117 有单因素、退出/清理/再启动及接流恢复门；[昇腾指南](../../knowledge/07-inference/ascend-inference-oom-triage.md) L83–98 为停止/回滚安排及诊断结束判据，不能据此声称它已有 GPU 篇同样的状态恢复子流程；共同的服务层设计在[发布恢复篇](../../knowledge/07-inference/release-and-recovery.md) L81–92。
- **关闭条件**：07.5 的标签直接说明实际验证方法及其未执行状态，支持限制留作边界；07.8 准确区分 GPU 指南、昇腾指南现有判据和发布恢复设计各自承担的内容。可增加节锚点或改准确标签，不强制为各指南扩写同一流程，也不要求实测。

### C04 · P3 · 保留导语仍称新正文正在轮末审阅，与本次闭环口径不一致

- **位置**：正文 L42；对照 L97/L131、取证记录 L3。
- **问题**：保留导语泛称“其余主题继续建设；新正文正在轮末审阅”，而本批已新增八主题五方面表，并列明 T07-01–T07-11 全部最终复核。当前待审对象是 T07-12 导航；不能使读者误以为所列新正文仍全部处于未闭环审阅。正文继续 draft、真实验证待补是另一状态，应分别表达。
- **证据**：上表 11 组最终报告及主计划的 done 状态支持内容审阅已在各自范围闭环；取证记录 L3 同样明确此前置。本页 L131 的新增交付表述也已切换到本批口径。L42 是既有文字，本项要求此次导航修订同步其状态表述，不追改历史记录。
- **关闭条件**：导语明确区分已交付正文的历史审阅闭环、当前 T07-12 审阅阶段及仍缺真实验证的事实；与 L97、场景表和成果段一致，不提前写成本轮初审通过。

## 四条 acceptance 的逐条判断

| 条款 | 核对结论 | 初审判断 |
|---|---|---|
| 1 · 八主题完整链接五方面，covered 07.3/07.7 仍复核四项边界 | 40 格已逐格查阅，四项核心边界保留；07.3 验证格只有支持限制/待补提示；07.5/07.8 方法存在但标签需校准 | **部分满足**：C01 必修，C03 修正定位 |
| 2 · vLLM/Ascend/MindIE/ROCm 各自平台，不给 generic 兼容承诺 | 平台线和硬件/功能 unknown 大体分立；总括把 MindIE latest 等来源说成固定快照 | **部分满足**：C02 必修；未发现新增跨平台兼容承诺 |
| 3 · 来源核对与真实负载验证分开，七份旧方案保持实际状态 | draft/source_checked/not_verified 分开，七份方案及 V01–V07 均未执行，0/7 与账本一致 | **满足状态分离要求**：不证明准备就绪；来源身份措辞仍按 C02 修 |
| 4 · 跨域依赖、稳定 ID/导航及闭环；技术未知不被改成已验证 | ID 未变、依赖/相对链接存在，11 组闭环与 18 项内容状态同步有据；动态来源 gate 被总括弱化，保留导语状态滞后 | **部分满足**：C02/C04；不重开既有任务，也不批准本轮最终覆盖 |

## 结构检查、写入范围与结论

正文 frontmatter 通过 Draft 2020-12 schema 及日期格式检查；稳定 ID 与 HEAD 均为 `inference.index`；3 个 source_refs、22 个 related_ids 均存在。独立清点正文 **122 处本地链接 / 47 个唯一相对目标**，无缺失；该数包含任务闭环、平台及章节入口。本页没有页内锚点，本地检查不证明远程内容、语义或平台适用性。`git diff --check` 通过。

写报告前，原工作区运行 `PYTHONDONTWRITEBYTECODE=1 make check` 通过：**126 content entries / 575 sources**。报告落盘后，在 `/private/tmp/b31-t0712-review-t7fbrqxq/validation-copy` 的源码副本（含本报告及既有 build 链接目标）执行 `make check`、`make build`，均退出 0，结果同为 **126 content entries / 575 sources**，成功生成两个 catalog 文件。构建仅写临时副本，原工作区 build 未变。未修改 `src/kb/`，无需新增测试或执行 `make test`。

入场时工作区已有训练入口、推理入口和 full-coverage-backlog 修改，以及本批 T06-09 三份审阅/来源文件和 T07-12 来源记录。本会话没有创建、修订或回退这些既有文件；计划中的 9 项训练同步不归本会话成果。报告写入前另记录 679 个既有文件的 SHA-256（排除 `.git`、虚拟环境和解释器/测试缓存，包含原有 build）；交付前比对既有文件变化 0、删除 0，唯一新增为本报告。正文复算仍为 131 行及头表所列 SHA-256。

**T07-12 需由编写者按 C01–C04 修订，再由同一审阅者按关闭条件定向复核。** 本会话只记录发现，不承担修订，不把内容缺口关闭、来源核对、编辑初审或结构检查当成真实负载验证。未安装/启动引擎、加载模型、调用健康探针、构造请求负载、修改路由、清理资源或执行故障实验；容量/SLO 基线、实际缓存命中/清理和各部署组合继续按原有 unknown 与验证轨道管理。
