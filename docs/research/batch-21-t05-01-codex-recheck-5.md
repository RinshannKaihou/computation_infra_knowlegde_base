# Batch 21 补交 T05-01 第五次定向复核（作者第五轮修订后）

## 1. 结论、角色与边界

- 日期：**2026-10-14（Asia/Shanghai）**；本机 `date` 返回同日、`CST`。
- 执行者：本会话 Codex，独立审阅角色，与作者第五轮修订角色分开；本轮不承担作者修订，只新增本报告，不改正文、作者记录、修订映射、登记、计划或历史报告，不提交 Git commit。
- 用户约定配置：`gpt-6.1-sol / xhigh`。**这是用户约定，不是已独立确认的执行元数据。** 本轮没有取得可独立核验的实际模型标识或 reasoning 配置，不用模型自述充当确认，未另行派发模型。
- 范围：仅 **B21-C30–C34**，优先级沿用初审。剩余关闭条件以[第四次定向复核](batch-21-t05-01-codex-recheck-4.md) L101、L114、L129、L144、L161 为权威，同时对照[初审](batch-21-t05-01-codex-review.md) §6 和[任务验收](../../plans/full-coverage-backlog.yaml) L5403–5406。第五轮映射 L128–134 只用于查找落盘改动，不代替交付证据。
- **结果：0 CLOSED / 5 OPEN（1 P1、4 P2）；第五次定向复核不通过。4 条 acceptance 均未完整通过。** 本轮认可上下文内容身份、SBOM 比较字段、签名信任输入、拉取具体默认值、配置版本头、原生 CDI 选择变量纠偏、ordinal 空表、Ascend 分支坐标/common.go 引用与条件、宿主硬件行等已补内容，不把这些子条件重新判作全缺失。
- 未执行镜像构建/拉取、SBOM 生成/比对、签名/验签、容器启动、设备访问、配置修改、隔离试验或 GPU/NPU 实测。知识库 `make check` / `make build` 是结构校验与清单生成，不是上述实测，也不建立软件支持交集或硬件验证结论。

## 2. 输入身份与位置口径

用户给出的五个 SHA-256 前缀全部匹配；前次报告、初审和计划另记录完整摘要。下文正文、记录、映射和登记的行号均为本轮输入原文件坐标；不把阅读器的显示行号直接当作 GitHub 原文件锚点。

| 输入 | 完整 SHA-256 |
|---|---|
| [正文](../../knowledge/05-cluster-platform/container-image-runtime-baseline.md) | `8c685d52ff8a23d830468012cf5923b985da3e53475767265559915704f3d417` |
| [作者来源记录](batch-21-t05-01-sources.md) | `b5d6f05044058a4598d33c1ea8455b51bed1afea327f1583fb6580ef19afa120` |
| [修订映射](batch-21-review-fixes.md)，第五轮节 L128–134 | `23e396bbc2935c05d4b28e13dc952c79d9bcf08e40f144d9e723794f08ebfc5a` |
| [第四次定向复核](batch-21-t05-01-codex-recheck-4.md) | `6afdc1db1ade9c645d7f81692ccbec5ef2a86181d711b746cf10923ffc6c3a4c` |
| [初审](batch-21-t05-01-codex-review.md) | `341775efc62d7b8d46659c2d272aa31ae301b0cd1db47623ebe86490b80e34b5` |
| [任务验收计划](../../plans/full-coverage-backlog.yaml)，T05-01 L5386–5418 | `5f9bcf865b8c77e13cc8ee5f1c03140c37b86f558d8227d8bb2080249f4fcfc3` |
| [来源登记](../../sources/registry.yaml) | `b125009520e1b55b514071b359566484f0d8153962b5b655d468f629185e9702` |

另读 README、编写指南、内容总目录、元数据 schema，以及本页实际链接的[Ascend 来源案例](../../knowledge/05-cluster-platform/ascend-device-visibility-source-case.md)和[待执行实验](../../knowledge/05-cluster-platform/ascend-device-visibility-experiment.md)。关联条目仅用于核对本页摘要和判据的支持范围，不扩大为重新验收这些条目。

登记实计 **429 项**。正文 L17 已加入 `src.ascend.device-plugin-common-44385c13`，L86 已给同 commit 精确文件链接；前次这两项缺失已补。登记或作者记录中历史 `curl 200` 不算审阅者本轮独立确认的结果。

## 3. 一次源抽查：实际执行、文字核对与限制

### 3.1 curl 执行记录

对下表十七个 URL 实际执行只读 GET，保持 curl 默认 TLS 校验。诊断、状态和输入摘要清单仅存于 `/private/tmp/b21-t05-01-recheck-5.2S8s8Fve/`，不作为仓库证据附件。命令形态如下，`--output` 指向该临时目录中的单次响应文件：

```bash
curl --fail --silent --show-error --location \
  --connect-timeout 10 --max-time 25 \
  --output <临时响应文件> \
  --write-out 'http=%{http_code}; effective_url=%{url_effective}; bytes=%{size_download}\n' \
  <精确 URL>
```

**十七次均 exit 6 / HTTP 000 / 0 bytes，诊断为无法解析主机名。** 未使用 `-k` / `--insecure`，未改 DNS、代理或 TLS 设置；未进入 TLS 握手，curl 没有获得远端文字。这个结果不证明源站不可达或链接失效。

### 3.2 允许的只读替代通道与实读内容

随后通过 `web.run` 打开精确官方页面/固定 ref 原文件，并定位下列正文；GitHub 只读连接器按明确 tag/commit 读取原文件区间，返回 blob SHA。Issue 另读官方仓库 API 的正文；API 长响应显示有截断，相关环境与错误又由网页正文定向核对，不以截断部分推断缺项。**这是远端文字抽查，不只是可达性判断，也不冒充 curl 成功。** 网页通道可能提供缓存/正文提取，本轮未独立审计该通道的 TLS 链、完整 HTTP 字节或刷新时刻；非版本化 Cosign 页面不能因本轮打开而视为已固定文档修订。

| 序号 / 实际 curl URL（均 DNS 失败） | 替代通道核对位置与文字要点 |
|---|---|
| 01 / [Kubernetes Images v1.32](https://v1-32.docs.kubernetes.io/docs/concepts/containers/images/) | `web.run`：Image pull policy / Default image pull policy。Always 先解析 digest，可复用缓存；省略策略时 digest/非 latest tag 为 IfNotPresent，latest/无 tag 为 Always；新对象提交 API server 时设置，后改镜像不自动更新策略。用于 C30。 |
| 02 / [Syft README@v1.54.1](https://raw.githubusercontent.com/anchore/syft/v1.54.1/README.md) | `web.run`：Features / The basics。镜像/目录包成分扫描及 CycloneDX/SPDX 等输出；不把该 README 当作所有 cataloger/配置的完整性证明。用于 C30。 |
| 03 / [Cosign signing overview](https://docs.sigstore.dev/cosign/signing/overview/) | `web.run`：Root of Trust / signing, witnessing, verifying。身份、证书和透明日志的关系；页面未提供本次已选定的 CLI/文档固定修订。用于 C30。 |
| 04 / [Cosign verifying](https://docs.sigstore.dev/cosign/verifying/verify/) | `web.run`：Keyless verification / Local verifications。核验需预期 certificate identity/OIDC issuer 或可信公钥；默认核对签名载荷 digest 与镜像。作者正文 L57 本轮已引用该页，不再判缺核验入口。用于 C30。 |
| 05 / [containerd CRI config@v2.4.1](https://raw.githubusercontent.com/containerd/containerd/v2.4.1/docs/cri/config.md) | GitHub 文件读取 L1–180，网页再定位 Full configuration。v3 版本头、v2 转换、runtime/images 插件分区；runtime 分区的 `cdi_spec_dirs` 与 runc options 的 `SystemdCgroup`；配置选择还涉及 runtime class/kubelet 条件。用于 C31。 |
| 06 / [runc.8.md@v1.5.2](https://raw.githubusercontent.com/opencontainers/runc/v1.5.2/man/runc.8.md) | GitHub 原文件：DESCRIPTION / COMMANDS / GLOBAL OPTIONS。bundle 内 `config.json` 与 rootfs、容器 ID、状态/进程/事件、日志目标/格式和状态 root；这些入口可关联记录，不能仅凭箭头推定某次容器配置已生效。用于 C31。 |
| 07 / [CDI SPEC@cb98bcf6](https://raw.githubusercontent.com/cncf-tags/container-device-interface/cb98bcf66dc68530012483bd56e33e14d815e167/SPEC.md) | GitHub 原文件 L1–150：规范自述 1.1.0，v1.1.1 行为无 Spec 变更；设备匹配后编辑 OCI，分别有全局/设备级 `containerEdits`。用于 C31/C32。 |
| 08 / [OCI config@v1.3.0](https://raw.githubusercontent.com/opencontainers/runtime-spec/v1.3.0/config.md) | `web.run`：Linux Process / POSIX-platform User。AppArmor、SELinux、UID/GID/附加组字段；本轮保持正文正确的 runtime-spec 通用入口。用于 C31/C32。 |
| 09 / [OCI config-linux@92249139](https://raw.githubusercontent.com/opencontainers/runtime-spec/92249139eea7161e13745abd4cb6d0ea02a3227a/config-linux.md) | GitHub 原文件 L127–151、L402–417：节点路径/类型/设备号/属主/模式与 allowed-device 规则分开，规则有 allow/type/major/minor/access。用于 C32。 |
| 10 / [NVIDIA plugin README@v0.20.1](https://raw.githubusercontent.com/NVIDIA/k8s-device-plugin/v0.20.1/README.md) | `web.run`：DEVICE_LIST_STRATEGY / DEVICE_ID_STRATEGY / Shared Access。cdi-cri 经 CRI `CDIDevices`，需 Kubernetes 转发与 CDI engine；UUID/index 是分配传递策略；time-slicing 不隔离显存/故障域，不能用关共享后影响消失证明这些隔离。用于 C32/C34。 |
| 11 / [Toolkit 1.20.0 CDI](https://docs.nvidia.com/datacenter/cloud-native/container-toolkit/1.20.0/cdi-support.html) | `web.run`：Generating / Running a Workload / Non-CDI-Enabled Runtimes。原生 engine 按 CDI 名请求；非原生 NVIDIA Runtime CDI 模式可使用选择变量。刷新限制和旧 hook 冲突须按路径解释。用于 C32。 |
| 12 / [Toolkit 1.20.0 troubleshooting](https://docs.nvidia.com/datacenter/cloud-native/container-toolkit/1.20.0/troubleshooting.html) | `web.run`：NVML permissions / Containers losing access。Insufficient Permissions 与 hook/legacy 的 Unknown Error 是不同情境；更新可包括 CPU/内存限制，systemd 相关更新另有条件；禁用 label 放弃 SELinux 隔离。用于 C34。 |
| 13 / [Toolkit 1.20.0 docker-specialized](https://docs.nvidia.com/datacenter/cloud-native/container-toolkit/1.20.0/docker-specialized.html) | `web.run`：GPU Enumeration / Driver Capabilities。GPU 选择与挂入的 driver libraries/binaries 分开；变量语义不代替实际库文件身份/版本/来源记录。用于 C32。 |
| 14 / [PyTorch CUDA notes 2.14](https://docs.pytorch.org/docs/2.14/notes/cuda.html) | `web.run`：Device-agnostic code。所引段落支持 `CUDA_VISIBLE_DEVICES` 管理可用 GPU 范围，不交付本页需要的逐 ordinal→UUID 取证方法。用于 C32。 |
| 15 / [Ascend plugin.go@44385c13](https://raw.githubusercontent.com/Ascend/mind-cluster/44385c13d7b1d87def35f1604e8be4d16de6ca4e/component/ascend-device-plugin/pkg/server/plugin.go) | GitHub 原文件 L1087–1174、L1290–1385。L1161–1169 是 UseAscendDocker 分支；挂载路径返回 HostPath/ContainerPath/Permissions；Allocate 经最终 ID 处理调用挂载/环境设置。定位支持插件输出，不证明 runtime 已消费。用于 C33。 |
| 16 / [Ascend common.go@44385c13](https://raw.githubusercontent.com/Ascend/mind-cluster/44385c13d7b1d87def35f1604e8be4d16de6ca4e/component/ascend-device-plugin/pkg/common/common.go) | GitHub 原文件 L93–145。SetAscendRuntimeEnv 写 ID 串与 runtime options；310B 条件写 allow-link；worker 组限 `!PresetVDevice`。这是静态实现文字，不是运行输出或库挂载消费证据。用于 C33。 |
| 17 / [vLLM Ascend Issue #2557](https://github.com/vllm-project/vllm-ascend/issues/2557) | GitHub API 与网页：Your current environment / Describe the bug。设备节点/物理 ID 已在容器；选择变量含 0,3,4,7，日志报参数范围 [0,4)，环境列 CANN 8.2.RC1。该症状支持调查逻辑选择分叉，不直接证明 DAC/LSM 拒绝，不当作通用 NPU 映射规范。用于 C34。 |

GitHub 文件读取返回的完整 blob SHA：containerd config `3a206263f4f9e76b6ca14110461b8661a03b1619`；runc 手册 `7e93a401f202f5746b7c27e81880166436c306ae`；CDI SPEC `2bc480a20ce447f5281b5d6844a486a81bb635b0`；OCI Linux config `c71757494ca743fd90692c25e4897bf74cf00388`；Ascend plugin `b7692611b12884854d973fa2a3da18e381353f10`、common `6cd038e9f1d67a8a913aa4bb1301692f177b3dbe`。它们是文件 blob 身份，不是仓库 commit，也不证明支持交集。正文的 OCI image-spec 既有规范纠偏未扩大为本轮全面重审。

## 4. B21-C30–C34 逐项复核

### B21-C30 — P2 / OPEN

**权威条件：** 第四次复核 L101。**本轮位置：** 正文 L27、L38、L49–58、L137；作者记录 L9、L17、L23–25；第五轮映射 L130；登记 L5292–5313。

| 子条件 | 本轮判断与位置证据 |
|---|---|
| 上下文内容身份与构建记录 | **本轮要求的格式已补。** L50 新增目录树哈希/清单和构建记录文件路径，L51–52 保留参数键值、锁文件哈希、工具名/版本；真实值可 unknown，不要求执行构建，不再以未选工具阻塞。 |
| SBOM 对象、字段与差异处理 | **本轮要求的方法字段已补。** L56 记录扫描 digest/配置范围/输出身份，明确包名/版本/来源层比较及配置差异、新增成分、版本漂移处置；保留重复一致不排除共同漏检与未执行限定。抽查 02 只支持已读工具范围，不要求假造扫描结果。 |
| 签名信任、对象匹配与结果 | **主要方法子条件已补，固定依据仍未满足。** L57 已有 identity/issuer 或可信 key、载荷 digest 和通过/失败＋身份，且增加核验页，抽查 04 支持这些字段。但同一行明确 CLI 修订未固定，两页均非版本化；登记 L5308 的历史最新 tag 描述不等于本方法已选定并核对该版本。 |
| 拉取默认值、缓存与职责 | **具体策略/缓存记录已补，职责措辞仍未改正。** L58 已正确写默认值、对象创建时设置、Always 非无条件重下，并加缓存命中/下载事实。仍称“kubelet 默认化规则”；抽查 01 将提交新对象时的集群字段默认化与 kubelet 按已设置策略拉取分开，不能合并成 kubelet 默认化。 |
| 取证状态同步 | **部分修正，仍矛盾。** L38 已列 syft/cosign 与 k8s 等已核对入口，作者记录 L25 也保留工具来源；L27 却仍称 SBOM/签名无官方工具取证，L137 又将 SBOM/签名官方工具整体列待确认，与 L23–24/L56–57 相冲突。尚未核对的 CLI 修订不能扩写成全部官方工具未取。 |

**剩余关闭条件：** 固定并引用与签名方法相对应的 CLI/文档修订，保留已补信任输入、对象匹配和结果记录；把集群对象字段默认化与 kubelet 拉取决策分开；同步 summary、notes、待确认项及作者记录中的已读范围/未覆盖范围。保持已补构建/SBOM/缓存格式，实际值和未执行结果仍可 unknown；**不要求运行供应链工具**。

### B21-C31 — P2 / OPEN

**权威条件：** 第四次复核 L114。**本轮位置：** 正文 L27、L38、L62、L71–72、L137；作者记录 L10、L26–28；第五轮映射 L131；登记 L5248–5269、L5314–5324。

| 子条件 | 本轮判断与位置证据 |
|---|---|
| containerd 模式与生效诊断 | **版本头已补，关联记录仍不足。** L62 已选 `version = 3`，指出 runtime/images 分区及 cdi_spec_dirs/SystemdCgroup。仍没有完整分区键、所选参考字段值/条件，以及配置来源与实际运行的 runtime handler/容器状态/日志如何按身份关联；“以所选分区字段值为准核对生效”仍未给核对规则。抽查 05 已有明确分区和条件依据，诊断输出 unknown 本身不是阻塞。 |
| runc 配置—状态—日志对应 | **入口保留，新增箭头仍未落实对应格式。** L62 的 bundle 配置→状态查询→日志采集没有共同容器 ID、bundle/config 身份、状态 root/状态字段、时间窗和日志对象定位，无法判定是否观察同一次运行或配置是否相符；抽查 06 支持这些入口可被分别记录，不支持把泛化箭头当作已交付关联判断。 |
| CDI 三层身份及 OCI 精确入口 | **主体已满足，摘要/待确认残留。** L62/L72 已区分 repo tag v1.1.1、spec 1.1.0 与文件 cdiVersion，L71 保留 CRI 转发/engine 条件；OCI 通用与 Linux 链接正确，不再要求重补。L27 的 CDI 1.1.1 固定点仍未限定为 repo tag，L137 仍把 CDI 规范正文整体列待确认；与 L38/L62 及作者记录 L28 不同步。 |

**剩余关闭条件：** 将已选 v3 模式落成配置分区/字段/参考值或未知实际值的记录格式及生效条件，说明配置—runtime/容器身份—状态—日志如何对应与判定；补 runc 的同一运行实例关联字段，而不是要求现场输出；同步 CDI 身份和实际已读范围，保留正确 OCI 链接和 CRI 条件。**不要求拼出受支持整栈或执行配置变更**。

### B21-C32 — P2 / OPEN

**权威条件：** 第四次复核 L129。**本轮位置：** 正文 L66–80、L103–106；作者记录 L11/L24；第五轮映射 L132。

| 子条件 | 本轮判断与位置证据 |
|---|---|
| 原生 CDI 与选择变量分开 | **模式混接已改正。** L71 明确 envvar/volume-mounts/选择变量不混入原生链，不再把变量存在作为必经证据；CRI 转发和消费支持前提保持。抽查 10–11 支持这个区分，不再重复前次变量混接阻塞。 |
| 具体分配→传递→匹配→OCI 对应 | **仍未完成。** L69/L71 有串行概述和文件顶层字段，但没有实际 Allocate ID 如何形成 qualified CDI name、对应 CRI CDIDevices 项、匹配 devices[].name，以及全局/设备级 edits 与最终 OCI 节点/挂载的逐项对应。每段“须逐段记录”没有提供这些具体连接规则；抽查 07/10 支持必须区分匹配和编辑范围。 |
| 三层库身份/版本/来源证据 | **仍未完成。** L66–68 分层机制保持，L68 有镜像库名称/版本/路径/来源层要求；层记录/diff_ids/annotations 未交代如何获得并关联具体库成分，注入的用户态 driver libraries/binaries 也没有同等身份/版本/宿主来源→容器路径/证据定位格式。L106 将镜像库信息附在框架行，不补足三层证据链。 |
| ordinal 核对表与稳定身份方法 | **表格已交付，取证方法仍缺。** L76–80 已有 ordinal、快照、分配 ID、CDI/传递、物理标识、证据与判定列；不再判空表不存在。但 L74 和表头仍明确稳定标识未取源，抽查 14 的可见范围段不提供 ordinal→UUID 方法，也没有与最终 OCI 注入对象相接的对应规则。三方名词/编号不同待查限定不等于稳定物理对应依据。 |
| 权限与 LSM 关联 | **前次已满足子条件保持。** L73 保留节点/DAC、访问规则、进程身份、AppArmor/SELinux 与事件关联，且无拒绝事件不推定已允许；抽查 08–09 支持配置字段，不把无现场事件结果列为本轮新增阻塞。 |

**剩余关闭条件：** 在已纠偏的 cdi-cri 原生模式下补字段级连接规则/可填写对应记录；补宿主、注入用户态组件和镜像库的成分身份/版本/路径/来源及证据定位方法；在固定框架/设备身份依据下连接 ordinal 表与分配、CDI、最终 OCI 对象，缺映射证据保留 unknown。保持模式、LSM 和不混编号的限定；**不要求执行采集或负向试验**。

### B21-C33 — P2 / OPEN

**权威条件：** 第四次复核 L144。**本轮位置：** 正文 L17、L38、L86–90、L137；作者记录 L12/L17；第五轮映射 L133；登记 L5237–5247、L5325–5335。

| 子条件 | 本轮判断与位置证据 |
|---|---|
| 分支坐标、common.go 引用与条件 | **已补。** L86 改成正确 L1161–1169 分支坐标，区别于 L1087 挂载函数体；新增同 commit common.go 精确链接，L17 纳入 source_refs，并写 worker 组的 !PresetVDevice 条件。抽查 15–16 与上述定位/条件相符。 |
| Ascend runtime 消费实现与字段连接 | **仍未满足。** L86 明确未选 runtime 组件/ref，设备/环境/库挂载消费与白名单 unknown；Allocate 仍只给入口、完整链未审计。插件和辅助函数返回 Envs/DeviceSpec 不能代替对应 runtime 已读取并编辑最终设备/挂载的证据，尚没有两端具体字段连接。 |
| 静态取证措辞 | **残留未修。** L86 前半已写辅助函数输出，后半仍称“其实测输出字段”；本轮输入没有实际执行输出，抽查 16 只有源码。需改为静态实现输出，不能用后文未执行限定抵消该措辞。 |
| 目标组合与平台边界 | **保持满足。** L43/L88 保留产品/OS/内核/驱动固件/runtime/plugin/CANN/框架/镜像字段和支持交集 unknown；GPU 不套用 NPU、digest 不证明兼容及不引入 ACP 的限定保持。 |

**剩余关闭条件：** 固定并引用实际选择的 Ascend runtime/ref，取得设备、环境、库挂载消费实现，并将插件/辅助函数具体返回字段连接到消费端/最终配置；保留本轮正确分支、common 引用和条件，清除“实测输出”残留并同步静态已读范围。支持交集仍可 unknown；**要求实现取证，不要求现场试运行**。

### B21-C34 — P1 / OPEN

**权威条件：** 第四次复核 L161。**本轮位置：** 正文 L94–132；作者记录 L13；第五轮映射 L134；关联案例 L32–40，关联实验的旁路/控制条件/判据章节。

| 子条件 | 本轮判断与位置证据 |
|---|---|
| 环境实表与新增硬件行 | **硬件行已补，完整记录仍不足。** L101 新增机型/卡型号/数量，五栏实表保持。L103 把资源请求数量当 ID 值例子，未给实际 Allocate ID 对应；L104 只有容器内节点/变量采集，L106 只有镜像库附项，缺 C32 所需三层库、最终配置与稳定映射关联记录。 |
| 三单对象与缺证据判据 | **缺证据限定保持满足，集合比较仍未定义。** L112/L116 保留任一单缺证据→无法判定，L117/L118 同样有缺证据限定。仍未定义请求数量与分配设备、默认/控制节点与作业节点、逻辑可见编号各自对象范围和稳定身份归一化；三单齐或文本一致不能替代同一设备对应证据。 |
| NPU 逻辑选择与访问拒绝 | **混类仍在。** L117 仍名“NPU 访问拒绝”，观测不可见/越界、候选映射/未注入，以映射一致/持续分叉判完成/失败；L130 却已称逻辑编号/选择分叉。抽查 17 设备节点已在且报参数范围问题，不直接支持 DAC/LSM 拒绝。语义未取源时不能同时给无条件技术完成/失败。 |
| 隔离维度、访问与恢复完成 | **仍未满足。** L114/L118 继续以关共享后影响消失判隔离完成；该对照只能收敛本次共享影响解释，不证明设备访问、显存、计算份额或故障域隔离。L113 拒绝消除/注入完整、L115 注入集恢复还缺同一目标进程受控访问与原边界恢复判据。抽查 10/12 支持这些区别，不要求本轮做隔离/恢复实测。 |
| 对照计划、安全与单变量 | **已有表格保持，关键内容未改。** L124–128 仍用三单字段/快照/同上，缺具体配置键、运行实例/时间窗和证据对象定位；旁路未覆盖 privileged、设备 hostPath、人工挂载或显式选择变量。L130 有单独授权原则，但未给未请求/未授权设备负向组、隔离、安全停止和回到基线判据。L128 仍以“仅镜像/驱动版本不同”作为回退更新，不对应 L115 的 hook/legacy 更新事件，也未保证唯一变量；抽查 12 包括 CPU/内存等更新条件。 |
| 案例条件摘要与 NVML 分开 | **NVML 和非复现限定保持，案例缺项仍未补。** L113 已分开 Insufficient Permissions/Unknown Error；L130 保留症状、框架版本和非本库复现。仍未在本页摘要 CANN 8.2.RC1 与 runtime/plugin/驱动固件/digest 等关键缺项，继续仅指向关联页；关联案例 L38–40 及抽查 17 已给相应定位。 |

**原 ID 下追记：** 逻辑选择混类、把共享影响对照当隔离完成、用镜像/驱动变更替代原更新条件，以及“实测输出”措辞，均为前次已记录问题的残留，分别归 C34/C33；不新增发现 ID，不调整优先级。本轮未发现必须另立 ID 的事实错误。

**剩余关闭条件：** 保留新增硬件行、五栏实表、缺证据判据、NVML 区分和授权限定；补三层库/实际分配/最终配置/稳定身份记录并定义三单比较范围；把节点已在但逻辑选择失败独立于访问策略拒绝，缺实现语义时判无法确定；将共享影响与各隔离维度分开，补目标进程访问及恢复边界；细化计划表的单一配置差异、主体/时间窗/证据、旁路、负向组/安全停止/恢复到基线，修正回退更新变体；在本页补案例 CANN 与关键缺项摘要。**不要求制造结果或执行生产变更**。

## 5. Acceptance 与最终计数

| 计划位置 / acceptance | 本轮判断 | 未关闭原 ID |
|---|---|---|
| L5403 / 镜像身份、构建输入、SBOM/签名、拉取方法与限制 | 部分满足，**未通过**：输入/SBOM/信任字段与默认值进步；签名固定依据、默认化职责和取证状态同步仍未闭环 | B21-C30 |
| L5404 / 固定 runtime/Toolkit/CDI，分离宿主、库、设备/环境/挂载、权限、框架映射 | 部分满足，**未通过**：v3、CDI 模式、OCI/LSM、ordinal 表已补；诊断身份关联、三层库、字段级链和稳定映射仍不足 | B21-C31、B21-C32 |
| L5405 / Ascend runtime/plugin 独立取证、目标组合与 GPU/NPU 边界 | 部分满足，**未通过**：分支/common 引用与条件已补；runtime 消费实现、两端字段连接和静态措辞仍未闭环 | B21-C33 |
| L5406 / 清单、异常/隔离分支、对照验证及源案例，不作安装处方 | 部分满足，**未通过**：硬件行与既有表格/案例/限定保持；对象比较、分支分类、隔离/访问/恢复及安全单变量对照仍不足 | B21-C34 |

**5 个原发现：0 CLOSED / 5 OPEN（1 P1、4 P2）；4 条 acceptance：0 完整通过 / 4 未完整通过。无新增发现 ID，无优先级调整。** 判断依据本轮正文交付和一次源文字，不因 curl DNS 失败本身判技术不通过，不以审阅补证替代作者必交方法，不以结构 PASS 或保留 unknown 宣告验收通过。修订后须按新的输入摘要继续定向复核；历史模型与角色记录不追改。

## 6. 结构校验与单文件边界

- 写入前原仓库 `PYTHONDONTWRITEBYTECODE=1 make check`：**PASS：94 content entries / 429 sources**；仅结构与本地文件链接，不验证远程内容、技术正确性或支持交集。
- 写入后原仓库 `PYTHONDONTWRITEBYTECODE=1 make check`：**PASS：94 content entries / 429 sources**；报告的五项原 ID/状态、行尾空白和本地链接检查通过。
- 为遵守单文件约束，复制仓库到 `/private/tmp/b21-t05-01-recheck-5.2S8s8Fve/validation/`，排除 `.git`、`.venv`、`.agents`、`.codex` 和缓存；副本使用原仓库虚拟环境 Python、禁写字节码执行 `make check` 和 `make build`，均 **PASS：94 content entries / 429 sources**。只在副本重建 `build/catalog.json`、`build/catalog.md`，没有镜像构建。
- 前后摘要核对：**376 个既有 Git 所列 tracked/untracked 非忽略文件及原仓库 build 文件均不变**，包含七个主输入；工作区相对本轮开始只新增本报告，已有作者改动和未跟踪文件保留。临时诊断/摘要清单不属于正式知识库证据包。
- 未改 `src/kb/` 或测试代码，不需 `make test`，不为内容复核报告新增测试。结构 PASS 不改变 §4–5 的技术不通过结论。

**最终技术结论：第五次定向复核不通过，C30–C34 全部保持 OPEN；已披露 curl DNS 失败和只读替代通道的文字核对/限制，未确认实际执行模型元数据，未执行实测。**
