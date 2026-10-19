# Batch 25 T06-06 第四轮定向复核报告

- 日期：2026-10-20（Asia/Shanghai）。本轮为第四轮修订后的内容定向复核，不是训练、启动或硬件验证。
- 对象：[性能分解正文](../../knowledge/06-training/performance-analysis.md)、[第四轮修订记录](batch-25-t06-06-sources.md)、[组合身份页](../../knowledge/06-training/parallelism-and-state.md)；对照[初审](batch-25-t06-06-codex-review.md)、[第二轮复核](batch-25-t06-06-codex-recheck.md)、[第三轮复核](batch-25-t06-06-codex-recheck-2.md)、[来源登记](../../sources/registry.yaml)和[任务验收条款](../../plans/full-coverage-backlog.yaml)。下列正文行号针对本轮快照。
- 执行与模型核验：当前本地 Codex CLI 会话独立复核，未委托其他审阅者。按当前 `CODEX_SESSION_ID` 定位本会话 JSONL，仅抽取 `turn_context` 的模型与推理字段，得到单一 `model=gpt-6.1-sol`、`effort=xhigh`；本轮结果无模型回退标记。历史报告的实际模型记录不改写。
- 写入边界：仅新增本报告，不修改正文、来源记录、registry、导航、任务或 `06.2-G3` 状态。仅执行本地纯算术检查及仓库结构校验，不执行训练、profiling、checkpoint 恢复或设备操作。

## 一、结论摘要

**B25-T06-C04 保持 OPEN（P2）。** 本轮已正确补齐 dense/expert DP、每 stage 层数、micro-batch 数和 A/B/恢复 A 结果表，认可这些子项完成；但正文第 117、119 行仍没有填写 B 的具体组成员与采集 rank，保留了“重算后的 expert 组各 1 rank”等待填指示。第三轮要求的“代表 rank/组成员的联动结果与具体采集选点”尚未交付，不能把正确的维度算术等同于完整候选记录已经填写。

**C01、C02、C03、R01、C05、C06、C07 均保持 CLOSED，未发现回归；无须新增 B25-T06-R3-xx 发现。** 累计仍为 8 项发现：7 项 CLOSED、1 项 OPEN。本轮指出的未填写组映射及修订摘要与交付不符，继续归入 C04，不重复编号。

**最终整体判定：仍需完成 C04 的剩余静态填写，暂不声明 T06-06 通过既定审阅范围；不建议关闭 `06.2-G3`。** 不要求补造实测数据，也不要求启动候选配置。

### 复核快照

| 文件 | SHA-256 |
|---|---|
| `knowledge/06-training/performance-analysis.md` | `a54d9654831416eed26a1bd9f5161b8aef73df60c36568455ef3baf68efea04c` |
| `docs/research/batch-25-t06-06-sources.md` | `ddfe1c253127913de10cfb5e8372435a881f7a3a2b739fce1ebca296de64334c` |
| `knowledge/06-training/parallelism-and-state.md` | `d46cfcf6dc785de96fba9fcfb538e1d3453db2e4aa359d637c03d5f1307f9338` |
| `sources/registry.yaml` | `99b81d2047b01fc2ed7885143d062e6e0d7b44a0415db22dd63d1d9dd474857b` |
| `docs/research/batch-25-t06-06-codex-recheck-2.md` | `8f7cffff94187c04dbcd13cdc235f4d3c5f03d25851937eb63dd28f794ce4a18` |

## 二、C04：已完成部分与算术核对

本轮逐项核对正文第 109–129 行，而非直接采信来源记录第 64 行的修订总结。解释沿用身份页第 90–125 行的合成条件：64 rank＝8 节点×8 卡，连续 8 rank 为一节点，32 层、128 专家、EP=4、TP=ETP=2、CP=2、默认轴序；未启用的 GTP/EGTP 因子均为 1。新增 global batch=32、micro-batch size=2 是本对照明确设定的固定项，不冒充身份页其他 batch 示例的原始数值。

| 核对项 | 独立核对结果 | 子项判定 |
|---|---|---|
| 候选语境及单变量 | A 的 TP2/PP2/CP2 与身份样例一致；B 仅将 PP 改为 4，其余已声明因子不变 | 接受，不再沿用第三轮的 TP4 候选 |
| dense DP | A：`64/(2×2×2)=8`；B：`64/(2×4×2)=4` | 正确 |
| expert DP | 专家 grid 不额外乘 CP；`64/(ETP×EP×PP×EGTP)` 给出 A＝4、B＝2。不能把 dense DP 直接当 expert DP | 正确 |
| 层数及均匀分段 | A 每 stage 16 层；B 每 stage 8 层。在身份页的连续均分约定下，分别对应 `[0–15,16–31]` 与 `[0–7,8–15,16–23,24–31]` | 正确；不是实际调度/模型装载结果 |
| micro-batch 换算 | A：`32/(8×2)=2`；B：`32/(4×2)=4`；反算 `8×2×2=4×2×4=32`。这里使用不含 CP 的 dense DP，不乘 EP 或 expert DP；两条件均整除且 micro-batch 数至少为 1 | 正确；固定输入及有效 token 口径下，总预算不因 CP 副本重复计数 |
| 已列整除检查 | A：`64%8=0`；B：`64%16=0`；`128%4=0`；固定序列长度可被 `2×CP=4` 整除 | 正确；只支持所列静态检查，不等于完整启动验证 |
| 结果表及实测边界 | 第 123–127 行已出现 A、B、恢复 A 条件行；吞吐、质量、恢复复测均为“未执行”，恢复 A 的部分分解列为破折号，没有伪造观测或收益 | 结果表结构这一子项完成，不再作为 OPEN 理由 |

公式依据为同一固定 Megatron commit 的 [expert grid 初始化与 PP 组一致性检查](https://github.com/NVIDIA/Megatron-LM/blob/4b4acac9a1d28ea6829c8d4f566d75698a21249d/megatron/core/parallel_state.py#L871-L907)、[固定 batch 的 micro-batch 计算](https://github.com/NVIDIA/Megatron-LM/blob/4b4acac9a1d28ea6829c8d4f566d75698a21249d/megatron/core/num_microbatches_calculator.py#L367-L395)，以及 [world-size 整除](https://github.com/NVIDIA/Megatron-LM/blob/4b4acac9a1d28ea6829c8d4f566d75698a21249d/megatron/training/arguments.py#L422-L431)、[序列长度整除](https://github.com/NVIDIA/Megatron-LM/blob/4b4acac9a1d28ea6829c8d4f566d75698a21249d/megatron/training/arguments.py#L1295-L1298)、[EP 与专家数检查](https://github.com/NVIDIA/Megatron-LM/blob/4b4acac9a1d28ea6829c8d4f566d75698a21249d/megatron/training/arguments.py#L1600-L1603)。本轮实际重读这些位置；未把其他版本约束拼成已验证的运行配置。

## 三、C04 保持 OPEN 的具体依据

**受影响位置：正文第 117–119、129 行；来源记录第 64 行。优先级仍为 P2。**

1. **采集选点仍是要求，不是已填写的集合。** A 列仅举 rank 37 并回指原身份页；B 列仍写“4 个 stage 各 ≥1 rank、新 dense DP 组、重算后的 expert 组各 1 rank”，没有一个 B 的实际采集 rank、所属 PP/DP/EP 组或 stage/expert 对应值。“4 个 stage”是覆盖数量，不是覆盖各 stage 的 rank 记录。正文第 129 行称选点为推导值，来源记录称已逐格填写，均不足以代替缺失的具体结果。
2. **专家组放置没有完成重算结果的表达。** 第 117 行的“EP 组的节点内放置随步长变化重算”没有给出步长和组成员；第 118 行也没有展示 dense/expert 两套 PP 组是否相同。两个 grid 的 PP 数量相同，不自动证明其 PP 组成员相同。本轮复算表明该候选确实可满足这条静态关系，但正文尚未把它接到选点记录；本项不是判定候选算术非法。
3. **此例尤其应区分改变与不变。** 默认轴序下，PP 步长从 32 变为 16，但 EP 步长仍为 2、expert-DP 步长仍为 8；EP 的全局组成员和节点内放置实际上不变，变化的是 PP 链、stage 身份、dense/expert DP 组范围。不能用“布局变了所以 EP 放置也变了”的笼统理解替代联动核对。

### 审阅者复算：缺失字段确实可以填写

下表是**审阅者本轮额外生成的纯算术核对**，用于定位 C04 的剩余缺口；不是作者已交付的正文记录，更不是进程组初始化或测量证据。按身份页默认轴序固定其他坐标、扫描目标轴，结果如下；专家编号遵循固定源码的 [本地专家索引规则](https://github.com/NVIDIA/Megatron-LM/blob/4b4acac9a1d28ea6829c8d4f566d75698a21249d/megatron/core/transformer/moe/moe_layer.py#L181-L194)。

| 静态身份字段 | A | B |
|---|---|---|
| dense 步长（慢→快） | `[pp=32,dp=4,cp=2,tp=1]` | `[pp=16,dp=4,cp=2,tp=1]` |
| expert 步长（慢→快） | `[pp=32,edp=8,ep=2,etp=1]` | `[pp=16,edp=8,ep=2,etp=1]` |
| rank 37 dense 坐标 | `(pp=1,dp=1,cp=0,tp=1)` | `(pp=2,dp=1,cp=0,tp=1)` |
| rank 37 stage/layer | stage 1，层 16–31 | stage 2，层 16–23 |
| rank 37 的 dense DP 组 | `{33,37,41,45,49,53,57,61}` | `{33,37,41,45}` |
| rank 37 的 expert DP 组 | `{37,45,53,61}` | `{37,45}` |
| rank 37 的 EP 组及放置 | `{33,35,37,39}`，均在节点 4 | `{33,35,37,39}`，仍均在节点 4 |
| rank 37 的 TP/ETP 组、专家 | `{36,37}`；EP 组内序号 2，expert 64–95 | 不变；不能误写为 expert 编号随 PP 改变 |
| 含 rank 37 的 PP 链（两套 grid 一致） | `{5,37}`，分别在 stage 0、1 | `{5,21,37,53}`，分别在 stage 0、1、2、3 |

本轮用独立 Python 算术枚举两套 grid 的 64 个 rank，检查每种单轴分组对 rank 集合的无重无漏覆盖、两套 grid 的全部 PP 组相等、A/B 的 EP 分组完全相同，以及 batch/整除关系，均通过。只生成坐标和分组，不导入或执行上游训练代码，不初始化通信。它证明可填上述静态值，不证明运行支持或性能收益。

### 最小剩余关闭条件

- 在现有 A/B 表旁实际填写一组具体采集 rank 及其两套组身份、stage/layer/expert 归属。例如可采用上表的 PP 链作跨 stage 代表，并说明 TP/EP 组内比较时需要哪些组员证据；可以声明只覆盖代表链，不要求全 64 rank 采集，也不将单 rank 视为全组证据。
- 写出对应 dense/expert PP 组一致性的核对结果，以及哪些步长/组成员改变、哪些不变；本例 EP 组节点内放置应明确记为“不变”，不能继续只写“重算”。
- 来源记录同步限定实际填写范围；保留现有正确的 DP、batch、层数与结果表，所有运行字段继续允许“未执行/unknown”。完成后只需定向复核 C04，不重开其余已关闭项。

这些条件沿用第三轮的具体关闭条件，不增加硬件实验、全量分组列举或工具命令要求。结果表缺失、TP4 语境不完整等已修好的旧缺口不再作为开放理由。

## 四、已关闭项的回归检查

| 发现 ID | 判定 | 本轮核对 |
|---|---|---|
| B25-T06-C01（P2） | **保持 CLOSED** | 正文第 92、95–98、139、148–157 行保留冻结 checkpoint 的权重/optimizer/LR/scaler/RNG/数据游标与输入身份、重复基线、A→B→A、关闭 profiler 的独立吞吐复测、配对等预算质量观察及短窗口有限结论；新增静态样例未越过这些门禁。 |
| B25-T06-C02（P2） | **保持 CLOSED** | 第 93–94、135–136、156 行仍将阶段排名视为候选，PP 按生产者→通信→消费者回溯；EP/长度区分工作量与单位效率；通信、CPU/设备分支要求依赖证据，缺失时记未解释空档；未把静态布局直接认定为瓶颈原因。 |
| B25-T06-C03（P2） | **保持 CLOSED** | 第 91 行保留 RL step 与 update mini-batch 的不同计步单位、continuous/discrete 边界、active/cycle—文件身份及完整性门禁；与重读的固定 verl 指南、PyTorch 2.6 末 cycle 导出说明一致。 |
| B25-T06-R01（P3） | **保持 CLOSED** | 第 92、96 行仍明确恢复/复跑为主动实验、隔离副本、独立输出目录与保护冻结 checkpoint；第 148 行不把配置回退当状态回退。没有把新增候选表当成执行授权。 |
| B25-T06-C05（P2） | **保持 CLOSED** | 第 70 行、来源记录第 49 行及 registry 保持 Nsight 2025.3 目录证据与 verl 镜像 2025.6.1 分立，OS runtime 仍未核对。本轮重读固定 Dockerfile 的版本声明、安装和链接；未借其证明 2025.3 工具能力或实际环境配套。 |
| B25-T06-C06（P3） | **保持 CLOSED** | 第 63、98、140、146 行保留 Timer 两端 synchronize、可选 barrier、interval-time 的 `elapsed(barrier=True)`、读日志/新计时区别及禁止部分 rank 随意加组 barrier；与本轮重读固定源码一致。 |
| B25-T06-C07（P3） | **保持 CLOSED** | 第 82、94、137、147 行通信交接链接、数据饥饿与供电散热链接均存在；带宽退化指南第 41 行保留回链，06 章入口第 51 行、身份页第 86 行可进入性能正文。未发现导航回归。 |

## 五、本轮来源核对与新问题检查

本轮沿既定固定 commit 读取一手证据。下列 blob SHA 为 GitHub 返回的文件身份，区别于本地快照 SHA-256；行号使用 GitHub 文件坐标，不用网页工具转换后的行号构造源码锚点。

| 来源 | 本轮重读位置与范围 | Git blob SHA |
|---|---|---|
| [Megatron parallel_state.py](https://github.com/NVIDIA/Megatron-LM/blob/4b4acac9a1d28ea6829c8d4f566d75698a21249d/megatron/core/parallel_state.py#L479-L556) | RankGenerator 的轴序/分组，第 601–620 行默认顺序与 GTP/EGTP 默认值、第 871–907 行 expert DP、两个 grid 的 PP 组相等要求 | `2a3c75811221aacaa0130f8feb081859788f3c5d` |
| [Megatron num_microbatches_calculator.py](https://github.com/NVIDIA/Megatron-LM/blob/4b4acac9a1d28ea6829c8d4f566d75698a21249d/megatron/core/num_microbatches_calculator.py#L367-L395) | 固定 batch 的整除、micro-batch 数和至少为 1 的检查 | `033820f174a6ed8d66853ae89b09220554f27341` |
| [Megatron arguments.py](https://github.com/NVIDIA/Megatron-LM/blob/4b4acac9a1d28ea6829c8d4f566d75698a21249d/megatron/training/arguments.py#L422-L431) | 第 422–431、1295–1298、1600–1603 行所列 world-size、序列长度及专家数整除 | `fd30984b38ae64e1207a948c71ef04dbaf5925da` |
| [Megatron moe_layer.py](https://github.com/NVIDIA/Megatron-LM/blob/4b4acac9a1d28ea6829c8d4f566d75698a21249d/megatron/core/transformer/moe/moe_layer.py#L181-L194) | EP 组内序号到本地专家集合的映射 | `48e78775a849575a9d46f95d900490ded4a5946d` |
| [verl torch_profiling.md](https://github.com/verl-project/verl/blob/1876b06d0a3e4e71e06230be10af14492ca8a75b/docs/perf/torch_profiling.md#L152-L204) | 第 152–204、250–335 行：mini-batch schedule、continuous/discrete、跨进程阶段及缺失活动边界 | `04d0903ba3b97f8bba285ac962b53b027d5489c9` |
| [verl nsight_profiling.md](https://github.com/verl-project/verl/blob/1876b06d0a3e4e71e06230be10af14492ca8a75b/docs/perf/nsight_profiling.md#L11-L32)与[Dockerfile.stable.sglang](https://github.com/verl-project/verl/blob/1876b06d0a3e4e71e06230be10af14492ca8a75b/docker/Dockerfile.stable.sglang#L52-L60) | 指南旧文件名仍存在于文案；实际 Dockerfile 第 9、52–60 行声明、安装并链接 2025.6.1 | 分别为 `f8665b42a01d52b39fdf4f923b35dd376c6172a1`、`76fb2ffb4afc9a37b1c0b8b03ef26e00b7b7ab11` |
| [Megatron timers.py](https://github.com/NVIDIA/Megatron-LM/blob/4b4acac9a1d28ea6829c8d4f566d75698a21249d/megatron/core/timers.py#L109-L168)与[training.py](https://github.com/NVIDIA/Megatron-LM/blob/4b4acac9a1d28ea6829c8d4f566d75698a21249d/megatron/training/training.py#L2824-L2833) | Timer 同步及 barrier 语义；interval-time 与均摊吞吐公式 | 分别为 `78204ad243f068e0944d1f54f113780363003a78`、`57b8efe9390eca9ca8596ed5bb073ed62d9d014d` |
| [PyTorch 2.6 profiler](https://docs.pytorch.org/docs/2.6/profiler.html#torch.profiler._KinetoProfile.export_chrome_trace) | schedule/step、Kineto 只导出末 cycle、shape/stack 采集额外开销 | 版本化文档页，无 Git blob 记录 |

部分精确 URL 经网页工具读取失败，随后用 GitHub 连接器在相同冻结 ref 下读取指定文件行成功；失败不解释为文件不存在。本轮没有重新获取 Nsight 2025.3 子页、CANN msprof、AMD 指定版本细节或全部 TorchNPU/MindSpeed profiler 源码，不新增确认其访问状态，也不借相邻版本补证。工具能力、CLI、版本组合、量化扰动和真实运行验证的既有 unknown 继续保留。

**新问题检查：未发现需以 B25-T06-R3-01 起另立的问题。** C04 的剩余静态填写缺口沿原 ID 跟踪；不将未实测本身算作缺陷，也不将源码检查/本地算术通过解释成硬件验证。

## 六、验收与交付边界

- T06-06 验收条款 1–5 的通用方法要求保持满足：有效产出口径与重叠边界、工具范围及 unknown、各分支依赖证据、重复/恢复和吞吐质量双判据、主动实验影响与专题交接均未回归。
- 既定承接的 `06.2-G3` 组合映射/性能验证仍有 C04 一项 OPEN，故整体仍需修订。此结论不影响其余 7 项 CLOSED，也不把静态候选判为一定不可运行。
- 正文继续保持 `draft / source_checked`、空 `environment_refs` 与未实测声明；本报告不更改编辑状态或任务状态，不扩大为所有平台/工具/版本的兼容结论。
- 已执行 `make check`、`make build`，均通过：`107 content entries; 525 sources`，生成 `build/catalog.json` 与 `build/catalog.md`；本报告 8 个本地 Markdown 链接另行核对，目标均存在。这些检查不证明技术因果、远程链接可达性、版本兼容或硬件正确性。
- 写入前纳入快照的 532 个既有文件经 SHA-256 对比均未修改或删除，本轮工具仅新增本报告。首次“工作区仅有一个新增文件”的严格断言因期间另出现 `docs/research/batch-25-t06-05-codex-recheck-3.md`、`docs/research/batch-25-t06-07-codex-recheck-2.md` 而未通过；随后将这些非本轮工具写入的并发新增文件与本报告分离核对，既有文件哈希检查通过。并发文件均保留，不读取其内容、不归为本轮交付，也不据此修改其他任务。
- 未修改 `src/kb/`，未新增测试或执行 `make test`；本轮纯算术检查不是训练测试，未运行任何 profiling 或硬件实验。
