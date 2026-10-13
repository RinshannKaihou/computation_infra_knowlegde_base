# 第二十批 T04-02 第五次定向复核（作者第五轮修订后）

- 审阅者：claude-opus-5-5（用户明确指定；不是既有 gpt-6.1-sol / xhigh 约定）。独立审阅角色，未改作者文件，未执行实测。
- 日期：2026-10-13
- 复核范围：只查 B20-C02 剩余的一处关闭条件，权威来源为 `batch-20-t04-02-claude-recheck-4.md` L84。其余 9 项已 CLOSED，本轮不重开。

**结论：T04-02 通过本次定向复核。本轮复核 1 项（C02），CLOSED 1 项。B20-C01–C10 合计 CLOSED 10 项，OPEN 0 项。** 本轮没有新增发现 ID。

## 输入核对（SHA-256 前 16 位）

| 文件 | 期望 | 实测 | 一致 |
|---|---|---|---|
| `knowledge/04-data-storage/local-and-shared-storage.md` | `2b489aa140af790d` | `2b489aa140af790d` | 是 |
| `docs/research/batch-20-review-fixes.md` | `98ba757b2794f862` | `98ba757b2794f862` | 是 |
| `docs/research/batch-20-t04-02-claude-recheck-4.md` | 未提供 | `ec8231f24056f251` | — |

## 外部来源

| 来源 | 本轮页面哈希前缀 | 核对内容 |
|---|---|---|
| [RFC 8881](https://datatracker.ietf.org/doc/html/rfc8881) | `7774e3fb520adf57`（与前几轮不同；datatracker 是动态渲染） | `id="section-8.4.2.1"` 恰好出现 1 次；所在标题为 `8.4.2.1. State Reclaim`（`<h5 id="name-state-reclaim">`） |

## B20-C02 — P1 / **CLOSED**

- 关闭条件（recheck-4 L84）：正文 L85 中 `[§8.4.2.1](…#section-8.4.2)` 改为 `[§8.4.2.1](…#section-8.4.2.1)`，且只改这一处 URL 片段。
- 正文现状：L85 证据列为 `[§8.4.2.1](https://datatracker.ietf.org/doc/html/rfc8881#section-8.4.2.1)`。全文已没有以 `#section-8.4.2)` 结尾的链接；RFC 8881 中指向 8.4.2 的片段只剩 `#section-8.4.2.1`。
- 语义：条件列写的是"服务器重启后 grace 期 reclaim（§8.4.2.1）"，链接文字、锚点和 RFC 子节标题 "State Reclaim" 三者现在一致。
- 修订映射第五轮节（`batch-20-review-fixes.md` L49–51）称"§8.4.2.1 锚点纠正为 #section-8.4.2.1"，并更正了第四轮映射的误述。这与正文现状相符。

## 非阻断项（沿用前次，本轮未复查是否处理，不影响通过）

- §1 表 L61 版本列未补 fcntl_locking(2) 页日期；"取证入口"未列 fcntl_locking(2)、flock(2)。（recheck-4 L90）
- 修订映射"改动位置索引"仍是旧行号；第五轮节没有给出实际行号，也没有附改后正文的 SHA-256（recheck-4 L108 要求过）。本轮靠用户提供的哈希和正文内容核对，不作为阻断。
- `verification.status: source_checked` 的 notes 应按实际核对范围重写；正文继续保持 `draft`。

## 验收对照（plans/full-coverage-backlog.yaml T04-02）

第 2 条（本地 vs NFS 的缓存/锁/可见性/恢复）此前只因 C02 未通过，现在 C02 已关闭，转为**通过**。第 1、3、4 条沿用 recheck-4 的结论，本轮未重新评估。

## 结论

**T04-02 通过第五次定向复核。B20-C01–C10 合计 CLOSED 10 项，OPEN 0 项。所有 P1 均已关闭。** 这次审阅通过只表示编辑与来源层面通过，不构成硬件、挂载或现场验证。正文 `status` 是否从 `draft` 提升，由作者和维护流程决定。
