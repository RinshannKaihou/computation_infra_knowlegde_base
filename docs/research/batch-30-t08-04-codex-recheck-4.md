# Batch 30 · T08-04 第五轮定向复核报告

## 会话元数据

| 项目 | 记录 |
|---|---|
| 审阅角色 | 独立批次审阅者；只复核 C05、C06、N10、N11 及相关修订引入的问题，不承担正文编写或修订 |
| 实际执行模型 / 档位 | `gpt-6.1-sol / xhigh` |
| turn_context 核验方法 | 读取本进程 `CODEX_THREAD_ID`、`CODEX_SESSION_ID`，据其定位本会话 rollout，逐行解析 JSONL；交叉核对同文件的 `session_meta.id`、`turn_context` 及 `collaboration_mode.settings`，未用默认配置或其他会话代证 |
| 核验结果 | 两个环境会话 ID 均与 `session_meta.id` 一致；`turn_context.model=gpt-6.1-sol`、`effort=xhigh`、`cwd=/Users/ywang2397/work/AI_reliability_knowledge_base`；嵌套设置为 `model=gpt-6.1-sol`、`reasoning_effort=xhigh`，符合本次用户指定 |
| 核验坐标 | `/Users/ywang2397/.codex/sessions/2026/10/21/rollout-2026-10-21T21-58-27-01a15ec1-93a3-7f10-ab23-8f6ea82c0386.jsonl` L8，时间戳 `2026-10-21T13:58:38.470Z` |
| 会话 / turn ID | `01a15ec1-93a3-7f10-ab23-8f6ea82c0386` / `01a15ec1-94e6-7340-8785-5d2fbbd040e0` |
| 执行方式 | 当前本地 Codex CLI 直接复核；同 rollout L1：`originator=codex_exec`、`cli_version=0.163.0`、`source=exec`；未另启模型、子代理或回退轮次 |
| 日期 / 时区 | 2026-10-21 / Asia/Shanghai |
| 写入范围 | 仅新增本报告；不修改正文、修订记录、registry、其他报告、导航、计划及本仓库构建产物 |

下列行号对应本轮读取快照；SHA-256 按文件原始字节计算。

| 对象 | 行数 | SHA-256 |
|---|---:|---|
| [初审](batch-30-t08-04-codex-review.md) | 184 | `8ddaa6b84f0567564dd63023fafed2085b440d82c05ce436dbed4cbb3de7e621` |
| [第二轮](batch-30-t08-04-codex-recheck.md) | 120 | `cb73d1ba36b818dc009989c54d13c6069431896c66bcdc63030ea3bb06b26433` |
| [第三轮](batch-30-t08-04-codex-recheck-2.md) | 106 | `305a41d0b361d38041bb17df08bb21261fb91d7c05498a993231f45b6c501797` |
| [第四轮](batch-30-t08-04-codex-recheck-3.md) | 97 | `eab732526b32f9b3a8e5420d55372f4f15ee0e2903bbbd40480ab8a14e0874c4` |
| [修订后正文](../../knowledge/08-reliability/silent-errors-and-integrity.md) | 218 | `c51b8f956dd50cc0b97e0b2814b34078c0b7a0b8e97e8c059c3c3a1d0c9987c1` |
| [来源与各轮修订记录](batch-30-t08-04-sources.md) | 65 | `5d02654afffe7b0f0d9c084d0590b7b9f70bdf9ce41268a5d3ed7fbf65f84b6b` |
| [registry](../../sources/registry.yaml) | 7227 | `720620e23ec757a08bf640e84745ef090be1af28c7d22c18a8d7a3bddf4d2321` |

## 范围与方法

先读 `README.md`、`AGENTS.md`、写作指南、总目录与元数据 schema。沿初审及三份复核报告核对上述四项的剩余关闭条件；此前已关闭项不重开，不重新执行整篇初审。来源记录现已包含 L60–65 的“第三轮修订记录（复核二后）”，逐条以实际正文、登记及上游证据验证其自述。

定向重读固定 commit 的 DCGM 字段头文件、固定 tag 的 rccl-tests README 与固定 commit 的输出实现；GitHub 连接器返回原文件内容，行号按原文件计数。另打开当前 DCGM 显存插件官方页和 arXiv v1 精确入口及 HTML 附录，核对支持前提与文件身份。未以搜索摘要、历史报告结论或修订完成声明代替本轮核对；未执行上游诊断或训练命令。

## 指定未闭项逐项状态

| 编号 | 优先级 | 状态 | 对照上一轮剩余关闭条件的判断 |
|---|---|---|---|
| C05 | P2 | **CLOSED** | 上一轮仅余与 N10 同源的错误 ECC 字段。正文 L168 已改为固定源码中存在的 CURRENT/PENDING 与 SBE/DBE volatile/aggregate 字段；显存测试允许性、最小分配条件、其余插件前提 unknown 和 AMD 关闭校验语义继续保留。三平台清单原条件满足，不据此认定实际硬件支持或 fleet 检出率。 |
| C06 | P2 | **CLOSED** | registry L610 已登记实际采用的固定 `dcgm_fields.h` 完整 URL；正文 L104、L212 均固定为 `abs/2502.12340v1`，与本篇 L21 依赖及 registry L7216 主入口一致。既有补链与依赖继续有效；36 处外链均可精确映射至本篇 source_refs 对应条目，详见下文。 |
| N10 | P2 | **CLOSED** | 正文 L168 的原 `DCGM_FI_DEV_ECC_SB_ERROR` / `_DB_ERROR` 错误例子已删除，六项替代宏的名称、编号和 mode/volatile/aggregate 语义均可在固定源码核实。来源记录 L62 与实际修订一致。 |
| N11 | P3 | **OPEN** | 正文 L97 已回到 L90–97 的三列表格，且只剩一条“代价”行，此子项关闭。但 L135 表头仍为四列，L144 任务质量行仍只有三个单元格：成本在机制列，误报/盲区在“覆盖与成本”列，最后一列缺失；来源记录 L63 所称“四列表头重排”未落实。 |

## 定向证据与剩余差距

### C05 / N10：准确字段已替换

正文 L168 所用固定文件为 [DCGM v3.3.9 dcgm_fields.h L751–793](https://github.com/NVIDIA/DCGM/blob/b0ec3c624ea21e688b0d93cf9b214ae0eeb6fe52/dcgmlib/dcgm_fields.h#L751-L793)，本轮读取返回 blob SHA `b87f87a8240ae03b81f6d4a22ab7e63d2c6dd2af`。六项可核对应如下；正文的缩写按共同前缀展开后均匹配。

| 宏名 | 编号 / 原文件行 | 语义 |
|---|---|---|
| `DCGM_FI_DEV_ECC_CURRENT` | 300 / L751 | 当前 ECC 模式 |
| `DCGM_FI_DEV_ECC_PENDING` | 301 / L756 | 待生效 ECC 模式 |
| `DCGM_FI_DEV_ECC_SBE_VOL_TOTAL` | 310 / L761 | 单比特 volatile 错误总数 |
| `DCGM_FI_DEV_ECC_DBE_VOL_TOTAL` | 311 / L766 | 双比特 volatile 错误总数 |
| `DCGM_FI_DEV_ECC_SBE_AGG_TOTAL` | 312 / L772 | 单比特 aggregate/persistent 错误总数 |
| `DCGM_FI_DEV_ECC_DBE_AGG_TOTAL` | 313 / L778 | 双比特 aggregate/persistent 错误总数 |

重读 [DCGM GPU Memory Plugin 的参数与失败条件](https://docs.nvidia.com/datacenter/dcgm/latest/user-guide/dcgm-diagnostics.html#gpu-memory-plugin)，正文保留的配置允许性、无相应配置默认不允许、最小分配条件及写入/回读 mismatch 判据与现页相符；固定源码和可变 user-guide 没有被合并为同一冻结版本。AMD 的校验迭代及规模开销可在 [固定 README L175](https://github.com/ROCm/rocm-systems/blob/therock-10.1/projects/rccl-tests/README.md#L175) 定位，未校验时的 `N/A` 可在 [固定 util.cu L510–524](https://github.com/ROCm/rocm-systems/blob/7da43026e4f2ef7600433c38c820732f7a205d22/projects/rccl-tests/src/util.cu#L510-L524) 的输出分支核对。原支持前提子项继续满足；本轮关闭 C05、N10。

### C06：两个剩余入口均已接通

按正文 Markdown 的完整目标 URL 提取，共 **36 处外链、19 个唯一 URL**。26 处与本篇依赖条目的主 `url` 精确相等；纳入对应条目 notes 和许可 scope 明示的完整 URL 后为 **36/36 处**。仅 GitHub `#L…` 定位片段按同一文件处理，其他片段及 arXiv 版本保留；未用仓库前缀、同 commit 或全库其他条目代替本篇依赖。15 个 source_refs 均有正文直接外链可映射，原五个缺链来源仍可从正文直接进入支持页。

| 上一轮剩余对象 | 本轮实际证据 |
|---|---|
| DCGM 固定头文件 | 正文 L168 的完整文件路径与 registry L610 notes 新增 URL 一致；本篇 L22 已依赖 `src.nvidia.dcgm-v3.3.9`，notes 所记 blob SHA 与本轮上游返回值一致。 |
| arXiv v1 附录入口 | 正文 L104、L212 均采用 registry L7216 的 `https://arxiv.org/abs/2502.12340v1`；本篇 L21 已依赖该 ID。独立打开 [v1 原页](https://arxiv.org/abs/2502.12340v1) 并进入 [v1 全文的附录 D](https://arxiv.org/html/2502.12340v1)，D.1–D.4 可定位；本轮没有把 ACL 与预印本当成相同文件修订。 |

Adam、RCCL README、Llama 3 v3、PyTorch 子页、ECC 深页和 msprobe 文档许可的既有精确映射继续有效。C06 关闭；这里只证明本项来源链闭合，不将 URL 映射等同于全篇技术或硬件验证。

### N11：代价行已恢复，任务质量行仍错列

正文 L90 的三列表头、L91 的分隔行与 L97 的“代价”行连续，代价行有三个单元格且没有孤立副本，两个策略的对应关系恢复。原来重复/脱表的问题已修复；L95–99 的共同分母、共同检出终点与单列扫描/部署时间仍在。

剩余问题可直接由原 Markdown 复核：L135 表头为“方法 / 机制与来源 / 覆盖与成本 / 已知假阴性/误报与盲区”，L136 有四个分隔格；L144 去除首尾管道符后只有 **三个单元格、两个内部分隔符**。第一格为任务质量检测；第二格同时容纳监控机制、成本限定与 loss 低敏感说明；第三格以“误报边界”开头，实际对应第三列表头“覆盖与成本”，第四列为空。来源记录 L63 的完成自述不能关闭该原有差距。

**继续关闭条件**：由作者使该任务质量行与四列表头对应，覆盖/成本与误报/盲区各归相应列；同步校正修订记录，使其符合最终正文。保留现有复用已计算 loss 的成本限定、额外范数/评估成本 unknown 及误报说明，不要求改写其他方法或增加硬件实验。本轮不提供替换正文，也不将同一结构缺口另计为新问题。

## 新发现

无须从 N30 起另列的独立新发现。N11 的任务质量行及其修订自述不一致均属于该未闭项的延续，未重复编号；此前已关闭的技术成本项不重开。

## 检查与写入边界

为遵守仅新增报告的限制，将当前 tracked/untracked 文件及已有 `build/` 文件复制至 `/private/tmp/batch30-t0804-recheck4-37ky3d1n/snapshot`，加入本报告后，使用项目既有 Python 环境执行 `make check`、`make build`，**均退出 0：126 content entries / 575 sources**。构建产物只写入临时副本，未安装或修改依赖。这些检查验证结构与本地文件链接，不验证远程内容、技术正确性或 Markdown 表格列语义；检查通过不关闭 N11。

本会话唯一仓库写入为新增本报告。开始时已有的正文、来源记录、registry 修订及其他审阅报告未回退、未改动；交付时复比 671 个既有文件的哈希，未发现内容变化或删除。期间另新增 `batch-30-t08-06-codex-recheck-4.md`，不是本会话写入。上述七个依据文件的哈希均保持表中值。

本轮未修改 `src/kb/`，无需运行 `make test`；未执行设备诊断、压力测试、故障注入、训练或生产动作。正文仍为 `draft / generic / source_checked`，模型审阅不替代真实环境验证。

## 结论

**3/4 CLOSED：C05、C06、N10；OPEN：N11。无新增 N30 项。T08-04 在本轮范围内仍需作者修订 N11 后定向复核，暂不通过；模型审阅不替代真实环境验证。**
