# Batch 21 补交 T05-01 第二十次定向复核

## 1. 结论、角色与范围

- 日期：2026-10-14（Asia/Shanghai）。执行者：当前 Codex 会话，以独立审阅角色核对作者第二十轮修订，与作者修订角色分开；未派发其他模型或子代理。
- `gpt-6.1-sol / xhigh` **仅为用户约定**，不是已独立确认的执行元数据。本会话未取得可独立核验的实际模型、推理档位或路由信息，不宣称模型一致性或无 fallback 已获独立确认。
- 唯一范围为 **B21-C32–C34**；权威关闭条件为[第十九次复核](batch-21-t05-01-codex-recheck-19.md) L87、L107、L122。[初审报告](batch-21-t05-01-codex-review.md)用于原 ID、优先级与职责核对。**C30/C31 保持此前 CLOSED、范围外，不重审。**
- **0 CLOSED / 3 OPEN（1 P1、2 P2）；第二十次定向复核不通过。** 白名单源文件、产品选择及 CLI 通用源/目标规则的补充可认可；“固定树未见”全树结论已纠正。但所选条件与必要库记录未完整交付，来源记录仍有旧口径，C32 方法和 C34 对照设计仍缺。
- 本轮问题均按原 ID 记录，**不新增发现 ID**。C33 的默认 mount group 与安装列表选择不能混同，以及口径未同步，均属于前次未关闭条件，不扩为安装流程或全部 CLI/DCMI 审计。
- 只新增本报告，不改作者正文、来源记录、修订映射、登记、计划或原仓库生成文件；保留开始时已有工作区改动。未提交或创建分支。
- 未安装组件、拉取/构建镜像、生成 SBOM、运行容器、接入集群、修改运行配置或执行访问/负向/恢复实测。只读上游脚本没有执行；知识库结构检查与目录构建不是容器或硬件验证。

| 原 ID | 原优先级 | 本轮状态 | 位置证据与主要剩余问题 |
|---|---|---|---|
| B21-C32 | P2 | OPEN | 正文 L60、L72、L78、L82–84、L109–112、L118、L131–138：扫描归层、逐 ordinal 稳定映射方法仍未交付；缺方法/缺采样未全量同步 |
| B21-C33 | P2 | OPEN | 正文 L90、L92；作者记录 L12、L17；登记 L5335、L5446、L5457、L5462：可读白名单链补充成立；所选产品/安装列表/节点许可环境与必要库记录仍缺，三分口径未全篇一致 |
| B21-C34 | P1 | OPEN | 正文 L127、L131–138：完整两端配置对、资源更新接口/字段、受控访问与负向边界恢复的生命周期关联仍缺；C32 依赖未闭合 |

## 2. 输入身份与写入边界

用户提供的 **4 个 SHA-256 前缀全部吻合**。以下完整摘要由本轮独立计算；报告中的仓库行号对应这些输入原文件，不是网页阅读器坐标。

| 输入 | SHA-256 |
|---|---|
| [正文](../../knowledge/05-cluster-platform/container-image-runtime-baseline.md) | `1cfe7221f907283634e96cc279702c657dfc0d8adb9500446b29d52b02b1f13a` |
| [作者来源记录](batch-21-t05-01-sources.md) | `c8b96e1a0848f3de00c42186a3e682ba4d8a4717b34a93a32f2d4e1df66a97db` |
| [修订映射](batch-21-review-fixes.md)，第二十轮节 L274–277 | `8ea6c2e09828ccfbd03657491570fbe5746b95c2d85fbefab1ccf8b1212f0fdd` |
| [第十九次复核](batch-21-t05-01-codex-recheck-19.md) | `ade54898a7bd7e4be0e64dd7679b6db2926d8e5e1e6b4a6d61b30a9a882ce62c` |
| [初审报告](batch-21-t05-01-codex-review.md) | `341775efc62d7b8d46659c2d272aa31ae301b0cd1db47623ebe86490b80e34b5` |
| [任务验收](../../plans/full-coverage-backlog.yaml)，T05-01 acceptance L5403–5406 | `5f9bcf865b8c77e13cc8ee5f1c03140c37b86f558d8227d8bb2080249f4fcfc3` |
| [来源登记](../../sources/registry.yaml) | `dfff04ab78e4c79afa466da75704a40cd840ed1b49a080676dcc1153e2502b3d` |

修订映射仅是作者落盘改动说明，不作为关闭证明。已从 `README.md`、`docs/authoring-guide.md` 开始核对仓库要求，并按 `content-outline.md` 核对 05.1 主归属/边界；相关目录未发现更深层 `AGENTS.md`。写入前对 Git 所列 tracked/untracked 非忽略路径及既有 build 文件做摘要快照、保存 Git 状态，并复制至 `/private/tmp/b21-t05-01-recheck20-NeTC95/validation`，供单文件写入审计与隔离构建使用。

## 3. 一次源抽查方法、文字与限制

### 3.1 curl 实际尝试与替代只读通道

对下表 **12 个**精确 HTTPS URL 实际执行只读 GET，命令形态为：

```sh
curl --location --fail --silent --show-error \
  --connect-timeout 8 --max-time 20 --output /dev/null \
  --write-out 'http_code=%{http_code}\n' "$url"
```

未使用 `-k`/`--insecure`，未更改默认 TLS 校验配置，未请求沙箱提权或自定 IP 绕行。**12 次均在 DNS 阶段失败，退出码 6、HTTP 000**，报 `Could not resolve host`（`github.com`、`docs.nvidia.com`、`docs.pytorch.org`）；没有取得 curl HTTP 正文，不能报告 curl 200、TLS 已校验成功或上游字节摘要，也不独立背书作者历史 curl 成功记录。

随后按用户允许的只读替代方式：用 **GitHub 连接器 `fetch_file`** 读取精确 ref/原文件区间，用 **网页读取通道**打开版本化文档并定位实际正文；不是仅判可达性，不以搜索片段或作者自述代替核对。GitHub 返回的 blob SHA 是上游文件身份，不是 curl 字节摘要；网页结果可能经解析或缓存，没有取得其独立 HTTP 字节快照。技术判定不以本次 curl DNS 失败作为阻断理由。

### 3.2 独立读取的关键一次源

下表 Ascend 文件均固定到 commit `44385c13d7b1d87def35f1604e8be4d16de6ca4e`。源码按原文件区间/函数定位；不把网页阅读器行号拼接为源码行号。

| curl 点 | 精确一次源 / 实际核对位置 | 核对文字及有限支持范围 |
|---|---|---|
| 01 | [build/scripts/base.list](https://github.com/Ascend/mind-cluster/blob/44385c13d7b1d87def35f1604e8be4d16de6ca4e/component/ascend-docker-runtime/build/scripts/base.list)，完整五行 | 列出 `/usr/local/Ascend/driver/lib64`、`/usr/local/Ascend/driver/include`、`/usr/local/dcmi`、`/usr/local/bin/npu-smi`、`/var/queue_schedule`；是路径候选，不是逐库名称/版本清单或挂载成功记录 |
| 02 | [build/scripts/run_main.sh](https://github.com/Ascend/mind-cluster/blob/44385c13d7b1d87def35f1604e8be4d16de6ca4e/component/ascend-docker-runtime/build/scripts/run_main.sh)，L1–75、L190–340、L400–655，重点 install/add_so/参数分支 | 五种安装产品选择不同源列表，另有未选产品变体时的默认源；它们都复制为配置目录中的 `base.list`，chmod 440；两种 A2 分支按 OS 追加库。故 group 名 `base` 不单独决定使用默认五项源列表 |
| 03 | [cli/src/u_mount.c](https://github.com/Ascend/mind-cluster/blob/44385c13d7b1d87def35f1604e8be4d16de6ca4e/component/ascend-docker-runtime/cli/src/u_mount.c)，完整文件，Mount/MountFile/MountDir/DoMounting | 目标宿主路径按 rootfs 与源路径拼接；bind 后以只读/nosuid remount；源不存在可跳过，校验/挂载也可失败。NODRV 的提前返回限定在该 CLI 的 DoMounting，不能据此宣布所有 runtime 挂载均不存在 |
| 04 | [build/build.sh](https://github.com/Ascend/mind-cluster/blob/44385c13d7b1d87def35f1604e8be4d16de6ca4e/component/ascend-docker-runtime/build/build.sh)，L105–文件末，copy_file_output | 将默认列表与五份产品变体复制入 run_pkg，再形成安装包；正面支持源码→打包→安装选择，不执行任何脚本 |
| 05 | [hook/process/process.go](https://github.com/Ascend/mind-cluster/blob/44385c13d7b1d87def35f1604e8be4d16de6ca4e/component/ascend-docker-runtime/hook/process/process.go)，L85–410 | 默认 mount group 为 base；每份列表先计扫描行，再做路径/stat/文件目录分类；构造 mount-file/mount-dir、PID/rootfs、allow-link 与条件 options 参数，并调用 CLI。读取列表不等于实际存在或挂载成功 |
| 06 | [runtime/process/process.go](https://github.com/Ascend/mind-cluster/blob/44385c13d7b1d87def35f1604e8be4d16de6ca4e/component/ascend-docker-runtime/runtime/process/process.go)，L243–405、L455–812 | LD_LIBRARY_PATH 处理与挂载配置分开；addHook 在非 VIRTUAL 时仍调用 CreateVDevice；有效 ID 更新设备集合/options 和 poststop；manager/产品/UB、节点与 rwm 均有独立条件 |
| 07 | [device-plugin common.go](https://github.com/Ascend/mind-cluster/blob/44385c13d7b1d87def35f1604e8be4d16de6ca4e/component/ascend-device-plugin/pkg/common/common.go)，L90–136 | 输出 ID 串/options；310B 条件写 allow-link，非 PresetVDevice 条件写 worker 环境组。来源支持这些条件，不替作者选择所选样板的条件值 |
| 08 | [syft README@v1.54.1](https://github.com/anchore/syft/blob/v1.54.1/README.md)，Features/The basics | 支持镜像/文件系统等扫描对象及 SBOM 格式入口；本段不交付正文所需的固定扫描范围、必需输出字段及逐库来源层解析规则。不重开 C30 |
| 09 | [PyTorch CUDA notes 2.14](https://docs.pytorch.org/docs/2.14/notes/cuda.html)，Device-agnostic code 的 CUDA_VISIBLE_DEVICES 段 | 说明管理 PyTorch 可用 GPU 范围；该段不是正文的逐 ordinal→Allocate/CDI/完整节点→稳定物理身份连接规则；不据此断言其他身份接口不存在 |
| 10 | [NVIDIA server.go@v0.20.1](https://github.com/NVIDIA/k8s-device-plugin/blob/v0.20.1/internal/plugin/server.go)，L280–438 | AnyCDIEnabled 与 AllCDIEnabled 分别判断；非全 CDI 组合下还可按条件输出 env/volume/DeviceSpecs；CDI CRI 路径填 CdiDevices。证明须固定完整策略集合，不只写“含 cdi-cri” |
| 11 | [Toolkit 1.20.0 CDI support](https://docs.nvidia.com/datacenter/cloud-native/container-toolkit/1.20.0/cdi-support.html)，Running a Workload/Non-CDI-Enabled Runtimes/Setting the CDI Mode Explicitly | 区分独立 NVIDIA Runtime Hook 与 CDI 消费；显式 CDI 模式仍可使用选择环境变量，不能仅凭变量存在推定 legacy |
| 12 | [Toolkit 1.20.0 troubleshooting](https://docs.nvidia.com/datacenter/cloud-native/container-toolkit/1.20.0/troubleshooting.html)，NVML/Containers losing access/Affected Environments/Mitigations | 权限拒绝与 hook/legacy 更新后访问丢失分别限定；CPU/内存更新和重建/CDI 的来源场景可核对，但该页不替本文选定更新接口/字段或提供实际恢复结果 |

另以连接器补读同提交 [CLI main.c L220–495](https://github.com/Ascend/mind-cluster/blob/44385c13d7b1d87def35f1604e8be4d16de6ca4e/component/ascend-docker-runtime/cli/src/main.c#L220)（参数→ParsedConfig→目标 PID 的 mount namespace→DoMounting）、[plugin.go L1087–1172](https://github.com/Ascend/mind-cluster/blob/44385c13d7b1d87def35f1604e8be4d16de6ca4e/component/ascend-device-plugin/pkg/server/plugin.go#L1087)（两条互斥输出路径与 rw）及 [api/default_name.go L145–182](https://github.com/Ascend/mind-cluster/blob/44385c13d7b1d87def35f1604e8be4d16de6ca4e/component/ascend-common/api/default_name.go#L145)（四个环境键与配置目录）。这些是独立文字补读，不计作新增 curl 成功记录；没有读取五份产品变体全文，不声称完成全部列表或 DCMI 审计。

关键 blob SHA：base.list `4ea1b223fdeed19fed7fdf1a3b4457b8ddd747b3`；run_main.sh `9be36636ff13c480c57342b81c78f4b74e95675b`；u_mount.c `d85fd8155a1805edaf509b047c6441bcdc603e12`；build.sh `34322058d3784446ce7475bdf7853588c0bb265b`；hook `816212afa5f69b8edfb1554d3935af2ebcd28f06`；runtime `acbd7a1ec0703498abfcfcb6ce1aa493069091b1`；common.go `6cd038e9f1d67a8a913aa4bb1301692f177b3dbe`；NVIDIA server.go `9281b48ef52f9eda9cbed6d98491729da85b5a75`。以上为连接器返回身份，不是现场证据。只在报告链接/原创归纳，不改来源登记或复制外部全文。

## 4. 逐项定向判定

### B21-C32 — P2 / OPEN

**权威条件：** 第十九次复核 L87。**位置证据：** 正文 L60、L72、L78、L82–84、L109–112、L118、L131–138；第二十轮映射 L277 仅列分类同步。

**认可/保留：** 宿主内核驱动、注入用户态组件与镜像库分层，Allocate/CDI/edits/最终 OCI 连接，节点与访问许可/LSM 分离继续认可。L112 已区分缺方法/缺采样，L118 已将缺规则优先判无法确定；不重开 C30/C31。

**仍未满足：**

1. **扫描归层与逐库连接方法未交付。** L60/L72 仍写“所选扫描配置”“字段以实际输出为准”“缺项逐项记 unknown”，没有固定扫描范围/必需字段、成分或路径到镜像来源层的解析规则，以及逐库身份与宿主来源→最终挂载→容器目标各段连接键。列层清单、diff_ids 或通用箭头不能替代该方法；抽查 08 只核到 README 能力入口。缺的是方法设计与依据，不是实际 SBOM 输出。
2. **完整稳定映射方法明确仍缺。** L78 仍写“稳定物理标识映射方法（未交付，unknown）”；L82–84 是待填表，尚无来源支持的逐 ordinal 可见集快照→分配 ID/CDI 名或传递字段→完整节点（类型、major/minor、路径/来源）→稳定身份连接规则。抽查 09 的可见集管理说明不补齐该规则；不要求靠数量或编号猜映射。
3. **分类仅局部交付。** L109 仍“未记录即缺失”，L110“无法确定写 unknown”，L111“同上”；没有统一关联到方法缺失/采样缺失的原因、具体缺项与记录格式。L118 的缺规则门槛可认可，但 L131–138 三单对照仍未引用已交付的物理对应规则。不能用“诚实写 unknown”代替方法交付。

**剩余关闭条件：** 按固定来源交付所选扫描范围、必要字段、逐库归层及宿主来源→最终挂载→容器目标连接规则；交付逐 ordinal 的完整稳定映射方法。将缺方法/缺采样的原因、缺项与记录格式同步到核对表、清单及 C34 比较/判定。**现场值可 unknown；不要求拉取镜像、生成 SBOM、审计全部 cataloger、采集设备或实测；不重开 C30。**

### B21-C33 — P2 / OPEN

**权威条件：** 第十九次复核 L107。**位置证据：** 正文 L31、L42、L90、L92、L147；作者记录 L12、L17；第二十轮映射 L276；登记 L5335、L5446、L5457、L5462。

**本轮已确认的补充，不再笼统列为未读：**

- 正文 L90/L147 与新增登记 L5452–5462 已纠正“固定 commit 树内未见”全树结论，补默认五项源列表、五个产品变体名称及安装选择；抽查 01/02/04 独立确认。五份变体内容未读的限定可保留，不要求一律读取全部变体。
- L90 已交付 CLI 通用源/目标拼接和 bind/remount 规则；抽查 03/05 与 main.c 补读支持这一有限链。**不能再把 CLI 源/目标通用规则整体写成未交付**；但也不从源码路径候选推出文件存在、每个库已知或挂载成功。
- 空 options 只排除 VIRTUAL 提前返回、有效 VdeviceID 仍可改写并加 poststop、插件与 hook 的 allow-link 作用域、四键定义、每列表 128 扫描行及条件 CLI 参数继续保留。抽查 05–07 与 default_name.go 补读支持相关事实；未重开已确认定义链。

**仍未满足及原 ID 内追记：**

1. **所选完整条件/节点/许可/环境表仍缺。** L90 仍仅固定 UseAscendDocker=true、空输入 options、默认 mount group；没有选择具体芯片/产品、输入 ID 的设计形式、PresetVDevice、安装列表选择、manager/UB 存在或缺失条件，形成对应节点、完整许可与环境字段表。L92 仍是目标组合字段清单及支持交集 unknown。抽查 06 的产品分支、dvpp_cmdlist 尝试及 UB 条件、抽查 07 的 worker 环境条件不能被泛列摘要替代；虚拟/poststop 分叉须按所选条件保留或有依据限定。无需实际 DCMI 返回值。
2. **默认 mount group 不等于默认源列表选择。** L90 的“所选组：默认 base（5 项如上）”没有同时固定安装类型/默认安装分支。抽查 02 显示全部产品选择最终都写同名 base.list；因此已知 group 为 base 仍不足以确定文件来自默认五项源还是某产品变体/追加库。应明确设计选择默认安装分支或一份必要变体并链接打包/安装选择，不以现场未采为由省略设计选择。此为前次同一关闭条件的剩余项，不新增 ID。
3. **必要库所选记录仍缺。** 默认候选列表与通用 CLI 规则现在可认可，但 L90 没有给所选条件下必要库的宿主绝对来源/候选库身份、CLI 入选与消费条件、rootfs 宿主目标及容器内目标的对应记录。源列表中的目录不等于每个库名/版本已知，也不全是库。应将必要目录/库候选明确选入记录、区分规则已知与待采文件身份/版本/结果；不要求本轮取得实际库版本或全目录审计。
4. **“口径全篇同步”尚未成立。** 作者记录 L12 仍写“未读：所选列表内容/CLI 源目标”，L17 仍将实际库挂载/白名单/hook 可执行/DCMI 合列 unknown，没有与本轮已读通用规则相区分。正文 L90 内也仍有“实际库挂载来源/目标/白名单未取”“runtime 库注入语义未核对”的宽口径，与同一段新增链并存；登记 L5335 仍“runtime 库注入/白名单未取”。登记 L5446 的四子目录未见不是全树断言，**不再把它判为全树检索事实错误**，但应明确链接 build/scripts 的正面来源，并区分源码列表/安装后文件。新增 L5457/L5462 不能自动改写这些旧表述。L31/L42/L147 的收窄可认可，不能代表全部位置已一致。

**剩余关闭条件：** 固定所选芯片/产品、输入 ID/options、PresetVDevice、安装列表选择/mount group、manager/UB 等设计条件，交付完整节点/许可/环境对应表及条件化虚拟/poststop。依据已读源码链选择必要列表和必要库，连接源码→打包/安装选择→hook 候选→CLI 消费→容器目标，补所选记录而非只列通用箭头。精确同步正文/作者记录/登记，分开**机制与通用规则已读、所选内容/记录未交付、现场结果未采/未执行**；保留本轮已认可修正。**现场文件/设备号/库版本/挂载结果可待采，支持交集可 unknown；不要求安装、运行脚本、实测、完整 DCMI/全部白名单或 CLI 审计。**

### B21-C34 — P1 / OPEN

**权威条件：** 第十九次复核 L122。**位置证据：** 正文 L118–125、L127、L131–138、L140–142；第二十轮映射 L277 未列本项对照设计补交。

**认可/保留：** 策略可多选、CDI 自身 hooks 与独立 legacy 区分、完整有序许可比较字段、S1/R1、旧新主体/时间窗、回退与更新/重建拆分、副本数解释收窄、NPU 独立方法未知、源案例与未执行/授权边界继续认可。L127 的公共对象格式存在，不指称完全没有恢复记录对象，也不要求每行机械重复。

**仍未满足：**

1. **两端完整配置对未选定。** L132 基线仍为策略“含 cdi-cri”，变体仍为“envvar 或 volume-mounts”；未固定两端完整策略集合、runtime 模式/handler 消费组合和传递字段。抽查 10 的多策略输出与抽查 11 的 CDI 环境变量消费表明，仅靠混合路径判无法确定不是选定受控配置对。站点 handler 名和现场旧新值可待填，设计选型不能空缺。
2. **资源更新接口/完整字段仍缺。** L137 仍以 CRI 更新对象/OCI linux.resources.cpu 为候选，并明确“固定字段未取，unknown”；未选一个更新接口、完整字段、单位/语义及旧新记录格式，未绑定同一次更新生命周期前后采样。抽查 12 仅支持该类源场景；镜像/驱动回退与重建不能替代资源更新对照。
3. **成功访问、原负向边界恢复及逐变体关联不足。** L127 有 audit/AVC、进程/设备/时间三元组及恢复后摘要，但未选定受控成功访问操作/结果记录，以及单独授权负向拒绝的记录形式；没有把它们用统一连接键关联至各变体更新/重建前后和恢复后的主体、目标节点/稳定身份、时间窗与可定位结果。L133/L135–138 仍主要以拒绝事件、注入集或“同上”指代。未见拒绝、摘要或可见集恢复不证明访问成功或原负向边界恢复；公共格式可以复用，但须补具体生命周期连接规则。
4. **C32 方法依赖仍未闭合。** 三单比较依赖尚未交付的稳定映射，缺方法/缺采样分类仍未全量同步。此处引用 C32 同一缺口，不新增发现，也不代替前三项独立对照要求。

**剩余关闭条件：** 固定两端完整传递策略集合、runtime 模式/handler 消费组合、字段及旁路排除；保留 CDI hooks/独立 legacy 与许可比较边界。选定资源更新接口、完整字段、单位/语义及旧新记录格式。完善受控成功访问与原负向边界恢复的设计记录，按各变体更新/重建生命周期连接主体、目标节点/稳定身份、时间窗与可定位结果；可统一引用公共规则。引用 C32 已交付方法，缺方法时优先无法确定并区分缺采样。保留 NPU 独立对照未知、S1/R1、回退拆分及安全授权边界。**不要求执行试验、取得现场值、扩大生产权限或制造结果；无负向授权不执行。**

## 5. Acceptance 与最终计数

| T05-01 acceptance / 原文件位置 | 本轮判断 | 原 ID |
|---|---|---|
| 镜像身份、构建输入、SBOM/签名、拉取策略 / L5403 | 沿用此前完整通过；范围外，不重审供应链 | C30 CLOSED |
| 固定 runtime/Toolkit/CDI、各层与映射分离 / L5404 | 部分满足，未完整通过：逐库归层、稳定映射及分类同步仍缺 | C31 CLOSED（范围外）；C32 OPEN |
| Ascend 独立实现与目标组合 / L5405 | 部分满足，未完整通过：本轮白名单通用链认可，所选条件/必要库记录/三分口径仍缺 | C33 OPEN |
| 清单、异常/隔离、对照与源案例 / L5406 | 部分满足，未完整通过：完整配置对、更新字段、访问/恢复关联与映射依赖仍缺 | C34 OPEN |

四条 acceptance 汇总：**1 沿用既有完整通过 / 3 未完整通过**。本轮 **0 CLOSED / 3 OPEN（1 P1、2 P2）**，**第二十次定向复核不通过**，无新增发现 ID。阻断依据是未交付的方法、所选条件/记录、证据关联与口径一致性，**不是 curl DNS 失败、现场值 unknown、没有实测或未证明整栈兼容**。本报告不变更正文、计划或验收状态。

## 6. 结构校验与写入审计

- 写入前原仓库 `PYTHONDONTWRITEBYTECODE=1 make check` **PASS：96 content entries / 440 sources**，只验证结构与本地链接。
- 写入后原仓库 `PYTHONDONTWRITEBYTECODE=1 make check` **PASS：96 content entries / 440 sources**。
- 将本报告同步至 §2 临时副本，用原仓库虚拟环境 Python、禁写字节码执行 `make check` / `make build`，均 **PASS：96 content entries / 440 sources**。只在副本重新生成 `build/catalog.json` / `build/catalog.md`，不重写原仓库生成文件；本节补记后同步最终报告并复跑同样校验/构建。
- 摘要审计覆盖 **403 个**既有文件（Git 所列 tracked/untracked 非忽略路径及既有 build 文件）：既有摘要不变、无删除；唯一新增为本报告。去除本报告后的 Git 状态与写入前一致，七个输入保持 §2 摘要。报告只有 C32/C33/C34 三个原发现标题，优先级与 OPEN 状态吻合；行尾空白及 `git diff --check` 检查通过。
- 未修改 `src/kb/` 或测试，不需要 `make test`；技术状态仅按 §4 判定，结构/构建不替代技术或硬件验证。

**最终技术结论：B21-C32、B21-C33、B21-C34 均 OPEN；0 CLOSED / 3 OPEN，第二十次定向复核不通过。C30/C31 保持此前 CLOSED、范围外；白名单源列表、安装选择及 CLI 通用规则的补充已认可，不以审阅者补读替代作者所选样板交付；约定审阅配置不是已独立确认的执行元数据。**
