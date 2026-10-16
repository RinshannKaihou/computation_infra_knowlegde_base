# Batch 21 补交 T05-01 第十六次定向复核

## 1. 结论、角色与范围

- 日期：2026-10-14（Asia/Shanghai）。执行者：当前 Codex 会话，以独立审阅角色核对作者第十六轮修订；与作者修订角色分开，未派发其他模型或子代理。
- `gpt-6.1-sol / xhigh` **仅为用户约定**，不是本会话已独立确认的执行元数据。未取得可独立核验的实际模型、推理档位或路由信息，不宣称实际模型一致性或无 fallback 已获独立确认。
- 唯一复核范围为 **B21-C32–C34**；剩余关闭条件以[第十五次复核](batch-21-t05-01-codex-recheck-15.md) L81、L95、L109 为权威。[初审报告](batch-21-t05-01-codex-review.md)用于核对原 ID、优先级和职责。C30/C31 保持此前 CLOSED、范围外，不重审。
- **0 CLOSED / 3 OPEN（1 P1、2 P2）；第十六次定向复核不通过。** 独立确认本轮新增 hook 入口、白名单读取机制和 CLI 参数构造的实质取证；不再沿用“hook 可执行内部完全未读”的旧判断。但所选条件对应、库挂载源/目标方法及其他剩余设计条件未闭合，不能把局部取证计为整项关闭。
- 没有新增发现 ID；hook 摘要的精确化及已读/未知范围同步继续归入 C33，映射与对照设计分别归入 C32/C34。
- 未安装组件、拉取或构建镜像、运行容器、生成 SBOM、采集设备、修改运行配置、接入集群或执行访问/负向/恢复实测。知识库结构检查与目录构建不是容器或硬件验证。

| 原 ID | 原优先级 | 本轮状态 | 正文位置 / 主要剩余问题 |
|---|---|---|---|
| B21-C32 | P2 | OPEN | L71、L77、L81–83、L108–113、L117、L130–137：所选扫描归层、逐 ordinal 稳定映射方法未交付，缺方法/缺采样未全量同步 |
| B21-C33 | P2 | OPEN | L30、L41、L89、L91、L146；作者记录 L12、L17；登记 L5441–5451：hook 机制取证已补，但所选产品/输入条件与完整节点/许可/环境表、必要库挂载源/目标仍缺，未知范围未清楚分层 |
| B21-C34 | P1 | OPEN | L126、L131–137：完整模式配置对、资源更新接口/字段、成功访问与负向恢复的逐变体关联仍缺，并依赖 C32 缺失方法 |

## 2. 输入身份与单文件边界

用户给出的 **4 个 SHA-256 前缀全部吻合**。下列摘要取自本轮起始输入；仓库行号均为原文件坐标。

| 输入 | 起始 SHA-256 |
|---|---|
| [正文](../../knowledge/05-cluster-platform/container-image-runtime-baseline.md)，146 行 | `81671c99377212951413cd37c89708e5fbf82a1e035ae7204b751ae18b84cb7e` |
| [作者来源记录](batch-21-t05-01-sources.md)，28 行 | `a74909d083aae8cc69a016a1adcfa11b6f771bf7ca7aaf2dc1b1c2aa720ba56e` |
| [修订映射](batch-21-review-fixes.md)，257 行 | `35ff5fd993120315fb97e4e30d07525f7d9e2bc56a2291ae1fa2071d826dc3dc` |
| [第十五次复核](batch-21-t05-01-codex-recheck-15.md) | `961979aeaf92e5f6e8505537ee50d0c1bb347a0e0398589e029de70f32911ecb` |
| [初审报告](batch-21-t05-01-codex-review.md) | `341775efc62d7b8d46659c2d272aa31ae301b0cd1db47623ebe86490b80e34b5` |
| [任务计划](../../plans/full-coverage-backlog.yaml)，T05-01 acceptance L5403–5406 | `5f9bcf865b8c77e13cc8ee5f1c03140c37b86f558d8227d8bb2080249f4fcfc3` |
| [来源登记](../../sources/registry.yaml)，439 项 | `0cdd65ae389357fb7e0bee9d6c2314db18862b4dd19281b9311585fc5a065d11` |

仅采用修订映射的 **T05-01 第十六轮节 L254–257** 作为落盘改动索引，不以作者自述充当关闭证据。已读取 README、编写指南、内容总目录与 metadata schema；主归属仍为 05.1/05.5，正文仍为 `draft / source_checked`，不变更编辑或任务状态。

起始工作区已有修改及未跟踪文件，均保留、不回滚。原仓库唯一写入目标为本报告。curl 诊断、摘要审计与隔离构建位于 `/private/tmp/b21-t05-01-recheck-16.swMjfr/`，不作为永久来源附件或知识内容；未复制上游全文入仓库。

## 3. 一次源文字抽查与方法限制

### 3.1 curl 实际请求

本机 curl **8.7.1**，对下表 01–12 各执行一次只读 GET；GitHub 文件使用同仓库/ref/路径的 `raw.githubusercontent.com` 原文地址，厂商/PyTorch 页面使用表列版本 URL。调用形态为：

```bash
curl --disable --location --silent --show-error --connect-timeout 8 --max-time 20 \
  --output "$audit_dir/$point.body" --write-out '%{http_code}' "$url"
```

使用默认 TLS 校验，未使用 `-k`、改 DNS/证书、提权或绕过沙箱。**12/12 退出码 6、HTTP `000`，诊断均为 `Could not resolve host`。** 未取得 curl 响应正文，TLS 握手未发生；不声称 curl 成功、HTTP 200 或本机完成证书验证。登记中的历史请求记录不作为本轮 curl 结果。请求与诊断保存在临时目录的 `urls.txt`、`curl-results.tsv`、`*.stderr`。

### 3.2 允许的只读替代通道

使用 `web.run` 打开版本化文档及 README，并读取实际支持段落；使用 GitHub 只读连接器读取固定 ref 的原文件区间，核对字段和控制流，**不是只判可达性**。网页通道可能使用缓存或归一化文本，不等于本机即时 GET；版本 URL 不自动构成不可变快照。下表源码坐标来自连接器的原文件区间，网页以章节定位，不将网页阅读器坐标拼成 GitHub 行号。

| 点 | 本轮实际阅读的一次源 / 位置 | 核对文字及有限支持范围 |
|---|---|---|
| 01 | [syft README@v1.54.1](https://github.com/anchore/syft/blob/v1.54.1/README.md)，Features / The basics | 支持镜像/文件系统成分扫描和输出格式入口；不能替正文选定扫描范围、必要字段及逐库归层规则。不重开 C30。 |
| 02 | [PyTorch CUDA notes 2.14](https://docs.pytorch.org/docs/2.14/notes/cuda.html)，Best practices / Device-agnostic code 的 `CUDA_VISIBLE_DEVICES` 段 | 支持管理 PyTorch 可见集；该段不是正文所需的逐 ordinal→分配/注入对象→完整节点→UUID 连接规则，不据此否定其他身份接口。 |
| 03 | [Ascend common.go@44385c13](https://github.com/Ascend/mind-cluster/blob/44385c13d7b1d87def35f1604e8be4d16de6ca4e/component/ascend-device-plugin/pkg/common/common.go)，L90–130 | 有效响应内 ID 串/options、310B allow-link、`!PresetVDevice` worker 组条件分开；不能仅选 `UseAscendDocker=true` 就推定全部字段恒有。 |
| 04 | [Ascend runtime/process/process.go@44385c13](https://github.com/Ascend/mind-cluster/blob/44385c13d7b1d87def35f1604e8be4d16de6ca4e/component/ascend-docker-runtime/runtime/process/process.go)，L60–130、L243–291、L330–405、L455–810、L850–910 | 核对 env 搜索路径、VIRTUAL 提前返回、CreateVDevice/poststop、节点/许可、manager 产品分支、UB 和设备非空分支；不把 env 路径改写当作库挂载。 |
| 05 | [Ascend hook/main.go@44385c13](https://github.com/Ascend/mind-cluster/blob/44385c13d7b1d87def35f1604e8be4d16de6ca4e/component/ascend-docker-runtime/hook/main.go)，全文 / `main()` | 入口先做日志初始化和参数检查，再调用 `process.DoPrestartHook()`，错误走退出路径。确认作者本轮新增入口取证。 |
| 06 | [Ascend hook/process/process.go@44385c13](https://github.com/Ascend/mind-cluster/blob/44385c13d7b1d87def35f1604e8be4d16de6ca4e/component/ascend-docker-runtime/hook/process/process.go)，全文，分段 L1–120、L121–235、L236–355、L356–文件末 | 核对 stdin state/bundle/rootfs/env、mount group/default、每份 `.list` 读取限制、UB 候选、options/allow-link、CLI 路径/参数及 `syscall.Exec`。这是挂载候选与参数构造证据，不是实际挂载成功或库目标路径的完整证据。 |
| 07 | [CDI SPEC@cb98bcf6](https://github.com/cncf-tags/container-device-interface/blob/cb98bcf66dc68530012483bd56e33e14d815e167/SPEC.md)，L90–175 | 全局/设备级 edits 应用条件及节点、挂载、环境、hooks 字段分开；CDI edits 自身可以带 hooks。 |
| 08 | [OCI config-linux.md@92249139](https://github.com/opencontainers/runtime-spec/blob/92249139eea7161e13745abd4cb6d0ea02a3227a/config-linux.md)，L127–151、L402–418 | 节点与访问许可分开；许可列表有序，设备类型/设备号未指定有通配语义。保留已经交付的完整许可比较对象。 |
| 09 | [Toolkit 1.20.0 CDI support](https://docs.nvidia.com/datacenter/cloud-native/container-toolkit/1.20.0/cdi-support.html)，Running a Workload / Non-CDI-Enabled Runtimes / Setting the CDI Mode Explicitly | 区分原生 CDI、NVIDIA runtime CDI 模式与独立 Runtime Hook；CDI 模式也可使用选择变量，变量存在不证明 legacy。 |
| 10 | [Toolkit 1.20.0 troubleshooting](https://docs.nvidia.com/datacenter/cloud-native/container-toolkit/1.20.0/troubleshooting.html)，NVML/SELinux、Unknown Error / Affected Environments / Mitigations | 区分权限与 hook/legacy 更新访问丢失；说明显式 CPU/内存更新及 systemd 条件，不替正文选定更新接口/完整字段。未执行任何处置建议。 |
| 11 | [NVIDIA README@v0.20.1](https://github.com/NVIDIA/k8s-device-plugin/blob/v0.20.1/README.md)，Configuration Option Details / Shared Access / With CUDA Time-Slicing | 设备列表策略可多选，cdi-cri 需 CRI 转发和消费端支持；副本计数不是隔离成立证据。 |
| 12 | [NVIDIA server.go@v0.20.1](https://github.com/NVIDIA/k8s-device-plugin/blob/v0.20.1/internal/plugin/server.go)，L280–370、L378–481 | `AnyCDIEnabled`/`AllCDIEnabled` 控制流允许混合策略继续加 envvar/volume-mounts，另有 `PassDeviceSpecs` 条件；cdi-cri 写 `CdiDevices[].Name`。只写“含 cdi-cri”未排除其他路径。 |

本轮连接器返回的文件 blob SHA：common.go `6cd038e9f1d67a8a913aa4bb1301692f177b3dbe`；runtime/process/process.go `acbd7a1ec0703498abfcfcb6ce1aa493069091b1`；hook/main.go `be190334836e2461727238cf3e773f07df0fc3ae`；hook/process/process.go `816212afa5f69b8edfb1554d3935af2ebcd28f06`；CDI SPEC `2bc480a20ce447f5281b5d6844a486a81bb635b0`；OCI Linux `c71757494ca743fd90692c25e4897bf74cf00388`；NVIDIA server.go `9281b48ef52f9eda9cbed6d98491729da85b5a75`。这些是文件 blob，不冒充 commit SHA。

## 4. 逐项复核与剩余关闭条件

### B21-C32 — P2 / OPEN

**权威条件：** 第十五次复核 L81。**位置证据：** 正文 L71、L77、L81–83、L108–113、L117、L130–137；第十六轮映射 L257。

**认可的修订/保留边界：** L111 明示“规则未交付→无法确定（缺方法，当前状态）”与“规则已交付但样本缺项→无法确定（缺采样）”，L117 也将缺规则置于技术完成/失败之前。诚实限定继续认可；此前 Allocate/CDI/edits/最终 OCI 链、节点与许可/LSM 分离、不以数量或编号文本证明同一设备的边界不重开。

**仍未满足：**

1. **扫描归层仍是入口和待选字段，不是所选方法。** L71 继续使用“所选扫描配置”“字段以实际输出为准”，未交付具体扫描范围、必要字段、成分/路径→来源层规则。镜像 digest→层清单→SBOM→宿主来源→最终挂载→容器目标路径的串联已写出，但每段的连接键/规则仍未固定。抽查 01 只支持工具入口，不能用层清单、diff_ids、annotations 或共同漏检边界替代逐库归属规则。
2. **逐 ordinal 稳定映射仍明确未交付。** L77 继续写“未交付，unknown”；L81–83 是待填表，而非可据此填写的映射规则。抽查 02 只支持可见集管理。仍缺框架 ordinal/可见集快照→分配 ID/CDI 名或传递字段→完整节点（类型、major/minor、路径/来源）→稳定身份的来源支持连接方法。
3. **缺失分类未全量同步。** L108 仍仅“未记录即缺失”，L109 为“无法确定写 unknown”，L110 为“同上”；L113 依赖“按已取证映射对应”。L117 的缺规则门槛不补成所需方法，L130–137 也没有统一引用一个已交付规则及缺方法/缺采样记录格式。第十六轮映射 L257 仍承认“方法仍 unknown”。

**剩余关闭条件：** 在固定来源上交付所选扫描范围、必要字段与逐库归层规则，连接镜像库、宿主注入来源、最终挂载和目标路径；交付逐 ordinal 的完整稳定映射规则。将缺方法/缺采样的原因、缺项与记录格式同步到核对表、清单和 C34 的映射依赖比较/判断。**现场值可 unknown；不要求拉取镜像、生成 SBOM、采集设备、审计全部 cataloger 或实测；不重开 C30。**

### B21-C33 — P2 / OPEN

**权威条件：** 第十五次复核 L95。**位置证据：** 正文 L30、L41、L89、L91、L146；作者记录 L12、L17；第十六轮映射 L256；登记 L5441–5451（新增 hook）、L5335（common 局部范围）、L5419–5429（runtime）。

**认可的本轮实质补充：** 抽查 05/06 独立确认 hook 入口与内部机制已取证。L89 和新增登记不再只有 prestart-hook 的路径名；作者来源记录 L12 也明确“hook 白名单机制与 CLI 调用参数已读”。**关闭“必要 hook 可执行内部尚未读取”这一子条件，不宣称 C33 整项 CLOSED。** VIRTUAL 提前返回/独立 vdavinci 选择、非提前返回后的 CreateVDevice/poststop 条件、A/B 互斥路径、原生 `rw` 不拼 wrapper `rwm`、env 搜索路径不当库挂载等此前修正继续认可。

独立核对所得的精确支持边界如下，均来自抽查 06，不代表执行结果：

- `getContainerConfig` 从 stdin 解码 state，读取 bundle `config.json`，使用 `Process.Env`；rootfs 为相对路径时与 bundle 连接，Pid 来自 state。hook 的可见变量检查只测空串，不把 runtime 侧 `void` 的提前处理移植为 hook 内部规则。
- `parseMounts` 在空串或长度超过 128 时返回 `base`；否则按逗号切分、去空白并转小写。配置目录仍由 `api.RunTimeDConfigPath` 提供；仅该文件的符号引用不能证明实际环境变量字符串键或目录值已经取得。
- `readMountConfig` 的 **128 限制是每份 `.list` 扫描的行数**，计数发生在路径解析/stat/分类前；不是合并后全部 mount 参数总数上限。单份列表选取 stat 后的常规文件/目录，多个配置列表合并；`addUBMount` 再独立追加存在的 `/etc/hccl_rootinfo.json` 与 `/usr/local/Ascend/driver/topo` 候选。L89/登记 L5446 的“白名单≤128条”应按这个作用域精确化，不扩大到整条 CLI 调用。
- `parseRuntimeOptions` 接受空 options；非空仅接受 `NODRV`/`VIRTUAL`。`parseSoftLinkMode` 接受 `True`、`False`，空串默认 `False`。`getArgs` 添加 allow-link/Pid/rootfs 及逐项 mount 参数；**仅 parsedOptions 非空时添加 `--options`**。实际调用目标是 hook 可执行同目录的 CLI，并用宿主 `os.Environ()` 执行。参数构造不证明 CLI 挂载目标、结果或安全检查已完成。

**仍未满足：**

1. **仍未选定一组完整条件并交付对应表。** L89 虽称“条件固定”，实质仍是 310B/910A5/default、Atlas 产品、UB 存在条件和 VIRTUAL 的分支摘要；没有选定产品、输入 ID/options、PresetVDevice 与实际环境键，并据此给出完整节点/许可/环境对应。抽查 03/04 确认这些条件各自影响输出：例如非 310B 路径先加 manager，Atlas200ISoc/Atlas200 与其他产品再决定公共 manager 设备；不能从芯片摘要单独推定最终节点集。支持交集和现场值可 unknown，但不能代替设计选型。
2. **白名单机制已读，不等于所选库来源/目标已交付。** 新补代码读出候选宿主路径并构造 `--mount-file/--mount-dir/--rootfs`，尚未选择 mount group/必要 `.list` 内容，也未交付来源库→CLI 消费规则→容器目标路径的连接。L89 后半仍将实际库来源/目标列为未取。未执行可使挂载结果保持 unknown，**不要求实测**；但必要源/目标语义的只读取证仍是前次关闭条件。
3. **已读/未读/未执行口径仍未清楚分层。** L30/L41 仍概括“白名单未取”；L89 后半仍写“环境变量与白名单未取源”，作者记录 L17 仍把白名单/hook 可执行与 dcmi 合列 unknown，L146 也未清楚归入新增 hook 机制。允许“所选列表实际内容/库目标未读、执行结果未采”，但应与已核对的白名单机制/入口/参数区分，避免旧的整体未取表述掩盖本轮已完成部分。登记 L5446/L5451 已注明新增已读范围，无需否定其局部取证。

**剩余关闭条件：** 保留已确认的 hook 机制及修正后的 VIRTUAL/common 条件；为所选 `UseAscendDocker=true` 样板确定产品、输入 ID/options、PresetVDevice、mount group 等必要设计条件与实际环境键，交付完整节点/许可/环境对应表，按所选条件覆盖 manager/产品/UB，并明确虚拟/poststop 纳入或排除。补必要库挂载来源/目标与所选白名单依据，精确化每列表 128 行及条件化参数的摘要，同步正文/作者记录/登记的“机制已读、具体源/目标未读、结果未执行”范围。**现场值、未选原生路径真正消费端和支持交集可 unknown；不要求安装、试运行、完整 dcmi/全部白名单审计或实测。**

### B21-C34 — P1 / OPEN

**权威条件：** 第十五次复核 L109。**位置证据：** 正文 L108–113、L117–124、L126、L130–137、L139–141；第十六轮映射 L257。

**认可的已有交付：** 策略可多选、CDI 自身 hooks/独立 legacy 区分、有序完整许可比较、S1/R1、旧新主体与时间窗、镜像/驱动回退和更新/重建拆分、replicas 解释收窄、NPU 独立对照未知及授权/安全边界继续认可。L126 已有公共 R1 证据对象格式，不再说完全没有记录对象，也不要求每行机械复制公共集合。

**仍未满足：**

1. **模式配置对仍未固定。** L131 基线仍是策略“含 cdi-cri”，变体仍是“envvar 或 volume-mounts”；未选定两端完整策略集合、runtime 模式/handler 消费组合、传递字段与并行 DeviceSpec/其他路径排除。抽查 11/12 确认组合策略可继续产生其他传递字段；抽查 09 确认选择变量也可由 CDI 模式消费。已有混合路径判据不是受控两端的配置选型，站点 handler 名和现场旧新值可待填，逻辑组合仍须选定。
2. **资源更新接口/字段仍明确未取。** L136 仍写候选为 CRI 更新对象/OCI `linux.resources.cpu`、“固定字段未取，unknown”。抽查 10 支持 CPU/内存显式更新场景，不提供本文选型。仍须确定接口、完整字段、单位/语义及旧新记录格式，并连接更新前后采样；镜像/驱动回退和重建记录不能替代资源更新生命周期。
3. **R1 仍缺成功访问和原负向边界的可定位记录及逐变体绑定。** L126 提供 audit/AVC 路径、进程/设备/时间、恢复后摘要与主体窗，却没有选定受控成功访问操作/结果记录、单独授权的负向拒绝记录，以及它们与各变体更新/重建前后和恢复后主体、目标节点、时间窗的连接键。L132 等仍以拒绝事件/注入集为主要证据；无拒绝、配置摘要或三单可见性不能替代成功访问与负向恢复比较。公共格式可复用，但“同上”须引用可落实到每个生命周期的绑定规则。
4. **C32 映射依赖仍未补齐。** 三单物理对应仍依赖未交付的稳定映射规则，缺方法/缺采样也未同步全表。该依赖沿用 C32 同一缺口，不另立 ID，不把映射记录与异常验证设计混为一项。

**剩余关闭条件：** 固定两端完整设备传递策略集合及 runtime 模式/handler 消费组合、字段与旁路排除，保留 CDI 自身 hooks/独立 legacy 区分。保留已补许可比较字段，选定资源更新接口、完整字段及旧新记录格式。完善 R1 的受控成功访问与原负向边界恢复记录，将主体/目标节点/时间窗按各变体更新或重建生命周期绑定到可定位证据；公共格式可统一引用，无需逐行复制。统一引用 C32 已交付方法，缺方法时优先无法确定并区分缺采样。保留 NPU 独立对照未知、S1/R1、回退拆分及全部授权/安全边界。**不要求执行试验、取得现场值、扩大生产权限或制造结果。**

## 5. Acceptance 与最终计数

| T05-01 acceptance / 原文件位置 | 本轮判断 | 原 ID |
|---|---|---|
| 镜像身份、构建输入、SBOM/签名、拉取策略 / L5403 | 沿用此前完整通过；范围外，不重审供应链 | C30 CLOSED |
| 固定 runtime/Toolkit/CDI、各层与映射分离 / L5404 | 部分满足，未完整通过：扫描归层和稳定映射方法/分类同步仍缺 | C31 CLOSED（范围外）；C32 OPEN |
| Ascend 独立实现与目标组合 / L5405 | 部分满足，未完整通过：hook 机制/参数已补，但所选条件对应与必要库源/目标仍缺 | C33 OPEN |
| 清单、异常/隔离、对照及源案例 / L5406 | 部分满足，未完整通过：配置对、资源更新字段、访问/恢复关联及映射依赖未闭合 | C34 OPEN |

四条 acceptance 汇总：**1 沿用既有完整通过 / 3 未完整通过**。本轮范围 **0 CLOSED / 3 OPEN（1 P1、2 P2）**，**第十六次定向复核不通过**；没有新增 ID。阻断依据是尚未交付的具体方法、条件对应与证据关联，**不是 curl DNS 失败、现场值 unknown、没有实测或未证明整栈兼容**。不变更正文或任务验收状态。

## 6. 结构校验与写入审计

- 写入前原仓库 `PYTHONDONTWRITEBYTECODE=1 make check` **PASS：96 content entries / 439 sources**；只验证结构与本地文件链接，不验证技术正确性或远程内容。
- 写入后原仓库 `PYTHONDONTWRITEBYTECODE=1 make check` **PASS：96 content entries / 439 sources**。
- 为遵守单文件写入边界，在 `/private/tmp/b21-t05-01-recheck-16.swMjfr/validation/` 复制起始源文件、本报告及既有 build 链接目标，用原仓库虚拟环境 Python、禁写字节码执行 `make check` / `make build`，均 **PASS：96 content entries / 439 sources**。仅在副本重新生成 `build/catalog.json` 和 `build/catalog.md`，未改原仓库生成文件；最终补记后再同步本报告并复跑同样检查。
- 摘要审计覆盖 **399 个**起始 Git 所列 tracked/untracked 非忽略文件及 build 文件：既有文件摘要不变，唯一新增为本报告；七个输入保持 §2 摘要。原 ID/优先级/OPEN 状态、无新增 ID、9 个本地 Markdown 链接及行尾空白检查均 **PASS**；临时诊断和副本不属于原仓库改动。
- 本会话未修改作者正文、作者来源记录、修订映射、来源登记、任务计划或其他既有文件；结构与构建 PASS 不改变 §4 技术状态。
- 未修改 `src/kb/` 或测试，本轮不需要 `make test`。未执行容器或硬件实测。

**最终技术结论：B21-C32、B21-C33、B21-C34 均 OPEN；0 CLOSED / 3 OPEN，第十六次定向复核不通过。C30/C31 保持此前 CLOSED、范围外；用户约定配置不作为已独立确认的执行元数据。**
