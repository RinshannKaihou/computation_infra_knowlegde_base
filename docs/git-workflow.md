# Git 版本管理

知识库使用 Git 保存正文、来源登记、计划、审阅记录、模板与校验工具。初始基线是 2026-10-08 工作目录的快照；此前的批次过程以已有文档为依据，不补造历史提交。

默认分支为 `main`。`.gitignore` 排除 `.venv/`、缓存、覆盖率数据、`build/` 和本地凭证文件；`.gitattributes` 约定 Markdown、YAML、JSON、Python 等文本源文件使用 LF 换行。构建产物通过 `make build` 重建。

## 日常修改

先查看当前分支和未提交内容，再为一个主题或批次建立分支。以下分支名仅为示例：

```bash
git status
git switch -c content/checkpoint-update
```

编辑源文件，保留稳定 ID、来源与历史审阅模型记录。内容修改后运行：

```bash
make check
make build
```

修改 `src/kb/` 时还需运行 `make test`。这些检查不代替技术审阅或硬件验证。

检查差异，按具体路径暂存本次主题的文件，再检查实际提交内容：

```bash
git diff
git add knowledge/04-data-storage/checkpoint-integrity-evidence.md
git diff --cached
git diff --cached --check
git commit -m "docs(storage): clarify checkpoint integrity evidence"
```

路径和提交说明须按实际改动替换；关联的来源登记、导航、计划和审阅记录应一起提交。提交说明写清楚本次改动及原因。提交前确认未包含凭证、未处理的敏感信息、大型日志或实时集群状态；忽略规则不能识别正文中的敏感信息。

## 查看历史与撤销已提交的改动

```bash
git log --oneline --decorate -10
git show HEAD
```

需要撤销已提交的改动时，先检查目标提交及当前工作目录，再使用 `git revert <commit>` 创建反向提交并重新校验。`<commit>` 是待替换的提交 ID；不要为撤销内容而重写已有共享历史。

## 远程备份与协作

本仓库已配置 GitHub 远程 [origin](https://github.com/RinshannKaihou/computation_infra_knowlegde_base)。提交前用 `git remote -v` 确认当前 checkout 的地址；推送前先 fetch 并核对分支差异，通过检查后按已有授权执行 `git push origin main` 或推送当前工作分支。本地提交不等于远程备份，推送后核对远程提交身份；不以本文替代实际推送授权。

共享分支通过评审合入 `main`；共享 `main` 不使用强制推送。本项目原创内容采用 [Apache License 2.0](../LICENSE)，第三方许可与署名要求仍按来源登记保留。
