# Batch 26 · T06-08 修订后定向复核（第二轮）

## 头部

- 审阅角色：批次审阅者；复核[初审报告](batch-26-t06-08-codex-review.md)的 C01–C05 关闭条件，并检查修订引入的问题，不代作者修改正文。
- 日期：2026-10-20（Asia/Shanghai）。
- 实际审阅模型 / 推理档位：`gpt-6.1-sol / xhigh`。本轮本地 CLI 会话 `01a15752-acd8-78b2-97d1-632d82fcff03` 的 `session_meta` 为 `originator=codex_exec`、CLI `0.163.0`；`turn_context` 中模型与档位均为上述单一值，未委派其他模型，未发现输出回退标记。
- 审阅范围：[Checkpoint 恢复一致性](../../knowledge/06-training/checkpoint-state-consistency.md) L100–105、L148；[弹性训练与成员变更](../../knowledge/06-training/elastic-training-and-membership.md) L71–81；[registry](../../sources/registry.yaml) 对应 Megatron/MindIO notes；[作者来源记录](batch-26-t06-08-sources.md) L7、L13、L22、L36、L39、L49。相邻版本声明、状态与验证边界一并核对；其他批次改动不纳入结论。
- 基准：[写作指南](../authoring-guide.md)第 5、7 节及初审各项关闭条件。核对当前原文件，并用初审留下的隔离副本辅助定位修订差异；临时副本不作为上游技术证据。

### 本轮重新打开的证据

1. **Megatron 固定源码**：通过 GitHub 连接器重新读取 `core_v0.12.1` tag 元数据，仍指向 `a845aa7e12b3a117e24c2352b9e3e60bad2e3a17`；重读 `megatron/training/checkpointing.py` L649–703、L878–940、L1350–1375。
2. **MindSpeed-LLM 固定源码**：重读 commit `53f3639c3da9c000a187c44cc0c08d55026ddded` 的 `mindspeed_llm/training/checkpointing.py` L190–285、`docs/pytorch/features/high_availability.md` L39–87、`docs/pytorch/install_guide.md` L58–84。安装指引仍钉扎 Megatron tag 和 MindSpeed 分支，HA 文档仍外链指定的 MindIO 约束页。
3. **MindIO HTML**：指定的 [MindX DL 6.0.0 约束页](https://www.hiascend.com/document/detail/zh/mindx-dl/600/clusterscheduling/ref/mindiottp/mindiotft005.html)本轮网页读取返回 404，浏览器接口报告无可用浏览器；未独立取得作者两次渲染所见的 HTML，不把工具不可达解释为官方删页。
4. **同版本补充证据**：本轮重新打开初审所引同 URL 的官方 [MindCluster 6.0.0《故障恢复加速》PDF](https://www.hiascend.com/doc_center/source/zh/mindx-dl/600/clusterscheduling/ref/mindiottp/%E6%95%85%E9%9A%9C%E6%81%A2%E5%A4%8D%E5%8A%A0%E9%80%9F.pdf)，网页工具返回 **87 页**，封面为文档版本 01、发布日期 2024-12-30。对既存本地 87 页副本的 §2.1.2 **印刷页 4–5 / 文件第 10–11 页**重新提取文本、用 Poppler 渲染并逐页目视核对，内容与本轮远程提取一致。本地副本 SHA-256 为 `56641a53cf1d0ab344562d905155371cfcea0069141d1c5215ad2e4e650a9d10`；该哈希不是本轮远程响应字节的指纹。此处沿用初审补充证据，并在本报告明确版本、定位和采信范围，不将它冒充为作者 HTML 快照或已登记的 HTML 来源本体。

源码行号来自原文件：下列既存副本的 Git blob SHA-1 均与本轮远程文件元数据一致，再用 `nl -ba` 核对行段；没有把网页转换坐标用作 GitHub 行锚点。

| 文件 | 本轮核对的远程 Git blob | 本地复算 SHA-256 前 16 位 |
|---|---|---|
| Megatron `megatron/training/checkpointing.py` | `04be04bf0443004f8c4b73e89198f0d4db48b74c` | `713fc0fcb172b710` |
| MindSpeed-LLM `mindspeed_llm/training/checkpointing.py` | `30fc0a604b886bf381963411ab2469e867548a17` | `beaa6057ac72f74f` |
| MindSpeed-LLM `docs/pytorch/features/high_availability.md` | `7c238ff474c9a0fa81312be2ca1132c0bb191e81` | `83b6b6d8e3590f0e` |
| MindSpeed-LLM `docs/pytorch/install_guide.md` | `4622bdb317664af7affc50692b10e6c56a7902da` | `8dd60a6cc0983ffc` |

## C01–C05 逐项复核表

| 初审项 | 结论 | 修订核对、上游证据与关闭判断 |
|---|---|---|
| **T06-08-C01 · P2** 公式量纲与范围 | **CLOSED** | 弹性正文 L76、checkpoint 正文 L148、MindIO registry notes、来源记录 L36 均已明确：增加片上内存总量 **GB = 模型参数量 N（以 B＝十亿计）×12×副本数**，结果为全局总量；不再把 N 释为卡数，也未据此推导每卡需求或目标环境扩容结果。与 [PDF §2.1.2 印刷页 5 / 文件第 11 页](https://www.hiascend.com/doc_center/source/zh/mindx-dl/600/clusterscheduling/ref/mindiottp/%E6%95%85%E9%9A%9C%E6%81%A2%E5%A4%8D%E5%8A%A0%E9%80%9F.pdf#page=11)一致。相邻版本线不互推声明保留。 |
| **T06-08-C02 · P2** 加载分支顺序 | **CLOSED** | checkpoint 正文 L103、L105、Megatron registry notes 与来源记录 L39 已同步。源码先以 tracker 初始化 iteration，再由满足 `getattr(args, "ckpt_step", None)` 条件的显式 step 覆盖；随后非持久 iteration 若存在且不小于当前有效值则直接返回；否则到 `iteration == -1` 才进入缺 checkpoint 告警/可选退出分支。修订不再把“无 tracker”单独当作随机初始化的充分条件。见固定 [L898–935](https://github.com/NVIDIA/Megatron-LM/blob/a845aa7e12b3a117e24c2352b9e3e60bad2e3a17/megatron/training/checkpointing.py#L898-L935)。 |
| **T06-08-C03 · P2** args 中的数据计数 | **CLOSED** | checkpoint 正文 L102 已区分 args 内已有计数、wrapper 补充统计及应用自定义游标语义，并保留 `no_save_optim` / `no_save_rng` 条件。Megatron [L657–699](https://github.com/NVIDIA/Megatron-LM/blob/a845aa7e12b3a117e24c2352b9e3e60bad2e3a17/megatron/training/checkpointing.py#L657-L699)支持保存 args 与条件组装；[L1357–1370](https://github.com/NVIDIA/Megatron-LM/blob/a845aa7e12b3a117e24c2352b9e3e60bad2e3a17/megatron/training/checkpointing.py#L1357-L1370)在存在 checkpoint args 且非 finetune 时恢复 consumed train、skipped train、consumed valid 计数，并据 consumed train 更新 microbatch 配置。MindSpeed wrapper [L210–213](https://github.com/Ascend/MindSpeed-LLM/blob/53f3639c3da9c000a187c44cc0c08d55026ddded/mindspeed_llm/training/checkpointing.py#L210-L213)另补 FLOP。没有将这些计数扩大成任意 loader 预取或 exactly-once 保证。 |
| **T06-08-C04 · P2** DP/MoE/机制术语及取证歧义 | **CLOSED** | 两正文、MindIO registry notes 与来源记录已同源订正：DP 偶数条件属于 ZeRO-1 总体约束；副本数 2 的分支条件为 DP>1，仍须同时满足总体条件；其他副本数的整除主体为 DP Size；MoE 为开启前/后，术语为“以算代传”。本轮 [PDF §2.1.2 印刷页 4–5 / 文件第 10–11 页](https://www.hiascend.com/doc_center/source/zh/mindx-dl/600/clusterscheduling/ref/mindiottp/%E6%95%85%E9%9A%9C%E6%81%A2%E5%A4%8D%E5%8A%A0%E9%80%9F.pdf#page=10)全部支持；A+K、9000 的 UCE/ARF 限制、严格多数阈值、一致性门、持久化路径与 ARF/级联故障条件也逐条相符。初审对 PDF 整除方向的描述需纠正，具体处置见下文。 |
| **T06-08-C05 · P3** 整包哈希归因 | **CLOSED** | 来源记录 L7、L13、L22 已去掉 gzip 不稳定归因，保留两个实际包哈希与同一 commit。对既存两包重新复算：tag 名包 `693f619a8b608726c23dc53a7e0d283684883149fb140951f169a297fe72936e`、commit 名包 `c6db8136f3163c595d614fd2aa26aa4f4a13f3719a9706db4609636b2b8d3bd1`；gzip 前 10 字节相同，解压后的 tar 仍不同。顶层目录分别为 `MindSpeed-LLM-2.2.0/`、`MindSpeed-LLM-53f3639c3da9c000a187c44cc0c08d55026ddded/`，PAX comment 均指向同一 commit。归一化顶层目录后全部 **1903 个成员（含根目录；非根成员 1902 个）**的路径、文件内容哈希及所比较成员元数据一致。Megatron 行仅保留 tag 名归档口径，不再继承未经证明的 gzip 归因；本轮复算其包哈希前缀仍为 `3e83d4a79014d77c`。未据此断言同一 URL/ref 的重复下载稳定性。 |

### C04 的证据处置与初审更正

**初审所称 PDF 的整除方向相反，在本轮重开材料中不成立。** 印刷页 4 的原文为“其他副本数时要求DP Size能被副本数整除”，文本提取与页面图像一致，支持作者当前转述。初审要求核实整除主体的目的已经达到；撤回该子项对相反方向的描述，保留历史报告，由本报告记录纠正。总体偶数条件没有被副本数 2 的 DP>1 条件取代，修订在这一层级上也正确。

作者没有把无法确认身份的“同 URL 直下 2 页文档”登记为来源，处置合理；本轮未取得该 2 页制品，不能判断差异来自何处，也不据此否定任何一方的取回记录。不过，**作者两次渲染一致的自校记录，本身不足以替代独立重开争议原文**。本轮关闭依据是修订同步完成，加上审阅者重新打开并定位的同版本 PDF 对相关主张逐条提供支持；不是假称已经独立读到 HTML。PDF 作为初审已有补充证据的本轮复核记录留在本报告，不冒认作者已采用或已登记它；本轮也不修改 registry。

因此，未独立重开的 HTML 快照身份及 2 页/87 页取回差异仍作为取证限制保留，但本轮已无影响上述技术主张的未消解矛盾，不再据此维持 C04 开放。MindX DL 6.0.0 与 MindSpeed-LLM v2.2.0 的正式配套仍未知，本轮补证不扩大版本兼容结论。

## 新发现（T06-08-R01…）

**无新增发现，不分配 R 编号。** 修订未引入新的公式、分支、数据状态或版本边界错误。初审对 PDF 整除方向的误读已在 C04 中纠正，不重复登记为作者修订引入的问题。

相邻检查确认：完整状态矩阵及恢复后分层验证保留；三种 checkpoint 格式没有被写成跨并行度重分片保证；mid-step、外部 whl、完整 load/resharding 及配套矩阵的 unknown 未被抹去。两篇正文继续为 `draft / source_checked`；既有 CPU 优先 DCP 实验与精度实验仍为 `not_verified`。未重审这些历史内容的全部上游证据。

## 整体结论

**C01–C05 全部 CLOSED；T06-08 在初审及本轮定向复核范围内通过。** 初审 4 项 P2、1 项 P3 均无遗留开放项，本轮无新增发现。C04 的关闭包含对初审证据误读的纠正，并明确区分作者 HTML 取回记录与本轮 PDF 独立补证。

- 结构检查：在包含本报告及现有 build 导航的隔离副本执行 `make check`、`make build`，均通过：**108 content entries / 534 sources**。只验证结构与本地文件链接，不证明技术正确性或远程内容；未修改 `src/kb/`，未新增测试。
- 写入边界：本轮工具仅新增本报告；前后 SHA-256 对照显示全部既存仓库文件内容不变、无文件删除。对照期间另出现 `docs/research/batch-26-t07-01-codex-recheck.md`，不在本轮工具写入清单中，本轮未触碰，也不纳入结论。构建只写临时副本，未回写当前仓库的 build。
- 验证边界：本轮未安装 whl、运行训练/保存/恢复、伸缩或故障注入实验；审阅通过不等于硬件验证，也不改变正文与实验的状态。
