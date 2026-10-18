# Batch 24 · T06-02 Codex 定向复核第三轮报告

- 复核日期：2026-10-19（Asia/Shanghai）。
- 结论：**暂不通过**。
- 第二轮遗留的四项：**CLOSED 3 项、OPEN 1 项**。C06、C08、R01 关闭；C07（P2）仍开放。
- 本轮新增：**P1 0 项、P2 1 项、P3 2 项，均 OPEN**；按本轮用户指定格式使用 `B24-B24-T062-S3-xx`，不擅自删除重复的 `B24-` 前缀。
- 合并全部历史与本轮发现：**CLOSED 9 项、OPEN 4 项**；OPEN 为 P1 0、P2 2、P3 2。
- 执行边界：只审阅，只新增本报告；不修改正文、作者取证、来源登记、导航、任务计划或工作树构建产物；不运行上游测试或 GPU/NPU 工作负载。
- 执行者为本会话 Codex CLI；未派发子代理。实际后端模型、推理档位及路由元数据未提供可独立核验的记录，记为 `unknown`，不声称已验证为约定模型，也不虚构另一次 CLI/模型执行。

## 1. 范围、基线与判定口径

先读取 `README.md`、`docs/authoring-guide.md`、`content-outline.md` 与 `schemas/content.schema.json`，以[第二轮报告](batch-24-t06-02-codex-recheck-2.md)规定的关闭条件为准，定向检查[当前正文](../../knowledge/06-training/framework-execution.md)和[作者取证](batch-24-t06-02-sources.md)末尾“修订轮三补充”（L139–144）。第一轮报告仅用于追溯 R01 原义；初审已关闭项仅作关联回归抽查，不重做全量初审。

不能以作者补充中的“同步”代替实际落点；也不能因出现新缺陷，就把已经完成的旧关闭条件重新记为未完成。故 C06/R01 的原问题与第三轮新增的错误测试限定名、重编译判读和引用错位分别计数。

本轮正文为 141 行。以下行号来自本轮实际读取的原文件，不沿用旧稿坐标。

| 输入 | SHA-256 |
|---|---|
| `knowledge/06-training/framework-execution.md` | `e635b30311e1d9bfd348700413d52f59ba91d6c4d9dcf76f4c77a75776d14262` |
| `docs/research/batch-24-t06-02-sources.md` | `ad469e89b576861f43896ea0b76a05e2ae660c61ba3aa8cfe2404d74146a58d4` |
| `docs/research/batch-24-t06-02-codex-recheck-2.md` | `d238e51106c95c6880182cf852a9b7f12c90e666923788c6d53c59fbba4e0822` |
| `sources/registry.yaml` | `3ea07202e7e0573c8ff8089bc5fcdd142b5a51269dc1f646a9d4a08d065215a2` |
| `plans/full-coverage-backlog.yaml` | `53bfc8fe47d56ab322e546c853858cbaa90cf5a5d0305b33a80bab0f39275d54` |

验收依据为任务表 L5880–5900 的 objective 和五条 acceptance。正文仍为 `draft / source_checked`；本轮通过与否均只指文档技术审阅，不代表模型、平台或硬件验证。

## 2. 独立重开证据

本轮通过只读 HTTPS 重新取回下列精确文件/版本化页面，查看实际断言、分支及上下文；没有 import 或执行这些文件。源码使用前轮已核定的 commit，重新取得的六个源码文件均与第二轮记录的 SHA-256 相同。本轮未另外声称重新解析了 tag 指向。

| 证据 | 精确位置与本轮用途 |
|---|---|
| E01 | PyTorch [test_optim.py](https://github.com/pytorch/pytorch/blob/1eba9b3aa3c43f86f4a2c807ac8e12c4a7767340/test/test_optim.py#L1349)：L1349–1439、L1646–1717。核对 optimizer 状态装载、后继更新、参数组与 CUDA 限定。 |
| E02 | PyTorch [test_autograd.py](https://github.com/pytorch/pytorch/blob/1eba9b3aa3c43f86f4a2c807ac8e12c4a7767340/test/test_autograd.py#L902)：L902–942、L1608–1611、L2263–2280。核对梯度/错误断言，不把它们当作恢复或保图时序测试。 |
| E03 | PyTorch [test/dynamo/test_compile.py](https://github.com/pytorch/pytorch/blob/1eba9b3aa3c43f86f4a2c807ac8e12c4a7767340/test/dynamo/test_compile.py#L24)：L24–32、L149–173。核对编译计数和 API 签名测试，特别检查类与方法的实际归属。 |
| E04 | MindSpeed-LLM [arguments.py](https://github.com/Ascend/MindSpeed-LLM/blob/53f3639c3da9c000a187c44cc0c08d55026ddded/mindspeed_llm/training/arguments.py#L242)：L242–282、L301–314。核对 CP 调用分支、GQA 进入条件、两次正商及 kv-repeat 绕过层级。 |
| E05 | PyTorch [autograd/__init__.py](https://github.com/pytorch/pytorch/blob/1eba9b3aa3c43f86f4a2c807ac8e12c4a7767340/torch/autograd/__init__.py#L294) L294–299、L339–350；[saved_variable.cpp](https://github.com/pytorch/pytorch/blob/1eba9b3aa3c43f86f4a2c807ac8e12c4a7767340/torch/csrc/autograd/saved_variable.cpp#L110) L110–131、L280–285；[Autograd mechanics](https://docs.pytorch.org/docs/2.6/notes/autograd.html#graph-retaining)。核对保存中间量的释放与先前调用保留的时序。 |
| E06 | PyTorch 2.6 [Troubleshooting](https://docs.pytorch.org/docs/2.6/torch.compiler_troubleshooting.html)：本轮原 HTML 的 Guards L738–744、Recompilation L768–788、Dynamic Shapes L790 起、[Where to apply](https://docs.pytorch.org/docs/2.6/torch.compiler_troubleshooting.html#where-to-apply-torch-compile) L901–948、[Wrapping constants with tensors](https://docs.pytorch.org/docs/2.6/torch.compiler_troubleshooting.html#wrapping-constants-with-tensors) L1212–1274。核对编译放置、合法重编译与 optimizer/scheduler 示例的真正出处。 |
| E07 | PyTorch 2.6 [torch.compile API](https://docs.pytorch.org/docs/2.6/generated/torch.compile.html#torch.compile)：本轮原 HTML L588–614、L657–660。核对模型编译仍受 guard/动态形状约束，以及本页实际示例范围。 |

| 取回对象 | 本轮 SHA-256 |
|---|---|
| E01 `test_optim.py` | `76cf0c7a0a79eb070bbd3fea508b083156dcbaefa68d38914e332c34a4177593` |
| E02 `test_autograd.py` | `a8daf1cb687dad29cc1633c222465a9faecdf2073e137195a32d6d795db033c1` |
| E03 `test_compile.py` | `36745171714b59a3ac313ac9b8a80e5423fd95f7abb538933e6731cdbd074d3d` |
| E04 `arguments.py` | `fd64204269ad1749159d9b98f47c91f92cb17de5075cb92670f8ab1d5df42a38` |
| E05 `autograd/__init__.py` | `98f86d295e386f647ad234ec63e36cb4b5d6acc3df696546c03bd62bf67a7503` |
| E05 `saved_variable.cpp` | `58c67f6b05a3ebe04dcf24318ed700401aeb7efbf7ba12589eb848603212eb84` |
| E05 Autograd mechanics HTML | `7bb9841dfcc78c106e375d3c5ad48ae7daf869ed49acd6314d4d16445ecc01e7` |
| E06 Troubleshooting HTML | `e755310a16da1153a2557588c313437459b2f78c1830f082b3ad299b945ca1b7` |
| E07 torch.compile API HTML | `bf53efd2b42f2bac3ccdb728cef2c5531ae385b46758ec1fe583746d94f1b417` |

版本化网页并非不可变字节快照；本轮 HTML 哈希/部分行号与历史记录不同，不能宣称匹配历史 HTML。本报告采用本轮实际读取的章节与行号；源码锚点则使用固定 commit 的原文件行号。

访问限制：网页阅读器不能取得上述部分源码页及两个编译文档页；随后系统 `curl --fail --location` 在正常证书校验下全部成功，未跳过证书校验。没有把阅读器失败当作页面不存在，也没有仅凭搜索摘要作判定。临时证据均放在仓库外 `/private/tmp/b24-t062-s3.8ggz2n`，不作为仓库永久附件。

## 3. 第二轮 OPEN 项逐项判定

### B24-T062-C06 · 原 P2 → CLOSED

**位置**：正文 L119–121、L128；作者取证 L141；registry L6122–6135。

第二轮关闭条件是至少交付一组代表性 PyTorch 测试的具名函数、具体断言、适用条件与不覆盖范围，并同步覆盖现状，不要求全量映射或运行上游测试。

1. L119 已说明 `test_state_dict_deterministic` 的克隆参数、装载 optimizer 状态后继续更新及参数/状态/参数组比较，并明确不证明完整应用 checkpoint/RNG 恢复。相邻 CUDA 测试标出 `onlyCUDA`，说明输入 state 不被装载修改、状态设备及后继更新检查。E01 支持这些核心摘要；设备/配置仍以各测试装饰器和测试体为准，不扩展成跨平台兼容证明。
2. L120 已把解析梯度与 `requires_grad=False` 的报错分别归到具名测试；E02 支持。它们没有被用来替代 C08 的保图时序证据。
3. L128 已改成代表性映射完成、完整训练循环/分布式端到端及 MindSpeed 测试面仍有缺口；不再与新增测试引用自相矛盾。L91 对更大测试面“未逐项映射”的限制可以保留。

因此原“只列名称、没有断言/适用与覆盖状态未同步”的最低关闭条件已经满足，关闭 C06。**但 L121 新增的限定名把 `test_compilation` 放到了错误类中**，另记本轮 P3 `B24-B24-T062-S3-02`；这不等于认可每个新定位都准确，也不把它重复记作旧 C06。

### B24-T062-C07 · 原 P2 / OPEN

**位置**：作者取证 L37、L121、L142；registry L6024；正文 L126 对参数校验入口的引用。

**已修复部分**：

- 取证 L37 与 registry L6024 已明确限定 Ulysses/Mamba/hybrid CP 分支及 `use_mcore_models`，不是所有 CP 算法的无条件头数规则。
- 三处实际摘要均已写出 GQA 开启且查询组数至少为 1 的进入条件、先除 TP 再除 Ulysses、两次商至少为 1，以及 kv-repeat 只绕过第二层。原串联除法算术错误和此前遗漏的正商已修复，不继续称其未修。
- E04 确认辅助检查：L247–257 包含头数及两层 GQA 谓词；L265–277 处理 CP 未启用和 Mcore 前提；L279–282 与 L301–314 分别在所述算法分支调用，不在 `megatron_cp_algo` 分支无条件调用。

**剩余原关闭条件**：取证 L121 的建议登记 `notes` 副本仍直接写 `_validate_cp_args（num_attention_heads 须能被 ulysses_size×TP 整除且商 ≥1；GQA 分支……）`，未加入 L37/registry 已补的 CP 算法调用范围与 Mcore 前提，也没有明确引用 L37 的完整谓词。L142 声称“取证/registry 摘要补进入条件”，不能替代这份实际副本。

第二轮明确要求 L37、L121、registry L6024 三处同步，或让副本明确引用完整谓词。本轮仅前两类实际位置中的 L37 和 registry 完成，L121 仍留下把辅助检查泛化为 `_validate_cp_args` 整体规则的歧义，因此保留 **OPEN/P2**，不降级、不另起新编号。

**关闭条件**：为取证 L121 补齐与 L37/registry 一致的调用范围和前提，或明确指向 L37 的完整条件；保持已正确的 GQA 进入条件、串联正商和开关层级。无需新增源码、扩展未读协议或运行任何配置。

### B24-T062-C08 · 原 P3 → CLOSED

**位置**：正文 L67、L120；作者取证 L34、L93、L143。

正文 L120 现在明确指向 L67 的完整定义，并保留“同图再次求导且需其中间量、在先前会释放它们的 backward 中保留”的限定。作者取证 L34 也实际补齐条件和时序，不再仅说“二次 backward 需 retain_graph”；L93 已有的常规新 forward 边界仍保留。

E05 的 API 与 saved-variable 路径支持先保留、已释放后不能追溯恢复的解释。正文没有把所有同图二次反向都写成必须保图，也没有要求新 forward 的每轮迭代保图。因此关闭 C08；不将这一语义核对当作本地复现或训练恢复证明。

### B24-T062-R01 · 原 P2 → CLOSED

**位置**：正文 L75、L82–83、L85；作者取证 L144。

本轮 L75 已为表格明确选择“仅 `compile(model)`”，外层训练驱动与 optimizer/scaler/scheduler 保持 eager；含 optimizer 的编译范围被明确列为另一种、不在本表范围内的放置方式。L83 也把状态推进表述收紧为逻辑契约，而非未选定范围时一概说其与编译无关。E06 的 Where to apply 与 LR 示例支持区分两种放置方式；L85 的数值对照及平台支持未知仍保留。

这已完成 R01 原先要求的作用域选择和逻辑/编译层次区分，故关闭 R01；不要求另做完整 step 变体，也不承诺 DDP/FSDP 任意包装都受支持。第三轮同时引入的“样板下无重编译预期，出现即异常”及错误示例链接，分别以新项 S3-01/S3-03 记录，不能因原 R01 关闭而放行。

## 4. 本轮新发现

### B24-B24-T062-S3-01 · P2 / OPEN：仅编译模型不意味着出现重编译即异常

- **位置**：正文 L82 的观测挂点“hook 时间线；样板下无重编译预期，出现即异常”；关联 L75。
- **问题**：L75 只限制编译范围，没有固定输入形状、dtype、设备或其他模型 guard 条件。optimizer/scheduler 和分布式 hook 留在 eager，不会消除模型编译区域自身的 guards。L82 却把该样板下出现重编译直接升级为异常，遗漏正常特化和动态形状行为。
- **证据**：E07 API 原 HTML L590–599 明确允许同一 frame 因 guard 不适用而产生多个编译结果，L608–614 说明默认动态形状发现可经重编译推进。E06 的 [Recompilation](https://docs.pytorch.org/docs/2.6/torch.compiler_troubleshooting.html#recompilation) 给出形状变化导致 guard 失配的例子；这不要求把 optimizer 纳入编译。
- **影响**：本页的训练执行路径观测可能把合法的模型重编译误判为 hook 或训练异常，直接影响验收第 1 条。若作者意图仅指“未追踪的 eager hook 本身没有对应编译 frame”，必须明确这一观测范围，不能写成整个样板的零重编译保证。
- **关闭条件**：区分 eager hook 与模型编译 frame；按实际 guard 原因、形状/类型等变化和事先约定的稳定输入/预热条件判断重编译，不使用“出现即异常”。可以提出稳定基线下异常频度的检查，但不能虚构已建立该基线或已经运行验证。
- **与旧项关系**：R01 是“未选择编译放置就泛化 optimizer/scheduler 边界”；本项是选择范围后新加的错误重编译判据，根因和修正落点不同，单独计数。

### B24-B24-T062-S3-02 · P3 / OPEN：编译测试限定名指向不存在的类方法

- **位置**：正文 L121 的 `PublicTorchCompilerTests.test_compilation`。
- **证据**：E03 L24–32 的实际归属是 **`InPlaceCompilationTests.test_compilation`**，使用 `ToyModel`、`model.compile(backend=CompileCounter)`，调用一次后断言 frame 数为 1；`PublicTorchCompilerTests` 在 L149 才开始，其 L163–173 是 `test_dynamo_signatures`。
- **影响**：给出的行范围可找到断言，但按限定名检索/选择测试会找不到目标，破坏源码—测试定位精度。这个单次调用断言也不能外推为任意训练样板长期零重编译。
- **关闭条件**：纠正类限定名，分别对应模型原地编译计数测试与公共 API 签名测试，并保留不覆盖完整训练 step、数值与 optimizer/scheduler 的限制；无需执行测试。
- **与旧项关系**：这是第三轮补具名映射时新引入的错误，不恢复“没有任何代表性测试断言/适用条件”的旧 C06。

### B24-B24-T062-S3-03 · P3 / OPEN：含 optimizer/scheduler 的编译示例链接不支持所指示例

- **位置**：正文 L75，将含 optimizer 的训练可调用对象及 optimizer frame guard 失配指向 `generated/torch.compile.html` 的“相关示例”。
- **证据**：E07 的 Example（原 HTML L657–660）是三角函数张量表达式，没有 optimizer/scheduler。真正支持该段具体示例的是 E06 的 [Where to apply torch.compile](https://docs.pytorch.org/docs/2.6/torch.compiler_troubleshooting.html#where-to-apply-torch-compile) 和 [Wrapping constants with tensors](https://docs.pytorch.org/docs/2.6/torch.compiler_troubleshooting.html#wrapping-constants-with-tensors)；后者本轮原 HTML L1242–1274 包含 optimizer、scheduler 与学习率 guard 失配。
- **影响**：概念可以由正确上游支持，但读者沿当前近邻链接无法复核所称示例。它是新增引用错位，不是认定“含 optimizer 的训练调用不能编译”。
- **关闭条件**：把相关断言的近邻引用改到上述精确章节；API 链接可继续支持 callable/guard 等 API 契约，但不要声称其中展示了该训练示例。

## 5. 已 CLOSED 项关联回归抽查与计数

| 历史项 | 本轮抽查 | 判定 |
|---|---|---|
| C01 / P2 | 正文 L92 保留 dataclass→参数工厂→CLI 生成链及未执行解析的限制；本轮不再增加否定 CLI 存在的断言。 | 维持 CLOSED |
| C02 / P2 | L75–85 的分阶段表、作用域与“编译不等于数值正确”仍在；原结构性缺失未回归。新增错误判据归 S3-01，不重复计数。 | 维持 CLOSED |
| C03 / P2 | L89–95 三组资料档案仍隔离，测试摘要没有被拼成三平台可运行配套。 | 维持 CLOSED |
| C04 / P2 | L97 保留 HIP 差异、正确版本化 distributed 链接、AMD 7.1.1 独立版本线及不得直接迁移的边界；未改部分不重做全量联网审计。 | 维持 CLOSED |
| C05 / P2 | L109–113 的连通性/恢复分离、完整 optimizer step 截点、截点 RNG 状态、后继输入与事先约定比较规则仍在；关联并行页的截取边界/合法跳步两节仍可定位。 | 维持 CLOSED |
| C09 / P3 | L134 继续为 optimizer state_dict“不能默认互换”，没有恢复绝对不兼容判断，也未把同版 PyTorch 测试当作跨框架互转证明。 | 维持 CLOSED |

| 计数范围 | CLOSED | OPEN | OPEN 组成 |
|---|---:|---:|---|
| 第二轮遗留 C06/C07/C08/R01 | 3 | 1 | C07：P2 |
| 初审 C01–C09 累计 | 8 | 1 | C07：P2 |
| 第一轮新增 R01 | 1 | 0 | 无 |
| 第二轮新增 S2 | 0 | 0 | 无 |
| 本轮新增 S3 | 0 | 3 | S3-01：P2；S3-02/S3-03：P3 |
| 全部历史及本轮发现合计 | **9** | **4** | **P1 0、P2 2、P3 2** |

## 6. 任务验收重新核对

| T06-02 验收条目 | 本轮结果 | 判定 |
|---|---|---|
| 1. eager/compiled step 路径、数据/控制流与观测，不把编译成功当数值正确 | R01 作用域已修；阶段表与数值边界保留。但 L82 新增错误重编译判据（S3-01/P2），L75 还有示例引用错位（S3-03/P3）。 | **暂不通过** |
| 2. PyTorch、NVIDIA、Ascend 三组独立资料档案，记录模型/框架/依赖/硬件边界与未知 | L89–95 保留三组独立档案；新增测试没有被外推为目标硬件或版本配套验证。 | 在所选资料范围内满足 |
| 3. AMD 所选官方后端执行差异与限制，不直接迁移 | L97 版本线和迁移限制未见关联回归。 | 在所选资料范围内满足 |
| 4. 初始化、first step、backward/update、保存等故障分界与小规模验证方法 | L101–113 保留故障分界、连通性与恢复设计及未执行边界。 | 在验证方法设计范围内满足 |
| 5. 源码/测试到职责定位，调用不补写未读依赖协议 | 代表性断言/适用与覆盖状态已补；但 C07 的摘要副本仍不完整，L121 另有错误测试限定名（S3-02/P3）。未读依赖协议继续 unknown。 | **部分满足，暂不通过** |

Objective 所需职责链与平台对照已存在，不能替代第 1/5 条的剩余准确性要求。本轮不更新任务计划状态，不把 `generic`、`source_checked` 或来源可访问视作跨平台运行证明。

## 7. 元数据、许可与执行边界

- 稳定 ID `training.framework-execution`、reference/training 主归属、`status: draft`、`platforms: [generic]` 及 17 个 `source_refs` 未见本轮关联回归。`updated_at` 仍为 2026-10-18；本报告日期与作者第三轮补充为 2026-10-19，不把该旧日期单独新增为技术阻断项。
- 取证表与 registry 是待核对证据，不是执行授权。未读取的 MindSpeed core 内部协议、具体可运行配套、完整 step 编译支持和跨框架恢复继续保持未知。
- 所有外部请求均只读；本报告仅作原创归纳及精确链接，不复制整份上游源码/文档，不改变任何第三方许可或仓库许可口径。
- 开始时工作树已有其他修改和未跟踪稿件；已在临时目录记录 494 个既有仓库文件的 SHA-256。它们不属于本轮清理、回滚或覆盖范围。

## 8. 本地检查与最终结论

1. 写入报告前及写入后，工作树只读执行 `PYTHONDONTWRITEBYTECODE=1 make check`，均退出码 0：**103 content entries / 493 sources**。补记本节后再次核对。该检查只验证结构与本地文件链接，不验证远程证据、技术正确性或硬件行为。
2. 在 `/private/tmp/b24-t062-s3.8ggz2n/build-snapshot` 复制仓库快照，使用仓库现有虚拟环境执行 `make check build`。第一次快照遗漏被 Git 忽略的既有 `build/catalog.json`、`build/catalog.md`，因此快照的检查退出码 2，报两条本地链接缺失；这是快照准备缺项，不是工作树正文缺陷。补入工作树既有 build 基线后重跑，退出码 0，仍为 **103 content entries / 493 sources**；两份清单仅在快照中重新生成。
3. 对照审阅基线的 494 个既有仓库文件：变化 0、删除 0，新增文件仅本报告；工作树原有两份 build 清单也以 SHA-256 单独核对，未被改写。既有未提交修改与未跟踪文件保持原状。
4. 未改动 `src/kb/`，不需要运行 `make test`；没有运行 PyTorch/Megatron/MindSpeed 上游测试、编译示例或本文的验证设计。以上结构检查不作为技术或硬件验证证据。

**最终结论：暂不通过。** C06、C08、R01 的原关闭条件已完成，C07 仍 OPEN；第三轮新增 S3-01/P2、S3-02/P3、S3-03/P3 均 OPEN。因此既不满足“全部遗留 OPEN 项 CLOSED”，也不满足“无新 OPEN P1/P2”。下一轮应只处理 C07 的取证 L121 条件同步、S3-01 的重编译判据、S3-02 的测试类归属与 S3-03 的精确引用，再进行定向复核；即使届时关闭，也不代表真实 GPU/NPU 或生产训练可靠性已经验证。
