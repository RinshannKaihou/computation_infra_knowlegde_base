---
id: cluster-platform.container-image-runtime-baseline
title: 镜像制品、容器运行时与设备暴露基线
type: reference
domain: cluster-platform
status: draft
platforms: [generic]
source_refs:
  - src.oci.image-spec-v1.1.1
  - src.oci.runtime-spec-v1.3.0
  - src.nvidia.container-toolkit-1.20.0
  - src.nvidia.k8s-device-plugin-v0.20.1
  - src.nvidia.framework-containers-user-guide-2026-09-30
  - src.nvidia.ngc-pytorch-25.01-py3-catalog-2026-09-30
  - src.ascend.mind-cluster-v26.1.1
  - src.ascend.device-plugin-pkg-44385c13
  - src.ascend.device-plugin-common-44385c13
  - src.ascend.docker-runtime-44385c13
  - src.ascend.docker-hook-44385c13
  - src.ascend.docker-install-44385c13
  - src.containerd.cri-config-v2.4.1
  - src.cdi.spec-1.1.0
  - src.vllm-ascend.issue-2557
  - src.k8s.images-v1.32
  - src.pytorch.cuda-notes-2.14
  - src.anchore.syft-v1.54.1
  - src.sigstore.cosign-docs
  - src.sigstore.cosign-cli-v3.1.3
  - src.opencontainers.runc-man-v1.5.2
updated_at: "2026-10-14"
summary: 以 OCI 镜像/运行时规范、NVIDIA Toolkit 1.20.0/CDI 与设备插件 v0.20.1、containerd 2.4.1/runc 1.5.2/CDI（仓库 tag v1.1.1/规范 1.1.0）、k8s 拉取策略/torch 可见集/syft/cosign 工具入口为 GPU 样板，昇腾以 MindCluster 固定 commit 的 device-plugin 实现为样板，建立运行环境身份与设备暴露/隔离边界；消费端输出/诊断输出/白名单变体内容与实际结果未取（unknown，白名单源码链已读）。
related_ids:
  - software-stack.framework-backend-adaptation
  - data-storage.artifact-transfer-and-publication
verification:
  status: source_checked
  evidence_refs:
    - src.oci.image-spec-v1.1.1
    - src.oci.runtime-spec-v1.3.0
    - src.nvidia.container-toolkit-1.20.0
    - src.nvidia.k8s-device-plugin-v0.20.1
  notes: "已核对 image-spec annotations/config（构建输入方法层）、runtime-spec config 通用/Linux 字段、Toolkit 1.20.0 安装/CDI/排障/枚举页、设备插件配置策略、Ascend plugin.go 分配/挂载路径、common.go 静态输出字段与 docker-runtime README＋process.go 消费实现、containerd CRI/runc 手册/CDI SPEC/k8s 拉取策略/torch 可见集/syft README/cosign 文档页＋CLI v3.1.3 版本锚；消费端输出/诊断命令输出/白名单变体内容与实际结果未取（unknown，白名单源码链已读）；未执行任何构建/运行实测。"
---

# 镜像制品、容器运行时与设备暴露基线

> 范围：OCI 镜像/containerd 与 NVIDIA Toolkit/CDI、设备插件 GPU 样板，加昇腾 device-plugin 固定实现样板。`generic` 仅为导航聚合；GPU 流程不套用 NPU；镜像 digest 不证明主机/驱动兼容；只记录方法，不宣称已有供应链系统；不得当成已验证安装处方。

## 1. 镜像身份（可填写的记录方法）

| 字段 | 记录方法 | 作用与限制 | 证据位置 |
|---|---|---|---|
| 基础镜像身份 | 镜像 digest（内容寻址）＋媒体类型 | digest 只证内容一致，不证主机/驱动兼容 | [image-spec v1.1.1](https://github.com/opencontainers/image-spec/tree/v1.1.1)（manifest/media-types/descriptor） |
| 构建文件/上下文修订 | 记录构建文件修订（git commit）＋上下文来源（路径/版本）＋上下文内容身份（目录树哈希或清单，无工具则记 unknown）；缺项判据：无修订记录即记缺失；证据定位：构建记录文件路径 | 未固定具体工具不影响格式交付 | 本库记录格式（设计约定） |
| 构建参数与依赖锁定 | 记录参数键值表＋锁文件（名称/哈希）；缺锁文件即记缺失 | 同上 | 同上 |
| 构建工具信息 | 记录工具名＋版本 | 同上 | 同上 |
| 注解 | `.source`/`.revision`/`.base.digest` 等 annotations（键值类型/唯一性等规则含 MUST；特定关系用 SHOULD，非整组 SHOULD） | 选填性注解不等于强制 provenance | [annotations.md](https://github.com/opencontainers/image-spec/blob/v1.1.1/annotations.md) |
| config/history | `diff_ids` 必填，`history` 可选；可复现建议仅针对层 tar 打包/解包，不等于完整构建 provenance | history 存在不等于构建可复现 | [config.md](https://github.com/opencontainers/image-spec/blob/v1.1.1/config.md) |
| subject 引用 | 跨制品引用（SBOM 关联点之一，可选） | 引用存在不等于 SBOM 完整 | [manifest.md](https://github.com/opencontainers/image-spec/blob/v1.1.1/manifest.md) |
| SBOM | 工具：syft v1.54.1（README Features/基础示例：镜像/文件系统成分与包清单、CycloneDX/SPDX 输出；未读全部 cataloger/扫描配置实现，不补写全覆盖能力）；记录对象为所选扫描配置实际扫描的成分记录（含扫描对象 digest、配置范围、输出文件身份）；核对方法：比对两份独立生成的 SBOM，比对字段为包名/版本/来源层，一致只证重复一致（共同漏检不排除），差异逐项处置（漏扫配置差异/新增成分/版本漂移） | 未执行生成与比对 | [syft README@v1.54.1](https://github.com/anchore/syft/tree/v1.54.1) |
| 签名 | 工具：cosign CLI v3.1.3（tag 对象 2f3a85b0，所指 commit 11926fa5）＋文档页（signing overview/verifying）；记录对象为镜像 digest 的签名与透明日志条目；核对方法：`cosign verify`＋预期证书身份/OIDC issuer（keyless）或可信 key（公钥模式）＋载荷 digest 匹配，核验结果（通过/失败＋身份）记入证据；边界：验签通过只证发布身份与未篡改，不证内容正确 | 未执行签名与核验 | [cosign CLI@v3.1.3](https://github.com/sigstore/cosign/tree/v3.1.3)（tag 对象 2f3a85b0→commit 11926fa5；核验入口 `cmd/cosign/cli/verify.go` L1–220、选项 `cmd/cosign/cli/options/verify.go` L1–195、`options/certificate.go` L1–155；命令输出未取）＋[cosign signing overview](https://docs.sigstore.dev/cosign/signing/overview/)（签名流程）/[verifying](https://docs.sigstore.dev/cosign/verifying/verify/)（Keyless/Local 核验） |
| 拉取策略 | 选定 Kubernetes→CRI 路径：`imagePullPolicy`（Always：每次启动先解析 digest 再决定复用缓存或下载；Never：禁止拉取；IfNotPresent：本地存在则复用）与对象创建时默认化规则（digest/非 latest tag 默认 IfNotPresent，latest/无 tag 默认 Always；默认化是 API server 侧字段填充，kubelet 按已设置策略执行拉取）；须保存镜像 digest＋拉取时间＋策略实际值＋缓存命中/实际下载事实 | tag 可变；digest 只固定内容 | [k8s Images v1.32](https://v1-32.docs.kubernetes.io/docs/concepts/containers/images/) |

## 2. GPU 样板：版本基线与层间机制

版本基线：containerd v2.4.1（tag 对象 e24870ce，所指 commit f2551031；CRI 配置见 [config.md](https://github.com/containerd/containerd/blob/v2.4.1/docs/cri/config.md)：版本头 `version = 3`、运行时/镜像插件分区（含运行时分区 `cdi_spec_dirs`＝`/etc/cdi`、`/var/run/cdi`）、runc options 含 `SystemdCgroup`；配置/状态/日志诊断方法（所选 v3 模式记录清单，逐项“完整键｜来源限定参考值｜实际值或 unknown｜证据”）：`version = 3`（v2 仍受支持并自动转 v3）；`plugins.'io.containerd.cri.v1.images'`（`snapshotter='overlayfs'`、`disable_snapshot_annotations=true`、`max_concurrent_downloads=3`、`use_local_image_pull=false`）；`plugins.'io.containerd.cri.v1.runtime'`（`enable_selinux=false`、`disable_cgroup=false`、`disable_apparmor=false`、`device_ownership_from_security_context=false`、`cdi_spec_dirs=['/etc/cdi','/var/run/cdi']`）；`plugins."io.containerd.cri.v1.runtime".containerd`（`default_runtime_name='runc'`）；`plugins."io.containerd.cri.v1.runtime".containerd.runtimes.<handler>`（`runtime_type='io.containerd.runc.v2'` 等，handler 名待填）；`plugins."io.containerd.cri.v1.runtime".containerd.runtimes.<handler>.options.SystemdCgroup`（条件化参考值：systemd 主机用 `= true`，并配 kubelet `cgroupDriver: systemd`（手动）或 `KubeletCgroupDriverFromCRI` 自动探测（v2.0+；runc 类须统一，否则行为不可预期）；非 systemd 主机另行取值，unknown）；Pod `.spec.runtimeClassName`→RuntimeClass `.handler`→上表 handler 名。实际值未采则记 unknown，不以 unknown 代替本清单。关联链：配置来源（文件路径/摘要）→daemon/CRI endpoint→Pod 所选 handler（`runtimeClassName`/默认）→容器身份→有效状态/日志对象。判据分两档：确证不符（已取得实际生效对象且与所选配置冲突）记未生效；未采到对象/日志记无法确定，不从无记录推定失效。仅版本头或默认/所选 handler 文本差异记基线不符（固定 config 文档：v2 仍受支持并自动转 v3；RuntimeClass 可显式选择 handler））、runc v1.5.2（所指 commit 29dd3dc2；手册页见 [man/runc.8.md](https://github.com/opencontainers/runc/blob/v1.5.2/man/runc.8.md)：bundle `config.json`、状态/进程/事件入口、debug/log/root 及 systemd cgroup 选项；配置—状态—日志对应记录为：同一容器 ID 下 bundle 路径/`config.json` 摘要→状态查询（`runc state <id>` 输出 JSON：`ociVersion`/`id`/`pid`/`status`/`bundle`/`rootfs`/`created`/`annotations`，见同 tag [`state.go`](https://github.com/opencontainers/runc/blob/v1.5.2/state.go)（状态对象构造、stopped 置零 PID）/[`list.go` L1–82](https://github.com/opencontainers/runc/blob/v1.5.2/list.go)（JSON 字段、`--root` 查询作用域）；`runc list` 按 `--root` 查询，`--root` 只定查询/存储作用域，不代替状态内容；stopped 状态 PID 置零，不把所有状态的 PID 当活进程身份。关联规则：同一容器 ID 下 bundle 路径/`config.json` 摘要→状态字段→日志对象，附观察时间窗；输出未取则记 unknown）→日志采集（`--log` 对象定位），附观察时间窗；命令输出未取，unknown；不符判据：三处容器 ID 不一致即记非同一次运行）、CDI 规范 1.1.0（仓库 tag v1.1.1 所指 commit cb98bcf6，[SPEC.md Version](https://github.com/cncf-tags/container-device-interface/blob/cb98bcf66dc68530012483bd56e33e14d815e167/SPEC.md#version) 自述 1.1.0；区分仓库 tag、spec 版本、实际 CDI 文件 `cdiVersion` 三层身份）、Toolkit 1.20.0（安装示例固定包版本 `1.20.0-1`）。OCI 通用运行时字段见 [`config.md`](https://github.com/opencontainers/runtime-spec/blob/v1.3.0/config.md)（tag v1.3.0；进程身份/AppArmor/SELinux 字段），Linux 字段见固定 [`config-linux.md`](https://github.com/opencontainers/runtime-spec/blob/92249139eea7161e13745abd4cb6d0ea02a3227a/config-linux.md)（既有登记 commit 92249139），禁止拼成未经支持的组合。summary 中"containerd 分支"指 v2.4.x 主线 tag 定位，见登记。

| 层 | 机制（分开） | 证据位置 |
|---|---|---|
| 宿主内核与驱动 | 容器使用宿主内核（S10 §1.1）；宿主驱动须先安装（Toolkit 先决条件）；"透传"指运行时把宿主侧用户态驱动组件挂入容器，**不是**把内核驱动搬入镜像；宿主/注入组件记录格式：组件名/版本/宿主来源路径→容器目标路径/证据定位（驱动版本与库路径待采集，未取则记 unknown） | [安装指南](https://docs.nvidia.com/datacenter/cloud-native/container-toolkit/1.20.0/install-guide.html)；框架指南 §1.1（复用登记） |
| 注入的驱动组件 | Driver Capabilities：`NVIDIA_VISIBLE_DEVICES` 控制 GPU 选择，`NVIDIA_DRIVER_CAPABILITIES` 控制挂入容器的 driver libraries/binaries | [docker-specialized](https://docs.nvidia.com/datacenter/cloud-native/container-toolkit/1.20.0/docker-specialized.html)（GPU Enumeration 与 Driver Capabilities 两节分开引用） |
| 镜像自带库 | NGC 目录样板：25.01-py3 可见十条层记录、Signed 标记、build id/ref（只读可见层，未拉取/验签）；镜像内 CUDA/框架库的名称/版本/路径/来源层记录方法：以层记录＋`diff_ids` 对应＋ annotations 为方法，留存格式为层清单文件（层号/digest/diff_id/annotations 逐行对应）；具体库归属方法：镜像 digest→层清单→所选扫描配置 SBOM 输出（包名/版本/路径/来源层字段，以实际输出为准；仅 README 已读不能证明逐库来源层字段全有，缺项逐项记 unknown）→注入组件宿主来源路径→最终挂载配置→容器目标路径，三段串成可追溯记录；未执行则记 unknown，不以层清单代替逐库归属 | src.nvidia.ngc-pytorch-25.01-py3-catalog-2026-09-30（复用；只读目录层） |
| 分配 ID→注入通道 | 选定 CDI 原生路径为样板链：请求 `nvidia.com/gpu` → Toolkit 生成 CDI 条目 → container engine 按 CDI 消费 → 设备节点/挂载落位；deviceListStrategy（如 envvar）与 deviceIDStrategy（如 uuid）只决定"分配了什么、以什么形式给容器"，**均不是框架设备编号映射** | [CDI 支持页](https://docs.nvidia.com/datacenter/cloud-native/container-toolkit/1.20.0/cdi-support.html)（原生/非原生路径、engine/CRI 条件）；[设备插件 README 配置节](https://github.com/NVIDIA/k8s-device-plugin/tree/v0.20.1) |

样板链实例（CDI 原生路径，字段级连接规则，非实测）：Pod 请求 `nvidia.com/gpu: 1`（Allocate 读取调用方请求 DevicesIds 并校验 `ValidateRequest`；随后按 deviceIDStrategy（UUID 取 ID/index 取序号）转换、去重，再构造 qualified 名并填 `CdiDevices[].Name`；请求数量不是 ID 生成规则，插件 `GetPreferredAllocation` 为优选分配，不混为 ID 生成）→ Toolkit 生成 CDI 条目（`kind` 标识条目类型，devices[].name 命名设备）→ container engine 按 CDI 消费（`cdi-cri` 经 CRI `CDIDevices` 字段引用 qualified CDI 名）→ devices[].name 匹配→匹配：qualified 名的 kind 与 devices[].name 一起对应（仅 name 不足）；全局 edits 在该 spec 任一设备被请求时应用，设备级 edits 只在对应设备被请求时应用。落位：`deviceNodes`（路径/类型/设备号/权限）→最终 OCI Linux 节点 `linux.devices[]`，许可另列 `linux.resources.devices[]`（节点与许可是不同对象）；mounts 按 hostPath→source、containerPath→destination；env→`process.env`。`cdi-annotations` 路径经注解触发、`cdi-cri` 路径经 `CdiDevices[].Name` 引用，消费端支持为前提。实现引用：[`server.go` L280–438/L448–481 @v0.20.1](https://github.com/NVIDIA/k8s-device-plugin/blob/v0.20.1/internal/plugin/server.go)（读取/校验 DevicesIds→策略转换去重→qualified 名→填 `CdiDevices[].Name`）。连接规则：Allocate ID（插件实际分配值，待采集，请求数量≠ID）→qualified CDI 名（`<domain>/<kind>=<name>` 格式，实际名待采集）→CRI `CDIDevices` 项→`devices[].name` 匹配→全局 containerEdits＋设备级 containerEdits→最终 OCI 节点/挂载；链上每段的实际值须逐段记录，未记录段记 unknown。`envvar`/`volume-mounts`/`NVIDIA_VISIBLE_DEVICES` 属其他传递路径，不混入本链。
| CDI 路径 | Toolkit 自动生成 CDI、原生 CDI 与非原生 runtime 路径三分；MIG 重配/驱动移除刷新限制、hook 冲突提示；规范身份见版本基线（仓库 tag/规范 1.1.0/文件 cdiVersion 三层） | [CDI 支持页](https://docs.nvidia.com/datacenter/cloud-native/container-toolkit/1.20.0/cdi-support.html)；[SPEC.md Version](https://github.com/cncf-tags/container-device-interface/blob/cb98bcf66dc68530012483bd56e33e14d815e167/SPEC.md#version) |
| 权限 | 设备节点（`path/type/major/minor/fileMode/uid/gid`）与访问许可（`allow/type/major/minor/access`）分开记录；容器进程 UID/GID/附加组按 OCI `uid`/`gid`/`additionalGids` 记录；LSM 关联方法：记录策略类型（AppArmor profile/SELinux label，见 runtime-spec 字段）、拒绝事件（audit/AVC，命令输出未取，unknown）、进程/设备/时间三元组；证据不足与实际拒绝的区分：无拒绝事件只记"未见拒绝"，不判"已允许"；可见性证据只支持可见性判断，访问判断须许可证据 | [runtime-spec config-linux.md](https://github.com/opencontainers/runtime-spec/blob/92249139eea7161e13745abd4cb6d0ea02a3227a/config-linux.md)（Devices L127–151、Allowed list L402–417）；[config.md User 节](https://github.com/opencontainers/runtime-spec/blob/v1.3.0/config.md) |
| 框架映射 | 框架可见编号→所选物理设备的映射记录方法：以分配 ID＋注入通道＋限制 GPU 暴露段为准；PyTorch 侧以 `CUDA_VISIBLE_DEVICES` 可见集管理为方法（只定可见范围，不给 ordinal→UUID 证明）；稳定物理标识映射方法（未交付，unknown）：需固定框架/设备身份材料完成可见集快照→分配 ID/CDI 名→完整节点（类型＋major/minor＋路径/来源）→稳定身份（UUID）的关联规则；仅 major 或数量/编号文本不构成稳定对应，缺规则时记无法确定；NPU 侧映射方法未取源（unknown）；无法确定物理对应时明确 unknown | 分配策略见上；暴露段见框架指南 §5.9（复用登记限定；该节只说明限制暴露，不定义 ordinal→UUID/物理映射）；[PyTorch CUDA notes 2.14](https://docs.pytorch.org/docs/2.14/notes/cuda.html) |

逐 ordinal 核对表（空表由读者填写）：

| ordinal | 可见集快照 | 分配 ID | CDI 名/传递字段 | 物理标识（UUID，未取源） | 最终 OCI 节点（类型/major/minor/路径） | 证据定位 | 判定（规则缺失时记无法确定，不记一致） |
|---|---|---|---|---|---|---|
| 待填 | 待填 | 待填 | 待填 | unknown | 待填（仅 major 不足，须类型＋major/minor＋路径/来源） | 待填 | 一致/待查/无法确定（规则缺失时只记无法确定） |
| 插件前置版本 | 设备插件配置示例要求前置版本（README 内 `v0.17.1` 残留为例，实际以 v0.20.1 tag 为准）；failOnInitError 初始化失败行为 | [README@v0.20.1](https://github.com/NVIDIA/k8s-device-plugin/tree/v0.20.1) |
| 共享与隔离 | time-slicing 只解决共享计数（replicas），**不提供工作负载隔离**；cgroups/namespaces 不能充当显存/计算份额/故障域隔离验证 | 同上（Shared Access 节）；隔离验证见 §4 |

## 3. 昇腾样板（独立取证）

组件/ref：MindCluster 固定 commit（既有登记）下 `component/ascend-device-plugin`——发现/健康检查/分配职责见 [README](https://github.com/Ascend/mind-cluster/blob/44385c13d7b1d87def35f1604e8be4d16de6ca4e/component/ascend-device-plugin/README.md)；分配/返回配置两条路径见 [plugin.go](https://github.com/Ascend/mind-cluster/blob/44385c13d7b1d87def35f1604e8be4d16de6ca4e/component/ascend-device-plugin/pkg/server/plugin.go)（分支判断在 L1161–1169：`UseAscendDocker` 为假走 mountDefaultDevice/mountDevice，被调挂载函数体 L1087–1100；为真调 `common.SetAscendRuntimeEnv` L1168；辅助函数输出见 [common.go](https://github.com/Ascend/mind-cluster/blob/44385c13d7b1d87def35f1604e8be4d16de6ca4e/component/ascend-device-plugin/pkg/common/common.go)（设备 ID 逗号拼接、runtime options、310B allow-link、worker 环境组；`!PresetVDevice` 条件；环境变量字符串值为兄弟 api default_name.go 定义（见上链），runtime 库注入语义未核对，unknown）；Allocate 调用链见 L1296 起（完整链未审计，unknown）。对应 runtime 消费端：同 commit `component/ascend-docker-runtime`，两条互斥路径分开记录（纠正前轮拼接错误）。路径 A（插件原生挂载，`UseAscendDocker=false`）：`mountDefaultDevice`＋`mountDevice`（plugin.go L1087–1100）直接返回 `DeviceSpec{HostPath, ContainerPath, Permissions: rw}`；该分支**不调** `common.SetAscendRuntimeEnv` 即 return，其 DeviceSpec 的真正消费端实现未取（unknown，不把 ascend-docker-runtime 的函数当作既定下一跳，不把 `rw` 改写为 `rwm`）。路径 B（ascend-docker，`UseAscendDocker=true`，本文选定路径）：插件调 `common.SetAscendRuntimeEnv`（L1168；字段级条件见 common.go L107–121：ID 逗号串与 runtime options 无条件写入，allow-link 写入仅当 `RealCardType==Ascend310B`（插件侧条件，不覆盖 hook 侧：hook 仍解析该键，空按 False 处理并传入 `--allow-link`），worker 环境组 7 键仅当 `!PresetVDevice`（common.go：`MsLocalWorkerEnv`/`MsWorkerNumEnv`/`PtWorldSizeEnv`/`PtLocalWorldSizeEnv`/`TfWorkerSizeEnv`/`TfLocalWorkerEnv`＝`Itoa(len(devices))`，`PtLocalRankEnv`＝`localRankStr(len)` 即 `0,1,…,n-1` 逗号串）。默认设备表 `GetDefaultDevices`：`davinci_manager`（310B 先试 `davinci_manager_docker`）＋`hisi_hdc`＋`devmm_svm`（存在才加）＋200RC 条件集＋`dvpp_cmdlist`（存在才加）＋200SoC 条件集＋310B 条件集）写 Allocate `Envs`→runtime `processDevicesAndHooks` 读可见变量（空/`void`→仅跳过设备/hook 注入分支）→非空解析→`addHook`（prestart `ascend-docker-hook`）＋`addDevice`（`/dev/davinci*`＋芯片相关 manager/UB，`addDeviceToSpec` 写节点＋cgroup allow `rwm`）→最终 OCI `linux.devices[]`＋`linux.resources.devices[]`＋`process.env`（`LD_LIBRARY_PATH` 仅改 env，非库挂载）。hook 可执行行为见 [hook/process/process.go](https://github.com/Ascend/mind-cluster/blob/44385c13d7b1d87def35f1604e8be4d16de6ca4e/component/ascend-docker-runtime/hook/process/process.go)（`DoPrestartHook`：stdin 读容器状态→bundle `config.json`→env；可见变量空即返回；`RUNTIME_MOUNTS` 默认 `base`；`<configDir>/<name>.list` 白名单（**每份 `.list` 扫描行数上限 128**，计数在路径/stat/分类之前，非合并挂载总数；仅常规文件/目录入选）；UB 挂载项（存在才加）；options 仅 `NODRV`/`VIRTUAL`；allow-link 仅 True/False；`--options` 仅 parsedOptions 非空才加入 CLI 参数；终 `syscall.Exec` 调 `ascend-docker-cli`；实际挂载结果与 CLI 行为未执行（unknown）；所选路径设计条件（所选示例基线，非部署断言，实际值未采则记 unknown）：`UseAscendDocker=true`＋options 为空＋mount group `base`＋默认安装分支（无 `--install-type`，即默认 5 项源列表；产品变体内容未读）＋芯片示例 310B（`addAscend310BManagerDevice` 路径；其他芯片走对应分支，见下）＋`PresetVDevice=false`（所选假设，worker 组写入待采确认）。卡类型两端来源（连接 unknown，待采）：插件侧 `ParamOption.RealCardType`（启动参数/配置来源，值待采）vs runtime 侧 dcmi `GetChipName()`→`GetDeviceTypeByChipName`，两者一致性无出处，不互证。分支条件表（310B 示例）：`addAscend310BManagerDevice` 14 项为尝试项（失败仅警告，不保证全成功）＋`davinci_manager_docker` 不存在则回退 `davinci_manager`；非空非 910A5 另尝试 `dvpp_cmdlist`；UB 受目录/条目存在条件限制（`addUBDevice` stat 门控，跳过子目录）；`addManagerDevice` 另按 `GetProductType` 分支（Atlas200ISoc/Atlas200 与其他）。完整节点/许可/环境逐段对应表（所选示例基线：产品形态示例＝310B 推理卡＋默认安装分支＋options 空＋base 组＋PresetVDevice=false 假设＋输入 ID 设计形式为整数 ID 数组（值待采）；两端卡型来源不互证）。所选辅助候选集合：310B manager 14 项（`svm0`/`ts_aisle`/`upgrade`/`sys`/`vdec`/`vpc`/`pngd`/`venc`/`log_drv`/`acodec`/`ai`/`ao`/`vo`/`hdmi`）＋`davinci_manager_docker`→不存在回退 `davinci_manager`（容器目标重命名为 `davinci_manager`）＋非空非 910A5 尝试 `dvpp_cmdlist`＋UB（`uburma`/`ummu` 目录存在＋跳过子目录＋`hccl_rootinfo.json`/`topo`存在才加）；worker/控制环境键生成规则（`SetAscendRuntimeEnv`：ID 逗号串/options 无条件，allow-link 按卡，worker 组 7 项按 `!PresetVDevice`，计数取输入长度，local-rank 有生成函数）：输入 ID 数组→插件（RealCardType 值待采；`SetAscendRuntimeEnv` 三条件）→env→runtime（dcmi 芯片＝310B 示例→`addAscend310BManagerDevice` 14 尝试项（失败仅警告，不保证全成功）＋`davinci_manager_docker` 不存在回退 `davinci_manager`＋非空非 910A5 尝试 `dvpp_cmdlist`＋UB stat 门控（不存在跳过，跳过子目录）；310B 提前返回不进 GetProductType）→节点（`addDeviceToSpec`：`oci.DeviceFromPath` 取信息失败返回 error；`addDevice` 对作业 davinci/UB/manager 失败继续返回，不等同跳过）/许可（cgroup allow `rwm`，按序应用）/env（ID 串/options/条件化 allow-link/worker 组）＋条件化 poststop（仅 VdeviceID!=-1；`mountDefaultDevice`/`mountDevice`仅属未选路径 A）。失败/跳过语义（按对象分别表述）：节点取信息失败（`DeviceFromPath`）＝返回 error；作业 davinci 失败＝直接返回错误；UB/manager 失败＝`Errorf` 后返回；仅 310B 14 辅助项与 dvpp 等特定分支＝警告后继续；hook 列表源 stat 失败/CLI 失败＝跳过或返回非零。挂载成功判据：CLI 成功返回＋目标可达均不单独证明挂载，须来源-目标关联记录（宿主源路径→CLI 目标→容器内同路径三方一致）为准：（`SetAscendRuntimeEnv` 三条件见上）→runtime（dcmi `GetChipName`=310B 示例→`addAscend310BManagerDevice` 14 尝试项＋回退＋dvpp_cmdlist 尝试＋UB stat 门控；310B 提前返回不进 GetProductType）→节点（宿主路径→类型/主次号→`spec.Linux.Devices`）/许可（cgroup allow `rwm`，按序应用）/env（ID 串/options/条件化 allow-link/worker 组）＋条件化 poststop（仅 VdeviceID!=-1）：芯片类型（`GetChipName`→`GetDeviceTypeByChipName`：310B→`addAscend310BManagerDevice`；910A5→`hisi_hdc`；默认→`devmm_svm`＋`hisi_hdc`）/VIRTUAL（输入 options 已含 VIRTUAL→`addHook` 内提前返回；`addDevice` 内 VIRTUAL→`vdavinci` 为另一独立判断）/非 VIRTUAL（`addHook` 仍调 CreateVDevice，仅 VdeviceID!=-1 才改设备列表/options＋poststop destroy hook；**options 为空仅排除 VIRTUAL 提前返回，不排除 CreateVDevice 返回有效 ID 后的 vdevice/poststop 路径**）。白名单完整链（纠正前轮“固定树未见”说法）：源码 [`build/scripts/base.list`](https://github.com/Ascend/mind-cluster/blob/44385c13d7b1d87def35f1604e8be4d16de6ca4e/component/ascend-docker-runtime/build/scripts/base.list)（5 项：driver `lib64`/`include`、`dcmi`、`npu-smi`、`queue_schedule`）及 5 产品变体（`base.list_A500/A200/A200ISoC/A500A2/A200IA2`，内容未读，unknown）→[`run_main.sh`](https://github.com/Ascend/mind-cluster/blob/44385c13d7b1d87def35f1604e8be4d16de6ca4e/component/ascend-docker-runtime/build/scripts/run_main.sh) 按 `--install-type` 选择复制为配置目录 `base.list`（chmod 440；A500A2/A200IA2 另 `add_so` 按 OS 追加库；`--install-scene` 分 docker/containerd/isula 注册 daemon.json/config.toml）→hook 读 `.list` 候选→CLI [`u_mount.c`](https://github.com/Ascend/mind-cluster/blob/44385c13d7b1d87def35f1604e8be4d16de6ca4e/component/ascend-docker-runtime/cli/src/u_mount.c)（`MountFile`/`MountDir`：目标＝rootfs＋源路径，`bind` 后 `remount ro,nosuid`；`NODRV` 时跳过全部挂载）→容器目标路径；实际挂载结果未执行（unknown）。所选组：默认 `base`（5 项逐项对应记录，身份/版本/挂载结果待采）：①宿主 `/usr/local/Ascend/driver/lib64`（目录候选；hook 入选记录的仅是父目录存在条件，不是逐库分类）→CLI `MountDir`→目标 rootfs＋同路径；目录内逐库待采（采样依据＝部署后目录清单逐库枚举，非 hook 分类；记录字段＝库文件名/版本/CLI 目标路径/挂载结果，缺则记 unknown 并注缺采样；挂载成功以 CLI 返回＋目标可达为准，未执行）；②`driver/include` 同①规则；③`/usr/local/dcmi` 同①规则；④`/usr/local/bin/npu-smi`（文件候选）→hook 入选（常规文件存在）→CLI `MountFile`（先建目标占位）→目标同路径；⑤`/var/queue_schedule` 同①规则。通用规则：源不存在可跳过，校验/挂载可失败（u_mount.c）；`NODRV` 时全部跳过。产品变体 5 份内容未读，unknown）。口径：机制/常量/白名单源码与消费规则已读；所选逐库记录未交付 filled 值；现场挂载结果未执行。`Ascend/ascend-docker` 独立仓库名 404 仅为该名称不可解析。环境键完整链（纠正前轮 vendored 说法）：`pkg/common/constants.go` 别名→`device-plugin/go.mod` replace 至兄弟目录 `../ascend-common`→同提交 `component/ascend-common/api/default_name.go`（docker runtime 段）：`ASCEND_VISIBLE_DEVICES`/`ASCEND_RUNTIME_OPTIONS`/`ASCEND_RUNTIME_MOUNTS`/`ASCEND_ALLOW_LINK`（另 `ASCEND_VNPU_SPECS`）、配置目录 `/etc/ascend-docker-runtime.d`。消费实现见 [README 设计简介](https://github.com/Ascend/mind-cluster/blob/44385c13d7b1d87def35f1604e8be4d16de6ca4e/component/ascend-docker-runtime/README.md)（OCI 插件、runc 前 prestart-hook、按 `ASCEND_VISIBLE_DEVICES` 挂载 NPU、Host 配置 device cgroup 隔离、Host CANN 库挂载）与 [process.go](https://github.com/Ascend/mind-cluster/blob/44385c13d7b1d87def35f1604e8be4d16de6ca4e/component/ascend-docker-runtime/runtime/process/process.go)（`DoProcess`/create 改写 bundle `config.json`；`checkVisibleDevice` 解析可见变量 nominal/range/`void` 为空；`addDevice` 落 `/dev/davinci*`＋manager/ub 设备；`addDeviceToSpec` 写 cgroup allow `rwm`；`addAscendLibraryPath` 仅改写 `process.env` 的 `LD_LIBRARY_PATH`（检查宿主 `lib64/common`＋`lib64/driver` 存在即前置，不是添加库挂载；所选逐库记录与现场挂载结果未取，unknown，通用来源/消费规则见白名单链，不代替逐库记录）；prestart `ascend-docker-hook`/poststop destroy hook）。条件链（所选分支）：`VIRTUAL` 检查先提前返回（与后续 CreateVDevice 不串为同一链）；未提前返回才调 CreateVDevice 并检查返回 `VdeviceID`（`!=-1` 时改写设备列表/options＋poststop destroy hook）。可见变量为空/`void`→仅不进入该作业设备/hook 注入分支（`addHook`/`addDevice` 在设备集非空条件内）；其余 env/`LD_LIBRARY_PATH`/DP-mounts 处理独立，不因无设备推定无任何挂载。非空解析→`addHook`＋`addDevice`（`/dev/davinci*`＋芯片相关 manager/UB 设备，cgroup allow `rwm`）。连接：插件 `SetAscendRuntimeEnv` 输出 ID 串/options→runtime 按可见变量解析→设备节点＋cgroup＋环境＋hook 落最终 OCI；api 实际键/所选产品/manager/UB 条件与最终节点/许可逐字段关联（缺则记 unknown）；vdevice 切分/dcmi 完整实现未审计（unknown，白名单源码链见上）；设备节点/环境/库挂载的白名单变体内容与实际结果未取（unknown，白名单源码链见上；`common.SetAscendRuntimeEnv` 定位到 `pkg/common/common.go`，其静态实现输出字段为设备 ID 逗号拼接、runtime options、310B 下 allow-link、worker 环境组，环境变量字符串值为兄弟 api default_name.go 定义（见上链）；runtime 库注入语义未核对，unknown）。

目标组合字段：产品形态、OS/内核、驱动/固件、runtime/plugin、CANN/框架、镜像身份——均须逐项固定支持材料；当前除 device-plugin 实现外均未建立支持交集（unknown），不得从 GPU/CDI 路径推导。既有[设备链条](device-resource-chain.md)可作入口，但本基线选择的 Ascend 分支即上述固定 commit 与未知条件。

MindIO ACP 与设备暴露无关，本页不引用（此前草稿误列，已删除）。

## 4. 最小环境清单、异常分支与对照验证（只设计不执行）

可填写清单（空表由读者填写；每行格式为"字段 | 期望 | 实际 | 证据定位 | 缺失解释"）：

| 字段 | 期望（示例） | 实际 | 证据定位 | 缺失解释 |
|---|---|---|---|---|
| 镜像 digest | `sha256:…`（固定） | 待填 | 镜像清单/拉取记录 | 未记录即缺失 |
| 基础镜像/构建信息 | 基础 digest＋构建修订 | 待填 | 构建记录 | 同上 |
| 宿主内核/驱动 | 版本号（GPU：`nvidia-smi`/驱动版本；NPU：驱动/固件版本，未取源，unknown） | 待填 | 节点记录 | 未记录即缺失 |
| 宿主硬件/产品形态 | 机型/加速卡型号/数量 | 待填 | 节点记录 | 未记录即缺失 |
| runtime/plugin/CDI 模式 | 如 CDI 原生＋CDI 文件版本 | 待填 | 运行时配置 | 同上 |
| 请求/分配设备 | 资源请求（资源名＋数量，如 `nvidia.com/gpu: 1`，数量≠Allocate ID）＋实际 Allocate ID（待采集，未取则记 unknown） | 待填 | 编排请求/插件状态 | 未记录即缺失 |
| 最终节点/挂载/环境 | 设备路径/变量实测值＋最终配置对象/摘要（bundle `config.json` 摘要） | 待填 | 容器内采集＋配置对象 | 未记录即缺失 |
| 宿主/注入库关联 | 宿主来源路径→最终挂载配置→容器目标路径＋版本 | 待填 | 挂载配置/库路径 | 未记录即缺失 |
| 稳定身份关联 | 分配 ID→CDI 名→最终节点→稳定身份（UUID）对应表 | 待填 | 三方记录 | 无法确定写 unknown |
| 进程身份/访问策略 | UID/GID/附加组/allow 规则 | 待填 | OCI 配置/审计 | 同上 |
| 框架映射 | 可见编号→物理标识对应表（含镜像内 CUDA/框架库名称/版本/路径/来源层） | 待填 | 框架可见集＋分配记录＋稳定身份（UUID，未取源） | 规则未交付→无法确定（缺方法，当前状态）；规则已交付但样本缺项→无法确定（缺采样），注明缺项 |

异常分支表（观测→候选解释→所需证据→受控对照→解释边界→停止/完成/无法判定）。三单对象范围：请求集＝编排侧资源请求（含请求数量与资源名）；分配设备＝插件/分配器实际分配的设备集合；默认/控制节点与作业节点区分记录；框架逻辑编号＝框架可见集；比较以稳定身份归一化（UUID/序列号，未取源则记 unknown），文本/数量一致不足以证明同一设备；三集合按已取证映射对应、不判全等：公共/默认控制设备节点（含 CDI 默认项、节点公共设备）vs 作业获配设备（Allocate 实际集合）vs 资源请求数量 vs 框架逻辑集合（可见集）；机器位置（生成/分发/运行主机）另行记录，不代替设备集合边界：

| 分支 | 观测 | 候选解释 | 所需证据 | 受控对照 | 边界与停止 |
|---|---|---|---|---|---|
| 设备注入缺失 | 设备文件/环境变量缺（限定注入模式：GPU 分 CDI 原生/nvidia-docker legacy，NPU 分 ascend-docker/原生挂载，缺模式 unknown 则先定模式） | 未分配 vs 未注入 vs 路径错误 | 请求集/最终注入集/框架可见集三单核对 | 同镜像/驱动，换注入模式 | 固定映射规则缺失（GPU/NPU 通用）→优先无法确定；规则已取时完成：三单一致，失败：三单齐且映射错；任一单缺证据→无法判定；解释不清即停，不扩大放宽权限 |
| 访问拒绝 | `Failed to initialize NVML: Insufficient Permissions`（权限段）、权限拒绝（GPU）；`Unknown Error` 属 hook/legacy 访问丢失段，不作权限拒绝证据；NPU 侧拒绝语义未取源（unknown） | 权限/SELinux/驱动 | 排障页 NVML/SELinux 段（警告 `--security-opt=label=disable` 放弃隔离，限 Insufficient Permissions 段）、附加 GID | 同条件换权限配置（不自动放宽生产策略） | 完成：拒绝消除、注入集完整且同一目标进程受控访问通过、原访问边界恢复；失败：同条件持续拒绝；无法判定：NPU 侧；同上 |
| 隔离范围 | 共享 GPU 互相影响 | time-slicing 无隔离（已知）；cgroups 未验证 | 共享配置＋影响证据 | 副本计数对照（未找到有依据的关共享开关对照；对照解释收窄为副本数作用域） | 完成：副本数变化后本次共享影响消失（本分支解释完成，不判显存/计算份额/故障域隔离成立）；失败：仍互相影响；无法判定：未做对照；同上 |
| 访问丢失 | 容器更新后 GPU 访问丢失 | hook/legacy 注入条件（排障页限定：更新可能撤销 hook 注入，重建容器为恢复路径之一，非充分恢复办法） | 更新前后注入集对比 | 回退更新（撤销更新≠已证实恢复，仅对照手段之一） | 完成：注入集恢复且同一目标进程受控访问通过、原访问边界恢复；失败：仍丢失；无法判定：未做对照；同上 |
| NPU 注入缺失 | NPU 设备文件/环境变量缺 | 未分配 vs 未注入 vs 路径错误（昇腾语义未取源，unknown） | 请求集/最终注入集/框架可见集三单核对 | 同镜像/驱动，换注入模式（ascend-docker/原生挂载） | 固定映射语义缺失→无法确定（优先于技术完成/失败）；语义已取时完成：三单一致，失败：三单齐且映射错；任一单缺证据→无法判定；同上 |
| NPU 逻辑选择分叉 | 节点在、逻辑选择失败（物理 ID 可列举，框架报范围错误） | 参数范围/选择语义（实现语义未取源，unknown） | 三单核对＋来源案例症状对照（物理 0/3/4/7 与逻辑 `[0,4)` 分叉） | 同条件复现 | 固定映射语义缺失→无法确定（优先，不判技术完成/失败）；语义已取时完成：映射一致，失败：三单齐仍持续分叉；缺证据→无法判定；同上 |
| NPU 访问拒绝 | 明确的权限拒绝事件（DAC/LSM） | 权限策略（语义未取源，unknown） | 拒绝事件＋进程/设备/时间关联 | 同条件复现 | 固定访问语义缺失→无法确定（优先，不判技术完成/失败）；语义已取时完成：拒绝消除且同一目标进程受控访问通过、原访问边界恢复，失败：持续拒绝；缺证据→无法判定；同上 |
| NPU 隔离范围 | 共享 NPU 互相影响 | 隔离语义未取源（unknown） | 共享配置＋影响证据 | NPU 独立对照（NVIDIA replicas 字段不适用；固定对照方法未取，unknown） | 固定隔离语义缺失→无法确定（优先）；语义已取时完成/失败按所选对照判；缺证据→无法判定；同上 |

对照方案（授权隔离环境内可执行计划表，每变体一行）。命名公共集合 S1（停止触发：未授权作业设备暴露/访问、进程/节点身份漂移、旁路漂移、影响其他负载）/R1（公共连接规则，各变体恢复栏引用 R1＋本变体主体/节点/时间窗）：阶段×对象绑定：变更前（基线主体/节点/时间窗快照）→变更后（变体主体/节点/时间窗快照）→恢复后（恢复主体/节点/时间窗＋正负访问结果）；每阶段记录＝主体（重建类新旧 ID 分别记）＋完整目标节点（类型/major/minor/路径/来源）＋稳定身份（未取则记 unknown）＋时间窗＋正负访问结果或未执行原因＋可定位证据（audit/AVC/配置摘要/快照 ID）；缺负向授权只记未执行：受控成功访问操作＝目标进程打开所选设备节点，记录＝open 结果＋框架可见集快照＋进程/设备/时间三元组；单独授权负向拒绝记录＝未授权设备 open 拒绝事件（errno/AVC）＋主体/节点/时间窗；恢复判据＝同一目标进程受控访问通过＋原 allow/负向边界恢复，证据＝恢复后配置对象摘要＋恢复后主体/节点/时间窗；阶段绑定：变更前（基线快照）→变更后（变体快照）→恢复后（R1 判据复核），重建类变体前后主体按新旧 ID 分别记录；凭访问证据，不凭三单可见性：

| 变体 | 唯一差异 | 主体/时间窗/字段 | 证据定位 | 旁路排除 | 负向验证前提 | 恢复边界 |
|---|---|---|---|---|---|---|
| 基线 | 无（同一镜像 digest/驱动版本/注入模式，记录三单集合） | 主体：单 Pod UID/容器 ID/目标进程 PID，时间窗：启动后快照时刻（待填）；字段：三单＋CDI 名＋OCI 节点 | 证据定位：CDI 文件路径/摘要、OCI `config.json` 路径/摘要、快照存档（待填，未取则记 unknown） | — | — | — |
| 换注入模式 | 唯一差异：两端字段级消费配置对（真实配置入口：插件 `flags.plugin.deviceListStrategy`（内部集合选择来源）＋`flags.plugin.passDeviceSpecs=false`（所选假设，关闭 DeviceSpecs 并行输出）；handler 名/旧新值待填。设计取值（所选假设）：基线端 `options.BinaryName` 取默认空（即默认 runc），Toolkit mode 不适用（CDI 原生直达低层 runtime，NVIDIA runtime 不参与）；变体端 legacy runtime hook 参与，Toolkit 对应 legacy 模式（设计值待填）。基线端＝Pod（`runtimeClassName` 或默认）→RuntimeClass `.handler`→containerd runtimes 表同名项（`runtime_type`＋options，含 `options.BinaryName` 执行器，值待填）→CDI 消费分支（`CdiDevices[].Name` qualified 名＋`cdi_spec_dirs` 可达＋containerEdits 落位＋Toolkit mode 取 CDI 模式设计值，待填；插件侧 `deviceListStrategies=[cdi-cri]` 且关闭其余并行输出）；变体端＝同链 handler→legacy hook 注入分支（插件侧 `deviceListStrategies=[envvar]`＋`NVIDIA_VISIBLE_DEVICES` 传递，无 CDI 引用）；旁路排除：DeviceSpecs/annotations/volume-mounts 任一端出现判混合→无法确定） | 主体：基线 Pod 与变体 Pod（UID/容器 ID/PID、节点各自记录）；时间窗：各自启动后快照时刻（待填） | 三单快照对比（CDI 文件路径/摘要、`config.json` 路径/摘要待填） | 旁路排除清单：privileged、设备 hostPath、人工挂载、默认注入、显式选择变量逐项确认无差异 | 授权隔离环境 | 安全停止：未授权作业设备暴露/访问、旁路漂移或影响其他负载时停止；恢复：恢复基线配置＋同一目标进程受控访问通过＋原负向边界恢复（三单可见性不证明权限边界，须访问证据） |
| 换权限配置 | 唯一差异：目标节点规则的完整比较对象（按 type/major/minor/`access` 选定目标规则，保存其规则索引、通配上下文与在 `linux.resources.devices[]` 中的顺序位置——规则按列表顺序应用；其余规则逐条保持；旧值→新值待填；UID/GID 为另一独立变体，不混改） | 主体：变更前后容器（旧新容器 ID/PID、节点、目标进程身份各自记录）；时间窗：变更前后快照（待填） | 拒绝事件（audit/AVC 路径待填）＋注入集 | 排除 SELinux 全局变更与上述旁路清单 | 不自动放宽生产策略；负向组：公共控制节点可见性与未请求作业设备不可见分别记录，未授权作业设备访问拒绝需单独授权（缺授权不执行）；停止/恢复按 S1/R1 绑定本变体：停止（身份/节点漂移、影响其他负载）即停；恢复（变更后目标进程受控访问记录＋原 allow 边界比较记录，证据对象见 R1；三单可见性不等访问恢复） | 同上 |
| 副本计数对照 | 唯一差异：sharing.timeSlicing.resources `nvidia.com/gpu` 的 `replicas`（旧值→新值待填；改变计数≠禁用共享策略，未找到有依据的关共享开关对照，隔离分支完成解释相应收窄） | 主体：同负载同 Pod/容器前后（容器 ID、目标进程、节点、旧新快照时刻分别记录） | 影响证据（共享配置＋影响记录路径待填） | 排除负载差异与上述旁路清单 | 同上 | 同上 |
| 镜像回退 | 仅镜像 digest 回退（旧值→新值待填；生命周期：重拉取→重建容器→新容器 ID/PID/快照；不代替 hook/legacy 资源更新对照） | 主体：回退前后容器（旧新容器 ID/PID、节点、观察窗各自记录；回退≠恢复，需恢复判据） | 回退前后注入集对比 | 排除配置漂移与上述旁路清单 | 不重启生产组件；恢复按 R1（目标主体为新容器关联） | 同上 |
| 驱动回退 | 仅驱动版本回退（旧值→新值待填；生命周期：重装驱动→重启运行时→重建容器；不代替资源更新对照） | 主体：回退前后容器（旧新容器 ID/PID、节点、观察窗各自记录） | 回退前后注入集对比 | 排除配置漂移与上述旁路清单 | 不重启生产组件；恢复按 R1 绑定本变体（目标主体为新容器关联；访问证据对象见 R1） | 同上 |
| 资源更新（hook/legacy） | 唯一差异：CPU 限制（接口/字段未选定，unknown；内存限制另立变体；以排障页 Affected Environments 为场景依据） | 主体：更新前后容器与目标进程（旧新容器 ID/PID、节点、观察窗各自记录；更新与重建为不同生命周期） | 更新前后注入集对比（接口选定后绑定同一次更新前后采样；回退/重建记录不替代） | 排除配置漂移与上述旁路清单 | 不重启生产组件；恢复按 R1 绑定本变体 | 同上 |
| 重建容器（hook/legacy） | 仅重建容器（更新撤销 hook 注入场景；旧容器 ID/PID/快照与新容器 ID/PID/快照分别记录，不按同 ID 判同一次运行） | 主体：旧新容器各自时间窗 | 重建前后注入集对比（旧新证据各自定位） | 排除配置漂移与上述旁路清单 | 恢复按 R1 绑定本变体（目标主体为新容器关联） | 同上 |

未授权设备负向验证须单独授权与隔离前提。源案例：[Ascend 来源案例](ascend-device-visibility-source-case.md)（症状：物理 ID 集合 `0,3,4,7` 与框架报范围 `[0,4)` 不一致，属逻辑编号/选择分叉；环境：torch 2.5.1/torch_npu 2.5.1.post1/vLLM 0.9.1/Ascend dev f6a0e1629/CANN 8.2.RC1；关键缺项（本页摘要，不以链接代替）：runtime/plugin/驱动固件版本、镜像 digest、CDI/注入模式、集群版本；版本范围与缺项明细见该页；非本库复现）与[待执行实验](ascend-device-visibility-experiment.md)（未执行）；判定设计见上表，不以链接代替。

只设计、未执行、不得作为已验证安装处方；源文档中的修改/恢复建议不赋予执行授权。

## 来源与更新范围

- 上表各入口（OCI 双规范、Toolkit 1.20.0 四页、设备插件 v0.20.1、Ascend 固定 commit 三文件）。
- 待确认（unknown 仅限以下，未读实现/配置、未执行结果或未固定文档修订；已读范围见上表，不扩大为无工具取证）：containerd 消费端输出（`crictl`/守护进程日志未取，unknown）；完整键清单见 §2（已交付，实际值待填）；runc 驱动细节与诊断命令输出；syft 全部 cataloger/扫描配置实现（README 已读范围外）与 SBOM 生成比对结果；cosign 未固定文档页修订与命令输出；构建输入工具选型；昇腾 runtime vdevice 切分/dcmi 完整实现与白名单变体内容/实际结果（插件静态输出、环境键定义链、runtime README＋process.go/hook 消费链、白名单源码链已读，见 §3；产品变体内容与实际结果未读/未执行）；NGC 之外镜像样板；全部实测（未执行）。
