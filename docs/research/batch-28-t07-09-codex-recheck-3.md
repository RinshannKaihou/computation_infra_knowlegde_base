# Batch 28 · T07-09 第三轮定向复核报告

## 会话元数据与结论

| 项目 | 记录 |
|---|---|
| 角色与范围 | 独立审阅者，仅复核[第二轮报告](batch-28-t07-09-codex-recheck-2.md)剩余 OPEN 项 C02 的正文残留断言及本次修订引入的问题；未编写或修改被审正文 |
| 实际执行模型 / 档位 | `gpt-6.1-sol / xhigh` |
| 模型核验 | 读取 `CODEX_THREAD_ID` 对应本地会话 JSONL，第 8 行 `turn_context`（`2026-10-21T08:02:17.346Z`）实见 `model=gpt-6.1-sol`、`effort=xhigh`，与 `collaboration_mode.settings` 一致；本轮未另启模型、审阅 CLI 子进程或子代理，未观察到 fallback 标记 |
| 会话 ID | `01a15d7b-2607-79a1-b323-dc62059fa231` |
| 执行方式 | 本地 Codex CLI，`originator=codex_exec`、`cli_version=0.163.0`；直接读取工作区文件及既有固定快照缓存 |
| 日期 / 时区 | 2026-10-21 / Asia/Shanghai |
| 工作目录 | `/Users/ywang2397/work/AI_reliability_knowledge_base` |
| 修订正文 | [capacity-and-autoscaling.md](../../knowledge/07-inference/capacity-and-autoscaling.md)，115 行；下文正文行号对应此版 |
| 作者提交的正文 SHA-256 | `7092dd3156e1646179aaf88378bc24f31523ee67da14aa6728ff660180ee584f` |
| 独立计算的正文 SHA-256 | `7092dd3156e1646179aaf88378bc24f31523ee67da14aa6728ff660180ee584f`，**匹配** |
| 写入范围 | 仅新增本报告；正文、来源记录、registry、任务账本与审核状态均未修改 |

**结论：C02（原 P2）CLOSED。本轮 CLOSED=1、OPEN=0；定向范围内未发现新问题，无新增 N02 或后续编号。**

正文 L102 已消除“实现细节未核，仅引用教程口径”的残留断言，与正文 L68/L103/L112 及来源记录现行表述一致，满足第二轮列出的最小关闭条件。T07-09 的既有发现至此全部关闭，在既有审阅范围内通过。其余已关闭项沿用前轮状态，本轮不重审；该结论不构成 Batch 28 整批验收或硬件验证。

## 方法与证据边界

按仓库 `AGENTS.md`、[README](../../README.md)、[写作指南](../authoring-guide.md)及[内容总目录](../../content-outline.md)执行，读取元数据 schema 与 T07-09 任务边界。重读前两轮报告、当前正文、[来源记录](batch-28-t07-09-sources.md)的相关主张与 unknown 清单，以及 registry 的相关来源条目；以实际文件为判据。

为核验相对第二轮的改动范围，在内存中仅将当前正文 L102 换回第二轮报告所录旧句，重新计算得到 SHA-256 `2e2bff94edb430df2fb1183ea3f5c7086a8b7ca4d5dd23b7641561c52bdb217c`，与第二轮被审正文哈希完全一致。因此本次提交的正文修订仅涉及 L102；未将与本项无关的既有内容纳入第三轮重审。

本轮尝试打开固定 GitHub 页面，网页工具返回 HTTP 429，未取得新的远端正文。实际证据为**重新读取既有固定快照缓存并核验其字节摘要**，未以历史报告结论代替源码核对，也未把缓存读取写成本轮远端取回。

| 固定来源 / 本轮读取范围 | 缓存位置 | 本轮 SHA-256 |
|---|---|---|
| vLLM `b17039bccc17b94a2ea107272ad7bc93508708df`，`gpu_worker.py` L109–155 | `/tmp/b28/vllm/gpu_worker.py` | `eb33b5f2bd389ac32785772ba596e5aecfaaaec281e3edfd804b993b4b1d7495` |
| production-stack `20a658044af0dea70e9e0136494bb9979cfd9fab`，sleep 教程 L1–4、L115–120、L169–175 | `/tmp/b28/production-stack-vllm-stack-0.1.9/docs/source/use_cases/sleep-wakeup-mode.rst` | `d62f16d2ac62184d0235bd63800121b0e1d4d48a04d4bd93cd29f76b82d65561` |

两份缓存摘要前缀均与第二轮记录一致；来源记录本轮 SHA-256 为 `45a576659c61191ef18bfc6bb6ef6b7a82f7f79db964ef7373c0f9398efff175`，亦与第二轮相同。缓存身份核对不证明远端 tag 当前解析、版本组合兼容或部署成功。本轮未扩查 allocator 内部、完整恢复路径或性能基线。

## C02 判定及新问题检查

| 检查点 | 本轮证据与判断 |
|---|---|
| 正文残留断言 | L102 现明确“已核 worker 层分支（sleep level 1/2 不同处理、wake 调 allocator）”，不再将已取证部分全部列为未知，也不再称仅引用教程。**原残留已消除。** |
| 已核范围是否有源码支持 | 固定 [gpu_worker.py L109–155](https://github.com/vllm-project/vllm/blob/b17039bccc17b94a2ea107272ad7bc93508708df/vllm/v1/worker/gpu_worker.py#L109-L155)中，L115–119 对 level 2 保存 buffers，L122 按 level 1 与其他 level 传入不同 offload tags；L136–145 调 `allocator.wake_up(tags)` 并按已保存状态恢复 buffers。这足以支持 worker 层分支已核的表述。 |
| 未核范围是否仍保留 | L102 继续明确 allocator 恢复链与完整唤醒路径未核；与 L68/L112 及来源记录 L26/L33 一致。局部调用证据没有被提升为完整恢复语义或统一权重重载结论。 |
| 教程数值是否被升级为基线 | L102 的“示例值不作基线”与 L65/L103、来源记录 L26–27/L33–34 一致。固定教程 [L115–120](https://github.com/vllm-project/production-stack/blob/20a658044af0dea70e9e0136494bb9979cfd9fab/docs/source/use_cases/sleep-wakeup-mode.rst#L115-L120)及 [L169–175](https://github.com/vllm-project/production-stack/blob/20a658044af0dea70e9e0136494bb9979cfd9fab/docs/source/use_cases/sleep-wakeup-mode.rst#L169-L175)确有示例日志；本次未将示例视为目标部署耗时，也未重新引入“上游没有任何数值”的绝对断言。 |

**C02：CLOSED。** 第二轮开放的是正文 L102 的取证范围冲突；本次已直接修正该句，既有数值边界仍然成立，无需补测或补核完整 allocator 才能关闭此项。

本次唯一修订未引入新的无依据实现断言、跨平台保证、耗时承诺或验证状态升级。正文仍为 `draft / source_checked`，环境档案为空；本部署三平台基线、allocator 恢复链及完整唤醒路径继续列为 unknown。未发现需新立编号的问题。

## 校验与写入范围

报告落盘后执行 `PYTHONDONTWRITEBYTECODE=1 make check`，结果为 **PASS: 117 content entries; 553 sources**。

为满足“只新增这一个文件”，将仓库（含既有 `build/`）复制到临时目录 `/var/folders/bk/3f4npkcs6l30twg9ph23c2jh0000gn/T/t0709-recheck3-fd6xt67z/repo`，在副本中执行 `make build`，结果同为 **PASS: 117 content entries; 553 sources**，成功生成两个 catalog 文件。读取生成 JSON 确认 `documents=117`、`sources=553`，其中被审正文 SHA-256 与本轮提交值一致，状态仍为 `draft / source_checked`；工作区 `build/` 未改写。这些检查仅验证结构、本地链接与生成过程，不验证技术语义或远端内容。

本会话写入工具仅操作本报告。对照本轮写入前的 606 个受版本控制或未忽略文件的摘要清单，既有文件无修改、无删除；除本报告外，另观察到 `docs/research/batch-28-t07-10-codex-recheck-2.md` 新增，非本会话写入，未覆盖或回退。交付前重新核验正文，SHA-256 仍为 `7092dd3156e1646179aaf88378bc24f31523ee67da14aa6728ff660180ee584f`。

本轮未修改 `src/kb/`，未新增或运行代码测试；未部署、压测或调用 sleep/wakeup。C02 关闭只确认原断言修订完成，不补足正文已声明的运行证据缺口。
