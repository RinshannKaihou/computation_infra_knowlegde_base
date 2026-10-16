# Batch 21 补交 T05-01 第三次定向复核（作者第三轮修订后）

## 1. 结论、角色与边界

- 日期：**2026-10-14（Asia/Shanghai）**；本机日期与本轮环境日期一致。
- 执行者：本会话 Codex，独立审阅角色；本轮未参与作者修订。原仓库只写本报告，不改作者正文、来源记录、修订映射、登记、计划或既有报告，不提交 Git commit。
- 用户约定配置：`gpt-6.1-sol / xhigh`。**仅为用户约定，不写成已独立确认的执行元数据。** 本轮没有取得可独立核验的实际模型标识或 reasoning 配置，没有用模型自述确认，也未另行派发模型。
- 范围：仅 **B21-C30–C34**；优先级沿用原报告。剩余关闭条件以[第二次定向复核](batch-21-t05-01-codex-recheck-2.md) L102、L117、L130、L143、L159 为权威，并对照[初审](batch-21-t05-01-codex-review.md) §6。修订映射是作者自述，不代替正文和一次源证据。
- **结果：0 CLOSED / 5 OPEN（1 P1、4 P2）；第三次定向复核不通过。四条 acceptance 均未完整满足。** 本轮认可五栏模板实装、新来源登记等局部进展，但关键旧错误及必交方法仍未关闭。
- 未执行镜像构建、拉取、SBOM 生成或比对、签名或验签、容器启动、配置修改、设备访问、隔离试验或 GPU/NPU 实测。知识库结构校验/清单构建不是这些实测；不建立软件支持交集或硬件验证结论。

## 2. 输入身份与位置口径

用户给出的五个 SHA-256 前缀全部匹配。七个输入的完整摘要如下；后文行号均指本轮这些原文件，不沿用旧正文坐标。

| 输入 | 完整 SHA-256 |
|---|---|
| [正文](../../knowledge/05-cluster-platform/container-image-runtime-baseline.md) | `f1ded47d40c5df72399b8fee38a325ad550795c5f3eff01e87da1babe75ecc93` |
| [作者来源记录](batch-21-t05-01-sources.md)，第三轮增补 L19–28 | `ea9f2e16ec5132e45012abeded500592bcaa6daf91dc19365872b272e3e5524d` |
| [修订映射](batch-21-review-fixes.md)，第三轮节 L110–117 | `57514806f44b130b27fd4752c5743b2dada29b96ade5d72e9e0bac08aa925461` |
| [第二次定向复核](batch-21-t05-01-codex-recheck-2.md) | `3670f647936a798218b72d0dedf029f469acf56adf0b5d0b3cdf626bddff3d06` |
| [初审](batch-21-t05-01-codex-review.md) | `341775efc62d7b8d46659c2d272aa31ae301b0cd1db47623ebe86490b80e34b5` |
| [任务验收计划](../../plans/full-coverage-backlog.yaml)，T05-01 acceptance L5403–5406 | `5f9bcf865b8c77e13cc8ee5f1c03140c37b86f558d8227d8bb2080249f4fcfc3` |
| [来源登记](../../sources/registry.yaml) | `e12c48a67e2fd6f6cd0d3f14af865c92b666807e722370c915ecc5b5c8ead0a4` |

另读 README、编写指南、内容总目录、元数据 schema，以及本页实际链接的[Ascend 来源案例](../../knowledge/05-cluster-platform/ascend-device-visibility-source-case.md)与[待执行实验](../../knowledge/05-cluster-platform/ascend-device-visibility-experiment.md)。关联条目用于判断本页链接和摘要的支持范围，不扩大为重新验收这些条目。

登记实计 **428 项**，较前次增加五项（登记 L5270–5324：Kubernetes Images、PyTorch CUDA、Syft、Cosign、runc 手册）；正文 L20–24 已同步 `source_refs`。新增来源登记成立，不等于其全部语义已写入正文，更不等于登记中的作者 `curl 200` 是本轮审阅者独立确认的执行记录。

## 3. 一次源抽查：方法、实读内容与限制

### 3.1 curl 实际结果

执行九次只读 GET，使用默认 TLS 校验，响应写 stdout；命令形态为：

```bash
curl --fail --silent --show-error --location \
  --connect-timeout 10 --max-time 25 \
  --write-out '\nhttp=%{http_code}; effective_url=%{url_effective}; bytes=%{size_download}\n' \
  <下表精确 URL>
```

未使用 `-k`/`--insecure`，未修改 DNS、代理或 TLS 设置。**九次均 exit 6 / HTTP 000 / 0 bytes，错误为无法解析主机名；未进入 TLS 握手，未取得远端正文。**

| 实际请求 URL | 结果 |
|---|---|
| <https://v1-32.docs.kubernetes.io/docs/concepts/containers/images/> | DNS 失败 |
| <https://raw.githubusercontent.com/anchore/syft/v1.54.1/README.md> | DNS 失败 |
| <https://docs.sigstore.dev/cosign/signing/overview/> | DNS 失败 |
| <https://raw.githubusercontent.com/containerd/containerd/v2.4.1/docs/cri/config.md> | DNS 失败 |
| <https://raw.githubusercontent.com/opencontainers/runc/v1.5.2/man/runc.8.md> | DNS 失败 |
| <https://raw.githubusercontent.com/cncf-tags/container-device-interface/cb98bcf66dc68530012483bd56e33e14d815e167/SPEC.md> | DNS 失败 |
| <https://docs.pytorch.org/docs/2.14/notes/cuda.html> | DNS 失败 |
| <https://docs.nvidia.com/datacenter/cloud-native/container-toolkit/1.20.0/troubleshooting.html> | DNS 失败 |
| <https://raw.githubusercontent.com/Ascend/mind-cluster/44385c13d7b1d87def35f1604e8be4d16de6ca4e/component/ascend-device-plugin/pkg/server/plugin.go> | DNS 失败 |

### 3.2 允许的只读替代通道及内容核对

随后用 **Web `open`/`find` 取文**，以及 **GitHub 连接器 `fetch_file` 按明确 ref 和原文件范围读取**。阅读了下表相关正文，不是只检查链接可达或搜索摘要。CDI raw URL 在 Web 通道返回 Internal Error，改用 GitHub 连接器读取同 commit 的 `SPEC.md` L1–135 成功；Syft GitHub HTML 阅读视图未展示所需段落，另读同 tag 的 raw README 和连接器文件正文。Ascend 通过连接器读取原文件 L1080–1175。

替代通道可能提供缓存/抽取文本，不等同于本机 curl 成功，不能据它独立核验本机 TLS 会话、原始响应字节摘要或作者历史取证时间。网页工具行号不作 GitHub 原文件 `#L` 锚点；以下源码坐标只使用原文件读取坐标。Cosign 为未版本化的动态文档，本轮没有把登记中的“取证时最新 tag”当作已独立确认的当前版本。没有执行上游文档里的安装、修改、生成或恢复命令。

| 一次源 / 实读定位 | 核对到的关键文字与本轮用途 |
|---|---|
| [Kubernetes v1.32 Images](https://v1-32.docs.kubernetes.io/docs/concepts/containers/images/#image-pull-policy)，Image pull policy / Default image pull policy | 三种策略分别规定本地存在、解析 digest 后复用缓存、禁止拉取等行为；digest/非 latest tag 与 latest/无 tag 有不同默认值。字段在对象首次创建时设置，改镜像引用不自动改策略。正文 L57 只列字段和值及“默认化/缓存语义”名称，未交付这些规则。 |
| [Syft README@v1.54.1](https://github.com/anchore/syft/blob/v1.54.1/README.md)，Features / The basics | 支持镜像/文件系统、包生态和 CycloneDX/SPDX 等输出；基础示例针对成分/包清单。不能据此推出正文 L55 的“镜像全部层文件清单”，也没有把两份 SBOM 一致定义为完整性证明。本轮未读取全部 cataloger/扫描配置实现，不能补写其全覆盖能力。 |
| [Cosign signing overview](https://docs.sigstore.dev/cosign/signing/overview/)，签名、见证、验证流程；[Verifying Signatures](https://docs.sigstore.dev/cosign/verifying/verify/)，Keyless verification / Local verifications | 身份式核验示例包含预期证书身份与 OIDC issuer；公钥模式指定可信 key；默认还核对签名载荷中的镜像 digest。仅写 `cosign verify` 名称和“发布身份”不足以交付预期身份/信任输入与证据记录方法。验证页是审阅补证，不算作者已登记/交付该页。 |
| [containerd config.md@v2.4.1](https://github.com/containerd/containerd/blob/v2.4.1/docs/cri/config.md)，Config versions / Full configuration / Image Pull Configuration | 配置示例有 `version = 3`，v2 配置有转换规则；runtime/images 插件分区有各自字段，runtime 分区列 `cdi_spec_dirs`。正文只说“含版本头、字段、分区”，没落下所选模式的值/归属或诊断记录方法。这里只核文档，不证明现场配置。 |
| [runc.8.md@v1.5.2](https://github.com/opencontainers/runc/blob/v1.5.2/man/runc.8.md)，DESCRIPTION / COMMANDS / GLOBAL OPTIONS | bundle 的 `config.json`、状态/进程/事件入口、debug/log/root 及 systemd cgroup 选项确有正文；新增版本化手册来源有效。正文 L61 未交代用哪些状态/配置/日志证据核对何种判断，不能由链接补齐诊断方法。 |
| [CDI SPEC.md@cb98bcf6](https://github.com/cncf-tags/container-device-interface/blob/cb98bcf66dc68530012483bd56e33e14d815e167/SPEC.md)，原文件 L1–135 | Version 为 spec 1.1.0；v1.1.1 行注明无 Spec 变更；描述读取 CDI 文件并修改 OCI 配置，JSON 中有 `cdiVersion`、`kind`、`devices`、`containerEdits` 等身份/编辑字段。L61 三层身份区分正确，L71“规范 v1.1.1（未读）”仍与它冲突。blob：`2bc480a20ce447f5281b5d6844a486a81bb635b0`。 |
| [NVIDIA 插件 README@v0.20.1](https://github.com/NVIDIA/k8s-device-plugin/blob/v0.20.1/README.md)，DEVICE_LIST_STRATEGY / DEVICE_ID_STRATEGY / Shared Access | `envvar` 经 `NVIDIA_VISIBLE_DEVICES` 指示 NVIDIA Runtime；`cdi-annotations` 需 CDI engine；`cdi-cri` 使用 CRI 的 `CDIDevices` 并需 Kubernetes 转发支持。time-slicing 不提供所述显存/故障域隔离。用于核对 L68–70 的模式混接及 L106 的判定边界。 |
| [Toolkit 1.20.0 CDI](https://docs.nvidia.com/datacenter/cloud-native/container-toolkit/1.20.0/cdi-support.html)，Running a Workload with CDI / Using CDI with Non-CDI-Enabled Runtimes | 原生 engine 例子通过 CDI 名称请求设备；非原生路径可由 NVIDIA Runtime 的 CDI 模式解释环境变量。两者不能省略条件拼成一个原生链，原生链也不以选择变量存在为必需证据。页内另有旧 hook/变量冲突提示，未执行其处置建议。 |
| [OCI image config@v1.1.1](https://github.com/opencontainers/image-spec/blob/v1.1.1/config.md)，OCI Image Configuration；[runtime config@v1.3.0](https://github.com/opencontainers/runtime-spec/blob/v1.3.0/config.md)，Process / User | 前者是镜像 JSON/层及执行参数，后者才是运行时进程、挂载等配置；L61“OCI 通用字段”仍指错规范。运行时规范可定位进程身份、AppArmor profile 和 SELinux label 等字段，不能以本页 LSM 一句 unknown 替代记录方法。 |
| [PyTorch CUDA notes 2.14](https://docs.pytorch.org/docs/2.14/notes/cuda.html#device-agnostic-code)，Device-agnostic code | `CUDA_VISIBLE_DEVICES` 管理 PyTorch 可用 GPU，设备上下文控制 tensor 目标设备；该段不交付 ordinal→UUID 的证明链。新增来源只支持可见集管理，不能关闭 L73 承认缺失的稳定物理映射方法。 |
| [Ascend plugin.go@44385c13](https://github.com/Ascend/mind-cluster/blob/44385c13d7b1d87def35f1604e8be4d16de6ca4e/component/ascend-device-plugin/pkg/server/plugin.go)，原文件 L1080–1175 | 设备挂载辅助函数填 `DeviceSpec.HostPath/ContainerPath/Permissions`；`setNPUDeviceMount` 的 `UseAscendDocker` 判断在 L1161 起，假分支调用挂载辅助函数，另一分支调用 `common.SetAscendRuntimeEnv`。blob：`b7692611b12884854d973fa2a3da18e381353f10`。本轮未继续核对环境辅助函数/runtime 消费端，不替作者补交。 |
| [Toolkit 1.20.0 Troubleshooting](https://docs.nvidia.com/datacenter/cloud-native/container-toolkit/1.20.0/troubleshooting.html#nvml-insufficient-permissions-and-selinux)，两个 NVML 情境 | SELinux 权限段的消息是 `Failed to initialize NVML: Insufficient Permissions`，并警告关闭标签隔离的代价；`Unknown Error` 在 hook/legacy 更新后访问丢失段。正文 L105 的消息/章节错配未改，L107 的更新/恢复限定已有进展。 |
| [vLLM Ascend Issue #2557](https://github.com/vllm-project/vllm-ascend/issues/2557)，环境、Pod 请求、编号及错误段 | 报告请求四个 NPU、物理编号 0/3/4/7 可列举，而输入选择触发 `[0,4)` 参数范围错误；环境列 torch 2.5.1、torch_npu 2.5.1.post1、vLLM 0.9.1、Ascend dev `f6a0e1629`。支持编号/选择分叉候选，不是权限拒绝或完全无节点的直接证明，不是本库复现。 |

## 4. B21-C30–C34 逐项复核

### B21-C30 — P2 / OPEN

**权威条件：** 第二次复核 L102。**位置：** 正文 L26、L37、L48–57、L119；作者记录 L9–10、L17、L23–25；映射 L113；登记 L5209–5214、L5270–5280、L5292–5313。

| 条件 | 本轮判断与位置证据 |
|---|---|
| 输入身份、证据留存与缺项格式 | **部分满足。** L49–51 已写 git commit、参数键值、锁文件名称/哈希、工具/版本及部分缺项判据，不再只是 unknown 列名；不要求为此选定某种构建工具。但上下文仅“路径/版本”未说明如何固定内容，证据格为“本库设计约定/同上”，仍缺输入记录与具体证据对象身份/定位的对应格式。 |
| SBOM 对象、方法和完整性边界 | **新增工具来源已满足，方法/范围未满足。** L55 固定 Syft 版本并保留未执行限定；“全部层文件清单”超出 README 支持范围，未记录扫描范围/输出身份。两份生成结果一致最多支持所选方法的重复一致，不能排除共同漏检；需说明比对对象、差异处理及不可证明的覆盖范围。 |
| 签名固定依据、信任输入及核对边界 | **部分满足。** L56 分列 digest 签名/日志对象，且不宣称内容正确；Cosign 文档及 CLI 版本/修订未在正文固定，核对方法只有命令名，没有预期签名者、issuer 或可信 key、对象 digest、核验结果证据格式。不能无条件从“验签通过”推出符合预期发布身份。 |
| 拉取路径、默认值与缓存记录 | **部分满足。** L57 已选 Kubernetes→CRI，列三种字段值和 digest/时间/实际策略；仍未写何时默认 Always/IfNotPresent、对象创建后策略不自动随镜像改变，以及 Always 解析 digest 后仍可用缓存等规则，也没有缓存/实际下载事实记录字段。还应区分对象创建时默认化与 kubelet 的拉取决策，不能笼统称“kubelet 默认化”。依据为 §3.2 的版本化 Images 页面。 |
| 原规范纠偏保持与记录同步 | **正文既有纠偏保持，同步仍未满足。** L52–54 的分级/必填可选/可复现边界本轮不重复要求；作者记录 L9 仍称“SHOULD 注解”，L17 与正文 L26/L37/L119 仍把已经补入的 SBOM/签名来源列作未取。增补表和新登记没有消除旧状态矛盾。 |

**原 ID 下事实追记：** L55 对 SBOM 范围的过度概括，以及 L57 把默认化笼统归 kubelet，仍归 C30 的记录对象/方法/限制，不另设 ID，不调整优先级。

**剩余关闭条件：** 补输入身份与证据留存定位；将 SBOM 范围改成所选配置实际支持的成分记录，交付生成/比较记录和共同漏检边界；固定签名依据与预期信任输入、对象匹配及结果记录；写拉取默认化/缓存行为和事实采集字段；同步旧来源记录、summary、verification notes 与待确认项。实际值、实测结果继续可以 unknown，不要求本次执行任何供应链工具。

### B21-C31 — P2 / OPEN

**权威条件：** 第二次复核 L117。**位置：** 正文 L26、L37、L61、L68–72、L119；作者记录 L10、L17、L26–28；映射 L114；登记 L5248–5269、L5314–5324。

| 条件 | 本轮判断与位置证据 |
|---|---|
| containerd 配置模式/字段与诊断依据 | **部分满足。** 版本化精确文件已引用；L61 新列 `runtime_type`、插件分区、版本头和 CDI 目录字段，但没有实际配置版本值、所选分区归属/生效条件及配置/状态/日志如何参与核对。列“文档含什么”不等于交付本页方法。 |
| runc 固定文件、登记引用与诊断依据 | **固定入口子条件已满足；诊断仍未满足。** L24/L61 与登记 L5314–5324 实装版本化手册，§3.2 实读确认；正文仍只写手册“含 cgroup/systemd 条目”，未展开相关字段、状态/日志证据和判断边界。不是要求逐项审计全部 runc 驱动实现。 |
| CDI 版本残留、生成/传递/消费前提 | **三层身份子条件在 L61 已满足，残留与链条件仍未满足。** L71 继续写“CDI 规范 v1.1.1（未读，unknown）”；L68–70 没有选 `cdi-annotations` 或 `cdi-cri` 及对应 engine/Kubernetes/CRI 转发条件。支持交集可以 unknown，但必须明确所选链需要什么。模式混接另在 C32 追记。 |
| OCI 通用/Linux 精确入口与状态同步 | **未满足。** L61 的“OCI 通用字段”仍链接 image-spec `config.md`，不是 runtime-spec 同名文件；L72 有正确 User 链不能抵消该错链。映射 L114 称已修正，实际未改。L37/L119、作者记录 L10/L17 的“正文未读/语义 unknown”与增补表及登记取证范围仍不一致。 |

**剩余关闭条件：** 落下所选 containerd 配置版本/分区/字段和诊断记录方法，补 runc 相关配置/状态/日志核对依据；清除 CDI 规范误标与未读残留，明确生成者、选定传递字段和消费前提；把 L61 改为正确 runtime-spec 精确入口并同步取证状态。已交付的 runc 版本化手册入口不再当作缺失，仍不要求虚构整栈兼容。

### B21-C32 — P2 / OPEN

**权威条件：** 第二次复核 L130。**位置：** 正文 L65–73、L91–98；作者记录 L11、L24；映射 L115；登记 L5281–5291。

| 条件 | 本轮判断与位置证据 |
|---|---|
| 三个来源层的库身份/版本 | **职责解释保持，身份方法仍未满足。** L65–66 分开宿主内核和挂入用户态组件，变量职责正确；L67 仍只有 NGC 层数、Signed、build 元数据，没有镜像 CUDA/框架库与注入驱动库的名称/版本/路径/来源及证据定位格式。§4 也没有独立库身份记录行。 |
| 一个选定 GPU 模式的字段级链 | **未满足，新增实例混接模式。** L68 自称原生 CDI，L70 却把 `envvar` 传递 ID→CDI→`NVIDIA_VISIBLE_DEVICES` 落位串成通用链。官方插件把 envvar 与两种 CDI 策略分开；Toolkit 文档允许非原生 runtime CDI 模式使用环境变量，不能因此省略路径前提。实际 Allocate ID、CDI qualified name/传递字段、CDI 匹配项和 OCI edits 的关系仍未给出，末句要求读者逐段记录不能替代核对方法。 |
| DAC、设备规则、LSM 的证据关联 | **字段分离保持，关联方法仍缺。** L72 有节点、许可和进程 UID/GID/附加组；LSM 仍仅“另行取证 unknown”。没有策略/label/profile、拒绝事件、进程/设备/时间的关联格式，也未说明怎样区分证据不足与实际拒绝。 |
| 固定框架来源和 ordinal/稳定物理标识映射 | **框架来源子条件已满足，映射方法未满足。** L73 新增 PyTorch 2.14，可支持可见范围管理，却明确承认不证明 ordinal→UUID；L98 虽列对应表，取证方法仍为可见集＋分配记录，没有获得或关联稳定物理标识的来源与逐行格式。可写 unknown，但不能据未知映射判三单相等。 |

**原 ID 下事实追记：** L70 将 envvar/NVIDIA Runtime 与所宣称的原生 CDI 消费链混接，归 C32 的分配→传递→最终配置条件；不认定 envvar 在所有 CDI 场景都无效，也不新增 ID。

**剩余关闭条件：** 选定一条 GPU 路径，按一次源具体字段连接分配、传递、CDI/最终 OCI 配置，并把其他模式隔开；补三层库身份/版本和证据记录；补权限及 LSM 关联方法；在固定框架/设备身份来源支持下交付逐 ordinal→稳定设备标识核对格式。只要求方法，不要求本次运行；C34 仍单独验收异常与对照。

### B21-C33 — P2 / OPEN

**权威条件：** 第二次复核 L143。**位置：** 正文 L79–83、L119；作者记录 L12、L17；映射 L116；登记 L5237–5247。

| 条件 | 本轮判断与位置证据 |
|---|---|
| Ascend runtime/ref、辅助函数输出与消费实现 | **未满足。** L79 明写 runtime 未选组件/ref、`SetAscendRuntimeEnv` 所在包文件未定位、环境/库挂载白名单与辅助函数输出 unknown。把缺项说得更具体不是完成实现取证；本轮审阅也不替作者补交消费端。 |
| 精确分支条件与具体字段连接两端 | **插件部分保持，定位仍不准确。** §3.2 原文件实读确认 `UseAscendDocker` 判断在 L1161 起；L1087 起是 mountDevice 辅助函数，不是分支判断位置。正文 L79 仍以 L1087–1100 指假分支且没有展开 `DeviceSpec` 字段及到环境辅助函数/runtime 消费端的连接。映射 L116 的“行号精确”没有落页。 |
| 目标组合未知、平台/digest 边界与 ACP 清理 | **这些子条件保持满足。** L42/L81 未从 GPU/CDI 推导 NPU，不把 digest 当兼容证据，目标组合未知明确；L83 没有重新引入 ACP。未知支持交集或未实测本身不是新增阻塞。 |

**剩余关闭条件：** 固定并引用明确 Ascend runtime/ref，定位环境辅助函数实际输出与消费端的节点/环境/库挂载实现，用具体字段连接两端；修正分支判断位置。两个实现的支持交集仍可未建立，不得把不同版本材料拼成兼容组合；本条件是实现取证，不是现场试运行。

### B21-C34 — P1 / OPEN

**权威条件：** 第二次复核 L159。**位置：** 正文 L87–114；作者记录 L13；映射 L117；关联案例 L19–25、L32–40、L82，关联实验的设计/前提/判据章节。

| 条件 | 本轮判断与位置证据 |
|---|---|
| 真实五栏环境模板 | **表格存在子条件已满足。** L89–98 确实交付五栏、八个可填写行，前次“只有声明、没有表”的问题不再重复要求。但宿主硬件/产品形态、镜像与注入库身份未落行；L95 的资源请求数量示例不替代实际分配 ID，L96–98 仍缺最终配置/物理映射的具体证据字段。 |
| 平台分支、映射比较、缺证据判据 | **新增 NPU 行有进展，但判定仍不满足。** L104/L108 保留“任一单缺失且模式已定即失败”，把没有采集证据与已证明漏注入混为一谈；“三单一致”没有稳定身份映射/集合范围。L109 把编号越界归“NPU 访问拒绝”，仅写语义 unknown，并以“持续分叉”作失败；案例支持参数/选择错误，不支持直接判 DAC/LSM 拒绝，合法重编号也可能数值不同。须独立设置“节点在、逻辑选择失败”分支并比较映射，而非编号文本。 |
| GPU/NPU 隔离观测与完成边界 | **未满足。** L106/L110 以“关共享后影响消失”作完成；这只支持该对照现象，不证明设备访问、显存、计算份额或故障域隔离。NPU 仅新增未知概念行，没有实现依据、观测边界或可区分规则。对证据未知的状态，不能同时给无条件技术通过/失败判据。 |
| 基线/变体计划、证据、旁路、授权及恢复 | **部分满足但未交付具体计划。** L112 仍是段落，没有“每变体一行”的计划表或等价逐变体记录块；“主体/时间窗/字段见下”无对应下文。唯一差异、证据定位、旁路检查和未授权设备负向验证的具体前提未展开，digest/版本 pinned 不代替设备身份比较。保持不自动放宽权限/禁用 LSM/重启生产组件的限定是正确的；关联实验可参考但不能抵充本页明确要求的设计。 |
| 案例版本、缺项、未复现属性和分支连接 | **症状摘要保持，其他未满足。** L112 已写物理 0/3/4/7 与逻辑 `[0,4)`，但环境与版本仍推给关联页，没有在本页摘要 torch/torch_npu/vLLM/CANN 等版本、关键 runtime/plugin/驱动/digest 缺项及“非本库复现”。紧跟实验的“未执行”不替代来源案例属性。关联案例自身 L38–40/L82 已有这些限定，不等于本页交付完成。 |
| 两个 NVML 情境、更新/恢复与授权限定 | **NVML 错配未改；其他边界保持。** L105 仍为“NVML Unknown Error（限 Insufficient Permissions 段…）”；官方权限段消息是 Insufficient Permissions，Unknown Error 属于 hook/legacy 访问丢失段。L107 不再把撤销更新等同恢复，L114 保留只设计/不授予执行权，认可这些子条件。 |

**原 ID 下事实追记：** NVML 错配和缺证据即失败是旧问题未消除；L109 新增的逻辑编号/选择错误与权限拒绝混类，以及持续数值分叉即失败，仍归 C34 的异常分支与集合判据，不新增 ID。

**剩余关闭条件：** 保留五栏实表并补缺失的硬件、库身份、分配/最终配置与物理映射证据格式；按 GPU/NPU 的已选模式分别交付注入、权限拒绝、逻辑选择和隔离分支，明确“缺证据→无法判定”，按稳定身份映射比较集合；具体列基线/各变体的唯一差异、主体/时间窗/证据字段、旁路排除、负向验证授权/隔离前提和恢复判据；在本页写案例版本、缺项和非本库复现摘要；真正改正两个 NVML 情境。仍只要求设计，不要求制造输出、放宽安全策略或执行生产生命周期操作。

## 5. Acceptance 与计数

| 计划位置 / acceptance | 本轮结论 | 未关闭的原 ID |
|---|---|---|
| L5403 / 镜像 digest、基础/依赖、构建输入、SBOM/签名与拉取策略的方法和限制 | 部分满足，**未通过**：输入格式进步，SBOM 范围/签名信任/默认缓存方法及状态同步仍不足 | B21-C30 |
| L5404 / 固定 OCI/containerd/runc/Toolkit/CDI，分离宿主、库、设备/环境/挂载、权限和框架映射 | 部分满足，**未通过**：runc 手册和框架来源已补，但错链/版本残留、配置诊断和 GPU 模式链/库身份/映射未闭环 | B21-C31、B21-C32 |
| L5405 / Ascend runtime/plugin 独立固定实现、目标组合及 GPU/NPU 边界 | 部分满足，**未通过**：插件与未知边界保持，辅助函数/runtime 消费端仍未交付 | B21-C33 |
| L5406 / 环境清单、观测/异常分支、对照验证和源案例，不作安装处方 | 部分满足，**未通过**：实表已补，判据/具体对照/案例边界仍缺，NVML 错配未清除 | B21-C34 |

**5 个原发现：0 CLOSED / 5 OPEN（1 P1、4 P2）；4 条 acceptance：0 完整通过 / 4 未完整通过。无新增发现 ID，无优先级调整。** 已认可的子条件不再作为全缺失反复要求；未满足条件仍需作者修订后按新输入摘要定向复核，不能用审阅者补证、结构 PASS 或缺项 unknown 替代正文方法交付。

## 6. 结构校验与单文件写入边界

- 写入前原仓库 `PYTHONDONTWRITEBYTECODE=1 make check`：**PASS：94 content entries / 428 sources**。
- 写入后原仓库 `PYTHONDONTWRITEBYTECODE=1 make check`：**PASS：94 content entries / 428 sources**；报告本地文件链接与行尾空白检查均 PASS。校验只证明结构和本地链接，不证明远程内容、技术结论或环境兼容。
- 为遵守单文件写入约束，将仓库复制到 `/private/tmp/b21-t05-01-recheck-3.f17rhy1t/validation`，排除 `.git`、`.venv`、`.agents`、`.codex` 与缓存；在副本内以原仓库虚拟环境 Python 执行 `make check`、`make build`（禁写字节码），均 **PASS：94 content entries / 428 sources**。只在副本重建知识库 `build/catalog.json`、`build/catalog.md`，没有镜像构建。
- 前后摘要核对：七个主输入不变；除本报告外全部既有 Git 所列 tracked/untracked 非忽略文件摘要相同；原仓库两个 `build/` 文件的摘要清单相同。工作区相对本轮开始只新增本报告，已有作者改动和未跟踪文件均保留。
- 本轮没有修改 `src/kb/` 或测试代码，不需要 `make test`，不为报告新增测试。

**最终技术结论：第三次定向复核不通过，C30–C34 全部保持 OPEN；已披露 curl DNS 失败与只读替代取文限制，未确认实际执行模型元数据，未执行实测。**
