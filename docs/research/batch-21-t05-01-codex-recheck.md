# Batch 21 补交 T05-01 定向复核（作者首轮修订后）

## 1. 结论、角色与范围

- 复核日期：**2026-10-14（Asia/Shanghai）**，以本机日期为准。
- 执行者：本会话 Codex，承担独立审阅角色；本轮未参与作者修订，也未改作者正文、来源记录、修订映射、来源登记或计划。
- 用户约定配置：`gpt-6.1-sol / xhigh`。**这只是用户约定，不是本轮已独立确认的执行元数据**；本轮没有取得可独立核验的实际模型标识或 reasoning 配置，不据模型自述确认，也没有另行派发模型。
- 仅复核 **B21-C30–C34**。关闭条件以[前次初审报告](batch-21-t05-01-codex-review.md) §6 为权威；作者“独立复核初审取证点”的自述不是关闭证据。本轮事实纠偏在原 ID 下追记，不新增发现 ID。
- 结果：**0 CLOSED / 5 OPEN（1 P1、4 P2），定向复核不通过，仍需修订**。四条 acceptance 均未完整满足。已有修订获得下文逐项认可，但不能把列出字段、版本名或 `unknown` 视为交付完整方法。
- 未开展镜像构建、拉取、验签、容器启动、配置变更、设备访问或 GPU/NPU 实测；结构检查与知识库目录构建不属于此类实测。正文仍为 `reference / draft`；本报告不建立兼容组合或硬件验证结论。

## 2. 输入身份（SHA-256）

以下为本轮读取并据以判断的六个文件完整字节摘要。位置均采用这些输入的本地原文件行号，不沿用初审时正文的旧行号。

| 输入 | SHA-256 |
|---|---|
| [正文](../../knowledge/05-cluster-platform/container-image-runtime-baseline.md) | `dadd0692542ac0b37c20879345898b0e13b8a7a87c89054569054b709c5a17d4` |
| [作者来源记录](batch-21-t05-01-sources.md) | `8a10aabc969984479221f36f1c1f051702c6cfc0a5f30b13fcfd15340bd6408b` |
| [修订映射](batch-21-review-fixes.md)（T05-01：L92–99） | `5d565b04286daf00a0559b0da4c041917481f780114b6995fed81a182a489920` |
| [前次初审报告](batch-21-t05-01-codex-review.md) | `341775efc62d7b8d46659c2d272aa31ae301b0cd1db47623ebe86490b80e34b5` |
| [任务验收计划](../../plans/full-coverage-backlog.yaml)（T05-01：L5386–5418） | `5f9bcf865b8c77e13cc8ee5f1c03140c37b86f558d8227d8bb2080249f4fcfc3` |
| [来源登记](../../sources/registry.yaml) | `a0175ed9dbf20349a294226227feeda9bdaa9a4c424e544c7fff42fd66297ca4` |

补充读取了 README、编写指南、内容总目录，以及正文实际链接的[Ascend 来源案例](../../knowledge/05-cluster-platform/ascend-device-visibility-source-case.md)、[待执行实验](../../knowledge/05-cluster-platform/ascend-device-visibility-experiment.md)和[设备链条](../../knowledge/05-cluster-platform/device-resource-chain.md)。这些是关联解释，不替代上述六个主输入，也不扩大为对关联条目的重新验收。

## 3. 一次源抽查方法与限制

### 3.1 curl 实际尝试

在默认 TLS 校验下执行四次只读 GET，实际命令形态为：

```bash
curl --fail --silent --show-error --location \
  --connect-timeout 10 --max-time 25 \
  --output <临时文件> \
  --write-out 'http=%{http_code}; effective_url=%{url_effective}; bytes=%{size_download}\n' \
  <精确URL>
```

未使用 `-k`/`--insecure`，未关闭 TLS 校验或修改 DNS/代理配置。结果如下；失败发生在域名解析阶段，**未获得远端正文，也未进入 TLS 握手**：

| 精确请求 | 结果 |
|---|---|
| [OCI annotations.md@v1.1.1](https://raw.githubusercontent.com/opencontainers/image-spec/v1.1.1/annotations.md) | exit 6；HTTP 000；0 bytes；`Could not resolve host: raw.githubusercontent.com` |
| [Toolkit 1.20.0 troubleshooting.html](https://docs.nvidia.com/datacenter/cloud-native/container-toolkit/1.20.0/troubleshooting.html) | exit 6；HTTP 000；0 bytes；`Could not resolve host: docs.nvidia.com` |
| [Ascend plugin.go@44385c13](https://raw.githubusercontent.com/Ascend/mind-cluster/44385c13d7b1d87def35f1604e8be4d16de6ca4e/component/ascend-device-plugin/pkg/server/plugin.go) | exit 6；HTTP 000；0 bytes；`Could not resolve host: raw.githubusercontent.com` |
| [CDI 仓库 v1.1.1](https://github.com/cncf-tags/container-device-interface/tree/v1.1.1) | exit 6；HTTP 000；0 bytes；`Could not resolve host: github.com` |

因此，**本轮没有完成“以 curl 成功取得一次源文字”的指定方法**。依用户允许的替代方式，随后使用只读网页通道 `web.run` 与 GitHub 连接器读取一次源正文、固定源码片段和 Git ref 对象，核对文字而非仅判断可达性。替代读取不记作 curl 成功，不伪造 HTTP 200、远端字节 SHA-256 或 TLS 验证结果。

### 3.2 已实际读取的关键文字

下表是本轮新增的独立读取记录，不是复用作者取证结论。网页通道可能返回缓存及经过转换的文字：NGC 页面标示约两个月前抓取，部分规范/排障页亦非当日抓取，不能视为本机实时取得的字节快照。GitHub `fetch_file` 的行号以指定原文件坐标为准；返回的 blob SHA 是 Git 对象身份，**不是文件 SHA-256**。本轮未核验签名、发布包或完整整栈配套。

| 一次源精确位置 | 通道及核对内容 | 支持边界 |
|---|---|---|
| [image-spec annotations.md@v1.1.1](https://raw.githubusercontent.com/opencontainers/image-spec/v1.1.1/annotations.md)，Rules / Pre-Defined Annotation Keys | 网页原文：注解属性可选；键值类型、唯一性等规则包含 MUST；`source`/`revision`/`base.digest` 有各自语义，部分基础镜像建议使用 SHOULD | 不支持“这些 annotations 一律 SHOULD 级”，不证明强制 provenance |
| [image-spec config.md@v1.1.1](https://raw.githubusercontent.com/opencontainers/image-spec/v1.1.1/config.md)，Layer DiffID / Properties | 网页原文：DiffID 是未压缩层 tar 的摘要；可重复打包/解包建议只针对层；`rootfs.diff_ids` 必填，`history` 可选 | 不证明构建输入完备或整体构建可复现 |
| [manifest.md@v1.1.1](https://raw.githubusercontent.com/opencontainers/image-spec/v1.1.1/manifest.md)，config / layers / subject；[descriptor.md@v1.1.1](https://raw.githubusercontent.com/opencontainers/image-spec/v1.1.1/descriptor.md)，Digests / Verification | 网页原文：manifest 引用 config 与有序层；subject 为可选关联；摘要校验识别所指内容字节 | 不替代 SBOM 清点、签名信任核验、拉取策略或兼容证明 |
| [runtime-spec config.md@92249139](https://raw.githubusercontent.com/opencontainers/runtime-spec/92249139eea7161e13745abd4cb6d0ea02a3227a/config.md)，User / POSIX-platform User | 网页原文：进程 `uid`、`gid`、`additionalGids` 等字段 | 通用进程配置，不能仅凭它认定设备访问成功；未独立核验登记中 v1.3.0 tag 与此 commit 的关系 |
| [runtime-spec config-linux.md@92249139](https://github.com/opencontainers/runtime-spec/blob/92249139eea7161e13745abd4cb6d0ea02a3227a/config-linux.md#L127-L151)，Devices L127–151、Allowed Device list L402–417 | raw 网页读取报 Internal Error，改用 GitHub 原文件片段；blob `c71757494ca743fd90692c25e4897bf74cf00388`。分别核对节点 `path/type/major/minor/fileMode/uid/gid` 与访问规则 `allow/type/major/minor/access` | 节点和许可不同；不提供选定 containerd/runc 或厂商路径的运行证据 |
| [Toolkit 1.20.0 install-guide.html](https://docs.nvidia.com/datacenter/cloud-native/container-toolkit/1.20.0/install-guide.html)，Prerequisites / Configuring containerd (for Kubernetes) | 网页正文：宿主驱动前置、包版本 `1.20.0-1`、containerd 配置入口及 drop-in/imports 描述 | 未给出正文声称的 containerd 2.4.1/runc 1.5.2 支持交集 |
| [Toolkit 1.20.0 cdi-support.html](https://docs.nvidia.com/datacenter/cloud-native/container-toolkit/1.20.0/cdi-support.html)，Automatic Generation / Known Limitations / Running a Workload / Non-CDI-Enabled Runtimes | 网页正文：自动生成、MIG 重配/驱动移除刷新限制、hook 冲突；原生 CDI 消费与 NVIDIA runtime 的 CDI 注入路径有区别 | 不能把环境变量存在与否用作所有模式的统一判据；不是 CDI spec 版本身份 |
| [Toolkit 1.20.0 docker-specialized.html](https://docs.nvidia.com/datacenter/cloud-native/container-toolkit/1.20.0/docker-specialized.html)，GPU Enumeration / Driver Capabilities | 网页正文：`NVIDIA_VISIBLE_DEVICES` 控制 GPU 选择；`NVIDIA_DRIVER_CAPABILITIES` 控制挂入的 driver libraries/binaries | 两个变量职责不同；不能推出 CUDA/框架 ordinal 与宿主物理 ID 的对应 |
| [Toolkit 1.20.0 troubleshooting.html](https://docs.nvidia.com/datacenter/cloud-native/container-toolkit/1.20.0/troubleshooting.html)，NVML: Insufficient Permissions and SELinux / Containers losing access / Affected Environments | 网页正文：SELinux 段对应 Insufficient Permissions；Unknown Error 的访问丢失段限定 hook/legacy 注入、容器更新等条件；禁用标签会失去 SELinux 隔离 | 不能按一个错误消息通判权限问题，不能把回退更新视为已证实恢复方法 |
| [NVIDIA plugin README@v0.20.1](https://raw.githubusercontent.com/NVIDIA/k8s-device-plugin/v0.20.1/README.md)，Configuration Option Details / Shared Access to GPUs | 网页原文：设备列表策略、ID 策略与 CDI/CRI 传递条件；time-slicing 的共享计数不提供显存及故障域隔离 | 不构成框架编号映射或各版本支持组合；没有执行 README 中的部署例子 |
| [Ascend plugin README@44385c13](https://github.com/Ascend/mind-cluster/blob/44385c13d7b1d87def35f1604e8be4d16de6ca4e/component/ascend-device-plugin/README.md)，组件介绍；[plugin.go@同 commit](https://github.com/Ascend/mind-cluster/blob/44385c13d7b1d87def35f1604e8be4d16de6ca4e/component/ascend-device-plugin/pkg/server/plugin.go#L1080-L1175)，L1080–1175、L1290–1363 | GitHub 原文件片段；README blob `a8e257ab89f6c2825b0c11fa28acad6b80a4d943`，plugin blob `b7692611b12884854d973fa2a3da18e381353f10`。核对 `DeviceSpec` 的 HostPath/ContainerPath/`rw`、`UseAscendDocker` 分支、调用 `SetAscendRuntimeEnv`，以及 Allocate 到设备配置的调用链 | 支持插件两路径；本轮未继续核对辅助函数或对应 runtime 消费/库挂载实现，不补造其语义 |
| [NVIDIA 框架容器指南](https://docs.nvidia.com/deeplearning/frameworks/user-guide/index.html)，§1.1 / §5.9；[NGC PyTorch 25.01-py3 layers](https://catalog.ngc.nvidia.com/orgs/nvidia/-/containers/pytorch/25.01-py3/layers) | 网页正文：宿主内核、限制 GPU 暴露；NGC 可见 Signed、build id `134983853`、build ref `3857cfd7a27acea1d4e19243329fcd1dae3b222e` 和有限层记录 | 指南为可变页面；NGC 本次为缓存文字，未拉镜像、取得 manifest digest、验签或清点完整成分 |
| [CDI SPEC.md@cb98bcf6](https://github.com/cncf-tags/container-device-interface/blob/cb98bcf66dc68530012483bd56e33e14d815e167/SPEC.md)，Version / Released versions；同 commit README 的 How does CDI work | SPEC raw 网页读取报 Internal Error，改用 GitHub 原文件 L1–130；SPEC blob `2bc480a20ce447f5281b5d6844a486a81bb635b0`。**仓库 v1.1.1 对应 spec 1.1.0**；发布表明确该 patch 没有 Spec 变更。README 区分文件、设备名传递、runtime 消费 | 仓库/API tag 不能直接写成 spec 版本；未核定实际生成文件的 `cdiVersion` 与消费端支持交集 |
| [vLLM Ascend Issue #2557](https://github.com/vllm-project/vllm-ascend/issues/2557)，环境变量 / 错误 / 报告者解释 | 网页正文：物理 ID `0,3,4,7` 写入 `ASCEND_RT_VISIBLE_DEVICES`，框架报输入范围 `[0,4)`；结合本地案例 L32–40 确认关联类别与缺失条件 | 是编号映射问题，不是“完全无设备节点”；本轮未复审 PR 的全部代码或原集群结果 |

### 3.3 新写入版本名的 ref 核验

通过 GitHub 只读 `git/ref` 和 annotated tag 对象核对，三个仓库 tag **确实存在**，不将“作者没有交付取证记录”误报为“版本不存在”：

| 仓库 tag | 本轮直接读取的官方对象 | 核对的身份 |
|---|---|---|
| containerd v2.4.1 | [ref](https://api.github.com/repos/containerd/containerd/git/ref/tags/v2.4.1) / [tag 对象](https://api.github.com/repos/containerd/containerd/git/tags/e24870ce498feb6721878a1af2fdd1641b926854) | tag object `e24870ce498feb6721878a1af2fdd1641b926854` → commit `f2551031d7276a770f65f98c9b52e57e7dad07e8` |
| runc v1.5.2 | [ref](https://api.github.com/repos/opencontainers/runc/git/ref/tags/v1.5.2) / [tag 对象](https://api.github.com/repos/opencontainers/runc/git/tags/b622a5992f0ba88fda05f2fd037d151b4fc5cc88) | tag object `b622a5992f0ba88fda05f2fd037d151b4fc5cc88` → commit `29dd3dc2b13b4123162e5fe132504bb4b15569f1` |
| CDI 仓库 v1.1.1 | [ref](https://api.github.com/repos/cncf-tags/container-device-interface/git/ref/tags/v1.1.1) | 直接指向 commit `cb98bcf66dc68530012483bd56e33e14d815e167`；规范版本另见 SPEC.md 的 1.1.0 |

这些身份是**审阅者补充证据**，不等于作者已登记，也不关闭尚未交付的配置/诊断方法。未用 tag 对象中的 verification 字段冒充本库独立验签结果。本轮只写报告，未把补充读取的来源追加到登记表。

## 4. B21-C30–C34 逐项复核

### B21-C30 — P2 / OPEN

**权威关闭条件：** 初审 §6，L97–102。

**修订位置：** 正文 L38–49、L95；作者记录 L9、L17；修订映射 L95；登记 L5204–5214。

| 原关闭条件 | 本轮核对及位置证据 |
|---|---|
| 1. 可填写的构建输入记录方法 | **部分满足。** 正文 L40–43 已拆基础镜像、构建文件/上下文、参数/锁定、工具信息；但仍只给字段名与版本记录泛称，未交代如何保留上下文/锁文件身份及证据位置、如何判别输入固定或缺失。并不要求选定某个构建工具，更不要求实测；可独立于工具交付具体记录格式和判断规则。 |
| 2. 分列 SBOM 与签名，固定规范/工具并给方法和限制 | **未满足。** L47–48 仍明确材料未取、对象/方法/限制 unknown。分成两行纠正了混写，但没有提供本条必交方法。 |
| 3. 固定所选拉取路径与策略依据 | **未满足。** L49 仍是“所选运行时文档（未固定则 unknown）”；没有确定编排/CLI 路径、精确官方页、实际字段与默认/显式策略及缓存判断。 |
| 4. 保留 digest/供应链边界并同步新增依据 | **部分满足。** L34、L40 保留边界；注解/config 在作者表中有链接，但登记注未体现该轮新增核对范围，SBOM/签名和拉取路径仍未交付。 |

**本 ID 下事实精度追记：** L44 把注解整体写成“SHOULD 级”不准确：manifest 的 annotations 是 OPTIONAL，annotations 的 Rules 则包含 MUST；特定基础镜像关系才有相应 SHOULD。L45 的可复现建议应限定到层 tar 打包/解包，不能当成完整构建 provenance。L49“digest 引用才可复现”也须限定为固定所指镜像内容，不能读成仅凭 digest 已建立可复现构建。依据为 §3.2 的 annotations、config、manifest 和 descriptor 原文。

**剩余关闭条件：** 补可填写的输入身份/证据格式与缺项判据；固定并分别交付 SBOM、签名的记录对象、核对方法、信任/完整性边界及未执行状态；选择一个实际拉取路径给出有版本依据的字段/默认值/缓存方法；纠正上述规范级别和可复现范围，并同步作者记录/登记。可以保留目标环境未知，不能以 unknown 替代必交方法。

### B21-C31 — P2 / OPEN

**权威关闭条件：** 初审 §6，L114–118。

**修订位置：** 正文 L18、L29、L53、L61、L95；作者记录 L10、L17；修订映射 L94、L96；登记 L2203–2216、L5204–5247。

| 原关闭条件 | 本轮核对及位置证据 |
|---|---|
| 1. containerd/runc 固定文档或实现、配置模式/字段和诊断依据，登记并引用 | **未满足。** L53 只列版本并声明正文未读；没有对应 URL、commit、配置字段或诊断位置。来源记录 L10 与映射 L94 所称“见登记注”，在本轮完整登记搜索中找不到对应 containerd/runc/CDI ref 记录。本轮独立确认 tag 存在，不把审阅者补充取证算成作者完成交付。 |
| 2. 固定 CDI 规范并分开生成、消费、Kubernetes/CRI 传递 | **部分满足但有事实错误。** L61 已提原生/非原生路径，仍未给 engine/CRI 条件或 spec 正文依据；L53 将仓库 v1.1.1 错写为 CDI 规范 v1.1.1，见下项追记。 |
| 3. OCI 通用/Linux 精确章节，以及有证据的 containerd 分支表述 | **部分满足。** L62 的固定 Linux 页与章节有效；L53 的通用 `config.md` 只是文件名，没有链接到固定版本/章节。v2.4.x 的文字说明仍不能替代配置/诊断文档定位。 |

**本 ID 下新事实错误追记：** 正文 L53 的“CDI 规范 v1.1.1”与上游不符。官方 v1.1.1 ref 指向 `cb98bcf66dc68530012483bd56e33e14d815e167`，该 commit 的 [SPEC.md / Version](https://github.com/cncf-tags/container-device-interface/blob/cb98bcf66dc68530012483bd56e33e14d815e167/SPEC.md#version) 明确规范为 **1.1.0**，Released versions 表说明 v1.1.1 未改变 Spec。应分列仓库/API 发布 tag、spec 版本和实际 CDI 文件 `cdiVersion`，不能用 tag 解引用代替读取规范。该错误属于原 C31 的版本/规范职责边界，**不新增 ID、不改变 P2**。

**剩余关闭条件：** 交付并登记已选 containerd/runc 的固定原文件或版本化文档，列实际配置模式/字段与诊断依据；纠正 CDI 规范身份并说明生成者、消费端、Kubernetes/CRI 各自前提；为 OCI 通用/Linux 字段提供各自精确链接。支持交集仍可 unknown，不要求拼造一组兼容安装组合。

### B21-C32 — P2 / OPEN

**权威关闭条件：** 初审 §6，L130–135。

**修订位置：** 正文 L57–65；作者记录 L11；修订映射 L97。

| 原关闭条件 | 本轮核对及位置证据 |
|---|---|
| 1. 宿主内核驱动、挂入用户态组件、镜像 CUDA/框架库分别交代来源/版本/边界 | **部分满足。** L57 已明确不是搬运内核驱动，L58 提及 driver libraries/binaries；L59 却仍只有目录页 Signed/build 元数据，没有镜像 CUDA/框架库的具体身份/版本记录方法与来源层区分。 |
| 2. 固定 GPU 样板串起分配 ID→注入通道→最终节点/挂载，分别列条件 | **部分满足。** L60 正确排除了插件 ID 策略等于框架映射；但没有选定一个模式，写出分配 ID、具体传递字段/值、生成或返回配置、最终节点/挂载之间的可核对链。列策略名称或三种路径类别不等于完成链条。 |
| 3. 节点/DAC、进程身份、设备访问控制/LSM 的证据分开，固定框架来源及映射方法 | **未完整满足。** L62 只列类别，未提供进程 UID/GID/附加组等记录项以及可见性与访问判断的证据规则；L63 仍依赖分配策略加框架指南 §5.9。该节说明限制 GPU 暴露，不定义框架 ordinal→UUID/物理设备映射，无法据它构成映射方法。映射未知可以保留，但必须说明需要什么框架证据、怎样记录对应关系。 |
| 4. 与 C34 区分机制/记录字段和异常/对照设计 | **已有形式分工，但不能据此关闭。** §2 放机制、§4 放分支；两节缺失的各自交付仍须分别补齐，不以同一概念表同时验收。 |

**来源位置纠偏：** L58 实际引用文件正确，但括号只标 GPU Enumeration；driver libraries/binaries 由该文件 **Driver Capabilities** 节支持，应分别写明 `NVIDIA_VISIBLE_DEVICES` 与 `NVIDIA_DRIVER_CAPABILITIES` 的职责。此处沿用 C32 记录，不新建发现。

**剩余关闭条件：** 在不宣称兼容的前提下固定一个 GPU 注入样板，用具体字段串起分配及最终配置；补宿主/挂入/镜像自带库的身份与版本字段；把节点、进程身份、设备规则、LSM 的证据位置和判断边界分开；提供固定框架来源与 ordinal/设备标识对应记录方法。实际运行结果仍可空缺，不能用暴露数量或插件 ID 策略代替物理映射证据。

### B21-C33 — P2 / OPEN

**权威关闭条件：** 初审 §6，L147–152。

**修订位置：** 正文 L69–73、L95；作者记录 L12、L17；修订映射 L94、L98；新增登记 L5237–5247。

| 原关闭条件 | 本轮核对及位置证据 |
|---|---|
| 1. 分别定位插件分配/配置与对应 runtime 消费、设备/环境/库挂载实现 | **部分满足。** 新增固定 plugin.go 及两路径说明有效；本轮直接读到 `setNPUDeviceMount` 的分支、`rw` DeviceSpec 与 Allocate 调用。但 L69、L95 仍明确辅助函数/runtime 未核对，且没有选定对应 runtime 组件/ref 或消费/库挂载位置，因此独立 Ascend runtime/plugin 样板尚不完整。 |
| 2. 列目标组合字段，给固定支持材料或明确交集未建立 | **满足字段与未知边界部分。** L71 已列产品、OS/内核、驱动/固件、runtime/plugin、CANN/框架、镜像身份，并未宣称支持交集。本项不因没有硬件实测而要求补造配套结果。 |
| 3. 删除无关 ACP 或说明有限用途与正确来源 | **满足。** L73 明确本页不引用 ACP，正文已不把它当设备暴露依据。 |
| 4. 保留 GPU 不套用 NPU、digest 边界并独立核对一次源 | **已满足现有插件范围。** L34、L71 保留边界；本轮独立核对固定插件原文。未取得 runtime 消费端证据的范围不因此获得通过。 |

**精确位置说明：** L1087 起是 `mountDevice`，控制 `UseAscendDocker` 两分支的是原文件 **L1161–1169**；L1168 调用 `common.SetAscendRuntimeEnv`。作者引用能定位相关文件，但应避免把 L1087 直接当成判断 `UseAscendDocker` 的分支起点。

**剩余关闭条件：** 选择明确 Ascend runtime/ref，核对插件辅助函数输出与 runtime 消费、设备节点/环境/库挂载的对应实现；写明分支条件和各阶段具体字段。既有登记中另有 runtime 材料可作为取证候选（L2264–2277），但版本不同，不得直接拼为与本插件兼容的组合。缺少目标配套材料继续 unknown；无需进行真实环境验证，也不能以所有 runtime 行为均 unknown 代替必交实现取证。

### B21-C34 — P1 / OPEN

**权威关闭条件：** 初审 §6，L165–171。

**修订位置：** 正文 L75–90；作者记录 L13、L17；修订映射 L99；关联案例 L32–40、待执行实验的分层记录与判据章节。

| 原关闭条件 | 本轮核对及位置证据 |
|---|---|
| 1. 可填写最小环境清单，含期望/实际/证据和各层字段 | **部分满足。** L77 扩充了清单类别，也要求期望与实际两栏，但没有真正给出记录表/字段模板和证据位置；镜像库信息、具体设备标识、最终配置及访问控制仍停留类别，无法按它完成逐字段核对。 |
| 2. 三类具体异常分支、GPU/NPU 条件分别写及停止/完成判据 | **未满足。** L83–86 虽有表头和四行，但内容基本限于 GPU/Toolkit，未给 NPU 对应分支。所需证据多是“三单核对”“排障页”“影响证据”，没有定位/比对方法；“解释不清即停/同上”只提供泛化停止提醒，无可判断的完成条件与无法判断条件。 |
| 3. 只设计的受控方案及未授权设备负向验证前提 | **部分满足。** L88 保留控制同一镜像/驱动和授权原则，却未展开基线/变体、唯一计划差异、证据采集、集合身份比较、旁路注入排除、结果判定及停止/恢复边界。“换注入模式/换权限配置/关共享/回退更新”不是完整受控方案。 |
| 4. 源案例/官方问题链接，提炼症状、条件、限制及非本库复现属性 | **部分满足。** L88 确有案例/实验链接，不再属于“没有链接”。但仅写“同类设备可见性”与“缺失条件见该页”，未提炼案例其实是物理/逻辑 ID 分叉、不是完全无节点，也未接入相应分支；§4 的 Toolkit 现象未在各分支提供精确问题章节及条件摘要。 |
| 5. 保留未执行、非安装处方、来源建议不授予操作权 | **满足。** L90 明确三项限定；本轮也未执行任何对照或修改安全策略。 |

**本 ID 下语义纠偏追记：** L84 把 `NVML Unknown Error` 与 SELinux 权限段并列，未区分该段实际对应的 `Insufficient Permissions` 与 hook/legacy 访问丢失上下文。L86 的“回退更新”未获所引官方段支持为充分恢复办法；源段描述更新可能撤销 hook 注入的访问，并说明重建容器的恢复路径。此处不是要求执行重建，而是要求设计中勿将撤销更新等同于恢复访问。案例 Issue #2557 的物理/逻辑 ID 分叉也不能直接充当设备节点完全缺失的证据。

**剩余关闭条件：** 交付带“字段/期望/实际/证据定位/缺失解释”的环境模板；分别给 GPU/NPU 注入、访问拒绝、隔离范围分支及可区分的完成/失败/无法判断判据；展开有授权与隔离前提的基线和变体设计，不自动放宽权限、禁用 LSM 或重启生产组件；将案例的实际症状、环境缺项、版本范围和未复现属性简要落在本页，与对应分支相连；修正两个 NVML 情境及恢复边界。这里只要求设计，不要求制造输出或执行硬件实验。

## 5. 四条 acceptance 与计数

| Acceptance / 计划原文件位置 | 复核结果 | 仍阻塞的原 ID |
|---|---|---|
| 1 / L5403：镜像身份、构建输入、SBOM/签名和拉取策略方法/限制 | 部分满足；**未通过** | B21-C30 |
| 2 / L5404：固定版本、host/库/注入/权限/框架映射职责分离 | 部分满足；**未通过** | B21-C31、B21-C32 |
| 3 / L5405：Ascend runtime/plugin 独立实现、目标组合与平台边界 | 插件及未知边界已有进展；runtime 对应取证缺失；**未通过** | B21-C33 |
| 4 / L5406：环境清单、异常分支、对照及源案例关联 | 已有表格和链接，仍未形成完整判定设计；**未通过** | B21-C34 |

**最终发现计数：5 项原发现，0 CLOSED、5 OPEN；没有新增发现 ID。** CDI 规范版本误标在 C31、注解规范级别及可复现范围在 C30、来源章节/分支精度在 C32–C34 下追记；不额外增加发现数量。后续应按新输入 SHA 再定向复核，不能把本报告中的审阅者补充取证当作作者已完成修改。

## 6. 结构校验与写入边界

- 写入报告前：`PYTHONDONTWRITEBYTECODE=1 make check` **PASS：94 content entries / 421 sources**。这确认登记数量和结构/本地文件链接，不确认远程内容、规范版本或技术结论。
- 写入报告后：原仓库 `PYTHONDONTWRITEBYTECODE=1 make check` **PASS：94 content entries / 421 sources**。
- 为遵守“只写这一份报告”，将源文件及既有 `build/` 复制到 `/private/tmp/b21-t05-01-recheck.2XvDlc/validation`，排除 `.git`、`.venv`、`.agents`、`.codex` 和字节码缓存；在副本中以原仓库虚拟环境 Python 执行 `PYTHONDONTWRITEBYTECODE=1 make check` 与 `make build`，两项均 **PASS：94 content entries / 421 sources**，副本重新生成 `build/catalog.json`、`build/catalog.md`。这只是知识库结构/目录构建，不是镜像构建或技术实测。
- 六个主输入在报告写入后再次计算 SHA-256，均与 §2 相同；原仓库全部 `build/` 文件的前后摘要清单相同。最终工作区状态相对进入本轮时仅新增本报告，既有作者改动和未跟踪文件保留不变。
- 不需要 `make test`：本轮不修改 `src/kb/` 或测试代码。报告仅记静态审阅和知识库结构校验，不产生设备实验结果。

**最终结论：定向复核不通过；五项仍 OPEN；curl 成功取文方法未完成，已如实使用允许的只读替代通道；未确认实际执行模型元数据，也未建立任何真实环境验证结论。**
