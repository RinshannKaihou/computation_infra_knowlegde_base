# 第十二批替代复查记录（非 astra 审阅）

**历史记录提示（2026-10-08）：** 本文保留当时实际执行与关闭结论。当前 `gpt-6.1-sol / xhigh` 的[新审阅](batch-12-codex-review.md)及[修订/定向复核](batch-10-11-12-codex-recheck.md)已完成，4 项 P2、2 项 P3 全部关闭，本批在原审阅范围内通过；以新报告和[汇总](batch-10-11-12-codex-review-summary.md)为当前状态。

复查日期：2026-10-08。复查者：同环境只读探索子代理（**不是约定的 gpt-6-astra/xhigh 独立审阅**；当前环境无该模型派发能力，约定审阅义务保留）。修订与复核：Opus 主任务。范围：batch 12 三篇新正文（pd-disaggregation、node-acceptance-triage、checkpoint-integrity-evidence）、6 项新增来源登记与 9 项 notes 扩充、三份来源研究记录、导航/计划/README 一致性。

## 发现与处置

| 编号 | 级别 | 发现 | 处置 |
|---|---|---|---|
| F1 | P1 | source-audit 前向引用 batch-12-substitute-review.md，落盘前 `make check` 失败 | 本文件已创建，check 转绿后关闭 |
| F2 | P2 | backlog R2-13/14/15 仍为 `planned`，与已交付事实矛盾 | 已改为 `done`（done 仅表示草稿交付，不涉及 reviewed/reproduced） |
| F3 | P3 | README「已有正文」表漏收 batch 12 三篇 | 已补三行（PD 分离、节点验收、完整性） |
| F4 | P3 | README 首段"当前状态"实为首轮口径（41 篇/63 项），易与当前计数混淆 | 首段改为"首轮状态（2026-09-30 首轮交付时口径）"；计数句注明"截至 2026-10-08（batch 12 交付后）" |

无其他 P2 发现；抽查通过项如下。

## 复查代理抽查通过项（摘自其报告）

- **GitHub 固定 commit 行号抽查 10 处全部命中**：vllm@b17039b 的 disagg_prefill.md（L1–6 experimental、L10–13 动机、L15–16 反面声明、L50–54 定义、L88–96 扩展路径）、kv_transfer.py（L13–15/L67–70/L90–116）、factory.py（L146–203 恰 10 个 connector）、nixl_connector_usage.md（L164–166）、toy_proxy_server.py（L66–68/L163–171）；vllm-ascend@52d4acf 的 supported_features.md L27 原文与 feature_guide L101–105 限制条款；pytorch@1eba9b3（v2.6.0）的 serialization.py L184/L196–209、filesystem.py L582–595/L666–668、metadata.py L136–147；mind-cluster@44385c1 的 register_checker接口.md L39 与 framework_acp.py L111–136；ceph@caf3def 的 ceph.rst L1633–1637 与 conf.py L58–61。
- **网页可达性**：DCGM user-guide/learn、gpu-node-triage、hiascend toolboxug_0019/0020、arXiv 2402.06194v2、ceph docs 两页、python zipfile 页均 HTTP 200。
- **元数据与一致性**：三篇正文 id/type/domain 与路径匹配，procedure 的 applicability/verification 齐全；13 个 source_refs 全部存在于 registry；6 项新登记与 9 项 notes 扩充与 source-audit 逐项吻合；内部相对链接目标均存在；计数核实 69 entries / 84 sources 一致。
- **边界红线**：三篇均明示未实测；latest 动态页带观察日期、Ceph 另以固定 commit 佐证；昇腾教程版本漂移如实保留；Ceph 仅作例子；SuperBench 统计注明 Azure 特定集群且 MTBI 为仿真；完成判据明确"不写硬件完全无故障"。

## 修订后复核

主任务逐项核对修订：F1–F4 均已在对应文件落盘；`make check` / `make build` 通过（69 content entries / 84 sources），catalog 中三篇新条目标题与摘要已核对。**四项发现全部关闭。**

## 限制声明

本次为同环境只读替代复查，复查代理与编写者共享环境与工具，不构成约定的 gpt-6-astra/xhigh 独立审阅；本批的约定模型审阅义务保留至可派发环境。三篇正文保持 draft、限定范围 source_checked，无 reproduced，未执行任何环境验证。
