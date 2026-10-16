# Batch 21 补交 T05-01 第二十一次定向复核

## 1. 结论、角色与范围

- 日期：2026-10-14（Asia/Shanghai）。执行者：当前 Codex 会话，以独立审阅角色核对作者第二十一轮落盘修订，与作者修订角色分开；未派发其他模型或子代理。
- `gpt-6.1-sol / xhigh` **仅为用户约定，不是已独立确认的执行元数据**。本会话没有可独立核验的实际模型、推理档位或路由证据，不宣称模型一致性或无 fallback 已获独立确认。
- 唯一复核范围：**B21-C32–C34**。剩余关闭条件以[第二十次复核](batch-21-t05-01-codex-recheck-20.md) L88、L107、L122 为准；[初审报告](batch-21-t05-01-codex-review.md)用于原 ID、职责及优先级核对。**C30/C31 保持此前 CLOSED、范围外，不重审。**
- **0 CLOSED / 3 OPEN（1 P1、2 P2）；第二十一次定向复核不通过。** 本轮认可 310B 芯片示例、默认安装分支、默认五项候选全选入记录及部分口径修正；不能据此关闭完整 Ascend 条件/输出记录、GPU 归层/稳定映射方法或对照设计。
- 本轮全部按原 ID 记录，**不新增发现 ID**；没有需要另设 ID 的范围外追记。修订映射是落盘改动说明，不是关闭证明。
- 只新增本报告，不修改作者正文/来源记录/修订映射/登记/计划或原仓库生成文件，保留开始时已有工作区改动；不提交、不创建分支。
- 未安装组件、拉取或构建镜像、生成 SBOM、运行容器、接入集群、修改运行配置或执行访问/负向/恢复实测；读取的上游脚本未执行。结构校验和目录构建不属于容器或硬件验证。

| 原 ID | 原优先级 | 本轮状态 | 位置证据与剩余问题 |
|---|---|---|---|
| B21-C32 | P2 | OPEN | 正文 L60、L72、L78、L82–84、L109–112、L114、L118、L131–138：扫描归层与逐 ordinal 稳定映射方法未交付，缺方法/缺采样分类未完整同步 |
| B21-C33 | P2 | OPEN | 正文 L90、L92；来源记录 L17；登记 L5335、L5446、L5457、L5462：新选择与五项候选认可；完整条件/节点/许可/环境及逐项库候选对应记录仍缺，正文/记录存在旧宽口径 |
| B21-C34 | P1 | OPEN | 正文 L127、L131–138：两端完整配置对、资源更新接口/字段、成功访问与原负向边界恢复的生命周期关联仍缺，C32 方法依赖未闭合 |

## 2. 输入身份与写入边界

用户给出的 **3 个 SHA-256 前缀全部吻合**。以下完整摘要由本轮独立计算；仓库位置均使用这些输入原文件行号，不是网页阅读器行号。

| 输入 | SHA-256 |
|---|---|
| [正文](../../knowledge/05-cluster-platform/container-image-runtime-baseline.md) | `f7da45591b1ebe2d45342189b9d57045d6555e09c4b33113e6e440bd67a782a5` |
| [修订映射](batch-21-review-fixes.md)，第二十一轮节 L279–282 | `d09b5f8fa1040487e0a7dec8983ec1f3128355f7eb8fa6cc19e3cb0fea1a1324` |
| [第二十次复核](batch-21-t05-01-codex-recheck-20.md) | `de832eb740eb918fa3219892ff7c144b40236cdef357831a06906db8bf0eca29` |
| [初审报告](batch-21-t05-01-codex-review.md) | `341775efc62d7b8d46659c2d272aa31ae301b0cd1db47623ebe86490b80e34b5` |
| [任务验收](../../plans/full-coverage-backlog.yaml)，T05-01 acceptance L5403–5406 | `5f9bcf865b8c77e13cc8ee5f1c03140c37b86f558d8227d8bb2080249f4fcfc3` |
| [来源登记](../../sources/registry.yaml)，440 项 | `e774b5c1440bce91a648d10b1ec8bcad6b70eda8e18883a46a60c5a5585c8bb1` |
| 补读：[作者来源记录](batch-21-t05-01-sources.md)，用于核对前次 C33 口径条件 | `a88ff7db50c3c246567bdbefa3b7825f7bbf6a5c1e3aec35f89e1f302437f6c2` |

已从 `README.md`、`docs/authoring-guide.md` 开始核对仓库要求，并按 `content-outline.md` 核对 05 主归属与相邻边界；相关目录未发现更深层 `AGENTS.md`。写入前保存 Git 状态，并对 Git 所列 tracked/untracked 非忽略路径及既有 build 文件做摘要快照，共 **404 个**既有文件。临时审计目录为 `/private/tmp/b21-t05-01-recheck21-akHhRR/`；构建在其中的独立副本进行，避免重写原仓库 `build/`。

## 3. 一次源抽查方法、文字与限制

### 3.1 curl 实际尝试与只读替代通道

对下表 01–10 的精确 HTTPS URL 实际执行只读 GET。仓库文件使用与表中 blob 链接相同 ref/path 的 `raw.githubusercontent.com` 地址；文档使用表中原 URL。命令形态：

```sh
curl --location --fail --silent --show-error \
  --connect-timeout 8 --max-time 20 --output "$audit_dir/curl-$index.body" \
  --write-out 'http_code=%{http_code}\n' "$url"
```

未用 `-k`/`--insecure`、未关闭默认 TLS 校验、未申请沙箱提权或自定 IP 绕行。**10 次全部在 DNS 阶段失败：退出码 6、HTTP 000、Could not resolve host**，涉及 `raw.githubusercontent.com`、`docs.pytorch.org`、`docs.nvidia.com`。未取得 curl HTTP 正文，不能称 curl 200、TLS 校验成功或已有上游 HTTP 字节摘要。

随后采用用户允许的只读替代通道：GitHub 连接器 `fetch`/`fetch_file` 实读固定 ref 源码，网页读取通道实开版本化 PyTorch/NVIDIA 文档并定位正文。网页通道对最初四个 raw 源码 URL 返回 Cache miss，未将它们计作成功取文；改由 GitHub 连接器读取。较长源码的完整返回有展示截断，关键安装、挂载、节点/许可、hook 与策略区间另用 `fetch_file` 读取，不从截断部分推定语义。网页可能经缓存/解析；连接器 blob SHA 不是 curl 字节摘要。**不是只判可达性，不以搜索片段、作者自述或前次摘录替代本轮取文，也不独立背书历史 curl 成功记录。**

### 3.2 本轮实际核对的关键文字

Ascend 源码均固定 commit `44385c13d7b1d87def35f1604e8be4d16de6ca4e`。源码坐标来自 `fetch_file` 原文件区间或函数名；文档用章节定位，不把网页阅读器行号转为 GitHub 源码锚点。

| curl 点 | 精确一次源 / 实读位置 | 核对内容与有限支持范围 |
|---|---|---|
| 01 | [build/scripts/base.list](https://github.com/Ascend/mind-cluster/blob/44385c13d7b1d87def35f1604e8be4d16de6ca4e/component/ascend-docker-runtime/build/scripts/base.list)，完整五行 | 宿主候选为 `/usr/local/Ascend/driver/lib64`、`/usr/local/Ascend/driver/include`、`/usr/local/dcmi`、`/usr/local/bin/npu-smi`、`/var/queue_schedule`；不是逐库身份/版本或成功挂载记录 |
| 02 | [run_main.sh](https://github.com/Ascend/mind-cluster/blob/44385c13d7b1d87def35f1604e8be4d16de6ca4e/component/ascend-docker-runtime/build/scripts/run_main.sh)，参数默认/安装选择，精读 L278–315 | 未选五种产品安装类型时走默认源列表；各分支均复制为配置目录的 base.list，并设权限 440。支持新增默认安装分支，不据此认定 310B 实际产品或部署兼容 |
| 03 | [cli/src/u_mount.c](https://github.com/Ascend/mind-cluster/blob/44385c13d7b1d87def35f1604e8be4d16de6ca4e/component/ascend-docker-runtime/cli/src/u_mount.c)，Mount/MountFile/MountDir/DoMounting；精读 L54–172 | 宿主目标按 rootfs 与源路径拼接；bind 后只读/nosuid remount；源不存在可以跳过，校验/挂载可失败。NODRV 提前返回仅限定该 CLI 挂载函数，不代表全部 runtime 挂载均消失 |
| 04 | [runtime/process/process.go](https://github.com/Ascend/mind-cluster/blob/44385c13d7b1d87def35f1604e8be4d16de6ca4e/component/ascend-docker-runtime/runtime/process/process.go)，精读 L300–405、L455–812 | 310B manager 辅助函数含 14 个尝试项和 manager 回退；此前另尝试 dvpp_cmdlist；节点信息来自宿主设备，许可写 allow/type/major/minor/access=rwm；UB 有目录/条目条件，非 VIRTUAL 仍可能产生 vdevice/poststop。不是实际设备存在或节点注入成功证据 |
| 05 | [device-plugin common.go](https://github.com/Ascend/mind-cluster/blob/44385c13d7b1d87def35f1604e8be4d16de6ca4e/component/ascend-device-plugin/pkg/common/common.go)，L107–135 | ID 串/options 输出；310B 条件写 allow-link；worker 环境组受非 PresetVDevice 条件控制。芯片示例不能替代 PresetVDevice 设计选择 |
| 06 | [hook/process/process.go](https://github.com/Ascend/mind-cluster/blob/44385c13d7b1d87def35f1604e8be4d16de6ca4e/component/ascend-docker-runtime/hook/process/process.go)，L85–225、L237–410 | mount group 默认 base；每份列表先计扫描行，再判断路径/stat/常规文件或目录；构造 PID/rootfs、文件/目录和条件 options 参数后调用 CLI。候选可因 stat/分类等未入选，不能凭五条源码认定五项已挂载 |
| 07 | [syft README@v1.54.1](https://github.com/anchore/syft/blob/v1.54.1/README.md)，Features/The basics，读取 L1–110 | 提供扫描对象与输出格式入口；这些段落不交付本文所需的固定范围、必要字段、逐库来源层解析与连接规则。不重开 C30 的工具入口条件 |
| 08 | [PyTorch CUDA notes 2.14](https://docs.pytorch.org/docs/2.14/notes/cuda.html)，Device-agnostic code 的 CUDA_VISIBLE_DEVICES 段 | 管理 PyTorch 可用 GPU 范围；这一段不是逐 ordinal→Allocate/CDI/完整节点→稳定身份连接方法，不据此断言其他身份接口不存在 |
| 09 | [NVIDIA server.go@v0.20.1](https://github.com/NVIDIA/k8s-device-plugin/blob/v0.20.1/internal/plugin/server.go)，L280–481 | Allocate 校验请求 ID，按策略转换/去重；按所选策略输出 CDI 或非 CDI 字段，存在组合路径；只写“含 cdi-cri”不足以固定完整对照配置 |
| 10 | [Toolkit 1.20.0 troubleshooting](https://docs.nvidia.com/datacenter/cloud-native/container-toolkit/1.20.0/troubleshooting.html)，权限、访问丢失及 Affected Environments | 权限段提醒禁用 SELinux 会放弃隔离；访问丢失段限定 hook/legacy 与更新场景，CPU/内存限制更新和 systemd 情形有区别。来源场景不等于作者已选更新接口/字段或已完成试验 |
| 补读 | [build/build.sh](https://github.com/Ascend/mind-cluster/blob/44385c13d7b1d87def35f1604e8be4d16de6ca4e/component/ascend-docker-runtime/build/build.sh)，L120–145 | copy_file_output 将默认/产品列表送入安装包，补核源码→打包→安装选择链；未执行脚本 |
| 补读 | [Toolkit 1.20.0 CDI support](https://docs.nvidia.com/datacenter/cloud-native/container-toolkit/1.20.0/cdi-support.html)，Running a Workload / Non-CDI-Enabled Runtimes / Setting the CDI Mode Explicitly | 独立 runtime hook 与 CDI 可冲突；环境变量也可在 CDI 模式消费。故 envvar 本身不能独立确定 legacy 模式，须固定 runtime/handler 消费组合 |

关键连接器 blob SHA：run_main `9be36636ff13c480c57342b81c78f4b74e95675b`、u_mount `d85fd8155a1805edaf509b047c6441bcdc603e12`、runtime `acbd7a1ec0703498abfcfcb6ce1aa493069091b1`、common `6cd038e9f1d67a8a913aa4bb1301692f177b3dbe`、hook `816212afa5f69b8edfb1554d3935af2ebcd28f06`、build `34322058d3784446ce7475bdf7853588c0bb265b`、syft README `9ffd2affa3b00031ea1fd01ee3fe228379978492`、NVIDIA server `9281b48ef52f9eda9cbed6d98491729da85b5a75`。只作上游文件身份，不作 HTTP 字节或现场结果证据；报告只链接并有限归纳，不复制外部全文或改变许可登记。

## 4. 逐项定向复核

### B21-C32 — P2 / OPEN

**权威条件：** 第二十次复核 L88。**位置证据：** 正文 L60、L72、L78、L82–84、L109–112、L114、L118、L131–138；第二十一轮映射 L282。

**认可/保留：** 宿主内核驱动/注入用户态组件/镜像库分层、Allocate/CDI/edits/OCI 连接、节点与访问许可区分、LSM 证据边界继续认可。L112 已区分缺方法/缺采样，L118 的缺规则优先无法确定保留，不重开 C30/C31。

**仍未满足：**

1. **扫描归层与逐库连接方法未交付。** L60/L72 仍用“所选扫描配置”“以实际输出为准”“缺项逐项记 unknown”，未固定扫描范围、必要字段、成分/路径到来源层的解析与逐库连接键。层清单/diff_ids/annotations 和通用箭头不替代所选方法。抽查 07 仅核到工具入口；缺的是设计与依据，不是本轮实际 SBOM 输出。
2. **完整稳定映射方法仍明确缺失。** L78 仍写“稳定物理标识映射方法（未交付，unknown）”；L82–84 是待填表，没有来源支持的逐 ordinal 可见集快照→分配 ID/CDI 名或传递字段→完整节点（类型、major/minor、路径/来源）→稳定身份连接规则。抽查 08 的可见范围说明不补齐该链，不能凭数量或编号猜对应。
3. **分类只局部同步。** L109“未记录即缺失”、L110“无法确定写 unknown”、L111“同上”，没有统一给出方法缺失/采样缺失的原因、具体缺项与记录格式；L114、L131–138 的三单比较也未引用已交付规则。诚实写 unknown 可保留，但不是方法交付。

**剩余关闭条件：** 按固定来源交付所选扫描范围、必要字段、逐库归层及宿主来源→最终挂载→容器目标连接规则；交付逐 ordinal 完整稳定映射方法。把缺方法/缺采样的原因、具体缺项和记录格式同步至核对表、清单及 C34 比较/判定。**现场值可 unknown；不要求拉镜像、生成 SBOM、审计全部 cataloger、采设备或实测；不重开 C30。**

### B21-C33 — P2 / OPEN

**权威条件：** 第二十次复核 L107。**位置证据：** 正文 L31、L42、L90、L92、L147；第二十一轮映射 L281；作者来源记录 L12、L17；登记 L5335、L5446、L5457、L5462。

**本轮认可的落盘进展：**

- L90 现已选择 `UseAscendDocker=true`、空输入 options、mount group base、**无 --install-type 的默认安装分支**及 **310B 芯片示例**。抽查 01/02 支持默认源选择；不再指称未选择芯片/安装分支，也不把 group 与安装类型继续混为一谈。未声称该组合已获产品支持或验证。
- L90 已将默认五项分别选为驱动库、头文件、设备管理、工具和队列候选；**不再指称完全未选必要候选**。源码列表、安装选择和 CLI 通用源/目标规则的已读状态继续认可，未要求阅读五份未选变体或取得实际库版本。
- 作者来源记录 L12 已明确默认列表/安装规则已读；登记 L5335 已把旧宽口径收窄为实际挂载结果/DCMI，且指向 hook/install 登记，**此前针对这两处的旧措辞问题已有修正**。L31/L42/L147 的范围收窄保留。L5446 的四子目录未见不是全树断言，不判作新增全树检索事实错误。

**仍未满足及原 ID 内追记：**

1. **完整所选条件/节点/许可/环境记录仍缺。** L90 明写 `!PresetVDevice` 未知，未选择输入 ID 的设计形式、具体产品/安装选择对应、manager 回退与 UB 条件并形成完整表；L92 仍仅列目标组合字段/支持交集 unknown。抽查 04 表明 310B 的 14 个 manager 项是尝试项，不保证全成功，还应纳入此前的 dvpp_cmdlist 尝试、manager 路径回退、UB 目录项及其失败条件；许可的 allow/type/major/minor/access 与节点/环境须逐段连接。310B 分支提前返回，不要求它再执行后续其他芯片的 GetProductType 分支；产品形态的样板选择/支持材料与实际返回值可区分。已有虚拟/poststop 条件修正须进入所选记录，不要求实际 DCMI 返回值或全实现审计。
2. **五项候选已选，但所选对应记录仍不完整。** L90 的分类括号加公共 rootfs 拼接规则没有逐项交付宿主绝对来源、目录/文件候选身份、hook 入选/跳过及 CLI 消费条件、rootfs 宿主目标与容器内目标对应，亦未单列驱动库候选中具体库身份/版本的待采位置。来源 01/03/06 现在可支持这些有限记录；审阅者补读的绝对路径不能代替作者补交。必要目录/库候选可以条件化，文件身份/版本/挂载结果可待采，不要求全目录审计或虚构库名。
3. **口径尚未全篇一致。** 正文 L90 仍两次写“runtime 库注入语义未核对”，另有“实际库挂载来源/目标/白名单未取”，与同段已读源码/通用目标规则并列而未限定到所选记录或现场结果。来源记录 L17 仍将库挂载/白名单/hook 可执行/DCMI 合列 unknown，未落实机制已读、所选记录未交付、现场未采三分。L12/登记 L5335 的修正不能替代这些位置的精确同步。登记 L5446 应清楚区分源码列表与安装后文件，并关联现有 build/scripts 正面证据；不把有限目录描述改判为全树错误。

**剩余关闭条件：** 保留本轮已选芯片示例、默认安装分支、五项候选和口径修正；补齐产品/输入 ID/PresetVDevice/manager/UB 的设计条件，交付完整节点/许可/环境及条件化虚拟/poststop 记录。依据已读源码→打包/安装→hook→CLI 链补逐项必要目录/库候选的来源、入选与目标对应记录，区分已知规则与待采身份/版本/结果。同步正文和作者记录的旧宽口径及登记的源码/部署产物边界，明确三分状态。**现场文件/设备号/库版本/挂载结果可待采，支持交集可 unknown；不要求安装、执行脚本、实测、完整 DCMI/全部白名单或 CLI 审计。**

### B21-C34 — P1 / OPEN

**权威条件：** 第二十次复核 L122。**位置证据：** 正文 L118–125、L127、L131–138、L140–142；第二十一轮映射 L282 未列完整对照设计补交。

**认可/保留：** 多策略可能、CDI 自身 hooks 与独立 legacy 区分、有序完整许可比较对象、S1/R1、旧新主体/时间窗、回退与更新/重建拆分、副本数作用域收窄、NPU 独立对照未知、源案例缺项及授权/未执行边界继续认可。L127 有公共恢复对象格式，**不指称完全没有恢复记录，也不要求逐行机械重复**。

**仍未满足：**

1. **两端完整配置对仍未选定。** L132 基线仍“含 cdi-cri”，变体仍“envvar 或 volume-mounts”；未固定两端完整策略集合、runtime 模式/handler 消费组合及字段。抽查 09 与 CDI 补读确认组合与环境变量消费存在条件；混合路径判无法确定是判据，不是完整对照选型。站点 handler 名和现场旧新值可待填，设计选型不能以待填代替。
2. **资源更新接口/完整字段仍缺。** L137 仍列 CRI 更新对象/OCI linux.resources.cpu 为候选并明写“固定字段未取，unknown”；未选择接口、完整字段、单位/语义及旧新记录格式，未绑定同一次更新前后采样。抽查 10 只支持源场景；镜像/驱动回退或重建不替代资源更新对照。
3. **成功访问/原负向边界恢复与各生命周期关联仍不足。** L127 有 audit/AVC、三元组和配置摘要，但未选择受控成功访问操作与可定位结果记录，也未给单独授权负向拒绝的记录形式和统一连接键，连接各变体更新/重建前后、恢复后的主体、目标节点/稳定身份及时间窗。L133、L135–138 仍主要靠拒绝事件/注入集/“同上”。未见拒绝、摘要或可见集恢复不证明成功访问及原负向边界恢复；公共规则可复用，但须能关联具体生命周期。
4. **C32 方法依赖未闭合。** 三单比较仍依赖未交付的完整稳定映射；缺方法/缺采样的原因及字段未同步。这是 C32 同一缺口的依赖引用，不另计发现，也不替代前三项独立设计要求。

**剩余关闭条件：** 固定两端完整传递策略集合、runtime 模式/handler 消费组合、字段及旁路排除；保留 CDI hooks/独立 legacy 与许可比较边界。选定资源更新接口、完整字段、单位/语义及旧新记录格式。完善成功访问和原负向边界恢复的设计记录，以公共连接规则对应各变体更新/重建前后及恢复后的主体、目标节点/稳定身份、时间窗和可定位结果。引用 C32 已交付方法，缺方法优先无法确定并区分缺采样。保留 NPU 独立未知、S1/R1、回退拆分和安全授权边界。**不要求执行试验、取得现场值、扩大生产权限或制造结果；无负向授权不执行。**

## 5. Acceptance 与最终计数

| T05-01 acceptance / 原文件位置 | 本轮判断 | 原 ID |
|---|---|---|
| 镜像身份、构建输入、SBOM/签名、拉取策略 / L5403 | 沿用此前完整通过；范围外，不重审供应链 | C30 CLOSED |
| 固定 runtime/Toolkit/CDI、各层与映射分离 / L5404 | 部分满足，未完整通过：逐库归层、稳定映射及分类仍缺 | C31 CLOSED（范围外）；C32 OPEN |
| Ascend 独立实现与目标组合 / L5405 | 部分满足，未完整通过：新条件/默认列表选择认可，完整所选输出/必要库对应记录及精确口径仍缺 | C33 OPEN |
| 清单、异常/隔离、对照与源案例 / L5406 | 部分满足，未完整通过：完整配置对、更新接口/字段、访问恢复关联与映射依赖仍缺 | C34 OPEN |

四条 acceptance：**1 沿用既有完整通过 / 3 未完整通过**。本轮 **0 CLOSED / 3 OPEN（1 P1、2 P2）**，**第二十一次定向复核不通过**，无新增发现 ID。阻断来自未交付的方法、所选记录、对照与证据关联及口径一致性，**不是 curl DNS 失败、现场值 unknown、没有实测或未证明整栈兼容**；不改计划或正文审核状态。

## 6. 结构校验与写入审计

- 写入前原仓库 `PYTHONDONTWRITEBYTECODE=1 make check` **PASS：96 content entries / 440 sources**；只验证结构与本地链接，不验证远程文字或技术正确性。
- 写入后原仓库 `PYTHONDONTWRITEBYTECODE=1 make check` **PASS：96 content entries / 440 sources**。
- 独立副本 `/private/tmp/b21-t05-01-recheck21-akHhRR/validation` 使用原仓库虚拟环境 Python、禁写字节码执行 `make check` / `make build`，均 **PASS：96 content entries / 440 sources**；只在副本生成 `build/catalog.json` / `build/catalog.md`，未改原仓库生成文件。本节补记后同步最终报告至副本并复跑校验/构建。
- 摘要审计覆盖 **404 个**既有文件：无修改或删除，唯一新增为本报告；去除本报告后的 Git 状态与写入前一致，六个指定输入及补读作者记录均保持 §2 摘要。`git diff --check` 与本报告行尾空白检查通过；报告仅含 C32/C33/C34 三个原发现标题，优先级与 OPEN 状态一致。
- 未修改 `src/kb/` 或测试；内容审阅报告不需要新增测试或执行 `make test`。

**最终技术结论：B21-C32、B21-C33、B21-C34 均 OPEN；0 CLOSED / 3 OPEN，第二十一次定向复核不通过。C30/C31 保持此前 CLOSED、范围外；本轮新增芯片示例、安装选择、五项候选及部分口径修正已认可，不以审阅者补读替代作者所选样板和方法交付；约定审阅配置不是已独立确认的执行元数据。**
