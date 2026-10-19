# Batch 24 交付后复查：Codex 定向复核

日期：2026-10-19（Asia/Shanghai）。基线：`bbdc0a4ed02a6ec69bd8840c74a61570e12060c8` 加本轮开始时的未提交修订。复核对象为 [交付后复查记录](batch-24-post-close-review.md) 的 B24-PC-01–06，不重新宣称完成整个批次的全面技术审阅。

## 1. 结论

**暂不通过。** B24-PC-01、02、03、05、06 为 **CLOSED**；B24-PC-04 为 **OPEN**。新增 **B24-PC-R01（P2，OPEN）**：Megatron hysteresis 被误写成“连续 overflow”门槛，并对单次 overflow 是否缩小 scale 作了过度概括。另有 **B24-PC-R02（P3，OPEN）**：新增引用中的原文件行号有偏差。原工作区正文、账面、来源登记和其他报告均不由本轮修改。

| 原发现 | 判定 | 修订后位置与依据 |
|---|---|---|
| B24-PC-01（账面未收尾） | CLOSED | `plans/topic-coverage.yaml:720`、`:754`、`:770`、`:786`；对应 backlog 的 11 条 gap 已区分 8 closed / 3 open，新增正文 ID、followup 和两份可读文档一致，详见第 3 节。 |
| B24-PC-02（提前宣称 covered） | CLOSED | `plans/full-coverage-backlog.yaml:2297`、`:2403`、`:2412` 保留 open；T06-04/T06-06 仍是 Batch 25 planned；06.2/06.4 保持 partial。 |
| B24-PC-03（专家 grid 轴序） | CLOSED | `knowledge/06-training/parallelism-and-state.md:86`、`:104`、`:106`、`:110`、`:141`、`:151`。独立重读 E01/E02 并按源码复算，组员、专家编号及合成节点放置均正确；SHA-256 与登记及历史 U12 一致。 |
| B24-PC-04（跨实现拼接 scaler） | OPEN | 同页 `:212`、`:214`、`:218`、`:219`、`:220`、`:222`。分列和 bf16 边界已修正，但 Megatron 列新写的连续 overflow 门槛与 E03 可执行逻辑不符，见 R01；不能仅因分列就关闭。 |
| B24-PC-05（QKV offset/切分术语） | CLOSED | 同页 `:100`、`:114`。MHA 的 `[3H,H]`、TP 第 1 片 offset `3H/2`、dim-0 column-parallel 和专家张量 offset 均正确；query-group 交错的说明也正确。其引用行号另列 R02，不把算术纠正撤销为技术错误。 |
| B24-PC-06（双句号） | CLOSED | `knowledge/06-training/index.md:43`、`:44` 两条导航均为单句号，链接及 frontmatter 未损坏。 |

通过条件未满足：必须先修订并定向复核 B24-PC-04 / R01；本报告没有把结构检查通过或历史审阅闭环当作本轮技术通过。

## 2. 角色、模型与取证方法

- 本轮承担原 Codex 审阅角色，不是 `claude-opus-5-5` 的修订者，也没有派发其他审阅代理。按 [编写指南第 7 节](../authoring-guide.md#7-批次审阅约定) 重新读取当前文件和精确上游；用户指定模型/档位为 `gpt-6.1-sol / xhigh`。
- 本轮可读的 CLI 会话记录为 `~/.codex/sessions/2026/10/19/rollout-2026-10-19T09-26-41-01a151c4-9956-7721-a30b-6e5aa4458b44.jsonl`：`session_meta.originator=codex_exec`、`cli_version=0.157.1`，本仓库 cwd；`turn_context.model=gpt-6.1-sol`、`effort=xhigh`，sandbox 为 workspace-write、`network_access=false`。该记录支持“本地 CLI 记录的指定模型/档位一致”，**不能独立证明自定义服务端路由最终使用的模型权重或实际推理档位**（记录的 provider 为 custom）。本轮没有可用于进一步核验服务端实际执行身份的返回元数据；不作超出此证据的身份保证，也不重新认证历史 22 轮。
- 已阅读 `README.md`、`docs/authoring-guide.md`、`content-outline.md`、metadata schema、复查记录、T06-01 来源补充、登记 notes，以及本轮相关 diff。未发现 `docs/` 下更深的 AGENTS.md。
- 对八份固定 tag 文件均尝试重开精确 raw URL。网页工具对 `grad_scaler.py` 返回 Internal Error；随后对该精确 URL 用保留默认 TLS 校验的 `curl -fLSs --retry 2` 重试，exit 7。对 `parallel_state.py` 的本地 curl 也失败。**这些是当前通道限制，不是上游文件不存在。** 没有关闭 TLS、绕过网络限制或申请提权；浏览器补充通道不可用后未继续操作 UI。
- 改用已连接 GitHub 工具，逐文件从 `NVIDIA/Megatron-LM`、`ref=core_v0.19.2` 重新读取精确路径和相关行，并取得该次响应的完整 Git blob SHA。为取得可按原文件坐标核对的实际字节，读取既有 `/private/tmp/b24src/` 缓存，对每份字节独立计算 `SHA1(b"blob " + 十进制字节数 + b"\0" + 文件字节)`，**八份均与本轮联网返回的 Git blob SHA 完全一致**；随后对同一实际字节重新计算 SHA-256。因而本轮不是只抄录作者摘要或信任缓存文件名；同时明确：**本轮没有新 curl 成功下载的八份原文件**，使用的是“本轮远端 blob 身份核验＋本地字节重算”的交叉取证方式。
- 复核用字节副本和算术结果放在 `/private/tmp/b24-post-close-recheck.hzN5Fw/`，未将上游源码写入仓库。以下行号均由这些字节的原始换行计数取得；不使用网页阅读工具的压缩行号。

### 2.1 固定来源与字节身份

均为同一 tag `core_v0.19.2`。E01–E08 的 URL 是本轮重开的精确目标；下表的 Git blob SHA 是本轮 GitHub 工具独立返回的身份，不是 SHA-256 的别名。

| 编号 | 原文件 | 字节数 / 原文件行数 | 本轮重算 SHA-256 | 远端 Git blob SHA（本地重算匹配） |
|---|---|---|---|---|
| E01 | `megatron/core/parallel_state.py` | 114374 / 2692 | `1f6e23a01022c06be3b67f930095898e5032f6ff93695f8da5aae3b5a546dcf0` | `2a3c75811221aacaa0130f8feb081859788f3c5d` |
| E02 | `megatron/core/transformer/moe/moe_layer.py` | 35212 / 807 | `189b0ce590ca1cb9fd8b8c33c2df8e2205e5def7d58dbb8dfd1829a5526553e3` | `48e78775a849575a9d46f95d900490ded4a5946d` |
| E03 | `megatron/core/optimizer/grad_scaler.py` | 6263 / 165 | `81402e800476fce96b70d91ff2b799d889ac6ed9407fe74be7cd73d32449c2a7` | `036564889825ef6a5b3f27fc0e39386730f17e36` |
| E04 | `megatron/core/optimizer/optimizer.py` | 87339 / 2022 | `24609822f7c165c9be9f6e95945c873bf474cdce3ca06600b00b52c5d23b31e4` | `dac16f4a2eeff10325dfcb7e28738e3d76f1ae88` |
| E05 | `megatron/core/optimizer/__init__.py` | 57172 / 1224 | `5a657e3f3ad88d1ea6bf3600258cd1e391921b55d88ba055134e958db300ea20` | `70f757f2889ba5834ad3b046132354bf7f9e8e43` |
| E06 | `megatron/training/arguments.py` | 207996 / 3655 | `f7fad20bc0e0cd9ba4b9ba7e70fa1a1b77030dfd020a7edb50b1d3b3aa41ebf6` | `fd30984b38ae64e1207a948c71ef04dbaf5925da` |
| E07 | `megatron/core/models/gpt/gpt_layer_specs.py` | 33430 / 799 | `af25c83f516b704a85ab93148a10d1ef3af707fd5eff28e32200b15c5274d0f4` | `984840b3a873a0d9e8a91161151347a0f3536513` |
| E08 | `megatron/core/transformer/attention.py` | 89030 / 2159 | `a019cd00a708a22237383456a7ba85bf522201c14a5b7cb0c1e4f0f12eac9837` | `3a5876bc0fe69f9c4a467cd3d74ecd303513af25` |

- E01：`https://raw.githubusercontent.com/NVIDIA/Megatron-LM/core_v0.19.2/megatron/core/parallel_state.py`
- E02：`https://raw.githubusercontent.com/NVIDIA/Megatron-LM/core_v0.19.2/megatron/core/transformer/moe/moe_layer.py`
- E03：`https://raw.githubusercontent.com/NVIDIA/Megatron-LM/core_v0.19.2/megatron/core/optimizer/grad_scaler.py`
- E04：`https://raw.githubusercontent.com/NVIDIA/Megatron-LM/core_v0.19.2/megatron/core/optimizer/optimizer.py`
- E05：`https://raw.githubusercontent.com/NVIDIA/Megatron-LM/core_v0.19.2/megatron/core/optimizer/__init__.py`
- E06：`https://raw.githubusercontent.com/NVIDIA/Megatron-LM/core_v0.19.2/megatron/training/arguments.py`
- E07：`https://raw.githubusercontent.com/NVIDIA/Megatron-LM/core_v0.19.2/megatron/core/models/gpt/gpt_layer_specs.py`
- E08：`https://raw.githubusercontent.com/NVIDIA/Megatron-LM/core_v0.19.2/megatron/core/transformer/attention.py`

E01/E02/E03/E04/E05/E07/E08 的完整 SHA-256 均与 `sources/registry.yaml:4707` 中复查补充相同。E06 的完整 SHA-256 与 [T06-01 初审报告](batch-24-t06-01-codex-review.md) `:128` 的 U07 相同；E01 同时与该报告 `:133` 的 U12 相同。字节相同不意味着作者据此写出的解释和行号必然正确，R01/R02 即为反例。

## 3. B24-PC-01/02：账面逐缺口复核

依据为 [topic coverage](../../plans/topic-coverage.yaml)、[backlog](../../plans/full-coverage-backlog.yaml)、[可读盘点](../topic-coverage-audit.md) 和 [路线图](../full-coverage-roadmap.md) 的当前内容，不以 HEAD 旧内容代替修订稿。

### 3.1 缺口与任务状态

| 缺口 | task_refs 的交付状态 | 当前 gap 状态 | 判定与 backlog 状态位置 |
|---|---|---|---|
| 05.7-G1 | T05-10 done（Batch 24） | closed | 一致，`:2189`；控制器/API/状态存储故障分支已有正文。 |
| 05.7-G2 | T05-10 done；T05-04 done（Batch 22） | closed | 一致，`:2198`；恢复前提、重建/账本核验与新旧任务验收方法均有内容。 |
| 06.2-G1 | T06-01 done | closed | 一致，`:2280`；EP dispatch/combine、专家身份和组合约束已写。 |
| 06.2-G2 | T06-01 done | closed | 一致，`:2288`；固定假设选型与效率权衡已写，不是实测最优配置。 |
| 06.2-G3 | T06-01 done；T06-06 planned（Batch 25） | open | 一致，`:2297`；已交付映射/静态检查，未据此关闭性能验证缺口。 |
| 06.3-G1 | T06-02 done | closed | 一致，`:2339`；训练循环、组件和 eager/compiled 路径已有主干。 |
| 06.3-G2 | T06-02 done | closed | 一致，`:2347`；三组独立版本档案的实现责任已有对照。 |
| 06.3-G3 | T06-02 done | closed | 一致，`:2355`；执行路径验证方法已交付，不等于执行验证成功。 |
| 06.4-G1 | T06-03 done | closed | 一致，`:2395`；预训练/微调工作流和状态契约已有主干。 |
| 06.4-G2 | T06-04 planned（Batch 25） | open | 一致，`:2403`；RL rollout、协同、权重同步尚待交付。 |
| 06.4-G3 | T06-03 done；T06-04 planned（Batch 25） | open | 一致，`:2412`；不能用预训练/微调侧方法覆盖 RL 侧一致性/吞吐验证。 |

任务状态原位：T05-04 `:5526`；T05-10 `:5789`；T06-01 `:5836`；T06-02 `:5884`；T06-03 `:5934`；T06-04 `:5977`；T06-06 `:6074`。Batch 24 为 done，Batch 25 为 planned。8 项关闭均在 `closure_lane: content` 下解释；`validation_refs: []` 不被解释为存在硬件验证。

内容范围抽查支持这些账面：`knowledge/05-cluster-platform/control-plane-recovery.md:86`、`:107`、`:118`、`:144` 分别有故障、恢复前提、账本和方法设计；`knowledge/06-training/framework-execution.md:50`、`:73`、`:87`、`:99` 有组件链、编译路径、责任边界和验证方法；`knowledge/06-training/pretraining-and-finetuning.md:79`、`:91`、`:116`、`:123` 有状态、adapter、观察口径和阶段验证。未因此重新认证这些正文的全部上游主张。

### 3.2 coverage、evidence 与 followup

| 主题及 topic-coverage 起始位置 | coverage / gaps | evidence_refs 与 followup | 可读文档一致性 |
|---|---|---|---|
| 05.7 `:720` | covered；gaps 空 | 已补 `cluster-platform.control-plane-recovery`；maintain / maintain | 盘点 `:108`、路线图 `:276` 均为已覆盖基础范围，保留未执行演练边界。 |
| 06.2 `:754` | partial；只余 G3 对应缺口 | 保留 `training.parallelism-and-state` 等；normal / add_or_extend；明确 T06-06 | 盘点 `:115`、路线图 `:276` 均将性能验证留给后续。 |
| 06.3 `:770` | covered；gaps 空 | 已补 `training.framework-execution`；maintain / maintain | 盘点 `:116`、路线图 `:276` 一致，未把方法设计升级为实跑。 |
| 06.4 `:786` | partial；G2/G3 开放 | 已补 `training.pretraining-and-finetuning`；high / add_or_extend；明确 T06-04 | 盘点 `:117`、路线图 `:276` 一致，没有提前宣称 RL 已覆盖。 |

`docs/topic-coverage-audit.md:3` 头段的 Batch 24 条目同样列出 8 项关闭及 3 项后续缺口；文末误置的收尾条目已移除。由此 **PC-01/02 CLOSED**。这不等于承诺计划文件全局 summary/batch_planning 历史计数已同步；复查记录已将该既有问题列为未处理，本轮不扩展处理。

## 4. B24-PC-03：默认轴序、专家编号与独立复算

### 4.1 源码规则

E01 原文件 L617 的默认 `order` 为 `tp-cp-ep-dp-pp`；L292 的秩表达式和 L322–375 的前缀乘积/坐标分解表明：**order 中靠前的轴变化最快**。RankGenerator 在 L479–491 限制 EP/CP 不同时大于 1；L857–868 的稠密 generator 取 EP=1，L871–896 的专家 generator 取 CP=1，并以 `expert_order = _inject_gtp_remat_axis(order, after="ep")` 构造。L898–907 检查 PP 组一致。

严格说，插入 remat 轴后的字符串分别为 `tp-gtp_remat-cp-ep-dp-pp` 与 `tp-cp-ep-gtp_remat-dp-pp`。**本样例 GTP/EGTP 均为 1、rank_offset=0**，略去大小为 1 的轴后，正文的稠密 `[pp,dp,cp,tp]`、专家 `[pp,edp,ep,etp]`（慢→快）等价且正确；不是声称所有配置的 order 字符串都被删除了 cp/remat。非默认 order 的限制已在正文注明。

E02 原文件 L181–194 按 EP 组内 rank 计算本地专家数及连续编号偏移：128/4=32；rank 37 的 ep_rank=2，故持 expert 64–95，不再是 0–31。

### 4.2 复算结果

只从经 blob 身份核对的 E01 用 AST 抽出 `generate_masked_orthogonal_rank_groups`、`RankGenerator`、`_inject_gtp_remat_axis` 执行纯整数构组；没有 import 整个 Megatron、没有初始化 torch/distributed 或进程组。各抽查轴的组集合都以断言验证互斥并覆盖 0–63，两个 grid 的 PP 组相等。

稠密样例 TP2/CP2/PP2/DP8：`rank = 32pp + 4dp + 2cp + tp`，rank 37 坐标 `(pp=1,dp=1,cp=0,tp=1)`。

| rank 37 的稠密组 | 本轮结果 |
|---|---|
| TP | `{36,37}`，组内第 1 号 |
| CP | `{37,39}`，组内第 0 号 |
| TP+CP | `{36,37,38,39}` |
| PP | `{5,37}`，组内第 1 号 |
| DP | `{33,37,41,45,49,53,57,61}`，组内第 1 号 |

专家样例 ETP2/EP4/PP2/EDP4：`rank = 32pp + 8edp + 2ep + etp`，rank 37 坐标 `(pp=1,edp=0,ep=2,etp=1)`。

| rank 37 的专家组 | 本轮结果 | node=rank//8 的合成放置 |
|---|---|---|
| ETP | `{36,37}`，组内第 1 号 | 节点 4 内 |
| EP | `{33,35,37,39}`，组内第 2 号 | 四成员均在节点 4 |
| expert DP | `{37,45,53,61}`，组内第 0 号 | 分别在节点 4、5、6、7 |
| PP | `{5,37}` | 与稠密 PP 组相同 |

选型表 EP 行 ETP2/EP4/PP1/EDP8：`rank = 8edp + 2ep + etp`。rank 0 的 ETP 组 `{0,1}`；EP 组 `{0,2,4,6}` 全在节点 0；expert DP 组 `{0,8,16,24,32,40,48,56}` 各在一个节点、跨全部 8 节点。每节点 2 个 EP 组的说法正确，不能再沿用前轮 stride 8 的 EP 组或 stride 2 的 expert DP 组。

与修订后正文 `:93`–`:117`、公共放置 `:141`、选型表 `:151` 一致。持有同一 ep/etp 坐标的 expert DP 成员是 expert 64–95 同一 shard 的副本，不是互补 shard。**PC-03 CLOSED**；这些是合成映射与整数复算，不是组网、通信或吞吐验证。

## 5. B24-PC-04 与新增 B24-PC-R01（P2，OPEN）

### 5.1 已确认修正的部分

- 同页 `:212` 明确使用 Megatron 自有 scaler，`:214`/`:216` 将 PyTorch 和 Megatron 分列；表后 `:224` 的 PyTorch 段有明确实现限定。PyTorch 列按用户要求保留原审阅已关闭口径，本轮不重新开放。
- E04 L741–774：先复制梯度，只有 scaler 存在才 unscale/check，并在 L770 调用 `grad_scaler.update(found_inf_flag)`；没有 scaler 时 L774 返回 False。L816–822 的 `step()` 得到 found_inf 后返回三元组 `(False,None,None)`，首元素才是 `update_successful=False`，与“overflow 跳过参数更新”一致。
- E05 L638–662：显式 loss_scale 选择 ConstantGradScaler；没有显式 loss_scale 且 fp16 时选择 DynamicGradScaler；bf16 且没有显式 loss_scale 不创建 scaler。动态 scaler 的 growth/backoff 分别为 2.0/0.5。正文 bf16 说明限定为“由 loss scaling 引起的”跳步，没有宣称 bf16 不会产生非有限值。
- E06 L2907、L2911–2917：loss-scale 默认 None，initial scale 为 `2**32`，minimum 为 1.0，window 为 1000，hysteresis 为 2。正文所写 1000/2 的默认值正确。动态更新解释应限于 fp16 且未设显式 loss-scale 的这一分支，不应推广到常量 scaler。

### 5.2 R01：hysteresis 不是被任意成功步重置的连续 overflow 计数

- **位置**：`knowledge/06-training/parallelism-and-state.md:220`，Megatron 列“连续 `--hysteresis` 次 overflow 后才缩小 scale”“单次 overflow 默认不缩小”；同一新解释见 `docs/research/batch-24-post-close-review.md:26`。相关支持范围为 E03 L127–153，而不是只读类 docstring 的“consecutive”措辞。
- **证据**：E03 L138–143 在 found_inf 时归零 growth、递减 hysteresis，并在 tracker<=0 时按 minimum 下界做 backoff；L144–153 的 finite 分支只递增 growth，**只有 growth 达到 growth_interval 才同时重置 growth/hysteresis**。一个普通 finite 步不会把 hysteresis 重置。发生 backoff 后也没有立即把 hysteresis 恢复到 2，因此门槛耗尽后后续孤立 overflow 仍可 backoff。
- **独立反例**：直接从 E03 的 AST 抽出 `DynamicGradScaler.update` 方法，以标量状态替身和标量 `max` 代替唯一 tensor max 运算，执行下表控制流；未构造 CUDA tensor、未调用真实 optimizer。取合成初始 scale=1024、minimum=1、hysteresis=2、growth_interval=1000，其余 growth/backoff 使用该实现的 2/0.5。这里只检验分支和计数，不是混合精度训练实验。

| 次序 | found_inf | 更新后 scale | growth tracker | hysteresis tracker |
|---|---|---|---|---|
| 初始 | — | 1024 | 0 | 2 |
| 1 | True | 1024 | 0 | 1 |
| 2 | False | 1024 | 1 | 1 |
| 3 | True | 512 | 0 | 0 |
| 4 | False | 512 | 1 | 0 |
| 5 | True | 256 | 0 | -1 |

第 1、3 步并不连续，却在第 3 步缩小；第 5 步是夹在 finite 步之后的单次 overflow，也缩小。每个 overflow 对 optimizer 的跳步与 scale 是否 backoff 是两回事；低至 minimum 时即使命中 backoff 分支，数值也可能不再下降。仅“初始化后第一次 overflow 默认不缩小”是有条件成立的说法。

- **影响/优先级**：P2。该错误会误导合法跳步、scaler 恢复和状态轨迹预期，是本次为纠正跨实现拼接而新增的不准确执行契约；不能用上游 docstring 的近似描述覆盖实际实现。
- **关闭条件**：将 Megatron 动态分支改为精确 tracker 状态机，删除“必须连续”和无条件“单次不缩小”；说明 reset 的 growth_interval 条件、backoff 后不自动 reset 和 min_scale 下界。明确 ConstantGradScaler 不按这套动态规则调整。定向复核至少覆盖 `True,False,True`、门槛耗尽后的 isolated overflow，以及连续有限更新达到增长窗口时的 reset；本轮仅执行了上表五步反例，未宣称另外两类轨迹已运行。

因此 **B24-PC-04 保持 OPEN**，同时以 **B24-PC-R01** 跟踪修订引入的这个新错误；这不是两个互相独立、重复计数的 P2。

## 6. B24-PC-05、PC-06 与新增 B24-PC-R02（P3，OPEN）

### 6.1 QKV 与专家 shard 的技术修正成立

E07 L324 是 `backend.column_parallel_layer_norm_linear()`，L444 是 `backend.column_parallel_linear()`；均不是 row-parallel。正文明确是**合成 MHA**，所以融合权重 `[3H,H]`、TP=2 本地 `[3H/2,H]`、第 1 片 dim-0 offset=`3H/2` 自洽；没有把此 shape 推广成任意 GQA/MQA 或 gated attention 的 shape。

E08 L1840–1841 的注释描述 query-group 交错；L1861–1867 先把输出 view 为 query-group 轴，L1887–1903 再沿组内维拆分 Q/K/V，支持“不能把 Megatron offset 当成 Q、K、V 三整块顺序拼接布局位置”。L1828–1829 本身不是该交错注释，见下节 R02。

按 H=4096 作独立整数核算：全局 `[12288,4096]`、本地 `[6144,4096]`，第 1 片从行 6144 到 12287。专家合成矩阵 `[11008,4096]` 由两个 ETP 片覆盖：每片 `[5504,4096]`，rank 37 对应第 1 片 offset=5504、行区间 5504–11007；`expert_64` 的合成命名与已纠正专家编号一致。因此 **PC-05 CLOSED**。

`knowledge/06-training/index.md:43`、`:44` 的两个句末重复标点已去除，diff 仅将各自双句号改为单句号，未改变导航目标。因此 **PC-06 CLOSED**。

### 6.2 R02：新增引用未全部使用正确原文件坐标

- **优先级/状态**：P3，OPEN。技术修正的主要方向不因这些定位错误被否定，但不满足编写指南的精确行号要求。
- **位置与证据**：
  - `knowledge/06-training/parallelism-and-state.md:100` 把 QKV 交错定位到 E08 L1828–1829；这两行实际上是有无 output gate 的形状注释。应定位 E08 **L1840–1841**，并可加 **L1861–1867、L1887–1903** 支持常规拆分路径。错误坐标还出现在来源补充 `docs/research/batch-24-t06-01-sources.md:141`、复查记录 `docs/research/batch-24-post-close-review.md:27` 和 `sources/registry.yaml:4707`。
  - 正文 `:222` 将无 scaler 的 `return False` 定位为 E04 L775；原文件实际是 **L774**，L775 为空行。
  - 正文 `:219` 用 E03 L131–152 支持成功时放大 scale；实际乘以 growth_factor 的赋值为 **L153**。该区间应至少延伸至 L153，不能把 L152 的注释当作赋值行。
- **关闭条件**：同步修正文与对应来源补充/登记中的错误坐标，对固定 tag 实际字节重新 `nl -ba` 核对；技术措辞保持已核实的 MHA/布局边界。不修改历史审阅结论或给历史报告倒填新行号。本轮严格只新增本报告，没有代作者修正这些位置。

## 7. 回归抽查与元数据

- 同页 `:161`–`:172` 的状态责任矩阵仍区分参数、梯度、optimizer、scheduler、scaler、RNG、数据计数和并行身份；`:167` 的建议明确以 PyTorch 2.6 为例，不强行要求 Megatron 采用 PyTorch 状态格式。Megatron 的 hysteresis tracker 确实是其序列化状态（E03 L155–165），R01 的状态机修订应保留这一恢复要求。
- 同页 `:193`–`:210`、`:224`–`:226` 仍区分完整 step 截取和 mid-step；没有把“所有 checkpoint 必须保存梯度”或“跳步就不保存 scaler”引入正文。`:212` 将尝试迭代、成功更新、scheduler、consumed samples 分开，bf16 新说明也没有更改这些计数责任。
- 常见误解 `:251`–`:260` 和验证判据 `:237`–`:245` 没有重现旧的专家轴序/专家编号；它们要求声明组成员、shape、offset、计数和真实拓扑，和本次合成映射修正一致。除 R01 所述 scaler 轨迹外，抽查未发现新增技术矛盾。
- `knowledge/06-training/framework-execution.md:44`、`:48`、`:83`、`:92`、`:112` 继续把并行状态责任交给并行页，且将三个版本档案相互隔离；完整 step 截取条件中的“同一逻辑点”不是要求 scheduler 进度与 consumed samples 数值相同。其合法 overflow 跳步表述没有规定 Megatron 每次 overflow 必须缩小 scale，不与更正后的 tracker 规则冲突。
- 并行页 frontmatter `:1`–`:36`、训练入口 `:1`–`:34`、框架页 `:1`–`:40` 均可解析并通过本轮 schema/引用检查。稳定 ID 不变，正文仍为 draft，相关核对状态仍为 source_checked；不升级 reproduced，也不声称 generic 表示跨平台实测。
- 行号抽查结论不是“全部正确”：新引 E01/E02/E05/E06/E07 的关键定位符合原文件坐标；E03/E04/E08 的具体偏差已列 R02。原页其他未改动的上游断言和全部旧锚点不在此次全面重审范围内。

## 8. 隔离结构检查与工作区保护

使用原工作区解释器 `/Users/ywang2397/work/AI_reliability_knowledge_base/.venv/bin/python`（Python 3.11.15），不安装依赖。隔离目录：`/private/tmp/b24-post-close-recheck.hzN5Fw/isolated-repo`。没有复制 `.git`、`.venv`、`.agents`、`.codex`，并排除无关 `__pycache__`；隔离副本不是训练环境。

本轮实际执行命令：

```bash
make -C /private/tmp/b24-post-close-recheck.hzN5Fw/isolated-repo RUN_PYTHON=/Users/ywang2397/work/AI_reliability_knowledge_base/.venv/bin/python check
make -C /private/tmp/b24-post-close-recheck.hzN5Fw/isolated-repo RUN_PYTHON=/Users/ywang2397/work/AI_reliability_knowledge_base/.venv/bin/python build
```

首次装配隔离副本时排除了 build，两个 make 命令均 exit 2：`docs/first-fill-status.md` 引用的 `../build/catalog.json` 和 `../build/catalog.md` 在该副本缺失，校验各报 2 项结构错误。此结果如实保留为**隔离装配问题**，不误报为正文新回归。随后仅将原工作区现有的两个 build 文件复制到隔离副本作为起始快照，再执行相同两条命令：

| 检查 | 完整副本结果 | 输出摘要 |
|---|---|---|
| make check | PASS，exit 0 | `PASS: 103 content entries; 493 sources.` |
| make build | PASS，exit 0 | 同为 103 / 493；生成隔离副本的 `build/catalog.json` 和 `build/catalog.md`。 |

日志保留在隔离审阅目录：首次 `make-check.log` / `make-build.log`，补齐副本后 `make-check-complete.log` / `make-build-complete.log`。这些检查只验证结构和本地文件链接，不验证远端内容、技术判断或硬件效果。本轮没有改 `src/kb/`，没有运行 make test，没有执行训练、集群、checkpoint 保存/加载或恢复操作。

报告写入前已记录原工作区 515 个既有文件的 SHA-256 或符号链接目标，其中包含原工作区两个 build 文件；最终增删改核对另见下方执行回执。既有未提交修订全部保留，未提交或创建分支。

## 9. 后续关闭门槛

1. 由修订者处理 R01，保持 PyTorch/Megatron 分列及 bf16/常量 scaler 边界；随后对 B24-PC-04 / R01 做定向复核。
2. 处理 R02 的原文件坐标及对应补充记录，避免继续传播网页坐标或差一行的定位。
3. 只有 B24-PC-01–06 全部 CLOSED 且无新 OPEN P1/P2，才能把本次“交付后复查定向复核”改判通过。模型复核和整数控制流核验均不替代真实训练、集群恢复或硬件验证。

## 10. 执行回执

- 报告落盘后已复制进同一个隔离副本，重新运行第 8 节两条 make 命令：check/build 均 exit 0，均为 `103 content entries; 493 sources`；日志为 `make-check-with-report.log` / `make-build-with-report.log`。本报告的本地链接也在该轮检查范围内。
- 已将原工作区与本轮写入前的 515 文件快照逐项比对：**既有文件变更 0、删除 0；唯一新增为 `docs/research/batch-24-post-close-codex-recheck.md`**。包含原工作区两个 build 文件的实际字节比较；排除目录限根目录的 `.git`、`.venv`、`.agents`、`.codex`。`git diff --binary` 与本轮开始时留存值完全相同，原有全部 tracked 未提交改动未被改写。
- 最终结论仍为**暂不通过**，5 项 CLOSED / 1 项 OPEN；新增 1 项 OPEN P2、1 项 OPEN P3，无新增 P1。后续只需围绕本报告明确的修订与关闭条件继续，不把真实环境验证缺失包装成模型审阅已补足。
