# Batch 21 补交 T05-01 第六次定向复核（作者第六轮修订后）

## 1. 结论、角色与边界

- 日期：**2026-10-14（Asia/Shanghai）**；本机 `date` 返回同日、`CST`。
- 执行者：本会话 Codex，独立审阅角色，与作者第六轮修订角色分开。本轮只新增本报告，不改作者正文、来源记录、修订映射、登记、计划、关联条目或历史报告，不提交 Git commit。
- 用户约定配置：`gpt-6.1-sol / xhigh`。**仅为用户约定，不是已独立确认的执行元数据。** 本轮没有取得可独立核验的实际模型标识或 reasoning 配置，不以模型自述充当确认，未另行派发模型。
- 范围：仅 **B21-C30–C34**，优先级沿用初审；剩余关闭条件以[第五次定向复核](batch-21-t05-01-codex-recheck-5.md) L86、L98、L112、L125、L142 为权威，并对照[初审](batch-21-t05-01-codex-review.md) §6 和[任务验收](../../plans/full-coverage-backlog.yaml) L5403–5406。第六轮修订映射 L136–142 只用于定位落盘改动，不是关闭证据。
- **结果：0 CLOSED / 5 OPEN（1 P1、4 P2）；第六次定向复核不通过。4 条 acceptance：0 完整通过 / 4 未完整通过。** 认可新增 Cosign CLI 版本锚、API server 默认化与 kubelet 拉取职责分开、runc 同一容器 ID、镜像层清单留存格式，以及 Ascend “静态实现输出”措辞纠偏；这些已补子条件不再判作全缺失。
- 未执行镜像构建/拉取、SBOM 生成/比对、签名/验签、容器启动、设备访问、配置修改、隔离/负向试验或 GPU/NPU 实测。知识库 `make check` / `make build` 仅为结构校验与清单生成，不建立技术正确性、支持交集或硬件验证结论。

## 2. 输入身份与位置口径

用户给出的五个 SHA-256 前缀全部匹配；其余两个报告和计划另记录完整摘要。下文正文、作者记录、映射、登记和关联条目的行号均为本轮原文件坐标；不把网页阅读器显示行号直接拼作 GitHub 原文件锚点。

| 输入 | 完整 SHA-256 |
|---|---|
| [正文](../../knowledge/05-cluster-platform/container-image-runtime-baseline.md) | `0930afe504f2e55ba1a4c2d5d890a9f07142c86a94e0f3bb1b0b92ee1647ff3b` |
| [作者来源记录](batch-21-t05-01-sources.md) | `b5d6f05044058a4598d33c1ea8455b51bed1afea327f1583fb6580ef19afa120` |
| [修订映射](batch-21-review-fixes.md)，第六轮节 L136–142 | `27b801c8051f3d3992f9d0c91c843802352af1d6bad2b25c4833ce949c593a75` |
| [第五次定向复核](batch-21-t05-01-codex-recheck-5.md) | `4b6e13fb86ce76af7b5158752c7600d7ac7ee4885b977e9258a63eef7b6c59b4` |
| [初审](batch-21-t05-01-codex-review.md) | `341775efc62d7b8d46659c2d272aa31ae301b0cd1db47623ebe86490b80e34b5` |
| [任务验收计划](../../plans/full-coverage-backlog.yaml)，T05-01 L5386–5418 | `5f9bcf865b8c77e13cc8ee5f1c03140c37b86f558d8227d8bb2080249f4fcfc3` |
| [来源登记](../../sources/registry.yaml) | `d3b87c36605aa31e6116d6421cca3757dcfe352d57ade2b3841f0e316f987ee6` |

另读 README、编写指南、内容总目录、元数据 schema，以及本页链接的[Ascend 来源案例](../../knowledge/05-cluster-platform/ascend-device-visibility-source-case.md)和[待执行实验](../../knowledge/05-cluster-platform/ascend-device-visibility-experiment.md)。关联条目只用于核对本页摘要与判据，不扩大为重新验收这些条目。登记实计 **430 项**；新 CLI 登记在 L5336–5346。作者记录摘要与前次相同，本轮没有新增 CLI 版本/方法的作者取证记录；登记中的历史 `curl 200` 不计作本轮审阅者独立请求结果。

## 3. 一次源抽查：执行方法、文字与限制

### 3.1 curl 实际执行

对下表十八个 URL 实际执行只读 GET，使用本机 curl 8.7.1，保持默认 TLS 校验，没有 `-k`、替换证书、改 DNS 或绕过沙箱。每项的调用形态为：

```bash
curl --location --silent --show-error --connect-timeout 8 --max-time 20 \
  --output "$audit_dir/$name.body" --write-out '%{http_code}' "$url"
```

**18/18 均为退出码 6、HTTP `000`、`Could not resolve host`；未取得响应正文，TLS 握手未发生。** 因此不能写成 curl 成功、TLS 链已验证或 HTTP 200。诊断、URL 清单与输入摘要只存于临时目录 `/private/tmp/b21-t05-01-recheck-6.ORDfqlrF/`，没有加入知识库。没有请求提权，也没有执行任何来源页面中的命令。

### 3.2 允许的只读替代通道与文字核对

DNS 失败后使用 `web.run` 的明确 URL 打开、章节定位和正文阅读，以及 GitHub 只读连接器的 tag/commit 文件区间与公开 API 读取。**以下是文字核对，不只是判可达性；替代通道成功不冒充 curl 成功。** 网页通道可能使用缓存/正文提取；本轮未独立审计其 TLS 链、完整 HTTP 字节或刷新时刻。非版本化 Sigstore 页面仍不是固定文档修订。Ascend common.go 与 CDI SPEC 的 raw URL 在网页通道返回 Internal Error，改用 GitHub 连接器成功取得对应固定文件；不将该网页错误解释为源文件不存在。

| 抽查 / 实际 curl URL（全部 DNS 失败） | 替代通道实际核对位置与文字要点 |
|---|---|
| 01 / [Kubernetes Images v1.32](https://v1-32.docs.kubernetes.io/docs/concepts/containers/images/) | 网页：Image pull policy / Default image pull policy。Always 可复用相同 digest 的缓存；省略策略时按 digest/latest/无 tag/其他 tag 设置默认值；新对象提交 API server 时设置，后续镜像变更不自动改策略。用于 C30。 |
| 02 / [Syft README@v1.54.1](https://raw.githubusercontent.com/anchore/syft/v1.54.1/README.md) | 网页：Features / The basics。镜像、文件系统等扫描目标与 CycloneDX/SPDX 输出；不推定已读全部 cataloger 或实际扫描完整。用于 C30。 |
| 03 / [Cosign verifying](https://docs.sigstore.dev/cosign/verifying/verify/) | 网页：Keyless verification / Important Note / Local verifications。预期证书 identity/issuer 或可信公钥；默认校验载荷 digest 与镜像，关闭 claims 检查不能得到同一对象匹配结论。用于 C30。 |
| 04 / [Cosign CLI verify.go@11926fa5](https://raw.githubusercontent.com/sigstore/cosign/11926fa5/cmd/cosign/cli/verify.go) | GitHub：同版本 `cmd/cosign/cli/verify.go` L1–220，读取 verify 入口、key 示例和选项传递；另读固定选项文件并解引用 tag，见下段。不是运行输出。用于 C30。 |
| 05 / [containerd CRI config@v2.4.1](https://raw.githubusercontent.com/containerd/containerd/v2.4.1/docs/cri/config.md) | GitHub L1–180、L214–290，网页定位 Full configuration。v3 版本头、runtime/images 分区、runc handler/options 与 cdi_spec_dirs；cgroup 生效还涉及 kubelet/RuntimeClass 条件。用于 C31。 |
| 06 / [runc.8.md@v1.5.2](https://raw.githubusercontent.com/opencontainers/runc/v1.5.2/man/runc.8.md) | GitHub L1–165：DESCRIPTION / COMMANDS / GLOBAL OPTIONS。bundle/config.json、容器 ID、state/ps/events、状态 root 和日志路径/格式是不同记录对象。用于 C31。 |
| 07 / [CDI SPEC@cb98bcf6](https://raw.githubusercontent.com/cncf-tags/container-device-interface/cb98bcf66dc68530012483bd56e33e14d815e167/SPEC.md) | GitHub L1–150、L190–310：规范自述 1.1.0，v1.1.1 无 Spec 变更；Kind / CDI Devices / OCI Edits 分开设备名匹配及全局、设备级编辑范围。用于 C31/C32。 |
| 08 / [OCI config@v1.3.0](https://raw.githubusercontent.com/opencontainers/runtime-spec/v1.3.0/config.md) | 网页：Linux Process / POSIX-platform User。进程 AppArmor/SELinux 与 UID/GID/additionalGids 字段。用于 C31/C32。 |
| 09 / [OCI config-linux@92249139](https://raw.githubusercontent.com/opencontainers/runtime-spec/92249139eea7161e13745abd4cb6d0ea02a3227a/config-linux.md) | GitHub L127–151、L402–418：设备节点路径/类型/设备号/模式/属主与 allowed-device 的 allow/type/major/minor/access 分开。用于 C32。 |
| 10 / [NVIDIA plugin README@v0.20.1](https://raw.githubusercontent.com/NVIDIA/k8s-device-plugin/v0.20.1/README.md) | 网页配置节与 GitHub L320–445：cdi-cri 通过 CRI CDIDevices 且需转发/engine 支持；UUID/index 属分配传递；Shared Access 明示 time-slicing 不隔离显存/故障域。用于 C32/C34。 |
| 11 / [Toolkit 1.20.0 CDI](https://docs.nvidia.com/datacenter/cloud-native/container-toolkit/1.20.0/cdi-support.html) | 网页：Running a Workload with CDI / Using CDI with Non-CDI-Enabled Runtimes。原生 engine 请求 CDI 名；非原生 runtime CDI 模式可用 NVIDIA_VISIBLE_DEVICES，旧 hook 冲突按路径限定。用于 C32。 |
| 12 / [Toolkit 1.20.0 troubleshooting](https://docs.nvidia.com/datacenter/cloud-native/container-toolkit/1.20.0/troubleshooting.html) | 网页：NVML permissions / Containers losing access / Affected Environments。权限错误与 hook/legacy 的 Unknown Error 分开；更新可含 CPU/内存限制，systemd 更新另有条件；禁用 label 放弃 SELinux 隔离。用于 C34。 |
| 13 / [Toolkit 1.20.0 docker-specialized](https://docs.nvidia.com/datacenter/cloud-native/container-toolkit/1.20.0/docker-specialized.html) | 网页：GPU Enumeration / Driver Capabilities。GPU 选择与挂入的 driver libraries/binaries 分开；变量不提供具体库文件身份。用于 C32。 |
| 14 / [PyTorch CUDA notes 2.14](https://docs.pytorch.org/docs/2.14/notes/cuda.html) | 网页：Device-agnostic code 中可见设备段。CUDA_VISIBLE_DEVICES 管理可用 GPU 范围，该段没有逐 ordinal→UUID 的取证方法。用于 C32。 |
| 15 / [Ascend plugin.go@44385c13](https://raw.githubusercontent.com/Ascend/mind-cluster/44385c13d7b1d87def35f1604e8be4d16de6ca4e/component/ascend-device-plugin/pkg/server/plugin.go) | GitHub L1080–1175、L1290–1385：L1161–1169 是 UseAscendDocker 分支；原生挂载返回 DeviceSpec；Allocate 经最终 ID 处理调用设备/环境设置。不能据此认定 runtime 已消费。用于 C33。 |
| 16 / [Ascend common.go@44385c13](https://raw.githubusercontent.com/Ascend/mind-cluster/44385c13d7b1d87def35f1604e8be4d16de6ca4e/component/ascend-device-plugin/pkg/common/common.go) | GitHub L90–150：SetAscendRuntimeEnv 写 ID 串/runtime options；310B 写 allow-link；worker 组限 !PresetVDevice。先读 L480–660 未命中，随后读取上述正确区间，不把首次区间当作函数证据。用于 C33。 |
| 17 / [vLLM Ascend Issue #2557](https://github.com/vllm-project/vllm-ascend/issues/2557) | 网页：Your current environment / Describe the bug。容器节点/物理编号已有，选择变量含稀疏编号，错误要求输入范围 [0,4)；环境列 CANN 8.2.RC1。支持调查逻辑选择分叉，不直接证明 DAC/LSM 拒绝。用于 C34。 |
| 18 / [OCI image config@v1.1.1](https://raw.githubusercontent.com/opencontainers/image-spec/v1.1.1/config.md) | 网页：Layer DiffID / rootfs / history。DiffID 与 manifest layer digest 不能混同；diff_ids 有序，history 可选且存在不对应 rootfs 层的 empty_layer 项。这些是层身份，不是逐库成分归属方法。用于 C32。 |

**补充只读核对（未计入十八次 curl）：** GitHub [v3.1.3 ref](https://api.github.com/repos/sigstore/cosign/git/ref/tags/v3.1.3) 与 [tag 对象](https://api.github.com/repos/sigstore/cosign/git/tags/2f3a85b04907df5b770eb049d7e4d08d4b018d86) 返回 tag `2f3a85b04907df5b770eb049d7e4d08d4b018d86` → commit `11926fa5bbbbde47e88fc006b625a17769b743b2`；与作者前缀相符。另读该修订的 [options/verify.go](https://github.com/sigstore/cosign/blob/11926fa5bbbbde47e88fc006b625a17769b743b2/cmd/cosign/cli/options/verify.go) L1–195 和 [options/certificate.go](https://github.com/sigstore/cosign/blob/11926fa5bbbbde47e88fc006b625a17769b743b2/cmd/cosign/cli/options/certificate.go) L1–155，核对 key、默认 check-claims、输出选择及 keyless identity/issuer 要求。本轮只确认所选版本与这些入口，不声称 v3.1.3 是当前最新版本，不将 GitHub tag verification 属性当成本库镜像验签。审阅者补读不能替代作者正文/记录应交付的引用关联。

GitHub 文件响应的完整 blob SHA：Cosign CLI verify `408c88e8d4759f39b200212c904ffefbf2c8bfff`、options/verify `918e226e776d091b1d1ce7c432d1e9351a674833`、options/certificate `33a2329aafadacee33bacba8044bc2480cdc5edb`；containerd config `3a206263f4f9e76b6ca14110461b8661a03b1619`；runc 手册 `7e93a401f202f5746b7c27e81880166436c306ae`；CDI SPEC `2bc480a20ce447f5281b5d6844a486a81bb635b0`；NVIDIA plugin README `44594d4343967a313ff268223c8f638de005062c`；OCI Linux config `c71757494ca743fd90692c25e4897bf74cf00388`；Ascend plugin `b7692611b12884854d973fa2a3da18e381353f10`、common `6cd038e9f1d67a8a913aa4bb1301692f177b3dbe`。它们是文件 blob 身份，不是 commit，也不证明支持交集。

## 4. B21-C30–C34 逐项复核

### B21-C30 — P2 / OPEN

**权威条件：** 第五次复核 L86。**本轮位置：** 正文 L8–25、L27、L38、L50–58、L137；作者记录 L9、L17、L23–25；第六轮映射 L138；登记 L5303–5313、L5336–5346。

| 子条件 | 本轮判断与位置证据 |
|---|---|
| 构建/SBOM 已补方法 | **保持满足。** L50–52 的上下文身份、参数/锁文件与工具记录，以及 L56 的扫描对象/配置/输出身份、包名/版本/来源层比较和差异处理保持；不以未实际生成结果重新阻塞。抽查 02 的已读范围限定保留。 |
| 签名固定依据与信任输入 | **版本锚新补，方法引用关联未闭环。** L57 选 CLI v3.1.3，登记已有对应项，审阅者解引用相符；不再称 CLI 版本未选。identity/issuer 或可信 key、digest 匹配与结果字段保持。该行实际链接仍仅为未固定修订的两个文档页，没有指向所选 CLI 的方法依据；新增 CLI 登记 ID 未进入正文 source_refs，作者记录 L25 仍仅列旧 docs 项，未记录所选 CLI/已核对位置。登记 L5346 仍说核验语义以文档页为准。审阅者补读固定选项不能冒充作者已完成方法取证同步。 |
| 默认化与 kubelet 拉取职责 | **本轮纠偏满足。** L58 明确 API server 侧字段填充与 kubelet 按策略拉取，已有默认值/缓存/实际事实字段。抽查 01 支持该区分；不再保留“kubelet 默认化”阻塞。 |
| 已读/未知状态同步 | **仍不满足。** L27 仍称 SBOM/签名无官方工具取证；L137 仍将官方工具整体列待确认，与 L23–24、L38、L56–57 及作者记录 L25 的工具入口已读范围相冲突。未知应限未读实现/配置、未执行结果或未固定文档，不扩大成没有官方工具取证。 |

**剩余关闭条件：** 在 L57 附近引用与所选 CLI 修订相对应的核验依据，并同步正文来源关联、作者记录的版本/具体位置/已读与未覆盖范围；同步 summary/notes/待确认中的 SBOM 与签名状态。保留已补版本锚、信任输入、对象匹配、默认化职责和构建/SBOM/缓存格式；**不要求运行工具或制造结果**。

### B21-C31 — P2 / OPEN

**权威条件：** 第五次复核 L98。**本轮位置：** 正文 L27、L38、L62、L71–72、L137；作者记录 L10、L26–28；第六轮映射 L139；登记 L5248–5269、L5314–5324。

| 子条件 | 本轮判断与位置证据 |
|---|---|
| containerd 所选配置与生效核对 | **仍不足。** L62 的 version=3、CDI 目录值保持，但仍没有完整 runtime/images 分区键、handler/options 的字段级参考值/条件和可填写实际值记录；“记录所选分区字段参考值，核对配置来源与实际运行的 runtime handler”没有交代同一运行身份、配置来源/摘要、状态/日志对象如何对应及如何判不符。抽查 05 已提供确切分区与 RuntimeClass/kubelet 条件，不要求现场输出。 |
| runc 同一运行关联 | **共同容器 ID 新补，其余未落实。** L62 加“同一容器 ID”，不再判该字段完全缺失；仍只有 bundle 配置→状态查询→日志采集箭头，缺 bundle/config 路径或身份、状态 root/状态字段、观察时间窗与日志对象定位及不符判据。抽查 06 表明这些入口不相互替代。 |
| CDI 三层身份、OCI 与同步 | **正文主体保持满足，摘要/待确认残留。** L62/L72 已分 repo tag v1.1.1、spec 1.1.0 与文件 cdiVersion，L71 有 CRI 条件，OCI 通用/Linux 链接正确。L27 的 CDI 1.1.1 固定点仍未限定为 repo tag；L137 仍将 CDI 规范正文、containerd/runc 正文整体列待确认，与 L38/L62 和作者记录 L26–28 不同步。抽查 07–09 支持既有纠偏。 |

**剩余关闭条件：** 将已选 v3 模式落成精确分区/字段/参考值或实际 unknown 值的记录格式及生效条件，交代配置—runtime/容器身份—状态—日志对应及不符判定；补 runc 的 config/bundle 身份、状态 root/字段、时间窗和日志定位；同步 CDI 身份及实际已读范围。保留新补共同 ID 和正确 OCI/CRI 条件；**不要求配置变更或建立整栈兼容组合**。

### B21-C32 — P2 / OPEN

**权威条件：** 第五次复核 L112。**本轮位置：** 正文 L66–80、L103–106；作者记录 L11、L24；第六轮映射 L140。

| 子条件 | 本轮判断与位置证据 |
|---|---|
| 原生 CDI 模式边界 | **保持满足。** L71 没有把 envvar/volume-mounts/NVIDIA_VISIBLE_DEVICES 混入原生链；CRI 转发/消费支持前提保持。抽查 10–11 支持，不能再以选择变量缺失判所有模式注入失败。 |
| 字段级分配—传递—匹配—OCI | **仍未交付。** L69/L71 虽标“字段级核对关系”，仍从资源请求数量跳到生成条目和消费；没有实际 Allocate ID 如何形成 qualified CDI name、如何对应 CRI CDIDevices 项及 devices[].name，也没区分全局/设备级 containerEdits 与最终节点/挂载的对应记录。抽查 07 的 Kind/CDI Devices/OCI Edits 和抽查 10 的传递策略明确是不同连接环节；“逐段记录实际值”不能代替连接规则。 |
| 三层库身份与成分归属 | **层清单留存格式新补，三层方法仍缺。** L68 新增层号/digest/diff_id/annotations 文件格式，认可留存设计；仍未交代如何从选定镜像/扫描结果得到具体库名称/版本/路径与来源层证据，并连接镜像/层身份。抽查 18 的 DiffID/rootfs/history 只支持层对象，不能自动建立逐库归属；不将 digest 与 DiffID 视作同一值。L66–67 也仍缺宿主/注入用户态组件的身份、版本、宿主来源→容器路径及证据定位格式。 |
| ordinal 与稳定身份/最终对象 | **表格保持，方法仍未补。** L74、L78 继续明确 UUID/序列号方法未取源；可见集＋分配记录＋物理标识三方比对没有固定框架依据，也未连到最终 OCI 注入对象。抽查 14 的可见范围段不是逐 ordinal→UUID 方法。保持 unknown 是正确，但不等于方法已交付。 |
| 权限、进程与 LSM | **保持满足。** L73 的节点/许可/进程身份/LSM 事件关联与“无事件不推定已允许”保留，抽查 08–09 支持所列字段；无现场事件不作新增阻塞。 |

**剩余关闭条件：** 在选定 cdi-cri 模式下补字段级连接规则/可填写对应记录；补宿主、注入用户态组件、镜像自带库的成分身份/版本/路径/来源及证据定位方法，说明层清单如何支持而非替代成分归属；用固定框架/设备身份依据连接 ordinal、分配、CDI 与最终 OCI 对象。证据缺失仍可 unknown；保留模式和 LSM 限定；**不要求执行采集或负向试验**。

### B21-C33 — P2 / OPEN

**权威条件：** 第五次复核 L125。**本轮位置：** 正文 L17、L38、L86–88、L137；作者记录 L12、L17；第六轮映射 L141；登记 L5237–5247、L5325–5335。

| 子条件 | 本轮判断与位置证据 |
|---|---|
| 插件分支/common 静态输出 | **保持满足，措辞本轮纠偏满足。** L86 正确区分 L1161–1169 分支与 L1087 挂载函数体，链接同 commit common.go，保留 310B/!PresetVDevice 条件；后半改为“静态实现输出字段”，不再称实测。抽查 15–16 支持这些静态事实，不重新保留措辞阻塞。 |
| runtime 消费实现与两端连接 | **核心条件仍未满足。** L86 继续明写“未选定组件/ref”，节点/环境/库挂载消费及白名单 unknown，Allocate 完整链仍未审计。插件 DeviceSpec/Envs 输出不是对应 runtime 已读取并编辑最终配置的证据；仍没有生产端字段→消费端配置/最终节点、挂载的具体连接。第六轮映射“消费端 unknown 收窄”没有交付所需消费实现。 |
| 已读范围同步 | **仍有残留。** L38/L86 与作者记录承认 common 输出已读，L137 却继续把“辅助函数语义”整体列待确认，登记 L5247 也仍说辅助函数语义未核对；须区分已读插件辅助输出与未读 runtime 库注入/白名单，不能混为同一缺口。 |
| 目标组合/GPU-NPU 边界 | **保持满足。** L43/L88 保留产品、OS/内核、驱动固件、runtime/plugin、CANN/框架、镜像字段及支持交集 unknown；GPU 不套用 NPU、digest 不作兼容证明、ACP 不引入的限定保持。 |

**剩余关闭条件：** 固定并引用实际选择的 Ascend runtime/ref，核对设备、环境、库挂载消费实现，连接插件/辅助函数具体返回字段与消费端/最终配置；同步已读静态输出与未读消费端范围。保留正确分支/common 条件和本轮静态措辞；支持交集仍可 unknown。**要求实现取证，不要求现场试运行**。

### B21-C34 — P1 / OPEN

**权威条件：** 第五次复核 L142。**本轮位置：** 正文 L94–132；作者记录 L13；第六轮映射 L142；关联案例 L32–40，关联实验的控制条件/旁路/判据章节。

| 子条件 | 本轮判断与位置证据 |
|---|---|
| 五栏清单与三单比较对象 | **已补表格/硬件行保持，完整关联仍缺。** L101 保持机型/卡型号/数量，L103 仍把请求数量作为 ID 值例子，没有实际 Allocate ID；L104 仅容器内采集、L106 仅附镜像库，不能补足 C32 的三层库/最终配置/稳定身份。L112/L116 的缺一单→无法判定保持，但仍未定义请求数量、分配设备、默认/控制节点与作业节点、框架逻辑编号的比较范围及稳定身份归一化规则；文本/数量一致不足以证明同一设备。 |
| NPU 逻辑选择与访问拒绝分开 | **混类未改。** L117 仍把设备不可见/越界称“NPU 访问拒绝”，以映射一致/持续分叉作完成/失败；L130 却已说逻辑编号/选择分叉。抽查 17 已有节点而报参数范围错误，不直接支持 DAC/LSM 拒绝；实现语义 unknown 时不能靠三单齐给无条件技术判定。 |
| 隔离、受控访问与恢复完成 | **未满足。** L114/L118 仍以关共享后影响消失判隔离完成，只能收敛本次共享影响解释，不能证明设备访问、显存、计算份额或故障域隔离。L113 拒绝消除/注入完整、L115 注入集恢复仍缺同一目标进程受控访问与原访问边界恢复条件。抽查 10/12 支持这些区别，未要求执行对照。 |
| 单变量、安全、旁路与负向组 | **既有计划表保持，内容仍不足。** L124–128 的单 Pod/单次启动/三单快照没有 Pod/容器/进程身份、明确时间窗和证据对象路径/身份；“仅模式/权限/共享开关不同”没有配置键/旧新值。旁路未覆盖 privileged、设备 hostPath、人工挂载、默认注入或显式选择变量；L130 仅给单独授权原则，缺未请求/未授权设备负向组、安全停止及回到基线判据。L128 “仅镜像/驱动版本不同”仍不对应 L115 的 hook/legacy 容器更新，且没有保证唯一变量；抽查 12 包括 CPU/内存更新条件。 |
| 案例环境/缺项摘要与 NVML 区分 | **既有纠偏保持，前次要求仍未补。** L113 的权限错误/Unknown Error 分开和 L130 的框架版本/非本库复现保留；本页仍没摘要 CANN 8.2.RC1、runtime/plugin/驱动固件/digest 等关键缺项，只让读者到关联页查。关联案例 L38–40 与抽查 17 已提供这些定位；源案例链接不能代替本页应交付的条件摘要。 |

**剩余关闭条件：** 补三层库/实际分配/最终配置/稳定身份关联清单，并定义三单集合的比较范围；将逻辑选择失败与策略访问拒绝分开，语义未取源时判无法确定；将共享影响对照与隔离维度分开，补目标进程访问/恢复边界。细化计划表的配置键/旧新值、主体/时间窗/证据定位、旁路排除、负向组、安全停止与回到基线，修正回退更新变体；在本页摘要案例 CANN 与关键缺项。保留已有表格、硬件行、缺证据判据、NVML 区分及授权限定；**不要求制造结果或执行生产变更**。

## 5. Acceptance 与最终计数

| 计划位置 / acceptance | 本轮判断 | 未关闭原 ID |
|---|---|---|
| L5403 / 镜像身份、构建输入、SBOM/签名、拉取方法与限制 | 部分满足，**未完整通过**：CLI 身份锚与默认化职责进步；固定方法引用/作者取证关联及状态同步尚未闭环 | B21-C30 |
| L5404 / 固定 runtime/Toolkit/CDI，分离宿主、库、设备/环境/挂载、权限、框架映射 | 部分满足，**未完整通过**：共同 ID 与层清单格式进步；配置诊断关联、三层库、字段级链与稳定映射仍不足 | B21-C31、B21-C32 |
| L5405 / Ascend runtime/plugin 独立取证、目标组合与 GPU/NPU 边界 | 部分满足，**未完整通过**：静态措辞纠偏；runtime 消费实现/两端连接未交付，已读范围同步有残留 | B21-C33 |
| L5406 / 清单、异常/隔离分支、对照验证及源案例，不作安装处方 | 部分满足，**未完整通过**：既有表格与限定保持；比较对象、分支分类、访问/隔离/恢复及安全单变量设计仍不足 | B21-C34 |

**5 个原发现：0 CLOSED / 5 OPEN（1 P1、4 P2）；无新增发现 ID，无优先级调整。** 上述残留和新增修订中的方法关联不足均在所属原 ID 下追记；未发现必须另立 ID 的已确认事实错误。不会将所有子条件未闭环概括为“第六轮毫无改动”，也不会因登记新增一项或仍保留 unknown 就宣告关闭。不因 curl DNS 失败本身判技术不通过，不以审阅者补证替代作者必交内容。模型执行元数据未独立核验的限制也不由结构 PASS 消除。

## 6. 结构校验与单文件边界

- 写入前原仓库 `PYTHONDONTWRITEBYTECODE=1 make check`：**PASS：94 content entries / 430 sources**。七个输入及 377 个既有 Git 所列 tracked/untracked 非忽略文件和原仓库 build 文件的摘要检查无变动。
- 写入后原仓库 `PYTHONDONTWRITEBYTECODE=1 make check`：**PASS：94 content entries / 430 sources**；报告五项原 ID/优先级/状态和行尾空白核对通过。
- 为遵守单文件约束，复制仓库到 `/private/tmp/b21-t05-01-recheck-6.ORDfqlrF/validation/`，排除 `.git`、`.venv`、`.agents`、`.codex` 和缓存；副本使用原仓库虚拟环境 Python、禁写字节码执行 `make check` / `make build`，均 **PASS：94 content entries / 430 sources**。只在副本重建 `build/catalog.json` / `build/catalog.md`，不在原仓库重建 build，没有镜像构建。
- 前后摘要核对：**377 个既有文件全部不变**，包含七个输入及原仓库 build 文件；本轮只新增本报告，已有作者改动和未跟踪文件保留。临时诊断/摘要清单不作为正式知识库证据包。
- 未改 `src/kb/` 或测试代码，不需 `make test`，不为内容复核报告新增测试。结构检查不验证远程内容或技术正确性，不改变上述技术不通过结论。

**最终技术结论：第六次定向复核不通过，C30–C34 全部保持 OPEN；已披露 curl DNS 失败与只读替代通道的文字核对/限制，未独立确认实际执行模型元数据，未执行实测。**
