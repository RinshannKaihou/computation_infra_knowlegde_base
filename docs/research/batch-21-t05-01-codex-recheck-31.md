# Batch 21 补交 T05-01 第三十一次定向复核

## 1. 结论、角色与范围

- 日期：2026-10-17（Asia/Shanghai）。执行者：当前本地 Codex CLI 会话，以独立审阅角色核对作者第三十一轮修订，与正文作者角色分开；未派发子代理或其他模型。
- **模型核验：** 实读 `~/.codex/sessions/2026/10/17/rollout-2026-10-17T03-25-47-01a1462d-78a3-7eb0-af1d-512449eb3657.jsonl`，会话 ID 为 `01a1462d-78a3-7eb0-af1d-512449eb3657`；逐条解析 `turn_context`，所见时间为 UTC `2026-10-16T19:25:53.377Z`（本地 2026-10-17 03:25:53），单一 `model=gpt-6.1-sol`、`effort=xhigh`，`collaboration_mode.settings` 同样为 `gpt-6.1-sol / xhigh`。检查本会话审阅者 `output_text`，未检出执行回退标记；提示词、引用或工具参数中讨论标记的文字不当作发生回退。`session_meta` 记录 originator=`codex_exec`、CLI=`0.157.1`、model_provider=`custom`。**本结论只核验本地执行元数据及可见输出，不是独立服务端路由、底层计算或供应商证明。** 不追改历史模型记录；摘录保存于仓库外审计目录。
- 唯一复核范围为 **B21-C32、B21-C33、B21-C34 的剩余关闭条件**，以[第二十六次复核](batch-21-t05-01-codex-recheck-26.md) L91、L106、L121 为权威条件，以[第三十次复核](batch-21-t05-01-codex-recheck-30.md) §4 为本轮前精确剩余范围；[初审](batch-21-t05-01-codex-review.md)仅继承 ID、优先级与职责边界。**C30/C31 已 CLOSED，不重开；C32-2 单卡 uuid 映射、C33-1 逐对象表/UB 分道、worker 算法、C34-1 两端配置、C34-2 resize 设计、S1/R1 公共规则均不重复索取。** 子项编号不是新发现 ID。
- **本轮 2 CLOSED / 1 OPEN（开放项：0 P1、1 P2）；第三十一次定向复核仍不通过。** C32 的成员 JSON 键、同路径跨层候选/摘要关联与 whiteout K1 分类在其明示范围内闭合，C34 的 C32 依赖随之关闭。C33 的父挂载设计有进展，但宿主 root 坐标换算漏掉宿主条目的 field 4，遮蔽处理仍未落实同页 field 2 的祖先可达前提，故 C33-2/3 不能关闭。
- 只新增本报告，不修改或删除其他仓库文件，不提交、不建分支。作者映射只作索引，关闭依据为修订后正文与本轮实读一次源；不修改正文、来源记录、登记或计划状态。
- **未执行实测，不构成硬件验证。** 未拉取/构建镜像、生成 SBOM、执行上游组件、运行容器、查询设备、读取现场 mountinfo 或接入集群；未开展访问、负向、更新、回退、恢复实测。阻断只限方法/记录设计与口径，不是现场值未采、未审全部 cataloger、未扩展多卡/index/NPU/whiteout 实现或网络取证失败。

| 原发现 | 优先级 | 本轮状态 | 关闭证据或精确剩余范围 |
|---|---|---|---|
| B21-C32 | P2 | CLOSED | 正文 L33、L62、L74、L167；作者来源记录 L17：JSON 键与 Go 字段分开，候选/层序/digest 规则及 whiteout K1 同步；C32-2 沿用 |
| B21-C33 | P2 | OPEN | 正文 L107、L167；作者来源记录 L12、L17：M-LIB 的宿主 root 换算、可达父挂载/遮蔽及相应 K1/K2 完成度 |
| B21-C34 | P1 | CLOSED | 正文 L146、L150 等沿用共同方法/分类；C32-1/3 本轮闭合，唯一剩余依赖解除；不另背 C33 |

优先级沿用初审：P1 为核心验收主干阻断，P2 为必须补齐的方法、证据或版本边界，不是生产漏洞或事故严重性评级。

## 2. 输入身份（SHA-256）

开始时工作区干净，HEAD 为作者提交 `dc27e7b8f5cf60ea21775dc2a206b72d0a5df6ca`。检查 `git show dc27e7b` 的文件清单与差异；该提交还纳入第 30 次报告，不把其纳入提交本身当作本轮关闭证据。修订后正文按当前 HEAD 工作区字节审阅。以下为完整文件原始字节摘要；正文行号均为该快照物理行号。

| 输入 | 本轮 SHA-256 | 审阅定位 |
|---|---|---|
| [第三十次复核](batch-21-t05-01-codex-recheck-30.md) | `ff3c9e58db8775327cd4815ab02119e234884d84964126a7ad43e492058c8c68` | §4 精确剩余条件；§5 acceptance 与既有关闭边界 |
| [第二十六次复核](batch-21-t05-01-codex-recheck-26.md) | `ade616897c367afb566c3076ffc8b36f2dbf6c95af8558d74af8d537ed3402b0` | L91、L106、L121 权威条件 |
| [初审报告](batch-21-t05-01-codex-review.md) | `341775efc62d7b8d46659c2d272aa31ae301b0cd1db47623ebe86490b80e34b5` | C32/C33/C34 的 ID、优先级与分工 |
| [作者修订映射](batch-21-review-fixes.md) | `9d5764892df1763e777a9f6b6d8c533c1e9b1e702fc37941349ca28e9dfbc385` | L423–430“第三十一轮修订”，仅作索引 |
| [修订后正文](../../knowledge/05-cluster-platform/container-image-runtime-baseline.md) | `762e882daa4318431dd91f906cefbc7fcf0a1e5e8dc5e009708ff5cbd6b30c83` | L33、L62、L74、L107、L117–131、L146–167；仍为 `reference / draft / source_checked` |
| [作者来源记录](batch-21-t05-01-sources.md) | `7b4c600681c54571bf91a31330afe75994ec9fb067636e15e12d96a18c1ccc77` | L12、L17、L38–45 |
| [任务计划](../../plans/full-coverage-backlog.yaml) | `5f9bcf865b8c77e13cc8ee5f1c03140c37b86f558d8227d8bb2080249f4fcfc3` | T05-01 L5386–5430，acceptance L5403–5406 |
| [来源登记](../../sources/registry.yaml) | `9897387f4a8fb0900411e5b8c70eb840be84fe844c86c6cd6937878f9d94235b` | mountinfo L333–343、Syft L5314–5324；全文解析为 446 项 |

先读 [README](../../README.md) 与[写作指南](../authoring-guide.md)，并核对[归属边界](../../content-outline.md)和[元数据 schema](../../schemas/content.schema.json)；四者摘要依次为 `21759d9b1fc122d94bb3c3990d1b2e621c53dabc7ba022852545cae7b2329b44`、`75ee28d1aca7a4ac1d56ae493856037770a14fcdac27fa9b662451cee169a801`、`ed9033d2f53fa504fc05e55b221697dd7a1d14c5adaf58f8cc0a6613f8fe7046`、`b60b8d9ccb8728f034607901124c4206f5dc705ca824e31ce0ab5615523d0147`。适用目录未发现额外嵌套 AGENTS 指令。

## 3. 一次源取证

### 3.1 实际通道、失败与限制

本轮用本机 `curl` 只读 HTTPS GET 获取固定 tag 原文件与 man7 页，命令形态为 `curl --proto '=https' --proto-redir '=https' --fail --show-error --silent --location --connect-timeout 10 --max-time 45 URL -o FILE -w '%{http_code}'`；保留默认 TLS 校验，未用 `-k`、自定解析或 IP 绕行。**16 次全部 exit 0 / HTTP 200**：Syft 同 tag 文件 12 份、OCI v1.1.1 文件 3 份、man7 页 1 份。逐份实读相关代码/文字，不凭 HTTP 状态判技术通过。请求 URL、退出码、字节数、SHA-256 与错误字段保存在仓库外 `downloads.json`，原文件在 `upstream/`；未执行下载代码。

Web `open` 另实读 man7 的 DESCRIPTION / COLOPHON；打开 Syft `dpkg.go`、`model/file.go` 的网页抽取均返回 `Cache miss`，这两份文件随后均经上述 curl 成功取得并实读。失败仅是网页通道缓存/抽取失败，**不是文件不存在、技术不通过或本机 curl 失败**。本轮无 curl/DNS 失败，不把历史轮次失败算入本轮。

源码锚点由下载原文件的物理行号确定，不使用网页抽取行号充当 GitHub `#L`。tag 按任务固定，不宣称完成 tag 签名/不可变性审计。man7 页自述 man-pages **6.19**、手册日期 **2026-02-08**、HTML 生成 **2026-09-09**，URL 本身可变，故另记本轮字节摘要。仓库外临时副本不是永久证据存档；报告只保留链接、摘要与原创判断，不搬入外部全文。其余已认可内容沿用前轮固定证据，不重新审全部实现。

### 3.2 本轮实读位置与支持边界

| 点 | 固定一次源与实读位置 | 核对结果及支持边界 |
|---|---|---|
| S01 | Syft v1.54.1 [pkg/dpkg.go](https://github.com/anchore/syft/blob/v1.54.1/syft/pkg/dpkg.go#L59) L55–83；[debian/package.go](https://github.com/anchore/syft/blob/v1.54.1/syft/pkg/cataloger/debian/package.go#L163) L163–193；[parse_dpkg_info_files.go](https://github.com/anchore/syft/blob/v1.54.1/syft/pkg/cataloger/debian/parse_dpkg_info_files.go#L26) L26–53；[to_format_model.go](https://github.com/anchore/syft/blob/v1.54.1/syft/format/syftjson/to_format_model.go#L270) L270–283 | `Files`/`Path` 对应 JSON `files`/`path`；摘要可省略，配置文件标记在 L71–72。md5sums 解析明确使用 md5；包 Metadata 被带入输出。支持所选 dpkg 解析，不推定全部包类型都有成员或摘要 |
| S02 | 同 tag [model/file.go](https://github.com/anchore/syft/blob/v1.54.1/syft/format/syftjson/model/file.go#L13) L13–62；[to_format_model.go](https://github.com/anchore/syft/blob/v1.54.1/syft/format/syftjson/to_format_model.go#L88) L88–101、L136–160 | 文件输出含 coordinates 与 digests；输出逐 coordinates 组装并排序，不把 path 当唯一跨层身份。字段存在不保证现场每个条目都有摘要 |
| S03 | 同 tag [filecataloging/config.go](https://github.com/anchore/syft/blob/v1.54.1/syft/cataloging/filecataloging/config.go#L16) L16–39；[options/file.go](https://github.com/anchore/syft/blob/v1.54.1/cmd/syft/internal/options/file.go#L34) L14–47、L54–72；[selection.go](https://github.com/anchore/syft/blob/v1.54.1/syft/file/selection.go#L3) L3–10 | selection 三值与默认 owned-by-package、CLI 默认 sha1/sha256 属实，md5 可配置（L72）；库层默认 sha256 与 CLI 不同。正文限定 CLI，没有混作同一个默认值 |
| S04 | 同 tag [coordinates.go](https://github.com/anchore/syft/blob/v1.54.1/syft/file/coordinates.go#L10) L10–34；[location.go](https://github.com/anchore/syft/blob/v1.54.1/syft/file/location.go#L137) L137–152；[scope.go](https://github.com/anchore/syft/blob/v1.54.1/syft/source/scope.go#L8) L8–24；[container_image_all_layers.go](https://github.com/anchore/syft/blob/v1.54.1/syft/internal/fileresolver/container_image_all_layers.go#L86) L24–41、L56–125、L175–192 | layerID 来自文件引用所属层，all-layers 可包含不可见内容；路径查询可返回多个层位置。支持候选必须归层且包证据层不能代替成员层；不自动证明最终可见性 |
| S05 | OCI image-spec v1.1.1 [manifest.md](https://github.com/opencontainers/image-spec/blob/v1.1.1/manifest.md#L62) L62–73；[config.md](https://github.com/opencontainers/image-spec/blob/v1.1.1/config.md#L210) L210–222；[layer.md](https://github.com/opencontainers/image-spec/blob/v1.1.1/layer.md#L229) L229–252、L276–301 | manifest 层序、diff_ids 顺序与普通覆盖/whiteout 分开。结合 S02/S04，在正文排除的删除/whiteout 情形之外支持按层序分列当前候选与历史候选；这是依据规范作的方法判断，不是 Syft 已产出该关联结果或本库实扫 |
| S06 | [proc_pid_mountinfo(5), man-pages 6.19](https://man7.org/linux/man-pages/man5/proc_pid_mountinfo.5.html)，DESCRIPTION 字段 (1)–(5)，尤其 (2) 堆叠说明及其后括注、(3)/(4)/(5) | 同位置 top-most 的判据有“祖先挂载未被隐藏”的可达前提；field 3 是文件系统 st_dev，field 4 是该挂载在文件系统内的根，field 5 是相对目标进程根的挂载点。支持 §4 中 root 基址与遮蔽的反例推演，不要求实际采集或创建挂载 |

关键原文件 SHA-256：`dpkg.go=7dedd2aa40fe2543af419e6819f5becb382d23f4cd362b0eb5314b192e9d893a`、`model/file.go=e762e9a61f32bc1e179cd29c2c0385f2d0f8de00f1a793cac5d3262dbeab16c7`、`filecataloging/config.go=d24512303604919e5b9f479dd48f4c4ba04030386230d48a34672952a438f673`、`options/file.go=daec15315d9208ae588ebadfcec33b10c2e38e087a5e0e16dbb2fb3f332e2376`、`selection.go=3493c1dac9068b1e9d412b6066595fbd705668154b2d0547abba32908f7d2a17`、`coordinates.go=0fab7831d3327b62348b6c637367d5e3f80c4801da35acbf345491066b3c3034`、`location.go=760ea48a6d246827250f5c1d49a97940de49ff9d566e5d89f991fc85d74cf1a1`、man7 HTML=`27a0e5ad5cf9fc4ef4059cd0c4a9b70fa2ac23457a4d39b82f2381a654b3813f`。其余在仓库外请求清单；本机摘要不是上游签名证明。

## 4. 逐项复核与剩余关闭条件

### B21-C32 — P2 / CLOSED

**权威条件：** 第 26 次 L91；第 30 次 §4 C32-1/3 为本轮剩余。**位置：** 正文 L33、L62、L74、L117–131、L146、L150、L167；作者来源记录 L17；登记 L5319。

1. **C32-1 / CLOSED（所选、明示排除 whiteout 的记录设计范围）。** L74 已以 `artifacts[].metadata.files[].path` 解析所选 syft-json，明确 Go `Files`/`Path` 与小写 JSON 键的对应，S01 实核支持。包段的 `metadata.Files` 作为 Go 实现描述仍可保留，不再被用作 JSON 查询路径；locations 与成员文件仍分离。成员记录的 digest/isConfigFile 与可省略摘要边界也由 S01 核到，不因没有每种包类型清单而阻断。
2. **C32-1 跨层子条件 / CLOSED。** L74 现在交付同 P 候选、同层冲突转无法确定、manifest 层序选择最上层候选、历史候选分列、layerID 与内容摘要分工、dpkg md5 与文件摘要的同算法比对、摘要不一致不认作该包版本文件，以及证据不全 K2。S02–S05 支持此范围的文件身份/层序/普通覆盖依据。没有再以任一同 path layerID 或 dpkg 数据库所在层直接充当成员来源，也没有把 md5 与默认 sha256 跨算法相比。此关闭不把摘要相同提升为安全认证或全量包归属证明。
3. **whiteout 不新增实现义务。** L74、summary L33、待确认 L167、作者 L17 已明确上层删除/whiteout 检测未选定为 K1，并将该情形排除出已交付归属规则。因而“最上层候选”不能被读成已排除删除/whiteout 的现场可见性证明；需要该判断而无方法时仍须无法确定。这个诚实限缩满足第 30 次允许的未覆盖情形分列，不因未交付 whiteout 实现继续阻断，不由审阅者替作者补实现。
4. **C32-2 / CLOSED，沿用。** 单卡 uuid 的 M-ID 不重审、不再索取现场值、多卡排序、index/NPU 方法或宿主节点独立复核。
5. **C32-3 / CLOSED。** summary、L74 缺项、L167 与作者 unknown 清单均同步 whiteout K1；公共 K1/K2/K3 定义和 L146/L150 的比较引用继续保留。不存在把本轮该明示未选方法改称仅缺采样的残留。未生成/比对 SBOM 仍是 K3，不据此阻断设计关闭。

**剩余关闭条件：无（本轮既定范围）。** 保留无成员清单包类型、whiteout 等明确 K1，以及现场 K2/执行 K3，不宣称扫描覆盖全部 cataloger、实际库可见性或硬件验证已完成。

### B21-C33 — P2 / OPEN

**权威条件：** 第 26 次 L106；第 30 次 §4 C33-2/3。**位置：** 正文 L107 的“有效父挂载”“坐标换算”“逐库目标全路径”及“四分”口径，L167；作者来源记录 L12、L17。

1. **C33-1 / CLOSED，沿用。** 不重开逐对象表、UB 分道、worker 七键/算法、manager/vdevice 条件或错误返回/警告继续；CLI 返回与可读性仅作旁证的修订仍正确，不再索取完整 CLI、产品变体或现场节点。
2. **C33-2a / 部分满足，仍 OPEN。** 父目录一次 bind、父挂载覆盖普通子库而不要求逐库独立条目、子库相对路径及两侧存在性证据都已补入；同位置通过父子 ID 取 top-most 也符合 S06。**但“最长路径前缀＋同位置 top-most”仍未排除被隐藏祖先下面的旧子挂载。** S06 的 field 2 紧接着明确：该 top-most 还须其最长祖先挂载未被堆叠挂载隐藏才可访问。正文只是说更长前缀“以更长条目为准”，没有先验证该候选沿挂载父子链可达，因此不能把原始 mountinfo 中字面更长的旧子挂载直接当有效覆盖。这正是第 30 次要求的遮蔽处理，不是新索取全部挂载情形。
   - **方法反例推演，非现场输出：** 目录挂载 A 下已有子挂载 B；新挂载 A2 堆叠在 A 的同位置，隐藏 A 及其原子树。原始记录中 B 的路径可以仍比 A2 更长，但 B 不因“更长＋其自身无同位置上层”变成目标进程实际可达挂载。应先排除被隐藏祖先下的候选，或明确限缩为已排除这类遮蔽的所选范围，其他情形 K1。
   - 逐库目标还须保留同一参照系：先由原定目标目录 D 与子库相对路径 r 得到完整目标 `D/r`，再选覆盖它的可达挂载。若“以更长条目为准”后仍套用“有效父挂载点＋原子库相对父目录路径”，会重复或漏掉路径段；例如 r 为 `plugins/libx.so`、更具体挂载点为 `D/plugins`，不能再拼成 `D/plugins/plugins/libx.so`。这是同一父挂载→逐库目标连接的未闭合部分，不要求新增目标或现场采样。
3. **C33-2b / OPEN，root 换算与 S06 冲突。** L107 定义 `R＝P_src 相对 M_host 的子路径`，然后要求容器 field 4＝R，**漏掉 M_host 自己的 field 4（源文件系统内部根）**。最长前缀的宿主挂载点不是必然从文件系统 `/` 起始；宿主该条目也可能是一个子树挂载。按 S06 的 field 4/5 语义，所选源目录的文件系统坐标应由 `join(M_host.root, relative(P_src, M_host.mount_point))` 得到（规范化为绝对路径）；field 3 比较继续保留。该公式是字段语义的路径换算推论，不声称手册逐字给出公式。
   - **方法反例推演，非宿主实际状态：** 宿主 mountinfo 条目 field 3=`8:1`、field 4=`/drivers`、field 5=`/usr/local/Ascend/driver`；所选 P_src=`/usr/local/Ascend/driver/lib64`。将该源目录 bind 到容器时应匹配的 root 是 `/drivers/lib64`，不是仅相对挂载点得到的 `lib64`（即使补前导 `/`，`/lib64` 仍错误）。旧公式会拒绝正确关联，或与其他同 st_dev 子树错误相配。**这不是缺少现场 root 值，而是尚未正确使用已有字段语义。** 如只选 M_host.root=`/` 的受限方法，也须明确这个前置条件与未覆盖情形的 K1，不能无条件宣称完成通用换算。
4. **C33-3 / OPEN，仅限随上述方法缺口同步。** L107 与作者 L12 已同步改称“目录父挂载/遮蔽处理与 root 坐标换算判据”，但仍将整个 M-LIB 归为“方法已交付，只缺 filled 值”；正文 L167、作者 L17 亦仅列逐库/实际挂载 K2。以上未完成的可达遮蔽和坐标规则不能用“遮蔽未判明（K2）”一并覆盖。实际证据未采 K2、操作未执行 K3、未读变体 K1 的既有分列继续认可，不要求全部改为 K1。

**精确剩余关闭条件：** 保留已交付的普通父目录覆盖、同位置堆叠方向、逐库字段与 CLI 旁证边界；修正所选宿主源→文件系统内部 root 的换算，纳入宿主条目 field 4（或明确只覆盖 root=`/` 的受限前置）；对完整目标 `D/r` 选择实际可达的覆盖挂载，处理隐藏祖先/更具体遮蔽，并在换算时保持相对路径基准一致。允许如实限缩未覆盖情形并列 K1，不要求实现全部挂载情形。随后同步正文 L107/L167 与作者 L12/L17：未完成方法或超出受限规则为 K1，已有规则下确实缺现场记录为 K2，未执行为 K3；证据不足不得判来源关联成立。**不要求现场 mountinfo/st_dev、挂载实测、新权限、全部产品白名单或完整 CLI 审计，不重开 C33-1。**

### B21-C34 — P1 / CLOSED

**权威条件：** 第 26 次 L121；第 30 次 §4 C34-3。**位置：** 正文 L146、L150 及各变体的公共引用。

1. **C34-1 / CLOSED，沿用。** 两端消费配置、原生 runc/Toolkit 不参与与包装器 legacy 区分、旁路排除不重审，不再索取 handler 或安装路径现场值。
2. **C34-2 / CLOSED，沿用。** resize 接口/字段/单位/旧新记录与门控/完成观察不重审；S1/R1 的阶段×对象、完整节点/稳定身份、正负访问/恢复结果或未执行原因、证据定位继续保留，不要求各变体机械重复。
3. **C34-3 / CLOSED。** L146、L150 已有共同方法/缺项分类连接，本轮 C32-1/3 在其明示范围内闭合，C32-2 沿用，因此第 30 次留下的唯一依赖解除。C33 的 M-LIB 问题按原分工只归 C33，**不拿它继续阻断 C34，也不另计发现**。whiteout/多卡/NPU 等未选范围仍按原 K1 处理，不据此宣称全部变体可执行或已通过实测。

**剩余关闭条件：无（本轮既定范围）。** 保留 NPU 独立 unknown、负向单独授权以及更新/回退/重建拆分；没有负向授权不执行。

## 5. Acceptance 与最终计数

| T05-01 acceptance | 本轮判定 | 原发现对应 |
|---|---|---|
| L5403：镜像 digest、基础系统/依赖层、构建输入、SBOM/签名、拉取策略的作用与限制 | 沿用既有完整通过，不重审；本轮成员解析归 C32，不重开 C30 | C30 CLOSED，范围外 |
| L5404：固定运行时/NVIDIA 版本，分开驱动、库、设备/环境/挂载、权限与框架映射 | 本轮范围内完整通过：成员 JSON 键、跨层候选/摘要关联与分类闭合；单卡 M-ID 沿用，未覆盖范围仍明确 K1 | C31 CLOSED，范围外；C32 CLOSED |
| L5405：Ascend 固定实现/目标组合独立取证，GPU/NPU 与 digest 兼容边界 | 部分满足，未完整通过：父挂载/root 方法仍有上述缺口及完成度口径残留 | C33 OPEN |
| L5406：最小清单、异常/隔离、对照与源案例，非已验证处方 | 本轮范围内完整通过：既有配置/resize/S1/R1 保留，唯一 C32 方法依赖解除；不宣称实测 | C34 CLOSED |

四条 acceptance：**3 完整通过（其中 1 条沿用既有通过）/ 1 未完整通过**。本轮三项原发现合计 **2 CLOSED / 1 OPEN；关闭 1 P1、1 P2，开放 0 P1、1 P2**。C30/C31 保持 CLOSED；按本任务五个原发现合计为 **4 CLOSED / 1 OPEN**，不新增发现 ID。**第三十一次定向复核不通过，不能宣称 T05-01 全部通过；唯一剩余原发现为 C33。** 阻断不是缺现场值、未实测、未生成 SBOM、未审全部 cataloger 或未实现 whiteout。

## 6. 结构校验与写入审计

- 仓库外审计目录：`/private/tmp/b21-t05-01-recheck31-f6se9J`。建立独立 `validation` 副本并保留既有 `build/`，排除 `.git`、虚拟环境、node_modules 与 Python/工具缓存；原仓库不运行会更新生成文件的构建。
- 写入前在副本用原仓库虚拟环境 Python、`PYTHONDONTWRITEBYTECODE=1` 执行 `make check build`，**均 PASS，96 content entries / 446 sources**，日志 `validation-before.log`。只验证结构与本地链接，不验证技术正确性、远程正文或硬件。
- 报告写入后同步到同一副本，执行 `make check build`，**均 PASS，96 content entries / 446 sources**，日志 `validation-after.log`；生成的 `build/catalog.json` / `build/catalog.md` 仅在副本更新。本节补记后再同步校验，最终日志为 `validation-final.log`，不在原仓库构建。
- 逐字节 SHA-256 审计覆盖写入前 **427 个既有文件**（排除上述 Git/环境/缓存目录）：无修改、无删除，包含原 `build/` 两个生成文件；§2 的 **12 个输入文件**全部未变，正文工作区字节与 HEAD 对应文件相同。HEAD 仍为 `dc27e7b8f5cf60ea21775dc2a206b72d0a5df6ca`，文件集合及 Git 状态仅新增本报告。`git diff --check` 与报告单独行尾空白检查均无报错；结果保存于 `audit-result.json`。
- 结束核验再次解析同一会话 JSONL，仍为一条 `turn_context`（UTC `2026-10-16T19:25:53.377Z`），模型/档位及协作设置均为 `gpt-6.1-sol / xhigh`；审阅者可见输出未检出执行回退标记。保存 `model-initial.json` / `model-final.json`；核验局限仍为 §1 的本地元数据，不扩张为服务端证明。
- 未运行 `make test`：未改 `src/kb/` 或测试代码。不安装/执行上游组件，不提交、不建分支，不将本报告冒充正文修订或硬件验证。

**最终技术结论：B21-C32 CLOSED、B21-C33 OPEN、B21-C34 CLOSED；2/3 关闭。后续仅复核 C33 的上述精确剩余条件，不重开既有 CLOSED 项。**
