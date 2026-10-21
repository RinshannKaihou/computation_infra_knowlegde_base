# Batch 28 · T07-11 第三轮定向复核报告

## 会话元数据与结论

| 项目 | 记录 |
|---|---|
| 角色与范围 | 承接[第二轮定向复核](batch-28-t07-11-codex-recheck-2.md)，仅复核 C04/C06 剩余条件、N01，以及这些修订引入的问题；本会话未编写或修订被审正文 |
| 实际执行模型 / 推理档位 | `gpt-6.1-sol / xhigh` |
| 模型核验 | 读取 `CODEX_THREAD_ID` 对应本地 JSONL 的 `session_meta` 与全部 `turn_context`；唯一模型/档位组合为 `model=gpt-6.1-sol`、`effort=xhigh`，与 `collaboration_mode.settings` 一致；assistant 文本未发现回退标记；未另启模型或子代理 |
| 本轮会话 ID | `01a15d85-fb23-7412-b59b-18072431a8c3` |
| 第二轮复核会话 ID | `01a15d7a-8573-7991-8e43-5e4ba5511841` |
| 执行方式 | 本地 Codex CLI；`originator=codex_exec`、`source=exec`、CLI 0.163.0；静态定向复核 |
| 日期 / 时区 | 2026-10-21 / Asia/Shanghai |
| 工作目录 | `/Users/ywang2397/work/AI_reliability_knowledge_base` |
| 修订后正文 | [gpu-inference-oom-triage.md](../../knowledge/07-inference/gpu-inference-oom-triage.md)，129 行 |
| 用户提供的正文 SHA-256 | `a37ecd6fa344593f59a6745f134def4eec21b98435d77cd6bab7380c12a58ab7` |
| 独立计算的正文 SHA-256 | `a37ecd6fa344593f59a6745f134def4eec21b98435d77cd6bab7380c12a58ab7`，**匹配** |
| 写入范围 | 仅新增本报告；检查和构建在含本报告的临时源码副本执行，不改正文、来源记录、registry、历史报告或工作区构建产物 |

**结论：本轮暂不通过。C04＝CLOSED，C06＝OPEN（沿用 P2），N01＝CLOSED。** C06 的字段结构及大部分支持边界已经落实，但新表将 CUDA backend 的判据写成 allocator 配置，未保留“实际 backend 与请求配置分别记录”的必要区别。该问题归原 C06，不另建发现编号。其余已 CLOSED 项沿用前轮结论，不重新审查或背书；原 C 项累计为 10 CLOSED / 1 OPEN，N01 已关闭。

以下仓库行号绑定本轮文件指纹；GitHub 行号使用固定 commit 原文件坐标，不使用网页工具转换后的行号。

| 关联文件 | 本轮 SHA-256 |
|---|---|
| [作者来源记录](batch-28-t07-11-sources.md) | `00a03dc64b8caa2a3f690a061a1a215eed26864ef16bb9c991bb705662d41f00` |
| [GPU 内存证据](../../knowledge/02-software-stack/gpu-memory-oom-evidence.md) | `d841a8e780f3c8e28b0faf2815903e970ba746bb27caa116da74dd9f1e4dfbdb` |
| [第二轮复核报告](batch-28-t07-11-codex-recheck-2.md) | `2c0623d5ed36369b604128ae5628636a566a5e4839d9e4a8b257774027f71062` |

## 逐项判定

| 编号 / 优先级 | 判定 | 理由与定位 |
|---|---|---|
| C04 · P2 | **CLOSED** | 来源记录 L49 已就地标注“错误旧解释，已由复核轮取代”，指向同文件“复核第一轮修订·补充”C04，并明确 R≥G 失败、R<G 通过；L61 保留现行解释，L23 与正文 L76 一致。旧回应不再作为有效解释。正文继续保留增加占用不由该断言检出、通过不证明无干扰的边界，满足第二轮仅余的撤回条件。 |
| C06 · P2 | **OPEN** | 正文 L92–101 已从三行概览扩为八个列组，HIP 2.6 明列的基础内存接口已填支持列，NVML/amdsmi 来源、身份、native reset 限制和失败处置均已补。但 L95 CUDA 栏新增“backend 以 allocator 配置为准”，与所复用的 02 域 L116 的“已证实际 backend＋请求配置”分列要求冲突；填写者仍可能以配置值代替实际 backend。详见下节；不要求取得目标硬件读数或消除已明确记录的 HIP unknown。 |
| N01 · P3 | **CLOSED** | 正文 L82 的③末句现为“不进入⑤对象清理、⑥采样对账与⑦再启动”，与同一恢复序列⑤清理、⑥采样、⑦重启逐项对应。到期未退或退出不完整时停止后续恢复序列、维持隔离的条件仍明确；没有重新引入编号与动作错配。来源记录 L73 同步。 |

C04 的比较关系也经静态重读确认：[固定 gpu_worker.py L329–339](https://github.com/vllm-project/vllm/blob/b17039bccc17b94a2ea107272ad7bc93508708df/vllm/v1/worker/gpu_worker.py#L329-L339)要求初始 free 严格大于结束 free。在前两轮采用的简化变量及忽略其他变化的条件下，结束 free＝初始 free−G＋R，因此 R≥G 失败、R<G 通过。本轮未将代数关系记为现场实验。

## C06：已满足部分与唯一剩余条件

本轮接受以下修订，不继续以“没有完整表格”或“缺少目标 HIP 硬件验证”为由开放 C06：

| 第二轮要求的列组 | 本轮验收结果 |
|---|---|
| current/peak、统计细项与计数器、snapshot | L94 已分出 HIP 2.6 明确支持的 allocated/max allocated、reserved/max reserved、memory_stats、memory_snapshot；具体键与 backend 限制留在目标构建待核列。与 [HIP 2.6 Memory management](https://docs.pytorch.org/docs/2.6/notes/hip.html#memory-management)一致。 |
| 单位、来源工具、进程显存与整卡口径 | L96–98 已给统一记录单位与随来源记录换算的规则，明确 `usedGpuMemory` 来自 pynvml/NVML、`vram_mem` 来自 list_gpu_processes 的 ROCm/amdsmi 分支；CLI 字段和单位按版本待核，不直接对齐数值。来源分支可由 [PyTorch 2.6 list_gpu_processes](https://docs.pytorch.org/docs/2.6/_modules/torch/cuda/memory.html#list_gpu_processes)复查。 |
| PID/rank/设备身份 | L99 明确共同身份列可沿用，目标可见设备映射仍待核；结合 02 域 L104–110 可落到 hostname、PID/rank、UUID/BDF 与可见索引映射。 |
| 峰值重置、累计计数器与窗口 | L100 明确 CUDA reset 证据限 native，不推为所有 backend；链接的 02 域 L126 给出峰值/累计计数器与 F0/F1/F2 顺序。HIP 同名接口的存在性可结合接口复用说明与 2.6 模块定义理解，目标 reset/backend 语义仍为待核，不据接口名推定所有 backend 语义一致。 |
| 不支持、未核与查询失败 | L91、L101 明确 unknown、失败状态、排除比较及不填 0；这是共用记录约束，目标 CLI 替代路径仍可待核。 |

L90 的 hipBLAS handle/stream、持续持有和专门清理接口边界与 [HIP 2.6 hipBLAS workspaces](https://docs.pytorch.org/docs/2.6/notes/hip.html#hipblas-workspaces)一致；L102 的 PyTorch 2.6 语义参考与 vLLM ROCm torch 2.8+ 部署要求继续分线。这些前轮已接受的条件没有回退。

**唯一剩余位置：正文 L95，CUDA 栏“backend 以 allocator 配置为准”。** 本项从第一轮起就要求记录实际 backend；第二轮的剩余条件也明确包括实际 backend 及其统计适用限制。所复用的 [02 域记录表](../../knowledge/02-software-stack/gpu-memory-oom-evidence.md) L116 已写明：实际 backend 用 `get_allocator_backend()` 取证，同时保留请求配置的 env 快照；请求配置未必等于初始化后的实际生效值。新表不能再用“以配置为准”覆盖这个区别。

[PyTorch 2.6 get_allocator_backend 定义](https://docs.pytorch.org/docs/2.6/_modules/torch/cuda/memory.html#get_allocator_backend)查询 active backend 并返回底层查询值，而非直接返回环境变量文本；[CUDA 2.6 Memory management](https://docs.pytorch.org/docs/2.6/notes/cuda.html#cuda-memory-management)也要求按 backend 判断统计是否有意义。这支持采用“运行中实际 backend 的查询结果＋单列请求配置”的记录方式。这里的影响是取证和比较口径可能选错，并非声称本轮观察到了配置不一致。

**最小关闭条件：** 仅需将 L95 CUDA 栏改为与 02 域 L116 一致的填写规则，例如“实际 backend 记录 `get_allocator_backend()` 查询结果；请求配置（env/启动参数）另列，不能据请求配置推定已生效；查询失败时实际 backend 记 unknown，排除依赖其语义的统计比较”。保留 HIP 实际 backend/选项/fork 与 reset 语义待目标构建核对。无需执行 GPU 命令、补造读数、复制 02 域全文或重新开放其余列组。

## 新问题检查与证据边界

**新增独立发现：0。** 新表的 backend 表述属于原 C06 所要求的同一字段及适用边界，已纳入其剩余条件，不重复编号。C04 撤回标注未引入新的断言方向错误；N01 修订后的编号与动作一致。没有因③停止后续恢复序列而推断其禁止①保存现场或独立诊断取证，也未扩大到已关闭项的全面复审。

本轮先读 `README.md`、`docs/authoring-guide.md`、`AGENTS.md`、`content-outline.md`、schema 和第二轮关闭条件。远端成功读取 PyTorch HIP 2.6、CUDA 2.6、2.6 memory 模块页面及固定 commit 的 vLLM raw 文件；GitHub blob 页面和 PyTorch 固定 commit raw 文件读取失败，后者未记为本轮远端重取成功。2.6 模块网页仅作为版本化文档佐证，不宣称已与固定 commit 原文件逐字节相等。

vLLM 原文件行号另以既存 `/tmp/vllm-b17039bccc17b94a2ea107272ad7bc93508708df/vllm/v1/worker/gpu_worker.py` 核对 L329–339，独立 SHA-256 为 `eb33b5f2bd389ac32785772ba596e5aecfaaaec281e3edfd804b993b4b1d7495`，与第二轮前缀一致。未重新解析 tag 或下载完整源码归档。

AMD SMI docs-10.1.0 CLI URL 本轮可打开，但返回页面标题为 AMD SMI 27.1.0；因此不将本次网页响应当作固定 10.1.0 CLI 全文已重新验证的证据，不据此改写登记或推断现场字段。新表已经把现场字段/版本与数值可比性保留为待核，这不是本轮新增的正文错误。

正文继续保持 `draft / source_checked`。本轮未启动引擎、运行 GPU/NPU 采集工具、构造负载、复现 OOM、终止服务或清理缓存；不宣称部署组合、修复或恢复验证成功。

## 校验与写入范围

含本报告的临时源码副本中，`make check` 与 `make build` 均通过：**117 content entries / 553 sources**，生成 `build/catalog.md` 与 `build/catalog.json`。构建清单内本篇 SHA-256 与用户提供值一致；`procedure`、`draft / source_checked`、平台及引用元数据与修订正文一致。副本保留既有 `build/` 供本地链接检查，再由构建重建；使用仓库现有虚拟环境，未安装依赖、修改检查规则或 `src/kb/`，未新增测试。工作区构建产物未改写。

写报告前记录了 613 个既有文件的指纹（排除 `.git`、虚拟环境和解释器/测试缓存）。末次核对没有既有文件改写或删除；除本报告外，会话期间并发新增了 `docs/research/batch-28-t00-02-codex-recheck-2.md`。本会话未写入、覆盖或回滚该文件；本轮写入动作仅针对本报告。修订正文及上表三个关联文件末次指纹保持一致。

结构检查与构建只验证结构、本地引用和生成清单，不证明技术结论、远端版本不可变性或硬件适用性。C06 须完成上述小范围修订并经定向复核后，才能宣布本轮所涉问题全部关闭。
