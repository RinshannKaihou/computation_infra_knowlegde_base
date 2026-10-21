# Batch 29 · T08-03 第二轮定向复核报告

## 会话元数据与结论

| 项目 | 记录 |
|---|---|
| 角色 / 范围 | 同一独立审阅者；只复核 C05、C10、N01 剩余关闭条件及本轮改动对已关闭项的影响，不编写或修订正文 |
| 实际执行模型 / 档位 | `gpt-6.1-sol / xhigh` |
| turn_context 核验方法 | 读取当前会话 JSONL 最新 `turn_context` 的 `model`、`effort`、`cwd`，并比对 `collaboration_mode.settings` |
| 核验结果 | `model=gpt-6.1-sol`、`effort=xhigh`、`cwd=/Users/ywang2397/work/AI_reliability_knowledge_base`；settings 中模型/档位一致，未调用其他模型或子代理 |
| 核验记录 | `/Users/ywang2397/.codex/sessions/2026/10/21/rollout-2026-10-21T19-22-05-01a15e32-6cde-73e0-aaeb-c0b856434851.jsonl`；最新 `turn_context.timestamp=2026-10-21T11:50:21.960Z` |
| 会话 ID | `01a15e32-6cde-73e0-aaeb-c0b856434851`；与初审及第一轮复核相同 |
| 日期 / 时区 | 2026-10-21 / Asia/Shanghai |
| 正文 | `knowledge/08-reliability/mitigation-and-recovery-principles.md`，145 行 |
| 正文 SHA-256 | `2a74a828371fda546a482a6614c146eb90d9007cf3ee645799a59a5af4bc75ba`；独立计算，与请求一致 |
| 第一轮复核依据 | `docs/research/batch-29-t08-03-codex-recheck.md`；SHA-256 `c825280c4aac19e85a6d0bb0c17b6d9b2ab3a88cee46833790675842f5a2a3c6` |
| 同步取证记录 | `docs/research/batch-29-t08-03-sources.md`；SHA-256 `901916e3c5096f71fa8ba0e8532e832acde2b2b7928368ec5952eb8982d3752a` |
| 写入范围 | 仅新增 `docs/research/batch-29-t08-03-codex-recheck-2.md`；不修改其他文件，不运行任何 make 目标 |
| 三项复核结果 | **CLOSED 2：C10、N01；OPEN 1：C05（沿用原 P2 标识）** |
| 新增发现 | 无 |
| 总体结论 | **暂不通过；仅余 C05 的固定源码链接与取证同步条件** |

以下正文行号均以本表新 SHA-256 为基准。本轮读取[第一轮复核报告](batch-29-t08-03-codex-recheck.md)、[当前正文](../../knowledge/08-reliability/mitigation-and-recovery-principles.md)与[取证记录](batch-29-t08-03-sources.md)，以原关闭条件逐项判断；相关技术证据沿用前轮已独立读取的同一固定 commit，未扩大为全篇上游重审或现场验证。

## 逐项复核表

| 发现 | 状态 | 理由与已满足部分 | 剩余关闭条件 |
|---|---|---|---|
| C05 · 原 P2 | **OPEN** | 正文 L85 现已明确 run.py 示例合并概括成员变化与失败，而 api.py 按 UNHEALTHY/FAILED、HEALTHY 等待新节点分别处理预算；写明按实现分支采信，并保留未核组合 unknown。这一差异说明与前轮固定源码证据一致，内容部分已满足。但 L85 的唯一 PyTorch 链接仍到 `elastic/run.html`，后接文件名/行号与“见登记 commit”，没有前轮明确要求的固定源码链接；取证 L21 仍只列 run.html 与文件名，未同步文档/实现差异及精确链接 | 在相关主张附近加入下文两个固定 commit 的原文件锚点，并在取证 L21 同步差异说明与定位。无需再改默认值、状态恢复前提或扩查其他组合 |
| C10 · P3 | **CLOSED** | 取证 L33 已补到 `../../knowledge/00-overview/design-targets-and-tradeoffs.md` 的实际 Markdown 链接，解析到 `overview.design-targets-and-tradeoffs`。目标正文 L57 分开总吞吐、净进展、重算量与错误预算，L97–119 定义 a/a' 折算；取证没有重新声称本篇使用该符号。前轮仅余的正文定位条件满足 | 无 |
| N01 · P2 | **CLOSED** | 正文 L91 区分控制/电源状态撤销与应用/证据状态重建：下电可再上电，但不保证应用状态恢复；按仅摘流/停止准入与驱逐/终止/复位区分对进程及易失状态的影响，并另列持久化/导出证据，要求执行前固定需保留的证据。已删除“下电不可逆”和“隔离必然保留现场”的二分法，且明确不把所有方式一律判为保留或清除全部现场 | 无；关闭范围是本段的动作/状态区分，不是对任意存储故障或具体设备复位行为的保证 |

### C05 仅余的定位与同步条件

[第一轮报告](batch-29-t08-03-codex-recheck.md)已经明确要求“在相关主张附近提供固定源码锚点；取证 L21 同步”。本轮新增文件名和行号解决了坐标说明，但没有完成直接链接；这不是本轮追加的新要求。正文和取证记录目前均没有指向 `github.com/pytorch/pytorch/blob/` 的链接。

需补齐的两个证据入口仍是前轮给出的同一固定 commit：

- [torch/distributed/run.py L157–165](https://github.com/pytorch/pytorch/blob/1eba9b3aa3c43f86f4a2c807ac8e12c4a7767340/torch/distributed/run.py#L157-L165)：Elastic 示例的概括及显式配置。
- [torch/distributed/elastic/agent/server/api.py L887–917](https://github.com/pytorch/pytorch/blob/1eba9b3aa3c43f86f4a2c807ac8e12c4a7767340/torch/distributed/elastic/agent/server/api.py#L887-L917)：扣预算与不扣预算的具体状态分支。

取证 L21 还需简要标出文档示例概括与实现分支的差异，不能仅重复“失败分支扣预算与 HEALTHY 扩容不扣”。registry 已提供固定 commit 身份，不必为关闭本项新增来源或更改版本。将上述链接只放在本复核报告内，不代替正文及取证记录补齐实际引用。

### 已关闭八项的受影响区域抽查

- **C01/C02**：正文 L79–83 仍保留幂等/原请求未应用证据、请求 ID 与幂等键区分、重复执行风险及三类流式中断边界；本轮预算段修订没有取消这些约束。
- **C03/C04**：L33/L85 的版本范围、Job/Pod v1.32 精确入口、Never/OnFailure 计数、默认值非推荐及不等同应用 attempt 的声明保留；未发现因补 PyTorch 差异说明而混用平台预算。
- **C06/C07**：L59 的潜在影响清单与 drain 成功不证明清空仍在；L91 保留不作无条件门槛排序、临时隔离不等于永久判坏及重启仍需六字段。节点摘除正文 L91–99/L170 的豁免、数据生命周期和证据保全责任未被本篇改写为新的执行规则。
- **C08/C09**：L68/L118 的按故障模式判断与物理冗余 unknown、L111 的有条件重算及质量/一致性结果判据保留。没有以本轮电源/进程状态分类替代这些效果验证条件。

上述八项维持 CLOSED；抽查不构成对其全部上游实现重新审计。L99/L102 的质量降级业务判据、L114 的恢复退出条件和 L134 的授权边界也保持原口径。

## 新增发现

无。本轮没有对未修改部分提出新的审阅要求。C05 的残余只属于前轮已列出的定位与同步条件；C10、N01 不再开放。

## 总体结论

**第二轮暂不通过。本轮三项中 C10、N01 CLOSED，C05 OPEN；累计 C01–C10 与 N01 共 11 项中 10 项 CLOSED、1 项 OPEN，无新增发现。**

C05 的技术差异说明已经补齐，后续只需补两个固定源码链接并同步取证 L21，再按新的正文 SHA-256 复核；不要求重复已完成的内容修订或开展环境实验。

本轮用项目 `.venv/bin/python -B` 做只读结构核查：正文 frontmatter 通过 Draft 2020-12 schema；10 项 source_refs、9 项 related_ids、5 项 evidence_refs 均存在，related_ids 不含来源 ID；正文 19 处本地相对链接和取证记录 5 处本地相对链接均可解析。这不检查引用语义或证明硬件兼容性，亦不能替代上述固定源码链接的缺失。

本会话仅新增本报告，未修改正文、来源或历史报告，未运行任何 make 目标，未执行节点/进程操作、服务、负载、故障注入或质量评估。正文继续保持 `draft / source_checked`；模型审阅不替代真实环境验证，本结论不代表 Batch 29 全批验收。

写入前后只读文件指纹对比还观察到 `plans/topic-coverage.yaml` 内容变化；本会话未对该文件执行写入，保留现状，不纳入本轮审阅。
