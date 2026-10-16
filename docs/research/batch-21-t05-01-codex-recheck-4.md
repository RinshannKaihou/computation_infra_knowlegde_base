# Batch 21 补交 T05-01 第四次定向复核（作者第四轮修订后）

## 1. 结论、角色与边界

- 日期：**2026-10-14（Asia/Shanghai）**；本机 `date` 返回同日、`CST +0800`。
- 执行者：本会话 Codex，独立审阅角色；本轮未参与作者修订。仓库内只新增本报告，不改作者正文、来源记录、修订映射、来源登记、计划或既有报告，不提交 Git commit。
- 用户约定配置：`gpt-6.1-sol / xhigh`。**仅记录用户约定，不写成已独立确认的执行元数据。** 本轮未取得可独立核验的实际模型标识或 reasoning 配置，未以模型自述确认，也未另行派发模型。
- 范围：仅 **B21-C30–C34**；优先级沿用初审。剩余关闭条件以[第三次定向复核](batch-21-t05-01-codex-recheck-3.md) L95、L108、L123、L135、L152 为权威，对照[初审](batch-21-t05-01-codex-review.md) §6。作者第四轮映射 L119–126 是修订自述，不代替正文交付和一次源证据。
- **结果：0 CLOSED / 5 OPEN（1 P1、4 P2）；第四次定向复核不通过。四条 acceptance 均未完整通过。** SBOM 范围收敛、OCI 错链修正、LSM 关联设计、common.go 定位、缺证据判据、对照表、案例版本摘要和 NVML 情境纠偏均有进展；下文不再把这些已交付子条件判作全缺失。
- 未执行镜像构建/拉取、SBOM 生成/比对、签名/验签、容器启动、配置修改、设备访问、隔离试验或 GPU/NPU 实测。知识库结构校验和清单构建不是上述实测，不建立软件支持交集或硬件验证结论。

## 2. 输入身份与位置口径

用户给出的五个 SHA-256 前缀全部匹配；另外两个报告及计划也记录完整摘要。下文正文/作者记录/登记行号均指本轮输入原文件，不沿用旧正文坐标。

| 输入 | 完整 SHA-256 |
|---|---|
| [正文](../../knowledge/05-cluster-platform/container-image-runtime-baseline.md) | `759971d35771a4c109a6926cb19ced1fcb165952c26b3bd4aa5ca10e66e25dbe` |
| [作者来源记录](batch-21-t05-01-sources.md) | `e4c3f2e950e84484ee5a65235d1925a8bad36f43bf49d9d1ad497c16cf263fc9` |
| [修订映射](batch-21-review-fixes.md)，第四轮节 L119–126 | `6b62f718d00f80b36a9ad9c8eebcf4980e3ec30a8099671280fa129abc74d6e0` |
| [第三次定向复核](batch-21-t05-01-codex-recheck-3.md) | `8d15a063357ff94a924d9db6927c89778f39e16ee371dcfe5dcb3b5546e36475` |
| [初审](batch-21-t05-01-codex-review.md) | `341775efc62d7b8d46659c2d272aa31ae301b0cd1db47623ebe86490b80e34b5` |
| [任务验收计划](../../plans/full-coverage-backlog.yaml)，T05-01 L5386–5418 | `5f9bcf865b8c77e13cc8ee5f1c03140c37b86f558d8227d8bb2080249f4fcfc3` |
| [来源登记](../../sources/registry.yaml) | `b125009520e1b55b514071b359566484f0d8153962b5b655d468f629185e9702` |

另读 README、编写指南、内容总目录、元数据 schema，以及本页实际链接的[Ascend 来源案例](../../knowledge/05-cluster-platform/ascend-device-visibility-source-case.md)和[待执行实验](../../knowledge/05-cluster-platform/ascend-device-visibility-experiment.md)。关联条目只用于核对本页摘要和链接的支持范围，不扩大为重新验收这些条目。

登记实计 **429 项**，较前次增加 `src.ascend.device-plugin-common-44385c13`（登记 L5325–5335）。正文 `source_refs` L8–24 **尚未加入该项**，L79 只写包文件路径，没有该文件的精确链接。新增登记不自动完成正文引用，也不能证明作者记录中的历史 `curl 200` 是审阅者本轮独立确认的结果。

## 3. 一次源抽查：方法、实读内容与限制

### 3.1 curl 实际执行

对下表十四个精确 URL 执行只读 GET，保持 curl 默认 TLS 校验；响应、诊断和状态只存于 `/private/tmp/b21-t05-01-recheck-4.wQitDEe1/`，未存入仓库。命令形态：

```bash
curl --fail --silent --show-error --location \
  --connect-timeout 10 --max-time 25 \
  --write-out '\nhttp=%{http_code}; effective_url=%{url_effective}; bytes=%{size_download}\n' \
  <精确 URL>
```

未使用 `-k`/`--insecure`，未修改 DNS、代理或 TLS 设置。**十四次均 exit 6 / HTTP 000 / 0 bytes，诊断为无法解析主机名；未进入 TLS 握手，curl 没有取得远端文字。** 这不证明源站不可达或链接失效。

| 实际请求 URL | curl 结果 |
|---|---|
| <https://v1-32.docs.kubernetes.io/docs/concepts/containers/images/> | DNS 失败 |
| <https://raw.githubusercontent.com/anchore/syft/v1.54.1/README.md> | DNS 失败 |
| <https://docs.sigstore.dev/cosign/signing/overview/> | DNS 失败 |
| <https://raw.githubusercontent.com/containerd/containerd/v2.4.1/docs/cri/config.md> | DNS 失败 |
| <https://raw.githubusercontent.com/opencontainers/runc/v1.5.2/man/runc.8.md> | DNS 失败 |
| <https://raw.githubusercontent.com/cncf-tags/container-device-interface/cb98bcf66dc68530012483bd56e33e14d815e167/SPEC.md> | DNS 失败 |
| <https://raw.githubusercontent.com/opencontainers/runtime-spec/v1.3.0/config.md> | DNS 失败 |
| <https://raw.githubusercontent.com/NVIDIA/k8s-device-plugin/v0.20.1/README.md> | DNS 失败 |
| <https://docs.nvidia.com/datacenter/cloud-native/container-toolkit/1.20.0/cdi-support.html> | DNS 失败 |
| <https://docs.nvidia.com/datacenter/cloud-native/container-toolkit/1.20.0/troubleshooting.html> | DNS 失败 |
| <https://raw.githubusercontent.com/Ascend/mind-cluster/44385c13d7b1d87def35f1604e8be4d16de6ca4e/component/ascend-device-plugin/pkg/server/plugin.go> | DNS 失败 |
| <https://raw.githubusercontent.com/Ascend/mind-cluster/44385c13d7b1d87def35f1604e8be4d16de6ca4e/component/ascend-device-plugin/pkg/common/common.go> | DNS 失败 |
| <https://docs.pytorch.org/docs/2.14/notes/cuda.html> | DNS 失败 |
| <https://github.com/vllm-project/vllm-ascend/issues/2557> | DNS 失败 |

### 3.2 允许的只读替代通道与文字核对

随后通过 **Web `open`/`find`** 实读官方页面/版本化文件的关键段落，以及 **GitHub 连接器 `fetch_file`** 按明确 ref 和原文件范围取文，不以搜索摘要或可达性作结论。CDI、Ascend plugin/common 的 raw 与 GitHub HTML 在 Web 通道返回 Cache miss/Internal Error，连接器读取同 commit 成功。一次默认分支代码搜索只用于发现 common.go；下述判断全部回到输入指定 commit，不引用搜索返回的另一 commit 作为固定样板。

替代通道可能返回缓存或抽取文字，不等同于本机 curl 成功，不能由它独立核验本机 TLS 会话、原始响应字节摘要或作者历史取证时间。Web 行号不作 GitHub 原文件锚点；下表源码坐标使用连接器原文件读取范围。Cosign 页面未版本化；本轮不把登记中的“取证时最新 tag”当作已核验的 CLI/文档版本。没有执行上游文档中的安装、生成、配置或恢复命令。

| 一次源与实读位置 | 核对内容及用途 |
|---|---|
| [Kubernetes v1.32 Images](https://v1-32.docs.kubernetes.io/docs/concepts/containers/images/#image-pull-policy)，Image pull policy / Default image pull policy | `Always` 每次启动先向 registry 解析 digest，再决定复用匹配缓存或下载；不是每次重新下载全部内容。省略策略时，digest/非 latest tag 默认 `IfNotPresent`，latest/无 tag 默认 `Always`；对象创建时设置，后改镜像不会自动改策略。用于 C30。 |
| [Syft README@v1.54.1](https://github.com/anchore/syft/blob/v1.54.1/README.md)，Features / The basics | 支持镜像/文件系统等扫描目标、包生态及 CycloneDX/SPDX 等输出。正文已撤回“全部层文件清单”，认可；本轮未审计所有 cataloger/配置，不补写全覆盖能力。用于 C30。 |
| [Cosign signing overview](https://docs.sigstore.dev/cosign/signing/overview/)，签名/透明日志/核验；[Verifying Signatures](https://docs.sigstore.dev/cosign/verifying/verify/)，Keyless verification / Local verifications | 身份核验示例指定预期 certificate identity 和 OIDC issuer；公钥模式指定可信 key；默认核对签名载荷 digest 与镜像。核验页是审阅补证，不算作者已交付该页。用于 C30 的信任输入和对象匹配。 |
| [containerd CRI config@v2.4.1](https://github.com/containerd/containerd/blob/v2.4.1/docs/cri/config.md)，Config versions / Cgroup Driver / Runtime classes / Full configuration | v2.x 示例为 `version = 3`，v2 配置可转换；runtime 与 images 插件分区不同，runtime 分区含 `cdi_spec_dirs`，runc options 有 `SystemdCgroup`。正文列出字段名但未选值/归属和核对方法。用于 C31。 |
| [runc.8.md@v1.5.2](https://github.com/opencontainers/runc/blob/v1.5.2/man/runc.8.md)，DESCRIPTION / COMMANDS / GLOBAL OPTIONS | 确有 bundle 配置、状态/进程/事件入口、debug/log/root 和 systemd cgroup 选项；新增正文列举有效，但未连成诊断记录方法。用于 C31。 |
| [CDI SPEC@cb98bcf6](https://github.com/cncf-tags/container-device-interface/blob/cb98bcf66dc68530012483bd56e33e14d815e167/SPEC.md)，原文件 L1–128 | Version 为 spec 1.1.0，v1.1.1 行说明无 Spec 变更；描述文件读取/设备匹配/OCI 编辑，JSON 有设备名及全局/设备级编辑。blob `2bc480a20ce447f5281b5d6844a486a81bb635b0`。用于 C31/C32。 |
| [OCI runtime config@v1.3.0](https://github.com/opencontainers/runtime-spec/blob/v1.3.0/config.md)，Process Linux / User；[config-linux@92249139](https://github.com/opencontainers/runtime-spec/blob/92249139eea7161e13745abd4cb6d0ea02a3227a/config-linux.md)，原文件 L127–151、L402–417 | 通用入口确为 runtime-spec，含进程身份与 AppArmor/SELinux 字段；Linux 文件分列节点信息与设备访问规则。Linux 文件 blob `c71757494ca743fd90692c25e4897bf74cf00388`。用于 C31 错链纠偏和 C32 权限/LSM 记录。 |
| [NVIDIA 插件 README@v0.20.1](https://github.com/NVIDIA/k8s-device-plugin/blob/v0.20.1/README.md)，DEVICE_LIST_STRATEGY / DEVICE_ID_STRATEGY / Shared Access | `envvar` 经 NVIDIA Runtime；`cdi-cri` 经 CRI `CDIDevices`，要求 Kubernetes 转发及 CDI engine 消费。time-slicing 不建立显存/故障域隔离。用于 C32/C34。 |
| [Toolkit 1.20.0 CDI](https://docs.nvidia.com/datacenter/cloud-native/container-toolkit/1.20.0/cdi-support.html)，Running a Workload with CDI / Using CDI with Non-CDI-Enabled Runtimes | 原生 engine 用 CDI 名称请求；NVIDIA Runtime 的非原生 CDI 模式可解释 `NVIDIA_VISIBLE_DEVICES`。文档另提醒 CDI 与旧 hook 的冲突。不能把变量落位作为所有原生 CDI 链的必经步骤。用于 C32。 |
| [Toolkit 1.20.0 troubleshooting](https://docs.nvidia.com/datacenter/cloud-native/container-toolkit/1.20.0/troubleshooting.html)，NVML permissions / Containers losing access | 权限段为 `Insufficient Permissions`，旧 hook/legacy 访问丢失段为 `Unknown Error`；后者讨论包括 CPU/内存资源调整等容器更新，不能用镜像/驱动双变更等价替代。禁用 label 会放弃 SELinux 隔离。用于 C34。 |
| [PyTorch CUDA notes 2.14](https://docs.pytorch.org/docs/2.14/notes/cuda.html)，Device-agnostic code | `CUDA_VISIBLE_DEVICES` 管理 PyTorch 可用 GPU 范围；所引段落没有交付逐 ordinal→稳定物理 ID 的方法。用于 C32。 |
| [Ascend plugin.go@44385c13](https://github.com/Ascend/mind-cluster/blob/44385c13d7b1d87def35f1604e8be4d16de6ca4e/component/ascend-device-plugin/pkg/server/plugin.go)，原文件 L1087–1174、L1290–1380 | L1087 起为挂载辅助函数，返回 HostPath/ContainerPath/Permissions；分支实际位于 L1161–1169，Allocate 经最终 ID 处理后调用挂载/环境设置。blob `b7692611b12884854d973fa2a3da18e381353f10`。用于 C33。 |
| [Ascend common.go@44385c13](https://github.com/Ascend/mind-cluster/blob/44385c13d7b1d87def35f1604e8be4d16de6ca4e/component/ascend-device-plugin/pkg/common/common.go)，原文件 L94–123 | `SetAscendRuntimeEnv` 写入返回对象 Envs：ID 逗号串和 runtime options；allow-link 限 310B；worker 组限 `!PresetVDevice`。这是静态实现，不是实测输出或 runtime 已消费证明。blob `6cd038e9f1d67a8a913aa4bb1301692f177b3dbe`。用于 C33。 |
| [vLLM Ascend Issue #2557](https://github.com/vllm-project/vllm-ascend/issues/2557)，环境/Pod 请求/错误段 | 四个 NPU 的物理编号为 0/3/4/7，选择输入触发 `[0,4)` 范围错误；torch 2.5.1、torch_npu 2.5.1.post1、vLLM 0.9.1、Ascend dev `f6a0e1629`、CANN 8.2.RC1。只支持逻辑选择/编号分叉候选，不是 DAC/LSM 拒绝或本库复现的直接证明。用于 C34。 |

## 4. B21-C30–C34 逐项复核

### B21-C30 — P2 / OPEN

**权威条件：** 第三次复核 L95。**本轮位置：** 正文 L26、L37、L48–57、L129；作者记录 L9、L17、L23–25；第四轮映射 L121–122；登记 L5292–5313。

| 子条件 | 判断与位置证据 |
|---|---|
| 构建输入身份与证据定位 | **部分满足，未关闭。** L49–51 保留修订、参数、锁文件哈希和工具/版本；上下文仍只写路径/版本，没有内容固定办法，证据格仍是“本库记录格式/同上”，没有输入与留存证据对象身份/定位的对应格式。未选择特定构建工具本身不是阻塞。 |
| SBOM 范围与比较 | **范围纠偏和共同漏检边界已满足；记录方法仍未满足。** L55 不再称全部层文件，且明确一致不排除共同漏检。但“比对对象、差异处理……须写明”仍是要求读者补写，不是本页的方法；没有扫描对象身份/配置范围、输出身份、所比字段与差异处置的填写格式。 |
| 签名固定依据与信任输入 | **未满足。** L56 仍只有未版本化 overview 和命令名，未在正文固定 CLI/文档修订，缺预期 signer/issuer 或可信 key、对象 digest 匹配及结果证据格式。“验签通过只证发布身份”缺预期身份/信任前提，不能无条件推出预期发布者。登记 L5308 提及 tag 不替代正文方法。 |
| 默认化、缓存与事实记录 | **部分进展，未满足。** L57 已补创建时设置/不随镜像自动改变，以及 digest 解析后复用缓存；但默认值只称“不同”，未写两组具体策略值，仍称“kubelet 默认化”，并以“Always：总拉取”与缓存说明形成歧义。未补缓存命中/实际下载事实的记录字段。依据见 §3.2 Images。 |
| 既有纠偏与状态同步 | **规范纠偏保持；同步未满足。** L52–54 保持 annotations 分级、diff_ids/history 及 provenance 边界，作者记录 L9/L17 已纠正旧状态。正文 L26/L37/L129 却仍称 SBOM/签名官方工具未取，与 L22–23/L55–56、作者记录 L25 及登记冲突。 |

**原 ID 下事实追记：** L57 的“Always：总拉取”不能当作无条件重新下载语义；默认化与 kubelet 拉取决策仍未分开。均归 C30 的拉取方法/限制，不新增 ID。

**剩余关闭条件：** 给出上下文内容身份及输入—留存证据定位格式；将 SBOM 的“须写明”落实为生成/比较记录（对象、配置范围、输出身份、比对字段、差异处理），保留共同漏检限定；固定签名依据并填写预期信任输入、对象匹配、核验结果证据；明确省略策略时的具体默认值与缓存/下载记录，改正 Always 和默认化措辞；同步正文 summary、verification notes、待确认项。继续允许实际值 unknown，**不要求运行供应链工具**。

### B21-C31 — P2 / OPEN

**权威条件：** 第三次复核 L108。**本轮位置：** 正文 L26、L37、L61、L68–71、L129；作者记录 L10、L26–28；第四轮映射 L123；登记 L5248–5269、L5314–5324。

| 子条件 | 判断与位置证据 |
|---|---|
| containerd 配置模式与诊断 | **未关闭。** L61 新增“配置/状态/日志诊断方法未取源”，仍只列文档含字段，没有选定配置版本值、插件分区归属、生效条件及如何用配置/状态/日志核对。所引文件已有 v3 与 v2 转换/分区依据；unknown 不能替代方法交付。 |
| runc 固定入口与诊断 | **入口和字段列举已满足；方法仍未满足。** L24/L61 和登记保留固定手册，新增 bundle、状态/进程/事件及日志选项有效；还没有配置、容器身份/状态和日志的对应记录与判断边界。不是要求逐项审计全部驱动实现。 |
| CDI 三层身份与路径条件 | **部分满足。** L61 的仓库 tag/spec/文件版本区分正确；L70 新写 `cdi-cri`/`CDIDevices`/CRI 转发与消费支持，认可该前提进展。但 L26 仍将 1.1.1 作基线，L71 仍写“CDI 规范 v1.1.1（未读）”；生成、传递和消费链的字段连接仍由 C32 验收。 |
| OCI 精确入口与取证状态 | **错链子条件已满足。** L61 已真正改成 runtime-spec `config.md@v1.3.0`，Linux 入口保持固定文件；不再判错链缺失。L37/L129 的 containerd/runc/CDI 正文未读状态却仍与 L61 和作者增补/登记不一致；需区分已读段落与未覆盖的诊断/消费细节。 |

**剩余关闭条件：** 落下所选 containerd 配置版本/分区/字段及核对方法，补 runc 配置—状态—日志对应记录；清除 CDI 1.1.1 规范误标和未读残留，同步实际取证范围；保持已修正 OCI 链接和所选 CRI 转发前提。支持交集仍可 unknown；已交付的固定手册和 OCI 正确入口不再要求重补。

### B21-C32 — P2 / OPEN

**权威条件：** 第三次复核 L123。**本轮位置：** 正文 L65–75、L93–98；作者记录 L11/L24；第四轮映射 L124。

| 子条件 | 判断与位置证据 |
|---|---|
| 三层库身份、版本与证据 | **部分满足。** L65–66 继续分开宿主内核和用户态挂入组件；L67/L98 新列镜像 CUDA/框架库名称、版本、路径、来源层。但“层记录＋diff_ids＋annotations”未交代如何取得/关联库成分，注入驱动组件也没有相同的身份/版本/路径/来源与证据格式，尚不能比较三层来源。 |
| 一个 GPU 模式的字段级链 | **部分进展，仍未满足。** L70 已把 envvar/volume-mounts 排除并补 cdi-cri 前提；却仍把“容器内 NVIDIA_VISIBLE_DEVICES……落位”串作原生 CDI 必经步骤。官方区分原生 engine 与 NVIDIA Runtime 非原生 CDI 模式，变量存在/缺失都不能独立判这条链成功/失败。仍未把实际 Allocate ID、qualified CDI name、传递字段、设备匹配项/全局和设备级 edits 与最终 OCI 节点/挂载逐一对应；“每段须记录”不替代字段级方法。 |
| 节点/DAC、访问规则、进程及 LSM | **本轮所需关联设计已补。** L72 有节点字段、访问规则、UID/GID/附加组、AppArmor/SELinux、拒绝事件和进程/设备/时间关联，并区分未见拒绝与已允许；§3.2 固定 OCI 字段支持配置侧身份。尚无事件输出/现场证据不作为本轮要求实测的理由。 |
| 框架 ordinal→稳定设备映射 | **未满足。** L73 新写三方比对及不比较编号文本的限定，认可；但稳定物理标识方法明写未取源，PyTorch 引用仍只支持可见范围。L98 仍没有逐 ordinal、稳定 ID、分配 ID、CDI/最终配置及证据定位的可填写对应格式。NPU 映射 unknown 的边界可以保留，不能靠 unknown 宣告三单一致。 |

**原 ID 下事实追记：** L70 仍保留原生 CDI→选择环境变量的模式混接；并非认定该变量在所有 CDI 场景都无效。归 C32，沿用优先级，不新增 ID。

**剩余关闭条件：** 完成选定 cdi-cri 原生链的具体字段对应，移出非原生选择变量及其前提；补三层库身份/版本和留存证据格式；在固定框架/设备身份依据下给逐 ordinal→稳定标识→分配/注入的核对表。保留已补 LSM 关联和 unknown 限定；不要求本次执行，具体异常/负向验证仍归 C34。

### B21-C33 — P2 / OPEN

**权威条件：** 第三次复核 L135。**本轮位置：** 正文 L8–24、L79–83、L128–129；作者记录 L12/L17；第四轮映射 L121/L125；登记 L5237–5247、L5325–5335。

| 子条件 | 判断与位置证据 |
|---|---|
| common.go 的固定实现 | **定位和部分输出描述已补。** L79 已指出 `pkg/common/common.go`，登记新增同 commit 文件；§3.2 独立读取确认 ID 串/runtime options 与条件输出。尚未加入正文 source_refs/精确引用，也未说明 worker 组的 `!PresetVDevice` 前提。本轮只读该辅助函数及 plugin 路径，没有替作者定位全部常量或 runtime。 |
| Ascend runtime 消费端及两端字段连接 | **未满足。** L79 仍明确未选 runtime 组件/ref，设备/环境/库挂载消费和白名单 unknown。增加插件辅助函数不能替代消费实现；返回 Envs 不证明 runtime 已读它或已经挂载库。 |
| 分支位置与返回字段 | **仍未满足。** 作者记录 L12 已正确区分 L1087 挂载函数和 L1161–1169 分支；正文 L79 仍用 L1087–1100 表示假分支，未落正确判断坐标，也未展开 HostPath/ContainerPath/Permissions 与后续消费的对应。Allocate 入口补入有效，但完整链接仍未交付。 |
| 目标组合与 GPU/NPU 边界 | **保持满足。** L42/L81 保留目标产品/OS/内核/驱动固件/runtime/plugin/CANN/框架/镜像字段和未建立支持交集；不从 GPU/CDI 推导 NPU、不用 digest 证明兼容，L83 不重新引入 ACP。缺真实组合或实测本身不新增阻塞。 |

**原 ID 下事实追记：** L79 的“其实测输出字段”只有静态源码/登记支持，与本页未执行限定冲突，应称实现输出字段；worker 环境组是条件路径，不能省略 `!PresetVDevice`。均归 C33 的实现取证/边界，不认定已有运行结果，不新增 ID。

**剩余关闭条件：** 固定并引用明确 Ascend runtime/ref，取得设备、环境及库挂载消费实现，按具体返回字段连接插件/辅助函数与消费端；修正正文分支坐标，补 common.go 精确引用/source_refs、条件输出及静态取证措辞。可继续说明整栈支持交集未建立，不能把不同版本拼成兼容组合；**要求实现取证，不要求现场试运行**。

### B21-C34 — P1 / OPEN

**权威条件：** 第三次复核 L152。**本轮位置：** 正文 L87–124；作者记录 L13；第四轮映射 L126；关联来源案例 L19–25/L32–40，关联实验的设计/旁路/判据章节。

| 子条件 | 判断与位置证据 |
|---|---|
| 五栏环境实表 | **实表保持，字段完整性未满足。** L89–98 有八行，L98 新列镜像库身份，认可；宿主硬件/产品形态仍未落行，注入库身份仍缺，L95 的资源数量例子不是实际 Allocate ID。L96/L98 仍缺最终配置/稳定物理映射的具体留存对应格式，需与 C32 方法相接。 |
| 缺证据判据与集合比较 | **缺证据纠偏已满足；比较规则仍未满足。** L104/L108 已改“任一单缺证据→无法判定”，L109/L110 也有缺证据限定，不再重复旧“缺证据即失败”发现。但三单的对象范围、控制节点与分配设备区别、稳定身份归一化未定义；“三单齐/一致”不是已证明同设备的充分条件。 |
| NPU 逻辑选择与权限分支 | **旧混类未关闭。** L122 已称逻辑编号/选择分叉，L109 仍名“NPU 访问拒绝”，以不可见/越界为观测，以“持续分叉”作失败。源案例支持参数范围/选择问题，不直接证明 DAC/LSM 拒绝；合法重编号也可数字不同。缺实现语义时不能同时给无条件技术通过/失败规则。 |
| 隔离观测与访问/恢复完成边界 | **未满足。** L106/L110 仍把关共享后影响消失作隔离完成；这仅支持该次对照现象，不证明设备访问、显存、计算份额或故障域隔离。NPU 三单齐也不补足这些维度。L105 的拒绝消除/注入完整及 L107 的注入恢复，还需与同一目标进程的受控访问结果和原边界关联，不能以注入状态代替功能恢复。 |
| 每变体一行的对照计划 | **表格子条件本轮已满足，内容仍不完整。** L114–120 确有基线和四个变体，不再判只有段落。字段仍为“三单字段/快照存档/同上”，没有具体配置键、身份/时间窗/证据对象定位；旁路未排除 privileged、设备 hostPath、人工挂载/显式变量等路径。L122 有单独授权限定，但没有未请求/未授权设备负向组与具体隔离、安全停止及恢复到基线的判据。L120 “仅镜像/驱动版本不同”不能作为 L107 hook/legacy 容器更新分支的单变量回退：两种版本可能同时变化，也未指定原更新字段。 |
| 案例摘要和 NVML 两情境 | **主要纠偏已满足，案例缺项摘要仍不足。** L105 已真正分开 Insufficient Permissions 与 Unknown Error；L122 新列 torch/torch_npu/vLLM/Ascend dev 和非本库复现。仍将缺项与版本范围推给关联页，未在本页列 CANN 版本和 runtime/plugin/驱动固件/digest 等关键缺项。保持 L124 只设计/不授予执行权的限定。 |

**原 ID 下事实追记：** L120 的镜像/驱动变更与所验证的 hook/legacy 更新事件不对应，且没有单变量保证；归 C34 的对照设计/恢复判据。L109 的逻辑选择混类及 L106/L110 的隔离完成过推仍是原未关闭条件。不新增 ID、不提高优先级。

**剩余关闭条件：** 补环境实表的硬件/三层库/分配与最终配置/稳定映射记录；定义三单对象范围并按稳定身份比较，保留缺证据→无法判定；将“节点在、逻辑选择失败”独立于权限拒绝，GPU/NPU 分支各给实现依据或明确不可判定；区分共享影响对照与各隔离维度，给受控访问/恢复的完成边界；细化已交付计划表的唯一配置差异、主体/时间窗/证据、旁路排除、负向验证授权/隔离/停止和回到基线判据，修正更新变体；在本页补案例 CANN/关键缺项摘要。保持已修正 NVML、表格、案例非复现和操作授权限定，**不要求制造输出或执行生产变更**。

## 5. Acceptance 与最终计数

| 计划位置 / acceptance | 本轮判断 | 未关闭原 ID |
|---|---|---|
| L5403 / 镜像身份、构建输入、SBOM/签名、拉取方法与限制 | 部分满足，**未通过**：SBOM 边界进步，输入留存、实际比较方法、签名信任/固定依据、默认缓存和正文状态同步仍缺 | B21-C30 |
| L5404 / 固定 runtime/Toolkit/CDI，分离宿主、库、设备/环境/挂载、权限、框架映射 | 部分满足，**未通过**：OCI 错链与 LSM 关联已补，配置诊断、CDI 残留、模式链、库身份与稳定映射仍未闭环 | B21-C31、B21-C32 |
| L5405 / Ascend runtime/plugin 独立取证、目标组合与 GPU/NPU 边界 | 部分满足，**未通过**：common.go 定位有效，runtime 消费实现及两端连接仍缺，正文分支位置/引用未同步 | B21-C33 |
| L5406 / 清单、异常/隔离分支、对照验证及源案例，不作安装处方 | 部分满足，**未通过**：缺证据/NVML/对照表/案例版本进步，映射判据、选择混类、隔离边界和具体安全对照仍缺 | B21-C34 |

**5 个原发现：0 CLOSED / 5 OPEN（1 P1、4 P2）；4 条 acceptance：0 完整通过 / 4 未完整通过。无新增发现 ID，无优先级调整。** 结论依据正文交付与一次源文字，不因 curl 沙箱失败本身判技术不通过，也不以审阅者补证、结构 PASS 或作者 unknown 代替必交方法。修订后应按新输入摘要再次定向复核；历史角色/模型记录不追改。

## 6. 结构校验与单文件写入边界

- 写入前原仓库 `PYTHONDONTWRITEBYTECODE=1 make check`：**PASS：94 content entries / 429 sources**。仅结构与本地文件链接，不验证远程链接、技术正确性或支持交集。
- 写入后原仓库 `PYTHONDONTWRITEBYTECODE=1 make check`：**PASS：94 content entries / 429 sources**；报告的本地链接、行尾空白、七个输入摘要和五项发现状态专项检查均 PASS。
- 为遵守单文件约束，将仓库复制至 `/private/tmp/b21-t05-01-recheck-4.wQitDEe1/validation/`，排除 `.git`、`.venv`、`.agents`、`.codex` 和字节码缓存；副本使用原仓库虚拟环境 Python，禁写字节码执行 `make check`、`make build`，均 **PASS：94 content entries / 429 sources**。只在副本重建 `build/catalog.json`、`build/catalog.md`，没有镜像构建。
- 前后摘要核对：**375 个既有 Git 所列 tracked/untracked 非忽略文件及原仓库 build 文件均不变**，包括七个主输入；工作区相对本轮开始只新增本报告，已有作者改动和未跟踪文件保留。临时 curl 诊断/摘要清单不属于正式知识库证据包。
- 未修改 `src/kb/` 或测试代码，不需要 `make test`，不为内容复核报告新增测试。结构 PASS 不改变 §4–5 的技术不通过结论。

**最终技术结论：第四次定向复核不通过，C30–C34 全部保持 OPEN；已披露 curl DNS 失败和允许只读替代通道的限制，未确认实际执行模型元数据，未执行实测。**
