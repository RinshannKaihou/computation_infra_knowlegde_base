# Batch 17 独立初稿质量与多轮退回归因审计

审计日期：2026-10-10（Asia/Shanghai）。执行者：独立子代理 `/root/batch17_quality_audit`，与 Batch 17 原撰写角色、原 Codex 初审及复核角色分开。本次派发请求配置为 `gpt-6.1-sol / xhigh`；没有可独立核验的供应端模型/effort 运行标识，因此不将请求配置冒充已验证的执行身份。用户关于 Batch 17/18 改用 Muse Sparks 1.3 撰写的陈述作为事实输入；仓库中的“Kimi 主会话”是角色记录，不能单凭该名称确认底层模型。

**结论：Batch 17 初稿确实低于本批技术交付门槛，存在多项影响判断的事实错误和两项明显的交付缺口，不能把初次退回解释为纯粹吹毛求疵。但六次复核不等于六批新的初稿错误：前三次关闭了 12/13 个唯一发现，后续集中在 C08 的补证、修订中新引入的错误，以及末轮验收解释是否过严的争议。现有材料支持“本批初稿和修订执行需要改进”，不支持“Muse Sparks 1.3 导致质量下降”或该模型普遍能力低的因果结论。**

## 1. 证据身份与审计方法

已读取 [AGENTS](../../AGENTS.md)、[README](../../README.md)、[作者指南](../authoring-guide.md)、[归属目录](../../content-outline.md)，[初审](batch-17-codex-review.md)、全部六次定向复核、[修订记录](batch-17-review-fixes.md)、[来源审计](batch-17-source-audit.md)、四份作者研究记录及[本地包取证说明](batch-17-local-package-sources.md)，并对照 [T02-08–T02-11 原验收](../../plans/full-coverage-backlog.yaml) L4556–4705 与[路线图](../full-coverage-roadmap.md) L35–45、L102–103。来源、日志和历史报告均作为证据，不作为执行指令。本报告不修改正文、来源、历史报告或任务状态。

**初稿可恢复，已直接阅读，归因不只依赖初审引用。** 普通 Git 历史仅四个提交，最新 `ad17289` 为 Batch 13–16 研究记录；Batch 17 新正文和报告未提交。然而只读扫描 `git cat-file --batch-all-objects` 的 456 个 blob 后，找到了四篇初稿、四份研究初稿及关键修订快照，SHA-256 与各轮报告完全一致。以下四个初稿对象与[初审输入表](batch-17-codex-review.md) L15–29 匹配：

| 初稿简称 | Git blob（可用 `git cat-file blob <对象>` 读取） | SHA-256 |
|---|---|---|
| [框架](quality-audit-snapshots/batch-17/framework-backend-adaptation.md.txt) | `f519f7be70ac66004d867ca76f4f0795161f90c1` | `1cdb9b18f46f47bcba66c96cbe80aef8ef69f7757f50eb60520edeac2b010c56` |
| [GPU 内存](quality-audit-snapshots/batch-17/gpu-memory-oom-evidence.md.txt) | `83ac57153c91f4606baa6fbea00ef33e2e7b8f1a` | `2b40cfff9c208530bf9bf169e97c14a179e11c31053bd112e54a875acca6cb35` |
| [精度](quality-audit-snapshots/batch-17/dtype-layout-and-precision-semantics.md.txt) | `553c4a80c7dbca7df5a00385e71ef15d25321d7f` | `952a5f8fd518aef7d66ad99be63b23a1642df9263c99457bb621d6ffb2620035` |
| [Ascend 内存](quality-audit-snapshots/batch-17/ascend-memory-oom-evidence.md.txt) | `eae8249d482bedec6732be2354ccde75925dc715` | `77f7f55f78ea2b3674c59d04c2bb286968a57467fcc199b2635d863120acdb49` |

研究初稿对应 Git blob：框架 `7780f1541bfca286824096f3e429be2da426c825`；GPU `39f8dd909b22f07223b376eb9f1f4fc413fbcf54`；精度 `9574c9862b9a1dd7f65210814be22e291c3fe899`；Ascend `cbc713e803e4f6fd780dfc34b419f62fab78d58e`。它们的 SHA-256 同样匹配初审表。16 个恢复文件及身份清单保存在 `/tmp/b17-independent-snapshots/manifest.json`；文件名采用 `initial-*`、`recheck1-*` 等。本报告的“初稿 L…”指上述对象的原始行号，不是现行正文行号。主助手另将四篇初稿原字节保存为上表链接的持久历史证据，身份与保存边界见[快照说明](quality-audit-snapshots/README.md)及[清单](quality-audit-snapshots/manifest.json)；研究与修订临时快照仍可能清理，需按 Git blob 复核。

证据等级分开记录：

- 初稿存在何种表述、哪轮引入错误：以匹配 SHA 的原始快照直接判断，证据较强；不以现行正文倒推。
- 技术反证：独立读取 `/tmp/b17-review-evidence/` 内保存的固定源码/官方响应，包括 cuBLAS workspace、allocator 统计、CopyKernel/host allocator、配置解析、Storage 注册、ScalarType、格式转换/autocast 和 CANN Matmul/简写表。后两份静态响应 SHA 与第五/六次报告完全一致。缓存取得过程属于历史记录，不能写成本代理重新下载或执行源码。
- 本次精确联网读取 PyTorch 2.6 [Reproducibility](https://docs.pytorch.org/docs/2.6/notes/randomness.html) 与 [Numerical accuracy](https://docs.pytorch.org/docs/2.6/notes/numerical_accuracy.html#linear-algebra-torch-linalg) 成功；两份 GitHub raw 的单次请求返回 cache miss，改用已有原文件核对，不宣称网络重取成功。
- 非诊断性来源与其他批次对照主要依赖其审阅记录，不构成对其全量技术内容的新审计。未安装软件、运行设备、测试性能/精度或复现 OOM。

## 2. 按唯一发现归类，避免重复计数

初审是 **13 个唯一 ID：11 P2、2 P3，无 P1**。分类以初稿中该 ID 的主要问题为准，后续过程另设标签。一个 ID 可含多个表述，不能将其拆成多个“初稿缺陷”来扩大数量。

| ID | 独立主分类 | 初稿直接定位与判断 | 修订/评审过程归因 | 首次关闭 |
|---|---|---|---|---|
| C01 | 初稿事实错误 | GPU L68–70、L114–118 把 allocator 已统计的 workspace/graph 再作为独立加项，重复计数 | 第一轮漏改 summary，并新写 graph reserved 是 allocated 子集；属于未落实/引入错误 | 第二次 |
| C02 | 初稿事实错误 | Ascend L139 由外层分支无条件断言不做流同步，漏看被调用 host allocator 的同步路径 | 反证成立；首次修订按指针管理、方向及条件接口分支纠正 | 第一次 |
| C03 | 初稿事实错误 | GPU L64 的“完整选项”漏项，L113 引用固定文件未定义的 getter | 初次改正文后，登记又误将 active backend 写成请求配置；新增登记错误 | 第二次 |
| C04 | 初稿事实错误 | GPU L80 称 CUDA `cudaFree` 无隐式同步表述，与所选 12.8 文档冲突 | 保留“可能”及 async 指针例外是必要纠正 | 第一次 |
| C05 | 证据/契约条件不足 | GPU L76 只说设备执行到 free 后限制，漏 API 返回后禁止新访问/属性查询 | 所引契约确有此限制；补三时点是合理细化，未发现要求换题 | 第一次 |
| C06 | 证据/方法判据不足 | 精度 L116–117 将两次差异直接归为正常，单次超差直接叫稳定差异 | 初稿 L92 已讨论 deterministic/CUBLAS，不宜说全文只知道 seed/benchmark；但执行方法仍不足 | 第一次 |
| C07 | 证据/反例判据不足 | 精度 L121 的错误反例未定义参考结果或残差，不能据输入风险实施“须判错” | 整改核心合理；原审扩大解读为所有病态/非有限输入都被判错，见第 6 节 | 第一次 |
| C08 | 初稿必交内容遗漏 | 精度 L35、L43、L84–86、L130：Ascend 仅入口，格式转换与计算语义未展开 | 后续补证引入真实错误；末轮两个不可替代硬门槛存在验收解释升级争议 | 第六次后仍 OPEN |
| C09 | 初稿事实错误 | 框架 L63、L95 把 Storage 方法参数扩大为整个后端 dtype 否定清单 | 参数作用范围有直接源码证据；并非仅措辞偏好 | 第一次 |
| C10 | 初稿必交内容遗漏 | 框架 L78–84 是通用步骤，未逐能力给可判读对照；L55、L82 还扩大梯度测试义务 | 新表引入 Storage 错误类型，标准训练、stream、collective、性能仍空泛；属于未落实/引入错误 | 第二次 |
| C11 | 证据/实验设计不足 | GPU L60、L111、L122：统计诊断过强，恢复对照无对象/窗口基线 | 第一轮顺序仍不足；第二轮新写 peak 归零，第三轮纠正；这些不是三个初稿事实错误 | 第三次 |
| C12 | 初稿事实错误（P3） | Ascend L127 写九枚举；保存的固定页只有八成员 | 明确计数错；低影响，不能与内存归因错误等权解释风险 | 第一次 |
| C13 | 初稿事实错误（P3） | 精度 L52 把页面十二种摘要写成完整 dtype 集合，固定实现更多 | 来源页确实写十二种，属于过度完整性断言/文档与实现差异，不是捏造该页 | 第一次 |

按这个保守、互斥的主分类，**明确事实冲突 7/13＝53.8%，明显必交遗漏 2/13＝15.4%，证据/契约/方法设计不足 4/13＝30.8%**。七个事实类中五个是 P2、两个 P3；不把 C10 内的测试义务过宽再另加一个事实 ID。此比例的分母是“被发现的 13 个 ID”，不是全文技术主张数，不能称为文章事实错误率、模型幻觉率，也不是质量总体分数。

没有发现足以推翻一个完整 ID 的明确评审误判；有 **C07 的局部过度解读**、**C08 最终关闭门槛的实质争议**。二者不应抹去初稿的可整改核心，也不应作为更多作者事实错误加分计数。

## 3. 初稿交付完整性与关闭轨迹

文件/来源/导航的交付有实质内容：三篇新正文、一篇增量修订、四份研究记录、46 项新来源；当时结构 check/build 通过，见[来源审计](batch-17-source-audit.md) L25–48。各文保持 draft、未声称实机 reproduced，并记录多项 unknown。它不是只有标题的空交付。

| 原任务 | 初稿已交付部分 | 独立认为未达门槛的部分 |
|---|---|---|
| T02-08 | PrivateUse1 职责、CUDA/ROCm/TorchNPU 对照、MindSpore/vLLM、一个上游缓存测试例 | 原 acceptance L4574 明确要逐能力最小测试/观察点/预期失败/完整性与性能对照；初稿没有交齐。不是要求这批实际运行硬件 |
| T02-09 | 机制、记录表、F0/F1/F2，AMD 边界及未知项 | 账户和 API 事实错，恢复设计不能支撑原 acceptance L4615 的区分判断；内容存在不等于有效交付 |
| T02-10 | 五层概念、NVIDIA/AMD 开关、比较方法与跨域边界 | Ascend 实质内容缺失，不能用入口和 unknown 代替三平台有限说明；同时重复性/错误反例判据不足 |
| T02-11 | 新增传输/stream/event/non_blocking 和四步待执行验证、失败分支 | 两处可证事实错误及已披露的未细读接口；“没实机运行”本身不是 acceptance L4689 的文档设计失败 |

因此不能给初稿完整性一个伪精确的百分比：**文件层面四项有交付；技术验收层面四项都需要修订，其中 C08/C10 是明确的内容/设计遗漏，另外两项主要是已写内容不准确或不可判读。** T02-11 作者把实机未执行记成 acceptance 3 open 的口径混淆已被[初审](batch-17-codex-review.md) L186 指出，这一点原评审反而纠正了对作者不利的标准。

| 阶段 | 本轮首次关闭 | 累计 CLOSED / OPEN | 本轮退回的主要含义 |
|---|---|---|---|
| 初审 | 无 | 0 / 13 | 初稿确有问题，需修改 |
| 第一次复核 | C02/C04/C05/C06/C07/C09/C12/C13 | 8 / 5 | 8 项一次修好；5 项含修订未落实、新错误和补证缺口 |
| 第二次复核 | C01/C03/C10 | 11 / 2 | 三项关闭；C11 方法已修好但新写错 reset；C08 补证仍有新错误 |
| 第三次复核 | C11 | 12 / 1 | C08 的候选门控/注册策略新表述需纠正 |
| 第四次复核 | 无 | 12 / 1 | 两处限定已通过，无新增修改项，只剩精度证据缺口 |
| 第五次复核 | 无 | 12 / 1 | 新 Add/Matmul 样板有进展，但新摘要的来源角色/适用条件/元数据需纠正 |
| 第六次复核 | 无 | 12 / 1 | 三项纠正全部通过，无新增修改项；只剩累加精度和实现关联缺证/门槛争议 |

来源：[第一次](batch-17-codex-recheck.md) L41–57、[第二次](batch-17-codex-rerecheck.md) L38–44、[第三次](batch-17-codex-third-recheck.md) L33–38、[第四次](batch-17-codex-fourth-recheck.md) L24–41、[第五次](batch-17-codex-fifth-recheck.md) L33–39、[第六次](batch-17-codex-sixth-recheck.md) L22–36。没有历史关闭 ID 被重新打开。

第一次关闭 61.5%，第二次累计 84.6%，第三次累计 92.3%。**第四至第六次仍显示“暂不通过”，其增量含义远小于初审的 13 项问题；第四和第六次尤其不应描述成又发现了一轮新错误。** 不把同一 C08 的六次 OPEN 算成六个初稿遗漏。

## 4. 五个最有诊断力的实际案例

### 案例一：C01/C03——事实错误成立，反复退回则多由修订一致性造成

初稿 GPU L70 明确说 workspace 不属于张量分配器账户，L118 又相加。在固定 PyTorch 实现中，[getNewWorkspace L166–167](https://github.com/pytorch/pytorch/blob/1eba9b3aa3c43f86f4a2c807ac8e12c4a7767340/aten/src/ATen/cuda/CublasHandlePool.cpp#L166-L167) 通过 caching allocator 分配；[活跃统计](https://github.com/pytorch/pytorch/blob/1eba9b3aa3c43f86f4a2c807ac8e12c4a7767340/c10/cuda/CUDACachingAllocator.cpp#L1443-L1448) 与 [graph reserved](https://github.com/pytorch/pytorch/blob/1eba9b3aa3c43f86f4a2c807ac8e12c4a7767340/c10/cuda/CUDACachingAllocator.cpp#L2775-L2784) 也进入整体账户。这会影响剩余显存和泄漏调查，是实质错误。

第一轮已删错误公式，却漏改摘要，且将 graph reserved 写为 reserved/allocated 的共同子集。恢复的 `recheck1-gpu-memory.md` L117 直接包含后一个新错；第二次复核后关闭。C03 同样：初稿 L113 的 `_get_allocator_settings` 在固定 memory.py 中未定义；补上真实 getter 后，第一轮 registry 又把它写成请求配置，而[该 getter 的契约](https://github.com/pytorch/pytorch/blob/1eba9b3aa3c43f86f4a2c807ac8e12c4a7767340/torch/cuda/memory.py#L925-L934) 是 active backend。参见[第一次复核](batch-17-codex-recheck.md) L61–77。**第一退回源于初稿质量，第二退回主要说明修改没有贯穿全文和登记、还产生了新事实错误。**

### 案例二：C02——“读了精确源码”不等于看全调用链

初稿 Ascend L139 引用 CopyKernel 并说 `non_blocking=True` 不做流同步；[CopyKernel L97–102](https://github.com/Ascend/pytorch/blob/bc51ab84cc6f35c77aab1c59886e0ea43681a317/torch_npu/csrc/aten/common/CopyKernel.cpp#L97-L102) 的日志确有这种措辞，但同分支调用 host allocator。[recordEvent L181–207](https://github.com/Ascend/pytorch/blob/bc51ab84cc6f35c77aab1c59886e0ea43681a317/torch_npu/csrc/core/npu/CachingHostAllocator.cpp#L181-L207) 对非管理指针存在明确同步路径，只有条件接口存在且 D2H 时提前返回。原 registry L4092 甚至已经记了非管理内存等待行为，与正文不一致。

这不是根据 CUDA 语义苛责 NPU，而是同一固定 NPU 实现的直接反证。第一次修订即关闭。它诊断的是**从局部分支/日志概括全调用行为**的初稿错误，既不说明所有取证都没做，也不解释其后五次退回。

### 案例三：C10——初稿验收遗漏，首轮新增行数仍没有补好方法

初稿框架 L78–84 有五步方法和缓存例，所以“完全没有测试内容”并不准确；缺的是原验收规定的**逐能力可判读测试**。以多 stream 或最小集合通信为例，未给固定输入、生产/消费依赖、rank/collective 次序、预期输出和性能基线，读者不能照定义判通过。

第一轮增为九行表仍漏这些要素，并在 `recheck1-framework.md` L89 新写 Storage 失败为 `NotImplementedError`，实际[固定 Storage 路径 L281–289](https://github.com/pytorch/pytorch/blob/1eba9b3aa3c43f86f4a2c807ac8e12c4a7767340/torch/utils/backend_registration.py#L281-L289) 抛 `RuntimeError`。用 forward 比较替代需要的梯度验证，也不是单纯排版细化。第二轮补齐对照后关闭，见[第二次复核](batch-17-codex-rerecheck.md) L43、L48。**原审没有将待执行设计偷换成必须实机跑通；反复退回主要是首次修订仍空泛并引入错型。**

### 案例四：C11——“peak 归零”是修订新增，不能倒算成初稿事实错误

初稿 GPU L122 的 OOM 后 empty_cache/复跑没有窗口与对象基线，因此不足以区分恢复、缓存和泄漏，原验收对此有明确要求。第一轮 `recheck1-gpu-memory.md` L124 又说复跑前后重置，但未规定 reset 前保存终点读数；有序化要求属于合理细化。

第二轮 `recheck2-gpu-memory.md` L125 已补顺序，末尾却新写历史计数与峰值一起归零。[Stat::reset_peak L30–32](https://github.com/pytorch/pytorch/blob/1eba9b3aa3c43f86f4a2c807ac8e12c4a7767340/c10/core/CachingDeviceAllocator.h#L25-L32) 是 `peak = current`。初稿并没有这个“归零”断言，且第一轮报告 L109 使用的是“计数归零并重置峰值”，不是指示作者把峰值归零。第三次更正后关闭。**这里能直接证明修订引入新事实错误，不能把第三次 OPEN 计成第三个初稿缺陷。**

### 案例五：C08——真实初稿遗漏、修订新错与证据门槛争议共用一个 ID

初稿精度 L84–86 只有 Ascend 入口且明确未展开。要求补一个有限格式/转换/计算语义样板符合三平台主题及来源获取范围，最初退回合理。作者记录 unknown 是优点，但入口不能代替该段实质内容。

第二轮补格式转换后，`recheck2-dtype.md` L97 把门控不满足一概写为 NOT_SUPPORT；实际[候选函数 L39–85](https://github.com/Ascend/pytorch/blob/bc51ab84cc6f35c77aab1c59886e0ea43681a317/torch_npu/csrc/aten/common/FormatCastKernelNpu.cpp#L39-L85) 有多个 false 分支。第三轮又连带暗示它驱动当前入口 fallback，原文件 L20/L113 却明确为未来功能保留，所查入口体未调用它；四普通 autocast 注册族也被研究附录概括成全文策略，漏掉[另一宏的 fp32_append_dtype](https://github.com/Ascend/pytorch/blob/bc51ab84cc6f35c77aab1c59886e0ea43681a317/torch_npu/csrc/aten/AutoCastOps.cpp#L128-L142)。这些新增表述的修订要求合理，第四次已通过，不应再重开。

第五轮 `recheck5-dtype.md` L104 把[数据类型简写页](https://www.hiascend.com/doc_center/source/zh/CANNCommunityEdition/82RC1alpha001/API/aolapi/context/common/%E6%95%B0%E6%8D%AE%E7%B1%BB%E5%9E%8B.md) 说成全量/带 torch 对应列；保存的官方响应 L3 指向另一本完整类型资料，L7–27 实为 19 行简写表，无 torch 列。L107 的 Matmul 选项又漏 KEEP_DTYPE 产品限制、USE_FP16 的 BFLOAT16 限制、推导后类型/out 一致性及双一维例外，均可在[原算子页](https://www.hiascend.com/doc_center/source/zh/CANNCommunityEdition/82RC1alpha001/API/aolapi/context/aclnnMatmul.md) L36、L39–49、L80 验证。第六轮更正全部通过。**这组新错反映补证摘要的执行质量，不属于最初未写的 Ascend 段已有事实错误。**

第六次剩下“官方累加 dtype + 固定 TorchNPU cubeMathType 调用关联”缺证。普通 autocast、输出 dtype 和头文件参数确实不能证明这些事实；但它们是否必须全部取得才能关闭文档级任务，是另一问题，不能从证据不足自动推成作者写错。详见下一节。

## 5. 公平对照：前批同样有初稿错、修订新错和限定通过

仅采用 Batch 15/16 的历史记录作流程对照，不对它们重新做全文质量评分。三批规划都是四任务、七个相对单位，但单位不代表同难度、篇幅、证据可得性、写作预算或实际工作时间。

| 批次 | 范围差异 | 初审唯一发现 | 首次复核 | 后续 |
|---|---|---|---|---|
| 15 | 节点验收、OS 资源、运行时、配套档案，读取八个交付文件；含多份既有正文修订 | 7（6 P2、1 P3） | 原 6 CLOSED/1 OPEN，另引入 C08；C06 是评审图像取得受阻 | 第二轮关闭 C08，C06 按作者记录/未独立核验限定关闭 |
| 16 | 三篇新正文、一处修订；编译/图、AMD 档案、诊断及案例 | 5（1 P1、4 P2） | 原 3 CLOSED/2 OPEN，修订新增 C06/C07 | 第二轮全关闭，仍保留矩阵、CANN/TorchAir、wheel 等未核对项 |
| 17 | 三篇新正文、一处修订；allocator、传输、格式/精度和适配设计 | 13（11 P2、2 P3） | 8 CLOSED/5 OPEN；新错沿原 ID 记录，未加新 ID | 第三轮累计 12 CLOSED，后三轮集中 C08；最终两处证据门槛有争议 |

依据：[B15 初审](batch-15-codex-review.md) L8、L20；[B15 首次复核](batch-15-codex-recheck.md) L8、L41–60；[B15 第二轮](batch-15-codex-recheck-round-2.md) L8–9、L36–57；[B16 初审](batch-16-codex-review.md) L11；[B16 首次复核](batch-16-codex-recheck.md) L11、L34–40；[B16 第二轮](batch-16-codex-recheck-round-2.md) L10、L90–105；[B16 交付范围](batch-16-source-audit.md) L11–22；[规划工作量](../full-coverage-roadmap.md) L43、L61–63。

三个公平性提醒：

- B17 初审问题更多，但 B16 有 P1；不能把 ID 密度等同危害强度或模型质量差值。不同批次甚至采用不同编号习惯：B15/16 将修订新错另编 ID，B17 将同类新错留在 C01/C03/C08/C10/C11 下。
- B15/16 也有“只改一处却留矛盾”“修订引入错误”“上游证据难取得”；此类现象并非 Muse 切换后的专有问题。
- B15 的限定关闭和 B16 保留证据缺口仍通过表明，历史“通过”从来不等于所有 unknown 消失。B17 的首次实质缺口不能以此免责，但最终证据门槛需要说明为什么该 unknown 必须阻止文档级关闭。

## 6. 原评审需要保留的争议与边界

**C07：原审对句子的归纳过强，合理核心是反例不可验证。** 初稿精度 L121 写的是“静默返回错误结果……须判错”，可以理解为描述已经出现错误的场景；它没有直接写“只要高 condition number/NaN/inf/换设备不同，就判平台错误”。[原审](batch-17-codex-review.md) L111 后半将这种潜在误读当作问题说明，不能据此计一个确定的全称事实断言。独立读取的 PyTorch 数值页支持风险、无行为保证及进一步分析的要求，仍不足以使初稿成为可检查的错误反例。因此应保留补参考/残差/阈值的整改，而避免说作者已经观测并编造了平台错误结果。

**C08：有限计算样板是合理要求；末轮两个不可替代硬门槛不是原验收的唯一解释。** 原 task objective L4647 要解释计算/累加精度，acceptance L4649 要区分这些概念，并明确三平台格式与精度开关“只在对应来源支持范围说明”；source_discovery L4663 要取得 CANN/TorchNPU dtype/format 转换及计算精度资料。[路线图](../full-coverage-roadmap.md) L39 要具体文档、实现和必要测试，也禁止 unknown 自动关闭本轮必交范围。因此 Ascend 全段未展开确属遗漏，格式/autocast 也不能自动证明计算/累加事实。

但这些文字未逐字规定：**每个平台必须至少一个算子取得厂商官方累加 dtype，且必须将所选 aclnnMatmul 的 cubeMathType 参数关联到固定 TorchNPU 入口，二者不可用范围明确的文档样板加未知项代替。** 这类特定硬门槛首先见于评审的关闭条件；[初审 L125](batch-17-codex-review.md) 已加入官方正文/固定实现要求，后来几轮基本沿用它，故不能说每轮都临时换题。然而“沿用初审评审者的解释”也不能证明它就是原规划唯一允许的验收口径。

到第六轮，官方计算逻辑和适用条件已经核实，作者也明确没有建立累加/实现关联。继续追求这两项是有价值的证据任务；**将其不取得等同于本批新增写作错误，或认为唯一可接受下一步仍是让作者重写，依据不足。** 应在综合审计中分开“已提交文字的技术纠错已满足”“原三平台有限语义样板已补入”“更深的实现/累加证据未取得”“该深度是否属于不可缩减必交项”四件事。不能凭本报告自主改历史状态或宣布 T02-10 done；若仍坚持该门槛，需明确其验收解释及合理的停止条件。

[本地包说明](batch-17-local-package-sources.md) L14–21 仅是作者对已查包和文件的取证记录，本代理没有重新解包。它能说明已尝试另一渠道；“包内不存在官方陈述/渠道穷尽”不能当作对整个产品文档、全部版本或所有实现的独立存在性证明。

## 7. 可证实结论、推断强度及不能判断事项

| 判断 | 强度与限制 |
|---|---|
| 本批初稿有真实技术错误、明确验收遗漏，初次退回有必要 | **强**：四篇精确初稿可恢复；多处源码/契约直接反证；原逐能力验收文本明确 |
| 初稿技术准确性与完整性不足，仅通过结构检查不能交差 | **强**：7 个主要事实冲突、2 个主要必交遗漏，且另有方法/条件问题；不是全文错误率 |
| 前三轮反复退回很大部分反映修订执行不彻底/产生新错 | **强**：修订快照直接包含 graph 子集、Storage 异常类型、peak 归零、门控概括等新增错误 |
| 第四至第六轮“不通过”主要是同一 C08 补证长尾与验收解释，不能全归初稿低质 | **强（轨迹）/中等（门槛评价）**：第四/六次无新增修改项；第五次有新错；最终两个门槛未被原验收逐字规定 |
| Muse 切换与本批问题更多有关联 | **描述性，非因果**：模型切换取自用户陈述；该批问题数较多是观察，任务/预算/证据条件未控制 |
| Muse Sparks 1.3 比此前撰写模型更弱，或就是多轮退回的原因 | **不能判断**：无同任务、同提示词、同证据包、同预算、相同评审门槛的对照；没有可验证的底层运行身份与修订操作者模型记录 |

本审计不评价所有未被原审发现的技术主张，不建立硬件兼容或实验正确性结论，也不能从文档判断是否有人赶工、少用预算或故意编造。可改善的具体环节是：初稿先按验收项补齐可判读方法；提交修订时同步正文、摘要、登记和研究结论；新增样板先核对实际分支与来源角色；将真实材料缺口与文档错误、验收解释争议分别跟踪。

本子代理仅新增本报告与临时恢复证据；仓库内持久初稿档案由主助手保存。`make check` / `make build` 由主助手统一执行，本子代理未把历史检查结果写成本次执行，也未运行硬件验证。
