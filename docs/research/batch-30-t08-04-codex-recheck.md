# Batch 30 · T08-04 定向复核报告（第二轮）

## 会话元数据与结论

| 项目 | 记录 |
|---|---|
| 审阅角色 | 独立批次审阅者；仅复核初审关闭条件与修订引入的问题，不承担正文编写或问题修订 |
| 实际执行模型 / 档位 | `gpt-6.1-sol / xhigh` |
| 模型核验方法 | 读取环境中的 `CODEX_THREAD_ID`、`CODEX_SESSION_ID`，二者均为下列会话 ID；据此定位 `~/.codex/sessions` 中本会话 rollout，逐行解析 JSONL，读取最新 `turn_context`，与 `session_meta` 和 `collaboration_mode.settings` 交叉核对 |
| 模型核验结果 | `model=gpt-6.1-sol`、`effort=xhigh`、`cwd=/Users/ywang2397/work/AI_reliability_knowledge_base`；嵌套设置亦为该模型与档位，符合本轮用户指定及写作指南 §7；未另启模型或子代理 |
| 模型核验坐标 | `/Users/ywang2397/.codex/sessions/2026/10/21/rollout-2026-10-21T21-21-55-01a15ea0-21a2-7860-9cc6-9041fc437865.jsonl` L8，`ordinal=7`，时间戳 `2026-10-21T13:22:15.231Z` |
| 会话 / turn ID | `01a15ea0-21a2-7860-9cc6-9041fc437865` / `01a15ea0-2402-79e2-addd-6f20540fca79` |
| 执行方式 | 当前本地 Codex CLI 直接复核；同文件 L1 的 `session_meta.originator=codex_exec`、`cli_version=0.163.0`、`source=exec`，未借用其他会话的模型记录 |
| 日期 / 时区 | 2026-10-21 / Asia/Shanghai |
| 初审依据 | [T08-04 初审报告](batch-30-t08-04-codex-review.md)，逐项采用 C01–C11 的关闭条件 |
| 修订后正文 | [静默错误与计算完整性判定](../../knowledge/08-reliability/silent-errors-and-integrity.md)，212 行（含 frontmatter） |
| 正文 SHA-256 | `9068d2aa0803da714f91d762ee5429e647551e8e5f7a27fe8592504a2c7d3af8` |
| 修订记录 | [来源记录](batch-30-t08-04-sources.md) L37–49；SHA-256：`3e966db8c6f98150df0c9d1da25ee435ad092f3bf27d8c82438861961e5e9962` |
| registry 快照 | [sources/registry.yaml](../../sources/registry.yaml)，7212 行；SHA-256：`36d2d69cdd0cf539b74c1f68d9e582ddf01b27976b237910969ef4000d6cb34a` |
| 写入范围 | 仅新增本报告；正文、来源记录、registry、导航、计划及本仓库构建产物均不修改 |

**复核结论：T08-04 尚未通过。初审项 6/11 CLOSED，5/11 OPEN（C02、C03、C05、C06、C09）；新增 N01（P2，OPEN）。合计 6/12 CLOSED，仍需作者修订及定向复核。**

沿用初审优先级：P1 为关键错误，P2 为影响准确性、证据边界或验收的必修项，P3 为局部措辞与追溯问题。C01 的非阻塞措辞建议按 P3 备注处理，不计为新增开放发现。模型审阅不替代真实环境验证。

## 复核范围与方法

先读 `README.md`、`AGENTS.md`、`docs/authoring-guide.md`、`content-outline.md` 与元数据 schema。重读修订后正文，逐项对照初审关闭条件、来源记录末尾的作者自述及本任务 registry 条目；作者自述不作为关闭证据。五条 acceptance 仅用于解释原发现边界，没有重新扩大为整篇初审。

涉及上游的项重新打开精确来源：2203.08989v1 的表 1、§5.2.2、§6；ACL 正式 PDF 的 §4.2、Table 3、§9、附录 D 与 E.5，以及 arXiv:2502.12340v1 的附录 D.1–D.4；OCP 的 §3.1、§5.1、§5.2、§5.3.1、§6.3.2；PyTorch 2.6 的数值、可复现性、testing 页面与固定 Adam 源码；DCGM 官方诊断页、固定字段源码；RCCL 固定 tag README；Ascend ECC、msprobe 比对与许可、FaultDiag 固定文件。SuperBench 和 Llama 3 仅复核本次补链所指对象与限定口径。

GitHub 文件由连接器按指定 tag/commit 读取，报告所列原文件行号按返回内容计数。PDF 使用可检索正文核对，页码注明印刷页与文件页序；本轮不声称完成 PDF 图像独立核验。DCMI 精确页直接打开失败后，从同版本 `dcmi_006.html` 的 `dcmi_get_device_ecc_info` 链接进入同一个 `dcmi_047.html` 并读取，未用相邻页替代。

## C01–C11 逐项状态

下表“正文 L…”均对应上述正文 SHA-256；registry 坐标对应上述快照。

| 编号 | 优先级 | 状态 | 关闭条件复核依据 |
|---|---|---|---|
| C01 | P2 | **CLOSED** | 正文 L51、L61–69 将硬件原生检测、应用间接症状、主动校验分开，L162 也不再把主动诊断全部归为已有硬件告警。重新核对 [OCP §3.1/§5.1](https://www.opencompute.org/documents/sdc-in-ai-ocp-whitepaper-final-pdf) 与 [DCGM GPU Memory Plugin](https://docs.nvidia.com/datacenter/dcgm/latest/user-guide/dcgm-diagnostics.html#gpu-memory-plugin)：后者明确写入后回读及 mismatch 判据。无通用覆盖率边界保留。P3 备注：L189 的“被动日志”宜限定为硬件错误日志/健康摘要；同句已保留应用症状与主动校验，按上下文不再作全部被动分析不可用的结论。 |
| C02 | P2 | **OPEN** | 正文 L84、L91–92 的分母仍不统一，时间行仍以 Fleetscanner 扫描/共同检出与 Ripple 发布作为两列内容；与“每行两列对象、分母、起止与终点可直接比较”的关闭条件有差距。已核 [2203.08989v1 表 1、§6.1–§6.3](https://arxiv.org/html/2203.08989v1)。范围已从多数收缩为较大子集，这部分满足；其余见下文。 |
| C03 | P2 | **OPEN** | 正文 L136–138 已补三类方法，但没有完成每类覆盖、成本、假阴性/误报与盲区的可核比较。新增成本断言和任务质量误报条件仍有缺口，且 L136 出现 N01。重开 [PyTorch 2.6 assert_close](https://docs.pytorch.org/docs/2.6/testing.html#torch.testing.assert_close) 与固定 msprobe 比对文档，确认其结构/数值/指纹检查不能合并为同一覆盖断言；见下文。 |
| C04 | P2 | **CLOSED** | 正文 L107–124、L142、L156、L200 已解释暂态 activation 经梯度、Adam 持久状态、update、checkpoint 跨 step 存续；明确最新 checkpoint 可能受污染，先核输入/参考身份，并保留软件/数据/算法与硬件候选分支。重读 [Adam 固定源码 L280–302](https://github.com/pytorch/pytorch/blob/1eba9b3aa3c43f86f4a2c807ac8e12c4a7767340/torch/optim/adam.py#L280-L302)，该状态依赖支持正文所标“方法推导”；[OCP §5.3.1/§6.3.2](https://www.opencompute.org/documents/sdc-in-ai-ocp-whitepaper-final-pdf) 支持此前正确状态及延迟发现的回滚代价。正文已链接 06/04 主归属，06 篇“恢复后验证”L150–163 提供状态、同输入单步与持续窗口判据。此项技术内容关闭，新增源码的登记映射仍由 C06 处理。 |
| C05 | P2 | **OPEN** | 正文 L162–164 增加了版本/tag 和被动/主动区分，属于实质改进；但 NVIDIA 仍只写“字段与健康判定”“各插件的前提与判据”，没有在清单中记录所采信的具体字段/判据及支持前提，也未把未核能力逐项列为 unknown。AMD 的 `-c`/`#wrong` 仍只提名称，未知项仅是发生率。不能以增加版本名视作整张版本化能力清单已交付；见下文。 |
| C06 | P2 | **OPEN** | 五个原缺链来源现均有正文直接入口，Llama 3 也已进入 source_refs 并有相邻引用；这部分关闭。逐字扫描现为 34 处外链、17 个唯一 URL，24 处与本篇 source_refs 对应 registry 主 `url` 一致；仍有 10 处、6 个唯一 URL 非主入口，不能把“同登记条目”解释当作本轮精确映射完成，尤其新增 Adam 路径未登记。详见下文的分项区分。 |
| C07 | P2 | **CLOSED** | 正文 L44、L99、L141、L206、来源记录 L10/L45、registry L7020 条目的 revision/notes 已明确两版身份和附录映射。重新核对 [arXiv v1 附录 D](https://arxiv.org/html/2502.12340v1) 与 [ACL 正式 PDF](https://aclanthology.org/2025.acl-long.996.pdf)：正式版实验位于 §4、Fig.5，附录 D.1/D.2 为解释/低精度；预印本 D.1–D.4 的定位可对应。正式版附录 D 位于印刷页 20386–20389 / 文件第 15–18 页。registry 中 arXiv 分发许可明确限预印本，没有再作为两版等同的证据。 |
| C08 | P2 | **CLOSED** | 正文 L105、L193、来源记录 L10 与 registry notes 已同时保留多数非灾难性运行/六任务的范围及反例；[ACL Table 3、§6.2](https://aclanthology.org/2025.acl-long.996.pdf)（印刷页 20379 / 文件第 8 页）确有 Node 6 CosmosQA 精度 0、DP 100%，换 seed 对照 DP 6.70%。附录 E.5 全表也可定位。正文已不把一次种子对照作为 SDC 影响的统计上界。 |
| C09 | P3 | **OPEN** | 正文 L103 已将初始尖峰的利用率解释标为作者推测，L124 也已改成观察窗口而非周期；但 L124 仍直接断言“同步/监控本身降低……从而降低 SDC 发生频率”，没有保留原文的推测限定，正文该处也未明确 Node 14。来源记录/notes 的限定不能代替正文。见 [ACL §9](https://aclanthology.org/2025.acl-long.996.pdf)（印刷页 20381 / 文件第 10 页）与下文。 |
| C10 | P3 | **CLOSED** | 正文 L151 已改为整批与逐 batch 样本执行同一运算，并单列整张量/切片；重新打开 [PyTorch 2.6 Batched computations or slice computations](https://docs.pytorch.org/docs/2.6/notes/numerical_accuracy.html#batched-computations-or-slice-computations)，比较对象及不保证逐位一致的边界与原文相符。 |
| C11 | P3 | **CLOSED** | registry L7118 条目的 license、来源记录 L12/L49、正文 L172/L210 已补 docs 文档范围。固定 tag [license_notice.md L3–5](https://github.com/Ascend/msprobe/blob/tag_MindStudio_26.2.0.B110_001/docs/zh/legal/license_notice.md#L3-L5) 分列产品与文档，所指 [docs/LICENSE](https://github.com/Ascend/msprobe/blob/tag_MindStudio_26.2.0.B110_001/docs/LICENSE) 明示 Attribution 4.0 International。结论限 docs，未扩展到产品、代码或第三方素材。 |

## 未闭项的剩余差距

### C02：分母和时间终点尚未真正统一

- **位置**：正文 L84、L91–92；来源记录 L9/L40；registry `src.arxiv.sdc-detection-wild-2203.notes`（L7006 起）。
- **已满足**：不再宣称覆盖未知全部 SDC；正文也已明确 signature 发布速度不是同等检出时间。
- **剩余差距**：L84 称分母为“该方法实际检出的集合”，registry 也写“各方法实际检出的集合”。若各用自身集合作分母，93% 与 77% 就失去原文共同比较基准。上游 §6 限定所研究缺陷族和同一失败集合，§6.1–§6.3 给出 23%/70%/7% 的互补关系。L92 仍把共同检出比较和全 fleet 扫描都塞入左格，右格仅写新 signature 部署；加“两个不同终点”标签没有满足逐行可比条件。
- **继续关闭所需**：明确以该研究所观察、两方法合并的检出集合为共同基准，分别说明共同与独有部分；将同等检出时间比较、扫描/部署范围和未公开的对应值分开记录，不再让各列承担不同统计终点。同步纠正 notes 与作者修订自述。

### C03：新增类别仍缺完整的比较边界

- **位置**：正文 L128、L136–138；来源记录 L41。
- **剩余差距**：开头说未取得量化成本/覆盖率的格子保持 unknown，新增三行却直接给“极低成本”“中等”“成本最低”，没有声明比较基线、是否包含 dump/搬运/参考运行或下游评估成本，也没有标注这些成本未量化。元数据属性检查和全量 CRC 计算不能共用一个无条件成本等级。任务质量行只列低敏感/缺少 oracle 的漏检，没有说明正常随机性、数据分布变化或合法数值差异可能造成的误报边界；其列举对象也从已有 loss 监控跨到额外下游评估，不能统一宣称成本最低。
- **证据**：[assert_close](https://docs.pytorch.org/docs/2.6/testing.html#torch.testing.assert_close) 区分属性检查与数值比较；[OCP §5.4](https://www.opencompute.org/documents/sdc-in-ai-ocp-whitepaper-final-pdf) 说明非确定性可混淆故障检测。所核工具文档不提供正文新增的跨方法成本排序。
- **继续关闭所需**：为新增类别分别明确对象/oracle、覆盖、成本条件及未量化项、假阴性与误报条件；没有量化依据时明记 unknown。N01 的错误覆盖断言另行修正。无需编造测量数据或增加未经验证的命令。

### C05：版本名已补，字段与能力记录仍有空位

- **位置**：正文 L162–164；来源记录 L43。
- **剩余差距**：NVIDIA 行没有列出任何具体健康字段名称，仅转引整篇；`NVML/nvidia-smi` 没有单独版本/观察边界。主动诊断说“各插件……前提与判据”，却未列采信哪项判据，unknown 只覆盖 fleet 检出率。AMD 虽已给固定 tag 和 `-c`/`#wrong` 名称，但没有交代校验对象、启用/跳过时的解释与前提，也没有明确该 inventory 未核的硬件观测能力。发生率未知不能代替这些能力的逐项边界。
- **已核证据**：被转引的[设备健康篇“固定字段例子”](../../knowledge/01-hardware/health-evidence.md)确有字段；固定 [dcgm_fields.h L758–778](https://github.com/NVIDIA/DCGM/blob/b0ec3c624ea21e688b0d93cf9b214ae0eeb6fe52/dcgmlib/dcgm_fields.h#L758-L778) 可核 ECC volatile/aggregate totals。当前 [DCGM 显存插件](https://docs.nvidia.com/datacenter/dcgm/latest/user-guide/dcgm-diagnostics.html#gpu-memory-plugin) 的 `DCGM_FR_MEMORY_MISMATCH` 有独立含义，不能只以 corrected/DUE 概括。固定 [rccl-tests README L175](https://github.com/ROCm/rocm-systems/blob/therock-10.1/projects/rccl-tests/README.md#L175) 说明 `-c` 检查结果及大 GPU 规模下开销；[RCCL 主干 L74–82](../../knowledge/03-communication/rccl-runtime-and-verification.md)已有更具体的校验/未校验解释。
- **继续关闭所需**：在本文清单填入少量实际采用的字段或检查项、覆盖对象、支持前提和逐项 unknown，并指向主干的相应小节；保留固定源码与可变 latest 的区分。无需复制整篇跨域正文。

### C06：补链成功，但精确登记映射未闭合

正文 11 个 source_refs 现在均有对应正文外链，原五个缺链来源及 Llama 3 依赖已接通。重开支持页确认 npu-smi 目录与 `npusmi_0034` 深页关系、DCMI 的 HBM 限制、msprobe/FaultDiag 固定文件身份及 Llama 3 Table 5 的 SDC 归因行；没有把链接存在认作工具检测保证。

仍有以下 6 个唯一 URL、10 处引用不等于对应 registry 主 `url`：

| 正文坐标 | URL 对象 / 次数 | 本轮核对结果 |
|---|---|---|
| L99、L206 | arXiv `abs/2502.12340`，2 处 | 出现在 ACL 条目的许可 scope URL，正文也已说明版本映射；主来源入口仍是 ACL。C07 的文件身份问题已关闭，本轮逐字主入口映射条件仍未满足。 |
| L109、L209 | 固定 commit 的 `torch/optim/adam.py`，2 处 | 新增证据实际已打开且支持状态依赖，但完整 URL/文件路径未进入所引用 registry 条目；revision 只含同一个 commit 不能代替登记该文件。 |
| L136、L154 | PyTorch `testing.html#torch.testing.assert_close`，2 处 | notes 有页面名说明，未形成该完整 URL 的登记入口；正文加“同登记条目”未改变初审所列差距。 |
| L153 | PyTorch `notes/randomness.html`，1 处 | 同上；来源真实，差距是本轮要求的精确映射。 |
| L170、L210 | npu-smi `npusmi_0034.html`，2 处 | 深页支持内容已核，notes 有页号、正文有目录关系，但 registry 主 `url` 仍为 `npusmi_0007.html`，未按本轮要求完成多页入口整理。 |
| L210 | msprobe `docs/LICENSE`，1 处 | **已经与 license.scopes 的 URL 精确对应**，故不判许可未登记；仅计入非主 `url` 的机械统计，C11 已关闭。 |

继续关闭 C06 时应保留精确深页，为多页资料建立明确可逐字核对的来源入口/映射，并让 source_refs 覆盖新增实际证据；不应把链接退回目录页来换取字符串一致。机械统计与许可 scope 已有映射的差别如上，不将全部 10 处一概称为无来源。

### C09：观察窗口已修，因果语气仍未全部收缩

正文 L103 对初始化利用率的标注已合格；L124 的“超过 4000 个 optimizer step 的观察窗口内”也消除了固定发生间隔的含义。但该段开头仍写成同步/监控必然降低 SDC 发生频率。重读 ACL §9：作者先说利用率下降**可能**降低频率，再以 Node 14 两种同步下的不同观测提示这种解释，未独立控制利用率建立普遍因果关系。

继续关闭所需是把 L124 的观测明确绑定 Node 14，将利用率/发生频率解释保留为论文提示或可能机制；探针会改变触发条件的实践提醒可以保留。正文 L124 未被来源记录 L47 或 registry 的节点名自动补齐。

## 修订引入的新发现

### N01 · P2 · 元数据检查行把内容指纹也归为完全不触发数值错误

- **状态**：OPEN。
- **位置**：正文 L136，新增“元数据/结构校验”整行；来源记录 L41。
- **问题**：该行一并列 dtype/shape、CRC-32 等“结构与指纹检查”，随后统称“合法范围内的数值错误完全不触发”。纯结构/属性检查确实不检查值，但内容指纹比对能够发现保持 dtype/shape 与数值范围的内容变化；这与同一行引用的工具规则矛盾。校验前数据已错且参考也受污染，是另一类 oracle 盲区，不能推出内容指纹对一切合法范围内错误都不触发。
- **证据**：固定 [msprobe 比对文档 L448–452](https://github.com/Ascend/msprobe/blob/tag_MindStudio_26.2.0.B110_001/docs/zh/user_guide/accuracy_compare/pytorch_accuracy_compare_instruct.md#L448-L452) 将 CRC-32 不一致列为单独 error 条件，和 dtype/shape 不一致分别列出；[PyTorch assert_close](https://docs.pytorch.org/docs/2.6/testing.html#torch.testing.assert_close) 也区分属性检查与数值比较。
- **建议 / 关闭条件**：将结构属性与内容指纹的覆盖分别说明；前者缺少值检查，后者在可信参考与非碰撞条件下可发现内容差异，但不证明计算语义、也不能自动容纳合法浮点差异。删除“完全不触发”的跨方法全称判断，和相邻字节完整性/容差说明保持一致。方法比较完整性仍按 C03 复核，不重复计算为第二项同义发现。

## 校验、写入与验证边界

只读定向校验已确认 frontmatter 符合 `schemas/content.schema.json`，11 个 source_refs、9 个 related_ids、9 个 evidence_refs 均可解析，正文 20 处相对链接目标存在。稳定 ID、`draft`、`generic`、`source_checked` 未升级；这些结构检查不关闭语义问题。

系统默认 Python 的旧 jsonschema 不提供 Draft 2020-12，首次只读 schema 探测因此失败；改用项目 `.venv/bin/python` 后通过，未安装或修改依赖。临时副本首次校验因复制范围遗漏 `plans/`、`templates/` 和现有 `build/` 等链接目标产生伪缺链；补齐当前 tracked/untracked 文件与现有构建目录后重跑，不将准备副本产生的错误记作内容发现。

完整临时副本的 `make check`、`make build` **均退出 2**：唯一结构问题来自并发出现的 `docs/research/batch-30-t08-07-codex-recheck.md`，其绝对链接 `/Users/ywang2397/.agents/skills/kimi-webbridge/SKILL.md` 被校验器判为仓库外链接。构建因该结构错误未执行生成阶段；没有取得全库检查/构建通过的结果。该文件不在 T08-04 复核范围，未修改，也不计为本任务 N 编号发现。本报告本地链接单独检查通过。本仓库 `build/` 未写入；未运行 `make test`（未修改 `src/kb/`）。

本会话没有执行任何诊断、压力测试、训练、故障注入或来源中的操作命令。NPU SDC 发生率、真实检出覆盖/误报、硬件配套与恢复效果仍为 unknown。未重审兄弟篇、未核全库远程链接；兄弟篇仅用于本次要求的职责衔接和字段定位。

开始时工作区已有正文、来源记录、registry 的修订和五份未跟踪初审报告；它们不是本会话成果。交付时复算正文、来源记录、registry 的 SHA-256，均与元数据表一致；本报告的 11 行初审状态及本地链接单独检查通过。期间其他任务的复核报告亦有并发新增或变化，不计为本会话成果。本会话唯一仓库写入为本报告，不修改作者的自述或待修内容。

**结论：6/12 CLOSED；OPEN：C02、C03、C05、C06、C09、N01。T08-04 未通过，须修订后按上述剩余关闭条件定向复核；模型审阅不替代真实环境验证。**
