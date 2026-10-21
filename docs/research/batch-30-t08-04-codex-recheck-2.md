# Batch 30 · T08-04 第三轮定向复核报告

## 会话元数据

| 项目 | 记录 |
|---|---|
| 审阅角色 | 独立批次审阅者；仅核对第二轮修订后的未闭项及修订新引入的问题，不承担正文编写或修订 |
| 实际执行模型 / 档位 | `gpt-6.1-sol / xhigh` |
| 核验方法 | 读取 `CODEX_THREAD_ID`、`CODEX_SESSION_ID`，按本会话 ID 定位 rollout，逐行解析 JSONL，读取最新 `turn_context`；与同文件 `session_meta` 及 `collaboration_mode.settings` 交叉核对，未以默认配置或其他会话代证 |
| 核验结果 | 两个环境会话 ID 与 `session_meta.id` 一致；`turn_context.model=gpt-6.1-sol`、`effort=xhigh`、`cwd=/Users/ywang2397/work/AI_reliability_knowledge_base`；嵌套设置亦为 `model=gpt-6.1-sol`、`reasoning_effort=xhigh`，符合本次用户指定及写作指南 §7 |
| 核验坐标 | `/Users/ywang2397/.codex/sessions/2026/10/21/rollout-2026-10-21T21-38-26-01a15eaf-4095-7742-be25-471564ebca88.jsonl` L8，`ordinal=7`，时间戳 `2026-10-21T13:38:50.687Z` |
| 会话 / turn ID | `01a15eaf-4095-7742-be25-471564ebca88` / `01a15eaf-42ae-7890-86fd-2cf728c88e36` |
| 执行方式 | 当前本地 Codex CLI 直接复核；同 rollout L1：`originator=codex_exec`、`cli_version=0.163.0`、`source=exec`；未另启模型、子代理或 fallback 轮次，报告无 fallback 输出标记 |
| 日期 / 时区 | 2026-10-21 / Asia/Shanghai |
| 写入范围 | 仅新增本报告；不修改正文、来源记录、registry、其他报告、计划、导航及本仓库构建产物 |

下列行号均以本轮读取快照为准；SHA-256 按原文件字节计算。

| 对象 | 行数 | SHA-256 |
|---|---:|---|
| [初审报告](batch-30-t08-04-codex-review.md) | 184 | `8ddaa6b84f0567564dd63023fafed2085b440d82c05ce436dbed4cbb3de7e621` |
| [第一轮复核](batch-30-t08-04-codex-recheck.md) | 120 | `cb73d1ba36b818dc009989c54d13c6069431896c66bcdc63030ea3bb06b26433` |
| [修订后正文](../../knowledge/08-reliability/silent-errors-and-integrity.md) | 215 | `976da4781ab33e96a95c1a1b910612f27437acb4615cbc48f69256bd726d788a` |
| [来源与第二轮修订记录](batch-30-t08-04-sources.md) | 58 | `d9e2835fd8d6da7755b6b355889f9a0e5f4770603d4164850e69f31e832510c5` |
| [registry](../../sources/registry.yaml) | 7226 | `334b739bf47e5032bc702f87b3c23d53199dc6b8d6cd6181e35c30c37cda7536` |

## 范围与方法

先读 `README.md`、`AGENTS.md`、写作指南、总目录与元数据 schema。仅对照初审 C02、C03、C05、C06、C09 的原始关闭条件及第一轮复核的剩余差距，并复核 N01；第二轮修订自述（来源记录 L51–58）不是关闭证据。第一轮已关闭项不重开，也不重新执行整篇初审。

定向重开：2203.08989v1 表 1、§5.2.2、§6；ACL 正式 PDF §9（印刷页 20381 / 文件第 10 页）及 arXiv:2502.12340v1 对应段落；OCP §5.4（页码 22 / 文件第 22 页）；PyTorch 2.6 testing、randomness 与固定 Adam 源码；DCGM 固定字段原文件和当前 user-guide 显存插件；RCCL 固定 tag README；msprobe 固定 tag 的 CRC/属性判定段。另打开新登记的 arXiv v1 与 Llama 3 v3 精确入口、npu-smi ECC 深页，核对映射对象。固定 GitHub 行号依据连接器返回的原文件计数；PDF 结论依据可检索文字，不声称完成图像独立核验。未执行上游诊断或训练命令。

## 指定未闭项逐项状态

| 编号 | 优先级 | 状态 | 对照关闭条件的判断 |
|---|---|---|---|
| C02 | P2 | **OPEN** | 正文 L84、L91–94 已统一观察并集、共同 70% 终点，并把扫描/部署时间单列；但 registry L7019 的 notes 仍写“分母为各方法实际检出的集合”，与正文相反。来源记录 L53 声称 notes 已同步，实际未完成。原条件要求同步更正登记与修订自述，故不能关闭。 |
| C03 | P2 | **OPEN** | 正文 L138–140 已分列结构、指纹、差分/golden 的成本 unknown，L141 也补了任务质量误报边界及下游评估 unknown。但该行仍无条件把 loss/梯度范数监控称为“近零额外成本”，没有限定复用既有指标还是额外计算、同步和采集，仍未满足无成本依据时明确 unknown 的条件。表格错列另见 N11，不将它重复计作新的技术成本问题。 |
| C05 | P2 | **OPEN** | 正文 L165–166 已增加字段/判据、AMD 未核硬件观测 unknown、NVML 未单独冻结版本等说明；但 NVIDIA 所举字段名不在固定源码中（N10），支持前提仍泛称“各插件前提/判据见节点验收”，未定位所采信显存检查的具体前提或对应 unknown；AMD 仍只说可开关，没有给出关闭校验时结果应判未校验的解释。原清单关闭条件尚未完整满足。 |
| C06 | P2 | **OPEN** | npu-smi、PyTorch 两个子页已增加完整 URL 映射；但 Adam 的来源 ID 未进入正文 `source_refs`，新 arXiv v1 主入口亦未接入，Llama 3 固定 v3 与正文无版本 URL 不一致；新增 DCGM/RCCL 直接文件链接也没有对应的精确登记和依赖。见下表，不能以 registry 全库中存在相关研究或仓库条目代替本篇证据链。 |
| C09 | P3 | **CLOSED** | 正文 L105 保留初始化利用率解释为作者推测；L126 已明确 Node 14、超过 4000 步的观察窗口及两种同步的不同观察，并用“论文提示其可能”“未独立控制”限定解释。与 [ACL §9](https://aclanthology.org/2025.acl-long.996.pdf)（印刷页 20381 / 文件第 10 页）及 [arXiv v1 §9](https://arxiv.org/html/2502.12340v1#S9) 一致；没有再赋予固定发生周期或独立因果识别。 |
| N01 | P2 | **CLOSED** | 正文 L138–139 已拆分属性检查与内容指纹：前者不查值，后者在可信参考与无碰撞前提下可发现内容变化，且保留语义、浮点差异及参考污染边界。重新核对 [msprobe 原文件 L448–452](https://github.com/Ascend/msprobe/blob/tag_MindStudio_26.2.0.B110_001/docs/zh/user_guide/accuracy_compare/pytorch_accuracy_compare_instruct.md#L448-L452) 的分列判据，以及 [PyTorch 2.6 assert_close](https://docs.pytorch.org/docs/2.6/testing.html#torch.testing.assert_close) 的属性/数值区分，原错误全称判断已删除。 |

## 仍需关闭的具体差距

### C02：正文已改，登记分母未改

[2203.08989v1 表 1、§6.1–§6.3](https://arxiv.org/html/2203.08989v1#S6) 以该缺陷族研究所观察的失败集合比较共同与独有部分，不能各以自身检出集合作分母。正文现在采用共同基准，比例及时间终点的核心修订成立；“规模”行仍明确标出 lifetime 与 per-month，未将它们直接相除，本轮不新增对此的要求。

剩余仅是 registry `src.arxiv.sdc-detection-wild-2203.notes`（L7019）仍保留第一轮指出的“各方法实际检出的集合”。继续关闭需让该说明与正文共同比较基准一致，并使来源记录 L53 的完成声明符合实际文件。表格中的代价行脱落另按 N11 记录。

### C03：任务质量监控的成本条件还缺一层

正文已实质修正跨方法统一排序，也已说明任务指标的漏检、oracle 缺失与正常随机性等误报；这些部分满足。结构属性“开销很低”已限定为属性比对本身并标明未量化，不再按此前的全量指纹问题判错。

但 L141 的“loss/梯度范数监控（随负载持续、近零额外成本）”没有相同限定。“持续”描述执行时机，不说明指标已经由原训练计算并可直接复用。作为成本可能依赖实现的证据，固定 [PyTorch 2.6 clip_grad.py L82–99](https://github.com/pytorch/pytorch/blob/1eba9b3aa3c43f86f4a2c807ac8e12c4a7767340/torch/nn/utils/clip_grad.py#L82-L99) 的范数实现需要张量范数、汇集和再次归约；这不证明某种监控必然昂贵，但也不能据此断言任意梯度范数监控近零成本。[OCP §5.4](https://www.opencompute.org/documents/sdc-in-ai-ocp-whitepaper-final-pdf) 支持非确定性与开销边界，不提供该成本结论。

继续关闭需限定复用既有指标时的增量采集范围，将新增范数计算/同步/评估等未量化成本记为 unknown；无需补造测量数据。来源记录 L54 所称“各行分别声明”应与最终表述一致。

### C05：记录有增量，准确字段及支持前提仍需闭合

显存写入-回读与 `DCGM_FR_MEMORY_MISMATCH` 的内容可由 [DCGM GPU Memory Plugin](https://docs.nvidia.com/datacenter/dcgm/latest/user-guide/dcgm-diagnostics.html#gpu-memory-plugin) 的失败条件核对，且正文保留了 current user-guide 与固定 v3.3.9 的区别。这部分成立。但所举 ECC 宏名错误，见 N10；其余“前提见节点验收”仍未提供所选检查的明确条件或对应未核项。例如该页 `is_allowed` 依 GPU 配置决定是否允许测试、无对应配置时默认 false；主显存测试还须满足所配置的最小内存分配条件。这类执行/覆盖条件未在清单中记录或列为未核，整体覆盖率 unknown 不能代替它们。

AMD 的固定 [README L175](https://github.com/ROCm/rocm-systems/blob/therock-10.1/projects/rccl-tests/README.md#L175) 确实说明 `-c` 的检查迭代及大 GPU 规模下开销。[RCCL 主干“rccl-tests 计时/校验口径”](../../knowledge/03-communication/rccl-runtime-and-verification.md#rccl-tests-计时校验口径固定-tag-therock-101) 也明确 `-c 0` 的 `#wrong=N/A` 为未校验。本文尚未传达该开启/跳过解释；这里只要求补齐能力记录和具体小节指向，不要求执行命令或复制完整操作流程。

### C06：精确映射与本篇依赖尚未同时成立

正文共 36 处外链、19 个唯一 URL。按完整 URL 提取并逐字比对，22 处与本篇 source_refs 对应条目的主 `url` 相等；允许 notes 或许可 scope 中的明确完整 URL 后，30 处可精确映射至本篇依赖。仅对 GitHub `#L…` 定位片段按同一文件处理；不把 arXiv 无版本 URL 当成固定版本，也不以字符串前缀命中充当精确映射。

| 正文位置 | 第二轮修订后核对结果 | 继续关闭所需 |
|---|---|---|
| L138、L156–157、L173、L213 | testing/randomness 与 ECC 深页完整 URL 现已进入对应 notes；docs/LICENSE 仍有许可 scope 精确映射 | 这部分关闭，不要求为机械统计退回主页 |
| L101、L209 | 链接仍为 `abs/2502.12340`；ACL 许可 scope 原已有这一完整 URL，新条目 L7213–7226 的主入口却是 `abs/2502.12340v1`，且 `src.arxiv.sdc-llm-training-2502-v1` 未进入本篇 source_refs | 接通明确采用的 v1 文件入口与依赖；不把已有许可映射误称为完全未登记，也不把新增孤立条目视作正文已接通 |
| L111、L212 | Adam 文件完整 URL 已在 `src.pytorch.parallel-training-state-2.6.notes`（L473）登记；但该 ID 不在正文 11 个 source_refs 中 | 补齐本篇对该实际源码证据的依赖 |
| L165 | 新增固定 `dcgm_fields.h` 文件链接；`src.nvidia.dcgm-v3.3.9` 主入口为仓库树，未登记该完整文件 URL，正文也未依赖该 ID | 精确文件映射与本篇依赖一起补齐 |
| L166 | 新增 rccl-tests README 固定 tag 文件链接；全 registry 未找到这一完整文件 URL，本篇亦无对应来源依赖 | 登记所用文件并接通依赖，不能只依赖 RCCL 主干的间接链接 |
| L178、L210 | 正文是 `abs/2407.21783`，registry L7036 已改为 `abs/2407.21783v3`；无版本 URL 未在该条目其他位置精确登记 | 正文与所采信 v3 入口保持一致，或建立明确的完整 URL 映射 |

尚无本篇精确依赖映射的是 Adam 2 处、DCGM 1 处、RCCL 1 处、Llama 3 2 处，共 6 处、4 个唯一 URL；arXiv v1 的新主入口接入问题另如表中所述。上述来源的真实内容与来源登记完整性分开判断，本轮没有将它们判为伪造材料。五个原缺链条目的直接入口仍在，没有退回仅来源表可达的状态。

## 第二轮修订引入的新发现

### N10 · P2 · NVIDIA 清单举出了固定源码中不存在的 ECC 字段名

- **状态 / 位置**：OPEN；正文 L165，第二轮为 C05 新补的字段例子。
- **问题**：该行以代码形式举 `DCGM_FI_DEV_ECC_SB_ERROR` / `_DB_ERROR` 为固定 v3.3.9 字段，却无法在所链接的 `dcgm_fields.h` 定位。这会使读者按清单查字段时得到不存在的名称，不能用“类字段”替代真实宏名。
- **证据**：重新读取固定 commit 的完整 2222 行头文件，两种所举全名均不存在。[原文件 L758–778](https://github.com/NVIDIA/DCGM/blob/b0ec3c624ea21e688b0d93cf9b214ae0eeb6fe52/dcgmlib/dcgm_fields.h#L758-L778) 的实际宏为 `DCGM_FI_DEV_ECC_SBE_VOL_TOTAL`（L761，310）、`DCGM_FI_DEV_ECC_DBE_VOL_TOTAL`（L766，311）、`DCGM_FI_DEV_ECC_SBE_AGG_TOTAL`（L772，312）、`DCGM_FI_DEV_ECC_DBE_AGG_TOTAL`（L778，313）。
- **关闭条件**：采用实际存在且与 volatile/aggregate 语义对应的字段名，或删除错误的代码例子并保留可核对的准确字段记录。此为修订新增的具体错误；C05 同时仍有原支持前提差距，N10 不另计作第二个同义清单缺失。

### N11 · P3 · 时间拆表和任务质量行改写破坏了表格结构

- **状态 / 位置**：OPEN；正文 L94–95、L132–145（具体 L141）。
- **问题与证据**：L94 插入普通段落后，L95 的“代价”管道行已经离开 L86–92 的三列表格，成为无表头/分隔行的文本，失去两策略的列关系。方法表表头为四列，L141 只有三个单元格：监控/评估的成本写进“机制与来源”，误报与盲区落在“覆盖与成本”，最后一列为空。这是本次拆时间量及重写任务质量行引入的局部结构问题，可由原 Markdown 直接复核，不涉及新增硬件验证要求。
- **关闭条件**：恢复代价信息与两策略的明确对应，并让任务质量行与四列表头对齐；保持已经收缩的分母、时间终点、误报和成本 unknown，不需要改写其他方法。

## 结构检查、写入与验证边界

正文 frontmatter 按 `schemas/content.schema.json` 只读检查通过；11 个 source_refs、9 个 related_ids、9 个 evidence_refs 均可解析，正文与本报告的相对链接目标检查通过。ID 存在不证明遗漏依赖已经补齐，也不关闭 C06。

为遵守仅新增报告的限制，将当前 tracked/untracked 文件及已有 `build/` 文件复制至 `/private/tmp/batch30-t0804-recheck2-c0qxn_gn`，使用项目既有 Python 环境分别执行 `make check`、`make build`，**均退出 0**：126 content entries / 575 sources；构建在该临时副本生成 catalog。原仓库 `build/` 未写入，未安装或修改依赖。该结果只覆盖结构与本地链接，不覆盖技术正确性、远程链接或硬件能力；亦不检查 N11 的表格列结构。

本轮只新增本报告。开始时已有正文、来源、registry 的未提交修订与其他批次审阅报告，不回退、不改动，也不计作本会话成果。交付期间对 661 个既有源文件/构建文件的哈希清单复比，未发现内容变化或删除；另并发出现 T08-05、T08-07、T08-08 的 `codex-recheck-2.md` 报告，不是本会话写入。没有改动 `src/kb/`，不运行 `make test`；没有执行设备诊断、压力测试、故障注入、训练或生产动作。`draft / generic / source_checked` 不因模型复核升级为硬件验证。

## 结论

**指定未闭项 2/6 CLOSED：C09、N01；OPEN：C02、C03、C05、C06。新增 N10（P2）、N11（P3），均 OPEN。本轮连同新增项计 2/8 CLOSED，T08-04 仍需作者修订后定向复核，暂不通过；模型审阅不替代真实环境验证。**
