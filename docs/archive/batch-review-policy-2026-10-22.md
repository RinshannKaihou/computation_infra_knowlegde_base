# 已退役的批次审阅政策（2026-10-22 归档）

> **历史材料，已于 2026-10-22 退役。** 以下保留归档前的政策原文，用于解释历史批次的审阅记录。文中的指定模型、推理档位、本地 CLI、fallback 处置与批次执行要求均不再作为当前或后续工作的默认规则；历史计划和记录不自动产生待执行任务。

当前约定见 [AGENTS.md](../../AGENTS.md) 和[内容使用与维护指南](../authoring-guide.md)。既有审阅报告继续保留当时实际执行的模型、角色和结论，不追改历史记录。

归档范围为本次归档前 `AGENTS.md` 的 review agreement 条目，以及 `docs/authoring-guide.md` 的完整第 7 节。下面两段原文保持原有字节；其中行内路径与命令是历史文本，不是当前执行指令。

## AGENTS.md 原 review agreement

- Current review agreement (user update, 2026-10-08): use `gpt-6.1-sol / xhigh` for batch review. Preserve the actual models in historical records. Record findings and require revision plus targeted recheck before declaring review passed; model review does not establish hardware verification.

## 原内容编写指南第 7 节

## 7. 批次审阅约定

2026-10-08 用户更新：当前及后续批次的约定审阅模型为 `gpt-6.1-sol / xhigh`。本次适用于 batch 10、11、12，替代此前保留的 astra 审阅义务；历史报告按实际使用模型保留，不追改为新模型。

2026-10-13 用户更新（Batch 20 起试用）：优先调用 `claude-opus-5-5` 审阅；若出现 fallback（含 `[frontier_llm]` 标记、实际执行模型与指定不一致、或认证/路由失败），则该轮审阅弃用并切换回 `gpt-6.1-sol / xhigh`。每轮审阅必须核验：输出元数据的实际模型为单一指定模型，且结果文本无 fallback 标记；核验方法与结论记入审计。被弃用的轮次不留档、不引用、不计入轮次。试用期间任一轮回退不改变本约定；用户可随时终止试用并恢复纯 `gpt-6.1-sol / xhigh` 约定。

审阅者重新读取正文与精确上游证据，核对技术主张、平台/版本边界、元数据、来源与导航，记录发现 ID、优先级、受影响位置、证据和关闭条件。来源核对、报告交付、问题修订和定向复核分别记录；开放的高优先级问题未解决前不声明该批审阅通过。修订后由同一审阅者定向复核。审阅执行者与正文编写者的角色及实际模型要如实记录，模型审阅不替代真实环境验证。

2026-10-16 用户更新：审阅执行方式固定为本地 CLI，不经过 OpenCode 子代理的模型参数。claude 模型用 `claude -p`（Claude Code 非交互模式）执行；gpt 模型用 Codex 方法执行（`codex exec --skip-git-repo-check -m <model> --config model_reasoning_effort="<effort>" --sandbox <mode>`，长提示词经 stdin 文件传入；方法详见 `~/.claude/skills/codex/SKILL.md`）。审阅写报告需落盘时用 `--sandbox workspace-write`，且只新增当轮报告文件；纯核对可用 `--sandbox read-only`。推理档位缺省 `xhigh`，以本节模型约定为准，不另行向用户提问。注意：codex-cli 0.157.1 已移除 `--full-auto`（沿用旧 flag 会 exit 2 启动失败），非交互自动放行改用 `--approve-for-me`，且该 flag 与 `--sandbox` 互斥（自带 workspace-write，不要同传）；SKILL.md 中的旧 flag 示例以实测 `codex exec --help` 为准。
