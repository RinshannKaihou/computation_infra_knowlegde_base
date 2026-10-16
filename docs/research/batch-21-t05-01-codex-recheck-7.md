# Batch 21 补交 T05-01 第七次定向复核（作者第七轮修订后）

## 1. 结论、角色与边界

- 日期：**2026-10-14（Asia/Shanghai）**；本机日期同日、时区 `CST / +0800`。
- 执行者：本会话 Codex，独立审阅角色，与作者第七轮修订角色分开；没有另行派发模型。本轮只新增本报告，不改正文、作者记录、修订映射、来源登记、计划、关联条目或历史报告，不提交 Git commit。
- 用户约定配置：`gpt-6.1-sol / xhigh`。**这是用户约定，不是已独立确认的执行元数据。** 本轮未取得可独立核验的实际模型标识或 reasoning 配置，不以模型自述充当确认。
- 范围：仅 **B21-C30–C34**；优先级沿用初审。剩余关闭条件以[第六次定向复核](batch-21-t05-01-codex-recheck-6.md) L83、L95、L109、L122、L136 为权威，对照[初审](batch-21-t05-01-codex-review.md) §6 和[任务验收](../../plans/full-coverage-backlog.yaml) L5403–5406。第七轮映射 L144–150 仅定位落盘改动，不作为关闭证明。
- **结果：1 CLOSED / 4 OPEN；第七次定向复核不通过。** CLOSED：C30（P2）；OPEN：C31、C32、C33（各 P2）、C34（P1）。四条 acceptance：**1 完整通过 / 3 未完整通过**。新修订中的事实/判据问题在所属原 ID 下追记，**不新增发现 ID，不调整优先级**。
- 认可签名固定方法关联与范围同步、runc 证据身份格式、GPU 成分记录格式、CDI 连接链骨架、NPU 逻辑选择/权限拒绝分栏、共享影响解释边界、旁路清单与案例环境摘要等进展；不会将这些已补子条件再判作全缺失。
- 未执行镜像构建/拉取、SBOM 生成/比对、签名/验签、容器启动、设备访问、配置修改、负向/隔离试验或 GPU/NPU 实测。知识库结构检查与临时副本清单生成不是上述实测，也不建立支持交集或硬件验证结论。

## 2. 输入身份与位置口径

用户给出的四个 SHA-256 前缀均匹配；其余三个输入另记录完整摘要。正文等行号均为本轮本地原文件坐标；上游源码行号仅采用 GitHub 连接器的固定 ref 原文件区间，不把网页阅读器行号拼成 GitHub 锚点。

| 输入 | 完整 SHA-256 |
|---|---|
| [正文](../../knowledge/05-cluster-platform/container-image-runtime-baseline.md) | `463e0b75093bc0cc47521b2718e92837362790ec8e3cb15004eef75be53c5db9` |
| [作者来源记录](batch-21-t05-01-sources.md) | `00a6457295faaf8251230781fd51cbc7cc19deebeca955ecf16a6af813978868` |
| [修订映射](batch-21-review-fixes.md)，只取第七轮 L144–150 | `c6369c99aa3061256b079e64d7b4496bfd8b23c77649abecf48de5a21e5d060a` |
| [第六次定向复核](batch-21-t05-01-codex-recheck-6.md) | `2cf46b41b553f93d01b3f2510fabed16f99a1e60c2b127bbb330de9e556b591c` |
| [初审](batch-21-t05-01-codex-review.md) | `341775efc62d7b8d46659c2d272aa31ae301b0cd1db47623ebe86490b80e34b5` |
| [任务验收计划](../../plans/full-coverage-backlog.yaml)，T05-01 L5386–5418 | `5f9bcf865b8c77e13cc8ee5f1c03140c37b86f558d8227d8bb2080249f4fcfc3` |
| [来源登记](../../sources/registry.yaml) | `842d6b25aaa11d75a074054c32e2f171d71f271f10cb3cc4f62d24135bb36c28` |

另读 README、编写指南、内容总目录、元数据 schema、[Ascend 来源案例](../../knowledge/05-cluster-platform/ascend-device-visibility-source-case.md) L32–40 和[待执行实验](../../knowledge/05-cluster-platform/ascend-device-visibility-experiment.md) 的控制条件/旁路/停止/判据章节；关联页只用于核对本页摘要和设计，不重新验收关联任务。登记实计 **436 项**；CLI 三文件位置在登记 L5341、作者记录 L25 和正文 L58 已同步；common 静态输出与未读消费端在登记 L5330–5335 已区分。登记中的历史 `curl 200` 不计为本轮独立请求结果。

## 3. 一次源抽查：执行方法、文字与限制

### 3.1 curl 实际执行

本机 curl **8.7.1**，对下表 01–19 的精确 URL 实际执行只读 GET；03–05 为三个独立请求。保持默认 TLS 校验，未使用 `-k`、替换证书、改 DNS、提权或绕过沙箱。调用形态为：

```bash
curl --location --silent --show-error --connect-timeout 8 --max-time 20 \
  --output "$audit_dir/$name.body" --write-out '%{http_code}' "$url"
```

**19/19：退出码 6、HTTP `000`、`Could not resolve host`；没有取得 curl 响应正文，TLS 握手未发生。** 因而本轮不声称 curl 成功、HTTP 200 或本机验证了远端 TLS 链。诊断和摘要清单仅存临时目录 `/private/tmp/b21-t05-01-recheck-7.wHhngASc/`，未加入知识库。

### 3.2 允许的只读替代通道与文字核对

使用 `web.run` 打开精确页面、定位章节并阅读文字，及 GitHub 只读连接器读取固定 ref 原文件区间/API 对象。下表是**实际文字核对，不只是可达性检查**。CDI SPEC、OCI Linux 配置、Ascend plugin/common 的 raw URL 在网页通道返回 Internal Error，改用 GitHub 连接器成功读到原文件；不将网页通道失败当成源文件不存在。读取到的代码和页面仅作证据，没有执行其命令。

| curl 抽查点 / 精确一次源 | 实际核对文字、范围及用途 |
|---|---|
| 01 / [Kubernetes Images v1.32](https://v1-32.docs.kubernetes.io/docs/concepts/containers/images/) | Image pull policy / Default image pull policy：策略、digest 缓存、对象创建时默认化及后续不自动重设。支持 C30 已有职责分离。 |
| 02 / [syft README@v1.54.1](https://raw.githubusercontent.com/anchore/syft/v1.54.1/README.md) | Features：扫描镜像/文件系统等目标，CycloneDX/SPDX/Syft JSON 等输出；只确认 README 能力范围，未读具体 cataloger/层归属输出实现。用于 C30/C32。 |
| 03–05 / cosign@`11926fa5`：[CLI verify](https://raw.githubusercontent.com/sigstore/cosign/11926fa5bbbbde47e88fc006b625a17769b743b2/cmd/cosign/cli/verify.go)、[verify options](https://raw.githubusercontent.com/sigstore/cosign/11926fa5bbbbde47e88fc006b625a17769b743b2/cmd/cosign/cli/options/verify.go)、[certificate options](https://raw.githubusercontent.com/sigstore/cosign/11926fa5bbbbde47e88fc006b625a17769b743b2/cmd/cosign/cli/options/certificate.go) | 网页文字及 GitHub 原文件 L28–155、L32–165、L22–155：核验入口传递 key/claims/证书选项；check-claims 默认开启；输出选项；keyless identity/issuer 要求。与作者同修订三文件定位一致，用于 C30。 |
| 06 / [containerd CRI config@v2.4.1](https://raw.githubusercontent.com/containerd/containerd/v2.4.1/docs/cri/config.md) | GitHub L15–145、L202–289；网页 Cgroup Driver / Full configuration：v2 配置仍受支持并自动转为 v3；images/runtime 分区、handler/options、CDI 目录和 kubelet cgroup 条件。用于 C31。 |
| 07 / [runc 手册@v1.5.2](https://raw.githubusercontent.com/opencontainers/runc/v1.5.2/man/runc.8.md) | GitHub L35–111 与网页 Bundles / Commands / Global Options：list 按 `--root` 查询，state 入口，`--log` 目标和状态存储 root。用于 C31；不把查询入口当成已采集状态字段。 |
| 08 / [CDI SPEC@cb98bcf6](https://raw.githubusercontent.com/cncf-tags/container-device-interface/cb98bcf66dc68530012483bd56e33e14d815e167/SPEC.md) | GitHub L1–200、L200–265：spec 1.1.0、v1.1.1 无规范变更、kind/name 匹配及容器级/设备级 edits 的不同应用条件；设备号与挂载来源/目标字段。用于 C31/C32/C34。 |
| 09 / [NVIDIA plugin README@v0.20.1](https://raw.githubusercontent.com/NVIDIA/k8s-device-plugin/v0.20.1/README.md) | 配置/Shared Access：cdi-cri 通过 CRI CDIDevices，需 Kubernetes 转发与 engine 支持；UUID/index 不等于框架编号；time-slicing 不隔离显存/故障域。用于 C32/C34。 |
| 10 / [Toolkit 1.20.0 CDI](https://docs.nvidia.com/datacenter/cloud-native/container-toolkit/1.20.0/cdi-support.html) | Running a Workload with CDI / Non-CDI-Enabled Runtimes：qualified 名请求、原生/非原生路径差别与 hook 冲突限定。用于 C32。 |
| 11 / [Toolkit 1.20.0 docker-specialized](https://docs.nvidia.com/datacenter/cloud-native/container-toolkit/1.20.0/docker-specialized.html) | GPU Enumeration / Driver Capabilities：设备选择与挂入的 driver libraries/binaries 是不同变量职责；不据此虚构具体库成分身份。用于 C32。 |
| 12 / [Toolkit 1.20.0 troubleshooting](https://docs.nvidia.com/datacenter/cloud-native/container-toolkit/1.20.0/troubleshooting.html) | NVML permissions / Containers losing access / Affected Environments：Insufficient Permissions 与 hook/legacy Unknown Error 区分；更新包括 CPU/内存限制，部分 systemd 条件另述；label disable 放弃 SELinux 分离。用于 C34。 |
| 13 / [OCI Linux config@92249139](https://raw.githubusercontent.com/opencontainers/runtime-spec/92249139eea7161e13745abd4cb6d0ea02a3227a/config-linux.md) | GitHub L127–151、L402–418：设备节点按 path/type/major/minor 等描述，访问 allow/type/major/minor/access 另列；单个 major 不构成设备身份。用于 C32/C34。 |
| 14 / [PyTorch CUDA notes 2.14](https://docs.pytorch.org/docs/2.14/notes/cuda.html) | Device-agnostic code 的 CUDA_VISIBLE_DEVICES 段管理可用 GPU 范围，不提供本页所需逐 ordinal→稳定物理身份的取证方法。用于 C32。 |
| 15 / [Ascend plugin.go@44385c13](https://raw.githubusercontent.com/Ascend/mind-cluster/44385c13d7b1d87def35f1604e8be4d16de6ca4e/component/ascend-device-plugin/pkg/server/plugin.go) | GitHub L1087–1185：DeviceSpec 的 host/container 路径和 rw；L1161–1169 的 UseAscendDocker 分支与 common 调用。用于 C33。 |
| 16 / [Ascend common.go@44385c13](https://raw.githubusercontent.com/Ascend/mind-cluster/44385c13d7b1d87def35f1604e8be4d16de6ca4e/component/ascend-device-plugin/pkg/common/common.go) | GitHub L90–150：SetAscendRuntimeEnv 的 ID 串/runtime options、310B allow-link、限 !PresetVDevice 的 worker 组。首次误取 L750–840 未命中，随后读取上述正确区间；不把首次区间当作函数证据。用于 C33。 |
| 17 / [vLLM Ascend Issue #2557](https://github.com/vllm-project/vllm-ascend/issues/2557) | Your current environment / Describe the bug：CANN 8.2.RC1、稀疏物理 ID 与选择输入范围错误；支持逻辑选择分叉，不直接证明 DAC/LSM 拒绝。用于 C34。 |
| 18 / [NVIDIA plugin server.go@v0.20.1](https://raw.githubusercontent.com/NVIDIA/k8s-device-plugin/v0.20.1/internal/plugin/server.go) | GitHub L280–430、L430–570 与网页 Allocate/CDI 函数：读取请求 DevicesIds，转换 UUID/index 并去重，再构造 qualified 名、填充 CdiDevices[].Name；另有附加 CDI 请求。用于 C32 的事实追记。 |
| 19 / [Ascend runtime README@44385c13](https://raw.githubusercontent.com/Ascend/mind-cluster/44385c13d7b1d87def35f1604e8be4d16de6ca4e/component/ascend-docker-runtime/README.md) | GitHub 完整 README 和网页“设计简介”：**同一 commit 下确有 ascend-docker-runtime 组件**，说明可见设备变量、设备 cgroup 与库挂载入口；不能据 README 宣告实现链/隔离或兼容已验证。用于 C33。 |

**补充只读核对（不计入十九次 curl）：** cosign [v3.1.3 ref](https://api.github.com/repos/sigstore/cosign/git/ref/tags/v3.1.3) → [tag 对象](https://api.github.com/repos/sigstore/cosign/git/tags/2f3a85b04907df5b770eb049d7e4d08d4b018d86) → commit `11926fa5bbbbde47e88fc006b625a17769b743b2`，与作者定位相符；不据此声称是当前最新版本或已完成镜像验签。另读 runc 同 tag 的 [state 手册](https://github.com/opencontainers/runc/blob/v1.5.2/man/runc-state.8.md)和 [list 手册](https://github.com/opencontainers/runc/blob/v1.5.2/man/runc-list.8.md)，确认 state 的 JSON 输出与 list 格式选项；OCI [config@v1.3.0](https://raw.githubusercontent.com/opencontainers/runtime-spec/v1.3.0/config.md) 作为进程配置入口，权限字段判定主要依据抽查 13。

Ascend [固定 component 目录](https://api.github.com/repos/Ascend/mind-cluster/contents/component?ref=44385c13d7b1d87def35f1604e8be4d16de6ca4e)明确包含 `ascend-docker-runtime`；随后读取[该组件目录](https://api.github.com/repos/Ascend/mind-cluster/contents/component/ascend-docker-runtime?ref=44385c13d7b1d87def35f1604e8be4d16de6ca4e)、runtime 子树和 [runtime/process/process.go](https://github.com/Ascend/mind-cluster/blob/44385c13d7b1d87def35f1604e8be4d16de6ca4e/component/ascend-docker-runtime/runtime/process/process.go) L1–170，确认存在实际 runtime 源码、设备变量别名、hook 路径及驱动库路径定义；也读 `runtime/common/const.go` L1–85，仅作组件身份辅助。两份 runtime raw 源码在网页通道失败，GitHub 原文件读取成功。**未继续审计完整消费/设备/库白名单与 hook 实现，不能将这些入口补读算成作者已交付 C33。** 对 `Ascend/ascend-docker` 的 API 请求确实返回 404，但该结果只能表明所请求名称在本次通道不可解析，不能证明相关组件不存在，更不能推翻同 commit 的目录/文件证据。

关键 GitHub 文件 blob 身份：cosign 三文件分别为 `408c88e8d4759f39b200212c904ffefbf2c8bfff`、`918e226e776d091b1d1ce7c432d1e9351a674833`、`33a2329aafadacee33bacba8044bc2480cdc5edb`；CDI SPEC `2bc480a20ce447f5281b5d6844a486a81bb635b0`；NVIDIA server `9281b48ef52f9eda9cbed6d98491729da85b5a75`；Ascend plugin/common `b7692611b12884854d973fa2a3da18e381353f10` / `6cd038e9f1d67a8a913aa4bb1301692f177b3dbe`；runtime README/process `f612ad6b5d2edcf65d9ad683d57a4f1a4e1f9088` / `acbd7a1ec0703498abfcfcb6ce1aa493069091b1`。blob 不是 commit，也不是现场验证证据。补读来源在本报告保留精确 ref/路径；依本轮单文件约束未改登记，不创造登记 ID，不将审阅者补证冒充作者取证。

## 4. B21-C30–C34 逐项复核

### B21-C30 — P2 / CLOSED

**权威条件：** 第六次复核 L83。**本轮位置：** 正文 L25、L28、L39、L50–59、L140；作者记录 L25；映射 L146；登记 L5341。

- 正文 L58 已在方法附近链接所选 CLI v3.1.3，给出 tag/commit 和同修订三个文件位置；source_refs L25、作者记录 L25、登记 L5341 已同步。抽查 03–05 与 tag 解引用支持该关联，原先“只登记 CLI，正文/作者取证未关联”的阻塞关闭。
- 构建输入格式、SBOM 扫描对象/范围/输出身份与重复比对限制、keyless 身份/issuer 或可信 key、载荷 digest 核对与未执行边界保持；拉取默认化与 kubelet 拉取职责仍分开，抽查 01–02 支持已核对范围。
- summary/notes/待确认不再宣称“没有官方工具取证”，L140 将未知收窄到未读实现、未固定文档修订或未执行结果；保留 unknown 不影响已交付的记录方法。
- 登记 L5346 的旧“核验语义以文档页为准”句仍保留，但本轮 revision L5341、正文及作者记录已经明确固定 CLI 方法依据，不再据这一孤立旧句重复阻塞；本结论不采信未固定文档为当前最新版，也不扩张为全 CLI 实现审计。

**剩余关闭条件：无（本轮范围内）。** 不要求运行 SBOM/验签工具，不要求制造结果或将 draft 改为 reviewed/reproduced。

### B21-C31 — P2 / OPEN

**权威条件：** 第六次复核 L95。**本轮位置：** 正文 L28、L39、L63、L140；作者记录 L10、L26–28；映射 L147。

| 子条件 | 判定与位置证据 |
|---|---|
| containerd 字段级参考格式与生效链 | **部分补齐，仍不足。** L63 新增配置文件路径/摘要、handler 观察入口和不符判据，但仍未给精确 images/runtime 分区键、default/所选 handler、runtime_type、options 完整键及 SystemdCgroup 参考值/条件；L140 继续把完整键列待确认。配置记录没有连接同一 daemon/CRI endpoint、Pod/容器运行身份及对应状态/日志对象。抽查 06 已提供这些分区与 cgroup/RuntimeClass 条件，不要求现场值。 |
| 新增不符判据 | **按 C31 追记需修正。** L63“handler 名不一致或版本头不一致即记配置未生效”把基线差异直接升级为失效，未指定比较的是哪个 Pod 所选 handler。固定 config 文档 L15–20 明说 v2 仍支持并自动转 v3；RuntimeClass 也可显式选择 handler。仅头部或默认/所选 handler 文本差异不足以证明配置没加载，应先区分基线不符、来源/转换/选择差异与有证据的未生效。 |
| runc 身份和证据格式 | **大部分补齐，状态字段仍不足。** L63 已有共同容器 ID、bundle 路径/config 摘要、状态 root、日志对象定位、时间窗和 ID 不符判据，认可这些方法字段，不要求输出。仍仅写“runc list/state 字段”，没有列应保留哪些状态字段及如何与 bundle/config、进程/运行期对应；`--root` 是查询/状态存储作用域，不能代替这组状态内容。抽查 07 和补读 state/list 手册支持该区别。 |
| CDI 身份与已读状态同步 | **满足。** L28/L63 已分仓库 tag v1.1.1、spec 1.1.0、文件 cdiVersion；L140 不再把规范/containerd/runc 正文整体列未读。既有 OCI 双页与 CRI 条件保持。 |

**剩余关闭条件：** 给出所选 v3 模式的精确分区/完整字段键和条件化参考值、实际值/unknown 填写位置；连接配置来源、实际所选 handler、同一次 daemon/CRI/容器身份、状态和日志。将“基线不符”与“未生效”分开，覆盖受支持的配置转换与显式 runtime 选择；列清 runc 所需状态字段及关联规则。保留已补身份/摘要/时间窗/CDI 三层区分；**不要求配置变更或实测，不要求证明整栈兼容**。

### B21-C32 — P2 / OPEN

**权威条件：** 第六次复核 L109。**本轮位置：** 正文 L67–75、L79–83、L104–107；作者记录 L11、L24–25；映射 L148。

| 子条件 | 判定与位置证据 |
|---|---|
| CDI 字段级链 | **骨架新增，连接规则仍不足。** L72 已列 qualified 名格式、CRI CDIDevices、devices[].name、全局/设备级 edits，认可所补环节。仍未交代实际 Allocate 请求 ID 怎样依据 deviceIDStrategy 转换成 CDI 名，以及 response.CdiDevices[].Name→CRI 请求→CDI kind/name 的字段对应；没有按全局与设备级来源把节点/挂载/env 逐项连接最终 OCI 字段。箭头和“逐段记录实际值”不足以给出这种规则，抽查 08/18 已有明确依据。 |
| 新增 Allocate 角色表述 | **按 C32 追记事实纠偏。** L72“Allocate ID 由设备插件按请求数量分配”不符合所选 v0.20.1 实现：Allocate 读取调用方请求 DevicesIds 并校验；随后按 UUID/index 转换、去重，再构造 qualified 名并填 CdiDevices[].Name。Pod 请求数量不是该 ID 的生成规则；插件提供 preferred allocation 与处理 Allocate 也不能混为从数量生成 ID。抽查 18 支持该区别。 |
| 三层库/来源层方法 | **记录格式已有进展，取证关联仍部分欠缺。** L67 已给宿主/注入组件名、版本、来源→目标路径与证据位置；L69 已给镜像/层/SBOM 成分交叉定位并明确层清单不能替代归属，不再判这些格式全缺。仍未固定所选扫描配置/输出中路径与来源层的具体依据或匹配规则，未连接注入组件来源与实际最终挂载证据；仅已读 syft README 不能证明所有输出都有可用的逐库来源层字段，缺项须逐项 unknown。 |
| ordinal/稳定身份与最终对象 | **未关闭。** L75 增加 CDI 名与“最终 OCI 节点主设备号”，但固定 ordinal→UUID 方法仍明确未取源；L79–81 对应表亦缺最终 OCI 对象字段。仅 major 不足以识别设备，须结合节点类型、major/minor、路径/来源及稳定身份；不要求将编号文本直接相等。抽查 13/14 支持这一限制。 |
| 原生模式与权限/LSM | **保持满足。** 不把 envvar/volume-mounts/NVIDIA_VISIBLE_DEVICES 混进所选 cdi-cri 链；L74 继续分节点与许可、关联进程/设备/时间，缺审计事件不自动判允许。不以未实测事件新增阻塞。 |

**剩余关闭条件：** 修正 Allocate 角色表述，在所选 cdi-cri 模式下补请求 ID 转换、qualified 名、插件返回字段、CRI 引用、kind/name 匹配和 edits→最终 OCI 的字段对应记录；补可追溯的成分/层输出依据与实际挂载关联方法。用固定框架/设备身份材料连接 ordinal、分配、CDI、完整 OCI 节点身份，缺实际值可以 unknown，但固定映射方法不能整体缺交。保留已补记录格式、模式和 LSM 限定；**不要求采集现场值或执行负向试验**。

### B21-C33 — P2 / OPEN

**权威条件：** 第六次复核 L122。**本轮位置：** 正文 L17、L39、L87–89、L140；作者记录 L12、L17；映射 L149；登记 L5330–5335。

- **静态输出与范围同步已补：** L87 保留正确 UseAscendDocker 分支、common 静态输出、310B/!PresetVDevice 条件；L140 和登记 L5335 区分已读输出与未读 api 字符串值/消费端库注入、白名单。抽查 15–16 支持，不继续把已读 common 输出整体列为未交付。
- **核心消费链仍未交付：** L87 仍写消费端 ref 未选、设备/环境/库挂载和白名单未取；DeviceSpec/Envs 的生产端输出不能证明消费端按何条件修改最终配置。没有插件/辅助函数具体字段→runtime 消费→最终节点/挂载的对应关系。
- **本轮检索结论按 C33 追记纠偏：** L87 声称在固定 commit 的 device-plugin 同级未定位独立 runtime；实际同级目录就有 `component/ascend-docker-runtime`，且 README 和 runtime/process 源码均可在同 commit 读取（抽查 19 与补读）。`Ascend/ascend-docker` 单独仓库名的 404 不支持“仓库不存在”这一无条件断言，也不能用来说明同级缺少消费实现。这里确认的是固定实现入口存在，**不是替作者完成消费链审计，更不是建立支持交集**。
- L89 的目标组合字段与支持交集 unknown、GPU 不套用 NPU、digest 不证明兼容、ACP 不引入等边界保持满足。

**剩余关闭条件：** 纠正检索范围/404 推论，固定所选实际 runtime/ref（同 commit 已有可读入口）；核对具体设备、环境、库挂载/白名单消费实现和必要 hook，并把插件/common 输出字段连接消费端条件与最终配置；同步作者正文/记录/登记的实际已读范围。支持交集和现场值仍可 unknown，**要求实现取证，不要求安装、试运行或实测**。

### B21-C34 — P1 / OPEN

**权威条件：** 第六次复核 L136。**本轮位置：** 正文 L95–135；作者记录 L13；映射 L150；关联案例 L32–40。

| 子条件 | 判定与位置证据 |
|---|---|
| 环境清单与三单比较范围 | **部分补齐，仍未闭环。** L104 已明确资源数量≠实际 Allocate ID，L109 明确稳定身份归一化、文本/数量一致不足。L105–107 仍主要是容器内采集/框架可见集，未在本清单落实三层库、最终配置对象与稳定设备身份关联。L109 又把“默认/控制节点”释为 CDI 生成/分发位置、“作业节点”释为运行位置，实际前次要求区分的是注入的默认/控制**设备节点**与作业获配设备；机器位置可以记录，但不能替代这种设备集合边界。抽查 08/13/15 支持节点可能含公共/默认项，不能要求三种异构清单直接全等。 |
| NPU 逻辑选择与访问拒绝 | **分栏纠偏满足，未知判据仍未落地。** L118/L119 已拆逻辑选择分叉与 DAC/LSM 拒绝，不再混类；但 L117–119 同时写实现语义 unknown，却仍给“三单齐/映射一致/拒绝消除”式技术完成/失败，没有把缺固定映射/访问语义列为无法确定的必要条件。尤其 L119 完成仅“拒绝消除”，缺同一目标进程受控访问通过与原访问边界恢复。 |
| 共享影响与隔离/恢复 | **GPU 修订基本满足，NPU 访问分支残留。** L115/L120 已明确关共享只是本分支解释完成，不证明显存/计算份额/故障域隔离；L114/L116 已补目标进程访问通过与原边界恢复，认可而不要求结果。剩余是上一行的 NPU 访问判据及三单比较未闭环，不因“只设计”免除设计条件。 |
| 计划、安全与单变量 | **身份/证据/旁路格式新增，关键内容仍不足。** L126–131 已有 Pod UID、容器 ID、PID、快照时间、CDI/config 路径摘要及 privileged/hostPath/人工挂载/默认注入/显式变量清单。变体的注入模式配置键和实际唯一变更字段仍“待填”；“allow 规则/UID/GID”需明确一次只改一项。负向组仅“未请求设备不可见”，未区分公共控制节点、作业设备可见性与未授权设备访问拒绝；“偏离即停/复核三单”没有具体安全停止与恢复访问边界判据。重建容器行“同上”还照搬同容器 ID/PID/快照时刻，须分别记录旧新对象并关联，不能按同 ID 判同一次运行。 |
| hook/legacy 更新对照 | **重建行已加，更新变体仍错配。** L116 的原分支是容器更新导致 hook 注入访问丢失；L130 只回退镜像或驱动、并排除 CPU/内存限制变更，没有针对源文档所述资源更新触发变量。L131 增加重建是进展，但不能让镜像/驱动回退替代资源更新对照，撤销/重建也不自动证明恢复。抽查 12 支持此范围限定。 |
| 案例条件与 NVML 区分 | **满足。** L133 已在本页摘要 CANN 8.2.RC1、框架版本及 runtime/plugin/驱动固件/digest/模式/集群版本缺项，并明确非本库复现；L114 保留 Insufficient Permissions 与 Unknown Error 区分及授权边界。抽查 17 与本地案例支持，不再要求读者仅到关联页寻找环境摘要。 |

**剩余关闭条件：** 补本清单的三层库/实际分配/最终配置/稳定身份关联；区分公共控制设备节点、获配作业设备、资源请求数量与框架逻辑集合，按已取证映射比较对应关系而非全等。NPU 固定语义缺失须进入无法确定判据；访问完成须同一目标进程受控访问及原边界恢复。明确每变体的具体配置键/唯一旧新差异、旧新主体与各自时间窗；区分未请求设备的可见性与未授权作业设备访问负向组，补安全停止/恢复条件，按 hook/legacy 的实际资源更新条件设计对照。保留已补分栏、隔离解释边界、旁路清单、证据格式与案例摘要；**不要求执行这些试验或制造结果**。

## 5. Acceptance 与最终计数

| 计划位置 / acceptance | 本轮判断 | 原 ID |
|---|---|---|
| L5403 / 镜像身份、构建输入、SBOM/签名、拉取方法与限制 | **在定向复核范围内完整通过**；固定 CLI 方法关联和状态同步闭环，方法设计不等于已执行供应链验证 | B21-C30 CLOSED |
| L5404 / 固定 runtime/Toolkit/CDI、各层与映射分离 | 部分满足，**未完整通过**；配置字段/生效关联、ID→CDI→OCI 连接及固定稳定映射仍不足 | B21-C31、B21-C32 OPEN |
| L5405 / Ascend runtime/plugin 独立实现与目标组合 | 部分满足，**未完整通过**；静态范围同步已补，消费实现未交付且同级检索结论须纠正 | B21-C33 OPEN |
| L5406 / 清单、异常/隔离分支、对照与案例，不作安装处方 | 部分满足，**未完整通过**；分栏/恢复限定/案例摘要进步，集合边界、未知判据与安全单变量设计仍不足 | B21-C34 OPEN |

**五个原发现：1 CLOSED / 4 OPEN（OPEN：1 P1、3 P2；CLOSED：1 P2）。第七次定向复核不通过；四条 acceptance：1 完整通过 / 3 未完整通过。** 新修订的配置失效判据、Allocate 角色、Ascend runtime 检索结论和集合/重建对象问题分别在 C31/C32/C33/C34 下追记，不另立 ID。失败不是由于 curl DNS 失败或没有实测，而是作者交付仍未满足对应关闭条件；也不以审阅者补读代替作者应交付内容。

## 6. 结构校验与单文件边界

- 写入前原仓库 `PYTHONDONTWRITEBYTECODE=1 make check`：**PASS：96 content entries / 436 sources**。
- 为遵守单文件约束，复制仓库到 `/private/tmp/b21-t05-01-recheck-7.wHhngASc/validation/`，排除 `.git`、`.venv`、`.agents`、`.codex` 和缓存；副本使用原仓库虚拟环境 Python、禁写字节码执行 `make check` / `make build`，均 **PASS：96 content entries / 436 sources**。只在副本生成 `build/catalog.json` / `build/catalog.md`，原仓库 build 不重建，没有镜像构建。
- 写入后原仓库 `PYTHONDONTWRITEBYTECODE=1 make check`、含本报告的临时副本 `make check` / `make build`：均 **PASS：96 content entries / 436 sources**；报告五项原 ID/优先级/状态和行尾空白核对通过。
- 前后摘要核对：**383 个既有 Git 所列 tracked/untracked 非忽略文件及 build 文件全部不变**，包含七个输入；只新增本报告，原有作者改动和未跟踪文件保留。
- 未改 `src/kb/` 或测试代码，无需 `make test`，不为内容复核报告新增测试。结构检查不验证远程文字/技术正确性，不改变上述技术不通过结论。

**最终技术结论：C30 CLOSED，C31–C34 OPEN；第七次定向复核不通过。curl/替代只读文字核对及执行元数据限制均已披露，未执行实测。**
