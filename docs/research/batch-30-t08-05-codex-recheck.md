# Batch 30 · T08-05 定向复核报告

## 会话元数据与结论

| 项目 | 记录 |
|---|---|
| 审阅角色 / 轮次 | 独立批次审阅者；第二轮定向复核；本会话不承担正文编写或问题修订 |
| 当前约定 / 实际执行模型 | `gpt-6.1-sol / xhigh`；按本次用户指令及写作指南 §7 核验 |
| 模型核验方法 | 用环境变量 `CODEX_SESSION_ID` 定位 `~/.codex/sessions` 下本会话的 rollout JSONL，读取最新 `turn_context`，同时核对 `collaboration_mode.settings`；不以其他会话或默认配置代替 |
| 模型核验结果 | 本会话只有 1 条 `turn_context`；`model=gpt-6.1-sol`、`effort=xhigh`、`cwd=/Users/ywang2397/work/AI_reliability_knowledge_base`；嵌套设置为同一模型、同一档位；未启动其他模型或子代理 |
| 核验坐标 | `/Users/ywang2397/.codex/sessions/2026/10/21/rollout-2026-10-21T21-21-55-01a15ea0-21a3-7fe0-acec-4f85bdfc0cf6.jsonl` L8；时间戳 `2026-10-21T13:22:09.344Z` |
| 会话 ID / turn ID | `01a15ea0-21a3-7fe0-acec-4f85bdfc0cf6` / `01a15ea0-2403-7601-833f-e7b919e5cde9` |
| 执行方式 / 日期 | 当前本地 Codex CLI 会话直接复核；本地只读检查、上游网页和论文 PDF、GitHub 连接器取证；2026-10-21 / Asia/Shanghai |
| 初审基准 | [初审报告](batch-30-t08-05-codex-review.md)的 C01–C09 及各自关闭条件 |
| 修订后正文 | [统一测试选择、压力/注入与统计方法](../../knowledge/08-reliability/test-design-and-coverage.md)，151 行；SHA-256 `1fe1337bea79dd2549162bb83cf85312bda0a1bf87463e43cc44c5e58330e7ee` |
| 修订记录 | [来源记录](batch-30-t08-05-sources.md)，44 行，重点 L34–44；SHA-256 `2024891fed247c11cfad5922c8c1d680eb50ef29cd373a850f9cec1fe71eac37` |
| registry 快照 | [来源登记](../../sources/registry.yaml)，7212 行；SHA-256 `36d2d69cdd0cf539b74c1f68d9e582ddf01b27976b237910969ef4000d6cb34a`；仅核查本任务相关条目 |
| 写入范围 | 仅新增本报告；不修改正文、来源记录、registry、计划、导航或构建产物 |

**结论：初审项 7/9 CLOSED，C03、C07 仍 OPEN；新增 N01（P3，OPEN）。含新增项合计 7/10 CLOSED，T08-05 本轮暂不通过。** C07 中原有的 MLPerf 仓库主页链接已修正，但其“正文每个外链均逐字匹配登记入口”的完整关闭条件尚未满足。N01 是修订新增引用的依赖登记缺口，与 C07 的字符串核对分别记录，不代表又发现了一项 DCGM 技术错误。

`CLOSED-with-note` 计入 CLOSED；附注均为 P3，不要求实施实验才能关闭。模型审阅不替代真实环境验证；七份方案的真实执行仍为 **0/7**。

## 复核范围与证据

已读 `README.md`、`AGENTS.md`、[写作指南](../authoring-guide.md)、元数据 schema 与内容总目录的 08 域边界。逐项重读修订后正文、作者修订记录及对应 registry 条目；对七份实验方案只重读准备状态、输入、判据、采集与恢复等受发现影响的位置，对相邻正文只核查被调用的入口和边界，不重复整篇初审。

| 证据 | 本轮重新打开的位置与用途 |
|---|---|
| E1 · Kalibera & Jones | [v1 HTML](https://arxiv.org/html/2007.10899v1) §7.1、§7.2.1、§7.3/§7.3.1、§7.4 Eq.13–14；核对均值目标、分层独立性及规划范围。另读 [abs 的 v1 提交历史及许可入口](https://arxiv.org/abs/2007.10899)，打开其指向的 [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/)；用于 C01/C08。未重新通读整篇论文 |
| E2 · SuperBench | [登记论文页](https://www.usenix.org/conference/atc24/presentation/xiong)及 [ATC PDF](https://www.usenix.org/system/files/atc24-xiong.pdf) §3.1（印刷页 839–840，文件页 6–7）、§3.4/Algorithm 2（印刷页 842–843，文件页 9–10）；核对离线学习、后续判定、周期更新及固件/驱动变更后的重调边界；用于 C02 |
| E3 · MLPerf Storage | GitHub 连接器重新取得[固定 commit 的规则原文件](https://github.com/mlcommons/storage/blob/7e71ca162d8f9e7ae4b5b698d7d79b0883817f25/Submission_guidelines.md)，确认文件标题为 V2.0，按返回原文逐行计数核对 L167–180 与 L182–184；用于 C06/C07。网页工具打开该 GitHub URL 返回 cache miss，未用搜索摘要替代 |
| E4 · DCGM | 重新打开修订新增的 [Run Levels and Tests 精确 URL](https://docs.nvidia.com/datacenter/dcgm/latest/user-guide/dcgm-diagnostics.html#run-levels-and-tests)，核对级别、负载及表头的 Hopper/卡数口径；与[节点验收](../../knowledge/01-hardware/node-acceptance-triage.md) L43、L88–93 和 [NCCL 方案](../../knowledge/03-communication/nccl-timeout-experiment.md) L104–123 互核；用于 C03/C07/N01。该 latest 页面仍是可变来源 |
| E5 · 准备与复核 | 重读[验证账本](../../plans/validation-backlog.yaml) V00–V07；七方案的定向坐标列于下表。未执行工具、安装、测量、清缓存、注入、压力或恢复操作 |

### 七方案准备状态的定向核对

所有七份实验的 `verification.status` 仍为 `not_verified`，环境引用及验证证据为空。V01–V07 均为 `planned`，`executed_at: null`、`evidence_refs: []`、`preparation_instance_ref: null`。因此，结果复核的当前状态可以如实登记为“未开始”，不要求虚构原始记录或预先填上已完成的责任安排。

| 方案 | 本轮重读坐标 | 对修订后矩阵的支持 |
|---|---|---|
| [NCCL](../../knowledge/03-communication/nccl-timeout-experiment.md) / V04 | L45–59、L104–139 | 有输入/预算字段、采集与清理设计；实际脚本、时间配置及资源实例未冻结 |
| [HCCL](../../knowledge/03-communication/hccl-timeout-experiment.md) / V03 | L47–61、L97–132 | 同为设计状态；发行物、NPU/rank/网口和时间配置须按 HCCL 独立冻结，不能套用 NCCL 实际值 |
| [版本失配](../../knowledge/02-software-stack/ascend-version-mismatch-experiment.md) / V01 | L45–63、L65–100 | 核对与对照设计存在；L63 明确实际脚本、种子、输入及容差待保存 |
| [设备可见性](../../knowledge/05-cluster-platform/ascend-device-visibility-experiment.md) / V02 | L38–62、L73–107 | 四层检查、枚举输入、回收及判读已有设计；具体 Pod/镜像、脚本及映射尚需冻结 |
| [GPU→NPU 精度](../../knowledge/06-training/gpu-npu-precision-difference-experiment.md) / V05 | L49–65、L115–155、L162 | 必须预注册的字段和规则已列，实际 dtype/模式/指标/容差尚未确定；无实际结果 |
| [checkpoint 状态](../../knowledge/06-training/checkpoint-state-recovery-experiment.md) / V06 | L61–77、L139–174 | 已设计制品/输入身份、快照和判据；没有构建制品、脚本实例或运行证据 |
| [推理长尾](../../knowledge/07-inference/ascend-inference-tail-latency-experiment.md) / V07 | L34–81 | 请求集、独立运行、采集与恢复、三值判读已有设计；实际请求计划/样本量/阈值仍待冻结 |

## C01–C09 逐项状态

下列正文行号以元数据表中的修订后 SHA-256 为准；来源记录简称“记录”。优先级沿用初审，附注另按 P3 处理。

| 编号 | 优先级 | 状态 | 关闭条件核对与依据 |
|---|---|---|---|
| C01 | P2 | **CLOSED** | 正文 L70、L74–77、L138 将均值规划与尾分位拆开，写明分层模型假设、请求/迭代不自动独立、失败请求口径；尾分位方法明确待定，未再从 §7.4 推导 p99 样本数。均值区间方法定位到 §7.3.1；E1 支持该范围，记录 L36 同步。按初审允许“具体尾分位方法保持待定”的处置关闭 |
| C02 | P2 | **CLOSED** | 正文 L79、L148 与记录 L37 区分学习和应用两期，写明周期更新、判据身份与冻结时点，不再把 build-out 自身称为测量前预注册。E2 支持离线/在线边界；本库预注册要求已单列。没有实际判据或验证结果，本次不声称已有某次冻结制品 |
| C03 | P2 | **OPEN** | L45、L53 已区分只读与主动层级，资源占用明显补强；但 L54 基准列仍为“低（需防缓存/后台负载污染）”，且没有在该格落实基准结束后的资源/配置恢复核对。直接用“基准”类别推低风险仍存在，与相邻节点验收 L92 的“高：基准占用整机”不一致。记录 L38 所称“不再按类别统一低”与现文不符；详见未闭项说明 |
| C04 | P2 | **CLOSED-with-note** | L112–124 已列齐方案、环境、脚本/输入、预先判据、执行/采集/恢复、结果复核；区分设计、冻结、执行、复核，明确制品未冻结和复核未开始，要求后续定位原始记录、方法、偏差/停止及复核责任，不再以编辑初审充当实验复核。上述七方案及 V 账本支持 0/7。P3 附注：L124“三行共同结论”应指七份方案；V00 原文是准备实例要求，新增的结果复核细则宜明确为本文要求 |
| C05 | P2 | **CLOSED** | L116–117 将超时窗口具体值列为待冻结，L120 将精度配置/容差列为当前未定，L112/L124 对“设计有”统一限定层级。与原方案相符；记录 L40 同步。没有反向把方案补写成已准备或已运行 |
| C06 | P2 | **CLOSED-with-note** | L71 明确每客户端 S、M 及写/读阶段相关规则的冲突定位，L140/L146 保留未决，不自行选择处方；E3 确认正文与示例确有不一致。记录 L41 区分冲突与待澄清解释。P3 附注：记录称“三倍缓存条件删除”，实际上保留并补足比较对象；registry L234 仍是第十批历史概括，尚未追加本轮冲突提示，独立消费该历史 notes 时应同时看本轮限制 |
| C07 | P2 | **OPEN** | L146 已逐字指向 registry L223 的固定规则入口，原仓库主页缺陷已修；但按初审“每个外链逐字匹配”的完整门槛，13 处外链仅 11 处完全相同：L71 新增行号 fragment，L45 新增 DCGM fragment。去 fragment 后均可对应现有登记，不能据此称坏链；但 L45 对应来源还漏出本文 `source_refs` 和本任务来源核对记录，见 N01。尚不能记录为全篇逐字对齐通过 |
| C08 | P3 | **CLOSED** | registry L7076–7089 已保留稳定 ID，修正 v1 为 2020-07-21、许可为 CC-BY-4.0 及对应链接；正文 L34/L145 与记录 L43 一致。E1 的 abs 提交历史、v1 HTML 与许可落点独立确认，未扩大为额外授权 |
| C09 | P3 | **CLOSED-with-note** | 原文不存在的“第七节”引用已从正文删除；L124 改为明确的验证账本入口并区分编辑与结果复核。L131 对指标篇改称事件损失/可用性/有效产出的合成记账例，与该篇现版 §六 L154–185 相符。P3 附注：记录 L44 称已加入写作指南 §7 的相对链接，实际正文无此链接；关闭依据是消除了错误承诺，不是作者自述的加链动作 |

## 仍 OPEN 的差距与建议

### C03 · 基准风险与恢复仍未按所选负载判定

- **位置与证据**：正文 L54 基准列保留统一“低”；L45 虽有总述，不能消除表内直接结论。[节点验收](../../knowledge/01-hardware/node-acceptance-triage.md) L90–92 对主动诊断和整机通信基准分别登记高影响；[NCCL 方案](../../knowledge/03-communication/nccl-timeout-experiment.md) L108–123 列出资源独占、预算、撤销覆盖、清理及恢复基线。这些是本篇已经调用的边界。原厂 [DCGM 级别表](https://docs.nvidia.com/datacenter/dcgm/latest/user-guide/dcgm-diagnostics.html#run-levels-and-tests)也不能推出某一测试类别统一低风险。
- **建议**：在基准的风险/恢复格按实际计算、显存、网络或存储负载及共享域登记影响、隔离和结束后的资源/配置核对；未知风险保持 unknown。若保留“分钟到小时”概括，限定具体主动级别/负载，不覆盖 DCGM r1 的秒级只读/软件检查。
- **再次关闭所需证据**：被动验收与整机主动诊断/通信基准代入矩阵后，资源、风险、隔离及恢复要求各有明确落点；矩阵不再凭“基准”名称判为低风险。无需实际运行。

### C07 · 原 MLPerf 入口已修，全部外链的关闭门槛尚未完成

本轮逐个提取正文外链，保留原字符串核对 registry；共 **13 处 / 9 个唯一 URL**。11 处逐字匹配登记 `url`；另两处如下：

| 位置 | 字符串差异与实际定位 | 还需完成的事项 |
|---|---|---|
| 正文 L71 | MLPerf 固定规则文件增加 `#L167-L180`；来源身份与 commit 没变，原文件行号有效 | 明确区分登记入口与页内定位；若继续声称“逐字匹配”，入口链接需采用登记值，行号可保留为邻文定位；不能把去 fragment 比较的结果记成原字符串完全相同 |
| 正文 L45 | DCGM user-guide 登记入口增加 `#run-levels-and-tests`；页面及章节可读 | 同样明确入口/定位对应，并补齐 N01 的稳定来源 ID 与本轮核对记录 |

**这两处不是远程失效链接，也没有证据表明它们指向了错误文档。** 本项保持 OPEN 是执行初审已写明的全部外链关闭条件，不能只凭 L146 修正就宣布整项通过。应保留有用的精确定位信息；不得为了匹配而把 registry 改回仓库主页、换版本或删除来源边界。

## 新发现

### N01 · P3 · OPEN · 新增 DCGM 直接引用未关联到本文来源依赖

- **位置**：正文 L45；frontmatter L8–16；来源核对范围 L142–151；记录 L38；registry L1035–1045。
- **证据**：修订新增了 [DCGM Run Levels and Tests](https://docs.nvidia.com/datacenter/dcgm/latest/user-guide/dcgm-diagnostics.html#run-levels-and-tests) 直接技术引用。该页已有稳定登记 ID `src.nvidia.dcgm-diag-user-guide-latest-2026-10-08`，但正文的 8 个 `source_refs` 没有该 ID，来源核对范围及本任务取证表也没有新增该页的读取记录。全库存在来源条目，不等于本文已经关联该依赖；[写作指南 §5](../authoring-guide.md#5-来源证据与许可)要求登记后将稳定 ID 写入条目。相邻节点验收篇的来源依赖不能自动继承到本篇。
- **影响**：从 `source_refs`/catalog 追踪本文依据时会漏掉新引入的可变 DCGM 页面及其观察版本；当前页面可读、级别表存在，因此本项不是对该技术表的反证。
- **建议与关闭条件**：复用上述既有稳定 ID，关联到本文 `source_refs`，在本任务来源记录/核对范围写清精确页、章节、读取日期及 latest 可变边界；不要创建重复来源或把新读到的内容追记为历史核验。C07 另核对入口字符串；N01 不要求增加硬件证据。

## 校验、写入边界与最终判定

- 已运行 `PYTHONDONTWRITEBYTECODE=1 make check`，退出码 0：`PASS: 126 content entries; 574 sources.` 它验证结构和本地文件链接，不验证技术正确性或远程内容。
- 另对正文 frontmatter 运行 Draft 2020-12 schema/日期格式校验，通过；28 处本地相对链接目标存在。原有 8 个来源 ID 均存在，N01 是来源依赖遗漏，现有结构检查不会自动发现。
- 本轮未修改知识内容；按用户“仅新增这一个报告文件”的限定，未运行会重写 `build/` 的 `make build`。未改 `src/kb/`，未运行 `make test`。
- 审阅开始时工作区已有作者对 Batch 30 各篇及 registry 的修订，以及五份初审报告；均未由本会话创建或修改。目标正文、来源记录和 registry 的核对快照在写报告前复读未变化，交付时再次核对；本会话唯一仓库写入为新增本报告。
- HCCL 技术页面的初审读取缺口不在本轮修订涉及的上游证据链内，本轮没有重开或据此补记已核实；尾分位区间方法、真实环境档案、脚本/输入/阈值冻结及所有执行证据继续待准备。

**最终：初审项 7/9 CLOSED；OPEN：C03、C07。新增 N01（P3，OPEN）；含新增项合计 7/10 CLOSED。T08-05 暂不通过，需对应修订后再定向复核；真实执行保持 0/7，模型审阅不替代真实环境验证。**
