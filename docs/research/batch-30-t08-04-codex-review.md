# Batch 30 · T08-04 初审报告

## 会话元数据与结论

| 项目 | 记录 |
|---|---|
| 审阅角色 | 独立批次审阅者；本会话不承担正文编写或问题修订 |
| 实际执行模型 / 档位 | `gpt-6.1-sol / xhigh` |
| 模型核验方法 | 用环境中的 `CODEX_THREAD_ID`、`CODEX_SESSION_ID` 定位本会话 rollout，逐行解析 JSONL，读取最新 `turn_context` 的 `model`、`effort`、`cwd`，并与 `collaboration_mode.settings` 交叉核对；未以默认配置或其他会话代证 |
| 模型核验结果 | `model=gpt-6.1-sol`、`effort=xhigh`、`cwd=/Users/ywang2397/work/AI_reliability_knowledge_base`；两个环境会话 ID 与 `session_meta` 一致；嵌套设置也为同一模型和档位 |
| 模型核验坐标 | `/Users/ywang2397/.codex/sessions/2026/10/21/rollout-2026-10-21T20-49-27-01a15e82-6922-7d02-8c5d-9c587227a50e.jsonl` L8，时间戳 `2026-10-21T12:49:47.749Z` |
| 会话 ID | `01a15e82-6922-7d02-8c5d-9c587227a50e`；对应 `turn_id=01a15e82-6aa6-7c90-a637-feb3da815b7b` |
| 执行方式 | 当前本地 Codex CLI 会话直接审阅；`session_meta.originator=codex_exec`、CLI `0.163.0`；未另启审阅模型或子代理 |
| 日期 / 时区 | 2026-10-21 / Asia/Shanghai |
| 审阅正文 | `knowledge/08-reliability/silent-errors-and-integrity.md`，183 行（含 frontmatter） |
| 正文 SHA-256 | `e6dd1faa79fcda455fca1bc91292b00f0e41d9000e7e8778570f9f44aeb8c892`；使用 `shasum -a 256` 取得 |
| 写入范围 | 仅新增 `docs/research/batch-30-t08-04-codex-review.md`；不修改正文、取证记录、registry、导航、计划或构建产物 |

**初审结论：需修订并定向复核，暂不通过。共 11 项发现：P1 为 0 项，P2 为 8 项（C01–C08），P3 为 3 项（C09–C11）。** 所有发现均为开放状态。主要问题是检测与观测层混用、量化口径、两项方法覆盖缺口、平台版本清单及证据追溯；另有论文版本混用和实验结论概括过强。

优先级：P1＝足以严重误导处置的关键错误；P2＝影响技术准确性、证据边界或验收判据的必修事项；P3＝局部措辞、定位与可追溯性问题。下文“正文 L…”均以表中 SHA-256 为基准，其他文件另行标明。

## 范围与方法

已先读 `README.md`、`AGENTS.md`、`docs/authoring-guide.md`、`schemas/content.schema.json`，以及 `content-outline.md` 的 08 域与跨域分工。完整重读[审阅正文](../../knowledge/08-reliability/silent-errors-and-integrity.md)和[取证记录](batch-30-t08-04-sources.md)。以 [T08-04](../../plans/full-coverage-backlog.yaml) L6874–6920 中 **L6890–6894 五条 acceptance** 逐条验收，不以摘要或目录标题代替验收。

独立打开用户列出的全部精确上游 URL：两篇新论文均进入全文，2203.08989 核对 §1–§7、表 1；2502.12340 核对研究方法、三层实验、§7/§9 和附录 D，并对照 ACL 正式 PDF 的相应正文与附录。OCP 核对 §5.1、§5.2–§7，并回查定义与间歇触发边界。其余核对官方字段页、固定 tag/commit 的原 Markdown 和 PyTorch 2.6 页面；另沿实际主张打开 SuperBench PDF、Llama 3 Table 5、DCGM 诊断说明、固定 PyTorch Adam 源码及 RCCL tests README。

GitHub 资料通过连接器读取精确文件，行号按返回的原 Markdown/源码逐行计数，不使用网页转换行号。PDF 采用可检索原文与 HTML 交叉核对，坐标同时记录印刷页和文件页序；截图接口未取得可判读图像，不声称已完成图像核验。DCMI 精确页直接打开曾失败，后从同版本 `dcmi_006.html` 的接口链接成功进入**同一个** `dcmi_047.html` 并核对全文，未用 A3 或其他版本替代。终端外网读取因 DNS 失败未取得证据；未申请放宽网络权限。

兄弟篇只核对链接与职责边界：08 域首页、故障模型、证据与假设、相关故障案例、统一测试方法、可靠性指标，以及被正文链接的设备健康、节点验收、RCCL、GPU→NPU 精度诊断；为核实恢复衔接另读 checkpoint 状态一致性的有关段落，不对这些正文作完整重审。

## 已核实的主链与边界

| 对象 | 独立核对结论 | 边界 |
|---|---|---|
| CPU SDC 与针对性复现 | [2102.11245v1](https://arxiv.org/abs/2102.11245v1) §1、§5–§8 支持硬件报告缺口、干净日志案例、复现缩减与组合检测 | CPU 来源案例；不是本库事故，也不建立加速器发生率 |
| Fleetscanner / Ripple | [2203.08989v1 全文](https://arxiv.org/html/2203.08989v1) §4–§6、表 1 支持互补检出和不同运行成本；正文测试次数、fleet 秒数可对上原表 | 生命周期累计与月度统计分列正确；同等覆盖口径仍需 C02 修订 |
| 真实不健康节点研究 | [ACL 正式 PDF](https://aclanthology.org/2025.acl-long.996.pdf) §3–§7：15 台不健康节点、确定性对照、loss 可掩盖参数差异；WCNTS 最大 5.1% 可核对 | 单节点 TP 与论文设置；具体硬件组件未定位，不推断厂商/SKU |
| ABFT 反例 | 同一正式 PDF §4.2、附录 D.1–D.2 支持有限检出及直接采用低精度检查的误报观察 | 不能泛化成所有 ABFT 无效；解释中包含作者假设，版本坐标见 C07 |
| OCP 检测与恢复 | [白皮书](https://www.opencompute.org/documents/sdc-in-ai-ocp-whitepaper-final-pdf) §5.2–§7 是机制与开放问题讨论；checksum、冗余、回滚的概括主线有依据 | 不是 NPU 产品检测保证；checkpoint 必须有可信恢复状态，见 C04 |
| PyTorch 数值背景 | [数值精度](https://docs.pytorch.org/docs/2.6/notes/numerical_accuracy.html)、[可复现性](https://docs.pytorch.org/docs/2.6/notes/randomness.html)和 [assert_close](https://docs.pytorch.org/docs/2.6/testing.html#torch.testing.assert_close)支持跨平台非逐位契约与显式容差；正文默认容差数字正确 | 工具默认值不是任务验收阈值；batched 译法见 C10 |
| Ascend ECC | [npu-smi ECC](https://www.hiascend.com/doc_center/source/zh/HDK/2610/A2/A2npu/npusmi_0034.html)的当前/生命周期计数、预留单比特页字段、0–64 待隔离范围和计数上限可核；[DCMI ECC](https://www.hiascend.com/doc_center/source/zh/HDK/2610/A2/A2DCMI/dcmi_047.html)的 HBM 限制、重启清零及支持矩阵可核 | 已检测 ECC 证据；不建立 SDC 覆盖率；页面还支持部分非 root/容器场景，不能将正文的 root 示例读成排他矩阵 |
| msprobe / FaultDiag | [固定 tag 比对文档](https://github.com/Ascend/msprobe/blob/tag_MindStudio_26.2.0.B110_001/docs/zh/user_guide/accuracy_compare/pytorch_accuracy_compare_instruct.md)支持所列指标、规则和豁免；[固定 commit 诊断页](https://github.com/Ascend/mind-cluster/blob/44385c13d7b1d87def35f1604e8be4d16de6ca4e/docs/zh/faultdiag/ascend-faultdiag/05_usage/04_fault_diagnosis.md)支持报告结构和 `-p` 分支 | 比对异常、规则命中都不单独证明硬件根因；文档示例不是现场事故 |
| 性能域与 GPU 统计 | [SuperBench PDF](https://www.usenix.org/system/files/atc24-xiong.pdf) §2.2、§5.2 的性能退化/仿真边界与本文定位一致；[Llama 3 v3](https://arxiv.org/html/2407.21783v3) Table 5 中的 SDC 1.4% 是意外中断分类占比 | 后者不是 GPU 或 NPU 每设备 SDC 发生率；本篇缺该来源依赖，见 C06 |
| 注入与 unknown | 正文 L148–150 明确不以合成注入代替真实发生证据，NPU 发生率与检测保障保持 unknown；与 08.7 的交叉引用一致 | 有限检索未找到材料不等于证明平台不存在能力；本轮没有硬件实验 |

## 发现

### C01 · P2 · 将硬件未报告误算扩大成被动证据不可检出，并把主动校验也归入有信号错误

- **位置**：正文 L47、L61、L135、L162；对照 L57 的硬件检测定义。
- **问题**：L61 将“被动证据不覆盖 SDC”称为定义性事实，L135 又将包括 DCGM 主动诊断在内的工具统称为有信号错误检测。这里混淆了硬件原生信号、应用间接症状和新增结果校验；会使读者丢弃有价值的分析证据，也低估主动诊断的正确性检查。
- **证据**：[OCP](https://www.opencompute.org/documents/sdc-in-ai-ocp-whitepaper-final-pdf) §3.1（印刷/文件页 8）以未触发**硬件**检测定义 SDC；§5.1（页 16）另有基于应用异常与 kernel 例外行为的分析检测。[DCGM User Guide](https://docs.nvidia.com/datacenter/dcgm/latest/user-guide/dcgm-diagnostics.html#gpu-memory-plugin) 的 GPU Memory Plugin / Test Description 明列写入模式后回读校验与 mismatch 检出，不只监听 ECC/Xid。
- **建议修订**：明确静默相对于哪个检测层和时点；将“健康计数/日志不能排除”与“间接症状可形成候选”“主动结果校验可有限检出”分开。保留无通用覆盖率的边界。
- **关闭条件**：上述各处使用一致的观测层定义；不再将所有被动分析排除，也不将主动正确性校验全部等同于已有硬件告警。

### C02 · P2 · 量化表把同等检出覆盖与全 fleet 部署/扫描时间混在一行

- **位置**：正文 L74、L81–82；取证记录 L9；registry 的 `src.arxiv.sdc-detection-wild-2203.notes`。
- **问题**：L82 表头为“达到同等覆盖时间”，两格却分别写全 fleet 扫描与新 signature 扩大发布。它们不是同一个统计终点；“对该缺陷族的覆盖”也应明确为观察到的检出集合，而非对未知全部缺陷的真值召回率。L74 的“大部分缺陷”还把范围表述加强为多数。
- **证据**：[2203.08989v1](https://arxiv.org/html/2203.08989v1) 表 1、§6.1–§6.3 的等价检出终点是共同 70%，约 6 个月与 15 天；§5.2.2 的新 signature 扩展和 §6.1 的全 fleet 覆盖是另两项描述。§6 开头只限定一个缺陷族的较大子集。
- **建议修订**：拆开“同一检出集合的时间”和“部署/扫描覆盖”；写清 93%/77%/23%/7% 的观察分母，将“大部分”改为不暗示多数的范围说明，同步取证记录和 notes。
- **关闭条件**：每行两列的对象、分母、起止与终点可直接比较；不把检出并集当全部潜在 SDC，也不把 signature 发布当同等检出。

### C03 · P2 · 检测方法比较未覆盖 acceptance 明列的若干类别

- **位置**：正文 L103–119、L145；验收 L6891。
- **问题**：总表有 ABFT、checksum、复制/重算，却没有完整比较元数据检查、差分/不变量和任务质量检测。L145 的 CRC、shape/dtype 等是工具指标清单，没有对应这些方法的覆盖、成本、假阴性/误报与盲区；loss 盲区也尚未形成任务级方法的比较。字节保存正确与算子语义正确的区别不足。
- **证据**：验收逐项要求这些类别。[PyTorch assert_close](https://docs.pytorch.org/docs/2.6/testing.html#torch.testing.assert_close) 分开结构/属性检查与带容差的数值比较；[OCP](https://www.opencompute.org/documents/sdc-in-ai-ocp-whitepaper-final-pdf) §5.2.1 与 §6.2 也分别讨论数据完整性和模型正确性，不能由一行 checksum 代替全部。
- **建议修订**：在现有表中补齐方法行或明确的对应小表，说明各自 oracle/对象、能发现什么、遗漏什么、开销与误报条件；数据/元数据检查可以链接其主归属正文，仍需在此完成比较。
- **关闭条件**：验收列举的每类方法均有可定位的五方面比较；未取得量化成本或覆盖率的格子明确 unknown，不编造阈值或检出率。

### C04 · P2 · 三层实验摘要没有补齐 optimizer 状态、update 与可信恢复链

- **位置**：正文 L87–101、L117、L131、L172；验收 L6892。
- **问题**：正文总结 activation/gradient 与参数漂移，但未解释错误进入 optimizer 的持久状态、经 update 影响后续步骤、写入 checkpoint 后的恢复后果。L117 仅说回滚到已保存状态，未说明已保存状态也可能已污染。数据错误虽然在 L131 被列为候选，缺少输入/参考本身出错与计算产生错值的区分检查。
- **证据**：[固定 PyTorch 2.6 Adam 源码](https://github.com/pytorch/pytorch/blob/1eba9b3aa3c43f86f4a2c807ac8e12c4a7767340/torch/optim/adam.py#L280-L302) 给出梯度→一/二阶矩→参数更新的状态依赖；据此可推导只替换参数不等于清理全部状态。[OCP](https://www.opencompute.org/documents/sdc-in-ai-ocp-whitepaper-final-pdf) §5.3.1（页 21）要求回到此前正确状态，§6.3.2（页 26）讨论延迟发现导致更远回滚。前者状态传播是方法推导，不是本库实测。
- **建议修订**：补一条带对象和检查点的传播链，区分暂态 activation、梯度累积、optimizer state、参数 update 与 checkpoint；明确可信恢复点和恢复后状态/任务判据，并链接 06 域状态一致性、04 域文件完整性正文。说明数据身份和参考正确性要先核对。
- **关闭条件**：读者能判断单次错值何时可能跨 step 存续、为何重启或加载最新 checkpoint 不足，以及数据错、合法数值差异、软件错误与硬件 SDC 候选如何保持分支；不要求补写未经来源支持的恢复命令。

### C05 · P2 · 三平台清单没有交付按版本的字段和校验能力记录

- **位置**：正文 L133–146；验收 L6894。
- **问题**：Ascend 有版本和字段表，NVIDIA 只转引两篇正文，AMD 仅给 RCCL 入口；没有把三者的已核版本、支持字段、数据/算子校验范围及未核部分分别记录。无 SDC 发生率不等于无可登记的观测或校验字段。现有摘要声称“逐平台校验与证据清单”，交付强度高于实际内容。
- **证据**：被链接的设备健康篇区分固定 DCGM 源码与可变 latest；RCCL 篇 L75–79 已分开版本、`-c` 与 `#wrong` 语义。[RCCL tests 的固定 tag README](https://github.com/ROCm/rocm-systems/blob/therock-10.1/projects/rccl-tests/README.md) L3、L175 明列性能/正确性检查及校验开销，不能只用“发生率 unknown”代替该类能力记录。
- **建议修订**：保持跨域主归属，通过简表列出各平台采用的版本/观察日期、字段或校验项、覆盖对象、支持前提和 unknown，链接已有主干的具体小节；NVIDIA 不把 latest 与 v3.3.9 当同一冻结版本。
- **关闭条件**：三平台均可追溯到明确版本边界的字段与数据/算子检查记录；未核能力逐项保留 unknown，不能将工具功能转写成 fleet 检出保证。

### C06 · P2 · 正文来源链缺失，且外链未全部与登记入口逐字对齐

- **位置**：正文 L89、L128–129、L143–148、L154、L156、L181；frontmatter L8–18。
- **问题**：14 处外链中 11 处等于本篇对应 registry 的 `url`，3 处不等：L89 为 arXiv，而登记为 ACL；L128–129 是 PyTorch 另两页，登记入口为 numerical_accuracy。后两页已在 notes 中说明，不是伪造来源，但仍不满足本轮的逐字对齐要求。另有 **5 个 source_refs 无正文直接外链**：SuperBench、msprobe、npu-smi、DCMI、FaultDiag；尤其四条 Ascend 表行没有精确上游链接。L148/L154 使用 Llama 3 数字，但本篇未登记该来源依赖，也没有相邻引用。
- **证据**：逐字比对正文 Markdown URL 与 registry 的 `url`，8 个唯一外链可复算上述结果。已独立打开 [msprobe 精确页](https://github.com/Ascend/msprobe/blob/tag_MindStudio_26.2.0.B110_001/docs/zh/user_guide/accuracy_compare/pytorch_accuracy_compare_instruct.md)、[DCMI 精确页](https://www.hiascend.com/doc_center/source/zh/HDK/2610/A2/A2DCMI/dcmi_047.html)及 [Llama 3 全文](https://arxiv.org/html/2407.21783v3)的 Table 5，这些材料存在；问题是正文追溯链未接上。npu-smi 条目登记 `npusmi_0007.html`，支持 ECC 主张的实际页是 notes 所列 `npusmi_0034.html`，还需明确入口与支持页关系。
- **建议修订**：给实质主张补精确链接和章节/字段定位；由编写者整理多页来源登记，使正文采用的 URL 有明确、逐字可核的登记入口，保留准确深页，不能为了匹配退回目录页。补上已存在的 Llama 3 来源 ID，或删除无直接依据的数值；与 C07 一并处理 ACL 版本映射。
- **关闭条件**：逐条主张能从正文直接到支持页；所有外链完成本轮要求的 registry 精确映射；source_refs 覆盖实际采用的来源，五个缺链条目不再只靠来源表或取证记录间接定位。

### C07 · P2 · arXiv v1 与 ACL 正式版被当作同一修订，导致附录引用不可定位

- **位置**：正文 L40、L89、L115、L178；取证记录 L10；registry 的 `src.acl.sdc-llm-training-2502.revision/notes`。
- **问题**：正文和取证记录等同两版，却沿用 arXiv 的 D.1–D.4 定位指向 ACL。两版属于同一研究，但不是可互换的文件修订；这直接影响“全文并节级引用”的验收。
- **证据**：[arXiv v1 全文](https://arxiv.org/html/2502.12340v1) 的 D.1/D.2 为实验设置/结果、D.3/D.4 为失败解释/低精度；[ACL 正式 PDF](https://aclanthology.org/2025.acl-long.996.pdf) 将实验放在 §4，附录只留 D.1/D.2（解释/低精度，印刷页 20386–20389 / 文件页 15–18）。正式版没有 D.3/D.4。
- **建议修订**：选定主引用修订，并为另一版本单列映射；若用正式版，更新附录与图号；若保留 arXiv 定位，明确引用其 v1 全文。同步核对 notes 与许可适用对象，不再写两版相等。
- **关闭条件**：每处论文节号都能在其所链接的版本定位；正文、取证记录、registry 的文件身份与读取范围一致。

### C08 · P2 · “微调分歧率不大于换种子”没有排除表中明确反例

- **位置**：正文 L95；取证记录 L10 与对应 registry notes。
- **问题**：该句没有范围限定，与同一格保留的 Node 6 灾难性结果冲突。它可能被读成 SDC 对任务影响受正常随机性上界约束，而该实验不支持这种保证。上游概括段也有类似强表述，审阅应同时对照表值。
- **证据**：[ACL 正式 PDF](https://aclanthology.org/2025.acl-long.996.pdf) Table 3、§6.2（印刷页 20379 / 文件页 8）：CosmosQA 的 Node 6 分歧率为 100%，换 seed 的健康节点为 6.70%；作者随后专门讨论末期尖峰。
- **建议修订**：限定为多数所观测的非灾难性运行与特定任务设置，紧接着说明反例；不将一次换种子对照概括成所有正常随机性的统计上界。
- **关闭条件**：概括与 Table 3/E.5 的反例一致；不再暗示 SDC 影响必定小于随机种子变化，取证记录和 notes 同步收缩。

### C09 · P3 · 将 4000 步观察窗口写成发生间隔，并省略利用率解释的假设语气

- **位置**：正文 L93、L100、L155。
- **问题**：L100 的“每 4000 步才偶发”赋予了发生周期；L93 把初始化期间较高系统利用率作为已确定伴随条件。原研究给的是窗口内稀少事件与可能解释，没有测得固定间隔，也没有独立控制利用率完成因果识别。
- **证据**：[arXiv v1](https://arxiv.org/html/2502.12340v1) §4.2、§9；[ACL 正式 PDF](https://aclanthology.org/2025.acl-long.996.pdf) §9（印刷页 20381 / 文件页 10）讨论 Node 14 在超过 4000 个 optimizer steps 的窗口中很少出现 SDC，并以同步开销解释差异。
- **建议修订**：改为“在约/超过 4000 步的观察窗口内偶发”，注明 Node 14；将利用率相关机制标为作者推测或提示，保留探针可能改变负载与复现条件的实践边界。
- **关闭条件**：不再产生每 4000 步一次的周期含义；观察、解释和因果结论清楚分开。

### C10 · P3 · batched 与 non-batched 被误写成 batched 与逐元素

- **位置**：正文 L126。
- **问题**：“batched 与逐元素”容易被理解为批矩阵乘与 elementwise 运算的对照，改变了原文比较对象。
- **证据**：[PyTorch 2.6 Numerical accuracy](https://docs.pytorch.org/docs/2.6/notes/numerical_accuracy.html#batched-computations-or-slice-computations) 的该小节比较整批执行与按 batch 成员分别执行同一运算，以及整张量与切片执行。
- **建议修订**：使用“批量与逐个 batch 样本执行同一运算”，保留整张量/切片的独立说明。
- **关闭条件**：术语与原文计算对象一致，仍表达数学等价不保证逐位相同的边界。

### C11 · P3 · msprobe 的许可取证停在根目录，漏掉明确的文档许可

- **位置**：正文 L145、L181 所依赖的 `src.ascend.msprobe-26.2.0.b110.license`；取证记录 L12（正文未直接宣称许可证名称）。
- **问题**：registry 以根目录未见 LICENSE 将本篇使用的文档许可保留 unknown；该 tag 的 README 实际提供许可证声明入口。根目录探测不能替代文档目录的许可核对。
- **证据**：同一 tag 的 [license_notice.md](https://github.com/Ascend/msprobe/blob/tag_MindStudio_26.2.0.B110_001/docs/zh/legal/license_notice.md) L3–5 分别说明产品与 docs 文档许可；[docs/LICENSE](https://github.com/Ascend/msprobe/blob/tag_MindStudio_26.2.0.B110_001/docs/LICENSE) 明示 CC BY 4.0，产品的 `docs/zh/legal/LICENSE` 为另一许可对象。
- **建议修订**：补正文所用 Markdown 文档的许可范围与精确入口，同步取证记录；保留代码/产品/文档区别，不将文档许可扩展到制品或第三方素材。
- **关闭条件**：registry 的文档许可结论可沿固定 tag 原文件复核；不再仅以根 LICENSE 探测作为该文档许可 unknown 的依据。

## 五条 acceptance 的逐条判断

| 序号 / 要求 | 已覆盖 | 初审判断 |
|---|---|---|
| 1 · 全文与节级引用检测量化、LLM 训练研究 | 已有两篇全文层面的具体数据与方法，超出目录级分类 | **部分满足**：C02 的可比口径、C07 的修订身份及 C08/C09 的实验表述待修 |
| 2 · 各类检测方法的覆盖、成本、假阴性/误报与盲区 | checksum、ABFT、复制、重算与回滚主线已建立 | **未充分满足**：C03 缺少明确要求的方法比较；C01 的检测边界也需修正 |
| 3 · activation/gradient/optimizer/update 传播与恢复，区分错误来源 | activation/gradient 对照、loss 盲区与容差纪律已有 | **未充分满足**：C04 缺 optimizer 状态与可信恢复链；C10 为局部术语修正 |
| 4 · NPU 原始材料 inventory 与有限检索边界 | 已取得 ECC、msprobe、FaultDiag 原始文档；NPU 统计保持 unknown | **基本覆盖但证据链待修**：C06 的正文入口、C11 的许可取证需闭合；不能因 inventory 存在声明硬件验证 |
| 5 · 三平台按版本记录字段及算子/数据校验；注入不是发生证据 | Ascend 表和注入边界明确，未以 CPU/GPU 统计代填 NPU | **部分满足**：C05 的 NVIDIA/AMD 版本清单未交付；C01/C06 影响平台能力表述与追溯 |

## 元数据、registry 与导航核查

- **Frontmatter**：按已读 schema 使用本地 `jsonschema` 及日期格式检查，只读校验通过。稳定 ID、`concept/reliability/draft`、`platforms: [generic]`、`updated_at: "2026-10-21"` 合法；10 个 source_refs、6 个 related_ids、9 个 evidence_refs 均存在。标题与 H1 一致。`source_checked` 未被升级为 `reproduced`；结构通过不关闭上述语义发现。
- **内部引用**：正文 15 处相对链接目标均存在。08 域 `index.md` L11/L26/L43 登记本篇 ID、正文入口及 08.6 主题；与总目录归属一致。08.7 承担测试/注入方法，08.8 承担计量，06 域承担训练状态恢复，04 域承担文件/存储完整性；本轮未把兄弟篇的链接存在认作其审阅通过。C04 要求的是补齐本文的传播解释与跨域衔接，不要求复制其他篇正文。
- **逐 URL 审计**：14 处外链、8 个唯一 URL；11 处与登记 `url` 精确一致，3 处变体及 5 个缺少正文外链的来源见 C06。没有把 notes 已登记的 PyTorch 子页说成不存在的来源。

| source_refs 条目 | URL / revision / license / notes 的核对结果 |
|---|---|
| `src.arxiv.sdc-at-scale-v1` | v1 与 arXiv 分发许可对象可核；CPU 边界正确；原文干净日志案例不能扩大为 C01 的全称判断 |
| `src.arxiv.sdc-detection-wild-2203` | abs 页仅 v1，HTML 明示 CC BY-NC-ND 4.0；notes 的定量终点和范围按 C02 校正 |
| `src.acl.sdc-llm-training-2502` | ACL URL 可达；登记的 arXiv 分发许可只对应预印本，不能充当正式版相同修订的证明；版本/附录映射见 C07，结果概括见 C08/C09 |
| `src.ocp.sdc-in-ai-2025` | 当前 PDF 30 页，封面 2025-08-27、Version History 1.0 于 2025-08-26 发布，CC BY-SA 4.0 可核；notes 主体机制有据，保留综述/开放问题边界 |
| `src.usenix.superbench-atc24` | 登记论文入口及 PDF 可达；页码 835–850、开放访问/作者版权与通用再分发许可分开；性能与仿真范围合理，但正文缺链接 |
| `src.pytorch.numerical-verification-2.6` | 三个版本化页面内容可核；登记 BSD-3-Clause 限仓库文档，不扩展到网站资产；子页映射与措辞见 C06/C10 |
| `src.ascend.msprobe-26.2.0.b110` | 固定 tag 比对页、README 及 docs 许可均已打开；判据可核，文档许可 unknown 需按 C11 补正 |
| `src.huawei.hdk-26.1x-a2-npu-smi-2026-10-08` | 登记目录与 ECC 支持页均可达，2610/A2 边界与字段可核；许可保守保持 unknown，本报告不新增网页复制授权；深页映射见 C06 |
| `src.huawei.hdk-26.1x-a2-dcmi-ecc` | 精确页已成功核读，notes 的 HBM、计数清零、预留字段与支持场景有据；网页许可保持 unknown，正文缺直接链接 |
| `src.ascend.faultdiag-v26.1.1` | 精确 commit 文件可读；同 commit 根 LICENSE 为 Apache-2.0；规则诊断和示例边界合理，正文缺直接链接 |

本轮只登记许可文本的存在、对象与来源记录是否相符，不由此选定仓库总许可。未复制第三方全文、图表或软件包进仓库。

## 未决 / 超出本轮范围

1. NPU SDC 发生率、fleet 扫描、实际覆盖/误报及算力保障仍为 unknown；本轮逐项核验列明官方材料，不能穷尽所有未公开或其他版本材料。
2. 论文不健康节点的具体器件根因、维修归队后效果、扩展到多节点复杂并行的结果不由本轮补齐。作者的假设、建议和统计观察不能写成本库实验结论。
3. msprobe 文档同时存在千分位指标“仅作趋势”的说明与基于该比例的 error 规则；本轮确认两种文字均存在，不替上游消解其产品判定语义，也未运行实现。编写者描述时应保留“经验指标说明”与“自动标记规则”的区别。
4. Llama 3 Table 5 部分绝对计数与百分比的自洽性未在本轮裁定；只核该 SDC 行及中断分类分母，不将其转化成每设备发生率。SuperBench 也未复现实验或仿真。
5. 本轮未重审兄弟篇技术正确性、未核全库远程链接与所有锚点，未进行硬件、兼容性或软件实现测试；PDF 图像未完成独立视觉核验，结论限于所核文字、表值与文件结构。
6. `T08-04` 的计划状态仍为 `planned / needs_source_preparation`、`source_revision: null`。本轮只交付初审，未修改任务账本，也不以报告存在推导 Batch 30 已通过。

## 校验与写入声明

未运行正文或上游中的任何命令，未运行 `make check`、`make build`、`make test`，未改动构建产物。本轮执行的是独立审阅用的文件读取、行号/哈希、只读 schema/ID/URL/相对链接检查与上游取证；这些检查不等价于全库检查通过或真实环境验证。

审阅开始时 Git 工作区干净；本会话唯一仓库写入为新增本报告，交付检查确认正文行数与 SHA-256 保持上述值。期间另出现 `batch-30-t08-05-codex-review.md`、`batch-30-t08-06-codex-review.md`、`batch-30-t08-07-codex-review.md`、`batch-30-t08-08-codex-review.md` 四个未跟踪报告文件；本会话未创建、读取其正文或改动它们，不将并发变化计作本会话成果。未修改正文、取证记录、registry、导航或计划。

报告提出的修订由编写者承担，完成后需提供新正文 SHA-256 与变更证据，由同一审阅者按 C01–C11 关闭条件定向复核。**在此之前，T08-04 需修订并定向复核，不能声明通过；模型审阅不替代真实环境验证。**
