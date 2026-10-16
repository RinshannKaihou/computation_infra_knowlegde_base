# Batch 21 补交 T05-01 第三十二次定向复核

## 1. 结论、角色与范围

- 日期：2026-10-17（Asia/Shanghai）。执行者：当前本地 Codex CLI 会话，以独立审阅角色核对作者第三十二轮修订，与正文作者角色分开；未派发子代理或其他模型。
- **模型核验：** 实读 `~/.codex/sessions/2026/10/17/rollout-2026-10-17T03-39-47-01a1463a-4804-7271-ad8a-07210bba2879.jsonl`，会话 ID 为 `01a1463a-4804-7271-ad8a-07210bba2879`。逐条解析 `turn_context`，本轮所见一条记录为 UTC `2026-10-16T19:39:52.415Z`（本地 2026-10-17 03:39:52），单一 `model=gpt-6.1-sol`、`effort=xhigh`；`collaboration_mode.settings` 同为 `gpt-6.1-sol / xhigh`。检查审阅者可见 `output_text`，未检出执行回退标记；提示词、工具参数及引用中讨论标记的文字不当作发生回退。`session_meta` 记录 originator=`codex_exec`、CLI=`0.157.1`、model_provider=`custom`。**此核验仅确认本地执行元数据与可见输出，不是独立服务端路由、底层计算或供应商证明。** 不追改历史模型记录；摘录保存在仓库外审计目录。
- 唯一复核范围为 **B21-C33 的 C33-2a/C33-2b/C33-3 剩余关闭条件**：以[第二十六次复核](batch-21-t05-01-codex-recheck-26.md) L106 为权威条件，以[第三十一次复核](batch-21-t05-01-codex-recheck-31.md) §4 C33（L74–86）为精确剩余范围。**C30/C31/C32/C34 均已 CLOSED，直接沿用，不重开、不重审；C33-1 逐对象表、UB 分道、worker 七键/算法、既有 M-LIB 字段及旧判据删除、S1/R1 等已认可子条件不重复索取。** 子项不是新增发现 ID。
- **B21-C33 仍 OPEN（P2）；第三十二次定向复核不通过。** 隐藏祖先的可达性前提及超出规则范围的 K1 已补；纳入宿主 field 4 的 root 换算获认可。先拼完整目标、再求覆盖挂载内相对路径也已替代重复拼接，但新定义的 `D（rootfs＋源同路径）` 仍直接与目标容器进程 mountinfo 的 field 5 比前缀，未落实宿主 CLI 路径到容器进程根坐标的转换。这属于前轮明确留下的“同一参照系”条件，不新增问题范围；相应“方法已交付、只缺 filled 值”的口径仍不能完整成立。
- 本轮只新增本报告，不修改或删除其他仓库文件，不提交、不建分支。作者修订映射仅为索引，技术判断依据为当前 HEAD 正文、本轮实读手册及明确沿用的既有固定 Ascend 证据。
- **未执行实测，不构成硬件验证。** 未安装组件、拉取/构建镜像、生成 SBOM、运行容器、查询设备、读取现场 mountinfo/st_dev 或接入集群；未做挂载、访问、负向、更新、回退、恢复实测。下文路径例子只是合成的规则推演，不是现场状态或挂载实验。

| 原发现 | 优先级 | 本轮状态 | 处理边界 |
|---|---|---|---|
| B21-C30 | 沿用 | CLOSED | 既有关闭结论，范围外，不重审 |
| B21-C31 | 沿用 | CLOSED | 既有关闭结论，范围外，不重审 |
| B21-C32 | P2 | CLOSED | 直接沿用第 31 次；不重新索取成员、层或单卡映射证据 |
| B21-C33 | P2 | OPEN | 正文 L109/L111：目标路径与 field 5 的坐标基准；正文 L111/L171、作者来源 L12/L17 的相应完成度口径 |
| B21-C34 | P1 | CLOSED | 直接沿用第 31 次；不因 C33 另行阻断或重复计数 |

P1/P2 沿用既有审阅分级，不是生产漏洞或事故严重性评级。

## 2. 输入身份（SHA-256）

开始时工作区干净，HEAD 为作者提交 `890b5c67ec789c1d7909a1e868387730a7499c59`。核对 `git show 890b5c6` 的提交身份、文件清单及正文/来源记录的文字差异；该提交同时纳入第 31 次报告，不把提交收录报告本身当作关闭证据。以下为整文件原始字节摘要；正文行号采用本轮快照的物理行号。

| 输入 | 本轮 SHA-256 | 审阅定位 |
|---|---|---|
| [第 31 次复核](batch-21-t05-01-codex-recheck-31.md) | `9a728b7efbfd58cb6d487602545f1696b22bde67217793f7a348744cf35c62e7` | §4 C33 精确剩余条件；§5 acceptance 与 C32/C34 关闭边界 |
| [第 26 次复核](batch-21-t05-01-codex-recheck-26.md) | `ade616897c367afb566c3076ffc8b36f2dbf6c95af8558d74af8d537ed3402b0` | L106 权威条件；§3 固定 Ascend 证据的已认可边界 |
| [作者修订映射](batch-21-review-fixes.md) | `b9b306b2d671ff3e8058bd0fc21bf7caba7f97fd9e8165f43d4bfd8fc27848bc` | L432–438“第三十二轮修订”，仅作索引 |
| [修订后正文](../../knowledge/05-cluster-platform/container-image-runtime-baseline.md) | `a1415ef81da69daafc0f291ea1f8f70c2538af6e47a7bef937e890707f45f01e` | §3，重点 L107/L109–111；公共分类 L121、待确认 L171；仍为 `reference / draft / source_checked` |
| [作者来源记录](batch-21-t05-01-sources.md) | `869508624c55c3689e96452ec00e1d6b22fa621d94dcdfa4c19d6761e2c3708d` | L12、L17、L45 |
| [来源登记](../../sources/registry.yaml) | `9897387f4a8fb0900411e5b8c70eb840be84fe844c86c6cd6937878f9d94235b` | mountinfo L333–343；相关 Ascend 固定实现登记；全文解析为 446 项 |
| [任务计划](../../plans/full-coverage-backlog.yaml) | `5f9bcf865b8c77e13cc8ee5f1c03140c37b86f558d8227d8bb2080249f4fcfc3` | T05-01 L5386 起；acceptance L5403–5406，只读 |
| [README](../../README.md) | `21759d9b1fc122d94bb3c3990d1b2e621c53dabc7ba022852545cae7b2329b44` | 开始约定、校验与交付边界 |
| [写作指南](../authoring-guide.md) | `75ee28d1aca7a4ac1d56ae493856037770a14fcdac27fa9b662451cee169a801` | 来源/验证状态及本地 CLI 审阅约定 |
| [归属边界](../../content-outline.md) | `ed9033d2f53fa504fc05e55b221697dd7a1d14c5adaf58f8cc0a6613f8fe7046` | 05.1 容器、镜像、设备暴露主归属 |
| [元数据 schema](../../schemas/content.schema.json) | `b60b8d9ccb8728f034607901124c4206f5dc705ca824e31ce0ab5615523d0147` | `draft` 与 `source_checked` 不等于硬件验证 |

先读 README/写作指南，再依次读第 31 次、第 26 次、作者本轮映射/提交差异、修订后正文、作者来源记录与相关登记。适用目录未发现额外嵌套 AGENTS 指令。不将其他已关闭主题扩展为本轮复审对象。

## 3. 一次源取证

### 3.1 实际通道、失败与限制

本轮实际打开 [man7 proc_pid_mountinfo(5)](https://man7.org/linux/man-pages/man5/proc_pid_mountinfo.5.html)，网页读取通道 `open` 成功返回 HTML 正文抽取，共 125 个抽取行；实读 DESCRIPTION 字段 (1)–(5)，特别是 (2) 的堆叠/可达性括注及父条目不显示的说明、(3)/(4)/(5) 语义，并核对 COLOPHON。页面自述为 **Linux man-pages 6.19**、手册日期 **2026-02-08**、HTML 生成 **2026-09-09**，与既有登记身份相符。抽取行只用于本次网页定位，不当作上游源文件物理行号。

本机另实际尝试同一 URL 的只读 HTTPS GET，命令形态为 `curl --proto '=https' --proto-redir '=https' --fail --show-error --silent --location --connect-timeout 10 --max-time 45 URL -o FILE -w 'http_code=%{http_code};ssl_verify_result=%{ssl_verify_result};size_download=%{size_download}'`；保留默认 TLS 校验，未用 `-k`、自定解析、IP 绕行或提权。**本次 curl 退出码 28、HTTP 000、下载 0 字节、`ssl_verify_result=1`，错误为 `SSL connection timeout`。** 不是成功的 TLS/HTTP 原始正文获取，也不改记成 DNS 失败；本轮没有取得可计算 SHA-256 的手册原始响应，不沿用第 31 次的 HTML 摘要冒充本轮下载结果。

技术核对依据为上述成功的网页正文读取，不依赖 curl 可达性。网页抽取可能经过缓存/转换，不是本机原始 HTTP 字节或上游当时实时版本的独立证明。取证记录 `source-access.json`、curl 状态/错误位于仓库外审计目录；不把临时目录当永久证据仓库。仅保存链接、访问元数据与原创判断，不镜像手册全文；登记的许可边界不变。

Ascend 固定 commit `44385c13d7b1d87def35f1604e8be4d16de6ca4e` 的默认 base/hook/CLI 相关实现，按授权沿用第 26 次 §3 及第 31 次已认可结论。**本轮没有重新下载或审计这些实现**，也不声称新增完成全部 CLI、产品变体或 DCMI 审计。作者来源 L12/L45 与相关登记仅用于核对身份和口径，不替代本轮手册实读。

### 3.2 实读位置与支持边界

| 点 | 精确一次源位置 | 本轮核对结果及边界 |
|---|---|---|
| S01 | [proc_pid_mountinfo(5)](https://man7.org/linux/man-pages/man5/proc_pid_mountinfo.5.html)，DESCRIPTION (2)；网页抽取 L37–60 | 同位置堆叠须结合父子 ID 与隐藏祖先判断可达性；进程根之外的父挂载记录可能不显示。支持本轮加入的可达性前提与无法判明时不肯定关联，不证明现场祖先链完整 |
| S02 | 同页 DESCRIPTION (3)/(4)，网页抽取 L62–66 | field 3 表示文件系统的 st_dev；field 4 表示该挂载在文件系统内的根。支持把宿主自身 field 4 纳入坐标计算；具体公式为字段语义推论，不是手册给出的算法或执行结果 |
| S03 | 同页 DESCRIPTION (5)，网页抽取 L68–69 | field 5 以该进程的根为路径参照。它不是自动带上宿主 bundle/rootfs 前缀的 CLI 目标路径；这是 §4 保留 OPEN 的直接字段依据 |

`source-access.json` 记录访问身份与通道限制。以下反例与正例在 `method-cases.json` 中另存合成路径运算结果；只是对文中规则的静态推演，不创建挂载、不读取 `/proc`，不把推演当产品兼容或现场验证。

## 4. 逐项复核与剩余关闭条件

### B21-C33 — P2 / OPEN

**权威条件：** 第 26 次 L106；第 31 次 §4 C33-2a/C33-2b/C33-3，尤其 L81/L86 的完整目标与同一参照系要求。**本轮位置：** 正文 L107、L109–111、L171；作者来源 L12/L17。C33-1 及既有逐库字段、旧挂载成功判据删除、CLI 旁证边界直接保留，不重审、不重复索取。

#### C33-2a：遮蔽可达性已满足；路径基准部分满足，仍 OPEN

1. **可达性子条件 / CLOSED。** L109 已在最长前缀、同位置 top-most 之后，明确验证最长前缀祖先未被堆叠隐藏，排除隐藏祖先下字面更长的旧子挂载。S01 支持该前提；文中还将所选规则下缺可达性证据列 K2，将祖先链不完整等超出可判情形列 K1。前轮 A/A2 隐藏旧 B 的反例因而不再被“路径更长”直接判为有效覆盖。不要求实现全部挂载情形或补现场父子 ID。
2. **先拼目标、再求覆盖内相对路径的改动 / 认可。** L109 先拼 `D/r` 再选覆盖挂载；L111 用完整目标去掉所选挂载点前缀求相对路径，且禁止在更具体挂载点后再次拼原 r。在同一坐标的前提下，若 `r=plugins/libx.so`、覆盖挂载点为 `D/plugins`，库在覆盖挂载内的相对路径是 `libx.so`，不是再拼一个 `plugins`。前轮指出的重复/遗漏路径段问题已修正，不重复要求这项改动。
3. **仍未满足的是 D 与 field 5 的根坐标连接。** L107 已区分“CLI 目标（rootfs＋同路径）→容器内同路径”；但 L109 随后把 **`D（rootfs＋源同路径）`** 定为原定目标目录，并直接要求目标容器进程 mountinfo 的 field 5 是 `D/r` 的前缀。S03 明确 field 5 相对该进程的根，不能默认带宿主 CLI 的 rootfs 前缀。“同一参照系”这句话没有交付两者之间的转换，也未声明只覆盖宿主 rootfs 前缀等于 `/` 的特殊前置。L111 的“去掉覆盖挂载点前缀”随之仍可能在不同坐标之间操作。**这不是要求新的挂载情形或现场 rootfs 值，而是第 31 次已经留下的路径参照系设计条件。**

**方法反例推演，非现场路径或输出：** 仅设 CLI rootfs 为 `/srv/bundle/rootfs`、所选源目录为 `/usr/local/Ascend/driver/lib64`、`r=plugins/libx.so`。依当前 D 定义，完整目标成为 `/srv/bundle/rootfs/usr/local/Ascend/driver/lib64/plugins/libx.so`；目标容器进程根下该目录挂载的 field 5 若为 `/usr/local/Ascend/driver/lib64`，它不是前一字符串的路径前缀。即使该条目可达、field 3/4 均正确，当前步骤也不能据此选中它；可能退到根挂载或无法关联。这只是已认可的父目录一次 bind，不需复杂堆叠，不能用“祖先链不完整”的 K1 限缩吸收。若先换到容器进程根坐标，完整目标为 `/usr/local/Ascend/driver/lib64/plugins/libx.so`，该父挂载内相对路径才是 `plugins/libx.so`。这个对照只展示坐标缺口，不声称该条目真实存在。

#### C33-2b：root 换算 / CLOSED

L110 已记录 M_host 的 field 3/4/5，并改用 `R_fs = join(M_host.field4, relative(P_src, M_host.field5))`，规范化为文件系统内部路径；不再把仅相对挂载点的子路径直接当 root。其例子 `/drivers` 与 `lib64` 拼得 `/drivers/lib64`，而不是旧规则的 `lib64` 或 `/lib64`。所选源目录关联继续要求容器条目 field 3 等于宿主 st_dev、field 4 等于 R_fs，并明确该公式为字段语义推论。**本轮按 S02 认可这项换算，不因 C33-2a 目标路径尚未闭合而重开它。** 不要求采集现场 st_dev/root，也不将字段一致扩大为全部挂载情形或库内容真实性的证明。

#### C33-3：口径同步 / 部分满足，仍 OPEN

- **已同步部分 / 认可。** 正文 L109/L111、待确认 L171、作者来源 L17 已区分“所选规则内可达性证据不足 K2”与“超出可判情形 K1”；正文 L111 与作者 L12 同步提到纳入宿主 field 4 的换算。未执行 K3、未读产品变体 K1、已交付规则下现场未采 K2 的既有分列保留，不要求全部改成 K1。
- **仍未同步的完成度 / OPEN。** 正文 L111 与作者 L12 仍将逐库 M-LIB 整体归为“方法已交付、只缺 filled 值”；L171/L17 对所选记录仍只列 filled 值/实际挂载证据 K2。上述目标坐标连接尚缺，属于当前所选规则的设计问题，不能由现场未采 K2 或超出祖先链规则的 K1 代替。可修正目标坐标规则后保留“方法已交付”，或在未修正时对这一个未完成方法明列 K1 并停止肯定来源关联；不必把其余已认可子条件改为未完成。

**精确剩余关闭条件：** 仅需把 CLI 宿主 rootfs 目标与目标容器进程 mountinfo 的 field 5 显式放入同一坐标：例如分别定义宿主 CLI 目标与进程根内目标，交付两者的转换，再以进程根内完整目标 `D/r` 选择可达覆盖挂载，并在同一坐标求覆盖挂载内相对路径；也可诚实声明可成立的受限前置及范围外 K1，不能只写“同一参照系”而继续跨根比较。随后同步正文 L111/L171 与作者来源 L12/L17 的完成度：确有未完成方法记 K1，已有方法下缺现场值记 K2，未执行记 K3，证据不足不得判关联成立。**保留本轮已认可的遮蔽可达性、root 换算和避免重复拼接修正；不再索取现场 mountinfo/st_dev、挂载实测、新权限、全部产品白名单、完整 CLI 审计或 C33-1 的已认可交付。**

## 5. Acceptance 与最终计数

| T05-01 acceptance | 本轮判定 | 原发现对应 |
|---|---|---|
| L5403：镜像 digest、基础系统/依赖层、构建输入、SBOM/签名、拉取策略的作用与限制 | 沿用既有完整通过，不重审，不据此宣称已有供应链系统 | C30 CLOSED，范围外 |
| L5404：固定运行时/NVIDIA 版本，分开驱动、库、设备/环境/挂载、权限与框架映射 | 沿用第 31 次完整通过，不重审，不新增扫描或映射要求 | C31/C32 CLOSED，范围外 |
| L5405：Ascend 固定实现/目标组合独立取证，GPU/NPU 与 digest 兼容边界 | 部分满足，未完整通过：可达性与 root 换算已补；目标坐标基准及相应完成度口径仍缺 | C33 OPEN |
| L5406：最小清单、异常/隔离、对照与源案例，非已验证处方 | 沿用第 31 次完整通过；C34 不重新承担 C33 的问题，不宣称实测 | C34 CLOSED，范围外 |

四条 acceptance：**3 完整通过（均沿用既有通过）/ 1 未完整通过**。本轮唯一受审原发现为 C33，**0 CLOSED / 1 OPEN（开放 0 P1、1 P2）**；C33 的 root 换算等子项关闭不额外计为原发现。C32/C34 直接沿用 CLOSED，连同本轮 C33，三项累计 **2 CLOSED / 1 OPEN（已关闭 1 P1、1 P2）**；包括 C30/C31 的五个原发现总计 **4 CLOSED / 1 OPEN**，不新增发现 ID。**第三十二次定向复核不通过，不能宣称 T05-01 全部通过。** 唯一剩余原发现仍为 C33，阻断不是网络失败、现场值未采、未实测或未扩展全部变体。

## 6. 结构校验与写入审计

- 仓库外审计目录：`/private/tmp/b21-t05-01-recheck32-dXDssf`。建立独立 `validation` 副本并保留既有 `build/`，排除 `.git`、虚拟环境、node_modules 与 Python/工具缓存；原仓库不运行结构检查或会更新生成文件的构建。
- 写入前在副本用原仓库虚拟环境 Python、`PYTHONDONTWRITEBYTECODE=1` 执行 `make check build`，**均 PASS，96 content entries / 446 sources**，日志 `validation-before.log`。这些检查仅验证结构与本地链接，不验证技术正确性、远程正文或硬件。
- 报告写入后同步到同一副本，执行 `make check build`，**均 PASS，96 content entries / 446 sources**，日志 `validation-after.log`；生成的 `build/catalog.json` / `build/catalog.md` 只在副本更新。本节补记后再同步复验，最终记录使用 `validation-final.log`，不在原仓库构建。
- 逐字节 SHA-256 审计覆盖 **428 个既有文件**，包含原 `build/` 两个生成文件：无修改、无删除，唯一新增为本报告；§2 的 **11 个输入文件全部未变**，正文工作区字节与 HEAD 对应文件相同。HEAD 仍为 `890b5c67ec789c1d7909a1e868387730a7499c59`，Git 状态只有本报告未跟踪；`git diff --check` 与报告单独行尾空白检查均无报错。基线、输入与结果分别为 `baseline.json`、`input-hashes.json`、`audit-result.json`。
- 结束时再次解析同一会话 JSONL，仍为一条 `turn_context`（UTC `2026-10-16T19:39:52.415Z`），单一模型/档位及协作设置均为 `gpt-6.1-sol / xhigh`，审阅者可见输出未检出执行回退标记。保存 `model-initial.json` / `model-final.json`；核验局限仍为 §1 的本地元数据，不扩张为服务端证明。
- 未运行 `make test`：未改 `src/kb/` 或测试代码。不安装或执行上游组件、不修改正文/来源/登记/计划状态，不提交、不建分支。

**最终技术结论：B21-C33 OPEN；C33-2a 的目标坐标基准与 C33-3 的对应口径仍需修订，C33-2b CLOSED。C30/C31/C32/C34 保持 CLOSED。后续只复核上述精确剩余条件。**
