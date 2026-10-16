# Batch 21 补交 T05-01 第三十三次定向复核

## 1. 结论、角色与范围

- 日期：2026-10-17（Asia/Shanghai）。执行者：当前本地 Codex CLI 会话，以独立审阅角色核对作者第三十三轮修订，与正文作者角色分开；未派发子代理或其他模型。
- **模型核验：** 实读 `~/.codex/sessions/2026/10/17/rollout-2026-10-17T03-52-40-01a14646-15cb-7663-9426-7d8c204a0276.jsonl`，会话 ID 为 `01a14646-15cb-7663-9426-7d8c204a0276`。逐条解析本会话 `turn_context`，所见一条记录为 UTC `2026-10-16T19:52:46.596Z`（本地 2026-10-17 03:52:46），单一 `model=gpt-6.1-sol`、`effort=xhigh`；`collaboration_mode.settings` 同为 `gpt-6.1-sol / xhigh`。检查审阅者可见 `output_text`，未检出执行回退标记；提示词、引用及工具参数中讨论 fallback 的文字不当作实际回退。`session_meta` 为 originator=`codex_exec`、CLI=`0.157.1`、model_provider=`custom`。**此核验仅确认本地执行元数据与可见输出，不是独立服务端路由、底层计算或供应商证明。** 不追改历史模型记录；最小核验摘录保存在仓库外审计目录。
- 唯一复核范围为 **B21-C33 的剩余关闭条件：C33-2a 的 CLI rootfs↔容器进程根坐标连接，以及 C33-3 的相应完成度口径**。以[第二十六次复核](batch-21-t05-01-codex-recheck-26.md) L106 为权威条件，以[第三十二次复核](batch-21-t05-01-codex-recheck-32.md) §4 为精确剩余范围。**C30/C31/C32/C34 已 CLOSED，直接沿用，不重开、不重审；C33-1 逐对象表、遮蔽可达性、C33-2b 的 R_fs 换算、避免重复拼接等已认可子条件不重复索取。** 子项不是新增发现 ID。
- **B21-C33 CLOSED（P2）；第三十三次定向复核通过。** 正文已显式区分宿主 CLI 目标 `D_cli` 与进程根内目标 `D_proc`，交付去掉宿主 rootfs 前缀的转换，使用 `D_proc/r` 选择覆盖挂载并计算覆盖内相对路径；文件项也改用进程根内路径匹配 field 5。正文与作者来源记录的“所选方法已交付、filled 值未采 K2”口径随之成立，没有把尚缺的方法伪装为仅缺现场值。
- 本轮只新增本报告，不修改或删除其他仓库文件，不提交、不建分支。作者修订映射只作索引，不作技术关闭证据。
- **未执行实测，不构成硬件验证。** 未安装组件、拉取或构建镜像、生成 SBOM、运行容器、查询设备、接入集群、读取现场 mountinfo/st_dev，未做挂载、访问、负向、更新、回退或恢复实验。§4 的路径例子仅为合成数据的静态运算，不是现场路径或输出。

| 原发现 | 优先级 | 本轮状态 | 处理边界 |
|---|---|---|---|
| B21-C30 | 沿用 | CLOSED | 既有关闭结论，范围外，不重审 |
| B21-C31 | 沿用 | CLOSED | 既有关闭结论，范围外，不重审 |
| B21-C32 | P2 | CLOSED | 沿用第 32 次确认的既有关闭状态，不重审 |
| B21-C33 | P2 | CLOSED | 本轮核对正文 L107/L109/L111/L171 与作者来源 L12/L17 的剩余条件 |
| B21-C34 | P1 | CLOSED | 沿用第 32 次确认的既有关闭状态，不重审、不重复计数 |

P1/P2 沿用既有审阅分级，不是生产漏洞或事故严重性评级。

## 2. 输入身份（SHA-256）

开始时工作区干净，HEAD 为作者提交 `9c273999dd59ed5875cc199007470ad5d3fb59e2`。实读 `git show 9c27399` 的提交身份、文件清单与本轮差异：正文 L107/L109/L111、作者来源 L12 及修订映射末节；该提交另收录第 32 次报告，不把收录报告本身当关闭证据。以下均为整文件原始字节 SHA-256；仓库定位使用本轮快照的物理行号。

| 输入 | 本轮 SHA-256 | 审阅定位 |
|---|---|---|
| [第 32 次复核](batch-21-t05-01-codex-recheck-32.md) | `f6a8f9b739377997e4c829461c65b420818c3976237dc1cd0e018ba7ab86676f` | §4 C33-2a 第 3 条、C33-3 与精确剩余条件；§5 acceptance |
| [第 26 次复核](batch-21-t05-01-codex-recheck-26.md) | `ade616897c367afb566c3076ffc8b36f2dbf6c95af8558d74af8d537ed3402b0` | L106 权威关闭条件及已认可边界 |
| [作者修订映射](batch-21-review-fixes.md) | `9958771ecb3252cbef1fefe7193c01881216c48926eec422a4a440d0230ad3e3` | L440–444“第三十三轮修订”，仅索引 |
| [修订后正文](../../knowledge/05-cluster-platform/container-image-runtime-baseline.md) | `96d8364e63a8197e4c477fa278c99bdf7cbbb42c444e4f077454da06e7caa39f` | §3 M-LIB，L107/L109–111；待确认 L171；仍为 `reference / draft / source_checked` |
| [作者来源记录](batch-21-t05-01-sources.md) | `dc6dbbc022b547f0abd50b78afa180c8ec5c53bf875644f2a2c24dce4ab5c108` | L12、L17、L45 |
| [来源登记](../../sources/registry.yaml) | `9897387f4a8fb0900411e5b8c70eb840be84fe844c86c6cd6937878f9d94235b` | mountinfo 6.19 与固定 Ascend CLI 相关既有登记；无新增来源 |
| [任务验收](../../plans/full-coverage-backlog.yaml) | `5f9bcf865b8c77e13cc8ee5f1c03140c37b86f558d8227d8bb2080249f4fcfc3` | T05-01，L5403–5406 |
| [README](../../README.md) | `21759d9b1fc122d94bb3c3990d1b2e621c53dabc7ba022852545cae7b2329b44` | 内容/构建与验证边界 |
| [写作指南](../authoring-guide.md) | `75ee28d1aca7a4ac1d56ae493856037770a14fcdac27fa9b662451cee169a801` | 来源、验证状态与本地 CLI 审阅约定 |
| [归属边界](../../content-outline.md) | `ed9033d2f53fa504fc05e55b221697dd7a1d14c5adaf58f8cc0a6613f8fe7046` | 05.1 容器、镜像与设备暴露的主归属 |
| [元数据 schema](../../schemas/content.schema.json) | `b60b8d9ccb8728f034607901124c4206f5dc705ca824e31ce0ab5615523d0147` | 编辑状态与验证状态分离 |

先读 README/写作指南，再按用户顺序读第 32 次、第 26 次、作者第 33 轮映射与提交差异、修订正文、作者来源记录；之后核对相关登记/验收并取证。适用目录未发现额外嵌套 AGENTS 指令。不将已关闭主题扩展为本轮复审对象。

## 3. 一次源取证

### 3.1 实际通道、失败与限制

本轮网页读取通道 `open` 成功返回 [man7 proc_pid_mountinfo(5)](https://man7.org/linux/man-pages/man5/proc_pid_mountinfo.5.html) 的 HTML 正文抽取，共 125 个抽取行；实读 DESCRIPTION，重点为 (5) 的进程根参照，并核对 COLOPHON。页面自述为 **Linux man-pages 6.19**、手册日期 **2026-02-08**、HTML 生成 **2026-09-09**。网页抽取行只作本轮阅读定位，不当作上游源文件物理行号或原始 HTTP 字节证明。

同轮 `open` 访问固定 Ascend `u_mount.c` 的 GitHub 页面失败，返回 **Cache miss**；随后 GitHub 连接器 `fetch_file` 按 commit `44385c13d7b1d87def35f1604e8be4d16de6ca4e`、原路径、L45–240 成功返回源码，Git blob SHA 为 `d85fd8155a1805edaf509b047c6441bcdc603e12`。不是仅沿用前轮摘要；本轮重新定位 `MountFile` 与 `MountDir` 的目标计算。

另对 man7 与同 commit/path 的 `raw.githubusercontent.com` 各实际发起一次只读 HTTPS GET。命令形态为 `curl --proto '=https' --proto-redir '=https' --fail --silent --show-error --location --connect-timeout 8 --max-time 20 URL -o FILE -w 'http_code=%{http_code};ssl_verify_result=%{ssl_verify_result};size_download=%{size_download}'`，保留默认 TLS 校验，未用 `-k`、自定解析、IP 绕行或提权。

| 目标 | 实际 curl 结果 | 取证处理 |
|---|---|---|
| man7 精确页面 | 退出码 28；HTTP 000；下载 0 字节；`ssl_verify_result=1`；`SSL connection timeout` | 未取得手册原始响应，不记成 DNS 失败或成功 TLS；本轮以成功的网页正文读取核对字段，不编造响应 SHA-256 |
| Ascend 固定 `u_mount.c` 原文件 | 退出码 0；HTTP 200；`ssl_verify_result=0`；6102 字节 | 本轮取得原文件，SHA-256=`3af78451fd2d9989e9e2b6798aa60abc5de094b39e387d0bcd97c99f4ebc8463`；按原文件物理行号定位，并独立计算 Git blob SHA-1，与连接器身份相同 |

网络失败不构成技术不通过。网页抽取可能经缓存/转换；连接器 Git blob SHA-1 与原文件 SHA-256 是不同摘要，不混用。访问状态、错误、最小身份记录见仓库外 `source-access.json` 与 curl 日志；临时目录不是永久证据仓库。仅在报告保留精确链接、必要定位与原创判断，不扩大既有许可结论；未执行下载的上游源码。

### 3.2 实读位置与支持边界

| 点 | 精确一次源位置 | 本轮核对结果及边界 |
|---|---|---|
| S01 | [proc_pid_mountinfo(5)](https://man7.org/linux/man-pages/man5/proc_pid_mountinfo.5.html)，DESCRIPTION (5)，网页抽取 L68–69 | field 5 的挂载点路径以该进程根为参照，不自动包含宿主 bundle/rootfs 前缀。支持用进程根内目标比较 field 5；不证明现场进程根或挂载值 |
| S02 | [u_mount.c@44385c13](https://github.com/Ascend/mind-cluster/blob/44385c13d7b1d87def35f1604e8be4d16de6ca4e/component/ascend-docker-runtime/cli/src/u_mount.c#L84-L151)，原文件 L94、L131（分别位于 `MountFile`、`MountDir`） | 两处目标字符串均由 rootfs 在前、源路径在后拼接，随后以源和目标调用挂载函数。支持正文的 CLI 侧目标定义；与 S01 连接后的去前缀转换是所选同路径规则下的坐标推论，不冒充源码或手册直接给出的 mountinfo 算法 |

C33 的其他固定 Ascend 实现与已认可子条件按用户授权沿用既有结论，不借这次定位扩展为完整 CLI、产品变体或 DCMI 审计。作者来源 L12/L45 与登记只核身份和口径，不能代替上述本轮实读。

## 4. 逐项复核与剩余关闭条件

### B21-C33 — P2 / CLOSED

**权威条件：** 第 26 次 L106；**精确剩余条件：** 第 32 次 §4 C33-2a 第 3 条、C33-3 及末尾关闭条件。**本轮位置：** 正文 L107/L109/L111/L171；作者来源 L12/L17。

#### C33-2a：CLI rootfs↔进程根坐标连接 / CLOSED

1. **两端坐标已分列，转换已交付。** L109 将 `D_cli` 明确定义为宿主 bundle rootfs 路径加源路径，将 `D_proc` 定义为源路径本身，并写明从 `D_cli` 去掉宿主 rootfs 前缀得到 `D_proc`。S02 核到 CLI 的拼接，S01 核到 field 5 的参照，二者不再直接跨根比较；该转换在本轮所选默认同路径记录中足以连接两端，不要求新增产品情形或填现场 rootfs 值。
2. **后续选择与相对路径均在进程根内。** L109 先拼 `D_proc/r`，明确不以 `D_cli` 直接匹配 field 5；L111 也改为从 `D_proc/r` 去掉所选覆盖挂载点前缀求覆盖内相对路径。正文已不再出现旧 `D（rootfs＋源同路径）` 或 `D/r` 的操作定义。既有可达性前提、先拼完整目标及禁止二次拼 r 均保留；这里仅确认修订没有丢失已认可限定，不重新审理这些子条件。
3. **文件项不留旧坐标入口。** L107 对④明确按进程根内目标路径（＝源路径本身）匹配 field 5；L111 的④继续引用公共 M-LIB 判据。不能将仍用于记录 CLI 目标的“rootfs＋同路径”误读为 field 5 比较输入。

**静态规则对照，非现场证据：** 沿用第 32 次反例的合成 rootfs `/srv/bundle/rootfs`、源目录 `/usr/local/Ascend/driver/lib64` 与 `r=plugins/libx.so`。本轮 `D_cli` 为 `/srv/bundle/rootfs/usr/local/Ascend/driver/lib64`，去前缀后 `D_proc` 为 `/usr/local/Ascend/driver/lib64`，完整进程内目标为 `/usr/local/Ascend/driver/lib64/plugins/libx.so`：

| 合成记录 | 进程根内 field 5 | 按修订规则得到的覆盖内相对路径/匹配 |
|---|---|---|
| 父目录一次 bind | `/usr/local/Ascend/driver/lib64` | `plugins/libx.so`；不再把宿主 rootfs 前缀带入匹配 |
| 已确认可达的更具体覆盖挂载 | `/usr/local/Ascend/driver/lib64/plugins` | `libx.so`；不重复追加 `plugins` |
| ④ 文件项，源为 `/usr/local/bin/npu-smi` | `/usr/local/bin/npu-smi` | CLI 目标去 rootfs 前缀后与该 field 5 相同 |

以上仅用合成字符串进行路径运算与断言，3 个对照均通过，记录在 `method-cases.json`；没有构造真实 mountinfo、检查实际可达性或执行挂载。第 32 次暴露的跨坐标反例在同一简单父 bind 情形下已消除，不以扩大测试范围换取关闭。

#### C33-3：正文与作者来源完成度口径 / CLOSED

- **方法交付口径已同步。** 正文 L111 与作者来源 L12 均在“逐对象/逐库 M-LIB 方法已交付”范围中补入 CLI 宿主 rootfs 目标、容器进程根内 field 5 的坐标分列与转换判据；本轮 L109/L111 确有相应方法，不再只是作者声明，也不必把已补齐的方法继续列 K1。
- **剩余未知仍分类一致。** 正文 L171 与作者来源 L17 保留未读变体/超出可判情形为 K1、所选逐对象/逐库 filled 值及实际挂载证据未采为 K2、现场挂载/CLI 执行与部署产物核对未做为 K3。两处无需机械复写完整公式；其缺项范围与 L111/L12 相容。正文 L109/L111 继续规定证据不足不能肯定关联，没有把方法交付扩大为现场结果成立或硬件验证。
- 本轮无需再要求改动 L171/L17：第 32 次的矛盾来自所选规则尚缺坐标连接，现在该缺段已补；不是靠把同一设计缺口改称现场 K2 关闭，也没有要求完成全部挂载情形、全部产品白名单或新增执行权限。

| C33 子条件 | 本轮处理 | 状态 |
|---|---|---|
| C33-1 逐对象表及已认可字段 | 直接沿用，不重审、不重复索取 | CLOSED |
| C33-2a 遮蔽可达性、先拼完整目标/避免重复拼接 | 沿用第 32 次认可；本轮只确认保留 | CLOSED |
| C33-2a 剩余 CLI rootfs↔进程根坐标连接 | 按 S01/S02 与当前正文独立核对 | CLOSED |
| C33-2b 纳入宿主 field 4 的 R_fs 换算 | 直接沿用第 32 次 CLOSED，不重新索取证明 | CLOSED |
| C33-3 相应完成度口径 | 核对 L111/L171 与作者来源 L12/L17 | CLOSED |

**精确剩余关闭条件：无。** 第 26 次 L106 的既有认可交付保留，第 32 次留下的两个缺口均已补齐，B21-C33 可以关闭。未采 mountinfo/st_dev、未实测、未读全部变体仍如实保留，但按本次判定口径不构成阻断，不新增发现 ID。

## 5. Acceptance 与最终计数

| T05-01 acceptance | 本轮判定 | 原发现对应 |
|---|---|---|
| L5403：镜像 digest、基础系统/依赖层、构建输入、SBOM/签名、拉取策略的作用与限制 | 沿用既有完整通过，不重审，不宣称已有供应链系统 | C30 CLOSED，范围外 |
| L5404：固定运行时/NVIDIA 版本，分开驱动、库、设备/环境/挂载、权限与框架映射 | 沿用既有完整通过，不重审 | C31/C32 CLOSED，范围外 |
| L5405：Ascend 固定实现/目标组合独立取证，GPU/NPU 与 digest 兼容边界 | 本轮剩余条件补齐后完整通过；不把所选记录方法等同于现场兼容交集或执行成功 | C33 CLOSED |
| L5406：最小清单、异常/隔离、对照与源案例，非已验证处方 | 沿用既有完整通过，不重审、不宣称实测 | C34 CLOSED，范围外 |

四条 acceptance：**4 完整通过 / 0 未完整通过**，其中 3 条沿用既有通过、1 条因本轮 C33 关闭而补齐。本轮唯一受审原发现为 C33，**1 CLOSED / 0 OPEN（本轮关闭 1 P2）**。C32/C34 直接沿用 CLOSED，连同 C33，三项累计 **3 CLOSED / 0 OPEN（已关闭 1 P1、2 P2）**；包括 C30/C31 的五个原发现总计 **5 CLOSED / 0 OPEN**，无新增发现 ID。**第三十三次定向复核通过；T05-01 在既定审阅/acceptance 范围内通过，不代表硬件验证或所有平台/变体兼容。** 不修改正文状态、计划状态或历史模型记录。

## 6. 结构校验与写入审计

- 仓库外审计目录：`/private/tmp/b21-t05-01-recheck33-8an8rr6m`。建立独立 `validation` 副本，保留原 `build/`，排除 `.git`、虚拟环境、node_modules 与 Python/工具缓存；原仓库不运行结构检查或会更新生成文件的构建。
- 写入前在该副本以原仓库虚拟环境 Python、`PYTHONDONTWRITEBYTECODE=1` 执行 `make check build`，**均 PASS，96 content entries / 446 sources**，记录为 `validation-before.log`。检查只验证结构与本地链接，不验证技术正确性、远程正文或硬件。
- 报告纳入同一副本后执行 `make check build`，**均 PASS，96 content entries / 446 sources**，记录为 `validation-after.log`；本节补记后再同步复验，最终记录为 `validation-final.log`。生成的 `build/catalog.json` / `build/catalog.md` 只在副本更新。
- 逐字节 SHA-256 审计覆盖 **429 个既有文件**（包含原 `build/` 两个生成文件）：无修改、无删除，唯一新增为本报告；§2 的 **11 个输入全部未变**，正文工作区字节与 HEAD 对应文件相同。HEAD 仍为 `9c273999dd59ed5875cc199007470ad5d3fb59e2`，Git 状态只有本报告未跟踪；`git diff --check` 与报告行尾空白检查均无报错。基线、输入、结果分别为 `baseline.json`、`input-hashes.json`、`audit-result.json`；初始状态与作者差异为 `initial-git-status.txt`、`git-show-9c27399.txt`。
- 结束时再次解析同一会话 JSONL，仍为一条 `turn_context`（UTC `2026-10-16T19:52:46.596Z`），单一模型/档位及协作设置均为 `gpt-6.1-sol / xhigh`，审阅者可见输出未检出执行回退标记；保存 `model-initial.json` / `model-final.json`。核验局限仍为 §1 的本地元数据，不扩大为服务端证明。
- 未运行 `make test`：未修改 `src/kb/` 或测试代码。上游组件仅只读取证，未安装或执行；不提交、不建分支。

**最终技术结论：B21-C33 CLOSED；C33-2a 剩余坐标连接与 C33-3 完成度口径均满足。C30/C31/C32/C34 保持 CLOSED；T05-01 的五个原发现全部关闭，四条 acceptance 在既定范围内完整通过。**
