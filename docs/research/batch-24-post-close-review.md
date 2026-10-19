# Batch 24 交付后复查与订正（2026-10-19）

状态：**复查发现全部关闭**。复查发现 6 项（B24-PC-01–06）；[第一次定向复核](batch-24-post-close-codex-recheck.md)关闭 PC-01/02/03/05/06，并新增 R01（P2）、R02（P3）；修订轮二处理后，[第二次定向复核](batch-24-post-close-codex-recheck-2.md)关闭 PC-04、R01、R02，无新增问题。两轮复核均为 codex `gpt-6.1-sol / xhigh`（会话 `2026-10-19T09-26-41`、`2026-10-19T09-42-49`，`turn_context` 核验单一模型/档位）。正文仍为 `draft`，未做真实环境验证。

## 角色与模型

| 角色 | 执行者 | 说明 |
|---|---|---|
| Batch 24 原正文、来源记录与收尾账面编写者 | GLM-5.3 | 用户 2026-10-19 告知；原批次记录未写明编写模型，此处补记 |
| Batch 24 原审阅者 | codex `gpt-6.1-sol / xhigh` | 22 轮（初审 4＋定向复核 18） |
| 本次复查与修订 | `claude-opus-5-5`（Claude Code 会话，用户要求） | 复查者同时承担本次修订，不作为独立审阅；关闭以下方定向复核为准 |
| 本次定向复核 | codex `gpt-6.1-sol / xhigh` | 见复核报告 |

## 原审阅链核对

- `~/.codex/sessions/2026/10/18–19` 中工作目录为本仓库的 `codex exec` 会话共 22 个（2026-10-18 20:54 至 2026-10-19 01:37），`turn_context` 均为 `gpt-6.1-sol`、effort `xhigh`、sandbox `workspace-write`，与 22 份 review/recheck 报告一一对应。
- 从各会话的 `apply_patch` 与后续脚本写入中还原报告内容，与提交版本逐行比对：22 份报告的内容均来自对应 Codex 会话自身（T06-01 初审报告末尾 36 行 URL/SHA-256 表由该会话内脚本从其取证缓存生成，其余行均能在会话写入中逐字找到），作者没有改动审阅结论。

## 发现与处理

| 编号 | 优先级 | 位置 | 问题与证据 | 关闭条件 | 处理 |
|---|---|---|---|---|---|
| B24-PC-01 | P2 | `plans/topic-coverage.yaml` 05.7/06.2/06.3/06.4；`plans/full-coverage-backlog.yaml` 对应 `gap_assignments`；`docs/topic-coverage-audit.md` 05.7、06.2–06.4 行 | 首版收尾把四个主题改为 covered，但 `gaps` 未清理、`evidence_refs` 未加入新条目（06.4 为空列表）、`followup_priority` 未改；backlog 中 05.7-G1/G2、06.2-G1–G3、06.3-G1–G3、06.4-G1–G3 全部仍为 open；覆盖盘点表四行仍是交付前口径；误置于文末的自写复核条目与 Batch 23 记录方式不一致 | 按交付内容逐个判定缺口；关闭的缺口在 backlog 置 closed、在盘点清单移出；新条目 ID 进入 evidence_refs；盘点表、路线图与清单一致 | 关闭 05.7-G1/G2、06.2-G1/G2、06.3-G1/G2/G3、06.4-G1 共 8 项；05.7、06.3 为 covered/maintain，新增 `cluster-platform.control-plane-recovery`、`training.framework-execution`；盘点表四行与头段 Batch 24 条目重写，删除文末误置条目；路线图同步 |
| B24-PC-02 | P2 | 同上 06.2、06.4 | 06.2-G3 由 T06-01＋T06-06 承担，06.4-G2 由 T06-04、06.4-G3 由 T06-03＋T06-04 承担，T06-04/T06-06 属 Batch 25 且为 planned；按 Batch 23 先例（05.7 因 T05-10 未交付保持 partial），06.2、06.4 不能记为 covered | 依赖后续任务的缺口保持 open，主题保持 partial | 06.2 保持 partial（仅 G3 开放，注明 T06-06）；06.4 由 missing 升为 partial，`evidence_refs` 加入 `training.pretraining-and-finetuning`，G2/G3 开放并注明 T06-04 |
| B24-PC-03 | P2 | `knowledge/06-training/parallelism-and-state.md` 身份样例、expert grid 段、选型表 EP 行 | 正文把专家轴序约定为 `[pp, ep, edp, etp]` 并称 Megatron 实际 order "未核对，unknown"；但所引 `parallel_state.py` 同一文件可以判定：默认 `order="tp-cp-ep-dp-pp"`（L617），专家 generator 取 `expert_order`（L886–893），排在前面的维度变化最快（L292 文档式）。按该规则 rank 37 的 EP 组应为 {33,35,37,39}（节点内）、expert DP 组为 {37,45,53,61}（跨节点），与正文恰好对调；选型表 EP 行同样对调（实际 EP 组 {0,2,4,6} 在节点内，expert DP 组 {0,8,…,56} 跨 8 节点）。以该文件 `RankGenerator` 对两组合成配置做纯算术复算，稠密组与正文一致，专家组与上述结论一致。本地专家编号也可由 `moe_layer.py` L181–194 判定（`ep_rank × num_local_experts`），不必作为本库约定 | 专家侧组员、持有专家与选型表 EP 行按 Megatron 默认轴序与源码分配规则给出，并注明非默认 `order` 时会改变 | 已改写：身份样例注明与默认轴序一致；expert grid 段改为短段＋表格，rank 37 的 EP 组 {33,35,37,39}、expert DP 组 {37,45,53,61}、持有 expert 64–95，shard 示例同步为 `expert_64`；公共放置约定的专家轴序改为 `[pp, edp, ep, etp]`；EP 行改为 `rank=8×edp+2×ep+etp` 及对应放置 |
| B24-PC-04 | P2 | 同文"梯度累积窗口内的完整执行契约（三情形）"表及其引导句 | 表格把 PyTorch `GradScaler.update()` 语义与 Megatron `train_step` 的 `skipped_iter` 分支并成一个 scaler 列，overflow 行写成"按 backoff 缩小 scale"。Megatron core_v0.19.2 的 fp16 路径使用自有 `DynamicGradScaler`：overflow 时 growth tracker 归零、hysteresis tracker 减 1，tracker ≤ 0 才缩小 scale，tracker 只在完成一个 `growth_interval` 增长窗口时恢复（grad_scaler.py L131–153；arguments.py L2917）〔首轮把这一规则误写为“连续 N 次 overflow”，见下文修订轮二〕；scaler 只在 `optimizer.step()` 的 `prepare_grads` 中更新（optimizer.py L741–774）；bf16 且未设 `--loss-scale` 时不创建 scaler（optimizer/__init__.py L638–662）。这违反本页"不跨实现拼接"的边界 | 两个实现的 scaler 语义分列，Megatron 列引用其固定 tag 源码 | 引导句改指 Megatron 自有 scaler；表格拆为 PyTorch 2.6 与 Megatron core_v0.19.2 两列，并补 bf16 无 scaler 的说明 |
| B24-PC-05 | P3 | 同文身份样例"参数身份示例"行、expert shard 示例 | `layers.20.self_attention.qkv` 写作 row-shard、offset = 1×(hidden/2)：融合 QKV 的输出维为 3×hidden（MHA），TP=2 时第 1 片 offset 应为 3×hidden/2；Megatron 的 `linear_qkv` 是 column-parallel（gpt_layer_specs.py L324/L444），沿 dim 0（输出维）切分，对应 PyTorch ColwiseParallel，称 row-shard 与本页 TP 行的 row/column 术语冲突；expert gate_proj 的"第 0 维 row-shard"同样 | offset 与切分术语正确，并说明 Megatron QKV 按 query group 交错存放 | 改为 `linear_qkv.weight`、全局 `[3×hidden, hidden]`、本地 `[3×hidden/2, hidden]`、offset 3×hidden/2，注明交错布局（attention.py L1840–1841〔首轮误标为 L1828–1829，见修订轮二〕）；expert shard 改称沿 dim 0 切分（column-parallel） |
| B24-PC-06 | P3 | `knowledge/06-training/index.md` 两条新增导航 | 句末为"。。" | 单个句号 | 已改 |

新引用的固定 tag 文件与 SHA-256 记入 `src.nvidia.megatron-lm-core-v0.19.2` 的 notes（同 tag 新增冻结文件，不新增登记 ID）；`parallel_state.py` 的 SHA-256 与原审阅轮 U12 一致。

## 修订轮二（第一次定向复核发现处理）

第一次定向复核报告：[batch-24-post-close-codex-recheck](batch-24-post-close-codex-recheck.md)。

- **B24-PC-04 / R01（P2）**：首轮修订把 Megatron `DynamicGradScaler` 写成“连续 `--hysteresis` 次 overflow 后才缩小、单次 overflow 默认不缩小”，这是错的。实际状态机（grad_scaler.py L131–153）：overflow 时 growth tracker 归零、hysteresis tracker 减 1，tracker ≤ 0 即按 backoff 缩小（下限 `--min-loss-scale`，默认 1.0，arguments.py L2913）；有限步只增加 growth tracker，累计满 `growth_interval` 个连续有限步才放大 scale 并恢复 hysteresis tracker。所以触发缩小的 overflow 不必连续，tracker 耗尽后每次 overflow 都缩小，直到下一个增长窗口完成。三情形表的成功/overflow 两格已按此改写；表后补充 `ConstantGradScaler` 不调整 scale（L43–52），以及动态 scaler 的 `state_dict` 含 hysteresis tracker（L155–165）。
- **B24-PC-R02（P3）**：坐标更正——QKV 交错注释为 attention.py L1840–1841（另引 L1861–1867、L1887–1903），无 scaler 时 `return False` 为 optimizer.py L774，放大 scale 的赋值为 grad_scaler.py L153。正文、本记录、T06-01 来源补充与登记 notes 已同步，均按固定 tag raw 文件 `nl -ba` 重新核对。

## 已记录、本次未处理

- T06-01 复核轮次的文字口径不一：来源审计表写"初审＋5 轮定向复核"，实际为 6 份 recheck 报告（审阅节另注"第六轮关闭最后单项"）。
- 可读性：T05-10 etcd 行单元格约 1,000 字，T06-01/T06-03 有超过 1,500 字的单段；本次只重排了 PC-03 涉及的 expert grid 段。
- `plans/topic-coverage.yaml` 的 `summary` 计数与 `batch_planning`（completed_batches 01–22）自 2026-10-08 起未随批次更新，非 Batch 24 引入，本次不改。
- 原批次两处作者否定断言（core_v0.19.2 无模型级示例、无 `--tensor-model-parallel-size` CLI 定义）已在原审阅链中纠正，见 T06-03/T06-02 来源记录。

## 结构检查

修订后 `make check`：PASS（103 content entries / 493 sources）；`make build`：PASS（生成 build/catalog.json 与 build/catalog.md）。它们只证明结构与本地链接，不证明技术正确性或远程内容。
