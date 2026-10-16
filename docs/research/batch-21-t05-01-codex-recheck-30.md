# Batch 21 补交 T05-01 第三十次定向复核

## 1. 结论、角色与范围

- 日期：2026-10-17（Asia/Shanghai）。执行者：当前本地 Codex CLI 会话，以独立审阅角色核对作者第三十轮修订，与正文作者角色分开；未派发子代理或其他模型。
- **模型核验：** 实读 `~/.codex/sessions/2026/10/17/rollout-2026-10-17T03-06-35-01a1461b-e32a-7120-a2cc-9bdc58215526.jsonl`，会话 ID 为 `01a1461b-e32a-7120-a2cc-9bdc58215526`。初次核验所见 `turn_context` 时间为 UTC `2026-10-16T19:06:41.974Z`（本地 2026-10-17 03:06:41），`model=gpt-6.1-sol`、`effort=xhigh`；`collaboration_mode.settings` 同样为 `gpt-6.1-sol / xhigh`。核验方法是逐条解析当前会话 JSONL 的执行上下文，并检查审阅者 `output_text` 的运行回退标记，不把提示词或引用中的标记示例当作执行回退。所见上下文为单一约定模型，审阅者已输出文本未检出 fallback 标记。`session_meta` 的 originator 为 `codex_exec`、model_provider 为 `custom`；这只核验本地执行元数据，不是独立服务端路由、实际推理计算量或供应商证明，不追改历史模型记录。摘录保存在仓库外审计目录。
- 唯一复核范围为 **B21-C32、B21-C33、B21-C34**；以[第二十六次复核](batch-21-t05-01-codex-recheck-26.md) L91、L106、L121 为权威关闭条件，以[第二十九次复核](batch-21-t05-01-codex-recheck-29.md) §4 为本轮前精确剩余范围。[初审](batch-21-t05-01-codex-review.md)仅继承 ID、优先级与职责边界。**C30/C31 已 CLOSED，不重审、不重开；C33-1、C34-1、C34-2、worker 生成算法、UB 分道、S1/R1 等已认可内容保留，不重复索取。** C32-1 等仅为既有发现的子项，不是新增发现 ID。
- **本轮 0 CLOSED / 3 OPEN（1 P1、2 P2）；第三十次定向复核不通过。** 包证据位置与成员文件的分离、文件编目默认值、单卡 uuid 范围的 M-ID、宿主内核/驱动行的分类修正均有实质交付；其中 **C32-2 可关闭**。仍缺所选 syft-json 的准确成员解析与 all-layers 文件归层判据，以及目录挂载覆盖逐库目标的完整 mountinfo 关联规则；相应完成度口径与 C34 的 C32 方法依赖尚不能关闭。
- 只新增本报告，不修改或删除其他仓库文件，不提交、不建分支。作者修订映射只是索引，不作关闭证据；未修改正文、来源记录、来源登记或计划状态。
- **未执行实测，不构成硬件验证。** 未拉取/构建镜像、生成 SBOM、安装或执行上游组件、运行容器、查询设备或接入集群；未进行访问、负向、更新、回退、恢复实测。剩余阻断仅为方法/记录设计、来源语义与口径问题，不是缺少现场值、未审全部 cataloger、未扩展多卡/index/NPU 或网络取证失败。

| 原发现 | 优先级 | 本轮状态 | 精确剩余范围 |
|---|---|---|---|
| B21-C32 | P2 | OPEN | 正文 L33、L62、L74：成员 JSON 键、同路径跨层候选的归属/缺项规则及完成度口径；L80 单卡 M-ID 本轮认可 |
| B21-C33 | P2 | OPEN | 正文 L107、L167；作者来源记录 L12、L17：实际目录挂载到逐库目标的关联方法及其 K1/K2 口径 |
| B21-C34 | P1 | OPEN | 正文 L146、L150 等：仅余 C32-1/3 方法与分类依赖，不另背 C33、不重开两端配置/resize/R1 |

优先级沿用初审：P1 是核心验收主干阻断，P2 是必须补齐的方法、证据或版本边界；不是生产漏洞或事故严重性评级。

## 2. 输入身份（SHA-256）

开始时 Git 工作区干净，HEAD 为作者提交 `02cc86886f71cb454531e260be149803016cc4de`。核对该提交的文件清单与正文差异，正文工作区字节与 HEAD 中对应文件一致。以下摘要按完整文件原始字节计算；行号均为本轮工作区物理行号。

| 输入 | 本轮 SHA-256 | 审阅定位 |
|---|---|---|
| [第二十九次复核](batch-21-t05-01-codex-recheck-29.md) | `1c557166c982ef2fcf09a5d75653846f3330cfeabf69237032da853bb5abfc7b` | §4 精确剩余条件及已认可子项 |
| [第二十六次复核](batch-21-t05-01-codex-recheck-26.md) | `ade616897c367afb566c3076ffc8b36f2dbf6c95af8558d74af8d537ed3402b0` | L91、L106、L121 权威条件 |
| [初审报告](batch-21-t05-01-codex-review.md) | `341775efc62d7b8d46659c2d272aa31ae301b0cd1db47623ebe86490b80e34b5` | C32/C33/C34 的 ID、优先级、分工 |
| [作者修订映射](batch-21-review-fixes.md) | `c272998e191593dafbe36fa1d5cc383106605f06e12a72a302da45e0e9c3b99a` | L413–420“第三十轮修订”，仅作索引 |
| [修订后正文](../../knowledge/05-cluster-platform/container-image-runtime-baseline.md) | `7f38663815dc65337de70cd43d3e880a15c2001ae5a7e5f0e03ae78bc1497035` | L33、L62、L74、L80–86、L107、L117–131、L146–167；仍为 `reference / draft / source_checked` |
| [作者来源记录](batch-21-t05-01-sources.md) | `8633d43abbaf65396d57a86b005f5249f89b3e124612e5a8f243ba1b5ce78118` | L12、L17、L38–45 第五轮增补 |
| [任务计划](../../plans/full-coverage-backlog.yaml) | `5f9bcf865b8c77e13cc8ee5f1c03140c37b86f558d8227d8bb2080249f4fcfc3` | T05-01 L5386–5430；acceptance L5403–5406 |
| [来源登记](../../sources/registry.yaml) | `a6471ec1c387a29f28b763278ea8f2a0f6ced3de5bcfcda2b4bdf4b9ca48e8cb` | mountinfo L333–343、resize L5292–5302、Syft L5314–5324 |

先读取 [README](../../README.md) 与[写作指南](../authoring-guide.md)，并核对[归属边界](../../content-outline.md)和[元数据 schema](../../schemas/content.schema.json)；摘要依次为 `21759d9b1fc122d94bb3c3990d1b2e621c53dabc7ba022852545cae7b2329b44`、`75ee28d1aca7a4ac1d56ae493856037770a14fcdac27fa9b662451cee169a801`、`ed9033d2f53fa504fc05e55b221697dd7a1d14c5adaf58f8cc0a6613f8fe7046`、`b60b8d9ccb8728f034607901124c4206f5dc705ca824e31ce0ab5615523d0147`。适用目录未发现额外嵌套 AGENTS 指令。当前来源登记为 **446 项**，不沿用前轮 445。

## 3. 一次源取证

### 3.1 实际通道、失败与限制

本轮以本机 `curl` 只读 HTTPS GET 获取固定 tag/commit 原文件和版本化文档，命令形态为 `curl --fail --show-error --silent --location --connect-timeout 10 --max-time 45 URL -o FILE`，开启默认 TLS 校验，没有 `-k`。带状态记录的 24 次请求中，**23 次 exit 0 / HTTP 200，1 次定位请求 exit 56 / HTTP 404**；成功原文件、文档与摘要保存在 `/private/tmp/b21-t05-01-recheck30-G3J0Xp/upstream/`，请求状态、字节数、SHA-256 和本机计算的 Git blob 形式 SHA-1 见 `downloads.json`。另有两次 curl 目录/递归树定位请求成功落盘，但未输出 HTTP 状态，不将其混入上述“200”计数；未执行取回的代码。

GitHub 只读连接器成功读取 Syft 同 tag 的 `syft/pkg` 目录，用于定位真正的 `dpkg.go`。Web `open/find` 另用于实读 man7 页、PyTorch 2.14 可见设备段及 Toolkit 1.20.0 GPU Enumeration，并辅助打开 NVIDIA 源码页；Web 的缓存/抽取行号不充当 GitHub 原文件锚点，源码行号由本机原文件生成。

**失败单列：** 初次试探 Syft `syft/pkg/dpkg_metadata.go` 返回上述 404；随后从同 tag 目录定位 `syft/pkg/dpkg.go`，curl 200 并实读。Web 打开 Syft `model/file.go` 返回 `Cache miss`，同文件 curl 已成功取得；Web 对 NVIDIA 页面查找 `deviceListEnvVar` 未返回匹配，改用已取得的同 tag 原文件核对 L46、L480–482。没有将这些定位/抽取失败解释为实现缺失，没有发生本轮 curl DNS 失败，也不借用历史失败记录作为本轮证据。不是只凭 HTTP 成功、搜索摘要或作者自述形成技术结论。

tag 按任务固定，额外原文件仍属于同一既有来源；不宣称完成 tag 签名或不可变性审计。man7 实读页尾自述 Linux man-pages **6.19**、手册日期 **2026-02-08**、HTML 生成 **2026-09-09**，并留本轮正文摘要；其 URL 本身不是不可变 URL。临时下载不是永久证据归档，不把外部全文搬入仓库，不扩展到全部 cataloger 或硬件验证。

### 3.2 本轮实读位置与支持边界

| 点 | 固定一次源与实读位置 | 核对结果及边界 |
|---|---|---|
| S01 | Syft v1.54.1 [debian/package.go](https://github.com/anchore/syft/blob/v1.54.1/syft/pkg/cataloger/debian/package.go#L163) L27–61、L163–193；[parse_dpkg_db.go](https://github.com/anchore/syft/blob/v1.54.1/syft/pkg/cataloger/debian/parse_dpkg_db.go#L36) L36–49；[parse_dpkg_info_files.go](https://github.com/anchore/syft/blob/v1.54.1/syft/pkg/cataloger/debian/parse_dpkg_info_files.go#L24) L24–53 | 包 Locations 保存数据库/辅助信息证据，成员记录另入 Metadata；md5 清单记录路径并补前导 `/`，不据此宣称它已经完成规范真实路径或逐层唯一归属解析。包证据与成员分离的修订正确 |
| S02 | 同 tag [pkg/dpkg.go](https://github.com/anchore/syft/blob/v1.54.1/syft/pkg/dpkg.go#L59) L59–83；[model/package.go](https://github.com/anchore/syft/blob/v1.54.1/syft/format/syftjson/model/package.go#L128) L128–135；[to_format_model.go](https://github.com/anchore/syft/blob/v1.54.1/syft/format/syftjson/to_format_model.go#L280) L270–283 | Go 成员是 `Files`/`Path`，JSON 标签实际为 `files`/`path`；所选 syft-json 包元数据保持该结构，不会变成大写 JSON 键。输出解析应区分 Go 字段名与 JSON 键 |
| S03 | 同 tag [model/file.go](https://github.com/anchore/syft/blob/v1.54.1/syft/format/syftjson/model/file.go#L13) L13–38、L40–62；[file/coordinates.go](https://github.com/anchore/syft/blob/v1.54.1/syft/file/coordinates.go#L10) L10–34；[file/location.go](https://github.com/anchore/syft/blob/v1.54.1/syft/file/location.go#L137) L137–152；[to_format_model.go](https://github.com/anchore/syft/blob/v1.54.1/syft/format/syftjson/to_format_model.go#L88) L88–101、L132–150 | `files[]` 的 location/digests、path/layerID 和文件 ID 可确认；编码按 coordinates 保留文件对象，排序亦保留层序。path 单独不是跨层文件身份键 |
| S04 | 同 tag [filecataloging/config.go](https://github.com/anchore/syft/blob/v1.54.1/syft/cataloging/filecataloging/config.go#L16) L16–39；[options/file.go](https://github.com/anchore/syft/blob/v1.54.1/cmd/syft/internal/options/file.go#L34) L14–47、L54–72；[selection.go](https://github.com/anchore/syft/blob/v1.54.1/syft/file/selection.go#L3) L3–10 | Selection 默认 owned-by-package，三取值属实；CLI 默认摘要 sha1+sha256 属实。库层 DefaultConfig 默认 hasher 为 sha256，与 CLI 默认须分开；正文已经限定 CLI，不据此提出问题 |
| S05 | 同 tag [source/scope.go](https://github.com/anchore/syft/blob/v1.54.1/syft/source/scope.go#L8) L8–24；[container_image_all_layers.go](https://github.com/anchore/syft/blob/v1.54.1/syft/internal/fileresolver/container_image_all_layers.go#L86) L86–125、L175–192 | all-layers 可含不可见旧层；按路径查询遍历各层并返回多个 location，另有相对给定层视图的查询语义。仅“同 path”不能自动选定某包版本对应的唯一文件/来源层 |
| S06 | NVIDIA 插件 v0.20.1 [server.go](https://github.com/NVIDIA/k8s-device-plugin/blob/v0.20.1/internal/plugin/server.go#L480) L46、L305–365、L375–408、L456–482 | UUID 策略、去重、qualified CDI 名/CRI 返回，以及 `NVIDIA_VISIBLE_DEVICES` 直写分配 ID 串均可确认；不由插件源码单独推出框架编号语义 |
| S07 | [Toolkit 1.20.0 GPU Enumeration](https://docs.nvidia.com/datacenter/cloud-native/container-toolkit/1.20.0/docker-specialized.html#gpu-enumeration)；[PyTorch CUDA notes 2.14](https://docs.pytorch.org/docs/2.14/notes/cuda.html#device-agnostic-code) Device-agnostic code / 可见设备段；[CDI SPEC@cb98bcf6](https://github.com/cncf-tags/container-device-interface/blob/cb98bcf66dc68530012483bd56e33e14d815e167/SPEC.md#L193) L193–249 | 分别支持 UUID 选择容器 GPU、框架可见范围/本地编号和 qualified 设备 edits。与 S06、既有最终节点记录共同支持严格单卡设计的唯一对应；不证明多卡排序或宿主独立复核 |
| S08 | [proc_pid_mountinfo(5), man-pages 6.19](https://man7.org/linux/man-pages/man5/proc_pid_mountinfo.5.html)，DESCRIPTION 字段 (1)–(11)，重点 (2)–(5)、(7)–(10) | field 3 为该文件系统的 st_dev，root 是文件系统内的挂载根，mount point 相对目标进程根；有覆盖/堆叠挂载与可变数量 optional fields。它记录挂载，不为目录内每个普通子文件各生成一条挂载记录；详见 §4 的方法推论 |
| S09 | Ascend 固定 commit `44385c13d7b1d87def35f1604e8be4d16de6ca4e` [u_mount.c](https://github.com/Ascend/mind-cluster/blob/44385c13d7b1d87def35f1604e8be4d16de6ca4e/component/ascend-docker-runtime/cli/src/u_mount.c#L57) L57–81、L84–160 | MountDir 对父目录执行一次 bind/remount，不逐子库挂载；MountFile 与目录路径分开，源 stat 失败返回 0 的旧反例仍成立。不重审已通过的 runtime 逐对象/UB 表 |

本轮关键原文件 SHA-256：`pkg/dpkg.go=7dedd2aa40fe2543af419e6819f5becb382d23f4cd362b0eb5314b192e9d893a`、`to_format_model.go=c863c9527259f11e3aa1242333a8fa8fee532dfb02cef3414074d4436d1e9a11`、`container_image_all_layers.go=2cb79ddaba9d3cd2ddcfb49f143b1e08db43cb819cf474fc6715f1ed7c6e0680`、NVIDIA `server.go=215f04ab2ee4cbfe8f57cbd65064930b852f0c9678b0314c4aa65f93c6c020d9`、Ascend `u_mount.c=3af78451fd2d9989e9e2b6798aa60abc5de094b39e387d0bcd97c99f4ebc8463`、man7 HTML `27a0e5ad5cf9fc4ef4059cd0c4a9b70fa2ac23457a4d39b82f2381a654b3813f`。其余在仓库外 manifest；不把本机摘要说成上游签名证明。

## 4. 逐项复核与剩余关闭条件

### B21-C32 — P2 / OPEN

**权威条件：** 第 26 次 L91；前轮精确条件：第 29 次 §4 C32-1/2/3。**位置：** 正文 L33、L62、L74、L80–86、L117–131、L146、L150。

1. **C32-1 / OPEN；包证据与成员文件分离、文件编目字段/默认值子条件认可。** L62 不再把 locations 当成员库路径；L74 将包段与成员文件段分开，给出 dpkg 例子并把无成员清单包类型列 K1。S01/S03/S04 支持这些改动，后续 layerID 接层表及宿主来源→挂载→目标的设计连接继续保留。剩余不是再索取这些内容，而是所选输出尚不能按给出的规则可靠解析/归层：
   - **输出键与 Go 字段混用。** L74 写 `metadata.Files[].Path`，但 S02 的 JSON 标签为 `metadata.files[].path`；Go 字段可以称 `Files`/`Path`，需要明确与所选 syft-json 键的对应，不能把大写成员表达式直接作为该输出解析路径。否则按本文规则找不到成员清单也可能被误报成 K1/K2，而非发现解析规则错误。这是原“必要字段/包文件解析”条件，不是要求新选工具。
   - **all-layers 的同 path 候选仍无归属判据。** L74 用 `files[]`“同 path 条目”的 layerID 直接定位来源层，却未规定同一路径在多个层出现时如何关联具体 artifact/包版本与成员文件、区分历史候选和实际所指文件。S03/S05 表明文件身份包含 path 与 layerID，查找路径可返回多层 location；这不是 path 唯一索引。**方法反例推演，非本库扫描结果：** 同一库路径先后在两层被替换时，两份 location 可以同 path、不同 layerID；包证据层亦不能直接当成员层。当前规则最多找出候选层，尚不能证明把哪份文件接到该包/最终库记录。增加 digest 字段但未规定如何用于关联，不自动消除该歧义。未要求覆盖全部 cataloger，也未要求拉镜像或生成 SBOM。
2. **C32-2 / CLOSED（严格单卡 uuid 所选记录设计）。** L80 已明确限定请求一个 `nvidia.com/gpu`、deviceIDStrategy=uuid，并分别交付 envvar 直写分配 UUID→容器 GPU 选择→单元素框架可见集→ordinal 0，及 qualified CDI 名→对应 device edits→最终 OCI 唯一作业设备节点→单设备框架 ordinal 0 的连接；公共/控制节点另列。S06 直接核实此前缺的 envvar 直写段；S07 与已认可的 CDI/最终节点链共同支持此范围内的唯一对应。这里认可的是沿同一记录链完成 UUID 选择、最终暴露与框架单设备核对后的关联，**不是由 Pod 请求数量为 1 自动推定实际成功，也不是由编号文字相同证明身份**。现场各段未采仍按 K2/未执行按 K3，不构成阻断。多卡排序、index 转 UUID、宿主节点↔UUID 独立复核和 NPU 已明确为未选/未取源范围，不再索取或把它们作为本子项阻断。
3. **C32-3 / OPEN，仅余与 C32-1 方法完成度一致的分类。** L123 已将 NPU 驱动/固件语义 K1 与节点记录未采 K2 分开，前轮该具体冲突关闭；L33 已限定单卡映射，亦不再以多卡/宿主复核 K1 反驳单卡交付。L74 对“包无成员清单”的 K1 与实际缺输出的 K2 分列有进展。但其同路径跨层关联规则尚缺，不能用 L33 的“包—成员文件—层连接规则已交付”或 L74 只列未采/缺字段的 K2 覆盖该设计缺段。须区分错误解析键、未选定归属判据和已有规则下确实缺输出；共同规则及 C34 比较应继承此范围。不是要求将所有未采一律改为 K1。

**精确剩余关闭条件：** 保留本轮认可的 locations/成员分离、文件编目与单卡 M-ID；明确 dpkg Go 成员与实际 syft-json `artifacts[].metadata.files[].path` 的对应，交付所选 all-layers 记录范围内 path→具体文件身份/来源层的归属或消歧规则，不能将同 path 的任一 layerID 当作该包/最终库的唯一来源。若有明确未覆盖的记录情形，应如实限缩适用范围并单列其 K1，不能将方法缺段统称缺采样；同步 L33/L74 及共同比较口径。**不要求实扫、补现场值、全部 cataloger、多卡/index/NPU、宿主独立复核或硬件实测；C32-2 本轮认可不再重复索取。**

### B21-C33 — P2 / OPEN

**权威条件：** 第 26 次 L106；前轮精确条件：第 29 次 §4 C33-2/3。**位置：** 正文 L107、L167；作者来源记录 L12、L17、L45。

1. **C33-1 / CLOSED，沿用第 29 次认可。** 逐对象表、UB 设备节点/配置挂载分道、worker 七键与生成算法、返回错误/警告继续、manager 重命名与 vdevice/poststop 条件均不重开。旧 CLI 返回＋目标可达成功判据已经删除，继续认可；不要求现场节点号、产品白名单全集或完整 DCMI/CLI 审计。
2. **C33-2 / OPEN；选用 mountinfo 的方向与字段语义认可，目录覆盖逐库目标的规则仍缺。** L107 已增加宿主源 st_dev、容器进程 mountinfo、目标子库的三方关联，S08 支持 field 3/4/5 与类型/源描述的基本语义，S09 支持需要实际挂载证据而非 CLI 返回/可读性的原边界。但新增规则尚不能覆盖其自己选定的默认目录挂载：
   - **挂载对象与逐库对象未接上。** M-LIB 适用于 lib64/include/dcmi/queue_schedule 目录内逐库，实际操作却是 MountDir 对父目录的一次 bind。mountinfo 的 mount point 是该挂载根，不会为目录中每个普通库文件生成一行。当前“目标路径条目（field 5＝挂载点）”及“缺条目→K2”没有说明如何选择覆盖目标子库的有效父挂载、保留子库相对路径并排除更具体/堆叠挂载遮蔽。**方法反例推演，非现场采样：** `/usr/local/Ascend/driver/lib64` 整体 bind 成功时，其普通子库可能没有独立 mountinfo 条目；按现规则不能把父挂载与该子库可靠连接，也不能将此缺口归为尚未采到那条子库记录。S08 的挂载树/覆盖说明与 S09 的 MountDir 调用共同支持此推论。
   - **源路径与 root 的坐标换算未定义。** field 4 是源文件系统内部的挂载根，不必等于宿主绝对路径或某个未定义的“相对位置”。L107 只列宿主路径、类型、st_dev 与元数据摘要，未给出所选宿主源如何取得所属挂载点/文件系统 root 并换算到容器 root 字段的记录规则；仅相同 st_dev 不会补出该路径关联。此处只需补所选源/父挂载/子库的可填写连接，不能让“root 与源路径相对位置一致”留为没有计算依据的判句。读者无需因此执行挂载。
3. **C33-3 / OPEN，实际未采/未执行的分列本身认可，仅余完成度同步。** L107、L167 与作者 L12/L17 已一致把实际挂载证据未采列 K2、CLI 执行/部署产物核对未做列 K3；机制已读/未读变体也未再合并。这些清理不重复索取。但三处仍将含 mountinfo 的 M-LIB 整体称为已交付、只缺 filled 值，未容纳上述父挂载→逐库目标及源 root 换算的方法缺段。它们仍属 K1，或待真正补齐后再改成仅缺采样；不能以增添字段名代替已完成判据。

**精确剩余关闭条件：** 在现有 M-LIB 中给出目录父挂载→目标子库的有效覆盖/相对路径关联及遮蔽处理规则，并给出所选宿主源路径到 mountinfo root 的可核对换算依据与证据定位；将源身份、同一目标容器/命名空间中的实际挂载和具体目标子库接成可填写记录，证据不足不判已关联。随后同步正文与作者清单的 K1/K2 完成度。**不要求现场 mountinfo/st_dev、新增执行权限、挂载实测、全部挂载情形/产品变体或完整 CLI 审计；不重开已认可逐对象表、UB、worker 和旧判据删除。**

### B21-C34 — P1 / OPEN

**权威条件：** 第 26 次 L121；前轮精确条件：第 29 次 §4 C34-3。**位置：** 正文 L146、L150 及各变体的共同引用。

1. **C34-1 / CLOSED，沿用。** 原生 runc/Toolkit 不参与与 NVIDIA 包装器 legacy 两端消费配置设计、旁路排除不重审；现场 handler/安装路径不再索取。
2. **C34-2 / CLOSED，沿用。** Pod resize 接口、CPU 字段/单位/旧新记录、门控/完成观察及与重建的区分均保留；没有要求实测或重写该设计。第 29 次及此前已认可的 S1/R1 公共阶段×对象、完整节点/稳定身份、正负访问与恢复结果/未执行原因、证据定位继续保留，不要求每个变体重复抄写。
3. **C34-3 / OPEN，仅因 C32-1/3 依赖未闭合。** L146、L150 引用 M-ID/K1/K2/K3 的连接动作已存在；本轮 C32-2 单卡映射获认可，不再把它列为缺方法。但基线与变体的共同记录仍依赖 §1/§2 尚不完整的成员文件/层归属及其分类，不能将该依赖说成只缺现场填值。C34 不新增独立问题，不另承担 C33 的挂载问题，也不要求再次补两端配置、resize 或 R1。

**精确剩余关闭条件：** 待 C32-1/3 在所选范围内闭合后，使本项基线与变体比较引用该已闭合、如实分类的方法。**无需重写已认可配置/resize/S1/R1；保留 NPU 独立 unknown、负向单独授权以及更新/回退/重建拆分，无负向授权不执行。**

## 5. Acceptance 与最终计数

| T05-01 acceptance | 本轮判定 | 原发现对应 |
|---|---|---|
| L5403：镜像 digest、基础系统/依赖层、构建输入、SBOM/签名、拉取策略的作用与限制 | 沿用既有完整通过，不重审；本轮逐库解析问题仍归 C32，不重开 C30 | C30 CLOSED，范围外 |
| L5404：固定运行时/NVIDIA 版本，分开驱动、库、设备/环境/挂载、权限与框架映射 | 部分满足，未完整通过：单卡 M-ID 新认可，成员文件/层解析及完成度分类仍缺 | C31 CLOSED，范围外；C32 OPEN |
| L5405：Ascend 固定实现/目标组合独立取证，GPU/NPU 与 digest 兼容边界 | 部分满足，未完整通过：mountinfo 字段引入认可，目录父挂载/源坐标到逐库目标的关联及口径仍缺 | C33 OPEN |
| L5406：最小清单、异常/隔离、对照与源案例，非已验证处方 | 部分满足，未完整通过：两端配置、resize、S1/R1 均保留，仅余 C32-1/3 方法依赖 | C34 OPEN |

四条 acceptance：**1 沿用既有完整通过 / 3 未完整通过**。本轮三项原发现合计 **0 CLOSED / 3 OPEN（1 P1、2 P2）**；不新增发现 ID，不重开 C30/C31。子条件关闭不等于所属原发现整体关闭，C34 的依赖不另计为新增发现。**第三十次定向复核不通过；阻断仅限上述方法/记录设计与完成度分类，不是现场值未采、未实测、未生成 SBOM、未审全部 cataloger 或上游定位失败。**

## 6. 结构校验与写入审计

- 仓库外审计目录：`/private/tmp/b21-t05-01-recheck30-G3J0Xp`。建立独立 `validation` 副本，复制既有 `build/`，排除 `.git`、虚拟环境、node_modules 与 Python/工具缓存；不在原仓库运行会更新生成文件的构建。
- 写入前在副本以原仓库虚拟环境 Python、`PYTHONDONTWRITEBYTECODE=1` 执行 `make check build`，**均 PASS，96 content entries / 446 sources**，日志 `validation-before.log`。这些检查只验证结构与本地链接，不验证技术正确性、远程正文或硬件。
- 报告写入后同步到同一副本，再执行 `make check build`，**均 PASS，96 content entries / 446 sources**，日志 `validation-after.log`；生成的 `build/catalog.json` / `build/catalog.md` 仅位于副本。本节补记完成后再同步校验，最终结果记录于 `validation-final.log`，不在原仓库运行构建。
- 逐字节摘要审计覆盖写入前 **426 个既有文件**（排除上述 Git/环境/缓存目录）：无修改、无删除，包括原 `build/` 两个生成文件；§2 的 **12 个输入文件**全部未变。HEAD 仍为 `02cc86886f71cb454531e260be149803016cc4de`，文件集合与 Git 状态仅新增本报告；`git diff --check` 与报告单独行尾空白检查均无报错。结果保存于仓库外 `audit-result.json`。
- 结束核验再次解析同一会话记录，所见仍为一条 `turn_context`（UTC `2026-10-16T19:06:41.974Z`），其 model/effort 与协作设置均为 `gpt-6.1-sol / xhigh`；审阅者 `output_text` 未检出 fallback 标记。保存 `model-initial.json` / `model-final.json`，核验局限仍为 §1 所述本地执行元数据，不扩张为服务端证明。
- 未运行 `make test`：未改 `src/kb/` 或测试代码。未安装/执行上游组件，不提交、不建分支，不将本报告冒充正文修订或硬件验证。

**最终技术结论：B21-C32 OPEN、B21-C33 OPEN、B21-C34 OPEN；0/3 关闭。C32-2 单卡所选方法本轮认可；其他既有认可项不重开，仅继续上述精确剩余条件。**
