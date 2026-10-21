# Batch 30 · T08-04 第四轮定向复核报告

## 会话元数据

| 项目 | 记录 |
|---|---|
| 审阅角色 | 独立批次审阅者；只复核指定六项及本次修订引入的问题，不承担正文编写或修订 |
| 实际执行模型 / 档位 | `gpt-6.1-sol / xhigh` |
| turn_context 核验方法 | 读取本进程 `CODEX_THREAD_ID`、`CODEX_SESSION_ID`，据其定位本会话 rollout，逐行解析 JSONL；交叉核对 `session_meta.id`、最新 `turn_context` 及 `collaboration_mode.settings`，未借用默认配置或其他会话记录 |
| 核验结果 | 两个环境会话 ID 均与 `session_meta.id` 一致；`turn_context.model=gpt-6.1-sol`、`effort=xhigh`、`cwd=/Users/ywang2397/work/AI_reliability_knowledge_base`；嵌套设置为 `model=gpt-6.1-sol`、`reasoning_effort=xhigh`，符合本次用户指定 |
| 核验坐标 | `/Users/ywang2397/.codex/sessions/2026/10/21/rollout-2026-10-21T21-50-05-01a15eb9-d721-7280-9ed7-cb0979a5ef99.jsonl` L8，`ordinal=7`，时间戳 `2026-10-21T13:50:15.784Z` |
| 会话 / turn ID | `01a15eb9-d721-7280-9ed7-cb0979a5ef99` / `01a15eb9-ec98-7931-8dcd-f8576a6052f8` |
| 执行方式 | 当前本地 Codex CLI 直接复核；同 rollout L1：`originator=codex_exec`、`cli_version=0.163.0`、`source=exec`；未另启模型、子代理或 fallback 轮次，报告无 fallback 输出标记 |
| 日期 / 时区 | 2026-10-21 / Asia/Shanghai |
| 写入范围 | 仅新增本报告；不修改正文、来源记录、registry、其他报告、计划、导航及本仓库构建产物 |

下列坐标对应本轮读取快照；SHA-256 按文件原始字节计算。

| 对象 | 行数 | SHA-256 |
|---|---:|---|
| [初审](batch-30-t08-04-codex-review.md) | 184 | `8ddaa6b84f0567564dd63023fafed2085b440d82c05ce436dbed4cbb3de7e621` |
| [第一轮复核](batch-30-t08-04-codex-recheck.md) | 120 | `cb73d1ba36b818dc009989c54d13c6069431896c66bcdc63030ea3bb06b26433` |
| [第二轮复核](batch-30-t08-04-codex-recheck-2.md) | 106 | `305a41d0b361d38041bb17df08bb21261fb91d7c05498a993231f45b6c501797` |
| [修订后正文](../../knowledge/08-reliability/silent-errors-and-integrity.md) | 221 | `4b9479e3cf5ce7c2defe4adcf3ebef9a75b9a5076631339c48a3caf71e9f29dd` |
| [来源与修订记录](batch-30-t08-04-sources.md) | 58 | `d9e2835fd8d6da7755b6b355889f9a0e5f4770603d4164850e69f31e832510c5` |
| [registry](../../sources/registry.yaml) | 7227 | `0e0defed4ec29acd3722f8f78dd4926b3e88441c7a48e59a4db96e0b976275b5` |

## 范围与方法

先读 `README.md`、`AGENTS.md`、写作指南、总目录和元数据 schema。只沿初审及两份复核报告对照 C02、C03、C05、C06、N10、N11 的关闭条件和剩余差距；此前已关闭项不重开，未重审整篇或兄弟篇。

定向重读上游：2203.08989v1 表 1、§5.2.1–§5.2.2、§6；OCP §5.4（印刷页 22 / 文件第 22 页）；PyTorch 2.6 testing 及固定 `clip_grad.py`、`adam.py`；DCGM 固定 `dcgm_fields.h` 全文及当前 user-guide 显存插件；RCCL 固定 tag README 与固定 commit 的输出实现。另打开 arXiv v1、Llama 3 v3 精确入口核对对象。GitHub 网页/raw 读取未成功的文件改由 GitHub 连接器按原 ref 读取；源码坐标按原文件计数。PDF 使用可检索文字，不声称完成图像独立核验；未执行上游诊断或训练命令。

**修订记录的实际边界**：提供的来源记录仍为 58 行，末节是“第二轮修订记录（复核后）”（L51–58），没有单列第三轮修订记录；其哈希亦与上一份复核所读相同。本文没有把不存在的第三轮自述作为证据，按当前正文与 registry 逐项核实。本轮的关闭只覆盖实际核到的修订。

## 指定未闭项逐项状态

| 编号 | 优先级 | 状态 | 对照剩余关闭条件的判断 |
|---|---|---|---|
| C02 | P2 | **CLOSED** | 正文 L88、L95–100 的共同分母、共同 70% 检出终点和扫描/部署时间继续分列；registry L7019 已改为两方法合并检出并集，消除了上一轮唯一剩余的分母矛盾，来源记录 L53 的同步声明现在与该 notes 一致。代价行结构问题仍由 N11 承载。 |
| C03 | P2 | **CLOSED** | 正文 L147 已将近零增量限定为直接复用训练已计算的 loss，另行梯度范数计算与下游评估的成本明确为未量化 unknown；L144–146 的结构/指纹/差分成本与原有误报边界仍在。满足上一轮剩余的成本条件要求；该行错列继续按 N11 判定，不重复计算为成本断言未修。 |
| C05 | P2 | **OPEN** | 正文 L171 新增了显存测试按 GPU 配置允许性、无配置默认不允许和最小分配条件，其余插件前提 unknown；L172 补了关闭校验时 `#wrong=N/A` 为未校验。上述原缺口已补，但 L171 的 ECC 字段名仍错误，三平台准确字段清单的总条件未全满足。仅余字段问题与 N10 同源，不另提出一套支持前提要求。 |
| C06 | P2 | **OPEN** | 正文 L20–23 已补四个依赖，RCCL README 完整 URL 已进入 registry L4789，Llama 3 两处正文入口已固定 v3；Adam、数值子页、ECC 深页等映射继续有效。但 DCGM 头文件完整 URL 仍未登记；arXiv v1 的新主入口虽进入 source_refs，正文两处仍用无版本 URL，尚未完成上一轮要求的固定入口接通。详见下表。 |
| N10 | P2 | **OPEN** | 正文 L171 仍为 `DCGM_FI_DEV_ECC_SB_ERROR` / `_DB_ERROR`，未采用固定源码中的真实宏名，也未删除错误示例。重新读取 2222 行头文件，两种完整名称均不存在；准确字段及原文件坐标见下文。 |
| N11 | P3 | **OPEN** | 正文 L98、L101 的两条“代价”行均在原三列表格之外，而且内容重复；L147 仍只有三个单元格，对应表头为四列，成本与误报没有各归其列。原结构关闭条件仍未满足。 |

## 关闭依据与剩余差距

### C02：共同分母已同步到登记

[2203.08989v1 表 1、§6.1–§6.3](https://arxiv.org/html/2203.08989v1#S6) 支持在所研究缺陷族的观察集合上比较共同与独有部分，并区分等价检出时间；[§5.2.2](https://arxiv.org/html/2203.08989v1#S5.SS2.SSS2) 的新 signature 扩展是另一终点。当前正文与 registry 已采用同一观察并集，保留研究范围和非通用召回率边界。上一轮所指“各方法实际检出的集合”已从该 notes 删除，C02 关闭；不因此关闭 N11。

### C03：成本限定满足，呈现问题另行保留

当前 L147 不再泛称任意 loss/梯度范数监控近零成本，而是限定直接复用既有 loss，另两类新增计算成本保持 unknown。固定 [PyTorch 2.6 clip_grad.py L82–99](https://github.com/pytorch/pytorch/blob/1eba9b3aa3c43f86f4a2c807ac8e12c4a7767340/torch/nn/utils/clip_grad.py#L82-L99) 可核范数与汇集计算；它不提供性能测量，本轮也不从中推导具体开销。[OCP §5.4](https://www.opencompute.org/documents/sdc-in-ai-ocp-whitepaper-final-pdf) 的非确定性混淆边界与正文所保留误报说明相容。上一轮已认可的属性/指纹拆分与其他类别不扩大重审；C03 关闭，四列对齐仍由 N11 处理。

### C05 / N10：支持前提已补，错误字段没有改

重新核对 [DCGM GPU Memory Plugin](https://docs.nvidia.com/datacenter/dcgm/latest/user-guide/dcgm-diagnostics.html#gpu-memory-plugin) 的 `is_allowed`、`minimum_allocation_percentage` 及 `DCGM_FR_MEMORY_MISMATCH`，当前 L171 新增的条件与该页相符，且仍区分 current user-guide 和固定 v3.3.9。AMD 的关闭/跳过解释与 [固定 README L175](https://github.com/ROCm/rocm-systems/blob/therock-10.1/projects/rccl-tests/README.md#L175)、[固定 util.cu L510–524](https://github.com/ROCm/rocm-systems/blob/7da43026e4f2ef7600433c38c820732f7a205d22/projects/rccl-tests/src/util.cu#L510-L524) 及[RCCL 主干](../../knowledge/03-communication/rccl-runtime-and-verification.md#rccl-tests-计时校验口径固定-tag-therock-101)一致。这些剩余子项满足，不要求补造支持矩阵或测试结果。

但 [dcgm_fields.h L758–778](https://github.com/NVIDIA/DCGM/blob/b0ec3c624ea21e688b0d93cf9b214ae0eeb6fe52/dcgmlib/dcgm_fields.h#L758-L778) 的实际宏为：`DCGM_FI_DEV_ECC_SBE_VOL_TOTAL`（L761，310）、`DCGM_FI_DEV_ECC_DBE_VOL_TOTAL`（L766，311）、`DCGM_FI_DEV_ECC_SBE_AGG_TOTAL`（L772，312）、`DCGM_FI_DEV_ECC_DBE_AGG_TOTAL`（L778，313）。本轮取得该文件 blob SHA `b87f87a8240ae03b81f6d4a22ab7e63d2c6dd2af`，全文检查仍无正文所举的两个完整名称。

**继续关闭条件**：按 N10 原条件使用真实且语义对应的字段名，或删除错误代码例子并保留准确可核记录。完成后即可复核 C05 的总条件及 N10；本轮不把同一字段错误扩张为新的独立发现。

### C06：依赖补齐不等于所有固定入口已接通

按完整 URL 逐字比较，当前正文为 **36 处外链、19 个唯一 URL**；24 处与本篇 source_refs 对应 registry 主 `url` 相等，纳入 notes 和许可 scope 的明确完整 URL 后为 **35/36 处**可精确映射。仅 GitHub 的 `#L…` 定位片段按同一文件处理；未按仓库前缀或相同 commit 推定文件已登记。

| 对象 / 正文位置 | 本轮结果 | 剩余要求 |
|---|---|---|
| Adam，L117、L218 | 对应来源 ID 已加入 source_refs；文件完整 URL 已在 registry L473 | 该子项关闭 |
| RCCL README，L172 | 对应来源 ID 已加入；精确文件 URL 已在 registry L4789 | 该子项关闭 |
| Llama 3，L184、L216 | 两处均已改为 `abs/2407.21783v3`，与登记主入口一致；[上游 v3](https://arxiv.org/abs/2407.21783v3) 的对象身份可核 | 该子项关闭 |
| DCGM 头文件，L171 | 来源 ID 已加入，但 registry 对应条目仍只登记仓库树；notes L610 没有该完整文件 URL。全 registry 亦未找到同一完整 URL | 将实际采用的固定文件建立精确映射；当前唯一完全未映射外链就是这一处 |
| arXiv v1，L107、L215 | `src.arxiv.sdc-llm-training-2502-v1` 已加入依赖；两处正文仍为 `abs/2502.12340`，而新登记主入口为 `abs/2502.12340v1`。无版本入口已有许可 scope 映射，故不计作完全未登记 | 接通明确采用的固定 v1 入口，或在新条目建立这两个完整入口的明确技术文件映射；现有许可 URL 不代替上一轮要求的固定附录入口接通 |

[arXiv v1 原页](https://arxiv.org/abs/2502.12340v1) 可核研究身份，当前显示的提交历史仅 v1；本轮未把无版本链接判为读到了另一篇或已发生版本漂移。剩余是本次关闭条件明确要求的入口追溯，不能将机械映射的 35/36 解释为固定入口条件也全部通过。数值子页、ECC 支持深页和 msprobe 许可的此前有效映射继续保留。

### N11：两处原结构问题均仍存在

正文主表 L90–96 后有空行；L98 的“代价”行没有表头/分隔行，不属于原主表。L100 的普通段落后又出现同义的 L101“代价”行，既未恢复两策略的表头对应，又重复了同一信息。方法表 L138 的四列依次为“方法 / 机制与来源 / 覆盖与成本 / 已知假阴性/误报与盲区”；L147 原 Markdown 实际仅三格：任务质量、含成本的机制长句、误报说明，最后一列缺失。

**继续关闭条件**：恢复代价信息与两策略的明确对应并去除重复，使任务质量行与四列表头对齐；保留本轮已满足的共同分母、时间终点、成本条件和 unknown。这里不要求改写其他方法或补做硬件验证。

## 新发现

没有发现需要从 N20 起另列的独立新问题。重复“代价”行属于 N11 同一表格结构问题的延续，成本限定修订本身按 C03 已满足；不重复记项。

## 结构检查与写入边界

为遵守仅新增报告的限制，将当前 tracked/untracked 文件及已有 `build/` 文件复制到临时目录，在副本使用项目既有 Python 环境执行 `make check`、`make build`，均退出 0：**126 content entries / 575 sources**；构建产物仅生成于副本。本报告加入副本后亦执行相同检查。检查覆盖结构与本地文件链接，不覆盖远程内容、技术正确性、N10 的宏名或 N11 的表格列结构。

本轮唯一仓库写入为本报告；既有正文、来源、registry 和其他批次报告的未提交改动不计为本会话成果。交付前复比 666 个既有文件的哈希，未发现本轮改写或删除；本报告的本地链接检查通过。未修改 `src/kb/`，未运行 `make test`；未执行设备诊断、压力测试、故障注入、训练或生产动作。正文仍为 `draft / generic / source_checked`，模型复核不升级为真实环境验证。

## 结论

**2/6 CLOSED：C02、C03；OPEN：C05、C06、N10、N11。无新增 N20 项。T08-04 仍需作者修订后定向复核，暂不通过；模型审阅不替代真实环境验证。**
