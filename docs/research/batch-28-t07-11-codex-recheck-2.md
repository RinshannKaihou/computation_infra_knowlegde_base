# Batch 28 · T07-11 第二轮定向复核报告

## 会话元数据与结论

| 项目 | 记录 |
|---|---|
| 角色与范围 | 承接[第一轮定向复核](batch-28-t07-11-codex-recheck.md)，仅复核 C02/C04/C06/C07/C08/C09/C10/C11 的剩余条件及这些修订引入的问题；本会话未编写或修订被审正文 |
| 实际执行模型 / 推理档位 | `gpt-6.1-sol / xhigh` |
| 模型核验 | 读取 `CODEX_THREAD_ID` 对应本地 JSONL 的 `session_meta` 与全部 `turn_context`；实际唯一组合为 `model=gpt-6.1-sol`、`effort=xhigh`，与 `collaboration_mode.settings` 一致；assistant 输出未检出 `[frontier_llm]` 回退标记；未另启模型或子代理 |
| 本轮会话 ID | `01a15d7a-8573-7991-8e43-5e4ba5511841` |
| 第一轮复核会话 ID | `01a15d6c-b144-7ab0-80ee-7ab332fb3e5b` |
| 执行方式 | 本地 Codex CLI；`originator=codex_exec`、`source=exec`、CLI 0.163.0；静态定向复核 |
| 日期 / 时区 | 2026-10-21 / Asia/Shanghai |
| 工作目录 | `/Users/ywang2397/work/AI_reliability_knowledge_base` |
| 修订后正文 | [gpu-inference-oom-triage.md](../../knowledge/07-inference/gpu-inference-oom-triage.md)，124 行 |
| 用户提供的正文 SHA-256 | `c1acf97a8cfb4bec099b1d29a813d83b7c85f3ef47904bdb4690bbbf0754b31e` |
| 独立计算的正文 SHA-256 | `c1acf97a8cfb4bec099b1d29a813d83b7c85f3ef47904bdb4690bbbf0754b31e`，**匹配** |
| 写入范围 | 仅新增本报告；检查和构建在含本报告的临时源码副本执行，不改正文、来源记录、registry、历史报告或工作区构建产物 |

**结论：本轮暂不通过。指定的 8 个 OPEN 项中，CLOSED=6（C02、C07、C08、C09、C10、C11），OPEN=2（C04、C06，均沿用原 P2）。新增 N01 · P3 · OPEN，为恢复步骤的编号指向错误。** C01/C03/C05 沿用第一轮 CLOSED，不重审、不重新背书；原 C 项累计为 9 CLOSED / 2 OPEN，新增项另计。

C04 的正文和现行主张表已改对，仅来源文件的旧修订回应仍保留反向解释且未明确撤回；C06 的 hipBLAS 边界已补，尚缺取证统计、单位与窗口的实际平台映射。两项都不要求为关闭文档问题执行引擎或硬件实验。

以下行号绑定本轮文件指纹；上游源码坐标使用固定 commit 原文件行号。

| 关联文件 | 本轮 SHA-256 |
|---|---|
| [作者来源记录](batch-28-t07-11-sources.md) | `9da52b5530f1bbb6d595686e59294bc2e842b2946bf17cf4be9ab4780ca80eb3` |
| [GPU 内存证据](../../knowledge/02-software-stack/gpu-memory-oom-evidence.md) | `d841a8e780f3c8e28b0faf2815903e970ba746bb27caa116da74dd9f1e4dfbdb` |
| [昇腾内存证据](../../knowledge/02-software-stack/ascend-memory-oom-evidence.md) | `b1c3e6cfceb9625d109a93629ce13d2ffa8205d58f17e5f2efae58155b6c2869` |
| [发布与恢复](../../knowledge/07-inference/release-and-recovery.md) | `c5018d2c94701777f3829a54a6ad62b24660fb004ec25eba608fa48a72807eb4` |
| [执行与 KV cache](../../knowledge/07-inference/execution-and-kv-cache.md) | `9d6f5ec44734fca749200c00019cd05f02250e528ce6d47fc1709f06396aa3f8` |
| [来源登记表](../../sources/registry.yaml) | `a87cd520ba611ef258ab7310359280b192b5d76721265ce4de3876e0950ab605` |

## 复核方法与证据边界

先读 `README.md`、`docs/authoring-guide.md`、`AGENTS.md`、`content-outline.md`、元数据 schema 和上一轮逐项关闭条件。逐行对照修订正文、现行主张—来源表、两轮作者回应、unknown 清单及 `src.vllm.inference-v0-14` 的 Batch 28 notes；关联页仅检查本次依赖的字段表、窗口、所有者和导航条件。

本轮尝试通过网页工具打开 PyTorch HIP 2.6 的 hipBLAS 精确节与 AMD SMI docs-10.1.0 CLI 精确页，调用整体返回 HTTP 429；GitHub `fetch_file` 返回工具不可用；备用只读 HTTP 请求固定 `gpu_worker.py` 因域名解析失败未取得文件。因此本轮采用既存缓存原文独立重读及指纹比对，**不记为本轮重新下载远端证据**。网络失败本身不作为作者错误；AMD SMI CLI 本轮未独立重取全文，现场字段也未验证。

vLLM 缓存根目录为 `/tmp/vllm-b17039bccc17b94a2ea107272ad7bc93508708df/`，固定 commit 为 `b17039bccc17b94a2ea107272ad7bc93508708df`。本轮独立计算下表指纹，与第一轮记录一致；未重新解析远端 tag 或下载源码归档。

| 上游文件 | SHA-256 前 16 位 | 本轮读取范围 |
|---|---|---|
| `vllm/v1/worker/utils.py` | `c0758a66a105e72e` | L253–273，启动预算与调参方向 |
| `vllm/v1/worker/gpu_worker.py` | `eb33b5f2bd389ac3` | L295–343，手工 KV 预算、profiling 断言与自动预算 |
| `vllm/v1/core/kv_cache_utils.py` | `208abc23e1cbaebe` | L609–645，两种 KV 容量失败建议 |
| `vllm/v1/worker/gpu_model_runner.py` | `7eaa9eb78cb99f9f` | L4281–4313、L4693–4757，批规模参与 dummy/profile |
| `vllm/platforms/rocm.py` | `b7fcec9a5263d8f9` | L430–446，auto worker 前提 |
| `docs/configuration/conserving_memory.md` | `895bc42beb0ff505` | 全文，候选范围、TP I/O 注记及无 gmu 条目 |
| `docs/configuration/optimization.md` | `b3aac342f2435e22` | L1–38，抢占与 gmu 调整依据 |
| `docs/getting_started/installation/gpu.rocm.inc.md` | `3f0c7129c7e08347` | L1–28，ROCm/torch 支持下界与 wheel 边界 |

HIP 文档使用 `/tmp/b24-t063-s3.AfgWGe/hip-2.6.html`，独立计算 SHA-256 为 `c544cb55f21a9578a4239114ef5b905286e1b1a763c1f2280a9ef2a2ead522f8`，与第一轮一致。读取接口复用、Checking for HIP、Memory management 与 hipBLAS workspaces 小节；2.6 是语义资料样板，不与 vLLM ROCm 的 torch 2.8+ 要求合成已核部署组合。

## 8 个 OPEN 项逐项判定

| 编号 / 原优先级 | 判定 | 理由与定位 |
|---|---|---|
| C02 · P2 | **CLOSED** | 正文 L52 已删除“改并发救不了它”，明确在线到达并发不参与 request_memory，而引擎批规模参与 dummy/profile。L76 分开①启动空闲不足（降 gmu/减他进程）、③ profile 规模、④非正预算（错误仅建议增 gmu）与单请求所需 KV 超可用预算（增 gmu/降 `max_model_len`），与 utils L262–270、runner L4281–4308、KV 检查 L615–642 一致。手工 `kv_cache_memory_bytes` 路径明确核对指定值与实际空闲量，增 gmu 不扩大指定值，且自动公式不覆盖该路径，符合 worker L295–313。来源记录 L60 对应。 |
| C04 · P2 | **OPEN** | 正文 L76、来源表 L23 和本轮补充回应 L61 已正确写为 R≥G 失败、R<G 通过，并保留增加占用不被检出、通过不证明无干扰。但来源记录 L49 仍写“只捕获他进程释放且未抵消增长的形态”，方向仍反，未标为已被替代。第一轮明确要求同步更正旧回应（原 L45，现 L49），仅新增 L61 不能消除此处矛盾。正文部分已满足，剩余仅为来源回应更正或明确撤回。 |
| C06 · P2 | **OPEN** | 正文 L90 已写出 handle＋stream、持续持有及专门清理接口/配置项，符合 HIP 2.6 精确节；MIOpen/AITER 仍单列 unknown。L95 也已加入按 AMD SMI 版本核对字段名、不得直接对齐数值的限制。但 L91 声称表含统计、单位、身份、backend、重置/同步窗口与失败处置，L92–96 实际仅有“采集 API / 进程显存 / 整卡口径”三行；`torch.cuda.memory_*` 与“同名接口复用”仍未落实这些列的 CUDA/HIP 支持映射。详见下节；不要求在目标 HIP 构建补造已验证值。 |
| C07 · P2 | **CLOSED** | 来源表 L30 已撤换全局清空承诺，明确现行口径为“已终止所有者的本地状态不自动继承”，并分别核对外部/offload、远端 KV、旧 frontend 请求、重试 attempt 与已提交输出。与正文 L82、发布恢复页 L76–77 及执行/KV 页的缓存层级/身份边界一致，满足第一轮仅余的来源表同步条件。 |
| C08 · P2 | **CLOSED** | 正文 L82 的③已补发起终止、等待退出、预登记时限；到期未退或成员退出不完整时停止清理与重建、维持隔离并记录影响范围。L112 明确未知终态旧请求须受控处置（隔离、禁用未经验证的复用、控制透明重试），仅记录 unknown 不满足接流门；仍须同时满足残留、身份、ready、质量、SLO/错误与稳定窗。原剩余条件已落实。③末尾新出现的步骤编号错误单列 N01，不否定已明确写出的停止重建要求。 |
| C09 · P3 | **CLOSED** | 正文 L81、来源表 L26 与 registry L536 的 Batch 28 notes 均明确 conserving_memory 无 gmu 条目，gmu 依据归 utils/KV 错误建议与 optimization 抢占节。候选范围、TP 的读取 I/O 注记、本库单因素验证方法、多模态及 CPU RAM 边界保留；来源表主张列含 KV L615–642，虽精确位置列未重复该坐标，仍可定位，不据此继续开放。 |
| C10 · P3 | **CLOSED** | 来源记录 L34–42 的实际 unknown 清单现为九项；前六项逐一覆盖正文 L124 的部署组合、HIP 选项/backend/fork 差异、capture 分配路径、目标真实峰值、外部缓存/取消链、ROCm 引擎行为/案例，另保留 NVIDIA 公开案例未取得、Ascend/MindIE 不适用和未运行引擎/负载的限制。没有把既有登记或修订摘要当成本轮远端重新取回证据。 |
| C11 · P3 | **CLOSED** | 正文 L45 已在 NPU 字段不迁移的说明处直接链接 `ascend-memory-oom-evidence.md`，并与 GPU 内存证据链接并列。目标存在，stable ID 不变；本轮抽查正文 24 处本地链接、12 个唯一本地目标均存在。没有复制或迁移 NPU API/账户说明。 |

## 两项剩余条件

### C04：来源旧回应的反向解释尚未撤回

**位置：来源记录 L49（“初审修订轮”C04）；已正确的对应位置为正文 L76、来源表 L23、本轮补充 L61。**

固定 [gpu_worker.py L329–339](https://github.com/vllm-project/vllm/blob/b17039bccc17b94a2ea107272ad7bc93508708df/vllm/v1/worker/gpu_worker.py#L329-L339)要求初始 free 严格大于 profile 后 free。沿用第一轮的简化变量（暂不计其他变化），终值＝初值−G＋R；未抵消增长即 R<G，终值较小，断言通过。L49 却仍把这个形态写成断言捕获对象。

“初审修订轮”标题可标识发生时间，但没有明确告诉读者该条解释已撤回；L61 的新说明也未指向或标注取代 L49。这里不是要求重写已归档的历史复核报告，而是完成第一轮明确要求的同一作者来源文件内部更正。

**最小关闭条件：** 将 L49 的反向解释改对；或保留旧文并逐条标注“错误旧解释，已由本轮 C04/L61 取代”，使其不再被当作有效回应。保留正确比较式和“增加占用不检出 / 通过不证明无干扰”，无需再改正文、重复实验或扩大复核范围。

### C06：三行概览尚未落实所称的字段映射

**位置：正文 L91–96；复用目标为 [GPU 内存证据](../../knowledge/02-software-stack/gpu-memory-oom-evidence.md) L102–126。**

本轮已满足 hipBLAS 部分：[HIP 2.6 hipBLAS workspaces](https://docs.pytorch.org/docs/2.6/notes/hip.html#hipblas-workspaces)支持按 handle/stream 组合按需分配、持续持有、专门清理接口与配置项；没有要求在正文执行这些接口，也不要求补未核的 MIOpen/AITER 行为。

剩余是字段结构，不能仅用“表列含……”的说明代替实际映射。现有三行不能让填写者确定以下各项应落在哪种支持状态：

| 第一轮已要求的列组 | 本轮已出现的材料 | 仍缺的映射 |
|---|---|---|
| allocated/reserved 的 current/peak、memory_stats 细项与计数器、snapshot | L66 通用统计表、L90 接口名和 L94 通配接口 | 哪些 HIP 基础语义有 2.6 文档支持；哪些具体键/限制须在目标构建重核，而非把通用表整体视为 HIP 已核 |
| 字节单位、SMI 单位与换算、来源工具 | L91 枚举了单位；L95 列进程字段 | 数值来源工具与单位如何记录；CUDA `usedGpuMemory` 属所引 `list_gpu_processes` 的 pynvml/NVML 分支，不能仅以“SMI”替代其来源口径；CLI 字段和单位另按版本核对 |
| PID/rank/设备身份、实际 backend | L91 枚举了身份和 backend，L94 目标待核列概括选项/fork | 哪些共用身份列可直接沿用、哪些可见设备映射/API/backend 在目标 HIP 构建待核 |
| 峰值重置、累计计数器、同步窗口、字段不支持/查询失败 | 链接 02 域记录表及 F0/F1/F2，L91 声称含记录方法 | 哪些窗口规则是通用记录约束；哪些 reset/backend 语义只由 CUDA native 证据支持；HIP 未核或查询失败时应如何填 unknown/失败状态并排除比较 |

[HIP 2.6 Memory management](https://docs.pytorch.org/docs/2.6/notes/hip.html#memory-management)已明确支持张量 allocated/max allocated、allocator reserved/max reserved、memory_stats 和 memory_snapshot，不能让它们继续只落在“同名接口复用”概括中。另一方面，02 域 L126 明确其 reset/backend 证据是 native 统计实现，不推为所有 backend 保证；通用表链接本身不能授予目标 HIP 构建同样的全部统计与重置语义。

**最小关闭条件：** 沿用现有 CUDA/HIP 2.6/目标 HIP 待核三列，按上述列组补行或提供等价填写规则。明确当前值/峰值/计数器和单位、身份、backend、重置/同步窗口、缺失/查询失败的记录处置；可直接引用 02 域表和窗口，注明共同记录列及其适用限制，无需复制全文。已获 HIP 2.6 基础语义填入支持列，未核字段/选项/实际 backend 填待核，避免将未知记成 0 或使用无意义统计比较；目标硬件读数和完整部署组合仍可 unknown。

## 新发现

### N01 · P3 · OPEN：退出失败分支的步骤编号与实际动作不符

- **位置**：正文 L82，③的新增末句“不进入⑤⑥的清理与再启动”。
- **证据**：同一行实际编号为⑤清理、⑥同步采样对账、⑦同身份重启；⑥不是再启动。该句是为修补 C08 新增的控制流交叉引用，属于本轮修订引入的编辑错误。
- **影响**：停止重建和维持隔离的动作已明确，故没有据此重开 C08；但按编号执行会将采样与重启位置混淆，降低异常分支的可操作性。
- **最小关闭条件**：将交叉引用改为与动作一致的⑤/⑦，或写清“不得进入⑤清理与⑦重启；⑥取证采样是否继续按隔离条件决定”。不需执行终止或清理操作。

除 N01 外，未发现需独立编号的新问题。C04 的遗留旧回应和 C06 的映射不完整仍归原发现，不另立 N 编号。C02 的预算子分支、C07 的所有者划分、C08 的退出失败/未知终态门禁、C09 的来源归属、C10 的缺口清单及 C11 的直接链接均按本轮剩余条件验收；不扩大到已 CLOSED 的 C01/C03/C05。

## 校验与写入范围

含本报告的临时源码副本中，`make check` 与 `make build` 均通过：**117 content entries / 553 sources**，生成 `build/catalog.md` 与 `build/catalog.json`。构建清单内本篇 SHA-256 与用户提供值一致，`procedure`、`draft / source_checked`、平台及引用元数据与被审正文一致。副本保留原有 `build/` 供既有链接检查，再由构建重建；使用仓库现有虚拟环境，未安装依赖，未修改检查规则或 `src/kb/`，未新增测试。

写报告前记录了 609 个既有文件的指纹（排除 `.git`、虚拟环境及解释器/测试缓存）。随后核对无既有文件改写或删除；除本报告外，工作区并发新增了 `batch-28-t00-02-codex-recheck.md`、`batch-28-t07-09-codex-recheck-3.md`、`batch-28-t07-10-codex-recheck-2.md` 三份报告。本会话未写入、覆盖或回滚这些文件；本轮写入动作仅针对指定报告，工作区既有构建产物未改写。

检查与构建只验证结构、引用和生成清单，不证明技术结论、远端内容或硬件适用性。正文继续保持 `draft / source_checked`；本轮未启动引擎、运行 GPU/NPU 工具、构造负载、复现 OOM、终止服务或清理缓存。
